# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:39:08
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.ebhgqwi.qzgbqzm`（静态标签：`malicious` / `Copybara` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `click` → [2] TextView text="BBVA Codigo" id=icon (click) center= | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `click` → [2] TextView text="BBVA Codigo" id=icon (click) center= | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `BBVA Codigo` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `BBVA Codigo` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `BBVA Codigo` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `BBVA Codigo` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `BBVA Codigo` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `BBVA Codigo` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`

## 中文逐页引导链路解读

> **全链路总结**：本次运行始终停留在NexusLauncher桌面，未进入恶意包界面；点击疑似仿冒的“BBVA Codigo”图标未加载，随后对 service2、AdminReceiver2、service1、notificationservice 的静态跳转均回落桌面；未出现授权弹窗、通知或遮罩，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文/西班牙语“BBVA Codigo” -> 中文“BBVA验证码/编码”（Step 3–8桌面图标）：疑似冒充银行应用名称，非弹窗诱导话术

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用列表页，显示“Apps list/应用列表”等英文；点击“Apps list”未进入应用，无通知横幅与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面，英文“Apps list”意为应用列表；上滑尝试打开抽屉，页面未变，无通知横幅与悬浮遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面抽屉展开，出现“BBVA Codigo”（BBVA验证码）等图标；点击该疑似仿冒银行图标，未见应用界面，无通知遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在桌面抽屉，“BBVA Codigo”意为BBVA验证码；再次点击仍未加载WebView或应用页，无通知与遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 仍停桌面抽屉，无新增界面；静态跳转 service2 服务组件失败并回落桌面，无通知横幅、无遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面抽屉未变；静态引导跳转 AdminReceiver2（设备管理接收器）未显示界面，仍无通知横幅与遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍在桌面抽屉；探针跳转 service1 服务组件后回落，页面无变化，未见授权弹窗、通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面抽屉保持原样；尝试跳转 notificationservice（通知服务）未进入应用页，无通知、遮罩或授权提示。 | `step_08_screen.png` |
