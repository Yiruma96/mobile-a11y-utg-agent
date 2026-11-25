# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:19:19
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.fakebook`（静态标签：`malicious` / `GnatSpy` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 27 | 275 / 否 | `click` → [27] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.fakebook` / `Fb_Home` | `-` | 3 | 151 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.fakebook` / `Fb_Home` | `-` | 5 | 83 / 否 | `click` → [1] EditText text="Enter Email or Phone" id=FB_EMAIL (c | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.fakebook` / `Fb_Home` | `-` | 5 | 83 / 否 | `type` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.fakebook` / `Fb_Home` | `-` | 5 | 79 / 否 | `click` → [2] EditText text="Enter Password" id=FB_PASSWORD (clic | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.fakebook` / `Fb_Home` | `-` | 5 | 79 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.fakebook` / `Fb_Home` | `-` | 5 | 79 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.fakebook` / `Fb_Home` | `-` | 5 | 79 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow App System Installer to access` | `Contacts` | `access your contacts` | `SMS` | `send and view SMS messages` | `Files and media` | `access photos, media, and files on your device` | `Microphone` | `record audio` | `Phone`
- **Step 2 (`com.fakebook/Fb_Home`)**: `App System Installer` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.fakebook/Fb_Home`)**: `Enter Email or Phone` | `Enter Password` | `LOG IN` | `FORGOT PASSWORD?` | `CREATE NEW FACEBOOK ACCOUNT`
- **Step 4 (`com.fakebook/Fb_Home`)**: `Enter Email or Phone` | `Enter Password` | `LOG IN` | `FORGOT PASSWORD?` | `CREATE NEW FACEBOOK ACCOUNT`
- **Step 5 (`com.fakebook/Fb_Home`)**: `test@example.com` | `Enter Password` | `LOG IN` | `FORGOT PASSWORD?` | `CREATE NEW FACEBOOK ACCOUNT`
- **Step 6 (`com.fakebook/Fb_Home`)**: `test@example.com` | `Enter Password` | `LOG IN` | `FORGOT PASSWORD?` | `CREATE NEW FACEBOOK ACCOUNT`
- **Step 7 (`com.fakebook/Fb_Home`)**: `test@example.com` | `Enter Password` | `LOG IN` | `FORGOT PASSWORD?` | `CREATE NEW FACEBOOK ACCOUNT`
- **Step 8 (`com.fakebook/Fb_Home`)**: `test@example.com` | `Enter Password` | `LOG IN` | `FORGOT PASSWORD?` | `CREATE NEW FACEBOOK ACCOUNT`

## 中文逐页引导链路解读

> **全链路总结**：应用先经系统权限审查页，以“应用系统安装器”名义请求通讯录、短信、文件媒体、麦克风、电话和通话记录，再以旧版兼容提示过渡到仿 Facebook 登录页收集邮箱/密码；本轨迹未测试拒绝授权，后续静态跳转暴露 CallRecorderReceiver 与 NetworkReceiver 等录音/网络组件。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “选择允许‘应用系统安装器’访问哪些权限”（Step 1 系统权限审查页）
- 英语 -> “联系人：访问你的联系人；短信：发送和查看短信；文件与媒体：访问照片、媒体和文件；麦克风：录音；电话：拨打和管理电话；通话记录：读写通话记录”（Step 1 权限审查页）
- 英语 -> “此应用为旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者”（Step 2 兼容性警告）
- 英语 -> “输入邮箱或手机号”“输入密码”“登录”“忘记密码？”“创建新的 Facebook 账户”（Step 3-5 仿 Facebook 登录页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审查页，以“应用系统安装器”名义请求通讯录、短信、文件、麦克风、电话、通话记录；点“继续”放行，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: Fb_Home** | 进入仿 Facebook 应用后弹出旧版 Android 兼容性警告，称应用可能无法正常运行；本步点“OK”关闭，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: Fb_Home** | 仿 Facebook 登录页，含邮箱/手机号、密码、登录、忘记密码、创建账户；本步点邮箱输入框，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: Fb_Home** | 仍为仿 Facebook 登录页；探针在邮箱框输入测试邮箱 test@example.com，页面未显示输入值，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: Fb_Home** | 同一仿 Facebook 登录页，邮箱框已显示 test@example.com；本步点密码框，继续收集伪造登录凭据，无遮罩。 | `step_05_action.png` |
| 6 | **Step 6: Fb_Home** | 仍停留在仿 Facebook 登录页，界面文字未变；探针静态跳转回 .activities.Fb_Home，无通知/遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: Fb_Home** | 仍为仿 Facebook 登录页，界面文字未变；探针静态跳转 .receivers.CallRecorderReceiver，暴露隐藏通话录音接收器。 | `step_07_screen.png` |
| 8 | **Step 8: Fb_Home** | 仍为仿 Facebook 登录页，界面文字未变；探针静态跳转 .receivers.NetworkReceiver，暴露网络监听/回传组件。 | `step_08_screen.png` |
