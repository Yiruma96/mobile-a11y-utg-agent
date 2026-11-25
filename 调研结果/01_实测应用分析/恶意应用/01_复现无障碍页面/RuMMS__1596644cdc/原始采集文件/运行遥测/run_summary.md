# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:29:51
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`org.day.cold`（静态标签：`malicious` / `RuMMS` / 静态可见性：`clear`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 215 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Оcновной прoцесc` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用将自身伪装为“主进程”无障碍服务，引导用户进入系统无障碍设置，并通过俄文通知谎称系统异常、要求开启统计/无障碍权限；在系统全权授权弹窗点 Deny 后返回桌面，未出现遮罩或崩溃，表现为优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 俄文通知 -> “系统运行不正常，您需要为‘主进程’开启统计访问权限”（无障碍列表、服务详情、授权弹窗及桌面通知横幅持续显示）
- 俄文/拉丁混排服务名 -> “主进程”（无障碍列表、服务详情、授权弹窗，伪装成系统进程）
- 英文 -> “未提供描述。”（服务详情页，刻意隐藏无障碍服务真实用途）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍列表，下载应用显示伪装名“主进程”；俄文通知谎称系统异常、要求开启统计权限，捕获钩子后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍在无障碍设置页，界面文本为空；无遮罩，俄文“主进程”通知横幅持续显示，系统异常话术未消失。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针，页面仍为无障碍设置且无可见文本；遮罩数为0，俄文通知继续谎称系统异常并要求开启统计权限。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | “主进程”无障碍服务详情页：显示“使用主进程”、快捷键选项及“未提供描述”；无遮罩，俄文通知横幅仍在。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 全权授权弹窗：警告“主进程”可完全控制设备、读屏、悬浮显示并跟踪/代为操作；本步点 Deny，通知横幅仍在。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒绝后2.0秒回到桌面，显示应用列表、天气与搜索；无遮罩，俄文“主进程”通知仍在，应用未崩溃，呈优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒绝后10.5秒桌面保持正常，无新弹窗或遮罩；俄文“主进程”通知继续谎称系统异常并要求开统计权限，表现优雅降级。 | `step_01_refusal_10500ms_screen.png` |
