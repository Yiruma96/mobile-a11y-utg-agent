# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:42:07
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.musheer360.swiftslate`（静态标签：`benign` / `系统效率与通用辅助` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.musheer360.swiftslate/com.musheer360.swiftslate.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Dashboard / Inactive / Enable / API Keys / 0 keys configured`
- **Back 后 +5.5s**：`com.musheer360.swiftslate/com.musheer360.swiftslate.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Dashboard / Inactive / Enable / API Keys / 0 keys configured`
- **Back 后 +10.5s**：`com.musheer360.swiftslate/com.musheer360.swiftslate.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Dashboard / Inactive / Enable / API Keys / 0 keys configured`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.musheer360.swiftslate` / `MainActivity` | `-` | 26 | 149 / 否 | `click` → [4] TextView text="Enable" center=(872,344) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 219 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.musheer360.swiftslate/MainActivity`)**: `Dashboard` | `Inactive` | `Enable` | `API Keys` | `0 keys configured` | `Add an API key to get started.` | `0` | `This Month` | `—` | `Top Command`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `SwiftSlate Assistant` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从主界面Dashboard以Inactive、Enable及“添加API密钥”提示引导开始，点击Enable跳转系统无障碍设置并展示SwiftSlate Assistant全控授权说明；在系统警告中点Deny拒权后返回应用仍停留同一Enable诱导页，表现为无权限即无法继续的卡点链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“Inactive / Enable” -> “未启用 / 启用”（主界面Dashboard服务状态与按钮，点击Enable跳往无障碍设置）
- 英文“0 keys configured / Add an API key to get started.” -> “已配置0个密钥 / 添加API密钥以开始使用”（主界面Dashboard空状态提示）
- 英文“Use SwiftSlate Assistant” -> “使用SwiftSlate助手”（无障碍服务详情页开关）
- 英文“Provides system-wide AI text replacements when trigger commands are typed.” -> “在输入触发命令时提供系统级AI文本替换”（服务详情页说明）
- 英文“Allow SwiftSlate Assistant to have full control of your device?” -> “允许SwiftSlate助手完全控制您的设备？”（系统警告弹窗）
- 英文“Full control is appropriate for apps that help you with accessibility needs, but not for most apps.” -> “完全控制适用于辅助无障碍需求的应用，但不适用于大多数应用”（系统警告弹窗）
- 英文“View and control screen / View and perform actions” -> “查看并控制屏幕 / 查看并执行操作”（系统警告弹窗风险项）
- 英文“It can read all content on the screen and display content over other apps.” -> “可读取屏幕全部内容并覆盖显示在其他应用上”（系统警告弹窗）
- 英文“It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.” -> “可跟踪您与应用或硬件传感器的交互，并代表您与应用交互”（系统警告弹窗）
- 英文“Allow / Deny” -> “允许 / 拒绝”（系统警告弹窗授权选择）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面仪表盘显示Inactive、Enable按钮及0个API密钥；点击Enable跳往无障碍设置页，无通知与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 无障碍设置列表显示SwiftSlate Assistant为Off；捕获HOOK_A11Y_SETTINGS后自动停止，无通知/遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍停在无障碍设置页，界面无文本、无通知、无遮罩，未出现叠加层。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒再次探针，仍在无障碍设置页，无文本、通知及遮罩，未见额外诱导弹窗。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页展示Use SwiftSlate Assistant及选项；说明称输入触发命令可系统级AI替换文本，无通知/遮罩。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告弹窗询问是否允许完全控制设备，列出读屏、覆盖显示、查看执行动作等风险；含Allow/Deny，无遮罩。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 点Deny拒权后2秒回到主界面，仍显示Inactive、Enable及0密钥；无通知/遮罩，停留诱导页。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍在主界面，Inactive与Enable反复提示、0密钥；无通知/遮罩，未离开诱导页。 | `step_02_refusal_10500ms_screen.png` |
