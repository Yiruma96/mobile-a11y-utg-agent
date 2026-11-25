# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:22:58
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`gcoojdprtw.tsqrstjtdi.crwrnqoqur`（静态标签：`malicious` / `Lucy` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`gcoojdprtw.tsqrstjtdi.crwrnqoqur/gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq` | hooks=`[]` | overlays=`0` | texts=`Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. / OK`
- **Back 后 +5.5s**：`gcoojdprtw.tsqrstjtdi.crwrnqoqur/gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq` | hooks=`[]` | overlays=`0` | texts=`Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. / OK`
- **Back 后 +10.5s**：`gcoojdprtw.tsqrstjtdi.crwrnqoqur/gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq` | hooks=`[]` | overlays=`0` | texts=`Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `gcoojdprtw.tsqrstjtdi.crwrnqoqur` / `xqbbbwdsrq` | `-` | 3 | 155 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,132 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 7 | 112 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`gcoojdprtw.tsqrstjtdi.crwrnqoqur/xqbbbwdsrq`)**: `Внимание` | `Для того что бы продолжить просмотр видео файла, нужно ` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Android Video Optimization                             `

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面启动后弹出俄语“视频优化”诱导框，点击 OK 跳转系统无障碍设置，把自身伪装成 Android Video Optimization 索取完全控制权限；拒绝后仍反复重弹同一诱导框。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 俄语「Внимание」 -> 中文意译“注意”（step_02、refusal_2.0s、refusal_10.5s 诱导弹窗标题）
- 俄语「Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее.」 -> 中文意译“为继续观看视频文件，需启用 Android Video Optimization（视频流优化），请开启。”（step_02、refusal 弹窗正文）
- 俄语「OK」 -> 中文意译“确定”（step_02 诱导弹窗按钮）
- 英语「Use Android Video Optimization」 -> 中文意译“使用 Android Video Optimization”（detail_1 伪装服务详情页）
- 英语「Allow Android Video Optimization ... to have full control of your device?」 -> 中文意译“允许 Android Video Optimization 完全控制您的设备？”（detail_2 系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用列表页，见 Messages、Chrome、Search；点击 Apps list 打开抽屉寻找伪装入口，无通知横幅/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: xqbbbwdsrq** | 恶意应用俄语诱导弹窗：标题“注意”，正文称继续看视频需开启 Android Video Optimization，点 OK；无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍设置页，DOWNLOADED APPS 下出现伪装服务 Android Video Optimization；命中无障碍钩子探针后自动终止，无通知/遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针：仍停留在系统无障碍设置页，界面文本为空、遮罩数为0，无通知横幅，等待未见变化。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针：仍为系统无障碍设置页，无界面文本、无遮罩与通知横幅，等待期间无新增弹窗。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 伪装服务详情页，标题 Android Video Optimization，显示“Use Android Video Optimization”开关；仅检查未授权，无通知/遮罩。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告弹窗：是否允许 Android Video Optimization 完全控制设备；本步检查并准备点 Deny，遮罩0、无通知横幅。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒绝授权返回后2.0秒，恶意应用再次弹出同一俄语“注意”视频优化诱导框，要求点 OK；无通知/遮罩，拒权后重弹。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回后10.5秒仍反复显示同一俄语诱导框，称需开启视频优化才能看视频；无通知/遮罩，体现拒权后持续重弹。 | `step_03_refusal_10500ms_screen.png` |
