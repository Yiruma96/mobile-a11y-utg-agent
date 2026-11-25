# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:09:27
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.androidsys.app`（静态标签：`malicious` / `donot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 331 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.androidsys.app` / `MainActivity` | `-` | 3 | 142 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.androidsys.app` / `MainActivity` | `-` | 2 | 115 / 否 | `click` → [2] Button text="OK" id=button1 (click) center=(887,115 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Android Sys to access` | `SMS` | `send and view SMS messages` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `Phone`
- **Step 2 (`com.androidsys.app/MainActivity`)**: `Android Sys` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.androidsys.app/MainActivity`)**: `Please enable 'Accessibility' for 'Android Sys' to get ` | `OK`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：应用首启经系统权限总览诱导继续，随后用旧版兼容提示与不可取消对话框索要无障碍权限，未见实际授权结果。之后反复跳回桌面并静态拉起 JobBootReceiver、fourre、PhonecallReceiver 等后台组件，未展示正常业务界面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English: Choose what to allow Android Sys to access → 中文核心意译：选择允许 Android Sys 访问哪些内容（Step 1 权限总览页）
- English: This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer. → 中文核心意译：应用为旧版 Android 构建，可能无法正常运行，请检查更新或联系开发者（Step 2 兼容提示）
- English: Please enable 'Accessibility' for 'Android Sys' to get this working. Tap on 'Ok' to go to Accessibility Settings. → 中文核心意译：请为 Android Sys 开启无障碍才能正常工作，点 OK 前往无障碍设置（Step 3 诱导弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限总览页，列出短信、文件媒体、联系人、通话记录、电话、麦克风、位置等权限；无遮罩/通知，点击「Continue」继续。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 返回应用主界面，弹出旧版 Android 兼容提示，称可能无法正常运行；点击「OK」关闭系统对话框继续。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 应用内弹窗以需开启无障碍才能工作为由诱导点击「OK」跳转无障碍设置；无取消键、无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 已跳至桌面启动器，仅见应用列表、日期和常用图标；无目标界面，探针尝试重启 com.qooqle.droid.mrch。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 仍在桌面启动器，界面与应用列表未变；再次尝试拉起目标包 com.qooqle.droid.mrch，未出现新页面。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面未变，执行静态引导跳转回退至 com.evernote.android.job.JobBootReceiver，无可见应用界面。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面未变，静态引导回退拉起 com.qooqle.droid.mrch.afo.fourre 组件，界面无变化。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面未变，静态引导回退拉起 com.qooqle.droid.mrch.ase.PhonecallReceiver，仍无可见业务界面。 | `step_08_screen.png` |
