# BN_027__d773fe1ae9｜极简桌面与双击锁屏 — DistroHopper

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：220.8s

## 1. 一句话核心结论

- **核心申请方式**：DistroHopper 仅在用户把桌面下滑手势设为打开通知栏时，通过原生说明页（可取消）或一条 Toast 后跳系统无障碍设置，请求一个只执行 performGlobalAction 打开通知栏、onAccessibilityEvent 为空的极窄权限，并明确披露范围且提供未授权降级。
- **静态可见性说明**：全部引导逻辑与文案均静态可见：跳转点、两页教学 Activity、strings.xml 原文、无障碍服务 XML 描述与空实现的 onAccessibilityEvent 均可直接反编译读取；无加壳、无加密载荷、无远端 HTML/WebView 承载引导。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d773fe1ae96227737cb56ca2721102d6f5572d2a7b63491e151aa68c714eb962` |
| 包名 / 年份 | `be.robinj.distrohopper` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://apt.izzysoft.de/fdroid/repo/be.robinj.distrohopper_116.apk |
| 桌面显示名 | DistroHopper |
| 引导页宣称品牌/身份 | DistroHopper（IzzyOnDroid 开源桌面替换应用，真实身份） |
| 系统无障碍列表服务名 | DistroHopper（服务未声明 android:label，系统无障碍列表回退显示应用名） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `be.robinj.distrohopper.accessibility.NotificationAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Lets DistroHopper open the notification tray when you swipe down on the home screen. Only used to perform that one action; no screen content is read. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | be.robinj.distrohopper.HomeActivity（LAUNCHER/HOME）→ 首次运行转 be.robinj.distrohopper.onboarding.OnboardingActivity | HomeActivity.onCreate 中 OnboardingGate.shouldShow(prefs) 为真时启动 OnboardingActivity 并 finish | 原生Activity | **原文**：无（OnboardingActivity 内仅处理默认桌面角色与主屏设置，不含无障碍引导）<br>**译注**：引导流程不包含无障碍授权，冷启动不请求无障碍权限 | 无（本步不涉及无障碍） | `be.robinj.distrohopper.HomeActivity.onCreate / be.robinj.distrohopper.onboarding.OnboardingActivity.onCreate` |
| 2 | 业务功能触发 | HomeActivity 手势控制器 HomeGestureController（下滑手势）→ Toast | 用户把下滑手势绑定为打开通知栏后执行该手势，回调 HomeActivity.lambda$onCreate$3 → promptEnableNotificationAccessibility() | 通知栏 | **原文**：Enable DistroHopper in Accessibility to use the notification gesture<br>**译注**：请在无障碍设置中启用 DistroHopper 以使用通知手势 | 阅读提示；随后应用自动跳转系统无障碍设置页，无取消按钮（Toast 自动消失） | `be.robinj.distrohopper.HomeActivity.promptEnableNotificationAccessibility` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（Intent 加 FLAG_ACTIVITY_NEW_TASK） | promptEnableNotificationAccessibility() 内 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(268435456)) | 系统无障碍页 | **原文**：无（系统页面，应用不注入任何内容）<br>**译注**：直接打开系统无障碍服务列表，用户在列表中手动找到 DistroHopper 并开启 | 在系统无障碍列表中开启 DistroHopper 服务；可返回或不做任何操作 | `be.robinj.distrohopper.HomeActivity.promptEnableNotificationAccessibility` |
| 4 | 引导说明页 | be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity 第 1 页（ViewFlipper child 0，布局 activity_accessibility_gesture_setup） | 设置页点击偏好项 dummy_enable_notification_gestures（标题 "Enable open notifications tray gestures"）→ lambda$applyGesturePreferences$5 启动该 Activity | 原生Activity | **原文**：Notification tray gesture setup / Android doesn't give ordinary apps any way to open the notification tray. For a home screen like DistroHopper, the only mechanism available is an accessibility service. DistroHopper's accessibility service needs to be enabled for that reason alone. It only opens the notification tray. It does not read what's on your screen, collect any data, or perform any other action.<br>**译注**：通知栏手势设置 / Android 不向普通应用开放打开通知栏的接口，对 DistroHopper 这类桌面应用唯一可用机制是无障碍服务；仅因此需要启用，且只用于打开通知栏，不读取屏幕内容、不收集数据、不执行其他动作 | 选择「Cancel」退出，或点击「I understand, proceed」进入下一页 | `be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.onCreate + res/layout/activity_accessibility_gesture_setup.xml + res/values/strings.xml(gesture_setup_explain_title/gesture_setup_explain_body/gesture_setup_cancel/gesture_setup_proceed)` |
| 5 | 跳无障碍设置 | AccessibilityGestureSetupActivity 第 2 页 → 系统 android.settings.ACCESSIBILITY_SETTINGS | 点击 btnGestureSetupOpenSettings → openAccessibilitySettings() → startActivity(NotificationAccessibilityService.Companion.accessibilitySettingsIntent()) | 系统无障碍页 | **原文**：Turn on the service / Find DistroHopper in the accessibility settings list and switch it on, then come back here. / Open accessibility settings<br>**译注**：开启服务 / 在无障碍设置列表中找到 DistroHopper 并打开开关，然后回到这里。 / 打开无障碍设置 | 按指引到系统无障碍列表手动开启 DistroHopper 服务，再返回应用；本页只有「Open accessibility settings」一个按钮，无应用内开关伪造 | `be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.openAccessibilitySettings + NotificationAccessibilityService$Companion.accessibilitySettingsIntent` |
| 6 | 拒权反馈循环 | AccessibilityGestureSetupActivity.onResume | 从系统设置返回时 onResume 调用 NotificationAccessibilityService.Companion.isEnabled(context)（读 AccessibilityManager 与 Settings.Secure.enabled_accessibility_services） | 原生Activity | **原文**：无（未启用时不显示任何文本，仅停留在当前页）<br>**译注**：未开启则静默留在说明页，不弹窗、不重跳、无定时器反复拉起 | 用户可自由返回或再次点按钮；无强制循环 | `be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.onResume` |
| 7 | 获权后动作 | AccessibilityGestureSetupActivity.onResume → Toast；NotificationAccessibilityService.onServiceConnected / openNotifications | isEnabled 返回 true 时 Toast.makeText(toast_gesture_setup_enabled) 并 finish()；服务连接后保存 instance，手势触发时调用 performGlobalAction 打开通知栏 | 原生Activity | **原文**：Notification tray gestures enabled<br>**译注**：通知栏手势已启用 | 无需操作；获权后无自点确认、无阻止撤权行为 | `be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.onResume + be.robinj.distrohopper.accessibility.NotificationAccessibilityService.onServiceConnected/openNotifications` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表服务说明：res/xml/notification_accessibility_service.xml 的 android:description → strings.xml accessibility_service_notification_tray_description
- 手势触发时的 Toast（硬编码英文，非资源）：HomeActivity.promptEnableNotificationAccessibility
- 设置页偏好项标题：strings.xml option_enable_notification_gestures（"Enable open notifications tray gestures"）
- 设置页提示项：strings.xml hint_enable_notification_gestures（"A system accessibility service needs to be enabled in order for this to work."），仅在服务未开启时可见（setVisible(!isEnabled)）
- 无障碍分步教学页第 1 页：AccessibilityGestureSetupActivity + res/layout/activity_accessibility_gesture_setup.xml（gesture_setup_explain_title / gesture_setup_explain_body，含 Cancel 与 Proceed 按钮）
- 无障碍分步教学页第 2 页：同一布局 ViewFlipper 第二子页（gesture_setup_guide_title / gesture_setup_guide_body / gesture_setup_open_settings）
- 获权成功提示 Toast：strings.xml toast_gesture_setup_enabled
- Activity 标题：strings.xml title_activity_gesture_setup（"Notification gestures"，显示在页面顶部栏）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Android doesn't give ordinary apps any way to open the notification tray. For a home screen like DistroHopper, the only mechanism available is an accessibility service.<br>DistroHopper's accessibility service needs to be enabled for that reason alone. It only opens the notification tray. It does not read what's on your screen, collect any data, or perform any other action. | Android 不向普通应用提供打开通知栏的任何途径，对 DistroHopper 这类桌面应用唯一可用的机制就是无障碍服务。仅因为这个原因才需要启用 DistroHopper 的无障碍服务。它只用于打开通知栏，不读取你屏幕上的内容、不收集任何数据、也不执行任何其他操作。 | `res/values/strings.xml → gesture_setup_explain_body` | 良性透明说明 |
| en | Lets DistroHopper open the notification tray when you swipe down on the home screen. Only used to perform that one action; no screen content is read. | 允许 DistroHopper 在你于主屏下滑时打开通知栏。仅用于执行这一动作；不读取任何屏幕内容。 | `res/values/strings.xml → accessibility_service_notification_tray_description（经 res/xml/notification_accessibility_service.xml 引用）` | 隐私承诺 |
| en | Find DistroHopper in the accessibility settings list and switch it on, then come back here. | 在无障碍设置列表中找到 DistroHopper 并打开它的开关，然后回到这里。 | `res/values/strings.xml → gesture_setup_guide_body` | 受限设置分步教学 |
| en | Enable DistroHopper in Accessibility to use the notification gesture | 请在无障碍中启用 DistroHopper 以使用通知手势 | `be.robinj.distrohopper.HomeActivity.promptEnableNotificationAccessibility（硬编码字符串）` | 良性透明说明 |
| en | A system accessibility service needs to be enabled in order for this to work. | 此功能需要启用一个系统无障碍服务才能生效。 | `res/values/strings.xml → hint_enable_notification_gestures` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环：从系统设置返回后 onResume 仅判断 isEnabled，未开启则静默停留在说明页或桌面，不弹窗、不重跳、无定时器拉起；已开启则 Toast 提示并 finish。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 在系统设置页上叠放遮罩；教学页自身使用 onboarding_scrim 背景但为独立 Activity，不覆盖系统页面，也无伪造开关。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无
- **良性降级 / 替代方案**：服务未开启时，设置页手势列表剔除“打开通知栏”选项并重置已选项（populateGestureList(isEnabled) / resetIfNotifications），仅显示提示项 hint_enable_notification_gestures；应用其余桌面/搜索功能不受影响。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测 Activity 跳转：出现 intent android.settings.ACCESSIBILITY_SETTINGS（来自 HomeActivity.promptEnableNotificationAccessibility 的 Toast 后直跳，或 AccessibilityGestureSetupActivity.openAccessibilitySettings），以及启动 be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity 时立即 UTG。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区；但纯 UTG 需注意两点：①浅层路径的说明仅是一条短 Toast，若采样间隔较大可能错过，仅看到“跳设置”会误判为强跳，应结合 AccessibilityGestureSetupActivity 说明页与无障碍服务描述共同判定；②设置页提示项 hint_enable_notification_gestures 仅在服务未开启时可见，需在未授权状态下采集。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **无障碍分步教学第 1 页（说明 + Cancel/Proceed）** | Activity be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity，标题 "Notification gestures"，含按钮文本 Cancel / I understand, proceed | 该页是唯一完整披露“为什么需要无障碍、只做什么”的位置，其是否存在可取消按钮与真实范围说明是区分良性告知与诱导的关键 | 标题文本 Notification tray gesture setup；正文是否含 'It does not read what's on your screen, collect any data' 披露语句；是否同时存在 Cancel 与 Proceed 两个按钮（可退出性） |
| **分步教学第 2 页（Turn on the service）** | 同一 Activity 的 ViewFlipper 第二页，按钮 "Open accessibility settings"，正文 "Find DistroHopper in the accessibility settings list and switch it on, then come back here." | 验证应用只做“指向系统设置”的引导，而非伪造开关或在应用内自授权 | 页面仅有引导文案与一个跳设置按钮；无应用内 switch/开关控件；无“允许受限设置”或应用详情页引导 |
| **手势触发瞬间的 Toast 与随后系统无障碍页** | Toast 文本 "Enable DistroHopper in Accessibility to use the notification gesture"；随后系统 Settings 无障碍列表中出现 DistroHopper 条目及描述 | 确认存在“一条 Toast 后直接跳设置”的浅层路径，评估其是否缺少说明（本案仍属功能按需触发） | Toast 文本是否与资源一致；系统无障碍列表项名称为 DistroHopper 且描述为“只打开通知栏、不读屏”；跳转前无全屏遮罩/无假设置页压栈 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `be.robinj.distrohopper.HomeActivity.promptEnableNotificationAccessibility`
- `be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.onCreate`
- `be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.openAccessibilitySettings`
- `be.robinj.distrohopper.accessibility.NotificationAccessibilityService$Companion.accessibilitySettingsIntent`
- `be.robinj.distrohopper.accessibility.NotificationAccessibilityService.onAccessibilityEvent`
- `res/values/strings.xml（gesture_setup_explain_body / gesture_setup_guide_body / accessibility_service_notification_tray_description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论（定向核验，静态完整可见）

- **性质：良性透明说明**。无障碍引导为**用户主动触发功能时才出现**（非冷启动强推），文案完整披露"为什么需要无障碍、只做什么、不做什么"，且提供显式 **Cancel**。
- **两条引导路径**：
  1. **浅层一步直达**：桌面下滑手势被配置为"打开通知栏"后，[HomeActivity.promptEnableNotificationAccessibility()](<resource-unit:#1.dex1 code:be.robinj.distrohopper.HomeActivity#promptEnableNotificationAccessibility>) 先弹一条 Toast（硬编码英文）再直接 `startActivity(ACTION_ACCESSIBILITY_SETTINGS)`（`FLAG_ACTIVITY_NEW_TASK`），无说明页。
  2. **分步教学页**：[AccessibilityGestureSetupActivity](<resource-unit:#1.dex1 code:be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity>) 用 `ViewFlipper` 两页：第一页解释 + Cancel/「I understand, proceed」；第二页「Turn on the service」指引 + 「Open accessibility settings」按钮，经 [accessibilitySettingsIntent()](<resource-unit:#1.dex1 code:be.robinj.distrohopper.accessibility.NotificationAccessibilityService$Companion#accessibilitySettingsIntent>) 跳系统无障碍页。入口为设置项 `dummy_enable_notification_gestures`。
- **无强制/循环**：返回后 [onResume()](<resource-unit:#1.dex1 code:be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity#onResume>) 仅判断 `isEnabled`，已开启则 Toast 并 `finish`，未开启则**停留原地**，不重跳、无定时器拉起。
- **无遮罩/无伪造页**：未使用 `SYSTEM_ALERT_WINDOW` 叠放引导层，无高仿无障碍开关页；未出现 `ACTION_APPLICATION_DETAILS_SETTINGS`，无 Android 13+ 受限设置（受限设置）绕过教学，无 Session 安装器。
- **获权后无防撤权**：`onServiceConnected` 仅保存实例；[onAccessibilityEvent()](<resource-unit:#1.dex1 code:be.robinj.distrohopper.accessibility.NotificationAccessibilityService#onAccessibilityEvent>) **空实现**（不读屏），仅 `performGlobalAction` 打开通知栏，与描述一致。
- **降级路径存在**：服务未开启时手势列表剔除通知栏选项并重置已选项（`populateGestureList(isEnabled)` / `resetIfNotifications`），仅显示提示项，属良性降级。
- **身份一致**：服务无 `android:label`，系统列表显示应用名 `DistroHopper`；[notification_accessibility_service.xml](<resource-unit:#1 file:res/xml/notification_accessibility_service.xml>) 的 description 明确"只执行该动作、不读取屏幕内容"。无空白挤出/同形字/多 alias/伪造 `isAccessibilityTool`。
- **未发现风险**：本轮范围内无恶意诱导、无强制、无越权读屏，不写入风险台账。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑与文案均静态可见：跳转点、两页教学 Activity、strings.xml 原文、无障碍服务 XML 描述与空实现的 onAccessibilityEvent 均可直接反编译读取；无加壳、无加密载荷、无远端 HTML/WebView 承载引导。",
  "summary_one_liner": "DistroHopper 仅在用户把桌面下滑手势设为打开通知栏时，通过原生说明页（可取消）或一条 Toast 后跳系统无障碍设置，请求一个只执行 performGlobalAction 打开通知栏、onAccessibilityEvent 为空的极窄权限，并明确披露范围且提供未授权降级。",
  "disguise_identity": {
    "app_display_name": "DistroHopper",
    "claimed_brand_or_persona": "DistroHopper（IzzyOnDroid 开源桌面替换应用，真实身份）",
    "a11y_service_label": "DistroHopper（服务未声明 android:label，系统无障碍列表回退显示应用名）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "be.robinj.distrohopper.HomeActivity（LAUNCHER/HOME）→ 首次运行转 be.robinj.distrohopper.onboarding.OnboardingActivity",
      "trigger_event": "HomeActivity.onCreate 中 OnboardingGate.shouldShow(prefs) 为真时启动 OnboardingActivity 并 finish",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（OnboardingActivity 内仅处理默认桌面角色与主屏设置，不含无障碍引导）",
      "shown_text_zh": "引导流程不包含无障碍授权，冷启动不请求无障碍权限",
      "user_action_requested": "无（本步不涉及无障碍）",
      "code_anchor": "be.robinj.distrohopper.HomeActivity.onCreate / be.robinj.distrohopper.onboarding.OnboardingActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "HomeActivity 手势控制器 HomeGestureController（下滑手势）→ Toast",
      "trigger_event": "用户把下滑手势绑定为打开通知栏后执行该手势，回调 HomeActivity.lambda$onCreate$3 → promptEnableNotificationAccessibility()",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Enable DistroHopper in Accessibility to use the notification gesture",
      "shown_text_zh": "请在无障碍设置中启用 DistroHopper 以使用通知手势",
      "user_action_requested": "阅读提示；随后应用自动跳转系统无障碍设置页，无取消按钮（Toast 自动消失）",
      "code_anchor": "be.robinj.distrohopper.HomeActivity.promptEnableNotificationAccessibility"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（Intent 加 FLAG_ACTIVITY_NEW_TASK）",
      "trigger_event": "promptEnableNotificationAccessibility() 内 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(268435456))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页面，应用不注入任何内容）",
      "shown_text_zh": "直接打开系统无障碍服务列表，用户在列表中手动找到 DistroHopper 并开启",
      "user_action_requested": "在系统无障碍列表中开启 DistroHopper 服务；可返回或不做任何操作",
      "code_anchor": "be.robinj.distrohopper.HomeActivity.promptEnableNotificationAccessibility"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity 第 1 页（ViewFlipper child 0，布局 activity_accessibility_gesture_setup）",
      "trigger_event": "设置页点击偏好项 dummy_enable_notification_gestures（标题 \"Enable open notifications tray gestures\"）→ lambda$applyGesturePreferences$5 启动该 Activity",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Notification tray gesture setup / Android doesn't give ordinary apps any way to open the notification tray. For a home screen like DistroHopper, the only mechanism available is an accessibility service. DistroHopper's accessibility service needs to be enabled for that reason alone. It only opens the notification tray. It does not read what's on your screen, collect any data, or perform any other action.",
      "shown_text_zh": "通知栏手势设置 / Android 不向普通应用开放打开通知栏的接口，对 DistroHopper 这类桌面应用唯一可用机制是无障碍服务；仅因此需要启用，且只用于打开通知栏，不读取屏幕内容、不收集数据、不执行其他动作",
      "user_action_requested": "选择「Cancel」退出，或点击「I understand, proceed」进入下一页",
      "code_anchor": "be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.onCreate + res/layout/activity_accessibility_gesture_setup.xml + res/values/strings.xml(gesture_setup_explain_title/gesture_setup_explain_body/gesture_setup_cancel/gesture_setup_proceed)"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "AccessibilityGestureSetupActivity 第 2 页 → 系统 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "点击 btnGestureSetupOpenSettings → openAccessibilitySettings() → startActivity(NotificationAccessibilityService.Companion.accessibilitySettingsIntent())",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Turn on the service / Find DistroHopper in the accessibility settings list and switch it on, then come back here. / Open accessibility settings",
      "shown_text_zh": "开启服务 / 在无障碍设置列表中找到 DistroHopper 并打开开关，然后回到这里。 / 打开无障碍设置",
      "user_action_requested": "按指引到系统无障碍列表手动开启 DistroHopper 服务，再返回应用；本页只有「Open accessibility settings」一个按钮，无应用内开关伪造",
      "code_anchor": "be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.openAccessibilitySettings + NotificationAccessibilityService$Companion.accessibilitySettingsIntent"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "AccessibilityGestureSetupActivity.onResume",
      "trigger_event": "从系统设置返回时 onResume 调用 NotificationAccessibilityService.Companion.isEnabled(context)（读 AccessibilityManager 与 Settings.Secure.enabled_accessibility_services）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（未启用时不显示任何文本，仅停留在当前页）",
      "shown_text_zh": "未开启则静默留在说明页，不弹窗、不重跳、无定时器反复拉起",
      "user_action_requested": "用户可自由返回或再次点按钮；无强制循环",
      "code_anchor": "be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.onResume"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityGestureSetupActivity.onResume → Toast；NotificationAccessibilityService.onServiceConnected / openNotifications",
      "trigger_event": "isEnabled 返回 true 时 Toast.makeText(toast_gesture_setup_enabled) 并 finish()；服务连接后保存 instance，手势触发时调用 performGlobalAction 打开通知栏",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Notification tray gestures enabled",
      "shown_text_zh": "通知栏手势已启用",
      "user_action_requested": "无需操作；获权后无自点确认、无阻止撤权行为",
      "code_anchor": "be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.onResume + be.robinj.distrohopper.accessibility.NotificationAccessibilityService.onServiceConnected/openNotifications"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表服务说明：res/xml/notification_accessibility_service.xml 的 android:description → strings.xml accessibility_service_notification_tray_description",
    "手势触发时的 Toast（硬编码英文，非资源）：HomeActivity.promptEnableNotificationAccessibility",
    "设置页偏好项标题：strings.xml option_enable_notification_gestures（\"Enable open notifications tray gestures\"）",
    "设置页提示项：strings.xml hint_enable_notification_gestures（\"A system accessibility service needs to be enabled in order for this to work.\"），仅在服务未开启时可见（setVisible(!isEnabled)）",
    "无障碍分步教学页第 1 页：AccessibilityGestureSetupActivity + res/layout/activity_accessibility_gesture_setup.xml（gesture_setup_explain_title / gesture_setup_explain_body，含 Cancel 与 Proceed 按钮）",
    "无障碍分步教学页第 2 页：同一布局 ViewFlipper 第二子页（gesture_setup_guide_title / gesture_setup_guide_body / gesture_setup_open_settings）",
    "获权成功提示 Toast：strings.xml toast_gesture_setup_enabled",
    "Activity 标题：strings.xml title_activity_gesture_setup（\"Notification gestures\"，显示在页面顶部栏）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Android doesn't give ordinary apps any way to open the notification tray. For a home screen like DistroHopper, the only mechanism available is an accessibility service.\nDistroHopper's accessibility service needs to be enabled for that reason alone. It only opens the notification tray. It does not read what's on your screen, collect any data, or perform any other action.",
      "text_zh": "Android 不向普通应用提供打开通知栏的任何途径，对 DistroHopper 这类桌面应用唯一可用的机制就是无障碍服务。仅因为这个原因才需要启用 DistroHopper 的无障碍服务。它只用于打开通知栏，不读取你屏幕上的内容、不收集任何数据、也不执行任何其他操作。",
      "source_location": "res/values/strings.xml → gesture_setup_explain_body",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Lets DistroHopper open the notification tray when you swipe down on the home screen. Only used to perform that one action; no screen content is read.",
      "text_zh": "允许 DistroHopper 在你于主屏下滑时打开通知栏。仅用于执行这一动作；不读取任何屏幕内容。",
      "source_location": "res/values/strings.xml → accessibility_service_notification_tray_description（经 res/xml/notification_accessibility_service.xml 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Find DistroHopper in the accessibility settings list and switch it on, then come back here.",
      "text_zh": "在无障碍设置列表中找到 DistroHopper 并打开它的开关，然后回到这里。",
      "source_location": "res/values/strings.xml → gesture_setup_guide_body",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable DistroHopper in Accessibility to use the notification gesture",
      "text_zh": "请在无障碍中启用 DistroHopper 以使用通知手势",
      "source_location": "be.robinj.distrohopper.HomeActivity.promptEnableNotificationAccessibility（硬编码字符串）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "A system accessibility service needs to be enabled in order for this to work.",
      "text_zh": "此功能需要启用一个系统无障碍服务才能生效。",
      "source_location": "res/values/strings.xml → hint_enable_notification_gestures",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环：从系统设置返回后 onResume 仅判断 isEnabled，未开启则静默停留在说明页或桌面，不弹窗、不重跳、无定时器拉起；已开启则 Toast 提示并 finish。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 在系统设置页上叠放遮罩；教学页自身使用 onboarding_scrim 背景但为独立 Activity，不覆盖系统页面，也无伪造开关。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无",
    "benign_graceful_degradation": "服务未开启时，设置页手势列表剔除“打开通知栏”选项并重置已选项（populateGestureList(isEnabled) / resetIfNotifications），仅显示提示项 hint_enable_notification_gestures；应用其余桌面/搜索功能不受影响。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测 Activity 跳转：出现 intent android.settings.ACCESSIBILITY_SETTINGS（来自 HomeActivity.promptEnableNotificationAccessibility 的 Toast 后直跳，或 AccessibilityGestureSetupActivity.openAccessibilitySettings），以及启动 be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity 时立即 UTG。",
    "key_pages_to_capture": [
      {
        "page_role": "无障碍分步教学第 1 页（说明 + Cancel/Proceed）",
        "page_identifier": "Activity be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity，标题 \"Notification gestures\"，含按钮文本 Cancel / I understand, proceed",
        "why_most_useful": "该页是唯一完整披露“为什么需要无障碍、只做什么”的位置，其是否存在可取消按钮与真实范围说明是区分良性告知与诱导的关键",
        "observable_utg_signals": ["标题文本 Notification tray gesture setup", "正文是否含 'It does not read what's on your screen, collect any data' 披露语句", "是否同时存在 Cancel 与 Proceed 两个按钮（可退出性）"]
      },
      {
        "page_role": "分步教学第 2 页（Turn on the service）",
        "page_identifier": "同一 Activity 的 ViewFlipper 第二页，按钮 \"Open accessibility settings\"，正文 \"Find DistroHopper in the accessibility settings list and switch it on, then come back here.\"",
        "why_most_useful": "验证应用只做“指向系统设置”的引导，而非伪造开关或在应用内自授权",
        "observable_utg_signals": ["页面仅有引导文案与一个跳设置按钮", "无应用内 switch/开关控件", "无“允许受限设置”或应用详情页引导"]
      },
      {
        "page_role": "手势触发瞬间的 Toast 与随后系统无障碍页",
        "page_identifier": "Toast 文本 \"Enable DistroHopper in Accessibility to use the notification gesture\"；随后系统 Settings 无障碍列表中出现 DistroHopper 条目及描述",
        "why_most_useful": "确认存在“一条 Toast 后直接跳设置”的浅层路径，评估其是否缺少说明（本案仍属功能按需触发）",
        "observable_utg_signals": ["Toast 文本是否与资源一致", "系统无障碍列表项名称为 DistroHopper 且描述为“只打开通知栏、不读屏”", "跳转前无全屏遮罩/无假设置页压栈"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区；但纯 UTG 需注意两点：①浅层路径的说明仅是一条短 Toast，若采样间隔较大可能错过，仅看到“跳设置”会误判为强跳，应结合 AccessibilityGestureSetupActivity 说明页与无障碍服务描述共同判定；②设置页提示项 hint_enable_notification_gestures 仅在服务未开启时可见，需在未授权状态下采集。"
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
    "be.robinj.distrohopper.HomeActivity.promptEnableNotificationAccessibility",
    "be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.onCreate",
    "be.robinj.distrohopper.accessibility.AccessibilityGestureSetupActivity.openAccessibilitySettings",
    "be.robinj.distrohopper.accessibility.NotificationAccessibilityService$Companion.accessibilitySettingsIntent",
    "be.robinj.distrohopper.accessibility.NotificationAccessibilityService.onAccessibilityEvent",
    "res/values/strings.xml（gesture_setup_explain_body / gesture_setup_guide_body / accessibility_service_notification_tray_description）"
  ]
}
```

</details>
