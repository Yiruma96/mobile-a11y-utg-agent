# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:20:04
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.focus.launcher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.focus.launcher/com.focus.launcher.SettingsActivity` | hooks=`[]` | overlays=`0` | texts=`← / Setup / Three switches make Focus work. Tap one to open the right system screen, flip it, and come back. / REQUIRED / 1 · Default launcher`
- **Back 后 +5.5s**：`com.focus.launcher/com.focus.launcher.SettingsActivity` | hooks=`[]` | overlays=`0` | texts=`← / Setup / Three switches make Focus work. Tap one to open the right system screen, flip it, and come back. / REQUIRED / 1 · Default launcher`
- **Back 后 +10.5s**：`com.focus.launcher/com.focus.launcher.SettingsActivity` | hooks=`[]` | overlays=`0` | texts=`← / Setup / Three switches make Focus work. Tap one to open the right system screen, flip it, and come back. / REQUIRED / 1 · Default launcher`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.focus.launcher` / `SettingsActivity` | `-` | 12 | 229 / 否 | `click` → [11] View (click) center=(540,1596) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.focus.launcher` / `SettingsActivity` | `-` | 27 | 843 / 否 | `click` → [17] TextView text="Turn on" center=(944,1197) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 31 | 273 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.focus.launcher/SettingsActivity`)**: `Focus` | `Reclaim your time. Spend it touching some grass.` | `No icons. No colour. No feed. Tips on the home screen s` | `Swipe right opens. Which app?` | `Swipe right opens` | `Any app, or the web search.` | `Web search` | `Start` | `Set up Focus first`
- **Step 2 (`com.focus.launcher/SettingsActivity`)**: `←` | `Setup` | `Three switches make Focus work. Tap one to open the rig` | `REQUIRED` | `1 · Default launcher` | `Makes Focus the screen you land on when you press Home.` | `Set` | `2 · Usage access` | `Lets Focus measure screen time: the day bar, app timers` | `Allow`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Focus app timers` | `Off / Enforces the daily app time limits you set in Foc` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：从Focus入口页点“Set up Focus first”进入三步强制设置，诱导开启默认桌面、Usage access及无障碍计时服务；在系统无障碍详情与“完全控制”警告页拒权后，仍被滞留在Setup必填页（TRAPPED_ON_LURE_SCREEN）。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Reclaim your time. Spend it touching some grass. -> 重拾时间、去接触真实生活（入口设置页，用生活化口号弱化权限请求）
- No icons. No colour. No feed. -> 无图标、无色彩、无信息流（入口页，包装极简卖点）
- Tips on the home screen show you around. -> 主屏提示会带你熟悉（入口页，引导继续设置）
- Three switches make Focus work. Tap one to open the right system screen, flip it, and come back. -> 三个开关才能让Focus工作，逐个去系统页打开再返回（Setup页，将关键权限包装成必要步骤）
- An accessibility service... It cannot read your screen. -> 无障碍服务只识别前台应用、不能读屏（Setup页，弱化无障碍高权限风险）
- Switch greyed out, or “restricted setting”? Open App info → ⋮ → Allow restricted settings, then try again. -> 若开关灰掉或受限，去应用信息右上角允许受限设置后重试（Setup页，指导绕过限制）
- Use Focus app timers... only receives the name of the app... cannot read... nothing ever leaves your device. -> 只接收应用名、不读屏、数据不出设备（服务详情页，合规承诺式安抚）
- Allow Focus app timers to have full control of your device? -> 允许Focus计时器完全控制设备？（系统警告弹窗，真实高风险提示）
- View and control screen / View and perform actions -> 可查看并控制屏幕／可查看并代你操作（系统警告弹窗，说明无障碍权限范围）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: SettingsActivity** | 入口设置/宣传页：显示Focus极简口号与滑动说明，点“Set up Focus first”开始设置向导。 | `step_01_action.png` |
| 2 | **Step 2: SettingsActivity** | Setup必填页：三项开关分别要求默认桌面、Usage access和无障碍计时服务；本步点“Turn on”拉起系统无障碍页。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表：DOWNLOADED APPS下“Focus app timers”为Off；探针触发HOOK_A11Y_SETTINGS后自动终止，无遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在系统无障碍设置页，界面文本为空，无通知横幅、无遮罩。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍在系统无障碍设置页，界面无文本、无通知、无遮罩，等待后未发生跳转。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 无障碍服务详情：展示“Use Focus app timers”开关与说明，承诺只识别前台应用名、不读屏且数据不出设备。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高风险警告：询问是否允许Focus计时器“完全控制设备”，列出可查看/控制屏幕与代操作，含Allow/Deny。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒：回Setup必填页，仍见默认桌面与Usage access两项，未离开引导页，状态TRAPPED_ON_LURE_SCREEN。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒：Setup页保持不变，仍要求完成必填开关，持续滞留于诱导页（TRAPPED_ON_LURE_SCREEN）。 | `step_03_refusal_10500ms_screen.png` |
