# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:11:13
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`cmf0.c3b5bm90zq.patch`（静态标签：`malicious` / `SpyMax` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 340 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `DeviceAdminAdd` | `-` | 3 | 143 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `DeviceAdminAdd` | `-` | 23 | 877 / 否 | `click` → [22] Button text="Activate this device admin app" id=ac | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow media player to access` | `Camera` | `take pictures and record video` | `Files and media` | `access photos, media, and files on your device` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Microphone`
- **Step 2 (`com.android.settings/DeviceAdminAdd`)**: `media player` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.android.settings/DeviceAdminAdd`)**: `Activate device admin app?` | `media player` | `Activating this admin app will allow the app media play` | `Erase all data` | `Erase the phone's data without warning by performing a ` | `Change the screen lock` | `Change the screen lock.` | `Set password rules` | `Control the length and the characters allowed in screen` | `Monitor screen unlock attempts`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：该样本以“media player/媒体播放器”伪装，先引导通过系统权限复核，再弹旧版兼容警告并诱导激活设备管理员，授予擦除数据、改锁屏、密码规则与解锁监控等高危权限；随后多次回到桌面并通过静态跳转 .C7/.C3/.C8 探针未呈现新界面，通知栏持续出现可疑 String 横幅，拒权路径未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 选择允许“媒体播放器”访问的内容（Step 1 权限复核页）
- 英语 -> 此应用为旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者（Step 2 兼容警告）
- 英语 -> 激活此设备管理应用？激活后“媒体播放器”可执行以下操作（Step 3 设备管理激活页）
- 英语 -> 可无警告恢复出厂设置并擦除手机全部数据（Step 3 设备管理激活页）
- 英语 -> 可更改锁屏、设置密码长度/字符规则、监控错误解锁次数并在多次输错后锁屏或擦除数据（Step 3 设备管理激活页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限复核页：询问“允许媒体播放器访问什么”，列出相机、文件、通话记录、联系人、麦克风、短信、电话；点继续放行。 | `step_01_action.png` |
| 2 | **Step 2: DeviceAdminAdd** | 设备管理添加页：冒充“媒体播放器”弹旧版兼容警告“可能无法正常运行”，通知栏有可疑 String 横幅；点 OK 进入激活。 | `step_02_action.png` |
| 3 | **Step 3: DeviceAdminAdd** | 设备管理激活页：以“媒体播放器”请求管理员，宣称可擦数据、改锁屏和密码规则、监控解锁及锁屏；点击激活，通知横幅仍在。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 返回桌面启动器：显示应用列表、日期和 Messages/Chrome/Search 图标；管理员激活后跳回桌面，可疑 String 通知仍驻留。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 仍在桌面启动器：显示应用列表与常用图标；点击“应用列表”试图查找并重启恶意应用，可疑 String 通知横幅未消失。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面启动器无可见变化：仍为应用列表/常用图标；探针直接跳转 .C7 组件，未见应用界面，可疑 String 通知持续。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面启动器仍停留：应用列表与图标未变；探针尝试跳转 .C3 组件未见新界面，String 通知横幅继续驻留，遮罩为 0。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面启动器仍无新界面：显示应用列表/常用图标；探针尝试跳转 .C8 组件失败或未渲染，通知持续，未出现授权弹窗。 | `step_08_screen.png` |
