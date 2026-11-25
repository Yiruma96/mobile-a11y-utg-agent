# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:14:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`baggage.stream.gonad`（静态标签：`malicious` / `Crocodilus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [900, 1200] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [900, 1200] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `baggage.stream.gonad` / `KFCTREgivzR` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `baggage.stream.gonad` / `KFCTREgivzR` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `baggage.stream.gonad` / `KFCTREgivzR` | `-` | 20 | 143 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`baggage.stream.gonad/KFCTREgivzR`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`baggage.stream.gonad/KFCTREgivzR`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`baggage.stream.gonad/KFCTREgivzR`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：该应用从桌面启动器打开应用抽屉并多次滑动未找到目标，随后通过静态引导回退连续跳转 baggage.stream.gonad 的多个混淆 Activity。全程未出现实际诱导界面、通知或授权弹窗，仅表现为 Crocodilus 投放器的规避式跳转与界面未渲染。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面应用抽屉入口页，显示“应用列表”“搜索”“语音搜索”等英文；点击“应用列表”尝试打开抽屉以寻找目标投放器。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面页，英文“应用列表/搜索/语音搜索”；上滑未打开抽屉，遂从主屏上滑继续尝试进入应用抽屉。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉已展开，列出日历、相机、Chrome等英文应用名；目标投放器未出现，向左滑动翻页查找。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 应用抽屉同一列表页，仍见日历、相机、Chrome等英文名称；再次左滑翻页，目标应用仍未显示。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 抽屉列表无变化，系统以静态引导回退直接跳转目标包混淆Activity KFCTREgivzR，属自动化探针跳转。 | `step_05_screen.png` |
| 6 | **Step 6: KFCTREgivzR** | 已切入目标包KFCTREgivzR，但画面仍停在应用抽屉，仅见日历、相机等英文名；无诱导弹窗、通知或遮罩，随后回退跳转。 | `step_06_screen.png` |
| 7 | **Step 7: KFCTREgivzR** | 目标包页未渲染新界面，仍是应用抽屉英文列表；探针静态跳转至混淆子页LaZGKudaf.vbOEuaVEYn，无授权提示。 | `step_07_screen.png` |
| 8 | **Step 8: KFCTREgivzR** | 仍无目标包可视界面，应用抽屉英文列表保持；再次静态跳转至混淆子页YZGzqExRMM.xEeCsbrbBnIyl，未见通知、遮罩或取消键。 | `step_08_screen.png` |
