# MB_090__aea84ebd9c｜Hook — Grab

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：181.7s

## 1. 一句话核心结论

- **核心申请方式**：应用以无界面的 2006 悬浮窗 Activity 加载内嵌 Base64 伪造的『系统无障碍服务列表页』（含 DOWNLOADED SERVICES/Switch Access/TalkBack/OFF 与 Start Accessibility 按钮），点击后跳系统无障碍设置并在其上再叠一层底部高仿浮层，全程无跳过按钮且返回键/onResume 反复重跳，直到开启 GrabAssistService。
- **静态可见性说明**：引导链路全部静态可见：无障碍服务类、PermissionsActivity 的 2006 悬浮窗 WebView、两份 Base64 内嵌 HTML 引导页（已解码为 23KB 仿系统无障碍列表）、ACTION_ACCESSIBILITY_SETTINGS 跳转点、DialogActivityasd 设置页叠层浮窗、onResume/onBackPressed 重跳逻辑均可完整还原；未发现加壳、V2 加密载荷或远端 HTML 下发，HTML 语言表与文案硬编码在 DEX 常量中。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `aea84ebd9c1194efa69033231fe055a9fa79f3e740825965ab2767c4f61b0531` |
| 包名 / 年份 | `com.tencent.mm` / 2024 |
| 家族 / 品类 | **Hook**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Grab |
| 引导页宣称品牌/身份 | 包名冒用 com.tencent.mm（微信），图标别名伪装 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram；引导页冒充 Android 系统『无障碍服务』设置界面 |
| 系统无障碍列表服务名 | GrabAssistService |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 包名与类前缀冒用 com.tencent.mm；2) 10 个 activity-alias 以主流社交/商店图标与标签伪装桌面入口，targetActivity 均指向 Main2；3) 主入口内容视图为 TextView(" ") 单空格，界面空白；4) 引导页 HTML 以 Base64 字符串内嵌，占位符 %Enable_Accessibility_Service% 与 <html lang="en"> 运行期按语言替换；5) 无障碍服务 description 用『请先关闭再开启』话术淡化真实权限范围；6) 设备管理员 receiver label 为空字符串、description 为 Add application to admin |
| 无障碍服务类名 | `com.xxx.zzz.accessppp.AccessibilityServiceQ` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | If accessibility permission has been on, please turn off then turn on. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tencent.mm.Main2（桌面 LAUNCHER，主题 @style/ACL，noHistory） | 用户点击桌面图标，Main2.onCreate | 原生Activity | **原文**：TextView 内容为 " "（单个空格，无任何界面文字）<br>**译注**：纯空白页面，用户看不到任何业务功能 | 无显式交互，页面立即 finish 并跳转下一环节 | `com.tencent.mm.Main2.onCreate` |
| 2 | 冷启动入口 | com.xxx.zzz.Payload.start2 → com.xxx.zzz.MainActivity.start → com.xxx.zzz.PermissionsActivity | Main2.onCreate 中 PermissionsActivity.Companion.hasAllPermission() 返回 false 时调用 Payload.INSTANCE.start2() | 原生Activity | 无 | 无，用户无选择权 | `com.xxx.zzz.Payload#start2 / com.xxx.zzz.MainActivity#start` |
| 3 | 引导说明页 | com.xxx.zzz.PermissionsActivity（setType(2006) 系统悬浮窗层，无布局，仅承载 WindowManager 全屏 WebView） | PermissionsActivity.onCreate → onResume → work() | 本地HTML WebView | **原文**：%Enable_Accessibility_Service% / Start Accessibility / >><br>**译注**：『启用无障碍服务』标题 + 『启动无障碍』按钮 + 向右箭头，页面其余为仿系统无障碍列表项 | 点击 Start Accessibility 按钮（页面无取消、跳过或返回入口） | `com.xxx.zzz.PermissionsActivity#work / PermissionsActivity$Companion#getS227` |
| 4 | 遮罩叠层指引 | PermissionsActivity 内全屏 WebView（WindowManager.LayoutParams(-1,-1,2,262144,-2)，注册 JavascriptInterface "Android"） | work() 中 this.launchHttp 为 true 时解码 Base64 并 loadDataWithBaseURL(null, html, "text/html", "UTF-8", null) | 悬浮窗Overlay | **原文**：Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF<br>**译注**：逐字复刻系统无障碍设置页：『无障碍服务』『已下载的服务』『切换访问』『TalkBack』『关闭』等系统同款字段与开关态 | 按仿系统列表样式引导用户『打开』服务，实为触发 JS 桥 onData() | `com.xxx.zzz.PermissionsActivity$WebAppInterface#onData` |
| 5 | 跳无障碍设置 | 系统页 android.settings.ACCESSIBILITY_SETTINGS（Intent FLAG_ACTIVITY_CLEAR_TOP\|NEW_TASK） | WebAppInterface.onData() → openAccessabilitySettings() 销毁遮罩 → UtilsGfgsd.gotoAccessibilityService() | 系统无障碍页 | **原文**：无（应用侧不呈现文字，直接拉起系统页）<br>**译注**：跳转到系统无障碍服务列表，由用户手动找到 GrabAssistService 并开启 | 在系统列表中手动开启 GrabAssistService（服务名与桌面名 Grab 不一致，易误认） | `com.xxx.zzz.globp.UtilsGfgsd#gotoAccessibilityService` |
| 6 | 遮罩叠层指引 | com.xxx.zzz.notifp.DialogActivityasd（windowIsFloating 2006，gravity=80 底部对齐，LayoutParams(-1,-2,...,262152,-3)） | gotoAccessibilityService() 中 PermissionsActivity.Companion.getS228().length() > 0 时，在拉起系统设置后立即 startActivity(DialogActivityasd)；ensureAccessibilityServiceEnabled 内 postDelayed(2000) 跳设置、postDelayed(3000) 执行后续包装 | 悬浮窗Overlay | **原文**：第二份 Base64 HTML（与首份同为仿系统无障碍列表模板，含 Start Accessibility 与 DOWNLOADED SERVICES / Switch Access / TalkBack / OFF）<br>**译注**：在系统无障碍设置页之上叠加底部高仿系统列表浮层，指向应点击的服务项位置 | 照浮层指引点击系统列表中的服务并确认开启 | `com.xxx.zzz.notifp.DialogActivityasd#onCreate` |
| 7 | 拒权反馈循环 | PermissionsActivity.onResume / onBackPressed（从系统设置返回时） | 用户从系统设置返回或按返回键：onResume 无条件调用 work()；onBackPressed 直接调用 work() | 本地HTML WebView | **原文**：%Enable_Accessibility_Service% / Start Accessibility<br>**译注**：重新显示同一仿系统引导页，要求再次开启，用户无法退出或跳过 | 反复要求开启无障碍；无取消、无跳过、无降级路径 | `com.xxx.zzz.PermissionsActivity#onBackPressed / #onResume` |
| 8 | 获权后动作 | 系统无障碍服务列表项 GrabAssistService（com.xxx.zzz.accessppp.AccessibilityServiceQ，配置 @xml/serviceconfig） | 服务被开启后 PermissionsActivity.Companion.hasAllPermission() 转为 true，Main2.onCreate 走 successWork()/saveCurAppName() 分支 | 系统无障碍页 | **原文**：If accessibility permission has been on, please turn off then turn on.<br>**译注**：『如果无障碍权限已经开启，请关闭后再重新开启一次』——以重启话术替代真实用途说明 | 按提示反复关闭再开启服务（实际授予 typeAllMask / canRetrieveWindowContent / canPerformGestures / flagRetrieveInteractiveWindows 全量能力） | `res/xml/serviceconfig.xml / res/values/strings.xml#text_accessibility_service_description` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- PermissionsActivity 通过 WindowManager 添加的全屏 WebView（悬浮窗类型 2006）：内嵌 Base64 HTML 首屏，标题 %Enable_Accessibility_Service%，按钮 Start Accessibility，仿系统列表项 Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF
- DialogActivityasd 通过 WindowManager 添加的底部浮层 WebView（gravity=80，windowIsFloating）：第二份 Base64 HTML，叠在系统无障碍设置页之上继续指引
- 系统无障碍列表项描述：res/values/strings.xml 中 text_accessibility_service_description = If accessibility permission has been on, please turn off then turn on.
- 设备管理员声明描述：strings.xml 中 adm = Add application to admin，AdminReceiverzxc 的 android:label 为空字符串
- 桌面图标与标签：AndroidManifest 中 application label Grab 与 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 十个 activity-alias
- 主入口界面：Main2 与 MainActivity 均 setContentView(new TextView(this)) 且 setText(" ")，无任何说明文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | %Enable_Accessibility_Service% | %启用无障碍服务%（占位符，运行期按系统语言替换为对应文案） | `classes.dex 内嵌 Base64 HTML（PermissionsActivity$Companion#getS227 解码），由 constNm.ключ_от_всего 占位符替换` | 假反诈安全 |
| en | Start Accessibility | 启动无障碍 | `classes.dex 内嵌 Base64 HTML 主按钮（点击经 JavascriptInterface "Android".onData 跳转）` | 受限设置分步教学 |
| en | Accessibility Service | 无障碍服务 | `内嵌 HTML 语言表 objLang.en.accessability1，仿系统无障碍设置页标题` | 假反诈安全 |
| en | DOWNLOADED SERVICES | 已下载的服务 | `内嵌 HTML 语言表 objLang.en.downloadedservice，仿系统无障碍列表分组标题` | 假反诈安全 |
| en | Switch Access | 切换访问 | `内嵌 HTML 语言表 objLang.en.switchaccess，用作列表项名` | 假反诈安全 |
| en | TalkBack | TalkBack（系统读屏服务） | `内嵌 HTML 语言表 objLang.en.talkback，用作列表项名` | 假反诈安全 |
| en | OFF | 关闭（开关状态文字） | `内嵌 HTML 语言表 objLang.en.off，用于仿造系统开关态` | 假反诈安全 |
| zh | 無障礙服務 / 下載的服務 / 開關訪問 / 頂嘴 / 關 | 繁体中文版系统无障碍设置页同款字段（TalkBack 被误译为『頂嘴』） | `内嵌 HTML 语言表 objLang.zh（按 Locale 动态替换 <html lang>）` | 假反诈安全 |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开启，请关闭后再重新开启一次。 | `res/values/strings.xml#text_accessibility_service_description（serviceconfig.xml 的 android:description）` | 教唆忽视警告 |
| en | Add application to admin | 将应用添加到设备管理员 | `res/values/strings.xml#adm（AdminReceiverzxc 的 android:description，label 为空字符串）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：PermissionsActivity.onResume 无条件调用 work()，onBackPressed 也直接调用 work()；用户从系统无障碍设置返回或按返回键即重新渲染仿系统引导页并再次要求开启，同时 ensureAccessibilityServiceEnabled 以 postDelayed(2000) 重跳设置、postDelayed(3000) 叠加底部引导浮层，形成循环直到 hasAllPermission()（无障碍+悬浮窗+全部危险权限+doze 白名单）为真
- **遮罩叠层 / 高仿系统设置页**：两者兼有：PermissionsActivity 本身即以 Window.setType(2006) 悬浮窗层承载全屏 WebView，页面内容为高仿系统无障碍设置页（Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF 及开关态）；跳系统设置后 DialogActivityasd 再以 windowIsFloating(2006) 底部对齐浮层叠在系统页之上继续指引
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=28，未使用应用详情右上角『允许受限设置』或 Session 安装器话术，直接跳 android.settings.ACCESSIBILITY_SETTINGS）
- **获权后即时行为与防撤权机制**：有：无障碍服务配置声明 typeAllMask、flagRetrieveInteractiveWindows、canPerformGestures 与 flagRequestFilterKeyEvents，且 DEX 线索含 PERFORM_GLOBAL_ACTION / WATCH_SETTINGS，可监听设置页并用全局返回/主页动作阻止撤权（本次未逐方法展开该分支，属未完全展开部分）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 com.xxx.zzz.PermissionsActivity 或 com.xxx.zzz.notifp.DialogActivityasd 成为前台窗口（二者均为 2006 悬浮窗层 WebView，无正常 Activity 布局），以及 Intent 发出 android.settings.ACCESSIBILITY_SETTINGS 的瞬间；亦可在冷启动 Main2 后 1 秒内截图（Payload.start 使用 postDelayed 1000ms）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导 HTML 为 DEX 内 Base64 字符串并在运行期做占位符与 lang 替换，若仅在包内检索 assets/*.html 或明文关键词会漏检；须在运行期捕获 PermissionsActivity / DialogActivityasd 的 WebView 窗口。另入口界面为 TextView(" ") 单空格空白页，冷启动首次截图可能只捕获空白窗口，需在 1 秒后（Payload.start 的 postDelayed 1000ms）再抓取。无障碍撤权对抗（GLOBAL_ACTION_BACK/HOME、WATCH_SETTINGS）本次未逐方法展开，属未完全核验分支。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动伪造系统无障碍设置页（首层引导）** | 全屏 WebView，标题 %Enable_Accessibility_Service%，按钮 Start Accessibility，列表含 DOWNLOADED SERVICES / Switch Access / TalkBack / OFF | 该页是判定『伪造系统设置页』的核心证据：字段与系统无障碍页逐字一致，但由应用自身 WebView 渲染，且无跳过入口 | 页面文案含 DOWNLOADED SERVICES / Switch Access / TalkBack 但控件非系统组件；存在 Start Accessibility 主按钮且无取消/跳过元素；同一页面在不同系统语言下切换 lang 属性（动态替换 <html lang>） |
| **跳转系统设置后 2000ms 压栈的底部引导浮层** | 系统无障碍设置页之上、屏幕底部对齐的半屏 WebView（DialogActivityasd，windowIsFloating 2006） | 叠层直接覆盖系统设置页并指向应点击项，是『设置页叠层指引』的直接运行证据，也是区分合法引导与诱导的关键 | 系统设置页上方出现应用包名的悬浮窗节点（非系统 UI）；底部浮层含与首层相同的仿系统列表文案；浮层出现时间与跳转系统设置相隔约 2 秒 |
| **系统无障碍服务列表项** | 设置→无障碍→已下载的服务中的 GrabAssistService 条目（description: If accessibility permission has been on, please turn off then turn on.） | 确认用户实际被要求开启的是应用自有服务，且描述话术与真实能力（读取窗口内容/模拟手势）不符，并可与桌面名 Grab 形成身份不一致对照 | 服务标签 GrabAssistService 与桌面应用名 Grab 不一致；description 仅提示『关闭再开启』而未说明实际能力；开启后应用立即进入 successWork 分支并隐藏入口 |
| **拒权后重跳页面** | 从系统设置返回后重新出现的 PermissionsActivity 全屏 WebView | 证明无跳过且存在拒绝循环，是强制引导定性的运行期证据 | 返回系统设置后 1 秒内同一引导页再次出现；多次返回后页面文案与结构不变且始终无取消按钮；按返回键不退出应用而重新加载引导页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.xxx.zzz.PermissionsActivity#work`
- `com.xxx.zzz.PermissionsActivity#openAccessabilitySettings`
- `com.xxx.zzz.PermissionsActivity$WebAppInterface#onData`
- `com.xxx.zzz.globp.UtilsGfgsd#gotoAccessibilityService`
- `com.xxx.zzz.notifp.DialogActivityasd#onCreate`
- `res/xml/serviceconfig.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **入口全部隐藏**：桌面图标（`Grab`，另有 Facebook、Google Play、Gmail、WhatsApp、TikTok 等 10 个 `activity-alias` 伪装图标）指向 `Main2`，界面只有 `TextView(" ")` 空白页，随即 `Payload.start2()` → `MainActivity` → `PermissionsActivity`，全程无真实业务界面。
- **权限页伪装成系统窗口**：`PermissionsActivity.onCreate` 调用 `Window.setType(2006)`（系统级悬浮窗）并设置 `FLAG_SHOW_WHEN_LOCKED`，无布局文件，只负责弹引导层。
- **引导内容 = 内嵌伪造的“系统无障碍列表页”**：`work()` 取 `getS227()` 的 Base64 串解码（约 24KB HTML），`loadDataWithBaseURL` 注入全屏 WebView（`LayoutParams(-1,-1,2,262144,-2)`），并注册 `Android` JS 桥。HTML 逐字复刻系统字段：`Accessibility Service`、`DOWNLOADED SERVICES`、`Switch Access`、`TalkBack`、`OFF`，主按钮为 `Start Accessibility`，并按 `Locale` 动态替换 30 余种语言。
- **分两步跳设置**：按钮回调 `WebAppInterface.onData()` → `openAccessabilitySettings()` 销毁遮罩 → `UtilsGfgsd.gotoAccessibilityService()` 发出 `android.settings.ACCESSIBILITY_SETTINGS`；同时 `getS228()` 非空时再启动 `DialogActivityasd`，以 `windowIsFloating(2006)` 底部对齐浮层把第二份 Base64 高仿列表压在系统设置页之上（`ensureAccessibilityServiceEnabled` 中 2000ms 后跳转、3000ms 后二次动作）。
- **无跳过 + 拒绝循环**：HTML 只有开启入口；`onResume` 无条件 `work()`，`onBackPressed` 也直接 `work()`，从设置页返回即重新拉起，直至 `hasAllPermission()`（无障碍+悬浮窗+全部危险权限+doze 白名单）满足。
- **系统列表项话术掩饰**：`serviceconfig.xml` 申请 `typeAllMask / canRetrieveWindowContent / canPerformGestures / flagRetrieveInteractiveWindows`，而 `android:description` 仅为“If accessibility permission has been on, please turn off then turn on.”，以“关掉再开”话术替代真实用途说明。

已登记风险：**R-001**（autonomous_audit / high / deceptive_behavior）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链路全部静态可见：无障碍服务类、PermissionsActivity 的 2006 悬浮窗 WebView、两份 Base64 内嵌 HTML 引导页（已解码为 23KB 仿系统无障碍列表）、ACTION_ACCESSIBILITY_SETTINGS 跳转点、DialogActivityasd 设置页叠层浮窗、onResume/onBackPressed 重跳逻辑均可完整还原；未发现加壳、V2 加密载荷或远端 HTML 下发，HTML 语言表与文案硬编码在 DEX 常量中。",
  "summary_one_liner": "应用以无界面的 2006 悬浮窗 Activity 加载内嵌 Base64 伪造的『系统无障碍服务列表页』（含 DOWNLOADED SERVICES/Switch Access/TalkBack/OFF 与 Start Accessibility 按钮），点击后跳系统无障碍设置并在其上再叠一层底部高仿浮层，全程无跳过按钮且返回键/onResume 反复重跳，直到开启 GrabAssistService。",
  "disguise_identity": {
    "app_display_name": "Grab",
    "claimed_brand_or_persona": "包名冒用 com.tencent.mm（微信），图标别名伪装 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram；引导页冒充 Android 系统『无障碍服务』设置界面",
    "a11y_service_label": "GrabAssistService",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 包名与类前缀冒用 com.tencent.mm；2) 10 个 activity-alias 以主流社交/商店图标与标签伪装桌面入口，targetActivity 均指向 Main2；3) 主入口内容视图为 TextView(\" \") 单空格，界面空白；4) 引导页 HTML 以 Base64 字符串内嵌，占位符 %Enable_Accessibility_Service% 与 <html lang=\"en\"> 运行期按语言替换；5) 无障碍服务 description 用『请先关闭再开启』话术淡化真实权限范围；6) 设备管理员 receiver label 为空字符串、description 为 Add application to admin"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tencent.mm.Main2（桌面 LAUNCHER，主题 @style/ACL，noHistory）",
      "trigger_event": "用户点击桌面图标，Main2.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "TextView 内容为 \" \"（单个空格，无任何界面文字）",
      "shown_text_zh": "纯空白页面，用户看不到任何业务功能",
      "user_action_requested": "无显式交互，页面立即 finish 并跳转下一环节",
      "code_anchor": "com.tencent.mm.Main2.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.xxx.zzz.Payload.start2 → com.xxx.zzz.MainActivity.start → com.xxx.zzz.PermissionsActivity",
      "trigger_event": "Main2.onCreate 中 PermissionsActivity.Companion.hasAllPermission() 返回 false 时调用 Payload.INSTANCE.start2()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静默串联跳转，MainActivity 同样只设置 TextView(\" \") 后 startActivity(PermissionsActivity) 并 finish",
      "user_action_requested": "无，用户无选择权",
      "code_anchor": "com.xxx.zzz.Payload#start2 / com.xxx.zzz.MainActivity#start"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.xxx.zzz.PermissionsActivity（setType(2006) 系统悬浮窗层，无布局，仅承载 WindowManager 全屏 WebView）",
      "trigger_event": "PermissionsActivity.onCreate → onResume → work()",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "%Enable_Accessibility_Service% / Start Accessibility / >>",
      "shown_text_zh": "『启用无障碍服务』标题 + 『启动无障碍』按钮 + 向右箭头，页面其余为仿系统无障碍列表项",
      "user_action_requested": "点击 Start Accessibility 按钮（页面无取消、跳过或返回入口）",
      "code_anchor": "com.xxx.zzz.PermissionsActivity#work / PermissionsActivity$Companion#getS227"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "PermissionsActivity 内全屏 WebView（WindowManager.LayoutParams(-1,-1,2,262144,-2)，注册 JavascriptInterface \"Android\"）",
      "trigger_event": "work() 中 this.launchHttp 为 true 时解码 Base64 并 loadDataWithBaseURL(null, html, \"text/html\", \"UTF-8\", null)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF",
      "shown_text_zh": "逐字复刻系统无障碍设置页：『无障碍服务』『已下载的服务』『切换访问』『TalkBack』『关闭』等系统同款字段与开关态",
      "user_action_requested": "按仿系统列表样式引导用户『打开』服务，实为触发 JS 桥 onData()",
      "code_anchor": "com.xxx.zzz.PermissionsActivity$WebAppInterface#onData"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统页 android.settings.ACCESSIBILITY_SETTINGS（Intent FLAG_ACTIVITY_CLEAR_TOP|NEW_TASK）",
      "trigger_event": "WebAppInterface.onData() → openAccessabilitySettings() 销毁遮罩 → UtilsGfgsd.gotoAccessibilityService()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧不呈现文字，直接拉起系统页）",
      "shown_text_zh": "跳转到系统无障碍服务列表，由用户手动找到 GrabAssistService 并开启",
      "user_action_requested": "在系统列表中手动开启 GrabAssistService（服务名与桌面名 Grab 不一致，易误认）",
      "code_anchor": "com.xxx.zzz.globp.UtilsGfgsd#gotoAccessibilityService"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.xxx.zzz.notifp.DialogActivityasd（windowIsFloating 2006，gravity=80 底部对齐，LayoutParams(-1,-2,...,262152,-3)）",
      "trigger_event": "gotoAccessibilityService() 中 PermissionsActivity.Companion.getS228().length() > 0 时，在拉起系统设置后立即 startActivity(DialogActivityasd)；ensureAccessibilityServiceEnabled 内 postDelayed(2000) 跳设置、postDelayed(3000) 执行后续包装",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "第二份 Base64 HTML（与首份同为仿系统无障碍列表模板，含 Start Accessibility 与 DOWNLOADED SERVICES / Switch Access / TalkBack / OFF）",
      "shown_text_zh": "在系统无障碍设置页之上叠加底部高仿系统列表浮层，指向应点击的服务项位置",
      "user_action_requested": "照浮层指引点击系统列表中的服务并确认开启",
      "code_anchor": "com.xxx.zzz.notifp.DialogActivityasd#onCreate"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "PermissionsActivity.onResume / onBackPressed（从系统设置返回时）",
      "trigger_event": "用户从系统设置返回或按返回键：onResume 无条件调用 work()；onBackPressed 直接调用 work()",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "%Enable_Accessibility_Service% / Start Accessibility",
      "shown_text_zh": "重新显示同一仿系统引导页，要求再次开启，用户无法退出或跳过",
      "user_action_requested": "反复要求开启无障碍；无取消、无跳过、无降级路径",
      "code_anchor": "com.xxx.zzz.PermissionsActivity#onBackPressed / #onResume"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "系统无障碍服务列表项 GrabAssistService（com.xxx.zzz.accessppp.AccessibilityServiceQ，配置 @xml/serviceconfig）",
      "trigger_event": "服务被开启后 PermissionsActivity.Companion.hasAllPermission() 转为 true，Main2.onCreate 走 successWork()/saveCurAppName() 分支",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "shown_text_zh": "『如果无障碍权限已经开启，请关闭后再重新开启一次』——以重启话术替代真实用途说明",
      "user_action_requested": "按提示反复关闭再开启服务（实际授予 typeAllMask / canRetrieveWindowContent / canPerformGestures / flagRetrieveInteractiveWindows 全量能力）",
      "code_anchor": "res/xml/serviceconfig.xml / res/values/strings.xml#text_accessibility_service_description"
    }
  ],
  "text_presentation_locations": [
    "PermissionsActivity 通过 WindowManager 添加的全屏 WebView（悬浮窗类型 2006）：内嵌 Base64 HTML 首屏，标题 %Enable_Accessibility_Service%，按钮 Start Accessibility，仿系统列表项 Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF",
    "DialogActivityasd 通过 WindowManager 添加的底部浮层 WebView（gravity=80，windowIsFloating）：第二份 Base64 HTML，叠在系统无障碍设置页之上继续指引",
    "系统无障碍列表项描述：res/values/strings.xml 中 text_accessibility_service_description = If accessibility permission has been on, please turn off then turn on.",
    "设备管理员声明描述：strings.xml 中 adm = Add application to admin，AdminReceiverzxc 的 android:label 为空字符串",
    "桌面图标与标签：AndroidManifest 中 application label Grab 与 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 十个 activity-alias",
    "主入口界面：Main2 与 MainActivity 均 setContentView(new TextView(this)) 且 setText(\" \")，无任何说明文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "%Enable_Accessibility_Service%",
      "text_zh": "%启用无障碍服务%（占位符，运行期按系统语言替换为对应文案）",
      "source_location": "classes.dex 内嵌 Base64 HTML（PermissionsActivity$Companion#getS227 解码），由 constNm.ключ_от_всего 占位符替换",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Start Accessibility",
      "text_zh": "启动无障碍",
      "source_location": "classes.dex 内嵌 Base64 HTML 主按钮（点击经 JavascriptInterface \"Android\".onData 跳转）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service",
      "text_zh": "无障碍服务",
      "source_location": "内嵌 HTML 语言表 objLang.en.accessability1，仿系统无障碍设置页标题",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "DOWNLOADED SERVICES",
      "text_zh": "已下载的服务",
      "source_location": "内嵌 HTML 语言表 objLang.en.downloadedservice，仿系统无障碍列表分组标题",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Switch Access",
      "text_zh": "切换访问",
      "source_location": "内嵌 HTML 语言表 objLang.en.switchaccess，用作列表项名",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "TalkBack",
      "text_zh": "TalkBack（系统读屏服务）",
      "source_location": "内嵌 HTML 语言表 objLang.en.talkback，用作列表项名",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "OFF",
      "text_zh": "关闭（开关状态文字）",
      "source_location": "内嵌 HTML 语言表 objLang.en.off，用于仿造系统开关态",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "zh",
      "text_verbatim": "無障礙服務 / 下載的服務 / 開關訪問 / 頂嘴 / 關",
      "text_zh": "繁体中文版系统无障碍设置页同款字段（TalkBack 被误译为『頂嘴』）",
      "source_location": "内嵌 HTML 语言表 objLang.zh（按 Locale 动态替换 <html lang>）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开启，请关闭后再重新开启一次。",
      "source_location": "res/values/strings.xml#text_accessibility_service_description（serviceconfig.xml 的 android:description）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Add application to admin",
      "text_zh": "将应用添加到设备管理员",
      "source_location": "res/values/strings.xml#adm（AdminReceiverzxc 的 android:description，label 为空字符串）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "PermissionsActivity.onResume 无条件调用 work()，onBackPressed 也直接调用 work()；用户从系统无障碍设置返回或按返回键即重新渲染仿系统引导页并再次要求开启，同时 ensureAccessibilityServiceEnabled 以 postDelayed(2000) 重跳设置、postDelayed(3000) 叠加底部引导浮层，形成循环直到 hasAllPermission()（无障碍+悬浮窗+全部危险权限+doze 白名单）为真",
    "overlay_or_fake_settings": "两者兼有：PermissionsActivity 本身即以 Window.setType(2006) 悬浮窗层承载全屏 WebView，页面内容为高仿系统无障碍设置页（Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF 及开关态）；跳系统设置后 DialogActivityasd 再以 windowIsFloating(2006) 底部对齐浮层叠在系统页之上继续指引",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=28，未使用应用详情右上角『允许受限设置』或 Session 安装器话术，直接跳 android.settings.ACCESSIBILITY_SETTINGS）",
    "post_grant_anti_removal": "有：无障碍服务配置声明 typeAllMask、flagRetrieveInteractiveWindows、canPerformGestures 与 flagRequestFilterKeyEvents，且 DEX 线索含 PERFORM_GLOBAL_ACTION / WATCH_SETTINGS，可监听设置页并用全局返回/主页动作阻止撤权（本次未逐方法展开该分支，属未完全展开部分）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 com.xxx.zzz.PermissionsActivity 或 com.xxx.zzz.notifp.DialogActivityasd 成为前台窗口（二者均为 2006 悬浮窗层 WebView，无正常 Activity 布局），以及 Intent 发出 android.settings.ACCESSIBILITY_SETTINGS 的瞬间；亦可在冷启动 Main2 后 1 秒内截图（Payload.start 使用 postDelayed 1000ms）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动伪造系统无障碍设置页（首层引导）",
        "page_identifier": "全屏 WebView，标题 %Enable_Accessibility_Service%，按钮 Start Accessibility，列表含 DOWNLOADED SERVICES / Switch Access / TalkBack / OFF",
        "why_most_useful": "该页是判定『伪造系统设置页』的核心证据：字段与系统无障碍页逐字一致，但由应用自身 WebView 渲染，且无跳过入口",
        "observable_utg_signals": [
          "页面文案含 DOWNLOADED SERVICES / Switch Access / TalkBack 但控件非系统组件",
          "存在 Start Accessibility 主按钮且无取消/跳过元素",
          "同一页面在不同系统语言下切换 lang 属性（动态替换 <html lang>）"
        ]
      },
      {
        "page_role": "跳转系统设置后 2000ms 压栈的底部引导浮层",
        "page_identifier": "系统无障碍设置页之上、屏幕底部对齐的半屏 WebView（DialogActivityasd，windowIsFloating 2006）",
        "why_most_useful": "叠层直接覆盖系统设置页并指向应点击项，是『设置页叠层指引』的直接运行证据，也是区分合法引导与诱导的关键",
        "observable_utg_signals": [
          "系统设置页上方出现应用包名的悬浮窗节点（非系统 UI）",
          "底部浮层含与首层相同的仿系统列表文案",
          "浮层出现时间与跳转系统设置相隔约 2 秒"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已下载的服务中的 GrabAssistService 条目（description: If accessibility permission has been on, please turn off then turn on.）",
        "why_most_useful": "确认用户实际被要求开启的是应用自有服务，且描述话术与真实能力（读取窗口内容/模拟手势）不符，并可与桌面名 Grab 形成身份不一致对照",
        "observable_utg_signals": [
          "服务标签 GrabAssistService 与桌面应用名 Grab 不一致",
          "description 仅提示『关闭再开启』而未说明实际能力",
          "开启后应用立即进入 successWork 分支并隐藏入口"
        ]
      },
      {
        "page_role": "拒权后重跳页面",
        "page_identifier": "从系统设置返回后重新出现的 PermissionsActivity 全屏 WebView",
        "why_most_useful": "证明无跳过且存在拒绝循环，是强制引导定性的运行期证据",
        "observable_utg_signals": [
          "返回系统设置后 1 秒内同一引导页再次出现",
          "多次返回后页面文案与结构不变且始终无取消按钮",
          "按返回键不退出应用而重新加载引导页"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导 HTML 为 DEX 内 Base64 字符串并在运行期做占位符与 lang 替换，若仅在包内检索 assets/*.html 或明文关键词会漏检；须在运行期捕获 PermissionsActivity / DialogActivityasd 的 WebView 窗口。另入口界面为 TextView(\" \") 单空格空白页，冷启动首次截图可能只捕获空白窗口，需在 1 秒后（Payload.start 的 postDelayed 1000ms）再抓取。无障碍撤权对抗（GLOBAL_ACTION_BACK/HOME、WATCH_SETTINGS）本次未逐方法展开，属未完全核验分支。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.xxx.zzz.PermissionsActivity#work",
    "com.xxx.zzz.PermissionsActivity#openAccessabilitySettings",
    "com.xxx.zzz.PermissionsActivity$WebAppInterface#onData",
    "com.xxx.zzz.globp.UtilsGfgsd#gotoAccessibilityService",
    "com.xxx.zzz.notifp.DialogActivityasd#onCreate",
    "res/xml/serviceconfig.xml"
  ]
}
```

</details>
