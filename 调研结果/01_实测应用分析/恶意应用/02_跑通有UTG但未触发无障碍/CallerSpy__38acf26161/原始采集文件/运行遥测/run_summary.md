# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:10:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sas.gservices.accesibility`（静态标签：`malicious` / `CallerSpy` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 337 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 140 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow GSERVICES to access` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `SMS` | `send and view SMS messages` | `Files and media` | `access photos, media, and files on your device` | `Phone`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `GSERVICES` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：该应用先借系统权限控制器批量索取联系人、通话记录、短信、文件媒体、电话、麦克风、相机等敏感权限，随后出现旧版兼容警告；点击OK后多次回到桌面，并以显式启动和静态Activity跳转探针尝试拉起悬浮窗权限、WorkManager约束代理与BootReceiver，未观察到后续前台界面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 选择允许GSERVICES访问哪些权限（Step1权限总览页）
- English -> 联系人：访问您的联系人（Step1）
- English -> 通话记录：读写电话通话记录（Step1）
- English -> 短信：发送和查看短信（Step1）
- English -> 文件与媒体：访问设备上的照片、媒体和文件（Step1）
- English -> 电话：拨打和管理电话（Step1）
- English -> 麦克风：录制音频（Step1）
- English -> 相机（Step1）
- English -> 此应用为旧版Android构建，可能无法正常工作，请检查更新或联系开发者（Step2兼容性警告）
- English -> OK：确认关闭警告（Step2）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限总览页：英文征询GSERVICES可访问联系人、通话记录、短信、文件媒体、电话、麦克风、相机；点击Continue批量授权，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面系统兼容性警告弹窗：称GSERVICES为旧版Android构建、可能无法正常工作，建议检查更新；点击OK关闭，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面：显示应用列表、日期天气及Messages/Chrome/Search图标；执行open后仍停留桌面，GSERVICES未前台，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面仍为应用列表、日期天气及Messages/Chrome/Search图标；再次open并显式启动com.sas.gservices.accesibility，仍未进前台，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面未变：应用列表、日期天气与常用图标；静态Activity跳转探针指向OPPO悬浮窗权限列表FloatWindowListActivity，界面无变化，无通知/遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面保持应用列表与天气图标；静态跳转探针指向WorkManager的ConstraintProxy$Batter…约束代理，未离开桌面，无通知/遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面仍为应用列表/天气；重复静态跳转探针至WorkManager ConstraintProxy$Batter…，目标页未展示，无通知/遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面未变：应用列表、日期天气与常用图标；静态跳转探针指向.BROADCAST_RECEIVER.BootReceiver，仍未进入目标界面，无通知/遮罩。 | `step_08_screen.png` |
