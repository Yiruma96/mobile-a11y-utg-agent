# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:03:18
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.yogadisodoxatuse.fapeze`（静态标签：`malicious` / `Hook` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 199 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size` | `Default`

## 中文逐页引导链路解读

> **全链路总结**：该应用通过常驻通知“Enable Accessibility/启用无障碍”把用户引向系统无障碍设置与服务详情页，并提示关闭后再开启权限，随后弹出系统全控制警告；点击Deny后返回桌面且无崩溃、无进一步遮罩，表现为优雅停留或降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “启用无障碍”（应用通知横幅，在无障碍列表、服务详情、系统警告及返回桌面阶段均常驻）
- English -> “若无障碍权限已开启，请关闭后再开启”（服务详情页的权限操作提示）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页，显示“Accessibility/无障碍”“DOWNLOADED APPS/已下载应用”等；应用横幅提示“启用无障碍”，捕获HOOK后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 同一无障碍列表页跳后0.8秒探针，界面文本为空；应用“启用无障碍”通知仍常驻，遮罩数为0，仅等待无操作。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 无障碍列表页跳后2秒探针，文本仍为空；应用“启用无障碍”通知常驻，遮罩数为0，未见新增弹窗或覆盖层。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 无障碍服务详情页，显示“Use Accessibility/使用无障碍”及“OPTIONS/选项”；含英文提示“若无障碍权限已开启请关闭再开启”，应用通知仍常驻。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统授权警告弹窗，英文说明无障碍可“查看控制屏幕/执行操作”，有Allow/允许与Deny/拒绝；遮罩0，本步仅检查未授予。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 点Deny拒绝后返回桌面启动器，显示应用列表、日期及Messages/Chrome等；应用“启用无障碍”通知仍常驻，结果为优雅停留或降级。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面启动器，界面同前含Apps list/应用列表等；无障碍通知未消失，未见悬浮遮罩，判定优雅降级。 | `step_01_refusal_10500ms_screen.png` |
