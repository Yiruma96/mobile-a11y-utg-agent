# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:46:54
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.rdevzph.fpsmeter`（静态标签：`benign` / `显示调节、截屏与分屏效率` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `6` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.rdevzph.fpsmeter` / `MainActivity` | `-` | 15 | 521 / 否 | `click` → [15] TextView text="Got it" center=(540,2038) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.rdevzph.fpsmeter` / `MainActivity` | `-` | 33 | 575 / 否 | `click` → [32] View (click) center=(1003,171) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.rdevzph.fpsmeter` / `MainActivity` | `-` | 8 | 29 / 否 | `click` → [6] TextView text="Settings" center=(908,589) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.rdevzph.fpsmeter` / `MainActivity` | `-` | 33 | 193 / 否 | `system_button` → Back | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.rdevzph.fpsmeter` / `MainActivity` | `-` | 33 | 575 / 否 | `swipe` → [540, 1800] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.rdevzph.fpsmeter` / `MainActivity` | `-` | 23 | 1185 / 否 | `click` → [5] View (click,unchecked) center=(920,428) | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.rdevzph.fpsmeter` / `MainActivity` | `-` | 25 | 1372 / 否 | `wait` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.rdevzph.fpsmeter` / `MainActivity` | `-` | 25 | 1372 / 否 | `click` → [24] View (click) center=(1003,171) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.rdevzph.fpsmeter/MainActivity`)**: `Close sheet` | `Drag handle` | `What's New` | `v3.6` | `Highlights and improvements in this release` | `Version 3.6` | `Latest` | `Added Swap (Virtual RAM) overlay toggle under the RAM O` | `Fixed root mode detection and switch lockout on KernelS` | `Extended Device Diagnostics to show the active operatin`
- **Step 2 (`com.rdevzph.fpsmeter/MainActivity`)**: `Shizuku (Optional)` | `Overlay Permission` | `Required to show the FPS counter over games. Grant via ` | `Settings` | `FPS Overlay` | `START OVERLAY` | `⚠ Grant overlay permission first` | `Overlay Settings` | `Quick Access & Toggles` | `Floating Assistive Bubble`
- **Step 3 (`com.rdevzph.fpsmeter/MainActivity`)**: `What's New` | `About` | `Settings` | `Donate`
- **Step 4 (`com.rdevzph.fpsmeter/MainActivity`)**: `App Theme` | `Follow System` | `Dark` | `Light` | `Dark AMOLED` | `Pure pitch black (#000000) for OLED screens` | `Language` | `English` | `简体中文` | `Startup`
- **Step 5 (`com.rdevzph.fpsmeter/MainActivity`)**: `Shizuku (Optional)` | `Overlay Permission` | `Required to show the FPS counter over games. Grant via ` | `Settings` | `FPS Overlay` | `START OVERLAY` | `⚠ Grant overlay permission first` | `Overlay Settings` | `Quick Access & Toggles` | `Floating Assistive Bubble`
- **Step 6 (`com.rdevzph.fpsmeter/MainActivity`)**: `Quick Access & Toggles` | `Floating Assistive Bubble` | `Draggable on-screen bubble with a quick menu to start/s` | `Quick Settings Panel Tile` | `Swipe down from your status bar in any game and tap the` | `How it works` | `FPS can be measured using two distinct providers:  • Ch` | `Meter` | `Games` | `History`
- **Step 7 (`com.rdevzph.fpsmeter/MainActivity`)**: `Quick Access & Toggles` | `Floating Assistive Bubble` | `Draggable on-screen bubble with a quick menu to start/s` | `Auto-Hide Bubble & Double-Tap Overlay` | `Hide the floating bubble while the overlay is visible. ` | `Quick Settings Panel Tile` | `Swipe down from your status bar in any game and tap the` | `How it works` | `FPS can be measured using two distinct providers:  • Ch` | `Meter`
- **Step 8 (`com.rdevzph.fpsmeter/MainActivity`)**: `Quick Access & Toggles` | `Floating Assistive Bubble` | `Draggable on-screen bubble with a quick menu to start/s` | `Auto-Hide Bubble & Double-Tap Overlay` | `Hide the floating bubble while the overlay is visible. ` | `Quick Settings Panel Tile` | `Swipe down from your status bar in any game and tap the` | `How it works` | `FPS can be measured using two distinct providers:  • Ch` | `Meter`

## 中文逐页引导链路解读

> **全链路总结**：该应用为帧率悬浮显示工具，启动先弹出版本更新说明浮层，随后进入主界面要求悬浮窗权限与可选的 Shizuku 授权；全程仅有功能说明与开关，未出现诱导弹窗、无取消键遮罩或跳转无障碍授权的强制话术，本机未完成任何授权。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 要求授予悬浮窗权限才能在游戏上显示帧率计数器，可通过 Shizuku（免 root）或手动授予（主界面）
- 英文 -> 悬浮辅助气泡：可拖动气泡，用快捷菜单从任意应用开始/停止游戏帧率录制并切换 HUD 显示（主界面）
- 英文 -> 下拉状态栏点「FPS Meter」磁贴即可在游戏中开关，无需打开本应用（主界面）
- 英文 -> 启动时自动开启悬浮窗（设置页-Startup）
- 英文 -> 权限：请手动或经 Shizuku 授予悬浮窗权限以获得无缝设置体验（工作原理说明区）
- 英文 -> 新增虚拟内存交换叠加开关、修复 KernelSU/APatch 的 root 检测等更新内容（What's New 浮层）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 应用启动弹出「What's New v3.6」更新日志半屏浮层，列虚拟内存叠加等改动，无取消键只有「Got it/知道了」，点击后关闭回到主界面。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 主界面：顶部提示需悬浮窗权限、可用 Shizuku 免 root，有 START OVERLAY 按钮与悬浮气泡开关；本步点右上更多选项，未授权故叠加未启动。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 右上弹出溢出菜单四项：更新、关于、设置、捐赠；本步点击「Settings/设置」，意在寻找无障碍服务入口，菜单内未见该卡片。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 设置页：主题（跟随系统/深色/浅色/纯黑）与语言（English、简体中文）、开机自启；无权限项，点系统返回键退回主界面。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 返回主界面并下滑滚动，页面仍是快速开关与「How it works/工作原理」说明，未出现无障碍服务配置卡，探针未获新授权入口。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 展开说明区介绍 Choreographer/SurfaceFlinger 两种帧率采集与温度监控；本步点开「Floating Assistive Bubble/悬浮辅助气泡」开关，未立即弹权限框。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 开关打开后新增「Auto-Hide Bubble/自动隐藏气泡」条目，界面无弹窗；等待复查是否出现权限或无障碍授权对话框，结果未出现。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 界面与上一步相同，仍未弹权限窗；再次点击右上更多选项，欲从菜单查找无障碍服务设置入口，本次探针未触发任何授权。 | `step_08_action.png` |
