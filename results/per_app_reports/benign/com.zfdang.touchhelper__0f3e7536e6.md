# BN_058__0f3e7536e6｜自动化与跳广告 — 开屏跳过

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：122.0s

## 1. 一句话核心结论

- **核心申请方式**：冷启动首页在服务未开启且未同意时弹出可取消的透明披露对话框，用户点“同意并前往设置”后才跳系统 ACTION_ACCESSIBILITY_SETTINGS，全程如实告知读取范围并承诺不联网，无遮罩、无死循环、无受限设置教学。
- **静态可见性说明**：无壳、无加密载荷、无动态加载与远端下发；权限申请链路全部为本地原生代码与 strings.xml 明文，Manifest 无 INTERNET 权限，故无远端 WebView 或云控开关可藏。
- **命中的行为模式标签**：`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0f3e7536e6d00416afa65f125c5dad2efd757773b7c05e3ea015d4170764f297` |
| 包名 / 年份 | `com.zfdang.touchhelper` / 2025-2026 |
| 家族 / 品类 | **自动化与跳广告**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.zfdang.touchhelper_278.apk |
| 桌面显示名 | 开屏跳过 |
| 引导页宣称品牌/身份 | 开屏跳过（com.zfdang.touchhelper，作者 Zhengfa Dang，F-Droid 开源项目） |
| 系统无障碍列表服务名 | 开屏跳过-无障碍服务 |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅有常规 R8 短名混淆（P0.a/P0.c 等），无空白或换行挤出警告、无同形字、无多 activity-alias 伪装、未伪造 isAccessibilityTool（如实设为 false） |
| 无障碍服务类名 | `com.zfdang.touchhelper.TouchHelperService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | "开屏跳过"是基于安卓系统的无障碍服务来实现自动跳过广告功能的，为了保证程序能正常工作，打开此服务。<br><br>本程序为开源程序，不需要网络权限，不会收集或上传任何个人信息，请放心使用！ |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.zfdang.touchhelper.MainActivity（NavHost + BottomNavigationView）→ HomeFragment | onCreate → setContentView(activity_main) → NavHost 挂载 HomeFragment.onCreateView → g() 刷新服务与电池优化状态 | 原生Activity | **原文**：开屏跳过（@string/app_name）<br>**译注**：桌面与标题栏显示“开屏跳过” | 无强制动作，可直接浏览首页 | `com.zfdang.touchhelper.MainActivity#onCreate / com.zfdang.touchhelper.ui.home.HomeFragment#onCreateView, #g / res/layout/activity_main.xml` |
| 2 | 引导说明页 | MaterialAlertDialog（MaterialAlertDialogBuilder，标题+正文+三按钮） | HomeFragment.onResume：当 TouchHelperService.b() 为 false（服务未连接）且 SharedPreferences 中 ACCESSIBILITY_DISCLOSURE_ACCEPTED 为 false 时调用 h() 弹窗 | 原生Dialog | **原文**：开启无障碍服务前请了解 / "开屏跳过"通过安卓无障碍服务读取当前屏幕上的界面内容（控件文字、描述和位置），用于识别并自动点击开屏广告的"跳过"按钮。· 自动识别时，这些内容只在本机内存中即时比对，不保存。· 当您使用"添加程序的跳过方法"时，您所选控件的文字、描述和坐标会作为规则保存在本机的应用数据中，可在设置中查看或删除。· 当您使用"复制窗口控件"时，当前窗口的控件信息会按您的操作复制到系统剪贴板。本程序不申请网络权限，不会收集或上传任何数据。同意后即可开启无障碍服务；未同意前服务不会读取任何界面内容。 [同意并前往设置] [取消]<br>**译注**：开启无障碍服务前请了解：说明无障碍服务读取的是屏幕控件文字/描述/位置，仅本机内存即时比对不保存；自定义规则保存在本机可删除；复制控件信息仅进入系统剪贴板；不申请网络权限、不上传数据；未同意前不读取任何界面内容。按钮为“同意并前往设置”与“取消” | 可点“同意并前往设置”进入系统无障碍设置，或点“取消”关闭（无死循环）；服务已开启时按钮变为“同意”仅作确认 | `com.zfdang.touchhelper.ui.home.HomeFragment#h / res/values/strings.xml accessibility_disclosure_title(0x7f110024)、accessibility_disclosure_message(0x7f110022)、accessibility_disclosure_agree(0x7f11001f)、accessibility_disclosure_agree_only(0x7f110020)、accessibility_disclosure_cancel(0x7f110021)` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（Intent + FLAG_ACTIVITY_NEW_TASK） | 用户点击对话框正向按钮 → P0.a.onClick(DialogInterface, int)：先写入 ACCESSIBILITY_DISCLOSURE_ACCEPTED=true，若服务已连接则直接 return，否则 startActivity | 系统无障碍页 | **原文**：无（应用自身不渲染该页）<br>**译注**：跳转至系统“无障碍”设置列表 | 由用户自行在系统列表中手动开启“开屏跳过-无障碍服务” | `P0.a#onClick / com.zfdang.touchhelper.f#<clinit>（读取 ACCESSIBILITY_DISCLOSURE_ACCEPTED）` |
| 4 | 遮罩叠层指引 | 系统无障碍列表中的服务条目（label + android:description） | 用户在系统无障碍列表查看该服务说明 | 系统无障碍页 | **原文**：开屏跳过-无障碍服务 / "开屏跳过"是基于安卓系统的无障碍服务来实现自动跳过广告功能的，为了保证程序能正常工作，打开此服务。<br><br>本程序为开源程序，不需要网络权限，不会收集或上传任何个人信息，请放心使用！<br>**译注**：服务名“开屏跳过-无障碍服务”，说明为开源、无需网络权限、不收集上传个人信息；未叠放任何悬浮窗或仿系统开关页 | 用户手动打开开关（应用不叠遮罩、不代点） | `res/xml/accessibility_service_config.xml / res/values/strings.xml touch_helper_service_label、touch_helper_service_description` |
| 5 | 获权后动作 | 回到 HomeFragment.onResume 的二次确认 Dialog（仅“同意”按钮） | 用户授权后返回应用触发 onResume：TouchHelperService.b() 为 true 且 ACCESSIBILITY_DISCLOSURE_ACCEPTED 仍为 false → h() 再次弹窗，正按钮文本为 accessibility_disclosure_agree_only | 原生Dialog | **原文**：开启无障碍服务前请了解 / ……本程序不申请网络权限，不会收集或上传任何数据。同意后即可开启无障碍服务；未同意前服务不会读取任何界面内容。 [同意] [取消]<br>**译注**：授权后补做一次披露确认，点“同意”仅写标志位，不再次跳设置、不自动点击系统开关 | 点“同意”完成确认（P0.a.onClick 中 z=true 时直接 return，不再 startActivity） | `com.zfdang.touchhelper.ui.home.HomeFragment#onResume, #h / P0.a#onClick` |
| 6 | 业务功能触发 | 首页/设置页的电池优化与后台保活引导（IGNORE_BATTERY_OPTIMIZATION_SETTINGS 跳转） | 用户点击首页电池优化项 → P0.c.onClick(case 0) 构造 ACTION IGNORE_BATTERY_OPTIMIZATION_SETTINGS 并 startActivity；g() 用 isIgnoringBatteryOptimizations 显示状态 | 系统无障碍页 | **原文**："开屏跳过"基于安卓系统的无障碍服务来实现跳过自动广告功能，开源不联网，绝对安全！为保证程序能正常工作，请检查以下设置：1. 在"无障碍"设置里，打开"开屏跳过 - 无障碍服务"。2. 在"电池优化"设置里，设置"开屏跳过"为"不优化"。3. 在电池管理里，设置"开屏跳过"为"允许后台耗电"。…… 4. 在"任务管理"里，锁定"开屏跳过"。<br>**译注**：以文字步骤如实告知需开启无障碍、关闭电池优化、允许后台耗电、锁定任务，均为用户主动点击的独立跳转 | 用户自行逐项前往系统页面设置，可随时跳过 | `P0.c#onClick / com.zfdang.touchhelper.ui.home.HomeFragment#g / res/values/strings.xml text_instructions、text_accessibility_permission、text_power_permission、text_rom_battery、text_task_manager` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- HomeFragment 的 MaterialAlertDialog（标题“开启无障碍服务前请了解”+ accessibility_disclosure_message 正文+“同意并前往设置/同意/取消”三按钮），非全屏、可取消
- 系统“无障碍”设置列表中的服务条目：label=开屏跳过-无障碍服务，说明=android:description（@string/touch_helper_service_description）
- 应用首页/设置页内的说明区块（res/layout 中 id 为 text_instructions、text_accessibility_permission、text_power_permission、text_rom_battery、text_task_manager 的文本）
- 关于页（AboutFragment，res/layout/fragment_about.xml）：about_app_introduction 功能说明、about_copyright、about_privacy_policy 与 about_weblink（https://touchhelper.zfdang.com/ 由浏览器打开，非应用内 WebView）
- Manifest 与 strings 中的无障碍披露提示文本 accessibility_disclosure_reminder：“开屏跳过：请打开应用并确认无障碍服务说明后，跳过功能才会开始工作”（用于提醒，不作为强制拦截）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| zh | 开启无障碍服务前请了解 | 开启无障碍服务前请了解 | `res/values/strings.xml accessibility_disclosure_title (0x7f110024)` | 良性透明说明 |
| zh | "开屏跳过"通过安卓无障碍服务读取当前屏幕上的界面内容（控件文字、描述和位置），用于识别并自动点击开屏广告的"跳过"按钮。· 自动识别时，这些内容只在本机内存中即时比对，不保存。· 当您使用"添加程序的跳过方法"时，您所选控件的文字、描述和坐标会作为规则保存在本机的应用数据中，可在设置中查看或删除。· 当您使用"复制窗口控件"时，当前窗口的控件信息会按您的操作复制到系统剪贴板。本程序不申请网络权限，不会收集或上传任何数据。同意后即可开启无障碍服务；未同意前服务不会读取任何界面内容。 | 披露无障碍读取范围与本地处理方式，声明不申请网络权限、不收集上传数据，未同意前不读取界面内容 | `res/values/strings.xml accessibility_disclosure_message (0x7f110022) / HomeFragment#h` | 良性透明说明 |
| zh | 同意并前往设置 / 同意 / 取消 | 同意并前往设置、同意、取消（存在明确取消出口） | `res/values/strings.xml accessibility_disclosure_agree(0x7f11001f)、accessibility_disclosure_agree_only(0x7f110020)、accessibility_disclosure_cancel(0x7f110021)` | 良性透明说明 |
| zh | "开屏跳过"是基于安卓系统的无障碍服务来实现自动跳过广告功能的，为了保证程序能正常工作，打开此服务。<br><br>本程序为开源程序，不需要网络权限，不会收集或上传任何个人信息，请放心使用！ | 系统无障碍列表中如实说明服务用途为自动跳过广告，并声明开源、不联网、不收集个人信息 | `res/values/strings.xml touch_helper_service_description / res/xml/accessibility_service_config.xml android:description` | 隐私承诺 |
| zh | "开屏跳过"基于安卓系统的无障碍服务来实现跳过自动广告功能，开源不联网，绝对安全！为保证程序能正常工作，请检查以下设置：1. 在"无障碍"设置里，打开"开屏跳过 - 无障碍服务"。2. 在"电池优化"设置里，设置"开屏跳过"为"不优化"。3. 在电池管理里，设置"开屏跳过"为"允许后台耗电"。设置方法因品牌不同有所差异，比如VIVO系统为："设置" -> "电池" -> "后台耗电管理"。4. 在"任务管理"里，锁定"开屏跳过"。 | 分步告知无障碍、电池优化、后台耗电与任务锁定的设置路径，属常规保活引导而非绕过安全限制 | `res/values/strings.xml text_instructions、text_accessibility_permission、text_power_permission、text_rom_battery、text_task_manager` | 良性透明说明 |
| zh | 开屏跳过：请打开应用并确认无障碍服务说明后，跳过功能才会开始工作 | 提醒用户需先确认披露说明，服务才会开始工作 | `res/values/strings.xml accessibility_disclosure_reminder` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无死循环：取消按钮无监听器仅关闭对话框；onResume 仅当无障碍服务已连接且尚未同意披露时才再次弹窗（用于授权后补确认），未授权时返回应用不会反复强制拉起，也不会定时重跳系统设置
- **遮罩叠层 / 高仿系统设置页**：无。Manifest 无 SYSTEM_ALERT_WINDOW 权限，代码无 requestAddView/WindowManager 悬浮窗，未仿制系统无障碍开关页；跳转后由系统设置页自行展示
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。未监听设置页做 GLOBAL_ACTION_BACK/HOME 阻止撤权，未自点系统开关确认；isAccessibilityTool 如实为 false
- **良性降级 / 替代方案**：有：用户可取消披露对话框并继续浏览首页与设置；首页通过 g() 显示“服务未开启”状态，仅在用户主动点击时才跳转系统设置；关于页提供功能说明与隐私政策链接供用户判断

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动进入 MainActivity/HomeFragment 且无障碍服务未连接时（onResume → h()）首个 MaterialAlertDialog 出现瞬间；以及用户点击正向按钮后 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的跳转瞬间
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：无纯图引导、无远端 HTML（应用无 INTERNET 权限）、无加壳与一阶段 Dropper；仅存在常规 R8 短名混淆，不影响运行期 UTG 判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动披露引导弹窗页** | 应用包 com.zfdang.touchhelper 内的系统 Dialog，标题“开启无障碍服务前请了解”，按钮“同意并前往设置 / 取消” | 该页决定用户是否被要求授权，可直接区分“透明披露+可取消”与“不可取消强迫授权” | 弹窗是否可关闭（存在“取消”按钮节点）；正文是否说明读取范围与不联网承诺；标题与桌面应用名/服务名是否一致（无身份混淆） |
| **跳转后的系统无障碍服务列表项** | com.android.settings 无障碍列表中出现“开屏跳过-无障碍服务”及其 description 文本 | 核对应用是否叠放遮罩/悬浮窗引导或伪造开关页，并验证 label 与说明的真实性 | 列表项文本与服务说明原文；是否存在应用侧悬浮窗/半透明遮罩覆盖系统页；开关状态是否被应用代点（无 GLOBAL_ACTION 点击痕迹） |
| **授权返回后的二次确认弹窗** | HomeFragment.onResume 触发的对话框，正按钮文本为“同意” | 验证获权后是补做披露确认还是执行对抗/反复跳转 | 按钮文本是否为“同意”而非“前往设置”；是否出现再次跳转系统设置或循环弹窗；弹窗后是否停留在首页（无强制停留/阻止退出） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.zfdang.touchhelper.ui.home.HomeFragment#onResume`
- `com.zfdang.touchhelper.ui.home.HomeFragment#h`
- `P0.a#onClick`
- `P0.c#onClick`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml accessibility_disclosure_message`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态可见性：clear）

**核心事实：这是一个完全静态可见的开源无障碍工具，没有诱导欺骗结构。**

1. **入口与检查状态**：`MainActivity.onCreate` 只设置布局，然后通过 NavHost 挂载 [HomeFragment.onCreateView()](<resource-unit:#1.dex1 code:com.zfdang.touchhelper.ui.home.HomeFragment#onCreateView>)，接着调用 `g()` 读取 `TouchHelperService.b()`（即服务连接状态）和 `isIgnoringBatteryOptimizations`，把结果显示为首页开关状态。它没有伪造系统警告、没有加壳、没有动态加载，也没有 WebView。

2. **唯一弹窗是透明披露对话框**：当服务尚未开启且用户尚未同意时，[HomeFragment.onResume()](<resource-unit:#1.dex1 code:com.zfdang.touchhelper.ui.home.HomeFragment#onResume>) 会进入 `h()`，再通过 MaterialAlertDialog 展示标题 `accessibility_disclosure_title`（“开启无障碍服务前请了解”）、正文 `accessibility_disclosure_message`（逐条说明会读取哪些控件信息、哪些仅在本机内存中比对、哪些保存在本机，以及“本程序不申请网络权限，不会收集或上传任何数据”），以及三个按钮 `同意并前往设置`、`同意`、`取消`。**取消按钮存在且没有监听器**，点击后只会关闭对话框，不会进入循环。

3. **跳转点明确且唯一**：[P0.a.onClick()](<resource-unit:#1.dex1 code:P0.a#onClick>) 先把 `ACCESSIBILITY_DISCLOSURE_ACCEPTED=true` 写入 SharedPreferences，再 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，并且只携带 `FLAG_ACTIVITY_NEW_TASK`。应用**没有** `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转，**没有**“受限设置”分步教学，也**没有** Session 安装器绕过，更没有悬浮窗权限或 `requestAddView`。

