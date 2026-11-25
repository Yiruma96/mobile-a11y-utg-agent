# MB_157__a769c40ce4｜BingoMod — Scudo App

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：241.3s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即以全屏 WebView 加载 assets 本地意大利语盾牌诱导页，无跳过按钮强制点 Prosegui，经 JavascriptInterface 直接 startActivity 跳系统设置页，并靠 isAccessibilityTool=true 与缺失 label/description 掩盖无障碍服务真实能力
- **静态可见性说明**：Manifest、无障碍服务配置、assets 本地 HTML 诱导页与 JS 桥调用链完全静态可见；但 onButtonClicked 内 Intent action 字符串、loadUrl 的 asset 路径与部分提示文案均经自定义字符串加密（String[] 分块密文表 + pd8097feb$pefc6dad5$p9fab99f0.a(long) 解密），未逐字还原，故跳转目标为无障碍设置页/应用详情页的精确 action 字面量未证实；无整体加壳、无远端下发 HTML
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a769c40ce48a38eed8897447081fc002d567535943befc4b51d866d134953588` |
| 包名 / 年份 | `p1a1fa04c.pae25061e.p658c02c8` / 2025 |
| 家族 / 品类 | **BingoMod**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Scudo App |
| 引导页宣称品牌/身份 | 意大利语“盾牌”安全防护应用（安全验证/权限合规工具），实际为 BingoMod 系银行木马（内嵌 bnl.apk、hibank.apk 银行钓鱼载荷） |
| 系统无障碍列表服务名 | 无独立标签，系统无障碍列表中仅显示应用名 Scudo App（service 未声明 android:label 与 android:description） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置伪造 isAccessibilityTool="true" 以冒充合规无障碍工具；service 缺失 android:label 与 android:description，使列表项无功能说明、警示被挤出；HTML 标题拼写错误为 AnroidRAA 与桌面名 Scudo App 不一致；多个 AppTheme.Transparent 透明 Activity（p9d04afb5/p87c443d6/p7d6d99f8）可作无感跳转中转；跳转 action 与页面 URL 全部字符串加密 |
| 无障碍服务类名 | `p1a1fa04c.pae25061e.p658c02c8.pf5d1b764` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | p1a1fa04c.pae25061e.p658c02c8.p055ff792（LAUNCHER Activity，全屏 WebView） | onCreate 即执行：setContentView → 取 WebView → setJavaScriptEnabled(true) / setAllowFileAccess(true) → addJavascriptInterface(p4e273033, "Android") → loadUrl(解密后的本地 asset 地址) | 本地HTML WebView | **原文**：Aspetta un minuto, stiamo verificando la disponibilità della sicurezza per il tuo dispositivo.<br>**译注**：请稍等一分钟，我们正在验证你设备的安全可用性。 | 无需操作，纯等待（假安全检测进度条），页面无任何按钮或取消入口 | `p1a1fa04c.pae25061e.p658c02c8.p055ff792.onCreate / assets/indexloading.html` |
| 2 | 引导说明页 | 同一 WebView 切换至引导页（assets/index1.html），顶部 shield.png 盾牌图标 + 居中灰字说明 + 底部橙色描边按钮 | 加载流程切换到 index1.html 后由用户点击按钮 onclick="notifyButtonClick()" | 本地HTML WebView | **原文**：Per abilitare correttamente l'app è necessario consentire tutti i permessi.<br>Clicca sul pulsante "Prosegui" in basso per continuare.<br>**译注**：为了正确启用本应用，必须允许所有权限。请点击下方的“继续”按钮以继续。 | 只能点击唯一按钮 Prosegui（继续）；页面仅有一个按钮，无跳过、取消、稍后或关闭选项，返回键亦被 WebView setOnTouchListener 与全屏沉浸(768)削弱 | `assets/index1.html（h2.continue-text + button.continue-button onclick=notifyButtonClick）` |
| 3 | 跳受限设置 | 系统设置页（无障碍设置或应用详情页），由 p055ff792$p4e273033.onButtonClicked 通过 startActivity(Intent(action=加密字符串)) 拉起 | JS 桥回调 Android.onButtonClicked()（@JavascriptInterface，由 index1.html 按钮触发） | 系统无障碍页 | **原文**：无（应用侧不呈现文案，直接跳转系统页面；action 字面量存于加密字符串表，未逐字还原）<br>**译注**：应用不解释即将打开的系统页面用途，仅以“允许所有权限”笼统话术带过 | 用户在系统页手动找到 Scudo App 并打开开关；应用侧未提供任何权限用途说明或逐项解释 | `p1a1fa04c.pae25061e.p658c02c8.p055ff792$p4e273033.onButtonClicked → Intent.<init> + Context.startActivity` |
| 4 | 获权后动作 | 无障碍服务 p1a1fa04c.pae25061e.p658c02c8.pf5d1b764（typeAllMask、canRetrieveWindowContent、canTakeScreenshot、canPerformGestures、flagRequestFilterKeyEvents） | onServiceConnected 后 onAccessibilityEvent 持续接收事件，内部类 H / $20.run 等调用 getRootInActiveWindow、dispatchGesture、performGlobalAction | 不可静态还原 | **原文**：无（后台自动点击，不呈现 UI）<br>**译注**：无界面呈现，服务在后台读取窗口内容、注入手势点击并执行全局动作（返回/主页），可用于自动确认、阻断撤权与银行界面操作 | 无用户可见请求，权限一旦开启即由服务自动驱动界面 | `p1a1fa04c.pae25061e.p658c02c8.pf5d1b764.onServiceConnected / onAccessibilityEvent / H / $20.run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动全屏 WebView 加载的 assets/indexloading.html：居中灰字“正在验证设备安全可用性”+ 循环进度条（无按钮）
- 同一 WebView 切换的 assets/index1.html：顶部 shield.png 盾牌图标、居中灰字“必须允许所有权限”、底部固定橙色描边按钮 Prosegui（页面唯一交互元素）
- 系统无障碍设置列表：仅显示应用名 Scudo App，无 android:label、无 android:description，列表项不呈现任何功能说明
- res/values/strings.xml 的 device_admin_description：设备管理器激活页显示 “This app requires device administration privileges to perform certain functions.”
- 跳转系统设置页后应用侧不再叠加任何解释性文案或遮罩层（本次静态证据未发现 Overlay 引导窗实现）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| it | Per abilitare correttamente l'app è necessario consentire tutti i permessi.<br>Clicca sul pulsante "Prosegui" in basso per continuare. | 为了正确启用本应用，必须允许所有权限。请点击下方的“继续”按钮以继续。 | `assets/index1.html 中 h2.continue-text` | 受限设置分步教学 |
| it | Prosegui | 继续 | `assets/index1.html 中 button.continue-button` | 受限设置分步教学 |
| it | Aspetta un minuto, stiamo verificando la disponibilità della sicurezza per il tuo dispositivo. | 请稍等一分钟，我们正在验证你设备的安全可用性。 | `assets/indexloading.html 中 div.loading-text` | 假反诈安全 |
| en | AnroidRAA | AnroidRAA（拼写错误的“Android RAA”，用作页面标题） | `assets/index1.html 与 assets/indexloading.html 的 <title>` | 假反诈安全 |
| en | This app requires device administration privileges to perform certain functions. | 本应用需要设备管理权限以执行某些功能。 | `res/values/strings.xml: device_admin_description` | 良性透明说明 |
| zh | 不在允许的范围内：%1$s | 不在允许的范围内：%1$s | `res/values-zh-rCN/strings.xml（预筛线索，具体键名未逐一确认）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：引导页为唯一入口：index1.html 仅有一个 Prosegui 按钮，无取消/跳过；WebView 设置 setLongClickable(false)、setOnTouchListener 拦截并关闭滚动条，配合全屏沉浸(systemUiVisibility=768)与黑色状态栏/导航栏削弱退出路径；用户从系统设置返回后仍停留在同一 WebView 引导页，需再次点 Prosegui 才会重新 startActivity 跳转（onButtonClicked 无状态判断，未发现 onResume 定时死循环的直接证据）
- **遮罩叠层 / 高仿系统设置页**：未发现悬浮窗 Overlay 遮罩或高仿系统无障碍开关页；应用侧以全屏本地 WebView 承载全部引导文案，跳转后交由真实系统页，但多个 AppTheme.Transparent 透明 Activity 可用于无感中转
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未发现应用详情页右上角菜单允许受限设置的图文教学，也无 Session 安装器绕过路径；仅笼统要求“允许所有权限”）
- **获权后即时行为与防撤权机制**：服务内部类（H、$20.run、$8.run、D 等）调用 performGlobalAction（含 GLOBAL_ACTION_BACK/HOME 能力）与 dispatchGesture 自动点击，可在系统设置页代点确认或弹回，形成撤权干扰；未发现显式监听设置页后强制返回的独立判定代码
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳时机为 p055ff792（LAUNCHER Activity）onCreate 后 WebView 首次渲染出盾牌图标的瞬间，即冷启动 0 步；次优时机为监测到 WebView 内 Prosegui 按钮被点击引发的 startActivity（Intent 指向 android.settings.* 时）立即在设置页截图并同步抓取无障碍服务列表项
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：文案全部为意大利语本地 HTML 纯文本，无需 OCR；主要盲区是 Intent action 字符串与 asset 路径经自定义字符串加密表保护，纯文本匹配抓不到 android.settings.ACCESSIBILITY_SETTINGS 等字面量，需靠“WebView 按钮点击后立即出现系统设置页”的行为序列判定；另服务无 label/description，基于文本特征的检测可能漏判为空壳无障碍服务

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动假安全检测页** | 全屏 WebView，页面标题 AnroidRAA，中央盾牌图片 + 灰字“Aspetta un minuto…verificando la disponibilità della sicurezza” + 蓝色循环进度条，无任何按钮 | 证明应用以“安全检测”名义冷启动即拦截用户，而非提供真实功能，是诱导链起点 | 页面无按钮无取消，仅加载文案；标题 AnroidRAA 与应用名 Scudo App 不一致；本地 file:///android_asset 渲染、无地址栏 |
| **跳转前 WebView 权限引导页** | 同一 WebView 内容切换为盾牌图标 + “Per abilitare correttamente l'app è necessario consentire tutti i permessi” + 底部橙色描边 Prosegui 按钮 | 这是诱导无障碍/受限权限的核心页：唯一可点元素就是“继续”，无跳过，话术只讲“允许所有权限”不说明用途 | 界面仅 1 个可点击按钮（Prosegui）；无跳过/取消/稍后节点；文案未出现任何权限具体用途说明 |
| **系统无障碍设置页与服务列表项** | 跳转后立即截图：Settings 无障碍页，列表项文本为 Scudo App，无子标题描述；点入后开关页显示空描述 | 直接暴露“无 description + 伪造 isAccessibilityTool”造成的警示缺失，是区分恶意与良性无障碍工具的关键判据 | 列表项无 description 文本节点；应用名与页面宣称身份不一致；从诱导页到本页的跳转耗时极短（同一 Activity 直接 startActivity） |
| **获权后自动点击行为** | 开启开关后服务连接，界面出现非用户触发的点击/返回（系统设置页被自动返回或开关被代点） | 证明无障碍权限被用于模拟点击而非辅助功能，可佐证反撤权与银行界面自动操作 | 开关状态在无用户输入下改变；页面被自动返回或跳出；无任何无障碍辅助交互反馈（朗读/焦点提示） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `p1a1fa04c.pae25061e.p658c02c8.p055ff792.onCreate`
- `p1a1fa04c.pae25061e.p658c02c8.p055ff792$p4e273033.onButtonClicked`
- `p1a1fa04c.pae25061e.p658c02c8.pf5d1b764.onServiceConnected`
- `p1a1fa04c.pae25061e.p658c02c8.pf5d1b764.onAccessibilityEvent`
- `assets/index1.html`
- `res/xml/accessibility_service_description.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，13 次工具调用内收口）

