# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:36:57
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.fees.claim`（静态标签：`malicious` / `SpyNote` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [540, 1900] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `click` → [19] FrameLayout desc="Search" id=search_container_all_ | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `type` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 29 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 29 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `DeviceAdminAdd` | `-` | 12 | 370 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Blockchain` | `Clear`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Blockchain` | `Clear`
- **Step 8 (`com.android.settings/DeviceAdminAdd`)**: `Activate device admin app?` | `Blockchain` | `Click on Activate button to secure your application.` | `Activating this admin app will allow the app Blockchain` | `Erase all data` | `Erase the phone's data without warning by performing a ` | `Lock the screen` | `Control how and when the screen locks.` | `Activate this device admin app` | `Cancel`

## 中文逐页引导链路解读

> **全链路总结**：该样本以伪装名“Blockchain”引导用户在桌面搜索并打开，随后通过静态跳转进入可疑包 com.fees.ttxj... 的组件，最终拉起 Android 设备管理激活页，索要清除数据与锁屏等高危权限；页面保留取消/卸载入口，未观察到实际授权结果（not_tested）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “点击‘激活’按钮以保护你的应用。”（Step 8 设备管理激活页）
- English -> “激活此管理应用将允许 Blockchain 执行以下操作：”（Step 8 设备管理激活页）
- English -> “执行恢复出厂设置，在无警告情况下清除手机数据。”（Step 8 设备管理激活页）
- English -> “锁定屏幕；控制屏幕锁定的方式与时机。”（Step 8 设备管理激活页）
- English -> “激活此设备管理应用”（Step 8 设备管理激活页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面主页，显示应用列表、Chrome、搜索等；顶部有“数据未备份”系统通知。点击“Apps list”未进入抽屉。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面主页，系统“数据未备份”通知横幅可见；点击应用列表无响应后上滑，未成功打开抽屉。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 上滑后出现应用抽屉，列出相机、Chrome、Gmail 等；系统备份通知仍在，无遮罩；继续上滑寻找目标应用。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 应用抽屉列表，含日历、相机、Chrome 等；系统备份通知可见。点击顶部搜索框，拟搜索“Blockchain”。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉搜索页，提示搜索应用/网页；系统备份通知仍在；输入“Blockchain”定位伪装应用。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 搜索框显示“Blockchain”及清除按钮；触发静态跳转至可疑包 com.fees...，非正常点击结果。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 同一搜索页仍显示“Blockchain”，系统备份通知在；再次静态跳转至可疑包 Security 页，非用户点击。 | `step_07_screen.png` |
| 8 | **Step 8: DeviceAdminAdd** | 设备管理激活页：伪装名“Blockchain”，称激活可保护应用；索要清除数据、锁屏权限；有取消/卸载键，无遮罩。 | `step_08_screen.png` |
