# BN_007__1556bd82dd｜专注自律与防沉迷管控 — Nudge - App Blocker

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：140.9s

## 1. 一句话核心结论

- **核心申请方式**：Nudge 在设置页 Permissions 中列出无障碍权限卡片，点击后先弹原生说明弹窗（How Nudge Works，含 Grant Permission 与 Cancel），用户确认后才跳转系统 ACTION_ACCESSIBILITY_SETTINGS，全程透明、可取消、无遮罩无死循环。
- **静态可见性说明**：全部引导逻辑位于 classes.dex 的 Compose 代码与 res/values/strings.xml、res/xml/accessibility_service_config.xml 中，完整静态可见；应用未加壳、无 WebView/HTML 引导页、无加密或远端下发页面，assets 目录仅少量小文件且不含引导资源。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1556bd82dd2dc9449524002516b39726c65342249c478c36d82dc74a514676e3` |
| 包名 / 年份 | `dev.astraedus.nudge` / 2025-2026 |
| 家族 / 品类 | **专注自律与防沉迷管控**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/dev.astraedus.nudge_79.apk |
| 桌面显示名 | Nudge - App Blocker |
| 引导页宣称品牌/身份 | Nudge（F-Droid 开源防沉迷/应用拦截工具，自称 privacy-first、无网络权限、数据不出设备） |
| 系统无障碍列表服务名 | Nudge - App Blocker（服务未单独设置 label，回落到应用名）；无障碍列表中说明为 Nudge monitors which app is in the foreground to apply your blocking rules. No data leaves your device. |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅存在常规 R8 类名混淆（如 kotlin.ResultKt.PermissionsPage 等被重命名的 Compose 入口），无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 android:isAccessibilityTool。 |
| 无障碍服务类名 | `com.astraedus.nudge.service.NudgeAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Nudge monitors which app is in the foreground to apply your blocking rules. No data leaves your device. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.astraedus.nudge.MainActivity（Compose 单 Activity 宿主，NavGraphKt 路由） | LAUNCHER 启动 → MainActivity.onCreate | 原生Activity | **原文**：无（仅 EdgeToEdge + setContent，未申请无障碍）<br>**译注**：冷启动仅同步监控服务并（Android 13+）请求通知权限，不强制申请无障碍 | 无强制操作；首次安装时进入 Onboarding 引导流程 | `com.astraedus.nudge.MainActivity#onCreate / MainActivity#routeFrom` |
| 2 | 引导说明页 | OnboardingScreen（Compose Pager，按钮 Next / Get Started） | 首次启动 ONBOARDING_COMPLETE=false 时渲染 | 原生Activity | **原文**：Next / Get Started<br>**译注**：“下一步”/“开始使用”按钮，允许直接跳过引导进入主界面 | 点击 Next 翻页或 Get Started 结束引导；无强制授权、可直接跳过 | `com.astraedus.nudge.ui.screens.onboarding.ComposableSingletons$OnboardingScreenKt$lambda-1$1#invoke；NudgePreferences$Keys.ONBOARDING_COMPLETE` |
| 3 | 业务功能触发（设置页权限清单） | SettingsScreen → Permissions 页（kotlin.ResultKt.PermissionsPage） | 用户主动进入 Settings 后点击 Permissions 分组 / 卡片点击 | 原生Activity | **原文**：Permissions / Nudge needs these permissions to work. No data is ever sent anywhere — the app has no internet permission. / Accessibility Service / Detects which app is in the foreground so Nudge can trigger your block rules. Also identifies in-app screens (like YouTube Shorts or Instagram Reels) by checking navigation elements. Does not read your messages, keystrokes, or screen content.<br>**译注**：“权限：Nudge 需要这些权限才能工作。数据从不发送到任何地方——应用没有联网权限。”无障碍卡片说明“检测前台应用以触发拦截规则，并通过导航元素识别应用内页面（如 Shorts、Reels）；不读取消息、按键或屏幕内容。” | 用户自行决定是否点击该权限卡片（另有 Display Over Other Apps、Usage Stats Access 两张卡片并列） | `kotlin.ResultKt#PermissionsPage` |
| 4 | 引导说明页（跳转前弹窗） | AccessibilityDisclosureDialog（Material3 AlertDialog，标题 How Nudge Works） | 点击 Accessibility Service 卡片 → mutableState 置 true → 组合渲染弹窗 | 原生Dialog | **原文**：How Nudge Works / Nudge uses Android's Accessibility Service to detect which app is currently open on your screen. / This lets Nudge show breathing exercises, delays, or blocks when you open apps you've chosen to limit. / Nudge only reads the name of the app in the foreground. It does not read your messages, keystrokes, passwords, or screen content. / All data stays on your device. Nudge has no internet permission and cannot send data anywhere. / Grant Permission / Cancel<br>**译注**：“Nudge 如何工作：使用 Android 无障碍服务检测当前前台应用；据此展示呼吸练习、延迟或拦截你选择限制的应用；只读取前台应用名称，不读取消息、按键、密码或屏幕内容；所有数据留在设备上，Nudge 无联网权限，无法外传数据。”按钮为“授予权限”“取消” | 二选一：Grant Permission 继续跳转系统无障碍设置，或 Cancel 关闭弹窗留在本页（有明确取消） | `com.astraedus.nudge.ui.components.TonalIconKt#AccessibilityDisclosureDialog；ComposableSingletons$AppPickerKt$lambda-1$1#invoke(case 2 正文/case 0 Cancel 图标)` |
| 5 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 弹窗确认回调：先置 dialog=false，再执行权限卡片回调 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Nudge monitors which app is in the foreground to apply your blocking rules. No data leaves your device.（系统列表项说明）<br>**译注**：系统无障碍服务列表中显示应用名 Nudge - App Blocker 与该说明，由用户手动打开开关 | 在系统页手动找到 Nudge 并开启服务；用户也可直接返回不开启 | `com.astraedus.nudge.ui.backup.BackupActionsKt$$ExternalSyntheticLambda8#invoke(case 26)；res/xml/accessibility_service_config.xml + strings.xml:accessibility_service_description` |
| 6 | 拒权反馈循环（良性降级） | 通知栏 Protection alerts + MainActivity(route=nudge.open_settings) → SettingsScreen | ProtectionStatus.isAccessibilityServiceGranted 读取 Settings.Secure "enabled_accessibility_services" 为未启用 → ProtectionAlertNotifier.notify 发送通知 | 通知栏 | **原文**：Nudge's accessibility permission is off, so apps are not being blocked. Tap to turn it back on. / Your phone shut Nudge down. It still shows as switched on, so blocking will not restart on its own — turn Nudge off and back on in Accessibility settings, or restart your phone. Tap for the steps.<br>**译注**：“Nudge 的无障碍权限已关闭，应用不再被拦截。点按可重新开启。”/“系统关闭了 Nudge 进程，开关仍显示开启但拦截不会自动恢复——请在无障碍设置中关闭再开启 Nudge，或重启手机。点按查看步骤。” | 用户可点按通知跳回应用设置页自行处理，也可忽略；不构成 onResume 死循环重跳或定时拉起 | `com.astraedus.nudge.service.ProtectionStatus#isAccessibilityServiceGranted；com.astraedus.nudge.service.ProtectionAlertNotifier#settingsIntent；strings.xml:protection_alert_accessibility_body / protection_alert_crashed_body` |
| 7 | 获权后动作 | NudgeAccessibilityService（onServiceConnected）+ NudgeMonitorService（foregroundServiceType=specialUse） | 用户在系统页开启服务 → onServiceConnected；MainActivity.onCreate 中 keepMonitorServiceInSync 保持前台服务 | 不可静态还原 | 无 | 无（正常业务运行） | `com.astraedus.nudge.service.NudgeAccessibilityService#onServiceConnected；com.astraedus.nudge.MainActivity$keepMonitorServiceInSync$1` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表说明：res/xml/accessibility_service_config.xml 的 android:description → strings.xml:accessibility_service_description（“Nudge monitors which app is in the foreground… No data leaves your device.”）
- 设置页 Permissions 区块（Compose 原生页面，kotlin.ResultKt.PermissionsPage）：标题 “Permissions” + 无联网声明 + 三张 PermissionCard（Accessibility Service / Display Over Other Apps / Usage Stats Access）说明文字
- 跳转前不可取消性为零的原生 AlertDialog：TonalIconKt.AccessibilityDisclosureDialog，标题 “How Nudge Works”，四条说明 + Grant Permission/Cancel 按钮
- Onboarding 引导页（Compose Pager）：Next / Get Started 按钮，可跳过
- 通知栏 Protection alerts 频道：protection_alert_accessibility_title/body、protection_alert_crashed_title/body、protection_alert_blocked_body（点击跳回 MainActivity 的 nudge.open_settings 路由）
- 无 WebView、无 assets HTML、无悬浮引导遮罩、无高仿系统无障碍开关页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Nudge monitors which app is in the foreground to apply your blocking rules. No data leaves your device. | Nudge 监控哪个应用处于前台，以应用你的拦截规则。数据不会离开你的设备。 | `res/values/strings.xml: accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）` | 良性透明说明 |
| en | How Nudge Works | Nudge 如何工作 | `com.astraedus.nudge.ui.components.ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 1）` | 良性透明说明 |
| en | Nudge uses Android's Accessibility Service to detect which app is currently open on your screen. | Nudge 使用 Android 无障碍服务来检测你屏幕上当前打开的是哪个应用。 | `ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 2）` | 良性透明说明 |
| en | This lets Nudge show breathing exercises, delays, or blocks when you open apps you've chosen to limit. | 这使 Nudge 在你打开已选择限制的应用时展示呼吸练习、延迟或拦截。 | `ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 2）` | 良性透明说明 |
| en | Nudge only reads the name of the app in the foreground. It does not read your messages, keystrokes, passwords, or screen content. | Nudge 只读取前台应用的名称，不读取你的消息、按键、密码或屏幕内容。 | `ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 2）` | 良性透明说明 |
| en | All data stays on your device. Nudge has no internet permission and cannot send data anywhere. | 所有数据留在你的设备上。Nudge 没有联网权限，无法把数据发送到任何地方。 | `ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 2）` | 隐私承诺 |
| en | Permissions / Nudge needs these permissions to work. No data is ever sent anywhere — the app has no internet permission. | 权限 / Nudge 需要这些权限才能工作。数据从不发送到任何地方——本应用没有联网权限。 | `kotlin.ResultKt#PermissionsPage（硬编码 Compose 文本）` | 良性透明说明 |
| en | Detects which app is in the foreground so Nudge can trigger your block rules. Also identifies in-app screens (like YouTube Shorts or Instagram Reels) by checking navigation elements. Does not read your messages, keystrokes, or screen content. | 检测哪个应用处于前台，以便 Nudge 触发你的拦截规则；并通过检查导航元素识别应用内页面（如 YouTube Shorts 或 Instagram Reels）。不读取你的消息、按键或屏幕内容。 | `kotlin.ResultKt#PermissionsPage（PermissionCard 文案）` | 良性透明说明 |
| en | Grant Permission / Cancel | 授予权限 / 取消 | `ComposableSingletons$OnboardingScreenKt$lambda-1$1#invoke（Grant Permission）与 ComposableSingletons$AppPickerKt$lambda-1$1#invoke case 0（Icon(Close, "Cancel")）` | 良性透明说明 |
| en | Nudge's accessibility permission is off, so apps are not being blocked. Tap to turn it back on. | Nudge 的无障碍权限已关闭，应用不再被拦截。点按可重新开启。 | `res/values/strings.xml: protection_alert_accessibility_body` | 故障恐吓 |
| en | Your phone shut Nudge down. It still shows as switched on, so blocking will not restart on its own — turn Nudge off and back on in Accessibility settings, or restart your phone. Tap for the steps. | 你的手机结束了 Nudge 进程。开关仍显示为开启，所以拦截不会自行恢复——请在无障碍设置中关闭再开启 Nudge，或重启手机。点按查看步骤。 | `res/values/strings.xml: protection_alert_crashed_body` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无死循环。用户取消弹窗即回到 Permissions 页；从系统设置返回后仅由 SettingsScreenKt$rememberPermissionStates$1$1$observer$1.onChange 刷新权限状态并停留在本页；未获权时仅通过 Protection alerts 通知提示（点击跳回应用设置页），不自动重跳、不定时拉起。
- **遮罩叠层 / 高仿系统设置页**：无。SYSTEM_ALERT_WINDOW 仅用于 BlockOverlayActivity / PhoneNudgeActivity 等拦截与呼吸练习页（Theme.Nudge.Overlay），不覆盖系统无障碍页；未发现高仿系统开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（代码内无受限设置/Session 安装器教学；预筛 restricted 线索 JUMP_A11Y_SETTINGS 对应的是普通 ACTION_ACCESSIBILITY_SETTINGS 跳转，RESTRICTED_STR 来自 androidx 常规受限 API 字符串）
- **获权后即时行为与防撤权机制**：无。未见自点确认、自授权、监听设置页后用 GLOBAL_ACTION_BACK/HOME 阻止撤权；PERFORM_GLOBAL_ACTION 仅用于拦截页返回等常规交互。
- **良性降级 / 替代方案**：有。引导可跳过（Next / Get Started），弹窗有 Cancel；未授权时应用继续运行并在通知栏告知“拦截未生效”，用户可自行选择去开启或忽略；声明无联网权限、数据本地存储，权限清单逐项说明用途。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（来自 BackupActionsKt$$ExternalSyntheticLambda8#invoke case 26）或点击设置页 “Accessibility Service” 卡片触发 AccessibilityDisclosureDialog 时拉起 UTG，可捕获完整说明弹窗；若验证拒权路径，则在 Settings.Secure "enabled_accessibility_services" 读取为未启用后捕获通知。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区。说明文字全部为 Compose 原生文本与 strings.xml 资源，可被 UTG 文本节点直接提取；无 WebView/HTML/图片引导，无加壳或密文载荷。唯一需要注意的是 Onboarding 的 Compose 文本可能被无障碍树合并为单一节点，需按 contentDescription/text 全量采集。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前无障碍说明弹窗页** | Compose AlertDialog，标题 How Nudge Works，含 Grant Permission 与 Cancel 两个按钮 | 这是判断是否诱导的核心：说明是否透明、是否有取消、是否恐吓或伪装 | 弹窗标题文本 How Nudge Works；说明正文四条文本节点；按钮文本 Grant Permission / Cancel 及 Cancel 是否可点 |
| **设置页权限清单页** | Permissions 标题 + Accessibility Service / Display Over Other Apps / Usage Stats Access 三张卡片 | 确认权限申请是用户主动、逐项披露用途，而非冷启动强制 | Permissions 标题与无联网声明文本；卡片标题与说明文本；是否存在跳过后仍可使用的其它入口 |
| **系统无障碍服务列表项** | 系统设置 > 无障碍 列表中 Nudge - App Blocker 条目及其说明摘要 | 核对系统侧展示名与说明是否与包内声明一致（无空白/同形字伪装） | 列表项应用名 Nudge - App Blocker；说明文本 Nudge monitors which app is in the foreground…；是否出现重复或异常同名条目 |
| **拒权后通知栏提示页** | 通知栏 Protection alerts 频道通知，含点按跳转 | 验证拒权后是良性告知还是死循环重跳/恐吓 | 通知标题 Nudge has stopped blocking；通知正文文本；点按后落地页为应用设置页而非系统页强制跳转 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `kotlin.ResultKt#PermissionsPage`
- `com.astraedus.nudge.ui.components.TonalIconKt#AccessibilityDisclosureDialog`
- `com.astraedus.nudge.ui.components.ComposableSingletons$AppPickerKt$lambda-1$1#invoke`
- `com.astraedus.nudge.ui.backup.BackupActionsKt$$ExternalSyntheticLambda8#invoke`
- `com.astraedus.nudge.service.ProtectionStatus#isAccessibilityServiceGranted`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（要点）

