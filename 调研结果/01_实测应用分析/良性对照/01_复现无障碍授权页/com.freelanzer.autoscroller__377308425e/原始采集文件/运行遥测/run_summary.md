# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:44:25
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.freelanzer.autoscroller`（静态标签：`benign` / `系统效率与通用辅助` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `7` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.freelanzer.autoscroller/com.freelanzer.autoscroller.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Accessibility service disabled / To use AutoScroller you need to enable its accessibility service. Tap the button below, find "AutoScroller" in the list and turn on the toggle. / Open Accessibility Settings / Auto-scroll / Interval: 4 s`
- **Back 后 +5.5s**：`com.freelanzer.autoscroller/com.freelanzer.autoscroller.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Accessibility service disabled / To use AutoScroller you need to enable its accessibility service. Tap the button below, find "AutoScroller" in the list and turn on the toggle. / Open Accessibility Settings / Auto-scroll / Interval: 4 s`
- **Back 后 +10.5s**：`com.freelanzer.autoscroller/com.freelanzer.autoscroller.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Accessibility service disabled / To use AutoScroller you need to enable its accessibility service. Tap the button below, find "AutoScroller" in the list and turn on the toggle. / Open Accessibility Settings / Auto-scroll / Interval: 4 s`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.freelanzer.autoscroller` / `MainActivity` | `-` | 10 | 884 / 否 | `click` → [8] View (click) center=(540,1799) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 255 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.freelanzer.autoscroller/MainActivity`)**: `AutoScroller automates scrolling in vertical-video apps` | `License` | `This software is distributed under the Apache 2.0 licen` | `Digital wellbeing notice` | `Prolonged use of vertical-video content can affect your` | `Data and privacy` | `AutoScroller stores usage statistics —duration of each ` | `Accept and continue` | `Before you start`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `AutoScroller` | `Off / Automatic scrolling for vertical video` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：该应用从 EULA 入口以“提升无障碍与数字福祉、仅本地统计、不读取内容”等话术取得信任，随后引导进入系统无障碍列表、服务详情和“完全控制设备”警告。用户拒绝授权后，应用反复回到“无障碍服务已禁用”主页，只保留“打开无障碍设置”诱导按钮，缺少跳过或退出路径，形成 TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 自动化竖屏视频滚动以提升无障碍与数字福祉（入口 EULA）
- 英文 -> 长时间观看竖屏内容可能影响福祉，建议设置健康时限（入口 EULA）
- 英文 -> 使用统计仅保存在本机、不传服务器、不共享、不访问观看内容；未来云同步也需明确同意（入口 EULA）
- 英文 -> AutoScroller 仅执行滚动手势，不读取、存储或传输你的内容（服务详情页）
- 英文 -> 允许 AutoScroller 完全控制设备；该权限适合无障碍需求，但不适合多数应用（系统警告弹窗）
- 英文 -> 可查看并控制屏幕、读取屏幕全部内容并覆盖显示在其他应用上（系统警告弹窗）
- 英文 -> 可追踪你与应用或硬件传感器的交互，并代表你操作应用（系统警告弹窗）
- 英文 -> 无障碍服务已禁用，必须点击按钮找到 AutoScroller 并开启开关才能使用（拒权返回页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 入口 EULA 首页：以自动化滚动、无障碍与数字福祉、本地统计和隐私承诺安抚用户；点击“Accept and continue”继续。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表：显示“AutoScroller 关闭/自动滚动竖屏视频”条目，作为授权入口；捕获无障碍钩子后自动终止。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 授权列表跳后0.8秒探针：仍停留无障碍设置页，UI文本为空、遮罩0，未见弹窗或通知横幅。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后2.0秒探针：仍在无障碍设置页，界面无文本、遮罩0，无额外授权提示或系统弹窗。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页：说明 AutoScroller 用于 Reels/TikTok/Shorts，仅执行滚动手势、不读取存储传输内容；含使用开关与快捷方式。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统“完全控制”警告：列明可查看控制屏幕、读取全部内容、覆盖显示及追踪交互；本步查看警告，拒绝后回应用。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回+2秒：应用主页显示“无障碍服务已禁用”，要求去设置开启 AutoScroller；无跳过或退出，停留于诱导页。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +10.5s** | 拒权返回+10.5秒：仍卡在“无障碍已禁用”主页，重复“打开无障碍设置”按钮和预览计数；无逃逸路径。 | `step_02_refusal_10500ms_screen.png` |