**样本性质确认：** 这是一个 BingoMod 系银行木马，它通过本地 HTML 诱导页和系统无障碍设置跳转来获取无障碍权限。无障碍服务本身具备全量事件监听、读取窗口内容、截图、手势注入和按键过滤能力。

**关键事实：**

1. **冷启动入口**：[p055ff792.onCreate()](<resource-unit:#1.dex1 code:p1a1fa04c.pae25061e.p658c02c8.p055ff792#onCreate>) 是 LAUNCHER Activity。它在 onCreate 中创建全屏 WebView，开启 JavaScript 和 file 访问，把导航栏和状态栏置黑，并禁用长按和滚动条。随后它通过 `loadUrl(解密字符串)` 加载 `assets/` 下的本地 HTML，同时通过 `addJavascriptInterface(new p4e273033(this), 解密名)` 注入名为 `Android` 的桥。

2. **引导页为意大利语本地 HTML**：[assets/index1.html (lines 90-103)](<resource-unit:#1 file:assets/index1.html#L90-L103>) 使用 `shield.png` 盾牌图标，页面标题为拼写错误的 `AnroidRAA`，正文要求用户“必须允许所有权限”，并提示点击下方 **Prosegui** 按钮。**页面中没有任何“跳过、取消或稍后”按钮**。按钮 onclick 会调用 `Android.onButtonClicked()`。另一页 [assets/indexloading.html (lines 137-142)](<resource-unit:#1 file:assets/indexloading.html#L137-L142>) 显示“正在验证你设备的安全可用性”，属于典型的假安全检测文案。

3. **跳转点**：[p055ff792$p4e273033.onButtonClicked()](<resource-unit:#1.dex1 code:p1a1fa04c.pae25061e.p658c02c8.p055ff792$p4e273033#onButtonClicked>) 带有 `@JavascriptInterface` 注解。该方法只做一件事：用加密字符串构造 `Intent(action=…)`，然后调用 `startActivity(intent)`，把用户送到系统设置页。`classes.dex` 的明文区**不含** `ACCESSIBILITY_SETTINGS` 或 `APPLICATION_DETAILS_SETTINGS` 字样。action 字符串与页面 URL 都来自自定义字符串加密表（`String[] a` 分块密文 + `pd8097feb$pefc6dad5$p9fab99f0.a(long)` 解密），因此未能逐字还原出 action 字面量；但“点击引导按钮 → 直接跳到系统受限设置页”的控制流是确定的。

4. **系统无障碍列表中的呈现**：[res/xml/accessibility_service_description.xml](<resource-unit:#1 file:res/xml/accessibility_service_description.xml>) 把 `isAccessibilityTool="true"` 设为真，从而**伪造无障碍工具标记**；它使用 `typeAllMask`、`flagRetrieveInteractiveWindows`、`flagRequestFilterKeyEvents`、`canTakeScreenshot`、`canPerformGestures`，并声明 `canRetrieveWindowContent`。Manifest 中该 service 没有 `android:label` 和 `android:description`，所以列表里只显示应用名 `Scudo App`（“盾牌 App”），没有功能说明，从而进一步弱化警示。**这就是“空白挤出警告”的实际实现方式：缺少 label 和 description，并搭配 isAccessibilityTool 伪标记**。

5. **获权后动作**：[pf5d1b764.onServiceConnected()](<resource-unit:#1.dex1 code:p1a1fa04c.pae25061e.p658c02c8.pf5d1b764#onServiceConnected>) 和 `onAccessibilityEvent` 会驱动 `getRootInActiveWindow`、`dispatchGesture`、`performGlobalAction` 等调用（共 9 个内部类都注入手势），用于自动点击，并阻断用户返回。`assets/bnl.apk`（5.4MB）与 `assets/hibank.apk`（5.4MB）是内嵌的意大利银行覆盖或钓鱼载荷；Manifest 还同时申请了 `READ_SMS/SEND_SMS/RECEIVE_SMS`、`REQUEST_INSTALL_PACKAGES`、`WRITE_SETTINGS` 和 DeviceAdmin 接收器。

6. **身份不一致**：应用名为 `Scudo App`，HTML 标题为 `AnroidRAA`，声称是安全工具，实际却是银行木马；无障碍服务没有任何功能描述。此外还有多个 `AppTheme.Transparent` 透明 Activity（`p9d04afb5`、`p87c443d6`、`p7d6d99f8`），可用于隐藏的跳转中转。

**证据边界：** HTML、Manifest、无障碍配置和 JS 桥完全静态可见；跳转的 action 字面量与部分引导文案封装在 DEX 字符串加密表中（不是 VMP/壳），本次未逐字解密，因此 `static_visibility` 记为 `partial_dynamic_or_remote`。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍服务配置、assets 本地 HTML 诱导页与 JS 桥调用链完全静态可见；但 onButtonClicked 内 Intent action 字符串、loadUrl 的 asset 路径与部分提示文案均经自定义字符串加密（String[] 分块密文表 + pd8097feb$pefc6dad5$p9fab99f0.a(long) 解密），未逐字还原，故跳转目标为无障碍设置页/应用详情页的精确 action 字面量未证实；无整体加壳、无远端下发 HTML",
  "summary_one_liner": "冷启动即以全屏 WebView 加载 assets 本地意大利语盾牌诱导页，无跳过按钮强制点 Prosegui，经 JavascriptInterface 直接 startActivity 跳系统设置页，并靠 isAccessibilityTool=true 与缺失 label/description 掩盖无障碍服务真实能力",
  "disguise_identity": {
    "app_display_name": "Scudo App",
    "claimed_brand_or_persona": "意大利语“盾牌”安全防护应用（安全验证/权限合规工具），实际为 BingoMod 系银行木马（内嵌 bnl.apk、hibank.apk 银行钓鱼载荷）",
    "a11y_service_label": "无独立标签，系统无障碍列表中仅显示应用名 Scudo App（service 未声明 android:label 与 android:description）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置伪造 isAccessibilityTool=\"true\" 以冒充合规无障碍工具；service 缺失 android:label 与 android:description，使列表项无功能说明、警示被挤出；HTML 标题拼写错误为 AnroidRAA 与桌面名 Scudo App 不一致；多个 AppTheme.Transparent 透明 Activity（p9d04afb5/p87c443d6/p7d6d99f8）可作无感跳转中转；跳转 action 与页面 URL 全部字符串加密"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "p1a1fa04c.pae25061e.p658c02c8.p055ff792（LAUNCHER Activity，全屏 WebView）",
      "trigger_event": "onCreate 即执行：setContentView → 取 WebView → setJavaScriptEnabled(true) / setAllowFileAccess(true) → addJavascriptInterface(p4e273033, \"Android\") → loadUrl(解密后的本地 asset 地址)",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Aspetta un minuto, stiamo verificando la disponibilità della sicurezza per il tuo dispositivo.",
      "shown_text_zh": "请稍等一分钟，我们正在验证你设备的安全可用性。",
      "user_action_requested": "无需操作，纯等待（假安全检测进度条），页面无任何按钮或取消入口",
      "code_anchor": "p1a1fa04c.pae25061e.p658c02c8.p055ff792.onCreate / assets/indexloading.html"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "同一 WebView 切换至引导页（assets/index1.html），顶部 shield.png 盾牌图标 + 居中灰字说明 + 底部橙色描边按钮",
      "trigger_event": "加载流程切换到 index1.html 后由用户点击按钮 onclick=\"notifyButtonClick()\"",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Per abilitare correttamente l'app è necessario consentire tutti i permessi.\nClicca sul pulsante \"Prosegui\" in basso per continuare.",
      "shown_text_zh": "为了正确启用本应用，必须允许所有权限。请点击下方的“继续”按钮以继续。",
      "user_action_requested": "只能点击唯一按钮 Prosegui（继续）；页面仅有一个按钮，无跳过、取消、稍后或关闭选项，返回键亦被 WebView setOnTouchListener 与全屏沉浸(768)削弱",
      "code_anchor": "assets/index1.html（h2.continue-text + button.continue-button onclick=notifyButtonClick）"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置页（无障碍设置或应用详情页），由 p055ff792$p4e273033.onButtonClicked 通过 startActivity(Intent(action=加密字符串)) 拉起",
      "trigger_event": "JS 桥回调 Android.onButtonClicked()（@JavascriptInterface，由 index1.html 按钮触发）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧不呈现文案，直接跳转系统页面；action 字面量存于加密字符串表，未逐字还原）",
      "shown_text_zh": "应用不解释即将打开的系统页面用途，仅以“允许所有权限”笼统话术带过",
      "user_action_requested": "用户在系统页手动找到 Scudo App 并打开开关；应用侧未提供任何权限用途说明或逐项解释",
      "code_anchor": "p1a1fa04c.pae25061e.p658c02c8.p055ff792$p4e273033.onButtonClicked → Intent.<init> + Context.startActivity"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 p1a1fa04c.pae25061e.p658c02c8.pf5d1b764（typeAllMask、canRetrieveWindowContent、canTakeScreenshot、canPerformGestures、flagRequestFilterKeyEvents）",
      "trigger_event": "onServiceConnected 后 onAccessibilityEvent 持续接收事件，内部类 H / $20.run 等调用 getRootInActiveWindow、dispatchGesture、performGlobalAction",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（后台自动点击，不呈现 UI）",
      "shown_text_zh": "无界面呈现，服务在后台读取窗口内容、注入手势点击并执行全局动作（返回/主页），可用于自动确认、阻断撤权与银行界面操作",
      "user_action_requested": "无用户可见请求，权限一旦开启即由服务自动驱动界面",
      "code_anchor": "p1a1fa04c.pae25061e.p658c02c8.pf5d1b764.onServiceConnected / onAccessibilityEvent / H / $20.run"
    }
  ],
  "text_presentation_locations": [
    "冷启动全屏 WebView 加载的 assets/indexloading.html：居中灰字“正在验证设备安全可用性”+ 循环进度条（无按钮）",
    "同一 WebView 切换的 assets/index1.html：顶部 shield.png 盾牌图标、居中灰字“必须允许所有权限”、底部固定橙色描边按钮 Prosegui（页面唯一交互元素）",
    "系统无障碍设置列表：仅显示应用名 Scudo App，无 android:label、无 android:description，列表项不呈现任何功能说明",
    "res/values/strings.xml 的 device_admin_description：设备管理器激活页显示 “This app requires device administration privileges to perform certain functions.”",
    "跳转系统设置页后应用侧不再叠加任何解释性文案或遮罩层（本次静态证据未发现 Overlay 引导窗实现）"
  ],
  "verbatim_texts": [
    {
      "lang": "it",
      "text_verbatim": "Per abilitare correttamente l'app è necessario consentire tutti i permessi.\nClicca sul pulsante \"Prosegui\" in basso per continuare.",
      "text_zh": "为了正确启用本应用，必须允许所有权限。请点击下方的“继续”按钮以继续。",
      "source_location": "assets/index1.html 中 h2.continue-text",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "it",
      "text_verbatim": "Prosegui",
      "text_zh": "继续",
      "source_location": "assets/index1.html 中 button.continue-button",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "it",
      "text_verbatim": "Aspetta un minuto, stiamo verificando la disponibilità della sicurezza per il tuo dispositivo.",
      "text_zh": "请稍等一分钟，我们正在验证你设备的安全可用性。",
      "source_location": "assets/indexloading.html 中 div.loading-text",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "AnroidRAA",
      "text_zh": "AnroidRAA（拼写错误的“Android RAA”，用作页面标题）",
      "source_location": "assets/index1.html 与 assets/indexloading.html 的 <title>",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "This app requires device administration privileges to perform certain functions.",
      "text_zh": "本应用需要设备管理权限以执行某些功能。",
      "source_location": "res/values/strings.xml: device_admin_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "不在允许的范围内：%1$s",
      "text_zh": "不在允许的范围内：%1$s",
      "source_location": "res/values-zh-rCN/strings.xml（预筛线索，具体键名未逐一确认）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "引导页为唯一入口：index1.html 仅有一个 Prosegui 按钮，无取消/跳过；WebView 设置 setLongClickable(false)、setOnTouchListener 拦截并关闭滚动条，配合全屏沉浸(systemUiVisibility=768)与黑色状态栏/导航栏削弱退出路径；用户从系统设置返回后仍停留在同一 WebView 引导页，需再次点 Prosegui 才会重新 startActivity 跳转（onButtonClicked 无状态判断，未发现 onResume 定时死循环的直接证据）",
    "overlay_or_fake_settings": "未发现悬浮窗 Overlay 遮罩或高仿系统无障碍开关页；应用侧以全屏本地 WebView 承载全部引导文案，跳转后交由真实系统页，但多个 AppTheme.Transparent 透明 Activity 可用于无感中转",
    "restricted_settings_13plus_coaching": "无（未发现应用详情页右上角菜单允许受限设置的图文教学，也无 Session 安装器绕过路径；仅笼统要求“允许所有权限”）",
    "post_grant_anti_removal": "服务内部类（H、$20.run、$8.run、D 等）调用 performGlobalAction（含 GLOBAL_ACTION_BACK/HOME 能力）与 dispatchGesture 自动点击，可在系统设置页代点确认或弹回，形成撤权干扰；未发现显式监听设置页后强制返回的独立判定代码",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳时机为 p055ff792（LAUNCHER Activity）onCreate 后 WebView 首次渲染出盾牌图标的瞬间，即冷启动 0 步；次优时机为监测到 WebView 内 Prosegui 按钮被点击引发的 startActivity（Intent 指向 android.settings.* 时）立即在设置页截图并同步抓取无障碍服务列表项",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动假安全检测页",
        "page_identifier": "全屏 WebView，页面标题 AnroidRAA，中央盾牌图片 + 灰字“Aspetta un minuto…verificando la disponibilità della sicurezza” + 蓝色循环进度条，无任何按钮",
        "why_most_useful": "证明应用以“安全检测”名义冷启动即拦截用户，而非提供真实功能，是诱导链起点",
        "observable_utg_signals": ["页面无按钮无取消，仅加载文案", "标题 AnroidRAA 与应用名 Scudo App 不一致", "本地 file:///android_asset 渲染、无地址栏"]
      },
      {
        "page_role": "跳转前 WebView 权限引导页",
        "page_identifier": "同一 WebView 内容切换为盾牌图标 + “Per abilitare correttamente l'app è necessario consentire tutti i permessi” + 底部橙色描边 Prosegui 按钮",
        "why_most_useful": "这是诱导无障碍/受限权限的核心页：唯一可点元素就是“继续”，无跳过，话术只讲“允许所有权限”不说明用途",
        "observable_utg_signals": ["界面仅 1 个可点击按钮（Prosegui）", "无跳过/取消/稍后节点", "文案未出现任何权限具体用途说明"]
      },
      {
        "page_role": "系统无障碍设置页与服务列表项",
        "page_identifier": "跳转后立即截图：Settings 无障碍页，列表项文本为 Scudo App，无子标题描述；点入后开关页显示空描述",
        "why_most_useful": "直接暴露“无 description + 伪造 isAccessibilityTool”造成的警示缺失，是区分恶意与良性无障碍工具的关键判据",
        "observable_utg_signals": ["列表项无 description 文本节点", "应用名与页面宣称身份不一致", "从诱导页到本页的跳转耗时极短（同一 Activity 直接 startActivity）"]
      },
      {
        "page_role": "获权后自动点击行为",
        "page_identifier": "开启开关后服务连接，界面出现非用户触发的点击/返回（系统设置页被自动返回或开关被代点）",
        "why_most_useful": "证明无障碍权限被用于模拟点击而非辅助功能，可佐证反撤权与银行界面自动操作",
        "observable_utg_signals": ["开关状态在无用户输入下改变", "页面被自动返回或跳出", "无任何无障碍辅助交互反馈（朗读/焦点提示）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "文案全部为意大利语本地 HTML 纯文本，无需 OCR；主要盲区是 Intent action 字符串与 asset 路径经自定义字符串加密表保护，纯文本匹配抓不到 android.settings.ACCESSIBILITY_SETTINGS 等字面量，需靠“WebView 按钮点击后立即出现系统设置页”的行为序列判定；另服务无 label/description，基于文本特征的检测可能漏判为空壳无障碍服务"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "p1a1fa04c.pae25061e.p658c02c8.p055ff792.onCreate",
    "p1a1fa04c.pae25061e.p658c02c8.p055ff792$p4e273033.onButtonClicked",
    "p1a1fa04c.pae25061e.p658c02c8.pf5d1b764.onServiceConnected",
    "p1a1fa04c.pae25061e.p658c02c8.pf5d1b764.onAccessibilityEvent",
    "assets/index1.html",
    "res/xml/accessibility_service_description.xml"
  ]
}
```

</details>
