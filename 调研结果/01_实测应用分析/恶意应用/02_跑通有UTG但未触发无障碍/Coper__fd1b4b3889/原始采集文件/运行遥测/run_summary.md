# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:13:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.nameown12`（静态标签：`malicious` / `Coper` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 53 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 52 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [7] TextView text="Chrome" (click) center=(741,1804) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.chrome` / `FirstRunActivity` | `-` | 4 | 237 / 否 | `system_button` → Home | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.nameown12` / `p041j` | `-` | 1 | 0 / 是 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Chrome to make and manage phone calls?` | `Allow` | `Deny`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Chrome to send and view SMS messages?` | `Allow` | `Deny`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.android.chrome/FirstRunActivity`)**: `Welcome to Chrome` | `By using Chrome, you agree to the Google Terms of Servi` | `Help make Chrome better by sending usage statistics and` | `Accept & continue`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.nameown12/p041j`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：应用先以Chrome名义请求通话与短信权限，再用桌面通知“启用服务/Chrome”和同名图标诱导点击；点击一度误入真实Chrome，之后通过静态跳转进入恶意包空白页继续探针，未测试到拒权路径。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “允许Chrome拨打和管理电话？”（Step 1 系统权限弹窗）
- 英语 -> “允许Chrome发送和查看短信？”（Step 2 系统权限弹窗）
- 土耳其语 -> “启用服务”，正文“Chrome”（Step 3/5/6/7/8 通知横幅）
- 英语 -> “欢迎使用Chrome”“接受并继续”及服务条款/使用统计说明（Step 4 真实Chrome首启页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 系统权限弹窗：请求“允许Chrome拨打和管理电话？”，点击“Allow”授权；无遮罩、无通知，属敏感通话权限诱导。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 系统权限弹窗：请求“允许Chrome发送和查看短信？”，再次点击“Allow”授权；无遮罩、无通知，属短信权限诱导。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面应用列表：通知横幅显示土耳其语“启用服务”、正文“Chrome”，点击Chrome图标却启动真实Chrome，未进入仿冒页。 | `step_03_action.png` |
| 4 | **Step 4: FirstRunActivity** | 真实Chrome首启页：显示“欢迎使用Chrome”及服务条款/使用统计说明，点击Home退出；仿冒应用通知横幅仍留在通知栏。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 返回桌面：通知横幅仍为“启用服务/Chrome”，点击“Apps list”打开应用抽屉，试图区分同名Chrome并定位仿冒入口。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面应用列表：静态引导跳转至恶意包内.p075f探针，界面仍停在桌面，通知横幅“启用服务/Chrome”持续显示。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面应用列表：再次静态跳转至恶意包内.p045l探针，仍无恶意页面内容可见，通知横幅“启用服务/Chrome”继续存在。 | `step_07_screen.png` |
| 8 | **Step 8: p041j** | 进入恶意包空白页p041j：无可见文字或控件，仅保留“启用服务/Chrome”通知，随即静态跳转至.p042g继续探针。 | `step_08_screen.png` |
