# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:25:59
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`wcqrucdpzh.otstodvvsm.vrbnjqrsrr`（静态标签：`malicious` / `Lucy` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`wcqrucdpzh.otstodvvsm.vrbnjqrsrr/wcqrucdpzh.otstodvvsm.vrbnjqrsrr.rsyqdappvn` | hooks=`[]` | overlays=`0` | texts=`Attention / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select it in the menu and turn it on! / OK`
- **Back 后 +5.5s**：`wcqrucdpzh.otstodvvsm.vrbnjqrsrr/wcqrucdpzh.otstodvvsm.vrbnjqrsrr.rsyqdappvn` | hooks=`[]` | overlays=`0` | texts=`Attention / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select it in the menu and turn it on! / OK`
- **Back 后 +10.5s**：`wcqrucdpzh.otstodvvsm.vrbnjqrsrr/wcqrucdpzh.otstodvvsm.vrbnjqrsrr.rsyqdappvn` | hooks=`[]` | overlays=`0` | texts=`Attention / To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select it in the menu and turn it on! / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 9 | 74 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `wcqrucdpzh.otstodvvsm.vrbnjqrsrr` / `rsyqdappvn` | `-` | 3 | 146 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,129 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 7 | 124 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`wcqrucdpzh.otstodvvsm.vrbnjqrsrr/rsyqdappvn`)**: `Attention` | `To continue watching the video on your phone, you must ` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Streaming Video Optimization (SVO)                     `

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面应用抽屉进入伪装视频播放器，弹窗以“继续看视频须开启SVO”为由诱导跳转无障碍设置并申请完全控制设备的无障碍权限；用户拒绝后应用反复重弹同一诱导对话框（RELAUNCHED_LURE_DIALOG），呈现Lucy家族无障碍滥用与循环施压特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Attention -> 注意（step_02诱导弹窗、refusal_2.0s/refusal_10.5s重弹页）
- To continue watching the video on your phone, you must enable Streaming Video Optimization (SVO), select it in the menu and turn it on! -> 要在手机上继续观看视频，你必须启用“流媒体视频优化(SVO)”，在菜单中选中并开启它！（step_02、refusal_2.0s、refusal_10.5s）
- Streaming Video Optimization (SVO) -> 流媒体视频优化(SVO)（step_03无障碍列表、detail_1服务详情、detail_2系统警告；伪装服务名）
- Use Streaming Video Optimization (SVO) -> 使用流媒体视频优化(SVO)（detail_1服务详情页开关项）
- Allow Streaming Video Optimization (SVO) ... to have full control of your device? -> 是否允许流媒体视频优化(SVO)完全控制你的设备？（detail_2系统警告弹窗）
- OK -> 确定（step_02诱导页按钮）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面/应用抽屉入口页，显示“应用列表”、日期天气及Messages、Chrome等图标；点击“Apps list”进入应用抽屉以寻找视频播放器。 | `step_01_action.png` |
| 2 | **Step 2: rsyqdappvn** | 恶意应用弹出“Attention”诱导页，谎称须启用SVO才能继续看视频；点击“OK”跳转无障碍设置，为申请无障碍权限铺路。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍设置页，列出“已下载应用”中的SVO服务；探针捕获无障碍设置HOOK后自动终止，说明诱导点击指向无障碍授权入口。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留在无障碍设置页，界面无新增文本、无悬浮遮罩；等待期间未出现额外弹窗，准备继续观察授权状态。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针，页面仍为无障碍设置，无新文本和悬浮遮罩；说明普通弹窗未覆盖系统页，攻击链依赖用户手动开启服务。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | SVO服务详情页，显示“使用流媒体视频优化(SVO)”开关项；检查详情以确认该无障碍服务伪装为视频优化、实为高权限控制工具。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高危警告弹窗，询问是否允许SVO“完全控制设备”；标题标注点Deny，说明审核侧拒绝该无障碍授权并记录警告内容。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒绝授权返回后2.0秒，恶意应用重新弹出同一“Attention/SVO”诱导对话框；呈现拒权即循环重试的RELAUNCHED_LURE_DIALOG行为。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回后10.5秒，仍反复展示相同SVO诱导页，没有取消或跳过入口；确认应用通过循环弹窗持续施压用户开启无障碍。 | `step_03_refusal_10500ms_screen.png` |
