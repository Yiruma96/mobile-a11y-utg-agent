# MB_134__2cdfb07d6c｜TrickMo — Google services

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：235.1s

## 1. 一句话核心结论

- **核心申请方式**：以「Google services」冒充身份，用本地多语言 HTML 页面做「进设置—打开已下载服务—为 Google Play services 开启」三步图文教学，单按钮直接拉起系统无障碍设置页，无取消路径，获权后跳转 smartclickhub.eu 并批量索取短信与电话权限。
- **静态可见性说明**：引导页与跳转逻辑（assets/www/index.html 全文、inject.js、JS 桥接调用点）完全静态可读；但 APK 的 ZIP 结构被刻意改造：56 个条目（含 index.html、clicker.json）被置为「加密」标志，且资源条目被挂到 classes.dex/、resources.arsc/ 伪目录下，常规解包器会失败，需绕过 ZIP 头直读压缩流还原。无障碍服务类 A2wC 等的具体业务实现位于被改名/混淆的 DEX 类体，未在本轮完全还原；libs/libipdetector.so 未深挖。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `2cdfb07d6cad4b2dcbbdb2713a99ae70dcdd2c049d2e3b356de4609a905e500a` |
| 包名 / 年份 | `breatham.li373.pai` / 2025 |
| 家族 / 品类 | **TrickMo**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google services |
| 引导页宣称品牌/身份 | Google Play services / Google Inc.（页面与标题均使用 Google services、Google Play services 品牌） |
| 系统无障碍列表服务名 | Google services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 为空，系统列表仅显示「Google services」而不展示权限用途说明；HTML 模板注释自曝为 'bot template title (Android Update)'，标题可被外部替换（%APP_TITLE% 占位）；ZIP 结构混淆（条目伪加密 + 资源挂到 classes.dex/、resources.arsc/ 伪目录）规避常规解包；引导文案按 Xiaomi/Samsung 机型切换菜单名以贴合真实系统路径 |
| 无障碍服务类名 | `breatham.li373.pai.A2wC` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | 承载 assets/www/index.html 的应用内 WebView Activity（Manifest 中多个随机名 Activity：StubActivity、EL_jyHnpCu、K8ahCdOuIed、Q06wlDFVTbTG、puFwYhltr、zdwdbOM1sCU、hY、VlGUhC、m2SPLg_UtP） | 应用启动加载本地 HTML，DOMContentLoaded 回调执行 android.isAccessibilityServiceEnabled() 判定 | 本地HTML WebView | **原文**：Google services / Google Inc.<br>**译注**：页面头部展示「Google services」与「Google Inc.」，伪装成 Google 官方服务组件 | 无操作，自动展示引导页面 | `assets/www/index.html#L13-L14（var app_title = 'Google services'）；#L471-L475（DOMContentLoaded 判定）` |
| 2 | 引导说明页 | 同一 WebView 内的 foAccess 说明区块与 step_1/step_2/step_3 分步条目 | isAccessibilityServiceEnabled() 返回 false，隐藏 spinner 并显示引导内容，同时 android.startPushService() | 本地HTML WebView | **原文**：Activate Accessibility services for the correct application work. Step 1. - Go to Settings Step 2. - Open "Downloaded Services" Step 3. - Activate services for the Google services<br>**译注**：请开启无障碍服务以保证应用正常运行：第1步进入设置；第2步打开「已下载的服务」（Xiaomi 为「已下载的应用」、Samsung 为「已安装的应用」）；第3步为「Google services」开启服务 | 按三步说明前往系统设置，并手动勾选「Google services」服务；页面无跳过或稍后再说按钮 | `assets/www/index.html#L59-L65（英文文案）、#L28-L34（西语）、#L39-L45（法语）、#L49-L55（德语）` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务 列表页（由 WebView 按钮触发） | 用户点击页面底部唯一按钮 btn1，触发 onclick="android.openAccessibilitySettings(true)" | 系统无障碍页 | **原文**：Go to Settings<br>**译注**：按钮文案「前往设置」，点击后跳转系统无障碍设置页 | 点击按钮跳转，并在系统列表中手动开启「Google services」开关（无取消或跳过入口） | `assets/www/index.html#L429（onclick="android.openAccessibilitySettings(true)"）` |
| 4 | 拒权反馈循环 | WebView 页面 + 返回键拦截（android.setVar("ACB_Cancel","go")） | 用户从设置页返回但未开启服务，或按返回键试图退出 | 本地HTML WebView | **原文**：Activate Accessibility services for the correct application work.<br>**译注**：返回后仍停留在同一引导页，继续要求开启无障碍；返回键被 ACB_Cancel 变量接管 | 只能重新点击「前往设置」再次尝试开启 | `assets/www/index.html#L471-L478；assets/www/inject.js#L2-L12` |
| 5 | 获权后动作 | 远端页面 https://smartclickhub.eu/good/ + PushService 前台/后台服务 | 再次进入页面时 isAccessibilityServiceEnabled() 返回 true | 远端WebView | **原文**：window.location.href = "https://smartclickhub.eu/good/"<br>**译注**：检测到无障碍已开启后，自动跳转至远端控制页面 smartclickhub.eu/good/，并向该域下发批量权限请求与忽略电池优化请求 | 无（自动跳转）；随后 inject.js 弹出 READ_SMS/RECEIVE_SMS/READ_PHONE_STATE/存储权限请求与忽略电池优化弹窗，第 5 秒与第 10 秒重复请求 | `assets/www/index.html#L471-L475；assets/www/inject.js#L2-L12` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 应用内 WebView 加载的本地页面 assets/www/index.html：顶部品牌区显示「Google services / Google Inc.」，下方 foAccess 说明块与 step_1/step_2/step_3 三步教学条目
- 同一页面底部唯一按钮 btn1（绿色 #689F39），文案「Go to Settings / Aller aux paramètres / Gehe zu den Einstellungen / Aceptar y continuar」，onclick 直连 android.openAccessibilitySettings(true)
- 系统无障碍服务列表项：服务标签为「Google services」（Manifest 中 A2wC 的 android:label），android:description 为空，列表内无任何用途说明
- 远端页面 https://smartclickhub.eu/good/（获权后跳转目标，内容不下发在包内，运行期才可见）
- inject.js 触发的原生权限请求弹窗与忽略电池优化系统弹窗（URL 含 smartclickhub 时启动）
- 波兰语片段「Identyfikator / Identyfikator powinno zawierać: od 6 do 16 znaków.」与「Dalej」按钮，位于同一 HTML 的独立覆盖层，用于收集标识符

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Activate Accessibility services for the correct application work. | 请开启无障碍服务，以保证应用正常运行。 | `assets/www/index.html#L59 (foAccess, case "en")` | 受限设置分步教学 |
| en | Step 1. - Go to Settings | 第 1 步 - 进入设置。 | `assets/www/index.html#L60 (step_1, case "en")` | 受限设置分步教学 |
| en | Step 2. - Open "Downloaded Services" | 第 2 步 - 打开「已下载的服务」菜单。 | `assets/www/index.html#L61 (step_2, case "en"；另含 step_2_xiaomi="Apps downloaded"、step_2_samsung="Applications installed")` | 受限设置分步教学 |
| en | Step 3. - Activate services for the Google services | 第 3 步 - 为「Google services」开启服务。 | `assets/www/index.html#L64 (step_3, case "en")` | 受限设置分步教学 |
| en | Go to Settings | 前往设置。 | `assets/www/index.html#L65 (btn1, case "en")；按钮 onclick 位于 #L429` | 受限设置分步教学 |
| fr | Activez les services d'accessibilité pour les travaux d'application corrects. / Étape 1. - Accédez aux paramètres / Étape 2. - Ouvrez le menu "Services téléchargés" / Étape 3. - Activer les services pour Google Play services / Aller aux paramètres | 请开启无障碍服务以保证应用正确运行。/ 第 1 步 - 进入设置 / 第 2 步 - 打开「已下载的服务」菜单 / 第 3 步 - 为 Google Play services 开启服务 / 前往设置 | `assets/www/index.html#L39-L45 (case "fr")` | 受限设置分步教学 |
| de | Aktivieren Sie Barrierefreiberdienste für die richtige Anwendungsarbeit. / Schritt 1. - Gehen Sie zu Einstellungen / Schritt 2. - Öffnen Sie das Menü "Heruntergeladene Services" / Schritt 3. - Aktivieren Sie die Dienste für den Google services / Gehe zu den Einstellungen | 请开启无障碍服务以保证应用正确运行。/ 第 1 步 - 进入设置 / 第 2 步 - 打开「已下载的服务」菜单 / 第 3 步 - 为 Google services 开启服务 / 前往设置 | `assets/www/index.html#L49-L55 (case "de")` | 受限设置分步教学 |
| es | Activar los servicios de accesibilidad para el correcto funcionamiento de la aplicación. / Paso 1. - Ve a Configuración / Paso 2. - Abra el menú "Servicios descargados" / Paso 3. - Activar servicios para Google services / Aceptar y continuar | 开启无障碍服务以保证应用正常运行。/ 第 1 步 - 进入设置 / 第 2 步 - 打开「已下载的服务」菜单 / 第 3 步 - 为 Google services 开启服务 / 接受并继续 | `assets/www/index.html#L28-L34 (case "es")` | 受限设置分步教学 |
| pl | Identyfikator powinno zawierać: od 6 do 16 znaków. | 标识符应包含 6 至 16 个字符。 | `assets/www/index.html#L385-L389（Identyfikator 覆盖层，按钮「Dalej」）` | 未知 |
| en | Google services | Google 服务（冒充品牌名，同时用作桌面显示名与无障碍服务标签） | `assets/www/index.html#L14 (var app_title = 'Google services')；Manifest 中 A2wC 的 android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：页面无取消/跳过路径；用户从系统设置返回后仍停在原引导页继续显示三步教学；inject.js 以 android.setVar("ACB_Cancel","go") 接管返回键；未获权时持续调用 android.startPushService() 维持前台/推送常驻，并在第 5 秒、第 10 秒重复请求忽略电池优化以保活
- **遮罩叠层 / 高仿系统设置页**：包内未见伪造系统无障碍开关页；引导为 WebView 内嵌图文教学页（含 base64 内联截图），未发现 SYSTEM_ALERT_WINDOW 半透明遮罩叠层的静态证据
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未见针对 Android 13+ 受限设置「允许受限设置」的引导文案或 APP_DETAILS 跳转点，也未使用 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：未确证自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权（相关逻辑位于被混淆的 A2wC 服务实现内，本轮未还原）；已确认的是获权后立即跳转远端 smartclickhub.eu/good/ 并拉起 PushService 常驻
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到应用进程启动后首次出现 WebView 页面（品牌区文本为「Google services」）时即开始抓取；并在检测到系统无障碍设置页（Settings$AccessibilitySettings 或 Settings$AccessibilityDetailsSettings）被拉起的瞬间记录压栈前的 WebView 页面快照
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导页文本为真实可提取的 DOM 文本，无需 OCR；但存在两点盲区：一是 APK 的 ZIP 结构被改造（条目伪加密 + 资源挂 classes.dex/ 伪目录），静态工具常规解包会失败而误判为空包，运行期 UTG 不受影响；二是无障碍服务类 A2wC 的业务逻辑在混淆类体内，获权后是否自点确认或阻止撤权需运行期观察，静态无法闭环。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（跳转前 WebView 教学页）** | WebView 渲染的本地页，顶部「Google services / Google Inc.」，中部三步条目，底部单个绿色按钮 | 这是诱导的核心文案载体，直接体现「为 Google services 开启无障碍」的教学与冒充身份，是区分诱导与良性说明的决定性页面 | 节点文本 Step 1. - Go to Settings / Step 2. - Open "Downloaded Services" / Step 3. - Activate services for the Google services；页面仅存在一个可点击按钮且无取消/跳过节点；品牌文本 Google services 与 Google Inc. 同页出现 |
| **系统无障碍服务列表项（Google services）** | 设置 → 无障碍 → 已下载的服务，列表中 label 为 Google services 的条目，无摘要说明 | 核验伪装身份在系统真实 UI 中的呈现效果——description 为空导致用户只能看到品牌名而看不到用途 | 条目文本仅为 Google services；条目下方无用途描述/摘要节点；开关初始为关闭状态 |
| **获权后跳转的远端页面** | WebView 地址栏或请求域名 smartclickhub.eu，路径 /good/ | 证明授权是后续远端控制/权限批量索取的前置门禁，形成「诱导→授权→下发」闭环 | 页面 URL 为 https://smartclickhub.eu/good/；出现 READ_SMS/READ_PHONE_STATE 等权限请求弹窗；出现忽略电池优化系统弹窗且重复弹出 |
| **拒权返回后的重复引导页** | 从系统设置返回后仍显示同一引导页，返回键无效 | 证明不存在跳过或降级路径，属强制循环而非一次性提示 | 返回操作后界面节点与引导页完全一致；无「稍后」「跳过」「不再提示」节点 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `assets/www/index.html#L429 (btn1 onclick="android.openAccessibilitySettings(true)")`
- `assets/www/index.html#L59-L65 (英文 foAccess/step_1/step_2/step_3/btn1 分步教学文案)`
- `assets/www/index.html#L471-L475 (isAccessibilityServiceEnabled 判定 + 跳转 https://smartclickhub.eu/good/)`
- `assets/www/inject.js#L2-L12 (smartclickhub 域下批量 requestPermissions + 重复 requestIgnoreBatteryOptimizations)`
- `assets/www/index.html#L13-L14 (var app_title = 'Google services'，注释自曝 bot template title)`
- `breatham.li373.pai.A2wC（Manifest 声明的无障碍服务，android:label=Google services，android:description 为空）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**静态可见性：** 代码与引导页完全静态可读，但 APK 的 ZIP 结构被刻意改动——56 个条目（含 `assets/www/index.html`、`clicker.json`）被标记为「加密」，且资源条目被挂在 `classes.dex/`、`resources.arsc/` 这类伪目录下，常规解包器直接失败；绕过 ZIP 头直读压缩流后，DEX（1087008 字节，与 DEX 头声明一致）与 HTML 均可正常还原。因此不能把它当成加壳，但必须按「结构混淆」处理。

**无障碍引导链（已确证）：**

1. **载体是本地 HTML，不是远端页面**：`assets/www/index.html`（239 KB）内置英/法/德/西/波多语言文案，通过 `android.*` JS 桥接调用原生方法（`isAccessibilityServiceEnabled` / `openAccessibilitySettings` / `startPushService`）。
2. **文案把权限需求伪装成「应用正确运行所需」**：英文原文为 `Activate Accessibility services for the correct application work.`，随后是 `Step 1. - Go to Settings` → `Step 2. - Open "Downloaded Services"` → `Step 3. - Activate services for the <a>Google services</a>`。第 61 行还按机型给出 Xiaomi「Apps downloaded」、Samsung「Applications installed」的菜单名变体，说明是按机型定制的教学。
3. **跳转点是页面内按钮，而非 Activity**：第 429 行 `onclick="android.openAccessibilitySettings(true)"`，由 WebView 直接拉起系统无障碍设置页。
4. **没有取消或跳过**：整个页面只有「Go to Settings / Accept and continue」一个前进按钮；`inject.js` 用 `android.setVar("ACB_Cancel","go")` 处理返回键，用户无法通过返回键退出该引导。
5. **授权后闭环**：第 471–475 行在 `DOMContentLoaded` 时检测服务是否已开启，已开启则跳转 `https://smartclickhub.eu/good/`，未开启则 `startPushService()` 保持等待；`inject.js` 在 URL 含 `smartclickhub` 时批量索取 READ_SMS/RECEIVE_SMS/READ_PHONE_STATE/存储权限，并在第 5 秒、第 10 秒重复请求忽略电池优化。
6. **身份伪装关键证据**：第 13–14 行 `var app_title = 'Google services'`，注释自曝模板为 `bot template title ('Android Update')`；该串同时是桌面显示名与无障碍服务标签，而 `android:description` 为空——系统无障碍列表只显示「Google services」，用户无从判断实际权限范围。

