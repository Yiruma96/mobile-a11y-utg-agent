# MR_103__920f18c5ff｜donot — Google Play Services

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：133.9s

## 1. 一句话核心结论

- **核心申请方式**：无任何应用内引导流程：冷启动 MainActivity 只静默拉起后台 Service 并立即隐藏桌面图标，无障碍服务伪装成『Google Play Services』被动等待被外部开启后静默记录用户输入文本。
- **静态可见性说明**：classes.dex 未加壳未加密，全部逻辑静态可读；但『引导开启无障碍』这一段在本模块中根本不存在实现——既无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无本地或远端 HTML 引导页、无悬浮窗遮罩、无拒权循环。权限开启被完全外置到应用之外（社工/落地页/后续阶段），故运行期 UTG 在本样本内无可捕获页面。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `920f18c5ffb59856deccf2d984ab07793fefeea9a5a45d1e8a94a57da9d2347c` |
| 包名 / 年份 | `com.system.android.updateleica` / 2018 |
| 家族 / 品类 | **donot**（同池样本数：18） |
| 原始来源标识 | https://ti.360.net/blog/articles/analysis-of-donot-andriod-sample/ |
| 桌面显示名 | Google Play Services |
| 引导页宣称品牌/身份 | Google Play Services（Google 官方系统组件） |
| 系统无障碍列表服务名 | Google Play Services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务的 android:label 与 android:description 均直接复用 @string/app_name（'Google Play Services'），不含任何真实功能说明，借系统级品牌名降低用户与审核警觉；另有隐藏图标手法：onPause/onBackPressed/onDestroy 调用 setComponentEnabledSetting(component, COMPONENT_ENABLED_STATE_DISABLED=2, DONT_KILL_APP=1) 并广播 com.android.launcher.action.UNINSTALL_SHORTCUT（shortcut 名 'ServiceUpdate'） |
| 无障碍服务类名 | `com.system.android.updateleica.nine.ninere` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Google Play Services |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.system.android.updateleica.MainActivity（无布局、无 setContentView） | onCreate(Bundle) | 不可静态还原 | 无 | 无请求，用户看不到任何说明或按钮 | `com.system.android.updateleica.MainActivity.onCreate` |
| 2 | 获权后动作 | 后台服务 com.system.android.updateleica.ten.ten | MainActivity.onCreate 中 startService(new Intent(this, ten.class)) | 不可静态还原 | 无 | 无 | `com.system.android.updateleica.ten.ten.onStartCommand` |
| 3 | 遮罩叠层指引 | 系统无障碍列表中的服务项 com.system.android.updateleica.nine.ninere | 系统读取 res/xml/accessibility.xml 元数据（description=@string/app_name） | 系统无障碍页 | **原文**：Google Play Services<br>**译注**：Google Play Services（服务名与说明均为该品牌名，无功能描述） | 由用户在系统设置中自行开启，应用内无任何引导、无跳过/取消控件（本步不涉及应用 UI） | `res/xml/accessibility.xml；res/values/strings.xml#app_name` |
| 4 | 跳无障碍设置 | 无（未实现） | 无 | 不可静态还原 | 无 | 无 | `com.system.android.updateleica.nine.nine.isAccessibilitySettingsOn（仅读取 Settings.Secure，无跳转，且无调用点）` |
| 5 | 获权后动作 | AccessibilityService ninere 事件回调 | onAccessibilityEvent(TYPE_VIEW_TEXT_CHANGED=16) 且开关 ten.fg.klog.wm 为真 | 不可静态还原 | **原文**：Nine Text / keyoff / ***ACCESSIBILITY IS ENABLED*** -----------------<br>**译注**：仅 logcat 日志（Nine Text、keyoff 等），无用户可见 UI；把捕获的输入文本按时间累积并启动 keyclass 线程外传 | 无 | `com.system.android.updateleica.nine.ninere.onAccessibilityEvent` |
| 6 | 冷启动入口 | MainActivity.removeShortcut() | onPause / onBackPressed / onDestroy | 不可静态还原 | **原文**：ServiceUpdate<br>**译注**：隐藏桌面图标并卸载名为 'ServiceUpdate' 的快捷方式，用户返回或退出即隐身 | 无 | `com.system.android.updateleica.MainActivity.removeShortcut` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务名与说明文字均为 android:label/@string/app_name 与 android:description/@string/app_name → 'Google Play Services'（res/xml/accessibility.xml + res/values/strings.xml）
- 桌面启动器图标名称：android:label=@string/app_name → 'Google Play Services'（AndroidManifest.xml）
- 应用内无任何引导文本：MainActivity 无 setContentView、无 Dialog、无 WebView loadUrl，assets 目录为空（解包目录仅 classes.dex / res / original）
- 仅存在于 logcat 的内部日志：'***ACCESSIBILITY IS ENABLED*** -----------------'、'-------------- > accessibilityService :: '、'***ACCESSIBILITY IS DISABLED***'、'Nine Text'、'keyoff'（nine.isAccessibilitySettingsOn / ninere.onAccessibilityEvent）
- 快捷方式卸载广播中的名称常量 'ServiceUpdate'（MainActivity.removeShortcut）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Play Services | Google Play 服务 | `res/values/strings.xml → app_name（同时用作无障碍服务 label 与 description）` | 假更新 |
| en | ServiceUpdate | 服务更新 | `com.system.android.updateleica.MainActivity.removeShortcut（硬编码，作为快捷方式名用于 UNINSTALL_SHORTCUT 广播）` | 假更新 |
| en | ***ACCESSIBILITY IS ENABLED*** ----------------- | ***无障碍已启用*** ----------------- | `com.system.android.updateleica.nine.nine.isAccessibilitySettingsOn（Log.d 硬编码）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无。代码中不存在 onResume 重跳、Timer 拉起或 startActivity 到设置页的任何实现；用户从未被应用请求过权限，故也无『拒绝后反应』逻辑
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 悬浮窗，无高仿无障碍开关页，无遮罩指引
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无 GLOBAL_ACTION_BACK/HOME 阻挠撤权；但有应用级反移除：onPause/onBackPressed/onDestroy 时禁用自身启动组件并广播卸载快捷方式以隐藏图标，使用户难以再次找到入口去关闭服务
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本无应用内跳转点可挂。可行的 UTG 钩子是：①在系统设置 Accessibility 页面停留期间监测『已启用服务』列表出现 'Google Play Services' 且包名为 com.system.android.updateleica；②冷启动后立即抓取 launcher 桌面与最近任务，观察图标在数秒内消失（component disabled）以确认隐身行为；③Hook Settings.Secure 读取 enabled_accessibility_services 的调用方包名
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：本样本『权限开启』环节完全外置——应用内无跳转、无引导页、无 HTML，纯 UTG 若只观察应用自身界面会判为『无诱导』而漏判。必须以系统无障碍列表条目文本 + 图标消失现象 + 无障碍事件接收者包名作为补充信号；此外无障碍采集由 ten.fg.klog.wm 开关控制，若该开关默认关闭，获权后也可能长时间无可见行为，需动态改配置或等待 C2 指令。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（伪装身份关键证据）** | 设置→无障碍→已下载/已启用服务中出现名称为 'Google Play Services'、无功能描述的条目 | 该条目是本样本唯一的『对外话术载体』，服务名与说明均为品牌伪装且无真实功能描述，是判定身份冒充的直接运行期证据 | 文本 'Google Play Services' 与包名 com.system.android.updateleica 不一致；无障碍服务条目无任何功能说明文本；开关状态与 Settings.Secure.enabled_accessibility_services 值 |
| **冷启动后桌面图标消失（反移除/隐身证据）** | 启动 com.system.android.updateleica 后返回桌面，'Google Play Services' 图标消失、快捷方式 'ServiceUpdate' 被移除 | 证明应用在 onPause 即自禁用组件隐藏入口，与『无引导却要长期驻留采集』的行为模式吻合 | launcher 组件列表中该包 activity 变为 disabled；返回键后桌面图标缺失；最近任务中无可识别界面 |
| **后台输入采集（获权后行为）** | 在任意输入框（短信、搜索、聊天）输入文本时的无障碍事件流 | 验证无障碍服务的真实用途是键盘记录而非辅助功能 | TYPE_VIEW_TEXT_CHANGED 事件被 com.system.android.updateleica 接收；logcat 出现 'Nine Text' 与 'keyoff' 标签；随后的网络外发连接 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.system.android.updateleica.MainActivity.onCreate`
- `com.system.android.updateleica.MainActivity.removeShortcut`
- `com.system.android.updateleica.nine.nine.isAccessibilitySettingsOn`
- `com.system.android.updateleica.nine.ninere.onAccessibilityEvent`
- `res/xml/accessibility.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**核心发现：本样本 DEX 内不存在任何“引导用户开启无障碍”的界面流程。**

- 冷启动入口 [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.system.android.updateleica.MainActivity#onCreate>) 方法体只有一件事：`startService(new Intent(this, ten.class))`；**没有 `setContentView`、没有弹窗、没有 WebView 加载**。虽然类中声明了 `WebView wev`、`TextView loadingt` 和 `CustomWebViewClient`，但 onCreate 里从未 inflate 或 loadUrl。
- 在整份 DEX 字符串表中检索 `android.settings`、`ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`com.android.settings` 均**无命中**（唯一的 URL 是 `https://www.geoip-db.com/json`）。也就是说，本模块不会跳转系统设置页，也没有“分步教学”“遮罩指引”“拒权死循环”等实现。
- 唯一与无障碍相关的“状态检查”代码 [nine.isAccessibilitySettingsOn()](<resource-unit:#1.dex1 code:com.system.android.updateleica.nine.nine#isAccessibilitySettingsOn>) 只读取 `Settings.Secure.accessibility_enabled` 和 `enabled_accessibility_services`，并比较 `包名/ninere`；它**不跳转设置页**，而且 `search_function_callsites` 显示**没有任何调用点**，所以它是未接线的遗留代码。
- 真实的无障碍用途是**在后台静默监听按键文本**：[ninere.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.system.android.updateleica.nine.ninere#onAccessibilityEvent>) 在 `eventType==16`（TYPE_VIEW_TEXT_CHANGED）时，把 `event.getText()` 累积进 `ninelo` 并启动 `keyclass` 线程，同时用 `ten.fg.klog.wm` 开关控制是否执行；配套配置 [res/xml/accessibility.xml](<resource-unit:#1 file:res/xml/accessibility.xml>) 设置了 `canRetrieveWindowContent="true"`，并包含 `typeViewClicked|typeViewFocused|typeViewTextChanged|typeWindowStateChanged`，`notificationTimeout=100`，这是典型的键盘记录/输入采集配置。
- 身份伪装明确：桌面名与服务标签、无障碍说明三处统一为 `Google Play Services`（[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L19>)），无障碍说明直接复用 `@string/app_name`，没有任何功能描述。
- 应用隐藏动作：[MainActivity.removeShortcut()](<resource-unit:#1.dex1 code:com.system.android.updateleica.MainActivity#removeShortcut>) 在 `onPause`/`onBackPressed`/`onDestroy` 中调用 `setComponentEnabledSetting(..., 2, 1)` 禁用启动组件，并广播 `UNINSTALL_SHORTCUT`（名称 `ServiceUpdate`），属于安装后立即隐身的反移除设计。

**因此，对于“纯运行期 UTG 页面流转”这一提问：静态上不存在可捕获的引导链。** 无障碍权限必须由外部（攻击者社工话术、投递侧落地页、后续阶段模块）在应用之外完成开启，本 DEX 只做“已获权后的静默采集”。

```json
{
  "static_visibility": "clear",
  "visibility_note": "classes.dex 未加壳未加密，全部逻辑静态可读；但『引导开启无障碍』这一段在本模块中根本不存在实现——既无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无本地或远端 HTML 引导页、无悬浮窗遮罩、无拒权循环。权限开启被完全外置到应用之外（社工/落地页/后续阶段），故运行期 UTG 在本样本内无可捕获页面。",
  "summary_one_liner": "无任何应用内引导流程：冷启动 MainActivity 只静默拉起后台 Service 并立即隐藏桌面图标，无障碍服务伪装成『Google Play Services』被动等待被外部开启后静默记录用户输入文本。",
  "disguise_identity": {
    "app_display_name": "Google Play Services",
    "claimed_brand_or_persona": "Google Play Services（Google 官方系统组件）",
    "a11y_service_label": "Google Play Services",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务的 android:label 与 android:description 均直接复用 @string/app_name（'Google Play Services'），不含任何真实功能说明，借系统级品牌名降低用户与审核警觉；另有隐藏图标手法：onPause/onBackPressed/onDestroy 调用 setComponentEnabledSetting(component, COMPONENT_ENABLED_STATE_DISABLED=2, DONT_KILL_APP=1) 并广播 com.android.launcher.action.UNINSTALL_SHORTCUT（shortcut 名 'ServiceUpdate'）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.system.android.updateleica.MainActivity（无布局、无 setContentView）",
      "trigger_event": "onCreate(Bundle)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面内容，Activity 不加载任何布局",
      "user_action_requested": "无请求，用户看不到任何说明或按钮",
      "code_anchor": "com.system.android.updateleica.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "获权后动作",
      "screen_or_component": "后台服务 com.system.android.updateleica.ten.ten",
      "trigger_event": "MainActivity.onCreate 中 startService(new Intent(this, ten.class))",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；服务初始化数据库、SharedPreferences、闹钟与 One/two/three/four/five/six/nine/eleven/thirteen/zero 等采集模块",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.updateleica.ten.ten.onStartCommand"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍列表中的服务项 com.system.android.updateleica.nine.ninere",
      "trigger_event": "系统读取 res/xml/accessibility.xml 元数据（description=@string/app_name）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Play Services",
      "shown_text_zh": "Google Play Services（服务名与说明均为该品牌名，无功能描述）",
      "user_action_requested": "由用户在系统设置中自行开启，应用内无任何引导、无跳过/取消控件（本步不涉及应用 UI）",
      "code_anchor": "res/xml/accessibility.xml；res/values/strings.xml#app_name"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "无（未实现）",
      "trigger_event": "无",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "DEX 字符串表中不存在 android.settings.ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 等跳转目标，无任何 startActivity 引导实现",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.updateleica.nine.nine.isAccessibilitySettingsOn（仅读取 Settings.Secure，无跳转，且无调用点）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityService ninere 事件回调",
      "trigger_event": "onAccessibilityEvent(TYPE_VIEW_TEXT_CHANGED=16) 且开关 ten.fg.klog.wm 为真",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Nine Text / keyoff / ***ACCESSIBILITY IS ENABLED*** -----------------",
      "shown_text_zh": "仅 logcat 日志（Nine Text、keyoff 等），无用户可见 UI；把捕获的输入文本按时间累积并启动 keyclass 线程外传",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.updateleica.nine.ninere.onAccessibilityEvent"
    },
    {
      "step": 6,
      "stage": "冷启动入口",
      "screen_or_component": "MainActivity.removeShortcut()",
      "trigger_event": "onPause / onBackPressed / onDestroy",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "ServiceUpdate",
      "shown_text_zh": "隐藏桌面图标并卸载名为 'ServiceUpdate' 的快捷方式，用户返回或退出即隐身",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.updateleica.MainActivity.removeShortcut"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务名与说明文字均为 android:label/@string/app_name 与 android:description/@string/app_name → 'Google Play Services'（res/xml/accessibility.xml + res/values/strings.xml）",
    "桌面启动器图标名称：android:label=@string/app_name → 'Google Play Services'（AndroidManifest.xml）",
    "应用内无任何引导文本：MainActivity 无 setContentView、无 Dialog、无 WebView loadUrl，assets 目录为空（解包目录仅 classes.dex / res / original）",
    "仅存在于 logcat 的内部日志：'***ACCESSIBILITY IS ENABLED*** -----------------'、'-------------- > accessibilityService :: '、'***ACCESSIBILITY IS DISABLED***'、'Nine Text'、'keyoff'（nine.isAccessibilitySettingsOn / ninere.onAccessibilityEvent）",
    "快捷方式卸载广播中的名称常量 'ServiceUpdate'（MainActivity.removeShortcut）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Play Services",
      "text_zh": "Google Play 服务",
      "source_location": "res/values/strings.xml → app_name（同时用作无障碍服务 label 与 description）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "ServiceUpdate",
      "text_zh": "服务更新",
      "source_location": "com.system.android.updateleica.MainActivity.removeShortcut（硬编码，作为快捷方式名用于 UNINSTALL_SHORTCUT 广播）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "***ACCESSIBILITY IS ENABLED*** -----------------",
      "text_zh": "***无障碍已启用*** -----------------",
      "source_location": "com.system.android.updateleica.nine.nine.isAccessibilitySettingsOn（Log.d 硬编码）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无。代码中不存在 onResume 重跳、Timer 拉起或 startActivity 到设置页的任何实现；用户从未被应用请求过权限，故也无『拒绝后反应』逻辑",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 悬浮窗，无高仿无障碍开关页，无遮罩指引",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无 GLOBAL_ACTION_BACK/HOME 阻挠撤权；但有应用级反移除：onPause/onBackPressed/onDestroy 时禁用自身启动组件并广播卸载快捷方式以隐藏图标，使用户难以再次找到入口去关闭服务",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本无应用内跳转点可挂。可行的 UTG 钩子是：①在系统设置 Accessibility 页面停留期间监测『已启用服务』列表出现 'Google Play Services' 且包名为 com.system.android.updateleica；②冷启动后立即抓取 launcher 桌面与最近任务，观察图标在数秒内消失（component disabled）以确认隐身行为；③Hook Settings.Secure 读取 enabled_accessibility_services 的调用方包名",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（伪装身份关键证据）",
        "page_identifier": "设置→无障碍→已下载/已启用服务中出现名称为 'Google Play Services'、无功能描述的条目",
        "why_most_useful": "该条目是本样本唯一的『对外话术载体』，服务名与说明均为品牌伪装且无真实功能描述，是判定身份冒充的直接运行期证据",
        "observable_utg_signals": ["文本 'Google Play Services' 与包名 com.system.android.updateleica 不一致", "无障碍服务条目无任何功能说明文本", "开关状态与 Settings.Secure.enabled_accessibility_services 值"]
      },
      {
        "page_role": "冷启动后桌面图标消失（反移除/隐身证据）",
        "page_identifier": "启动 com.system.android.updateleica 后返回桌面，'Google Play Services' 图标消失、快捷方式 'ServiceUpdate' 被移除",
        "why_most_useful": "证明应用在 onPause 即自禁用组件隐藏入口，与『无引导却要长期驻留采集』的行为模式吻合",
        "observable_utg_signals": ["launcher 组件列表中该包 activity 变为 disabled", "返回键后桌面图标缺失", "最近任务中无可识别界面"]
      },
      {
        "page_role": "后台输入采集（获权后行为）",
        "page_identifier": "在任意输入框（短信、搜索、聊天）输入文本时的无障碍事件流",
        "why_most_useful": "验证无障碍服务的真实用途是键盘记录而非辅助功能",
        "observable_utg_signals": ["TYPE_VIEW_TEXT_CHANGED 事件被 com.system.android.updateleica 接收", "logcat 出现 'Nine Text' 与 'keyoff' 标签", "随后的网络外发连接"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：本样本『权限开启』环节完全外置——应用内无跳转、无引导页、无 HTML，纯 UTG 若只观察应用自身界面会判为『无诱导』而漏判。必须以系统无障碍列表条目文本 + 图标消失现象 + 无障碍事件接收者包名作为补充信号；此外无障碍采集由 ten.fg.klog.wm 开关控制，若该开关默认关闭，获权后也可能长时间无可见行为，需动态改配置或等待 C2 指令。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "TRIG_COLD_START_BLOCK"
  ],
  "code_anchors": [
    "com.system.android.updateleica.MainActivity.onCreate",
    "com.system.android.updateleica.MainActivity.removeShortcut",
    "com.system.android.updateleica.nine.nine.isAccessibilitySettingsOn",
    "com.system.android.updateleica.nine.ninere.onAccessibilityEvent",
    "res/xml/accessibility.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
