# MB_020__f4d7e9ec4e｜Vultur — Protection Guard

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：81.5s

## 1. 一句话核心结论

- **核心申请方式**：以“Protection Guard 安全防护”为名的伪安全工具，用不可取消弹窗 + 每约15秒强制重跳系统无障碍设置 + 取消即重拉服务的死循环，逼迫用户开启 AcService 无障碍服务，授权后自点确认并连按 HOME 防撤权。
- **静态可见性说明**：本地引导链（不可取消 AlertDialog、强制循环跳 ACTION_ACCESSIBILITY_SETTINGS、AwesomeDialogActivity 取消即重拉、全屏意图通知、无障碍描述）全部静态可见；唯 WebViewActivity 展示的教学 HTML 取自 SharedPreferences 的 config:dialog:html，由 FCM MessagingService 远端下发，静态包内不存在该文本，属远端可替换内容。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `f4d7e9ec4eda034c29b8d73d479084658858f56e67909c2ffedf9223d7ca9bd2` |
| 包名 / 年份 | `com.appsmastersafey` / 2025 |
| 家族 / 品类 | **Vultur**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Protection Guard |
| 引导页宣称品牌/身份 | Protection Guard 手机安全防护/防第三方篡改工具 |
| 系统无障碍列表服务名 | Protection Guard |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未设独立 label，直接复用 app_name，使系统无障碍列表显示与桌面名一致；description 用 ENG/IT/NL/FR 四语种重复堆砌拉长文本；关键提示文案（"Please enable "、"  service"、"Settings"、"AccessibilityRequestService::doWork"）以 char[] 数组逐字符拼接规避静态字符串扫描；类名大面积混淆为 a.a.a.*；无空白/换行挤出、无同形字、无多 activity-alias、未伪造 isAccessibilityTool |
| 无障碍服务类名 | `com.appsmastersafey.lib.AcService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `RECORD_AUDIO, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | === ENG<br> We are very sensitive for your safety, this service check your phone parameters from third party changes<br><br> === IT<br> Siamo molto sensibili per la tua sicurezza, questo servizio controlla i parametri del tuo telefono da modifiche di terze parti<br><br> === NL<br> We zijn erg gevoelig voor uw veiligheid, deze service controleert de parameters van uw telefoon tegen wijzigingen van derden<br><br> === FR<br> Nous sommes très sensibles pour votre sécurité, ce service vérifie les paramètres de votre téléphone contre les changements de tiers |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.appsmastersafey.MainActivity（Theme.Translucent 启动器入口） | LAUNCHER 启动 → onCreate；若无障碍已开启或 a11y=true，onResume 直接 finish | 原生Activity | 无 | 无（不要求任何操作） | `com.appsmastersafey.MainActivity.onCreate / MainActivity.onResume` |
| 2 | 业务功能触发 | com.appsmastersafey.bot.AccessibilityRequestActivity / WebViewService / VncService（后台或远端拉起） | FCM 下发（MessagingService 写入 config:dialog:html 并拉起 WebViewActivity/WebViewService）、VncService 连接后拉起请求页；AccessibilityRequestActivity.onCreate 按 action 分流 | 原生Activity | 无 | 无 | `com.appsmastersafey.bot.AccessibilityRequestActivity.onCreate / com.appsmastersafey.fcm.MessagingService.a` |
| 3 | 引导说明页 | AlertDialog（ContextThemeWrapper Theme.DeviceDefault.Light.Dialog.Alert） | AccessibilityRequestActivity.b() 在 onCreate 非 action 分支、以及 onPause/onStop 回到前台后调用 | 原生Dialog | **原文**：Title: Protection Guard \| Message: Please enable Protection Guard  service \| Button: Settings<br>**译注**：标题“Protection Guard”，正文“请启用 Protection Guard 服务”，唯一按钮“设置” | 只能点“设置”；setCancelable(false)，无取消、无跳过、返回键离页仍会重弹 | `com.appsmastersafey.bot.AccessibilityRequestActivity.b` |
| 4 | 跳无障碍设置 | 系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS | 点击“Settings” → AccessibilityRequestActivity.a() → startService(AccessibilityRequestService)；服务线程每 counter%30==0 再次 startActivity(ACCESSIBILITY_SETTINGS) | 系统无障碍页 | **原文**：无（跳转系统页面）<br>**译注**：跳转到系统无障碍服务列表，要求用户在其中找到并开启 “Protection Guard” | 在系统列表中手动找到 “Protection Guard” 并打开开关 | `com.appsmastersafey.bot.AccessibilityRequestService.a` |
| 5 | 拒权反馈循环 | AwesomeDialogActivity（Theme.AppCompat.Light.NoActionBar） | 循环中 counter % (config:dialog:timeout*2)==0（默认每约30秒）强制拉起；onCreate 检查 ACTION_SHOW 后执行 j() | 原生Dialog | **原文**：Action required \| Please enable Protection Guard service \| Open settings<br>**译注**：“需要您操作” / “请启用 Protection Guard 服务” / “打开设置” | 点“Open settings”跳设置；点按钮、点外部取消、切走（onPause）均触发 j() 重新 startService，形成取消即重拉的死循环 | `com.appsmastersafey.bot.AwesomeDialogActivity.i / AwesomeDialogActivity.j` |
| 6 | 遮罩叠层指引 | 常驻通知（NotificationChannel + setFullScreenIntent） | AccessibilityRequestService.a(int) 在 doWork 起始阶段 startForeground 发布，点击 contentIntent 直达无障碍设置 | 通知栏 | **原文**：Protection Guard \| Please enable Protection Guard  service<br>**译注**：通知标题“Protection Guard”，正文“请启用 Protection Guard 服务”，锁屏可直接全屏拉起设置页 | 点击通知跳转无障碍设置（无可忽略的替代动作） | `com.appsmastersafey.bot.AccessibilityRequestService.a(int)` |
| 7 | 引导说明页 | WebViewActivity（Theme.NoTitleBar，全屏 WebView） | WebViewService 通知（id 1235）或远端下发后拉起；onCreate → a() 读取 config:dialog:html 渲染 | 远端WebView | **原文**：（HTML 由 FCM 下发至 SharedPreferences key config:dialog:html，静态包内无原文；模板含 ${APP_NAME} 占位符，运行时替换为 Protection Guard）<br>**译注**：远端可随时替换的图文教学页，用于强化“必须开启服务”的话术；任意触摸即关闭并回到循环 | 阅读后触摸关闭，随即被重新拉回弹窗/设置页 | `com.appsmastersafey.bot.WebViewActivity.a / com.appsmastersafey.bot.WebViewService.b` |
| 8 | 获权后动作 | com.appsmastersafey.lib.AcService（AccessibilityService） | 用户在系统设置中开启服务 → onServiceConnected（eventTypes=-1、flags=80、写入 a11y=true）→ 后续 AccessibilityEvent 回调 | 不可静态还原 | 无 | 无（用户被动被自动点击与返回主页） | `com.appsmastersafey.lib.AcService.onServiceConnected / AcService.b / a.a.a.kh.a` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- AccessibilityRequestActivity.b() 弹出的 setCancelable(false) AlertDialog：标题 Protection Guard、正文 Please enable Protection Guard  service、按钮 Settings
- AwesomeDialogActivity.i() 构建的原生对话框：Action required / Please enable Protection Guard service / Open settings（取自 res/values/strings.xml 的 a11_request_title、a11_request_message、a11_request_button）
- AccessibilityRequestService.a(int) 发布的常驻/全屏意图通知：Protection Guard / Please enable Protection Guard  service
- WebViewService 通知（通知 id 1235）：Action required / Please enable … service，点击拉起 WebViewActivity
- WebViewActivity.a() 渲染的远端 HTML 页面（config:dialog:html，来自 FCM 下发，含 ${APP_NAME} 占位符），全屏展示
- 系统无障碍服务列表项的 android:description（res/values/strings.xml 的 accessibility_service_description，ENG/IT/NL/FR 四语种）与列表项名称（复用 app_name = Protection Guard）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Action required | 需要您操作 | `res/values/strings.xml key=a11_request_title（AwesomeDialogActivity.i 使用）` | 假反诈安全 |
| en | Please enable %1$s service | 请启用 %1$s 服务（运行时替换为 Protection Guard） | `res/values/strings.xml key=a11_request_message（AwesomeDialogActivity.i 使用）` | 假反诈安全 |
| en | Open settings | 打开设置 | `res/values/strings.xml key=a11_request_button（AwesomeDialogActivity.i 使用）` | 受限设置分步教学 |
| en | Please enable Protection Guard  service | 请启用 Protection Guard 服务 | `AccessibilityRequestActivity.b 硬编码 char[] 拼接；AccessibilityRequestService.a(int) 通知正文同样拼接` | 假反诈安全 |
| en | Protection Guard | Protection Guard（伪装的安全防护品牌名） | `res/values/strings.xml key=app_name（对话框标题、通知标题、无障碍服务列表名均复用）` | 假反诈安全 |
| en | === ENG<br> We are very sensitive for your safety, this service check your phone parameters from third party changes | === ENG 我们非常关注您的安全，本服务检查您的手机参数是否被第三方修改 | `res/values/strings.xml key=accessibility_service_description（经 res/xml/ac_config.xml android:description 引用）` | 假反诈安全 |
| it | === IT<br> Siamo molto sensibili per la tua sicurezza, questo servizio controlla i parametri del tuo telefono da modifiche di terze parti | === IT 我们非常关注您的安全，本服务检查您的手机参数是否被第三方修改 | `res/values/strings.xml key=accessibility_service_description` | 假反诈安全 |
| nl | === NL<br> We zijn erg gevoelig voor uw veiligheid, deze service controleert de parameters van uw telefoon tegen wijzigingen van derden | === NL 我们非常关注您的安全，本服务检查您的手机参数是否被第三方修改 | `res/values/strings.xml key=accessibility_service_description` | 假反诈安全 |
| fr | === FR<br> Nous sommes très sensibles pour votre sécurité, ce service vérifie les paramètres de votre téléphone contre les changements de tiers | === FR 我们非常关注您的安全，本服务检查您的手机参数是否被第三方修改 | `res/values/strings.xml key=accessibility_service_description` | 假反诈安全 |
| en | This update does not work correctly with the current version of Play Market and will be closed | 此更新无法在当前版本的 Play 商店上正常工作，将被关闭 | `res/values/strings.xml（预筛命中，本轮未确认调用点）` | 假更新 |
| en | %1$s won't work unless you enable Google Play services. | 除非您启用 Google Play 服务，否则 %1$s 无法工作 | `res/values/strings.xml（预筛命中，本轮未确认调用点）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：AccessibilityRequestService.a() 在 WakeLock 下 while(!kh.a(this)) 无限循环：每约15秒（counter%30==0）重新 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；每约30秒（counter%(config:dialog:timeout*2)==0）强制拉起 AwesomeDialogActivity；用户点取消/切走/返回触发 AwesomeDialogActivity.j() 或 AccessibilityRequestActivity.onPause/onStop 再次 startService，形成“取消→重拉→再弹”闭环；仅检测到无障碍已开启才 break。
- **遮罩叠层 / 高仿系统设置页**：未发现悬浮窗遮罩或高仿无障碍开关页；但使用 setFullScreenIntent 常驻通知在锁屏/前台全屏拉起设置跳转，并以 Theme.NoTitleBar 全屏 WebView 承载远端下发话术页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未发现 ACTION_APPLICATION_DETAILS_SETTINGS 的受限设置分步教学；预筛命中的 SESSION_INSTALLER 类字符串本轮未定位到针对该目标的实现，属覆盖边界）
- **获权后即时行为与防撤权机制**：是。AcService 获权后监听全量事件（eventTypes=-1、flags=80），在 com.android.settings / com.android.systemui / com.miui.securitycenter / 安装器等界面按应用名匹配节点并 performAction(16) 自动点击确认；同时以 performGlobalAction(GLOBAL_ACTION_HOME) 连按退出设置页，阻止用户返回撤权（依据已登记风险 R-001，本轮静态调用点复核一致）。
- **良性降级 / 替代方案**：无。不存在手动模式、仅观看模式或 ADB 等替代路径，未授权即无限循环施压。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：Hook 监测 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 调用（AccessibilityRequestService.a 内）作为拉起瞬间；同时监测 AwesomeDialogActivity 的 onCreate（ACTION_SHOW）与 AccessibilityRequestActivity.b 的 AlertDialog.show，在后台/远端拉起后 10–20 秒内必然出现上述任一页面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：(1) WebViewActivity 的话术 HTML 完全由 FCM 远端下发（config:dialog:html），静态包内无原文，且下发内容可按设备/时间变化，UTG 需在远端下发后才可捕获；(2) 引导链的初始触发来自后台/远端（FCM、VncService），纯冷启动 UTG 抓不到首弹，需在应用被远端唤醒后保持观测。静态加壳初判为 False，不构成运行期 UTG 阻碍。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/后台拉起后的不可取消引导弹窗页** | 包名 com.appsmastersafey 的 AccessibilityRequestActivity 之上的 AlertDialog，标题 Protection Guard、正文 Please enable Protection Guard  service、单按钮 Settings，无取消按钮且返回键无效 | 这是“无跳过路径”的直接物证：仅一个按钮且 setCancelable(false)，可证明用户被剥夺拒绝权 | 弹窗文本节点：Protection Guard / Please enable Protection Guard  service / Settings；当前 Activity 名 com.appsmastersafey.bot.AccessibilityRequestActivity；界面上不存在 Cancel/Not now/Skip/关闭 类控件 |
| **强制催促弹窗（循环期内每约30秒复现）** | AwesomeDialogActivity 对话框：Action required / Please enable Protection Guard service / Open settings | 可用于验证“拒绝后再次弹窗”的循环行为：捕获两次以上同页面出现即可确认 COERCE_REFUSAL_LOOP_RELAUNCH | 文本 Action required、Open settings；Activity 名 com.appsmastersafey.bot.AwesomeDialogActivity；同一会话内多次出现的时间间隔 |
| **跳转后的系统无障碍服务列表项** | 系统设置 com.android.settings 无障碍服务列表，条目名为 Protection Guard，描述为多语种“我们非常关注您的安全……”段落 | 直接核对伪装身份与服务名一致（identity_mismatch），并提取 android:description 实际渲染文本作为虚假安全承诺物证 | 条目文本 Protection Guard 与四语种描述段落；当前前台包名为 com.android.settings，且由应用主动跳转进入；列表条目开关初始为关闭状态 |
| **远端下发 HTML 教学页** | com.appsmastersafey.bot.WebViewActivity（Theme.NoTitleBar 全屏 WebView，无系统标题栏与地址栏） | 该页文本仅运行期由 FCM 下发，静态包内不存在，是唯一必须靠动态捕获才能取证的话术载体 | 全屏无标题栏 WebView 页面及其文本内容；页面出现应用名 Protection Guard 替换后的文案；触摸屏幕任意位置后页面立即消失 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.appsmastersafey.bot.AccessibilityRequestActivity.b`
- `com.appsmastersafey.bot.AccessibilityRequestActivity.a`
- `com.appsmastersafey.bot.AccessibilityRequestService.a`
- `com.appsmastersafey.bot.AwesomeDialogActivity.i`
- `com.appsmastersafey.bot.AwesomeDialogActivity.j`
- `res/values/strings.xml（a11_request_title / a11_request_message / a11_request_button / accessibility_service_description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

