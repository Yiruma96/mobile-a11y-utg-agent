# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:38:50
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.atlotzowj`（静态标签：`malicious` / `Octo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 60 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 59 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 100] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 16 | 424 / 否 | `click` → [10] FrameLayout (click) center=(540,756) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.atlotzowj` / `p013g` | `-` | 1 | 0 / 是 | `click` → [300, 370] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.atlotzowj` / `p013g` | `-` | 8 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.atlotzowj` / `p013g` | `-` | 8 | 74 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.atlotzowj` / `p013g` | `-` | 8 | 74 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Chrome to make and manage phone calls?` | `Allow` | `Deny`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Chrome to send and view SMS messages?` | `Allow` | `Deny`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `5:39` | `5:39 AM` | `Off` | `Wi-Fi,` | `On` | `Bluetooth.` | `Do Not Disturb.` | `Flashlight` | `Auto-rotate screen` | `Battery Saver`
- **Step 5 (`com.atlotzowj/p013g`)**: (空文本)
- **Step 6 (`com.atlotzowj/p013g`)**: `Enable Accessibility Service` | `•` | `Find` | `'Google Chrome'` | `Set switch ON` | `Open Settings`
- **Step 7 (`com.atlotzowj/p013g`)**: `Enable Accessibility Service` | `•` | `Find` | `'Google Chrome'` | `Set switch ON` | `Open Settings`
- **Step 8 (`com.atlotzowj/p013g`)**: `Enable Accessibility Service` | `•` | `Find` | `'Google Chrome'` | `Set switch ON` | `Open Settings`

## 中文逐页引导链路解读

> **全链路总结**：该应用先借助Chrome的名义骗取电话与短信运行时权限，再通过土耳其语通知和WebView页面引导用户启用无障碍服务，并伪装成Google Chrome，核心特征是权限滥用与无障碍诱导授权。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “允许Google Chrome拨打和管理电话？”（Step 1 权限授权页）
- 英文 -> “允许Google Chrome发送和查看短信？”（Step 2 权限授权页）
- 土耳其语 -> “启用服务”，副文案为“Google Chrome”（Step 3/4/8 通知横幅）
- 英文 -> “启用无障碍服务”“找到‘Google Chrome’”“打开开关”“打开设置”（Step 6-8 WebView引导页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 系统权限弹窗，请求允许Chrome拨打和管理电话；点击“Allow”授予电话权限，顶部有系统备份提醒。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 系统权限弹窗，请求允许Chrome发送和查看短信；点击“Allow”授予短信权限，继续推进后续诱导。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面，出现土耳其语通知“Servisi etkinleştirin/Google Chrome”催促启用服务；执行上滑未进入应用页。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 下拉快捷设置显示通知栏，应用通知仍催促“启用服务—Google Chrome”；点击该通知准备打开提示页。 | `step_04_action.png` |
| 5 | **Step 5: p013g** | 应用内空白WebView页，无可见文字；按坐标点击疑似“打开设置”按钮，触发跳转无障碍设置意图。 | `step_05_action.png` |
| 6 | **Step 6: p013g** | WebView引导页，英文指示“启用无障碍服务、找到Google Chrome、打开开关”；本步静态跳转到下一活动。 | `step_06_screen.png` |
| 7 | **Step 7: p013g** | 同一无障碍诱导页，反复展示“Find ‘Google Chrome’/Set switch ON/Open Settings”；静态跳转继续推进。 | `step_07_screen.png` |
| 8 | **Step 8: p013g** | 仍为无障碍诱导页，通知横幅“Servisi etkinleştirin—Google Chrome”再次催促；静态跳转至下一活动。 | `step_08_screen.png` |
