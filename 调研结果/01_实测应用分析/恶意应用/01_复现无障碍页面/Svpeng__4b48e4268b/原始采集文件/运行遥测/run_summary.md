# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:36:24
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.ufotosoft.justshot`（静态标签：`malicious` / `Svpeng` / 静态可见性：`clear`）
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
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 210 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_07_layout.xml` + `step_07_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Avito to access` | `SMS` | `send and view SMS messages` | `Contacts` | `access your contacts` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Avito` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Play` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以 Avito 名义请求短信、联系人和电话权限，再经兼容警告与桌面静态跳转探测卸载器及其他应用包，最终进入无障碍设置并拉起 Google Play 全控制授权警告；拒绝后仍重新拉起无障碍设置。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 选择允许Avito访问哪些内容（Step1 权限复核页）
- 英语 -> 发送和查看短信（Step1 权限复核页）
- 英语 -> 访问你的联系人（Step1 权限复核页）
- 英语 -> 拨打和管理电话（Step1 权限复核页）
- 英语 -> 此应用针对旧版Android构建，可能无法正常运行（Step2 兼容警告）
- 英语 -> 允许Google Play完全控制你的设备？（系统警告弹窗）
- 英语 -> 完全控制适合辅助无障碍需求的应用，但不适合大多数应用（系统警告弹窗）
- 英语 -> 查看并控制屏幕（系统警告弹窗）
- 英语 -> 可读取屏幕所有内容并覆盖显示在其他应用上（系统警告弹窗）
- 英语 -> 查看并执行操作（系统警告弹窗）
- 英语 -> 可追踪你与应用或硬件传感器的交互，并代表你与应用交互（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限复核页显示“允许Avito访问”，列短信、联系人、电话权限，含取消/继续；本步点击“继续”放行。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面弹出旧版Android兼容警告，称应用可能无法正常运行；本步点击“确定”关闭警告，无通知横幅或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面或应用列表页，显示时间天气及Messages、Chrome等图标；本步尝试打开目标应用，未见目标页面与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在桌面应用列表页，界面同前；本步点击“应用列表”入口以查找并启动目标应用，无通知与遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面应用列表页无变化；静态引导跳转至系统卸载器界面，未展示实际内容，无通知与遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍在桌面应用列表页；再次静态跳转至另一应用包，未见页面内容，探针无通知、遮罩为0。 | `step_06_screen.png` |
| 7 | **Step 7: [无障碍列表页]** | 进入系统无障碍设置列表，显示Google Play为关闭及屏幕阅读器等项；捕获无障碍钩子与探针后自动终止，无遮罩。 | `step_07_screen.png` |
| 8 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍处无障碍设置页，UI文本为空、无通知横幅、遮罩数为0，未发生交互。 | `step_07_probe_800ms_screen.png` |
| 9 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍处无障碍设置页，界面未变化、无通知横幅、遮罩数为0，未发生交互。 | `step_07_probe_2000ms_screen.png` |
| 10 | **服务详情页** | 打开Google Play无障碍服务详情，显示“使用Google Play”、快捷键与“未提供说明”；本步仅检查详情，无通知与遮罩。 | `step_07_service_detail_screen.png` |
| 11 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗，称允许Google Play完全控制设备，可查看控制屏幕、执行操作；本步检查该警告，随后拒绝授权，遮罩为0。 | `step_07_system_warning_screen.png` |
| 12 | **拒权返回 +2.0s** | 拒绝后2秒返回无障碍列表，Google Play仍为关闭；因拒绝触发重新拉起无障碍设置，无通知与遮罩。 | `step_07_refusal_2000ms_screen.png` |
