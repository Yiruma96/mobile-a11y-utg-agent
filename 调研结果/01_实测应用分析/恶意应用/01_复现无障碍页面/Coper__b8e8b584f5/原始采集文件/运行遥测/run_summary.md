# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:21:50
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.upon.front`（静态标签：`malicious` / `Coper` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 5 步，UTG 唯一节点 `6` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 5 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_05_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.upon.front/com.involve.p041j` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Chrome' / Set switch ON`
- **Back 后 +5.5s**：`com.upon.front/com.involve.p041j` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Chrome' / Set switch ON`
- **Back 后 +10.5s**：`com.google.android.permissioncontroller/com.android.permissioncontroller.permission.ui.GrantPermissionsActivity` | hooks=`[]` | overlays=`0` | texts=`Allow Chrome to make and manage phone calls? / Allow / Deny`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 53 / 否 | `click` → [5] Button text="Deny" id=permission_deny_button (click | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 52 / 否 | `click` → [5] Button text="Deny" id=permission_deny_button (click | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [270, 130] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.upon.front` / `p041j` | `-` | 8 | 67 / 否 | `click` → [8] Button text="Open Settings" id=t_openSettings (clic | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_05_layout.xml` + `step_05_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Chrome to make and manage phone calls?` | `Allow` | `Deny`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Chrome to send and view SMS messages?` | `Allow` | `Deny`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.upon.front/p041j`)**: `Enable Accessibility Service` | `•` | `Find` | `'Chrome'` | `Set switch ON` | `Open Settings`
- **Step 5 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：com.upon.front 以“Chrome”名义先请求电话/短信权限，被拒后退回桌面并挂出“Servisi etkinleştirin/Chrome”通知，再用仿冒引导页诱导用户在系统无障碍设置中为 Chrome 开启无障碍服务；拒权返回后反复重弹同一引导和电话权限请求，具备 Coper 类无障碍滥用与循环诱导特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Servisi etkinleştirin（土耳其语） -> 启用服务（通知横幅，贯穿各页）
- Chrome（英语，用作服务名） -> 以“Chrome”名义伪装无障碍服务（通知与系统设置页）
- Enable Accessibility Service（英语） -> 启用无障碍服务（应用内引导页 step_04/detail_2/refusal）
- Find 'Chrome'（英语） -> 找到“Chrome”（应用内引导页）
- Set switch ON（英语） -> 打开开关（应用内引导页）
- Open Settings（英语） -> 打开设置（应用内引导页按钮）
- Erişebilirlik Servisileri Etkinleştirme（土耳其语） -> 启用无障碍服务（服务详情页 detail_1）
- Use Chrome（英语） -> 使用 Chrome（Chrome 无障碍服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 权限控制器请求「允许 Chrome 拨打和管理电话？」，点 Deny 拒绝，未授予电话权限，应用继续。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 权限页请求「允许 Chrome 发送和查看短信？」，点 Deny 拒绝；通知栏仍挂「启用服务/Chrome」诱导横幅。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用退回桌面启动器，可见 Messages/Chrome 图标；通知栏仍留「启用服务/Chrome」横幅，点击坐标(270,130)。 | `step_03_action.png` |
| 4 | **Step 4: p041j** | 仿冒引导页提示「启用无障碍服务：找到 Chrome 并打开开关」，点 Open Settings 跳系统无障碍设置；无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: [无障碍列表页]** | 系统无障碍列表显示下载应用 Chrome 为 Off；采集到设置 Hook 后自动终止，通知栏仍留「启用服务/Chrome」横幅。 | `step_05_screen.png` |
| 6 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留无障碍设置页，UI 未取到文本、无遮罩；通知栏持续显示「启用服务/Chrome」。 | `step_05_probe_800ms_screen.png` |
| 7 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：仍为无障碍设置页，无遮罩、无新 UI 文本；通知栏持续显示「启用服务/Chrome」诱导横幅。 | `step_05_probe_2000ms_screen.png` |
| 8 | **服务详情页** | Chrome 无障碍服务详情页，含 Use Chrome、快捷键、音量键等选项及土耳其语「启用无障碍服务」标题；仅检查未操作。 | `step_05_service_detail_screen.png` |
| 9 | **系统警告弹窗(点Deny)** | 实际回到应用内「启用无障碍服务」引导页，指示找到 Chrome 并打开开关；探针未见系统警告弹窗或遮罩。 | `step_05_system_warning_screen.png` |
| 10 | **拒权返回 +2.0s** | 拒权返回 2 秒后，应用重新弹出同一「启用无障碍服务/找到 Chrome 开开关」引导页，形成反复诱导。 | `step_05_refusal_2000ms_screen.png` |
| 11 | **拒权返回 +10.5s** | 拒权返回 10.5 秒后又弹回电话权限请求「允许 Chrome 拨打和管理电话？」，显示拒绝后仍循环诱导。 | `step_05_refusal_10500ms_screen.png` |
