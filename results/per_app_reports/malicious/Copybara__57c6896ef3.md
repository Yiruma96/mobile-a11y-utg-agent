# MB_139__57c6896ef3｜Copybara — Widiba Token

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：152.3s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即用本地多语HTML伪造“Chrome更新”页并把品牌名运行期替换为自身标签，单按钮分三步教用户进无障碍列表开启伪装的“Google Chrome”服务，未开启则靠后台服务延迟重跳加“Important/Activate Permission”通知持续回拉。
- **静态可见性说明**：无障碍诱导全链（本地HTML文案、品牌名运行期替换、ACCESSIBILITY_SETTINGS跳转、通知催开、服务配置）均完整静态可见，无远端HTML/加密下发。仅获权后的二阶段载荷 assets/encrypted_dex.zip 与 inj_dnlader*/inj_dnlader2* 属另一条动态加载链，未纳入本次引导链结论。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `57c6896ef32e6e1989b69abc7c8cf179173b8b3a061f363b3b7a6421e87778eb` |
| 包名 / 年份 | `com.frmsena.mwhsgxz` / 2025 |
| 家族 / 品类 | **Copybara**（同池样本数：7） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Widiba Token |
| 引导页宣称品牌/身份 | Google Chrome（页面标题“Chrome Update”，要求开启“Google Chrome”无障碍服务）；桌面图标/名称同时伪装为意大利 Widiba 银行令牌应用 |
| 系统无障碍列表服务名 | Widiba Token（Manifest 中 service android:label 与 application label 相同，故系统无障碍列表显示 Widiba Token，而非页面宣称的 Google Chrome） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：HTML 内字面量 'Chrome Update'/'Google Chrome' 在 _create_ui2 中被 Application.getLabelName() 运行期替换，并注入应用图标，使页面品牌随包名标签漂移；按系统语言切换 pg-en/it/de/es/fl/gr/pt/se 八套模板；模拟器环境直接退出规避沙箱；无障碍服务描述伪称防病毒，实际申请 typeAllMask+读窗口内容+模拟手势；accessibility_service_config 未设置 isAccessibilityTool 以规避 Android 13+ 的“受限设置”判定说明，同时也不提供任何真实无障碍辅助说明。 |
| 无障碍服务类名 | `.backgroundservice` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli). / Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli). |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.frmsena.mwhsgxz.main（LAUNCHER Activity，Manifest 中 android:name=".main"） | onCreate → _activity_create → _create_act_data；先 _isemulator()/_isemulator2() 检测，命中则 Toast "App can't work on Emulators" 并 ExitApplication | 原生Activity（随后切换为本地HTML WebView） | **原文**：App can't work on Emulators<br>**译注**：应用无法在模拟器上运行（仅模拟器环境出现） | 无（真实设备上直接进入下一步；模拟器直接退出） | `com.frmsena.mwhsgxz.main#_create_act_data` |
| 2 | 引导说明页 | main Activity 内嵌全屏 WebView（WebViewWrapper + WebViewExtras + B4A JS 接口），加载 assets/pg-*.html | _create_act_data 调 _create_ui2()：按语言选页 → File.ReadString(dirAssets, 页面) → replace("Chrome Update"→label)、replace("Google Chrome"→label)、replace("appiconhere"→base64图标) → webViewWrapper.LoadHtml() | 本地HTML WebView | **原文**：Chrome Update / Update your Google Chrome. / Click the "Continue" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the "Downloaded Services" or "Installed Services" section. / 3 Activate the "Google Chrome" option. / Continue<br>**译注**：（运行期替换后）Widiba Token 更新页：更新你的 Widiba Token；点击“继续”并按照安装步骤操作；①打开设置 ②在无障碍中打开“已下载的服务”或“已安装的服务”分区 ③启用“Widiba Token”选项；按钮：继续 | 只能点击“Continue/Continua”；页面无取消、跳过、稍后再说或返回按钮 | `com.frmsena.mwhsgxz.main#_create_ui2 + assets/pg-en.html` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | HTML 按钮 onClick="javascript:B4A.CallSub('check_data', false, '1', '2')" → main._check_data → main$ResumableSub_check_data.resume：isAccessibilityServiceEnabled 为 false 时 IntentWrapper.Initialize("android.settings.ACCESSIBILITY_SETTINGS","") + StartActivity | 系统无障碍页 | **原文**：无（由系统渲染无障碍服务列表）<br>**译注**：系统“无障碍/已安装的服务”列表，其中条目名为 Widiba Token | 要求用户在系统列表中手动打开 Widiba Token 服务开关（无引导遮罩，无教用户进“应用详情右上角菜单允许受限设置”的步骤） | `com.frmsena.mwhsgxz.main$ResumableSub_check_data#resume` |
| 4 | 获权后动作 | com.frmsena.mwhsgxz.backgroundservice（BIND_ACCESSIBILITY_SERVICE，foregroundServiceType=mediaPlayback） | resume 分支无条件 Common.StartService(backgroundservice)；_service_create → _checkifserviceisenabled → intIsAccessibilityServiceEnabled_WithCrashCheck 返回 0 时置 globalparameters._isaccactive=true | 不可静态还原（服务内后续行为依赖远端指令，二阶段载荷为 assets/encrypted_dex.zip 与 inj_dnlader/inj_dnlader2） | 无 | 无 | `com.frmsena.mwhsgxz.backgroundservice#_checkifserviceisenabled` |
| 5 | 拒权反馈循环 | 通知栏通知 + 再次拉起系统无障碍设置页 + 导出 Activity forc_activateacc | _checkifserviceisenabled 判定未启用 → _isaccactive=false → Common.CallSubDelayed2(main,"IsTheAccessibilityServiceEnabled",false)（→ main._istheaccessibilityserviceenabled 再次 StartActivity(ACCESSIBILITY_SETTINGS)）+ _createnotification_alert("Important","Activate Permission")；仅当距 _lnglastpermnotification 超过 5 秒才再次弹出（setSound/setVibrate true，Notify(1)，PendingIntent → forc_activateacc） | 通知栏 + 系统无障碍页 | **原文**：Important / Activate Permission<br>**译注**：重要 / 激活权限（点击后进入伪装令牌页 forc_activateacc，用户可再次被引向无障碍设置） | 点击通知回到应用/设置继续开启；无停止催促的界面开关 | `com.frmsena.mwhsgxz.backgroundservice#_checkifserviceisenabled + #_createnotification_alert` |
| 6 | 引导说明页 | Toast 提示（首次建 UI 且未获权时） | _create_act_data 中 if (!_isactive_acc()) 时 Common.ToastMessageShow | 原生Dialog（Toast） | **原文**：Open Installed Services, Enable Widiba Token service<br>**译注**：打开“已安装的服务”，启用 Widiba Token 服务 | 无交互按钮，仅提示 | `com.frmsena.mwhsgxz.main#_create_act_data` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- main Activity 冷启动内嵌全屏 WebView：assets/pg-en.html（或 pg-it/de/es/fl/gr/pt/se），通过 File.ReadString + LoadHtml 渲染，文案品牌名被运行期替换为应用 label
- WebView 内 <p id="welcome">Chrome Update、<p id="updated">、<p id="manual0">、<p id="manual1..3"> 三步教学、<button id="continue">Continue
- Toast："Open Installed Services, Enable <应用名> service"（main._create_act_data，未获权时）
- 通知栏：标题 "Important"、正文 "Activate Permission"（backgroundservice._createnotification_alert，5 秒节流）
- 系统无障碍列表条目描述：@string/accessibility_service_description（res/xml/accessibility_service_config.xml，意大利语“帮系统保护设备、用无障碍事件查找并阻止病毒”）
- 系统无障碍列表条目名称：Manifest service android:label="Widiba Token"（与页面宣称的 Google Chrome 不一致）
- 无：无原生 AlertDialog 引导页、无高仿系统无障碍开关页、无半透明引导遮罩（悬浮窗 WebView 仅用于 samsung_overlay_pans_* 的锁屏/远端页面场景）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome Update | Chrome 更新 | `assets/pg-en.html#L? <p id="welcome">（运行期被替换为 Widiba Token）` | 假更新 |
| en | Update your Google Chrome. | 更新你的 Google Chrome。 | `assets/pg-en.html <p id="updated">` | 假更新 |
| en | Click the "Continue" button and follow the installation steps. | 点击“继续”按钮并按照安装步骤操作。 | `assets/pg-en.html <p id="manual0">` | 受限设置分步教学 |
| en | Open settings | 打开设置 | `assets/pg-en.html <p id="manual1">` | 受限设置分步教学 |
| en | In Accessibility, open the "Downloaded Services" or "Installed Services" section. | 在无障碍中，打开“已下载的服务”或“已安装的服务”分区。 | `assets/pg-en.html <p id="manual2">` | 受限设置分步教学 |
| en | Activate the "Google Chrome" option. | 启用“Google Chrome”选项。 | `assets/pg-en.html <p id="manual3">（运行期替换为 Widiba Token）` | 教唆忽视警告 |
| it | Aggiorna il tuo Google Chrome. / Fare clic sul pulsante "Continua" e seguire i passaggi di installazione. / Apri le impostazioni / In Accessibilità, apri la sezione "Servizi scaricati" o "Servizi installati". / Attiva l'opzione "Google Chrome". | 更新你的 Google Chrome。／点击“继续”按钮并按照安装步骤操作。／打开设置／在无障碍中打开“已下载的服务”或“已安装的服务”分区。／启用“Google Chrome”选项。 | `assets/pg-it.html <p id="updated/manual0/manual1/manual2/manual3">` | 假更新 |
| it | Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. | 允许系统保护设备，使用无障碍事件查找并阻止病毒。 | `res/xml/accessibility_service_config.xml → @string/accessibility_service_description（android:description 与 android:summary 同值）` | 假反诈安全 |
| en | Important / Activate Permission | 重要 / 激活权限 | `com.frmsena.mwhsgxz.backgroundservice#_createnotification_alert 硬编码参数` | 故障恐吓 |
| en | Open Installed Services, Enable Widiba Token service | 打开“已安装的服务”，启用 Widiba Token 服务 | `com.frmsena.mwhsgxz.main#_create_act_data 硬编码 Toast（拼接 Application.getLabelName()）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：未获权时由 backgroundservice._checkifserviceisenabled 触发 CallSubDelayed2(main,"IsTheAccessibilityServiceEnabled")，使 main._istheaccessibilityserviceenabled 再次 StartActivity(android.settings.ACCESSIBILITY_SETTINGS)；同时 _createnotification_alert 每 >5 秒（_lnglastpermnotification 节流）弹一次 "Important/Activate Permission" 响铃震动通知，点击进入导出的 forc_activateacc 再次引向设置页，构成延迟重跳 + 通知回拉的反馈循环；应用无退出/放弃入口（main 仅由 _ismainact_shouldclose 控制 Finish）。
- **遮罩叠层 / 高仿系统设置页**：引导链本身不叠遮罩、不伪造系统开关页；但应用具备 SYSTEM_ALERT_WINDOW 与 b4a.flm.overlaywdw 悬浮窗能力，backgroundservice 的 samsung_overlay_pans_co_local/_url 会用 WindowManager.addView 全屏半透明 WebView 覆盖（TYPE 2002/2032/2038），可用于盖住设置页，属同族能力而非本轮引导链直接使用。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。HTML 仅教用户进“无障碍 → 已下载/已安装的服务”开启服务，未教进应用详情右上角菜单允许受限设置，也无 Session 安装器绕过；服务配置未声明 android:isAccessibilityTool，targetSdk 33。
- **获权后即时行为与防撤权机制**：线索级：DEX 预筛显示存在 WATCH_SETTINGS/GLOBAL_BACK/GLOBAL_HOME/PERFORM_GLOBAL_ACTION，backgroundservice 具备 GestureDescription 手势注入与全局动作能力，但本轮未在无障碍引导链上取得“监听设置页并阻止撤权”的直接代码路径，未作确认。
- **良性降级 / 替代方案**：无。未获权不降级为只读/手动模式，而是持续重跳与通知催促；模拟器环境反而直接 ExitApplication。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动即拉起：监测 main Activity onCreate 后 1–2 秒内出现全屏 WebView 且文本含 "Chrome Update"/"Update your Google Chrome"/"Open settings"；次优钩子为监测 Intent action == android.settings.ACCESSIBILITY_SETTINGS 的 StartActivity（来自 main._istheaccessibilityserviceenabled 与 ResumableSub_check_data.resume）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案均为文本（HTML/Toast/通知），无需 OCR；盲区在于：1) 获权后的真实恶意行为依赖远端指令与 assets/encrypted_dex.zip 二阶段加密载荷，UTG 在获权瞬间无法看到后续动作；2) 悬浮窗全屏半透明 WebView 覆盖场景（samsung_overlay_pans_*）可能被 UTG 判为普通页面，需结合窗口类型判断；3) 应用含模拟器检测，纯模拟器环境会直接退出而抓不到引导页，须使用真机或可绕过检测的环境。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动假更新引导页（最关键）** | com.frmsena.mwhsgxz.main 内全屏 WebView，标题区文本 "Chrome Update"/应用名 + "Update your Google Chrome." + 三步编号列表 + 唯一 "Continue" 按钮 | 这一页同时暴露假更新诱饵、分步教学与无退出按钮三重特征，且页面宣称品牌（Google Chrome）与无障碍列表条目名（Widiba Token）不一致，是判定诱导与身份冒用最直接的一帧。 | WebView 内可提取文本含 "Chrome Update"/"Continue"/"Installed Services" 等教学关键词；页面宣称品牌与当前应用 label 文本差异（如出现 Google Chrome 字样）；界面上仅存在一个可点击按钮、无返回/取消/跳过控件；无系统状态栏业务界面、无银行令牌类输入控件 |
| **系统无障碍服务列表项** | Settings 无障碍 → 已安装的服务 列表项 "Widiba Token"，描述为意大利语“防病毒”说明 | 核对服务条目名/描述与引导页宣称品牌是否一致，并确认用户被要求开启的正是该服务。 | 列表项名称 = Widiba Token；描述文本为 Consente al sistema di proteggere il dispositivo…（防病毒伪装）；列表项旁无 isAccessibilityTool 友好标识（系统可能显示隐私警告） |
| **拒权后通知催开** | 通知栏标题 "Important"、正文 "Activate Permission"，点击进入 com.frmsena.mwhsgxz.forc_activateacc | 证明存在拒绝反馈循环而非一次性说明，是区分良性引导与强迫授权的关键运行期证据。 | 同一通知在 >5 秒间隔内重复出现；返回应用后再次自动跳转 ACCESSIBILITY_SETTINGS；通知点击后落到非引导页的伪装令牌 Activity |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.frmsena.mwhsgxz.main#_create_ui2`
- `com.frmsena.mwhsgxz.main#_create_act_data`
- `com.frmsena.mwhsgxz.main$ResumableSub_check_data#resume`
- `com.frmsena.mwhsgxz.main#_istheaccessibilityserviceenabled`
- `com.frmsena.mwhsgxz.backgroundservice#_checkifserviceisenabled`
- `assets/pg-en.html`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验）

