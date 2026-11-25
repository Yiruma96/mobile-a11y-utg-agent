# MR_125__64b9f19911｜EventBot — Posta Elettronica Certificata

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：131.6s

## 1. 一句话核心结论

- **核心申请方式**：以意大利法定电子邮箱 PEC 为伪装，用不可取消的 2003 型系统悬浮 AlertDialog 内嵌本地 HTML 图文教程，单按钮把用户直接甩进系统无障碍列表页，获权后立刻用全屏半透明 WebView 遮罩盖住界面。
- **静态可见性说明**：主 classes.dex 仅含加载器与 Manifest；无障碍引导 UI（弹窗、WebView 教程、跳设置、遮罩）全部位于 RC4 加密资源 assets/fonts/default.ttf 解出的二阶段 DEX（密钥为硬编码 cfg.gatePublicKey），本次已静态解密并完整还原，因此引导链 100% 可见；仅远控指令内容与后续注入脚本需云端下发，不影响无障碍诱导流程的判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `64b9f19911c2e4318048f81f2b32da7cbab0ce818594b2d181b323e0300a68ea` |
| 包名 / 年份 | `com.example.eventbot` / 2020 |
| 家族 / 品类 | **EventBot**（同池样本数：124） |
| 原始来源标识 | https://www.cybereason.com/blog/eventbot-a-new-mobile-banking-trojan-is-born |
| 桌面显示名 | Posta Elettronica Certificata |
| 引导页宣称品牌/身份 | Posta Elettronica Certificata（意大利邮政法定电子认证邮箱 PEC 服务） |
| 系统无障碍列表服务名 | Posta Elettronica Certificata |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务实现类为 com.example.eventbot.events、包名为 com.example.eventbot，与宣称的 PEC 品牌完全无关；服务 label 与 android:description 复用 @string/app_name 伪装；无空白/换行挤出、无同形字、无多 activity-alias；targetSdk 21 未使用 isAccessibilityTool 声明；引导文案不出现任何真实开发商信息 |
| 无障碍服务类名 | `com.example.eventbot.events` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | You must enable Posta Elettronica Certificata in order to get full functionality of the application. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.example.eventbot.MainActivity（LAUNCHER）→ com.example.eventbot.activity（theme FullScreen、无 ActionBar，仅含一个全屏 WebView splashView） | 用户点击桌面图标，MainActivity.onCreate → 启动 activity（Intent extra "mode" 决定后续界面形态） | 原生Activity | 无 | 无，被动进入 | `com.example.eventbot.MainActivity.onCreate；com.example.eventbot.activity.onCreate；res/layout/activity.xml(@id/splashView)` |
| 2 | 引导说明页 | 系统级 AlertDialog（window type=2003）+ 内嵌 WebView，内容取自 R.string.hint_text | activity.onCreate → service.Func.doActivity(...) → lib.doActivity → requestA11yAlert（a11yAlertVisible 去重） | 原生Dialog | **原文**：Posta Elettronica Certificata will not work correctly. / 1. Select Posta Elettronica Certificata in Settings / 2. Turn on it<br>**译注**：“Posta Elettronica Certificata 将无法正常工作。”然后分两步图文：1. 在设置中选择 Posta Elettronica Certificata；2. 将其打开 | 只有唯一按钮 “Open PEC”（setCancelable(false)，无取消/跳过/关闭按钮，点外部与返回键均不能关闭） | `com.lib#requestA11yAlert；res/values/strings.xml#hint_text / #hint_button` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表，其中列出 “Posta Elettronica Certificata”） | 用户点击 “Open PEC” → lib$3.onClick 执行 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(1409286144)) | 系统无障碍页 | **原文**：You must enable Posta Elettronica Certificata in order to get full functionality of the application.<br>**译注**：系统列表项说明：“您必须启用 Posta Elettronica Certificata 才能获得本应用的完整功能。” | 要求用户在该列表中手动找到同名条目并打开开关（flag 1409286144 = NEW_TASK\|CLEAR_TASK\|CLEAR_TOP，返回键不会回到应用引导页） | `com.lib$3#onClick；com.lib#requestA11y；res/xml/accessibility_config.xml(android:description=@string/accessibility_config_text)` |
| 4 | 拒权反馈循环 | 重复拉起的 AlertDialog / 系统设置页（isA11y 轮询检测） | lib.doAutorun、requestPermissions、parseCommand、makeKnockPacket 均先调用 isA11y(context, "events") 校验 getEnabledAccessibilityServiceList；未启用时再次 requestA11yAlert / requestA11y；无障碍事件回调 onAccessibilityEvent 亦持续拉起 service | 原生Dialog | **原文**：无（复用 step 2 的 hint_text 文案）<br>**译注**：未获权则重新弹出同一不可取消引导弹窗并再次跳设置页 | 反复要求开启无障碍开关，无降级路径 | `com.lib#isA11y；com.lib#doAutorun；com.example.eventbot.events#onAccessibilityEvent` |
| 5 | 遮罩叠层指引 | 全屏半透明 WebView 悬浮窗（WindowManager，type=2032 TYPE_APPLICATION_OVERLAY，flags 含 NOT_FOCUSABLE/NOT_TOUCHABLE 类位），叠加在当前前台界面之上 | 获权后 events.onServiceConnected → Func.minimizeAll → setServiceInfo → doAutorun → lib.createOverlay() | 悬浮窗Overlay | **原文**：System updating, please wait...<br>**译注**：“系统正在更新，请稍候……”（居中白字 + 旋转 spinner） | 要求用户原地等待，实际用于遮盖后续自动化注入与界面跳转 | `com.lib#createOverlay（overlay.loadData(getString(banner_text))）；res/values/strings.xml#banner_text` |
| 6 | 获权后动作 | com.example.eventbot.events（AccessibilityService）+ com.example.eventbot.service + 后台注入队列 libInterface$injectEvent | onServiceConnected 注册 injectEventQueue、setServiceInfo(makeA11yServiceInfo)、doAutorun；onAccessibilityEvent 将事件投入队列由二阶段库解析执行 | 不可静态还原 | 无 | 无需用户操作 | `com.example.eventbot.events#onServiceConnected；com.example.eventbot.events#onAccessibilityEvent；com.lib#doAutorun` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动 activity 弹出的 AlertDialog 内嵌 WebView：loadDataWithBaseURL("file:///android_asset/", getString(R.string.hint_text))，标题句 + 两步图文（1.jpg / 2.jpg 系统设置截图）
- 同一 AlertDialog 的唯一按钮文本：R.string.hint_button = "Open PEC"
- 系统无障碍服务列表项标题：android:label=@string/app_name = "Posta Elettronica Certificata"
- 系统无障碍服务列表项说明：res/xml/accessibility_config.xml android:description = "You must enable Posta Elettronica Certificata in order to get full functionality of the application."
- 获权后叠在屏幕上的全屏 WebView 遮罩：R.string.banner_text = "System updating, please wait..."
- assets/1.jpg、assets/2.jpg：真实系统“设置 → 无障碍 → 已下载服务”界面截图，用于纯图指引

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Posta Elettronica Certificata will not work correctly. | Posta Elettronica Certificata 将无法正常工作。 | `res/values/strings.xml key=hint_text` | 故障恐吓 |
| en | 1. Select Posta Elettronica Certificata in Settings | 1. 在设置中选择 Posta Elettronica Certificata | `res/values/strings.xml key=hint_text` | 受限设置分步教学 |
| en | 2. Turn on it | 2. 将其打开（打开开关） | `res/values/strings.xml key=hint_text` | 受限设置分步教学 |
| en | Open PEC | 打开 PEC | `res/values/strings.xml key=hint_button` | 受限设置分步教学 |
| en | You must enable Posta Elettronica Certificata in order to get full functionality of the application. | 您必须启用 Posta Elettronica Certificata 才能获得本应用的完整功能。 | `res/values/strings.xml key=accessibility_config_text（accessibility_config.xml android:description）` | 故障恐吓 |
| en | System updating, please wait... | 系统正在更新，请稍候…… | `res/values/strings.xml key=banner_text（lib.createOverlay 全屏遮罩）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：AlertDialog 为 setCancelable(false) 且仅有一个正向按钮，无法关闭；跳转使用 1409286144（NEW_TASK|CLEAR_TASK|CLEAR_TOP），返回键无法回到原应用；未授权时 lib.isA11y 在 doAutorun / requestPermissions / parseCommand / makeKnockPacket 中反复校验并重新弹窗跳设置；onAccessibilityEvent 每次事件都会拉起 service，形成持续重试。
- **遮罩叠层 / 高仿系统设置页**：是。引导弹窗本身是 window type=2003 的系统级悬浮 AlertDialog；获权后 createOverlay 再叠加 type=2032 的全屏半透明 WebView（WallpaperManager 背景 + "System updating, please wait..." spinner）盖住前台界面，实现设置页之后的遮罩式接管。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdk 21，未见“应用详情 → 右上角菜单 → 允许受限设置”教学，也未见 SESSION_INSTALLER 绕过；但存在对系统设置弹窗的注入自动点击（lib.requestOptimizationsIgnored / requestSmsAdmin 注入 com.android.settings 的 button1/button2 CLICK 事件）。
- **获权后即时行为与防撤权机制**：未发现监听设置页后自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权的显式逻辑；但 onKeyEvent→libInterface.BlockHardwareButtons 具备拦截硬件按键能力，配合全屏遮罩可妨碍用户回到设置撤权。
- **良性降级 / 替代方案**：无。无手动模式、无仅观看模式、无 ADB 替代路径，未授权即持续弹窗重跳。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间，或冷启动后 activity 创建约 15s（cfg.permissionsDelay=15）内出现的 type=2003 AlertDialog；此外无障碍服务 onServiceConnected 触发后约 1s 内出现的 type=2032 全屏 WebView 遮罩。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：一阶段主 DEX 仅有加载器与 Manifest，引导文案与跳转逻辑全在 RC4 加密的 assets/fonts/default.ttf 二阶段 DEX 中，纯静态浅层扫描会漏掉全部引导字符串；该文件以字体文件命名伪装，需按 RC4+硬编码密钥还原后才能取到 hint_text/hint_button/banner_text。运行期 UTG 不受此影响（解密后正常渲染）。此外教程含 1.jpg/2.jpg 系统截图，纯图部分需 OCR 才能读出引导内容。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（最关键）** | com.example.eventbot.activity 之上的 AlertDialog（window type=2003），内含 WebView 渲染的 “Posta Elettronica Certificata will not work correctly.” 与两张系统截图 | 该弹窗是唯一入口，且不可取消、无跳过按钮，可直接证明强制诱导与信息不对称（宣称功能故障而非安全授权） | 弹窗节点文本 'Posta Elettronica Certificata will not work correctly.'；唯一按钮文本 'Open PEC' 且无 cancel/关闭按钮节点；窗口层级为悬浮窗（非普通 Activity 内容），覆盖在启动页之上 |
| **跳转前 WebView 教学页（图文分步指引）** | 同一 AlertDialog 内 WebView，含 1.jpg / 2.jpg 两张系统设置截图与 '1. Select ...' '2. Turn on it' 文本 | 图文分步教学是“受限设置教学”类诱导的直接物证，且图片与文本可交叉验证引导目标就是无障碍开关 | 文本节点 '1. Select Posta Elettronica Certificata in Settings'；存在 image 节点（1.jpg/2.jpg 系统设置截图）；WebView 容器节点 className=android.webkit.WebView |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务 中的 'Posta Elettronica Certificata' 条目及其说明文字 | 确认服务标签与描述复用伪装品牌，且与真实包名 com.example.eventbot 明显不符 | 条目文本 'Posta Elettronica Certificata'；描述 'You must enable Posta Elettronica Certificata in order to get full functionality of the application.'；开关控件状态（未启用/已启用） |
| **设置页后的全屏压栈遮罩页** | 无障碍服务连接后出现的全屏 WebView 悬浮窗（type=2032，透明背景 + 壁纸），文本 'System updating, please wait...' 与旋转 spinner | 证明获权后立即接管屏幕、掩盖后续自动化行为，是“诱导成功后隐藏真实动作”的关键环节 | 文本节点 'System updating, please wait...'；窗口覆盖整个屏幕且不可点击（非焦点窗口）；出现在无障碍开关被打开后的 1-2 秒内 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.lib#requestA11yAlert`
- `com.lib$3#onClick`
- `com.lib#requestA11y`
- `com.lib#createOverlay`
- `com.example.eventbot.service#loadLib`
- `res/values/strings.xml#hint_text / #hint_button / #banner_text / #accessibility_config_text`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **无障碍授权链条的核心不在主 DEX 中**：主包 `classes.dex` 只是一个 4 KB 级的加载器，真正引导用户开启无障碍的 UI 逻辑位于 RC4 加密资源 `assets/fonts/default.ttf` 中，这段资源会解密为 `classes.dex` 并载入 `DexClassLoader`。我用 `cfg.gatePublicKey` 静态解出该二阶段 DEX（102 KB，23 个 `com.lib*` 类），因此整条引导链**静态可还原**，无需动态脱壳。
- **伪装身份**：桌面名、无障碍服务标签、无障碍描述全部复用同一意大利“Posta Elettronica Certificata”（法定电子认证邮箱）品牌名；实际是 EventBot 类短信/银行木马（`cfg.botnetID = "pec101"`，gate 域名 `ora.studiolegalebasili.com` 等）。
- **引导方式**：不是温和的说明页，而是 **不可取消的系统级悬浮 AlertDialog（`Window.setType(2003)`）+ 内嵌 WebView 分步图文教程 + 单一正向按钮**，点击后带着 `CLEAR_TASK` 类 flag 直接跳到系统无障碍列表页，不给返回原应用的路径。
- **教程载体是本地 HTML 字符串**（`res/values/strings.xml` 中的 `hint_text`），引用 `assets/1.jpg`、`assets/2.jpg` 两张真实系统设置截图，属于“受限设置分步教学 + 截图指引”的组合。
- **获权后立刻叠加遮罩**：`onServiceConnected` → `doAutorun` → `createOverlay` 用全屏半透明 WebView（`banner_text`："System updating, please wait..."）盖住用户界面，用于隐藏后续自动化操作。

