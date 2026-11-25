# MB_136__bdae3cc96a｜Copybara — BBVA Codigo

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：134.6s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即用本地多语言 HTML 冒充“Chrome 更新”，把品牌字样替换为自身 BBVA Codigo 标识，三步图文教用户到无障碍列表打开同名开关，点击即跳 ACCESSIBILITY_SETTINGS，未授权则 5 秒节流反复弹振动通知并循环重跳。
- **静态可见性说明**：引导链完全静态可见：本地 assets/pg-*.html 为明文 HTML，B4A 事件回调（check_data、ResumableSub_check_data.resume）、ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 跳转点、通知催办节流逻辑均在 DEX 明文可读。唯一未展开的是 assets/encrypted_dex.zip（约3.4MB加密二次载荷），属运行期注入能力，不影响本次 UTG 引导链判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `bdae3cc96acd16347a7ca568b9972d82ecdef8d637abee96302d20d4d02cd613` |
| 包名 / 年份 | `com.ebhgqwi.qzgbqzm` / 2025 |
| 家族 / 品类 | **Copybara**（同池样本数：7） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | BBVA Codigo |
| 引导页宣称品牌/身份 | Google Chrome（页面标题 “Chrome Update / Update your Google Chrome”），同时冒充 BBVA 银行品牌名，无障碍说明自称系统病毒防护 |
| 系统无障碍列表服务名 | BBVA Codigo（服务 android:label 与 android:description 分别为 BBVA Codigo 与西语“允许系统保护您的设备，用无障碍事件查杀病毒”） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：HTML 内以 'Chrome Update'/'Google Chrome' 占位符，运行时被 replace 为应用自身 label，并注入自身图标 base64 到 appiconhere；无障碍说明文案与真实能力（typeAllMask 全量读屏 + canPerformGestures 手势 + flagRetrieveInteractiveWindows）完全不符；DEX 内残留另一包名 com.appnuevacodigoappapk.app；服务名 .backgroundservice 无语义；无伪造 isAccessibilityTool、无空白/换行挤出警告、无同形字、无多 activity-alias 堆叠 |
| 无障碍服务类名 | `.backgroundservice` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Permite que el sistema proteja su dispositivo. Utiliza los eventos de accesibilidad para buscar virus y detenerlos. (Permite al sistema asegurar su dispositivo, Utiliza los eventos de accesibilidad para buscar virus y detenerlos). / Permite que el sistema proteja su dispositivo. Utiliza los eventos de accesibilidad para buscar virus y detenerlos. (Permite al sistema asegurar su dispositivo, Utiliza los eventos de accesibilidad para buscar virus y detenerlos). |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.ebhgqwi.qzgbqzm.main（LAUNCHER Activity，excludeFromRecents=true） | 用户点击桌面图标 → onCreate → activity_create → _create_act_data | 原生Activity | 无 | 无（自动执行） | `com.ebhgqwi.qzgbqzm.main._create_act_data` |
| 2 | 引导说明页 | main 内嵌全屏 WebView（_create_ui2 动态 AddView，宽高 100%） | _create_act_data 中 _intdesignver==0 分支调用 _create_ui2()；同时 _isactive_acc() 为 false 时先弹 Toast "Open Installed Services, Enable BBVA Codigo service" | 本地HTML WebView | **原文**：Chrome Update / Update your Google Chrome. / Click the "Continue" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the "Downloaded Services" or "Installed Services" section. / 3 Activate the "Google Chrome" option. / Continuar(Continue)<br>**译注**：「Chrome 更新」「请更新你的 Google Chrome。」「点击“继续”按钮并按照安装步骤操作。」「1 打开设置」「2 在无障碍中打开“已下载的服务”或“已安装的服务”」「3 激活“Google Chrome”选项」以及底部“继续”按钮 | 点击页面内任意 els 区域或“Continue”按钮；页面无取消/关闭/跳过按钮，WebView 全屏铺满覆盖 Activity 内容 | `com.ebhgqwi.qzgbqzm.main._create_ui2 / assets/pg-en.html#L266-L307 / assets/design.txt` |
| 3 | 跳受限设置 | android.settings.ACCESSIBILITY_SETTINGS（系统无障碍设置页） | HTML onClick 触发 B4A.CallSub('check_data','1','2') → main._check_data → ResumableSub_check_data.resume：先 Sleep(0) 与联网检查（无网则 MsgBox "Please make sure you are connected to the internet" / "No internet"），再反射 isAccessibilityServiceEnabled，为 false 则 StartActivity(ACCESSIBILITY_SETTINGS) | 系统无障碍页 | **原文**：Please make sure you are connected to the internet（仅断网时弹出）<br>**译注**：系统无障碍设置列表，其中服务项显示为 “BBVA Codigo”，说明文字为“允许系统保护您的设备……” | 在系统页找到 BBVA Codigo 并手动打开开关；应用不提供任何替代路径 | `com.ebhgqwi.qzgbqzm.main$ResumableSub_check_data#resume（case 10）/ com.ebhgqwi.qzgbqzm.main._istheaccessibilityserviceenabled` |
| 4 | 拒权反馈循环 | dtrsbnotisuntilactv 服务 + backgroundservice 通知（PendingIntent → forc_activateacc Activity） | _create_act_data 末尾 _dstrb_not_hndlr()：无障碍未启用且 globalparameters._isaccactive 为 false → StartService(dtrsbnotisuntilactv)；backgroundservice._checkifserviceisenabled → _createnotification_alert 以 _lnglastpermnotification 做 >5 秒节流反复 Notify(1)，setSound(true)+setVibrate(true) | 通知栏 | **原文**：（通知标题/正文由调用方传入的 str、str2 决定，未在包内固定；图标固定为 "icon"）<br>**译注**：振动+响铃通知反复提醒，点击后打开 forc_activateacc 全屏页（fullScreen=true、无标题栏、getWindow().setFlags(1024,1024) 全屏）再次走判定与跳转 | 点击通知回到强制引导页；无“不再提醒”选项 | `com.ebhgqwi.qzgbqzm.main._dstrb_not_hndlr / com.ebhgqwi.qzgbqzm.backgroundservice._createnotification_alert / com.ebhgqwi.qzgbqzm.forc_activateacc#onCreate` |
| 5 | 获权后动作 | backgroundservice（无障碍服务，foregroundServiceType=mediaPlayback） | resume 中 isAccActive 为 true 后继续执行：Common.StartService(backgroundservice)；SDK≥34 且无后台定位权限时追加 StartActivity(LOCATION_SOURCE_SETTINGS)；globalparameters.ispreinjallfls 为真时 StartService(inj_dnlader) | 不可静态还原（后续动作由 encrypted_dex.zip 二阶段载荷承载，本次未展开） | 无 | 无 | `com.ebhgqwi.qzgbqzm.main$ResumableSub_check_data#resume（case 21/24）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- main Activity 内动态添加的全屏 WebView（_create_ui2 中 AddView 覆盖 100%×100%，LoadHtml 加载 assets/pg-*.html 并 BringToFront）——主引导文案全部在此
- assets/pg-en.html、pg-es.html、pg-de.html、pg-it.html、pg-pt.html、pg-fl.html、pg-gr.html、pg-se.html 第 266-307 行（Chrome Update / Update your Google Chrome. / 三步 manual1-3）
- assets/design.txt：九语种版本的“启用无障碍服务”四行文案模板（含 <app> 占位）
- 系统无障碍服务列表项：res/xml/accessibility_service_config.xml 的 android:label="BBVA Codigo" 与 android:description/@string/accessibility_service_description（西语“允许系统保护您的设备…查杀病毒”）
- Toast（非弹窗）：_create_act_data 中 "Open Installed Services, Enable BBVA Codigo service"；模拟器检测命中时 "App can't work on Emulators"
- 断网 MsgBox：ResumableSub_check_data case 6 的 "Please make sure you are connected to the internet" / 标题 "No internet"
- 通知栏：backgroundservice._createnotification_alert 生成的振动响铃通知，点击进入 forc_activateacc 全屏强制引导页
- 未发现悬浮窗遮罩引导（SYSTEM_ALERT_WINDOW 权限存在但引导链未使用 Overlay 教学层）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome Update | Chrome 更新 | `assets/pg-en.html#L267（运行时被 replace 为应用 label 'BBVA Codigo'）` | 假更新 |
| en | Update your Google Chrome. | 请更新你的 Google Chrome。 | `assets/pg-en.html#L270` | 假更新 |
| en | Click the "Continue" button and follow the installation steps. | 点击“继续”按钮并按照安装步骤操作。 | `assets/pg-en.html#L273` | 假更新 |
| en | 1 Open settings / 2 In Accessibility, open the "Downloaded Services" or "Installed Services" section. / 3 Activate the "Google Chrome" option. | 1 打开设置 / 2 在无障碍中打开“已下载的服务”或“已安装的服务” / 3 激活“Google Chrome”选项 | `assets/pg-en.html#L289-L306` | 受限设置分步教学 |
| es | Actualiza tu Google Chrome. / Haga clic en el botón "Continuar" y siga los pasos de instalación. / En Accesibilidad, abra la sección "Servicios descargados" o "Servicios instalados". / Activa la opción "Google Chrome". | 请更新你的 Google Chrome。/ 点击“继续”按钮并按照安装步骤操作。/ 在无障碍中打开“已下载的服务”或“已安装的服务”/ 激活“Google Chrome”选项。 | `assets/pg-es.html（对应 manual0-manual3 段落）` | 受限设置分步教学 |
| es | Permite que el sistema proteja su dispositivo. Utiliza los eventos de accesibilidad para buscar virus y detenerlos. | 允许系统保护您的设备。使用无障碍事件搜索病毒并阻止它们。 | `res/xml/accessibility_service_config.xml → @string/accessibility_service_description（系统无障碍列表说明）` | 假反诈安全 |
| en | Open Installed Services, Enable BBVA Codigo service | 打开已安装的服务，启用 BBVA Codigo 服务 | `com.ebhgqwi.qzgbqzm.main._create_act_data（Toast 硬编码）` | 受限设置分步教学 |
| en | Please make sure you are connected to the internet | 请确认您已连接互联网 | `com.ebhgqwi.qzgbqzm.main$ResumableSub_check_data#resume（case 6，标题 No internet）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：未授权时 _dstrb_not_hndlr 启动 dtrsbnotisuntilactv；backgroundservice._createnotification_alert 以 _lnglastpermnotification 做 >5 秒节流反复发振动+响铃通知，PendingIntent 指向 forc_activateacc 全屏页；用户从系统无障碍页返回或点击通知后再次经 check_data 判定并重新 StartActivity(ACCESSIBILITY_SETTINGS)，形成无终止的催办循环。此外每次 resume 都会无条件 StartService(backgroundservice)，SDK≥34 无后台定位权限时还会追加跳 LOCATION_SOURCE_SETTINGS
- **遮罩叠层 / 高仿系统设置页**：无半透明引导遮罩，也未伪造高仿系统无障碍开关页；但引导页为全屏 WebView（100%×100% AddView + BringToFront）覆盖整个 Activity，视觉上完全替代应用界面，并注入应用自身图标伪装成更新器
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现引导用户进入应用详情页右上角菜单开启“允许受限设置”的文案或跳转（代码中的 APPLICATION_DETAILS_SETTINGS 跳转位于 homescreen._lbl_app_info_click、perm_deflancher.showClearDefaultsDialog 与 backgroundservice.openapp_sett，均非引导链教学用途）
- **获权后即时行为与防撤权机制**：引导链中未见获权后自点确认或自授权。反撤权能力（GLOBAL_ACTION_BACK/HOME/RECENTS、PERFORM_GLOBAL_ACTION、WATCH_SETTINGS）位于 backgroundservice 运行期逻辑，属获权后动作而非引导步骤
- **良性降级 / 替代方案**：无。未启用无障碍即无任何降级路径，只有通知催办与重复跳转

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：应用进程启动后首个 Activity 上屏瞬间即应拉起 UTG（无需等待任何交互）；同时挂 StartActivity 的 Intent 监听，命中 android.settings.ACCESSIBILITY_SETTINGS 时二次抓取系统页与随后返回的强制页
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案全部为可提取文本（HTML 内 <p> 元素与 strings 资源），无需 OCR。显著盲区：①通知标题/正文由调用方动态传入，静态不可固定，需运行期抓取通知内容；②获权后由 assets/encrypted_dex.zip 承载的二阶段载荷（注入下载 inj_dnlader 等）为加密资产，静态不可还原，运行期 UTG 若在获权后立即采集，可能只能看到无障碍服务常驻而无可见界面；③应用含模拟器检测（_isemulator/_isemulator2，命中即 Toast 后退出），在模拟器上 UTG 可能无法进入引导页，需真机或对检测做 Hook 绕过。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页（冒充 Chrome 更新）** | com.ebhgqwi.qzgbqzm.main，全屏 WebView，顶部大字“Chrome Update”或已被替换为“BBVA Codigo”，下方三步编号教程与“Continue/Continuar”按钮 | 这是全部诱导文案的唯一载体，直接给出“假更新 + 分步教开启无障碍”的完整证据，且无取消按钮可佐证不可跳过 | 界面文本“Chrome Update / Update your Google Chrome / Activate the "Google Chrome" option”；页面图标与桌面图标一致但文案宣称 Chrome，形成品牌错配；不存在返回/关闭/跳过控件 |
| **跳转前一刻的联网检查与 Toast 页** | 同一 Activity 上叠加的 Toast“Open Installed Services, Enable BBVA Codigo service”，或断网时 MsgBox“No internet” | 把页面文案与真实目标服务名（BBVA Codigo）直接关联，证明页面宣称的 Chrome 与实际要开启的服务不是同一对象 | Toast 中出现的应用自身 label 与服务名；MsgBox 标题 No internet / 正文 Please make sure you are connected to the internet |
| **系统无障碍服务列表项** | Settings → Accessibility → Installed/Downloaded services，条目名“BBVA Codigo”，副标题为西语“Permite que el sistema proteja su dispositivo…buscar virus y detenerlos.” | 捕获系统侧服务名与说明，可与页面宣称的 Chrome 更新做身份比对，并记录该服务申请了全量事件类型与手势能力 | 列表项 label 与 android:description 原文；开关初始为关闭状态；同一列表中不存在任何 Chrome 相关服务 |
| **拒权后返回的强制催办页与通知** | forc_activateacc 全屏页（无标题栏、无返回按钮）+ 通知栏中 5 秒节流重复出现的振动响铃通知 | 证明拒绝授权后不降级而是循环催办，是“不可取消 / 拒权循环”的关键运行期证据 | 从系统设置返回后短时间内再次出现同一引导页；通知栏在数秒内重复刷新同一通知；页面无任何退出路径，需按 Home 或最近任务才能离开 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.ebhgqwi.qzgbqzm.main._create_act_data`
- `com.ebhgqwi.qzgbqzm.main._create_ui2`
- `com.ebhgqwi.qzgbqzm.main$ResumableSub_check_data#resume`
- `com.ebhgqwi.qzgbqzm.backgroundservice._createnotification_alert`
- `assets/pg-en.html#L266-L307`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**静态可见性**：引导链完整静态可见。本地 HTML、B4A 事件回调、跳转 Intent 与催办通知均为明文实现，无需解密即可还原；二次载荷 `assets/encrypted_dex.zip`（3.4MB）未纳入本次 UTG 视角命题。

