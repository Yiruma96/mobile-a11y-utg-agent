# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:43:20
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.deehem.splitz`（静态标签：`benign` / `显示调节、截屏与分屏效率` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `4` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.deehem.splitz/com.deehem.splitz.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Automation Service Disabled / Requires offline Accessibility permission to automate split screens. / Enable / Prevent Background Kills / Exempt Splitz from battery optimization to keep automation instant.`
- **Back 后 +5.5s**：`com.deehem.splitz/com.deehem.splitz.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Automation Service Disabled / Requires offline Accessibility permission to automate split screens. / Enable / Prevent Background Kills / Exempt Splitz from battery optimization to keep automation instant.`
- **Back 后 +10.5s**：`com.deehem.splitz/com.deehem.splitz.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Automation Service Disabled / Requires offline Accessibility permission to automate split screens. / Enable / Prevent Background Kills / Exempt Splitz from battery optimization to keep automation instant.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.deehem.splitz` / `MainActivity` | `-` | 15 | 358 / 否 | `click` → [4] TextView text="Enable" center=(917,400) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.deehem.splitz/MainActivity`)**: `Automation Service Disabled` | `Requires offline Accessibility permission to automate s` | `Enable` | `Prevent Background Kills` | `Exempt Splitz from battery optimization to keep automat` | `Later` | `Exempt` | `Create Your First Split-Screen Shortcut` | `Tap the + icon below to pair two apps, assign a folder,` | `Splitz`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Splitz` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用入口 MainActivity 以「自动化服务未启用」卡片引导开启离线无障碍与电池优化豁免，跳转系统无障碍列表及 Splitz 服务详情，触发系统全控制警告；拒绝后无崩溃或强制循环，静默返回主页并降级为普通分屏快捷方式，整体属合规工具型引导。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 需开启离线无障碍权限以实现自动分屏（MainActivity）
- 英文 -> 将 Splitz 排除电池优化以保持自动化即时生效（MainActivity）
- 英文 -> 声称无障碍服务仅用于自动将所选应用对放入分屏（服务详情页）
- 英文 -> 强调完全离线、不读取/收集/传输屏幕内容、按键或个人数据（服务详情页）
- 英文 -> 系统警告称允许 Splitz 完全控制设备，多数应用不适用（系统警告弹窗）
- 英文 -> 引导点击 + 图标配对两个应用、分配文件夹并固定到主屏（MainActivity）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 主界面：自动化服务禁用卡片引导点 Enable 开无障碍，提示电池优化豁免并引导新建分屏快捷方式；本步点击 Enable，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表：DOWNLOADED APPS 下 Splitz 显示 Off，含屏幕阅读器与显示项；采集到无障碍设置 Hook/探针后自动终止，无通知/遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后 +0.8s 探针：仍处系统无障碍设置页，无可见文案与操作，遮罩计数 0、无通知横幅，等待观察无弹窗。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后 +2.0s 探针：仍停留系统无障碍设置页，无新增文案或弹窗，遮罩计数 0、无通知，未发生强制跳转。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | Splitz 无障碍服务详情：Use Splitz 与 Splitz shortcut 均关闭；说明称仅用于自动分屏、完全离线且不采集数据；本步仅检查详情。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统全控制警告：称允许 Splitz 完全控制设备，多数应用不适用；列明可查看/控制屏幕与代操作；本步检查警告并点 Deny，遮罩 0。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒绝授权后 +2.0s：已回 MainActivity，仍显示自动化禁用卡片与 Enable/Later/Exempt，未崩溃或循环；状态为优雅停留/降级。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒绝后 +10.5s：主界面保持稳定，未反复弹窗或强制跳转；仅保留启用引导，属优雅降级，无通知与遮罩。 | `step_02_refusal_10500ms_screen.png` |
