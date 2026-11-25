# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:09:42
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`li.songe.gkd`（静态标签：`benign` / `自动化与跳广告` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 6 步，UTG 唯一节点 `8` 个，有向边 `10` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 6 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_06_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`li.songe.gkd/li.gkd.app.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Accessibility / Manual start / Grant accessibility permission once / Authorization is required again after accessibility is stopped / Enable accessibility`
- **Back 后 +5.5s**：`li.songe.gkd/li.gkd.app.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Accessibility / Manual start / Grant accessibility permission once / Authorization is required again after accessibility is stopped / Enable accessibility`
- **Back 后 +10.5s**：`li.songe.gkd/li.gkd.app.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Accessibility / Manual start / Grant accessibility permission once / Authorization is required again after accessibility is stopped / Enable accessibility`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `li.songe.gkd` / `MainActivity` | `-` | 6 | 136 / 否 | `click` → [6] TextView text="Agree" center=(829,1297) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `li.songe.gkd` / `MainActivity` | `-` | 6 | 160 / 否 | `click` → [6] TextView text="Agree" center=(829,1324) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `li.songe.gkd` / `MainActivity` | `-` | 30 | 390 / 否 | `click` → [7] View (click) center=(540,780) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `li.songe.gkd` / `MainActivity` | `-` | 29 | 564 / 否 | `click` → [8] TextView text="Enable accessibility" center=(339,75 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `li.songe.gkd` / `MainActivity` | `-` | 6 | 186 / 否 | `click` → [6] TextView text="Go" center=(834,1407) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 30 | 239 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_06_layout.xml` + `step_06_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`li.songe.gkd/MainActivity`)**: `Usage notice` | `Welcome to GKD! To continue, read and accept the User a` | `Disagree` | `Agree`
- **Step 2 (`li.songe.gkd/MainActivity`)**: `About accessibility` | `GKD uses the system Accessibility API to read screen in` | `Disagree` | `Agree`
- **Step 3 (`li.songe.gkd/MainActivity`)**: `Ignore battery optimization` | `Android may freeze GKD in the background and delay rule` | `Service status` | `Accessibility not authorized` | `Working mode` | `Accessibility` | `Persistent notification` | `Show service status and statistics` | `History` | `Trigger history`
- **Step 4 (`li.songe.gkd/MainActivity`)**: `Accessibility` | `Manual start` | `Grant accessibility permission once` | `Authorization is required again after accessibility is ` | `Enable accessibility` | `View help` | `Automatic start` | `Grant write secure settings permission permanently` | `Allow the app to turn accessibility on and off` | `Touch optimization`
- **Step 5 (`li.songe.gkd/MainActivity`)**: `Enable GKD accessibility` | `System accessibility settings will open. Follow these s` | `Cancel` | `Go`
- **Step 6 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `GKD` | `Off` | `GKD companion service (do not enable manually)` | `GKD touch optimization (do not enable manually)` | `SCREEN READERS` | `Text-to-speech output`

## 中文逐页引导链路解读

> **全链路总结**：GKD 启动后依次弹出「使用须知」与「无障碍说明」两个同意弹窗，再引导用户在主页开启无障碍、写入安全设置与触摸优化特权，并跳转系统无障碍列表；用户在被拒后（系统高危警告选 Deny）返回应用，仍被卡在要求授权的主页，未能进入任何正常功能，判定为 TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 「使用须知：欢迎使用 GKD！继续前请阅读并接受用户协议与隐私政策，请仔细阅读。」（Step1 使用须知弹窗，仅“不同意/同意”两键）
- 英文 -> 「关于无障碍：GKD 使用系统无障碍 API 读取屏幕信息，并依据你的订阅规则执行自动化操作。」（Step2 无障碍说明弹窗）
- 英文 -> 「忽略电池优化：Android 可能在后臺冻结 GKD 并延迟规则触发」——以功能失效为由施压（Step3 主页提示）
- 英文 -> 「自动启动：永久授予写入安全设置权限，允许应用开启和关闭无障碍」——以便利换取常驻高权限（Step4）
- 英文 -> 「启用 GKD 无障碍：将打开系统无障碍设置，依次为 1 在服务列表找到 GKD 2 打开并确认系统提示 3 返回 GKD」（Step5 引导弹窗）
- 英文 -> 「允许 GKD 完全控制你的设备？它可读取屏幕全部内容、跟踪你的交互并代替你操作应用。」（系统高危授权警告）
- 英文 -> 「GKD 伴生服务（请勿手动启用）」「GKD 触摸优化（请勿手动启用）」（系统无障碍列表项，暗示另有隐藏开关）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 启动后首个「使用须知」弹窗，英文要求阅读并同意用户协议与隐私政策，仅「不同意/同意」；本步点击「同意」继续。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 第二个「关于无障碍」弹窗，说明 GKD 将用系统无障碍 API 读屏并按订阅规则自动操作；本步点击「同意」进入主页。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | GKD 主页：服务状态显示「无障碍未授权」，并有忽略电池优化提示与工作模式、历史等入口；本步点击「工作模式」行。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 无障碍设置页：手动启动需单次授权，自动启动要求永久写入安全设置，触摸优化需特权服务；本步点击「启用无障碍」。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 应用内引导弹窗称即将打开系统无障碍设置，并列三步操作，只有「取消/前往」；本步点「前往」跳转系统设置。 | `step_05_action.png` |
| 6 | **Step 6: [无障碍列表页]** | 跳至系统无障碍列表，GKD 显示「关闭」，另有两项标注「请勿手动启用」的伴生服务；采到无障碍设置钩子后自动终止。 | `step_06_screen.png` |
| 7 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停在系统无障碍设置列表，无弹窗、无遮罩、无通知横幅，界面无任何变化。 | `step_06_probe_800ms_screen.png` |
| 8 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：页面依旧为系统无障碍列表，未出现遮罩或通知，等待期间也未见自动开启开关的动作。 | `step_06_probe_2000ms_screen.png` |
| 9 | **服务详情页** | GKD 服务详情页：「使用 GKD」总开关为关闭，选项含 GKD 快捷方式；下方英文说明称可基于高级选择器与订阅规则自定义点击屏幕。 | `step_06_service_detail_screen.png` |
| 10 | **系统警告弹窗(点Deny)** | 系统高危授权警告：询问是否允许 GKD 完全控制设备，列明可读取全部屏幕内容、跟踪交互并代为操作；本步查看后选择拒绝。 | `step_06_system_warning_screen.png` |
| 11 | **拒权返回 +2.0s** | 拒权返回应用 2 秒：回到无障碍设置页，「启用无障碍」入口仍醒目存在，授权状态未变，仍被判定停留在诱导页。 | `step_06_refusal_2000ms_screen.png` |
| 12 | **拒权返回 +10.5s** | 拒权后 10.5 秒：界面与 2 秒时完全一致，应用未放行也未给替代路径，持续卡在要求授权的诱导界面（TRAPPED_ON_LURE_SCREEN）。 | `step_06_refusal_10500ms_screen.png` |
