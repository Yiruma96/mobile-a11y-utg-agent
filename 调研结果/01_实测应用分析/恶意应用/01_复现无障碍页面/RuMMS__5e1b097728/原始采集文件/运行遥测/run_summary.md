# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:06:45
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.difficult.alarm`（静态标签：`malicious` / `RuMMS` / 静态可见性：`clear`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 215 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Ocнoвнoй прoцecc` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以伪装为“主进程”的无障碍服务和通知横幅，谎称系统异常需开启统计/无障碍权限，引导用户进入系统无障碍设置并触发授权弹窗；用户点“拒绝”后回到桌面，应用未崩溃或强退，表现为优雅降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Ocнoвнoй прoцecc -> “主进程”（无障碍列表/服务详情/授权弹窗中的服务名，混用拉丁与西里尔字形伪装系统进程）
- Cиcтeмa нe кoррeктнo работаeт, вам необходимo включить дoступ к cтaтиcтикe для 'Ocнoвнoй прoцecc' -> “系统运行不正常，您需要为‘主进程’开启统计/使用情况访问权限”（通知横幅，贯穿各页）
- Use Ocнoвнoй прoцecc -> “使用主进程”（服务详情页启用项）
- Allow Ocнoвнoй прoцecc to have full control of your device? -> “允许‘主进程’完全控制您的设备吗？”（系统无障碍授权弹窗）
- View and control screen / View and perform actions -> “查看并控制屏幕/查看并执行操作”（系统授权风险说明）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：下载应用中“主进程”为Off，通知谎称系统异常需开统计权限；采集无障碍Hook与探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8s探针：仍在无障碍设置页，UI无文本，通知横幅持续谎称系统异常需开统计权限；无遮罩，仅等待。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0s探针：页面与通知未变化，仍无遮罩；应用继续用“主进程”通知催促开启统计权限，未产生新界面。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：显示“主进程”及“使用主进程”，附快捷方式/音量键选项且无描述；系统设置页，无遮罩，通知仍催促开统计权限。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统无障碍授权弹窗：英文警告“允许主进程完全控制设备？”，列明可读屏、可代操作等风险，提供Allow/Deny；本步仅检查未点。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回+2.0s：点Deny后回到桌面，应用未崩溃或反复弹窗；通知横幅仍在，状态为GRACEFUL_STAY_OR_DEGRADE。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权返回+10.5s：仍停在桌面，无新弹窗/遮罩；恶意通知横幅未消失，链路维持优雅降级状态。 | `step_01_refusal_10500ms_screen.png` |
