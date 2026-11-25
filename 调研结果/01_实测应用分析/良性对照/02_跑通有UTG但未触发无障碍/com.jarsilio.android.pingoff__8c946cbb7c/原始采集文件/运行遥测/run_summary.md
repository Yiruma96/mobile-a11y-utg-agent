# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:24:19
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.jarsilio.android.pingoff`（静态标签：`benign` / `系统清理与省电冻结` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `1` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.jarsilio.android.pingoff` / `AppIntro` | `-` | 6 | 208 / 否 | `click` → [6] ImageButton desc="NEXT" id=next (click) center=(981 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.jarsilio.android.pingoff` / `AppIntro` | `-` | 6 | 208 / 否 | `swipe` → [900, 1100] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.jarsilio.android.pingoff` / `AppIntro` | `-` | 6 | 208 / 否 | `swipe` → [950, 1000] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.jarsilio.android.pingoff` / `AppIntro` | `-` | 6 | 208 / 否 | `swipe` → [900, 1074] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.jarsilio.android.pingoff` / `AppIntro` | `-` | 6 | 208 / 否 | `swipe` → [950, 1074] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.jarsilio.android.pingoff` / `AppIntro` | `-` | 6 | 208 / 否 | `swipe` → [1000, 1074] | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.jarsilio.android.pingoff` / `AppIntro` | `-` | 6 | 208 / 否 | `click` → [531, 2090] | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.jarsilio.android.pingoff` / `AppIntro` | `-` | 6 | 208 / 否 | `click` → [574, 2110] | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.jarsilio.android.pingoff/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, PingOf` | `Please select PingOff and check 'Permit usage access' a` | `REQUEST PERMISSION` | `NEXT`
- **Step 2 (`com.jarsilio.android.pingoff/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, PingOf` | `Please select PingOff and check 'Permit usage access' a` | `REQUEST PERMISSION` | `NEXT`
- **Step 3 (`com.jarsilio.android.pingoff/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, PingOf` | `Please select PingOff and check 'Permit usage access' a` | `REQUEST PERMISSION` | `NEXT`
- **Step 4 (`com.jarsilio.android.pingoff/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, PingOf` | `Please select PingOff and check 'Permit usage access' a` | `REQUEST PERMISSION` | `NEXT`
- **Step 5 (`com.jarsilio.android.pingoff/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, PingOf` | `Please select PingOff and check 'Permit usage access' a` | `REQUEST PERMISSION` | `NEXT`
- **Step 6 (`com.jarsilio.android.pingoff/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, PingOf` | `Please select PingOff and check 'Permit usage access' a` | `REQUEST PERMISSION` | `NEXT`
- **Step 7 (`com.jarsilio.android.pingoff/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, PingOf` | `Please select PingOff and check 'Permit usage access' a` | `REQUEST PERMISSION` | `NEXT`
- **Step 8 (`com.jarsilio.android.pingoff/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, PingOf` | `Please select PingOff and check 'Permit usage access' a` | `REQUEST PERMISSION` | `NEXT`

## 中文逐页引导链路解读

> **全链路总结**：应用启动后进入AppIntro引导页，反复展示“Usage Access（使用情况访问）”权限说明并要求请求授权；多次点NEXT、滑动及点分页点均未推进，未触发系统授权或拒绝，链路停滞于引导页。界面无通知/遮罩，话术为功能所需权限说明，未见明显诱导或拒权结果。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文：Usage Access -> 使用情况访问（步骤1-8 AppIntro引导页）
- 英文：In order to know which app is currently running, PingOff needs to have 'Usage Access'. -> 为识别当前正在运行的应用，PingOff需要“使用情况访问”权限（步骤1-8 AppIntro引导页）
- 英文：Please select PingOff and check 'Permit usage access' after tapping on the button below. -> 请点击下方按钮，选择PingOff并勾选“允许使用情况访问”（步骤1-8 AppIntro引导页）
- 英文：REQUEST PERMISSION -> 请求权限（步骤1-8 AppIntro引导页按钮）
- 英文：NEXT -> 下一步（步骤1-8 AppIntro引导页箭头按钮）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AppIntro** | 使用情况访问引导页：英文说明需此权限识别当前应用；点NEXT箭头未生效，页面未跳转，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: AppIntro** | 仍为使用情况访问引导页：英文提示授权并点按钮请求权限；本步左滑分页未推进，仍停原页，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: AppIntro** | 同一使用情况访问引导页：英文要求选择PingOff并勾选允许；本步再次左滑仍未换页，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: AppIntro** | 使用情况访问引导页未变：英文提示点击下方按钮请求权限；本步左滑坐标尝试未跳转，仍停留原页。 | `step_04_action.png` |
| 5 | **Step 5: AppIntro** | 仍停留使用情况访问引导页：英文称需权限识别运行应用；本步全宽左滑未生效，页面未推进，无遮罩。 | `step_05_action.png` |
| 6 | **Step 6: AppIntro** | 同一使用情况访问引导页：英文要求授予使用情况访问；本步右到左滑动仍未翻页，无通知或浮层。 | `step_06_action.png` |
| 7 | **Step 7: AppIntro** | 使用情况访问引导页：英文含请求权限与下一步按钮；本步点第二个分页点未跳转，仍停留原页。 | `step_07_action.png` |
| 8 | **Step 8: AppIntro** | 仍为使用情况访问引导页：英文提示授权以识别当前应用；再点第二个分页点仍未推进，无遮罩/通知。 | `step_08_action.png` |
