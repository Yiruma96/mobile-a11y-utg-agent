# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:26:04
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.slate.launcher`（静态标签：`benign` / `极简桌面与双击锁屏` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `5` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.slate.launcher` / `OnboardingActivity` | `-` | 35 | 200 / 否 | `click` → [34] CheckBox desc="I have read the privacy policy" id= | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.slate.launcher` / `OnboardingActivity` | `-` | 35 | 200 / 否 | `swipe` → [540, 1900] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.slate.launcher` / `OnboardingActivity` | `-` | 37 | 273 / 否 | `click` → [35] TextView text="Skip for now" id=btnSkip (click) ce | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.slate.launcher` / `MainActivity` | `-` | 5 | 141 / 否 | `click` → [4] TextView text="Skip" id=btnTourSkip (click) center= | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.slate.launcher` / `MainActivity` | `-` | 18 | 128 / 否 | `system_button` → Back | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.slate.launcher` / `MainActivity` | `-` | 18 | 128 / 否 | `swipe` → [540, 1100] | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.slate.launcher` / `MainActivity` | `-` | 10 | 278 / 否 | `system_button` → Back | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.slate.launcher` / `MainActivity` | `-` | 18 | 128 / 否 | `system_button` → Back | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.slate.launcher/OnboardingActivity`)**: `slate` | `a minimal launcher` | `CHOOSE A THEME` | `DARK` | `messages` | `maps` | `camera` | `photos` | `LIGHT` | `CHOOSE A LAYOUT`
- **Step 2 (`com.slate.launcher/OnboardingActivity`)**: `slate` | `a minimal launcher` | `CHOOSE A THEME` | `DARK` | `messages` | `maps` | `camera` | `photos` | `LIGHT` | `CHOOSE A LAYOUT`
- **Step 3 (`com.slate.launcher/OnboardingActivity`)**: `CHOOSE A THEME` | `DARK` | `messages` | `maps` | `camera` | `photos` | `LIGHT` | `CHOOSE A LAYOUT` | `FLOW` | `mail`
- **Step 4 (`com.slate.launcher/MainActivity`)**: `WELCOME TO SLATE` | `1 / 8` | `Step 1 of 8` | `Slate shows your apps as plain text - no icons, no widg` | `Skip` | `Next`
- **Step 5 (`com.slate.launcher/MainActivity`)**: `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google` | `Maps`
- **Step 6 (`com.slate.launcher/MainActivity`)**: `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google` | `Maps`
- **Step 7 (`com.slate.launcher/MainActivity`)**: `4:26` | `4:26 AM` | `On` | `Wi-Fi,` | `Bluetooth.` | `Off` | `Do Not Disturb.` | `Flashlight` | `Auto-rotate screen` | `Battery Saver`
- **Step 8 (`com.slate.launcher/MainActivity`)**: `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files` | `Gmail` | `Google` | `Maps`

## 中文逐页引导链路解读

> **全链路总结**：从引导页勾选隐私政策、滚动寻找入口并点“暂时跳过”，进入启动器后跳过8步使用说明；随后在应用抽屉与系统通知栏间返回切换，全程无通知横幅、无悬浮遮罩，未出现明显诱导或索权行为，属合规极简桌面。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语 -> “slate / a minimal launcher”即“Slate / 一款极简启动器”（Step 1-2 引导页）
- 英语 -> “CHOOSE A THEME / CHOOSE A LAYOUT”即“选择主题 / 选择布局”（Step 1-3 引导页）
- 英语 -> “I have read the privacy policy”即“我已阅读隐私政策”（Step 1 隐私复选框）
- 英语 -> “Skip for now”即“暂时跳过”（Step 3 引导页）
- 英语 -> “WELCOME TO SLATE / Step 1 of 8 / Slate shows your apps as plain text - no icons, no widgets. Here's a 30-second tour of how to use it.”即“欢迎使用Slate/共8步第1步/Slate以纯文本显示应用，无图标无小部件，30秒导览”（Step 4 使用引导）
- 英语 -> “Skip / Next”即“跳过 / 下一步”（Step 4 使用引导）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: OnboardingActivity** | 引导页显示“极简启动器”、主题/布局选择；点击未勾选的隐私政策复选框，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: OnboardingActivity** | 同页隐私复选框已勾选但未见继续按钮；向上滑动寻找下一步入口，仍无通知横幅或遮罩。 | `step_02_action.png` |
| 3 | **Step 3: OnboardingActivity** | 同页滚动后出现“暂时跳过”；点击后不设默认桌面直接进入启动器，无通知与遮罩。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 启动器8步引导第1步；英文说明纯文本显示应用、无图标小部件，点击“跳过”退出引导。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 主界面应用抽屉列出日历、相机、Chrome等；按返回键关闭抽屉，无通知横幅或遮罩。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | 应用抽屉仍展开，显示日历、相机等应用名；下滑尝试关闭抽屉回桌面，无通知与遮罩。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 系统通知栏/快捷设置展开，含Wi‑Fi、蓝牙、勿扰、手电筒等开关；按返回关闭，无应用遮罩。 | `step_07_action.png` |
| 8 | **Step 8: MainActivity** | 应用抽屉再次展开，列出日历、相机、Gmail等应用；按返回键返回启动器桌面，无通知或遮罩。 | `step_08_action.png` |
