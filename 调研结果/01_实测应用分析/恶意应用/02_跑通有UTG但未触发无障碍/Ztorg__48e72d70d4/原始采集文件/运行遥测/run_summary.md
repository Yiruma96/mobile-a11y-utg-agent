# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:04:45
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.rxhl.poiu`（静态标签：`malicious` / `Ztorg` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 23 | 241 / 否 | `click` → [23] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 41 / 否 | `click` → [3] Button text="Close app" id=aerr_close (click) cente | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 140 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow fast game to access` | `SMS` | `send and view SMS messages` | `Contacts` | `access your contacts` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Location`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `fast game keeps stopping` | `App info` | `Close app`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `fast game` | `This app was built for an older version of Android and ` | `OK`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：应用以“fast game”游戏名义启动，先请求短信、联系人、电话、文件媒体和位置等高风险权限，随后崩溃并被旧版兼容性弹窗阻断；在桌面多次拉起失败后，通过静态跳转指向广告落地页、辅助功能入口和广播接收器，呈现 Ztorg 类后台推广与规避特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 选择允许“fast game”访问的内容（Step 1 权限总览）
- 英文 -> 发送和查看短信（Step 1 短信权限）
- 英文 -> 访问你的联系人（Step 1 联系人权限）
- 英文 -> 拨打和管理电话（Step 1 电话权限）
- 英文 -> 访问设备上的照片、媒体和文件（Step 1 文件媒体权限）
- 英文 -> 访问本设备位置（Step 1 位置权限）
- 英文 -> “fast game”不断停止运行（Step 2 崩溃弹窗）
- 英文 -> 此应用针对旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者（Step 3 兼容性警告）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限审核页：“fast game”请求短信、联系人、电话、文件媒体与位置权限；本步点“Continue”，有“Cancel”可取消，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面崩溃弹窗称“fast game keeps stopping”（不断停止），有“App info/Close app”；本步点“Close app”，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面兼容性警告：“fast game”针对旧版 Android 构建、可能无法正常运行；本步点“OK”忽略，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面/应用列表页，显示 Messages、Chrome、搜索等，无目标应用界面；本步执行 open 重新拉起被关闭的“fast game”，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面/应用列表页仍无目标应用界面；本步再次按包名 open 拉起“fast game”，以恢复其后台服务，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 界面仍为桌面；静态引导跳转广告落地 Activity（InnerWebLandingActivity），无可见页面、通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 界面仍为桌面；静态引导跳转“辅助功能”Activity（OpenFuzhuAccess），疑似诱导无障碍授权，无可见页面、通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 界面仍为桌面；静态引导跳转广播接收器（com.edcf.MyReceiver），无可见页面、通知或遮罩，疑似后台触发。 | `step_08_screen.png` |
