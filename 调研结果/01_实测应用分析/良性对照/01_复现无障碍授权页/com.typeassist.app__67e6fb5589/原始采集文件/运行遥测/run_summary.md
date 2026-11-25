# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:01:23
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.typeassist.app`（静态标签：`benign` / `残障辅助与无障碍支持` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.typeassist.app/com.typeassist.app.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Permissions / TypeAssist works best with these permissions. / REQUIRED / Accessibility Service / Required to read and replace text.`
- **Back 后 +5.5s**：`com.typeassist.app/com.typeassist.app.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Permissions / TypeAssist works best with these permissions. / REQUIRED / Accessibility Service / Required to read and replace text.`
- **Back 后 +10.5s**：`com.typeassist.app/com.typeassist.app.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Permissions / TypeAssist works best with these permissions. / REQUIRED / Accessibility Service / Required to read and replace text.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.typeassist.app` / `MainActivity` | `-` | 7 | 107 / 否 | `click` → [6] View (click) center=(540,1837) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.typeassist.app` / `MainActivity` | `-` | 12 | 210 / 否 | `click` → [4] View (click) center=(540,646) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 212 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.typeassist.app/MainActivity`)**: `Welcome to` | `TypeAssist` | `AI is thinking` | `Live Preview` | `Type anywhere, add a trigger, and let AI handle the res` | `Next`
- **Step 2 (`com.typeassist.app/MainActivity`)**: `Permissions` | `TypeAssist works best with these permissions.` | `REQUIRED` | `Accessibility Service` | `Required to read and replace text.` | `RECOMMENDED FOR STABILITY` | `Ignore Battery Opt.` | `Prevent system from killing the app.` | `Get Started`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `TypeAssist AI` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以“TypeAssist AI 输入增强”欢迎页引导用户进入权限页，将无障碍服务标为必需并跳转系统设置；在系统“完全控制设备”警告处拒绝后，应用仍反复回到权限诱导页并卡住，形成 TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 在任何地方输入，添加触发词，让 AI 处理其余内容（欢迎页）
- 英文 -> TypeAssist 在这些权限下效果最佳（权限页）
- 英文 -> 读取并替换文本所必需（权限页）
- 英文 -> 防止系统杀死应用（权限页）
- 英文 -> 允许 TypeAssist AI 完全控制你的设备？（系统警告弹窗）
- 英文 -> 完全控制适用于帮助无障碍需求的 app，但大多数应用不适用（系统警告弹窗）
- 英文 -> 可读取屏幕上所有内容并在其他应用上显示内容（系统警告弹窗）
- 英文 -> 可跟踪你与 app 或硬件传感器的交互，并代表你操作 app（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 欢迎页展示 TypeAssist 与 AI is thinking，称可在任意处输入并由 AI 处理；点击 Next 进入引导，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 权限页将无障碍服务标为 REQUIRED，称用于读取替换文本，电池优化为稳定性推荐；点击无障碍服务卡，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 系统无障碍列表页显示 TypeAssist AI 为 Off；捕获无障碍设置 Hook 与探针后自动终止，无通知/遮罩，尚未开启服务。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针仍停留在系统无障碍设置页，界面无可读文本，overlays=0、无通知，未出现额外弹窗。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针仍在系统无障碍设置页，无新增文本与通知，overlays=0，状态未变化。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | TypeAssist AI 服务详情页显示 Use TypeAssist AI 开关及快捷方式选项仍为 Off；仅检查详情，无通知/遮罩。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统警告弹窗询问是否允许 TypeAssist AI 完全控制设备，列明可读屏、覆盖显示与代替操作；有 Allow/Deny，overlays=0。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 在警告弹窗拒绝/返回后 2 秒，应用回到权限页，仍将无障碍服务标为 REQUIRED 并卡住；无通知/遮罩，形成诱导页陷阱。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回 10.5 秒后仍停留在同一权限诱导页，无障碍服务仍标 REQUIRED，无通知/遮罩，未提供继续退出路径。 | `step_03_refusal_10500ms_screen.png` |
