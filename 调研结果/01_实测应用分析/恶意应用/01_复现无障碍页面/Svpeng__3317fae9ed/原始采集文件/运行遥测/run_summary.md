# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:21:22
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.nanohead.fort.last.world.war.bestActionGame`（静态标签：`malicious` / `Svpeng` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 7 步，UTG 唯一节点 `6` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 7 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_07_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / Google Play`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `ReviewPermissionsActivity` | `-` | 15 | 139 / 否 | `click` → [15] Button text="Continue" id=continue_button (click)  | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 136 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 210 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_07_layout.xml` + `step_07_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Авито to access` | `SMS` | `send and view SMS messages` | `Contacts` | `access your contacts` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Авито` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Play` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用伪装为Авито/Google Play，先请求短信、联系人、电话权限，绕过旧版兼容警告并在桌面重复拉起，随后跳转无障碍设置诱导授予Google Play完全控制；拒绝后返回无障碍页并再次拉起设置。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文/俄文「Choose what to allow Авито to access」-> 选择允许Авито访问哪些内容，并列出短信、联系人、电话（权限总览页）
- 英文「This app was built for an older version of Android and may not work properly...」-> 此应用面向旧版Android构建，可能无法正常运行，请检查更新或联系开发者（兼容性警告页）
- 英文「Use Google Play / Google Play shortcut / Hold volume keys」-> 使用Google Play、Google Play快捷方式、按住音量键（无障碍服务详情页）
- 英文「Allow Google Play to have full control of your device?」-> 允许Google Play完全控制您的设备？并称可查看控制屏幕、查看并执行操作（系统无障碍警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限总览页显示“选择允许Авито访问…”，列出短信、联系人、电话及取消/继续；本步点击“继续”提交权限请求。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面弹出旧版Android兼容警告，提示Авито可能无法正常运行；本步点击“OK”关闭警告并准备重启应用。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面应用列表，含Messages、Chrome、搜索等；本步按包名重新拉起目标应用以重启流程。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍为桌面应用列表，无新弹窗或通知；本步再次直接拉起伪装入口包，继续重启诱导流程。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面应用列表保持不变，无可见提示；静态引导跳转到n30ud6p52j1.onActivityResult，开始切换内部回调流程。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面列表仍无变化；静态引导再次跳转到telugu.telugulatestnews.n30ud6p52j1，进入下一段伪装/新闻模块。 | `step_06_screen.png` |
| 7 | **Step 7: [无障碍列表页]** | 进入系统无障碍列表，Google Play显示为关闭；已捕获无障碍设置钩子与探针后自动终止，未见通知或遮罩。 | `step_07_screen.png` |
| 8 | **跳后探针 +0.8s** | 无障碍设置列表停留0.8秒探针，界面无文本、无通知横幅、遮罩数为0，未出现额外诱导弹窗。 | `step_07_probe_800ms_screen.png` |
| 9 | **跳后探针 +2.0s** | 无障碍设置列表停留2.0秒探针，仍无文本与通知，遮罩数为0，说明跳转后未立即叠加覆盖层。 | `step_07_probe_2000ms_screen.png` |
| 10 | **服务详情页** | 打开Google Play无障碍服务详情页，含“使用Google Play”、快捷方式设置与音量键说明；本步仅检查详情，无点击。 | `step_07_service_detail_screen.png` |
| 11 | **系统警告弹窗(点Deny)** | 系统警告弹窗询问是否允许Google Play完全控制设备，列查看/控制屏幕与执行操作等能力；本步检查弹窗内容，允许/拒绝并存。 | `step_07_system_warning_screen.png` |
| 12 | **拒权返回 +2.0s** | 拒绝无障碍授权后返回无障碍列表，Google Play仍显示关闭；系统记录RELAUNCHED_A11Y_SETTINGS，应用再次拉起设置页。 | `step_07_refusal_2000ms_screen.png` |
