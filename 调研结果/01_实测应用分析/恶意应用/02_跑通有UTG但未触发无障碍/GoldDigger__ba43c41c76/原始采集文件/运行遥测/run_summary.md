# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:00:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.tfwyp.ghdtyi.jwrr.dhak`（静态标签：`malicious` / `GoldDigger` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `click` → [17] TextView text="SKY Airline" id=icon (click) center | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 154 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：该样本从系统桌面启动器开始，多次尝试按包名或点击图标启动均未进入应用界面；随后通过静态Activity跳转探测权限相关及混淆页面，但始终停留在桌面/应用抽屉，未观察到授权、拒权或诱导话术。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器首页，显示“应用列表/11月25日周三/信息/Chrome/搜索/语音搜索”；本步尝试按包名启动目标应用，未出现应用界面，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面启动器首页，显示“应用列表、周三、信息、Chrome、搜索”；点击“应用列表”未进入目标应用，无通知、遮罩或授权弹窗。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面启动器未跳转，静态探针尝试直达哈希命名的混淆Activity；页面仍为“应用列表/信息/Chrome”等，无应用界面、通知或遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面启动器页，文本仍为“应用列表、周三、信息、Chrome、搜索”；上滑尝试打开应用抽屉，未见目标应用，无通知、遮罩或授权弹窗。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉界面，显示日历、相机、Chrome、时钟、联系人等；点击“SKY Airline”图标意图启动样本，仍未显示应用内页面，无通知或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 应用抽屉仍停留原页，含日历/相机/Chrome等；静态探针尝试跳转“检查权限”Activity，但界面未变，无权限弹窗、通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 应用抽屉界面未变化，显示日历/相机/Chrome等；静态探针尝试跳转“透明权限”Activity，未见权限请求页，无通知或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 应用抽屉仍为原界面，显示日历/相机/Chrome等；静态探针再次尝试混淆Activity，未出现目标页面、通知、遮罩或授权弹窗。 | `step_08_screen.png` |
