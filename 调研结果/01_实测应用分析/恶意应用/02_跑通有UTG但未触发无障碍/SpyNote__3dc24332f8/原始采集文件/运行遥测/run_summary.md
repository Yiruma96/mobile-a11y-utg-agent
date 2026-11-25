# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:20:18
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.definitely.cell`（静态标签：`malicious` / `SpyNote` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `2` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `open` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1688) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.apps.nexuslauncher` / `NexusLauncherActivity` | `-` | 8 | 58 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.definitely.cell` / `zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20` | `-` | 7 | 201 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.definitely.cell` / `zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20` | `-` | 7 | 201 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 2 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 3 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 4 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 5 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 6 (`com.google.android.apps.nexuslauncher/NexusLauncherActivity`)**: `Apps list` | `Wednesday, Nov 25` | `Messages` | `Chrome` | `Search` | `Voice search`
- **Step 7 (`com.definitely.cell/zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20`)**: `Accessibility` | `Blockchain` | `Чтобы разблокировать премиум-функцию,  следуйте этим ша` | `Включить`
- **Step 8 (`com.definitely.cell/zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20`)**: `Accessibility` | `Blockchain` | `Чтобы разблокировать премиум-функцию,  следуйте этим ша` | `Включить`

## 中文逐页引导链路解读

> **全链路总结**：应用从桌面启动器多次尝试直接拉起失败，期间打开应用抽屉并回退到静态 Activity 跳转；最终进入伪装成“Blockchain”的页面，以俄语引导用户开启无障碍服务以解锁所谓高级功能，属于典型 SpyNote 授权诱导链。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 俄语 -> “要解锁高级功能，请按以下步骤：1. 点击启用按钮 2. 前往已安装服务/应用 3. 启用高亮应用”（Step 7/8 Blockchain 无障碍引导页）
- 俄语 -> “Включить”即“启用”按钮（Step 7/8 Blockchain 页面）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: NexusLauncherActivity** | 桌面 NexusLauncher 主屏，显示应用列表、信息、Chrome 等；本步尝试打开目标应用但未进入，通知与遮罩均为 0。 | `step_01_action.png` |
| 2 | **Step 2: NexusLauncherActivity** | 仍在桌面主屏，界面同上；直接拉起目标应用再次失败，系统未显示通知横幅或遮罩，准备改用包名重试。 | `step_02_action.png` |
| 3 | **Step 3: NexusLauncherActivity** | 桌面主屏无变化；直接启动失败后执行静态 Activity 跳转回退，仍停在启动器，未出现目标界面或授权弹窗。 | `step_03_screen.png` |
| 4 | **Step 4: NexusLauncherActivity** | 桌面主屏，点击“Apps list”打开应用抽屉，拟寻找伪装成 Blockchain 的入口；通知与遮罩均为 0，尚未进入应用。 | `step_04_action.png` |
| 5 | **Step 5: NexusLauncherActivity** | 桌面主屏仍显示应用列表入口；再次采用静态 Activity 跳转回退，未成功展示目标页面，也无通知横幅或浮层。 | `step_05_screen.png` |
| 6 | **Step 6: NexusLauncherActivity** | 桌面主屏重复回退跳转，目标 Activity 尚未呈现；页面无通知、无遮罩，仍处于启动器级探针阶段。 | `step_06_screen.png` |
| 7 | **Step 7: zgozvdaumbithjiidvaegtdxza** | 进入伪装 Blockchain 页面，俄语称解锁高级功能需点击启用、到已安装服务/应用启用高亮应用；本步静态跳转，无通知遮罩。 | `step_07_screen.png` |
| 8 | **Step 8: zgozvdaumbithjiidvaegtdxza** | 同一伪装 Blockchain 无障碍引导页，俄语“Включить”即“启用”；本步仍静态跳转，未见通知横幅或遮罩，诱导开启无障碍。 | `step_08_screen.png` |
