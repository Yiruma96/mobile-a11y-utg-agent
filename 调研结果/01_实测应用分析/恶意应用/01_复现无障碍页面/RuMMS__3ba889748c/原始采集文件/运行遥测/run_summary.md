# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:37:46
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`ru.shift.element`（静态标签：`malicious` / `RuMMS` / 静态可见性：`clear`）
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

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Оcновнoй прoцeсс` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以俄语通知谎称系统异常，诱导用户进入无障碍设置启用名为“主进程”的服务；在系统全控制警告处拒绝后回到桌面，未崩溃或再弹窗，表现为优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 俄语 -> “系统运行不正常，您需要为‘主进程’启用使用情况统计访问权限”（通知横幅，贯穿无障碍列表页与服务详情页）
- 英语 -> “允许‘主进程’完全控制您的设备吗？”并称可查看/控制屏幕、读取全部内容并代为操作（系统全控制授权弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页，俄语通知谎称系统异常需为“主进程”开统计权限；无遮罩，捕获钩子/探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停在无障碍设置页且无可见UI文本；俄语通知持续显示，overlays=0，仅等待未点击。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍为无障碍设置空文本页；俄语通知继续诱导开启统计权限，overlays=0，仅等待未操作。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | “主进程”服务详情页，含“使用主进程”开关、快捷键选项和“未提供描述”；俄语通知仍在，仅查看详情，无遮罩。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统全控制警告弹窗：英文警告应用可查看/控制屏幕、读取全部内容并代为操作，含允许/拒绝按钮；本步仅查看，无遮罩。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒绝授权后2秒已回到桌面，通知横幅仍谎称系统异常需开统计权限；无应用弹窗或遮罩，表现优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒绝授权后10.5秒仍在桌面，俄语通知持续显示诱导开启统计权限；无二次弹窗或遮罩，应用未崩溃，维持优雅降级。 | `step_01_refusal_10500ms_screen.png` |
