# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:54:44
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.broughtbluea`（静态标签：`malicious` / `Octo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `3` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.broughtbluea/com.broughtbluea.p014i` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Trendyol' / Set switch ON`
- **Back 后 +5.5s**：`com.broughtbluea/com.broughtbluea.p014i` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Trendyol' / Set switch ON`
- **Back 后 +10.5s**：`com.broughtbluea/com.broughtbluea.p014i` | hooks=`[]` | overlays=`0` | texts=`Enable Accessibility Service / • / Find / 'Trendyol' / Set switch ON`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.broughtbluea` / `p014i` | `-` | 8 | 69 / 否 | `click` → [8] Button text="Open Settings" id=t_openSettings (clic | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 207 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.broughtbluea/p014i`)**: `Enable Accessibility Service` | `•` | `Find` | `'Trendyol'` | `Set switch ON` | `Open Settings`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Trendyol` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以“Trendyol”无障碍服务名义发送土耳其语通知并展示英文引导页，诱导用户进入系统无障碍设置开启服务；进入详情页后仍以品牌名和启用选项诱导，用户拒绝返回后应用反复重拉同一诱导页面，后台通知常驻。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 启用无障碍服务；找到“Trendyol”；把开关打开（应用引导页）
- 英文 -> 打开设置（应用引导页按钮）
- 土耳其语 -> 请启用服务（通知标题）
- 英文/品牌名 -> Trendyol（通知正文、系统设置项、服务详情页）
- 英文 -> 使用 Trendyol（服务详情页选项）
- 土耳其语 -> 无障碍服务启用（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: p014i** | 应用内英文预授权引导页，要求找到“Trendyol”并开启无障碍开关；本步点击“Open Settings”跳系统设置，通知横幅显示土耳其语“请启用服务/Trendyol”。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表页，下载应用中“Trendyol”显示 Off；捕获无障碍设置钩子后自动终止，顶部仍有该应用土耳其语“请启用服务/Trendyol”通知，无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后0.8秒探针仍停在系统无障碍列表，界面文本暂空、遮罩数0；后台“请启用服务/Trendyol”通知持续存在。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后2.0秒探针同页无新文本，遮罩仍为0；该应用通知继续常驻，未见系统授权成功或取消提示。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 进入 Trendyol 无障碍服务详情页，含“Use Trendyol”使用服务、快捷方式等选项及土耳其语“无障碍服务启用”；未弹遮罩，等待用户开启。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 本步未捕获系统警告，仍显示应用英文引导页“启用无障碍服务/找到Trendyol/打开设置”；无遮罩与通知，疑似警告被绕过或漏录。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝授权返回2秒后，应用重拉同一英文引导页，仍要求开启Trendyol无障碍；无遮罩，通知横幅恢复为土耳其语“请启用服务”。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权10.5秒后仍停同一引导页并再次重拉诱导弹窗，文案按钮不变；通知持续存在，显示应用不接受拒绝、循环诱导。 | `step_02_refusal_10500ms_screen.png` |
