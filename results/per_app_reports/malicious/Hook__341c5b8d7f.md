# MB_088__341c5b8d7f｜Hook — BBVA

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：144.3s

## 1. 一句话核心结论

- **核心申请方式**：以 BBVA 银行名和 10 个社交/商店图标别名伪装，冷启动只显示空白页，1 秒后由系统级悬浮窗口 WebView 直接拉起 android.settings.ACCESSIBILITY_SETTINGS，且 onResume/返回键无条件重跳形成拒权死循环，诱使用户开启名为 BBVA4 的全量监听无障碍服务。
- **静态可见性说明**：引导链路（入口 Activity、跳转 Intent、悬浮层添加、拒权循环）全部静态可见；但承载引导/教学文案的两个 WebView HTML 常量 s227、s228 的 Lazy 提供器在本样本中返回空字符串，且无 assets 下 HTML 资源，故实际展示的引导文字无法静态还原（可能为剥离构建或由远端下发/后续注入）。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `341c5b8d7fda09706c39fdb959897e9a983f25bb06cfa9b1a96fbfe54854086a` |
| 包名 / 年份 | `com.weruzepufalo.mavimibe` / 2024 |
| 家族 / 品类 | **Hook**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | BBVA |
| 引导页宣称品牌/身份 | BBVA（西班牙对外银行）及 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram（activity-alias 伪装） |
| 系统无障碍列表服务名 | BBVA4 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面图标名伪装为 BBVA 银行；10 个 enabled=false 的 activity-alias 可动态启用为 Facebook/Google Play/Gmail/WhatsApp/Telegram/TikTok/Instagram/Chrome/Youtube/Contacts 图标与名称（多别名伪装）；主界面内容视图为仅含一个空格的 TextView、多个 Activity 使用 label=" " 或 label=""；Application 与启动 Activity 均为 Theme.Translucent.NoTitleBar 半透明无标题、excludeFromRecents+noHistory，桌面无残留；无障碍描述用“先关再开”话术诱导重复开关以规避系统提示；类名/包名（com.xenusihapalo.sari.*、binipohi、vipero）与业务语义完全无关。 |
| 无障碍服务类名 | `com.xenusihapalo.sari.vewabeyufixo.binipohi` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | If accessibility permission has been on, please turn off then turn on. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.weruzepufalo.mavimibe.zigibe（LAUNCHER，@style/ACL，noHistory，excludeFromRecents） | 用户点击桌面图标 BBVA → zigibe.onCreate | 原生Activity | 界面内容为一个空格的 TextView，视觉上完全空白，无任何业务界面 | 无需操作（无按钮、无取消入口），用户只能看到空白屏等待自动跳转 | `com.weruzepufalo.mavimibe.zigibe#onCreate` |
| 2 | 业务功能触发 | com.xenusihapalo.sari.Payload.start2 → com.xenusihapalo.sari.sunaduloji（空白页，noHistory） | zigibe.onCreate 判定 hasAllPermission()==false → Payload.start2(this)；sunaduloji.onCreate 调 start(FromPush) → Payload.start 用 Handler.postDelayed(...,1000ms) | 原生Activity | 仍是只有一个空格的空白页，用于拖延 1 秒并抢占前台，规避用户察觉 | 无（无取消/跳过按钮；onBackPressed 只会再次调用 start(true) 重入） | `com.xenusihapalo.sari.Payload#start2 / com.xenusihapalo.sari.Payload#start / com.xenusihapalo.sari.sunaduloji#onCreate` |
| 3 | 引导说明页 | com.xenusihapalo.sari.vipero（Window.setType(2006) 系统级窗口 + 全屏 WebView，经 WindowManager.addView） | 延迟 1s 后启动 vipero → onCreate 读取 Base64 常量 s227 作为 HTML → onResume 调 work() | 悬浮窗Overlay | **原文**：（本样本 s227 解码后为空字符串，HTML 正文不可静态还原）<br>**译注**：预期为引导用户开启无障碍的说明/教学页（覆盖在其他应用之上），本包内文案为空，实际呈现为空白覆盖层 | 预期由网页按钮触发 Android.onData()；无取消/跳过按钮，onBackPressed 仅重新执行 work() | `com.xenusihapalo.sari.vipero#work / com.xenusihapalo.sari.vipero$WebAppInterface#onData` |
| 4 | 跳无障碍设置 | 系统「设置 → 无障碍 → 已下载的服务」页（Intent android.settings.ACCESSIBILITY_SETTINGS） | work() 检测 xadifa.isAccessibilityServiceEnabled(this, binipohi.class)==false，且 launchHttp 因 s227 为空被置 false → 走 else 分支 openAccessabilitySettings() → kaditoguha.gotoAccessibilityService(activity) | 系统无障碍页 | **原文**：If accessibility permission has been on, please turn off then turn on.<br>**译注**：“如果无障碍权限已开启，请先关闭再重新开启。”——列表项下方说明文字，诱导用户反复开关 | 要求用户在该页找到并开启名为 BBVA4 的服务；无取消/返回提示，无跳过入口 | `com.xenusihapalo.sari.vipero#openAccessabilitySettings / com.xenusihapalo.sari.jese.kaditoguha#gotoAccessibilityService / res/xml/xonapuwuseki.xml` |
| 5 | 遮罩叠层指引 | com.xenusihapalo.sari.modawu.peruzi（gravity=80 底部、WindowManager 悬浮 WebView，加载 Base64 常量 s228） | gotoAccessibilityService() 在 s228.length()>0 时，跳设置后立即 startActivity(peruzi)（FLAG_ACTIVITY_NEW_TASK\|REORDER_TO_FRONT；小米且 SDK>=29 额外加 CLEAR_TASK） | 悬浮窗Overlay | **原文**：（本样本 s228 解码后为空字符串，遮罩文案不可静态还原）<br>**译注**：预期为压在系统设置页之上的半透明/底部引导条，指引用户点开 BBVA4 开关；本包内为空 | 预期引导用户点击开关；无取消按钮，onBackPressed 仅 WebView.goBack() | `com.xenusihapalo.sari.modawu.peruzi#onCreate / com.xenusihapalo.sari.jese.kaditoguha#gotoAccessibilityService` |
| 6 | 拒权反馈循环 | vipero.onResume / vipero.onBackPressed → work() → openAccessabilitySettings() | 用户从系统设置页返回（onResume）或按返回键（onBackPressed）时，未开启无障碍则再次跳转 ACCESSIBILITY_SETTINGS | 系统无障碍页 | **原文**：If accessibility permission has been on, please turn off then turn on.<br>**译注**：反复回到同一系统无障碍页，说明文字继续要求“关闭再开启”，形成无法退出的索权循环 | 除开启无障碍外无其他出路（无取消/跳过/降级路径） | `com.xenusihapalo.sari.vipero#onResume / com.xenusihapalo.sari.vipero#onBackPressed / com.xenusihapalo.sari.vipero#work` |
| 7 | 获权后动作 | binipohi（无障碍服务 BBVA4）+ vipero.work() 后续权限链（通知使用权、运行时权限、悬浮窗、忽略电池优化） | isAccessibilityServiceEnabled 返回 true 后，work() 依次检查 DrawerSniffer.hasPermission、keyixiju.PERMISSIONS、fayuwoni.canDrawOverlays/xiaomiOverlayPermission、is_dozemode（tryCount<5），最后进入 Payload 协程 | 系统无障碍页 | 无 | 继续被要求授予通知使用权、通讯录/短信/电话/相机等运行时权限、悬浮窗与忽略电池优化 | `com.xenusihapalo.sari.vipero#work / com.xenusihapalo.sari.vewabeyufixo.binipohi` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：service com.xenusihapalo.sari.vewabeyufixo.binipohi，label="BBVA4"，android:description=@string/text_accessibility_service_description（res/values/strings.xml:33）
- vipero 全屏系统级悬浮窗口 WebView（Window.setType(2006)，addView 到 WindowManager）：承载 Base64 常量 s227 解码的 HTML 引导页；本样本解码为空，无可见文案
- peruzi 底部悬浮 WebView 遮罩（gravity=80，y 偏移，高度 wrap_content）：承载 Base64 常量 s228 解码的 HTML 获权指引；本样本解码为空，无可见文案
- zigibe / sunaduloji 主界面：内容视图为 TextView(" ")，无任何引导文字（视觉空白）
- 桌面图标与任务栏名称：application android:label="BBVA"，10 个 activity-alias 的 label 分别为 Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram；另有 label=" " 与 label="" 的空标签组件
- 设备管理器广播接收器 wozekice 的 android:description=@string/adm，label=" "（空白标签）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开启，请先关闭再重新开启。 | `res/values/strings.xml 第 33 行 key=text_accessibility_service_description（被 res/xml/xonapuwuseki.xml 的 android:description 引用）` | 教唆忽视警告 |
| en | BBVA4 | BBVA4（银行品牌加序号，制造“官方第 4 版服务”的假象） | `AndroidManifest.xml service com.xenusihapalo.sari.vewabeyufixo.binipohi android:label` | 假更新 |
| en | BBVA | BBVA（西班牙对外银行） | `AndroidManifest.xml application android:label（桌面显示名）` | 假更新 |
| en | — | 单个空格（空白界面，用于隐藏真实意图） | `com.weruzepufalo.mavimibe.zigibe#onCreate 与 com.xenusihapalo.sari.sunaduloji#onCreate 中的 TextView.setText(" ")` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：vipero.onResume() 与 vipero.onBackPressed() 均无条件调用 work()，从系统无障碍页返回而服务未开启时立刻再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；返回键不退出应用而是重入 work()，sunaduloji.onBackPressed 亦重新 start(true)，形成无退出的反复拉起重跳
- **遮罩叠层 / 高仿系统设置页**：有叠层：vipero 为 Window.setType(2006) 系统级窗口承载的全屏 WebView 覆盖层；peruzi 为 gravity=BOTTOM 的悬浮 WebView 遮罩条，在跳转系统设置页后立即压栈显示（本样本两者 HTML 内容均为空）；未发现伪造的无障碍开关界面，跳转目标是真实系统设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=28，未使用 ACTION_MANAGE_APP_OVERLAY 之外的受限设置分步教学，也未使用 Session 安装器；悬浮窗走 xadifa.requestOverlayPermission / xiaomiOverlayPermission）
- **获权后即时行为与防撤权机制**：获权后 binipohi 具备 flagRequestFilterKeyEvents、canRetrieveWindowContent、canPerformGestures，并实现 exitSettings、permissionClick、unclick、blockDeleteBots、injectView、addBlackView/addWaitView、keylogger 等方法，可在设置/权限页面注入黑色遮罩与自动点击以阻止用户关闭；同时配合设备管理器接收器（BIND_DEVICE_ADMIN）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 降低被移除概率
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到前台 Activity 切换到 com.xenusihapalo.sari.vipero / com.xenusihapalo.sari.modawu.peruzi / com.xenusihapalo.sari.sunaduloji（均为空白或系统级悬浮窗口），或捕获到 Intent android.settings.ACCESSIBILITY_SETTINGS 被本包拉起的瞬间；亦可在冷启动 1 秒内直接 UTG 抓取，因该样本无任何可见引导文字，界面为空即强信号
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在盲区：本样本承载引导文案的 s227/s228 HTML 常量在代码中返回空字符串，纯 UTG 文本提取可能只看到空白窗口而无任何引导措辞，需结合“空白界面 + 直跳 ACCESSIBILITY_SETTINGS + 返回重跳循环”行为特征判定；此外应用未加壳（无 VMP/密文 DEX），静态加壳不构成盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动空白入口页** | packageName=com.weruzepufalo.mavimibe，Activity=com.weruzepufalo.mavimibe.zigibe，界面仅一个空格 TextView，无任何控件 | 确认“桌面名 BBVA 但界面完全空白”这一伪装-功能脱节事实，是判定诱导而非真实银行/工具业务的第一证据 | Activity 名与包名不匹配（com.weruzepufalo.mavimibe.zigibe 而非 BBVA 官方包名）；全屏无控件、无文本（仅空白）；Activity 在启动后 1 秒内自动 finish/切换 |
| **跳转前系统级悬浮 WebView 教学页** | Activity=com.xenusihapalo.sari.vipero，窗口类型 2006，全屏 WebView 覆盖层 | 该层是唯一承载引导文案的载体，其文本/按钮是否存在直接决定用户是否被明确引导点击开启无障碍 | 存在 WebView 节点且 text 为空（说明文案被剥离/远端下发）；点击后窗口销毁并跳转系统设置页；无任何取消/关闭按钮 |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载的服务，条目文本 BBVA4，描述 If accessibility permission has been on, please turn off then turn on. | 核对服务显示名与真实品牌不符、描述使用“关闭再开启”话术诱导反复开关，是判断索权欺诈的关键页面 | 服务名 BBVA4 与系统设置包名不同源；描述文案要求先关闭再开启；开启后描述/开关状态变化 |
| **设置页后压栈的底部遮罩引导条** | Activity=com.xenusihapalo.sari.modawu.peruzi，gravity=BOTTOM 悬浮 WebView | 确认存在“在系统设置页之上叠加引导层”的行为，且该层是否遮挡/伪造系统控件是区分正常引导与叠层诱导的判别点 | 系统设置页前台时仍有本包悬浮窗口节点；悬浮节点可点击且指向本包 Activity；返回键被 WebView.goBack 拦截 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.weruzepufalo.mavimibe.zigibe#onCreate`
- `com.xenusihapalo.sari.Payload#start2`
- `com.xenusihapalo.sari.vipero#work`
- `com.xenusihapalo.sari.vipero#openAccessabilitySettings`
- `com.xenusihapalo.sari.jese.kaditoguha#gotoAccessibilityService`
- `com.xenusihapalo.sari.modawu.peruzi#onCreate`
- `res/xml/xonapuwuseki.xml`
- `res/values/strings.xml#L33`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（无障碍服务类 → 引导页 → 跳转点 → 悬浮叠层）。核心结论如下：