**核心机制（冷启动 0 步触发）**
1. `main._activity_create` → `_create_act_data`：先做模拟器检测，再调用 `_create_ui2` 建 WebView 全屏铺满（100%×100%）。
2. `_create_ui2` 按系统语言从 assets 选 `pg-{de,en,es,fl,gr,it,pt,se}.html`；把 HTML 里 `Chrome Update` / `Google Chrome` 两处占位替换为应用自身 label（`BBVA Codigo`），并把自身图标 base64 注入 `appiconhere`，使页面呈现为“本应用正在更新 Chrome”。
3. HTML 正文即三步教程：`Open settings` → 在无障碍里打开“已下载/已安装服务” → 打开 “Google Chrome” 开关；整块区域 `onClick="javascript:B4A.CallSub('check_data',false,'1','2')"`。
4. `main._check_data` → `ResumableSub_check_data.resume`：先查联网，再用反射 `isAccessibilityServiceEnabled` 判定；未启用则 `android.settings.ACCESSIBILITY_SETTINGS` 直跳系统无障碍页。`_istheaccessibilityserviceenabled` 内还有同样一处跳转。
5. 拒权循环：`_dstrb_not_hndlr` 在未启用时启动 `dtrsbnotisuntilactv`；`backgroundservice._createnotification_alert` 以 5 秒节流反复发振动+响铃通知，PendingIntent 指向 `forc_activateacc`，点击后再次走判定→跳设置。
6. 获权后 `resume` 继续 `StartService(backgroundservice)`，SDK≥34 还会追加 `LOCATION_SOURCE_SETTINGS` 跳转，并在 `ispreinjallfls` 为真时启动 `inj_dnlader` 注入下载服务。

