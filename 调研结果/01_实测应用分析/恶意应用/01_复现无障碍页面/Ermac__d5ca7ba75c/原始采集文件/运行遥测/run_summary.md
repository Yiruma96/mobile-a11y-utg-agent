# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:54:27
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.camavoyaxiwokocu.huvusuwi`（静态标签：`malicious` / `Ermac` / 静态可见性：`partial_dynamic_or_remote`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `HookAPPService` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以 HookAPP 通知“启用 Chrome 更新服务”常驻，引导用户在系统无障碍列表中开启 HookAPPService；服务详情页提示反复开关无障碍权限，随后出现系统完全控制警告，点 Deny 后应用未崩溃而是退回桌面并保留通知，表现为 GRACEFUL_STAY_OR_DEGRADE。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- String (Enable Chrome Update Service)（通知横幅/无障碍列表页）→ 字符串（启用 Chrome 更新服务）
- Use HookAPPService（服务详情页）→ 使用 HookAPPService
- If accessibility permission has been on, please turn off then turn on.（服务详情页）→ 如果无障碍权限已开启，请先关闭再重新开启
- HookAPPService shortcut / Hold volume keys / Shortcut settings（服务详情页）→ HookAPPService 快捷方式/按住音量键/快捷方式设置
- Allow HookAPPService to have full control of your device?（系统警告弹窗）→ 允许 HookAPPService 完全控制你的设备？
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps.（系统警告弹窗）→ 完全控制适用于帮助无障碍需求的 app，但不适用于大多数 app
- View and control screen / It can read all content on the screen and display content over other apps.（系统警告弹窗）→ 查看并控制屏幕/可读取屏幕全部内容并在其他 app 上显示内容
- View and perform actions / It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.（系统警告弹窗）→ 查看并执行操作/可追踪你与 app 或硬件传感器的交互，并代表你操作 app

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：HookAPPService 显示 Off，通知横幅称“String (Enable Chrome Update Service)”；采集设置钩子/探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停留在无障碍设置页，无可见文本、无遮罩；HookAPP 通知横幅持续存在。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒探针：页面仍为无障碍设置，UI 文本为空，遮罩数为0；HookAPP 通知横幅未消失。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：显示 HookAPPService、Use HookAPPService 与快捷方式；提示无障碍权限需关闭再开启，本步查看详情/警告。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗：询问是否允许 HookAPPService 完全控制设备，并列出读屏、代操作能力；本步点 Deny 拒绝授权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2.0秒：已退回 Nexus 桌面，显示应用列表/天气/Chrome 等；应用未崩溃，通知横幅仍在，呈优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒：仍停留桌面，HookAPP 通知横幅持续；无遮罩或二次弹窗，确认拒权后静默降级。 | `step_01_refusal_10500ms_screen.png` |
