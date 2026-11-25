# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:40:16
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`untitled.lividly.disobey`（静态标签：`malicious` / `Crocodilus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `untitled.lividly.disobey` / `AatUqiQRi` | `-` | 8 | 58 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `untitled.lividly.disobey` / `AatUqiQRi` | `-` | 8 | 58 / 否 | `swipe` → [540, 1500] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`untitled.lividly.disobey/AatUqiQRi`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`untitled.lividly.disobey/AatUqiQRi`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：代理从桌面尝试启动未果，经应用抽屉与静态引导跳转进入 untitled.lividly.disobey 的多个 Activity；可见界面始终为桌面或透明页，未出现应用内诱导文案、通知、遮罩或授权/拒权结果。核心表现为 Crocodilus 加载器式透明 Activity 前台切换，未完成可见授权链路。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面主屏，显示“应用列表/11月25日星期三/信息/Chrome/搜索/语音搜索”；执行 open 未启动目标应用，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面主屏，英文同上；点击“应用列表”打开抽屉以寻找 Play-Plus 加载器，未进入应用，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面/应用抽屉页，未见应用界面；系统执行静态 Activity 跳转至 .AatUqiQRi，仍无可见诱导文案、通知或遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: AatUqiQRi** | AatUqiQRi 前台但界面仍透出桌面标签“应用列表/信息/搜索”等；等待后无应用 UI、无通知或遮罩，未出现授权提示。 | `step_04_action.png` |
| 5 | **Step 5: AatUqiQRi** | 同一透明 AatUqiQRi 页，仍见桌面英文标签；执行上滑后未显露应用内容，无通知、遮罩或取消键，也无诱导话术。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 回到桌面/应用抽屉，显示日历/相机/Chrome 等图标；静态跳转至 .TrumpTayyip，未见应用页面、通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 桌面应用列表页，图标标签为日历、相机、联系人等；静态跳转至 .YzYQRvhWFJDll.qjSiKSYDT，仍无可视应用 UI 或诱导文案。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 桌面应用列表页，英文图标名如 Calendar/Camera/Contacts；静态跳转至 .fpiIoMjBZDT.VpaEyFLWstvJz，未见通知、遮罩或授权弹窗。 | `step_08_screen.png` |
