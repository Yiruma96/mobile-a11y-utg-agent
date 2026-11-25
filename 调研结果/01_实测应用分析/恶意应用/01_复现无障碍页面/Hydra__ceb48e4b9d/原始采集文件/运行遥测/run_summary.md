# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:05:30
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.grand.dogla`（静态标签：`malicious` / `Hydra` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `5` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.grand.dogla` / `PermissionsActivity` | `-` | 6 | 301 / 否 | `click` → [6] Button text="GO TO SETTINGS" id=bt_goto_settings (c | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 232 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.grand.dogla/PermissionsActivity`)**: `In order for the latest version of Commerzbank Sicherhe` | `Step 1 - Go to “Settings”` | `Step 2 - Open “Accessibility”` | `Step 3 - Open “Installed Services”` | `Step 4 - Turn “Commerzbank Sicherheitszertifikat” on` | `GO TO SETTINGS`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Commerzbank Sicherheitszertifikat` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以仿冒的“Commerzbank Sicherheitszertifikat”为名，先用引导页诱导用户开启无障碍，再跳转到系统设置定位服务，并触发“完全控制设备”警告；用户拒绝后返回桌面，通知横幅持续驻留，无遮罩也无崩溃，表现为优雅停留或降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “为使最新版 Commerzbank Sicherheitszertifikat 正常工作，您需要启用无障碍功能。请按以下步骤操作：”（PermissionsActivity 权限引导页）
- 英语 -> “第1步-进入设置；第2步-打开无障碍；第3步-打开已安装服务；第4步-开启 Commerzbank Sicherheitszertifikat”（PermissionsActivity 权限引导页）
- 英语/德语品牌名 -> “Commerzbank Sicherheitszertifikat（德国商业银行安全证书）”（系统无障碍列表、服务详情页与通知横幅，仿冒银行安全证书名称）
- 英语 -> “允许 Commerzbank Sicherheitszertifikat 完全控制您的设备？完全控制适合辅助无障碍需求的应用，但不适合大多数应用。查看并控制屏幕 / 查看并执行操作 / 允许 / 拒绝”（系统全控警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: PermissionsActivity** | 权限引导页：英文称需为仿冒银行证书启用无障碍并按四步设置，点击“GO TO SETTINGS”跳系统设置。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 无障碍列表页：见仿冒“Commerzbank Sicherheitszertifikat”状态为Off；通知横幅重复诱导语，采集设置钩子后终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒仍为无障碍列表，文本为空、无遮罩；应用通知横幅持续显示诱导语，仅等待未操作。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒仍停在无障碍列表空文本页，无遮罩；通知横幅持续驻留复述诱导，仅等待。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页：显示启用项“Use Commerzbank Sicherheitszertifikat”、快捷键及“未提供描述”；本步仅检查，通知仍在。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统全控警告弹窗：英文称可查看并控制屏幕、代操作应用，含Allow/Deny；本步仅检查，随后拒绝。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝后2秒回到桌面，无应用遮罩；通知横幅仍驻留，状态为优雅停留/降级，未见崩溃或进一步诱导页。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒绝后10.5秒仍在桌面，无遮罩弹窗；仿冒证书通知持续驻留，应用保持优雅降级，未再请求无障碍。 | `step_02_refusal_10500ms_screen.png` |
