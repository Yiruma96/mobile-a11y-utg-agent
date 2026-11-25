# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:52:40
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.farmerbb.taskbar`（静态标签：`benign` / `系统效率与通用辅助` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.farmerbb.taskbar` / `MainActivity` | `-` | 12 | 276 / 否 | `click` → [8] TextView text="Advanced features" id=title center=( | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.farmerbb.taskbar` / `MainActivity` | `-` | 24 | 639 / 否 | `click` → [10] CheckBox id=checkbox (unchecked) center=(992,678) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.farmerbb.taskbar` / `MainActivity` | `-` | 24 | 639 / 否 | `click` → [16] TextView text="Navigation bar buttons" id=title ce | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.farmerbb.taskbar` / `NavigationBarButtonsActivity` | `-` | 7 | 37 / 否 | `click` → [3] CheckBox id=checkbox (unchecked) center=(826,1030) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.farmerbb.taskbar` / `NavigationBarButtonsActivity` | `-` | 7 | 37 / 否 | `click` → [5] CheckBox id=checkbox (unchecked) center=(826,1177) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.farmerbb.taskbar` / `NavigationBarButtonsActivity` | `-` | 7 | 37 / 否 | `system_button` → Back | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.farmerbb.taskbar` / `MainActivity` | `-` | 24 | 639 / 否 | `click` → [10] CheckBox id=checkbox (checked) center=(992,678) | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.farmerbb.taskbar` / `MainActivity` | `-` | 24 | 639 / 否 | `click` → [16] TextView text="Navigation bar buttons" id=title ce | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.farmerbb.taskbar/MainActivity`)**: `Taskbar` | `General settings` | `Appearance` | `Recent apps` | `Freeform mode` | `Desktop mode` | `Advanced features` | `About Taskbar` | `Taskbar: PC-style productivity for Android  © 2024 Brad` | `See what's new in this release`
- **Step 2 (`com.farmerbb.taskbar/MainActivity`)**: `Navigate up` | `Advanced features` | `Replace home screen` | `Use Taskbar as a home screen replacement` | `Enable keyboard shortcuts` | `Start/stop Taskbar:    + M    + M  Lock device:    +` | `Enable widget support` | `Add a button to the Taskbar that displays widgets when ` | `Widget dashboard grid size` | `2 × 2`
- **Step 3 (`com.farmerbb.taskbar/MainActivity`)**: `Navigate up` | `Advanced features` | `Replace home screen` | `Use Taskbar as a home screen replacement` | `Enable keyboard shortcuts` | `Start/stop Taskbar:    + M    + M  Lock device:    +` | `Enable widget support` | `Add a button to the Taskbar that displays widgets when ` | `Widget dashboard grid size` | `2 × 2`
- **Step 4 (`com.farmerbb.taskbar/NavigationBarButtonsActivity`)**: `Navigation bar buttons` | `Back` | `Home` | `Recents`
- **Step 5 (`com.farmerbb.taskbar/NavigationBarButtonsActivity`)**: `Navigation bar buttons` | `Back` | `Home` | `Recents`
- **Step 6 (`com.farmerbb.taskbar/NavigationBarButtonsActivity`)**: `Navigation bar buttons` | `Back` | `Home` | `Recents`
- **Step 7 (`com.farmerbb.taskbar/MainActivity`)**: `Navigate up` | `Advanced features` | `Replace home screen` | `Use Taskbar as a home screen replacement` | `Enable keyboard shortcuts` | `Start/stop Taskbar:    + M    + M  Lock device:    +` | `Enable widget support` | `Add a button to the Taskbar that displays widgets when ` | `Widget dashboard grid size` | `2 × 2`
- **Step 8 (`com.farmerbb.taskbar/MainActivity`)**: `Navigate up` | `Advanced features` | `Replace home screen` | `Use Taskbar as a home screen replacement` | `Enable keyboard shortcuts` | `Start/stop Taskbar:    + M    + M  Lock device:    +` | `Enable widget support` | `Add a button to the Taskbar that displays widgets when ` | `Widget dashboard grid size` | `2 × 2`

## 中文逐页引导链路解读

> **全链路总结**：该应用从 Taskbar 主设置页进入高级功能，围绕键盘快捷键、导航栏按钮等系统辅助能力反复开关与进入子对话框；未见强制授权、通知横幅或遮罩，整体为正常系统效率工具的功能引导。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> 中文意译：Taskbar：面向 Android 的 PC 风格生产力（Step 1 主页面）
- 英文 -> 中文意译：点击此处检查更新或留下评分！😁（Step 1 主页面）
- 英文 -> 中文意译：查看此版本的新内容（Step 1 主页面）
- 英文 -> 中文意译：需在设置中将 Taskbar 设为辅助应用（Step 2/3/7/8 高级功能页）
- 英文 -> 中文意译：禁用可提升安全性（Step 2/3/7/8 高级功能页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | Taskbar主设置页，列常规、外观、最近应用、自由/桌面模式与高级功能；本步点击“Advanced features”进入高级选项，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 高级功能页：替换主屏、键盘快捷键、小部件、导航栏按钮等；本步勾选“Enable keyboard shortcuts”，见辅助应用依赖提示，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 仍为高级功能页；键盘快捷键已启用，本步点击“Navigation bar buttons”进入导航栏按钮子页，无通知横幅与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: NavigationBarButtonsActivi** | 导航栏按钮子页/对话框，列出 Back、Home、Recents 三个可选按钮；本步勾选“Back”复选框以触发无障碍相关配置，无通知或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: NavigationBarButtonsActivi** | 同一导航栏按钮子页；Back 已勾选，本步尝试勾选“Home”，继续探测按钮配置是否触发权限/无障碍流程，无通知或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: NavigationBarButtonsActivi** | 导航栏按钮子页已配置；本步按系统返回键关闭该子页，准备返回高级功能页继续试探，无通知横幅或遮罩。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 返回高级功能页；本步点击已勾选的“Enable keyboard shortcuts”以关闭/重开该开关，尝试再次触发无障碍授权流程，无通知或遮罩。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 仍为高级功能页；本步再次点击“Navigation bar buttons”重开导航栏按钮子页，确认其依赖无障碍服务的行为，无通知或遮罩。 | `step_08_action.png` |
