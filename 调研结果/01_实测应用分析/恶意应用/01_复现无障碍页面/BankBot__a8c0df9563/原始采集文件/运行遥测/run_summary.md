# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:44:37
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.themdont25`（静态标签：`malicious` / `BankBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 5 步，UTG 唯一节点 `7` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 5 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_05_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.themdont25/com.themdont25.p012p` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Postegro' / Set switch ON`
- **Back 后 +5.5s**：`com.themdont25/com.themdont25.p012p` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Postegro' / Set switch ON`
- **Back 后 +10.5s**：`com.themdont25/com.themdont25.p012p` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Postegro' / Set switch ON`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 55 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 54 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [540, 190] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.themdont25` / `p012p` | `-` | 1 | 0 / 是 | `click` → [540, 676] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 207 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_05_layout.xml` + `step_05_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Postegro to make and manage phone calls?` | `Allow` | `Deny`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Postegro to send and view SMS messages?` | `Allow` | `Deny`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.themdont25/p012p`)**: (空文本)
- **Step 5 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Postegro` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先骗取电话与短信权限，再通过土耳其语通知和WebView弹窗反复诱导用户开启Postegro无障碍服务；拒权后仍重拉诱导对话框。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 -> 「Servisi etkinleştirin」（启用服务；通知标题，多页持续显示）
- 英文 -> 「Enable Accessibility Service • Find 'Postegro' Set switch ON / Open Settings」（启用无障碍服务，找到Postegro并打开开关/打开设置；WebView诱导弹窗）
- 土耳其语 -> 「Erişebilirlik Servisileri Etkinleştirme」（启用无障碍服务；服务详情页）
- 英文 -> 「Allow Postegro to make and manage phone calls?」（允许Postegro拨打和管理电话；系统权限弹窗）
- 英文 -> 「Allow Postegro to send and view SMS messages?」（允许Postegro发送和查看短信；系统权限弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 系统电话权限弹窗，英文询问是否允许Postegro拨打和管理电话；点击Allow授予，为后续诱导流程放行。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 系统短信权限弹窗，英文询问是否允许Postegro发送和查看短信；点击Allow授予；顶部已出现土耳其语服务通知。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面，可见Postegro土耳其语通知「Servisi etkinleştirin（启用服务）」；点击横幅跳转应用，未出现遮罩。 | `step_03_action.png` |
| 4 | **Step 4: p012p** | 进入Postegro空白WebView页，界面无可见文本；通知横幅仍在；点击中央区域应触发「打开设置」与无障碍诱导。 | `step_04_action.png` |
| 5 | **Step 5: [无障碍列表页]** | 系统无障碍设置列表，下载应用中有Postegro且开关Off；顶部保留启用服务通知；采集钩子后自动终止。 | `step_05_screen.png` |
| 6 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在无障碍设置列表，无文本与遮罩；Postegro启用服务通知持续显示。 | `step_05_probe_800ms_screen.png` |
| 7 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面未变化，无障碍列表无遮罩；Postegro通知横幅仍驻留，未触发新弹窗。 | `step_05_probe_2000ms_screen.png` |
| 8 | **服务详情页** | Postegro无障碍服务详情页，含Use Postegro开关及选项；底部出现土耳其语「启用无障碍服务」提示，通知仍在。 | `step_05_service_detail_screen.png` |
| 9 | **系统警告弹窗(点Deny)** | Postegro内WebView诱导弹窗：英文要求启用无障碍服务，查找Postegro并打开开关，点Open Settings；无遮罩。 | `step_05_system_warning_screen.png` |
| 10 | **拒权返回 +2.0s** | 拒权返回2秒后，同一「启用无障碍服务」诱导弹窗被重新拉起；通知横幅仍在，未提供取消出口。 | `step_05_refusal_2000ms_screen.png` |
| 11 | **拒权返回 +10.5s** | 拒权返回10.5秒后，诱导弹窗仍反复重现；页面持续要求开启无障碍并点Open Settings，通知未消失。 | `step_05_refusal_10500ms_screen.png` |
