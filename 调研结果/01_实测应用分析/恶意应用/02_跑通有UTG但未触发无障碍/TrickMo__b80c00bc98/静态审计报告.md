# MB_132__b80c00bc98｜TrickMo — Google services

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：256.6s

## 1. 一句话核心结论

- **核心申请方式**：以「Google services」品牌与 Google Play 服务说明文案伪装，声明 isAccessibilityTool=true 的全能无障碍服务，桌面无图标、引导页面与服务工作类全部藏于加密 assets 中运行期释放，属典型伪装型 UTG 无障碍诱导木马。
- **静态可见性说明**：classes.dex 可解析但为花指令混淆（大量无意义算术填充），无障碍服务类 orkei.ti981.pay.ZNmNNvl7NO 在 DEX 中完全无定义（全库仅 1 处 'orkei' 字符串），且无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 常量；引导界面主体 assets/www/index.html(829KB)、assets/EDcb.json(5.4MB)、assets/clicker.json、assets/googleinfo.txt、assets/*.js 等 53 个 assets 条目在 ZIP 层即被加密，需运行期由 Rthingworld.yellowjob() 释放后才可读。因此仅伪装层（应用名、无障碍服务标签/说明、a11y 能力配置、组件隐匿）静态可见，引导页面流转与跳转逻辑不可静态还原。
- **命中的行为模式标签**：`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b80c00bc987ea9acacec57eeaf299421da8e083f611084816bf0c015c7088ded` |
| 包名 / 年份 | `orkei.ti981.pay` / 2025 |
| 家族 / 品类 | **TrickMo**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google services |
| 引导页宣称品牌/身份 | Google / Google Play services |
| 系统无障碍列表服务名 | Google services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 orkei.ti981.pay 与 Google 无关；无障碍说明直接套用 Google Play 服务官方文案；accessibilityservice.xml 设置 isAccessibilityTool="true" 伪称系统无障碍工具；全部 Activity 设 excludeFromRecents/noHistory/空 taskAffinity 且无 LAUNCHER 入口，桌面无图标；另有 enabled="false" 的备用 Activity dZ9jgilhHwzgNQKEdtB 可远程启用；DEX 花指令混淆、引导载荷 ZIP 层加密 |
| 无障碍服务类名 | `orkei.ti981.pay.ZNmNNvl7NO` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Google play services also enhances your app experience. It speeds up offline searches, provides more immersive maps, and improves gaming experiences. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | Application: com.dad.acquire.Rthingworld（无 LAUNCHER Activity，入口为导出 Activity orkei.ti981.pay.mNGrwzrxXIO9Azr / PushService / StubActivity 之一） | attachBaseContext() → onCreate() | 不可静态还原 | 无 | 无（静默初始化） | `com.dad.acquire.Rthingworld.attachBaseContext / com.dad.acquire.Rthingworld.yellowjob` |
| 2 | 引导说明页 | 本地 WebView 载荷 assets/www/index.html（829 KB，加密，运行期释放到私有目录）+ assets/www/inject.js、assets/1165.js/1168.js/1172.js/1173.js、assets/EDcb.json(5.4MB)、assets/clicker.json | 资产释放完成后加载（具体拉起者不可静态还原） | 本地HTML WebView | **原文**：不可静态还原（ZIP 层加密，需运行期解密）<br>**译注**：疑似仿 Google Play 服务/更新页的引导说明内容，无法静态确认 | 不可静态还原（疑为「启用/开启」按钮，无取消路径证据） | `com.dad.acquire.Rthingworld.yellowjob；assets/www/index.html` |
| 3 | 跳无障碍设置 | 系统 Settings.ACTION_ACCESSIBILITY_SETTINGS（目标列表项显示为 Google services） | 不可静态还原（DEX 中不存在 ACTION_ACCESSIBILITY_SETTINGS 常量，跳转意图应由加密载荷或运行期拼接产生） | 系统无障碍页 | **原文**：This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Google play services also enhances your app experience. It speeds up offline searches, provides more immersive maps, and improves gaming experiences.<br>**译注**：本组件提供核心功能，例如 Google 服务身份认证、联系人同步、访问最新的用户隐私设置，以及更高质量、更低功耗的基于位置的服务。Google Play 服务还会提升您的应用体验：加快离线搜索、提供更沉浸的地图与更好的游戏体验。 | 在系统无障碍列表中为「Google services」打开开关（是否含引导遮罩/教学不可静态还原） | `res/xml/accessibilityservice.xml (android:description=@7F0E001B)；AndroidManifest.xml 中 service orkei.ti981.pay.ZNmNNvl7NO (android:label=@7F0E001C)` |
| 4 | 获权后动作 | 无障碍服务 orkei.ti981.pay.ZNmNNvl7NO（实现类不在 classes.dex，由运行期载荷提供） | 系统绑定无障碍服务后 onServiceConnected（推断） | 不可静态还原 | 无 | 无 | `res/xml/accessibilityservice.xml；AndroidManifest.xml <service android:name="orkei.ti981.pay.ZNmNNvl7NO">` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务标签「Google services」（@7F0E001C）+ 说明文案（@7F0E001B，套用 Google Play 服务官方描述）——静态确认
- 应用桌面/应用信息页名称：「Google services」（application android:label=@7F0E0021）——静态确认
- 运行期私有目录释放的本地 WebView 页面 assets/www/index.html 及其配套 assets/www/inject.js、assets/1165.js~1173.js（加密，静态不可读，推断为主要图文引导载体）
- 疑似弹窗/Activity 载体：导出 Activity orkei.ti981.pay.mNGrwzrxXIO9Azr（标签 @7F0E001D）、备用 dZ9jgilhHwzgNQKEdtB（enabled=false）、StubActivity——具体布局与文案不可静态还原
- 资源内存在大量 Google Play 服务多语种提示串（Enable Google Play services / %1$s won't work unless you enable Google Play services. 等），其中部分来自 GMS/Ads SDK 资源，但同时被无障碍说明文案复用

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google services | Google 服务 | `resources.arsc @7F0E0021（application android:label）与 @7F0E001C（无障碍服务 android:label）` | 假更新 |
| en | This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Google play services also enhances your app experience. It speeds up offline searches, provides more immersive maps, and improves gaming experiences. | 本组件提供核心功能，例如 Google 服务身份认证、联系人同步、访问最新的用户隐私设置，以及更高质量、更低功耗的基于位置的服务。Google Play 服务还会提升应用体验：加快离线搜索、提供更沉浸的地图与更好的游戏体验。 | `resources.arsc @7F0E001B（accessibilityservice.xml 的 android:description）` | 隐私承诺 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 无法运行，除非你启用 Google Play 服务。 | `resources.arsc（common_google_play_services_enable_text 系列多语种串，DEX 中可见该资源名引用）` | 故障恐吓 |
| en | Enable Google Play services | 启用 Google Play 服务 | `resources.arsc（common_google_play_services_enable_title / enable_button）` | 假更新 |
| en | %1$s won't run without Google Play services, which are missing from your device. | %1$s 无法运行，因为设备缺少 Google Play 服务。 | `resources.arsc（common_google_play_services_install_text 系列）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原（DEX 中无无障碍设置跳转常量，引导/拒权重试逻辑应由加密载荷提供；运行期需 UTG 观测是否 onResume 重跳或定时拉起）
- **遮罩叠层 / 高仿系统设置页**：静态侧未见悬浮窗引导代码；但已申请 SYSTEM_ALERT_WINDOW，且载荷为本地 WebView 页面，运行期可能叠放遮罩，需 UTG 验证
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=31，低于 33，静态无受限设置教学字符串）
- **获权后即时行为与防撤权机制**：无（DEX 中无 GLOBAL_ACTION_BACK/HOME 相关静态字符串，服务实现不在 DEX 内，无法静态确认）
- **良性降级 / 替代方案**：无（无任何降级/手动模式/取消路径证据）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到应用进程启动（orkei.ti981.pay）后首次出现 WebView 加载本地 file:// 私有目录 index.html 的时刻；以及任何 Intent 指向 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（此时立即截图 + dump 无障碍服务列表项文案）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：引导正文与服务工作类均不在静态 DEX，assets 53 个条目 ZIP 层加密，只能运行期抓取；若样本在一阶段仅做静默资产释放、需服务端/二次拉起才呈现引导页，冷启动短时 UTG 可能只看到空白或无界面；另需注意该应用无 LAUNCHER 入口，UTG 必须通过外部 Intent 或推送唤醒进程。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/释放后的本地 WebView 引导页** | 包名 orkei.ti981.pay 进程内 WebView，URL 为 file:///data/user/0/orkei.ti981.pay/app_*/... 指向释放出的 index.html | 该页承载全部伪装说明与「启用」按钮，是判断是否教唆开启无障碍与是否可取消的唯一直接证据 | 页面标题/正文是否出现 Google Play 服务、更新、认证等品牌文案；是否存在「启用/开启/继续」主按钮而无取消/跳过控件；是否出现指向无障碍设置的点击热区 |
| **系统无障碍服务列表项** | Settings.ACTION_ACCESSIBILITY_SETTINGS 页面中 label=Google services 的条目及其 description 展开 | 确认系统层面呈现给用户的身份就是 Google services，构成品牌冒充的直接证据 | 列表项文本 Google services；说明文本含 authentication/synchronized contacts 等 Google 官方措辞；同列表内是否存在真实 Google Play 服务条目以比对 |
| **跳转后压栈的遮罩/引导层** | 无障碍设置页之上叠加的悬浮窗（SYSTEM_ALERT_WINDOW）或全屏 Activity | 区分「仅跳转」与「叠层指引/伪造开关」两类诱导强度，是定级关键 | 设置页上层是否出现半透明遮罩或箭头指引；是否绘制仿系统开关控件；返回键行为是否被拦截 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.dad.acquire.Rthingworld.attachBaseContext`
- `com.dad.acquire.Rthingworld.yellowjob`
- `res/xml/accessibilityservice.xml`
- `AndroidManifest.xml（service orkei.ti981.pay.ZNmNNvl7NO / activity dZ9jgilhHwzgNQKEdtB enabled=false）`
- `assets/www/index.html（加密）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（约 14 次工具调用内完成）

