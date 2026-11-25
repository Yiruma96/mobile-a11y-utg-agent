# MB_036__27e0ec79db｜BRATA — 1. Módulo de Seguridad Bancaria

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：150.0s

## 1. 一句话核心结论

- **核心申请方式**：以“银行安全模块”名义用本地西语引导页+Proceder 按钮和明文路径指引，把用户送去系统无障碍列表手动勾选具备读屏与手势能力的 .websockservice，系统说明伪称“保护设备安全”。
- **静态可见性说明**：引导界面、无障碍服务配置、系统列表描述与权限清单均在包内明文静态可见（assets/*.bal 为未加密的 B4A 布局资源，res/xml 与 strings.xml 可读）；但全部业务 DEX 被 Beingyi 加固（com.beingyi.encrypt.StringPool、PmsHookApplication、np.manager.signature 签名校验桩），字符串池与 unknown/src/2e15f58d32a5ff652706ef41ec85a763（约3.9MB密文）均加密，Proceder 按钮点击后的 Intent 构造、ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 跳转代码及拒权后重跳逻辑不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `27e0ec79dbb7c7f99b43c8c01a94188d1071d1245b1745d0e066ae774c78a8f8` |
| 包名 / 年份 | `com.xd.craft.school` / 2022 |
| 家族 / 品类 | **BRATA**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | 1. Módulo de Seguridad Bancaria |
| 引导页宣称品牌/身份 | 虚构的“银行安全模块 / Módulo de Seguridad Bancaria”（未指明任何真实银行，但用银行安全语义伪装） |
| 系统无障碍列表服务名 | Módulo de Seguridad Bancaria |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 显示名前置序号“1. ”营造系统模块/官方下发的观感；2) 系统无障碍列表说明写为“Our app use this service for make your device safety”，与实际的读屏+手势+窗口ID上报能力不符；3) 应用名为 com.xd.craft.school（游戏/校园类包名）与“银行安全”身份不符；4) 全量 DEX 使用 Beingyi 加固并带签名校验桩 PmsHookApplication；5) 服务 exported=true 并配置 BOOT_COMPLETED 接收器常驻。 |
| 无障碍服务类名 | `.websockservice` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Our app use this service for make your device safety |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.xd.craft.school.main（LAUNCHER Activity，label=1. Módulo de Seguridad Bancaria） | 用户点击桌面图标启动，Activity.onCreate 触发权限/引导判定 | 原生Activity | **原文**：无（入口页文案位于加密 DEX 字符串池，不可静态还原）<br>**译注**：入口页内容不可静态还原，推测为权限引导入口 | 启动应用，继续进入授权流程 | `AndroidManifest.xml application/activity .main；跳转实现位于加密 DEX` |
| 2 | 引导说明页 | B4A 布局 Activity（assets/a11y_eng.bal，对应 Manifest 中 .permission_activity_a11y 或同类引导 Activity） | 冷启动/权限检查未通过后加载 a11y_eng 布局 | 原生Activity | **原文**：Nuestra App requiere tu autorización operativa para mantenerla completamente segura.<br><br>Haga clic en el botón "Proceder" a continuación para autorizar que nuestro sistema de seguridad funcione en su dispositivo.<br><br>Más descargas -> Accesibilidad -> Módulo de Seguridad Bancaria<br>**译注**：我们的应用需要您授予运行授权，以保持其完全安全。请点击下方“继续(Proceder)”按钮，授权我们的安全系统在您的设备上运行。更多/设置 → 无障碍 → 银行安全模块。 | 点击唯一按钮 Proceder；布局中仅有一个按钮与品牌图，未见取消/跳过控件 | `assets/a11y_eng.bal（Label1 说明文字、Panel1、Label2="Proceder"、ImageView1=brand-white.png）` |
| 3 | 跳无障碍设置 | 系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS（无障碍服务列表，含项“Módulo de Seguridad Bancaria”） | Proceder 点击后 startActivity 跳转（Intent 构造代码在加密 DEX 中） | 系统无障碍页 | **原文**：Our app use this service for make your device safety<br>**译注**：我们的应用使用此服务来保障您设备的安全 | 在系统列表中找到“Módulo de Seguridad Bancaria”并打开开关 | `res/xml/windowchangedetectingservice.xml → @string/accessibility_service_description（res/values/strings.xml:3）` |
| 4 | 遮罩叠层指引 | SYSTEM_ALERT_WINDOW 悬浮窗引导（对应 assets/manuale_over.bal“Please Enable Overlay Permission :)”与 assets/test_over.bal 多按钮覆盖页） | 无障碍未开启或悬浮窗权限缺失时由引导流程拉起 | 悬浮窗Overlay | **原文**：Please Enable Overlay Permission :)<br>**译注**：请启用悬浮窗权限 :) | 前往应用详情/悬浮窗设置授权，随后返回继续 | `assets/manuale_over.bal（Label1 文案 + Button1）；assets/test_over.bal（Button1/2/3 多路覆盖页）` |
| 5 | 获权后动作 | .websockservice（无障碍服务）配合 .fakepin_activity / assets/pin_geeet.bal 仿系统 PIN 页 | 服务 onAccessibilityEvent 收到目标银行/支付应用窗口事件后触发覆盖与注入 | 悬浮窗Overlay | **原文**：Android informa, digite seu PIN para continuar usando o aparelho<br>**译注**：Android 提示：请输入您的 PIN 码以继续使用该设备 | 在伪造的系统 PIN 输入框中输入银行密码/PIN | `assets/pin_geeet.bal（EditText1 + 文案）；AndroidManifest .fakepin_activity、.websockservice` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 本地原生引导 Activity 页面（B4A 布局 assets/a11y_eng.bal）：西语两段授权说明 + 路径指引 + 唯一按钮“Proceder”，含 brand-white.png 品牌图与 background-1.png 背景
- 系统无障碍服务列表项说明（android:description → res/values/strings.xml 的 accessibility_service_description）：“Our app use this service for make your device safety”
- 系统无障碍列表条目名称（service android:label / activity label）：“Módulo de Seguridad Bancaria”
- 桌面启动器图标名称：“1. Módulo de Seguridad Bancaria”
- 悬浮窗/覆盖引导页 assets/manuale_over.bal：“Please Enable Overlay Permission :)” + Button1
- 多按钮覆盖页 assets/test_over.bal（Button1/Button2/Button3，用于分步引导或拦截返回）
- 仿系统 PIN 采集页 assets/pin_geeet.bal + .fakepin_activity：“Android informa, digite seu PIN para continuar usando o aparelho”
- 次要权限申请页 assets/perm_eng.bal（title="Activity das Permissoes Secundarias"，text="Estamos Quase Finalizando... Aguarde O Resto!!!"）
- 内部测试/占位页 assets/drawer_eng.bal（title="drawer get perm"，text="DRAWEEEEER PEDE PERM"）
- 未使用本地 HTML/WebView：assets 下无 html 资源，引导不依赖远端网页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| es | Nuestra App requiere tu autorización operativa para mantenerla completamente segura. | 我们的应用需要您的运行授权，才能保持其完全安全。 | `assets/a11y_eng.bal（Label1.text，硬编码于 B4A 布局）` | 假反诈安全 |
| es | Haga clic en el botón "Proceder" a continuación para autorizar que nuestro sistema de seguridad funcione en su dispositivo. | 请点击下方的“继续(Proceder)”按钮，授权我们的安全系统在您的设备上运行。 | `assets/a11y_eng.bal（Label1.text）` | 假反诈安全 |
| es | Más descargas -> Accesibilidad -> Módulo de Seguridad Bancaria | 更多/设置 → 无障碍 → 银行安全模块 | `assets/a11y_eng.bal（Label1.text 末尾路径指引）` | 受限设置分步教学 |
| es | Proceder | 继续 / 前往 | `assets/a11y_eng.bal（Label2.text，唯一按钮文案）` | 假反诈安全 |
| en | Our app use this service for make your device safety | 我们的应用使用此服务来保障您设备的安全。 | `res/values/strings.xml:3（key=accessibility_service_description，经 windowchangedetectingservice.xml 引用）` | 假反诈安全 |
| en | Please Enable Overlay Permission :) | 请启用悬浮窗权限 :) | `assets/manuale_over.bal（Label1.text）` | 受限设置分步教学 |
| pt | Android informa, digite seu PIN para continuar usando o aparelho | Android 提示：请输入您的 PIN 码以继续使用该设备。 | `assets/pin_geeet.bal（EditText1 提示文案）+ AndroidManifest .fakepin_activity` | 教唆忽视警告 |
| pt | Estamos Quase Finalizando... Aguarde O Resto!!! | 我们快要完成了……请等待后续步骤！！！ | `assets/perm_eng.bal（title="Activity das Permissoes Secundarias"）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无法静态确认：a11y_eng 布局仅有一个 Proceder 按钮，无取消控件；拒绝返回后的重跳逻辑（onResume 重跳/定时器拉起）位于被 Beingyi 加密的 DEX 中，不可还原。旁证为 .websockservice 声明 exported=true 且配置 BOOT_COMPLETED 接收器（.websockservice$websockservice_BR），可在开机/外部意图下反复拉起服务侧流程。
- **遮罩叠层 / 高仿系统设置页**：存在悬浮窗引导与覆盖层：assets/manuale_over.bal（请启用悬浮窗权限）、assets/test_over.bal（Button1/2/3 多按钮覆盖页），配合 SYSTEM_ALERT_WINDOW 权限；未见高仿系统无障碍开关页（引导依赖真实系统无障碍列表）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=28，低于 Android 13，引导文案仅教用户进入“设置→无障碍”勾选服务，未涉及受限设置菜单或 Session 安装器绕过）。
- **获权后即时行为与防撤权机制**：无法静态确认；未见静态可证的自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码（服务配置已开启 canPerformGestures，具备该能力但具体使用逻辑在加密 DEX 中）。
- **良性降级 / 替代方案**：无（应用无任何真实安全功能或降级路径，引导页唯一出路是授权）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在应用冷启动（LAUNCHER Activity com.xd.craft.school.main 创建）后立即开始 UTG 抓取；并在系统 AccessibilityManagerService 被拉起（无障碍服务列表页出现）以及 SYSTEM_ALERT_WINDOW 添加时继续抓取。由于引导为 0 步冷启动直出，最优点是在进程启动瞬间起录。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：DEX 经 Beingyi 加固且字符串池加密（unknown/src/2e15f58d… 为密文载荷），Proceder 点击后的 Intent 构造、拒权重跳循环与无障碍事件处理逻辑不可静态还原，需运行期 UTG/日志补齐；引导页本身为纯文本布局，无纯图空文本诱导，故 UTG 文本提取即可覆盖核心判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（a11y_eng 布局）** | 含文本“Nuestra App requiere tu autorización operativa…”与“Proceder”按钮、brand-white.png 品牌图的原生 Activity | 这是诱导的唯一入口与全部说服话术所在，可直接判定是否存在“伪造安全身份+路径教学”的诱导 | 按钮文案 Proceder 且页面无取消/跳过控件；说明文字中出现 Accesibilidad / Módulo de Seguridad Bancaria 路径指引；页面元素仅 Label/ImageView/Button，无真实安全功能控件 |
| **跳转后的系统无障碍服务列表项** | Settings 无障碍页中服务条目名“Módulo de Seguridad Bancaria”及说明“Our app use this service for make your device safety” | 验证引导页与系统列表条目一一对应，且系统侧描述与实际能力（读屏/手势）不一致 | 无障碍设置页被拉起且本应用服务项可见；服务描述为“device safety”类表述；开关初始为关闭、需用户手动开启 |
| **悬浮窗引导/覆盖层页** | 含“Please Enable Overlay Permission :)”或 test_over 多按钮覆盖界面，窗口类型为 TYPE_APPLICATION_OVERLAY | 识别除无障碍外的第二层权限引导（悬浮窗），用于后续覆盖银行应用界面 | 系统级 overlay 窗口出现；文案含 Enable Overlay Permission；多按钮页面用于分步拦截 |
| **获权后仿系统 PIN 页** | Activity .fakepin_activity 或含“Android informa, digite seu PIN…”的 EditText 页面 | 确认获权后立即转向凭据窃取，闭合“诱导→滥用”的行为链 | 无系统标题栏/非 Settings 包名的 PIN 输入页；EditText 输入框 + 银行/Android 提示文案；页面出现于目标银行应用前台时 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `assets/a11y_eng.bal（Label1 说明文字 + Label2="Proceder" + ImageView1=brand-white.png）`
- `res/xml/windowchangedetectingservice.xml（canRetrieveWindowContent=true、canPerformGestures=true、flagReportViewIds）`
- `res/values/strings.xml:3（accessibility_service_description="Our app use this service for make your device safety"）`
- `AndroidManifest.xml .websockservice（exported=true，label=Módulo de Seguridad Bancaria，BOOT_COMPLETED 接收器）`
- `assets/pin_geeet.bal + AndroidManifest .fakepin_activity（仿系统 PIN 采集页）`
- `assets/manuale_over.bal / assets/test_over.bal（悬浮窗权限引导与覆盖页）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **诱导链完整且完全静态可见**：无障碍引导页是 B4A 布局资源 [assets/a11y_eng.bal](<resource-unit:#1 file:assets/a11y_eng.bal>)，其中包含品牌图 `brand-white.png`、西语“安全授权”说明文字和 `Proceder` 按钮，并给出 `Más descargas -> Accesibilidad -> Módulo de Seguridad Bancaria` 的明文路径指引，直接教用户进入系统无障碍列表并勾选本服务。全程不依赖远端 HTML 或云控下发。
- **身份与能力双重欺骗**：桌面名、Activity label、无障碍服务 label 统一为 `1. Módulo de Seguridad Bancaria`；系统列表说明取自 [strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3>) 的 `Our app use this service for make your device safety`。而 [windowchangedetectingservice.xml](<resource-unit:#1 file:res/xml/windowchangedetectingservice.xml>) 实际开启了 `canRetrieveWindowContent`、`canPerformGestures`、`flagReportViewIds`，事件覆盖点击、焦点和窗口内容变化，可读全屏内容并执行手势。
- **配套伪造与权限组合**：同包内 [assets/pin_geeet.bal](<resource-unit:#1 file:assets/pin_geeet.bal>) 提供仿系统 PIN 页（`Android informa, digite seu PIN para continuar usando o aparelho`），Manifest 申请 `READ_SMS`、`RECEIVE_SMS`、`SEND_SMS`、`SYSTEM_ALERT_WINDOW`、`CALL_PHONE`、`READ_CONTACTS`、`WRITE_SETTINGS`，与“安全模块”用途无关；`<queries>` 精确列出巴西及拉美银行包名（bradesco、santander、itau、mercadopago 等）。
- **静态可见性边界**：业务 DEX 被 Beingyi 壳加密（`com.beingyi.encrypt.StringPool`、`PmsHookApplication`，字符串池与 `unknown/src/2e15f58d...` 载荷均为密文），因此 `Proceder` 点击后的具体 Intent 构造、`ACTION_ACCESSIBILITY_SETTINGS` 跳转实现与拒绝后是否重跳（onResume 死循环）**无法静态还原**；引导界面与目标系统页由资源与 Manifest 明确可证。
- **服务暴露面**：`.websockservice` 声明 `exported=true`，可被外部意图拉起，冷启动并非唯一入口。

---

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "引导界面、无障碍服务配置、系统列表描述与权限清单均在包内明文静态可见（assets/*.bal 为未加密的 B4A 布局资源，res/xml 与 strings.xml 可读）；但全部业务 DEX 被 Beingyi 加固（com.beingyi.encrypt.StringPool、PmsHookApplication、np.manager.signature 签名校验桩），字符串池与 unknown/src/2e15f58d32a5ff652706ef41ec85a763（约3.9MB密文）均加密，Proceder 按钮点击后的 Intent 构造、ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 跳转代码及拒权后重跳逻辑不可静态还原。",
  "summary_one_liner": "以“银行安全模块”名义用本地西语引导页+Proceder 按钮和明文路径指引，把用户送去系统无障碍列表手动勾选具备读屏与手势能力的 .websockservice，系统说明伪称“保护设备安全”。",
  "disguise_identity": {
    "app_display_name": "1. Módulo de Seguridad Bancaria",
    "claimed_brand_or_persona": "虚构的“银行安全模块 / Módulo de Seguridad Bancaria”（未指明任何真实银行，但用银行安全语义伪装）",
    "a11y_service_label": "Módulo de Seguridad Bancaria",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 显示名前置序号“1. ”营造系统模块/官方下发的观感；2) 系统无障碍列表说明写为“Our app use this service for make your device safety”，与实际的读屏+手势+窗口ID上报能力不符；3) 应用名为 com.xd.craft.school（游戏/校园类包名）与“银行安全”身份不符；4) 全量 DEX 使用 Beingyi 加固并带签名校验桩 PmsHookApplication；5) 服务 exported=true 并配置 BOOT_COMPLETED 接收器常驻。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.xd.craft.school.main（LAUNCHER Activity，label=1. Módulo de Seguridad Bancaria）",
      "trigger_event": "用户点击桌面图标启动，Activity.onCreate 触发权限/引导判定",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（入口页文案位于加密 DEX 字符串池，不可静态还原）",
      "shown_text_zh": "入口页内容不可静态还原，推测为权限引导入口",
      "user_action_requested": "启动应用，继续进入授权流程",
      "code_anchor": "AndroidManifest.xml application/activity .main；跳转实现位于加密 DEX"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "B4A 布局 Activity（assets/a11y_eng.bal，对应 Manifest 中 .permission_activity_a11y 或同类引导 Activity）",
      "trigger_event": "冷启动/权限检查未通过后加载 a11y_eng 布局",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Nuestra App requiere tu autorización operativa para mantenerla completamente segura.\n\nHaga clic en el botón \"Proceder\" a continuación para autorizar que nuestro sistema de seguridad funcione en su dispositivo.\n\nMás descargas -> Accesibilidad -> Módulo de Seguridad Bancaria",
      "shown_text_zh": "我们的应用需要您授予运行授权，以保持其完全安全。请点击下方“继续(Proceder)”按钮，授权我们的安全系统在您的设备上运行。更多/设置 → 无障碍 → 银行安全模块。",
      "user_action_requested": "点击唯一按钮 Proceder；布局中仅有一个按钮与品牌图，未见取消/跳过控件",
      "code_anchor": "assets/a11y_eng.bal（Label1 说明文字、Panel1、Label2=\"Proceder\"、ImageView1=brand-white.png）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS（无障碍服务列表，含项“Módulo de Seguridad Bancaria”）",
      "trigger_event": "Proceder 点击后 startActivity 跳转（Intent 构造代码在加密 DEX 中）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Our app use this service for make your device safety",
      "shown_text_zh": "我们的应用使用此服务来保障您设备的安全",
      "user_action_requested": "在系统列表中找到“Módulo de Seguridad Bancaria”并打开开关",
      "code_anchor": "res/xml/windowchangedetectingservice.xml → @string/accessibility_service_description（res/values/strings.xml:3）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "SYSTEM_ALERT_WINDOW 悬浮窗引导（对应 assets/manuale_over.bal“Please Enable Overlay Permission :)”与 assets/test_over.bal 多按钮覆盖页）",
      "trigger_event": "无障碍未开启或悬浮窗权限缺失时由引导流程拉起",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Please Enable Overlay Permission :)",
      "shown_text_zh": "请启用悬浮窗权限 :)",
      "user_action_requested": "前往应用详情/悬浮窗设置授权，随后返回继续",
      "code_anchor": "assets/manuale_over.bal（Label1 文案 + Button1）；assets/test_over.bal（Button1/2/3 多路覆盖页）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": ".websockservice（无障碍服务）配合 .fakepin_activity / assets/pin_geeet.bal 仿系统 PIN 页",
      "trigger_event": "服务 onAccessibilityEvent 收到目标银行/支付应用窗口事件后触发覆盖与注入",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Android informa, digite seu PIN para continuar usando o aparelho",
      "shown_text_zh": "Android 提示：请输入您的 PIN 码以继续使用该设备",
      "user_action_requested": "在伪造的系统 PIN 输入框中输入银行密码/PIN",
      "code_anchor": "assets/pin_geeet.bal（EditText1 + 文案）；AndroidManifest .fakepin_activity、.websockservice"
    }
  ],
  "text_presentation_locations": [
    "本地原生引导 Activity 页面（B4A 布局 assets/a11y_eng.bal）：西语两段授权说明 + 路径指引 + 唯一按钮“Proceder”，含 brand-white.png 品牌图与 background-1.png 背景",
    "系统无障碍服务列表项说明（android:description → res/values/strings.xml 的 accessibility_service_description）：“Our app use this service for make your device safety”",
    "系统无障碍列表条目名称（service android:label / activity label）：“Módulo de Seguridad Bancaria”",
    "桌面启动器图标名称：“1. Módulo de Seguridad Bancaria”",
    "悬浮窗/覆盖引导页 assets/manuale_over.bal：“Please Enable Overlay Permission :)” + Button1",
    "多按钮覆盖页 assets/test_over.bal（Button1/Button2/Button3，用于分步引导或拦截返回）",
    "仿系统 PIN 采集页 assets/pin_geeet.bal + .fakepin_activity：“Android informa, digite seu PIN para continuar usando o aparelho”",
    "次要权限申请页 assets/perm_eng.bal（title=\"Activity das Permissoes Secundarias\"，text=\"Estamos Quase Finalizando... Aguarde O Resto!!!\"）",
    "内部测试/占位页 assets/drawer_eng.bal（title=\"drawer get perm\"，text=\"DRAWEEEEER PEDE PERM\"）",
    "未使用本地 HTML/WebView：assets 下无 html 资源，引导不依赖远端网页"
  ],
  "verbatim_texts": [
    {
      "lang": "es",
      "text_verbatim": "Nuestra App requiere tu autorización operativa para mantenerla completamente segura.",
      "text_zh": "我们的应用需要您的运行授权，才能保持其完全安全。",
      "source_location": "assets/a11y_eng.bal（Label1.text，硬编码于 B4A 布局）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "es",
      "text_verbatim": "Haga clic en el botón \"Proceder\" a continuación para autorizar que nuestro sistema de seguridad funcione en su dispositivo.",
      "text_zh": "请点击下方的“继续(Proceder)”按钮，授权我们的安全系统在您的设备上运行。",
      "source_location": "assets/a11y_eng.bal（Label1.text）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "es",
      "text_verbatim": "Más descargas -> Accesibilidad -> Módulo de Seguridad Bancaria",
      "text_zh": "更多/设置 → 无障碍 → 银行安全模块",
      "source_location": "assets/a11y_eng.bal（Label1.text 末尾路径指引）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "es",
      "text_verbatim": "Proceder",
      "text_zh": "继续 / 前往",
      "source_location": "assets/a11y_eng.bal（Label2.text，唯一按钮文案）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Our app use this service for make your device safety",
      "text_zh": "我们的应用使用此服务来保障您设备的安全。",
      "source_location": "res/values/strings.xml:3（key=accessibility_service_description，经 windowchangedetectingservice.xml 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Please Enable Overlay Permission :)",
      "text_zh": "请启用悬浮窗权限 :)",
      "source_location": "assets/manuale_over.bal（Label1.text）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "Android informa, digite seu PIN para continuar usando o aparelho",
      "text_zh": "Android 提示：请输入您的 PIN 码以继续使用该设备。",
      "source_location": "assets/pin_geeet.bal（EditText1 提示文案）+ AndroidManifest .fakepin_activity",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "pt",
      "text_verbatim": "Estamos Quase Finalizando... Aguarde O Resto!!!",
      "text_zh": "我们快要完成了……请等待后续步骤！！！",
      "source_location": "assets/perm_eng.bal（title=\"Activity das Permissoes Secundarias\"）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无法静态确认：a11y_eng 布局仅有一个 Proceder 按钮，无取消控件；拒绝返回后的重跳逻辑（onResume 重跳/定时器拉起）位于被 Beingyi 加密的 DEX 中，不可还原。旁证为 .websockservice 声明 exported=true 且配置 BOOT_COMPLETED 接收器（.websockservice$websockservice_BR），可在开机/外部意图下反复拉起服务侧流程。",
    "overlay_or_fake_settings": "存在悬浮窗引导与覆盖层：assets/manuale_over.bal（请启用悬浮窗权限）、assets/test_over.bal（Button1/2/3 多按钮覆盖页），配合 SYSTEM_ALERT_WINDOW 权限；未见高仿系统无障碍开关页（引导依赖真实系统无障碍列表）。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=28，低于 Android 13，引导文案仅教用户进入“设置→无障碍”勾选服务，未涉及受限设置菜单或 Session 安装器绕过）。",
    "post_grant_anti_removal": "无法静态确认；未见静态可证的自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码（服务配置已开启 canPerformGestures，具备该能力但具体使用逻辑在加密 DEX 中）。",
    "benign_graceful_degradation": "无（应用无任何真实安全功能或降级路径，引导页唯一出路是授权）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在应用冷启动（LAUNCHER Activity com.xd.craft.school.main 创建）后立即开始 UTG 抓取；并在系统 AccessibilityManagerService 被拉起（无障碍服务列表页出现）以及 SYSTEM_ALERT_WINDOW 添加时继续抓取。由于引导为 0 步冷启动直出，最优点是在进程启动瞬间起录。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（a11y_eng 布局）",
        "page_identifier": "含文本“Nuestra App requiere tu autorización operativa…”与“Proceder”按钮、brand-white.png 品牌图的原生 Activity",
        "why_most_useful": "这是诱导的唯一入口与全部说服话术所在，可直接判定是否存在“伪造安全身份+路径教学”的诱导",
        "observable_utg_signals": ["按钮文案 Proceder 且页面无取消/跳过控件", "说明文字中出现 Accesibilidad / Módulo de Seguridad Bancaria 路径指引", "页面元素仅 Label/ImageView/Button，无真实安全功能控件"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中服务条目名“Módulo de Seguridad Bancaria”及说明“Our app use this service for make your device safety”",
        "why_most_useful": "验证引导页与系统列表条目一一对应，且系统侧描述与实际能力（读屏/手势）不一致",
        "observable_utg_signals": ["无障碍设置页被拉起且本应用服务项可见", "服务描述为“device safety”类表述", "开关初始为关闭、需用户手动开启"]
      },
      {
        "page_role": "悬浮窗引导/覆盖层页",
        "page_identifier": "含“Please Enable Overlay Permission :)”或 test_over 多按钮覆盖界面，窗口类型为 TYPE_APPLICATION_OVERLAY",
        "why_most_useful": "识别除无障碍外的第二层权限引导（悬浮窗），用于后续覆盖银行应用界面",
        "observable_utg_signals": ["系统级 overlay 窗口出现", "文案含 Enable Overlay Permission", "多按钮页面用于分步拦截"]
      },
      {
        "page_role": "获权后仿系统 PIN 页",
        "page_identifier": "Activity .fakepin_activity 或含“Android informa, digite seu PIN…”的 EditText 页面",
        "why_most_useful": "确认获权后立即转向凭据窃取，闭合“诱导→滥用”的行为链",
        "observable_utg_signals": ["无系统标题栏/非 Settings 包名的 PIN 输入页", "EditText 输入框 + 银行/Android 提示文案", "页面出现于目标银行应用前台时"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：DEX 经 Beingyi 加固且字符串池加密（unknown/src/2e15f58d… 为密文载荷），Proceder 点击后的 Intent 构造、拒权重跳循环与无障碍事件处理逻辑不可静态还原，需运行期 UTG/日志补齐；引导页本身为纯文本布局，无纯图空文本诱导，故 UTG 文本提取即可覆盖核心判定。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "assets/a11y_eng.bal（Label1 说明文字 + Label2=\"Proceder\" + ImageView1=brand-white.png）",
    "res/xml/windowchangedetectingservice.xml（canRetrieveWindowContent=true、canPerformGestures=true、flagReportViewIds）",
    "res/values/strings.xml:3（accessibility_service_description=\"Our app use this service for make your device safety\"）",
    "AndroidManifest.xml .websockservice（exported=true，label=Módulo de Seguridad Bancaria，BOOT_COMPLETED 接收器）",
    "assets/pin_geeet.bal + AndroidManifest .fakepin_activity（仿系统 PIN 采集页）",
    "assets/manuale_over.bal / assets/test_over.bal（悬浮窗权限引导与覆盖页）"
  ]
}
```

</details>
