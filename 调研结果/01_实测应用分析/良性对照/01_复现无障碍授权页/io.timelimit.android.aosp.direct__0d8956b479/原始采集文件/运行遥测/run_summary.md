# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:27:10
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`io.timelimit.android.aosp.direct`（静态标签：`benign` / `专注自律与防沉迷管控` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 7 步，UTG 唯一节点 `8` 个，有向边 `11` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 7 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_07_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`io.timelimit.android.aosp.direct/io.timelimit.android.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`TimeLimit needs some permissions to work / Usage stats access / Device admin / Notification access / Draw over other Apps`
- **Back 后 +5.5s**：`io.timelimit.android.aosp.direct/io.timelimit.android.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`TimeLimit needs some permissions to work / Usage stats access / Device admin / Notification access / Draw over other Apps`
- **Back 后 +10.5s**：`io.timelimit.android.aosp.direct/io.timelimit.android.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`TimeLimit needs some permissions to work / Usage stats access / Device admin / Notification access / Draw over other Apps`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `io.timelimit.android.aosp.direct` / `MainActivity` | `-` | 8 | 919 / 否 | `click` → [7] Button text="ACCEPT AND CONTINUE" id=btn_accept (cl | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `io.timelimit.android.aosp.direct` / `MainActivity` | `-` | 12 | 888 / 否 | `click` → [9] Button text="NEXT" id=next_button (click) center=(9 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `io.timelimit.android.aosp.direct` / `MainActivity` | `-` | 16 | 512 / 否 | `click` → [1] View (click) center=(540,452) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `io.timelimit.android.aosp.direct` / `MainActivity` | `-` | 40 | 365 / 否 | `click` → [34] View (click) center=(967,2095) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `io.timelimit.android.aosp.direct` / `MainActivity` | `-` | 40 | 365 / 否 | `click` → [11] View (click) center=(694,809) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `io.timelimit.android.aosp.direct` / `MainActivity` | `-` | 9 | 495 / 否 | `click` → [8] View (click) center=(866,1653) | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 208 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_07_layout.xml` + `step_07_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`io.timelimit.android.aosp.direct/MainActivity`)**: `Welcome to TimeLimit` | `To use TimeLimit with the default server you have to ac` | `You are using the default server` | `SELECT CUSTOM SERVER` | `TimeLimit Copyright © 2019 - 2026 Jonas Lochmann  This ` | `ACCEPT AND CONTINUE` | `TimeLimit`
- **Step 2 (`io.timelimit.android.aosp.direct/MainActivity`)**: `Keep your eye open for this icon:` | `You can show some additional info about something when ` | `User key` | `There is no key for this user` | `ADD KEY` | `This feature is only available in the local mode.` | `Some questions are answered at https://timelimit.io/en/` | `NEXT` | `Back` | `TimeLimit`
- **Step 3 (`io.timelimit.android.aosp.direct/MainActivity`)**: `local mode` | `TimeLimit limits this device. There is no connection to` | `connected mode` | `TimeLimit limits some devices. The TimeLimit settings c` | `uninstall TimeLimit` | `Not a setup option. TimeLimit revokes all permissions w` | `You can change your opinion later, but you have to rein` | `Back` | `TimeLimit`
- **Step 4 (`io.timelimit.android.aosp.direct/MainActivity`)**: `TimeLimit needs some permissions to work` | `Usage stats access` | `Device admin` | `Notification access` | `Draw over other Apps` | `Accessibility service` | `Allow applying limits` | `needs` | `or` | `needs in the future`
- **Step 5 (`io.timelimit.android.aosp.direct/MainActivity`)**: `TimeLimit needs some permissions to work` | `Usage stats access` | `Device admin` | `Notification access` | `Draw over other Apps` | `Accessibility service` | `Allow applying limits` | `needs` | `or` | `needs in the future`
- **Step 6 (`io.timelimit.android.aosp.direct/MainActivity`)**: `Accessibility service` | `This is used to "press" the home button before showing ` | `The permission was not granted` | `Apps can not grant permissions themself. You are redire` | `Cancel` | `Modify`
- **Step 7 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `TimeLimit` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从条款同意与新手引导进入模式选择，选择本地模式后进入权限总览，并以“需要权限”说明引导启用无障碍；跳转系统设置并出现高危“完全控制”警告，拒绝后返回仍卡在权限页。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “欢迎使用 TimeLimit；使用默认服务器须接受使用条款与隐私政策”（Step 1 条款页）
- 英文 -> “TimeLimit 需要一些权限才能工作”，并列使用统计、设备管理、通知、悬浮窗、无障碍等（Step 4/5 权限页）
- 英文 -> 无障碍服务用于锁屏前“按下”主页键并打开锁屏，授权需跳转系统应用（Step 6 无障碍说明弹窗）
- 英文 -> “允许 TimeLimit 完全控制你的设备？”并说明可查看/控制屏幕、代你操作（服务详情系统警告弹窗）
- 英文 -> 提醒默认配置很可能不适合，应先看官网，且公开差评不适合提问（Step 2 引导页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 条款同意页：英文提示默认服务器须接受使用条款与隐私政策，可选用自定义服务器；本步点击“ACCEPT AND CONTINUE”继续。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 引导说明页：英文介绍右上角图标提示、用户密钥与本地模式限制，并提醒先看官网/默认配置；本步点“NEXT”进入模式选择。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 模式选择页：英文列出本地模式（仅限本机、免费且隐私最大）、连接模式及卸载选项；本步点击“local mode”进入权限设置。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 权限总览页：英文称 TimeLimit 需要使用统计、设备管理、通知、悬浮窗和无障碍等权限；本步点底部“Next”推进授权流程。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 同一权限总览页：列有无障碍服务及“允许应用限制/阻止悬浮窗/限制后台音频”等说明；本步点“Accessibility service”图标打开说明弹窗。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 无障碍说明弹窗：英文称该服务用于锁屏前“按”主页键并打开锁屏，当前未授权且需跳系统设置；本步点“Modify”跳转。 | `step_06_action.png` |
| 7 | **Step 7: [无障碍列表页]** | 系统无障碍列表页：下载应用下可见 TimeLimit 处于“Off”；采集到无障碍设置钩子与探针后自动终止，未继续授权。 | `step_07_screen.png` |
| 8 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在系统无障碍设置页，页面文本为空、遮罩数为0，无弹窗或通知横幅。 | `step_07_probe_800ms_screen.png` |
| 9 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在系统无障碍设置页，页面文本为空、遮罩数为0，无弹窗或通知横幅。 | `step_07_probe_2000ms_screen.png` |
| 10 | **服务详情页** | TimeLimit 无障碍服务详情页：显示“Use TimeLimit”、快捷方式关闭及服务用途说明；本步仅检查详情，未点击启用。 | `step_07_service_detail_screen.png` |
| 11 | **系统警告弹窗(点Deny)** | 系统高危授权警告：英文问是否允许 TimeLimit 完全控制设备，并说明可读屏、显示悬浮内容及代操作；界面有 Allow/Deny。 | `step_07_system_warning_screen.png` |
| 12 | **拒权返回 +2.0s** | 拒权返回2秒后：回到 TimeLimit 权限总览页，仍列使用统计、设备管理、通知、悬浮窗、无障碍等项，流程停在诱导授权页。 | `step_07_refusal_2000ms_screen.png` |
| 13 | **拒权返回 +10.5s** | 拒权返回10.5秒后：页面未变化仍停在权限总览，未见取消/跳过出口，表现为被卡在授权引导页。 | `step_07_refusal_10500ms_screen.png` |
