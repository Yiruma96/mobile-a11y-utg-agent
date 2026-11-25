# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:34:03
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`dev.cena.whyiamhere`（静态标签：`benign` / `专注自律与防沉迷管控` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`dev.cena.whyiamhere/dev.cena.whyiamhere.SettingsActivity` | hooks=`[]` | overlays=`0` | texts=`Why am I here? / Open apps with a purpose. Make time for what matters. / Accessibility service / Disabled — the goal form and widget are not active / The service detects the open app, shows your goal, and returns home when time runs out. Your data stays on your phone. Text inside other apps is not read.`
- **Back 后 +5.5s**：`dev.cena.whyiamhere/dev.cena.whyiamhere.SettingsActivity` | hooks=`[]` | overlays=`0` | texts=`Why am I here? / Open apps with a purpose. Make time for what matters. / Accessibility service / Disabled — the goal form and widget are not active / The service detects the open app, shows your goal, and returns home when time runs out. Your data stays on your phone. Text inside other apps is not read.`
- **Back 后 +10.5s**：`dev.cena.whyiamhere/dev.cena.whyiamhere.SettingsActivity` | hooks=`[]` | overlays=`0` | texts=`Why am I here? / Open apps with a purpose. Make time for what matters. / Accessibility service / Disabled — the goal form and widget are not active / The service detects the open app, shows your goal, and returns home when time runs out. Your data stays on your phone. Text inside other apps is not read.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `dev.cena.whyiamhere` / `SettingsActivity` | `-` | 20 | 685 / 否 | `click` → [8] TextView text="Open service settings" center=(352,1 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`dev.cena.whyiamhere/SettingsActivity`)**: `Why am I here?` | `Open apps with a purpose. Make time for what matters.` | `Accessibility service` | `Disabled — the goal form and widget are not active` | `The service detects the open app, shows your goal, and ` | `Open service settings` | `Android 13+: if the switch is unavailable, open App inf` | `If the service stops working, allow autostart and remov` | `Warning before the session ends` | `60`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Why am I here?` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口设置页以“带着目的打开应用”引导开启无障碍服务，跳转系统无障碍列表/服务详情并触发全控制警告；用户点拒绝后仍返回原设置页反复停留，无取消或退出路径（TRAPPED_ON_LURE_SCREEN），探针期间无通知与遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文：Open apps with a purpose. Make time for what matters. -> 带着目的打开应用，把时间留给重要的事（入口设置页/拒权返回页）
- 英文：Disabled — the goal form and widget are not active -> 无障碍服务已禁用，目标表单和小组件不生效（入口设置页/拒权返回页）
- 英文：The service detects the open app, shows your goal, and returns home when time runs out. Your data stays on your phone. Text inside other apps is not read. -> 服务检测当前打开应用、显示目标并在时间结束时回桌面；数据留在本机，不读取其他应用内文字（入口设置页/服务详情页）
- 英文：Android 13+: if the switch is unavailable, open App info → ⋮ → Allow restricted settings. Names may differ on your phone. -> Android 13+若开关不可用，去应用信息→⋮→允许受限设置，名称可能因手机而异（入口设置页）
- 英文：If the service stops working, allow autostart and remove battery restrictions in your phone settings. -> 若服务停止工作，请在手机设置中允许自启动并移除电池限制（入口设置页）
- 英文：Asks for a goal when you open selected apps, reminds you of the time, and returns to the home screen when the session ends. Uses the package name of the active window. Screen text, passwords, and messages are not stored or transmitted. -> 打开选定应用时询问目标、提醒时长并在会话结束时回桌面；仅使用当前窗口包名，不存储或传输屏幕文字、密码和消息（服务详情页）
- 英文：Allow Why am I here? to have full control of your device? Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 允许 Why am I here? 完全控制设备？完全控制适用于辅助无障碍需求的应用，不适用于多数应用（系统警告弹窗）
- 英文：View and control screen / View and perform actions -> 可查看并控制屏幕 / 可查看并执行操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: SettingsActivity** | 入口设置页，标题‘Why am I here?’，以‘带着目的打开应用’引导；显示无障碍服务禁用，本步点‘Open service settings’跳系统无障碍设置，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页，DOWNLOADED APPS 下可见‘Why am I here?’状态为 Off；本步采集无障碍设置 Hook/探针后自动终止，无通知/遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 系统无障碍列表页跳后0.8秒探针：仍在 Settings$AccessibilitySettingsActivity，无可见文本变化，遮罩数为0，仅等待未交互。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍停留系统无障碍列表页，无新增文本、通知或遮罩，仅等待，未触发授权开关或页面跳转。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页：显示‘Use Why am I here?’与选项，‘Why am I here? shortcut’为 Off；说明会询问目标、提醒时长并回桌面，仅用包名不存屏幕文字，本步查看详情/警告。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统全控制警告弹窗：询问是否允许 Why am I here? 完全控制设备，列明可查看控制屏幕、查看并执行操作；本步查看后点 Deny 拒绝，遮罩0。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 点 Deny 后2秒返回应用设置页，服务仍 Disabled，继续显示开启服务与 Android 13+ 受限设置指引；无取消/退出，标记 TRAPPED_ON_LURE_SCREEN，无通知/遮罩。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍困在应用设置页，重复‘Open service settings’与自启动/电池限制提示，服务保持禁用；无取消/退出，持续 TRAPPED_ON_LURE_SCREEN，无通知/遮罩。 | `step_02_refusal_10500ms_screen.png` |
