# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:37:08
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.nitulshah.nudge`（静态标签：`benign` / `专注自律与防沉迷管控` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.nitulshah.nudge/com.nitulshah.nudge.MainActivity` | hooks=`[]` | overlays=`0` | texts=`nudge / Wed, Nov 25 / Settings / Turn on scroll tracking / Nudge counts scrolls and unlocks with an Android accessibility service. Nothing is tracked, and there's no score, until it's on.`
- **Back 后 +5.5s**：`com.nitulshah.nudge/com.nitulshah.nudge.MainActivity` | hooks=`[]` | overlays=`0` | texts=`nudge / Wed, Nov 25 / Settings / Turn on scroll tracking / Nudge counts scrolls and unlocks with an Android accessibility service. Nothing is tracked, and there's no score, until it's on.`
- **Back 后 +10.5s**：`com.nitulshah.nudge/com.nitulshah.nudge.MainActivity` | hooks=`[]` | overlays=`0` | texts=`nudge / Wed, Nov 25 / Settings / Turn on scroll tracking / Nudge counts scrolls and unlocks with an Android accessibility service. Nothing is tracked, and there's no score, until it's on.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.nitulshah.nudge` / `MainActivity` | `-` | 25 | 420 / 否 | `click` → [8] View (click) center=(540,720) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 219 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.nitulshah.nudge/MainActivity`)**: `nudge` | `Wed, Nov 25` | `Settings` | `Turn on scroll tracking` | `Nudge counts scrolls and unlocks with an Android access` | `Open accessibility settings` | `Find Nudge under Downloaded apps (or Installed apps) an` | `Optional: allow Display over other apps to show the flo` | `Allow display over other apps` | `0`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Nudge Scroll Tracker` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：专注自律类应用以“统计滑动/解锁、显示计数气泡”为由，引导开启无障碍服务和悬浮窗，并跳转系统无障碍列表、服务详情及全控件警告。用户点Deny拒权后仍被留在主界面诱导页，缺少关闭或替代路径，形成TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- “Nudge counts scrolls and unlocks with an Android accessibility service. Nothing is tracked, and there's no score, until it's on.” -> 用无障碍服务统计滑动与解锁，开启前不追踪、不计分（主界面）
- “Find Nudge under Downloaded apps (or Installed apps) and switch it on.” -> 到已下载/已安装应用中找到Nudge并开启（主界面）
- “Optional: allow Display over other apps to show the floating scroll-count bubble.” -> 可选允许悬浮窗以显示滑动计数气泡（主界面）
- “Nudge counts your scrolls to help you track your phone use. It only learns that a scroll happened and in which app. It cannot read text or anything else on your screen.” -> 宣称仅统计滑动及所在应用，不能读取屏幕文本（服务详情页）
- “Allow Nudge Scroll Tracker to have full control of your device? Full control is appropriate for apps that help you with accessibility needs, but not for most apps.” -> 系统警告询问是否授予完整设备控制，提醒多数应用不适用（系统警告弹窗）
- “View and control screen / It can read all content on the screen and display content over other apps.” -> 可查看控制屏幕、读取全部屏幕内容并悬浮显示（系统警告弹窗）
- “View and perform actions / It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.” -> 可跟踪与应用或硬件传感器交互并代为操作应用（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面展示“nudge”与0滑动/解锁，文案称无障碍仅统计滑动和解锁、启用前不记录；点击“Open accessibility settings”跳系统页。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍页“DOWNLOADED APPS(已下载应用)”下Nudge Scroll Tracker显示Off(关闭)；捕获设置钩子后自动终止，服务未开启。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 仍停留系统无障碍设置页，0.8秒探针未采集到界面文本，overlays=0，无通知横幅或遮罩。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 同一系统无障碍设置页等待2.0秒，界面文本仍为空，overlays=0，未见通知、横幅或遮罩弹层。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页显示“Use Nudge Scroll Tracker(使用Nudge滚动追踪器)”及快捷方式Off；说明称只知滑动及所在应用，不能读屏。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统全控件警告弹窗称可查看控制屏幕、读取全部内容并悬浮显示、跟踪交互；提供Allow(允许)/Deny(拒绝)，本步仅检查。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 点Deny拒权2秒后返回主界面，仍显示开启无障碍与悬浮窗引导，计数0，无关闭入口，判定TRAPPED_ON_LURE_SCREEN。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权10.5秒后仍停同一主界面诱导页，无障碍与悬浮窗按钮未消失，计数0，无取消/退出，维持TRAPPED_ON_LURE_SCREEN。 | `step_02_refusal_10500ms_screen.png` |
