# MR_141__88eb93c07c｜Anubis — Uber App

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：146.1s

## 1. 一句话核心结论

- **核心申请方式**：以 Uber App 为外壳、把无障碍服务伪装成 Google Start Protect，用空白 Activity 直跳系统无障碍设置页 + 居中 Toast 文案 + 每 700ms 不可逃逸重跳，逼用户手动勾选开启。
- **静态可见性说明**：无障碍引导全链路（ActivityAccessibility 空白壳页、ACCESSIBILITY_SETTINGS 跳转、StartWhileRequest 700ms 循环、ServiceToast 居中引导文案、ServiceAccessibility 扩容与抗卸载）在 classes.dex 中完全静态可见，无加壳、无 VMP、无加密载荷。仅 Play Protect 弹窗正文（textPlayProtect/buttonPlayProtect）与部分行为开关由 C2 /private/settings.php 远端下发，不影响无障碍引导链的静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `88eb93c07cfbf33ae0535f4500c43fa0ec58375ba7b6329283c71e47ecc555b3` |
| 包名 / 年份 | `cihomy.iatfxismdobcaqqg.yikltdmmxgizz` / 2019 |
| 家族 / 品类 | **Anubis**（同池样本数：9） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | Uber App |
| 引导页宣称品牌/身份 | Google Start Protect / Google Play Protect（Google 官方安全组件） |
| 系统无障碍列表服务名 | Google Start Protect |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务名与真实 Google Play Protect 仅差一词（Play→Start），构成同形品牌冒用；serviceconfig.xml 未声明 android:description，系统无障碍列表内不显示任何用途说明；settingsActivity 指向非本应用且不存在的 com.example.root.myapplication.MainActivity；所有 Activity 除 MainActivity 外 android:label 为空串、icon 统一为 @drawable/im 且 excludeFromRecents=true，无近期任务痕迹；MainActivity 启动后 setComponentEnabledSetting(...,2,1) 自禁用桌面组件，图标消失；应用主题为 Theme.Translucent.NoTitleBar。 |
| 无障碍服务类名 | `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.MainActivity（activity_main.xml，全屏 WebView） | LAUNCHER 图标点击 → onCreate | 原生Activity | **原文**：无（layout 仅含 <WebView android:id="@id/webView" fill_parent/>；仅在配置 b.n=true 时 loadUrl(b.o) 加载远端页面）<br>**译注**：冷启动无本地可见文案，按配置决定是否展示远端 WebView；随后立即自禁用组件并 finish，桌面图标消失。 | 无显式请求；用户看不到可操作界面，进程转入后台服务链 | `MainActivity.onCreate / res/layout/activity_main.xml` |
| 2 | 业务功能触发 | cihomy.iatfxismdobcaqqg.yikltdmmxgizz.StartWhileGlobal（IntentService）+ ReceiverAlarm / Jobi 定时链 | MainActivity 调 c.a(this,"startAlarm", Integer.parseInt("Interval")) 默认 10000ms；以及 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON 等广播 | 不可静态还原（后台无界面） | 无 | 无（后台静默） | `StartWhileGlobal.onHandleIntent / c.a(Context,String,int)` |
| 3 | 引导说明页 | cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityAccessibility（activity_accessibility.xml） | StartWhileRequest.onHandleIntent 在 !keyguard 且 startRequest 不含 Access=1 时 startActivity(ActivityAccessibility) | 原生Activity | **原文**：无（res/layout/activity_accessibility.xml 仅为无子控件的 <RelativeLayout android:id="@id/activity_go_adm"/>）<br>**译注**：纯空白全屏页面，不含任何说明文字、图标或按钮，用户只能看到空白并已被送往系统设置。 | 无按钮可点；无取消/跳过/返回入口（Activity 无标题栏，异常时直接 finish） | `ActivityAccessibility.onCreate / res/layout/activity_accessibility.xml` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | ActivityAccessibility.onCreate 内 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Google Start Protect（系统无障碍服务列表中显示的服务名，来自 Manifest android:label；无 android:description 说明行）<br>**译注**：系统无障碍服务列表中出现名为「Google Start Protect」的服务条目，无任何用途描述，等待用户手动打开开关。 | 要求用户在该系统页中找到「Google Start Protect」并点击开关开启（无应用内取消路径） | `ActivityAccessibility.onCreate / AndroidManifest.xml ServiceAccessibility@android:label` |
| 5 | 遮罩叠层指引 | cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceToast（居中 Toast，非悬浮窗） | StartWhileRequest 首次拉起引导页时 startService(ServiceToast) → onStartCommand | 悬浮窗Overlay（Toast 叠于系统设置页之上，setGravity(16,0,0) 屏幕正中） | **原文**：Enable access for 'Google Start Protect'<br>**译注**：为“Google Start Protect”启用访问权限（多语言版本如中文「使访问 'Google Start Protect'」、俄文「Включите доступ для ...」、葡文「Habilite o acesso para ...」等 100+ 语种由 b.h/b.i 表按系统语言选取） | 仅提示，无按钮；用户须自行在系统列表中勾选开启（Toast 本身不可交互） | `ServiceToast.onStartCommand / c.b(Context,String,String) 中 StringAccessibility 初始化 / b.i 多语言表` |
| 6 | 拒权反馈循环 | StartWhileRequest.onHandleIntent 循环体 + ActivityAccessibility 反复重建 | 用户按返回键退出设置页或返回桌面后，TimeUnit.MILLISECONDS.sleep(700) 到期再次 startActivity(ActivityAccessibility) | 原生Activity | **原文**：无（每轮重新进入空白页后再次跳转系统设置）<br>**译注**：每 700ms 无条件重新拉起空白页并跳转无障碍设置页，计数到 25 后归零继续，用户无法通过返回/退出摆脱。 | 无取消路径，只能通过开启服务使 startRequest 出现 Access=1 才停止 | `StartWhileRequest.onHandleIntent（r13.b = 700; r13.d > 25 归 -1 循环）` |
| 7 | 跳受限设置 | android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS（package:本包） | StartWhileRequest 在 Access=1 达成后、SDK≥23 且未忽略电池优化时 startActivity 该 Intent；ReceiverAlarm#a 亦重复该跳转 | 系统无障碍页（电池优化系统页） | **原文**：无（系统页原文，应用侧无自定义文案）<br>**译注**：引导用户将本应用加入「不优化电池」白名单，保障后台常驻；非 Android 13 受限设置教学路径。 | 要求用户点击「允许」/「不优化」 | `StartWhileRequest.onHandleIntent（Intent("android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS")）` |
| 8 | 获权后动作 | ServiceAccessibility.onServiceConnected → onAccessibilityEvent → ServiceAccessibility.a() + ActivityAlert2 | 用户在系统页开启服务 → onServiceConnected；后续为无障碍事件驱动与卸载监听驱动 | 原生Activity（ActivityAlert2 弹窗）/ 通知栏（无） | **原文**：Request to disable <Google Play Protect>! / Trying to enable <Google Play Protect>!（上报 C2 的日志串）；ActivityAlert2 携带 extra "blockDelete" / "deleteApp"<br>**译注**：服务全量扩容（eventTypes=-1、flags=1、canRetrieveWindowContent=true）进行按键与界面记录；检测到用户试图开启 Play Protect 或卸载时，先发 HOME Intent 再压栈 ActivityAlert2 弹窗阻断，并跳转 APPLICATION_DETAILS_SETTINGS 应用详情页。 | 被要求放弃卸载/放弃开启防护（弹窗无良性退出路径） | `ServiceAccessibility.onServiceConnected / ServiceAccessibility.a() / ActivityAlert2.onCreate` |
| 9 | 业务功能触发 | cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityPlayProtect（不可取消 AlertDialog）+ com.google.android.gms.security.settings.VerifyAppsSettingsActivity | StartWhileGlobal.onHandleIntent 在锁屏状态且 foregroundwhile=true 时调用 c.a(this,"Google","Update Google Play Service")；或 C2 置 play_protect 开关后 startActivity(ActivityPlayProtect) | 原生Dialog | **原文**：Title: Google Play Protect \| Message: textPlayProtect（C2 下发，缺省空串）\| Button: buttonPlayProtect（C2 下发，缺省空串）<br>**译注**：以「Google Play Protect」为标题的不可取消对话框，正文与按钮文字由 C2 下发，点击后跳转 GMS 的 VerifyAppsSettingsActivity 关闭 Play Protect；无取消按钮（setCancelable(false)，仅 setNegativeButton）。 | 要求用户点击唯一按钮前往关闭 Google Play Protect | `ActivityPlayProtect.onCreate / ActivityPlayProtect$1.onClick` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- ServiceToast.onStartCommand 的居中 Toast（setGravity(16,0,0)）：“Enable access for 'Google Start Protect'”，叠在系统无障碍设置页之上，是无障碍引导链中唯一的说服性文案载体
- 系统无障碍服务列表条目名（AndroidManifest.xml ServiceAccessibility android:label="Google Start Protect"），该条目无 android:description，列表内不呈现任何用途说明
- ActivityPlayProtect.onCreate 的 setCancelable(false) AlertDialog，标题硬编码 "Google Play Protect"，正文/按钮文字来自 C2 下发 textPlayProtect / buttonPlayProtect
- ActivityAccessibility 承载的 res/layout/activity_accessibility.xml 为空白 RelativeLayout，不含任何文字控件
- MainActivity 的 res/layout/activity_main.xml 仅含全屏 WebView，仅在 b.n=true 时 loadUrl(b.o) 加载远端 URL（C2 配置 urls=https://9pjlin9ilj,9iulj9piloj.com），该 WebView 用于界面注入而非无障碍教学
- 多语言引导文案以 [lang] 前缀内嵌在 b.h / b.i / b.j / b.k / b.l / b.m 静态字符串数组中，运行期由 c.b(Context,String,String) 按 Locale.getDefault().getLanguage() 选取并写入 SharedPreferences（StringActivate / StringAccessibility / StringPermis / StringYes）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable access for | 为……启用访问权限 | `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.b#i 数组 [en] 项 / c.b() 中 d(context,"StringAccessibility","Enable access for")` | 教唆忽视警告 |
| en | activate | 激活 | `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.b#h 数组 [en] 项 / c.b() 中 d(context,"StringActivate","activate")` | 假反诈安全 |
| zh | 使访问 | 使访问（“使访问 'Google Start Protect'”，中文语种下 Toast 的完整文本） | `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.b#i 数组 [zh] 项` | 教唆忽视警告 |
| ru | Включите доступ для | 为……启用访问权限 | `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.b#i 数组 [ru] 项` | 教唆忽视警告 |
| en | Google Start Protect | Google Start Protect（伪造的 Google 安全组件名，实为无障碍服务标签） | `AndroidManifest.xml ServiceAccessibility android:label / ServiceToast.onStartCommand 硬编码` | 假反诈安全 |
| en | Google Play Protect | Google Play Protect（伪造的官方防护组件标题） | `ActivityPlayProtect.onCreate setTitle 硬编码` | 假反诈安全 |
| en | Request to disable <Google Play Protect>! | 请求关闭 <Google Play Protect>！（上报 C2 的内部日志串） | `ActivityPlayProtect.onCreate c.b(this,"4",...)` | 未知 |
| en | Trying to enable <Google Play Protect>! | （用户）正在尝试启用 <Google Play Protect>！（无障碍事件监测到后的上报串） | `ServiceAccessibility.onAccessibilityEvent` | 未知 |
| en | Update Google Play Service | 更新 Google Play 服务（锁屏时展示的假更新提示） | `StartWhileGlobal.onHandleIntent c.a(this,"Google","Update Google Play Service")` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：StartWhileRequest.onHandleIntent 在设备未锁屏且本地 startRequest 不含 Access=1 时，循环体内 TimeUnit.MILLISECONDS.sleep(700) 后无条件 startActivity(ActivityAccessibility)（FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TOP），并累加 r13.d，超过 25 次归 -1 后继续，构成无上限的返回即重跳死循环；ActivityAccessibility 自身无 UI 可返回，onCreate 异常时 finish() 亦会被下一轮立即重建。
- **遮罩叠层 / 高仿系统设置页**：未实现半透明遮罩或高仿系统无障碍开关页；仅以 Toast（setGravity(16,0,0) 居中）叠加在真实系统无障碍设置页之上做文字引导，系统页本身未被仿冒。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=27、minSdkVersion=15，未包含 Android 13 受限设置（应用详情右上角菜单允许受限设置）或 Session 安装器绕过的教学文案；仅额外跳转 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 申请忽略电池优化。
- **获权后即时行为与防撤权机制**：有。ServiceAccessibility.a() 先 startActivity(Intent.ACTION_MAIN + CATEGORY_HOME) 回桌面，再以 FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TOP 压栈 ActivityAlert2(extra="blockDelete") 阻断卸载；ActivityAlert2.onCreate 同时 startActivity("android.settings.APPLICATION_DETAILS_SETTINGS", package:本包) 用于诱导/干扰；ReceiverBoot 监听 PACKAGE_REMOVED 与 ServiceAccessibility 监听 com.android.settings 界面事件；另有 API.a.c DeviceAdminReceiver 与 play_protect 开关压制 Play Protect。
- **良性降级 / 替代方案**：无。全链无任何手动模式、ADB 引导、只读降级或取消路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 am start / Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 或 ActivityAccessibility onCreate 被调用的瞬间（冷启动后 10s 内首次触发，之后每 700ms 一次），立即抓取「空白引导页 → 系统无障碍列表」这一组连续帧；同时在 startService(ServiceToast) 后 800ms 内抓取居中 Toast 帧。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导文案全部为可提取文本（Toast 文本 + 系统列表条目名），无纯图片诱导。需注意两点：① 应用无常规可见 UI，冷启动后立即 finish 并自禁用桌面组件，若 UTG 仅监控应用自身 Activity 生命周期且以包名过滤 Launcher 启动，可能漏掉 700ms 循环拉起；② Play Protect 弹窗正文由 C2 下发（缺省为空串），未联网时该步可能呈现空正文对话框，此时应以标题与跳转目标为准。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首个空白引导 Activity（跳转前的短暂画面）** | cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityAccessibility，全屏纯空白 RelativeLayout、无标题栏、无任何文本节点 | 空白页是“应用未做任何用途说明即直送系统开关”的直接证据，可与合规应用的说明页形成鲜明对比 | 页面节点树为空（仅根 RelativeLayout，无 TextView/Button）；无返回按钮、无取消/跳过控件；停留时间极短（<1s）后跳转系统设置 |
| **系统无障碍设置页上叠加的居中引导 Toast** | Toast 浮层，屏幕正中，文本形如 Enable access for 'Google Start Protect'（随系统语言变化） | 该 Toast 是整条引导链唯一的说服性文案，且其引用的服务名与真实 Google Play Protect 高度近似，是伪装身份的关键判别点 | Toast 文本包含 “Google Start Protect” 且与系统设置列表条目名一致；Toast 无任何按钮/交互节点；文本使用“Enable access for”祈使句式 |
| **系统无障碍服务列表项（伪装条目）** | 设置 → 无障碍 → 已下载/已安装服务，条目名 “Google Start Protect”，无描述行 | 可直接核对服务名与真实 Google 组件不符、且缺失用途说明，是无障碍权限钓鱼的核心证据 | 条目名 “Google Start Protect”；条目下无 android:description 说明文本；条目所属包名 cihomy.iatfxismdobcaqqg.yikltdmmxgizz 与 Google 无关 |
| **退出设置后被反复重跳的循环帧** | 同一 ActivityAccessibility 空白页连续多次出现在前台，间隔约 700ms | 证明存在拒绝循环机制，用户无法通过返回操作摆脱引导，属强制而非自愿授权 | 返回键/Home 后 700ms 内同一空白页再次前台；同一页面前台出现次数持续累积（>25 次仍不停止） |
| **Play Protect 关闭诱导弹窗** | ActivityPlayProtect 不可取消 AlertDialog，标题 “Google Play Protect”，单一按钮 | 证明除无障碍外还主动压制系统安全防护，是判定恶意性的强证据 | 对话框无取消/关闭按钮且点击外部不可关闭；标题为 “Google Play Protect”；点击后跳转 com.google.android.gms.security.settings.VerifyAppsSettingsActivity |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityAccessibility.onCreate`
- `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.StartWhileRequest.onHandleIntent`
- `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceToast.onStartCommand`
- `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceAccessibility.onServiceConnected`
- `cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityPlayProtect.onCreate`
- `res/xml/serviceconfig.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（UTG 视角）

