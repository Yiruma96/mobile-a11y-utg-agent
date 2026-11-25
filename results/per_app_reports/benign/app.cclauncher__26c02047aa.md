# BN_023__26c02047aa｜极简桌面与双击锁屏 — CClauncher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：183.1s

## 1. 一句话核心结论

- **核心申请方式**：CClauncher 仅在用户于设置页开启“双击锁屏”时弹出原生 Compose 说明对话框，透明告知无障碍仅用于锁屏且不采集数据，用户确认后才跳转系统无障碍设置页手动开启，无遮罩、无循环、无诱导。
- **静态可见性说明**：DEX 未加壳（apkid 初判 False），无障碍服务、说明弹窗与设置跳转全部为可反编译的 Kotlin/Compose 实现；仅有 R8 生成的 ExternalSyntheticLambda 名称混淆，无加密载荷、无远端 HTML 引导页。弹窗按钮文案的资源 key 未在本次调用预算内逐一定位，属资源文字细节。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `26c02047aaaaa84ab51882244d6d0fe28b4869999db781f18ddca9182bf5986d` |
| 包名 / 年份 | `app.cclauncher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/app.cclauncher_1450.apk |
| 桌面显示名 | CClauncher |
| 引导页宣称品牌/身份 | CClauncher（F-Droid 开源极简桌面，真实身份） |
| 系统无障碍列表服务名 | CClauncher |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。R8 仅生成 ExternalSyntheticLambda 类名混淆，属常规编译产物；服务标签直接引用 @string/app_name，未使用空白/换行挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool |
| 无障碍服务类名 | `app.cclauncher.helper.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | The accessibility permission is required to enable double tap to lock. Any data acquired by CClauncher via this service will not leave your device. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | app.cclauncher.MainActivity（HOME 桌面）→ 设置界面 Compose SettingsScreen | 用户在设置页操作“Double Tap to Lock Screen”开关（设置项 key: cclauncher.settings.setting_double_tap_to_lock_screen），SettingsScreen 据此渲染说明弹窗；冷启动不触发 | 原生Activity | **原文**：Double Tap to Lock Screen<br>**译注**：双击锁屏（设置项名称） | 用户自行进入设置并打开该功能开关；不打开则不会出现任何无障碍提示，可自由返回 | `app.cclauncher.ui.screens.HomeScreenKt.SettingsScreen；app.cclauncher.settings.AppSettingsSchema.<clinit>` |
| 2 | 引导说明页 | Compose Dialog：app.cclauncher.ui.dialogs.ResizeDialogKt.AccessibilityDisclosureDialog（DialogProperties(4)） | SettingsScreen 组合阶段调用 AccessibilityDisclosureDialog(onDismiss, onConfirm, titleText)，弹窗出现 | 原生Dialog | **原文**：CClauncher accessibility service / Please turn on or off CClauncher's accessibility service in your device's settings to enable or disable this feature. Please note that this service is only used to let you turn off your device's screen using the double tap gesture. Our accessibility service does not collect or share any data. / What this service accesses: no screen content, no keystrokes, no app data, and no personal information. Nothing is collected and nothing leaves your device. / You can turn this service off at any time in Android Settings > Accessibility. / Turn on CClauncher under Accessibility > Downloaded apps (called Installed services on some devices).<br>**译注**：CClauncher 无障碍服务：请在设备设置中开启或关闭本服务以启用/停用该功能；本服务仅用于通过双击手势关闭屏幕，不收集或共享任何数据。本服务访问范围：无屏幕内容、无按键、无应用数据、无个人信息，不采集任何内容、数据不离开设备。你可随时在 设置 > 无障碍 中关闭本服务。开启路径：在“无障碍 > 已下载的应用”（部分设备称“已安装的服务”）中开启 CClauncher。 | 阅读说明后选择确认（Agree and continue）或取消/关闭弹窗；存在取消路径（onDismiss 回调），不阻断使用 | `app.cclauncher.ui.dialogs.ResizeDialogKt#AccessibilityDisclosureDialog；res/values/strings.xml（accessibility_disclosure / accessibility_disclosure_data / accessibility_disclosure_disable / accessibility_disclosure_title / accessibility_settings_hint）` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 用户在说明弹窗点击确认，触发 ResizeDialogKt$$ExternalSyntheticLambda7.invoke → context.startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(FLAG_ACTIVITY_NEW_TASK)) | 系统无障碍页 | **原文**：CClauncher（系统无障碍服务列表项，label=@string/app_name）；The accessibility permission is required to enable double tap to lock. Any data acquired by CClauncher via this service will not leave your device.<br>**译注**：系统无障碍列表显示服务名 CClauncher；描述为“启用双击锁屏需要无障碍权限，CClauncher 通过该服务获取的任何数据都不会离开你的设备”。 | 用户在系统无障碍页手动找到 CClauncher 并自行开启；是否开启完全由用户决定，可返回不开启 | `app.cclauncher.ui.dialogs.ResizeDialogKt$$ExternalSyntheticLambda7#invoke；res/xml/accessibility_service_config.xml` |
| 4 | 拒权反馈循环 | MainActivity / SettingsScreen（返回后） | 用户从系统设置返回应用；未发现 onResume 重跳、定时器拉起或监听设置页的逻辑 | 原生Activity | 无 | 无强制动作；用户可继续使用桌面其余功能，仅双击锁屏不可用 | `app.cclauncher.MainActivity$onCreate$4$1#emit（仅处理方向与 MANAGE_DEFAULT_APPS_SETTINGS，无无障碍重跳）` |
| 5 | 获权后动作 | app.cclauncher.helper.MyAccessibilityService | 服务被系统连接后 onServiceConnected 置 connected=this；双击手势触发 startService(action="LOCK_SCREEN") → onStartCommand 执行 performGlobalAction(8) 锁屏 | 原生Dialog | 无 | 无需额外操作；用户可随时在系统无障碍设置中关闭该服务，应用无阻止行为 | `app.cclauncher.helper.MyAccessibilityService#onServiceConnected；app.cclauncher.helper.MyAccessibilityService#onStartCommand；app.cclauncher.helper.MyAccessibilityService#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- SettingsScreen 内的原生 Compose Dialog（AccessibilityDisclosureDialog，DialogProperties(4)）：主说明标题 accessibility_disclosure_title、正文 accessibility_disclosure、访问范围 accessibility_disclosure_data、关闭方式 accessibility_disclosure_disable、开启路径提示 accessibility_settings_hint
- res/values/strings.xml：accessibility_service_description（呈现于系统无障碍服务列表项的描述栏）
- 系统无障碍列表服务名：AndroidManifest 中 service android:label="@string/app_name" → 显示 CClauncher
- 设置界面开关项文本：setting_double_tap_to_lock_screen（Double Tap to Lock Screen）
- 未使用 WebView / HTML / 悬浮窗 Overlay / 通知栏 承载任何无障碍引导文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | CClauncher accessibility service | CClauncher 无障碍服务 | `strings.xml key accessibility_disclosure_title` | 良性透明说明 |
| en | Please turn on or off CClauncher's accessibility service in your device's settings to enable or disable this feature. Please note that this service is only used to let you turn off your device's screen using the double tap gesture. Our accessibility service does not collect or share any data. | 请在设备设置中开启或关闭 CClauncher 的无障碍服务以启用或停用该功能。请注意，本服务仅用于让你通过双击手势关闭设备屏幕。我们的无障碍服务不收集也不共享任何数据。 | `strings.xml key accessibility_disclosure` | 良性透明说明 |
| en | What this service accesses: no screen content, no keystrokes, no app data, and no personal information. Nothing is collected and nothing leaves your device. | 本服务访问的内容：无屏幕内容、无按键记录、无应用数据、无个人信息。不收集任何内容，任何数据都不会离开你的设备。 | `strings.xml key accessibility_disclosure_data` | 隐私承诺 |
| en | You can turn this service off at any time in Android Settings > Accessibility. | 你可以随时在 Android 设置 > 无障碍 中关闭本服务。 | `strings.xml key accessibility_disclosure_disable` | 良性透明说明 |
| en | Turn on CClauncher under Accessibility > Downloaded apps (called Installed services on some devices). | 在“无障碍 > 已下载的应用”（部分设备称为“已安装的服务”）中开启 CClauncher。 | `strings.xml key accessibility_settings_hint` | 受限设置分步教学 |
| en | The accessibility permission is required to enable double tap to lock. Any data acquired by CClauncher via this service will not leave your device. | 启用双击锁屏需要无障碍权限。CClauncher 通过该服务获取的任何数据都不会离开你的设备。 | `strings.xml key accessibility_service_description（res/xml/accessibility_service_config.xml 引用）` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性降级：用户取消弹窗或从系统设置返回后不重跳、不轮询、不弹二次提示，仅双击锁屏功能保持不可用，桌面其余功能正常
- **遮罩叠层 / 高仿系统设置页**：无。未使用半透明遮罩、全屏悬浮窗或高仿系统无障碍开关页；仅跳转真实系统设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现引导进入应用详情点击右上角菜单允许受限设置，也无 Session 安装器绕过；APPLICATION_DETAILS_SETTINGS 跳转位于 SettingsScreenKt$$ExternalSyntheticLambda54，用于常规应用详情，与无障碍授权无关
- **获权后即时行为与防撤权机制**：无。onAccessibilityEvent 空实现，onServiceConnected 仅记录静态引用并启动协程，未监听设置页、未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权、未自动点击确认
- **良性降级 / 替代方案**：不开启无障碍时双击锁屏功能不可用，其余桌面功能（隐藏应用、搜索、壁纸等）照常使用；弹窗提供取消回调，说明中明确告知可随时在系统设置关闭服务

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（来源 ResizeDialogKt$$ExternalSyntheticLambda7.invoke），以及此前 SettingsScreen 内 AccessibilityDisclosureDialog 首次渲染（Dialog window 出现）时；本应用冷启动不弹无障碍引导，无需在 0 步拉起
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本应用无图文化诱导、无空文本外壳、无一阶段 Dropper、无静态加壳（静态加壳亦不影响运行期 UTG）。唯一盲区是：若设备已预先授权无障碍，则运行期不再出现说明弹窗与设置跳转，UTG 需先清除授权再复现；另外弹窗按钮的具体资源 key 未在本次预算内定位，纯文本提取应以 UI 实际渲染为准。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **设置页内无障碍说明弹窗页** | CClauncher 设置界面之上的 Compose Dialog，标题文本 'CClauncher accessibility service'，含“Agree and continue”确认按钮与取消/关闭入口 | 这是全流程唯一的授权说服点，可直接判定文案是否透明、是否具备取消路径、是否存在恐吓或假更新话术 | 弹窗标题与正文文本节点（accessibility_disclosure_title / accessibility_disclosure）；是否存在取消/返回可点节点与 Dialog 是否可外部取消；是否出现“假更新/系统故障/安全风险”类诱导词 |
| **系统无障碍服务列表项** | android.settings.ACCESSIBILITY_SETTINGS 中服务名 'CClauncher' 及其描述栏 | 核对应用向系统申报的真实服务名与描述是否与弹窗一致，识别是否存在标签伪装或描述与实际能力不符 | 列表项显示名是否等于 app_name（CClauncher）；描述文本是否与 accessibility_service_description 一致；是否存在同名多服务或可疑空白挤出名称 |
| **设置页功能开关入口页** | CClauncher 设置界面 'Double Tap to Lock Screen' 开关项 | 确认授权引导是否由用户主动开启功能触发（按需触发）而非冷启动强制，判定诱导强度 | 开关初始状态与点击后是否才出现弹窗；冷启动桌面是否无任何无障碍提示 |
| **获权后双击锁屏行为页** | 桌面双击手势后屏幕熄灭（performGlobalAction(8)） | 验证无障碍能力实际用途仅为锁屏，排除获权后执行读屏、自动点击或后台拉起其他界面的行为 | 双击后是否仅熄屏而无额外界面跳转；锁屏后是否出现自动点击/自动授权等异常动作 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `app.cclauncher.helper.MyAccessibilityService#onStartCommand`
- `app.cclauncher.helper.MyAccessibilityService#onServiceConnected`
- `app.cclauncher.ui.dialogs.ResizeDialogKt#AccessibilityDisclosureDialog`
- `app.cclauncher.ui.dialogs.ResizeDialogKt$$ExternalSyntheticLambda7#invoke`
- `app.cclauncher.ui.screens.HomeScreenKt#SettingsScreen`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 核验结论（定向审计，共 14 次工具调用后停止）

