# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:19:53
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.example.eventbot`（静态标签：`malicious` / `EventBot` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 5 步，UTG 唯一节点 `6` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 5 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_05_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Flash Update will not work correctly. / 1. Select Flash Update in Settings / 1 / 2. Turn on it / 2`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Flash Update will not work correctly. / 1. Select Flash Update in Settings / 1 / 2. Turn on it / 2`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Flash Update will not work correctly. / 1. Select Flash Update in Settings / 1 / 2. Turn on it / 2`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 11 | 147 / 否 | `click` → [11] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `wait` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `wait` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 7 | 105 / 否 | `click` → [7] Button text="Enable Flash Update" id=button1 (click | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 211 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_05_layout.xml` + `step_05_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Flash Update to access` | `Files and media` | `access photos, media, and files on your device` | `SMS` | `send and view SMS messages` | `Cancel` | `Continue`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Flash Update will not work correctly.` | `1. Select Flash Update in Settings` | `1` | `2. Turn on it` | `2` | `Enable Flash Update`
- **Step 5 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Flash Update` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用先请求文件媒体与短信权限并常驻桌面，循环弹出假“Flash Update”故障浮层诱导开启无障碍；进入系统授权页后若拒绝，返回桌面仍反复重弹同一诱骗浮层。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “选择允许 Flash Update 访问什么”，请求文件媒体与短信权限（权限审核页）
- English -> “Flash Update 将无法正常工作”，以故障恐吓促使用户开启（假浮层/服务详情页）
- English -> “1. 在设置中选择 Flash Update；2. 将其开启”，给出开启无障碍的诱导步骤（假浮层/拒权后重弹页）
- English -> “启用 Flash Update”，诱导点击跳转无障碍设置（假浮层/拒权后重弹页）
- English -> “必须启用 Flash Update 才能获得应用完整功能”，以功能不完整施压（无障碍服务详情页）
- English -> “允许 Flash Update 完全控制你的设备？”，系统高危授权警告（系统警告弹窗）
- English -> “可查看并控制屏幕/查看并执行操作”，说明无障碍可读屏、覆盖显示和代操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限审核页：Flash Update 请求文件媒体与短信权限；点“继续”放行，无通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面启动器页：等待后台约每20秒循环弹出假“Flash Update”浮层；本步仅等待，无通知、遮罩为0。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 仍在桌面等待：未出现系统通知或遮罩，预期假“Flash Update”浮层按约20秒循环再次弹出。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 假“Flash Update”浮层称将无法正常工作，列出“设置选择/开启”两步，仅“启用”键无取消，点击后跳系统无障碍。 | `step_04_action.png` |
| 5 | **Step 5: [无障碍列表页]** | 系统无障碍设置页：已下载应用中“Flash Update”为“关闭”；捕获无障碍钩子/探针后自动终止，无通知或遮罩。 | `step_05_screen.png` |
| 6 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停在无障碍设置页，无UI文本、无通知横幅，遮罩计数为0。 | `step_05_probe_800ms_screen.png` |
| 7 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍停在无障碍设置，无通知或浮层，遮罩计数为0，未见新动作。 | `step_05_probe_2000ms_screen.png` |
| 8 | **服务详情页** | 无障碍服务详情页：开关“Use Flash Update”未启用，提示必须开启才具完整功能；含音量键快捷键，仅检查未操作。 | `step_05_service_detail_screen.png` |
| 9 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗：称允许“Flash Update”完全控制设备，可读屏并代操作；有“允许/拒绝”，本步仅检查未点。 | `step_05_system_warning_screen.png` |
| 10 | **拒权返回 +2.0s** | 点“拒绝”返回桌面后2秒，假“Flash Update”启用无障碍诱导浮层再次自动弹出；无通知横幅，遮罩为0。 | `step_05_refusal_2000ms_screen.png` |
| 11 | **拒权返回 +10.5s** | 拒权返回10.5秒后，同一假“Flash Update”启用无障碍浮层仍反复重弹，显示拒权后诱骗并未停止。 | `step_05_refusal_10500ms_screen.png` |
