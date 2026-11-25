# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:33:38
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.system.android.updater`（静态标签：`malicious` / `SpyAgent` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 311 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 150 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `wait` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Google Play Service to access` | `SMS` | `send and view SMS messages` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `Phone`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Google Play Service` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Google Play Service”名义，先在系统权限页诱导一次性授予短信、通讯录、通话记录、电话、麦克风、位置等敏感权限；随后隐藏图标退居后台，并通过兼容性弹窗和多个混淆组件（含 PhonecallReceiver）静默维持或拉起，呈现典型 SpyAgent 窃取链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 Google Play 服务访问的内容”（Step 1 系统权限页标题）
- 英文 -> “发送和查看短信”“访问通讯录”“读写通话记录”“拨打电话和管理通话”“录制音频”“定位”等权限说明（Step 1 权限列表）
- 英文 -> “此应用针对旧版 Android 构建，可能无法正常工作。请检查更新或联系开发者。”（Step 2 兼容性弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限页以“Google Play 服务”名义索取短信、通讯录、通话记录、电话、麦克风、定位等权限；点击 Continue 继续整体授权。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面弹出兼容性警告，称“Google Play 服务”为旧版 Android 构建、可能异常；点击 OK 关闭弹窗，继续后续组件探针。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面，显示应用列表、天气与常用图标；应用未主动弹出辅助功能页，仅短暂等待观察后台服务是否拉起设置，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在桌面，应用已隐藏启动图标并退居后台；探针按包名重新拉起应用以继续流程，界面无可见恶意弹窗或通知。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面无变化，流程以静态引导跳转至混淆组件 .four.fourre；未见新界面、通知或遮罩，属于后台/隐藏组件探针。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面保持原样，静态跳转至 .seven.PhonecallReceiver；该组件名指向通话监听，但本页未显示可见界面，也无通知横幅。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍停留在桌面，继续静态跳转至混淆组件 .five.fivere；无可见页面、通知或悬浮遮罩，疑似后台功能入口探针。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面无可见变化，最后跳转至 .twenty.twenty 混淆组件；未出现新界面或通知，显示应用以隐藏组件维持后台行为。 | `step_08_screen.png` |
