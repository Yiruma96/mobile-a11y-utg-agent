# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:43:49
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.seoadvice.swentoday`（静态标签：`malicious` / `Svpeng` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 6 步，UTG 唯一节点 `6` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 6 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_06_layout_harmony.json` |

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
| 6 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 210 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_06_layout.xml` + `step_06_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/ReviewPermissionsActivity`)**: `Choose what to allow Авито to access` | `SMS` | `send and view SMS messages` | `Contacts` | `access your contacts` | `Phone` | `make and manage phone calls` | `Cancel` | `Continue`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Авито` | `This app was built for an older version of Android and ` | `OK`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Play` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用伪装成俄语二手平台 Авито，先诱导一次性授予短信、联系人和电话权限，再多次尝试拉起主包；失败后以静态跳转进入无障碍设置，借“Google Play”名义请求完全控制设备，点 Deny 后仍重新拉起无障碍设置页。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语+俄语品牌名 -> 选择允许 Авито（Avito）访问哪些权限（权限审核页）
- send and view SMS messages -> 发送和查看短信（权限审核页）
- access your contacts -> 访问你的联系人（权限审核页）
- make and manage phone calls -> 拨打和管理电话（权限审核页）
- This app was built for an older version of Android and may not work properly. -> 此应用为旧版 Android 构建，可能无法正常运行（桌面兼容性弹窗）
- Allow Google Play to have full control of your device? -> 允许 Google Play 完全控制你的设备吗？（无障碍系统警告）
- Full control is appropriate for apps that help you with accessibility needs, but not for most apps. -> 完全控制适用于辅助功能类应用，并不适合大多数应用（无障碍警告）
- View and control screen -> 查看并控制屏幕：可读取屏幕全部内容并悬浮显示（无障碍警告）
- View and perform actions -> 查看并执行操作：可跟踪交互并代表你操作应用（无障碍警告）
- Use Google Play / Google Play shortcut / Hold volume keys / No description provided. -> 使用 Google Play / Google Play 快捷方式 / 长按音量键 / 未提供说明（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ReviewPermissionsActivity** | 系统权限审核页伪装成 Авито，列出短信、联系人、电话三项敏感权限；本步点击 Continue（继续），无取消以外的拒绝引导。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面弹出旧版 Android 兼容性提示，称 Авито 可能无法正常运行；本步点击 OK 关闭系统提示，未进入主界面。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面应用列表，显示 Messages、Chrome 等图标；本步尝试重新打开目标包，未出现新界面，继续等待权限向导。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在桌面应用列表，无新弹窗；本步再次按包名拉起目标应用，仍未出现可见界面，属重复拉起尝试。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面静态跳转兜底，目标指向 bubbleshooter.orig.jlncg46bksq；本步无可见业务页，直接切往后续无障碍相关界面。 | `step_05_screen.png` |
| 6 | **Step 6: [无障碍列表页]** | 进入系统无障碍设置列表，可见 Google Play 显示 Off；本步命中无障碍设置钩子并自动终止，未点开开关。 | `step_06_screen.png` |
| 7 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在无障碍设置页，无可见文本、无通知横幅、无遮罩，未发生二次跳转。 | `step_06_probe_800ms_screen.png` |
| 8 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：页面与遮罩仍无变化，无通知弹出，说明应用在无障碍页潜伏等待后续操作。 | `step_06_probe_2000ms_screen.png` |
| 9 | **服务详情页** | 进入 Google Play 服务详情页，显示 Use Google Play、快捷方式、长按音量键及“未提供说明”；本步仅查看详情与警告。 | `step_06_service_detail_screen.png` |
| 10 | **系统警告弹窗(点Deny)** | 系统警告弹窗称允许 Google Play 完全控制设备，并解释可读屏、悬浮、跟踪与代操作；本步查看后选择 Deny（拒绝）。 | `step_06_system_warning_screen.png` |
| 11 | **拒权返回 +2.0s** | 点 Deny 后返回无障碍列表，Google Play 仍为 Off；但应用随即重新拉起无障碍设置页，呈现拒权后复发行为。 | `step_06_refusal_2000ms_screen.png` |
