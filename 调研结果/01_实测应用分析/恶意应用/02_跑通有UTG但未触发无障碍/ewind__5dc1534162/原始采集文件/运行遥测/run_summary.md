# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:10:39
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.antivirus.easy.cleaner`（静态标签：`malicious` / `ewind` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `8` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 31 | 335 / 否 | `click` → [31] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.antivirus.easy.cleaner` / `cmstapge` | `-` | 3 | 143 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.antivirus.easy.cleaner` / `cmstapge` | `-` | 7 | 195 / 否 | `click` → [6] TextView text="START" id=guide_btn (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.antivirus.easy.cleaner` / `CleanMainActivity` | `-` | 25 | 75 / 否 | `click` → [22] RelativeLayout id=keep_rl_battery (click) center=( | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.antivirus.easy.cleaner` / `cmbatsaver` | `-` | 4 | 25 / 否 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.antivirus.easy.cleaner` / `cmressafe` | `-` | 19 | 188 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.antivirus.easy.cleaner` / `cmshcutani` | `-` | 19 | 188 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.antivirus.easy.cleaner` / `cmstapge` | `-` | 3 | 42 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Easy Cleaner to access` | `Phone` | `make and manage phone calls` | `Files and media` | `access photos, media, and files on your device` | `Contacts` | `access your contacts` | `Camera` | `take pictures and record video` | `Location`
- **Step 2 (`com.antivirus.easy.cleaner/cmstapge`)**: `Easy Cleaner` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.antivirus.easy.cleaner/cmstapge`)**: `Easy Cleaner` | `I agree to Privacy Policy by starting the app` | `I agree to open Auto Clean,Smart Lock,Smart Swipe,Call ` | `START` | `Powered by Easy Cleaner Team`
- **Step 4 (`com.antivirus.easy.cleaner/CleanMainActivity`)**: `45` | `%` | `RAM` | `1.32GB` | `/` | `2.92GB` | `STORAGE` | `4` | `272MB` | `5.80GB`
- **Step 5 (`com.antivirus.easy.cleaner/cmbatsaver`)**: `100` | `%` | `Analyzing power usage`
- **Step 6 (`com.antivirus.easy.cleaner/cmressafe`)**: `Navigate up` | `BATTERY SAVED` | `Junk Clean` | `Temperature Detect` | `Battery Saver` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`
- **Step 7 (`com.antivirus.easy.cleaner/cmshcutani`)**: `Navigate up` | `BATTERY SAVED` | `Junk Clean` | `Temperature Detect` | `Battery Saver` | `Catch your privacy invaders` | `Lock apps to prevent snooping` | `PROTECT` | `Possible security risks` | `Scan now to avoid pricacy leaking`
- **Step 8 (`com.antivirus.easy.cleaner/cmstapge`)**: `Easy Cleaner isn't responding` | `Close app` | `Wait`

## 中文逐页引导链路解读

> **全链路总结**：该应用先经系统权限审核页批量请求手机、文件、联系人、相机、位置等敏感权限，再以START打包取得隐私政策及自动清理等同意，进入清理主界面后以电池分析和“隐私风险/SCAN”安全恐吓引导；中途出现旧版兼容提示与ANR，未完成拒权测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “此应用为旧版Android构建，可能无法正常运行”（Step 2 兼容警告）
- English -> “点击START即表示同意隐私政策，并开启自动清理、智能锁、智能滑动、挂断、WiFi优化（可能含赞助内容）”（Step 3 启动同意页）
- English -> “捕捉你的隐私入侵者/锁定应用防止窥探”（Step 6-7 安全恐吓页）
- English -> “可能存在安全风险/立即扫描以免隐私泄露”（Step 6-7 安全恐吓页，原文含拼写pricacy）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审核页，列手机、文件、联系人、相机、位置等敏感权限；点击Continue即批量继续授权，无拒绝入口。 | `step_01_action.png` |
| 2 | **Step 2: cmstapge** | 旧版Android兼容警告，称应用可能无法正常运行，仅OK按钮；点击OK关闭提示并继续进入应用。 | `step_02_action.png` |
| 3 | **Step 3: cmstapge** | 启动同意页称点击START即同意隐私政策，并开启自动清理、智能锁等可能含赞助内容功能；点击START。 | `step_03_action.png` |
| 4 | **Step 4: CleanMainActivity** | 清理主界面显示RAM 45%、存储统计及垃圾清理、电池节省、CPU降温入口；点击Battery Saver进入电池优化。 | `step_04_action.png` |
| 5 | **Step 5: cmbatsaver** | 电池节省页显示100%并提示Analyzing power usage，无操作按钮；等待分析结束以自动进入电池选择页。 | `step_05_action.png` |
| 6 | **Step 6: cmressafe** | 电池已省页混排垃圾清理、温度检测和安全恐吓文案，称有隐私入侵与安全风险；本步静态跳转下一活动。 | `step_06_screen.png` |
| 7 | **Step 7: cmshcutani** | 重复上页的电池已省与安全恐吓界面，含Catch your privacy invaders及SCAN；静态引导跳转至启动页。 | `step_07_screen.png` |
| 8 | **Step 8: cmstapge** | 应用无响应系统对话框，提供Close app与Wait；探针静态跳转至下一活动，未展示实际业务页面。 | `step_08_screen.png` |
