# MB_084__692e7b0f65｜Ermac — HookAPP

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：180.3s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即用 WindowManager 全屏/底部悬浮 WebView 把远端 HTML 渲染成伪『Chrome Update Service』启用提示，同时跳系统无障碍设置页并以 2s/3s 定时器和 PendingIntent 自拉起循环重跳，服务侧用 isAccessibilityTool=true 抹掉受限警告
- **静态可见性说明**：Java 层诱导链（跳转、定时器、PendingIntent 自拉起、悬浮窗叠层、占位符替换）全部静态可见；但诱饵 HTML 正文不在包内——korimiti$b.o()/korimiti$c.o() 在本样本返回空串，assets 下仅 dexopt 目录，页面文本由运行期远端配置下发；assets 无本地 HTML 资源
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `692e7b0f657ac34635e0dcd633f9c73b37d0258457d161ec6dbee26820cb72dd` |
| 包名 / 年份 | `com.nisarexubunajo.xaroca` / 2024 |
| 家族 / 品类 | **Ermac**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | HookAPP |
| 引导页宣称品牌/身份 | Chrome Update Service（Chrome 更新服务）；另有 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 共 12 个 activity-alias 备用伪装身份 |
| 系统无障碍列表服务名 | HookAPPService |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍服务声明 android:isAccessibilityTool="true" 且 accessibilityDataSensitive="no"，使系统无障碍列表不展示『可查看屏幕内容/敏感数据』受限警告；2) 服务标签 HookAPPService 与页面宣称的 Chrome Update Service 完全无关，而真实应用名仅为 HookAPP；3) 12 个 activity-alias 复用知名应用图标与名称（ic_facebook/ic_google_play/ic_gmail/ic_whatsapp/ic_chrome 等）默认关闭、可按需切换；4) 无障碍描述不写用途，只写『若已开启请关闭后重新开启』，制造必须重开关的操作惯性；5) 启动 Activity 无可见 UI（仅一个空格 TextView）且 Theme.Translucent.NoTitleBar + noHistory |
| 无障碍服务类名 | `com.pavanovaciyana.ceyino.pahoduco.dasoxawajeluvezi` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.nisarexubunajo.xaroca.lidi（LAUNCHER，主题 Theme.Translucent.NoTitleBar，noHistory=true） | 用户点击桌面图标（或 activity-alias 图标）→ onCreate | 原生Activity | **原文**：textView.setText(" ")<br>**译注**：界面仅显示一个空格，无任何可见业务内容，用户看到空白/瞬间透明页 | 无（无取消、无跳过、无说明） | `com.nisarexubunajo.xaroca.lidi#onCreate` |
| 2 | 引导说明页 | com.pavanovaciyana.ceyino.korimiti（Window.setType(2006) 系统级悬浮窗口承载的 Activity + WebView） | korimiti.onCreate 检测到无障碍服务未开启（dasoxawajeluvezi$b.P()==false）且悬浮窗权限已授予 → korimiti.s() | 悬浮窗Overlay | **原文**：f4.i.E0(new String(bArrDecode, j3.c.a), "%Enable_Accessibility_Service%", "Chrome Update Service")<br>**译注**：页面模板中的占位符被替换为『Chrome Update Service（Chrome 更新服务）』；本样本 HTML 正文为空串，实际文案由远端配置填充，模板固定注入当前系统语言与多语种『启用/Enable』词表 | 按页面提示去开启无障碍服务；WebView 暴露 Android JS 桥（addJavascriptInterface(..., "Android")）供页面回调原生动作，无取消/跳过按钮实现 | `com.pavanovaciyana.ceyino.korimiti#s；j3.c#<clinit>` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | j3.h.c 中 Handler.postDelayed(runnable, 2000) → j3.h.b()（另 lidi.onCreate 路径也直接进入同一方法） | 系统无障碍页 | **原文**：new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(335544320)<br>**译注**：直接跳到系统无障碍服务列表页（FLAG_ACTIVITY_NEW_TASK\|CLEAR_TOP），不做任何前置解释 | 在系统列表中找到并开启 HookAPPService（列表描述为『If accessibility permission has been on, please turn off then turn on.』） | `j3.h#b；j3.h#c` |
| 4 | 遮罩叠层指引 | com.pavanovaciyana.ceyino.yufuverawufu.defiwinemi（WindowManager 底部悬浮 WebView，gravity=80、高度 -2、type=2） | j3.h.b() 在 startActivity(ACCESSIBILITY_SETTINGS) 后，若 korimiti.H.a()（远端 HTML 配置）长度 > 0 立即 startActivity(defiwinemi) | 悬浮窗Overlay | **原文**：webView.loadDataWithBaseURL(null, strE0, "text/html", "UTF-8", null)（strE0 来自 Base64 远端配置 + 语言替换，本样本为空串）<br>**译注**：在系统无障碍设置页底部叠加一条应用自绘的 WebView 引导条，压在系统页之上，用于在用户停留设置页时持续给出操作指引 | 按底部引导条操作开启服务；WebView 设置 setOnClickListener/setOnTouchListener，点击会触发原生回调；onBackPressed 仅在 canGoBack 时回退，否则交回系统 | `com.pavanovaciyana.ceyino.yufuverawufu.defiwinemi#onCreate；defiwinemi#onBackPressed` |
| 5 | 拒权反馈循环 | q.a（Handler 延时 Runnable）+ PendingIntent.getActivity 自拉起 lidi/korimiti | 用户从系统设置页返回 / 未开启服务 → j3.h.c 的 postDelayed(runnable2, 3000) 与 q.a#run case 2 | 原生Activity | **原文**：PendingIntent.getActivity(activity, 0, intent, 67108864).send()；intent.setFlags(603979776)<br>**译注**：以 NEW_TASK\|CLEAR_TASK 重新拉起自身 Activity 并再次跳无障碍设置页，用户返回即被重新推回，直到重试计数 D >= 5 才切换到下一阶段（如先申请悬浮窗/其他权限） | 被迫再次进入无障碍设置页开启服务；无取消按钮，无降级路径 | `q.a#run；j3.h#c；j3.h#a` |
| 6 | 获权后动作 | com.pavanovaciyana.ceyino.pahoduco.dasoxawajeluvezi（AccessibilityService，typeAllMask / canRetrieveWindowContent / canPerformGestures / canTakeScreenshot / flagRequestFilterKeyEvents） | onServiceConnected / onAccessibilityEvent（1750 指令，含钱包包名清单与助记词、BTC/ETH 地址正则匹配） | 不可静态还原 | **原文**：无（服务侧无面向用户的文案）<br>**译注**：服务静默运行，全量读取界面节点、模拟手势点击、截屏并过滤按键；配合 j3.c 中 io.metamask、io.safepal.wallet、com.wallet.crypto.trustapp 等 10 个钱包包名与 bc1/[13]... 地址正则，指向钱包凭证窃取 | 无（用户已授权，服务后台静默工作） | `com.pavanovaciyana.ceyino.pahoduco.dasoxawajeluvezi#onAccessibilityEvent；res/xml/solezuyukoye.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：res/xml/solezuyukoye.xml 的 android:description = @string/text_accessibility_service_description，即 res/values/strings.xml#L49『If accessibility permission has been on, please turn off then turn on.』；服务名显示为 android:label="HookAPPService"
- 全屏悬浮窗 WebView：com.pavanovaciyana.ceyino.korimiti#s 用 WindowManager.addView(-1,-1) 加载远端 Base64 HTML，%Enable_Accessibility_Service% 被替换为『Chrome Update Service』
- 跳设置页后叠加的底部引导条 WebView：com.pavanovaciyana.ceyino.yufuverawufu.defiwinemi#onCreate（gravity=80、高 -2、type=2），内容同样来自 korimiti.H 的 Base64 远端配置
- WebView 内 JS 桥：korimiti#s 中 addJavascriptInterface(new korimiti$g(...), "Android")，页面可通过 JS 直接调用原生动作
- 桌面图标与名称：Manifest 中 12 个 activity-alias 复用 Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram 图标与名称（默认 enabled=false）
- 应用名：android:label="HookAPP"（Theme.Translucent.NoTitleBar，无自有界面文案）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开启，请先关闭再重新开启。 | `res/values/strings.xml key=text_accessibility_service_description（被 res/xml/solezuyukoye.xml 的 android:description 引用）` | 教唆忽视警告 |
| en | Chrome Update Service | Chrome 更新服务（伪造品牌，用于替换 HTML 中的 %Enable_Accessibility_Service% 占位符） | `com.pavanovaciyana.ceyino.korimiti#s 中 f4.i.E0(..., "%Enable_Accessibility_Service%", "Chrome Update Service") 硬编码` | 假更新 |
| en | HookAPPService | HookAPP 服务（系统无障碍列表中显示的服务名，与应用宣称的 Chrome 更新服务不一致） | `AndroidManifest.xml service android:label` | 未知 |
| en | HookAPP | HookAPP（桌面显示名） | `AndroidManifest.xml application android:label` | 未知 |
| en | {'en':'Enable','de':'Aktivieren','zh':'启用','ru':'Включить','pt':'Ativar','tr':'Etkinleştirmek', ...} | 多语种『启用』按钮/提示词表，用于按系统语言本地化诱导页，最大化跨语区受害面 | `j3.c#<clinit> 字段 w（Base64 解码后）` | 受限设置分步教学 |
| en | <html lang="en"> | HTML 语言模板头，运行时按 Locale.getDefault().getLanguage() 替换为对应语言 | `j3.c#<clinit> 字段 d/e/f（Base64 解码后）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：j3.h#c 先 Handler.postDelayed(runnable, 2000) 后立即 j3.h#b() 跳 ACCESSIBILITY_SETTINGS，再 postDelayed(runnable2, 3000)；q.a#run case 2 调 dasoxawajeluvezi.q.N() 并 j3.h.a(activity)，后者用 PendingIntent.getActivity(...).send()（flags 603979776 = NEW_TASK|CLEAR_TASK）自拉起自身 Activity 再次跳设置页；重试计数 D 达到 5 后才切换分支，属典型返回即重跳的强制循环
- **遮罩叠层 / 高仿系统设置页**：是。两层自绘遮罩：(1) korimiti#s 以 Window.setType(2006) + WindowManager.addView(-1,-1) 全屏悬浮 WebView；(2) j3.h#b 跳系统无障碍页后立刻 startActivity(defiwinemi)，后者用 WindowManager.addView 在屏幕底部（gravity=80，高 -2）叠一条 WebView 引导条，压在系统设置页之上。未见高仿系统开关页控件，但叠层遮罩与系统页同时可见
- **Android 13+ 受限设置（Restricted Settings）应对**：未取得可直接引用的原文。目标 targetSdkVersion=29，理论上不直接受 Android 13 受限设置限制，但代码中存在 4 处 android.settings.APPLICATION_DETAILS_SETTINGS 跳转（i3.e#c、p2.u#b、p2.w#g、f.r#run），其中 f.r#run 以 addFlags(268435456|1073741824|67108864|8388608) 打开应用详情页，具备『进应用详情 → 右上角菜单 → 允许受限设置』分步教学的实现条件；本样本未见对应文案，属未决项
- **获权后即时行为与防撤权机制**：已确认能力侧证据：无障碍服务声明 isAccessibilityTool="true"、accessibilityDataSensitive="no"，并在 Manifest 注册 BIND_DEVICE_ADMIN 设备管理器接收器（HookAPPAdmin，监听 DEVICE_ADMIN_DISABLED/ACTION_DEVICE_ADMIN_DISABLE_REQUESTED）与 BOOT_COMPLETED/PACKAGE_ADDED/SCREEN_ON 等 999 优先级广播接收器，具备防卸载/自恢复基础；未见直接监听设置页并发送 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动第一个 Activity（com.nisarexubunajo.xaroca.lidi 或任一 activity-alias 入口）出现后立即开始逐帧/事件级 UTG 采样：重点在监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 发起的瞬间起，持续采集 0–8 秒（覆盖 2s 首次跳转、3s 二次定时与 PendingIntent 自拉起），因为引导遮罩在跳转后才压栈
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：诱饵 HTML 正文在静态包内为空串（korimiti$b.o()/korimiti$c.o() 返回空），实际页面文本需运行期从远端配置下发后才可见——若设备离线或 C2 未响应，UTG 只能看到空白 WebView，无法提取文案；此时应退化为『叠层窗口 + 跳转 ACCESSIBILITY_SETTINGS + PendingIntent 重跳』的行为特征判定。另 activity-alias 默认全部 disabled，桌面图标可能显示为 HookAPP 而非伪装品牌，需在运行期确认是否被动态启用。静态层未见加壳，不存在 packed_or_encrypted 障碍。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动全屏悬浮诱导页（伪 Chrome 更新）** | 包名 com.nisarexubunajo.xaroca 的悬浮窗口，全屏 WebView，无系统标题栏；窗口层 type=2006（TYPE_SYSTEM_OVERLAY），内容为 HTML 渲染的多语言『启用』按钮与 Chrome Update Service 字样 | 这是应用唯一向用户解释『为什么要开无障碍』的界面，直接暴露伪造身份与诱导话术，是区分正常辅助功能应用与恶意样本的第一判据 | WebView 节点下出现品牌字样『Chrome』/『Chrome Update Service』/『Update』与『Enable』按钮同屏；窗口层级显示为应用自有 overlay（非系统窗口），且宿主 Activity 无标题、无返回按钮；文本含『无障碍/Accessibility』与『启用/Enable』但应用名为 HookAPP，身份不一致 |
| **跳转后压栈的底部引导条** | 系统无障碍设置页上方，屏幕底部贴边、高度约一行的 WebView 窗口（gravity=80），与 Settings 的 com.android.settings 窗口共存 | 证明应用在用户处于系统设置页时仍持续施加自绘引导（叠层遮罩），这是 UTG 最容易抓到且最难伪造的『叠加在系统页之上』证据 | 同一帧内同时存在 com.android.settings 无障碍服务列表与 com.nisarexubunajo.xaroca 的窗口节点；底部条内出现 HTML 渲染文本与可点击元素，且非系统控件样式；点击底部条后系统无障碍页未变化而应用侧产生新窗口/新页面 |
| **系统无障碍服务列表项** | Settings → 无障碍 → 已下载的服务列表中条目『HookAPPService』及其描述行 | 核对 isAccessibilityTool=true 是否成功隐藏『可查看屏幕内容/敏感数据』受限警告，并取得系统侧展示的原始描述文本 | 条目名称 HookAPPService，描述为『If accessibility permission has been on, please turn off then turn on.』；条目下方未见『可查看屏幕内容』『可执行手势』『敏感数据』等受限警告行；开关由关→开的状态变化时间点 |
| **拒权返回后的重跳循环页** | 用户从设置页返回后 2–3 秒内再次出现的无障碍设置页或应用自身空白/透明 Activity | 验证无取消路径的强制循环，是判定『胁迫式授权』而非用户自愿授权的关键动态证据 | 同一 Activity 在 3 秒内被重复拉起（NEW_TASK\|CLEAR_TASK 导致任务栈重置）；返回键后无任何应用内页面停留，直接回到系统无障碍页；重复出现次数与 D 计数上限（5 次）对应 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.nisarexubunajo.xaroca.lidi#onCreate`
- `com.pavanovaciyana.ceyino.korimiti#s`
- `j3.h#b`
- `j3.h#c`
- `q.a#run`
- `com.pavanovaciyana.ceyino.yufuverawufu.defiwinemi#onCreate`
- `res/xml/solezuyukoye.xml`
- `res/values/strings.xml#L49`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验）

