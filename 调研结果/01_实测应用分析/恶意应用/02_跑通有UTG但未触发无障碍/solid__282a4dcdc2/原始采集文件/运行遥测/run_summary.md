# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:15:27
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.clean.antivirus.security`（静态标签：`malicious` / `solid` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 35 | 364 / 否 | `click` → [35] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.clean.antivirus.security` / `StartPageActivity` | `-` | 3 | 143 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.clean.antivirus.security` / `StartPageActivity` | `-` | 7 | 194 / 否 | `click` → [6] TextView text="START" id=guide_btn (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.clean.antivirus.security` / `MainActivity` | `-` | 7 | 194 / 否 | `click` → [539, 1307] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.clean.antivirus.security` / `MainActivity` | `-` | 7 | 194 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.clean.antivirus.security` / `ScanResultActivity` | `-` | 22 | 374 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.clean.antivirus.security` / `ScanResultActivity` | `-` | 22 | 374 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.clean.antivirus.security` / `ScanResultActivity` | `-` | 22 | 374 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Dr. Security to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.clean.antivirus.security/StartPageActivity`)**: `Dr. Security` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.clean.antivirus.security/StartPageActivity`)**: `DR.SECURITY` | `I agree to Privacy Policy by starting the app` | `I agree to open Auto Clean,Smart Lock,Smart Swipe,Call ` | `START` | `Powered by Dr. Security Team`
- **Step 4 (`com.clean.antivirus.security/MainActivity`)**: `DR.SECURITY` | `I agree to Privacy Policy by starting the app` | `I agree to open Auto Clean,Smart Lock,Smart Swipe,Call ` | `START` | `Powered by Dr. Security Team`
- **Step 5 (`com.clean.antivirus.security/MainActivity`)**: `DR.SECURITY` | `I agree to Privacy Policy by starting the app` | `I agree to open Auto Clean,Smart Lock,Smart Swipe,Call ` | `START` | `Powered by Dr. Security Team`
- **Step 6 (`com.clean.antivirus.security/ScanResultActivity`)**: `IN DANGER` | `4 problem(s)` | `Security Grant Failed` | `System` | `Grant for full & advanced protection` | `No private data will be collected` | `GRANT` | `Real-time protection` | `No more virus or privacy leak` | `Auto scan newly installed apps`
- **Step 7 (`com.clean.antivirus.security/ScanResultActivity`)**: `IN DANGER` | `4 problem(s)` | `Security Grant Failed` | `System` | `Grant for full & advanced protection` | `No private data will be collected` | `GRANT` | `Real-time protection` | `No more virus or privacy leak` | `Auto scan newly installed apps`
- **Step 8 (`com.clean.antivirus.security/ScanResultActivity`)**: `IN DANGER` | `4 problem(s)` | `Security Grant Failed` | `System` | `Grant for full & advanced protection` | `No private data will be collected` | `GRANT` | `Real-time protection` | `No more virus or privacy leak` | `Auto scan newly installed apps`

## 中文逐页引导链路解读

> **全链路总结**：应用先请求电话、文件媒体、联系人、相机、定位、通话记录和短信等权限，再以旧版Android警告及隐私/赞助内容同意页诱导点击START；随后展示“4项危险”的假扫描结果，并借GRANT/ENABLE NOW将流程跳转至授权与无障碍对话框。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 选择允许“Dr. Security”访问的内容（权限页）
- English -> 该应用为旧版Android构建，可能无法正常运行（旧版警告页）
- English -> 启动应用即表示同意隐私政策（启动页）
- English -> 同意开启自动清理、智能锁、智能滑动、通话结束、WiFi优化，可能含赞助内容（启动页）
- English -> 处于危险/4个问题/安全授权失败（扫描结果页）
- English -> 授予完整与高级保护；不会收集私人数据；授予（扫描结果页）
- English -> 实时保护、无病毒或隐私泄露、自动扫描新装应用、24小时防恶意软件、卸载即失去保护（扫描结果页）
- English -> 立即启用（扫描结果页）
- English -> 系统漏洞（扫描结果页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限选择页，列出电话、文件媒体、联系人、相机、定位、通话记录和短信；点击“Continue”继续，无通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: StartPageActivity** | 应用启动页弹出旧版Android兼容警告，含“Dr. Security”和“OK”；点击OK关闭警告，未出现通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: StartPageActivity** | 启动页展示DR.SECURITY，含隐私政策与开启多项清理/优化功能的赞助内容同意文案；点击START进入，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 仍为同一启动页文案，点击疑似橙色扫描按钮，未捕获扫描进度新文案；无通知横幅和遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 停留MainActivity等待假扫描完成；页面仍显示START及同意文案，未见结果或FIX按钮，无通知横幅或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: ScanResultActivity** | 扫描结果页显示“IN DANGER/4个问题/安全授权失败”，诱导GRANT/ENABLE NOW；静态跳转权限授予页，无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: ScanResultActivity** | 同一扫描结果页仍展示危险、授权失败及实时保护宣传；再次静态跳转权限授予页的匿名回调，无通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: ScanResultActivity** | 扫描结果页重复“处于危险/4问题/授权失败”，并以立即启用诱导；静态跳转至无障碍对话框页，无通知或遮罩。 | `step_08_screen.png` |
