# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:51:30
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`dto.assistivetouch.touch`（静态标签：`malicious` / `GhostClicker` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$OverlaySettingsActivity` | `-` | 31 | 164 / 否 | `click` → [8] LinearLayout desc="Assistive Touch" (click) center= | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `SubSettings` | `-` | 10 | 236 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `SubSettings` | `-` | 10 | 236 / 否 | `system_button` → Back | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$OverlaySettingsActivity` | `-` | 31 | 153 / 否 | `system_button` → Back | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 6 | 93 / 否 | `click` → [4] Button text="While using the app" id=permission_all | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `dto.assistivetouch.touch` / `MainActivity` | `-` | 6 | 34 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `dto.assistivetouch.touch` / `MainActivity` | `-` | 6 | 34 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `dto.assistivetouch.touch` / `MainActivity` | `-` | 6 | 34 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$OverlaySettingsActivity`)**: `Back` | `Display over other apps` | `Search` | `More options` | `Android Auto` | `Allowed` | `Assistive Touch` | `Not allowed` | `Digital Wellbeing` | `Google`
- **Step 2 (`com.android.settings/SubSettings`)**: `Back` | `Display over other apps` | `Search settings` | `Assistive Touch` | `1.004` | `Allow display over other apps` | `Allow this app to display on top of other apps you’re u`
- **Step 3 (`com.android.settings/SubSettings`)**: `Back` | `Display over other apps` | `Search settings` | `Assistive Touch` | `1.004` | `Allow display over other apps` | `Allow this app to display on top of other apps you’re u`
- **Step 4 (`com.android.settings/Settings$OverlaySettingsActivity`)**: `Back` | `Display over other apps` | `Search` | `More options` | `Android Auto` | `Allowed` | `Assistive Touch` | `Digital Wellbeing` | `Google` | `Google Play services`
- **Step 5 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow Assistive Touch to take pictures and record video` | `While using the app` | `Only this time` | `Deny`
- **Step 6 (`dto.assistivetouch.touch/MainActivity`)**: `Start` | `Settings` | `Rate` | `More App` | `Uninstall`
- **Step 7 (`dto.assistivetouch.touch/MainActivity`)**: `Start` | `Settings` | `Rate` | `More App` | `Uninstall`
- **Step 8 (`dto.assistivetouch.touch/MainActivity`)**: `Start` | `Settings` | `Rate` | `More App` | `Uninstall`

## 中文逐页引导链路解读

> **全链路总结**：该应用先引导开启悬浮窗权限并授予相机权限，随后进入含 Start/Settings 等功能的主菜单；主菜单还会静态跳转到内部设置页、GMS 日志隐藏组件及 AdminReceiver 设备管理接收器，呈现 GhostClicker 式权限滥用与隐藏组件特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 「允许此应用显示在其他应用上层；它将能看到你的点击位置或改变屏幕显示内容」（Step 2/3 悬浮窗授权说明页）
- 英文 -> 「允许 Assistive Touch 拍照和录像吗？」（Step 5 相机权限弹窗）
- 英文 -> 「仅在使用该应用时允许」（Step 5 相机权限按钮）
- 英文 -> 「已允许 / 不允许」（Step 1/4 悬浮窗权限列表状态）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: Settings$OverlaySettingsAc** | 系统「显示在其他应用上层」列表，Assistive Touch 显示 Not allowed/不允许；点击该条目进入授权详情。 | `step_01_action.png` |
| 2 | **Step 2: SubSettings** | 悬浮窗授权详情页，开关未勾选；说明称可覆盖其他应用并读取点击、改变屏幕内容；点击开关允许。 | `step_02_action.png` |
| 3 | **Step 3: SubSettings** | 同一悬浮窗详情页，权限已开启；执行系统返回键退回列表，准备回到应用继续流程。 | `step_03_action.png` |
| 4 | **Step 4: Settings$OverlaySettingsAc** | 返回悬浮窗列表，Assistive Touch 已变为 Allowed/已允许；再次返回应用主界面。 | `step_04_action.png` |
| 5 | **Step 5: GrantPermissionsActivity** | 系统相机权限弹窗，询问是否允许 Assistive Touch 拍照录像；点击 While using the app/仅使用期间允许。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 应用主菜单含 Start、Settings、Rate、More App、Uninstall；静态跳转至内部 SettingsActivity，未显示额外诱导文案。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 仍为主菜单；静态跳转目标为 com.google.android.gms.logs.b 隐藏组件，界面无变化，属可疑后台组件探测。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 主菜单未变；静态跳转至 AdminReceiver 设备管理接收器，疑似申请或触发设备管理员能力，风险高。 | `step_08_screen.png` |
