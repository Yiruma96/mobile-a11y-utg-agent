# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:52:24
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`uuctvbgtlb.nkoqrtdctt.unootbawgh`（静态标签：`malicious` / `Lucy` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`uuctvbgtlb.nkoqrtdctt.unootbawgh/uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw` | hooks=`[]` | overlays=`0` | texts=`Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on! / OK`
- **Back 后 +5.5s**：`uuctvbgtlb.nkoqrtdctt.unootbawgh/uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw` | hooks=`[]` | overlays=`0` | texts=`Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on! / OK`
- **Back 后 +10.5s**：`uuctvbgtlb.nkoqrtdctt.unootbawgh/uuctvbgtlb.nkoqrtdctt.unootbawgh.nzpdotxvtw` | hooks=`[]` | overlays=`0` | texts=`Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on! / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `uuctvbgtlb.nkoqrtdctt.unootbawgh` / `nzpdotxvtw` | `-` | 3 | 149 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 7 | 124 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`uuctvbgtlb.nkoqrtdctt.unootbawgh/nzpdotxvtw`)**: `Attention!` | `To continue watching the video on your phone, you must ` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Streaming Video Optimization (SVO)                     `

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面启动后弹出“Attention!”谎称需开启 Streaming Video Optimization(SVO) 才能继续看视频，点击 OK 跳转无障碍设置；用户拒绝授权后返回，应用反复重弹同一诱导弹窗，形成拒权再诱导循环。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “注意！要在手机上继续观看视频，您必须启用流媒体视频优化（SVO），在菜单中选择该行并打开它！”（step_02 / refusal_2.0s / refusal_10.5s 诱导弹窗）
- 英语 -> “使用流媒体视频优化（SVO）”（服务详情页开关说明，伪装无障碍服务名称）
- 英语 -> “允许流媒体视频优化（SVO）完全控制您的设备吗？”（系统警告弹窗，披露高权限风险）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用列表页；可见 Messages、Chrome、Search 等图标，无诱导文案；点击“Apps list”进入抽屉以寻找并启动目标应用。 | `step_01_action.png` |
| 2 | **Step 2: nzpdotxvtw** | 应用首屏弹“Attention!”：英语称须开启流媒体视频优化(SVO)才能继续看视频；点击 OK 后应跳转无障碍设置。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍设置页，下载应用列表出现“Streaming Video Optimization (SVO)”条目；探针捕获设置钩子后自动终止，未继续点击。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍停留在无障碍设置页，无可见文本、无通知横幅、遮罩为 0；仅等待观察，无交互动作。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：页面仍为无障碍设置页，无文本与通知，遮罩为 0；未发生额外弹窗或自动点击。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 进入 SVO 服务详情页，显示“Use Streaming Video Optimization (SVO)”开关；以优化名义伪装无障碍服务，本步仅检查详情/警告未授权。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高权限警告弹窗，英语询问是否允许 SVO 完全控制设备；遮罩为 0，本步检查警告并准备点 Deny 拒绝。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒绝授权返回应用 2 秒后，同一“Attention!”诱导弹窗被重新拉起；仍要求开启 SVO 才能看视频，形成拒权循环。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回 10.5 秒后仍反复重弹相同诱导弹窗，文案与 OK 按钮不变；无通知/遮罩，显示强粘性再诱导。 | `step_03_refusal_10500ms_screen.png` |
