# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:16:50
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`sops.system.android.updater`（静态标签：`malicious` / `SpyAgent` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `7` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`sops.system.android.updater/sops.system.android.updater.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Your Device is not Supported as of now. / Application is now Uninstalling. / OK`
- **Back 后 +5.5s**：`sops.system.android.updater/sops.system.android.updater.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Your Device is not Supported as of now. / Application is now Uninstalling. / OK`
- **Back 后 +10.5s**：`sops.system.android.updater/sops.system.android.updater.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Your Device is not Supported as of now. / Application is now Uninstalling. / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 339 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `sops.system.android.updater` / `MainActivity` | `-` | 3 | 150 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `sops.system.android.updater` / `MainActivity` | `-` | 2 | 123 / 否 | `click` → [2] Button text="OK" id=button1 (click) center=(887,115 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 218 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Google Play Service to access` | `SMS` | `send and view SMS messages` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Call logs` | `read and write phone call log` | `Phone`
- **Step 2 (`sops.system.android.updater/MainActivity`)**: `Google Play Service` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`sops.system.android.updater/MainActivity`)**: `Please enable 'Accessibility' for 'Google Play Service'` | `OK`
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Play Service` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用先请求短信、联系人、通话记录、麦克风、定位等敏感权限，再伪装成Google Play服务并以旧版兼容提示诱导开启无障碍；用户拒绝后不退出，而是重弹“设备不支持/正在卸载”的恐吓弹窗继续施压。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 选择允许Google Play服务访问的内容（Step 1 权限总览页）
- 英文 -> 发送和查看短信、访问照片/媒体/文件、联系人、通话记录、拨打电话、录音、定位（Step 1 权限总览页）
- 英文 -> 此应用为旧版Android构建，可能无法正常运行；请检查更新或联系开发者（Step 2 伪Google Play服务弹窗）
- 英文 -> 请为Google Play服务开启无障碍以使其工作，点OK前往无障碍设置（Step 3 诱导弹窗）
- 英文 -> 使用Google Play服务；Google Play服务快捷方式/音量键快捷方式（无障碍列表/服务详情页）
- 英文 -> 允许Google Play服务完全控制你的设备？（系统警告弹窗）
- 英文 -> 完全控制适合辅助无障碍需求的应用，不适用于大多数应用（系统警告弹窗）
- 英文 -> 可查看并控制屏幕，读取屏幕所有内容并覆盖显示在其他应用上（系统警告弹窗）
- 英文 -> 可观察并执行操作，跟踪与应用或硬件传感器的交互，并代表你操作应用（系统警告弹窗）
- 英文 -> 你的设备目前不受支持（拒权后恐吓弹窗）
- 英文 -> 应用正在卸载（拒权后恐吓弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 权限总览页伪装为Google Play服务，罗列短信、文件、联系人、通话记录、电话、麦克风、定位等敏感权限；点继续，无通知遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 应用内弹出伪装Google Play服务提示，称旧版Android可能异常，建议检查更新或联系开发者；点OK，无通知遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 应用内弹窗称需为Google Play服务开启无障碍才能工作，并引导点OK进入无障碍设置；无通知与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | 系统无障碍列表的已下载应用中出现Google Play服务且为关闭；采集到设置钩子/探针后自动终止，无通知遮罩。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留无障碍设置页，UI文本为空，无通知横幅、遮罩为0，页面暂未变化。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍为无障碍设置页，无文本与通知横幅，遮罩为0，未出现覆盖层或新跳转。 | `step_04_probe_2000ms_screen.png` |
| 7 | **服务详情页** | Google Play服务无障碍详情页，含Use Google Play Service开关、快捷方式与音量键选项；仅检查详情/警告，无遮罩。 | `step_04_service_detail_screen.png` |
| 8 | **系统警告弹窗(点Deny)** | 系统高风险警告：问是否允许Google Play服务完全控制设备，列明读屏、覆盖显示和代操作风险；含允许/拒绝，无遮罩。 | `step_04_system_warning_screen.png` |
| 9 | **拒权返回 +2.0s** | 拒权返回应用后重弹恐吓框：称设备暂不支持、应用正在卸载，仅OK；属拒权后重启诱导，无通知遮罩。 | `step_04_refusal_2000ms_screen.png` |
| 10 | **拒权返回 +10.5s** | 拒权返回10.5秒后仍显示同一恐吓框：设备暂不支持、应用正在卸载，仅OK；确认拒权后循环诱导，无通知遮罩。 | `step_04_refusal_10500ms_screen.png` |
