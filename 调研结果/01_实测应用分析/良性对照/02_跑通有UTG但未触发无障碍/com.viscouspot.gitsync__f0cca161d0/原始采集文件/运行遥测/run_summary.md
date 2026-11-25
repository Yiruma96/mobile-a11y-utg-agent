# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:19:00
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.viscouspot.gitsync`（静态标签：`benign` / `远程协助与跨设备互联` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.viscouspot.gitsync` / `MainActivity` | `-` | 4 | 93 / 否 | `click` → [4] Button desc="LET'S GO" (click) center=(786,2010) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.viscouspot.gitsync` / `MainActivity` | `-` | 15 | 248 / 否 | `click` → [15] Button desc="SKIP" (click) center=(909,2010) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.viscouspot.gitsync` / `MainActivity` | `-` | 7 | 285 / 否 | `click` → [5] View desc="Sync Mode
Automated file syncing in the  | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.viscouspot.gitsync` / `MainActivity` | `-` | 7 | 285 / 否 | `click` → [7] Button desc="NEXT" (click) center=(817,2010) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.viscouspot.gitsync` / `MainActivity` | `-` | 12 | 189 / 否 | `click` → [12] Button desc="PREMIUM FEATURES" (click) center=(777 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.viscouspot.gitsync` / `MainActivity` | `-` | 11 | 337 / 否 | `swipe` → [900, 1100] | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.viscouspot.gitsync` / `MainActivity` | `-` | 12 | 382 / 否 | `swipe` → [900, 1100] | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.viscouspot.gitsync` / `MainActivity` | `-` | 12 | 355 / 否 | `swipe` → [540, 1800] | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.viscouspot.gitsync/MainActivity`)**: `Effortless File Syncing` | `Works in the background, your work always in focus` | `I'M FAMILIAR` | `LET'S GO`
- **Step 2 (`com.viscouspot.gitsync/MainActivity`)**: `How did you discover GitSync?` | `Help us understand where our users come from (select al` | `Reddit` | `Obsidian Git Plugin` | `YouTube` | `Discord` | `Medium` | `Google Search` | `AI Search (ChatGPT, Claude, Grok)` | `GitHub / F-Droid`
- **Step 3 (`com.viscouspot.gitsync/MainActivity`)**: `Choose your focus` | `You can change this later in settings` | `Client Mode Everything you would expect from a git clie` | `Sync Mode Automated file syncing in the background Auto` | `BACK` | `NEXT`
- **Step 4 (`com.viscouspot.gitsync/MainActivity`)**: `Choose your focus` | `You can change this later in settings` | `Client Mode Everything you would expect from a git clie` | `Sync Mode Automated file syncing in the background Auto` | `BACK` | `NEXT`
- **Step 5 (`com.viscouspot.gitsync/MainActivity`)**: `Browse & Edit` | `Built-in tools for your files` | `File Explorer` | `View hidden files` | `View git log` | `Untrack and ignore files` | `Code Editor` | `Syntax highlighting` | `Auto-saving` | `Experimental feature`
- **Step 6 (`com.viscouspot.gitsync/MainActivity`)**: `Premium` | `ADD MORE Manage Multiple Repos One app. All your reposi` | `Unlimited containers` | `Independent auth per repo` | `Auto-add submodules` | `BUILT BY ONE DEVELOPER` | `GitSync is an independent project, not a company. Buyin` | `PURCHASE NOW — $20.00` | `RESTORE PURCHASE`
- **Step 7 (`com.viscouspot.gitsync/MainActivity`)**: `Premium` | `LARGE FILES Git LFS Full support for Git Large File Sto` | `Exclusive Features: Store Version Only!` | `Full Git LFS support` | `Track large binary files` | `Automatic LFS pull/push` | `BUILT BY ONE DEVELOPER` | `GitSync is an independent project, not a company. Buyin` | `PURCHASE NOW — $20.00` | `RESTORE PURCHASE`
- **Step 8 (`com.viscouspot.gitsync/MainActivity`)**: `Premium` | `FILTERS Git Filters Support for git filters including g` | `Exclusive Features: Store Version Only!` | `git-lfs filter` | `git-crypt filter` | `More filters coming soon` | `BUILT BY ONE DEVELOPER` | `GitSync is an independent project, not a company. Buyin` | `PURCHASE NOW — $20.00` | `RESTORE PURCHASE`

## 中文逐页引导链路解读

> **全链路总结**：应用从首次启动进入 GitSync 引导页，跳过用户来源调查、选择同步模式并浏览文件编辑功能，随后进入付费页连续滑动查看多仓库、Git LFS、Git Filters 等高级卖点，并以 20 美元购买按钮促转化；全程属正常引导与付费墙，未出现权限索取、通知横幅或遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 中文核心意译（Step 1 首屏）：Effortless File Syncing / Works in the background, your work always in focus -> 轻松文件同步/后台运行，让你始终专注工作
- 英文 -> 中文核心意译（Step 2 来源调查）：Help us understand where our users come from -> 帮助我们了解用户来源，可多选
- 英文 -> 中文核心意译（Step 6-8 付费页）：BUILT BY ONE DEVELOPER, Buying Premium pays for the time that goes into it -> 独立开发者项目，购买高级版以支持开发投入
- 英文 -> 中文核心意译（Step 6-8 付费页）：PURCHASE NOW — $20.00 -> 立即购买，20 美元
- 英文 -> 中文核心意译（Step 7-8 付费页）：Exclusive Features: Store Version Only! -> 独家功能：仅商店版本提供

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 首次启动引导页，宣传后台轻松同步、工作不受打扰；点击 LET'S GO 进入下一步，无通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 用户来源调查页，列出 Reddit、YouTube、GitHub 等渠道；点击 SKIP 跳过，未提交来源，无权限请求。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 选择使用模式页，对比客户端模式与同步模式；点选同步模式，准备启用自动后台同步，选项高亮。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 同一模式选择页，同步模式已蓝色选中；点击 NEXT 继续引导，进入文件浏览与编辑功能介绍。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 文件浏览与编辑功能页，展示文件浏览器、代码编辑器等；点击 PREMIUM FEATURES 进入付费介绍。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 高级版多仓库页，强调一个应用管理全部仓库；无前进按钮，左滑轮播，页面含 20 美元购买与恢复购买。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 高级版 Git LFS 页，宣传大文件存储与自动拉取推送；标注仅商店版独家，左滑继续，仍见购买按钮。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 高级版 Git Filters 页，列出 git-lfs、git-crypt 等过滤器；下滑查看，末尾仍是 20 美元购买与恢复购买。 | `step_08_action.png` |
