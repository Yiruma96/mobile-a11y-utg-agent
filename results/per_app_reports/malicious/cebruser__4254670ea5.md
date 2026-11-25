# MR_123__4254670ea5｜cebruser — Google Play

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：264.6s

## 1. 一句话核心结论

- **核心申请方式**：以“Google Play/Google Update”身份内嵌本地 HTML 高仿系统无障碍服务列表页，页面唯一动作经 JS 桥跳转真实 ACCESSIBILITY_SETTINGS，并由后台服务每秒轮询反复重跳直至用户开启无障碍。
- **静态可见性说明**：无加壳、无加密二阶段载荷。伪造设置页 HTML 以明文 Base64 内嵌在 classes.dex，字符串常量采用 RC4(密钥取串首12字符)+hex+Base64 三层硬编码，已用脚本全部静态还原（471 条），引导文案、日志串与远端模板占位符均可读；未发现从远端下发 HTML 的路径，远端仅下发文字/指令。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4254670ea5f353263570792a8ff4a1e6ea35999c2454fa1ec040786d7be33b69` |
| 包名 / 年份 | `com.wjnjrmigikmpher.efaunxm` / 2020 |
| 家族 / 品类 | **cebruser**（同池样本数：3） |
| 原始来源标识 | https://gbhackers.com/hackers-breached-mdm-servers-to-install-android-malware/ |
| 桌面显示名 | Google Play |
| 引导页宣称品牌/身份 | Google Play（应用名）/ Google Update（无障碍服务名）/ 系统无障碍设置页（Switch Access、TalkBack、DOWNLOADED SERVICES） |
| 系统无障碍列表服务名 | Google Update |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务无 android:description / android:summary（res/xml/tttannftd.xml 仅声明事件与 canRetrieveWindowContent，系统列表仅显示“Google Update”四字，无用途说明）；类名/包名全随机化（com.wjnjrmigikmpher.efaunxm、hfstolkr、ascvgkhzwyroo）；所有 UI 文案与跳转 action 均以 RC4+hex+Base64 硬编码隐藏；WebView 内页面结构与系统无障碍页同构，用 TalkBack/Switch Access 等真实服务名做陪衬，另配闪烁箭头动画；多处 Activity 设 label=""、Theme.NoDisplay、excludeFromRecents 隐藏自身；未使用 activity-alias，也未伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.wjnjrmigikmpher.efaunxm.hfstolkr` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.wjnjrmigikmpher.efaunxm.fgakwv（MAIN/LAUNCHER，Theme.Translucent.NoTitleBar） | onCreate（用户点桌面图标启动） | 原生Activity（瞬时、无界面） | **原文**：无（onCreate 中无 setContentView，非目标厂商直接 finish()）<br>**译注**：无可见界面，静默完成初始化与开关判定 | 无；用户仅看到图标被点击后一闪 | `com.wjnjrmigikmpher.efaunxm.fgakwv.onCreate` |
| 2 | 业务功能触发（条件判定） | a.b(Context, hfstolkr.class) 读取 Settings.Secure.enabled_accessibility_services | onCreate 中 Build.MANUFACTURER / MIUI 版本号判定通过后，检查无障碍服务是否已启用 | 不可静态还原（无 UI，纯判定分支） | 无 | 无 | `com.wjnjrmigikmpher.efaunxm.a.b(Context, Class) / com.wjnjrmigikmpher.efaunxm.fgakwv.onCreate` |
| 3 | 引导说明页（伪造系统设置页） | com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo（WebView Activity，loadDataWithBaseURL 加载 DEX 内 Base64 HTML） | onCreate 中 startActivity(ascvgkhzwyroo) 后页面渲染完成 | 本地HTML WebView | **原文**：%Enable_Accessibility_Service% / Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / Start Accessibility / OFF / >><br>**译注**：标题为“启用无障碍服务”（占位符由加密配置注入），下方完整仿制系统无障碍页：分组“已下载的服务”，列出“开关访问”“TalkBack”，并有“启动无障碍”条目与右侧“OFF”开关，底部为“>>”按钮，箭头闪烁指向开关 | 点击“启动无障碍”条目或“>>”按钮；页面无取消、跳过或关闭入口，仅能按返回键退出（退出后会被重新拉起） | `com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo.onCreate / pages.txt（HTML: onclick="Android.openAccessibilityService()"）` |
| 4 | 跳无障碍设置 | 系统页 android.settings.ACCESSIBILITY_SETTINGS | 点击 HTML 元素 → JS 桥 Android.openAccessibilityService() 回调 | 系统无障碍页 | **原文**：无（应用自身不渲染，交由系统 Settings 显示）<br>**译注**：跳转至系统“无障碍/已下载的服务”列表，用户需自行找到“Google Update”并开启 | 在系统列表中点击“Google Update”并确认开启（此步需用户真实操作，无法被应用代劳） | `com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo$c.openAccessibilityService` |
| 5 | 拒权反馈循环 | com.wjnjrmigikmpher.efaunxm.lqmgyyfk（exported Service，onStartCommand） | 服务启动后进入 while(true)：Thread.sleep(1000) → 复查 enabled_accessibility_services → 未启用则再次 startActivity | 系统无障碍页（被反复重新压栈） | **原文**：无（重复跳转系统设置页）<br>**译注**：用户返回或拒绝后，每秒被重新拉回无障碍设置页，无法正常退出 | 无有效“拒绝”路径；用户只能开启服务，或强杀进程/断网 | `com.wjnjrmigikmpher.efaunxm.lqmgyyfk.onStartCommand` |
| 6 | 获权后动作 | com.wjnjrmigikmpher.efaunxm.hfstolkr（AccessibilityService，label=Google Update） | onServiceConnected 回调 | 不可静态还原（后台无界面） | **原文**：无（日志串："Blocked attempt to disable accessibility service[143523#]"、"AccessibilityClickButton"、"Start Accessibility"）<br>**译注**：无界面；服务进入 eventTypes=-1、flags=17 全量监听，具备读屏、模拟点击与阻止撤权能力 | 无 | `com.wjnjrmigikmpher.efaunxm.hfstolkr.onServiceConnected / com.wjnjrmigikmpher.efaunxm.e.a` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- ascvgkhzwyroo：全屏 WebView（setContentView(webView)）加载 DEX 内 Base64 硬编码 HTML，为引导文案的唯一呈现载体
- 该 HTML 顶部标题 <h3>%Enable_Accessibility_Service%</h3>（占位符由 ascvgkhzwyroo.onCreate 从加密配置 a.aO 取模板后 replace 注入，并按系统语言替换文案）
- HTML 内 <div class="header"> + id=accessability1（Accessibility Service）、id=downloadedservice（DOWNLOADED SERVICES）、id=switchaccess（Switch Access）、id='talkback'（TalkBack）、id='startaccessibility'（Start Accessibility）、id=off2/off3/off4（OFF）
- HTML 内 <div class="els" onclick="Android.openAccessibilityService();"> 与 <button onclick="Android.openAccessibilityService();"> >> 两个可点区域，配 st01 缩放闪烁动画与内嵌 base64 箭头图
- HTML 内嵌 objLang 多语言字典（en/de/nl/zh-TW/cs/it/ja/ko 等），同一套伪造无障碍文案按 Locale 切换
- 系统无障碍服务列表：Manifest android:label="Google Update"，但 res/xml/tttannftd.xml 无 android:description，故系统页不呈现任何用途说明
- 桌面图标名：AndroidManifest application android:label="Google Play"

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | %Enable_Accessibility_Service% | 启用无障碍服务（模板占位符，运行期被替换为对应语言文案） | `classes.dex 内嵌 HTML（ascvgkhzwyroo.onCreate 中 a.e(this.b.aO) 模板 + replace 注入）` | 假更新 |
| en | Accessibility Service | 无障碍服务 | `内嵌 HTML id=accessability1（objLang['en']）` | 假更新 |
| en | DOWNLOADED SERVICES | 已下载的服务 | `内嵌 HTML id=downloadedservice（objLang['en']）` | 假更新 |
| en | Switch Access | 开关访问（系统真实无障碍服务名，用作陪衬增强可信度） | `内嵌 HTML id=switchaccess（objLang['en']）` | 假更新 |
| en | TalkBack | TalkBack（系统读屏服务名，用作陪衬） | `内嵌 HTML id='talkback'（objLang['en']）` | 假更新 |
| en | Start Accessibility | 启动无障碍 | `内嵌 HTML id='startaccessibility'（<div class="an"> 动画高亮行）` | 受限设置分步教学 |
| en | OFF | 关闭 | `内嵌 HTML id=off2/off3/off4（objLang['en']）` | 假更新 |
| en | Click on me to activate / Enable | 点我激活 / 启用 | `加密字符串常量（RC4+hex+Base64 还原，用于引导点击）` | 受限设置分步教学 |
| en | Blocked attempt to disable accessibility service[143523#] | 已阻止尝试关闭无障碍服务[143523#] | `加密字符串常量（上报日志串，含家族标识 143523）` | 教唆忽视警告 |
| en | Google Update | Google 更新 | `AndroidManifest.xml 无障碍服务 android:label` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：lqmgyyfk.onStartCommand 内 while(true)：每次 Thread.sleep(1000) 后复查 Settings.Secure.enabled_accessibility_services，未启用即再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)（FLAG_ACTIVITY_NEW_TASK|CLEAR_TOP|RESET_TASK_IF_NEEDED），用户从设置页返回会被立刻重新拉起，构成拒权死循环；另由 fgakwv.onCreate 设置 10000ms 周期 AlarmManager 广播自拉起，进程被杀后仍可重入。
- **遮罩叠层 / 高仿系统设置页**：不使用悬浮窗/透明遮罩（未申请 SYSTEM_ALERT_WINDOW，overlay 线索为空）；而是以全屏 WebView Activity 高仿系统无障碍设置页（同构标题、分组、TalkBack/Switch Access 条目、OFF 开关、闪烁箭头），点击后跳真实系统页。
- **Android 13+ 受限设置（Restricted Settings）应对**：未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转与 Android 13+“允许受限设置”教学；仅见 e.a(Context)/a.a(Context,...) 以加密字符串构造 miui.intent.action.APP_PERM_EDITOR + com.miui.securitycenter.permissions.PermissionsEditorActivity（extra_pkgname）跳厂商权限编辑页。
- **获权后即时行为与防撤权机制**：有：字符串表存在 "Blocked attempt to disable accessibility service[143523#]"，且 onAccessibilityEvent 内对事件文本做包含匹配后 performAction(16) 模拟点击；获权后 eventTypes=-1 全量监听窗口，具备识别并阻断用户在系统设置中关闭无障碍的自动化能力（防撤权路径已具备，具体触发条件因事件处理体庞大未逐行还原）。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以“监测到 startActivity(Intent android.settings.ACCESSIBILITY_SETTINGS)”为主钩子（同时命中 ascvgkhzwyroo$c.openAccessibilityService 与 lqmgyyfk.onStartCommand 两处）；辅以冷启动后首个 Activity 为 ascvgkhzwyroo（WebView 载入含 'Accessibility Service' 文本页）作为前置钩子，先抓伪造页、再抓系统页，可完整还原“伪造页→真系统页→循环重跳”三段。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：伪造页文本为 HTML 真实文本节点，UTG 可直接取；但页面标题 %Enable_Accessibility_Service% 由加密配置运行期注入，若网络配置未下发则标题可能为空，需靠固定文案（DOWNLOADED SERVICES/Start Accessibility）兜底识别。另：远端仅下发文字/指令，HTML 不在远端，故无远端 HTML 盲区；应用未使用悬浮窗遮罩，故无 overlay 类盲区；lqmgyyfk 循环受 Build.MANUFACTURER 判定约束，在非目标机型上不会触发，动态验证须选用对应厂商设备。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动伪造系统无障碍设置页** | Activity com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo 内的 WebView，页面含 'Accessibility Service'、'DOWNLOADED SERVICES'、'Start Accessibility'、'OFF' | 这是全部诱导文案的唯一载体，与真实系统页的同构程度是判定“假设置页诱导”的决定性证据 | 页面文本节点含 DOWNLOADED SERVICES + TalkBack + Switch Access（真实系统页不会以 WebView 承载）；包名 com.wjnjrmigikmpher.efaunxm 的 Activity 承载无障碍设置版式；存在闪烁/缩放动画箭头指向 OFF 开关 |
| **跳转后的真实系统无障碍列表项** | Settings 无障碍“已下载的服务”列表中条目 'Google Update' | 验证用户被引导的目标对象：服务名伪装 Google、且无任何用途描述文字 | 列表项文本为 'Google Update'；该项无 summary/description 副标题；归属包名 com.wjnjrmigikmpher.efaunxm 与 Google 无关联 |
| **拒权返回后的循环重跳页（第2次+系统设置页）** | 1 秒后再次压栈的 android.settings.ACCESSIBILITY_SETTINGS | 证明存在强制引导/拒权循环，可与良性授权说明区分 | 按返回键后 ≤2s 内同一系统页再次成为前台 Activity；重复次数与 1s 轮询节奏一致；期间前台无本应用取消/跳过按钮 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.wjnjrmigikmpher.efaunxm.fgakwv.onCreate`
- `com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo.onCreate`
- `com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo$c.openAccessibilityService`
- `com.wjnjrmigikmpher.efaunxm.lqmgyyfk.onStartCommand`
- `com.wjnjrmigikmpher.efaunxm.hfstolkr.onServiceConnected`
- `res/xml/tttannftd.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（基于静态代码核实）

