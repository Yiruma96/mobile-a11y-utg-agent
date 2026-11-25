# BN_021__ae84008e69｜显示调节、截屏与分屏效率 — Circle to Share

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：153.1s

## 1. 一句话核心结论

- **核心申请方式**：用户在设置页主动点击“Open accessibility settings”时，应用先用原生 DisclosureActivity 逐条披露截屏/元素位置读取范围并给出“No thanks”退出路径，同意后才一次性跳转系统无障碍设置页，未开启时仅 Toast 提示原因，无遮罩、无拒权循环。
- **静态可见性说明**：未加壳，classes.dex 全量可反编译；引导链（MainActivity → DisclosureActivity → 系统 ACCESSIBILITY_SETTINGS）的触发条件、按钮分支、同意状态持久化与跳转 Intent 均静态可见。仅 A0.b.f0 外链 URL 的具体目标未展开核验，不影响引导流程判定。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ae84008e6909931b26facf6dbdd02940b32dcb65c06012f947f523a98bf4987b` |
| 包名 / 年份 | `eu.woshicado.circletoshare` / 2025-2026 |
| 家族 / 品类 | **显示调节、截屏与分屏效率**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/eu.woshicado.circletoshare_16.apk |
| 桌面显示名 | Circle to Share |
| 引导页宣称品牌/身份 | Circle to Share（F-Droid 开源截屏裁剪分享工具，自述非无障碍工具、无网络权限） |
| 系统无障碍列表服务名 | Circle to Share |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。代码经 R8 混淆（T0.s/T0.t/T0.e 等短类名），但属常规编译优化；显示名、无障碍服务标签、说明文案三者一致，无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `eu.woshicado.circletoshare.capture.ScreenshotAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | Lets Circle to Share capture the screen when you trigger it with the assistant gesture, the Quick Settings tile, or the app's floating button. You can then crop and share it. Screen content (element positions) is read only at the moment of capture, and only to align the crop box with what's on screen; if enabled in the app. Nothing is captured until you trigger it, nothing is saved to your device unless you tap Save, and nothing ever leaves it. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | eu.woshicado.circletoshare.MainActivity（主题 Theme.CircleToShare 的设置页） | onCreate() 绑定各控件；onStart() 注册 enabled_accessibility_services / voice_interaction_service / voice_recognition_service 的 ContentObserver | 原生Activity | **原文**：status_accessibility 状态行文案由 z() 动态填充（如 error_accessibility_stale: "The accessibility fallback is switched on but not running. Switch it off and on again under Settings → Accessibility."）<br>**译注**：冷启动不弹任何说明或权限弹窗，仅在设置页状态卡上显示无障碍/助手/磁贴的真实开启状态；无障碍未开启时显示对应状态提示文字。 | 无强制操作；页面提供 Open accessibility settings / Open assistant settings / Add Quick Settings tile / Open language settings 等按钮及多个功能开关，用户可自由忽略。 | `eu.woshicado.circletoshare.MainActivity.onCreate / onStart / z` |
| 2 | 引导说明页 | eu.woshicado.circletoshare.DisclosureActivity（原生说明页，layout 2131427356） | 用户点击 btn_accessibility_settings（T0.s.onClick case 7）且 cts.a11y_consent 为 false → ActivityResultLauncher G 启动 DisclosureActivity；另在服务已开启但未记录同意时由 MainActivity.z() 经 Launcher H 补发一次 | 原生Activity | **原文**：Before you turn on the accessibility service / Circle to Share uses Android's Accessibility API (AccessibilityService) to capture your screen when you ask it to... It is not an accessibility tool. Nothing it accesses is collected by, sent to, or shared with the developer or anyone else. / Tap Agree to allow this. You then switch the service on in Android's accessibility settings, and can switch it off there at any time. Tap No thanks to keep using Circle to Share with the assistant gesture only.<br>**译注**：“在你开启无障碍服务之前”：说明应用用 AccessibilityService 在你主动触发时截屏，它不是无障碍工具，所访问内容不会被收集或发送给开发者；点 Agree 后你再到系统无障碍设置里开启，并可随时关闭；点 No thanks 可继续仅用助手手势，磁贴、悬浮球与吸附功能保持关闭。 | 三选一：Agree（写入 cts.a11y_consent=true 并返回 RESULT_OK）、No thanks（setResult(0) 直接 finish，无二次打扰）、或点击正文链接了解详情；均有明确取消/跳过按钮。 | `eu.woshicado.circletoshare.DisclosureActivity.onCreate + T0.e.onClick；res/values/strings.xml disclosure_title/disclosure_lead/disclosure_choice_body` |
| 3 | 跳无障碍设置 | 系统 Settings 无障碍页（android.settings.ACCESSIBILITY_SETTINGS），用户需在列表中找到服务项 Circle to Share | DisclosureActivity 返回 RESULT_OK → 启动器回调 T0.t.b() 执行 mainActivity.s(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))；已同意用户则由 T0.s.onClick case 7 直接跳转 | 系统无障碍页 | **原文**：Open accessibility settings（按钮文案）；系统列表项显示 label "Circle to Share"，详情描述为 accessibility_service_description 全文<br>**译注**：点击“打开无障碍设置”后进入系统无障碍设置页；列表中以“Circle to Share”为名展示，点开可见完整披露说明。全程为系统原生页面，应用不叠加任何遮罩或仿冒开关。 | 用户在系统页面内自行选择 Circle to Share 并开启开关（系统会再次弹出自身的权限确认）；应用无法代为点击。 | `T0.s.onClick case 7 / T0.t.b；res/values/strings.xml btn_accessibility_settings；res/xml/accessibility_service_config.xml` |
| 4 | 拒权反馈循环 | MainActivity 设置页开关（MaterialSwitch）与 Toast | 用户返回应用后尝试操作依赖无障碍的功能（如磁贴开关 u.onCheckedChanged → MainActivity.t(CompoundButton)），或状态刷新 z() | 原生Activity | **原文**：Toast: ScreenshotAccessibilityService.Companion.whyNotRunning(context) 对应文案（如 "Enable the accessibility fallback (step 2) first." / "Open Circle to Share and agree to the accessibility disclosure first."）；状态行 error_needs_accessibility<br>**译注**：若仍未开启，开关自动回弹为关闭并 Toast 说明具体原因（如“请先在应用内同意无障碍披露”“请先开启无障碍回退”），停留在当前页，不自动重跳设置页。 | 用户可再次主动点击按钮前往设置，或直接放弃该功能；无强制、无循环拉起。 | `eu.woshicado.circletoshare.MainActivity.t / z；res/values/strings.xml error_needs_accessibility / error_needs_consent` |
| 5 | 获权后动作 | ScreenshotAccessibilityService（无障碍服务）与悬浮球/磁贴 | 服务开启后 MainActivity.onStart 的 ContentObserver 触发 z() 刷新状态；DisclosureActivity Agree 分支调用 ScreenshotAccessibilityService.Companion.applyBubbleState()；用户点“Add Quick Settings tile”走 StatusBarManager.requestAddTileService() | 原生Activity | **原文**：disclosure_use_body: "• Everything is processed on this device, in memory, to show you the crop tool. ... • An image leaves Circle to Share only when you tap Share or Copy... The app has no internet permission. • The service never taps, types or changes settings for you."<br>**译注**：获权后仅在本地内存处理截图、显示裁剪工具；仅当用户点 Share/Copy/Save 才写出图片；应用无网络权限；服务不会代替用户点击或更改设置（仅收起通知栏与实验性滚动截屏手势两项动作）。 | 用户后续通过助手手势 / 磁贴 / 悬浮球主动触发截屏；磁贴添加需在系统弹窗中确认。 | `ScreenshotAccessibilityService.Companion.applyBubbleState / MainActivity.z / T0.s.onClick case 9；res/values/strings.xml disclosure_use_body` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 设置页内嵌状态卡（TextView 2131231176/2131231177/2131231143 等），显示无障碍与助手开关的真实状态及错误提示（strings.xml status_* / error_*）
- DisclosureActivity 原生 Activity 说明页（layout 2131427356）：标题 disclosure_title、导语 disclosure_lead、What it accesses（disclosure_access_body）、How it is used（disclosure_use_body）、Your choice（disclosure_choice_body），底部 Agree / No thanks 按钮
- 系统无障碍设置列表项名称 accessibility_service_label = "Circle to Share"，详情页描述 accessibility_service_description（长段透明披露）
- 操作失败时的 Toast（ScreenshotAccessibilityService.Companion.whyNotRunning、Toast 2131755125/2131755126）
- 设置页按钮文案：Open accessibility settings / Open assistant settings / Add Quick Settings tile / Open language settings（strings.xml btn_*）
- 未出现任何 WebView、assets HTML、悬浮窗遮罩或伪造系统设置页承载引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Lets Circle to Share capture the screen when you trigger it with the assistant gesture, the Quick Settings tile, or the app's floating button. You can then crop and share it. Screen content (element positions) is read only at the moment of capture, and only to align the crop box with what's on screen; if enabled in the app. Nothing is captured until you trigger it, nothing is saved to your device unless you tap Save, and nothing ever leaves it. | Circle to Share 仅在你通过助手手势、快捷设置磁贴或应用悬浮按钮触发时截取屏幕，随后你可裁剪并分享。屏幕内容（元素位置）仅在截屏瞬间读取，且仅用于让裁剪框对齐屏幕内容（如应用内已启用）。未触发前不截取任何内容，未点保存不写入设备，任何内容都不会外传。 | `res/values/strings.xml key=accessibility_service_description（系统无障碍详情页展示）` | 良性透明说明 |
| en | Circle to Share uses Android's Accessibility API (AccessibilityService) to capture your screen when you ask it to: from the Quick Settings tile, the floating button, or as a fallback for the assistant gesture. It is not an accessibility tool. Nothing it accesses is collected by, sent to, or shared with the developer or anyone else. | Circle to Share 使用 Android 无障碍 API（AccessibilityService）在你主动请求时截屏：来自快捷设置磁贴、悬浮按钮，或作为助手手势的回退方案。它不是无障碍工具。它访问的任何内容都不会被收集、发送或共享给开发者或任何其他人。 | `res/values/strings.xml key=disclosure_lead（DisclosureActivity 页首）` | 良性透明说明 |
| en | Tap Agree to allow this. You then switch the service on in Android's accessibility settings, and can switch it off there at any time.<br><br>Tap No thanks to keep using Circle to Share with the assistant gesture only. The tile, the floating button and snapping stay off, and a service that is already on is switched off. | 点“同意”即允许上述内容，随后你到 Android 无障碍设置中开启该服务，并可随时在那里关闭。点“不用了”则可继续仅通过助手手势使用 Circle to Share；磁贴、悬浮按钮与吸附功能保持关闭，已开启的服务也会被关闭。 | `res/values/strings.xml key=disclosure_choice_body（DisclosureActivity “Your choice” 段）` | 良性透明说明 |
| en | • A screenshot of your screen at the moment you trigger a capture.<br><br>• The positions and sizes of the elements on screen (not their text or content) at that same moment, and only while "Snap to screen content" is switched on.<br><br>• Notices from the system that a window has opened or changed, with the window's title and the app it belongs to, and the positions of system windows to recognize the lock screen, the power menu and the notification shade, so the floating button and the crop tool get out of their way. | • 你触发截屏瞬间的屏幕截图。• 同一时刻屏幕上元素的位置与大小（不含其文字或内容），且仅在“吸附到屏幕内容”开启时读取。• 系统窗口打开/变化的通知，含窗口标题与所属应用，以及系统窗口位置，用于识别锁屏、电源菜单和通知栏，以便悬浮按钮与裁剪工具避让。 | `res/values/strings.xml key=disclosure_access_body（DisclosureActivity “What it accesses” 段）` | 良性透明说明 |
| en | • Everything is processed on this device, in memory, to show you the crop tool. ... • An image leaves Circle to Share only when you tap Share or Copy, and only to the app you choose, or when you tap Save, which puts it in your gallery (below Screenshots). The app has no internet permission. • The service never taps, types or changes settings for you. Its only two actions are (1) closing the notification shade when you use the Quick Settings tile; (2) simulating a swipe gesture when using the (experimental) scrollshot feature. | • 一切均在本机内存中处理以显示裁剪工具。……• 仅当你点分享/复制（且仅发给你选择的应用）或点保存（存入图库 Screenshots 目录）时图片才离开应用；应用无网络权限。• 服务绝不代替你点击、输入或更改设置，仅有两种动作：(1) 使用磁贴时收起通知栏；(2) 使用（实验性）滚动截屏时模拟滑动手势。 | `res/values/strings.xml key=disclosure_use_body（DisclosureActivity “How it is used” 段）` | 隐私承诺 |
| en | Open accessibility settings | 打开无障碍设置 | `res/values/strings.xml key=btn_accessibility_settings（MainActivity 按钮）` | 良性透明说明 |
| en | Enable the accessibility fallback (step 2) first. | 请先开启无障碍回退（第 2 步）。 | `res/values/strings.xml key=error_needs_accessibility（功能未开启时的 Toast）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。DisclosureActivity 的 No thanks 分支 setResult(0)+finish() 后直接回到设置页；用户未开启时操作相关开关仅 setChecked(false) 并 Toast 说明原因，不自动重跳系统设置；MainActivity.z() 用 I 标志位与 cts.a11y_consent 双重条件保证说明页至多补发一次。
- **遮罩叠层 / 高仿系统设置页**：无。全部引导位于本应用原生 Activity 与系统原生设置页，未使用 SYSTEM_ALERT_WINDOW 遮罩、未绘制高仿无障碍开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中未见 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、右上角菜单受限设置教学或 Session 安装器绕过路径。
- **获权后即时行为与防撤权机制**：无。未发现获权后自点确认、自授权，或监听设置页以 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；onStart 的 ContentObserver 仅用于回读状态刷新 UI。
- **良性降级 / 替代方案**：有。No thanks 后保留“仅助手手势”路径（需设为助手应用，走 VOICE_INPUT_SETTINGS/MANAGE_DEFAULT_APPS_SETTINGS 引导），磁贴、悬浮球与吸附功能关闭；已开启的服务也会被主动关闭，文案与代码一致。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到前台由 eu.woshicado.circletoshare.MainActivity 切换到 eu.woshicado.circletoshare.DisclosureActivity（首次点击“Open accessibility settings”或服务已开启但未记录同意时由 onTopResumedActivityChanged 补发），以及随后由 DisclosureActivity finish 触发的 android.settings.ACCESSIBILITY_SETTINGS 跳转瞬间。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。引导文案全部为可提取的文本节点（原生 TextView / 系统设置页），未使用纯图引导、GIF 教学或远端 HTML。边界：说明页正文中的“了解更多”链接由 A0.b.f0 打开，其目标 URL 未展开核验；若需完全排除外链导向远端页面，需补一次该 URL 的动态抓取。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动设置页（判断是否存在强制弹窗/遮罩）** | Activity=eu.woshicado.circletoshare.MainActivity，布局含 Open accessibility settings / Open assistant settings / Add Quick Settings tile 按钮与 status_accessibility 状态行 | 确认冷启动无强制引导、无叠加遮罩，是无障碍诱导审计的首要排除项 | 是否存在覆盖系统或应用界面的悬浮窗节点；是否存在除 MainActivity 之外的弹窗/对话框窗口层级；状态行文本是否为真实系统开关状态 |
| **跳转前原生披露说明页** | Activity=eu.woshicado.circletoshare.DisclosureActivity，标题“Before you turn on the accessibility service”，底部 Agree / No thanks 两个按钮 | 这是区分“透明披露”与“伪装话术”的关键页：可直接比对文案是否谎称安全/故障/更新，以及是否提供可点击的取消按钮 | 页面文本是否包含 It is not an accessibility tool / No thanks 等透明与取消要素；No thanks 按钮是否真实可点且非禁用；页面是否为原生 Activity 而非 WebView（无 WebView 节点） |
| **系统无障碍服务列表项** | Settings 无障碍页中标签为 Circle to Share 的服务项，详情描述为长段 accessibility_service_description | 核对系统层暴露的服务名与描述是否与应用自述一致、是否借用系统品牌或伪造 isAccessibilityTool | 服务项 label 文本；描述文本是否与 strings.xml accessibility_service_description 一致；是否存在额外可疑服务项或重复条目 |
| **拒权返回后的应用页** | MainActivity 恢复前台 + Toast 文本（whyNotRunning / error_needs_accessibility） | 验证拒权后是否出现自动重跳设置页的死循环或遮罩压迫 | 是否再次自动进入 ACCESSIBILITY_SETTINGS；Toast 文案内容；开关是否回弹为关闭 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `eu.woshicado.circletoshare.MainActivity.onTopResumedActivityChanged`
- `eu.woshicado.circletoshare.MainActivity.z`
- `T0.s.onClick`
- `T0.t.b`
- `T0.e.onClick`
- `res/values/strings.xml（disclosure_lead / disclosure_choice_body / disclosure_use_body / accessibility_service_description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（代码级定向核验）

