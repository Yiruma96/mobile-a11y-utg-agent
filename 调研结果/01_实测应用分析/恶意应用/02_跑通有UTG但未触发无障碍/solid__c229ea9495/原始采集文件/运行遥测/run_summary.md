# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:48:03
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.antivirus.deep.cleaner`（静态标签：`malicious` / `solid` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `8` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 335 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.antivirus.deep.cleaner` / `cmstapge` | `-` | 3 | 143 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.antivirus.deep.cleaner` / `cmstapge` | `-` | 7 | 195 / 否 | `click` → [6] TextView text="START" id=guide_btn (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.antivirus.deep.cleaner` / `CleanMainActivity` | `-` | 17 | 67 / 否 | `click` → [12] RelativeLayout id=keep_rl_battery (click) center=( | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.antivirus.deep.cleaner` / `cmbatsaver` | `-` | 4 | 25 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.antivirus.deep.cleaner` / `cmressafe` | `-` | 19 | 189 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.antivirus.deep.cleaner` / `cmshcutani` | `-` | 19 | 189 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.antivirus.deep.cleaner` / `cmstapge` | `-` | 19 | 189 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Deep Cleaner to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.antivirus.deep.cleaner/cmstapge`)**: `Deep Cleaner` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.antivirus.deep.cleaner/cmstapge`)**: `Deep Cleaner` | `I agree to Privacy Policy by starting the app` | `I agree to open Auto Clean,Smart Lock,Smart Swipe,Call ` | `START` | `Powered by Deep Cleaner Team`
- **Step 4 (`com.antivirus.deep.cleaner/CleanMainActivity`)**: `CLEAN` | `Scan` | `Junk Clean` | `Phone Boost` | `Battery Saver` | `Cpu Cooler` | `WiFi Optimizer`
- **Step 5 (`com.antivirus.deep.cleaner/cmbatsaver`)**: `100` | `%` | `Analyzing power usage`
- **Step 6 (`com.antivirus.deep.cleaner/cmressafe`)**: `Navigate up` | `BATTERY SAVED` | `Phone Boost` | `Temperature Detect` | `Battery Saver` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`
- **Step 7 (`com.antivirus.deep.cleaner/cmshcutani`)**: `Navigate up` | `BATTERY SAVED` | `Phone Boost` | `Temperature Detect` | `Battery Saver` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`
- **Step 8 (`com.antivirus.deep.cleaner/cmstapge`)**: `Navigate up` | `BATTERY SAVED` | `Phone Boost` | `Temperature Detect` | `Battery Saver` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`

## 中文逐页引导链路解读

> **全链路总结**：应用先经系统权限总览申请电话、文件、联系人、相机、定位和通话记录等敏感权限，再以旧版兼容提示和默认勾选的隐私/功能同意页进入清理主界面；随后用省电扫描伪进度及“隐私泄露/安全风险”结果页反复诱导扫描并静态跳转。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English: Choose what to allow Deep Cleaner to access -> 选择允许Deep Cleaner访问的内容（Step 1 系统权限总览页）
- English: This app was built for an older version of Android and may not work properly -> 本应用为旧版Android构建，可能无法正常工作（Step 2 兼容性警告页）
- English: I agree to Privacy Policy by starting the app -> 启动应用即视为同意隐私政策（Step 3 启动同意页）
- English: I agree to open Auto Clean,Smart Lock,Smart Swipe,Call End,WiFi Optimizer(May contain sponsored contents) -> 同意开启自动清理、智能锁、智能滑动、挂断、WiFi优化，且可能含赞助内容（Step 3 启动同意页）
- English: Analyzing power usage -> 正在分析电量使用（Step 5 省电扫描页）
- English: Catch your privacy invaders / Lock apps to prevent snooping -> 抓住隐私入侵者 / 锁定应用防止窥探（Step 6-8 安全结果页）
- English: Possible security risks / Scan now to avoid pricacy leaking -> 可能存在安全风险 / 立即扫描避免隐私泄露（Step 6-8 安全结果页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限总览页，逐项请求电话、文件媒体、联系人、相机、定位、通话记录权限；点击Continue继续。 | `step_01_action.png` |
| 2 | **Step 2: cmstapge** | 应用内兼容性警告页，提示Deep Cleaner为旧版Android构建、可能异常；点击OK关闭并继续。 | `step_02_action.png` |
| 3 | **Step 3: cmstapge** | 启动同意页，默认勾选隐私政策及自动清理、智能锁、智能滑动、挂断、WiFi优化等含赞助内容；点START。 | `step_03_action.png` |
| 4 | **Step 4: CleanMainActivity** | 清理主界面，展示Scan、垃圾清理、手机加速、省电、降温、WiFi优化等入口；点击Battery Saver。 | `step_04_action.png` |
| 5 | **Step 5: cmbatsaver** | 省电扫描页，显示100%与“正在分析电量使用”的伪进度；本步等待扫描结束，为后续无障碍授权铺垫。 | `step_05_action.png` |
| 6 | **Step 6: cmressafe** | 安全结果页，宣称“电池已省”，展示隐私入侵、锁应用、安全风险及“立即扫描避免隐私泄露”；本步静态跳至cmshcutani。 | `step_06_screen.png` |
| 7 | **Step 7: cmshcutani** | 同一安全结果页在cmshcutani重现，保留省电、隐私保护和风险扫描话术；本步无点击，静态跳转至cmstapge。 | `step_07_screen.png` |
| 8 | **Step 8: cmstapge** | 同一结果页在cmstapge再次呈现，仍以隐私泄露风险和SCAN诱导；本步无点击，静态跳至cmsnpinf。 | `step_08_screen.png` |
