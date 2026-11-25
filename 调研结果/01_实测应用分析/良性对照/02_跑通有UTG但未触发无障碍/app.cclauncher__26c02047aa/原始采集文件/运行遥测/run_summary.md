# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:35:16
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`app.cclauncher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `app.cclauncher` / `MainActivity` | `-` | 0 | 0 / 否 | `long_press` → [540, 1000] | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `app.cclauncher` / `MainActivity` | `-` | 33 | 367 / 否 | `swipe` → [540, 1800] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `app.cclauncher` / `MainActivity` | `-` | 36 | 580 / 否 | `swipe` → [540, 1800] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `app.cclauncher` / `MainActivity` | `-` | 34 | 336 / 否 | `swipe` → [540, 1800] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `app.cclauncher` / `MainActivity` | `-` | 36 | 382 / 否 | `click` → [36] View desc="Search settings" center=(1003,88) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `app.cclauncher` / `MainActivity` | `-` | 35 | 374 / 否 | `type` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `app.cclauncher` / `MainActivity` | `-` | 33 | 337 / 否 | `system_button` → Enter | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `app.cclauncher` / `MainActivity` | `-` | 33 | 337 / 否 | `click` → [33] View desc="Clear search" center=(992,88) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`app.cclauncher/MainActivity`)**: (空文本)
- **Step 2 (`app.cclauncher/MainActivity`)**: `General` | `Show App Names` | `Show Names in Search After` | `0` | `Show app names in search results after typing this many` | `Show Pinned Shortcuts` | `Display pinned app shortcuts in the app drawer.` | `Show App Drawer Icons` | `Auto Show Keyboard` | `Show Hidden in Search`
- **Step 3 (`app.cclauncher/MainActivity`)**: `Auto Open Single Matches` | `Search Type` | `Contains` | `Return to Home After App` | `Return to home screen instead of search after closing a` | `Default Screen` | `Home` | `Choose which screen to show when opening the launcher` | `Search Sort Order` | `Alphabetical`
- **Step 4 (`app.cclauncher/MainActivity`)**: `Tap to Open in App Drawer` | `When disabled, tapping an app drawer app does nothing. ` | `Show Web Search Option` | `Show 'Search Web' button when no apps match` | `Appearance` | `Language` | `System` | `Theme` | `Dark` | `Home Text Size`
- **Step 5 (`app.cclauncher/MainActivity`)**: `Select a custom font file` | `Use Dynamic Theme` | `Screen Orientation` | `System Default` | `Item Spacing` | `Small` | `Search Results Use Home Font Size` | `Use the same font size for search results as home scree` | `Search Results Font Size` | `1.0`
- **Step 6 (`app.cclauncher/MainActivity`)**: `Select a custom font file` | `Use Dynamic Theme` | `Screen Orientation` | `System Default` | `Item Spacing` | `Small` | `Search Results Use Home Font Size` | `Use the same font size for search results as home scree` | `Search Results Font Size` | `1.0`
- **Step 7 (`app.cclauncher/MainActivity`)**: `Private Space` | `Requires Android 15 or higher` | `System` | `Set as Default Launcher` | `CCLauncher is not default` | `Lock Settings` | `Prevent changes to settings without a PIN` | `Hidden Apps` | `App Info` | `About CCLauncher`
- **Step 8 (`app.cclauncher/MainActivity`)**: `Private Space` | `Requires Android 15 or higher` | `System` | `Set as Default Launcher` | `CCLauncher is not default` | `Lock Settings` | `Prevent changes to settings without a PIN` | `Hidden Apps` | `App Info` | `About CCLauncher`

## 中文逐页引导链路解读

> **全链路总结**：CCLauncher 从空白主桌面长按进入设置，随后在 General 与 Appearance 中滚动并尝试用设置搜索定位“Double-tap to lock”，但未命中，最终回到设置主页；全程未触发授权/拒权、通知或悬浮遮罩，表现为常规启动器配置流程。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 空白主桌面，无可见文字、通知或遮罩；长按桌面空白处[540,1000]，尝试打开启动器设置入口。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 设置“General”页，含显示应用名、搜索显示名、固定快捷方式等英文项；向下滑动查找“双击锁屏”，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 设置继续下滚，显示搜索类型、默认屏幕、搜索排序与别名匹配说明；仍未出现双击锁屏项，无通知或遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 设置下滚至外观相关项：语言、主题、主屏文字大小、字体粗细等；说明点击应用抽屉行为；无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 设置外观页含自定义字体、动态主题、屏幕方向、图标圆角等；点击右上“搜索设置”图标，未见双击锁屏项。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 仍在设置外观页，聚焦搜索框并输入“Double-tap to lock”（双击锁屏）；界面未显示新结果，无通知/遮罩。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 按回车提交搜索后回到设置主页，显示私有空间、设为默认启动器、锁定设置、隐藏应用、备份等项；无匹配结果。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 设置主页停留，显示“CCLauncher 非默认”、版本 v10.7.20 与导出设置；点击“清除搜索”返回，无通知/遮罩。 | `step_08_action.png` |
