# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:57:24
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.resolvecommunity.awaydoomscrollin`（静态标签：`benign` / `系统效率与通用辅助` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `8` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.resolvecommunity.awaydoomscrollin` / `MainActivity` | `-` | 20 | 1050 / 否 | `swipe` → [540, 1900] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.resolvecommunity.awaydoomscrollin` / `MainActivity` | `-` | 12 | 1313 / 否 | `swipe` → [540, 2000] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.resolvecommunity.awaydoomscrollin` / `MainActivity` | `-` | 11 | 1199 / 否 | `click` → [11] TextView text="Start setup →" center=(830,1972) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.resolvecommunity.awaydoomscrollin` / `MainActivity` | `-` | 16 | 1044 / 否 | `swipe` → [540, 2000] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.resolvecommunity.awaydoomscrollin` / `MainActivity` | `-` | 17 | 1203 / 否 | `click` → [16] View (click) center=(892,2025) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.resolvecommunity.awaydoomscrollin` / `MainActivity` | `-` | 15 | 872 / 否 | `click` → [15] View (click) center=(892,2142) | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.resolvecommunity.awaydoomscrollin` / `MainActivity` | `-` | 27 | 610 / 否 | `swipe` → [540, 2000] | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.resolvecommunity.awaydoomscrollin` / `MainActivity` | `-` | 31 | 631 / 否 | `click` → [30] View (click) center=(892,1972) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.resolvecommunity.awaydoomscrollin/MainActivity`)**: `Step 1 / 5 · Welcome` | `Why AwayDoomscrollin'?` | `On-device protection for feeds and short videos` | `Why not just use a timer?` | `A timer limits how long you use an app. AwayDoomscrolli` | `Communication stays available` | `Messages, search and YouTube long videos remain availab` | `Any language` | `Works whatever language your apps use.` | `On-device`
- **Step 2 (`com.resolvecommunity.awaydoomscrollin/MainActivity`)**: `I'm one of you.` | `A letter from Resolve Community` | `Hi, I'm the independent developer behind Resolve Commun` | `During the COVID-19 pandemic, I started spending almost` | `What I noticed` | `I realized that short-content habits were taking more t` | `Why did I build this app under Resolve Community?` | `Even when I was busy with something else, I'd find myse` | `Why short-content feeds never end` | `• Feeds automatically load the next item. • Watch time `
- **Step 3 (`com.resolvecommunity.awaydoomscrollin/MainActivity`)**: `During the COVID-19 pandemic, I started spending almost` | `What I noticed` | `I realized that short-content habits were taking more t` | `Why did I build this app under Resolve Community?` | `Even when I was busy with something else, I'd find myse` | `Why short-content feeds never end` | `• Feeds automatically load the next item. • Watch time ` | `AwayDoomscrollin' was created to make room for study, w` | `Start setup →`
- **Step 4 (`com.resolvecommunity.awaydoomscrollin/MainActivity`)**: `Step 2 / 5 · How it works` | `?` | `How does protection work?` | `Clear boundaries for feeds and short videos` | `How it works` | `Instagram` | `Home and Explore are covered and the Reels tab is block` | `BALANCED` | `Profiles, profile posts, Stories and Highlights stay op` | `STRICT`
- **Step 5 (`com.resolvecommunity.awaydoomscrollin/MainActivity`)**: `STRICT` | `Profile posts are covered. Reels (including those share` | `TikTok` | `Opening and browsing TikTok is allowed. The first swipe` | `YouTube` | `Home is covered and the Shorts tab is blocked. Search r` | `BALANCED` | `Subscriptions stay open: they only show channels you ch` | `Subscriptions are covered as well. All Shorts are block` | `On-device protection`
- **Step 6 (`com.resolvecommunity.awaydoomscrollin/MainActivity`)**: `Step 3 / 5 · Scope and privacy` | `What it can and cannot do` | `Here's what protection covers and how your information ` | `WHAT PROTECTION DOES` | `All analysis and protection happen directly on your dev` | `Protection reads the structure of the screen, not its t` | `You can turn protection off at any time, in the app or ` | `Changes to Instagram, TikTok or YouTube can affect how ` | `WHAT IT NEVER DOES OR COLLECTS` | `Does not save on-screen text or send screen information`
- **Step 7 (`com.resolvecommunity.awaydoomscrollin/MainActivity`)**: `Step 4 / 5 · Apps` | `Apps and preferences` | `Choose the apps where protection will be active:` | `YouTube` | `BETA` | `Home feed and Shorts` | `Protection mode` | `Balanced` | `Strict` | `Subscriptions stay open; you can watch one Short you op`
- **Step 8 (`com.resolvecommunity.awaydoomscrollin/MainActivity`)**: `Apps and preferences` | `Choose the apps where protection will be active:` | `YouTube` | `BETA` | `Home feed and Shorts` | `Protection mode` | `Balanced` | `Strict` | `Subscriptions stay open; you can watch one Short you op` | `Instagram, not installed`

## 中文逐页引导链路解读

> **全链路总结**：应用启动后进入5步引导：欢迎与开发者自述、逐平台说明阻断规则、范围与隐私承诺、应用与模式选择，最后点击Next前往权限步骤；全程仅说明与选择，无通知横幅或遮罩，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 为什么选择AwayDoomscrollin'：声称在设备端保护信息流和短视频（Step 1 欢迎页）
- 英文 -> 为何不用计时器：声称不是限制使用时长，而是阻断信息流并保留有目的的使用（Step 1 欢迎页）
- 英文 -> 通信仍可用：消息、搜索和YouTube长视频保留（Step 1 欢迎页）
- 英文 -> 保护决策在设备本地完成（Step 1 欢迎页）
- 英文 -> 无广告、开源、任意语言可用（Step 1 欢迎页）
- 英文 -> 只读屏幕结构不读文字，因此跨语言生效（Step 3 范围与隐私页）
- 英文 -> 不保存屏幕文字、不发送屏幕信息，不收集消息/密码/照片/截图（Step 3 范围与隐私页）
- 英文 -> 使用数据共享可选且默认关闭，不展示广告或出售个人数据（Step 3 范围与隐私页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 欢迎页说明阻断信息流与短视频、通信保留、本地处理与开源；本步下滑，无通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 开发者自述信页，讲疫情期刷屏经历与创建动机，解释信息流无自然终点；本步下滑，无通知、无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 同一自述信下半页，出现“Start setup →”；本步点按进入设置，无通知横幅或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 第2/5步“如何运作”，分平台说明Instagram、TikTok、YouTube限制差异；本步下滑，无通知遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 承接运作说明，列YouTube限制与本地处理隐私声明；本步点“Next →”前进，无通知、无遮罩。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 第3/5步范围与隐私页，声称仅读屏幕结构、不存文字不传服务器、无广告；本步点Next，无通知遮罩。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 第4/5步应用与偏好，选择YouTube平衡/严格，Instagram未安装；本步下滑，无通知、无遮罩。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 承接应用选择页，显示TikTok未安装；本步点“Next →”前往权限步骤，无通知、无遮罩。 | `step_08_action.png` |
