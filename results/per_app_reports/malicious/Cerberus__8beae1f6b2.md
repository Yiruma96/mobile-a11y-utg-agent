# MB_066__8beae1f6b2｜Cerberus —                            

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：173.5s

## 1. 一句话核心结论

- **核心申请方式**：一阶段壳在 attachBaseContext 反射注入 DexClassLoader 加载加密二阶段 dex，运行期以 33 个空格空名图标和土耳其语『ANDROID GUNCELLEME』（Android 更新）无障碍服务名冒充系统更新，诱导用户开启可读取窗口内容的无障碍权限。
- **静态可见性说明**：classes.dex 仅含一阶段壳与三方 SDK（amap/appsflyer/line/jackson），Manifest 声明的无障碍服务 com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj 与全部同包引导 Activity/Service 均不在静态 DEX 中；一阶段在 Application.attachBaseContext 内以异或密文解出 android.app.ActivityThread/LoadedApk 类名，通过 Field.set 篡改 ClassLoader 字段并反射构造 DexClassLoader 加载私有目录下的二阶段 dex，故无障碍引导页流转、跳转点、弹窗与遮罩逻辑全部藏于加密二阶段载荷，静态不可见。assets/consentform.html 仅确认存在（Google Roboto 样式的本地 HTML 同意书模板），正文字句未提取且无证据表明其被无障碍流程引用。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8beae1f6b21cec17eed82fb7af25e1782d5b7bf10fd22369603313f1b1a5e5e4` |
| 包名 / 年份 | `com.cave.series` / 2025 |
| 家族 / 品类 | **Cerberus**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | — |
| 引导页宣称品牌/身份 | ANDROID GUNCELLEME（土耳其语「Android 更新」，冒充 Android 系统更新） |
| 系统无障碍列表服务名 | ANDROID GUNCELLEME |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用 android:label 为 33 个纯空格使桌面图标无可见名称；多个 Activity 使用 android:label=""+Theme.NoDisplay+excludeFromRecents 实现运行后无界面残留；无障碍服务与设备管理器 Receiver 复用同一伪装标签『ANDROID GUNCELLEME』；无障碍配置无 android:description，系统列表中不出现任何用途说明；类名整体随机化（com.qyqnmuqtrwcsxf.nnjuaiupnwe.*）并以异或密文+反射隐藏加载器构造 |
| 无障碍服务类名 | `com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.cave.series.DAqUrXn（Application）+ com.qyqnmuqtrwcsxf.nnjuaiupnwe.zfgefrltz（MAIN/LAUNCHER，同时声明 android.app.role.SMS） | 进程创建即调用 Application.attachBaseContext | 不可静态还原 | 无 | 无 | `com.cave.series.DAqUrXn.attachBaseContext → walnutjoy → com.cave.series.YWoWjQcQfIlXjPdByPs.digitalhabit` |
| 2 | 跳无障碍设置 | 二阶段 dex 内 Activity（预期，类名未知）→ 系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS | 不可静态还原（classes.dex 中无 ACTION_ACCESSIBILITY_SETTINGS 调用点） | 不可静态还原 | 无 | 不可静态还原 | `无（搜索 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 均 no_matches）` |
| 3 | 跳受限设置 | 系统无障碍服务列表项「ANDROID GUNCELLEME」 | 用户进入系统无障碍设置并看到该条目 | 系统无障碍页 | **原文**：ANDROID GUNCELLEME<br>**译注**：系统无障碍列表中仅显示「ANDROID 更新」，无任何用途说明（android:description 缺失） | 用户点击条目并开启开关（是否配套引导话术不可静态还原） | `AndroidManifest.xml service com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj + res/xml/ykoojnc.xml` |
| 4 | 获权后动作 | com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj（AccessibilityService） | 服务被绑定后接收 typeWindowContentChanged / typeWindowStateChanged 事件 | 不可静态还原 | 无 | 无 | `res/xml/ykoojnc.xml（canRetrieveWindowContent=true, typeWindowContentChanged\|typeWindowStateChanged）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面启动器图标名称：android:label 为 33 个空格，视觉上完全空白
- 系统无障碍服务列表条目名：android:label="ANDROID GUNCELLEME"（无 android:description 补充说明）
- 系统设备管理器激活页名称：receiver com.qyqnmuqtrwcsxf.nnjuaiupnwe.rsw.sozjrrawore 复用 label="ANDROID GUNCELLEME"
- 本地 HTML 同意书模板 assets/consentform.html（仅确认存在，正文字句未提取，未见与无障碍引导的静态关联）
- 引导弹窗/WebView/悬浮窗等运行期文字：全部位于加密二阶段 dex，静态不可见

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | ANDROID GUNCELLEME | ANDROID 更新 | `AndroidManifest.xml: accessibility service android:label 与 device-admin receiver android:label` | 假更新 |
| en | — | （33 个空格，无可见应用名） | `AndroidManifest.xml: <application android:label>` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：classes.dex 内无任何无障碍设置跳转或 onResume 重跳代码，拒绝后的反应逻辑位于加密二阶段 dex
- **遮罩叠层 / 高仿系统设置页**：不可静态还原：静态 DEX 中无 TYPE_APPLICATION_OVERLAY / ACTION_MANAGE_OVERLAY 调用点，虽已申请 SYSTEM_ALERT_WINDOW 权限，但悬浮遮罩实现位于二阶段载荷
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（targetSdkVersion=30，未在静态 DEX 发现应用详情/受限设置引导代码）
- **获权后即时行为与防撤权机制**：不可静态还原；Manifest 已声明 BIND_DEVICE_ADMIN 设备管理器 Receiver 与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备抗卸载/抗清理能力面，但具体是否在获权后阻止撤权位于二阶段 dex
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动瞬间即开始采集：应用一启动就执行 attachBaseContext 解密注入二阶段 dex，因此应在 Launcher 点击后立即录屏并持续抓取顶层 Activity，重点捕捉首次出现的新 Activity 以及任何指向 Settings.ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 的 intent 跳转（可 Hook startActivity 的 Intent action 作为触发点）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在明显盲区：一阶段壳在 attachBaseContext 反射注入 DexClassLoader 加载私有目录二阶段 dex，所有引导页、跳转与遮罩逻辑均在加密载荷中，纯静态无法定位；此外应用标签为 33 个空格、Activity 使用 NoDisplay 与 excludeFromRecents，运行后桌面与最近任务均无可见痕迹，若 UTG 仅在用户主动操作后抓取，可能错过冷启动阶段的瞬时弹窗，需从进程创建起全程录屏。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（二阶段 dex 内的首个 Activity/Dialog）** | 包名 com.cave.series 下新出现的 Activity，标签为空、Theme.NoDisplay 或半透明主题；层级中含「ANDROID GUNCELLEME」或土耳其语文本 | 这是唯一能直接观测到诱导话术原文与按钮可取消性的页面，静态完全不可见 | 页面标题/正文文本是否出现 Android 更新、系统故障等字样；是否存在取消/跳过按钮，或仅单个确认按钮；是否出现 WebView 节点承载说明文字 |
| **系统无障碍服务列表项** | Settings 无障碍页面中包含文本 ANDROID GUNCELLEME 的条目 | 直接验证伪装身份与服务开启状态，是无障碍滥用的必要环节 | 服务条目显示名 ANDROID GUNCELLEME；条目副标题/描述为空；开关状态变化前后应用是否立即切页 |
| **跳转设置后压栈的悬浮遮罩/引导层** | 非本应用 Activity 的全屏半透明窗口，覆盖在 Settings 之上，含高亮圆圈或手指指引图 | 判定是否采用遮罩叠层指引（overlay 教学），是区分强诱导与普通引导的关键 | 窗口类型是否为 TYPE_APPLICATION_OVERLAY；遮罩上是否有指向无障碍开关的箭头或编号步骤；返回键是否被吞掉 |
| **拒绝/返回后的反馈页** | 用户按返回离开系统设置后重新出现的本应用 Activity 或弹窗 | 识别拒绝循环重跳机制（onResume 死循环或定时器拉起） | 返回设置后 1–3 秒内是否自动再跳设置页；弹窗文案是否变为催促/恐吓措辞 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.cave.series.DAqUrXn.attachBaseContext`
- `com.cave.series.YWoWjQcQfIlXjPdByPs.digitalhabit`
- `com.cave.series.YWoWjQcQfIlXjPdByPs.crashworry`
- `com.cave.series.YWoWjQcQfIlXjPdByPs.despairarmed`
- `res/xml/ykoojnc.xml`
- `AndroidManifest.xml（service com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验：无障碍引导流程）

**1. 静态可见性：核心引导流程不在 `classes.dex` 内**
Manifest 声明的无障碍服务 `com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj`、全部 `com.qyqnmuqtrwcsxf.*` 下的 Activity、Service 和 Receiver 在 `classes.dex` 中**均不存在**（`list_codebase` 显示只有 `com.amap`、`com.cave`、`com.appsflyer`、`com.linecorp` 四个包）。因此，对无障碍引导流程、`ACTION_ACCESSIBILITY_SETTINGS` 跳转和引导弹窗做静态核验时，**全部无法得出结果**：`search_function_callsites` 对 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`TYPE_APPLICATION_OVERLAY`、`ACTION_MANAGE_OVERLAY` 均返回 `no_matches`。

**2. 原因已定位：一阶段壳在 `attachBaseContext` 反射注入二阶段 dex**
[DAqUrXn.attachBaseContext()](<resource-unit:#1.dex1 code:com.cave.series.DAqUrXn#attachBaseContext>) → `privatepledge`/`sessionunlock`（`Context.getDir` 建私有目录）→ `walnutjoy` → [Y WoWjQcQfIlXjPdByPs.digitalhabit()](<resource-unit:#1.dex1 code:com.cave.series.YWoWjQcQfIlXjPdByPs#digitalhabit>)。其中类名由异或密文解出（[despairarmed](<resource-unit:#1.dex1 code:com.cave.series.YWoWjQcQfIlXjPdByPs#despairarmed>) → `android.app.ActivityThread`、[wetwhen](<resource-unit:#1.dex1 code:com.cave.series.YWoWjQcQfIlXjPdByPs#wetwhen>) → `LoadedApk` 相关），[phrasedecorate()](<resource-unit:#1.dex1 code:com.cave.series.YWoWjQcQfIlXjPdByPs#phrasedecorate>) 用 `Field.set` 改写 ClassLoader 字段，[crashworry()](<resource-unit:#1.dex1 code:com.cave.series.YWoWjQcQfIlXjPdByPs#crashworry>) 用反射构造 `DexClassLoader` 并挂入。二阶段 dex 来自私有目录，包内 `assets/` 无 dex/zip 载荷。

**3. 仍可静态确认的伪装与诱导设计（Manifest 层）**
- 应用 `android:label` 为 **33 个空格**，桌面图标无可见名称；多个 Activity `android:label=""`、`Theme.NoDisplay`、`excludeFromRecents="true"`，运行后无可见界面残留。
- 无障碍服务 `android:label="ANDROID GUNCELLEME"`（土耳其语“Android 更新”），设备管理器 Receiver 也复用同一标签，构成**以“系统更新”名义冒名**。
- 无障碍配置 [res/xml/ykoojnc.xml](<resource-unit:#1 file:res/xml/ykoojnc.xml>)：`canRetrieveWindowContent="true"`、`typeWindowContentChanged|typeWindowStateChanged`、`flagReportViewIds|flagIncludeNotImportantViews`，**无 `android:description`** —— 系统无障碍列表中只有“ANDROID GUNCELLEME”一行字，没有任何用途说明。
- 首启入口为 `com.qyqnmuqtrwcsxf.nnjuaiupnwe.zfgefrltz`（MAIN/LAUNCHER，同时申请 `android.app.role.SMS` 角色），同包另有短信 `SENDTO/SEND`、`WAP_PUSH_DELIVER`、`RESPOND_VIA_MESSAGE` 组件，属完整短信拦截能力面。

**4. 未能证实项（如实标注）**
`assets/consentform.html` 仅核验到 CSS/字体（Roboto、`#title_head`、`.button_title` 等），**未取得正文字句**，也无静态证据表明它被无障碍引导流程加载，故不作为引导话术证据；`assets/HM_JsBridge.js` 属 HMS 桥，与本流程无关。

