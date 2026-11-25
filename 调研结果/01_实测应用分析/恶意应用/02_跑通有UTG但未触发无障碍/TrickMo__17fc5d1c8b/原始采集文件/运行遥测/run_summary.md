# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:24:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`centtem.houe948.ov`（静态标签：`malicious` / `TrickMo` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1600] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [540, 1800] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [900, 900] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `centtem.houe948.ov` / `ojfY0f4MWzO` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `centtem.houe948.ov` / `ojfY0f4MWzO` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `centtem.houe948.ov` / `ojfY0f4MWzO` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`centtem.houe948.ov/ojfY0f4MWzO`)**: (空文本)
- **Step 7 (`centtem.houe948.ov/ojfY0f4MWzO`)**: (空文本)
- **Step 8 (`centtem.houe948.ov/ojfY0f4MWzO`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：轨迹从系统启动器查找“Google services”应用失败后，经静态引导直接切入恶意包centtem.houe948.ov的多个空白Activity并连续跳转；全程未见可见诱导话术、通知或遮罩，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 系统启动器应用列表页，含“应用列表、搜索、语音搜索”等；点击后打开应用抽屉，未见通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为启动器应用列表页，显示11月25日周三、信息、Chrome等；上滑打开抽屉，未出现通知或浮层遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 启动器应用抽屉页列日历、相机、Chrome等常见应用；上滑滚动查找目标应用，未发现“Google服务”入口。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 同一应用抽屉页仍仅见常见应用图标；左滑尝试翻页未获新页，未出现通知、遮罩或诱导文本。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 页面仍为启动器抽屉；本步触发静态引导跳转，直接进入恶意包Activity .ojfY0f4MWzO，原页无通知/遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: ojfY0f4MWzO** | 进入恶意包centtem.houe948.ov的空白Activity ojfY0f4MWzO，无可见文本；随即静态跳转.dyjGgnh，无通知与遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: ojfY0f4MWzO** | 恶意包空白Activity ojfY0f4MWzO仍无文本和按钮；本步静态跳转至.dnCongKR186，通知与遮罩均为0。 | `step_07_screen.png` |
| 8 | **Step 8: ojfY0f4MWzO** | 恶意包空白Activity继续静态跳向ConstraintProxy$Batter，无可见话术或取消键；通知、遮罩计数均为0。 | `step_08_screen.png` |