**总体：该应用全程围绕“无障碍授权”展开，且是伪造系统/品牌更新场景的强诱导链，非良性说明。**

1. **冷启动即伪装**：`main` 在 `onCreate → _create_act_data` 里先做模拟器检测（命中即 `ExitApplication`），随后不走任何令牌业务界面，而是调 `_create_ui2()` 建全屏 WebView。
2. **运行期改写品牌（关键诡计）**：`_create_ui2()` 按系统语言挑 `assets/pg-{en,it,de,es,fl,gr,pt,se}.html`，把 HTML 里的字面量 `"Chrome Update"`、`"Google Chrome"` 全部 `replace` 成 `Application.getLabelName()`（= `Widiba Token`），并注入应用图标。所以用户看到的是“更新 Google Chrome / 开启 Google Chrome”，而系统无障碍列表里实际条目名是 `Widiba Token`——身份完全错位。
3. **三步教学 + 单按钮无退出**：HTML 正文为 `Open settings` → `In Accessibility, open the "Downloaded Services" or "Installed Services" section.` → `Activate the "Google Chrome" option.`，只有一个 `Continue` 按钮（`onClick` 触发 `B4A.CallSub('check_data')`），没有取消/跳过/稍后。
4. **直达受限设置**：`check_data → ResumableSub_check_data.resume` 中 `isAccessibilityServiceEnabled` 为 false 即 `StartActivity("android.settings.ACCESSIBILITY_SETTINGS")`，紧接着无条件 `StartService(backgroundservice)`。
5. **拒绝后反馈循环**：`backgroundservice._checkifserviceisenabled` 在服务创建时判定未启用 → 置 `_isaccactive=false`、`CallSubDelayed2(main,"IsTheAccessibilityServiceEnabled")`（`main._istheaccessibilityserviceenabled` 再跳一次无障碍设置）+ `_createnotification_alert("Important","Activate Permission")` 发高优先级（响铃/震动）通知，点击指向导出的 `forc_activateacc`，并以 `_lnglastpermnotification` 做 >5s 节流持续回拉。
6. **服务描述与能力严重不符**：`accessibility_service_config.xml` 描述为“帮系统防病毒”，实际申请 `typeAllMask`、`canRetrieveWindowContent`、`flagRetrieveInteractiveWindows`、`canPerformGestures`，具备读窗口内容与模拟手势能力。