**一句话**：该样本并不依靠弹窗来“说明权限”，它用一段内嵌在 DEX 中的本地 HTML **高仿出系统“无障碍服务列表”界面**，其中包含 TalkBack、Switch Access 与 OFF 开关；页面上的任意点击都通过 JS 桥跳转到真实的 `android.settings.ACCESSIBILITY_SETTINGS`，同时后台还有一个服务以 `while(true)` 循环每秒重新拉起该设置页，直到用户开启无障碍。

关键事实：

1. **冷启动直接拦截**：[fgakwv.onCreate()](<resource-unit:#1.dex1 code:com.wjnjrmigikmpher.efaunxm.fgakwv#onCreate>)（MAIN/LAUNCHER，label=`Google Play`）先做初始化，再用 [a.b()](<resource-unit:#1.dex1 code:com.wjnjrmigikmpher.efaunxm.a#b>) 读取 `Settings.Secure.enabled_accessibility_services`，判断无障碍服务是否已启用：如果未启用，就 `startActivity(ascvgkhzwyroo)`；如果已启用，就调用 `e.a(this)`。此外还会设置一个 10000ms 的周期广播闹钟用于自拉起；在非目标厂商设备上，该应用会直接 `finish()`，这是环境开关式的分发。
2. **伪造系统设置页**：[ascvgkhzwyroo.onCreate()](<resource-unit:#1.dex1 code:com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo#onCreate>) 创建 `WebView`，开启 JS，注入 `Android` 桥，并通过 `loadDataWithBaseURL` 加载 DEX 内 Base64 硬编码的 HTML（[pages.txt](<resource-unit:<local_path> file:all>)）。页面结构逐项复刻系统无障碍页：标题 `Accessibility Service`、分组 `DOWNLOADED SERVICES`、条目 `Switch Access` / `TalkBack` / `Start Accessibility`、右侧 `OFF`，并叠加 `st01` 闪烁箭头与呼吸动画指向开关；内置 en/de/nl/zh-TW/cs/it/ja/ko 等十余种语言，属于面向多语言地区的批量投放模板。
3. **唯一动作 = 跳系统设置**：页面 `onclick="Android.openAccessibilityService()"` 与 `>>` 按钮都绑定 [ascvgkhzwyroo$c.openAccessibilityService()](<resource-unit:#1.dex1 code:com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo$c#openAccessibilityService>)，该方法体只有一句 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。页面**没有取消、跳过或关闭按钮**，也没有任何真实功能项，所谓“开关”只是贴图。
4. **拒绝后循环重推**：[lqmgyyfk.onStartCommand()](<resource-unit:#1.dex1 code:com.wjnjrmigikmpher.efaunxm.lqmgyyfk#onStartCommand>) 在特定厂商且 API≥10 时进入 `while(true)`：`sleep(1000)` → 复查服务是否启用 → 未启用则再次 `startActivity(ACCESSIBILITY_SETTINGS)`（FLAG_ACTIVITY_NEW_TASK 等三重 flag）。用户从设置页返回后会被持续弹回，形成拒权死循环。
5. **身份与披露**：桌面名 `Google Play`，无障碍服务名 `Google Update`，包名 `com.wjnjrmigikmpher.efaunxm` 与二者毫无关联；[res/xml/tttannftd.xml](<resource-unit:#1 file:res/xml/tttannftd.xml>) 无 `android:description`/`android:summary`，系统列表里只有“Google Update”四字，用户看不到 `canRetrieveWindowContent="true"`、`flagIncludeNotImportantViews` 这类高危能力说明。
6. **获权后动作**：[hfstolkr.onServiceConnected()](<resource-unit:#1.dex1 code:com.wjnjrmigikmpher.efaunxm.hfstolkr#onServiceConnected>) 将 `eventTypes=-1`、`flags=17` 设为全量监听；`e` 类用 `performAction(16)` 模拟点击、`findAccessibilityNodeInfosForViewId` 定位控件，并在字符串表中留有 `Blocked attempt to disable accessibility service[143523#]`（阻止撤权）与 `AccessibilityClickButton`，指向银行木马式自动化。
7. **受限设置引导**：未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转；`e.a(Context)`/`a.a(Context,...)` 使用加密字符串构造 `miui.intent.action.APP_PERM_EDITOR` + `com.miui.securitycenter...PermissionsEditorActivity`（`extra_pkgname`）进入厂商权限编辑页，属于厂商定制路径，未确认 Android 13+ 受限设置教学流程。
8. **可见性**：无加壳；全部 UI 文本以 RC4（密钥 = 串前 12 字符）+ hex + Base64 三层硬编码，已通过脚本静态还原 471 条；伪造页 HTML 以明文 Base64 内嵌于 DEX。因此**纯静态可见**，无需动态脱壳。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "无加壳、无加密二阶段载荷。伪造设置页 HTML 以明文 Base64 内嵌在 classes.dex，字符串常量采用 RC4(密钥取串首12字符)+hex+Base64 三层硬编码，已用脚本全部静态还原（471 条），引导文案、日志串与远端模板占位符均可读；未发现从远端下发 HTML 的路径，远端仅下发文字/指令。",
  "summary_one_liner": "以“Google Play/Google Update”身份内嵌本地 HTML 高仿系统无障碍服务列表页，页面唯一动作经 JS 桥跳转真实 ACCESSIBILITY_SETTINGS，并由后台服务每秒轮询反复重跳直至用户开启无障碍。",
  "disguise_identity": {
    "app_display_name": "Google Play",
    "claimed_brand_or_persona": "Google Play（应用名）/ Google Update（无障碍服务名）/ 系统无障碍设置页（Switch Access、TalkBack、DOWNLOADED SERVICES）",
    "a11y_service_label": "Google Update",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务无 android:description / android:summary（res/xml/tttannftd.xml 仅声明事件与 canRetrieveWindowContent，系统列表仅显示“Google Update”四字，无用途说明）；类名/包名全随机化（com.wjnjrmigikmpher.efaunxm、hfstolkr、ascvgkhzwyroo）；所有 UI 文案与跳转 action 均以 RC4+hex+Base64 硬编码隐藏；WebView 内页面结构与系统无障碍页同构，用 TalkBack/Switch Access 等真实服务名做陪衬，另配闪烁箭头动画；多处 Activity 设 label=\"\"、Theme.NoDisplay、excludeFromRecents 隐藏自身；未使用 activity-alias，也未伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.wjnjrmigikmpher.efaunxm.fgakwv（MAIN/LAUNCHER，Theme.Translucent.NoTitleBar）",
      "trigger_event": "onCreate（用户点桌面图标启动）",
      "ui_carrier": "原生Activity（瞬时、无界面）",
      "shown_text_verbatim": "无（onCreate 中无 setContentView，非目标厂商直接 finish()）",
      "shown_text_zh": "无可见界面，静默完成初始化与开关判定",
      "user_action_requested": "无；用户仅看到图标被点击后一闪",
      "code_anchor": "com.wjnjrmigikmpher.efaunxm.fgakwv.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发（条件判定）",
      "screen_or_component": "a.b(Context, hfstolkr.class) 读取 Settings.Secure.enabled_accessibility_services",
      "trigger_event": "onCreate 中 Build.MANUFACTURER / MIUI 版本号判定通过后，检查无障碍服务是否已启用",
      "ui_carrier": "不可静态还原（无 UI，纯判定分支）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "未启用 → 拉起伪造引导页；已启用 → 直接进入后续控制流程",
      "user_action_requested": "无",
      "code_anchor": "com.wjnjrmigikmpher.efaunxm.a.b(Context, Class) / com.wjnjrmigikmpher.efaunxm.fgakwv.onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页（伪造系统设置页）",
      "screen_or_component": "com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo（WebView Activity，loadDataWithBaseURL 加载 DEX 内 Base64 HTML）",
      "trigger_event": "onCreate 中 startActivity(ascvgkhzwyroo) 后页面渲染完成",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "%Enable_Accessibility_Service% / Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / Start Accessibility / OFF / >>",
      "shown_text_zh": "标题为“启用无障碍服务”（占位符由加密配置注入），下方完整仿制系统无障碍页：分组“已下载的服务”，列出“开关访问”“TalkBack”，并有“启动无障碍”条目与右侧“OFF”开关，底部为“>>”按钮，箭头闪烁指向开关",
      "user_action_requested": "点击“启动无障碍”条目或“>>”按钮；页面无取消、跳过或关闭入口，仅能按返回键退出（退出后会被重新拉起）",
      "code_anchor": "com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo.onCreate / pages.txt（HTML: onclick=\"Android.openAccessibilityService()\"）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "点击 HTML 元素 → JS 桥 Android.openAccessibilityService() 回调",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用自身不渲染，交由系统 Settings 显示）",
      "shown_text_zh": "跳转至系统“无障碍/已下载的服务”列表，用户需自行找到“Google Update”并开启",
      "user_action_requested": "在系统列表中点击“Google Update”并确认开启（此步需用户真实操作，无法被应用代劳）",
      "code_anchor": "com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo$c.openAccessibilityService"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.wjnjrmigikmpher.efaunxm.lqmgyyfk（exported Service，onStartCommand）",
      "trigger_event": "服务启动后进入 while(true)：Thread.sleep(1000) → 复查 enabled_accessibility_services → 未启用则再次 startActivity",
      "ui_carrier": "系统无障碍页（被反复重新压栈）",
      "shown_text_verbatim": "无（重复跳转系统设置页）",
      "shown_text_zh": "用户返回或拒绝后，每秒被重新拉回无障碍设置页，无法正常退出",
      "user_action_requested": "无有效“拒绝”路径；用户只能开启服务，或强杀进程/断网",
      "code_anchor": "com.wjnjrmigikmpher.efaunxm.lqmgyyfk.onStartCommand"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.wjnjrmigikmpher.efaunxm.hfstolkr（AccessibilityService，label=Google Update）",
      "trigger_event": "onServiceConnected 回调",
      "ui_carrier": "不可静态还原（后台无界面）",
      "shown_text_verbatim": "无（日志串：\"Blocked attempt to disable accessibility service[143523#]\"、\"AccessibilityClickButton\"、\"Start Accessibility\"）",
      "shown_text_zh": "无界面；服务进入 eventTypes=-1、flags=17 全量监听，具备读屏、模拟点击与阻止撤权能力",
      "user_action_requested": "无",
      "code_anchor": "com.wjnjrmigikmpher.efaunxm.hfstolkr.onServiceConnected / com.wjnjrmigikmpher.efaunxm.e.a"
    }
  ],
  "text_presentation_locations": [
    "ascvgkhzwyroo：全屏 WebView（setContentView(webView)）加载 DEX 内 Base64 硬编码 HTML，为引导文案的唯一呈现载体",
    "该 HTML 顶部标题 <h3>%Enable_Accessibility_Service%</h3>（占位符由 ascvgkhzwyroo.onCreate 从加密配置 a.aO 取模板后 replace 注入，并按系统语言替换文案）",
    "HTML 内 <div class=\"header\"> + id=accessability1（Accessibility Service）、id=downloadedservice（DOWNLOADED SERVICES）、id=switchaccess（Switch Access）、id='talkback'（TalkBack）、id='startaccessibility'（Start Accessibility）、id=off2/off3/off4（OFF）",
    "HTML 内 <div class=\"els\" onclick=\"Android.openAccessibilityService();\"> 与 <button onclick=\"Android.openAccessibilityService();\"> >> 两个可点区域，配 st01 缩放闪烁动画与内嵌 base64 箭头图",
    "HTML 内嵌 objLang 多语言字典（en/de/nl/zh-TW/cs/it/ja/ko 等），同一套伪造无障碍文案按 Locale 切换",
    "系统无障碍服务列表：Manifest android:label=\"Google Update\"，但 res/xml/tttannftd.xml 无 android:description，故系统页不呈现任何用途说明",
    "桌面图标名：AndroidManifest application android:label=\"Google Play\""
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "%Enable_Accessibility_Service%",
      "text_zh": "启用无障碍服务（模板占位符，运行期被替换为对应语言文案）",
      "source_location": "classes.dex 内嵌 HTML（ascvgkhzwyroo.onCreate 中 a.e(this.b.aO) 模板 + replace 注入）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service",
      "text_zh": "无障碍服务",
      "source_location": "内嵌 HTML id=accessability1（objLang['en']）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "DOWNLOADED SERVICES",
      "text_zh": "已下载的服务",
      "source_location": "内嵌 HTML id=downloadedservice（objLang['en']）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Switch Access",
      "text_zh": "开关访问（系统真实无障碍服务名，用作陪衬增强可信度）",
      "source_location": "内嵌 HTML id=switchaccess（objLang['en']）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "TalkBack",
      "text_zh": "TalkBack（系统读屏服务名，用作陪衬）",
      "source_location": "内嵌 HTML id='talkback'（objLang['en']）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Start Accessibility",
      "text_zh": "启动无障碍",
      "source_location": "内嵌 HTML id='startaccessibility'（<div class=\"an\"> 动画高亮行）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "OFF",
      "text_zh": "关闭",
      "source_location": "内嵌 HTML id=off2/off3/off4（objLang['en']）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on me to activate / Enable",
      "text_zh": "点我激活 / 启用",
      "source_location": "加密字符串常量（RC4+hex+Base64 还原，用于引导点击）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Blocked attempt to disable accessibility service[143523#]",
      "text_zh": "已阻止尝试关闭无障碍服务[143523#]",
      "source_location": "加密字符串常量（上报日志串，含家族标识 143523）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Update",
      "text_zh": "Google 更新",
      "source_location": "AndroidManifest.xml 无障碍服务 android:label",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "lqmgyyfk.onStartCommand 内 while(true)：每次 Thread.sleep(1000) 后复查 Settings.Secure.enabled_accessibility_services，未启用即再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)（FLAG_ACTIVITY_NEW_TASK|CLEAR_TOP|RESET_TASK_IF_NEEDED），用户从设置页返回会被立刻重新拉起，构成拒权死循环；另由 fgakwv.onCreate 设置 10000ms 周期 AlarmManager 广播自拉起，进程被杀后仍可重入。",
    "overlay_or_fake_settings": "不使用悬浮窗/透明遮罩（未申请 SYSTEM_ALERT_WINDOW，overlay 线索为空）；而是以全屏 WebView Activity 高仿系统无障碍设置页（同构标题、分组、TalkBack/Switch Access 条目、OFF 开关、闪烁箭头），点击后跳真实系统页。",
    "restricted_settings_13plus_coaching": "未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转与 Android 13+“允许受限设置”教学；仅见 e.a(Context)/a.a(Context,...) 以加密字符串构造 miui.intent.action.APP_PERM_EDITOR + com.miui.securitycenter.permissions.PermissionsEditorActivity（extra_pkgname）跳厂商权限编辑页。",
    "post_grant_anti_removal": "有：字符串表存在 \"Blocked attempt to disable accessibility service[143523#]\"，且 onAccessibilityEvent 内对事件文本做包含匹配后 performAction(16) 模拟点击；获权后 eventTypes=-1 全量监听窗口，具备识别并阻断用户在系统设置中关闭无障碍的自动化能力（防撤权路径已具备，具体触发条件因事件处理体庞大未逐行还原）。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以“监测到 startActivity(Intent android.settings.ACCESSIBILITY_SETTINGS)”为主钩子（同时命中 ascvgkhzwyroo$c.openAccessibilityService 与 lqmgyyfk.onStartCommand 两处）；辅以冷启动后首个 Activity 为 ascvgkhzwyroo（WebView 载入含 'Accessibility Service' 文本页）作为前置钩子，先抓伪造页、再抓系统页，可完整还原“伪造页→真系统页→循环重跳”三段。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动伪造系统无障碍设置页",
        "page_identifier": "Activity com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo 内的 WebView，页面含 'Accessibility Service'、'DOWNLOADED SERVICES'、'Start Accessibility'、'OFF'",
        "why_most_useful": "这是全部诱导文案的唯一载体，与真实系统页的同构程度是判定“假设置页诱导”的决定性证据",
        "observable_utg_signals": ["页面文本节点含 DOWNLOADED SERVICES + TalkBack + Switch Access（真实系统页不会以 WebView 承载）", "包名 com.wjnjrmigikmpher.efaunxm 的 Activity 承载无障碍设置版式", "存在闪烁/缩放动画箭头指向 OFF 开关"]
      },
      {
        "page_role": "跳转后的真实系统无障碍列表项",
        "page_identifier": "Settings 无障碍“已下载的服务”列表中条目 'Google Update'",
        "why_most_useful": "验证用户被引导的目标对象：服务名伪装 Google、且无任何用途描述文字",
        "observable_utg_signals": ["列表项文本为 'Google Update'", "该项无 summary/description 副标题", "归属包名 com.wjnjrmigikmpher.efaunxm 与 Google 无关联"]
      },
      {
        "page_role": "拒权返回后的循环重跳页（第2次+系统设置页）",
        "page_identifier": "1 秒后再次压栈的 android.settings.ACCESSIBILITY_SETTINGS",
        "why_most_useful": "证明存在强制引导/拒权循环，可与良性授权说明区分",
        "observable_utg_signals": ["按返回键后 ≤2s 内同一系统页再次成为前台 Activity", "重复次数与 1s 轮询节奏一致", "期间前台无本应用取消/跳过按钮"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "伪造页文本为 HTML 真实文本节点，UTG 可直接取；但页面标题 %Enable_Accessibility_Service% 由加密配置运行期注入，若网络配置未下发则标题可能为空，需靠固定文案（DOWNLOADED SERVICES/Start Accessibility）兜底识别。另：远端仅下发文字/指令，HTML 不在远端，故无远端 HTML 盲区；应用未使用悬浮窗遮罩，故无 overlay 类盲区；lqmgyyfk 循环受 Build.MANUFACTURER 判定约束，在非目标机型上不会触发，动态验证须选用对应厂商设备。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.wjnjrmigikmpher.efaunxm.fgakwv.onCreate",
    "com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo.onCreate",
    "com.wjnjrmigikmpher.efaunxm.ascvgkhzwyroo$c.openAccessibilityService",
    "com.wjnjrmigikmpher.efaunxm.lqmgyyfk.onStartCommand",
    "com.wjnjrmigikmpher.efaunxm.hfstolkr.onServiceConnected",
    "res/xml/tttannftd.xml"
  ]
}
```

</details>
