# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:42:39
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`dtlaxmiguptaclasses.in.net`（静态标签：`malicious` / `SpyNote` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `dtlaxmiguptaclasses.in.net` / `aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31` | `-` | 3 | 68 / 否 | `click` → [3] Button text="ok" id=button1 (click) center=(540,138 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `dtlaxmiguptaclasses.in.net` / `aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31` | `-` | 3 | 68 / 否 | `click` → [3] Button text="ok" id=button1 (click) center=(540,138 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`dtlaxmiguptaclasses.in.net/aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31`)**: `TG88` | `Emulator detected.  this app does not support emulator ` | `ok`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`dtlaxmiguptaclasses.in.net/aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31`)**: `TG88` | `Emulator detected.  this app does not support emulator ` | `ok`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`

## 中文逐页引导链路解读

> **全链路总结**：应用入口为混淆命名的TG88页面，启动即弹出“检测到模拟器”阻断框；点击ok后反复退回系统桌面，多次静态跳转也未恢复应用流程，未出现权限授权/拒绝提示，整体呈反模拟器、反分析特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 检测到模拟器。本应用不支持模拟器设备（Step 1/Step 5 入口阻断弹窗）
- 英文 -> 确定（Step 1/Step 5 弹窗唯一按钮，无取消选项）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: aksnmvsovloyugmwsdtlqnfhfr** | TG88入口弹出英文“检测到模拟器，本应用不支持模拟器设备”阻断框，仅ok无取消键；点确定未进入应用，无通知遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 系统桌面显示应用列表、日期、信息、Chrome、搜索与语音搜索；打开TG88失败仍停留桌面，无通知遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 仍在系统桌面，含应用列表、日期、信息、Chrome、搜索与语音搜索；点击“应用列表”欲定位TG88，未进入应用，无通知遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 系统桌面保持前台，含应用列表、日期、信息、Chrome、搜索与语音搜索；静态跳转混淆Activity失败，仍停留桌面，无通知遮罩。 | `step_04_screen.png` |
| 5 | **Step 5: aksnmvsovloyugmwsdtlqnfhfr** | 再次出现TG88英文“检测到模拟器，本应用不支持模拟器设备”阻断框，仅ok无取消；再点确定仍未进入应用，无通知遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 系统桌面仍在前台，含应用列表、日期、信息、Chrome、搜索与语音搜索；再试静态跳转混淆Activity失败，未回TG88，无通知遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 系统桌面重复出现，含应用列表、日期、信息、Chrome、搜索与语音搜索；静态跳转混淆Activity再失败，流程未恢复，无通知遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 系统桌面仍未变化，含应用列表、日期、信息、Chrome、搜索与语音搜索；末次静态跳转混淆Activity失败，未恢复TG88，无通知遮罩。 | `step_08_screen.png` |