**核心事实：这是一条“先说明、后跳转”的良性透明引导链，未发现诱导、恐吓、遮罩或拒权循环。**

1. **无冷启动强制弹窗。** [MainActivity.onCreate()](<resource-unit:#1.dex1 code:eu.woshicado.circletoshare.MainActivity#onCreate>) 仅 `setContentView(2131427358)` 搭建常规设置页，逐项绑定开关/按钮；`onStart()` 只注册 `Settings.Secure`（`enabled_accessibility_services`、`voice_interaction_service`、`voice_recognition_service`）的 `ContentObserver`，用于**回读真实系统状态**，不含任何定时拉起逻辑。
2. **无障碍开关是用户主动点击触发的业务入口。** [T0.s.onClick()](<resource-unit:#1.dex1 code:T0.s#onClick>) 的 `case 7`（`btn_accessibility_settings`）逻辑为：若 `cts.a11y_consent == false` → 先用 `ActivityResultLauncher` 打开 [DisclosureActivity](<resource-unit:#1.dex1 code:eu.woshicado.circletoshare.DisclosureActivity#onCreate>) 说明页；已同意过 → 直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。同方法另含 `VOICE_INPUT_SETTINGS`/`MANAGE_DEFAULT_APPS_SETTINGS`（助手角色）、`LOCALE_SETTINGS`、`LicensesActivity`、`ScrollshotSettingsActivity` 等**正常功能入口**，以及 `StatusBarManager.requestAddTileService()`（需系统弹窗由用户确认添加磁贴）。
3. **说明页为原生 Activity，含逐条“读取内容/用途”披露 + 明确的取消路径。** [T0.e.onClick()](<resource-unit:#1.dex1 code:T0.e#onClick>)：`case 1` = “No thanks” → `setResult(0); finish()`；`default` = “Agree” → 写入 `cts.a11y_consent=true`、刷新悬浮球状态、`setResult(-1); finish()`。文案自述“It is not an accessibility tool”“无网络权限”“仅在你触发时读取”，属**主动披露 + 明示能力边界**。
4. **同意后才跳系统无障碍列表；拒权后无循环。** [T0.t.b()](<resource-unit:#1.dex1 code:T0.t#b>) 接收说明页结果后 `startActivity("android.settings.ACCESSIBILITY_SETTINGS")`；`MainActivity.z()` 在服务已开启但 `a11y_consent` 未记录时才补发一次说明页（`I` 标志位防重复）。未发现 `onResume` 死循环重跳、Timer 拉起或遮罩叠层。
5. **拒绝/未开启时安全降级。** [MainActivity.t(CompoundButton)](<resource-unit:#1.dex1 code:eu.woshicado.circletoshare.MainActivity#t>) 未运行时 `setChecked(false)` 并 Toast `whyNotRunning()` 原因；`disclosure_choice_body` 明写“No thanks 可继续仅用助手手势，磁贴/悬浮球关闭”。`z()` 亦会因 `ActivityNotFoundException` 回退 Toast（`T0.s`），不强制。
6. **身份与权限声明一致。** 无障碍服务 `android:label="@string/accessibility_service_label"` = `Circle to Share`，与桌面名一致；`android:description` 为长段透明说明；配置仅 `canTakeScreenshot`/`canPerformGestures`/`canRetrieveWindowContent` + `typeWindowStateChanged`，无 `FLAG_REQUEST_FILTER_KEY_EVENTS` 类隐蔽能力。未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转、受限设置（13+）分步教学、伪造系统开关页、`isAccessibilityTool` 伪造或多 `activity-alias`。
7. **未决/边界：** `A0.b.f0()` 的具体外链目标未逐字节展开（属说明页“了解更多”链接）；`performGlobalAction` 的实际调用点未逐条核对，但披露文案已声明仅用于收起通知栏与滚动截屏手势。加壳初判 `False`，DEX 完整静态可见。

```json
{
  "static_visibility": "clear",
  "visibility_note": "未加壳，classes.dex 全量可反编译；引导链（MainActivity → DisclosureActivity → 系统 ACCESSIBILITY_SETTINGS）的触发条件、按钮分支、同意状态持久化与跳转 Intent 均静态可见。仅 A0.b.f0 外链 URL 的具体目标未展开核验，不影响引导流程判定。",
  "summary_one_liner": "用户在设置页主动点击“Open accessibility settings”时，应用先用原生 DisclosureActivity 逐条披露截屏/元素位置读取范围并给出“No thanks”退出路径，同意后才一次性跳转系统无障碍设置页，未开启时仅 Toast 提示原因，无遮罩、无拒权循环。",
  "disguise_identity": {
    "app_display_name": "Circle to Share",
    "claimed_brand_or_persona": "Circle to Share（F-Droid 开源截屏裁剪分享工具，自述非无障碍工具、无网络权限）",
    "a11y_service_label": "Circle to Share",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。代码经 R8 混淆（T0.s/T0.t/T0.e 等短类名），但属常规编译优化；显示名、无障碍服务标签、说明文案三者一致，无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "eu.woshicado.circletoshare.MainActivity（主题 Theme.CircleToShare 的设置页）",
      "trigger_event": "onCreate() 绑定各控件；onStart() 注册 enabled_accessibility_services / voice_interaction_service / voice_recognition_service 的 ContentObserver",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "status_accessibility 状态行文案由 z() 动态填充（如 error_accessibility_stale: \"The accessibility fallback is switched on but not running. Switch it off and on again under Settings → Accessibility.\"）",
      "shown_text_zh": "冷启动不弹任何说明或权限弹窗，仅在设置页状态卡上显示无障碍/助手/磁贴的真实开启状态；无障碍未开启时显示对应状态提示文字。",
      "user_action_requested": "无强制操作；页面提供 Open accessibility settings / Open assistant settings / Add Quick Settings tile / Open language settings 等按钮及多个功能开关，用户可自由忽略。",
      "code_anchor": "eu.woshicado.circletoshare.MainActivity.onCreate / onStart / z"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "eu.woshicado.circletoshare.DisclosureActivity（原生说明页，layout 2131427356）",
      "trigger_event": "用户点击 btn_accessibility_settings（T0.s.onClick case 7）且 cts.a11y_consent 为 false → ActivityResultLauncher G 启动 DisclosureActivity；另在服务已开启但未记录同意时由 MainActivity.z() 经 Launcher H 补发一次",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Before you turn on the accessibility service / Circle to Share uses Android's Accessibility API (AccessibilityService) to capture your screen when you ask it to... It is not an accessibility tool. Nothing it accesses is collected by, sent to, or shared with the developer or anyone else. / Tap Agree to allow this. You then switch the service on in Android's accessibility settings, and can switch it off there at any time. Tap No thanks to keep using Circle to Share with the assistant gesture only.",
      "shown_text_zh": "“在你开启无障碍服务之前”：说明应用用 AccessibilityService 在你主动触发时截屏，它不是无障碍工具，所访问内容不会被收集或发送给开发者；点 Agree 后你再到系统无障碍设置里开启，并可随时关闭；点 No thanks 可继续仅用助手手势，磁贴、悬浮球与吸附功能保持关闭。",
      "user_action_requested": "三选一：Agree（写入 cts.a11y_consent=true 并返回 RESULT_OK）、No thanks（setResult(0) 直接 finish，无二次打扰）、或点击正文链接了解详情；均有明确取消/跳过按钮。",
      "code_anchor": "eu.woshicado.circletoshare.DisclosureActivity.onCreate + T0.e.onClick；res/values/strings.xml disclosure_title/disclosure_lead/disclosure_choice_body"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings 无障碍页（android.settings.ACCESSIBILITY_SETTINGS），用户需在列表中找到服务项 Circle to Share",
      "trigger_event": "DisclosureActivity 返回 RESULT_OK → 启动器回调 T0.t.b() 执行 mainActivity.s(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))；已同意用户则由 T0.s.onClick case 7 直接跳转",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Open accessibility settings（按钮文案）；系统列表项显示 label \"Circle to Share\"，详情描述为 accessibility_service_description 全文",
      "shown_text_zh": "点击“打开无障碍设置”后进入系统无障碍设置页；列表中以“Circle to Share”为名展示，点开可见完整披露说明。全程为系统原生页面，应用不叠加任何遮罩或仿冒开关。",
      "user_action_requested": "用户在系统页面内自行选择 Circle to Share 并开启开关（系统会再次弹出自身的权限确认）；应用无法代为点击。",
      "code_anchor": "T0.s.onClick case 7 / T0.t.b；res/values/strings.xml btn_accessibility_settings；res/xml/accessibility_service_config.xml"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 设置页开关（MaterialSwitch）与 Toast",
      "trigger_event": "用户返回应用后尝试操作依赖无障碍的功能（如磁贴开关 u.onCheckedChanged → MainActivity.t(CompoundButton)），或状态刷新 z()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Toast: ScreenshotAccessibilityService.Companion.whyNotRunning(context) 对应文案（如 \"Enable the accessibility fallback (step 2) first.\" / \"Open Circle to Share and agree to the accessibility disclosure first.\"）；状态行 error_needs_accessibility",
      "shown_text_zh": "若仍未开启，开关自动回弹为关闭并 Toast 说明具体原因（如“请先在应用内同意无障碍披露”“请先开启无障碍回退”），停留在当前页，不自动重跳设置页。",
      "user_action_requested": "用户可再次主动点击按钮前往设置，或直接放弃该功能；无强制、无循环拉起。",
      "code_anchor": "eu.woshicado.circletoshare.MainActivity.t / z；res/values/strings.xml error_needs_accessibility / error_needs_consent"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "ScreenshotAccessibilityService（无障碍服务）与悬浮球/磁贴",
      "trigger_event": "服务开启后 MainActivity.onStart 的 ContentObserver 触发 z() 刷新状态；DisclosureActivity Agree 分支调用 ScreenshotAccessibilityService.Companion.applyBubbleState()；用户点“Add Quick Settings tile”走 StatusBarManager.requestAddTileService()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "disclosure_use_body: \"• Everything is processed on this device, in memory, to show you the crop tool. ... • An image leaves Circle to Share only when you tap Share or Copy... The app has no internet permission. • The service never taps, types or changes settings for you.\"",
      "shown_text_zh": "获权后仅在本地内存处理截图、显示裁剪工具；仅当用户点 Share/Copy/Save 才写出图片；应用无网络权限；服务不会代替用户点击或更改设置（仅收起通知栏与实验性滚动截屏手势两项动作）。",
      "user_action_requested": "用户后续通过助手手势 / 磁贴 / 悬浮球主动触发截屏；磁贴添加需在系统弹窗中确认。",
      "code_anchor": "ScreenshotAccessibilityService.Companion.applyBubbleState / MainActivity.z / T0.s.onClick case 9；res/values/strings.xml disclosure_use_body"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 设置页内嵌状态卡（TextView 2131231176/2131231177/2131231143 等），显示无障碍与助手开关的真实状态及错误提示（strings.xml status_* / error_*）",
    "DisclosureActivity 原生 Activity 说明页（layout 2131427356）：标题 disclosure_title、导语 disclosure_lead、What it accesses（disclosure_access_body）、How it is used（disclosure_use_body）、Your choice（disclosure_choice_body），底部 Agree / No thanks 按钮",
    "系统无障碍设置列表项名称 accessibility_service_label = \"Circle to Share\"，详情页描述 accessibility_service_description（长段透明披露）",
    "操作失败时的 Toast（ScreenshotAccessibilityService.Companion.whyNotRunning、Toast 2131755125/2131755126）",
    "设置页按钮文案：Open accessibility settings / Open assistant settings / Add Quick Settings tile / Open language settings（strings.xml btn_*）",
    "未出现任何 WebView、assets HTML、悬浮窗遮罩或伪造系统设置页承载引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Lets Circle to Share capture the screen when you trigger it with the assistant gesture, the Quick Settings tile, or the app's floating button. You can then crop and share it. Screen content (element positions) is read only at the moment of capture, and only to align the crop box with what's on screen; if enabled in the app. Nothing is captured until you trigger it, nothing is saved to your device unless you tap Save, and nothing ever leaves it.",
      "text_zh": "Circle to Share 仅在你通过助手手势、快捷设置磁贴或应用悬浮按钮触发时截取屏幕，随后你可裁剪并分享。屏幕内容（元素位置）仅在截屏瞬间读取，且仅用于让裁剪框对齐屏幕内容（如应用内已启用）。未触发前不截取任何内容，未点保存不写入设备，任何内容都不会外传。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（系统无障碍详情页展示）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Circle to Share uses Android's Accessibility API (AccessibilityService) to capture your screen when you ask it to: from the Quick Settings tile, the floating button, or as a fallback for the assistant gesture. It is not an accessibility tool. Nothing it accesses is collected by, sent to, or shared with the developer or anyone else.",
      "text_zh": "Circle to Share 使用 Android 无障碍 API（AccessibilityService）在你主动请求时截屏：来自快捷设置磁贴、悬浮按钮，或作为助手手势的回退方案。它不是无障碍工具。它访问的任何内容都不会被收集、发送或共享给开发者或任何其他人。",
      "source_location": "res/values/strings.xml key=disclosure_lead（DisclosureActivity 页首）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Tap Agree to allow this. You then switch the service on in Android's accessibility settings, and can switch it off there at any time.\n\nTap No thanks to keep using Circle to Share with the assistant gesture only. The tile, the floating button and snapping stay off, and a service that is already on is switched off.",
      "text_zh": "点“同意”即允许上述内容，随后你到 Android 无障碍设置中开启该服务，并可随时在那里关闭。点“不用了”则可继续仅通过助手手势使用 Circle to Share；磁贴、悬浮按钮与吸附功能保持关闭，已开启的服务也会被关闭。",
      "source_location": "res/values/strings.xml key=disclosure_choice_body（DisclosureActivity “Your choice” 段）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "• A screenshot of your screen at the moment you trigger a capture.\n\n• The positions and sizes of the elements on screen (not their text or content) at that same moment, and only while \"Snap to screen content\" is switched on.\n\n• Notices from the system that a window has opened or changed, with the window's title and the app it belongs to, and the positions of system windows to recognize the lock screen, the power menu and the notification shade, so the floating button and the crop tool get out of their way.",
      "text_zh": "• 你触发截屏瞬间的屏幕截图。• 同一时刻屏幕上元素的位置与大小（不含其文字或内容），且仅在“吸附到屏幕内容”开启时读取。• 系统窗口打开/变化的通知，含窗口标题与所属应用，以及系统窗口位置，用于识别锁屏、电源菜单和通知栏，以便悬浮按钮与裁剪工具避让。",
      "source_location": "res/values/strings.xml key=disclosure_access_body（DisclosureActivity “What it accesses” 段）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "• Everything is processed on this device, in memory, to show you the crop tool. ... • An image leaves Circle to Share only when you tap Share or Copy, and only to the app you choose, or when you tap Save, which puts it in your gallery (below Screenshots). The app has no internet permission. • The service never taps, types or changes settings for you. Its only two actions are (1) closing the notification shade when you use the Quick Settings tile; (2) simulating a swipe gesture when using the (experimental) scrollshot feature.",
      "text_zh": "• 一切均在本机内存中处理以显示裁剪工具。……• 仅当你点分享/复制（且仅发给你选择的应用）或点保存（存入图库 Screenshots 目录）时图片才离开应用；应用无网络权限。• 服务绝不代替你点击、输入或更改设置，仅有两种动作：(1) 使用磁贴时收起通知栏；(2) 使用（实验性）滚动截屏时模拟滑动手势。",
      "source_location": "res/values/strings.xml key=disclosure_use_body（DisclosureActivity “How it is used” 段）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Open accessibility settings",
      "text_zh": "打开无障碍设置",
      "source_location": "res/values/strings.xml key=btn_accessibility_settings（MainActivity 按钮）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable the accessibility fallback (step 2) first.",
      "text_zh": "请先开启无障碍回退（第 2 步）。",
      "source_location": "res/values/strings.xml key=error_needs_accessibility（功能未开启时的 Toast）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。DisclosureActivity 的 No thanks 分支 setResult(0)+finish() 后直接回到设置页；用户未开启时操作相关开关仅 setChecked(false) 并 Toast 说明原因，不自动重跳系统设置；MainActivity.z() 用 I 标志位与 cts.a11y_consent 双重条件保证说明页至多补发一次。",
    "overlay_or_fake_settings": "无。全部引导位于本应用原生 Activity 与系统原生设置页，未使用 SYSTEM_ALERT_WINDOW 遮罩、未绘制高仿无障碍开关页。",
    "restricted_settings_13plus_coaching": "无。代码中未见 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、右上角菜单受限设置教学或 Session 安装器绕过路径。",
    "post_grant_anti_removal": "无。未发现获权后自点确认、自授权，或监听设置页以 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；onStart 的 ContentObserver 仅用于回读状态刷新 UI。",
    "benign_graceful_degradation": "有。No thanks 后保留“仅助手手势”路径（需设为助手应用，走 VOICE_INPUT_SETTINGS/MANAGE_DEFAULT_APPS_SETTINGS 引导），磁贴、悬浮球与吸附功能关闭；已开启的服务也会被主动关闭，文案与代码一致。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到前台由 eu.woshicado.circletoshare.MainActivity 切换到 eu.woshicado.circletoshare.DisclosureActivity（首次点击“Open accessibility settings”或服务已开启但未记录同意时由 onTopResumedActivityChanged 补发），以及随后由 DisclosureActivity finish 触发的 android.settings.ACCESSIBILITY_SETTINGS 跳转瞬间。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动设置页（判断是否存在强制弹窗/遮罩）",
        "page_identifier": "Activity=eu.woshicado.circletoshare.MainActivity，布局含 Open accessibility settings / Open assistant settings / Add Quick Settings tile 按钮与 status_accessibility 状态行",
        "why_most_useful": "确认冷启动无强制引导、无叠加遮罩，是无障碍诱导审计的首要排除项",
        "observable_utg_signals": ["是否存在覆盖系统或应用界面的悬浮窗节点", "是否存在除 MainActivity 之外的弹窗/对话框窗口层级", "状态行文本是否为真实系统开关状态"]
      },
      {
        "page_role": "跳转前原生披露说明页",
        "page_identifier": "Activity=eu.woshicado.circletoshare.DisclosureActivity，标题“Before you turn on the accessibility service”，底部 Agree / No thanks 两个按钮",
        "why_most_useful": "这是区分“透明披露”与“伪装话术”的关键页：可直接比对文案是否谎称安全/故障/更新，以及是否提供可点击的取消按钮",
        "observable_utg_signals": ["页面文本是否包含 It is not an accessibility tool / No thanks 等透明与取消要素", "No thanks 按钮是否真实可点且非禁用", "页面是否为原生 Activity 而非 WebView（无 WebView 节点）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中标签为 Circle to Share 的服务项，详情描述为长段 accessibility_service_description",
        "why_most_useful": "核对系统层暴露的服务名与描述是否与应用自述一致、是否借用系统品牌或伪造 isAccessibilityTool",
        "observable_utg_signals": ["服务项 label 文本", "描述文本是否与 strings.xml accessibility_service_description 一致", "是否存在额外可疑服务项或重复条目"]
      },
      {
        "page_role": "拒权返回后的应用页",
        "page_identifier": "MainActivity 恢复前台 + Toast 文本（whyNotRunning / error_needs_accessibility）",
        "why_most_useful": "验证拒权后是否出现自动重跳设置页的死循环或遮罩压迫",
        "observable_utg_signals": ["是否再次自动进入 ACCESSIBILITY_SETTINGS", "Toast 文案内容", "开关是否回弹为关闭"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。引导文案全部为可提取的文本节点（原生 TextView / 系统设置页），未使用纯图引导、GIF 教学或远端 HTML。边界：说明页正文中的“了解更多”链接由 A0.b.f0 打开，其目标 URL 未展开核验；若需完全排除外链导向远端页面，需补一次该 URL 的动态抓取。"
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
    "eu.woshicado.circletoshare.MainActivity.onTopResumedActivityChanged",
    "eu.woshicado.circletoshare.MainActivity.z",
    "T0.s.onClick",
    "T0.t.b",
    "T0.e.onClick",
    "res/values/strings.xml（disclosure_lead / disclosure_choice_body / disclosure_use_body / accessibility_service_description）"
  ]
}
```

</details>
