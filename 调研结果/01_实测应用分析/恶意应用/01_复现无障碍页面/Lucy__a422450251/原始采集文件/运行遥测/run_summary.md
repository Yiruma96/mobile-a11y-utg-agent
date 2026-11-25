# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:34:03
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`co1m.andr53oid.gohpat`（静态标签：`malicious` / `Lucy` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`co1m.andr53oid.gohpat/co1m.andr53oid.gohpat.Admin53Activity` | hooks=`[]` | overlays=`0` | texts=`Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on! / OK`
- **Back 后 +5.5s**：`co1m.andr53oid.gohpat/co1m.andr53oid.gohpat.Admin53Activity` | hooks=`[]` | overlays=`0` | texts=`Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on! / OK`
- **Back 后 +10.5s**：`co1m.andr53oid.gohpat/co1m.andr53oid.gohpat.Admin53Activity` | hooks=`[]` | overlays=`0` | texts=`Attention! / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on! / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `co1m.andr53oid.gohpat` / `Admin53Activity` | `-` | 3 | 149 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 7 | 124 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`co1m.andr53oid.gohpat/Admin53Activity`)**: `Attention!` | `To continue watching the video on your phone, you must ` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Streaming Video Optimization (SVO)                     `

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面抽屉进入，先由Admin53Activity以“启用SVO才能继续看视频”诱导点击OK，再跳转无障碍设置并展示SVO服务及“完全控制设备”授权警告；用户拒绝后仍反复重拉同一诱导弹窗，呈现典型无障碍滥用与拒权重诱链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English: Attention! To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select line in the menu and turn it on! -> “注意！要在手机上继续观看视频，必须启用流媒体视频优化（SVO），在菜单中选择线路并开启！”（Admin53Activity诱导弹窗）
- English: Use Streaming Video Optimization (SVO) -> “使用流媒体视频优化（SVO）”（无障碍服务详情开关）
- English: Allow Streaming Video Optimization (SVO) ... to have full control of your device? -> “允许流媒体视频优化（SVO）……完全控制您的设备？”（系统授权警告弹窗）
- English: Streaming Video Optimization (SVO) -> “流媒体视频优化（SVO）”（无障碍服务列表与详情中的伪装名称）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用抽屉页，显示“Apps list/应用列表”和常用图标；点击进入应用列表寻找目标入口，无通知横幅与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: Admin53Activity** | 恶意Admin53Activity弹出“Attention!”诱导框，意译需启用SVO才能继续看视频；点击OK跳系统设置，无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍设置页，“DOWNLOADED APPS”列出SVO服务；触发HOOK_A11Y_SETTINGS后自动终止，无通知横幅与遮罩。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停在无障碍设置页，UI文本为空、遮罩为0；未见通知横幅，等待观察无变化。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍为无障碍设置页且无可见文本，遮罩为0；未见通知横幅，页面保持静止。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 进入SVO服务详情子页，显示“Use Streaming Video Optimization”开关；仅检查详情/警告，遮罩0、无通知，为授权铺垫。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 弹出系统授权警告，询问是否允许SVO“完全控制设备”；仅检查未授权，遮罩0、无通知横幅，属高风险无障碍授权。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回后2秒，恶意应用重新弹出同一“Attention!”SVO诱导框；拒权未阻止重拉，无通知与遮罩。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回后10.5秒，Admin53Activity再次显示同一SVO诱导框并保留OK按钮；诱导弹窗反复重拉，无通知与遮罩。 | `step_03_refusal_10500ms_screen.png` |