**性质判定：良性、透明的无障碍权限申请流程，未发现诱导或伪装行为。**

1. **权限入口清晰且用户主动**：无障碍权限只能通过用户点击触发。`MainActivity.onCreate` 仅申请 `POST_NOTIFICATIONS` 并设置 Compose 内容，**没有冷启动时强制跳转**；真正的跳转点是设置页 `Permissions` 里 “Accessibility Service” 卡片的点击回调，代码为 `BackupActionsKt$$ExternalSyntheticLambda8#invoke` case 26 → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。
2. **跳转前先展示说明弹窗（原生 AlertDialog，可取消）**：`kotlin.ResultKt.PermissionsPage` 先置 `showDialog=true`，再由 `TonalIconKt.AccessibilityDisclosureDialog` 弹出 “How Nudge Works”，包含四条逐字说明（用途、范围限制、无网络）。按钮为 “Grant Permission” 与 “Cancel”（关闭图标 `Icon(Close, "Cancel")`），**取消后回到列表，不会循环重新弹出**。
3. **身份与声明一致**：显示名 `Nudge - App Blocker`，无障碍列表中的说明为 `accessibility_service_description`：“Nudge monitors which app is in the foreground to apply your blocking rules. No data leaves your device.” 未发现空白字符或同形字挤出、未伪造 `isAccessibilityTool`（`search` 结果 `isAccessibilityTool` 无命中）、无多 `activity-alias`、无内嵌无障碍 APK。
4. **无悬浮遮罩、无假设置页、无教唆受限设置**：`SYSTEM_ALERT_WINDOW` 仅用于 `BlockOverlayActivity`、`PhoneNudgeActivity` 等拦截与呼吸练习页（`Theme.Nudge.Overlay`），未见覆盖系统无障碍页的引导遮罩；代码内无 `Settings.ACTION_MANAGE_...` 受限设置或 Session 安装器绕过教学。
5. **无拒权死循环、无获权后防撤权**：`ProtectionStatus.isAccessibilityServiceGranted` 仅通过 `Settings.Secure.getString(...,"enabled_accessibility_services")` 读取状态供 UI 展示，`SettingsScreenKt$rememberPermissionStates$1$1$observer$1.onChange` 为普通状态刷新；未见 `GLOBAL_ACTION_BACK/HOME` 阻止撤权。
6. **良性降级**：权限缺失时通过通知（`protection_alert_accessibility_body` / `protection_alert_crashed_body`）提示用户“点按去重新开启”，`ProtectionAlertNotifier#settingsIntent` 以 `nudge.open_settings` extra 拉起 `MainActivity` 到设置页，属于可忽略的告知性通知而非强制循环。
7. **佐证良性**：Manifest 无 `INTERNET` 权限，与“no internet permission”声明一致；无 WebView、无 assets 下的 HTML 引导页、无加密载荷（`static_visibility=clear`）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于 classes.dex 的 Compose 代码与 res/values/strings.xml、res/xml/accessibility_service_config.xml 中，完整静态可见；应用未加壳、无 WebView/HTML 引导页、无加密或远端下发页面，assets 目录仅少量小文件且不含引导资源。",
  "summary_one_liner": "Nudge 在设置页 Permissions 中列出无障碍权限卡片，点击后先弹原生说明弹窗（How Nudge Works，含 Grant Permission 与 Cancel），用户确认后才跳转系统 ACTION_ACCESSIBILITY_SETTINGS，全程透明、可取消、无遮罩无死循环。",
  "disguise_identity": {
    "app_display_name": "Nudge - App Blocker",
    "claimed_brand_or_persona": "Nudge（F-Droid 开源防沉迷/应用拦截工具，自称 privacy-first、无网络权限、数据不出设备）",
    "a11y_service_label": "Nudge - App Blocker（服务未单独设置 label，回落到应用名）；无障碍列表中说明为 Nudge monitors which app is in the foreground to apply your blocking rules. No data leaves your device.",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅存在常规 R8 类名混淆（如 kotlin.ResultKt.PermissionsPage 等被重命名的 Compose 入口），无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 android:isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.astraedus.nudge.MainActivity（Compose 单 Activity 宿主，NavGraphKt 路由）",
      "trigger_event": "LAUNCHER 启动 → MainActivity.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅 EdgeToEdge + setContent，未申请无障碍）",
      "shown_text_zh": "冷启动仅同步监控服务并（Android 13+）请求通知权限，不强制申请无障碍",
      "user_action_requested": "无强制操作；首次安装时进入 Onboarding 引导流程",
      "code_anchor": "com.astraedus.nudge.MainActivity#onCreate / MainActivity#routeFrom"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "OnboardingScreen（Compose Pager，按钮 Next / Get Started）",
      "trigger_event": "首次启动 ONBOARDING_COMPLETE=false 时渲染",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Next / Get Started",
      "shown_text_zh": "“下一步”/“开始使用”按钮，允许直接跳过引导进入主界面",
      "user_action_requested": "点击 Next 翻页或 Get Started 结束引导；无强制授权、可直接跳过",
      "code_anchor": "com.astraedus.nudge.ui.screens.onboarding.ComposableSingletons$OnboardingScreenKt$lambda-1$1#invoke；NudgePreferences$Keys.ONBOARDING_COMPLETE"
    },
    {
      "step": 3,
      "stage": "业务功能触发（设置页权限清单）",
      "screen_or_component": "SettingsScreen → Permissions 页（kotlin.ResultKt.PermissionsPage）",
      "trigger_event": "用户主动进入 Settings 后点击 Permissions 分组 / 卡片点击",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Permissions / Nudge needs these permissions to work. No data is ever sent anywhere — the app has no internet permission. / Accessibility Service / Detects which app is in the foreground so Nudge can trigger your block rules. Also identifies in-app screens (like YouTube Shorts or Instagram Reels) by checking navigation elements. Does not read your messages, keystrokes, or screen content.",
      "shown_text_zh": "“权限：Nudge 需要这些权限才能工作。数据从不发送到任何地方——应用没有联网权限。”无障碍卡片说明“检测前台应用以触发拦截规则，并通过导航元素识别应用内页面（如 Shorts、Reels）；不读取消息、按键或屏幕内容。”",
      "user_action_requested": "用户自行决定是否点击该权限卡片（另有 Display Over Other Apps、Usage Stats Access 两张卡片并列）",
      "code_anchor": "kotlin.ResultKt#PermissionsPage"
    },
    {
      "step": 4,
      "stage": "引导说明页（跳转前弹窗）",
      "screen_or_component": "AccessibilityDisclosureDialog（Material3 AlertDialog，标题 How Nudge Works）",
      "trigger_event": "点击 Accessibility Service 卡片 → mutableState 置 true → 组合渲染弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "How Nudge Works / Nudge uses Android's Accessibility Service to detect which app is currently open on your screen. / This lets Nudge show breathing exercises, delays, or blocks when you open apps you've chosen to limit. / Nudge only reads the name of the app in the foreground. It does not read your messages, keystrokes, passwords, or screen content. / All data stays on your device. Nudge has no internet permission and cannot send data anywhere. / Grant Permission / Cancel",
      "shown_text_zh": "“Nudge 如何工作：使用 Android 无障碍服务检测当前前台应用；据此展示呼吸练习、延迟或拦截你选择限制的应用；只读取前台应用名称，不读取消息、按键、密码或屏幕内容；所有数据留在设备上，Nudge 无联网权限，无法外传数据。”按钮为“授予权限”“取消”",
      "user_action_requested": "二选一：Grant Permission 继续跳转系统无障碍设置，或 Cancel 关闭弹窗留在本页（有明确取消）",
      "code_anchor": "com.astraedus.nudge.ui.components.TonalIconKt#AccessibilityDisclosureDialog；ComposableSingletons$AppPickerKt$lambda-1$1#invoke(case 2 正文/case 0 Cancel 图标)"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "弹窗确认回调：先置 dialog=false，再执行权限卡片回调 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Nudge monitors which app is in the foreground to apply your blocking rules. No data leaves your device.（系统列表项说明）",
      "shown_text_zh": "系统无障碍服务列表中显示应用名 Nudge - App Blocker 与该说明，由用户手动打开开关",
      "user_action_requested": "在系统页手动找到 Nudge 并开启服务；用户也可直接返回不开启",
      "code_anchor": "com.astraedus.nudge.ui.backup.BackupActionsKt$$ExternalSyntheticLambda8#invoke(case 26)；res/xml/accessibility_service_config.xml + strings.xml:accessibility_service_description"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环（良性降级）",
      "screen_or_component": "通知栏 Protection alerts + MainActivity(route=nudge.open_settings) → SettingsScreen",
      "trigger_event": "ProtectionStatus.isAccessibilityServiceGranted 读取 Settings.Secure \"enabled_accessibility_services\" 为未启用 → ProtectionAlertNotifier.notify 发送通知",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Nudge's accessibility permission is off, so apps are not being blocked. Tap to turn it back on. / Your phone shut Nudge down. It still shows as switched on, so blocking will not restart on its own — turn Nudge off and back on in Accessibility settings, or restart your phone. Tap for the steps.",
      "shown_text_zh": "“Nudge 的无障碍权限已关闭，应用不再被拦截。点按可重新开启。”/“系统关闭了 Nudge 进程，开关仍显示开启但拦截不会自动恢复——请在无障碍设置中关闭再开启 Nudge，或重启手机。点按查看步骤。”",
      "user_action_requested": "用户可点按通知跳回应用设置页自行处理，也可忽略；不构成 onResume 死循环重跳或定时拉起",
      "code_anchor": "com.astraedus.nudge.service.ProtectionStatus#isAccessibilityServiceGranted；com.astraedus.nudge.service.ProtectionAlertNotifier#settingsIntent；strings.xml:protection_alert_accessibility_body / protection_alert_crashed_body"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "NudgeAccessibilityService（onServiceConnected）+ NudgeMonitorService（foregroundServiceType=specialUse）",
      "trigger_event": "用户在系统页开启服务 → onServiceConnected；MainActivity.onCreate 中 keepMonitorServiceInSync 保持前台服务",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务连接后按前台窗口变化执行拦截/延迟/呼吸练习（BlockOverlayActivity、PhoneNudgeActivity、StrictModeGuardActivity），无自点确认、无阻止撤权动作",
      "user_action_requested": "无（正常业务运行）",
      "code_anchor": "com.astraedus.nudge.service.NudgeAccessibilityService#onServiceConnected；com.astraedus.nudge.MainActivity$keepMonitorServiceInSync$1"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表说明：res/xml/accessibility_service_config.xml 的 android:description → strings.xml:accessibility_service_description（“Nudge monitors which app is in the foreground… No data leaves your device.”）",
    "设置页 Permissions 区块（Compose 原生页面，kotlin.ResultKt.PermissionsPage）：标题 “Permissions” + 无联网声明 + 三张 PermissionCard（Accessibility Service / Display Over Other Apps / Usage Stats Access）说明文字",
    "跳转前不可取消性为零的原生 AlertDialog：TonalIconKt.AccessibilityDisclosureDialog，标题 “How Nudge Works”，四条说明 + Grant Permission/Cancel 按钮",
    "Onboarding 引导页（Compose Pager）：Next / Get Started 按钮，可跳过",
    "通知栏 Protection alerts 频道：protection_alert_accessibility_title/body、protection_alert_crashed_title/body、protection_alert_blocked_body（点击跳回 MainActivity 的 nudge.open_settings 路由）",
    "无 WebView、无 assets HTML、无悬浮引导遮罩、无高仿系统无障碍开关页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Nudge monitors which app is in the foreground to apply your blocking rules. No data leaves your device.",
      "text_zh": "Nudge 监控哪个应用处于前台，以应用你的拦截规则。数据不会离开你的设备。",
      "source_location": "res/values/strings.xml: accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "How Nudge Works",
      "text_zh": "Nudge 如何工作",
      "source_location": "com.astraedus.nudge.ui.components.ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 1）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Nudge uses Android's Accessibility Service to detect which app is currently open on your screen.",
      "text_zh": "Nudge 使用 Android 无障碍服务来检测你屏幕上当前打开的是哪个应用。",
      "source_location": "ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 2）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This lets Nudge show breathing exercises, delays, or blocks when you open apps you've chosen to limit.",
      "text_zh": "这使 Nudge 在你打开已选择限制的应用时展示呼吸练习、延迟或拦截。",
      "source_location": "ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 2）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Nudge only reads the name of the app in the foreground. It does not read your messages, keystrokes, passwords, or screen content.",
      "text_zh": "Nudge 只读取前台应用的名称，不读取你的消息、按键、密码或屏幕内容。",
      "source_location": "ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 2）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "All data stays on your device. Nudge has no internet permission and cannot send data anywhere.",
      "text_zh": "所有数据留在你的设备上。Nudge 没有联网权限，无法把数据发送到任何地方。",
      "source_location": "ComposableSingletons$AppPickerKt$lambda-1$1#invoke（硬编码，case 2）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Permissions / Nudge needs these permissions to work. No data is ever sent anywhere — the app has no internet permission.",
      "text_zh": "权限 / Nudge 需要这些权限才能工作。数据从不发送到任何地方——本应用没有联网权限。",
      "source_location": "kotlin.ResultKt#PermissionsPage（硬编码 Compose 文本）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Detects which app is in the foreground so Nudge can trigger your block rules. Also identifies in-app screens (like YouTube Shorts or Instagram Reels) by checking navigation elements. Does not read your messages, keystrokes, or screen content.",
      "text_zh": "检测哪个应用处于前台，以便 Nudge 触发你的拦截规则；并通过检查导航元素识别应用内页面（如 YouTube Shorts 或 Instagram Reels）。不读取你的消息、按键或屏幕内容。",
      "source_location": "kotlin.ResultKt#PermissionsPage（PermissionCard 文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant Permission / Cancel",
      "text_zh": "授予权限 / 取消",
      "source_location": "ComposableSingletons$OnboardingScreenKt$lambda-1$1#invoke（Grant Permission）与 ComposableSingletons$AppPickerKt$lambda-1$1#invoke case 0（Icon(Close, \"Cancel\")）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Nudge's accessibility permission is off, so apps are not being blocked. Tap to turn it back on.",
      "text_zh": "Nudge 的无障碍权限已关闭，应用不再被拦截。点按可重新开启。",
      "source_location": "res/values/strings.xml: protection_alert_accessibility_body",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Your phone shut Nudge down. It still shows as switched on, so blocking will not restart on its own — turn Nudge off and back on in Accessibility settings, or restart your phone. Tap for the steps.",
      "text_zh": "你的手机结束了 Nudge 进程。开关仍显示为开启，所以拦截不会自行恢复——请在无障碍设置中关闭再开启 Nudge，或重启手机。点按查看步骤。",
      "source_location": "res/values/strings.xml: protection_alert_crashed_body",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无死循环。用户取消弹窗即回到 Permissions 页；从系统设置返回后仅由 SettingsScreenKt$rememberPermissionStates$1$1$observer$1.onChange 刷新权限状态并停留在本页；未获权时仅通过 Protection alerts 通知提示（点击跳回应用设置页），不自动重跳、不定时拉起。",
    "overlay_or_fake_settings": "无。SYSTEM_ALERT_WINDOW 仅用于 BlockOverlayActivity / PhoneNudgeActivity 等拦截与呼吸练习页（Theme.Nudge.Overlay），不覆盖系统无障碍页；未发现高仿系统开关页。",
    "restricted_settings_13plus_coaching": "无（代码内无受限设置/Session 安装器教学；预筛 restricted 线索 JUMP_A11Y_SETTINGS 对应的是普通 ACTION_ACCESSIBILITY_SETTINGS 跳转，RESTRICTED_STR 来自 androidx 常规受限 API 字符串）",
    "post_grant_anti_removal": "无。未见自点确认、自授权、监听设置页后用 GLOBAL_ACTION_BACK/HOME 阻止撤权；PERFORM_GLOBAL_ACTION 仅用于拦截页返回等常规交互。",
    "benign_graceful_degradation": "有。引导可跳过（Next / Get Started），弹窗有 Cancel；未授权时应用继续运行并在通知栏告知“拦截未生效”，用户可自行选择去开启或忽略；声明无联网权限、数据本地存储，权限清单逐项说明用途。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（来自 BackupActionsKt$$ExternalSyntheticLambda8#invoke case 26）或点击设置页 “Accessibility Service” 卡片触发 AccessibilityDisclosureDialog 时拉起 UTG，可捕获完整说明弹窗；若验证拒权路径，则在 Settings.Secure \"enabled_accessibility_services\" 读取为未启用后捕获通知。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前无障碍说明弹窗页",
        "page_identifier": "Compose AlertDialog，标题 How Nudge Works，含 Grant Permission 与 Cancel 两个按钮",
        "why_most_useful": "这是判断是否诱导的核心：说明是否透明、是否有取消、是否恐吓或伪装",
        "observable_utg_signals": ["弹窗标题文本 How Nudge Works", "说明正文四条文本节点", "按钮文本 Grant Permission / Cancel 及 Cancel 是否可点"]
      },
      {
        "page_role": "设置页权限清单页",
        "page_identifier": "Permissions 标题 + Accessibility Service / Display Over Other Apps / Usage Stats Access 三张卡片",
        "why_most_useful": "确认权限申请是用户主动、逐项披露用途，而非冷启动强制",
        "observable_utg_signals": ["Permissions 标题与无联网声明文本", "卡片标题与说明文本", "是否存在跳过后仍可使用的其它入口"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 > 无障碍 列表中 Nudge - App Blocker 条目及其说明摘要",
        "why_most_useful": "核对系统侧展示名与说明是否与包内声明一致（无空白/同形字伪装）",
        "observable_utg_signals": ["列表项应用名 Nudge - App Blocker", "说明文本 Nudge monitors which app is in the foreground…", "是否出现重复或异常同名条目"]
      },
      {
        "page_role": "拒权后通知栏提示页",
        "page_identifier": "通知栏 Protection alerts 频道通知，含点按跳转",
        "why_most_useful": "验证拒权后是良性告知还是死循环重跳/恐吓",
        "observable_utg_signals": ["通知标题 Nudge has stopped blocking", "通知正文文本", "点按后落地页为应用设置页而非系统页强制跳转"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区。说明文字全部为 Compose 原生文本与 strings.xml 资源，可被 UTG 文本节点直接提取；无 WebView/HTML/图片引导，无加壳或密文载荷。唯一需要注意的是 Onboarding 的 Compose 文本可能被无障碍树合并为单一节点，需按 contentDescription/text 全量采集。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "kotlin.ResultKt#PermissionsPage",
    "com.astraedus.nudge.ui.components.TonalIconKt#AccessibilityDisclosureDialog",
    "com.astraedus.nudge.ui.components.ComposableSingletons$AppPickerKt$lambda-1$1#invoke",
    "com.astraedus.nudge.ui.backup.BackupActionsKt$$ExternalSyntheticLambda8#invoke",
    "com.astraedus.nudge.service.ProtectionStatus#isAccessibilityServiceGranted",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
