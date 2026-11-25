# MB_087__9f17fc20c5｜Hook — tiktok+18

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：162.8s

## 1. 一句话核心结论

- **核心申请方式**：以纯空白界面冷启动后直接跳转 ACCESSIBILITY_SETTINGS，并用 2 秒轮询 + onResume 重跳强制用户开启无障碍，同时在设置页上方叠加不可聚焦 WebView 悬浮遮罩做（本包为空的）指引，全程无取消入口与任何透明说明。
- **静态可见性说明**：无障碍跳转、轮询重跳、悬浮窗叠层、空白 Activity 等控制逻辑完全静态可见（jiwi/toyuvovihinipe/maxiyayohoki 均未加壳、无 VMP）；但引导文案载体 s227/s228 的 Lazy 实现直接 return ""，本包内不含任何引导 HTML 明文，WebView 加载内容为空，真实文案可能依赖远端下发或运行时替换，无法静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9f17fc20c5c725707168b93690063638cb6e5b3a7b77b3e826e8458a79eb36e2` |
| 包名 / 年份 | `com.mugitepefaxade.ponowe` / 2024 |
| 家族 / 品类 | **Hook**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | tiktok+18 |
| 引导页宣称品牌/身份 | TikTok（短视频社交平台）+ 伪 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / Telegram 图标身份 |
| 系统无障碍列表服务名 | tiktok+18 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：十余个 activity-alias 复用同一 targetActivity com.mugitepefaxade.ponowe.zopulalekutu 并配 Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome 等图标与名称，默认 enabled=false 可运行时启用换脸；真实包名 com.mugitepefaxade.ponowe 与宣称品牌无关；无障碍服务类名 com.cinuxexasuba.zidogi.zonizafi.xuvisapabovijovu 与展示名完全不同；android:description 用英文让用户'关掉再打开'无障碍以掩盖服务重绑定；主 Activity 主题 @style/ACL 全屏透明 + noHistory + 仅含空格 TextView，桌面点击后无任何可见界面 |
| 无障碍服务类名 | `com.cinuxexasuba.zidogi.zonizafi.xuvisapabovijovu` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | If accessibility permission has been on, please turn off then turn on. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.mugitepefaxade.ponowe.zopulalekutu（LAUNCHER，label=tiktok+18，theme=@style/ACL，noHistory） | onCreate | 原生Activity | **原文**：setContentView(new TextView(...).setText(" "))<br>**译注**：界面仅有一个空格字符，用户看到的是空白页 | 无任何提示，无需用户操作（用户只感到'点了没反应'） | `com.mugitepefaxade.ponowe.zopulalekutu#onCreate` |
| 2 | 业务功能触发 | com.cinuxexasuba.zidogi.heda（同为空白 TextView，setFlags(0x40000) 不可聚焦） | Payload.start2() → Intent(app, heda) 启动；heda.onCreate → Payload.start(FromPush) → postDelayed 1000ms 再次 start2；onBackPressed → start(true) | 原生Activity | **原文**：textView.setText(" "); setContentView(textView);<br>**译注**：依然为空白页，1 秒后自我重入 | 无按钮、无取消入口，按返回键反而再次触发 start(true) | `com.cinuxexasuba.zidogi.Payload#start2 / com.cinuxexasuba.zidogi.heda#onCreate` |
| 3 | 引导说明页 | toyuvovihinipe 内动态创建的 WebView 全屏悬浮窗（WindowManager.LayoutParams(-1,-1,type=2,flags=0x40000)），注入 JS 桥 "Android" | onResume → work()；条件：isAccessibilityServiceEnabled()==false 且 launchHttp==true | 悬浮窗Overlay | **原文**：loadDataWithBaseURL(null, Base64.decode(getS227()).replace("<html lang=\"en\">", ...), "text/html", "UTF-8", null)；本包 s227$2.invoke() 返回 ""<br>**译注**：设计意图为加载一段 Base64 编码的 HTML 教学页；本包内解码结果为空字符串，实际呈现空白页 | HTML 内 JS 通过 Android.onData() 回调触发跳转（文案缺失，无法确认具体要求点击的文字） | `com.cinuxexasuba.zidogi.toyuvovihinipe#work / toyuvovihinipe$WebAppInterface#onData` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS） | work() 在 launchHttp==false 分支直接调用 openAccessabilitySettings()；或 WebView JS 桥 onData → openAccessabilitySettings() | 系统无障碍页 | **原文**：Intent intentAddFlags = new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(335544320);<br>**译注**：直接打开系统无障碍设置页，无前置说明 | 要求用户在系统列表中找到并开启名为 "tiktok+18" 的无障碍服务；无跳过/取消路径 | `com.cinuxexasuba.zidogi.nedafifubeju.jiwi#gotoAccessibilityService` |
| 5 | 遮罩叠层指引 | com.cinuxexasuba.zidogi.hudu.maxiyayohoki（setFlags(FLAG_NOT_FOCUSABLE)，WindowManager 底部 gravity=80 的 WebView 悬浮层，type=2） | gotoAccessibilityService 内 if (getS228().length() > 0) → startActivity(maxiyayohoki)（小米且 SDK>=29 加 FLAG_ACTIVITY_NEW_TASK/REORDER_TO_FRONT） | 悬浮窗Overlay | **原文**：loadDataWithBaseURL(null, Base64.decode(getS228())..., "text/html", "UTF-8", null)；本包 s228 为空<br>**译注**：设计为压在系统无障碍设置页底部的悬浮指引条；本包内容为空，用户只会在设置页上方看到空白透明层 | 点击/触摸悬浮层时回调（setOnClickListener / setOnTouchListener），意图引导用户在设置页完成开启 | `com.cinuxexasuba.zidogi.hudu.maxiyayohoki#onCreate` |
| 6 | 拒权反馈循环 | jiwi$ensureAccessibilityServiceEnabled$enterWrapper$1 / $exitWrapper$1（主线程 Handler 轮询）+ 系统 Toast | 每 2000ms postDelayed 轮询 xuvisapabovijovu.Companion.isEnabled()；用户从设置页返回时 toyuvovihinipe.onResume → work() 再次拉起 | 系统无障碍页 | **原文**：Toast.makeText(activity, "accessibility disconnected", 0).show();<br>**译注**：服务被关闭时弹出英文提示"无障碍连接已断开"，随即再次执行跳转回调 | 用户无法退出：返回即重跳，未开启则 2 秒后再次拉起无障碍设置或引导悬浮层 | `com.cinuxexasuba.zidogi.nedafifubeju.jiwi$ensureAccessibilityServiceEnabled$exitWrapper$1#run` |
| 7 | 跳受限设置 | 系统应用详情页（android.settings.APPLICATION_DETAILS_SETTINGS，data=package:<自身包名>） | work() 中 hasAllPermission 通过后 → 申请短信/通讯录/通话记录/相机等运行时权限 → 悬浮窗权限 → 忽略电池优化 → work$1$3 协程 launch 后延迟跳转 | 原生Activity | **原文**：new Intent("android.settings.APPLICATION_DETAILS_SETTINGS").addFlags(...).setData(Uri.fromParts("package", getPackageName(), null));<br>**译注**：把用户带到本应用的系统详情页（用于自启动/后台受限等开关），无文字教学，依赖系统页面自行操作 | 在应用详情页手动开启自启动/后台运行等受限项；setClickAutoStart(false)、setStartAppDetail(true) 标记该步已走 | `com.cinuxexasuba.zidogi.toyuvovihinipe$work$1$3#invokeSuspend$lambda-2` |
| 8 | 获权后动作 | com.cinuxexasuba.zidogi.zonizafi.xuvisapabovijovu（AccessibilityService） | 服务 onServiceConnected / onAccessibilityEvent 后按远端下发的 bot 参数执行 | 悬浮窗Overlay | **原文**：openFake / injectView / permissionClick / readPush / keylogger / addBlackView / addWaitView<br>**译注**：开启后不再展示任何说明，直接进入伪造界面注入、点击代操作、通知读取、按键记录等控制与窃取行为 | 用户被完全置于被代操作状态，无任何提示 | `com.cinuxexasuba.zidogi.zonizafi.xuvisapabovijovu#onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项 android:description："If accessibility permission has been on, please turn off then turn on."（服务名同为 tiktok+18）
- toyuvovihinipe#work 动态创建的全屏 WebView 悬浮窗（WindowManager type=2、FLAG_NOT_FOCUSABLE，覆盖整个屏幕）加载 Base64 HTML s227——本包解码为空，实际无文字
- 跳转 ACCESSIBILITY_SETTINGS 后启动的 maxiyayohoki Activity 底部 WebView 悬浮遮罩（gravity=80）加载 Base64 HTML s228——本包为空，实际无文字
- jiwi$exitWrapper$1 在服务被关闭时弹出的系统 Toast："accessibility disconnected"
- 启动器与中转 Activity（zopulalekutu / heda）仅含一个空格 TextView，没有任何引导或说明文字
- 应用详情页/权限请求弹窗为纯系统原生界面，应用侧未提供任何解释性文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已开启，请先关闭再重新开启。 | `AndroidManifest.xml 无障碍服务 android:description（strings 资源）` | 教唆忽视警告 |
| en | accessibility disconnected | 无障碍已断开 | `硬编码于 com.cinuxexasuba.zidogi.nedafifubeju.jiwi$ensureAccessibilityServiceEnabled$exitWrapper$1#run（Toast.makeText）` | 故障恐吓 |
| en | tiktok+18 | TikTok 18+（伪装为短视频成人内容应用） | `AndroidManifest.xml application android:label 与无障碍服务 android:label` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：jiwi.ensureAccessibilityServiceEnabled 每 2000ms 轮询 isEnabled()，未开启则 postDelayed(this, 2000) 无限重投；开启后 exitWrapper 继续每 2000ms 监控，检测到被关闭即 Toast "accessibility disconnected" 并执行 exitCallback（bringMeFront 用 PendingIntent 把自身拉回前台，失败则 Payload.start2 重新拉起中转 Activity）；同时 toyuvovihinipe.onResume → work() 保证用户从设置页返回就再次进入 WebView 悬浮引导/重跳无障碍设置，形成关闭—重跳闭环。
- **遮罩叠层 / 高仿系统设置页**：使用 WindowManager 叠加两层悬浮窗：toyuvovihinipe 全屏 WebView（LayoutParams(-1,-1,type=2,flags=0x40000) 不可聚焦）用于引导页；maxiyayohoki 底部 WebView（gravity=80、setFlags(FLAG_NOT_FOCUSABLE)、type=2）压在系统无障碍设置页之上做指引。未发现高仿系统无障碍开关页（未自绘开关控件），但存在明显的设置页上方遮罩层。
- **Android 13+ 受限设置（Restricted Settings）应对**：未发现逐字文字教学；代码通过 Intent("android.settings.APPLICATION_DETAILS_SETTINGS") 直接跳应用详情页并置 setStartAppDetail(true)，把'受限设置/自启动'授权交由用户在系统页面自行完成。
- **获权后即时行为与防撤权机制**：有：exitWrapper$1 持续每 2000ms 监控服务启用状态，一旦被撤销立即 Toast 提示并回调 bringMeFront / gotoAccessibilityService 重新拉回前台重跳；无障碍服务内另有 exitSettings(278 指令)、PERFORM_GLOBAL_ACTION、blockDeleteBots、killApplication 等防撤销/防清除手段。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到应用调用 startActivity 且 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（或 APPLICATION_DETAILS_SETTINGS）的瞬间，以及冷启动后 1 秒内出现的 type=2 WindowManager 悬浮窗（WebView）——此时应立即截取当前 UI 树与截图
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：本包内引导 HTML（s227/s228）为空的 Lazy 占位，静态与运行初期都可能呈现'纯空白无文字'的温和外壳，纯 UTG 文本提取可能拿到空串；真实诱导文案可能由远端下发或运行时替换，需在联网环境下抓取 WebView 内容或 hook Base64.decode/loadDataWithBaseURL 才能拿到逐字原文。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后叠加的全屏 WebView 引导层** | 窗口类型 TYPE_SYSTEM_ALERT/2002 级悬浮窗，节点树中存在 android.webkit.WebView 且无应用标题栏，宿主 Activity 为 toyuvovihinipe | 这是本家族唯一可能承载'引导文案'的载体，其内容是判定是'良性透明说明'还是'欺骗诱导'的分水岭 | WebView 节点存在但 text 为空（对应 s227 为空字符串）；同屏无任何原生 Dialog / 取消按钮；Activity 背景为空白 TextView（仅空格字符） |
| **系统无障碍设置页及其上方压栈的底部悬浮遮罩** | packageName=com.android.settings 的无障碍列表页，其上叠加另一窗口（maxiyayohoki，gravity=bottom，不可聚焦） | 证明'设置页 + 遮罩指引'的叠层诱导手法，并可在系统列表项上直接读到服务名 tiktok+18 与 android:description 话术 | 无障碍服务列表项文本 'tiktok+18'；description 文本 'If accessibility permission has been on, please turn off then turn on.'；同一时刻存在两个顶层窗口（settings + 应用悬浮层） |
| **拒权返回后的循环重跳页** | 2 秒间隔反复出现的 ACCESSIBILITY_SETTINGS 或空 WebView 悬浮窗；伴随 Toast 'accessibility disconnected' | 捕获 onResume 死循环与 2000ms 轮询重投，是判定'不可取消强制诱导'的关键运行证据 | 相同 Activity 在固定 2 秒周期重复出现；Toast 文本 'accessibility disconnected'；无任何取消/跳过控件 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.cinuxexasuba.zidogi.toyuvovihinipe#work`
- `com.cinuxexasuba.zidogi.nedafifubeju.jiwi#gotoAccessibilityService`
- `com.cinuxexasuba.zidogi.nedafifubeju.jiwi$ensureAccessibilityServiceEnabled$enterWrapper$1#run`
- `com.cinuxexasuba.zidogi.hudu.maxiyayohoki#onCreate`
- `com.cinuxexasuba.zidogi.toyuvovihinipe$work$1$3#invokeSuspend$lambda-2`
- `com.mugitepefaxade.ponowe.zopulalekutu#onCreate`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期 UTG 视角）

