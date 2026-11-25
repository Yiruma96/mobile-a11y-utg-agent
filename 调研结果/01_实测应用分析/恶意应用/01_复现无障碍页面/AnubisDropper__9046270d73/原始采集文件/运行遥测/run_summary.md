# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:37:13
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`apps.mustak.sason`（静态标签：`malicious` / `AnubisDropper` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Operatör Güncellemesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Operatör Güncellemesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Operatör Güncellemesi to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 220 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Operatör Güncellemesi` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Operatör Güncellemesi（运营商更新）”伪装无障碍服务，诱导开启完全控制与后台常驻；拒权后不崩溃，停留在电池优化页并降级等待。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 Operatör Güncellemesi -> 运营商更新（无障碍列表/服务详情页，伪装成系统运营商更新服务）
- 英语 Use Operatör Güncellemesi -> 使用“运营商更新”（服务详情页，诱导启用无障碍服务）
- 英语 Allow Operatör Güncellemesi to have full control of your device? -> 允许“运营商更新”完全控制你的设备？（系统警告弹窗）
- 英语 Let app always run in background? -> 让应用始终在后台运行？（电池优化弹窗，诱导后台常驻）
- 英语 No description provided. -> 未提供描述（服务详情页，掩盖服务用途）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页；已下载应用中出现“Operatör Güncellemesi（运营商更新）”，开关为关闭；探针命中无障碍 Hook 后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针页；仍停留在无障碍设置，界面文本为空，无通知横幅、无悬浮遮罩，等待未触发新页面。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针页；仍在无障碍设置且无界面文本，通知与悬浮遮罩均为0，继续等待未发现诱导弹窗。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页；显示“Operatör Güncellemesi（运营商更新）”及“使用”开关、快捷键设置，标注未提供描述；本步仅检查详情未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统无障碍授权警告；询问是否允许“运营商更新”完全控制设备，说明可读屏、覆盖显示和代操作；本步查看后点Deny拒绝。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2秒弹出电池优化页；英文问“让应用始终后台运行？”，称可能耗电且可稍后改；有Deny/Allow，结果为优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍停在电池优化页；同一后台运行诱导话术未变，Deny/Allow仍在，应用未崩溃，呈优雅停留或降级。 | `step_01_refusal_10500ms_screen.png` |
