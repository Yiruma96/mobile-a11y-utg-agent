# MB_085__fe1be05225｜Ermac — HookAPP

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：157.7s

## 1. 一句话核心结论

- **核心申请方式**：冷启动后立即自隐藏图标并以系统级全屏 WebView 悬浮窗（内嵌 Base64 HTML，冒充 'Chrome Update Service'）覆盖桌面，用 JS 桥引导用户开启名为 HookAPPService 且伪造 isAccessibilityTool=true 的无障碍服务。
- **静态可见性说明**：Manifest、无障碍服务配置、引导逻辑骨架（tofa.s）与字符串资源均静态清晰可见；但真正的引导页面正文是以 Base64 分散内嵌在 classes.dex 字符串常量中的本地 HTML（仅解出 '<html lang="en">' 头部片段，正文不可完整还原），且打开无障碍设置的跳转由该 HTML 经 addJavascriptInterface 的 'Android' 桥在运行期发起，DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 字面量；JS 桥实现类 tofa$g 未取得反编译体。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fe1be052250f53b52017499744451c614e4771a392efa37afeb1b4774d861df0` |
| 包名 / 年份 | `com.dewoleyulucobazu.mowesi` / 2024 |
| 家族 / 品类 | **Ermac**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | HookAPP |
| 引导页宣称品牌/身份 | Chrome Update Service（假 Chrome 更新服务），另有 Facebook / Google Play / Gmail / WhatsApp / YouTube / Instagram / TikTok / Telegram / Contacts / Chrome 共 10 个 activity-alias 备用伪装身份 |
| 系统无障碍列表服务名 | HookAPPService |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用标签 HookAPP 但界面几乎空白（Theme.Translucent.NoTitleBar + TextView 内容仅一个空格），启动即 setComponentEnabledSetting 禁用自身入口并 finish；10 个 activity-alias 全部静态 enabled=false、带官方品牌图标，可在运行期按需启用冒充 Facebook/Google Play/Chrome/WhatsApp 等；无障碍配置伪造 android:isAccessibilityTool="true" 以规避系统'非无障碍工具'警告；包名与类名全部随机化且拆分为 com.dewoleyulucobazu.mowesi 与 com.cakohajozeza.zazi 两套混淆命名空间；说明文字用'先关闭再开启'的话术诱导重复授权。 |
| 无障碍服务类名 | `com.cakohajozeza.zazi.hojisukukuku.recosihani` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.dewoleyulucobazu.mowesi.gehezosajo（launcher Activity，theme=Theme.Translucent.NoTitleBar，noHistory、excludeFromRecents） | 用户点击桌面图标 → onCreate → 先 setComponentEnabledSetting(gehezosajo, DISABLED) 自隐藏 → 若 getApplicationLabel 为空则 r(this) 直接禁用组件，否则进入 v()/w() 主流程 | 原生Activity | **原文**：" "（setContentView(new TextView(this)); textView.setText(" ")）<br>**译注**：仅一个空格字符的空白页面，无任何说明或按钮 | 无可操作元素；界面随即消失或转交后台流程，用户无法取消或跳过 | `com.dewoleyulucobazu.mowesi.gehezosajo.onCreate / gehezosajo.r / gehezosajo.s` |
| 2 | 业务功能触发 | com.cakohajozeza.zazi.tofa（theme=@style/ACL，getWindow().setType(2006) 系统级窗口） | onCreate 中注册 WeakReference 并在 recosihani$b.P() 为假且无障碍未启用时 startService(recosihani)；onResume → s() 重新判定 | 原生Activity | 无 | 无 | `com.cakohajozeza.zazi.tofa.onCreate` |
| 3 | 引导说明页 | new WebView(this) 经 WindowManager.addView(webView, LayoutParams(-1,-1, type=2, flags=262144, format=-2)) 叠为全屏悬浮层 | tofa.s() 中 s1.a.a(context) 判定无障碍未开启且 this.z 为真 → 构造 WebView、setJavaScriptEnabled(true)、addJavascriptInterface(new tofa$g(this,this), "Android")、Base64.decode(G.a()) 后 f4.i.D0 替换占位符并 loadDataWithBaseURL | 悬浮窗Overlay | **原文**："Chrome Update Service"（%Enable_Accessibility_Service% 被替换值）；HTML 正文为 Base64 内嵌，仅解出 "<html lang=" 头部<br>**译注**：以“Chrome 更新服务”为名的页面覆盖整个桌面（正文文案因 Base64 分散存储未能静态还原） | 页面由本地 HTML 渲染并通过 JS 桥 "Android" 与原生交互，用户需按页面指引操作；无取消/跳过证据 | `com.cakohajozeza.zazi.tofa.s` |
| 4 | 跳无障碍设置 | 系统「设置 → 无障碍 → 已下载的服务」页面（经悬浮窗 HTML 按钮 + JavascriptInterface "Android" 触发） | 用户在悬浮页点击按钮 → tofa$g 桥方法回调原生（DEX 内无 ACTION_ACCESSIBILITY_SETTINGS 字面量，跳转参数由 HTML 侧决定，不可静态还原） | 不可静态还原 | **原文**：无（跳转动作来自 Base64 内嵌 HTML 的 JS 逻辑）<br>**译注**：用户在假 Chrome 更新页引导下进入系统无障碍设置，列表项显示 HookAPPService | 要求用户在系统无障碍列表中开启 HookAPPService | `com.cakohajozeza.zazi.tofa$g（JavascriptInterface "Android"）/ res/xml/hodixuni.xml` |
| 5 | 系统无障碍服务列表项 | 系统无障碍设置中 recosihani 服务条目（label=HookAPPService，description=@string/text_accessibility_service_description） | 用户点开条目时系统展示 android:description 文本 | 系统无障碍页 | **原文**：If accessibility permission has been on, please turn off then turn on.<br>**译注**：如果无障碍权限已经开启过，请先关闭再重新开启。 | 要求用户关闭再重新开启该服务（迫使服务重新绑定） | `res/values/strings.xml#text_accessibility_service_description / res/xml/hodixuni.xml` |
| 6 | 获权后动作 | com.cakohajozeza.zazi.hojisukukuku.recosihani（无障碍服务，BIND_ACCESSIBILITY_SERVICE） | 服务连接后进入 s1.a.a(context) 为真的分支，执行 s1.a.c(this) 等后续任务；同时 tofa 中提示 "need accessibility service" 的分支（androidx.activity.b#run）不再触发 | 系统无障碍页 | **原文**：need accessibility service<br>**译注**：需要无障碍服务（无障碍未启用时的提示） | 无（获权后转入静默自动化操作） | `com.cakohajozeza.zazi.tofa.s / androidx.activity.b#run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- launcher Activity gehezosajo：Theme.Translucent.NoTitleBar + TextView 内容为单个空格，界面近乎全空白，无任何说明文字
- WindowManager 全屏悬浮层中的 WebView（tofa.s）：本地 Base64 内嵌 HTML，占位符 %Enable_Accessibility_Service% 被替换为 "Chrome Update Service"，正文文案不可静态完整还原
- 系统无障碍服务列表：android:description = @string/text_accessibility_service_description（"If accessibility permission has been on, please turn off then turn on."）
- 系统无障碍服务列表：服务标签 label = "HookAPPService"
- 桌面图标名称：application android:label = "HookAPP"；10 个 activity-alias 分别显示 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram
- Toast 提示："need accessibility service"（无障碍未开启路径，androidx.activity.b#run）
- 无 assets 下的 HTML/JS 文件（assets 仅含 dexopt/baseline.prof*），引导页完全来自 DEX 内 Base64 常量

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome Update Service | Chrome 更新服务 | `com.cakohajozeza.zazi.tofa.s 中硬编码，替换内嵌 HTML 的 %Enable_Accessibility_Service% 占位符` | 假更新 |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开启过，请先关闭再重新开启。 | `res/values/strings.xml key=text_accessibility_service_description（被 res/xml/hodixuni.xml 引用）` | 教唆忽视警告 |
| en | need accessibility service | 需要无障碍服务 | `androidx.activity.b#run（Toast.makeText）` | 未知 |
| en | HookAPPService | HookAPP 服务（系统无障碍列表显示名） | `AndroidManifest.xml service com.cakohajozeza.zazi.hojisukukuku.recosihani android:label` | 未知 |
| en | HookAPP | HookAPP（桌面显示名） | `AndroidManifest.xml application android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：tofa.onResume 每次回到前台都重新执行 s()：若 s1.a.a(context)（无障碍未启用）仍为假且 this.z 为真，则重新构造 WebView 并 WindowManager.addView 全屏悬浮层，即从系统设置返回后引导页会再次弹出；叠加系统无障碍描述'先关闭再开启'的话术迫使服务重新绑定。具体重弹周期与是否带定时器未静态确认（HTML/JS 侧）。
- **遮罩叠层 / 高仿系统设置页**：是。WebView 以 WindowManager.LayoutParams(-1,-1, type=2, flags=262144(FLAG_NOT_FOCUSABLE), format=-2) 全屏叠加为系统级悬浮层，压在桌面/当前界面之上，内容为冒充的 'Chrome Update Service' 页面；未发现高仿系统无障碍开关页的原生布局。
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（targetSdkVersion=29，不涉及 Android 13 受限设置流程；相关教学文案若存在应位于未还原的 Base64 HTML 中）
- **获权后即时行为与防撤权机制**：无直接静态证据；但存在 device_admin receiver（com.cakohajozeza.zazi.wawufibayi.noxehahivuyo，label=HookAPPAdmin）与 BOOT_COMPLETED/PACKAGE_REMOVED/SCREEN_ON 等高优先级广播接收器（priority 999/994），具备获权后维持驻留与对抗撤权的组件基础
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 WindowManager.addView 被调用或 tofa.onResume 触发后约 800ms（此时全屏悬浮 WebView 已渲染首帧）；亦可直接以'冷启动后桌面之上出现无标题、无状态栏适配的全屏 WebView 层'为信号拉起 UTG
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：一是引导页正文为 DEX 内 Base64 分散存储的 HTML，静态不可读，只能运行期 UTG 抓取；二是打开设置的跳转由 JS 桥 'Android' 发起（tofa$g 未取得反编译体），DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 字面量，若设备处于 CIS 语言/地区（正则 [ua][ru][by][tj][uz][tm][az][am][kz][kg][md] 命中）或标签为空，应用会 setComponentEnabledSetting 禁用自身入口并 finish，此时冷启动无任何界面，需切换语言/地区后再触发。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后全屏悬浮引导页（假 Chrome Update Service）** | type=2006/2 的系统悬浮窗口内 WebView，页面标题/正文含 'Chrome Update Service'，无原生 ActionBar | 这是本样本唯一的诱导入口与全部引导文案载体，可直接读出'假更新'话术与按钮语义，是判定诱导而非良性说明的决定性证据 | WebView 节点文本中含 'Chrome Update Service'；页面存在单一主按钮且无取消/关闭控件；窗口层级为 TYPE_SYSTEM_ALERT / 悬浮层（非应用 Activity 内容） |
| **跳转后的系统无障碍服务列表项** | Settings 无障碍页中条目文本 'HookAPPService' 及其描述 'If accessibility permission has been on, please turn off then turn on.' | 验证引导落点确为无障碍授权，并记录服务名与'先关闭再开启'话术，用于与悬浮页话术对应 | 条目名称 'HookAPPService'；描述文本 'If accessibility permission has been on, please turn off then turn on.'；同页是否出现系统'此服务可查看屏幕内容'警告 |
| **从设置返回后的重弹悬浮层** | 返回桌面/应用后再次出现的同一 WebView 悬浮层 | 确认拒权反馈循环（onResume 重弹）是否成立，是判定强制性与非自愿授权的关键 | 同一悬浮层在用户返回后重复出现；重弹间隔与是否伴随 Toast 'need accessibility service'；界面是否提供任何退出路径 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.dewoleyulucobazu.mowesi.gehezosajo.onCreate`
- `com.dewoleyulucobazu.mowesi.gehezosajo.r`
- `com.cakohajozeza.zazi.tofa.s`
- `com.cakohajozeza.zazi.tofa.onCreate`
- `res/xml/hodixuni.xml`
- `res/values/strings.xml#text_accessibility_service_description`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，静态可见度：部分）