主要证据节点：
- [com.example.eventbot.service#loadLib](<resource-unit:#1.dex1 code:com.example.eventbot.service#loadLib>) 从 `assets/fonts/default.ttf` 做 RC4 解密并 `DexClassLoader` 加载 `com.lib`
- [com.lib#requestA11yAlert](<resource-unit:<local_path> code:com.lib#requestA11yAlert>) 构建不可取消的 2003 型 AlertDialog + WebView 教程
- [com.lib$3#onClick](<resource-unit:<local_path> code:com.lib$3#onClick>) 点击 “Open PEC” 跳 `android.settings.ACCESSIBILITY_SETTINGS`
- [com.lib#createOverlay](<resource-unit:<local_path> code:com.lib#createOverlay>) 获权后 `banner_text` 全屏遮罩
- [res/values/strings.xml 的 hint_text / banner_text](<resource-unit:#1 file:res/values/strings.xml#L44-L46>)
- [res/xml/accessibility_config.xml](<resource-unit:#1 file:res/xml/accessibility_config.xml>)

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "主 classes.dex 仅含加载器与 Manifest；无障碍引导 UI（弹窗、WebView 教程、跳设置、遮罩）全部位于 RC4 加密资源 assets/fonts/default.ttf 解出的二阶段 DEX（密钥为硬编码 cfg.gatePublicKey），本次已静态解密并完整还原，因此引导链 100% 可见；仅远控指令内容与后续注入脚本需云端下发，不影响无障碍诱导流程的判定。",
  "summary_one_liner": "以意大利法定电子邮箱 PEC 为伪装，用不可取消的 2003 型系统悬浮 AlertDialog 内嵌本地 HTML 图文教程，单按钮把用户直接甩进系统无障碍列表页，获权后立刻用全屏半透明 WebView 遮罩盖住界面。",
  "disguise_identity": {
    "app_display_name": "Posta Elettronica Certificata",
    "claimed_brand_or_persona": "Posta Elettronica Certificata（意大利邮政法定电子认证邮箱 PEC 服务）",
    "a11y_service_label": "Posta Elettronica Certificata",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务实现类为 com.example.eventbot.events、包名为 com.example.eventbot，与宣称的 PEC 品牌完全无关；服务 label 与 android:description 复用 @string/app_name 伪装；无空白/换行挤出、无同形字、无多 activity-alias；targetSdk 21 未使用 isAccessibilityTool 声明；引导文案不出现任何真实开发商信息"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.example.eventbot.MainActivity（LAUNCHER）→ com.example.eventbot.activity（theme FullScreen、无 ActionBar，仅含一个全屏 WebView splashView）",
      "trigger_event": "用户点击桌面图标，MainActivity.onCreate → 启动 activity（Intent extra \"mode\" 决定后续界面形态）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "空白全屏 WebView 启动页，无任何文字",
      "user_action_requested": "无，被动进入",
      "code_anchor": "com.example.eventbot.MainActivity.onCreate；com.example.eventbot.activity.onCreate；res/layout/activity.xml(@id/splashView)"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "系统级 AlertDialog（window type=2003）+ 内嵌 WebView，内容取自 R.string.hint_text",
      "trigger_event": "activity.onCreate → service.Func.doActivity(...) → lib.doActivity → requestA11yAlert（a11yAlertVisible 去重）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Posta Elettronica Certificata will not work correctly. / 1. Select Posta Elettronica Certificata in Settings / 2. Turn on it",
      "shown_text_zh": "“Posta Elettronica Certificata 将无法正常工作。”然后分两步图文：1. 在设置中选择 Posta Elettronica Certificata；2. 将其打开",
      "user_action_requested": "只有唯一按钮 “Open PEC”（setCancelable(false)，无取消/跳过/关闭按钮，点外部与返回键均不能关闭）",
      "code_anchor": "com.lib#requestA11yAlert；res/values/strings.xml#hint_text / #hint_button"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表，其中列出 “Posta Elettronica Certificata”）",
      "trigger_event": "用户点击 “Open PEC” → lib$3.onClick 执行 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(1409286144))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "You must enable Posta Elettronica Certificata in order to get full functionality of the application.",
      "shown_text_zh": "系统列表项说明：“您必须启用 Posta Elettronica Certificata 才能获得本应用的完整功能。”",
      "user_action_requested": "要求用户在该列表中手动找到同名条目并打开开关（flag 1409286144 = NEW_TASK|CLEAR_TASK|CLEAR_TOP，返回键不会回到应用引导页）",
      "code_anchor": "com.lib$3#onClick；com.lib#requestA11y；res/xml/accessibility_config.xml(android:description=@string/accessibility_config_text)"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "重复拉起的 AlertDialog / 系统设置页（isA11y 轮询检测）",
      "trigger_event": "lib.doAutorun、requestPermissions、parseCommand、makeKnockPacket 均先调用 isA11y(context, \"events\") 校验 getEnabledAccessibilityServiceList；未启用时再次 requestA11yAlert / requestA11y；无障碍事件回调 onAccessibilityEvent 亦持续拉起 service",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无（复用 step 2 的 hint_text 文案）",
      "shown_text_zh": "未获权则重新弹出同一不可取消引导弹窗并再次跳设置页",
      "user_action_requested": "反复要求开启无障碍开关，无降级路径",
      "code_anchor": "com.lib#isA11y；com.lib#doAutorun；com.example.eventbot.events#onAccessibilityEvent"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "全屏半透明 WebView 悬浮窗（WindowManager，type=2032 TYPE_APPLICATION_OVERLAY，flags 含 NOT_FOCUSABLE/NOT_TOUCHABLE 类位），叠加在当前前台界面之上",
      "trigger_event": "获权后 events.onServiceConnected → Func.minimizeAll → setServiceInfo → doAutorun → lib.createOverlay()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "System updating, please wait...",
      "shown_text_zh": "“系统正在更新，请稍候……”（居中白字 + 旋转 spinner）",
      "user_action_requested": "要求用户原地等待，实际用于遮盖后续自动化注入与界面跳转",
      "code_anchor": "com.lib#createOverlay（overlay.loadData(getString(banner_text))）；res/values/strings.xml#banner_text"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.example.eventbot.events（AccessibilityService）+ com.example.eventbot.service + 后台注入队列 libInterface$injectEvent",
      "trigger_event": "onServiceConnected 注册 injectEventQueue、setServiceInfo(makeA11yServiceInfo)、doAutorun；onAccessibilityEvent 将事件投入队列由二阶段库解析执行",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无障碍事件流被送入远控脚本引擎，按云端下发指令执行点击/读取等操作（指令内容需云端下发）",
      "user_action_requested": "无需用户操作",
      "code_anchor": "com.example.eventbot.events#onServiceConnected；com.example.eventbot.events#onAccessibilityEvent；com.lib#doAutorun"
    }
  ],
  "text_presentation_locations": [
    "冷启动 activity 弹出的 AlertDialog 内嵌 WebView：loadDataWithBaseURL(\"file:///android_asset/\", getString(R.string.hint_text))，标题句 + 两步图文（1.jpg / 2.jpg 系统设置截图）",
    "同一 AlertDialog 的唯一按钮文本：R.string.hint_button = \"Open PEC\"",
    "系统无障碍服务列表项标题：android:label=@string/app_name = \"Posta Elettronica Certificata\"",
    "系统无障碍服务列表项说明：res/xml/accessibility_config.xml android:description = \"You must enable Posta Elettronica Certificata in order to get full functionality of the application.\"",
    "获权后叠在屏幕上的全屏 WebView 遮罩：R.string.banner_text = \"System updating, please wait...\"",
    "assets/1.jpg、assets/2.jpg：真实系统“设置 → 无障碍 → 已下载服务”界面截图，用于纯图指引"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Posta Elettronica Certificata will not work correctly.",
      "text_zh": "Posta Elettronica Certificata 将无法正常工作。",
      "source_location": "res/values/strings.xml key=hint_text",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Select Posta Elettronica Certificata in Settings",
      "text_zh": "1. 在设置中选择 Posta Elettronica Certificata",
      "source_location": "res/values/strings.xml key=hint_text",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. Turn on it",
      "text_zh": "2. 将其打开（打开开关）",
      "source_location": "res/values/strings.xml key=hint_text",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Open PEC",
      "text_zh": "打开 PEC",
      "source_location": "res/values/strings.xml key=hint_button",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "You must enable Posta Elettronica Certificata in order to get full functionality of the application.",
      "text_zh": "您必须启用 Posta Elettronica Certificata 才能获得本应用的完整功能。",
      "source_location": "res/values/strings.xml key=accessibility_config_text（accessibility_config.xml android:description）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "System updating, please wait...",
      "text_zh": "系统正在更新，请稍候……",
      "source_location": "res/values/strings.xml key=banner_text（lib.createOverlay 全屏遮罩）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "AlertDialog 为 setCancelable(false) 且仅有一个正向按钮，无法关闭；跳转使用 1409286144（NEW_TASK|CLEAR_TASK|CLEAR_TOP），返回键无法回到原应用；未授权时 lib.isA11y 在 doAutorun / requestPermissions / parseCommand / makeKnockPacket 中反复校验并重新弹窗跳设置；onAccessibilityEvent 每次事件都会拉起 service，形成持续重试。",
    "overlay_or_fake_settings": "是。引导弹窗本身是 window type=2003 的系统级悬浮 AlertDialog；获权后 createOverlay 再叠加 type=2032 的全屏半透明 WebView（WallpaperManager 背景 + \"System updating, please wait...\" spinner）盖住前台界面，实现设置页之后的遮罩式接管。",
    "restricted_settings_13plus_coaching": "无。targetSdk 21，未见“应用详情 → 右上角菜单 → 允许受限设置”教学，也未见 SESSION_INSTALLER 绕过；但存在对系统设置弹窗的注入自动点击（lib.requestOptimizationsIgnored / requestSmsAdmin 注入 com.android.settings 的 button1/button2 CLICK 事件）。",
    "post_grant_anti_removal": "未发现监听设置页后自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权的显式逻辑；但 onKeyEvent→libInterface.BlockHardwareButtons 具备拦截硬件按键能力，配合全屏遮罩可妨碍用户回到设置撤权。",
    "benign_graceful_degradation": "无。无手动模式、无仅观看模式、无 ADB 替代路径，未授权即持续弹窗重跳。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间，或冷启动后 activity 创建约 15s（cfg.permissionsDelay=15）内出现的 type=2003 AlertDialog；此外无障碍服务 onServiceConnected 触发后约 1s 内出现的 type=2032 全屏 WebView 遮罩。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（最关键）",
        "page_identifier": "com.example.eventbot.activity 之上的 AlertDialog（window type=2003），内含 WebView 渲染的 “Posta Elettronica Certificata will not work correctly.” 与两张系统截图",
        "why_most_useful": "该弹窗是唯一入口，且不可取消、无跳过按钮，可直接证明强制诱导与信息不对称（宣称功能故障而非安全授权）",
        "observable_utg_signals": ["弹窗节点文本 'Posta Elettronica Certificata will not work correctly.'", "唯一按钮文本 'Open PEC' 且无 cancel/关闭按钮节点", "窗口层级为悬浮窗（非普通 Activity 内容），覆盖在启动页之上"]
      },
      {
        "page_role": "跳转前 WebView 教学页（图文分步指引）",
        "page_identifier": "同一 AlertDialog 内 WebView，含 1.jpg / 2.jpg 两张系统设置截图与 '1. Select ...' '2. Turn on it' 文本",
        "why_most_useful": "图文分步教学是“受限设置教学”类诱导的直接物证，且图片与文本可交叉验证引导目标就是无障碍开关",
        "observable_utg_signals": ["文本节点 '1. Select Posta Elettronica Certificata in Settings'", "存在 image 节点（1.jpg/2.jpg 系统设置截图）", "WebView 容器节点 className=android.webkit.WebView"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务 中的 'Posta Elettronica Certificata' 条目及其说明文字",
        "why_most_useful": "确认服务标签与描述复用伪装品牌，且与真实包名 com.example.eventbot 明显不符",
        "observable_utg_signals": ["条目文本 'Posta Elettronica Certificata'", "描述 'You must enable Posta Elettronica Certificata in order to get full functionality of the application.'", "开关控件状态（未启用/已启用）"]
      },
      {
        "page_role": "设置页后的全屏压栈遮罩页",
        "page_identifier": "无障碍服务连接后出现的全屏 WebView 悬浮窗（type=2032，透明背景 + 壁纸），文本 'System updating, please wait...' 与旋转 spinner",
        "why_most_useful": "证明获权后立即接管屏幕、掩盖后续自动化行为，是“诱导成功后隐藏真实动作”的关键环节",
        "observable_utg_signals": ["文本节点 'System updating, please wait...'", "窗口覆盖整个屏幕且不可点击（非焦点窗口）", "出现在无障碍开关被打开后的 1-2 秒内"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "一阶段主 DEX 仅有加载器与 Manifest，引导文案与跳转逻辑全在 RC4 加密的 assets/fonts/default.ttf 二阶段 DEX 中，纯静态浅层扫描会漏掉全部引导字符串；该文件以字体文件命名伪装，需按 RC4+硬编码密钥还原后才能取到 hint_text/hint_button/banner_text。运行期 UTG 不受此影响（解密后正常渲染）。此外教程含 1.jpg/2.jpg 系统截图，纯图部分需 OCR 才能读出引导内容。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.lib#requestA11yAlert",
    "com.lib$3#onClick",
    "com.lib#requestA11y",
    "com.lib#createOverlay",
    "com.example.eventbot.service#loadLib",
    "res/values/strings.xml#hint_text / #hint_button / #banner_text / #accessibility_config_text"
  ]
}
```

</details>
