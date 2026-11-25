# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:10:20
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.freeroad11`（静态标签：`malicious` / `Octo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `RequestIgnoreBatteryOptimizations` | `-` | 4 | 180 / 否 | `click` → [4] Button text="Allow" id=button1 (click) center=(887, | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.freeroad11` / `p031x` | `-` | 1 | 0 / 是 | `click` → [551, 690] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/RequestIgnoreBatteryOptimizations`)**: `Let app always run in background?` | `Allowing Chrome to always run in the background may red` | `Deny` | `Allow`
- **Step 2 (`com.freeroad11/p031x`)**: (空文本)
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先申请忽略电池优化以保后台，再通过应用内空白WebView跳转系统无障碍列表，借伪造Chrome服务条目和“保护设备”话术诱导开启无障碍；审核拒权后应用未崩溃，退回桌面并降级停留，常驻伪Chrome通知。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “让应用始终在后台运行？”（系统电池优化请求页）
- 英文 -> “允许Chrome始终在后台运行可能缩短电池续航；稍后可在设置>应用和通知中更改。”（系统电池优化请求页）
- 英文 -> “启用此服务以保护你的设备”（无障碍服务详情页，伪装Chrome）
- 英文 -> “使用Chrome”/“Chrome快捷方式”/“按住音量键”（无障碍服务详情页选项，用于强化Chrome伪装）
- 英文占位 -> “String (Enable service)”/“String (Chrome)”（常驻通知横幅，伪装Chrome启用服务）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestIgnoreBatteryOptimi** | 系统电池优化弹窗，英文诱导“让应用始终后台运行”，假借Chrome说明耗电；点Allow放行，顶部伪Chrome通知，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: p031x** | 应用内空白WebView页p031x，无文案，顶部伪Chrome通知；按坐标点预设“Open Settings”区域跳转无障碍设置，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表页，DOWNLOADED APPS下Chrome为Off；借伪造Chrome条目诱导开启服务，顶部伪通知驻留，采集Hook后终止。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转无障碍列表后0.8秒探针：界面同前，无新增文案与遮罩；伪Chrome通知仍驻留，等待中未见授权。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：无障碍列表保持原状，无新增文案与遮罩；伪Chrome通知仍在，等待中未发生授权。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 无障碍服务详情页，英文显示Chrome/Use Chrome及“启用此服务以保护设备”诱导；顶部伪Chrome通知驻留，本步仅检查详情，无遮罩。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告弹窗场景，详情页仍含“启用此服务以保护设备”诱导；顶部伪Chrome通知驻留、无遮罩，本步检查后按Deny/返回。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2.0秒：回桌面启动器，见Apps list/Chrome；拒权后应用未崩溃而降级停留，伪Chrome通知仍驻留，无遮罩。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒：仍在桌面启动器，可见Apps list/Chrome；应用保持降级停留无进一步弹窗，伪Chrome通知持续驻留，无遮罩。 | `step_03_refusal_10500ms_screen.png` |
