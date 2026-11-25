# MB_080__d5ca7ba75c｜Ermac — HookAPP

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：141.3s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即用 WindowManager 全屏 WebView 把无障碍服务伪装成“Chrome Update Service”，跳转 ACCESSIBILITY_SETTINGS 后再压一层底部悬浮引导，并以 2s/3s Handler 循环无限重跳直至授权。
- **静态可见性说明**：无障碍服务类、Activity、Intent 跳转与 Handler 重试逻辑均在 DEX 中明文可见可完整还原；但两层 WebView 引导页的 HTML 正文来自 Base64 加密常量（zebajima.G 与 mitivucobiza 中的 Base64.decode），运行期解密后才渲染，静态无法读取具体话术；未发现远端 HTML 加载或加壳。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d5ca7ba75cfb8fd76929c1b8f6547780d8305a6654b6423124d380ff59b0d1c9` |
| 包名 / 年份 | `com.camavoyaxiwokocu.huvusuwi` / 2024 |
| 家族 / 品类 | **Ermac**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | HookAPP |
| 引导页宣称品牌/身份 | Chrome Update Service（Chrome 更新服务）；另有 10 个可动态启用的 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 图标与名称伪装 |
| 系统无障碍列表服务名 | HookAPPService |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍配置伪造 android:isAccessibilityTool="true"，冒充合规辅助工具以规避系统高风险提示；2) 桌面名 HookAPP 与页面宣称的 Chrome Update Service 完全不符；3) Manifest 预置 10 个 enabled=false 的 activity-alias，podi.t() 依据已安装包名动态 setComponentEnabledSetting 启用对应品牌图标与名称；4) 主 Activity 声明 noHistory=true、Translucent.NoTitleBar 主题，内容视图仅为单空格 TextView，返回键被改写，难以看出真实界面；5) 部分 Activity android:label="" 置空标签 |
| 无障碍服务类名 | `com.kedeluribeyisu.folowe.wesodahi.hofaxe` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | If accessibility permission has been on, please turn off then turn on. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.camavoyaxiwokocu.huvusuwi.podi（LAUNCHER，theme=@style/ACL，noHistory=true） | onCreate（含 try/catch 后再次执行引导分支）；onResume 回调至父类 zebajima.s() | 原生Activity | **原文**：textView.setText(" ")<br>**译注**：内容视图被设为一个仅含空格的 TextView，界面上不显示任何真实业务内容或说明文字 | 无显式请求，用户打开应用即被带入后续引导；无取消/跳过入口 | `com.camavoyaxiwokocu.huvusuwi.podi#onCreate` |
| 2 | 引导说明页 | WindowManager 全屏 WebView 悬浮层（zebajima.A），addJavascriptInterface(..., "Android")，WebSettings.setJavaScriptEnabled(true) | zebajima.s() 在 onResume 中被调用，且 v2.a.a(this) 判定无需先申请权限时进入 | 悬浮窗Overlay | **原文**：%Enable_Accessibility_Service% → "Chrome Update Service"（HTML 正文为 Base64 常量，运行期解密）<br>**译注**：以全屏网页形式展示“Chrome 更新服务”需要开启无障碍权限的说明与操作指引（正文话术静态不可见） | 引导用户在随后弹出的系统设置中开启名为 Chrome Update Service 的服务；页面无取消按钮，JS 桥 onData 仅用于关闭遮罩 | `com.kedeluribeyisu.folowe.zebajima#s；com.kedeluribeyisu.folowe.zebajima$g#onData` |
| 3 | 跳无障碍设置 | 系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS） | r1.d.c() 判定 hofaxe$b.P()==false（服务未启用）后调用 r1.d.b() | 系统无障碍页 | **原文**：new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(335544320)<br>**译注**：直接跳转到系统无障碍设置列表，列表项显示服务名 HookAPPService、描述“If accessibility permission has been on, please turn off then turn on.” | 要求用户在该列表中找到并开启 HookAPPService；系统页面本身可返回，但应用会立即重跳 | `r1.d#b` |
| 4 | 遮罩叠层指引 | com.kedeluribeyisu.folowe.fojocexago.mitivucobiza（theme=@style/ACL，noHistory=true，excludeFromRecents） | r1.d.b() 跳设置后立即 startActivity（FLAG_ACTIVITY_NEW_TASK；小米且 SDK≥29 时加 CLEAR_TASK\|NO_ANIMATION） | 悬浮窗Overlay | **原文**：WindowManager.LayoutParams(-1, -2, 2, 262152, -3)，gravity = 80；Base64.decode(...) 后按语言替换 <html lang="xx"><br>**译注**：在系统设置页之上叠一条贴底的半透明网页引导条，继续指示用户在页面上点选开关（正文话术为运行期解密的 Base64 HTML） | 在悬浮引导条指示下于系统设置页点击开关；引导层无取消/跳过按钮，仅 setOnClickListener 与 setOnTouchListener | `com.kedeluribeyisu.folowe.fojocexago.mitivucobiza#onCreate；mitivucobiza$a#shouldOverrideUrlLoading` |
| 5 | 拒权反馈循环 | Handler 轮询器 r1.b + Toast + 反复 startActivity(ACCESSIBILITY_SETTINGS) | r1.d.c() 中 handler.postDelayed(androidx.activity.b, 2000) 与 postDelayed(r1.b, 3000)；r1.b.run() 每轮重新检查 hofaxe$b.P() | 原生Dialog | **原文**：Toast.makeText(activity, "need accessibility service", 0).show()<br>**译注**：弹出“需要无障碍服务”的短提示，随后再次强制跳回系统无障碍设置页，未授权则每 3 秒无限重复 | 无选择权：不存在取消或跳过按钮，返回系统设置后由 onResume/Handler 重新拉起，形成死循环 | `r1.d#c；r1.b#run；androidx.activity.b#run` |
| 6 | 获权后动作 | com.kedeluribeyisu.folowe.wesodahi.hofaxe（无障碍服务，BIND_ACCESSIBILITY_SERVICE） | 服务被系统绑定后 onAccessibilityEvent 监听 com.android.settings.SubSettings / accessibilitysettingsactivity 等页面 | 不可静态还原 | 无 | 无（用户已授权，后续由服务自动执行） | `com.kedeluribeyisu.folowe.zebajima#r；com.kedeluribeyisu.folowe.wesodahi.hofaxe#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- podi 冷启动：WindowManager 全屏 WebView 悬浮层（LayoutParams -1/-1，zebajima.s()），HTML 为 Base64 常量解密，占位符替换为 Chrome Update Service
- 跳转系统设置后叠加的底部悬浮 WebView 引导条（mitivucobiza.onCreate，gravity=80，WindowManager 层 type=2）
- 系统无障碍服务列表项：label=HookAPPService，android:description=@string/text_accessibility_service_description（res/values/strings.xml:49）
- 循环阶段的 Toast 提示："need accessibility service"（androidx.activity.b#run 内硬编码）
- 桌面图标与名称：android:label="HookAPP"，以及 10 个可动态启用的 activity-alias 名称/图标（Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram、TikTok、Telegram）
- 主 Activity 内容视图被设为单空格 TextView（textView.setText(" ")），界面上不呈现任何说明文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开启过，请先关闭再重新开启。 | `res/values/strings.xml:49 key=text_accessibility_service_description（被 res/xml/vayeha.xml 的 android:description 引用）` | 教唆忽视警告 |
| en | need accessibility service | 需要无障碍服务。 | `硬编码于 androidx.activity.b#run（由 r1.d.c 通过 Handler 每 2 秒投递）` | 故障恐吓 |
| en | Chrome Update Service | Chrome 更新服务 | `com.kedeluribeyisu.folowe.zebajima#s 中替换 %Enable_Accessibility_Service% 占位符的硬编码字符串` | 假更新 |
| en | HookAPP / HookAPPService | HookAPP（桌面名）/ HookAPPService（系统无障碍列表中的服务名） | `AndroidManifest.xml application android:label 与 service android:label` | 未知 |
| en | （Base64 加密的 HTML 引导正文，运行期解密渲染，静态不可见） | 引导网页正文内容未知，需运行期 UTG/截图捕获 | `com.kedeluribeyisu.folowe.zebajima.G（m3.e 常量）与 mitivucobiza.onCreate 内 Base64.decode 常量` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：r1.b.run() 每轮检查 hofaxe$b.P()：未授权则 postDelayed(this, 3000) 自我重投递；r1.d.c() 另以 postDelayed(2000) 弹 Toast "need accessibility service" 并再次调用 r1.d.b() 跳 ACCESSIBILITY_SETTINGS。用户从系统设置返回后 zebajima.onResume→s() 重新评估并再次叠加遮罩与跳转，构成 onResume + Handler 双重死循环。
- **遮罩叠层 / 高仿系统设置页**：两层 WindowManager 悬浮 WebView：全屏层（-1/-1，占满屏幕）+ 贴底引导条（-1/-2, gravity=80），均叠加在系统无障碍设置页之上；未发现高仿系统开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：有：无障碍服务 onAccessibilityEvent 监听 com.android.settings.SubSettings / com.android.settings.settings.accessibilitysettingsactivity / com.android.settings.applications.installedappdetailstop / deviceadminadd 等页面并按 "button1"/"action_button" 等控件执行点击；Manifest 另注册 HookAPPAdmin 设备管理器（BIND_DEVICE_ADMIN）与 PACKAGE_REMOVED/BOOT_COMPLETED 监听，用于阻止卸载与自启恢复。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（r1.d#b）的瞬间，或应用冷启动后 0–1 秒内 WindowManager.addView 注入 WebView 的时刻；两者任一触发即开始抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：盲区：两层引导页 HTML 正文为 Base64 常量，静态不可读，若运行期页面以图片或空文本渲染则 UTG 文本提取会缺失，需补截图/OCR；另应用会按 Build.MANUFACTURER（如 xiaomi）与 SDK 版本改变跳转 flags 与遮罩参数，不同设备上引导层表现可能不同；静态未加壳，不影响运行期 UTG。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动全屏引导层** | com.camavoyaxiwokocu.huvusuwi.podi 之上、WindowManager 全屏 WebView（无 Activity 标题、内容为网页渲染） | 此处是首次向用户展示诱导话术的界面，可判定是否以 Chrome Update Service 等第三方品牌名义索取无障碍权限 | WebView 渲染的标题/正文文本（含 Chrome Update Service 字样）；页面按钮文案（是否仅有“开启/下一步”而无取消）；页面语言是否随系统语言变化（多语言话术） |
| **系统无障碍设置页 + 底部压栈引导条** | android.settings.ACCESSIBILITY_SETTINGS 列表，其上叠加 mitivucobiza 的底部 WebView（WindowManager 悬浮层） | 同时可取得系统侧真实服务名/描述与应用侧引导话术，直接暴露 HookAPPService 与“Chrome 更新”身份不一致 | 列表项文本 HookAPPService 与描述 If accessibility permission has been on, please turn off then turn on.；底部悬浮条的指示文本与指向控件；悬浮条是否遮挡系统返回/开关控件 |
| **拒权循环观测页** | 从系统设置返回后的 Toast "need accessibility service" + 再次出现的无障碍设置页 | 验证不存在取消路径，构成强制诱导的客观证据 | Toast 文本与出现频次（约每 2–3 秒）；页面在无用户操作下自动回到 ACCESSIBILITY_SETTINGS 的次数 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.camavoyaxiwokocu.huvusuwi.podi#onCreate`
- `com.kedeluribeyisu.folowe.zebajima#s`
- `r1.d#b`
- `r1.d#c`
- `com.kedeluribeyisu.folowe.fojocexago.mitivucobiza#onCreate`
- `res/xml/vayeha.xml / res/values/strings.xml#L49`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**静态可见性：partial_dynamic_or_remote**。无障碍服务类、引导流程、跳转和重试逻辑全部为明文 DEX 代码，可完整还原；只有 WebView 引导页的 HTML 正文是 Base64 常量，在运行期解密后渲染，因此静态状态下读不到具体话术。

