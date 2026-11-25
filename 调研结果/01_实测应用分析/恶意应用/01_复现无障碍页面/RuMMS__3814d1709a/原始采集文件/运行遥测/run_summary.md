# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:57:31
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`ru.sailor.energy`（静态标签：`malicious` / `RuMMS` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `4` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / Oсновной процесc`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 215 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Oсновной процесc` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以伪装名“主进程”和俄语通知谎称系统异常、需开启统计权限，将用户引至无障碍服务详情并弹出完全控制警告；点拒绝后先回桌面，随即自动重开无障碍设置继续施压。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Oсновной процесc -> 俄语（含同形字符） -> “主进程”（通知标题/应用显示名，贯穿多个页面）
- Сиcтема не кoррeктнo рaбoтает, вaм неoбходимo включить дoступ к cтaтиcтикe для 'Oсновной процесc' -> 俄语 -> “系统运行异常，您需要为‘主进程’开启统计访问权限”（常驻通知横幅）
- Use Oсновной процесc -> 英语+俄语 -> “使用主进程”（无障碍服务详情页开关项）
- Oсновной процесc shortcut / Hold volume keys / Shortcut settings -> 英语+俄语 -> “主进程快捷方式/按住音量键/快捷方式设置”（服务详情页选项）
- No description provided. -> 英语 -> “未提供描述”（服务详情页）
- Allow Oсновной процесc to have full control of your device? -> 英语 -> “允许主进程完全控制您的设备吗？”（系统警告弹窗）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 英语 -> “完全控制适用于辅助无障碍需求的应用，但不适用于大多数应用。”（系统警告弹窗）
- View and control screen / It can read all content on the screen and display content over other apps. -> 英语 -> “查看并控制屏幕/可读取屏幕全部内容并覆盖显示在其他应用上。”（系统警告弹窗）
- View and perform actions / It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 英语 -> “查看并执行操作/可跟踪您与应用或硬件传感器的交互，并代表您操作应用。”（系统警告弹窗）
- Allow / Deny -> 英语 -> “允许/拒绝”（系统警告弹窗按钮）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：伪装“主进程”显示为已下载应用且关闭；俄语通知谎称系统异常需开统计权限，探针命中无障碍钩子后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍在无障碍设置页，未捕获可见控件；伪装“主进程”俄语通知横幅持续显示，无遮罩。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒探针：无障碍设置页仍无可见控件；伪装“主进程”俄语通知持续误导，未出现遮罩或弹窗。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 无障碍服务详情页：显示“使用主进程”、快捷方式与音量键选项，并称未提供描述；常驻俄语通知仍在，本步仅检查详情。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统高危警告弹窗：英文提示“主进程”将完全控制设备、可读屏并代操作，需选允许/拒绝；本步检查弹窗，未授权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒绝后2秒回到桌面：显示应用列表、Chrome等，俄语通知仍驻留；随后应用自动重开无障碍设置，表现拒权后重试。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +5.5s** | 拒绝后5.5秒：应用已自动重开无障碍列表，“主进程”仍为关闭；俄语通知继续施压，无遮罩，体现循环诱导授权。 | `step_01_refusal_5500ms_screen.png` |
