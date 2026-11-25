# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:39:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`semplo.ic327.skin`（静态标签：`malicious` / `TrickMo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `swipe` → [540, 1500] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [540, 1600] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [900, 736] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `semplo.ic327.skin` / `mrWz` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `semplo.ic327.skin` / `mrWz` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `semplo.ic327.skin` / `mrWz` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`semplo.ic327.skin/mrWz`)**: (空文本)
- **Step 7 (`semplo.ic327.skin/mrWz`)**: (空文本)
- **Step 8 (`semplo.ic327.skin/mrWz`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：入口为 Nexus 桌面，未在应用抽屉找到目标后，通过静态引导回退进入 semplo.ic327.skin 的 mrWz 空白页，并连续跳转多个内部或后台 Activity；全程未出现授权弹窗、通知横幅或可见诱导话术，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | Nexus 桌面主页，显示“应用列表、消息、Chrome、搜索、语音搜索”等；点击“应用列表”后未跳转，无通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为 Nexus 桌面主页，含“应用列表、消息、Chrome、搜索”等；因按钮无响应改上滑打开抽屉，页面未变，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉已打开，显示日历、相机、Chrome、时钟、联系人等；目标应用未出现，上滑继续滚动，无通知横幅与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍为应用抽屉列表页，含日历、相机、Chrome、时钟、联系人等；目标仍不可见，左滑翻页未发现目标，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉列表页仍显示常用应用；未点中目标后触发静态引导回退，跳转至本应用 .mrWz，界面无文字，无通知/遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: mrWz** | 跳转至 semplo.ic327.skin 的 mrWz 空界面，无可见文字与控件；随即静态引导跳转 .H8C0JkV，无通知横幅或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: mrWz** | 仍为 mrWz 空白页，无可见文案与按钮；静态引导继续跳转至 .ZTx，未出现授权弹窗、通知横幅或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: mrWz** | mrWz 空白页无可见文本；静态引导跳转至系统 WorkManager 的 ConstraintProxy$Batter 组件，无授权提示、通知或遮罩。 | `step_08_screen.png` |
