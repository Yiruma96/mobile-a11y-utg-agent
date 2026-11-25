# BN_031__7fb711c88d｜极简桌面与双击锁屏 — Minimo Launcher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：145.5s

## 1. 一句话核心结论

- **核心申请方式**：Minimo Launcher 仅在用户主动开启「双击锁屏」开关时，用原生 Compose 弹窗说明用途并显式声明不收集数据，随后直接跳转系统无障碍设置页，返回后只读校验授权状态、未授权则保持关闭，权限范围为零事件监听加锁屏全局动作。
- **静态可见性说明**：无障碍引导全链路静态可见：入口开关 lambda（j10.a）、跳转实现（qy.D）、状态校验（qy.r）、回读校验（r8.a）、说明文案（strings.xml: enable_accessibility_dialog_title/message、enable_accessibility_permission_for_minimo）、服务配置（res/xml/accessibility_service_config.xml）均可直接反编译确认；无加壳、无加密载荷、无 WebView/远端 HTML 参与该流程。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `7fb711c88da575a836de8f4d200b0a4abbea6dc09f255e54ba228beb46660292` |
| 包名 / 年份 | `com.minimo.launcher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://apt.izzysoft.de/fdroid/repo/com.minimo.launcher_161.apk |
| 桌面显示名 | Minimo Launcher |
| 引导页宣称品牌/身份 | Minimo（IzzyOnDroid 开源极简桌面，真实身份） |
| 系统无障碍列表服务名 | Minimo Launcher（服务未单独声明 android:label，继承 application 的 @string/app_name） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅存在 R8 常规混淆（类名如 qy/j10/r8/zd），未用于无障碍引导的身份伪装；无空白/换行挤出、无同形字、无多 activity-alias、无伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.minimo.launcher.utils.MinimoAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `BIND_NOTIFICATION_LISTENER_SERVICE, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Accessibility permission is needed for double tap to turn off the screen |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.minimo.launcher.ui.main.MainActivity（HOME/LAUNCHER，singleTask） | onCreate / 作为桌面冷启动 | 原生Activity | 无 | 无（可直接使用桌面） | `com.minimo.launcher.ui.main.MainActivity` |
| 2 | 业务功能触发 | 设置页「Double Tap To Lock」开关（Compose 设置界面，string double_tap_to_lock） | 用户手动点击该开关（onClick 回调 lambda j10.a，case 0 分支） | 原生Activity | **原文**：Double Tap To Lock<br>**译注**：双击锁屏（开关项名称） | 用户自行选择是否开启该功能；不开启则不涉及任何无障碍权限 | `j10.a / strings.xml: double_tap_to_lock` |
| 3 | 引导说明页 | 原生 Compose AlertDialog（组合 lambda zd.h case 15/16 渲染标题与正文，含 Back 返回控件） | 开关点击后立即弹出说明弹窗 | 原生Dialog | **原文**：Enable Accessibility / Accessibility permission is required for double tap to turn off the screen.<br>No data is being collected during the process.<br><br>To allow the permission, enable accessibility for %s in the settings.<br>**译注**：开启无障碍 / 双击熄屏需要无障碍权限。此过程中不会收集任何数据。若要授予该权限，请在设置中为 %s 开启无障碍。 | 阅读后确认继续（弹窗内另有 Back 返回控件，可退出不授权） | `zd.h（2131689588=enable_accessibility_dialog_title，2131689587=enable_accessibility_dialog_message）/ res/values/strings.xml#L80-L85` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 确认后 qy.D 先 Toast 再 startActivity（FLAG_ACTIVITY_NEW_TASK） | 系统无障碍页 | **原文**：Enable accessibility permission for Minimo<br>**译注**：为 Minimo 开启无障碍权限（跳转前 Toast 提示） | 在系统无障碍列表中找到 Minimo Launcher 并手动开启；无自动点击、无遮罩叠层 | `qy.D / strings.xml: enable_accessibility_permission_for_minimo` |
| 5 | 引导说明页（系统侧描述） | 系统无障碍服务列表项描述（res/xml/accessibility_service_config.xml android:description） | 用户在系统无障碍页展开 Minimo Launcher 条目 | 系统无障碍页 | **原文**：Accessibility permission is needed for double tap to turn off the screen<br>**译注**：双击关闭屏幕需要无障碍权限 | 核对说明后决定是否启用 | `res/xml/accessibility_service_config.xml / strings.xml: accessibility_service_description` |
| 6 | 拒权反馈循环 | 返回应用后 r8.a 回读 Settings.Secure.enabled_accessibility_services（经 qy.r 比对 ComponentName） | 从系统设置返回，开关状态刷新回调 | 原生Activity | 无 | 可放弃该功能或稍后再次手动开启 | `r8.a / qy.r` |
| 7 | 获权后动作 | com.minimo.launcher.utils.MinimoAccessibilityService | onServiceConnected()：eventTypes=0、packageNames 为空并保存单例 e | 不可静态还原（服务无 UI） | 无 | 无 | `MinimoAccessibilityService.onServiceConnected / onAccessibilityEvent（空实现）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 设置页「Double Tap To Lock」开关项文字（strings.xml: double_tap_to_lock），为用户主动进入的功能入口
- 原生 Compose AlertDialog：标题 enable_accessibility_dialog_title「Enable Accessibility」+ 正文 enable_accessibility_dialog_message（含「No data is being collected during the process」隐私声明与操作指引），由 zd.h 组合 lambda 渲染
- 跳转前系统 Toast：enable_accessibility_permission_for_minimo「Enable accessibility permission for Minimo」（qy.D 内 Toast.makeText）
- 系统无障碍服务列表项描述：res/xml/accessibility_service_config.xml 的 android:description = accessibility_service_description
- Android <28 降级路径 Toast 与设备管理器说明：enable_device_admin_first / ADD_DEVICE_ADMIN 的 ADD_EXPLANATION 文案
- 全程无 assets HTML、无 WebView、无悬浮窗遮罩承载引导文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable Accessibility | 开启无障碍 | `res/values/strings.xml key=enable_accessibility_dialog_title` | 良性透明说明 |
| en | Accessibility permission is required for double tap to turn off the screen.<br>No data is being collected during the process.<br><br>To allow the permission, enable accessibility for %s in the settings. | 双击熄屏需要无障碍权限。此过程中不会收集任何数据。若要授予该权限，请在设置中为 %s 开启无障碍。 | `res/values/strings.xml key=enable_accessibility_dialog_message` | 良性透明说明 |
| en | Enable accessibility permission for Minimo | 为 Minimo 开启无障碍权限 | `res/values/strings.xml key=enable_accessibility_permission_for_minimo（qy.D 中 Toast 使用）` | 良性透明说明 |
| en | Accessibility permission is needed for double tap to turn off the screen | 双击关闭屏幕需要无障碍权限 | `res/xml/accessibility_service_config.xml android:description → strings.xml key=accessibility_service_description` | 良性透明说明 |
| en | Double Tap To Lock | 双击锁屏 | `res/values/strings.xml key=double_tap_to_lock` | 良性透明说明 |
| en | Enable Device Admin First! | 请先启用设备管理器！ | `res/values/strings.xml key=enable_device_admin_first（Android <28 降级路径）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。从系统设置返回后 r8.a 读取 Settings.Secure.enabled_accessibility_services（经 qy.r 与 ComponentName 比对）仅更新开关状态；未授权则开关保持关闭、停留在设置页，不重复跳转、无定时器拉起。
- **遮罩叠层 / 高仿系统设置页**：无。未申请 SYSTEM_ALERT_WINDOW，DEX 中无 TYPE_APPLICATION_OVERLAY / WindowManager 遮罩，也无高仿系统无障碍开关页；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现跳转 ACTION_APPLICATION_DETAILS_SETTINGS、未发现「允许受限设置」分步教学，也未发现 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。服务 onServiceConnected 不订阅事件、不监听设置页，未发现 GLOBAL_ACTION_BACK/HOME 阻止撤权或自授权确认行为。
- **良性降级 / 替代方案**：有。Android <28 自动降级为设备管理器（ScreenOffAdminReceiver + ADD_DEVICE_ADMIN + ADD_EXPLANATION 说明）；未授权时双击锁屏功能保持不可用，桌面其余功能正常使用。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在设置页点击「Double Tap To Lock」开关的瞬间拉起 UTG（随后出现 Compose AlertDialog），并在监测到 startActivity("android.settings.ACCESSIBILITY_SETTINGS") 后继续采样系统设置页与返回后的设置页；冷启动与 MainActivity onResume 无需采集。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。该应用无障碍引导完全由原生 Compose 弹窗 + 系统设置跳转承载，无 WebView、无图片引导、无加壳；唯一静态不可见处为 R8 混淆后的 lambda 类名，但不影响运行期 UTG 文本提取。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **引导说明弹窗页** | Compose AlertDialog，标题文本 Enable Accessibility，正文含 No data is being collected during the process | 此处能判断说明是否如实、是否含恐吓/假更新/隐私空头承诺，以及是否存在可取消控件 | 标题与正文完整文本；是否存在 Cancel/Back 可点控件；弹窗是否可返回键关闭 |
| **跳转前状态（Toast + 目标 Intent）** | Toast 文本 Enable accessibility permission for Minimo，随后前台切换为设置包 com.android.settings 的无障碍页 | 确认跳转目标为真实系统无障碍设置页而非伪造同名页面 | 前台包名为 com.android.settings；页面标题/列表项含无障碍服务开关；无悬浮窗覆盖设置页 |
| **系统无障碍服务列表项** | 列表项文本 Minimo Launcher 与描述 Accessibility permission is needed for double tap to turn off the screen | 核对系统侧展示的服务名与描述是否与应用真实身份、用途一致 | 服务名文本；描述文本；是否与包名/品牌一致 |
| **拒权返回后的设置页** | 返回 Minimo 设置页，Double Tap To Lock 开关保持关闭 | 确认无拒权死循环重跳、无强制阻断 | 页面停留在应用设置页；开关状态为关闭；短时间内无重复 startActivity 到设置页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `qy.D`
- `qy.r`
- `j10.a`
- `r8.a`
- `com.minimo.launcher.utils.MinimoAccessibilityService.onServiceConnected`
- `res/values/strings.xml#L80-L85`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**结论：这是一个良性的开源极简桌面应用，其无障碍权限引导流程透明、按需触发、可以取消，未发现诱导、恐吓、遮罩或拒权循环。**

