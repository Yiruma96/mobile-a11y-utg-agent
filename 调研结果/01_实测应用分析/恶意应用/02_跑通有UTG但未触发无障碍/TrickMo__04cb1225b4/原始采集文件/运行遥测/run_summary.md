# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:07:44
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`monger.discard.wheneer52`（静态标签：`malicious` / `TrickMo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [540, 1800] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `click` → [19] FrameLayout desc="Search" id=search_container_all_ | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `type` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 39 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `monger.discard.wheneer52` / `Bd` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `monger.discard.wheneer52` / `Bd` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Google Play Services` | `Clear`
- **Step 7 (`monger.discard.wheneer52/Bd`)**: (空文本)
- **Step 8 (`monger.discard.wheneer52/Bd`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面启动器打开应用抽屉并搜索伪装成“Google Play Services”的入口，点击后经多次静态Activity跳转进入恶意包空白页；全程未见授权弹窗、拒权结果或明显诱导说明，拒权场景未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 “Google Play Services” -> 中文核心意译：谷歌Play服务；被用作伪装应用名，诱导用户在搜索结果页点击进入（Step 6 搜索结果页）。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面启动器页，显示Apps list、日期及常用图标；点击应用抽屉入口未展开，无通知横幅与悬浮遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面启动器，界面同前；上滑尝试打开应用抽屉未出现新页，仍无通知横幅或悬浮遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉展开，列日历、相机、Chrome等系统应用；再次上滑寻找伪装应用，未见目标及遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 应用抽屉页，仍列系统应用；点击顶部Search搜索框以检索伪装应用，无通知横幅或悬浮遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 启动器搜索页，提示Search apps, web, and more…并输入伪装名；系统搜索界面，无通知或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 搜索结果仅显示Google Play Services；该名称伪装成谷歌Play服务诱导点击进入恶意包，无通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: Bd** | 进入恶意包Bd空白页，无文本、无通知与遮罩；静态跳转探针指向fLTFhC，未展示授权或取消按钮。 | `step_07_screen.png` |
| 8 | **Step 8: Bd** | 仍为恶意包Bd空白页，无可见UI、通知或遮罩；静态探针再跳h76v，未见诱导话术或授权弹窗。 | `step_08_screen.png` |