**无障碍引导链已完全静态还原，共 4 层，且无任何用户可逃逸点。**

1. **冷启动即自我隐藏**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.MainActivity#onCreate>) 启动后立即 `setComponentEnabledSetting(MainActivity, 2, 1)` 禁用自身桌面组件并 `finish()`，同时 `startAlarm("Interval")`（默认 10s）拉起后台链，桌面图标随即消失。
2. **空白壳页直送系统设置**：[ActivityAccessibility.onCreate()](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityAccessibility#onCreate>) 加载的 [activity_accessibility.xml](<resource-unit:#1 file:res/layout/activity_accessibility.xml>) 是**零子控件的空白 RelativeLayout**，`onCreate` 内唯一动作就是 `startActivity("android.settings.ACCESSIBILITY_SETTINGS")`，异常时 `finish()`。全程无一句用途说明、无取消按钮。
3. **Toast 文案承担唯一“说服”职能**：[ServiceToast.onStartCommand()](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceToast#onStartCommand>) 以 `setGravity(16,0,0)` 在屏幕正中弹出 `Enable access for 'Google Start Protect'`，文案取自 [c.b()](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.c#b>) 初始化的 `StringAccessibility`，并由 [b](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.b>) 的 100+ 语种 `[lang]` 表按系统语言覆盖——为跨语区投放而设计。
4. **700ms 死循环重跳**：[StartWhileRequest.onHandleIntent()](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.StartWhileRequest#onHandleIntent>) 在未锁屏且 `startRequest` 不含 `Access=1` 时，每 700ms `startActivity(ActivityAccessibility)`（`NEW_TASK|CLEAR_TOP`），计数到 25 归零继续；用户返回桌面/退出设置都会被反复拉回。

**关键伪装点**：Manifest 显示名 `Uber App`，无障碍服务标签却是 `Google Start Protect`（与真实 Play Protect 仅差 Play→Start 一词）；[serviceconfig.xml](<resource-unit:#1 file:res/xml/serviceconfig.xml>) **无 `android:description`**，且 `settingsActivity` 指向不存在的 `com.example.root.myapplication.MainActivity`（残留/伪造），系统列表里只剩一个无说明的“Google 系”服务名。

**同一套诱导还覆盖系统防护**：[ActivityPlayProtect.onCreate()](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityPlayProtect#onCreate>) 弹标题为 `Google Play Protect` 的 `setCancelable(false)` AlertDialog，唯一按钮回调 [ActivityPlayProtect$1.onClick](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityPlayProtect$1#onClick>) 用 `setClassName("com.google.android.gms", "com.google.android.gms.security.settings.VerifyAppsSettingsActivity")` 把用户送到关闭 Play Protect 的页面，并向 C2 上报 `Request to disable <Google Play Protect>!`。

**获权后**：[onServiceConnected()](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceAccessibility#onServiceConnected>) 将 `eventTypes=-1`、`flags=1` 全量扩容；`onAccessibilityEvent` 做 KEY1/KEY2/KEY3 键盘记录并 POST 至 `/private/datakeylogger.php`；[ServiceAccessibility.a()](<resource-unit:#1.dex1 code:cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceAccessibility#a>) 先发 HOME 再压栈 `ActivityAlert2(blockDelete)` 阻断卸载。

已登记风险：**R-001**（malware_trojan / high）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（ActivityAccessibility 空白壳页、ACCESSIBILITY_SETTINGS 跳转、StartWhileRequest 700ms 循环、ServiceToast 居中引导文案、ServiceAccessibility 扩容与抗卸载）在 classes.dex 中完全静态可见，无加壳、无 VMP、无加密载荷。仅 Play Protect 弹窗正文（textPlayProtect/buttonPlayProtect）与部分行为开关由 C2 /private/settings.php 远端下发，不影响无障碍引导链的静态还原。",
  "summary_one_liner": "以 Uber App 为外壳、把无障碍服务伪装成 Google Start Protect，用空白 Activity 直跳系统无障碍设置页 + 居中 Toast 文案 + 每 700ms 不可逃逸重跳，逼用户手动勾选开启。",
  "disguise_identity": {
    "app_display_name": "Uber App",
    "claimed_brand_or_persona": "Google Start Protect / Google Play Protect（Google 官方安全组件）",
    "a11y_service_label": "Google Start Protect",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务名与真实 Google Play Protect 仅差一词（Play→Start），构成同形品牌冒用；serviceconfig.xml 未声明 android:description，系统无障碍列表内不显示任何用途说明；settingsActivity 指向非本应用且不存在的 com.example.root.myapplication.MainActivity；所有 Activity 除 MainActivity 外 android:label 为空串、icon 统一为 @drawable/im 且 excludeFromRecents=true，无近期任务痕迹；MainActivity 启动后 setComponentEnabledSetting(...,2,1) 自禁用桌面组件，图标消失；应用主题为 Theme.Translucent.NoTitleBar。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.MainActivity（activity_main.xml，全屏 WebView）",
      "trigger_event": "LAUNCHER 图标点击 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（layout 仅含 <WebView android:id=\"@id/webView\" fill_parent/>；仅在配置 b.n=true 时 loadUrl(b.o) 加载远端页面）",
      "shown_text_zh": "冷启动无本地可见文案，按配置决定是否展示远端 WebView；随后立即自禁用组件并 finish，桌面图标消失。",
      "user_action_requested": "无显式请求；用户看不到可操作界面，进程转入后台服务链",
      "code_anchor": "MainActivity.onCreate / res/layout/activity_main.xml"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.StartWhileGlobal（IntentService）+ ReceiverAlarm / Jobi 定时链",
      "trigger_event": "MainActivity 调 c.a(this,\"startAlarm\", Integer.parseInt(\"Interval\")) 默认 10000ms；以及 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON 等广播",
      "ui_carrier": "不可静态还原（后台无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台定时任务周期性检查 startRequest 中的 Access=1 标志与设备锁屏状态，决定是否启动无障碍引导。",
      "user_action_requested": "无（后台静默）",
      "code_anchor": "StartWhileGlobal.onHandleIntent / c.a(Context,String,int)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityAccessibility（activity_accessibility.xml）",
      "trigger_event": "StartWhileRequest.onHandleIntent 在 !keyguard 且 startRequest 不含 Access=1 时 startActivity(ActivityAccessibility)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（res/layout/activity_accessibility.xml 仅为无子控件的 <RelativeLayout android:id=\"@id/activity_go_adm\"/>）",
      "shown_text_zh": "纯空白全屏页面，不含任何说明文字、图标或按钮，用户只能看到空白并已被送往系统设置。",
      "user_action_requested": "无按钮可点；无取消/跳过/返回入口（Activity 无标题栏，异常时直接 finish）",
      "code_anchor": "ActivityAccessibility.onCreate / res/layout/activity_accessibility.xml"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "ActivityAccessibility.onCreate 内 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Start Protect（系统无障碍服务列表中显示的服务名，来自 Manifest android:label；无 android:description 说明行）",
      "shown_text_zh": "系统无障碍服务列表中出现名为「Google Start Protect」的服务条目，无任何用途描述，等待用户手动打开开关。",
      "user_action_requested": "要求用户在该系统页中找到「Google Start Protect」并点击开关开启（无应用内取消路径）",
      "code_anchor": "ActivityAccessibility.onCreate / AndroidManifest.xml ServiceAccessibility@android:label"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceToast（居中 Toast，非悬浮窗）",
      "trigger_event": "StartWhileRequest 首次拉起引导页时 startService(ServiceToast) → onStartCommand",
      "ui_carrier": "悬浮窗Overlay（Toast 叠于系统设置页之上，setGravity(16,0,0) 屏幕正中）",
      "shown_text_verbatim": "Enable access for 'Google Start Protect'",
      "shown_text_zh": "为“Google Start Protect”启用访问权限（多语言版本如中文「使访问 'Google Start Protect'」、俄文「Включите доступ для ...」、葡文「Habilite o acesso para ...」等 100+ 语种由 b.h/b.i 表按系统语言选取）",
      "user_action_requested": "仅提示，无按钮；用户须自行在系统列表中勾选开启（Toast 本身不可交互）",
      "code_anchor": "ServiceToast.onStartCommand / c.b(Context,String,String) 中 StringAccessibility 初始化 / b.i 多语言表"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "StartWhileRequest.onHandleIntent 循环体 + ActivityAccessibility 反复重建",
      "trigger_event": "用户按返回键退出设置页或返回桌面后，TimeUnit.MILLISECONDS.sleep(700) 到期再次 startActivity(ActivityAccessibility)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（每轮重新进入空白页后再次跳转系统设置）",
      "shown_text_zh": "每 700ms 无条件重新拉起空白页并跳转无障碍设置页，计数到 25 后归零继续，用户无法通过返回/退出摆脱。",
      "user_action_requested": "无取消路径，只能通过开启服务使 startRequest 出现 Access=1 才停止",
      "code_anchor": "StartWhileRequest.onHandleIntent（r13.b = 700; r13.d > 25 归 -1 循环）"
    },
    {
      "step": 7,
      "stage": "跳受限设置",
      "screen_or_component": "android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS（package:本包）",
      "trigger_event": "StartWhileRequest 在 Access=1 达成后、SDK≥23 且未忽略电池优化时 startActivity 该 Intent；ReceiverAlarm#a 亦重复该跳转",
      "ui_carrier": "系统无障碍页（电池优化系统页）",
      "shown_text_verbatim": "无（系统页原文，应用侧无自定义文案）",
      "shown_text_zh": "引导用户将本应用加入「不优化电池」白名单，保障后台常驻；非 Android 13 受限设置教学路径。",
      "user_action_requested": "要求用户点击「允许」/「不优化」",
      "code_anchor": "StartWhileRequest.onHandleIntent（Intent(\"android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS\")）"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "ServiceAccessibility.onServiceConnected → onAccessibilityEvent → ServiceAccessibility.a() + ActivityAlert2",
      "trigger_event": "用户在系统页开启服务 → onServiceConnected；后续为无障碍事件驱动与卸载监听驱动",
      "ui_carrier": "原生Activity（ActivityAlert2 弹窗）/ 通知栏（无）",
      "shown_text_verbatim": "Request to disable <Google Play Protect>! / Trying to enable <Google Play Protect>!（上报 C2 的日志串）；ActivityAlert2 携带 extra \"blockDelete\" / \"deleteApp\"",
      "shown_text_zh": "服务全量扩容（eventTypes=-1、flags=1、canRetrieveWindowContent=true）进行按键与界面记录；检测到用户试图开启 Play Protect 或卸载时，先发 HOME Intent 再压栈 ActivityAlert2 弹窗阻断，并跳转 APPLICATION_DETAILS_SETTINGS 应用详情页。",
      "user_action_requested": "被要求放弃卸载/放弃开启防护（弹窗无良性退出路径）",
      "code_anchor": "ServiceAccessibility.onServiceConnected / ServiceAccessibility.a() / ActivityAlert2.onCreate"
    },
    {
      "step": 9,
      "stage": "业务功能触发",
      "screen_or_component": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityPlayProtect（不可取消 AlertDialog）+ com.google.android.gms.security.settings.VerifyAppsSettingsActivity",
      "trigger_event": "StartWhileGlobal.onHandleIntent 在锁屏状态且 foregroundwhile=true 时调用 c.a(this,\"Google\",\"Update Google Play Service\")；或 C2 置 play_protect 开关后 startActivity(ActivityPlayProtect)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: Google Play Protect | Message: textPlayProtect（C2 下发，缺省空串）| Button: buttonPlayProtect（C2 下发，缺省空串）",
      "shown_text_zh": "以「Google Play Protect」为标题的不可取消对话框，正文与按钮文字由 C2 下发，点击后跳转 GMS 的 VerifyAppsSettingsActivity 关闭 Play Protect；无取消按钮（setCancelable(false)，仅 setNegativeButton）。",
      "user_action_requested": "要求用户点击唯一按钮前往关闭 Google Play Protect",
      "code_anchor": "ActivityPlayProtect.onCreate / ActivityPlayProtect$1.onClick"
    }
  ],
  "text_presentation_locations": [
    "ServiceToast.onStartCommand 的居中 Toast（setGravity(16,0,0)）：“Enable access for 'Google Start Protect'”，叠在系统无障碍设置页之上，是无障碍引导链中唯一的说服性文案载体",
    "系统无障碍服务列表条目名（AndroidManifest.xml ServiceAccessibility android:label=\"Google Start Protect\"），该条目无 android:description，列表内不呈现任何用途说明",
    "ActivityPlayProtect.onCreate 的 setCancelable(false) AlertDialog，标题硬编码 \"Google Play Protect\"，正文/按钮文字来自 C2 下发 textPlayProtect / buttonPlayProtect",
    "ActivityAccessibility 承载的 res/layout/activity_accessibility.xml 为空白 RelativeLayout，不含任何文字控件",
    "MainActivity 的 res/layout/activity_main.xml 仅含全屏 WebView，仅在 b.n=true 时 loadUrl(b.o) 加载远端 URL（C2 配置 urls=https://9pjlin9ilj,9iulj9piloj.com），该 WebView 用于界面注入而非无障碍教学",
    "多语言引导文案以 [lang] 前缀内嵌在 b.h / b.i / b.j / b.k / b.l / b.m 静态字符串数组中，运行期由 c.b(Context,String,String) 按 Locale.getDefault().getLanguage() 选取并写入 SharedPreferences（StringActivate / StringAccessibility / StringPermis / StringYes）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable access for",
      "text_zh": "为……启用访问权限",
      "source_location": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.b#i 数组 [en] 项 / c.b() 中 d(context,\"StringAccessibility\",\"Enable access for\")",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "activate",
      "text_zh": "激活",
      "source_location": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.b#h 数组 [en] 项 / c.b() 中 d(context,\"StringActivate\",\"activate\")",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "zh",
      "text_verbatim": "使访问",
      "text_zh": "使访问（“使访问 'Google Start Protect'”，中文语种下 Toast 的完整文本）",
      "source_location": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.b#i 数组 [zh] 项",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "ru",
      "text_verbatim": "Включите доступ для",
      "text_zh": "为……启用访问权限",
      "source_location": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.b#i 数组 [ru] 项",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Start Protect",
      "text_zh": "Google Start Protect（伪造的 Google 安全组件名，实为无障碍服务标签）",
      "source_location": "AndroidManifest.xml ServiceAccessibility android:label / ServiceToast.onStartCommand 硬编码",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play Protect",
      "text_zh": "Google Play Protect（伪造的官方防护组件标题）",
      "source_location": "ActivityPlayProtect.onCreate setTitle 硬编码",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Request to disable <Google Play Protect>!",
      "text_zh": "请求关闭 <Google Play Protect>！（上报 C2 的内部日志串）",
      "source_location": "ActivityPlayProtect.onCreate c.b(this,\"4\",...)",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Trying to enable <Google Play Protect>!",
      "text_zh": "（用户）正在尝试启用 <Google Play Protect>！（无障碍事件监测到后的上报串）",
      "source_location": "ServiceAccessibility.onAccessibilityEvent",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Update Google Play Service",
      "text_zh": "更新 Google Play 服务（锁屏时展示的假更新提示）",
      "source_location": "StartWhileGlobal.onHandleIntent c.a(this,\"Google\",\"Update Google Play Service\")",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "StartWhileRequest.onHandleIntent 在设备未锁屏且本地 startRequest 不含 Access=1 时，循环体内 TimeUnit.MILLISECONDS.sleep(700) 后无条件 startActivity(ActivityAccessibility)（FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TOP），并累加 r13.d，超过 25 次归 -1 后继续，构成无上限的返回即重跳死循环；ActivityAccessibility 自身无 UI 可返回，onCreate 异常时 finish() 亦会被下一轮立即重建。",
    "overlay_or_fake_settings": "未实现半透明遮罩或高仿系统无障碍开关页；仅以 Toast（setGravity(16,0,0) 居中）叠加在真实系统无障碍设置页之上做文字引导，系统页本身未被仿冒。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=27、minSdkVersion=15，未包含 Android 13 受限设置（应用详情右上角菜单允许受限设置）或 Session 安装器绕过的教学文案；仅额外跳转 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 申请忽略电池优化。",
    "post_grant_anti_removal": "有。ServiceAccessibility.a() 先 startActivity(Intent.ACTION_MAIN + CATEGORY_HOME) 回桌面，再以 FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TOP 压栈 ActivityAlert2(extra=\"blockDelete\") 阻断卸载；ActivityAlert2.onCreate 同时 startActivity(\"android.settings.APPLICATION_DETAILS_SETTINGS\", package:本包) 用于诱导/干扰；ReceiverBoot 监听 PACKAGE_REMOVED 与 ServiceAccessibility 监听 com.android.settings 界面事件；另有 API.a.c DeviceAdminReceiver 与 play_protect 开关压制 Play Protect。",
    "benign_graceful_degradation": "无。全链无任何手动模式、ADB 引导、只读降级或取消路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 am start / Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 或 ActivityAccessibility onCreate 被调用的瞬间（冷启动后 10s 内首次触发，之后每 700ms 一次），立即抓取「空白引导页 → 系统无障碍列表」这一组连续帧；同时在 startService(ServiceToast) 后 800ms 内抓取居中 Toast 帧。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首个空白引导 Activity（跳转前的短暂画面）",
        "page_identifier": "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityAccessibility，全屏纯空白 RelativeLayout、无标题栏、无任何文本节点",
        "why_most_useful": "空白页是“应用未做任何用途说明即直送系统开关”的直接证据，可与合规应用的说明页形成鲜明对比",
        "observable_utg_signals": ["页面节点树为空（仅根 RelativeLayout，无 TextView/Button）", "无返回按钮、无取消/跳过控件", "停留时间极短（<1s）后跳转系统设置"]
      },
      {
        "page_role": "系统无障碍设置页上叠加的居中引导 Toast",
        "page_identifier": "Toast 浮层，屏幕正中，文本形如 Enable access for 'Google Start Protect'（随系统语言变化）",
        "why_most_useful": "该 Toast 是整条引导链唯一的说服性文案，且其引用的服务名与真实 Google Play Protect 高度近似，是伪装身份的关键判别点",
        "observable_utg_signals": ["Toast 文本包含 “Google Start Protect” 且与系统设置列表条目名一致", "Toast 无任何按钮/交互节点", "文本使用“Enable access for”祈使句式"]
      },
      {
        "page_role": "系统无障碍服务列表项（伪装条目）",
        "page_identifier": "设置 → 无障碍 → 已下载/已安装服务，条目名 “Google Start Protect”，无描述行",
        "why_most_useful": "可直接核对服务名与真实 Google 组件不符、且缺失用途说明，是无障碍权限钓鱼的核心证据",
        "observable_utg_signals": ["条目名 “Google Start Protect”", "条目下无 android:description 说明文本", "条目所属包名 cihomy.iatfxismdobcaqqg.yikltdmmxgizz 与 Google 无关"]
      },
      {
        "page_role": "退出设置后被反复重跳的循环帧",
        "page_identifier": "同一 ActivityAccessibility 空白页连续多次出现在前台，间隔约 700ms",
        "why_most_useful": "证明存在拒绝循环机制，用户无法通过返回操作摆脱引导，属强制而非自愿授权",
        "observable_utg_signals": ["返回键/Home 后 700ms 内同一空白页再次前台", "同一页面前台出现次数持续累积（>25 次仍不停止）"]
      },
      {
        "page_role": "Play Protect 关闭诱导弹窗",
        "page_identifier": "ActivityPlayProtect 不可取消 AlertDialog，标题 “Google Play Protect”，单一按钮",
        "why_most_useful": "证明除无障碍外还主动压制系统安全防护，是判定恶意性的强证据",
        "observable_utg_signals": ["对话框无取消/关闭按钮且点击外部不可关闭", "标题为 “Google Play Protect”", "点击后跳转 com.google.android.gms.security.settings.VerifyAppsSettingsActivity"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导文案全部为可提取文本（Toast 文本 + 系统列表条目名），无纯图片诱导。需注意两点：① 应用无常规可见 UI，冷启动后立即 finish 并自禁用桌面组件，若 UTG 仅监控应用自身 Activity 生命周期且以包名过滤 Launcher 启动，可能漏掉 700ms 循环拉起；② Play Protect 弹窗正文由 C2 下发（缺省为空串），未联网时该步可能呈现空正文对话框，此时应以标题与跳转目标为准。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityAccessibility.onCreate",
    "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.StartWhileRequest.onHandleIntent",
    "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceToast.onStartCommand",
    "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.ServiceAccessibility.onServiceConnected",
    "cihomy.iatfxismdobcaqqg.yikltdmmxgizz.Activity.ActivityPlayProtect.onCreate",
    "res/xml/serviceconfig.xml"
  ]
}
```

</details>
