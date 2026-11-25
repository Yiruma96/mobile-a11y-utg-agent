# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:23:22
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.carriez.flutter_hbb`（静态标签：`benign` / `远程协助与跨设备互联` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `6` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.carriez.flutter_hbb/com.carriez.flutter_hbb.MainActivity` | hooks=`[]` | overlays=`0` | texts=`RustDesk / Service is not running
Tap [Start service] or enable [Screen capture] permission to start the screen sharing service. / Start service / Permissions
Change path / Screen capture`
- **Back 后 +5.5s**：`com.carriez.flutter_hbb/com.carriez.flutter_hbb.MainActivity` | hooks=`[]` | overlays=`0` | texts=`RustDesk / Service is not running
Tap [Start service] or enable [Screen capture] permission to start the screen sharing service. / Start service / Permissions
Change path / Screen capture`
- **Back 后 +10.5s**：`com.carriez.flutter_hbb/com.carriez.flutter_hbb.MainActivity` | hooks=`[]` | overlays=`0` | texts=`RustDesk / Service is not running
Tap [Start service] or enable [Screen capture] permission to start the screen sharing service. / Start service / Permissions
Change path / Screen capture`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.carriez.flutter_hbb` / `MainActivity` | `-` | 15 | 135 / 否 | `click` → [14] Button desc="Share screen
Tab 3 of 4" (click) cent | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.carriez.flutter_hbb` / `MainActivity` | `-` | 14 | 308 / 否 | `click` → [7] Switch desc="Input control" (click,unchecked) cente | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.carriez.flutter_hbb` / `MainActivity` | `-` | 18 | 626 / 否 | `click` → [18] Button desc="Open system setting" (click) center=( | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.carriez.flutter_hbb/MainActivity`)**: `RustDesk` | `Oops, no recent sessions! Time to plan a new one.` | `Connection Tab 1 of 4` | `Chat Tab 2 of 4` | `Share screen Tab 3 of 4` | `Settings Tab 4 of 4`
- **Step 2 (`com.carriez.flutter_hbb/MainActivity`)**: `RustDesk` | `Service is not running Tap [Start service] or enable [S` | `Start service` | `Permissions Change path` | `Screen capture` | `Input control` | `Transfer file` | `Audio capture` | `Enable clipboard` | `Connection Tab 1 of 4`
- **Step 3 (`com.carriez.flutter_hbb/MainActivity`)**: `RustDesk` | `Service is not running Tap [Start service] or enable [S` | `Start service` | `Permissions Change path` | `Screen capture` | `Input control` | `Transfer file` | `Audio capture` | `Enable clipboard` | `Connection Tab 1 of 4`
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `RustDesk Input` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以 RustDesk 远程协助为入口，先引导进入“共享屏幕—输入控制”，再弹出“如何获取 Android 输入权限？”并跳转系统无障碍开启 RustDesk Input，最终触发“完全控制设备”的高危授权警告；拒绝后返回应用仍停在权限引导页，呈现 TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “哎呀，暂无最近会话！该规划新会话了。”（RustDesk 主页）
- 英语 -> “服务未运行：点[启动服务]或启用[屏幕捕获]权限以启动屏幕共享服务。”（共享屏幕权限页）
- 英语 -> “如何获取 Android 输入权限？”（共享屏幕权限页弹窗）
- 英语 -> “当 RustDesk 屏幕共享建立后，允许其他设备使用虚拟触控控制你的手机。”（RustDesk Input 服务详情页）
- 英语 -> “允许 RustDesk Input 完全控制你的设备吗？”（系统警告弹窗）
- 英语 -> “完全控制适合帮助无障碍需求的 App，但不适合大多数 App。”（系统警告弹窗）
- 英语 -> “查看并控制屏幕：可读取屏幕所有内容并悬浮显示在其他应用上。”（系统警告弹窗）
- 英语 -> “查看并执行操作：可跟踪你与应用或硬件传感器的交互，并代表你操作应用。”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | RustDesk 主页，底部四标签；空会话提示意为“暂无最近会话，去新建一个”。本步点击“共享屏幕”标签，无通知、无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 共享屏幕权限页，提示服务未运行，可启动服务或开屏幕捕获。本步点击“输入控制”开关（未勾选），无通知、无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 权限页弹出“如何获取 Android 输入权限？”说明；本步点“打开系统设置”，仍未启动服务，无通知、无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | 跳系统无障碍列表，“RustDesk Input”显示为“关闭”；捕获无障碍设置钩子后终止，无通知、无遮罩。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍停留系统无障碍设置页；无新增文本、无通知，遮罩数为 0。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针，仍在系统无障碍设置页；无可读文本更新、无通知，遮罩数为 0。 | `step_04_probe_2000ms_screen.png` |
| 7 | **服务详情页** | RustDesk Input 详情页，含“使用”开关与快捷键；说明称共享后他机可用虚拟触控控制本机，无通知、无遮罩。 | `step_04_service_detail_screen.png` |
| 8 | **系统警告弹窗(点Deny)** | 系统警告弹窗询问是否允许 RustDesk Input 完全控制设备，列屏幕/操作控制项，有允许/拒绝；本步点拒绝。 | `step_04_system_warning_screen.png` |
| 9 | **拒权返回 +2.0s** | 拒绝后 2 秒返回应用权限页，仍显示服务未运行与输入控制等开关；停留诱导页，无通知、无遮罩。 | `step_04_refusal_2000ms_screen.png` |
| 10 | **拒权返回 +10.5s** | 拒绝后 10.5 秒仍困在应用权限引导页，服务未运行提示与输入控制开关未消失，无通知、无遮罩，未自动退出。 | `step_04_refusal_10500ms_screen.png` |
