# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:25:47
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.buzbuz.smartautoclicker`（静态标签：`benign` / `自动化与跳广告` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.buzbuz.smartautoclicker` / `ScenarioActivity` | `-` | 7 | 115 / 否 | `click` → [3] Button text="Create a scenario" id=empty_create_but | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.buzbuz.smartautoclicker` / `ScenarioActivity` | `-` | 11 | 167 / 否 | `click` → [4] Button id=button_save (click) center=(991,1124) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.buzbuz.smartautoclicker` / `ScenarioActivity` | `-` | 16 | 93 / 否 | `click` → [15] Button id=button_start (click) center=(925,710) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.buzbuz.smartautoclicker` / `ScenarioActivity` | `-` | 4 | 222 / 否 | `click` → [3] Button text="Request permission" id=button_request_ | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$OverlaySettingsActivity` | `-` | 31 | 156 / 否 | `click` → [17] LinearLayout desc="Klick'r" (click) center=(540,11 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `SubSettings` | `-` | 10 | 228 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `SubSettings` | `-` | 10 | 228 / 否 | `click` → [1] ImageButton desc="Back" (click) center=(77,160) | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.buzbuz.smartautoclicker` / `ScenarioActivity` | `-` | 4 | 365 / 否 | `click` → [3] Button text="Request permission" id=button_request_ | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.buzbuz.smartautoclicker/ScenarioActivity`)**: `Create your first scenario and start automatizing tasks` | `Create a scenario` | `Scenarios` | `Import` | `Export` | `Settings`
- **Step 2 (`com.buzbuz.smartautoclicker/ScenarioActivity`)**: `New scenario` | `Default name` | `Simple` | `The regular auto clicker experience. Simply place click` | `Smart` | `Use image detection to create complex use cases.`
- **Step 3 (`com.buzbuz.smartautoclicker/ScenarioActivity`)**: `Scenarios` | `Import` | `Search` | `Export` | `Settings` | `Name` | `Recent` | `Uses` | `Smart` | `Simple`
- **Step 4 (`com.buzbuz.smartautoclicker/ScenarioActivity`)**: `Overlay` | `The overlay permission is required in order to show Kli` | `Request permission` | `Deny`
- **Step 5 (`com.android.settings/Settings$OverlaySettingsActivity`)**: `Back` | `Display over other apps` | `Search` | `More options` | `Android Auto` | `Allowed` | `Digital Wellbeing` | `Google` | `Google Play services` | `Klick'r`
- **Step 6 (`com.android.settings/SubSettings`)**: `Back` | `Display over other apps` | `Search settings` | `Klick'r` | `4.1.2` | `Allow display over other apps` | `Allow this app to display on top of other apps you’re u`
- **Step 7 (`com.android.settings/SubSettings`)**: `Back` | `Display over other apps` | `Search settings` | `Klick'r` | `4.1.2` | `Allow display over other apps` | `Allow this app to display on top of other apps you’re u`
- **Step 8 (`com.buzbuz.smartautoclicker/ScenarioActivity`)**: `Accessibility service` | `The accessibility service permission allows Klick'r to ` | `Request permission` | `Deny`

## 中文逐页引导链路解读

> **全链路总结**：从空场景入口创建“Default name”场景，运行后依次引导开启系统悬浮窗与无障碍服务；权限说明明确用途并声明不收集数据，提供拒绝但拒权路径未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “创建你的第一个场景，开始让手机上的任务自动化”（Step 1 首页空态）
- 英文 -> “悬浮窗权限用于在其他应用上显示Klick'r界面，便于不中断地配置场景”（Step 4 悬浮窗说明）
- 英文系统 -> “允许此应用显示在其他应用上层，它将能查看你点击的位置或更改屏幕显示内容”（Step 6 系统权限详情）
- 英文 -> “无障碍权限用于在设备屏幕执行手势，Klick'r不收集数据”（Step 8 无障碍说明）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ScenarioActivity** | 场景列表空态，提示创建首个场景并在手机上自动化任务；点击“Create a scenario”进入新建，未见通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: ScenarioActivity** | 新建场景弹窗，选择Simple（普通自动点击）或Smart（图像识别）；本步点击保存创建“Default name”，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: ScenarioActivity** | 返回场景列表，已出现“Default name”条目及Recent/Uses；点击条目右侧开始按钮运行场景并触发权限检查。 | `step_03_action.png` |
| 4 | **Step 4: ScenarioActivity** | 应用悬浮窗权限说明称需在其他应用上显示Klick'r界面以便配置；点击“Request permission”转系统设置，有Deny。 | `step_04_action.png` |
| 5 | **Step 5: Settings$OverlaySettingsAc** | 系统“Display over other apps”列表，Klick'r标为Not allowed；点击Klick'r条目进入其悬浮窗开关页，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: SubSettings** | Klick'r悬浮窗权限详情，开关未勾选；系统说明可查看点击位置或更改屏幕内容，本步点击开关授权。 | `step_06_action.png` |
| 7 | **Step 7: SubSettings** | 同一权限详情页，悬浮窗开关已开启；点击左上角Back返回Klick'r，继续无障碍服务授权流程。 | `step_07_action.png` |
| 8 | **Step 8: ScenarioActivity** | Klick'r弹出无障碍服务说明，称用于执行屏幕手势且不收集数据；点击“Request permission”跳转系统无障碍设置，有Deny。 | `step_08_action.png` |
