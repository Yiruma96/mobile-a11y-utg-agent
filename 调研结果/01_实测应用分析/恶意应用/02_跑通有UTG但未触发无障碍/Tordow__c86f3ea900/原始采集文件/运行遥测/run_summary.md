# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:02:08
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.example.raccoonapi2`（静态标签：`malicious` / `Tordow` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1900] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 166 / 否 | `open` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 166 / 否 | `open` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 166 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 166 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 166 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 166 / 否 | `click` → [2] TextView text="Android Security Update" id=icon (cl | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Android Security Update` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Android Security Update` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Android Security Update` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Android Security Update` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Android Security Update` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Android Security Update` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面进入应用列表并上滑打开应用抽屉，目标应用冷启动时隐藏自身图标，仅以“Android Security Update”伪装项出现；多次静态跳转 DummyAccessibility、MyReceiver、MainActivity 均未展示实际界面，未见通知或遮罩，且未测试拒权结果。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Android Security Update -> “Android 安全更新”（应用抽屉伪装图标，疑似诱导点击入口）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面主屏，含“Apps list/应用列表”、日期及信息、Chrome等图标；本步点击“Apps list”打开应用列表。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面，显示应用列表入口、日期与常用图标；本步从底部上滑，尝试打开应用抽屉，未见通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉页，含“Android Security Update/Android 安全更新”伪装项及系统应用；本步尝试按包名直接启动，界面未变。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 应用抽屉页，仍见“Android Security Update”伪装图标与系统应用列表；再次尝试按包名启动目标，界面无变化。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉页，显示伪装安全更新项及系统应用；本步静态跳转 DummyAccessibility 组件，仍停留抽屉，无通知或遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 应用抽屉页，仍为系统应用与“Android Security Update”伪装项；本步静态跳转 MyReceiver，界面未变化，无遮罩或通知。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 应用抽屉页，含伪装安全更新图标；本步静态跳转 MainActivity，仍未出现应用界面，无通知横幅或悬浮遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 应用抽屉页，点击“Android Security Update/Android 安全更新”伪装图标，疑似诱导入口；未展示实际应用页面，无通知或遮罩。 | `step_08_action.png` |
