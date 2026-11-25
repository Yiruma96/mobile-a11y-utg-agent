# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:32:43
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`app.scratchpad.launcher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `8` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 7 | 102 / 否 | `click` → [5] RadioButton (unchecked) center=(898,1278) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.google.android.permissioncontroller` / `RequestRoleActivity` | `-` | 8 | 123 / 否 | `click` → [8] Button text="Set as default" id=button1 (click) cen | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `app.scratchpad.launcher` / `MainActivity` | `-` | 8 | 162 / 否 | `long_press` → [1] EditText text="Scratchpad empty…" id=scratchpad (cl | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `app.scratchpad.launcher` / `MainActivity` | `-` | 27 | 173 / 否 | `swipe` → [540, 1800] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `app.scratchpad.launcher` / `MainActivity` | `-` | 38 | 195 / 否 | `swipe` → [540, 1800] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `app.scratchpad.launcher` / `MainActivity` | `-` | 34 | 197 / 否 | `swipe` → [540, 1800] | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `app.scratchpad.launcher` / `MainActivity` | `-` | 28 | 209 / 否 | `swipe` → [540, 1800] | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `app.scratchpad.launcher` / `MainActivity` | `-` | 28 | 175 / 否 | `click` → [17] Switch id=toggleLock (unchecked) center=(928,1210) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set Scratchpad Launcher as your default home app?` | `Pixel Launcher` | `Scratchpad Launcher` | `Cancel` | `Set as default`
- **Step 2 (`com.google.android.permissioncontroller/RequestRoleActivity`)**: `Set Scratchpad Launcher as your default home app?` | `Pixel Launcher` | `Scratchpad Launcher` | `No permissions needed` | `Cancel` | `Set as default`
- **Step 3 (`app.scratchpad.launcher/MainActivity`)**: `Scratchpad empty…` | `4:32` | `Wed, 25 Nov, 100%` | `App` | `1. Swipe up for all apps 2. Long press anywhere for set` | `lock layout description to be used a unique id to lock `
- **Step 4 (`app.scratchpad.launcher/MainActivity`)**: `Scratchpad Launcher` | `Change default launcher` | `Hidden apps` | `Home screen` | `Apps on home screen` | `3` | `Widget` | `Off` | `Show date time` | `On`
- **Step 5 (`app.scratchpad.launcher/MainActivity`)**: `Widget` | `Off` | `Show date time` | `On` | `Clock at top` | `App alignment` | `Left` | `Space below home apps` | `56 dp` | `App icons`
- **Step 6 (`app.scratchpad.launcher/MainActivity`)**: `Appearance` | `Auto show keyboard` | `Notification bar` | `Theme mode` | `Dark` | `Dim wallpaper` | `0%` | `Text colour` | `Default` | `Text size`
- **Step 7 (`app.scratchpad.launcher/MainActivity`)**: `Clock & date appearance` | `Scratchpad` | `Scratchpad font` | `Sans` | `Link colour` | `#4A90E2` | `Formatting toolbar` | `Scratchpad text size` | `1.0` | `Scratchpad line height`
- **Step 8 (`app.scratchpad.launcher/MainActivity`)**: `Scratchpad line height` | `1.3` | `Sync folder` | `Back up` | `Restore` | `Gestures` | `Swipe left app` | `Camera` | `Swipe right app` | `Phone`

## 中文逐页引导链路解读

> **全链路总结**：应用先通过系统角色对话框被设为默认主屏，进入 Scratchpad 桌面后长按打开设置，连续下滑浏览桌面、外观与便签参数，最终点击“双击锁屏”实验开关。整体为合规的极简桌面配置流程，全程未见诱导话术、通知横幅或遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: RequestRoleActivity** | 系统默认主屏确认页，询问是否将 Scratchpad Launcher 设为默认；本步选中 Scratchpad 单选钮，未确认，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: RequestRoleActivity** | 同一系统角色页，Scratchpad 下显示“无需权限”；本步点击“设为默认”确认主屏，随后进入桌面，无横幅或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | Scratchpad 桌面主页：便签区空、时钟 4:32、周三 25 日 100%、底部 App 与手势提示；本步长按便签区打开设置。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 桌面设置页：含更换默认启动器、隐藏应用、主屏应用数 3、小部件关、显示日期时间开、时钟置顶、图标左对齐；本步下滑。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 设置续页：小部件关、日期时间开、时钟置顶、对齐左、下方间距 56dp、应用图标、表情分类、最近应用、屏幕时间、外观；继续下滑。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 外观设置页：自动弹键盘、通知栏、深色主题、壁纸变暗 0%、文字默认/1.0、应用间距与文字大小、时钟日期外观；本步下滑。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 便签外观页：字体 Sans、链接色 #4A90E2、格式工具栏、文字 1.0/行高 1.3、同步文件夹、备份恢复；本步下滑至手势区。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 手势设置页：左滑相机、右滑电话、双击锁屏（实验性）、主屏列数 2；本步点击未勾选开关，拟启用双击锁屏。 | `step_08_action.png` |
