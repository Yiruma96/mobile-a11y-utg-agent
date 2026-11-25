# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:31:33
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.procrastilearn.app`（静态标签：`benign` / `专注自律与防沉迷管控` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.procrastilearn.app/com.procrastilearn.app.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Why we need Accessibility / This app uses Android Accessibility Service permission to detect when you open selected apps (e.g., TikTok, Reddit or any other app you choose) so it can show a short learning prompt before you continue. / What we access / • Which app is currently on your screen.
 • We do NOT read your passwords, messages, or on-screen text.
 • Your data never leaves your device and is never sold or shared. / How it’s used`
- **Back 后 +5.5s**：`com.procrastilearn.app/com.procrastilearn.app.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Why we need Accessibility / This app uses Android Accessibility Service permission to detect when you open selected apps (e.g., TikTok, Reddit or any other app you choose) so it can show a short learning prompt before you continue. / What we access / • Which app is currently on your screen.
 • We do NOT read your passwords, messages, or on-screen text.
 • Your data never leaves your device and is never sold or shared. / How it’s used`
- **Back 后 +10.5s**：`com.procrastilearn.app/com.procrastilearn.app.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Why we need Accessibility / This app uses Android Accessibility Service permission to detect when you open selected apps (e.g., TikTok, Reddit or any other app you choose) so it can show a short learning prompt before you continue. / What we access / • Which app is currently on your screen.
 • We do NOT read your passwords, messages, or on-screen text.
 • Your data never leaves your device and is never sold or shared. / How it’s used`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.procrastilearn.app` / `MainActivity` | `-` | 15 | 744 / 否 | `click` → [8] CheckBox (click,unchecked) center=(133,1536) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.procrastilearn.app` / `MainActivity` | `-` | 15 | 744 / 否 | `click` → [10] View (click) center=(540,1733) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.procrastilearn.app/MainActivity`)**: `Why we need Accessibility` | `This app uses Android Accessibility Service permission ` | `What we access` | `• Which app is currently on your screen.  • We do NOT r` | `How it’s used` | `Only to trigger the learning overlay for the apps you s` | `I understand and agree to allow this app to use the Acc` | `Accept & Continue` | `Not now` | `Privacy policy & details`
- **Step 2 (`com.procrastilearn.app/MainActivity`)**: `Why we need Accessibility` | `This app uses Android Accessibility Service permission ` | `What we access` | `• Which app is currently on your screen.  • We do NOT r` | `How it’s used` | `Only to trigger the learning overlay for the apps you s` | `I understand and agree to allow this app to use the Acc` | `Accept & Continue` | `Not now` | `Privacy policy & details`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `ProcrastiLearn` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口为 MainActivity 的无障碍权限说明页，勾选同意后跳转系统无障碍设置，并在服务详情与系统高危警告弹窗中请求“完全控制设备”能力；拒绝授权后返回原说明页并保持可操作、优雅降级。整体以透明说明和防沉迷学习提示为叙事，未见通知横幅或覆盖遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Why we need Accessibility -> “为什么需要无障碍权限”（MainActivity 权限说明页）
- This app uses Android Accessibility Service permission to detect when you open selected apps ... so it can show a short learning prompt before you continue. -> “使用无障碍服务检测你打开所选应用（如 TikTok、Reddit 等），以便在继续前显示简短学习提示”（MainActivity 权限说明页）
- We do NOT read your passwords, messages, or on-screen text. Your data never leaves your device and is never sold or shared. -> “不读取密码、消息或屏幕文本；数据不离开设备、不出售不共享”（MainActivity 权限说明页）
- I understand and agree ... Accept & Continue / Not now -> “我理解并同意……接受并继续 / 暂不”（MainActivity 权限说明页）
- Allow ProcrastiLearn to have full control of your device? -> “允许 ProcrastiLearn 完全控制你的设备？”（系统警告弹窗）
- It can read all content on the screen and display content over other apps. / It can track your interactions ... and interact with apps on your behalf. -> “可读取屏幕所有内容并覆盖其他应用；可跟踪交互并代表你操作应用”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | MainActivity 无障碍说明页：称仅检测所选应用并弹学习提示，承诺不读密码/消息/屏幕文本、数据不出设备；本步点击未勾选同意框。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 同一无障碍说明页：同意框已勾选，用户点击“接受并继续”准备跳转系统授权；页面仍强调数据本地、不售不共享，无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍设置列表：下载应用下 ProcrastiLearn 显示为关闭；探针捕获无障碍设置钩子后自动终止，无通知或遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在系统无障碍设置页，界面文本为空，遮罩数为0；仅等待观察，无新增弹窗。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在系统无障碍设置页，界面文本为空，遮罩数为0；等待期间无通知横幅或诱导弹窗。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页：显示“使用 ProcrastiLearn”、快捷方式关闭及“未提供描述”；本步仅检查详情/警告，未见遮罩或通知。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高危警告弹窗：询问是否允许 ProcrastiLearn 完全控制设备，说明可读屏幕内容、覆盖其他应用并代为操作；含允许/拒绝，遮罩为0。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒绝授权返回后2秒：回到 MainActivity 同一无障碍说明页，未崩溃、未强制退出；状态为优雅停留/降级，无通知与遮罩。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒绝授权返回后10.5秒：仍停留在同一无障碍说明页，应用保持可操作并降级运行；无二次弹窗、通知横幅或遮罩。 | `step_03_refusal_10500ms_screen.png` |
