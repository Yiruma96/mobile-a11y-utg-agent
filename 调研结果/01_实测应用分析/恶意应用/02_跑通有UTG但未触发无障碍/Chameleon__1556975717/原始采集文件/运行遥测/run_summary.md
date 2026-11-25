# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:12:23
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.because.toe`（静态标签：`malicious` / `Chameleon` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `1` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.because.toe` / `MainActivity` | `-` | 9 | 74 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.because.toe` / `MainActivity` | `-` | 9 | 74 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.because.toe` / `MainActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.because.toe` / `MainActivity` | `-` | 9 | 74 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.because.toe` / `MainActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.because.toe` / `MainActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.because.toe` / `MainActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.because.toe` / `MainActivity` | `-` | 9 | 74 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.because.toe/MainActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.because.toe/MainActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.because.toe/MainActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.because.toe/MainActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.because.toe/MainActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.because.toe/MainActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.because.toe/MainActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.because.toe/MainActivity`)**: `Apps list` | `Wednesday, Nov 25` | `-1°C` | `Cloudy, -1°C` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：该应用入口MainActivity未展示自身界面，而是反复退至系统桌面，并多次通过静态引导跳转至内部命名为GmailNew、Facebook、Chrome、Youtube、Play的Activity，呈现Chameleon式仿冒常用应用入口特征；全程无通知/遮罩，未实际测试授权或拒权。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 系统桌面非应用界面：应用列表、11月25日周三、-1°C多云、消息/Chrome/搜索；打开后仍停留桌面，无通知遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 系统桌面仍在前台：应用列表、日期天气、消息/Chrome/搜索；上滑后未进入应用，仍无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 系统桌面未变：应用列表、日期天气、消息/Chrome/搜索；静态跳转至内部GmailNew，画面仍桌面，无通知遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: MainActivity** | 系统桌面仍在前台：应用列表、日期天气、消息/Chrome/搜索；按包名重开未显示应用，仍无通知遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 系统桌面未变：应用列表、日期天气、消息/Chrome/搜索；静态跳转至内部Facebook，实际仍桌面，无通知遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: MainActivity** | 系统桌面未变：应用列表、日期天气、消息/Chrome/搜索；静态跳转至内部Chrome，实际仍桌面，无通知遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: MainActivity** | 系统桌面未变：应用列表、日期天气、消息/Chrome/搜索；静态跳转至内部Youtube，实际仍桌面，无通知遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: MainActivity** | 系统桌面未变：应用列表、日期天气、消息/Chrome/搜索；静态跳转至内部Play，实际仍桌面，无通知遮罩。 | `step_08_screen.png` |
