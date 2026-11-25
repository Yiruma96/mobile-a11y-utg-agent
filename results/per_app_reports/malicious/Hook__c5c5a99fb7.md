# MB_091__c5c5a99fb7｜Hook — Googlecom

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：163.9s

## 1. 一句话核心结论

- **核心申请方式**：冷启动空白页静默判定无障碍未开启后，用 type=2006 系统级悬浮窗 Activity 加载远端 Base64 HTML 引导页，再跳系统无障碍设置并叠加底部 WebView 遮罩，配合 2000/3000ms 定时器与 PendingIntent 自重启循环逼迫用户开启标名为 Contacts 的无障碍服务。
- **静态可见性说明**：Manifest、无障碍配置、strings.xml 明文可读；跳转与循环逻辑（u2.h、nazemidu、vifolulasomitayu）静态完全可还原；但引导页 HTML 正文以 Base64 存于运行时数据源（nazemidu.y/z 的初值来自 SharedPreferences/远端下发），仅模板片段（<html lang> 等）硬编码在 u2.i，逐字文案不可静态获取。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c5c5a99fb79efb383586ed7f7e16419dbb2b02a829aa0f976eadce9581edba44` |
| 包名 / 年份 | `com.sonirupiwebidoti.geyosego` / 2024 |
| 家族 / 品类 | **Hook**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Googlecom |
| 引导页宣称品牌/身份 | Google 系产品家族（Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram、TikTok、Telegram 共 10 个 activity-alias 与对应图标） |
| 系统无障碍列表服务名 | Contacts |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 11 个 activity-alias 共用同一 targetActivity 做图标/名称伪装，默认 enabled=false，运行期用 setComponentEnabledSetting 动态启停；2) 无障碍服务 label 设为 Contacts，description 写成『若已开启请先关再开』的刷新口吻以降低戒心；3) 引导页跑在 type=2006 系统悬浮窗中，不占用应用界面，用户难以判断来源；4) 全部类名/包名混淆（com.repexetuzibi.zucu.*、u2.h、r3.a0）；5) 主界面 setContentView 仅为单空格 TextView，桌面点击后无可见界面。 |
| 无障碍服务类名 | `com.repexetuzibi.zucu.cisehe.nalamoti` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | If accessibility permission has been on, please turn off then turn on. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sonirupiwebidoti.geyosego.duxazociwudexa（LAUNCHER，label=Googlecom，Theme.Translucent.NoTitleBar，noHistory，excludeFromRecents） | 用户点击桌面图标（含任意 activity-alias 图标）→ onCreate | 原生Activity | 仅设置一个内容为单个空格的 TextView，界面呈全屏空白/透明，不展示任何真实功能 | 无（用户看到空白页，无任何按钮或说明） | `com.sonirupiwebidoti.geyosego.duxazociwudexa.onCreate` |
| 2 | 业务功能触发 | r3.a0#b0 读取 Settings.Secure "enabled_accessibility_services" 判定本服务是否已启用；未启用则调用 a.b(this) | duxazociwudexa.onCreate 中 if (!nazemidu$d.b(this)) { a.b(this); return; } | 不可静态还原 | 无 | 无 | `r3.a0#b0 / com.sonirupiwebidoti.geyosego.duxazociwudexa.onCreate` |
| 3 | 引导说明页 | com.repexetuzibi.zucu.nazemidu（getWindow().setType(2006) 系统悬浮窗 + 全屏 WebView，JS 桥名 Android） | nazemidu.onCreate → nazemidu.r() 创建 WebView 并 WindowManager.addView(-1,-1,type=2,flags=0x40000) | 悬浮窗Overlay | **原文**：不可静态还原（Base64.decode(y.a()) 注入的 HTML，按 Locale 替换 <html lang="en"> 为 <html lang="<language>">）<br>**译注**：远端下发的多语言引导页，内容随设备语言切换，静态不可读 | 引导用户在页面上点击（点击后经 JS 桥 nazemidu$g.onData 回调） | `com.repexetuzibi.zucu.nazemidu.r / com.repexetuzibi.zucu.nazemidu.onCreate / u2.i` |
| 4 | 跳受限设置 | u2.h.c(Activity) → 2000ms 后 u2.h.b() | nazemidu.q()（WebView 引导页点击回调后关闭页面）→ u2.h.c(this) | 不可静态还原 | 无 | 无（自动执行） | `com.repexetuzibi.zucu.nazemidu#q / u2.h#c` |
| 5 | 跳无障碍设置 | Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(335544320 /* NEW_TASK\|CLEAR_TOP */) → 系统无障碍服务列表页 | u2.h.b() 中 activity2.startActivity(intentAddFlags) | 系统无障碍页 | **原文**：无（跳转系统页，页面内容由系统渲染）<br>**译注**：直接把用户送到系统无障碍服务列表，列表中该服务显示为 Contacts | 要求用户在列表中找到 Contacts 并打开开关；页面无本应用提供的取消/跳过控件 | `u2.h#b` |
| 6 | 遮罩叠层指引 | com.repexetuzibi.zucu.xadosawasutumula.vifolulasomitayu（WindowManager 叠加 -1 x -2、type=2、flags=0x40008 NOT_FOCUSABLE\|LAYOUT_NO_LIMITS、gravity=BOTTOM 的 WebView） | u2.h.b() 在 startActivity(ACCESSIBILITY_SETTINGS) 之后立即 startActivity(vifolulasomitayu, flags=0x10000000\|0x8000 或 0x800000) | 悬浮窗Overlay | **原文**：不可静态还原（Base64.decode(nazemidu.z.a()) 的 HTML，同样做 <html lang> 语言替换）<br>**译注**：贴在系统无障碍页底部的半透明引导条，提示用户在该页操作 | 按悬浮条指引在系统页中勾选 Contacts 服务；无关闭按钮（不可聚焦且铺满宽度） | `com.repexetuzibi.zucu.xadosawasutumula.vifolulasomitayu#onCreate` |
| 7 | 拒权反馈循环 | u2.h.c 的 Handler 定时链（u2.b.a() → HandlerThread "mainHandlerThread"）+ u2.h.a() 的 PendingIntent 自重启 | Handler.postDelayed(runnable, 2000) 与 postDelayed(self, 3000)；以及 u2.d.run → u2.h.a(activity) 的 PendingIntent.getActivity(...).send() | 不可静态还原 | 无 | 被迫开启无障碍；无退出路径（onBackPressed 仅 super，onDestroy 亦不移除定时器） | `u2.h#c / u2.h#a / u2.d#run` |
| 8 | 获权后动作 | com.repexetuzibi.zucu.cisehe.nalamoti 连接成功 → duxazociwudexa.u()/v()/r()/s() | nazemidu$d.b(this) 返回 true（enabled_accessibility_services 已含本服务）→ duxazociwudexa.onCreate 走 u(); v(); | 原生Activity | 无 | 无（自动完成，用户无法感知权限已被用于后续自动化操作） | `com.sonirupiwebidoti.geyosego.duxazociwudexa#r / #s / #v / com.repexetuzibi.zucu.cisehe.nalamoti` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表中该条目的服务名：Manifest <service android:label="Contacts">（com.repexetuzibi.zucu.cisehe.nalamoti）
- 系统无障碍服务列表中该条目的说明文字：res/values/strings.xml 的 text_accessibility_service_description = "If accessibility permission has been on, please turn off then turn on."（由 res/xml/silazufunewakahi.xml 的 android:description 引用）
- type=2006 系统悬浮窗 Activity nazemidu 内全屏 WebView：Base64/远端 HTML 引导页（JS 桥 Android，按设备语言替换 <html lang>），静态不可读
- 跳转系统无障碍设置页后叠加的 vifolulasomitayu 底部 WebView 悬浮条（type=2、gravity=BOTTOM、NOT_FOCUSABLE）：Base64/远端 HTML，静态不可读
- 桌面图标与名称：application android:label="Googlecom" 及 10 个 activity-alias 的 label/icon（Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram、TikTok、Telegram），默认关闭、运行期按已装应用动态启用
- 主界面无任何文字（setContentView(new TextView(" "))），设备管理广播接收器 label 为单个空格、description 为 "Add application to admin"

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开启，请先关闭再重新开启。 | `res/values/strings.xml → key text_accessibility_service_description（经 res/xml/silazufunewakahi.xml 的 android:description 引用）` | 教唆忽视警告 |
| en | Contacts | 通讯录 | `AndroidManifest.xml → <service android:name="com.repexetuzibi.zucu.cisehe.nalamoti" android:label="Contacts">；同名 activity-alias label="Contacts"` | 假反诈安全 |
| en | Googlecom | 谷歌公司（拼写残缺的伪造品牌名） | `AndroidManifest.xml → <application android:label="Googlecom">` | 假更新 |
| en | Add application to admin | 将应用添加为设备管理员 | `res/values/strings.xml → key adm（设备管理广播接收器 com.repexetuzibi.zucu.xuriremogo.ruce 的 android:description）` | 未知 |
| en | 不可静态还原：Base64.decode(y.a()) / Base64.decode(nazemidu.z.a()) 注入的 HTML 引导页正文 | 运行时下发的多语言引导文案，静态不可读 | `com.repexetuzibi.zucu.nazemidu.r 与 com.repexetuzibi.zucu.xadosawasutumula.vifolulasomitayu.onCreate（模板片段位于 u2.i）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：u2.h.c 在独立 HandlerThread 上 postDelayed(2000ms) 执行跳转、postDelayed(3000ms) 重跑自身，形成 2 秒跳一次、3 秒一轮的持续重跳；u2.d.run 另经 u2.h.a 用 PendingIntent.send() 以 0x24000000（NEW_TASK|CLEAR_TASK）自重启把用户拉回引导页；nazemidu.onDestroy 与 onBackPressed 均未撤销定时器与悬浮窗。
- **遮罩叠层 / 高仿系统设置页**：双层叠放：① 引导阶段用 getWindow().setType(2006) 把 nazemidu 变成系统级悬浮窗（全屏 WebView）；② 跳系统无障碍设置页后立即 addView 一个 type=2、NOT_FOCUSABLE、gravity=BOTTOM 的 WebView 半透明引导条压在系统页上方。非高仿系统开关页，而是覆盖真实系统页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（应用 targetSdkVersion=28，未使用应用详情页受限设置教学，也未用 Session 安装器绕过；引导文本为远端 HTML，静态不可确认是否含该教学）
- **获权后即时行为与防撤权机制**：获权后由无障碍服务自身能力（canPerformGestures、canRequestFilterKeyEvents、canRetrieveWindowContent、typeAllMask）配合，可自动点击系统授权按钮并在设置页执行全局动作；获权瞬间 duxazociwudexa 先禁用全部 11 个图标别名再按已装目标应用启用对应别名并启动真实应用，完成图标换脸。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS")) 或 PendingIntent.send 重启本应用 Activity 的瞬间立即抓取；也可在 launcher duxazociwudexa 启动后 1-3 秒（首个 2000ms 定时器到期前）开始连续截屏，此时 nazemidu 悬浮窗正在铺满屏幕。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区在引导文案本身：nazemidu 与 vifolulasomitayu 的 HTML 均来自 Base64.decode(y.a()) / z.a()（偏好或远端下发），静态无法获得逐字文本，必须依赖 UTG/截图获取；此外主界面为单空格 TextView、无障碍服务 label 仅『Contacts』，若 UTG 仅在应用常规 Activity 层面采样而忽略 type=2006 悬浮窗，会完全漏掉诱导页。静态无加壳，运行期逻辑完整可见。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的 type=2006 全屏悬浮窗引导页** | 包名 com.sonirupiwebidoti.geyosego 的 WebView 内容 + 无标题栏无导航的全屏 HTML 页面，窗口非 Activity 常规任务栈表现 | 这是唯一的『说明/诱导』文案载体，其文案完全由远端 Base64 决定，静态无法获得，只有 UTG 才能取到真实话术 | HTML 页面标题与正文文本；是否存在『开启无障碍』『Turn on』『Accessibility』关键词；页面是否含伪造的系统设置样式控件；窗口是否覆盖在其他应用/桌面上方（悬浮窗特征） |
| **跳转后压在系统无障碍设置页上的底部引导条** | 系统『设置 → 无障碍 → 已下载的服务』页面上方叠加的底部半透明条（非系统控件，无返回键归属） | 直接证明『遮罩叠层指引』——用户以为自己还在系统设置里操作，实际被第三方浮层引导；同时可确认目标服务条目显示为 Contacts | 系统无障碍列表中出现 label 为 Contacts 的服务项；该服务项 description 为『If accessibility permission has been on, please turn off then turn on.』；底部浮层文本与系统 UI 的层级差异（浮层无系统无障碍节点归属） |
| **拒权返回后的循环重跳现场** | 连续多次出现同一系统无障碍设置页 + 应用自身被重新拉起（Activity 任务被清空重建） | 区分『一次性引导』与『强制循环』，是判定非自愿授权的决定性观测 | 按返回键后 2 秒内无障碍设置页再次出现；同一页面在 10 秒内重复出现 ≥3 次；应用任务栈被 CLEAR_TASK 重建（桌面图标再次闪出） |
| **获权后的图标换脸** | 桌面/最近任务中应用图标变为目标社交应用（Telegram/Facebook/WhatsApp 等），或启动后直接跳进该真实应用 | 证明权限授予后立即发生的身份伪装与后续动作，闭环『诱导→获权→变脸』因果 | 桌面图标与 label 在获权前后变化；启动后 1 秒内跳转到第三方应用界面；无障碍服务在运行服务列表中保持 enabled |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.sonirupiwebidoti.geyosego.duxazociwudexa.onCreate`
- `com.repexetuzibi.zucu.nazemidu.r`
- `u2.h.c / u2.h.b / u2.h.a`
- `com.repexetuzibi.zucu.xadosawasutumula.vifolulasomitayu.onCreate`
- `com.sonirupiwebidoti.geyosego.duxazociwudexa.r`
- `res/xml/silazufunewakahi.xml + res/values/strings.xml#text_accessibility_service_description`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（沿 launcher → 引导 Activity → 系统设置跳转 → 覆盖层 → 循环重拉链）。以下为结论。

