#!/usr/bin/env python3
"""Static-Guided Local-Model GUI-Owl (Mobile-Agent-v3.5) Agent + HarmonyOS-Ready UTG Builder.

Key capabilities:
  1. Static-Guided Dynamic Analysis (`--static_json`):
       Ingests the app's APKAudit static dossier (`step_by_step_flow`, `verbatim_texts`,
       `how_user_is_guided_to_enable`, `code_anchors`) so the GUI agent knows exactly
       which Tab/Button/Flow triggers Accessibility and how to bypass decoy screens.
       Optionally supports transparent static-guided Activity fallback (`--allow_activity_fallback`)
       if an app stalls on dead C2 / splash screens, explicitly tagging forced vs natural UTG edges.
  2. Complete Entry -> Induction -> Grant Hook -> Post-Jump Overlay -> Refusal Loop UTG:
       - Captures every step from Node 0 (cold start) to `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`.
       - At EVERY step, exports BOTH Android `step_XX_layout.xml` AND OpenHarmony
         `uitest dumpLayout`-compliant `step_XX_layout_harmony.json`.
       - Automatically runs `0.8s` & `2.0s` Post-Jump Overlay Probes (Golden Page 3) upon hook.
       - Automatically runs a Refusal-Loop Probe (`Back` once -> wait 2.0s & 5.0s, Golden Page 4)
         WITHOUT ever granting Accessibility to malware, classifying `RELAUNCHED_A11Y_SETTINGS`,
         `RELAUNCHED_LURE_DIALOG`, or `GRACEFUL_STAY_OR_DEGRADE`.
  3. Deliverables per app:
       - `utg_harmony.json`: HarmonyOS-ready directed UTG graph referencing `*_layout_harmony.json`
       - `utg_trace.json`  : Full raw dynamic execution trace
       - `utg_graph.mmd`   : Mermaid `flowchart TD` visualizing the complete Entry->Hook->Refusal path
       - `run_summary.md`  : Human-readable dynamic UTG & static-vs-dynamic comparison report
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from PIL import Image, ImageDraw

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR.parent))

from a11y_utg_agent.android_xml_to_harmony_json import convert_xml_file
from a11y_utg_agent.device_bridge import (
    DEFAULT_ADB_PATH,
    DEFAULT_HDC_PATH,
    AndroidLayoutController,
    HarmonyLayoutController,
    LayoutSnapshot,
)
from a11y_utg_agent.llm_client import create_openai_client, resolve_model_config

TOOL_CALL_OPEN = "<tool_call>"
TOOL_CALL_PATTERN = re.compile(r"<tool_call>\s*(.*?)\s*</tool_call>", re.DOTALL)


def _encode_image_b64(image_path: Path, max_side: int = 1280) -> str:
    with Image.open(image_path) as im:
        im = im.convert("RGB")
        if max(im.size) > max_side:
            scale = max_side / max(im.size)
            im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def _parse_tool_call(output_text: str) -> dict[str, Any]:
    if not output_text or not output_text.strip():
        raise ValueError("Empty model output")
    m = TOOL_CALL_PATTERN.search(output_text)
    if m:
        raw = m.group(1).strip()
    elif TOOL_CALL_OPEN in output_text:
        raw = output_text.split(TOOL_CALL_OPEN, 1)[1].strip()
    else:
        brace = output_text.find("{")
        if brace == -1:
            raise ValueError(f"No <tool_call> or JSON found: {output_text[:180]!r}")
        raw = output_text[brace:].strip()

    obj, _ = json.JSONDecoder().raw_decode(raw)
    if not isinstance(obj, dict):
        raise ValueError("Parsed tool call is not a JSON object")
    if "arguments" in obj and isinstance(obj["arguments"], dict):
        args = obj["arguments"]
    elif "action" in obj:
        args = obj
        obj = {"name": "mobile_use", "arguments": args}
    else:
        raise ValueError(f"Missing 'arguments' or 'action' key: {raw[:180]}")
    if "action" not in args:
        raise ValueError(f"Missing 'action' inside arguments: {raw[:180]}")
    return obj


def _annotate_action(screen_path: Path, action_args: dict[str, Any], out_path: Path) -> None:
    im = Image.open(screen_path).convert("RGB")
    draw = ImageDraw.Draw(im)
    act = action_args.get("action", "")
    if act in ("click", "long_press") and "pixel_xy" in action_args:
        cx, cy = action_args["pixel_xy"]
        r = 24
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(239, 68, 68), width=6)
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(239, 68, 68))
    elif act in ("swipe", "scroll") and "pixel_xy" in action_args and "pixel_xy2" in action_args:
        x1, y1 = action_args["pixel_xy"]
        x2, y2 = action_args["pixel_xy2"]
        draw.line([x1, y1, x2, y2], fill=(239, 68, 68), width=6)
        draw.ellipse([x2 - 12, y2 - 12, x2 + 12, y2 + 12], fill=(239, 68, 68))
    im.save(out_path)


def build_static_guidance(static_json_path: Optional[str]) -> tuple[str, dict[str, Any]]:
    """Extract a concise Static Guidance Brief + candidate Activity names from an APKAudit JSON."""
    if not static_json_path:
        return "", {}
    p = Path(static_json_path)
    if not p.exists():
        return "", {}
    d = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    item = d.get("item") or {}
    st = d.get("structured") or {}

    lines = [
        "=== STATIC ANALYSIS GUIDANCE (from APKAudit code audit — use this to reach the Accessibility prompt fast!) ===",
        f"- App label/family: {item.get('label', '?')} | family/cat: {item.get('family') or item.get('benign_category') or '?'} | static_visibility: {st.get('static_visibility', '?')}",
    ]
    if st.get("summary_one_liner"):
        lines.append(f"- Static summary: {str(st['summary_one_liner'])[:260]}")

    flow = st.get("step_by_step_flow") or []
    if flow:
        lines.append("- Static predicted pre-grant flow:")
        for step in flow[:6]:
            if isinstance(step, dict):
                s_idx = step.get("step", "?")
                where = step.get("screen_or_component") or step.get("page_name") or ""
                what = step.get("what_happens") or step.get("description") or step.get("user_action") or ""
                lines.append(f"    Step {s_idx} [{where}]: {str(what)[:160]}")
            else:
                lines.append(f"    - {str(step)[:160]}")

    vtexts = st.get("verbatim_texts") or []
    if vtexts:
        sample_btns = []
        for vt in vtexts[:6]:
            if isinstance(vt, dict):
                txt = vt.get("original_text") or vt.get("text") or ""
                loc = vt.get("location") or ""
                if txt:
                    sample_btns.append(f"{loc}: {str(txt)[:70]}")
        if sample_btns:
            lines.append("- Known UI strings/buttons from code: " + " | ".join(sample_btns[:4]))

    guide = st.get("how_user_is_guided_to_enable") or {}
    if isinstance(guide, dict):
        mech = guide.get("mechanism_summary") or guide.get("coercion_mechanism") or ""
        if mech:
            lines.append(f"- Enabling/coercion mechanism: {str(mech)[:220]}")

    # Extract candidate Activity names from code_anchors / step_by_step_flow for fallback if app stalls
    candidate_activities: list[str] = []
    blob = json.dumps({"flow": flow, "anchors": st.get("code_anchors") or []}, ensure_ascii=False)
    for m in re.finditer(r"\b([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+Activity[a-zA-Z0-9_$]*)\b", blob):
        act = m.group(1)
        if not act.startswith("android.") and not act.startswith("androidx.") and act not in candidate_activities:
            candidate_activities.append(act)

    meta = {
        "app_id": d.get("app_id", p.stem),
        "label": item.get("label", ""),
        "family": item.get("family", ""),
        "benign_category": item.get("benign_category", ""),
        "pool": item.get("pool", ""),
        "static_visibility": st.get("static_visibility", ""),
        "behavior_pattern_tags": st.get("behavior_pattern_tags") or [],
        "candidate_activities": candidate_activities[:6],
        "static_json_path": str(p),
    }
    return "\n".join(lines), meta


SYSTEM_PROMPT_HYBRID = """# Tools (Mobile-Agent-v3.5 / GUI-Owl Static-Guided Hybrid Protocol)

