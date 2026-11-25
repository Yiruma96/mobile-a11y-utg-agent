# MB_024__c7411c0daf｜Anubis — Chrome Güncellemesi

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：161.0s

## 1. 一句话核心结论

- **核心申请方式**：伪装成“Chrome Güncellemesi”更新包，启动即自禁桌面图标并常驻 1 秒循环，反复静默跳转系统无障碍设置页、同时用不可取消弹窗恐吓用户去开使用情况访问，并靠自身无障碍服务在 com.android.settings 页面按文本查找节点自动点击勾选本服务，命中卸载关键词则回 HOME 阻止撤权。
- **静态可见性说明**：核心 UTG 流转（启动器自禁用、1 秒循环拉起、静默跳 ACCESSIBILITY_SETTINGS、不可取消的 USAGE_ACCESS_SETTINGS 引导弹窗、无障碍自我点击授权、HOME 反撤权）全部为明文 Java 且完整静态可见，无加壳、无 assets/HTML、无嵌入 a11y APK；仅引导用文案变量（straccessibility/straccessibility2/StringActivate/uninstall1/uninstall2）、远端 WebView URL(b.p) 与部分控制开关由 e-kasimaydin.xyz 的 /o1o/aN.php 服务端下发，无法静态确定最终话术。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c7411c0daff520468c3accff4318076a66034b2d14cbae08a5d3ecec2c6ce9ed` |
| 包名 / 年份 | `wocwvy.czyxoxmbauu.slsa` / 2025 |
| 家族 / 品类 | **Anubis**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome Güncellemesi |
| 引导页宣称品牌/身份 | Google Chrome 浏览器更新 / Android 系统安全（无障碍服务名 Android Security） |
| 系统无障碍列表服务名 | Android Security |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) res/xml/mihaf.xml 完全缺失 android:description，系统无障碍列表仅显示“Android Security”而无任何用途说明；2) 无障碍配置 settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity（模板残留/伪造）；3) 十余个 Activity 统一 android:label="" 且 icon=@drawable/im，界面无标题无标识；4) 首次启动后 setComponentEnabledSetting(myvbo, COMPONENT_DISABLED) 自禁用启动器组件，图标从桌面消失；5) 应用主题为 Theme.Translucent.NoTitleBar，跳转系统设置时无任何可见自有界面。 |
| 无障碍服务类名 | `wocwvy.czyxoxmbauu.slsa.egxltnv` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | wocwvy.czyxoxmbauu.slsa.ncec.myvbo（LAUNCHER Activity，Theme.Translucent.NoTitleBar） | onCreate（用户点击桌面图标“Chrome Güncellemesi”） | 不可静态还原（无任何自有界面，立即 startService + finish） | 无 | 无（用户无任何选择或取消机会） | `wocwvy.czyxoxmbauu.slsa.ncec.myvbo.onCreate` |
| 2 | 拒权反馈循环 | wocwvy.czyxoxmbauu.slsa.ncec.dzudmx（由 jtfxlnc/kldqwysgkfcrmq 循环拉起） | jtfxlnc.onHandleIntent 每 1 秒轮询后 startActivity(dzudmx.class)；b.g() 判定自身无障碍未开启 | 原生Dialog（Activity 内 AlertDialog，setCancelable(false)） | **原文**：Sorry! / You have no permission to use this app! / ОК<br>**译注**：“抱歉！您没有使用本应用的权限！”——仅一个“ОК”按钮，不可取消、不可返回跳过 | 只能点击 ОК 关闭；关闭后循环再次拉起，无取消/跳过/拒绝路径 | `wocwvy.czyxoxmbauu.slsa.ncec.dzudmx.onCreate` |
| 3 | 跳无障碍设置 | wocwvy.czyxoxmbauu.slsa.ncec.fymeshs → 系统 android.settings.ACCESSIBILITY_SETTINGS | kldqwysgkfcrmq.onHandleIntent / jtfxlnc 循环内 startActivity(fymeshs.class)；fymeshs.onCreate 立即 startActivity(ACTION=android.settings.ACCESSIBILITY_SETTINGS) | 系统无障碍页（自有界面仅一行跳转，无说明页） | **原文**：无（应用自身不展示任何文字，直接打开系统“无障碍”设置）<br>**译注**：无前置说明，直接把用户丢到系统无障碍服务列表，让用户在“Android Security”项上自行开启 | 要求用户进入系统无障碍页并开启“Android Security”服务；无取消按钮，异常时仅 finish() | `wocwvy.czyxoxmbauu.slsa.ncec.fymeshs.onCreate` |
| 4 | 遮罩叠层指引 | egxltnv 无障碍服务在 com.android.settings 页面操作 AccessibilityNodeInfo | onAccessibilityEvent（TYPE_WINDOW_STATE_CHANGED/TYPE_WINDOW_CONTENT_CHANGED，用户停留在系统设置页） | 系统无障碍页（以无障碍节点点击替代遮罩，等效于“代用户勾选”） | **原文**：Enable access for / activate / straccessibility(远端可配) / 应用名“Chrome Güncellemesi”<br>**译注**：以“Enable access for”“activate”等文本（可被服务端改写）及本应用名在设置页查找节点，并对匹配节点执行点击，自动打开自身无障碍开关 | 用户无需操作——服务在设置页自动点击完成授权；若用户试图关闭/卸载，则命中 uninstall1/uninstall2 文本后强制回桌面 | `wocwvy.czyxoxmbauu.slsa.egxltnv.onAccessibilityEvent` |
| 5 | 跳受限设置 | wocwvy.czyxoxmbauu.slsa.b.d(Context,String) 弹窗 → android.settings.USAGE_ACCESS_SETTINGS / LOCATION_SOURCE_SETTINGS | 业务侧调用 b.d(ctx,"statistic") / b.d(ctx,"gps")（由 jtfxlnc、ukhakhcgifofl、wifu、cpysnikhf、egxltnv 等多处调用） | 原生Dialog（不可取消 AlertDialog）+ 系统设置页 | **原文**：Get permission / The system does not work correctly, you need to enable access to the statistics '<应用名>' / Enable now<br>**译注**：标题“获取权限”，正文“系统运行不正常，您需要开启对统计信息的访问权限'<应用名>'”，唯一按钮“立即启用” | 只能点“Enable now”跳转使用情况访问设置；setCancelable(false)、无取消/跳过按钮，无 positive 按钮，点击即强制跳转 | `wocwvy.czyxoxmbauu.slsa.b.d + wocwvy.czyxoxmbauu.slsa.b$1.onClick` |
| 6 | 获权后动作 | wocwvy.czyxoxmbauu.slsa.egxltnv.onServiceConnected / onAccessibilityEvent | 系统绑定无障碍服务成功（onServiceConnected）后进入全量事件监听 | 不可静态还原（无界面，后台静默采集） | **原文**：KEY1\|(TEXT)\| / KEY2\|(FOCUSED)\| / KEY3\|(CLICKED)\| / \|Attempt to remove malware 2\| / \|Attempt to remove malware 3\|<br>**译注**：把文本框/焦点/点击内容按时间戳写入 keys.log 并上报（keylogger=true 时），并在 com.android.settings 检测到卸载关键词时上报“尝试移除恶意软件 2/3”并回桌面阻断 | 无（用户已无感知，权限被用于键盘记录、反卸载与后续锁屏/覆盖攻击） | `wocwvy.czyxoxmbauu.slsa.egxltnv.onServiceConnected + wocwvy.czyxoxmbauu.slsa.egxltnv.a()` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：仅由 AndroidManifest 中 service android:label="Android Security" 呈现，res/xml/mihaf.xml 无 android:description，故列表中无任何用途说明文字
- dzudmx Activity 内的不可取消 AlertDialog（标题 Sorry!、正文 You have no permission to use this app!、按钮 ОК）——由 jtfxlnc/kldqwysgkfcrmq 后台循环反复拉起
- b.d(Context,String) 构造的不可取消 AlertDialog（标题 Get permission / 正文 The system does not work correctly, you need to enable access to the statistics '<应用名>' / 唯一按钮 Enable now），点击后跳 USAGE_ACCESS_SETTINGS；同函数另有 Geolocation 版本跳 LOCATION_SOURCE_SETTINGS
- 前台通知：锁屏且 foregroundwhile=true 时以 title=Google、content=Update Google Play Service 伪造系统更新通知（SDK>=26 走 b.a 通知，低版本走 Activity）
- nixcec.fyqapyahei Activity：以 Intent 传入的 title/content 显示 AlertDialog（仅一个 OK 按钮），作为通用弹窗载体
- 全包无 assets 目录、无本地 HTML/WebView 引导页、无自定义引导布局；唯一 WebView 在 myvbo.onCreate 且仅当远端配置 b.o=true 时 loadUrl(远端 b.p)，非本地资源
- 无障碍授权动作本身不呈现任何应用文字，而是由 egxltnv 在 com.android.settings 页面按文本查找节点并点击

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Chrome Güncellemesi | Chrome 更新 | `AndroidManifest.xml application android:label` | 假更新 |
| en | Android Security | 安卓安全 | `AndroidManifest.xml service android:label（b.d 常量 "Android Security"）` | 假反诈安全 |
| en | Sorry! | 抱歉！ | `wocwvy.czyxoxmbauu.slsa.ncec.dzudmx.onCreate` | 故障恐吓 |
| en | You have no permission to use this app! | 您没有使用本应用的权限！ | `wocwvy.czyxoxmbauu.slsa.ncec.dzudmx.onCreate` | 故障恐吓 |
| en | Get permission | 获取权限 | `wocwvy.czyxoxmbauu.slsa.b#d(Context,String)（US/US 分支默认）` | 受限设置分步教学 |
| en | The system does not work correctly, you need to enable access to the statistics '<应用名>' | 系统运行不正常，您需要开启对统计信息的访问权限'<应用名>' | `wocwvy.czyxoxmbauu.slsa.b#d(Context,String)` | 故障恐吓 |
| en | Enable now | 立即启用 | `wocwvy.czyxoxmbauu.slsa.b#d(Context,String)（setNegativeButton 唯一按钮）` | 受限设置分步教学 |
| tr | Sistem düzgün çalışmıyor, istatistiklere erişim etkinleştirmeniz gerekir '<uygulama>' / Şimdi etkinleştir | 系统运行不正常，您需要开启对统计信息的访问'<应用>' / 立即启用 | `wocwvy.czyxoxmbauu.slsa.b#d(Context,String)（TR 分支，匹配本机土耳其语环境）` | 故障恐吓 |
| en | Enable access for | 为以下对象启用访问权限： | `wocwvy.czyxoxmbauu.slsa.b#b（SharedPreferences StringAccessibility 默认值）及 a.h/a.i 多语言数组` | 受限设置分步教学 |
| en | activate | 激活 | `wocwvy.czyxoxmbauu.slsa.b#b（StringActivate 默认值）` | 受限设置分步教学 |
| en | Update Google Play Service | 更新 Google Play 服务 | `wocwvy.czyxoxmbauu.slsa.jtfxlnc.onHandleIntent（b.a(ctx,"Google","Update Google Play Service")）` | 假更新 |
| en | Attempt to remove malware 2 / Attempt to remove malware 3 | 尝试移除恶意软件 2 / 尝试移除恶意软件 3 | `wocwvy.czyxoxmbauu.slsa.egxltnv.onAccessibilityEvent（上报串，命中 uninstall1/uninstall2 后发送）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：jtfxlnc.onHandleIntent 以 TimeUnit.MILLISECONDS.sleep(1000) 常驻死循环（同时 startAlarm 每 10 秒重置），每轮先用 b.g() 检查自身无障碍是否已启用，未启用即 startActivity(fymeshs) 重新静默跳 ACCESSIBILITY_SETTINGS，并叠加 dzudmx 的不可取消“Sorry!”弹窗；用户从设置页返回只会被再次拉起，无降级路径。
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗遮罩、无高仿系统无障碍开关页；但用更隐蔽的等效手段——自身无障碍服务在 com.android.settings 页面 findAccessibilityNodeInfosByText 后直接点击节点完成“代勾选”，并以 ACTION_MAIN+HOME 强制退出设置页。
- **Android 13+ 受限设置（Restricted Settings）应对**：有（使用情况访问维度）：b.d(ctx,"statistic") 以不可取消弹窗“The system does not work correctly, you need to enable access to the statistics '<应用名>'+Enable now”引导跳 android.settings.USAGE_ACCESS_SETTINGS；未发现 ACTION_APPLICATION_DETAILS_SETTINGS 右上角菜单/Session 安装器式受限设置教学。
- **获权后即时行为与防撤权机制**：有：egxltnv.onAccessibilityEvent 在 com.android.settings 中命中 uninstall1/uninstall2（远端下发）文本即调用 a() 发出 ACTION_MAIN+CATEGORY_HOME 回桌面，并上报“|Attempt to remove malware 2|/|Attempt to remove malware 3|”阻断卸载与撤权；此外 onServiceConnected 后置 eventTypes=-1 全量监听并启动 keys.log 键盘记录。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到当前前台包为 com.android.settings 且 Intent 为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（由 fymeshs.onCreate 触发）立即抓取；同时在冷启动后 0–3 秒内捕获首个自有弹窗（dzudmx“Sorry!”或 b.d“Get permission”）以及随后 1 秒一次的重复拉起事件。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图/空文本外壳：所有诱导文案均为明文（AlertDialog 与多语言字符串数组）。真实盲区是“授权动作发生在系统设置页、由应用自身无障碍节点点击完成”，若 UTG 只在应用自有界面采集，会看不到任何诱导文本，必须在 com.android.settings 前台期间同步抓取；另有服务端下发的 straccessibility*/uninstall1/2 与 WebView URL 需联网才可见，离线抓包会退化为英文默认值。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首个恐吓弹窗页（拒权反馈循环入口）** | Activity wocwvy.czyxoxmbauu.slsa.ncec.dzudmx 的 AlertDialog：标题 Sorry!、正文 You have no permission to use this app!、唯一按钮 ОК | 这是唯一真正呈现在用户眼前的诱导/恐吓文本，且由后台定时器每 1 秒重复拉起，可直接证明“无取消路径 + 循环施压”的胁迫性质。 | 弹窗文本 Sorry! / You have no permission to use this app!；仅存在一个 ОК 按钮且无取消/返回按钮；同一弹窗在数十秒内被反复拉起（时间戳密集）；弹窗背后无任何自有业务界面（透明主题） |
| **跳转后的系统无障碍服务列表项** | 系统“无障碍 → 已下载的服务”页面中 label 为 Android Security 的条目，其下无任何描述文字 | 证明应用把用户直接丢到系统授权页，服务名伪装成“Android Security”且无 android:description 说明，用户无法判断真实用途；同时可观测该条目是否被“自动点亮”。 | 服务名 Android Security 且描述区为空；页面在应用无任何自有 UI 情况下被突然打开；条目开关在用户未点击时被置为开启（自我点击授权）；页面在数秒内被强制退回桌面（HOME） |
| **受限设置（使用情况访问）引导弹窗页** | wocwvy.czyxoxmbauu.slsa.b.d 构造的 AlertDialog：Get permission / The system does not work correctly, you need to enable access to the statistics '<应用名>' / Enable now | 体现“系统故障”话术 + 不可取消 + 唯一跳转按钮的受限权限引导模板，是判定故障恐吓与强制跳转的关键页面。 | 标题 Get permission、正文含 does not work correctly；仅一个 Enable now 按钮，无取消按钮；点击后前台立即切至 android.settings.USAGE_ACCESS_SETTINGS；弹窗以应用图标 2130837504 展示，冒充系统提示 |
| **锁屏态假更新通知** | 通知栏项 title=Google、content=Update Google Play Service（仅在 keyguard 锁屏且 foregroundwhile=true 时） | 证明后台在锁屏态以 Google 官方更新名义重新拉起用户，构成品牌冒充与后台再激活触发点。 | 通知标题 Google、正文 Update Google Play Service；通知来源包名为 wocwvy.czyxoxmbauu.slsa；锁屏状态下周期性出现 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `wocwvy.czyxoxmbauu.slsa.ncec.myvbo.onCreate`
- `wocwvy.czyxoxmbauu.slsa.jtfxlnc.onHandleIntent`
- `wocwvy.czyxoxmbauu.slsa.ncec.fymeshs.onCreate`
- `wocwvy.czyxoxmbauu.slsa.b#d(Context,String)`
- `wocwvy.czyxoxmbauu.slsa.egxltnv.onAccessibilityEvent`
- `res/xml/mihaf.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验）

**总体：静态可见性较高（核心 UTG 流转完全可静态还原），恶意意图明确，属 Anubis 银行木马家族的“无障碍自动授权 + 反卸载”实现。**

**引导链路（运行期 UTG 视角）**
1. **冷启动无引导页**：桌面入口 [myvbo.onCreate()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.ncec.myvbo#onCreate>) 不做任何说明，直接 `startService(jtfxlnc)`，随即 `setComponentEnabledSetting(myvbo, 2, 1)` **自禁用启动图标**（图标消失、无法再找到入口），并 `startAlarm(10000)` 后 `finish()`。远端配置 `b.o` 为真时才改载 WebView(`b.p` 远端 URL)。
2. **后台定时循环拉起**：[jtfxlnc.onHandleIntent()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent>) 以 1 秒 `TimeUnit.sleep` 死循环常驻，循环体内：检查自身无障碍是否已开启（[b.g()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.b#g>) 读 `getEnabledAccessibilityServiceList`）→ 未开则拉起 `dzudmx`（恐吓弹窗）、`fymeshs`（**直接跳无障碍设置**）、锁屏注入 Activity；锁屏时以 `"Google"/"Update Google Play Service"` 发假更新通知。
3. **跳无障碍设置无任何前置说明页**：[fymeshs.onCreate()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.ncec.fymeshs#onCreate>) 仅一行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，异常才 `finish()`。**全包无 `assets/`、无本地 HTML、无自定义引导布局**（解包目录仅 Manifest/classes.dex/res）。
4. **“自己点自己”——用无障碍自我授权**：[egxltnv.onAccessibilityEvent()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.egxltnv#onAccessibilityEvent>) 在 `com.android.settings` 页面用 `findAccessibilityNodeInfosByText` 按 `StringAccessibility("Enable access for")`、`StringActivate("activate")`、远端 `straccessibility/straccessibility2` 及本应用名（`b.i()` 取 `getApplicationLabel` = “Chrome Güncellemesi”）搜索节点并点击，**模拟用户在设置页勾选本服务**。
5. **拒权/撤权对抗**：同一事件回调里命中 `uninstall1/uninstall2` 文本（远端下发，代码内置上报串 `|Attempt to remove malware 2|`、`|Attempt to remove malware 3|`）即执行 `a()` → `ACTION_MAIN + CATEGORY_HOME` **强制退出设置页**，中断卸载/关权限操作。
6. **受限设置（使用情况访问）分步教学**：[b.d(Context,String)](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.b#d>) 构造 `setCancelable(false)` 的 **不可取消 AlertDialog**，标题 “Get permission”，正文 “The system does not work correctly, you need to enable access to the statistics '<应用名>'”，**唯一按钮**（`setNegativeButton`，无 positive/无取消）为 “Enable now” → 跳 `android.settings.USAGE_ACCESS_SETTINGS`；同法对 GPS 跳 `LOCATION_SOURCE_SETTINGS`。
7. **身份伪装**：桌面名 `Chrome Güncellemesi`（土耳其语“Chrome 更新”），无障碍列表服务名 `Android Security`，而 `res/xml/mihaf.xml` **无 `android:description`**（系统列表里无任何用途说明，规避审查与用户判断），且 `settingsActivity` 指向不存在的 `com.example.root.myapplication.MainActivity`（模板残留/伪造）。
8. **获权后**：[onServiceConnected()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.egxltnv#onServiceConnected>) 置 `eventTypes=-1`、`flags=1` 全量监听，按 `keylogger` 配置记录按键至 `keys.log` 并回传 `e-kasimaydin.xyz`。

**未决/覆盖边界**：远端 `/o1o/a3.php` 系列下发的 `straccessibility*`、`StringActivate`、`uninstall1/2` 与 WebView URL 未运行，其具体诱导文案无法静态确定（但“英文/多语言 `Enable access for`”等内置默认值已足以定性）；本轮未做动态 UTG 实测。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "核心 UTG 流转（启动器自禁用、1 秒循环拉起、静默跳 ACCESSIBILITY_SETTINGS、不可取消的 USAGE_ACCESS_SETTINGS 引导弹窗、无障碍自我点击授权、HOME 反撤权）全部为明文 Java 且完整静态可见，无加壳、无 assets/HTML、无嵌入 a11y APK；仅引导用文案变量（straccessibility/straccessibility2/StringActivate/uninstall1/uninstall2）、远端 WebView URL(b.p) 与部分控制开关由 e-kasimaydin.xyz 的 /o1o/aN.php 服务端下发，无法静态确定最终话术。",
  "summary_one_liner": "伪装成“Chrome Güncellemesi”更新包，启动即自禁桌面图标并常驻 1 秒循环，反复静默跳转系统无障碍设置页、同时用不可取消弹窗恐吓用户去开使用情况访问，并靠自身无障碍服务在 com.android.settings 页面按文本查找节点自动点击勾选本服务，命中卸载关键词则回 HOME 阻止撤权。",
  "disguise_identity": {
    "app_display_name": "Chrome Güncellemesi",
    "claimed_brand_or_persona": "Google Chrome 浏览器更新 / Android 系统安全（无障碍服务名 Android Security）",
    "a11y_service_label": "Android Security",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) res/xml/mihaf.xml 完全缺失 android:description，系统无障碍列表仅显示“Android Security”而无任何用途说明；2) 无障碍配置 settingsActivity 指向不存在的 com.example.root.myapplication.MainActivity（模板残留/伪造）；3) 十余个 Activity 统一 android:label=\"\" 且 icon=@drawable/im，界面无标题无标识；4) 首次启动后 setComponentEnabledSetting(myvbo, COMPONENT_DISABLED) 自禁用启动器组件，图标从桌面消失；5) 应用主题为 Theme.Translucent.NoTitleBar，跳转系统设置时无任何可见自有界面。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.ncec.myvbo（LAUNCHER Activity，Theme.Translucent.NoTitleBar）",
      "trigger_event": "onCreate（用户点击桌面图标“Chrome Güncellemesi”）",
      "ui_carrier": "不可静态还原（无任何自有界面，立即 startService + finish）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不展示任何界面或说明，直接转入后台服务并关闭自身",
      "user_action_requested": "无（用户无任何选择或取消机会）",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.ncec.myvbo.onCreate"
    },
    {
      "step": 2,
      "stage": "拒权反馈循环",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.ncec.dzudmx（由 jtfxlnc/kldqwysgkfcrmq 循环拉起）",
      "trigger_event": "jtfxlnc.onHandleIntent 每 1 秒轮询后 startActivity(dzudmx.class)；b.g() 判定自身无障碍未开启",
      "ui_carrier": "原生Dialog（Activity 内 AlertDialog，setCancelable(false)）",
      "shown_text_verbatim": "Sorry! / You have no permission to use this app! / ОК",
      "shown_text_zh": "“抱歉！您没有使用本应用的权限！”——仅一个“ОК”按钮，不可取消、不可返回跳过",
      "user_action_requested": "只能点击 ОК 关闭；关闭后循环再次拉起，无取消/跳过/拒绝路径",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.ncec.dzudmx.onCreate"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.ncec.fymeshs → 系统 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "kldqwysgkfcrmq.onHandleIntent / jtfxlnc 循环内 startActivity(fymeshs.class)；fymeshs.onCreate 立即 startActivity(ACTION=android.settings.ACCESSIBILITY_SETTINGS)",
      "ui_carrier": "系统无障碍页（自有界面仅一行跳转，无说明页）",
      "shown_text_verbatim": "无（应用自身不展示任何文字，直接打开系统“无障碍”设置）",
      "shown_text_zh": "无前置说明，直接把用户丢到系统无障碍服务列表，让用户在“Android Security”项上自行开启",
      "user_action_requested": "要求用户进入系统无障碍页并开启“Android Security”服务；无取消按钮，异常时仅 finish()",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.ncec.fymeshs.onCreate"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "egxltnv 无障碍服务在 com.android.settings 页面操作 AccessibilityNodeInfo",
      "trigger_event": "onAccessibilityEvent（TYPE_WINDOW_STATE_CHANGED/TYPE_WINDOW_CONTENT_CHANGED，用户停留在系统设置页）",
      "ui_carrier": "系统无障碍页（以无障碍节点点击替代遮罩，等效于“代用户勾选”）",
      "shown_text_verbatim": "Enable access for / activate / straccessibility(远端可配) / 应用名“Chrome Güncellemesi”",
      "shown_text_zh": "以“Enable access for”“activate”等文本（可被服务端改写）及本应用名在设置页查找节点，并对匹配节点执行点击，自动打开自身无障碍开关",
      "user_action_requested": "用户无需操作——服务在设置页自动点击完成授权；若用户试图关闭/卸载，则命中 uninstall1/uninstall2 文本后强制回桌面",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.egxltnv.onAccessibilityEvent"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.b.d(Context,String) 弹窗 → android.settings.USAGE_ACCESS_SETTINGS / LOCATION_SOURCE_SETTINGS",
      "trigger_event": "业务侧调用 b.d(ctx,\"statistic\") / b.d(ctx,\"gps\")（由 jtfxlnc、ukhakhcgifofl、wifu、cpysnikhf、egxltnv 等多处调用）",
      "ui_carrier": "原生Dialog（不可取消 AlertDialog）+ 系统设置页",
      "shown_text_verbatim": "Get permission / The system does not work correctly, you need to enable access to the statistics '<应用名>' / Enable now",
      "shown_text_zh": "标题“获取权限”，正文“系统运行不正常，您需要开启对统计信息的访问权限'<应用名>'”，唯一按钮“立即启用”",
      "user_action_requested": "只能点“Enable now”跳转使用情况访问设置；setCancelable(false)、无取消/跳过按钮，无 positive 按钮，点击即强制跳转",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.b.d + wocwvy.czyxoxmbauu.slsa.b$1.onClick"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.egxltnv.onServiceConnected / onAccessibilityEvent",
      "trigger_event": "系统绑定无障碍服务成功（onServiceConnected）后进入全量事件监听",
      "ui_carrier": "不可静态还原（无界面，后台静默采集）",
      "shown_text_verbatim": "KEY1|(TEXT)| / KEY2|(FOCUSED)| / KEY3|(CLICKED)| / |Attempt to remove malware 2| / |Attempt to remove malware 3|",
      "shown_text_zh": "把文本框/焦点/点击内容按时间戳写入 keys.log 并上报（keylogger=true 时），并在 com.android.settings 检测到卸载关键词时上报“尝试移除恶意软件 2/3”并回桌面阻断",
      "user_action_requested": "无（用户已无感知，权限被用于键盘记录、反卸载与后续锁屏/覆盖攻击）",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.egxltnv.onServiceConnected + wocwvy.czyxoxmbauu.slsa.egxltnv.a()"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：仅由 AndroidManifest 中 service android:label=\"Android Security\" 呈现，res/xml/mihaf.xml 无 android:description，故列表中无任何用途说明文字",
    "dzudmx Activity 内的不可取消 AlertDialog（标题 Sorry!、正文 You have no permission to use this app!、按钮 ОК）——由 jtfxlnc/kldqwysgkfcrmq 后台循环反复拉起",
    "b.d(Context,String) 构造的不可取消 AlertDialog（标题 Get permission / 正文 The system does not work correctly, you need to enable access to the statistics '<应用名>' / 唯一按钮 Enable now），点击后跳 USAGE_ACCESS_SETTINGS；同函数另有 Geolocation 版本跳 LOCATION_SOURCE_SETTINGS",
    "前台通知：锁屏且 foregroundwhile=true 时以 title=Google、content=Update Google Play Service 伪造系统更新通知（SDK>=26 走 b.a 通知，低版本走 Activity）",
    "nixcec.fyqapyahei Activity：以 Intent 传入的 title/content 显示 AlertDialog（仅一个 OK 按钮），作为通用弹窗载体",
    "全包无 assets 目录、无本地 HTML/WebView 引导页、无自定义引导布局；唯一 WebView 在 myvbo.onCreate 且仅当远端配置 b.o=true 时 loadUrl(远端 b.p)，非本地资源",
    "无障碍授权动作本身不呈现任何应用文字，而是由 egxltnv 在 com.android.settings 页面按文本查找节点并点击"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Chrome Güncellemesi",
      "text_zh": "Chrome 更新",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Security",
      "text_zh": "安卓安全",
      "source_location": "AndroidManifest.xml service android:label（b.d 常量 \"Android Security\"）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Sorry!",
      "text_zh": "抱歉！",
      "source_location": "wocwvy.czyxoxmbauu.slsa.ncec.dzudmx.onCreate",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "You have no permission to use this app!",
      "text_zh": "您没有使用本应用的权限！",
      "source_location": "wocwvy.czyxoxmbauu.slsa.ncec.dzudmx.onCreate",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Get permission",
      "text_zh": "获取权限",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#d(Context,String)（US/US 分支默认）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The system does not work correctly, you need to enable access to the statistics '<应用名>'",
      "text_zh": "系统运行不正常，您需要开启对统计信息的访问权限'<应用名>'",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#d(Context,String)",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable now",
      "text_zh": "立即启用",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#d(Context,String)（setNegativeButton 唯一按钮）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Sistem düzgün çalışmıyor, istatistiklere erişim etkinleştirmeniz gerekir '<uygulama>' / Şimdi etkinleştir",
      "text_zh": "系统运行不正常，您需要开启对统计信息的访问'<应用>' / 立即启用",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#d(Context,String)（TR 分支，匹配本机土耳其语环境）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable access for",
      "text_zh": "为以下对象启用访问权限：",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#b（SharedPreferences StringAccessibility 默认值）及 a.h/a.i 多语言数组",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "activate",
      "text_zh": "激活",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#b（StringActivate 默认值）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Update Google Play Service",
      "text_zh": "更新 Google Play 服务",
      "source_location": "wocwvy.czyxoxmbauu.slsa.jtfxlnc.onHandleIntent（b.a(ctx,\"Google\",\"Update Google Play Service\")）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Attempt to remove malware 2 / Attempt to remove malware 3",
      "text_zh": "尝试移除恶意软件 2 / 尝试移除恶意软件 3",
      "source_location": "wocwvy.czyxoxmbauu.slsa.egxltnv.onAccessibilityEvent（上报串，命中 uninstall1/uninstall2 后发送）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "jtfxlnc.onHandleIntent 以 TimeUnit.MILLISECONDS.sleep(1000) 常驻死循环（同时 startAlarm 每 10 秒重置），每轮先用 b.g() 检查自身无障碍是否已启用，未启用即 startActivity(fymeshs) 重新静默跳 ACCESSIBILITY_SETTINGS，并叠加 dzudmx 的不可取消“Sorry!”弹窗；用户从设置页返回只会被再次拉起，无降级路径。",
    "overlay_or_fake_settings": "无悬浮窗遮罩、无高仿系统无障碍开关页；但用更隐蔽的等效手段——自身无障碍服务在 com.android.settings 页面 findAccessibilityNodeInfosByText 后直接点击节点完成“代勾选”，并以 ACTION_MAIN+HOME 强制退出设置页。",
    "restricted_settings_13plus_coaching": "有（使用情况访问维度）：b.d(ctx,\"statistic\") 以不可取消弹窗“The system does not work correctly, you need to enable access to the statistics '<应用名>'+Enable now”引导跳 android.settings.USAGE_ACCESS_SETTINGS；未发现 ACTION_APPLICATION_DETAILS_SETTINGS 右上角菜单/Session 安装器式受限设置教学。",
    "post_grant_anti_removal": "有：egxltnv.onAccessibilityEvent 在 com.android.settings 中命中 uninstall1/uninstall2（远端下发）文本即调用 a() 发出 ACTION_MAIN+CATEGORY_HOME 回桌面，并上报“|Attempt to remove malware 2|/|Attempt to remove malware 3|”阻断卸载与撤权；此外 onServiceConnected 后置 eventTypes=-1 全量监听并启动 keys.log 键盘记录。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到当前前台包为 com.android.settings 且 Intent 为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（由 fymeshs.onCreate 触发）立即抓取；同时在冷启动后 0–3 秒内捕获首个自有弹窗（dzudmx“Sorry!”或 b.d“Get permission”）以及随后 1 秒一次的重复拉起事件。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首个恐吓弹窗页（拒权反馈循环入口）",
        "page_identifier": "Activity wocwvy.czyxoxmbauu.slsa.ncec.dzudmx 的 AlertDialog：标题 Sorry!、正文 You have no permission to use this app!、唯一按钮 ОК",
        "why_most_useful": "这是唯一真正呈现在用户眼前的诱导/恐吓文本，且由后台定时器每 1 秒重复拉起，可直接证明“无取消路径 + 循环施压”的胁迫性质。",
        "observable_utg_signals": ["弹窗文本 Sorry! / You have no permission to use this app!", "仅存在一个 ОК 按钮且无取消/返回按钮", "同一弹窗在数十秒内被反复拉起（时间戳密集）", "弹窗背后无任何自有业务界面（透明主题）"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "系统“无障碍 → 已下载的服务”页面中 label 为 Android Security 的条目，其下无任何描述文字",
        "why_most_useful": "证明应用把用户直接丢到系统授权页，服务名伪装成“Android Security”且无 android:description 说明，用户无法判断真实用途；同时可观测该条目是否被“自动点亮”。",
        "observable_utg_signals": ["服务名 Android Security 且描述区为空", "页面在应用无任何自有 UI 情况下被突然打开", "条目开关在用户未点击时被置为开启（自我点击授权）", "页面在数秒内被强制退回桌面（HOME）"]
      },
      {
        "page_role": "受限设置（使用情况访问）引导弹窗页",
        "page_identifier": "wocwvy.czyxoxmbauu.slsa.b.d 构造的 AlertDialog：Get permission / The system does not work correctly, you need to enable access to the statistics '<应用名>' / Enable now",
        "why_most_useful": "体现“系统故障”话术 + 不可取消 + 唯一跳转按钮的受限权限引导模板，是判定故障恐吓与强制跳转的关键页面。",
        "observable_utg_signals": ["标题 Get permission、正文含 does not work correctly", "仅一个 Enable now 按钮，无取消按钮", "点击后前台立即切至 android.settings.USAGE_ACCESS_SETTINGS", "弹窗以应用图标 2130837504 展示，冒充系统提示"]
      },
      {
        "page_role": "锁屏态假更新通知",
        "page_identifier": "通知栏项 title=Google、content=Update Google Play Service（仅在 keyguard 锁屏且 foregroundwhile=true 时）",
        "why_most_useful": "证明后台在锁屏态以 Google 官方更新名义重新拉起用户，构成品牌冒充与后台再激活触发点。",
        "observable_utg_signals": ["通知标题 Google、正文 Update Google Play Service", "通知来源包名为 wocwvy.czyxoxmbauu.slsa", "锁屏状态下周期性出现"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图/空文本外壳：所有诱导文案均为明文（AlertDialog 与多语言字符串数组）。真实盲区是“授权动作发生在系统设置页、由应用自身无障碍节点点击完成”，若 UTG 只在应用自有界面采集，会看不到任何诱导文本，必须在 com.android.settings 前台期间同步抓取；另有服务端下发的 straccessibility*/uninstall1/2 与 WebView URL 需联网才可见，离线抓包会退化为英文默认值。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "wocwvy.czyxoxmbauu.slsa.ncec.myvbo.onCreate",
    "wocwvy.czyxoxmbauu.slsa.jtfxlnc.onHandleIntent",
    "wocwvy.czyxoxmbauu.slsa.ncec.fymeshs.onCreate",
    "wocwvy.czyxoxmbauu.slsa.b#d(Context,String)",
    "wocwvy.czyxoxmbauu.slsa.egxltnv.onAccessibilityEvent",
    "res/xml/mihaf.xml"
  ]
}
```

</details>
