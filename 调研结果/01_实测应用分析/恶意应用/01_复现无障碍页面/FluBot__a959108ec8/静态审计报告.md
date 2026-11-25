# MB_155__a959108ec8｜FluBot — DHL

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：168.1s

## 1. 一句话核心结论

- **核心申请方式**：DHL 品牌伪装的 FluBot 家族样本，以 MultidexPacker 加密二阶段载荷在 attachBaseContext 静默加载，再借 / DHL / 无障碍服务（typeAllMask+可读取窗口内容）配合短信/通知监听权限引导用户开启无障碍，实现验证码窃取与界面控制。
- **静态可见性说明**：一阶段 classes.dex 仅含 11 个 com.hadoop.bigspark 加载器类；Application.attachBaseContext 立即调用 f.a(Context) 反射改写 BaseDexClassLoader 注入 assets/rukjGfF/gFIG8gauf1.8Uj（zlib 解压后 949KB 高熵密文，无 dex/PK/accessibility/DHL 明文，单字节 XOR 无命中）。无障碍服务实现、引导 Activity/WebView、ACTION_ACCESSIBILITY_SETTINGS 跳转与全部文案均在二阶段加密载荷内，静态不可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a959108ec8f93ee4c71e588236788d17372f9d61b8f71a509a776f097889f36b` |
| 包名 / 年份 | `com.iqiyi.i18n` / 2022 |
| 家族 / 品类 | **FluBot**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | DHL |
| 引导页宣称品牌/身份 | DHL（国际快递品牌），用于冒充物流/包裹通知类应用 |
| 系统无障碍列表服务名 | / DHL /（android:description 原文，服务无可见功能名，仅显示斜杠包裹的品牌词） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.iqiyi.i18n（爱奇艺包名）与显示名 DHL 完全不符；sharedUserId=jxvomWxSCcZRYWSi.uid.shared 随机串；全部组件名混淆为 p4c4a83bb/p05f9560f 等短随机串；无障碍描述用『/ DHL /』斜杠包裹，制造近似空白/占位的观感以弱化警告文本；同时注册 5 个无 intent-filter 的 Activity（p7c9f21e3、p638ebd54 singleInstance、pe795bd05 等）用于遮罩与跳板；debuggable=true 便于远程调试注入 |
| 无障碍服务类名 | `com.iqiyi.i18n.p4c4a83bb` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |
| 系统设置项说明 (`android:description`) | / DHL / |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.iqiyi.i18n.p05f9560f（LAUNCHER, singleTop）→ Application com.hadoop.bigspark.e | 点击桌面 DHL 图标启动，Application.attachBaseContext 先执行解密注入，再进入 Launcher Activity | 不可静态还原 | **原文**：无（实现类在加密载荷内）<br>**译注**：不可静态确认，预计为 DHL 快递查询类外壳界面 | 不可静态还原 | `com.hadoop.bigspark.e#attachBaseContext → com.hadoop.bigspark.f#a(Context)` |
| 2 | 业务功能触发 | 二阶段载荷内的引导 Activity / Dialog（类名不可见） | 不可静态还原；预期由 Launcher Activity 的 onCreate/onResume 或点击业务按钮触发 | 不可静态还原 | **原文**：无（文案位于加密载荷或远端）<br>**译注**：不可静态确认 | 不可静态还原（是否存在取消/跳过按钮无法确定） | `不可静态定位（二阶段密文）` |
| 3 | 跳无障碍设置 | 系统 Settings.ACTION_ACCESSIBILITY_SETTINGS（android.settings.ACCESSIBILITY_SETTINGS） | 不可静态还原；可见 DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 字符串，跳转代码在载荷内 | 系统无障碍页 | **原文**：系统页内服务项显示：/ DHL /（来自 res/values/strings.xml accessibility_service_description）<br>**译注**：系统无障碍服务列表中该应用呈现为『/ DHL /』，用户据此开启 | 在系统无障碍列表中点击『/ DHL /』并确认开启 | `res/xml/accessibility_service_config.xml + res/values/strings.xml#accessibility_service_description` |
| 4 | 获权后动作 | com.iqiyi.i18n.p4c4a83bb（AccessibilityService，typeAllMask / canRetrieveWindowContent / flagRetrieveInteractiveWindows） | onAccessibilityEvent 与 onServiceConnected（实现不可见） | 不可静态还原 | 无 | 无需用户操作 | `#1 manifest:components（service com.iqiyi.i18n.p4c4a83bb）、res/xml/accessibility_service_config.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项描述：res/values/strings.xml 的 accessibility_service_description = "/ DHL /"，经 res/xml/accessibility_service_config.xml 的 android:description 引用
- 桌面图标名称：res/values/strings.xml 的 app_name = "DHL"，由 AndroidManifest application android:label 引用
- 引导说明页/Dialog/WebView 的正文：位于 assets/rukjGfF/gFIG8gauf1.8Uj 加密载荷内，静态不可读
- 未确认：是否存在跳转后的悬浮遮罩引导窗（应用注册了 singleInstance Activity p638ebd54，疑似遮罩页但实现不可见）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | / DHL / | / DHL /（仅斜杠包裹的品牌词，无任何功能说明） | `res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）` | 未知 |
| en | DHL | DHL | `res/values/strings.xml key=app_name（AndroidManifest application android:label）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导与回跳逻辑位于加密二阶段载荷，可见 DEX 中无 onResume 重跳或 Timer 拉起代码；结合 FluBot 家族行为需运行期 UTG 确认是否 onResume 死循环重跳系统设置页
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；Manifest 中注册了 singleInstance Activity com.iqiyi.i18n.p638ebd54 与无 intent-filter 的 p7c9f21e3，具备叠加遮罩/自绘引导页的组件条件，但实现类在载荷内无法确认
- **Android 13+ 受限设置（Restricted Settings）应对**：无（应用 targetSdkVersion=28，低于 Android 13，无受限设置概念；静态未见相关引导代码）
- **获权后即时行为与防撤权机制**：不可静态还原：预筛检出 WATCH_SETTINGS 线索指向监听系统设置页，但相关代码在加密载荷内，无法确认是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权；另有 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 与 KILL_BACKGROUND_PROCESSES 用于维持常驻
- **良性降级 / 替代方案**：无（无降级或替代路径证据）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：从 Launcher Activity com.iqiyi.i18n.p05f9560f 冷启动即全程录屏；同时 Hook Context.startActivity 的 Intent action，一旦出现 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 立即截帧，并在系统页停留期间每 500ms 连续截帧以捕获叠层遮罩
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：主要盲区为一阶段完全无引导逻辑：真实引导文案、页面流转与回跳循环全部位于 MultidexPacker 加密载荷 assets/rukjGfF/gFIG8gauf1.8Uj 中，静态只能给出 Manifest 与资源层证据；另需注意若载荷以图片/GIF 承载引导（needs_ocr）或由远端 HTML 下发，纯文本 UTG 可能采集不到可判别话术。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | com.iqiyi.i18n.p05f9560f 之上弹出的 Dialog 或全屏 Activity，文本中应出现 DHL/快递/包裹/权限等关键词 | 这是唯一能逐字取得引导话术（假更新、假安全、清理伪装等）的界面，静态被壳阻断 | 弹窗标题与正文全文本；按钮文案是否只有『确定/开启』而无取消；是否出现 DHL 之外的品牌词或系统警告字样 |
| **跳转前 WebView 教学页** | 含 WebView 的 Activity 或 assets 内 HTML（当前 assets 仅见 sConsole.html 269 字节与模型文件，真实 HTML 可能在载荷内） | 区分本地 HTML 教学与远端下发页面，判断文案可被云控替换 | WebView 加载 URL 域名；页面内分步截图/GIF 引导元素；是否含『忽略系统警告』类文案 |
| **系统无障碍服务列表项** | Settings$AccessibilitySettings 中文本为『/ DHL /』的条目 | 直接验证身份伪装：服务名无功能说明、仅有品牌词与斜杠，用户无法判断真实用途 | 列表项 description 原文 / DHL /；该条目是否为列表唯一或首个高亮项；跳转时是否自动滚动定位到该条目 |
| **设置页后压栈遮罩页** | 返回应用后出现的 singleInstance Activity com.iqiyi.i18n.p638ebd54 或全屏半透明 View | 确认是否在系统设置页之上叠加指引遮罩或伪造开关页，这是判定强制诱导的关键 | 返回后 800ms 内的顶层包名与 Activity 名；是否出现自绘开关控件而非系统控件；遮罩层是否存在无法关闭的返回键行为 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.hadoop.bigspark.e#attachBaseContext`
- `com.hadoop.bigspark.f#a(Context)`
- `assets/rukjGfF/gFIG8gauf1.8Uj`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml#accessibility_service_description`
- `AndroidManifest.xml service com.iqiyi.i18n.p4c4a83bb`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，已收口）

