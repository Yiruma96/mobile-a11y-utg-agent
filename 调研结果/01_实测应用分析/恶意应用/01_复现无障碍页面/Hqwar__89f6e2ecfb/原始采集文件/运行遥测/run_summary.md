# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:48:57
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.pagkijxim.tycdlm`（静态标签：`malicious` / `Hqwar` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing PayLife Kartensicherheit to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing PayLife Kartensicherheit to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing PayLife Kartensicherheit to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 206 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `PayLife` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以PayLife/PayLife Kartensicherheit名义，从系统无障碍列表诱导启用服务，再弹出全权控制警告；拒权后转索要后台常驻权限并停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文：PayLife / Use PayLife / No description provided. -> 中文意译：PayLife／使用PayLife／未提供描述（服务详情页）
- 英文：Allow PayLife to have full control of your device? Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 中文意译：允许PayLife完全控制设备？完全控制适合无障碍应用但多数应用不适合；可查看并控制屏幕、代执行操作（系统警告弹窗）
- 英文：Let app always run in background? Allowing PayLife Kartensicherheit to always run in the background may reduce battery life. -> 中文意译：让应用始终后台运行？允许PayLife Kartensicherheit始终后台可能降低续航（电池优化请求页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍列表中“已下载应用”内PayLife显示Off（关闭）；捕获无障碍设置钩子与探针后自动终止，无通知/遮罩。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在无障碍设置页，页面文本为空；仅等待，遮罩数为0，无通知横幅。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针：无障碍设置页无文本变化，仍无遮罩/通知；继续等待，未发生授权或跳转。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | PayLife服务详情页：显示“Use PayLife（使用PayLife）”、快捷方式与音量键选项，并称“未提供描述”；执行查看详情/警告。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗询问是否允许PayLife完全控制设备，称可读屏并代操作；含Allow/Deny，本步仅检查未授权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2秒跳至电池优化请求：问是否让PayLife Kartensicherheit始终后台运行，称可能耗电；含Deny/Allow，停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍停在电池优化请求页，同一后台常驻话术未变；无遮罩/通知，应用未崩溃而是停留或降级。 | `step_01_refusal_10500ms_screen.png` |
