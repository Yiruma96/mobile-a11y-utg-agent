# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:41:22
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`artwork.differ.kitchen`（静态标签：`malicious` / `BlackRock` / 静态可见性：`packed_or_encrypted`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 211 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Flash Player` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Flash Player”为名出现在无障碍下载应用列表，进入服务详情后诱导开启完全控制权限；在系统警告处拒绝后返回桌面，未崩溃、未反复弹窗，表现为优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “Flash Player”伪装名称（无障碍列表/服务详情页）
- 英文 -> 使用 Flash Player（服务详情页）
- 英文 -> Flash Player 快捷方式（服务详情页）
- 英文 -> 按住音量键（服务详情页）
- 英文 -> 快捷方式设置（服务详情页）
- 英文 -> 未提供任何描述（服务详情页）
- 英文 -> 允许 Flash Player 完全控制您的设备？（系统警告弹窗）
- 英文 -> 完全控制适合帮助无障碍需求的应用程序，但不适合大多数应用（系统警告弹窗）
- 英文 -> 查看并控制屏幕／可读取屏幕全部内容并覆盖显示在其他应用之上（系统警告弹窗）
- 英文 -> 查看并执行操作／可跟踪与应用程序或硬件传感器的交互，并代表您与应用交互（系统警告弹窗）
- 英文 -> 允许／拒绝（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页，下载应用见“Flash Player”，状态“关”；本步自动终止并记录无障碍钩子与探针。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍在无障碍设置页，界面文本为空、遮罩为0，无通知横幅，仅等待观察。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针仍停在无障碍设置页，文本为空、遮罩为0，无通知横幅，等待期间无新弹层或诱导界面。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | “Flash Player”无障碍服务详情页，含“使用 Flash Player”“按住音量键”选项，描述称“未提供任何描述”；本步仅检查未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗询问是否允许“Flash Player”完全控制设备，称可读屏、悬浮覆盖及代操作，含允许/拒绝；本步仅检查未授权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2.0秒回到桌面启动器，见应用列表、日期及 Messages/Chrome/搜索图标；无遮罩通知，应用呈优雅降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面启动器，显示应用列表、日期及 Messages/Chrome/搜索等；无通知横幅与遮罩，未再弹窗。 | `step_01_refusal_10500ms_screen.png` |
