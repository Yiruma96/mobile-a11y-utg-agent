# MR_047__9046270d73｜AnubisDropper — Operatör Güncellemesi

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：132.4s

## 1. 一句话核心结论

- **核心申请方式**：应用冷启动即关闭自身桌面图标转入后台服务，用 700ms 循环定时器反复拉起无任何说明的 ActivityAccessibility 直跳系统无障碍设置页，同时以屏幕居中 Toast『Enable access for Operatör Güncellemesi』冒充运营商更新催促开启，获权后用不可取消的假系统错误弹窗阻断撤权。
- **静态可见性说明**：DEX 未加壳、无加密资产与二阶段载荷，无障碍引导的全部跳转点、循环定时器与 Toast 文案均在静态代码中可见；唯一不可静态确定的是 SharedPreferences 中 StringActivate/StringAccessibility/StringPermis/StringYes 的具体文案可被服务端下发覆盖，以及 startRequest/urls 等云端开关值。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9046270d735579bcedb6bb7c0a2ad21f9b5ef9432e46e733b36de964aecd3abc` |
| 包名 / 年份 | `apps.mustak.sason` / 2019 |
| 家族 / 品类 | **AnubisDropper**（同池样本数：1） |
| 原始来源标识 | https://blog.trendmicro.com/trendlabs-security-intelligence/anubis-android-malware-returns-with-over-17000-samples/ |
| 桌面显示名 | Operatör Güncellemesi |
| 引导页宣称品牌/身份 | 冒充土耳其移动运营商系统/驱动更新（通知栏文案为 Update The Driver System..、Update Google Play Service），真实身份为具备短信劫持、联系人读取、录音、屏幕注入、RAT 通道的银行木马投放器 |
| 系统无障碍列表服务名 | Operatör Güncellemesi |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置 android:settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity（伪造/死链）；服务未声明 android:description，系统无障碍列表项无任何用途说明；MainActivity 启动后立即 setComponentEnabledSetting 自禁用桌面入口实现图标消失；多个 Activity 的 android:label 置为空字符串（label=""）；核心类/方法名全部单字母混淆（c.d、c.b、ServiceAccessibility.a） |
| 无障碍服务类名 | `apps.mustak.sason.ServiceAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | apps.mustak.sason.Activity.MainActivity（LAUNCHER） | 用户点击桌面图标 onCreate | 原生Activity | **原文**：无（仅 setContentView(2130968582)；当 b.o 为真时改为 WebView 加载 this.b.p 远端地址）<br>**译注**：无可见引导文案，界面随即 finish | 无要求；应用自行 setComponentEnabledSetting(MainActivity, COMPONENT_DISABLED) 隐藏桌面图标，启动 StartWhileGlobal 并设定 10 秒 Alarm 后 finish()，用户看不到任何界面 | `apps.mustak.sason.Activity.MainActivity.onCreate` |
| 2 | 业务功能触发 | apps.mustak.sason.StartWhileGlobal（Service，onHandleIntent 主循环） | MainActivity onCreate 中 startService(StartWhileGlobal)；此后 TimeUnit.MILLISECONDS.sleep(1000) 每秒循环 | 通知栏 | **原文**：Info / Update The Driver System..<br>**译注**：标题“信息”，正文“更新驱动程序系统..”的前台常驻通知（startForeground(9906)）；锁屏态另走 c.a(this,"Google","Update Google Play Service") | 无按钮；用于伪装“系统驱动更新”并维持后台存活，同时把无障碍/设备管理员/统计权限申请流程串成循环 | `apps.mustak.sason.StartWhileGlobal.onHandleIntent / StartWhileGlobal.a` |
| 3 | 业务功能触发 | apps.mustak.sason.StartWhileRequest（Service，onHandleIntent 申请循环） | 定时器循环：TimeUnit.MILLISECONDS.sleep(c)，正常 700ms，未获权时压至 500ms，最多 25 次后重置 | 系统无障碍页 | **原文**：无界面文案（仅写日志 "STARTWHILE" / "!!!"）<br>**译注**：无文案，直接执行跳转判定 | 判定 c.g(context)==false（无障碍未启用）且 startRequest 含 "Access=1"（或 a.t 为 1/5/6）时，startActivity(ActivityAccessibility) 并 startService(ServiceToast) | `apps.mustak.sason.StartWhileRequest.onHandleIntent` |
| 4 | 引导说明页 | apps.mustak.sason.ServiceToast（Service，无界面，仅系统 Toast） | StartWhileRequest 每次跳转后 startService(ServiceToast) → onStartCommand | 悬浮窗Overlay | **原文**：Enable access for 'Operatör Güncellemesi'<br>**译注**：「为『Operatör Güncellemesi』开启访问权限」——Toast 通过 setGravity(16,0,0) 居中显示在屏幕正中；文案取自 SharedPreferences StringAccessibility（多语言表 b.i，tr 语言位为 "Aktif edin. "，zh 为 "使访问"），应用名取自 PackageManager label | 无按钮、无取消、无说明；仅催促用户去系统设置里为该服务打开开关 | `apps.mustak.sason.ServiceToast.onStartCommand；apps.mustak.sason.c.b(Context)` |
| 5 | 跳无障碍设置 | apps.mustak.sason.Activity.ActivityAccessibility（Theme 继承 application 的 Theme.Translucent.NoTitleBar，label=""） | onCreate 内联执行 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：无（setContentView(2130968576) 后立即跳转，异常时 finish()）<br>**译注**：自身界面不展示任何内容，直接跳转系统「无障碍 / Erişilebilirlik」设置页 | 要求用户在系统无障碍列表中找到并开启服务；本应用不提供任何说明、图示或跳过入口 | `apps.mustak.sason.Activity.ActivityAccessibility.onCreate` |
| 6 | 跳无障碍设置 | 系统无障碍服务列表项（ServiceAccessibility，label="Operatör Güncellemesi"，meta-data @xml/serviceconfig） | 系统解析 manifest 中的 BIND_ACCESSIBILITY_SERVICE 声明与 serviceconfig.xml | 系统无障碍页 | **原文**：Operatör Güncellemesi（android:label）；android:description 未声明<br>**译注**：系统列表仅显示“运营商更新”，没有任何用途说明文字，用户无从得知该服务可读取全部窗口内容并模拟点击 | 用户需在无说明的状态下自行打开该开关 | `AndroidManifest.xml service android:name="apps.mustak.sason.ServiceAccessibility"；res/xml/serviceconfig.xml` |
| 7 | 拒权反馈循环 | apps.mustak.sason.StartWhileRequest 循环 + ActivityAccessibility 重跳 | 用户从系统设置页返回而未开启服务，onHandleIntent 循环继续命中 c.g(context)==false | 系统无障碍页 | **原文**：Enable access for 'Operatör Güncellemesi'（每轮重新弹出 Toast）<br>**译注**：拒绝或返回后不会被放弃：500ms 一轮重新跳转无障碍设置页并重新弹居中 Toast，最多 25 次后计数器重置继续循环，无取消/跳过按钮 | 反复要求用户进入设置开启开关 | `apps.mustak.sason.StartWhileRequest.onHandleIntent` |
| 8 | 获权后动作 | apps.mustak.sason.ServiceAccessibility（onServiceConnected / onAccessibilityEvent / a()） | 用户在系统设置中开启开关，系统绑定服务触发 onServiceConnected | 原生Dialog | **原文**：HATA! / Sistem Dosyaları Kaldırılamaz!<br>**译注**：「错误！」/「系统文件无法移除！」——setCancelable(false) 且仅有一个 "ОК"（西里尔字母 О，非拉丁 O）按钮；由 ServiceAccessibility.a() 先按 HOME 回桌面再 startActivity(ActivityAlert2,"start=blockDelete") 弹出，用于阻断用户关闭无障碍/卸载 | 只能点“确定”，无取消/跳过；同时服务已 setServiceInfo(flags=1, eventTypes=-1) 全量监听界面事件并回传 time_start_permission | `apps.mustak.sason.ServiceAccessibility.onServiceConnected；apps.mustak.sason.ServiceAccessibility.a()；apps.mustak.sason.Activity.ActivityAlert2.onCreate` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统居中 Toast（非应用界面）：ServiceToast.onStartCommand 通过 Toast.makeText(...).setGravity(16,0,0) 显示 "Enable access for 'Operatör Güncellemesi'"，是唯一的授权催促文案
- 通知栏前台通知：StartWhileGlobal.a() 的 Notification "Info" / "Update The Driver System.."（startForeground(9906)）
- 系统无障碍服务列表项：仅显示 android:label="Operatör Güncellemesi"，android:description 缺失（无任何用途说明）
- 不可取消原生 AlertDialog：ActivityAlert2.onCreate 的 "HATA!" / "Sistem Dosyaları Kaldırılamaz!"（setCancelable(false)）
- 按语言本地化的多语言文案表：apps.mustak.sason.b 的静态字段 h/i/j/k/l/m/n/o/p/q/r，写入 SharedPreferences 的 StringActivate / StringAccessibility / StringPermis / StringYes / uninstall1 / uninstall2 / vkladmin / straccessibility，可被服务端下发覆盖
- 跳转设置前的应用界面：ActivityAccessibility 仅 setContentView(2130968576) 后立即跳转，无可见文字；MainActivity 亦不展示引导
- 无本地 HTML、无 assets 页面、无远端 WebView 教学页（MainActivity 的 WebView 仅在 b.o 为真时加载 this.b.p，属于变脸外壳而非无障碍教学）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable access for | 为……开启访问权限 | `apps.mustak.sason.b 字段 i（[en] 语言位），经 c.b(Context) 写入 SharedPreferences 键 StringAccessibility，由 ServiceToast.onStartCommand 拼成 "Enable access for 'Operatör Güncellemesi'"` | 假更新 |
| tr | Aktif edin. | 请激活。 | `apps.mustak.sason.b 字段 i（[tr] 语言位），同上路径` | 假更新 |
| en | Update The Driver System.. | 正在更新驱动程序系统.. | `apps.mustak.sason.StartWhileGlobal.a()（硬编码 Notification setContentText）` | 假更新 |
| en | Update Google Play Service | 更新 Google Play 服务 | `apps.mustak.sason.StartWhileGlobal.onHandleIntent（c.a(this,"Google","Update Google Play Service")）` | 假更新 |
| tr | HATA! | 错误！ | `apps.mustak.sason.Activity.ActivityAlert2.onCreate（AlertDialog setTitle，硬编码）` | 故障恐吓 |
| tr | Sistem Dosyaları Kaldırılamaz! | 系统文件无法移除！ | `apps.mustak.sason.Activity.ActivityAlert2.onCreate（AlertDialog setMessage，setCancelable(false)，硬编码）` | 故障恐吓 |
| tr | Sistem düzgün çalışmıyor, istatistiklere erişim etkinleştirmeniz gerekir ' | 系统无法正常运行，您需要开启对统计信息的访问权限『……』 | `apps.mustak.sason.c.d(Context,String) 的 statistic 分支（硬编码，用于 USAGE_ACCESS_SETTINGS 引导，与本无障碍流程同源套路）` | 故障恐吓 |
| en | The system does not work correctly, you need to enable access to the statistics ' | 系统无法正常运行，您需要开启对统计信息的访问权限『……』 | `apps.mustak.sason.c.d(Context,String) 的 statistic 分支（en 硬编码）` | 故障恐吓 |
| tr | İzin almak / Şimdi etkinleştir | 获取权限 / 立即启用 | `apps.mustak.sason.c.d(Context,String) statistic 分支的 AlertDialog 标题与按钮文案` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：StartWhileRequest.onHandleIntent 主循环每 700ms 一轮；未获权时 sleep 降至 500ms，重复 startActivity(ActivityAccessibility) + startService(ServiceToast)；计数器 e 累加到 25 后重置为 -1 继续无限循环，只要 c.g(context) 仍为 false 且云端 startRequest 含 "Access=1" 就不停止，用户返回系统设置页或拒绝均无法退出
- **遮罩叠层 / 高仿系统设置页**：无半透明遮罩、无高仿系统设置页；但使用 Toast.setGravity(16,0,0) 在屏幕正中叠加系统级 Toast 充当“引导提示”，并在后台拉起无内容的中转 Activity 直跳系统设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现引导用户进应用详情点右上角菜单开启“受限设置”的文案或分步教学；ACTION_APPLICATION_DETAILS_SETTINGS 仅在 ActivityAlert2 的 deleteApp 分支用于跳本应用详情页（卸载场景）。样本 targetSdkVersion=27，本身不触发 Android 13+ 受限设置拦截，因此无需该教学
- **获权后即时行为与防撤权机制**：有。ServiceAccessibility.a() 先 startActivity(ACTION_MAIN/HOME) 回到桌面，再以 FLAG_ACTIVITY_NEW_TASK|CLEAR_TASK 拉起 ActivityAlert2 弹 setCancelable(false) 的 "HATA! / Sistem Dosyaları Kaldırılamaz!" 假系统错误框，阻断用户前往设置关闭服务或卸载；同时 StartWhileGlobal/StartWhileRequest 在锁屏态与后台持续保活，ReceiverBoot 监听 PACKAGE_REMOVED/SCREEN_ON/USER_PRESENT 等重启
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到应用进程拉起 intent=android.settings.ACCESSIBILITY_SETTINGS 的瞬间（来源包 apps.mustak.sason，源 Activity apps.mustak.sason.Activity.ActivityAccessibility）——此时屏幕正中会同时出现 Toast，是最短捕获窗口；若无该 hook，则在冷启动 MainActivity 后 1~2 秒内（图标消失、无界面）直接录屏/截图系统无障碍设置页
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区不在 UI：引导文案全部为纯文本 Toast 与系统页，无图片诱导；但存在两点需注意——(1) 文案可由服务端下发覆盖 SharedPreferences（StringAccessibility/StringActivate），实际展示语言随 Locale 变化（tr/en/ru/zh 等 80+ 语言），UTG 规则需按语言表匹配而非固定英文；(2) 冷启动时 MainActivity 会自禁用桌面组件并 finish，无可见界面，若 UTG 仅在 Activity 前台时采样可能漏掉入口，建议在进程启动后即挂 hook 监测 ACCESSIBILITY_SETTINGS 跳转。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转瞬间的居中 Toast + 系统无障碍设置页** | 系统设置页 TITLE 含“无障碍/Erişilebilirlik/Accessibility”，同时屏幕中央浮层文本为 "Enable access for 'Operatör Güncellemesi'" 或 "Aktif edin. 'Operatör Güncellemesi'" | 这是全流程唯一的口头引导载体，且文案直接暴露“应用在催促开启无障碍”的意图，配合系统设置页可证明是应用主动跳转而非用户自发操作 | Toast 文本包含应用名 Operatör Güncellemesi 与 Enable access for / Aktif edin 关键字；Toast 位于屏幕正中（gravity=center）而非底部默认位置；前台页面包名为 com.android.settings 且标题为无障碍设置 |
| **系统无障碍服务列表项** | 列表中出现 "Operatör Güncellemesi" 服务项，且该项下方无任何描述文字 | 证明身份伪装（运营商更新名义）与描述缺失，是判定“利用无障碍权限且不告知用途”的直接证据 | 服务名 Operatör Güncellemesi；该项无 subtitle/description 文本节点；开关状态为关闭（未获权态） |
| **拒权后的重跳循环页** | 从系统设置按返回键后，1 秒内再次回到无障碍设置页，并重复出现居中 Toast | 证明存在强制循环而非良性降级，是区分“引导”与“逼迫”的关键动态证据 | 返回桌面后 1~2 秒内系统无障碍页被再次拉起；Toast 文本与上一轮完全一致并重复出现；同一 Activity 栈反复重建（ActivityAccessibility 无界面即 finish） |
| **获权后的假系统错误弹窗** | 屏幕中央 AlertDialog 标题 "HATA!"、正文 "Sistem Dosyaları Kaldırılamaz!"、单个 "ОК" 按钮，且无法通过返回键/点击外部关闭 | 证明获权后立即实施反撤权，是恶意定性而非权限滥用的决定性证据 | Dialog 文本 HATA! / Sistem Dosyaları Kaldırılamaz!；按钮文本使用西里尔字母 О（非拉丁 O）；按返回键与点击外部区域均无法关闭；Dialog 出现前应用曾拉起 HOME |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `apps.mustak.sason.Activity.ActivityAccessibility.onCreate`
- `apps.mustak.sason.StartWhileRequest.onHandleIntent`
- `apps.mustak.sason.ServiceToast.onStartCommand`
- `apps.mustak.sason.ServiceAccessibility.onServiceConnected`
- `apps.mustak.sason.Activity.ActivityAlert2.onCreate`
- `res/xml/serviceconfig.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**核心结论：该样本没有任何“说明页/教学页/遮罩”，而是用「后台定时器 + 居中 Toast 文案」把用户直接推进系统无障碍设置页，靠无限重跳实现强制授权。**

1. **冷启动即自毁入口**：[MainActivity.onCreate](<resource-unit:#1.dex1 code:apps.mustak.sason.Activity.MainActivity#onCreate>) 加载布局后立刻 `setComponentEnabledSetting(MainActivity, COMPONENT_DISABLED)` 关闭自身桌面图标，拉起 `StartWhileGlobal`，设定 10 秒 Alarm，然后 `finish()`——用户桌面“点一下就没反应”，真正的引导全部发生在后台。
2. **无任何说明界面**：`ActivityAccessibility.onCreate` 只有三行实质逻辑——`setContentView(2130968576)` → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` → 异常时 `finish()`。**没有弹窗、没有 WebView、没有本地 HTML、没有悬浮引导层**。
3. **唯一的“引导文案”是系统级 Toast**：`StartWhileRequest` 每 700ms 循环（未获权时把间隔压到 500ms，最多 25 次），每次 `startActivity(ActivityAccessibility)` 后同时 `startService(ServiceToast)`；`ServiceToast.onStartCommand` 用 `Toast.setGravity(16,0,0)` 在**屏幕正中**显示 `StringAccessibility + " 'Operatör Güncellemesi'"`，即多语言本地化的 **“Enable access for 'Operatör Güncellemesi'”**（中文资源位为“使访问 'Operatör Güncellemesi'”，土耳其语为“Aktif edin. ”）。该文案由 `c.b(Context)` 依据 `Locale` 从 `b.h/b.i` 语言表写入 SharedPreferences（`StringActivate`/`StringAccessibility`/`StringPermis`/`StringYes`），可被服务端下发覆盖。
4. **拒绝即死循环**：`StartWhileRequest` 的判定条件是 `c.g(context)`（无障碍是否已启用）为 false 且 `startRequest` 含 `Access=1`（或 `a.t` 属于 1/5/6）；未获权就永远回到 `startActivity(ActivityAccessibility)`，没有取消/跳过分支。
5. **伪更新话术铺垫**：`StartWhileGlobal.onHandleIntent` 在锁屏态下走 `c.a(this,"Google","Update Google Play Service")`，并在 `a()` 中 `startForeground(9906, Notification("Info","Update The Driver System.."))`，用“驱动/Google Play 服务更新”伪装成系统维护动作。
6. **获权后立即锁死撤权路径**：`ServiceAccessibility.onServiceConnected` 把 `flags=1 / eventTypes=-1`（监听全部事件、含不重要视图）拉满；`ServiceAccessibility.a()` 一旦触发先按 HOME 回桌面，再 `startActivity(ActivityAlert2,"start=blockDelete")` 弹出 **`setCancelable(false)`** 的 `"HATA!" / "Sistem Dosyaları Kaldırılamaz!"`（“错误！系统文件无法移除！”）——用假系统错误阻止用户去设置里关闭服务或卸载。
7. **身份伪装的关键破绽**：无障碍服务在系统列表里显示 `Operatör Güncellemesi`（“运营商更新”），但 `res/xml/serviceconfig.xml` 的 `android:settingsActivity` 指向不存在的 `com.example.root.myapplication.MainActivity`，且 **未声明 `android:description`**——系统无障碍列表项没有任何用途说明，用户看不到“可读取屏幕内容/代操作”的真实权限含义。
8. **受限设置教学（Android 13+）**：未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 用于引导开启“受限设置”的路径；该 Intent 仅在 `ActivityAlert2` 的 `deleteApp` 分支用于跳本应用详情页（自助卸载场景）。样本 `targetSdkVersion=27`，本身不触发 13+ 受限设置拦截，故不需要该教学。
9. **静态可见性**：DEX 未加壳、无加密资产、无动态加载 Dex；引导文案、跳转点、循环逻辑全部静态可见（仅 `StringActivate/StringAccessibility` 等具体字符串可被远端下发覆盖）。

