# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:49:37
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d`（静态标签：`malicious` / `EventBot` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 6 步，UTG 唯一节点 `9` 个，有向边 `10` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 6 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_06_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d/com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln` | hooks=`[]` | overlays=`0` | texts=`Select Flash Player in Settings / 1 / 2. Turn on it / 2 / Open Flash Player`
- **Back 后 +5.5s**：`com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d/com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln` | hooks=`[]` | overlays=`0` | texts=`Select Flash Player in Settings / 1 / 2. Turn on it / 2 / Open Flash Player`
- **Back 后 +10.5s**：`com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d/com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln` | hooks=`[]` | overlays=`0` | texts=`Select Flash Player in Settings / 1 / 2. Turn on it / 2 / Open Flash Player`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 11 | 147 / 否 | `click` → [11] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 143 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d` / `tvpeqghuln` | `-` | 9 | 74 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d` / `tvpeqghuln` | `-` | 2 | 17 / 是 | `click` → [2] Button text="Open Flash Player" id=button1 (click)  | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 211 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_06_layout.xml` + `step_06_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Flash Player to access` | `Files and media` | `access photos, media, and files on your device` | `SMS` | `send and view SMS messages` | `Cancel` | `Continue`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Flash Player` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d/tvpeqghuln`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d/tvpeqghuln`)**: `Open Flash Player`
- **Step 6 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Flash Player` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：EventBot样本伪装成Flash Player：启动后请求文件/媒体与短信权限，再引导至无障碍设置开启服务；拒权后反复回到“Select Flash Player in Settings”诱导页，形成无法退出的闭环。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 选择允许Flash Player访问哪些内容（Step 1 权限审核页）
- English -> 此应用为旧版Android构建，可能无法正常运行；请检查更新或联系开发者（Step 2 兼容性弹窗）
- English -> 打开Flash Player（Step 5 诱导按钮/拒权后诱导页）
- English -> 必须启用Flash Player才能获得应用完整功能，否则Flash Player将无法正常工作（服务详情页）
- English -> 允许Flash Player完全控制你的设备？（系统警告弹窗标题）
- English -> 可查看并控制屏幕，读取屏幕全部内容并悬浮显示于其他应用之上（系统警告弹窗）
- English -> 可跟踪你与应用的交互或硬件传感器，并代表你操作应用（系统警告弹窗）
- English -> 在设置中选择Flash Player / 打开它（拒权后诱导页步骤）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审核页，要求允许Flash Player访问文件媒体并收发短信；点击Continue继续，无通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面兼容性弹窗，称Flash Player为旧版Android构建、可能异常，建议更新或联系开发者；点击OK关闭，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面应用列表，见天气、Messages、Chrome、Search等，无应用专属界面；本步重新打开目标应用，无通知或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: tvpeqghuln** | 目标包tvpeqghuln已启动但仍显示桌面应用列表；等待全屏Activity/WebView加载，无通知横幅或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: tvpeqghuln** | 应用内诱导页仅显示Open Flash Player按钮；点击后预期进入无障碍授权引导，无通知横幅或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: [无障碍列表页]** | 进入系统无障碍设置，DOWNLOADED APPS下Flash Player为Off；捕获A11Y设置钩子与探针后终止，无遮罩。 | `step_06_screen.png` |
| 7 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留在无障碍设置页且文本为空；等待0.8秒，overlays=0，无通知横幅或遮罩。 | `step_06_probe_800ms_screen.png` |
| 8 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍在无障碍设置页且文本为空；等待2.0秒，overlays=0，无通知横幅或遮罩。 | `step_06_probe_2000ms_screen.png` |
| 9 | **服务详情页** | Flash Player服务详情页，有Use Flash Player开关与快捷键项；警告必须启用才可完整使用，否则无法正常工作。 | `step_06_service_detail_screen.png` |
| 10 | **系统警告弹窗(点Deny)** | 系统全控制警告弹窗称可读屏、显示悬浮层并代操作，提供Allow/Deny；本步检查未授权，overlays=0。 | `step_06_system_warning_screen.png` |
| 11 | **拒权返回 +2.0s** | 拒权返回2.0秒仍被困诱导页：提示在设置中选择Flash Player、第2步打开它，并保留Open Flash Player按钮。 | `step_06_refusal_2000ms_screen.png` |
| 12 | **拒权返回 +10.5s** | 拒权返回10.5秒仍停留在同一诱导页，反复要求设置中选择并开启Flash Player，未提供取消或退出路径。 | `step_06_refusal_10500ms_screen.png` |
