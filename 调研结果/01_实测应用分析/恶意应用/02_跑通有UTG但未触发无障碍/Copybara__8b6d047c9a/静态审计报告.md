# MB_141__8b6d047c9a｜Copybara — Certificato HYPE

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：147.9s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即在全屏本地 HTML 中伪装成『Chrome 更新/Certificato HYPE 证书』，用三步图文加唯一 Continue 按钮把用户直送系统无障碍设置，未授权则每 3 秒 Toast 循环催促，获权后拉起无障碍主服务与 inj_dnlader 二阶段载荷。
- **静态可见性说明**：DEX 未加壳（B4A/Basic4Android），无障碍引导主链（.main 冷启动 → assets/pg-*.html WebView → check_data → ACCESSIBILITY_SETTINGS）完全静态可见；仅原生备用页文案存于 assets/db.db（未解码）与获权后叠层文案由远端下发文件 show_over.txt 提供，属运行期内容，不影响主链可见性。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8b6d047c9a1985c0c15ef0452828e8a77270fe122f51b953d16f0d81c507cce3` |
| 包名 / 年份 | `com.orijucaroma.newicon` / 2024 |
| 家族 / 品类 | **Copybara**（同池样本数：7） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Certificato HYPE |
| 引导页宣称品牌/身份 | HYPE（意大利 HYPE 电子钱包/银行卡证书助手）＋伪造 Google Chrome 官方更新 |
| 系统无障碍列表服务名 | Certificato HYPE（服务 android:label 与桌面名一致，系统无障碍列表项显示为该名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：HTML 模板原文写死 'Chrome Update'/'Google Chrome'，运行时以 Application.getLabelName() 全局替换为 'Certificato HYPE'，一套模板可套任意品牌；a11y 配置 android:settingsActivity 残留第三方包名 'com.com.androidrr.main'；无障碍说明用中英意双语假杀毒话术掩盖读屏/点击能力；全部 Activity 统一打 'Certificato HYPE' 标签、launcher 加 excludeFromRecents |
| 无障碍服务类名 | `.backgroundservice` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：@00000000, @00000000 |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Allows the system to secure your device, It uses the accessibility events to search for viruses and stop them. (Consente al sistema di proteggere il tuo dispositivo, utilizza gli eventi di accessibilità per cercare virus e fermarli.) / Allows the system to secure your device, It uses the accessibility events to search for viruses and stop them. (Consente al sistema di proteggere il tuo dispositivo, utilizza gli eventi di accessibilità per cercare virus e fermarli.) |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.orijucaroma.newicon.main（LAUNCHER，exported，excludeFromRecents，竖屏单例） | onCreate → _activity_create → _create_act_data；先做模拟器检测，命中则 Toast 后 ExitApplication | 原生Activity | **原文**：App can't work on Emulators<br>**译注**：应用无法在模拟器上运行（检测到模拟器即退出，规避沙箱/UTG 环境） | 无（模拟器分支直接退出；真机继续下一步） | `com.orijucaroma.newicon.main._create_act_data` |
| 2 | 冷启动入口 | main Activity 顶部 Toast（原生 Toast） | _create_act_data 内 _isactive_acc() 反射调用 isAccessibilityServiceEnabled 返回 false 时立即弹出 | 原生Activity | **原文**：Open Installed Services, Enable <应用名> service<br>**译注**：打开『已安装的服务』，启用 <应用名> 服务（即指导到系统无障碍列表勾选自身） | 按提示去无障碍设置启用服务（Toast 无按钮，不可取消） | `com.orijucaroma.newicon.main._create_act_data` |
| 3 | 引导说明页 | main Activity 内全屏 WebView（_vvvvvvvvvv3==0 分支，注入 B4A JS 桥） | _create_act_data 末尾调用 _create_ui2()；按 Locale.getDefault().getLanguage() 加载 assets/pg-<lang>.html，缺语言回落 pg-en.html | 本地HTML WebView | **原文**：Chrome Update / Update your Google Chrome. / Click the "Continue" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the "Downloaded Services" or "Installed Services" section. / 3 Activate the "Google Chrome" option. / Continue（运行时 'Chrome Update' 与 'Google Chrome' 被替换为 'Certificato HYPE'）<br>**译注**：Chrome 更新 / 请更新您的 Google Chrome。/ 点击『继续』按钮并按照安装步骤操作。1 打开设置；2 在无障碍中打开『已下载的服务』或『已安装的服务』；3 激活『Google Chrome（实为 Certificato HYPE）』选项。/ 继续 | 只提供唯一蓝色『继续(Continue)』按钮，无取消/关闭/跳过入口，点击触发 JS→B4A.CallSub('check_data') | `com.orijucaroma.newicon.main._create_ui2 + assets/pg-en.html（pg-de/it/es/pt/fl/gr/se 同模板多语言）` |
| 4 | 引导说明页 | main Activity 原生备用引导页（多个 Label + 蓝色 lblsettings 按钮） | _create_act_data 中 _vvvvvvvvvv3 != 0 时改调 _create_ui3() | 原生Activity | **原文**：无（标题/正文/按钮文案由 _design2_map_strings(lang) 从 assets/db.db 读取，正文含 <app> 占位符）<br>**译注**：原生版引导页：标题 + 三段说明（<app> 替换为 Certificato HYPE）+ 可点击的深蓝按钮 | 点击 lblsettings 按钮 → _lblsettings_click → _check_data，同样无取消入口 | `com.orijucaroma.newicon.main._create_ui3 / _lblsettings_click` |
| 5 | 业务功能触发 | main$ResumableSub_check_data（异步流程） | HTML『继续』按钮的 B4A.CallSub('check_data') 或原生 lblsettings 点击 | 原生Dialog | **原文**：Please make sure you are connected to the internet / No internet<br>**译注**：请确认已连接网络 / 无网络（无网时弹窗，仍不提供退出引导的选项） | 仅能确认弹窗；联网后继续走无障碍检测与跳转 | `com.orijucaroma.newicon.main$ResumableSub_check_data#resume` |
| 6 | 跳无障碍设置 | 系统设置 · 无障碍（android.settings.ACCESSIBILITY_SETTINGS） | resume 中反射 isAccessibilityServiceEnabled==false → Intent('android.settings.ACCESSIBILITY_SETTINGS') + Common.StartActivity（_istheaccessibilityserviceenabled 为同逻辑第二处跳转点） | 系统无障碍页 | **原文**：Allows the system to secure your device, It uses the accessibility events to search for viruses and stop them. (Consente al sistema di proteggere il tuo dispositivo, utilizza gli eventi di accessibilità per cercare virus e fermarli.)<br>**译注**：允许系统保护您的设备，它使用无障碍事件搜索病毒并阻止它们。（英意双语说明，服务名显示为 Certificato HYPE） | 在系统无障碍『已下载的服务』中手动打开 Certificato HYPE 开关（Android 13 上还需先解除受限设置，App 未提供该步教学） | `com.orijucaroma.newicon.main$ResumableSub_check_data#resume / main._istheaccessibilityserviceenabled` |
| 7 | 拒权反馈循环 | com.orijucaroma.newicon.dtrsbnotisuntilactv（导出服务，Timer 3000ms） | _service_create 中 globalparameters._isacc_noti_disturb 为真 → Timer.Initialize(processBA,"timer1",3000L)；每次 timer1_tick 执行 | 通知栏 | **原文**：Open Installed Services, Enable <应用名> service<br>**译注**：每 3 秒重复弹出『打开已安装的服务，启用 <应用名> 服务』，用户返回 App 或停留时持续催促 | 被迫再次前往无障碍设置开启；无停止/跳过按钮，仅当内部开关位 _vvvvv7 置真才停止服务 | `com.orijucaroma.newicon.dtrsbnotisuntilactv._timer1_tick / _service_create` |
| 8 | 获权后动作 | backgroundservice（无障碍主服务）+ inj_dnlader（注入式二阶段载荷服务） | resume 中若 backgroundservice 处于暂停则 Common.StartService；若 globalparameters._vvvvvvv1 为真再启动 inj_dnlader | 不可静态还原 | **原文**：无（后台服务启动，无界面）<br>**译注**：获得无障碍权限后立即接管无障碍事件并拉起下载/注入型载荷服务，进入后续窃取与远控阶段 | 无需操作，用户已授权 | `com.orijucaroma.newicon.main$ResumableSub_check_data#resume（case 11-16）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- main Activity 内全屏 WebView 加载 assets/pg-en.html（及 pg-it/de/es/pt/fl/gr/se 多语言副本），标题『Chrome Update』与步骤中的『Google Chrome』在 LoadHtml 前被替换为 Certificato HYPE
- main._create_act_data 中的原生 Toast『Open Installed Services, Enable <label> service』
- main._create_ui3 原生备用引导页：标题 Label + 三段说明 Label（<app> 替换为应用名）+ 深蓝 lblsettings 按钮（文案来自 assets/db.db）
- dtrsbnotisuntilactv 每 3 秒一次的原生 Toast 催促（同样的 Installed Services 文案）
- ResumableSub_check_data 中的 MsgboxAsync 网络提示弹窗（No internet）
- 系统无障碍列表项：服务 android:label=Certificato HYPE + @string/accessibility_service_description 的英意双语『查杀病毒』说明
- 获权后由 backgroundservice._show_ovr 依据 internal/show_over.txt（toptitle/bottomtitle/imgurl/bcolor，远端下发）构造的悬浮叠层

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome Update | Chrome 更新 | `assets/pg-en.html #welcome（运行时被替换为应用名 Certificato HYPE）` | 假更新 |
| en | Update your Google Chrome. | 请更新您的 Google Chrome。 | `assets/pg-en.html #updated（运行时替换为 Certificato HYPE）` | 假更新 |
| en | Click the "Continue" button and follow the installation steps. | 点击『继续』按钮并按照安装步骤操作。 | `assets/pg-en.html #manual0` | 受限设置分步教学 |
| en | Open settings | 打开设置 | `assets/pg-en.html #manual1` | 受限设置分步教学 |
| en | In Accessibility, open the "Downloaded Services" or "Installed Services" section. | 在无障碍中打开『已下载的服务』或『已安装的服务』部分。 | `assets/pg-en.html #manual2` | 受限设置分步教学 |
| en | Activate the "Google Chrome" option. | 激活『Google Chrome』选项。（运行时显示为『Certificato HYPE』，与系统无障碍列表项同名） | `assets/pg-en.html #manual3（被 getLabelName 替换）` | 教唆忽视警告 |
| de | Klicken Sie auf die Schaltfläche „Weiter“ und folgen Sie den Installationsschritten. / Einstellungen öffnen / Öffnen Sie in Barrierefreiheit den Abschnitt „Heruntergeladene Dienste“ oder „Installierte Dienste“. / Aktivieren Sie die Option „Google Chrome“. / Weitermachen | 点击『继续』按钮并按照安装步骤操作。/ 打开设置 / 在无障碍中打开『已下载的服务』或『已安装的服务』。/ 激活『Google Chrome』选项。/ 继续 | `assets/pg-de.html` | 受限设置分步教学 |
| en/it | Allows the system to secure your device, It uses the accessibility events to search for viruses and stop them. (Consente al sistema di proteggere il tuo dispositivo, utilizza gli eventi di accessibilità per cercare virus e fermarli.) | 允许系统保护您的设备，它使用无障碍事件搜索病毒并阻止它们。（意大利语同义重复） | `res/values/strings.xml accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）` | 假反诈安全 |
| en | Open Installed Services, Enable <应用名> service | 打开『已安装的服务』，启用 <应用名> 服务 | `main._create_act_data 与 dtrsbnotisuntilactv._timer1_tick 硬编码字符串` | 受限设置分步教学 |
| en | Please make sure you are connected to the internet / No internet | 请确认已连接网络 / 无网络 | `main$ResumableSub_check_data#resume 硬编码 MsgboxAsync` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：①dtrsbnotisuntilactv 在 _isacc_noti_disturb 为真时以 3000ms Timer 无限循环 Toast『Open Installed Services, Enable <应用名> service』，只有内部开关位 _vvvvv7 置真才 StopService；②每次回到 main 都重新执行 _create_act_data（WebView 引导页重建 + 未授权 Toast），点击『继续』再次 StartActivity 跳无障碍设置，形成返回即重跳的死循环；③全程无取消/跳过按钮
- **遮罩叠层 / 高仿系统设置页**：无高仿系统无障碍开关页；但具备叠层能力：manifest 申请 SYSTEM_ALERT_WINDOW 并提供 perm_activateoverlay 引导 Activity，获权后 backgroundservice._show_ovr 依据远端下发的 internal/show_over.txt（toptitle/bottomtitle/imgurl/bcolor）构造悬浮叠层
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdk 33，全文检索未发现 'Restricted setting'/'允许受限设置'/'Allow restricted settings' 等字符串，也未调用 ACTION_MANAGE_* 或 Session 安装器绕过路径；Android 13+ 上该服务被受限设置拦截时应用无对应教学，仅反复跳系统无障碍页
- **获权后即时行为与防撤权机制**：本轮未静态核验到获权后自点确认或自授权代码；预筛线索显示存在 PERFORM_GLOBAL_ACTION / GLOBAL_BACK / GLOBAL_HOME / WATCH_SETTINGS 相关实现（用于监听设置页并回退退出），具体函数链未逐条展开
- **良性降级 / 替代方案**：无（未授权不降级，只有 Toast/循环催促与重复跳转）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 1.5~3 秒内（模拟器检测之后、WebView 引导页渲染完成时）即拉起；同时监测 Intent 'android.settings.ACCESSIBILITY_SETTINGS' 的 Activity 启动时刻，在其后 800ms~1.5s 再抓一帧系统无障碍页，可同时拿到『引导页』与『服务列表项』两类证据
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导页文案为纯文本节点，无需 OCR；但需注意三点盲区：①模拟器检测命中会 Toast『App can't work on Emulators』后 ExitApplication，UTG 若在模拟器/仿真环境运行将看不到后续引导页，建议在真机或已伪装设备指纹环境取证；②原生备用引导页（_create_ui3）文案取自 assets/db.db，若 WebView 分支未走则该页文本需另行提取；③获权后的悬浮叠层文案由远端 show_over.txt 下发，纯静态不可见，需联网运行才能捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（本地 HTML WebView，假 Chrome 更新）** | 全屏 WebView，标题为『Chrome Update』/应用名，蓝色 Continue 按钮 + 三步编号图文；无返回/关闭控件，Activity 为 com.orijucaroma.newicon.main | 这是诱导话术的原始载体，能直接证明『假更新 + 无障碍分步教学 + 唯一继续按钮』三要素同时存在，且证明品牌名是被模板替换而非真实身份 | 文本节点 Chrome Update / Update your Google Chrome（未替换则说明语言包缺失回落）；文本节点 Open settings / In Accessibility, open the "Downloaded Services" or "Installed Services" section / Activate the "..." option；唯一按钮 Continue 且无取消/跳过同级节点；页面为本地 assets 加载（无地址栏、无网络请求域名） |
| **跳转前 Toast 催促（冷启动未授权分支）** | 系统 Toast 文本『Open Installed Services, Enable <应用名> service』，可与 WebView 引导页同屏出现 | 证明应用在用户尚未做任何操作时即主动指示去无障碍列表启用自身，属于冷启动即索取无障碍权限 | Toast 文本含 Installed Services / Enable ... service；Toast 出现时间点早于任何用户点击 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务，条目名『Certificato HYPE』，下方描述为英意双语『search for viruses and stop them』 | 可直接对比『应用名/服务名 = HYPE 证书』与『说明 = 杀毒工具』的身份与功能双重错位，是判定冒充与虚假功能的关键静态-运行期交叉证据 | 列表项 label = Certificato HYPE；description 含 secure your device / search for viruses；服务开关初始为关闭，需用户手动开启 |
| **拒权/返回后的循环催促页** | 用户从无障碍页返回后重新出现的同一 WebView 引导页 + 每 3 秒一次的 Toast | 证明无良性降级、存在拒权反馈循环（返回即重跳、定时器反复催促） | 返回后 0.5s 内再次出现同一引导页；3 秒间隔重复 Toast 文本；页面无『稍后再说/跳过/仅浏览』类按钮 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.orijucaroma.newicon.main._create_act_data`
- `com.orijucaroma.newicon.main._create_ui2`
- `com.orijucaroma.newicon.main$ResumableSub_check_data#resume`
- `com.orijucaroma.newicon.main._istheaccessibilityserviceenabled`
- `com.orijucaroma.newicon.dtrsbnotisuntilactv._timer1_tick`
- `assets/pg-en.html`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（Copybara 家族 B4A 样本，包名 `com.orijucaroma.newicon`）

