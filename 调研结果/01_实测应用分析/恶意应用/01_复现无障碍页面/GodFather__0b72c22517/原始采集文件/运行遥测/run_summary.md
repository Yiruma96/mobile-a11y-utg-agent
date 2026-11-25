# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:42:27
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.rduzmauwns.jieliysagr`（静态标签：`malicious` / `GodFather` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +5.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`
- **Back 后 +10.5s**：`com.google.android.apps.nexuslauncher/com.google.android.apps.nexuslauncher.NexusLauncherActivity` | hooks=`[]` | overlays=`0` | texts=`Apps list / Wednesday, Nov 25 / Messages / Chrome / Search`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 217 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `apkversion1.1.5.43` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面启动后引导至系统无障碍设置，以“apkversion1.1.5.43”服务名和“请激活以使更新生效”通知诱导授权；捕获无障碍设置钩子与探针后终止，拒权后返回桌面并保持驻留/降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 请激活以使更新生效（无障碍设置页及跳后探针通知横幅）
- English -> 未提供描述（服务详情页，服务描述为空）
- English -> apkversion1.1.5.43（无障碍服务显示名，伪装为版本号）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器首页，显示应用列表与Chrome等图标；目标应用通知已出现，标题为包名、正文为空；本步点击启动目标应用。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 无障碍设置页列“apkversion1.1.5.43”且关闭；通知诱导“激活以更新”；捕获设置钩子与探针后终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 页面停留于无障碍设置，UI文本为空；目标应用通知仍在并催促激活更新；等待0.8秒探针显示无遮罩、无弹窗。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 仍为无障碍设置空文本页；通知横幅持续提示激活更新；等待2.0秒探针仍无遮罩、无浮层，界面无变化。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页显示“使用apkversion1.1.5.43”、快捷方式与“按住音量键”；描述为空；本步仅检查详情与警告。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 服务详情页触发系统警告场景，可见“使用apkversion…”及快捷方式；选择拒绝；探针遮罩为0，无额外弹窗文本。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权后2秒返回桌面启动器；目标应用通知仍驻留，含激活更新提示；无遮罩，结果为优雅停留或降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权后10.5秒仍在桌面；目标应用通知继续驻留并提示激活更新；无遮罩，应用未崩溃，维持降级/停留。 | `step_02_refusal_10500ms_screen.png` |
