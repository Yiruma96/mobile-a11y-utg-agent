# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:42:59
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.fashlightalerts.vnm`（静态标签：`malicious` / `GhostClicker` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 5 步，UTG 唯一节点 `7` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 5 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_05_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.fashlightalerts.vnm/com.dhama.international.flashalert.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Flash Alerts on Call and SMS / Incoming Call / Sms Service / Notification`
- **Back 后 +5.5s**：`com.fashlightalerts.vnm/com.dhama.international.flashalert.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Flash Alerts on Call and SMS / Incoming Call / Sms Service / Notification`
- **Back 后 +10.5s**：`com.fashlightalerts.vnm/com.dhama.international.flashalert.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Flash Alerts on Call and SMS / Incoming Call / Sms Service / Notification`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 15 | 160 / 否 | `click` → [15] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.fashlightalerts.vnm` / `MainActivity` | `-` | 3 | 149 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.fashlightalerts.vnm` / `MainActivity` | `-` | 9 | 64 / 否 | `click` → [9] ToggleButton id=tglNotification (click,unchecked) c | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.fashlightalerts.vnm` / `MainActivity` | `-` | 4 | 120 / 否 | `click` → [3] Button text="Yes" id=Yes (click) center=(340,1290) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_05_layout.xml` + `step_05_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Flash light alerts to access` | `Camera` | `take pictures and record video` | `SMS` | `send and view SMS messages` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`com.fashlightalerts.vnm/MainActivity`)**: `Flash light alerts` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.fashlightalerts.vnm/MainActivity`)**: `Flash Alerts on Call and SMS` | `Incoming Call` | `Sms Service` | `Notification`
- **Step 4 (`com.fashlightalerts.vnm/MainActivity`)**: `Notification Alert` | `Notification requires accessibility service to be on. d` | `Yes` | `No`
- **Step 5 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Flash light alerts` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先请求相机、短信与电话权限，再以通知功能为由诱导开启无障碍服务；进入系统完全控制警告后若拒绝，仍反复回到主界面并停留，形成被困于诱导页的链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许手电筒提醒访问哪些内容”（权限审查页）
- 英文 -> “此应用为旧版 Android 构建，可能无法正常运行，请检查更新或联系开发者”（主界面旧版警告）
- 英文 -> “通知提醒需要开启无障碍服务，是否启用通知功能？”（通知授权弹窗）
- 英文 -> “是否允许手电筒提醒完全控制你的设备？”（系统警告弹窗）
- 英文 -> “完全控制适用于有无障碍需求的辅助应用，但不适合大多数应用”（系统警告弹窗）
- 英文 -> “可查看并控制屏幕，读取屏幕全部内容并覆盖显示在其他应用上”（系统警告弹窗）
- 英文 -> “可查看并执行操作，追踪与应用的交互或硬件传感器，并代表你操作应用”（系统警告弹窗）
- 英文 -> “未提供描述”（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限审查页，要求选择允许“手电筒提醒”访问相机、短信与电话；点 Continue 同意后进入应用主界面。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 主界面弹出旧版 Android 兼容警告，称应用可能无法正常运行；点 OK 关闭弹窗并返回主界面，尚无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 主界面显示来电、短信与通知开关；点按未勾选的通知开关，触发无障碍授权说明弹窗，尚无通知或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 通知授权说明弹窗，称通知提醒需开启无障碍服务并询问是否启用；点 Yes 将跳转系统无障碍设置页。 | `step_04_action.png` |
| 5 | **Step 5: [无障碍列表页]** | 系统无障碍列表页，下载应用区显示“手电筒提醒”为关闭状态；探针在此捕获无障碍设置钩子并自动终止。 | `step_05_screen.png` |
| 6 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍停留在系统无障碍列表页；页面文本为空，未见通知横幅或悬浮遮罩。 | `step_05_probe_800ms_screen.png` |
| 7 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针，仍为系统无障碍列表页且无新文本；未出现通知横幅或悬浮遮罩。 | `step_05_probe_2000ms_screen.png` |
| 8 | **服务详情页** | 服务详情页，显示“手电筒提醒”的使用开关、快捷方式与音量键选项；说明为未提供描述，未见遮罩。 | `step_05_service_detail_screen.png` |
| 9 | **系统警告弹窗(点Deny)** | 系统完全控制警告弹窗，称可查看并控制屏幕、代执行操作；本步检查后点 Deny 拒绝，弹窗无额外遮罩。 | `step_05_system_warning_screen.png` |
| 10 | **拒权返回 +2.0s** | 拒绝无障碍后 2.0 秒回到应用主界面，仍显示来电、短信、通知开关；无通知或遮罩，流程被困于诱导主屏。 | `step_05_refusal_2000ms_screen.png` |
| 11 | **拒权返回 +10.5s** | 拒绝后 10.5 秒仍停在应用主界面，无进一步跳转或弹窗；未出现通知横幅或遮罩，确认被困于诱导页。 | `step_05_refusal_10500ms_screen.png` |
