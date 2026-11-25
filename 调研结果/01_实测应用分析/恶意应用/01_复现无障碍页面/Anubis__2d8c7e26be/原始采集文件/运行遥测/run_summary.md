# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:53:57
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`ivo.baxkjggmgror.itiukv`（静态标签：`malicious` / `Anubis` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing MX Player to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing MX Player to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing MX Player to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 218 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Play Protect` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从系统无障碍列表触发设置钩子，随后以 Google Play Protect 名义进入服务详情并弹出全屏控制警告；拒绝后转跳 MX Player 电池优化保活请求，最终未获授权而优雅停留或降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “允许 Google Play Protect 完全控制您的设备吗？”并以“适合无障碍需求、不适合大多数应用”包装授权合理性（系统警告弹窗）
- 英文 -> “可查看并控制屏幕，读取屏幕全部内容并叠加显示在其他应用上方”（系统警告弹窗）
- 英文 -> “可查看并执行操作，跟踪与应用的交互并代表您操作应用”（系统警告弹窗）
- 英文 -> “让应用始终在后台运行？允许 MX Player 始终后台运行可能降低续航，可稍后在设置中更改”（电池优化弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页，已下载应用中的 Play Protect 显示关闭；捕获无障碍钩子与探针后自动终止，无通知与遮罩。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍停在无障碍设置页，界面无文本，无通知与遮罩，仅等待观察页面是否变化。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针继续停留同一无障碍设置页，仍无可见文本、通知或遮罩，未出现额外授权弹窗。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 进入 Play Protect 服务详情页，含“使用 Play Protect”、快捷键与音量键选项，并提示“未提供说明”；执行查看详情与警告。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗要求允许 Play Protect 完全控制设备，列出读屏、叠加与代操作能力，并提供 Allow/Deny；本步仅检查弹窗。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2秒转至电池优化页，弹窗请求让 MX Player 始终后台运行并提供 Deny/Allow；执行返回拒绝，结果优雅停留或降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍停留同一电池优化弹窗，MX Player 后台保活请求未变，无通知与遮罩；保持拒绝并优雅停留或降级。 | `step_01_refusal_10500ms_screen.png` |