**整体形态**：这是一个典型的“无障碍引导获取”恶意样本，采用**空白界面、直接跳转设置、轮询重跳**的方式，几乎不向用户解释原因。

1. **入口完全空白**：启动器 Activity [zopulalekutu.onCreate()](<resource-unit:#1.dex1 code:com.mugitepefaxade.ponowe.zopulalekutu#onCreate>) 只执行 `setContentView(new TextView(" "))`，随后调用 `Payload.start2()` 转到同样空白的 [heda.onCreate()](<resource-unit:#1.dex1 code:com.cinuxexasuba.zidogi.heda#onCreate>)（`Payload.start` 延迟 1000ms 后重入），用户看不到任何业务界面或说明文字。
2. **引导页是叠加在界面上的 WebView**：[toyuvovihinipe.work()](<resource-unit:#1.dex1 code:com.cinuxexasuba.zidogi.toyuvovihinipe#work>) 在“无障碍未开启且 launchHttp”时，通过 `WindowManager.addView(new WebView, LayoutParams(-1,-1,type=2,flags=0x40000))` 叠加一个全屏、不可聚焦的 WebView，内容为 `Base64.decode(s227)` 的 HTML（并注入 JS 桥 `Android`，`onData` 回调直达跳设置）。本包内 `s227$2.invoke()` 直接 `return ""`，实际 HTML 为空，所以**本样本的引导文案在静态层面为空/缺失**，页面本体无法还原。
3. **直接跳转系统无障碍页**：[jiwi.gotoAccessibilityService()](<resource-unit:#1.dex1 code:com.cinuxexasuba.zidogi.nedafifubeju.jiwi#gotoAccessibilityService>) 使用 `Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(FLAG_ACTIVITY_CLEAR_TOP)` 跳转；若 `s228` 非空，则**紧接着启动 [maxiyayohoki.onCreate()](<resource-unit:#1.dex1 code:com.cinuxexasuba.zidogi.hudu.maxiyayohoki#onCreate>)（底部 gravity=80、`FLAG_NOT_FOCUSABLE` 的 WebView 悬浮遮罩）压在设置页之上做指引**——本包 `s228` 同样为空，故遮罩文本不可静态还原，但叠层机制明确存在。
4. **拒绝后反复循环**：[enterWrapper$1.run()](<resource-unit:#1.dex1 code:com.cinuxexasuba.zidogi.nedafifubeju.jiwi$ensureAccessibilityServiceEnabled$enterWrapper$1#run>) 每 **2000ms** 轮询 `isEnabled()`，未开启就重新排入自身；开启后由 `exitWrapper$1` 继续每 2000ms 监控，一旦被关闭就 `Toast("accessibility disconnected")` 并回调再次 `bringMeFront/gotoAccessibilityService`；此外 `toyuvovihinipe.onResume → work()` 使**用户从设置页返回即再次拉起**，没有取消或跳过按钮。
5. **获权后动作**：`work()` 在 `hasAllPermission` 成立后依次索要短信/通讯录/通话记录/相机等权限、悬浮窗、忽略电池优化，最后由 [invokeSuspend$lambda-2()](<resource-unit:#1.dex1 code:com.cinuxexasuba.zidogi.toyuvovihinipe$work$1$3#invokeSuspend$lambda-2>) 用 `Intent("android.settings.APPLICATION_DETAILS_SETTINGS")` 把用户带进应用详情页（配合 `setStartAppDetail(true)`，用于自启动/受限设置授权），随后进入无障碍服务 [xuvisapabovijovu](<resource-unit:#1.dex1 code:com.cinuxexasuba.zidogi.zonizafi.xuvisapabovijovu>) 的 `openFake/injectView/permissionClick/readPush/keylogger` 等控制与窃取逻辑。
6. **身份伪装**：桌面名 `tiktok+18`，另声明 Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram、Telegram、TikTok 等十余个 `activity-alias`（默认 `enabled=false`，可动态启用以换脸）；无障碍服务标签也复用 `tiktok+18`，description 却写 “If accessibility permission has been on, please turn off then turn on.”（让用户反复关闭再开启以完成服务重绑定），属**系统列表内的欺骗性话术**。

**证据边界**：跳转与轮询逻辑 100% 静态可见；引导 HTML（s227/s228）在本包内为空的 Lazy 占位，真实文案可能由远端下发或后续版本填入，需动态 UTG 抓取确认。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍跳转、轮询重跳、悬浮窗叠层、空白 Activity 等控制逻辑完全静态可见（jiwi/toyuvovihinipe/maxiyayohoki 均未加壳、无 VMP）；但引导文案载体 s227/s228 的 Lazy 实现直接 return \"\"，本包内不含任何引导 HTML 明文，WebView 加载内容为空，真实文案可能依赖远端下发或运行时替换，无法静态还原。",
  "summary_one_liner": "以纯空白界面冷启动后直接跳转 ACCESSIBILITY_SETTINGS，并用 2 秒轮询 + onResume 重跳强制用户开启无障碍，同时在设置页上方叠加不可聚焦 WebView 悬浮遮罩做（本包为空的）指引，全程无取消入口与任何透明说明。",
  "disguise_identity": {
    "app_display_name": "tiktok+18",
    "claimed_brand_or_persona": "TikTok（短视频社交平台）+ 伪 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / Telegram 图标身份",
    "a11y_service_label": "tiktok+18",
    "identity_mismatch": true,
    "obfuscation_tricks": "十余个 activity-alias 复用同一 targetActivity com.mugitepefaxade.ponowe.zopulalekutu 并配 Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome 等图标与名称，默认 enabled=false 可运行时启用换脸；真实包名 com.mugitepefaxade.ponowe 与宣称品牌无关；无障碍服务类名 com.cinuxexasuba.zidogi.zonizafi.xuvisapabovijovu 与展示名完全不同；android:description 用英文让用户'关掉再打开'无障碍以掩盖服务重绑定；主 Activity 主题 @style/ACL 全屏透明 + noHistory + 仅含空格 TextView，桌面点击后无任何可见界面"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.mugitepefaxade.ponowe.zopulalekutu（LAUNCHER，label=tiktok+18，theme=@style/ACL，noHistory）",
      "trigger_event": "onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "setContentView(new TextView(...).setText(\" \"))",
      "shown_text_zh": "界面仅有一个空格字符，用户看到的是空白页",
      "user_action_requested": "无任何提示，无需用户操作（用户只感到'点了没反应'）",
      "code_anchor": "com.mugitepefaxade.ponowe.zopulalekutu#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.cinuxexasuba.zidogi.heda（同为空白 TextView，setFlags(0x40000) 不可聚焦）",
      "trigger_event": "Payload.start2() → Intent(app, heda) 启动；heda.onCreate → Payload.start(FromPush) → postDelayed 1000ms 再次 start2；onBackPressed → start(true)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "textView.setText(\" \"); setContentView(textView);",
      "shown_text_zh": "依然为空白页，1 秒后自我重入",
      "user_action_requested": "无按钮、无取消入口，按返回键反而再次触发 start(true)",
      "code_anchor": "com.cinuxexasuba.zidogi.Payload#start2 / com.cinuxexasuba.zidogi.heda#onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "toyuvovihinipe 内动态创建的 WebView 全屏悬浮窗（WindowManager.LayoutParams(-1,-1,type=2,flags=0x40000)），注入 JS 桥 \"Android\"",
      "trigger_event": "onResume → work()；条件：isAccessibilityServiceEnabled()==false 且 launchHttp==true",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "loadDataWithBaseURL(null, Base64.decode(getS227()).replace(\"<html lang=\\\"en\\\">\", ...), \"text/html\", \"UTF-8\", null)；本包 s227$2.invoke() 返回 \"\"",
      "shown_text_zh": "设计意图为加载一段 Base64 编码的 HTML 教学页；本包内解码结果为空字符串，实际呈现空白页",
      "user_action_requested": "HTML 内 JS 通过 Android.onData() 回调触发跳转（文案缺失，无法确认具体要求点击的文字）",
      "code_anchor": "com.cinuxexasuba.zidogi.toyuvovihinipe#work / toyuvovihinipe$WebAppInterface#onData"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "work() 在 launchHttp==false 分支直接调用 openAccessabilitySettings()；或 WebView JS 桥 onData → openAccessabilitySettings()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Intent intentAddFlags = new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(335544320);",
      "shown_text_zh": "直接打开系统无障碍设置页，无前置说明",
      "user_action_requested": "要求用户在系统列表中找到并开启名为 \"tiktok+18\" 的无障碍服务；无跳过/取消路径",
      "code_anchor": "com.cinuxexasuba.zidogi.nedafifubeju.jiwi#gotoAccessibilityService"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.cinuxexasuba.zidogi.hudu.maxiyayohoki（setFlags(FLAG_NOT_FOCUSABLE)，WindowManager 底部 gravity=80 的 WebView 悬浮层，type=2）",
      "trigger_event": "gotoAccessibilityService 内 if (getS228().length() > 0) → startActivity(maxiyayohoki)（小米且 SDK>=29 加 FLAG_ACTIVITY_NEW_TASK/REORDER_TO_FRONT）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "loadDataWithBaseURL(null, Base64.decode(getS228())..., \"text/html\", \"UTF-8\", null)；本包 s228 为空",
      "shown_text_zh": "设计为压在系统无障碍设置页底部的悬浮指引条；本包内容为空，用户只会在设置页上方看到空白透明层",
      "user_action_requested": "点击/触摸悬浮层时回调（setOnClickListener / setOnTouchListener），意图引导用户在设置页完成开启",
      "code_anchor": "com.cinuxexasuba.zidogi.hudu.maxiyayohoki#onCreate"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "jiwi$ensureAccessibilityServiceEnabled$enterWrapper$1 / $exitWrapper$1（主线程 Handler 轮询）+ 系统 Toast",
      "trigger_event": "每 2000ms postDelayed 轮询 xuvisapabovijovu.Companion.isEnabled()；用户从设置页返回时 toyuvovihinipe.onResume → work() 再次拉起",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Toast.makeText(activity, \"accessibility disconnected\", 0).show();",
      "shown_text_zh": "服务被关闭时弹出英文提示\"无障碍连接已断开\"，随即再次执行跳转回调",
      "user_action_requested": "用户无法退出：返回即重跳，未开启则 2 秒后再次拉起无障碍设置或引导悬浮层",
      "code_anchor": "com.cinuxexasuba.zidogi.nedafifubeju.jiwi$ensureAccessibilityServiceEnabled$exitWrapper$1#run"
    },
    {
      "step": 7,
      "stage": "跳受限设置",
      "screen_or_component": "系统应用详情页（android.settings.APPLICATION_DETAILS_SETTINGS，data=package:<自身包名>）",
      "trigger_event": "work() 中 hasAllPermission 通过后 → 申请短信/通讯录/通话记录/相机等运行时权限 → 悬浮窗权限 → 忽略电池优化 → work$1$3 协程 launch 后延迟跳转",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "new Intent(\"android.settings.APPLICATION_DETAILS_SETTINGS\").addFlags(...).setData(Uri.fromParts(\"package\", getPackageName(), null));",
      "shown_text_zh": "把用户带到本应用的系统详情页（用于自启动/后台受限等开关），无文字教学，依赖系统页面自行操作",
      "user_action_requested": "在应用详情页手动开启自启动/后台运行等受限项；setClickAutoStart(false)、setStartAppDetail(true) 标记该步已走",
      "code_anchor": "com.cinuxexasuba.zidogi.toyuvovihinipe$work$1$3#invokeSuspend$lambda-2"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.cinuxexasuba.zidogi.zonizafi.xuvisapabovijovu（AccessibilityService）",
      "trigger_event": "服务 onServiceConnected / onAccessibilityEvent 后按远端下发的 bot 参数执行",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "openFake / injectView / permissionClick / readPush / keylogger / addBlackView / addWaitView",
      "shown_text_zh": "开启后不再展示任何说明，直接进入伪造界面注入、点击代操作、通知读取、按键记录等控制与窃取行为",
      "user_action_requested": "用户被完全置于被代操作状态，无任何提示",
      "code_anchor": "com.cinuxexasuba.zidogi.zonizafi.xuvisapabovijovu#onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项 android:description：\"If accessibility permission has been on, please turn off then turn on.\"（服务名同为 tiktok+18）",
    "toyuvovihinipe#work 动态创建的全屏 WebView 悬浮窗（WindowManager type=2、FLAG_NOT_FOCUSABLE，覆盖整个屏幕）加载 Base64 HTML s227——本包解码为空，实际无文字",
    "跳转 ACCESSIBILITY_SETTINGS 后启动的 maxiyayohoki Activity 底部 WebView 悬浮遮罩（gravity=80）加载 Base64 HTML s228——本包为空，实际无文字",
    "jiwi$exitWrapper$1 在服务被关闭时弹出的系统 Toast：\"accessibility disconnected\"",
    "启动器与中转 Activity（zopulalekutu / heda）仅含一个空格 TextView，没有任何引导或说明文字",
    "应用详情页/权限请求弹窗为纯系统原生界面，应用侧未提供任何解释性文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已开启，请先关闭再重新开启。",
      "source_location": "AndroidManifest.xml 无障碍服务 android:description（strings 资源）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "accessibility disconnected",
      "text_zh": "无障碍已断开",
      "source_location": "硬编码于 com.cinuxexasuba.zidogi.nedafifubeju.jiwi$ensureAccessibilityServiceEnabled$exitWrapper$1#run（Toast.makeText）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "tiktok+18",
      "text_zh": "TikTok 18+（伪装为短视频成人内容应用）",
      "source_location": "AndroidManifest.xml application android:label 与无障碍服务 android:label",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "jiwi.ensureAccessibilityServiceEnabled 每 2000ms 轮询 isEnabled()，未开启则 postDelayed(this, 2000) 无限重投；开启后 exitWrapper 继续每 2000ms 监控，检测到被关闭即 Toast \"accessibility disconnected\" 并执行 exitCallback（bringMeFront 用 PendingIntent 把自身拉回前台，失败则 Payload.start2 重新拉起中转 Activity）；同时 toyuvovihinipe.onResume → work() 保证用户从设置页返回就再次进入 WebView 悬浮引导/重跳无障碍设置，形成关闭—重跳闭环。",
    "overlay_or_fake_settings": "使用 WindowManager 叠加两层悬浮窗：toyuvovihinipe 全屏 WebView（LayoutParams(-1,-1,type=2,flags=0x40000) 不可聚焦）用于引导页；maxiyayohoki 底部 WebView（gravity=80、setFlags(FLAG_NOT_FOCUSABLE)、type=2）压在系统无障碍设置页之上做指引。未发现高仿系统无障碍开关页（未自绘开关控件），但存在明显的设置页上方遮罩层。",
    "restricted_settings_13plus_coaching": "未发现逐字文字教学；代码通过 Intent(\"android.settings.APPLICATION_DETAILS_SETTINGS\") 直接跳应用详情页并置 setStartAppDetail(true)，把'受限设置/自启动'授权交由用户在系统页面自行完成。",
    "post_grant_anti_removal": "有：exitWrapper$1 持续每 2000ms 监控服务启用状态，一旦被撤销立即 Toast 提示并回调 bringMeFront / gotoAccessibilityService 重新拉回前台重跳；无障碍服务内另有 exitSettings(278 指令)、PERFORM_GLOBAL_ACTION、blockDeleteBots、killApplication 等防撤销/防清除手段。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到应用调用 startActivity 且 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（或 APPLICATION_DETAILS_SETTINGS）的瞬间，以及冷启动后 1 秒内出现的 type=2 WindowManager 悬浮窗（WebView）——此时应立即截取当前 UI 树与截图",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后叠加的全屏 WebView 引导层",
        "page_identifier": "窗口类型 TYPE_SYSTEM_ALERT/2002 级悬浮窗，节点树中存在 android.webkit.WebView 且无应用标题栏，宿主 Activity 为 toyuvovihinipe",
        "why_most_useful": "这是本家族唯一可能承载'引导文案'的载体，其内容是判定是'良性透明说明'还是'欺骗诱导'的分水岭",
        "observable_utg_signals": ["WebView 节点存在但 text 为空（对应 s227 为空字符串）", "同屏无任何原生 Dialog / 取消按钮", "Activity 背景为空白 TextView（仅空格字符）"]
      },
      {
        "page_role": "系统无障碍设置页及其上方压栈的底部悬浮遮罩",
        "page_identifier": "packageName=com.android.settings 的无障碍列表页，其上叠加另一窗口（maxiyayohoki，gravity=bottom，不可聚焦）",
        "why_most_useful": "证明'设置页 + 遮罩指引'的叠层诱导手法，并可在系统列表项上直接读到服务名 tiktok+18 与 android:description 话术",
        "observable_utg_signals": ["无障碍服务列表项文本 'tiktok+18'", "description 文本 'If accessibility permission has been on, please turn off then turn on.'", "同一时刻存在两个顶层窗口（settings + 应用悬浮层）"]
      },
      {
        "page_role": "拒权返回后的循环重跳页",
        "page_identifier": "2 秒间隔反复出现的 ACCESSIBILITY_SETTINGS 或空 WebView 悬浮窗；伴随 Toast 'accessibility disconnected'",
        "why_most_useful": "捕获 onResume 死循环与 2000ms 轮询重投，是判定'不可取消强制诱导'的关键运行证据",
        "observable_utg_signals": ["相同 Activity 在固定 2 秒周期重复出现", "Toast 文本 'accessibility disconnected'", "无任何取消/跳过控件"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：本包内引导 HTML（s227/s228）为空的 Lazy 占位，静态与运行初期都可能呈现'纯空白无文字'的温和外壳，纯 UTG 文本提取可能拿到空串；真实诱导文案可能由远端下发或运行时替换，需在联网环境下抓取 WebView 内容或 hook Base64.decode/loadDataWithBaseURL 才能拿到逐字原文。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.cinuxexasuba.zidogi.toyuvovihinipe#work",
    "com.cinuxexasuba.zidogi.nedafifubeju.jiwi#gotoAccessibilityService",
    "com.cinuxexasuba.zidogi.nedafifubeju.jiwi$ensureAccessibilityServiceEnabled$enterWrapper$1#run",
    "com.cinuxexasuba.zidogi.hudu.maxiyayohoki#onCreate",
    "com.cinuxexasuba.zidogi.toyuvovihinipe$work$1$3#invokeSuspend$lambda-2",
    "com.mugitepefaxade.ponowe.zopulalekutu#onCreate"
  ]
}
```

**未决问题与边界**：引导 HTML（s227/s228）在本包内为空 Lazy 占位，真实逐字文案不可静态确认，需动态抓取或 hook `Base64.decode`/`WebView.loadDataWithBaseURL`；本次受 14 次工具调用上限约束，未执行风险台账写入与动态验证。

</details>
