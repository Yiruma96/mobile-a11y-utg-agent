# MB_137__f717e94498｜Copybara — ISP Token

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：156.0s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即全屏加载本地 HTML 页面、以"Chrome 更新/安装步骤"叙事分步教学并一键跳系统无障碍设置，页面无取消按钮，未开启时用 3 秒定时 Toast 持续催促，获权后直接启动无障碍主服务与注入加载器。
- **静态可见性说明**：无障碍诱导链完整静态可见：入口 main._activity_create→_create_act_data，载体 _create_ui2 读取的 assets/pg-*.html 与 _create_ui3 读取的 design.txt/designxiaomi.txt 均为明文，跳转点 android.settings.ACCESSIBILITY_SETTINGS 出现在 main._istheaccessibilityserviceenabled 与 ResumableSub_check_data.resume，拒权循环在 dtrsbnotisuntilactv._timer1_tick。仅 assets/encrypted_dex.zip 为加密二阶段载荷（与本次引导流程无关，属获权后窃取/远控链）。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `f717e9449835314b9923aaa5ad0d41ee76bd2803044cb190a77c9b3f4e982d6f` |
| 包名 / 年份 | `com.dohpgfr.qarthpc` / 2025 |
| 家族 / 品类 | **Copybara**（同池样本数：7） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | ISP Token |
| 引导页宣称品牌/身份 | Google Chrome / Chrome Update（HTML 原文品牌名，运行期被替换为应用自身名称 ISP Token，但"更新 Chrome、按安装步骤操作"的叙事保留）；系统无障碍说明另伪装为设备杀毒防护 |
| 系统无障碍列表服务名 | ISP Token（.backgroundservice 的 android:label；android:description 为意大利语"帮助系统保护设备、用无障碍事件扫描并拦截病毒"） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：HTML 原文写死 Chrome Update / Google Chrome / appiconhere，运行时被 String.replace 替换为应用自身 label 与应用图标 base64，使页面外观与本应用一致但保留"更新/安装"误导叙事；无障碍 description 与 summary 使用意大利语杀毒话术，与页面宣称的浏览器更新及服务真实能力（typeAllMask + canRetrieveWindowContent + canPerformGestures + flagRetrieveInteractiveWindows）均不符；桌面名为无意义品牌 ISP Token |
| 无障碍服务类名 | `.backgroundservice` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli). / Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli). |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.dohpgfr.qarthpc.main（LAUNCHER Activity .main） | _activity_create → _create_act_data，冷启动即执行；仅 _isemulator/_isemulator2 为真时 Toast "App can't work on Emulators" 并退出 | 原生Activity | **原文**：App can't work on Emulators<br>**译注**：（仅模拟器环境）应用无法在模拟器上运行 | 真机无需操作，直接进入下一步；无取消/跳过 | `com.dohpgfr.qarthpc.main._activity_create / _create_act_data` |
| 2 | 引导说明页 | main Activity 上全屏 AddView 的 WebViewWrapper（_webviewextras1 + B4A JS 接口），加载 assets/pg-en.html 等本地 HTML | _create_act_data 中 _intdesignver==0 时调用 _create_ui2；按系统语言选 pg-de/en/es/fl/gr/it/pt/se.html，缺省回落 pg-en.html | 本地HTML WebView | **原文**：Chrome Update / Update your Google Chrome. / Click the "Continue" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the "Downloaded Services" or "Installed Services" section. / 3 Activate the "Google Chrome" option. / Continue<br>**译注**：Chrome 更新 / 请更新你的 Google Chrome。/ 点击"继续"按钮并按照安装步骤操作。/ 1 打开设置 / 2 在无障碍中打开"已下载的服务"或"已安装的服务" / 3 启用"Google Chrome"选项 / 继续 | 点击底部 Continue（整个 .els 区域均可点击，同一回调），无取消/跳过按钮 | `com.dohpgfr.qarthpc.main._create_ui2 + assets/pg-en.html` |
| 3 | 引导说明页 | 原生 Label 版引导页（_create_ui3，三个 LabelWrapper + 蓝色按钮 lblsettings） | _create_act_data 中 _intdesignver!=0 时调用 _create_ui3 | 原生Activity | **原文**：Enable Accessibility Service / 1- Open 'Installed Services' / 2- Find <app> / 3- Set Switch ON / Open Settings<br>**译注**：启用无障碍服务 / 1- 打开"已安装的服务" / 2- 找到 <应用名> / 3- 将开关设为开启 / 打开设置 | 点击 lblsettings（文案"Open Settings"），无取消/跳过 | `com.dohpgfr.qarthpc.main._create_ui3 + assets/design.txt、assets/designxiaomi.txt` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | B4A.CallSub('check_data') / lblsettings 点击 → main._check_data → ResumableSub_check_data.resume：isAccessibilityServiceEnabled 为 false 时 IntentWrapper.Initialize("android.settings.ACCESSIBILITY_SETTINGS") + StartActivity | 系统无障碍页 | **原文**：无（应用不渲染该页）<br>**译注**：系统无障碍设置列表，其中出现本应用服务项 ISP Token 及其意大利语杀毒说明 | 要求用户手动在系统无障碍列表中找到并开启本应用服务 | `com.dohpgfr.qarthpc.main$ResumableSub_check_data.resume（case 10）+ com.dohpgfr.qarthpc.main._check_data` |
| 5 | 拒权反馈循环 | .dtrsbnotisuntilactv 服务（Timer 3000ms + Notification） | _create_act_data 末尾 _dstrb_not_hndlr 检测服务未启用且 globalparameters._isaccactive 为 false 时 StartService(.dtrsbnotisuntilactv)；其 _service_create 在 _isacc_noti_disturb 为真时 Initialize timer1 3000ms | 通知栏 | **原文**：Open Installed Services, Enable <应用名> service<br>**译注**：打开"已安装的服务"，启用 <应用名> 服务 | 持续 Toast 与通知催促用户回到系统设置开启服务；无取消，仅当 isAccessibilityServiceEnabled 变真才 Cancel(111) 并 StopService | `com.dohpgfr.qarthpc.dtrsbnotisuntilactv._timer1_tick / _service_create` |
| 6 | 获权后动作 | com.dohpgfr.qarthpc.backgroundservice（无障碍主服务）+ 可选 inj_dnlader、LOCATION_SOURCE_SETTINGS | ResumableSub_check_data.resume case 21 StartService(backgroundservice)；SDK>=34 且缺后台定位权限时再 StartActivity("android.settings.LOCATION_SOURCE_SETTINGS")；globalparameters._ispreinjallfls 为真时 StartService(inj_dnlader) | 系统无障碍页 | 无 | 无（获权后自动进入后续能力阶段）；此阶段无撤权确认提示 | `com.dohpgfr.qarthpc.main$ResumableSub_check_data.resume（case 19/21/24）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动 main Activity 上全屏本地 HTML WebView（assets/pg-en.html、pg-it.html、pg-de.html、pg-es.html、pg-fl.html、pg-gr.html、pg-pt.html、pg-se.html，LoadHtml 渲染，品牌名运行期替换为本应用名）
- 同一 Activity 的原生 Label 备用页（main._create_ui3，文案来自 assets/design.txt 与 assets/designxiaomi.txt，按语言取 5 条数组）
- HTML 内 "Continue" 按钮与整个 .els 容器 onClick="javascript:B4A.CallSub('check_data', false, '1', '2')"
- 原生页 lblsettings 标签（文案"Open Settings"，深蓝底色按钮样式）
- 系统无障碍设置列表中本应用服务项：android:label="ISP Token" + res/xml/accessibility_service_config.xml 的 android:description/@string/accessibility_service_description（意大利语杀毒说明）
- 未开启时的 Toast 与通知："Open Installed Services, Enable <应用名> service"（main._create_act_data 与 dtrsbnotisuntilactv._timer1_tick 各一处）
- 网络异常时的 MsgboxAsync：标题 "No internet"、正文 "Please make sure you are connected to the internet"（ResumableSub_check_data.resume case 6）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome Update | Chrome 更新 | `assets/pg-en.html（标题；_create_ui2 运行期 replace 为应用 label）` | 假更新 |
| en | Update your Google Chrome. | 请更新你的 Google Chrome。 | `assets/pg-en.html 第 2 段` | 假更新 |
| en | Click the "Continue" button and follow the installation steps. | 点击"继续"按钮并按照安装步骤操作。 | `assets/pg-en.html（p#manual0）` | 假更新 |
| en | 1 Open settings 2 In Accessibility, open the "Downloaded Services" or "Installed Services" section. 3 Activate the "Google Chrome" option. | 1 打开设置；2 在无障碍中打开"已下载的服务"或"已安装的服务"分区；3 启用"Google Chrome"选项。 | `assets/pg-en.html（p#manual1-3）` | 受限设置分步教学 |
| en | Continue | 继续 | `assets/pg-en.html（button#continue）` | 假更新 |
| it | Aggiorna il tuo Google Chrome. Fare clic sul pulsante "Continua" e seguire i passaggi di installazione. / In Accessibilità, apri la sezione "Servizi scaricati" o "Servizi installati". / Attiva l'opzione "Google Chrome". | 请更新你的 Google Chrome。点击"继续"按钮并按安装步骤操作。/ 在无障碍中打开"已下载的服务"或"已安装的服务"。/ 启用"Google Chrome"选项。 | `assets/pg-it.html` | 假更新 |
| it | Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. | 允许系统保护本设备，使用无障碍事件搜索并拦截病毒。 | `res/values/strings.xml accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description/android:summary 引用）` | 假反诈安全 |
| en | Enable Accessibility Service / 1- Open 'Installed Services' / 2- Find <app> / 3- Set Switch ON / Open Settings | 启用无障碍服务 / 1- 打开"已安装的服务" / 2- 找到 <应用名> / 3- 将开关设为开启 / 打开设置 | `assets/design.txt 与 assets/designxiaomi.txt（en 数组，_create_ui3 读取）` | 受限设置分步教学 |
| en | Open Installed Services, Enable <应用名> service | 打开"已安装的服务"，启用 <应用名> 服务 | `com.dohpgfr.qarthpc.main._create_act_data / com.dohpgfr.qarthpc.dtrsbnotisuntilactv._timer1_tick（硬编码拼接 B4AApplication.getLabelName()）` | 受限设置分步教学 |
| en | Please make sure you are connected to the internet | 请确保已连接互联网 | `com.dohpgfr.qarthpc.main$ResumableSub_check_data.resume（case 6，MsgboxAsync，标题 No internet）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户按返回键回到应用后再点 Continue/Open Settings 会重新走 _check_data→resume 并再次 StartActivity(ACCESSIBILITY_SETTINGS)；未获权期间 .dtrsbnotisuntilactv 以 3000ms 定时器循环弹 Toast "Open Installed Services, Enable <应用名> service" 并重建通知，直至 isAccessibilityServiceEnabled 为真才 Cancel(111)+StopService；冷启动时 _create_act_data 也会重新拉起该服务
- **遮罩叠层 / 高仿系统设置页**：有半屏/全屏叠层：引导页以 WebViewWrapper 覆盖整个 Activity（PerX 100%/PerY 100%，BringToFront）并 setZoomEnabled(false)；未使用 TYPE_ACCESSIBILITY_OVERLAY 或 SYSTEM_ALERT_WINDOW 悬浮遮罩，也未高仿系统无障碍开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。页面与原生文案只教"打开设置→无障碍→已安装/已下载服务→开启开关"，未涉及应用详情右上角菜单允许受限设置，也未使用 Session 安装器绕过
- **获权后即时行为与防撤权机制**：获权后 resume case 21 直接 StartService(backgroundservice)；服务启用即 _service_create 停止定时器与通知。反撤权动作位于引用库 com.ddkyvzr.tesmsbd.AccessibilityEventsListenerWrapper#selfDefense / onServiceConnected 中调用 PerformGlobalAction(1)=BACK、PerformGlobalAction(2)=HOME，属获权后自保能力，本次未逐行确认其触发条件
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动即拉起应用（无需任何点击），在 main Activity 创建后 1–2 秒内截取全屏 WebView 引导页；同时 Hook/monkey 监听 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 的瞬间，用于核对点击 Continue 后的跳转链
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：一是引导页品牌名与图标在运行时被 replace 为本应用 label（ISP Token）与自身图标，纯文本抓取只会看到"ISP Token Update"，需结合"更新/安装步骤"叙事而非品牌字符串判断；二是 assets/encrypted_dex.zip 为加密二阶段载荷，本流程之后的窃取/远控行为不在静态可见范围内，需动态解密补充。另 .forc_activateacc、perm_* 等权限向导 Activity 的 onCreate 为空实现，UI 逻辑在 layout 事件层，未纳入本次主链。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页（本地 HTML WebView，含"更新"标题与三步教学）** | 全屏 WebView 覆盖 main Activity，标题含"Chrome Update"或"ISP Token"+ 步骤文本 "Open settings / In Accessibility, open the Downloaded Services..." + 底部单按钮 "Continue" | 该页是唯一向用户解释"为何要去无障碍设置"的地方，其文案性质（假更新+分步教学）与是否提供取消入口直接决定诱导定性 | 标题/正文中"更新/安装/Update"叙事与桌面应用名 ISP Token 的不一致；存在 1/2/3 编号的无障碍设置分步教学文本；界面只有一个主按钮、无可点击的取消/跳过/稍后控件；WebView 内容为本地 assets 渲染（无网络请求即可出现） |
| **跳转前点击动作与系统设置落地页** | 点击 Continue 后 Activity 切换到 Settings 无障碍列表，列表中出现服务项 ISP Token，其说明为意大利语杀毒文本 | 确认跳转由页面按钮触发、目标正是无障碍设置而非应用详情页，并核对系统列表中展示的服务名与说明是否与页面宣称一致 | Intent action 为 android.settings.ACCESSIBILITY_SETTINGS；系统无障碍列表项标签 ISP Token 与页面"Chrome 更新"话术的矛盾；服务说明文本为"cercare i virus e bloccarli"（扫描并拦截病毒） |
| **拒权后催促循环页（Toast/通知）** | 返回应用后反复出现的 Toast "Open Installed Services, Enable ISP Token service" 与常驻通知（约 3 秒一次） | 区分"一次性引导"与"持续施压"，量化拒权后的复发频率，是判断强迫性的关键运行证据 | Toast 文本与出现周期（约 3000ms）；通知栏常驻项及其取消条件（仅获权后消失）；返回键退出引导页后是否仍持续出现 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.dohpgfr.qarthpc.main._activity_create / _create_act_data`
- `com.dohpgfr.qarthpc.main._create_ui2（assets/pg-*.html 加载与品牌名替换）`
- `com.dohpgfr.qarthpc.main._create_ui3（assets/design.txt、designxiaomi.txt 原生备用页）`
- `com.dohpgfr.qarthpc.main$ResumableSub_check_data.resume（ACCESSIBILITY_SETTINGS 跳转 + 获权后 StartService）`
- `com.dohpgfr.qarthpc.dtrsbnotisuntilactv._timer1_tick（3000ms 催促循环）`
- `res/xml/accessibility_service_config.xml + assets/pg-en.html`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期 UTG 视角）

