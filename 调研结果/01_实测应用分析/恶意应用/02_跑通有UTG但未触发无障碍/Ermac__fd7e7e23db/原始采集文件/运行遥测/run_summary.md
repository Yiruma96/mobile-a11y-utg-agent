# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:30:20
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.tag.right`（静态标签：`malicious` / `Ermac` / 静态可见性：`packed_or_encrypted`）
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
| 4 | `com.tag.right` / `moye` | `-` | 0 | 0 / 否 | `swipe` → [540, 1700] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.tag.right` / `moye` | `-` | 0 | 0 / 否 | `open` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.tag.right` / `moye` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.tag.right` / `cevuna` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.tag.right` / `cevuna` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.tag.right/moye`)**: (空文本)
- **Step 5 (`com.tag.right/moye`)**: (空文本)
- **Step 6 (`com.tag.right/moye`)**: (空文本)
- **Step 7 (`com.tag.right/cevuna`)**: (空文本)
- **Step 8 (`com.tag.right/cevuna`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面入口未能直接拉起，经多次包名启动与静态 Activity 跳转进入 com.tag.right 的 moye、cevuna 等空白页，全程未见授权弹窗或诱导界面，最终未进入授权/拒权环节（not_tested）。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面主屏含 Apps list、Messages、Chrome 等入口；顶部有英文“数据未备份/添加备份账户”系统通知，无遮罩，本步仅 open 尝试拉起目标包。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面主屏，界面同前；点击“Apps list”试图打开应用抽屉，目标应用未显现，系统备份通知持续，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面主屏未变，直接静态跳转到混淆包名的 moye 页面；界面未见任何内容或授权提示，系统备份通知仍在。 | `step_03_screen.png` |
| 4 | **Step 4: moye** | 进入 com.tag.right 的 moye 空白页，无可见文案与遮罩；执行上滑动作但未出现应用列表，系统备份通知仍在。 | `step_04_action.png` |
| 5 | **Step 5: moye** | moye 空白页仍无内容，应用包处于活动状态但桌面未正常拉起；再次按包名 open 尝试启动，无授权弹窗。 | `step_05_action.png` |
| 6 | **Step 6: moye** | moye 空白页未变化，静态跳转至混淆子包 xexerexejeko.cevuna；全程无可见话术、无遮罩、无取消/授权控件。 | `step_06_screen.png` |
| 7 | **Step 7: cevuna** | 进入 cevuna 空白页，无任何 UI 文案；随即静态跳转至 zamosa，仍无授权弹窗或诱导界面，系统通知在。 | `step_07_screen.png` |
| 8 | **Step 8: cevuna** | cevuna 空白页保持空白，继续静态跳转至 kivamu.duyehi；未出现权限请求、遮罩或可交互控件，链路终止于此观测。 | `step_08_screen.png` |
