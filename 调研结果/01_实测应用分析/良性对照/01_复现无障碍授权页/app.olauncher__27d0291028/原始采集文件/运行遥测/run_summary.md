# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:48:03
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`app.olauncher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 7 步，UTG 唯一节点 `10` 个，有向边 `11` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 7 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_07_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`app.olauncher/app.olauncher.MainActivity` | hooks=`[]` | overlays=`0` | texts=`App / lock layout description to be used a unique id to lock screen / 3:49 / Wed, 25 Nov, 100% / Set as default launcher`
- **Back 后 +5.5s**：`app.olauncher/app.olauncher.MainActivity` | hooks=`[]` | overlays=`0` | texts=`App / lock layout description to be used a unique id to lock screen / 3:49 / Wed, 25 Nov, 100% / Set as default launcher`
- **Back 后 +10.5s**：`app.olauncher/app.olauncher.MainActivity` | hooks=`[]` | overlays=`0` | texts=`App / lock layout description to be used a unique id to lock screen / 3:49 / Wed, 25 Nov, 100% / Set as default launcher`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 7 | 82 / 否 | `click` → [6] Button text="Cancel" id=button2 (click) center=(577 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `app.olauncher` / `MainActivity` | `-` | 8 | 145 / 否 | `long_press` → [540, 1400] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `app.olauncher` / `MainActivity` | `-` | 4 | 112 / 否 | `click` → [4] TextView text="Okay" id=tvAction (click) center=(87 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `app.olauncher` / `MainActivity` | `-` | 20 | 185 / 否 | `swipe` → [540, 1900] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `app.olauncher` / `MainActivity` | `-` | 27 | 211 / 否 | `click` → [27] TextView text="Off" id=toggleLock (click) center=( | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `app.olauncher` / `MainActivity` | `-` | 5 | 279 / 否 | `click` → [5] TextView text="Enable" id=tvAction (click) center=( | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 208 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_07_layout.xml` + `step_07_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set Olauncher as your default home app?` | `Olauncher` | `Pixel Launcher` | `Cancel` | `Set as default`
- **Step 2 (`app.olauncher/MainActivity`)**: `App` | `lock layout description to be used a unique id to lock ` | `3:48` | `Wed, 25 Nov, 100%` | `1. Swipe up for all apps 2. Long press anywhere for set`
- **Step 3 (`app.olauncher/MainActivity`)**: `Olauncher` | `Close` | `Welcome to the settings!   Remember, if you have any qu` | `Okay`
- **Step 4 (`app.olauncher/MainActivity`)**: `Olauncher` | `Set as default launcher` | `About and FAQs` | `More features…` | `Home screen` | `Apps on home screen` | `4` | `Show date time` | `On` | `App alignment`
- **Step 5 (`app.olauncher/MainActivity`)**: `Show date time` | `On` | `App alignment` | `Left` | `Screen time` | `Off` | `Appearance` | `Auto show keyboard` | `Daily new wallpaper` | `Notification bar`
- **Step 6 (`app.olauncher/MainActivity`)**: `Gestures` | `Close` | `Please turn on Olauncher's accessibility service in you` | `Not working?` | `Enable`
- **Step 7 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Olauncher` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先取消系统默认桌面设置，进入极简桌面并长按呼出设置；开启双击锁屏时以无障碍说明引导跳转系统授权，拒权后返回桌面反复显示「设为默认启动器」入口，形成被困诱导页。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 中文：将 Olauncher 设为默认主屏幕应用？（系统角色页，提供取消/设为默认）
- 英文 -> 中文：欢迎来到设置！如有问题，关于页面有答案。（欢迎弹窗，Okay 关闭）
- 英文 -> 中文：请在设备设置中开启 Olauncher 无障碍服务以启用双击锁屏；该服务仅用于此功能，不收集或分享任何数据。（无障碍说明弹窗）
- 英文 -> 中文：启用双击锁屏手势需要无障碍权限；Olauncher 经此服务获取的任何数据都不会离开你的设备。（服务详情页）
- 英文 -> 中文：允许 Olauncher 完全控制你的设备？适合无障碍需求应用，不适合多数应用；可查看控制屏幕、跟踪交互并代为操作。（系统警告弹窗）
- 英文 -> 中文：将 Olauncher 设为默认启动器（拒权返回桌面上的入口）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestRoleActivity** | 系统默认主屏角色页，询问是否将 Olauncher 设为默认主屏；列出 Pixel Launcher，并提供取消与设为默认，本步点击取消。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | Olauncher 主屏首次进入，显示时间日期、100% 电量及上滑应用/长按设置提示；本步长按空白处打开设置。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 主屏弹出英文欢迎弹窗，称有疑问可看关于页，按钮 Okay；本步点击 Okay 关闭并露出设置页。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | Olauncher 设置页上半部，含设为默认启动器、关于、主屏应用数、日期时间与外观；本步下滑寻找双击锁屏项。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 设置页下半部外观与手势项，可见自动键盘、每日壁纸、通知栏、主题及 Off 开关；本步点击双击锁屏行的 Off。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 手势说明弹窗称开启无障碍服务可启用双击锁屏，并称不收集共享数据；有 Enable 按钮，本步点击跳系统设置。 | `step_06_action.png` |
| 7 | **Step 7: [无障碍列表页]** | 系统无障碍设置页，下载应用列表显示 Olauncher 为 Off，另有搜索、屏幕阅读器与显示项；采集 hook 后自动终止。 | `step_07_screen.png` |
| 8 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍停留系统无障碍设置页，无通知横幅、无悬浮遮罩，页面文本暂未采集。 | `step_07_probe_800ms_screen.png` |
| 9 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针，系统无障碍设置页保持稳定，仍无通知与遮罩，未出现覆盖层诱导。 | `step_07_probe_2000ms_screen.png` |
| 10 | **服务详情页** | Olauncher 无障碍服务详情页，含 Use Olauncher、Olauncher shortcut 为 Off 与隐私说明；称权限仅用于双击锁屏且数据不离设备。 | `step_07_service_detail_screen.png` |
| 11 | **系统警告弹窗(点Deny)** | 系统全权控制警告弹窗，说明可查看控制屏幕、跟踪交互并代为操作，提供 Allow/Deny；本步检查后选择拒绝。 | `step_07_system_warning_screen.png` |
| 12 | **拒权返回 +2.0s** | 拒绝无障碍权限后 2 秒返回 Olauncher 主屏，仅见时间日期与「设为默认启动器」入口，无取消关闭，形成被困诱导页。 | `step_07_refusal_2000ms_screen.png` |
| 13 | **拒权返回 +10.5s** | 拒权返回 10.5 秒后仍停在 Olauncher 主屏，同样显示「设为默认启动器」入口，无退出或取消，持续被困。 | `step_07_refusal_10500ms_screen.png` |