4. **获权后无对抗行为**：用户返回应用时，如果服务已连接且仍未同意，会再弹一次只有“同意”按钮的确认框；点击后只写入标志位，不跳转。没有用 `GLOBAL_ACTION_BACK/HOME` 阻止撤权，也没有自点确认或监听设置页死循环。`isAccessibilityTool="false"` 是如实声明，并非伪造。

5. **辅助引导是如实告知，没有诱导**：电池优化引导是 [P0.c.onClick()](<resource-unit:#1.dex1 code:P0.c#onClick>) 跳 `IGNORE_BATTERY_OPTIMIZATION_SETTINGS`；[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 的 description 与 strings 里的四条分步说明（`text_accessibility_permission` / `text_power_permission` / `text_rom_battery` / `text_task_manager`）都是如实告知操作路径。About 页外链 `https://touchhelper.zfdang.com/` 依赖浏览器打开，应用本身无 INTERNET 权限。

**结论：未发现诱导或强制开启无障碍的恶意模式，无需登记风险。**

```json
{
  "static_visibility": "clear",
  "visibility_note": "无壳、无加密载荷、无动态加载与远端下发；权限申请链路全部为本地原生代码与 strings.xml 明文，Manifest 无 INTERNET 权限，故无远端 WebView 或云控开关可藏。",
  "summary_one_liner": "冷启动首页在服务未开启且未同意时弹出可取消的透明披露对话框，用户点“同意并前往设置”后才跳系统 ACTION_ACCESSIBILITY_SETTINGS，全程如实告知读取范围并承诺不联网，无遮罩、无死循环、无受限设置教学。",
  "disguise_identity": {
    "app_display_name": "开屏跳过",
    "claimed_brand_or_persona": "开屏跳过（com.zfdang.touchhelper，作者 Zhengfa Dang，F-Droid 开源项目）",
    "a11y_service_label": "开屏跳过-无障碍服务",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅有常规 R8 短名混淆（P0.a/P0.c 等），无空白或换行挤出警告、无同形字、无多 activity-alias 伪装、未伪造 isAccessibilityTool（如实设为 false）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.zfdang.touchhelper.MainActivity（NavHost + BottomNavigationView）→ HomeFragment",
      "trigger_event": "onCreate → setContentView(activity_main) → NavHost 挂载 HomeFragment.onCreateView → g() 刷新服务与电池优化状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "开屏跳过（@string/app_name）",
      "shown_text_zh": "桌面与标题栏显示“开屏跳过”",
      "user_action_requested": "无强制动作，可直接浏览首页",
      "code_anchor": "com.zfdang.touchhelper.MainActivity#onCreate / com.zfdang.touchhelper.ui.home.HomeFragment#onCreateView, #g / res/layout/activity_main.xml"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MaterialAlertDialog（MaterialAlertDialogBuilder，标题+正文+三按钮）",
      "trigger_event": "HomeFragment.onResume：当 TouchHelperService.b() 为 false（服务未连接）且 SharedPreferences 中 ACCESSIBILITY_DISCLOSURE_ACCEPTED 为 false 时调用 h() 弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "开启无障碍服务前请了解 / \"开屏跳过\"通过安卓无障碍服务读取当前屏幕上的界面内容（控件文字、描述和位置），用于识别并自动点击开屏广告的\"跳过\"按钮。· 自动识别时，这些内容只在本机内存中即时比对，不保存。· 当您使用\"添加程序的跳过方法\"时，您所选控件的文字、描述和坐标会作为规则保存在本机的应用数据中，可在设置中查看或删除。· 当您使用\"复制窗口控件\"时，当前窗口的控件信息会按您的操作复制到系统剪贴板。本程序不申请网络权限，不会收集或上传任何数据。同意后即可开启无障碍服务；未同意前服务不会读取任何界面内容。 [同意并前往设置] [取消]",
      "shown_text_zh": "开启无障碍服务前请了解：说明无障碍服务读取的是屏幕控件文字/描述/位置，仅本机内存即时比对不保存；自定义规则保存在本机可删除；复制控件信息仅进入系统剪贴板；不申请网络权限、不上传数据；未同意前不读取任何界面内容。按钮为“同意并前往设置”与“取消”",
      "user_action_requested": "可点“同意并前往设置”进入系统无障碍设置，或点“取消”关闭（无死循环）；服务已开启时按钮变为“同意”仅作确认",
      "code_anchor": "com.zfdang.touchhelper.ui.home.HomeFragment#h / res/values/strings.xml accessibility_disclosure_title(0x7f110024)、accessibility_disclosure_message(0x7f110022)、accessibility_disclosure_agree(0x7f11001f)、accessibility_disclosure_agree_only(0x7f110020)、accessibility_disclosure_cancel(0x7f110021)"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（Intent + FLAG_ACTIVITY_NEW_TASK）",
      "trigger_event": "用户点击对话框正向按钮 → P0.a.onClick(DialogInterface, int)：先写入 ACCESSIBILITY_DISCLOSURE_ACCEPTED=true，若服务已连接则直接 return，否则 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用自身不渲染该页）",
      "shown_text_zh": "跳转至系统“无障碍”设置列表",
      "user_action_requested": "由用户自行在系统列表中手动开启“开屏跳过-无障碍服务”",
      "code_anchor": "P0.a#onClick / com.zfdang.touchhelper.f#<clinit>（读取 ACCESSIBILITY_DISCLOSURE_ACCEPTED）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍列表中的服务条目（label + android:description）",
      "trigger_event": "用户在系统无障碍列表查看该服务说明",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "开屏跳过-无障碍服务 / \"开屏跳过\"是基于安卓系统的无障碍服务来实现自动跳过广告功能的，为了保证程序能正常工作，打开此服务。\n\n本程序为开源程序，不需要网络权限，不会收集或上传任何个人信息，请放心使用！",
      "shown_text_zh": "服务名“开屏跳过-无障碍服务”，说明为开源、无需网络权限、不收集上传个人信息；未叠放任何悬浮窗或仿系统开关页",
      "user_action_requested": "用户手动打开开关（应用不叠遮罩、不代点）",
      "code_anchor": "res/xml/accessibility_service_config.xml / res/values/strings.xml touch_helper_service_label、touch_helper_service_description"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "回到 HomeFragment.onResume 的二次确认 Dialog（仅“同意”按钮）",
      "trigger_event": "用户授权后返回应用触发 onResume：TouchHelperService.b() 为 true 且 ACCESSIBILITY_DISCLOSURE_ACCEPTED 仍为 false → h() 再次弹窗，正按钮文本为 accessibility_disclosure_agree_only",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "开启无障碍服务前请了解 / ……本程序不申请网络权限，不会收集或上传任何数据。同意后即可开启无障碍服务；未同意前服务不会读取任何界面内容。 [同意] [取消]",
      "shown_text_zh": "授权后补做一次披露确认，点“同意”仅写标志位，不再次跳设置、不自动点击系统开关",
      "user_action_requested": "点“同意”完成确认（P0.a.onClick 中 z=true 时直接 return，不再 startActivity）",
      "code_anchor": "com.zfdang.touchhelper.ui.home.HomeFragment#onResume, #h / P0.a#onClick"
    },
    {
      "step": 6,
      "stage": "业务功能触发",
      "screen_or_component": "首页/设置页的电池优化与后台保活引导（IGNORE_BATTERY_OPTIMIZATION_SETTINGS 跳转）",
      "trigger_event": "用户点击首页电池优化项 → P0.c.onClick(case 0) 构造 ACTION IGNORE_BATTERY_OPTIMIZATION_SETTINGS 并 startActivity；g() 用 isIgnoringBatteryOptimizations 显示状态",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "\"开屏跳过\"基于安卓系统的无障碍服务来实现跳过自动广告功能，开源不联网，绝对安全！为保证程序能正常工作，请检查以下设置：1. 在\"无障碍\"设置里，打开\"开屏跳过 - 无障碍服务\"。2. 在\"电池优化\"设置里，设置\"开屏跳过\"为\"不优化\"。3. 在电池管理里，设置\"开屏跳过\"为\"允许后台耗电\"。…… 4. 在\"任务管理\"里，锁定\"开屏跳过\"。",
      "shown_text_zh": "以文字步骤如实告知需开启无障碍、关闭电池优化、允许后台耗电、锁定任务，均为用户主动点击的独立跳转",
      "user_action_requested": "用户自行逐项前往系统页面设置，可随时跳过",
      "code_anchor": "P0.c#onClick / com.zfdang.touchhelper.ui.home.HomeFragment#g / res/values/strings.xml text_instructions、text_accessibility_permission、text_power_permission、text_rom_battery、text_task_manager"
    }
  ],
  "text_presentation_locations": [
    "HomeFragment 的 MaterialAlertDialog（标题“开启无障碍服务前请了解”+ accessibility_disclosure_message 正文+“同意并前往设置/同意/取消”三按钮），非全屏、可取消",
    "系统“无障碍”设置列表中的服务条目：label=开屏跳过-无障碍服务，说明=android:description（@string/touch_helper_service_description）",
    "应用首页/设置页内的说明区块（res/layout 中 id 为 text_instructions、text_accessibility_permission、text_power_permission、text_rom_battery、text_task_manager 的文本）",
    "关于页（AboutFragment，res/layout/fragment_about.xml）：about_app_introduction 功能说明、about_copyright、about_privacy_policy 与 about_weblink（https://touchhelper.zfdang.com/ 由浏览器打开，非应用内 WebView）",
    "Manifest 与 strings 中的无障碍披露提示文本 accessibility_disclosure_reminder：“开屏跳过：请打开应用并确认无障碍服务说明后，跳过功能才会开始工作”（用于提醒，不作为强制拦截）"
  ],
  "verbatim_texts": [
    {
      "lang": "zh",
      "text_verbatim": "开启无障碍服务前请了解",
      "text_zh": "开启无障碍服务前请了解",
      "source_location": "res/values/strings.xml accessibility_disclosure_title (0x7f110024)",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "\"开屏跳过\"通过安卓无障碍服务读取当前屏幕上的界面内容（控件文字、描述和位置），用于识别并自动点击开屏广告的\"跳过\"按钮。· 自动识别时，这些内容只在本机内存中即时比对，不保存。· 当您使用\"添加程序的跳过方法\"时，您所选控件的文字、描述和坐标会作为规则保存在本机的应用数据中，可在设置中查看或删除。· 当您使用\"复制窗口控件\"时，当前窗口的控件信息会按您的操作复制到系统剪贴板。本程序不申请网络权限，不会收集或上传任何数据。同意后即可开启无障碍服务；未同意前服务不会读取任何界面内容。",
      "text_zh": "披露无障碍读取范围与本地处理方式，声明不申请网络权限、不收集上传数据，未同意前不读取界面内容",
      "source_location": "res/values/strings.xml accessibility_disclosure_message (0x7f110022) / HomeFragment#h",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "同意并前往设置 / 同意 / 取消",
      "text_zh": "同意并前往设置、同意、取消（存在明确取消出口）",
      "source_location": "res/values/strings.xml accessibility_disclosure_agree(0x7f11001f)、accessibility_disclosure_agree_only(0x7f110020)、accessibility_disclosure_cancel(0x7f110021)",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "\"开屏跳过\"是基于安卓系统的无障碍服务来实现自动跳过广告功能的，为了保证程序能正常工作，打开此服务。\n\n本程序为开源程序，不需要网络权限，不会收集或上传任何个人信息，请放心使用！",
      "text_zh": "系统无障碍列表中如实说明服务用途为自动跳过广告，并声明开源、不联网、不收集个人信息",
      "source_location": "res/values/strings.xml touch_helper_service_description / res/xml/accessibility_service_config.xml android:description",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "zh",
      "text_verbatim": "\"开屏跳过\"基于安卓系统的无障碍服务来实现跳过自动广告功能，开源不联网，绝对安全！为保证程序能正常工作，请检查以下设置：1. 在\"无障碍\"设置里，打开\"开屏跳过 - 无障碍服务\"。2. 在\"电池优化\"设置里，设置\"开屏跳过\"为\"不优化\"。3. 在电池管理里，设置\"开屏跳过\"为\"允许后台耗电\"。设置方法因品牌不同有所差异，比如VIVO系统为：\"设置\" -> \"电池\" -> \"后台耗电管理\"。4. 在\"任务管理\"里，锁定\"开屏跳过\"。",
      "text_zh": "分步告知无障碍、电池优化、后台耗电与任务锁定的设置路径，属常规保活引导而非绕过安全限制",
      "source_location": "res/values/strings.xml text_instructions、text_accessibility_permission、text_power_permission、text_rom_battery、text_task_manager",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "开屏跳过：请打开应用并确认无障碍服务说明后，跳过功能才会开始工作",
      "text_zh": "提醒用户需先确认披露说明，服务才会开始工作",
      "source_location": "res/values/strings.xml accessibility_disclosure_reminder",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无死循环：取消按钮无监听器仅关闭对话框；onResume 仅当无障碍服务已连接且尚未同意披露时才再次弹窗（用于授权后补确认），未授权时返回应用不会反复强制拉起，也不会定时重跳系统设置",
    "overlay_or_fake_settings": "无。Manifest 无 SYSTEM_ALERT_WINDOW 权限，代码无 requestAddView/WindowManager 悬浮窗，未仿制系统无障碍开关页；跳转后由系统设置页自行展示",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。未监听设置页做 GLOBAL_ACTION_BACK/HOME 阻止撤权，未自点系统开关确认；isAccessibilityTool 如实为 false",
    "benign_graceful_degradation": "有：用户可取消披露对话框并继续浏览首页与设置；首页通过 g() 显示“服务未开启”状态，仅在用户主动点击时才跳转系统设置；关于页提供功能说明与隐私政策链接供用户判断"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动进入 MainActivity/HomeFragment 且无障碍服务未连接时（onResume → h()）首个 MaterialAlertDialog 出现瞬间；以及用户点击正向按钮后 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的跳转瞬间",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动披露引导弹窗页",
        "page_identifier": "应用包 com.zfdang.touchhelper 内的系统 Dialog，标题“开启无障碍服务前请了解”，按钮“同意并前往设置 / 取消”",
        "why_most_useful": "该页决定用户是否被要求授权，可直接区分“透明披露+可取消”与“不可取消强迫授权”",
        "observable_utg_signals": ["弹窗是否可关闭（存在“取消”按钮节点）", "正文是否说明读取范围与不联网承诺", "标题与桌面应用名/服务名是否一致（无身份混淆）"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍列表中出现“开屏跳过-无障碍服务”及其 description 文本",
        "why_most_useful": "核对应用是否叠放遮罩/悬浮窗引导或伪造开关页，并验证 label 与说明的真实性",
        "observable_utg_signals": ["列表项文本与服务说明原文", "是否存在应用侧悬浮窗/半透明遮罩覆盖系统页", "开关状态是否被应用代点（无 GLOBAL_ACTION 点击痕迹）"]
      },
      {
        "page_role": "授权返回后的二次确认弹窗",
        "page_identifier": "HomeFragment.onResume 触发的对话框，正按钮文本为“同意”",
        "why_most_useful": "验证获权后是补做披露确认还是执行对抗/反复跳转",
        "observable_utg_signals": ["按钮文本是否为“同意”而非“前往设置”", "是否出现再次跳转系统设置或循环弹窗", "弹窗后是否停留在首页（无强制停留/阻止退出）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：无纯图引导、无远端 HTML（应用无 INTERNET 权限）、无加壳与一阶段 Dropper；仅存在常规 R8 短名混淆，不影响运行期 UTG 判定。"
  },
  "behavior_pattern_tags": [
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "com.zfdang.touchhelper.ui.home.HomeFragment#onResume",
    "com.zfdang.touchhelper.ui.home.HomeFragment#h",
    "P0.a#onClick",
    "P0.c#onClick",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml accessibility_disclosure_message"
  ]
}
```

</details>
