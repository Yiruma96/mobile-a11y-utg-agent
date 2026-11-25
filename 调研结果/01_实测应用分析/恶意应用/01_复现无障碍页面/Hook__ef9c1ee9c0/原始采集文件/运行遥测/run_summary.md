# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:31:21
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.gohaxacupumasa.kipo`（静态标签：`malicious` / `Hook` / 静态可见性：`partial_dynamic_or_remote`）
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
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `FlexTV` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先通过“FlexTV/Enable FlexTV”通知引导进入系统无障碍列表，将 FlexTV 服务显示为关闭并诱导开启；进入服务详情页要求开关权限，拒权后回到桌面且通知仍在，整体呈优雅停留/降级而不崩溃。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- String (FlexTV) / String (Enable FlexTV) -> “FlexTV/启用 FlexTV”（无障碍列表页及服务详情页通知横幅）
- Use FlexTV -> “使用 FlexTV”（服务详情页开关）
- If accessibility permission has been on, please turn off then turn on. -> “若无障碍权限已开启，请先关闭再重新开启”（服务详情页说明）
- FlexTV shortcut / Hold volume keys -> “FlexTV 快捷方式/按住音量键”（服务详情页选项）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍列表页：FlexTV 显示 Off，通知“Enable FlexTV”催促启用；采集到无障碍 Hook 与探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 同一无障碍列表页跳后探针：界面文本未采集，FlexTV 通知仍在，遮罩 0；等待 0.8 秒无新增交互。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 同一无障碍列表页跳后探针：界面文本未采集，FlexTV 通知仍在，遮罩 0；继续等待 2.0 秒仍无变化。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | FlexTV 服务详情页：Use FlexTV 开关、快捷方式与音量键选项，并提示权限开启后需关闭再开启；未授权。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 服务详情页出现系统警告弹窗并点 Deny 拒绝；未采到弹窗正文，遮罩 0，仍显示返回、FlexTV、Use FlexTV。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权返回桌面：FlexTV 通知仍在，无遮罩；2 秒后未崩溃，呈 GRACEFUL_STAY_OR_DEGRADE。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权返回桌面 10.5 秒：FlexTV 通知仍在，无遮罩；应用持续未崩溃，维持优雅停留/降级。 | `step_01_refusal_10500ms_screen.png` |