**可见性**：引导链（HTML 文案、跳转、通知、服务配置）全部静态清晰可见，无远端下发教学页。仅获权后的二阶段载荷（`assets/encrypted_dex.zip`、`inj_dnlader*`）属另一条链，本轮未展开。

**覆盖边界**：`WATCH_SETTINGS`/`GLOBAL_BACK`/`GLOBAL_HOME` 撤权阻断线索在 DEX 中确实存在（`backgroundservice` 具备手势与全局动作能力），但本轮未在“无障碍引导链”上取得“监听设置页阻止返回”的直接代码证据，故 `post_grant_anti_removal` 如实标注为线索级。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导全链（本地HTML文案、品牌名运行期替换、ACCESSIBILITY_SETTINGS跳转、通知催开、服务配置）均完整静态可见，无远端HTML/加密下发。仅获权后的二阶段载荷 assets/encrypted_dex.zip 与 inj_dnlader*/inj_dnlader2* 属另一条动态加载链，未纳入本次引导链结论。",
  "summary_one_liner": "冷启动即用本地多语HTML伪造“Chrome更新”页并把品牌名运行期替换为自身标签，单按钮分三步教用户进无障碍列表开启伪装的“Google Chrome”服务，未开启则靠后台服务延迟重跳加“Important/Activate Permission”通知持续回拉。",
  "disguise_identity": {
    "app_display_name": "Widiba Token",
    "claimed_brand_or_persona": "Google Chrome（页面标题“Chrome Update”，要求开启“Google Chrome”无障碍服务）；桌面图标/名称同时伪装为意大利 Widiba 银行令牌应用",
    "a11y_service_label": "Widiba Token（Manifest 中 service android:label 与 application label 相同，故系统无障碍列表显示 Widiba Token，而非页面宣称的 Google Chrome）",
    "identity_mismatch": true,
    "obfuscation_tricks": "HTML 内字面量 'Chrome Update'/'Google Chrome' 在 _create_ui2 中被 Application.getLabelName() 运行期替换，并注入应用图标，使页面品牌随包名标签漂移；按系统语言切换 pg-en/it/de/es/fl/gr/pt/se 八套模板；模拟器环境直接退出规避沙箱；无障碍服务描述伪称防病毒，实际申请 typeAllMask+读窗口内容+模拟手势；accessibility_service_config 未设置 isAccessibilityTool 以规避 Android 13+ 的“受限设置”判定说明，同时也不提供任何真实无障碍辅助说明。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.frmsena.mwhsgxz.main（LAUNCHER Activity，Manifest 中 android:name=\".main\"）",
      "trigger_event": "onCreate → _activity_create → _create_act_data；先 _isemulator()/_isemulator2() 检测，命中则 Toast \"App can't work on Emulators\" 并 ExitApplication",
      "ui_carrier": "原生Activity（随后切换为本地HTML WebView）",
      "shown_text_verbatim": "App can't work on Emulators",
      "shown_text_zh": "应用无法在模拟器上运行（仅模拟器环境出现）",
      "user_action_requested": "无（真实设备上直接进入下一步；模拟器直接退出）",
      "code_anchor": "com.frmsena.mwhsgxz.main#_create_act_data"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "main Activity 内嵌全屏 WebView（WebViewWrapper + WebViewExtras + B4A JS 接口），加载 assets/pg-*.html",
      "trigger_event": "_create_act_data 调 _create_ui2()：按语言选页 → File.ReadString(dirAssets, 页面) → replace(\"Chrome Update\"→label)、replace(\"Google Chrome\"→label)、replace(\"appiconhere\"→base64图标) → webViewWrapper.LoadHtml()",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Chrome Update / Update your Google Chrome. / Click the \"Continue\" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section. / 3 Activate the \"Google Chrome\" option. / Continue",
      "shown_text_zh": "（运行期替换后）Widiba Token 更新页：更新你的 Widiba Token；点击“继续”并按照安装步骤操作；①打开设置 ②在无障碍中打开“已下载的服务”或“已安装的服务”分区 ③启用“Widiba Token”选项；按钮：继续",
      "user_action_requested": "只能点击“Continue/Continua”；页面无取消、跳过、稍后再说或返回按钮",
      "code_anchor": "com.frmsena.mwhsgxz.main#_create_ui2 + assets/pg-en.html"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "HTML 按钮 onClick=\"javascript:B4A.CallSub('check_data', false, '1', '2')\" → main._check_data → main$ResumableSub_check_data.resume：isAccessibilityServiceEnabled 为 false 时 IntentWrapper.Initialize(\"android.settings.ACCESSIBILITY_SETTINGS\",\"\") + StartActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（由系统渲染无障碍服务列表）",
      "shown_text_zh": "系统“无障碍/已安装的服务”列表，其中条目名为 Widiba Token",
      "user_action_requested": "要求用户在系统列表中手动打开 Widiba Token 服务开关（无引导遮罩，无教用户进“应用详情右上角菜单允许受限设置”的步骤）",
      "code_anchor": "com.frmsena.mwhsgxz.main$ResumableSub_check_data#resume"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.frmsena.mwhsgxz.backgroundservice（BIND_ACCESSIBILITY_SERVICE，foregroundServiceType=mediaPlayback）",
      "trigger_event": "resume 分支无条件 Common.StartService(backgroundservice)；_service_create → _checkifserviceisenabled → intIsAccessibilityServiceEnabled_WithCrashCheck 返回 0 时置 globalparameters._isaccactive=true",
      "ui_carrier": "不可静态还原（服务内后续行为依赖远端指令，二阶段载荷为 assets/encrypted_dex.zip 与 inj_dnlader/inj_dnlader2）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后无任何界面提示，直接进入静默服务运行",
      "user_action_requested": "无",
      "code_anchor": "com.frmsena.mwhsgxz.backgroundservice#_checkifserviceisenabled"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "通知栏通知 + 再次拉起系统无障碍设置页 + 导出 Activity forc_activateacc",
      "trigger_event": "_checkifserviceisenabled 判定未启用 → _isaccactive=false → Common.CallSubDelayed2(main,\"IsTheAccessibilityServiceEnabled\",false)（→ main._istheaccessibilityserviceenabled 再次 StartActivity(ACCESSIBILITY_SETTINGS)）+ _createnotification_alert(\"Important\",\"Activate Permission\")；仅当距 _lnglastpermnotification 超过 5 秒才再次弹出（setSound/setVibrate true，Notify(1)，PendingIntent → forc_activateacc）",
      "ui_carrier": "通知栏 + 系统无障碍页",
      "shown_text_verbatim": "Important / Activate Permission",
      "shown_text_zh": "重要 / 激活权限（点击后进入伪装令牌页 forc_activateacc，用户可再次被引向无障碍设置）",
      "user_action_requested": "点击通知回到应用/设置继续开启；无停止催促的界面开关",
      "code_anchor": "com.frmsena.mwhsgxz.backgroundservice#_checkifserviceisenabled + #_createnotification_alert"
    },
    {
      "step": 6,
      "stage": "引导说明页",
      "screen_or_component": "Toast 提示（首次建 UI 且未获权时）",
      "trigger_event": "_create_act_data 中 if (!_isactive_acc()) 时 Common.ToastMessageShow",
      "ui_carrier": "原生Dialog（Toast）",
      "shown_text_verbatim": "Open Installed Services, Enable Widiba Token service",
      "shown_text_zh": "打开“已安装的服务”，启用 Widiba Token 服务",
      "user_action_requested": "无交互按钮，仅提示",
      "code_anchor": "com.frmsena.mwhsgxz.main#_create_act_data"
    }
  ],
  "text_presentation_locations": [
    "main Activity 冷启动内嵌全屏 WebView：assets/pg-en.html（或 pg-it/de/es/fl/gr/pt/se），通过 File.ReadString + LoadHtml 渲染，文案品牌名被运行期替换为应用 label",
    "WebView 内 <p id=\"welcome\">Chrome Update、<p id=\"updated\">、<p id=\"manual0\">、<p id=\"manual1..3\"> 三步教学、<button id=\"continue\">Continue",
    "Toast：\"Open Installed Services, Enable <应用名> service\"（main._create_act_data，未获权时）",
    "通知栏：标题 \"Important\"、正文 \"Activate Permission\"（backgroundservice._createnotification_alert，5 秒节流）",
    "系统无障碍列表条目描述：@string/accessibility_service_description（res/xml/accessibility_service_config.xml，意大利语“帮系统保护设备、用无障碍事件查找并阻止病毒”）",
    "系统无障碍列表条目名称：Manifest service android:label=\"Widiba Token\"（与页面宣称的 Google Chrome 不一致）",
    "无：无原生 AlertDialog 引导页、无高仿系统无障碍开关页、无半透明引导遮罩（悬浮窗 WebView 仅用于 samsung_overlay_pans_* 的锁屏/远端页面场景）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome Update",
      "text_zh": "Chrome 更新",
      "source_location": "assets/pg-en.html#L? <p id=\"welcome\">（运行期被替换为 Widiba Token）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update your Google Chrome.",
      "text_zh": "更新你的 Google Chrome。",
      "source_location": "assets/pg-en.html <p id=\"updated\">",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Click the \"Continue\" button and follow the installation steps.",
      "text_zh": "点击“继续”按钮并按照安装步骤操作。",
      "source_location": "assets/pg-en.html <p id=\"manual0\">",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Open settings",
      "text_zh": "打开设置",
      "source_location": "assets/pg-en.html <p id=\"manual1\">",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section.",
      "text_zh": "在无障碍中，打开“已下载的服务”或“已安装的服务”分区。",
      "source_location": "assets/pg-en.html <p id=\"manual2\">",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Activate the \"Google Chrome\" option.",
      "text_zh": "启用“Google Chrome”选项。",
      "source_location": "assets/pg-en.html <p id=\"manual3\">（运行期替换为 Widiba Token）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "it",
      "text_verbatim": "Aggiorna il tuo Google Chrome. / Fare clic sul pulsante \"Continua\" e seguire i passaggi di installazione. / Apri le impostazioni / In Accessibilità, apri la sezione \"Servizi scaricati\" o \"Servizi installati\". / Attiva l'opzione \"Google Chrome\".",
      "text_zh": "更新你的 Google Chrome。／点击“继续”按钮并按照安装步骤操作。／打开设置／在无障碍中打开“已下载的服务”或“已安装的服务”分区。／启用“Google Chrome”选项。",
      "source_location": "assets/pg-it.html <p id=\"updated/manual0/manual1/manual2/manual3\">",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "it",
      "text_verbatim": "Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli.",
      "text_zh": "允许系统保护设备，使用无障碍事件查找并阻止病毒。",
      "source_location": "res/xml/accessibility_service_config.xml → @string/accessibility_service_description（android:description 与 android:summary 同值）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Important / Activate Permission",
      "text_zh": "重要 / 激活权限",
      "source_location": "com.frmsena.mwhsgxz.backgroundservice#_createnotification_alert 硬编码参数",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Installed Services, Enable Widiba Token service",
      "text_zh": "打开“已安装的服务”，启用 Widiba Token 服务",
      "source_location": "com.frmsena.mwhsgxz.main#_create_act_data 硬编码 Toast（拼接 Application.getLabelName()）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "未获权时由 backgroundservice._checkifserviceisenabled 触发 CallSubDelayed2(main,\"IsTheAccessibilityServiceEnabled\")，使 main._istheaccessibilityserviceenabled 再次 StartActivity(android.settings.ACCESSIBILITY_SETTINGS)；同时 _createnotification_alert 每 >5 秒（_lnglastpermnotification 节流）弹一次 \"Important/Activate Permission\" 响铃震动通知，点击进入导出的 forc_activateacc 再次引向设置页，构成延迟重跳 + 通知回拉的反馈循环；应用无退出/放弃入口（main 仅由 _ismainact_shouldclose 控制 Finish）。",
    "overlay_or_fake_settings": "引导链本身不叠遮罩、不伪造系统开关页；但应用具备 SYSTEM_ALERT_WINDOW 与 b4a.flm.overlaywdw 悬浮窗能力，backgroundservice 的 samsung_overlay_pans_co_local/_url 会用 WindowManager.addView 全屏半透明 WebView 覆盖（TYPE 2002/2032/2038），可用于盖住设置页，属同族能力而非本轮引导链直接使用。",
    "restricted_settings_13plus_coaching": "无。HTML 仅教用户进“无障碍 → 已下载/已安装的服务”开启服务，未教进应用详情右上角菜单允许受限设置，也无 Session 安装器绕过；服务配置未声明 android:isAccessibilityTool，targetSdk 33。",
    "post_grant_anti_removal": "线索级：DEX 预筛显示存在 WATCH_SETTINGS/GLOBAL_BACK/GLOBAL_HOME/PERFORM_GLOBAL_ACTION，backgroundservice 具备 GestureDescription 手势注入与全局动作能力，但本轮未在无障碍引导链上取得“监听设置页并阻止撤权”的直接代码路径，未作确认。",
    "benign_graceful_degradation": "无。未获权不降级为只读/手动模式，而是持续重跳与通知催促；模拟器环境反而直接 ExitApplication。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动即拉起：监测 main Activity onCreate 后 1–2 秒内出现全屏 WebView 且文本含 \"Chrome Update\"/\"Update your Google Chrome\"/\"Open settings\"；次优钩子为监测 Intent action == android.settings.ACCESSIBILITY_SETTINGS 的 StartActivity（来自 main._istheaccessibilityserviceenabled 与 ResumableSub_check_data.resume）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动假更新引导页（最关键）",
        "page_identifier": "com.frmsena.mwhsgxz.main 内全屏 WebView，标题区文本 \"Chrome Update\"/应用名 + \"Update your Google Chrome.\" + 三步编号列表 + 唯一 \"Continue\" 按钮",
        "why_most_useful": "这一页同时暴露假更新诱饵、分步教学与无退出按钮三重特征，且页面宣称品牌（Google Chrome）与无障碍列表条目名（Widiba Token）不一致，是判定诱导与身份冒用最直接的一帧。",
        "observable_utg_signals": [
          "WebView 内可提取文本含 \"Chrome Update\"/\"Continue\"/\"Installed Services\" 等教学关键词",
          "页面宣称品牌与当前应用 label 文本差异（如出现 Google Chrome 字样）",
          "界面上仅存在一个可点击按钮、无返回/取消/跳过控件",
          "无系统状态栏业务界面、无银行令牌类输入控件"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍 → 已安装的服务 列表项 \"Widiba Token\"，描述为意大利语“防病毒”说明",
        "why_most_useful": "核对服务条目名/描述与引导页宣称品牌是否一致，并确认用户被要求开启的正是该服务。",
        "observable_utg_signals": [
          "列表项名称 = Widiba Token",
          "描述文本为 Consente al sistema di proteggere il dispositivo…（防病毒伪装）",
          "列表项旁无 isAccessibilityTool 友好标识（系统可能显示隐私警告）"
        ]
      },
      {
        "page_role": "拒权后通知催开",
        "page_identifier": "通知栏标题 \"Important\"、正文 \"Activate Permission\"，点击进入 com.frmsena.mwhsgxz.forc_activateacc",
        "why_most_useful": "证明存在拒绝反馈循环而非一次性说明，是区分良性引导与强迫授权的关键运行期证据。",
        "observable_utg_signals": [
          "同一通知在 >5 秒间隔内重复出现",
          "返回应用后再次自动跳转 ACCESSIBILITY_SETTINGS",
          "通知点击后落到非引导页的伪装令牌 Activity"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案均为文本（HTML/Toast/通知），无需 OCR；盲区在于：1) 获权后的真实恶意行为依赖远端指令与 assets/encrypted_dex.zip 二阶段加密载荷，UTG 在获权瞬间无法看到后续动作；2) 悬浮窗全屏半透明 WebView 覆盖场景（samsung_overlay_pans_*）可能被 UTG 判为普通页面，需结合窗口类型判断；3) 应用含模拟器检测，纯模拟器环境会直接退出而抓不到引导页，须使用真机或可绕过检测的环境。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.frmsena.mwhsgxz.main#_create_ui2",
    "com.frmsena.mwhsgxz.main#_create_act_data",
    "com.frmsena.mwhsgxz.main$ResumableSub_check_data#resume",
    "com.frmsena.mwhsgxz.main#_istheaccessibilityserviceenabled",
    "com.frmsena.mwhsgxz.backgroundservice#_checkifserviceisenabled",
    "assets/pg-en.html"
  ]
}
```

</details>
