# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:55:17
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`org.thoughtcrime.securesms`（静态标签：`malicious` / `PUXIS` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 23 | 255 / 否 | `click` → [23] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `org.thoughtcrime.securesms` / `FirstActivity` | `-` | 3 | 153 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `org.thoughtcrime.securesms` / `ActDefault` | `-` | 4 | 149 / 否 | `click` → [4] Button text="Set as default SMS app" id=button1 (cl | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 8 | 116 / 否 | `click` → [6] RadioButton (unchecked) center=(898,1278) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 9 | 151 / 否 | `click` → [9] Button text="Set as default" id=button1 (click) cen | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `org.thoughtcrime.securesms` / `ActDefault` | `-` | 4 | 149 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `org.thoughtcrime.securesms` / `ActDefault` | `-` | 4 | 149 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `org.thoughtcrime.securesms` / `FirstActivity` | `-` | 5 | 750 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Raiffeisen SmsSecurity to access` | `Contacts` | `access your contacts` | `SMS` | `send and view SMS messages` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Call logs`
- **Step 2 (`org.thoughtcrime.securesms/FirstActivity`)**: `Raiffeisen SmsSecurity` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`org.thoughtcrime.securesms/ActDefault`)**: `Raiffeisen SmsSecurity` | `For the correct working of the application you wish to ` | `Set as default SMS app`
- **Step 4 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set Raiffeisen SmsSecurity as your default SMS app?` | `Messages` | `Current default` | `Raiffeisen SmsSecurity` | `Cancel` | `Set as default`
- **Step 5 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set Raiffeisen SmsSecurity as your default SMS app?` | `Messages` | `Current default` | `Raiffeisen SmsSecurity` | `Gets access to contacts, SMS, phone` | `Cancel` | `Set as default`
- **Step 6 (`org.thoughtcrime.securesms/ActDefault`)**: `Raiffeisen SmsSecurity` | `For the correct working of the application you wish to ` | `Set as default SMS app`
- **Step 7 (`org.thoughtcrime.securesms/ActDefault`)**: `Raiffeisen SmsSecurity` | `For the correct working of the application you wish to ` | `Set as default SMS app`
- **Step 8 (`org.thoughtcrime.securesms/FirstActivity`)**: `Raiffeisen SmsSecurity` | `SmsSecure - Quick Start Guide  It will be offered a fre` | `I have read the Quick Start Guide. Continue.` | `© Raiffeisen`

## 中文逐页引导链路解读

> **全链路总结**：应用仿冒莱夫艾森银行的 Raiffeisen SmsSecurity，先诱导授予通讯录、短信、电话、文件媒体和通话记录等宽泛权限，再要求设为默认短信应用，并用“安全快速指南”话术推动继续；链路中多次静态跳转到 USSD 弹窗与路由页，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“Choose what to allow Raiffeisen SmsSecurity to access” -> 中文：选择允许 Raiffeisen SmsSecurity 访问哪些内容（Step 1 权限审核页）
- 英文“send and view SMS messages”“make and manage phone calls”“access your contacts”“read and write phone call log” -> 中文：发送/查看短信、拨打和管理电话、访问通讯录、读写通话记录（Step 1）
- 英文“For the correct working of the application you wish to use it by default. Press Yes in the next window.” -> 中文：为使应用正常工作，希望您将其设为默认，并在下一窗口点“是”（Step 3/6/7 ActDefault）
- 英文“Set Raiffeisen SmsSecurity as your default SMS app?” -> 中文：将 Raiffeisen SmsSecurity 设为默认短信应用？（Step 4/5 系统角色请求页）
- 英文“Gets access to contacts, SMS, phone” -> 中文：可获得通讯录、短信、电话访问权（Step 5）
- 英文“It will be offered a free mobile application that was developed by our IT professionals and combines all modern development in the field of safety” -> 中文：将提供由 IT 专业人员开发、集成安全领域现代成果的免费手机应用（Step 8 快速指南）
- 英文“SmsSecure is a mobile application for generation one-time password for access to your account...” -> 中文：SmsSecure 可生成用于访问账户的一次性密码，并加密收到的短信、存入加密容器（Step 8）
- 英文“Follow the instructions in the SmsSecure Wizard... generate a unique password... use it as a standard program to work with sms.” -> 中文：按 SmsSecure 向导操作、生成唯一密码，并将其作为标准短信程序使用（Step 8）
- 英文“I have read the Quick Start Guide. Continue.” -> 中文：我已阅读快速指南，继续（Step 8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审核页，列出通讯录、短信、电话、文件媒体和通话记录等敏感权限，并以 Continue 继续；本步点击继续进入应用。 | `step_01_action.png` |
| 2 | **Step 2: FirstActivity** | 应用首屏弹出旧版 Android 兼容警告，仅可点 OK 关闭；无其他功能说明，本步点击 OK 绕过警告继续引导。 | `step_02_action.png` |
| 3 | **Step 3: ActDefault** | 应用内默认短信引导页，英文称需设为默认并让下窗口点 Yes，按钮为 Set as default SMS app；本步点击进入系统角色请求。 | `step_03_action.png` |
| 4 | **Step 4: RequestRoleActivity** | 系统默认短信角色请求页，询问是否将 Raiffeisen SmsSecurity 设为默认短信应用，提供取消与设为默认；本步选中该应用选项。 | `step_04_action.png` |
| 5 | **Step 5: RequestRoleActivity** | 同一系统角色页补充“可获得通讯录、短信、电话访问权”，仍以设为默认确认；本步点击 Set as default，等于同意让渡短信权限。 | `step_05_action.png` |
| 6 | **Step 6: ActDefault** | 界面仍停在默认短信引导页，重复“正确运行需设为默认并点 Yes”话术；本步无点击，探针静态跳转至 USSD 弹窗活动，风险可疑。 | `step_06_screen.png` |
| 7 | **Step 7: ActDefault** | 仍为默认短信引导页，继续以“设为默认才能正常工作”施压；本步无点击，静态跳转至应用 RoutingActivity，疑似进入后续诱导流程。 | `step_07_screen.png` |
| 8 | **Step 8: FirstActivity** | 应用内英文快速指南，自称银行 IT 团队免费安全应用，可生成一次性密码并加密短信；要求阅读后继续，本步静态跳转路由页。 | `step_08_screen.png` |
