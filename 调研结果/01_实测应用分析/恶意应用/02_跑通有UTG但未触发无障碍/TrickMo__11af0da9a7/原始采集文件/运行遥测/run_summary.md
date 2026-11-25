# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:46:37
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`consnews.matt960.can`（静态标签：`malicious` / `TrickMo` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [540, 1800] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [540, 1200] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `consnews.matt960.can` / `Gestatedisorder` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `consnews.matt960.can` / `Oa1` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `consnews.matt960.can` / `Oa1` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`consnews.matt960.can/Gestatedisorder`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`consnews.matt960.can/Oa1`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`consnews.matt960.can/Oa1`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：该样本从系统桌面进入应用抽屉，未找到伪装“Google服务”入口后，经静态引导连续跳转至包内 Gestatedisorder、Oa1 等 Activity；全程仍显示应用抽屉样式，未见诱导话术、通知或遮罩，授权/拒权未被实际触发。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器主屏，显示“应用列表”、日期及信息/Chrome等图标；点击“应用列表”未打开抽屉。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面主屏，界面文本与上步相同；向上滑动试图展开应用抽屉，但未见抽屉打开。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉已展开，显示日历、相机、Chrome等系统应用；再次上滑以查找伪装“Google服务”应用。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 抽屉仍列系统应用，未出现目标图标；上滑试图露出下方行，结果界面不变，仍无“Google服务”。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 静态跳转至包内Gestatedisorder活动，界面仍为应用抽屉，无通知横幅、无遮罩、无授权弹窗。 | `step_05_screen.png` |
| 6 | **Step 6: Gestatedisorder** | Gestatedisorder静态跳至.Oa1，屏幕仍为系统应用列表，未见新文案或诱导话术，也无授权/取消操作。 | `step_06_screen.png` |
| 7 | **Step 7: Oa1** | Oa1再次静态跳往ZQROWdeKJeAMZp3wrhW7；画面未变，仍为应用抽屉，无通知与遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: Oa1** | Oa1再次静态跳至.NH，界面保持应用列表与系统图标，未呈现授权请求或拒权按钮，交互结果不可见。 | `step_08_screen.png` |
