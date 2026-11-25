# MB_009__a6ed100ae4｜GodFather — Music Downloader

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：179.5s

## 1. 一句话核心结论

- **核心申请方式**：以 'Music Downloader' 为名、无障碍服务同名伪装，冷启动即请求通知权限并拉取密文远端指令，先用 Chrome 打开 google.com 掩护、2 秒后拉起系统设置，配合无跳过按钮的两步图文截图教学页诱导开启无障碍，服务连接瞬间 performGlobalAction(1) 弹回阻止撤权。
- **静态可见性说明**：无障碍服务声明、引导布局 activity_fragment.xml、截图资源 access/accessok、服务标签与全部逻辑控制流均静态可见；但跳转系统的 Intent action（含无障碍设置页）、目标包名与引导文案正文全部来自 AES/CBC 密文（密钥硬编码 B9M80O2RAK1VRJNV，经 Hagai.hardim 解密）且由远端 JSON 指令下发，包内无 ACCESSIBILITY_SETTINGS 明文；rensselaerite 布局在解包资源中缺失，引导页实际呈现需运行期 UTG 观测。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a6ed100ae42e4fdabfd1b4c992762152bc4a11cc8e521b647b444c75bb7a9782` |
| 包名 / 年份 | `com.motivities.grubroot` / 2026 |
| 家族 / 品类 | **GodFather**（同池样本数：11） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Music Downloader |
| 引导页宣称品牌/身份 | 音乐下载器（Music Downloader），并复用 Google Play services 提示文案与 'Settings' 资源名伪造系统组件身份 |
| 系统无障碍列表服务名 | Music Downloader（@string/app_name） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) application android:label 置为空串，仅靠 @string/app_name 显示名；2) 无障碍服务 label 直接复用 app_name，与桌面名一致，无 android:description 说明用途；3) 另设 @string/appname = 'Settings' 用于伪造系统设置名；4) activity_splash 使用土耳其语 'Düşük Pil'（低电量）+ banner 图标伪装系统低电提醒；5) 主 Activity 同时挂 MAIN/INFO 与 BROWSABLE(host=www.google.com) 双 intent-filter；6) 全部关键字符串 AES/CBC 加密 + 语义化英文伪类名/方法名（tatouays、subprovinces、epistemophilia）混淆；7) 未声明 isAccessibilityTool。 |
| 无障碍服务类名 | `com.motivities.grubroot.tatouays` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.motivities.grubroot.truthfully（MAIN/INFO + BROWSABLE www.google.com），setContentView(R$layout.rensselaerite) | onCreate → onResume | 原生Activity | **原文**：无（rensselaerite 布局在解包资源中缺失，activity_main.xml 为空 LinearLayout）<br>**译注**：冷启动主界面为空白容器，实际内容运行期填充 | 无需操作，自动进入下一步 | `com.motivities.grubroot.truthfully#onCreate / #onResume` |
| 2 | 冷启动入口 | truthfully.Latin() 环境检测 | onResume 首行调用 Latin() | 不可静态还原 | 无 | 无（模拟器/沙箱环境下静默退出） | `com.motivities.grubroot.truthfully#Latin` |
| 3 | 业务功能触发 | truthfully.onResume → spermatoplasmic() 与后台线程 truthfully$1 | onResume 中 SDK_INT>32 分支 / Thread.start() | 原生Activity | **原文**：无（仅系统权限弹窗：android.permission.POST_NOTIFICATIONS）<br>**译注**：先索取通知权限，同时后台线程向远端拉取指令与配置；随后 epistemophilia() 批量写入大量本地配置键（密文键名/值） | 系统通知权限弹窗：允许/拒绝 | `com.motivities.grubroot.truthfully#onResume / #spermatoplasmic / #epistemophilia` |
| 4 | 跳受限设置 | subprovinces.outblazes() → Chrome（com.android.chrome）打开 https://google.com/ | 远端指令经 subprovinces.Cucumis 分发，命中对应 key 后调用 outblazes() | 原生Activity（外部浏览器） | **原文**：Intent(android.intent.action.VIEW, Uri.parse("https://google.com/")) setPackage("com.android.chrome")；失败则 setPackage(null) 走系统默认浏览器<br>**译注**：先跳转到 Chrome 并打开 Google 首页作为掩护页，掩盖后续跳转意图 | 无需操作，用户看到的是正常网页 | `com.motivities.grubroot.subprovinces#outblazes` |
| 5 | 跳无障碍设置 | new Handler(Looper.getMainLooper()).postDelayed(new subprovinces$1(s), 2000L) → startActivity；或 tatouays.open1()/open2() 的密文 Intent | 掩护页打开后 2 秒定时器触发；或远端指令直接下发 open1/open2 | 系统无障碍页 | **原文**：Intent(Hagai.hardim("4Uy7TBu9sZfySaO5zJiHaCgID0YgNse81sJbLZ6M/x/aO9YwtAbcDgs6wAJuKw2")) / Intent(Hagai.hardim("7jfoAzLUPmwIqFccO+jolTHlwxKYiITXtNXOkabz4lohW9BsyORUpJRuDiwo/ekq"))，均 addFlags(FLAG_ACTIVITY_NEW_TASK)<br>**译注**：action 与目标包名经 AES 解密后跳转，本地字符串表中存在 android.settings.SETTINGS、com.android.settings、:settings:show_fragment_args、android:id/summary 等密文片段，指向系统设置/无障碍服务列表页；包内无 ACCESSIBILITY_SETTINGS 明文 | 在系统设置中找到并点击 'Music Downloader' 服务项 | `com.motivities.grubroot.subprovinces#outblazes / com.motivities.grubroot.tatouays#open1 / #open2` |
| 6 | 遮罩叠层指引 | res/layout/activity_fragment.xml（两步图文教学页） | 跳转设置页同时/之前展示引导页；文案 text1~text4 运行期填充 | 原生Dialog | **原文**：TextView android:text="1. " / TextView android:text="2. "；ImageView android:src="@drawable/access" / "@drawable/accessok"；Button android:id="@id/button_open" android:text="@android:string/ok"；标题 text1 运行期填充（空）<br>**译注**：分步图文教学：第 1 步截图 access 指向系统无障碍设置入口，第 2 步截图 accessok 指向开启后的服务开关状态，底部仅一个 '确定' 按钮 | 点击 '确定'（OK）继续，无取消/跳过按钮 | `res/layout/activity_fragment.xml#L3-L20 / com.motivities.grubroot.truthfully#onCreate(setContentView)` |
| 7 | 获权后动作 | com.motivities.grubroot.tatouays.onServiceConnected() | 用户开启无障碍开关后系统回调 onServiceConnected | 系统无障碍页 | **原文**：super.onServiceConnected(); performGlobalAction(1);<br>**译注**：服务连接瞬间立即执行 GLOBAL_ACTION_BACK（返回键），把用户从刚打开的系统无障碍设置页弹回上一层，压缩撤销授权的时间窗口 | 无（被动被返回） | `com.motivities.grubroot.tatouays#onServiceConnected` |
| 8 | 获权后动作 | tatouays.onAccessibilityEvent（3756 条指令）/ scroll、swipe、slide、d、j、w、y 等手势与节点操作，及 subprovinces.Cucumis 指令分发 | 无障碍事件回调 + 远端指令（again/accs/min/protect/restart/clickk 等密文键） | 悬浮窗Overlay | **原文**：类字段含 Turkophilia / Unanglican / topkick / laurellocked 等 View、FrameLayout 与 WindowManager camerier/eveck/voluptuaries<br>**译注**：获权后通过 WindowManager 叠放悬浮窗/遮罩层，并按远端指令执行读取窗口内容、模拟点击滑动、拉起指定应用（getLaunchIntentForPackage）等操作 | 无 | `com.motivities.grubroot.tatouays#onAccessibilityEvent / #onCreate / com.motivities.grubroot.subprovinces#Cucumis` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/layout/activity_fragment.xml：两步编号图文教学布局（'1.'/'2.' + @drawable/access、@drawable/accessok 操作截图 + @android:string/ok 按钮），文案由代码运行期填入 text1/text2/text3/text4
- res/layout/activity_splash.xml：假系统低电提醒页（@drawable/banner 图标 + @string/battery = 'Düşük Pil' 土耳其语低电量）
- res/values/strings.xml：@string/app_name = 'Music Downloader'（桌面名与无障碍服务标签共用）、@string/appname = 'Settings'（伪造系统设置名）
- res/xml/preferences.xml：无障碍服务配置，未设置 android:description，系统无障碍列表中该服务无任何用途说明
- com.google.android.gms.common 资源库的 Google Play services 提示文案（'%1$s won't work unless you enable Google Play services.'、'Enable Google Play services' 等）作为假更新/假依赖恐吓外壳
- 跳转 Chrome 打开 https://google.com/ 的掩护网页（非引导文案，仅作掩盖）
- 跳转系统设置/无障碍列表的 Intent action 与目标包名：全部 AES 密文，包内无明文，实际界面由系统渲染

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Music Downloader | 音乐下载器 | `res/values/strings.xml @string/app_name（同时作为 android:label 与无障碍服务 label）` | 清理工具伪装 |
| en | Settings | 设置 | `res/values/strings.xml @string/appname` | 未知 |
| tr | Düşük Pil | 低电量 | `res/values/strings.xml @string/battery（activity_splash.xml 引用）` | 故障恐吓 |
| tr | İzin Ver | 允许 | `res/values/strings.xml @string/allow` | 未知 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 无法运行，除非你启用 Google Play 服务。 | `res/values/strings.xml common_google_play_services_enable_text（GMS 资源）` | 假更新 |
| en | Enable Google Play services | 启用 Google Play 服务 | `res/values/strings.xml common_google_play_services_enable_title` | 假更新 |
| en | A new version of our application is available. To update, go to Play Store. | 我们的应用有新版本可用。要更新，请前往 Play 商店。 | `classes.dex 密文常量（Hagai.hardim 解密，多语言 [en]/[ru]/[ja]/[es] 等内嵌）` | 假更新 |
| en | 1. | 第 1 步 | `res/layout/activity_fragment.xml TableRow TextView` | 受限设置分步教学 |
| en | 2. | 第 2 步 | `res/layout/activity_fragment.xml TableRow TextView` | 受限设置分步教学 |
| en | OK | 确定 | `res/layout/activity_fragment.xml @id/button_open → @android:string/ok` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：包内未见 onResume 死循环重跳的明文实现；但指令由远端 JSON 驱动（subprovinces.Cucumis 按 key 分发到 open1/open2/outblazes），服务端可重复下发跳转指令；且 tatouays.onServiceConnected 一旦连接立即 performGlobalAction(1) 弹回，用户从设置页返回应用后服务已生效、无法停留在设置页撤权。另有 kill 广播接收器 unoccupiedness 与 restart/protect 类密文指令用于保活。
- **遮罩叠层 / 高仿系统设置页**：是。activity_fragment.xml 为高仿操作指引页（两步编号 + access/accessok 两张真实系统截图 + 单一 OK 按钮）；tatouays 类中持有多个 WindowManager 实例（camerier/eveck/voluptuaries）、FrameLayout topkick/Unanglican 与 View laurellocked/multivincular，具备在设置页之上叠放半透明遮罩/悬浮引导层的能力；activity_splash 另伪造系统低电提醒。
- **Android 13+ 受限设置（Restricted Settings）应对**：无明确证据。密文指令表中存在 com.android.packageinstaller.permission.ui.grantpermissionsactivity、:settings:show_fragment_args、:settings:fragment_args_key、android:id/summary、com.android.settings:id/button1/button2/5555 等节点与控件标识，具备按包名/控件名自动点击安装器与设置页按钮的能力，但未见针对 Android 13 受限设置的'点右上角菜单允许'专门文案。
- **获权后即时行为与防撤权机制**：是。onServiceConnected 在 super 调用后立刻 performGlobalAction(1)（GLOBAL_ACTION_BACK），把用户从无障碍设置页弹回，阻碍即时撤权；同时 open1/open2/on 具备拉起应用与设置页的能力，配合悬浮窗可在用户再次进入设置页时覆盖引导。
- **良性降级 / 替代方案**：无。不存在手动模式、仅观看模式或 ADB 替代路径；模拟器/沙箱环境下直接 finish() 退出而非降级。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以冷启动 truthfully.onResume 完成后为起点连续 UTG 抓帧（约 0~10 秒窗口）；重点钩住 (a) Chrome 被拉起打开 google.com 后的 2 秒定时器到期瞬间（subprovinces$1 触发 startActivity），(b) 任何 Activity 切换为 com.android.settings / packageinstaller 的跳转事件，(c) AccessibilityService 连接回调（可用 Hook 监听 tatouays.onServiceConnected 触发时刻）以抓取紧随其后的 GLOBAL_ACTION_BACK 弹回画面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：1) 无障碍设置页的 Intent action 与全部引导正文均为 AES 密文 + 远端 JSON 下发，包内无明文，静态无法枚举具体页面与文案；2) rensselaerite 布局在解包资源中缺失（activity_main.xml 为空），冷启动首屏实际内容需运行期观测。另样本含完整模拟器/指纹检测（Latin()）与 kill 广播、restart/protect 保活指令，在模拟器环境下会 finish() 静默退出，UTG 采集须使用真机或做好指纹伪装，否则捕获不到任何引导页面。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（两步图文教学）** | 含编号 '1.'/'2.' 两行、内嵌 access/accessok 系统设置截图、底部仅一个 '确定' 按钮的 Dialog/Activity；控件 id 含 button_open、text1~text4 | 这是唯一静态可见的引导载体，且明确无取消按钮；捕获后可直接固定'分步教学 + 无跳过'的诱导证据，区分良性说明与恶意诱导 | 页面仅 1 个可点击按钮（OK），无取消/关闭/跳过控件；两张截图均为系统无障碍设置页 UI；文案含 'accessibility'/'settings'/'services' 等词 |
| **掩护网页（Chrome + google.com）** | com.android.chrome 前台、地址栏显示 https://google.com/ | 证明跳转链条刻意插入中性网页作掩护，是'先掩护后跳设置'的关键时序证据 | 前台包名为 com.android.chrome；打开后 2 秒内发生第二次 Activity 切换 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中名为 'Music Downloader' 的服务条目，且无用途说明文本 | 确认服务标签伪装与 android:description 缺失，直接对应系统列表中的身份欺骗呈现 | 条目文本仅为 'Music Downloader'，无描述副标题；同页出现 access/accessok 截图对应位置 |
| **获权瞬间的弹回/遮罩页** | 无障碍开关开启后立即退回到上一层（浏览器或应用页），或出现覆盖在设置页上的半透明悬浮引导层 | performGlobalAction(1) 是最强的反撤权证据，UTG 可捕获'开关开启 → 页面立即弹回'的时序 | 开关 toggle 后 <1 秒内 Activity 栈变化；设置页被透明浮层覆盖、点击穿透异常 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.motivities.grubroot.truthfully#onResume`
- `com.motivities.grubroot.truthfully#Latin`
- `com.motivities.grubroot.subprovinces#outblazes`
- `com.motivities.grubroot.subprovinces#Cucumis`
- `com.motivities.grubroot.tatouays#onServiceConnected`
- `res/layout/activity_fragment.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**整体判断**：该样本是 GodFather 家族衍生木马，采用“远端/密文指令驱动 + 本地图文步骤页”的方式诱导用户开启无障碍服务；静态包内**不存在** `ACTION_ACCESSIBILITY_SETTINGS` 明文，跳转目标与文案由 AES 密文解密后执行，属**部分静态可见**。

**关键证据链**
1. **服务伪装**：[preferences.xml](<resource-unit:#1 file:res/xml/preferences.xml#L2-L3>) 声明 `typeAllMask`、`canRetrieveWindowContent`、`canPerformGestures`、`canRequestEnhancedWebAccessibility`，**无 android:description**；服务 label 取 `@string/app_name`，值为 `Music Downloader`。Manifest 中 `<application android:label="">` 为空串，与 `@string/appname`（值为 `Settings`）并存，属标签混淆。
2. **引导载体**：[activity_fragment.xml](<resource-unit:#1 file:res/layout/activity_fragment.xml#L3-L20>) 为 “1.” / “2.” 编号两步图文教学布局，内嵌 `@drawable/access`、`@drawable/accessok` 两张操作截图，底部 `button_open`（`@android:string/ok`）；文案由运行期填充，**无取消/跳过按钮**。
3. **触发时机**：[truthfully#onResume](<resource-unit:#1.dex1 code:com.motivities.grubroot.truthfully#onResume>) 冷启动即执行：先经 [Latin()](<resource-unit:#1.dex1 code:com.motivities.grubroot.truthfully#Latin>) 比对 BRAND/DEVICE/FINGERPRINT/HARDWARE/MODEL/MANUFACTURER/PRODUCT 模拟器特征（`google_sdk`、`Emulator`、`goldfish` 等密文常量），命中即 `finish()`；随后 `SDK_INT>32` 请求 `POST_NOTIFICATIONS`，并起线程拉取远端指令。
4. **跳转实现**：[subprovinces#Cucumis](<resource-unit:#1.dex1 code:com.motivities.grubroot.subprovinces#Cucumis>) 解析 JSON 指令分发给无障碍服务实例；`outblazes()` 先以 `VIEW + https://google.com + setPackage("com.android.chrome")` 打开浏览器作掩护，**`postDelayed(..., 2000L)` 后**再 `startActivity` 拉起系统设置；`open1()/open2()` 的 action 字符串均经 [Hagai#hardim](<resource-unit:#1.dex1 code:com.motivities.grubroot.Hagai#hardim>)（AES/CBC/PKCS5，密钥硬编码 `B9M80O2RAK1VRJNV`）解密。
5. **获权后反撤权**：[tatouays#onServiceConnected](<resource-unit:#1.dex1 code:com.motivities.grubroot.tatouays#onServiceConnected>) 全部业务代码只有 `super.onServiceConnected(); performGlobalAction(1);`——服务一连接即执行 GLOBAL_ACTION_BACK，把用户从刚打开的系统设置页弹回，压缩撤权窗口。
6. **低电伪装页**：`activity_splash.xml` 使用 `@string/battery`（土耳其语 “Düşük Pil”＝低电量）与 banner 图标，构成假系统低电提醒外壳。

**覆盖边界**：无障碍设置页 action、引导文案正文、远端 HTML/JSON 均在密文或服务端，包内无明文；`rensselaerite` 布局在解包资源中未找到（`activity_main.xml` 为空 LinearLayout），该页实际 UI 需运行期观测。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍服务声明、引导布局 activity_fragment.xml、截图资源 access/accessok、服务标签与全部逻辑控制流均静态可见；但跳转系统的 Intent action（含无障碍设置页）、目标包名与引导文案正文全部来自 AES/CBC 密文（密钥硬编码 B9M80O2RAK1VRJNV，经 Hagai.hardim 解密）且由远端 JSON 指令下发，包内无 ACCESSIBILITY_SETTINGS 明文；rensselaerite 布局在解包资源中缺失，引导页实际呈现需运行期 UTG 观测。",
  "summary_one_liner": "以 'Music Downloader' 为名、无障碍服务同名伪装，冷启动即请求通知权限并拉取密文远端指令，先用 Chrome 打开 google.com 掩护、2 秒后拉起系统设置，配合无跳过按钮的两步图文截图教学页诱导开启无障碍，服务连接瞬间 performGlobalAction(1) 弹回阻止撤权。",
  "disguise_identity": {
    "app_display_name": "Music Downloader",
    "claimed_brand_or_persona": "音乐下载器（Music Downloader），并复用 Google Play services 提示文案与 'Settings' 资源名伪造系统组件身份",
    "a11y_service_label": "Music Downloader（@string/app_name）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) application android:label 置为空串，仅靠 @string/app_name 显示名；2) 无障碍服务 label 直接复用 app_name，与桌面名一致，无 android:description 说明用途；3) 另设 @string/appname = 'Settings' 用于伪造系统设置名；4) activity_splash 使用土耳其语 'Düşük Pil'（低电量）+ banner 图标伪装系统低电提醒；5) 主 Activity 同时挂 MAIN/INFO 与 BROWSABLE(host=www.google.com) 双 intent-filter；6) 全部关键字符串 AES/CBC 加密 + 语义化英文伪类名/方法名（tatouays、subprovinces、epistemophilia）混淆；7) 未声明 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.motivities.grubroot.truthfully（MAIN/INFO + BROWSABLE www.google.com），setContentView(R$layout.rensselaerite)",
      "trigger_event": "onCreate → onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（rensselaerite 布局在解包资源中缺失，activity_main.xml 为空 LinearLayout）",
      "shown_text_zh": "冷启动主界面为空白容器，实际内容运行期填充",
      "user_action_requested": "无需操作，自动进入下一步",
      "code_anchor": "com.motivities.grubroot.truthfully#onCreate / #onResume"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "truthfully.Latin() 环境检测",
      "trigger_event": "onResume 首行调用 Latin()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "检测 BRAND/DEVICE/FINGERPRINT/HARDWARE/MODEL/MANUFACTURER/PRODUCT 中的模拟器特征（google_sdk、sdk_google、Emulator、goldfish、Genymotion 等密文常量），命中则直接 finish() 退出，不展示任何引导",
      "user_action_requested": "无（模拟器/沙箱环境下静默退出）",
      "code_anchor": "com.motivities.grubroot.truthfully#Latin"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "truthfully.onResume → spermatoplasmic() 与后台线程 truthfully$1",
      "trigger_event": "onResume 中 SDK_INT>32 分支 / Thread.start()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅系统权限弹窗：android.permission.POST_NOTIFICATIONS）",
      "shown_text_zh": "先索取通知权限，同时后台线程向远端拉取指令与配置；随后 epistemophilia() 批量写入大量本地配置键（密文键名/值）",
      "user_action_requested": "系统通知权限弹窗：允许/拒绝",
      "code_anchor": "com.motivities.grubroot.truthfully#onResume / #spermatoplasmic / #epistemophilia"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "subprovinces.outblazes() → Chrome（com.android.chrome）打开 https://google.com/",
      "trigger_event": "远端指令经 subprovinces.Cucumis 分发，命中对应 key 后调用 outblazes()",
      "ui_carrier": "原生Activity（外部浏览器）",
      "shown_text_verbatim": "Intent(android.intent.action.VIEW, Uri.parse(\"https://google.com/\")) setPackage(\"com.android.chrome\")；失败则 setPackage(null) 走系统默认浏览器",
      "shown_text_zh": "先跳转到 Chrome 并打开 Google 首页作为掩护页，掩盖后续跳转意图",
      "user_action_requested": "无需操作，用户看到的是正常网页",
      "code_anchor": "com.motivities.grubroot.subprovinces#outblazes"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "new Handler(Looper.getMainLooper()).postDelayed(new subprovinces$1(s), 2000L) → startActivity；或 tatouays.open1()/open2() 的密文 Intent",
      "trigger_event": "掩护页打开后 2 秒定时器触发；或远端指令直接下发 open1/open2",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Intent(Hagai.hardim(\"4Uy7TBu9sZfySaO5zJiHaCgID0YgNse81sJbLZ6M/x/aO9YwtAbcDgs6wAJuKw2\")) / Intent(Hagai.hardim(\"7jfoAzLUPmwIqFccO+jolTHlwxKYiITXtNXOkabz4lohW9BsyORUpJRuDiwo/ekq\"))，均 addFlags(FLAG_ACTIVITY_NEW_TASK)",
      "shown_text_zh": "action 与目标包名经 AES 解密后跳转，本地字符串表中存在 android.settings.SETTINGS、com.android.settings、:settings:show_fragment_args、android:id/summary 等密文片段，指向系统设置/无障碍服务列表页；包内无 ACCESSIBILITY_SETTINGS 明文",
      "user_action_requested": "在系统设置中找到并点击 'Music Downloader' 服务项",
      "code_anchor": "com.motivities.grubroot.subprovinces#outblazes / com.motivities.grubroot.tatouays#open1 / #open2"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "res/layout/activity_fragment.xml（两步图文教学页）",
      "trigger_event": "跳转设置页同时/之前展示引导页；文案 text1~text4 运行期填充",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "TextView android:text=\"1. \" / TextView android:text=\"2. \"；ImageView android:src=\"@drawable/access\" / \"@drawable/accessok\"；Button android:id=\"@id/button_open\" android:text=\"@android:string/ok\"；标题 text1 运行期填充（空）",
      "shown_text_zh": "分步图文教学：第 1 步截图 access 指向系统无障碍设置入口，第 2 步截图 accessok 指向开启后的服务开关状态，底部仅一个 '确定' 按钮",
      "user_action_requested": "点击 '确定'（OK）继续，无取消/跳过按钮",
      "code_anchor": "res/layout/activity_fragment.xml#L3-L20 / com.motivities.grubroot.truthfully#onCreate(setContentView)"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.motivities.grubroot.tatouays.onServiceConnected()",
      "trigger_event": "用户开启无障碍开关后系统回调 onServiceConnected",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "super.onServiceConnected(); performGlobalAction(1);",
      "shown_text_zh": "服务连接瞬间立即执行 GLOBAL_ACTION_BACK（返回键），把用户从刚打开的系统无障碍设置页弹回上一层，压缩撤销授权的时间窗口",
      "user_action_requested": "无（被动被返回）",
      "code_anchor": "com.motivities.grubroot.tatouays#onServiceConnected"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "tatouays.onAccessibilityEvent（3756 条指令）/ scroll、swipe、slide、d、j、w、y 等手势与节点操作，及 subprovinces.Cucumis 指令分发",
      "trigger_event": "无障碍事件回调 + 远端指令（again/accs/min/protect/restart/clickk 等密文键）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "类字段含 Turkophilia / Unanglican / topkick / laurellocked 等 View、FrameLayout 与 WindowManager camerier/eveck/voluptuaries",
      "shown_text_zh": "获权后通过 WindowManager 叠放悬浮窗/遮罩层，并按远端指令执行读取窗口内容、模拟点击滑动、拉起指定应用（getLaunchIntentForPackage）等操作",
      "user_action_requested": "无",
      "code_anchor": "com.motivities.grubroot.tatouays#onAccessibilityEvent / #onCreate / com.motivities.grubroot.subprovinces#Cucumis"
    }
  ],
  "text_presentation_locations": [
    "res/layout/activity_fragment.xml：两步编号图文教学布局（'1.'/'2.' + @drawable/access、@drawable/accessok 操作截图 + @android:string/ok 按钮），文案由代码运行期填入 text1/text2/text3/text4",
    "res/layout/activity_splash.xml：假系统低电提醒页（@drawable/banner 图标 + @string/battery = 'Düşük Pil' 土耳其语低电量）",
    "res/values/strings.xml：@string/app_name = 'Music Downloader'（桌面名与无障碍服务标签共用）、@string/appname = 'Settings'（伪造系统设置名）",
    "res/xml/preferences.xml：无障碍服务配置，未设置 android:description，系统无障碍列表中该服务无任何用途说明",
    "com.google.android.gms.common 资源库的 Google Play services 提示文案（'%1$s won't work unless you enable Google Play services.'、'Enable Google Play services' 等）作为假更新/假依赖恐吓外壳",
    "跳转 Chrome 打开 https://google.com/ 的掩护网页（非引导文案，仅作掩盖）",
    "跳转系统设置/无障碍列表的 Intent action 与目标包名：全部 AES 密文，包内无明文，实际界面由系统渲染"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Music Downloader",
      "text_zh": "音乐下载器",
      "source_location": "res/values/strings.xml @string/app_name（同时作为 android:label 与无障碍服务 label）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Settings",
      "text_zh": "设置",
      "source_location": "res/values/strings.xml @string/appname",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "Düşük Pil",
      "text_zh": "低电量",
      "source_location": "res/values/strings.xml @string/battery（activity_splash.xml 引用）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "tr",
      "text_verbatim": "İzin Ver",
      "text_zh": "允许",
      "source_location": "res/values/strings.xml @string/allow",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 无法运行，除非你启用 Google Play 服务。",
      "source_location": "res/values/strings.xml common_google_play_services_enable_text（GMS 资源）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Google Play services",
      "text_zh": "启用 Google Play 服务",
      "source_location": "res/values/strings.xml common_google_play_services_enable_title",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "A new version of our application is available. To update, go to Play Store.",
      "text_zh": "我们的应用有新版本可用。要更新，请前往 Play 商店。",
      "source_location": "classes.dex 密文常量（Hagai.hardim 解密，多语言 [en]/[ru]/[ja]/[es] 等内嵌）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "1. ",
      "text_zh": "第 1 步",
      "source_location": "res/layout/activity_fragment.xml TableRow TextView",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. ",
      "text_zh": "第 2 步",
      "source_location": "res/layout/activity_fragment.xml TableRow TextView",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "OK",
      "text_zh": "确定",
      "source_location": "res/layout/activity_fragment.xml @id/button_open → @android:string/ok",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "包内未见 onResume 死循环重跳的明文实现；但指令由远端 JSON 驱动（subprovinces.Cucumis 按 key 分发到 open1/open2/outblazes），服务端可重复下发跳转指令；且 tatouays.onServiceConnected 一旦连接立即 performGlobalAction(1) 弹回，用户从设置页返回应用后服务已生效、无法停留在设置页撤权。另有 kill 广播接收器 unoccupiedness 与 restart/protect 类密文指令用于保活。",
    "overlay_or_fake_settings": "是。activity_fragment.xml 为高仿操作指引页（两步编号 + access/accessok 两张真实系统截图 + 单一 OK 按钮）；tatouays 类中持有多个 WindowManager 实例（camerier/eveck/voluptuaries）、FrameLayout topkick/Unanglican 与 View laurellocked/multivincular，具备在设置页之上叠放半透明遮罩/悬浮引导层的能力；activity_splash 另伪造系统低电提醒。",
    "restricted_settings_13plus_coaching": "无明确证据。密文指令表中存在 com.android.packageinstaller.permission.ui.grantpermissionsactivity、:settings:show_fragment_args、:settings:fragment_args_key、android:id/summary、com.android.settings:id/button1/button2/5555 等节点与控件标识，具备按包名/控件名自动点击安装器与设置页按钮的能力，但未见针对 Android 13 受限设置的'点右上角菜单允许'专门文案。",
    "post_grant_anti_removal": "是。onServiceConnected 在 super 调用后立刻 performGlobalAction(1)（GLOBAL_ACTION_BACK），把用户从无障碍设置页弹回，阻碍即时撤权；同时 open1/open2/on 具备拉起应用与设置页的能力，配合悬浮窗可在用户再次进入设置页时覆盖引导。",
    "benign_graceful_degradation": "无。不存在手动模式、仅观看模式或 ADB 替代路径；模拟器/沙箱环境下直接 finish() 退出而非降级。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以冷启动 truthfully.onResume 完成后为起点连续 UTG 抓帧（约 0~10 秒窗口）；重点钩住 (a) Chrome 被拉起打开 google.com 后的 2 秒定时器到期瞬间（subprovinces$1 触发 startActivity），(b) 任何 Activity 切换为 com.android.settings / packageinstaller 的跳转事件，(c) AccessibilityService 连接回调（可用 Hook 监听 tatouays.onServiceConnected 触发时刻）以抓取紧随其后的 GLOBAL_ACTION_BACK 弹回画面。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（两步图文教学）",
        "page_identifier": "含编号 '1.'/'2.' 两行、内嵌 access/accessok 系统设置截图、底部仅一个 '确定' 按钮的 Dialog/Activity；控件 id 含 button_open、text1~text4",
        "why_most_useful": "这是唯一静态可见的引导载体，且明确无取消按钮；捕获后可直接固定'分步教学 + 无跳过'的诱导证据，区分良性说明与恶意诱导",
        "observable_utg_signals": ["页面仅 1 个可点击按钮（OK），无取消/关闭/跳过控件", "两张截图均为系统无障碍设置页 UI", "文案含 'accessibility'/'settings'/'services' 等词"]
      },
      {
        "page_role": "掩护网页（Chrome + google.com）",
        "page_identifier": "com.android.chrome 前台、地址栏显示 https://google.com/",
        "why_most_useful": "证明跳转链条刻意插入中性网页作掩护，是'先掩护后跳设置'的关键时序证据",
        "observable_utg_signals": ["前台包名为 com.android.chrome", "打开后 2 秒内发生第二次 Activity 切换"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中名为 'Music Downloader' 的服务条目，且无用途说明文本",
        "why_most_useful": "确认服务标签伪装与 android:description 缺失，直接对应系统列表中的身份欺骗呈现",
        "observable_utg_signals": ["条目文本仅为 'Music Downloader'，无描述副标题", "同页出现 access/accessok 截图对应位置"]
      },
      {
        "page_role": "获权瞬间的弹回/遮罩页",
        "page_identifier": "无障碍开关开启后立即退回到上一层（浏览器或应用页），或出现覆盖在设置页上的半透明悬浮引导层",
        "why_most_useful": "performGlobalAction(1) 是最强的反撤权证据，UTG 可捕获'开关开启 → 页面立即弹回'的时序",
        "observable_utg_signals": ["开关 toggle 后 <1 秒内 Activity 栈变化", "设置页被透明浮层覆盖、点击穿透异常"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：1) 无障碍设置页的 Intent action 与全部引导正文均为 AES 密文 + 远端 JSON 下发，包内无明文，静态无法枚举具体页面与文案；2) rensselaerite 布局在解包资源中缺失（activity_main.xml 为空），冷启动首屏实际内容需运行期观测。另样本含完整模拟器/指纹检测（Latin()）与 kill 广播、restart/protect 保活指令，在模拟器环境下会 finish() 静默退出，UTG 采集须使用真机或做好指纹伪装，否则捕获不到任何引导页面。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.motivities.grubroot.truthfully#onResume",
    "com.motivities.grubroot.truthfully#Latin",
    "com.motivities.grubroot.subprovinces#outblazes",
    "com.motivities.grubroot.subprovinces#Cucumis",
    "com.motivities.grubroot.tatouays#onServiceConnected",
    "res/layout/activity_fragment.xml"
  ]
}
```

</details>
