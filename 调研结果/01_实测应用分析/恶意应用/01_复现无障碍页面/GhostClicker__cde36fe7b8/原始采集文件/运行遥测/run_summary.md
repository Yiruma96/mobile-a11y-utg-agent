# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:58:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.flashalertsoncalltt.vnm`（静态标签：`malicious` / `GhostClicker` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 6 步，UTG 唯一节点 `8` 个，有向边 `10` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 6 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_06_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.flashalertsoncalltt.vnm/com.avlon.flashalerts.ToggleFlashSettings` | hooks=`[]` | overlays=`0` | texts=`Flash Alerts/Notification / Flash Alerts - Notification / FLASH ON CALL / FLASH ON SMS / FLASH ON NOTIFICATION`
- **Back 后 +5.5s**：`com.flashalertsoncalltt.vnm/com.avlon.flashalerts.ToggleFlashSettings` | hooks=`[]` | overlays=`0` | texts=`Flash Alerts/Notification / Flash Alerts - Notification / FLASH ON CALL / FLASH ON SMS / FLASH ON NOTIFICATION`
- **Back 后 +10.5s**：`com.flashalertsoncalltt.vnm/com.avlon.flashalerts.ToggleFlashSettings` | hooks=`[]` | overlays=`0` | texts=`Flash Alerts/Notification / Flash Alerts - Notification / FLASH ON CALL / FLASH ON SMS / FLASH ON NOTIFICATION`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 15 | 167 / 否 | `click` → [15] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.flashalertsoncalltt.vnm` / `SplashScreenActivity` | `-` | 3 | 156 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.flashalertsoncalltt.vnm` / `SplashScreenActivity` | `-` | 7 | 45 / 否 | `click` → [5] Button text="START" id=btnStart (click) center=(875 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.flashalertsoncalltt.vnm` / `ToggleFlashSettings` | `-` | 14 | 113 / 否 | `click` → [8] ToggleButton id=tgNotification (click,unchecked) ce | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.flashalertsoncalltt.vnm` / `ToggleFlashSettings` | `-` | 4 | 120 / 否 | `click` → [3] Button text="yes" id=btnYes (click) center=(340,133 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 227 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_06_layout.xml` + `step_06_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Flash Alerts on Call and… to acces` | `Camera` | `take pictures and record video` | `SMS` | `send and view SMS messages` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`com.flashalertsoncalltt.vnm/SplashScreenActivity`)**: `Flash Alerts on Call and…` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.flashalertsoncalltt.vnm/SplashScreenActivity`)**: `Flash Alerts/Notification` | `START` | `GET MORE` | `RATE US`
- **Step 4 (`com.flashalertsoncalltt.vnm/ToggleFlashSettings`)**: `Flash Alerts/Notification` | `Flash Alerts - Notification` | `FLASH ON CALL` | `FLASH ON SMS` | `FLASH ON NOTIFICATION` | `RATE US` | `GET MORE`
- **Step 5 (`com.flashalertsoncalltt.vnm/ToggleFlashSettings`)**: `notification alert` | `notification requires accessibility service to be on. d` | `yes` | `no`
- **Step 6 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Flash Alerts on Call and SMS` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先引导授予相机、短信、电话运行时权限，再以旧版兼容警告和“通知需无障碍”的误导弹窗，把用户引至系统无障碍设置；一旦拒绝授权即返回并停留在闪光开关页，形成诱导授权陷阱。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Choose what to allow Flash Alerts on Call and… to access -> 选择允许“来电闪光提醒”访问哪些权限（权限总览页）
- This app was built for an older version of Android and may not work properly. Try checking for updates, or contact the developer. -> 应用为旧版Android构建、可能无法正常工作，请检查更新或联系开发者（启动页系统警告）
- notification requires accessibility service to be on. do you want to enable notification feature? -> 通知功能需要开启无障碍服务，是否启用通知功能（应用内误导弹窗）
- Allow Flash Alerts on Call and SMS to have full control of your device? -> 允许“来电短信闪光提醒”完全控制你的设备吗（系统高风险授权警告）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适用于辅助无障碍需求的app，但不适用于大多数app（系统警告说明）
- No description provided. -> 未提供描述（无障碍服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限总览页，列出相机、短信、电话权限及说明；点击“继续”准备一次性授予运行时权限。 | `step_01_action.png` |
| 2 | **Step 2: SplashScreenActivity** | 应用启动页弹出旧版Android兼容警告，称应用可能无法正常工作；点击“OK”关闭警告继续进入。 | `step_02_action.png` |
| 3 | **Step 3: SplashScreenActivity** | 应用主页/启动页，显示“闪光提醒/通知”“START”“GET MORE”“RATE US”；点击START进入闪光设置。 | `step_03_action.png` |
| 4 | **Step 4: ToggleFlashSettings** | 闪光设置页，含来电/短信/通知闪光开关及评分、更多；点击“通知闪光”开关触发无障碍引导。 | `step_04_action.png` |
| 5 | **Step 5: ToggleFlashSettings** | 应用内弹窗称“通知需开启无障碍服务”，并问是否启用通知功能；点击“yes”继续走向系统无障碍授权。 | `step_05_action.png` |
| 6 | **Step 6: [无障碍列表页]** | 系统无障碍设置列表，已列出该应用开关为关闭；探针捕获无障碍设置钩子后自动终止，未继续授权。 | `step_06_screen.png` |
| 7 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停系统无障碍设置页，界面文本为空、遮罩0；未发现弹窗或跳转。 | `step_06_probe_800ms_screen.png` |
| 8 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍在系统无障碍设置页，界面文本为空、遮罩0；等待期间无新弹窗。 | `step_06_probe_2000ms_screen.png` |
| 9 | **服务详情页** | 无障碍服务详情页，显示应用名、启用项、快捷键与“未提供描述”；仅检查详情未授权。 | `step_06_service_detail_screen.png` |
| 10 | **系统警告弹窗(点Deny)** | 系统高风险授权警告：允许后应用可查看/控制屏幕并代操作；本步检查弹窗，未点允许。 | `step_06_system_warning_screen.png` |
| 11 | **拒权返回 +2.0s** | 拒绝无障碍授权返回应用开关页，界面仍为来电/短信/通知闪光开关；流程被卡在诱导页。 | `step_06_refusal_2000ms_screen.png` |
| 12 | **拒权返回 +10.5s** | 拒权返回10.5秒后仍停在应用闪光开关页，无取消/退出引导；持续被困于诱导授权页。 | `step_06_refusal_10500ms_screen.png` |
