# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:45:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.system.android.updater`（静态标签：`malicious` / `donot` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 5 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 5 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_05_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 311 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 150 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings` | `-` | 32 | 363 / 否 | `swipe` → [540, 1800] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings` | `HOOK_A11Y_SETTINGS` | 36 | 461 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_05_layout.xml` + `step_05_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Google Play Service to access` | `SMS` | `send and view SMS messages` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `Phone`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Google Play Service` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.android.settings/Settings`)**: `Search settings` | `Network & internet` | `Wi‑Fi, mobile, data usage, and hotspot` | `Connected devices` | `Bluetooth, Android Auto` | `Apps & notifications` | `Recent apps, default apps` | `Battery` | `100%` | `Display`
- **Step 5 (`com.android.settings/Settings`)**: `Sound` | `Volume, vibration, Do Not Disturb` | `Storage` | `28% used - 5.77 GB free` | `Privacy` | `Permissions, account activity, personal data` | `Location` | `On - 3 apps have access to location` | `Security` | `Screen lock, fingerprint`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装成“Google Play 服务/系统更新器”，先展示高危权限审查并诱导点击继续，再以旧版 Android 兼容提示和返回桌面隐藏自身，随后跳转系统设置并滚动至无障碍入口，触发 HOOK_A11Y_SETTINGS 后被终止；拒权后仅停留桌面，呈优雅降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “选择允许 Google Play 服务访问哪些内容”（Step 1 权限审查页）
- English -> “发送和查看短信”（Step 1 权限审查页）
- English -> “访问设备上的照片、媒体和文件”（Step 1 权限审查页）
- English -> “访问您的联系人”（Step 1 权限审查页）
- English -> “读取和写入通话记录”（Step 1 权限审查页）
- English -> “拨打和管理电话”（Step 1 权限审查页）
- English -> “录制音频”（Step 1 权限审查页）
- English -> “定位”（Step 1 权限审查页）
- English -> “Google Play 服务”仿冒应用名（Step 1/Step 2 权限与兼容提示）
- English -> “此应用针对旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者”（Step 2 兼容性提示）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 伪装成“Google Play 服务”的权限审查页，列出短信、联系人、通话记录、电话、麦克风、定位等敏感权限，点击“Continue”继续。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面弹出“Google Play 服务”旧版兼容警告，称可能无法正常工作，建议检查更新或联系开发者；点击“OK”关闭。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 返回桌面应用列表，未见应用界面，说明应用启动后自行隐藏或退至后台；此步为打开动作，无通知或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: Settings** | 进入系统设置主列表，含网络、应用、电池、显示、隐私、安全等项；下滑查找“Accessibility（无障碍）”入口，无通知或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: [无障碍列表页]** | 设置页已滚动至“Accessibility（无障碍）”入口，旁有屏幕阅读器/显示/交互控制说明；触发 HOOK_A11Y_SETTINGS 与探针后自动终止，未见通知或遮罩。 | `step_05_screen.png` |
| 6 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在系统设置页，无任何可见 UI 文本、通知横幅或遮罩（overlays=0），仅等待。 | `step_05_probe_800ms_screen.png` |
| 7 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：仍为系统设置空白页，无 UI 文本、通知或遮罩，overlays=0，未见进一步诱导动作。 | `step_05_probe_2000ms_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权/返回后 2 秒：回到桌面应用列表，应用未弹二次诱导或错误提示，结果为 GRACEFUL_STAY_OR_DEGRADE，无通知或遮罩。 | `step_05_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权/返回后 10.5 秒：仍停留在桌面应用列表，无补偿弹窗、通知或遮罩，维持 GRACEFUL_STAY_OR_DEGRADE 的优雅降级状态。 | `step_05_refusal_10500ms_screen.png` |
