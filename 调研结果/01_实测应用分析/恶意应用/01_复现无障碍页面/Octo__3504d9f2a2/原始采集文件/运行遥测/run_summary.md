# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:05:24
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.travelabout8`（静态标签：`malicious` / `Octo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.travelabout8/com.travelabout8.p021c` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Google Chrome' / Set switch ON`
- **Back 后 +5.5s**：`com.travelabout8/com.travelabout8.p021c` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Google Chrome' / Set switch ON`
- **Back 后 +10.5s**：`com.travelabout8/com.travelabout8.p021c` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Google Chrome' / Set switch ON`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.travelabout8` / `p021c` | `-` | 1 | 0 / 是 | `click` → [361, 398] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.travelabout8` / `p021c` | `-` | 8 | 74 / 否 | `click` → [8] Button text="Open Settings" id=t_openSettings (clic | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 212 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.travelabout8/p021c`)**: (空文本)
- **Step 2 (`com.travelabout8/p021c`)**: `Enable Accessibility Service` | `•` | `Find` | `'Google Chrome'` | `Set switch ON` | `Open Settings`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Google Chrome` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以 p021c WebView 伪装成启用 Google Chrome 无障碍服务的引导页，通知栏西语“Habilite el servicio”持续施压；点击 Open Settings 跳转系统无障碍页并触发 HOOK，服务详情页夹带西语“保护设备”诱导。用户返回或拒绝授权后，应用立即重启同一诱导对话框（RELAUNCHED_LURE_DIALOG），形成拒权循环。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 西班牙语 -> 请启用服务（通知横幅，各步骤持续显示）
- 英语 -> 启用无障碍服务（p021c 诱导页）
- 英语 -> 找到“Google Chrome”（p021c 诱导页，借合法应用名伪装）
- 英语 -> 打开开关（p021c 诱导页）
- 英语 -> 打开设置（p021c 诱导页按钮）
- 英语 -> 使用 Google Chrome（服务详情页选项）
- 西班牙语 -> 启用此选项以全面保护您的移动设备（服务详情页，恐吓式诱导）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: p021c** | 应用 p021c 空白 WebView 首次加载，尚无可见文案；点击打开设置未命中，通知栏已有西语“启用服务”横幅。 | `step_01_action.png` |
| 2 | **Step 2: p021c** | p021c 诱导页要求启用无障碍、查找 Google Chrome 并开启开关；本步点中 Open Settings，通知横幅持续施压。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 进入系统无障碍设置，DOWNLOADED APPS 中 Google Chrome 为 Off；触发 HOOK 后终止，通知横幅仍显示西语“启用服务”。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍停留在系统无障碍设置页，无遮罩或弹窗；通知栏继续显示西语“启用服务”横幅。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2 秒探针，系统无障碍设置页无 UI 变化、无遮罩；西语“启用服务”通知横幅持续存在。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 进入 Google Chrome 服务详情，含 Use Google Chrome 与快捷键选项；夹带西语“启用可全面保护设备”的恐吓诱导。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 回到 p021c 诱导页，仍要求启用无障碍并打开设置；系统警告或点 Deny 被记录，通知横幅暂隐，未见取消入口。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 拒权返回 2 秒后，应用立即重启同一 p021c 诱导对话框（RELAUNCHED_LURE_DIALOG）；通知横幅恢复，形成拒权循环。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回 10.5 秒后，p021c 诱导页仍被反复拉起，通知横幅持续；RELAUNCHED_LURE_DIALOG 表明拒权后循环施压。 | `step_03_refusal_10500ms_screen.png` |
