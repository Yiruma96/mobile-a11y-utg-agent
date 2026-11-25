# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:41:05
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.weruzepufalo.mavimibe`（静态标签：`malicious` / `Hook` / 静态可见性：`partial_dynamic_or_remote`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 204 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `BBVA4` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以BBVA4伪装无障碍服务，引导用户进入系统无障碍列表并打开服务详情，通知横幅持续催促启用；用户拒绝授权后回落桌面，未崩溃，表现为优雅停留或降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 启用BBVA4（通知横幅，多处出现）
- 英文 -> 若无障碍权限已开启，请先关闭再开启（BBVA4服务详情页）
- 英文 -> 使用BBVA4（BBVA4服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 进入系统无障碍列表页，已下载应用BBVA4显示为Off，页面含字体与显示等设置；底部有备份通知。探针命中无障碍设置Hook后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 仍停留在无障碍列表页，界面文本为空；BBVA4通知横幅提示“Enable BBVA4”，备份通知并存，遮罩数为0，等待0.8秒后无变化。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 无障碍列表页保持静止，UI文本为空；BBVA4通知继续催启用，备份通知并存，遮罩为0，等待2.0秒仍无页面跳转。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 进入BBVA4服务详情页，显示“Use BBVA4”开关及快捷键、音量键选项；底部英文提示若无障碍权限已开需关闭再开启，诱导授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告弹窗页仍显示BBVA4服务详情，无额外遮罩；探针查看警告并点Deny，BBVA4与备份通知仍在，未见取消软键异常。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后返回桌面，显示应用列表与Messages/Chrome等图标；BBVA4通知仍提示启用，备份通知并存，无遮罩，判定优雅停留/降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权10.5秒后仍在桌面，页面内容与通知未变；BBVA4横幅继续提示启用，备份通知并存，无遮罩，应用未崩溃或无明显降级。 | `step_01_refusal_10500ms_screen.png` |
