# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:41:23
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.rekezapayojekubu.kebi`（静态标签：`malicious` / `Ermac` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `3` 个，有向边 `5` 条）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `HookAPPService` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从系统无障碍设置入口引导开启 HookAPPService，并在服务详情以“关闭再开启”等说明诱导反复授权，同时用“启用 Chrome 更新服务”常驻通知伪装。用户拒绝后回到桌面，应用保持驻留并安静降级，未见强制弹窗或崩溃。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “HookAPP/启用 Chrome 更新服务”（通知横幅，贯穿无障碍列表与服务详情页）：以更新 Chrome 服务为名掩盖 Hook 无障碍服务。
- 英语 -> “若无障碍权限已开启，请先关闭再重新开启。”（HookAPPService 服务详情页）：诱导用户反复切换以激活无障碍权限。
- 英语 -> “使用 HookAPPService”（服务详情页）：直接引导开启该无障碍服务，弱化权限风险。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍设置列表，HookAPPService 显示关闭；通知冒充“启用 Chrome 更新服务”，探针命中后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒仍在无障碍设置页，界面文本为空；应用通知“HookAPP/启用Chrome更新服务”持续显示，未见悬浮遮罩。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒仍停留无障碍设置页，无可见文本；伪装“启用Chrome更新服务”的通知横幅持续驻留，遮罩数为0。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 进入 HookAPPService 服务详情，显示“使用 HookAPPService”开关与快捷方式；提示先关闭再开启无障碍权限，通知仍在。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗环节并选择拒绝，页面仍为 HookAPPService 详情；可见“关闭再开启”提示，遮罩为0，弹窗未以悬浮层出现。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒绝后2秒回到桌面，显示应用列表、日期及 Messages/Chrome/Search 图标；应用通知仍驻留，无崩溃或强制跳转，呈安静降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒绝后10.5秒仍停在桌面，图标与通知状态不变；未见二次弹窗或强制跳转，应用维持驻留与降级行为。 | `step_01_refusal_10500ms_screen.png` |
