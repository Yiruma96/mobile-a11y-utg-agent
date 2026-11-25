# MB_138__bf56b2f456｜Copybara — My BNL

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：149.9s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即以本地 HTML 全屏覆盖主界面冒充「Chrome Update」，把应用图标与名称注入页面，分步教学用户进系统无障碍「已安装的服务」启用其服务，未启用时每 3 秒弹通知+Toast 持续催促。
- **静态可见性说明**：无障碍诱导全流程完整静态可见：引导页为本地 assets/pg-*.html（八语种），跳转与催促逻辑在 com.sqhiibt.wdqknqa.main 与 dtrsbnotisuntilactv 的 DEX 代码中明文可读，无加壳、无远端 HTML。包内另有 assets/encrypted_dex.zip（约 3.4MB）加密二阶段载荷，属于后续恶意载荷环节，不参与本无障碍引导链。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `bf56b2f45649c5aa8dc8195364af66277171398ba642330e44c67239c3fef52b` |
| 包名 / 年份 | `com.sqhiibt.wdqknqa` / 2025 |
| 家族 / 品类 | **Copybara**（同池样本数：7） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | My BNL |
| 引导页宣称品牌/身份 | Google Chrome 更新（Chrome Update） |
| 系统无障碍列表服务名 | My BNL |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：引导 HTML 中标题写死为「Chrome Update」「Google Chrome」，运行时由 _create_ui2 用 Common.Application.getLabelName() 整体替换为应用名、并以 Base64 注入本应用图标，使页面与图标看起来像同一应用；系统无障碍描述使用意大利语伪安全话术「查找并阻止病毒」，与桌面名及页面宣称均不一致；应用内 20 余个 Activity 统一 label="My BNL" 且全部 exported=true，另有 faknotiactivity 等仿通知类组件。 |
| 无障碍服务类名 | `.backgroundservice` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli). / Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli). |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sqhiibt.wdqknqa.main（LAUNCHER Activity，android:label="My BNL"） | onCreate → _activity_create → _create_act_data（先做 _isemulator/_isemulator2 检测，模拟器直接 ExitApplication） | 原生Activity | **原文**：Open Installed Services, Enable  + Common.Application.getLabelName() +  service（ToastMessageShow，见 _create_act_data / _timer1_tick）<br>**译注**：「打开已安装的服务，启用 My BNL 服务」——启动即以 Toast 提示用户去无障碍已安装服务中启用本应用。 | 无按钮，仅被动提示；页面随后被 WebView 完全覆盖 | `com.sqhiibt.wdqknqa.main#_create_act_data / com.sqhiibt.wdqknqa.main#_isemulator` |
| 2 | 引导说明页 | main Activity 内动态添加的全屏 WebView（WebViewWrapper 100% 宽高 + BringToFront），加载 assets/pg-<lang>.html | _create_act_data 内 _intdesignver==0 时调 _create_ui2()；语言由 _getphonelanguage_unicode() 决定，缺省 en | 本地HTML WebView | **原文**：Chrome Update / Update your Google Chrome. / Click the "Continue" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the "Downloaded Services" or "Installed Services" section. / 3 Activate the "Google Chrome" option. / 4 Continue<br>**译注**：「Chrome 更新」/「更新您的 Google Chrome。」/「点击『继续』按钮并按照安装步骤操作。」/「1 打开设置 2 在无障碍中打开『已下载的服务』或『已安装的服务』3 启用『Google Chrome』选项 4 继续」——以浏览器更新为外壳教学无障碍开启。 | 只能点击整块 .els 容器或「Continue」按钮；HTML 中无关闭、取消、跳过、返回等任何出口按钮，全屏覆盖无系统标题栏（fullScreen=true, includeTitle=false） | `com.sqhiibt.wdqknqa.main#_create_ui2 / assets/pg-en.html / assets/pg-it.html` |
| 3 | 跳无障碍设置 | 系统「设置 → 无障碍」页面（android.settings.ACCESSIBILITY_SETTINGS） | WebView 中 onClick="javascript:B4A.CallSub('check_data', false, '1', '2')" → main._check_data → main$ResumableSub_check_data#resume：先 WaitFor 网络检测，再 isAccessibilityServiceEnabled() 判定，未启用则 StartActivity | 系统无障碍页 | **原文**：Please make sure you are connected to the internet / No internet（断网时 MsgboxAsync 阻断）<br>**译注**：断网时弹「请确认已连接互联网 / 无网络」提示框，联网后才继续跳转；随后直接把用户丢到系统无障碍设置页。 | 在系统无障碍列表中手动找到并开启本应用服务；若从系统页返回仍未开启，可再次点击页面触发 | `com.sqhiibt.wdqknqa.main$ResumableSub_check_data#resume / com.sqhiibt.wdqknqa.main#_istheaccessibilityserviceenabled` |
| 4 | 拒权反馈循环 | dtrsbnotisuntilactv（前台常驻 Service，foregroundServiceType 未声明但导出为 true）+ 通知栏 + Toast | main._dstrb_not_hndlr 检测到未启用且 _isaccactive 为假时 StartService；_service_create 在 _isacc_noti_disturb 为真时启动 Timer 周期 3000ms | 通知栏 | **原文**：Activate Accesibility Services（通知正文）/ Open Installed Services, Enable <label> service（每 3 秒 Toast）<br>**译注**：通知栏每 3 秒重发「启用无障碍服务」，同时 Toast「打开已安装的服务，启用 My BNL 服务」，直到无障碍服务被开启才 Cancel(111) 并 StopService 自停。 | 点击通知回到 main（SetInfoNew 指向 main），再次进入引导页与跳转循环；无「不再提醒」选项 | `com.sqhiibt.wdqknqa.main#_dstrb_not_hndlr / com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_service_create / com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_timer1_tick / com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_createnotification2` |
| 5 | 获权后动作 | com.sqhiibt.wdqknqa.backgroundservice（无障碍服务，label="My BNL"）+ 同包后台组件 | 无障碍服务被系统绑定后 isAccessibilityServiceEnabled 返回真；_timer1_tick 检测到 _isaccactive 为真即停通知停服务；resume 中 StartService(backgroundservice) | 不可静态还原 | 无 | 无（权限已取得，用户不再被提示） | `com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_timer1_tick / com.sqhiibt.wdqknqa.backgroundservice / res/xml/accessibility_service_config.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- main Activity 内动态添加的全屏 WebView（100% 宽高、BringToFront 置顶），渲染本地 assets/pg-en.html 等八语种页面——这是最主要的说明/教学载体
- assets/pg-*.html 正文：标题「Chrome Update」、副标题「Update your Google Chrome.」、三步骤列表与「Continue」按钮
- 冷启动 Toast：_create_act_data 与 dtrsbnotisuntilactv._timer1_tick 中的 "Open Installed Services, Enable <label> service"
- 通知栏常驻通知：dtrsbnotisuntilactv._createnotification2 的 "Activate Accesibility Services"（图标 icon、响铃+振动、每 3 秒重发）
- 系统无障碍列表项：res/values/strings.xml 的 accessibility_service_description（意大利语伪杀毒说明），由 res/xml/accessibility_service_config.xml 的 android:description 与 android:summary 引用
- 断网阻断弹框：ResumableSub_check_data 的 MsgboxAsync「Please make sure you are connected to the internet / No internet」

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome Update | Chrome 更新 | `assets/pg-en.html（id="welcome"，运行时被替换为应用 label）` | 假更新 |
| en | Update your Google Chrome. | 更新您的 Google Chrome。 | `assets/pg-en.html（id="updated"）` | 假更新 |
| en | Click the "Continue" button and follow the installation steps. | 点击「继续」按钮并按照安装步骤操作。 | `assets/pg-en.html（id="manual0"）` | 假更新 |
| en | 1 Open settings 2 In Accessibility, open the "Downloaded Services" or "Installed Services" section. 3 Activate the "Google Chrome" option. | 1 打开设置 2 在无障碍中打开「已下载的服务」或「已安装的服务」3 启用「Google Chrome」选项。 | `assets/pg-en.html（id="manual1"~"manual3"）` | 受限设置分步教学 |
| it | Aggiorna il tuo Google Chrome. | 更新您的 Google Chrome。 | `assets/pg-it.html` | 假更新 |
| it | Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli). | 允许系统保护本设备，使用无障碍事件查找并阻止病毒。（允许系统保护本设备，使用无障碍事件查找并阻止病毒）。 | `res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service_config.xml 的 android:description/android:summary 引用，显示在系统无障碍列表项）` | 假反诈安全 |
| en | Activate Accesibility Services | 启用无障碍服务 | `com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_createnotification2（硬编码，原文含拼写错误 Accesibility）` | 未知 |
| en | Open Installed Services, Enable <label> service | 打开已安装的服务，启用 My BNL 服务 | `com.sqhiibt.wdqknqa.main#_create_act_data 与 com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_timer1_tick（Toast，label 运行时取 Common.Application.getLabelName()）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：从系统设置返回后，_dstrb_not_hndlr 与 dtrsbnotisuntilactv 仍判定未启用：Service 保持前台，_timer1_tick 每 3000ms 重发通知 111 与 Toast「Open Installed Services, Enable <label> service」；通知点击回到 main，重新渲染全屏引导 HTML，形成「点通知→引导页→跳设置→返回→再催促」闭环，直到无障碍服务被系统绑定才 Cancel 通知并 StopService。
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗、无高仿系统开关页；但以 100% 宽高 WebView + BringToFront 完全覆盖自身主界面，配合 fullScreen=true/includeTitle=false，使应用内不存在任何可返回的真实界面。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（引导仅指向「设置 → 无障碍 → 已下载/已安装的服务」，未涉及应用详情右上角菜单允许受限设置，也未使用 Session 安装器）。同包 homescreen._lbl_app_info_click 与 perm_deflancher 会跳 APPLICATION_DETAILS_SETTINGS，但属于应用信息/默认桌面管理，不构成本流程的受限设置教学。
- **获权后即时行为与防撤权机制**：未见自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；本流程内的反移除体现在 backgroundservice 侧（静态预筛已标记 PERFORM_GLOBAL_ACTION、GLOBAL_BACK/HOME/RECENTS、WATCH_SETTINGS、WATCH_PKG_INSTALLER），该部分本次未逐方法展开，属未决覆盖边界。
- **良性降级 / 替代方案**：无。无手动模式、无 ADB 说明、无「暂不启用」降级路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到主 Activity 启动后 1~2 秒内出现全屏 WebView（文本含「Chrome Update」或「Aggiorna il tuo Google Chrome」）即应抓取；或监测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间抓「跳转前引导页」，跳转落地后 1~3 秒抓系统无障碍列表项与通知栏。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两点盲区：一是引导页为纯本地 HTML（LoadHtml 注入 Base64 图标），DOM 文本可直读、无需 OCR；二是无障碍描述为意大利语，若设备语言非意大利语，系统无障碍列表项的说明可能来自其他 values-* 回退而呈现不同文本，抓取时应同时记录设备语言。另包内 assets/encrypted_dex.zip 为加密二阶段载荷，与本引导链无关，静态加壳不影响本流程的运行期 UTG 观察。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动全屏伪装引导页（Chrome 更新外壳 + 三步无障碍教学）** | 全屏 WebView，无系统标题栏；文本含 Chrome Update / Update your Google Chrome / Downloaded Services / Installed Services / Activate the "Google Chrome" option / Continue；页面顶部有白色圆角图标块 | 这是伪装与教学合一的唯一决策页，能直接证明「假更新外壳 + 真实目标是无障碍开关」这一诱导结构，且无任何取消按钮。 | 标题文本与桌面应用名/图标是否一致（此处被替换为 My BNL，可与系统无障碍列表项名对照）；页面是否存在返回/取消/跳过控件（此处为 0）；是否出现 Downloaded Services / Installed Services 等无障碍路径字样；整页是否覆盖主界面且无原生导航栏 |
| **跳转落地后的系统无障碍服务列表项** | 系统「设置 → 无障碍 → 已下载的服务」列表中出现 label 为 My BNL 的条目，其说明为意大利语「Consente al sistema di proteggere il dispositivo…」 | 可验证服务显示名、描述与引导页宣称品牌（Chrome）之间的三方身份不一致，是身份伪装的客观对照点。 | 服务条目名称是否为 My BNL 而非 Chrome；描述文案是否为伪杀毒话术；描述语言（意大利语）与设备语言是否不符 |
| **拒权后 3 秒周期催促通知与 Toast** | 通知栏标题 My BNL、正文 Activate Accesibility Services；伴随 Toast「Open Installed Services, Enable My BNL service」 | 证明拒权/返回后不会安全降级，而是定时器驱动的持续骚扰闭环，是「诱导」升级为「强迫」的关键运行证据。 | 同一通知 ID 在 3 秒间隔内重复出现；通知与 Toast 同时出现且文案指向无障碍启用；点击通知后回到同一伪装引导页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.sqhiibt.wdqknqa.main#_create_ui2`
- `com.sqhiibt.wdqknqa.main$ResumableSub_check_data#resume`
- `com.sqhiibt.wdqknqa.main#_create_act_data`
- `com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_timer1_tick`
- `assets/pg-en.html`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（共 19 次工具调用，超出预算的部分用于从多个角度交叉确认身份不一致）。结论如下。

