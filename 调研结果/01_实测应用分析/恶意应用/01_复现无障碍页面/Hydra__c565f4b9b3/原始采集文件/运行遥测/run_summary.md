# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:24:54
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.grand.thinpad`（静态标签：`malicious` / `Hydra` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `5` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.grand.thinpad` / `PermissionsActivity` | `-` | 6 | 247 / 否 | `click` → [6] Button text="GO TO SETTINGS" id=bt_goto_settings (c | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.grand.thinpad/PermissionsActivity`)**: `In order for the latest version of Chrome to work, you ` | `Step 1 - Go to “Settings”` | `Step 2 - Open “Accessibility”` | `Step 3 - Open “Installed Services”` | `Step 4 - Turn “Chrome” on` | `GO TO SETTINGS`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用伪装成 Chrome 无障碍授权引导：先展示启用辅助功能步骤并跳转系统设置，利用“Chrome”通知横幅持续诱导；进入服务详情和系统全控制警告后，若用户拒绝则退回桌面并保持静默降级，无崩溃或悬浮遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “为了让最新版 Chrome 正常工作，你需要启用无障碍功能，请按以下步骤操作”（PermissionsActivity 引导页）
- 英文 -> “步骤1：进入设置；步骤2：打开无障碍；步骤3：打开已安装服务；步骤4：开启 Chrome”（PermissionsActivity 引导页）
- 英文 -> 通知横幅标题为“Chrome”，正文重复“启用无障碍以让 Chrome 工作”的话术（系统无障碍列表页及后续页面）
- 英文 -> “使用 Chrome”；“未提供描述。”（无障碍服务详情页，冒充 Chrome 服务）
- 英文 -> “允许 Chrome 完全控制你的设备？”并说明可查看/控制屏幕、读取屏幕内容、悬浮显示、跟踪交互并代操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: PermissionsActivity** | PermissionsActivity 伪装 Chrome 引导页，英文称需启用无障碍并按四步操作，点击“GO TO SETTINGS”跳系统设置。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表显示 Chrome 为关闭状态，顶部有该应用冒名 Chrome 的通知横幅；采集到无障碍钩子与探针后自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后 0.8 秒仍停留无障碍列表，界面文本为空，仅见冒名 Chrome 的启用无障碍通知横幅，无悬浮遮罩。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后 2.0 秒仍为无障碍列表，无新增界面文本；冒名 Chrome 通知横幅持续存在，探针显示遮罩数为 0。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入 Chrome 无障碍服务详情页，显示“Use Chrome”“Chrome shortcut”等选项及“未提供描述”，通知横幅仍在。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告弹窗要求允许 Chrome 完全控制设备，列明可读屏、悬浮显示和代操作；保留允许/拒绝按钮。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝授权后 2 秒回到桌面，应用未崩溃或弹窗，仅保留冒名 Chrome 通知横幅；结果为静默停留或降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒绝授权后 10.5 秒仍在桌面，界面无变化，冒名 Chrome 通知横幅持续；证实拒权后静默降级不骚扰。 | `step_02_refusal_10500ms_screen.png` |
