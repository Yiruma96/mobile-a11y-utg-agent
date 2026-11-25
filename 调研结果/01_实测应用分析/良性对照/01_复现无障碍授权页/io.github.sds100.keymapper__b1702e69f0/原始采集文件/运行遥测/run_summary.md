# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:16:24
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`io.github.sds100.keymapper`（静态标签：`benign` / `按键映射与手势导航` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `7` 个，有向边 `8` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `io.github.sds100.keymapper` / `MainActivity` | `-` | 19 | 454 / 否 | `click` → [19] TextView text="OK" center=(856,1924) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `io.github.sds100.keymapper` / `MainActivity` | `-` | 20 | 260 / 否 | `click` → [3] TextView text="Fix" center=(922,347) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `io.github.sds100.keymapper` / `MainActivity` | `-` | 7 | 409 / 否 | `click` → [7] TextView text="Enable" center=(822,1555) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 209 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`io.github.sds100.keymapper/MainActivity`)**: `What's New` | `Version 4.7.1-foss` | `New` | `Variables` | `Add to, subtract from or set variables` | `Key map names` | `Give key maps custom names and sort them by name` | `• Do Not Disturb constraint` | `• Broadcast whether mappings are paused so other apps c` | `• Undo and redo changes when configuring a key map`
- **Step 2 (`io.github.sds100.keymapper/MainActivity`)**: `The accessibility service needs to be turned on for you` | `Fix` | `Disable battery optimization.` | `New group` | `¯\_(ツ)_/¯  Create a key map!  A key map is a rule to te` | `Sort` | `2 warnings` | `What's New` | `More` | `New key map`
- **Step 3 (`io.github.sds100.keymapper/MainActivity`)**: `Accessibility service must be enabled` | `You may need to allow Restricted Settings. Tap to read ` | `Key Mapper requires the use of an accessibility service` | `Cancel` | `Enable`
- **Step 4 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Key Mapper` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先展示4.7.1更新日志，随后在主界面以“按键映射必须依赖无障碍服务”反复提示，并引导点击Fix/Enable跳转系统无障碍设置；最终在系统“完全控制设备”高危警告处被拒权并返回桌面。全程仅请求无障碍权限，拒权后通知保留、应用未崩溃，呈优雅保留/降级，未见强制循环、遮罩或自动授权。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 通知横幅提示“无障碍服务已禁用，点击可启动无障碍服务”（全局通知）
- 英文 -> “必须开启无障碍服务，否则按键映射无法工作”（主界面警告）
- 英文 -> “建议关闭电池优化”（主界面提示）
- 英文 -> “必须启用无障碍服务；你可能需要允许受限设置，点击阅读说明”（说明弹窗）
- 英文 -> “Key Mapper需要无障碍服务来检测并改变你在应用外的按键行为；启用后才能创建触发和测试动作”（说明弹窗/服务详情）
- 英文 -> “允许Key Mapper完全控制你的设备？”（系统警告弹窗）
- 英文 -> “完全控制适合帮助无障碍需求的应用，但不适合大多数应用”（系统警告弹窗）
- 英文 -> “可查看并控制屏幕，读取屏幕全部内容并悬浮显示在其他应用上”（系统警告弹窗）
- 英文 -> “可查看并执行动作，追踪你与应用或硬件传感器的交互，并代表你操作应用”（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面弹4.7.1“What's New”更新日志，介绍变量与命名等；通知提示无障碍未启用。点击OK关闭弹窗，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 主界面警告无障碍未开启则映射不生效，旁有Fix；空状态引导创建映射。点击Fix开说明弹窗，通知仍提示未启用。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 弹窗称必须启用无障碍服务，称可检测并改变应用外按键、创建触发与测试；提示可能需解除受限设置。点Enable跳系统设置。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | 系统无障碍列表页，“已下载应用”中Key Mapper为Off，另有屏幕阅读器与显示设置。捕获设置钩子后自动终止，未点击开启。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留在无障碍设置页；页面未抓到文本，遮罩为0，Key Mapper未启用通知持续显示。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍在无障碍设置页；无文本、无遮罩，Key Mapper未启用通知持续存在，未见自动授权。 | `step_04_probe_2000ms_screen.png` |
| 7 | **服务详情页** | Key Mapper无障碍服务详情页，有Use Key Mapper开关、快捷键选项为Off，并重复说明需无障碍检测应用外按键。仅检查详情，未开启。 | `step_04_service_detail_screen.png` |
| 8 | **系统警告弹窗(点Deny)** | 系统弹窗问是否允许Key Mapper完全控制设备，列明可读全屏、悬浮显示、追踪交互并代操作；含Allow/Deny，仅检查未点。 | `step_04_system_warning_screen.png` |
| 9 | **拒权返回 +2.0s** | 拒权返回后2秒回到桌面启动器，显示应用列表、日期天气与图标；Key Mapper未启用通知仍在，未崩溃，呈保留/降级状态。 | `step_04_refusal_2000ms_screen.png` |
| 10 | **拒权返回 +10.5s** | 拒权返回后10.5秒仍在桌面启动器，无应用弹窗或遮罩；Key Mapper未启用通知持续存在，应用未崩溃，保持降级。 | `step_04_refusal_10500ms_screen.png` |
