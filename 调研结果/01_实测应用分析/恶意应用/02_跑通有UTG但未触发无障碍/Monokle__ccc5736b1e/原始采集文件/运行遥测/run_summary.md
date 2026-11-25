# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:27:08
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.flashlight.ultra.gps.logger`（静态标签：`malicious` / `Monokle` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 37 | 336 / 否 | `click` → [37] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 147 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Ultra GPS Logger to access` | `Files and media` | `access photos, media, and files on your device` | `Location` | `access this device's location` | `Contacts` | `access your contacts` | `Phone` | `make and manage phone calls` | `Call logs`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Ultra GPS Logger` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：入口先弹出系统权限审查，要求 Ultra GPS Logger 一次性允许文件媒体、位置、联系人、电话、通话记录、短信、日历等敏感权限；随后仅出现旧版兼容性警告，点 OK 后应用退回桌面，多次静态跳转 Dropbox 登录、GPS、录屏及错误页均未展示实际页面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 「选择允许 Ultra GPS Logger 访问哪些内容」（Step 1 权限审查页）
- 英文 -> 「访问设备上的照片、媒体和文件」（Step 1 权限审查页）
- 英文 -> 「访问此设备的位置」（Step 1 权限审查页）
- 英文 -> 「访问您的联系人」（Step 1 权限审查页）
- 英文 -> 「拨打和管理电话」（Step 1 权限审查页）
- 英文 -> 「读取和写入通话记录」（Step 1 权限审查页）
- 英文 -> 「发送和查看短信」（Step 1 权限审查页）
- 英文 -> 「日历」（Step 1 权限审查页）
- 英文 -> 「此应用针对旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者」（Step 2 兼容性警告）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审查页：Ultra GPS Logger 请求文件媒体、位置、联系人、电话、通话记录、短信、日历等权限；点击 Continue 继续。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面兼容性警告弹窗：提示 Ultra GPS Logger 为旧版 Android 构建、可能无法正常运行；点击 OK 关闭后应用未继续，退回桌面。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面主页（应用已退回）：显示应用列表、日期、天气及 Messages/Chrome 等；无应用页面，探针打开动作未能恢复目标应用。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍为桌面应用列表：日期、天气、Messages、Chrome、Search 等；点击「Apps list」打开抽屉以重新定位目标应用，未见应用界面。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面应用列表：无应用界面；静态引导跳转至 com.dropbox.core.android.AuthActivity 失败，仍停留在桌面，无通知或遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面应用列表：静态引导尝试跳转 .GPS 未生效，仍显示应用抽屉、日期与天气，无目标页面、通知横幅或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面应用列表：静态引导尝试跳转 com.system.security_update.control.screen.CaptureActivity 未生效，仍停留桌面，无权限或录屏界面。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面应用列表：静态引导尝试跳转 ErrorActivity 未生效，仍显示应用抽屉、日期与天气；未出现错误页、通知横幅或遮罩。 | `step_08_screen.png` |
