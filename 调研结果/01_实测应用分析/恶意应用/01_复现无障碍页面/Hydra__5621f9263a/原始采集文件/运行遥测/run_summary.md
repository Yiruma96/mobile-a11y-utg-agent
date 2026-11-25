# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:39:55
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.grand.yoypop`（静态标签：`malicious` / `Hydra` / 静态可见性：`packed_or_encrypted`）
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
| 1 | `com.grand.yoypop` / `PermissionsActivity` | `-` | 6 | 271 / 否 | `click` → [6] Button text="GO TO SETTINGS" id=bt_goto_settings (c | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.grand.yoypop/PermissionsActivity`)**: `In order for the latest version of Commerzbank Update t` | `Step 1 - Go to “Settings”` | `Step 2 - Open “Accessibility”` | `Step 3 - Open “Installed Services”` | `Step 4 - Turn “Commerzbank Update” on` | `GO TO SETTINGS`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Commerzbank Update` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装为“Commerzbank Update”，先以功能需要为由引导用户进入系统无障碍设置并开启完全控制权限；用户拒绝后返回桌面且应用通知仍驻留，表现为优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “为了让最新版 Commerzbank Update 正常工作，你需要启用无障碍”，并给出四步设置教程（Step 1 权限引导页）
- 英语 -> “Commerzbank Update”通知横幅重复同一说明，持续催促开启无障碍（系统无障碍列表及后续页面）
- 英语 -> 系统弹窗警告“允许 Commerzbank Update 完全控制设备？”，说明可查看/控制屏幕并代操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: PermissionsActivity** | 权限引导页：英文称“Commerzbank Update”需开启无障碍，列四步教程并诱导点“GO TO SETTINGS”跳系统设置；通知栏有GMS备份提示。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表：下载应用中显示Commerzbank Update为Off，通知横幅重复诱导开启；探针捕获A11Y_SETTINGS钩子后自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后0.8秒探针：仍停在系统无障碍页，界面无文本、无遮罩；应用与GMS通知仍在，未出现新诱导层。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍在系统无障碍页，无界面文本与遮罩；应用和GMS通知持续驻留，未见新增弹窗或跳转。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页：显示“Use Commerzbank Update”开关、快捷键与音量键选项，称无描述；仍见应用通知，未点授权。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统高风险授权弹窗：英文警告将可全面控制设备、读取屏幕并代操作，提供Allow/Deny；本步仅查看，未同意。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回桌面：Launcher主页显示应用列表与搜索，无遮罩/弹窗；应用通知仍驻留，判定为优雅停留或降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒：仍在桌面Launcher，无新增覆盖或跳转；恶意应用通知横幅持续，表现平稳降级。 | `step_02_refusal_10500ms_screen.png` |
