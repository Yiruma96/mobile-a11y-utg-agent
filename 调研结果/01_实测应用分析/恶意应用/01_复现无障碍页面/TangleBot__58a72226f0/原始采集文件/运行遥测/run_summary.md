# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:30:59
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.jsfzhkdwok.iaitibsyurmnq`（静态标签：`malicious` / `TangleBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `5` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.jsfzhkdwok.iaitibsyurmnq` / `MainActivity` | `-` | 1 | 0 / 是 | `click` → [540, 1638] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 210 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.jsfzhkdwok.iaitibsyurmnq/MainActivity`)**: (空文本)
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `4K IPTV PRO` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：入口 MainActivity 的 WebView 点击“Continuare（继续）”后跳转系统无障碍列表，并以持续通知诱导启用伪装的“4K IPTV PRO”无障碍服务，再进入详情与“完全控制设备”系统警告；拒绝/返回后回到桌面，通知仍驻留、无遮罩，呈 GRACEFUL_STAY_OR_DEGRADE 的优雅降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 罗马尼亚语/意大利语 -> “继续”（主界面 WebView 的 Continuare 按钮）
- 英语 -> 以“4K IPTV PRO”伪装成 IPTV 应用（无障碍列表、服务详情页及通知横幅）
- 英语 -> 请在设置→无障碍→已安装服务或已下载服务中启用“4K IPTV PRO”（无障碍列表页及后续页持续通知）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面为 WebView，仅见“Continuare（继续）”按钮；本步点击坐标[540,1638]触发跳转，页面未显示其他说明或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳至系统无障碍列表，已下载应用区显示“4K IPTV PRO”为关闭；应用通知要求到设置中启用该服务，探针捕获无障碍钩子后自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒仍在无障碍列表页，前台无界面文字；应用通知横幅持续提示启用“4K IPTV PRO”，无遮罩，探针仅等待。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒同一无障碍列表页，无界面文字；同一条启用“4K IPTV PRO”的通知出现两条，仍无遮罩，探针等待结束。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入“4K IPTV PRO”无障碍服务详情页，含“Use 4K IPTV PRO（使用）”开关为关、快捷方式关闭；通知仍催启用，本步仅检查详情/警告。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告弹窗：是否允许“4K IPTV PRO”完全控制设备，称可读屏、覆盖应用并代操作；含“Allow/Deny”，本步查看后点拒绝。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝授权并返回桌面启动器，见应用列表与日期；应用通知仍提示启用“4K IPTV PRO”，无遮罩，结果为优雅停留/降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面启动器，界面无变化；启用“4K IPTV PRO”的通知继续驻留，无遮罩，应用未崩溃而降级停留。 | `step_02_refusal_10500ms_screen.png` |