You control a mobile device via the `mobile_use` function to trace the complete UI path from app launch to the Accessibility Service permission prompt and System Accessibility Settings.
At each step, you receive:
  1. Static analysis guidance (if available) pointing out which button/tab/flow triggers the Accessibility prompt.
  2. The live OS UI layout list with numbered elements `[1]`, `[2]`, ... and their exact center coordinates.
  3. (In hybrid/vision mode) The live screen image (annotated with matching `[id]` boxes in hybrid mode).

Available actions inside `<tool_call>{"name": "mobile_use", "arguments": {...}}</tool_call>`:
- `click`: Preferred: pass `"element_id": <int>` from the layout list for pixel-exact tapping. If inside a WebView/image not in the list, pass `"coordinate": [x, y]` in ACTUAL screen pixels (`Screen: WxH`).
- `long_press`: `"element_id"` or `"coordinate": [x, y]`, optional `"time": 1.0`.
- `swipe`: `"coordinate": [x1, y1]`, `"coordinate2": [x2, y2]` in ACTUAL screen pixels (e.g. scroll down: `[540, 1800]` -> `[540, 600]`).
- `type`: `"text": "..."` to type into the focused input box.
- `system_button`: `"button": "Back" | "Home" | "Enter"`.
- `open`: `"package": "com.example.app"` to relaunch the target app if you accidentally left it.
- `wait`: `"time": 2` to wait for splash/loading/delayed popups.
- `terminate`: `"status": "success" | "failure"`, `"summary": "brief reason"` ONLY when the goal is complete OR confirmed unreachable (e.g. app crashed, demands live C2/login that is offline).

CRITICAL SAFETY & EFFICIENCY RULES:
- Follow the static analysis guidance first if a matching button/tab/dialog is visible!
- Dismiss standard Android runtime permission dialogs (Allow / Continue / OK) if they block reaching the Accessibility prompt.
- NEVER actually toggle ON a malicious Accessibility Service inside System Settings; stop as soon as Android Accessibility Settings opens.
- Avoid repeating the exact same ineffective click/swipe twice; try a different element or Back.

Response format for EVERY step (strictly 2 parts, nothing else):
Action: <one short imperative sentence describing what you are doing and why>
<tool_call>
{"name": "mobile_use", "arguments": {"action": "...", ...}}
</tool_call>
"""

SYSTEM_PROMPT_VISION_ONLY = """# Tools (Mobile-Agent-v3.5 / GUI-Owl Native Vision Protocol)

You control a mobile device via `mobile_use`. Coordinates are normalized to 1000x1000.
Actions: `click` (`coordinate`), `long_press` (`coordinate`, `time`), `swipe` (`coordinate`, `coordinate2`), `type` (`text`), `system_button` (`button`: Back|Home|Enter), `wait` (`time`), `terminate` (`status`, `summary`).

