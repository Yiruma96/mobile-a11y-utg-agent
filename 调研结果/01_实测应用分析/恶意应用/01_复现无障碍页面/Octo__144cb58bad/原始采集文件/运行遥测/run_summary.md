# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:28:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.standhave03`（静态标签：`malicious` / `Octo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `5` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.standhave03/com.standhave03.p069f` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Google Play' / Set switch ON`
- **Back 后 +5.5s**：`com.standhave03/com.standhave03.p069f` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Google Play' / Set switch ON`
- **Back 后 +10.5s**：`com.standhave03/com.standhave03.p069f` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Google Play' / Set switch ON`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 185 / 否 | `click` → [3] Button text="Deny" id=button2 (click) center=(711,1 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 185 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.standhave03` / `p069f` | `-` | 1 | 0 / 是 | `click` → [628, 692] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 210 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing Google Play to always run in the background ma` | `Deny` | `Allow`
- **Step 2 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing Google Play to always run in the background ma` | `Deny` | `Allow`
- **Step 3 (`com.standhave03/p069f`)**: (空文本)
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Play` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以“Google Play”名义请求电池优化后台常驻，随后在应用内引导跳转系统无障碍设置，并在服务详情页用“保护设备”等话术诱导开启无障碍；用户拒权返回后立即重新拉起同一诱导弹窗，形成循环诱导。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语：Let app always run in background? / Allowing Google Play to always run in the background may reduce battery life. -> “让应用始终在后台运行？”并称允许“Google Play”后台常驻可能降低续航，可稍后在设置更改（电池优化弹窗）。
- 英语：Enable Accessibility Service / Find 'Google Play' / Set switch ON / Open Settings -> 启用无障碍服务：找到“Google Play”并把开关打开，点“打开设置”（应用内诱导页）。
- 英语：Use Google Play / Google Play shortcut / Hold volume keys / Enable this service to protect your device. -> 使用 Google Play、Google Play 快捷方式、按住音量键，启用此服务以保护设备（服务详情页）。
- 英语：String (Enable service) / String (Google Play) -> 通知横幅显示“启用服务”/“Google Play”占位字符串，疑为伪装或占位话术（通知栏）。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 系统电池优化弹窗，英文询问是否让应用后台常驻并称可能耗电；通知栏有应用常驻通知。本步点“Deny”未生效。 | `step_01_action.png` |
| 2 | **Step 2: RequestIgnoreBatteryOptimi** | 同一电池优化弹窗仍在，英文称允许“Google Play”后台运行可能耗电；通知栏常驻启用服务通知。因Deny无效改点Allow。 | `step_02_action.png` |
| 3 | **Step 3: p069f** | 应用内p069f页无可见文本，通知栏常驻“启用服务/Google Play”占位通知；点击坐标跳系统设置，引导开无障碍。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | 系统无障碍列表页，“DOWNLOADED APPS”下“Google Play”显示Off；通知栏仍有应用常驻通知。采集到无障碍设置Hook后自动终止。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留无障碍列表页，无可见文本与遮罩；通知栏常驻“启用服务/Google Play”通知。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面仍为无障碍列表，无文本变化、遮罩为0；应用常驻通知继续显示，未见授权结果。 | `step_04_probe_2000ms_screen.png` |
| 7 | **服务详情页** | 无障碍服务详情页，英文含“Use Google Play”“Google Play shortcut”“Hold volume keys”及“启用服务保护设备”，诱导开启。 | `step_04_service_detail_screen.png` |
| 8 | **系统警告弹窗(点Deny)** | 应用内诱导弹窗/引导页，英文要求启用无障碍服务：找到“Google Play”、把开关打开，并提供“Open Settings”。无遮罩。 | `step_04_system_warning_screen.png` |
| 9 | **拒权返回 +2.0s** | 拒权返回2秒后，应用未退出而是重新弹出同一无障碍诱导页，要求找“Google Play”并开开关；通知栏恢复常驻通知。 | `step_04_refusal_2000ms_screen.png` |
| 10 | **拒权返回 +10.5s** | 拒权返回10.5秒后仍反复展示同一无障碍诱导页，持续要求开启“Google Play”服务；通知栏常驻通知未消失。 | `step_04_refusal_10500ms_screen.png` |
