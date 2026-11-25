# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:13:45
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.goami.applocker`（静态标签：`malicious` / `TOASTAMIGO` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 3 | 47 / 否 | `click` → [3] Button text="Close app" id=aerr_close (click) cente | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Smart AppLocker keeps stopping` | `App info` | `Close app`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：从桌面启动 com.goami.applocker 后应用立即崩溃，弹出“Smart AppLocker keeps stopping”，关闭弹窗后回到桌面；随后尝试打开应用抽屉，并按静态引导跳转到安装推荐页、媒体页、无障碍服务临时页及奇虎启动页，但均未渲染目标界面，未观测到授权、拒权或诱导话术。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面 NexusLauncher 首页，含“Apps list”、日期、Messages/Chrome/搜索；本步按包名启动目标应用，但目标未运行，仍停留桌面。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 系统崩溃弹窗“Smart AppLocker keeps stopping”（智能应用锁已停止），含 App info/Close app；点击 Close app 关闭弹窗，回到桌面。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面 NexusLauncher 首页再次出现，仍显示 Apps list 与常用图标；本步重试启动目标应用，但页面未变化，疑似崩溃后未进入应用。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面 NexusLauncher 首页；点击底部“Apps list（应用列表）”视图以打开应用抽屉，尝试从图标进入目标应用，仍未显示目标界面。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面 NexusLauncher 首页；静态引导跳转 InstallRecommandActivity（安装推荐页），但界面仍停在桌面，未见目标页。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面 NexusLauncher 首页；静态引导跳转 MediaActivity（媒体页），实际界面未切换，仍显示应用列表与搜索入口。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面 NexusLauncher 首页；静态引导跳转 MyAccessibilityServiceTmp（无障碍服务临时页），页面未渲染，仍为桌面，无授权提示。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面 NexusLauncher 首页；静态引导跳转 com.qihoo.util.StartActivity（奇虎通用启动页），仍未进入目标 Activity，界面保持桌面。 | `step_08_screen.png` |
