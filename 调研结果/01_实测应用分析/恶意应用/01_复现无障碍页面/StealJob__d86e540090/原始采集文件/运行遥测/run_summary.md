# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:58:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.update.gooqle`（静态标签：`malicious` / `StealJob` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `7` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.update.gooqle/com.jgoogle.android.gservicekns.MainActivity` | hooks=`[]` | overlays=`0` | texts=``
- **Back 后 +5.5s**：`com.update.gooqle/com.jgoogle.android.gservicekns.MainActivity` | hooks=`[]` | overlays=`0` | texts=``
- **Back 后 +10.5s**：`com.update.gooqle/com.jgoogle.android.gservicekns.MainActivity` | hooks=`[]` | overlays=`0` | texts=``

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 341 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.update.gooqle` / `MainActivity` | `-` | 3 | 152 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.update.gooqle` / `MainActivity` | `-` | 2 | 125 / 否 | `click` → [2] Button text="OK" id=button1 (click) center=(887,115 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 220 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Google Update Service to access` | `SMS` | `send and view SMS messages` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `Phone`
- **Step 2 (`com.update.gooqle/MainActivity`)**: `Google Update Service` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.update.gooqle/MainActivity`)**: `Please enable 'Accessibility' for 'Google Update Servic` | `OK`
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Update Service` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装成 Google 更新服务，先借系统权限审查索取短信、文件媒体、联系人、通话记录、电话、麦克风与定位，再以兼容性提示和“须开启无障碍才能工作”的弹窗诱导进入系统无障碍设置并申请完全控制设备；拒绝授权后主界面空白滞留，形成 TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English: Choose what to allow Google Update Service to access -> 选择允许“Google Update Service”访问哪些内容（系统权限审查页）
- English: send and view SMS messages; access photos, media, and files on your device; access your contacts; read and write phone call log; make and manage phone calls; record audio; Location -> 发送和查看短信；访问照片、媒体和文件；访问联系人；读写通话记录；拨打和管理电话；录音；定位（权限审查页权限说明）
- English: This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer. -> 该应用为旧版 Android 构建，可能无法正常工作，请检查更新或联系开发者（兼容性警告）
- English: Please enable 'Accessibility' for 'Google Update Service' to get this working. Tap on 'Ok' to go to Accessibility Settings. -> 请为“Google Update Service”开启“无障碍”才能正常工作，点击“确定”前往无障碍设置（主界面诱导弹窗）
- English: Allow Google Update Service to have full control of your device? -> 允许“Google Update Service”完全控制您的设备？（系统无障碍警告）
- English: Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适用于帮助无障碍需求的应用，不适用于大多数应用（系统无障碍警告）
- English: View and control screen; It can read all content on the screen and display content over other apps. -> 查看并控制屏幕；可读取屏幕所有内容并悬浮显示于其他应用之上（系统无障碍警告）
- English: View and perform actions; It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf. -> 查看并执行操作；可跟踪与应用或硬件传感器的交互，并代表您与应用交互（系统无障碍警告）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审查页，以“Google Update Service”名义请求短信、文件媒体、联系人、通话记录、电话、麦克风、定位；本步点 Continue 继续。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 应用主界面弹出 Android 兼容性警告，称该应用为旧版构建、可能无法正常工作；点 OK 关闭后进入原生流程。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 应用原生弹窗仅见 OK，称须为“Google Update Service”开启无障碍才能工作，点击后跳系统无障碍设置。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | 系统无障碍列表页，DOWNLOADED APPS 下“Google Update Service”显示 Off；采集到设置钩子与探针后自动终止。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在系统无障碍设置页，无新增文本、无通知横幅、无遮罩。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：页面文本为空、仍为无障碍设置页，overlays=0，未见应用悬浮层。 | `step_04_probe_2000ms_screen.png` |
| 7 | **服务详情页** | 无障碍服务详情页：显示“Use Google Update Service”、快捷键与音量键选项；尚未授权，仅巡检详情。 | `step_04_service_detail_screen.png` |
| 8 | **系统警告弹窗(点Deny)** | 系统无障碍授权警告：询问是否允许“Google Update Service”完全控制设备，列明读屏、悬浮、跟踪交互并代操作；随后走 Deny 拒绝。 | `step_04_system_warning_screen.png` |
| 9 | **拒权返回 +2.0s** | 拒绝授权后 2 秒返回应用 MainActivity，界面无文本/无控件，仍被困在诱导页，标记 TRAPPED_ON_LURE_SCREEN。 | `step_04_refusal_2000ms_screen.png` |
| 10 | **拒权返回 +10.5s** | 拒绝后 10.5 秒仍困于 MainActivity 空白诱导页，无文本、无通知、无遮罩，未放行到正常功能。 | `step_04_refusal_10500ms_screen.png` |
