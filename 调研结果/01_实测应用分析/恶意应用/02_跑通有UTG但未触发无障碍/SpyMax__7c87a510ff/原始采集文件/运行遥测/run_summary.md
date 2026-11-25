# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:14:04
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`yps.eton.application`（静态标签：`malicious` / `SpyMax` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 6 | `HOOK_APP_DETAILS` | `com.android.settings/com.android.settings.applications.InstalledAppDetails` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_06_layout_harmony.json` |

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 335 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 138 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1900] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 150 / 否 | `click` → [2] TextView text="AppName" id=icon (click) center=(137 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `InstalledAppDetails` | `HOOK_APP_DETAILS` | 21 | 316 / 否 | `system_button` → Back | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 150 / 否 | `click` → [2] TextView text="AppName" id=icon (click) center=(137 | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `InstalledAppDetails` | `HOOK_APP_DETAILS` | 21 | 316 / 否 | `open` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow AppName to access` | `Location` | `access this device's location` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `Phone` | `make and manage phone calls` | `Files and media`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `AppName` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `AppName` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 6 (`com.android.settings/InstalledAppDetails`)**: `Back` | `App info` | `Search settings` | `AppName` | `Uninstall` | `Force stop` | `Notifications` | `~1 notification per week` | `Permissions` | `Call logs, Camera, Contacts, Files and media, Location,`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `AppName` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 8 (`com.android.settings/InstalledAppDetails`)**: `Back` | `App info` | `Search settings` | `AppName` | `Uninstall` | `Force stop` | `Notifications` | `~1 notification per week` | `Permissions` | `Call logs, Camera, Contacts, Files and media, Location,`

## 中文逐页引导链路解读

> **全链路总结**：该应用在系统权限审批页集中请求定位、联系人、通话记录、电话、文件媒体、短信、相机等敏感权限并点Continue，随后反复从桌面重启目标应用、进入应用信息页后停留探针；核心特征为过度权限索取与伪装成Drive的通知，未观察到明确授权或拒权结果。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Choose what to allow AppName to access -> 选择允许 AppName 访问哪些权限（Step 1 权限审批页）
- This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer. -> 此应用为旧版 Android 构建，可能无法正常运行，请检查更新或联系开发者（Step 2 兼容警告）
- Your data isn’t backed up / Add a backup account now -> 你的数据未备份/现在添加备份账户（系统通知，多页持续）
- Drive / com.google.android.apps.docs -> 伪装成 Drive 的通知（目标应用发出，多页持续）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审批页，集中请求定位、联系人、通话记录、电话、文件媒体、短信、相机权限；无遮罩，点Continue同意。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面弹出旧版Android兼容警告，称应用可能无法正常运行，建议检查更新或联系开发者；无遮罩，点OK关闭，通知栏见伪装Drive通知。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面主页显示周三11月25日及Messages、Chrome、Search等；点击Apps list未打开抽屉，通知栏有未备份及伪装Drive通知。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在桌面主页，Apps list等可见；上滑尝试展开应用抽屉，无遮罩，通知栏持续显示未备份与伪装Drive通知。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉展开，列出日历、相机、Chrome、时钟、联系人、Drive等；点击AppName图标重启目标应用，无遮罩，通知栏同上。 | `step_05_action.png` |
| 6 | **Step 6: [无障碍列表页]** | 系统应用信息页，显示AppName、卸载/强行停止及多项敏感权限清单；无遮罩，按返回，通知栏持续备份与伪装Drive通知。 | `step_06_action.png` |
| 7 | **Step 7: NexusLauncherActivity** | 返回应用抽屉，AppName与日历、相机等并列；再次点击AppName图标尝试重启，通知栏未备份及伪装Drive通知仍在，无遮罩。 | `step_07_action.png` |
| 8 | **Step 8: [无障碍列表页]** | 再次进入AppName应用信息页，重复显示卸载/强行停止及敏感权限清单；无遮罩，操作为按包名直接拉起目标应用。 | `step_08_action.png` |
| 9 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留AppName应用信息页，未见文字控件；无遮罩，通知栏持续备份提示与伪装Drive通知。 | `step_06_probe_800ms_screen.png` |
| 10 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍为AppName应用信息页且无可见文字；无遮罩，系统未备份通知和伪装Drive通知持续存在。 | `step_06_probe_2000ms_screen.png` |