**核心手法：假"Chrome 更新"本地 HTML 教学页 → 一键跳系统无障碍设置，全程无取消/跳过按钮，未授权时每 3 秒 Toast 循环催促。**

- **身份伪装**：桌面名/所有 Activity 标签均为 `Certificato HYPE`（意大利 HYPE 电子钱包/银行卡身份），但界面文案模板原文是 **"Chrome Update / Update your Google Chrome"**，运行时用 `Application.getLabelName()` 把 `"Chrome Update"`、`"Google Chrome"` 全部替换成 `Certificato HYPE`——即同一套模板可套任意品牌，本样本落地为伪造 HYPE 与伪造 Chrome 更新的双重身份。无障碍服务在系统列表中显示名同为 `Certificato HYPE`，说明文案则自称"查杀病毒、保护设备"（假杀毒）。a11y 配置里 `android:settingsActivity="com.com.androidrr.main"` 是残留的另一个包名，与自身包名不符。
- **引导载体**：`.main`（launcher，`excludeFromRecents`）冷启动 → `_create_act_data` → `_create_ui2()` 全屏 `WebView` 加载 **assets 本地 HTML**（按 `Locale.getDefault().getLanguage()` 选 `pg-xx.html`，缺语言回落 `pg-en.html`），注入 `B4A` JS 桥，`LoadHtml` 前替换品牌名与 `appiconhere` 为自身图标 base64。页面只有一个蓝色 `Continue` 按钮（`onClick=B4A.CallSub('check_data')`），三步图文教用户"设置 → 无障碍 → 已下载的服务 → 激活 Google Chrome（实际显示为 Certificato HYPE）"。
- **备用原生页**：`_vvvvvvvvvv3 != 0` 时走 `_create_ui3()`，用原生 `Label` 拼标题/正文/蓝色 `lblsettings` 按钮（文案取自 `assets/db.db`，`<app>` 占位替换），点击同样进 `_check_data`。
- **跳转点**：`ResumableSub_check_data.resume` 先判网络（无网 `MsgboxAsync("Please make sure you are connected to the internet","No internet")`），再反射调用 `isAccessibilityServiceEnabled`，未开启即 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 直跳系统无障碍页；`_istheaccessibilityserviceenabled` 为同逻辑的第二处跳转点。**未见任何 `Allow restricted settings` / 受限设置分步教学**（targetSdk 33，Android 13 上该服务会被"受限设置"拦截，样本未做对应引导）。
- **拒权反馈循环**：`dtrsbnotisuntilactv` 服务在 `globalparameters._isacc_noti_disturb` 为真时启动 3000ms `Timer`，每 tick 都 Toast `"Open Installed Services, Enable <应用名> service"`，直到开关位关闭——形成不间断催促，且用户每次回到 App 都会再次被引导页+跳设置。
- **获权后**：`resume` 继续拉起 `backgroundservice`（无障碍主体），并在 `globalparameters._vvvvvvv1` 为真时启动 `inj_dnlader`（注入式二阶段下载/载荷服务）；`backgroundservice._show_ovr` 还会读取 `internal/show_over.txt` 的 `toptitle/bottomtitle/imgurl/bcolor` 构造叠层，说明叠层文案由远端下发（本次未静态展开其网络下发链）。

