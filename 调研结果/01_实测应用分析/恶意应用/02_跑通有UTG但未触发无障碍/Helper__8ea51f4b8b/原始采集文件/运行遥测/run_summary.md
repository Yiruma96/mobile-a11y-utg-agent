# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:21:36
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`loaddex.hb.com.loaddex.psx`（静态标签：`malicious` / `Helper` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `click` → [19] FrameLayout desc="Search" id=search_container_all_ | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `type` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 26 / 否 | `click` → [5] ImageView desc="Clear" id=clear_or_voice_button (cl | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `loaddex` | `Clear`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`

## 中文逐页引导链路解读

> **全链路总结**：该应用未在桌面、应用抽屉或搜索中暴露入口，代理只能通过静态 Activity 跳转依次探针 Accessibilitypsx、Receiverpsx、Notificationpsx；界面始终停留在原生桌面搜索页，未出现授权/拒权交互、通知横幅或遮罩，故未见具体诱导话术。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 原生桌面首页，显示“Apps list/应用列表”、日期与天气；点击“应用列表”试图打开抽屉，但未见目标应用。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面首页，内容同前；从屏幕底部上滑以展开应用抽屉，未出现目标应用界面或任何提示。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉已展开，列出日历、相机、Chrome等；点击顶部“Search/搜索”容器，仍未发现loaddex图标。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面全局搜索页，显示“搜索应用、网页等”输入框；聚焦后准备输入包名片段，尚无目标应用结果。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 搜索框内输入“loaddex”，无匹配应用；点击右侧“Clear/清除”按钮清空关键词，未触发目标组件。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍停留在桌面搜索页；静态引导跳转尝试进入.Accessibilitypsx，界面未变化，无授权弹窗或说明话术。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍为桌面搜索页；静态跳转尝试进入.Receiverpsx，页面无可见变化，未出现接收器相关界面或系统提示。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 仍为桌面搜索页；静态跳转尝试进入.Notificationpsx，未显示通知监听授权页，也无通知横幅或遮罩。 | `step_08_screen.png` |
