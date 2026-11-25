# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:07:33
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc`（静态标签：`malicious` / `BlackRock` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 1 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 1 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_01_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / -1°C / Cloudy, -1°C / Messages`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 212 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Update` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Google Update”名义进入系统无障碍设置，展示服务详情并触发“完全控制设备”的授权警告；测试点拒绝后返回桌面，无通知横幅或悬浮遮罩，整体表现为拒权后优雅停留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 中文意译：“Google Update”即伪装成“谷歌更新”的应用名（无障碍列表/服务详情页）
- English -> 中文意译：“Use Google Update”即启用“谷歌更新”服务（服务详情页）
- English -> 中文意译：“No description provided.”即未提供服务说明（服务详情页）
- English -> 中文意译：“Allow Google Update to have full control of your device?”即询问是否允许“谷歌更新”完全控制设备（系统警告弹窗）
- English -> 中文意译：“Full control is appropriate for apps that help you with accessibility needs, but not for most apps.”即完全控制适用于辅助无障碍需求的应用，不适用于多数应用（系统警告弹窗）
- English -> 中文意译：“View and control screen”即可查看并控制屏幕（系统警告弹窗）
- English -> 中文意译：“It can read all content on the screen and display content over other apps.”即可读取屏幕全部内容并在其他应用上叠加显示（系统警告弹窗）
- English -> 中文意译：“View and perform actions”即可查看并代你执行操作（系统警告弹窗）
- English -> 中文意译：“It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.”即可跟踪交互并代表你操作应用（系统警告弹窗）
- English -> 中文意译：“Allow”/“Deny”即允许/拒绝授权按钮（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: [无障碍列表页]** | 无障碍设置列表页：下载应用区出现伪装名“Google Update”，状态“Off/关闭”；已捕获无障碍设置钩子与探针后自动终止。 | `step_01_screen.png` |
| 2 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在无障碍设置页，UI文本为空，无通知横幅、无悬浮遮罩；仅等待观察，无点击。 | `step_01_probe_800ms_screen.png` |
| 3 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍为无障碍设置页，界面文本为空，无通知与遮罩；继续等待，未触发任何授权动作。 | `step_01_probe_2000ms_screen.png` |
| 4 | **服务详情页** | 服务详情页：伪装名“Google Update”，开关“Use Google Update/启用”，含快捷方式与音量键选项，“No description/未提供说明”；仅查看详情与警告。 | `step_01_service_detail_screen.png` |
| 5 | **系统警告弹窗(点Deny)** | 系统授权警告弹窗：询问是否允许“Google Update”完全控制设备，列明读屏、悬浮叠加和代操作能力；含Allow/Deny，本步仅检查未确认。 | `step_01_system_warning_screen.png` |
| 6 | **拒权返回 +2.0s** | 拒权后2秒：已返回Nexus桌面，显示应用列表、日期天气及Messages/Chrome/Search等图标；无弹窗遮罩，应用未反复骚扰。 | `step_01_refusal_2000ms_screen.png` |
| 7 | **拒权返回 +10.5s** | 拒权后10.5秒：仍停留在桌面，界面同前，无通知横幅与悬浮遮罩；未出现二次诱导或强制跳转，表现为优雅降级。 | `step_01_refusal_10500ms_screen.png` |
