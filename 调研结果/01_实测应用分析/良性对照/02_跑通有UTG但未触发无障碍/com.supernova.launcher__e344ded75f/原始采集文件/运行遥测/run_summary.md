# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:36:22
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.supernova.launcher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `android` / `ResolverActivity` | `-` | 2 | 32 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `android` / `ResolverActivity` | `-` | 2 | 32 / 否 | `system_button` → Back | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `android` / `ResolverActivity` | `-` | 2 | 32 / 否 | `system_button` → Home | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `android` / `ResolverActivity` | `-` | 2 | 32 / 否 | `click` → [330, 804] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `android` / `ResolverActivity` | `-` | 6 | 69 / 否 | `click` → [6] TextView text="Supernova" id=text1 center=(279,2067 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.supernova.launcher` / `OnboardingActivity` | `-` | 14 | 160 / 否 | `click` → [14] TextView text="Skip setup" id=welcomeSkip (click)  | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.supernova.launcher` / `LauncherActivity` | `-` | 20 | 76 / 否 | `click` → [3] LinearLayout desc="Supernova Settings" (click) cent | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.supernova.launcher` / `SettingsLauncherAlias` | `-` | 27 | 255 / 否 | `swipe` → [540, 1700] | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`android/ResolverActivity`)**: `No apps can perform this action.`
- **Step 2 (`android/ResolverActivity`)**: `No apps can perform this action.`
- **Step 3 (`android/ResolverActivity`)**: `No apps can perform this action.`
- **Step 4 (`android/ResolverActivity`)**: `No apps can perform this action.`
- **Step 5 (`android/ResolverActivity`)**: `Use Pixel Launcher as Home` | `Just once` | `Always` | `Use a different app` | `Supernova`
- **Step 6 (`com.supernova.launcher/OnboardingActivity`)**: `Previous` | `Skip` | `Supernova Settings` | `Gmail` | `Photos` | `Search` | `Voice search` | `Next` | `Welcome to` | `Supernova`
- **Step 7 (`com.supernova.launcher/LauncherActivity`)**: `Supernova Settings` | `Gmail` | `Photos` | `Phone` | `Messages` | `Maps` | `Chrome` | `Camera` | `Search` | `Voice search`
- **Step 8 (`com.supernova.launcher/SettingsLauncherAlias`)**: `Settings` | `Search settings` | `Set as default launcher` | `Complete action` | `Screens` | `Home screen` | `Grid, icons, labels and pages` | `Dock` | `Icons, background and pages` | `App drawer`

## 中文逐页引导链路解读

> **全链路总结**：应用启动后先被系统 Resolver 的“无应用可执行此操作”错误页卡住，多次返回、回桌面和坐标点击后，在解析器中选择 Supernova 进入引导页；跳过设置后进入极简桌面，再打开应用设置准备查找手势/锁屏项。全程未见明显诱导话术、通知横幅或遮罩，也未观察到权限索取。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- Welcome to Supernova -> 欢迎来到 Supernova（Step 6 引导页标题）
- Infinitely customisable homescreen -> 无限可定制的主屏（Step 6 引导页说明）
- Design my homescreen -> 设计我的主屏（Step 6 引导页按钮）
- Restore backup -> 恢复备份（Step 6 引导页按钮）
- Skip setup -> 跳过设置（Step 6 引导页按钮）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: ResolverActivity** | 系统解析器错误页，仅显示“无应用可执行此操作”；无通知与遮罩，本步执行打开操作后仍停留该错误页。 | `step_01_action.png` |
| 2 | **Step 2: ResolverActivity** | 仍是系统解析器错误页，文案同为“无应用可执行此操作”；本步按返回键尝试关闭卡住的弹窗，未见权限请求。 | `step_02_action.png` |
| 3 | **Step 3: ResolverActivity** | 系统解析器错误页持续存在，显示“无应用可执行此操作”；本步按 Home 键退出以解除卡顿，页面无通知横幅。 | `step_03_action.png` |
| 4 | **Step 4: ResolverActivity** | 系统解析器错误页，仍提示“无应用可执行此操作”；本步坐标点击尝试选择默认主屏选项，界面文本尚未更新。 | `step_04_action.png` |
| 5 | **Step 5: ResolverActivity** | 系统主屏选择弹窗，列出“将 Pixel Launcher 设为主屏/仅一次/始终/使用其他应用/Supernova”；本步点选 Supernova 返回目标应用。 | `step_05_action.png` |
| 6 | **Step 6: OnboardingActivity** | Supernova 引导页，含“欢迎来到 Supernova、无限可定制主屏、设计我的主屏、恢复备份、跳过设置”；本步点“跳过设置”。 | `step_06_action.png` |
| 7 | **Step 7: LauncherActivity** | 进入极简桌面主页，显示 Supernova 设置图标及 Gmail、照片、电话、信息、地图、Chrome、相机等；本步点击“Supernova 设置”。 | `step_07_action.png` |
| 8 | **Step 8: SettingsLauncherAlias** | 应用设置页，含“设为默认桌面、完成操作、屏幕/主屏/停靠栏/应用抽屉/文件夹/信息流”等；本步向下滑动查找手势与锁屏项。 | `step_08_action.png` |
