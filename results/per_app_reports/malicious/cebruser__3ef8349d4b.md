# MR_035__3ef8349d4b｜cebruser — GTA V

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：141.3s

## 1. 一句话核心结论

- **核心申请方式**：以「GTA V」为名、无障碍服务伪装成「Google update」，冷启动检测未启用即拉起内嵌高仿系统无障碍界面（40+语言）的 WebView 引导页，按钮经 JS 桥直跳系统无障碍设置，并由后台服务每 1 秒无限重跳、无任何取消路径。
- **静态可见性说明**：未加壳、无 VMP、无远端 HTML。DEX 字符串采用自研双重编码（前12字符作 RC4 key + 剩余部分 Base64 后按 hex 转字节再 RC4），已脚本全量还原 471 条明文；引导页与仿 Gmail 页均为 DEX 内嵌 Base64 HTML，静态完整可见。仅有后台 C2 配置值（aJ 多语言 JSON、aO 页面模板）与远程指令语义需运行期确认，但不影响无障碍诱导链路的判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3ef8349d4b717d73d31366dfbe941470e749222331edd0b9484955a212080ad8` |
| 包名 / 年份 | `com.sakkkwyl.ncceberwpdhfq` / 2020 |
| 家族 / 品类 | **cebruser**（同池样本数：3） |
| 原始来源标识 | https://gbhackers.com/hackers-breached-mdm-servers-to-install-android-malware/ |
| 桌面显示名 | GTA V |
| 引导页宣称品牌/身份 | Google（服务名伪装为系统更新组件「Google update」，引导页复刻系统无障碍服务列表界面） |
| 系统无障碍列表服务名 | Google update |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签「Google update」与真实功能无关；android:description 为空，系统无障碍列表不显示任何用途说明；引导页为多语言高仿系统无障碍界面（含 TalkBack / Switch Access / DOWNLOADED SERVICES / OFF 等伪系统条目）；包内另有仿 Gmail 登录页用于凭证窃取；无障碍服务类名、Activity 名全部随机化（msusephjqx、lluiztetabeombd 等）；多处 Activity 使用 android:label="" 且 excludeFromRecents 隐藏于最近任务；未伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.sakkkwyl.ncceberwpdhfq.msusephjqx` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sakkkwyl.ncceberwpdhfq.iexuymsx（LAUNCHER + android.app.role.SMS 入口 Activity） | 用户点击桌面图标启动，onCreate 回调 | 原生Activity | 无 | 仅需启动应用，无需任何操作 | `com.sakkkwyl.ncceberwpdhfq.iexuymsx.onCreate` |
| 2 | 业务功能触发 | com.sakkkwyl.ncceberwpdhfq.e.b(Context, Class) 读取 Settings.Secure.enabled_accessibility_services | onCreate 中调用 e.b(this, msusephjqx.class) 判断无障碍服务是否已启用 | 不可静态还原 | 无 | 无（未启用则进入下一步；已启用则 f.a(this) 直接执行无障碍业务） | `com.sakkkwyl.ncceberwpdhfq.e.b(Context, Class)` |
| 3 | 引导说明页 | com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd（WebView Activity，Manifest 主题 Theme.Translucent.NoTitleBar） | 未启用无障碍时 startActivity(new Intent(this, lluiztetabeombd.class)) | 本地HTML WebView | **原文**：%Enable_Accessibility_Service%   Start Accessibility >>   （页面 JS 内置多语言表：'en':{'accessability1':'Accessibility Service','downloadedservice':'DOWNLOADED SERVICES','switchaccess':'Switch Access','talkback':'TalkBack','off':'OFF'} / 'zh':{'accessability1':'無障礙服務','downloadedservice':'下載的服務','switchaccess':'開關訪問','talkback':'頂嘴','off':'關'}）<br>**译注**：「无障碍服务」标题 +「开始无障碍 >>」按钮，并铺排「已下载的服务 / Switch Access / TalkBack / 关」等仿系统条目 | 点击页面按钮「Start Accessibility >>」；页面无取消、跳过或关闭按钮（HTML 仅两个 onclick 元素，均绑定 openAccessibilityService） | `com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd.onCreate + 内嵌 Base64 HTML 的 onclick="Android.openAccessibilityService();"` |
| 4 | 跳无障碍设置 | @JavascriptInterface 桥 com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd$c#openAccessibilityService | WebView 中用户点击按钮触发 JS 调用 Android.openAccessibilityService() | 系统无障碍页 | 无 | 在系统无障碍列表中手动找到并开启名为「Google update」的服务（列表项无 description 说明） | `com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd$c.openAccessibilityService` |
| 5 | 拒权反馈循环 | com.sakkkwyl.ncceberwpdhfq.trwsdjimslf（exported=true 的后台 Service） | onStartCommand 中 while(true)：e.b(this, msusephjqx.class) 为假或配置项 e(this, c.ab) != 期望值时，e.a(1000) 睡眠 1 秒后再次 startActivity(ACCESSIBILITY_SETTINGS) | 系统无障碍页 | **原文**：无（仅反复拉起系统设置页，叠加 FLAG_ACTIVITY_NEW_TASK\|CLEAR_TOP\|RESET_TASK_IF_NEEDED = 268435456\|536870912\|1073741824）<br>**译注**：用户返回或拒绝授权后，1 秒内被强制重新拉回无障碍设置页，循环无出口 | 除开启服务外无任何可退出路径；返回键无效（无取消分支、无退出条件） | `com.sakkkwyl.ncceberwpdhfq.trwsdjimslf.onStartCommand` |
| 6 | 获权后动作 | com.sakkkwyl.ncceberwpdhfq.msusephjqx（AccessibilityService，canRetrieveWindowContent=true）+ 内嵌仿 Gmail 登录页 HTML | onAccessibilityEvent 接收 typeWindowContentChanged\|typeWindowStateChanged 后 f.a(this) 进入业务；另含 lgvm$c.send_log_injects 回传登录表单 | 不可静态还原 | **原文**：grabbing_pass_gmail / grabbing_lockpattern / Lock Pattern: / Blocked attempt to disable accessibility service[143523#] / 'en':'Click on me to activate' / 'en':'Open More downloaded services > '<br>**译注**：抓取 Gmail 密码、抓取锁屏图案；监听并阻断用户关闭无障碍服务的尝试；在系统界面注入「点我激活」「打开更多已下载的服务」提示引导继续授权 | 无（后台静默执行；仅在被引导时按注入文案继续点击） | `com.sakkkwyl.ncceberwpdhfq.msusephjqx.onAccessibilityEvent / com.sakkkwyl.ncceberwpdhfq.f.a` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- lluiztetabeombd：全屏 WebView（Theme.Translucent.NoTitleBar）加载 DEX 内嵌 Base64 HTML，显示「Enable_Accessibility_Service」标题与「Start Accessibility >>」按钮及仿系统无障碍条目（Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF，40+ 语言）
- 该 WebView 页面无任何取消/跳过/关闭控件，两个可点击元素均为 onclick="Android.openAccessibilityService();"
- 系统无障碍服务列表项：android:label="Google update"，android:description 未配置（列表内无任何用途说明文字）
- 无障碍服务运行时向其他应用界面注入的文案：'Click on me to activate'（点我激活）、'Open More downloaded services > '（打开更多已下载的服务 >）
- 另存在独立的仿 Gmail 登录页内嵌 HTML（Welcome %gmail_to_device% / Forgot password? / Next），用于输入邮箱密码，非无障碍引导文字
- 未发现悬浮窗 Overlay 引导、未发现本地 HTML 文件（assets/ 下无页面）、未发现远端 URL 教学页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable_Accessibility_Service% | 启用无障碍服务（模板占位符，运行期由配置替换） | `classes.dex 内嵌 Base64 HTML（lluiztetabeombd WebView 页面正文）` | 受限设置分步教学 |
| en | Start Accessibility >> | 开始无障碍 >> | `classes.dex 内嵌 Base64 HTML 按钮文案` | 受限设置分步教学 |
| en | 'en': { 'accessability1':'Accessibility Service', 'downloadedservice':'DOWNLOADED SERVICES', 'switchaccess':'Switch Access', 'talkback':'TalkBack', 'off':'OFF' } | 「无障碍服务」「已下载的服务」「切换访问」「TalkBack」「关闭」——用于仿冒系统无障碍界面 | `classes.dex 内嵌 Base64 HTML 的 objLang 多语言表` | 未知 |
| zh | 'zh': { 'accessability1':'無障礙服務', 'downloadedservice':'下載的服務', 'switchaccess':'開關訪問', 'talkback':'頂嘴', 'off':'關' } | 「无障碍服务」「下载的服务」「开关访问」「顶嘴（TalkBack 误译）」「关」 | `classes.dex 内嵌 Base64 HTML 的 objLang 多语言表（zh 项）` | 未知 |
| en | Click on me to activate | 点我来激活 | `classes.dex 解密字符串（'en' 多语言表）` | 受限设置分步教学 |
| en | Open More downloaded services > | 打开「更多已下载的服务 >」 | `classes.dex 解密字符串（'en' 多语言表，40+ 语言同款）` | 受限设置分步教学 |
| en | Blocked attempt to disable accessibility service[143523#] | 已拦截关闭无障碍服务的尝试 | `classes.dex 解密字符串` | 教唆忽视警告 |
| en | Google update | Google 更新 | `AndroidManifest.xml 无障碍服务 android:label` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：trwsdjimslf.onStartCommand 以 while(true) 循环：只要 Settings.Secure.enabled_accessibility_services 未包含自身组件，或配置项 e(this, c.ab) 不等于期望值，就 e.a(1000) 睡眠 1 秒后重新 startActivity("android.settings.ACCESSIBILITY_SETTINGS")（带 NEW_TASK|CLEAR_TOP|RESET_TASK_IF_NEEDED），用户返回或拒绝授权即被立刻重新拉回系统设置页，循环无退出条件；另有无障碍服务在界面注入「Click on me to activate」引导继续点击。
- **遮罩叠层 / 高仿系统设置页**：未使用 SYSTEM_ALERT_WINDOW 悬浮窗遮罩；但引导页 WebView 自身即高仿系统无障碍设置界面（多语言复刻 Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF 条目与开关视觉），配合 Theme.Translucent.NoTitleBar 全屏呈现，可误认为系统原生页面。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=29，未发现跳转 ACTION_APPLICATION_DETAILS_SETTINGS、未发现「允许受限设置」或 Session 安装器绕过教学。
- **获权后即时行为与防撤权机制**：有。解密字符串含「Blocked attempt to disable accessibility service[143523#]」与 time_run_bypass_protect，无障碍服务持续监听 typeWindowStateChanged 并在用户进入系统无障碍页撤权时执行阻断（静态预筛亦命中 PERFORM_GLOBAL_ACTION）；trwsdjimslf 同时持续重跳设置页施压。
- **良性降级 / 替代方案**：无。除开启无障碍服务外不存在任何替代路径、手动模式或降级提示。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：Hook 监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（lluiztetabeombd$c.openAccessibilityService 与 trwsdjimslf.onStartCommand 两处），或冷启动后 lluiztetabeombd 的 WebView 加载完成（loadDataWithBaseURL 返回）瞬间拉起 UTG 截图；前者可同时捕获循环重跳行为。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区在于：引导页 HTML 与全部字符串在 DEX 内以自研编码（RC4 key+Base64+hex）存放，纯 strings/静态资源扫描（assets、res/layout、strings.xml）完全取不到任何引导文案，需先解密 DEX 字符串；WebView 页面无本地 HTML 文件，UTG 必须依赖运行期截图而非资源文件比对。此外入口 iexuymsx 在非目标厂商分支会直接 finish() 且不展示任何界面，冷启动可能瞬时不出现可见页面，需按厂商/版本条件重试触发。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页（高仿系统无障碍界面 WebView）** | Activity com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd，全屏无标题栏 WebView，页面标题区含「Enable_Accessibility_Service」与「Start Accessibility >>」按钮，下方仿系统条目「DOWNLOADED SERVICES / Switch Access / TalkBack / OFF」 | 这是应用唯一的授权说理界面，直接暴露其复刻系统无障碍 UI、无任何用途说明与取消入口的诱导本质，且与 GTA V 名称毫无关联 | Activity 类名 lluiztetabeombd 且为 WebView 容器；页面文本含 Accessibility Service / DOWNLOADED SERVICES / TalkBack / OFF 等系统无障碍专有词；页面无任何「取消 / 跳过 / 关闭 / 稍后」控件，仅有 Start Accessibility 按钮；文本语言随系统语言切换（内置 40+ 语言表） |
| **系统无障碍服务列表项（跳转落地页）** | android.settings.ACCESSIBILITY_SETTINGS，列表中出现 label 为「Google update」的条目，无描述副标题 | 验证伪装服务名已实际注册进系统列表，且与桌面应用名 GTA V 明显不一致，是身份混淆的直接运行期证据 | 条目文本「Google update」；条目下方无任何 description 说明文字；应用包名 com.sakkkwyl.ncceberwpdhfq 与 label 不匹配 |
| **拒权后循环重跳压栈页** | 用户从 ACCESSIBILITY_SETTINGS 返回后 ≤1.5 秒内再次出现同一系统无障碍设置页 | 证明存在无出口的强制循环，是区别于良性引导的关键行为特征 | 同一 Activity（系统无障碍设置）在短时间内被重复压栈/重复出现；返回动作无法停留在桌面或上一应用；日志中出现 trwsdjimslf.onStartCommand 的周期性 startActivity |
| **获权后无障碍服务注入的引导文案** | 当前应用界面上出现的注入浮层文本「Click on me to activate」或「Open More downloaded services > 」 | 证明服务获权后继续操控界面、以无障碍能力驱动进一步授权/操作，而非提供无障碍功能 | 非目标应用原生 UI 的文本「Click on me to activate」；「Open More downloaded services >」提示与系统设置页文案混排 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.sakkkwyl.ncceberwpdhfq.iexuymsx.onCreate`
- `com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd.onCreate`
- `com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd$c.openAccessibilityService`
- `com.sakkkwyl.ncceberwpdhfq.trwsdjimslf.onStartCommand`
- `com.sakkkwyl.ncceberwpdhfq.e.b(Context, Class)`
- `res/xml/shreix.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**核心机制已完整静态还原（未加壳，DEX 字符串用“12 字符 RC4 key + Base64(hex)”自研双重编码，已脚本解密 471 条；引导页为 DEX 内嵌 Base64 HTML）。**

- **伪装身份**：桌面名 `GTA V`，无障碍服务标签 `Google update`，与游戏无关；`res/xml/shreix.xml` 声明 `canRetrieveWindowContent="true"` + `typeWindowContentChanged|typeWindowStateChanged`，可读取任意界面内容；`android:description` 为空（系统列表无任何说明）。
- **冷启动链路**：启动器 `iexuymsx.onCreate` 先读 `Settings.Secure.enabled_accessibility_services` 自检 → 未启用则启动 `lluiztetabeombd` 引导 Activity（Manifest 主题为 `Theme.Translucent.NoTitleBar`）→ 该 Activity 建 WebView + `addJavascriptInterface("Android")` → 加载内嵌 HTML 引导页。
- **引导页本质是“高仿系统无障碍界面”**：HTML 内置 40+ 语言文案（`accessability1/downloadedservice/switchaccess/talkback/off`，zh 为“無障礙服務/下載的服務/開關訪問/頂嘴/關”），页面主按钮文案 `Enable_Accessibility_Service` / `Start Accessibility >>`，`onclick="Android.openAccessibilityService();"` → JS 桥直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。
- **拒权循环**：导出的 `trwsdjimslf.onStartCommand` 在 `while(true)` 中：未启用则 `e.a(1000)` 睡 1 秒再跳 `ACCESSIBILITY_SETTINGS`（带 `NEW_TASK|CLEAR_TOP` 等 flag），**无取消、无跳过、无退出条件**。
- **无 13+ 受限设置教学**：`targetSdkVersion=29`，不存在应用详情页“允许受限设置”分步教学或 Session 安装器绕过；亦未发现 `APPLICATION_DETAILS_SETTINGS` 跳转。
- **获权后用途（旁证）**：包内另有仿 Gmail 登录页 HTML，JS 桥 `Android.send_log_injects` 回传表单 JSON；解密串含 `grabbing_pass_gmail`、`grabbing_lockpattern`、`Lock Pattern:`、`Blocked attempt to disable accessibility service[143523#]`、`time_run_bypass_protect` —— 表明授权后用于凭证/锁屏图案窃取并阻止撤权。
- **第三方 SDK 无关**：全部引导与跳转逻辑均在应用自身 33 个类内，非 SDK 行为。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "未加壳、无 VMP、无远端 HTML。DEX 字符串采用自研双重编码（前12字符作 RC4 key + 剩余部分 Base64 后按 hex 转字节再 RC4），已脚本全量还原 471 条明文；引导页与仿 Gmail 页均为 DEX 内嵌 Base64 HTML，静态完整可见。仅有后台 C2 配置值（aJ 多语言 JSON、aO 页面模板）与远程指令语义需运行期确认，但不影响无障碍诱导链路的判定。",
  "summary_one_liner": "以「GTA V」为名、无障碍服务伪装成「Google update」，冷启动检测未启用即拉起内嵌高仿系统无障碍界面（40+语言）的 WebView 引导页，按钮经 JS 桥直跳系统无障碍设置，并由后台服务每 1 秒无限重跳、无任何取消路径。",
  "disguise_identity": {
    "app_display_name": "GTA V",
    "claimed_brand_or_persona": "Google（服务名伪装为系统更新组件「Google update」，引导页复刻系统无障碍服务列表界面）",
    "a11y_service_label": "Google update",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签「Google update」与真实功能无关；android:description 为空，系统无障碍列表不显示任何用途说明；引导页为多语言高仿系统无障碍界面（含 TalkBack / Switch Access / DOWNLOADED SERVICES / OFF 等伪系统条目）；包内另有仿 Gmail 登录页用于凭证窃取；无障碍服务类名、Activity 名全部随机化（msusephjqx、lluiztetabeombd 等）；多处 Activity 使用 android:label=\"\" 且 excludeFromRecents 隐藏于最近任务；未伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sakkkwyl.ncceberwpdhfq.iexuymsx（LAUNCHER + android.app.role.SMS 入口 Activity）",
      "trigger_event": "用户点击桌面图标启动，onCreate 回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见界面：onCreate 中完成设备信息采集后按厂商/版本分支 finish() 或转引导",
      "user_action_requested": "仅需启动应用，无需任何操作",
      "code_anchor": "com.sakkkwyl.ncceberwpdhfq.iexuymsx.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.sakkkwyl.ncceberwpdhfq.e.b(Context, Class) 读取 Settings.Secure.enabled_accessibility_services",
      "trigger_event": "onCreate 中调用 e.b(this, msusephjqx.class) 判断无障碍服务是否已启用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静默自检：解析 enabled_accessibility_services 冒号分隔列表比对自身组件",
      "user_action_requested": "无（未启用则进入下一步；已启用则 f.a(this) 直接执行无障碍业务）",
      "code_anchor": "com.sakkkwyl.ncceberwpdhfq.e.b(Context, Class)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd（WebView Activity，Manifest 主题 Theme.Translucent.NoTitleBar）",
      "trigger_event": "未启用无障碍时 startActivity(new Intent(this, lluiztetabeombd.class))",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "%Enable_Accessibility_Service%   Start Accessibility >>   （页面 JS 内置多语言表：'en':{'accessability1':'Accessibility Service','downloadedservice':'DOWNLOADED SERVICES','switchaccess':'Switch Access','talkback':'TalkBack','off':'OFF'} / 'zh':{'accessability1':'無障礙服務','downloadedservice':'下載的服務','switchaccess':'開關訪問','talkback':'頂嘴','off':'關'}）",
      "shown_text_zh": "「无障碍服务」标题 +「开始无障碍 >>」按钮，并铺排「已下载的服务 / Switch Access / TalkBack / 关」等仿系统条目",
      "user_action_requested": "点击页面按钮「Start Accessibility >>」；页面无取消、跳过或关闭按钮（HTML 仅两个 onclick 元素，均绑定 openAccessibilityService）",
      "code_anchor": "com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd.onCreate + 内嵌 Base64 HTML 的 onclick=\"Android.openAccessibilityService();\""
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "@JavascriptInterface 桥 com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd$c#openAccessibilityService",
      "trigger_event": "WebView 中用户点击按钮触发 JS 调用 Android.openAccessibilityService()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))，无任何参数引导或高亮",
      "user_action_requested": "在系统无障碍列表中手动找到并开启名为「Google update」的服务（列表项无 description 说明）",
      "code_anchor": "com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd$c.openAccessibilityService"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.sakkkwyl.ncceberwpdhfq.trwsdjimslf（exported=true 的后台 Service）",
      "trigger_event": "onStartCommand 中 while(true)：e.b(this, msusephjqx.class) 为假或配置项 e(this, c.ab) != 期望值时，e.a(1000) 睡眠 1 秒后再次 startActivity(ACCESSIBILITY_SETTINGS)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（仅反复拉起系统设置页，叠加 FLAG_ACTIVITY_NEW_TASK|CLEAR_TOP|RESET_TASK_IF_NEEDED = 268435456|536870912|1073741824）",
      "shown_text_zh": "用户返回或拒绝授权后，1 秒内被强制重新拉回无障碍设置页，循环无出口",
      "user_action_requested": "除开启服务外无任何可退出路径；返回键无效（无取消分支、无退出条件）",
      "code_anchor": "com.sakkkwyl.ncceberwpdhfq.trwsdjimslf.onStartCommand"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.sakkkwyl.ncceberwpdhfq.msusephjqx（AccessibilityService，canRetrieveWindowContent=true）+ 内嵌仿 Gmail 登录页 HTML",
      "trigger_event": "onAccessibilityEvent 接收 typeWindowContentChanged|typeWindowStateChanged 后 f.a(this) 进入业务；另含 lgvm$c.send_log_injects 回传登录表单",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "grabbing_pass_gmail / grabbing_lockpattern / Lock Pattern: / Blocked attempt to disable accessibility service[143523#] / 'en':'Click on me to activate' / 'en':'Open More downloaded services > '",
      "shown_text_zh": "抓取 Gmail 密码、抓取锁屏图案；监听并阻断用户关闭无障碍服务的尝试；在系统界面注入「点我激活」「打开更多已下载的服务」提示引导继续授权",
      "user_action_requested": "无（后台静默执行；仅在被引导时按注入文案继续点击）",
      "code_anchor": "com.sakkkwyl.ncceberwpdhfq.msusephjqx.onAccessibilityEvent / com.sakkkwyl.ncceberwpdhfq.f.a"
    }
  ],
  "text_presentation_locations": [
    "lluiztetabeombd：全屏 WebView（Theme.Translucent.NoTitleBar）加载 DEX 内嵌 Base64 HTML，显示「Enable_Accessibility_Service」标题与「Start Accessibility >>」按钮及仿系统无障碍条目（Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF，40+ 语言）",
    "该 WebView 页面无任何取消/跳过/关闭控件，两个可点击元素均为 onclick=\"Android.openAccessibilityService();\"",
    "系统无障碍服务列表项：android:label=\"Google update\"，android:description 未配置（列表内无任何用途说明文字）",
    "无障碍服务运行时向其他应用界面注入的文案：'Click on me to activate'（点我激活）、'Open More downloaded services > '（打开更多已下载的服务 >）",
    "另存在独立的仿 Gmail 登录页内嵌 HTML（Welcome %gmail_to_device% / Forgot password? / Next），用于输入邮箱密码，非无障碍引导文字",
    "未发现悬浮窗 Overlay 引导、未发现本地 HTML 文件（assets/ 下无页面）、未发现远端 URL 教学页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable_Accessibility_Service%",
      "text_zh": "启用无障碍服务（模板占位符，运行期由配置替换）",
      "source_location": "classes.dex 内嵌 Base64 HTML（lluiztetabeombd WebView 页面正文）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Start Accessibility >>",
      "text_zh": "开始无障碍 >>",
      "source_location": "classes.dex 内嵌 Base64 HTML 按钮文案",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "'en': { 'accessability1':'Accessibility Service', 'downloadedservice':'DOWNLOADED SERVICES', 'switchaccess':'Switch Access', 'talkback':'TalkBack', 'off':'OFF' }",
      "text_zh": "「无障碍服务」「已下载的服务」「切换访问」「TalkBack」「关闭」——用于仿冒系统无障碍界面",
      "source_location": "classes.dex 内嵌 Base64 HTML 的 objLang 多语言表",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "'zh': { 'accessability1':'無障礙服務', 'downloadedservice':'下載的服務', 'switchaccess':'開關訪問', 'talkback':'頂嘴', 'off':'關' }",
      "text_zh": "「无障碍服务」「下载的服务」「开关访问」「顶嘴（TalkBack 误译）」「关」",
      "source_location": "classes.dex 内嵌 Base64 HTML 的 objLang 多语言表（zh 项）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on me to activate",
      "text_zh": "点我来激活",
      "source_location": "classes.dex 解密字符串（'en' 多语言表）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Open More downloaded services > ",
      "text_zh": "打开「更多已下载的服务 >」",
      "source_location": "classes.dex 解密字符串（'en' 多语言表，40+ 语言同款）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Blocked attempt to disable accessibility service[143523#]",
      "text_zh": "已拦截关闭无障碍服务的尝试",
      "source_location": "classes.dex 解密字符串",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Google update",
      "text_zh": "Google 更新",
      "source_location": "AndroidManifest.xml 无障碍服务 android:label",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "trwsdjimslf.onStartCommand 以 while(true) 循环：只要 Settings.Secure.enabled_accessibility_services 未包含自身组件，或配置项 e(this, c.ab) 不等于期望值，就 e.a(1000) 睡眠 1 秒后重新 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\")（带 NEW_TASK|CLEAR_TOP|RESET_TASK_IF_NEEDED），用户返回或拒绝授权即被立刻重新拉回系统设置页，循环无退出条件；另有无障碍服务在界面注入「Click on me to activate」引导继续点击。",
    "overlay_or_fake_settings": "未使用 SYSTEM_ALERT_WINDOW 悬浮窗遮罩；但引导页 WebView 自身即高仿系统无障碍设置界面（多语言复刻 Accessibility Service / DOWNLOADED SERVICES / Switch Access / TalkBack / OFF 条目与开关视觉），配合 Theme.Translucent.NoTitleBar 全屏呈现，可误认为系统原生页面。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=29，未发现跳转 ACTION_APPLICATION_DETAILS_SETTINGS、未发现「允许受限设置」或 Session 安装器绕过教学。",
    "post_grant_anti_removal": "有。解密字符串含「Blocked attempt to disable accessibility service[143523#]」与 time_run_bypass_protect，无障碍服务持续监听 typeWindowStateChanged 并在用户进入系统无障碍页撤权时执行阻断（静态预筛亦命中 PERFORM_GLOBAL_ACTION）；trwsdjimslf 同时持续重跳设置页施压。",
    "benign_graceful_degradation": "无。除开启无障碍服务外不存在任何替代路径、手动模式或降级提示。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "Hook 监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（lluiztetabeombd$c.openAccessibilityService 与 trwsdjimslf.onStartCommand 两处），或冷启动后 lluiztetabeombd 的 WebView 加载完成（loadDataWithBaseURL 返回）瞬间拉起 UTG 截图；前者可同时捕获循环重跳行为。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页（高仿系统无障碍界面 WebView）",
        "page_identifier": "Activity com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd，全屏无标题栏 WebView，页面标题区含「Enable_Accessibility_Service」与「Start Accessibility >>」按钮，下方仿系统条目「DOWNLOADED SERVICES / Switch Access / TalkBack / OFF」",
        "why_most_useful": "这是应用唯一的授权说理界面，直接暴露其复刻系统无障碍 UI、无任何用途说明与取消入口的诱导本质，且与 GTA V 名称毫无关联",
        "observable_utg_signals": [
          "Activity 类名 lluiztetabeombd 且为 WebView 容器",
          "页面文本含 Accessibility Service / DOWNLOADED SERVICES / TalkBack / OFF 等系统无障碍专有词",
          "页面无任何「取消 / 跳过 / 关闭 / 稍后」控件，仅有 Start Accessibility 按钮",
          "文本语言随系统语言切换（内置 40+ 语言表）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（跳转落地页）",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS，列表中出现 label 为「Google update」的条目，无描述副标题",
        "why_most_useful": "验证伪装服务名已实际注册进系统列表，且与桌面应用名 GTA V 明显不一致，是身份混淆的直接运行期证据",
        "observable_utg_signals": [
          "条目文本「Google update」",
          "条目下方无任何 description 说明文字",
          "应用包名 com.sakkkwyl.ncceberwpdhfq 与 label 不匹配"
        ]
      },
      {
        "page_role": "拒权后循环重跳压栈页",
        "page_identifier": "用户从 ACCESSIBILITY_SETTINGS 返回后 ≤1.5 秒内再次出现同一系统无障碍设置页",
        "why_most_useful": "证明存在无出口的强制循环，是区别于良性引导的关键行为特征",
        "observable_utg_signals": [
          "同一 Activity（系统无障碍设置）在短时间内被重复压栈/重复出现",
          "返回动作无法停留在桌面或上一应用",
          "日志中出现 trwsdjimslf.onStartCommand 的周期性 startActivity"
        ]
      },
      {
        "page_role": "获权后无障碍服务注入的引导文案",
        "page_identifier": "当前应用界面上出现的注入浮层文本「Click on me to activate」或「Open More downloaded services > 」",
        "why_most_useful": "证明服务获权后继续操控界面、以无障碍能力驱动进一步授权/操作，而非提供无障碍功能",
        "observable_utg_signals": [
          "非目标应用原生 UI 的文本「Click on me to activate」",
          "「Open More downloaded services >」提示与系统设置页文案混排"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区在于：引导页 HTML 与全部字符串在 DEX 内以自研编码（RC4 key+Base64+hex）存放，纯 strings/静态资源扫描（assets、res/layout、strings.xml）完全取不到任何引导文案，需先解密 DEX 字符串；WebView 页面无本地 HTML 文件，UTG 必须依赖运行期截图而非资源文件比对。此外入口 iexuymsx 在非目标厂商分支会直接 finish() 且不展示任何界面，冷启动可能瞬时不出现可见页面，需按厂商/版本条件重试触发。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.sakkkwyl.ncceberwpdhfq.iexuymsx.onCreate",
    "com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd.onCreate",
    "com.sakkkwyl.ncceberwpdhfq.lluiztetabeombd$c.openAccessibilityService",
    "com.sakkkwyl.ncceberwpdhfq.trwsdjimslf.onStartCommand",
    "com.sakkkwyl.ncceberwpdhfq.e.b(Context, Class)",
    "res/xml/shreix.xml"
  ]
}
```

</details>
