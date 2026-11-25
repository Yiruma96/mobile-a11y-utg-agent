# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:15:07
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.gejalevubakupa.sugi`（静态标签：`malicious` / `Ermac` / 静态可见性：`partial_dynamic_or_remote`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `HookAPPService` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用在系统无障碍列表与详情页用 HookAPPService 和“启用 Chrome 更新服务”通知诱导开启无障碍，并提示关闭再开启权限；系统高危警告下拒绝后返回桌面，通知仍驻留但未见强退，呈优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文通知 -> 标题“String (HookAPP)”、正文“String (Enable Chrome Update Service)”，核心意译为伪装 HookAPP 并称“启用 Chrome 更新服务”（无障碍列表/详情及拒权后持续）。
- 英文 -> “Use HookAPPService”，核心意译为使用 HookAPPService 无障碍服务（服务详情页）。
- 英文 -> “HookAPPService shortcut / Hold volume keys / Shortcut settings”，核心意译为可设 HookAPPService 快捷方式并按住音量键触发（服务详情页）。
- 英文 -> “If accessibility permission has been on, please turn off then turn on.”，核心意译为若无障碍权限已开启请先关闭再重新开启（服务详情页）。
- 英文 -> “Allow HookAPPService to have full control of your device?”，核心意译为允许 HookAPPService 完全控制你的设备（系统警告弹窗）。
- 英文 -> “View and control screen / View and perform actions”，核心意译为可查看并控制屏幕、可代为查看并执行操作（系统警告弹窗）。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍列表页，已下载应用 HookAPPService 显示“关闭”；顶部应用通知称“启用 Chrome 更新服务”，遮罩0，命中探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍在系统无障碍设置页，文本未采集；应用通知“HookAPP/启用 Chrome 更新服务”持续，遮罩0，执行等待。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍停留系统无障碍设置页，无可见文本；应用通知“HookAPP/启用 Chrome 更新服务”仍在，遮罩0，继续等待。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | HookAPPService 服务详情页，含“使用服务/快捷方式/按住音量键”等选项，并提示权限开启后需关闭再开启；通知仍在，遮罩0，执行检查。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗，警告 HookAPPService 将“完全控制设备”，可读屏并代操作；底部 Allow/Deny，通知仍在、遮罩0，本步检查后拒绝。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后返回桌面：显示应用列表、日期、天气及 Messages/Chrome 图标；应用通知仍驻留，遮罩0，未见强退，呈优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面，应用列表、日期、天气与 Chrome 图标不变；应用通知持续，遮罩0，仍无异常或强退，维持优雅停留/降级。 | `step_01_refusal_10500ms_screen.png` |
