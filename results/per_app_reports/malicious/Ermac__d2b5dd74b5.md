# MB_086__d2b5dd74b5｜Ermac — HookAPP

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：140.4s

## 1. 一句话核心结论

- **核心申请方式**：冷启动无界面即拉起系统无障碍设置页，并在其上叠加远端 Base64 HTML 引导遮罩（伪称 Chrome 更新服务），用户返回后每 3 秒重跳形成死循环，授权瞬间由无障碍服务自己点击开关完成开启。
- **静态可见性说明**：跳转点(ACTION_ACCESSIBILITY_SETTINGS)、2s/3s 重试循环、设置页压栈遮罩 WebView、服务自点击开关、10 个 activity-alias 图标伪装、isAccessibilityTool=true 均静态完整可见；引导页面 HTML 本体不在包内（assets 仅有 dexopt 空目录），由远端配置 viyeregika.G/viyeregika.H 取回后 Base64 解码并 loadDataWithBaseURL 渲染，仅可见占位符 %Enable_Accessibility_Service% 被替换为 'Chrome Update Service' 及 i3.h.w 的多语言 Enable 词表，逐字引导文案需运行期抓取。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d2b5dd74b5950953028cabf5d62c40366b14a2e803fb091500c6b6826f03f95e` |
| 包名 / 年份 | `com.zejapizehiyuki.yijoro` / 2024 |
| 家族 / 品类 | **Ermac**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | HookAPP |
| 引导页宣称品牌/身份 | Chrome Update Service（引导页与设置页内文本均以此名义出现）；桌面图标按已安装应用动态伪装成 Telegram / Facebook / TikTok / Instagram / Chrome / YouTube / Google Play / Gmail / WhatsApp / Contacts |
| 系统无障碍列表服务名 | HookAPPService |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍配置 android:isAccessibilityTool="true" 伪造系统辅助功能工具属性，规避 Android 13+ 受限设置拦截；2) android:description 为误导性话术 "If accessibility permission has been on, please turn off then turn on."，不含任何真实用途说明；3) 10 个 activity-alias 全部 enabled="false" 且共用 targetActivity，运行期按已安装包 setComponentEnabledSetting 逐一启用，实现桌面名/图标变脸；4) 多个导出 Activity 声明 android:label=""（空标签）与 Theme.NoDisplay 隐藏界面；5) 应用级 android:label="HookAPP" 与引导页宣称的 Chrome 更新服务完全不符；6) 启动 Activity 用空白 TextView 顶替真实界面。 |
| 无障碍服务类名 | `com.fedozojaforo.valeso.gukupuga.kanenovewuceba` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.zejapizehiyuki.yijoro.gojonamopi（MAIN/LAUNCHER，Theme.Translucent.NoTitleBar，noHistory） | onCreate：setContentView(new TextView(" ")) 后按 viyeregika$d.b() 分流调用 v()/w()/r() | 原生Activity | 仅一个空白字符的 TextView，用户看到近似空白页 | 无任何可操作控件，无取消/跳过入口；界面随即被后续流程替换 | `com.zejapizehiyuki.yijoro.gojonamopi.onCreate` |
| 2 | 业务功能触发 | PackageManager.setComponentEnabledSetting → 对应 activity-alias（Telegram/Facebook/TikTok/Instagram/Chrome/YouTube 等） | gojonamopi.t() 检测到 com.android.chrome 等目标应用已安装即启用同名别名 | 原生Activity | **原文**：Chrome / Facebook / Telegram / TikTok / Instagram / Youtube / Google Play / Gmail / WhatsApp / Contacts<br>**译注**：桌面图标与名称被替换为受害应用的同名同图标别名 | 诱使用户认为点击的是真实常用应用图标 | `com.zejapizehiyuki.yijoro.gojonamopi.t / AndroidManifest.xml activity-alias` |
| 3 | 跳无障碍设置 | 系统页 android.settings.ACCESSIBILITY_SETTINGS | i3.f.b() 由 i3.f.c() 经 Handler.postDelayed(2000ms) 触发，startActivity(FLAG_ACTIVITY_NEW_TASK\|FLAG_ACTIVITY_CLEAR_TOP=335544320) | 系统无障碍页 | 无 | 要求用户在系统无障碍列表中找到并开启对应服务（列表项显示 HookAPPService） | `i3.f.b` |
| 4 | 遮罩叠层指引 | com.fedozojaforo.valeso.foxugovixo.jokaju（WebView 通过 WindowManager.addView 叠加，LayoutParams(-1,-2,type=2,flags=262152), gravity=80） | i3.f.b() 在 startActivity 设置页后立即 startActivity(jokaju)，onCreate 中 Base64.decode(viyeregika.H.a()) 并 loadDataWithBaseURL | 远端WebView | **原文**：HTML 模板含占位 %Enable_Accessibility_Service%（远端下发，本地仅可见占位符）；<html lang="en"> 被替换为本机语言<br>**译注**：远端下发的底部悬浮引导条，语言随设备切换，文案本体仅在运行期可见 | WebView 设置 setOnClickListener/setOnTouchListener，用户点击引导条即被引导操作；无取消按钮 | `com.fedozojaforo.valeso.foxugovixo.jokaju.onCreate` |
| 5 | 引导说明页 | com.fedozojaforo.valeso.viyeregika（window setType(2006) 系统级悬浮窗，全屏 WebView LayoutParams(-1,-1,type=2,flags=262144)，addJavascriptInterface(...,"Android")） | viyeregika.s() 在 z==true 分支执行 Base64.decode(viyeregika.G.a()) → 字符串替换 %Enable_Accessibility_Service% → loadDataWithBaseURL | 远端WebView | **原文**：Chrome Update Service（替换进远端 HTML 的服务名占位符）<br>**译注**：全屏远端 HTML 教学页，宣称需要开启「Chrome Update Service」的无障碍权限 | 通过 JS 桥 Android 接口与页面按钮引导用户前往无障碍设置开启服务；页面无退出/取消入口，onData 回调后移除视图 | `com.fedozojaforo.valeso.viyeregika.s` |
| 6 | 拒权反馈循环 | Handler 定时器 + Toast | i3.f.c(Activity) 中 postDelayed(q.a, 3000) 递归回调自身；androidx.activity.b.run 弹 Toast | 系统无障碍页 | **原文**：need accessibility service<br>**译注**：「需要无障碍服务」提示条，并在用户返回后每 3 秒重新拉起无障碍设置页 | 不提供取消/跳过，用户无法通过返回键退出引导流程 | `i3.f.c / androidx.activity.b.run` |
| 7 | 获权后动作 | com.fedozojaforo.valeso.gukupuga.kanenovewuceba（BIND_ACCESSIBILITY_SERVICE） | onAccessibilityEvent → i()：className 匹配 com.android.settings.SubSettings 且 text/contentDescription 含 "Chrome Update Service" 时调用 kanenovewuceba$b.r() 自动点击开关；30 秒节流 | 系统无障碍页 | **原文**：Chrome Update Service<br>**译注**：服务自己识别设置页上的开关项文本并代为点击，用户尚未操作即完成开启；onServiceConnected 后移除引导视图并转入后台控制 | 无需用户确认，服务自动完成开关点击与授权 | `com.fedozojaforo.valeso.gukupuga.kanenovewuceba.i / onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表项名称：Manifest 中 service android:label="HookAPPService"
- 系统无障碍列表项说明：res/xml/covovido.xml 引用 res/values/strings.xml:49 text_accessibility_service_description = "If accessibility permission has been on, please turn off then turn on."
- 系统无障碍设置页之上的底部悬浮 WebView 引导条：com.fedozojaforo.valeso.foxugovixo.jokaju.onCreate（远端 Base64 HTML，gravity=80）
- 系统无障碍设置页之上的全屏远端 WebView 教学页：com.fedozojaforo.valeso.viyeregika.s（type=2006 悬浮窗，含 "Chrome Update Service" 替换文本）
- Toast 催促提示：androidx.activity.b.run 硬编码 "need accessibility service"
- 桌面图标/名称位置：10 个 activity-alias（Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram），运行期 setComponentEnabledSetting 逐个启用
- 启动 Activity 空白占位：com.zejapizehiyuki.yijoro.gojonamopi.onCreate 的 TextView(" ")，不呈现任何说明文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开着，请先关闭再重新打开。 | `res/values/strings.xml key=text_accessibility_service_description（被 res/xml/covovido.xml android:description 引用）` | 教唆忽视警告 |
| en | Chrome Update Service | Chrome 更新服务 | `com.fedozojaforo.valeso.viyeregika#s 中替换远端 HTML 占位符 %Enable_Accessibility_Service%；亦用于 gukupuga.kanenovewuceba#i 的节点匹配` | 假更新 |
| en | need accessibility service | 需要无障碍服务 | `androidx.activity.b#run 硬编码 Toast.makeText` | 未知 |
| zh | 启用 | 启用（页面「开启」按钮文案，来自多语言映射表） | `i3.h#w 常量 {'en':'Enable',...,'zh':'启用',...,'ru':'Включить',...}` | 受限设置分步教学 |
| en | %Enable_Accessibility_Service% | 无障碍服务名占位符（运行期被替换为 Chrome Update Service） | `com.fedozojaforo.valeso.viyeregika#s；HTML 模板位于远端配置 viyeregika.G（Base64）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：i3.f.c 先 Handler.postDelayed(2000ms) 跳无障碍设置，再 postDelayed(q.a, 3000ms) 每 3 秒回调自身重新 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；返回键无效，另以 Toast("need accessibility service") 持续催促，形成无退出条件的重跳循环
- **遮罩叠层 / 高仿系统设置页**：两层叠放：jokaju 的底部悬浮 WebView 引导条（type=2、flags=262152、gravity=80）与 viyeregika 的全屏系统级悬浮窗（window setType(2006)、WebView LayoutParams(-1,-1)），均压在系统无障碍设置页之上；不含高仿系统开关页，但遮挡真实页面文本
- **Android 13+ 受限设置（Restricted Settings）应对**：未见「进应用详情→右上角菜单→允许受限设置」的分步教学；改为用 covovido.xml 中 android:isAccessibilityTool="true" 伪造辅助功能工具身份，从系统层面绕过受限设置提示
- **获权后即时行为与防撤权机制**：onAccessibilityEvent 中 i() 检测到 com.android.settings.SubSettings 页面且节点文本含 "Chrome Update Service" 时，由服务自身调用 kanenovewuceba$b.r() 自动点击开关完成开启（30 秒节流）；未发现用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑，另有 DeviceAdmin 接收器与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 用于驻留
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到应用 startActivity("android.settings.ACCESSIBILITY_SETTINGS") 的瞬间，或冷启动 com.zejapizehiyuki.yijoro.gojonamopi 后约 2 秒（i3.f.c 首次 postDelayed 到期）拉起 UTG；此后每 3 秒重跳一次，可稳定复现
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区是引导文案位于远端 HTML：静态不可见，需依赖运行期 UTG/流量抓取才能获得逐字文本；若设备断网或远端配置为空（viyeregika.H/G 长度为 0），应用只做裸跳设置页而不显示引导层，UTG 仅能看到系统无障碍页，容易误判为无诱导。此外桌面图标伪装依赖已安装应用存在，纯净测试机上可能不触发别名切换。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳设置后压栈的底部悬浮引导条** | com.fedozojaforo.valeso.foxugovixo.jokaju 的 WebView（type=2 悬浮窗、gravity=80、高度 -2），内容为远端 Base64 HTML | 这是唯一一处对用户直接可见的引导文案，且文案完全来自远端下发，静态无法获得，是判定诱导话术性质的决定性页面 | WebView 节点树中的 HTML 文本与按钮文案（含多语言 Enable 按钮）；悬浮窗与系统设置页的层级叠压关系；页面 lang 是否已替换为设备语言 |
| **全屏远端教学页** | com.fedozojaforo.valeso.viyeregika 全屏 WebView（window type=2006） | 该页把服务名伪装为 Chrome Update Service，直接体现品牌冒用与假更新话术 | 页面中出现的 "Chrome Update Service" 字样；是否存在跳转按钮/箭头指引与 JS 桥调用；页面是否覆盖全屏且无关闭控件 |
| **系统无障碍服务列表项** | com.android.settings SubSettings 页中的 "HookAPPService" 条目及其说明文字 | 验证服务标签、误导性 description 与实际应用名 HookAPP 的身份错配，并可观察服务是否自行点击开关 | 列表项文本 HookAPPService 与 description 原文；开关在用户未操作时是否自动切换；页面停留时长与 3 秒重跳频次 |
| **冷启动空白占位页** | com.zejapizehiyuki.yijoro.gojonamopi（Theme.Translucent.NoTitleBar，TextView(" ")） | 确认应用在 0 步内即触发引导，无任何功能页或说明页作为前置，属最激进的诱导时序 | 冷启动到跳设置页的时间差（≈2s）；界面节点数极少（近乎空白） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `i3.f.b`
- `i3.f.c`
- `com.fedozojaforo.valeso.foxugovixo.jokaju.onCreate`
- `com.fedozojaforo.valeso.viyeregika.s`
- `com.fedozojaforo.valeso.gukupuga.kanenovewuceba.i`
- `res/xml/covovido.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，纯运行期 UTG 视角）