**已确认事实**

- **桌面身份伪装**：`application android:label="HookAPP"`，launcher 是 [gehezosajo](<resource-unit:#1.dex1 code:com.dewoleyulucobazu.mowesi.gehezosajo#onCreate>)，主题为 `Theme.Translucent.NoTitleBar` + `noHistory` + `excludeFromRecents`，`onCreate` 只 `setContentView(new TextView(" "))` 放一个空格文本——**用户点开图标看到的是近乎空白、随即消失的界面**。另有 10 个 `activity-alias`（Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram，各带官方图标 drawable，静态 `enabled="false"`），可运行期切换伪装身份。
- **无障碍服务与"官方工具"伪装**：[recosihani](<resource-unit:#1 manifest:components>)（`label="HookAPPService"`）配置 [hodixuni.xml](<resource-unit:#1 file:res/xml/hodixuni.xml>) 显式声明 `android:isAccessibilityTool="true"`，并申请 `canTakeScreenshot`、`canPerformGestures`、`typeAllMask`、`flagRequestFilterKeyEvents`、`flagRetrieveInteractiveWindows`、`canRetrieveWindowContent`——远超"Chrome 更新服务"所需。
- **真正的引导载体是"假 Chrome 更新"全屏悬浮窗**：`tofa.onCreate` 把窗口 `setType(2006)`（系统级 overlay 类型），`onResume→s()` 在检测到无障碍未开启时（`s1.a.a(context)` 为假）构造 `WebView`，开启 `setJavaScriptEnabled(true)`、`addJavascriptInterface(..., "Android")`，将 **Base64 内嵌 HTML** 解出后把占位符 `%Enable_Accessibility_Service%` 替换为 `"Chrome Update Service"`，再 `loadDataWithBaseURL(null, html, "text/html", ...)`，最后 `WindowManager.addView(webView, LayoutParams(-1,-1, 2, 262144, -2))`——**全屏不可聚焦的系统悬浮层压在桌面上**，内容以"Chrome 更新服务"名义呈现。
- **跳转无障碍设置由 HTML/JS 桥驱动**：DEX 中不存在 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 字面量（`search_function_callsites` 无命中），说明"打开设置页"动作来自悬浮窗 HTML 里的按钮经 `Android` JS 接口回调——该段 HTML 正文以 Base64 分散存放在 DEX 字符串常量中，`PGh0bWwgbGFuZz0i` 仅为头部片段，**正文文本无法静态完整还原**。
- **地域门控与自隐藏**：`j3.c.a()` 用正则 `[ua][ru][by][tj][uz][tm][az][am][kz][kg][md]` 匹配语言/地区，命中则 `j3.c.c()` 直接 `setComponentEnabledSetting(DISABLED)` 关闭自身入口并 `finish()`；`gehezosajo.r()` 同样在标签为空时禁用自身组件——**目标地域外不留入口**。
- **无障碍说明文字反向"教导"**：系统无障碍列表描述为 `"If accessibility permission has been on, please turn off then turn on."`（要求用户"先关闭再开启"），用于强制服务重新绑定。

**未决/边界**：悬浮窗 HTML 正文（具体按钮文案、是否含"受限设置"教学、拒权后是否死循环重弹）藏于 DEX 内 Base64 片段，未能静态还原；`Android` JS 桥方法体（`tofa$g`）未取得反编译结果。故 `static_visibility = partial_dynamic_or_remote`，运行期 UTG 应重点抓取悬浮窗首帧。

**UTG 抓取建议**：在 `WindowManager.addView` 触发后（冷启动 1–2 秒内、桌面之上出现无标题全屏层）立即截屏 + 抓取悬浮层视图树；关键页为"假 Chrome Update Service 全屏悬浮页"与随后的系统无障碍服务列表项（`HookAPPService`）。

> 说明：受本轮工具调用上限约束，未将风险台账（`record_risk`）落盘，仅登记了证据图 `EG-CF5DA6DB3478`。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍服务配置、引导逻辑骨架（tofa.s）与字符串资源均静态清晰可见；但真正的引导页面正文是以 Base64 分散内嵌在 classes.dex 字符串常量中的本地 HTML（仅解出 '<html lang=\"en\">' 头部片段，正文不可完整还原），且打开无障碍设置的跳转由该 HTML 经 addJavascriptInterface 的 'Android' 桥在运行期发起，DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 字面量；JS 桥实现类 tofa$g 未取得反编译体。",
  "summary_one_liner": "冷启动后立即自隐藏图标并以系统级全屏 WebView 悬浮窗（内嵌 Base64 HTML，冒充 'Chrome Update Service'）覆盖桌面，用 JS 桥引导用户开启名为 HookAPPService 且伪造 isAccessibilityTool=true 的无障碍服务。",
  "disguise_identity": {
    "app_display_name": "HookAPP",
    "claimed_brand_or_persona": "Chrome Update Service（假 Chrome 更新服务），另有 Facebook / Google Play / Gmail / WhatsApp / YouTube / Instagram / TikTok / Telegram / Contacts / Chrome 共 10 个 activity-alias 备用伪装身份",
    "a11y_service_label": "HookAPPService",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用标签 HookAPP 但界面几乎空白（Theme.Translucent.NoTitleBar + TextView 内容仅一个空格），启动即 setComponentEnabledSetting 禁用自身入口并 finish；10 个 activity-alias 全部静态 enabled=false、带官方品牌图标，可在运行期按需启用冒充 Facebook/Google Play/Chrome/WhatsApp 等；无障碍配置伪造 android:isAccessibilityTool=\"true\" 以规避系统'非无障碍工具'警告；包名与类名全部随机化且拆分为 com.dewoleyulucobazu.mowesi 与 com.cakohajozeza.zazi 两套混淆命名空间；说明文字用'先关闭再开启'的话术诱导重复授权。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.dewoleyulucobazu.mowesi.gehezosajo（launcher Activity，theme=Theme.Translucent.NoTitleBar，noHistory、excludeFromRecents）",
      "trigger_event": "用户点击桌面图标 → onCreate → 先 setComponentEnabledSetting(gehezosajo, DISABLED) 自隐藏 → 若 getApplicationLabel 为空则 r(this) 直接禁用组件，否则进入 v()/w() 主流程",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "\" \"（setContentView(new TextView(this)); textView.setText(\" \")）",
      "shown_text_zh": "仅一个空格字符的空白页面，无任何说明或按钮",
      "user_action_requested": "无可操作元素；界面随即消失或转交后台流程，用户无法取消或跳过",
      "code_anchor": "com.dewoleyulucobazu.mowesi.gehezosajo.onCreate / gehezosajo.r / gehezosajo.s"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.cakohajozeza.zazi.tofa（theme=@style/ACL，getWindow().setType(2006) 系统级窗口）",
      "trigger_event": "onCreate 中注册 WeakReference 并在 recosihani$b.P() 为假且无障碍未启用时 startService(recosihani)；onResume → s() 重新判定",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见文案，仅完成窗口类型与状态初始化",
      "user_action_requested": "无",
      "code_anchor": "com.cakohajozeza.zazi.tofa.onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "new WebView(this) 经 WindowManager.addView(webView, LayoutParams(-1,-1, type=2, flags=262144, format=-2)) 叠为全屏悬浮层",
      "trigger_event": "tofa.s() 中 s1.a.a(context) 判定无障碍未开启且 this.z 为真 → 构造 WebView、setJavaScriptEnabled(true)、addJavascriptInterface(new tofa$g(this,this), \"Android\")、Base64.decode(G.a()) 后 f4.i.D0 替换占位符并 loadDataWithBaseURL",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "\"Chrome Update Service\"（%Enable_Accessibility_Service% 被替换值）；HTML 正文为 Base64 内嵌，仅解出 \"<html lang=\" 头部",
      "shown_text_zh": "以“Chrome 更新服务”为名的页面覆盖整个桌面（正文文案因 Base64 分散存储未能静态还原）",
      "user_action_requested": "页面由本地 HTML 渲染并通过 JS 桥 \"Android\" 与原生交互，用户需按页面指引操作；无取消/跳过证据",
      "code_anchor": "com.cakohajozeza.zazi.tofa.s"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍 → 已下载的服务」页面（经悬浮窗 HTML 按钮 + JavascriptInterface \"Android\" 触发）",
      "trigger_event": "用户在悬浮页点击按钮 → tofa$g 桥方法回调原生（DEX 内无 ACTION_ACCESSIBILITY_SETTINGS 字面量，跳转参数由 HTML 侧决定，不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（跳转动作来自 Base64 内嵌 HTML 的 JS 逻辑）",
      "shown_text_zh": "用户在假 Chrome 更新页引导下进入系统无障碍设置，列表项显示 HookAPPService",
      "user_action_requested": "要求用户在系统无障碍列表中开启 HookAPPService",
      "code_anchor": "com.cakohajozeza.zazi.tofa$g（JavascriptInterface \"Android\"）/ res/xml/hodixuni.xml"
    },
    {
      "step": 5,
      "stage": "系统无障碍服务列表项",
      "screen_or_component": "系统无障碍设置中 recosihani 服务条目（label=HookAPPService，description=@string/text_accessibility_service_description）",
      "trigger_event": "用户点开条目时系统展示 android:description 文本",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "shown_text_zh": "如果无障碍权限已经开启过，请先关闭再重新开启。",
      "user_action_requested": "要求用户关闭再重新开启该服务（迫使服务重新绑定）",
      "code_anchor": "res/values/strings.xml#text_accessibility_service_description / res/xml/hodixuni.xml"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.cakohajozeza.zazi.hojisukukuku.recosihani（无障碍服务，BIND_ACCESSIBILITY_SERVICE）",
      "trigger_event": "服务连接后进入 s1.a.a(context) 为真的分支，执行 s1.a.c(this) 等后续任务；同时 tofa 中提示 \"need accessibility service\" 的分支（androidx.activity.b#run）不再触发",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "need accessibility service",
      "shown_text_zh": "需要无障碍服务（无障碍未启用时的提示）",
      "user_action_requested": "无（获权后转入静默自动化操作）",
      "code_anchor": "com.cakohajozeza.zazi.tofa.s / androidx.activity.b#run"
    }
  ],
  "text_presentation_locations": [
    "launcher Activity gehezosajo：Theme.Translucent.NoTitleBar + TextView 内容为单个空格，界面近乎全空白，无任何说明文字",
    "WindowManager 全屏悬浮层中的 WebView（tofa.s）：本地 Base64 内嵌 HTML，占位符 %Enable_Accessibility_Service% 被替换为 \"Chrome Update Service\"，正文文案不可静态完整还原",
    "系统无障碍服务列表：android:description = @string/text_accessibility_service_description（\"If accessibility permission has been on, please turn off then turn on.\"）",
    "系统无障碍服务列表：服务标签 label = \"HookAPPService\"",
    "桌面图标名称：application android:label = \"HookAPP\"；10 个 activity-alias 分别显示 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram",
    "Toast 提示：\"need accessibility service\"（无障碍未开启路径，androidx.activity.b#run）",
    "无 assets 下的 HTML/JS 文件（assets 仅含 dexopt/baseline.prof*），引导页完全来自 DEX 内 Base64 常量"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome Update Service",
      "text_zh": "Chrome 更新服务",
      "source_location": "com.cakohajozeza.zazi.tofa.s 中硬编码，替换内嵌 HTML 的 %Enable_Accessibility_Service% 占位符",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开启过，请先关闭再重新开启。",
      "source_location": "res/values/strings.xml key=text_accessibility_service_description（被 res/xml/hodixuni.xml 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "need accessibility service",
      "text_zh": "需要无障碍服务",
      "source_location": "androidx.activity.b#run（Toast.makeText）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "HookAPPService",
      "text_zh": "HookAPP 服务（系统无障碍列表显示名）",
      "source_location": "AndroidManifest.xml service com.cakohajozeza.zazi.hojisukukuku.recosihani android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "HookAPP",
      "text_zh": "HookAPP（桌面显示名）",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "tofa.onResume 每次回到前台都重新执行 s()：若 s1.a.a(context)（无障碍未启用）仍为假且 this.z 为真，则重新构造 WebView 并 WindowManager.addView 全屏悬浮层，即从系统设置返回后引导页会再次弹出；叠加系统无障碍描述'先关闭再开启'的话术迫使服务重新绑定。具体重弹周期与是否带定时器未静态确认（HTML/JS 侧）。",
    "overlay_or_fake_settings": "是。WebView 以 WindowManager.LayoutParams(-1,-1, type=2, flags=262144(FLAG_NOT_FOCUSABLE), format=-2) 全屏叠加为系统级悬浮层，压在桌面/当前界面之上，内容为冒充的 'Chrome Update Service' 页面；未发现高仿系统无障碍开关页的原生布局。",
    "restricted_settings_13plus_coaching": "无静态证据（targetSdkVersion=29，不涉及 Android 13 受限设置流程；相关教学文案若存在应位于未还原的 Base64 HTML 中）",
    "post_grant_anti_removal": "无直接静态证据；但存在 device_admin receiver（com.cakohajozeza.zazi.wawufibayi.noxehahivuyo，label=HookAPPAdmin）与 BOOT_COMPLETED/PACKAGE_REMOVED/SCREEN_ON 等高优先级广播接收器（priority 999/994），具备获权后维持驻留与对抗撤权的组件基础",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 WindowManager.addView 被调用或 tofa.onResume 触发后约 800ms（此时全屏悬浮 WebView 已渲染首帧）；亦可直接以'冷启动后桌面之上出现无标题、无状态栏适配的全屏 WebView 层'为信号拉起 UTG",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后全屏悬浮引导页（假 Chrome Update Service）",
        "page_identifier": "type=2006/2 的系统悬浮窗口内 WebView，页面标题/正文含 'Chrome Update Service'，无原生 ActionBar",
        "why_most_useful": "这是本样本唯一的诱导入口与全部引导文案载体，可直接读出'假更新'话术与按钮语义，是判定诱导而非良性说明的决定性证据",
        "observable_utg_signals": [
          "WebView 节点文本中含 'Chrome Update Service'",
          "页面存在单一主按钮且无取消/关闭控件",
          "窗口层级为 TYPE_SYSTEM_ALERT / 悬浮层（非应用 Activity 内容）"
        ]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中条目文本 'HookAPPService' 及其描述 'If accessibility permission has been on, please turn off then turn on.'",
        "why_most_useful": "验证引导落点确为无障碍授权，并记录服务名与'先关闭再开启'话术，用于与悬浮页话术对应",
        "observable_utg_signals": [
          "条目名称 'HookAPPService'",
          "描述文本 'If accessibility permission has been on, please turn off then turn on.'",
          "同页是否出现系统'此服务可查看屏幕内容'警告"
        ]
      },
      {
        "page_role": "从设置返回后的重弹悬浮层",
        "page_identifier": "返回桌面/应用后再次出现的同一 WebView 悬浮层",
        "why_most_useful": "确认拒权反馈循环（onResume 重弹）是否成立，是判定强制性与非自愿授权的关键",
        "observable_utg_signals": [
          "同一悬浮层在用户返回后重复出现",
          "重弹间隔与是否伴随 Toast 'need accessibility service'",
          "界面是否提供任何退出路径"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：一是引导页正文为 DEX 内 Base64 分散存储的 HTML，静态不可读，只能运行期 UTG 抓取；二是打开设置的跳转由 JS 桥 'Android' 发起（tofa$g 未取得反编译体），DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 字面量，若设备处于 CIS 语言/地区（正则 [ua][ru][by][tj][uz][tm][az][am][kz][kg][md] 命中）或标签为空，应用会 setComponentEnabledSetting 禁用自身入口并 finish，此时冷启动无任何界面，需切换语言/地区后再触发。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL"
  ],
  "code_anchors": [
    "com.dewoleyulucobazu.mowesi.gehezosajo.onCreate",
    "com.dewoleyulucobazu.mowesi.gehezosajo.r",
    "com.cakohajozeza.zazi.tofa.s",
    "com.cakohajozeza.zazi.tofa.onCreate",
    "res/xml/hodixuni.xml",
    "res/values/strings.xml#text_accessibility_service_description"
  ]
}
```

</details>