- **入口只由用户操作触发**：`MainActivity` 作为 HOME/launcher 冷启动时不会弹出任何无障碍引导；只有当用户在设置页打开「Double Tap To Lock」（双击锁屏）开关时，才会触发 [j10.a](<resource-unit:#1.dex1 code:j10#a>) 调用 [qy.D()](<resource-unit:#1.dex1 code:qy#D>)。
- **说明文字出现在原生 Compose 弹窗中**：标题为 `Enable Accessibility`，正文为「双击熄屏需要无障碍权限，过程中不收集任何数据；请在设置中为 %s 开启无障碍」，弹窗内同时渲染了 `Back` 返回控件，没有“取消/跳过即失败”式的强制文案。
- **跳转前先显示 Toast**：`qy.D` 先用 Toast 显示 `Enable accessibility permission for Minimo`，然后执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").setFlags(FLAG_ACTIVITY_NEW_TASK))` 跳转到系统无障碍设置页；应用没有伪造设置页，也没有使用悬浮窗遮罩（`SYSTEM_ALERT_WINDOW` 未声明，DEX 中没有 `TYPE_APPLICATION_OVERLAY`/`WebView`）。
- **降级路径明确**：Android < 28 时不引导无障碍，而是改为申请设备管理器（`ADD_DEVICE_ADMIN` + `Enable Device Admin First!`）。
- **用户拒绝后不会陷入循环**：返回后由 [r8.a](<resource-unit:#1.dex1 code:r8#a>) 通过 `Settings.Secure.enabled_accessibility_services` 只读校验，然后更新开关状态；未获权时开关保持关闭，不会反复拉起设置页。
- **权限范围最小化**：`MinimoAccessibilityService.onServiceConnected` 将 `eventTypes = 0`、`packageNames = 空`，不监听任何无障碍事件；该服务只作为执行 `GLOBAL_ACTION_LOCK_SCREEN` 的载体（预筛命中 `PERFORM_GLOBAL_ACTION`，单例 `MinimoAccessibilityService.e` 被 `g.i` 使用），不存在读屏抓取或自动点击。
- **未发现的身份伪装**：无障碍服务没有单独设置 `android:label`，系统列表显示继承的应用名 `Minimo Launcher`，`android:description` 与实际用途一致；没有 `isAccessibilityTool` 伪造、没有多 activity-alias、没有空白/换行挤出或同形字。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路静态可见：入口开关 lambda（j10.a）、跳转实现（qy.D）、状态校验（qy.r）、回读校验（r8.a）、说明文案（strings.xml: enable_accessibility_dialog_title/message、enable_accessibility_permission_for_minimo）、服务配置（res/xml/accessibility_service_config.xml）均可直接反编译确认；无加壳、无加密载荷、无 WebView/远端 HTML 参与该流程。",
  "summary_one_liner": "Minimo Launcher 仅在用户主动开启「双击锁屏」开关时，用原生 Compose 弹窗说明用途并显式声明不收集数据，随后直接跳转系统无障碍设置页，返回后只读校验授权状态、未授权则保持关闭，权限范围为零事件监听加锁屏全局动作。",
  "disguise_identity": {
    "app_display_name": "Minimo Launcher",
    "claimed_brand_or_persona": "Minimo（IzzyOnDroid 开源极简桌面，真实身份）",
    "a11y_service_label": "Minimo Launcher（服务未单独声明 android:label，继承 application 的 @string/app_name）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅存在 R8 常规混淆（类名如 qy/j10/r8/zd），未用于无障碍引导的身份伪装；无空白/换行挤出、无同形字、无多 activity-alias、无伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.minimo.launcher.ui.main.MainActivity（HOME/LAUNCHER，singleTask）",
      "trigger_event": "onCreate / 作为桌面冷启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动直接进入极简桌面，无任何无障碍权限弹窗或全屏引导",
      "user_action_requested": "无（可直接使用桌面）",
      "code_anchor": "com.minimo.launcher.ui.main.MainActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "设置页「Double Tap To Lock」开关（Compose 设置界面，string double_tap_to_lock）",
      "trigger_event": "用户手动点击该开关（onClick 回调 lambda j10.a，case 0 分支）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Double Tap To Lock",
      "shown_text_zh": "双击锁屏（开关项名称）",
      "user_action_requested": "用户自行选择是否开启该功能；不开启则不涉及任何无障碍权限",
      "code_anchor": "j10.a / strings.xml: double_tap_to_lock"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "原生 Compose AlertDialog（组合 lambda zd.h case 15/16 渲染标题与正文，含 Back 返回控件）",
      "trigger_event": "开关点击后立即弹出说明弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Accessibility / Accessibility permission is required for double tap to turn off the screen.\nNo data is being collected during the process.\n\nTo allow the permission, enable accessibility for %s in the settings.",
      "shown_text_zh": "开启无障碍 / 双击熄屏需要无障碍权限。此过程中不会收集任何数据。若要授予该权限，请在设置中为 %s 开启无障碍。",
      "user_action_requested": "阅读后确认继续（弹窗内另有 Back 返回控件，可退出不授权）",
      "code_anchor": "zd.h（2131689588=enable_accessibility_dialog_title，2131689587=enable_accessibility_dialog_message）/ res/values/strings.xml#L80-L85"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "确认后 qy.D 先 Toast 再 startActivity（FLAG_ACTIVITY_NEW_TASK）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable accessibility permission for Minimo",
      "shown_text_zh": "为 Minimo 开启无障碍权限（跳转前 Toast 提示）",
      "user_action_requested": "在系统无障碍列表中找到 Minimo Launcher 并手动开启；无自动点击、无遮罩叠层",
      "code_anchor": "qy.D / strings.xml: enable_accessibility_permission_for_minimo"
    },
    {
      "step": 5,
      "stage": "引导说明页（系统侧描述）",
      "screen_or_component": "系统无障碍服务列表项描述（res/xml/accessibility_service_config.xml android:description）",
      "trigger_event": "用户在系统无障碍页展开 Minimo Launcher 条目",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility permission is needed for double tap to turn off the screen",
      "shown_text_zh": "双击关闭屏幕需要无障碍权限",
      "user_action_requested": "核对说明后决定是否启用",
      "code_anchor": "res/xml/accessibility_service_config.xml / strings.xml: accessibility_service_description"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回应用后 r8.a 回读 Settings.Secure.enabled_accessibility_services（经 qy.r 比对 ComponentName）",
      "trigger_event": "从系统设置返回，开关状态刷新回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "未授权时开关回到关闭状态，停留在设置页，不重复拉起无障碍设置，无死循环",
      "user_action_requested": "可放弃该功能或稍后再次手动开启",
      "code_anchor": "r8.a / qy.r"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.minimo.launcher.utils.MinimoAccessibilityService",
      "trigger_event": "onServiceConnected()：eventTypes=0、packageNames 为空并保存单例 e",
      "ui_carrier": "不可静态还原（服务无 UI）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务不订阅任何无障碍事件，仅在用户双击桌面时执行全局动作锁屏（GLOBAL_ACTION_LOCK_SCREEN）",
      "user_action_requested": "无",
      "code_anchor": "MinimoAccessibilityService.onServiceConnected / onAccessibilityEvent（空实现）"
    }
  ],
  "text_presentation_locations": [
    "设置页「Double Tap To Lock」开关项文字（strings.xml: double_tap_to_lock），为用户主动进入的功能入口",
    "原生 Compose AlertDialog：标题 enable_accessibility_dialog_title「Enable Accessibility」+ 正文 enable_accessibility_dialog_message（含「No data is being collected during the process」隐私声明与操作指引），由 zd.h 组合 lambda 渲染",
    "跳转前系统 Toast：enable_accessibility_permission_for_minimo「Enable accessibility permission for Minimo」（qy.D 内 Toast.makeText）",
    "系统无障碍服务列表项描述：res/xml/accessibility_service_config.xml 的 android:description = accessibility_service_description",
    "Android <28 降级路径 Toast 与设备管理器说明：enable_device_admin_first / ADD_DEVICE_ADMIN 的 ADD_EXPLANATION 文案",
    "全程无 assets HTML、无 WebView、无悬浮窗遮罩承载引导文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility",
      "text_zh": "开启无障碍",
      "source_location": "res/values/strings.xml key=enable_accessibility_dialog_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility permission is required for double tap to turn off the screen.\nNo data is being collected during the process.\n\nTo allow the permission, enable accessibility for %s in the settings.",
      "text_zh": "双击熄屏需要无障碍权限。此过程中不会收集任何数据。若要授予该权限，请在设置中为 %s 开启无障碍。",
      "source_location": "res/values/strings.xml key=enable_accessibility_dialog_message",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable accessibility permission for Minimo",
      "text_zh": "为 Minimo 开启无障碍权限",
      "source_location": "res/values/strings.xml key=enable_accessibility_permission_for_minimo（qy.D 中 Toast 使用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility permission is needed for double tap to turn off the screen",
      "text_zh": "双击关闭屏幕需要无障碍权限",
      "source_location": "res/xml/accessibility_service_config.xml android:description → strings.xml key=accessibility_service_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Double Tap To Lock",
      "text_zh": "双击锁屏",
      "source_location": "res/values/strings.xml key=double_tap_to_lock",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Device Admin First!",
      "text_zh": "请先启用设备管理器！",
      "source_location": "res/values/strings.xml key=enable_device_admin_first（Android <28 降级路径）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。从系统设置返回后 r8.a 读取 Settings.Secure.enabled_accessibility_services（经 qy.r 与 ComponentName 比对）仅更新开关状态；未授权则开关保持关闭、停留在设置页，不重复跳转、无定时器拉起。",
    "overlay_or_fake_settings": "无。未申请 SYSTEM_ALERT_WINDOW，DEX 中无 TYPE_APPLICATION_OVERLAY / WindowManager 遮罩，也无高仿系统无障碍开关页；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无。未发现跳转 ACTION_APPLICATION_DETAILS_SETTINGS、未发现「允许受限设置」分步教学，也未发现 Session 安装器绕过。",
    "post_grant_anti_removal": "无。服务 onServiceConnected 不订阅事件、不监听设置页，未发现 GLOBAL_ACTION_BACK/HOME 阻止撤权或自授权确认行为。",
    "benign_graceful_degradation": "有。Android <28 自动降级为设备管理器（ScreenOffAdminReceiver + ADD_DEVICE_ADMIN + ADD_EXPLANATION 说明）；未授权时双击锁屏功能保持不可用，桌面其余功能正常使用。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在设置页点击「Double Tap To Lock」开关的瞬间拉起 UTG（随后出现 Compose AlertDialog），并在监测到 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\") 后继续采样系统设置页与返回后的设置页；冷启动与 MainActivity onResume 无需采集。",
    "key_pages_to_capture": [
      {
        "page_role": "引导说明弹窗页",
        "page_identifier": "Compose AlertDialog，标题文本 Enable Accessibility，正文含 No data is being collected during the process",
        "why_most_useful": "此处能判断说明是否如实、是否含恐吓/假更新/隐私空头承诺，以及是否存在可取消控件",
        "observable_utg_signals": ["标题与正文完整文本", "是否存在 Cancel/Back 可点控件", "弹窗是否可返回键关闭"]
      },
      {
        "page_role": "跳转前状态（Toast + 目标 Intent）",
        "page_identifier": "Toast 文本 Enable accessibility permission for Minimo，随后前台切换为设置包 com.android.settings 的无障碍页",
        "why_most_useful": "确认跳转目标为真实系统无障碍设置页而非伪造同名页面",
        "observable_utg_signals": ["前台包名为 com.android.settings", "页面标题/列表项含无障碍服务开关", "无悬浮窗覆盖设置页"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "列表项文本 Minimo Launcher 与描述 Accessibility permission is needed for double tap to turn off the screen",
        "why_most_useful": "核对系统侧展示的服务名与描述是否与应用真实身份、用途一致",
        "observable_utg_signals": ["服务名文本", "描述文本", "是否与包名/品牌一致"]
      },
      {
        "page_role": "拒权返回后的设置页",
        "page_identifier": "返回 Minimo 设置页，Double Tap To Lock 开关保持关闭",
        "why_most_useful": "确认无拒权死循环重跳、无强制阻断",
        "observable_utg_signals": ["页面停留在应用设置页", "开关状态为关闭", "短时间内无重复 startActivity 到设置页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。该应用无障碍引导完全由原生 Compose 弹窗 + 系统设置跳转承载，无 WebView、无图片引导、无加壳；唯一静态不可见处为 R8 混淆后的 lambda 类名，但不影响运行期 UTG 文本提取。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "qy.D",
    "qy.r",
    "j10.a",
    "r8.a",
    "com.minimo.launcher.utils.MinimoAccessibilityService.onServiceConnected",
    "res/values/strings.xml#L80-L85"
  ]
}
```

</details>