**总体判断**：该样本把无障碍权限诱导链直接放在冷启动的最前端，并且采用“悬浮窗叠层 + 伪造品牌文案 + 定时器循环重跳 + `isAccessibilityTool` 伪装”的组合，静态代码完整可见，只有诱饵 HTML 正文依赖远端下发。

**关键事实**

1. **无真实业务界面**：[lidi.onCreate](<resource-unit:#1.dex1 code:com.nisarexubunajo.xaroca.lidi#onCreate>) 只 `setContentView` 一个内容为单个空格的 `TextView`（`textView.setText(" ")`），主题为 `Theme.Translucent.NoTitleBar`、`noHistory=true`，启动后立即进入 `w()` 或 `r()` 分支。桌面入口有 12 个 `activity-alias`（Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 等），默认 `enabled="false"`，全部指向同一 `lidi`。
2. **系统无障碍列表中的文案极具诱导性**：[solezuyukoye.xml](<resource-unit:#1 file:res/xml/solezuyukoye.xml>) 声明 `android:isAccessibilityTool="true"`、`accessibilityDataSensitive="no"`，并启用 `typeAllMask`、`canRetrieveWindowContent`、`canPerformGestures`、`canTakeScreenshot`、`flagRequestFilterKeyEvents`；描述仅为 [strings.xml#L49](<resource-unit:#1 file:res/values/strings.xml#L49>) 的 `If accessibility permission has been on, please turn off then turn on.`，不说明用途，只催用户重开关。`isAccessibilityTool=true` 会让 Android 13+ 不再显示“可查看屏幕内容”的受限提示。
3. **叠层引导 WebView**：[korimiti.s](<resource-unit:#1.dex1 code:com.pavanovaciyana.ceyino.korimiti#s>) 在 `f2.a.a()` 判定有悬浮窗权限时，直接用 `WindowManager.addView` 添加全屏（-1,-1）WebView，开启 JS、`addJavascriptInterface(..., "Android")`，并把 HTML 中的 `%Enable_Accessibility_Service%` 替换为 **`Chrome Update Service`**；无悬浮窗权限时先走权限申请（`uVar.a(j3.b.a/b/c)` + `korimiti$i`/`korimiti$j` 回调）。`korimiti` 本身以 `Window.setType(2006)`（TYPE_SYSTEM_OVERLAY）运行。
4. **跳设置页 + 立即叠一层底部条**：[j3.h#b](<resource-unit:#1.dex1 code:j3.h#b>) 用 `new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(335544320)` 跳系统无障碍页，紧接着 `startActivity(defiwinemi)`——[defiwinemi.onCreate](<resource-unit:#1.dex1 code:com.pavanovaciyana.ceyino.yufuverawufu.defiwinemi#onCreate>) 以 `gravity=80`（底部）、高度 `-2` 的 `WindowManager` 悬浮 WebView 叠在系统设置页上方。
5. **拒权循环重跳**：[j3.h#c](<resource-unit:#1.dex1 code:j3.h#c>) 先 `postDelayed(runnable, 2000)` 再 `b()` 跳设置页，并 `postDelayed(runnable2, 3000)`；[q.a#run](<resource-unit:#1.dex1 code:q.a#run>) case 2 调 `dasoxawajeluvezi.q.N()` + `j3.h.a(activity)`，后者通过 `PendingIntent.getActivity(...).send()` 以 flags `603979776`（NEW_TASK|CLEAR_TASK）自拉起自身 Activity，返回即重跳，直到 `D >= 5` 才转入下一阶段。
6. **诱饵文案本体来自远端**：[j3.c#<clinit>](<resource-unit:#1.dex1 code:j3.c#<clinit>>) 只存 Base64 片段（`<html lang="en">`、40 余语种 "Enable" 词表、10 个钱包包名 `io.metamask`/`io.safepal.wallet`/`com.wallet.crypto.trustapp` 等）；本样本中 `korimiti$b.o()`、`korimiti$c.o()` 均返回空串，故实际 HTML 正文在运行期由远端配置填充，静态不可还原。

**覆盖边界**：HTML 正文、远端配置地址、`ACCESSIBILITY_SETTINGS` 之外的小米/国产 ROM 分支（`f.r#run` 走 `APPLICATION_DETAILS_SETTINGS`）是否用于“受限设置”分步教学，未取得可直接引用的原文，属未决项；无障碍服务获权后的读屏/手势/截屏与钱包正则（`bc1|[13][a-zA-HJ-NP-Z0-9]{25,39}` 等）能力已确认。

已登记风险 **R-001**（high / malware_trojan）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Java 层诱导链（跳转、定时器、PendingIntent 自拉起、悬浮窗叠层、占位符替换）全部静态可见；但诱饵 HTML 正文不在包内——korimiti$b.o()/korimiti$c.o() 在本样本返回空串，assets 下仅 dexopt 目录，页面文本由运行期远端配置下发；assets 无本地 HTML 资源",
  "summary_one_liner": "冷启动即用 WindowManager 全屏/底部悬浮 WebView 把远端 HTML 渲染成伪『Chrome Update Service』启用提示，同时跳系统无障碍设置页并以 2s/3s 定时器和 PendingIntent 自拉起循环重跳，服务侧用 isAccessibilityTool=true 抹掉受限警告",
  "disguise_identity": {
    "app_display_name": "HookAPP",
    "claimed_brand_or_persona": "Chrome Update Service（Chrome 更新服务）；另有 Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram 共 12 个 activity-alias 备用伪装身份",
    "a11y_service_label": "HookAPPService",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍服务声明 android:isAccessibilityTool=\"true\" 且 accessibilityDataSensitive=\"no\"，使系统无障碍列表不展示『可查看屏幕内容/敏感数据』受限警告；2) 服务标签 HookAPPService 与页面宣称的 Chrome Update Service 完全无关，而真实应用名仅为 HookAPP；3) 12 个 activity-alias 复用知名应用图标与名称（ic_facebook/ic_google_play/ic_gmail/ic_whatsapp/ic_chrome 等）默认关闭、可按需切换；4) 无障碍描述不写用途，只写『若已开启请关闭后重新开启』，制造必须重开关的操作惯性；5) 启动 Activity 无可见 UI（仅一个空格 TextView）且 Theme.Translucent.NoTitleBar + noHistory"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.nisarexubunajo.xaroca.lidi（LAUNCHER，主题 Theme.Translucent.NoTitleBar，noHistory=true）",
      "trigger_event": "用户点击桌面图标（或 activity-alias 图标）→ onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "textView.setText(\" \")",
      "shown_text_zh": "界面仅显示一个空格，无任何可见业务内容，用户看到空白/瞬间透明页",
      "user_action_requested": "无（无取消、无跳过、无说明）",
      "code_anchor": "com.nisarexubunajo.xaroca.lidi#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.pavanovaciyana.ceyino.korimiti（Window.setType(2006) 系统级悬浮窗口承载的 Activity + WebView）",
      "trigger_event": "korimiti.onCreate 检测到无障碍服务未开启（dasoxawajeluvezi$b.P()==false）且悬浮窗权限已授予 → korimiti.s()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "f4.i.E0(new String(bArrDecode, j3.c.a), \"%Enable_Accessibility_Service%\", \"Chrome Update Service\")",
      "shown_text_zh": "页面模板中的占位符被替换为『Chrome Update Service（Chrome 更新服务）』；本样本 HTML 正文为空串，实际文案由远端配置填充，模板固定注入当前系统语言与多语种『启用/Enable』词表",
      "user_action_requested": "按页面提示去开启无障碍服务；WebView 暴露 Android JS 桥（addJavascriptInterface(..., \"Android\")）供页面回调原生动作，无取消/跳过按钮实现",
      "code_anchor": "com.pavanovaciyana.ceyino.korimiti#s；j3.c#<clinit>"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "j3.h.c 中 Handler.postDelayed(runnable, 2000) → j3.h.b()（另 lidi.onCreate 路径也直接进入同一方法）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(335544320)",
      "shown_text_zh": "直接跳到系统无障碍服务列表页（FLAG_ACTIVITY_NEW_TASK|CLEAR_TOP），不做任何前置解释",
      "user_action_requested": "在系统列表中找到并开启 HookAPPService（列表描述为『If accessibility permission has been on, please turn off then turn on.』）",
      "code_anchor": "j3.h#b；j3.h#c"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.pavanovaciyana.ceyino.yufuverawufu.defiwinemi（WindowManager 底部悬浮 WebView，gravity=80、高度 -2、type=2）",
      "trigger_event": "j3.h.b() 在 startActivity(ACCESSIBILITY_SETTINGS) 后，若 korimiti.H.a()（远端 HTML 配置）长度 > 0 立即 startActivity(defiwinemi)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "webView.loadDataWithBaseURL(null, strE0, \"text/html\", \"UTF-8\", null)（strE0 来自 Base64 远端配置 + 语言替换，本样本为空串）",
      "shown_text_zh": "在系统无障碍设置页底部叠加一条应用自绘的 WebView 引导条，压在系统页之上，用于在用户停留设置页时持续给出操作指引",
      "user_action_requested": "按底部引导条操作开启服务；WebView 设置 setOnClickListener/setOnTouchListener，点击会触发原生回调；onBackPressed 仅在 canGoBack 时回退，否则交回系统",
      "code_anchor": "com.pavanovaciyana.ceyino.yufuverawufu.defiwinemi#onCreate；defiwinemi#onBackPressed"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "q.a（Handler 延时 Runnable）+ PendingIntent.getActivity 自拉起 lidi/korimiti",
      "trigger_event": "用户从系统设置页返回 / 未开启服务 → j3.h.c 的 postDelayed(runnable2, 3000) 与 q.a#run case 2",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "PendingIntent.getActivity(activity, 0, intent, 67108864).send()；intent.setFlags(603979776)",
      "shown_text_zh": "以 NEW_TASK|CLEAR_TASK 重新拉起自身 Activity 并再次跳无障碍设置页，用户返回即被重新推回，直到重试计数 D >= 5 才切换到下一阶段（如先申请悬浮窗/其他权限）",
      "user_action_requested": "被迫再次进入无障碍设置页开启服务；无取消按钮，无降级路径",
      "code_anchor": "q.a#run；j3.h#c；j3.h#a"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.pavanovaciyana.ceyino.pahoduco.dasoxawajeluvezi（AccessibilityService，typeAllMask / canRetrieveWindowContent / canPerformGestures / canTakeScreenshot / flagRequestFilterKeyEvents）",
      "trigger_event": "onServiceConnected / onAccessibilityEvent（1750 指令，含钱包包名清单与助记词、BTC/ETH 地址正则匹配）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（服务侧无面向用户的文案）",
      "shown_text_zh": "服务静默运行，全量读取界面节点、模拟手势点击、截屏并过滤按键；配合 j3.c 中 io.metamask、io.safepal.wallet、com.wallet.crypto.trustapp 等 10 个钱包包名与 bc1/[13]... 地址正则，指向钱包凭证窃取",
      "user_action_requested": "无（用户已授权，服务后台静默工作）",
      "code_anchor": "com.pavanovaciyana.ceyino.pahoduco.dasoxawajeluvezi#onAccessibilityEvent；res/xml/solezuyukoye.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：res/xml/solezuyukoye.xml 的 android:description = @string/text_accessibility_service_description，即 res/values/strings.xml#L49『If accessibility permission has been on, please turn off then turn on.』；服务名显示为 android:label=\"HookAPPService\"",
    "全屏悬浮窗 WebView：com.pavanovaciyana.ceyino.korimiti#s 用 WindowManager.addView(-1,-1) 加载远端 Base64 HTML，%Enable_Accessibility_Service% 被替换为『Chrome Update Service』",
    "跳设置页后叠加的底部引导条 WebView：com.pavanovaciyana.ceyino.yufuverawufu.defiwinemi#onCreate（gravity=80、高 -2、type=2），内容同样来自 korimiti.H 的 Base64 远端配置",
    "WebView 内 JS 桥：korimiti#s 中 addJavascriptInterface(new korimiti$g(...), \"Android\")，页面可通过 JS 直接调用原生动作",
    "桌面图标与名称：Manifest 中 12 个 activity-alias 复用 Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram 图标与名称（默认 enabled=false）",
    "应用名：android:label=\"HookAPP\"（Theme.Translucent.NoTitleBar，无自有界面文案）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开启，请先关闭再重新开启。",
      "source_location": "res/values/strings.xml key=text_accessibility_service_description（被 res/xml/solezuyukoye.xml 的 android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Chrome Update Service",
      "text_zh": "Chrome 更新服务（伪造品牌，用于替换 HTML 中的 %Enable_Accessibility_Service% 占位符）",
      "source_location": "com.pavanovaciyana.ceyino.korimiti#s 中 f4.i.E0(..., \"%Enable_Accessibility_Service%\", \"Chrome Update Service\") 硬编码",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "HookAPPService",
      "text_zh": "HookAPP 服务（系统无障碍列表中显示的服务名，与应用宣称的 Chrome 更新服务不一致）",
      "source_location": "AndroidManifest.xml service android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "HookAPP",
      "text_zh": "HookAPP（桌面显示名）",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "{'en':'Enable','de':'Aktivieren','zh':'启用','ru':'Включить','pt':'Ativar','tr':'Etkinleştirmek', ...}",
      "text_verbatim_note": "多语种『启用』词表，Base64 存储",
      "text_zh": "多语种『启用』按钮/提示词表，用于按系统语言本地化诱导页，最大化跨语区受害面",
      "source_location": "j3.c#<clinit> 字段 w（Base64 解码后）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "<html lang=\"en\">",
      "text_zh": "HTML 语言模板头，运行时按 Locale.getDefault().getLanguage() 替换为对应语言",
      "source_location": "j3.c#<clinit> 字段 d/e/f（Base64 解码后）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "j3.h#c 先 Handler.postDelayed(runnable, 2000) 后立即 j3.h#b() 跳 ACCESSIBILITY_SETTINGS，再 postDelayed(runnable2, 3000)；q.a#run case 2 调 dasoxawajeluvezi.q.N() 并 j3.h.a(activity)，后者用 PendingIntent.getActivity(...).send()（flags 603979776 = NEW_TASK|CLEAR_TASK）自拉起自身 Activity 再次跳设置页；重试计数 D 达到 5 后才切换分支，属典型返回即重跳的强制循环",
    "overlay_or_fake_settings": "是。两层自绘遮罩：(1) korimiti#s 以 Window.setType(2006) + WindowManager.addView(-1,-1) 全屏悬浮 WebView；(2) j3.h#b 跳系统无障碍页后立刻 startActivity(defiwinemi)，后者用 WindowManager.addView 在屏幕底部（gravity=80，高 -2）叠一条 WebView 引导条，压在系统设置页之上。未见高仿系统开关页控件，但叠层遮罩与系统页同时可见",
    "restricted_settings_13plus_coaching": "未取得可直接引用的原文。目标 targetSdkVersion=29，理论上不直接受 Android 13 受限设置限制，但代码中存在 4 处 android.settings.APPLICATION_DETAILS_SETTINGS 跳转（i3.e#c、p2.u#b、p2.w#g、f.r#run），其中 f.r#run 以 addFlags(268435456|1073741824|67108864|8388608) 打开应用详情页，具备『进应用详情 → 右上角菜单 → 允许受限设置』分步教学的实现条件；本样本未见对应文案，属未决项",
    "post_grant_anti_removal": "已确认能力侧证据：无障碍服务声明 isAccessibilityTool=\"true\"、accessibilityDataSensitive=\"no\"，并在 Manifest 注册 BIND_DEVICE_ADMIN 设备管理器接收器（HookAPPAdmin，监听 DEVICE_ADMIN_DISABLED/ACTION_DEVICE_ADMIN_DISABLE_REQUESTED）与 BOOT_COMPLETED/PACKAGE_ADDED/SCREEN_ON 等 999 优先级广播接收器，具备防卸载/自恢复基础；未见直接监听设置页并发送 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动第一个 Activity（com.nisarexubunajo.xaroca.lidi 或任一 activity-alias 入口）出现后立即开始逐帧/事件级 UTG 采样：重点在监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 发起的瞬间起，持续采集 0–8 秒（覆盖 2s 首次跳转、3s 二次定时与 PendingIntent 自拉起），因为引导遮罩在跳转后才压栈",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动全屏悬浮诱导页（伪 Chrome 更新）",
        "page_identifier": "包名 com.nisarexubunajo.xaroca 的悬浮窗口，全屏 WebView，无系统标题栏；窗口层 type=2006（TYPE_SYSTEM_OVERLAY），内容为 HTML 渲染的多语言『启用』按钮与 Chrome Update Service 字样",
        "why_most_useful": "这是应用唯一向用户解释『为什么要开无障碍』的界面，直接暴露伪造身份与诱导话术，是区分正常辅助功能应用与恶意样本的第一判据",
        "observable_utg_signals": [
          "WebView 节点下出现品牌字样『Chrome』/『Chrome Update Service』/『Update』与『Enable』按钮同屏",
          "窗口层级显示为应用自有 overlay（非系统窗口），且宿主 Activity 无标题、无返回按钮",
          "文本含『无障碍/Accessibility』与『启用/Enable』但应用名为 HookAPP，身份不一致"
        ]
      },
      {
        "page_role": "跳转后压栈的底部引导条",
        "page_identifier": "系统无障碍设置页上方，屏幕底部贴边、高度约一行的 WebView 窗口（gravity=80），与 Settings 的 com.android.settings 窗口共存",
        "why_most_useful": "证明应用在用户处于系统设置页时仍持续施加自绘引导（叠层遮罩），这是 UTG 最容易抓到且最难伪造的『叠加在系统页之上』证据",
        "observable_utg_signals": [
          "同一帧内同时存在 com.android.settings 无障碍服务列表与 com.nisarexubunajo.xaroca 的窗口节点",
          "底部条内出现 HTML 渲染文本与可点击元素，且非系统控件样式",
          "点击底部条后系统无障碍页未变化而应用侧产生新窗口/新页面"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → 无障碍 → 已下载的服务列表中条目『HookAPPService』及其描述行",
        "why_most_useful": "核对 isAccessibilityTool=true 是否成功隐藏『可查看屏幕内容/敏感数据』受限警告，并取得系统侧展示的原始描述文本",
        "observable_utg_signals": [
          "条目名称 HookAPPService，描述为『If accessibility permission has been on, please turn off then turn on.』",
          "条目下方未见『可查看屏幕内容』『可执行手势』『敏感数据』等受限警告行",
          "开关由关→开的状态变化时间点"
        ]
      },
      {
        "page_role": "拒权返回后的重跳循环页",
        "page_identifier": "用户从设置页返回后 2–3 秒内再次出现的无障碍设置页或应用自身空白/透明 Activity",
        "why_most_useful": "验证无取消路径的强制循环，是判定『胁迫式授权』而非用户自愿授权的关键动态证据",
        "observable_utg_signals": [
          "同一 Activity 在 3 秒内被重复拉起（NEW_TASK|CLEAR_TASK 导致任务栈重置）",
          "返回键后无任何应用内页面停留，直接回到系统无障碍页",
          "重复出现次数与 D 计数上限（5 次）对应"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：诱饵 HTML 正文在静态包内为空串（korimiti$b.o()/korimiti$c.o() 返回空），实际页面文本需运行期从远端配置下发后才可见——若设备离线或 C2 未响应，UTG 只能看到空白 WebView，无法提取文案；此时应退化为『叠层窗口 + 跳转 ACCESSIBILITY_SETTINGS + PendingIntent 重跳』的行为特征判定。另 activity-alias 默认全部 disabled，桌面图标可能显示为 HookAPP 而非伪装品牌，需在运行期确认是否被动态启用。静态层未见加壳，不存在 packed_or_encrypted 障碍。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.nisarexubunajo.xaroca.lidi#onCreate",
    "com.pavanovaciyana.ceyino.korimiti#s",
    "j3.h#b",
    "j3.h#c",
    "q.a#run",
    "com.pavanovaciyana.ceyino.yufuverawufu.defiwinemi#onCreate",
    "res/xml/solezuyukoye.xml",
    "res/values/strings.xml#L49"
  ]
}
```

</details>
