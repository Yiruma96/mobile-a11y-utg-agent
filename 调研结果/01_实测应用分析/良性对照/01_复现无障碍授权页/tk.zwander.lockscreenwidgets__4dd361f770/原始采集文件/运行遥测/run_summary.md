# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:03:43
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`tk.zwander.lockscreenwidgets`（静态标签：`benign` / `锁屏与悬浮组件辅助` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 6 步，UTG 唯一节点 `8` 个，有向边 `10` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 6 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_06_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`tk.zwander.lockscreenwidgets/tk.zwander.common.activities.OnboardingActivity` | hooks=`[]` | overlays=`0` | texts=`Accessibility / Widgets Anywhere requires an Accessibility Service to display widgets on the lock screen and in the notification center. No data is collected, and no actions will be performed on the device. This permission is optional if you are only using the home screen widget stacks. / More Info / Previous / Next`
- **Back 后 +5.5s**：`tk.zwander.lockscreenwidgets/tk.zwander.common.activities.OnboardingActivity` | hooks=`[]` | overlays=`0` | texts=`Accessibility / Widgets Anywhere requires an Accessibility Service to display widgets on the lock screen and in the notification center. No data is collected, and no actions will be performed on the device. This permission is optional if you are only using the home screen widget stacks. / More Info / Previous / Next`
- **Back 后 +10.5s**：`tk.zwander.lockscreenwidgets/tk.zwander.common.activities.OnboardingActivity` | hooks=`[]` | overlays=`0` | texts=`Accessibility / Widgets Anywhere requires an Accessibility Service to display widgets on the lock screen and in the notification center. No data is collected, and no actions will be performed on the device. This permission is optional if you are only using the home screen widget stacks. / More Info / Previous / Next`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `tk.zwander.lockscreenwidgets` / `OnboardingActivity` | `-` | 7 | 114 / 否 | `click` → [6] View (click) center=(970,2082) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `tk.zwander.lockscreenwidgets` / `OnboardingActivity` | `-` | 7 | 315 / 否 | `click` → [6] View (click) center=(970,2082) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `tk.zwander.lockscreenwidgets` / `OnboardingActivity` | `-` | 9 | 135 / 否 | `click` → [8] View (click) center=(970,2082) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `tk.zwander.lockscreenwidgets` / `OnboardingActivity` | `-` | 9 | 305 / 否 | `click` → [4] View (click) center=(540,1906) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `tk.zwander.lockscreenwidgets` / `OnboardingActivity` | `-` | 6 | 186 / 否 | `click` → [3] View (click) center=(833,1324) | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 215 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_06_layout.xml` + `step_06_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`tk.zwander.lockscreenwidgets/OnboardingActivity`)**: `Welcome!` | `Widgets Anywhere is an app focused on making widgets mo` | `Exit` | `Next`
- **Step 2 (`tk.zwander.lockscreenwidgets/OnboardingActivity`)**: `Basic Usage` | `Tap the "plus" page to add a widget, press and hold to ` | `Previous` | `Next`
- **Step 3 (`tk.zwander.lockscreenwidgets/OnboardingActivity`)**: `Privacy Policy` | `Widgets Anywhere doesn't collect any data beyond what's` | `More Info` | `Previous` | `Next`
- **Step 4 (`tk.zwander.lockscreenwidgets/OnboardingActivity`)**: `Accessibility` | `Widgets Anywhere requires an Accessibility Service to d` | `More Info` | `Previous` | `Next`
- **Step 5 (`tk.zwander.lockscreenwidgets/OnboardingActivity`)**: `Accessibility` | `To be able to display on the lock screen, you'll need t` | `Grant` | `Close App`
- **Step 6 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Widgets Anywhere` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以欢迎、功能与隐私说明引导用户进入无障碍页，用“不收集数据、不执行操作”等话术降低戒心，再点 Grant 跳转系统无障碍授权；拒绝后反复回到同一诱导页，无法继续，形成 TRAPPED_ON_LURE_SCREEN。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英语「Welcome!」-> 欢迎！（欢迎页）
- 英语「Widgets Anywhere is an app focused on making widgets more accessible and providing extra features.」-> 本应用致力于让小组件更易访问并提供额外功能（欢迎页）
- 英语「Widgets Anywhere doesn't collect any data beyond what's needed for crash analysis.」-> 除崩溃分析外不收集任何数据（隐私政策页）
- 英语「Widgets Anywhere requires an Accessibility Service to display widgets on the lock screen and in the notification center. No data is collected... This permission is optional...」-> 需无障碍服务在锁屏/通知中心显示小组件，不收集数据、不执行操作，仅用主屏小组件时可选用（无障碍说明页）
- 英语「To be able to display on the lock screen... This app doesn't collect any data from your screen.」-> 为在锁屏显示需启用无障碍，应用不采集屏幕数据（授权弹窗）
- 英语「Allow Widgets Anywhere to have full control of your device?」-> 允许 Widgets Anywhere 完全控制设备？（系统警告弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: OnboardingActivity** | 引导欢迎页，说明应用让小组件更易用并含额外功能，有 Exit/Next；本步点 Next 前进。 | `step_01_action.png` |
| 2 | **Step 2: OnboardingActivity** | 基础用法页，介绍加号添加、长按排序缩放删除、双指移动/三指隐藏；本步点 Next 继续。 | `step_02_action.png` |
| 3 | **Step 3: OnboardingActivity** | 隐私政策页，称除崩溃分析外不收集数据并提供 More Info；本步点 Next 继续。 | `step_03_action.png` |
| 4 | **Step 4: OnboardingActivity** | 无障碍说明页，称仅用于锁屏/通知中心显示小组件、不收集数据且可选；本步点 More Info。 | `step_04_action.png` |
| 5 | **Step 5: OnboardingActivity** | 无障碍授权弹窗，强调不采集屏幕数据，含 Grant/Close App；本步点 Grant 跳转系统设置。 | `step_05_action.png` |
| 6 | **Step 6: [无障碍列表页]** | 系统无障碍列表显示 Widgets Anywhere 为 Off；探针捕获无障碍设置钩子与检测后自动终止。 | `step_06_screen.png` |
| 7 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍停留系统无障碍列表，无通知横幅、无遮罩，未发生交互。 | `step_06_probe_800ms_screen.png` |
| 8 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针，仍停留系统无障碍列表，无通知横幅、无遮罩，未发生交互。 | `step_06_probe_2000ms_screen.png` |
| 9 | **服务详情页** | 服务详情页显示 Use Widgets Anywhere 开关与说明，称不收集数据且可选；仅检查未授权。 | `step_06_service_detail_screen.png` |
| 10 | **系统警告弹窗(点Deny)** | 系统高危警告弹窗，提示可查看/控制屏幕并代执行操作，含 Allow/Deny；仅检查未选择。 | `step_06_system_warning_screen.png` |
| 11 | **拒权返回 +2.0s** | 拒权返回 2 秒后仍停在无障碍说明页，仅有 More Info/Previous/Next，无退出，形成诱导页困住。 | `step_06_refusal_2000ms_screen.png` |
| 12 | **拒权返回 +10.5s** | 拒权返回 10.5 秒后仍停同一无障碍说明页，交互未变，仍无退出，持续困在诱导页。 | `step_06_refusal_10500ms_screen.png` |
