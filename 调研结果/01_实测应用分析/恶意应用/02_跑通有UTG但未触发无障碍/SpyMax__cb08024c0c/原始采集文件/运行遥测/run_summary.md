# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:03:14
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`excluding.albuquerque.neural`（静态标签：`malicious` / `SpyMax` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `excluding.albuquerque.neural` / `` | `-` | 1 | 16 / 否 | `wait` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`excluding.albuquerque.neural/`)**: `SEGURANÇA NUBANK`

## 中文逐页引导链路解读

> **全链路总结**：前7步均停留在NexusLauncher桌面/应用列表，直接启动、按包名启动和多次静态Activity跳转均未进入目标界面；第8步才出现目标包启动闪屏，伪装为“NUBANK安全”，并用系统通知中的未本地化文案诱导点击“完成安装”，尚未出现授权/拒权界面，亦未见遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 葡萄牙语 -> 中文核心意译：NUBANK安全（Step 8 启动闪屏，伪装银行安全品牌）
- 英语 -> 中文核心意译：字符串（完成安装）（Step 8 通知标题，疑似未本地化占位文案）
- 英语 -> 中文核心意译：字符串（点击此处完成安装）（Step 8 通知正文，诱导点击完成安装）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 当前为NexusLauncher桌面/应用列表，显示应用列表、11月25日周三、Messages、Chrome、搜索、语音搜索；目标应用未在前台，直接打开主Activity未成功，无通知无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 当前仍是NexusLauncher桌面/应用列表，含应用列表、日期、Messages、Chrome、搜索等；上次启动未生效后再按包名打开仍失败，无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 当前仍为NexusLauncher应用列表；静态Activity跳转回退到目标包名也未见目标界面，说明直接拉起未成功，页面无通知、无遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: NexusLauncherActivity** | 当前仍在NexusLauncher应用列表；点击“Apps list/应用列表”以手动查找已安装目标应用，但页面未切换，仍无目标界面、通知或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 当前仍为NexusLauncher应用列表；静态跳转至目标包costm组件仍未切换到应用界面，探针未成功，无通知与遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 当前仍为NexusLauncher应用列表；静态跳转至androidx FileProvider组件未进入目标界面，说明该跳转非有效入口，无通知与遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 当前仍为NexusLauncher应用列表；静态跳转至目标包MainActive组件仍停留在桌面，未出现应用界面，无通知与遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: ** | 当前页为目标应用启动页：闪屏显示葡语“SEGURANÇA NUBANK”（NUBANK安全），通知横幅以“String (Complete install)”和“String (Click Here to Complete installing)”诱导点击完成安装；无遮罩。 | `step_08_action.png` |