关键代码位置：[ActivityAccessibility.onCreate](<resource-unit:#1.dex1 code:apps.mustak.sason.Activity.ActivityAccessibility#onCreate>)、[ServiceToast.onStartCommand](<resource-unit:#1.dex1 code:apps.mustak.sason.ServiceToast#onStartCommand>)、[StartWhileRequest.onHandleIntent](<resource-unit:#1.dex1 code:apps.mustak.sason.StartWhileRequest#onHandleIntent>)、[ServiceAccessibility.onServiceConnected](<resource-unit:#1.dex1 code:apps.mustak.sason.ServiceAccessibility#onServiceConnected>)、[serviceconfig.xml](<resource-unit:#1 file:res/xml/serviceconfig.xml>)。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳、无加密资产与二阶段载荷，无障碍引导的全部跳转点、循环定时器与 Toast 文案均在静态代码中可见；唯一不可静态确定的是 SharedPreferences 中 StringActivate/StringAccessibility/StringPermis/StringYes 的具体文案可被服务端下发覆盖，以及 startRequest/urls 等云端开关值。",
  "summary_one_liner": "应用冷启动即关闭自身桌面图标转入后台服务，用 700ms 循环定时器反复拉起无任何说明的 ActivityAccessibility 直跳系统无障碍设置页，同时以屏幕居中 Toast『Enable access for Operatör Güncellemesi』冒充运营商更新催促开启，获权后用不可取消的假系统错误弹窗阻断撤权。",
  "disguise_identity": {
    "app_display_name": "Operatör Güncellemesi",
    "claimed_brand_or_persona": "冒充土耳其移动运营商系统/驱动更新（通知栏文案为 Update The Driver System..、Update Google Play Service），真实身份为具备短信劫持、联系人读取、录音、屏幕注入、RAT 通道的银行木马投放器",
    "a11y_service_label": "Operatör Güncellemesi",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置 android:settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity（伪造/死链）；服务未声明 android:description，系统无障碍列表项无任何用途说明；MainActivity 启动后立即 setComponentEnabledSetting 自禁用桌面入口实现图标消失；多个 Activity 的 android:label 置为空字符串（label=\"\"）；核心类/方法名全部单字母混淆（c.d、c.b、ServiceAccessibility.a）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "apps.mustak.sason.Activity.MainActivity（LAUNCHER）",
      "trigger_event": "用户点击桌面图标 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅 setContentView(2130968582)；当 b.o 为真时改为 WebView 加载 this.b.p 远端地址）",
      "shown_text_zh": "无可见引导文案，界面随即 finish",
      "user_action_requested": "无要求；应用自行 setComponentEnabledSetting(MainActivity, COMPONENT_DISABLED) 隐藏桌面图标，启动 StartWhileGlobal 并设定 10 秒 Alarm 后 finish()，用户看不到任何界面",
      "code_anchor": "apps.mustak.sason.Activity.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "apps.mustak.sason.StartWhileGlobal（Service，onHandleIntent 主循环）",
      "trigger_event": "MainActivity onCreate 中 startService(StartWhileGlobal)；此后 TimeUnit.MILLISECONDS.sleep(1000) 每秒循环",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Info / Update The Driver System..",
      "shown_text_zh": "标题“信息”，正文“更新驱动程序系统..”的前台常驻通知（startForeground(9906)）；锁屏态另走 c.a(this,\"Google\",\"Update Google Play Service\")",
      "user_action_requested": "无按钮；用于伪装“系统驱动更新”并维持后台存活，同时把无障碍/设备管理员/统计权限申请流程串成循环",
      "code_anchor": "apps.mustak.sason.StartWhileGlobal.onHandleIntent / StartWhileGlobal.a"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "apps.mustak.sason.StartWhileRequest（Service，onHandleIntent 申请循环）",
      "trigger_event": "定时器循环：TimeUnit.MILLISECONDS.sleep(c)，正常 700ms，未获权时压至 500ms，最多 25 次后重置",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无界面文案（仅写日志 \"STARTWHILE\" / \"!!!\"）",
      "shown_text_zh": "无文案，直接执行跳转判定",
      "user_action_requested": "判定 c.g(context)==false（无障碍未启用）且 startRequest 含 \"Access=1\"（或 a.t 为 1/5/6）时，startActivity(ActivityAccessibility) 并 startService(ServiceToast)",
      "code_anchor": "apps.mustak.sason.StartWhileRequest.onHandleIntent"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "apps.mustak.sason.ServiceToast（Service，无界面，仅系统 Toast）",
      "trigger_event": "StartWhileRequest 每次跳转后 startService(ServiceToast) → onStartCommand",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Enable access for 'Operatör Güncellemesi'",
      "shown_text_zh": "「为『Operatör Güncellemesi』开启访问权限」——Toast 通过 setGravity(16,0,0) 居中显示在屏幕正中；文案取自 SharedPreferences StringAccessibility（多语言表 b.i，tr 语言位为 \"Aktif edin. \"，zh 为 \"使访问\"），应用名取自 PackageManager label",
      "user_action_requested": "无按钮、无取消、无说明；仅催促用户去系统设置里为该服务打开开关",
      "code_anchor": "apps.mustak.sason.ServiceToast.onStartCommand；apps.mustak.sason.c.b(Context)"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "apps.mustak.sason.Activity.ActivityAccessibility（Theme 继承 application 的 Theme.Translucent.NoTitleBar，label=\"\"）",
      "trigger_event": "onCreate 内联执行 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（setContentView(2130968576) 后立即跳转，异常时 finish()）",
      "shown_text_zh": "自身界面不展示任何内容，直接跳转系统「无障碍 / Erişilebilirlik」设置页",
      "user_action_requested": "要求用户在系统无障碍列表中找到并开启服务；本应用不提供任何说明、图示或跳过入口",
      "code_anchor": "apps.mustak.sason.Activity.ActivityAccessibility.onCreate"
    },
    {
      "step": 6,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表项（ServiceAccessibility，label=\"Operatör Güncellemesi\"，meta-data @xml/serviceconfig）",
      "trigger_event": "系统解析 manifest 中的 BIND_ACCESSIBILITY_SERVICE 声明与 serviceconfig.xml",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Operatör Güncellemesi（android:label）；android:description 未声明",
      "shown_text_zh": "系统列表仅显示“运营商更新”，没有任何用途说明文字，用户无从得知该服务可读取全部窗口内容并模拟点击",
      "user_action_requested": "用户需在无说明的状态下自行打开该开关",
      "code_anchor": "AndroidManifest.xml service android:name=\"apps.mustak.sason.ServiceAccessibility\"；res/xml/serviceconfig.xml"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "apps.mustak.sason.StartWhileRequest 循环 + ActivityAccessibility 重跳",
      "trigger_event": "用户从系统设置页返回而未开启服务，onHandleIntent 循环继续命中 c.g(context)==false",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable access for 'Operatör Güncellemesi'（每轮重新弹出 Toast）",
      "shown_text_zh": "拒绝或返回后不会被放弃：500ms 一轮重新跳转无障碍设置页并重新弹居中 Toast，最多 25 次后计数器重置继续循环，无取消/跳过按钮",
      "user_action_requested": "反复要求用户进入设置开启开关",
      "code_anchor": "apps.mustak.sason.StartWhileRequest.onHandleIntent"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "apps.mustak.sason.ServiceAccessibility（onServiceConnected / onAccessibilityEvent / a()）",
      "trigger_event": "用户在系统设置中开启开关，系统绑定服务触发 onServiceConnected",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "HATA! / Sistem Dosyaları Kaldırılamaz!",
      "shown_text_zh": "「错误！」/「系统文件无法移除！」——setCancelable(false) 且仅有一个 \"ОК\"（西里尔字母 О，非拉丁 O）按钮；由 ServiceAccessibility.a() 先按 HOME 回桌面再 startActivity(ActivityAlert2,\"start=blockDelete\") 弹出，用于阻断用户关闭无障碍/卸载",
      "user_action_requested": "只能点“确定”，无取消/跳过；同时服务已 setServiceInfo(flags=1, eventTypes=-1) 全量监听界面事件并回传 time_start_permission",
      "code_anchor": "apps.mustak.sason.ServiceAccessibility.onServiceConnected；apps.mustak.sason.ServiceAccessibility.a()；apps.mustak.sason.Activity.ActivityAlert2.onCreate"
    }
  ],
  "text_presentation_locations": [
    "系统居中 Toast（非应用界面）：ServiceToast.onStartCommand 通过 Toast.makeText(...).setGravity(16,0,0) 显示 \"Enable access for 'Operatör Güncellemesi'\"，是唯一的授权催促文案",
    "通知栏前台通知：StartWhileGlobal.a() 的 Notification \"Info\" / \"Update The Driver System..\"（startForeground(9906)）",
    "系统无障碍服务列表项：仅显示 android:label=\"Operatör Güncellemesi\"，android:description 缺失（无任何用途说明）",
    "不可取消原生 AlertDialog：ActivityAlert2.onCreate 的 \"HATA!\" / \"Sistem Dosyaları Kaldırılamaz!\"（setCancelable(false)）",
    "按语言本地化的多语言文案表：apps.mustak.sason.b 的静态字段 h/i/j/k/l/m/n/o/p/q/r，写入 SharedPreferences 的 StringActivate / StringAccessibility / StringPermis / StringYes / uninstall1 / uninstall2 / vkladmin / straccessibility，可被服务端下发覆盖",
    "跳转设置前的应用界面：ActivityAccessibility 仅 setContentView(2130968576) 后立即跳转，无可见文字；MainActivity 亦不展示引导",
    "无本地 HTML、无 assets 页面、无远端 WebView 教学页（MainActivity 的 WebView 仅在 b.o 为真时加载 this.b.p，属于变脸外壳而非无障碍教学）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable access for",
      "text_zh": "为……开启访问权限",
      "source_location": "apps.mustak.sason.b 字段 i（[en] 语言位），经 c.b(Context) 写入 SharedPreferences 键 StringAccessibility，由 ServiceToast.onStartCommand 拼成 \"Enable access for 'Operatör Güncellemesi'\"",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "Aktif edin. ",
      "text_zh": "请激活。",
      "source_location": "apps.mustak.sason.b 字段 i（[tr] 语言位），同上路径",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update The Driver System..",
      "text_zh": "正在更新驱动程序系统..",
      "source_location": "apps.mustak.sason.StartWhileGlobal.a()（硬编码 Notification setContentText）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update Google Play Service",
      "text_zh": "更新 Google Play 服务",
      "source_location": "apps.mustak.sason.StartWhileGlobal.onHandleIntent（c.a(this,\"Google\",\"Update Google Play Service\")）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "HATA!",
      "text_zh": "错误！",
      "source_location": "apps.mustak.sason.Activity.ActivityAlert2.onCreate（AlertDialog setTitle，硬编码）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "tr",
      "text_verbatim": "Sistem Dosyaları Kaldırılamaz!",
      "text_zh": "系统文件无法移除！",
      "source_location": "apps.mustak.sason.Activity.ActivityAlert2.onCreate（AlertDialog setMessage，setCancelable(false)，硬编码）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "tr",
      "text_verbatim": "Sistem düzgün çalışmıyor, istatistiklere erişim etkinleştirmeniz gerekir '",
      "text_zh": "系统无法正常运行，您需要开启对统计信息的访问权限『……』",
      "source_location": "apps.mustak.sason.c.d(Context,String) 的 statistic 分支（硬编码，用于 USAGE_ACCESS_SETTINGS 引导，与本无障碍流程同源套路）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "The system does not work correctly, you need to enable access to the statistics '",
      "text_zh": "系统无法正常运行，您需要开启对统计信息的访问权限『……』",
      "source_location": "apps.mustak.sason.c.d(Context,String) 的 statistic 分支（en 硬编码）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "tr",
      "text_verbatim": "İzin almak / Şimdi etkinleştir",
      "text_zh": "获取权限 / 立即启用",
      "source_location": "apps.mustak.sason.c.d(Context,String) statistic 分支的 AlertDialog 标题与按钮文案",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "StartWhileRequest.onHandleIntent 主循环每 700ms 一轮；未获权时 sleep 降至 500ms，重复 startActivity(ActivityAccessibility) + startService(ServiceToast)；计数器 e 累加到 25 后重置为 -1 继续无限循环，只要 c.g(context) 仍为 false 且云端 startRequest 含 \"Access=1\" 就不停止，用户返回系统设置页或拒绝均无法退出",
    "overlay_or_fake_settings": "无半透明遮罩、无高仿系统设置页；但使用 Toast.setGravity(16,0,0) 在屏幕正中叠加系统级 Toast 充当“引导提示”，并在后台拉起无内容的中转 Activity 直跳系统设置页",
    "restricted_settings_13plus_coaching": "无。未发现引导用户进应用详情点右上角菜单开启“受限设置”的文案或分步教学；ACTION_APPLICATION_DETAILS_SETTINGS 仅在 ActivityAlert2 的 deleteApp 分支用于跳本应用详情页（卸载场景）。样本 targetSdkVersion=27，本身不触发 Android 13+ 受限设置拦截，因此无需该教学",
    "post_grant_anti_removal": "有。ServiceAccessibility.a() 先 startActivity(ACTION_MAIN/HOME) 回到桌面，再以 FLAG_ACTIVITY_NEW_TASK|CLEAR_TASK 拉起 ActivityAlert2 弹 setCancelable(false) 的 \"HATA! / Sistem Dosyaları Kaldırılamaz!\" 假系统错误框，阻断用户前往设置关闭服务或卸载；同时 StartWhileGlobal/StartWhileRequest 在锁屏态与后台持续保活，ReceiverBoot 监听 PACKAGE_REMOVED/SCREEN_ON/USER_PRESENT 等重启",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到应用进程拉起 intent=android.settings.ACCESSIBILITY_SETTINGS 的瞬间（来源包 apps.mustak.sason，源 Activity apps.mustak.sason.Activity.ActivityAccessibility）——此时屏幕正中会同时出现 Toast，是最短捕获窗口；若无该 hook，则在冷启动 MainActivity 后 1~2 秒内（图标消失、无界面）直接录屏/截图系统无障碍设置页",
    "key_pages_to_capture": [
      {
        "page_role": "跳转瞬间的居中 Toast + 系统无障碍设置页",
        "page_identifier": "系统设置页 TITLE 含“无障碍/Erişilebilirlik/Accessibility”，同时屏幕中央浮层文本为 \"Enable access for 'Operatör Güncellemesi'\" 或 \"Aktif edin. 'Operatör Güncellemesi'\"",
        "why_most_useful": "这是全流程唯一的口头引导载体，且文案直接暴露“应用在催促开启无障碍”的意图，配合系统设置页可证明是应用主动跳转而非用户自发操作",
        "observable_utg_signals": ["Toast 文本包含应用名 Operatör Güncellemesi 与 Enable access for / Aktif edin 关键字", "Toast 位于屏幕正中（gravity=center）而非底部默认位置", "前台页面包名为 com.android.settings 且标题为无障碍设置"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "列表中出现 \"Operatör Güncellemesi\" 服务项，且该项下方无任何描述文字",
        "why_most_useful": "证明身份伪装（运营商更新名义）与描述缺失，是判定“利用无障碍权限且不告知用途”的直接证据",
        "observable_utg_signals": ["服务名 Operatör Güncellemesi", "该项无 subtitle/description 文本节点", "开关状态为关闭（未获权态）"]
      },
      {
        "page_role": "拒权后的重跳循环页",
        "page_identifier": "从系统设置按返回键后，1 秒内再次回到无障碍设置页，并重复出现居中 Toast",
        "why_most_useful": "证明存在强制循环而非良性降级，是区分“引导”与“逼迫”的关键动态证据",
        "observable_utg_signals": ["返回桌面后 1~2 秒内系统无障碍页被再次拉起", "Toast 文本与上一轮完全一致并重复出现", "同一 Activity 栈反复重建（ActivityAccessibility 无界面即 finish）"]
      },
      {
        "page_role": "获权后的假系统错误弹窗",
        "page_identifier": "屏幕中央 AlertDialog 标题 \"HATA!\"、正文 \"Sistem Dosyaları Kaldırılamaz!\"、单个 \"ОК\" 按钮，且无法通过返回键/点击外部关闭",
        "why_most_useful": "证明获权后立即实施反撤权，是恶意定性而非权限滥用的决定性证据",
        "observable_utg_signals": ["Dialog 文本 HATA! / Sistem Dosyaları Kaldırılamaz!", "按钮文本使用西里尔字母 О（非拉丁 O）", "按返回键与点击外部区域均无法关闭", "Dialog 出现前应用曾拉起 HOME"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区不在 UI：引导文案全部为纯文本 Toast 与系统页，无图片诱导；但存在两点需注意——(1) 文案可由服务端下发覆盖 SharedPreferences（StringAccessibility/StringActivate），实际展示语言随 Locale 变化（tr/en/ru/zh 等 80+ 语言），UTG 规则需按语言表匹配而非固定英文；(2) 冷启动时 MainActivity 会自禁用桌面组件并 finish，无可见界面，若 UTG 仅在 Activity 前台时采样可能漏掉入口，建议在进程启动后即挂 hook 监测 ACCESSIBILITY_SETTINGS 跳转。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "apps.mustak.sason.Activity.ActivityAccessibility.onCreate",
    "apps.mustak.sason.StartWhileRequest.onHandleIntent",
    "apps.mustak.sason.ServiceToast.onStartCommand",
    "apps.mustak.sason.ServiceAccessibility.onServiceConnected",
    "apps.mustak.sason.Activity.ActivityAlert2.onCreate",
    "res/xml/serviceconfig.xml"
  ]
}
```

</details>
