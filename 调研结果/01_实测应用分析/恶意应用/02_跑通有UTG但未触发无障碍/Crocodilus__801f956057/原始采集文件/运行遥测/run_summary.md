# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:58:33
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`unrelated.hamburger`（静态标签：`malicious` / `Crocodilus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1500] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `click` → [19] FrameLayout desc="Search" id=search_container_all_ | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `type` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 29 / 否 | `system_button` → Enter | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.googlequicksearchbox` / `SearchNowActivity` | `-` | 22 | 201 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `unrelated.hamburger` / `yXfRlQHtIHgw` | `-` | 22 | 201 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `unrelated.hamburger` / `yXfRlQHtIHgw` | `-` | 6 | 257 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `IKO Lokata` | `Clear`
- **Step 6 (`com.google.android.googlequicksearchbox/SearchNowActivity`)**: `ALL` | `Mobile data is off` | `No data connection. Consider turning on mobile data or ` | `Turn on mobile data` | `Try again` | `FEEDBACK` | `Go to Discover` | `IKO Lokata` | `Voice Search` | `Discover`
- **Step 7 (`unrelated.hamburger/yXfRlQHtIHgw`)**: `ALL` | `Mobile data is off` | `No data connection. Consider turning on mobile data or ` | `Turn on mobile data` | `Try again` | `FEEDBACK` | `Go to Discover` | `IKO Lokata` | `Voice Search` | `Discover`
- **Step 8 (`unrelated.hamburger/yXfRlQHtIHgw`)**: `Erişilebilirlik İzni` | `Chrome Icon` | `Accessibility Permission Required` | `You need to grant accessibility permission for the app ` | `Enable Accessibility` | `Accessibility settings can be found under installed app`

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面启动器查找“IKO Lokata”，经 Google 搜索页无数据提示后静态跳转至 unrelated.hamburger 随机 Activity，最终弹出混合土耳其语/英语的无障碍权限诱导页；全程无通知横幅或遮罩，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “移动数据已关闭/无数据连接，建议开启移动数据或 Wi-Fi”（Step 6/7 Google 搜索页）
- 土耳其语 -> “无障碍权限”（Step 8 权限页）
- 英文 -> “需要无障碍权限”（Step 8 权限页）
- 英文 -> “需授予无障碍权限应用才能正常运行”（Step 8 权限页）
- 英文 -> “启用无障碍”（Step 8 权限页）
- 英文 -> “可在已安装应用或无障碍设置中找到该权限”（Step 8 权限页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器主页，显示 Apps list 与 Messages、Chrome 等图标；代理点击“Apps list”寻找目标应用，未跳转。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面主页，应用列表入口无响应；代理上滑屏幕尝试打开应用抽屉，界面未变化。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉网格显示 Calendar、Camera、Chrome 等图标；代理点击顶部 Search 搜索框，准备查找目标应用。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 启动器搜索页显示“Search apps, web, and more…”和 Voice Search；代理输入疑似应用名 IKO Lokata。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 搜索框已填入 IKO Lokata 并显示 Clear；代理按 Enter 执行启动器搜索，等待结果跳转。 | `step_05_action.png` |
| 6 | **Step 6: SearchNowActivity** | 跳转 Google 搜索页，显示 Mobile data is off/无数据连接及 Turn on mobile data、Try again；随后静态跳转。 | `step_06_screen.png` |
| 7 | **Step 7: yXfRlQHtIHgw** | 页面外观仍是 Google 搜索页与无数据提示，但包名已变为 unrelated.hamburger，静态跳转进入随机命名 Activity。 | `step_07_screen.png` |
| 8 | **Step 8: yXfRlQHtIHgw** | 弹出无障碍权限页，土耳其语 Erişilebilirlik İzni 混英文说明，要求 Enable Accessibility；未见取消项，未记录授权结果。 | `step_08_screen.png` |