**覆盖边界**：B4A 代码未加壳，上述流程静态完全可见；`db.db` 内原生页文案、`show_over.txt` 远端叠层内容未解码，`_show_ovr` 反编译为回退指令流仅部分读取；`GLOBAL_BACK/HOME`、`WATCH_SETTINGS` 等防撤权动作本轮未逐函数核验。受本轮 14 次工具调用上限约束，未写入风险台账与报告。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳（B4A/Basic4Android），无障碍引导主链（.main 冷启动 → assets/pg-*.html WebView → check_data → ACCESSIBILITY_SETTINGS）完全静态可见；仅原生备用页文案存于 assets/db.db（未解码）与获权后叠层文案由远端下发文件 show_over.txt 提供，属运行期内容，不影响主链可见性。",
  "summary_one_liner": "冷启动即在全屏本地 HTML 中伪装成『Chrome 更新/Certificato HYPE 证书』，用三步图文加唯一 Continue 按钮把用户直送系统无障碍设置，未授权则每 3 秒 Toast 循环催促，获权后拉起无障碍主服务与 inj_dnlader 二阶段载荷。",
  "disguise_identity": {
    "app_display_name": "Certificato HYPE",
    "claimed_brand_or_persona": "HYPE（意大利 HYPE 电子钱包/银行卡证书助手）＋伪造 Google Chrome 官方更新",
    "a11y_service_label": "Certificato HYPE（服务 android:label 与桌面名一致，系统无障碍列表项显示为该名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "HTML 模板原文写死 'Chrome Update'/'Google Chrome'，运行时以 Application.getLabelName() 全局替换为 'Certificato HYPE'，一套模板可套任意品牌；a11y 配置 android:settingsActivity 残留第三方包名 'com.com.androidrr.main'；无障碍说明用中英意双语假杀毒话术掩盖读屏/点击能力；全部 Activity 统一打 'Certificato HYPE' 标签、launcher 加 excludeFromRecents"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.orijucaroma.newicon.main（LAUNCHER，exported，excludeFromRecents，竖屏单例）",
      "trigger_event": "onCreate → _activity_create → _create_act_data；先做模拟器检测，命中则 Toast 后 ExitApplication",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "App can't work on Emulators",
      "shown_text_zh": "应用无法在模拟器上运行（检测到模拟器即退出，规避沙箱/UTG 环境）",
      "user_action_requested": "无（模拟器分支直接退出；真机继续下一步）",
      "code_anchor": "com.orijucaroma.newicon.main._create_act_data"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "main Activity 顶部 Toast（原生 Toast）",
      "trigger_event": "_create_act_data 内 _isactive_acc() 反射调用 isAccessibilityServiceEnabled 返回 false 时立即弹出",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Open Installed Services, Enable <应用名> service",
      "shown_text_zh": "打开『已安装的服务』，启用 <应用名> 服务（即指导到系统无障碍列表勾选自身）",
      "user_action_requested": "按提示去无障碍设置启用服务（Toast 无按钮，不可取消）",
      "code_anchor": "com.orijucaroma.newicon.main._create_act_data"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "main Activity 内全屏 WebView（_vvvvvvvvvv3==0 分支，注入 B4A JS 桥）",
      "trigger_event": "_create_act_data 末尾调用 _create_ui2()；按 Locale.getDefault().getLanguage() 加载 assets/pg-<lang>.html，缺语言回落 pg-en.html",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Chrome Update / Update your Google Chrome. / Click the \"Continue\" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section. / 3 Activate the \"Google Chrome\" option. / Continue（运行时 'Chrome Update' 与 'Google Chrome' 被替换为 'Certificato HYPE'）",
      "shown_text_zh": "Chrome 更新 / 请更新您的 Google Chrome。/ 点击『继续』按钮并按照安装步骤操作。1 打开设置；2 在无障碍中打开『已下载的服务』或『已安装的服务』；3 激活『Google Chrome（实为 Certificato HYPE）』选项。/ 继续",
      "user_action_requested": "只提供唯一蓝色『继续(Continue)』按钮，无取消/关闭/跳过入口，点击触发 JS→B4A.CallSub('check_data')",
      "code_anchor": "com.orijucaroma.newicon.main._create_ui2 + assets/pg-en.html（pg-de/it/es/pt/fl/gr/se 同模板多语言）"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "main Activity 原生备用引导页（多个 Label + 蓝色 lblsettings 按钮）",
      "trigger_event": "_create_act_data 中 _vvvvvvvvvv3 != 0 时改调 _create_ui3()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（标题/正文/按钮文案由 _design2_map_strings(lang) 从 assets/db.db 读取，正文含 <app> 占位符）",
      "shown_text_zh": "原生版引导页：标题 + 三段说明（<app> 替换为 Certificato HYPE）+ 可点击的深蓝按钮",
      "user_action_requested": "点击 lblsettings 按钮 → _lblsettings_click → _check_data，同样无取消入口",
      "code_anchor": "com.orijucaroma.newicon.main._create_ui3 / _lblsettings_click"
    },
    {
      "step": 5,
      "stage": "业务功能触发",
      "screen_or_component": "main$ResumableSub_check_data（异步流程）",
      "trigger_event": "HTML『继续』按钮的 B4A.CallSub('check_data') 或原生 lblsettings 点击",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please make sure you are connected to the internet / No internet",
      "shown_text_zh": "请确认已连接网络 / 无网络（无网时弹窗，仍不提供退出引导的选项）",
      "user_action_requested": "仅能确认弹窗；联网后继续走无障碍检测与跳转",
      "code_anchor": "com.orijucaroma.newicon.main$ResumableSub_check_data#resume"
    },
    {
      "step": 6,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 · 无障碍（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "resume 中反射 isAccessibilityServiceEnabled==false → Intent('android.settings.ACCESSIBILITY_SETTINGS') + Common.StartActivity（_istheaccessibilityserviceenabled 为同逻辑第二处跳转点）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Allows the system to secure your device, It uses the accessibility events to search for viruses and stop them. (Consente al sistema di proteggere il tuo dispositivo, utilizza gli eventi di accessibilità per cercare virus e fermarli.)",
      "shown_text_zh": "允许系统保护您的设备，它使用无障碍事件搜索病毒并阻止它们。（英意双语说明，服务名显示为 Certificato HYPE）",
      "user_action_requested": "在系统无障碍『已下载的服务』中手动打开 Certificato HYPE 开关（Android 13 上还需先解除受限设置，App 未提供该步教学）",
      "code_anchor": "com.orijucaroma.newicon.main$ResumableSub_check_data#resume / main._istheaccessibilityserviceenabled"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.orijucaroma.newicon.dtrsbnotisuntilactv（导出服务，Timer 3000ms）",
      "trigger_event": "_service_create 中 globalparameters._isacc_noti_disturb 为真 → Timer.Initialize(processBA,\"timer1\",3000L)；每次 timer1_tick 执行",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Open Installed Services, Enable <应用名> service",
      "shown_text_zh": "每 3 秒重复弹出『打开已安装的服务，启用 <应用名> 服务』，用户返回 App 或停留时持续催促",
      "user_action_requested": "被迫再次前往无障碍设置开启；无停止/跳过按钮，仅当内部开关位 _vvvvv7 置真才停止服务",
      "code_anchor": "com.orijucaroma.newicon.dtrsbnotisuntilactv._timer1_tick / _service_create"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "backgroundservice（无障碍主服务）+ inj_dnlader（注入式二阶段载荷服务）",
      "trigger_event": "resume 中若 backgroundservice 处于暂停则 Common.StartService；若 globalparameters._vvvvvvv1 为真再启动 inj_dnlader",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（后台服务启动，无界面）",
      "shown_text_zh": "获得无障碍权限后立即接管无障碍事件并拉起下载/注入型载荷服务，进入后续窃取与远控阶段",
      "user_action_requested": "无需操作，用户已授权",
      "code_anchor": "com.orijucaroma.newicon.main$ResumableSub_check_data#resume（case 11-16）"
    }
  ],
  "text_presentation_locations": [
    "main Activity 内全屏 WebView 加载 assets/pg-en.html（及 pg-it/de/es/pt/fl/gr/se 多语言副本），标题『Chrome Update』与步骤中的『Google Chrome』在 LoadHtml 前被替换为 Certificato HYPE",
    "main._create_act_data 中的原生 Toast『Open Installed Services, Enable <label> service』",
    "main._create_ui3 原生备用引导页：标题 Label + 三段说明 Label（<app> 替换为应用名）+ 深蓝 lblsettings 按钮（文案来自 assets/db.db）",
    "dtrsbnotisuntilactv 每 3 秒一次的原生 Toast 催促（同样的 Installed Services 文案）",
    "ResumableSub_check_data 中的 MsgboxAsync 网络提示弹窗（No internet）",
    "系统无障碍列表项：服务 android:label=Certificato HYPE + @string/accessibility_service_description 的英意双语『查杀病毒』说明",
    "获权后由 backgroundservice._show_ovr 依据 internal/show_over.txt（toptitle/bottomtitle/imgurl/bcolor，远端下发）构造的悬浮叠层"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome Update",
      "text_zh": "Chrome 更新",
      "source_location": "assets/pg-en.html #welcome（运行时被替换为应用名 Certificato HYPE）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update your Google Chrome.",
      "text_zh": "请更新您的 Google Chrome。",
      "source_location": "assets/pg-en.html #updated（运行时替换为 Certificato HYPE）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Click the \"Continue\" button and follow the installation steps.",
      "text_zh": "点击『继续』按钮并按照安装步骤操作。",
      "source_location": "assets/pg-en.html #manual0",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Open settings",
      "text_zh": "打开设置",
      "source_location": "assets/pg-en.html #manual1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section.",
      "text_zh": "在无障碍中打开『已下载的服务』或『已安装的服务』部分。",
      "source_location": "assets/pg-en.html #manual2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Activate the \"Google Chrome\" option.",
      "text_zh": "激活『Google Chrome』选项。（运行时显示为『Certificato HYPE』，与系统无障碍列表项同名）",
      "source_location": "assets/pg-en.html #manual3（被 getLabelName 替换）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "de",
      "text_verbatim": "Klicken Sie auf die Schaltfläche „Weiter“ und folgen Sie den Installationsschritten. / Einstellungen öffnen / Öffnen Sie in Barrierefreiheit den Abschnitt „Heruntergeladene Dienste“ oder „Installierte Dienste“. / Aktivieren Sie die Option „Google Chrome“. / Weitermachen",
      "text_zh": "点击『继续』按钮并按照安装步骤操作。/ 打开设置 / 在无障碍中打开『已下载的服务』或『已安装的服务』。/ 激活『Google Chrome』选项。/ 继续",
      "source_location": "assets/pg-de.html",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en/it",
      "text_verbatim": "Allows the system to secure your device, It uses the accessibility events to search for viruses and stop them. (Consente al sistema di proteggere il tuo dispositivo, utilizza gli eventi di accessibilità per cercare virus e fermarli.)",
      "text_zh": "允许系统保护您的设备，它使用无障碍事件搜索病毒并阻止它们。（意大利语同义重复）",
      "source_location": "res/values/strings.xml accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Installed Services, Enable <应用名> service",
      "text_zh": "打开『已安装的服务』，启用 <应用名> 服务",
      "source_location": "main._create_act_data 与 dtrsbnotisuntilactv._timer1_tick 硬编码字符串",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please make sure you are connected to the internet / No internet",
      "text_zh": "请确认已连接网络 / 无网络",
      "source_location": "main$ResumableSub_check_data#resume 硬编码 MsgboxAsync",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "①dtrsbnotisuntilactv 在 _isacc_noti_disturb 为真时以 3000ms Timer 无限循环 Toast『Open Installed Services, Enable <应用名> service』，只有内部开关位 _vvvvv7 置真才 StopService；②每次回到 main 都重新执行 _create_act_data（WebView 引导页重建 + 未授权 Toast），点击『继续』再次 StartActivity 跳无障碍设置，形成返回即重跳的死循环；③全程无取消/跳过按钮",
    "overlay_or_fake_settings": "无高仿系统无障碍开关页；但具备叠层能力：manifest 申请 SYSTEM_ALERT_WINDOW 并提供 perm_activateoverlay 引导 Activity，获权后 backgroundservice._show_ovr 依据远端下发的 internal/show_over.txt（toptitle/bottomtitle/imgurl/bcolor）构造悬浮叠层",
    "restricted_settings_13plus_coaching": "无。targetSdk 33，全文检索未发现 'Restricted setting'/'允许受限设置'/'Allow restricted settings' 等字符串，也未调用 ACTION_MANAGE_* 或 Session 安装器绕过路径；Android 13+ 上该服务被受限设置拦截时应用无对应教学，仅反复跳系统无障碍页",
    "post_grant_anti_removal": "本轮未静态核验到获权后自点确认或自授权代码；预筛线索显示存在 PERFORM_GLOBAL_ACTION / GLOBAL_BACK / GLOBAL_HOME / WATCH_SETTINGS 相关实现（用于监听设置页并回退退出），具体函数链未逐条展开",
    "benign_graceful_degradation": "无（未授权不降级，只有 Toast/循环催促与重复跳转）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 1.5~3 秒内（模拟器检测之后、WebView 引导页渲染完成时）即拉起；同时监测 Intent 'android.settings.ACCESSIBILITY_SETTINGS' 的 Activity 启动时刻，在其后 800ms~1.5s 再抓一帧系统无障碍页，可同时拿到『引导页』与『服务列表项』两类证据",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（本地 HTML WebView，假 Chrome 更新）",
        "page_identifier": "全屏 WebView，标题为『Chrome Update』/应用名，蓝色 Continue 按钮 + 三步编号图文；无返回/关闭控件，Activity 为 com.orijucaroma.newicon.main",
        "why_most_useful": "这是诱导话术的原始载体，能直接证明『假更新 + 无障碍分步教学 + 唯一继续按钮』三要素同时存在，且证明品牌名是被模板替换而非真实身份",
        "observable_utg_signals": ["文本节点 Chrome Update / Update your Google Chrome（未替换则说明语言包缺失回落）", "文本节点 Open settings / In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section / Activate the \"...\" option", "唯一按钮 Continue 且无取消/跳过同级节点", "页面为本地 assets 加载（无地址栏、无网络请求域名）"]
      },
      {
        "page_role": "跳转前 Toast 催促（冷启动未授权分支）",
        "page_identifier": "系统 Toast 文本『Open Installed Services, Enable <应用名> service』，可与 WebView 引导页同屏出现",
        "why_most_useful": "证明应用在用户尚未做任何操作时即主动指示去无障碍列表启用自身，属于冷启动即索取无障碍权限",
        "observable_utg_signals": ["Toast 文本含 Installed Services / Enable ... service", "Toast 出现时间点早于任何用户点击"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，条目名『Certificato HYPE』，下方描述为英意双语『search for viruses and stop them』",
        "why_most_useful": "可直接对比『应用名/服务名 = HYPE 证书』与『说明 = 杀毒工具』的身份与功能双重错位，是判定冒充与虚假功能的关键静态-运行期交叉证据",
        "observable_utg_signals": ["列表项 label = Certificato HYPE", "description 含 secure your device / search for viruses", "服务开关初始为关闭，需用户手动开启"]
      },
      {
        "page_role": "拒权/返回后的循环催促页",
        "page_identifier": "用户从无障碍页返回后重新出现的同一 WebView 引导页 + 每 3 秒一次的 Toast",
        "why_most_useful": "证明无良性降级、存在拒权反馈循环（返回即重跳、定时器反复催促）",
        "observable_utg_signals": ["返回后 0.5s 内再次出现同一引导页", "3 秒间隔重复 Toast 文本", "页面无『稍后再说/跳过/仅浏览』类按钮"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导页文案为纯文本节点，无需 OCR；但需注意三点盲区：①模拟器检测命中会 Toast『App can't work on Emulators』后 ExitApplication，UTG 若在模拟器/仿真环境运行将看不到后续引导页，建议在真机或已伪装设备指纹环境取证；②原生备用引导页（_create_ui3）文案取自 assets/db.db，若 WebView 分支未走则该页文本需另行提取；③获权后的悬浮叠层文案由远端 show_over.txt 下发，纯静态不可见，需联网运行才能捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.orijucaroma.newicon.main._create_act_data",
    "com.orijucaroma.newicon.main._create_ui2",
    "com.orijucaroma.newicon.main$ResumableSub_check_data#resume",
    "com.orijucaroma.newicon.main._istheaccessibilityserviceenabled",
    "com.orijucaroma.newicon.dtrsbnotisuntilactv._timer1_tick",
    "assets/pg-en.html"
  ]
}
```

</details>