**核心机制已静态还原**：这是一个 Ermac 系样本，引导链完全围绕“远程 HTML 引导层 + 系统无障碍设置页 + 服务自点击”构建，文字不在本地 assets 中，而是从远端配置取 Base64 HTML。

**逐步流转**：

1. **冷启动即触发，无可见界面**：[gojonamopi.onCreate()](<resource-unit:#1.dex1 code:com.zejapizehiyuki.yijoro.gojonamopi#onCreate>) 用 `setContentView(new TextView(" "))` 铺一个空白 TextView，窗口 `setFlags(32/262144)` 保持常亮、不锁屏，随即走 `viyeregika$d.b()` 判断后调用 `v()`/`r()`/`w()`，无任何用户可理解的入口页。
2. **图标身份动态伪装**：同一 `onCreate` 链上 [gojonamopi.t()](<resource-unit:#1.dex1 code:com.zejapizehiyuki.yijoro.gojonamopi#t>) 依据 `org.telegram.messenger`、`com.facebook.katana`、`com.zhiliaoapp.musically`、`com.instagram.android`、`com.android.chrome`、`com.google.android.youtube` 等是否安装，调用 `setComponentEnabledSetting(..., 1, 1)` 启用对应 `activity-alias`（Manifest 中 Facebook / Google Play / Gmail / WhatsApp / YouTube / Chrome / Instagram / TikTok / Telegram 共 10 个别名，默认 `enabled="false"`），桌面名与图标变为受害目标 App。
3. **跳转无障碍设置**：[i3.f.b()](<resource-unit:#1.dex1 code:i3.f#b>) 直接 `new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(335544320)` 并 `startActivity`，紧接着若远端配置 `viyeregika.H` 非空，再以 `FLAG_ACTIVITY_NEW_TASK|...` 拉起 [jokaju](<resource-unit:#1.dex1 code:com.fedozojaforo.valeso.foxugovixo.jokaju#onCreate>) 引导层；对小米设备额外叠加 `131072`/`8388608` 标志以压栈。
4. **设置页之上压一层底部 WebView 引导条**：`jokaju.onCreate` 用 `WindowManager.addView` 挂 `LayoutParams(-1,-2, 2, 262152)`、`gravity=80` 的 WebView，内容为 `Base64.decode(viyeregika.H.a())` 的远端 HTML，并把 `<html lang="en">` 替换成本机语言（`i3.h.d/e/f`）。
5. **全屏远端引导页**：[viyeregika.s()](<resource-unit:#1.dex1 code:com.fedozojaforo.valeso.viyeregika#s>) 走 `z==true` 分支，创建开启 JS、`addJavascriptInterface(new viyeregika$g(...), "Android")` 的全屏 WebView（`LayoutParams(-1,-1, 2, 262144)`），HTML 来自 `Base64.decode(viyeregika.G.a())`，并把占位符 `%Enable_Accessibility_Service%` 替换为 **"Chrome Update Service"**。
6. **拒权/返回后死循环重跳**：[i3.f.c(Activity)](<resource-unit:#1.dex1 code:i3.f#c>) 用 `Handler.postDelayed(..., 2000)` 延迟 2 秒调 `b()` 跳设置页，再 `postDelayed(q.a, 3000)` 每 3 秒回调 `f.c` 重来一次，无取消路径；同时 `androidx.activity.b.run` 弹 `Toast("need accessibility service")` 持续催促。
7. **获权后自点击确认**：[kanenovewuceba.i()](<resource-unit:#1.dex1 code:com.fedozojaforo.valeso.gukupuga.kanenovewuceba#i>) 在 `onAccessibilityEvent` 中判定当前页 `className == "com.android.settings.SubSettings"` 且 text/contentDescription 含 `"Chrome Update Service"`，即调用 `kanenovewuceba$b.r()` 由无障碍服务自己点击开关完成授权（30 秒节流）。

**身份伪造点**：桌面名 `HookAPP`、无障碍服务标签 `HookAPPService`、`android:label=""` 的多个 Activity、`android:description` 是一句语焉不详的 `If accessibility permission has been on, please turn off then turn on.`，同时 [covovido.xml](<resource-unit:#1 file:res/xml/covovido.xml>) 里 `android:isAccessibilityTool="true"` 伪造“辅助功能工具”属性以规避 Android 13+ 受限设置提示；`canTakeScreenshot`/`canPerformGestures`/`flagRequestFilterKeyEvents` 全部打开。

**静态可见性**：跳转点、重试循环、自点击逻辑、图标伪装全部静态可见；**引导文案本体不可见**——`i3.h` 中除 Base64 常量与多语言 `Enable` 词表（`{'en':'Enable',...,'zh':'启用',...}`）外无任何引导句，HTML 由远端配置下发后解码渲染，故文案逐字内容需动态抓取。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "跳转点(ACTION_ACCESSIBILITY_SETTINGS)、2s/3s 重试循环、设置页压栈遮罩 WebView、服务自点击开关、10 个 activity-alias 图标伪装、isAccessibilityTool=true 均静态完整可见；引导页面 HTML 本体不在包内（assets 仅有 dexopt 空目录），由远端配置 viyeregika.G/viyeregika.H 取回后 Base64 解码并 loadDataWithBaseURL 渲染，仅可见占位符 %Enable_Accessibility_Service% 被替换为 'Chrome Update Service' 及 i3.h.w 的多语言 Enable 词表，逐字引导文案需运行期抓取。",
  "summary_one_liner": "冷启动无界面即拉起系统无障碍设置页，并在其上叠加远端 Base64 HTML 引导遮罩（伪称 Chrome 更新服务），用户返回后每 3 秒重跳形成死循环，授权瞬间由无障碍服务自己点击开关完成开启。",
  "disguise_identity": {
    "app_display_name": "HookAPP",
    "claimed_brand_or_persona": "Chrome Update Service（引导页与设置页内文本均以此名义出现）；桌面图标按已安装应用动态伪装成 Telegram / Facebook / TikTok / Instagram / Chrome / YouTube / Google Play / Gmail / WhatsApp / Contacts",
    "a11y_service_label": "HookAPPService",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍配置 android:isAccessibilityTool=\"true\" 伪造系统辅助功能工具属性，规避 Android 13+ 受限设置拦截；2) android:description 为误导性话术 \"If accessibility permission has been on, please turn off then turn on.\"，不含任何真实用途说明；3) 10 个 activity-alias 全部 enabled=\"false\" 且共用 targetActivity，运行期按已安装包 setComponentEnabledSetting 逐一启用，实现桌面名/图标变脸；4) 多个导出 Activity 声明 android:label=\"\"（空标签）与 Theme.NoDisplay 隐藏界面；5) 应用级 android:label=\"HookAPP\" 与引导页宣称的 Chrome 更新服务完全不符；6) 启动 Activity 用空白 TextView 顶替真实界面。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.zejapizehiyuki.yijoro.gojonamopi（MAIN/LAUNCHER，Theme.Translucent.NoTitleBar，noHistory）",
      "trigger_event": "onCreate：setContentView(new TextView(\" \")) 后按 viyeregika$d.b() 分流调用 v()/w()/r()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": " ",
      "shown_text_zh": "仅一个空白字符的 TextView，用户看到近似空白页",
      "user_action_requested": "无任何可操作控件，无取消/跳过入口；界面随即被后续流程替换",
      "code_anchor": "com.zejapizehiyuki.yijoro.gojonamopi.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "PackageManager.setComponentEnabledSetting → 对应 activity-alias（Telegram/Facebook/TikTok/Instagram/Chrome/YouTube 等）",
      "trigger_event": "gojonamopi.t() 检测到 com.android.chrome 等目标应用已安装即启用同名别名",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Chrome / Facebook / Telegram / TikTok / Instagram / Youtube / Google Play / Gmail / WhatsApp / Contacts",
      "shown_text_zh": "桌面图标与名称被替换为受害应用的同名同图标别名",
      "user_action_requested": "诱使用户认为点击的是真实常用应用图标",
      "code_anchor": "com.zejapizehiyuki.yijoro.gojonamopi.t / AndroidManifest.xml activity-alias"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "i3.f.b() 由 i3.f.c() 经 Handler.postDelayed(2000ms) 触发，startActivity(FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TOP=335544320)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳转至系统「已下载的服务/无障碍」列表页",
      "user_action_requested": "要求用户在系统无障碍列表中找到并开启对应服务（列表项显示 HookAPPService）",
      "code_anchor": "i3.f.b"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.fedozojaforo.valeso.foxugovixo.jokaju（WebView 通过 WindowManager.addView 叠加，LayoutParams(-1,-2,type=2,flags=262152), gravity=80）",
      "trigger_event": "i3.f.b() 在 startActivity 设置页后立即 startActivity(jokaju)，onCreate 中 Base64.decode(viyeregika.H.a()) 并 loadDataWithBaseURL",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "HTML 模板含占位 %Enable_Accessibility_Service%（远端下发，本地仅可见占位符）；<html lang=\"en\"> 被替换为本机语言",
      "shown_text_zh": "远端下发的底部悬浮引导条，语言随设备切换，文案本体仅在运行期可见",
      "user_action_requested": "WebView 设置 setOnClickListener/setOnTouchListener，用户点击引导条即被引导操作；无取消按钮",
      "code_anchor": "com.fedozojaforo.valeso.foxugovixo.jokaju.onCreate"
    },
    {
      "step": 5,
      "stage": "引导说明页",
      "screen_or_component": "com.fedozojaforo.valeso.viyeregika（window setType(2006) 系统级悬浮窗，全屏 WebView LayoutParams(-1,-1,type=2,flags=262144)，addJavascriptInterface(...,\"Android\")）",
      "trigger_event": "viyeregika.s() 在 z==true 分支执行 Base64.decode(viyeregika.G.a()) → 字符串替换 %Enable_Accessibility_Service% → loadDataWithBaseURL",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "Chrome Update Service（替换进远端 HTML 的服务名占位符）",
      "shown_text_zh": "全屏远端 HTML 教学页，宣称需要开启「Chrome Update Service」的无障碍权限",
      "user_action_requested": "通过 JS 桥 Android 接口与页面按钮引导用户前往无障碍设置开启服务；页面无退出/取消入口，onData 回调后移除视图",
      "code_anchor": "com.fedozojaforo.valeso.viyeregika.s"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "Handler 定时器 + Toast",
      "trigger_event": "i3.f.c(Activity) 中 postDelayed(q.a, 3000) 递归回调自身；androidx.activity.b.run 弹 Toast",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "need accessibility service",
      "shown_text_zh": "「需要无障碍服务」提示条，并在用户返回后每 3 秒重新拉起无障碍设置页",
      "user_action_requested": "不提供取消/跳过，用户无法通过返回键退出引导流程",
      "code_anchor": "i3.f.c / androidx.activity.b.run"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.fedozojaforo.valeso.gukupuga.kanenovewuceba（BIND_ACCESSIBILITY_SERVICE）",
      "trigger_event": "onAccessibilityEvent → i()：className 匹配 com.android.settings.SubSettings 且 text/contentDescription 含 \"Chrome Update Service\" 时调用 kanenovewuceba$b.r() 自动点击开关；30 秒节流",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Chrome Update Service",
      "shown_text_zh": "服务自己识别设置页上的开关项文本并代为点击，用户尚未操作即完成开启；onServiceConnected 后移除引导视图并转入后台控制",
      "user_action_requested": "无需用户确认，服务自动完成开关点击与授权",
      "code_anchor": "com.fedozojaforo.valeso.gukupuga.kanenovewuceba.i / onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表项名称：Manifest 中 service android:label=\"HookAPPService\"",
    "系统无障碍列表项说明：res/xml/covovido.xml 引用 res/values/strings.xml:49 text_accessibility_service_description = \"If accessibility permission has been on, please turn off then turn on.\"",
    "系统无障碍设置页之上的底部悬浮 WebView 引导条：com.fedozojaforo.valeso.foxugovixo.jokaju.onCreate（远端 Base64 HTML，gravity=80）",
    "系统无障碍设置页之上的全屏远端 WebView 教学页：com.fedozojaforo.valeso.viyeregika.s（type=2006 悬浮窗，含 \"Chrome Update Service\" 替换文本）",
    "Toast 催促提示：androidx.activity.b.run 硬编码 \"need accessibility service\"",
    "桌面图标/名称位置：10 个 activity-alias（Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram），运行期 setComponentEnabledSetting 逐个启用",
    "启动 Activity 空白占位：com.zejapizehiyuki.yijoro.gojonamopi.onCreate 的 TextView(\" \")，不呈现任何说明文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开着，请先关闭再重新打开。",
      "source_location": "res/values/strings.xml key=text_accessibility_service_description（被 res/xml/covovido.xml android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Chrome Update Service",
      "text_zh": "Chrome 更新服务",
      "source_location": "com.fedozojaforo.valeso.viyeregika#s 中替换远端 HTML 占位符 %Enable_Accessibility_Service%；亦用于 gukupuga.kanenovewuceba#i 的节点匹配",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "need accessibility service",
      "text_zh": "需要无障碍服务",
      "source_location": "androidx.activity.b#run 硬编码 Toast.makeText",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "启用",
      "text_zh": "启用（页面「开启」按钮文案，来自多语言映射表）",
      "source_location": "i3.h#w 常量 {'en':'Enable',...,'zh':'启用',...,'ru':'Включить',...}",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "%Enable_Accessibility_Service%",
      "text_zh": "无障碍服务名占位符（运行期被替换为 Chrome Update Service）",
      "source_location": "com.fedozojaforo.valeso.viyeregika#s；HTML 模板位于远端配置 viyeregika.G（Base64）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "i3.f.c 先 Handler.postDelayed(2000ms) 跳无障碍设置，再 postDelayed(q.a, 3000ms) 每 3 秒回调自身重新 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；返回键无效，另以 Toast(\"need accessibility service\") 持续催促，形成无退出条件的重跳循环",
    "overlay_or_fake_settings": "两层叠放：jokaju 的底部悬浮 WebView 引导条（type=2、flags=262152、gravity=80）与 viyeregika 的全屏系统级悬浮窗（window setType(2006)、WebView LayoutParams(-1,-1)），均压在系统无障碍设置页之上；不含高仿系统开关页，但遮挡真实页面文本",
    "restricted_settings_13plus_coaching": "未见「进应用详情→右上角菜单→允许受限设置」的分步教学；改为用 covovido.xml 中 android:isAccessibilityTool=\"true\" 伪造辅助功能工具身份，从系统层面绕过受限设置提示",
    "post_grant_anti_removal": "onAccessibilityEvent 中 i() 检测到 com.android.settings.SubSettings 页面且节点文本含 \"Chrome Update Service\" 时，由服务自身调用 kanenovewuceba$b.r() 自动点击开关完成开启（30 秒节流）；未发现用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑，另有 DeviceAdmin 接收器与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 用于驻留",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到应用 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\") 的瞬间，或冷启动 com.zejapizehiyuki.yijoro.gojonamopi 后约 2 秒（i3.f.c 首次 postDelayed 到期）拉起 UTG；此后每 3 秒重跳一次，可稳定复现",
    "key_pages_to_capture": [
      {
        "page_role": "跳设置后压栈的底部悬浮引导条",
        "page_identifier": "com.fedozojaforo.valeso.foxugovixo.jokaju 的 WebView（type=2 悬浮窗、gravity=80、高度 -2），内容为远端 Base64 HTML",
        "why_most_useful": "这是唯一一处对用户直接可见的引导文案，且文案完全来自远端下发，静态无法获得，是判定诱导话术性质的决定性页面",
        "observable_utg_signals": ["WebView 节点树中的 HTML 文本与按钮文案（含多语言 Enable 按钮）", "悬浮窗与系统设置页的层级叠压关系", "页面 lang 是否已替换为设备语言"]
      },
      {
        "page_role": "全屏远端教学页",
        "page_identifier": "com.fedozojaforo.valeso.viyeregika 全屏 WebView（window type=2006）",
        "why_most_useful": "该页把服务名伪装为 Chrome Update Service，直接体现品牌冒用与假更新话术",
        "observable_utg_signals": ["页面中出现的 \"Chrome Update Service\" 字样", "是否存在跳转按钮/箭头指引与 JS 桥调用", "页面是否覆盖全屏且无关闭控件"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings SubSettings 页中的 \"HookAPPService\" 条目及其说明文字",
        "why_most_useful": "验证服务标签、误导性 description 与实际应用名 HookAPP 的身份错配，并可观察服务是否自行点击开关",
        "observable_utg_signals": ["列表项文本 HookAPPService 与 description 原文", "开关在用户未操作时是否自动切换", "页面停留时长与 3 秒重跳频次"]
      },
      {
        "page_role": "冷启动空白占位页",
        "page_identifier": "com.zejapizehiyuki.yijoro.gojonamopi（Theme.Translucent.NoTitleBar，TextView(\" \")）",
        "why_most_useful": "确认应用在 0 步内即触发引导，无任何功能页或说明页作为前置，属最激进的诱导时序",
        "observable_utg_signals": ["冷启动到跳设置页的时间差（≈2s）", "界面节点数极少（近乎空白）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区是引导文案位于远端 HTML：静态不可见，需依赖运行期 UTG/流量抓取才能获得逐字文本；若设备断网或远端配置为空（viyeregika.H/G 长度为 0），应用只做裸跳设置页而不显示引导层，UTG 仅能看到系统无障碍页，容易误判为无诱导。此外桌面图标伪装依赖已安装应用存在，纯净测试机上可能不触发别名切换。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL"
  ],
  "code_anchors": [
    "i3.f.b",
    "i3.f.c",
    "com.fedozojaforo.valeso.foxugovixo.jokaju.onCreate",
    "com.fedozojaforo.valeso.viyeregika.s",
    "com.fedozojaforo.valeso.gukupuga.kanenovewuceba.i",
    "res/xml/covovido.xml"
  ]
}
```

</details>
