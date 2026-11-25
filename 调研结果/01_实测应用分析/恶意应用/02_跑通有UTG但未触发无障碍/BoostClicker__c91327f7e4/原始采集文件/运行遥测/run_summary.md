# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:08:34
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.xolo.qifyf`（静态标签：`malicious` / `BoostClicker` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 15 | 176 / 否 | `click` → [15] Button text="Continue" id=continue_button (click)  | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.xolo.qifyf` / `AdTransActivity` | `-` | 3 | 141 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.xolo.qifyf` / `AdTransActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.xolo.qifyf` / `AdTransActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.xolo.qifyf` / `AdTransActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow ConfigAPKs to access` | `Files and media` | `access photos, media, and files on your device` | `Phone` | `make and manage phone calls` | `Contacts` | `access your contacts` | `Cancel` | `Continue`
- **Step 5 (`com.xolo.qifyf/AdTransActivity`)**: `ConfigAPKs` | `This app was built for an older version of Android and ` | `OK`
- **Step 6 (`com.xolo.qifyf/AdTransActivity`)**: (空文本)
- **Step 7 (`com.xolo.qifyf/AdTransActivity`)**: (空文本)
- **Step 8 (`com.xolo.qifyf/AdTransActivity`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：目标应用无桌面图标，探针从启动器静态直达 AdTransActivity；权限审核页打包索取文件媒体、电话、联系人并点击 Continue，随后兼容性警告点 OK，再跳转 TransActivity、MReceiver、AccService，未见拒权。核心特征是无图标隐蔽入口、权限聚合索取与组件链过渡。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 选择允许 ConfigAPKs 访问哪些权限（系统权限审核页）
- 英文 -> 文件与媒体：访问设备上的照片、媒体和文件（系统权限审核页）
- 英文 -> 电话：拨打和管理电话（系统权限审核页）
- 英文 -> 联系人：访问联系人（系统权限审核页）
- 英文 -> 该应用为旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者（兼容性警告弹窗）
- 英文 -> 应用显示名为 ConfigAPKs，用于权限审核与兼容性提示（权限页/弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | Nexus 启动器桌面：显示应用列表、日期天气和搜索入口；尝试直接打开目标包但未见图标，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为同一启动器桌面：目标应用无桌面图标，直接启动未成功；页面无通知、无遮罩，外文入口均为系统常规元素。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 启动器未变，探针静态跳转至 com.app.assists.AdTransActivity；无可见诱导文案，属绕过桌面图标的组件直达。 | `step_03_screen.png` |
| 4 | **Step 4: ReviewPermissionsActivity** | 系统权限审核页：英文提示选择允许 ConfigAPKs 访问，列出文件媒体、电话、联系人；本步点击 Continue，仍保留 Cancel。 | `step_04_action.png` |
| 5 | **Step 5: AdTransActivity** | 应用内兼容性警告：英文称 ConfigAPKs 为旧版 Android 构建、可能无法正常运行；点击 OK 关闭后继续跳转。 | `step_05_action.png` |
| 6 | **Step 6: AdTransActivity** | AdTransActivity 空白过渡页：无文案、通知或遮罩；探针静态跳转至 com.app.assists.TransActivity，继续组件链。 | `step_06_screen.png` |
| 7 | **Step 7: AdTransActivity** | AdTransActivity 无可见 UI；探针静态跳转至 MReceiver 接收器，无通知、无遮罩，也无取消或拒绝入口。 | `step_07_screen.png` |
| 8 | **Step 8: AdTransActivity** | AdTransActivity 无可见界面；继续静态跳转至 com.app.assists.service.AccService，链路进入后台服务组件，无通知或遮罩。 | `step_08_screen.png` |
