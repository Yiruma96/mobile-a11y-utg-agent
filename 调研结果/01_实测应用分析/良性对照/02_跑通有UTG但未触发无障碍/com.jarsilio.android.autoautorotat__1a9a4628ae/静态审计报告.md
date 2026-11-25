# BN_018__1a9a4628ae｜显示调节、截屏与分屏效率 — Auto Auto-Rotate

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：131.1s

## 1. 一句话核心结论

- **核心申请方式**：冷启动时 MainActivity.onStart 检测 Usage Stats／无障碍／WRITE_SETTINGS 是否齐备，缺失即拉起禁用跳过的原生 AppIntro 引导页逐项说明并跳系统设置，返回后重新判定，全程无悬浮遮罩、无伪造设置页、无防撤权，且提供 Usage Access 作为无障碍的替代检测方式。
- **静态可见性说明**：DEX 仅经 R8 混淆，无加壳、无密文载荷、无远端 HTML；引导页结构、文案资源（res/values/strings.xml）与权限判定逻辑（st1.z/st1.w/Settings.System.canWrite）全部静态可见。唯一轻微缺口是跳转无障碍设置所用的 Settings.ACTION_ACCESSIBILITY_SETTINGS 常量被 R8 内联，未在方法引用中直接命中，但预筛 JUMP_A11Y_SETTINGS 与返回后复查逻辑已闭合该链路。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1a9a4628ae0105488db269a07393ae9f3e933ac54e4ad1eb3f4b0eeb1eaa64c7` |
| 包名 / 年份 | `com.jarsilio.android.autoautorotate` / 2025-2026 |
| 家族 / 品类 | **显示调节、截屏与分屏效率**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.jarsilio.android.autoautorotate_53.apk |
| 桌面显示名 | Auto Auto-Rotate |
| 引导页宣称品牌/身份 | Auto Auto-Rotate（开源无障碍自动旋转应用，com.jarsilio.android.autoautorotate） |
| 系统无障碍列表服务名 | Auto Auto-Rotate |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.jarsilio.android.autoautorotate.services.AppLaunchDetectionService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | This service is used to detect activity launches, which allows us to know which app is currently running in the foreground. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.jarsilio.android.autoautorotate.MainActivity（LAUNCHER，@style/AppTheme.NoActionBar） | onStart() 判定 !(st1.z() \|\| st1.w()) \|\| !Settings$System.canWrite() 成立 | 原生Activity | **原文**：无（此步仅日志 "'Usage access' or 'Accessibility Service' and 'Write settings' permission must be allowed. Disabling Auto Auto-Rotate and starting AppIntro"）<br>**译注**：未授予使用情况访问或无障碍服务、或未授予写入设置权限时，关闭功能并跳转引导页 | 无需操作，自动跳转引导页；用户可返回键退出应用 | `com.jarsilio.android.autoautorotate.MainActivity#onStart` |
| 2 | 引导说明页 | com.jarsilio.android.autoautorotate.appintro.AppIntro（AppIntroBase 翻页容器） | onCreate() 中 registerForActivityResult 启动器跳入；setSkipButtonEnabled(false)，再按缺失项 addSlide | 原生Activity | **原文**：无（容器层文案由各 slide fragment 提供）<br>**译注**：引导页容器，关闭“跳过”按钮，仅保留“下一步/完成”与系统返回 | 逐页阅读并点“下一步”；无跳过按钮，可返回键退出整个引导 | `com.jarsilio.android.autoautorotate.appintro.AppIntro#onCreate` |
| 3 | 引导说明页 | Slide 片段 gv1（实现 com.github.appintro.SlidePolicy）——Usage Access 说明页 | AppIntro.onCreate 在 !st1.z() && !st1.w() 时 addSlide(new gv1()) | 原生Activity | **原文**：无（文案在 gv1.onCreate 内部绑定字符串资源）<br>**译注**：说明需授予“使用情况访问”以检测前台应用，并提供跳转按钮 | 点击跳转系统“使用情况访问”设置；未授权时 isPolicyRespected=false 且 onUserIllegallyRequestedNextPage 阻止翻页（无法跳过） | `gv1#isPolicyRespected / gv1#onUserIllegallyRequestedNextPage` |
| 4 | 引导说明页 | Slide 片段 hh——无障碍服务说明页（含跳转按钮） | AppIntro.onCreate 在 !st1.y() 时 addSlide(new hh()) | 原生Activity | **原文**：App detection: Accessibility Service Auto Auto-Rotate can be used as an 'Accessibility Service' to detect the currently running app more rel…（摘录，完整文案在 res/values/strings.xml 的 accessibility_service_explanation 等 key）<br>**译注**：应用检测：无障碍服务——可将 Auto Auto-Rotate 用作“无障碍服务”，以更可靠地检测当前运行的应用 | 阅读说明后点击按钮跳转系统无障碍设置并手动开启 Auto Auto-Rotate；同时告知可用 Usage Access 替代 | `hh#onCreate / hh#onViewCreated；res/xml/accessibility_service.xml` |
| 5 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（服务列表项显示为 “Auto Auto-Rotate”，描述为 accessibility_service_description） | hh 页面按钮点击构造 Intent 跳转（预筛 JUMP_A11Y_SETTINGS；常量被 R8 内联） | 系统无障碍页 | **原文**：This service is used to detect activity launches, which allows us to know which app is currently running in the foreground.<br>**译注**：此服务用于检测 Activity 启动，使我们能够知道当前哪个应用在前台运行。 | 在系统无障碍列表中点击 “Auto Auto-Rotate” 并确认开启（系统原生确认弹窗） | `res/xml/accessibility_service.xml（android:description=@string/accessibility_service_description）；res/values/strings.xml:23` |
| 6 | 引导说明页 | Slide 片段 g22——WRITE_SETTINGS 说明页 | AppIntro.onCreate 在 !Settings$System.canWrite() 时 addSlide(new g22()) | 原生Activity | **原文**：无（文案在 g22.onCreate 内部绑定字符串资源）<br>**译注**：说明需授予“修改系统设置”以切换自动旋转 | 点击按钮跳转应用详情/写入设置授权页手动允许 | `com.jarsilio.android.autoautorotate.appintro.AppIntro#onCreate（g22 slide）` |
| 7 | 引导说明页 | Slide 片段 f51（POST_NOTIFICATIONS）与 wf（OEM 保活/自启动）及自定义 layout 页 2131427473 | AppIntro.onCreate：SDK_INT>=33 且通知权限未授予时 addSlide(f51)；设备已安装 dontkillmyapp 名单内 OEM 应用时 addSlide(wf)；末尾固定 addSlide(custom layout) | 原生Activity | **原文**：Auto Auto-Rotate needs to run in the background to do its work. Android itself and some manufacturers restrict which apps can run in the bac… / Please allow Auto Auto-Rotate to show notifications by tapping on the button below.<br>**译注**：Auto Auto-Rotate 需要在后台运行才能工作，Android 本身及部分厂商会限制应用后台运行；请点击下方按钮允许 Auto Auto-Rotate 显示通知。 | 点击按钮授予通知权限；按 OEM 差异跳转厂商自启动/电池优化设置页；引导结束点“完成” | `com.jarsilio.android.autoautorotate.appintro.AppIntro#onCreate` |
| 8 | 拒权反馈循环 | MainActivity.onStart ← AppIntro.onDonePressed（setResult(-1)/finish）与 ActivityResult 回调 gh.a | 用户从系统设置返回或点击“完成”关闭引导，MainActivity 重新 onStart / ActivityResult 回调 | 原生Activity | 无 | 继续补齐权限或退出应用；不存在后台定时强制拉起 | `com.jarsilio.android.autoautorotate.MainActivity#onStart；gh#a；com.jarsilio.android.autoautorotate.appintro.AppIntro#onDonePressed` |
| 9 | 获权后动作 | com.jarsilio.android.autoautorotate.services.AppLaunchDetectionService + PersistentService（前台服务 specialUse）+ AutoStartReceiver | st1.w() 命中 enabled_accessibility_services 后服务绑定；PersistentService.onCreate/onStartCommand 亦复检；开机 BOOT_COMPLETED 重启 | 通知栏（常驻前台服务通知） | **原文**：To ensure smooth operation, Auto Auto-Rotate requires permission to display a persistent notification. This notification can be minimized or…<br>**译注**：为保证顺畅运行，Auto Auto-Rotate 需要显示常驻通知的权限；该通知可被最小化。 | 无需操作；服务仅监听 typeWindowStateChanged 事件识别前台应用并切换自动旋转 | `com.jarsilio.android.autoautorotate.services.AppLaunchDetectionService#onAccessibilityEvent；st1#w；res/xml/accessibility_service.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/xml/accessibility_service.xml 的 android:description（@string/accessibility_service_description），直接显示在系统“无障碍 → 已安装服务”列表中该应用条目下方
- res/values/strings.xml 的 accessibility_service_explanation（含 <b>App detection: Accessibility Service</b>），在应用内 AppIntro 的无障碍说明 slide（hh）与设置页“应用检测方式”说明中呈现
- res/values/strings.xml 的 pref_use_accessibility_service / pref_use_accessibility_service_summary（App detection method：可用 Usage Access 替代无障碍服务），在主界面设置项中呈现
- AppIntro 原生引导页 slide 文案：gv1（Usage Access）、g22（WRITE_SETTINGS）、hh（无障碍服务）、f51（通知权限）、wf（OEM 后台限制，含 dontkillmyapp.com 链接）、自定义 layout 2131427473
- AppIntro 内的电池优化说明与跳转："Battery (un)optimization"、"Please allow Auto Auto-Rotate to ignore the battery optimizations after tapping on the button below."，由 MainActivity$a#onSharedPreferenceChanged 与 fh#onClick 触发 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS
- 系统无障碍开启确认弹窗（系统原生，非应用自绘）
- 常驻前台服务通知（PersistentService，specialUse 类型）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | This service is used to detect activity launches, which allows us to know which app is currently running in the foreground. | 此服务用于检测 Activity 启动，使我们能够知道当前哪个应用在前台运行。 | `res/values/strings.xml:23（accessibility_service_description，经 res/xml/accessibility_service.xml 引用）` | 良性透明说明 |
| en | App detection: Accessibility Service Auto Auto-Rotate can be used as an 'Accessibility Service' to detect the currently running app more reliably | 应用检测：无障碍服务——可将 Auto Auto-Rotate 用作“无障碍服务”，以更可靠地检测当前运行的应用。 | `res/values/strings.xml（accessibility_service_explanation，AppIntro 无障碍 slide hh）` | 良性透明说明 |
| en | Use 'Accessibility Service' instead of 'Usage Access' to detect currently running app. | 使用“无障碍服务”代替“使用情况访问”来检测当前运行的应用。 | `res/values/strings.xml:165（pref_use_accessibility_service_summary）` | 良性透明说明 |
| en | Auto Auto-Rotate needs to run in the background to do its work. Android itself and some manufacturers restrict which apps can run in the background | Auto Auto-Rotate 需要在后台运行才能完成工作。Android 本身及部分厂商会限制哪些应用可以在后台运行。 | `res/values/strings.xml（AppIntro 通知/保活 slide f51、wf）` | 良性透明说明 |
| en | Please allow Auto Auto-Rotate to ignore the battery optimizations after tapping on the button below. | 请点击下方按钮后允许 Auto Auto-Rotate 忽略电池优化。 | `res/values/strings.xml（电池优化引导）；fh#onClick 触发 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` | 良性透明说明 |
| en | Some Android manufacturers are pretty harsh while killing other apps to preserve battery (check out https://dontkillmyapp.com for more information) | 部分 Android 厂商为省电会较为激进地杀掉其他应用（更多信息见 https://dontkillmyapp.com）。 | `res/values/strings.xml（OEM 保活 slide wf）` | 受限设置分步教学 |
| en | If you tap on the button below, we'll try to take you to your device's specific settings. Please enable Auto Auto-Rotate to auto-start and to keep running in the background. | 点击下方按钮，我们会尝试带你到本设备对应的设置页。请允许 Auto Auto-Rotate 自启动并在后台持续运行。 | `res/values/strings.xml（OEM 自启动引导，配合 <queries> 中 miui/huawei/coloros/vivo 等厂商包名）` | 受限设置分步教学 |
| en | Yay, permission granted! | 太好了，权限已授予！ | `res/values/strings.xml（AppIntro 各 slide 授权成功反馈）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：AppIntro 的 setSkipButtonEnabled(false) 关闭跳过；gv1 实现 SlidePolicy，isPolicyRespected 返回 st1.z()，未授权时 onUserIllegallyRequestedNextPage 阻止滑动翻页。用户从系统设置返回后，MainActivity.onStart 与 ActivityResult 回调 gh.a 重新判定 st1.z()/st1.w()/canWrite()，仍未满足则再次拉起 AppIntro，形成可随时退出应用的引导闭环；无定时器重跳、无后台强制拉起。
- **遮罩叠层 / 高仿系统设置页**：无。全部为原生 AppIntro Activity 页面与系统原生设置页/系统原生无障碍确认弹窗，无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现引导用户进入应用详情点右上角菜单开启“允许受限设置”，也无 Session 安装器绕过；仅有常规 OEM 电池优化/自启动跳转引导（dontkillmyapp 说明）。
- **获权后即时行为与防撤权机制**：无。无障碍服务仅处理 typeWindowStateChanged 事件；未见 GLOBAL_ACTION_BACK/HOME 操作、无自动点击确认、无监听设置页阻止撤权；AutoStartReceiver 仅在 BOOT_COMPLETED/MY_PACKAGE_REPLACED 重启前台服务。
- **良性降级 / 替代方案**：有。MainActivity.onStart 的判定为 st1.z() || st1.w()，即 Usage Stats（PACKAGE_USAGE_STATS）与无障碍服务二者取一；设置项 pref_use_accessibility_service_summary 明确说明可用 “Usage Access” 替代 “Accessibility Service” 检测前台应用，无障碍属可选增强而非强制门槛。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后首次进入 MainActivity 并在 onStart 触发 AppIntro 启动器的瞬间（无需点击任何开关）；以及点击 AppIntro 无障碍 slide（hh）按钮、捕获到 Intent action = android.settings.ACCESSIBILITY_SETTINGS 的时刻。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。文案全部为原生 TextView/字符串资源，UTG 可直接提取；无图片诱导、无远端 HTML、无加壳。唯一注意点是跳转无障碍设置的 Intent action 常量被 R8 内联，静态文本未直接命中，UTG 侧应以捕获到的系统设置页 action 为准。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页首屏（AppIntro，无跳过按钮）** | Activity com.jarsilio.android.autoautorotate.appintro.AppIntro，底部仅有“下一步/完成”而无 Skip，页面标题为应用检测/权限说明 | 证明引导为冷启动自动触发且不可跳过，是区分“良性透明说明”与“诱导/强制”的第一判定点 | 当前 Activity 为 appintro.AppIntro；底部按钮区无 skip 文本节点；文案含 App detection / permission 等权限说明关键词 |
| **无障碍服务说明 slide（跳转前教学页）** | hh slide 页，含“App detection: Accessibility Service”标题与跳转按钮 | 该页决定用户是否理解无障碍用途；可核对说明文字与 android:description 是否一致、有无伪装品牌 | 文案与 strings.xml accessibility_service_explanation 一致；存在跳转按钮文本；页面未出现其他品牌名或系统警告字样 |
| **系统无障碍服务列表项** | 系统 Settings 无障碍页，条目显示 “Auto Auto-Rotate”，描述为检测 Activity 启动 | 确认服务名与桌面名一致、无同形字/空白挤出伪装，且跳转目标为系统原生页面 | 包名 com.jarsilio.android.autoautorotate 对应条目；description 文本与 strings.xml 完全一致；当前窗口包名为 com.android.settings |
| **从设置返回后的复查/再次引导** | 返回 MainActivity 后是否立刻再次压栈 AppIntro，或停留在主界面 | 区分良性降级（停留/说明）与恶意死循环重跳、遮罩叠层 | 返回后栈顶 Activity 类型；是否存在 overlay 窗口（TYPE_APPLICATION_OVERLAY）；是否出现重复弹窗计数 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.jarsilio.android.autoautorotate.MainActivity#onStart`
- `com.jarsilio.android.autoautorotate.appintro.AppIntro#onCreate`
- `gv1#isPolicyRespected`
- `st1#w`
- `gh#a`
- `res/xml/accessibility_service.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态可见，无加壳）

- **入口与触发**：`MainActivity.onCreate` 用 `registerForActivityResult(StartActivityForResult, gh)` 注册一个启动器；`onStart` 做三项检查：Usage Stats（`st1.z`）、无障碍已启用（`st1.w` 读 `Settings.Secure#enabled_accessibility_services`）、`Settings.System.canWrite`。**任一缺失即停用功能、停止 `PersistentService` 并直接拉起 `AppIntro`**（冷启动即进入引导，无需先点功能开关）。
- **引导载体是原生 AppIntro 引导页（非 WebView、非悬浮窗、非高仿设置页）**：`AppIntro.onCreate` 调用 `setSkipButtonEnabled(false)` 关闭"跳过"，再按缺失项动态 `addSlide`：`gv1`（Usage Access，实现 `SlidePolicy`）、`g22`（WRITE_SETTINGS）、`hh`（无障碍服务）、`f51`（Android 13 POST_NOTIFICATIONS）、`wf`（OEM 保活/自启动）与一个自定义 layout 页。
- **强制性与可退出性**：`gv1.isPolicyRespected` 直接返回 `st1.z()`，未授权时 `onUserIllegallyRequestedNextPage` 阻止滑动翻页——属"不可跳过但可返回退出"的引导，无悬浮遮罩、无压栈叠层、无伪造开关页。
- **无障碍不是唯一路径（良性降级）**：`MainActivity.onStart` 的判定是 `st1.z() || st1.w()`，且 `pref_use_accessibility_service_summary` 明示"可用 Usage Access 替代 Accessibility Service 检测前台应用"，即无障碍为可选增强项，符合其真实功能（按前台应用切换自动旋转）。
- **拒权反馈**：无 `onResume` 定时重跳、无 `Timer`、无 `GLOBAL_ACTION_BACK` 阻止撤权；每次回到 `MainActivity` 前台时 `onStart` 重新判定并再次拉起 `AppIntro`，属可随时退出应用的引导闭环。
- **身份一致**：桌面名 `Auto Auto-Rotate`、无障碍服务标签同为 `Auto Auto-Rotate`、`android:description` 如实说明"用于检测 Activity 启动以获知前台应用"，无空白挤出/同形字/多 `activity-alias`/伪造 `isAccessibilityTool`。
- **未决点**：`ACTION_ACCESSIBILITY_SETTINGS` 常量经 R8 内联后未在方法引用与反编译文本中直接命中（预筛 `JUMP_A11Y_SETTINGS` 已确认存在跳转点），其精确字面位于 `hh`/`gh` 内的 Intent 构造处，属轻度静态定位缺口，不影响链路判定。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 仅经 R8 混淆，无加壳、无密文载荷、无远端 HTML；引导页结构、文案资源（res/values/strings.xml）与权限判定逻辑（st1.z/st1.w/Settings.System.canWrite）全部静态可见。唯一轻微缺口是跳转无障碍设置所用的 Settings.ACTION_ACCESSIBILITY_SETTINGS 常量被 R8 内联，未在方法引用中直接命中，但预筛 JUMP_A11Y_SETTINGS 与返回后复查逻辑已闭合该链路。",
  "summary_one_liner": "冷启动时 MainActivity.onStart 检测 Usage Stats／无障碍／WRITE_SETTINGS 是否齐备，缺失即拉起禁用跳过的原生 AppIntro 引导页逐项说明并跳系统设置，返回后重新判定，全程无悬浮遮罩、无伪造设置页、无防撤权，且提供 Usage Access 作为无障碍的替代检测方式。",
  "disguise_identity": {
    "app_display_name": "Auto Auto-Rotate",
    "claimed_brand_or_persona": "Auto Auto-Rotate（开源无障碍自动旋转应用，com.jarsilio.android.autoautorotate）",
    "a11y_service_label": "Auto Auto-Rotate",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.jarsilio.android.autoautorotate.MainActivity（LAUNCHER，@style/AppTheme.NoActionBar）",
      "trigger_event": "onStart() 判定 !(st1.z() || st1.w()) || !Settings$System.canWrite() 成立",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（此步仅日志 \"'Usage access' or 'Accessibility Service' and 'Write settings' permission must be allowed. Disabling Auto Auto-Rotate and starting AppIntro\"）",
      "shown_text_zh": "未授予使用情况访问或无障碍服务、或未授予写入设置权限时，关闭功能并跳转引导页",
      "user_action_requested": "无需操作，自动跳转引导页；用户可返回键退出应用",
      "code_anchor": "com.jarsilio.android.autoautorotate.MainActivity#onStart"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.jarsilio.android.autoautorotate.appintro.AppIntro（AppIntroBase 翻页容器）",
      "trigger_event": "onCreate() 中 registerForActivityResult 启动器跳入；setSkipButtonEnabled(false)，再按缺失项 addSlide",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（容器层文案由各 slide fragment 提供）",
      "shown_text_zh": "引导页容器，关闭“跳过”按钮，仅保留“下一步/完成”与系统返回",
      "user_action_requested": "逐页阅读并点“下一步”；无跳过按钮，可返回键退出整个引导",
      "code_anchor": "com.jarsilio.android.autoautorotate.appintro.AppIntro#onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "Slide 片段 gv1（实现 com.github.appintro.SlidePolicy）——Usage Access 说明页",
      "trigger_event": "AppIntro.onCreate 在 !st1.z() && !st1.w() 时 addSlide(new gv1())",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（文案在 gv1.onCreate 内部绑定字符串资源）",
      "shown_text_zh": "说明需授予“使用情况访问”以检测前台应用，并提供跳转按钮",
      "user_action_requested": "点击跳转系统“使用情况访问”设置；未授权时 isPolicyRespected=false 且 onUserIllegallyRequestedNextPage 阻止翻页（无法跳过）",
      "code_anchor": "gv1#isPolicyRespected / gv1#onUserIllegallyRequestedNextPage"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "Slide 片段 hh——无障碍服务说明页（含跳转按钮）",
      "trigger_event": "AppIntro.onCreate 在 !st1.y() 时 addSlide(new hh())",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "App detection: Accessibility Service Auto Auto-Rotate can be used as an 'Accessibility Service' to detect the currently running app more rel…（摘录，完整文案在 res/values/strings.xml 的 accessibility_service_explanation 等 key）",
      "shown_text_zh": "应用检测：无障碍服务——可将 Auto Auto-Rotate 用作“无障碍服务”，以更可靠地检测当前运行的应用",
      "user_action_requested": "阅读说明后点击按钮跳转系统无障碍设置并手动开启 Auto Auto-Rotate；同时告知可用 Usage Access 替代",
      "code_anchor": "hh#onCreate / hh#onViewCreated；res/xml/accessibility_service.xml"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（服务列表项显示为 “Auto Auto-Rotate”，描述为 accessibility_service_description）",
      "trigger_event": "hh 页面按钮点击构造 Intent 跳转（预筛 JUMP_A11Y_SETTINGS；常量被 R8 内联）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "This service is used to detect activity launches, which allows us to know which app is currently running in the foreground.",
      "shown_text_zh": "此服务用于检测 Activity 启动，使我们能够知道当前哪个应用在前台运行。",
      "user_action_requested": "在系统无障碍列表中点击 “Auto Auto-Rotate” 并确认开启（系统原生确认弹窗）",
      "code_anchor": "res/xml/accessibility_service.xml（android:description=@string/accessibility_service_description）；res/values/strings.xml:23"
    },
    {
      "step": 6,
      "stage": "引导说明页",
      "screen_or_component": "Slide 片段 g22——WRITE_SETTINGS 说明页",
      "trigger_event": "AppIntro.onCreate 在 !Settings$System.canWrite() 时 addSlide(new g22())",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（文案在 g22.onCreate 内部绑定字符串资源）",
      "shown_text_zh": "说明需授予“修改系统设置”以切换自动旋转",
      "user_action_requested": "点击按钮跳转应用详情/写入设置授权页手动允许",
      "code_anchor": "com.jarsilio.android.autoautorotate.appintro.AppIntro#onCreate（g22 slide）"
    },
    {
      "step": 7,
      "stage": "引导说明页",
      "screen_or_component": "Slide 片段 f51（POST_NOTIFICATIONS）与 wf（OEM 保活/自启动）及自定义 layout 页 2131427473",
      "trigger_event": "AppIntro.onCreate：SDK_INT>=33 且通知权限未授予时 addSlide(f51)；设备已安装 dontkillmyapp 名单内 OEM 应用时 addSlide(wf)；末尾固定 addSlide(custom layout)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Auto Auto-Rotate needs to run in the background to do its work. Android itself and some manufacturers restrict which apps can run in the bac… / Please allow Auto Auto-Rotate to show notifications by tapping on the button below.",
      "shown_text_zh": "Auto Auto-Rotate 需要在后台运行才能工作，Android 本身及部分厂商会限制应用后台运行；请点击下方按钮允许 Auto Auto-Rotate 显示通知。",
      "user_action_requested": "点击按钮授予通知权限；按 OEM 差异跳转厂商自启动/电池优化设置页；引导结束点“完成”",
      "code_anchor": "com.jarsilio.android.autoautorotate.appintro.AppIntro#onCreate"
    },
    {
      "step": 8,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onStart ← AppIntro.onDonePressed（setResult(-1)/finish）与 ActivityResult 回调 gh.a",
      "trigger_event": "用户从系统设置返回或点击“完成”关闭引导，MainActivity 重新 onStart / ActivityResult 回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "重新校验三项条件；仍未满足则再次拉起 AppIntro 引导页（无定时器、无悬浮遮罩、无自动点击）",
      "user_action_requested": "继续补齐权限或退出应用；不存在后台定时强制拉起",
      "code_anchor": "com.jarsilio.android.autoautorotate.MainActivity#onStart；gh#a；com.jarsilio.android.autoautorotate.appintro.AppIntro#onDonePressed"
    },
    {
      "step": 9,
      "stage": "获权后动作",
      "screen_or_component": "com.jarsilio.android.autoautorotate.services.AppLaunchDetectionService + PersistentService（前台服务 specialUse）+ AutoStartReceiver",
      "trigger_event": "st1.w() 命中 enabled_accessibility_services 后服务绑定；PersistentService.onCreate/onStartCommand 亦复检；开机 BOOT_COMPLETED 重启",
      "ui_carrier": "通知栏（常驻前台服务通知）",
      "shown_text_verbatim": "To ensure smooth operation, Auto Auto-Rotate requires permission to display a persistent notification. This notification can be minimized or…",
      "shown_text_zh": "为保证顺畅运行，Auto Auto-Rotate 需要显示常驻通知的权限；该通知可被最小化。",
      "user_action_requested": "无需操作；服务仅监听 typeWindowStateChanged 事件识别前台应用并切换自动旋转",
      "code_anchor": "com.jarsilio.android.autoautorotate.services.AppLaunchDetectionService#onAccessibilityEvent；st1#w；res/xml/accessibility_service.xml"
    }
  ],
  "text_presentation_locations": [
    "res/xml/accessibility_service.xml 的 android:description（@string/accessibility_service_description），直接显示在系统“无障碍 → 已安装服务”列表中该应用条目下方",
    "res/values/strings.xml 的 accessibility_service_explanation（含 <b>App detection: Accessibility Service</b>），在应用内 AppIntro 的无障碍说明 slide（hh）与设置页“应用检测方式”说明中呈现",
    "res/values/strings.xml 的 pref_use_accessibility_service / pref_use_accessibility_service_summary（App detection method：可用 Usage Access 替代无障碍服务），在主界面设置项中呈现",
    "AppIntro 原生引导页 slide 文案：gv1（Usage Access）、g22（WRITE_SETTINGS）、hh（无障碍服务）、f51（通知权限）、wf（OEM 后台限制，含 dontkillmyapp.com 链接）、自定义 layout 2131427473",
    "AppIntro 内的电池优化说明与跳转：\"Battery (un)optimization\"、\"Please allow Auto Auto-Rotate to ignore the battery optimizations after tapping on the button below.\"，由 MainActivity$a#onSharedPreferenceChanged 与 fh#onClick 触发 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS",
    "系统无障碍开启确认弹窗（系统原生，非应用自绘）",
    "常驻前台服务通知（PersistentService，specialUse 类型）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "This service is used to detect activity launches, which allows us to know which app is currently running in the foreground.",
      "text_zh": "此服务用于检测 Activity 启动，使我们能够知道当前哪个应用在前台运行。",
      "source_location": "res/values/strings.xml:23（accessibility_service_description，经 res/xml/accessibility_service.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "App detection: Accessibility Service Auto Auto-Rotate can be used as an 'Accessibility Service' to detect the currently running app more reliably",
      "text_zh": "应用检测：无障碍服务——可将 Auto Auto-Rotate 用作“无障碍服务”，以更可靠地检测当前运行的应用。",
      "source_location": "res/values/strings.xml（accessibility_service_explanation，AppIntro 无障碍 slide hh）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Use 'Accessibility Service' instead of 'Usage Access' to detect currently running app.",
      "text_zh": "使用“无障碍服务”代替“使用情况访问”来检测当前运行的应用。",
      "source_location": "res/values/strings.xml:165（pref_use_accessibility_service_summary）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Auto Auto-Rotate needs to run in the background to do its work. Android itself and some manufacturers restrict which apps can run in the background",
      "text_zh": "Auto Auto-Rotate 需要在后台运行才能完成工作。Android 本身及部分厂商会限制哪些应用可以在后台运行。",
      "source_location": "res/values/strings.xml（AppIntro 通知/保活 slide f51、wf）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Please allow Auto Auto-Rotate to ignore the battery optimizations after tapping on the button below.",
      "text_zh": "请点击下方按钮后允许 Auto Auto-Rotate 忽略电池优化。",
      "source_location": "res/values/strings.xml（电池优化引导）；fh#onClick 触发 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Some Android manufacturers are pretty harsh while killing other apps to preserve battery (check out https://dontkillmyapp.com for more information)",
      "text_zh": "部分 Android 厂商为省电会较为激进地杀掉其他应用（更多信息见 https://dontkillmyapp.com）。",
      "source_location": "res/values/strings.xml（OEM 保活 slide wf）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "If you tap on the button below, we'll try to take you to your device's specific settings. Please enable Auto Auto-Rotate to auto-start and to keep running in the background.",
      "text_zh": "点击下方按钮，我们会尝试带你到本设备对应的设置页。请允许 Auto Auto-Rotate 自启动并在后台持续运行。",
      "source_location": "res/values/strings.xml（OEM 自启动引导，配合 <queries> 中 miui/huawei/coloros/vivo 等厂商包名）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Yay, permission granted!",
      "text_zh": "太好了，权限已授予！",
      "source_location": "res/values/strings.xml（AppIntro 各 slide 授权成功反馈）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "AppIntro 的 setSkipButtonEnabled(false) 关闭跳过；gv1 实现 SlidePolicy，isPolicyRespected 返回 st1.z()，未授权时 onUserIllegallyRequestedNextPage 阻止滑动翻页。用户从系统设置返回后，MainActivity.onStart 与 ActivityResult 回调 gh.a 重新判定 st1.z()/st1.w()/canWrite()，仍未满足则再次拉起 AppIntro，形成可随时退出应用的引导闭环；无定时器重跳、无后台强制拉起。",
    "overlay_or_fake_settings": "无。全部为原生 AppIntro Activity 页面与系统原生设置页/系统原生无障碍确认弹窗，无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页。",
    "restricted_settings_13plus_coaching": "无。未发现引导用户进入应用详情点右上角菜单开启“允许受限设置”，也无 Session 安装器绕过；仅有常规 OEM 电池优化/自启动跳转引导（dontkillmyapp 说明）。",
    "post_grant_anti_removal": "无。无障碍服务仅处理 typeWindowStateChanged 事件；未见 GLOBAL_ACTION_BACK/HOME 操作、无自动点击确认、无监听设置页阻止撤权；AutoStartReceiver 仅在 BOOT_COMPLETED/MY_PACKAGE_REPLACED 重启前台服务。",
    "benign_graceful_degradation": "有。MainActivity.onStart 的判定为 st1.z() || st1.w()，即 Usage Stats（PACKAGE_USAGE_STATS）与无障碍服务二者取一；设置项 pref_use_accessibility_service_summary 明确说明可用 “Usage Access” 替代 “Accessibility Service” 检测前台应用，无障碍属可选增强而非强制门槛。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后首次进入 MainActivity 并在 onStart 触发 AppIntro 启动器的瞬间（无需点击任何开关）；以及点击 AppIntro 无障碍 slide（hh）按钮、捕获到 Intent action = android.settings.ACCESSIBILITY_SETTINGS 的时刻。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页首屏（AppIntro，无跳过按钮）",
        "page_identifier": "Activity com.jarsilio.android.autoautorotate.appintro.AppIntro，底部仅有“下一步/完成”而无 Skip，页面标题为应用检测/权限说明",
        "why_most_useful": "证明引导为冷启动自动触发且不可跳过，是区分“良性透明说明”与“诱导/强制”的第一判定点",
        "observable_utg_signals": ["当前 Activity 为 appintro.AppIntro", "底部按钮区无 skip 文本节点", "文案含 App detection / permission 等权限说明关键词"]
      },
      {
        "page_role": "无障碍服务说明 slide（跳转前教学页）",
        "page_identifier": "hh slide 页，含“App detection: Accessibility Service”标题与跳转按钮",
        "why_most_useful": "该页决定用户是否理解无障碍用途；可核对说明文字与 android:description 是否一致、有无伪装品牌",
        "observable_utg_signals": ["文案与 strings.xml accessibility_service_explanation 一致", "存在跳转按钮文本", "页面未出现其他品牌名或系统警告字样"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页，条目显示 “Auto Auto-Rotate”，描述为检测 Activity 启动",
        "why_most_useful": "确认服务名与桌面名一致、无同形字/空白挤出伪装，且跳转目标为系统原生页面",
        "observable_utg_signals": ["包名 com.jarsilio.android.autoautorotate 对应条目", "description 文本与 strings.xml 完全一致", "当前窗口包名为 com.android.settings"]
      },
      {
        "page_role": "从设置返回后的复查/再次引导",
        "page_identifier": "返回 MainActivity 后是否立刻再次压栈 AppIntro，或停留在主界面",
        "why_most_useful": "区分良性降级（停留/说明）与恶意死循环重跳、遮罩叠层",
        "observable_utg_signals": ["返回后栈顶 Activity 类型", "是否存在 overlay 窗口（TYPE_APPLICATION_OVERLAY）", "是否出现重复弹窗计数"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。文案全部为原生 TextView/字符串资源，UTG 可直接提取；无图片诱导、无远端 HTML、无加壳。唯一注意点是跳转无障碍设置的 Intent action 常量被 R8 内联，静态文本未直接命中，UTG 侧应以捕获到的系统设置页 action 为准。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.jarsilio.android.autoautorotate.MainActivity#onStart",
    "com.jarsilio.android.autoautorotate.appintro.AppIntro#onCreate",
    "gv1#isPolicyRespected",
    "st1#w",
    "gh#a",
    "res/xml/accessibility_service.xml"
  ]
}
```

</details>
