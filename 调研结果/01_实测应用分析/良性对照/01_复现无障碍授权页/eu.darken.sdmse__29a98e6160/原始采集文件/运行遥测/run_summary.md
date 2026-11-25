# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T11:22:32
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`False`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`eu.darken.sdmse`（静态标签：`benign` / `系统效率与通用辅助` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 8 步，UTG 唯一节点 `11` 个，有向边 `12` 条）
- **拒权回退探针结论（Golden Page ④）**：`GRACEFUL_STAY_OR_DEGRADE`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 8 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_08_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`eu.darken.sdmse/eu.darken.sdmse.main.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`I didn't root my device / Only available on rooted devices. If you didn't make this modification, then your device is not rooted and this setting has no effect. / Usage statistics / The usage statistics permission grants access to more app details. SD Maid uses it to determine additional cache sizes. / Grant access`
- **Back 后 +5.5s**：`eu.darken.sdmse/eu.darken.sdmse.main.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`I didn't root my device / Only available on rooted devices. If you didn't make this modification, then your device is not rooted and this setting has no effect. / Usage statistics / The usage statistics permission grants access to more app details. SD Maid uses it to determine additional cache sizes. / Grant access`
- **Back 后 +10.5s**：`eu.darken.sdmse/eu.darken.sdmse.main.ui.MainActivity` | hooks=`[]` | overlays=`0` | texts=`I didn't root my device / Only available on rooted devices. If you didn't make this modification, then your device is not rooted and this setting has no effect. / Usage statistics / The usage statistics permission grants access to more app details. SD Maid uses it to determine additional cache sizes. / Grant access`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `eu.darken.sdmse` / `MainActivity` | `-` | 5 | 160 / 否 | `click` → [4] View (click) center=(540,2038) | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `eu.darken.sdmse` / `MainActivity` | `-` | 12 | 254 / 否 | `click` → [11] View (click) center=(540,2038) | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `eu.darken.sdmse` / `MainActivity` | `-` | 11 | 439 / 否 | `click` → [10] View (click) center=(540,2038) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `eu.darken.sdmse` / `MainActivity` | `-` | 32 | 580 / 否 | `click` → [31] View (click) center=(912,1369) | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `eu.darken.sdmse` / `MainActivity` | `-` | 33 | 615 / 否 | `swipe` → [540, 1800] | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `eu.darken.sdmse` / `MainActivity` | `-` | 31 | 823 / 否 | `swipe` → [540, 1800] | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `eu.darken.sdmse` / `MainActivity` | `-` | 26 | 896 / 否 | `click` → [16] TextView text="Enable service and grant access" ce | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 209 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`eu.darken.sdmse/MainActivity`)**: `Welcome` | `SD Maid SE manages files, apps and storage.` | `Gain storage space by cleaning up behind other apps. De` | `Continue`
- **Step 2 (`eu.darken.sdmse/MainActivity`)**: `Privacy` | `SD Maid has no ads and does not sell user data.` | `Privacy policy` | `Update check` | `Allow SD Maid to check for updates to let you know if a` | `Important messages` | `Allow SD Maid to check for important messages from the ` | `Continue`
- **Step 3 (`eu.darken.sdmse/MainActivity`)**: `Setup` | `SD Maid will search all accessible data areas.` | `What is accessible depends on your device, Android vers` | `SD Maid's defaults are configured to be safe and thorou` | `For more thorough results, visit each tool's settings a` | `Start using SD Maid by setting up access.` | `Show guided tours` | `A quick guided tour of each feature as you open it.` | `Set up access`
- **Step 4 (`eu.darken.sdmse/MainActivity`)**: `Manage storage` | `Allow SD Maid to manage your storage.` | `Public storage` | `/storage/emulated/0` | `Grant access` | `Help` | `Default public app assets` | `/storage/emulated/0/Android/obb` | `In most cases the window will open with the correct pat` | `ADB access`
- **Step 5 (`eu.darken.sdmse/MainActivity`)**: `Manage storage` | `Allow SD Maid to manage your storage.` | `Public storage` | `/storage/emulated/0` | `Grant access` | `Basic access to public storage, e.g. "Download/" and "D` | `Help` | `Storage access framework` | `Improve results by granting SD Maid access to additiona` | `Default public app data`
- **Step 6 (`eu.darken.sdmse/MainActivity`)**: `In most cases the window will open with the correct pat` | `ADB access` | `Allow SD Maid to use ADB access where possible to impro` | `Try to use ADB access` | `Don't use ADB access` | `This setting has no effect unless Porter or Shizuku is ` | `Help` | `Root access` | `Should SD Maid use root access if it is available? Root` | `Try to use root access`
- **Step 7 (`eu.darken.sdmse/MainActivity`)**: `I didn't root my device` | `Only available on rooted devices. If you didn't make th` | `Usage statistics` | `The usage statistics permission grants access to more a` | `Grant access` | `Required for accessibility service based cache deletion` | `Help` | `Accessibility service` | `The accessibility service allows SD Maid to interact wi` | `SD Maid will not use the accessibility service without `
- **Step 8 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `SD Maid SE` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用以向导依次介绍清理、隐私、存储、ADB/Root、用量统计与无障碍服务；最终跳转系统无障碍页并触发高危授权警告，拒权后回到应用原页保持可用并优雅降级。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “SD Maid 会搜索所有可访问数据区域；可访问范围取决于设备、Android 版本和已授权限”（Setup 页）
- 英文 -> “默认配置安全且彻底，兼顾大多数用户；可进各工具设置调整”（Setup 页）
- 英文 -> “无障碍服务用于与屏幕交互并自动化繁琐操作，例如多屏点‘清除缓存’”（无障碍服务卡片）
- 英文 -> “未经同意不会使用无障碍服务，活跃时始终显示醒目可取消提示，且不用于收集信息”（无障碍服务卡片）
- 英文 -> “使用统计权限授予更多应用详情，用于判断额外缓存大小”（用量统计卡片）
- 英文 -> “ADB/Root 可提高结果并启用功能；未配置 Porter/Shizuku 或未 Root 则无效”（ADB/Root 卡片）
- 英文 -> “用户有特殊无障碍需求时可启用该服务，自动完成原本繁琐的手动交互，如缓存删除”（服务详情页）
- 英文 -> “系统警告：允许 SD Maid SE 完全控制设备？可查看/控制屏幕并代你操作”（系统授权弹窗）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: MainActivity** | 欢迎页；英文介绍文件/应用/存储管理与清理释放空间；点击Continue进入隐私页，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: MainActivity** | 隐私页；英文声明无广告、不卖数据，含隐私政策/更新检查/重要消息开关；点击Continue，无遮罩。 | `step_02_action.png` |
| 3 | **Step 3: MainActivity** | 设置说明页；英文称将搜索可访问区域、默认安全彻底；点击Set up access进入访问配置，无通知。 | `step_03_action.png` |
| 4 | **Step 4: MainActivity** | 存储管理弹层；英文列公共存储/obb/ADB授权并提示路径预选、变绿即成功；点勾选关闭说明，无遮罩。 | `step_04_action.png` |
| 5 | **Step 5: MainActivity** | 存储管理卡片；英文说明基础公共存储与SAF可扩大访问，含Android/data与obb路径；下滑继续，无通知/遮罩。 | `step_05_action.png` |
| 6 | **Step 6: MainActivity** | ADB/Root/用量统计卡片；英文称ADB需Porter或Shizuku、Root仅限已Root、统计助算缓存；下滑继续。 | `step_06_action.png` |
| 7 | **Step 7: MainActivity** | 无障碍服务卡片；英文称用于屏幕自动化清缓存，承诺需同意、醒目可取消、不收集信息；点击启用并授权。 | `step_07_action.png` |
| 8 | **Step 8: [无障碍列表页]** | 系统无障碍列表；SD Maid SE显示Off；探针捕获无障碍设置钩子后自动终止，无通知横幅/遮罩。 | `step_08_screen.png` |
| 9 | **跳后探针 +0.8s** | 跳转后0.8秒探针；仍停留系统无障碍列表，无文本、无通知、无遮罩，未发生授权动作。 | `step_08_probe_800ms_screen.png` |
| 10 | **跳后探针 +2.0s** | 跳转后2.0秒探针；页面保持系统无障碍列表，无文本、无通知、无遮罩，授权状态未变。 | `step_08_probe_2000ms_screen.png` |
| 11 | **服务详情页** | 服务详情页；Use SD Maid SE开关与快捷方式Off；长文称仅自动化、显眼提示、可随时禁用；仅检查未开启。 | `step_08_service_detail_screen.png` |
| 12 | **系统警告弹窗(点Deny)** | 系统高危授权弹窗；英文问是否允许完全控制设备，列查看屏幕/代操作，含Allow/Deny；检查时点Deny。 | `step_08_system_warning_screen.png` |
| 13 | **拒权返回 +2.0s** | 拒权返回2秒；回到应用无障碍服务卡片，权限未授予但页面正常，无通知/遮罩，呈优雅保持/降级。 | `step_08_refusal_2000ms_screen.png` |
| 14 | **拒权返回 +10.5s** | 拒权返回10.5秒；仍停留无障碍服务卡片，界面稳定无崩溃，无通知/遮罩，继续可手动配置或跳过。 | `step_08_refusal_10500ms_screen.png` |
