# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:50:58
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.antivirus.easy.cleaner`（静态标签：`malicious` / `solid` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 335 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.antivirus.easy.cleaner` / `StartPageActivity` | `-` | 3 | 143 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.antivirus.easy.cleaner` / `StartPageActivity` | `-` | 7 | 212 / 否 | `click` → [6] TextView text="START" id=guide_btn (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.antivirus.easy.cleaner` / `CleanMainActivity` | `-` | 25 | 75 / 否 | `click` → [22] RelativeLayout id=keep_rl_battery (click) center=( | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.antivirus.easy.cleaner` / `BatterySaverActivity` | `-` | 4 | 25 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.antivirus.easy.cleaner` / `ResultSafetyActivity` | `-` | 19 | 188 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.antivirus.easy.cleaner` / `ResultSafetyActivity` | `-` | 19 | 188 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.antivirus.easy.cleaner` / `ResultSafetyActivity` | `-` | 19 | 188 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Easy Cleaner to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.antivirus.easy.cleaner/StartPageActivity`)**: `Easy Cleaner` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.antivirus.easy.cleaner/StartPageActivity`)**: `Easy Cleaner` | `I agree to Privacy Policy by starting the app` | `I agree to open Realtime Protect,Auto Clean,Smart Lock,` | `START` | `Powered by Easy Cleaner Team`
- **Step 4 (`com.antivirus.easy.cleaner/CleanMainActivity`)**: `53` | `%` | `RAM` | `1.04GB` | `/` | `1.93GB` | `STORAGE` | `3` | `226MB` | `5.80GB`
- **Step 5 (`com.antivirus.easy.cleaner/BatterySaverActivity`)**: `100` | `%` | `Analyzing power usage`
- **Step 6 (`com.antivirus.easy.cleaner/ResultSafetyActivity`)**: `Navigate up` | `BATTERY SAVED` | `Battery Saver` | `Temperature Detect` | `Junk Clean` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`
- **Step 7 (`com.antivirus.easy.cleaner/ResultSafetyActivity`)**: `Navigate up` | `BATTERY SAVED` | `Battery Saver` | `Temperature Detect` | `Junk Clean` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`
- **Step 8 (`com.antivirus.easy.cleaner/ResultSafetyActivity`)**: `Navigate up` | `BATTERY SAVED` | `Battery Saver` | `Temperature Detect` | `Junk Clean` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`

## 中文逐页引导链路解读

> **全链路总结**：链路：系统权限复核页放行多项敏感权限→旧版Android警告→预勾选协议START→清理主界面→电池分析→结果页反复以安全风险诱导并静态跳转授权/无障碍页面，核心为制造风险恐慌推动授权。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- I agree to Privacy Policy by starting the app -> 启动即视为同意隐私政策（Step 3 启动页）
- I agree to open Realtime Protect,Auto Clean,Smart Lock,Smart Swipe,Call End,WiFi Optimizer(May contain sponsored contents) -> 同意开启实时保护、自动清理、智能锁、智能滑动、通话结束、WiFi优化，且可能含赞助内容（Step 3 启动页）
- Catch your privacy invaders -> 抓住你的隐私入侵者（Step 6-8 结果页）
- Lock apps to prevent snooping -> 锁定应用以防窥探（Step 6-8 结果页）
- Possible security risks -> 可能存在安全风险（Step 6-8 结果页）
- Scan now to avoid pricacy leaking -> 立即扫描以避免隐私泄露（Step 6-8 结果页，原文pricacy为拼写错误）
- BATTERY SAVED -> 电池已节省（Step 6-8 结果页）
- Analyzing power usage -> 正在分析电量使用（Step 5 省电页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页，列出手机、文件媒体、联系人、相机、位置、通话记录等权限；点Continue放行，顶部有Google备份通知，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: StartPageActivity** | 旧版Android兼容警告弹窗，提示应用按旧版构建可能异常；点OK关闭进入启动页，顶部有Google备份通知，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: StartPageActivity** | 启动页两行协议默认勾选：启动即同意隐私政策、开启多项保护并可能含赞助内容；点START进入主界面，顶部有备份通知。 | `step_03_action.png` |
| 4 | **Step 4: CleanMainActivity** | 清理主界面显示RAM 53%、存储226MB等，入口有扫描、垃圾清理、省电、CPU降温；点Battery Saver，顶部备份通知。 | `step_04_action.png` |
| 5 | **Step 5: BatterySaverActivity** | 省电页显示100%与“正在分析电量使用”动画；本步等待分析结束，顶部Google备份通知，无遮罩。 | `step_05_action.png` |
| 6 | **Step 6: ResultSafetyActivity** | 结果页称电池已节省，列温度检测、垃圾清理、隐私入侵、应用锁及安全风险；静态跳授权页GrantPermissonsActivity，顶部备份通知。 | `step_06_screen.png` |
| 7 | **Step 7: ResultSafetyActivity** | 同一结果页仍以隐私入侵、锁应用防窥、安全风险和SCAN施压；静态跳无障碍弹窗AccessibilityDialogActivity，顶部备份通知。 | `step_07_screen.png` |
| 8 | **Step 8: ResultSafetyActivity** | 同一结果页重复安全风险与SCAN诱导；静态跳至GrantPermissonsActivity$2继续授权流程，顶部Google备份通知，无遮罩。 | `step_08_screen.png` |