## 核心结论要点

- **入口即伪装**：launcher 是 [duxazociwudexa](<resource-unit:#1.dex1 code:com.sonirupiwebidoti.geyosego.duxazociwudexa>)，桌面名为 `Googlecom`，同时声明 10 个默认 `enabled="false"` 的 activity-alias（Facebook / Google Play / Gmail / **Contacts** / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram），全部指向同一 Activity。`onCreate` 仅 `setContentView(new TextView(" "))` 铺一张空白页，配合 `Theme.Translucent.NoTitleBar` + `noHistory` + `FLAG_LAYOUT_NO_LIMITS`，用户看不到任何内容。
- **纯运行期判定**：无障碍是否已开启由 `Settings.Secure "enabled_accessibility_services"` 读取判定（[r3.a0#b0](<resource-unit:#1.dex1 code:r3.a0#b0>)），未开启即走 `a.b(this)` 拉起引导页，已开启则走 `u()/v()` 进入变脸与业务分支——完全无静态弹窗资源。
- **引导页是系统级悬浮窗 + Base64 HTML**：[nazemidu.onCreate()](<resource-unit:#1.dex1 code:com.repexetuzibi.zucu.nazemidu#onCreate>) 用 `getWindow().setType(2006)` 把 Activity 变成系统悬浮窗；[nazemidu.r()](<resource-unit:#1.dex1 code:com.repexetuzibi.zucu.nazemidu#r>) 创建全屏 WebView、开 JS/插件/JS 桥 `Android`，把 `Base64.decode(y.a())` 的 HTML 用 `loadDataWithBaseURL` 注入，并按 `Locale.getDefault().getLanguage()` 替换 `<html lang="en">` 做多语言化（模板常量见 [u2.i](<resource-unit:#1.dex1 code:u2.i>)）。**引导文案本体不在包内明文，来自远端/SharedPreferences 的 Base64 载荷**。
- **拒权即循环重跳**：[u2.h.c()](<resource-unit:#1.dex1 code:u2.h#c>) 通过 `u2.b.a()`（独立 `HandlerThread("mainHandlerThread")`）`postDelayed` 2000ms 后执行 `b()`、3000ms 后重复自身；`b()` 直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(0x14000000))` 跳系统无障碍列表，并紧接着启动覆盖层 Activity。另一条回路 [u2.h.a()](<resource-unit:#1.dex1 code:u2.h#a>) 用 `PendingIntent.send()` 以 `0x24000000`（NEW_TASK|CLEAR_TASK）重新拉起自身，形成"关不掉"的重入。
- **设置页压栈遮罩**：[vifolulasomitayu.onCreate()](<resource-unit:#1.dex1 code:com.repexetuzibi.zucu.xadosawasutumula.vifolulasomitayu#onCreate>) 在跳转无障碍设置页后立刻用 `WindowManager.addView` 叠加一个 `(-1, -2, type=2, flags=0x40008=NOT_FOCUSABLE|LAYOUT_NO_LIMITS, gravity=BOTTOM)` 的 WebView 条，内容同样是 Base64 HTML 且做了语言替换——即"系统无障碍页上浮着的教学条"。
- **伪装身份与说明文案**：无障碍服务 [nalamoti](<resource-unit:#1.dex1 code:com.repexetuzibi.zucu.cisehe.nalamoti>) 在 Manifest 中 `android:label="Contacts"`，`android:description` 为 `If accessibility permission has been on, please turn off then turn on.`（[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L31>)、[silazufunewakahi.xml](<resource-unit:#1 file:res/xml/silazufunewakahi.xml>)）。该说明把高危权限说成"关一次再开一下"的常规刷新操作，同时具备 `canPerformGestures`、`canRequestFilterKeyEvents`、`canRetrieveWindowContent` 等自动点击与按键过滤能力。
- **获权后动作**：[duxazociwudexa.r()](<resource-unit:#1.dex1 code:com.sonirupiwebidoti.geyosego.duxazociwudexa#r>) 先用 `setComponentEnabledSetting(..., 2, 1)` 关闭全部 11 个别名，再按 `getPackageInfo` 探测到的已装目标应用启用对应别名；[v()](<resource-unit:#1.dex1 code:com.sonirupiwebidoti.geyosego.duxazociwudexa#v>) 随即 `startActivity(getLaunchIntentForPackage(...))` 打开该真实应用，使桌面图标与真实应用一致（应用变脸）。
- **与既有风险的关系**：本轮结论与已登记 [R-001]（伪装 Contacts 的无障碍诱导，source_mode=autonomous_audit）一致，并补充了 `vifolulasomitayu` 底部压栈遮罩、2000/3000ms 双定时器与 `PendingIntent` 重入三条细节。

## 静态可见性边界

Manifest、无障碍 XML、`strings.xml` 全部明文可读；**引导 HTML 正文为 Base64、运行时按语言注入，且 `nazemidu.y/z` 初值来自偏好/远端**，因此页面逐字文案无法静态还原 → `partial_dynamic_or_remote`。跳转逻辑、覆盖层参数、循环节奏均静态可证，未加壳、无 VMP。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍配置、strings.xml 明文可读；跳转与循环逻辑（u2.h、nazemidu、vifolulasomitayu）静态完全可还原；但引导页 HTML 正文以 Base64 存于运行时数据源（nazemidu.y/z 的初值来自 SharedPreferences/远端下发），仅模板片段（<html lang> 等）硬编码在 u2.i，逐字文案不可静态获取。",
  "summary_one_liner": "冷启动空白页静默判定无障碍未开启后，用 type=2006 系统级悬浮窗 Activity 加载远端 Base64 HTML 引导页，再跳系统无障碍设置并叠加底部 WebView 遮罩，配合 2000/3000ms 定时器与 PendingIntent 自重启循环逼迫用户开启标名为 Contacts 的无障碍服务。",
  "disguise_identity": {
    "app_display_name": "Googlecom",
    "claimed_brand_or_persona": "Google 系产品家族（Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram、TikTok、Telegram 共 10 个 activity-alias 与对应图标）",
    "a11y_service_label": "Contacts",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 11 个 activity-alias 共用同一 targetActivity 做图标/名称伪装，默认 enabled=false，运行期用 setComponentEnabledSetting 动态启停；2) 无障碍服务 label 设为 Contacts，description 写成『若已开启请先关再开』的刷新口吻以降低戒心；3) 引导页跑在 type=2006 系统悬浮窗中，不占用应用界面，用户难以判断来源；4) 全部类名/包名混淆（com.repexetuzibi.zucu.*、u2.h、r3.a0）；5) 主界面 setContentView 仅为单空格 TextView，桌面点击后无可见界面。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sonirupiwebidoti.geyosego.duxazociwudexa（LAUNCHER，label=Googlecom，Theme.Translucent.NoTitleBar，noHistory，excludeFromRecents）",
      "trigger_event": "用户点击桌面图标（含任意 activity-alias 图标）→ onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": " ",
      "shown_text_zh": "仅设置一个内容为单个空格的 TextView，界面呈全屏空白/透明，不展示任何真实功能",
      "user_action_requested": "无（用户看到空白页，无任何按钮或说明）",
      "code_anchor": "com.sonirupiwebidoti.geyosego.duxazociwudexa.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "r3.a0#b0 读取 Settings.Secure \"enabled_accessibility_services\" 判定本服务是否已启用；未启用则调用 a.b(this)",
      "trigger_event": "duxazociwudexa.onCreate 中 if (!nazemidu$d.b(this)) { a.b(this); return; }",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静默检测无障碍开关状态，无任何可见 UI；未开启即转入引导分支",
      "user_action_requested": "无",
      "code_anchor": "r3.a0#b0 / com.sonirupiwebidoti.geyosego.duxazociwudexa.onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.repexetuzibi.zucu.nazemidu（getWindow().setType(2006) 系统悬浮窗 + 全屏 WebView，JS 桥名 Android）",
      "trigger_event": "nazemidu.onCreate → nazemidu.r() 创建 WebView 并 WindowManager.addView(-1,-1,type=2,flags=0x40000)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "不可静态还原（Base64.decode(y.a()) 注入的 HTML，按 Locale 替换 <html lang=\"en\"> 为 <html lang=\"<language>\">）",
      "shown_text_zh": "远端下发的多语言引导页，内容随设备语言切换，静态不可读",
      "user_action_requested": "引导用户在页面上点击（点击后经 JS 桥 nazemidu$g.onData 回调）",
      "code_anchor": "com.repexetuzibi.zucu.nazemidu.r / com.repexetuzibi.zucu.nazemidu.onCreate / u2.i"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "u2.h.c(Activity) → 2000ms 后 u2.h.b()",
      "trigger_event": "nazemidu.q()（WebView 引导页点击回调后关闭页面）→ u2.h.c(this)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "关闭引导页后延迟 2 秒自动触发跳转，用户无感知间隔",
      "user_action_requested": "无（自动执行）",
      "code_anchor": "com.repexetuzibi.zucu.nazemidu#q / u2.h#c"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(335544320 /* NEW_TASK|CLEAR_TOP */) → 系统无障碍服务列表页",
      "trigger_event": "u2.h.b() 中 activity2.startActivity(intentAddFlags)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转系统页，页面内容由系统渲染）",
      "shown_text_zh": "直接把用户送到系统无障碍服务列表，列表中该服务显示为 Contacts",
      "user_action_requested": "要求用户在列表中找到 Contacts 并打开开关；页面无本应用提供的取消/跳过控件",
      "code_anchor": "u2.h#b"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.repexetuzibi.zucu.xadosawasutumula.vifolulasomitayu（WindowManager 叠加 -1 x -2、type=2、flags=0x40008 NOT_FOCUSABLE|LAYOUT_NO_LIMITS、gravity=BOTTOM 的 WebView）",
      "trigger_event": "u2.h.b() 在 startActivity(ACCESSIBILITY_SETTINGS) 之后立即 startActivity(vifolulasomitayu, flags=0x10000000|0x8000 或 0x800000)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "不可静态还原（Base64.decode(nazemidu.z.a()) 的 HTML，同样做 <html lang> 语言替换）",
      "shown_text_zh": "贴在系统无障碍页底部的半透明引导条，提示用户在该页操作",
      "user_action_requested": "按悬浮条指引在系统页中勾选 Contacts 服务；无关闭按钮（不可聚焦且铺满宽度）",
      "code_anchor": "com.repexetuzibi.zucu.xadosawasutumula.vifolulasomitayu#onCreate"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "u2.h.c 的 Handler 定时链（u2.b.a() → HandlerThread \"mainHandlerThread\"）+ u2.h.a() 的 PendingIntent 自重启",
      "trigger_event": "Handler.postDelayed(runnable, 2000) 与 postDelayed(self, 3000)；以及 u2.d.run → u2.h.a(activity) 的 PendingIntent.getActivity(...).send()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户返回或拒绝后，每 2 秒重新跳一次无障碍设置页、每 3 秒重跑一轮，并通过 CLEAR_TASK 自重启把用户拉回引导流程",
      "user_action_requested": "被迫开启无障碍；无退出路径（onBackPressed 仅 super，onDestroy 亦不移除定时器）",
      "code_anchor": "u2.h#c / u2.h#a / u2.d#run"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.repexetuzibi.zucu.cisehe.nalamoti 连接成功 → duxazociwudexa.u()/v()/r()/s()",
      "trigger_event": "nazemidu$d.b(this) 返回 true（enabled_accessibility_services 已含本服务）→ duxazociwudexa.onCreate 走 u(); v();",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "先禁用全部 11 个图标别名，再按已安装的目标应用启用对应别名并启动真实应用，实现桌面图标与真实应用一致；同时无障碍服务获得自动点击、按键过滤、读屏能力",
      "user_action_requested": "无（自动完成，用户无法感知权限已被用于后续自动化操作）",
      "code_anchor": "com.sonirupiwebidoti.geyosego.duxazociwudexa#r / #s / #v / com.repexetuzibi.zucu.cisehe.nalamoti"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表中该条目的服务名：Manifest <service android:label=\"Contacts\">（com.repexetuzibi.zucu.cisehe.nalamoti）",
    "系统无障碍服务列表中该条目的说明文字：res/values/strings.xml 的 text_accessibility_service_description = \"If accessibility permission has been on, please turn off then turn on.\"（由 res/xml/silazufunewakahi.xml 的 android:description 引用）",
    "type=2006 系统悬浮窗 Activity nazemidu 内全屏 WebView：Base64/远端 HTML 引导页（JS 桥 Android，按设备语言替换 <html lang>），静态不可读",
    "跳转系统无障碍设置页后叠加的 vifolulasomitayu 底部 WebView 悬浮条（type=2、gravity=BOTTOM、NOT_FOCUSABLE）：Base64/远端 HTML，静态不可读",
    "桌面图标与名称：application android:label=\"Googlecom\" 及 10 个 activity-alias 的 label/icon（Facebook、Google Play、Gmail、Contacts、WhatsApp、Youtube、Chrome、Instagram、TikTok、Telegram），默认关闭、运行期按已装应用动态启用",
    "主界面无任何文字（setContentView(new TextView(\" \"))），设备管理广播接收器 label 为单个空格、description 为 \"Add application to admin\""
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开启，请先关闭再重新开启。",
      "source_location": "res/values/strings.xml → key text_accessibility_service_description（经 res/xml/silazufunewakahi.xml 的 android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Contacts",
      "text_zh": "通讯录",
      "source_location": "AndroidManifest.xml → <service android:name=\"com.repexetuzibi.zucu.cisehe.nalamoti\" android:label=\"Contacts\">；同名 activity-alias label=\"Contacts\"",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Googlecom",
      "text_zh": "谷歌公司（拼写残缺的伪造品牌名）",
      "source_location": "AndroidManifest.xml → <application android:label=\"Googlecom\">",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Add application to admin",
      "text_zh": "将应用添加为设备管理员",
      "source_location": "res/values/strings.xml → key adm（设备管理广播接收器 com.repexetuzibi.zucu.xuriremogo.ruce 的 android:description）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "不可静态还原：Base64.decode(y.a()) / Base64.decode(nazemidu.z.a()) 注入的 HTML 引导页正文",
      "text_zh": "运行时下发的多语言引导文案，静态不可读",
      "source_location": "com.repexetuzibi.zucu.nazemidu.r 与 com.repexetuzibi.zucu.xadosawasutumula.vifolulasomitayu.onCreate（模板片段位于 u2.i）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "u2.h.c 在独立 HandlerThread 上 postDelayed(2000ms) 执行跳转、postDelayed(3000ms) 重跑自身，形成 2 秒跳一次、3 秒一轮的持续重跳；u2.d.run 另经 u2.h.a 用 PendingIntent.send() 以 0x24000000（NEW_TASK|CLEAR_TASK）自重启把用户拉回引导页；nazemidu.onDestroy 与 onBackPressed 均未撤销定时器与悬浮窗。",
    "overlay_or_fake_settings": "双层叠放：① 引导阶段用 getWindow().setType(2006) 把 nazemidu 变成系统级悬浮窗（全屏 WebView）；② 跳系统无障碍设置页后立即 addView 一个 type=2、NOT_FOCUSABLE、gravity=BOTTOM 的 WebView 半透明引导条压在系统页上方。非高仿系统开关页，而是覆盖真实系统页。",
    "restricted_settings_13plus_coaching": "无（应用 targetSdkVersion=28，未使用应用详情页受限设置教学，也未用 Session 安装器绕过；引导文本为远端 HTML，静态不可确认是否含该教学）",
    "post_grant_anti_removal": "获权后由无障碍服务自身能力（canPerformGestures、canRequestFilterKeyEvents、canRetrieveWindowContent、typeAllMask）配合，可自动点击系统授权按钮并在设置页执行全局动作；获权瞬间 duxazociwudexa 先禁用全部 11 个图标别名再按已装目标应用启用对应别名并启动真实应用，完成图标换脸。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")) 或 PendingIntent.send 重启本应用 Activity 的瞬间立即抓取；也可在 launcher duxazociwudexa 启动后 1-3 秒（首个 2000ms 定时器到期前）开始连续截屏，此时 nazemidu 悬浮窗正在铺满屏幕。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的 type=2006 全屏悬浮窗引导页",
        "page_identifier": "包名 com.sonirupiwebidoti.geyosego 的 WebView 内容 + 无标题栏无导航的全屏 HTML 页面，窗口非 Activity 常规任务栈表现",
        "why_most_useful": "这是唯一的『说明/诱导』文案载体，其文案完全由远端 Base64 决定，静态无法获得，只有 UTG 才能取到真实话术",
        "observable_utg_signals": ["HTML 页面标题与正文文本", "是否存在『开启无障碍』『Turn on』『Accessibility』关键词", "页面是否含伪造的系统设置样式控件", "窗口是否覆盖在其他应用/桌面上方（悬浮窗特征）"]
      },
      {
        "page_role": "跳转后压在系统无障碍设置页上的底部引导条",
        "page_identifier": "系统『设置 → 无障碍 → 已下载的服务』页面上方叠加的底部半透明条（非系统控件，无返回键归属）",
        "why_most_useful": "直接证明『遮罩叠层指引』——用户以为自己还在系统设置里操作，实际被第三方浮层引导；同时可确认目标服务条目显示为 Contacts",
        "observable_utg_signals": ["系统无障碍列表中出现 label 为 Contacts 的服务项", "该服务项 description 为『If accessibility permission has been on, please turn off then turn on.』", "底部浮层文本与系统 UI 的层级差异（浮层无系统无障碍节点归属）"]
      },
      {
        "page_role": "拒权返回后的循环重跳现场",
        "page_identifier": "连续多次出现同一系统无障碍设置页 + 应用自身被重新拉起（Activity 任务被清空重建）",
        "why_most_useful": "区分『一次性引导』与『强制循环』，是判定非自愿授权的决定性观测",
        "observable_utg_signals": ["按返回键后 2 秒内无障碍设置页再次出现", "同一页面在 10 秒内重复出现 ≥3 次", "应用任务栈被 CLEAR_TASK 重建（桌面图标再次闪出）"]
      },
      {
        "page_role": "获权后的图标换脸",
        "page_identifier": "桌面/最近任务中应用图标变为目标社交应用（Telegram/Facebook/WhatsApp 等），或启动后直接跳进该真实应用",
        "why_most_useful": "证明权限授予后立即发生的身份伪装与后续动作，闭环『诱导→获权→变脸』因果",
        "observable_utg_signals": ["桌面图标与 label 在获权前后变化", "启动后 1 秒内跳转到第三方应用界面", "无障碍服务在运行服务列表中保持 enabled"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区在引导文案本身：nazemidu 与 vifolulasomitayu 的 HTML 均来自 Base64.decode(y.a()) / z.a()（偏好或远端下发），静态无法获得逐字文本，必须依赖 UTG/截图获取；此外主界面为单空格 TextView、无障碍服务 label 仅『Contacts』，若 UTG 仅在应用常规 Activity 层面采样而忽略 type=2006 悬浮窗，会完全漏掉诱导页。静态无加壳，运行期逻辑完整可见。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.sonirupiwebidoti.geyosego.duxazociwudexa.onCreate",
    "com.repexetuzibi.zucu.nazemidu.r",
    "u2.h.c / u2.h.b / u2.h.a",
    "com.repexetuzibi.zucu.xadosawasutumula.vifolulasomitayu.onCreate",
    "com.sonirupiwebidoti.geyosego.duxazociwudexa.r",
    "res/xml/silazufunewakahi.xml + res/values/strings.xml#text_accessibility_service_description"
  ]
}
```

> 说明：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD` 仅指引导 HTML 以 Base64 承载、非明文资源（非加壳），静态可见性已按 `partial_dynamic_or_remote` 标注。既有 [R-001] 结论未被推翻，本轮仅补充压栈遮罩、双定时器与 `PendingIntent` 重入细节，未新增独立风险命题。

</details>
