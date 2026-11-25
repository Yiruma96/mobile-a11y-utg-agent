# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:04:02
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

- **Back 后 +2.0s**：`co1m.andr53oid.gohpat/co1m.andr53oid.gohpat.Admin53Activity` | hooks=`[]` | overlays=`0` | texts=`Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. / OK`
- **Back 后 +5.5s**：`co1m.andr53oid.gohpat/co1m.andr53oid.gohpat.Admin53Activity` | hooks=`[]` | overlays=`0` | texts=`Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. / OK`
- **Back 后 +10.5s**：`co1m.andr53oid.gohpat/co1m.andr53oid.gohpat.Admin53Activity` | hooks=`[]` | overlays=`0` | texts=`Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. / OK`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `co1m.andr53oid.gohpat` / `Admin53Activity` | `-` | 3 | 155 / 否 | `click` → [3] Button text="OK" id=button1 (click) center=(887,132 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 7 | 112 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`co1m.andr53oid.gohpat/Admin53Activity`)**: `Внимание` | `Для того что бы продолжить просмотр видео файла, нужно ` | `OK`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Android Video Optimization                             `

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面应用抽屉启动后，以俄语弹窗谎称需开启“Android Video Optimization”才能继续看视频，点击 OK 跳转系统无障碍设置并诱导授予完全控制权限；用户拒绝返回后，恶意应用立即重放同一诱导弹窗，形成反复施压。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 俄语 -> “注意：要继续观看视频文件，需开启 Android Video Optimization（视频流优化），请启用。”（Admin53Activity 诱导弹窗）
- 英语 -> “使用 Android Video Optimization”（无障碍服务详情页开关）
- 英语 -> “允许 Android Video Optimization 完全控制您的设备？”（系统无障碍授权警告）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用抽屉页，显示 Apps list、搜索及常用图标；无通知/遮罩，点击 Apps list 以查找并启动恶意应用。 | `step_01_action.png` |
| 2 | **Step 2: Admin53Activity** | Admin53Activity 俄语弹窗称需开启 Android Video Optimization 才能看视频；无通知/遮罩，点唯一 OK 转向无障碍授权。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍设置页，DOWNLOADED APPS 下列出 Android Video Optimization；无通知/遮罩，命中 A11Y_SETTINGS 钩子后自动终止。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 仍停留在系统无障碍设置页，UI 文本未捕获；等待 0.8 秒，overlays=0，无通知横幅或遮罩出现。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 仍停留在系统无障碍设置页，UI 文本未捕获；等待 2.0 秒，overlays=0，无通知横幅或遮罩出现。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 无障碍服务详情页，含 Android Video Optimization 及启用开关；无通知/遮罩，执行查看详情/警告。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统授权警告弹窗，英文询问是否允许 Android Video Optimization 完全控制设备；无通知/遮罩，选择 Deny 拒绝。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回 2.0 秒，Admin53Activity 重放俄语诱导弹窗，仍称需开启视频优化；无遮罩，触发 RELAUNCHED_LURE_DIALOG。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回 10.5 秒，Admin53Activity 仍反复重放同一俄语诱导弹窗；无遮罩，再次触发 RELAUNCHED_LURE_DIALOG。 | `step_03_refusal_10500ms_screen.png` |
