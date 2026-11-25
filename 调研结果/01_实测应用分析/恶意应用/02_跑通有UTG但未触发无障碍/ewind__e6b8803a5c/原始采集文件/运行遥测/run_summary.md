# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:46:34
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.antivirus.booster.security`（静态标签：`malicious` / `ewind` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 341 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.antivirus.booster.security` / `smstapge` | `-` | 3 | 149 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.antivirus.booster.security` / `smstapge` | `-` | 7 | 207 / 否 | `click` → [6] TextView text="START" id=guide_btn (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.antivirus.booster.security` / `smmain` | `-` | 14 | 69 / 否 | `click` → [11] LinearLayout id=ll_battery (click) center=(270,183 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.antivirus.booster.security` / `smbatsaver` | `-` | 4 | 25 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.antivirus.booster.security` / `smressafe` | `-` | 19 | 188 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.antivirus.booster.security` / `smressafe` | `-` | 19 | 188 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.antivirus.booster.security` / `smressafe` | `-` | 19 | 188 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Security Antivirus to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.antivirus.booster.security/smstapge`)**: `Security Antivirus` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.antivirus.booster.security/smstapge`)**: `Security Antivirus` | `I agree to Privacy Policy by starting the app` | `I agree to open Auto Clean,Smart Lock,Smart Swipe,Call ` | `START` | `Powered by Security Antivirus Team`
- **Step 4 (`com.antivirus.booster.security/smmain`)**: `RISKY` | `NEVER SCANNED BEFORE` | `Junk Clean` | `Phone Boost` | `Battery Saver` | `CPU Cooler`
- **Step 5 (`com.antivirus.booster.security/smbatsaver`)**: `100` | `%` | `Analyzing power usage`
- **Step 6 (`com.antivirus.booster.security/smressafe`)**: `Navigate up` | `BATTERY SAVED` | `Temperature Detect` | `Junk Clean` | `Battery Saver` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`
- **Step 7 (`com.antivirus.booster.security/smressafe`)**: `Navigate up` | `BATTERY SAVED` | `Temperature Detect` | `Junk Clean` | `Battery Saver` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`
- **Step 8 (`com.antivirus.booster.security/smressafe`)**: `Navigate up` | `BATTERY SAVED` | `Temperature Detect` | `Junk Clean` | `Battery Saver` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`

## 中文逐页引导链路解读

> **全链路总结**：应用从系统权限复核开始请求电话、文件媒体、联系人、相机、定位、通话记录等广泛权限，经旧版兼容提示和 START 捆绑同意页进入 RISKY 主面板，再由 Battery Saver 导流至“隐私风险/SCAN”安全页并静态跳转授权页面；拒绝授权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 选择允许“Security Antivirus”访问的内容（Step 1 系统权限复核页）
- English -> 该应用针对旧版 Android 构建，可能无法正常工作，请检查更新或联系开发者（Step 2 兼容性弹窗）
- English -> 启动应用即表示我同意隐私政策（Step 3 START 页）
- English -> 我同意开启自动清理、智能锁、智能滑动、通话结束、WiFi 优化（可能含赞助内容）（Step 3 START 页）
- English -> 高风险/从未扫描过（Step 4 主面板）
- English -> 正在分析电量使用（Step 5 省电页）
- English -> 电池已省电；抓住隐私入侵者；锁定应用防止窥探；可能存在安全风险；立即扫描以避免隐私泄露（Step 6 安全页，原文含拼写 pricacy）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页，要求允许 Security Antivirus 访问电话、文件媒体、联系人、相机、定位、通话记录等；本步点 Continue 继续。 | `step_01_action.png` |
| 2 | **Step 2: smstapge** | 旧版 Android 兼容性弹窗，英文提示应用或无法正常工作并建议检查更新或联系开发者；本步点 OK 关闭后继续进入应用。 | `step_02_action.png` |
| 3 | **Step 3: smstapge** | START 捆绑同意页：英文称启动即同意隐私政策，并同意开启自动清理、智能锁、智能滑动、通话结束、WiFi优化（可能含赞助内容）；本步点 START。 | `step_03_action.png` |
| 4 | **Step 4: smmain** | 主面板显示 RISKY、NEVER SCANNED BEFORE（高风险/从未扫描），列 Junk Clean、Phone Boost、Battery Saver、CPU Cooler；本步点 Battery Saver。 | `step_04_action.png` |
| 5 | **Step 5: smbatsaver** | 电池省电页显示 100% 与 Analyzing power usage（正在分析电量使用），本步无点击仅等待，随后导向权限/授权流程。 | `step_05_action.png` |
| 6 | **Step 6: smressafe** | 安全页以 BATTERY SAVED、防隐私入侵/锁应用及“可能有安全风险、立即扫描避免隐私泄露”诱导 SCAN；本步静态跳转授权页。 | `step_06_screen.png` |
| 7 | **Step 7: smressafe** | 重复的安全页：仍以 BATTERY SAVED、隐私防护与 SCAN 风险话术诱导；本步静态跳转 GrantPermissonsActivity$3，无可见点击。 | `step_07_screen.png` |
| 8 | **Step 8: smressafe** | 再次出现同一安全页，继续用 BATTERY SAVED、隐私防护与 SCAN 话术施压；本步静态跳转 GrantPermissonsActivity$4，无可见点击。 | `step_08_screen.png` |
