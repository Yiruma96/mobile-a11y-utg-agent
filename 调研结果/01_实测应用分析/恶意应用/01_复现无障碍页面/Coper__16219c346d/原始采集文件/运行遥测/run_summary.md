# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:56:13
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.ublocked47tallcloud`（静态标签：`malicious` / `Coper` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.ublocked47tallcloud/com.ublocked47tallcloud.vtiE8xJsNyR` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Binance' / Set switch ON`
- **Back 后 +5.5s**：`com.ublocked47tallcloud/com.ublocked47tallcloud.vtiE8xJsNyR` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Binance' / Set switch ON`
- **Back 后 +10.5s**：`com.ublocked47tallcloud/com.ublocked47tallcloud.vtiE8xJsNyR` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Binance' / Set switch ON`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 181 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.ublocked47tallcloud` / `vtiE8xJsNyR` | `-` | 1 | 0 / 是 | `click` → [528, 600] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 206 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing Binance to always run in the background may re` | `Deny` | `Allow`
- **Step 2 (`com.ublocked47tallcloud/vtiE8xJsNyR`)**: (空文本)
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Binance` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用先在系统设置请求电池优化白名单，再经应用内空白页跳转无障碍设置，将服务伪装为“Binance”诱导开启；拒权后反复重拉“启用无障碍服务”弹窗，具备强诱导与重试特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Let app always run in background? -> 让应用始终在后台运行？（step_01）
- Allowing Binance to always run in the background may reduce battery life. -> 允许“Binance”始终后台运行可能降低续航，但可稍后更改（step_01）
- Enable this service to protect your device. -> 启用此服务以保护你的设备（detail_1_service_detail_page）
- Enable Accessibility Service -> 启用无障碍服务（detail_2_system_warning_dialog/refusal_*）
- Find 'Binance' / Set switch ON / Open Settings -> 找到“Binance”、把开关设为开启、打开设置（detail_2_system_warning_dialog/refusal_*）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 系统电池优化授权页，应用伪装为“Binance”；通知横幅显示更新/需注意，提示允许后台运行，本步点“Allow”放行。 | `step_01_action.png` |
| 2 | **Step 2: vtiE8xJsNyR** | 应用内空白页，仅有“Update/Attention required”通知横幅；按坐标点击疑似“Open Settings”，触发无障碍设置跳转。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表页，已列出“Binance”且为关闭；页面引导开启下载应用服务，检测到无障碍设置钩子后自动终止。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留在无障碍列表页；无新增文案与遮罩，仅通知横幅持续显示更新/需注意占位文本。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针，无障碍列表页无变化；遮罩为0、无新增弹窗，通知横幅仍为“Update/Attention required”占位。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 系统无障碍服务详情页：伪装“Binance”，显示“Use Binance”“Binance shortcut”与“启用此服务可保护设备”，开关仍为关闭。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 应用内授权诱导弹窗：要求查找“Binance”、把开关设为ON并点“Open Settings”，为关键无障碍授权引导页。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒后仍显示同一“启用无障碍服务”诱导弹窗；返回拒绝未消失，记录为重新拉起诱导弹窗。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒后诱导弹窗依旧存在；反复要求查找“Binance”、开启开关并进设置，显示强黏性重拉授权话术。 | `step_03_refusal_10500ms_screen.png` |