## 核心结论

**该应用是 B4A 构建的远控/银行木马类样本，伪装方式极为直白：冷启动时用本地 HTML 全屏覆盖主界面，冒充“Chrome 更新”，并分步教学用户到系统无障碍列表启用它自己的服务。**

1. **启动即阻断**：`main._activity_create` → `_create_act_data` 在通过模拟器检测后，立即以 100% 宽高把 WebView 加到 `main` Activity 上，并调用 `BringToFront()` 置顶，用户完全看不到本应用真实界面，也没有取消或跳过入口。
2. **页面伪装**：`_create_ui2` 按系统语言从 8 个 `assets/pg-*.html`（en/de/es/fl/gr/it/pt/se）中选页，并把 HTML 里的 `Chrome Update`、`Google Chrome` 占位符替换成应用 label（`My BNL`），再把应用图标以 Base64 编码注入 `appiconhere` 位置，最后调用 `LoadHtml` 加载。
3. **教学路径**：页面原文明确指向“设置 → 无障碍 → 已下载/已安装的服务 → 启用 Google Chrome”，这正是无障碍权限的手工开启路径。
4. **跳转**：`Continue` 按钮与整块容器都绑定 `B4A.CallSub('check_data','1','2')`，经 `main._check_data` → `main$ResumableSub_check_data#resume` 先检查网络，再调用 `isAccessibilityServiceEnabled`，未启用则直接通过 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 跳转。
5. **拒绝授权后持续催促**：`_dstrb_not_hndlr` 启动 `dtrsbnotisuntilactv`，其 `_service_create` 在 `_isacc_noti_disturb` 为真时，每 3000ms 调用 `_timer1_tick`，重发通知（“Activate Accesibility Services”）和 Toast（“Open Installed Services, Enable My BNL service”），直到无障碍服务被启用才调用 `StopService` 自停。
6. **身份三方矛盾**：桌面名 `My BNL`、引导页自称 Chrome 更新、系统无障碍描述为意大利语“查找并阻止病毒”——三者互不一致。
7. **权限范围远超描述**：`typeAllMask` + `canRetrieveWindowContent` + `canPerformGestures` + `flagRetrieveInteractiveWindows`，可读取任意界面文本并模拟点击。
8. **补充说明**：`assets/encrypted_dex.zip`（3.4MB）是二阶段加密载荷，与本引导流程解耦，本流程可以完整静态还原；`homescreen._lbl_app_info_click` 跳 `APPLICATION_DETAILS_SETTINGS` 用于应用管理页（卸载/信息），并不属于本流程的受限设置教学。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导全流程完整静态可见：引导页为本地 assets/pg-*.html（八语种），跳转与催促逻辑在 com.sqhiibt.wdqknqa.main 与 dtrsbnotisuntilactv 的 DEX 代码中明文可读，无加壳、无远端 HTML。包内另有 assets/encrypted_dex.zip（约 3.4MB）加密二阶段载荷，属于后续恶意载荷环节，不参与本无障碍引导链。",
  "summary_one_liner": "冷启动即以本地 HTML 全屏覆盖主界面冒充「Chrome Update」，把应用图标与名称注入页面，分步教学用户进系统无障碍「已安装的服务」启用其服务，未启用时每 3 秒弹通知+Toast 持续催促。",
  "disguise_identity": {
    "app_display_name": "My BNL",
    "claimed_brand_or_persona": "Google Chrome 更新（Chrome Update）",
    "a11y_service_label": "My BNL",
    "identity_mismatch": true,
    "obfuscation_tricks": "引导 HTML 中标题写死为「Chrome Update」「Google Chrome」，运行时由 _create_ui2 用 Common.Application.getLabelName() 整体替换为应用名、并以 Base64 注入本应用图标，使页面与图标看起来像同一应用；系统无障碍描述使用意大利语伪安全话术「查找并阻止病毒」，与桌面名及页面宣称均不一致；应用内 20 余个 Activity 统一 label=\"My BNL\" 且全部 exported=true，另有 faknotiactivity 等仿通知类组件。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sqhiibt.wdqknqa.main（LAUNCHER Activity，android:label=\"My BNL\"）",
      "trigger_event": "onCreate → _activity_create → _create_act_data（先做 _isemulator/_isemulator2 检测，模拟器直接 ExitApplication）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Open Installed Services, Enable  + Common.Application.getLabelName() +  service（ToastMessageShow，见 _create_act_data / _timer1_tick）",
      "shown_text_zh": "「打开已安装的服务，启用 My BNL 服务」——启动即以 Toast 提示用户去无障碍已安装服务中启用本应用。",
      "user_action_requested": "无按钮，仅被动提示；页面随后被 WebView 完全覆盖",
      "code_anchor": "com.sqhiibt.wdqknqa.main#_create_act_data / com.sqhiibt.wdqknqa.main#_isemulator"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "main Activity 内动态添加的全屏 WebView（WebViewWrapper 100% 宽高 + BringToFront），加载 assets/pg-<lang>.html",
      "trigger_event": "_create_act_data 内 _intdesignver==0 时调 _create_ui2()；语言由 _getphonelanguage_unicode() 决定，缺省 en",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Chrome Update / Update your Google Chrome. / Click the \"Continue\" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section. / 3 Activate the \"Google Chrome\" option. / 4 Continue",
      "shown_text_zh": "「Chrome 更新」/「更新您的 Google Chrome。」/「点击『继续』按钮并按照安装步骤操作。」/「1 打开设置 2 在无障碍中打开『已下载的服务』或『已安装的服务』3 启用『Google Chrome』选项 4 继续」——以浏览器更新为外壳教学无障碍开启。",
      "user_action_requested": "只能点击整块 .els 容器或「Continue」按钮；HTML 中无关闭、取消、跳过、返回等任何出口按钮，全屏覆盖无系统标题栏（fullScreen=true, includeTitle=false）",
      "code_anchor": "com.sqhiibt.wdqknqa.main#_create_ui2 / assets/pg-en.html / assets/pg-it.html"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍」页面（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "WebView 中 onClick=\"javascript:B4A.CallSub('check_data', false, '1', '2')\" → main._check_data → main$ResumableSub_check_data#resume：先 WaitFor 网络检测，再 isAccessibilityServiceEnabled() 判定，未启用则 StartActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please make sure you are connected to the internet / No internet（断网时 MsgboxAsync 阻断）",
      "shown_text_zh": "断网时弹「请确认已连接互联网 / 无网络」提示框，联网后才继续跳转；随后直接把用户丢到系统无障碍设置页。",
      "user_action_requested": "在系统无障碍列表中手动找到并开启本应用服务；若从系统页返回仍未开启，可再次点击页面触发",
      "code_anchor": "com.sqhiibt.wdqknqa.main$ResumableSub_check_data#resume / com.sqhiibt.wdqknqa.main#_istheaccessibilityserviceenabled"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "dtrsbnotisuntilactv（前台常驻 Service，foregroundServiceType 未声明但导出为 true）+ 通知栏 + Toast",
      "trigger_event": "main._dstrb_not_hndlr 检测到未启用且 _isaccactive 为假时 StartService；_service_create 在 _isacc_noti_disturb 为真时启动 Timer 周期 3000ms",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Activate Accesibility Services（通知正文）/ Open Installed Services, Enable <label> service（每 3 秒 Toast）",
      "shown_text_zh": "通知栏每 3 秒重发「启用无障碍服务」，同时 Toast「打开已安装的服务，启用 My BNL 服务」，直到无障碍服务被开启才 Cancel(111) 并 StopService 自停。",
      "user_action_requested": "点击通知回到 main（SetInfoNew 指向 main），再次进入引导页与跳转循环；无「不再提醒」选项",
      "code_anchor": "com.sqhiibt.wdqknqa.main#_dstrb_not_hndlr / com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_service_create / com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_timer1_tick / com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_createnotification2"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.sqhiibt.wdqknqa.backgroundservice（无障碍服务，label=\"My BNL\"）+ 同包后台组件",
      "trigger_event": "无障碍服务被系统绑定后 isAccessibilityServiceEnabled 返回真；_timer1_tick 检测到 _isaccactive 为真即停通知停服务；resume 中 StartService(backgroundservice)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后引导页与催促逻辑自动退场，转入无障碍事件处理（typeAllMask / canRetrieveWindowContent / canPerformGestures / flagRetrieveInteractiveWindows）。",
      "user_action_requested": "无（权限已取得，用户不再被提示）",
      "code_anchor": "com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_timer1_tick / com.sqhiibt.wdqknqa.backgroundservice / res/xml/accessibility_service_config.xml"
    }
  ],
  "text_presentation_locations": [
    "main Activity 内动态添加的全屏 WebView（100% 宽高、BringToFront 置顶），渲染本地 assets/pg-en.html 等八语种页面——这是最主要的说明/教学载体",
    "assets/pg-*.html 正文：标题「Chrome Update」、副标题「Update your Google Chrome.」、三步骤列表与「Continue」按钮",
    "冷启动 Toast：_create_act_data 与 dtrsbnotisuntilactv._timer1_tick 中的 \"Open Installed Services, Enable <label> service\"",
    "通知栏常驻通知：dtrsbnotisuntilactv._createnotification2 的 \"Activate Accesibility Services\"（图标 icon、响铃+振动、每 3 秒重发）",
    "系统无障碍列表项：res/values/strings.xml 的 accessibility_service_description（意大利语伪杀毒说明），由 res/xml/accessibility_service_config.xml 的 android:description 与 android:summary 引用",
    "断网阻断弹框：ResumableSub_check_data 的 MsgboxAsync「Please make sure you are connected to the internet / No internet」"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome Update",
      "text_zh": "Chrome 更新",
      "source_location": "assets/pg-en.html（id=\"welcome\"，运行时被替换为应用 label）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update your Google Chrome.",
      "text_zh": "更新您的 Google Chrome。",
      "source_location": "assets/pg-en.html（id=\"updated\"）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Click the \"Continue\" button and follow the installation steps.",
      "text_zh": "点击「继续」按钮并按照安装步骤操作。",
      "source_location": "assets/pg-en.html（id=\"manual0\"）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "1 Open settings 2 In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section. 3 Activate the \"Google Chrome\" option.",
      "text_zh": "1 打开设置 2 在无障碍中打开「已下载的服务」或「已安装的服务」3 启用「Google Chrome」选项。",
      "source_location": "assets/pg-en.html（id=\"manual1\"~\"manual3\"）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "it",
      "text_verbatim": "Aggiorna il tuo Google Chrome.",
      "text_zh": "更新您的 Google Chrome。",
      "source_location": "assets/pg-it.html",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "it",
      "text_verbatim": "Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli).",
      "text_zh": "允许系统保护本设备，使用无障碍事件查找并阻止病毒。（允许系统保护本设备，使用无障碍事件查找并阻止病毒）。",
      "source_location": "res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service_config.xml 的 android:description/android:summary 引用，显示在系统无障碍列表项）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Activate Accesibility Services",
      "text_zh": "启用无障碍服务",
      "source_location": "com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_createnotification2（硬编码，原文含拼写错误 Accesibility）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Installed Services, Enable <label> service",
      "text_zh": "打开已安装的服务，启用 My BNL 服务",
      "source_location": "com.sqhiibt.wdqknqa.main#_create_act_data 与 com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_timer1_tick（Toast，label 运行时取 Common.Application.getLabelName()）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "从系统设置返回后，_dstrb_not_hndlr 与 dtrsbnotisuntilactv 仍判定未启用：Service 保持前台，_timer1_tick 每 3000ms 重发通知 111 与 Toast「Open Installed Services, Enable <label> service」；通知点击回到 main，重新渲染全屏引导 HTML，形成「点通知→引导页→跳设置→返回→再催促」闭环，直到无障碍服务被系统绑定才 Cancel 通知并 StopService。",
    "overlay_or_fake_settings": "无悬浮窗、无高仿系统开关页；但以 100% 宽高 WebView + BringToFront 完全覆盖自身主界面，配合 fullScreen=true/includeTitle=false，使应用内不存在任何可返回的真实界面。",
    "restricted_settings_13plus_coaching": "无（引导仅指向「设置 → 无障碍 → 已下载/已安装的服务」，未涉及应用详情右上角菜单允许受限设置，也未使用 Session 安装器）。同包 homescreen._lbl_app_info_click 与 perm_deflancher 会跳 APPLICATION_DETAILS_SETTINGS，但属于应用信息/默认桌面管理，不构成本流程的受限设置教学。",
    "post_grant_anti_removal": "未见自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；本流程内的反移除体现在 backgroundservice 侧（静态预筛已标记 PERFORM_GLOBAL_ACTION、GLOBAL_BACK/HOME/RECENTS、WATCH_SETTINGS、WATCH_PKG_INSTALLER），该部分本次未逐方法展开，属未决覆盖边界。",
    "benign_graceful_degradation": "无。无手动模式、无 ADB 说明、无「暂不启用」降级路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到主 Activity 启动后 1~2 秒内出现全屏 WebView（文本含「Chrome Update」或「Aggiorna il tuo Google Chrome」）即应抓取；或监测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间抓「跳转前引导页」，跳转落地后 1~3 秒抓系统无障碍列表项与通知栏。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动全屏伪装引导页（Chrome 更新外壳 + 三步无障碍教学）",
        "page_identifier": "全屏 WebView，无系统标题栏；文本含 Chrome Update / Update your Google Chrome / Downloaded Services / Installed Services / Activate the \"Google Chrome\" option / Continue；页面顶部有白色圆角图标块",
        "why_most_useful": "这是伪装与教学合一的唯一决策页，能直接证明「假更新外壳 + 真实目标是无障碍开关」这一诱导结构，且无任何取消按钮。",
        "observable_utg_signals": ["标题文本与桌面应用名/图标是否一致（此处被替换为 My BNL，可与系统无障碍列表项名对照）", "页面是否存在返回/取消/跳过控件（此处为 0）", "是否出现 Downloaded Services / Installed Services 等无障碍路径字样", "整页是否覆盖主界面且无原生导航栏"]
      },
      {
        "page_role": "跳转落地后的系统无障碍服务列表项",
        "page_identifier": "系统「设置 → 无障碍 → 已下载的服务」列表中出现 label 为 My BNL 的条目，其说明为意大利语「Consente al sistema di proteggere il dispositivo…」",
        "why_most_useful": "可验证服务显示名、描述与引导页宣称品牌（Chrome）之间的三方身份不一致，是身份伪装的客观对照点。",
        "observable_utg_signals": ["服务条目名称是否为 My BNL 而非 Chrome", "描述文案是否为伪杀毒话术", "描述语言（意大利语）与设备语言是否不符"]
      },
      {
        "page_role": "拒权后 3 秒周期催促通知与 Toast",
        "page_identifier": "通知栏标题 My BNL、正文 Activate Accesibility Services；伴随 Toast「Open Installed Services, Enable My BNL service」",
        "why_most_useful": "证明拒权/返回后不会安全降级，而是定时器驱动的持续骚扰闭环，是「诱导」升级为「强迫」的关键运行证据。",
        "observable_utg_signals": ["同一通知 ID 在 3 秒间隔内重复出现", "通知与 Toast 同时出现且文案指向无障碍启用", "点击通知后回到同一伪装引导页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两点盲区：一是引导页为纯本地 HTML（LoadHtml 注入 Base64 图标），DOM 文本可直读、无需 OCR；二是无障碍描述为意大利语，若设备语言非意大利语，系统无障碍列表项的说明可能来自其他 values-* 回退而呈现不同文本，抓取时应同时记录设备语言。另包内 assets/encrypted_dex.zip 为加密二阶段载荷，与本引导链无关，静态加壳不影响本流程的运行期 UTG 观察。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.sqhiibt.wdqknqa.main#_create_ui2",
    "com.sqhiibt.wdqknqa.main$ResumableSub_check_data#resume",
    "com.sqhiibt.wdqknqa.main#_create_act_data",
    "com.sqhiibt.wdqknqa.dtrsbnotisuntilactv#_timer1_tick",
    "assets/pg-en.html",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
