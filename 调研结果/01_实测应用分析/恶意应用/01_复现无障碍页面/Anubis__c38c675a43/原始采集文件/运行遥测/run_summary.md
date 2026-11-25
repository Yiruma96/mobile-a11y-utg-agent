# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:18:33
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`wocwvy.czyxoxmbauu.slsa`（静态标签：`malicious` / `Anubis` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Fattura to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Fattura to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Fattura to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 215 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Android Security` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：Anubis 样本先引导开启名为“Android Security”的无障碍服务，借系统警告索取读屏、覆盖显示与代操作等高危权限；拒绝后转入以“Fattura”名义的后台常驻请求，遭拒仍优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “允许 Android Security 完全控制你的设备？”（系统警告弹窗）
- 英文 -> “完全控制适用于辅助无障碍需求的 App，但不适合大多数 App。”（系统警告弹窗）
- 英文 -> “查看并控制屏幕：可读取屏幕全部内容并在其他 App 上覆盖显示。”（系统警告弹窗）
- 英文 -> “查看并执行操作：可跟踪你与 App 或硬件传感器的交互，并代你操作 App。”（系统警告弹窗）
- 英文 -> “让 App 始终在后台运行？”（后台优化弹窗）
- 英文 -> “允许 Fattura 始终后台运行可能缩短电池续航；可稍后在设置中更改。”（后台优化弹窗）
- 英文 -> “未提供说明。”（服务详情页）
- 英文 -> “Android Security”作为服务名出现，疑冒充系统安全组件（服务详情/警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：已安装应用中出现“Android Security/关闭”，疑冒充系统安全组件；无通知/遮罩，捕获钩子后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后探针+0.8s：仍停留无障碍设置页，无新增文案、通知或遮罩，仅等待观察，未点击。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后探针+2.0s：仍停留无障碍设置页，无新增文案、通知或遮罩，仅等待观察，未点击。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：显示“Android Security”启用开关及快捷键设置，描述为“未提供说明”；本步仅检查未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗：请求“Android Security”完全控制设备，称可读屏、覆盖显示并代操作；含允许/拒绝，本步仅检查未授权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权+2.0s：后台优化弹窗以“Fattura”名义请求始终后台运行并提示耗电；已返回拒绝，应用优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权+10.5s：同一后台优化弹窗仍以“Fattura”名义请求常驻后台并提示耗电；返回拒绝后应用优雅停留/降级。 | `step_01_refusal_10500ms_screen.png` |
