# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:34:03
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.amputate.volunteer`（静态标签：`malicious` / `Asacub` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 215 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Основнoй процесс` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以俄文通知“主进程”谎称系统异常，诱导进入无障碍设置并开启“主进程”服务；在系统完全控制警告处点Deny后，应用未崩溃而退回桌面，呈优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 俄文 -> “系统运行不正确，您需要为‘主进程’开启统计访问权限”（无障碍列表及服务详情页顶部常驻通知，制造系统故障紧迫感）
- 俄文/英文混排 -> “主进程”被用作无障碍服务名称，伪装为系统核心进程（无障碍列表、服务详情、警告弹窗）
- 俄文 -> “使用主进程”“主进程快捷方式”“按住音量键”“快捷方式设置”“未提供描述”（无障碍服务详情页）
- 英文 -> “允许主进程完全控制您的设备？”并称完全控制适合无障碍应用、可查看控制屏幕、读取所有内容、跟踪交互并代为操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍列表：下载应用中俄文“主进程”为Off，通知谎称系统异常诱导开启统计权限；捕获无障碍钩子后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍在无障碍列表，文本为空且无遮罩；俄文“主进程”通知持续显示，等待未见变化。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒探针：无障碍列表仍无文本、无遮罩，俄文通知常驻；等待后无新页面或弹窗出现。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 无障碍服务详情页：俄文“主进程”含“使用主进程”、快捷方式与音量键选项，描述为空；检查详情未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统完全控制警告弹窗：英文询问是否允许“主进程”完全控制设备，列明读屏与代操作风险；本步检查后点Deny。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2秒：返回Nexus桌面，显示应用列表、日期与搜索；俄文通知仍在，无遮罩，结果为优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒：仍在Nexus桌面，界面未变、俄文通知持续；应用未崩溃或强退，保持优雅降级状态。 | `step_01_refusal_10500ms_screen.png` |
