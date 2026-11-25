# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:13:46
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.castle.sefirah`（静态标签：`benign` / `远程协助与跨设备互联` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 8 步，UTG 唯一节点 `9` 个，有向边 `12` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 6 | `HOOK_APP_DETAILS` | `com.android.settings/com.android.settings.applications.InstalledAppDetails` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_06_layout_harmony.json` |
| Step 8 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_08_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.castle.sefirah/com.castle.sefirah.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Contacts permission / To sync and lookup contacts / Grant / Messages permission / To send and read messages`
- **Back 后 +5.5s**：`com.castle.sefirah/com.castle.sefirah.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Contacts permission / To sync and lookup contacts / Grant / Messages permission / To send and read messages`
- **Back 后 +10.5s**：`com.castle.sefirah/com.castle.sefirah.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Contacts permission / To sync and lookup contacts / Grant / Messages permission / To send and read messages`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.castle.sefirah` / `MainActivity` | `-` | 9 | 153 / 否 | `click` → [9] TextView text="Next" center=(917,2082) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.castle.sefirah` / `MainActivity` | `-` | 8 | 179 / 否 | `click` → [7] View (click) center=(917,2082) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.castle.sefirah` / `MainActivity` | `-` | 34 | 486 / 否 | `swipe` → [540, 1800] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.castle.sefirah` / `MainActivity` | `-` | 37 | 461 / 否 | `click` → [34] View (click) center=(911,1829) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.castle.sefirah` / `MainActivity` | `-` | 8 | 348 / 否 | `click` → [3] View (click) center=(299,1368) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `InstalledAppDetails` | `HOOK_APP_DETAILS` | 22 | 261 / 否 | `system_button` → Back | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.castle.sefirah` / `MainActivity` | `-` | 8 | 348 / 否 | `click` → [6] TextView text="Accessibility Service" center=(673,1 | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 206 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.castle.sefirah/MainActivity`)**: `Welcome` | `Let's get you started. First, install the companion app` | `Windows` | `Linux` | `Next`
- **Step 2 (`com.castle.sefirah/MainActivity`)**: `Choose Storage Location` | `Select a folder where the app will store received files` | `Selected folder: /storage/emulated/0/Downloads` | `Select a folder` | `Next`
- **Step 3 (`com.castle.sefirah/MainActivity`)**: `Permissions` | `Background Battery Usage` | `Allow the app to maintain stable connections by disabli` | `Grant` | `Optional` | `Notification Access` | `To read, dismiss, and trigger actions from notification` | `Contacts permission` | `To sync and lookup contacts` | `Messages permission`
- **Step 4 (`com.castle.sefirah/MainActivity`)**: `Contacts permission` | `To sync and lookup contacts` | `Grant` | `Messages permission` | `To send and read messages` | `Phone permission` | `To get phone number and notify about incoming calls` | `Call logs permission` | `To sync recent call history` | `Storage Access`
- **Step 5 (`com.castle.sefirah/MainActivity`)**: `Restricted settings` | `Due to security restrictions, you'll need to:   1. Try ` | `App info` | `Accessibility Service` | `Cancel`
- **Step 6 (`com.android.settings/InstalledAppDetails`)**: `Back` | `App info` | `Search settings` | `Sefirah` | `Open` | `Uninstall` | `Force stop` | `Notifications` | `~1 notification per week` | `Permissions`
- **Step 7 (`com.castle.sefirah/MainActivity`)**: `Restricted settings` | `Due to security restrictions, you'll need to:   1. Try ` | `App info` | `Accessibility Service` | `Cancel`
- **Step 8 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Sefirah` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | Step 1: MainActivity（MainActivity）：Welcome / Let's get you started. First, ；动作 click | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | Step 2: MainActivity（MainActivity）：Choose Storage Location / Select a folde；动作 click | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | Step 3: MainActivity（MainActivity）：Permissions / Background Battery Usage /；动作 swipe | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | Step 4: MainActivity（MainActivity）：Contacts permission / To sync and lookup；动作 click | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | Step 5: MainActivity（MainActivity）：Restricted settings / Due to security re；动作 click | `step_05_action.png` |
| 6 | **Step 6: [无障碍列表页]** | Step 6: [无障碍列表页]（InstalledAppDetails）：Back / App info / Search settings；动作 system_button | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | Step 7: MainActivity（MainActivity）：Restricted settings / Due to security re；动作 click | `step_07_action.png` |
| 8 | **Step 8: [无障碍列表页]** | Step 8: [无障碍列表页]（Settings$AccessibilitySettingsActivity）：Back / Accessibility / Search settings；动作 terminate | `step_08_screen.png` |
| 9 | **跳后探针 +0.8s** | 跳后探针 +0.8s（InstalledAppDetails）：无文本；动作 wait(0.8s) | `step_06_probe_800ms_screen.png` |
| 10 | **跳后探针 +2.0s** | 跳后探针 +2.0s（InstalledAppDetails）：无文本；动作 wait(2.0s) | `step_06_probe_2000ms_screen.png` |
| 11 | **跳后探针 +0.8s** | 跳后探针 +0.8s（InstalledAppDetails）：无文本；动作 wait(0.8s) | `step_08_probe_800ms_screen.png` |
| 12 | **跳后探针 +2.0s** | 跳后探针 +2.0s（InstalledAppDetails）：无文本；动作 wait(2.0s) | `step_08_probe_2000ms_screen.png` |
| 13 | **服务详情页** | 服务详情页（SubSettings）：Back / Sefirah / Use Sefirah；动作 inspect_detail_or_warning | `step_08_service_detail_screen.png` |
| 14 | **系统警告弹窗(点Deny)** | 系统警告弹窗(点Deny)（SubSettings）：Allow Sefirah to have full control of yo；动作 inspect_detail_or_warning | `step_08_system_warning_screen.png` |
| 15 | **拒权返回 +2.0s** | 拒权返回 +2.0s（MainActivity）：Contacts permission / To sync and lookup；动作 Back_refuse -> TRAPPED_ON_LURE_SCREEN | `step_08_refusal_2000ms_screen.png` |
| 16 | **拒权返回 +10.5s** | 拒权返回 +10.5s（MainActivity）：Contacts permission / To sync and lookup；动作 Back_refuse -> TRAPPED_ON_LURE_SCREEN | `step_08_refusal_10500ms_screen.png` |
