# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:40:29
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`service.webview.kiszweb`（静态标签：`malicious` / `Banker` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`service.webview.kiszweb/desire.fenix.service.novoapp.packages.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WhatsLocal - Ache Já! / Webpage not available / x+AAAAAElFTkSuQmCC / The webpage at https://bitsolution.info/?odjasijdaosi could not be loaded because: / net::ERR_NAME_NOT_RESOLVED`
- **Back 后 +5.5s**：`service.webview.kiszweb/desire.fenix.service.novoapp.packages.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WhatsLocal - Ache Já! / Webpage not available / x+AAAAAElFTkSuQmCC / The webpage at https://bitsolution.info/?odjasijdaosi could not be loaded because: / net::ERR_NAME_NOT_RESOLVED`
- **Back 后 +10.5s**：`service.webview.kiszweb/desire.fenix.service.novoapp.packages.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WhatsLocal - Ache Já! / Webpage not available / x+AAAAAElFTkSuQmCC / The webpage at https://bitsolution.info/?odjasijdaosi could not be loaded because: / net::ERR_NAME_NOT_RESOLVED`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 220 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `WhatsLocal - Ache Já!` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装成「WhatsLocal - Ache Já!」WhatsApp 号码追踪器，引导用户进入系统无障碍设置，并试图诱骗用户授予自己「完全控制设备」的高危无障碍权限；用户拒绝后，应用主界面的 WebView 加载远程域名 bitsolution.info 失败，表现优雅降级并停留。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语 -> 「用 WhatsLocal - Ache Já! 追踪你想追踪的任何人的 WhatsApp！实时定位任意号码、完全免费、最好的 WhatsApp 追踪器」（无障碍服务详情页描述文本）
- 英语（系统权限弹窗）-> 「允许 WhatsLocal - Ache Já! 完全控制你的设备？」并说明该权限可查看并控制屏幕、读取屏幕上全部内容、在其他应用上叠加显示、跟踪交互并代替用户操作应用（系统警告弹窗）
- 英语（WebView 错误页）-> 「网页无法打开」，因 net::ERR_NAME_NOT_RESOLVED 无法加载 https://bitsolution.info/?odjasijdaosi（拒权后主界面）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 安卓系统「无障碍」设置页，下载应用列表中可见 WhatsLocal - Ache Já!，开关为关闭；探针捕获无障碍设置钩子后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在无障碍设置页，界面文本尚未渲染，遮罩数为 0，无通知横幅，也未执行任何点击。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：页面依旧为无障碍设置页且无可读文本，遮罩数仍为 0，期间应用未弹出覆盖层或诱导浮窗。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 无障碍服务详情页，标题为 WhatsLocal - Ache Já!，含「使用该服务」「按住音量键」「快捷方式设置」；下方葡萄牙语宣称可实时追踪任意 WhatsApp 号码、完全免费，属于典型的诱导话术。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗，询问是否允许 WhatsLocal - Ache Já! 完全控制设备，并列出可查看并控制屏幕、读取全部内容、叠加显示、代替用户操作等权限；本步仅查看后点击 Deny 拒绝。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后 2 秒返回应用主界面 MainActivity；WebView 显示「网页无法打开」，因 bitsolution.info 域名解析失败（ERR_NAME_NOT_RESOLVED），页面降级停留且未崩溃。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后 10.5 秒界面无变化，仍为同一 WebView 错误页与失效域名，无重试弹窗、无跳转、无遮罩，表现为优雅降级后的静止停留。 | `step_01_refusal_10500ms_screen.png` |
