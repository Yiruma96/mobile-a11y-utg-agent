# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:48:22
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.mufc.fireymn`（静态标签：`malicious` / `Helper` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `1` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：目标应用com.mufc.fireymn两次直接启动均失败，轨迹始终停留在NexusLauncher桌面；随后通过静态回退连续触发com.superman.moduleshell下Boost、Shk、Hearing、Flight、Nhk等后台接收器。全程未见授权/拒权弹窗、通知横幅或遮罩，也无诱导话术，仅有一次点击“Apps list（应用列表）”。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | NexusLauncher桌面，显示“应用列表、信息、Chrome、搜索、语音搜索”等英文入口；尝试启动目标应用未成功，仍停留桌面，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为NexusLauncher桌面，英文元素同前（应用列表、信息、搜索等）；第二次尝试打开目标包仍未启动，无任何授权或诱导界面。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面未变化，英文仍为应用列表与搜索等；探针改为静态跳到BoostEventReceiver，属后台接收器，无可见页面、通知或遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍为启动器桌面，点击“Apps list（应用列表）”试图进抽屉找目标应用；界面未变，未见目标图标或授权弹窗。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面保持原样，英文为应用列表/信息/搜索等；静态跳到ShkReceiver后台组件，未展示页面，也无通知横幅或遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍停留NexusLauncher桌面，应用列表/搜索等英文不变；静态触发HearingTaskReceiver，属隐藏后台接收器，无可见交互或授权提示。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面界面未变，仍见应用列表、信息、Chrome、搜索等英文；静态跳到FlightTaskReceiver后台组件，无页面跳转、通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 仍为NexusLauncher桌面，英文入口同前；静态触发NhkTaskReceiver后台接收器，未见任何前台界面、授权弹窗或通知横幅。 | `step_08_screen.png` |
