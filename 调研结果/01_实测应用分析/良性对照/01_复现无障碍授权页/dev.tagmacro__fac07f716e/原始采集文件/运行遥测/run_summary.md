# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:31:30
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`dev.tagmacro`（静态标签：`benign` / `系统效率与通用辅助` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`dev.tagmacro/dev.tagmacro.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Settings / Permissions / Each one is optional, and only needed for the actions listed. TagMacro has no internet permission. / Accessibility service / Not allowed`
- **Back 后 +5.5s**：`dev.tagmacro/dev.tagmacro.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Settings / Permissions / Each one is optional, and only needed for the actions listed. TagMacro has no internet permission. / Accessibility service / Not allowed`
- **Back 后 +10.5s**：`dev.tagmacro/dev.tagmacro.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Settings / Permissions / Each one is optional, and only needed for the actions listed. TagMacro has no internet permission. / Accessibility service / Not allowed`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `dev.tagmacro` / `MainActivity` | `-` | 22 | 367 / 否 | `click` → [21] LinearLayout desc="Settings" (click) center=(936,2 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `dev.tagmacro` / `MainActivity` | `-` | 26 | 734 / 否 | `click` → [8] Button text="Open accessibility settings" (click) c | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`dev.tagmacro/MainActivity`)**: `Macros` | `No macros yet` | `A macro is a list of actions that runs when you tap a t` | `1` | `Tap New macro and pick a template, or start blank.` | `2` | `Fill in anything marked "Needs setup", then Save.` | `3` | `Tap "Write trigger to a tag" and hold a sticker to the ` | `4`
- **Step 2 (`dev.tagmacro/MainActivity`)**: `Settings` | `Permissions` | `Each one is optional, and only needed for the actions l` | `Accessibility service` | `Not allowed` | `For Signal, WhatsApp and Lock the screen. It only recei` | `Open accessibility settings` | `If the switch is greyed out as a restricted setting: op` | `Open App info` | `Do Not Disturb access`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `TagMacro messaging` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从宏列表引导进入权限设置，以“权限可选、无联网、仅服务消息/锁屏”等话术推动开启无障碍，并指导绕过受限设置；跳转系统无障碍详情与高风险授权弹窗后，审核拒绝即返回应用并反复停留在仍未授权的权限页（TRAPPED_ON_LURE_SCREEN）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“Each one is optional, and only needed for the actions listed. TagMacro has no internet permission.” -> “每项权限可选，仅用于所列动作；无联网权限”（Step 2 权限页）
- 英文“For Signal, WhatsApp and Lock the screen...” -> “无障碍仅接收 Signal/WhatsApp 事件，且只在宏发送时读屏”（Step 2 权限页）
- 英文“If the switch is greyed out as a restricted setting...” -> “如开关因受限设置变灰，去应用信息菜单选‘允许受限设置’再试”（Step 2 权限页）
- 英文“Lets TagMacro send Signal and WhatsApp messages, share WhatsApp live location, and lock the screen...” -> “称可按宏发消息、共享 WhatsApp 实时位置并锁屏，且无联网”（服务详情页）
- 英文“Allow TagMacro messaging to have full control of your device?” -> “询问是否允许完整控制设备，并称适合无障碍需求而非多数应用”（系统警告弹窗）
- 英文“View and control screen / View and perform actions” -> “可读取屏幕全部内容并悬浮显示，可跟踪交互并代为操作”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面为宏列表空状态，展示创建宏四步引导与“New macro/Tags”；本步点击设置标签进入权限页，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 权限页称权限可选且无联网，解释无障碍仅服务消息与锁屏，并教绕过受限设置；本步点“Open accessibility settings”。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表显示“TagMacro messaging”为 Off；探针捕获无障碍设置钩子后自动终止，无通知、无遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留系统无障碍列表；页面未取到文本，无通知、无遮罩，仅执行等待。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍在系统无障碍列表；未出现通知横幅或遮罩，保持等待，无进一步点击。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页显示“Use TagMacro messaging”开关，快捷方式为 Off；说明称仅按宏发消息、共享位置或锁屏且无联网。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告弹窗询问是否允许“完整控制设备”，列明读屏与代操作能力，并含 Allow/Deny；审核选择拒绝。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒绝后2秒返回应用权限页，无障碍仍为“Not allowed”；页面重复打开设置及绕过受限设置引导，已困在诱导页。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权后10.5秒仍停留同一权限页，未跳转也未解除提示；无障碍保持“Not allowed”，判定困在诱导屏幕。 | `step_03_refusal_10500ms_screen.png` |
