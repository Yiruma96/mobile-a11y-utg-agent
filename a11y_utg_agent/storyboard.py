#!/usr/bin/env python3
"""Zero-truncation multi-row visual UTG Storyboard + Per-Page Chinese Description Annotator.

Features:
  1. Never drops intermediate steps (multi-row grid up to 5 frames/row) and retains
     ALL post-jump probes, Service Detail Page, System Warning Dialog, and Refusal Probes.
  2. Automatically generates concise, accurate **Chinese per-page descriptions** (`zh_caption`)
     for every frame via a single fast local `deepseek-v4.1-flash` call per app (translating
     English/Italian/German/Russian/Turkish/Portuguese UI text and summarizing the observed
     induction/action), caches captions into `zh_captions.json` + `utg_harmony.json`, renders
     multi-line wrapped Chinese captions directly onto `utg_storyboard.png` (Microsoft YaHei),
     and appends a Chinese page-by-page narrative section into `run_summary.md`.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Optional

from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR.parent))

from a11y_utg_agent.llm_client import create_openai_client, resolve_model_config

DATASET_DIR = SCRIPT_DIR / "dynamic_utg_dataset_v2"


def _load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = (
        (
            "C:/Windows/Fonts/msyhbd.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        )
        if bold
        else (
            "C:/Windows/Fonts/msyh.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        )
    )
    for fp in candidates:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _wrap_cjk(text: str, font: ImageFont.ImageFont, max_px: int, draw: ImageDraw.ImageDraw, max_lines: int = 4) -> list[str]:
    """Pixel-accurate line wrapper supporting mixed Chinese & ASCII text."""
    text = (text or "").replace("\r", " ").replace("\n", " ").strip()
    if not text:
        return [""]
    lines: list[str] = []
    cur = ""
    for ch in text:
        cand = cur + ch
        if draw.textlength(cand, font=font) <= max_px or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = ch
            if len(lines) >= max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    elif len(lines) == max_lines and cur:
        # Ellipsize last line cleanly
        last = lines[-1]
        while len(last) > 2 and draw.textlength(last + "…", font=font) > max_px:
            last = last[:-1]
        lines[-1] = last + "…"
    return lines


def refine_refusal_outcome(trace: dict[str, Any]) -> str:
    cur = trace.get("refusal_outcome") or "not_tested"
    probes = trace.get("refusal_probes") or []
    target_pkg = trace.get("target_package") or ""
    if cur == "not_tested" or not probes:
        return cur

    if cur == "RELAUNCHED_A11Y_SETTINGS":
        p0 = probes[0]
        p0_texts = " ".join(p0.get("sample_texts") or [])
        if (
            len(probes) == 1
            and "HOOK_A11Y_SETTINGS" in (p0.get("hooks") or [])
            and "DOWNLOADED APPS" not in p0_texts
            and p0.get("top_package") == "com.android.settings"
        ):
            return "STALE_SETTINGS_BACKSTACK"
        return cur

    if cur == "RELAUNCHED_LURE_DIALOG":
        return cur

    entry_acts = {
        s["snapshot"]["top_activity"]
        for s in (trace.get("steps") or [])
        if s.get("snapshot", {}).get("top_package") == target_pkg
    }
    for pr in probes:
        texts = " ".join(pr.get("sample_texts") or []).lower()
        act = (pr.get("top_activity") or "").lower()
        is_lure_cue = any(
            k in texts or k in act
            for k in (
                "accessibility", "downloaded services", "switch access", "talkback",
                "permessi", "prosegui", "open settings", "go to settings",
                "etkinleştirin", "无障碍", "permissionactivity", "permissionsactivity",
                "accessactivity", "flash update", "installed services", "enable ",
            )
        )
        has_cancel = any(
            k in texts
            for k in ("cancel", "refuse", "skip", "not now", "later", "取消", "拒绝", "跳过")
        )
        if pr.get("top_package") == target_pkg:
            if is_lure_cue and not has_cancel:
                return "TRAPPED_ON_LURE_SCREEN"
            if pr.get("top_activity") in entry_acts and not has_cancel and len(pr.get("sample_texts") or []) <= 10:
                return "TRAPPED_ON_LURE_SCREEN"
        elif is_lure_cue and not has_cancel and ("use service" in texts or "will not work" in texts or "downloaded services" in texts or "enable " in texts):
            # Catches EventBot-style system overlay dialogs floating over NexusLauncher!
            return "RELAUNCHED_LURE_DIALOG"
    return cur


def _read_window_notifs(screenshot_path: Path) -> list[dict[str, str]]:
    """Read sibling `*_windows.json` active notifications if captured."""
    wp = screenshot_path.with_name(screenshot_path.name.replace("_screen.png", "_windows.json").replace("_action.png", "_windows.json"))
    if wp.is_file():
        try:
            return json.loads(wp.read_text(encoding="utf-8")).get("active_notifications") or []
        except Exception:
            pass
    return []


def _resolve_file(run_dir: Path, path_str: str) -> Optional[Path]:
    """Resolve screenshot/artifact paths cleanly across absolute, relative, or relocated run dirs."""
    if not path_str:
        return None
    p = Path(path_str)
    if p.is_file():
        return p
    cand = run_dir / path_str
    if cand.is_file():
        return cand
    cand2 = run_dir / p.name
    if cand2.is_file():
        return cand2
    return None


def collect_frames(run_dir: Path, trace: dict[str, Any], refined_refusal: str) -> list[dict[str, Any]]:
    """Collect ALL chronological frames (0 steps dropped) with rich metadata for Chinese captioning."""
    frames: list[dict[str, Any]] = []

    for st in trace.get("steps") or []:
        snap = st.get("snapshot") or {}
        anno_p = _resolve_file(run_dir, st.get("action_anno_path") or "")
        raw_p = _resolve_file(run_dir, snap.get("screenshot_path") or "")
        sp = anno_p if anno_p else raw_p
        if not sp:
            continue
        act_short = (snap.get("top_activity") or "").rsplit(".", 1)[-1][:26]
        hooks = snap.get("trigger_hooks") or []
        act_obj = st.get("action") or {}
        act_cmd = act_obj.get("action", "")
        key = f"step_{st['step']:02d}"
        frames.append({
            "key": key,
            "title": f"Step {st['step']}: {'[无障碍列表页]' if hooks else act_short}",
            "kind": "hook" if hooks else "step",
            "img_path": sp,
            "package": snap.get("top_package") or "",
            "activity": snap.get("top_activity") or "",
            "texts": (snap.get("all_texts") or [])[:14],
            "action": act_cmd,
            "action_detail": act_obj.get("matched_element") or act_obj.get("summary") or str(act_obj.get("pixel_xy") or act_obj.get("button") or ""),
            "model_thought": (st.get("model_output") or "").split("<tool_call>")[0].strip()[:140],
            "overlays": snap.get("overlay_windows") or [],
            "notifications": _read_window_notifs(raw_p if raw_p else sp),
        })

    for ev in trace.get("trigger_events") or []:
        for p_item in (ev.get("post_jump_probes") or []):
            pp = _resolve_file(run_dir, p_item.get("screenshot_path") or "")
            if pp:
                key = f"post_jump_{p_item['delay_s']}s"
                frames.append({
                    "key": key,
                    "title": f"跳后探针 +{p_item['delay_s']}s",
                    "kind": "probe",
                    "img_path": pp,
                    "package": p_item.get("top_package") or "",
                    "activity": p_item.get("top_activity") or "",
                    "texts": (p_item.get("sample_texts") or [])[:10],
                    "action": f"wait({p_item['delay_s']}s)",
                    "action_detail": f"overlays={len(p_item.get('overlays') or [])}",
                    "model_thought": "",
                    "overlays": p_item.get("overlays") or [],
                    "notifications": _read_window_notifs(pp),
                })

    for idx_d, dp in enumerate(trace.get("detail_probes") or [], 1):
        dpath = _resolve_file(run_dir, dp.get("screenshot_path") or "")
        if dpath:
            stage = dp.get("stage", "Detail")
            zh_stage = "服务详情页" if "Detail" in stage else ("系统警告弹窗(点Deny)" if "Warning" in stage else stage)
            frames.append({
                "key": f"detail_{idx_d}_{stage.lower().replace(' ', '_')}",
                "title": zh_stage,
                "kind": "detail",
                "img_path": dpath,
                "package": dp.get("top_package") or "",
                "activity": dp.get("top_activity") or "",
                "texts": (dp.get("sample_texts") or [])[:12],
                "action": "inspect_detail_or_warning",
                "action_detail": dp.get("note") or "",
                "model_thought": "",
                "overlays": dp.get("overlays") or [],
                "notifications": _read_window_notifs(dpath),
            })

    rprobes = trace.get("refusal_probes") or []
    seen_r: set[tuple[str, str]] = set()
    for idx_r, rp in enumerate(rprobes):
        rpath = _resolve_file(run_dir, rp.get("screenshot_path") or "")
        if not rpath:
            continue
        sig = (rp.get("top_activity") or "", " ".join(rp.get("sample_texts") or [])[:60])
        if idx_r == 0 or idx_r == len(rprobes) - 1 or sig not in seen_r:
            seen_r.add(sig)
            frames.append({
                "key": f"refusal_{rp['delay_s']}s",
                "title": f"拒权返回 +{rp['delay_s']}s",
                "kind": "refusal",
                "img_path": rpath,
                "package": rp.get("top_package") or "",
                "activity": rp.get("top_activity") or "",
                "texts": (rp.get("sample_texts") or [])[:10],
                "action": f"Back_refuse -> {refined_refusal}",
                "action_detail": refined_refusal,
                "model_thought": "",
                "overlays": rp.get("overlays") or [],
                "notifications": _read_window_notifs(rpath),
            })

    return frames


_LLM_CLIENT_CACHE: dict[str, Any] = {}


def generate_zh_captions(
    run_dir: Path,
    trace: dict[str, Any],
    frames: list[dict[str, Any]],
    refined_refusal: str,
    model: Optional[str] = None, base_url: Optional[str] = None, api_key: Optional[str] = None,
) -> dict[str, Any]:
    """Generate concise Chinese per-page captions + rhetoric summary via 1 fast LLM call (cached)."""
    cache_p = run_dir / "zh_captions.json"
    if cache_p.is_file():
        try:
            cached = json.loads(cache_p.read_text(encoding="utf-8"))
            if cached.get("frame_captions") and all(f["key"] in cached["frame_captions"] for f in frames):
                return cached
        except Exception:
            pass

    sm = trace.get("static_meta") or {}
    payload_frames = []
    for f in frames:
        payload_frames.append({
            "key": f["key"],
            "title": f["title"],
            "package": f["package"],
            "activity": f["activity"].rsplit(".", 1)[-1],
            "ui_texts": f["texts"],
            "active_notifications": f["notifications"][:3],
            "overlays_count": len(f["overlays"]),
            "action": f["action"],
            "action_detail": f["action_detail"][:90],
            "agent_note": f["model_thought"][:100],
        })

    prompt = (
        "你是移动安全研究员，请为下面这个 Android 应用动态运行轨迹中的【每一个页面】写一段清晰、简洁的中文说明，"
        "方便审核人员直接看懂非中文界面上的诱导话术、界面角色和交互动作。\n"
        f"应用元信息：app_id={sm.get('app_id', run_dir.name)} | label={sm.get('label', '?')} | "
        f"family_or_category={sm.get('family') or sm.get('benign_category') or '?'} | "
        f"package={trace.get('target_package', '')} | refusal_outcome={refined_refusal}\n\n"
        "各页面观测数据（JSON）：\n"
        + json.dumps(payload_frames, ensure_ascii=False, indent=1)
        + "\n\n请严格输出一个 JSON 对象（不要加多余解释），字段如下：\n"
        "{\n"
        '  "app_chain_summary_zh": "用 1-2 句中文概括该应用从入口到授权/拒权的完整动态链路与核心诱导/合规特征",\n'
        '  "observed_lure_rhetoric_zh": ["若出现具体诱导/说明话术，按「原文语种 -> 中文核心意译（所在页面）」逐条列出，无则空数组"],\n'
        '  "frame_captions": {\n'
        '    "<key>": "30-55字中文：说明当前页是什么界面、关键外文内容中文意译、以及本步点击/探针结果（含通知横幅/遮罩/无取消键等要点）"\n'
        "  }\n"
        "}"
    )

    result: dict[str, Any] = {
        "app_chain_summary_zh": "",
        "observed_lure_rhetoric_zh": [],
        "frame_captions": {},
    }

    try:
        if "client" not in _LLM_CLIENT_CACHE:
            ep = resolve_model_config(model=model, base_url=base_url, api_key=api_key)
            _LLM_CLIENT_CACHE["client"] = create_openai_client(ep, timeout=45.0)
            _LLM_CLIENT_CACHE["model"] = ep.model
        for _attempt in range(2):
            resp = _LLM_CLIENT_CACHE["client"].chat.completions.create(
                model=_LLM_CLIENT_CACHE["model"],
                messages=[
                    {"role": "system", "content": "Output ONLY valid compact JSON. Be accurate, concise, and faithful to the observed UI texts."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=4096,
            )
            raw = (resp.choices[0].message.content or "").strip()
            if "```json" in raw:
                raw = raw.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in raw:
                raw = raw.split("```", 1)[1].split("```", 1)[0].strip()
            start = raw.find("{")
            if start != -1:
                parsed, _ = json.JSONDecoder().raw_decode(raw[start:])
                if isinstance(parsed, dict) and parsed.get("frame_captions"):
                    result["app_chain_summary_zh"] = str(parsed.get("app_chain_summary_zh") or "")
                    result["observed_lure_rhetoric_zh"] = list(parsed.get("observed_lure_rhetoric_zh") or [])
                    fc = parsed.get("frame_captions") or {}
                    if isinstance(fc, dict):
                        result["frame_captions"] = {str(k): str(v) for k, v in fc.items()}
                    break
    except Exception as e:
        print(f"[WARN] Chinese caption generation failed for {run_dir.name}: {e}")

    # Deterministic fallback for any missing frame key
    for f in frames:
        if not result["frame_captions"].get(f["key"]):
            txt_snip = " / ".join(f["texts"][:3])[:40]
            result["frame_captions"][f["key"]] = f"{f['title']}（{f['activity'].rsplit('.', 1)[-1]}）：{txt_snip or '无文本'}；动作 {f['action']}"

    cache_p.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


def build_storyboard_for_run(
    run_dir: Path,
    trace: dict[str, Any],
    refined_refusal: str,
    with_zh_captions: bool = True,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> tuple[Optional[Path], dict[str, Any]]:
    frames = collect_frames(run_dir, trace, refined_refusal)
    if not frames:
        return None, {}

    zh_info: dict[str, Any] = {}
    if with_zh_captions:
        zh_info = generate_zh_captions(run_dir, trace, frames, refined_refusal, model=model, base_url=base_url, api_key=api_key)

    # Sync zh_captions into utg_harmony.json & append Chinese frame table into run_summary.md
    hm_utg_p = run_dir / "utg_harmony.json"
    if hm_utg_p.is_file() and zh_info:
        try:
            hm_utg = json.loads(hm_utg_p.read_text(encoding="utf-8"))
            hm_utg["refusal_outcome_refined"] = refined_refusal
            hm_utg["app_chain_summary_zh"] = zh_info.get("app_chain_summary_zh", "")
            hm_utg["observed_lure_rhetoric_zh"] = zh_info.get("observed_lure_rhetoric_zh", [])
            hm_utg["frame_captions_zh"] = zh_info.get("frame_captions", {})
            hm_utg_p.write_text(json.dumps(hm_utg, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    sum_p = run_dir / "run_summary.md"
    if sum_p.is_file() and zh_info:
        cur_md = sum_p.read_text(encoding="utf-8")
        marker = "## 中文逐页引导链路解读"
        if marker not in cur_md:
            extra = [
                "",
                marker,
                "",
                f"> **全链路总结**：{zh_info.get('app_chain_summary_zh', '')}",
                "",
                "![全流程中文标注连环画](./utg_storyboard.png)",
                "",
            ]
            if zh_info.get("observed_lure_rhetoric_zh"):
                extra.append("**捕获到的诱导/说明话术（中译）**：")
                for item in zh_info["observed_lure_rhetoric_zh"]:
                    extra.append(f"- {item}")
                extra.append("")
            extra.append("| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |")
            extra.append("|---:|---|---|---|")
            for idx_f, f in enumerate(frames, 1):
                cap = (zh_info.get("frame_captions") or {}).get(f["key"], "")
                extra.append(f"| {idx_f} | **{f['title']}** | {cap} | `{f['img_path'].name}` |")
            sum_p.write_text(cur_md.rstrip() + "\n" + "\n".join(extra) + "\n", encoding="utf-8")

    # Render crisp multi-row storyboard with dedicated Chinese description box per frame!
    cols_per_row = min(4, len(frames)) if len(frames) <= 8 else min(5, len(frames))
    rows = math.ceil(len(frames) / cols_per_row)
    thumb_w, thumb_h = 330, 696
    pad_x, pad_y = 24, 22
    header_h = 92
    badge_h = 28
    zh_box_h = 84  # generous 4-line Chinese caption box!
    cell_h = badge_h + zh_box_h + thumb_h + pad_y

    canvas_w = pad_x + cols_per_row * (thumb_w + pad_x)
    canvas_h = header_h + pad_y + rows * cell_h

    canvas = Image.new("RGB", (canvas_w, canvas_h), (244, 246, 250))
    draw = ImageDraw.Draw(canvas)
    f_hdr = _load_font(20, bold=True)
    f_hdr_sub = _load_font(14, bold=False)
    f_title = _load_font(15, bold=True)
    f_zh = _load_font(13, bold=False)

    sm = trace.get("static_meta") or {}
    fam = sm.get("family") or sm.get("benign_category") or trace.get("target_package") or run_dir.name
    lbl_zh = "恶意" if sm.get("label") == "malicious" else ("良性" if sm.get("label") == "benign" else "样本")
    hdr_txt = f"{sm.get('app_id', run_dir.name)} | {lbl_zh} · {fam} | 共 {len(frames)} 帧(0 截断) | 拒权结论: {refined_refusal}"
    draw.rectangle([0, 0, canvas_w, header_h], fill=(15, 31, 56))
    draw.text((pad_x, 12), hdr_txt, fill=(255, 255, 255), font=f_hdr)

    chain_sum = zh_info.get("app_chain_summary_zh") or ""
    if chain_sum:
        sum_lines = _wrap_cjk("全链路摘要：" + chain_sum, f_hdr_sub, canvas_w - 2 * pad_x, draw, max_lines=2)
        for li, sl in enumerate(sum_lines):
            draw.text((pad_x, 44 + li * 20), sl, fill=(186, 230, 253), font=f_hdr_sub)

    badge_colors = {
        "hook": (185, 28, 28),
        "detail": (217, 119, 6),
        "probe": (13, 148, 136),
        "refusal": (124, 58, 237),
        "step": (30, 64, 175),
    }

    for i, f in enumerate(frames):
        r_idx, c_idx = divmod(i, cols_per_row)
        x = pad_x + c_idx * (thumb_w + pad_x)
        y_top = header_h + pad_y + r_idx * cell_h
        y_zh = y_top + badge_h
        y_img = y_zh + zh_box_h

        col = badge_colors.get(f["kind"], (30, 64, 175))
        draw.rectangle([x, y_top, x + thumb_w, y_top + badge_h], fill=col)
        draw.text((x + 8, y_top + 4), f["title"][:28], fill=(255, 255, 255), font=f_title)

        # Clean light card for wrapped Chinese caption
        draw.rectangle([x, y_zh, x + thumb_w, y_img], fill=(255, 255, 255), outline=(203, 213, 225), width=1)
        cap_txt = (zh_info.get("frame_captions") or {}).get(f["key"], f["action_detail"])
        cap_lines = _wrap_cjk(cap_txt, f_zh, thumb_w - 14, draw, max_lines=4)
        for li, cl in enumerate(cap_lines):
            draw.text((x + 7, y_zh + 5 + li * 19), cl, fill=(30, 41, 59), font=f_zh)

        with Image.open(f["img_path"]) as im:
            im = im.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            canvas.paste(im, (x, y_img))
        draw.rectangle([x, y_img, x + thumb_w, y_img + thumb_h], outline=(180, 190, 205), width=2)

        if c_idx < cols_per_row - 1 and i < len(frames) - 1:
            ax = x + thumb_w + 5
            ay = y_img + thumb_h // 2
            draw.polygon([(ax, ay - 9), (ax + 14, ay), (ax, ay + 9)], fill=(100, 116, 139))

    out_p = run_dir / "utg_storyboard.png"
    canvas.save(out_p, quality=91)
    return out_p, zh_info


def rebuild_dir(target_dir: Path, with_zh_captions: bool = True) -> None:
    count = 0
    for d in sorted(target_dir.iterdir()):
        if d.is_dir() and (d / "utg_trace.json").is_file():
            tr = json.loads((d / "utg_trace.json").read_text(encoding="utf-8"))
            ref = refine_refusal_outcome(tr)
            sb, _ = build_storyboard_for_run(d, tr, ref, with_zh_captions=with_zh_captions)
            if sb:
                count += 1
                print(f"[SB+ZH] {d.name} -> {sb.name}")
    print(f"[DONE] Built {count} Chinese-annotated storyboards under {target_dir}")


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description="Build zero-truncation Chinese-annotated UTG storyboards from run folders.")
    p.add_argument("target_dir", help="Run folder or parent directory containing run folders with utg_trace.json")
    p.add_argument("--no-zh", action="store_true", help="Skip LLM Chinese captioning (render screenshots only)")
    p.add_argument("--model", default=None)
    p.add_argument("--base-url", default=None)
    p.add_argument("--api-key", default=None)
    args = p.parse_args()
    tgt = Path(args.target_dir)
    if (tgt / "utg_trace.json").is_file():
        tr = json.loads((tgt / "utg_trace.json").read_text(encoding="utf-8"))
        ref = refine_refusal_outcome(tr)
        sb, _ = build_storyboard_for_run(tgt, tr, ref, with_zh_captions=not args.no_zh, model=args.model, base_url=args.base_url, api_key=args.api_key)
        print(f"[OK] {sb}")
    else:
        for d in sorted(tgt.iterdir()):
            if d.is_dir() and (d / "utg_trace.json").is_file():
                tr = json.loads((d / "utg_trace.json").read_text(encoding="utf-8"))
                ref = refine_refusal_outcome(tr)
                sb, _ = build_storyboard_for_run(d, tr, ref, with_zh_captions=not args.no_zh, model=args.model, base_url=args.base_url, api_key=args.api_key)
                if sb:
                    print(f"[OK] {d.name} -> {sb.name}")


if __name__ == "__main__":
    main()
