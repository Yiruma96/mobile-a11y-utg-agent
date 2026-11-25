# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:21:50
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`wocwvy.czyxoxmbauu.slsa`（静态标签：`malicious` / `Anubis` / 静态可见性：`partial_dynamic_or_remote`）
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

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Android Security` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以“Android Security/安卓安全”冒充安全组件，诱导用户进入无障碍设置并尝试获取完全控制权限；系统警告出现后测试拒绝授权，应用退回桌面且无遮罩/通知，呈优雅停留或降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Android Security -> 安卓安全（无障碍列表/服务详情页）
- Use Android Security -> 启用安卓安全（服务详情页）
- Android Security shortcut -> 安卓安全快捷方式（服务详情页）
- No description provided. -> 未提供说明（服务详情页）
- Allow Android Security to have full control of your device? -> 允许安卓安全完全控制你的设备？（系统警告弹窗）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适用于帮助无障碍需求的应用，但不适合多数应用（系统警告弹窗）
- View and control screen -> 查看并控制屏幕（系统警告弹窗）
- It can read all content on the screen and display content over other apps. -> 可读取屏幕全部内容并叠加显示在其他应用上（系统警告弹窗）
- View and perform actions -> 查看并执行操作（系统警告弹窗）
- It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 可跟踪你与应用或硬件传感器的交互，并代表你操作应用（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表：见伪“Android Security/安卓安全”服务关闭；采集无障碍钩子/探针后自动终止，无遮罩。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停无障碍设置页，界面无文本、无通知、遮罩0，仅等待观察，未点击。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在无障碍设置页，界面无文本、无通知、遮罩0，仅等待观察，未点击。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：显示“Android Security/安卓安全”启用项和音量键快捷方式，无说明；仅检查详情，未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗：问是否允许“安卓安全”完全控制设备，列明读屏、查看并执行操作风险；本步查看后拒权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2秒：回桌面应用列表，通知空、遮罩0；未强推授权，呈优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒：仍在桌面应用列表，通知空、遮罩0；无二次诱导，维持优雅停留/降级。 | `step_01_refusal_10500ms_screen.png` |
