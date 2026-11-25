# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:09:33
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.armed.little`（静态标签：`malicious` / `Sova` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `5` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.armed.little/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`gtAREXX46EByVjYKZoj9azZA / Welcome to Aras Kargo / Browser updated successfully / To use this application, click the "Continue" button and then enable Aras Kargo services. / 1Open settings`
- **Back 后 +5.5s**：`com.armed.little/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`gtAREXX46EByVjYKZoj9azZA / Welcome to Aras Kargo / Browser updated successfully / To use this application, click the "Continue" button and then enable Aras Kargo services. / 1Open settings`
- **Back 后 +10.5s**：`com.armed.little/com.tapston.burgerking.ui.AccessibilityGuideActivity` | hooks=`[]` | overlays=`0` | texts=`gtAREXX46EByVjYKZoj9azZA / Welcome to Aras Kargo / Browser updated successfully / To use this application, click the "Continue" button and then enable Aras Kargo services. / 1Open settings`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.armed.little` / `AccessibilityGuideActivity` | `-` | 5 | 93 / 否 | `click` → [540, 1755] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 209 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.armed.little/AccessibilityGuideActivity`)**: `Find Powerful Cleaner, Antivirus and grant usage Access` | `Powerful Cleaner, Antivirus`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Aras Kargo` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以“强力清理/杀毒需授权”和通知“为Aras Kargo启用访问”诱导点击，跳转系统无障碍列表及服务详情；用户拒绝返回后仍被锁在含“浏览器更新成功”和开启无障碍三步指引的诱导页，无法正常退出。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“Find Powerful Cleaner, Antivirus and grant usage Access permission” -> “寻找强力清理、杀毒功能并授予使用权限”（Step 1 应用引导页）
- 英文“Powerful Cleaner, Antivirus” -> “强力清理、杀毒”（Step 1 应用引导页）
- 英文“Update app accesses / Enable access for ‘Aras Kargo’” -> “更新应用访问权限/为‘Aras Kargo’启用访问”（Step 1、服务详情页及拒权页通知横幅）
- 英文“Service allows Accessibility for Android to scan your device for accessibility issues.” -> “该服务允许Android无障碍扫描设备无障碍问题”（服务详情页）
- 英文“Use Aras Kargo” -> “使用Aras Kargo”（服务详情页）
- 英文“Welcome to Aras Kargo / Browser updated successfully” -> “欢迎使用ArasKargo/浏览器已成功更新”（拒权返回页）
- 英文“To use this application, click the ‘Continue’ button and then enable Aras Kargo services.” -> “要使用本应用，请点击‘继续’并启用ArasKargo服务”（拒权返回页）
- 英文“1 Open settings / 2 Select Accessibility / 3 Slide the switch to enable” -> “1打开设置/2选择无障碍/3滑动开关启用”（拒权返回页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AccessibilityGuideActivity** | 应用引导页用英文“强力清理/杀毒需授予使用权限”诱导；点击CONTINUE触发“为Aras Kargo启用访问”通知流程，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳转系统无障碍设置，下载应用列表显示“Aras Kargo”为Off；因捕获无障碍设置钩子与探针自动终止，无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停在系统无障碍设置页，界面空白，无遮罩；仅残留恶意应用空通知，未触发新动作。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍为系统无障碍设置页且无文本，无遮罩；恶意应用空通知残留，未出现进一步跳转。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 无障碍服务详情页显示“使用Aras Kargo”、快捷方式关闭及“扫描设备无障碍问题”说明，包装成合规服务；通知横幅催启用，无遮罩。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统授权警告弹窗浮现于应用内引导页，拟点Deny；界面文本未捕获，无遮罩，通知横幅仍提示为“Aras Kargo”启用访问。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回+2秒仍锁在诱导页：英文“欢迎使用Aras Kargo/浏览器更新成功”并三步教开启无障碍；返回无法退出，通知横幅持续，无遮罩。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回+10.5秒仍停诱导页：英文“欢迎使用Aras Kargo/浏览器更新成功”及开启无障碍三步指引未变；返回无法退出，通知横幅持续，无遮罩。 | `step_02_refusal_10500ms_screen.png` |
