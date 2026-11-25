# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:21:20
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.mobihk.v`（静态标签：`malicious` / `SpyMax` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 335 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 138 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow AppName to access` | `Location` | `access this device's location` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `Phone` | `make and manage phone calls` | `Files and media`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `AppName` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | Step 1: ReviewPermissionsActivity（ReviewPermissionsActivity）：Choose what to allow AppName to access /；动作 click | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | Step 2: NexusLauncherActivity（NexusLauncherActivity）：AppName / This app was built for an olde；动作 click | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | Step 3: NexusLauncherActivity（NexusLauncherActivity）：Apps list / Wednesday, Nov 25 / Messages；动作 open | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | Step 4: NexusLauncherActivity（NexusLauncherActivity）：Apps list / Wednesday, Nov 25 / Messages；动作 open | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | Step 5: NexusLauncherActivity（NexusLauncherActivity）：Apps list / Wednesday, Nov 25 / Messages；动作 static_activity_jump | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | Step 6: NexusLauncherActivity（NexusLauncherActivity）：Apps list / Wednesday, Nov 25 / Messages；动作 static_activity_jump | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | Step 7: NexusLauncherActivity（NexusLauncherActivity）：Apps list / Wednesday, Nov 25 / Messages；动作 static_activity_jump | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | Step 8: NexusLauncherActivity（NexusLauncherActivity）：Apps list / Wednesday, Nov 25 / Messages；动作 static_activity_jump | `step_08_screen.png` |
