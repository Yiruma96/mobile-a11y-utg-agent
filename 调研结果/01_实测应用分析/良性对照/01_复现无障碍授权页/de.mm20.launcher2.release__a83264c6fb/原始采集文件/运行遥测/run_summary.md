# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:41:13
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`de.mm20.launcher2.release`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 5 步，UTG 唯一节点 `7` 个，有向边 `9` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 5 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_05_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`de.mm20.launcher2.release/de.mm20.launcher2.ui.settings.SettingsActivity` | hooks=`[]` | overlays=`0` | texts=`Swipe down / Search / app drawer / Swipe left / Do nothing / Swipe right`
- **Back 后 +5.5s**：`de.mm20.launcher2.release/de.mm20.launcher2.ui.settings.SettingsActivity` | hooks=`[]` | overlays=`0` | texts=`Swipe down / Search / app drawer / Swipe left / Do nothing / Swipe right`
- **Back 后 +10.5s**：`de.mm20.launcher2.release/de.mm20.launcher2.ui.settings.SettingsActivity` | hooks=`[]` | overlays=`0` | texts=`Swipe down / Search / app drawer / Swipe left / Do nothing / Swipe right`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `de.mm20.launcher2.release` / `LauncherActivity` | `-` | 8 | 35 / 否 | `click` → [8] View desc="More actions" center=(992,171) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `de.mm20.launcher2.release` / `LauncherActivity` | `-` | 6 | 21 / 否 | `click` → [4] TextView text="Settings" center=(904,441) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `de.mm20.launcher2.release` / `SettingsActivity` | `-` | 31 | 391 / 否 | `click` → [14] View (click) center=(540,1256) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `de.mm20.launcher2.release` / `SettingsActivity` | `-` | 28 | 218 / 否 | `click` → [16] TextView text="Grant" center=(851,1438) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 208 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_05_layout.xml` + `step_05_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`de.mm20.launcher2.release/LauncherActivity`)**: `04 41` | `100%` | `Charging` | `Search` | `More actions`
- **Step 2 (`de.mm20.launcher2.release/LauncherActivity`)**: `Wallpaper` | `Settings` | `Help`
- **Step 3 (`de.mm20.launcher2.release/SettingsActivity`)**: `Appearance` | `Customize the look and feel` | `Home screen` | `Clock, search bar, wallpaper, system bars` | `Grid and icons` | `Grid size, icons, badges` | `Search` | `Search, tags, excluded results` | `Gestures` | `Gestures and gesture actions`
- **Step 4 (`de.mm20.launcher2.release/SettingsActivity`)**: `Swipe down` | `Search / app drawer` | `Swipe left` | `Do nothing` | `Swipe right` | `Swipe up` | `Widgets` | `This action requires the launcher's accessibility servi` | `Grant` | `Double tap`
- **Step 5 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Kvaesitso` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用从启动器主屏“更多操作→设置→手势”进入，以“此操作需启用无障碍服务”横幅和“授予”按钮诱导跳转系统无障碍授权；在系统警告页拒绝后仍返回并停留在同一手势设置诱导页，形成 TRAPPED_ON_LURE_SCREEN。整体为极简桌面功能引导，但授权链路依赖无障碍高危权限，拒权后无法脱离诱导页。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文“This action requires the launcher's accessibility service to be enabled.” -> “此操作需要启用启动器的无障碍服务。”（手势设置页提示横幅）
- 英文“Grant” -> “授予”（手势设置页按钮，引导跳转无障碍授权）
- 英文“Use Kvaesitso” -> “使用 Kvaesitso”（无障碍服务详情页开关标题）
- 英文“No description provided.” -> “未提供说明。”（无障碍服务详情页说明）
- 英文“Allow Kvaesitso to have full control of your device?” -> “允许 Kvaesitso 完全控制你的设备？”（系统无障碍授权警告弹窗标题）
- 英文“Full control is appropriate for apps that help you with accessibility needs, but not for most apps.” -> “完全控制适用于帮助无障碍需求的 App，但不适合大多数 App。”（系统警告说明）
- 英文“View and control screen: It can read all content on the screen and display content over other apps.” -> “查看并控制屏幕：可读取屏幕全部内容并覆盖显示在其他 App 上。”（系统警告权限说明）
- 英文“View and perform actions: It can track your interactions with an app or a hardware sensor, and interact with apps on your behalf.” -> “查看并执行操作：可跟踪交互并代表你操作其他 App。”（系统警告权限说明）
- 英文“Allow / Deny” -> “允许 / 拒绝”（系统警告弹窗按钮，审核中应拒绝）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: LauncherActivity** | 启动器主屏：显示时间04:41、100%充电、搜索与“更多操作”；点击右上角“更多操作”展开菜单，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: LauncherActivity** | 展开菜单仅含“壁纸/设置/帮助”；点击“设置”进入配置页，意图打开手势与无障碍相关选项，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: SettingsActivity** | 启动器设置列表：外观、主屏、网格图标、搜索、手势、集成、插件；点击“手势”进入手势动作配置。 | `step_03_action.png` |
| 4 | **Step 4: SettingsActivity** | 手势设置页：列下滑/左滑/上滑等动作；提示“此操作需启用启动器无障碍服务”并有“授予”按钮，点击授予。 | `step_04_action.png` |
| 5 | **Step 5: [无障碍列表页]** | 跳转系统无障碍列表：Kvaesitso 显示“关闭”；含屏幕阅读器、显示项；自动终止并记录钩子探针，无通知/遮罩。 | `step_05_screen.png` |
| 6 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留系统无障碍设置页，文本为空，通知0、遮罩0，未见额外诱导弹窗。 | `step_05_probe_800ms_screen.png` |
| 7 | **跳后探针 +2.0s** | 跳转后2.0秒探针：页面仍为系统无障碍设置，文本为空，通知0、遮罩0，未出现延迟弹窗或覆盖层。 | `step_05_probe_2000ms_screen.png` |
| 8 | **服务详情页** | Kvaesitso 服务详情：有“使用 Kvaesitso”、快捷方式“关闭”、快捷设置；说明为“未提供说明”，为授权前置页。 | `step_05_service_detail_screen.png` |
| 9 | **系统警告弹窗(点Deny)** | 系统敏感权限警告：询问是否允许 Kvaesitso 完全控制设备，列明可查看/控制屏幕与代操作；提供“允许/拒绝”。 | `step_05_system_warning_screen.png` |
| 10 | **拒权返回 +2.0s** | 拒绝授权后2秒：返回启动器手势设置页，仍显示“授予”与无障碍服务提示，无法脱离该诱导页，状态 TRAPPED_ON_LURE_SCREEN。 | `step_05_refusal_2000ms_screen.png` |
| 11 | **拒权返回 +10.5s** | 拒绝授权后10.5秒：仍被困在手势设置页，“授予”提示未消失，无通知/遮罩，状态 TRAPPED_ON_LURE_SCREEN。 | `step_05_refusal_10500ms_screen.png` |
