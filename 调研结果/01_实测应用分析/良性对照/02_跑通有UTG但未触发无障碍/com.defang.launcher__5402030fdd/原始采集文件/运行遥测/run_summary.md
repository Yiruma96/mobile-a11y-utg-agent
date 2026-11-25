# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:45:41
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.defang.launcher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.defang.launcher` / `OnboardingActivity` | `-` | 5 | 684 / 否 | `click` → [2] View (click) center=(912,281) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.defang.launcher` / `OnboardingActivity` | `-` | 4 | 490 / 否 | `click` → [3] View (click) center=(540,1950) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.defang.launcher` / `SettingsActivity` | `-` | 30 | 732 / 否 | `click` → [8] View (click) center=(540,760) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.defang.launcher` / `SettingsActivity` | `-` | 14 | 342 / 否 | `click` → [13] View desc="Back" center=(77,171) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.defang.launcher` / `SettingsActivity` | `-` | 30 | 732 / 否 | `swipe` → [540, 1800] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.defang.launcher` / `SettingsActivity` | `-` | 24 | 720 / 否 | `swipe` → [540, 2000] | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.defang.launcher` / `SettingsActivity` | `-` | 27 | 540 / 否 | `swipe` → [540, 600] | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.defang.launcher` / `SettingsActivity` | `-` | 24 | 834 / 否 | `swipe` → [540, 2000] | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.defang.launcher/OnboardingActivity`)**: `Skip` | `This is a speed bump. Not a wall.` | `Some apps will block your phone completely. Some will g`
- **Step 2 (`com.defang.launcher/OnboardingActivity`)**: `Let's set it up. Two minutes.` | `Pick which apps get the speed bump. Set how long you wa` | `Continue to setup →`
- **Step 3 (`com.defang.launcher/SettingsActivity`)**: `Default timings` | `Gate delay, max session length, and cool-down` | `App setup` | `These apps are watched by default. Adjust if needed.` | `Watched websites` | `Gate specific sites in your browser` | `Work profile apps` | `Show and open apps from your Android work profile` | `App drawer letter index` | `Size and position of the side letter index`
- **Step 4 (`com.defang.launcher/SettingsActivity`)**: `Sites you add are gated when opened in a browser. Adult` | `Built-in adult site list` | `Gates well-known adult sites in any browser with a 1-mi` | `example.com or example.com/path` | `Adult (1-min leash)` | `Add` | `No sites added yet.` | `Back` | `Watched websites`
- **Step 5 (`com.defang.launcher/SettingsActivity`)**: `Default timings` | `Gate delay, max session length, and cool-down` | `App setup` | `These apps are watched by default. Adjust if needed.` | `Watched websites` | `Gate specific sites in your browser` | `Work profile apps` | `Show and open apps from your Android work profile` | `App drawer letter index` | `Size and position of the side letter index`
- **Step 6 (`com.defang.launcher/SettingsActivity`)**: `Register code` | `No code registered yet` | `Why?` | `Math problem unlock` | `Solve an arithmetic problem to open watched apps, in pl` | `Personal lines` | `Sometimes show your own numbers instead of a tidbit, bl` | `Adaptive threshold` | `Raises the wait automatically when you keep reopening a` | `Home screen`
- **Step 7 (`com.defang.launcher/SettingsActivity`)**: `Clock and tidbit` | `Today's usage on home screen` | `Small bars under the clock — only shown on days with wa` | `Folders in app list` | `Group apps into folders from the long-press menu. Turni` | `Swipe left on home opens` | `Off` | `Swipe right on home opens` | `Your own tasks` | `Tasks you add are suggested on the end card alongside t`
- **Step 8 (`com.defang.launcher/SettingsActivity`)**: `Require a code scan to open watched apps, in place of t` | `Register code` | `No code registered yet` | `Why?` | `Math problem unlock` | `Solve an arithmetic problem to open watched apps, in pl` | `Personal lines` | `Sometimes show your own numbers instead of a tidbit, bl` | `Adaptive threshold` | `Raises the wait automatically when you keep reopening a`

