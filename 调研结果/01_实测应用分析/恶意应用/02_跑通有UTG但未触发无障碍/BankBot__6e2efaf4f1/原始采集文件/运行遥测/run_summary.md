# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:06:18
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.mygamejewelsclassic.app`（静态标签：`malicious` / `BankBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 11 | 157 / 否 | `click` → [11] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.mygamejewelsclassic.app` / `UnityPlayerActivity` | `-` | 3 | 150 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,125 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.mygamejewelsclassic.app` / `UnityPlayerActivity` | `-` | 0 | 0 / 否 | `wait` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.mygamejewelsclassic.app` / `UnityPlayerActivity` | `-` | 0 | 0 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.mygamejewelsclassic.app` / `UnityPlayerActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.mygamejewelsclassic.app` / `UnityPlayerActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.mygamejewelsclassic.app` / `UnityPlayerActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.mygamejewelsclassic.app` / `UnityPlayerActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Jewels Star Classic to access` | `Files and media` | `access photos, media, and files on your device` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`com.mygamejewelsclassic.app/UnityPlayerActivity`)**: `Jewels Star Classic` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.mygamejewelsclassic.app/UnityPlayerActivity`)**: (空文本)
- **Step 4 (`com.mygamejewelsclassic.app/UnityPlayerActivity`)**: (空文本)
- **Step 5 (`com.mygamejewelsclassic.app/UnityPlayerActivity`)**: (空文本)
- **Step 6 (`com.mygamejewelsclassic.app/UnityPlayerActivity`)**: (空文本)
- **Step 7 (`com.mygamejewelsclassic.app/UnityPlayerActivity`)**: (空文本)
- **Step 8 (`com.mygamejewelsclassic.app/UnityPlayerActivity`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：应用以“Jewels Star Classic”游戏为名，先经系统权限复核页请求文件媒体和电话权限并点 Continue，再进入 Unity 启动/主菜单等待延迟的假“Google Service”弹窗；轨迹未捕获该弹窗，后续以静态引导跳转 MyAccessibilityService、Unity、InstallReferrer 与 Firebase 接收器等组件，呈现 BankBot 常见的无障碍服务与后台组件探测特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “选择允许 Jewels Star Classic 访问的内容；文件与媒体：访问设备上的照片、媒体和文件；电话：拨打和管理电话”（Step 1 权限复核页）
- 英语 -> “此应用为旧版 Android 构建，可能无法正常运行；请检查更新或联系开发者”（Step 2 兼容警告弹窗）
- 英语 -> “String (Your data isn’t backed up) / String (Add a backup account now)”，核心意译“你的数据未备份/立即添加备份账户”（各步顶部 Google 通知横幅）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页，列出文件媒体与电话权限；文案意译“选择允许 Jewels Star Classic 访问”；点 Continue 继续，顶部 Google 未备份通知，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: UnityPlayerActivity** | 旧版 Android 兼容警告弹窗：“此应用为旧版构建，可能无法正常运行”；点 OK 关闭进入 Unity 页，顶部 Google 未备份通知，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: UnityPlayerActivity** | Unity 加载页，无可见文字；等待加载完成及延迟假“Google Service”弹窗，顶部 Google 未备份通知，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: UnityPlayerActivity** | Unity 主菜单已显示但无文字；继续等待延迟假“Google Service”弹窗，未见授权框，顶部 Google 未备份通知，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: UnityPlayerActivity** | 仍为 UnityPlayerActivity 且无文字；静态引导跳转“.MyAccessibilityService”探针，顶部 Google 未备份通知，无遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: UnityPlayerActivity** | 仍为 UnityPlayerActivity 且无文字；静态引导回跳 UnityPlayerActivity，未见授权/诱导弹窗，顶部 Google 未备份通知，无遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: UnityPlayerActivity** | 界面无可见文字；静态引导跳转 AppMeasurementInstallReferrer 组件探针，未见诱导话术，顶部 Google 未备份通知，无遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: UnityPlayerActivity** | 仍无可见界面文字；静态引导跳转 FirebaseInstanceIdReceiver 组件探针，未见授权/诱导弹窗，顶部 Google 未备份通知，无遮罩。 | `step_08_screen.png` |
