# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:56:02
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.fqaqkdwn.uhkshvhv`（静态标签：`malicious` / `Hqwar` / 静态可见性：`packed_or_encrypted`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 218 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Play Protect` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用从系统无障碍设置页进入，经空界面探针转至 Google Play Protect 服务详情与“完全控制设备”高危授权弹窗；用户拒绝后回落桌面启动器并保持/降级，未崩溃或持续覆盖。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Allow Google Play Protect to have full control of your device? -> 是否允许 Google Play Protect 完全控制你的设备？（系统警告弹窗）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适用于辅助无障碍需求的应用，但不适用于大多数应用。（系统警告弹窗）
- It can read all content on the screen and display content over other apps. -> 可读取屏幕全部内容并覆盖显示在其他应用之上。（系统警告弹窗）
- It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 可追踪交互与传感器并代表你操作其他应用。（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页：显示已下载应用、Play Protect 关闭及屏幕阅读器等；命中无障碍设置 Hook 与探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在无障碍设置页，界面文本为空、无通知横幅、遮罩数为 0，仅等待观察。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：仍在无障碍设置页，界面文本为空、无通知与遮罩，遮罩数为 0，等待无变化。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | Google Play Protect 服务详情页：含启用开关、快捷方式与音量键选项，并提示未提供说明；本步仅查看详情/警告。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗：询问是否允许 Play Protect 完全控制设备，列出查看/控制屏幕与代操作能力；本步查看后点 Deny 拒绝。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后 2 秒回到桌面启动器：显示应用列表、日期与天气；无通知/遮罩，应用未崩溃，呈优雅停留或降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后 10.5 秒仍在桌面启动器：应用列表、日期与天气可见，无通知与遮罩；确认拒绝后保持停留/降级，无进一步诱导。 | `step_01_refusal_10500ms_screen.png` |
