# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:23:46
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.jejisinepebuxo.cunenu`（静态标签：`malicious` / `Hook` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 203 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `king` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用通过常驻通知「String (king) / String (Enable king)」将用户引向系统无障碍设置，并在「king」服务详情与完全控制授权警告中推动开启无障碍权限；用户拒绝后返回桌面，通知仍保留，表现为优雅停留或降级而非强制弹窗。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文：String (king) / String (Enable king) -> 中文：king / 启用 king（通知横幅，贯穿无障碍列表、服务详情、授权弹窗与返回桌面）
- 英文：Use king -> 中文：使用 king（服务详情页）
- 英文：king shortcut / Hold volume keys / Shortcut settings -> 中文：king 快捷键 / 长按音量键 / 快捷键设置（服务详情页）
- 英文：If accessibility permission has been on, please turn off then turn on. -> 中文：若无障碍权限曾开启，请先关闭再重新开启（服务详情页）
- 英文：Allow king to have full control of your device? -> 中文：允许 king 完全控制您的设备？（系统警告弹窗）
- 英文：Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 中文：完全控制适合辅助无障碍需求的应用，但不适合多数应用（系统警告弹窗）
- 英文：View and control screen / It can read all content on the screen and display content over other apps. -> 中文：查看并控制屏幕 / 可读取屏幕全部内容并覆盖显示在其他应用上（系统警告弹窗）
- 英文：View and perform actions / It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 中文：查看并执行操作 / 可追踪交互并代表您操作应用（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表：已下载应用「king」显示为关闭，通知横幅提示「启用 king」；采集到 Hook 与探针后终止，遮罩数为0。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 同一无障碍列表跳后0.8秒探针：页面文本为空，应用通知「启用 king」仍常驻，无遮罩，继续等待。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒再次探针：无障碍列表仍无可见控件文本，通知持续悬挂且遮罩为0，未发生授权或跳转。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：显示「king」「使用 king」、快捷键与音量键选项，并提示权限曾开启需关闭再开启；通知仍在，本步检查详情。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统授权警告：询问是否允许 king 完全控制设备，列明可读屏、覆盖显示及代操作，提供允许/拒绝；本步仅检查弹窗。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒绝后返回桌面：显示应用列表、天气与常用图标，通知「启用 king」未消失，无遮罩，结果记为优雅停留或降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面：界面与通知「启用 king」保持，无弹窗或遮罩，应用未强制牵引，呈优雅降级。 | `step_01_refusal_10500ms_screen.png` |