**总体判断：冷启动 0 步触发，本地 HTML 教学页 + 直接跳系统无障碍设置，无取消入口，拒权后 3 秒 Toast 循环提醒。**

1. **入口是冷启动强制路径**：`main._activity_create` → [main#_create_act_data](<resource-unit:#1.dex1 code:com.dohpgfr.qarthpc.main#_create_act_data>)，仅排除模拟器（`_isemulator`/`_isemulator2`），随后按 `_intdesignver` 走 WebView 版或原生版引导页，与用户是否点击任何业务功能无关。
2. **载体是本地 HTML 全屏 WebView**：[main#_create_ui2](<resource-unit:#1.dex1 code:com.dohpgfr.qarthpc.main#_create_ui2>) 按系统语言从 `assets/pg-{en,it,de,es,fl,gr,pt,se}.html` 读文件，用 `LoadHtml` 全屏 `AddView` 并 `BringToFront`，注册 `B4A` JS 接口。页面标题与正文原文是 `Chrome Update` / `Update your Google Chrome.` / `Activate the "Google Chrome" option.`，运行期被 `replace()` 成 `B4AApplication.getLabelName()`（实际为 `ISP Token`），并注入应用自身图标 base64 到 `appiconhere`。
3. **原生备用页同构**：`_intdesignver != 0` 时走 [main#_create_ui3](<resource-unit:#1.dex1 code:com.dohpgfr.qarthpc.main#_create_ui3>)，文案取自 `assets/design.txt` / `designxiaomi.txt`（"Enable Accessibility Service / 1- Open 'Installed Services' / 2- Find \<app\> / 3- Set Switch ON / Open Settings"），`<app>` 同样替换为应用标签。
4. **跳转点收敛到一处协程**：HTML 的 `Continue`（`.els` 整块 onClick）与原生 `lblsettings` 都回调 `main._check_data` → [ResumableSub_check_data#resume](<resource-unit:#1.dex1 code:com.dohpgfr.qarthpc.main$ResumableSub_check_data#resume>)，在 `isAccessibilityServiceEnabled == false` 时 `StartActivity("android.settings.ACCESSIBILITY_SETTINGS")`；另两条独立路径 [main#_istheaccessibilityserviceenabled](<resource-unit:#1.dex1 code:com.dohpgfr.qarthpc.main#_istheaccessibilityserviceenabled>) 与 [main#_dstrb_not_hndlr](<resource-unit:#1.dex1 code:com.dohpgfr.qarthpc.main#_dstrb_not_hndlr>) 也做同样未开启即跳转。
5. **无取消/跳过**：HTML 与原生页都只有一个主按钮，没有"稍后/跳过/取消"控件，唯一退出方式是按返回键。
6. **拒权反馈循环**：未开启时 `_dstrb_not_hndlr` 启动 `.dtrsbnotisuntilactv`，其 [dtrsbnotisuntilactv#_timer1_tick](<resource-unit:#1.dex1 code:com.dohpgfr.qarthpc.dtrsbnotisuntilactv#_timer1_tick>) 以 3000ms 定时器反复 Toast "Open Installed Services, Enable <应用名> service" 并重建通知，直到 `_isaccactive` 为真才 `StopService`。
7. **获权后动作**：`resume` 在 case 21 直接 `StartService(backgroundservice)`（无障碍主服务），SDK≥34 且无后台定位时再跳 `LOCATION_SOURCE_SETTINGS`，`_ispreinjallfls` 为真时启动 `inj_dnlader` 注入式加载服务。
8. **身份三重矛盾**：桌面名 `ISP Token`；页面框架为"Chrome 更新安装步骤"（品牌名运行期被替换为本应用名，但"更新/安装步骤"叙事保留）；系统无障碍列表说明却是意大利语"帮助系统保护设备、用无障碍事件扫描并拦截病毒"。服务配置 `typeAllMask` + `canRetrieveWindowContent` + `canPerformGestures` + `flagRetrieveInteractiveWindows`，与"杀毒"或"Chrome 更新"均不相符。
9. **边界**：`assets/encrypted_dex.zip` 为加密二阶段载荷，属后续窃取/远控链，不影响本次引导流程的静态可见性；`.forc_activateacc`、`perm_*` 等权限向导 Activity 的 `_activity_create` 为空实现，具体 UI 逻辑在 layout 事件层，未纳入本次 UTG 主链。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导链完整静态可见：入口 main._activity_create→_create_act_data，载体 _create_ui2 读取的 assets/pg-*.html 与 _create_ui3 读取的 design.txt/designxiaomi.txt 均为明文，跳转点 android.settings.ACCESSIBILITY_SETTINGS 出现在 main._istheaccessibilityserviceenabled 与 ResumableSub_check_data.resume，拒权循环在 dtrsbnotisuntilactv._timer1_tick。仅 assets/encrypted_dex.zip 为加密二阶段载荷（与本次引导流程无关，属获权后窃取/远控链）。",
  "summary_one_liner": "冷启动即全屏加载本地 HTML 页面、以\"Chrome 更新/安装步骤\"叙事分步教学并一键跳系统无障碍设置，页面无取消按钮，未开启时用 3 秒定时 Toast 持续催促，获权后直接启动无障碍主服务与注入加载器。",
  "disguise_identity": {
    "app_display_name": "ISP Token",
    "claimed_brand_or_persona": "Google Chrome / Chrome Update（HTML 原文品牌名，运行期被替换为应用自身名称 ISP Token，但\"更新 Chrome、按安装步骤操作\"的叙事保留）；系统无障碍说明另伪装为设备杀毒防护",
    "a11y_service_label": "ISP Token（.backgroundservice 的 android:label；android:description 为意大利语\"帮助系统保护设备、用无障碍事件扫描并拦截病毒\"）",
    "identity_mismatch": true,
    "obfuscation_tricks": "HTML 原文写死 Chrome Update / Google Chrome / appiconhere，运行时被 String.replace 替换为应用自身 label 与应用图标 base64，使页面外观与本应用一致但保留\"更新/安装\"误导叙事；无障碍 description 与 summary 使用意大利语杀毒话术，与页面宣称的浏览器更新及服务真实能力（typeAllMask + canRetrieveWindowContent + canPerformGestures + flagRetrieveInteractiveWindows）均不符；桌面名为无意义品牌 ISP Token"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.dohpgfr.qarthpc.main（LAUNCHER Activity .main）",
      "trigger_event": "_activity_create → _create_act_data，冷启动即执行；仅 _isemulator/_isemulator2 为真时 Toast \"App can't work on Emulators\" 并退出",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "App can't work on Emulators",
      "shown_text_zh": "（仅模拟器环境）应用无法在模拟器上运行",
      "user_action_requested": "真机无需操作，直接进入下一步；无取消/跳过",
      "code_anchor": "com.dohpgfr.qarthpc.main._activity_create / _create_act_data"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "main Activity 上全屏 AddView 的 WebViewWrapper（_webviewextras1 + B4A JS 接口），加载 assets/pg-en.html 等本地 HTML",
      "trigger_event": "_create_act_data 中 _intdesignver==0 时调用 _create_ui2；按系统语言选 pg-de/en/es/fl/gr/it/pt/se.html，缺省回落 pg-en.html",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Chrome Update / Update your Google Chrome. / Click the \"Continue\" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section. / 3 Activate the \"Google Chrome\" option. / Continue",
      "shown_text_zh": "Chrome 更新 / 请更新你的 Google Chrome。/ 点击\"继续\"按钮并按照安装步骤操作。/ 1 打开设置 / 2 在无障碍中打开\"已下载的服务\"或\"已安装的服务\" / 3 启用\"Google Chrome\"选项 / 继续",
      "user_action_requested": "点击底部 Continue（整个 .els 区域均可点击，同一回调），无取消/跳过按钮",
      "code_anchor": "com.dohpgfr.qarthpc.main._create_ui2 + assets/pg-en.html"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "原生 Label 版引导页（_create_ui3，三个 LabelWrapper + 蓝色按钮 lblsettings）",
      "trigger_event": "_create_act_data 中 _intdesignver!=0 时调用 _create_ui3",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Enable Accessibility Service / 1- Open 'Installed Services' / 2- Find <app> / 3- Set Switch ON / Open Settings",
      "shown_text_zh": "启用无障碍服务 / 1- 打开\"已安装的服务\" / 2- 找到 <应用名> / 3- 将开关设为开启 / 打开设置",
      "user_action_requested": "点击 lblsettings（文案\"Open Settings\"），无取消/跳过",
      "code_anchor": "com.dohpgfr.qarthpc.main._create_ui3 + assets/design.txt、assets/designxiaomi.txt"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "B4A.CallSub('check_data') / lblsettings 点击 → main._check_data → ResumableSub_check_data.resume：isAccessibilityServiceEnabled 为 false 时 IntentWrapper.Initialize(\"android.settings.ACCESSIBILITY_SETTINGS\") + StartActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用不渲染该页）",
      "shown_text_zh": "系统无障碍设置列表，其中出现本应用服务项 ISP Token 及其意大利语杀毒说明",
      "user_action_requested": "要求用户手动在系统无障碍列表中找到并开启本应用服务",
      "code_anchor": "com.dohpgfr.qarthpc.main$ResumableSub_check_data.resume（case 10）+ com.dohpgfr.qarthpc.main._check_data"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": ".dtrsbnotisuntilactv 服务（Timer 3000ms + Notification）",
      "trigger_event": "_create_act_data 末尾 _dstrb_not_hndlr 检测服务未启用且 globalparameters._isaccactive 为 false 时 StartService(.dtrsbnotisuntilactv)；其 _service_create 在 _isacc_noti_disturb 为真时 Initialize timer1 3000ms",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Open Installed Services, Enable <应用名> service",
      "shown_text_zh": "打开\"已安装的服务\"，启用 <应用名> 服务",
      "user_action_requested": "持续 Toast 与通知催促用户回到系统设置开启服务；无取消，仅当 isAccessibilityServiceEnabled 变真才 Cancel(111) 并 StopService",
      "code_anchor": "com.dohpgfr.qarthpc.dtrsbnotisuntilactv._timer1_tick / _service_create"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.dohpgfr.qarthpc.backgroundservice（无障碍主服务）+ 可选 inj_dnlader、LOCATION_SOURCE_SETTINGS",
      "trigger_event": "ResumableSub_check_data.resume case 21 StartService(backgroundservice)；SDK>=34 且缺后台定位权限时再 StartActivity(\"android.settings.LOCATION_SOURCE_SETTINGS\")；globalparameters._ispreinjallfls 为真时 StartService(inj_dnlader)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统定位来源设置页（SDK≥34 时叠加）",
      "user_action_requested": "无（获权后自动进入后续能力阶段）；此阶段无撤权确认提示",
      "code_anchor": "com.dohpgfr.qarthpc.main$ResumableSub_check_data.resume（case 19/21/24）"
    }
  ],
  "text_presentation_locations": [
    "冷启动 main Activity 上全屏本地 HTML WebView（assets/pg-en.html、pg-it.html、pg-de.html、pg-es.html、pg-fl.html、pg-gr.html、pg-pt.html、pg-se.html，LoadHtml 渲染，品牌名运行期替换为本应用名）",
    "同一 Activity 的原生 Label 备用页（main._create_ui3，文案来自 assets/design.txt 与 assets/designxiaomi.txt，按语言取 5 条数组）",
    "HTML 内 \"Continue\" 按钮与整个 .els 容器 onClick=\"javascript:B4A.CallSub('check_data', false, '1', '2')\"",
    "原生页 lblsettings 标签（文案\"Open Settings\"，深蓝底色按钮样式）",
    "系统无障碍设置列表中本应用服务项：android:label=\"ISP Token\" + res/xml/accessibility_service_config.xml 的 android:description/@string/accessibility_service_description（意大利语杀毒说明）",
    "未开启时的 Toast 与通知：\"Open Installed Services, Enable <应用名> service\"（main._create_act_data 与 dtrsbnotisuntilactv._timer1_tick 各一处）",
    "网络异常时的 MsgboxAsync：标题 \"No internet\"、正文 \"Please make sure you are connected to the internet\"（ResumableSub_check_data.resume case 6）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome Update",
      "text_zh": "Chrome 更新",
      "source_location": "assets/pg-en.html（标题；_create_ui2 运行期 replace 为应用 label）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update your Google Chrome.",
      "text_zh": "请更新你的 Google Chrome。",
      "source_location": "assets/pg-en.html 第 2 段",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Click the \"Continue\" button and follow the installation steps.",
      "text_zh": "点击\"继续\"按钮并按照安装步骤操作。",
      "source_location": "assets/pg-en.html（p#manual0）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "1 Open settings 2 In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section. 3 Activate the \"Google Chrome\" option.",
      "text_zh": "1 打开设置；2 在无障碍中打开\"已下载的服务\"或\"已安装的服务\"分区；3 启用\"Google Chrome\"选项。",
      "source_location": "assets/pg-en.html（p#manual1-3）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Continue",
      "text_zh": "继续",
      "source_location": "assets/pg-en.html（button#continue）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "it",
      "text_verbatim": "Aggiorna il tuo Google Chrome. Fare clic sul pulsante \"Continua\" e seguire i passaggi di installazione. / In Accessibilità, apri la sezione \"Servizi scaricati\" o \"Servizi installati\". / Attiva l'opzione \"Google Chrome\".",
      "text_zh": "请更新你的 Google Chrome。点击\"继续\"按钮并按安装步骤操作。/ 在无障碍中打开\"已下载的服务\"或\"已安装的服务\"。/ 启用\"Google Chrome\"选项。",
      "source_location": "assets/pg-it.html",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "it",
      "text_verbatim": "Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli.",
      "text_zh": "允许系统保护本设备，使用无障碍事件搜索并拦截病毒。",
      "source_location": "res/values/strings.xml accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description/android:summary 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Service / 1- Open 'Installed Services' / 2- Find <app> / 3- Set Switch ON / Open Settings",
      "text_zh": "启用无障碍服务 / 1- 打开\"已安装的服务\" / 2- 找到 <应用名> / 3- 将开关设为开启 / 打开设置",
      "source_location": "assets/design.txt 与 assets/designxiaomi.txt（en 数组，_create_ui3 读取）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Installed Services, Enable <应用名> service",
      "text_zh": "打开\"已安装的服务\"，启用 <应用名> 服务",
      "source_location": "com.dohpgfr.qarthpc.main._create_act_data / com.dohpgfr.qarthpc.dtrsbnotisuntilactv._timer1_tick（硬编码拼接 B4AApplication.getLabelName()）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please make sure you are connected to the internet",
      "text_zh": "请确保已连接互联网",
      "source_location": "com.dohpgfr.qarthpc.main$ResumableSub_check_data.resume（case 6，MsgboxAsync，标题 No internet）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户按返回键回到应用后再点 Continue/Open Settings 会重新走 _check_data→resume 并再次 StartActivity(ACCESSIBILITY_SETTINGS)；未获权期间 .dtrsbnotisuntilactv 以 3000ms 定时器循环弹 Toast \"Open Installed Services, Enable <应用名> service\" 并重建通知，直至 isAccessibilityServiceEnabled 为真才 Cancel(111)+StopService；冷启动时 _create_act_data 也会重新拉起该服务",
    "overlay_or_fake_settings": "有半屏/全屏叠层：引导页以 WebViewWrapper 覆盖整个 Activity（PerX 100%/PerY 100%，BringToFront）并 setZoomEnabled(false)；未使用 TYPE_ACCESSIBILITY_OVERLAY 或 SYSTEM_ALERT_WINDOW 悬浮遮罩，也未高仿系统无障碍开关页",
    "restricted_settings_13plus_coaching": "无。页面与原生文案只教\"打开设置→无障碍→已安装/已下载服务→开启开关\"，未涉及应用详情右上角菜单允许受限设置，也未使用 Session 安装器绕过",
    "post_grant_anti_removal": "获权后 resume case 21 直接 StartService(backgroundservice)；服务启用即 _service_create 停止定时器与通知。反撤权动作位于引用库 com.ddkyvzr.tesmsbd.AccessibilityEventsListenerWrapper#selfDefense / onServiceConnected 中调用 PerformGlobalAction(1)=BACK、PerformGlobalAction(2)=HOME，属获权后自保能力，本次未逐行确认其触发条件",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动即拉起应用（无需任何点击），在 main Activity 创建后 1–2 秒内截取全屏 WebView 引导页；同时 Hook/monkey 监听 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 的瞬间，用于核对点击 Continue 后的跳转链",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页（本地 HTML WebView，含\"更新\"标题与三步教学）",
        "page_identifier": "全屏 WebView 覆盖 main Activity，标题含\"Chrome Update\"或\"ISP Token\"+ 步骤文本 \"Open settings / In Accessibility, open the Downloaded Services...\" + 底部单按钮 \"Continue\"",
        "why_most_useful": "该页是唯一向用户解释\"为何要去无障碍设置\"的地方，其文案性质（假更新+分步教学）与是否提供取消入口直接决定诱导定性",
        "observable_utg_signals": [
          "标题/正文中\"更新/安装/Update\"叙事与桌面应用名 ISP Token 的不一致",
          "存在 1/2/3 编号的无障碍设置分步教学文本",
          "界面只有一个主按钮、无可点击的取消/跳过/稍后控件",
          "WebView 内容为本地 assets 渲染（无网络请求即可出现）"
        ]
      },
      {
        "page_role": "跳转前点击动作与系统设置落地页",
        "page_identifier": "点击 Continue 后 Activity 切换到 Settings 无障碍列表，列表中出现服务项 ISP Token，其说明为意大利语杀毒文本",
        "why_most_useful": "确认跳转由页面按钮触发、目标正是无障碍设置而非应用详情页，并核对系统列表中展示的服务名与说明是否与页面宣称一致",
        "observable_utg_signals": [
          "Intent action 为 android.settings.ACCESSIBILITY_SETTINGS",
          "系统无障碍列表项标签 ISP Token 与页面\"Chrome 更新\"话术的矛盾",
          "服务说明文本为\"cercare i virus e bloccarli\"（扫描并拦截病毒）"
        ]
      },
      {
        "page_role": "拒权后催促循环页（Toast/通知）",
        "page_identifier": "返回应用后反复出现的 Toast \"Open Installed Services, Enable ISP Token service\" 与常驻通知（约 3 秒一次）",
        "why_most_useful": "区分\"一次性引导\"与\"持续施压\"，量化拒权后的复发频率，是判断强迫性的关键运行证据",
        "observable_utg_signals": [
          "Toast 文本与出现周期（约 3000ms）",
          "通知栏常驻项及其取消条件（仅获权后消失）",
          "返回键退出引导页后是否仍持续出现"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：一是引导页品牌名与图标在运行时被 replace 为本应用 label（ISP Token）与自身图标，纯文本抓取只会看到\"ISP Token Update\"，需结合\"更新/安装步骤\"叙事而非品牌字符串判断；二是 assets/encrypted_dex.zip 为加密二阶段载荷，本流程之后的窃取/远控行为不在静态可见范围内，需动态解密补充。另 .forc_activateacc、perm_* 等权限向导 Activity 的 onCreate 为空实现，UI 逻辑在 layout 事件层，未纳入本次主链。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.dohpgfr.qarthpc.main._activity_create / _create_act_data",
    "com.dohpgfr.qarthpc.main._create_ui2（assets/pg-*.html 加载与品牌名替换）",
    "com.dohpgfr.qarthpc.main._create_ui3（assets/design.txt、designxiaomi.txt 原生备用页）",
    "com.dohpgfr.qarthpc.main$ResumableSub_check_data.resume（ACCESSIBILITY_SETTINGS 跳转 + 获权后 StartService）",
    "com.dohpgfr.qarthpc.dtrsbnotisuntilactv._timer1_tick（3000ms 催促循环）",
    "res/xml/accessibility_service_config.xml + assets/pg-en.html"
  ]
}
```

</details>
