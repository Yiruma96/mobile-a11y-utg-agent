# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:17:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.antivirus.powerful.security`（静态标签：`malicious` / `solid` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 340 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.antivirus.powerful.security` / `smstapge` | `-` | 3 | 148 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.antivirus.powerful.security` / `smstapge` | `-` | 7 | 205 / 否 | `click` → [6] TextView text="START" id=guide_btn (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.antivirus.powerful.security` / `smmain` | `-` | 14 | 69 / 否 | `click` → [4] LinearLayout id=rl_scan (click) center=(540,1121) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.antivirus.powerful.security` / `smmain` | `-` | 14 | 69 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.antivirus.powerful.security` / `smscanres` | `-` | 22 | 379 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.antivirus.powerful.security` / `smscanres` | `-` | 22 | 379 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.antivirus.powerful.security` / `smscanres` | `-` | 22 | 379 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Powerful Security to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.antivirus.powerful.security/smstapge`)**: `Powerful Security` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.antivirus.powerful.security/smstapge`)**: `Powerful Security` | `I agree to Privacy Policy by starting the app` | `I agree to open Auto Clean,Smart Lock,Smart Swipe,Call ` | `START` | `Powered by Powerful Security Team`
- **Step 4 (`com.antivirus.powerful.security/smmain`)**: `RISKY` | `NEVER SCANNED BEFORE` | `Junk Clean` | `Phone Boost` | `Battery Saver` | `CPU Cooler`
- **Step 5 (`com.antivirus.powerful.security/smmain`)**: `RISKY` | `NEVER SCANNED BEFORE` | `Junk Clean` | `Phone Boost` | `Battery Saver` | `CPU Cooler`
- **Step 6 (`com.antivirus.powerful.security/smscanres`)**: `IN DANGER` | `4 problem(s)` | `Security Grant Failed` | `System` | `Grant for full & advanced protection` | `No private data will be collected` | `GRANT` | `Real-time protection` | `No more virus or privacy leak` | `Auto scan newly installed apps`
- **Step 7 (`com.antivirus.powerful.security/smscanres`)**: `IN DANGER` | `4 problem(s)` | `Security Grant Failed` | `System` | `Grant for full & advanced protection` | `No private data will be collected` | `GRANT` | `Real-time protection` | `No more virus or privacy leak` | `Auto scan newly installed apps`
- **Step 8 (`com.antivirus.powerful.security/smscanres`)**: `IN DANGER` | `4 problem(s)` | `Security Grant Failed` | `System` | `Grant for full & advanced protection` | `No private data will be collected` | `GRANT` | `Real-time protection` | `No more virus or privacy leak` | `Auto scan newly installed apps`

## 中文逐页引导链路解读

> **全链路总结**：应用先拉起系统权限总览，申请电话、文件媒体、联系人、相机、位置、通话记录与身体活动权限；随后关闭旧版警告、以预勾选隐私/功能同意进入主页，再用“RISKY/从未扫描”诱导扫描。结果页以“IN DANGER/4个问题/授权失败”制造恐慌并引导GRANT/ENABLE NOW，最终静态跳转授权与快捷功能页。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “选择允许Powerful Security访问的内容”（权限总览页）
- English -> “此应用为旧版Android构建，可能无法正常工作，请检查更新或联系开发者”（兼容警告页）
- English -> “启动应用即同意隐私政策”（启动同意页）
- English -> “同意开启自动清理、智能锁、智能滑动、通话结束、WiFi优化（可能含赞助内容）”（启动同意页）
- English -> “有风险/从未扫描”（主扫描页）
- English -> “处于危险中/4个问题/安全授权失败”（扫描结果页）
- English -> “授予完整与高级保护/不会收集任何私人数据/授予”（扫描结果页）
- English -> “实时防护、杜绝病毒与隐私泄露、自动扫描新装应用、24小时防恶意软件、卸载Powerful Security后设备将失去保护/立即启用”（扫描结果页）
- English -> “系统漏洞”（扫描结果页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限总览页，列电话、文件媒体、联系人、相机、位置、通话记录等权限；点击“Continue”进入应用，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: smstapge** | 应用兼容警告页，提示为旧版Android构建可能无法正常工作；点击“OK”关闭警告，无通知横幅或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: smstapge** | 启动同意页，两项隐私政策与自动清理、智能锁、智能滑动、通话结束、WiFi优化（含赞助内容）已预勾选；点“START”进入，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: smmain** | 主扫描页，中央圆环显示“RISKY/从未扫描”；点击扫描环启动扫描，页面无通知横幅或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: smmain** | 主扫描页等待态，扫描已至100%但界面文字未变；本步仅等待结果或权限提示出现，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: smscanres** | 扫描结果页显示“IN DANGER/4个问题/安全授权失败”，以实时防护、24小时防恶意软件诱导GRANT/ENABLE NOW；静态跳转授权页，无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: smscanres** | 同一扫描结果页与恐慌授权话术仍展示，本步再次静态跳转至GrantPermissonsActivity相关流程；无通知/遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: smscanres** | 结果页仍展示GRANT/ENABLE NOW及“不收集隐私”话术，随后静态跳转快捷功能页an.sc.clean.act.smshcutani；无通知/遮罩。 | `step_08_screen.png` |
