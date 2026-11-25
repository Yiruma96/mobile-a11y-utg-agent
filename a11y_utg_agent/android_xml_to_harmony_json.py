#!/usr/bin/env python3
"""Convert Android `uiautomator dump` XML into OpenHarmony `uitest dumpLayout` JSON.

Schema strictly verified against official OpenHarmony `testfwk_arkxtest` C++ sources:
  - `uitest/core/ui_model.h` (`UiAttr` enum & `ATTR_NAMES[0..34]`)
  - `uitest/core/ui_model.cpp` (`Widget::WrapperWidgetToJson`)
  - `uitest/core/dump_handler.cpp` (`DumpHandler::DFSMarshalWidget`)
  - `uitest/core/ui_driver.cpp` (`UiDriver::DumpUiHierarchy` & `DumpWindowsInfo`)

Output structure matches real `hdc shell uitest dumpLayout -p <path>` output:
  {
    "attributes": { <ATTR_NAMES[0..25]>, "bounds": "[0,0][W,H]" },
    "children": [
      {
        "attributes": {
          <ATTR_NAMES[0..26]>,
          "visible": "true",
          "hashcode": "...",
          "hint": "",
          "abilityName": "...",
          "bundleName": "...",
          "pagePath": "..."
        },
        "children": [ ... ]
      }
    ]
  }
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Optional

# Exact `ATTR_NAMES[0..25]` (before UiAttr::HIERARCHY) from OpenHarmony ui_model.h
ROOT_ATTR_NAMES: tuple[str, ...] = (
    "accessibilityId",
    "id",
    "text",
    "key",
    "description",
    "type",
    "bounds",
    "enabled",
    "focused",
    "selected",
    "clickable",
    "longClickable",
    "scrollable",
    "checkable",
    "checked",
    "hostWindowId",
    "displayId",
    "origBounds",
    "zIndex",
    "opacity",
    "backgroundColor",
    "backgroundImage",
    "blur",
    "hitTestBehavior",
    "clip",
    "originalText",
)

# Exact widget attributes emitted by `Widget::WrapperWidgetToJson`
WIDGET_EXTRA_ATTR_NAMES: tuple[str, ...] = (
    "hierarchy",
    "visible",
    "hashcode",
    "hint",
)

BOUNDS_RE = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")

# Android View class -> ArkUI component `type` mapping
ANDROID_TO_ARKUI_TYPE: dict[str, str] = {
    "android.widget.TextView": "Text",
    "android.widget.Button": "Button",
    "android.widget.ImageButton": "Button",
    "android.widget.ImageView": "Image",
    "android.widget.EditText": "TextInput",
    "android.widget.AutoCompleteTextView": "TextInput",
    "android.widget.Switch": "Toggle",
    "androidx.appcompat.widget.SwitchCompat": "Toggle",
    "com.google.android.material.switchmaterial.SwitchMaterial": "Toggle",
    "android.widget.CheckBox": "Checkbox",
    "android.widget.CheckedTextView": "Checkbox",
    "android.widget.RadioButton": "Radio",
    "android.widget.ToggleButton": "Toggle",
    "android.widget.ProgressBar": "Progress",
    "android.widget.SeekBar": "Slider",
    "android.webkit.WebView": "Web",
    "android.widget.ScrollView": "Scroll",
    "android.widget.HorizontalScrollView": "Scroll",
    "androidx.core.widget.NestedScrollView": "Scroll",
    "android.widget.ListView": "List",
    "androidx.recyclerview.widget.RecyclerView": "List",
    "android.widget.GridView": "Grid",
    "android.widget.LinearLayout": "Column",
    "android.widget.FrameLayout": "Stack",
    "android.widget.RelativeLayout": "RelativeContainer",
    "androidx.constraintlayout.widget.ConstraintLayout": "RelativeContainer",
    "androidx.coordinatorlayout.widget.CoordinatorLayout": "Stack",
    "androidx.drawerlayout.widget.DrawerLayout": "SideBarContainer",
    "android.widget.TableLayout": "Column",
    "android.widget.TableRow": "Row",
    "android.view.ViewGroup": "Flex",
    "android.view.View": "Common",
    "android.widget.TabWidget": "Tabs",
    "android.widget.Toolbar": "Row",
    "androidx.appcompat.widget.Toolbar": "Row",
    "android.widget.Spinner": "Select",
    "android.widget.Toast": "Toast",
}

# Optional mapping for Android Settings -> HarmonyOS Settings bundle/ability names
ANDROID_SETTINGS_TO_HARMONY: dict[str, tuple[str, str, str]] = {
    "com.android.settings": (
        "com.huawei.hmos.settings",
        "com.huawei.hmos.settings.MainAbility",
        "pages/settings",
    ),
}


def map_android_class_to_arkui(cls_name: str, bounds: tuple[int, int, int, int] = (0, 0, 0, 0)) -> str:
    if not cls_name:
        return "Common"
    if cls_name in ANDROID_TO_ARKUI_TYPE:
        mapped = ANDROID_TO_ARKUI_TYPE[cls_name]
        # Heuristic: horizontal wide LinearLayout -> Row, tall -> Column
        if cls_name == "android.widget.LinearLayout":
            w, h = bounds[2] - bounds[0], bounds[3] - bounds[1]
            if w > 0 and h > 0 and w > h * 1.8 and h < 260:
                return "Row"
        return mapped
    short = cls_name.rsplit(".", 1)[-1]
    sl = short.lower()
    if "webview" in sl:
        return "Web"
    if "button" in sl:
        return "Button"
    if "switch" in sl or "toggle" in sl:
        return "Toggle"
    if "checkbox" in sl:
        return "Checkbox"
    if "edittext" in sl or "input" in sl:
        return "TextInput"
    if "text" in sl:
        return "Text"
    if "image" in sl or "icon" in sl:
        return "Image"
    if "recycler" in sl or "listview" in sl:
        return "List"
    if "scroll" in sl:
        return "Scroll"
    if "dialog" in sl:
        return "Dialog"
    if "layout" in sl or "container" in sl:
        return "Column"
    return short


def _parse_bounds(b_str: str) -> tuple[int, int, int, int]:
    m = BOUNDS_RE.match(b_str or "")
    if not m:
        return (0, 0, 0, 0)
    return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))


def _bool_str(val: Optional[str], default: str = "false") -> str:
    if val is None:
        return default
    return "true" if str(val).lower() == "true" else "false"


def _make_hashcode(hierarchy: str, cls_name: str, rid: str, bounds: str) -> str:
    raw = f"{hierarchy}|{cls_name}|{rid}|{bounds}".encode("utf-8", errors="ignore")
    return hashlib.md5(raw).hexdigest()[:12]


def _normalize_bundle_ability(
    package: str,
    activity: str,
    map_system_settings: bool = False,
) -> tuple[str, str, str]:
    pkg = (package or "").strip()
    act = (activity or "").strip()
    short_act = act.rsplit(".", 1)[-1] if act else "MainAbility"
    page_path = f"pages/{short_act}"

    if map_system_settings and pkg in ANDROID_SETTINGS_TO_HARMONY:
        hm_bundle, hm_ability, hm_page = ANDROID_SETTINGS_TO_HARMONY[pkg]
        act_l = act.lower()
        if "accessibility" in act_l:
            return hm_bundle, "AccessibilitySettingsAbility", "pages/accessibility/AccessibilitySettings"
        if "installedappdetails" in act_l or "appinfo" in act_l:
            return hm_bundle, "AppInfoAbility", "pages/appinfo/AppInfoPage"
        return hm_bundle, hm_ability, hm_page

    return pkg, (act or "EntryAbility"), page_path


def android_xml_to_harmony_dict(
    xml_text: str,
    *,
    top_package: str = "",
    top_activity: str = "",
    screen_width: int = 1080,
    screen_height: int = 2280,
    host_window_id: str = "1",
    map_system_settings: bool = False,
    preserve_android_meta: bool = False,
) -> dict[str, Any]:
    """Convert raw Android `uiautomator dump` XML text into OpenHarmony `uitest dumpLayout` JSON."""
    root_attrs: dict[str, str] = {k: "" for k in ROOT_ATTR_NAMES}
    root_attrs["bounds"] = f"[0,0][{screen_width},{screen_height}]"

    if not xml_text or "<hierarchy" not in xml_text:
        return {"attributes": root_attrs, "children": []}

    try:
        xml_root = ET.fromstring(xml_text)
    except ET.ParseError:
        return {"attributes": root_attrs, "children": []}

    # Detect bounding screen size from top nodes if present
    max_r, max_b = screen_width, screen_height
    counter = [1000]

    def convert_node(
        elem: ET.Element,
        hierarchy: str,
        is_window_root: bool,
        win_id: str,
    ) -> dict[str, Any]:
        nonlocal max_r, max_b
        counter[0] += 1
        a11y_id = str(counter[0])

        b_str = elem.attrib.get("bounds") or f"[0,0][{screen_width},{screen_height}]"
        x1, y1, x2, y2 = _parse_bounds(b_str)
        if x2 > max_r:
            max_r = x2
        if y2 > max_b:
            max_b = y2

        cls_name = elem.attrib.get("class") or ""
        pkg = elem.attrib.get("package") or top_package or ""
        rid = elem.attrib.get("resource-id") or ""
        short_id = rid.split("/")[-1] if "/" in rid else rid
        text = elem.attrib.get("text") or ""
        desc = elem.attrib.get("content-desc") or ""
        hint = elem.attrib.get("hint") or ""

        ark_type = "root" if is_window_root else map_android_class_to_arkui(cls_name, (x1, y1, x2, y2))

        attrs: dict[str, str] = {
            "accessibilityId": a11y_id,
            "id": short_id,
            "text": text,
            "key": rid,
            "description": desc,
            "type": ark_type,
            "bounds": f"[{x1},{y1}][{x2},{y2}]",
            "enabled": _bool_str(elem.attrib.get("enabled"), "true"),
            "focused": _bool_str(elem.attrib.get("focused"), "false"),
            "selected": _bool_str(elem.attrib.get("selected"), "false"),
            "clickable": _bool_str(elem.attrib.get("clickable"), "false"),
            "longClickable": _bool_str(elem.attrib.get("long-clickable"), "false"),
            "scrollable": _bool_str(elem.attrib.get("scrollable"), "false"),
            "checkable": _bool_str(elem.attrib.get("checkable"), "false"),
            "checked": _bool_str(elem.attrib.get("checked"), "false"),
            "hostWindowId": win_id,
            "displayId": "0",
            "origBounds": f"[{x1},{y1}][{x2},{y2}]",
            "zIndex": "0",
            "opacity": "1.0",
            "backgroundColor": "",
            "backgroundImage": "",
            "blur": "0.0",
            "hitTestBehavior": "Default",
            "clip": "false",
            "originalText": text,
            "hierarchy": hierarchy,
            "visible": "true",
            "hashcode": _make_hashcode(hierarchy, cls_name, rid, b_str),
            "hint": hint,
        }

        if is_window_root:
            bundle, ability, page_path = _normalize_bundle_ability(
                pkg or top_package,
                top_activity,
                map_system_settings=map_system_settings,
            )
            attrs["abilityName"] = ability
            attrs["bundleName"] = bundle
            attrs["pagePath"] = page_path

        if preserve_android_meta:
            attrs["_androidClass"] = cls_name
            attrs["_androidPackage"] = pkg
            attrs["_androidResourceId"] = rid

        children_out = []
        for idx, child in enumerate(elem.findall("node")):
            child_h = f"{hierarchy},{idx}"
            children_out.append(convert_node(child, child_h, False, win_id))

        return {
            "attributes": attrs,
            "children": children_out,
        }

    top_nodes = xml_root.findall("node")
    window_children = []
    for w_idx, w_node in enumerate(top_nodes):
        wid = str(int(host_window_id) + w_idx)
        window_children.append(convert_node(w_node, "ROOT", True, wid))

    root_attrs["bounds"] = f"[0,0][{max_r},{max_b}]"
    return {
        "attributes": root_attrs,
        "children": window_children,
    }


def convert_xml_file(
    xml_path: Path,
    json_out_path: Path,
    *,
    top_package: str = "",
    top_activity: str = "",
    screen_width: int = 1080,
    screen_height: int = 2280,
    map_system_settings: bool = False,
    preserve_android_meta: bool = False,
) -> dict[str, Any]:
    xml_text = xml_path.read_text(encoding="utf-8", errors="replace")
    hm = android_xml_to_harmony_dict(
        xml_text,
        top_package=top_package,
        top_activity=top_activity,
        screen_width=screen_width,
        screen_height=screen_height,
        map_system_settings=map_system_settings,
        preserve_android_meta=preserve_android_meta,
    )
    json_out_path.parent.mkdir(parents=True, exist_ok=True)
    json_out_path.write_text(json.dumps(hm, indent=2, ensure_ascii=False), encoding="utf-8")
    return hm


def main() -> None:
    p = argparse.ArgumentParser(
        description="Convert Android uiautomator XML -> OpenHarmony uitest dumpLayout JSON"
    )
    p.add_argument("--input", help="Single Android XML file path")
    p.add_argument("--output", help="Output HarmonyOS JSON file path")
    p.add_argument("--input-dir", help="Batch convert all *_layout.xml files under this directory")
    p.add_argument("--package", default="", help="Optional top package / bundleName override")
    p.add_argument("--activity", default="", help="Optional top activity / abilityName override")
    p.add_argument("--map-system-settings", action="store_true",
                   help="Map com.android.settings -> com.huawei.hmos.settings")
    p.add_argument("--preserve-android-meta", action="store_true",
                   help="Include _androidClass/_androidPackage/_androidResourceId fields")
    args = p.parse_args()

    if args.input:
        in_p = Path(args.input)
        out_p = Path(args.output) if args.output else in_p.with_name(in_p.stem + "_harmony.json")
        convert_xml_file(
            in_p, out_p,
            top_package=args.package,
            top_activity=args.activity,
            map_system_settings=args.map_system_settings,
            preserve_android_meta=args.preserve_android_meta,
        )
        print(f"[OK] {in_p} -> {out_p}")
        return

    if args.input_dir:
        root_dir = Path(args.input_dir)
        xmls = sorted(root_dir.rglob("*_layout.xml"))
        for xp in xmls:
            out_p = xp.with_name(xp.stem + "_harmony.json")
            convert_xml_file(
                xp, out_p,
                map_system_settings=args.map_system_settings,
                preserve_android_meta=args.preserve_android_meta,
            )
        print(f"[OK] Batch converted {len(xmls)} XML files under {root_dir}")
        return

    p.print_help()


if __name__ == "__main__":
    main()
