# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:59:47
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.dewoleyulucobazu.mowesi`（静态标签：`malicious` / `Ermac` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `3` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `HookAPPService` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用通过通知横幅“启用 Chrome 更新服务”和 HookAPPService 名称进入无障碍设置与服务详情，诱导开启或重开无障碍权限；拒绝授权后退回桌面并保持/降级驻留，通知横幅仍持续存在。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “启用 Chrome 更新服务”（通知横幅，各页面持续显示）
- 英文 -> “使用 HookAPPService”（服务详情页，开关选项）
- 英文 -> “HookAPPService 快捷方式；按住音量键”（服务详情页，快捷方式设置）
- 英文 -> “若无障碍权限已开启，请先关闭再重新开启”（服务详情页，诱导重开权限）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置页：下载应用列表见 HookAPPService 处于 Off，顶部通知横幅显示 HookAPP/启用 Chrome 更新服务；探针命中后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留无障碍设置页，文本未取到；通知横幅继续显示 HookAPP/启用 Chrome 更新服务，无遮罩。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍停留无障碍设置页，界面文本为空；通知横幅持续驻留，未出现悬浮遮罩。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：显示 Use HookAPPService、OPTIONS 与快捷键“按住音量键”；英文提示若无障碍权限曾开启，请关闭再重开。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统警告/授权确认阶段（标题称点 Deny）：仍见 HookAPPService 开关及关后重开提示，未捕获弹窗文本与遮罩。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后返回 +2.0s：回到桌面启动器，见 Messages、Chrome 等图标；应用通知横幅仍驻留，未弹遮罩。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后 +10.5s：桌面保持稳定，Chrome 等图标可见；恶意通知横幅仍显示 HookAPP/启用 Chrome 更新服务。 | `step_01_refusal_10500ms_screen.png` |
