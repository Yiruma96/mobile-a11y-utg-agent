# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:30:16
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.antivirus.guardian.cleaner.security`（静态标签：`malicious` / `hiddad` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 341 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.antivirus.guardian.cleaner.security` / `StartPageActivity` | `-` | 3 | 149 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.antivirus.guardian.cleaner.security` / `StartPageActivity` | `-` | 7 | 224 / 否 | `click` → [6] TextView text="START" id=guide_btn (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.antivirus.guardian.cleaner.security` / `MainActivity` | `-` | 14 | 78 / 否 | `click` → [11] LinearLayout id=ll_phone_boost (click) center=(540 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.antivirus.guardian.cleaner.security` / `ResultSafetyActivity` | `-` | 1 | 14 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.antivirus.guardian.cleaner.security` / `ResultSafetyActivity` | `-` | 20 | 201 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.antivirus.guardian.cleaner.security` / `ResultSafetyActivity` | `-` | 20 | 201 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.antivirus.guardian.cleaner.security` / `ResultSafetyActivity` | `-` | 20 | 201 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Guardian Antivirus to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.antivirus.guardian.cleaner.security/StartPageActivity`)**: `Guardian Antivirus` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.antivirus.guardian.cleaner.security/StartPageActivity`)**: `Guardian Antivirus` | `I agree to Privacy Policy by starting the app` | `I agree to open Realtime Protect,Auto Clean,Smart Lock,` | `START` | `Powered by Guardian Antivirus Team`
- **Step 4 (`com.antivirus.guardian.cleaner.security/MainActivity`)**: `SCAN` | `Virus & Privacy` | `Risky` | `Never scanned before` | `Junk Clean` | `Phone Boost` | `Battery Saver`
- **Step 5 (`com.antivirus.guardian.cleaner.security/ResultSafetyActivity`)**: `214MB released`
- **Step 6 (`com.antivirus.guardian.cleaner.security/ResultSafetyActivity`)**: `Navigate up` | `Memory Use:46%` | `214MB released` | `Junk Clean` | `Phone Boost` | `Temperature Detect` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks`
- **Step 7 (`com.antivirus.guardian.cleaner.security/ResultSafetyActivity`)**: `Navigate up` | `Memory Use:46%` | `214MB released` | `Junk Clean` | `Phone Boost` | `Temperature Detect` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks`
- **Step 8 (`com.antivirus.guardian.cleaner.security/ResultSafetyActivity`)**: `Navigate up` | `Memory Use:46%` | `214MB released` | `Junk Clean` | `Phone Boost` | `Temperature Detect` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks`

## 中文逐页引导链路解读

> **全链路总结**：该应用先引导系统权限总览并继续授权，再以旧版兼容提示和启动页捆绑同意进入主界面；随后用“释放214MB/内存46%/隐私风险”等结果页催促扫描，并多次静态跳转尝试拉起授权页。整体呈现清理加速类工具外壳下的权限诱导与夸大安全风险话术。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“This app was built for an older version of Android and may not work properly...” -> 应用为旧版Android构建，可能无法正常工作（启动页弹窗）
- 英文“I agree to Privacy Policy by starting the app” -> 开始使用即视为同意隐私政策（启动页）
- 英文“I agree to open Realtime Protect,Auto Clean,Smart Lock,Smart Swipe,Call End,WiFi Optimizer(May contain sponsored contents)” -> 同意开启实时保护、自动清理、智能锁、智能滑动、通话结束、WiFi优化，可能含赞助内容（启动页）
- 英文“Possible security risks / Scan now to avoid pricacy leaking” -> 存在可能安全风险，立即扫描以避免隐私泄露（结果安全页）
- 英文“Catch your privacy invaders / Lock apps to prevent snooping” -> 抓住隐私入侵者，锁定应用以防窥探（结果安全页）
- 英文“214MB released / Memory Use:46%” -> 已释放214MB，内存占用46%（结果安全页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限总览页，列出电话、文件媒体、联系人、相机、位置等权限；点击“Continue”继续授权，无通知与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: StartPageActivity** | 旧版Android兼容性警告弹窗，提示应用为旧版本构建、可能无法正常运行；点击“OK”关闭弹窗继续，无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: StartPageActivity** | 启动页以隐私政策和多项功能开启构成捆绑同意，并提示可能含赞助内容；点击“START”进入，无通知与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 主界面展示“SCAN”、病毒与隐私风险、垃圾清理、手机加速等入口；点击“Phone Boost”进入加速，无通知与遮罩。 | `step_04_action.png` |
| 5 | **Step 5: ResultSafetyActivity** | 结果页仅显示“214MB released”，即已释放214MB，作为过渡/结果展示；本步等待加载，无通知与遮罩。 | `step_05_action.png` |
| 6 | **Step 6: ResultSafetyActivity** | 结果安全页展示内存占用46%、已释放214MB及隐私风险扫描催促；静态跳转尝试前往授权页，无通知与遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: ResultSafetyActivity** | 同一结果安全页重复展示内存46%、已释放214MB与“立即扫描”催促；再次静态跳转授权页，无通知与遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: ResultSafetyActivity** | 结果安全页仍以风险提示和扫描按钮诱导继续防护；静态跳转改用startActivityForResult拉起授权，无通知与遮罩。 | `step_08_screen.png` |
