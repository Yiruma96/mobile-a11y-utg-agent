# BN_064__3657b9fd96｜远程协助与跨设备互联 — MidnightBeam

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：94.4s

## 1. 一句话核心结论

- **核心申请方式**：MidnightBeam 在 TV 原生设置页和手机本地 HTML 的 setup 页第 2 步（标注 recommended）分别放置一个可选的无障碍开关入口，用户点击后由 Compat.enableOrOpenAccessibility 判断 WRITE_SECURE_SETTINGS，具备则静默开启、否则打开系统无障碍设置页，弹窗仅一次且带 Later 取消，无遮罩、无循环、无撤权对抗。
- **静态可见性说明**：全部引导逻辑静态可见：TV 端为 MainActivity.onCreate 原生 View 硬编码文案，手机端为本地 assets/app.html 内联 JS（setup 页第 2 步、一次性 a11y 弹窗）与 strings 式 L 对象，跳转为 Compat.enableOrOpenAccessibility 固定 ACTION_ACCESSIBILITY_SETTINGS；无加壳、无 AES 密文、无远端 HTML 承载引导。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3657b9fd963eae4d84ae2408683d2b35c4661d80a1ceec1561e762508b59e141` |
| 包名 / 年份 | `dev.midnightbeam` / 2025-2026 |
| 家族 / 品类 | **远程协助与跨设备互联**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/dev.midnightbeam_39.apk |
| 桌面显示名 | MidnightBeam |
| 引导页宣称品牌/身份 | MidnightBeam（F-Droid 开源项目，界面 wordmark 为 MIDNIGHTBEAM） |
| 系统无障碍列表服务名 | MidnightBeam（无障碍服务 .DimAccessibilityService，标签继承应用名，description 为 @string/accessibility_description） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `.DimAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Only used to draw the dimming overlay above everything, including the status and navigation bars, without blocking touches. It does not read the screen, your input or any app content, and it sends nothing anywhere. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | dev.midnightbeam.MainActivity（TV/LEANBACK 启动器）→ 非 TV 设备直接 startActivity(PhoneActivity) 并 finish | onCreate：Compat.isTv(this) 判定后分流 | 原生Activity | **原文**：无（仅分流逻辑，无引导文案）<br>**译注**：无 | 无 | `dev.midnightbeam.MainActivity.onCreate` |
| 2 | 引导说明页 | MainActivity 原生 ScrollView 内的 accessibilityHint TextView + accessibility 按钮（仅当 DimAccessibilityService.instance == null 时可见） | onCreate 构建视图；onResume / AccessibilityCheck.run 调用 refreshAccessibility 控制可见性 | 原生Activity | **原文**：To cover the screensaver and the system bars too (and for full darkness), enable MidnightBeam in Accessibility / Enable<br>**译注**：为了同时覆盖屏保和系统栏（并实现全黑），请在「无障碍」中启用 MidnightBeam / 启用 | 用户可选点击「Enable」按钮；不点击则调光功能照常以普通悬浮窗运行，无强制 | `dev.midnightbeam.MainActivity.onCreate / dev.midnightbeam.MainActivity.refreshAccessibility` |
| 3 | 业务功能触发 | PhoneActivity 内本地 WebView（assets/app.html）的 setup 页第 2 步卡片（id=su-s2，tag=recommended） | 首次加载 home 视图时 permissionPopup()（条件 app.sdk >= 31 && !app.accessibility && !store('mb_a11y_tip')）弹一次性引导，或用户点设置页「设置」入口进入 setup | 本地HTML WebView | **原文**：For full darkness / On this Android version the filter stops at 80% darkness and does not cover the navigation bar unless MidnightBeam is enabled in Accessibility. It is optional and it reads nothing on the screen. — Enable / Later；卡片文案：Without it, Android 12 and later cap the filter at 80% darkness and leave the navigation bar uncovered. In Accessibility, open MidnightBeam (it may be under Installed apps or Downloaded apps) and turn it on. It reads nothing on the screen.<br>**译注**：为了全黑：在此 Android 版本上，除非在无障碍中启用 MidnightBeam，调光最高只能到 80% 且不会覆盖导航栏。该项为可选，且不会读取屏幕上的任何内容。— 启用 / 稍后；卡片：若不启用，Android 12 及以后调光被限制在 80% 且导航栏不被覆盖。请到无障碍里找到 MidnightBeam（可能位于「已安装的应用」或「已下载的应用」下）并开启。它不会读取屏幕内容。 | 点击「Enable / 启用」或「Later / 稍后」；卡片标注 recommended，第 1 步「显示在其他应用上层」才标 required，且 su-done 仅在 overlay 已授予时可用 | `assets/app.html permissionPopup() L1350-L1364；assets/app.html setup 卡片 L282-L289；assets/app.html renderSetup L1333-L1345` |
| 4 | 跳无障碍设置 | 系统「设置 → 无障碍」页（Intent.ACTION_ACCESSIBILITY_SETTINGS，FLAG_ACTIVITY_NEW_TASK） | WebView 链接 midnightbeam-app://accessibility → AppWebClient.shouldOverrideUrlLoading 识别自定义 scheme → PhoneActivity.appAction("accessibility") → Compat.enableOrOpenAccessibility；或 TV 端 onClick(view == accessibility) | 系统无障碍页 | **原文**：无（直接跳系统页，不叠加任何自绘界面）<br>**译注**：无 | 用户自行在系统无障碍列表中打开 MidnightBeam 开关（服务名即应用名 MidnightBeam） | `dev.midnightbeam.Compat.enableOrOpenAccessibility / dev.midnightbeam.Compat.accessibilitySettings / dev.midnightbeam.PhoneActivity.appAction` |
| 5 | 获权后动作 | DimAccessibilityService.onServiceConnected → startForegroundService(DimService, refresh=true)，叠加调光遮罩 | 系统绑定无障碍服务时回调 onServiceConnected | 悬浮窗Overlay | 无 | 无；返回应用后 onResume → refreshAccessibility 自动隐藏提示与按钮，WebView 通过 /api/app 返回 accessibility=true 隐藏第 2 步卡片 | `dev.midnightbeam.DimAccessibilityService.onServiceConnected / dev.midnightbeam.DimAccessibilityService.refresh / dev.midnightbeam.MainActivity.onResume` |
| 6 | 拒权反馈循环 | 返回 MainActivity / PhoneActivity 后的状态刷新 | onResume、以及点击后 1500ms 的 AccessibilityCheck.run | 原生Activity | **原文**：无（仅按 instance 是否为空决定提示/按钮显隐，无重复弹窗或强制跳转）<br>**译注**：无 | 无；用户可随时放弃，调光功能以普通悬浮窗方式继续工作 | `dev.midnightbeam.MainActivity.refreshAccessibility / dev.midnightbeam.MainActivity$AccessibilityCheck.run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表服务说明：res/xml/accessibility_service.xml 的 android:description=@string/accessibility_description（'Only used to draw the dimming overlay above everything, including the status and navigation bars, without blocking touches. It does not read the screen, your input or any app content, and it sends nothing anywhere.'）
- TV 端 MainActivity 原生 ScrollView 内的 accessibilityHint TextView（硬编码 t("en","it") 双语文案，代码内联，非 strings.xml）
- 手机端 assets/app.html setup 视图第 2 步卡片（id=su-s2，tag=recommended）及 #su-t2 动态状态文字
- 手机端 assets/app.html permissionPopup() 一次性弹层（popA11yTitle='For full darkness'，含 Enable / Later）
- assets/app.html 设置页状态行 #st-setup（setupA11y 提示）与 L.a11yButton='Open Accessibility settings'
- assets/app.html 睡眠/关机说明 sleepNote 中提及 box 亦可使用无障碍服务（辅助说明，非引导入口）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Only used to draw the dimming overlay above everything, including the status and navigation bars, without blocking touches. It does not read the screen, your input or any app content, and it sends nothing anywhere. | 仅用于在所有内容（包括状态栏和导航栏）之上绘制调光遮罩，且不拦截触摸。它不读取屏幕、你的输入或任何应用内容，也不向任何地方发送数据。 | `res/values/strings.xml → accessibility_description（被 res/xml/accessibility_service.xml 引用）` | 良性透明说明 |
| en | To cover the screensaver and the system bars too (and for full darkness), enable MidnightBeam in Accessibility | 为了同时覆盖屏保和系统栏（并实现全黑），请在「无障碍」中启用 MidnightBeam | `dev.midnightbeam.MainActivity.onCreate 硬编码 t(en,it)` | 良性透明说明 |
| en | For full darkness | 为了全黑 | `assets/app.html L540 popA11yTitle` | 良性透明说明 |
| en | On this Android version the filter stops at 80% darkness and does not cover the navigation bar unless MidnightBeam is enabled in Accessibility. It is optional and it reads nothing on the screen. | 在此 Android 版本上，除非在无障碍中启用 MidnightBeam，调光最高只能到 80% 且不会覆盖导航栏。该项为可选，且不会读取屏幕上的任何内容。 | `assets/app.html L540 popA11yText` | 良性透明说明 |
| en | Without it, Android 12 and later cap the filter at 80% darkness and leave the navigation bar uncovered. In Accessibility, open MidnightBeam (it may be under Installed apps or Downloaded apps) and turn it on. It reads nothing on the screen. | 若不启用，Android 12 及以后调光被限制在 80% 且导航栏不被覆盖。请到无障碍中打开 MidnightBeam（可能位于「已安装的应用」或「已下载的应用」下）并开启。它不会读取屏幕内容。 | `assets/app.html L534 stA11yText` | 受限设置分步教学 |
| en | Android 12+ limits overlays to 80% darkness. For full darkness and to cover the system bars, enable MidnightBeam in Accessibility (optional, it reads nothing). | Android 12+ 将悬浮窗限制在 80% 暗度。要实现全黑并覆盖系统栏，请在无障碍中启用 MidnightBeam（可选，它不读取任何内容）。 | `assets/app.html L530 a11yText` | 良性透明说明 |
| it | Per il buio totale | 为了全黑 | `assets/app.html L597 popA11yTitle（意大利语本地化）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环：返回应用后仅 onResume 与一次 1500ms 延迟检查刷新按钮/提示可见性，不重跳设置；WebView 侧一次性提示由 store('mb_a11y_tip') 标记后不再弹出，并提供 Later 关闭
- **遮罩叠层 / 高仿系统设置页**：无。不叠放半透明引导遮罩或全屏悬浮窗，不伪造系统无障碍开关页；悬浮窗仅用于调光遮罩本身
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未跳转 ACTION_APPLICATION_DETAILS_SETTINGS，未出现「右上角菜单允许受限设置」类教学，亦未使用 Session 安装器绕过
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅置 instance 并刷新 DimService；performGlobalAction(8) 出现在 DimService.powerAction 用于定时休眠/关机的返回动作，不用于阻止撤权；未监听设置页回退
- **良性降级 / 替代方案**：有。无障碍为可选增强（recommended）：不开启时仍以 SYSTEM_ALERT_WINDOW 悬浮窗调光，仅受 Android 12+ 80% 暗度与系统栏不可覆盖限制；另提供手机远程控制（PhoneActivity/本地 HTTP 8765）与 root/本地 ADB 关机等替代路径，setup 页 su-done 仅在 overlay 授予后启用

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS（由 Compat.enableOrOpenAccessibility 发起）时立即拉起；其次在 PhoneActivity WebView 首次加载 home 视图触发 permissionPopup 一次性弹层时拉起
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导文案为可提取文本，未使用纯图/空文本诱饵；无加壳、无二阶段 Dropper、无远端 HTML 下发（app.html 为包内本地资源）。仅 DimService 本地 HTTP 服务与 WebView AppApi 桥接的完整接口面未逐行审计，若需评估数据外发应另行覆盖。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动一次性引导弹层页（手机端）** | PhoneActivity 内本地 WebView，标题文本 'For full darkness'，含 Enable / Later 两个按钮 | 区分该应用是否以「全黑/覆盖系统栏」功能性理由提出可选请求，还是以恐吓/假更新/假安全为诱饵 | 标题与正文字面文本（For full darkness / It is optional）；是否同时存在 Later 取消按钮；是否出现假更新、病毒、故障等恐吓关键词 |
| **setup 教学页（步骤卡片）** | WebView setup 视图：第 1 步 'Display over other apps' 标 Required，第 2 步 'Accessibility (full darkness)' 标 Recommended | 判断无障碍被呈现为可选增强还是强制前置，以及是否含受限设置分步教学 | required / recommended 标签分布；第 2 步按钮是否存在跳过路径；是否出现「应用详情 → 右上角菜单 → 允许受限设置」类文字 |
| **系统无障碍服务列表项** | 系统设置无障碍页中 'MidnightBeam' 条目及其 description 展开文本 | 核验系统侧呈现的服务名与说明是否与代码内承诺一致、有无同形字/空白伪装 | 服务显示名是否等于应用名 MidnightBeam；description 是否含 'does not read the screen' 承诺；有无异常长空白或不可见字符 |
| **跳设置后叠层核验页** | 系统无障碍页上层是否出现任何自绘悬浮窗/遮罩 | 排除「遮罩叠压系统设置页引导点击」这一典型诱导手法 | 无障碍页面上是否存在非系统 overlay 节点；是否出现高仿开关控件；页面是否被半透明层覆盖 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `dev.midnightbeam.Compat.enableOrOpenAccessibility`
- `dev.midnightbeam.Compat.accessibilitySettings`
- `dev.midnightbeam.PhoneActivity.appAction`
- `dev.midnightbeam.MainActivity.onCreate`
- `assets/app.html permissionPopup() L1350-L1364`
- `res/xml/accessibility_service.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**定性：良性、透明、按需引导，无诱导攻击特征。**

1. **引导的入口有两条，都来自用户主动触发**
   - **TV 原生界面**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:dev.midnightbeam.MainActivity#onCreate>) 构建原生 `ScrollView`，其中放入提示文字 `accessibilityHint`（“To cover the screensaver and the system bars too (and for full darkness), enable MidnightBeam in Accessibility”）和一个 “Enable” 按钮；[onClick()](<resource-unit:#1.dex1 code:dev.midnightbeam.MainActivity#onClick>) 只有在用户点击这个按钮后才走跳转流程。
   - **手机端本地 WebView**：非 TV 设备在 `onCreate` 中直接转到 [PhoneActivity](<resource-unit:#1.dex1 code:dev.midnightbeam.PhoneActivity>)，由它加载 `assets/app.html`。其中 `setup` 页第 2 步卡片标注为 **recommended（非必需）**，链接 `midnightbeam-app://accessibility` 经 [AppWebClient.shouldOverrideUrlLoading()](<resource-unit:#1.dex1 code:dev.midnightbeam.AppWebClient#shouldOverrideUrlLoading>) → [PhoneActivity.appAction()](<resource-unit:#1.dex1 code:dev.midnightbeam.PhoneActivity#appAction>) 进入跳转逻辑。

