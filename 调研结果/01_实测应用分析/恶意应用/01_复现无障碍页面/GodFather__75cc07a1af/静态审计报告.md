# MB_094__75cc07a1af｜GodFather — Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：184.0s

## 1. 一句话核心结论

- **核心申请方式**：伪装成土耳其语歌曲应用，冷启动零说明直接跳系统无障碍设置并用 show_fragment_args 预定位自身服务项，无取消按钮、返回即由前台服务秒级重跳，同时以零宽字符服务名与 com.viber.voip 包名冒用掩盖身份。
- **静态可见性说明**：全部关键字符串（设置页 action、组件名、配置键、设备门控）均为硬编码 AES/ECB 密文，密钥由 PBKDF2WithHmacSHA1(pass='o', salt='o', iter=8, 256) 本地派生，已完整静态解密还原；无加壳、无远端 HTML、无二阶段载荷，引导与拒权循环逻辑 100% 静态可见。唯一未解析项为 Toast 拼接的 string 资源 id 0x7f0b00db 的具体文本。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `75cc07a1af57d9d2a9a06840a25d1b9b368b1ddd57d98bac9a5a5f2f4d0d931d` |
| 包名 / 年份 | `com.alphainventor.filemanager` / 2024 |
| 家族 / 品类 | **GodFather**（同池样本数：11） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i |
| 引导页宣称品牌/身份 | 土耳其语“Şarkı Evreni（歌曲宇宙）”音乐应用；备用别名伪装为 Youtube（@string/app_names=Youtube，ic_youtube 图标）；无障碍服务类冒用 Viber 的 com.viber.voip 包名 |
| 系统无障碍列表服务名 | Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i（复用 @string/app_name，字符间插入 U+200E 零宽标记；serviceconfig.xml 未配置 android:description，系统无障碍列表无任何用途说明） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) app_name 与 app_names 在字母间插入 U+200E LEFT-TO-RIGHT MARK，并含 NBSP(U+00A0)，使系统无障碍列表/桌面名无法被关键字匹配与人工辨认；2) 无障碍服务类名为 com.viber.voip.InputService，与宿主包 com.alphainventor.filemanager 不符，冒用第三方通讯软件身份；3) 三个 activity-alias 变体：Android（MAIN/LAUNCHER 实际入口）、Youtube（enabled=false，图标 ic_youtube，运行期由 setComponentEnabledSetting 动态启用）；4) 存在 android:label="" 的透明 Activity piscifaunacytomicrosome（excludeFromRecents）用于无痕页面；5) 服务配置不写 android:description，规避系统列表中的能力披露；6) 全部引导相关 action/键名以 AES 密文常量存放，配合 com.stringmanager.GF 解密。 |
| 无障碍服务类名 | `com.viber.voip.InputService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | activity-alias com.alphainventor.filemanager.Android → com.alphainventor.filemanager.intraspecificallyunanimatedness (AppCompatActivity) | LAUNCHER 点击，onCreate(Bundle) 执行 | 原生Activity | **原文**：无（onCreate 不 setContentView 任何引导布局，直接执行跳转逻辑）<br>**译注**：无任何引导说明界面，用户点击图标后即刻被推往系统设置 | 无提示、无选择，用户只看到系统无障碍设置页弹出 | `com.alphainventor.filemanager.intraspecificallyunanimatedness.onCreate` |
| 2 | 业务功能触发 | Settings.Secure 查询：enabled_accessibility_services | onCreate 内调用 unvariationsoddenminded.t63r63(getApplicationContext()) | 不可静态还原 | **原文**：enabled_accessibility_services<br>**译注**：读取系统无障碍已启用服务列表，判断是否包含 com.alphainventor.filemanager | 无 | `com.alphainventor.filemanager.unvariationsoddenminded.t63r63` |
| 3 | 跳无障碍设置 | 系统无障碍设置页：首选 action com.android.settings.accessibility.miuiaccessibilitysettingsactivity（MIUI）/ com.samsung.accessibility.installed_service（三星），resolveActivity 为空时回退 android.settings.ACCESSIBILITY_SETTINGS；携带 :settings:fragment_args_key = "com.alphainventor.filemanager/com.viber.voip.InputService" 与 :settings:show_fragment_args Bundle | t63r63 返回 false 时立即 startActivity(kfayfa)，FLAG_ACTIVITY_NEW_TASK(0x10000000) | 系统无障碍页 | **原文**：无应用自绘文字；界面为系统无障碍服务列表，且已被预定位到本应用服务项<br>**译注**：系统无障碍列表自动滚动/定位到“Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i”这一项（无 description 说明） | 要求用户在该列表中手动点开本应用服务开关；页面内无应用提供的取消/跳过入口 | `com.alphainventor.filemanager.intraspecificallyunanimatedness.onCreate` |
| 4 | 拒权反馈循环 | com.alphainventor.filemanager.Services.frugalitiespowerdriven（前台服务）$2.run + 居中 Toast | vivacissimoselftimer.onCreate → postDelayed(1000ms) → start(ctx) → postDelayed(1000ms) 启动 startForegroundService(frugalitiespowerdriven)，run() 内再次 t63r63 判否 | 系统无障碍页 + 通知栏 | **原文**：StringAccess + " (" + getString(0x7f0b00db) + 解密片段（Toast 文本由配置值拼接，部分片段未解出）<br>**译注**：以“应用名 (…)”形式弹出短提示后再次把用户丢回系统无障碍设置页 | 无“取消/不再提示”选项，用户按返回键后仍被重新拉起 | `com.alphainventor.filemanager.Services.frugalitiespowerdriven$2.run` |
| 5 | 跳受限设置 | android.settings.ACCESSIBILITY_SETTINGS 重复 startActivity（带 FLAG_ACTIVITY_NEW_TASK）；同时配合 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS / SYSTEM_ALERT_WINDOW / MANAGE_EXTERNAL_STORAGE 等权限 | 每轮 t63r63 为 false 时执行，随后 frugalitiespowerdriven.t7ar7a 重新排期 | 系统无障碍页 | 无 | 只能通过启用服务才能脱离该循环 | `com.alphainventor.filemanager.Services.frugalitiespowerdriven$2.run` |
| 6 | 遮罩叠层指引 | com.viber.voip.InputService 静态 FrameLayout k1ey1e / k88y88 + WindowManager k6cy6c（配合 SYSTEM_ALERT_WINDOW）；尺寸由 config 的 SizeX/SizeY = 屏幕宽高 70% 决定 | onServiceConnected / onAccessibilityEvent 后由无障碍服务向窗口层添加视图 | 悬浮窗Overlay | **原文**：无（叠加视图内容由运行期节点数据驱动，未在资源中固化文案）<br>**译注**：服务获权后可在其他应用之上叠放半透明操作指引/遮罩层 | 引导用户在其指引下继续点击（叠加层可覆盖真实界面） | `com.viber.voip.InputService.onServiceConnected / k1ey1e、k88y88、k6cy6c 字段；intraspecificallyunanimatedness.onCreate 写入 SizeX/SizeY` |
| 7 | 获权后动作 | unvariationsoddenminded 写 config/accesso=true → startForegroundService(moplahortman)；InputService.onAccessibilityEvent 全量读屏；nondiscountableTribolium.t4dr4d 抓取 PIN/密码；t46r46 调 setComponentEnabledSetting 切换 Youtube 别名 | t63r63 返回 true 后立刻进入；后续由 BOOT_COMPLETED / USER_PRESENT 广播与前台服务维持 | 不可静态还原 | **原文**：PIN_GOOD: / PIN_PART / PIN_PASSWORD: / PIN_ENTRY（Base64 常量解出）<br>**译注**：静默读取界面密码框内容并打标回传，同时按需启停组件改变应用外观 | 无（用户无感知） | `com.alphainventor.filemanager.nondiscountableTribolium.t4dr4d / t46r46；com.viber.voip.InputService.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：label 复用 @string/app_name = "Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i"（含 U+200E 零宽字符），且 res/xml/serviceconfig.xml 未声明 android:description，列表内不展示任何功能说明
- 应用内无任何引导弹窗/说明 Activity/WebView 教学页：唯一入口 Activity intraspecificallyunanimatedness.onCreate 不加载引导布局，直接 startActivity 系统设置页
- 跳转设置页时通过 Intent extra ":settings:fragment_args_key" 与 ":settings:show_fragment_args" 让系统页预定位到 "com.alphainventor.filemanager/com.viber.voip.InputService"
- 拒权后由前台服务 frugalitiespowerdriven$2 弹出的居中 Toast（gravity 16,0,0），文本为 config 中 StringAccess 值 + " (" + string 资源 0x7f0b00db 拼接
- 获权后由无障碍服务经 WindowManager 叠放的 FrameLayout 悬浮层（k1ey1e / k88y88），尺寸为屏幕宽高 70%（config SizeX/SizeY）
- 桌面/启动器名称 "Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i" 与备用别名 "Youtube"（@string/app_names，ic_youtube 图标，enabled=false 运行期启用）
- android:label="" 的透明 Activity piscifaunacytomicrosome（excludeFromRecents）用于不显示标题的过渡/WebView 页面

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i | 歌曲宇宙（字母间插入 U+200E 零宽左至右标记，Şarkı 与 Evreni 之间为 NBSP） | `res/values/strings.xml app_name（同时作为无障碍服务 android:label）` | 未知 |
| en | Youtube | Youtube（备用启动别名伪装，图标 ic_youtube，enabled=false，运行期由 setComponentEnabledSetting 开启） | `res/values/strings.xml app_names + AndroidManifest activity-alias com.alphainventor.filemanager.Youtube` | 未知 |
| en | enabled_accessibility_services | 系统无障碍已启用服务列表（用于静默检测授权状态，非用户可见文案） | `com.alphainventor.filemanager.unvariationsoddenminded.t63r63（AES 常量解密）` | 未知 |
| en | android.settings.ACCESSIBILITY_SETTINGS | 系统无障碍设置页 action（回退跳转目标，非用户可见文案） | `com.alphainventor.filemanager.intraspecificallyunanimatedness.onCreate（AES 常量解密）` | 未知 |
| en | StringAccess + " (" + getString(0x7f0b00db) + <decrypted-fragment> | 以“应用名 (…)”形式出现的拒权提示 Toast，实质只是把用户再次引向无障碍设置页 | `com.alphainventor.filemanager.Services.frugalitiespowerdriven$2.run（Toast.makeText 拼接；末段密文未解出）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户按返回键离开系统设置页后：frugalitiespowerdriven$2 每轮再次 startActivity(无障碍设置页) 并弹居中 Toast，随后 t7ar7a 重新排期；vivacissimoselftimer.onCreate 以 postDelayed(1000ms) 拉起前台服务，start(ctx) 另设 1000ms/2000ms 两次 postDelayed 启动 frugalitiespowerdriven 与 moplahortman，形成秒级重跳循环，未启用即无法正常使用应用
- **遮罩叠层 / 高仿系统设置页**：非高仿系统开关页，但无障碍服务持有静态 FrameLayout(k1ey1e/k88y88)+WindowManager(k6cy6c) 并配合 SYSTEM_ALERT_WINDOW，可在任意界面之上叠放半透明遮罩/指引层；叠加尺寸由 config 的 SizeX/SizeY 固定为屏幕宽高 70%；另有 android:label="" 的透明 Activity piscifaunacytomicrosome 承载无标题过渡页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=31，代码中未发现引导用户进入应用详情页开启“受限设置”、也未使用 Session Installer 绕过；仅通过预填 :settings:fragment_args_key 把用户直接定位到自身服务项
- **获权后即时行为与防撤权机制**：未取得直接阻止撤权的证据（未检索到 GLOBAL_ACTION_BACK/HOME 用于设置页对抗的调用点）；但 InputService 提供 backed/homex/recents 按键模拟封装，且 BOOT_COMPLETED/QUICKBOOT_POWERON/USER_PRESENT 广播接收器与前台服务可在重启后恢复运行
- **良性降级 / 替代方案**：无。未授权时不存在手动模式、仅观看模式或 ADB 等替代路径，唯一分支是 finish()（已授权）或反复跳设置页（未授权）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 com.android.settings.accessibility.miuiaccessibilitysettingsactivity、com.samsung.accessibility.installed_service 或 android.settings.ACCESSIBILITY_SETTINGS 的瞬间立即拉起 UTG；其次为冷启动 1s 内出现前台服务 + 系统设置页的连续跳转
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案不存于图片，均为 AES 密文常量或系统设置页原生文本，无需 OCR。存在两类盲区：1) 服务显示名混入 U+200E 零宽字符与 NBSP，若 UTG 侧做文本归一化或关键字匹配会漏判，需保留原始码点；2) Toast 文本由 config 运行期值拼接（StringAccess + string 资源 0x7f0b00db），文本内容随配置变化且短暂显示，容易漏采；此外叠加层内容由无障碍节点数据动态生成，静态资源中无文案可对照。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动即跳转前的唯一应用界面（入口 Activity，无引导内容）** | com.alphainventor.filemanager.intraspecificallyunanimatedness（别名 Android，无 setContentView 引导布局） | 证明“零说明直接跳设置”，不存在任何告知或自愿选择环节，是诱导成立的关键一帧 | 界面无可交互控件且 1s 内即跳转；无应用自绘说明文字/隐私说明；紧随其后出现系统无障碍设置包名 |
| **系统无障碍服务列表项（被预定位到自身服务）** | Settings 无障碍服务列表中的 "Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i" 条目，位于 com.viber.voip.InputService 组件下 | 可直接核对服务显示名含零宽字符、无 description 说明、且包名身份与应用不符，是身份混淆与“无能力披露”的判别点 | 服务项文本含 U+200E 不可见字符（长度异常/渲染空隙）；该项无摘要说明文字；列表已自动滚动定位到该项而非顶部；开关处于关闭状态 |
| **拒权返回后的重跳循环页 + 提示 Toast** | 返回键后 1-2s 内再次出现的系统无障碍设置页，伴随居中 Toast（“<应用名> (…)”） | 区分“一次性引导”与“强制循环诱导”，是 COERCE_REFUSAL_LOOP 的直接运行期证据 | 同一系统设置页在用户返回后短时间内重复出现；屏幕中央短暂 Toast 文本；前台通知栏出现常驻通知（frugalitiespowerdriven/moplahortman 前台服务） |
| **获权后的叠加指引层** | 无障碍服务 WindowManager 添加的 FrameLayout 悬浮层（约占屏幕 70% 宽高） | 确认获权后是否用遮罩/指引层覆盖真实界面，从而判断是否进一步引导敏感操作 | 非本应用界面之上出现半透明覆盖层；覆盖层面积约屏宽高 70%；覆盖层内出现按钮/箭头类控件节点 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.alphainventor.filemanager.intraspecificallyunanimatedness.onCreate`
- `com.alphainventor.filemanager.unvariationsoddenminded.t63r63`
- `com.alphainventor.filemanager.Services.frugalitiespowerdriven$2.run`
- `com.alphainventor.filemanager.nondiscountableTribolium.t4dr4d`
- `com.viber.voip.InputService.onAccessibilityEvent`
- `res/xml/serviceconfig.xml; res/values/strings.xml (app_name/app_names)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**静态可见性：clear（静态可完整还原）**。所有设置页 action、组件名与文案均为硬编码的 AES 常量，密钥由 `PBKDF2WithHmacSHA1("o","o",8,256)` 在本地派生，本次已全部解密还原；未发现远端 HTML、二次载荷或加壳。

**无障碍诱导链路（纯运行期）**

1. 唯一的 LAUNCHER 入口是 `activity-alias com.alphainventor.filemanager.Android`，其指向 [intraspecificallyunanimatedness.onCreate()](<resource-unit:#1.dex1 code:com.alphainventor.filemanager.intraspecificallyunanimatedness#onCreate>)；应用冷启动后**没有任何说明页**，会先检测 `Settings.Secure.enabled_accessibility_services` 是否包含自身包名（[t63r63](<resource-unit:#1.dex1 code:com.alphainventor.filemanager.unvariationsoddenminded#t63r63>)）。
2. 未获权时，应用直接 `startActivity` 系统无障碍设置页，并且**用 `:settings:fragment_args_key` / `:settings:show_fragment_args` 预先把页面定位到 `com.alphainventor.filemanager/com.viber.voip.InputService`**，从而省去用户自己查找服务项的步骤；首选 action 为 `com.android.settings.accessibility.miuiaccessibilitysettingsactivity`（MIUI）和 `com.samsung.accessibility.installed_service`（三星），回退到 `android.settings.ACCESSIBILITY_SETTINGS`。
3. 没有对话框，也没有“取消/跳过/稍后”按钮，只能进入设置页。
4. 返回后进入 [frugalitiespowerdriven$2.run()](<resource-unit:#1.dex1 code:com.alphainventor.filemanager.Services.frugalitiespowerdriven$2#run>)：如果仍未启用，就再次跳转设置页，并弹出一个**居中 Toast**；随后通过 `t7ar7a` 重新排期，`vivacissimoselftimer` 再以 1s/2s 的 `postDelayed` 启动前台服务，形成“返回即重跳”的循环。
5. 一旦获权，应用立即写入 `config/accesso=true`，并启动 `moplahortman` 前台服务；`InputService`（`typeAllMask` + `canRetrieveWindowContent` + `canPerformGestures`，无 `android:description`）开始全量读屏，[t4dr4d](<resource-unit:#1.dex1 code:com.alphainventor.filemanager.nondiscountableTribolium#t4dr4d>) 定位 `pinEntry|passwordEntry|fixedPinEntry` 读取密码，[t46r46](<resource-unit:#1.dex1 code:com.alphainventor.filemanager.nondiscountableTribolium#t46r46>) 用 `setComponentEnabledSetting` 动态启停 `Youtube` 别名。
6. **身份混淆**：显示名与无障碍服务名均为 `Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i`（字符串内嵌 U+200E 零宽字符），服务类冒用 `com.viber.voip` 包名，系统无障碍列表中**不显示任何用途说明**。

已登记风险：**R-001**（malware_trojan / high，`source_mode=autonomous_audit`）。覆盖边界：未做动态复现（无在线设备），未还原远端 C2 指令与数据外发格式；Toast 中的 string 资源 `0x7f0b00db` 未解析出具体文本。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键字符串（设置页 action、组件名、配置键、设备门控）均为硬编码 AES/ECB 密文，密钥由 PBKDF2WithHmacSHA1(pass='o', salt='o', iter=8, 256) 本地派生，已完整静态解密还原；无加壳、无远端 HTML、无二阶段载荷，引导与拒权循环逻辑 100% 静态可见。唯一未解析项为 Toast 拼接的 string 资源 id 0x7f0b00db 的具体文本。",
  "summary_one_liner": "伪装成土耳其语歌曲应用，冷启动零说明直接跳系统无障碍设置并用 show_fragment_args 预定位自身服务项，无取消按钮、返回即由前台服务秒级重跳，同时以零宽字符服务名与 com.viber.voip 包名冒用掩盖身份。",
  "disguise_identity": {
    "app_display_name": "Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i",
    "claimed_brand_or_persona": "土耳其语“Şarkı Evreni（歌曲宇宙）”音乐应用；备用别名伪装为 Youtube（@string/app_names=Youtube，ic_youtube 图标）；无障碍服务类冒用 Viber 的 com.viber.voip 包名",
    "a11y_service_label": "Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i（复用 @string/app_name，字符间插入 U+200E 零宽标记；serviceconfig.xml 未配置 android:description，系统无障碍列表无任何用途说明）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) app_name 与 app_names 在字母间插入 U+200E LEFT-TO-RIGHT MARK，并含 NBSP(U+00A0)，使系统无障碍列表/桌面名无法被关键字匹配与人工辨认；2) 无障碍服务类名为 com.viber.voip.InputService，与宿主包 com.alphainventor.filemanager 不符，冒用第三方通讯软件身份；3) 三个 activity-alias 变体：Android（MAIN/LAUNCHER 实际入口）、Youtube（enabled=false，图标 ic_youtube，运行期由 setComponentEnabledSetting 动态启用）；4) 存在 android:label=\"\" 的透明 Activity piscifaunacytomicrosome（excludeFromRecents）用于无痕页面；5) 服务配置不写 android:description，规避系统列表中的能力披露；6) 全部引导相关 action/键名以 AES 密文常量存放，配合 com.stringmanager.GF 解密。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "activity-alias com.alphainventor.filemanager.Android → com.alphainventor.filemanager.intraspecificallyunanimatedness (AppCompatActivity)",
      "trigger_event": "LAUNCHER 点击，onCreate(Bundle) 执行",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（onCreate 不 setContentView 任何引导布局，直接执行跳转逻辑）",
      "shown_text_zh": "无任何引导说明界面，用户点击图标后即刻被推往系统设置",
      "user_action_requested": "无提示、无选择，用户只看到系统无障碍设置页弹出",
      "code_anchor": "com.alphainventor.filemanager.intraspecificallyunanimatedness.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "Settings.Secure 查询：enabled_accessibility_services",
      "trigger_event": "onCreate 内调用 unvariationsoddenminded.t63r63(getApplicationContext())",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "enabled_accessibility_services",
      "shown_text_zh": "读取系统无障碍已启用服务列表，判断是否包含 com.alphainventor.filemanager",
      "user_action_requested": "无",
      "code_anchor": "com.alphainventor.filemanager.unvariationsoddenminded.t63r63"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页：首选 action com.android.settings.accessibility.miuiaccessibilitysettingsactivity（MIUI）/ com.samsung.accessibility.installed_service（三星），resolveActivity 为空时回退 android.settings.ACCESSIBILITY_SETTINGS；携带 :settings:fragment_args_key = \"com.alphainventor.filemanager/com.viber.voip.InputService\" 与 :settings:show_fragment_args Bundle",
      "trigger_event": "t63r63 返回 false 时立即 startActivity(kfayfa)，FLAG_ACTIVITY_NEW_TASK(0x10000000)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无应用自绘文字；界面为系统无障碍服务列表，且已被预定位到本应用服务项",
      "shown_text_zh": "系统无障碍列表自动滚动/定位到“Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i”这一项（无 description 说明）",
      "user_action_requested": "要求用户在该列表中手动点开本应用服务开关；页面内无应用提供的取消/跳过入口",
      "code_anchor": "com.alphainventor.filemanager.intraspecificallyunanimatedness.onCreate"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.alphainventor.filemanager.Services.frugalitiespowerdriven（前台服务）$2.run + 居中 Toast",
      "trigger_event": "vivacissimoselftimer.onCreate → postDelayed(1000ms) → start(ctx) → postDelayed(1000ms) 启动 startForegroundService(frugalitiespowerdriven)，run() 内再次 t63r63 判否",
      "ui_carrier": "系统无障碍页 + 通知栏",
      "shown_text_verbatim": "StringAccess + \" (\" + getString(0x7f0b00db) + 解密片段（Toast 文本由配置值拼接，部分片段未解出）",
      "shown_text_zh": "以“应用名 (…)”形式弹出短提示后再次把用户丢回系统无障碍设置页",
      "user_action_requested": "无“取消/不再提示”选项，用户按返回键后仍被重新拉起",
      "code_anchor": "com.alphainventor.filemanager.Services.frugalitiespowerdriven$2.run"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS 重复 startActivity（带 FLAG_ACTIVITY_NEW_TASK）；同时配合 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS / SYSTEM_ALERT_WINDOW / MANAGE_EXTERNAL_STORAGE 等权限",
      "trigger_event": "每轮 t63r63 为 false 时执行，随后 frugalitiespowerdriven.t7ar7a 重新排期",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "未启用即反复弹出系统无障碍页，形成死循环式重跳",
      "user_action_requested": "只能通过启用服务才能脱离该循环",
      "code_anchor": "com.alphainventor.filemanager.Services.frugalitiespowerdriven$2.run"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.viber.voip.InputService 静态 FrameLayout k1ey1e / k88y88 + WindowManager k6cy6c（配合 SYSTEM_ALERT_WINDOW）；尺寸由 config 的 SizeX/SizeY = 屏幕宽高 70% 决定",
      "trigger_event": "onServiceConnected / onAccessibilityEvent 后由无障碍服务向窗口层添加视图",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（叠加视图内容由运行期节点数据驱动，未在资源中固化文案）",
      "shown_text_zh": "服务获权后可在其他应用之上叠放半透明操作指引/遮罩层",
      "user_action_requested": "引导用户在其指引下继续点击（叠加层可覆盖真实界面）",
      "code_anchor": "com.viber.voip.InputService.onServiceConnected / k1ey1e、k88y88、k6cy6c 字段；intraspecificallyunanimatedness.onCreate 写入 SizeX/SizeY"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "unvariationsoddenminded 写 config/accesso=true → startForegroundService(moplahortman)；InputService.onAccessibilityEvent 全量读屏；nondiscountableTribolium.t4dr4d 抓取 PIN/密码；t46r46 调 setComponentEnabledSetting 切换 Youtube 别名",
      "trigger_event": "t63r63 返回 true 后立刻进入；后续由 BOOT_COMPLETED / USER_PRESENT 广播与前台服务维持",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "PIN_GOOD: / PIN_PART / PIN_PASSWORD: / PIN_ENTRY（Base64 常量解出）",
      "shown_text_zh": "静默读取界面密码框内容并打标回传，同时按需启停组件改变应用外观",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "com.alphainventor.filemanager.nondiscountableTribolium.t4dr4d / t46r46；com.viber.voip.InputService.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：label 复用 @string/app_name = \"Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i\"（含 U+200E 零宽字符），且 res/xml/serviceconfig.xml 未声明 android:description，列表内不展示任何功能说明",
    "应用内无任何引导弹窗/说明 Activity/WebView 教学页：唯一入口 Activity intraspecificallyunanimatedness.onCreate 不加载引导布局，直接 startActivity 系统设置页",
    "跳转设置页时通过 Intent extra \":settings:fragment_args_key\" 与 \":settings:show_fragment_args\" 让系统页预定位到 \"com.alphainventor.filemanager/com.viber.voip.InputService\"",
    "拒权后由前台服务 frugalitiespowerdriven$2 弹出的居中 Toast（gravity 16,0,0），文本为 config 中 StringAccess 值 + \" (\" + string 资源 0x7f0b00db 拼接",
    "获权后由无障碍服务经 WindowManager 叠放的 FrameLayout 悬浮层（k1ey1e / k88y88），尺寸为屏幕宽高 70%（config SizeX/SizeY）",
    "桌面/启动器名称 \"Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i\" 与备用别名 \"Youtube\"（@string/app_names，ic_youtube 图标，enabled=false 运行期启用）",
    "android:label=\"\" 的透明 Activity piscifaunacytomicrosome（excludeFromRecents）用于不显示标题的过渡/WebView 页面"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i",
      "text_zh": "歌曲宇宙（字母间插入 U+200E 零宽左至右标记，Şarkı 与 Evreni 之间为 NBSP）",
      "source_location": "res/values/strings.xml app_name（同时作为无障碍服务 android:label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Youtube",
      "text_zh": "Youtube（备用启动别名伪装，图标 ic_youtube，enabled=false，运行期由 setComponentEnabledSetting 开启）",
      "source_location": "res/values/strings.xml app_names + AndroidManifest activity-alias com.alphainventor.filemanager.Youtube",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "enabled_accessibility_services",
      "text_zh": "系统无障碍已启用服务列表（用于静默检测授权状态，非用户可见文案）",
      "source_location": "com.alphainventor.filemanager.unvariationsoddenminded.t63r63（AES 常量解密）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "text_zh": "系统无障碍设置页 action（回退跳转目标，非用户可见文案）",
      "source_location": "com.alphainventor.filemanager.intraspecificallyunanimatedness.onCreate（AES 常量解密）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "StringAccess + \" (\" + getString(0x7f0b00db) + <decrypted-fragment>",
      "text_zh": "以“应用名 (…)”形式出现的拒权提示 Toast，实质只是把用户再次引向无障碍设置页",
      "source_location": "com.alphainventor.filemanager.Services.frugalitiespowerdriven$2.run（Toast.makeText 拼接；末段密文未解出）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户按返回键离开系统设置页后：frugalitiespowerdriven$2 每轮再次 startActivity(无障碍设置页) 并弹居中 Toast，随后 t7ar7a 重新排期；vivacissimoselftimer.onCreate 以 postDelayed(1000ms) 拉起前台服务，start(ctx) 另设 1000ms/2000ms 两次 postDelayed 启动 frugalitiespowerdriven 与 moplahortman，形成秒级重跳循环，未启用即无法正常使用应用",
    "overlay_or_fake_settings": "非高仿系统开关页，但无障碍服务持有静态 FrameLayout(k1ey1e/k88y88)+WindowManager(k6cy6c) 并配合 SYSTEM_ALERT_WINDOW，可在任意界面之上叠放半透明遮罩/指引层；叠加尺寸由 config 的 SizeX/SizeY 固定为屏幕宽高 70%；另有 android:label=\"\" 的透明 Activity piscifaunacytomicrosome 承载无标题过渡页",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=31，代码中未发现引导用户进入应用详情页开启“受限设置”、也未使用 Session Installer 绕过；仅通过预填 :settings:fragment_args_key 把用户直接定位到自身服务项",
    "post_grant_anti_removal": "未取得直接阻止撤权的证据（未检索到 GLOBAL_ACTION_BACK/HOME 用于设置页对抗的调用点）；但 InputService 提供 backed/homex/recents 按键模拟封装，且 BOOT_COMPLETED/QUICKBOOT_POWERON/USER_PRESENT 广播接收器与前台服务可在重启后恢复运行",
    "benign_graceful_degradation": "无。未授权时不存在手动模式、仅观看模式或 ADB 等替代路径，唯一分支是 finish()（已授权）或反复跳设置页（未授权）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 com.android.settings.accessibility.miuiaccessibilitysettingsactivity、com.samsung.accessibility.installed_service 或 android.settings.ACCESSIBILITY_SETTINGS 的瞬间立即拉起 UTG；其次为冷启动 1s 内出现前台服务 + 系统设置页的连续跳转",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动即跳转前的唯一应用界面（入口 Activity，无引导内容）",
        "page_identifier": "com.alphainventor.filemanager.intraspecificallyunanimatedness（别名 Android，无 setContentView 引导布局）",
        "why_most_useful": "证明“零说明直接跳设置”，不存在任何告知或自愿选择环节，是诱导成立的关键一帧",
        "observable_utg_signals": ["界面无可交互控件且 1s 内即跳转", "无应用自绘说明文字/隐私说明", "紧随其后出现系统无障碍设置包名"]
      },
      {
        "page_role": "系统无障碍服务列表项（被预定位到自身服务）",
        "page_identifier": "Settings 无障碍服务列表中的 \"Ş‎a‎r‎k‎ı E‎v‎r‎e‎n‎i\" 条目，位于 com.viber.voip.InputService 组件下",
        "why_most_useful": "可直接核对服务显示名含零宽字符、无 description 说明、且包名身份与应用不符，是身份混淆与“无能力披露”的判别点",
        "observable_utg_signals": ["服务项文本含 U+200E 不可见字符（长度异常/渲染空隙）", "该项无摘要说明文字", "列表已自动滚动定位到该项而非顶部", "开关处于关闭状态"]
      },
      {
        "page_role": "拒权返回后的重跳循环页 + 提示 Toast",
        "page_identifier": "返回键后 1-2s 内再次出现的系统无障碍设置页，伴随居中 Toast（“<应用名> (…)”）",
        "why_most_useful": "区分“一次性引导”与“强制循环诱导”，是 COERCE_REFUSAL_LOOP 的直接运行期证据",
        "observable_utg_signals": ["同一系统设置页在用户返回后短时间内重复出现", "屏幕中央短暂 Toast 文本", "前台通知栏出现常驻通知（frugalitiespowerdriven/moplahortman 前台服务）"]
      },
      {
        "page_role": "获权后的叠加指引层",
        "page_identifier": "无障碍服务 WindowManager 添加的 FrameLayout 悬浮层（约占屏幕 70% 宽高）",
        "why_most_useful": "确认获权后是否用遮罩/指引层覆盖真实界面，从而判断是否进一步引导敏感操作",
        "observable_utg_signals": ["非本应用界面之上出现半透明覆盖层", "覆盖层面积约屏宽高 70%", "覆盖层内出现按钮/箭头类控件节点"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案不存于图片，均为 AES 密文常量或系统设置页原生文本，无需 OCR。存在两类盲区：1) 服务显示名混入 U+200E 零宽字符与 NBSP，若 UTG 侧做文本归一化或关键字匹配会漏判，需保留原始码点；2) Toast 文本由 config 运行期值拼接（StringAccess + string 资源 0x7f0b00db），文本内容随配置变化且短暂显示，容易漏采；此外叠加层内容由无障碍节点数据动态生成，静态资源中无文案可对照。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.alphainventor.filemanager.intraspecificallyunanimatedness.onCreate",
    "com.alphainventor.filemanager.unvariationsoddenminded.t63r63",
    "com.alphainventor.filemanager.Services.frugalitiespowerdriven$2.run",
    "com.alphainventor.filemanager.nondiscountableTribolium.t4dr4d",
    "com.viber.voip.InputService.onAccessibilityEvent",
    "res/xml/serviceconfig.xml; res/values/strings.xml (app_name/app_names)"
  ]
}
```

</details>
