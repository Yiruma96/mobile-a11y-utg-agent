# BN_030__a2df41359b｜极简桌面与双击锁屏 — MinkLauncher OpenSource

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：180.1s

## 1. 一句话核心结论

- **核心申请方式**：仅在用户主动开启双击锁屏功能时，先以原生确认框逐条披露用途与数据边界，再由 s80.x() 携带组件名跳转系统无障碍设置页；未授权则静默降级不弹窗，获权后仅调用 performGlobalAction(8) 执行锁屏。
- **静态可见性说明**：无障碍申请链路完整静态可见：Intent 构造位于明文 DEX 类 s80#x，服务声明与配置位于 AndroidManifest.xml 与 res/xml/lock_accessibility_service.xml，全部文案位于 res/values*/strings.xml。无加壳、无 VMP、无 AES 载荷、无远端 HTML（代码中 WebView 零命中）。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a2df41359b3bdb76c04f3ed247709291936c575f526a0735eb3f3ccc09d581d7` |
| 包名 / 年份 | `com.katoaapps.openminilaunch` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.katoaapps.openminilaunch_35.apk |
| 桌面显示名 | MinkLauncher OpenSource |
| 引导页宣称品牌/身份 | MinkLauncher OpenSource（Katoa Apps 开源极简桌面，官网 minklauncher.com，F-Droid 发布） |
| 系统无障碍列表服务名 | MinkLauncher OpenSource - Double-tap screen lock |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.katoaapps.openminilaunch.platform.LockScreenAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, SEND_SMS` |
| 系统设置项说明 (`android:description`) | Allows MinkLauncher OpenSource to perform Android’s Lock screen action only after you double-tap empty Home space. It cannot read or interact with screen content. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | 设置页 Double-tap screen lock 开关项（res/values/strings.xml 中的 double_tap_screen_lock） | 用户在桌面设置中主动点击/切换“Double-tap screen lock”开关 | 原生Activity | **原文**：Double-tap screen lock<br>**译注**：双击锁屏 | 用户自行开启该开关（非系统必需，可随时不开启） | `res/values/strings.xml:double_tap_screen_lock / s80#x 调用方 mt0.a` |
| 2 | 引导说明页 | 原生确认对话框（标题 enable_double_tap_lock + 三段披露文案） | 开关开启动作触发披露对话框，用户点确认后才继续 | 原生Dialog | **原文**：Enable double-tap to lock? / To make double-tap behave like the power button, %1$s uses Android’s accessibility Lock screen action. / The service runs only when you double-tap empty Home space. It does not observe accessibility events, read screen content, perform gestures, or collect data. / Android will ask you to enable Double-tap screen lock. You can disable it at any time in Accessibility settings.<br>**译注**：是否启用双击锁屏？/ 为使双击行为等同电源键，%1$s 会使用 Android 无障碍的锁屏动作。/ 该服务仅在你双击空白 Home 区域时运行。它不观察无障碍事件、不读取屏幕内容、不执行手势、不收集数据。/ Android 将要求你启用“双击锁屏”。你可随时在无障碍设置中关闭它。 | 用户可选择确认继续跳转系统设置，也可取消/返回而不授权（存在明确否定路径） | `res/values/strings.xml:enable_double_tap_lock / double_tap_disclosure_one\|two\|three；确认回调 mt0.a case 0/1` |
| 3 | 跳无障碍设置 | 系统无障碍设置页（精确定位到本服务项） | 对话框确认后由 mt0.a 调用 ni1.T(s80.x())，再经 Context.startActivity 下发 Intent | 系统无障碍页 | **原文**：MinkLauncher OpenSource - Double-tap screen lock<br>**译注**：MinkLauncher OpenSource - 双击锁屏（系统无障碍列表项与说明：Allows MinkLauncher OpenSource to perform Android’s Lock screen action only after you double-tap empty Home space. It cannot read or interact with screen content.） | 用户在系统页面自行决定是否开启该无障碍服务（应用不代点、不遮罩、不强制） | `s80#x → new Intent("android.settings.ACCESSIBILITY_SETTINGS").putExtra(":settings:fragment_args_key", ComponentName(..., LockScreenAccessibilityService.class).flattenToString())` |
| 4 | 拒权反馈循环 | 桌面主界面（r80.h case 2 双击空白处处理器） | 用户双击 Home 空白区域，s80.t() 检测服务未启用则直接 return，不发起任何弹窗或重跳 | 原生Activity | 无 | 无强制操作；用户可改用手动锁屏键 | `r80#h case 2 → s80#t() 返回 false 后直接 break` |
| 5 | 获权后动作 | LockScreenAccessibilityService（空 onAccessibilityEvent / 空 onInterrupt） | s80.t() 判定已启用后，s80.y() 调用 performGlobalAction(GLOBAL_ACTION_LOCK_SCREEN=8) | 不可静态还原 | 无 | 无；服务不自点确认、不监听设置页阻止撤权 | `s80#y → LockScreenAccessibilityService.f.performGlobalAction(8)；LockScreenAccessibilityService#onServiceConnected 仅赋值静态引用 f` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml 的 enable_double_tap_lock、double_tap_disclosure_one/two/three、double_tap_screen_lock、double_tap_permission_description（原生确认对话框正文，由 mt0.a / g.a 回调驱动）
- res/values/strings.xml 的 lock_accessibility_label（AndroidManifest.xml 中 service android:label，即系统无障碍列表项名称）
- res/values/strings.xml 的 lock_accessibility_description（AndroidManifest.xml 中 service android:description 与 res/xml/lock_accessibility_service.xml 的 android:description，即系统无障碍详情页说明）
- res/values/strings.xml 的 double_tap_lock_requires_android_9（Android 9 以下不可用时的原生提示）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable double-tap to lock? | 是否启用双击锁屏？ | `res/values/strings.xml key: enable_double_tap_lock` | 良性透明说明 |
| en | To make double-tap behave like the power button, %1$s uses Android’s accessibility Lock screen action. | 为使双击行为等同电源键，%1$s 会使用 Android 无障碍的锁屏动作。 | `res/values/strings.xml key: double_tap_disclosure_one` | 良性透明说明 |
| en | The service runs only when you double-tap empty Home space. It does not observe accessibility events, read screen content, perform gestures, or collect data. | 该服务仅在你双击空白 Home 区域时运行。它不观察无障碍事件、不读取屏幕内容、不执行手势、不收集数据。 | `res/values/strings.xml key: double_tap_disclosure_two` | 隐私承诺 |
| en | Android will ask you to enable Double-tap screen lock. You can disable it at any time in Accessibility settings. | Android 将要求你启用“双击锁屏”。你可随时在无障碍设置中关闭它。 | `res/values/strings.xml key: double_tap_disclosure_three` | 良性透明说明 |
| en | Allows MinkLauncher OpenSource to perform Android’s Lock screen action only after you double-tap empty Home space. It cannot read or interact with screen content. | 允许 MinkLauncher OpenSource 仅在你双击空白 Home 区域后执行 Android 的锁屏动作。它无法读取或交互屏幕内容。 | `res/values/strings.xml key: lock_accessibility_description（AndroidManifest.xml service android:description / res/xml/lock_accessibility_service.xml）` | 良性透明说明 |
| en | Uses Android’s Lock screen action only after you double-tap. It cannot read screen content. | 仅在你双击后使用 Android 的锁屏动作。它无法读取屏幕内容。 | `res/values/strings.xml key: double_tap_permission_description` | 良性透明说明 |
| en | MinkLauncher OpenSource - Double-tap screen lock | MinkLauncher OpenSource - 双击锁屏 | `res/values/strings.xml key: lock_accessibility_label（AndroidManifest.xml service android:label）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。s80.t() 通过 getEnabledAccessibilityServiceList(-1) 判定未启用时，双击空白 Home 的处理器 r80.h case 2 直接 return，不弹窗、不重跳系统设置、无定时器拉起；用户停留在原界面，可继续使用手动电源键锁屏。
- **遮罩叠层 / 高仿系统设置页**：无。Manifest 未申请 SYSTEM_ALERT_WINDOW，代码中 TYPE_APPLICATION_OVERLAY 零命中，无 WebView、无高仿系统无障碍开关页。跳转为标准 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。onAccessibilityEvent 与 onInterrupt 为空实现；不含 GLOBAL_ACTION_BACK/HOME 干预撤权，不含自点确认或自授权逻辑；performGlobalAction 唯一用途为 GLOBAL_ACTION_LOCK_SCREEN(8)。
- **良性降级 / 替代方案**：有。未授权时双击锁屏功能静默失效，应用仍可正常作为桌面使用，并可改用手动电源键；Android 9 以下以 double_tap_lock_requires_android_9 提示不可用而非诱导。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（且附带 :settings:fragment_args_key 指向自身组件）时拉起；或在设置页开关点击后、原生确认框弹出瞬间抓取对话框全文。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。该应用无静态加壳（预筛 False，且 s80#x 等关键方法可直接反编译）、无远端 HTML、无图引导。唯一 UTG 盲区是用户取消后双击桌面空白处的静默失败无任何文本反馈，但该行为本身不构成诱导。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **引导说明弹窗页（双击锁屏开关确认框）** | 标题文本 Enable double-tap to lock?，含三段披露文案，包名 com.katoaapps.openminilaunch | 这是唯一承担说明义务的界面，可直接判定是否存在虚假理由、隐私承诺造假、教唆忽视警告或不可取消强制。 | 对话框是否存在取消/返回路径（本应用存在）；文案是否明确声明不读取屏幕内容、不收集数据；是否含“假更新/故障恐吓/清理优化”等诱导语料 |
| **系统无障碍服务列表项** | android.settings.ACCESSIBILITY_SETTINGS 页面中文本 MinkLauncher OpenSource - Double-tap screen lock 及其描述 | 核对系统层面暴露的服务名与描述是否与桌面名称一致、是否如实声明用途范围，识别伪造 isAccessibilityTool 或身份冒充。 | 服务标签是否与包名/品牌一致；描述是否自述仅锁屏、不读取内容；是否同时存在多个可疑无障碍服务项 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `s80#x（构造 android.settings.ACCESSIBILITY_SETTINGS + :settings:fragment_args_key 精准跳转）`
- `s80#t（getEnabledAccessibilityServiceList(-1) 判定本服务是否已启用）`
- `s80#y（performGlobalAction(8) 执行 GLOBAL_ACTION_LOCK_SCREEN）`
- `com.katoaapps.openminilaunch.platform.LockScreenAccessibilityService#onAccessibilityEvent（空实现）`
- `res/xml/lock_accessibility_service.xml（canRetrieveWindowContent=false, canPerformGestures=false, isAccessibilityTool=false）`
- `res/values/strings.xml（enable_double_tap_lock / double_tap_disclosure_one|two|three / lock_accessibility_description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论（定向核验，12 次工具调用）

**静态可见性：完整清晰，无壳、无加密、无动态加载。** 无障碍权限申请链路全部位于明文 DEX 与资源中。

**引导链路实际形态（三处，均良性透明）**

1. **触发时机：用户按需（user_feature_on_demand）**。无障碍不是冷启动第一步强制要求。只有在设置里开启“Double-tap screen lock”时，才会弹确认框。另有可用性检查 `s80.t()` 遍历 `getEnabledAccessibilityServiceList(-1)`，判断本服务是否已启用。双击桌面空白处的动作处理器在未授权时直接**静默跳过**，不会弹窗，也不会重跳。
2. **前置披露**：`enable_double_tap_lock` 与 `double_tap_disclosure_one/two/three` 三条文案依次说明：为让双击等同电源键，应用会使用 Android 无障碍的锁屏动作；服务仅在你双击空白 Home 区时运行，**不观察无障碍事件、不读取屏幕内容、不执行手势、不收集数据**；系统会要求你开启，并可随时在无障碍设置中关闭。
3. **跳转方式**：`s80.x()` 构造 `android.settings.ACCESSIBILITY_SETTINGS`，并带 `:settings:fragment_args_key` 精准定位到本服务项。该 Intent 由 `mt0.a`（对话框确认按钮回调）与 `g.a`（case 16 设置入口）触发，最终通过 `Context.startActivity` 下发。全程没有叠加遮罩、没有悬浮窗（Manifest 无 `SYSTEM_ALERT_WINDOW`，代码无 `TYPE_APPLICATION_OVERLAY`）、没有 WebView（代码中 `WebView` 零命中）、没有高仿系统页。
4. **获权后动作**：`onAccessibilityEvent` 与 `onInterrupt` 均为空实现，`canRetrieveWindowContent="false"`、`canPerformGestures="false"`，配置 `isAccessibilityTool="false"` 是如实声明（服务确实不是辅助工具，仅用于锁屏，并未伪造 `true` 冒充）。唯一动作是 `performGlobalAction(8)`（GLOBAL_ACTION_LOCK_SCREEN）。没有自点确认，没有 `GLOBAL_ACTION_BACK/HOME` 阻止撤权，也没有抗移除逻辑。
5. **受限设置（Android 13+）教学**：无。`APPLICATION_DETAILS_SETTINGS` 仅用于常规应用详情页，没有引导“允许受限设置”。

**身份一致性**：桌面名、服务标签（`MinkLauncher OpenSource - Double-tap screen lock`）、`android:description`、F-Droid 开源发布三者一致，没有同形字、空白挤出、多 activity-alias 伪装。

**UTG 判别要点**：该应用的引导是原生确认框加一次性跳系统无障碍页，用户取消后不重跳，因此 UTG 只需在 `ACCESSIBILITY_SETTINGS` 跳转瞬间抓取系统无障碍列表项即可判定。纯图诱导与 OCR 均不需要。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请链路完整静态可见：Intent 构造位于明文 DEX 类 s80#x，服务声明与配置位于 AndroidManifest.xml 与 res/xml/lock_accessibility_service.xml，全部文案位于 res/values*/strings.xml。无加壳、无 VMP、无 AES 载荷、无远端 HTML（代码中 WebView 零命中）。",
  "summary_one_liner": "仅在用户主动开启双击锁屏功能时，先以原生确认框逐条披露用途与数据边界，再由 s80.x() 携带组件名跳转系统无障碍设置页；未授权则静默降级不弹窗，获权后仅调用 performGlobalAction(8) 执行锁屏。",
  "disguise_identity": {
    "app_display_name": "MinkLauncher OpenSource",
    "claimed_brand_or_persona": "MinkLauncher OpenSource（Katoa Apps 开源极简桌面，官网 minklauncher.com，F-Droid 发布）",
    "a11y_service_label": "MinkLauncher OpenSource - Double-tap screen lock",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "设置页 Double-tap screen lock 开关项（res/values/strings.xml 中的 double_tap_screen_lock）",
      "trigger_event": "用户在桌面设置中主动点击/切换“Double-tap screen lock”开关",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Double-tap screen lock",
      "shown_text_zh": "双击锁屏",
      "user_action_requested": "用户自行开启该开关（非系统必需，可随时不开启）",
      "code_anchor": "res/values/strings.xml:double_tap_screen_lock / s80#x 调用方 mt0.a"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "原生确认对话框（标题 enable_double_tap_lock + 三段披露文案）",
      "trigger_event": "开关开启动作触发披露对话框，用户点确认后才继续",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable double-tap to lock? / To make double-tap behave like the power button, %1$s uses Android’s accessibility Lock screen action. / The service runs only when you double-tap empty Home space. It does not observe accessibility events, read screen content, perform gestures, or collect data. / Android will ask you to enable Double-tap screen lock. You can disable it at any time in Accessibility settings.",
      "shown_text_zh": "是否启用双击锁屏？/ 为使双击行为等同电源键，%1$s 会使用 Android 无障碍的锁屏动作。/ 该服务仅在你双击空白 Home 区域时运行。它不观察无障碍事件、不读取屏幕内容、不执行手势、不收集数据。/ Android 将要求你启用“双击锁屏”。你可随时在无障碍设置中关闭它。",
      "user_action_requested": "用户可选择确认继续跳转系统设置，也可取消/返回而不授权（存在明确否定路径）",
      "code_anchor": "res/values/strings.xml:enable_double_tap_lock / double_tap_disclosure_one|two|three；确认回调 mt0.a case 0/1"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（精确定位到本服务项）",
      "trigger_event": "对话框确认后由 mt0.a 调用 ni1.T(s80.x())，再经 Context.startActivity 下发 Intent",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "MinkLauncher OpenSource - Double-tap screen lock",
      "shown_text_zh": "MinkLauncher OpenSource - 双击锁屏（系统无障碍列表项与说明：Allows MinkLauncher OpenSource to perform Android’s Lock screen action only after you double-tap empty Home space. It cannot read or interact with screen content.）",
      "user_action_requested": "用户在系统页面自行决定是否开启该无障碍服务（应用不代点、不遮罩、不强制）",
      "code_anchor": "s80#x → new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").putExtra(\":settings:fragment_args_key\", ComponentName(..., LockScreenAccessibilityService.class).flattenToString())"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "桌面主界面（r80.h case 2 双击空白处处理器）",
      "trigger_event": "用户双击 Home 空白区域，s80.t() 检测服务未启用则直接 return，不发起任何弹窗或重跳",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何提示，动作被静默忽略（良性降级，无死循环、无定时重跳）",
      "user_action_requested": "无强制操作；用户可改用手动锁屏键",
      "code_anchor": "r80#h case 2 → s80#t() 返回 false 后直接 break"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "LockScreenAccessibilityService（空 onAccessibilityEvent / 空 onInterrupt）",
      "trigger_event": "s80.t() 判定已启用后，s80.y() 调用 performGlobalAction(GLOBAL_ACTION_LOCK_SCREEN=8)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；仅执行系统锁屏动作（SDK_INT>=28 时才生效）",
      "user_action_requested": "无；服务不自点确认、不监听设置页阻止撤权",
      "code_anchor": "s80#y → LockScreenAccessibilityService.f.performGlobalAction(8)；LockScreenAccessibilityService#onServiceConnected 仅赋值静态引用 f"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml 的 enable_double_tap_lock、double_tap_disclosure_one/two/three、double_tap_screen_lock、double_tap_permission_description（原生确认对话框正文，由 mt0.a / g.a 回调驱动）",
    "res/values/strings.xml 的 lock_accessibility_label（AndroidManifest.xml 中 service android:label，即系统无障碍列表项名称）",
    "res/values/strings.xml 的 lock_accessibility_description（AndroidManifest.xml 中 service android:description 与 res/xml/lock_accessibility_service.xml 的 android:description，即系统无障碍详情页说明）",
    "res/values/strings.xml 的 double_tap_lock_requires_android_9（Android 9 以下不可用时的原生提示）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable double-tap to lock?",
      "text_zh": "是否启用双击锁屏？",
      "source_location": "res/values/strings.xml key: enable_double_tap_lock",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To make double-tap behave like the power button, %1$s uses Android’s accessibility Lock screen action.",
      "text_zh": "为使双击行为等同电源键，%1$s 会使用 Android 无障碍的锁屏动作。",
      "source_location": "res/values/strings.xml key: double_tap_disclosure_one",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The service runs only when you double-tap empty Home space. It does not observe accessibility events, read screen content, perform gestures, or collect data.",
      "text_zh": "该服务仅在你双击空白 Home 区域时运行。它不观察无障碍事件、不读取屏幕内容、不执行手势、不收集数据。",
      "source_location": "res/values/strings.xml key: double_tap_disclosure_two",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Android will ask you to enable Double-tap screen lock. You can disable it at any time in Accessibility settings.",
      "text_zh": "Android 将要求你启用“双击锁屏”。你可随时在无障碍设置中关闭它。",
      "source_location": "res/values/strings.xml key: double_tap_disclosure_three",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Allows MinkLauncher OpenSource to perform Android’s Lock screen action only after you double-tap empty Home space. It cannot read or interact with screen content.",
      "text_zh": "允许 MinkLauncher OpenSource 仅在你双击空白 Home 区域后执行 Android 的锁屏动作。它无法读取或交互屏幕内容。",
      "source_location": "res/values/strings.xml key: lock_accessibility_description（AndroidManifest.xml service android:description / res/xml/lock_accessibility_service.xml）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Uses Android’s Lock screen action only after you double-tap. It cannot read screen content.",
      "text_zh": "仅在你双击后使用 Android 的锁屏动作。它无法读取屏幕内容。",
      "source_location": "res/values/strings.xml key: double_tap_permission_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "MinkLauncher OpenSource - Double-tap screen lock",
      "text_zh": "MinkLauncher OpenSource - 双击锁屏",
      "source_location": "res/values/strings.xml key: lock_accessibility_label（AndroidManifest.xml service android:label）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。s80.t() 通过 getEnabledAccessibilityServiceList(-1) 判定未启用时，双击空白 Home 的处理器 r80.h case 2 直接 return，不弹窗、不重跳系统设置、无定时器拉起；用户停留在原界面，可继续使用手动电源键锁屏。",
    "overlay_or_fake_settings": "无。Manifest 未申请 SYSTEM_ALERT_WINDOW，代码中 TYPE_APPLICATION_OVERLAY 零命中，无 WebView、无高仿系统无障碍开关页。跳转为标准 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。onAccessibilityEvent 与 onInterrupt 为空实现；不含 GLOBAL_ACTION_BACK/HOME 干预撤权，不含自点确认或自授权逻辑；performGlobalAction 唯一用途为 GLOBAL_ACTION_LOCK_SCREEN(8)。",
    "benign_graceful_degradation": "有。未授权时双击锁屏功能静默失效，应用仍可正常作为桌面使用，并可改用手动电源键；Android 9 以下以 double_tap_lock_requires_android_9 提示不可用而非诱导。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（且附带 :settings:fragment_args_key 指向自身组件）时拉起；或在设置页开关点击后、原生确认框弹出瞬间抓取对话框全文。",
    "key_pages_to_capture": [
      {
        "page_role": "引导说明弹窗页（双击锁屏开关确认框）",
        "page_identifier": "标题文本 Enable double-tap to lock?，含三段披露文案，包名 com.katoaapps.openminilaunch",
        "why_most_useful": "这是唯一承担说明义务的界面，可直接判定是否存在虚假理由、隐私承诺造假、教唆忽视警告或不可取消强制。",
        "observable_utg_signals": [
          "对话框是否存在取消/返回路径（本应用存在）",
          "文案是否明确声明不读取屏幕内容、不收集数据",
          "是否含“假更新/故障恐吓/清理优化”等诱导语料"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 页面中文本 MinkLauncher OpenSource - Double-tap screen lock 及其描述",
        "why_most_useful": "核对系统层面暴露的服务名与描述是否与桌面名称一致、是否如实声明用途范围，识别伪造 isAccessibilityTool 或身份冒充。",
        "observable_utg_signals": [
          "服务标签是否与包名/品牌一致",
          "描述是否自述仅锁屏、不读取内容",
          "是否同时存在多个可疑无障碍服务项"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。该应用无静态加壳（预筛 False，且 s80#x 等关键方法可直接反编译）、无远端 HTML、无图引导。唯一 UTG 盲区是用户取消后双击桌面空白处的静默失败无任何文本反馈，但该行为本身不构成诱导。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "s80#x（构造 android.settings.ACCESSIBILITY_SETTINGS + :settings:fragment_args_key 精准跳转）",
    "s80#t（getEnabledAccessibilityServiceList(-1) 判定本服务是否已启用）",
    "s80#y（performGlobalAction(8) 执行 GLOBAL_ACTION_LOCK_SCREEN）",
    "com.katoaapps.openminilaunch.platform.LockScreenAccessibilityService#onAccessibilityEvent（空实现）",
    "res/xml/lock_accessibility_service.xml（canRetrieveWindowContent=false, canPerformGestures=false, isAccessibilityTool=false）",
    "res/values/strings.xml（enable_double_tap_lock / double_tap_disclosure_one|two|three / lock_accessibility_description）"
  ]
}
```

</details>
