# MB_130__11af0da9a7｜TrickMo — Google services

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：134.2s

## 1. 一句话核心结论

- **核心申请方式**：冒充 Google services 的恶意样本，冷启动即用本地 HTML WebView 播放假加载动画后展示三步无障碍开启教学，点击按钮经 JS 桥跳系统无障碍设置，并配合 clicker.json 自动点按系统页完成授权/激活设备管理，获权后立即跳转 https://xxxtik.com 控制面板。
- **静态可见性说明**：引导页文案、三步教学、JS桥调用名、获权后跳转 URL 与 clicker.json 自动化规则均在包内明文可见；但装载 www/index.html 的 WebView 容器代码与 android.openAccessibilitySettings/isAccessibilityServiceEnabled 的 Java 侧绑定位于高度混淆类中未能精确定位，5.4MB 的 assets/MAtN.json 疑为后续模板/资源包未展开，属部分静态可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `11af0da9a7c5f65bb098ed52973e814b12eba492fb3615a5fada5d4cc390928d` |
| 包名 / 年份 | `consnews.matt960.can` / 2024 |
| 家族 / 品类 | **TrickMo**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google services |
| 引导页宣称品牌/身份 | Google Play services / Google services（Google LLC 官方服务） |
| 系统无障碍列表服务名 | Google services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 consnews.matt960.can 与无障碍服务类名 mcomOWj1nw2rRdmt 均为随机无意义串；桌面名、入口 Activity 标签、无障碍服务名、WebView 页标题 app_title 全部统一为 'Google services'；android:description 逐字抄袭 Google Play 服务官方说明；accessibilityservice.xml 声明 isAccessibilityTool="true" 伪造为官方无障碍工具；dex 中混入 com.dubox.drive、com.crunchyroll、com.ticket 等第三方应用代码作掩护；入口 Activity 设置 noHistory/excludeFromRecents 隐藏任务栈痕迹。 |
| 无障碍服务类名 | `consnews.matt960.can.mcomOWj1nw2rRdmt` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Google play services also enhances your app experience. It speeds up offline searches, provides more immersive maps, and improves gaming experiences. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | consnews.matt960.can.MdaFXbaTi（exported、noHistory、excludeFromRecents 的 WebView 容器 Activity，label=@string/activity_name） | 用户点击桌面图标冷启动，Activity onCreate 加载 assets/www/index.html | 本地HTML WebView | **原文**：<div id="pre_loader" style="background:#fff;height:100%;...z-index:1000;"><img src="data:image/gif;base64,R0lGODlh..."></div><br>**译注**：全屏白色假加载动画（base64 GIF），持续 3000ms 后隐藏并显示正文 | 无操作，被动等待加载动画结束（无取消/跳过入口） | `assets/www/index.html#L339、#L397-L401；AndroidManifest.xml 中 consnews.matt960.can.MdaFXbaTi` |
| 2 | 引导说明页 | assets/www/index.html 的 #main_div / #foAccess / #step_1 / #step_2 / #step_3 区块（本地 HTML WebView 页面） | setTimeout 3000ms 后 main_div display=block；DOMContentLoaded 同时调用 android.startPushService() | 本地HTML WebView | **原文**：Activate Accessibility services for the correct application work.<br>Step 1. - Go to Settings<br>Step 2. - Open the menu "Downloaded services"<br>Step 3. - Activate services for Google Play services<br>**译注**：请为应用程序正常运行启用无障碍服务；第 1 步 前往设置；第 2 步 打开"已下载的服务"菜单；第 3 步 为 Google Play 服务启用该服务 | 按页面提示自行进入系统设置开启服务；页面仅有"Go to Settings"一个按钮，无取消/跳过/关闭选项 | `assets/www/index.html#L381-L387、#L403-L408；多语言文案表 index.html#L28-L70` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（经 WebView JS 桥 android.openAccessibilitySettings(true) 拉起） | 用户点击 #btn1 按钮 onclick="android.openAccessibilitySettings(true)" | 系统无障碍页 | **原文**：<button type="button" class="btnmy" id="btn1" onclick="android.openAccessibilitySettings(true)" ...>Aller aux paramètres</button><br>**译注**：绿色按钮"前往设置"（默认英文 Go to Settings），点击后跳到系统无障碍服务列表 | 在系统无障碍列表中找到"Google services"并拨开开关，确认系统警告弹窗 | `assets/www/index.html#L387；JS 桥方法 android.openAccessibilitySettings` |
| 4 | 遮罩叠层指引 | assets/img_1_english.webp、img_2_english.webp、img_2_hamburg.webp 等截图引导图（WebView 内嵌图） | 引导页渲染时加载对应语言的截图素材 | 本地HTML WebView | **原文**：img_1_english.webp / img_2_english.webp / img_2_hamburg.webp<br>**译注**：以真实系统设置截图逐屏演示无障碍开关位置（含特定厂商 ROM 版本），属纯图引导 | 对照截图在系统设置中逐步操作 | `assets/img_1_english.webp、assets/img_2_english.webp、assets/img_2_hamburg.webp` |
| 5 | 拒权反馈循环 | WebView 页面重载 + clicker.json 规则（eventPackageName=com.android.settings） | 用户从设置页返回（WebView 恢复/重新加载）时再次执行 android.isAccessibilityServiceEnabled() 判定 | 本地HTML WebView | **原文**：if(android.isAccessibilityServiceEnabled()) {window.location.href ="https://xxxtik.com";} else { android.startPushService(); }<br>**译注**：若无障碍未开启则停留原引导页并再次启动推送服务，等待用户重试，无降级或退出路径 | 只能继续开启无障碍，页面不提供"稍后再说/不再提示" | `assets/www/index.html#L434-L437` |
| 6 | 获权后动作 | 系统设置/Play 商店/安装器页面上由无障碍服务执行的自动点击（clicker.json 规则集）＋ WebView 跳转远端页面 | 无障碍服务启用后 isAccessibilityServiceEnabled() 返回 true | 悬浮窗Overlay | **原文**："Activate device admin (ALL LANG) (Samsung, Huawei)" ... "id~": "com.android.settings:id/restricted_action\|com.android.settings:id/action_button", "actions": [{"id": "pressConfirm", "action": "click"...}]；"Google Protect Turn On - Cancel" ... "actions": [{"action": "sendText", "argText": "{ruleName}"}, {"action": "pressBack"}]<br>**译注**：自动点击设备管理激活确认（含受限设置确认按钮）、关闭 Google Play Protect 弹窗、取消卸载流程并回到桌面；同时 WebView 跳转 https://xxxtik.com | 用户无需操作，由无障碍服务代点系统按钮 | `assets/clicker.json#L5-L37；assets/www/index.html#L434` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets/www/index.html 本地 WebView 引导页：#foAccess 一句总述、#step_1/#step_2/#step_3 三步分条教学、#btn1 绿色"Go to Settings"按钮（无取消按钮）
- assets/www/index.html 内置多语言文案表（es/fr/de/default 等 case 分支），按 navigator.language 自动切换，并按 is_xiaomi/is_samsung 改写第 2 步菜单名（Downloaded services / Apps downloaded / Installed apps）
- assets/www/index.html 顶部 3 秒全屏 base64 GIF 假加载动画（pre_loader）
- assets/img_1_english.webp、img_2_english.webp、img_2_hamburg.webp 等系统设置截图式图文引导
- 系统无障碍服务列表项：android:label="Google services"，android:description 为整段 Google Play 服务官方说明（res/values/strings.xml#L30-L31）
- res/values/strings.xml#L58 message："Please enable the accessibility menu for Google services. ... Without Google services your phone may be slow." 恐吓式说明
- res/values/strings.xml#L39-L52 一组 Google Play services 缺失/需更新的官方原文案（Enable/Get/Update Google Play services）作为伪装素材
- clicker.json 中 setVar 注入的自定义弹窗文案："Settings" / "You are trying to delete an official Android system application. This may lead to complete data loss on the device."（卸载拦截恐吓弹窗）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Activate Accessibility services for the correct application work. | 请启用无障碍服务以保证应用程序正常运行。 | `assets/www/index.html 第 59 行（default 分支 foAccess）` | 受限设置分步教学 |
| en | Step 1. - Go to Settings / Step 2. - Open the menu "Downloaded services" / Step 3. - Activate services for Google Play services | 第 1 步 前往设置；第 2 步 打开"已下载的服务"菜单；第 3 步 为 Google Play 服务启用该服务。 | `assets/www/index.html 第 60-66 行、第 383-385 行` | 受限设置分步教学 |
| en | This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Google play services also enhances your app experience. It speeds up offline searches, provides more immersive maps, and improves gaming experiences. | 该组件提供 Google 服务身份验证、联系人同步、访问最新隐私设置以及更高质量、更低功耗的基于位置的服务等核心功能。Google Play 服务还能提升应用体验，加速离线搜索、提供更沉浸的地图和更好的游戏体验。 | `res/values/strings.xml#L30 accessibility_service_description（系统无障碍服务详情页显示）` | 隐私承诺 |
| en | Please enable the accessibility menu for Google services. This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Without Google services your phone may be slow. | 请为 Google 服务启用无障碍菜单。该组件提供 Google 服务身份验证、联系人同步、访问最新隐私设置以及更高质量、更低功耗的位置服务等核心功能。没有 Google 服务，你的手机可能会变慢。 | `res/values/strings.xml#L58 message` | 故障恐吓 |
| en | "Enable Google Play services" / "%1$s won't work unless you enable Google Play services." / "Get Google Play services" / "%1$s won't run without Google Play services, which are missing from your device." | "启用 Google Play 服务" / "除非启用 Google Play 服务，否则 %1$s 无法运行。" / "获取 Google Play 服务" / "设备缺少 Google Play 服务，%1$s 无法运行。" | `res/values/strings.xml#L39-L52` | 故障恐吓 |
| en | You are trying to delete an official Android system application. This may lead to complete data loss on the device. | 你正在尝试删除一个官方 Android 系统应用，这可能导致设备上的数据完全丢失。 | `assets/clicker.json 第 37 行 setVar ShowDialog` | 故障恐吓 |
| fr | Activez les services d'accessibilité pour les travaux d'application corrects. / Étape 1. - Accédez aux paramètres / Étape 2. - Ouvrez le menu "Services téléchargés" / Étape 3. - Activer les services pour Google Play services / Aller aux paramètres | 请启用无障碍服务以保证应用正常工作。第 1 步 前往设置；第 2 步 打开"已下载的服务"菜单；第 3 步 为 Google Play 服务启用服务；按钮：前往设置。 | `assets/www/index.html 第 34-40 行、第 381-387 行` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：引导页仅有"Go to Settings"一个按钮，无返回/跳过；用户从系统设置返回后 WebView 重新执行 android.isAccessibilityServiceEnabled()，未开启则继续留在引导页并再次 android.startPushService()，不提供退出或降级路径；同时 clicker.json 规则在系统设置页执行 sendText{ruleName} 与 pressBack/pressHome，把用户拉回或代其操作。
- **遮罩叠层 / 高仿系统设置页**：未见半透明遮罩或高仿无障碍开关页；采用真实系统设置页 + 本地 WebView 三步图文教学 + 系统设置截图素材（img_1_english.webp 等），并在服务声明中伪造 isAccessibilityTool="true" 弱化系统警告。
- **Android 13+ 受限设置（Restricted Settings）应对**：无文字版受限设置教学；但 clicker.json 的 "Activate device admin (ALL LANG)" 规则直接定位并点击 com.android.settings:id/restricted_action|action_button（即 Android 13+ 受限设置确认按钮），由无障碍服务代替用户点击确认。
- **获权后即时行为与防撤权机制**：有：clicker.json 提供 "Deactivate device admin cancel"、"uninstall cancel (ENG)" 等规则，在用户尝试停用设备管理或卸载时自动点击取消（pressConfirm）并弹出自定义恐吓弹窗；同时 Manifest 声明 DeviceAdminReceiver 与 FORCE_STOP_PACKAGES/REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，配合无障碍自动操作维持驻留。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最优先：监测到本应用 Activity 启动后 3 秒内 WebView 页面出现"Step 1. - Go to Settings / Go to Settings"按钮并伴随对 android.settings.ACCESSIBILITY_SETTINGS 的跳转意图时立即抓取；其次：无障碍服务列表页出现 label="Google services" 条目被拨开瞬间抓取（可同时捕获系统警告弹窗与后续自动点击）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：引导页在 3 秒假加载动画期间无可读文本（base64 GIF 全屏覆盖），过早截图会得到空白页；img_*.webp 截图为纯图引导但文本版教学已足够判别，无需 OCR；dex 侧 WebView 装载与 JS 桥绑定高度混淆，若采用纯静态特征匹配（如搜索 openAccessibilitySettings 字符串）会漏检，须以运行期页面文本与 ACCESSIBILITY_SETTINGS 跳转行为为准；assets/MAtN.json（5.4MB）与远端 xxxtik.com 后续模板未展开，可能存在一阶段外壳/后续变体差异。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（WebView 假加载后三步教学页）** | 全屏白色页面顶部一句"Activate Accessibility services for the correct application work."，下方三条浅灰底分步条目 Step 1/2/3，底部绿色"Go to Settings"按钮，无返回/取消按钮 | 这是诱导链条唯一的人工可读入口，直接证明应用以 Google 品牌名义要求开启无障碍，且无跳过路径 | 无障碍服务名 'Google services' 出现在应用自身引导文案中；文案包含 'Step 1. - Go to Settings' 与 'Accessibility services' 共现；页面仅存在一个可点击按钮且文本为 Go to Settings/Aller aux paramètres；无任何取消、跳过、稍后提示控件 |
| **系统无障碍服务列表项与详情页** | 设置→无障碍→已下载的服务中名为 'Google services' 的条目，详情页描述为整段 Google Play 服务官方文案 | 核对服务名/描述与官方 Google Play 服务是否一致，是判定品牌冒用与 isAccessibilityTool 伪装的直接证据 | 服务标签 'Google services' 与安装包名 consnews.matt960.can 不匹配；描述文本为 Google Play 服务官方说明的逐字复制；应用信息页显示应用名 Google services 但开发者/包名为随机串 |
| **授权后自动点击/反卸载页（系统设置、Play Protect、安装器弹窗）** | 设备管理激活确认页（含受限设置确认按钮）、Google Play Protect 关闭弹窗、卸载确认弹窗被自动点按并返回桌面的瞬间 | 证明无障碍权限已被用于代替用户点按系统安全按钮，是恶意性最关键的一环 | 用户无触摸输入但系统按钮被点击（UTG 上可见无手势却发生 click）；系统设置/安装器页面被 pressBack/pressHome 快速关闭；出现自定义标题 'Settings' 的恐吓弹窗文本 'delete an official Android system application' |
| **获权后跳转的远端页面** | WebView 加载 https://xxxtik.com 后的界面（远控面板/伪装页） | 验证权限获取与业务切换的因果，确认该域名仅在全权限达成后可达 | 跳转发生在无障碍开启之后、未开启时不出现；页面地址栏/网络请求出现 xxxtik.com |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `assets/www/index.html#L381-L387（三步教学页与 android.openAccessibilitySettings(true) 按钮）`
- `assets/www/index.html#L434-L437（isAccessibilityServiceEnabled 判定与 https://xxxtik.com 跳转）`
- `assets/clicker.json#L27-L37（系统设置 restricted_action 自动点击、Play Protect 关闭、卸载拦截恐吓弹窗）`
- `res/xml/accessibilityservice.xml（isAccessibilityTool="true"、typeAllMask、canPerformGestures、canTakeScreenshot）`
- `res/values/strings.xml#L30-L31、#L58（Google services 服务名/官方描述与"手机变慢"恐吓文案）`
- `AndroidManifest.xml: consnews.matt960.can.mcomOWj1nw2rRdmt 无障碍服务 + consnews.matt960.can.MdaFXbaTi 入口 Activity`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

