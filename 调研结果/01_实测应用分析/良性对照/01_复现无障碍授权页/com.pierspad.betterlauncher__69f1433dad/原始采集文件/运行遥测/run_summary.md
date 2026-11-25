# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:38:48
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.pierspad.betterlauncher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.pierspad.betterlauncher/app.olauncher.MainActivity` | hooks=`[]` | overlays=`0` | texts=`App / lock layout description to be used a unique id to lock screen / 4:39 / Wed, 25 Nov, 100% / 1. Swipe up for all apps
2. Long press anywhere for settings`
- **Back 后 +5.5s**：`com.pierspad.betterlauncher/app.olauncher.MainActivity` | hooks=`[]` | overlays=`0` | texts=`App / lock layout description to be used a unique id to lock screen / 4:39 / Wed, 25 Nov, 100% / 1. Swipe up for all apps
2. Long press anywhere for settings`
- **Back 后 +10.5s**：`com.pierspad.betterlauncher/app.olauncher.MainActivity` | hooks=`[]` | overlays=`0` | texts=`App / lock layout description to be used a unique id to lock screen / 4:39 / Wed, 25 Nov, 100% / 1. Swipe up for all apps
2. Long press anywhere for settings`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 7 | 92 / 否 | `click` → [6] Button text="Cancel" id=button2 (click) center=(577 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.pierspad.betterlauncher` / `MainActivity` | `-` | 5 | 1016 / 否 | `click` → [4] TextView text="I agree — open settings" id=consentA | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set BetterLauncher as your default home app?` | `BetterLauncher` | `Pixel Launcher` | `Cancel` | `Set as default`
- **Step 2 (`com.pierspad.betterlauncher/MainActivity`)**: `Accessibility service` | `BetterLauncher uses the Android AccessibilityService AP` | `I agree — open settings` | `No thanks`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `BetterLauncher` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先请求设为默认桌面，随后以无障碍说明引导进入系统无障碍设置，并展示“完全控制设备”高危警告；拒绝授权后回到 BetterLauncher 主屏提示页并持续停留（TRAPPED_ON_LURE_SCREEN）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Set BetterLauncher as your default home app? -> 是否将 BetterLauncher 设为默认主屏幕应用？（默认桌面请求页）
- I agree — open settings -> 我同意——打开设置（应用内无障碍说明页）
- No thanks -> 不用了（应用内无障碍说明页）
- BetterLauncher uses the Android AccessibilityService API for optional double-tap screen locking and app limits you configure -> BetterLauncher 使用无障碍服务实现可选的双击锁屏与你设置的应用限额（应用内/服务详情说明）
- When a selected app is in cooldown, it returns to the home screen and displays the remaining cooldown -> 当所选应用处于冷却期，会返回主屏并显示剩余冷却时间（应用内/服务详情说明）
- Accessibility data is processed on your device and is not sent to servers or shared with third parties -> 无障碍数据仅在设备本地处理，不发送服务器或共享第三方（应用内/服务详情说明）
- Use BetterLauncher -> 使用 BetterLauncher（服务详情页）
- Allow BetterLauncher to have full control of your device? -> 允许 BetterLauncher 完全控制你的设备？（系统警告弹窗）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适用于帮助无障碍需求的 App，但不适合大多数 App（系统警告弹窗）
- View and control screen -> 查看并控制屏幕（系统警告弹窗）
- View and perform actions -> 查看并执行操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestRoleActivity** | 默认主屏选择页：系统询问是否将 BetterLauncher 设为默认桌面；本步点“Cancel”取消该无关请求。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 应用内无障碍说明页：长文解释双击锁屏、应用限额与本地处理；本步点“I agree — open settings”打开系统设置。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表：BetterLauncher 显示为 Off（未开启）；探针在捕获无障碍设置钩子后自动终止，无通知与遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留系统无障碍设置页，界面文本为空、无通知横幅、遮罩为0，未发生交互。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在无障碍设置页，无可见文本、无通知、无遮罩，页面状态未变，等待结束。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页：显示“Use BetterLauncher”与快捷方式选项、同段隐私说明；本步仅检查详情/警告，未开启服务。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗：警告“完全控制设备”，列读屏与代操作能力；本步仅检查，标题称点 Deny，未确认 Allow。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2.0秒：回到 BetterLauncher 主屏，显示时间、锁定布局说明与上滑/长按提示；无遮罩但停留此诱导页。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒：仍停在 BetterLauncher 主屏同一提示页，仅有时间/操作说明，无通知无遮罩，未能离开。 | `step_03_refusal_10500ms_screen.png` |
