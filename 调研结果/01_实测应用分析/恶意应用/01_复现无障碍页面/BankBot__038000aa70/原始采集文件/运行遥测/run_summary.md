# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:32:55
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.jiuloisetp.muvhbmbajhun`（静态标签：`malicious` / `BankBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Sistem Güncelleştirmesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Sistem Güncelleştirmesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Sistem Güncelleştirmesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 222 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Sistem Güncelleştirmesi` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用先引导进入无障碍设置，仿冒“系统更新”服务并弹出完全控制设备的高危授权警告；拒绝后转至后台运行电池优化弹窗，未崩溃而是优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 -> “Sistem Güncelleştirmesi（系统更新）”：以正常系统更新名义伪装无障碍服务（无障碍列表/服务详情/授权弹窗）。
- 英语 -> “Allow Sistem Güncelleştirmesi to have full control of your device?”及读屏、覆盖显示、跟踪交互说明：诱导授予完全控制权（系统警告弹窗）。
- 英语 -> “Let app always run in background?”及可能降低电池寿命说明：诱导允许后台常驻（电池优化弹窗）。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页出现“Sistem Güncelleştirmesi（系统更新）”已下载项，状态Off；顶部Google备份通知，无遮罩；采集Hook后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒仍停留无障碍设置页，文本为空；仅Google“数据未备份/添加备份账户”通知，遮罩0，等待探针无新动作。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2秒仍在无障碍设置页，无可见文本；Google备份通知持续，遮罩0，等待探针未发现弹窗或跳转。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页显示“Sistem Güncelleştirmesi（系统更新）”、Use开关与快捷方式选项，说明缺失；检查详情，无遮罩。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗称“允许系统更新完全控制设备”，列明读屏、覆盖显示、跟踪交互并代操作；有Allow/Deny，本步仅检查。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回2秒后出现电池优化弹窗“允许应用始终后台运行？”，可后续更改；有Deny/Allow，遮罩0；结果优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权返回10.5秒仍停在电池优化弹窗“允许应用始终后台运行？”，可后续更改；有Deny/Allow，遮罩0；结果优雅停留/降级。 | `step_01_refusal_10500ms_screen.png` |
