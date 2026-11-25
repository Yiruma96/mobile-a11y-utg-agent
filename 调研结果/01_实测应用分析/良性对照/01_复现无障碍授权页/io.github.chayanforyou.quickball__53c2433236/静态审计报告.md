# BN_013__53c2433236｜按键映射与手势导航 — Quick Ball

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：236.5s

## 1. 一句话核心结论

- **核心申请方式**：首次启动由 Compose 引导向导（Meet Quick Ball → Permissions）透明说明无障碍用途，用户点击 Accessibility 行/Open Accessibility settings 后以 fragment_args_key 精准跳转系统无障碍列表开启服务，失败仅 Toast 提示、无遮罩无死循环、无伪系统页。
- **静态可见性说明**：无障碍申请链路完全静态可见：Manifest 单 Activity + 单 AccessibilityService，跳转实现位于 k3.a.F（明文 android.settings.ACCESSIBILITY_SETTINGS），无 WebView/远端 HTML、无加密载荷、无加壳（apkid 初判 False，DEX 可直接反编译出完整方法体）。仅 Compose UI 的组件层级被 R8 重命名为 j4/m4/l4 匿名 lambda，文案与按钮的绑定关系由 strings.xml key 与 l4.f.a 分支号推断。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `53c24332369940b68b6d51d03f52e2d0588cd27cffc933b1eb19a1ce853308e5` |
| 包名 / 年份 | `io.github.chayanforyou.quickball` / 2025-2026 |
| 家族 / 品类 | **按键映射与手势导航**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/io.github.chayanforyou.quickball_26.apk |
| 桌面显示名 | Quick Ball |
| 引导页宣称品牌/身份 | Quick Ball（F-Droid 开源项目，引导页含跳转 github.com/chayanforyou/QuickBall 源码仓库入口） |
| 系统无障碍列表服务名 | Quick Ball（服务未设 android:label，继承 application android:label=@string/app_name；系统列表描述为 "QuickBall floating ball service that provides a floating ball overlay on your screen for quick access to features."） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。无 activity-alias、无空白/换行挤出、无同形字、无 isAccessibilityTool 伪造、无伪造系统设置页。 |
| 无障碍服务类名 | `io.github.chayanforyou.quickball.core.QuickBallService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | QuickBall floating ball service that provides a floating ball overlay on your screen for quick access to features. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | io.github.chayanforyou.quickball.ui.MainActivity（Compose 内容，R8 后内容体为 g.b） | LAUNCHER 启动 → MainActivity.onCreate → setContentView(c1, ComposeView) | 原生Activity | **原文**：Meet Quick Ball / A floating button that puts one-handed navigation and quick actions anywhere on your screen. It never reads screen content, and nothing leaves your device. / Get started<br>**译注**：认识 Quick Ball / 一颗悬浮按钮，在屏幕任意位置提供单手导航与快捷操作。它从不读取屏幕内容，任何数据都不会离开你的设备。/ 开始使用 | 点击 Get started 进入权限说明页；可用系统返回键离开（非强制不可取消） | `io.github.chayanforyou.quickball.ui.MainActivity#onCreate；res/values/strings.xml: onboarding_title / onboarding_subtitle / onboarding_get_started` |
| 2 | 引导说明页 | MainActivity 内 Compose Permissions 页（Accessibility + Modify System Settings 两项卡片） | onboarding 向导翻页（含 onboarding_back 返回上一步） | 原生Activity | **原文**：Permissions / Quick Ball needs just these two to run. Anything else is asked for only when you turn on a feature that needs it. / Quick Ball needs Accessibility and System Settings permissions to work properly. / Accessibility / Powers the floating button and lets Quick Ball perform navigation actions like Home, Back and Recents. It never reads screen content. / Modify System Settings / Lets Quick Ball adjust system settings like screen brightness and volume directly from the floating menu. / Grant / Granted<br>**译注**：权限 / Quick Ball 仅需这两项即可运行，其它权限只在你开启需要它的功能时才会申请。/ Quick Ball 需要无障碍与修改系统设置权限才能正常工作。/ 无障碍 / 用于驱动悬浮按钮，并让 Quick Ball 执行 Home、返回、最近任务等导航动作。它从不读取屏幕内容。/ 修改系统设置 / 让 Quick Ball 直接从悬浮菜单调节屏幕亮度与音量。/ 授予 / 已授予 | 点击 Accessibility 行的 Grant（或 Granted 状态显示）触发跳转；亦可点 Back 回上一步 | `res/values/strings.xml: onboarding_permissions_title / onboarding_permissions_subtitle / onboarding_permissions_warning / onboarding_accessibility_title / onboarding_accessibility_description / onboarding_system_settings_description / permission_grant` |
| 3 | 跳无障碍设置 | 系统设置：设置 → 无障碍 → 已安装服务（精准定位 QuickBallService 条目） | 用户点击 Accessibility 项/“Open Accessibility settings” → 点击回调 l4.f.a(case 0) → k3.a.F(context) | 系统无障碍页 | **原文**：Open Accessibility settings / Quick Ball needs Accessibility access to show the floating button and perform navigation actions. / Could not open accessibility settings（跳转失败 Toast）<br>**译注**：打开无障碍设置 / Quick Ball 需要无障碍权限以显示悬浮按钮并执行导航动作。/ 无法打开无障碍设置（异常兜底 Toast） | 在系统无障碍列表中手动找到并开启 Quick Ball 服务；可随时返回不开启 | `k3.a#F（Intent "android.settings.ACCESSIBILITY_SETTINGS" + putExtra ":settings:fragment_args_key" + FLAG_ACTIVITY_NEW_TASK）；strings.xml: open_accessibility_settings / accessibility_setup_description` |
| 4 | 获权后动作 | io.github.chayanforyou.quickball.core.QuickBallService（悬浮球 WindowManager Overlay） | 系统回调 AccessibilityService.onServiceConnected → 初始化 WindowManager、悬浮球与边把手布局、注册 SCREEN_ON/SCREEN_OFF/USER_PRESENT 广播 | 悬浮窗Overlay | **原文**：Start using Quick Ball / Turn on Quick Ball / Enable gestures<br>**译注**：开始使用 Quick Ball / 开启 Quick Ball / 启用手势 | 返回应用后点击 Start using Quick Ball / Turn on Quick Ball 开关启用悬浮球与手势（功能由用户自主开启） | `io.github.chayanforyou.quickball.core.QuickBallService#onServiceConnected；strings.xml: onboarding_start_using / turn_on_quick_ball / enable_quick_ball` |
| 5 | 业务功能触发 | 厂商电池优化白名单/自启动管理页（华为、小米、OPPO、vivo、三星等）或本应用详情页 | 用户点击“保持后台运行/电池优化”相关入口 → l4.f.a(case 2/case 3) 按 Build.BRAND 选择目标组件；找不到时回退 android.settings.APPLICATION_DETAILS_SETTINGS(package:本包) | 原生Activity | **原文**：无（使用系统厂商页面，无自有文案）<br>**译注**：按机型引导到系统电池优化/自启动白名单页面，保证悬浮球后台存活 | 在系统页允许后台运行；可拒绝，应用不阻断使用 | `l4.f#a（case 2 / case 3，d4.a / d4.b 厂商分支；回退 Intent "android.settings.APPLICATION_DETAILS_SETTINGS"）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内 Compose 引导向导（onboarding_title/subtitle/bullets/get_started，R8 后渲染于 g.b 内容体）——首次启动页面正文
- MainActivity 内 Compose Permissions 页卡片（onboarding_accessibility_title/description、onboarding_system_settings_description、permission_grant/permission_granted）——无障碍申请说明与授权按钮
- 系统无障碍服务列表条目描述：android:description=@string/accessibility_service_description（res/xml/accessibility_service_config.xml 引用）
- 系统设置跳转前的界面文案：open_accessibility_settings（"Open Accessibility settings"）与 accessibility_setup_description
- 跳转失败时 Toast：k3.a.F 内硬编码 "Could not open accessibility settings"
- 设置页内功能开关文案：turn_on_quick_ball / enable_quick_ball / gesture_requirement_notice（悬浮球与手势说明）
- 无 WebView 页面、无 HTML 资源、无悬浮遮罩引导层（全包无 loadUrl/javascriptEnabled 命中）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | A floating button that puts one-handed navigation and quick actions anywhere on your screen. It never reads screen content, and nothing leaves your device. | 一颗悬浮按钮，在屏幕任意位置提供单手导航与快捷操作。它从不读取屏幕内容，任何数据都不会离开你的设备。 | `res/values/strings.xml: onboarding_subtitle` | 隐私承诺 |
| en | Powers the floating button and lets Quick Ball perform navigation actions like Home, Back and Recents. It never reads screen content. | 用于驱动悬浮按钮，并让 Quick Ball 执行 Home、返回、最近任务等导航动作。它从不读取屏幕内容。 | `res/values/strings.xml: onboarding_accessibility_description` | 良性透明说明 |
| en | Quick Ball needs just these two to run. Anything else is asked for only when you turn on a feature that needs it. | Quick Ball 仅需这两项权限即可运行，其它权限只在你开启需要它的功能时才会申请。 | `res/values/strings.xml: onboarding_permissions_subtitle` | 良性透明说明 |
| en | QuickBall floating ball service that provides a floating ball overlay on your screen for quick access to features. | QuickBall 悬浮球服务，在你的屏幕上提供悬浮球浮层，以便快速访问各项功能。 | `res/values/strings.xml: accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 呈现于系统无障碍列表）` | 良性透明说明 |
| en | Quick Ball needs Accessibility access to show the floating button and perform navigation actions. | Quick Ball 需要无障碍权限以显示悬浮按钮并执行导航动作。 | `res/values/strings.xml: accessibility_setup_description` | 受限设置分步教学 |
| en | Could not open accessibility settings | 无法打开无障碍设置 | `k3.a#F 内硬编码 Toast 文案` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无死循环。MainActivity 仅重写 onCreate/attachBaseContext，未在 onResume/onWindowFocusChanged 中重跳；k3.a.F 异常时只弹 Toast 并 return；QuickBallService.onAccessibilityEvent 仅处理前台包名变化用于隐藏悬浮球，不含任何设置页监听或反复拉起逻辑。用户拒绝授权时应用停留在自身引导/设置页，功能不可用但不阻断退出。
- **遮罩叠层 / 高仿系统设置页**：无。全包无 TYPE_ACCESSIBILITY_OVERLAY 引导遮罩、无高仿系统无障碍开关页；悬浮球 Overlay 仅在服务真正连接后创建（onServiceConnected）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未检索到任何“应用详情 → 右上角菜单 → 允许受限设置”或 Session 安装器绕过的文案与代码。
- **获权后即时行为与防撤权机制**：无。未发现监听设置页并 performGlobalAction(GLOBAL_ACTION_BACK/HOME) 阻止撤权；performGlobalAction 仅用于悬浮菜单的 Home/Back/Recents(1/2/3) 与音量动作(8/9)，属功能本体。
- **良性降级 / 替代方案**：有。权限说明页逐项标注 Granted/Grant，未授予时仅对应功能不可用；跳转失败降级为 Toast 提示；电池优化/自启动引导找不到厂商页面时回退到本应用详情页，均不阻断应用使用。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Activity 启动 Intent action == "android.settings.ACCESSIBILITY_SETTINGS" 且 extras 含 ":settings:fragment_args_key" 指向 io.github.chayanforyou.quickball/core.QuickBallService 的瞬间；或冷启动后首次出现 MainActivity 的 Compose Permissions 页（Accessibility 卡片 + Grant 按钮）时。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一注意点：引导 UI 由 Compose 渲染且类名被 R8 重命名（j4/m4/l4 匿名 lambda），静态仅能从 strings.xml 与 l4.f.a 分支号对应文案与跳转，页面层级需运行期 UTG 补齐；静态未加壳，不影响运行期捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页（Meet Quick Ball）** | io.github.chayanforyou.quickball.ui.MainActivity，文本含 "Meet Quick Ball" / "Get started" | 判定是否为强制首启阻断式引导，以及首屏是否已把无障碍包装成其他诉求 | 标题 Meet Quick Ball 与说明文案是否与无障碍用途一致；是否存在 Cancel/Skip/关闭控件；是否出现恐吓、更新、清理类字样 |
| **权限说明页（跳转前最后一屏）** | MainActivity 内 Permissions 卡片，文本含 "Accessibility"、"Modify System Settings"、"Grant"/"Granted" | 区分透明说明与话术诱导的最关键一屏：能否看到用途解释与已授权状态、是否有拒绝路径 | Accessibility 行是否附带真实用途描述；Grant/Granted 状态是否由真实系统状态驱动；是否存在“允许受限设置”类分步教学 |
| **系统无障碍服务列表项** | 系统 Settings 无障碍页，条目名 "Quick Ball"，描述 "QuickBall floating ball service that provides a floating ball overlay…" | 核对系统侧展示身份与声明是否与包名/文案一致，验证未被伪造或同名混淆 | 服务名与桌面应用名是否一致；描述文本是否与 strings 资源一致；跳转是否精准定位到该条目（fragment_args_key 生效） |
| **获权后悬浮球叠层** | QuickBallService onServiceConnected 后出现的悬浮球/边把手 Overlay（无引导遮罩） | 确认获权后行为是否仅为本职悬浮球，而非在设置页上压栈遮罩或弹二次授权 | 返回应用后设置页之上是否出现遮罩/浮层；悬浮球是否只在应用内或桌面出现；是否存在自动点击确认 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `k3.a#F`
- `l4.f#a`
- `io.github.chayanforyou.quickball.core.QuickBallService#onServiceConnected`
- `io.github.chayanforyou.quickball.core.QuickBallService#onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（要点）

**总体判断：这是良性、透明地说明需求的无障碍权限申请流程，未发现诱导或强制行为。**

- **权限跳转入口唯一且需用户主动点击**：[k3.a#F](<resource-unit:#1.dex1 code:k3.a#F>) 构造 `Intent("android.settings.ACCESSIBILITY_SETTINGS")`，并携带 `:settings:fragment_args_key` = `io.github.chayanforyou.quickball/…core.QuickBallService`，直接定位到系统无障碍列表中的本服务条目；失败时只弹出 Toast “Could not open accessibility settings”，不会强制重试。
- **调用方为 Compose 点击回调**：`k3.a.F` 只有一个调用者 [l4.f#a](<resource-unit:#1.dex1 code:l4.f#a>)（`switch` case 0）；其余分支分别是 case 1 打开 `https://github.com/chayanforyou/QuickBall`（真实开源仓库，身份透明），以及 case 2、case 3 按厂商品牌跳转电池优化白名单或自启动管理页（`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 的常规配套引导）。
- **无 WebView、无远端内容**：整个 DEX 中 `loadUrl` 和 `javascriptEnabled` 都没有命中，唯一的 “WebView” 字面量出现在服务的前台包名白名单里。不存在本地或远端 HTML 教学页，也没有伪造的系统设置界面或叠层遮罩。
- **无障碍声明最小化**：[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 只声明 `typeWindowStateChanged|typeWindowsChanged` 和 `flagDefault`，**未声明 `canRetrieveWindowContent`**；`onAccessibilityEvent` 仅取 `getPackageName()` 用于“在选定应用中隐藏悬浮球”，与描述一致。
- **无规避检测的手法**：没有 `activity-alias`、没有 `isAccessibilityTool` 伪造、没有同形字或换行挤出；`app_name`=“Quick Ball”，服务描述为 “QuickBall floating ball service that provides a floating ball overlay on your screen for quick access to features.”
- **没有拒绝授权后的反复跳转**：`MainActivity` 只重写了 `onCreate` 和 `attachBaseContext`，没有 `onResume` 重新拉起设置页；服务侧没有 `WATCH_SETTINGS` 式撤权对抗逻辑，`performGlobalAction` 只用于 Home、Back、Recents 与音量动作。
- **隐私承诺真实可核**：`onboarding_subtitle` 明确写 “It never reads screen content, and nothing leaves your device.”，代码侧确实无窗口内容读取、无网络上报（无 INTERNET 相关外发实现命中）。

**覆盖边界**：Compose 的 UI 结构经 R8 混淆为 `j4/m4/l4` 匿名 lambda，页面层级与按钮文案的精确对应关系由 `strings.xml` key 与 `l4.f.a` 分支推断；未做运行期 UTG 复核（本轮为静态定向审计）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请链路完全静态可见：Manifest 单 Activity + 单 AccessibilityService，跳转实现位于 k3.a.F（明文 android.settings.ACCESSIBILITY_SETTINGS），无 WebView/远端 HTML、无加密载荷、无加壳（apkid 初判 False，DEX 可直接反编译出完整方法体）。仅 Compose UI 的组件层级被 R8 重命名为 j4/m4/l4 匿名 lambda，文案与按钮的绑定关系由 strings.xml key 与 l4.f.a 分支号推断。",
  "summary_one_liner": "首次启动由 Compose 引导向导（Meet Quick Ball → Permissions）透明说明无障碍用途，用户点击 Accessibility 行/Open Accessibility settings 后以 fragment_args_key 精准跳转系统无障碍列表开启服务，失败仅 Toast 提示、无遮罩无死循环、无伪系统页。",
  "disguise_identity": {
    "app_display_name": "Quick Ball",
    "claimed_brand_or_persona": "Quick Ball（F-Droid 开源项目，引导页含跳转 github.com/chayanforyou/QuickBall 源码仓库入口）",
    "a11y_service_label": "Quick Ball（服务未设 android:label，继承 application android:label=@string/app_name；系统列表描述为 \"QuickBall floating ball service that provides a floating ball overlay on your screen for quick access to features.\"）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。无 activity-alias、无空白/换行挤出、无同形字、无 isAccessibilityTool 伪造、无伪造系统设置页。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "io.github.chayanforyou.quickball.ui.MainActivity（Compose 内容，R8 后内容体为 g.b）",
      "trigger_event": "LAUNCHER 启动 → MainActivity.onCreate → setContentView(c1, ComposeView)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Meet Quick Ball / A floating button that puts one-handed navigation and quick actions anywhere on your screen. It never reads screen content, and nothing leaves your device. / Get started",
      "shown_text_zh": "认识 Quick Ball / 一颗悬浮按钮，在屏幕任意位置提供单手导航与快捷操作。它从不读取屏幕内容，任何数据都不会离开你的设备。/ 开始使用",
      "user_action_requested": "点击 Get started 进入权限说明页；可用系统返回键离开（非强制不可取消）",
      "code_anchor": "io.github.chayanforyou.quickball.ui.MainActivity#onCreate；res/values/strings.xml: onboarding_title / onboarding_subtitle / onboarding_get_started"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 内 Compose Permissions 页（Accessibility + Modify System Settings 两项卡片）",
      "trigger_event": "onboarding 向导翻页（含 onboarding_back 返回上一步）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Permissions / Quick Ball needs just these two to run. Anything else is asked for only when you turn on a feature that needs it. / Quick Ball needs Accessibility and System Settings permissions to work properly. / Accessibility / Powers the floating button and lets Quick Ball perform navigation actions like Home, Back and Recents. It never reads screen content. / Modify System Settings / Lets Quick Ball adjust system settings like screen brightness and volume directly from the floating menu. / Grant / Granted",
      "shown_text_zh": "权限 / Quick Ball 仅需这两项即可运行，其它权限只在你开启需要它的功能时才会申请。/ Quick Ball 需要无障碍与修改系统设置权限才能正常工作。/ 无障碍 / 用于驱动悬浮按钮，并让 Quick Ball 执行 Home、返回、最近任务等导航动作。它从不读取屏幕内容。/ 修改系统设置 / 让 Quick Ball 直接从悬浮菜单调节屏幕亮度与音量。/ 授予 / 已授予",
      "user_action_requested": "点击 Accessibility 行的 Grant（或 Granted 状态显示）触发跳转；亦可点 Back 回上一步",
      "code_anchor": "res/values/strings.xml: onboarding_permissions_title / onboarding_permissions_subtitle / onboarding_permissions_warning / onboarding_accessibility_title / onboarding_accessibility_description / onboarding_system_settings_description / permission_grant"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置：设置 → 无障碍 → 已安装服务（精准定位 QuickBallService 条目）",
      "trigger_event": "用户点击 Accessibility 项/“Open Accessibility settings” → 点击回调 l4.f.a(case 0) → k3.a.F(context)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Open Accessibility settings / Quick Ball needs Accessibility access to show the floating button and perform navigation actions. / Could not open accessibility settings（跳转失败 Toast）",
      "shown_text_zh": "打开无障碍设置 / Quick Ball 需要无障碍权限以显示悬浮按钮并执行导航动作。/ 无法打开无障碍设置（异常兜底 Toast）",
      "user_action_requested": "在系统无障碍列表中手动找到并开启 Quick Ball 服务；可随时返回不开启",
      "code_anchor": "k3.a#F（Intent \"android.settings.ACCESSIBILITY_SETTINGS\" + putExtra \":settings:fragment_args_key\" + FLAG_ACTIVITY_NEW_TASK）；strings.xml: open_accessibility_settings / accessibility_setup_description"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "io.github.chayanforyou.quickball.core.QuickBallService（悬浮球 WindowManager Overlay）",
      "trigger_event": "系统回调 AccessibilityService.onServiceConnected → 初始化 WindowManager、悬浮球与边把手布局、注册 SCREEN_ON/SCREEN_OFF/USER_PRESENT 广播",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Start using Quick Ball / Turn on Quick Ball / Enable gestures",
      "shown_text_zh": "开始使用 Quick Ball / 开启 Quick Ball / 启用手势",
      "user_action_requested": "返回应用后点击 Start using Quick Ball / Turn on Quick Ball 开关启用悬浮球与手势（功能由用户自主开启）",
      "code_anchor": "io.github.chayanforyou.quickball.core.QuickBallService#onServiceConnected；strings.xml: onboarding_start_using / turn_on_quick_ball / enable_quick_ball"
    },
    {
      "step": 5,
      "stage": "业务功能触发",
      "screen_or_component": "厂商电池优化白名单/自启动管理页（华为、小米、OPPO、vivo、三星等）或本应用详情页",
      "trigger_event": "用户点击“保持后台运行/电池优化”相关入口 → l4.f.a(case 2/case 3) 按 Build.BRAND 选择目标组件；找不到时回退 android.settings.APPLICATION_DETAILS_SETTINGS(package:本包)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（使用系统厂商页面，无自有文案）",
      "shown_text_zh": "按机型引导到系统电池优化/自启动白名单页面，保证悬浮球后台存活",
      "user_action_requested": "在系统页允许后台运行；可拒绝，应用不阻断使用",
      "code_anchor": "l4.f#a（case 2 / case 3，d4.a / d4.b 厂商分支；回退 Intent \"android.settings.APPLICATION_DETAILS_SETTINGS\"）"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内 Compose 引导向导（onboarding_title/subtitle/bullets/get_started，R8 后渲染于 g.b 内容体）——首次启动页面正文",
    "MainActivity 内 Compose Permissions 页卡片（onboarding_accessibility_title/description、onboarding_system_settings_description、permission_grant/permission_granted）——无障碍申请说明与授权按钮",
    "系统无障碍服务列表条目描述：android:description=@string/accessibility_service_description（res/xml/accessibility_service_config.xml 引用）",
    "系统设置跳转前的界面文案：open_accessibility_settings（\"Open Accessibility settings\"）与 accessibility_setup_description",
    "跳转失败时 Toast：k3.a.F 内硬编码 \"Could not open accessibility settings\"",
    "设置页内功能开关文案：turn_on_quick_ball / enable_quick_ball / gesture_requirement_notice（悬浮球与手势说明）",
    "无 WebView 页面、无 HTML 资源、无悬浮遮罩引导层（全包无 loadUrl/javascriptEnabled 命中）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "A floating button that puts one-handed navigation and quick actions anywhere on your screen. It never reads screen content, and nothing leaves your device.",
      "text_zh": "一颗悬浮按钮，在屏幕任意位置提供单手导航与快捷操作。它从不读取屏幕内容，任何数据都不会离开你的设备。",
      "source_location": "res/values/strings.xml: onboarding_subtitle",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Powers the floating button and lets Quick Ball perform navigation actions like Home, Back and Recents. It never reads screen content.",
      "text_zh": "用于驱动悬浮按钮，并让 Quick Ball 执行 Home、返回、最近任务等导航动作。它从不读取屏幕内容。",
      "source_location": "res/values/strings.xml: onboarding_accessibility_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Quick Ball needs just these two to run. Anything else is asked for only when you turn on a feature that needs it.",
      "text_zh": "Quick Ball 仅需这两项权限即可运行，其它权限只在你开启需要它的功能时才会申请。",
      "source_location": "res/values/strings.xml: onboarding_permissions_subtitle",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "QuickBall floating ball service that provides a floating ball overlay on your screen for quick access to features.",
      "text_zh": "QuickBall 悬浮球服务，在你的屏幕上提供悬浮球浮层，以便快速访问各项功能。",
      "source_location": "res/values/strings.xml: accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 呈现于系统无障碍列表）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Quick Ball needs Accessibility access to show the floating button and perform navigation actions.",
      "text_zh": "Quick Ball 需要无障碍权限以显示悬浮按钮并执行导航动作。",
      "source_location": "res/values/strings.xml: accessibility_setup_description",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Could not open accessibility settings",
      "text_zh": "无法打开无障碍设置",
      "source_location": "k3.a#F 内硬编码 Toast 文案",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无死循环。MainActivity 仅重写 onCreate/attachBaseContext，未在 onResume/onWindowFocusChanged 中重跳；k3.a.F 异常时只弹 Toast 并 return；QuickBallService.onAccessibilityEvent 仅处理前台包名变化用于隐藏悬浮球，不含任何设置页监听或反复拉起逻辑。用户拒绝授权时应用停留在自身引导/设置页，功能不可用但不阻断退出。",
    "overlay_or_fake_settings": "无。全包无 TYPE_ACCESSIBILITY_OVERLAY 引导遮罩、无高仿系统无障碍开关页；悬浮球 Overlay 仅在服务真正连接后创建（onServiceConnected）。",
    "restricted_settings_13plus_coaching": "无。未检索到任何“应用详情 → 右上角菜单 → 允许受限设置”或 Session 安装器绕过的文案与代码。",
    "post_grant_anti_removal": "无。未发现监听设置页并 performGlobalAction(GLOBAL_ACTION_BACK/HOME) 阻止撤权；performGlobalAction 仅用于悬浮菜单的 Home/Back/Recents(1/2/3) 与音量动作(8/9)，属功能本体。",
    "benign_graceful_degradation": "有。权限说明页逐项标注 Granted/Grant，未授予时仅对应功能不可用；跳转失败降级为 Toast 提示；电池优化/自启动引导找不到厂商页面时回退到本应用详情页，均不阻断应用使用。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Activity 启动 Intent action == \"android.settings.ACCESSIBILITY_SETTINGS\" 且 extras 含 \":settings:fragment_args_key\" 指向 io.github.chayanforyou.quickball/core.QuickBallService 的瞬间；或冷启动后首次出现 MainActivity 的 Compose Permissions 页（Accessibility 卡片 + Grant 按钮）时。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页（Meet Quick Ball）",
        "page_identifier": "io.github.chayanforyou.quickball.ui.MainActivity，文本含 \"Meet Quick Ball\" / \"Get started\"",
        "why_most_useful": "判定是否为强制首启阻断式引导，以及首屏是否已把无障碍包装成其他诉求",
        "observable_utg_signals": ["标题 Meet Quick Ball 与说明文案是否与无障碍用途一致", "是否存在 Cancel/Skip/关闭控件", "是否出现恐吓、更新、清理类字样"]
      },
      {
        "page_role": "权限说明页（跳转前最后一屏）",
        "page_identifier": "MainActivity 内 Permissions 卡片，文本含 \"Accessibility\"、\"Modify System Settings\"、\"Grant\"/\"Granted\"",
        "why_most_useful": "区分透明说明与话术诱导的最关键一屏：能否看到用途解释与已授权状态、是否有拒绝路径",
        "observable_utg_signals": ["Accessibility 行是否附带真实用途描述", "Grant/Granted 状态是否由真实系统状态驱动", "是否存在“允许受限设置”类分步教学"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页，条目名 \"Quick Ball\"，描述 \"QuickBall floating ball service that provides a floating ball overlay…\"",
        "why_most_useful": "核对系统侧展示身份与声明是否与包名/文案一致，验证未被伪造或同名混淆",
        "observable_utg_signals": ["服务名与桌面应用名是否一致", "描述文本是否与 strings 资源一致", "跳转是否精准定位到该条目（fragment_args_key 生效）"]
      },
      {
        "page_role": "获权后悬浮球叠层",
        "page_identifier": "QuickBallService onServiceConnected 后出现的悬浮球/边把手 Overlay（无引导遮罩）",
        "why_most_useful": "确认获权后行为是否仅为本职悬浮球，而非在设置页上压栈遮罩或弹二次授权",
        "observable_utg_signals": ["返回应用后设置页之上是否出现遮罩/浮层", "悬浮球是否只在应用内或桌面出现", "是否存在自动点击确认"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一注意点：引导 UI 由 Compose 渲染且类名被 R8 重命名（j4/m4/l4 匿名 lambda），静态仅能从 strings.xml 与 l4.f.a 分支号对应文案与跳转，页面层级需运行期 UTG 补齐；静态未加壳，不影响运行期捕获。"
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
    "k3.a#F",
    "l4.f#a",
    "io.github.chayanforyou.quickball.core.QuickBallService#onServiceConnected",
    "io.github.chayanforyou.quickball.core.QuickBallService#onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
