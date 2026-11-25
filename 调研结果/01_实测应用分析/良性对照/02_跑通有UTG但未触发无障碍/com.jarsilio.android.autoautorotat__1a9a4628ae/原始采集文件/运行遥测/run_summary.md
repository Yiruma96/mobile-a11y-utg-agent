# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:18:44
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.jarsilio.android.autoautorotate`（静态标签：`benign` / `显示调节、截屏与分屏效率` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.jarsilio.android.autoautorotate` / `AppIntro` | `-` | 6 | 226 / 否 | `click` → [6] ImageButton desc="NEXT" id=next (click) center=(981 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.jarsilio.android.autoautorotate` / `AppIntro` | `-` | 6 | 226 / 否 | `swipe` → [900, 1000] | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.jarsilio.android.autoautorotate` / `AppIntro` | `-` | 6 | 226 / 否 | `swipe` → [900, 1100] | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.jarsilio.android.autoautorotate` / `AppIntro` | `-` | 6 | 226 / 否 | `click` → [1017, 2132] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.jarsilio.android.autoautorotate` / `AppIntro` | `-` | 6 | 226 / 否 | `click` → [5] Button text="REQUEST PERMISSION" id=slide_button (c | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.android.settings` / `Settings$UsageAccessSettingsActivity` | `-` | 16 | 111 / 否 | `click` → [5] LinearLayout desc="Auto Auto-Rotate" (click) center | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.android.settings` / `SubSettings` | `-` | 10 | 213 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `SubSettings` | `-` | 10 | 213 / 否 | `click` → [1] ImageButton desc="Back" (click) center=(77,160) | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.jarsilio.android.autoautorotate/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, Auto A` | `Please select Auto Auto-Rotate and check 'Permit usage ` | `REQUEST PERMISSION` | `NEXT`
- **Step 2 (`com.jarsilio.android.autoautorotate/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, Auto A` | `Please select Auto Auto-Rotate and check 'Permit usage ` | `REQUEST PERMISSION` | `NEXT`
- **Step 3 (`com.jarsilio.android.autoautorotate/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, Auto A` | `Please select Auto Auto-Rotate and check 'Permit usage ` | `REQUEST PERMISSION` | `NEXT`
- **Step 4 (`com.jarsilio.android.autoautorotate/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, Auto A` | `Please select Auto Auto-Rotate and check 'Permit usage ` | `REQUEST PERMISSION` | `NEXT`
- **Step 5 (`com.jarsilio.android.autoautorotate/AppIntro`)**: `Usage Access` | `In order to know which app is currently running, Auto A` | `Please select Auto Auto-Rotate and check 'Permit usage ` | `REQUEST PERMISSION` | `NEXT`
- **Step 6 (`com.android.settings/Settings$UsageAccessSettingsActivity`)**: `Back` | `Usage access` | `Search` | `More options` | `Auto Auto-Rotate` | `Not allowed` | `Digital Wellbeing` | `Allowed` | `Google` | `Google Play services`
- **Step 7 (`com.android.settings/SubSettings`)**: `Back` | `Usage access` | `Search settings` | `Auto Auto-Rotate` | `1.2.4` | `Permit usage access` | `Usage access allows an app to track what other apps you`
- **Step 8 (`com.android.settings/SubSettings`)**: `Back` | `Usage access` | `Search settings` | `Auto Auto-Rotate` | `1.2.4` | `Permit usage access` | `Usage access allows an app to track what other apps you`

## 中文逐页引导链路解读

> **全链路总结**：应用启动后停留在英文 AppIntro 的“Usage Access”引导页，以识别前台应用为由要求授予使用情况访问；NEXT 被权限门控，多次点击/滑动无效，点击 REQUEST PERMISSION 跳转系统设置并开启后返回。全程未见通知横幅或遮罩，属系统权限引导链路。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “自动自动旋转需要‘使用情况访问’才能知道当前运行哪个应用”（Step1-5引导页）
- 英文 -> “点击下方按钮后选择 Auto Auto-Rotate 并勾选‘允许使用情况访问’”（Step1-5引导页）
- 英文 -> “请求权限”/“下一步”（Step1-5按钮）
- 英文 -> “允许使用情况访问”，系统说明其可跟踪其他应用使用情况、运营商和语言等（Step7-8系统设置）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: AppIntro** | 英文引导页“Usage Access”说明需使用情况访问以识别当前应用；点击NEXT未前进，页面仍停留本页，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: AppIntro** | 同一英文引导页，仍要求授予使用情况访问；左滑ViewPager试图前进但未见切换，页面保持原样，无通知/遮罩。 | `step_02_action.png` |
| 3 | **Step 3: AppIntro** | 仍是“Usage Access”引导页，说明需权限才能识别当前应用；再次指定坐标左滑仍未翻页，无通知/遮罩。 | `step_03_action.png` |
| 4 | **Step 4: AppIntro** | 页面仍显示使用情况访问说明与REQUEST PERMISSION；点击右上箭头字形未前进，无通知/遮罩。 | `step_04_action.png` |
| 5 | **Step 5: AppIntro** | 因NEXT被权限门控，点击REQUEST PERMISSION跳转系统使用情况访问设置；本页为权限入口，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: Settings$UsageAccessSettin** | 系统“Usage access”列表显示Auto Auto-Rotate为Not allowed；点击该应用进入授权详情，无通知/遮罩。 | `step_06_action.png` |
| 7 | **Step 7: SubSettings** | 系统授权详情页，含Permit usage access开关及跟踪说明；点击未选中的开关以开启，无通知/遮罩。 | `step_07_action.png` |
| 8 | **Step 8: SubSettings** | 同一授权详情页，开关已开启后点击Back返回应用引导流；页面为系统设置，无通知/遮罩。 | `step_08_action.png` |
