# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:28:53
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.zam.tquroa`（静态标签：`malicious` / `GoldDigger` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `swipe` → [540, 1600] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 173 / 否 | `click` → [11] TextView text="Identitas Kependudukan Digital" id= | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 173 / 否 | `wait` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 173 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 173 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 173 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 21 | 173 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 7 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`
- **Step 8 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google`

## 中文逐页引导链路解读

> **全链路总结**：轨迹从桌面/应用抽屉开始，点击伪装成“Identitas Kependudukan Digital（数字人口身份/电子身份证）”的图标未成功启动目标应用，随后以静态 Activity 跳转依次探针 CheckPermissionActivity、TransplentPermissionActivity、SplashActivity、ActivationActivity，但画面始终停在 NexusLauncher，未捕获授权/拒权页，拒绝结果未测试。核心特征是利用仿印尼电子身份证名称进行入口伪装，实际权限与激活流程未在界面呈现。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 印尼语 -> “数字人口身份/电子身份证”（应用抽屉伪装图标名称，非弹窗话术）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面页显示“Apps list（应用列表）”、Messages、Chrome等；目标应用未在前台，点击应用列表未进入，无通知与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面：点击应用列表无效后上滑，试图打开应用抽屉查找伪装图标；界面未变化，无通知横幅与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 应用抽屉页：出现伪装图标“Identitas Kependudukan Digital（数字人口身份/电子身份证）”，已点击该图标尝试启动，无通知与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NexusLauncherActivity** | 仍在应用抽屉：上一击未触发目标应用，等待后界面无变化；伪装电子身份证图标仍可见，无通知与遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 仍停留应用抽屉：静态引导跳转探针 CheckPermissionActivity，但画面未切换、未显示权限说明页，无通知与遮罩。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 仍为应用抽屉：静态跳转 TransplentPermissionActivity 探针，未渲染透明权限页，仍只见图标列表，无通知遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: NexusLauncherActivity** | 仍为应用抽屉：静态跳转 SplashActivity 探针，启动页未显示，界面仍是桌面图标列表，无通知与遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: NexusLauncherActivity** | 仍为应用抽屉：静态跳转 ActivationActivity 探针，激活页未渲染，界面无变化，无通知与遮罩，未出现授权/拒权按钮。 | `step_08_screen.png` |
