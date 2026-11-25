# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:33:59
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.vuji.luzudomi`（静态标签：`malicious` / `Unattributed` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.vuji.luzudomi` / `QewohequyuAuthbc6d` | `-` | 1 | 8 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.vuji.luzudomi` / `QewohequyuAuthbc6d` | `-` | 1 | 8 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.vuji.luzudomi` / `QewohequyuAuthbc6d` | `-` | 1 | 8 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.vuji.luzudomi` / `QewohequyuAuthbc6d` | `-` | 1 | 8 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.vuji.luzudomi` / `QewohequyuAuthbc6d` | `-` | 1 | 8 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.vuji.luzudomi/QewohequyuAuthbc6d`)**: `Loading…`
- **Step 5 (`com.vuji.luzudomi/QewohequyuAuthbc6d`)**: `Loading…`
- **Step 6 (`com.vuji.luzudomi/QewohequyuAuthbc6d`)**: `Loading…`
- **Step 7 (`com.vuji.luzudomi/QewohequyuAuthbc6d`)**: `Loading…`
- **Step 8 (`com.vuji.luzudomi/QewohequyuAuthbc6d`)**: `Loading…`

## 中文逐页引导链路解读

> **全链路总结**：应用入口未正常拉起，先停留在NexusLauncher桌面；随后通过静态Activity跳转进入com.vuji.luzudomi的QewohequyuAuthbc6d，长时间仅显示“Loading…”，并多次被静态引导到GatewayActivity、GoniyulujufoActivity_a12f、WasucisoqeliwubuReceiver_4c2c，未观察到实际授权/拒权或取消操作。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器主页，显示应用列表、搜索与系统“数据未备份”通知；执行打开目标应用但未离开桌面，仍无应用遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在同一桌面/应用列表页，点击“Apps list”尝试打开抽屉寻找目标；系统备份通知仍在，未进入目标应用。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面页未变，改为静态跳转到com.vuji.luzudomi的GoniyulujufoActivity_a12f；无点击、无遮罩，系统通知保留。 | `step_03_screen.png` |
| 4 | **Step 4: QewohequyuAuthbc6d** | 进入目标应用QewohequyuAuthbc6d，仅显示“Loading…”加载中；等待渲染，背景仍有系统“数据未备份”通知，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: QewohequyuAuthbc6d** | 同一目标加载页仍显示“Loading…”；继续等待更久，未见引导页或权限弹窗，系统备份通知持续存在。 | `step_05_action.png` |
| 6 | **Step 6: QewohequyuAuthbc6d** | 仍停留在“Loading…”加载页，随后被静态引导到activities.GatewayActivity；无用户点击，系统备份通知未消失。 | `step_06_screen.png` |
| 7 | **Step 7: QewohequyuAuthbc6d** | 页面仍为“Loading…”，再次通过静态跳转指向GoniyulujufoActivity_a12f；未出现新界面或授权/取消控件。 | `step_07_screen.png` |
| 8 | **Step 8: QewohequyuAuthbc6d** | 仍在“Loading…”页，静态跳转至WasucisoqeliwubuReceiver_4c2c；目标应用未呈现可操作页面，系统通知贯穿。 | `step_08_screen.png` |
