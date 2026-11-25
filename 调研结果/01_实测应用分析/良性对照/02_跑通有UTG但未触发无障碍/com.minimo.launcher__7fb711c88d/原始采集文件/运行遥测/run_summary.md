# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:34:00
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.minimo.launcher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `7` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.minimo.launcher` / `MainActivity` | `-` | 4 | 54 / 否 | `click` → [3] View (click) center=(540,2071) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.minimo.launcher` / `MainActivity` | `-` | 36 | 107 / 否 | `click` → [7] View (click,unchecked) center=(920,545) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.minimo.launcher` / `MainActivity` | `-` | 36 | 89 / 否 | `click` → [36] TextView text="Continue" center=(540,2071) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.minimo.launcher` / `MainActivity` | `-` | 6 | 90 / 否 | `click` → [6] TextView text="Skip" center=(540,1319) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.minimo.launcher` / `MainActivity` | `-` | 2 | 8 / 否 | `long_press` → [540, 1700] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.minimo.launcher` / `MainActivity` | `-` | 9 | 96 / 否 | `click` → [3] TextView text="Customization" (click) center=(540,6 | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.minimo.launcher` / `MainActivity` | `-` | 42 | 395 / 否 | `click` → [42] View desc="Back" center=(77,171) | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.minimo.launcher` / `MainActivity` | `-` | 9 | 96 / 否 | `click` → [3] TextView text="Customization" (click) center=(540,6 | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.minimo.launcher/MainActivity`)**: `Minimo Launcher` | `Distraction free home screen` | `Get Started`
- **Step 2 (`com.minimo.launcher/MainActivity`)**: `Favorite Apps` | `Search app` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 3 (`com.minimo.launcher/MainActivity`)**: `Favorite Apps` | `Search app` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail`
- **Step 4 (`com.minimo.launcher/MainActivity`)**: `Distraction free home screen` | `Choose Minimo as your default launcher` | `Set Default Launcher` | `Skip`
- **Step 5 (`com.minimo.launcher/MainActivity`)**: `Calendar`
- **Step 6 (`com.minimo.launcher/MainActivity`)**: `Favorite Apps` | `Hidden Apps` | `Customization` | `Set Default Launcher` | `About App` | `Become a Supporter` | `Back` | `Settings`
- **Step 7 (`com.minimo.launcher/MainActivity`)**: `Orientation` | `Portrait` | `Dropdown arrow` | `Icon Pack` | `Install an icon pack app to select it here. Apps withou` | `Icon Pack: Default` | `Default` | `Font` | `System` | `Theme`
- **Step 8 (`com.minimo.launcher/MainActivity`)**: `Favorite Apps` | `Hidden Apps` | `Customization` | `Set Default Launcher` | `About App` | `Become a Supporter` | `Back` | `Settings`

## 中文逐页引导链路解读

> **全链路总结**：该应用为极简桌面/双击锁屏类启动器：从欢迎页进入收藏应用选择，跳过默认桌面设置，长按主屏进入设置并探索自定义项；全程无强制授权、通知横幅或遮罩，未见明显诱导话术。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “无干扰的主屏幕”（步骤1欢迎页）
- 英文 -> “至少添加1个才能继续”（步骤2收藏应用页）
- 英文 -> “选择Minimo作为你的默认桌面”（步骤4默认桌面引导页）
- 英文 -> “安装图标包应用后可在此选择，未匹配图标保持默认”（步骤7自定义页）
- 英文 -> “成为支持者”（步骤6/8设置菜单）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 启动欢迎页，英文意为“极简启动器/无干扰主屏/开始使用”；点Get Started进入引导，无通知遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 收藏应用选择页，列出日历、相机等应用并提示“至少添加1个才能继续”；点击日历开关，未见通知或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 同一收藏应用页，底部按钮变为“继续”；点击Continue完成选择并进入下一步，页面无通知横幅与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 默认桌面引导页，英文意为“选择Minimo为默认桌面”，提供设置默认与跳过；点击Skip拒绝设置，无通知遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 极简主屏仅显示日历标签；长按空白处以打开桌面选项/设置，当前页无通知横幅或浮层遮罩。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 桌面设置菜单含收藏/隐藏应用、自定义、默认桌面、关于、支持作者等；点Customization，无通知遮罩。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 自定义页显示方向、图标包、字体、主题及壁纸开关，提示可装图标包；未见双击锁屏项，点返回，无通知遮罩。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 返回设置菜单后再次点击Customization，拟下滑查找“双击锁屏”开关；本页无通知横幅与遮罩。 | `step_08_action.png` |
