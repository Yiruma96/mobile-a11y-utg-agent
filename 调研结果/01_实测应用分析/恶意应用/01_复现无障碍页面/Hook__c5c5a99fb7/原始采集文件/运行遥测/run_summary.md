# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:54:54
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sonirupiwebidoti.geyosego`（静态标签：`malicious` / `Hook` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `3` 个，有向边 `5` 条）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 207 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Contacts` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该Hook类应用先引导至系统无障碍设置并反复推送“启用联系人”通知，再进入联系人无障碍服务详情页，以“若权限曾开启请先关闭再开启”的说明施压授权；用户拒绝后未出现遮罩，应用退至桌面且通知持续，表现为平稳降级停留。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“String (Enable Contacts)” -> 启用联系人（无障碍列表页及后续各页通知横幅）
- 英文“Use Contacts” -> 使用联系人（联系人服务详情页）
- 英文“If accessibility permission has been on, please turn off then turn on.” -> 若无障碍权限曾开启，请先关闭再开启（联系人服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：系统项含“联系人/关闭”等；通知横幅“启用联系人”，无遮罩，本步捕获Hook与探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒探针仍停留无障碍设置页，界面无可见文本；应用通知横幅“启用联系人”持续，遮罩0，仅等待无操作。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒探针仍在无障碍设置页，界面空白；同一“启用联系人”通知出现3条，遮罩0，等待期间无交互。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 联系人服务详情页：含“使用联系人/音量键快捷方式”；英文提示“若权限曾开启请先关再开”，通知求启用联系人，无遮罩。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗探针：点击Deny后仍停留联系人服务详情，界面含同样“先关再开”提示；通知求启用联系人，未见遮罩。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权2秒后回桌面：显示应用列表、日期天气与Messages/Chrome/Search；通知仍求“启用联系人”，无遮罩，平稳降级停留。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权10.5秒后仍在桌面：应用列表、日期天气与Messages/Chrome/Search可见；通知持续求“启用联系人”，无遮罩，保持降级。 | `step_01_refusal_10500ms_screen.png` |
