# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:26:09
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.nisarexubunajo.xaroca`（静态标签：`malicious` / `Ermac` / 静态可见性：`partial_dynamic_or_remote`）
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

> **全链路总结**：该Ermac样本在无障碍设置中暴露HookAPPService，并用“启用Chrome更新服务”通知伪装诱导授权；查看服务详情并拒绝系统警告后回到桌面，未强制跳转，呈优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “启用Chrome更新服务”（应用通知横幅正文，多页持续出现，伪装Chrome更新）
- 英文 -> “如果无障碍权限已开启，请先关闭再重新开启。”（HookAPPService服务详情页）
- 英文 -> “使用HookAPPService”/“按住音量键”/“HookAPPService快捷方式”（HookAPPService服务详情页选项与说明）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表：下载应用区见HookAPPService为Off；应用通知伪装“启用Chrome更新服务”。检测到无障碍钩子与探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍在无障碍设置页，界面文本为空；应用通知持续显示“启用Chrome更新服务”，无悬浮遮罩。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针：无障碍设置页仍无可见文本；通知横幅继续显示“启用Chrome更新服务”，悬浮层为0。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | HookAPPService服务详情页：有“Use HookAPPService”“按住音量键”等选项，并提示无障碍权限需关闭再开启；仅查看未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 服务详情页系统警告检查：未见可读弹窗文本，通知横幅消失；记录为点击Deny拒绝授权，悬浮层为0。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2秒回到桌面：显示应用列表、Chrome与搜索；通知仍伪装“启用Chrome更新服务”，无强制跳转或遮罩。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面：应用列表和Chrome入口无变化；恶意通知横幅持续存在，无弹窗、无悬浮遮罩。 | `step_01_refusal_10500ms_screen.png` |
