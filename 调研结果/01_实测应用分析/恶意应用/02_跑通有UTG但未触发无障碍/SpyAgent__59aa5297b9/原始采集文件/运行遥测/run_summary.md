# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:57:36
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`yps.eton.application`（静态标签：`malicious` / `SpyAgent` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 333 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 136 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow FBPRO to access` | `Camera` | `take pictures and record video` | `Files and media` | `access photos, media, and files on your device` | `Call logs` | `read and write phone call log` | `SMS` | `send and view SMS messages` | `Contacts`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `FBPRO` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：应用入口先请求FBPRO的相机、文件媒体、通话记录、短信、联系人、麦克风与电话等宽泛权限，并以“继续”推进；随后仅见旧版Android兼容警告和持续FBPRO通知，返回启动器后多次显式/静态跳转（.M/.D/.C/.B）均未进入应用界面，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 选择允许FBPRO访问的内容（Step 1 系统权限页）
- 英文 -> 拍照并录制视频（Step 1 相机权限说明）
- 英文 -> 访问设备上的照片、媒体和文件（Step 1 文件与媒体权限说明）
- 英文 -> 读取和写入通话记录（Step 1 通话记录权限说明）
- 英文 -> 发送和查看短信（Step 1 短信权限说明）
- 英文 -> 访问联系人（Step 1 联系人权限说明）
- 英文 -> 录制音频（Step 1 麦克风权限说明）
- 英文 -> 此应用为旧版Android构建，可能无法正常运行；请检查更新或联系开发者（Step 2 启动器兼容警告）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限页列出FBPRO可访问的相机、文件媒体、通话记录、短信、联系人、麦克风与电话；仅见“继续”键，本步点击跳过授权弹窗。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 启动器弹出旧版Android兼容警告，称FBPRO可能无法正常运行；通知栏仍有FBPRO横幅，本步点击“OK”关闭警告。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到启动器主屏，显示应用列表、日期与Messages/Chrome等图标；FBPRO通知横幅仍在，本步尝试打开应用继续流程。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在启动器主屏，可见应用列表与Messages/Chrome图标；FBPRO通知横幅持续，本步按包名显式重启应用但未进入界面。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 静态跳转探针尝试进入.M页面，但界面仍停在启动器主屏；FBPRO通知横幅持续存在，未出现任何应用界面。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 静态跳转探针尝试进入.D页面，界面仍停在启动器主屏；FBPRO通知横幅仍显示，未出现应用内页面或授权提示。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 静态跳转探针尝试进入.C页面，系统仍显示启动器主屏与应用列表；FBPRO通知横幅持续，未进入应用界面。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 静态跳转探针尝试进入.B页面，仍停留在启动器主屏；FBPRO通知横幅持续存在，未出现应用页面或进一步诱导。 | `step_08_screen.png` |
