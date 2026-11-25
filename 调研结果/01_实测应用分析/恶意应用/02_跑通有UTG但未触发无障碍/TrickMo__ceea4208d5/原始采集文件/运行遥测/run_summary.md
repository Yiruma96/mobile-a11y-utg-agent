# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:14:47
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`nilheart.ptur744.lens`（静态标签：`malicious` / `TrickMo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1900] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 155 / 否 | `click` → [20] FrameLayout desc="Search" id=search_container_all_ | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `type` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 34 / 否 | `system_button` → Enter | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.googlequicksearchbox` / `SearchNowActivity` | `-` | 22 | 206 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `nilheart.ptur744.lens` / `uzvrIrYAPIBstjG5q` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `nilheart.ptur744.lens` / `uzvrIrYAPIBstjG5q` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Google services` | `Clear`
- **Step 6 (`com.google.android.googlequicksearchbox/SearchNowActivity`)**: `ALL` | `Mobile data is off` | `No data connection. Consider turning on mobile data or ` | `Turn on mobile data` | `Try again` | `FEEDBACK` | `Go to Discover` | `Google services` | `Voice Search` | `Discover`
- **Step 7 (`nilheart.ptur744.lens/uzvrIrYAPIBstjG5q`)**: (空文本)
- **Step 8 (`nilheart.ptur744.lens/uzvrIrYAPIBstjG5q`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：轨迹从 Nexus 桌面经应用抽屉搜索“Google services”进入 Google SearchNowActivity，页面提示移动数据关闭后，通过静态引导跳入恶意包 nilheart.ptur744.lens 的空 Activity。核心特征是伪装 Google 服务并借静态跳转规避正常交互，未触发授权或拒权界面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 谷歌服务（应用抽屉/搜索页，伪装应用名）
- English -> 移动数据已关闭（SearchNowActivity）
- English -> 无数据连接，建议开启移动数据或 Wi-Fi（SearchNowActivity）
- English -> 开启移动数据（SearchNowActivity）
- English -> 重试（SearchNowActivity）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面主页，显示“Apps list/应用列表”、Messages、Chrome 等；点击“应用列表”准备进入抽屉，未出现通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面，相同“Apps list”等；执行上滑以打开应用抽屉，未出现通知横幅或遮罩，也未进入恶意应用。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉显示 Calendar、Camera、Chrome 等；点击顶部“Search/搜索”容器准备检索目标应用，无通知与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 搜索页显示“Search apps, web, and more…”；输入“Google services”查伪装应用，无通知横幅或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 搜索框已填“Google services/谷歌服务”，旁有“Clear/清除”；按 Enter 执行搜索，未出现通知横幅或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: SearchNowActivity** | Google搜索页提示移动数据关闭（Mobile data is off），提供开启数据/重试；随后静态跳转恶意页，无通知遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: uzvrIrYAPIBstjG5q** | 进入恶意包 nilheart.ptur744.lens 的空 Activity，界面无文字控件；由静态引导跳转触发，无通知遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: uzvrIrYAPIBstjG5q** | 仍为恶意空 Activity（uzvr…），无 UI 文本；再次静态跳转至 .SwrYM7Y，未显示通知横幅、遮罩或取消键。 | `step_08_screen.png` |
