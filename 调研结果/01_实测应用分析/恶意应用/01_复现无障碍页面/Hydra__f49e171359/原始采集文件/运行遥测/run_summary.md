# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:32:51
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.digpbzgcd.pelnoisux`（静态标签：`malicious` / `Hydra` / 静态可见性：`packed_or_encrypted`）
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
| 1 | `com.digpbzgcd.pelnoisux` / `PermissionsActivity` | `-` | 6 | 263 / 否 | `click` → [6] Button text="GO TO SETTINGS" id=bt_goto_settings (c | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 213 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.digpbzgcd.pelnoisux/PermissionsActivity`)**: `In order for the latest version of BAWAG Security to wo` | `Step 1 - Go to “Settings”` | `Step 2 - Open “Accessibility”` | `Step 3 - Open “Installed Services”` | `Step 4 - Turn “BAWAG Security” on` | `GO TO SETTINGS`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `BAWAG Security` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用伪装成BAWAG Security，先以启用无障碍为由引导用户进入系统设置并开启服务，随后显示完全控制设备的高危授权警告；拒绝后返回桌面并保留通知横幅，无崩溃或强制兜底，呈优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 为使最新版 BAWAG Security 正常工作，需启用无障碍功能，请按以下步骤操作（PermissionsActivity/通知横幅）
- English -> 第1步进入“设置”；第2步打开“无障碍”；第3步打开“已安装服务”；第4步开启“BAWAG Security”（PermissionsActivity）
- English -> 前往设置（GO TO SETTINGS按钮，PermissionsActivity）
- English -> 使用 BAWAG Security（服务详情页开关）
- English -> 未提供描述（服务详情页）
- English/system -> 允许BAWAG Security完全控制设备？可查看并控制屏幕、读取屏幕全部内容、跟踪交互并代为操作（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: PermissionsActivity** | 应用PermissionsActivity伪装BAWAG Security，英文称需启用无障碍并列出四步，点击“GO TO SETTINGS”跳转系统设置。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | Android无障碍列表页，DOWNLOADED APPS下BAWAG Security显示Off；通知横幅复用授权话术；采集钩子后自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍在无障碍设置页，UI文本为空，通知横幅持续显示授权诱导话术，无遮罩。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在无障碍设置页，无新增界面文本，通知横幅保持授权诱导，遮罩数为0。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情SubSettings页：显示BAWAG Security、Use BAWAG Security开关及快捷键选项，底部称未提供描述；通知横幅仍在。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告弹窗：询问是否允许BAWAG Security完全控制设备，列明可查看屏幕、读取内容、代操作；有Allow/Deny，本步仅检查未授权。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝授权后2.0秒：回到NexusLauncher桌面，显示应用列表与搜索；应用通知横幅仍在，未崩溃、无二次弹窗，链路优雅降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒绝后10.5秒：仍在桌面，通知横幅持续保留授权诱导；无遮罩、无二次跳转，表现为GRACEFUL_STAY_OR_DEGRADE。 | `step_02_refusal_10500ms_screen.png` |
