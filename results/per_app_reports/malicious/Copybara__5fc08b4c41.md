# MB_015__5fc08b4c41｜Copybara — Star Patcher

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：148.1s

## 1. 一句话核心结论

- **核心申请方式**：以'Chrome 更新/Shizuku LP 集成'为名的本地HTML教学页起手，点按钮即跳系统无障碍设置，并在后台服务与全屏悬浮WebView遮罩层持续催办开启无障碍，系统列表却用意大利语杀毒防护描述伪装。
- **静态可见性说明**：冷启动HTML教学页、设计分步文案、无障碍设置跳转、通知催办、无障碍描述均在包内静态可见；仅全屏悬浮遮罩页面的实际URL由 broker 远端指令经 _ws_send_lockscreen_overlay_url 下发，其页面内容需运行期捕获。无加壳。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5fc08b4c4197d94016ec27e3cf09d4943891921519b489ade3c9494d71fe4715` |
| 包名 / 年份 | `com.ilmybnlapp.apk` / 2026 |
| 家族 / 品类 | **Copybara**（同池样本数：7） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Star Patcher |
| 引导页宣称品牌/身份 | Google Chrome 更新（pg-it/pg-es/pg-de 等本地化版本）与 Shizuku LP / ADB 内存编辑集成工具（pg-en） |
| 系统无障碍列表服务名 | Star Patcher（.backgroundservice，描述为意大利语'保护设备、查找并拦截病毒'） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：HTML 内 Chrome Update/Google Chrome 占位符在运行时被替换为自身 label；意大利语版伪装 Chrome 更新、英语版伪装 Shizuku 集成，同一诱导页对不同语言用户呈现不同身份；accessibility_service_config 的 settingsActivity 指向不存在的 com.com.android.rr.main；无障碍描述用非本地语言(意大利语)声称杀毒；大量 perm_* / inj_dnlader / faknotiactivity 等近义 activity-service 并存掩护真实入口 |
| 无障碍服务类名 | `.backgroundservice` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：@00000000, @00000000 |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli). / Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. (Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli). |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.ilmybnlapp.apk.main（LAUNCHER Activity，全屏 WebView 覆盖） | onCreate → _create_act_data → _create_ui2 | 本地HTML WebView | **原文**：Aggiorna il tuo Google Chrome. / Fare clic sul pulsante "Continua" e seguire i passaggi di installazione. / Apri le impostazioni<br>**译注**：更新你的 Google Chrome。点击"继续"按钮并按安装步骤操作。打开设置。 | 点击"继续/打开设置"按钮（页面无跳过或关闭入口，仅一个主按钮） | `com.ilmybnlapp.apk.main#_create_ui2 / assets/pg-it.html` |
| 2 | 业务功能触发 | main 内 WebView 的 B4A JS 桥回调 _lblsettings_click | 用户点击页面按钮 → DefaultJavascriptInterface 回调 → _lblsettings_click → _check_data | 本地HTML WebView | **原文**：Enable Accessibility Service to enable Shizuku integration / 1- Open 'Installed Services' 2- Find <app> 3- Set Switch ON / Open Settings<br>**译注**：启用无障碍服务以启用 Shizuku 集成；1-打开'已安装的服务' 2-找到本应用 3-把开关打开；打开设置 | 按三步指引进入已安装服务列表并打开本应用开关 | `com.ilmybnlapp.apk.main#_lblsettings_click / assets/design.txt` |
| 3 | 跳无障碍设置 | Intent(android.settings.ACCESSIBILITY_SETTINGS) → 系统无障碍设置页 | ResumableSub_check_data#resume 中 isAccessibilityServiceEnabled 返回 false | 系统无障碍页 | **原文**：无（应用侧无自定义提示，直接 StartActivity）<br>**译注**：直接跳转系统无障碍设置，界面由系统呈现，列表项显示 Star Patcher 及意大利语杀毒描述 | 在系统页手动找到 Star Patcher 并开启开关（应用不提供取消或跳过） | `com.ilmybnlapp.apk.main$ResumableSub_check_data#resume` |
| 4 | 拒权反馈循环 | 后台通知栏通知（标题 Important / 内容 Activate Permission），点击落地 forc_activateacc | backgroundservice._service_create → _checkifserviceisenabled 未启用 → _createnotification_alert + CallSubDelayed2 重新触发跳转 | 通知栏 | **原文**：Important / Activate Permission<br>**译注**：重要 / 激活权限 | 点击通知返回应用继续授权；通知带声音与震动，5 秒节流反复推送，无取消入口 | `com.ilmybnlapp.apk.backgroundservice#_checkifserviceisenabled / #_createnotification_alert` |
| 5 | 遮罩叠层指引 | WindowManager 全屏 Panel + WebView 悬浮层（TYPE_APPLICATION_OVERLAY / 旧版 2002） | broker 指令 → backgroundservice._ws_send_lockscreen_overlay_url → _samsung_overlay_pans_url | 悬浮窗Overlay | **原文**：无（页面内容由远端 URL 加载，静态不可见）<br>**译注**：覆盖在屏幕上方（y=-250、高度+400）的全屏 WebView 引导页，同时把屏幕亮度强制写为 1 | 在遮罩层内继续按远端页面指引操作（远端可随时更换文案） | `com.ilmybnlapp.apk.backgroundservice#_samsung_overlay_pans_url` |
| 6 | 获权后动作 | backgroundservice（AccessibilityService，typeAllMask / canRetrieveWindowContent）+ inj_dnlader / inj_dnlader2 / managerservice | 服务被系统启用后 _service_create 完成初始化 | 不可静态还原 | **原文**：The normal functions of the service (reading the screen and emulating taps) is not used by this app, but the service must exist for android to let us edit other apps memory and edit any system apps.<br>**译注**：本应用并不使用该服务的正常功能（读取屏幕与模拟点击），但为了让 Android 允许我们编辑其他应用内存和系统应用，该服务必须存在。 | 无（获权后自动启动注入下载与远程管理服务，用户无感知） | `com.ilmybnlapp.apk.backgroundservice#_service_create` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- main Activity 内全屏 WebView 加载 assets/pg-<语言>.html（运行时替换 Chrome Update/Google Chrome 为 Star Patcher 并内嵌自身图标 base64）
- assets/design.txt 与 assets/designxiaomi.txt 的 JSON 多语言分步指引（含 Open Settings 按钮文案），经 _design2_map_strings 注入界面
- 系统无障碍服务列表项：res/values/strings.xml 的 accessibility_service_description（意大利语杀毒防护描述）+ 服务 label Star Patcher
- 通知栏常驻/反复通知：_createnotification_alert("Important","Activate Permission")，点击进入 forc_activateacc
- 屏幕上方悬浮 WebView 遮罩层：_samsung_overlay_pans_url 以 WindowManager.addView 全屏叠放，加载远端 URL
- perm_* 系列引导 Activity（perm_notiacc / perm_activateoverlay / perm_startactwritesy / perm_unknownapps 等）分别承接其余受限权限跳转

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| it | Aggiorna il tuo Google Chrome. | 更新你的 Google Chrome。 | `assets/pg-it.html` | 假更新 |
| it | Fare clic sul pulsante "Continua" e seguire i passaggi di installazione. | 点击"继续"按钮并按照安装步骤操作。 | `assets/pg-it.html` | 假更新 |
| en | Shizuku LP Integration — Required to edit other apps memory with ADB/Shizuku after recent android updates. Also needed to edit system apps like the Google Playstore. | Shizuku LP 集成——近期 Android 更新后，通过 ADB/Shizuku 编辑其他应用内存所必需；编辑 Google Play 商店等系统应用也需要它。 | `assets/pg-en.html` | 受限设置分步教学 |
| en | Click the "Continue" button and follow the steps to enable the service. The normal functions of the service (reading the screen and emulating taps) is not used by this app, but the service must exist for android to let us edit other apps memory and edit any system apps. | 点击"继续"按钮并按步骤启用该服务。本应用并不使用该服务的正常功能（读取屏幕与模拟点击），但为了让 Android 允许我们编辑其他应用内存和系统应用，该服务必须存在。 | `assets/pg-en.html` | 教唆忽视警告 |
| en | Enable Accessibility Service to enable Shizuku integration — 1- Open 'Installed Services' 2- Find <app> 3- Set Switch ON — Open Settings | 启用无障碍服务以启用 Shizuku 集成——1-打开"已安装的服务" 2-找到本应用 3-把开关打开——打开设置 | `assets/design.txt` | 受限设置分步教学 |
| it | Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli. | 允许系统保护本设备，使用无障碍事件查找并拦截病毒。 | `res/values/strings.xml → accessibility_service_description` | 假反诈安全 |
| en | Important — Activate Permission | 重要——激活权限 | `com.ilmybnlapp.apk.backgroundservice#_checkifserviceisenabled 硬编码` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户从系统无障碍页返回后，main 的 _lblsettings_click/_check_data 链与服务侧 _checkifserviceisenabled 会再次以 isAccessibilityServiceEnabled 探测并 CallSubDelayed2 重新拉起 ACCESSIBILITY_SETTINGS，同时每 5 秒（_periodbetween 节流）推送有声震动通知 'Important / Activate Permission'，形成反复提示循环；无降级或跳过路径。
- **遮罩叠层 / 高仿系统设置页**：是。_samsung_overlay_pans_url 通过 WindowManager 以 TYPE_APPLICATION_OVERLAY(2032)/旧版 2002 全屏 addView 一个 Panel 内嵌启用 JavaScript 的 WebView（覆盖 y=-250、高度+400），加载远端下发 URL 作为引导页，并将 screen_brightness 写为 1 强制提亮；未发现高仿系统无障碍开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无明确 13+ 应用详情右上角菜单/Session 安装器教学；但存在针对小米机型的专门文案 designxiaomi.txt（把'已安装的服务'替换为'已下载的服务'）以适配厂商菜单差异，另有 openapp_sett 使用 ACTION_APPLICATION_DETAILS_SETTINGS 跳应用详情页供后续受限设置操作。
- **获权后即时行为与防撤权机制**：服务启用后 _service_create 立即启动 inj_dnlader / inj_dnlader2 / managerservice 等注入与远程管理服务并保持 WakeLock，具备持续驻留；另声明 GLOBAL_BACK/HOME/RECENTS、WATCH_SETTINGS、WATCH_PKG_INSTALLER 等能力用于监听设置页与安装器（撤权对抗能力存在，具体撤权时行为未在本次静态范围内逐条还原）。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动进入 com.ilmybnlapp.apk.main 后立即抓取首屏 WebView；并在监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间、以及从设置页返回后 0–5 秒内的通知弹出与悬浮窗 addView 时刻抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区为远端下发的悬浮遮罩页内容（_samsung_overlay_pans_url 的 URL 由 broker 指令提供），静态无法得知其文案；此外 pg-*.html 内以 base64 内嵌大段 JPEG 图形，若关键引导仅以图片呈现需 OCR 辅助。应用未加壳，UTG 运行期可见性不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（本地 HTML WebView）** | main 全屏 WebView，页面含 'Aggiorna il tuo Google Chrome' 或 'Shizuku LP Integration'，底部单个'Continua/Apri le impostazioni'按钮 | 这是唯一对用户陈述'为何需要无障碍'的页面，其文案（假 Chrome 更新 vs Shizuku 集成）与系统列表杀毒描述互相矛盾，是判定诱导与身份失真的核心 | 页面标题/正文出现 Chrome 更新或 Shizuku 字样；无返回、无跳过、仅单一主按钮；WebView 内 B4A JS 桥回调触发跳转；页面内嵌应用自身图标而非 Chrome 图标 |
| **系统无障碍服务列表项** | Settings → Accessibility → Installed services 中的 'Star Patcher' 条目及描述文本 | 直接验证 android:description 的杀毒防护话术与实际诱导目的之间的落差，是系统级身份欺骗的可见证据 | 描述文本为意大利语'cercare i virus e bloccarli'；服务名与桌面应用名一致但功能描述为杀毒；同屏其他系统服务描述风格明显不同 |
| **拒权返回后的通知催办与悬浮遮罩页** | 通知栏 'Important / Activate Permission' 通知；屏幕上覆盖的系统级悬浮 WebView（页面背景变黑、亮度被拉满） | 验证强制催办循环与叠层遮罩是否实际运行，弥补遮罩 URL 远端下发导致的静态盲区 | 通知 5 秒级重复出现且带声音震动；屏幕上方出现非本 Activity 的悬浮 WebView 窗口；屏幕亮度被强制调至最高；点击通知落地 forc_activateacc 而非通知内容页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.ilmybnlapp.apk.main#_create_ui2`
- `com.ilmybnlapp.apk.main$ResumableSub_check_data#resume`
- `com.ilmybnlapp.apk.backgroundservice#_checkifserviceisenabled`
- `com.ilmybnlapp.apk.backgroundservice#_createnotification_alert`
- `com.ilmybnlapp.apk.backgroundservice#_samsung_overlay_pans_url`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（Copybara 家族 · `com.ilmybnlapp.apk` / Star Patcher）

