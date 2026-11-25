# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:35:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`service.webview.strongwebview`（静态标签：`malicious` / `Banker` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`service.webview.strongwebview/desire.fenix.service.novoapp.packages.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WLocalize - Ache Já! / Webpage not available / x+AAAAAElFTkSuQmCC / The webpage at https://bitsolution.info/?odjasijdaosi could not be loaded because: / net::ERR_NAME_NOT_RESOLVED`
- **Back 后 +5.5s**：`service.webview.strongwebview/desire.fenix.service.novoapp.packages.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WLocalize - Ache Já! / Webpage not available / x+AAAAAElFTkSuQmCC / The webpage at https://bitsolution.info/?odjasijdaosi could not be loaded because: / net::ERR_NAME_NOT_RESOLVED`
- **Back 后 +10.5s**：`service.webview.strongwebview/desire.fenix.service.novoapp.packages.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WLocalize - Ache Já! / Webpage not available / x+AAAAAElFTkSuQmCC / The webpage at https://bitsolution.info/?odjasijdaosi could not be loaded because: / net::ERR_NAME_NOT_RESOLVED`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 219 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `WLocalize - Ache Já!` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先进入系统无障碍列表，显示已安装的 WLocalize 为 Off；随后服务详情页用葡萄牙语“实时追踪任意 WhatsApp 号码、完全免费”诱导开启无障碍。系统全控权弹窗选择 Deny 后，应用退回自身 MainActivity，WebView 加载 bitsolution.info 失败并显示 net::ERR_NAME_NOT_RESOLVED，整体优雅停留或降级，无通知或遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语 -> “使用 WLocalize - Ache Já! 追踪任何人的 WhatsApp！实时定位任意号码；完全免费；最佳 WhatsApp 追踪器”（服务详情页）
- 英语 -> “允许 WLocalize - Ache Já! 完全控制你的设备吗？可查看和控制屏幕、查看并执行操作”（系统警告弹窗）
- 英语 -> “网页无法访问：https://bitsolution.info/?odjasijdaosi 无法加载，net::ERR_NAME_NOT_RESOLVED”（拒权返回页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍列表：已下载应用 WLocalize 显示 Off；采集无障碍设置钩子后自动终止，无通知与遮罩。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留系统无障碍设置页，界面文本为空，通知与遮罩均为 0；仅等待观察，无点击。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：仍在无障碍设置页，未捕获界面文本，通知与遮罩均为 0；继续等待且无操作。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：提示启用 WLocalize 无障碍及音量键快捷方式；葡语宣称可实时追踪任意 WhatsApp 号码且免费，属诱导；仅检查未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统全控警告：英文询问是否允许 WLocalize 完全控制设备，可查看和控制屏幕并代为操作；检查后点 Deny，无遮罩。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回+2.0s：退回 WLocalize 主界面，WebView 报“网页无法访问”，bitsolution.info 解析失败；呈优雅停留或降级，无通知遮罩。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权返回+10.5s：仍停留 WLocalize 主界面，WebView 继续显示同一域名解析失败错误；无新增通知或遮罩，维持降级状态。 | `step_01_refusal_10500ms_screen.png` |
