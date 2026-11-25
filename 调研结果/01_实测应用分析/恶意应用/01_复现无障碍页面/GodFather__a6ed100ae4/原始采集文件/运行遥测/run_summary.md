# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:52:32
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.motivities.grubroot`（静态标签：`malicious` / `GodFather` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`hook_captured`（共执行 5 步，UTG 唯一节点 `5` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 5 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_05_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.motivities.grubroot/com.motivities.grubroot.selffertility` | hooks=`[]` | overlays=`0` | texts=`Please follow the steps below on the next screen: / 1. / On the Accessibility screen, find Download Music and tap on it / Attention: may be different for each device / 2.`
- **Back 后 +5.5s**：`com.motivities.grubroot/com.motivities.grubroot.selffertility` | hooks=`[]` | overlays=`0` | texts=`Please follow the steps below on the next screen: / 1. / On the Accessibility screen, find Download Music and tap on it / Attention: may be different for each device / 2.`
- **Back 后 +10.5s**：`com.motivities.grubroot/com.motivities.grubroot.selffertility` | hooks=`[]` | overlays=`0` | texts=`Please follow the steps below on the next screen: / 1. / On the Accessibility screen, find Download Music and tap on it / Attention: may be different for each device / 2.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.motivities.grubroot` / `selffertility` | `-` | 7 | 192 / 否 | `click` → [7] Button text="OK" id=button_open (click) center=(540 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 215 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_05_layout.xml` + `step_05_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.motivities.grubroot/selffertility`)**: `Please follow the steps below on the next screen:` | `1.` | `On the Accessibility screen, find Download Music and ta` | `Attention: may be different for each device` | `2.` | `Enable the Download Music switch` | `OK`
- **Step 5 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Music Downloader` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面启动失败后经静态跳转进入伪装教程页，引导用户在系统无障碍中开启“Music Downloader/下载音乐”权限；用户点 Deny 返回后，应用反复重启同一诱导对话框/教程，呈现典型 GodFather 无障碍滥用与拒权后重试特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “请按下一屏步骤操作：在无障碍页找到 Download Music 并点击；启用 Download Music 开关；注意不同设备可能不同”（selffertility 教程页）
- 英语 -> 通知：“请授予无障碍权限以使用本应用”，标题为“Music Downloader/Settings”（无障碍列表页、系统警告弹窗）
- 英语 -> 系统警告：“允许 Music Downloader 完全控制你的设备？”并说明可查看/控制屏幕、读取全部屏幕内容、叠加显示及代你操作应用（系统警告弹窗）
- 英语 -> 服务详情：“Use Music Downloader”“未提供描述”（设备服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用列表页，显示天气与 Messages、Chrome、Search 等；代理从启动器打开 com.motivities.grubroot.truthfully，尚无应用界面。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面应用列表，上次目标未启动；代理再次直接打开该包尝试拉起应用，页面无通知、无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 仍在桌面页，启动失败后触发静态引导 Activity 跳转兜底至 .truthfully，未见应用界面或授权内容。 | `step_03_screen.png` |
| 4 | **Step 4: selffertility** | 应用教程页，英文提示在无障碍中找 Download Music 并开启开关，点 OK 前往系统设置；含误导性名称与步骤说明。 | `step_04_action.png` |
| 5 | **Step 5: [无障碍列表页]** | 系统无障碍列表，DOWNLOADED APPS 下 Music Downloader 为 Off；通知横幅催授无障碍权限，采集到设置钩子/探针后终止。 | `step_05_screen.png` |
| 6 | **跳后探针 +0.8s** | 跳后0.8秒探针，仍停在无障碍设置页，界面文本为空，仅见应用 Settings 通知，无遮罩或弹窗。 | `step_05_probe_800ms_screen.png` |
| 7 | **跳后探针 +2.0s** | 跳后2.0秒探针，仍在无障碍设置页，无界面文本与遮罩，仅保留应用 Settings 通知，状态未变化。 | `step_05_probe_2000ms_screen.png` |
| 8 | **服务详情页** | Music Downloader 服务详情页，显示 Use Music Downloader、快捷方式 Off 与“未提供描述”，用于检查权限入口与说明缺失。 | `step_05_service_detail_screen.png` |
| 9 | **系统警告弹窗(点Deny)** | 系统无障碍警告弹窗，说明可查看/控制屏幕、读取全部内容及代操作；代理检查后准备点 Deny，未授权。 | `step_05_system_warning_screen.png` |
| 10 | **拒权返回 +2.0s** | 点 Deny 返回应用教程页，仍显示英文开启无障碍步骤与 OK；拒权后立即重启同一诱导对话框。 | `step_05_refusal_2000ms_screen.png` |
| 11 | **拒权返回 +10.5s** | 拒权后10.5秒仍回到同一教程页，步骤与 OK 未变；应用持续重启诱导对话框，反复索要无障碍权限。 | `step_05_refusal_10500ms_screen.png` |
