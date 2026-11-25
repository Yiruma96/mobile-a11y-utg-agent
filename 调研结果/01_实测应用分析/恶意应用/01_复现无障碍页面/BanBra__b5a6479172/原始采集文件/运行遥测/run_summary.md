# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:05:06
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.brazil.android.free`（静态标签：`malicious` / `BanBra` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 4 步，UTG 唯一节点 `3` 个，有向边 `4` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_A11Y_SETTINGS`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 4 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$WriteSettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_04_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.android.settings/com.android.settings.Settings$WriteSettingsActivity` | hooks=`['HOOK_A11Y_SETTINGS']` | overlays=`0` | texts=`Collapse / accessibility / Clear query / More options`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.android.settings` / `Settings$WriteSettingsActivity` | `-` | 25 | 129 / 否 | `click` → [3] TextView desc="Search" id=search_app_list_menu (cli | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$WriteSettingsActivity` | `-` | 23 | 111 / 否 | `click` → [2] EditText text="Search" id=search_src_text (click) c | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$WriteSettingsActivity` | `-` | 23 | 111 / 否 | `type` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.android.settings` / `Settings$WriteSettingsActivity` | `HOOK_A11Y_SETTINGS` | 4 | 44 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_04_layout.xml` + `step_04_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.android.settings/Settings$WriteSettingsActivity`)**: `Back` | `Modify system settings` | `Search` | `More options` | `Camera` | `Allowed` | `Contacts` | `Defensor Digital` | `Not allowed` | `Google`
- **Step 2 (`com.android.settings/Settings$WriteSettingsActivity`)**: `Collapse` | `Search` | `More options` | `Camera` | `Allowed` | `Contacts` | `Defensor Digital` | `Not allowed` | `Google` | `Google Play services`
- **Step 3 (`com.android.settings/Settings$WriteSettingsActivity`)**: `Collapse` | `Search` | `More options` | `Camera` | `Allowed` | `Contacts` | `Defensor Digital` | `Not allowed` | `Google` | `Google Play services`
- **Step 4 (`com.android.settings/Settings$WriteSettingsActivity`)**: `Collapse` | `accessibility` | `Clear query` | `More options`

## 中文逐页引导链路解读

> **全链路总结**：应用以“Defensor Digital（数字卫士）”伪装安全工具，先停在“修改系统设置”授权页，再搜索无障碍设置并触发钩子；拒权返回后落入 STALE_SETTINGS_BACKSTACK，未见显式弹窗话术但存在高权限诱导路径。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语 Defensor Digital -> “数字卫士/数字防御者”，安全工具式伪装名称（Step1 修改系统设置页）
- 英语 Modify system settings -> “修改系统设置”，高权限授权页标题（Step1-2）
- 英语 accessibility -> “无障碍”，用于检索无障碍授权入口（Step3-4）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: Settings$WriteSettingsActi** | “修改系统设置”授权页：Defensor Digital 显示“不允许”，相机为“允许”；本步点搜索图标，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: Settings$WriteSettingsActi** | 仍在“修改系统设置”页，搜索栏已展开；本步点搜索输入框准备检索，无通知横幅、无遮罩、无取消授权键。 | `step_02_action.png` |
| 3 | **Step 3: Settings$WriteSettingsActi** | 授权页搜索框已聚焦，本步输入关键词“accessibility（无障碍）”；无通知/遮罩，未见取消或拒绝提示。 | `step_03_action.png` |
| 4 | **Step 4: [无障碍列表页]** | “无障碍列表页”搜索框显示“accessibility（无障碍）”；触发无障碍钩子探针后自动终止，无通知/遮罩。 | `step_04_screen.png` |
| 5 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针：仍在设置活动页，无可见文本；等待期间无通知横幅、无遮罩（overlays=0）。 | `step_04_probe_800ms_screen.png` |
| 6 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针：页面无可见文本，仍无通知与遮罩（overlays=0）；未见新增授权弹窗或诱导提示。 | `step_04_probe_2000ms_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回 2.0 秒：搜索框仍为“accessibility（无障碍）”，返回后设置回退栈陈旧，无通知/遮罩。 | `step_04_refusal_2000ms_screen.png` |
