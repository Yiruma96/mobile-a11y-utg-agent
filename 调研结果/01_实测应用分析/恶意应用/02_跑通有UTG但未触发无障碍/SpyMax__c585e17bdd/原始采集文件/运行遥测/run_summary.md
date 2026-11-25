# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:33:22
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`package.name.suffix`（静态标签：`malicious` / `SpyMax` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 341 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 144 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1600] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 156 / 否 | `click` → [17] TextView text="Void PubgHack" id=icon (click) cent | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 156 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 156 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 156 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Void PubgHack to access` | `SMS` | `send and view SMS messages` | `Call logs` | `read and write phone call log` | `Contacts` | `access your contacts` | `Files and media` | `access photos, media, and files on your device` | `Camera`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Void PubgHack` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Void PubgHack”游戏外挂为名，先诱导用户审阅并放行短信、通话记录、联系人、文件、相机、麦克风、定位等敏感权限，再经旧版兼容性警告后从桌面启动；后续静态跳转仅在桌面/抽屉触发随机组件，未呈现目标界面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “选择允许 Void PubgHack 访问哪些内容”（Step 1 权限审查页），以游戏外挂名义集中索取多项敏感权限。
- 英文 -> “此应用是为旧版 Android 构建，可能无法正常运行。请检查更新或联系开发者。”（Step 2 兼容性警告弹窗），用兼容性说明降低警惕。
- 英文 -> “Void PubgHack”（Step 5 应用抽屉图标/应用名），以“PUBG 外挂”命名诱导点击启动。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限页：Void PubgHack 请求短信、通话记录、联系人、文件、相机、麦克风、定位等权限；点击“继续”放行。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 旧版兼容性警告弹窗：称该应用为旧版 Android 构建、可能异常，点击“OK”关闭；通知栏见目标包空标题通知。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面应用列表页：显示 Messages、Chrome、搜索等；点击“Apps list”打开抽屉查找目标，通知栏仍有目标包空通知。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在桌面应用列表：显示 Messages、Chrome、搜索等；上滑打开应用抽屉定位目标，未见应用界面，通知栏空通知仍在。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉网格：列出日历、相机、Chrome、时钟、联系人等；点击“Void PubgHack”图标启动，通知栏空通知仍在。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍停留桌面应用抽屉，未见目标界面；执行静态 Activity 跳转至随机后缀包名组件，页面无变化，通知栏空通知仍在。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍为桌面应用抽屉，未见目标 UI；静态引导跳转至另一随机后缀包名组件，页面无可见变化，通知栏空通知仍在。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 仍为桌面应用抽屉，未出现目标界面；第三次静态跳转至随机包名组件探针，页面无变化，仅保留目标包空标题通知。 | `step_08_screen.png` |
