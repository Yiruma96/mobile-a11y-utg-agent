# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:27:05
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`dev.midnightbeam`（静态标签：`benign` / `远程协助与跨设备互联` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `dev.midnightbeam` / `PhoneActivity` | `-` | 1 | 0 / 是 | `click` → [540, 1580] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `dev.midnightbeam` / `PhoneActivity` | `-` | 16 | 465 / 否 | `swipe` → [540, 1600] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `dev.midnightbeam` / `PhoneActivity` | `-` | 16 | 465 / 否 | `swipe` → [540, 1300] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `dev.midnightbeam` / `PhoneActivity` | `-` | 16 | 465 / 否 | `swipe` → [540, 1700] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `dev.midnightbeam` / `PhoneActivity` | `-` | 16 | 465 / 否 | `click` → [8] View desc="Allow" id=su-b1 (click) center=(595,1001 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$OverlaySettingsActivity` | `-` | 31 | 161 / 否 | `click` → [17] LinearLayout desc="MidnightBeam" (click) center=(5 | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `SubSettings` | `-` | 10 | 234 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `SubSettings` | `-` | 10 | 234 / 否 | `system_button` → Back | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`dev.midnightbeam/PhoneActivity`)**: (空文本)
- **Step 2 (`dev.midnightbeam/PhoneActivity`)**: `MidnightBeam` | `Back` | `SET UP THIS DEVICE` | `For the warm filter and the dimming to work on this pho` | `1` | `Display over other appsRequired` | `Lets MidnightBeam draw the filter over the screen. In t` | `Allow` | `Start using it` | `Allow “Display over other apps” first: without it nothi`
- **Step 3 (`dev.midnightbeam/PhoneActivity`)**: `MidnightBeam` | `Back` | `SET UP THIS DEVICE` | `For the warm filter and the dimming to work on this pho` | `1` | `Display over other appsRequired` | `Lets MidnightBeam draw the filter over the screen. In t` | `Allow` | `Start using it` | `Allow “Display over other apps” first: without it nothi`
- **Step 4 (`dev.midnightbeam/PhoneActivity`)**: `MidnightBeam` | `Back` | `SET UP THIS DEVICE` | `For the warm filter and the dimming to work on this pho` | `1` | `Display over other appsRequired` | `Lets MidnightBeam draw the filter over the screen. In t` | `Allow` | `Start using it` | `Allow “Display over other apps” first: without it nothi`
- **Step 5 (`dev.midnightbeam/PhoneActivity`)**: `MidnightBeam` | `Back` | `SET UP THIS DEVICE` | `For the warm filter and the dimming to work on this pho` | `1` | `Display over other appsRequired` | `Lets MidnightBeam draw the filter over the screen. In t` | `Allow` | `Start using it` | `Allow “Display over other apps” first: without it nothi`
- **Step 6 (`com.android.settings/Settings$OverlaySettingsActivity`)**: `Back` | `Display over other apps` | `Search` | `More options` | `Android Auto` | `Allowed` | `Digital Wellbeing` | `Google` | `Google Play services` | `MidnightBeam`
- **Step 7 (`com.android.settings/SubSettings`)**: `Back` | `Display over other apps` | `Search settings` | `MidnightBeam` | `1.14.0` | `Allow display over other apps` | `Allow this app to display on top of other apps you’re u`
- **Step 8 (`com.android.settings/SubSettings`)**: `Back` | `Display over other apps` | `Search settings` | `MidnightBeam` | `1.14.0` | `Allow display over other apps` | `Allow this app to display on top of other apps you’re u`

## 中文逐页引导链路解读

> **全链路总结**：应用从 PhoneActivity 的 WebView 落地页进入“本机设置”，以暖色滤镜/调光需要权限为由，先引导开启悬浮窗并跳转系统设置授权，再返回准备继续无障碍授权；整体属分步权限引导，未见明显恶意诱导话术，拒权路径未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- EN "Use on this device" -> “在此设备上使用”（Step 1 落地页，进入本机设置）
- EN "SET UP THIS DEVICE" -> “设置此设备”（Step 2-5 设置页标题）
- EN "For the warm filter and the dimming to work on this phone, Android needs your permission. It takes a few seconds." -> 暖色滤镜与调光需 Android 授权，只需几秒（Step 2-5）
- EN "Display over other appsRequired" -> “显示在其他应用上层（必需）”（Step 2-5，步骤1）
- EN "Lets MidnightBeam draw the filter over the screen. In the list, find MidnightBeam and turn the switch on, then come back here." -> 允许 MidnightBeam 在屏幕上绘制滤镜，去列表打开开关再返回（Step 2-5）
- EN "Allow “Display over other apps” first: without it nothing changes on the screen." -> 必须先允许悬浮窗，否则屏幕不会变化（Step 2-5）
- EN "Or control a TV or projector instead" -> 或改为控制电视/投影仪（Step 2-5）
- EN "Allow this app to display on top of other apps you’re using. This app will be able to see where you tap or change what’s displayed on the screen." -> 允许覆盖其他应用；应用可看到点击位置并改变屏幕显示（Step 7-8 系统授权页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: PhoneActivity** | WebView落地页；通知栏显示“String(MidnightBeam)”及滤镜0%/亮度100%/1100K；无遮罩；点击“Use on this device”进入本机设置。 | `step_01_action.png` |
| 2 | **Step 2: PhoneActivity** | 本机设置页仅见步骤1悬浮窗权限“Required”，称授权后才能绘制滤镜；下滑未露出步骤2，通知横幅仍在，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: PhoneActivity** | 继续下滑仍停留步骤1悬浮窗授权卡，要求在列表开启MidnightBeam；步骤2未出现，通知横幅持续，无遮罩。 | `step_03_action.png` |
| 4 | **Step 4: PhoneActivity** | 再次下滑页面仍在顶部，只显示步骤1悬浮窗权限与“Allow”；步骤2未展开，通知横幅显示滤镜参数，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: PhoneActivity** | 点击步骤1“Allow”跳转系统悬浮窗列表；通知横幅仍显示滤镜0%/亮度100%/1100K，页面无遮罩。 | `step_05_action.png` |
| 6 | **Step 6: Settings$OverlaySettingsAc** | 系统悬浮窗权限列表，MidnightBeam标为“Not allowed”；点击该应用条目进入开关详情，无通知横幅与遮罩。 | `step_06_action.png` |
| 7 | **Step 7: SubSettings** | 系统授权详情页显示MidnightBeam 1.14.0，悬浮窗开关未开；系统提示可覆盖屏幕并感知点击；本步点击开关授权。 | `step_07_action.png` |
| 8 | **Step 8: SubSettings** | 悬浮窗开关已开启，系统仍提示应用可覆盖屏幕并感知点击；按返回键回应用，准备继续步骤2无障碍授权。 | `step_08_action.png` |
