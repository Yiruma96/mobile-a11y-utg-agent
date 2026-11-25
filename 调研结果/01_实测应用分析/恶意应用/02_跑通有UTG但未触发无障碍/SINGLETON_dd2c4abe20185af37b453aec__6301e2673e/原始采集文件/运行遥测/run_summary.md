# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:56:36
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.update.system.important`（静态标签：`malicious` / `SINGLETON:dd2c4abe20185af37b453aec5a99c165` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 37 | 341 / 否 | `click` → [37] Button text="Continue" id=continue_button (click)  | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 144 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow System Update to access` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location` | `access this device's location` | `Microphone` | `record audio` | `Phone`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `System Update` | `This app was built for an older version of Android and ` | `OK`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：该应用从桌面启动失败后，借静态引导跳转进入权限审查页，以“System Update（系统更新）”名义一次性索取联系人、相机、位置、麦克风、电话、通话记录和短信等广泛权限，并用旧版 Android 兼容警告诱导点击 OK；随后跳转包广播与电池/约束后台组件，全程无通知横幅或遮罩，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “选择允许系统更新访问哪些内容”（Step 4 权限审查页）
- 英语 -> “此应用针对旧版 Android 构建，可能无法正常运行。请检查更新或联系开发者”（Step 5 兼容性警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器页，显示应用列表、日期及 Messages/Chrome/搜索入口；按包名直接启动目标应用，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面启动器页，应用列表与常用图标可见；因目标未启动而打开应用列表寻找入口，无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面启动器页保持显示，UI 未变；执行静态引导跳转探针到 .LeanbackLauncherActivity，无可见反馈、通知或遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: ReviewPermissionsActivity** | 权限审查页，要求为“系统更新”勾选联系人、相机、位置、麦克风、电话、通话记录、短信等权限；点击 Continue 继续，无通知或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面启动器上的兼容性警告弹窗，提示“System Update”为旧版 Android 构建、可能无法正常运行；点击 OK 关闭，无通知或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 返回桌面启动器页，应用列表与日期可见；执行静态引导跳转到 .reciever.PackageBroadcast 广播组件，无界面反馈、通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面启动器页无变化，仍显示应用列表与常用图标；静态跳转至 WorkManager 的 ConstraintProxy$Batter... 组件，无通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面启动器页无变化，显示应用列表、日期与搜索入口；静态跳转至 .reciever.BatteryChargingBroadcast 广播组件，无通知或遮罩。 | `step_08_screen.png` |
