# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:49:45
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`superfreeze.tool.android`（静态标签：`benign` / `系统清理与省电冻结` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `8` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `superfreeze.tool.android` / `IntroActivity` | `-` | 4 | 21 / 是 | `click` → [4] ImageButton id=next (click) center=(920,2060) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `superfreeze.tool.android` / `IntroActivity` | `-` | 4 | 255 / 否 | `click` → [4] ImageButton id=next (click) center=(920,2060) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `superfreeze.tool.android` / `IntroActivity` | `-` | 4 | 164 / 否 | `click` → [4] ImageButton id=next (click) center=(920,2060) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `superfreeze.tool.android` / `IntroActivity` | `-` | 8 | 136 / 否 | `click` → [8] ImageButton id=next (click) center=(920,2060) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `superfreeze.tool.android` / `IntroActivity` | `-` | 8 | 174 / 否 | `click` → [8] ImageButton id=next (click) center=(920,2060) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `superfreeze.tool.android` / `IntroActivity` | `-` | 8 | 92 / 否 | `swipe` → [900, 1115] | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `superfreeze.tool.android` / `IntroActivity` | `-` | 9 | 252 / 否 | `click` → [3] LinearLayout id=accessibilityYes (click) center=(54 | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `superfreeze.tool.android` / `IntroActivity` | `-` | 4 | 155 / 否 | `click` → [4] Button text="ENABLE" id=button1 (click) center=(869 | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`superfreeze.tool.android/IntroActivity`)**: `welcome to` | `SuperFreezZ`
- **Step 2 (`superfreeze.tool.android/IntroActivity`)**: `Warning` | `Stopping/freezing apps frequently will probably drain y`
- **Step 3 (`superfreeze.tool.android/IntroActivity`)**: `Info` | `Examples of apps that deserve to be frozen:    • Untrus`
- **Step 4 (`superfreeze.tool.android/IntroActivity`)**: `modes` | `Freeze Mode: ALWAYS FREEZE` | `There are 3 freeze modes. You can choose one for every `
- **Step 5 (`superfreeze.tool.android/IntroActivity`)**: `modes` | `Freeze Mode: INTELLIGENT` | `INTELLIGENT FREEZE will freeze an app only if it has no`
- **Step 6 (`superfreeze.tool.android/IntroActivity`)**: `modes` | `Freeze Mode: NEVER FREEZE` | `NEVER FREEZE will - turn off freezing and never freeze `
- **Step 7 (`superfreeze.tool.android/IntroActivity`)**: `automatic freezing` | `Yes` | `For:  • Ease of use  • Freezing a lot of apps` | `No` | `You will have to press "FORCE STOP", "OK" and "Back" ma`
- **Step 8 (`superfreeze.tool.android/IntroActivity`)**: `Accessibility Service` | `SuperFreezZ needs the accessibility service in order to` | `CANCEL` | `ENABLE`

## 中文逐页引导链路解读

> **全链路总结**：应用以欢迎页和多个介绍页解释冻结/省电逻辑，逐步引导用户选择自动冻结并启用无障碍服务；未见通知横幅或遮罩，授权说明较透明，属合规系统工具引导。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 频繁停止/冻结应用可能更快耗电，因为解冻耗电；同类应用不提示（Step 2 警告页）
- 英文 -> 不可信、少用、烦人的应用值得冻结（Step 3 信息页）
- 英文 -> 自动冻结便于使用和批量冻结；手动需按强制停止、OK、返回，适合慢设备、安全顾虑、不注册无障碍服务（Step 7 选择页）
- 英文 -> SuperFreezZ 需无障碍服务才能自动冻结，请选择本应用并启用访问（Step 8 授权弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: IntroActivity** | IntroActivity欢迎页显示“welcome to SuperFreezZ”，点击右下next箭头进入介绍；无通知横幅与遮罩。 | `step_01_action.png` |
| 2 | **Step 2: IntroActivity** | IntroActivity警告页提示频繁冻结可能更耗电，并批评同类省电应用不提示；点击next继续，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: IntroActivity** | IntroActivity信息页列举值得冻结的应用：不可信、少用、烦人的应用；点击next继续，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: IntroActivity** | IntroActivity冻结模式页介绍“始终冻结”，称任何情况下都冻结应用；点击next继续，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: IntroActivity** | IntroActivity模式页介绍“智能冻结”：默认7天未用才冻结，且不冻结F-Droid应用；点击next继续，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: IntroActivity** | IntroActivity模式页介绍“从不冻结”，即关闭冻结永不再冻结应用；点击next未推进故左滑ViewPager，无通知/遮罩。 | `step_06_action.png` |
| 7 | **Step 7: IntroActivity** | IntroActivity自动冻结选择页：Yes便于使用和批量冻结，No需手动强制停止/OK/返回且适合安全顾虑；点击Yes卡片。 | `step_07_action.png` |
| 8 | **Step 8: IntroActivity** | IntroActivity弹窗称需无障碍服务自动冻结，请选择SuperFreezZ并启用；点击ENABLE进入系统授权，无遮罩。 | `step_08_action.png` |
