# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:23:35
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.frmsena.mwhsgxz`（静态标签：`malicious` / `Copybara` / 静态可见性：`clear`）
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

> **全链路总结**：应用从桌面入口启动后始终未进入 Copybara 页面：按包名启动、点击应用列表及多次静态组件跳转均停留在 NexusLauncher，另见反模拟器提示“App can't work on Emulators”。未观察到实际诱导界面、通知横幅、遮罩或授权/拒权结果。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “应用无法在模拟器上运行”（Step 2 启动重试时出现；属反模拟器/环境检测提示，非用户诱导话术）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | Nexus 桌面，含应用列表、11月25日星期三、信息、Chrome、搜索/语音搜索；按包名启动 Copybara 未切换页面，仍无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为 Nexus 桌面；启动后疑似提示“App can't work on Emulators”（应用无法在模拟器运行），重试后仍未进入目标页，无横幅/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 仍为 Nexus 桌面，显示应用列表、日期、信息、Chrome、搜索等；静态跳转至 service2_BR 后台组件未加载新界面，无通知/遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍为 Nexus 桌面；点击“Apps list（应用列表）”后未见抽屉或目标页变化，仍显示日期、信息、Chrome、搜索等，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 仍为 Nexus 桌面；静态跳转至 AdminReceiver2 设备管理组件未呈现页面，桌面日期、信息、Chrome、搜索不变，无通知/遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍为 Nexus 桌面；静态跳转至 service1_BR 后台服务未切换界面，应用列表、日期、信息、Chrome、搜索保持原样，无通知/遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍为 Nexus 桌面；静态跳转至 notificationservice_BR 未显示通知页，界面仍为应用列表、日期、信息、Chrome、搜索，无横幅/遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 仍为 Nexus 桌面；静态跳转至 startatbootreceiver 开机接收器未加载界面，仍见应用列表、日期、信息、Chrome、搜索，无通知/遮罩。 | `step_08_screen.png` |