2. **跳转实现单一且标准**：[Compat.enableOrOpenAccessibility()](<resource-unit:#1.dex1 code:dev.midnightbeam.Compat#enableOrOpenAccessibility>) 先用 `checkSelfPermission(WRITE_SECURE_SETTINGS)` 判断；如果具备（例如通过 ADB 授权），就[静默写入 `enabled_accessibility_services`](<resource-unit:#1.dex1 code:dev.midnightbeam.Compat#enableAccessibility>)；否则调用 `startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 打开系统无障碍设置页。**未发现**跳转 `ACTION_APPLICATION_DETAILS_SETTINGS`、未发现“受限设置”分步教学、未发现 Session 安装器绕过。

3. **拒权反馈：没有诱导或反复弹窗**。[MainActivity.onResume()](<resource-unit:#1.dex1 code:dev.midnightbeam.MainActivity#refreshAccessibility>) 只根据 `DimAccessibilityService.instance` 是否存在来显示或隐藏按钮；`AccessibilityCheck`（延迟 1500ms）也做同样处理。WebView 侧的 a11y 弹窗使用 `store('mb_a11y_tip')` **只弹一次**，并带 “Later” 取消按钮；[permissionPopup()](<resource-unit:#1 file:assets/app.html#L1350-L1364>)。

4. **没有遮罩式指引，也没有仿系统页面**：未发现悬浮引导窗叠在系统设置页上，也未发现高仿无障碍开关页；唯一悬浮窗用途是调光遮罩（`SYSTEM_ALERT_WINDOW`/`MANAGE_OVERLAY_PERMISSION` 步骤 1，属必需功能）。

5. **服务声明最小化、与描述一致**：[accessibility_service.xml](<resource-unit:#1 file:res/xml/accessibility_service.xml>) 仅 `typeWindowStateChanged`、`canRetrieveWindowContent="false"`、`feedbackGeneric`，无 `flagRequestFilterKeyEvents` 等；[onAccessibilityEvent()](<resource-unit:#1.dex1 code:dev.midnightbeam.DimAccessibilityService#onAccessibilityEvent>) 是**空方法体**，`onServiceConnected` 仅置 `instance` 并 `startForegroundService(DimService)` 刷新遮罩。获权后**无自点确认、无阻止撤权**。

6. **关于预筛 `PERFORM_GLOBAL_ACTION`**：唯一调用点在 [DimService.powerAction](<resource-unit:#1.dex1 code:dev.midnightbeam.DimService#powerAction>) 的 `performGlobalAction(8)`（`GLOBAL_ACTION_BACK`），用于定时休眠/关机后返回，与撤权对抗无关。预筛 `SESSION_INSTALLER` 未在无障碍链路中定位到对应实现，属未证实线索。

7. **身份一致**：桌面名 `MidnightBeam`、界面 wordmark `MIDNIGHTBEAM`、无障碍列表项同名（`android:label` 继承应用名），无空白/同形字/多 `activity-alias` 伪装，无 `isAccessibilityTool` 伪造。

**覆盖边界**：`DimService` 的本地 HTTP 服务与 WebView `AppApi` 桥接未做逐行审计（本轮范围聚焦无障碍引导链路）；`SESSION_INSTALLER` 线索未证实。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑静态可见：TV 端为 MainActivity.onCreate 原生 View 硬编码文案，手机端为本地 assets/app.html 内联 JS（setup 页第 2 步、一次性 a11y 弹窗）与 strings 式 L 对象，跳转为 Compat.enableOrOpenAccessibility 固定 ACTION_ACCESSIBILITY_SETTINGS；无加壳、无 AES 密文、无远端 HTML 承载引导。",
  "summary_one_liner": "MidnightBeam 在 TV 原生设置页和手机本地 HTML 的 setup 页第 2 步（标注 recommended）分别放置一个可选的无障碍开关入口，用户点击后由 Compat.enableOrOpenAccessibility 判断 WRITE_SECURE_SETTINGS，具备则静默开启、否则打开系统无障碍设置页，弹窗仅一次且带 Later 取消，无遮罩、无循环、无撤权对抗。",
  "disguise_identity": {
    "app_display_name": "MidnightBeam",
    "claimed_brand_or_persona": "MidnightBeam（F-Droid 开源项目，界面 wordmark 为 MIDNIGHTBEAM）",
    "a11y_service_label": "MidnightBeam（无障碍服务 .DimAccessibilityService，标签继承应用名，description 为 @string/accessibility_description）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "dev.midnightbeam.MainActivity（TV/LEANBACK 启动器）→ 非 TV 设备直接 startActivity(PhoneActivity) 并 finish",
      "trigger_event": "onCreate：Compat.isTv(this) 判定后分流",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅分流逻辑，无引导文案）",
      "shown_text_zh": "无",
      "user_action_requested": "无",
      "code_anchor": "dev.midnightbeam.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 原生 ScrollView 内的 accessibilityHint TextView + accessibility 按钮（仅当 DimAccessibilityService.instance == null 时可见）",
      "trigger_event": "onCreate 构建视图；onResume / AccessibilityCheck.run 调用 refreshAccessibility 控制可见性",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "To cover the screensaver and the system bars too (and for full darkness), enable MidnightBeam in Accessibility / Enable",
      "shown_text_zh": "为了同时覆盖屏保和系统栏（并实现全黑），请在「无障碍」中启用 MidnightBeam / 启用",
      "user_action_requested": "用户可选点击「Enable」按钮；不点击则调光功能照常以普通悬浮窗运行，无强制",
      "code_anchor": "dev.midnightbeam.MainActivity.onCreate / dev.midnightbeam.MainActivity.refreshAccessibility"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "PhoneActivity 内本地 WebView（assets/app.html）的 setup 页第 2 步卡片（id=su-s2，tag=recommended）",
      "trigger_event": "首次加载 home 视图时 permissionPopup()（条件 app.sdk >= 31 && !app.accessibility && !store('mb_a11y_tip')）弹一次性引导，或用户点设置页「设置」入口进入 setup",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "For full darkness / On this Android version the filter stops at 80% darkness and does not cover the navigation bar unless MidnightBeam is enabled in Accessibility. It is optional and it reads nothing on the screen. — Enable / Later；卡片文案：Without it, Android 12 and later cap the filter at 80% darkness and leave the navigation bar uncovered. In Accessibility, open MidnightBeam (it may be under Installed apps or Downloaded apps) and turn it on. It reads nothing on the screen.",
      "shown_text_zh": "为了全黑：在此 Android 版本上，除非在无障碍中启用 MidnightBeam，调光最高只能到 80% 且不会覆盖导航栏。该项为可选，且不会读取屏幕上的任何内容。— 启用 / 稍后；卡片：若不启用，Android 12 及以后调光被限制在 80% 且导航栏不被覆盖。请到无障碍里找到 MidnightBeam（可能位于「已安装的应用」或「已下载的应用」下）并开启。它不会读取屏幕内容。",
      "user_action_requested": "点击「Enable / 启用」或「Later / 稍后」；卡片标注 recommended，第 1 步「显示在其他应用上层」才标 required，且 su-done 仅在 overlay 已授予时可用",
      "code_anchor": "assets/app.html permissionPopup() L1350-L1364；assets/app.html setup 卡片 L282-L289；assets/app.html renderSetup L1333-L1345"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍」页（Intent.ACTION_ACCESSIBILITY_SETTINGS，FLAG_ACTIVITY_NEW_TASK）",
      "trigger_event": "WebView 链接 midnightbeam-app://accessibility → AppWebClient.shouldOverrideUrlLoading 识别自定义 scheme → PhoneActivity.appAction(\"accessibility\") → Compat.enableOrOpenAccessibility；或 TV 端 onClick(view == accessibility)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（直接跳系统页，不叠加任何自绘界面）",
      "shown_text_zh": "无",
      "user_action_requested": "用户自行在系统无障碍列表中打开 MidnightBeam 开关（服务名即应用名 MidnightBeam）",
      "code_anchor": "dev.midnightbeam.Compat.enableOrOpenAccessibility / dev.midnightbeam.Compat.accessibilitySettings / dev.midnightbeam.PhoneActivity.appAction"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "DimAccessibilityService.onServiceConnected → startForegroundService(DimService, refresh=true)，叠加调光遮罩",
      "trigger_event": "系统绑定无障碍服务时回调 onServiceConnected",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无",
      "user_action_requested": "无；返回应用后 onResume → refreshAccessibility 自动隐藏提示与按钮，WebView 通过 /api/app 返回 accessibility=true 隐藏第 2 步卡片",
      "code_anchor": "dev.midnightbeam.DimAccessibilityService.onServiceConnected / dev.midnightbeam.DimAccessibilityService.refresh / dev.midnightbeam.MainActivity.onResume"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 MainActivity / PhoneActivity 后的状态刷新",
      "trigger_event": "onResume、以及点击后 1500ms 的 AccessibilityCheck.run",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅按 instance 是否为空决定提示/按钮显隐，无重复弹窗或强制跳转）",
      "shown_text_zh": "无",
      "user_action_requested": "无；用户可随时放弃，调光功能以普通悬浮窗方式继续工作",
      "code_anchor": "dev.midnightbeam.MainActivity.refreshAccessibility / dev.midnightbeam.MainActivity$AccessibilityCheck.run"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表服务说明：res/xml/accessibility_service.xml 的 android:description=@string/accessibility_description（'Only used to draw the dimming overlay above everything, including the status and navigation bars, without blocking touches. It does not read the screen, your input or any app content, and it sends nothing anywhere.'）",
    "TV 端 MainActivity 原生 ScrollView 内的 accessibilityHint TextView（硬编码 t(\"en\",\"it\") 双语文案，代码内联，非 strings.xml）",
    "手机端 assets/app.html setup 视图第 2 步卡片（id=su-s2，tag=recommended）及 #su-t2 动态状态文字",
    "手机端 assets/app.html permissionPopup() 一次性弹层（popA11yTitle='For full darkness'，含 Enable / Later）",
    "assets/app.html 设置页状态行 #st-setup（setupA11y 提示）与 L.a11yButton='Open Accessibility settings'",
    "assets/app.html 睡眠/关机说明 sleepNote 中提及 box 亦可使用无障碍服务（辅助说明，非引导入口）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Only used to draw the dimming overlay above everything, including the status and navigation bars, without blocking touches. It does not read the screen, your input or any app content, and it sends nothing anywhere.",
      "text_zh": "仅用于在所有内容（包括状态栏和导航栏）之上绘制调光遮罩，且不拦截触摸。它不读取屏幕、你的输入或任何应用内容，也不向任何地方发送数据。",
      "source_location": "res/values/strings.xml → accessibility_description（被 res/xml/accessibility_service.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To cover the screensaver and the system bars too (and for full darkness), enable MidnightBeam in Accessibility",
      "text_zh": "为了同时覆盖屏保和系统栏（并实现全黑），请在「无障碍」中启用 MidnightBeam",
      "source_location": "dev.midnightbeam.MainActivity.onCreate 硬编码 t(en,it)",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "For full darkness",
      "text_zh": "为了全黑",
      "source_location": "assets/app.html L540 popA11yTitle",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "On this Android version the filter stops at 80% darkness and does not cover the navigation bar unless MidnightBeam is enabled in Accessibility. It is optional and it reads nothing on the screen.",
      "text_zh": "在此 Android 版本上，除非在无障碍中启用 MidnightBeam，调光最高只能到 80% 且不会覆盖导航栏。该项为可选，且不会读取屏幕上的任何内容。",
      "source_location": "assets/app.html L540 popA11yText",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Without it, Android 12 and later cap the filter at 80% darkness and leave the navigation bar uncovered. In Accessibility, open MidnightBeam (it may be under Installed apps or Downloaded apps) and turn it on. It reads nothing on the screen.",
      "text_zh": "若不启用，Android 12 及以后调光被限制在 80% 且导航栏不被覆盖。请到无障碍中打开 MidnightBeam（可能位于「已安装的应用」或「已下载的应用」下）并开启。它不会读取屏幕内容。",
      "source_location": "assets/app.html L534 stA11yText",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Android 12+ limits overlays to 80% darkness. For full darkness and to cover the system bars, enable MidnightBeam in Accessibility (optional, it reads nothing).",
      "text_zh": "Android 12+ 将悬浮窗限制在 80% 暗度。要实现全黑并覆盖系统栏，请在无障碍中启用 MidnightBeam（可选，它不读取任何内容）。",
      "source_location": "assets/app.html L530 a11yText",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "it",
      "text_verbatim": "Per il buio totale",
      "text_zh": "为了全黑",
      "source_location": "assets/app.html L597 popA11yTitle（意大利语本地化）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环：返回应用后仅 onResume 与一次 1500ms 延迟检查刷新按钮/提示可见性，不重跳设置；WebView 侧一次性提示由 store('mb_a11y_tip') 标记后不再弹出，并提供 Later 关闭",
    "overlay_or_fake_settings": "无。不叠放半透明引导遮罩或全屏悬浮窗，不伪造系统无障碍开关页；悬浮窗仅用于调光遮罩本身",
    "restricted_settings_13plus_coaching": "无。未跳转 ACTION_APPLICATION_DETAILS_SETTINGS，未出现「右上角菜单允许受限设置」类教学，亦未使用 Session 安装器绕过",
    "post_grant_anti_removal": "无。onServiceConnected 仅置 instance 并刷新 DimService；performGlobalAction(8) 出现在 DimService.powerAction 用于定时休眠/关机的返回动作，不用于阻止撤权；未监听设置页回退",
    "benign_graceful_degradation": "有。无障碍为可选增强（recommended）：不开启时仍以 SYSTEM_ALERT_WINDOW 悬浮窗调光，仅受 Android 12+ 80% 暗度与系统栏不可覆盖限制；另提供手机远程控制（PhoneActivity/本地 HTTP 8765）与 root/本地 ADB 关机等替代路径，setup 页 su-done 仅在 overlay 授予后启用"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS（由 Compat.enableOrOpenAccessibility 发起）时立即拉起；其次在 PhoneActivity WebView 首次加载 home 视图触发 permissionPopup 一次性弹层时拉起",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动一次性引导弹层页（手机端）",
        "page_identifier": "PhoneActivity 内本地 WebView，标题文本 'For full darkness'，含 Enable / Later 两个按钮",
        "why_most_useful": "区分该应用是否以「全黑/覆盖系统栏」功能性理由提出可选请求，还是以恐吓/假更新/假安全为诱饵",
        "observable_utg_signals": ["标题与正文字面文本（For full darkness / It is optional）", "是否同时存在 Later 取消按钮", "是否出现假更新、病毒、故障等恐吓关键词"]
      },
      {
        "page_role": "setup 教学页（步骤卡片）",
        "page_identifier": "WebView setup 视图：第 1 步 'Display over other apps' 标 Required，第 2 步 'Accessibility (full darkness)' 标 Recommended",
        "why_most_useful": "判断无障碍被呈现为可选增强还是强制前置，以及是否含受限设置分步教学",
        "observable_utg_signals": ["required / recommended 标签分布", "第 2 步按钮是否存在跳过路径", "是否出现「应用详情 → 右上角菜单 → 允许受限设置」类文字"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置无障碍页中 'MidnightBeam' 条目及其 description 展开文本",
        "why_most_useful": "核验系统侧呈现的服务名与说明是否与代码内承诺一致、有无同形字/空白伪装",
        "observable_utg_signals": ["服务显示名是否等于应用名 MidnightBeam", "description 是否含 'does not read the screen' 承诺", "有无异常长空白或不可见字符"]
      },
      {
        "page_role": "跳设置后叠层核验页",
        "page_identifier": "系统无障碍页上层是否出现任何自绘悬浮窗/遮罩",
        "why_most_useful": "排除「遮罩叠压系统设置页引导点击」这一典型诱导手法",
        "observable_utg_signals": ["无障碍页面上是否存在非系统 overlay 节点", "是否出现高仿开关控件", "页面是否被半透明层覆盖"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导文案为可提取文本，未使用纯图/空文本诱饵；无加壳、无二阶段 Dropper、无远端 HTML 下发（app.html 为包内本地资源）。仅 DimService 本地 HTTP 服务与 WebView AppApi 桥接的完整接口面未逐行审计，若需评估数据外发应另行覆盖。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "dev.midnightbeam.Compat.enableOrOpenAccessibility",
    "dev.midnightbeam.Compat.accessibilitySettings",
    "dev.midnightbeam.PhoneActivity.appAction",
    "dev.midnightbeam.MainActivity.onCreate",
    "assets/app.html permissionPopup() L1350-L1364",
    "res/xml/accessibility_service.xml"
  ]
}
```

</details>
