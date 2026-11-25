# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:23:31
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.luna.applocker.gp`（静态标签：`malicious` / `TOASTAMIGO` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `1` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.luna.applocker.gp` / `SetPasswordActivity` | `-` | 13 | 22 / 否 | `click` → [2] Button text="1" id=number_button_1 (click) center=( | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.luna.applocker.gp` / `SetPasswordActivity` | `-` | 13 | 22 / 否 | `click` → [3] Button text="2" id=number_button_2 (click) center=( | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.luna.applocker.gp` / `SetPasswordActivity` | `-` | 13 | 22 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.luna.applocker.gp` / `SetPasswordActivity` | `-` | 13 | 22 / 否 | `click` → [4] Button text="3" id=number_button_3 (click) center=( | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.luna.applocker.gp` / `SetPasswordActivity` | `-` | 13 | 22 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.luna.applocker.gp` / `SetPasswordActivity` | `-` | 13 | 22 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.luna.applocker.gp` / `SetPasswordActivity` | `-` | 13 | 22 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.luna.applocker.gp` / `SetPasswordActivity` | `-` | 13 | 22 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.luna.applocker.gp/SetPasswordActivity`)**: `Set password` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9`
- **Step 2 (`com.luna.applocker.gp/SetPasswordActivity`)**: `Set password` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9`
- **Step 3 (`com.luna.applocker.gp/SetPasswordActivity`)**: `Set password` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9`
- **Step 4 (`com.luna.applocker.gp/SetPasswordActivity`)**: `Set password` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9`
- **Step 5 (`com.luna.applocker.gp/SetPasswordActivity`)**: `Set password` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9`
- **Step 6 (`com.luna.applocker.gp/SetPasswordActivity`)**: `Set password` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9`
- **Step 7 (`com.luna.applocker.gp/SetPasswordActivity`)**: `Set password` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9`
- **Step 8 (`com.luna.applocker.gp/SetPasswordActivity`)**: `Set password` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9`

## 中文逐页引导链路解读

> **全链路总结**：应用首次启动进入 SetPasswordActivity，要求设置数字密码；随后通过静态探针依次跳转至无障碍服务 MyAccessibilityService、应用锁应用列表 ApplicationListActivity、卸载广播 UninstallIntentReceiver 与安装广播 PackageInstallReceiver。该链路以“应用锁”为壳，表现出获取无障碍、应用列表及安装卸载感知能力的高风险特征，且页面未见取消或拒绝入口。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “设置密码”（SetPasswordActivity 首次启动密码设置页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: SetPasswordActivity** | 当前为 SetPasswordActivity 数字密码设置页，英文“Set password”意为设置密码；本步点击“1”输入首位，未见通知横幅或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: SetPasswordActivity** | 仍在 SetPasswordActivity 密码设置页，标题“Set password”即设置密码；本步点击“2”继续录入 PIN，无通知与遮罩。 | `step_02_action.png` |
| 3 | **Step 3: SetPasswordActivity** | 同一密码设置页，标题意为“设置密码”；本步为静态探针跳转至 MyAccessibilityService，界面未变，未见授权弹窗或通知。 | `step_03_screen.png` |
| 4 | **Step 4: SetPasswordActivity** | 仍在 SetPasswordActivity 密码页，英文标题意为设置密码；本步点击“3”继续填入密码点，无横幅、遮罩或取消入口。 | `step_04_action.png` |
| 5 | **Step 5: SetPasswordActivity** | 密码设置页标题“Set password”意为设置密码；本步静态跳转探针指向 ApplicationListActivity 应用列表，界面仍停留原页。 | `step_05_screen.png` |
| 6 | **Step 6: SetPasswordActivity** | 仍为 SetPasswordActivity 密码页，标题意为设置密码；本步再次静态跳转至应用列表 ApplicationListActivity，无通知或遮罩。 | `step_06_screen.png` |
| 7 | **Step 7: SetPasswordActivity** | 密码设置页标题意为“设置密码”；本步静态探针跳转至 UninstallIntentReceiver 卸载广播接收器，界面未变、无授权提示。 | `step_07_screen.png` |
| 8 | **Step 8: SetPasswordActivity** | 同一 SetPasswordActivity 密码页，标题意为设置密码；本步静态探针跳转至 PackageInstallReceiver 安装广播接收器，无通知/遮罩。 | `step_08_screen.png` |