**权限引导链路（共 5 段，全部落在应用自身代码中）**

1. **冷启动即遮挡**：入口 [podi.onCreate](<resource-unit:#1.dex1 code:com.camavoyaxiwokocu.huvusuwi.podi#onCreate>) 只用一个内容为空格的 `TextView` 作为内容视图，没有任何真实业务界面；Activity 声明 `noHistory=true`、`Theme.Translucent.NoTitleBar`，`onBackPressed` 也被改写。
2. **全屏 WebView 悬浮层伪装**：[zebajima.s()](<resource-unit:#1.dex1 code:com.kedeluribeyisu.folowe.zebajima#s>) 用 `WindowManager` 添加一个全屏 `WebView`（`LayoutParams(-1,-1)`，启用 JS，并注入 `Android` 桥），并把 HTML 中 `%Enable_Accessibility_Service%` 替换为 **“Chrome Update Service”**——该伪装对象明确，不是应用自身的真实名称。
3. **跳转系统无障碍设置**：[r1.d.b()](<resource-unit:#1.dex1 code:r1.d#b>) 显式构造 `Intent("android.settings.ACCESSIBILITY_SETTINGS")`，添加 `FLAG_ACTIVITY_CLEAR_TOP|NEW_TASK` 后 `startActivity`。
4. **设置页之上再叠引导层**：同一方法随即以 `NEW_TASK`（小米 + SDK≥29 时追加 `CLEAR_TASK|NO_ANIMATION`）拉起 [mitivucobiza.onCreate](<resource-unit:#1.dex1 code:com.kedeluribeyisu.folowe.fojocexago.mitivucobiza#onCreate>)，在其 `onCreate` 中再次用 `WindowManager` 添加 **底部悬浮 WebView**（gravity=80），HTML 同样来自 Base64 常量，并按系统语言改写 `<html lang>`。
5. **拒权/返回后无限重跳**：[r1.d.c()](<resource-unit:#1.dex1 code:r1.d#c>) 组装 [r1.b.run()](<resource-unit:#1.dex1 code:r1.b#run>) 轮询器：未授权时 `postDelayed(2000)` 弹出 `Toast "need accessibility service"`，然后重新调用 `r1.d.b()`，再 `postDelayed(3000)` 自我重投递；`hofaxe$b.P()` 一旦返回 false，就永久循环，**没有取消或跳过路径**。

**伪装与权限面**

- [res/xml/vayeha.xml](<resource-unit:#1 file:res/xml/vayeha.xml>) 声明 `isAccessibilityTool="true"`（伪造“辅助工具”性质以降低系统警告），同时开启 `canRetrieveWindowContent`、`canRequestFilterKeyEvents`、`canPerformGestures`、`canTakeScreenshot`、`flagRetrieveInteractiveWindows`、`typeAllMask`——获取全局读屏、按键截获与截图能力。
- [strings.xml 第 49 行](<resource-unit:#1 file:res/values/strings.xml#L49>) 的无障碍描述为“If accessibility permission has been on, please turn off then turn on.”，教唆用户关闭再开启以触发服务重载。
- Manifest 中 10 个默认禁用、动态启用的 `activity-alias`（Chrome / Google Play / Telegram / WhatsApp / Facebook / Gmail / Contacts / Youtube / Instagram / TikTok），由 [podi.t()](<resource-unit:#1.dex1 code:com.camavoyaxiwokocu.huvusuwi.podi#t>) 按已安装包名 `setComponentEnabledSetting` 切换图标与名称，与“Chrome Update Service”话术形成一致的品牌冒用叙事。

**UTG 取证要点**：最关键的瞬间是 `podi` 启动后的第 0–2 秒（全屏 WebView 出现）以及 `ACCESSIBILITY_SETTINGS` 跳转后压栈的底部悬浮层；这两层都包含可被 UTG 直接读取的文本（“Chrome Update Service”、开关项、按钮），无需 OCR。盲区：HTML 正文为 Base64 常量，若页面以纯图片或空文本渲染，则需配合截图；静态加密不阻挡运行期 UTG。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍服务类、Activity、Intent 跳转与 Handler 重试逻辑均在 DEX 中明文可见可完整还原；但两层 WebView 引导页的 HTML 正文来自 Base64 加密常量（zebajima.G 与 mitivucobiza 中的 Base64.decode），运行期解密后才渲染，静态无法读取具体话术；未发现远端 HTML 加载或加壳。",
  "summary_one_liner": "冷启动即用 WindowManager 全屏 WebView 把无障碍服务伪装成“Chrome Update Service”，跳转 ACCESSIBILITY_SETTINGS 后再压一层底部悬浮引导，并以 2s/3s Handler 循环无限重跳直至授权。",
  "disguise_identity": {
    "app_display_name": "HookAPP",
    "claimed_brand_or_persona": "Chrome Update Service（Chrome 更新服务）；另有 10 个可动态启用的 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 图标与名称伪装",
    "a11y_service_label": "HookAPPService",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍配置伪造 android:isAccessibilityTool=\"true\"，冒充合规辅助工具以规避系统高风险提示；2) 桌面名 HookAPP 与页面宣称的 Chrome Update Service 完全不符；3) Manifest 预置 10 个 enabled=false 的 activity-alias，podi.t() 依据已安装包名动态 setComponentEnabledSetting 启用对应品牌图标与名称；4) 主 Activity 声明 noHistory=true、Translucent.NoTitleBar 主题，内容视图仅为单空格 TextView，返回键被改写，难以看出真实界面；5) 部分 Activity android:label=\"\" 置空标签"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.camavoyaxiwokocu.huvusuwi.podi（LAUNCHER，theme=@style/ACL，noHistory=true）",
      "trigger_event": "onCreate（含 try/catch 后再次执行引导分支）；onResume 回调至父类 zebajima.s()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "textView.setText(\" \")",
      "shown_text_zh": "内容视图被设为一个仅含空格的 TextView，界面上不显示任何真实业务内容或说明文字",
      "user_action_requested": "无显式请求，用户打开应用即被带入后续引导；无取消/跳过入口",
      "code_anchor": "com.camavoyaxiwokocu.huvusuwi.podi#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "WindowManager 全屏 WebView 悬浮层（zebajima.A），addJavascriptInterface(..., \"Android\")，WebSettings.setJavaScriptEnabled(true)",
      "trigger_event": "zebajima.s() 在 onResume 中被调用，且 v2.a.a(this) 判定无需先申请权限时进入",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "%Enable_Accessibility_Service% → \"Chrome Update Service\"（HTML 正文为 Base64 常量，运行期解密）",
      "shown_text_zh": "以全屏网页形式展示“Chrome 更新服务”需要开启无障碍权限的说明与操作指引（正文话术静态不可见）",
      "user_action_requested": "引导用户在随后弹出的系统设置中开启名为 Chrome Update Service 的服务；页面无取消按钮，JS 桥 onData 仅用于关闭遮罩",
      "code_anchor": "com.kedeluribeyisu.folowe.zebajima#s；com.kedeluribeyisu.folowe.zebajima$g#onData"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "r1.d.c() 判定 hofaxe$b.P()==false（服务未启用）后调用 r1.d.b()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(335544320)",
      "shown_text_zh": "直接跳转到系统无障碍设置列表，列表项显示服务名 HookAPPService、描述“If accessibility permission has been on, please turn off then turn on.”",
      "user_action_requested": "要求用户在该列表中找到并开启 HookAPPService；系统页面本身可返回，但应用会立即重跳",
      "code_anchor": "r1.d#b"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.kedeluribeyisu.folowe.fojocexago.mitivucobiza（theme=@style/ACL，noHistory=true，excludeFromRecents）",
      "trigger_event": "r1.d.b() 跳设置后立即 startActivity（FLAG_ACTIVITY_NEW_TASK；小米且 SDK≥29 时加 CLEAR_TASK|NO_ANIMATION）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "WindowManager.LayoutParams(-1, -2, 2, 262152, -3)，gravity = 80；Base64.decode(...) 后按语言替换 <html lang=\"xx\">",
      "shown_text_zh": "在系统设置页之上叠一条贴底的半透明网页引导条，继续指示用户在页面上点选开关（正文话术为运行期解密的 Base64 HTML）",
      "user_action_requested": "在悬浮引导条指示下于系统设置页点击开关；引导层无取消/跳过按钮，仅 setOnClickListener 与 setOnTouchListener",
      "code_anchor": "com.kedeluribeyisu.folowe.fojocexago.mitivucobiza#onCreate；mitivucobiza$a#shouldOverrideUrlLoading"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "Handler 轮询器 r1.b + Toast + 反复 startActivity(ACCESSIBILITY_SETTINGS)",
      "trigger_event": "r1.d.c() 中 handler.postDelayed(androidx.activity.b, 2000) 与 postDelayed(r1.b, 3000)；r1.b.run() 每轮重新检查 hofaxe$b.P()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Toast.makeText(activity, \"need accessibility service\", 0).show()",
      "shown_text_zh": "弹出“需要无障碍服务”的短提示，随后再次强制跳回系统无障碍设置页，未授权则每 3 秒无限重复",
      "user_action_requested": "无选择权：不存在取消或跳过按钮，返回系统设置后由 onResume/Handler 重新拉起，形成死循环",
      "code_anchor": "r1.d#c；r1.b#run；androidx.activity.b#run"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.kedeluribeyisu.folowe.wesodahi.hofaxe（无障碍服务，BIND_ACCESSIBILITY_SERVICE）",
      "trigger_event": "服务被系统绑定后 onAccessibilityEvent 监听 com.android.settings.SubSettings / accessibilitysettingsactivity 等页面",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务启用后遮罩层经 JS 桥 Android.onData 关闭（zebajima.r() removeView/destroy），转为后台监听系统设置页与应用安装事件",
      "user_action_requested": "无（用户已授权，后续由服务自动执行）",
      "code_anchor": "com.kedeluribeyisu.folowe.zebajima#r；com.kedeluribeyisu.folowe.wesodahi.hofaxe#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "podi 冷启动：WindowManager 全屏 WebView 悬浮层（LayoutParams -1/-1，zebajima.s()），HTML 为 Base64 常量解密，占位符替换为 Chrome Update Service",
    "跳转系统设置后叠加的底部悬浮 WebView 引导条（mitivucobiza.onCreate，gravity=80，WindowManager 层 type=2）",
    "系统无障碍服务列表项：label=HookAPPService，android:description=@string/text_accessibility_service_description（res/values/strings.xml:49）",
    "循环阶段的 Toast 提示：\"need accessibility service\"（androidx.activity.b#run 内硬编码）",
    "桌面图标与名称：android:label=\"HookAPP\"，以及 10 个可动态启用的 activity-alias 名称/图标（Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram、TikTok、Telegram）",
    "主 Activity 内容视图被设为单空格 TextView（textView.setText(\" \")），界面上不呈现任何说明文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开启过，请先关闭再重新开启。",
      "source_location": "res/values/strings.xml:49 key=text_accessibility_service_description（被 res/xml/vayeha.xml 的 android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "need accessibility service",
      "text_zh": "需要无障碍服务。",
      "source_location": "硬编码于 androidx.activity.b#run（由 r1.d.c 通过 Handler 每 2 秒投递）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Chrome Update Service",
      "text_zh": "Chrome 更新服务",
      "source_location": "com.kedeluribeyisu.folowe.zebajima#s 中替换 %Enable_Accessibility_Service% 占位符的硬编码字符串",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "HookAPP / HookAPPService",
      "text_zh": "HookAPP（桌面名）/ HookAPPService（系统无障碍列表中的服务名）",
      "source_location": "AndroidManifest.xml application android:label 与 service android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "（Base64 加密的 HTML 引导正文，运行期解密渲染，静态不可见）",
      "text_zh": "引导网页正文内容未知，需运行期 UTG/截图捕获",
      "source_location": "com.kedeluribeyisu.folowe.zebajima.G（m3.e 常量）与 mitivucobiza.onCreate 内 Base64.decode 常量",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "r1.b.run() 每轮检查 hofaxe$b.P()：未授权则 postDelayed(this, 3000) 自我重投递；r1.d.c() 另以 postDelayed(2000) 弹 Toast \"need accessibility service\" 并再次调用 r1.d.b() 跳 ACCESSIBILITY_SETTINGS。用户从系统设置返回后 zebajima.onResume→s() 重新评估并再次叠加遮罩与跳转，构成 onResume + Handler 双重死循环。",
    "overlay_or_fake_settings": "两层 WindowManager 悬浮 WebView：全屏层（-1/-1，占满屏幕）+ 贴底引导条（-1/-2, gravity=80），均叠加在系统无障碍设置页之上；未发现高仿系统开关页。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "有：无障碍服务 onAccessibilityEvent 监听 com.android.settings.SubSettings / com.android.settings.settings.accessibilitysettingsactivity / com.android.settings.applications.installedappdetailstop / deviceadminadd 等页面并按 \"button1\"/\"action_button\" 等控件执行点击；Manifest 另注册 HookAPPAdmin 设备管理器（BIND_DEVICE_ADMIN）与 PACKAGE_REMOVED/BOOT_COMPLETED 监听，用于阻止卸载与自启恢复。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（r1.d#b）的瞬间，或应用冷启动后 0–1 秒内 WindowManager.addView 注入 WebView 的时刻；两者任一触发即开始抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动全屏引导层",
        "page_identifier": "com.camavoyaxiwokocu.huvusuwi.podi 之上、WindowManager 全屏 WebView（无 Activity 标题、内容为网页渲染）",
        "why_most_useful": "此处是首次向用户展示诱导话术的界面，可判定是否以 Chrome Update Service 等第三方品牌名义索取无障碍权限",
        "observable_utg_signals": ["WebView 渲染的标题/正文文本（含 Chrome Update Service 字样）", "页面按钮文案（是否仅有“开启/下一步”而无取消）", "页面语言是否随系统语言变化（多语言话术）"]
      },
      {
        "page_role": "系统无障碍设置页 + 底部压栈引导条",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 列表，其上叠加 mitivucobiza 的底部 WebView（WindowManager 悬浮层）",
        "why_most_useful": "同时可取得系统侧真实服务名/描述与应用侧引导话术，直接暴露 HookAPPService 与“Chrome 更新”身份不一致",
        "observable_utg_signals": ["列表项文本 HookAPPService 与描述 If accessibility permission has been on, please turn off then turn on.", "底部悬浮条的指示文本与指向控件", "悬浮条是否遮挡系统返回/开关控件"]
      },
      {
        "page_role": "拒权循环观测页",
        "page_identifier": "从系统设置返回后的 Toast \"need accessibility service\" + 再次出现的无障碍设置页",
        "why_most_useful": "验证不存在取消路径，构成强制诱导的客观证据",
        "observable_utg_signals": ["Toast 文本与出现频次（约每 2–3 秒）", "页面在无用户操作下自动回到 ACCESSIBILITY_SETTINGS 的次数"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "盲区：两层引导页 HTML 正文为 Base64 常量，静态不可读，若运行期页面以图片或空文本渲染则 UTG 文本提取会缺失，需补截图/OCR；另应用会按 Build.MANUFACTURER（如 xiaomi）与 SDK 版本改变跳转 flags 与遮罩参数，不同设备上引导层表现可能不同；静态未加壳，不影响运行期 UTG。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.camavoyaxiwokocu.huvusuwi.podi#onCreate",
    "com.kedeluribeyisu.folowe.zebajima#s",
    "r1.d#b",
    "r1.d#c",
    "com.kedeluribeyisu.folowe.fojocexago.mitivucobiza#onCreate",
    "res/xml/vayeha.xml / res/values/strings.xml#L49"
  ]
}
```

</details>
