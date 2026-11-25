# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:50:31
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.wdgrlnjoufx.qdlijknlopte`（静态标签：`malicious` / `Hqwar` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Servis Güncellemesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Servis Güncellemesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Servis Güncellemesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 218 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Servis Güncellemesi` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以土耳其语名“Servis Güncellemesi”（服务更新）伪装，在系统无障碍列表中暴露后进入服务详情并弹出“完全控制设备”高危授权；拒绝后转向后台常驻/电池优化豁免弹窗，最终呈优雅停留或降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语“Servis Güncellemesi” -> “服务更新”（无障碍应用列表/服务详情页）
- 英语“Use Servis Güncellemesi” -> “使用服务更新”（服务详情页）
- 英语“No description provided.” -> “未提供描述”（服务详情页）
- 英语“Allow Servis Güncellemesi to have full control of your device?” -> “允许‘服务更新’完全控制你的设备？”（系统警告弹窗）
- 英语“Full control is appropriate for apps that help you with accessibility needs, but not for most apps.” -> “完全控制适用于帮助无障碍需求的应用，但不适合大多数应用。”（系统警告弹窗）
- 英语“View and control screen / It can read all content on the screen and display content over other apps.” -> “查看并控制屏幕 / 可读取屏幕全部内容并叠加显示在其他应用上。”（系统警告弹窗）
- 英语“View and perform actions / It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.” -> “查看并执行操作 / 可跟踪你与应用或硬件传感器的交互，并代表你操作应用。”（系统警告弹窗）
- 英语“Let app always run in background? / Allowing Servis Güncellemesi to always run in the background may reduce battery life.” -> “让应用始终在后台运行？/ 允许‘服务更新’始终后台运行可能缩短电池续航。”（电池优化豁免弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页，下载应用显示土耳其语“Servis Güncellemesi”（服务更新）且为Off；触发无障碍设置钩子后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停在无障碍设置页，界面文本为空，无通知横幅与遮罩，仅等待观察。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针，页面仍为无障碍设置，文本为空，无通知与遮罩，继续等待未发生跳转。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页，标题为“Servis Güncellemesi”（服务更新），含使用服务、OPTIONS、音量键快捷方式及“未提供描述”；仅检查未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗，问是否允许“服务更新”完全控制设备，列明读屏、叠加、跟踪交互与代操作，含Allow/Deny；本步仅检查未授权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回2秒后弹出电池优化豁免框：是否让“服务更新”始终后台运行并提示耗电，含Deny/Allow；已拒绝，结果优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权返回10.5秒后仍见同一后台常驻弹窗，询问是否让“服务更新”始终后台运行，含Deny/Allow；未授权，结果优雅停留/降级。 | `step_01_refusal_10500ms_screen.png` |
