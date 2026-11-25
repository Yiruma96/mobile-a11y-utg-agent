# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:13:05
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.gelini`（静态标签：`malicious` / `BankBot` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.gelini` / `MainActivity` | `-` | 3 | 49 / 否 | `click` → [3] Button text="CONTINUAR" id=button3 (click) center=( | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.gelini/MainActivity`)**: `Atenção` | `Atualização aplicada com sucesso.` | `CONTINUAR`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：应用以葡语“更新成功”弹窗为入口，仅提供“继续”诱导点击，随后退至桌面并隐藏图标；多次重启动失败后，探针改以静态跳转尝试进入 com.irifix 的 AccService 与 MainActivity 内部类，未观察到授权或拒权页面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语 -> 注意（Step 1 MainActivity）
- 葡萄牙语 -> 更新已成功应用（Step 1 MainActivity）
- 葡萄牙语 -> 继续（Step 1 MainActivity，唯一按钮）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 入口弹窗：葡语“注意，更新已成功应用”，仅“继续”按钮；点击后应用退到后台并隐藏图标。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 桌面首页：显示应用列表、日期、Messages、Chrome、搜索等；从桌面重新打开目标失败，未见应用界面。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 仍为桌面首页：应用列表与常规图标可见；再次按包名启动仍无效，目标图标已被隐藏，无通知或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面首页停留：常规图标与搜索可见；自动静态跳转探针指向 com.irifix.AccService，未呈现可交互应用页面。 | `step_04_screen.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面首页：Messages、Chrome、搜索可见；尝试按包名强制重启仍未进入应用，图标隐藏状态持续，无通知横幅。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面首页无变化：应用列表、日期和搜索仍在；静态跳转探针指向 com.irifix.MainActivity，仍未显示业务界面。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面首页：图标与搜索可见，无遮罩通知；静态跳转探针指向 com.irifix.MainActivity$a 内部类，未发生可见页面切换。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面首页：应用列表与常规图标可见；静态跳转探针指向 com.irifix.MainActivity$a$1，仍无可见界面或权限弹窗。 | `step_08_screen.png` |
