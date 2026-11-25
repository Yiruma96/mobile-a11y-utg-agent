# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:05:57
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.grand.snail`（静态标签：`malicious` / `Hydra` / 静态可见性：`clear`）
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
| 1 | `com.grand.snail` / `PermissionsActivity` | `-` | 6 | 293 / 否 | `click` → [6] Button text="GO TO SETTINGS" id=bt_goto_settings (c | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 228 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.grand.snail/PermissionsActivity`)**: `In order for the latest version of Commerzbank Sicherhe` | `Step 1 - Go to “Settings”` | `Step 2 - Open “Accessibility”` | `Step 3 - Open “Installed Services”` | `Step 4 - Turn “Commerzbank Sicherheitsupdate” on` | `GO TO SETTINGS`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Commerzbank Sicherheitsupdate` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装为“Commerzbank Sicherheitsupdate”，先在应用内以英文引导用户开启无障碍，再跳转系统无障碍列表并持续显示同文案通知；进入服务详情和系统高风险授权弹窗后，若用户拒绝则回到桌面，表现为优雅停留或降级，未继续强弹。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “为使最新版 Commerzbank Sicherheitsupdate 正常运行，你需要启用无障碍；请按以下步骤操作。” （PermissionsActivity 权限引导页）
- 英文 -> “步骤1 打开设置；步骤2 打开无障碍；步骤3 打开已安装服务；步骤4 开启 Commerzbank Sicherheitsupdate。” （PermissionsActivity 权限引导页）
- 英文 -> “允许 Commerzbank Sicherheitsupdate 完全控制你的设备？可查看并控制屏幕、查看并执行操作。” （系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: PermissionsActivity** | 应用内权限引导页，英文称需开启无障碍才能运行，列出四步设置指引；本步点击“GO TO SETTINGS”。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页，下载应用显示“Commerzbank Sicherheitsupdate”且为Off；同文案通知横幅出现，探针捕获设置钩子后终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在无障碍列表，界面文本为空，通知横幅持续，遮罩数为0，未发生交互。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针：无障碍列表无变化，仍仅有同文案通知横幅，遮罩为0，继续等待未触发新界面。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页：显示“Commerzbank Sicherheitsupdate”开关、快捷键选项及“未提供描述”；本步仅检查详情未授权。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统高风险警告弹窗：询问是否允许完全控制设备，说明可读屏、覆盖显示及代操作；本步检查弹窗，含Allow/Deny。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权后2秒回到桌面启动器，应用未再弹窗；同文案通知仍驻留，结果标记为优雅停留或降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面，无新界面或遮罩；应用保持通知横幅驻留，结果仍为优雅停留或降级。 | `step_02_refusal_10500ms_screen.png` |
