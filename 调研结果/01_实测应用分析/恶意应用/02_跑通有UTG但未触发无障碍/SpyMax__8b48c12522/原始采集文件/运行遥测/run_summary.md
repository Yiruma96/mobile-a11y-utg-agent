# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:41:19
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`package.name.suffix`（静态标签：`malicious` / `SpyMax` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 343 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 146 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [890, 2209] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 2 | 52 / 否 | `click` → [2] ImageView desc="Close" id=dismiss (click) center=(9 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 7 | 25 / 否 | `click` → [540, 1860] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow corona live 1.1 to access` | `SMS` | `send and view SMS messages` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Files and media` | `access photos, media, and files on your device` | `Camera`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `corona live 1.1` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Select text and images to copy, share, and more` | `Close`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Screenshot` | `Select`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：应用先以“corona live 1.1”触发系统运行时权限页，集中索取短信、通话记录、联系人、文件媒体、相机、麦克风和位置；继续后仅出现旧版兼容警告即退到桌面并留下空通知，后续通过静态跳转尝试拉起多个混淆活动但无可见界面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 corona live 1.1 访问哪些内容”（Step 1 系统权限页；逐项列出短信、通话记录、联系人、文件媒体、相机、麦克风、位置等敏感权限）
- 英文 -> “此应用为旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者”（Step 2 兼容性警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限页：为“corona live 1.1”索取短信、通话记录、联系人、文件媒体、相机、麦克风和位置；本步点“继续”授权。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面弹出旧版 Android 兼容性警告，称应用可能无法正常运行；本步点“OK”关闭，目标包空通知仍在。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面应用列表页，显示日期、信息、Chrome、搜索与语音搜索；目标应用已退后台，空通知仍在；本步点空白处尝试回最近任务。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面截图编辑浮层，提示可选择文字和图片复制分享；本步点“关闭”叉号，消除浮层并返回桌面。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面应用列表出现“Screenshot/Select”，疑似截图或 Chrome 无障碍说明浮层；本步点外部区域关闭浮层。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍在桌面应用列表；探针静态跳转到混淆活动 dofnw...，界面无可见变化，仅目标包空通知持续存在。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面应用列表未变；再次静态跳转到混淆活动 xixwfcyemxe41914，未见应用新页面，空通知仍驻留。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面列表仍未变化；静态跳转到混淆活动 xixwfcyemxe4191，未展示可见界面，显示目标包后台活动与空通知异常。 | `step_08_screen.png` |
