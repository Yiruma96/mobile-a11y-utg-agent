# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:37:31
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.wreck.chef`（静态标签：`malicious` / `Coper` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 6 步，UTG 唯一节点 `7` 个，有向边 `10` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 6 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_06_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.wreck.chef/com.elevator.p041j` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Chrome' / Set switch ON`
- **Back 后 +5.5s**：`com.wreck.chef/com.elevator.p041j` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Chrome' / Set switch ON`
- **Back 后 +10.5s**：`com.wreck.chef/com.elevator.p041j` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Chrome' / Set switch ON`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 53 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 52 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [360, 165] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.wreck.chef` / `p041j` | `-` | 1 | 0 / 是 | `click` → [720, 888] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.wreck.chef` / `p041j` | `-` | 8 | 67 / 否 | `click` → [8] Button text="Open Settings" id=t_openSettings (clic | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_06_layout.xml` + `step_06_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Chrome to make and manage phone calls?` | `Allow` | `Deny`
- **Step 2 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Chrome to send and view SMS messages?` | `Allow` | `Deny`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.wreck.chef/p041j`)**: (空文本)
- **Step 5 (`com.wreck.chef/p041j`)**: `Enable Accessibility Service` | `•` | `Find` | `'Chrome'` | `Set switch ON` | `Open Settings`
- **Step 6 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先诱导授予电话与短信权限，随后通过常驻土耳其语通知把用户拉回 WebView，反复指导在系统设置中为“Chrome”开启无障碍服务；用户返回拒绝后立即重弹同一诱导页，呈现 Coper 家族常见的无障碍滥用与持久化诱导特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> 允许 Chrome 拨打和管理电话（Step 1 系统权限弹窗）
- 英语 -> 允许 Chrome 发送和查看短信（Step 2 系统权限弹窗）
- 土耳其语 -> “启用服务”，通知正文为“Chrome”（Step 3/4/5 等常驻通知）
- 英语 -> 启用无障碍服务；查找“Chrome”；打开开关；打开设置（Step 5 及拒权返回页）
- 英语 -> 使用 Chrome / Chrome 快捷方式（服务详情页，伪装成 Chrome 服务）
- 土耳其语 -> “启用无障碍服务”（服务详情页说明，含拼写 Servisileri）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 系统权限弹窗请求“允许 Chrome 拨打和管理电话”，点击 Allow 同意；未见通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: GrantPermissionsActivity** | 系统权限弹窗请求“允许 Chrome 发送和查看短信”，点击 Allow 同意；仍无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 回到桌面启动器，顶部有本应用常驻通知“Servisi etkinleştirin/Chrome”（启用服务）；点击通知返回应用。 | `step_03_action.png` |
| 4 | **Step 4: p041j** | 进入应用 WebView 页，未捕获文字；保留土耳其语“启用服务”通知，按坐标点击页面以打开系统设置。 | `step_04_action.png` |
| 5 | **Step 5: p041j** | 应用内诱导页用英文指导：启用无障碍服务、查找 Chrome、打开开关；点击 Open Settings 跳系统设置。 | `step_05_action.png` |
| 6 | **Step 6: [无障碍列表页]** | 跳至系统无障碍列表，DOWNLOADED APPS 下 Chrome 显示 Off；采集到设置钩子后终止，无通知或遮罩。 | `step_06_screen.png` |
| 7 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在无障碍设置页，无 UI 文本、无通知、遮罩数为 0，仅等待观察。 | `step_06_probe_800ms_screen.png` |
| 8 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：页面未变化，无 UI 文本、无通知、遮罩数为 0，确认未出现额外覆盖层。 | `step_06_probe_2000ms_screen.png` |
| 9 | **服务详情页** | 进入 Chrome 服务详情页，显示 Use Chrome、快捷方式等选项及土耳其语“启用无障碍服务”；保持通知，仅检查未点击。 | `step_06_service_detail_screen.png` |
| 10 | **系统警告弹窗(点Deny)** | 应用内又现同一英文诱导页，指导查找 Chrome 并开启开关；遮罩为 0、无通知，仅检查未点 Deny。 | `step_06_system_warning_screen.png` |
| 11 | **拒权返回 +2.0s** | 拒权返回 2 秒后，应用立即重弹同一无障碍诱导页，常驻通知仍在；动作记为 RELAUNCHED_LURE_DIALOG。 | `step_06_refusal_2000ms_screen.png` |
| 12 | **拒权返回 +10.5s** | 拒权返回 10.5 秒后仍反复展示同一诱导页，通知未消失；再次触发 RELAUNCHED_LURE_DIALOG，显示强诱导回拉。 | `step_06_refusal_10500ms_screen.png` |
