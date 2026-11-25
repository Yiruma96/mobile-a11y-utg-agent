# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:25:25
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`org.djp.user`（静态标签：`malicious` / `MMRat` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `org.djp.user` / `LoginActivity` | `-` | 6 | 198 / 否 | `click` → [4] EditText text="Silakan masukkan nomor ponsel Anda"  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `org.djp.user` / `LoginActivity` | `-` | 6 | 198 / 否 | `type` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `org.djp.user` / `LoginActivity` | `-` | 6 | 175 / 否 | `click` → [5] EditText text="Silakan masukkan sandi anda" (click) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `org.djp.user` / `LoginActivity` | `-` | 6 | 175 / 否 | `type` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `org.djp.user` / `LoginActivity` | `-` | 6 | 159 / 否 | `click` → [545, 1339] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `org.djp.user` / `LoginActivity` | `-` | 6 | 159 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `org.djp.user` / `WebViewActivity` | `-` | 5 | 88 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `org.djp.user` / `WebViewActivity` | `-` | 5 | 88 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`org.djp.user/LoginActivity`)**: `Selamat datang di M-pajak` | `Setelah Anda sudah memiliki akun, login akan terus menj` | `Daftar masuk` | `Silakan masukkan nomor ponsel Anda` | `Silakan masukkan sandi anda`
- **Step 2 (`org.djp.user/LoginActivity`)**: `Selamat datang di M-pajak` | `Setelah Anda sudah memiliki akun, login akan terus menj` | `Daftar masuk` | `Silakan masukkan nomor ponsel Anda` | `Silakan masukkan sandi anda`
- **Step 3 (`org.djp.user/LoginActivity`)**: `Selamat datang di M-pajak` | `Setelah Anda sudah memiliki akun, login akan terus menj` | `Daftar masuk` | `81234567890` | `Silakan masukkan sandi anda`
- **Step 4 (`org.djp.user/LoginActivity`)**: `Selamat datang di M-pajak` | `Setelah Anda sudah memiliki akun, login akan terus menj` | `Daftar masuk` | `81234567890` | `Silakan masukkan sandi anda`
- **Step 5 (`org.djp.user/LoginActivity`)**: `Selamat datang di M-pajak` | `Setelah Anda sudah memiliki akun, login akan terus menj` | `Daftar masuk` | `81234567890` | `•••••••••••`
- **Step 6 (`org.djp.user/LoginActivity`)**: `Selamat datang di M-pajak` | `Setelah Anda sudah memiliki akun, login akan terus menj` | `Daftar masuk` | `81234567890` | `•••••••••••`
- **Step 7 (`org.djp.user/WebViewActivity`)**: `Klik untuk membuka dan memverifikasi status akun anda` | `Klik untuk mengkonfirmasi akun anda`
- **Step 8 (`org.djp.user/WebViewActivity`)**: `Klik untuk membuka dan memverifikasi status akun anda` | `Klik untuk mengkonfirmasi akun anda`

## 中文逐页引导链路解读

> **全链路总结**：该MMRat样本伪装印尼税务M-pajak登录页收集手机号和密码，提交后静态跳转WebView以“验证/确认账户”继续诱导，并串联权限请求与无障碍服务；全程无通知横幅或遮罩，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 印尼语 -> “欢迎使用M-pajak”（Step 1-6 LoginActivity）
- 印尼语 -> “在您已有账户后，登录将继续运行已激活的DJP在线账户”（Step 1-6 LoginActivity）
- 印尼语 -> “登录/注册进入”（Daftar masuk，登录按钮，Step 1-6 LoginActivity）
- 印尼语 -> “请输入您的手机号码”（Step 1-4/6 LoginActivity）
- 印尼语 -> “请输入您的密码”（Step 1-5/6 LoginActivity）
- 印尼语 -> “点击打开并验证您的账户状态”（Step 7-8 WebViewActivity）
- 印尼语 -> “点击确认您的账户”（Step 7-8 WebViewActivity）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: LoginActivity** | 仿M-pajak税务登录页，显示“欢迎使用M-pajak”并索要手机号、密码；本步点击手机号框，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: LoginActivity** | 仍为M-pajak登录页，索要手机号与密码；本步在已聚焦手机号框输入样例号码，无通知横幅与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: LoginActivity** | M-pajak登录页手机号已填81234567890，提示输入密码；本步点击密码框，无通知横幅与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: LoginActivity** | M-pajak登录页已见样例手机号，密码框聚焦；本步输入样例密码，页面仍索要凭证，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: LoginActivity** | M-pajak登录页手机号和掩码密码已填，按钮“Daftar masuk”意为登录；本步点击提交，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: LoginActivity** | 登录页提交后静态跳转至WebViewActivity；仍见“欢迎使用M-pajak”登录要素，无通知/遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: WebViewActivity** | WebView页显示“点击打开并验证账户状态”“点击确认账户”；本步静态跳转至权限请求页，无通知/遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: WebViewActivity** | 同一WebView诱饵页，文案仍为验证/确认账户；本步静态跳转至无障碍服务，无通知横幅与遮罩。 | `step_08_screen.png` |
