# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:50:47
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`service.webview.webkisz`（静态标签：`malicious` / `Banker` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`service.webview.webkisz/desire.fenix.service.novoapp.packages.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WhatsWhere - Ache Já! / Webpage not available / x+AAAAAElFTkSuQmCC / The webpage at https://bitsolution.info/?odjasijdaosi could not be loaded because: / net::ERR_NAME_NOT_RESOLVED`
- **Back 后 +5.5s**：`service.webview.webkisz/desire.fenix.service.novoapp.packages.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WhatsWhere - Ache Já! / Webpage not available / x+AAAAAElFTkSuQmCC / The webpage at https://bitsolution.info/?odjasijdaosi could not be loaded because: / net::ERR_NAME_NOT_RESOLVED`
- **Back 后 +10.5s**：`service.webview.webkisz/desire.fenix.service.novoapp.packages.MainActivity` | hooks=`[]` | overlays=`0` | texts=`WhatsWhere - Ache Já! / Webpage not available / x+AAAAAElFTkSuQmCC / The webpage at https://bitsolution.info/?odjasijdaosi could not be loaded because: / net::ERR_NAME_NOT_RESOLVED`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 220 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `WhatsWhere - Ache Já!` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口指向无障碍设置中的伪装追踪工具 WhatsWhere - Ache Já!，先以葡语“实时追踪任意 WhatsApp 号码且免费”的话术诱导，再引导开启完全控制权限；拒权后回落至 WebView 错误页并保持降级停留，未见进一步诱导或崩溃。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语 -> 使用 WhatsWhere - Ache Já! 追踪任何人的 WhatsApp；实时定位任意号码、完全免费、最佳 WhatsApp 追踪器（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：下载应用“WhatsWhere”显示 Off；无通知/遮罩，捕获无障碍设置 Hook 后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在无障碍设置页，界面无新增文本，通知横幅与遮罩均为 0，继续等待。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：页面保持无障碍设置，未见新增文本或浮层，通知/遮罩计数为 0，仍无交互动作。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：展示“WhatsWhere - Ache Já!”及快捷方式/音量键选项；下方葡语宣称可实时追踪任意 WhatsApp 号码且免费。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统授权弹窗：英文提示该应用将获得设备完全控制、可读屏并代操作；含 Allow/Deny，本步选择 Deny 拒绝。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回 +2.0 秒：进入应用 MainActivity WebView，显示网页不可用及 ERR_NAME_NOT_RESOLVED；无通知/遮罩，呈降级停留。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权返回 +10.5 秒：仍停留在同一 WebView 错误页，域名 bitsolution.info 解析失败；无通知横幅与遮罩，未恢复诱导流程。 | `step_01_refusal_10500ms_screen.png` |
