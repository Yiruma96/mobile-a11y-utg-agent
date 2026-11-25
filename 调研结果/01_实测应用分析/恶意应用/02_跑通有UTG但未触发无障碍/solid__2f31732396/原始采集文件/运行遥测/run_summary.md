# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:52:16
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.antivirus.power.cleaner`（静态标签：`malicious` / `solid` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 336 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.antivirus.power.cleaner` / `StartPageActivity` | `-` | 3 | 144 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.antivirus.power.cleaner` / `StartPageActivity` | `-` | 7 | 214 / 否 | `click` → [6] TextView text="START" id=guide_btn (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.antivirus.power.cleaner` / `CleanMainActivity` | `-` | 25 | 75 / 否 | `click` → [3] RelativeLayout id=rl_menu (click) center=(1004,159) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.antivirus.power.cleaner` / `CleanMainActivity` | `-` | 93 | 257 / 否 | `swipe` → [540, 1600] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.antivirus.power.cleaner` / `CleanMainActivity` | `-` | 89 | 256 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.antivirus.power.cleaner` / `CleanMainActivity` | `-` | 89 | 256 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.antivirus.power.cleaner` / `CleanMainActivity` | `-` | 89 | 256 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Power Cleaner to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.antivirus.power.cleaner/StartPageActivity`)**: `Power Cleaner` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.antivirus.power.cleaner/StartPageActivity`)**: `Power Cleaner` | `I agree to Privacy Policy by starting the app` | `I agree to open Realtime Protect,Auto Clean,Smart Lock,` | `START` | `Powered by Power Cleaner Team`
- **Step 4 (`com.antivirus.power.cleaner/CleanMainActivity`)**: `5` | `%` | `STORAGE` | `341MB` | `/` | `5.80GB` | `48` | `RAM` | `1.43GB` | `2.92GB`
- **Step 5 (`com.antivirus.power.cleaner/CleanMainActivity`)**: `Menu` | `Security Level` | `Basic` | `Scan` | `AppLock` | `Message Security` | `Intruder Selfie` | `Junk Clean` | `Battery Saver` | `Phone Boost`
- **Step 6 (`com.antivirus.power.cleaner/CleanMainActivity`)**: `Menu` | `Security Level` | `Basic` | `Intruder Selfie` | `Junk Clean` | `Battery Saver` | `Phone Boost` | `Cpu Cooler` | `Realtime Process Monitor` | `Notification cleaner`
- **Step 7 (`com.antivirus.power.cleaner/CleanMainActivity`)**: `Menu` | `Security Level` | `Basic` | `Intruder Selfie` | `Junk Clean` | `Battery Saver` | `Phone Boost` | `Cpu Cooler` | `Realtime Process Monitor` | `Notification cleaner`
- **Step 8 (`com.antivirus.power.cleaner/CleanMainActivity`)**: `Menu` | `Security Level` | `Basic` | `Intruder Selfie` | `Junk Clean` | `Battery Saver` | `Phone Boost` | `Cpu Cooler` | `Realtime Process Monitor` | `Notification cleaner`

## 中文逐页引导链路解读

> **全链路总结**：该应用先在系统权限审查页请求电话、文件、联系人、相机、位置等多项权限，经旧版兼容提示后进入启动页，以点击 START 捆绑同意隐私政策及实时保护、自动清理等含赞助功能，随后进入清理主界面和侧边菜单；探针尝试静态跳转到授权页与无障碍弹窗页，但界面仍停留菜单，未出现可见授权弹窗。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 选择允许 Power Cleaner 访问的内容（Step 1: ReviewPermissionsActivity）
- 英文 -> 该应用为旧版 Android 构建，可能无法正常工作；请检查更新或联系开发者（Step 2: StartPageActivity）
- 英文 -> 开始使用应用即表示同意隐私政策（Step 3: StartPageActivity）
- 英文 -> 同意开启实时保护、自动清理、智能锁、智能滑动、通话结束、WiFi 优化（可能含赞助内容）（Step 3: StartPageActivity）
- 英文 -> 安全等级：基础（Step 5-8: CleanMainActivity 菜单）
- 英文 -> 权限检查器、实时保护等入口名称（Step 6-8: CleanMainActivity 菜单）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审查页，列出电话、文件媒体、联系人、相机、位置、通话记录等；点击Continue继续，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: StartPageActivity** | 启动页弹出旧版Android兼容性提示，称可能无法正常工作；点击OK关闭，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: StartPageActivity** | 启动页点击START即同意隐私政策，并捆绑开启实时保护、自动清理等含赞助内容功能；无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: CleanMainActivity** | 进入主界面，显示存储5%、内存等仪表盘及扫描、垃圾清理、省电、降温入口；点击左上菜单打开抽屉，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: CleanMainActivity** | 侧边菜单展开，含安全等级Basic、扫描、应用锁、消息安全、垃圾清理等；本步下滑菜单露出更多条目，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: CleanMainActivity** | 菜单续显权限检查、实时保护等入口；静态跳转GrantPermissonsActivity授权页，界面仍停留菜单，无通知/遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: CleanMainActivity** | 菜单仍停留原页，未出现授权弹窗；探针再次静态跳转GrantPermissonsActivity$4，疑为权限引导内部类。 | `step_07_screen.png` |
| 8 | **Step 8: CleanMainActivity** | 菜单未变化，无可见授权/无障碍弹窗；静态跳转AccessibilityDialogActivity，疑似引导开启无障碍权限。 | `step_08_screen.png` |
