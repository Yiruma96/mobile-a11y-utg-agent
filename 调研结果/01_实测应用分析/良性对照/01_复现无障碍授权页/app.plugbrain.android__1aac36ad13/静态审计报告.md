# BN_001__1aac36ad13｜专注自律与防沉迷管控 — PlugBrain ������

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：165.4s

## 1. 一句话核心结论

- **核心申请方式**：PlugBrain 在原生 Compose 引导页内以「Accessibility permission」说明卡+底部教学 Sheet 明确告知用途并给出 Not now 选项，用户同意后仅跳转标准系统无障碍设置页，无遮罩、无伪造界面、无死循环催办。
- **静态可见性说明**：引导链完整静态可见：OnboardingActivity / MainActivity 的 Compose 引导页、权限页与底部教学 Sheet 均为包内原生代码，跳转字符串 android.settings.ACCESSIBILITY_SETTINGS 明文硬编码于 a1.k0#a；无加壳、无加密资源、无 WebView 或远端 HTML 承载文案。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1aac36ad13aeba62ebe4120956165648c6fbbc45585dd85b98c11d9878a19bf0` |
| 包名 / 年份 | `app.plugbrain.android` / 2025-2026 |
| 家族 / 品类 | **专注自律与防沉迷管控**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/app.plugbrain.android_165.apk |
| 桌面显示名 | PlugBrain 🧠（android:label=@string/app_name_with_brain_icon） |
| 引导页宣称品牌/身份 | PlugBrain（F-Droid 开源专注自律/屏幕时间管控应用，真实身份） |
| 系统无障碍列表服务名 | 无自定义 label，系统无障碍列表显示应用名 PlugBrain，说明为 res/values/strings.xml 中 accessibility_service_description：Detects when you open an app you chose to block so PlugBrain can show a math challenge. Only the app's name is read. |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。预筛显示名出现乱码是名称内 emoji（🧠）解码失败所致，非空白字符、换行挤出、同形字或多 activity-alias 伪装；服务未设置 android:label，未伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `app.plugbrain.android.service.MathLockService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Detects when you open an app you chose to block so PlugBrain can show a math challenge. Only the app's name is read. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | app.plugbrain.android.ui.onboarding.OnboardingActivity（Compose 引导流） | 首次启动由 MainActivity 引导进入 OnboardingActivity.onCreate → setContent(p6.f) 渲染引导步骤 | 原生Activity | **原文**：Accessibility permission / Allows PlugBrain to detect when apps are open.<br>**译注**：无障碍权限 / 允许 PlugBrain 检测当前打开的应用。 | 阅读说明，选择同意（Agree and continue）或拒绝（Not now） | `app.plugbrain.android.ui.onboarding.OnboardingActivity#onCreate / p6.f#e / res/values/strings.xml onboarding_accessibility_title、onboarding_accessibility_description` |
| 2 | 引导说明页 | OnboardingActivity 权限说明卡 + 完整披露正文（Compose Text） | 进入无障碍权限步骤时渲染 onboarding_accessibility_disclosure 全文 | 原生Activity | **原文**：PlugBrain uses the Accessibility service to see which app is open. When you open an app you chose to block, or a calculator during a challenge, PlugBrain shows a math challenge first.<br><br>PlugBrain only reads the app's name. It doesn't read what's on your screen or what you type, and nothing leaves your phone.<br>**译注**：PlugBrain 使用无障碍服务查看当前打开的应用。当你打开自己选择屏蔽的应用，或挑战过程中打开计算器时，PlugBrain 会先弹出一道数学题。PlugBrain 只读取应用名称，不读取屏幕内容和你的输入，且数据不会离开你的手机。 | 点击 Agree and continue 继续；点击 Not now 放弃（存在明确取消路径） | `res/values/strings.xml onboarding_accessibility_disclosure / onboarding_accessibility_accept / onboarding_accessibility_decline` |
| 3 | 遮罩叠层指引 | 应用内底部教学 Sheet（Compose ModalBottomSheet 风格面板，非系统悬浮窗） | 用户点击 Agree and continue 后先展示分步操作指引，再由用户点击 Use PlugBrain 触发跳转 | 原生Dialog | **原文**：Turn the accessibility service on / Find PlugBrain, then turn on the switch and confirm. / Use PlugBrain<br>**译注**：开启无障碍服务 / 找到 PlugBrain，然后打开开关并确认。/ 使用 PlugBrain | 按指引在系统页找到 PlugBrain 并开启开关；可关闭该面板放弃 | `res/values/strings.xml onboarding_accessibility_sheet_title、onboarding_accessibility_sheet_toggle、onboarding_accessibility_sheet_switch` |
| 4 | 跳无障碍设置 | 系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS） | OnboardingActivity 权限回调 p6.i 枚举 ordinal==2 → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").setFlags(FLAG_ACTIVITY_NEW_TASK)) | 系统无障碍页 | **原文**：Detects when you open an app you chose to block so PlugBrain can show a math challenge. Only the app's name is read.<br>**译注**：检测你打开被选择屏蔽的应用，以便 PlugBrain 显示数学挑战。仅读取应用名称。 | 在系统列表中打开 PlugBrain 的开关并确认（系统级确认弹窗由 Android 提供） | `a1.k0#a (case 5, p6.i ordinal==2) / res/xml/accessibility_service_config.xml / res/values/strings.xml accessibility_service_description` |
| 5 | 跳受限设置 | 系统「使用情况访问」页 / 「显示在其他应用上层」页 / 电池优化豁免页 | 引导流中其他权限步骤分别调用 n3.a.A()（USAGE_ACCESS_SETTINGS，失败回退无 package 版本）、n3.a.z()（MANAGE_OVERLAY_PERMISSION）、n3.a.y()（REQUEST_IGNORE_BATTERY_OPTIMIZATIONS） | 系统无障碍页 | **原文**：PlugBrain needs the following permissions to work correctly. / Allow the required permissions to proceed. / Ensures that PlugBrain keeps running reliably even when your device tries to save battery.<br>**译注**：PlugBrain 需要以下权限才能正常工作。/ 请允许所需权限以继续。/ 确保即使设备尝试省电时 PlugBrain 也能可靠运行。 | 在各系统页手动打开对应开关；页面含 Proceed 按钮，未授权时停留在本页 | `n3.a#A / n3.a#z / n3.a#y / p6.e#c / res/values/strings.xml onboarding_permissions_subtitle、onboarding_permissions_helper、onboarding_battery_description` |
| 6 | 拒权反馈循环 | 主面板（MainActivity）无障碍未开启提示 + 再次跳设置入口 | MainActivity 检测无障碍未启用时渲染提示；用户点击入口经 a1.k0#a case 4 再次跳 ACCESSIBILITY_SETTINGS | 原生Activity | **原文**：Accessibility access was turned off, so PlugBrain can't block your apps.<br>**译注**：无障碍权限已被关闭，因此 PlugBrain 无法屏蔽你的应用。 | 用户可自行决定是否重新开启；无自动循环重跳、无定时拉起 | `app.plugbrain.android.ui.main.MainActivity#j / a1.k0#a (case 4) / res/values/strings.xml dashboard_paused_accessibility` |
| 7 | 获权后动作 | app.plugbrain.android.service.MathLockService（无障碍服务）+ ChallengeActivity（数学挑战页） | onServiceConnected 注册事件；onAccessibilityEvent 收到 TYPE_WINDOW_STATE_CHANGED(32) 时取 getPackageName()，命中本地 distractiveApps 集合且满足冷却条件即拉起 ChallengeActivity | 原生Activity | **原文**：无（服务内仅 Toast 提示，界面文案位于 ChallengeActivity 资源）<br>**译注**：获权后仅按包名判断是否为被屏蔽应用并弹出数学挑战，不采集屏幕内容、不执行全局操作撤权。 | 用户完成数学挑战后方可继续使用被屏蔽应用 | `app.plugbrain.android.service.MathLockService#onAccessibilityEvent / app.plugbrain.android.service.MathLockService#onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- OnboardingActivity 原生 Compose 引导页：无障碍权限标题、用途说明与完整披露正文（strings: onboarding_accessibility_title / _description / _disclosure）
- OnboardingActivity 内应用自有底部教学 Sheet：标题「Turn the accessibility service on」与分步指引「Find PlugBrain, then turn on the switch and confirm.」（非系统悬浮窗、非高仿系统界面）
- 系统无障碍服务列表项：应用名 PlugBrain + android:description（res/xml/accessibility_service_config.xml → accessibility_service_description）
- OnboardingActivity 权限汇总页：onboarding_permissions_subtitle / onboarding_permissions_helper / onboarding_permissions_cta（Proceed）
- MainActivity 主面板：无障碍被关闭提示 dashboard_paused_accessibility
- 跳转目标均为 Android 标准系统设置页（ACCESSIBILITY_SETTINGS / USAGE_ACCESS_SETTINGS / MANAGE_OVERLAY_PERMISSION / REQUEST_IGNORE_BATTERY_OPTIMIZATIONS），无任何 WebView、HTML 或远端页面承载引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility permission | 无障碍权限 | `res/values/strings.xml onboarding_accessibility_title` | 良性透明说明 |
| en | Allows PlugBrain to detect when apps are open. | 允许 PlugBrain 检测当前打开的应用。 | `res/values/strings.xml onboarding_accessibility_description` | 良性透明说明 |
| en | PlugBrain uses the Accessibility service to see which app is open. When you open an app you chose to block, or a calculator during a challenge, PlugBrain shows a math challenge first.<br><br>PlugBrain only reads the app's name. It doesn't read what's on your screen or what you type, and nothing leaves your phone. | PlugBrain 使用无障碍服务查看当前打开的应用。当你打开自己选择屏蔽的应用，或挑战过程中打开计算器时，PlugBrain 会先弹出一道数学题。PlugBrain 只读取应用名称，不读取屏幕内容和你的输入，且数据不会离开你的手机。 | `res/values/strings.xml onboarding_accessibility_disclosure` | 隐私承诺 |
| en | Agree and continue | 同意并继续 | `res/values/strings.xml onboarding_accessibility_accept` | 良性透明说明 |
| en | Not now | 暂不 | `res/values/strings.xml onboarding_accessibility_decline` | 良性透明说明 |
| en | Turn the accessibility service on | 开启无障碍服务 | `res/values/strings.xml onboarding_accessibility_sheet_title` | 受限设置分步教学 |
| en | Find PlugBrain, then turn on the switch and confirm. | 找到 PlugBrain，然后打开开关并确认。 | `res/values/strings.xml onboarding_accessibility_sheet_toggle` | 受限设置分步教学 |
| en | Detects when you open an app you chose to block so PlugBrain can show a math challenge. Only the app's name is read. | 检测你打开被选择屏蔽的应用，以便 PlugBrain 显示数学挑战。仅读取应用名称。 | `res/values/strings.xml accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）` | 良性透明说明 |
| en | Accessibility access was turned off, so PlugBrain can't block your apps. | 无障碍权限已被关闭，因此 PlugBrain 无法屏蔽你的应用。 | `res/values/strings.xml dashboard_paused_accessibility` | 良性透明说明 |
| en | PlugBrain needs the following permissions to work correctly. | PlugBrain 需要以下权限才能正常工作。 | `res/values/strings.xml onboarding_permissions_subtitle` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性安全降级：点击 Not now 或返回后不自动重跳、无定时器拉起；未授权时主面板仅静态显示 dashboard_paused_accessibility 提示，由用户自行点击入口再次跳转系统页
- **遮罩叠层 / 高仿系统设置页**：无。引导用底部教学 Sheet 为应用内 Compose 组件，非 SYSTEM_ALERT_WINDOW 悬浮窗，也非高仿系统无障碍开关页；跳转目标为 Android 标准设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。未见监听无障碍设置页、disableSelf、performGlobalAction 撤权阻止或自动点击确认逻辑（performGlobalAction 仅见 x5.b.a 一处调用点，未展开用途，不构成撤权反制证据）
- **良性降级 / 替代方案**：存在。未授权无障碍时应用不阻断使用，仅提示无法屏蔽应用；电池优化与悬浮窗在引导中明确标注为可选（Battery optimization (optional)）；使用情况访问跳转失败时回退为不带 package 的通用设置页

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 Intent.ACTION_VIEW/显式 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间抓取（来源 a1.k0#a 与 MainActivity#j 的 a1.k0.a 回调），并同时抓取跳转前 1~2 帧的 OnboardingActivity 权限页与底部教学 Sheet
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。全部引导文案来自 res/values/strings.xml 明文资源与原生 Compose 组件，静态与 UTG 均可完整读取；未发现纯图片引导、空白文本诱导、一阶段 Dropper 或加壳/加密载荷。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页（无障碍权限说明卡）** | OnboardingActivity 界面标题 Accessibility permission，正文含 Allows PlugBrain to detect when apps are open. 与完整披露段落，底部按钮 Agree and continue / Not now | 决定该应用是否在跳转前完整披露用途与范围、是否提供取消路径，是区分透明引导与诱导的关键 | 标题与正文文案节点文本；是否存在 Not now 可点击节点；无 WebView 节点（纯原生 Compose 视图树） |
| **跳转前分步教学 Sheet** | 应用内底部面板，标题 Turn the accessibility service on，正文 Find PlugBrain, then turn on the switch and confirm.，按钮 Use PlugBrain | 确认指引是应用内面板还是系统悬浮窗遮罩，以及是否出现伪造系统开关界面 | 面板节点位于应用包名视图树内而非 TYPE_APPLICATION_OVERLAY 窗口；无仿系统 Switch/确认按钮控件；存在关闭入口 |
| **系统无障碍服务列表项** | Settings 无障碍页中 PlugBrain 条目及其描述文本 | 核对系统侧显示的服务名与描述是否与包内配置一致，判断是否存在身份伪装 | 条目显示名 PlugBrain；描述文本与 accessibility_service_description 一致 |
| **拒权返回后的主面板** | MainActivity 提示 Accessibility access was turned off, so PlugBrain can't block your apps. | 判断拒权后是否存在死循环重跳或强迫性催办 | 返回后停留于本页而非立即再次进入设置页；无高频弹窗/Toast 循环；页面仍可正常导航 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `a1.k0#a`
- `app.plugbrain.android.ui.onboarding.OnboardingActivity#onCreate`
- `app.plugbrain.android.ui.onboarding.OnboardingActivity#j`
- `app.plugbrain.android.service.MathLockService#onAccessibilityEvent`
- `n3.a#A`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

