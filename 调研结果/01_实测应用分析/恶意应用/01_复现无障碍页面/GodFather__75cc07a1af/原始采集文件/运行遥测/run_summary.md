# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:04:37
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.alphainventor.filemanager`（静态标签：`malicious` / `GodFather` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `5` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.alphainventor.filemanager/com.alphainventor.filemanager.Activitys.vivacissimoselftimer` | hooks=`[]` | overlays=`0` | texts=``
- **Back 后 +5.5s**：`com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Back / Accessibility / Search settings / DOWNLOADED APPS / Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.alphainventor.filemanager` / `vivacissimoselftimer` | `-` | 0 | 0 / 否 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 220 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.alphainventor.filemanager/vivacissimoselftimer`)**: (空文本)
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: vivacissimoselftimer** | Step 1: vivacissimoselftimer（vivacissimoselftimer）：无文本；动作 wait | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | Step 2: [无障碍列表页]（Settings$AccessibilitySettingsActivity）：Back / Accessibility / Search settings；动作 terminate | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后探针 +0.8s（Settings$AccessibilitySettingsActivity）：无文本；动作 wait(0.8s) | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后探针 +2.0s（Settings$AccessibilitySettingsActivity）：无文本；动作 wait(2.0s) | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页（SubSettings）：Back / Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i / Use Ş‎a‎r；动作 inspect_detail_or_warning | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统警告弹窗(点Deny)（SubSettings）：Allow Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i to have full；动作 inspect_detail_or_warning | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回 +2.0s（vivacissimoselftimer）：无文本；动作 Back_refuse -> RELAUNCHED_A11Y_SETTINGS | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +5.5s** | 拒权返回 +5.5s（Settings$AccessibilitySettingsActivity）：Back / Accessibility / Search settings；动作 Back_refuse -> RELAUNCHED_A11Y_SETTINGS | `step_02_refusal_5500ms_screen.png` |
