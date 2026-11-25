# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:19:39
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.lavju.pigfcb.lrymx.lhl`（静态标签：`malicious` / `GoldDigger` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1600] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 22 | 168 / 否 | `click` → [14] TextView text="PEA SMART PRO" id=icon (click) cent | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 22 | 168 / 否 | `click` → [14] TextView text="PEA SMART PRO" id=icon (click) cent | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 22 | 168 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 22 | 168 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 22 | 168 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 22 | 168 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：该样本从桌面启动器打开应用抽屉，点击伪装为“PEA SMART PRO”的图标，多次启动未生效后改由静态探针依次跳转 CheckPermissionActivity、TransplentPermissionActivity、混淆 Activity 与 SplashActivity；全程未渲染应用内页面，未见通知横幅、遮罩或权限弹窗，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器页，显示应用列表入口及 Messages、Chrome 等图标；本步点击“Apps list”，尚未进入目标应用。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面启动器，显示应用列表入口、Messages/Chrome 等；本步上滑试图打开抽屉但未成功，未见目标应用界面。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉已展开，可见“PEA SMART PRO”等图标；本步点击该图标尝试启动目标应用。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 应用抽屉仍停留原页，图标列表未变化；本步再次点击“PEA SMART PRO”，说明上一步启动未生效。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 画面仍为应用抽屉；静态探针跳转 CheckPermissionActivity，疑似权限申请入口，未见权限弹窗。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 画面仍为应用抽屉；静态探针跳转 TransplentPermissionActivity，疑似透明/悬浮权限页，未渲染界面。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 画面仍为应用抽屉；静态探针跳转混淆名 Activity（c56ddef9…），疑似规避识别的权限/加载组件，未渲染界面。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 画面仍为应用抽屉；静态探针跳转 SplashActivity，疑似启动闪屏入口，仍未渲染任何应用内诱导内容。 | `step_08_screen.png` |