**5. 覆盖边界**
引导弹窗、跳设置时机、拒绝循环、遮罩叠层等**全部运行期 UTG 细节均位于加密二阶段 dex**，本次静态分析不可还原；需动态运行才能补齐。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 仅含一阶段壳与三方 SDK（amap/appsflyer/line/jackson），Manifest 声明的无障碍服务 com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj 与全部同包引导 Activity/Service 均不在静态 DEX 中；一阶段在 Application.attachBaseContext 内以异或密文解出 android.app.ActivityThread/LoadedApk 类名，通过 Field.set 篡改 ClassLoader 字段并反射构造 DexClassLoader 加载私有目录下的二阶段 dex，故无障碍引导页流转、跳转点、弹窗与遮罩逻辑全部藏于加密二阶段载荷，静态不可见。assets/consentform.html 仅确认存在（Google Roboto 样式的本地 HTML 同意书模板），正文字句未提取且无证据表明其被无障碍流程引用。",
  "summary_one_liner": "一阶段壳在 attachBaseContext 反射注入 DexClassLoader 加载加密二阶段 dex，运行期以 33 个空格空名图标和土耳其语『ANDROID GUNCELLEME』（Android 更新）无障碍服务名冒充系统更新，诱导用户开启可读取窗口内容的无障碍权限。",
  "disguise_identity": {
    "app_display_name": "                           ",
    "claimed_brand_or_persona": "ANDROID GUNCELLEME（土耳其语「Android 更新」，冒充 Android 系统更新）",
    "a11y_service_label": "ANDROID GUNCELLEME",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用 android:label 为 33 个纯空格使桌面图标无可见名称；多个 Activity 使用 android:label=\"\"+Theme.NoDisplay+excludeFromRecents 实现运行后无界面残留；无障碍服务与设备管理器 Receiver 复用同一伪装标签『ANDROID GUNCELLEME』；无障碍配置无 android:description，系统列表中不出现任何用途说明；类名整体随机化（com.qyqnmuqtrwcsxf.nnjuaiupnwe.*）并以异或密文+反射隐藏加载器构造"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.cave.series.DAqUrXn（Application）+ com.qyqnmuqtrwcsxf.nnjuaiupnwe.zfgefrltz（MAIN/LAUNCHER，同时声明 android.app.role.SMS）",
      "trigger_event": "进程创建即调用 Application.attachBaseContext",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此阶段不展示界面；壳在 attachBaseContext 中建私有目录、解密类名并反射注入 DexClassLoader 加载二阶段 dex",
      "user_action_requested": "无",
      "code_anchor": "com.cave.series.DAqUrXn.attachBaseContext → walnutjoy → com.cave.series.YWoWjQcQfIlXjPdByPs.digitalhabit"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "二阶段 dex 内 Activity（预期，类名未知）→ 系统设置 Settings.ACTION_ACCESSIBILITY_SETTINGS",
      "trigger_event": "不可静态还原（classes.dex 中无 ACTION_ACCESSIBILITY_SETTINGS 调用点）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静态 DEX 中不存在任何跳转无障碍设置或应用详情设置的代码，跳转动作完全位于加密二阶段载荷",
      "user_action_requested": "不可静态还原",
      "code_anchor": "无（搜索 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 均 no_matches）"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统无障碍服务列表项「ANDROID GUNCELLEME」",
      "trigger_event": "用户进入系统无障碍设置并看到该条目",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "ANDROID GUNCELLEME",
      "shown_text_zh": "系统无障碍列表中仅显示「ANDROID 更新」，无任何用途说明（android:description 缺失）",
      "user_action_requested": "用户点击条目并开启开关（是否配套引导话术不可静态还原）",
      "code_anchor": "AndroidManifest.xml service com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj + res/xml/ykoojnc.xml"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj（AccessibilityService）",
      "trigger_event": "服务被绑定后接收 typeWindowContentChanged / typeWindowStateChanged 事件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务具备 canRetrieveWindowContent 与 flagReportViewIds，可持续读取前台窗口内容与控件 ID；具体滥用逻辑在二阶段 dex",
      "user_action_requested": "无",
      "code_anchor": "res/xml/ykoojnc.xml（canRetrieveWindowContent=true, typeWindowContentChanged|typeWindowStateChanged）"
    }
  ],
  "text_presentation_locations": [
    "桌面启动器图标名称：android:label 为 33 个空格，视觉上完全空白",
    "系统无障碍服务列表条目名：android:label=\"ANDROID GUNCELLEME\"（无 android:description 补充说明）",
    "系统设备管理器激活页名称：receiver com.qyqnmuqtrwcsxf.nnjuaiupnwe.rsw.sozjrrawore 复用 label=\"ANDROID GUNCELLEME\"",
    "本地 HTML 同意书模板 assets/consentform.html（仅确认存在，正文字句未提取，未见与无障碍引导的静态关联）",
    "引导弹窗/WebView/悬浮窗等运行期文字：全部位于加密二阶段 dex，静态不可见"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "ANDROID GUNCELLEME",
      "text_zh": "ANDROID 更新",
      "source_location": "AndroidManifest.xml: accessibility service android:label 与 device-admin receiver android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "                           ",
      "text_zh": "（33 个空格，无可见应用名）",
      "source_location": "AndroidManifest.xml: <application android:label>",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：classes.dex 内无任何无障碍设置跳转或 onResume 重跳代码，拒绝后的反应逻辑位于加密二阶段 dex",
    "overlay_or_fake_settings": "不可静态还原：静态 DEX 中无 TYPE_APPLICATION_OVERLAY / ACTION_MANAGE_OVERLAY 调用点，虽已申请 SYSTEM_ALERT_WINDOW 权限，但悬浮遮罩实现位于二阶段载荷",
    "restricted_settings_13plus_coaching": "无静态证据（targetSdkVersion=30，未在静态 DEX 发现应用详情/受限设置引导代码）",
    "post_grant_anti_removal": "不可静态还原；Manifest 已声明 BIND_DEVICE_ADMIN 设备管理器 Receiver 与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，具备抗卸载/抗清理能力面，但具体是否在获权后阻止撤权位于二阶段 dex",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动瞬间即开始采集：应用一启动就执行 attachBaseContext 解密注入二阶段 dex，因此应在 Launcher 点击后立即录屏并持续抓取顶层 Activity，重点捕捉首次出现的新 Activity 以及任何指向 Settings.ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 的 intent 跳转（可 Hook startActivity 的 Intent action 作为触发点）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（二阶段 dex 内的首个 Activity/Dialog）",
        "page_identifier": "包名 com.cave.series 下新出现的 Activity，标签为空、Theme.NoDisplay 或半透明主题；层级中含「ANDROID GUNCELLEME」或土耳其语文本",
        "why_most_useful": "这是唯一能直接观测到诱导话术原文与按钮可取消性的页面，静态完全不可见",
        "observable_utg_signals": ["页面标题/正文文本是否出现 Android 更新、系统故障等字样", "是否存在取消/跳过按钮，或仅单个确认按钮", "是否出现 WebView 节点承载说明文字"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页面中包含文本 ANDROID GUNCELLEME 的条目",
        "why_most_useful": "直接验证伪装身份与服务开启状态，是无障碍滥用的必要环节",
        "observable_utg_signals": ["服务条目显示名 ANDROID GUNCELLEME", "条目副标题/描述为空", "开关状态变化前后应用是否立即切页"]
      },
      {
        "page_role": "跳转设置后压栈的悬浮遮罩/引导层",
        "page_identifier": "非本应用 Activity 的全屏半透明窗口，覆盖在 Settings 之上，含高亮圆圈或手指指引图",
        "why_most_useful": "判定是否采用遮罩叠层指引（overlay 教学），是区分强诱导与普通引导的关键",
        "observable_utg_signals": ["窗口类型是否为 TYPE_APPLICATION_OVERLAY", "遮罩上是否有指向无障碍开关的箭头或编号步骤", "返回键是否被吞掉"]
      },
      {
        "page_role": "拒绝/返回后的反馈页",
        "page_identifier": "用户按返回离开系统设置后重新出现的本应用 Activity 或弹窗",
        "why_most_useful": "识别拒绝循环重跳机制（onResume 死循环或定时器拉起）",
        "observable_utg_signals": ["返回设置后 1–3 秒内是否自动再跳设置页", "弹窗文案是否变为催促/恐吓措辞"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在明显盲区：一阶段壳在 attachBaseContext 反射注入 DexClassLoader 加载私有目录二阶段 dex，所有引导页、跳转与遮罩逻辑均在加密载荷中，纯静态无法定位；此外应用标签为 33 个空格、Activity 使用 NoDisplay 与 excludeFromRecents，运行后桌面与最近任务均无可见痕迹，若 UTG 仅在用户主动操作后抓取，可能错过冷启动阶段的瞬时弹窗，需从进程创建起全程录屏。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION"
  ],
  "code_anchors": [
    "com.cave.series.DAqUrXn.attachBaseContext",
    "com.cave.series.YWoWjQcQfIlXjPdByPs.digitalhabit",
    "com.cave.series.YWoWjQcQfIlXjPdByPs.crashworry",
    "com.cave.series.YWoWjQcQfIlXjPdByPs.despairarmed",
    "res/xml/ykoojnc.xml",
    "AndroidManifest.xml（service com.qyqnmuqtrwcsxf.nnjuaiupnwe.aorgjkpdws.fuacmnhqmbbj）"
  ]
}
```

**本次已写入的风险台账**：新增 R-002（`malware_trojan` / high，反射注入 DexClassLoader 加载二阶段 dex）；R-001（`deceptive_behavior` / high，冒充“ANDROID GUNCELLEME”无障碍服务并捆绑短信/装包权限）保持不变，二者互补：R-002 解释了 R-001 中引导流程静态不可见的成因。

</details>
