# MB_089__bc0b22a27d｜Hook — BBVA

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：168.9s

## 1. 一句话核心结论

- **核心申请方式**：冒充 BBVA 银行的空白图标应用，冷启动即弹出系统级全屏 WebView 悬浮层，权限拿全后强跳系统无障碍设置并在其上叠加自制教学遮罩，靠 onResume/2 秒定时器死循环重跳、屏蔽返回与主页键逼用户开启无障碍，获权后再去拉起真实银行/社交 App 供其读屏代点。
- **静态可见性说明**：Manifest、无障碍配置 res/xml/yeka.xml、strings.xml 与全部 Java/Kotlin 控制流完全静态可见；但两处引导页 HTML 正文（vixabafi$Companion$s227$2 / s228$2 的 invoke()）在 DEX 中反编译为空字符串，实际页面文案无法静态还原，需运行期从 WebView loadDataWithBaseURL 抓取。未发现加壳或 VMP。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `bc0b22a27dc2865e3194c23a0555fb791a17da00ed8935b7d0a118262c786f0b` |
| 包名 / 年份 | `com.fisececitinoje.lalole` / 2024 |
| 家族 / 品类 | **Hook**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | BBVA |
| 引导页宣称品牌/身份 | BBVA（西班牙对外银行）及 Facebook / Google Play / Gmail / WhatsApp / Instagram / TikTok / Telegram / Chrome / YouTube / Contacts 等被冒充应用 |
| 系统无障碍列表服务名 | BBVA4 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍服务标签为 BBVA4，与桌面名 BBVA 不一致（数字后缀规避同名比对）；2) 11 个 activity-alias（Facebook/Google Play/Gmail/WhatsApp/Instagram/TikTok/Telegram/Chrome/Youtube/Contacts）全部 targetActivity 指向同一空白 Launcher，可运行期 enableIcon/disableAll 切换图标与名称；3) 主 Launcher 用 Theme.Translucent.NoTitleBar + @style/ACL + noHistory + excludeFromRecents，界面仅一个空格 TextView；4) onKeyDown 直接 return true 吞掉 HOME(3)/BACK(4)/MENU(82) 键；5) 无障碍 description 用一句话把用户注意力从授权风险引向『先关再开』；6) 无障碍配置声明 typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRequestFilterKeyEvents、flagRetrieveInteractiveWindows，远超任何合理用途。 |
| 无障碍服务类名 | `com.pucovilejedilizu.cerodu.gehaxepojilo.xobopabepuwi` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | If accessibility permission has been on, please turn off then turn on. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.fisececitinoje.lalole.yamixesojotawe（MAIN/LAUNCHER，@style/ACL 半透明主题） | onCreate → hasAllPermission() 为 false → Payload.INSTANCE.start2(this) | 原生Activity | 仅一个空格（setContentView(new TextView) 设文本为 " "），界面实质空白 | 无提示、无按钮，用户看不到任何说明即被带向下一页 | `com.fisececitinoje.lalole.yamixesojotawe.onCreate` |
| 2 | 引导说明页 | com.pucovilejedilizu.cerodu.vixabafi（exported=false，Window.setType(2006) 系统级悬浮窗，全屏 WebView） | onResume() → work()；无障碍未启用且 launchHttp=true 时创建 WebView 并 addView 到 WindowManager | 悬浮窗Overlay | **原文**：无（HTML 由 Base64.decode(getS227()) 解码后 loadDataWithBaseURL 加载，静态为空串，需运行期抓取）<br>**译注**：运行期从 DEX 内 Base64 常量解码的 HTML 引导页，内容静态不可还原 | 由 HTML 内 JS 经 addJavascriptInterface(..., "Android") 回调 WebAppInterface.onData 触发后续跳转，页面按钮文案需运行期确认 | `com.pucovilejedilizu.cerodu.vixabafi.work / vixabafi$WebAppInterface.onData` |
| 3 | 跳受限设置 | 系统「应用信息」页（android.settings.APPLICATION_DETAILS_SETTINGS + package uri） | 运行时权限与悬浮窗权限均满足后，work$1$3 协程执行 invokeSuspend$lambda-2：new Intent(APPLICATION_DETAILS_SETTINGS).addFlags(...).setData(Uri.fromParts("package", getPackageName(), null))，并 setClickAutoStart(false)、setStartAppDetail(true) | 系统无障碍页 | 无 | 要求用户在应用详情页右上角菜单中允许受限设置（具体措辞在不可静态还原的 HTML 内） | `com.pucovilejedilizu.cerodu.vixabafi$work$1$3#invokeSuspend$lambda-2` |
| 4 | 跳无障碍设置 | 系统「无障碍」设置页 + 立即压栈的 com.pucovilejedilizu.cerodu.focigisega.kerafehocu | openAccessabilitySettings()（由 WebView JS 桥或 work() 的 else 分支调用）先销毁悬浮 WebView，再 rotu.gotoAccessibilityService(this) | 系统无障碍页 | 无 | 要求用户在无障碍列表中找到并开启 BBVA4 服务 | `com.pucovilejedilizu.cerodu.tiwehemahosi.rotu.gotoAccessibilityService / vixabafi.openAccessabilitySettings` |
| 5 | 遮罩叠层指引 | com.pucovilejedilizu.cerodu.focigisega.kerafehocu（exported=true，noHistory，@style/ACL），WindowManager 全屏 WebView（Xiaomi 且 SDK>=29 时改为 gravity=80、高度 -2 底部条） | kerafehocu.onCreate → Base64.decode(getS228()) → 替换 <html lang> 与语言占位符 → loadDataWithBaseURL → getWm().addView(webView, LayoutParams(-1, -2, 2, 262152, -3)) | 悬浮窗Overlay | **原文**：无（s228 静态解码为空串，HTML 正文需运行期抓取）<br>**译注**：覆盖在系统无障碍设置页之上的图文/网页指引层，无系统原生返回按钮 | 要求用户按指引点击列表中对应服务；onBackPressed 仅在 WebView canGoBack 时回退，否则放行 | `com.pucovilejedilizu.cerodu.focigisega.kerafehocu.onCreate` |
| 6 | 拒权反馈循环 | vixabafi.onResume / rotu.ensureAccessibilityServiceEnabled 定时重跳 | 用户从设置页返回 → vixabafi.onResume() 无条件 work()；ensureAccessibilityServiceEnabled 在服务未启用时 Handler.postDelayed(gotoAccessibilityService, 2000) 并再挂 exitWrapper/enterWrapper；vixabafi.onKeyDown 对 keyCode 3/4/82 一律 return true；onBackPressed() 改为 work() | 系统无障碍页 | 无 | 无取消、无跳过、无降级路径，只能开启服务 | `com.pucovilejedilizu.cerodu.vixabafi.onResume / onKeyDown / onBackPressed；com.pucovilejedilizu.cerodu.tiwehemahosi.rotu.ensureAccessibilityServiceEnabled` |
| 7 | 获权后动作 | yamixesojotawe.successWork / startApplication / enableIcon / disableAll | 无障碍已启用 → work() 依次检查通知使用权(DrawerSniffer.hasPermission)、全部运行时权限、悬浮窗、电池优化豁免，逐项循环请求；随后 successWork() 按 appToStart 与内置包名清单 getLaunchIntentForPackage 拉起目标应用，并切换图标别名 | 原生Activity | 无 | 无额外交互，用户在真实 App 内的操作被无障碍服务接管 | `com.fisececitinoje.lalole.yamixesojotawe.successWork` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml:33 → text_accessibility_service_description = "If accessibility permission has been on, please turn off then turn on."，经 res/xml/yeka.xml 的 android:description 引用，显示在系统「无障碍」服务列表条目下方
- AndroidManifest.xml service 节点 android:label="BBVA4"，即系统无障碍列表中呈现的服务名
- AndroidManifest.xml application android:label="BBVA" + @mipmap/ic_launcher，桌面图标名称
- 11 个 activity-alias 的 android:label（Facebook / Google Play / Gmail / WhatsApp / Instagram / TikTok / Telegram / Chrome / Youtube / Contacts），可运行期启用以替换桌面名称与图标
- com.pucovilejedilizu.cerodu.vixabafi#work 中由 Base64 常量 s227 解码并 loadDataWithBaseURL 的全屏悬浮 WebView（引导主页，正文静态不可还原）
- com.pucovilejedilizu.cerodu.focigisega.kerafehocu#onCreate 中由 Base64 常量 s228 解码的全屏/底部 WebView，用 WindowManager 直接压在系统无障碍设置页之上（遮罩教学页，正文静态不可还原）
- com.fisececitinoje.lalole.yamixesojotawe#onCreate 的 setContentView(new TextView(" "))，即桌面点击后用户唯一看到的原生界面（一个空格）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经处于开启状态，请先关闭再重新打开。 | `res/values/strings.xml#text_accessibility_service_description（经 res/xml/yeka.xml android:description 引用）` | 教唆忽视警告 |
| en | BBVA4 | BBVA4（系统无障碍服务列表中显示的服务名，仿冒 BBVA 银行并在末尾加数字） | `AndroidManifest.xml service com.pucovilejedilizu.cerodu.gehaxepojilo.xobopabepuwi android:label；常量 com.pucovilejedilizu.cerodu.tiwehemahosi.kutohitetazi.access1/access2` | 假反诈安全 |
| en | BBVA | BBVA（桌面应用名，冒充西班牙对外银行） | `AndroidManifest.xml application android:label` | 未知 |
| en | Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram | 脸书 / 谷歌应用商店 / 谷歌邮箱 / 通讯录 / WhatsApp / YouTube / 谷歌浏览器 / Instagram / TikTok / Telegram（activity-alias 可切换的伪装名称） | `AndroidManifest.xml 各 activity-alias android:label 及 @drawable/ic_facebook、ic_google_play、ic_gmail、ic_contacts、ic_whatsapp、ic_youtube、ic_chrome、ic_instagram、ic_tiktok、ic_telegram` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：vixabafi.onResume() 每次回到前台无条件执行 work()，若无障碍未启用则重开全屏悬浮 WebView；rotu.ensureAccessibilityServiceEnabled 在检测到服务未启用时用 cucibi.getMainHandler().postDelayed(gotoAccessibilityService, 2000) 周期性重新跳转 ACCESSIBILITY_SETTINGS，并以 2000ms 的 enterWrapper/exitWrapper 包裹成功/失败回调；onBackPressed() 不退出而是再次 work()；onKeyDown 对 HOME(3)/BACK(4)/MENU(82) 直接返回 true 屏蔽，用户无法用返回或主页键逃离。
- **遮罩叠层 / 高仿系统设置页**：有。两处 WindowManager 悬浮 WebView：vixabafi 用 WindowManager.LayoutParams(-1, -1, 2, 262144, -2) 全屏覆盖；kerafehocu 在跳转系统无障碍设置后立即压栈，参数 (-1, -2, 2, 262152, -3)，Xiaomi 且 SDK>=29 时 gravity=80 改为底部条状贴边指引，均为自制 HTML 而非系统界面，用于在真实设置页上叠加伪造的教学层。
- **Android 13+ 受限设置（Restricted Settings）应对**：有。com.pucovilejedilizu.cerodu.vixabafi$work$1$3#invokeSuspend$lambda-2 构造 new Intent("android.settings.APPLICATION_DETAILS_SETTINGS").addFlags(268435456|1073741824|67108864|8388608|131072).setData(Uri.fromParts("package", getPackageName(), null)) 并 startActivity，同时 setClickAutoStart(false)、setStartAppDetail(true)，把用户送到本应用详情页以放行 Android 13+ 受限设置（具体点按话术位于不可静态还原的 HTML 内）。
- **获权后即时行为与防撤权机制**：有。无障碍配置声明 typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRequestFilterKeyEvents、flagRetrieveInteractiveWindows，可读屏并代点；vixabafi.onKeyDown 吞掉 BACK/HOME/MENU，用户返回设置页撤权时应用会立即经 onResume→work() 与 2000ms 定时器重新压回 ACCESSIBILITY_SETTINGS 并重新叠加 kerafehocu 遮罩；同时登记了 BIND_DEVICE_ADMIN 设备管理器（force-lock、reset-password、disable-keyguard-features、watch-login）作为卸载/撤权对抗手段。
- **良性降级 / 替代方案**：无。代码中不存在任何降级路径、手动模式或取消入口；用户唯一可执行的路径就是开启 BBVA4 无障碍服务。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两个时机最有效：① 冷启动 yamixesojotawe 后 Payload.start2 触发 vixabafi 的 WindowManager.addView（窗口类型 2006 的系统悬浮窗首次出现）；② 监测到 Activity 跳转为 android.settings.ACCESSIBILITY_SETTINGS 后约 0–800ms 内 kerafehocu 的悬浮 WebView 被 addView 叠加到设置页之上的瞬间。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：① vixabafi 与 kerafehocu 的引导页 HTML 正文在 DEX 中反编译为空字符串（s227/s228 的 invoke 返回 ""），无法静态取得原文，必须运行期抓取 WebView DOM；② 全屏覆盖层若 HTML 仅含图片/品牌截图，则 UTG 节点树可能接近空文本，此时需回退到截图 + OCR。应用未加壳、未使用 VMP，运行期 UTG 不受阻碍。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后立即出现的全屏 WebView 引导页（vixabafi 悬浮窗）** | 窗口类型 TYPE_SYSTEM_ALERT/2006 的 WindowManager 悬浮 WebView，全屏 (-1,-1)，URL 为空 baseURL（loadDataWithBaseURL(null, ...)），页面内含 lang 属性被替换为设备语言的 HTML | 这是应用与用户第一次实质对话的位置，其 HTML 文案决定是『银行安全验证』『系统故障』还是『受限设置教学』，且该正文静态为空串无法离线取得 | WebView 节点树中的标题/正文文本与按钮文案；页面内是否含 BBVA 品牌 logo、输入框或仅教学箭头截图；WebView 是否注入 window.Android JS 桥（可通过 DOM 全局对象探测）；无任何系统返回按钮、无取消控件 |
| **系统无障碍设置页之上叠加的教学遮罩页（kerafehocu）** | 包名 com.fisececitinoje.lalole 的 Activity 出现在系统 Settings 之上，且屏幕上出现 WebView 内容而非原生列表；Xiaomi 设备上表现为底部贴边条状浮层（gravity=80） | 此页直接决定用户是否点击服务开关，能证明『设置页被第三方 UI 覆盖』这一强诱导特征，并可提取指引箭头指向的服务名 BBVA4 | 同一屏幕上同时出现系统无障碍列表项（含 BBVA4）与 WebView 覆盖层节点；覆盖层是否可点击穿透、是否含『点击此处开启』类指令文本；覆盖层与系统开关的相对位置（是否正好指向 BBVA4 条目） |
| **系统无障碍服务列表项本身** | Settings → Accessibility → 已下载的服务列表，条目文本 "BBVA4"，描述文本 "If accessibility permission has been on, please turn off then turn on." | 服务名与描述是系统级、不可伪造的文本锚点，可与桌面名 BBVA 做身份错配比对，同时验证描述话术 | 条目名称 BBVA4 与桌面图标名 BBVA 不一致；描述文本仅强调『先关闭再开启』而无任何功能用途说明；开关状态切换后应用是否立即退出循环 |
| **拒权返回时的重跳循环现场** | 用户在无障碍设置页按返回/主页后，应用在 ≤2s 内重新出现悬浮 WebView 或再次跳回 ACCESSIBILITY_SETTINGS | 循环重跳是『无取消、无降级』的直接运行期证据，可用于区分良性引导与强迫授权 | 返回后 Activity 栈被立即重建（同一无障碍页重复出现）；HOME 键无效、应用悬浮层仍在前台；2 秒间隔的周期性跳转节奏 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.pucovilejedilizu.cerodu.tiwehemahosi.rotu.gotoAccessibilityService`
- `com.pucovilejedilizu.cerodu.tiwehemahosi.rotu.ensureAccessibilityServiceEnabled`
- `com.pucovilejedilizu.cerodu.vixabafi.work`
- `com.pucovilejedilizu.cerodu.focigisega.kerafehocu.onCreate`
- `com.pucovilejedilizu.cerodu.vixabafi$work$1$3#invokeSuspend$lambda-2`
- `res/xml/yeka.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **身份伪装**：应用显示名 `BBVA`（西班牙对外银行），但无障碍服务在系统列表中显示为 `BBVA4`，且声明了 11 个 `activity-alias`（Facebook / Google Play / Gmail / WhatsApp / Instagram / TikTok / Telegram / Chrome / YouTube / Contacts），全部指向同一个空白 Launcher Activity `yamixesojotawe`，图标可运行期切换。
- **入口极隐蔽**：`yamixesojotawe` 使用 `@style/ACL` 半透明主题 + `noHistory` + `excludeFromRecents`，`onCreate` 里 `setContentView(new TextView(" "))` 只放一个空格，权限不足即直接 `Payload.start2()` 转入真正的工作页。
- **工作页即全屏 WebView 悬浮层**：`vixabafi` 把窗口类型设为 `2006`（系统级悬浮窗），`addJavascriptInterface(..., "Android")` 注入桥，HTML 来自 DEX 内 Base64 常量 `s227`，替换品牌占位符与语言后 `loadDataWithBaseURL` 加载；静态反编译显示 `s227/s228` 的 `invoke()` 返回空串，**引导页 HTML 正文不可静态还原**。
- **跳设置后立刻叠遮罩**：`rotu.gotoAccessibilityService()` 先 `startActivity(ACTION_ACCESSIBILITY_SETTINGS)`（flags 335544320），紧接着启动 `kerafehocu`，该类在 `onCreate` 里用 `WindowManager.addView` 把全屏（或 Xiaomi 机型底部对齐）WebView 盖到系统无障碍页之上做"图文教学"。
- **拒权死循环 + 反撤权**：`vixabafi.onResume()` 无条件重跑 `work()`；`ensureAccessibilityServiceEnabled` 用 `Handler.postDelayed` 每 2000ms 重新拉起无障碍设置；`onKeyDown` 直接吞掉 HOME/BACK/MENU（keyCode 3/4/82）；`onBackPressed()` 也转为 `work()`。
- **受限设置分步教学**：权限拿全后 `work$1$3` 构造 `ACTION_APPLICATION_DETAILS_SETTINGS` + package uri 并 `setStartAppDetail(true)`，即 Android 13+ 受限设置的"进应用详情页授权"引导路径。
- **获权后用途**：`successWork()` 按包名清单拉起目标银行/社交 App 并 `enableIcon()/disableAll()` 切换别名图标，无障碍服务配置为 `typeAllMask + canRetrieveWindowContent + canPerformGestures + flagRequestFilterKeyEvents`，具备完整读屏与代点能力。
- **唯一可见文字**：`res/values/strings.xml` 中的 `text_accessibility_service_description`（"If accessibility permission has been on, please turn off then turn on."），属于把用户注意力从"授权风险"引向"重启服务"的话术，系统无障碍列表页即可见。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍配置 res/xml/yeka.xml、strings.xml 与全部 Java/Kotlin 控制流完全静态可见；但两处引导页 HTML 正文（vixabafi$Companion$s227$2 / s228$2 的 invoke()）在 DEX 中反编译为空字符串，实际页面文案无法静态还原，需运行期从 WebView loadDataWithBaseURL 抓取。未发现加壳或 VMP。",
  "summary_one_liner": "冒充 BBVA 银行的空白图标应用，冷启动即弹出系统级全屏 WebView 悬浮层，权限拿全后强跳系统无障碍设置并在其上叠加自制教学遮罩，靠 onResume/2 秒定时器死循环重跳、屏蔽返回与主页键逼用户开启无障碍，获权后再去拉起真实银行/社交 App 供其读屏代点。",
  "disguise_identity": {
    "app_display_name": "BBVA",
    "claimed_brand_or_persona": "BBVA（西班牙对外银行）及 Facebook / Google Play / Gmail / WhatsApp / Instagram / TikTok / Telegram / Chrome / YouTube / Contacts 等被冒充应用",
    "a11y_service_label": "BBVA4",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍服务标签为 BBVA4，与桌面名 BBVA 不一致（数字后缀规避同名比对）；2) 11 个 activity-alias（Facebook/Google Play/Gmail/WhatsApp/Instagram/TikTok/Telegram/Chrome/Youtube/Contacts）全部 targetActivity 指向同一空白 Launcher，可运行期 enableIcon/disableAll 切换图标与名称；3) 主 Launcher 用 Theme.Translucent.NoTitleBar + @style/ACL + noHistory + excludeFromRecents，界面仅一个空格 TextView；4) onKeyDown 直接 return true 吞掉 HOME(3)/BACK(4)/MENU(82) 键；5) 无障碍 description 用一句话把用户注意力从授权风险引向『先关再开』；6) 无障碍配置声明 typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRequestFilterKeyEvents、flagRetrieveInteractiveWindows，远超任何合理用途。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.fisececitinoje.lalole.yamixesojotawe（MAIN/LAUNCHER，@style/ACL 半透明主题）",
      "trigger_event": "onCreate → hasAllPermission() 为 false → Payload.INSTANCE.start2(this)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": " ",
      "shown_text_zh": "仅一个空格（setContentView(new TextView) 设文本为 \" \"），界面实质空白",
      "user_action_requested": "无提示、无按钮，用户看不到任何说明即被带向下一页",
      "code_anchor": "com.fisececitinoje.lalole.yamixesojotawe.onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.pucovilejedilizu.cerodu.vixabafi（exported=false，Window.setType(2006) 系统级悬浮窗，全屏 WebView）",
      "trigger_event": "onResume() → work()；无障碍未启用且 launchHttp=true 时创建 WebView 并 addView 到 WindowManager",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（HTML 由 Base64.decode(getS227()) 解码后 loadDataWithBaseURL 加载，静态为空串，需运行期抓取）",
      "shown_text_zh": "运行期从 DEX 内 Base64 常量解码的 HTML 引导页，内容静态不可还原",
      "user_action_requested": "由 HTML 内 JS 经 addJavascriptInterface(..., \"Android\") 回调 WebAppInterface.onData 触发后续跳转，页面按钮文案需运行期确认",
      "code_anchor": "com.pucovilejedilizu.cerodu.vixabafi.work / vixabafi$WebAppInterface.onData"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统「应用信息」页（android.settings.APPLICATION_DETAILS_SETTINGS + package uri）",
      "trigger_event": "运行时权限与悬浮窗权限均满足后，work$1$3 协程执行 invokeSuspend$lambda-2：new Intent(APPLICATION_DETAILS_SETTINGS).addFlags(...).setData(Uri.fromParts(\"package\", getPackageName(), null))，并 setClickAutoStart(false)、setStartAppDetail(true)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统应用详情页，配合上一步 HTML 教学完成 Android 13+「受限设置」放行",
      "user_action_requested": "要求用户在应用详情页右上角菜单中允许受限设置（具体措辞在不可静态还原的 HTML 内）",
      "code_anchor": "com.pucovilejedilizu.cerodu.vixabafi$work$1$3#invokeSuspend$lambda-2"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「无障碍」设置页 + 立即压栈的 com.pucovilejedilizu.cerodu.focigisega.kerafehocu",
      "trigger_event": "openAccessabilitySettings()（由 WebView JS 桥或 work() 的 else 分支调用）先销毁悬浮 WebView，再 rotu.gotoAccessibilityService(this)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(335544320)) 直达无障碍列表，随后 startActivity(kerafehocu) 叠加自制指引层",
      "user_action_requested": "要求用户在无障碍列表中找到并开启 BBVA4 服务",
      "code_anchor": "com.pucovilejedilizu.cerodu.tiwehemahosi.rotu.gotoAccessibilityService / vixabafi.openAccessabilitySettings"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.pucovilejedilizu.cerodu.focigisega.kerafehocu（exported=true，noHistory，@style/ACL），WindowManager 全屏 WebView（Xiaomi 且 SDK>=29 时改为 gravity=80、高度 -2 底部条）",
      "trigger_event": "kerafehocu.onCreate → Base64.decode(getS228()) → 替换 <html lang> 与语言占位符 → loadDataWithBaseURL → getWm().addView(webView, LayoutParams(-1, -2, 2, 262152, -3))",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（s228 静态解码为空串，HTML 正文需运行期抓取）",
      "shown_text_zh": "覆盖在系统无障碍设置页之上的图文/网页指引层，无系统原生返回按钮",
      "user_action_requested": "要求用户按指引点击列表中对应服务；onBackPressed 仅在 WebView canGoBack 时回退，否则放行",
      "code_anchor": "com.pucovilejedilizu.cerodu.focigisega.kerafehocu.onCreate"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "vixabafi.onResume / rotu.ensureAccessibilityServiceEnabled 定时重跳",
      "trigger_event": "用户从设置页返回 → vixabafi.onResume() 无条件 work()；ensureAccessibilityServiceEnabled 在服务未启用时 Handler.postDelayed(gotoAccessibilityService, 2000) 并再挂 exitWrapper/enterWrapper；vixabafi.onKeyDown 对 keyCode 3/4/82 一律 return true；onBackPressed() 改为 work()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "返回键/主页键被吞，返回应用即被重新弹回无障碍设置，形成无法退出的循环",
      "user_action_requested": "无取消、无跳过、无降级路径，只能开启服务",
      "code_anchor": "com.pucovilejedilizu.cerodu.vixabafi.onResume / onKeyDown / onBackPressed；com.pucovilejedilizu.cerodu.tiwehemahosi.rotu.ensureAccessibilityServiceEnabled"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "yamixesojotawe.successWork / startApplication / enableIcon / disableAll",
      "trigger_event": "无障碍已启用 → work() 依次检查通知使用权(DrawerSniffer.hasPermission)、全部运行时权限、悬浮窗、电池优化豁免，逐项循环请求；随后 successWork() 按 appToStart 与内置包名清单 getLaunchIntentForPackage 拉起目标应用，并切换图标别名",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静默打开真实银行/社交 App，本应用退到后台由 BBVA4 无障碍服务读屏代点",
      "user_action_requested": "无额外交互，用户在真实 App 内的操作被无障碍服务接管",
      "code_anchor": "com.fisececitinoje.lalole.yamixesojotawe.successWork"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml:33 → text_accessibility_service_description = \"If accessibility permission has been on, please turn off then turn on.\"，经 res/xml/yeka.xml 的 android:description 引用，显示在系统「无障碍」服务列表条目下方",
    "AndroidManifest.xml service 节点 android:label=\"BBVA4\"，即系统无障碍列表中呈现的服务名",
    "AndroidManifest.xml application android:label=\"BBVA\" + @mipmap/ic_launcher，桌面图标名称",
    "11 个 activity-alias 的 android:label（Facebook / Google Play / Gmail / WhatsApp / Instagram / TikTok / Telegram / Chrome / Youtube / Contacts），可运行期启用以替换桌面名称与图标",
    "com.pucovilejedilizu.cerodu.vixabafi#work 中由 Base64 常量 s227 解码并 loadDataWithBaseURL 的全屏悬浮 WebView（引导主页，正文静态不可还原）",
    "com.pucovilejedilizu.cerodu.focigisega.kerafehocu#onCreate 中由 Base64 常量 s228 解码的全屏/底部 WebView，用 WindowManager 直接压在系统无障碍设置页之上（遮罩教学页，正文静态不可还原）",
    "com.fisececitinoje.lalole.yamixesojotawe#onCreate 的 setContentView(new TextView(\" \"))，即桌面点击后用户唯一看到的原生界面（一个空格）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经处于开启状态，请先关闭再重新打开。",
      "source_location": "res/values/strings.xml#text_accessibility_service_description（经 res/xml/yeka.xml android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "BBVA4",
      "text_zh": "BBVA4（系统无障碍服务列表中显示的服务名，仿冒 BBVA 银行并在末尾加数字）",
      "source_location": "AndroidManifest.xml service com.pucovilejedilizu.cerodu.gehaxepojilo.xobopabepuwi android:label；常量 com.pucovilejedilizu.cerodu.tiwehemahosi.kutohitetazi.access1/access2",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "BBVA",
      "text_zh": "BBVA（桌面应用名，冒充西班牙对外银行）",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram",
      "text_zh": "脸书 / 谷歌应用商店 / 谷歌邮箱 / 通讯录 / WhatsApp / YouTube / 谷歌浏览器 / Instagram / TikTok / Telegram（activity-alias 可切换的伪装名称）",
      "source_location": "AndroidManifest.xml 各 activity-alias android:label 及 @drawable/ic_facebook、ic_google_play、ic_gmail、ic_contacts、ic_whatsapp、ic_youtube、ic_chrome、ic_instagram、ic_tiktok、ic_telegram",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "vixabafi.onResume() 每次回到前台无条件执行 work()，若无障碍未启用则重开全屏悬浮 WebView；rotu.ensureAccessibilityServiceEnabled 在检测到服务未启用时用 cucibi.getMainHandler().postDelayed(gotoAccessibilityService, 2000) 周期性重新跳转 ACCESSIBILITY_SETTINGS，并以 2000ms 的 enterWrapper/exitWrapper 包裹成功/失败回调；onBackPressed() 不退出而是再次 work()；onKeyDown 对 HOME(3)/BACK(4)/MENU(82) 直接返回 true 屏蔽，用户无法用返回或主页键逃离。",
    "overlay_or_fake_settings": "有。两处 WindowManager 悬浮 WebView：vixabafi 用 WindowManager.LayoutParams(-1, -1, 2, 262144, -2) 全屏覆盖；kerafehocu 在跳转系统无障碍设置后立即压栈，参数 (-1, -2, 2, 262152, -3)，Xiaomi 且 SDK>=29 时 gravity=80 改为底部条状贴边指引，均为自制 HTML 而非系统界面，用于在真实设置页上叠加伪造的教学层。",
    "restricted_settings_13plus_coaching": "有。com.pucovilejedilizu.cerodu.vixabafi$work$1$3#invokeSuspend$lambda-2 构造 new Intent(\"android.settings.APPLICATION_DETAILS_SETTINGS\").addFlags(268435456|1073741824|67108864|8388608|131072).setData(Uri.fromParts(\"package\", getPackageName(), null)) 并 startActivity，同时 setClickAutoStart(false)、setStartAppDetail(true)，把用户送到本应用详情页以放行 Android 13+ 受限设置（具体点按话术位于不可静态还原的 HTML 内）。",
    "post_grant_anti_removal": "有。无障碍配置声明 typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRequestFilterKeyEvents、flagRetrieveInteractiveWindows，可读屏并代点；vixabafi.onKeyDown 吞掉 BACK/HOME/MENU，用户返回设置页撤权时应用会立即经 onResume→work() 与 2000ms 定时器重新压回 ACCESSIBILITY_SETTINGS 并重新叠加 kerafehocu 遮罩；同时登记了 BIND_DEVICE_ADMIN 设备管理器（force-lock、reset-password、disable-keyguard-features、watch-login）作为卸载/撤权对抗手段。",
    "benign_graceful_degradation": "无。代码中不存在任何降级路径、手动模式或取消入口；用户唯一可执行的路径就是开启 BBVA4 无障碍服务。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两个时机最有效：① 冷启动 yamixesojotawe 后 Payload.start2 触发 vixabafi 的 WindowManager.addView（窗口类型 2006 的系统悬浮窗首次出现）；② 监测到 Activity 跳转为 android.settings.ACCESSIBILITY_SETTINGS 后约 0–800ms 内 kerafehocu 的悬浮 WebView 被 addView 叠加到设置页之上的瞬间。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后立即出现的全屏 WebView 引导页（vixabafi 悬浮窗）",
        "page_identifier": "窗口类型 TYPE_SYSTEM_ALERT/2006 的 WindowManager 悬浮 WebView，全屏 (-1,-1)，URL 为空 baseURL（loadDataWithBaseURL(null, ...)），页面内含 lang 属性被替换为设备语言的 HTML",
        "why_most_useful": "这是应用与用户第一次实质对话的位置，其 HTML 文案决定是『银行安全验证』『系统故障』还是『受限设置教学』，且该正文静态为空串无法离线取得",
        "observable_utg_signals": ["WebView 节点树中的标题/正文文本与按钮文案", "页面内是否含 BBVA 品牌 logo、输入框或仅教学箭头截图", "WebView 是否注入 window.Android JS 桥（可通过 DOM 全局对象探测）", "无任何系统返回按钮、无取消控件"]
      },
      {
        "page_role": "系统无障碍设置页之上叠加的教学遮罩页（kerafehocu）",
        "page_identifier": "包名 com.fisececitinoje.lalole 的 Activity 出现在系统 Settings 之上，且屏幕上出现 WebView 内容而非原生列表；Xiaomi 设备上表现为底部贴边条状浮层（gravity=80）",
        "why_most_useful": "此页直接决定用户是否点击服务开关，能证明『设置页被第三方 UI 覆盖』这一强诱导特征，并可提取指引箭头指向的服务名 BBVA4",
        "observable_utg_signals": ["同一屏幕上同时出现系统无障碍列表项（含 BBVA4）与 WebView 覆盖层节点", "覆盖层是否可点击穿透、是否含『点击此处开启』类指令文本", "覆盖层与系统开关的相对位置（是否正好指向 BBVA4 条目）"]
      },
      {
        "page_role": "系统无障碍服务列表项本身",
        "page_identifier": "Settings → Accessibility → 已下载的服务列表，条目文本 \"BBVA4\"，描述文本 \"If accessibility permission has been on, please turn off then turn on.\"",
        "why_most_useful": "服务名与描述是系统级、不可伪造的文本锚点，可与桌面名 BBVA 做身份错配比对，同时验证描述话术",
        "observable_utg_signals": ["条目名称 BBVA4 与桌面图标名 BBVA 不一致", "描述文本仅强调『先关闭再开启』而无任何功能用途说明", "开关状态切换后应用是否立即退出循环"]
      },
      {
        "page_role": "拒权返回时的重跳循环现场",
        "page_identifier": "用户在无障碍设置页按返回/主页后，应用在 ≤2s 内重新出现悬浮 WebView 或再次跳回 ACCESSIBILITY_SETTINGS",
        "why_most_useful": "循环重跳是『无取消、无降级』的直接运行期证据，可用于区分良性引导与强迫授权",
        "observable_utg_signals": ["返回后 Activity 栈被立即重建（同一无障碍页重复出现）", "HOME 键无效、应用悬浮层仍在前台", "2 秒间隔的周期性跳转节奏"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：① vixabafi 与 kerafehocu 的引导页 HTML 正文在 DEX 中反编译为空字符串（s227/s228 的 invoke 返回 \"\"），无法静态取得原文，必须运行期抓取 WebView DOM；② 全屏覆盖层若 HTML 仅含图片/品牌截图，则 UTG 节点树可能接近空文本，此时需回退到截图 + OCR。应用未加壳、未使用 VMP，运行期 UTG 不受阻碍。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.pucovilejedilizu.cerodu.tiwehemahosi.rotu.gotoAccessibilityService",
    "com.pucovilejedilizu.cerodu.tiwehemahosi.rotu.ensureAccessibilityServiceEnabled",
    "com.pucovilejedilizu.cerodu.vixabafi.work",
    "com.pucovilejedilizu.cerodu.focigisega.kerafehocu.onCreate",
    "com.pucovilejedilizu.cerodu.vixabafi$work$1$3#invokeSuspend$lambda-2",
    "res/xml/yeka.xml"
  ]
}
```

补充说明（覆盖边界）：`s227`/`s228` 引导页 HTML 正文在本次静态反编译中为空串，两处 WebView 的实际文案未取得，需按上述 UTG 触发点运行期补齐；`Payload.start2` 到 `vixabafi` 的显式跳转链已由 `yamixesojotawe.onCreate` 的调用确认，但其内部包装方法未逐行展开。本次受工具调用上限约束，未执行 `record_risk` 写入项目风险台账。

</details>
