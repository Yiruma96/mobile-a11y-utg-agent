# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:31:45
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.antivirus.booster.smart.security`（静态标签：`malicious` / `solid` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 366 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.antivirus.booster.smart.security` / `StartPageActivity` | `-` | 3 | 145 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.antivirus.booster.smart.security` / `StartPageActivity` | `-` | 7 | 199 / 否 | `click` → [6] TextView text="START" id=guide_btn (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.antivirus.booster.smart.security` / `MainActivity` | `-` | 15 | 66 / 否 | `click` → [3] RelativeLayout id=rl_menu (click) center=(1004,158) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.antivirus.booster.smart.security` / `MainActivity` | `-` | 83 | 241 / 否 | `click` → [7] ImageButton id=btn (click) center=(998,310) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.antivirus.booster.smart.security` / `GrantPermissonsActivity` | `-` | 18 | 226 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.antivirus.booster.smart.security` / `GrantPermissonsActivity` | `-` | 18 | 226 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.antivirus.booster.smart.security` / `GrantPermissonsActivity` | `-` | 18 | 226 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Smart Security to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.antivirus.booster.smart.security/StartPageActivity`)**: `Smart Security` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.antivirus.booster.smart.security/StartPageActivity`)**: `SMART SECURITY` | `I agree to Privacy Policy by starting the app` | `I agree to open Auto Clean,Smart Lock,Smart Swipe,Call ` | `START` | `Powered by Smart Security Team`
- **Step 4 (`com.antivirus.booster.smart.security/MainActivity`)**: `RISKY` | `NEVER SCANNED BEFORE` | `Junk Clean` | `Phone Boost` | `Battery Saver` | `Applock`
- **Step 5 (`com.antivirus.booster.smart.security/MainActivity`)**: `Menu` | `Security Level` | `Basic` | `Scan` | `AppLock` | `Intruder Selfie` | `Junk Clean` | `Battery Saver` | `Phone Boost` | `Cpu Cooler`
- **Step 6 (`com.antivirus.booster.smart.security/GrantPermissonsActivity`)**: `Security Level` | `Basic` | `Please grant all permissions to enhance security level` | `Accessibility` | `System optimization and phone security` | `ENABLE` | `Notification Usage` | `Assist to protect personal information` | `App with Usages acess` | `Protect app privacy`
- **Step 7 (`com.antivirus.booster.smart.security/GrantPermissonsActivity`)**: `Security Level` | `Basic` | `Please grant all permissions to enhance security level` | `Accessibility` | `System optimization and phone security` | `ENABLE` | `Notification Usage` | `Assist to protect personal information` | `App with Usages acess` | `Protect app privacy`
- **Step 8 (`com.antivirus.booster.smart.security/GrantPermissonsActivity`)**: `Security Level` | `Basic` | `Please grant all permissions to enhance security level` | `Accessibility` | `System optimization and phone security` | `ENABLE` | `Notification Usage` | `Assist to protect personal information` | `App with Usages acess` | `Protect app privacy`

## 中文逐页引导链路解读

> **全链路总结**：应用先经系统权限复核批量索取电话、文件媒体、联系人、相机、位置、通话记录和短信权限，再以旧版兼容警告及捆绑同意页进入主界面；随后用“RISKY/从未扫描”制造恐慌，并通过菜单和权限中心反复诱导开启无障碍、通知使用等高风险权限，链路止于静态跳转且未测试拒权结果。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “选择允许Smart Security访问什么”的权限清单引导（Step 1 权限复核页）
- 英语 -> “请授予全部权限以提升安全级别”的授权施压（Step 6-8 权限中心）
- 英语 -> “系统优化与手机安全”“协助保护个人信息”“保护应用隐私”等授权理由（Step 6-8 权限中心）
- 英语 -> “本应用为旧版Android构建，可能无法正常运行”的兼容警告（Step 2 启动页）
- 英语 -> “开始应用即同意隐私政策”“同意开启自动清理、智能锁、智能滑动、通话结束、WiFi优化，可能含赞助内容”的捆绑同意（Step 3 启动页）
- 英语 -> “RISKY”“NEVER SCANNED BEFORE”的风险恐慌标签（Step 4 主界面）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页，列出电话、文件媒体、联系人、相机、位置、通话记录、短信权限；点击Continue继续授权，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: StartPageActivity** | 应用启动页弹出旧版Android兼容警告，称可能无法正常运行；点击OK关闭弹窗，无通知横幅或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: StartPageActivity** | 启动页展示SMART SECURITY及隐私政策、自动清理等捆绑同意文案；点击START即视为同意并进入主界面，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 主界面以RISKY、NEVER SCANNED BEFORE制造风险恐慌，列出垃圾清理、提速、省电、应用锁；点击右上菜单，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 侧边菜单含Security Level、Scan、AppLock、入侵自拍、WiFi优化等；点击Security Level箭头进入权限中心，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: GrantPermissonsActivity** | 权限中心显示Security Level为Basic，要求授予无障碍、通知使用等全部权限；静态跳转至GrantPermissonsActivity$4，无通知遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: GrantPermissonsActivity** | 同一权限中心继续以Basic和全部授权施压，列无障碍、通知使用等入口；静态跳转至AccessibilityDialogActivity，无通知遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: GrantPermissonsActivity** | 权限中心再次展示Basic与全部授权要求，称可提升安全级别；静态跳转至GrantPermissonsActivity$3，无通知遮罩。 | `step_08_screen.png` |