**未决/边界：** 无障碍服务实现类 `breatham.li373.pai.A2wC` 与 `com.aunt.gather.Mpuritydad` 等的实际业务逻辑位于 DEX 中被改名/加密的类体，本轮仅确认到配置与引导层；`libs/libipdetector.so` 未深挖。系统无障碍列表项的实际渲染文本需运行期 UTG 确认。

**关键位置：** [index.html 三步引导文案](<resource-unit:<local_path>)、[跳转按钮](<resource-unit:<local_path>)、[获权后跳转判定](<resource-unit:<local_path>)、[inject.js 权限批量索取](<resource-unit:<local_path>)

已登记风险：**R-001**（high / deceptive_behavior）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "引导页与跳转逻辑（assets/www/index.html 全文、inject.js、JS 桥接调用点）完全静态可读；但 APK 的 ZIP 结构被刻意改造：56 个条目（含 index.html、clicker.json）被置为「加密」标志，且资源条目被挂到 classes.dex/、resources.arsc/ 伪目录下，常规解包器会失败，需绕过 ZIP 头直读压缩流还原。无障碍服务类 A2wC 等的具体业务实现位于被改名/混淆的 DEX 类体，未在本轮完全还原；libs/libipdetector.so 未深挖。",
  "summary_one_liner": "以「Google services」冒充身份，用本地多语言 HTML 页面做「进设置—打开已下载服务—为 Google Play services 开启」三步图文教学，单按钮直接拉起系统无障碍设置页，无取消路径，获权后跳转 smartclickhub.eu 并批量索取短信与电话权限。",
  "disguise_identity": {
    "app_display_name": "Google services",
    "claimed_brand_or_persona": "Google Play services / Google Inc.（页面与标题均使用 Google services、Google Play services 品牌）",
    "a11y_service_label": "Google services",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 为空，系统列表仅显示「Google services」而不展示权限用途说明；HTML 模板注释自曝为 'bot template title (Android Update)'，标题可被外部替换（%APP_TITLE% 占位）；ZIP 结构混淆（条目伪加密 + 资源挂到 classes.dex/、resources.arsc/ 伪目录）规避常规解包；引导文案按 Xiaomi/Samsung 机型切换菜单名以贴合真实系统路径"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "承载 assets/www/index.html 的应用内 WebView Activity（Manifest 中多个随机名 Activity：StubActivity、EL_jyHnpCu、K8ahCdOuIed、Q06wlDFVTbTG、puFwYhltr、zdwdbOM1sCU、hY、VlGUhC、m2SPLg_UtP）",
      "trigger_event": "应用启动加载本地 HTML，DOMContentLoaded 回调执行 android.isAccessibilityServiceEnabled() 判定",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Google services / Google Inc.",
      "shown_text_zh": "页面头部展示「Google services」与「Google Inc.」，伪装成 Google 官方服务组件",
      "user_action_requested": "无操作，自动展示引导页面",
      "code_anchor": "assets/www/index.html#L13-L14（var app_title = 'Google services'）；#L471-L475（DOMContentLoaded 判定）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "同一 WebView 内的 foAccess 说明区块与 step_1/step_2/step_3 分步条目",
      "trigger_event": "isAccessibilityServiceEnabled() 返回 false，隐藏 spinner 并显示引导内容，同时 android.startPushService()",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Activate Accessibility services for the correct application work. Step 1. - Go to Settings Step 2. - Open \"Downloaded Services\" Step 3. - Activate services for the Google services",
      "shown_text_zh": "请开启无障碍服务以保证应用正常运行：第1步进入设置；第2步打开「已下载的服务」（Xiaomi 为「已下载的应用」、Samsung 为「已安装的应用」）；第3步为「Google services」开启服务",
      "user_action_requested": "按三步说明前往系统设置，并手动勾选「Google services」服务；页面无跳过或稍后再说按钮",
      "code_anchor": "assets/www/index.html#L59-L65（英文文案）、#L28-L34（西语）、#L39-L45（法语）、#L49-L55（德语）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务 列表页（由 WebView 按钮触发）",
      "trigger_event": "用户点击页面底部唯一按钮 btn1，触发 onclick=\"android.openAccessibilitySettings(true)\"",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Go to Settings",
      "shown_text_zh": "按钮文案「前往设置」，点击后跳转系统无障碍设置页",
      "user_action_requested": "点击按钮跳转，并在系统列表中手动开启「Google services」开关（无取消或跳过入口）",
      "code_anchor": "assets/www/index.html#L429（onclick=\"android.openAccessibilitySettings(true)\"）"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "WebView 页面 + 返回键拦截（android.setVar(\"ACB_Cancel\",\"go\")）",
      "trigger_event": "用户从设置页返回但未开启服务，或按返回键试图退出",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Activate Accessibility services for the correct application work.",
      "shown_text_zh": "返回后仍停留在同一引导页，继续要求开启无障碍；返回键被 ACB_Cancel 变量接管",
      "user_action_requested": "只能重新点击「前往设置」再次尝试开启",
      "code_anchor": "assets/www/index.html#L471-L478；assets/www/inject.js#L2-L12"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "远端页面 https://smartclickhub.eu/good/ + PushService 前台/后台服务",
      "trigger_event": "再次进入页面时 isAccessibilityServiceEnabled() 返回 true",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "window.location.href = \"https://smartclickhub.eu/good/\"",
      "shown_text_zh": "检测到无障碍已开启后，自动跳转至远端控制页面 smartclickhub.eu/good/，并向该域下发批量权限请求与忽略电池优化请求",
      "user_action_requested": "无（自动跳转）；随后 inject.js 弹出 READ_SMS/RECEIVE_SMS/READ_PHONE_STATE/存储权限请求与忽略电池优化弹窗，第 5 秒与第 10 秒重复请求",
      "code_anchor": "assets/www/index.html#L471-L475；assets/www/inject.js#L2-L12"
    }
  ],
  "text_presentation_locations": [
    "应用内 WebView 加载的本地页面 assets/www/index.html：顶部品牌区显示「Google services / Google Inc.」，下方 foAccess 说明块与 step_1/step_2/step_3 三步教学条目",
    "同一页面底部唯一按钮 btn1（绿色 #689F39），文案「Go to Settings / Aller aux paramètres / Gehe zu den Einstellungen / Aceptar y continuar」，onclick 直连 android.openAccessibilitySettings(true)",
    "系统无障碍服务列表项：服务标签为「Google services」（Manifest 中 A2wC 的 android:label），android:description 为空，列表内无任何用途说明",
    "远端页面 https://smartclickhub.eu/good/（获权后跳转目标，内容不下发在包内，运行期才可见）",
    "inject.js 触发的原生权限请求弹窗与忽略电池优化系统弹窗（URL 含 smartclickhub 时启动）",
    "波兰语片段「Identyfikator / Identyfikator powinno zawierać: od 6 do 16 znaków.」与「Dalej」按钮，位于同一 HTML 的独立覆盖层，用于收集标识符"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Activate Accessibility services for the correct application work.",
      "text_zh": "请开启无障碍服务，以保证应用正常运行。",
      "source_location": "assets/www/index.html#L59 (foAccess, case \"en\")",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. - Go to Settings",
      "text_zh": "第 1 步 - 进入设置。",
      "source_location": "assets/www/index.html#L60 (step_1, case \"en\")",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. - Open \"Downloaded Services\"",
      "text_zh": "第 2 步 - 打开「已下载的服务」菜单。",
      "source_location": "assets/www/index.html#L61 (step_2, case \"en\"；另含 step_2_xiaomi=\"Apps downloaded\"、step_2_samsung=\"Applications installed\")",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 3. - Activate services for the Google services",
      "text_zh": "第 3 步 - 为「Google services」开启服务。",
      "source_location": "assets/www/index.html#L64 (step_3, case \"en\")",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to Settings",
      "text_zh": "前往设置。",
      "source_location": "assets/www/index.html#L65 (btn1, case \"en\")；按钮 onclick 位于 #L429",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "fr",
      "text_verbatim": "Activez les services d'accessibilité pour les travaux d'application corrects. / Étape 1. - Accédez aux paramètres / Étape 2. - Ouvrez le menu \"Services téléchargés\" / Étape 3. - Activer les services pour Google Play services / Aller aux paramètres",
      "text_zh": "请开启无障碍服务以保证应用正确运行。/ 第 1 步 - 进入设置 / 第 2 步 - 打开「已下载的服务」菜单 / 第 3 步 - 为 Google Play services 开启服务 / 前往设置",
      "source_location": "assets/www/index.html#L39-L45 (case \"fr\")",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "de",
      "text_verbatim": "Aktivieren Sie Barrierefreiberdienste für die richtige Anwendungsarbeit. / Schritt 1. - Gehen Sie zu Einstellungen / Schritt 2. - Öffnen Sie das Menü \"Heruntergeladene Services\" / Schritt 3. - Aktivieren Sie die Dienste für den Google services / Gehe zu den Einstellungen",
      "text_zh": "请开启无障碍服务以保证应用正确运行。/ 第 1 步 - 进入设置 / 第 2 步 - 打开「已下载的服务」菜单 / 第 3 步 - 为 Google services 开启服务 / 前往设置",
      "source_location": "assets/www/index.html#L49-L55 (case \"de\")",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "es",
      "text_verbatim": "Activar los servicios de accesibilidad para el correcto funcionamiento de la aplicación. / Paso 1. - Ve a Configuración / Paso 2. - Abra el menú \"Servicios descargados\" / Paso 3. - Activar servicios para Google services / Aceptar y continuar",
      "text_zh": "开启无障碍服务以保证应用正常运行。/ 第 1 步 - 进入设置 / 第 2 步 - 打开「已下载的服务」菜单 / 第 3 步 - 为 Google services 开启服务 / 接受并继续",
      "source_location": "assets/www/index.html#L28-L34 (case \"es\")",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pl",
      "text_verbatim": "Identyfikator powinno zawierać: od 6 do 16 znaków.",
      "text_zh": "标识符应包含 6 至 16 个字符。",
      "source_location": "assets/www/index.html#L385-L389（Identyfikator 覆盖层，按钮「Dalej」）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Google services",
      "text_zh": "Google 服务（冒充品牌名，同时用作桌面显示名与无障碍服务标签）",
      "source_location": "assets/www/index.html#L14 (var app_title = 'Google services')；Manifest 中 A2wC 的 android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "页面无取消/跳过路径；用户从系统设置返回后仍停在原引导页继续显示三步教学；inject.js 以 android.setVar(\"ACB_Cancel\",\"go\") 接管返回键；未获权时持续调用 android.startPushService() 维持前台/推送常驻，并在第 5 秒、第 10 秒重复请求忽略电池优化以保活",
    "overlay_or_fake_settings": "包内未见伪造系统无障碍开关页；引导为 WebView 内嵌图文教学页（含 base64 内联截图），未发现 SYSTEM_ALERT_WINDOW 半透明遮罩叠层的静态证据",
    "restricted_settings_13plus_coaching": "无（未见针对 Android 13+ 受限设置「允许受限设置」的引导文案或 APP_DETAILS 跳转点，也未使用 Session 安装器绕过）",
    "post_grant_anti_removal": "未确证自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权（相关逻辑位于被混淆的 A2wC 服务实现内，本轮未还原）；已确认的是获权后立即跳转远端 smartclickhub.eu/good/ 并拉起 PushService 常驻",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到应用进程启动后首次出现 WebView 页面（品牌区文本为「Google services」）时即开始抓取；并在检测到系统无障碍设置页（Settings$AccessibilitySettings 或 Settings$AccessibilityDetailsSettings）被拉起的瞬间记录压栈前的 WebView 页面快照",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（跳转前 WebView 教学页）",
        "page_identifier": "WebView 渲染的本地页，顶部「Google services / Google Inc.」，中部三步条目，底部单个绿色按钮",
        "why_most_useful": "这是诱导的核心文案载体，直接体现「为 Google services 开启无障碍」的教学与冒充身份，是区分诱导与良性说明的决定性页面",
        "observable_utg_signals": ["节点文本 Step 1. - Go to Settings / Step 2. - Open \"Downloaded Services\" / Step 3. - Activate services for the Google services", "页面仅存在一个可点击按钮且无取消/跳过节点", "品牌文本 Google services 与 Google Inc. 同页出现"]
      },
      {
        "page_role": "系统无障碍服务列表项（Google services）",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，列表中 label 为 Google services 的条目，无摘要说明",
        "why_most_useful": "核验伪装身份在系统真实 UI 中的呈现效果——description 为空导致用户只能看到品牌名而看不到用途",
        "observable_utg_signals": ["条目文本仅为 Google services", "条目下方无用途描述/摘要节点", "开关初始为关闭状态"]
      },
      {
        "page_role": "获权后跳转的远端页面",
        "page_identifier": "WebView 地址栏或请求域名 smartclickhub.eu，路径 /good/",
        "why_most_useful": "证明授权是后续远端控制/权限批量索取的前置门禁，形成「诱导→授权→下发」闭环",
        "observable_utg_signals": ["页面 URL 为 https://smartclickhub.eu/good/", "出现 READ_SMS/READ_PHONE_STATE 等权限请求弹窗", "出现忽略电池优化系统弹窗且重复弹出"]
      },
      {
        "page_role": "拒权返回后的重复引导页",
        "page_identifier": "从系统设置返回后仍显示同一引导页，返回键无效",
        "why_most_useful": "证明不存在跳过或降级路径，属强制循环而非一次性提示",
        "observable_utg_signals": ["返回操作后界面节点与引导页完全一致", "无「稍后」「跳过」「不再提示」节点"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导页文本为真实可提取的 DOM 文本，无需 OCR；但存在两点盲区：一是 APK 的 ZIP 结构被改造（条目伪加密 + 资源挂 classes.dex/ 伪目录），静态工具常规解包会失败而误判为空包，运行期 UTG 不受影响；二是无障碍服务类 A2wC 的业务逻辑在混淆类体内，获权后是否自点确认或阻止撤权需运行期观察，静态无法闭环。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "assets/www/index.html#L429 (btn1 onclick=\"android.openAccessibilitySettings(true)\")",
    "assets/www/index.html#L59-L65 (英文 foAccess/step_1/step_2/step_3/btn1 分步教学文案)",
    "assets/www/index.html#L471-L475 (isAccessibilityServiceEnabled 判定 + 跳转 https://smartclickhub.eu/good/)",
    "assets/www/inject.js#L2-L12 (smartclickhub 域下批量 requestPermissions + 重复 requestIgnoreBatteryOptimizations)",
    "assets/www/index.html#L13-L14 (var app_title = 'Google services'，注释自曝 bot template title)",
    "breatham.li373.pai.A2wC（Manifest 声明的无障碍服务，android:label=Google services，android:description 为空）"
  ]
}
```

</details>
