# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:39:21
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.secure.protect.world`（静态标签：`malicious` / `BanBra` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$WriteSettingsActivity` | `-` | 25 | 124 / 否 | `system_button` → Back | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$OverlaySettingsActivity` | `-` | 31 | 160 / 否 | `system_button` → Back | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$OverlaySettingsActivity` | `-` | 31 | 160 / 否 | `click` → [8] LinearLayout desc="DEFENSOR ID" (click) center=(540 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `SubSettings` | `-` | 10 | 230 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `SubSettings` | `-` | 10 | 230 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$OverlaySettingsActivity` | `-` | 31 | 149 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `Settings$OverlaySettingsActivity` | `-` | 31 | 149 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `Settings$OverlaySettingsActivity` | `-` | 31 | 149 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$WriteSettingsActivity`)**: `Back` | `Modify system settings` | `Search` | `More options` | `Camera` | `Allowed` | `Contacts` | `DEFENSOR ID` | `Not allowed` | `Google`
- **Step 2 (`com.android.settings/Settings$OverlaySettingsActivity`)**: `Back` | `Display over other apps` | `Search` | `More options` | `Android Auto` | `Allowed` | `DEFENSOR ID` | `Not allowed` | `Digital Wellbeing` | `Google`
- **Step 3 (`com.android.settings/Settings$OverlaySettingsActivity`)**: `Back` | `Display over other apps` | `Search` | `More options` | `Android Auto` | `Allowed` | `DEFENSOR ID` | `Not allowed` | `Digital Wellbeing` | `Google`
- **Step 4 (`com.android.settings/SubSettings`)**: `Back` | `Display over other apps` | `Search settings` | `DEFENSOR ID` | `1.4` | `Allow display over other apps` | `Allow this app to display on top of other apps you’re u`
- **Step 5 (`com.android.settings/SubSettings`)**: `Back` | `Display over other apps` | `Search settings` | `DEFENSOR ID` | `1.4` | `Allow display over other apps` | `Allow this app to display on top of other apps you’re u`
- **Step 6 (`com.android.settings/Settings$OverlaySettingsActivity`)**: `Back` | `Display over other apps` | `Search` | `More options` | `Android Auto` | `Allowed` | `DEFENSOR ID` | `Digital Wellbeing` | `Google` | `Google Play services`
- **Step 7 (`com.android.settings/Settings$OverlaySettingsActivity`)**: `Back` | `Display over other apps` | `Search` | `More options` | `Android Auto` | `Allowed` | `DEFENSOR ID` | `Digital Wellbeing` | `Google` | `Google Play services`
- **Step 8 (`com.android.settings/Settings$OverlaySettingsActivity`)**: `Back` | `Display over other apps` | `Search` | `More options` | `Android Auto` | `Allowed` | `DEFENSOR ID` | `Digital Wellbeing` | `Google` | `Google Play services`

## 中文逐页引导链路解读

> **全链路总结**：该应用动态轨迹主要停留在系统设置：先打开“修改系统设置”，再进入“显示在其他应用上层”并为 DEFENSOR ID 开启悬浮窗权限；后续仅出现 Google 测量/Firebase 组件的静态跳转，未采集到应用自身诱导文案或拒权结果。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: Settings$WriteSettingsActi** | 安卓“修改系统设置”授权列表页，列出 DEFENSOR ID 等应用及允许状态；本步发现目标不是无障碍提示，点击返回。 | `step_01_action.png` |
| 2 | **Step 2: Settings$OverlaySettingsAc** | 安卓“显示在其他应用上层”总列表，显示 DEFENSOR ID 等应用及允许状态；仍非目标页，本步按返回键退出。 | `step_02_action.png` |
| 3 | **Step 3: Settings$OverlaySettingsAc** | 仍在“显示在其他应用上层”列表；本步点击 DEFENSOR ID 条目，进入该应用的悬浮窗单独授权页。 | `step_03_action.png` |
| 4 | **Step 4: SubSettings** | DEFENSOR ID 1.4 的悬浮窗单独授权页，含英文开关与说明；本步点击未勾选开关开启“允许显示在其他应用上层”。 | `step_04_action.png` |
| 5 | **Step 5: SubSettings** | 同一悬浮窗授权页，开关已开启；系统提示该应用可覆盖屏幕并读取点击位置，本步按返回键回到列表。 | `step_05_action.png` |
| 6 | **Step 6: Settings$OverlaySettingsAc** | 返回“显示在其他应用上层”列表，界面无新增授权；静态引导尝试跳转 Google 测量安装来源组件，未出现应用诱导页。 | `step_06_screen.png` |
| 7 | **Step 7: Settings$OverlaySettingsAc** | 界面仍为悬浮窗总列表，DEFENSOR ID 等状态未变；静态引导转向 Firebase 消息接收器，未观察到实际页面变化。 | `step_07_screen.png` |
| 8 | **Step 8: Settings$OverlaySettingsAc** | 仍停留在悬浮窗总列表；静态引导再跳 Firebase 实例 ID 服务，仅组件级探针，无可见界面或诱导话术。 | `step_08_screen.png` |
