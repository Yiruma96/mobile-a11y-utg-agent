# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:08:24
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`breatham.li373.pai`（静态标签：`malicious` / `TrickMo` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `swipe` → [900, 1000] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 20 | 143 / 否 | `click` → [19] FrameLayout desc="Search" id=search_container_all_ | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 53 / 否 | `type` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 5 | 34 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `breatham.li373.pai` / `Q06wlDFVTbTG` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `breatham.li373.pai` / `Q06wlDFVTbTG` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Search apps, web, and more…` | `Voice Search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Go to Discover` | `Google services` | `Clear`
- **Step 7 (`breatham.li373.pai/Q06wlDFVTbTG`)**: (空文本)
- **Step 8 (`breatham.li373.pai/Q06wlDFVTbTG`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：链路从 NexusLauncher 桌面进入应用抽屉，未找到目标后改用搜索并输入伪装名“Google services”，随后静态引导跳转进入恶意包的多个混淆 Activity（Q06wlDFVTbTG→uIgeg8Dkpo6tfk→zdwdbOM1sCU）。全程页面空白，无通知/遮罩，未测试授权或拒权，核心特征是冒充 Google 服务并借系统搜索入口诱导启动。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “Google 服务”（第6步搜索页：以系统组件样式名称作为应用名，诱导用户点击启动恶意包）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面主屏，显示“应用列表、消息、Chrome、搜索、语音搜索”；点击应用列表进入抽屉以查找伪装应用，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为桌面主屏，显示应用列表、消息、Chrome、搜索与语音搜索；上滑尝试打开应用抽屉，页面未变，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉首页，列有日历、相机、Chrome、时钟、联系人、Gmail、Google、地图等；左滑翻页找“Google services”未成功，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 应用抽屉仍首页，系统应用列表未变；点击“搜索”容器，改用抽屉搜索定位“Google services”，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 抽屉搜索页，显示“前往 Discover、搜索应用/网页等、语音搜索”；输入“Google services”查找伪装应用，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 搜索页出现“Google services”结果及“清除”，未显示应用信息；探针触发静态跳转至包内 Q06wlDFVTbTG，无通知/遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: Q06wlDFVTbTG** | 进入恶意包内混淆活动 Q06wlDFVTbTG，界面无文字与控件；静态探针继续跳转至 .uIgeg8Dkpo6tfk，无通知/遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: Q06wlDFVTbTG** | 仍在混淆活动 Q06wlDFVTbTG，界面空白无文字；探针再次静态跳转至 .zdwdbOM1sCU，无通知横幅或遮罩。 | `step_08_screen.png` |