**静态可见性：核心引导链不可静态还原。** 应用属于 MultidexPacker 加壳样本：一阶段 `classes.dex` 只有 11 个类，全部位于 `com.hadoop.bigspark` 加载器包下；`Application` 在 [attachBaseContext](<resource-unit:#1.dex1 code:com.hadoop.bigspark.e#attachBaseContext>) 中直接调用 `com.hadoop.bigspark.f.a(Context)`，通过反射改写 `BaseDexClassLoader` 的 `pathList/dexElements`，把 [assets/rukjGfF/gFIG8gauf1.8Uj](<resource-unit:#1 file:assets/rukjGfF/gFIG8gauf1.8Uj>) 解密后注入 ClassLoader。该资产 zlib 解压后为 949 KB 高熵数据，不包含 `dex\n`、`PK`、`accessibility`、`DHL` 等任何明文，也没有单字节 XOR 命中，因此真实业务类（含无障碍服务实现、引导页 Activity/WebView）全部位于二阶段密文中。

**从 Manifest 与资源层可以确认的事实：**
- 应用身份是伪装：`android:label`/`app_name` = `DHL`，无障碍服务描述 [strings.xml](<resource-unit:#1 file:res/values/strings.xml>) 中的 `accessibility_service_description` = `/ DHL /`；包名却为 `com.iqiyi.i18n`（爱奇艺包名），`sharedUserId` = `jxvomWxSCcZRYWSi.uid.shared`，所有组件名混淆为 `p4c4a83bb` 式短串，并且 `debuggable=true`。
- 无障碍服务 [com.iqiyi.i18n.p4c4a83bb](<resource-unit:#1 manifest:components>) 的配置见 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>)：`typeAllMask`、`flagRetrieveInteractiveWindows`、`flagReportViewIds`、`canRetrieveWindowContent=true`，这意味着它可以读取全部界面内容并执行全局操作，属于典型的短信木马与覆盖攻击配置。
- 同时具备通知监听服务 `p91564b42`（BIND_NOTIFICATION_LISTENER_SERVICE）、SMS_DELIVER/WAP_PUSH 接收器、`SEND_SMS/READ_SMS/WRITE_SMS/READ_CONTACTS/CALL_PHONE/QUERY_ALL_PACKAGES/REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 等权限，这是 FluBot 家族“拦截短信验证码 + 电话诈骗”的能力组合。
- 冷启动入口为 [com.iqiyi.i18n.p05f9560f](<resource-unit:#1 manifest:components>)（MAIN/LAUNCHER, singleTop）；另有 `p638ebd54`（singleInstance，疑似悬浮/遮罩页）、`p7c9f21e3`、`pe795bd05` 等未命名 Activity，但它们的实现类均不在可见 DEX 中。
- `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 在可见 DEX 中没有任何静态引用（检索结果为 no_matches），说明跳转代码位于加密载荷内。

**结论：** 该应用通过 `attachBaseContext` 阶段的加密二阶段加载进入执行，再以 `DHL` 品牌伪装和 `/ DHL /` 无障碍服务描述引导用户开启高权限无障碍服务；引导页面的具体载体（原生 Dialog、本地或远端 WebView、悬浮遮罩）、文案、是否拒绝后循环重跳等 UTG 细节全部位于加壳载荷中，静态无法确定。已确认风险 R-001 记录了该加壳加载链；无障碍诱导的具体页面流转需在设备端通过 UTG 在运行期捕获。

**运行期 UTG 建议：** 冷启动即开始录制；在系统 `AccessibilitySettings` 页、`应用详情` 页弹出瞬间以及获权后 800 ms 内各保存一帧；重点比对系统无障碍列表项文字是否仅为 `/ DHL /`（无实际功能说明）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "一阶段 classes.dex 仅含 11 个 com.hadoop.bigspark 加载器类；Application.attachBaseContext 立即调用 f.a(Context) 反射改写 BaseDexClassLoader 注入 assets/rukjGfF/gFIG8gauf1.8Uj（zlib 解压后 949KB 高熵密文，无 dex/PK/accessibility/DHL 明文，单字节 XOR 无命中）。无障碍服务实现、引导 Activity/WebView、ACTION_ACCESSIBILITY_SETTINGS 跳转与全部文案均在二阶段加密载荷内，静态不可见。",
  "summary_one_liner": "DHL 品牌伪装的 FluBot 家族样本，以 MultidexPacker 加密二阶段载荷在 attachBaseContext 静默加载，再借 / DHL / 无障碍服务（typeAllMask+可读取窗口内容）配合短信/通知监听权限引导用户开启无障碍，实现验证码窃取与界面控制。",
  "disguise_identity": {
    "app_display_name": "DHL",
    "claimed_brand_or_persona": "DHL（国际快递品牌），用于冒充物流/包裹通知类应用",
    "a11y_service_label": "/ DHL /（android:description 原文，服务无可见功能名，仅显示斜杠包裹的品牌词）",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.iqiyi.i18n（爱奇艺包名）与显示名 DHL 完全不符；sharedUserId=jxvomWxSCcZRYWSi.uid.shared 随机串；全部组件名混淆为 p4c4a83bb/p05f9560f 等短随机串；无障碍描述用『/ DHL /』斜杠包裹，制造近似空白/占位的观感以弱化警告文本；同时注册 5 个无 intent-filter 的 Activity（p7c9f21e3、p638ebd54 singleInstance、pe795bd05 等）用于遮罩与跳板；debuggable=true 便于远程调试注入"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.iqiyi.i18n.p05f9560f（LAUNCHER, singleTop）→ Application com.hadoop.bigspark.e",
      "trigger_event": "点击桌面 DHL 图标启动，Application.attachBaseContext 先执行解密注入，再进入 Launcher Activity",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（实现类在加密载荷内）",
      "shown_text_zh": "不可静态确认，预计为 DHL 快递查询类外壳界面",
      "user_action_requested": "不可静态还原",
      "code_anchor": "com.hadoop.bigspark.e#attachBaseContext → com.hadoop.bigspark.f#a(Context)"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "二阶段载荷内的引导 Activity / Dialog（类名不可见）",
      "trigger_event": "不可静态还原；预期由 Launcher Activity 的 onCreate/onResume 或点击业务按钮触发",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（文案位于加密载荷或远端）",
      "shown_text_zh": "不可静态确认",
      "user_action_requested": "不可静态还原（是否存在取消/跳过按钮无法确定）",
      "code_anchor": "不可静态定位（二阶段密文）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings.ACTION_ACCESSIBILITY_SETTINGS（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "不可静态还原；可见 DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 字符串，跳转代码在载荷内",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "系统页内服务项显示：/ DHL /（来自 res/values/strings.xml accessibility_service_description）",
      "shown_text_zh": "系统无障碍服务列表中该应用呈现为『/ DHL /』，用户据此开启",
      "user_action_requested": "在系统无障碍列表中点击『/ DHL /』并确认开启",
      "code_anchor": "res/xml/accessibility_service_config.xml + res/values/strings.xml#accessibility_service_description"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.iqiyi.i18n.p4c4a83bb（AccessibilityService，typeAllMask / canRetrieveWindowContent / flagRetrieveInteractiveWindows）",
      "trigger_event": "onAccessibilityEvent 与 onServiceConnected（实现不可见）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后可读取全部窗口内容并执行全局操作，配合 SMS_DELIVER/WAP_PUSH 接收器与通知监听服务 p91564b42",
      "user_action_requested": "无需用户操作",
      "code_anchor": "#1 manifest:components（service com.iqiyi.i18n.p4c4a83bb）、res/xml/accessibility_service_config.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项描述：res/values/strings.xml 的 accessibility_service_description = \"/ DHL /\"，经 res/xml/accessibility_service_config.xml 的 android:description 引用",
    "桌面图标名称：res/values/strings.xml 的 app_name = \"DHL\"，由 AndroidManifest application android:label 引用",
    "引导说明页/Dialog/WebView 的正文：位于 assets/rukjGfF/gFIG8gauf1.8Uj 加密载荷内，静态不可读",
    "未确认：是否存在跳转后的悬浮遮罩引导窗（应用注册了 singleInstance Activity p638ebd54，疑似遮罩页但实现不可见）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "/ DHL /",
      "text_zh": "/ DHL /（仅斜杠包裹的品牌词，无任何功能说明）",
      "source_location": "res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "DHL",
      "text_zh": "DHL",
      "source_location": "res/values/strings.xml key=app_name（AndroidManifest application android:label）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导与回跳逻辑位于加密二阶段载荷，可见 DEX 中无 onResume 重跳或 Timer 拉起代码；结合 FluBot 家族行为需运行期 UTG 确认是否 onResume 死循环重跳系统设置页",
    "overlay_or_fake_settings": "不可静态还原；Manifest 中注册了 singleInstance Activity com.iqiyi.i18n.p638ebd54 与无 intent-filter 的 p7c9f21e3，具备叠加遮罩/自绘引导页的组件条件，但实现类在载荷内无法确认",
    "restricted_settings_13plus_coaching": "无（应用 targetSdkVersion=28，低于 Android 13，无受限设置概念；静态未见相关引导代码）",
    "post_grant_anti_removal": "不可静态还原：预筛检出 WATCH_SETTINGS 线索指向监听系统设置页，但相关代码在加密载荷内，无法确认是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权；另有 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 与 KILL_BACKGROUND_PROCESSES 用于维持常驻",
    "benign_graceful_degradation": "无（无降级或替代路径证据）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "从 Launcher Activity com.iqiyi.i18n.p05f9560f 冷启动即全程录屏；同时 Hook Context.startActivity 的 Intent action，一旦出现 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 立即截帧，并在系统页停留期间每 500ms 连续截帧以捕获叠层遮罩",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "com.iqiyi.i18n.p05f9560f 之上弹出的 Dialog 或全屏 Activity，文本中应出现 DHL/快递/包裹/权限等关键词",
        "why_most_useful": "这是唯一能逐字取得引导话术（假更新、假安全、清理伪装等）的界面，静态被壳阻断",
        "observable_utg_signals": ["弹窗标题与正文全文本", "按钮文案是否只有『确定/开启』而无取消", "是否出现 DHL 之外的品牌词或系统警告字样"]
      },
      {
        "page_role": "跳转前 WebView 教学页",
        "page_identifier": "含 WebView 的 Activity 或 assets 内 HTML（当前 assets 仅见 sConsole.html 269 字节与模型文件，真实 HTML 可能在载荷内）",
        "why_most_useful": "区分本地 HTML 教学与远端下发页面，判断文案可被云控替换",
        "observable_utg_signals": ["WebView 加载 URL 域名", "页面内分步截图/GIF 引导元素", "是否含『忽略系统警告』类文案"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings$AccessibilitySettings 中文本为『/ DHL /』的条目",
        "why_most_useful": "直接验证身份伪装：服务名无功能说明、仅有品牌词与斜杠，用户无法判断真实用途",
        "observable_utg_signals": ["列表项 description 原文 / DHL /", "该条目是否为列表唯一或首个高亮项", "跳转时是否自动滚动定位到该条目"]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "返回应用后出现的 singleInstance Activity com.iqiyi.i18n.p638ebd54 或全屏半透明 View",
        "why_most_useful": "确认是否在系统设置页之上叠加指引遮罩或伪造开关页，这是判定强制诱导的关键",
        "observable_utg_signals": ["返回后 800ms 内的顶层包名与 Activity 名", "是否出现自绘开关控件而非系统控件", "遮罩层是否存在无法关闭的返回键行为"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "主要盲区为一阶段完全无引导逻辑：真实引导文案、页面流转与回跳循环全部位于 MultidexPacker 加密载荷 assets/rukjGfF/gFIG8gauf1.8Uj 中，静态只能给出 Manifest 与资源层证据；另需注意若载荷以图片/GIF 承载引导（needs_ocr）或由远端 HTML 下发，纯文本 UTG 可能采集不到可判别话术。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.hadoop.bigspark.e#attachBaseContext",
    "com.hadoop.bigspark.f#a(Context)",
    "assets/rukjGfF/gFIG8gauf1.8Uj",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml#accessibility_service_description",
    "AndroidManifest.xml service com.iqiyi.i18n.p4c4a83bb"
  ]
}
```

</details>
