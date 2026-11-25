# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:00:55
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`yps.eton.application`（静态标签：`malicious` / `SpyAgent` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `5` 个，有向边 `4` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / كشف رقم واسم المتصل المجهول`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 359 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `DeviceAdminAdd` | `-` | 3 | 158 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `DeviceAdminAdd` | `-` | 11 | 352 / 否 | `click` → [10] Button text="Cancel" id=cancel_button (click) cent | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 3 | 63 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow ‎‫كشف رقم واسم المتصل المجهول‬‎ to` | `Camera` | `take pictures and record video` | `Files and media` | `access photos, media, and files on your device` | `Call logs` | `read and write phone call log` | `SMS` | `send and view SMS messages` | `Contacts`
- **Step 2 (`com.android.settings/DeviceAdminAdd`)**: `كشف رقم واسم المتصل المجهول` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.android.settings/DeviceAdminAdd`)**: `Activate device admin app?` | `كشف رقم واسم المتصل المجهول` | `Activating this admin app will allow the app كشف رقم وا` | `Erase all data` | `Erase the phone's data without warning by performing a ` | `Lock the screen` | `Control how and when the screen locks.` | `Activate this device admin app` | `Cancel` | `Uninstall app`
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `‎‫كشف رقم واسم المتصل المجهول‬‎ keeps stopping` | `App info` | `Close app`

## 中文逐页引导链路解读

> **全链路总结**：应用以阿拉伯语“未知来电号码与姓名识别”工具为名，先批量申请相机、文件媒体、通话记录、短信、联系人、麦克风和电话权限，再诱导激活可清除数据与锁屏的设备管理员；用户拒绝后跳至无障碍设置并崩溃/终止，随后在无障碍列表拒权仍触发重新拉起无障碍设置。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 阿拉伯语 -> “未知来电号码与姓名识别/探测”（应用名，出现在权限页、设备管理页与通知横幅）
- 英语+阿拉伯语 -> “选择允许[未知来电识别]访问哪些权限”（系统权限复核页标题）
- 英语 -> “此应用为旧版 Android 构建，可能无法正常运行，请检查更新或联系开发者”（设备管理页兼容弹窗）
- 英语 -> “激活设备管理应用后，将允许其执行清除全部数据、锁定屏幕等操作”（设备管理激活页说明）
- 英语 -> “Activate this device admin app / Erase all data / Lock the screen”（设备管理激活页的授权诱导与高风险能力说明）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页，列出相机、文件媒体、通话记录、短信、联系人、麦克风和电话权限；点击“Continue”准备批量授权，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: DeviceAdminAdd** | 设备管理添加页先弹出旧版Android兼容提示，点“OK”关闭；应用通知横幅显示阿拉伯语应用名，遮罩0。 | `step_02_action.png` |
| 3 | **Step 3: DeviceAdminAdd** | 设备管理员激活页，说明可清除全部数据、锁定屏幕；本步点“Cancel”拒绝激活，通知横幅仍在，遮罩0。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | 无障碍设置页上弹出阿拉伯语应用“屡次停止”崩溃框，含“App info/Close app”；探针命中后终止，通知横幅仍在，遮罩0。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍处无障碍设置页，无可见文案；应用通知横幅持续，遮罩0，未见弹窗或诱导操作。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后2秒探针：无障碍设置页保持空白可见区；应用通知横幅仍活跃，遮罩0，说明跳转后未出现覆盖层。 | `step_04_probe_2000ms_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回后，无障碍列表显示该阿拉伯语应用为“Off”，可返回；动作触发再次拉起无障碍设置（RELAUNCHED_A11Y_SETTINGS）。 | `step_04_refusal_2000ms_screen.png` |