工具调用预算已用尽，停止探索并立即输出结论。

## 分析结论（要点）

**核心事实（已静态确认）**

1. **身份伪装**：应用桌面名、入口 Activity 标签、无障碍服务标签统一为 `Google services`；无障碍服务声明 `android:description` 直接照抄 Google Play 服务官方说明文案，服务类名与包名均为随机混淆串 `consnews.matt960.can.mcomOWj1nw2rRdmt`。
2. **伪造无障碍工具属性**：[accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml>) 中声明 `isAccessibilityTool="true"`，同时开启 `typeAllMask`、`canRetrieveWindowContent`、`canPerformGestures`、`canTakeScreenshot` —— 以"官方无障碍工具"身份弱化系统对敏感能力的提示。
3. **运行期引导载体为本地 WebView HTML**：[assets/www/index.html](<resource-unit:#1 file:assets/www/index.html#L381-L387>) 内置多语言（en/de/fr/es/it 等）分步教学页，文案为 `Activate Accessibility services for the correct application work.` + `Step 1. - Go to Settings` / `Step 2. - Open the menu "Downloaded services"` / `Step 3. - Activate services for Google Play services`，按钮 `btn1` 的 onclick 直接调用 JS 桥 `android.openAccessibilitySettings(true)`。页面带 3 秒假加载动画（base64 GIF preloader）后显示正文。
4. **获权后即刻切换业务**：[index.html 第 434 行](<resource-unit:#1 file:assets/www/index.html#L434>) `if(android.isAccessibilityServiceEnabled()) {window.location.href ="https://xxxtik.com";}` —— 未获权则继续 `android.startPushService()`，形成"未授权即停留引导页"的循环。
5. **系统设置页自动化点击**：[assets/clicker.json](<resource-unit:#1 file:assets/clicker.json#L27-L30>) 定义针对 `com.android.settings`、`com.android.vending`、`com.google.android.packageinstaller` 的规则集，含 `Activate device admin`（点击 `restricted_action`/`action_button`）、`Google Protect Turn On`、`uninstall cancel` 等，动作为 `sendText{ruleName}`、`click`、`pressBack`、`pressHome` —— 即借无障碍能力自动完成设备管理激活、关闭 Play Protect、拦截卸载。
6. **恐吓话术**：[strings.xml 第 58 行](<resource-unit:#1 file:res/values/strings.xml#L58>) `Please enable the accessibility menu for Google services. ... Without Google services your phone may be slow.`（不开就"手机变慢"）。

**未决与覆盖边界**

- HTML 中 `android.*` 桥接方法（`openAccessibilitySettings` / `isAccessibilityServiceEnabled` / `startPushService`）在 `classes.dex` 文本索引中未直接命中，Java 侧 WebView 装载与 `addJavascriptInterface` 绑定位于高度混淆的类（`com.ticket.web.*`、`com.dubox.drive.*`、`com.crunchyroll.*` 等混入包）中，未能精确定位到具体方法，故 Java 侧调用链标注为部分静态可见。
- 入口 Activity `consnews.matt960.can.MdaFXbaTi`（`noHistory`、`excludeFromRecents`）为 WebView 容器，其装载 `www/index.html` 的代码未静态还原；`assets/MAtN.json`（5.4 MB）与 `resourceGroup.json` 疑为后续模板/资源包，未展开。
- 因超出本轮调用预算，未做动态验证；无障碍开启后的远控面板 `https://xxxtik.com` 未取证。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "引导页文案、三步教学、JS桥调用名、获权后跳转 URL 与 clicker.json 自动化规则均在包内明文可见；但装载 www/index.html 的 WebView 容器代码与 android.openAccessibilitySettings/isAccessibilityServiceEnabled 的 Java 侧绑定位于高度混淆类中未能精确定位，5.4MB 的 assets/MAtN.json 疑为后续模板/资源包未展开，属部分静态可见。",
  "summary_one_liner": "冒充 Google services 的恶意样本，冷启动即用本地 HTML WebView 播放假加载动画后展示三步无障碍开启教学，点击按钮经 JS 桥跳系统无障碍设置，并配合 clicker.json 自动点按系统页完成授权/激活设备管理，获权后立即跳转 https://xxxtik.com 控制面板。",
  "disguise_identity": {
    "app_display_name": "Google services",
    "claimed_brand_or_persona": "Google Play services / Google services（Google LLC 官方服务）",
    "a11y_service_label": "Google services",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 consnews.matt960.can 与无障碍服务类名 mcomOWj1nw2rRdmt 均为随机无意义串；桌面名、入口 Activity 标签、无障碍服务名、WebView 页标题 app_title 全部统一为 'Google services'；android:description 逐字抄袭 Google Play 服务官方说明；accessibilityservice.xml 声明 isAccessibilityTool=\"true\" 伪造为官方无障碍工具；dex 中混入 com.dubox.drive、com.crunchyroll、com.ticket 等第三方应用代码作掩护；入口 Activity 设置 noHistory/excludeFromRecents 隐藏任务栈痕迹。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "consnews.matt960.can.MdaFXbaTi（exported、noHistory、excludeFromRecents 的 WebView 容器 Activity，label=@string/activity_name）",
      "trigger_event": "用户点击桌面图标冷启动，Activity onCreate 加载 assets/www/index.html",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "<div id=\"pre_loader\" style=\"background:#fff;height:100%;...z-index:1000;\"><img src=\"data:image/gif;base64,R0lGODlh...\"></div>",
      "shown_text_zh": "全屏白色假加载动画（base64 GIF），持续 3000ms 后隐藏并显示正文",
      "user_action_requested": "无操作，被动等待加载动画结束（无取消/跳过入口）",
      "code_anchor": "assets/www/index.html#L339、#L397-L401；AndroidManifest.xml 中 consnews.matt960.can.MdaFXbaTi"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "assets/www/index.html 的 #main_div / #foAccess / #step_1 / #step_2 / #step_3 区块（本地 HTML WebView 页面）",
      "trigger_event": "setTimeout 3000ms 后 main_div display=block；DOMContentLoaded 同时调用 android.startPushService()",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Activate Accessibility services for the correct application work.\nStep 1. - Go to Settings\nStep 2. - Open the menu \"Downloaded services\"\nStep 3. - Activate services for Google Play services",
      "shown_text_zh": "请为应用程序正常运行启用无障碍服务；第 1 步 前往设置；第 2 步 打开\"已下载的服务\"菜单；第 3 步 为 Google Play 服务启用该服务",
      "user_action_requested": "按页面提示自行进入系统设置开启服务；页面仅有\"Go to Settings\"一个按钮，无取消/跳过/关闭选项",
      "code_anchor": "assets/www/index.html#L381-L387、#L403-L408；多语言文案表 index.html#L28-L70"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（经 WebView JS 桥 android.openAccessibilitySettings(true) 拉起）",
      "trigger_event": "用户点击 #btn1 按钮 onclick=\"android.openAccessibilitySettings(true)\"",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "<button type=\"button\" class=\"btnmy\" id=\"btn1\" onclick=\"android.openAccessibilitySettings(true)\" ...>Aller aux paramètres</button>",
      "shown_text_zh": "绿色按钮\"前往设置\"（默认英文 Go to Settings），点击后跳到系统无障碍服务列表",
      "user_action_requested": "在系统无障碍列表中找到\"Google services\"并拨开开关，确认系统警告弹窗",
      "code_anchor": "assets/www/index.html#L387；JS 桥方法 android.openAccessibilitySettings"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "assets/img_1_english.webp、img_2_english.webp、img_2_hamburg.webp 等截图引导图（WebView 内嵌图）",
      "trigger_event": "引导页渲染时加载对应语言的截图素材",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "img_1_english.webp / img_2_english.webp / img_2_hamburg.webp",
      "shown_text_zh": "以真实系统设置截图逐屏演示无障碍开关位置（含特定厂商 ROM 版本），属纯图引导",
      "user_action_requested": "对照截图在系统设置中逐步操作",
      "code_anchor": "assets/img_1_english.webp、assets/img_2_english.webp、assets/img_2_hamburg.webp"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "WebView 页面重载 + clicker.json 规则（eventPackageName=com.android.settings）",
      "trigger_event": "用户从设置页返回（WebView 恢复/重新加载）时再次执行 android.isAccessibilityServiceEnabled() 判定",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "if(android.isAccessibilityServiceEnabled()) {window.location.href =\"https://xxxtik.com\";} else { android.startPushService(); }",
      "shown_text_zh": "若无障碍未开启则停留原引导页并再次启动推送服务，等待用户重试，无降级或退出路径",
      "user_action_requested": "只能继续开启无障碍，页面不提供\"稍后再说/不再提示\"",
      "code_anchor": "assets/www/index.html#L434-L437"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "系统设置/Play 商店/安装器页面上由无障碍服务执行的自动点击（clicker.json 规则集）＋ WebView 跳转远端页面",
      "trigger_event": "无障碍服务启用后 isAccessibilityServiceEnabled() 返回 true",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "\"Activate device admin (ALL LANG) (Samsung, Huawei)\" ... \"id~\": \"com.android.settings:id/restricted_action|com.android.settings:id/action_button\", \"actions\": [{\"id\": \"pressConfirm\", \"action\": \"click\"...}]；\"Google Protect Turn On - Cancel\" ... \"actions\": [{\"action\": \"sendText\", \"argText\": \"{ruleName}\"}, {\"action\": \"pressBack\"}]",
      "shown_text_zh": "自动点击设备管理激活确认（含受限设置确认按钮）、关闭 Google Play Protect 弹窗、取消卸载流程并回到桌面；同时 WebView 跳转 https://xxxtik.com",
      "user_action_requested": "用户无需操作，由无障碍服务代点系统按钮",
      "code_anchor": "assets/clicker.json#L5-L37；assets/www/index.html#L434"
    }
  ],
  "text_presentation_locations": [
    "assets/www/index.html 本地 WebView 引导页：#foAccess 一句总述、#step_1/#step_2/#step_3 三步分条教学、#btn1 绿色\"Go to Settings\"按钮（无取消按钮）",
    "assets/www/index.html 内置多语言文案表（es/fr/de/default 等 case 分支），按 navigator.language 自动切换，并按 is_xiaomi/is_samsung 改写第 2 步菜单名（Downloaded services / Apps downloaded / Installed apps）",
    "assets/www/index.html 顶部 3 秒全屏 base64 GIF 假加载动画（pre_loader）",
    "assets/img_1_english.webp、img_2_english.webp、img_2_hamburg.webp 等系统设置截图式图文引导",
    "系统无障碍服务列表项：android:label=\"Google services\"，android:description 为整段 Google Play 服务官方说明（res/values/strings.xml#L30-L31）",
    "res/values/strings.xml#L58 message：\"Please enable the accessibility menu for Google services. ... Without Google services your phone may be slow.\" 恐吓式说明",
    "res/values/strings.xml#L39-L52 一组 Google Play services 缺失/需更新的官方原文案（Enable/Get/Update Google Play services）作为伪装素材",
    "clicker.json 中 setVar 注入的自定义弹窗文案：\"Settings\" / \"You are trying to delete an official Android system application. This may lead to complete data loss on the device.\"（卸载拦截恐吓弹窗）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Activate Accessibility services for the correct application work.",
      "text_zh": "请启用无障碍服务以保证应用程序正常运行。",
      "source_location": "assets/www/index.html 第 59 行（default 分支 foAccess）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. - Go to Settings / Step 2. - Open the menu \"Downloaded services\" / Step 3. - Activate services for Google Play services",
      "text_zh": "第 1 步 前往设置；第 2 步 打开\"已下载的服务\"菜单；第 3 步 为 Google Play 服务启用该服务。",
      "source_location": "assets/www/index.html 第 60-66 行、第 383-385 行",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Google play services also enhances your app experience. It speeds up offline searches, provides more immersive maps, and improves gaming experiences.",
      "text_zh": "该组件提供 Google 服务身份验证、联系人同步、访问最新隐私设置以及更高质量、更低功耗的基于位置的服务等核心功能。Google Play 服务还能提升应用体验，加速离线搜索、提供更沉浸的地图和更好的游戏体验。",
      "source_location": "res/values/strings.xml#L30 accessibility_service_description（系统无障碍服务详情页显示）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enable the accessibility menu for Google services. This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Without Google services your phone may be slow.",
      "text_zh": "请为 Google 服务启用无障碍菜单。该组件提供 Google 服务身份验证、联系人同步、访问最新隐私设置以及更高质量、更低功耗的位置服务等核心功能。没有 Google 服务，你的手机可能会变慢。",
      "source_location": "res/values/strings.xml#L58 message",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "\"Enable Google Play services\" / \"%1$s won't work unless you enable Google Play services.\" / \"Get Google Play services\" / \"%1$s won't run without Google Play services, which are missing from your device.\"",
      "text_zh": "\"启用 Google Play 服务\" / \"除非启用 Google Play 服务，否则 %1$s 无法运行。\" / \"获取 Google Play 服务\" / \"设备缺少 Google Play 服务，%1$s 无法运行。\"",
      "source_location": "res/values/strings.xml#L39-L52",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "You are trying to delete an official Android system application. This may lead to complete data loss on the device.",
      "text_zh": "你正在尝试删除一个官方 Android 系统应用，这可能导致设备上的数据完全丢失。",
      "source_location": "assets/clicker.json 第 37 行 setVar ShowDialog",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "fr",
      "text_verbatim": "Activez les services d'accessibilité pour les travaux d'application corrects. / Étape 1. - Accédez aux paramètres / Étape 2. - Ouvrez le menu \"Services téléchargés\" / Étape 3. - Activer les services pour Google Play services / Aller aux paramètres",
      "text_zh": "请启用无障碍服务以保证应用正常工作。第 1 步 前往设置；第 2 步 打开\"已下载的服务\"菜单；第 3 步 为 Google Play 服务启用服务；按钮：前往设置。",
      "source_location": "assets/www/index.html 第 34-40 行、第 381-387 行",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "引导页仅有\"Go to Settings\"一个按钮，无返回/跳过；用户从系统设置返回后 WebView 重新执行 android.isAccessibilityServiceEnabled()，未开启则继续留在引导页并再次 android.startPushService()，不提供退出或降级路径；同时 clicker.json 规则在系统设置页执行 sendText{ruleName} 与 pressBack/pressHome，把用户拉回或代其操作。",
    "overlay_or_fake_settings": "未见半透明遮罩或高仿无障碍开关页；采用真实系统设置页 + 本地 WebView 三步图文教学 + 系统设置截图素材（img_1_english.webp 等），并在服务声明中伪造 isAccessibilityTool=\"true\" 弱化系统警告。",
    "restricted_settings_13plus_coaching": "无文字版受限设置教学；但 clicker.json 的 \"Activate device admin (ALL LANG)\" 规则直接定位并点击 com.android.settings:id/restricted_action|action_button（即 Android 13+ 受限设置确认按钮），由无障碍服务代替用户点击确认。",
    "post_grant_anti_removal": "有：clicker.json 提供 \"Deactivate device admin cancel\"、\"uninstall cancel (ENG)\" 等规则，在用户尝试停用设备管理或卸载时自动点击取消（pressConfirm）并弹出自定义恐吓弹窗；同时 Manifest 声明 DeviceAdminReceiver 与 FORCE_STOP_PACKAGES/REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，配合无障碍自动操作维持驻留。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最优先：监测到本应用 Activity 启动后 3 秒内 WebView 页面出现\"Step 1. - Go to Settings / Go to Settings\"按钮并伴随对 android.settings.ACCESSIBILITY_SETTINGS 的跳转意图时立即抓取；其次：无障碍服务列表页出现 label=\"Google services\" 条目被拨开瞬间抓取（可同时捕获系统警告弹窗与后续自动点击）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（WebView 假加载后三步教学页）",
        "page_identifier": "全屏白色页面顶部一句\"Activate Accessibility services for the correct application work.\"，下方三条浅灰底分步条目 Step 1/2/3，底部绿色\"Go to Settings\"按钮，无返回/取消按钮",
        "why_most_useful": "这是诱导链条唯一的人工可读入口，直接证明应用以 Google 品牌名义要求开启无障碍，且无跳过路径",
        "observable_utg_signals": ["无障碍服务名 'Google services' 出现在应用自身引导文案中", "文案包含 'Step 1. - Go to Settings' 与 'Accessibility services' 共现", "页面仅存在一个可点击按钮且文本为 Go to Settings/Aller aux paramètres", "无任何取消、跳过、稍后提示控件"]
      },
      {
        "page_role": "系统无障碍服务列表项与详情页",
        "page_identifier": "设置→无障碍→已下载的服务中名为 'Google services' 的条目，详情页描述为整段 Google Play 服务官方文案",
        "why_most_useful": "核对服务名/描述与官方 Google Play 服务是否一致，是判定品牌冒用与 isAccessibilityTool 伪装的直接证据",
        "observable_utg_signals": ["服务标签 'Google services' 与安装包名 consnews.matt960.can 不匹配", "描述文本为 Google Play 服务官方说明的逐字复制", "应用信息页显示应用名 Google services 但开发者/包名为随机串"]
      },
      {
        "page_role": "授权后自动点击/反卸载页（系统设置、Play Protect、安装器弹窗）",
        "page_identifier": "设备管理激活确认页（含受限设置确认按钮）、Google Play Protect 关闭弹窗、卸载确认弹窗被自动点按并返回桌面的瞬间",
        "why_most_useful": "证明无障碍权限已被用于代替用户点按系统安全按钮，是恶意性最关键的一环",
        "observable_utg_signals": ["用户无触摸输入但系统按钮被点击（UTG 上可见无手势却发生 click）", "系统设置/安装器页面被 pressBack/pressHome 快速关闭", "出现自定义标题 'Settings' 的恐吓弹窗文本 'delete an official Android system application'"]
      },
      {
        "page_role": "获权后跳转的远端页面",
        "page_identifier": "WebView 加载 https://xxxtik.com 后的界面（远控面板/伪装页）",
        "why_most_useful": "验证权限获取与业务切换的因果，确认该域名仅在全权限达成后可达",
        "observable_utg_signals": ["跳转发生在无障碍开启之后、未开启时不出现", "页面地址栏/网络请求出现 xxxtik.com"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：引导页在 3 秒假加载动画期间无可读文本（base64 GIF 全屏覆盖），过早截图会得到空白页；img_*.webp 截图为纯图引导但文本版教学已足够判别，无需 OCR；dex 侧 WebView 装载与 JS 桥绑定高度混淆，若采用纯静态特征匹配（如搜索 openAccessibilitySettings 字符串）会漏检，须以运行期页面文本与 ACCESSIBILITY_SETTINGS 跳转行为为准；assets/MAtN.json（5.4MB）与远端 xxxtik.com 后续模板未展开，可能存在一阶段外壳/后续变体差异。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL"
  ],
  "code_anchors": [
    "assets/www/index.html#L381-L387（三步教学页与 android.openAccessibilitySettings(true) 按钮）",
    "assets/www/index.html#L434-L437（isAccessibilityServiceEnabled 判定与 https://xxxtik.com 跳转）",
    "assets/clicker.json#L27-L37（系统设置 restricted_action 自动点击、Play Protect 关闭、卸载拦截恐吓弹窗）",
    "res/xml/accessibilityservice.xml（isAccessibilityTool=\"true\"、typeAllMask、canPerformGestures、canTakeScreenshot）",
    "res/values/strings.xml#L30-L31、#L58（Google services 服务名/官方描述与\"手机变慢\"恐吓文案）",
    "AndroidManifest.xml: consnews.matt960.can.mcomOWj1nw2rRdmt 无障碍服务 + consnews.matt960.can.MdaFXbaTi 入口 Activity"
  ]
}
```

</details>