**静态可见性：核心引导逻辑不可静态还原。** classes.dex 可正常解析，但引导界面与无障碍服务实现都不在其中：

1. **无障碍服务类在 DEX 中不存在。** 清单声明 `orkei.ti981.pay.ZNmNNvl7NO`，但 `classes.dex` 中 `orkei` 字符串仅出现 1 次（位于 `Rthingworld.onCreate` 的 `"orkei.ti981.pay.OJICKFuNSkxW"`），全库无 `ZNmNNvl7NO` 定义，也无 `ACTION_ACCESSIBILITY_SETTINGS` / `APPLICATION_DETAILS_SETTINGS` 字符串。也就是说，**服务实现与跳转逻辑都不在静态 DEX 中**，只能来自运行期释放的载荷。
2. **载荷在 ZIP 层即被加密。** APK 内 53 个 `assets/` 条目 `flag_bits & 0x1`，含 `assets/www/index.html`（829 KB，WebView 引导页）、`assets/EDcb.json`（5.4 MB）、`assets/clicker.json`、`assets/googleinfo.txt`、`assets/data.json`、`assets/1165.js` 等，无法直接读取文案。
3. **释放链已确认。** [Rthingworld.attachBaseContext](<resource-unit:#1.dex1 code:com.dad.acquire.Rthingworld#attachBaseContext>) 通过 `getDir()` 取得私有目录，并调用 [Rthingworld.yellowjob()](<resource-unit:#1.dex1 code:com.dad.acquire.Rthingworld#yellowjob>) 把 `getAssets().open(...)` 读出的加密资产复制写入私有目录，形成「APK → 私有目录」的一阶段落地。
4. **伪装层完整可见。** 应用标签 `@7F0E0021` = `Google services`（`resources.arsc`），无障碍服务标签 `@7F0E001C`、说明 `@7F0E001B` 复用 Google Play 服务的标准说明文案；包名 `orkei.ti981.pay` 与 Google 毫无关系。
5. **无障碍配置冒充系统工具。** [accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml>) 设置 `isAccessibilityTool="true"`，同时开放 `canRetrieveWindowContent` / `canPerformGestures` / `canTakeScreenshot` / `canRequestFilterKeyEvents` 与 `accessibilityEventTypes="0xFFFFFFFF"`，远超「认证、同步联系人」的声称范围。
6. **无启动图标、入口隐藏。** 清单无 `LAUNCHER`/`MAIN`；全部 `orkei.ti981.pay.*` Activity 带 `excludeFromRecents`+`noHistory`+空 `taskAffinity`，另有 `enabled="false"` 的备用 Activity `dZ9jgilhHwzgNQKEdtB`，说明拉起依赖外部组件（导出 Activity `mNGrwzrxXIO9Azr`、FCM `PushService`、`StubActivity`）。
7. **同源高危能力并存。** 设备管理（`wipe-data`/`reset-password`/`disable-camera`）、通知监听 `gX2k3Fx`、输入法 `SoftKeyboardService`、`VpnService`、默认短信应用组件——无障碍只是整套控制面的其中一环。

**覆盖边界：** 具体「第几步弹什么页、是否悬浮遮罩、是否受限设置教学、拒权是否死循环」在静态侧**无任何证据**（DEX 无相关字符串、HTML 加密），只能靠运行期 UTG 在跳转 `ACCESSIBILITY_SETTINGS` 或释放后首次加载 WebView 时抓取。

已登记风险：R-001（deceptive_behavior / high）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 可解析但为花指令混淆（大量无意义算术填充），无障碍服务类 orkei.ti981.pay.ZNmNNvl7NO 在 DEX 中完全无定义（全库仅 1 处 'orkei' 字符串），且无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 常量；引导界面主体 assets/www/index.html(829KB)、assets/EDcb.json(5.4MB)、assets/clicker.json、assets/googleinfo.txt、assets/*.js 等 53 个 assets 条目在 ZIP 层即被加密，需运行期由 Rthingworld.yellowjob() 释放后才可读。因此仅伪装层（应用名、无障碍服务标签/说明、a11y 能力配置、组件隐匿）静态可见，引导页面流转与跳转逻辑不可静态还原。",
  "summary_one_liner": "以「Google services」品牌与 Google Play 服务说明文案伪装，声明 isAccessibilityTool=true 的全能无障碍服务，桌面无图标、引导页面与服务工作类全部藏于加密 assets 中运行期释放，属典型伪装型 UTG 无障碍诱导木马。",
  "disguise_identity": {
    "app_display_name": "Google services",
    "claimed_brand_or_persona": "Google / Google Play services",
    "a11y_service_label": "Google services",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 orkei.ti981.pay 与 Google 无关；无障碍说明直接套用 Google Play 服务官方文案；accessibilityservice.xml 设置 isAccessibilityTool=\"true\" 伪称系统无障碍工具；全部 Activity 设 excludeFromRecents/noHistory/空 taskAffinity 且无 LAUNCHER 入口，桌面无图标；另有 enabled=\"false\" 的备用 Activity dZ9jgilhHwzgNQKEdtB 可远程启用；DEX 花指令混淆、引导载荷 ZIP 层加密"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "Application: com.dad.acquire.Rthingworld（无 LAUNCHER Activity，入口为导出 Activity orkei.ti981.pay.mNGrwzrxXIO9Azr / PushService / StubActivity 之一）",
      "trigger_event": "attachBaseContext() → onCreate()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面文案；此阶段仅执行 getDir() 建私有目录并调用 yellowjob(assetPath, context) 把加密资产复制落盘",
      "user_action_requested": "无（静默初始化）",
      "code_anchor": "com.dad.acquire.Rthingworld.attachBaseContext / com.dad.acquire.Rthingworld.yellowjob"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "本地 WebView 载荷 assets/www/index.html（829 KB，加密，运行期释放到私有目录）+ assets/www/inject.js、assets/1165.js/1168.js/1172.js/1173.js、assets/EDcb.json(5.4MB)、assets/clicker.json",
      "trigger_event": "资产释放完成后加载（具体拉起者不可静态还原）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "不可静态还原（ZIP 层加密，需运行期解密）",
      "shown_text_zh": "疑似仿 Google Play 服务/更新页的引导说明内容，无法静态确认",
      "user_action_requested": "不可静态还原（疑为「启用/开启」按钮，无取消路径证据）",
      "code_anchor": "com.dad.acquire.Rthingworld.yellowjob；assets/www/index.html"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings.ACTION_ACCESSIBILITY_SETTINGS（目标列表项显示为 Google services）",
      "trigger_event": "不可静态还原（DEX 中不存在 ACTION_ACCESSIBILITY_SETTINGS 常量，跳转意图应由加密载荷或运行期拼接产生）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Google play services also enhances your app experience. It speeds up offline searches, provides more immersive maps, and improves gaming experiences.",
      "shown_text_zh": "本组件提供核心功能，例如 Google 服务身份认证、联系人同步、访问最新的用户隐私设置，以及更高质量、更低功耗的基于位置的服务。Google Play 服务还会提升您的应用体验：加快离线搜索、提供更沉浸的地图与更好的游戏体验。",
      "user_action_requested": "在系统无障碍列表中为「Google services」打开开关（是否含引导遮罩/教学不可静态还原）",
      "code_anchor": "res/xml/accessibilityservice.xml (android:description=@7F0E001B)；AndroidManifest.xml 中 service orkei.ti981.pay.ZNmNNvl7NO (android:label=@7F0E001C)"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 orkei.ti981.pay.ZNmNNvl7NO（实现类不在 classes.dex，由运行期载荷提供）",
      "trigger_event": "系统绑定无障碍服务后 onServiceConnected（推断）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面文案；配置已授予 canRetrieveWindowContent / canPerformGestures / canTakeScreenshot / canRequestFilterKeyEvents 与全部事件类型",
      "user_action_requested": "无",
      "code_anchor": "res/xml/accessibilityservice.xml；AndroidManifest.xml <service android:name=\"orkei.ti981.pay.ZNmNNvl7NO\">"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务标签「Google services」（@7F0E001C）+ 说明文案（@7F0E001B，套用 Google Play 服务官方描述）——静态确认",
    "应用桌面/应用信息页名称：「Google services」（application android:label=@7F0E0021）——静态确认",
    "运行期私有目录释放的本地 WebView 页面 assets/www/index.html 及其配套 assets/www/inject.js、assets/1165.js~1173.js（加密，静态不可读，推断为主要图文引导载体）",
    "疑似弹窗/Activity 载体：导出 Activity orkei.ti981.pay.mNGrwzrxXIO9Azr（标签 @7F0E001D）、备用 dZ9jgilhHwzgNQKEdtB（enabled=false）、StubActivity——具体布局与文案不可静态还原",
    "资源内存在大量 Google Play 服务多语种提示串（Enable Google Play services / %1$s won't work unless you enable Google Play services. 等），其中部分来自 GMS/Ads SDK 资源，但同时被无障碍说明文案复用"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google services",
      "text_zh": "Google 服务",
      "source_location": "resources.arsc @7F0E0021（application android:label）与 @7F0E001C（无障碍服务 android:label）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "This component provides core functionality like authentication to your Google services, synchronized contacts, access to all the latest user privacy settings, and higher quality, lower-powered location based services. Google play services also enhances your app experience. It speeds up offline searches, provides more immersive maps, and improves gaming experiences.",
      "text_zh": "本组件提供核心功能，例如 Google 服务身份认证、联系人同步、访问最新的用户隐私设置，以及更高质量、更低功耗的基于位置的服务。Google Play 服务还会提升应用体验：加快离线搜索、提供更沉浸的地图与更好的游戏体验。",
      "source_location": "resources.arsc @7F0E001B（accessibilityservice.xml 的 android:description）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 无法运行，除非你启用 Google Play 服务。",
      "source_location": "resources.arsc（common_google_play_services_enable_text 系列多语种串，DEX 中可见该资源名引用）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Google Play services",
      "text_zh": "启用 Google Play 服务",
      "source_location": "resources.arsc（common_google_play_services_enable_title / enable_button）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't run without Google Play services, which are missing from your device.",
      "text_zh": "%1$s 无法运行，因为设备缺少 Google Play 服务。",
      "source_location": "resources.arsc（common_google_play_services_install_text 系列）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原（DEX 中无无障碍设置跳转常量，引导/拒权重试逻辑应由加密载荷提供；运行期需 UTG 观测是否 onResume 重跳或定时拉起）",
    "overlay_or_fake_settings": "静态侧未见悬浮窗引导代码；但已申请 SYSTEM_ALERT_WINDOW，且载荷为本地 WebView 页面，运行期可能叠放遮罩，需 UTG 验证",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=31，低于 33，静态无受限设置教学字符串）",
    "post_grant_anti_removal": "无（DEX 中无 GLOBAL_ACTION_BACK/HOME 相关静态字符串，服务实现不在 DEX 内，无法静态确认）",
    "benign_graceful_degradation": "无（无任何降级/手动模式/取消路径证据）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到应用进程启动（orkei.ti981.pay）后首次出现 WebView 加载本地 file:// 私有目录 index.html 的时刻；以及任何 Intent 指向 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（此时立即截图 + dump 无障碍服务列表项文案）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/释放后的本地 WebView 引导页",
        "page_identifier": "包名 orkei.ti981.pay 进程内 WebView，URL 为 file:///data/user/0/orkei.ti981.pay/app_*/... 指向释放出的 index.html",
        "why_most_useful": "该页承载全部伪装说明与「启用」按钮，是判断是否教唆开启无障碍与是否可取消的唯一直接证据",
        "observable_utg_signals": ["页面标题/正文是否出现 Google Play 服务、更新、认证等品牌文案", "是否存在「启用/开启/继续」主按钮而无取消/跳过控件", "是否出现指向无障碍设置的点击热区"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings.ACTION_ACCESSIBILITY_SETTINGS 页面中 label=Google services 的条目及其 description 展开",
        "why_most_useful": "确认系统层面呈现给用户的身份就是 Google services，构成品牌冒充的直接证据",
        "observable_utg_signals": ["列表项文本 Google services", "说明文本含 authentication/synchronized contacts 等 Google 官方措辞", "同列表内是否存在真实 Google Play 服务条目以比对"]
      },
      {
        "page_role": "跳转后压栈的遮罩/引导层",
        "page_identifier": "无障碍设置页之上叠加的悬浮窗（SYSTEM_ALERT_WINDOW）或全屏 Activity",
        "why_most_useful": "区分「仅跳转」与「叠层指引/伪造开关」两类诱导强度，是定级关键",
        "observable_utg_signals": ["设置页上层是否出现半透明遮罩或箭头指引", "是否绘制仿系统开关控件", "返回键行为是否被拦截"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：引导正文与服务工作类均不在静态 DEX，assets 53 个条目 ZIP 层加密，只能运行期抓取；若样本在一阶段仅做静默资产释放、需服务端/二次拉起才呈现引导页，冷启动短时 UTG 可能只看到空白或无界面；另需注意该应用无 LAUNCHER 入口，UTG 必须通过外部 Intent 或推送唤醒进程。"
  },
  "behavior_pattern_tags": [
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.dad.acquire.Rthingworld.attachBaseContext",
    "com.dad.acquire.Rthingworld.yellowjob",
    "res/xml/accessibilityservice.xml",
    "AndroidManifest.xml（service orkei.ti981.pay.ZNmNNvl7NO / activity dZ9jgilhHwzgNQKEdtB enabled=false）",
    "assets/www/index.html（加密）"
  ]
}
```

</details>