分析已完成，工具调用预算已用尽，以下是结论。

## 核心结论

- **无障碍申请方式：完全良性的原生透明引导**。引导链全部在 Compose 原生界面内实现，**无 WebView、无本地/远端 HTML、无悬浮窗遮罩、无高仿系统设置页**。
- 跳转点集中在两处：`a1.k0#a`（协程回调内按枚举分派 `Intent("android.settings.ACCESSIBILITY_SETTINGS")`）与 `MainActivity`（`a1.k0.a` case 4）；旁路还包括 `n3.a.A()`（`USAGE_ACCESS_SETTINGS`）、`n3.a.z()`（`MANAGE_OVERLAY_PERMISSION`）、`n3.a.y()`（`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`），均为标准系统页且带 `package:` 限定。
- **文案透明且明确告知范围**：[strings.xml (lines 170-179)](<resource-unit:#1 file:res/values/strings.xml#L170-L179>) 提供 "Agree and continue" / "Not now" 双向选择，disclosure 明确写出"只读取应用名，不读取屏幕内容和输入，数据不出手机"。
- **无障碍服务配置最小化**：[accessibility_service_config.xml (lines 1-3)](<resource-unit:#1 file:res/xml/accessibility_service_config.xml#L1-L3>) 仅 `typeWindowStateChanged`、`notificationTimeout=100`，**无** `canRetrieveWindowContent`、无 `flagRequestFilterKeyEvents`、无 `canPerformGestures`。
- **获权后行为与描述一致**：[MathLockService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:app.plugbrain.android.service.MathLockService#onAccessibilityEvent>) 仅在事件类型 32（`TYPE_WINDOW_STATE_CHANGED`）时取 `getPackageName()`，与本地 `distractiveApps` 集合比对后弹出 `ChallengeActivity`；未见监听无障碍设置页、`disableSelf`、撤权阻止或 `GLOBAL_ACTION_BACK` 反制（`performGlobalAction` 仅见 `x5.b.a` 一处调用，未展开用途，不构成本题证据）。
- **身份无伪装**：`android:label=@string/app_name_with_brain_icon`，服务无自定义 label，系统列表显示真实应用名 PlugBrain；预筛显示名乱码系名称内 emoji（🧠）解码所致，非空白/同形字混淆。
- **拒权反馈**：未授予时停留在权限页并显示 helper 文案 "Allow the required permissions to proceed."，`MainActivity` 面板显示 "Accessibility access was turned off, so PlugBrain can't block your apps."，属安全降级而非死循环重跳。

未登记风险（未发现可单独成立的恶意/违规命题）；证据边界：`MainActivity.j`（848 指令）与 `x5.b.a` 的 `performGlobalAction` 用途未逐行展开，但不影响"引导为良性透明"的判定。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链完整静态可见：OnboardingActivity / MainActivity 的 Compose 引导页、权限页与底部教学 Sheet 均为包内原生代码，跳转字符串 android.settings.ACCESSIBILITY_SETTINGS 明文硬编码于 a1.k0#a；无加壳、无加密资源、无 WebView 或远端 HTML 承载文案。",
  "summary_one_liner": "PlugBrain 在原生 Compose 引导页内以「Accessibility permission」说明卡+底部教学 Sheet 明确告知用途并给出 Not now 选项，用户同意后仅跳转标准系统无障碍设置页，无遮罩、无伪造界面、无死循环催办。",
  "disguise_identity": {
    "app_display_name": "PlugBrain 🧠（android:label=@string/app_name_with_brain_icon）",
    "claimed_brand_or_persona": "PlugBrain（F-Droid 开源专注自律/屏幕时间管控应用，真实身份）",
    "a11y_service_label": "无自定义 label，系统无障碍列表显示应用名 PlugBrain，说明为 res/values/strings.xml 中 accessibility_service_description：Detects when you open an app you chose to block so PlugBrain can show a math challenge. Only the app's name is read.",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。预筛显示名出现乱码是名称内 emoji（🧠）解码失败所致，非空白字符、换行挤出、同形字或多 activity-alias 伪装；服务未设置 android:label，未伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "app.plugbrain.android.ui.onboarding.OnboardingActivity（Compose 引导流）",
      "trigger_event": "首次启动由 MainActivity 引导进入 OnboardingActivity.onCreate → setContent(p6.f) 渲染引导步骤",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility permission / Allows PlugBrain to detect when apps are open.",
      "shown_text_zh": "无障碍权限 / 允许 PlugBrain 检测当前打开的应用。",
      "user_action_requested": "阅读说明，选择同意（Agree and continue）或拒绝（Not now）",
      "code_anchor": "app.plugbrain.android.ui.onboarding.OnboardingActivity#onCreate / p6.f#e / res/values/strings.xml onboarding_accessibility_title、onboarding_accessibility_description"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "OnboardingActivity 权限说明卡 + 完整披露正文（Compose Text）",
      "trigger_event": "进入无障碍权限步骤时渲染 onboarding_accessibility_disclosure 全文",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "PlugBrain uses the Accessibility service to see which app is open. When you open an app you chose to block, or a calculator during a challenge, PlugBrain shows a math challenge first.\n\nPlugBrain only reads the app's name. It doesn't read what's on your screen or what you type, and nothing leaves your phone.",
      "shown_text_zh": "PlugBrain 使用无障碍服务查看当前打开的应用。当你打开自己选择屏蔽的应用，或挑战过程中打开计算器时，PlugBrain 会先弹出一道数学题。PlugBrain 只读取应用名称，不读取屏幕内容和你的输入，且数据不会离开你的手机。",
      "user_action_requested": "点击 Agree and continue 继续；点击 Not now 放弃（存在明确取消路径）",
      "code_anchor": "res/values/strings.xml onboarding_accessibility_disclosure / onboarding_accessibility_accept / onboarding_accessibility_decline"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "应用内底部教学 Sheet（Compose ModalBottomSheet 风格面板，非系统悬浮窗）",
      "trigger_event": "用户点击 Agree and continue 后先展示分步操作指引，再由用户点击 Use PlugBrain 触发跳转",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Turn the accessibility service on / Find PlugBrain, then turn on the switch and confirm. / Use PlugBrain",
      "shown_text_zh": "开启无障碍服务 / 找到 PlugBrain，然后打开开关并确认。/ 使用 PlugBrain",
      "user_action_requested": "按指引在系统页找到 PlugBrain 并开启开关；可关闭该面板放弃",
      "code_anchor": "res/values/strings.xml onboarding_accessibility_sheet_title、onboarding_accessibility_sheet_toggle、onboarding_accessibility_sheet_switch"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "OnboardingActivity 权限回调 p6.i 枚举 ordinal==2 → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").setFlags(FLAG_ACTIVITY_NEW_TASK))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Detects when you open an app you chose to block so PlugBrain can show a math challenge. Only the app's name is read.",
      "shown_text_zh": "检测你打开被选择屏蔽的应用，以便 PlugBrain 显示数学挑战。仅读取应用名称。",
      "user_action_requested": "在系统列表中打开 PlugBrain 的开关并确认（系统级确认弹窗由 Android 提供）",
      "code_anchor": "a1.k0#a (case 5, p6.i ordinal==2) / res/xml/accessibility_service_config.xml / res/values/strings.xml accessibility_service_description"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统「使用情况访问」页 / 「显示在其他应用上层」页 / 电池优化豁免页",
      "trigger_event": "引导流中其他权限步骤分别调用 n3.a.A()（USAGE_ACCESS_SETTINGS，失败回退无 package 版本）、n3.a.z()（MANAGE_OVERLAY_PERMISSION）、n3.a.y()（REQUEST_IGNORE_BATTERY_OPTIMIZATIONS）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "PlugBrain needs the following permissions to work correctly. / Allow the required permissions to proceed. / Ensures that PlugBrain keeps running reliably even when your device tries to save battery.",
      "shown_text_zh": "PlugBrain 需要以下权限才能正常工作。/ 请允许所需权限以继续。/ 确保即使设备尝试省电时 PlugBrain 也能可靠运行。",
      "user_action_requested": "在各系统页手动打开对应开关；页面含 Proceed 按钮，未授权时停留在本页",
      "code_anchor": "n3.a#A / n3.a#z / n3.a#y / p6.e#c / res/values/strings.xml onboarding_permissions_subtitle、onboarding_permissions_helper、onboarding_battery_description"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "主面板（MainActivity）无障碍未开启提示 + 再次跳设置入口",
      "trigger_event": "MainActivity 检测无障碍未启用时渲染提示；用户点击入口经 a1.k0#a case 4 再次跳 ACCESSIBILITY_SETTINGS",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility access was turned off, so PlugBrain can't block your apps.",
      "shown_text_zh": "无障碍权限已被关闭，因此 PlugBrain 无法屏蔽你的应用。",
      "user_action_requested": "用户可自行决定是否重新开启；无自动循环重跳、无定时拉起",
      "code_anchor": "app.plugbrain.android.ui.main.MainActivity#j / a1.k0#a (case 4) / res/values/strings.xml dashboard_paused_accessibility"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "app.plugbrain.android.service.MathLockService（无障碍服务）+ ChallengeActivity（数学挑战页）",
      "trigger_event": "onServiceConnected 注册事件；onAccessibilityEvent 收到 TYPE_WINDOW_STATE_CHANGED(32) 时取 getPackageName()，命中本地 distractiveApps 集合且满足冷却条件即拉起 ChallengeActivity",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（服务内仅 Toast 提示，界面文案位于 ChallengeActivity 资源）",
      "shown_text_zh": "获权后仅按包名判断是否为被屏蔽应用并弹出数学挑战，不采集屏幕内容、不执行全局操作撤权。",
      "user_action_requested": "用户完成数学挑战后方可继续使用被屏蔽应用",
      "code_anchor": "app.plugbrain.android.service.MathLockService#onAccessibilityEvent / app.plugbrain.android.service.MathLockService#onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "OnboardingActivity 原生 Compose 引导页：无障碍权限标题、用途说明与完整披露正文（strings: onboarding_accessibility_title / _description / _disclosure）",
    "OnboardingActivity 内应用自有底部教学 Sheet：标题「Turn the accessibility service on」与分步指引「Find PlugBrain, then turn on the switch and confirm.」（非系统悬浮窗、非高仿系统界面）",
    "系统无障碍服务列表项：应用名 PlugBrain + android:description（res/xml/accessibility_service_config.xml → accessibility_service_description）",
    "OnboardingActivity 权限汇总页：onboarding_permissions_subtitle / onboarding_permissions_helper / onboarding_permissions_cta（Proceed）",
    "MainActivity 主面板：无障碍被关闭提示 dashboard_paused_accessibility",
    "跳转目标均为 Android 标准系统设置页（ACCESSIBILITY_SETTINGS / USAGE_ACCESS_SETTINGS / MANAGE_OVERLAY_PERMISSION / REQUEST_IGNORE_BATTERY_OPTIMIZATIONS），无任何 WebView、HTML 或远端页面承载引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility permission",
      "text_zh": "无障碍权限",
      "source_location": "res/values/strings.xml onboarding_accessibility_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Allows PlugBrain to detect when apps are open.",
      "text_zh": "允许 PlugBrain 检测当前打开的应用。",
      "source_location": "res/values/strings.xml onboarding_accessibility_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "PlugBrain uses the Accessibility service to see which app is open. When you open an app you chose to block, or a calculator during a challenge, PlugBrain shows a math challenge first.\n\nPlugBrain only reads the app's name. It doesn't read what's on your screen or what you type, and nothing leaves your phone.",
      "text_zh": "PlugBrain 使用无障碍服务查看当前打开的应用。当你打开自己选择屏蔽的应用，或挑战过程中打开计算器时，PlugBrain 会先弹出一道数学题。PlugBrain 只读取应用名称，不读取屏幕内容和你的输入，且数据不会离开你的手机。",
      "source_location": "res/values/strings.xml onboarding_accessibility_disclosure",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Agree and continue",
      "text_zh": "同意并继续",
      "source_location": "res/values/strings.xml onboarding_accessibility_accept",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Not now",
      "text_zh": "暂不",
      "source_location": "res/values/strings.xml onboarding_accessibility_decline",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn the accessibility service on",
      "text_zh": "开启无障碍服务",
      "source_location": "res/values/strings.xml onboarding_accessibility_sheet_title",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Find PlugBrain, then turn on the switch and confirm.",
      "text_zh": "找到 PlugBrain，然后打开开关并确认。",
      "source_location": "res/values/strings.xml onboarding_accessibility_sheet_toggle",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Detects when you open an app you chose to block so PlugBrain can show a math challenge. Only the app's name is read.",
      "text_zh": "检测你打开被选择屏蔽的应用，以便 PlugBrain 显示数学挑战。仅读取应用名称。",
      "source_location": "res/values/strings.xml accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility access was turned off, so PlugBrain can't block your apps.",
      "text_zh": "无障碍权限已被关闭，因此 PlugBrain 无法屏蔽你的应用。",
      "source_location": "res/values/strings.xml dashboard_paused_accessibility",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "PlugBrain needs the following permissions to work correctly.",
      "text_zh": "PlugBrain 需要以下权限才能正常工作。",
      "source_location": "res/values/strings.xml onboarding_permissions_subtitle",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性安全降级：点击 Not now 或返回后不自动重跳、无定时器拉起；未授权时主面板仅静态显示 dashboard_paused_accessibility 提示，由用户自行点击入口再次跳转系统页",
    "overlay_or_fake_settings": "无。引导用底部教学 Sheet 为应用内 Compose 组件，非 SYSTEM_ALERT_WINDOW 悬浮窗，也非高仿系统无障碍开关页；跳转目标为 Android 标准设置页",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。未见监听无障碍设置页、disableSelf、performGlobalAction 撤权阻止或自动点击确认逻辑（performGlobalAction 仅见 x5.b.a 一处调用点，未展开用途，不构成撤权反制证据）",
    "benign_graceful_degradation": "存在。未授权无障碍时应用不阻断使用，仅提示无法屏蔽应用；电池优化与悬浮窗在引导中明确标注为可选（Battery optimization (optional)）；使用情况访问跳转失败时回退为不带 package 的通用设置页"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 Intent.ACTION_VIEW/显式 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间抓取（来源 a1.k0#a 与 MainActivity#j 的 a1.k0.a 回调），并同时抓取跳转前 1~2 帧的 OnboardingActivity 权限页与底部教学 Sheet",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页（无障碍权限说明卡）",
        "page_identifier": "OnboardingActivity 界面标题 Accessibility permission，正文含 Allows PlugBrain to detect when apps are open. 与完整披露段落，底部按钮 Agree and continue / Not now",
        "why_most_useful": "决定该应用是否在跳转前完整披露用途与范围、是否提供取消路径，是区分透明引导与诱导的关键",
        "observable_utg_signals": ["标题与正文文案节点文本", "是否存在 Not now 可点击节点", "无 WebView 节点（纯原生 Compose 视图树）"]
      },
      {
        "page_role": "跳转前分步教学 Sheet",
        "page_identifier": "应用内底部面板，标题 Turn the accessibility service on，正文 Find PlugBrain, then turn on the switch and confirm.，按钮 Use PlugBrain",
        "why_most_useful": "确认指引是应用内面板还是系统悬浮窗遮罩，以及是否出现伪造系统开关界面",
        "observable_utg_signals": ["面板节点位于应用包名视图树内而非 TYPE_APPLICATION_OVERLAY 窗口", "无仿系统 Switch/确认按钮控件", "存在关闭入口"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中 PlugBrain 条目及其描述文本",
        "why_most_useful": "核对系统侧显示的服务名与描述是否与包内配置一致，判断是否存在身份伪装",
        "observable_utg_signals": ["条目显示名 PlugBrain", "描述文本与 accessibility_service_description 一致"]
      },
      {
        "page_role": "拒权返回后的主面板",
        "page_identifier": "MainActivity 提示 Accessibility access was turned off, so PlugBrain can't block your apps.",
        "why_most_useful": "判断拒权后是否存在死循环重跳或强迫性催办",
        "observable_utg_signals": ["返回后停留于本页而非立即再次进入设置页", "无高频弹窗/Toast 循环", "页面仍可正常导航"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。全部引导文案来自 res/values/strings.xml 明文资源与原生 Compose 组件，静态与 UTG 均可完整读取；未发现纯图片引导、空白文本诱导、一阶段 Dropper 或加壳/加密载荷。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "a1.k0#a",
    "app.plugbrain.android.ui.onboarding.OnboardingActivity#onCreate",
    "app.plugbrain.android.ui.onboarding.OnboardingActivity#j",
    "app.plugbrain.android.service.MathLockService#onAccessibilityEvent",
    "n3.a#A",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
