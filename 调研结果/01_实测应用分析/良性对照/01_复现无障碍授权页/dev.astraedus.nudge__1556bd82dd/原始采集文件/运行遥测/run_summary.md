# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:24:47
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`dev.astraedus.nudge`（静态标签：`benign` / `专注自律与防沉迷管控` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `6` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`dev.astraedus.nudge/com.astraedus.nudge.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Permissions / Nudge needs these permissions to work. No data is ever sent anywhere — the app has no internet permission. / Accessibility Service / Detects which app is in the foreground so Nudge can trigger your block rules. Also identifies in-app screens (like YouTube Shorts or Instagram Reels) by checking navigation elements. Does not read your messages, keystrokes, or screen content. / Grant Permission`
- **Back 后 +5.5s**：`dev.astraedus.nudge/com.astraedus.nudge.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Permissions / Nudge needs these permissions to work. No data is ever sent anywhere — the app has no internet permission. / Accessibility Service / Detects which app is in the foreground so Nudge can trigger your block rules. Also identifies in-app screens (like YouTube Shorts or Instagram Reels) by checking navigation elements. Does not read your messages, keystrokes, or screen content. / Grant Permission`
- **Back 后 +10.5s**：`dev.astraedus.nudge/com.astraedus.nudge.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Permissions / Nudge needs these permissions to work. No data is ever sent anywhere — the app has no internet permission. / Accessibility Service / Detects which app is in the foreground so Nudge can trigger your block rules. Also identifies in-app screens (like YouTube Shorts or Instagram Reels) by checking navigation elements. Does not read your messages, keystrokes, or screen content. / Grant Permission`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `dev.astraedus.nudge` / `MainActivity` | `-` | 6 | 139 / 否 | `click` → [6] TextView text="Next" center=(540,2016) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `dev.astraedus.nudge` / `MainActivity` | `-` | 15 | 749 / 否 | `click` → [8] TextView text="Grant Permission" center=(540,935) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `dev.astraedus.nudge` / `MainActivity` | `-` | 9 | 455 / 否 | `click` → [9] TextView text="I Understand" center=(770,1621) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 218 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`dev.astraedus.nudge/MainActivity`)**: `Nudge` | `Mindful app usage through gentle friction` | `Take back control of your screen time with breathing ex` | `Next`
- **Step 2 (`dev.astraedus.nudge/MainActivity`)**: `Permissions` | `Nudge needs these permissions to work. No data is ever ` | `Accessibility Service` | `Detects which app is in the foreground so Nudge can tri` | `Grant Permission` | `Display Over Other Apps` | `Shows the delay countdown or breathing exercise overlay` | `Usage Stats Access` | `Next`
- **Step 3 (`dev.astraedus.nudge/MainActivity`)**: `How Nudge Works` | `Nudge uses Android's Accessibility Service to detect wh` | `This lets Nudge show breathing exercises, delays, or bl` | `Nudge only reads the name of the app in the foreground.` | `All data stays on your device. Nudge has no internet pe` | `Not Now` | `I Understand`
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Nudge - App Blocker` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以“温和摩擦、夺回屏幕时间”引导进入三步式权限说明，反复强调无障碍仅识别前台应用且无联网，从而推动授予无障碍、悬浮窗与用量权限；在系统无障碍警告页拒绝后返回权限页并停留于劝授权界面（TRAPPED_ON_LURE_SCREEN）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 以“温和摩擦”实现正念应用使用（Step1主页）
- 英文 -> 通过呼吸练习、延迟和每日限额夺回屏幕时间（Step1主页）
- 英文 -> 声称所需权限必要且数据永不外发、应用无联网权限（Step2权限页）
- 英文 -> 声称不读取消息、按键或屏幕内容（Step2权限页）
- 英文 -> 以帮助后台自启恢复保护为由劝说授予悬浮窗（Step2权限页）
- 英文 -> 仅读取前台应用名、数据留在本机且无联网（Step3说明弹窗）
- 英文 -> 系统警告称授予后将完全控制设备，仅适合无障碍需求应用（系统警告弹窗）
- 英文 -> 无障碍服务详情页再次解释仅监控前台应用、数据不出设备（服务详情页）
- 英文 -> 通知横幅称无障碍关闭、应用未被拦截，点按可重新开启（各页通知）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | Nudge引导首页，称以呼吸、延迟和每日限额实现温和防沉迷；点“Next”进入权限说明。通知横幅提示无障碍已关闭、拦截失效。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 权限说明页，逐项解释无障碍、悬浮窗、用量权限，称无联网且数据不外发；本步点无障碍卡片“Grant Permission”。通知仍提示拦截失效。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 应用内说明弹窗，称无障碍仅识别前台应用名、不读内容且数据留本机；点“I Understand”确认并跳系统无障碍设置。通知横幅持续提示权限关闭。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | [无障碍列表页]系统设置中“Nudge - App Blocker”显示Off；探针捕获设置钩子后自动终止。通知横幅仍称Nudge已停止拦截，引导点按重开。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停在系统无障碍列表页，无可见控件文本与悬浮遮罩；通知横幅继续提示Nudge未拦截、权限关闭。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后2.0秒探针：界面与通知保持不变，仍为系统无障碍列表，无悬浮遮罩；应用未自动恢复授权流程。 | `step_04_probe_2000ms_screen.png` |
| 7 | **服务详情页** | Nudge无障碍服务详情页，开关Off，说明称仅监控前台应用且数据不出设备；含“Use Nudge - App Blocker”入口，通知仍提示未拦截。 | `step_04_service_detail_screen.png` |
| 8 | **系统警告弹窗(点Deny)** | 系统无障碍警告弹窗：称授予后可查看/控制屏幕、执行操作并完全控制设备，仅适合无障碍需求；本步检查后出现Allow/Deny，未点允许。 | `step_04_system_warning_screen.png` |
| 9 | **拒权返回 +2.0s** | 拒权后2秒回到权限页，仍显示Grant Permission与Next，无取消/退出；仅剩一条通知称无障碍关闭，陷入劝授权停留屏。 | `step_04_refusal_2000ms_screen.png` |
| 10 | **拒权返回 +10.5s** | 拒权后10.5秒界面无变化，仍停留在权限说明页要求Grant Permission；无取消路径且通知持续称无障碍关闭，符合TRAPPED_ON_LURE_SCREEN。 | `step_04_refusal_10500ms_screen.png` |
