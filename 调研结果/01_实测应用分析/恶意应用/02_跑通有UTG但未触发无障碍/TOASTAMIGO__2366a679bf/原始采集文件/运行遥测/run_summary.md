# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:45:08
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.agomi.applocker`（静态标签：`malicious` / `TOASTAMIGO` / 静态可见性：`packed_or_encrypted`）
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
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 158 / 否 | `click` → [17] TextView text="Smart AppLocker" id=icon (click) ce | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 158 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 158 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 158 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

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

> **全链路总结**：动态链路全程停留在 Nexus 启动器或应用抽屉：多次尝试启动“Smart AppLocker”，并通过静态引导跳转至无障碍服务、应用列表和 Stub 组件，均未成功进入真实界面；未出现通知、遮罩或授权弹窗，仅暴露伪装成安全工具的入口名称。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 智能应用锁（Step 5 应用抽屉图标，疑似以安全工具名义诱导点击）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | Nexus启动器主屏，含应用列表、周三11月25日、信息、Chrome、搜索、语音搜索；按包名直接启动目标未生效，仍停留桌面。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍为Nexus启动器主屏，显示应用列表与常用图标；点击“Apps list（应用列表）”尝试打开抽屉未奏效，页面无变化。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 同一启动器主屏；静态跳转至MediaActivity无障碍页的探针失败，未离开桌面，无新界面、通知或遮罩。 | `step_03_screen.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在Nexus主屏；从底部上滑尝试拉起应用抽屉，但本帧仍显示原桌面，未见目标应用界面或提示。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 应用抽屉已展开，显示日历、相机、Chrome、时钟等；点击“Smart AppLocker（智能应用锁）”图标尝试启动。 | `step_05_action.png` |
| 6 | **Step 6: NexusLauncherActivity** | 应用抽屉仍展开；静态跳转至MyAccessibilityServiceTmp无障碍服务探针失败，仍停留启动器，无授权弹窗。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍为应用抽屉；再静态跳转ApplicationListActivity（应用列表页）失败，未见应用锁列表界面或遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 应用抽屉仍展开；静态跳转Stub01占位组件探针失败，全程未进入com.agomi.applocker真实页面，无通知横幅。 | `step_08_screen.png` |