**身份错配**：桌面名与服务 label 均为 `BBVA Codigo`（西班牙外换银行），页面宣称 Chrome 更新，无障碍说明写成“允许系统保护设备、用无障碍事件查杀病毒”——三者互不一致，且该服务实际申请 `typeAllMask` + `flagRetrieveInteractiveWindows` + `canRetrieveWindowContent` + `canPerformGestures`（全量读屏+手势），与“查毒”说明严重不符。B4A 包名常量还残留 `com.appnuevacodigoappapk.app`。

**未见项**：无 Android 13+ 受限设置分步教学，无获权后自点确认/`GLOBAL_ACTION_BACK` 阻断撤权（反撤权逻辑在 `backgroundservice` 运行期，未在引导链上）；引导页无取消/跳过按钮。

已登记风险 **R-001**（high，deceptive_behavior）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链完全静态可见：本地 assets/pg-*.html 为明文 HTML，B4A 事件回调（check_data、ResumableSub_check_data.resume）、ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 跳转点、通知催办节流逻辑均在 DEX 明文可读。唯一未展开的是 assets/encrypted_dex.zip（约3.4MB加密二次载荷），属运行期注入能力，不影响本次 UTG 引导链判定。",
  "summary_one_liner": "冷启动即用本地多语言 HTML 冒充“Chrome 更新”，把品牌字样替换为自身 BBVA Codigo 标识，三步图文教用户到无障碍列表打开同名开关，点击即跳 ACCESSIBILITY_SETTINGS，未授权则 5 秒节流反复弹振动通知并循环重跳。",
  "disguise_identity": {
    "app_display_name": "BBVA Codigo",
    "claimed_brand_or_persona": "Google Chrome（页面标题 “Chrome Update / Update your Google Chrome”），同时冒充 BBVA 银行品牌名，无障碍说明自称系统病毒防护",
    "a11y_service_label": "BBVA Codigo（服务 android:label 与 android:description 分别为 BBVA Codigo 与西语“允许系统保护您的设备，用无障碍事件查杀病毒”）",
    "identity_mismatch": true,
    "obfuscation_tricks": "HTML 内以 'Chrome Update'/'Google Chrome' 占位符，运行时被 replace 为应用自身 label，并注入自身图标 base64 到 appiconhere；无障碍说明文案与真实能力（typeAllMask 全量读屏 + canPerformGestures 手势 + flagRetrieveInteractiveWindows）完全不符；DEX 内残留另一包名 com.appnuevacodigoappapk.app；服务名 .backgroundservice 无语义；无伪造 isAccessibilityTool、无空白/换行挤出警告、无同形字、无多 activity-alias 堆叠"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.ebhgqwi.qzgbqzm.main（LAUNCHER Activity，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标 → onCreate → activity_create → _create_act_data",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无文字，仅执行环境判定（_isemulator/_isemulator2，命中则 Toast \"App can't work on Emulators\" 并退出）",
      "user_action_requested": "无（自动执行）",
      "code_anchor": "com.ebhgqwi.qzgbqzm.main._create_act_data"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "main 内嵌全屏 WebView（_create_ui2 动态 AddView，宽高 100%）",
      "trigger_event": "_create_act_data 中 _intdesignver==0 分支调用 _create_ui2()；同时 _isactive_acc() 为 false 时先弹 Toast \"Open Installed Services, Enable BBVA Codigo service\"",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Chrome Update / Update your Google Chrome. / Click the \"Continue\" button and follow the installation steps. / 1 Open settings / 2 In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section. / 3 Activate the \"Google Chrome\" option. / Continuar(Continue)",
      "shown_text_zh": "「Chrome 更新」「请更新你的 Google Chrome。」「点击“继续”按钮并按照安装步骤操作。」「1 打开设置」「2 在无障碍中打开“已下载的服务”或“已安装的服务”」「3 激活“Google Chrome”选项」以及底部“继续”按钮",
      "user_action_requested": "点击页面内任意 els 区域或“Continue”按钮；页面无取消/关闭/跳过按钮，WebView 全屏铺满覆盖 Activity 内容",
      "code_anchor": "com.ebhgqwi.qzgbqzm.main._create_ui2 / assets/pg-en.html#L266-L307 / assets/design.txt"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS（系统无障碍设置页）",
      "trigger_event": "HTML onClick 触发 B4A.CallSub('check_data','1','2') → main._check_data → ResumableSub_check_data.resume：先 Sleep(0) 与联网检查（无网则 MsgBox \"Please make sure you are connected to the internet\" / \"No internet\"），再反射 isAccessibilityServiceEnabled，为 false 则 StartActivity(ACCESSIBILITY_SETTINGS)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please make sure you are connected to the internet（仅断网时弹出）",
      "shown_text_zh": "系统无障碍设置列表，其中服务项显示为 “BBVA Codigo”，说明文字为“允许系统保护您的设备……”",
      "user_action_requested": "在系统页找到 BBVA Codigo 并手动打开开关；应用不提供任何替代路径",
      "code_anchor": "com.ebhgqwi.qzgbqzm.main$ResumableSub_check_data#resume（case 10）/ com.ebhgqwi.qzgbqzm.main._istheaccessibilityserviceenabled"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "dtrsbnotisuntilactv 服务 + backgroundservice 通知（PendingIntent → forc_activateacc Activity）",
      "trigger_event": "_create_act_data 末尾 _dstrb_not_hndlr()：无障碍未启用且 globalparameters._isaccactive 为 false → StartService(dtrsbnotisuntilactv)；backgroundservice._checkifserviceisenabled → _createnotification_alert 以 _lnglastpermnotification 做 >5 秒节流反复 Notify(1)，setSound(true)+setVibrate(true)",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "（通知标题/正文由调用方传入的 str、str2 决定，未在包内固定；图标固定为 \"icon\"）",
      "shown_text_zh": "振动+响铃通知反复提醒，点击后打开 forc_activateacc 全屏页（fullScreen=true、无标题栏、getWindow().setFlags(1024,1024) 全屏）再次走判定与跳转",
      "user_action_requested": "点击通知回到强制引导页；无“不再提醒”选项",
      "code_anchor": "com.ebhgqwi.qzgbqzm.main._dstrb_not_hndlr / com.ebhgqwi.qzgbqzm.backgroundservice._createnotification_alert / com.ebhgqwi.qzgbqzm.forc_activateacc#onCreate"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "backgroundservice（无障碍服务，foregroundServiceType=mediaPlayback）",
      "trigger_event": "resume 中 isAccActive 为 true 后继续执行：Common.StartService(backgroundservice)；SDK≥34 且无后台定位权限时追加 StartActivity(LOCATION_SOURCE_SETTINGS)；globalparameters.ispreinjallfls 为真时 StartService(inj_dnlader)",
      "ui_carrier": "不可静态还原（后续动作由 encrypted_dex.zip 二阶段载荷承载，本次未展开）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，转入后台服务运行",
      "user_action_requested": "无",
      "code_anchor": "com.ebhgqwi.qzgbqzm.main$ResumableSub_check_data#resume（case 21/24）"
    }
  ],
  "text_presentation_locations": [
    "main Activity 内动态添加的全屏 WebView（_create_ui2 中 AddView 覆盖 100%×100%，LoadHtml 加载 assets/pg-*.html 并 BringToFront）——主引导文案全部在此",
    "assets/pg-en.html、pg-es.html、pg-de.html、pg-it.html、pg-pt.html、pg-fl.html、pg-gr.html、pg-se.html 第 266-307 行（Chrome Update / Update your Google Chrome. / 三步 manual1-3）",
    "assets/design.txt：九语种版本的“启用无障碍服务”四行文案模板（含 <app> 占位）",
    "系统无障碍服务列表项：res/xml/accessibility_service_config.xml 的 android:label=\"BBVA Codigo\" 与 android:description/@string/accessibility_service_description（西语“允许系统保护您的设备…查杀病毒”）",
    "Toast（非弹窗）：_create_act_data 中 \"Open Installed Services, Enable BBVA Codigo service\"；模拟器检测命中时 \"App can't work on Emulators\"",
    "断网 MsgBox：ResumableSub_check_data case 6 的 \"Please make sure you are connected to the internet\" / 标题 \"No internet\"",
    "通知栏：backgroundservice._createnotification_alert 生成的振动响铃通知，点击进入 forc_activateacc 全屏强制引导页",
    "未发现悬浮窗遮罩引导（SYSTEM_ALERT_WINDOW 权限存在但引导链未使用 Overlay 教学层）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome Update",
      "text_zh": "Chrome 更新",
      "source_location": "assets/pg-en.html#L267（运行时被 replace 为应用 label 'BBVA Codigo'）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update your Google Chrome.",
      "text_zh": "请更新你的 Google Chrome。",
      "source_location": "assets/pg-en.html#L270",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Click the \"Continue\" button and follow the installation steps.",
      "text_zh": "点击“继续”按钮并按照安装步骤操作。",
      "source_location": "assets/pg-en.html#L273",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "1 Open settings / 2 In Accessibility, open the \"Downloaded Services\" or \"Installed Services\" section. / 3 Activate the \"Google Chrome\" option.",
      "text_zh": "1 打开设置 / 2 在无障碍中打开“已下载的服务”或“已安装的服务” / 3 激活“Google Chrome”选项",
      "source_location": "assets/pg-en.html#L289-L306",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "es",
      "text_verbatim": "Actualiza tu Google Chrome. / Haga clic en el botón \"Continuar\" y siga los pasos de instalación. / En Accesibilidad, abra la sección \"Servicios descargados\" o \"Servicios instalados\". / Activa la opción \"Google Chrome\".",
      "text_zh": "请更新你的 Google Chrome。/ 点击“继续”按钮并按照安装步骤操作。/ 在无障碍中打开“已下载的服务”或“已安装的服务”/ 激活“Google Chrome”选项。",
      "source_location": "assets/pg-es.html（对应 manual0-manual3 段落）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "es",
      "text_verbatim": "Permite que el sistema proteja su dispositivo. Utiliza los eventos de accesibilidad para buscar virus y detenerlos.",
      "text_zh": "允许系统保护您的设备。使用无障碍事件搜索病毒并阻止它们。",
      "source_location": "res/xml/accessibility_service_config.xml → @string/accessibility_service_description（系统无障碍列表说明）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Installed Services, Enable BBVA Codigo service",
      "text_zh": "打开已安装的服务，启用 BBVA Codigo 服务",
      "source_location": "com.ebhgqwi.qzgbqzm.main._create_act_data（Toast 硬编码）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please make sure you are connected to the internet",
      "text_zh": "请确认您已连接互联网",
      "source_location": "com.ebhgqwi.qzgbqzm.main$ResumableSub_check_data#resume（case 6，标题 No internet）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "未授权时 _dstrb_not_hndlr 启动 dtrsbnotisuntilactv；backgroundservice._createnotification_alert 以 _lnglastpermnotification 做 >5 秒节流反复发振动+响铃通知，PendingIntent 指向 forc_activateacc 全屏页；用户从系统无障碍页返回或点击通知后再次经 check_data 判定并重新 StartActivity(ACCESSIBILITY_SETTINGS)，形成无终止的催办循环。此外每次 resume 都会无条件 StartService(backgroundservice)，SDK≥34 无后台定位权限时还会追加跳 LOCATION_SOURCE_SETTINGS",
    "overlay_or_fake_settings": "无半透明引导遮罩，也未伪造高仿系统无障碍开关页；但引导页为全屏 WebView（100%×100% AddView + BringToFront）覆盖整个 Activity，视觉上完全替代应用界面，并注入应用自身图标伪装成更新器",
    "restricted_settings_13plus_coaching": "无。未发现引导用户进入应用详情页右上角菜单开启“允许受限设置”的文案或跳转（代码中的 APPLICATION_DETAILS_SETTINGS 跳转位于 homescreen._lbl_app_info_click、perm_deflancher.showClearDefaultsDialog 与 backgroundservice.openapp_sett，均非引导链教学用途）",
    "post_grant_anti_removal": "引导链中未见获权后自点确认或自授权。反撤权能力（GLOBAL_ACTION_BACK/HOME/RECENTS、PERFORM_GLOBAL_ACTION、WATCH_SETTINGS）位于 backgroundservice 运行期逻辑，属获权后动作而非引导步骤",
    "benign_graceful_degradation": "无。未启用无障碍即无任何降级路径，只有通知催办与重复跳转"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "应用进程启动后首个 Activity 上屏瞬间即应拉起 UTG（无需等待任何交互）；同时挂 StartActivity 的 Intent 监听，命中 android.settings.ACCESSIBILITY_SETTINGS 时二次抓取系统页与随后返回的强制页",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页（冒充 Chrome 更新）",
        "page_identifier": "com.ebhgqwi.qzgbqzm.main，全屏 WebView，顶部大字“Chrome Update”或已被替换为“BBVA Codigo”，下方三步编号教程与“Continue/Continuar”按钮",
        "why_most_useful": "这是全部诱导文案的唯一载体，直接给出“假更新 + 分步教开启无障碍”的完整证据，且无取消按钮可佐证不可跳过",
        "observable_utg_signals": [
          "界面文本“Chrome Update / Update your Google Chrome / Activate the \"Google Chrome\" option”",
          "页面图标与桌面图标一致但文案宣称 Chrome，形成品牌错配",
          "不存在返回/关闭/跳过控件"
        ]
      },
      {
        "page_role": "跳转前一刻的联网检查与 Toast 页",
        "page_identifier": "同一 Activity 上叠加的 Toast“Open Installed Services, Enable BBVA Codigo service”，或断网时 MsgBox“No internet”",
        "why_most_useful": "把页面文案与真实目标服务名（BBVA Codigo）直接关联，证明页面宣称的 Chrome 与实际要开启的服务不是同一对象",
        "observable_utg_signals": [
          "Toast 中出现的应用自身 label 与服务名",
          "MsgBox 标题 No internet / 正文 Please make sure you are connected to the internet"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility → Installed/Downloaded services，条目名“BBVA Codigo”，副标题为西语“Permite que el sistema proteja su dispositivo…buscar virus y detenerlos.”",
        "why_most_useful": "捕获系统侧服务名与说明，可与页面宣称的 Chrome 更新做身份比对，并记录该服务申请了全量事件类型与手势能力",
        "observable_utg_signals": [
          "列表项 label 与 android:description 原文",
          "开关初始为关闭状态",
          "同一列表中不存在任何 Chrome 相关服务"
        ]
      },
      {
        "page_role": "拒权后返回的强制催办页与通知",
        "page_identifier": "forc_activateacc 全屏页（无标题栏、无返回按钮）+ 通知栏中 5 秒节流重复出现的振动响铃通知",
        "why_most_useful": "证明拒绝授权后不降级而是循环催办，是“不可取消 / 拒权循环”的关键运行期证据",
        "observable_utg_signals": [
          "从系统设置返回后短时间内再次出现同一引导页",
          "通知栏在数秒内重复刷新同一通知",
          "页面无任何退出路径，需按 Home 或最近任务才能离开"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案全部为可提取文本（HTML 内 <p> 元素与 strings 资源），无需 OCR。显著盲区：①通知标题/正文由调用方动态传入，静态不可固定，需运行期抓取通知内容；②获权后由 assets/encrypted_dex.zip 承载的二阶段载荷（注入下载 inj_dnlader 等）为加密资产，静态不可还原，运行期 UTG 若在获权后立即采集，可能只能看到无障碍服务常驻而无可见界面；③应用含模拟器检测（_isemulator/_isemulator2，命中即 Toast 后退出），在模拟器上 UTG 可能无法进入引导页，需真机或对检测做 Hook 绕过。"
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
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.ebhgqwi.qzgbqzm.main._create_act_data",
    "com.ebhgqwi.qzgbqzm.main._create_ui2",
    "com.ebhgqwi.qzgbqzm.main$ResumableSub_check_data#resume",
    "com.ebhgqwi.qzgbqzm.backgroundservice._createnotification_alert",
    "assets/pg-en.html#L266-L307",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