Response format for EVERY step (strictly 2 parts):
Action: <one short sentence>
<tool_call>
{"name": "mobile_use", "arguments": {"action": "...", ...}}
</tool_call>
"""


def build_step_messages(
    mode: str,
    instruction: str,
    static_guidance: str,
    snap: LayoutSnapshot,
    history_lines: list[str],
    extra_hint: str = "",
) -> list[dict[str, Any]]:
    sys_prompt = SYSTEM_PROMPT_VISION_ONLY if mode == "vision_only" else SYSTEM_PROMPT_HYBRID
    hist_str = "\n".join(history_lines[-10:]) if history_lines else "None (first step)"

    text_lines = [f"Goal: {instruction}"]
    if static_guidance:
        text_lines.append("\n" + static_guidance)
    text_lines.append(f"\nPrevious steps:\n{hist_str}")

    if mode != "vision_only":
        text_lines.append("\nCurrent Live Layout (from OS UI hierarchy dump):\n" + snap.to_compact_prompt_text())
    else:
        text_lines.append(
            f"\nCurrent Focus: package={snap.top_package} activity={snap.top_activity} "
            f"hooks={snap.trigger_hooks}"
        )
    if extra_hint:
        text_lines.append("\n" + extra_hint)

    user_parts: list[dict[str, Any]] = [{"type": "text", "text": "\n".join(text_lines)}]
    if mode == "hybrid":
        img_to_send = Path(snap.som_path) if snap.som_path and Path(snap.som_path).exists() else Path(snap.screenshot_path)
        user_parts.append({"type": "image_url", "image_url": {"url": _encode_image_b64(img_to_send)}})
    elif mode == "vision_only":
        user_parts.append({"type": "image_url", "image_url": {"url": _encode_image_b64(Path(snap.screenshot_path))}})

    return [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_parts},
    ]


def _resolve_pixel_coords(action_args: dict[str, Any], snap: LayoutSnapshot, mode: str = "hybrid") -> dict[str, Any]:
    out = dict(action_args)
    if "element_id" in out and out["element_id"] is not None:
        eid = int(out["element_id"])
        match = next((e for e in snap.elements if e.elem_id == eid), None)
        if match is not None:
            out["pixel_xy"] = list(match.center)
            out["matched_element"] = match.short_label()
            return out

    c1 = out.get("coordinate") if isinstance(out.get("coordinate"), list) and len(out["coordinate"]) == 2 else None
    c2 = out.get("coordinate2") if isinstance(out.get("coordinate2"), list) and len(out["coordinate2"]) == 2 else None
    vals = []
    if c1:
        vals.extend([float(c1[0]), float(c1[1])])
    if c2:
        vals.extend([float(c2[0]), float(c2[1])])
    use_norm_1000 = (mode == "vision_only") and bool(vals) and all(0.0 <= v <= 1000.0 for v in vals)

    def _to_px(pair: list[Any]) -> list[int]:
        nx, ny = float(pair[0]), float(pair[1])
        if use_norm_1000:
            px = int(round(nx / 1000.0 * snap.screen_width))
            py = int(round(ny / 1000.0 * snap.screen_height))
        else:
            px, py = int(round(nx)), int(round(ny))
        return [max(0, min(snap.screen_width - 1, px)), max(0, min(snap.screen_height - 1, py))]

    if c1:
        out["pixel_xy"] = _to_px(c1)
    if c2:
        out["pixel_xy2"] = _to_px(c2)
    return out


def _convert_snap_to_harmony(snap: LayoutSnapshot, map_system_settings: bool = True) -> str:
    """Convert a captured Android XML layout snapshot into OpenHarmony uitest dumpLayout JSON."""
    if not snap.raw_layout_path or not snap.raw_layout_path.endswith(".xml"):
        return snap.raw_layout_path
    xml_p = Path(snap.raw_layout_path)
    if not xml_p.exists():
        return ""
    hm_p = xml_p.with_name(xml_p.stem + "_harmony.json")
    convert_xml_file(
        xml_p,
        hm_p,
        top_package=snap.top_package,
        top_activity=snap.top_activity,
        screen_width=snap.screen_width,
        screen_height=snap.screen_height,
        map_system_settings=map_system_settings,
    )
    return str(hm_p)


def _export_utg_harmony_and_mermaid(run_dir: Path, trace: dict[str, Any]) -> tuple[Path, Path]:
    """Export clean HarmonyOS-ready UTG graph (`utg_harmony.json`) and Mermaid diagram (`utg_graph.mmd`)."""
    hm_nodes = []
    for node_id, info in trace["utg_nodes"].items():
        hm_nodes.append({
            "node_id": node_id,
            "first_step": info["first_step"],
            "role": info.get("role", "intermediate"),
            "bundleName": info["top_package"],
            "abilityName": info["top_activity"],
            "trigger_hooks": info.get("trigger_hooks") or [],
            "overlay_windows": info.get("overlay_windows") or [],
            "sample_texts": info.get("sample_texts") or [],
            "harmony_layout_json": Path(info.get("harmony_layout_path") or "").name,
            "android_layout_xml": Path(info.get("raw_layout_path") or "").name,
            "screenshot": Path(info.get("screenshot_path") or "").name,
        })

    utg_hm = {
        "schema": "harmonyos_utg_v1",
        "layout_format": "openharmony_arkxtest_uitest_dumpLayout",
        "app_id": (trace.get("static_meta") or {}).get("app_id") or trace.get("target_package") or "",
        "label": (trace.get("static_meta") or {}).get("label") or "",
        "family_or_category": (trace.get("static_meta") or {}).get("family")
                              or (trace.get("static_meta") or {}).get("benign_category") or "",
        "static_visibility": (trace.get("static_meta") or {}).get("static_visibility") or "",
        "target_package": trace.get("target_package") or "",
        "model": trace["model"],
        "mode": trace["mode"],
        "offline_isolated": trace["offline_isolated"],
        "final_status": trace["final_status"],
        "reached_a11y_hook": any("HOOK_A11Y_SETTINGS" in (ev.get("hooks") or []) for ev in trace.get("trigger_events") or []),
        "reached_app_details_hook": any("HOOK_APP_DETAILS" in (ev.get("hooks") or []) for ev in trace.get("trigger_events") or []),
        "refusal_outcome": trace.get("refusal_outcome") or "not_tested",
        "entry_node_id": trace.get("entry_node_id") or "",
        "hook_node_ids": trace.get("hook_node_ids") or [],
        "nodes": hm_nodes,
        "edges": trace.get("utg_edges") or [],
        "trigger_events": trace.get("trigger_events") or [],
        "detail_probes": trace.get("detail_probes") or [],
        "refusal_probes": trace.get("refusal_probes") or [],
    }
    utg_hm_path = run_dir / "utg_harmony.json"
    utg_hm_path.write_text(json.dumps(utg_hm, indent=2, ensure_ascii=False), encoding="utf-8")

    # Mermaid flowchart TD
    mmd_lines = ["flowchart TD"]
    for n in hm_nodes:
        nid = f"N_{n['node_id']}"
        act_short = (n["abilityName"] or "Screen").rsplit(".", 1)[-1][:28]
        hook_tag = f" [{','.join(n['trigger_hooks'])}]" if n["trigger_hooks"] else ""
        txt_snip = (n["sample_texts"][0][:22] if n["sample_texts"] else "").replace('"', "'")
        label = f"Step {n['first_step']}: {act_short}{hook_tag}\\n{txt_snip}"
        mmd_lines.append(f'    {nid}["{label}"]')
    for e in trace.get("utg_edges") or []:
        src = f"N_{e['from']}"
        dst = f"N_{e['to']}"
        elbl = f"{e.get('edge_type', 'ui')}: {str(e.get('action', ''))[:32]}".replace('"', "'")
        mmd_lines.append(f'    {src} -->|"{elbl}"| {dst}')
    mmd_path = run_dir / "utg_graph.mmd"
    mmd_path.write_text("\n".join(mmd_lines) + "\n", encoding="utf-8")
    return utg_hm_path, mmd_path


def _write_run_summary(run_dir: Path, trace: dict[str, Any]) -> Path:
    md = run_dir / "run_summary.md"
    sm = trace.get("static_meta") or {}
    lines = [
        "# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告",
        "",
        f"- **运行时间**：{trace['started_at']}",
        f"- **平台与设备**：`{trace['platform']}` / `{trace['device'] or 'default'}`（断网隔离：`{trace['offline_isolated']}`）",
        f"- **驱动模型与模式**：`{trace['model']}`（模式：`{trace['mode']}`）",
        f"- **目标应用**：`{trace.get('target_package') or 'N/A'}`（静态标签：`{sm.get('label') or 'N/A'}` / `{sm.get('family') or sm.get('benign_category') or 'N/A'}` / 静态可见性：`{sm.get('static_visibility') or 'N/A'}`）",
        f"- **最终状态**：`{trace['final_status']}`（共执行 {len(trace['steps'])} 步，UTG 唯一节点 `{len(trace['utg_nodes'])}` 个，有向边 `{len(trace['utg_edges'])}` 条）",
        f"- **拒权回退探针结论（Golden Page ④）**：`{trace.get('refusal_outcome') or 'not_tested'}`",
        "",
        "## 1. 触发钩子与黄金 UTG 页面捕获汇总",
        "",
    ]
    hooks = trace.get("trigger_events") or []
    if hooks:
        lines.append("| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |")
        lines.append("|---:|---|---|---|---|")
        for ev in hooks:
            probes = ev.get("post_jump_probes") or []
            ov_txt = " / ".join(
                f"{p['delay_s']}s: {'有遮罩(' + str(len(p['overlays'])) + ')' if p['overlays'] else '无异源遮罩'}"
                for p in probes
            ) or "N/A"
            lines.append(
                f"| Step {ev['step']} | `{', '.join(ev['hooks'])}` | "
                f"`{ev['top_package']}/{ev['top_activity']}` | {ov_txt} | "
                f"`{Path(ev.get('harmony_layout_path') or '').name}` |"
            )
    else:
        lines.append("- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。")

    if trace.get("refusal_probes"):
        lines.extend(["", "## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）", ""])
        for rp in trace["refusal_probes"]:
            lines.append(
                f"- **Back 后 +{rp['delay_s']}s**：`{rp['top_package']}/{rp['top_activity']}` | "
                f"hooks=`{rp['hooks']}` | overlays=`{len(rp['overlays'])}` | "
                f"texts=`{' / '.join(rp.get('sample_texts', [])[:5])}`"
            )

    lines.extend([
        "",
        "## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）",
        "",
        "| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |",
        "|---:|---|---|---:|---|---|---|",
    ])
    for st in trace["steps"]:
        snap = st["snapshot"]
        act = st.get("action") or {}
        act_desc = f"`{act.get('action', '-')}`"
        if act.get("matched_element"):
            act_desc += f" → {act['matched_element'][:55]}"
        elif act.get("pixel_xy"):
            act_desc += f" → {act['pixel_xy']}"
        elif act.get("button"):
            act_desc += f" → {act['button']}"
        elif act.get("summary"):
            act_desc += f" → {act['summary'][:55]}"
        lines.append(
            f"| {st['step']} | `{snap['top_package']}` / `{snap['top_activity'].split('.')[-1]}` | "
            f"`{','.join(snap['trigger_hooks']) or '-'}` | {snap['element_count']} | "
            f"{snap['text_char_count']} / {'是' if snap['needs_ocr_fallback'] else '否'} | "
            f"{act_desc} | `{Path(snap['raw_layout_path']).name}` + `{Path(st.get('harmony_layout_path') or '').name}` |"
        )

    lines.extend(["", "## 4. 各步骤原始界面文本摘录", ""])
    for st in trace["steps"]:
        snap = st["snapshot"]
        sample_texts = [t.replace("\n", " ").strip() for t in snap.get("all_texts", []) if t.strip()][:10]
        lines.append(
            f"- **Step {st['step']} (`{snap['top_package']}/{snap['top_activity'].split('.')[-1]}`)**: "
            + (" | ".join(f"`{t[:55]}`" for t in sample_texts) or "(空文本)")
        )

    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md


def run_agent(args: argparse.Namespace) -> tuple[Path, dict[str, Any]]:
    ep = resolve_model_config(
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key,
    )
    static_guidance, static_meta = build_static_guidance(args.static_json)
    print(f"[MODEL] {ep.safe_summary()} | mode={args.mode} | static_guided={bool(static_guidance)}")

    if args.platform == "android":
        ctrl: Any = AndroidLayoutController(adb_path=args.adb_path, device=args.device)
    else:
        ctrl = HarmonyLayoutController(hdc_path=args.hdc_path, device=args.device)

    client = create_openai_client(ep, timeout=60.0)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag = re.sub(r"[^a-zA-Z0-9._-]+", "_", args.tag or static_meta.get("app_id") or args.package or "session")[:48]
    run_dir = Path(args.output_dir) / f"{ts}_{tag}"
    run_dir.mkdir(parents=True, exist_ok=True)

    target_pkg = args.package or ""
    install_error = ""
    if args.apk and args.platform == "android":
        apk_p = Path(args.apk)
        if args.clean_sandbox:
            wiped = ctrl.wipe_all_third_party_apps()
            if wiped:
                print(f"[SANDBOX WIPE] Removed {len(wiped)} leftover 3rd-party pkg(s): {wiped}")
        if args.offline:
            print("[ISOLATION] Disabling emulator Wi-Fi & mobile data before APK launch...")
            ctrl.set_offline(True)
        before_pkgs = set(ctrl.list_third_party_packages())
        print(f"[INSTALL] Installing {apk_p.name} ...")
        ok, msg = ctrl.install_apk(apk_p)
        if not ok:
            install_error = msg[:300]
            print(f"[INSTALL FAILED] {install_error}")
        else:
            after_pkgs = set(ctrl.list_third_party_packages())
            new_pkgs = sorted(after_pkgs - before_pkgs)
            if not target_pkg:
                if new_pkgs:
                    target_pkg = new_pkgs[0]
                else:
                    m = re.match(r"^([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+)", apk_p.name)
                    if m:
                        target_pkg = m.group(1)
            # Merge live manifest activities into static_meta candidate_activities
            if target_pkg:
                live_comps = ctrl.get_package_activities(target_pkg)
                live_acts = [c.split("/", 1)[1] for c in live_comps if "/" in c]
                merged = list(static_meta.get("candidate_activities") or [])
                for la in live_acts:
                    if la not in merged:
                        merged.append(la)
                static_meta["candidate_activities"] = merged[:15]
            print(f"[INSTALL OK] target_package={target_pkg} (manifest_acts={len(static_meta.get('candidate_activities') or [])})")

    trace: dict[str, Any] = {
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "platform": args.platform,
        "device": args.device,
        "model": ep.model,
        "provider": "openai_compatible",
        "mode": args.mode,
        "target_package": target_pkg,
        "apk_path": args.apk or "",
        "offline_isolated": bool(args.offline),
        "static_meta": static_meta,
        "instruction": args.instruction,
        "final_status": "install_failed" if install_error else "max_steps_reached",
        "install_error": install_error,
        "entry_node_id": "",
        "hook_node_ids": [],
        "refusal_outcome": "not_tested",
        "steps": [],
        "utg_nodes": {},
        "utg_edges": [],
        "trigger_events": [],
        "detail_probes": [],
        "refusal_probes": [],
    }

    if install_error:
        trace["finished_at"] = datetime.now().isoformat(timespec="seconds")
        (run_dir / "utg_trace.json").write_text(json.dumps(trace, indent=2, ensure_ascii=False), encoding="utf-8")
        _export_utg_harmony_and_mermaid(run_dir, trace)
        _write_run_summary(run_dir, trace)
        return run_dir, trace

    if target_pkg and args.platform == "android":
        ctrl.force_stop("com.android.settings")
        ctrl.home()
        time.sleep(0.8)
        print(f"[LAUNCH] Opening {target_pkg} ...")
        ctrl.open_app(target_pkg)
        time.sleep(2.5)

    history_lines: list[str] = []
    seen_hooks: set[tuple[str, str]] = set()
    prev_hash: Optional[str] = None
    prev_action_label: Optional[str] = None
    prev_edge_type: str = "ui_action"
    stagnant_count = 0
    tried_fallback_acts: set[str] = set()

    def register_node(snap: LayoutSnapshot, hm_path: str, step_num: int, role: str = "intermediate") -> None:
        if not trace["entry_node_id"]:
            trace["entry_node_id"] = snap.structure_hash
            role = "entry"
        if snap.trigger_hooks:
            role = "trigger_hook"
            if snap.structure_hash not in trace["hook_node_ids"]:
                trace["hook_node_ids"].append(snap.structure_hash)
        if snap.structure_hash not in trace["utg_nodes"]:
            trace["utg_nodes"][snap.structure_hash] = {
                "first_step": step_num,
                "role": role,
                "top_package": snap.top_package,
                "top_activity": snap.top_activity,
                "trigger_hooks": snap.trigger_hooks,
                "overlay_windows": snap.overlay_windows,
                "sample_texts": snap.all_texts[:15],
                "screenshot_path": snap.screenshot_path,
                "raw_layout_path": snap.raw_layout_path,
                "harmony_layout_path": hm_path,
            }

    for step in range(1, args.max_steps + 1):
        step_tag = f"step_{step:02d}"
        print(f"\n================ STEP {step}/{args.max_steps} ================")
        snap = ctrl.capture_snapshot(run_dir, step_tag, draw_som=(args.mode == "hybrid"))
        hm_path = _convert_snap_to_harmony(snap, map_system_settings=args.map_system_settings) if args.platform == "android" else snap.raw_layout_path
        print(
            f"[LAYOUT] pkg={snap.top_package} act={snap.top_activity} "
            f"elements={len(snap.elements)} chars={snap.text_char_count} "
            f"hooks={snap.trigger_hooks} overlays={len(snap.overlay_windows)}"
        )

        register_node(snap, hm_path, step)
        if prev_hash is not None:
            trace["utg_edges"].append({
                "from": prev_hash,
                "to": snap.structure_hash,
                "step": step - 1,
                "edge_type": prev_edge_type,
                "action": prev_action_label or "",
            })
            if snap.structure_hash == prev_hash:
                stagnant_count += 1
            else:
                stagnant_count = 0

        # ---- Trigger Hook Fired: Post-Jump Overlay Probe (Golden Page 3) + Refusal-Loop Probe (Golden Page 4) ----
        if snap.trigger_hooks and args.platform == "android":
            hk_key = (snap.structure_hash, ",".join(snap.trigger_hooks))
            if hk_key not in seen_hooks:
                seen_hooks.add(hk_key)
                print(f"[TRIGGER HOOK FIRED] {snap.trigger_hooks}! Running 0.8s & 2.0s post-jump overlay probes...")
                probes = []
                for idx_p, (sleep_s, cum_s) in enumerate(((0.8, 0.8), (1.2, 2.0))):
                    time.sleep(sleep_s)
                    p_tag = f"{step_tag}_probe_{int(cum_s * 1000)}ms"
                    p_snap = ctrl.capture_snapshot(run_dir, p_tag, draw_som=False)
                    p_hm = _convert_snap_to_harmony(p_snap, map_system_settings=args.map_system_settings)
                    probes.append({
                        "delay_s": cum_s,
                        "top_package": p_snap.top_package,
                        "top_activity": p_snap.top_activity,
                        "hooks": p_snap.trigger_hooks,
                        "overlays": p_snap.overlay_windows,
                        "screenshot_path": p_snap.screenshot_path,
                        "harmony_layout_path": p_hm,
                    })
                    if p_snap.structure_hash != snap.structure_hash:
                        register_node(p_snap, p_hm, step, role="post_jump_probe")
                        trace["utg_edges"].append({
                            "from": snap.structure_hash,
                            "to": p_snap.structure_hash,
                            "step": step,
                            "edge_type": "post_jump_probe",
                            "action": f"wait({cum_s}s)_post_jump",
                        })

                trace["trigger_events"].append({
                    "step": step,
                    "hooks": snap.trigger_hooks,
                    "top_package": snap.top_package,
                    "top_activity": snap.top_activity,
                    "screenshot_path": snap.screenshot_path,
                    "raw_layout_path": snap.raw_layout_path,
                    "harmony_layout_path": hm_path,
                    "post_jump_probes": probes,
                })

                # Optional Safe Service-Detail + System-Warning-Dialog Capture (NEVER clicks Allow!)
                entered_detail_page = False
                if args.capture_service_detail and "HOOK_A11Y_SETTINGS" in snap.trigger_hooks:
                    # Find the first clickable/text row directly below "DOWNLOADED APPS" (and above "SCREEN READERS")
                    dl_y, sr_y = None, 99999
                    for el in snap.elements:
                        tl = (el.text or "").upper()
                        if "DOWNLOADED APP" in tl or "DOWNLOADED SERVICE" in tl or "已下载" in tl:
                            dl_y = el.bounds[3]
                        elif ("SCREEN READER" in tl or "DISPLAY" in tl or "屏幕阅读" in tl) and dl_y is not None:
                            sr_y = min(sr_y, el.bounds[1])
                    svc_el = None
                    if dl_y is not None:
                        cands = [
                            el for el in snap.elements
                            if el.bounds[1] >= dl_y - 5 and el.bounds[3] <= sr_y + 5
                            and (el.text or el.clickable)
                            and (el.text or "").strip().upper() not in ("OFF", "ON", "DOWNLOADED APPS", "DOWNLOADED SERVICES")
                        ]
                        if cands:
                            svc_el = sorted(cands, key=lambda e: (e.bounds[1], -int(bool(e.text))))[0]
                    if svc_el is not None:
                        print(f"[SERVICE DETAIL] Tapping downloaded service row: {svc_el.short_label()}")
                        ctrl.tap(svc_el.center[0], svc_el.center[1])
                        time.sleep(1.5)
                        d_snap = ctrl.capture_snapshot(run_dir, f"{step_tag}_service_detail", draw_som=False)
                        d_hm = _convert_snap_to_harmony(d_snap, map_system_settings=args.map_system_settings)
                        register_node(d_snap, d_hm, step, role="service_detail")
                        trace["utg_edges"].append({
                            "from": snap.structure_hash,
                            "to": d_snap.structure_hash,
                            "step": step,
                            "edge_type": "detail_probe",
                            "action": f"click_service({svc_el.text[:24]})",
                        })
                        trace["detail_probes"].append({
                            "stage": "Service Detail Page",
                            "note": " ".join(d_snap.all_texts[:4])[:60],
                            "top_package": d_snap.top_package,
                            "top_activity": d_snap.top_activity,
                            "overlays": d_snap.overlay_windows,
                            "sample_texts": d_snap.all_texts[:15],
                            "screenshot_path": d_snap.screenshot_path,
                            "harmony_layout_path": d_hm,
                        })
                        entered_detail_page = (d_snap.structure_hash != snap.structure_hash)

                        # Tap the 'Use service' toggle to trigger the System Warning Dialog, then IMMEDIATELY click Deny!
                        toggle_el = next(
                            (e for e in d_snap.elements if e.checkable or "switch" in e.class_name.lower() or "use " in (e.text or "").lower()),
                            None,
                        )
                        if entered_detail_page and toggle_el is not None:
                            print(f"[WARNING DIALOG] Tapping switch to inspect System Warning Dialog (will click Deny): {toggle_el.short_label()}")
                            ctrl.tap(toggle_el.center[0], toggle_el.center[1])
                            time.sleep(1.0)
                            w_snap = ctrl.capture_snapshot(run_dir, f"{step_tag}_system_warning", draw_som=False)
                            w_hm = _convert_snap_to_harmony(w_snap, map_system_settings=args.map_system_settings)
                            register_node(w_snap, w_hm, step, role="system_warning_dialog")
                            trace["utg_edges"].append({
                                "from": d_snap.structure_hash,
                                "to": w_snap.structure_hash,
                                "step": step,
                                "edge_type": "warning_probe",
                                "action": "click_use_service_switch",
                            })
                            trace["detail_probes"].append({
                                "stage": "System Warning Dialog",
                                "note": f"Overlays:{len(w_snap.overlay_windows)} | " + " ".join(w_snap.all_texts[:3])[:45],
                                "top_package": w_snap.top_package,
                                "top_activity": w_snap.top_activity,
                                "overlays": w_snap.overlay_windows,
                                "sample_texts": w_snap.all_texts[:15],
                                "screenshot_path": w_snap.screenshot_path,
                                "harmony_layout_path": w_hm,
                            })
                            # SAFETY: Always tap Deny / Cancel (NEVER Allow!)
                            deny_el = next(
                                (e for e in w_snap.elements if (e.text or "").strip().lower() in ("deny", "cancel", "拒绝", "取消", "不允许")),
                                None,
                            )
                            if deny_el is not None:
                                print(f"[SAFETY DENY] Clicking {deny_el.text!r} so service stays OFF.")
                                ctrl.tap(deny_el.center[0], deny_el.center[1])
                                time.sleep(0.8)
                            else:
                                ctrl.back()
                                time.sleep(0.8)

                # Automatic Refusal-Loop Probe (Golden Page 4) when HOOK_A11Y_SETTINGS fires!
                if args.probe_refusal and "HOOK_A11Y_SETTINGS" in snap.trigger_hooks:
                    print("[REFUSAL PROBE] Pressing Back to exit Settings and test refusal-loop behavior...")
                    if entered_detail_page:
                        ctrl.back()
                        time.sleep(0.7)
                    ctrl.back()
                    refusal_probes = []
                    ref_prev_hash = snap.structure_hash
                    outcome = "GRACEFUL_STAY_OR_DEGRADE"
                    for sleep_s, cum_s in ((2.0, 2.0), (3.5, 5.5), (5.0, 10.5)):
                        time.sleep(sleep_s)
                        r_tag = f"{step_tag}_refusal_{int(cum_s * 1000)}ms"
                        r_snap = ctrl.capture_snapshot(run_dir, r_tag, draw_som=False)
                        r_hm = _convert_snap_to_harmony(r_snap, map_system_settings=args.map_system_settings)
                        register_node(r_snap, r_hm, step, role="refusal_probe")
                        trace["utg_edges"].append({
                            "from": ref_prev_hash,
                            "to": r_snap.structure_hash,
                            "step": step,
                            "edge_type": "refusal_probe",
                            "action": "Back_refuse" if cum_s == 2.0 else f"wait({cum_s}s)_after_refusal",
                        })
                        ref_prev_hash = r_snap.structure_hash
                        refusal_probes.append({
                            "delay_s": cum_s,
                            "top_package": r_snap.top_package,
                            "top_activity": r_snap.top_activity,
                            "hooks": r_snap.trigger_hooks,
                            "overlays": r_snap.overlay_windows,
                            "sample_texts": r_snap.all_texts[:10],
                            "screenshot_path": r_snap.screenshot_path,
                            "harmony_layout_path": r_hm,
                        })
                        if "HOOK_A11Y_SETTINGS" in r_snap.trigger_hooks:
                            outcome = "RELAUNCHED_A11Y_SETTINGS"
                            break
                        elif r_snap.top_package == target_pkg and outcome == "GRACEFUL_STAY_OR_DEGRADE":
                            joined_r = " ".join(r_snap.all_texts).lower()
                            if any(k in joined_r for k in ("accessibility", "无障碍", "enable", "ok", "allow", "continue")) and len(r_snap.elements) <= 8:
                                outcome = "RELAUNCHED_LURE_DIALOG"
                    trace["refusal_probes"] = refusal_probes
                    trace["refusal_outcome"] = outcome
                    print(f"[REFUSAL PROBE RESULT] outcome={outcome}")

                if args.stop_on_a11y_hook and "HOOK_A11Y_SETTINGS" in snap.trigger_hooks:
                    print("[STOP_ON_HOOK] Captured complete Entry -> Hook -> Overlay Probe -> Refusal Probe UTG!")
                    trace["steps"].append({
                        "step": step,
                        "snapshot": snap.to_json_dict(),
                        "harmony_layout_path": hm_path,
                        "model_output": "(stopped automatically upon HOOK_A11Y_SETTINGS + probes)",
                        "action": {"action": "terminate", "status": "success", "summary": "Captured Accessibility Settings hook & probes"},
                    })
                    trace["final_status"] = "hook_captured"
                    break

        # ---- Optional Static-Guided Activity Fallback if UI stalled or near budget end without hook ----
        should_fallback = (
            stagnant_count >= 2
            or (step >= max(4, args.max_steps - 2) and not trace["trigger_events"])
        )
        if (
            args.allow_activity_fallback
            and args.platform == "android"
            and target_pkg
            and should_fallback
            and static_meta.get("candidate_activities")
        ):
            # Prefer non-Main, non-current Activities that look like A11y/Guide/Perm/Web Activities
            cur_act = snap.top_activity or ""
            def _act_prio(a: str):
                al = a.lower()
                return (
                    any(k in al for k in ("access", "a11y", "perm", "guide", "web", "alert", "overlay", "dialog", "grant", "enable")),
                    "main" not in al,
                )
            cands = sorted(
                [a for a in static_meta["candidate_activities"] if a not in tried_fallback_acts and a != cur_act],
                key=_act_prio,
                reverse=True,
            )
            next_act = cands[0] if cands else None
            if next_act:
                tried_fallback_acts.add(next_act)
                print(f"[STATIC FALLBACK] Attempting static-guided Activity launch: {target_pkg}/{next_act}")
                ctrl.run_adb(["shell", "am", "start", "-n", f"{target_pkg}/{next_act}"])
                trace["steps"].append({
                    "step": step,
                    "snapshot": snap.to_json_dict(),
                    "harmony_layout_path": hm_path,
                    "model_output": f"(static_guided_activity_fallback -> {next_act})",
                    "action": {"action": "static_activity_jump", "activity": next_act},
                })
                prev_hash = snap.structure_hash
                prev_action_label = f"am_start({next_act.rsplit('.', 1)[-1]})"
                prev_edge_type = "static_guided_activity_jump"
                stagnant_count = 0
                time.sleep(2.0)
                continue

        # ---- Query Local Model via GUI-Owl / Mobile-Agent-v3.5 Protocol ----
        parsed_call: Optional[dict[str, Any]] = None
        model_text = ""
        hint = ""
        if stagnant_count >= 1:
            hint = "NOTE: The previous action did not change the screen. Pick a DIFFERENT button/tab or navigate Back."
        for attempt in range(1, 4):
            msgs = build_step_messages(args.mode, args.instruction, static_guidance, snap, history_lines, extra_hint=hint)
            resp = client.chat.completions.create(
                model=ep.model,
                messages=msgs,
                temperature=0.0,
                max_tokens=2048,
            )
            msg = resp.choices[0].message
            model_text = (msg.content or "").strip()
            try:
                parsed_call = _parse_tool_call(model_text)
                break
            except Exception as e:
                print(f"[WARN] Parse attempt {attempt}/3 failed: {e}")
                hint = (
                    "Your previous output could not be parsed. Output strictly:\n"
                    "Action: <one sentence>\n"
                    '<tool_call>\n{"name": "mobile_use", "arguments": {"action": "..."}}\n</tool_call>'
                )

        if parsed_call is None:
            print("[ERROR] Failed to parse model tool_call after 3 attempts.")
            trace["final_status"] = "parse_error"
            break

        action_args = _resolve_pixel_coords(parsed_call["arguments"], snap, mode=args.mode)
        action_type = action_args["action"]
        action_line = model_text.split(TOOL_CALL_OPEN)[0].strip().replace("\n", " ")
        print(f"[AGENT] {action_line}")
        print(f"[EXEC]  {json.dumps(action_args, ensure_ascii=False)}")

        anno_path = run_dir / f"{step_tag}_action.png"
        _annotate_action(Path(snap.screenshot_path), action_args, anno_path)

        trace["steps"].append({
            "step": step,
            "snapshot": snap.to_json_dict(),
            "harmony_layout_path": hm_path,
            "model_output": model_text,
            "action": action_args,
            "action_anno_path": str(anno_path),
        })

        # Execute action
        prev_edge_type = f"ui_{action_type}"
        if action_type == "click" and "pixel_xy" in action_args:
            ctrl.tap(action_args["pixel_xy"][0], action_args["pixel_xy"][1])
        elif action_type == "long_press" and "pixel_xy" in action_args:
            dur = int(float(action_args.get("time", 0.8)) * 1000)
            ctrl.long_press(action_args["pixel_xy"][0], action_args["pixel_xy"][1], dur)
        elif action_type in ("swipe", "scroll") and "pixel_xy" in action_args and "pixel_xy2" in action_args:
            ctrl.swipe(
                action_args["pixel_xy"][0], action_args["pixel_xy"][1],
                action_args["pixel_xy2"][0], action_args["pixel_xy2"][1],
            )
        elif action_type == "type":
            ctrl.type_text(str(action_args.get("text", "")))
        elif action_type == "system_button":
            btn = str(action_args.get("button", "")).lower()
            if btn == "back":
                ctrl.back()
            elif btn == "home":
                ctrl.home()
            elif btn == "enter" and args.platform == "android":
                ctrl.keyevent(66)
        elif action_type == "open" and args.platform == "android":
            pkg = action_args.get("package") or action_args.get("text") or target_pkg
            if pkg:
                ctrl.open_app(str(pkg))
        elif action_type == "wait":
            time.sleep(min(8.0, float(action_args.get("time", 2.0))))
        elif action_type in ("terminate", "answer"):
            trace["final_status"] = str(action_args.get("status", "success"))
            print(f"[DONE] status={trace['final_status']} summary={action_args.get('summary') or action_args.get('text', '')}")
            break
        else:
            print(f"[WARN] Unsupported or incomplete action: {action_args}")

        prev_hash = snap.structure_hash
        prev_action_label = f"{action_type}({action_args.get('matched_element') or action_args.get('pixel_xy') or action_args.get('button') or ''})"
        history_lines.append(f"Step {step}: {action_line} | {prev_action_label}")
        time.sleep(args.step_delay)

    trace["finished_at"] = datetime.now().isoformat(timespec="seconds")
    trace_path = run_dir / "utg_trace.json"
    trace_path.write_text(json.dumps(trace, indent=2, ensure_ascii=False), encoding="utf-8")
    hm_utg_path, mmd_path = _export_utg_harmony_and_mermaid(run_dir, trace)
    summary_path = _write_run_summary(run_dir, trace)

    if args.uninstall_after and target_pkg and args.platform == "android":
        print(f"[CLEANUP] Uninstalling {target_pkg} ...")
        ctrl.uninstall_package(target_pkg)
    if args.offline and args.platform == "android":
        ctrl.set_offline(False)

    print(f"\n[SAVED] Harmony UTG : {hm_utg_path}")
    print(f"[SAVED] Mermaid UTG : {mmd_path}")
    print(f"[SAVED] Summary     : {summary_path}")
    return run_dir, trace


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Static-Guided Local-Model GUI-Owl + HarmonyOS UTG Builder")
    p.add_argument("--platform", choices=("android", "harmonyos"), default="android")
    p.add_argument("--adb-path", "--adb_path", dest="adb_path", default=DEFAULT_ADB_PATH)
    p.add_argument("--hdc-path", "--hdc_path", dest="hdc_path", default=DEFAULT_HDC_PATH)
    p.add_argument("--device", default=None, help="ADB serial or HDC target (auto-selects single connected device if omitted)")
    p.add_argument("--model", default=None, help="Model name (defaults to LLM_MODEL / OPENAI_MODEL env var)")
    p.add_argument("--base-url", "--base_url", dest="base_url", default=None, help="OpenAI-compatible base URL (or LLM_BASE_URL)")
    p.add_argument("--api-key", "--api_key", dest="api_key", default=None, help="API key (or LLM_API_KEY / OPENAI_API_KEY)")
    p.add_argument("--mode", choices=("hybrid", "vision_only", "layout_only"), default="hybrid")
    p.add_argument("--apk", default=None)
    p.add_argument("--package", default=None)
    p.add_argument("--static_json", default=None, help="Path to APKAudit static JSON for static-guided exploration")
    p.add_argument("--instruction", default="Follow the app's flow (using the static analysis guidance) from launch until it triggers the Accessibility Service prompt and navigates to System Accessibility Settings. Do NOT toggle a malicious service ON.")
    p.add_argument("--max_steps", type=int, default=10)
    p.add_argument("--step_delay", type=float, default=1.5)
    p.add_argument("--stop_on_a11y_hook", action="store_true", default=True)
    p.add_argument("--no_stop_on_a11y_hook", dest="stop_on_a11y_hook", action="store_false")
    p.add_argument("--probe_refusal", action="store_true", default=True)
    p.add_argument("--no_probe_refusal", dest="probe_refusal", action="store_false")
    p.add_argument("--capture_service_detail", action="store_true", default=True)
    p.add_argument("--no_capture_service_detail", dest="capture_service_detail", action="store_false")
    p.add_argument("--clean_sandbox", action="store_true", default=True)
    p.add_argument("--no_clean_sandbox", dest="clean_sandbox", action="store_false")
    p.add_argument("--allow_activity_fallback", action="store_true", default=False)
    p.add_argument("--map_system_settings", action="store_true", default=True)
    p.add_argument("--offline", action="store_true")
    p.add_argument("--uninstall_after", action="store_true")
    p.add_argument("--tag", default="")
    p.add_argument("--output_dir", default=str(SCRIPT_DIR / "runs"))
    return p.parse_args(argv)


if __name__ == "__main__":
    run_agent(parse_args())
