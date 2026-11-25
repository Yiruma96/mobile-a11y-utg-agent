# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:53:34
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.skype.raider`（静态标签：`malicious` / `Monokle` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.skype.raider` / `UnifiedLandingPageActivity` | `-` | 6 | 103 / 否 | `click` → [3] EditText text="Enter your email, phone number or Sk | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.skype.raider` / `UnifiedLandingPageActivity` | `-` | 4 | 89 / 否 | `type` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.skype.raider` / `UnifiedLandingPageActivity` | `-` | 4 | 56 / 否 | `click` → [4] TextView text="" desc="Next button" id=sign_in_nex | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.skype.raider` / `SignInActivity` | `-` | 6 | 129 / 否 | `click` → [4] EditText text="Password" desc="Password, enter your | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.skype.raider` / `SignInActivity` | `-` | 6 | 129 / 否 | `type` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.skype.raider` / `SignInActivity` | `-` | 6 | 116 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.skype.raider` / `SignInActivity` | `-` | 6 | 116 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.skype.raider` / `SignInActivity` | `-` | 6 | 116 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.skype.raider/UnifiedLandingPageActivity`)**: `Sign in` | `Skype name, email or phone` | `Enter your email, phone number or Skype name` | `` | `Next button` | `Create account`
- **Step 2 (`com.skype.raider/UnifiedLandingPageActivity`)**: `Sign in` | `Skype name, email or phone` | `Enter your email, phone number or Skype name` | `` | `Next button`
- **Step 3 (`com.skype.raider/UnifiedLandingPageActivity`)**: `Sign in` | `Skype name, email or phone` | `testuser123` | `` | `Next button`
- **Step 4 (`com.skype.raider/SignInActivity`)**: `Sign in` | `Skype name, email or phone` | `Skype Name testuser123` | `Password` | `Password, enter your password here` | `` | `Next button` | `Problems signing in?`
- **Step 5 (`com.skype.raider/SignInActivity`)**: `Sign in` | `Skype name, email or phone` | `Skype Name testuser123` | `Password` | `Password, enter your password here` | `` | `Next button` | `Problems signing in?`
- **Step 6 (`com.skype.raider/SignInActivity`)**: `Sign in` | `Skype name, email or phone` | `Skype Name testuser123` | `••••••••••••` | `Password, 12 dots` | `` | `Next button` | `Problems signing in?`
- **Step 7 (`com.skype.raider/SignInActivity`)**: `Sign in` | `Skype name, email or phone` | `Skype Name testuser123` | `••••••••••••` | `Password, 12 dots` | `` | `Next button` | `Problems signing in?`
- **Step 8 (`com.skype.raider/SignInActivity`)**: `Sign in` | `Skype name, email or phone` | `Skype Name testuser123` | `••••••••••••` | `Password, 12 dots` | `` | `Next button` | `Problems signing in?`

## 中文逐页引导链路解读

> **全链路总结**：Monokle家族仿冒Skype，先以登录落地页收集账号，再以密码页收集密码，随后静态跳转至SpiceActivity及微软账户选择/添加账户组件；全程无通知横幅或遮罩，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 登录（Step1-8）
- 英语 -> Skype用户名、邮箱或手机号（Step1-8）
- 英语 -> 输入你的邮箱、电话号码或Skype名称（Step1-3）
- 英语 -> 下一步按钮（Step1-8）
- 英语 -> 创建账户（Step1）
- 英语 -> 密码，请在此输入密码（Step4-8）
- 英语 -> 登录遇到问题？（Step4-8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: UnifiedLandingPageActivity** | 仿Skype登录落地页，含“Sign in/登录”“Skype名、邮箱或手机号”“创建账户”；本步点击账号输入框，无通知横幅与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: UnifiedLandingPageActivity** | 同一仿Skype登录页，账号框提示输入邮箱、电话或Skype名；本步向已聚焦输入框键入测试账号，页面无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: UnifiedLandingPageActivity** | 仿Skype登录页中账号框已填testuser123；本步点击“Next button/下一步”按钮，推进至密码页，未见通知与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: SignInActivity** | 仿Skype密码页，显示“Skype Name testuser123”“Password/密码”“Problems signing in?/登录遇到问题”；本步点击密码框，无通知与遮罩。 | `step_04_action.png` |
| 5 | **Step 5: SignInActivity** | 仿Skype密码页保持提示“请输入密码”；本步向已聚焦密码框键入测试密码，为后续提交作准备，无通知与遮罩。 | `step_05_action.png` |
| 6 | **Step 6: SignInActivity** | 仿Skype密码页密码已显示为12个圆点；本步发生静态活动跳转至SpiceActivity，无可见通知与遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: SignInActivity** | 仿Skype密码页仍停留，密码以12个圆点显示；本步静态跳转至微软账户选择AccountPickerActivity，无通知与遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: SignInActivity** | 仿Skype密码页保持12点掩码；本步静态跳转至微软添加账户AddAccountActivity，未见通知横幅与遮罩。 | `step_08_screen.png` |
