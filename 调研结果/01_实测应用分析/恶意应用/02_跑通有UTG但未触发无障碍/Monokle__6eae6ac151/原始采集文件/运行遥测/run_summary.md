# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:54:06
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.wUzbekChat1`（静态标签：`malicious` / `Monokle` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.wUzbekChat1` / `IntroActivity` | `-` | 4 | 81 / 否 | `click` → [4] TextView text="START MESSAGING" id=start_messaging_ | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.wUzbekChat1` / `LaunchActivity` | `-` | 6 | 66 / 否 | `click` → [5] EditText (click) center=(640,517) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.wUzbekChat1` / `LaunchActivity` | `-` | 6 | 66 / 否 | `type` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.wUzbekChat1` / `LaunchActivity` | `-` | 6 | 78 / 否 | `click` → [1] FrameLayout (click) center=(1003,160) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.wUzbekChat1` / `LaunchActivity` | `-` | 3 | 112 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,120 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 56 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.wUzbekChat1` / `LaunchActivity` | `-` | 1 | 10 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.wUzbekChat1` / `LaunchActivity` | `-` | 1 | 10 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.wUzbekChat1/IntroActivity`)**: `UzbekChat` | `The world's fastest messaging app. It is free and secur` | `START MESSAGING`
- **Step 2 (`com.wUzbekChat1/LaunchActivity`)**: `USA` | `+` | `1` | `Please confirm your country code and enter your phone n`
- **Step 3 (`com.wUzbekChat1/LaunchActivity`)**: `USA` | `+` | `1` | `Please confirm your country code and enter your phone n`
- **Step 4 (`com.wUzbekChat1/LaunchActivity`)**: `USA` | `+` | `1` | `555 123 4567` | `Please confirm your country code and enter your phone n`
- **Step 5 (`com.wUzbekChat1/LaunchActivity`)**: `UzbekChat` | `Please allow UzbekChat to receive calls and SMS so that` | `OK`
- **Step 6 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow UzbekChat to make and manage phone calls?` | `Allow` | `Deny`
- **Step 7 (`com.wUzbekChat1/LaunchActivity`)**: `Loading...`
- **Step 8 (`com.wUzbekChat1/LaunchActivity`)**: `Loading...`

## 中文逐页引导链路解读

> **全链路总结**：该应用以 UzbekChat“全球最快、免费安全”的聊天入口诱导用户开始使用，收集美国 +1 手机号并请求短信/通话权限；系统授权弹窗后进入 Telegram 加载页，并静态跳转至 OneAudience 检查器及伪装系统更新的接收器。本次未实际测试拒绝授权结果。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “全球最快的消息应用，免费且安全”（IntroActivity 入口页）
- 英文 -> “开始聊天”（IntroActivity 按钮）
- 英文 -> “请确认国家代码并输入手机号”（LaunchActivity 手机号页）
- 英文 -> “请允许 UzbekChat 接收电话和短信，以便自动为你填入验证码”（LaunchActivity 权限说明页）
- 英文 -> “允许 UzbekChat 拨打和管理电话？”（系统权限弹窗）
- 英文 -> “加载中…”（LaunchActivity 加载页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: IntroActivity** | 入口介绍页，宣称“全球最快、免费安全”，点击 START MESSAGING 开始，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: LaunchActivity** | 手机号登录页，显示 USA +1 并提示确认国家代码、输入手机号；点击输入框，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: LaunchActivity** | 同一手机号页，向已聚焦输入框键入测试号码；页面无通知横幅或遮罩，继续等待提交。 | `step_03_action.png` |
| 4 | **Step 4: LaunchActivity** | 手机号已显示 555 123 4567，点击右上角勾选提交；无通知/遮罩，进入权限说明。 | `step_04_action.png` |
| 5 | **Step 5: LaunchActivity** | 短信/通话权限说明页，称允许后可自动代填验证码，点击 OK；无通知/遮罩，继续流程。 | `step_05_action.png` |
| 6 | **Step 6: GrantPermissionsActivity** | 系统电话权限弹窗，询问是否允许拨打电话和管理通话，含允许/拒绝；探针静态跳转至 Telegram LaunchActivity。 | `step_06_screen.png` |
| 7 | **Step 7: LaunchActivity** | 加载页仅显示 Loading...；探针直接静态跳转 OneAudienceReceiverChecker，无通知/遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: LaunchActivity** | 仍为加载页 Loading...；探针静态跳转伪装为系统更新的 MediaReceiver，无通知/遮罩。 | `step_08_screen.png` |