**整体判断：这是一次良性的透明授权流程，未发现诱导或胁迫行为。**

- **无障碍服务能力范围极小**：[MyAccessibilityService](<resource-unit:#1.dex1 code:app.cclauncher.helper.MyAccessibilityService#onStartCommand>) 的 `onAccessibilityEvent` 方法为空实现，只调用 `getClass()`，不读取界面内容；`onStartCommand` 仅识别 `action == "LOCK_SCREEN"`，然后调用 `performGlobalAction(8)`，即执行 `GLOBAL_ACTION_LOCK_SCREEN` 来锁屏。配置 `accessibility_service_config.xml` 中 `canRetrieveWindowContent="false"`、`canRequestFilterKeyEvents="false"`，因此不具备读取屏幕或键盘输入的能力。
- **跳转点只有一个，并且由用户主动触发**：`android.settings.ACCESSIBILITY_SETTINGS` 只出现在 `ResizeDialogKt$$ExternalSyntheticLambda7.invoke` 中（带 `FLAG_ACTIVITY_NEW_TASK`），该回调由 `HomeScreenKt.SettingsScreen` 内的说明弹窗确认按钮触发，属于“用户到设置页手动开启双击锁屏”的按需路径；冷启动 `MainActivity.onCreate` 不会拉起无障碍设置（仅当某个开关被打开时跳 `MANAGE_DEFAULT_APPS_SETTINGS`）。
- **说明载体是原生 Compose Dialog**：`ResizeDialogKt.AccessibilityDisclosureDialog`（`DialogProperties(4)`，即 `dismissOnBackPress/dismissOnClickOutside` 相关默认属性）承载 `accessibility_disclosure*` 系列文案，明确声明“不采集屏幕内容、按键、应用数据与个人信息”，并告知用户可在“设置 > 无障碍”随时关闭；具备取消回调。
- **系统无障碍列表描述透明**：`android:description` = `accessibility_service_description`，服务 label = `@string/app_name`（CClauncher），无空白/换行挤出、无同形字、无多 activity-alias、未伪造 `isAccessibilityTool`。
- **无诱导或胁迫机制**：无悬浮遮罩叠放设置页、无 `onResume` 死循环重跳、无定时器反复拉起、无“允许受限设置”分步教学、获权后无 `GLOBAL_ACTION_BACK/HOME` 阻止撤权；`APPLICATION_DETAILS_SETTINGS` 出现在 `SettingsScreenKt$$ExternalSyntheticLambda54`，属常规应用详情跳转，与无障碍引导无关。
- **静态可见性**：`clear`。DEX 未加壳，仅有 R8 常规 lambda 名称混淆，无加密资产或远端 HTML 引导页。

**未决/边界**：说明弹窗内按钮的逐字文案（预筛给出的“Agree and continue”等）未在本次调用预算内定位到其 `strings.xml` key 的代码引用点，属资源层文字而非行为差异，不影响结论。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳（apkid 初判 False），无障碍服务、说明弹窗与设置跳转全部为可反编译的 Kotlin/Compose 实现；仅有 R8 生成的 ExternalSyntheticLambda 名称混淆，无加密载荷、无远端 HTML 引导页。弹窗按钮文案的资源 key 未在本次调用预算内逐一定位，属资源文字细节。",
  "summary_one_liner": "CClauncher 仅在用户于设置页开启“双击锁屏”时弹出原生 Compose 说明对话框，透明告知无障碍仅用于锁屏且不采集数据，用户确认后才跳转系统无障碍设置页手动开启，无遮罩、无循环、无诱导。",
  "disguise_identity": {
    "app_display_name": "CClauncher",
    "claimed_brand_or_persona": "CClauncher（F-Droid 开源极简桌面，真实身份）",
    "a11y_service_label": "CClauncher",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。R8 仅生成 ExternalSyntheticLambda 类名混淆，属常规编译产物；服务标签直接引用 @string/app_name，未使用空白/换行挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "app.cclauncher.MainActivity（HOME 桌面）→ 设置界面 Compose SettingsScreen",
      "trigger_event": "用户在设置页操作“Double Tap to Lock Screen”开关（设置项 key: cclauncher.settings.setting_double_tap_to_lock_screen），SettingsScreen 据此渲染说明弹窗；冷启动不触发",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Double Tap to Lock Screen",
      "shown_text_zh": "双击锁屏（设置项名称）",
      "user_action_requested": "用户自行进入设置并打开该功能开关；不打开则不会出现任何无障碍提示，可自由返回",
      "code_anchor": "app.cclauncher.ui.screens.HomeScreenKt.SettingsScreen；app.cclauncher.settings.AppSettingsSchema.<clinit>"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "Compose Dialog：app.cclauncher.ui.dialogs.ResizeDialogKt.AccessibilityDisclosureDialog（DialogProperties(4)）",
      "trigger_event": "SettingsScreen 组合阶段调用 AccessibilityDisclosureDialog(onDismiss, onConfirm, titleText)，弹窗出现",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "CClauncher accessibility service / Please turn on or off CClauncher's accessibility service in your device's settings to enable or disable this feature. Please note that this service is only used to let you turn off your device's screen using the double tap gesture. Our accessibility service does not collect or share any data. / What this service accesses: no screen content, no keystrokes, no app data, and no personal information. Nothing is collected and nothing leaves your device. / You can turn this service off at any time in Android Settings > Accessibility. / Turn on CClauncher under Accessibility > Downloaded apps (called Installed services on some devices).",
      "shown_text_zh": "CClauncher 无障碍服务：请在设备设置中开启或关闭本服务以启用/停用该功能；本服务仅用于通过双击手势关闭屏幕，不收集或共享任何数据。本服务访问范围：无屏幕内容、无按键、无应用数据、无个人信息，不采集任何内容、数据不离开设备。你可随时在 设置 > 无障碍 中关闭本服务。开启路径：在“无障碍 > 已下载的应用”（部分设备称“已安装的服务”）中开启 CClauncher。",
      "user_action_requested": "阅读说明后选择确认（Agree and continue）或取消/关闭弹窗；存在取消路径（onDismiss 回调），不阻断使用",
      "code_anchor": "app.cclauncher.ui.dialogs.ResizeDialogKt#AccessibilityDisclosureDialog；res/values/strings.xml（accessibility_disclosure / accessibility_disclosure_data / accessibility_disclosure_disable / accessibility_disclosure_title / accessibility_settings_hint）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户在说明弹窗点击确认，触发 ResizeDialogKt$$ExternalSyntheticLambda7.invoke → context.startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(FLAG_ACTIVITY_NEW_TASK))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "CClauncher（系统无障碍服务列表项，label=@string/app_name）；The accessibility permission is required to enable double tap to lock. Any data acquired by CClauncher via this service will not leave your device.",
      "shown_text_zh": "系统无障碍列表显示服务名 CClauncher；描述为“启用双击锁屏需要无障碍权限，CClauncher 通过该服务获取的任何数据都不会离开你的设备”。",
      "user_action_requested": "用户在系统无障碍页手动找到 CClauncher 并自行开启；是否开启完全由用户决定，可返回不开启",
      "code_anchor": "app.cclauncher.ui.dialogs.ResizeDialogKt$$ExternalSyntheticLambda7#invoke；res/xml/accessibility_service_config.xml"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity / SettingsScreen（返回后）",
      "trigger_event": "用户从系统设置返回应用；未发现 onResume 重跳、定时器拉起或监听设置页的逻辑",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（拒绝授权后仅功能不可用，无弹窗再拉起、无循环提示）",
      "user_action_requested": "无强制动作；用户可继续使用桌面其余功能，仅双击锁屏不可用",
      "code_anchor": "app.cclauncher.MainActivity$onCreate$4$1#emit（仅处理方向与 MANAGE_DEFAULT_APPS_SETTINGS，无无障碍重跳）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "app.cclauncher.helper.MyAccessibilityService",
      "trigger_event": "服务被系统连接后 onServiceConnected 置 connected=this；双击手势触发 startService(action=\"LOCK_SCREEN\") → onStartCommand 执行 performGlobalAction(8) 锁屏",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（仅执行锁屏全局动作，不弹界面、不自动授权、不阻止撤权）",
      "user_action_requested": "无需额外操作；用户可随时在系统无障碍设置中关闭该服务，应用无阻止行为",
      "code_anchor": "app.cclauncher.helper.MyAccessibilityService#onServiceConnected；app.cclauncher.helper.MyAccessibilityService#onStartCommand；app.cclauncher.helper.MyAccessibilityService#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "SettingsScreen 内的原生 Compose Dialog（AccessibilityDisclosureDialog，DialogProperties(4)）：主说明标题 accessibility_disclosure_title、正文 accessibility_disclosure、访问范围 accessibility_disclosure_data、关闭方式 accessibility_disclosure_disable、开启路径提示 accessibility_settings_hint",
    "res/values/strings.xml：accessibility_service_description（呈现于系统无障碍服务列表项的描述栏）",
    "系统无障碍列表服务名：AndroidManifest 中 service android:label=\"@string/app_name\" → 显示 CClauncher",
    "设置界面开关项文本：setting_double_tap_to_lock_screen（Double Tap to Lock Screen）",
    "未使用 WebView / HTML / 悬浮窗 Overlay / 通知栏 承载任何无障碍引导文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "CClauncher accessibility service",
      "text_zh": "CClauncher 无障碍服务",
      "source_location": "strings.xml key accessibility_disclosure_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Please turn on or off CClauncher's accessibility service in your device's settings to enable or disable this feature. Please note that this service is only used to let you turn off your device's screen using the double tap gesture. Our accessibility service does not collect or share any data.",
      "text_zh": "请在设备设置中开启或关闭 CClauncher 的无障碍服务以启用或停用该功能。请注意，本服务仅用于让你通过双击手势关闭设备屏幕。我们的无障碍服务不收集也不共享任何数据。",
      "source_location": "strings.xml key accessibility_disclosure",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "What this service accesses: no screen content, no keystrokes, no app data, and no personal information. Nothing is collected and nothing leaves your device.",
      "text_zh": "本服务访问的内容：无屏幕内容、无按键记录、无应用数据、无个人信息。不收集任何内容，任何数据都不会离开你的设备。",
      "source_location": "strings.xml key accessibility_disclosure_data",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "You can turn this service off at any time in Android Settings > Accessibility.",
      "text_zh": "你可以随时在 Android 设置 > 无障碍 中关闭本服务。",
      "source_location": "strings.xml key accessibility_disclosure_disable",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn on CClauncher under Accessibility > Downloaded apps (called Installed services on some devices).",
      "text_zh": "在“无障碍 > 已下载的应用”（部分设备称为“已安装的服务”）中开启 CClauncher。",
      "source_location": "strings.xml key accessibility_settings_hint",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The accessibility permission is required to enable double tap to lock. Any data acquired by CClauncher via this service will not leave your device.",
      "text_zh": "启用双击锁屏需要无障碍权限。CClauncher 通过该服务获取的任何数据都不会离开你的设备。",
      "source_location": "strings.xml key accessibility_service_description（res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性降级：用户取消弹窗或从系统设置返回后不重跳、不轮询、不弹二次提示，仅双击锁屏功能保持不可用，桌面其余功能正常",
    "overlay_or_fake_settings": "无。未使用半透明遮罩、全屏悬浮窗或高仿系统无障碍开关页；仅跳转真实系统设置页",
    "restricted_settings_13plus_coaching": "无。未出现引导进入应用详情点击右上角菜单允许受限设置，也无 Session 安装器绕过；APPLICATION_DETAILS_SETTINGS 跳转位于 SettingsScreenKt$$ExternalSyntheticLambda54，用于常规应用详情，与无障碍授权无关",
    "post_grant_anti_removal": "无。onAccessibilityEvent 空实现，onServiceConnected 仅记录静态引用并启动协程，未监听设置页、未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权、未自动点击确认",
    "benign_graceful_degradation": "不开启无障碍时双击锁屏功能不可用，其余桌面功能（隐藏应用、搜索、壁纸等）照常使用；弹窗提供取消回调，说明中明确告知可随时在系统设置关闭服务"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（来源 ResizeDialogKt$$ExternalSyntheticLambda7.invoke），以及此前 SettingsScreen 内 AccessibilityDisclosureDialog 首次渲染（Dialog window 出现）时；本应用冷启动不弹无障碍引导，无需在 0 步拉起",
    "key_pages_to_capture": [
      {
        "page_role": "设置页内无障碍说明弹窗页",
        "page_identifier": "CClauncher 设置界面之上的 Compose Dialog，标题文本 'CClauncher accessibility service'，含“Agree and continue”确认按钮与取消/关闭入口",
        "why_most_useful": "这是全流程唯一的授权说服点，可直接判定文案是否透明、是否具备取消路径、是否存在恐吓或假更新话术",
        "observable_utg_signals": ["弹窗标题与正文文本节点（accessibility_disclosure_title / accessibility_disclosure）", "是否存在取消/返回可点节点与 Dialog 是否可外部取消", "是否出现“假更新/系统故障/安全风险”类诱导词"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 中服务名 'CClauncher' 及其描述栏",
        "why_most_useful": "核对应用向系统申报的真实服务名与描述是否与弹窗一致，识别是否存在标签伪装或描述与实际能力不符",
        "observable_utg_signals": ["列表项显示名是否等于 app_name（CClauncher）", "描述文本是否与 accessibility_service_description 一致", "是否存在同名多服务或可疑空白挤出名称"]
      },
      {
        "page_role": "设置页功能开关入口页",
        "page_identifier": "CClauncher 设置界面 'Double Tap to Lock Screen' 开关项",
        "why_most_useful": "确认授权引导是否由用户主动开启功能触发（按需触发）而非冷启动强制，判定诱导强度",
        "observable_utg_signals": ["开关初始状态与点击后是否才出现弹窗", "冷启动桌面是否无任何无障碍提示"]
      },
      {
        "page_role": "获权后双击锁屏行为页",
        "page_identifier": "桌面双击手势后屏幕熄灭（performGlobalAction(8)）",
        "why_most_useful": "验证无障碍能力实际用途仅为锁屏，排除获权后执行读屏、自动点击或后台拉起其他界面的行为",
        "observable_utg_signals": ["双击后是否仅熄屏而无额外界面跳转", "锁屏后是否出现自动点击/自动授权等异常动作"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本应用无图文化诱导、无空文本外壳、无一阶段 Dropper、无静态加壳（静态加壳亦不影响运行期 UTG）。唯一盲区是：若设备已预先授权无障碍，则运行期不再出现说明弹窗与设置跳转，UTG 需先清除授权再复现；另外弹窗按钮的具体资源 key 未在本次预算内定位，纯文本提取应以 UI 实际渲染为准。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "app.cclauncher.helper.MyAccessibilityService#onStartCommand",
    "app.cclauncher.helper.MyAccessibilityService#onServiceConnected",
    "app.cclauncher.ui.dialogs.ResizeDialogKt#AccessibilityDisclosureDialog",
    "app.cclauncher.ui.dialogs.ResizeDialogKt$$ExternalSyntheticLambda7#invoke",
    "app.cclauncher.ui.screens.HomeScreenKt#SettingsScreen",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
