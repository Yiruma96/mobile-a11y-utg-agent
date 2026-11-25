# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:53:04
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.nightcommonwz`（静态标签：`malicious` / `Coper` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [7] TextView text="Chrome" (click) center=(741,1804) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.chrome` / `FirstRunActivity` | `-` | 4 | 237 / 否 | `system_button` → Home | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 59 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 59 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.android.chrome/FirstRunActivity`)**: `Welcome to Chrome` | `By using Chrome, you agree to the Google Terms of Servi` | `Help make Chrome better by sending usage statistics and` | `Accept & continue`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Chrome to send and view SMS messages?` | `Allow` | `Deny`
- **Step 8 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Google Chrome to send and view SMS messages?` | `Allow` | `Deny`

## 中文逐页引导链路解读

> **全链路总结**：该样本（com.nightcommonwz，伪装名 Google Chrome）无桌面启动图标，探针只能从桌面反复按包名/静态跳转拉起；链路最终落在借用“Google Chrome”名义的系统短信权限弹窗上，反复索要收发与查看短信的高危权限。全程未见自有业务界面，属以正版 Chrome 名义掩护的权限骗取型链路，最终未完成允许/拒绝测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “允许 Google Chrome 发送和查看短信？”（Step 7/8 系统权限弹窗，应用名被伪造成 Google Chrome，仅“允许/拒绝”两项、无取消键）
- 英文 -> “欢迎使用 Chrome……接受并继续”（Step 2 真实 Chrome 首次运行页，为样本借用的正版外壳话术，非样本自身诱导）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面主页，可见 Chrome、信息等图标；探针点击 Chrome 图标，误启正版 Chrome，说明恶意包伪装同名但无启动图标。 | `step_01_action.png` |
| 2 | **Step 2: FirstRunActivity** | 正版 Chrome 首次运行欢迎页，提示接受服务条款并发送使用统计；探针按 Home 键退出，确认非目标样本界面。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面主页，仍无恶意应用图标；探针改为按包名直接启动其主 Activity，画面未发生变化。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍停留桌面，第二次尝试按包名拉起恶意主入口；界面无任何响应，说明其入口被隐藏或延迟加载。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面静止画面，探针改用静态引导跳转回退至 .p034a 组件；UI 无变化，无通知横幅、无遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面静止画面，再次静态跳转至 .p090b；前台仍无落地界面，跳转疑似在后台静默完成。 | `step_06_screen.png` |
| 7 | **Step 7: GrantPermissionsActivity** | 系统权限弹窗，以“Google Chrome”名义请求发送与查看短信；仅有允许/拒绝，无取消键，属高危短信权限诱导。 | `step_07_screen.png` |
| 8 | **Step 8: GrantPermissionsActivity** | 同一短信权限弹窗重复出现，探针再次以静态跳转触发；反复索权强化诱导，仍无取消或暂不选项。 | `step_08_screen.png` |
