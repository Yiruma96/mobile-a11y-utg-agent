# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:44:50
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sqhiibt.wdqknqa`（静态标签：`malicious` / `Copybara` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 149 / 否 | `click` → [13] TextView text="My BNL" id=icon (click) center=(338 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 149 / 否 | `click` → [13] TextView text="My BNL" id=icon (click) center=(338 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 149 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 149 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 149 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 149 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：动态链路从桌面/应用抽屉开始，点击“My BNL”两次均未进入应用界面，随后静态跳转探测 service2、AdminReceiver2、service1、notificationservice 等组件也均未渲染；全程未见授权/拒权页或应用内诱导话术，仅有系统“数据未备份”通知，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “你的数据未备份”（主屏/应用抽屉系统通知，非应用界面）
- 英文 -> “立即添加备份账户”（同上，系统通知引导）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 主屏/应用抽屉入口，英文“Apps list”意为应用列表；点击应用列表，顶部系统通知提示“数据未备份”，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为主屏/应用抽屉，显示搜索、Chrome等；上滑试图打开抽屉寻找“My BNL”，系统备份通知仍在，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉列表出现“My BNL”；点击该图标尝试启动恶意应用，但页面未切换，系统备份通知仍在，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在应用抽屉，再次点击“My BNL”并等待；可能被模拟器检测提示阻挡，未进入应用界面，通知不变且无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉未变；静态跳转探针指向 service2_BR 服务组件，未渲染新界面，仅见系统备份通知，无遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 应用抽屉未变；静态跳转探针指向 AdminReceiver2 设备管理组件，未弹出授权页，系统备份通知仍在，无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 应用抽屉未变；静态跳转探针指向 service1_BR 服务组件，仍停留启动器，未出现诱导或授权界面，无遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 应用抽屉未变；静态跳转探针指向 notificationservice_BR 通知服务组件，未渲染页面，仅系统备份通知，无遮罩。 | `step_08_screen.png` |
