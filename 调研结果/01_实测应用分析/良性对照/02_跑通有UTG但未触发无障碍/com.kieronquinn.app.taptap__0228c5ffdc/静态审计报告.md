# BN_012__0228c5ffdc｜按键映射与手势导航 — Tap, Tap

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：212.9s

## 1. 一句话核心结论

- **核心申请方式**：Tap, Tap 通过标准 Setup 向导（可跳过）以本地原生页面透明说明其无障碍用途与隐私承诺，仅在添加具体动作/条件时按需跳转系统无障碍设置，无强制、遮罩或拒权循环。
- **静态可见性说明**：无障碍申请链、设置向导页、字符串资源与跳转 Intent 均完整静态可见（无壳、无 VMP、无密文动态加载）；无远端 HTML 引导页，说明文字全部来自本地 strings.xml 并以内嵌 HTML 渲染。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0228c5ffdc8a3d1b7db01461f80bdceefcad74119519db452f794c0d6a7cc071` |
| 包名 / 年份 | `com.kieronquinn.app.taptap` / 2025-2026 |
| 家族 / 品类 | **按键映射与手势导航**（同池样本数：1） |
| 原始来源标识 | https://github.com/KieronQuinn/TapTap/releases/download/1.6.2/TapTap-v1.6.2.apk |
| 桌面显示名 | Tap, Tap |
| 引导页宣称品牌/身份 | Tap, Tap（Kieron Quinn 开源背部双击手势工具，基于 Google Columbus 模型） |
| 系统无障碍列表服务名 | Tap, Tap（主服务）/ Tap, Tap Secondary Service（手势服务） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.kieronquinn.app.taptap.service.accessibility.TapTapAccessibilityService, com.kieronquinn.app.taptap.service.accessibility.TapTapGestureAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Tap, Tap Accessibility Service<br><br>Important Note: No data is collected from any of your apps, this service is simply used to keep the recognition active and provide interaction with the device / Tap, Tap Gesture Accessibility Service. <br><br>You don't need to enable this if the app does not tell you to. It's only required for certain actions.<br><br>Important Note: No data is collected from any of your apps, this service is simply used to provide the gesture interaction with the device.<br><br>This is a separate service due to how Android works and how apps adapt their UI when services that can perform gestures are enabled. For example, Chrome will not hide the Omnibar on scroll with this service enabled. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.kieronquinn.app.taptap.ui.activities.MainActivity → SetupLandingFragment | 首次安装/未完成设置时冷启动，导航图 startDestination=setupLandingFragment | 原生Activity | **原文**：Get started / Skip setup<br>**译注**：“开始使用”与“跳过设置”两个按钮，落地页无权限索取。 | 可选择 Get Started 进入说明，或直接 Skip Setup 跳过整个向导 | `SetupLandingFragment.setupGetStarted / SetupLandingFragment.setupSkip / res/navigation/nav_graph_setup.xml` |
| 2 | 引导说明页 | SetupInfoFragment（含 SetupInfoWarningBottomSheetFragment 警告 BottomSheet） | 点击 Get Started 后导航 action_setupLandingFragment_to_setupInfoFragment | 原生Activity | **原文**：Tap, Tap is and always will be free, building off open source components. The source code is available for anyone to view and make edits to at the GitHub repository. Official free downloads for the app are only available at XDA, the GitHub repository, and APKMirror.<br>**译注**：强调开源可审计、仅从官方渠道下载；警告页明确说明无障碍服务可自动操作设备，不应授予不信任的应用。 | 阅读后点击 Next 继续（无强制授权，可返回或跳过） | `SetupInfoFragment.setupContent（Html.fromHtml(R.string.setup_foss_info_content)）/ SetupInfoFragment.setupNext / strings.xml:setup_foss_info_bs_content` |
| 3 | 引导说明页 | SetupNotificationsFragment | SetupInfoFragment 导航 action_setupInfoFragment_to_setupNotificationsFragment | 原生Activity | **原文**：Tap, Tap uses notifications to inform you of action and gate requirements, as well as possible errors and other important app functions.<br>**译注**：说明通知用于告知动作/条件需求与错误，随后请求 POST_NOTIFICATIONS，非无障碍权限。 | 点击授权通知，或直接继续（拒绝不影响流程） | `SetupNotificationsFragment.setupGrant / strings.xml:setup_notifications_content` |
| 4 | 业务功能触发 | SetupGestureFragment（背部双击演示 + 手势配置 BottomSheet） | 导航至 setupGestureFragment 后 onViewCreated→setupState/startDemoMode，onResume 亦调用 startDemoMode | 原生Activity | **原文**：Double tap the back of your device to activate the gesture. Try to tap firmly, using the tip of your index finger. / Great! Tap to continue.<br>**译注**：引导用户实际双击机身背部触发演示；未触发时提示可调整机型尺寸与灵敏度，属功能自检而非权限索取。 | 实际双击设备背部完成演示，然后点击继续 | `SetupGestureFragment.startDemoMode / SetupGestureViewModelImpl.startService / strings.xml:setup_gesture_info_hint` |
| 5 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 用户在设置中添加需要无障碍的动作/Gate、或从通知点击启用（TapTapAction.showAccessibilityNotification / TapTapGate.showAccessibilityNotification / SettingsActionsAddGenericFragment.requestAccessibilityService） | 系统无障碍页 | **原文**：Tap, Tap Accessibility Service<br><br>Important Note: No data is collected from any of your apps, this service is simply used to keep the recognition active and provide interaction with the device<br>**译注**：系统列表内显示服务名与说明：不收集任何应用数据，仅用于保持识别活跃并与设备交互。 | 用户在系统页手动找到 Tap, Tap 并打开开关（应用不代点、不伪造页面） | `Extensions_ContextKt.getAccessibilityIntent / TapTapAction.showAccessibilityNotification / res/xml/accessibilityservice.xml` |
| 6 | 获权后动作 | TapTapAccessibilityService / TapTapGestureAccessibilityService 与 SetupCompleteFragment | 服务 onServiceConnected 后开始输入监听；向导完成进入 SetupCompleteFragment | 原生Activity | **原文**：Setup Complete / Actions & Gates may require permissions to be granted the first time they are added or used, look out for notifications to set them up.<br>**译注**：设置完成页提示：动作与条件首次使用时可能还需授权，留意通知。 | 关闭向导进入主界面 | `SetupCompleteFragment.setupClose / TapTapAccessibilityService.setupInputListener` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- SetupLandingFragment 原生落地页（Get started / Skip setup 按钮，无权限文案）
- SetupInfoFragment 原生页面内嵌 HTML TextView（R.string.setup_foss_info_content，含 GitHub/XDA/APKMirror 链接）
- SetupInfoWarningBottomSheetFragment 原生 BottomSheet（R.string.setup_foss_info_bs_content / bs_title：无障碍服务风险警告）
- SetupNotificationsFragment 原生页面（通知用途说明）
- SetupGestureFragment 原生页面 + 手势配置 BottomSheet（双击演示提示与“Not working?”帮助文案）
- SetupCompleteFragment 原生完成页
- 系统无障碍服务列表项：android:description（res/xml/accessibilityservice.xml、gesture_accessibilityservice.xml，文案来自 strings.xml:accessibility_service_description / _gesture）
- 系统通知栏：TapTapAction / TapTapGate 的“启用无障碍服务”通知按钮跳转 ACCESSIBILITY_SETTINGS；TapTapForegroundService 前台通知跳转 APPLICATION_DETAILS_SETTINGS

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Tap, Tap uses an Accessibility Service. This gives it access to perform actions on your device automatically, and should not be granted to apps you do not trust. This is why Tap, Tap is open source - so you and everyone else who wants to can look at the code and verify it's not doing anything it shouldn't be. | Tap, Tap 使用无障碍服务，这使它能自动在你的设备上执行操作，因此不应授予不信任的应用。这也是 Tap, Tap 开源的原因——任何人都可以查看代码，验证它没有做不该做的事。 | `res/values/strings.xml: setup_foss_info_bs_content` | 良性透明说明 |
| en | Important Note: No data is collected from any of your apps, this service is simply used to keep the recognition active and provide interaction with the device | 重要提示：不会收集你任何应用中的数据，该服务仅用于保持识别活跃并与设备进行交互。 | `res/values/strings.xml: accessibility_service_description（系统无障碍列表 android:description）` | 隐私承诺 |
| en | Tap, Tap is and always will be free, building off open source components. The source code is available for anyone to view and make edits to at the GitHub repository. Official free downloads for the app are only available at XDA, the GitHub repository, and APKMirror. | Tap, Tap 现在和将来都免费，基于开源组件构建。源码在 GitHub 仓库公开，任何人都可查看和修改。官方免费下载仅限 XDA、GitHub 仓库和 APKMirror。 | `res/values/strings.xml: setup_foss_info_content（SetupInfoFragment.setupContent 以 Html.fromHtml 渲染）` | 良性透明说明 |
| en | Double tap the back of your device to activate the gesture.<br>Try to tap firmly, using the tip of your index finger. | 双击设备背部以激活手势。请用食指指尖稍用力敲击。 | `res/values/strings.xml: setup_gesture_info_hint` | 良性透明说明 |
| en | You don't need to enable this if the app does not tell you to. It's only required for certain actions. | 如果应用没有提示你，就无需启用此服务；它仅用于某些特定动作。 | `res/values/strings.xml: accessibility_service_description_gesture（Tap, Tap Secondary Service）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环：SetupGestureFragment.onResume 仅在 isLoaded 后调用 startDemoMode() 播放自身演示动画，不检测无障碍启用状态、不重复拉起系统设置；未启用时动作/Gate 以通知形式提示，用户可忽略，应用停留在说明页/设置页。
- **遮罩叠层 / 高仿系统设置页**：无。未发现用于无障碍引导的 SYSTEM_ALERT_WINDOW 遮罩或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 权限用于 Reachability 可达性悬浮面板等前台功能。
- **Android 13+ 受限设置（Restricted Settings）应对**：未发现：全包仅一处 ACTION_ACCESSIBILITY_SETTINGS 构造（Extensions_ContextKt.getAccessibilityIntent），未定位到引导进入应用详情页开启“受限设置”或 Session 安装器绕过的实现；预筛 RESTRICTED_STR/SESSION_INSTALLER 线索未落到具体引导文案。
- **获权后即时行为与防撤权机制**：无。未发现获权后自点确认、或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权；TapTapAccessibilityService 仅处理输入事件用于敲击识别。
- **良性降级 / 替代方案**：有：落地页 Skip Setup 可跳过整个向导；设置页提供 Shizuku/Sui（ADB/root）替代路径与手动手势配置面板（尺寸/灵敏度），未获无障碍权限时功能提示而非阻断。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在检测到 Intent action == android.settings.ACCESSIBILITY_SETTINGS 跳转瞬间（含从通知栏点击进入）拉起 UTG，并同步截取跳转前的 SetupInfoFragment / SetupGestureFragment 页面；冷启动首启时对 MainActivity→SetupLandingFragment 也需取样。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：说明文字均为可提取文本（strings.xml → TextView/BottomSheet），非纯图片空文本。唯一需注意：无障碍申请为按需触发，若 UTG 仅在冷启动采样可能错过跳转点，需以 ACCESSIBILITY_SETTINGS 跳转为锚点。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动向导落地页** | SetupLandingFragment：id/setup_landing_title、setup_landing_get_started、setup_landing_skip_setup | 判断是否强制权限索取或提供跳过，是良性/诱导的首要分界 | 存在 Skip setup 可点击节点；页面无任何权限请求控件；按钮文本 Get started / Skip setup |
| **跳转前开源与风险说明页** | SetupInfoFragment：id/setup_foss_info_content（含 GitHub/XDA/APKMirror 链接）、setup_info_next | 核实是否以透明风险警告与来源说明换取用户知情同意，而非虚假理由 | 文本包含 Accessibility Service 风险警示；包含 github/xda/apkmirror 链接文本；单一 Next 按钮，无恐吓性措辞 |
| **功能自检演示页** | SetupGestureFragment：id/setup_gesture_lottie、setup_gesture_bottom_sheet、setup_gesture_info_card | 确认“双击背部”功能声明与实际引导一致，无遮罩覆盖系统页 | 提示文案 setup_gesture_info_hint；页面层级中无 TYPE_APPLICATION_OVERLAY 窗口；底部 BottomSheet 而非全屏遮罩 |
| **系统无障碍服务列表项** | Settings 无障碍页中 Tap, Tap / Tap, Tap Secondary Service 条目 | 核对服务名与 android:description 是否与宣传一致、有无同形字或空白挤出 | 服务名与桌面名一致；description 含“No data is collected”；无多余空白/换行隐藏文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.kieronquinn.app.taptap.utils.extensions.Extensions_ContextKt#getAccessibilityIntent`
- `com.kieronquinn.app.taptap.ui.screens.setup.landing.SetupLandingFragment#setupSkip`
- `com.kieronquinn.app.taptap.ui.screens.setup.info.SetupInfoFragment#setupContent`
- `com.kieronquinn.app.taptap.ui.screens.setup.gesture.SetupGestureFragment#onResume`
- `res/navigation/nav_graph_setup.xml`
- `res/values/strings.xml（setup_foss_info_bs_content / accessibility_service_description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，静态可见）

- **无障碍跳转点唯一且集中**：全包只有一处构造 `ACTION_ACCESSIBILITY_SETTINGS` 的 Intent，即 [Extensions_ContextKt.getAccessibilityIntent()](<resource-unit:#1.dex1 code:com.kieronquinn.app.taptap.utils.extensions.Extensions_ContextKt#getAccessibilityIntent>)；调用方共 8 处，全部是“功能所需时”的按需申请（动作/条件 Gate 添加、备份恢复、通知内按钮），不存在冷启动强制跳转。
- **设置流程是标准向导，并非诱导外壳**：`nav_graph_setup.xml` 的导航顺序为 [SetupLandingFragment](<resource-unit:#1.dex1 code:com.kieronquinn.app.taptap.ui.screens.setup.landing.SetupLandingFragment>)（Get Started / Skip Setup）→ SetupInfoFragment（开源与来源说明 + 警告 BottomSheet）→ SetupNotificationsFragment（通知授权，可跳过）→ SetupGestureFragment（背部双击演示，`startDemoMode`）→ SetupCompleteFragment。
- **文字是透明免责 + 隐私承诺**：`setup_foss_info_content` 明示开源、仅从 GitHub/XDA/APKMirror 下载；`setup_foss_info_bs_content` 直接警示“无障碍服务可自动操作设备，不应授予不信任的应用”；无障碍描述声明不收集任何数据。
- **无遮罩、无死循环、无伪造系统页**：`SetupGestureFragment.onResume` 仅在 `isLoaded` 后 `startDemoMode()`（自身演示动画），不检测设置返回态、不重跳；未发现 `SYSTEM_ALERT_WINDOW` 用于设置引导遮罩的实现，也未发现伪造无障碍开关页或自点确认。
- **降级路径明确**：落地页存在显式跳过（`setupSkip`），设置页提供 Shizuku/Sui（ADB/root）替代方案与手动配置入口，未获权时应用停留在说明页而非反复弹窗。
- **边界说明**：预筛的 `JUMP_A11Y_SETTINGS`/`RESTRICTED_STR` 未在本次核验中定位到“受限设置分步教学”实现；`APPLICATION_DETAILS_SETTINGS` 仅用于前台服务通知与手电筒权限错误跳转（`TapTapForegroundService#createForegroundNotification`、`FlashlightToggleActivity#showErrorNotification`），属常规设置跳转。未发现需要登记的恶意/违规风险命题。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请链、设置向导页、字符串资源与跳转 Intent 均完整静态可见（无壳、无 VMP、无密文动态加载）；无远端 HTML 引导页，说明文字全部来自本地 strings.xml 并以内嵌 HTML 渲染。",
  "summary_one_liner": "Tap, Tap 通过标准 Setup 向导（可跳过）以本地原生页面透明说明其无障碍用途与隐私承诺，仅在添加具体动作/条件时按需跳转系统无障碍设置，无强制、遮罩或拒权循环。",
  "disguise_identity": {
    "app_display_name": "Tap, Tap",
    "claimed_brand_or_persona": "Tap, Tap（Kieron Quinn 开源背部双击手势工具，基于 Google Columbus 模型）",
    "a11y_service_label": "Tap, Tap（主服务）/ Tap, Tap Secondary Service（手势服务）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.kieronquinn.app.taptap.ui.activities.MainActivity → SetupLandingFragment",
      "trigger_event": "首次安装/未完成设置时冷启动，导航图 startDestination=setupLandingFragment",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Get started / Skip setup",
      "shown_text_zh": "“开始使用”与“跳过设置”两个按钮，落地页无权限索取。",
      "user_action_requested": "可选择 Get Started 进入说明，或直接 Skip Setup 跳过整个向导",
      "code_anchor": "SetupLandingFragment.setupGetStarted / SetupLandingFragment.setupSkip / res/navigation/nav_graph_setup.xml"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "SetupInfoFragment（含 SetupInfoWarningBottomSheetFragment 警告 BottomSheet）",
      "trigger_event": "点击 Get Started 后导航 action_setupLandingFragment_to_setupInfoFragment",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Tap, Tap is and always will be free, building off open source components. The source code is available for anyone to view and make edits to at the GitHub repository. Official free downloads for the app are only available at XDA, the GitHub repository, and APKMirror.",
      "shown_text_zh": "强调开源可审计、仅从官方渠道下载；警告页明确说明无障碍服务可自动操作设备，不应授予不信任的应用。",
      "user_action_requested": "阅读后点击 Next 继续（无强制授权，可返回或跳过）",
      "code_anchor": "SetupInfoFragment.setupContent（Html.fromHtml(R.string.setup_foss_info_content)）/ SetupInfoFragment.setupNext / strings.xml:setup_foss_info_bs_content"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "SetupNotificationsFragment",
      "trigger_event": "SetupInfoFragment 导航 action_setupInfoFragment_to_setupNotificationsFragment",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Tap, Tap uses notifications to inform you of action and gate requirements, as well as possible errors and other important app functions.",
      "shown_text_zh": "说明通知用于告知动作/条件需求与错误，随后请求 POST_NOTIFICATIONS，非无障碍权限。",
      "user_action_requested": "点击授权通知，或直接继续（拒绝不影响流程）",
      "code_anchor": "SetupNotificationsFragment.setupGrant / strings.xml:setup_notifications_content"
    },
    {
      "step": 4,
      "stage": "业务功能触发",
      "screen_or_component": "SetupGestureFragment（背部双击演示 + 手势配置 BottomSheet）",
      "trigger_event": "导航至 setupGestureFragment 后 onViewCreated→setupState/startDemoMode，onResume 亦调用 startDemoMode",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Double tap the back of your device to activate the gesture. Try to tap firmly, using the tip of your index finger. / Great! Tap to continue.",
      "shown_text_zh": "引导用户实际双击机身背部触发演示；未触发时提示可调整机型尺寸与灵敏度，属功能自检而非权限索取。",
      "user_action_requested": "实际双击设备背部完成演示，然后点击继续",
      "code_anchor": "SetupGestureFragment.startDemoMode / SetupGestureViewModelImpl.startService / strings.xml:setup_gesture_info_hint"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户在设置中添加需要无障碍的动作/Gate、或从通知点击启用（TapTapAction.showAccessibilityNotification / TapTapGate.showAccessibilityNotification / SettingsActionsAddGenericFragment.requestAccessibilityService）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Tap, Tap Accessibility Service\n\nImportant Note: No data is collected from any of your apps, this service is simply used to keep the recognition active and provide interaction with the device",
      "shown_text_zh": "系统列表内显示服务名与说明：不收集任何应用数据，仅用于保持识别活跃并与设备交互。",
      "user_action_requested": "用户在系统页手动找到 Tap, Tap 并打开开关（应用不代点、不伪造页面）",
      "code_anchor": "Extensions_ContextKt.getAccessibilityIntent / TapTapAction.showAccessibilityNotification / res/xml/accessibilityservice.xml"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "TapTapAccessibilityService / TapTapGestureAccessibilityService 与 SetupCompleteFragment",
      "trigger_event": "服务 onServiceConnected 后开始输入监听；向导完成进入 SetupCompleteFragment",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Setup Complete / Actions & Gates may require permissions to be granted the first time they are added or used, look out for notifications to set them up.",
      "shown_text_zh": "设置完成页提示：动作与条件首次使用时可能还需授权，留意通知。",
      "user_action_requested": "关闭向导进入主界面",
      "code_anchor": "SetupCompleteFragment.setupClose / TapTapAccessibilityService.setupInputListener"
    }
  ],
  "text_presentation_locations": [
    "SetupLandingFragment 原生落地页（Get started / Skip setup 按钮，无权限文案）",
    "SetupInfoFragment 原生页面内嵌 HTML TextView（R.string.setup_foss_info_content，含 GitHub/XDA/APKMirror 链接）",
    "SetupInfoWarningBottomSheetFragment 原生 BottomSheet（R.string.setup_foss_info_bs_content / bs_title：无障碍服务风险警告）",
    "SetupNotificationsFragment 原生页面（通知用途说明）",
    "SetupGestureFragment 原生页面 + 手势配置 BottomSheet（双击演示提示与“Not working?”帮助文案）",
    "SetupCompleteFragment 原生完成页",
    "系统无障碍服务列表项：android:description（res/xml/accessibilityservice.xml、gesture_accessibilityservice.xml，文案来自 strings.xml:accessibility_service_description / _gesture）",
    "系统通知栏：TapTapAction / TapTapGate 的“启用无障碍服务”通知按钮跳转 ACCESSIBILITY_SETTINGS；TapTapForegroundService 前台通知跳转 APPLICATION_DETAILS_SETTINGS"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Tap, Tap uses an Accessibility Service. This gives it access to perform actions on your device automatically, and should not be granted to apps you do not trust. This is why Tap, Tap is open source - so you and everyone else who wants to can look at the code and verify it's not doing anything it shouldn't be.",
      "text_zh": "Tap, Tap 使用无障碍服务，这使它能自动在你的设备上执行操作，因此不应授予不信任的应用。这也是 Tap, Tap 开源的原因——任何人都可以查看代码，验证它没有做不该做的事。",
      "source_location": "res/values/strings.xml: setup_foss_info_bs_content",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Important Note: No data is collected from any of your apps, this service is simply used to keep the recognition active and provide interaction with the device",
      "text_zh": "重要提示：不会收集你任何应用中的数据，该服务仅用于保持识别活跃并与设备进行交互。",
      "source_location": "res/values/strings.xml: accessibility_service_description（系统无障碍列表 android:description）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Tap, Tap is and always will be free, building off open source components. The source code is available for anyone to view and make edits to at the GitHub repository. Official free downloads for the app are only available at XDA, the GitHub repository, and APKMirror.",
      "text_zh": "Tap, Tap 现在和将来都免费，基于开源组件构建。源码在 GitHub 仓库公开，任何人都可查看和修改。官方免费下载仅限 XDA、GitHub 仓库和 APKMirror。",
      "source_location": "res/values/strings.xml: setup_foss_info_content（SetupInfoFragment.setupContent 以 Html.fromHtml 渲染）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Double tap the back of your device to activate the gesture.\nTry to tap firmly, using the tip of your index finger.",
      "text_zh": "双击设备背部以激活手势。请用食指指尖稍用力敲击。",
      "source_location": "res/values/strings.xml: setup_gesture_info_hint",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "You don't need to enable this if the app does not tell you to. It's only required for certain actions.",
      "text_zh": "如果应用没有提示你，就无需启用此服务；它仅用于某些特定动作。",
      "source_location": "res/values/strings.xml: accessibility_service_description_gesture（Tap, Tap Secondary Service）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环：SetupGestureFragment.onResume 仅在 isLoaded 后调用 startDemoMode() 播放自身演示动画，不检测无障碍启用状态、不重复拉起系统设置；未启用时动作/Gate 以通知形式提示，用户可忽略，应用停留在说明页/设置页。",
    "overlay_or_fake_settings": "无。未发现用于无障碍引导的 SYSTEM_ALERT_WINDOW 遮罩或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 权限用于 Reachability 可达性悬浮面板等前台功能。",
    "restricted_settings_13plus_coaching": "未发现：全包仅一处 ACTION_ACCESSIBILITY_SETTINGS 构造（Extensions_ContextKt.getAccessibilityIntent），未定位到引导进入应用详情页开启“受限设置”或 Session 安装器绕过的实现；预筛 RESTRICTED_STR/SESSION_INSTALLER 线索未落到具体引导文案。",
    "post_grant_anti_removal": "无。未发现获权后自点确认、或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权；TapTapAccessibilityService 仅处理输入事件用于敲击识别。",
    "benign_graceful_degradation": "有：落地页 Skip Setup 可跳过整个向导；设置页提供 Shizuku/Sui（ADB/root）替代路径与手动手势配置面板（尺寸/灵敏度），未获无障碍权限时功能提示而非阻断。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在检测到 Intent action == android.settings.ACCESSIBILITY_SETTINGS 跳转瞬间（含从通知栏点击进入）拉起 UTG，并同步截取跳转前的 SetupInfoFragment / SetupGestureFragment 页面；冷启动首启时对 MainActivity→SetupLandingFragment 也需取样。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动向导落地页",
        "page_identifier": "SetupLandingFragment：id/setup_landing_title、setup_landing_get_started、setup_landing_skip_setup",
        "why_most_useful": "判断是否强制权限索取或提供跳过，是良性/诱导的首要分界",
        "observable_utg_signals": ["存在 Skip setup 可点击节点", "页面无任何权限请求控件", "按钮文本 Get started / Skip setup"]
      },
      {
        "page_role": "跳转前开源与风险说明页",
        "page_identifier": "SetupInfoFragment：id/setup_foss_info_content（含 GitHub/XDA/APKMirror 链接）、setup_info_next",
        "why_most_useful": "核实是否以透明风险警告与来源说明换取用户知情同意，而非虚假理由",
        "observable_utg_signals": ["文本包含 Accessibility Service 风险警示", "包含 github/xda/apkmirror 链接文本", "单一 Next 按钮，无恐吓性措辞"]
      },
      {
        "page_role": "功能自检演示页",
        "page_identifier": "SetupGestureFragment：id/setup_gesture_lottie、setup_gesture_bottom_sheet、setup_gesture_info_card",
        "why_most_useful": "确认“双击背部”功能声明与实际引导一致，无遮罩覆盖系统页",
        "observable_utg_signals": ["提示文案 setup_gesture_info_hint", "页面层级中无 TYPE_APPLICATION_OVERLAY 窗口", "底部 BottomSheet 而非全屏遮罩"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中 Tap, Tap / Tap, Tap Secondary Service 条目",
        "why_most_useful": "核对服务名与 android:description 是否与宣传一致、有无同形字或空白挤出",
        "observable_utg_signals": ["服务名与桌面名一致", "description 含“No data is collected”", "无多余空白/换行隐藏文案"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：说明文字均为可提取文本（strings.xml → TextView/BottomSheet），非纯图片空文本。唯一需注意：无障碍申请为按需触发，若 UTG 仅在冷启动采样可能错过跳转点，需以 ACCESSIBILITY_SETTINGS 跳转为锚点。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.kieronquinn.app.taptap.utils.extensions.Extensions_ContextKt#getAccessibilityIntent",
    "com.kieronquinn.app.taptap.ui.screens.setup.landing.SetupLandingFragment#setupSkip",
    "com.kieronquinn.app.taptap.ui.screens.setup.info.SetupInfoFragment#setupContent",
    "com.kieronquinn.app.taptap.ui.screens.setup.gesture.SetupGestureFragment#onResume",
    "res/navigation/nav_graph_setup.xml",
    "res/values/strings.xml（setup_foss_info_bs_content / accessibility_service_description）"
  ]
}
```

</details>
