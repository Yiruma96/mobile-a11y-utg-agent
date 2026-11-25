# BN_034__fc3fe8f232｜极简桌面与双击锁屏 — Slate

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：172.5s

## 1. 一句话核心结论

- **核心申请方式**：Slate 仅在用户主动打开设置页的“双击锁屏”开关时才弹出原生说明弹窗（含明确 Cancel 按钮），确认后直接跳系统无障碍设置列表，获权后仅调用 performGlobalAction(8) 锁屏，属透明告知型按需申请。
- **静态可见性说明**：全链路完全静态可见：classes.dex 未加壳（r8 混淆但可反编译），assets 目录仅含 PRIVACY_POLICY.md 与 dexopt baseline profile，无 HTML/JS/加密载荷；无障碍引导由 SettingsActivity 原生 Dialog + 显式 Intent 跳转实现，无 WebView、无远端配置、无动态加载。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fc3fe8f2323e78ca6ed9708a7a2067fa8fc21fe3ad90c8c14adeba27fea16a28` |
| 包名 / 年份 | `com.slate.launcher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.slate.launcher_7.apk |
| 桌面显示名 | Slate |
| 引导页宣称品牌/身份 | Slate（F-Droid 开源极简文本桌面，真实身份，无第三方品牌冒充） |
| 系统无障碍列表服务名 | Slate |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。无障碍服务 label 直接复用 @string/app_name（Slate），description 与实际行为一致；无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool（未覆写该方法）。 |
| 无障碍服务类名 | `com.slate.launcher.SlateAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |
| 系统设置项说明 (`android:description`) | Allows Slate to lock the screen on double tap while keeping biometric unlock available. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.slate.launcher.MainActivity（HOME/LAUNCHER，singleTask）/ com.slate.launcher.OnboardingActivity（label=Welcome） | onCreate / onResume；Onboarding 仅做隐私勾选与“设为默认桌面”请求 | 原生Activity | **原文**：Welcome<br>**译注**：欢迎页；仅隐私政策同意与设为默认桌面，无任何无障碍提示 | 勾选隐私同意、可选“设为默认桌面”或跳过（btnSkip） | `com.slate.launcher.OnboardingActivity.onCreate / setupPrivacyConsent / requestDefaultLauncher` |
| 2 | 业务功能触发 | com.slate.launcher.SettingsActivity — Gestures 分组中的 switchDoubleTap 开关行 | 用户点击开关（CompoundButton onCheckedChanged → setupDoubleTapListener$lambda$0），检测 isAccessibilityServiceEnabled()==false | 原生Activity | **原文**：Double tap to lock screen / Requires accessibility service permission<br>**译注**：双击锁屏 / 需要无障碍服务权限 | 用户主动开启该功能开关（默认关闭，无任何主动推送） | `com.slate.launcher.SettingsActivity#setupDoubleTapListener$lambda$0；R.string.settings_double_tap_to_lock_screen(_summary)` |
| 3 | 引导说明页 | 原生 Dialog（R.layout.dialog_accessibility_info），标题 ACCESSIBILITY SERVICE，正文 dialogBody + 隐私说明 dialogPrivacy | 开关被回弹为关闭后立即 showAccessibilityDialog() | 原生Dialog | **原文**：ACCESSIBILITY SERVICE / Double-tap to lock uses Android's Accessibility Service to lock your screen.<br><br>On the next screen, find "Slate" in the list and enable it. / Slate only uses this permission to lock the screen. No data is collected, read, or sent anywhere. / Cancel / Open Settings<br>**译注**：无障碍服务；双击锁屏使用 Android 无障碍服务锁屏。在下一个界面中，在列表里找到 "Slate" 并启用它；Slate 仅用此权限锁屏，不收集、不读取、不外发任何数据。按钮：取消 / 打开设置 | 可点 Cancel 取消（仅 dismiss，不改 pref），或点 Open Settings 继续；弹窗可点击外部取消（setCanceledOnTouchOutside(true)） | `com.slate.launcher.SettingsActivity#showAccessibilityDialog；res/layout/dialog_accessibility_info.xml；R.string.settings_accessibility_body / settings_accessibility_privacy / dialog_open_settings / common_cancel` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | 点击 btnContinue（Open Settings）→ showAccessibilityDialog$lambda$4$0：dialog.dismiss() + setAwaitingAccessibilityPermission(true) + startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：无（应用自身不再渲染任何内容，直接交由系统页面）<br>**译注**：跳转后为系统原生无障碍服务列表，用户需自行找到 Slate 并开启；应用不叠加任何遮罩或仿冒开关 | 用户在系统页面中手动启用 Slate 服务并确认系统警告 | `com.slate.launcher.SettingsActivity#showAccessibilityDialog$lambda$4$0` |
| 5 | 拒权反馈循环 | SettingsActivity.onResume → syncPermissionToggles → syncAccessibilityToggle | 从系统设置返回触发 onResume；若 awaiting=true 且服务未启用：清除 awaiting 标志，postDelayed 500ms 后把 switchDoubleTap 置回关闭 | 原生Activity | **原文**：无新增文案（开关回落为关闭状态）<br>**译注**：返回后开关保持关闭，不重复弹窗、不重复跳转，属于良性安全降级 | 无需操作；用户可稍后再次手动开启该功能 | `com.slate.launcher.SettingsActivity#syncAccessibilityToggle / #syncAccessibilityToggle$lambda$1；com.slate.launcher.AppDrawerFragment#reconcileDoubleTapPref$lambda$0（服务被撤销后自动把 pref 置 false）` |
| 6 | 获权后动作 | com.slate.launcher.SlateAccessibilityService（onAccessibilityEvent 空实现）/ AppDrawerFragment 双击手势 → Companion.lockScreen() | awaiting=true 且服务已启用 → syncAccessibilityToggle 自动勾选开关并写 setDoubleTapToLock(true)；用户双击桌面时调用 performGlobalAction(8) | 不可静态还原 | **原文**：无（无 UI，直接调用系统 GLOBAL_ACTION_LOCK_SCREEN 锁屏）<br>**译注**：获权后仅用于锁屏，不读取屏幕内容、不监听窗口内容、不阻止用户撤权 | 用户在桌面双击触发锁屏 | `com.slate.launcher.SlateAccessibilityService$Companion#lockScreen（performGlobalAction(8)）；com.slate.launcher.SlateAccessibilityService#onAccessibilityEvent（空）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：res/xml/accessibility_service.xml 的 android:description = @string/accessibility_service_description（'Allows Slate to lock the screen on double tap while keeping biometric unlock available.'），服务名显示为 @string/app_name = Slate
- SettingsActivity Gestures 分组开关行：switchDoubleTap 标题 R.string.settings_double_tap_to_lock_screen（Double tap to lock screen）与副标题 settings_double_tap_to_lock_screen_summary（Requires accessibility service permission）
- SettingsActivity 原生 Dialog（res/layout/dialog_accessibility_info.xml）：dialogTitle = R.string.dialog_accessibility_title（ACCESSIBILITY SERVICE）、dialogBody = R.string.settings_accessibility_body、dialogPrivacy = R.string.settings_accessibility_privacy、btnCancel = common_cancel、btnContinue = dialog_open_settings（Open Settings）
- AppDrawerFragment.showFaqDialog 的 FAQ 列表项：faq_accessibility_question / faq_accessibility_answer（用户长按桌面主动查阅的说明页）
- 无 WebView / 本地 HTML / 远端 HTML 承载任何引导文案；assets 目录只有 PRIVACY_POLICY.md 与 dexopt baseline profile

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Allows Slate to lock the screen on double tap while keeping biometric unlock available. | 允许 Slate 在双击时锁定屏幕，同时保留生物识别解锁可用。 | `res/values/strings.xml: accessibility_service_description（经 res/xml/accessibility_service.xml android:description 呈现）` | 良性透明说明 |
| en | Double-tap to lock uses Android's Accessibility Service to lock your screen.<br><br>On the next screen, find "Slate" in the list and enable it. | 双击锁屏使用 Android 的无障碍服务来锁定屏幕。在下一个界面中，在列表里找到 "Slate" 并启用它。 | `res/values/strings.xml: settings_accessibility_body（Dialog dialogBody）` | 良性透明说明 |
| en | Slate only uses this permission to lock the screen. No data is collected, read, or sent anywhere. | Slate 仅使用此权限锁屏。不收集、不读取、不外发任何数据到任何地方。 | `res/values/strings.xml: settings_accessibility_privacy（Dialog dialogPrivacy）` | 隐私承诺 |
| en | ACCESSIBILITY SERVICE | 无障碍服务 | `res/values/strings.xml: dialog_accessibility_title（layout dialog_accessibility_info.xml dialogTitle，textAllCaps=true）` | 良性透明说明 |
| en | Open Settings | 打开设置 | `res/values/strings.xml: dialog_open_settings（Dialog btnContinue，点击后跳系统无障碍设置）` | 受限设置分步教学 |
| en | Accessibility is used only for the "double tap to lock screen" feature. It calls a single system API (GLOBAL_ACTION_LOCK_SCREEN) to lock the device while keeping biometric unlock available.<br><br>Slate cannot read screen content, monitor app usage, or collect any data via this permission. | 无障碍仅用于“双击锁屏”功能。它只调用一个系统 API（GLOBAL_ACTION_LOCK_SCREEN）来锁屏并保留生物识别解锁。Slate 无法通过此权限读取屏幕内容、监控应用使用或收集任何数据。 | `res/values/strings.xml: faq_accessibility_answer（AppDrawerFragment.showFaqDialog）` | 隐私承诺 |
| en | Double tap to lock screen | 双击锁屏 | `res/values/strings.xml: settings_double_tap_to_lock_screen（SettingsActivity Gestures 开关标题）` | 良性透明说明 |
| en | Requires accessibility service permission | 需要无障碍服务权限 | `res/values/strings.xml: settings_double_tap_to_lock_screen_summary（开关副标题，开启前即告知）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。用户从系统设置返回后 onResume → syncAccessibilityToggle 检测到 awaiting=true 且服务未启用，清除 awaiting 标志并将开关 500ms 后置回关闭；不重弹弹窗、不重跳设置页。若用户事后在系统设置中撤销服务，AppDrawerFragment.reconcileDoubleTapPref$lambda$0 会把 doubleTapToLock pref 自动置 false，静默降级。
- **遮罩叠层 / 高仿系统设置页**：无。全包无 SYSTEM_ALERT_WINDOW 权限、无悬浮窗代码、无仿冒无障碍开关页；跳转后即为系统原生 ACCESSIBILITY_SETTINGS 页面。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。onAccessibilityEvent/onInterrupt 均为空实现，不使用 GLOBAL_ACTION_BACK/HOME 阻断撤权，不自动点击确认，不自授权。
- **良性降级 / 替代方案**：有。双击锁屏默认关闭；未授权时开关自动回弹为关并保留设置页其余功能；获权状态被撤销后仅关闭该功能，桌面其余能力（文本列表、搜索、手势、快捷条）不受影响。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 SettingsActivity 的 Gestures 分组点击 switchDoubleTap（或监测 startActivity 目标 = android.settings.ACCESSIBILITY_SETTINGS）的瞬间拉起 UTG；冷启动阶段无需拉起（MainActivity/OnboardingActivity 不涉及无障碍）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一注意点：应用为 R8 混淆（类名如 c1/c2/d1/j 为监听器壳），但业务类与方法名（SettingsActivity.showAccessibilityDialog/syncAccessibilityToggle、SlateAccessibilityService）保留完好，纯文本节点即可判别；无障碍服务 onAccessibilityEvent 为空实现意味着运行期也不会出现屏幕内容读取行为，UTG 侧无内容遮蔽风险。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **触发前设置页（开关行）** | SettingsActivity 中文本为 'Double tap to lock screen' 的 MaterialSwitch 行及其副标题 'Requires accessibility service permission' | 确认申请是否由用户主动点击业务开关触发（按需型），而非冷启动强制或后台拉起 | 开关初始为关闭状态；副标题已提前披露需要无障碍权限；无自动勾选/无倒计时 |
| **引导说明弹窗页** | Dialog（R.layout.dialog_accessibility_info）：标题 'ACCESSIBILITY SERVICE'、正文含 'find "Slate" in the list and enable it'、两个按钮 'Cancel' 与 'Open Settings' | 区分良性告知与诱导的关键页：是否存在取消按钮、文案是否如实说明单一用途与隐私边界、是否教唆忽视系统警告 | 存在可点击的 'Cancel' 文本节点；标题/正文为纯文本、无图片诱饵；隐私承诺文案与 Manifest 权限范围一致；无 'ignore warning'/'allow anyway' 类措辞 |
| **跳转目标系统无障碍列表页** | 系统 Settings 无障碍服务列表，其中 'Slate' 项 description 为 'Allows Slate to lock the screen on double tap while keeping biometric unlock available.' | 确认应用未叠加遮罩/仿冒开关页，且服务在系统中的显示名与描述和真实身份一致 | 前台包名为系统设置而非 com.slate.launcher；服务项文本为 Slate；无悬浮层覆盖该页；description 与代码实际能力（仅锁屏）一致 |
| **拒权返回后的设置页** | SettingsActivity 同一 Gestures 页，switchDoubleTap 回到关闭态 | 验证无 refusal loop（不重弹/不重跳） | 开关为关闭状态；无新弹窗出现；页面稳定停留、无周期性 startActivity |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.slate.launcher.SettingsActivity#setupDoubleTapListener$lambda$0`
- `com.slate.launcher.SettingsActivity#showAccessibilityDialog`
- `com.slate.launcher.SettingsActivity#showAccessibilityDialog$lambda$4$0`
- `com.slate.launcher.SettingsActivity#syncAccessibilityToggle`
- `com.slate.launcher.SlateAccessibilityService$Companion#lockScreen`
- `res/layout/dialog_accessibility_info.xml + res/values/strings.xml(settings_accessibility_body/settings_accessibility_privacy/accessibility_service_description)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：完全可见（clear）**。该应用无壳、无加密载荷、无 WebView/HTML 引导页、无悬浮窗、无动态加载；无障碍引导链路 100% 在 DEX 中可静态还原。

**引导链路（纯运行期 UTG 视角）**：仅"按需触发"，不存在冷启动强制弹窗。

1. 冷启动：[MainActivity](<resource-unit:#1.dex1 code:com.slate.launcher.MainActivity>)（HOME/LAUNCHER）与 [OnboardingActivity](<resource-unit:#1.dex1 code:com.slate.launcher.OnboardingActivity>)（"Welcome"，隐私勾选 + 设默认桌面）**完全不涉及无障碍**，无 a11y 提示、无 `ACTION_ACCESSIBILITY_SETTINGS` 跳转。
2. 业务触发：用户在 [SettingsActivity](<resource-unit:#1.dex1 code:com.slate.launcher.SettingsActivity>) 的 Gestures 分组打开 `switchDoubleTap`（"Double tap to lock screen" / 副标题 "Requires accessibility service permission"）。
3. 开关监听 [setupDoubleTapListener$lambda$0](<resource-unit:#1.dex1 code:com.slate.launcher.SettingsActivity#setupDoubleTapListener$lambda$0>) 先调 `isAccessibilityServiceEnabled()`；未开启则**立即把开关回弹为关**，再调用 [showAccessibilityDialog](<resource-unit:#1.dex1 code:com.slate.launcher.SettingsActivity#showAccessibilityDialog>)。
4. 引导弹窗：原生 `Dialog`（`R.layout.dialog_accessibility_info`），标题 "ACCESSIBILITY SERVICE"，正文说明用途 + 隐私承诺，底部两个按钮 `Cancel`（`common_cancel`）与 `Open Settings`（`dialog_open_settings`）；`setCanceledOnTouchOutside(true)`，**可取消、无死循环**。
5. 跳转：[showAccessibilityDialog$lambda$4$0](<resource-unit:#1.dex1 code:com.slate.launcher.SettingsActivity#showAccessibilityDialog$lambda$4$0>) 先置 `awaitingAccessibilityPermission=true`，再 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` —— 直接进系统无障碍列表，**无遮罩叠层、无高仿设置页、无 APPLICATION_DETAILS_SETTINGS 受限设置教学**（全包仅 1 处 `Settings.ACTION` 引用，且为通知监听设置）。
6. 返回处理：[syncAccessibilityToggle](<resource-unit:#1.dex1 code:com.slate.launcher.SettingsActivity#syncAccessibilityToggle>) 在 `onResume` 中核对：已开启→自动勾选并写 pref；未开启→清除 awaiting、500ms 后把开关置回关闭。**降级自然、不反复拉起**。
7. 获权后行为：`SlateAccessibilityService.onAccessibilityEvent` 为**空实现**，`onInterrupt` 空实现；唯一能力是 [Companion.lockScreen](<resource-unit:#1.dex1 code:com.slate.launcher.SlateAccessibilityService$Companion#lockScreen>) → `performGlobalAction(8)`（GLOBAL_ACTION_LOCK_SCREEN）。无读屏、无窗口读取、无 GLOBAL_ACTION_BACK/HOME 撤权阻断、无自授权。
8. 无障碍声明极简：[accessibility_service.xml](<resource-unit:#1 file:res/xml/accessibility_service.xml#L2>) 仅 `typeWindowStateChanged` + `feedbackGeneric` + `flagDefault`，`android:description` 如实说明用途，系统无障碍列表中显示 "Slate"（= `app_name`），身份无错位。

**判断**：属于**良性透明说明型**无障碍申请；无伪装身份、无空白/换行挤出、无同形字、无多 alias、无伪造 isAccessibilityTool、无病毒木马载荷。预筛命中的 `PERFORM_GLOBAL_ACTION` 已被证实仅为锁屏（code 8），`QUERY_ALL_PACKAGES`/`READ_CONTACTS`/`CALL_PHONE` 对应桌面列出应用、可选联系人搜索与直接拨号功能，与本链无关。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "全链路完全静态可见：classes.dex 未加壳（r8 混淆但可反编译），assets 目录仅含 PRIVACY_POLICY.md 与 dexopt baseline profile，无 HTML/JS/加密载荷；无障碍引导由 SettingsActivity 原生 Dialog + 显式 Intent 跳转实现，无 WebView、无远端配置、无动态加载。",
  "summary_one_liner": "Slate 仅在用户主动打开设置页的“双击锁屏”开关时才弹出原生说明弹窗（含明确 Cancel 按钮），确认后直接跳系统无障碍设置列表，获权后仅调用 performGlobalAction(8) 锁屏，属透明告知型按需申请。",
  "disguise_identity": {
    "app_display_name": "Slate",
    "claimed_brand_or_persona": "Slate（F-Droid 开源极简文本桌面，真实身份，无第三方品牌冒充）",
    "a11y_service_label": "Slate",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。无障碍服务 label 直接复用 @string/app_name（Slate），description 与实际行为一致；无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool（未覆写该方法）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.slate.launcher.MainActivity（HOME/LAUNCHER，singleTask）/ com.slate.launcher.OnboardingActivity（label=Welcome）",
      "trigger_event": "onCreate / onResume；Onboarding 仅做隐私勾选与“设为默认桌面”请求",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Welcome",
      "shown_text_zh": "欢迎页；仅隐私政策同意与设为默认桌面，无任何无障碍提示",
      "user_action_requested": "勾选隐私同意、可选“设为默认桌面”或跳过（btnSkip）",
      "code_anchor": "com.slate.launcher.OnboardingActivity.onCreate / setupPrivacyConsent / requestDefaultLauncher"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.slate.launcher.SettingsActivity — Gestures 分组中的 switchDoubleTap 开关行",
      "trigger_event": "用户点击开关（CompoundButton onCheckedChanged → setupDoubleTapListener$lambda$0），检测 isAccessibilityServiceEnabled()==false",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Double tap to lock screen / Requires accessibility service permission",
      "shown_text_zh": "双击锁屏 / 需要无障碍服务权限",
      "user_action_requested": "用户主动开启该功能开关（默认关闭，无任何主动推送）",
      "code_anchor": "com.slate.launcher.SettingsActivity#setupDoubleTapListener$lambda$0；R.string.settings_double_tap_to_lock_screen(_summary)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "原生 Dialog（R.layout.dialog_accessibility_info），标题 ACCESSIBILITY SERVICE，正文 dialogBody + 隐私说明 dialogPrivacy",
      "trigger_event": "开关被回弹为关闭后立即 showAccessibilityDialog()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "ACCESSIBILITY SERVICE / Double-tap to lock uses Android's Accessibility Service to lock your screen.\n\nOn the next screen, find \"Slate\" in the list and enable it. / Slate only uses this permission to lock the screen. No data is collected, read, or sent anywhere. / Cancel / Open Settings",
      "shown_text_zh": "无障碍服务；双击锁屏使用 Android 无障碍服务锁屏。在下一个界面中，在列表里找到 \"Slate\" 并启用它；Slate 仅用此权限锁屏，不收集、不读取、不外发任何数据。按钮：取消 / 打开设置",
      "user_action_requested": "可点 Cancel 取消（仅 dismiss，不改 pref），或点 Open Settings 继续；弹窗可点击外部取消（setCanceledOnTouchOutside(true)）",
      "code_anchor": "com.slate.launcher.SettingsActivity#showAccessibilityDialog；res/layout/dialog_accessibility_info.xml；R.string.settings_accessibility_body / settings_accessibility_privacy / dialog_open_settings / common_cancel"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "点击 btnContinue（Open Settings）→ showAccessibilityDialog$lambda$4$0：dialog.dismiss() + setAwaitingAccessibilityPermission(true) + startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用自身不再渲染任何内容，直接交由系统页面）",
      "shown_text_zh": "跳转后为系统原生无障碍服务列表，用户需自行找到 Slate 并开启；应用不叠加任何遮罩或仿冒开关",
      "user_action_requested": "用户在系统页面中手动启用 Slate 服务并确认系统警告",
      "code_anchor": "com.slate.launcher.SettingsActivity#showAccessibilityDialog$lambda$4$0"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "SettingsActivity.onResume → syncPermissionToggles → syncAccessibilityToggle",
      "trigger_event": "从系统设置返回触发 onResume；若 awaiting=true 且服务未启用：清除 awaiting 标志，postDelayed 500ms 后把 switchDoubleTap 置回关闭",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无新增文案（开关回落为关闭状态）",
      "shown_text_zh": "返回后开关保持关闭，不重复弹窗、不重复跳转，属于良性安全降级",
      "user_action_requested": "无需操作；用户可稍后再次手动开启该功能",
      "code_anchor": "com.slate.launcher.SettingsActivity#syncAccessibilityToggle / #syncAccessibilityToggle$lambda$1；com.slate.launcher.AppDrawerFragment#reconcileDoubleTapPref$lambda$0（服务被撤销后自动把 pref 置 false）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.slate.launcher.SlateAccessibilityService（onAccessibilityEvent 空实现）/ AppDrawerFragment 双击手势 → Companion.lockScreen()",
      "trigger_event": "awaiting=true 且服务已启用 → syncAccessibilityToggle 自动勾选开关并写 setDoubleTapToLock(true)；用户双击桌面时调用 performGlobalAction(8)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（无 UI，直接调用系统 GLOBAL_ACTION_LOCK_SCREEN 锁屏）",
      "shown_text_zh": "获权后仅用于锁屏，不读取屏幕内容、不监听窗口内容、不阻止用户撤权",
      "user_action_requested": "用户在桌面双击触发锁屏",
      "code_anchor": "com.slate.launcher.SlateAccessibilityService$Companion#lockScreen（performGlobalAction(8)）；com.slate.launcher.SlateAccessibilityService#onAccessibilityEvent（空）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：res/xml/accessibility_service.xml 的 android:description = @string/accessibility_service_description（'Allows Slate to lock the screen on double tap while keeping biometric unlock available.'），服务名显示为 @string/app_name = Slate",
    "SettingsActivity Gestures 分组开关行：switchDoubleTap 标题 R.string.settings_double_tap_to_lock_screen（Double tap to lock screen）与副标题 settings_double_tap_to_lock_screen_summary（Requires accessibility service permission）",
    "SettingsActivity 原生 Dialog（res/layout/dialog_accessibility_info.xml）：dialogTitle = R.string.dialog_accessibility_title（ACCESSIBILITY SERVICE）、dialogBody = R.string.settings_accessibility_body、dialogPrivacy = R.string.settings_accessibility_privacy、btnCancel = common_cancel、btnContinue = dialog_open_settings（Open Settings）",
    "AppDrawerFragment.showFaqDialog 的 FAQ 列表项：faq_accessibility_question / faq_accessibility_answer（用户长按桌面主动查阅的说明页）",
    "无 WebView / 本地 HTML / 远端 HTML 承载任何引导文案；assets 目录只有 PRIVACY_POLICY.md 与 dexopt baseline profile"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Allows Slate to lock the screen on double tap while keeping biometric unlock available.",
      "text_zh": "允许 Slate 在双击时锁定屏幕，同时保留生物识别解锁可用。",
      "source_location": "res/values/strings.xml: accessibility_service_description（经 res/xml/accessibility_service.xml android:description 呈现）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Double-tap to lock uses Android's Accessibility Service to lock your screen.\n\nOn the next screen, find \"Slate\" in the list and enable it.",
      "text_zh": "双击锁屏使用 Android 的无障碍服务来锁定屏幕。在下一个界面中，在列表里找到 \"Slate\" 并启用它。",
      "source_location": "res/values/strings.xml: settings_accessibility_body（Dialog dialogBody）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Slate only uses this permission to lock the screen. No data is collected, read, or sent anywhere.",
      "text_zh": "Slate 仅使用此权限锁屏。不收集、不读取、不外发任何数据到任何地方。",
      "source_location": "res/values/strings.xml: settings_accessibility_privacy（Dialog dialogPrivacy）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "ACCESSIBILITY SERVICE",
      "text_zh": "无障碍服务",
      "source_location": "res/values/strings.xml: dialog_accessibility_title（layout dialog_accessibility_info.xml dialogTitle，textAllCaps=true）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Settings",
      "text_zh": "打开设置",
      "source_location": "res/values/strings.xml: dialog_open_settings（Dialog btnContinue，点击后跳系统无障碍设置）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility is used only for the \"double tap to lock screen\" feature. It calls a single system API (GLOBAL_ACTION_LOCK_SCREEN) to lock the device while keeping biometric unlock available.\n\nSlate cannot read screen content, monitor app usage, or collect any data via this permission.",
      "text_zh": "无障碍仅用于“双击锁屏”功能。它只调用一个系统 API（GLOBAL_ACTION_LOCK_SCREEN）来锁屏并保留生物识别解锁。Slate 无法通过此权限读取屏幕内容、监控应用使用或收集任何数据。",
      "source_location": "res/values/strings.xml: faq_accessibility_answer（AppDrawerFragment.showFaqDialog）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Double tap to lock screen",
      "text_zh": "双击锁屏",
      "source_location": "res/values/strings.xml: settings_double_tap_to_lock_screen（SettingsActivity Gestures 开关标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Requires accessibility service permission",
      "text_zh": "需要无障碍服务权限",
      "source_location": "res/values/strings.xml: settings_double_tap_to_lock_screen_summary（开关副标题，开启前即告知）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。用户从系统设置返回后 onResume → syncAccessibilityToggle 检测到 awaiting=true 且服务未启用，清除 awaiting 标志并将开关 500ms 后置回关闭；不重弹弹窗、不重跳设置页。若用户事后在系统设置中撤销服务，AppDrawerFragment.reconcileDoubleTapPref$lambda$0 会把 doubleTapToLock pref 自动置 false，静默降级。",
    "overlay_or_fake_settings": "无。全包无 SYSTEM_ALERT_WINDOW 权限、无悬浮窗代码、无仿冒无障碍开关页；跳转后即为系统原生 ACCESSIBILITY_SETTINGS 页面。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。onAccessibilityEvent/onInterrupt 均为空实现，不使用 GLOBAL_ACTION_BACK/HOME 阻断撤权，不自动点击确认，不自授权。",
    "benign_graceful_degradation": "有。双击锁屏默认关闭；未授权时开关自动回弹为关并保留设置页其余功能；获权状态被撤销后仅关闭该功能，桌面其余能力（文本列表、搜索、手势、快捷条）不受影响。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 SettingsActivity 的 Gestures 分组点击 switchDoubleTap（或监测 startActivity 目标 = android.settings.ACCESSIBILITY_SETTINGS）的瞬间拉起 UTG；冷启动阶段无需拉起（MainActivity/OnboardingActivity 不涉及无障碍）。",
    "key_pages_to_capture": [
      {
        "page_role": "触发前设置页（开关行）",
        "page_identifier": "SettingsActivity 中文本为 'Double tap to lock screen' 的 MaterialSwitch 行及其副标题 'Requires accessibility service permission'",
        "why_most_useful": "确认申请是否由用户主动点击业务开关触发（按需型），而非冷启动强制或后台拉起",
        "observable_utg_signals": ["开关初始为关闭状态", "副标题已提前披露需要无障碍权限", "无自动勾选/无倒计时"]
      },
      {
        "page_role": "引导说明弹窗页",
        "page_identifier": "Dialog（R.layout.dialog_accessibility_info）：标题 'ACCESSIBILITY SERVICE'、正文含 'find \"Slate\" in the list and enable it'、两个按钮 'Cancel' 与 'Open Settings'",
        "why_most_useful": "区分良性告知与诱导的关键页：是否存在取消按钮、文案是否如实说明单一用途与隐私边界、是否教唆忽视系统警告",
        "observable_utg_signals": ["存在可点击的 'Cancel' 文本节点", "标题/正文为纯文本、无图片诱饵", "隐私承诺文案与 Manifest 权限范围一致", "无 'ignore warning'/'allow anyway' 类措辞"]
      },
      {
        "page_role": "跳转目标系统无障碍列表页",
        "page_identifier": "系统 Settings 无障碍服务列表，其中 'Slate' 项 description 为 'Allows Slate to lock the screen on double tap while keeping biometric unlock available.'",
        "why_most_useful": "确认应用未叠加遮罩/仿冒开关页，且服务在系统中的显示名与描述和真实身份一致",
        "observable_utg_signals": ["前台包名为系统设置而非 com.slate.launcher", "服务项文本为 Slate", "无悬浮层覆盖该页", "description 与代码实际能力（仅锁屏）一致"]
      },
      {
        "page_role": "拒权返回后的设置页",
        "page_identifier": "SettingsActivity 同一 Gestures 页，switchDoubleTap 回到关闭态",
        "why_most_useful": "验证无 refusal loop（不重弹/不重跳）",
        "observable_utg_signals": ["开关为关闭状态", "无新弹窗出现", "页面稳定停留、无周期性 startActivity"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一注意点：应用为 R8 混淆（类名如 c1/c2/d1/j 为监听器壳），但业务类与方法名（SettingsActivity.showAccessibilityDialog/syncAccessibilityToggle、SlateAccessibilityService）保留完好，纯文本节点即可判别；无障碍服务 onAccessibilityEvent 为空实现意味着运行期也不会出现屏幕内容读取行为，UTG 侧无内容遮蔽风险。"
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
    "com.slate.launcher.SettingsActivity#setupDoubleTapListener$lambda$0",
    "com.slate.launcher.SettingsActivity#showAccessibilityDialog",
    "com.slate.launcher.SettingsActivity#showAccessibilityDialog$lambda$4$0",
    "com.slate.launcher.SettingsActivity#syncAccessibilityToggle",
    "com.slate.launcher.SlateAccessibilityService$Companion#lockScreen",
    "res/layout/dialog_accessibility_info.xml + res/values/strings.xml(settings_accessibility_body/settings_accessibility_privacy/accessibility_service_description)"
  ]
}
```

</details>
