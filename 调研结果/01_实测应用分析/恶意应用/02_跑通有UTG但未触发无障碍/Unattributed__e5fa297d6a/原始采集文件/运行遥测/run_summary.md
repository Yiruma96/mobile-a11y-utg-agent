# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:12:05
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`uplift.shadow.planet`（静态标签：`malicious` / `Unattributed` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [540, 1700] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `click` → [19] FrameLayout desc="Search" id=search_container_all_ | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `type` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 16 | 136 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `uplift.shadow.planet` / `A1` | `-` | 16 | 136 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `uplift.shadow.planet` / `bdavykqpfj` | `-` | 16 | 136 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `p` | `Clear` | `FROM YOUR APPS` | `Open Phone.` | `Phone` | `Open Photos.` | `Photos` | `Open Play Movies & TV.` | `Play Movies & TV`
- **Step 7 (`uplift.shadow.planet/A1`)**: `Go to Discover` | `p` | `Clear` | `FROM YOUR APPS` | `Open Phone.` | `Phone` | `Open Photos.` | `Photos` | `Open Play Movies & TV.` | `Play Movies & TV`
- **Step 8 (`uplift.shadow.planet/bdavykqpfj`)**: `Go to Discover` | `p` | `Clear` | `FROM YOUR APPS` | `Open Phone.` | `Phone` | `Open Photos.` | `Photos` | `Open Play Movies & TV.` | `Play Movies & TV`

## 中文逐页引导链路解读

> **全链路总结**：链路从NexusLauncher主屏及应用抽屉开始，多次滑动、搜索“p”均未进入目标应用；随后以静态Activity跳转进入uplift.shadow.planet的A1与bdavykqpfj，前台始终显示启动器搜索页，仅新增应用通知“<E>”，未出现授权弹窗或实质诱导界面，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 中文意译：系统通知“Your data isn’t backed up”/“Add a backup account now”=“你的数据尚未备份”/“立即添加备份账户”（step_01-08通知横幅，属系统备份提醒，非应用自有话术）
- 占位符 -> “<E>”：应用包通知标题与正文均为不可读占位符（step_07-08），不构成可读诱导话术

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 启动器主屏；点“Apps list/应用列表”未打开抽屉，顶部有“数据未备份/添加备份账户”通知，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在启动器主屏；上滑试图打开应用抽屉但未成功，屏幕保持原样，备份提醒通知持续，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 启动器显示应用图标列表（日历/相机等）；再次上滑未展开抽屉，备份提醒仍在，未见应用自有界面或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 应用抽屉已显示系统图标；点击“Search/搜索”容器，准备用启动器搜索定位目标，备份提醒仍在，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 启动器搜索页，显示“Search apps, web, and more…/搜索应用、网页等…”；搜索框获焦并输入，未见诱导授权弹窗。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 搜索“p”后列出“FROM YOUR APPS/来自你的应用”等建议；静态引导回退跳转至应用A1，视觉仍为启动器，无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: A1** | 应用A1无可见自有UI，屏仍为启动器搜索“p”；应用通知“<E>”出现，备份提醒并存，无遮罩、无取消键；静态跳至A2。 | `step_07_screen.png` |
| 8 | **Step 8: bdavykqpfj** | 应用bdavykqpfj同样无可见界面，仍显示启动器搜索“p”；“<E>”与备份通知并存，无遮罩；静态跳至HomeSIM。 | `step_08_screen.png` |
