#!/usr/bin/env python3
"""Unified Android (ADB) and HarmonyOS (HDC) Layout, Window-Stack, and Input Bridge.

Captures:
  1. Lossless screenshots via binary stdout (Windows UTF-8 path safe, no /sdcard issues)
  2. Full live UI Layout Hierarchy:
       - Android:   `uiautomator dump /data/local/tmp/window_dump.xml` (AccessibilityNodeInfo XML)
       - HarmonyOS: `uitest dumpLayout -p /data/local/tmp/layout.json` (ArkUI Inspector JSON)
  3. Live Activity / Window / Overlay stack (`dumpsys window` / `dumpsys activity` or `aa dump`)
  4. Automatic detection of the 2 Accessibility Trigger Hooks:
       - HOOK_A11Y_SETTINGS (entering system Accessibility Settings)
       - HOOK_APP_DETAILS   (entering App Details / Android 13+ Restricted Settings)
  5. Set-of-Mark (SoM) annotated screenshot rendering for pixel-exact hybrid VLM grounding.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from PIL import Image, ImageDraw, ImageFont

DEFAULT_ADB_PATH = os.environ.get("ADB_PATH", "adb")
DEFAULT_HDC_PATH = os.environ.get("HDC_PATH", "hdc")

BOUNDS_RE = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")


@dataclass
class UIElement:
    elem_id: int
    text: str
    content_desc: str
    resource_id: str
    class_name: str
    package: str
    bounds: tuple[int, int, int, int]
    center: tuple[int, int]
    clickable: bool
    checkable: bool
    checked: bool
    scrollable: bool
    enabled: bool
    focusable: bool

    def short_label(self) -> str:
        rid = self.resource_id.split("/")[-1] if "/" in self.resource_id else self.resource_id
        cls = self.class_name.split(".")[-1] if "." in self.class_name else self.class_name
        parts = [f"[{self.elem_id}] {cls}"]
        if self.text:
            parts.append(f'text="{self.text[:80]}"')
        if self.content_desc and self.content_desc != self.text:
            parts.append(f'desc="{self.content_desc[:60]}"')
        if rid:
            parts.append(f"id={rid}")
        flags = []
        if self.clickable:
            flags.append("click")
        if self.checkable:
            flags.append("checked" if self.checked else "unchecked")
        if self.scrollable:
            flags.append("scroll")
        if flags:
            parts.append("(" + ",".join(flags) + ")")
        parts.append(f"center=({self.center[0]},{self.center[1]})")
        return " ".join(parts)


@dataclass
class LayoutSnapshot:
    platform: str
    timestamp: float
    screen_width: int
    screen_height: int
    top_package: str
    top_activity: str
    current_focus: str
    overlay_windows: list[str] = field(default_factory=list)
    trigger_hooks: list[str] = field(default_factory=list)
    elements: list[UIElement] = field(default_factory=list)
    all_texts: list[str] = field(default_factory=list)
    has_webview: bool = False
    has_large_image: bool = False
    text_char_count: int = 0
    needs_ocr_fallback: bool = False
    structure_hash: str = ""
    raw_layout_path: str = ""
    screenshot_path: str = ""
    som_path: str = ""

    def to_compact_prompt_text(self, max_elements: int = 55) -> str:
        lines = [
            f"Screen: {self.screen_width}x{self.screen_height} | "
            f"Package: {self.top_package or 'unknown'} | "
            f"Activity: {self.top_activity or 'unknown'}"
        ]
        if self.trigger_hooks:
            lines.append(f"TRIGGER_HOOKS_ACTIVE: {', '.join(self.trigger_hooks)}")
        if self.overlay_windows:
            lines.append(f"OVERLAY_WINDOWS_DETECTED: {', '.join(self.overlay_windows[:4])}")
        if self.has_webview:
            lines.append("NOTE: Page contains a WebView container.")
        if self.needs_ocr_fallback:
            lines.append("NOTE: Low text density with large image/WebView (rely on visual screenshot).")
        lines.append("Interactive & visible UI elements:")
        for el in self.elements[:max_elements]:
            lines.append("  " + el.short_label())
        if len(self.elements) > max_elements:
            lines.append(f"  ... ({len(self.elements) - max_elements} more elements omitted)")
        return "\n".join(lines)

    def to_json_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["element_count"] = len(self.elements)
        return d


def render_som_overlay(
    screenshot_path: Path,
    elements: list[UIElement],
    out_path: Path,
    max_boxes: int = 50,
) -> Path:
    """Draw clean numbered Set-of-Mark boxes onto a copy of the screenshot."""
    img = Image.open(screenshot_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(next((f for f in ("C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Helvetica.ttc") if Path(f).exists()), ""), 20)
    except Exception:
        font = ImageFont.load_default()

    palette = [
        (220, 38, 38),
        (37, 99, 235),
        (5, 150, 105),
        (147, 51, 234),
        (217, 119, 6),
    ]
    for el in elements[:max_boxes]:
        if not (el.clickable or el.checkable or el.scrollable):
            continue
        x1, y1, x2, y2 = el.bounds
        col = palette[el.elem_id % len(palette)]
        draw.rectangle([x1, y1, x2, y2], outline=col, width=3)
        tag = str(el.elem_id)
        tw = 14 * len(tag) + 10
        th = 24
        tx = max(0, min(img.width - tw, x1))
        ty = max(0, y1 - th if y1 >= th else y1)
        draw.rectangle([tx, ty, tx + tw, ty + th], fill=col)
        draw.text((tx + 5, ty + 2), tag, fill=(255, 255, 255), font=font)

    img.save(out_path)
    return out_path


def detect_trigger_hooks(
    top_package: str,
    top_activity: str,
    all_texts: list[str],
    raw_layout: str = "",
) -> list[str]:
    """Detect whether the current screen matches our 2 Accessibility Trigger Hooks."""
    hooks: list[str] = []
    act_l = (top_activity or "").lower()
    pkg_l = (top_package or "").lower()
    joined = " ".join(all_texts[:60]).lower()
    raw_l = raw_layout[:20000].lower()

    is_settings_pkg = pkg_l in (
        "com.android.settings",
        "com.huawei.hmos.settings",
        "com.ohos.settings",
        "com.miui.securitycenter",
    )

    if is_settings_pkg and (
        "accessibility" in act_l
        or "accessibility" in joined
        or "无障碍" in joined
        or "downloaded apps" in joined
        or "downloaded services" in joined
        or "已下载的应用" in joined
        or "已下载的服务" in joined
        or "use service" in joined
        or "accessibility_settings" in raw_l
    ):
        hooks.append("HOOK_A11Y_SETTINGS")

    if is_settings_pkg and (
        "installedappdetails" in act_l
        or "appinfodashboard" in act_l
        or "allow restricted settings" in joined
        or "允许受限设置" in joined
        or ("app info" in joined and ("uninstall" in joined or "force stop" in joined))
    ):
        hooks.append("HOOK_APP_DETAILS")

    return hooks


class AndroidLayoutController:
    """ADB controller with live AccessibilityNodeInfo XML layout & window-stack capture."""

    def __init__(self, adb_path: str = DEFAULT_ADB_PATH, device: Optional[str] = None):
        self.adb_path = adb_path
        self.device = device
        self.platform = "android"

    def _base_cmd(self) -> list[str]:
        cmd = [self.adb_path]
        if self.device:
            cmd.extend(["-s", self.device])
        return cmd

    def run_adb(self, args: list[str], timeout: int = 20, binary: bool = False):
        cmd = self._base_cmd() + args
        if binary:
            return subprocess.run(cmd, capture_output=True, timeout=timeout)
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )

    def get_screenshot(self, save_path: Path, retries: int = 3) -> tuple[int, int]:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(retries):
            r = self.run_adb(["exec-out", "screencap", "-p"], timeout=20, binary=True)
            if r.returncode == 0 and r.stdout.startswith(b"\x89PNG"):
                save_path.write_bytes(r.stdout)
                with Image.open(save_path) as im:
                    return im.size
            time.sleep(0.4)
        raise RuntimeError(f"Failed to capture screenshot via adb exec-out to {save_path}")

    def dump_layout_xml(self, xml_save_path: Path, retries: int = 2) -> str:
        xml_save_path.parent.mkdir(parents=True, exist_ok=True)
        remote = "/data/local/tmp/gui_owl_dump.xml"
        xml_text = ""
        for _ in range(retries):
            self.run_adb(["shell", "uiautomator", "dump", remote], timeout=15)
            r = self.run_adb(["exec-out", "cat", remote], timeout=15, binary=True)
            if r.returncode == 0 and b"<hierarchy" in r.stdout:
                xml_text = r.stdout.decode("utf-8", errors="replace")
                break
            time.sleep(0.4)
        xml_save_path.write_text(xml_text, encoding="utf-8")
        return xml_text

    def get_window_state(self) -> tuple[str, str, str, list[str]]:
        """Return (top_package, top_activity, current_focus, overlay_windows)."""
        r = self.run_adb(["shell", "dumpsys", "window"], timeout=15)
        out = r.stdout or ""
        current_focus = ""
        focused_app = ""
        overlays: list[str] = []

        for line in out.splitlines():
            s = line.strip()
            if s.startswith("mCurrentFocus="):
                current_focus = s.split("=", 1)[1].strip()
            elif s.startswith("mFocusedApp="):
                focused_app = s.split("=", 1)[1].strip()
            elif any(t in s for t in ("TYPE_APPLICATION_OVERLAY", "TYPE_SYSTEM_ALERT", "TYPE_TOAST", "TYPE_SYSTEM_OVERLAY")):
                overlays.append(s[:140])

        # Parse package/activity from mCurrentFocus or mFocusedApp
        top_pkg, top_act = "", ""
        m = re.search(r"([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.$-]+)", current_focus)
        if not m:
            m = re.search(r"([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.$-]+)", focused_app)
        if m:
            top_pkg, top_act = m.group(1), m.group(2)

        # Deduplicate overlays keeping non-systemui/launcher ones first
        filtered_overlays = []
        for ov in overlays:
            if "NavigationBar" in ov or "StatusBar" in ov or "InputMethod" in ov:
                continue
            if ov not in filtered_overlays:
                filtered_overlays.append(ov)
        return top_pkg, top_act, current_focus, filtered_overlays

    def parse_xml_elements(
        self, xml_text: str, screen_w: int, screen_h: int
    ) -> tuple[list[UIElement], list[str], bool, bool]:
        if not xml_text or "<hierarchy" not in xml_text:
            return [], [], False, False
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return [], [], False, False

        elements: list[UIElement] = []
        all_texts: list[str] = []
        has_webview = False
        has_large_image = False
        screen_area = max(1, screen_w * screen_h)
        seen_keys: set[tuple[str, str, tuple[int, int, int, int]]] = set()

        for node in root.iter("node"):
            cls = node.attrib.get("class", "")
            text = (node.attrib.get("text") or "").strip()
            desc = (node.attrib.get("content-desc") or "").strip()
            rid = (node.attrib.get("resource-id") or "").strip()
            pkg = (node.attrib.get("package") or "").strip()
            clickable = node.attrib.get("clickable") == "true"
            checkable = node.attrib.get("checkable") == "true"
            checked = node.attrib.get("checked") == "true"
            scrollable = node.attrib.get("scrollable") == "true"
            enabled = node.attrib.get("enabled") != "false"
            focusable = node.attrib.get("focusable") == "true"
            b_str = node.attrib.get("bounds", "")

            if "WebView" in cls:
                has_webview = True

            m = BOUNDS_RE.match(b_str)
            if not m:
                continue
            x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
            w, h = x2 - x1, y2 - y1
            if w <= 2 or h <= 2:
                continue

            if ("ImageView" in cls or "SurfaceView" in cls) and (w * h) / screen_area >= 0.18:
                has_large_image = True

            if text and text not in all_texts:
                all_texts.append(text)
            if desc and desc not in all_texts:
                all_texts.append(desc)

            # Keep interactive nodes OR informative text nodes (skip pure anonymous layout containers)
            is_interactive = clickable or checkable or scrollable
            is_informative = bool(text or desc)
            if not (is_interactive or is_informative):
                continue

            # Skip system status/nav bar clutter unless clickable
            if pkg == "com.android.systemui" and not is_interactive:
                continue

            dedup_key = (text, desc, (x1, y1, x2, y2))
            if dedup_key in seen_keys:
                continue
            seen_keys.add(dedup_key)

            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            elements.append(
                UIElement(
                    elem_id=len(elements) + 1,
                    text=text,
                    content_desc=desc,
                    resource_id=rid,
                    class_name=cls,
                    package=pkg,
                    bounds=(x1, y1, x2, y2),
                    center=(cx, cy),
                    clickable=clickable,
                    checkable=checkable,
                    checked=checked,
                    scrollable=scrollable,
                    enabled=enabled,
                    focusable=focusable,
                )
            )

        return elements, all_texts, has_webview, has_large_image

    def capture_window_telemetry(self, save_path: Path) -> dict[str, Any]:
        """Losslessly capture all visible windows + active notification banners for later pruning/ablation."""
        rw = self.run_adb(["shell", "dumpsys", "window", "windows"], timeout=12)
        windows_raw: list[dict[str, str]] = []
        cur_win: dict[str, str] = {}
        for line in (rw.stdout or "").splitlines():
            s = line.strip()
            if s.startswith("Window #"):
                if cur_win:
                    windows_raw.append(cur_win)
                cur_win = {"header": s}
            elif cur_win:
                if s.startswith("mOwnerUid=") or s.startswith("mHasSurface=") or s.startswith("ty=") or s.startswith("mAttrs="):
                    k = s.split("=", 1)[0]
                    cur_win[k] = s[:220]
        if cur_win:
            windows_raw.append(cur_win)

        # Capture active posted notification titles/texts (catches Hook/Ermac/Hydra/Coper heads-up banners!)
        rn = self.run_adb(["shell", "dumpsys", "notification", "--noredact"], timeout=12)
        notifs: list[dict[str, str]] = []
        cur_pkg = ""
        cur_title = ""
        cur_text = ""
        for line in (rn.stdout or "").splitlines():
            s = line.strip()
            if s.startswith("NotificationRecord("):
                if cur_pkg and (cur_title or cur_text):
                    notifs.append({"package": cur_pkg, "title": cur_title[:160], "text": cur_text[:240]})
                m = re.search(r"pkg=([^\s]+)", s)
                cur_pkg = m.group(1) if m else ""
                cur_title, cur_text = "", ""
            elif "android.title=" in s:
                cur_title = s.split("android.title=", 1)[1].strip()
            elif "android.text=" in s:
                cur_text = s.split("android.text=", 1)[1].strip()
        if cur_pkg and (cur_title or cur_text):
            notifs.append({"package": cur_pkg, "title": cur_title[:160], "text": cur_text[:240]})

        data = {
            "timestamp": time.time(),
            "visible_windows": [w for w in windows_raw if "mHasSurface=true" in w.get("mHasSurface", "") or "ty=" in w.get("ty", "")][:30],
            "active_notifications": [n for n in notifs if n["package"] not in ("android", "com.android.systemui")][:15],
        }
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return data

    def capture_snapshot(self, out_dir: Path, step_tag: str, draw_som: bool = True) -> LayoutSnapshot:
        out_dir.mkdir(parents=True, exist_ok=True)
        screen_path = out_dir / f"{step_tag}_screen.png"
        xml_path = out_dir / f"{step_tag}_layout.xml"
        som_path = out_dir / f"{step_tag}_som.png"
        win_path = out_dir / f"{step_tag}_windows.json"

        # Dump XML FIRST (waits for Android UI idle), THEN capture screenshot + full window/notification telemetry
        # so delayed popups (e.g. EventBot) never appear in XML while missing in screenshot, and zero signals are lost!
        xml_text = self.dump_layout_xml(xml_path)
        w, h = self.get_screenshot(screen_path)
        top_pkg, top_act, cur_focus, overlays = self.get_window_state()
        self.capture_window_telemetry(win_path)
        elements, all_texts, has_webview, has_large_image = self.parse_xml_elements(xml_text, w, h)

        if not top_pkg and elements:
            top_pkg = elements[0].package

        hooks = detect_trigger_hooks(top_pkg, top_act, all_texts, xml_text)
        text_chars = sum(len(t) for t in all_texts)
        needs_ocr = (text_chars < 25) and (has_large_image or has_webview)

        sig_src = f"{top_pkg}|{top_act}|" + "|".join(all_texts[:20])
        struct_hash = hashlib.sha1(sig_src.encode("utf-8", errors="ignore")).hexdigest()[:12]

        if draw_som:
            render_som_overlay(screen_path, elements, som_path)

        return LayoutSnapshot(
            platform=self.platform,
            timestamp=time.time(),
            screen_width=w,
            screen_height=h,
            top_package=top_pkg,
            top_activity=top_act,
            current_focus=cur_focus,
            overlay_windows=overlays,
            trigger_hooks=hooks,
            elements=elements,
            all_texts=all_texts,
            has_webview=has_webview,
            has_large_image=has_large_image,
            text_char_count=text_chars,
            needs_ocr_fallback=needs_ocr,
            structure_hash=struct_hash,
            raw_layout_path=str(xml_path),
            screenshot_path=str(screen_path),
            som_path=str(som_path) if draw_som else "",
        )

    # ---- Input actions ----
    def tap(self, x: int, y: int) -> None:
        self.run_adb(["shell", "input", "tap", str(int(x)), str(int(y))])

    def long_press(self, x: int, y: int, duration_ms: int = 800) -> None:
        self.run_adb(["shell", "input", "swipe", str(int(x)), str(int(y)), str(int(x)), str(int(y)), str(int(duration_ms))])

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 500) -> None:
        self.run_adb(["shell", "input", "swipe", str(int(x1)), str(int(y1)), str(int(x2)), str(int(y2)), str(int(duration_ms))])

    def type_text(self, text: str) -> None:
        # ASCII fast path via `input text`, escaping spaces as %s
        safe = text.replace(" ", "%s").replace("&", r"\&").replace('"', r'\"')
        self.run_adb(["shell", "input", "text", safe])

    def keyevent(self, key: str | int) -> None:
        self.run_adb(["shell", "input", "keyevent", str(key)])

    def back(self) -> None:
        self.keyevent(4)

    def home(self) -> None:
        self.run_adb(["shell", "am", "start", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.HOME"])

    def open_app(self, package_name: str) -> None:
        # Prefer exact resolved LAUNCHER activity via `cmd package resolve-activity`, fallback to monkey
        r = self.run_adb(["shell", "cmd", "package", "resolve-activity", "--brief", package_name], timeout=10)
        comp = ""
        for line in (r.stdout or "").splitlines():
            s = line.strip()
            if "/" in s and not s.startswith("priority="):
                comp = s
        if comp:
            self.run_adb(["shell", "am", "start", "-W", "-n", comp], timeout=15)
        else:
            self.run_adb(["shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"], timeout=15)

    def wipe_all_third_party_apps(self) -> list[str]:
        """Uninstall ALL 3rd-party packages & reset Settings task stack to guarantee zero cross-app residue."""
        pkgs = self.list_third_party_packages()
        wiped = []
        for p in pkgs:
            self.force_stop(p)
            self.uninstall_package(p)
            wiped.append(p)
        self.force_stop("com.android.settings")
        self.home()
        return wiped

    def get_package_activities(self, package_name: str) -> list[str]:
        """Extract all declared Activity component names for `package_name` via dumpsys package."""
        r = self.run_adb(["shell", "dumpsys", "package", package_name], timeout=15)
        acts: list[str] = []
        pat = re.compile(rf"\b({re.escape(package_name)}/[a-zA-Z0-9_.$-]+)")
        for m in pat.finditer(r.stdout or ""):
            c = m.group(1)
            if c not in acts:
                acts.append(c)
        return acts

    def force_stop(self, package_name: str) -> None:
        self.run_adb(["shell", "am", "force-stop", package_name])

    def list_third_party_packages(self) -> list[str]:
        r = self.run_adb(["shell", "pm", "list", "packages", "-3"])
        pkgs = []
        for line in (r.stdout or "").splitlines():
            s = line.strip()
            if s.startswith("package:"):
                pkgs.append(s[len("package:"):].strip())
        return sorted(set(pkgs))

    def install_apk(self, apk_path: Path) -> tuple[bool, str]:
        """Install an APK safely even when Windows host path contains CJK characters."""
        # Stream APK directly via `adb exec-in` / temp ASCII staging to bypass Windows ANSI fopen bug in adb.exe
        import shutil, tempfile
        tmp_dir = Path(tempfile.gettempdir()) / "gui_owl_apk_stage"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        staged = tmp_dir / "stage_app.apk"
        shutil.copy2(apk_path, staged)
        try:
            r = self.run_adb(["install", "-r", str(staged)], timeout=90)
            ok = r.returncode == 0 and "Success" in (r.stdout + r.stderr)
            return ok, (r.stdout + "\n" + r.stderr).strip()
        finally:
            try:
                staged.unlink(missing_ok=True)
            except Exception:
                pass

    def uninstall_package(self, package_name: str) -> None:
        self.run_adb(["uninstall", package_name], timeout=30)

    def set_offline(self, offline: bool = True) -> None:
        """Toggle Wi-Fi & mobile data off for safe isolated dynamic malware analysis."""
        val = "disable" if offline else "enable"
        self.run_adb(["shell", "svc", "wifi", val])
        self.run_adb(["shell", "svc", "data", val])


class HarmonyLayoutController:
    """Symmetric HarmonyOS (HDC + uitest dumpLayout) controller using the exact same UTG schema."""

    def __init__(self, hdc_path: str = DEFAULT_HDC_PATH, device: Optional[str] = None):
        self.hdc_path = hdc_path
        self.device = device
        self.platform = "harmonyos"

    def _base_cmd(self) -> list[str]:
        cmd = [self.hdc_path]
        if self.device:
            cmd.extend(["-t", self.device])
        return cmd

    def run_hdc(self, args: list[str], timeout: int = 20):
        return subprocess.run(
            self._base_cmd() + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )

    def get_screenshot(self, save_path: Path) -> tuple[int, int]:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        import shutil, tempfile
        tmp_png = Path(tempfile.gettempdir()) / "hm_screen.png"
        self.run_hdc(["shell", "uitest", "screenCap", "-p", "/data/local/tmp/hm_screen.png"])
        self.run_hdc(["file", "recv", "/data/local/tmp/hm_screen.png", str(tmp_png)])
        shutil.move(str(tmp_png), str(save_path))
        with Image.open(save_path) as im:
            return im.size

    def dump_layout_json(self, json_save_path: Path) -> dict[str, Any]:
        json_save_path.parent.mkdir(parents=True, exist_ok=True)
        import shutil, tempfile
        tmp_json = Path(tempfile.gettempdir()) / "hm_layout.json"
        self.run_hdc(["shell", "uitest", "dumpLayout", "-p", "/data/local/tmp/hm_layout.json"])
        self.run_hdc(["file", "recv", "/data/local/tmp/hm_layout.json", str(tmp_json)])
        shutil.move(str(tmp_json), str(json_save_path))
        return json.loads(json_save_path.read_text(encoding="utf-8", errors="replace"))

    def capture_snapshot(self, out_dir: Path, step_tag: str, draw_som: bool = True) -> LayoutSnapshot:
        out_dir.mkdir(parents=True, exist_ok=True)
        screen_path = out_dir / f"{step_tag}_screen.png"
        json_path = out_dir / f"{step_tag}_layout.json"
        som_path = out_dir / f"{step_tag}_som.png"

        w, h = self.get_screenshot(screen_path)
        tree = self.dump_layout_json(json_path)

        elements: list[UIElement] = []
        all_texts: list[str] = []
        top_pkg = ""
        has_webview = False

        def walk(node: dict[str, Any]):
            nonlocal top_pkg, has_webview
            attrs = node.get("attributes") or {}
            b_str = attrs.get("bounds", "")
            text = (attrs.get("text") or "").strip()
            desc = (attrs.get("description") or "").strip()
            cls = attrs.get("type", "")
            pkg = attrs.get("bundleName", "")
            if pkg and not top_pkg:
                top_pkg = pkg
            if "Web" in cls:
                has_webview = True
            if text and text not in all_texts:
                all_texts.append(text)
            m = BOUNDS_RE.match(b_str)
            if m and (attrs.get("clickable") == "true" or text or desc):
                x1, y1, x2, y2 = map(int, m.groups())
                if x2 - x1 > 2 and y2 - y1 > 2:
                    elements.append(
                        UIElement(
                            elem_id=len(elements) + 1,
                            text=text,
                            content_desc=desc,
                            resource_id=attrs.get("id", ""),
                            class_name=cls,
                            package=pkg,
                            bounds=(x1, y1, x2, y2),
                            center=((x1 + x2) // 2, (y1 + y2) // 2),
                            clickable=attrs.get("clickable") == "true",
                            checkable=attrs.get("checkable") == "true",
                            checked=attrs.get("checked") == "true",
                            scrollable=attrs.get("scrollable") == "true",
                            enabled=attrs.get("enabled") != "false",
                            focusable=attrs.get("focusable") == "true",
                        )
                    )
            for child in node.get("children") or []:
                walk(child)

        walk(tree)
        hooks = detect_trigger_hooks(top_pkg, "", all_texts, json.dumps(tree, ensure_ascii=False)[:15000])
        if draw_som:
            render_som_overlay(screen_path, elements, som_path)
        sig_src = f"{top_pkg}|" + "|".join(all_texts[:20])
        return LayoutSnapshot(
            platform=self.platform,
            timestamp=time.time(),
            screen_width=w,
            screen_height=h,
            top_package=top_pkg,
            top_activity="",
            current_focus=top_pkg,
            trigger_hooks=hooks,
            elements=elements,
            all_texts=all_texts,
            has_webview=has_webview,
            text_char_count=sum(len(t) for t in all_texts),
            structure_hash=hashlib.sha1(sig_src.encode("utf-8")).hexdigest()[:12],
            raw_layout_path=str(json_path),
            screenshot_path=str(screen_path),
            som_path=str(som_path) if draw_som else "",
        )

    def tap(self, x: int, y: int) -> None:
        self.run_hdc(["shell", "uitest", "uiInput", "click", str(int(x)), str(int(y))])

    def long_press(self, x: int, y: int, duration_ms: int = 800) -> None:
        self.run_hdc(["shell", "uitest", "uiInput", "longClick", str(int(x)), str(int(y))])

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 500) -> None:
        self.run_hdc(["shell", "uitest", "uiInput", "swipe", str(int(x1)), str(int(y1)), str(int(x2)), str(int(y2)), "600"])

    def type_text(self, text: str) -> None:
        self.run_hdc(["shell", "uitest", "uiInput", "inputText", "1", "1", text])

    def back(self) -> None:
        self.run_hdc(["shell", "uitest", "uiInput", "keyEvent", "Back"])

    def home(self) -> None:
        self.run_hdc(["shell", "uitest", "uiInput", "keyEvent", "Home"])
