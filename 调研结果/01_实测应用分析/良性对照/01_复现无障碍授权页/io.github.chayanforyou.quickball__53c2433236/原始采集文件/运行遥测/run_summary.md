# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:38:19
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`io.github.chayanforyou.quickball`（静态标签：`benign` / `按键映射与手势导航` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`io.github.chayanforyou.quickball/io.github.chayanforyou.quickball.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Permissions / Quick Ball needs just these two to run. Anything else is asked for only when you turn on a feature that needs it. / Accessibility / Powers the floating button and lets Quick Ball perform navigation actions like Home, Back and Recents. It never reads screen content. / Grant`
- **Back 后 +5.5s**：`io.github.chayanforyou.quickball/io.github.chayanforyou.quickball.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Permissions / Quick Ball needs just these two to run. Anything else is asked for only when you turn on a feature that needs it. / Accessibility / Powers the floating button and lets Quick Ball perform navigation actions like Home, Back and Recents. It never reads screen content. / Grant`
- **Back 后 +10.5s**：`io.github.chayanforyou.quickball/io.github.chayanforyou.quickball.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Permissions / Quick Ball needs just these two to run. Anything else is asked for only when you turn on a feature that needs it. / Accessibility / Powers the floating button and lets Quick Ball perform navigation actions like Home, Back and Recents. It never reads screen content. / Grant`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `io.github.chayanforyou.quickball` / `MainActivity` | `-` | 8 | 289 / 否 | `click` → [7] View (click) center=(540,2039) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `io.github.chayanforyou.quickball` / `MainActivity` | `-` | 15 | 508 / 否 | `click` → [5] View (click) center=(856,840) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 209 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`io.github.chayanforyou.quickball/MainActivity`)**: `Meet Quick Ball` | `A floating button that puts one-handed navigation and q` | `•` | `Home, Back, Recents and more from a fan menu you design` | `Swipe gestures, media controls and one-tap shortcuts` | `Get started`
- **Step 2 (`io.github.chayanforyou.quickball/MainActivity`)**: `Permissions` | `Quick Ball needs just these two to run. Anything else i` | `Accessibility` | `Powers the floating button and lets Quick Ball perform ` | `Grant` | `Modify System Settings` | `Lets Quick Ball adjust system settings like screen brig` | `Quick Ball needs Accessibility and System Settings perm` | `Back` | `Start using Quick Ball`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Quick Ball` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从引导页宣传“不读屏、数据不出设备”，进入权限页要求无障碍与修改系统设置；点击Grant跳转系统无障碍列表与服务详情，触发系统“完全控制”警告，拒权后仍被锁回同一权限说明页。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 主打悬浮球单手导航与快捷操作，强调不读取屏幕内容、数据不出设备，弱化后续无障碍授权敏感性（Step 1 引导页）
- 英文 -> 声称“仅需这两项权限”，其他等开启功能时再询问，降低用户对权限组合的警惕（Step 2/拒权页）
- 英文 -> 将无障碍权限包装为悬浮球及Home/Back/Recents导航所需，并重申不读屏（Step 2/拒权页）
- 英文 -> 将修改系统设置描述为悬浮菜单调亮度/音量，弱化系统级设置权限范围（Step 2/拒权页）
- 英文 -> 系统警告明确提示可查看/控制屏幕、跟踪交互并代操作应用，与“不读屏”话术形成反差（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 入口引导页：标题“认识 Quick Ball”，宣称悬浮球提供单手导航与快捷操作、不读屏且数据不出设备；本步点击底部“Get started”进入授权向导。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 权限说明页：称仅需无障碍与修改系统设置两项权限，无障碍用于悬浮球及Home/Back/Recents且不读屏；本步点击无障碍旁“Grant”跳系统设置。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表页：显示“Quick Ball”状态为“Off”，位于已下载应用区；采集到无障碍设置钩子与探针后自动终止，未执行开启。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在系统无障碍设置页，页面文本为空、无通知横幅、遮罩数为0，未观察到额外弹窗或诱导覆盖。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：同一系统无障碍设置页保持静止，无新增文本、通知或遮罩，说明跳转后未立即出现二次诱导界面。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 服务详情页：标题“Quick Ball”，含“Use Quick Ball”开关、快捷方式“Off”及悬浮球服务说明；本步仅检查详情与警告，未开启服务。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告弹窗：问是否允许Quick Ball完全控制设备，列明可查看/控制屏幕与代操作应用，并提供“Allow”“Deny”；本步检查后未确认。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回2秒：回到应用权限说明页，仍要求无障碍与修改系统设置，无授权成功提示；页面成为停留陷阱，用户被锁在授权说明页。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回10.5秒：界面仍停在权限说明页，未跳转也未放行；“Grant”与“Start using Quick Ball”继续施压，确认拒权后被锁在诱导授权页。 | `step_03_refusal_10500ms_screen.png` |
