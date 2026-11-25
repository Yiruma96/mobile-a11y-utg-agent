# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:03:44
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.kcyhit.tjdedz`（静态标签：`malicious` / `Anubis` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Android Update to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Android Update to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`
- **Back 后 +10.5s**：`com.android.settings/com.android.settings.fuelgauge.RequestIgnoreBatteryOptimizations` | hooks=`[]` | overlays=`0` | texts=`Let app always run in background? / Allowing Android Update to always run in the background may reduce battery life. 

You can change this later from Settings > Apps & notifications. / Deny / Allow`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 220 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Active Secure Service` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以“Active Secure Service”名义进入系统无障碍设置，先诱导开启完全控制/读屏悬浮能力，遭拒后再弹电池优化后台常驻请求。连续拒绝后表现为优雅停留或降级，未崩溃，具有典型Anubis式权限索取链。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 允许“Active Secure Service”完全控制你的设备？该权限适合无障碍需求应用而非多数应用（系统警告弹窗）
- 英文 -> 可查看并控制屏幕，读取屏幕全部内容并悬浮显示于其他应用之上（系统警告弹窗）
- 英文 -> 可查看并执行操作，跟踪你与应用或硬件传感器的交互，并代表你操作其他应用（系统警告弹窗）
- 英文 -> 允许应用始终在后台运行？允许“Android Update”常驻可能降低续航，可稍后在设置中更改（电池优化弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页：已安装应用中出现“Active Secure Service”且状态为Off；本步采集无障碍设置钩子与探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在无障碍设置页，未捕获任何界面文字，遮罩为0、无通知，仅等待观察。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面仍为无障碍设置且无界面文字，遮罩0、无通知，继续等待未出现诱导浮层。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：显示“Active Secure Service”启用开关及快捷键选项，文案称无描述；本步仅检查详情与警告，未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统授权警告弹窗：要求允许该服务完全控制设备，并列出读屏、悬浮、跟踪与代操作能力；本步检查后应点Deny拒绝。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回2.0秒：跳至电池优化请求弹窗，要求允许“Android Update”常驻后台；本步返回拒绝，结果为优雅停留或降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权返回10.5秒：同一电池优化弹窗仍在，继续索要后台常驻权限；再次返回拒绝，应用未崩溃而停留或降级。 | `step_01_refusal_10500ms_screen.png` |
