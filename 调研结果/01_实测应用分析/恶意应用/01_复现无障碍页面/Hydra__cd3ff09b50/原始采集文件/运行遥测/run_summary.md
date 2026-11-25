# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:27:26
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.camp.make`（静态标签：`malicious` / `Hydra` / 静态可见性：`partial_dynamic_or_remote`）
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
| 1 | `com.camp.make` / `PermissionsActivity` | `-` | 6 | 275 / 否 | `click` → [6] Button text="GO TO SETTINGS" id=bt_goto_settings (c | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 219 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.camp.make/PermissionsActivity`)**: `In order for the latest version of Commerzbank Security` | `Step 1 - Go to “Settings”` | `Step 2 - Open “Accessibility”` | `Step 3 - Open “Installed Services”` | `Step 4 - Turn “Commerzbank Security” on` | `GO TO SETTINGS`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Commerzbank Security` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用以“Commerzbank Security”银行安全组件为幌子，先引导用户开启无障碍，再进入系统无障碍开关与全权控制警告；用户拒绝后回到桌面，通知仍反复诱导，但未见锁死或强制弹窗，表现为优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “为了让最新版 Commerzbank Security 正常工作，需开启无障碍，请按以下步骤操作”（PermissionsActivity/无障碍列表通知）
- 英语 -> “步骤1 前往设置；步骤2 打开无障碍；步骤3 打开已安装服务；步骤4 开启 Commerzbank Security”（PermissionsActivity）
- 英语 -> “前往设置”（PermissionsActivity按钮）
- 英语 -> “使用 Commerzbank Security”（服务详情页开关）
- 英语 -> “允许 Commerzbank Security 完全控制您的设备？”（系统警告弹窗）
- 英语 -> “完全控制适合辅助无障碍需求的应用，但不适合大多数应用”（系统警告弹窗）
- 英语 -> “查看并控制屏幕：可读取屏幕全部内容并覆盖显示在其他应用上”（系统警告弹窗）
- 英语 -> “查看并执行操作：可跟踪您与应用或硬件传感器的交互，并代表您操作应用”（系统警告弹窗）
- 英语 -> “未提供说明”（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: PermissionsActivity** | 权限引导页伪装银行安全组件，要求开启无障碍并列出四步；点击“前往设置”，顶部有本应用提示及谷歌备份通知，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页，该应用显示“Off/关闭”，通知栏重复诱导开启无障碍；本步终止并捕获无障碍设置钩子与探测。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒仍在无障碍列表页，无可见控件；应用通知重复开启无障碍话术，谷歌备份通知仍在，遮罩0，仅等待。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒仍为无障碍列表页，无文字控件；通知栏继续显示开启无障碍提示与谷歌备份通知，遮罩0，等待无变化。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 银行安全服务详情页，有“Use/使用”开关、快捷方式及音量键选项，并标注“未提供说明”；本步仅检查详情，无遮罩。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告弹窗称允许该应用完全控制设备，可读屏覆盖、跟踪交互并代操作；含Allow/允许与Deny/拒绝，本步检查，遮罩0。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝后2秒回到桌面启动器，显示应用列表、日期及Messages等；应用通知仍诱导开启无障碍，遮罩0，结果优雅停留/降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒绝后10.5秒仍在桌面启动器，界面同前，应用通知继续诱导开启无障碍；遮罩0，未见强制跳转，维持优雅停留/降级。 | `step_02_refusal_10500ms_screen.png` |
