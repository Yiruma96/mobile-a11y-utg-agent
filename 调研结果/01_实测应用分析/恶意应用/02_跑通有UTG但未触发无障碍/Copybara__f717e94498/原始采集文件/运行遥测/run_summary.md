# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:57:31
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.dohpgfr.qarthpc`（静态标签：`malicious` / `Copybara` / 静态可见性：`clear`）
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

> **全链路总结**：样本 com.dohpgfr.qarthpc 启动后未展示自身界面，始终停留在 NexusLauncherActivity 桌面启动器；测试依次尝试包名直启及静态跳转 service2_BR、AdminReceiver2、service1_BR、notificationservice_BR、startatbootreceiver，均未出现授权弹窗、通知横幅或遮罩，未观察到诱导话术，授权/拒权链路未完成。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器，显示应用列表、11月25日星期三、信息、Chrome、搜索、语音搜索；尝试启动目标应用未成功，仍停留桌面。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面启动器同一页面，含应用列表、日期、信息、Chrome、搜索等；改用包名直启目标应用，应用未启动，无新界面。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 仍为桌面启动器；尝试静态跳转 service2_BR 组件，页面未变，无目标界面、通知横幅或遮罩，未见授权弹窗。 | `step_03_screen.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面启动器页面；点击“应用列表”入口（坐标540,1688），拟手动查找目标应用，仍停留桌面，无通知或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面启动器；静态跳转 AdminReceiver2 组件后无界面变化，仍显示应用列表与搜索等，无设备管理授权弹窗。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面启动器未变；静态跳转 service1_BR 组件后仍无目标页面，无通知横幅、悬浮遮罩或授权提示，交互无可见结果。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍为桌面启动器；静态跳转 notificationservice_BR 后未出现通知授权界面或通知横幅，仅见应用列表、搜索等桌面元素。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 仍为桌面启动器；静态跳转 startatbootreceiver 组件后页面无变化，无开机自启授权提示、通知或遮罩，未进入应用界面。 | `step_08_screen.png` |
