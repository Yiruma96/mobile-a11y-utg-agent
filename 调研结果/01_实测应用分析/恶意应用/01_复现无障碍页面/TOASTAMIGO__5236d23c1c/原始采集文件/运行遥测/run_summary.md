# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:37:54
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.agomi.applocker`（静态标签：`malicious` / `TOASTAMIGO` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.agomi.applocker/com.goami.applocker.AppLocker.ApplicationListActivity` | hooks=`[]` | overlays=`0` | texts=`Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm`
- **Back 后 +5.5s**：`com.agomi.applocker/com.goami.applocker.AppLocker.ApplicationListActivity` | hooks=`[]` | overlays=`0` | texts=`Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm`
- **Back 后 +10.5s**：`com.agomi.applocker/com.goami.applocker.AppLocker.ApplicationListActivity` | hooks=`[]` | overlays=`0` | texts=`Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.agomi.applocker` / `ApplicationListActivity` | `-` | 4 | 130 / 否 | `click` → [4] TextView text="Confirm" id=btn_ok (click) center=(8 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 214 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.agomi.applocker/ApplicationListActivity`)**: `Attention` | `This device version is above Android 4.0.3 .Please Go S` | `Cancel` | `Confirm`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Smart AppLocker` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用启动即在应用列表页弹出英文Attention对话框，以Android版本为由引导前往无障碍服务开启App Locker；进入系统无障碍设置与服务详情后触发全控权限警告，拒绝授权后返回并自动重弹同一诱导框，形成循环施压。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 「Attention」（启动页/拒权后的诱导弹窗标题）
- 英文 -> 「本设备版本高于Android 4.0.3，请前往设置→无障碍服务→App Locker并开启」（启动页/拒权后的ApplicationListActivity）
- 英文 -> 「允许Smart AppLocker完全控制您的设备？」（系统无障碍授权警告页）
- 英文 -> 「完全控制适合有辅助需求的应用，但不适合大多数应用」（系统警告说明）
- 英文 -> 「查看并控制屏幕：可读取屏幕上所有内容并叠加显示在其他应用上」（系统警告权限说明）
- 英文 -> 「查看并执行操作：可跟踪与应用的交互或硬件传感器，并代表您操作应用」（系统警告权限说明）
- 英文 -> 「该服务用于Android 4.0.3及以上轻松锁定应用」（服务详情页说明）
- 英文占位 -> 「AppLocker / 服务正在运行」（全局通知横幅，贯穿各页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ApplicationListActivity** | 启动页Attention框诱导去无障碍开启App Locker；点Confirm后通知栏常驻服务运行中。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳至系统无障碍设置，Smart AppLocker显示Off；捕获设置钩子后终止，通知栏仍显示服务运行中。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针仍在无障碍设置页，无可读文本、遮罩为0；仅见AppLocker服务运行中通知。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针仍停留无障碍设置页，无新增文本与遮罩；通知栏持续显示AppLocker服务运行中。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | Smart AppLocker服务详情含Use开关、快捷键/音量键选项，英文说明称用于Android 4.0.3以上轻松锁应用。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告询问是否允许Smart AppLocker完全控制设备，列明可读屏、叠加显示并代为操作；本步检查未点允许/拒绝。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权后2秒返回应用列表页，原Attention诱导框自动重弹，仍要求去无障碍开启App Locker；通知栏服务运行中。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍返回并重弹Attention诱导框，要求去无障碍开启App Locker；通知栏服务运行中，呈循环施压。 | `step_02_refusal_10500ms_screen.png` |
