# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:13:07
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.tower.revolution`（静态标签：`malicious` / `RuMMS` / 静态可见性：`clear`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 216 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Систeмный прoцеcc` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用通过伪装成俄语“系统进程”的通知，谎称系统异常需开启使用情况统计/无障碍权限，引导用户进入无障碍列表与服务详情，并在全控警告弹窗处被拒；拒权后回到桌面，应用未崩溃而保持/降级驻留（GRACEFUL_STAY_OR_DEGRADE）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 俄语 -> “系统运行不正常，您需要为‘系统进程’开启使用情况统计访问权限”（伪装系统进程的通知横幅，在无障碍列表、服务详情、警告弹窗及桌面持续显示）
- 英语 -> “允许‘系统进程’完全控制您的设备吗？可查看并控制屏幕、读取屏幕全部内容并覆盖显示、跟踪交互并代您操作应用。”（系统无障碍全控警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页，下载应用含俄语伪装“系统进程”；通知横幅称系统异常需开统计权限，本步捕获无障碍设置钩子后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留无障碍列表，页面文本为空；俄语伪装“系统进程”通知横幅持续显示，无遮罩，等待未见弹窗。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2秒探针，仍为无障碍列表空文本页；俄语伪装“系统进程”通知横幅未消失，无遮罩与弹窗，继续等待。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页，标题为俄语“系统进程”，含启用开关及快捷键/音量键选项；通知横幅仍称系统异常需开统计权限，本步仅查看详情。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统全控警告弹窗：问是否允许俄语“系统进程”完全控制设备，列明读屏、覆盖显示及代操作；含Allow/Deny，本步查看未授权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 点Deny拒权后2秒回到桌面，显示应用列表、日期与常用图标；俄语伪装“系统进程”通知仍在，应用未崩溃，进入保持/降级状态。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面，页面无变化且无遮罩；俄语伪装“系统进程”通知持续存在，应用保持/降级驻留，未见再弹授权诱导。 | `step_01_refusal_10500ms_screen.png` |
