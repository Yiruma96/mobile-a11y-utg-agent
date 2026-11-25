# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:56:11
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.pedronveloso.a11ybutton`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 3 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 3 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_03_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.pedronveloso.a11ybutton/com.pedronveloso.a11ybutton.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Setup needed / 3 steps left / Accessibility disclosure / Accessibility service / Turn it on in Accessibility settings so the button can work.`
- **Back 后 +5.5s**：`com.pedronveloso.a11ybutton/com.pedronveloso.a11ybutton.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Setup needed / 3 steps left / Accessibility disclosure / Accessibility service / Turn it on in Accessibility settings so the button can work.`
- **Back 后 +10.5s**：`com.pedronveloso.a11ybutton/com.pedronveloso.a11ybutton.MainActivity` | hooks=`[]` | overlays=`0` | texts=`Setup needed / 3 steps left / Accessibility disclosure / Accessibility service / Turn it on in Accessibility settings so the button can work.`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.pedronveloso.a11ybutton` / `MainActivity` | `-` | 11 | 480 / 否 | `click` → [10] View (click) center=(540,2038) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.pedronveloso.a11ybutton` / `MainActivity` | `-` | 22 | 486 / 否 | `click` → [6] View (click) center=(540,817) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 228 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_03_layout.xml` + `step_03_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.pedronveloso.a11ybutton/MainActivity`)**: `Step 1 of 4` | `Skip setup` | `One button, one app` | `Once you enable Android’s Accessibility button and choo` | `Accessibility button at the bottom right of Android’s n` | `Navigation bar button` | `Accessibility button floating at the right edge of the ` | `Accept and continue`
- **Step 2 (`com.pedronveloso.a11ybutton/MainActivity`)**: `Setup needed` | `3 steps left` | `Accessibility disclosure` | `Accessibility service` | `Turn it on in Accessibility settings so the button can ` | `What the button opens` | `Choose the app or shortcut the button opens.` | `Unrestricted battery` | `Stops your phone from putting the service to sleep.` | `Button action`
- **Step 3 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Accessibility Button Launcher` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以4步引导让用户接受无障碍按钮启动器，随后跳转系统无障碍设置并弹出“完全控制设备”高危授权；点击拒绝后仍反复回到设置待办页，无跳过或退出，表现为拒权即滞留的诱导链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “一个按钮，一个应用；启用后可在其他应用中打开所选应用或快捷方式”（Step 1 主引导页）
- 英文 -> “无障碍披露：需在设置中开启服务，按钮才能工作”（Step 2 设置待办页）
- 英文 -> “不受限电池：防止系统休眠该服务”（Step 2 设置待办页）
- 英文 -> “按钮动作：尚未分配；请选择应用或应用内快捷方式供按下时打开”（Step 2 设置待办页）
- 英文 -> “允许Accessibility Button Launcher完全控制设备？适用于无障碍需求，不适用于多数应用”（系统警告弹窗）
- 英文 -> “查看并控制屏幕：可读取全部屏幕内容并覆盖其他应用显示”（系统警告弹窗）
- 英文 -> “查看并执行操作：可追踪与应用的交互并代表你操作”（系统警告弹窗）
- 英文 -> “从无障碍按钮或快捷方式启动所选应用”（服务详情页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 应用引导第1/4步，宣称“一个按钮，一个应用”，展示无障碍按钮位于导航栏或屏幕边缘，点击“接受并继续”进入下一步。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 设置待办页称还需3步，分无障碍服务、按钮打开对象、电池不限三项；点击“无障碍服务”卡片，准备跳系统设置。 | `step_02_action.png` |
| 3 | **Step 3: [无障碍列表页]** | 跳转系统无障碍列表，见“Accessibility Button Launcher”处于关闭；探针命中无障碍设置钩子后自动终止，未执行授权。 | `step_03_screen.png` |
| 4 | **跳后探针 +0.8s** | 跳转后0.8秒探针，仍停留在系统无障碍设置页，未发现弹窗或悬浮遮罩，等待未操作。 | `step_03_probe_800ms_screen.png` |
| 5 | **跳后探针 +2.0s** | 跳转后2.0秒探针，仍停留在系统无障碍设置页，未发现弹窗或悬浮遮罩，等待未操作。 | `step_03_probe_2000ms_screen.png` |
| 6 | **服务详情页** | 应用无障碍服务详情页，选项显示快捷方式关闭；说明“通过无障碍按钮或快捷方式启动所选应用”，本步仅检查未操作。 | `step_03_service_detail_screen.png` |
| 7 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗警告“完全控制设备”，列出读取屏幕、显示悬浮窗、追踪交互并以应用代操作；提供允许/拒绝。 | `step_03_system_warning_screen.png` |
| 8 | **拒权返回 +2.0s** | 点“拒绝”返回应用后仍停在“设置待办/3步剩余”页，反复要求开启无障碍服务，未提供跳过或退出，形成拒权滞留。 | `step_03_refusal_2000ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权10.5秒后仍停留在同一设置待办页，无障碍服务项与“3步剩余”持续催促，无取消/退出路径，确认被困于诱导页。 | `step_03_refusal_10500ms_screen.png` |
