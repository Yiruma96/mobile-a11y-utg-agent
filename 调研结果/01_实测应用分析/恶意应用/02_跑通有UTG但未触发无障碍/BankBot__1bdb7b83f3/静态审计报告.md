# MB_011__1bdb7b83f3｜BankBot — Asistan

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：146.6s

## 1. 一句话核心结论

- **核心申请方式**：以 Cordova 网页壳（桌面名 Asistan）通过通用 NativeSettings 插件从页面内静默跳转系统无障碍设置，并在列表中投放一个描述为空、仅显示土耳其语祈使句“Aktif Ediniz”的高危无障碍服务，真正实现藏于 AES 加密的二阶段 Dex 载荷。
- **静态可见性说明**：可见 dex 仅暴露通用 Cordova 插件分发器（NativeSettings 的 accessibility/application_details/battery_optimization 跳转）与无障碍服务在 Manifest 中的声明；无障碍服务类 spin.window.mobile.lyugp.qvxzpe 的实现、onAccessibilityEvent 逻辑、引导页面文案与拒绝后重跳策略均不在明文 dex 中。assets/uL.json（713992 字节，头部高熵随机字节）为加密载荷，配合 melt.pull.leg.STeScUbXqNfMkWo#spoildecide 反射构造 DexClassLoader 与 com.tkyaji.cordova.DecryptResource 的 AES/CBC 解密，判定为二阶段加密加载；应用层类名整体随机化，进一步阻碍静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1bdb7b83f3964b84d03694bbbc66a02f5a270043b8ac635932d9de12b81b172e` |
| 包名 / 年份 | `melt.pull.leg` / 2023 |
| 家族 / 品类 | **BankBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Asistan |
| 引导页宣称品牌/身份 | 伪装为通用助手/工具类应用（内部页面资源自称为 IG Plus，且内嵌广告与社交/云盘类页面模板） |
| 系统无障碍列表服务名 | Aktif Ediniz |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签为祈使句“Aktif Ediniz”（请将其激活）而非功能名，且 android:description 完全缺失，系统列表无任何用途说明；同一句“Aktif Ediniz”被复用到 DeviceAdmin receiver 标签，制造“必须激活”的一致性暗示；应用名 Asistan 与内部 app.xml 的 appname=IG Plus 不一致；全部类名随机化（melt.pull.leg.*、spin.window.mobile.* 无意义类名），关键实现迁入加密二阶段 Dex；未发现多 activity-alias 或多图标伪装。 |
| 无障碍服务类名 | `spin.window.mobile.lyugp.qvxzpe` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | melt.pull.leg.ZFlSyMqEeNo（android.app.Application）→ spin.window.mobile.gkab（LAUNCHER/SMS role） | attachBaseContext / onCreate（Application 初始化时解密 assets/uL.json 并加载二阶段 Dex） | 原生Activity | 无 | 无（自动执行） | `melt.pull.leg.ZFlSyMqEeNo#attachBaseContext / melt.pull.leg.STeScUbXqNfMkWo#spoildecide` |
| 2 | 冷启动入口 | com.electroneum.mobile.MainActivity（Cordova WebView 壳）+ assets/app.xml 页面清单 | onCreate 中 WebView loadUrl 本地 assets 页面（index/igpluspaso1..4 等） | 本地HTML WebView | **原文**：appname = "IG Plus"；页面标题 "Inicio"、"Tutoriales"、"Paso 1"、"Paso 2"、"Paso 3"、"Paso 4"<br>**译注**：页面名依次为“首页/教程/第 1 步…第 4 步”，提示存在分步教学式引导流程 | 浏览页面并点击引导入口（引导文案实体在加密二阶段或远端，明文不可见） | `com.electroneum.mobile.MainActivity#onCreate / assets/app.xml` |
| 3 | 引导说明页 | WebView 内页面 JS 调用 Cordova 插件 nativesettings | 页面脚本执行 cordova.exec(..., "accessibility")（由 Web 侧触发，非原生页面） | 本地HTML WebView | **原文**：无（文案位于加密载荷/远端页面，明文 dex 中不含）<br>**译注**：以“需要开启辅助功能/权限”类说明引导用户点击按钮 | 点击页面按钮进入系统设置；是否提供取消/跳过由加密阶段决定，明文不可确认 | `com.phonegap.plugins.nativesettings.NativeSettings#execute` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | NativeSettings.execute 中 string.equals("accessibility") 分支构造 Intent 并 startActivity | 系统无障碍页 | **原文**：intent = new Intent("android.settings.ACCESSIBILITY_SETTINGS");<br>**译注**：直接跳转系统“无障碍/已下载的服务”列表 | 要求用户在列表中自行找到并开启服务项（列表项名为“Aktif Ediniz”，无描述） | `com.phonegap.plugins.nativesettings.NativeSettings#execute` |
| 5 | 跳受限设置 | 系统设置页 android.settings.APPLICATION_DETAILS_SETTINGS（本应用详情） | 同一插件 execute 中 string.equals("application_details") 分支，数据为 package:<本应用包名> | 系统无障碍页 | **原文**：intent = new Intent("android.settings.APPLICATION_DETAILS_SETTINGS", uri);<br>**译注**：跳转本应用详情页，具备实施 Android 13+ 受限设置分步教学（右上角菜单→允许受限设置）的现成能力 | 在应用详情页开启受限设置（具体教学文案在加密阶段，明文不可确认） | `com.phonegap.plugins.nativesettings.NativeSettings#execute` |
| 6 | 跳受限设置 | 系统设置页 android.settings.IGNORE_BATTERY_OPTIMIZATION_SETTINGS | 插件 execute 中 string.equals("battery_optimization") 分支（对应声明权限 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS） | 系统无障碍页 | **原文**：intent = new Intent("android.settings.IGNORE_BATTERY_OPTIMIZATION_SETTINGS");<br>**译注**：引导关闭电池优化，保障后台常驻与后续窃取/远控链路不被系统清理 | 允许应用忽略电池优化 | `com.phonegap.plugins.nativesettings.NativeSettings#execute` |
| 7 | 获权后动作 | spin.window.mobile.lyugp.qvxzpe（BIND_ACCESSIBILITY_SERVICE，config=res/xml/wxgw.xml） | 用户手动开启后系统绑定服务，服务回调开始监听窗口内容/状态变化 | 不可静态还原 | **原文**：android:accessibilityEventTypes="typeWindowContentChanged\|typeWindowStateChanged" android:canRetrieveWindowContent="true"<br>**译注**：服务获取完整界面文本与控件树读取能力（典型用于读取银行/短信/支付界面并模拟点击） | 无（获权后自动运行，具体行为实现位于加密二阶段） | `res/xml/wxgw.xml / AndroidManifest.xml service spin.window.mobile.lyugp.qvxzpe` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- WebView 本地 HTML 页面（assets/app.xml 登记的 igpluspaso1.html ~ igpluspaso4.html 分步教学页；这些 html 未打包在 assets 中，实际由加密二阶段/远端提供）
- Cordova WebView 壳 com.electroneum.mobile.MainActivity 内加载的页面（assets/index.html、intro.html、menututoriales.html 等由 app.xml 定义）
- 系统无障碍服务列表项：标签“Aktif Ediniz”，android:description 缺失（无任何说明文字）
- 系统应用详情页（APPLICATION_DETAILS_SETTINGS，用于受限设置开启教学）
- 系统电池优化页（IGNORE_BATTERY_OPTIMIZATION_SETTINGS）
- DeviceAdmin 授权弹窗：receiver spin.window.mobile.wmmrh.osqrcezxrytkr 的 label 同为“Aktif Ediniz”
- assets/POLITICAS.html（AppModelo 隐私政策模板）与 assets/LICENSE.html、assets/CertificateWarning.html（通用模板页，非无障碍引导文案）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Aktif Ediniz | 请将其激活 | `AndroidManifest.xml：service spin.window.mobile.lyugp.qvxzpe 的 android:label；同时用于 receiver spin.window.mobile.wmmrh.osqrcezxrytkr` | 假更新 |
| en | intent = new Intent("android.settings.ACCESSIBILITY_SETTINGS"); | 构造跳转系统无障碍设置的 Intent | `com.phonegap.plugins.nativesettings.NativeSettings#execute` | 受限设置分步教学 |
| en | intent = new Intent("android.settings.APPLICATION_DETAILS_SETTINGS", uri); | 构造跳转本应用详情页的 Intent（用于开启受限设置） | `com.phonegap.plugins.nativesettings.NativeSettings#execute` | 受限设置分步教学 |
| en | android:accessibilityEventTypes="typeWindowContentChanged\|typeWindowStateChanged" android:accessibilityFlags="flagDefault\|flagIncludeNotImportantViews\|flagReportViewIds" android:canRetrieveWindowContent="true" | 监听窗口内容与窗口状态变化，可读取窗口内容并上报 View ID | `res/xml/wxgw.xml` | 未知 |
| es | AppModelo Políticas de Privacidad Nos damos cuenta de que la privacidad de su información personal es importante. | AppModelo 隐私政策：我们认识到您个人信息的隐私很重要。 | `assets/POLITICAS.html` | 隐私承诺 |
| en | IG Plus | IG Plus（内部页面资源中的应用名） | `assets/app.xml：<prop id="appname">IG Plus</prop>` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：明文代码仅见一次性 startActivity 跳转，无 onResume 计数或定时器重跳实现；拒绝/返回后的循环逻辑（是否死循环重跳）位于 AES 加密的二阶段 Dex 中，静态不可确认
- **遮罩叠层 / 高仿系统设置页**：未发现自绘高仿无障碍开关页或悬浮引导遮罩（应用主题为 Theme.Translucent.NoTitleBar、含多个 Theme.NoDisplay/excludeFromRecents 的 cimtbvqevr 页面，具备透明覆盖能力但无静态证据表明用于设置页叠层）
- **Android 13+ 受限设置（Restricted Settings）应对**：存在现成能力：NativeSettings.execute 支持跳转 android.settings.APPLICATION_DETAILS_SETTINGS（本应用详情页），可用于 Android 13+ 受限设置开启教学；教学文案本身在加密阶段，未见 Session 安装器绕过
- **获权后即时行为与防撤权机制**：未发现静态证据（无 GLOBAL_ACTION_BACK/HOME 监听、无自点确认代码在明文 dex 中）；但 Manifest 部署了 BIND_DEVICE_ADMIN receiver（label 同为“Aktif Ediniz”）与 RECEIVE_BOOT_COMPLETED/USER_PRESENT 广播，具备抗卸载与开机复活结构，实际撤权对抗逻辑可能在加密阶段
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：Hook android.content.Context.startActivity / Instrumentation 监测 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间，并在跳转前 300ms 抓取 WebView 当前页面；同时 hook Cordova exec 参数（action=nativesettings）以获取页面侧调用链
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：无障碍服务实现、引导文案与拒绝循环逻辑位于 assets/uL.json（713992 字节高熵密文）经 AES 解密 + DexClassLoader 加载的二阶段载荷中，纯静态 UTG 无法取到其页面文本与条件开关；app.xml 登记的 igpluspaso1~4 引导页 HTML 未打包在 assets 内，运行期需联网或解密后生成，因此必须在运行期捕获跳转瞬间的 WebView 页面才能取到诱导原文。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前 WebView 教学页（igpluspaso1~4 / intro / menututoriales）** | com.electroneum.mobile.MainActivity 内 WebView，URL 为 file:///android_asset/... 或远端 http(s) 页面，页面含“开启辅助功能/激活服务”按钮 | 此处是用户被诱导的唯一说明来源，文案决定是良性说明还是伪装/恐吓式引导 | 页面文本中是否出现辅助功能/无障碍/激活服务等词；是否提供取消/稍后/跳过按钮；是否伪装系统弹窗样式或品牌图标；是否含“点右上角菜单允许受限设置”字样 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页，服务项名“Aktif Ediniz”，描述为空 | 直接验证身份错位：服务名是祈使句、无用途描述，且与桌面名 Asistan 不一致 | 服务列表项文本 Aktif Ediniz；描述区域为空；同页是否被透明 Activity 覆盖；是否出现应用自绘遮罩 |
| **跳转落地后的叠层/返回反馈页** | spin.window.mobile.cimtbvqevr.* 中 theme=Theme.NoDisplay、excludeFromRecents、label 为空的 Activity | 用于确认是否存在设置页压栈遮罩、透明覆盖或返回后立即重跳的拒绝循环 | 设置页上方是否叠加透明窗口；返回键后是否立即再次进入 ACCESSIBILITY_SETTINGS；屏幕内容是否被自定义视图替换 |
| **冷启动首屏** | spin.window.mobile.gkab（LAUNCHER，含 role.SMS）启动后的首帧 | 确认引导是否为冷启动 0 步强制弹出（无取消），这是判定强制引导的关键 | 首屏是否直接出现权限引导；是否存在可关闭控件；是否先展示正常业务页面再弹引导 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.phonegap.plugins.nativesettings.NativeSettings#execute`
- `spin.window.mobile.lyugp.qvxzpe（AndroidManifest.xml service，BIND_ACCESSIBILITY_SERVICE）`
- `res/xml/wxgw.xml`
- `melt.pull.leg.STeScUbXqNfMkWo#spoildecide`
- `melt.pull.leg.ZFlSyMqEeNo#attachBaseContext`
- `com.electroneum.mobile.MainActivity#onCreate / assets/app.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（简要）

- **载体与技术栈**：Cordova/PhoneGap 混合应用，入口为 [spin.window.mobile.gkab](<resource-unit:#1 manifest:components>)（`MAIN`+`LAUNCHER`+`role.SMS`），WebView 侧由 `com.electroneum.mobile.MainActivity` 与 `assets/app.xml`（页面清单 `index/radio1/igpluspaso1..4`）驱动。
- **跳转能力来自通用插件**：[NativeSettings.execute()](<resource-unit:#1.dex1 code:com.phonegap.plugins.nativesettings.NativeSettings#execute>) 按 JS 传入的参数名构造 Intent，其中 `"accessibility"` → `android.settings.ACCESSIBILITY_SETTINGS`，`"application_details"` → `android.settings.APPLICATION_DETAILS_SETTINGS`（可承载 Android 13+ 受限设置教学），`"battery_optimization"` → `IGNORE_BATTERY_OPTIMIZATION_SETTINGS`。这是**运行期由 Web 页触发的动态跳转**，静态代码中只有“分发器”，具体文案在页面 JS/HTML 里。
- **无障碍服务本身极度可疑**：Manifest 声明 [spin.window.mobile.lyugp.qvxzpe](<resource-unit:#1 manifest:components>)（`BIND_ACCESSIBILITY_SERVICE`），标签为 `Aktif Ediniz`（土耳其语“请将其激活”），`android:description` 为空，配置 [res/xml/wxgw.xml](<resource-unit:#1 file:res/xml/wxgw.xml>) 申请 `canRetrieveWindowContent=true` 与 `typeWindowContentChanged|typeWindowStateChanged`（读屏内容+窗口切换，典型银行木马/短信窃取所需的强能力），却**没有任何正当辅助功能声明**。
- **身份错位**：桌面名 `Asistan`，无障碍列表项名 `Aktif Ediniz`（一句祈使句，不像服务名），且 `app.xml` 内 `appname` 为 `IG Plus`，广告配置指向 AdMob；另有一个 `label="Aktif Ediniz"` 的 DeviceAdmin receiver（`spin.window.mobile.wmmrh.osqrcezxrytkr`），与无障碍标签复用同一句话，诱导一致性明显。
- **静态可见性受限**：应用类名全部随机化（`melt.pull.leg.*`、`spin.window.mobile.*` 大量无意义类名），无障碍服务类与 `onAccessibilityEvent` 实现**不在可见 dex 中**；`assets/uL.json`（713,992 字节）头部为高熵随机字节，配合 [STeScUbXqNfMkWo#spoildecide](<resource-unit:#1.dex1 code:melt.pull.leg.STeScUbXqNfMkWo#spoildecide>) 反射构造 `DexClassLoader`、以及 `com.tkyaji.cordova.DecryptResource` 的 AES/CBC 解密，可判定为**二阶段加密载荷**，引导文案、拒绝后重跳逻辑、获权后动作均在该密文阶段。
- **UTG 视角要点**：最稳定的捕获瞬间是 WebView 页面触发 `nativesettings.accessibility` 跳转前的一帧，以及跳转落地后的系统无障碍列表页（服务项名 `Aktif Ediniz`、描述为空）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "可见 dex 仅暴露通用 Cordova 插件分发器（NativeSettings 的 accessibility/application_details/battery_optimization 跳转）与无障碍服务在 Manifest 中的声明；无障碍服务类 spin.window.mobile.lyugp.qvxzpe 的实现、onAccessibilityEvent 逻辑、引导页面文案与拒绝后重跳策略均不在明文 dex 中。assets/uL.json（713992 字节，头部高熵随机字节）为加密载荷，配合 melt.pull.leg.STeScUbXqNfMkWo#spoildecide 反射构造 DexClassLoader 与 com.tkyaji.cordova.DecryptResource 的 AES/CBC 解密，判定为二阶段加密加载；应用层类名整体随机化，进一步阻碍静态还原。",
  "summary_one_liner": "以 Cordova 网页壳（桌面名 Asistan）通过通用 NativeSettings 插件从页面内静默跳转系统无障碍设置，并在列表中投放一个描述为空、仅显示土耳其语祈使句“Aktif Ediniz”的高危无障碍服务，真正实现藏于 AES 加密的二阶段 Dex 载荷。",
  "disguise_identity": {
    "app_display_name": "Asistan",
    "claimed_brand_or_persona": "伪装为通用助手/工具类应用（内部页面资源自称为 IG Plus，且内嵌广告与社交/云盘类页面模板）",
    "a11y_service_label": "Aktif Ediniz",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签为祈使句“Aktif Ediniz”（请将其激活）而非功能名，且 android:description 完全缺失，系统列表无任何用途说明；同一句“Aktif Ediniz”被复用到 DeviceAdmin receiver 标签，制造“必须激活”的一致性暗示；应用名 Asistan 与内部 app.xml 的 appname=IG Plus 不一致；全部类名随机化（melt.pull.leg.*、spin.window.mobile.* 无意义类名），关键实现迁入加密二阶段 Dex；未发现多 activity-alias 或多图标伪装。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "melt.pull.leg.ZFlSyMqEeNo（android.app.Application）→ spin.window.mobile.gkab（LAUNCHER/SMS role）",
      "trigger_event": "attachBaseContext / onCreate（Application 初始化时解密 assets/uL.json 并加载二阶段 Dex）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此步无可视界面，仅完成环境初始化与二阶段载荷装载",
      "user_action_requested": "无（自动执行）",
      "code_anchor": "melt.pull.leg.ZFlSyMqEeNo#attachBaseContext / melt.pull.leg.STeScUbXqNfMkWo#spoildecide"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.electroneum.mobile.MainActivity（Cordova WebView 壳）+ assets/app.xml 页面清单",
      "trigger_event": "onCreate 中 WebView loadUrl 本地 assets 页面（index/igpluspaso1..4 等）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "appname = \"IG Plus\"；页面标题 \"Inicio\"、\"Tutoriales\"、\"Paso 1\"、\"Paso 2\"、\"Paso 3\"、\"Paso 4\"",
      "shown_text_zh": "页面名依次为“首页/教程/第 1 步…第 4 步”，提示存在分步教学式引导流程",
      "user_action_requested": "浏览页面并点击引导入口（引导文案实体在加密二阶段或远端，明文不可见）",
      "code_anchor": "com.electroneum.mobile.MainActivity#onCreate / assets/app.xml"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "WebView 内页面 JS 调用 Cordova 插件 nativesettings",
      "trigger_event": "页面脚本执行 cordova.exec(..., \"accessibility\")（由 Web 侧触发，非原生页面）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "无（文案位于加密载荷/远端页面，明文 dex 中不含）",
      "shown_text_zh": "以“需要开启辅助功能/权限”类说明引导用户点击按钮",
      "user_action_requested": "点击页面按钮进入系统设置；是否提供取消/跳过由加密阶段决定，明文不可确认",
      "code_anchor": "com.phonegap.plugins.nativesettings.NativeSettings#execute"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "NativeSettings.execute 中 string.equals(\"accessibility\") 分支构造 Intent 并 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "intent = new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\");",
      "shown_text_zh": "直接跳转系统“无障碍/已下载的服务”列表",
      "user_action_requested": "要求用户在列表中自行找到并开启服务项（列表项名为“Aktif Ediniz”，无描述）",
      "code_anchor": "com.phonegap.plugins.nativesettings.NativeSettings#execute"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置页 android.settings.APPLICATION_DETAILS_SETTINGS（本应用详情）",
      "trigger_event": "同一插件 execute 中 string.equals(\"application_details\") 分支，数据为 package:<本应用包名>",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "intent = new Intent(\"android.settings.APPLICATION_DETAILS_SETTINGS\", uri);",
      "shown_text_zh": "跳转本应用详情页，具备实施 Android 13+ 受限设置分步教学（右上角菜单→允许受限设置）的现成能力",
      "user_action_requested": "在应用详情页开启受限设置（具体教学文案在加密阶段，明文不可确认）",
      "code_anchor": "com.phonegap.plugins.nativesettings.NativeSettings#execute"
    },
    {
      "step": 6,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置页 android.settings.IGNORE_BATTERY_OPTIMIZATION_SETTINGS",
      "trigger_event": "插件 execute 中 string.equals(\"battery_optimization\") 分支（对应声明权限 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "intent = new Intent(\"android.settings.IGNORE_BATTERY_OPTIMIZATION_SETTINGS\");",
      "shown_text_zh": "引导关闭电池优化，保障后台常驻与后续窃取/远控链路不被系统清理",
      "user_action_requested": "允许应用忽略电池优化",
      "code_anchor": "com.phonegap.plugins.nativesettings.NativeSettings#execute"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "spin.window.mobile.lyugp.qvxzpe（BIND_ACCESSIBILITY_SERVICE，config=res/xml/wxgw.xml）",
      "trigger_event": "用户手动开启后系统绑定服务，服务回调开始监听窗口内容/状态变化",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "android:accessibilityEventTypes=\"typeWindowContentChanged|typeWindowStateChanged\" android:canRetrieveWindowContent=\"true\"",
      "shown_text_zh": "服务获取完整界面文本与控件树读取能力（典型用于读取银行/短信/支付界面并模拟点击）",
      "user_action_requested": "无（获权后自动运行，具体行为实现位于加密二阶段）",
      "code_anchor": "res/xml/wxgw.xml / AndroidManifest.xml service spin.window.mobile.lyugp.qvxzpe"
    }
  ],
  "text_presentation_locations": [
    "WebView 本地 HTML 页面（assets/app.xml 登记的 igpluspaso1.html ~ igpluspaso4.html 分步教学页；这些 html 未打包在 assets 中，实际由加密二阶段/远端提供）",
    "Cordova WebView 壳 com.electroneum.mobile.MainActivity 内加载的页面（assets/index.html、intro.html、menututoriales.html 等由 app.xml 定义）",
    "系统无障碍服务列表项：标签“Aktif Ediniz”，android:description 缺失（无任何说明文字）",
    "系统应用详情页（APPLICATION_DETAILS_SETTINGS，用于受限设置开启教学）",
    "系统电池优化页（IGNORE_BATTERY_OPTIMIZATION_SETTINGS）",
    "DeviceAdmin 授权弹窗：receiver spin.window.mobile.wmmrh.osqrcezxrytkr 的 label 同为“Aktif Ediniz”",
    "assets/POLITICAS.html（AppModelo 隐私政策模板）与 assets/LICENSE.html、assets/CertificateWarning.html（通用模板页，非无障碍引导文案）"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Aktif Ediniz",
      "text_zh": "请将其激活",
      "source_location": "AndroidManifest.xml：service spin.window.mobile.lyugp.qvxzpe 的 android:label；同时用于 receiver spin.window.mobile.wmmrh.osqrcezxrytkr",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "intent = new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\");",
      "text_zh": "构造跳转系统无障碍设置的 Intent",
      "source_location": "com.phonegap.plugins.nativesettings.NativeSettings#execute",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "intent = new Intent(\"android.settings.APPLICATION_DETAILS_SETTINGS\", uri);",
      "text_zh": "构造跳转本应用详情页的 Intent（用于开启受限设置）",
      "source_location": "com.phonegap.plugins.nativesettings.NativeSettings#execute",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "android:accessibilityEventTypes=\"typeWindowContentChanged|typeWindowStateChanged\" android:accessibilityFlags=\"flagDefault|flagIncludeNotImportantViews|flagReportViewIds\" android:canRetrieveWindowContent=\"true\"",
      "text_zh": "监听窗口内容与窗口状态变化，可读取窗口内容并上报 View ID",
      "source_location": "res/xml/wxgw.xml",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "es",
      "text_verbatim": "AppModelo Políticas de Privacidad Nos damos cuenta de que la privacidad de su información personal es importante.",
      "text_zh": "AppModelo 隐私政策：我们认识到您个人信息的隐私很重要。",
      "source_location": "assets/POLITICAS.html",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "IG Plus",
      "text_zh": "IG Plus（内部页面资源中的应用名）",
      "source_location": "assets/app.xml：<prop id=\"appname\">IG Plus</prop>",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "明文代码仅见一次性 startActivity 跳转，无 onResume 计数或定时器重跳实现；拒绝/返回后的循环逻辑（是否死循环重跳）位于 AES 加密的二阶段 Dex 中，静态不可确认",
    "overlay_or_fake_settings": "未发现自绘高仿无障碍开关页或悬浮引导遮罩（应用主题为 Theme.Translucent.NoTitleBar、含多个 Theme.NoDisplay/excludeFromRecents 的 cimtbvqevr 页面，具备透明覆盖能力但无静态证据表明用于设置页叠层）",
    "restricted_settings_13plus_coaching": "存在现成能力：NativeSettings.execute 支持跳转 android.settings.APPLICATION_DETAILS_SETTINGS（本应用详情页），可用于 Android 13+ 受限设置开启教学；教学文案本身在加密阶段，未见 Session 安装器绕过",
    "post_grant_anti_removal": "未发现静态证据（无 GLOBAL_ACTION_BACK/HOME 监听、无自点确认代码在明文 dex 中）；但 Manifest 部署了 BIND_DEVICE_ADMIN receiver（label 同为“Aktif Ediniz”）与 RECEIVE_BOOT_COMPLETED/USER_PRESENT 广播，具备抗卸载与开机复活结构，实际撤权对抗逻辑可能在加密阶段",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "Hook android.content.Context.startActivity / Instrumentation 监测 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间，并在跳转前 300ms 抓取 WebView 当前页面；同时 hook Cordova exec 参数（action=nativesettings）以获取页面侧调用链",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前 WebView 教学页（igpluspaso1~4 / intro / menututoriales）",
        "page_identifier": "com.electroneum.mobile.MainActivity 内 WebView，URL 为 file:///android_asset/... 或远端 http(s) 页面，页面含“开启辅助功能/激活服务”按钮",
        "why_most_useful": "此处是用户被诱导的唯一说明来源，文案决定是良性说明还是伪装/恐吓式引导",
        "observable_utg_signals": ["页面文本中是否出现辅助功能/无障碍/激活服务等词", "是否提供取消/稍后/跳过按钮", "是否伪装系统弹窗样式或品牌图标", "是否含“点右上角菜单允许受限设置”字样"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页，服务项名“Aktif Ediniz”，描述为空",
        "why_most_useful": "直接验证身份错位：服务名是祈使句、无用途描述，且与桌面名 Asistan 不一致",
        "observable_utg_signals": ["服务列表项文本 Aktif Ediniz", "描述区域为空", "同页是否被透明 Activity 覆盖", "是否出现应用自绘遮罩"]
      },
      {
        "page_role": "跳转落地后的叠层/返回反馈页",
        "page_identifier": "spin.window.mobile.cimtbvqevr.* 中 theme=Theme.NoDisplay、excludeFromRecents、label 为空的 Activity",
        "why_most_useful": "用于确认是否存在设置页压栈遮罩、透明覆盖或返回后立即重跳的拒绝循环",
        "observable_utg_signals": ["设置页上方是否叠加透明窗口", "返回键后是否立即再次进入 ACCESSIBILITY_SETTINGS", "屏幕内容是否被自定义视图替换"]
      },
      {
        "page_role": "冷启动首屏",
        "page_identifier": "spin.window.mobile.gkab（LAUNCHER，含 role.SMS）启动后的首帧",
        "why_most_useful": "确认引导是否为冷启动 0 步强制弹出（无取消），这是判定强制引导的关键",
        "observable_utg_signals": ["首屏是否直接出现权限引导", "是否存在可关闭控件", "是否先展示正常业务页面再弹引导"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：无障碍服务实现、引导文案与拒绝循环逻辑位于 assets/uL.json（713992 字节高熵密文）经 AES 解密 + DexClassLoader 加载的二阶段载荷中，纯静态 UTG 无法取到其页面文本与条件开关；app.xml 登记的 igpluspaso1~4 引导页 HTML 未打包在 assets 内，运行期需联网或解密后生成，因此必须在运行期捕获跳转瞬间的 WebView 页面才能取到诱导原文。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.phonegap.plugins.nativesettings.NativeSettings#execute",
    "spin.window.mobile.lyugp.qvxzpe（AndroidManifest.xml service，BIND_ACCESSIBILITY_SERVICE）",
    "res/xml/wxgw.xml",
    "melt.pull.leg.STeScUbXqNfMkWo#spoildecide",
    "melt.pull.leg.ZFlSyMqEeNo#attachBaseContext",
    "com.electroneum.mobile.MainActivity#onCreate / assets/app.xml"
  ]
}
```

</details>
