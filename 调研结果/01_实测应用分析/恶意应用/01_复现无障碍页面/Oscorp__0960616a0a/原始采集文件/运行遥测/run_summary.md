# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:24:14
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.cosmos.starwarz`（静态标签：`malicious` / `Oscorp` / 静态可见性：`partial_dynamic_or_remote`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Protezione Cliente` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以意大利语“Protezione Cliente（客户保护）”名义出现在系统无障碍服务列表，并引导进入详情开启完全控制权限；系统警告弹窗出现后测试选择拒绝，随后回到桌面并保持静默，呈 GRACEFUL_STAY_OR_DEGRADE 的温和降级特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 意大利语「Protezione Cliente」 -> 中文意译“客户保护/客户防护”（无障碍列表页、服务详情页）
- 意大利语「Use Protezione Cliente」 -> 中文意译“使用‘客户保护’”（服务详情页开关项）
- 意大利语「Protezione Cliente shortcut」 -> 中文意译“‘客户保护’快捷方式”（服务详情页选项）
- 英语「Hold volume keys」 -> 中文意译“按住音量键”（服务详情页快捷方式设置）
- 英语「No description provided.」 -> 中文意译“未提供描述”（服务详情页）
- 英语「Allow Protezione Cliente to have full control of your device?」 -> 中文意译“允许‘客户保护’完全控制你的设备吗？”（系统警告弹窗）
- 英语「Full control is appropriate for apps that help you with accessibility needs, but not for most apps.」 -> 中文意译“完全控制适用于帮助无障碍需求的应用程序，但不适用于大多数应用。”（系统警告弹窗）
- 英语「View and control screen」 -> 中文意译“查看并控制屏幕”（系统警告弹窗）
- 英语「It can read all content on the screen and display content over other apps.」 -> 中文意译“它可以读取屏幕上的所有内容，并在其他应用之上显示内容。”（系统警告弹窗）
- 英语「View and perform actions」 -> 中文意译“查看并执行操作”（系统警告弹窗）
- 英语「It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.」 -> 中文意译“它可以跟踪你与应用或硬件传感器的交互，并代表你与应用交互。”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍列表页显示可疑服务“Protezione Cliente”为Off；捕获无障碍设置钩子与探针后自动终止，无通知或遮罩。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍在无障碍设置页，界面无文本；无通知横幅、无遮罩，未出现新页面或诱导动作。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针继续停留无障碍设置页，界面无文本；无通知与遮罩，说明未立即触发新界面或覆盖层。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 进入“Protezione Cliente”服务详情页，含启用开关、快捷方式与按住音量键选项，描述缺失；本步仅检查详情，未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗称允许“Protezione Cliente”完全控制设备，并列出读屏、覆盖与代操作能力；本步点Deny拒绝，遮罩为0。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2秒回到桌面启动器，仅见应用列表、搜索与Chrome等图标；无通知、无遮罩，应用未立即反弹强推授权。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍停留桌面启动器，界面与2秒时一致；无通知、无遮罩，未再索权或异常跳转，呈温和降级。 | `step_01_refusal_10500ms_screen.png` |