- **身份伪装**：桌面名 `Protection Guard`，无障碍服务 `AcService` 未设独立 label，直接复用 `app_name`，因此系统无障碍列表中同样显示 “Protection Guard”；`android:description` 用 ENG/IT/NL/FR 四语种重复堆砌“我们非常关注您的安全，本服务检查手机参数是否被第三方修改”，而实际配置 [ac_config.xml](<resource-unit:#1 file:res/xml/ac_config.xml#L2>) 声明 `typeAllMask`、`canRetrieveWindowContent="true"`、`canPerformGestures="true"`，与“参数检查”描述严重不符。包内另有 `lib.VncService`、`usc.ScreenRecordService`、`UnlockScreenCaptureActivity` 等远控/录屏组件。
- **不是冷启动直接弹窗**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.appsmastersafey.MainActivity#onCreate>) 仅 `setContentView` 后 `finish()`，`onResume` 在无障碍已开启或 `a11y=true` 时直接结束——启动器入口刻意“安静”，引导链由后台/远端拉起。
- **入口**：[AccessibilityRequestActivity.onCreate()](<resource-unit:#1.dex1 code:com.appsmastersafey.bot.AccessibilityRequestActivity#onCreate>) 在 action 匹配时直接 `startService(AccessibilityRequestService)` 并结束；否则调用 [b()](<resource-unit:#1.dex1 code:com.appsmastersafey.bot.AccessibilityRequestActivity#b>) 弹出 **`setCancelable(false)`** 的 AlertDialog：标题 `Protection Guard`、正文 `Please enable Protection Guard  service`（硬编码 char[] 拼接，注意双空格）、唯一按钮 `Settings`。点击后 [a()](<resource-unit:#1.dex1 code:com.appsmastersafey.bot.AccessibilityRequestActivity#a>) 启动请求服务；`onPause`/`onStop` 也调用同一方法，**用户按返回键离页同样重拉服务**。
- **强制循环**：[AccessibilityRequestService.a()](<resource-unit:#1.dex1 code:com.appsmastersafey.bot.AccessibilityRequestService#a>) 持有 `WakeLock`，`while (!kh.a(this))`（无障碍未启用即持续）循环，每轮 `sleep(500ms)`：
  - `counter % 30 == 0` → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`（约每 15 秒重跳一次系统无障碍页，flags `1956708352`）；
  - `counter % (timeout*2) == 0`（`config:dialog:timeout` 默认 30，约每 30 秒）→ 强制拉起 [AwesomeDialogActivity](<resource-unit:#1.dex1 code:com.appsmastersafey.bot.AwesomeDialogActivity#i>)；
  - `SDK_INT < 29` 时非跳转轮次仍持续跳设置页。循环仅以“无障碍被开启”为唯一出口，**无任何跳过/降级路径**。
- **弹窗闭环**：[AwesomeDialogActivity#i()](<resource-unit:#1.dex1 code:com.appsmastersafey.bot.AwesomeDialogActivity#i>) 用 `a11_request_title`=`Action required`、`a11_request_message`=`Please enable %1$s service`、`a11_request_button`=`Open settings` 组弹窗，并设 `setOnCancelListener` → [j()](<resource-unit:#1.dex1 code:com.appsmastersafey.bot.AwesomeDialogActivity#j>) → `startService(AccessibilityRequestService)` + `finish()`；`onPause` 亦走 `j()`。**取消/点按钮/切走三种动作都回到重拉服务**，形成“取消→再弹”死循环。
- **通知催促**：[AccessibilityRequestService.a(int)](<resource-unit:#1.dex1 code:com.appsmastersafey.bot.AccessibilityRequestService#a>) 以 `setFullScreenIntent(pendingIntent, true)` 构造常驻通知，标题 `Protection Guard`、正文 `Please enable Protection Guard  service`，点击即跳无障碍设置（锁屏可直接拉起）。
- **远端 HTML 话术页**：[WebViewActivity.a()](<resource-unit:#1.dex1 code:com.appsmastersafey.bot.WebViewActivity#a>) 从 `SharedPreferences` 的 `config:dialog:html` 读取 HTML、替换 `${APP_NAME}` 后 `loadData` 渲染（`setJavaScriptEnabled(true)`），**该 HTML 由 FCM 下发写入，静态不可见**；页面任意触摸即 `finish()`，配合 `WebViewService` 通知（id 1235，`Action required` / `Please enable … service`）二次催促。
- **获权后**：`AcService#onServiceConnected` 以 `eventTypes=-1`、`flags=80` 接管（已确认风险 R-001 记载），`AcService#b(event)` 对 `com.android.settings`、`com.android.systemui`、`com.miui.securitycenter` 等界面按应用名匹配节点并 `performAction(16)` 自动点击，配合 `performGlobalAction(GLOBAL_ACTION_HOME)` 退出设置页以**防止撤权**（本轮静态调用点复核一致）。
- **Android 13+ 受限设置**：未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 的受限设置分步教学或 `PackageInstaller` 会话绕过路径，该维度属覆盖边界。

---

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "本地引导链（不可取消 AlertDialog、强制循环跳 ACTION_ACCESSIBILITY_SETTINGS、AwesomeDialogActivity 取消即重拉、全屏意图通知、无障碍描述）全部静态可见；唯 WebViewActivity 展示的教学 HTML 取自 SharedPreferences 的 config:dialog:html，由 FCM MessagingService 远端下发，静态包内不存在该文本，属远端可替换内容。",
  "summary_one_liner": "以“Protection Guard 安全防护”为名的伪安全工具，用不可取消弹窗 + 每约15秒强制重跳系统无障碍设置 + 取消即重拉服务的死循环，逼迫用户开启 AcService 无障碍服务，授权后自点确认并连按 HOME 防撤权。",
  "disguise_identity": {
    "app_display_name": "Protection Guard",
    "claimed_brand_or_persona": "Protection Guard 手机安全防护/防第三方篡改工具",
    "a11y_service_label": "Protection Guard",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未设独立 label，直接复用 app_name，使系统无障碍列表显示与桌面名一致；description 用 ENG/IT/NL/FR 四语种重复堆砌拉长文本；关键提示文案（\"Please enable \"、\"  service\"、\"Settings\"、\"AccessibilityRequestService::doWork\"）以 char[] 数组逐字符拼接规避静态字符串扫描；类名大面积混淆为 a.a.a.*；无空白/换行挤出、无同形字、无多 activity-alias、未伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.appsmastersafey.MainActivity（Theme.Translucent 启动器入口）",
      "trigger_event": "LAUNCHER 启动 → onCreate；若无障碍已开启或 a11y=true，onResume 直接 finish",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "启动器入口不展示任何内容，透明主题，加载布局后立即结束，刻意保持“安静”",
      "user_action_requested": "无（不要求任何操作）",
      "code_anchor": "com.appsmastersafey.MainActivity.onCreate / MainActivity.onResume"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.appsmastersafey.bot.AccessibilityRequestActivity / WebViewService / VncService（后台或远端拉起）",
      "trigger_event": "FCM 下发（MessagingService 写入 config:dialog:html 并拉起 WebViewActivity/WebViewService）、VncService 连接后拉起请求页；AccessibilityRequestActivity.onCreate 按 action 分流",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台链路静默拉起引导页，无本地固定文案",
      "user_action_requested": "无",
      "code_anchor": "com.appsmastersafey.bot.AccessibilityRequestActivity.onCreate / com.appsmastersafey.fcm.MessagingService.a"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "AlertDialog（ContextThemeWrapper Theme.DeviceDefault.Light.Dialog.Alert）",
      "trigger_event": "AccessibilityRequestActivity.b() 在 onCreate 非 action 分支、以及 onPause/onStop 回到前台后调用",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: Protection Guard | Message: Please enable Protection Guard  service | Button: Settings",
      "shown_text_zh": "标题“Protection Guard”，正文“请启用 Protection Guard 服务”，唯一按钮“设置”",
      "user_action_requested": "只能点“设置”；setCancelable(false)，无取消、无跳过、返回键离页仍会重弹",
      "code_anchor": "com.appsmastersafey.bot.AccessibilityRequestActivity.b"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "点击“Settings” → AccessibilityRequestActivity.a() → startService(AccessibilityRequestService)；服务线程每 counter%30==0 再次 startActivity(ACCESSIBILITY_SETTINGS)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转系统页面）",
      "shown_text_zh": "跳转到系统无障碍服务列表，要求用户在其中找到并开启 “Protection Guard”",
      "user_action_requested": "在系统列表中手动找到 “Protection Guard” 并打开开关",
      "code_anchor": "com.appsmastersafey.bot.AccessibilityRequestService.a"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "AwesomeDialogActivity（Theme.AppCompat.Light.NoActionBar）",
      "trigger_event": "循环中 counter % (config:dialog:timeout*2)==0（默认每约30秒）强制拉起；onCreate 检查 ACTION_SHOW 后执行 j()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Action required | Please enable Protection Guard service | Open settings",
      "shown_text_zh": "“需要您操作” / “请启用 Protection Guard 服务” / “打开设置”",
      "user_action_requested": "点“Open settings”跳设置；点按钮、点外部取消、切走（onPause）均触发 j() 重新 startService，形成取消即重拉的死循环",
      "code_anchor": "com.appsmastersafey.bot.AwesomeDialogActivity.i / AwesomeDialogActivity.j"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "常驻通知（NotificationChannel + setFullScreenIntent）",
      "trigger_event": "AccessibilityRequestService.a(int) 在 doWork 起始阶段 startForeground 发布，点击 contentIntent 直达无障碍设置",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Protection Guard | Please enable Protection Guard  service",
      "shown_text_zh": "通知标题“Protection Guard”，正文“请启用 Protection Guard 服务”，锁屏可直接全屏拉起设置页",
      "user_action_requested": "点击通知跳转无障碍设置（无可忽略的替代动作）",
      "code_anchor": "com.appsmastersafey.bot.AccessibilityRequestService.a(int)"
    },
    {
      "step": 7,
      "stage": "引导说明页",
      "screen_or_component": "WebViewActivity（Theme.NoTitleBar，全屏 WebView）",
      "trigger_event": "WebViewService 通知（id 1235）或远端下发后拉起；onCreate → a() 读取 config:dialog:html 渲染",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "（HTML 由 FCM 下发至 SharedPreferences key config:dialog:html，静态包内无原文；模板含 ${APP_NAME} 占位符，运行时替换为 Protection Guard）",
      "shown_text_zh": "远端可随时替换的图文教学页，用于强化“必须开启服务”的话术；任意触摸即关闭并回到循环",
      "user_action_requested": "阅读后触摸关闭，随即被重新拉回弹窗/设置页",
      "code_anchor": "com.appsmastersafey.bot.WebViewActivity.a / com.appsmastersafey.bot.WebViewService.b"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.appsmastersafey.lib.AcService（AccessibilityService）",
      "trigger_event": "用户在系统设置中开启服务 → onServiceConnected（eventTypes=-1、flags=80、写入 a11y=true）→ 后续 AccessibilityEvent 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后静默接管：监听全量事件，在系统设置/SystemUI/小米安全中心/安装器等界面按应用名匹配节点并自动点击确认，并用 GLOBAL_ACTION_HOME 连按退出设置页，阻止用户撤权",
      "user_action_requested": "无（用户被动被自动点击与返回主页）",
      "code_anchor": "com.appsmastersafey.lib.AcService.onServiceConnected / AcService.b / a.a.a.kh.a"
    }
  ],
  "text_presentation_locations": [
    "AccessibilityRequestActivity.b() 弹出的 setCancelable(false) AlertDialog：标题 Protection Guard、正文 Please enable Protection Guard  service、按钮 Settings",
    "AwesomeDialogActivity.i() 构建的原生对话框：Action required / Please enable Protection Guard service / Open settings（取自 res/values/strings.xml 的 a11_request_title、a11_request_message、a11_request_button）",
    "AccessibilityRequestService.a(int) 发布的常驻/全屏意图通知：Protection Guard / Please enable Protection Guard  service",
    "WebViewService 通知（通知 id 1235）：Action required / Please enable … service，点击拉起 WebViewActivity",
    "WebViewActivity.a() 渲染的远端 HTML 页面（config:dialog:html，来自 FCM 下发，含 ${APP_NAME} 占位符），全屏展示",
    "系统无障碍服务列表项的 android:description（res/values/strings.xml 的 accessibility_service_description，ENG/IT/NL/FR 四语种）与列表项名称（复用 app_name = Protection Guard）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Action required",
      "text_zh": "需要您操作",
      "source_location": "res/values/strings.xml key=a11_request_title（AwesomeDialogActivity.i 使用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enable %1$s service",
      "text_zh": "请启用 %1$s 服务（运行时替换为 Protection Guard）",
      "source_location": "res/values/strings.xml key=a11_request_message（AwesomeDialogActivity.i 使用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Open settings",
      "text_zh": "打开设置",
      "source_location": "res/values/strings.xml key=a11_request_button（AwesomeDialogActivity.i 使用）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enable Protection Guard  service",
      "text_zh": "请启用 Protection Guard 服务",
      "source_location": "AccessibilityRequestActivity.b 硬编码 char[] 拼接；AccessibilityRequestService.a(int) 通知正文同样拼接",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Protection Guard",
      "text_zh": "Protection Guard（伪装的安全防护品牌名）",
      "source_location": "res/values/strings.xml key=app_name（对话框标题、通知标题、无障碍服务列表名均复用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "=== ENG\n We are very sensitive for your safety, this service check your phone parameters from third party changes",
      "text_zh": "=== ENG 我们非常关注您的安全，本服务检查您的手机参数是否被第三方修改",
      "source_location": "res/values/strings.xml key=accessibility_service_description（经 res/xml/ac_config.xml android:description 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "it",
      "text_verbatim": "=== IT\n Siamo molto sensibili per la tua sicurezza, questo servizio controlla i parametri del tuo telefono da modifiche di terze parti",
      "text_zh": "=== IT 我们非常关注您的安全，本服务检查您的手机参数是否被第三方修改",
      "source_location": "res/values/strings.xml key=accessibility_service_description",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "nl",
      "text_verbatim": "=== NL\n We zijn erg gevoelig voor uw veiligheid, deze service controleert de parameters van uw telefoon tegen wijzigingen van derden",
      "text_zh": "=== NL 我们非常关注您的安全，本服务检查您的手机参数是否被第三方修改",
      "source_location": "res/values/strings.xml key=accessibility_service_description",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "fr",
      "text_verbatim": "=== FR\n Nous sommes très sensibles pour votre sécurité, ce service vérifie les paramètres de votre téléphone contre les changements de tiers",
      "text_zh": "=== FR 我们非常关注您的安全，本服务检查您的手机参数是否被第三方修改",
      "source_location": "res/values/strings.xml key=accessibility_service_description",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "This update does not work correctly with the current version of Play Market and will be closed",
      "text_zh": "此更新无法在当前版本的 Play 商店上正常工作，将被关闭",
      "source_location": "res/values/strings.xml（预筛命中，本轮未确认调用点）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "除非您启用 Google Play 服务，否则 %1$s 无法工作",
      "source_location": "res/values/strings.xml（预筛命中，本轮未确认调用点）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "AccessibilityRequestService.a() 在 WakeLock 下 while(!kh.a(this)) 无限循环：每约15秒（counter%30==0）重新 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；每约30秒（counter%(config:dialog:timeout*2)==0）强制拉起 AwesomeDialogActivity；用户点取消/切走/返回触发 AwesomeDialogActivity.j() 或 AccessibilityRequestActivity.onPause/onStop 再次 startService，形成“取消→重拉→再弹”闭环；仅检测到无障碍已开启才 break。",
    "overlay_or_fake_settings": "未发现悬浮窗遮罩或高仿无障碍开关页；但使用 setFullScreenIntent 常驻通知在锁屏/前台全屏拉起设置跳转，并以 Theme.NoTitleBar 全屏 WebView 承载远端下发话术页。",
    "restricted_settings_13plus_coaching": "无（未发现 ACTION_APPLICATION_DETAILS_SETTINGS 的受限设置分步教学；预筛命中的 SESSION_INSTALLER 类字符串本轮未定位到针对该目标的实现，属覆盖边界）",
    "post_grant_anti_removal": "是。AcService 获权后监听全量事件（eventTypes=-1、flags=80），在 com.android.settings / com.android.systemui / com.miui.securitycenter / 安装器等界面按应用名匹配节点并 performAction(16) 自动点击确认；同时以 performGlobalAction(GLOBAL_ACTION_HOME) 连按退出设置页，阻止用户返回撤权（依据已登记风险 R-001，本轮静态调用点复核一致）。",
    "benign_graceful_degradation": "无。不存在手动模式、仅观看模式或 ADB 等替代路径，未授权即无限循环施压。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "Hook 监测 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 调用（AccessibilityRequestService.a 内）作为拉起瞬间；同时监测 AwesomeDialogActivity 的 onCreate（ACTION_SHOW）与 AccessibilityRequestActivity.b 的 AlertDialog.show，在后台/远端拉起后 10–20 秒内必然出现上述任一页面。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/后台拉起后的不可取消引导弹窗页",
        "page_identifier": "包名 com.appsmastersafey 的 AccessibilityRequestActivity 之上的 AlertDialog，标题 Protection Guard、正文 Please enable Protection Guard  service、单按钮 Settings，无取消按钮且返回键无效",
        "why_most_useful": "这是“无跳过路径”的直接物证：仅一个按钮且 setCancelable(false)，可证明用户被剥夺拒绝权",
        "observable_utg_signals": [
          "弹窗文本节点：Protection Guard / Please enable Protection Guard  service / Settings",
          "当前 Activity 名 com.appsmastersafey.bot.AccessibilityRequestActivity",
          "界面上不存在 Cancel/Not now/Skip/关闭 类控件"
        ]
      },
      {
        "page_role": "强制催促弹窗（循环期内每约30秒复现）",
        "page_identifier": "AwesomeDialogActivity 对话框：Action required / Please enable Protection Guard service / Open settings",
        "why_most_useful": "可用于验证“拒绝后再次弹窗”的循环行为：捕获两次以上同页面出现即可确认 COERCE_REFUSAL_LOOP_RELAUNCH",
        "observable_utg_signals": [
          "文本 Action required、Open settings",
          "Activity 名 com.appsmastersafey.bot.AwesomeDialogActivity",
          "同一会话内多次出现的时间间隔"
        ]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "系统设置 com.android.settings 无障碍服务列表，条目名为 Protection Guard，描述为多语种“我们非常关注您的安全……”段落",
        "why_most_useful": "直接核对伪装身份与服务名一致（identity_mismatch），并提取 android:description 实际渲染文本作为虚假安全承诺物证",
        "observable_utg_signals": [
          "条目文本 Protection Guard 与四语种描述段落",
          "当前前台包名为 com.android.settings，且由应用主动跳转进入",
          "列表条目开关初始为关闭状态"
        ]
      },
      {
        "page_role": "远端下发 HTML 教学页",
        "page_identifier": "com.appsmastersafey.bot.WebViewActivity（Theme.NoTitleBar 全屏 WebView，无系统标题栏与地址栏）",
        "why_most_useful": "该页文本仅运行期由 FCM 下发，静态包内不存在，是唯一必须靠动态捕获才能取证的话术载体",
        "observable_utg_signals": [
          "全屏无标题栏 WebView 页面及其文本内容",
          "页面出现应用名 Protection Guard 替换后的文案",
          "触摸屏幕任意位置后页面立即消失"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：(1) WebViewActivity 的话术 HTML 完全由 FCM 远端下发（config:dialog:html），静态包内无原文，且下发内容可按设备/时间变化，UTG 需在远端下发后才可捕获；(2) 引导链的初始触发来自后台/远端（FCM、VncService），纯冷启动 UTG 抓不到首弹，需在应用被远端唤醒后保持观测。静态加壳初判为 False，不构成运行期 UTG 阻碍。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.appsmastersafey.bot.AccessibilityRequestActivity.b",
    "com.appsmastersafey.bot.AccessibilityRequestActivity.a",
    "com.appsmastersafey.bot.AccessibilityRequestService.a",
    "com.appsmastersafey.bot.AwesomeDialogActivity.i",
    "com.appsmastersafey.bot.AwesomeDialogActivity.j",
    "res/values/strings.xml（a11_request_title / a11_request_message / a11_request_button / accessibility_service_description）"
  ]
}
```

说明：本轮为定向核验，与既有已确认风险 R-001（`malware_trojan` / high，`source_mode=autonomous_audit`）指向同一处置对象与同一命题，故未重复登记新风险；`behavior_pattern_tags` 中 `DROPPER_STAGE1_INSTALL_OR_EMBEDDED` 依据包内 `dpm.SetupProfileActivity`、`VncDeviceAdminReceiver` 设备管理员授权链，其完整安装/嵌入二阶段未在本轮展开，属覆盖边界。

</details>
