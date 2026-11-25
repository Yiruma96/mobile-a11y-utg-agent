# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:30:15
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`dev.vulcanlauncher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `8` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `android` / `ResolverActivity` | `-` | 6 | 66 / 否 | `click` → [6] TextView text="Vulcan" id=text1 center=(241,2067) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `dev.vulcanlauncher` / `MainActivity` | `-` | 18 | 151 / 否 | `click` → [18] TextView text="Get started" (click) center=(540,20 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `dev.vulcanlauncher` / `MainActivity` | `-` | 20 | 212 / 否 | `click` → [20] TextView text="Start fresh" (click) center=(540,20 | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `dev.vulcanlauncher` / `MainActivity` | `-` | 14 | 64 / 否 | `click` → [1] LinearLayout desc="Vulcan" (click) center=(972,218) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `dev.vulcanlauncher` / `SettingsActivity` | `-` | 30 | 381 / 否 | `click` → [21] LinearLayout (click) center=(540,1611) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `dev.vulcanlauncher` / `SettingsActivity` | `-` | 30 | 296 / 否 | `click` → [18] LinearLayout (click) center=(540,1407) | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `dev.vulcanlauncher` / `SettingsActivity` | `-` | 15 | 182 / 否 | `click` → [9] TextView text="Recent apps" center=(589,1276) | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `dev.vulcanlauncher` / `SettingsActivity` | `-` | 30 | 307 / 否 | `system_button` → Back | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`android/ResolverActivity`)**: `Use Pixel Launcher as Home` | `Just once` | `Always` | `Use a different app` | `Vulcan`
- **Step 2 (`dev.vulcanlauncher/MainActivity`)**: `Vulcan` | `Gmail` | `Photos` | `Phone` | `Messages` | `Maps` | `Chrome` | `Camera` | `Search` | `Voice search`
- **Step 3 (`dev.vulcanlauncher/MainActivity`)**: `Vulcan` | `Gmail` | `Photos` | `Phone` | `Messages` | `Maps` | `Chrome` | `Camera` | `Search` | `Voice search`
- **Step 4 (`dev.vulcanlauncher/MainActivity`)**: `Vulcan` | `Gmail` | `Photos` | `Phone` | `Messages` | `Maps` | `Chrome` | `Camera` | `Search` | `Voice search`
- **Step 5 (`dev.vulcanlauncher/SettingsActivity`)**: `Back` | `Settings` | `Search settings` | `Vulcan` | `VERSION 0.31.3` | `SETTINGS` | `Home screen` | `Grid, dock, labels, scrolling and widgets` | `App drawer` | `Layout, sorting, hidden apps and groups`
- **Step 6 (`dev.vulcanlauncher/SettingsActivity`)**: `Back` | `Gestures & inputs` | `BUTTON ACTIONS` | `Home button` | `Default page` | `First press goes to the default page, second runs the a` | `GESTURES` | `Swipe up` | `App drawer` | `Swipe down`
- **Step 7 (`dev.vulcanlauncher/SettingsActivity`)**: `Two finger swipe up` | `Nothing` | `App drawer` | `Now page` | `Expand notifications` | `Expand quick settings` | `Toggle notification bar` | `Recent apps` | `Default page` | `Desktop previews`
- **Step 8 (`dev.vulcanlauncher/SettingsActivity`)**: `Back` | `Gestures & inputs` | `BUTTON ACTIONS` | `Home button` | `Default page` | `First press goes to the default page, second runs the a` | `GESTURES` | `Swipe up` | `App drawer` | `Swipe down`

## 中文逐页引导链路解读

> **全链路总结**：应用从系统主屏幕选择器进入 Vulcan 极简桌面，经无网络隐私声明、跳过 Nova 迁移的引导后进入主页；随后在设置中把双指上滑手势改为“Recent apps”，再返回桌面准备测试。全程无通知横幅或遮罩，未出现权限授权弹窗，拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- EN -> 一个没有联网权限的主屏幕，它的任何操作都不会离开你的手机。（Step 2 启动引导页）
- EN -> 把你的主屏幕带过来；选择 Nova 备份即可迁移应用、文件夹、Dock、网格和小组件。（Step 3 导入/恢复页）
- EN -> 首次按下回默认页，再次按下执行动作。（Step 6 手势设置页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ResolverActivity** | 系统主屏幕选择器，询问是否将 Pixel Launcher 设为桌面，并提供仅一次/始终/换应用；本步点击列表中的 Vulcan，未确认默认。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | Vulcan 启动引导页，展示 Gmail、相机等图标，并称无网络访问、数据不会离开手机；本步点“Get started”进入下一步。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 恢复/导入页，提示可从 Nova 备份迁移应用、文件夹、Dock 和小组件，或恢复 Vulcan 备份；本步点“Start fresh”跳过导入。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 进入极简桌面主页，显示 Gmail、照片、电话、信息、地图、Chrome、相机等图标；本步点右上角 Vulcan 图标进入设置。 | `step_04_action.png` |
| 5 | **Step 5: SettingsActivity** | Vulcan 设置主页，列出版本 0.31.3、主屏幕、应用抽屉、文件夹、搜索等项；本步点“手势与输入”入口以配置动作。 | `step_05_action.png` |
| 6 | **Step 6: SettingsActivity** | 手势与输入页，列出 Home 键、滑动上/下及双指滑动动作；本步点“双指上滑”（当前 Nothing）以分配动作。 | `step_06_action.png` |
| 7 | **Step 7: SettingsActivity** | 双指上滑动作选择弹层，列出应用抽屉、Now 页、通知栏、最近任务等及取消；本步选择“Recent apps”，该动作依赖无障碍。 | `step_07_action.png` |
| 8 | **Step 8: SettingsActivity** | 返回手势设置页，可见双指上滑已设为“Recent apps”，其余滑动仍为应用抽屉/展开通知；本步按系统返回键准备回桌面测试。 | `step_08_action.png` |
