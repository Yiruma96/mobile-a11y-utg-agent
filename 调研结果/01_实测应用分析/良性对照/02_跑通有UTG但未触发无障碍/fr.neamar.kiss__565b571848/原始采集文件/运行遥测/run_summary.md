# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:28:56
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`fr.neamar.kiss`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.google.android.permissioncontroller` / `GrantPermissionsActivity` | `-` | 5 | 53 / 否 | `click` → [4] Button text="Allow" id=permission_allow_button (cli | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `fr.neamar.kiss` / `MainActivity` | `-` | 12 | 223 / 否 | `click` → [12] ImageView desc="Menu" id=menuButton (click) center | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `fr.neamar.kiss` / `MainActivity` | `-` | 3 | 46 / 否 | `click` → [1] TextView text="KISS settings" id=title center=(540, | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `fr.neamar.kiss` / `SettingsActivity` | `-` | 32 | 516 / 否 | `click` → [24] LinearLayout (click) center=(540,1669) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `fr.neamar.kiss` / `SettingsActivity` | `-` | 23 | 367 / 否 | `click` → [23] Switch id=switch_widget (unchecked) center=(972,16 | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `fr.neamar.kiss` / `SettingsActivity` | `-` | 23 | 367 / 否 | `click` → [21] LinearLayout (click) center=(540,1638) | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `fr.neamar.kiss` / `SettingsActivity` | `-` | 23 | 367 / 否 | `click` → [972, 1638] | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `fr.neamar.kiss` / `SettingsActivity` | `-` | 23 | 367 / 否 | `click` → [400, 1638] | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.google.android.permissioncontroller/GrantPermissionsActivity`)**: `Allow KISS launcher to access your contacts?` | `Allow` | `Deny`
- **Step 2 (`fr.neamar.kiss/MainActivity`)**: `Start searching for anything` | `Apps, contacts, settings, …` | `Always see your history` | `For fast access` | `Quick access to most used apps` | `KISS launcher learns from your habits` | `Phone` | `Contacts` | `Chrome` | `Display app list`
- **Step 3 (`fr.neamar.kiss/MainActivity`)**: `KISS settings` | `Update wallpaper…` | `Device settings…`
- **Step 4 (`fr.neamar.kiss/SettingsActivity`)**: `Navigate up` | `KISS settings` | `Search settings` | `Get help` | `Appearance` | `Themes, transparency, colors, icons and shapes` | `Home screen` | `Minimalistic UI, system bars, live wallpaper, …` | `Search bar & keyboard` | `Keyboard behavior, search bar size and buttons, …`
- **Step 5 (`fr.neamar.kiss/SettingsActivity`)**: `Navigate up` | `Gestures` | `Search settings` | `Get help` | `Gestures only work with Minimalistic UI, on empty areas` | `Action on swipe up` | `Display keyboard` | `Action on swipe down` | `Display notification shade` | `Action on swipe left`
- **Step 6 (`fr.neamar.kiss/SettingsActivity`)**: `Navigate up` | `Gestures` | `Search settings` | `Get help` | `Gestures only work with Minimalistic UI, on empty areas` | `Action on swipe up` | `Display keyboard` | `Action on swipe down` | `Display notification shade` | `Action on swipe left`
- **Step 7 (`fr.neamar.kiss/SettingsActivity`)**: `Navigate up` | `Gestures` | `Search settings` | `Get help` | `Gestures only work with Minimalistic UI, on empty areas` | `Action on swipe up` | `Display keyboard` | `Action on swipe down` | `Display notification shade` | `Action on swipe left`
- **Step 8 (`fr.neamar.kiss/SettingsActivity`)**: `Navigate up` | `Gestures` | `Search settings` | `Get help` | `Gestures only work with Minimalistic UI, on empty areas` | `Action on swipe up` | `Display keyboard` | `Action on swipe down` | `Display notification shade` | `Action on swipe left`

## 中文逐页引导链路解读

> **全链路总结**：该应用从系统联系人权限弹窗点击 Allow 进入 KISS 主界面，再经菜单进入 KISS 设置与 Gestures 手势页，多次尝试开启“双击锁屏”开关但未成功。全程未出现通知横幅或遮罩，属于常规极简桌面启动器的权限申请与功能配置链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- English -> 允许 KISS 启动器访问你的联系人吗？（Step 1 系统权限弹窗）
- English -> 开始搜索任何内容：应用、联系人、设置等（Step 2 主界面搜索引导）
- English -> 始终查看历史记录以便快速访问；快速访问常用应用，KISS 会学习你的使用习惯（Step 2 主界面引导）
- English -> 手势仅在极简 UI 的主屏幕空白区域生效；需在 Home screen 设置中开启 Minimalistic UI（Step 5-8 手势设置页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: GrantPermissionsActivity** | 系统联系人权限弹窗，询问是否允许 KISS 访问联系人，含 Allow/Deny；点击 Allow 授权，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | KISS 主界面，展示搜索栏及常用应用/联系人引导；点击右下 Menu 图标进入设置，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 主界面菜单展开，含 KISS settings/Update wallpaper/Device settings；点击 KISS settings 进设置，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: SettingsActivity** | KISS 设置主页，分区含外观、主屏、搜索、历史等；点击一项进入 Gestures 手势设置，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: SettingsActivity** | Gestures 手势设置页，说明仅极简 UI 空白区生效；点击未选中的双击锁屏开关，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: SettingsActivity** | 仍为 Gestures 页，双击锁屏开关未开启；改点整行尝试切换，界面无变化，无通知/遮罩。 | `step_06_action.png` |
| 7 | **Step 7: SettingsActivity** | 仍为 Gestures 页，开关显示未选中；改点开关滑块坐标，仍未开启，无通知/遮罩。 | `step_07_action.png` |
| 8 | **Step 8: SettingsActivity** | 仍为 Gestures 页，双击锁屏开关未选中；再点标签区域，开关仍未开启，无通知/遮罩。 | `step_08_action.png` |
