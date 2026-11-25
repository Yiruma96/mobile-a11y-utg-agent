# BN_006__d9933fc2de｜专注自律与防沉迷管控 — Zenwell

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：175.1s

## 1. 一句话核心结论

- **核心申请方式**：开源防沉迷应用 Zenwell 在 Compose 主界面用真实品牌与明确用途文案提示“需要无障碍权限以识别前台应用并锁定”，用户点击后一次 Intent 直跳系统 ACCESSIBILITY_SETTINGS，无遮罩、无强制、无回跳循环，服务仅用于窗口事件阻断被列入日程的应用。
- **静态可见性说明**：全部关键逻辑静态可见：classes.dex 未加壳（加壳初判 False），引导文案在 res/values/strings.xml（含多语言），无障碍服务配置在 res/xml/app_blocker_service_config.xml，跳转点在 z1#a() 硬编码 Intent 字符串；UI 为 Jetpack Compose 原生实现（MainActivity 单 Activity + ComposeView），无 WebView/远端 HTML/密文二阶段载荷。仅 Compose 组件的具体可组合函数名受 R8 混淆（k11.j 等），不影响流程与文案判定。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d9933fc2de7f0e9d9aceec44c1e04a066fff43d54a7f3bcd33602a8fafd43242` |
| 包名 / 年份 | `com.sarangem.zenwell` / 2025-2026 |
| 家族 / 品类 | **专注自律与防沉迷管控**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.sarangem.zenwell_17.apk |
| 桌面显示名 | Zenwell |
| 引导页宣称品牌/身份 | Zenwell（真实名称，F-Droid 开源防沉迷/专注自律工具） |
| 系统无障碍列表服务名 | Zenwell（服务未声明 android:label，系统无障碍列表沿用应用名；描述为 app_locker_service_description） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未发现空白/换行挤出警告、同形字、多 activity-alias 伪装或伪造 isAccessibilityTool；仅存在模板残留 android:settingsActivity="com.example.android.accessibility.ServiceSettingsActivity"（该类不存在，属开发遗留，非伪装） |
| 无障碍服务类名 | `com.sarangem.zenwell.service.AppLockerService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Zenwell uses this service to know which app you are using and locks that app to cure your addiction. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sarangem.zenwell.MainActivity（单 Activity，setContentView 为 ComposeView，内容 lambda k11.j） | Launcher 图标冷启动 → onCreate(Bundle) → setContent(k11.j) | 原生Activity | **原文**：Zenwell；home_screen_description: "Create schedules to lock distracting apps. Tap '+' to begin."<br>**译注**：Zenwell 首页；提示“创建日程以锁定让人分心的应用，点击 + 开始” | 浏览首页、创建日程（此时尚未强制要求权限） | `com.sarangem.zenwell.MainActivity.onCreate / res/values/strings.xml#home_screen_description` |
| 2 | 引导说明页 | MainActivity 内 Compose 权限引导卡片/提示区（权限未授予时展示） | Compose 组合阶段读取无障碍与使用情况访问状态后渲染提示文案 | 原生Activity | **原文**：Let’s unlock your focus goals! Zenwell needs <b>Accessibility permission</b> to see which apps are open so it can keep your screen time in check. / Enable permissions to unlock your focus / Grant permission / Enable all<br>**译注**：“来解锁你的专注目标吧！Zenwell 需要无障碍权限来查看当前打开了哪些应用，以便帮你控制屏幕使用时间。”按钮为“授予权限”“全部启用” | 点击“Grant permission”（授予权限）按钮；界面为普通页面，用户可直接返回或忽略 | `res/values/strings.xml#accessibility_service_permission / #grant_permission / #enable_all` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装的服务列表（android.settings.ACCESSIBILITY_SETTINGS） | 用户点击授权按钮 → 协程/回调执行 z1#a() case 0 → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Zenwell uses this service to know which app you are using and locks that app to cure your addiction.<br>**译注**：系统无障碍列表中本服务描述：“Zenwell 使用此服务了解你正在使用哪个应用，并锁定该应用以戒除成瘾。” | 在系统页手动找到 Zenwell 并打开开关；无应用侧遮罩、无悬浮指引窗覆盖系统页 | `z1#a（case 0）/ res/xml/app_blocker_service_config.xml / strings.xml#app_locker_service_description` |
| 4 | 跳受限设置 | 系统设置 → 使用情况访问权限（android.settings.USAGE_ACCESS_SETTINGS） | 同 z1#a() 的 default 分支，用于 PACKAGE_USAGE_STATS 授权引导 | 系统无障碍页 | **原文**：<b>Usage Statistics Access</b> for Zenwell not enabled. It is required to monitor your app usage and display motivational statistics.<br>**译注**：“Zenwell 的使用情况统计访问权限未开启，该权限用于监测应用使用情况并展示激励统计。” | 在系统使用情况访问列表中授予 Zenwell 权限；有取消/返回路径 | `z1#a（default 分支）/ xo2#e（AppOps "android:get_usage_stats" 校验）/ strings.xml` |
| 5 | 获权后动作 | com.sarangem.zenwell.service.AppLockerService（无障碍服务实例） | 系统绑定服务 → onServiceConnected() → 启动协程加载日程并 setServiceInfo(eventTypes) → onAccessibilityEvent 收到 typeWindowStateChanged(0x20)/内容变化(0x800) | 原生Activity | **原文**：app_lock_notification_message: %1$s would soon lock %2$s / app_lock_notification_description: Send a notification before locking the app again.<br>**译注**：“%1$s 即将锁定 %2$s”——锁定前发送通知提醒，并可将被拦截应用退回 | 无额外操作；服务仅按用户配置的日程阻断被列入名单的应用 | `com.sarangem.zenwell.service.AppLockerService.onServiceConnected / onAccessibilityEvent / a()` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity（Compose 原生界面）内的权限引导卡片/提示文本，资源 res/values/strings.xml#accessibility_service_permission（含 <b> 加粗强调，由 Compose 富文本渲染，非 HTML 页面）
- 引导卡片按钮文案 res/values/strings.xml#grant_permission（Grant permission）与 #enable_all（Enable all）
- 使用情况访问提示文案（Usage Statistics Access ... required to monitor your app usage）呈现于 MainActivity 的权限提示区
- 系统无障碍服务列表项描述 android:description=@string/app_locker_service_description（res/xml/app_blocker_service_config.xml）
- 系统使用情况访问列表中的应用条目（跳转后由系统渲染，应用不覆盖）
- 锁定时的通知栏提示 res/values/strings.xml#app_lock_notification_message（应用功能提示，非权限引导）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Let’s unlock your focus goals! Zenwell needs <b>Accessibility permission</b> to see which apps are open so it can keep your screen time in check. | 来解锁你的专注目标吧！Zenwell 需要无障碍权限来查看当前打开了哪些应用，以便帮你控制屏幕使用时间。 | `res/values/strings.xml#accessibility_service_permission` | 良性透明说明 |
| en | Zenwell uses this service to know which app you are using and locks that app to cure your addiction. | Zenwell 使用此服务了解你正在使用哪个应用，并锁定该应用以帮助你戒除成瘾。 | `res/values/strings.xml#app_locker_service_description（被 res/xml/app_blocker_service_config.xml 的 android:description 引用）` | 良性透明说明 |
| en | <b>Usage Statistics Access</b> for Zenwell not enabled. It is required to monitor your app usage and display motivational statistics. | Zenwell 的使用情况统计访问权限未开启。该权限用于监测应用使用情况并展示激励性统计。 | `res/values/strings.xml（Usage Statistics 相关字符串，MainActivity 权限提示区）` | 良性透明说明 |
| en | Grant permission / Enable permissions to unlock your focus / Enable all | 授予权限 / 启用权限以解锁你的专注 / 全部启用 | `res/values/strings.xml#grant_permission、#enable_all` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：未见强制循环：MainActivity 未覆写 onResume 做强制重跳，也未注册无障碍状态监听来反复拉起设置页；用户从系统设置返回后停留在首页，权限提示仍然保留，可再次手动点击或直接使用其它功能（良性安全降级，不做拦截）
- **遮罩叠层 / 高仿系统设置页**：无。应用未申请悬浮窗权限，无全屏遮罩、无高仿系统无障碍开关页，跳转后系统页由系统自身渲染
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、未发现“点右上角菜单允许受限设置”类文案或 Session 安装器绕过
- **获权后即时行为与防撤权机制**：无。未见自点确认、自授权或监听设置页使用 GLOBAL_ACTION_BACK/HOME 阻止撤权；PERFORM_GLOBAL_ACTION 仅用于把被锁应用退回（阻断功能本身）
- **良性降级 / 替代方案**：权限未授予时应用仍可正常进入首页与创建日程，仅提示权限缺失（如“Usage Statistics Access for Zenwell not enabled”为提示性文案），未阻断使用、未以假故障逼迫授权

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监控应用进程发起 startActivity 且 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（来源 z1#a case 0）或 android.settings.USAGE_ACCESS_SETTINGS（default 分支）的瞬间；同时可在 MainActivity 冷启动后首帧渲染时抓取权限引导卡片页
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：文案均为纯文本资源（无纯图空文本诱导），无远端 HTML 一阶段 Dropper，静态未加壳故运行期 UTG 可完整对照。唯一注意点为 Compose 语义树中加粗文本可能被拆分为多段 Span，UTG 文本提取需拼接同一节点内的多个 Text 段。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后应用内无障碍引导卡片页** | com.sarangem.zenwell.MainActivity + 含“Accessibility permission”“Grant permission”文本的 Compose 卡片 | 区分“良性透明说明”与“故障恐吓/假安全”话术的唯一应用侧话术载体，且可判断是否可取消 | 文案是否说明真实用途（识别前台应用/屏幕时间）；是否存在取消/跳过入口；是否存在伪造系统 UI 或警告遮挡元素 |
| **跳转瞬间的系统无障碍服务列表项** | 系统 Settings 无障碍页中 com.sarangem.zenwell 条目（描述：Zenwell uses this service to know which app you are using...） | 核验服务名与描述是否与实际品牌一致、是否被空白/换行挤出警告或同形字伪装 | 服务标题是否等于应用名 Zenwell；描述文本是否与代码资源一致；是否存在多个可疑同名服务项 |
| **返回应用后的状态页（拒权/已授权对照）** | MainActivity 在从设置页返回后重新渲染的首页/权限卡片 | 验证是否存在拒权后死循环重跳设置页、或未授权即被阻断使用的强制行为 | 是否自动再次跳转设置页；是否出现不可关闭弹窗/遮罩；首页功能是否仍可访问（降级） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `z1#a（case 0 → android.settings.ACCESSIBILITY_SETTINGS；default → android.settings.USAGE_ACCESS_SETTINGS）`
- `com.sarangem.zenwell.MainActivity.onCreate（ComposeView 挂载 k11.j 内容，单 Activity 引导载体）`
- `com.sarangem.zenwell.service.AppLockerService.onAccessibilityEvent / onServiceConnected / a（窗口事件处理与 eventTypes 动态收缩）`
- `res/xml/app_blocker_service_config.xml（typeWindowStateChanged、canRetrieveWindowContent、flagRetrieveInteractiveWindows、description 引用）`
- `res/values/strings.xml#accessibility_service_permission / #app_locker_service_description / #grant_permission`
- `xo2#e（AppOps "android:get_usage_stats" 授权状态校验）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **无障碍申请方式属于良性、透明且单步的流程**：`MainActivity`（唯一的 Activity，Jetpack Compose 原生界面）中显示引导卡片和文案，用户点击后直接调用 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 跳转到系统无障碍列表；没有 WebView、悬浮窗遮罩或伪造的设置页。
- **跳转点集中在同一处**：`z1#a()` 使用 switch 分发四个动作，其中 `case 0` 跳转到无障碍设置，`default` 跳转到 `android.settings.USAGE_ACCESS_SETTINGS`；整个应用中没有发现 `ACTION_APPLICATION_DETAILS_SETTINGS`，也没有“受限设置”分步教学，`Session` 或安装器绕过都不存在。
- **文案来自资源文件，说明真实用途**：`accessibility_service_permission` 明确说明“需要无障碍权限查看当前打开的应用以控制屏幕时间”；服务描述 `app_locker_service_description` 同样明确写出真实用途。无障碍列表中显示的服务名沿用应用名 `Zenwell`，没有进行身份伪装。
- **服务本体行为与声明的用途一致**：`AppLockerService.onAccessibilityEvent` 只处理窗口状态和内容变化事件，并以 2000 毫秒进行节流，随后交由 `ab2.r` 解析前台应用，再依据日程锁定目标应用；`a()` 会按日程动态收缩 `eventTypes`（从 2080 收缩到 32），因此它既不会监听键盘或密码，也不会收集文本。
- **无强制、无回跳循环、无防撤权**：`MainActivity` 没有覆写 `onResume` 来强制重新拉起引导页；没有发现监听设置页并使用 `GLOBAL_ACTION_BACK/HOME` 阻止撤权；预筛得到的 `PERFORM_GLOBAL_ACTION` 属于“把被拦截应用退回桌面”的阻断功能实现，不是阻止用户撤权。
- **一处轻微瑕疵（非风险）**：`app_blocker_service_config.xml` 残留了模板占位 `android:settingsActivity="com.example.android.accessibility.ServiceSettingsActivity"`，而该类不存在于应用内。用户在系统无障碍列表中点击“设置”图标时可能无响应，但这不影响权限申请流程。
- 未发现恶意诱导特征，因此没有登记风险；静态可见性为 `clear`（没有加壳、没有密文载荷、没有动态加载）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键逻辑静态可见：classes.dex 未加壳（加壳初判 False），引导文案在 res/values/strings.xml（含多语言），无障碍服务配置在 res/xml/app_blocker_service_config.xml，跳转点在 z1#a() 硬编码 Intent 字符串；UI 为 Jetpack Compose 原生实现（MainActivity 单 Activity + ComposeView），无 WebView/远端 HTML/密文二阶段载荷。仅 Compose 组件的具体可组合函数名受 R8 混淆（k11.j 等），不影响流程与文案判定。",
  "summary_one_liner": "开源防沉迷应用 Zenwell 在 Compose 主界面用真实品牌与明确用途文案提示“需要无障碍权限以识别前台应用并锁定”，用户点击后一次 Intent 直跳系统 ACCESSIBILITY_SETTINGS，无遮罩、无强制、无回跳循环，服务仅用于窗口事件阻断被列入日程的应用。",
  "disguise_identity": {
    "app_display_name": "Zenwell",
    "claimed_brand_or_persona": "Zenwell（真实名称，F-Droid 开源防沉迷/专注自律工具）",
    "a11y_service_label": "Zenwell（服务未声明 android:label，系统无障碍列表沿用应用名；描述为 app_locker_service_description）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未发现空白/换行挤出警告、同形字、多 activity-alias 伪装或伪造 isAccessibilityTool；仅存在模板残留 android:settingsActivity=\"com.example.android.accessibility.ServiceSettingsActivity\"（该类不存在，属开发遗留，非伪装）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sarangem.zenwell.MainActivity（单 Activity，setContentView 为 ComposeView，内容 lambda k11.j）",
      "trigger_event": "Launcher 图标冷启动 → onCreate(Bundle) → setContent(k11.j)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Zenwell；home_screen_description: \"Create schedules to lock distracting apps. Tap '+' to begin.\"",
      "shown_text_zh": "Zenwell 首页；提示“创建日程以锁定让人分心的应用，点击 + 开始”",
      "user_action_requested": "浏览首页、创建日程（此时尚未强制要求权限）",
      "code_anchor": "com.sarangem.zenwell.MainActivity.onCreate / res/values/strings.xml#home_screen_description"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 内 Compose 权限引导卡片/提示区（权限未授予时展示）",
      "trigger_event": "Compose 组合阶段读取无障碍与使用情况访问状态后渲染提示文案",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Let’s unlock your focus goals! Zenwell needs <b>Accessibility permission</b> to see which apps are open so it can keep your screen time in check. / Enable permissions to unlock your focus / Grant permission / Enable all",
      "shown_text_zh": "“来解锁你的专注目标吧！Zenwell 需要无障碍权限来查看当前打开了哪些应用，以便帮你控制屏幕使用时间。”按钮为“授予权限”“全部启用”",
      "user_action_requested": "点击“Grant permission”（授予权限）按钮；界面为普通页面，用户可直接返回或忽略",
      "code_anchor": "res/values/strings.xml#accessibility_service_permission / #grant_permission / #enable_all"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装的服务列表（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "用户点击授权按钮 → 协程/回调执行 z1#a() case 0 → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Zenwell uses this service to know which app you are using and locks that app to cure your addiction.",
      "shown_text_zh": "系统无障碍列表中本服务描述：“Zenwell 使用此服务了解你正在使用哪个应用，并锁定该应用以戒除成瘾。”",
      "user_action_requested": "在系统页手动找到 Zenwell 并打开开关；无应用侧遮罩、无悬浮指引窗覆盖系统页",
      "code_anchor": "z1#a（case 0）/ res/xml/app_blocker_service_config.xml / strings.xml#app_locker_service_description"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置 → 使用情况访问权限（android.settings.USAGE_ACCESS_SETTINGS）",
      "trigger_event": "同 z1#a() 的 default 分支，用于 PACKAGE_USAGE_STATS 授权引导",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "<b>Usage Statistics Access</b> for Zenwell not enabled. It is required to monitor your app usage and display motivational statistics.",
      "shown_text_zh": "“Zenwell 的使用情况统计访问权限未开启，该权限用于监测应用使用情况并展示激励统计。”",
      "user_action_requested": "在系统使用情况访问列表中授予 Zenwell 权限；有取消/返回路径",
      "code_anchor": "z1#a（default 分支）/ xo2#e（AppOps \"android:get_usage_stats\" 校验）/ strings.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.sarangem.zenwell.service.AppLockerService（无障碍服务实例）",
      "trigger_event": "系统绑定服务 → onServiceConnected() → 启动协程加载日程并 setServiceInfo(eventTypes) → onAccessibilityEvent 收到 typeWindowStateChanged(0x20)/内容变化(0x800)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "app_lock_notification_message: %1$s would soon lock %2$s / app_lock_notification_description: Send a notification before locking the app again.",
      "shown_text_zh": "“%1$s 即将锁定 %2$s”——锁定前发送通知提醒，并可将被拦截应用退回",
      "user_action_requested": "无额外操作；服务仅按用户配置的日程阻断被列入名单的应用",
      "code_anchor": "com.sarangem.zenwell.service.AppLockerService.onServiceConnected / onAccessibilityEvent / a()"
    }
  ],
  "text_presentation_locations": [
    "MainActivity（Compose 原生界面）内的权限引导卡片/提示文本，资源 res/values/strings.xml#accessibility_service_permission（含 <b> 加粗强调，由 Compose 富文本渲染，非 HTML 页面）",
    "引导卡片按钮文案 res/values/strings.xml#grant_permission（Grant permission）与 #enable_all（Enable all）",
    "使用情况访问提示文案（Usage Statistics Access ... required to monitor your app usage）呈现于 MainActivity 的权限提示区",
    "系统无障碍服务列表项描述 android:description=@string/app_locker_service_description（res/xml/app_blocker_service_config.xml）",
    "系统使用情况访问列表中的应用条目（跳转后由系统渲染，应用不覆盖）",
    "锁定时的通知栏提示 res/values/strings.xml#app_lock_notification_message（应用功能提示，非权限引导）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Let’s unlock your focus goals! Zenwell needs <b>Accessibility permission</b> to see which apps are open so it can keep your screen time in check.",
      "text_zh": "来解锁你的专注目标吧！Zenwell 需要无障碍权限来查看当前打开了哪些应用，以便帮你控制屏幕使用时间。",
      "source_location": "res/values/strings.xml#accessibility_service_permission",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Zenwell uses this service to know which app you are using and locks that app to cure your addiction.",
      "text_zh": "Zenwell 使用此服务了解你正在使用哪个应用，并锁定该应用以帮助你戒除成瘾。",
      "source_location": "res/values/strings.xml#app_locker_service_description（被 res/xml/app_blocker_service_config.xml 的 android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "<b>Usage Statistics Access</b> for Zenwell not enabled. It is required to monitor your app usage and display motivational statistics.",
      "text_zh": "Zenwell 的使用情况统计访问权限未开启。该权限用于监测应用使用情况并展示激励性统计。",
      "source_location": "res/values/strings.xml（Usage Statistics 相关字符串，MainActivity 权限提示区）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant permission / Enable permissions to unlock your focus / Enable all",
      "text_zh": "授予权限 / 启用权限以解锁你的专注 / 全部启用",
      "source_location": "res/values/strings.xml#grant_permission、#enable_all",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "未见强制循环：MainActivity 未覆写 onResume 做强制重跳，也未注册无障碍状态监听来反复拉起设置页；用户从系统设置返回后停留在首页，权限提示仍然保留，可再次手动点击或直接使用其它功能（良性安全降级，不做拦截）",
    "overlay_or_fake_settings": "无。应用未申请悬浮窗权限，无全屏遮罩、无高仿系统无障碍开关页，跳转后系统页由系统自身渲染",
    "restricted_settings_13plus_coaching": "无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、未发现“点右上角菜单允许受限设置”类文案或 Session 安装器绕过",
    "post_grant_anti_removal": "无。未见自点确认、自授权或监听设置页使用 GLOBAL_ACTION_BACK/HOME 阻止撤权；PERFORM_GLOBAL_ACTION 仅用于把被锁应用退回（阻断功能本身）",
    "benign_graceful_degradation": "权限未授予时应用仍可正常进入首页与创建日程，仅提示权限缺失（如“Usage Statistics Access for Zenwell not enabled”为提示性文案），未阻断使用、未以假故障逼迫授权"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监控应用进程发起 startActivity 且 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（来源 z1#a case 0）或 android.settings.USAGE_ACCESS_SETTINGS（default 分支）的瞬间；同时可在 MainActivity 冷启动后首帧渲染时抓取权限引导卡片页",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后应用内无障碍引导卡片页",
        "page_identifier": "com.sarangem.zenwell.MainActivity + 含“Accessibility permission”“Grant permission”文本的 Compose 卡片",
        "why_most_useful": "区分“良性透明说明”与“故障恐吓/假安全”话术的唯一应用侧话术载体，且可判断是否可取消",
        "observable_utg_signals": ["文案是否说明真实用途（识别前台应用/屏幕时间）", "是否存在取消/跳过入口", "是否存在伪造系统 UI 或警告遮挡元素"]
      },
      {
        "page_role": "跳转瞬间的系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页中 com.sarangem.zenwell 条目（描述：Zenwell uses this service to know which app you are using...）",
        "why_most_useful": "核验服务名与描述是否与实际品牌一致、是否被空白/换行挤出警告或同形字伪装",
        "observable_utg_signals": ["服务标题是否等于应用名 Zenwell", "描述文本是否与代码资源一致", "是否存在多个可疑同名服务项"]
      },
      {
        "page_role": "返回应用后的状态页（拒权/已授权对照）",
        "page_identifier": "MainActivity 在从设置页返回后重新渲染的首页/权限卡片",
        "why_most_useful": "验证是否存在拒权后死循环重跳设置页、或未授权即被阻断使用的强制行为",
        "observable_utg_signals": ["是否自动再次跳转设置页", "是否出现不可关闭弹窗/遮罩", "首页功能是否仍可访问（降级）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：文案均为纯文本资源（无纯图空文本诱导），无远端 HTML 一阶段 Dropper，静态未加壳故运行期 UTG 可完整对照。唯一注意点为 Compose 语义树中加粗文本可能被拆分为多段 Span，UTG 文本提取需拼接同一节点内的多个 Text 段。"
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
    "z1#a（case 0 → android.settings.ACCESSIBILITY_SETTINGS；default → android.settings.USAGE_ACCESS_SETTINGS）",
    "com.sarangem.zenwell.MainActivity.onCreate（ComposeView 挂载 k11.j 内容，单 Activity 引导载体）",
    "com.sarangem.zenwell.service.AppLockerService.onAccessibilityEvent / onServiceConnected / a（窗口事件处理与 eventTypes 动态收缩）",
    "res/xml/app_blocker_service_config.xml（typeWindowStateChanged、canRetrieveWindowContent、flagRetrieveInteractiveWindows、description 引用）",
    "res/values/strings.xml#accessibility_service_permission / #app_locker_service_description / #grant_permission",
    "xo2#e（AppOps \"android:get_usage_stats\" 授权状态校验）"
  ]
}
```

**覆盖边界**：受 8–14 次调用约束，未逐一反编译 Compose 权限卡片的具体可组合函数（`k11.j` 内部），因此“拒权后界面停留/可取消”的结论基于 `MainActivity` 无 `onResume` 覆写、无无障碍状态监听与无悬浮窗权限的静态事实推断，未做运行期 UTG 实证；如需闭环可在真机上按上述 hook 点抓取三页对照。

</details>
