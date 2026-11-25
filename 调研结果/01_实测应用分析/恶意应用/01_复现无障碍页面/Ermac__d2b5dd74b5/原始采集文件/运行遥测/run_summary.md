# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:43:42
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.zejapizehiyuki.yijoro`（静态标签：`malicious` / `Ermac` / 静态可见性：`partial_dynamic_or_remote`）
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

> **全链路总结**：该应用通过常驻通知“HookAPP／启用 Chrome 更新服务”把用户引至系统无障碍设置，诱导开启 HookAPPService；服务详情页再用“关闭再开启无障碍权限”等说明推动授权。代理点击 Deny 返回桌面后，无弹窗或遮罩，表现为 GRACEFUL_STAY_OR_DEGRADE。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> “HookAPP／启用 Chrome 更新服务”（常驻通知；以更新服务名义伪装）
- English -> “使用 HookAPPService”（无障碍服务详情页授权开关）
- English -> “HookAPPService 快捷方式／按住音量键／快捷方式设置”（服务详情页，弱化风险）
- English -> “若无障碍权限已开启，请先关闭再重新开启。”（服务详情页，推动重新授权）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 系统无障碍列表页，DOWNLOADED APPS中HookAPPService显示Off；常驻通知称启用Chrome更新服务，无遮罩，捕获探针后终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳后0.8秒探针仍停留无障碍列表，页面文本为空，遮罩0；HookAPP通知持续存在，未触发新界面。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳后2.0秒探针继续等待，无障碍列表无新增文本、遮罩0；通知仍显示HookAPP/启用Chrome更新服务。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | HookAPPService服务详情页，见Use HookAPPService、音量键快捷方式及关闭再开启无障碍提示；无遮罩，检查详情。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 服务详情页触发系统警告弹窗但文本未捕获，遮罩0；仍见Use HookAPPService等，本步检查后点Deny拒绝授权。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 点Deny后约2秒返回Nexus桌面，可见Chrome等图标，遮罩0；HookAPP通知仍在，应用未弹窗，呈降级停留。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒仍在Nexus桌面，Apps list、Chrome等正常显示，遮罩0；HookAPP通知持续，未见二次诱导。 | `step_01_refusal_10500ms_screen.png` |
