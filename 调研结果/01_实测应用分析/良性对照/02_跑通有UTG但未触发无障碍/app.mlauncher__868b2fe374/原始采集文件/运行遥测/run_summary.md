# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:37:25
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`app.mlauncher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `app.mlauncher` / `OnboardingActivity` | `-` | 6 | 107 / 否 | `click` → [6] Button text="Next" id=nextButton (click) center=(54 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `app.mlauncher` / `OnboardingActivity` | `-` | 6 | 107 / 否 | `click` → [5] Button text="Set as Default Launcher" id=permission | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 7 | 92 / 否 | `click` → [3] RadioButton (unchecked) center=(898,1102) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 8 | 113 / 否 | `click` → [8] Button text="Set as default" id=button1 (click) cen | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `app.mlauncher` / `OnboardingActivity` | `-` | 6 | 107 / 否 | `click` → [6] Button text="Next" id=nextButton (click) center=(54 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `app.mlauncher` / `OnboardingActivity` | `-` | 6 | 107 / 否 | `click` → [514, 1425] | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `Settings$AppUsageAccessSettingsActivity` | `-` | 10 | 230 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `Settings$AppUsageAccessSettingsActivity` | `-` | 10 | 230 / 否 | `click` → [1] ImageButton desc="Back" (click) center=(77,160) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`app.mlauncher/OnboardingActivity`)**: `Multi Launcher` | `Welcome to Multi Launcher` | `By continuing you agree to Privacy Policy` | `Set as Default Launcher` | `Next`
- **Step 2 (`app.mlauncher/OnboardingActivity`)**: `Multi Launcher` | `Welcome to Multi Launcher` | `By continuing you agree to Privacy Policy` | `Set as Default Launcher` | `Next`
- **Step 3 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set Multi Launcher as your default home app?` | `Multi Launcher` | `Pixel Launcher` | `Cancel` | `Set as default`
- **Step 4 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set Multi Launcher as your default home app?` | `Multi Launcher` | `No permissions needed` | `Pixel Launcher` | `Cancel` | `Set as default`
- **Step 5 (`app.mlauncher/OnboardingActivity`)**: `Multi Launcher` | `Welcome to Multi Launcher` | `By continuing you agree to Privacy Policy` | `Set as Default Launcher` | `Next`
- **Step 6 (`app.mlauncher/OnboardingActivity`)**: `Multi Launcher` | `Welcome to Multi Launcher` | `By continuing you agree to Privacy Policy` | `Set as Default Launcher` | `Next`
- **Step 7 (`com.android.settings/Settings$AppUsageAccessSettingsActivity`)**: `Back` | `Apps with usage access` | `Search settings` | `Multi Launcher` | `1.12.3 Build 0` | `Permit usage access` | `Usage access allows an app to track what other apps you`
- **Step 8 (`com.android.settings/Settings$AppUsageAccessSettingsActivity`)**: `Back` | `Apps with usage access` | `Search settings` | `Multi Launcher` | `1.12.3 Build 0` | `Permit usage access` | `Usage access allows an app to track what other apps you`

## 中文逐页引导链路解读

> **全链路总结**：该应用从欢迎引导页请求设为默认桌面，进入系统角色确认并确认后返回，再引导开启使用情况访问权限，跳转系统设置开启后返回继续引导。全程无通知横幅/遮罩，属功能引导叠加敏感权限说明，未测试拒权路径。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“By continuing you agree to Privacy Policy” -> 继续即表示同意隐私政策（欢迎引导页 Step1/2/5/6）
- 英文“Set as Default Launcher” -> 将 Multi Launcher 设为默认桌面（欢迎页按钮）
- 英文“Set Multi Launcher as your default home app?” -> 是否将 Multi Launcher 设为默认主屏幕应用？（系统角色确认页 Step3/4）
- 英文“No permissions needed” -> 无需权限（系统角色页选中 Multi Launcher 后显示）
- 英文“Permit usage access”及说明 -> 允许使用情况访问；可跟踪其他应用使用及频率、运营商与语言设置等（系统设置 Step7/8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: OnboardingActivity** | 欢迎引导页：含欢迎语、继续即同意隐私政策、设为默认桌面与Next；点击Next推进，未见通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: OnboardingActivity** | 同欢迎页：Next显示禁用，改点“Set as Default Launcher”触发系统默认桌面请求；无通知横幅与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: RequestRoleActivity** | 系统角色页：询问是否设Multi Launcher为默认主屏，列Pixel Launcher、取消与确认；本步仅选中前者单选，未确认。 | `step_03_action.png` |
| 4 | **Step 4: RequestRoleActivity** | 系统角色页：Multi Launcher选中后显示“无需权限”，点“Set as default”确认默认主屏；无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: OnboardingActivity** | 返回欢迎页：Next已高亮，点击继续引导；仍含继续即同意隐私政策及设为默认桌面，未见通知横幅或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: OnboardingActivity** | 欢迎页出现使用情况访问权限门槛，按坐标点击“Grant Permission”入口跳系统设置；无通知横幅/遮罩。 | `step_06_action.png` |
| 7 | **Step 7: Settings$AppUsageAccessSet** | 系统使用情况访问设置页：说明可跟踪其他应用使用及频率等，点开关为Multi Launcher授权；无通知/遮罩。 | `step_07_action.png` |
| 8 | **Step 8: Settings$AppUsageAccessSet** | 同一使用情况访问设置页：权限已开启，点左上Back返回应用继续引导；含跟踪应用使用说明，无通知/遮罩。 | `step_08_action.png` |