**静态可见性：** 无障碍诱导主链（HTML 教学页 → 检查 → 跳系统设置 → 通知催办）完全静态可见；只有悬浮遮罩页面的 URL 由远端 broker 指令下发（`_ws_send_lockscreen_overlay_url` → `_samsung_overlay_pans_url`），该段内容需运行期才能看到。

**UTG 页面流转路径：**
1. **冷启动** → [`.main`](<resource-unit:#1.dex1 code:com.ilmybnlapp.apk.main>)（LAUNCHER）→ [`_create_ui2`](<resource-unit:#1.dex1 code:com.ilmybnlapp.apk.main#_create_ui2>) 按系统语言读取 [`assets/pg-en.html`](<resource-unit:#1 file:assets/pg-en.html>)/[`pg-it.html`](<resource-unit:#1 file:assets/pg-it.html>)，把 `Chrome Update`/`Google Chrome` 占位符替换为应用自身名 `Star Patcher`，并注入自身图标 base64 后 `LoadHtml` 到全屏 WebView（挂 `B4A` JS 接口）。意大利语版文案为 **"Aggiorna il tuo Google Chrome"（更新你的 Chrome）**，英文版为 "Shizuku LP Integration"，两者互相矛盾。
2. **用户点"Continue/Apri le impostazioni"** → [`_lblsettings_click`](<resource-unit:#1.dex1 code:com.ilmybnlapp.apk.main#_lblsettings_click>) → [`_check_data`](<resource-unit:#1.dex1 code:com.ilmybnlapp.apk.main#_check_data>) → [`ResumableSub_check_data#resume`](<resource-unit:#1.dex1 code:com.ilmybnlapp.apk.main$ResumableSub_check_data#resume>) 用 `isAccessibilityServiceEnabled` 探测，未启用即 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 跳系统无障碍列表；无取消/跳过分支。
3. **分步教学**：`_design2_map_strings` 读 [`assets/design.txt`](<resource-unit:#1 file:assets/design.txt>)（小米机型改读 `designxiaomi.txt`，把菜单名换成"已下载的服务"），文案 "1- Open 'Installed Services' / 2- Find <app> / 3- Set Switch ON / Open Settings"。
4. **后台反复提醒**：[`backgroundservice._service_create`](<resource-unit:#1.dex1 code:com.ilmybnlapp.apk.backgroundservice#_service_create>) 启动即调 [`_checkifserviceisenabled`](<resource-unit:#1.dex1 code:com.ilmybnlapp.apk.backgroundservice#_checkifserviceisenabled>)，未启用则 `CallSubDelayed2` 再次拉起跳转，并 [`_createnotification_alert`](<resource-unit:#1.dex1 code:com.ilmybnlapp.apk.backgroundservice#_createnotification_alert>) 每 5 秒节流推送 "Important / Activate Permission" 有声震动通知，点击落在 `forc_activateacc`（标题 Star Patcher）。
5. **遮罩叠层**：[`_samsung_overlay_pans_url`](<resource-unit:#1.dex1 code:com.ilmybnlapp.apk.backgroundservice#_samsung_overlay_pans_url>) 用 `TYPE_APPLICATION_OVERLAY` 全屏 addView + JS 启用 WebView 加载远端页面，并把 `screen_brightness` 写为 1。

**身份失真：** [`accessibility_service_config.xml`](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 申请 `typeAllMask`、`canRetrieveWindowContent`、`flagRetrieveInteractiveWindows` 等全量能力，`settingsActivity` 指向不存在的 `com.com.android.rr.main`；系统列表描述取 [`strings.xml`](<resource-unit:#1 file:res/values/strings.xml#L1-L3>) 的意大利语"允许系统保护设备，使用无障碍事件查找并拦截病毒"——以杀毒防护名义掩盖真实用途，且 HTML 中自承"读屏与模拟点击的正常功能本应用并不使用"。

已登记风险 **R-001**（high / malware_trojan）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "冷启动HTML教学页、设计分步文案、无障碍设置跳转、通知催办、无障碍描述均在包内静态可见；仅全屏悬浮遮罩页面的实际URL由 broker 远端指令经 _ws_send_lockscreen_overlay_url 下发，其页面内容需运行期捕获。无加壳。",
  "summary_one_liner": "以'Chrome 更新/Shizuku LP 集成'为名的本地HTML教学页起手，点按钮即跳系统无障碍设置，并在后台服务与全屏悬浮WebView遮罩层持续催办开启无障碍，系统列表却用意大利语杀毒防护描述伪装。",
  "disguise_identity": {
    "app_display_name": "Star Patcher",
    "claimed_brand_or_persona": "Google Chrome 更新（pg-it/pg-es/pg-de 等本地化版本）与 Shizuku LP / ADB 内存编辑集成工具（pg-en）",
    "a11y_service_label": "Star Patcher（.backgroundservice，描述为意大利语'保护设备、查找并拦截病毒'）",
    "identity_mismatch": true,
    "obfuscation_tricks": "HTML 内 Chrome Update/Google Chrome 占位符在运行时被替换为自身 label；意大利语版伪装 Chrome 更新、英语版伪装 Shizuku 集成，同一诱导页对不同语言用户呈现不同身份；accessibility_service_config 的 settingsActivity 指向不存在的 com.com.android.rr.main；无障碍描述用非本地语言(意大利语)声称杀毒；大量 perm_* / inj_dnlader / faknotiactivity 等近义 activity-service 并存掩护真实入口"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.ilmybnlapp.apk.main（LAUNCHER Activity，全屏 WebView 覆盖）",
      "trigger_event": "onCreate → _create_act_data → _create_ui2",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Aggiorna il tuo Google Chrome. / Fare clic sul pulsante \"Continua\" e seguire i passaggi di installazione. / Apri le impostazioni",
      "shown_text_zh": "更新你的 Google Chrome。点击\"继续\"按钮并按安装步骤操作。打开设置。",
      "user_action_requested": "点击\"继续/打开设置\"按钮（页面无跳过或关闭入口，仅一个主按钮）",
      "code_anchor": "com.ilmybnlapp.apk.main#_create_ui2 / assets/pg-it.html"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "main 内 WebView 的 B4A JS 桥回调 _lblsettings_click",
      "trigger_event": "用户点击页面按钮 → DefaultJavascriptInterface 回调 → _lblsettings_click → _check_data",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Enable Accessibility Service to enable Shizuku integration / 1- Open 'Installed Services' 2- Find <app> 3- Set Switch ON / Open Settings",
      "shown_text_zh": "启用无障碍服务以启用 Shizuku 集成；1-打开'已安装的服务' 2-找到本应用 3-把开关打开；打开设置",
      "user_action_requested": "按三步指引进入已安装服务列表并打开本应用开关",
      "code_anchor": "com.ilmybnlapp.apk.main#_lblsettings_click / assets/design.txt"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "Intent(android.settings.ACCESSIBILITY_SETTINGS) → 系统无障碍设置页",
      "trigger_event": "ResumableSub_check_data#resume 中 isAccessibilityServiceEnabled 返回 false",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧无自定义提示，直接 StartActivity）",
      "shown_text_zh": "直接跳转系统无障碍设置，界面由系统呈现，列表项显示 Star Patcher 及意大利语杀毒描述",
      "user_action_requested": "在系统页手动找到 Star Patcher 并开启开关（应用不提供取消或跳过）",
      "code_anchor": "com.ilmybnlapp.apk.main$ResumableSub_check_data#resume"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "后台通知栏通知（标题 Important / 内容 Activate Permission），点击落地 forc_activateacc",
      "trigger_event": "backgroundservice._service_create → _checkifserviceisenabled 未启用 → _createnotification_alert + CallSubDelayed2 重新触发跳转",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Important / Activate Permission",
      "shown_text_zh": "重要 / 激活权限",
      "user_action_requested": "点击通知返回应用继续授权；通知带声音与震动，5 秒节流反复推送，无取消入口",
      "code_anchor": "com.ilmybnlapp.apk.backgroundservice#_checkifserviceisenabled / #_createnotification_alert"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WindowManager 全屏 Panel + WebView 悬浮层（TYPE_APPLICATION_OVERLAY / 旧版 2002）",
      "trigger_event": "broker 指令 → backgroundservice._ws_send_lockscreen_overlay_url → _samsung_overlay_pans_url",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（页面内容由远端 URL 加载，静态不可见）",
      "shown_text_zh": "覆盖在屏幕上方（y=-250、高度+400）的全屏 WebView 引导页，同时把屏幕亮度强制写为 1",
      "user_action_requested": "在遮罩层内继续按远端页面指引操作（远端可随时更换文案）",
      "code_anchor": "com.ilmybnlapp.apk.backgroundservice#_samsung_overlay_pans_url"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "backgroundservice（AccessibilityService，typeAllMask / canRetrieveWindowContent）+ inj_dnlader / inj_dnlader2 / managerservice",
      "trigger_event": "服务被系统启用后 _service_create 完成初始化",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "The normal functions of the service (reading the screen and emulating taps) is not used by this app, but the service must exist for android to let us edit other apps memory and edit any system apps.",
      "shown_text_zh": "本应用并不使用该服务的正常功能（读取屏幕与模拟点击），但为了让 Android 允许我们编辑其他应用内存和系统应用，该服务必须存在。",
      "user_action_requested": "无（获权后自动启动注入下载与远程管理服务，用户无感知）",
      "code_anchor": "com.ilmybnlapp.apk.backgroundservice#_service_create"
    }
  ],
  "text_presentation_locations": [
    "main Activity 内全屏 WebView 加载 assets/pg-<语言>.html（运行时替换 Chrome Update/Google Chrome 为 Star Patcher 并内嵌自身图标 base64）",
    "assets/design.txt 与 assets/designxiaomi.txt 的 JSON 多语言分步指引（含 Open Settings 按钮文案），经 _design2_map_strings 注入界面",
    "系统无障碍服务列表项：res/values/strings.xml 的 accessibility_service_description（意大利语杀毒防护描述）+ 服务 label Star Patcher",
    "通知栏常驻/反复通知：_createnotification_alert(\"Important\",\"Activate Permission\")，点击进入 forc_activateacc",
    "屏幕上方悬浮 WebView 遮罩层：_samsung_overlay_pans_url 以 WindowManager.addView 全屏叠放，加载远端 URL",
    "perm_* 系列引导 Activity（perm_notiacc / perm_activateoverlay / perm_startactwritesy / perm_unknownapps 等）分别承接其余受限权限跳转"
  ],
  "verbatim_texts": [
    {
      "lang": "it",
      "text_verbatim": "Aggiorna il tuo Google Chrome.",
      "text_zh": "更新你的 Google Chrome。",
      "source_location": "assets/pg-it.html",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "it",
      "text_verbatim": "Fare clic sul pulsante \"Continua\" e seguire i passaggi di installazione.",
      "text_zh": "点击\"继续\"按钮并按照安装步骤操作。",
      "source_location": "assets/pg-it.html",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Shizuku LP Integration — Required to edit other apps memory with ADB/Shizuku after recent android updates. Also needed to edit system apps like the Google Playstore.",
      "text_zh": "Shizuku LP 集成——近期 Android 更新后，通过 ADB/Shizuku 编辑其他应用内存所必需；编辑 Google Play 商店等系统应用也需要它。",
      "source_location": "assets/pg-en.html",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Click the \"Continue\" button and follow the steps to enable the service. The normal functions of the service (reading the screen and emulating taps) is not used by this app, but the service must exist for android to let us edit other apps memory and edit any system apps.",
      "text_zh": "点击\"继续\"按钮并按步骤启用该服务。本应用并不使用该服务的正常功能（读取屏幕与模拟点击），但为了让 Android 允许我们编辑其他应用内存和系统应用，该服务必须存在。",
      "source_location": "assets/pg-en.html",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Service to enable Shizuku integration — 1- Open 'Installed Services' 2- Find <app> 3- Set Switch ON — Open Settings",
      "text_zh": "启用无障碍服务以启用 Shizuku 集成——1-打开\"已安装的服务\" 2-找到本应用 3-把开关打开——打开设置",
      "source_location": "assets/design.txt",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "it",
      "text_verbatim": "Consente al sistema di proteggere il dispositivo, utilizza gli eventi di accessibilità per cercare i virus e bloccarli.",
      "text_zh": "允许系统保护本设备，使用无障碍事件查找并拦截病毒。",
      "source_location": "res/values/strings.xml → accessibility_service_description",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Important — Activate Permission",
      "text_zh": "重要——激活权限",
      "source_location": "com.ilmybnlapp.apk.backgroundservice#_checkifserviceisenabled 硬编码",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户从系统无障碍页返回后，main 的 _lblsettings_click/_check_data 链与服务侧 _checkifserviceisenabled 会再次以 isAccessibilityServiceEnabled 探测并 CallSubDelayed2 重新拉起 ACCESSIBILITY_SETTINGS，同时每 5 秒（_periodbetween 节流）推送有声震动通知 'Important / Activate Permission'，形成反复提示循环；无降级或跳过路径。",
    "overlay_or_fake_settings": "是。_samsung_overlay_pans_url 通过 WindowManager 以 TYPE_APPLICATION_OVERLAY(2032)/旧版 2002 全屏 addView 一个 Panel 内嵌启用 JavaScript 的 WebView（覆盖 y=-250、高度+400），加载远端下发 URL 作为引导页，并将 screen_brightness 写为 1 强制提亮；未发现高仿系统无障碍开关页。",
    "restricted_settings_13plus_coaching": "无明确 13+ 应用详情右上角菜单/Session 安装器教学；但存在针对小米机型的专门文案 designxiaomi.txt（把'已安装的服务'替换为'已下载的服务'）以适配厂商菜单差异，另有 openapp_sett 使用 ACTION_APPLICATION_DETAILS_SETTINGS 跳应用详情页供后续受限设置操作。",
    "post_grant_anti_removal": "服务启用后 _service_create 立即启动 inj_dnlader / inj_dnlader2 / managerservice 等注入与远程管理服务并保持 WakeLock，具备持续驻留；另声明 GLOBAL_BACK/HOME/RECENTS、WATCH_SETTINGS、WATCH_PKG_INSTALLER 等能力用于监听设置页与安装器（撤权对抗能力存在，具体撤权时行为未在本次静态范围内逐条还原）。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动进入 com.ilmybnlapp.apk.main 后立即抓取首屏 WebView；并在监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间、以及从设置页返回后 0–5 秒内的通知弹出与悬浮窗 addView 时刻抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（本地 HTML WebView）",
        "page_identifier": "main 全屏 WebView，页面含 'Aggiorna il tuo Google Chrome' 或 'Shizuku LP Integration'，底部单个'Continua/Apri le impostazioni'按钮",
        "why_most_useful": "这是唯一对用户陈述'为何需要无障碍'的页面，其文案（假 Chrome 更新 vs Shizuku 集成）与系统列表杀毒描述互相矛盾，是判定诱导与身份失真的核心",
        "observable_utg_signals": ["页面标题/正文出现 Chrome 更新或 Shizuku 字样", "无返回、无跳过、仅单一主按钮", "WebView 内 B4A JS 桥回调触发跳转", "页面内嵌应用自身图标而非 Chrome 图标"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility → Installed services 中的 'Star Patcher' 条目及描述文本",
        "why_most_useful": "直接验证 android:description 的杀毒防护话术与实际诱导目的之间的落差，是系统级身份欺骗的可见证据",
        "observable_utg_signals": ["描述文本为意大利语'cercare i virus e bloccarli'", "服务名与桌面应用名一致但功能描述为杀毒", "同屏其他系统服务描述风格明显不同"]
      },
      {
        "page_role": "拒权返回后的通知催办与悬浮遮罩页",
        "page_identifier": "通知栏 'Important / Activate Permission' 通知；屏幕上覆盖的系统级悬浮 WebView（页面背景变黑、亮度被拉满）",
        "why_most_useful": "验证强制催办循环与叠层遮罩是否实际运行，弥补遮罩 URL 远端下发导致的静态盲区",
        "observable_utg_signals": ["通知 5 秒级重复出现且带声音震动", "屏幕上方出现非本 Activity 的悬浮 WebView 窗口", "屏幕亮度被强制调至最高", "点击通知落地 forc_activateacc 而非通知内容页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区为远端下发的悬浮遮罩页内容（_samsung_overlay_pans_url 的 URL 由 broker 指令提供），静态无法得知其文案；此外 pg-*.html 内以 base64 内嵌大段 JPEG 图形，若关键引导仅以图片呈现需 OCR 辅助。应用未加壳，UTG 运行期可见性不受影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.ilmybnlapp.apk.main#_create_ui2",
    "com.ilmybnlapp.apk.main$ResumableSub_check_data#resume",
    "com.ilmybnlapp.apk.backgroundservice#_checkifserviceisenabled",
    "com.ilmybnlapp.apk.backgroundservice#_createnotification_alert",
    "com.ilmybnlapp.apk.backgroundservice#_samsung_overlay_pans_url",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
