# MB_008__ef9c1ee9c0｜Hook — FlexTV

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：139.1s

## 1. 一句话核心结论

- **核心申请方式**：以视频应用 FlexTV 为壳，冷启动直接进入内嵌 HTML 的 WebView 引导页，经 JS 桥 Android.onData 拉起系统无障碍设置，并在设置页上叠加悬浮 WebView 引导条、每 2 秒重跳形成拒权循环，直至拿到可读屏/可注入/可手势的全量无障碍服务。
- **静态可见性说明**：代码骨架（Activity/WebView/JS桥/Intent跳转/WindowManager悬浮层/Handler定时重跳）完全静态可见，无壳无VMP；但两段引导HTML载荷由 mugohofijagu$Companion$s227$2 / s228$2 的 Lazy 提供者返回空串（Base64.decode 后为空），当前包内文本载荷已被剥离或依赖投放版本填充，逐字引导文案无法静态还原，仅能确认渲染路径与占位符 %Enable_Accessibility_Service%（运行时替换为 FlexTV）。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ef9c1ee9c06e8f6f92e9388e445d268072a321a4bf77704054dfdfbc68bd8830` |
| 包名 / 年份 | `com.gohaxacupumasa.kipo` / 2024 |
| 家族 / 品类 | **Hook**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | FlexTV |
| 引导页宣称品牌/身份 | FlexTV（视频/影视播放器，桌面图标与无障碍服务标签同名） |
| 系统无障碍列表服务名 | FlexTV |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：启动Activity内容仅为单空格 TextView 的透明主题页，用户看不到任何业务界面；无障碍 description 只写'如已开启请关掉再打开'，隐瞒读屏/按键记录/界面遮挡能力；Manifest 内置 Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram 等十余个 enabled=false 的 activity-alias，获权后由 saxixi.enableIcon() 按 appToStart 动态启用实现二次图标与名称伪装；类名/包名全部使用随机拼音式混淆（zawirepaza、mugohofijagu、jaxafakawoke、tano 等）。 |
| 无障碍服务类名 | `com.pavotekehigo.ruwuga.johimusuwoyu.zawirepaza` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | If accessibility permission has been on, please turn off then turn on. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.gohaxacupumasa.kipo.saxixi（LAUNCHER Activity，Theme.Translucent.NoTitleBar，noHistory，excludeFromRecents） | 用户点击桌面 FlexTV 图标 → onCreate | 原生Activity | 界面只有一个内容为单个空格的 TextView，即视觉空白页，不展示任何视频业务内容 | 无显式要求，用户看到空白/瞬间过渡后自动进入下一阶段，无取消或跳过入口 | `com.gohaxacupumasa.kipo.saxixi#onCreate → Payload.INSTANCE.start2(this)` |
| 2 | 引导说明页 | com.pavotekehigo.ruwuga.mugohofijagu（AppCompatActivity，onResume 即调用 work()），内部创建 WebView 并 addJavascriptInterface(..., "Android") | onResume → work()，判断 fepe.isAccessibilityServiceEnabled(this, zawirepaza.class) 为 false 时走 launchHttp 分支 | 本地HTML WebView | **原文**：（HTML 由 Base64.decode(mugohofijagu.Companion.getS227()) 提供，本包该字段为空串；文案模板含占位符 %Enable_Accessibility_Service%，运行时被 zuhoxipapuwavape.getAcname() 替换为 FlexTV）<br>**译注**：包内内嵌（当前已被剥离）的引导页 HTML，含以 FlexTV 名义的“开启无障碍服务”指引，页面按钮通过 JS 桥 Android.onData() 回调原生代码 | 要求用户点击页面上的引导按钮以“启用无障碍服务”，页面无取消/跳过逻辑（onBackPressed 无降级处理） | `com.pavotekehigo.ruwuga.mugohofijagu#work / com.pavotekehigo.ruwuga.mugohofijagu$WebAppInterface#onData` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | JS 桥 Android.onData() → openAccessabilitySettings()（先 removeView/destroy 引导 WebView）→ tano.gotoAccessibilityService(this) | 系统无障碍页 | 无 | 要求用户在系统列表中手动找到 FlexTV 并打开开关；跳转前无二次确认，未使用 ACTION_APPLICATION_DETAILS_SETTINGS，也无 Android 13 受限设置分步教学 | `com.pavotekehigo.ruwuga.fihoto.tano#gotoAccessibilityService（new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(335544320)）` |
| 4 | 遮罩叠层指引 | com.pavotekehigo.ruwuga.bumuve.jaxafakawoke（Theme.Translucent.NoTitleBar.Fullscreen），用 WindowManager.addView 叠加 WebView | gotoAccessibilityService() 内 if (mugohofijagu.Companion.getS228().length() > 0) 成立时 startActivity(jaxafakawoke)；Xiaomi 且 SDK_INT>=29 额外加 NEW_TASK\|131072\|8388608 | 悬浮窗Overlay | **原文**：（HTML 由 Base64.decode(mugohofijagu.Companion.getS228()) 提供，本包该字段为空串）<br>**译注**：以 TYPE_APPLICATION_OVERLAY(type=2)+FLAG_NOT_FOCUSABLE、gravity=80（底部）、-1 x -2 尺寸压在系统无障碍设置页下方的半透明引导条，继续指引用户在系统页里点选 FlexTV | 要求用户按悬浮条提示在系统无障碍页操作；悬浮层不可聚焦，用户无法通过它取消，只能点系统开关或返回 | `com.pavotekehigo.ruwuga.bumuve.jaxafakawoke#onCreate（getWm().addView(this.webView, windowManager$LayoutParams)）` |
| 5 | 拒权反馈循环 | Handler 定时任务 + 重复跳转系统无障碍设置页 | ensureAccessibilityServiceEnabled 中 zawirepaza.Companion.isEnabled() 或 fepe.isAccessibilityServiceEnabled(ctx, zawirepaza.class) 为 false 时，casimayuwuxe.getMainHandler().postDelayed(lambda, 2000) → 再次 gotoAccessibilityService() | 系统无障碍页 | 无 | 无取消选项；用户只能通过开启 FlexTV 无障碍开关来终止循环 | `com.pavotekehigo.ruwuga.fihoto.tano#ensureAccessibilityServiceEnabled（postDelayed(r0, 2000) 后调用 gotoAccessibilityService）` |
| 6 | 获权后动作 | com.pavotekehigo.ruwuga.johimusuwoyu.zawirepaza（AccessibilityService） | 服务 onServiceConnected 后被系统启用，mugohofijagu.work() 检测 isAccessibilityServiceEnabled 为 true，转入权限申请与 Payload 协程 | 不可静态还原 | 无 | 继续逐个授予运行时权限与悬浮窗、忽略电池优化；服务本身通过 WATCH_PKG_INSTALLER/WATCH_SETTINGS 与 GLOBAL_ACTION 监听设置页阻止撤权 | `com.pavotekehigo.ruwuga.mugohofijagu#work / com.pavotekehigo.ruwuga.johimusuwoyu.zawirepaza#onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务标签 FlexTV，description = res/values/strings.xml 的 text_accessibility_service_description（"If accessibility permission has been on, please turn off then turn on."），由 res/xml/jile.xml 的 android:description 引用
- com.pavotekehigo.ruwuga.mugohofijagu 内 WebView：loadDataWithBaseURL(null, Base64.decode(getS227()) 的 HTML, "text/html", "UTF-8")，全屏引导页（本包载荷为空串，模板占位符 %Enable_Accessibility_Service% → FlexTV）
- 系统无障碍设置页之上的悬浮 WebView：jaxafakawoke 通过 WindowManager.addView 以 TYPE_APPLICATION_OVERLAY、底部 gravity=80、宽满高包裹的悬浮条呈现 Base64.decode(getS228()) 的 HTML（本包载荷为空串）
- com.gohaxacupumasa.kipo.saxixi 启动页：仅 setContentView(new TextView(" "))，无任何说明文字，制造视觉空白以掩盖引导流程
- 无 AlertDialog、无 strings.xml 中的引导文案、无 assets/ 下 HTML 文件（引导文本全部以 DEX 内 Base64 常量形式存在）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开启过，请先关闭再重新打开。 | `res/values/strings.xml → text_accessibility_service_description（被 res/xml/jile.xml 的 android:description 引用，显示在系统无障碍服务列表项）` | 教唆忽视警告 |
| en | FlexTV | FlexTV（视频应用品牌名） | `com.pavotekehigo.ruwuga.fihoto.zuhoxipapuwavape 的 tag/access1/access2 常量，用于替换引导 HTML 中的 %Enable_Accessibility_Service% 占位符；同时为 AndroidManifest 的 application android:label 与无障碍服务标签` | 未知 |
| en | %Enable_Accessibility_Service% | （占位符，运行时被替换为 FlexTV，即“启用 FlexTV 的无障碍服务”） | `com.pavotekehigo.ruwuga.fihoto.zuhoxipapuwavape 的 acname 常量；在 mugohofijagu#work 与 jaxafakawoke#onCreate 中通过 StringsKt.replace$default 替换` | 受限设置分步教学 |
| en | — | 单个空格（视觉空白页） | `com.gohaxacupumasa.kipo.saxixi#onCreate：TextView textView = new TextView(this); textView.setText(" "); setContentView(textView)` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：ensureAccessibilityServiceEnabled 每 2000ms 通过 Handler.postDelayed 再次调用 gotoAccessibilityService() 重跳系统无障碍设置页；退出回调延迟 2000ms、进入回调延迟 3000ms，用户从设置页返回或关闭开关后仍会被拉回，只有真正启用 FlexTV 无障碍服务才会走 enabled 分支（r0=0）停止重跳；mugohofijagu.onBackPressed/onKeyDown 亦无降级或退出逻辑。
- **遮罩叠层 / 高仿系统设置页**：有半透明悬浮引导遮罩：jaxafakawoke 以 WindowManager 叠加 TYPE_APPLICATION_OVERLAY、FLAG_NOT_FOCUSABLE、gravity=80、-1 x -2 的 WebView 于系统无障碍设置页底部；未伪造系统开关控件（无仿冒无障碍设置页），仅为覆盖式引导条。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：有：无障碍服务 zawirepaza 实现 blockDeleteBots、exitSettings、killApplication，配合 DEX 预筛的 PERFORM_GLOBAL_ACTION（GLOBAL_ACTION_BACK/HOME）、WATCH_PKG_INSTALLER、WATCH_SETTINGS 特征，可在用户进入设置页撤权时执行返回/回主页动作；addBlackView 还可叠加黑色遮挡视图。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两点任一命中即拉起 UTG 抓取：① 监测到 Intent action == android.settings.ACCESSIBILITY_SETTINGS 被 startActivity（tano.gotoAccessibilityService，含 FLAG_ACTIVITY_CLEAR_TOP），或 ② 冷启动 launcher Activity com.gohaxacupumasa.kipo.saxixi 后 1–3 秒内出现 WebView 承载的引导页。同时挂 WindowManager.addView 的 TYPE_APPLICATION_OVERLAY 创建回调，可在悬浮层出现瞬间抓图。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本样本引导文案全部为 Base64 内嵌 HTML 常量（s227/s228），当前包内 Lazy 提供者返回空串，说明实际文案依赖投放版本填充，纯静态无法逐字获取——UTG 必须在运行期抓取该 WebView 文本。另需注意：启动页仅为一个空格 TextView，纯文本 UTG 在此页会读到空内容，须等到 WebView 页或悬浮层出现才有可判别信号；应用同时具备 activity-alias 变脸能力，桌面上可能显示为 Facebook/Gmail/WhatsApp 等图标，UTG 应按包名 com.gohaxacupumasa.kipo 而非图标名识别。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的引导 WebView 页（跳转前教学页）** | Activity com.pavotekehigo.ruwuga.mugohofijagu，全屏 WebView，含 JS 接口 Android（window.Android.onData） | 这是应用自述“为什么需要无障碍”的唯一自建说明页，其文案决定是否构成虚假理由/教唆忽视警告；该页 HTML 在包内已被剥离，只有运行期才能取到真实文本 | WebView 节点下的全部可见文本；是否存在“取消/跳过/稍后”按钮（预期无）；页面是否出现 FlexTV 品牌名与“开启无障碍”字样；window.Android 桥对象是否存在 |
| **跳转后叠加在系统无障碍设置页上的悬浮引导条** | jaxafakawoke 的 TYPE_APPLICATION_OVERLAY WebView，位于屏幕底部（gravity=80），高度包裹内容，FLAG_NOT_FOCUSABLE | 这是区分“正常引导”与“覆盖式压迫引导”的关键：悬浮层压住系统设置页说明应用在主动干预系统 UI，且用户无法通过该层退出 | 系统设置页上方是否出现第二个窗口的文本节点；悬浮层文本是否重复指引点击 FlexTV 开关；悬浮层是否覆盖系统列表项导致误触 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务，条目名称 FlexTV，摘要为“If accessibility permission has been on, please turn off then turn on.” | 证明服务标签与真实能力（读屏、按键过滤、手势注入、窗口检索）严重不符，且描述文案刻意回避能力说明 | 服务项 label = FlexTV；description 文本逐字比对；开关初始状态；同一页是否被悬浮层覆盖 |
| **拒权后自动重跳的设置页（循环证据）** | 连续两次以上出现 android.settings.ACCESSIBILITY_SETTINGS 的 Activity 切换，间隔约 2000ms | 直接证明非自愿性：用户退出即被拉回，无取消路径，是诱导/强迫判定的决定性运行期证据 | 2000ms 周期性的 Activity 重入事件；用户按返回后页面重新出现在前台；循环终止条件是否仅为开关被打开 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.gohaxacupumasa.kipo.saxixi#onCreate`
- `com.pavotekehigo.ruwuga.mugohofijagu#work`
- `com.pavotekehigo.ruwuga.mugohofijagu$WebAppInterface#onData`
- `com.pavotekehigo.ruwuga.fihoto.tano#gotoAccessibilityService`
- `com.pavotekehigo.ruwuga.fihoto.tano#ensureAccessibilityServiceEnabled`
- `com.pavotekehigo.ruwuga.bumuve.jaxafakawoke#onCreate`
- `res/xml/jile.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**1. 静态可见性：部分可见。** 引导流程的代码骨架完全静态可还原（Activity → WebView → JS 桥 → 系统设置 → 悬浮遮罩 → 定时重跳），但两段引导 HTML（`s227`/`s228`）由 Lazy 提供者返回空串，当前包内文本载荷已被剥离，逐字文案不可得；无加壳、无 VMP。

**2. 冷启动即为引导流程，无正常业务界面。** 桌面入口 [saxixi](<resource-unit:#1.dex1 code:com.gohaxacupumasa.kipo.saxixi#onCreate>) 使用 `Theme.Translucent.NoTitleBar` + `noHistory`，`onCreate` 只 `setContentView` 一个内容为单空格 `" "` 的 TextView，随后 `Payload.start2()` 直接进入权限/引导链。

**3. 引导载体是本地内嵌 HTML 的 WebView，不是远端页面。** [mugohofijagu.work()](<resource-unit:#1.dex1 code:com.pavotekehigo.ruwuga.mugohofijagu#work>) 在无障碍未启用分支中创建 WebView，开启 JS 与弹窗，`addJavascriptInterface(..., "Android")` 注入 [WebAppInterface](<resource-unit:#1.dex1 code:com.pavotekehigo.ruwuga.mugohofijagu$WebAppInterface#onData>)；HTML 来自 `getS227()` 的 `Base64.decode` 后 `loadDataWithBaseURL`，占位符 `%Enable_Accessibility_Service%` 被替换为 `FlexTV`。

**4. 跳转与拒绝授权循环。** HTML 按钮 → `Android.onData()` → [openAccessabilitySettings()](<resource-unit:#1.dex1 code:com.pavotekehigo.ruwuga.mugohofijagu#openAccessabilitySettings>)（先销毁引导 WebView）→ [tano.gotoAccessibilityService()](<resource-unit:#1.dex1 code:com.pavotekehigo.ruwuga.fihoto.tano#gotoAccessibilityService>) 拉起 `android.settings.ACCESSIBILITY_SETTINGS`；跳前经 [ensureAccessibilityServiceEnabled()](<resource-unit:#1.dex1 code:com.pavotekehigo.ruwuga.fihoto.tano#ensureAccessibilityServiceEnabled>) 校验，未启用则 `postDelayed(2000)` 再次跳转，退出回调 2000ms／进入回调 3000ms，形成返回即重跳的循环，无取消/跳过分支。

**5. 设置页之上叠加悬浮引导条。** [jaxafakawoke.onCreate()](<resource-unit:#1.dex1 code:com.pavotekehigo.ruwuga.bumuve.jaxafakawoke#onCreate>) 用 `WindowManager.addView` 以 `TYPE_APPLICATION_OVERLAY`、`FLAG_NOT_FOCUSABLE`、gravity=80 叠加 `-1 x -2` 的 WebView（内容 `Base64.decode(getS228())`），压在系统无障碍页底部继续指引；Xiaomi≥29 分支额外加独立任务栈标志规避厂商限制。

**6. 身份与能力严重不符。** 服务标签、description 与引导页均以 `FlexTV` 视频应用自居，description 仅教用户“关掉再打开开关”（[strings.xml#L33](<resource-unit:#1 file:res/values/strings.xml#L33>)），未披露读屏、按键记录、界面遮挡能力；[jile.xml](<resource-unit:#1 file:res/xml/jile.xml>) 声明 `typeAllMask`、`flagRequestFilterKeyEvents`、`flagRetrieveInteractiveWindows`、`canPerformGestures`，服务类 `zawirepaza` 实现 `keylogger`、`permissionClick`、`injectView`、`addBlackView`、`exitSettings`、`getClipboard`。Manifest 另备 Facebook/Google Play/Gmail/WhatsApp/Chrome/Instagram 等 10 余个 `enabled=false` 的 activity-alias，获权后可动态启用做二次变脸。

已登记风险 **R-001**（high / malware_trojan）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "代码骨架（Activity/WebView/JS桥/Intent跳转/WindowManager悬浮层/Handler定时重跳）完全静态可见，无壳无VMP；但两段引导HTML载荷由 mugohofijagu$Companion$s227$2 / s228$2 的 Lazy 提供者返回空串（Base64.decode 后为空），当前包内文本载荷已被剥离或依赖投放版本填充，逐字引导文案无法静态还原，仅能确认渲染路径与占位符 %Enable_Accessibility_Service%（运行时替换为 FlexTV）。",
  "summary_one_liner": "以视频应用 FlexTV 为壳，冷启动直接进入内嵌 HTML 的 WebView 引导页，经 JS 桥 Android.onData 拉起系统无障碍设置，并在设置页上叠加悬浮 WebView 引导条、每 2 秒重跳形成拒权循环，直至拿到可读屏/可注入/可手势的全量无障碍服务。",
  "disguise_identity": {
    "app_display_name": "FlexTV",
    "claimed_brand_or_persona": "FlexTV（视频/影视播放器，桌面图标与无障碍服务标签同名）",
    "a11y_service_label": "FlexTV",
    "identity_mismatch": true,
    "obfuscation_tricks": "启动Activity内容仅为单空格 TextView 的透明主题页，用户看不到任何业务界面；无障碍 description 只写'如已开启请关掉再打开'，隐瞒读屏/按键记录/界面遮挡能力；Manifest 内置 Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram 等十余个 enabled=false 的 activity-alias，获权后由 saxixi.enableIcon() 按 appToStart 动态启用实现二次图标与名称伪装；类名/包名全部使用随机拼音式混淆（zawirepaza、mugohofijagu、jaxafakawoke、tano 等）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.gohaxacupumasa.kipo.saxixi（LAUNCHER Activity，Theme.Translucent.NoTitleBar，noHistory，excludeFromRecents）",
      "trigger_event": "用户点击桌面 FlexTV 图标 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": " ",
      "shown_text_zh": "界面只有一个内容为单个空格的 TextView，即视觉空白页，不展示任何视频业务内容",
      "user_action_requested": "无显式要求，用户看到空白/瞬间过渡后自动进入下一阶段，无取消或跳过入口",
      "code_anchor": "com.gohaxacupumasa.kipo.saxixi#onCreate → Payload.INSTANCE.start2(this)"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.pavotekehigo.ruwuga.mugohofijagu（AppCompatActivity，onResume 即调用 work()），内部创建 WebView 并 addJavascriptInterface(..., \"Android\")",
      "trigger_event": "onResume → work()，判断 fepe.isAccessibilityServiceEnabled(this, zawirepaza.class) 为 false 时走 launchHttp 分支",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "（HTML 由 Base64.decode(mugohofijagu.Companion.getS227()) 提供，本包该字段为空串；文案模板含占位符 %Enable_Accessibility_Service%，运行时被 zuhoxipapuwavape.getAcname() 替换为 FlexTV）",
      "shown_text_zh": "包内内嵌（当前已被剥离）的引导页 HTML，含以 FlexTV 名义的“开启无障碍服务”指引，页面按钮通过 JS 桥 Android.onData() 回调原生代码",
      "user_action_requested": "要求用户点击页面上的引导按钮以“启用无障碍服务”，页面无取消/跳过逻辑（onBackPressed 无降级处理）",
      "code_anchor": "com.pavotekehigo.ruwuga.mugohofijagu#work / com.pavotekehigo.ruwuga.mugohofijagu$WebAppInterface#onData"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "JS 桥 Android.onData() → openAccessabilitySettings()（先 removeView/destroy 引导 WebView）→ tano.gotoAccessibilityService(this)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍设置列表，其中显示一个名为 FlexTV 的服务项，描述为“If accessibility permission has been on, please turn off then turn on.”",
      "user_action_requested": "要求用户在系统列表中手动找到 FlexTV 并打开开关；跳转前无二次确认，未使用 ACTION_APPLICATION_DETAILS_SETTINGS，也无 Android 13 受限设置分步教学",
      "code_anchor": "com.pavotekehigo.ruwuga.fihoto.tano#gotoAccessibilityService（new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(335544320)）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.pavotekehigo.ruwuga.bumuve.jaxafakawoke（Theme.Translucent.NoTitleBar.Fullscreen），用 WindowManager.addView 叠加 WebView",
      "trigger_event": "gotoAccessibilityService() 内 if (mugohofijagu.Companion.getS228().length() > 0) 成立时 startActivity(jaxafakawoke)；Xiaomi 且 SDK_INT>=29 额外加 NEW_TASK|131072|8388608",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "（HTML 由 Base64.decode(mugohofijagu.Companion.getS228()) 提供，本包该字段为空串）",
      "shown_text_zh": "以 TYPE_APPLICATION_OVERLAY(type=2)+FLAG_NOT_FOCUSABLE、gravity=80（底部）、-1 x -2 尺寸压在系统无障碍设置页下方的半透明引导条，继续指引用户在系统页里点选 FlexTV",
      "user_action_requested": "要求用户按悬浮条提示在系统无障碍页操作；悬浮层不可聚焦，用户无法通过它取消，只能点系统开关或返回",
      "code_anchor": "com.pavotekehigo.ruwuga.bumuve.jaxafakawoke#onCreate（getWm().addView(this.webView, windowManager$LayoutParams)）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "Handler 定时任务 + 重复跳转系统无障碍设置页",
      "trigger_event": "ensureAccessibilityServiceEnabled 中 zawirepaza.Companion.isEnabled() 或 fepe.isAccessibilityServiceEnabled(ctx, zawirepaza.class) 为 false 时，casimayuwuxe.getMainHandler().postDelayed(lambda, 2000) → 再次 gotoAccessibilityService()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户退出或返回系统设置后 2 秒被再次拉回无障碍设置页，进入/退出回调分别延迟 3000ms/2000ms，构成强制循环",
      "user_action_requested": "无取消选项；用户只能通过开启 FlexTV 无障碍开关来终止循环",
      "code_anchor": "com.pavotekehigo.ruwuga.fihoto.tano#ensureAccessibilityServiceEnabled（postDelayed(r0, 2000) 后调用 gotoAccessibilityService）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.pavotekehigo.ruwuga.johimusuwoyu.zawirepaza（AccessibilityService）",
      "trigger_event": "服务 onServiceConnected 后被系统启用，mugohofijagu.work() 检测 isAccessibilityServiceEnabled 为 true，转入权限申请与 Payload 协程",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后继续申请短信/通讯录/相机/悬浮窗/忽略电池优化等权限，并通过无障碍服务执行 keylogger、permissionClick、injectView、addBlackView、blockDeleteBots、exitSettings 等操作",
      "user_action_requested": "继续逐个授予运行时权限与悬浮窗、忽略电池优化；服务本身通过 WATCH_PKG_INSTALLER/WATCH_SETTINGS 与 GLOBAL_ACTION 监听设置页阻止撤权",
      "code_anchor": "com.pavotekehigo.ruwuga.mugohofijagu#work / com.pavotekehigo.ruwuga.johimusuwoyu.zawirepaza#onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务标签 FlexTV，description = res/values/strings.xml 的 text_accessibility_service_description（\"If accessibility permission has been on, please turn off then turn on.\"），由 res/xml/jile.xml 的 android:description 引用",
    "com.pavotekehigo.ruwuga.mugohofijagu 内 WebView：loadDataWithBaseURL(null, Base64.decode(getS227()) 的 HTML, \"text/html\", \"UTF-8\")，全屏引导页（本包载荷为空串，模板占位符 %Enable_Accessibility_Service% → FlexTV）",
    "系统无障碍设置页之上的悬浮 WebView：jaxafakawoke 通过 WindowManager.addView 以 TYPE_APPLICATION_OVERLAY、底部 gravity=80、宽满高包裹的悬浮条呈现 Base64.decode(getS228()) 的 HTML（本包载荷为空串）",
    "com.gohaxacupumasa.kipo.saxixi 启动页：仅 setContentView(new TextView(\" \"))，无任何说明文字，制造视觉空白以掩盖引导流程",
    "无 AlertDialog、无 strings.xml 中的引导文案、无 assets/ 下 HTML 文件（引导文本全部以 DEX 内 Base64 常量形式存在）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开启过，请先关闭再重新打开。",
      "source_location": "res/values/strings.xml → text_accessibility_service_description（被 res/xml/jile.xml 的 android:description 引用，显示在系统无障碍服务列表项）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "FlexTV",
      "text_zh": "FlexTV（视频应用品牌名）",
      "source_location": "com.pavotekehigo.ruwuga.fihoto.zuhoxipapuwavape 的 tag/access1/access2 常量，用于替换引导 HTML 中的 %Enable_Accessibility_Service% 占位符；同时为 AndroidManifest 的 application android:label 与无障碍服务标签",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%Enable_Accessibility_Service%",
      "text_zh": "（占位符，运行时被替换为 FlexTV，即“启用 FlexTV 的无障碍服务”）",
      "source_location": "com.pavotekehigo.ruwuga.fihoto.zuhoxipapuwavape 的 acname 常量；在 mugohofijagu#work 与 jaxafakawoke#onCreate 中通过 StringsKt.replace$default 替换",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": " ",
      "text_zh": "单个空格（视觉空白页）",
      "source_location": "com.gohaxacupumasa.kipo.saxixi#onCreate：TextView textView = new TextView(this); textView.setText(\" \"); setContentView(textView)",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "ensureAccessibilityServiceEnabled 每 2000ms 通过 Handler.postDelayed 再次调用 gotoAccessibilityService() 重跳系统无障碍设置页；退出回调延迟 2000ms、进入回调延迟 3000ms，用户从设置页返回或关闭开关后仍会被拉回，只有真正启用 FlexTV 无障碍服务才会走 enabled 分支（r0=0）停止重跳；mugohofijagu.onBackPressed/onKeyDown 亦无降级或退出逻辑。",
    "overlay_or_fake_settings": "有半透明悬浮引导遮罩：jaxafakawoke 以 WindowManager 叠加 TYPE_APPLICATION_OVERLAY、FLAG_NOT_FOCUSABLE、gravity=80、-1 x -2 的 WebView 于系统无障碍设置页底部；未伪造系统开关控件（无仿冒无障碍设置页），仅为覆盖式引导条。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "有：无障碍服务 zawirepaza 实现 blockDeleteBots、exitSettings、killApplication，配合 DEX 预筛的 PERFORM_GLOBAL_ACTION（GLOBAL_ACTION_BACK/HOME）、WATCH_PKG_INSTALLER、WATCH_SETTINGS 特征，可在用户进入设置页撤权时执行返回/回主页动作；addBlackView 还可叠加黑色遮挡视图。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两点任一命中即拉起 UTG 抓取：① 监测到 Intent action == android.settings.ACCESSIBILITY_SETTINGS 被 startActivity（tano.gotoAccessibilityService，含 FLAG_ACTIVITY_CLEAR_TOP），或 ② 冷启动 launcher Activity com.gohaxacupumasa.kipo.saxixi 后 1–3 秒内出现 WebView 承载的引导页。同时挂 WindowManager.addView 的 TYPE_APPLICATION_OVERLAY 创建回调，可在悬浮层出现瞬间抓图。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的引导 WebView 页（跳转前教学页）",
        "page_identifier": "Activity com.pavotekehigo.ruwuga.mugohofijagu，全屏 WebView，含 JS 接口 Android（window.Android.onData）",
        "why_most_useful": "这是应用自述“为什么需要无障碍”的唯一自建说明页，其文案决定是否构成虚假理由/教唆忽视警告；该页 HTML 在包内已被剥离，只有运行期才能取到真实文本",
        "observable_utg_signals": ["WebView 节点下的全部可见文本", "是否存在“取消/跳过/稍后”按钮（预期无）", "页面是否出现 FlexTV 品牌名与“开启无障碍”字样", "window.Android 桥对象是否存在"]
      },
      {
        "page_role": "跳转后叠加在系统无障碍设置页上的悬浮引导条",
        "page_identifier": "jaxafakawoke 的 TYPE_APPLICATION_OVERLAY WebView，位于屏幕底部（gravity=80），高度包裹内容，FLAG_NOT_FOCUSABLE",
        "why_most_useful": "这是区分“正常引导”与“覆盖式压迫引导”的关键：悬浮层压住系统设置页说明应用在主动干预系统 UI，且用户无法通过该层退出",
        "observable_utg_signals": ["系统设置页上方是否出现第二个窗口的文本节点", "悬浮层文本是否重复指引点击 FlexTV 开关", "悬浮层是否覆盖系统列表项导致误触"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，条目名称 FlexTV，摘要为“If accessibility permission has been on, please turn off then turn on.”",
        "why_most_useful": "证明服务标签与真实能力（读屏、按键过滤、手势注入、窗口检索）严重不符，且描述文案刻意回避能力说明",
        "observable_utg_signals": ["服务项 label = FlexTV", "description 文本逐字比对", "开关初始状态", "同一页是否被悬浮层覆盖"]
      },
      {
        "page_role": "拒权后自动重跳的设置页（循环证据）",
        "page_identifier": "连续两次以上出现 android.settings.ACCESSIBILITY_SETTINGS 的 Activity 切换，间隔约 2000ms",
        "why_most_useful": "直接证明非自愿性：用户退出即被拉回，无取消路径，是诱导/强迫判定的决定性运行期证据",
        "observable_utg_signals": ["2000ms 周期性的 Activity 重入事件", "用户按返回后页面重新出现在前台", "循环终止条件是否仅为开关被打开"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本样本引导文案全部为 Base64 内嵌 HTML 常量（s227/s228），当前包内 Lazy 提供者返回空串，说明实际文案依赖投放版本填充，纯静态无法逐字获取——UTG 必须在运行期抓取该 WebView 文本。另需注意：启动页仅为一个空格 TextView，纯文本 UTG 在此页会读到空内容，须等到 WebView 页或悬浮层出现才有可判别信号；应用同时具备 activity-alias 变脸能力，桌面上可能显示为 Facebook/Gmail/WhatsApp 等图标，UTG 应按包名 com.gohaxacupumasa.kipo 而非图标名识别。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.gohaxacupumasa.kipo.saxixi#onCreate",
    "com.pavotekehigo.ruwuga.mugohofijagu#work",
    "com.pavotekehigo.ruwuga.mugohofijagu$WebAppInterface#onData",
    "com.pavotekehigo.ruwuga.fihoto.tano#gotoAccessibilityService",
    "com.pavotekehigo.ruwuga.fihoto.tano#ensureAccessibilityServiceEnabled",
    "com.pavotekehigo.ruwuga.bumuve.jaxafakawoke#onCreate",
    "res/xml/jile.xml"
  ]
}
```

</details>
