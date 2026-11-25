# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:35:25
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`org.thoughtcrime.securesms`（静态标签：`malicious` / `Monokle` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `org.thoughtcrime.securesms` / `WelcomeActivity` | `-` | 3 | 82 / 否 | `click` → [3] Button text="CONTINUE" id=welcome_continue_button ( | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `org.thoughtcrime.securesms` / `WelcomeActivity` | `-` | 4 | 137 / 否 | `click` → [4] Button text="CONTINUE" id=button1 (click) center=(7 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 46 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 53 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 72 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `org.thoughtcrime.securesms` / `RegistrationActivity` | `-` | 8 | 144 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `org.thoughtcrime.securesms` / `RegistrationActivity` | `-` | 8 | 144 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`org.thoughtcrime.securesms/WelcomeActivity`)**: `Take privacy with you. Be yourself in every message.` | `Terms & Privacy Policy` | `CONTINUE`
- **Step 2 (`org.thoughtcrime.securesms/WelcomeActivity`)**: `+` | `Signal needs access to your contacts and media in order` | `NOT NOW` | `CONTINUE`
- **Step 3 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Signal to access your contacts?` | `Allow` | `Deny`
- **Step 4 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Signal to make and manage phone calls?` | `Allow` | `Deny`
- **Step 5 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Signal to access photos, media, and files on your` | `Allow` | `Deny`
- **Step 6 (`org.thoughtcrime.securesms/RegistrationActivity`)**: `Enter your phone number to get started` | `You will receive a verification code. Carrier rates may` | `United States` | `1` | `Phone Number` | `(555) 521-5556` | `NEXT`
- **Step 7 (`org.thoughtcrime.securesms/RegistrationActivity`)**: `Enter your phone number to get started` | `You will receive a verification code. Carrier rates may` | `United States` | `1` | `Phone Number` | `(555) 521-5556` | `NEXT`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：该应用以仿Signal欢迎页和隐私口号开场，先用权限说明诱导连续授予联系人、电话、媒体权限，再进入手机号注册；随后静态引导跳转到VoiceCallShare、SmsSendtoActivity及桌面/分享Activity，未测试拒权且未见通知或遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “随身携带隐私。在每条消息中做自己。”（Step 1 欢迎页）
- 英文 -> “Signal需要访问你的联系人和媒体，以便连接朋友、交换消息并进行安全通话”（Step 2 权限引导页）
- 英文 -> “输入你的手机号以开始使用”（Step 6/7 注册页）
- 英文 -> “你将收到验证码。可能产生运营商费用。”（Step 6/7 注册页）
- 英文 -> “允许Signal访问你的联系人？”（Step 3 系统通讯录授权页）
- 英文 -> “允许Signal拨打和管理电话？”（Step 4 系统电话授权页）
- 英文 -> “允许Signal访问你设备上的照片、媒体和文件？”（Step 5 系统媒体授权页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: WelcomeActivity** | 欢迎页：以“随身携带隐私、每条消息做自己”口号及条款链接包装；点击CONTINUE进入下一步，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: WelcomeActivity** | 权限引导页：称Signal需访问联系人和媒体以连接好友、收发消息及安全通话；点CONTINUE继续，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: GrantPermissionsActivity** | 系统通讯录授权页：询问“允许Signal访问联系人？”；本步点击Allow同意，未测试Deny，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: GrantPermissionsActivity** | 系统电话授权页：询问“允许Signal拨打和管理电话？”；本步点Allow同意，未测试拒权，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: GrantPermissionsActivity** | 系统媒体授权页：询问“允许Signal访问照片、媒体和文件？”；本步点Allow同意，未测试拒权，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: RegistrationActivity** | 注册页：要求输入手机号，称将收验证码且可能计费；探针静态跳转至.webrtc.VoiceCallShare，无通知/遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: RegistrationActivity** | 注册页重复：仍要求手机号并提示验证码/运营商计费；静态跳转至.SmsSendtoActivity，无通知/遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 系统桌面/应用列表页：显示周三11月25日、Messages、Chrome等；探针静态跳转至.ShareActivity，无通知/遮罩。 | `step_08_screen.png` |