## 中文逐页引导链路解读

> **全链路总结**：该应用为极简桌面+使用摩擦类工具（Defang），链路为：英文欢迎页强调『只是减速带不是墙』→设置引导页→设置主页→受监控网站子页→反复滚动浏览二维码/数学题解锁、自适应阈值等选项。全程无权限弹窗、无通知横幅、无悬浮遮罩，未进入授权或拒权判定（not_tested），话术以自我克制与反沉迷说明为主，无强制诱导。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 『这是减速带，不是墙』，强调不封锁手机、仍可打开 Instagram、仍可覆盖计时（引导首屏）
- 英文 -> 以 Instagram 自带时限的『再给 15 分钟』按钮为例，称无摩擦的出口会训练用户无视限制（引导首屏）
- 英文 -> 『本应用在反射动作前放一个减速带，让无意识打开变成有意识的打开』（引导首屏）
- 英文 -> 『两分钟就能设置好』，可自选受管应用、使用时长与通知时段，之后随时可改（引导第二屏）
- 英文 -> 『默认值只是合理起点，不是推荐』，且系统勿扰/就寝时段会自动加大摩擦（引导第二屏）
- 英文 -> 成人站点默认『1 分钟牵绳』，其他站点使用标准会话与冷却时间（受监控网站页）
- 英文 -> 可打印二维码放在够不到的地方，扫码才能打开受管应用（设置页二维码解锁）
- 英文 -> 个性化文案示例：『这就是你每天花 43 分钟做的事？』，仅在本机计算（设置页）
- 英文 -> 使用报告是『证据，而非罪责』（设置页使用报告）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: OnboardingActivity** | 引导首屏：英文长文称本应用只是『减速带不是墙』，可跳过、可覆盖计时，不封锁任何应用；本步点击右上角 Skip 跳过引导，页面无遮罩无通知。 | `step_01_action.png` |
| 2 | **Step 2: OnboardingActivity** | 引导第二屏：英文称『两分钟即可设置完』，可选受管应用、时长与通知时段且随时可改；本步点击底部『Continue to setup →』进入设置流程。 | `step_02_action.png` |
| 3 | **Step 3: SettingsActivity** | 设置主页：默认时长、应用设置、受监控网站、工作资料应用、字母索引、二维码解锁等卡片；无权限弹窗与遮罩，本步点击『Watched websites』。 | `step_03_action.png` |
| 4 | **Step 4: SettingsActivity** | 受监控网站子页：英文称成人站点默认 1 分钟限时，可输入域名后点 Add 添加，列表显示尚未添加站点；本步点击左上返回键回设置主页。 | `step_04_action.png` |
| 5 | **Step 5: SettingsActivity** | 返回设置主页的同一列表页，卡片与上一步一致；本步向下滑动寻找无障碍权限卡片，页面无通知横幅、无悬浮遮罩，未触发任何授权弹窗。 | `step_05_action.png` |
| 6 | **Step 6: SettingsActivity** | 设置列表下半部：二维码注册码、数学题解锁、个性化文案、自适应阈值、桌面时钟等卡片，英文称自适应默认关闭可随时关；本步继续下滑。 | `step_06_action.png` |
| 7 | **Step 7: SettingsActivity** | 设置更下方：文件夹、桌面左右滑手势、自定义任务、使用报告等项，英文称使用报告为『证据而非罪责』；本步上滑回滚，仍未出现权限卡片。 | `step_07_action.png` |
| 8 | **Step 8: SettingsActivity** | 回滚后重现二维码/数学题解锁与自适应阈值段落，英文说明可扫远处印码或做题替代滑动解锁；本步再下滑，全程无权限请求与遮罩。 | `step_08_action.png` |
