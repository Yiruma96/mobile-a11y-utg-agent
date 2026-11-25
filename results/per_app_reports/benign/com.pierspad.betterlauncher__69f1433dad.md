# BN_033__69f1433dad｜极简桌面与双击锁屏 — BetterLauncher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：125.7s

## 1. 一句话核心结论

- **核心申请方式**：应用仅在用户启用双击锁屏或应用限额等功能后，冷启动时以原生可取消说明弹窗做一次透明度告知，用户点同意才跳系统无障碍设置页（优先直达本应用服务详情），点拒绝则记录已展示并静默降级，无循环重弹、无遮罩、无伪造设置页。
- **静态可见性说明**：全部引导逻辑位于 classes.dex（未混淆关键路径，符号可读），弹窗与跳转均由 s1.a / u2.a / app.olauncher.MainActivity 明文实现；文案集中在 res/values/strings.xml（accessibility_disclosure* 系列）。无加壳、无 AES 载荷、无远端 HTML、无 WebView 参与。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `69f1433daddd24a18ca96a9205759b3600d213457863021434d043091492762e` |
| 包名 / 年份 | `com.pierspad.betterlauncher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.pierspad.betterlauncher_153.apk |
| 桌面显示名 | BetterLauncher |
| 引导页宣称品牌/身份 | BetterLauncher（F-Droid 开源极简桌面，无第三方品牌伪装） |
| 系统无障碍列表服务名 | BetterLauncher |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务 android:label 直接引用 @string/app_name；描述文本与弹窗正文同文；未使用 activity-alias 伪装、未伪造 isAccessibilityTool、无空白/换行挤出警告、无同形字。 |
| 无障碍服务类名 | `app.olauncher.helper.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, READ_CONTACTS` |
| 系统设置项说明 (`android:description`) | BetterLauncher uses the Android AccessibilityService API for optional double-tap screen locking and app limits you configure.<br><br>It accesses foreground app package names and window-change events to detect when a limited app opens or closes, and clicked view information (view type and accessibility label) to recognise the screen-lock gesture. When a selected app is in cooldown, it returns to the home screen and displays the remaining cooldown. App-limit settings and cooldown timestamps are stored only on your device.<br><br>Accessibility data is processed on your device and is not sent to servers or shared with third parties. You can decline and continue using the launcher without these features, or disable the service at any time in Android Accessibility settings.<br><br>Optional Xiaomi gestures use this same service to detect edge swipes and perform Back, Home and Recents. Unused edge touches are replayed locally. No additional accessibility service is required. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | app.olauncher.MainActivity（HOME/LAUNCHER 入口，singleTask） | onCreate：if ((prefs.v() \|\| prefs.d() \|\| prefs.W()) && !s1.a.x(this) && getSharedPreferences("accessibility_consent",0).getInt("shown_version",0) != 2) → s1.a.T(this) | 原生Dialog | **原文**：Accessibility service<br>**译注**：无障碍服务（弹窗标题）；仅在用户已启用相关功能且尚未确认时展示一次 | 阅读说明后选择同意或拒绝（非强制、非不可取消） | `app.olauncher.MainActivity.onCreate` |
| 2 | 引导说明页 | u2.a 构建的 AlertDialog（原生弹窗，标题+正文+两个按钮） | s1.a.T(context) 构造并 show() | 原生Dialog | **原文**：BetterLauncher uses the Android AccessibilityService API for optional double-tap screen locking and app limits you configure.<br><br>It accesses foreground app package names and window-change events to detect when a limited app opens or closes, and clicked view information (view type and accessibility label) to recognise the screen-lock gesture. When a selected app is in cooldown, it returns to the home screen and displays the remaining cooldown. App-limit settings and cooldown timestamps are stored only on your device.<br><br>Accessibility data is processed on your device and is not sent to servers or shared with third parties. You can decline and continue using the launcher without these features, or disable the service at any time in Android Accessibility settings.<br><br>Optional Xiaomi gestures use this same service to detect edge swipes and perform Back, Home and Recents. Unused edge touches are replayed locally. No additional accessibility service is required.<br>**译注**：BetterLauncher 使用 Android AccessibilityService API，用于可选的“双击锁屏”和用户自行配置的应用限额。它会读取前台应用包名与窗口变化事件，以判断受限应用何时打开或关闭；读取被点击视图信息（视图类型与无障碍标签）以识别锁屏手势。被选中应用处于冷却期时，它会返回主屏并显示剩余冷却时间。限额设置与冷却时间戳仅保存在本机。无障碍数据在设备本地处理，不会发送到服务器，也不会与第三方共享。你可以拒绝并继续在不启用这些功能的情况下使用启动器，也可随时在 Android 无障碍设置中关闭该服务。可选的小米手势复用同一服务检测边缘滑动并执行返回、主屏和最近任务；未使用的边缘触摸在本地回放，无需额外的无障碍服务。 | 同意（I agree — open settings）或拒绝（No thanks），两者均可点击 | `res/values/strings.xml#L29-L35 (accessibility_disclosure_message)` |
| 3 | 跳受限设置 | 系统设置页：android.settings.ACCESSIBILITY_DETAILS_SETTINGS（带 android.intent.extra.COMPONENT_NAME），失败回退 android.settings.ACCESSIBILITY_SETTINGS | u2.a.onClick case 0：写入 accepted_version=2、shown_version=2 并 commit()，dismiss 后调用 s1.a.N(context) | 系统无障碍页 | **原文**：I agree — open settings<br>**译注**：我同意 — 打开设置（点击后直达本应用的无障碍服务开关项） | 在系统无障碍页面手动打开 BetterLauncher 服务开关 | `u2.a.onClick / s1.a.N` |
| 4 | 拒权反馈循环 | 同一原生 AlertDialog（无后续弹窗、无 onResume 重跳） | u2.a.onClick default 分支：仅 putInt("shown_version", 2).apply() 后 dismiss() | 原生Dialog | **原文**：No thanks<br>**译注**：不用了（拒绝后仅记录已展示，不再自动弹出，功能降级为不可用） | 无需操作；后续仍可在设置页主动点击“Accessibility: lock and app limits”重新触发（SettingsFragment.onClick → s1.a.M → 已同意则直接跳设置，未同意则再弹说明） | `u2.a.onClick / app.olauncher.ui.SettingsFragment.onClick → s1.a.M` |
| 5 | 业务功能触发 | app.olauncher.ui.SettingsFragment（设置项点击/长按） | onClick/onLongClick → s1.a.M(context)：if (x(context)) N(context) else T(context) | 原生Activity | **原文**：Accessibility: lock and app limits<br>**译注**：无障碍：锁屏与应用限额（设置页中的功能入口项） | 用户主动点击功能项，按需进入说明或设置页 | `app.olauncher.ui.SettingsFragment.onClick / s1.a.M` |
| 6 | 获权后动作 | app.olauncher.helper.MyAccessibilityService | onServiceConnected / onAccessibilityEvent：先读 accessibility_consent.accepted_version，!= 2 则不执行任何监听逻辑 | 不可静态还原（系统无障碍服务，无 UI） | **原文**：BetterLauncher uses the Android AccessibilityService API for optional double-tap screen locking and app limits you configure.<br>**译注**：系统无障碍列表中的服务描述，与弹窗正文同文；获权后服务仅在用户同意前提下按配置处理前台包名/窗口变化与点击事件，冷却期回主屏 | 无；未发现自点确认、未监听设置页阻止撤权 | `app.olauncher.helper.MyAccessibilityService.onAccessibilityEvent / res/xml/accessibility_service_config.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml 的 accessibility_disclosure_title（"Accessibility service"）作为原生 AlertDialog 标题
- res/values/strings.xml 的 accessibility_disclosure_message 作为该 AlertDialog 正文（由 s1.a.T → u2.a 构建）
- res/values/strings.xml 的 accessibility_disclosure_accept / accessibility_disclosure_decline 作为弹窗两个按钮文案
- res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description，显示在系统无障碍服务列表项下方
- res/values/strings.xml 的 accessibility_features（"Accessibility: lock and app limits"）作为应用内设置页功能项标题
- res/values/strings.xml 的 accessibility_disclosure（"Please turn on BetterLauncher's accessibility service in your device's settings ... Our accessibility service does not collect or share any data."）为说明性提示文案，属原生文本资源，未通过 WebView/HTML 呈现

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please turn on BetterLauncher's accessibility service in your device's settings to enable Double tap to lock gesture. <br><br>Please note that this service is only used for this particular feature. Our accessibility service does not collect or share any data. | 请在设备设置中开启 BetterLauncher 的无障碍服务，以启用“双击锁屏”手势。请注意，该服务仅用于这一特定功能。我们的无障碍服务不收集也不共享任何数据。 | `res/values/strings.xml key=accessibility_disclosure` | 良性透明说明 |
| en | Accessibility service | 无障碍服务 | `res/values/strings.xml key=accessibility_disclosure_title（弹窗标题）` | 良性透明说明 |
| en | I agree — open settings | 我同意 — 打开设置 | `res/values/strings.xml key=accessibility_disclosure_accept（弹窗肯定按钮）` | 良性透明说明 |
| en | No thanks | 不用了 | `res/values/strings.xml key=accessibility_disclosure_decline（弹窗拒绝按钮，可取消）` | 良性透明说明 |
| en | Accessibility data is processed on your device and is not sent to servers or shared with third parties. You can decline and continue using the launcher without these features, or disable the service at any time in Android Accessibility settings. | 无障碍数据在设备本地处理，不会发送到服务器，也不会与第三方共享。你可以拒绝并继续在不启用这些功能的情况下使用启动器，也可随时在 Android 无障碍设置中关闭该服务。 | `res/values/strings.xml key=accessibility_disclosure_message / accessibility_service_description` | 隐私承诺 |
| en | Accessibility: lock and app limits | 无障碍：锁屏与应用限额 | `res/values/strings.xml key=accessibility_features（设置页功能项）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：点 No thanks 仅写入 shown_version=2 并关闭弹窗；无 onResume 重跳、无定时器拉起、无后台重启重弹，功能静默降级（双击锁屏/限额不可用，启动器照常使用）；再次进入需用户主动点击设置页功能项（SettingsFragment.onClick → s1.a.M，此时未同意会再弹一次说明）。
- **遮罩叠层 / 高仿系统设置页**：无。未声明 SYSTEM_ALERT_WINDOW，无悬浮窗/半透明遮罩，无高仿系统无障碍开关页；跳转目标为真实系统设置（ACCESSIBILITY_DETAILS_SETTINGS 带 COMPONENT_NAME，失败回退 ACCESSIBILITY_SETTINGS）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。onAccessibilityEvent 中 performGlobalAction 仅用于“受限应用冷却期回主屏”（对应 app limits 功能），未用于监听设置页并阻止撤权；未发现自点确认、自授权或 WATCH_SETTINGS 式回跳。
- **良性降级 / 替代方案**：有。弹窗明确告知“You can decline and continue using the launcher without these features”，拒绝后桌面启动器、快捷方式、小组件等主体功能不受影响；无障碍能力仅在 accepted_version==2 时启用。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在用户于设置页启用双击锁屏/应用限额后重启应用（或首次启用后返回主界面），监测到 Activity 变为 app.olauncher.MainActivity 且随后出现 Dialog 窗口时拉起 UTG；更精确的信号是监测到 Intent 跳转 android.settings.ACCESSIBILITY_DETAILS_SETTINGS（含 extra COMPONENT_NAME=app.olauncher.helper.MyAccessibilityService）或回退的 android.settings.ACCESSIBILITY_SETTINGS 时，抓取跳转前后窗口栈。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区。全部引导文案为原生字符串资源与原生 Dialog，无图片引导、无 WebView/HTML、无远端下发。唯一需注意：说明弹窗仅在用户已启用相关功能（prefs v()/d()/W()）后才会出现，未启用功能的设备冷启动不会弹窗，UTG 若仅做冷启动采集会漏检；建议先进入设置页启用“双击锁屏”或“应用限额”再复现。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **功能按需触发的原生说明弹窗页** | app.olauncher.MainActivity 上叠加的 AlertDialog，标题文本为 "Accessibility service"，按钮为 "I agree — open settings" / "No thanks" | 该页是唯一引导入口，直接决定是否属诱导：是否可取消、文案是否如实披露读取范围与数据流向、是否含恐吓/假更新话术，均可在此页一次性判定 | 弹窗存在两个可点击按钮且其中之一为拒绝/取消（No thanks）；正文包含读取范围声明（foreground app package names / window-change events / clicked view information）与本地处理声明；标题与系统无障碍列表服务名一致为 BetterLauncher，无第三方品牌 |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载的服务中的 BetterLauncher 条目，摘要为 accessibility_service_description 文本 | 核对 android:label 与 android:description 是否与弹窗一致、有无空白挤出/同形字伪装；可验证应用未伪造 isAccessibilityTool 使服务免于系统警示 | 服务名与桌面应用名一致（BetterLauncher）；描述首句为 "BetterLauncher uses the Android AccessibilityService API for optional double-tap screen locking and app limits you configure."；未出现空白行/异常字符挤出警告文案 |
| **跳转后系统无障碍详情开关页** | android.settings.ACCESSIBILITY_DETAILS_SETTINGS 打开的本应用服务开关页 | 验证跳转为真实系统页（含系统标题栏与开关），无压栈遮罩或高仿开关页；并观察获权返回后是否自动重跳/自动开启 | 页面包名为 com.android.settings 而非本应用；返回应用后未出现二次弹窗或强制重跳；开关状态仅由用户操作改变 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `app.olauncher.MainActivity.onCreate`
- `s1.a.N`
- `s1.a.M`
- `u2.a.onClick`
- `app.olauncher.helper.MyAccessibilityService.onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 页面流转视角）

**结论：未发现诱导或强制开启无障碍的行为；这是典型“功能按需 + 透明说明 + 可拒绝”的良性模式。**

1. **入口分层，不会在冷启动时立即拦截**：`MainActivity.onCreate` 中，只有当用户已在设置里启用相关功能（`prefs.v()/d()/W()` 为真，对应双击锁屏、应用限额等）时，才判断 `!s1.a.x(this)`（即尚未同意，`accessibility_consent.accepted_version != 2`）且 `shown_version != 2`，然后调用 `s1.a.T(this)` 弹出说明弹窗。也就是说，该弹窗属于**功能触发的提示**，并非冷启动时无条件弹出。
2. **说明弹窗为原生对话框，可取消**：标题 `Accessibility service`，正文逐项说明用途（双击锁屏、应用限额）、读取范围（前台包名、窗口变化事件、点击视图类型与无障碍标签）、数据仅本地处理、可拒绝并继续使用启动器。两个按钮：`I agree — open settings` 与 `No thanks`（[u2.a.onClick](<resource-unit:#1.dex1 code:u2.a#onClick>)）。
3. **拒绝后会正常退出，不会循环重弹**：点 `No thanks` 只写入 `shown_version=2` 并关闭弹窗，不重跳；`onResume` 无强制重弹逻辑，弹窗不再自动出现（后续需用户到设置页主动点击）。
4. **跳转是标准系统页，无遮罩、无假设置页**：[s1.a.N()](<resource-unit:#1.dex1 code:s1.a#N>) 优先 `android.settings.ACCESSIBILITY_DETAILS_SETTINGS` + `COMPONENT_NAME`（直达本应用服务开关项），异常时回退 `android.settings.ACCESSIBILITY_SETTINGS`。全程未发现 `ACTION_APPLICATION_DETAILS_SETTINGS`、悬浮窗（`SYSTEM_ALERT_WINDOW` 缺失）、无本地/远端 WebView 教学页、无“右上角菜单允许受限设置”13+ 教唆文案。
5. **获权后不会阻止撤权**：`MyAccessibilityService` 仅声明 `typeViewClicked|typeWindowStateChanged`、`canRetrieveWindowContent`、`canPerformGestures`，`android:label=@string/app_name`（真实品牌 BetterLauncher），`accessibility_service_config.xml` 未伪造 `isAccessibilityTool`；`onAccessibilityEvent` 首先校验 `accepted_version == 2`，未同意则服务完全惰性。`performGlobalAction` 仅在“受限应用冷却中”用于回主页（对应描述中的 app limits），非 `GLOBAL_ACTION_BACK` 循环阻止撤权。
6. **系统侧文案与弹窗文案一致且诚实**：`android:description` = `accessibility_service_description`，与弹窗正文 `accessibility_disclosure_message` 完全同文，明确“数据不外发、可拒绝、可随时关闭”。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于 classes.dex（未混淆关键路径，符号可读），弹窗与跳转均由 s1.a / u2.a / app.olauncher.MainActivity 明文实现；文案集中在 res/values/strings.xml（accessibility_disclosure* 系列）。无加壳、无 AES 载荷、无远端 HTML、无 WebView 参与。",
  "summary_one_liner": "应用仅在用户启用双击锁屏或应用限额等功能后，冷启动时以原生可取消说明弹窗做一次透明度告知，用户点同意才跳系统无障碍设置页（优先直达本应用服务详情），点拒绝则记录已展示并静默降级，无循环重弹、无遮罩、无伪造设置页。",
  "disguise_identity": {
    "app_display_name": "BetterLauncher",
    "claimed_brand_or_persona": "BetterLauncher（F-Droid 开源极简桌面，无第三方品牌伪装）",
    "a11y_service_label": "BetterLauncher",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务 android:label 直接引用 @string/app_name；描述文本与弹窗正文同文；未使用 activity-alias 伪装、未伪造 isAccessibilityTool、无空白/换行挤出警告、无同形字。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "app.olauncher.MainActivity（HOME/LAUNCHER 入口，singleTask）",
      "trigger_event": "onCreate：if ((prefs.v() || prefs.d() || prefs.W()) && !s1.a.x(this) && getSharedPreferences(\"accessibility_consent\",0).getInt(\"shown_version\",0) != 2) → s1.a.T(this)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Accessibility service",
      "shown_text_zh": "无障碍服务（弹窗标题）；仅在用户已启用相关功能且尚未确认时展示一次",
      "user_action_requested": "阅读说明后选择同意或拒绝（非强制、非不可取消）",
      "code_anchor": "app.olauncher.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "u2.a 构建的 AlertDialog（原生弹窗，标题+正文+两个按钮）",
      "trigger_event": "s1.a.T(context) 构造并 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "BetterLauncher uses the Android AccessibilityService API for optional double-tap screen locking and app limits you configure.\n\nIt accesses foreground app package names and window-change events to detect when a limited app opens or closes, and clicked view information (view type and accessibility label) to recognise the screen-lock gesture. When a selected app is in cooldown, it returns to the home screen and displays the remaining cooldown. App-limit settings and cooldown timestamps are stored only on your device.\n\nAccessibility data is processed on your device and is not sent to servers or shared with third parties. You can decline and continue using the launcher without these features, or disable the service at any time in Android Accessibility settings.\n\nOptional Xiaomi gestures use this same service to detect edge swipes and perform Back, Home and Recents. Unused edge touches are replayed locally. No additional accessibility service is required.",
      "shown_text_zh": "BetterLauncher 使用 Android AccessibilityService API，用于可选的“双击锁屏”和用户自行配置的应用限额。它会读取前台应用包名与窗口变化事件，以判断受限应用何时打开或关闭；读取被点击视图信息（视图类型与无障碍标签）以识别锁屏手势。被选中应用处于冷却期时，它会返回主屏并显示剩余冷却时间。限额设置与冷却时间戳仅保存在本机。无障碍数据在设备本地处理，不会发送到服务器，也不会与第三方共享。你可以拒绝并继续在不启用这些功能的情况下使用启动器，也可随时在 Android 无障碍设置中关闭该服务。可选的小米手势复用同一服务检测边缘滑动并执行返回、主屏和最近任务；未使用的边缘触摸在本地回放，无需额外的无障碍服务。",
      "user_action_requested": "同意（I agree — open settings）或拒绝（No thanks），两者均可点击",
      "code_anchor": "res/values/strings.xml#L29-L35 (accessibility_disclosure_message)"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置页：android.settings.ACCESSIBILITY_DETAILS_SETTINGS（带 android.intent.extra.COMPONENT_NAME），失败回退 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "u2.a.onClick case 0：写入 accepted_version=2、shown_version=2 并 commit()，dismiss 后调用 s1.a.N(context)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "I agree — open settings",
      "shown_text_zh": "我同意 — 打开设置（点击后直达本应用的无障碍服务开关项）",
      "user_action_requested": "在系统无障碍页面手动打开 BetterLauncher 服务开关",
      "code_anchor": "u2.a.onClick / s1.a.N"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "同一原生 AlertDialog（无后续弹窗、无 onResume 重跳）",
      "trigger_event": "u2.a.onClick default 分支：仅 putInt(\"shown_version\", 2).apply() 后 dismiss()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "No thanks",
      "shown_text_zh": "不用了（拒绝后仅记录已展示，不再自动弹出，功能降级为不可用）",
      "user_action_requested": "无需操作；后续仍可在设置页主动点击“Accessibility: lock and app limits”重新触发（SettingsFragment.onClick → s1.a.M → 已同意则直接跳设置，未同意则再弹说明）",
      "code_anchor": "u2.a.onClick / app.olauncher.ui.SettingsFragment.onClick → s1.a.M"
    },
    {
      "step": 5,
      "stage": "业务功能触发",
      "screen_or_component": "app.olauncher.ui.SettingsFragment（设置项点击/长按）",
      "trigger_event": "onClick/onLongClick → s1.a.M(context)：if (x(context)) N(context) else T(context)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility: lock and app limits",
      "shown_text_zh": "无障碍：锁屏与应用限额（设置页中的功能入口项）",
      "user_action_requested": "用户主动点击功能项，按需进入说明或设置页",
      "code_anchor": "app.olauncher.ui.SettingsFragment.onClick / s1.a.M"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "app.olauncher.helper.MyAccessibilityService",
      "trigger_event": "onServiceConnected / onAccessibilityEvent：先读 accessibility_consent.accepted_version，!= 2 则不执行任何监听逻辑",
      "ui_carrier": "不可静态还原（系统无障碍服务，无 UI）",
      "shown_text_verbatim": "BetterLauncher uses the Android AccessibilityService API for optional double-tap screen locking and app limits you configure.",
      "shown_text_zh": "系统无障碍列表中的服务描述，与弹窗正文同文；获权后服务仅在用户同意前提下按配置处理前台包名/窗口变化与点击事件，冷却期回主屏",
      "user_action_requested": "无；未发现自点确认、未监听设置页阻止撤权",
      "code_anchor": "app.olauncher.helper.MyAccessibilityService.onAccessibilityEvent / res/xml/accessibility_service_config.xml"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml 的 accessibility_disclosure_title（\"Accessibility service\"）作为原生 AlertDialog 标题",
    "res/values/strings.xml 的 accessibility_disclosure_message 作为该 AlertDialog 正文（由 s1.a.T → u2.a 构建）",
    "res/values/strings.xml 的 accessibility_disclosure_accept / accessibility_disclosure_decline 作为弹窗两个按钮文案",
    "res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description，显示在系统无障碍服务列表项下方",
    "res/values/strings.xml 的 accessibility_features（\"Accessibility: lock and app limits\"）作为应用内设置页功能项标题",
    "res/values/strings.xml 的 accessibility_disclosure（\"Please turn on BetterLauncher's accessibility service in your device's settings ... Our accessibility service does not collect or share any data.\"）为说明性提示文案，属原生文本资源，未通过 WebView/HTML 呈现"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please turn on BetterLauncher's accessibility service in your device's settings to enable Double tap to lock gesture. \n\nPlease note that this service is only used for this particular feature. Our accessibility service does not collect or share any data.",
      "text_zh": "请在设备设置中开启 BetterLauncher 的无障碍服务，以启用“双击锁屏”手势。请注意，该服务仅用于这一特定功能。我们的无障碍服务不收集也不共享任何数据。",
      "source_location": "res/values/strings.xml key=accessibility_disclosure",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service",
      "text_zh": "无障碍服务",
      "source_location": "res/values/strings.xml key=accessibility_disclosure_title（弹窗标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "I agree — open settings",
      "text_zh": "我同意 — 打开设置",
      "source_location": "res/values/strings.xml key=accessibility_disclosure_accept（弹窗肯定按钮）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "No thanks",
      "text_zh": "不用了",
      "source_location": "res/values/strings.xml key=accessibility_disclosure_decline（弹窗拒绝按钮，可取消）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility data is processed on your device and is not sent to servers or shared with third parties. You can decline and continue using the launcher without these features, or disable the service at any time in Android Accessibility settings.",
      "text_zh": "无障碍数据在设备本地处理，不会发送到服务器，也不会与第三方共享。你可以拒绝并继续在不启用这些功能的情况下使用启动器，也可随时在 Android 无障碍设置中关闭该服务。",
      "source_location": "res/values/strings.xml key=accessibility_disclosure_message / accessibility_service_description",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility: lock and app limits",
      "text_zh": "无障碍：锁屏与应用限额",
      "source_location": "res/values/strings.xml key=accessibility_features（设置页功能项）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "点 No thanks 仅写入 shown_version=2 并关闭弹窗；无 onResume 重跳、无定时器拉起、无后台重启重弹，功能静默降级（双击锁屏/限额不可用，启动器照常使用）；再次进入需用户主动点击设置页功能项（SettingsFragment.onClick → s1.a.M，此时未同意会再弹一次说明）。",
    "overlay_or_fake_settings": "无。未声明 SYSTEM_ALERT_WINDOW，无悬浮窗/半透明遮罩，无高仿系统无障碍开关页；跳转目标为真实系统设置（ACCESSIBILITY_DETAILS_SETTINGS 带 COMPONENT_NAME，失败回退 ACCESSIBILITY_SETTINGS）。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。onAccessibilityEvent 中 performGlobalAction 仅用于“受限应用冷却期回主屏”（对应 app limits 功能），未用于监听设置页并阻止撤权；未发现自点确认、自授权或 WATCH_SETTINGS 式回跳。",
    "benign_graceful_degradation": "有。弹窗明确告知“You can decline and continue using the launcher without these features”，拒绝后桌面启动器、快捷方式、小组件等主体功能不受影响；无障碍能力仅在 accepted_version==2 时启用。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在用户于设置页启用双击锁屏/应用限额后重启应用（或首次启用后返回主界面），监测到 Activity 变为 app.olauncher.MainActivity 且随后出现 Dialog 窗口时拉起 UTG；更精确的信号是监测到 Intent 跳转 android.settings.ACCESSIBILITY_DETAILS_SETTINGS（含 extra COMPONENT_NAME=app.olauncher.helper.MyAccessibilityService）或回退的 android.settings.ACCESSIBILITY_SETTINGS 时，抓取跳转前后窗口栈。",
    "key_pages_to_capture": [
      {
        "page_role": "功能按需触发的原生说明弹窗页",
        "page_identifier": "app.olauncher.MainActivity 上叠加的 AlertDialog，标题文本为 \"Accessibility service\"，按钮为 \"I agree — open settings\" / \"No thanks\"",
        "why_most_useful": "该页是唯一引导入口，直接决定是否属诱导：是否可取消、文案是否如实披露读取范围与数据流向、是否含恐吓/假更新话术，均可在此页一次性判定",
        "observable_utg_signals": ["弹窗存在两个可点击按钮且其中之一为拒绝/取消（No thanks）", "正文包含读取范围声明（foreground app package names / window-change events / clicked view information）与本地处理声明", "标题与系统无障碍列表服务名一致为 BetterLauncher，无第三方品牌"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载的服务中的 BetterLauncher 条目，摘要为 accessibility_service_description 文本",
        "why_most_useful": "核对 android:label 与 android:description 是否与弹窗一致、有无空白挤出/同形字伪装；可验证应用未伪造 isAccessibilityTool 使服务免于系统警示",
        "observable_utg_signals": ["服务名与桌面应用名一致（BetterLauncher）", "描述首句为 \"BetterLauncher uses the Android AccessibilityService API for optional double-tap screen locking and app limits you configure.\"", "未出现空白行/异常字符挤出警告文案"]
      },
      {
        "page_role": "跳转后系统无障碍详情开关页",
        "page_identifier": "android.settings.ACCESSIBILITY_DETAILS_SETTINGS 打开的本应用服务开关页",
        "why_most_useful": "验证跳转为真实系统页（含系统标题栏与开关），无压栈遮罩或高仿开关页；并观察获权返回后是否自动重跳/自动开启",
        "observable_utg_signals": ["页面包名为 com.android.settings 而非本应用", "返回应用后未出现二次弹窗或强制重跳", "开关状态仅由用户操作改变"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区。全部引导文案为原生字符串资源与原生 Dialog，无图片引导、无 WebView/HTML、无远端下发。唯一需注意：说明弹窗仅在用户已启用相关功能（prefs v()/d()/W()）后才会出现，未启用功能的设备冷启动不会弹窗，UTG 若仅做冷启动采集会漏检；建议先进入设置页启用“双击锁屏”或“应用限额”再复现。"
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
    "app.olauncher.MainActivity.onCreate",
    "s1.a.N",
    "s1.a.M",
    "u2.a.onClick",
    "app.olauncher.helper.MyAccessibilityService.onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
