# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:20:31
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.jrsx.dkeczy.okgpu.jie`（静态标签：`malicious` / `GoldDigger` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `swipe` → [540, 1900] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 149 / 否 | `click` → [20] FrameLayout desc="Search" id=search_container_all_ | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `type` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 22 / 否 | `click` → [5] ImageView desc="Clear" id=clear_or_voice_button (cl | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `eGOVph` | `Files` | `Gmail`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `sso` | `Clear`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`

## 中文逐页引导链路解读

> **全链路总结**：本次轨迹始终停留在NexusLauncher桌面、应用抽屉与全局搜索，未捕获目标应用实际界面；搜索“sso”无结果后清空，随后三次静态跳转尝试进入CheckPermissionActivity、TransplentPermissionActivity与SplashActivity，但画面仍为桌面，未出现权限弹窗或诱导话术，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | NexusLauncher桌面主页，显示“Apps list”应用列表与天气-1°C；点击应用列表但未见抽屉打开，无通知与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面主页，外文“Apps list/Cloudy”意为应用列表/多云；从底部上滑以打开应用抽屉，仍无通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉已展开，可见Calendar、eGOVph等图标；点击顶部Search搜索框，尚未进入目标应用，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 全局搜索页，“Search apps, web, and more…”意为搜索应用与网页；搜索框获得焦点并输入关键词，无结果页尚未出现。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 搜索页输入“sso”，未匹配到应用；点击Clear清空搜索框，页面仍为桌面搜索，无目标应用界面、通知或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面搜索页；静态跳转尝试打开CheckPermissionActivity（检查权限页），但截图仍停在搜索页，未出现权限弹窗或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面搜索页；静态跳转尝试进入TransplentPermissionActivity（透明权限页），画面未变化，仍无权限弹窗、通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面搜索页；静态跳转尝试进入SplashActivity（启动闪屏页），仍停留在搜索界面，未捕获目标应用内容或授权提示。 | `step_08_screen.png` |
