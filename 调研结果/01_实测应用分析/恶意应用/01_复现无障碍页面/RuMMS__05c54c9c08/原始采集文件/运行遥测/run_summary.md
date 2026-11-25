# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:28:45
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`ru.calendar.pen`（静态标签：`malicious` / `RuMMS` / 静态可见性：`clear`）
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

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Систeмный прoцecc` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用 ru.calendar.pen 先以俄文常驻通知冒充“系统进程”，谎称“系统运行异常，需为系统进程开启使用情况访问权限”，把用户引到系统无障碍设置页，并尝试为其伪装服务开启无障碍权限；系统弹出可读屏、可代替用户操作的全权警告后，用户点击 Deny 拒绝授权，应用没有崩溃，也没有再次弹窗，而是静默退回桌面，仅保留通知横幅，等待后续诱导，表现为保活降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 俄语 -> 『系统运行不正常，您需要为“系统进程”开启使用情况（统计）访问权限』（无障碍设置列表页、服务详情页常驻通知横幅，反复出现）
- 俄语 -> 服务名『Систeмный прoцecc』意为“系统进程”，冒充系统组件以降低戒心（无障碍列表页与服务详情页条目）
- 英语 -> 『未提供任何描述』（No description provided.），伪装服务缺少说明，与真实系统应用不符（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页：DOWNLOADED APPS 下出现俄文『系统进程』伪装服务且状态为 Off，通知横幅同步诱导开启统计权限；本步捕获无障碍钩子后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后 0.8 秒仍停在无障碍设置页，界面文本为空（已被清空），俄文“系统运行异常需开权限”通知横幅持续挂着，无遮罩层。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后 2.0 秒同前：无障碍设置页无新文本、无遮罩，伪系统通知横幅仍在，说明诱导依赖通知而非界面覆盖。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 伪装服务的无障碍详情页：标题为俄文『系统进程』，Use 开关未启用，选项仅有快捷键与音量键，描述为“未提供任何描述”，显然并非系统组件。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统全权控制警告弹窗：提示该服务可读屏、可覆盖其他应用并代替用户操作；人工检视后选择 Deny 拒绝，是关键授权拦截点。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后 2 秒已回到 Nexus 桌面，应用没有二次强扰弹窗，仅保留俄文伪系统通知横幅，表现为静默保活降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后 10.5 秒仍停留在桌面，无二次弹窗与遮罩，俄文伪『系统进程』通知横幅常驻，疑似持久通知等待再次诱导。 | `step_01_refusal_10500ms_screen.png` |
