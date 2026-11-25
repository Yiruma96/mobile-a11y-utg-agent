# MR_086__9ef7031c21｜boogr — Sikh Net

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：79.2s

## 1. 一句话核心结论

- **核心申请方式**：无任何应用内引导或设置跳转，仅靠伪造系统/三星身份的包名与同名无障碍服务条目诱使用户在系统设置中手动开启，服务实为抓取全应用输入文本并加密外发的键盘记录器。
- **静态可见性说明**：无障碍服务的注册、事件处理与数据外发逻辑完整静态可见（DEX 未加壳、未加密，restricted 仅 RESTRICTED_STR）；但应用内不存在任何开启无障碍的引导 UI 或设置跳转代码，主界面为远端 HTTP 页面 http://www.thaidateclub.com/gallery0.htm 的 WebView 外壳，任何引导话术若存在均由该远端页面动态下发，包内 assets 无本地 HTML 教学页，故引导呈现部分不可静态还原。
- **命中的行为模式标签**：`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9ef7031c21675175d39c99e0afa32d9e1a99b53572ae014126bd8374ead4f708` |
| 包名 / 年份 | `com.system.android.sikhnet` / 2018 |
| 家族 / 品类 | **boogr**（同池样本数：2） |
| 原始来源标识 | https://ti.360.net/blog/articles/analysis-of-donot-andriod-sample/ |
| 桌面显示名 | Sikh Net |
| 引导页宣称品牌/身份 | 锡克教社区资讯类良性应用（Sikh Net），同时以包名 com.system.android.sikhnet 与内嵌 com.samsung.android.updater 资源包冒充 Android 系统组件与三星系统更新程序 |
| 系统无障碍列表服务名 | Sikh Net |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.system.android.sikhnet 使用 system 字样冒充系统级应用；DEX 内嵌完整 com.samsung.android.updater 包（BuildConfig/R/R$anim 等 16 个类）伪造三星系统更新组件；无障碍服务 android:label 与 android:description 均直接复用 @string/app_name，使系统无障碍列表中显示的条目与桌面图标名称完全一致，不暴露任何键盘记录/窗口内容读取能力说明；类名与包名高度模式化（nine/ninere、ten/ten$runto、one/onere、eight/eightre）以规避关键字检索。 |
| 无障碍服务类名 | `com.system.android.sikhnet.nine.ninere` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Sikh Net |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.system.android.sikhnet.MainActivity（布局 R$layout.activity_main，内含 R$id.webview） | LAUNCHER intent-filter 的 MAIN/LAUNCHER 启动，onCreate 执行 | 远端WebView | **原文**：http://www.thaidateclub.com/gallery0.htm<br>**译注**：加载泰国约会俱乐部（thaidateclub.com）的 gallery0.htm 页面；标题栏初始显示 "Loading..."，加载完成后改为 "Sikh Net" | 无明确要求；页面内容由远端决定，用户仅能看到远端渲染的 Web 内容（远端可能在此投放引导话术，包内不可见） | `com.system.android.sikhnet.MainActivity.onCreate / MainActivity$1.onProgressChanged` |
| 2 | 获权后动作 | com.system.android.sikhnet.ten（IntentService 常驻）+ com.system.android.sikhnet.nine.ninere（无障碍服务） | onCreate 内 startService(ten)，ten.onStartCommand 初始化各采集模块并启动 ten$runto 轮询线程；ninere.onServiceConnected 仅在用户于系统设置手动开启后回调 | 不可静态还原 | 无 | 无 | `com.system.android.sikhnet.ten.ten.onStartCommand / com.system.android.sikhnet.nine.ninere.onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统设置 → 无障碍 → 已安装服务列表：条目名称 "Sikh Net"（service android:label=@string/app_name）
- 系统设置无障碍条目的功能说明文字：同样为 "Sikh Net"（res/xml/accessibility.xml 的 android:description=@string/app_name），不含任何键盘记录/窗口内容读取说明
- 应用主界面：远端网页 http://www.thaidateclub.com/gallery0.htm 在 R$id.webview 中渲染，文案内容由远端决定，包内无本地副本
- 应用内不存在任何原生 Dialog、本地 HTML 教学页、悬浮窗遮罩或高仿设置页承载引导文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Sikh Net | 锡克网络 | `res/values/strings.xml: app_name；同时用于 service android:label 与 accessibility.xml android:description` | 未知 |
| en | Loading... | 加载中… | `com.system.android.sikhnet.MainActivity$1.onProgressChanged 硬编码` | 良性透明说明 |
| en | http://www.thaidateclub.com/gallery0.htm | 泰国约会俱乐部网站页面（远端内容，含引导话术可能性，静态不可见） | `com.system.android.sikhnet.MainActivity.onCreate 硬编码` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无。代码中不存在 onResume 重跳、Timer 拉起或后台反复跳转设置页的逻辑；用户不开启无障碍时服务只是不连接，应用无任何反馈或循环施压
- **遮罩叠层 / 高仿系统设置页**：无。无悬浮窗、无半透明引导遮罩、无高仿系统无障碍开关页（overlay 线索为空，且全包搜索无 Settings 跳转与 WindowManager TYPE_APPLICATION_OVERLAY 使用）
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：获权后不做自点确认或自授权；撤权防护改由 ten.onDestroy 的 AlarmManager 20 秒自重拉维持后台服务（属后台驻留而非无障碍防撤权）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本无应用内引导跳转，UTG 应在两处拉起：①冷启动 MainActivity 后立即抓取远端 WebView 首屏（http://www.thaidateclub.com/gallery0.htm），确认是否有远端下发的话术；②主动进入 系统设置 → 无障碍，抓取 "Sikh Net" 条目的系统列表页与确认弹窗原文
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区在于引导完全外置：包内无任何引导 UI，若远端页面用图片承载话术则需 OCR；此外包名伪造 system/三星更新组件，静态名单匹配容易被误判为系统组件；DEX 虽未加壳但核心外发链路经 AES-128（种子硬编码）加密，明文载荷需动态抓包或解密脚本才能还原。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动远端 WebView 外壳页（唯一可能承载引导话术的位置）** | com.system.android.sikhnet.MainActivity 内的 WebView 渲染 thaidateclub.com 页面，标题栏为 "Sikh Net" | 包内无本地引导资源，若存在诱导文案只能在此页；捕获即可判定是社工话术还是纯色情/约会引流外壳 | 页面是否出现"开启无障碍/辅助功能"等字样；是否有指向设置页的按钮或链接；页面语言与站点主题（约会/宗教）；加载后标题是否被改成 Sikh Net 掩盖 |
| **系统无障碍服务列表项与开启确认弹窗** | 设置 → 无障碍 → 已下载/已安装服务中的 "Sikh Net" 条目，以及点击后的系统警告弹窗 | 这是用户唯一获知该服务的入口，可验证 description 是否仅为应用名（无能力说明），从而证明依赖名称混淆而非功能说明 | 条目名称是否仅显示 "Sikh Net"；副标题/说明文字是否为空或等同应用名；系统警告中"查看和控制屏幕内容"等敏感能力提示 |
| **获权后行为佐证（无界面）** | 无 UI；可在任意输入框中键入文本后观察 ninere 是否抓取并触发外发线程 | 证明获权后动作是全局键盘记录而非无障碍辅助，可与代码证据交叉验证 | 切换应用后网络请求（加密载荷）是否出现；输入文本是否被拼接进 JSON 结构 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.system.android.sikhnet.MainActivity.onCreate`
- `com.system.android.sikhnet.nine.ninere.onAccessibilityEvent`
- `com.system.android.sikhnet.nine.ninere$keyclass.run`
- `com.system.android.sikhnet.ten.ten$runto.gkey`
- `res/xml/accessibility.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（在硬性预算内收口）。

## 结论要点

- **无障碍服务注册存在，但应用内无任何引导/跳转代码。** 在整个 DEX 中搜索 `android.settings.`、`ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`startActivity`、`AlertDialog` 均**无匹配**：应用没有 `ACTION_ACCESSIBILITY_SETTINGS` 跳转点、没有引导弹窗、没有悬浮遮罩、没有拒权重跳循环。用户唯一能看到"Sikh Net"入口的位置是**系统设置 → 无障碍服务列表**（`res/xml/accessibility.xml` 的 `android:description="@string/app_name"`，与桌面名完全一致，无任何功能说明）。
- **主入口是远端 WebView 外壳。** [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.system.android.sikhnet.MainActivity#onCreate>) 仅 `setContentView` 后 `loadUrl("http://www.thaidateclub.com/gallery0.htm")`，并拉起 [ten.onStartCommand()](<resource-unit:#1.dex1 code:com.system.android.sikhnet.ten.ten#onStartCommand>) 常驻服务。若存在"教你开启无障碍"的文案，只可能由该**远端 HTTP 页面**动态下发，静态包内不可见 → 可见性判为 `partial_dynamic_or_remote`。
- **无障碍服务的真实用途是键盘记录，而非无障碍辅助。** [ninere.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.system.android.sikhnet.nine.ninere#onAccessibilityEvent>) 在 `typeViewTextChanged`(16)/`typeWindowStateChanged`(8)/`typeViewFocused`(32) 上抓取 `getText()` 与包名，累积进 `ninelo` 并由 [ninere$keyclass.run()](<resource-unit:#1.dex1 code:com.system.android.sikhnet.nine.ninere$keyclass#run>) 线程外发；配置 `canRetrieveWindowContent="true"`。这是获权后动作的核心危害。
- **身份伪装双层面**：包名 `com.system.android.sikhnet`（伪造系统级命名）+ DEX 内嵌 `com.samsung.android.updater` 资源包（伪造三星系统更新组件）；显示名" Sikh Net "以宗教/社区名义作良性外壳。属典型 boogr 家族"伪系统组件 + 无障碍键盘记录"结构。
- **C2/加密证据**：`ten$runto.gkey()` 用硬编码种子 `"this is agdfhgdfh key"` 经 SHA1PRNG 派生 AES-128 密钥，配合 `ten$runto.run()` 中 `while(stopped) two()` 的轮询循环，构成加密回传通道；`ten.onDestroy()` 用 AlarmManager 20 秒自重拉防退出。
- **引导链定性**：该样本**没有**"一步步引导"的 UTG 可捕获页面流转；它依赖**用户自行在系统无障碍列表中开启**同名服务（社工靠外壳站点话术，非代码内引导）。这是判定时的重要负向事实。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍服务的注册、事件处理与数据外发逻辑完整静态可见（DEX 未加壳、未加密，restricted 仅 RESTRICTED_STR）；但应用内不存在任何开启无障碍的引导 UI 或设置跳转代码，主界面为远端 HTTP 页面 http://www.thaidateclub.com/gallery0.htm 的 WebView 外壳，任何引导话术若存在均由该远端页面动态下发，包内 assets 无本地 HTML 教学页，故引导呈现部分不可静态还原。",
  "summary_one_liner": "无任何应用内引导或设置跳转，仅靠伪造系统/三星身份的包名与同名无障碍服务条目诱使用户在系统设置中手动开启，服务实为抓取全应用输入文本并加密外发的键盘记录器。",
  "disguise_identity": {
    "app_display_name": "Sikh Net",
    "claimed_brand_or_persona": "锡克教社区资讯类良性应用（Sikh Net），同时以包名 com.system.android.sikhnet 与内嵌 com.samsung.android.updater 资源包冒充 Android 系统组件与三星系统更新程序",
    "a11y_service_label": "Sikh Net",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.system.android.sikhnet 使用 system 字样冒充系统级应用；DEX 内嵌完整 com.samsung.android.updater 包（BuildConfig/R/R$anim 等 16 个类）伪造三星系统更新组件；无障碍服务 android:label 与 android:description 均直接复用 @string/app_name，使系统无障碍列表中显示的条目与桌面图标名称完全一致，不暴露任何键盘记录/窗口内容读取能力说明；类名与包名高度模式化（nine/ninere、ten/ten$runto、one/onere、eight/eightre）以规避关键字检索。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.system.android.sikhnet.MainActivity（布局 R$layout.activity_main，内含 R$id.webview）",
      "trigger_event": "LAUNCHER intent-filter 的 MAIN/LAUNCHER 启动，onCreate 执行",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "http://www.thaidateclub.com/gallery0.htm",
      "shown_text_zh": "加载泰国约会俱乐部（thaidateclub.com）的 gallery0.htm 页面；标题栏初始显示 \"Loading...\"，加载完成后改为 \"Sikh Net\"",
      "user_action_requested": "无明确要求；页面内容由远端决定，用户仅能看到远端渲染的 Web 内容（远端可能在此投放引导话术，包内不可见）",
      "code_anchor": "com.system.android.sikhnet.MainActivity.onCreate / MainActivity$1.onProgressChanged"
    },
    {
      "step": 2,
      "stage": "获权后动作",
      "screen_or_component": "com.system.android.sikhnet.ten（IntentService 常驻）+ com.system.android.sikhnet.nine.ninere（无障碍服务）",
      "trigger_event": "onCreate 内 startService(ten)，ten.onStartCommand 初始化各采集模块并启动 ten$runto 轮询线程；ninere.onServiceConnected 仅在用户于系统设置手动开启后回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全程无界面；后台采集键盘输入并加密回传",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.sikhnet.ten.ten.onStartCommand / com.system.android.sikhnet.nine.ninere.onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "系统设置 → 无障碍 → 已安装服务列表：条目名称 \"Sikh Net\"（service android:label=@string/app_name）",
    "系统设置无障碍条目的功能说明文字：同样为 \"Sikh Net\"（res/xml/accessibility.xml 的 android:description=@string/app_name），不含任何键盘记录/窗口内容读取说明",
    "应用主界面：远端网页 http://www.thaidateclub.com/gallery0.htm 在 R$id.webview 中渲染，文案内容由远端决定，包内无本地副本",
    "应用内不存在任何原生 Dialog、本地 HTML 教学页、悬浮窗遮罩或高仿设置页承载引导文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Sikh Net",
      "text_zh": "锡克网络",
      "source_location": "res/values/strings.xml: app_name；同时用于 service android:label 与 accessibility.xml android:description",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Loading...",
      "text_zh": "加载中…",
      "source_location": "com.system.android.sikhnet.MainActivity$1.onProgressChanged 硬编码",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "http://www.thaidateclub.com/gallery0.htm",
      "text_zh": "泰国约会俱乐部网站页面（远端内容，含引导话术可能性，静态不可见）",
      "source_location": "com.system.android.sikhnet.MainActivity.onCreate 硬编码",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无。代码中不存在 onResume 重跳、Timer 拉起或后台反复跳转设置页的逻辑；用户不开启无障碍时服务只是不连接，应用无任何反馈或循环施压",
    "overlay_or_fake_settings": "无。无悬浮窗、无半透明引导遮罩、无高仿系统无障碍开关页（overlay 线索为空，且全包搜索无 Settings 跳转与 WindowManager TYPE_APPLICATION_OVERLAY 使用）",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "获权后不做自点确认或自授权；撤权防护改由 ten.onDestroy 的 AlarmManager 20 秒自重拉维持后台服务（属后台驻留而非无障碍防撤权）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本无应用内引导跳转，UTG 应在两处拉起：①冷启动 MainActivity 后立即抓取远端 WebView 首屏（http://www.thaidateclub.com/gallery0.htm），确认是否有远端下发的话术；②主动进入 系统设置 → 无障碍，抓取 \"Sikh Net\" 条目的系统列表页与确认弹窗原文",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动远端 WebView 外壳页（唯一可能承载引导话术的位置）",
        "page_identifier": "com.system.android.sikhnet.MainActivity 内的 WebView 渲染 thaidateclub.com 页面，标题栏为 \"Sikh Net\"",
        "why_most_useful": "包内无本地引导资源，若存在诱导文案只能在此页；捕获即可判定是社工话术还是纯色情/约会引流外壳",
        "observable_utg_signals": ["页面是否出现\"开启无障碍/辅助功能\"等字样", "是否有指向设置页的按钮或链接", "页面语言与站点主题（约会/宗教）", "加载后标题是否被改成 Sikh Net 掩盖"]
      },
      {
        "page_role": "系统无障碍服务列表项与开启确认弹窗",
        "page_identifier": "设置 → 无障碍 → 已下载/已安装服务中的 \"Sikh Net\" 条目，以及点击后的系统警告弹窗",
        "why_most_useful": "这是用户唯一获知该服务的入口，可验证 description 是否仅为应用名（无能力说明），从而证明依赖名称混淆而非功能说明",
        "observable_utg_signals": ["条目名称是否仅显示 \"Sikh Net\"", "副标题/说明文字是否为空或等同应用名", "系统警告中\"查看和控制屏幕内容\"等敏感能力提示"]
      },
      {
        "page_role": "获权后行为佐证（无界面）",
        "page_identifier": "无 UI；可在任意输入框中键入文本后观察 ninere 是否抓取并触发外发线程",
        "why_most_useful": "证明获权后动作是全局键盘记录而非无障碍辅助，可与代码证据交叉验证",
        "observable_utg_signals": ["切换应用后网络请求（加密载荷）是否出现", "输入文本是否被拼接进 JSON 结构"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区在于引导完全外置：包内无任何引导 UI，若远端页面用图片承载话术则需 OCR；此外包名伪造 system/三星更新组件，静态名单匹配容易被误判为系统组件；DEX 虽未加壳但核心外发链路经 AES-128（种子硬编码）加密，明文载荷需动态抓包或解密脚本才能还原。"
  },
  "behavior_pattern_tags": [
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "TRIG_COLD_START_BLOCK"
  ],
  "code_anchors": [
    "com.system.android.sikhnet.MainActivity.onCreate",
    "com.system.android.sikhnet.nine.ninere.onAccessibilityEvent",
    "com.system.android.sikhnet.nine.ninere$keyclass.run",
    "com.system.android.sikhnet.ten.ten$runto.gkey",
    "res/xml/accessibility.xml",
    "res/values/strings.xml"
  ]
}
```

**覆盖边界**：受 14 次调用硬约束，未展开 `two()` 轮询体、`thirteen`、`eleven`、`zero/zerotwo/zerothree` 等采集模块的明文 C2 地址与上报字段，也未对远端页面做动态抓取；该样本的实际诱导链路需以远端 WebView 内容为准，静态侧只能确认"无应用内引导代码"这一负向结论。基于预算约束，本轮未写入项目风险台账。

</details>
