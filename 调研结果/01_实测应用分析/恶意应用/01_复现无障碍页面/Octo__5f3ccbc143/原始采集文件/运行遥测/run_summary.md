# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:25:54
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.earlysince27`（静态标签：`malicious` / `Octo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.earlysince27/com.earlysince27.p040j` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Chrome' / Set switch ON`
- **Back 后 +5.5s**：`com.earlysince27/com.earlysince27.p040j` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Chrome' / Set switch ON`
- **Back 后 +10.5s**：`com.earlysince27/com.earlysince27.p040j` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Chrome' / Set switch ON`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 180 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.earlysince27` / `p040j` | `-` | 8 | 67 / 否 | `click` → [8] Button text="Open Settings" id=t_openSettings (clic | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing Chrome to always run in the background may red` | `Deny` | `Allow`
- **Step 2 (`com.earlysince27/p040j`)**: `Enable Accessibility Service` | `•` | `Find` | `'Chrome'` | `Set switch ON` | `Open Settings`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用先借Chrome名义诱导用户同意电池优化豁免，再引导开启名为Chrome的无障碍服务；用户拒绝返回后立即重弹同一诱导页，核心是借用/伪造Chrome身份骗取无障碍权限。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Let app always run in background? -> 让应用始终在后台运行？（电池优化弹窗）
- Allowing Chrome to always run in the background may reduce battery life... -> 允许Chrome始终后台运行可能降低续航，可稍后在设置中更改（电池优化弹窗）
- Enable Accessibility Service -> 启用无障碍服务（应用引导页/拒权后重弹页）
- Find 'Chrome' / Set switch ON -> 找到“Chrome”并将开关打开（应用引导页/拒权后重弹页）
- Open Settings -> 打开设置（应用引导页）
- Use Chrome -> 使用Chrome（服务详情页）
- Enable this service to protect your device -> 启用此服务以保护你的设备（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 系统电池优化豁免弹窗借Chrome名义请求让应用常驻后台；点Allow同意，通知横幅常驻，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: p040j** | 应用内p040j引导页要求启用无障碍服务：找到“Chrome”并打开开关；点Open Settings跳系统设置，通知横幅常驻、无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 进入系统无障碍列表，DOWNLOADED APPS下Chrome显示Off；采集到无障碍设置钩子后终止，通知横幅常驻、无遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留无障碍设置列表，界面文本为空；无遮罩叠加，通知横幅仍显示Enable service/Chrome。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍停留无障碍设置列表，界面文本为空；无遮罩叠加，通知横幅仍显示Enable service/Chrome。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页以Chrome命名，含Use Chrome、快捷键选项及“启用此服务以保护设备”话术；仅检查未点击，无遮罩、通知横幅常驻。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告检查点实际仍为应用内无障碍诱导页，要求找到Chrome并打开开关；无系统弹窗/遮罩，通知横幅常驻。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒后应用再次拉起同一无障碍诱导页，仍要求找到Chrome开开关；无遮罩，通知横幅常驻，呈重弹循环。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒后仍重弹同一无障碍诱导页，持续要求启用Chrome无障碍；无遮罩，通知横幅常驻，未见放弃。 | `step_03_refusal_10500ms_screen.png` |
