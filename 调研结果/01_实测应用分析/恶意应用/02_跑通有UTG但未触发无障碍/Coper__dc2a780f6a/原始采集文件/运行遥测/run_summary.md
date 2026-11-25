# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:31:28
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.pagethan10`（静态标签：`malicious` / `Coper` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [540, 2200] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 53 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 53 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Chrome to access your contacts?` | `Allow` | `Deny`
- **Step 8 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Chrome to access your contacts?` | `Allow` | `Deny`

## 中文逐页引导链路解读

> **全链路总结**：应用启动未生效，轨迹停留在桌面/应用抽屉；多次点击与上滑失败后，通过静态 Activity 跳转探针触发系统联系人权限页，请求允许 Google Chrome 访问联系人，未记录授权/拒绝结果，未测试拒权。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面 NexusLauncher 主屏，显示应用列表、搜索及“数据未备份/立即添加备份账户”通知；启动目标应用未生效。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面主屏；点击“应用列表”未打开抽屉，界面不变，系统“数据未备份/立即添加备份账户”通知仍在，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 仍为桌面；静态跳转探针执行至 .p078w，界面无变化，应用列表、搜索与系统备份通知仍显示，无遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面主屏；上滑手势后仍未展开应用抽屉，页面文本不变，仅系统“数据未备份”通知持续显示，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉展开，列出日历、相机、Chrome、时钟、通讯录等图标；系统“数据未备份”通知仍在，无遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 应用抽屉页；静态跳转探针至 .p063j 后未出现目标界面，仍显示日历、相机、Chrome 等图标与备份通知，无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: GrantPermissionsActivity** | 系统权限页：英文询问是否允许 Google Chrome 访问联系人，含允许/拒绝；由 .p064x 跳转触发，无遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: GrantPermissionsActivity** | 仍为系统联系人权限页，重复显示允许/拒绝；探针跳转 .p010r 后未授权也未拒绝，无遮罩，备份通知仍在。 | `step_08_screen.png` |
