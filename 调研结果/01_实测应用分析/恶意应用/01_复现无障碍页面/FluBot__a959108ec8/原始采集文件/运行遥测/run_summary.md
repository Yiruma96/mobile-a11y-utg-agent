# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:26:46
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.iqiyi.i18n`（静态标签：`malicious` / `FluBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 202 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `DHL` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以常驻通知“请点击此处激活DHL”把用户引至系统无障碍设置，列表中的DHL处于Off；用户进入DHL服务详情触发“完全控制设备”高危授权弹窗。代理点Deny回到桌面后，应用未继续强制弹窗，表现为优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> String (Please click here to activate DHL) 的核心意译为“请点击此处激活DHL”（通知横幅，多页持续显示）
- 英文 -> “允许DHL完全控制您的设备？”（系统警告弹窗）
- 英文 -> “完全控制适用于帮助无障碍需求的应用程序，但不适用于大多数应用。”（系统警告弹窗）
- 英文 -> “查看并控制屏幕：它可以读取屏幕上的所有内容，并在其他应用上显示内容。”（系统警告弹窗）
- 英文 -> “查看并执行操作：它可以跟踪您与应用或硬件传感器的交互，并代表您与应用交互。”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍设置页：已下载应用列表出现DHL且状态Off；通知栏显示英文“请点击此处激活DHL”诱导，本步采集设置钩子后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留无障碍设置页，页面文本暂空；DHL激活通知横幅仍在，遮罩为0，未见新界面。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针：无障碍设置页仍无文本变化；DHL激活通知持续，遮罩为0，未弹覆盖层或新诱导页。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | DHL服务详情页：有“Use DHL”开关及“DHL shortcut/按住音量键/快捷设置”选项；通知横幅仍在，本步检查未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗：询问是否允许DHL完全控制设备，说明可读屏、覆盖显示并代操作；有Allow/Deny，本步点Deny。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回2.0秒：回到NexusLauncher桌面，DHL激活通知仍驻留；无遮罩与新弹窗，结果为优雅停留或降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权返回10.5秒：仍停在桌面，DHL激活通知持续存在；无覆盖层和新诱导，应用保持静默降级，未反复弹窗。 | `step_01_refusal_10500ms_screen.png` |
