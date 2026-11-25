# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:45:59
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.turenak.ch`（静态标签：`malicious` / `Banker` / 静态可见性：`partial_dynamic_or_remote`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 227 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `UYGULAMA AKTIFLESTIRME ONAYI` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该 Banker 类应用从系统无障碍设置进入，展示伪装成“UYGULAMA AKTIFLESTIRME ONAYI”（应用激活批准）的服务，并诱导用户授予完全控制权；用户点 Deny 后返回桌面且无异常，表现为平稳停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语：UYGULAMA AKTIFLESTIRME ONAYI -> 应用激活批准（无障碍列表页/服务详情页/系统警告弹窗）
- 土耳其语：Use UYGULAMA AKTIFLESTIRME ONAYI -> 使用/启用“应用激活批准”（服务详情页）
- 土耳其语：UYGULAMA AKTIFLESTIRME ONAYI shortcut -> “应用激活批准”快捷方式（服务详情页）
- 土耳其语：Hold volume keys -> 长按音量键（服务详情页）
- 英语：No description provided. -> 未提供描述（服务详情页）
- 英语：Allow UYGULAMA AKTIFLESTIRME ONAYI to have full control of your device? -> 是否允许“应用激活批准”完全控制您的设备？（系统警告弹窗）
- 英语：Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适用于辅助无障碍需求的App，不适用于大多数App（系统警告弹窗）
- 英语：View and control screen -> 查看并控制屏幕（系统警告弹窗）
- 英语：It can read all content on the screen and display content over other apps. -> 可读取屏幕全部内容并在其他应用上显示内容（系统警告弹窗）
- 英语：View and perform actions -> 查看并执行操作（系统警告弹窗）
- 英语：It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 可跟踪与App或硬件传感器的交互，并代您操作App（系统警告弹窗）
- 英语：Allow / Deny -> 允许 / 拒绝（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍设置列表页，出现土耳其语“UYGULAMA AKTIFLESTIRME ONAYI”（应用激活批准）服务项且为 Off；捕获无障碍设置钩子后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒仍停留无障碍列表页，界面文本为空，无通知横幅与悬浮遮罩；仅等待探针，无点击和页面跳转。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2秒仍停在无障碍列表页，界面文本为空，无通知横幅或遮罩；继续等待，未发生点击或跳转。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 无障碍服务详情页显示土语“UYGULAMA AKTIFLESTIRME ONAYI”（应用激活批准）及“Use…”启用项、音量键快捷方式；仅检查未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗，询问是否允许“UYGULAMA AKTIFLESTIRME ONAYI”（应用激活批准）完全控制设备，并称可读屏、覆盖应用、代操作；未点 Allow。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 点 Deny 后2秒返回 Google 桌面，显示应用列表、日期天气等常规内容；无错误弹窗或二次诱导，表现为拒权后平稳降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍停在 Google 桌面，显示应用列表、日期天气等；无通知横幅、遮罩或再次索权，保持平稳停留。 | `step_01_refusal_10500ms_screen.png` |
