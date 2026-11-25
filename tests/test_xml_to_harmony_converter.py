#!/usr/bin/env python3
"""Unit test verifying Android uiautomator XML -> OpenHarmony uitest dumpLayout JSON conversion."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from a11y_utg_agent.android_xml_to_harmony_json import (
    ROOT_ATTR_NAMES,
    WIDGET_EXTRA_ATTR_NAMES,
    android_xml_to_harmony_dict,
)

SAMPLE_XML = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<hierarchy rotation="0">
  <node index="0" text="" resource-id="" class="android.widget.FrameLayout" package="com.android.settings"
        content-desc="" checkable="false" checked="false" clickable="false" enabled="true"
        focusable="false" focused="false" scrollable="false" long-clickable="false" password="false"
        selected="false" bounds="[0,0][1080,2280]">
    <node index="0" text="Accessibility" resource-id="com.android.settings:id/title"
          class="android.widget.TextView" package="com.android.settings" content-desc=""
          checkable="false" checked="false" clickable="false" enabled="true" focusable="false"
          focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
          bounds="[198,106][504,180]" />
    <node index="1" text="Use Flash Update" resource-id="android:id/switch_widget"
          class="android.widget.Switch" package="com.android.settings" content-desc="Toggle service"
          checkable="true" checked="false" clickable="true" enabled="true" focusable="true"
          focused="false" scrollable="false" long-clickable="false" password="false" selected="false"
          bounds="[48,280][1032,420]" />
  </node>
</hierarchy>
"""


def test_openharmony_uitest_schema_compliance() -> None:
    out = android_xml_to_harmony_dict(
        SAMPLE_XML,
        top_package="com.android.settings",
        top_activity="com.android.settings.Settings$AccessibilitySettingsActivity",
        map_system_settings=True,
    )
    assert set(out["attributes"].keys()) == set(ROOT_ATTR_NAMES)
    assert out["attributes"]["bounds"] == "[0,0][1080,2280]"
    assert len(out["children"]) == 1

    win = out["children"][0]
    w_attrs = win["attributes"]
    for k in list(ROOT_ATTR_NAMES) + list(WIDGET_EXTRA_ATTR_NAMES) + ["abilityName", "bundleName", "pagePath"]:
        assert k in w_attrs, f"Missing OpenHarmony uitest key: {k}"
    assert w_attrs["bundleName"] == "com.huawei.hmos.settings"
    assert w_attrs["abilityName"] == "AccessibilitySettingsAbility"
    assert w_attrs["type"] == "root"

    title_node, toggle_node = win["children"]
    assert title_node["attributes"]["type"] == "Text"
    assert title_node["attributes"]["text"] == "Accessibility"
    assert title_node["attributes"]["hierarchy"] == "ROOT,0"

    assert toggle_node["attributes"]["type"] == "Toggle"
    assert toggle_node["attributes"]["checkable"] == "true"
    assert toggle_node["attributes"]["clickable"] == "true"
    assert toggle_node["attributes"]["description"] == "Toggle service"
    assert toggle_node["attributes"]["id"] == "switch_widget"
    assert toggle_node["attributes"]["hierarchy"] == "ROOT,1"


if __name__ == "__main__":
    test_openharmony_uitest_schema_compliance()
    print("[PASS] OpenHarmony uitest dumpLayout JSON schema test passed!")