**关键发现**
- 入口 [zigibe](<resource-unit:#1.dex1 code:com.weruzepufalo.mavimibe.zigibe#onCreate>)（`@style/ACL` 半透明、`noHistory`、桌面名 `BBVA`）`onCreate` 只把内容视图设成一个内容为单个空格的 `TextView`，随后即 `Payload.start2()` → `sunaduloji`（同样空白页）→ `vipero`；用户几乎看不到任何业务界面，冷启动即进入权限索取链路。
- [vipero](<resource-unit:#1.dex1 code:com.xenusihapalo.sari.vipero#work>) 是一个 `Window.setType(2006)`（系统级窗口类型）的全屏 `WebView` 覆盖层：HTML 来自 Base64 常量 `s227`，注入 JS 接口 `"Android"`，网页点击回调 [vipero$WebAppInterface.onData()](<resource-unit:#1.dex1 code:com.xenusihapalo.sari.vipero$WebAppInterface#onData>) 直接调用 `openAccessabilitySettings()`。**本样本中 `s227` 与 `s228` 的 Lazy 提供器均返回空串**（`vipero$Companion$s227$2.invoke` / `s228$2.invoke` 为 `return ""`），因此教学 HTML 正文在本包内不可静态还原，`launchHttp` 被置为 `false`，`work()` 直接走“跳设置”分支。
- 跳转点明确：[kaditoguha.gotoAccessibilityService()](<resource-unit:#1.dex1 code:com.xenusihapalo.sari.jese.kaditoguha#gotoAccessibilityService>) 构造 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `FLAG_ACTIVITY_NEW_TASK|CLEAR_TOP` 直接跳系统无障碍列表页，并在 `s228` 非空时再压入 [peruzi](<resource-unit:#1.dex1 code:com.xenusihapalo.sari.modawu.peruzi#onCreate>)（gravity=BOTTOM 的底部悬浮 WebView 遮罩）做获权后指引。
- 无取消/无跳过：[vipero.onResume()](<resource-unit:#1.dex1 code:com.xenusihapalo.sari.vipero#onResume>) 与 [vipero.onBackPressed()](<resource-unit:#1.dex1 code:com.xenusihapalo.sari.vipero#onBackPressed>) 都无条件调用 `work()`，从设置页返回未开启即再次跳设置，返回键也只会重新进入该流程（拒权循环）。
- 无障碍服务 `binipohi` 在系统列表显示 `BBVA4`，`android:description` 为 “If accessibility permission has been on, please turn off then turn on.”（[strings.xml:33](<resource-unit:#1 file:res/values/strings.xml#L33>)、[xonapuwuseki.xml](<resource-unit:#1 file:res/xml/xonapuwuseki.xml>)），属教唆用户反复开关以绕过系统提示/重置服务状态的话术；其能力（`flagRequestFilterKeyEvents`、`canRetrieveWindowContent`、`canPerformGestures`）与 `keylogger`、`injectView`、`addBlackView`、`permissionClick`、`killApplication` 等成员指向银行/IM 覆盖窃取，而非无障碍辅助。
- 身份伪装：`BBVA`（西班牙对外银行）+ 10 个 `activity-alias`（Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram、TikTok、Telegram，均 `enabled="false"` 可动态启用）+ 空白标签（`label=" "`、`label=""`）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "引导链路（入口 Activity、跳转 Intent、悬浮层添加、拒权循环）全部静态可见；但承载引导/教学文案的两个 WebView HTML 常量 s227、s228 的 Lazy 提供器在本样本中返回空字符串，且无 assets 下 HTML 资源，故实际展示的引导文字无法静态还原（可能为剥离构建或由远端下发/后续注入）。",
  "summary_one_liner": "以 BBVA 银行名和 10 个社交/商店图标别名伪装，冷启动只显示空白页，1 秒后由系统级悬浮窗口 WebView 直接拉起 android.settings.ACCESSIBILITY_SETTINGS，且 onResume/返回键无条件重跳形成拒权死循环，诱使用户开启名为 BBVA4 的全量监听无障碍服务。",
  "disguise_identity": {
    "app_display_name": "BBVA",
    "claimed_brand_or_persona": "BBVA（西班牙对外银行）及 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram（activity-alias 伪装）",
    "a11y_service_label": "BBVA4",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面图标名伪装为 BBVA 银行；10 个 enabled=false 的 activity-alias 可动态启用为 Facebook/Google Play/Gmail/WhatsApp/Telegram/TikTok/Instagram/Chrome/Youtube/Contacts 图标与名称（多别名伪装）；主界面内容视图为仅含一个空格的 TextView、多个 Activity 使用 label=\" \" 或 label=\"\"；Application 与启动 Activity 均为 Theme.Translucent.NoTitleBar 半透明无标题、excludeFromRecents+noHistory，桌面无残留；无障碍描述用“先关再开”话术诱导重复开关以规避系统提示；类名/包名（com.xenusihapalo.sari.*、binipohi、vipero）与业务语义完全无关。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.weruzepufalo.mavimibe.zigibe（LAUNCHER，@style/ACL，noHistory，excludeFromRecents）",
      "trigger_event": "用户点击桌面图标 BBVA → zigibe.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": " ",
      "shown_text_zh": "界面内容为一个空格的 TextView，视觉上完全空白，无任何业务界面",
      "user_action_requested": "无需操作（无按钮、无取消入口），用户只能看到空白屏等待自动跳转",
      "code_anchor": "com.weruzepufalo.mavimibe.zigibe#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.xenusihapalo.sari.Payload.start2 → com.xenusihapalo.sari.sunaduloji（空白页，noHistory）",
      "trigger_event": "zigibe.onCreate 判定 hasAllPermission()==false → Payload.start2(this)；sunaduloji.onCreate 调 start(FromPush) → Payload.start 用 Handler.postDelayed(...,1000ms)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": " ",
      "shown_text_zh": "仍是只有一个空格的空白页，用于拖延 1 秒并抢占前台，规避用户察觉",
      "user_action_requested": "无（无取消/跳过按钮；onBackPressed 只会再次调用 start(true) 重入）",
      "code_anchor": "com.xenusihapalo.sari.Payload#start2 / com.xenusihapalo.sari.Payload#start / com.xenusihapalo.sari.sunaduloji#onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.xenusihapalo.sari.vipero（Window.setType(2006) 系统级窗口 + 全屏 WebView，经 WindowManager.addView）",
      "trigger_event": "延迟 1s 后启动 vipero → onCreate 读取 Base64 常量 s227 作为 HTML → onResume 调 work()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "（本样本 s227 解码后为空字符串，HTML 正文不可静态还原）",
      "shown_text_zh": "预期为引导用户开启无障碍的说明/教学页（覆盖在其他应用之上），本包内文案为空，实际呈现为空白覆盖层",
      "user_action_requested": "预期由网页按钮触发 Android.onData()；无取消/跳过按钮，onBackPressed 仅重新执行 work()",
      "code_anchor": "com.xenusihapalo.sari.vipero#work / com.xenusihapalo.sari.vipero$WebAppInterface#onData"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍 → 已下载的服务」页（Intent android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "work() 检测 xadifa.isAccessibilityServiceEnabled(this, binipohi.class)==false，且 launchHttp 因 s227 为空被置 false → 走 else 分支 openAccessabilitySettings() → kaditoguha.gotoAccessibilityService(activity)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "shown_text_zh": "“如果无障碍权限已开启，请先关闭再重新开启。”——列表项下方说明文字，诱导用户反复开关",
      "user_action_requested": "要求用户在该页找到并开启名为 BBVA4 的服务；无取消/返回提示，无跳过入口",
      "code_anchor": "com.xenusihapalo.sari.vipero#openAccessabilitySettings / com.xenusihapalo.sari.jese.kaditoguha#gotoAccessibilityService / res/xml/xonapuwuseki.xml"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.xenusihapalo.sari.modawu.peruzi（gravity=80 底部、WindowManager 悬浮 WebView，加载 Base64 常量 s228）",
      "trigger_event": "gotoAccessibilityService() 在 s228.length()>0 时，跳设置后立即 startActivity(peruzi)（FLAG_ACTIVITY_NEW_TASK|REORDER_TO_FRONT；小米且 SDK>=29 额外加 CLEAR_TASK）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "（本样本 s228 解码后为空字符串，遮罩文案不可静态还原）",
      "shown_text_zh": "预期为压在系统设置页之上的半透明/底部引导条，指引用户点开 BBVA4 开关；本包内为空",
      "user_action_requested": "预期引导用户点击开关；无取消按钮，onBackPressed 仅 WebView.goBack()",
      "code_anchor": "com.xenusihapalo.sari.modawu.peruzi#onCreate / com.xenusihapalo.sari.jese.kaditoguha#gotoAccessibilityService"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "vipero.onResume / vipero.onBackPressed → work() → openAccessabilitySettings()",
      "trigger_event": "用户从系统设置页返回（onResume）或按返回键（onBackPressed）时，未开启无障碍则再次跳转 ACCESSIBILITY_SETTINGS",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "shown_text_zh": "反复回到同一系统无障碍页，说明文字继续要求“关闭再开启”，形成无法退出的索权循环",
      "user_action_requested": "除开启无障碍外无其他出路（无取消/跳过/降级路径）",
      "code_anchor": "com.xenusihapalo.sari.vipero#onResume / com.xenusihapalo.sari.vipero#onBackPressed / com.xenusihapalo.sari.vipero#work"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "binipohi（无障碍服务 BBVA4）+ vipero.work() 后续权限链（通知使用权、运行时权限、悬浮窗、忽略电池优化）",
      "trigger_event": "isAccessibilityServiceEnabled 返回 true 后，work() 依次检查 DrawerSniffer.hasPermission、keyixiju.PERMISSIONS、fayuwoni.canDrawOverlays/xiaomiOverlayPermission、is_dozemode（tryCount<5），最后进入 Payload 协程",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后不再展示任何说明，直接进入后续权限索取与 Payload 主逻辑",
      "user_action_requested": "继续被要求授予通知使用权、通讯录/短信/电话/相机等运行时权限、悬浮窗与忽略电池优化",
      "code_anchor": "com.xenusihapalo.sari.vipero#work / com.xenusihapalo.sari.vewabeyufixo.binipohi"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：service com.xenusihapalo.sari.vewabeyufixo.binipohi，label=\"BBVA4\"，android:description=@string/text_accessibility_service_description（res/values/strings.xml:33）",
    "vipero 全屏系统级悬浮窗口 WebView（Window.setType(2006)，addView 到 WindowManager）：承载 Base64 常量 s227 解码的 HTML 引导页；本样本解码为空，无可见文案",
    "peruzi 底部悬浮 WebView 遮罩（gravity=80，y 偏移，高度 wrap_content）：承载 Base64 常量 s228 解码的 HTML 获权指引；本样本解码为空，无可见文案",
    "zigibe / sunaduloji 主界面：内容视图为 TextView(\" \")，无任何引导文字（视觉空白）",
    "桌面图标与任务栏名称：application android:label=\"BBVA\"，10 个 activity-alias 的 label 分别为 Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram；另有 label=\" \" 与 label=\"\" 的空标签组件",
    "设备管理器广播接收器 wozekice 的 android:description=@string/adm，label=\" \"（空白标签）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开启，请先关闭再重新开启。",
      "source_location": "res/values/strings.xml 第 33 行 key=text_accessibility_service_description（被 res/xml/xonapuwuseki.xml 的 android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "BBVA4",
      "text_zh": "BBVA4（银行品牌加序号，制造“官方第 4 版服务”的假象）",
      "source_location": "AndroidManifest.xml service com.xenusihapalo.sari.vewabeyufixo.binipohi android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "BBVA",
      "text_zh": "BBVA（西班牙对外银行）",
      "source_location": "AndroidManifest.xml application android:label（桌面显示名）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": " ",
      "text_zh": "单个空格（空白界面，用于隐藏真实意图）",
      "source_location": "com.weruzepufalo.mavimibe.zigibe#onCreate 与 com.xenusihapalo.sari.sunaduloji#onCreate 中的 TextView.setText(\" \")",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "vipero.onResume() 与 vipero.onBackPressed() 均无条件调用 work()，从系统无障碍页返回而服务未开启时立刻再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)；返回键不退出应用而是重入 work()，sunaduloji.onBackPressed 亦重新 start(true)，形成无退出的反复拉起重跳",
    "overlay_or_fake_settings": "有叠层：vipero 为 Window.setType(2006) 系统级窗口承载的全屏 WebView 覆盖层；peruzi 为 gravity=BOTTOM 的悬浮 WebView 遮罩条，在跳转系统设置页后立即压栈显示（本样本两者 HTML 内容均为空）；未发现伪造的无障碍开关界面，跳转目标是真实系统设置页",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=28，未使用 ACTION_MANAGE_APP_OVERLAY 之外的受限设置分步教学，也未使用 Session 安装器；悬浮窗走 xadifa.requestOverlayPermission / xiaomiOverlayPermission）",
    "post_grant_anti_removal": "获权后 binipohi 具备 flagRequestFilterKeyEvents、canRetrieveWindowContent、canPerformGestures，并实现 exitSettings、permissionClick、unclick、blockDeleteBots、injectView、addBlackView/addWaitView、keylogger 等方法，可在设置/权限页面注入黑色遮罩与自动点击以阻止用户关闭；同时配合设备管理器接收器（BIND_DEVICE_ADMIN）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 降低被移除概率",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到前台 Activity 切换到 com.xenusihapalo.sari.vipero / com.xenusihapalo.sari.modawu.peruzi / com.xenusihapalo.sari.sunaduloji（均为空白或系统级悬浮窗口），或捕获到 Intent android.settings.ACCESSIBILITY_SETTINGS 被本包拉起的瞬间；亦可在冷启动 1 秒内直接 UTG 抓取，因该样本无任何可见引导文字，界面为空即强信号",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动空白入口页",
        "page_identifier": "packageName=com.weruzepufalo.mavimibe，Activity=com.weruzepufalo.mavimibe.zigibe，界面仅一个空格 TextView，无任何控件",
        "why_most_useful": "确认“桌面名 BBVA 但界面完全空白”这一伪装-功能脱节事实，是判定诱导而非真实银行/工具业务的第一证据",
        "observable_utg_signals": ["Activity 名与包名不匹配（com.weruzepufalo.mavimibe.zigibe 而非 BBVA 官方包名）", "全屏无控件、无文本（仅空白）", "Activity 在启动后 1 秒内自动 finish/切换"]
      },
      {
        "page_role": "跳转前系统级悬浮 WebView 教学页",
        "page_identifier": "Activity=com.xenusihapalo.sari.vipero，窗口类型 2006，全屏 WebView 覆盖层",
        "why_most_useful": "该层是唯一承载引导文案的载体，其文本/按钮是否存在直接决定用户是否被明确引导点击开启无障碍",
        "observable_utg_signals": ["存在 WebView 节点且 text 为空（说明文案被剥离/远端下发）", "点击后窗口销毁并跳转系统设置页", "无任何取消/关闭按钮"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载的服务，条目文本 BBVA4，描述 If accessibility permission has been on, please turn off then turn on.",
        "why_most_useful": "核对服务显示名与真实品牌不符、描述使用“关闭再开启”话术诱导反复开关，是判断索权欺诈的关键页面",
        "observable_utg_signals": ["服务名 BBVA4 与系统设置包名不同源", "描述文案要求先关闭再开启", "开启后描述/开关状态变化"]
      },
      {
        "page_role": "设置页后压栈的底部遮罩引导条",
        "page_identifier": "Activity=com.xenusihapalo.sari.modawu.peruzi，gravity=BOTTOM 悬浮 WebView",
        "why_most_useful": "确认存在“在系统设置页之上叠加引导层”的行为，且该层是否遮挡/伪造系统控件是区分正常引导与叠层诱导的判别点",
        "observable_utg_signals": ["系统设置页前台时仍有本包悬浮窗口节点", "悬浮节点可点击且指向本包 Activity", "返回键被 WebView.goBack 拦截"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在盲区：本样本承载引导文案的 s227/s228 HTML 常量在代码中返回空字符串，纯 UTG 文本提取可能只看到空白窗口而无任何引导措辞，需结合“空白界面 + 直跳 ACCESSIBILITY_SETTINGS + 返回重跳循环”行为特征判定；此外应用未加壳（无 VMP/密文 DEX），静态加壳不构成盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.weruzepufalo.mavimibe.zigibe#onCreate",
    "com.xenusihapalo.sari.Payload#start2",
    "com.xenusihapalo.sari.vipero#work",
    "com.xenusihapalo.sari.vipero#openAccessabilitySettings",
    "com.xenusihapalo.sari.jese.kaditoguha#gotoAccessibilityService",
    "com.xenusihapalo.sari.modawu.peruzi#onCreate",
    "res/xml/xonapuwuseki.xml",
    "res/values/strings.xml#L33"
  ]
}
```

</details>
