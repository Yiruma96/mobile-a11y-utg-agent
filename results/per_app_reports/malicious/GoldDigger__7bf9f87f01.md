# MB_061__7bf9f87f01｜GoldDigger — Identitas Kependudukan Digital

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：165.1s

## 1. 一句话核心结论

- **核心申请方式**：以印尼电子身份证应用「Identitas Kependudukan Digital」为名、实际为 com.yqpmd.duxkj.kezuz.pxq 的加密壳样本，通过 ActivationActivity→CheckPermissionActivity→WaitCheckActivity 激活校验链引导用户跳转系统无障碍设置开启 FocusService，并内置 OEM 设置页控件 ID 用于自动点击确认。
- **静态可见性说明**：根 classes.dex 仅含 6 个壳类（com.nashsiqiu.shell.ProxyApplication/ProxyComponentFactory/JniBridge、com.nash.dpt.MainActivity），真实业务 DEX 由 JniBridge.cbde 从 assets/OoooooOooo（2.2MB，非 DEX 魔数）经 libdpt.so native 解密后动态加载。无障碍引导的 Activity 跳转调用点、弹窗布局、ACTION_ACCESSIBILITY_SETTINGS 跳转代码全部位于加密载荷内，静态不可读；Manifest 组件声明、无障碍服务名/label/description、resources.arsc 明文文案与权限声明可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `7bf9f87f01106f544b17c60d9356746917aeb69387a3c03e2bed55a9c485cd4d` |
| 包名 / 年份 | `com.yqpmd.duxkj.kezuz.pxq` / 2025 |
| 家族 / 品类 | **GoldDigger**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Identitas Kependudukan Digital |
| 引导页宣称品牌/身份 | 印尼政府官方电子身份证应用 Identitas Kependudukan Digital（另在引导文案中自称“ssoconnect 安全系统”） |
| 系统无障碍列表服务名 | Identitas Kependudukan Digital |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.yqpmd.duxkj.kezuz.pxq 与显示名无关；真实业务类名与包名整体为 32 位十六进制随机串（cc77874c9e1d94b9e8e054c66ff383450.c55d9ec01b8784b91a95a7ca1a8cff4d5.c903d816578cf439da6f32d7171aa2271）；多个 activity-alias（AliasActivity/AliasTmpActivity/AliasGoogleActivity/AliasTmpActivity）做组件遮蔽；并存 com.sextest.test、asd.fgh.*、asd.kkdaemon/kkalive.* 守护组件与多进程（:daemon/:assist1/:sync/:mr2_process）保活；无障碍 description 仅写应用名而不说明用途，规避系统无障碍风险提示。 |
| 无障碍服务类名 | `cc77874c9e1d94b9e8e054c66ff383450.c55d9ec01b8784b91a95a7ca1a8cff4d5.c903d816578cf439da6f32d7171aa2271.service.FocusService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Identitas Kependudukan Digital |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | ProxyApplication（壳）→ 解密后 SplashActivity / ActivationActivity | 进程启动 attachBaseContext → JniBridge.cbde 解密加载真实 DEX，随后启动解密后业务入口 | 不可静态还原 | **原文**：无（壳阶段无 UI）<br>**译注**：无界面，完成载荷解密与 ClassLoader 替换 | 无 | `com.nashsiqiu.shell.ProxyApplication.attachBaseContext（实际路径 gd_tmp/classes.dex）；解密后入口 cc77874c9e1d94b9e8e054c66ff383450...ui.SplashActivity（Manifest 声明）` |
| 2 | 业务功能触发 | ActivationActivity（Manifest 声明，:assist1 等辅助进程可达） | 启动后进入“激活”流程，推断为权限/服务检查前置页 | 不可静态还原 | **原文**：无（布局位于加密载荷）<br>**译注**：激活引导页，用户须完成“激活”才能使用后续功能 | 推断为点击“启动服务/开始激活”按钮（对应明文文案「启动服务」），取消/跳过按钮不可静态确认 | `...c903d816578cf439da6f32d7171aa2271.ui.ActivationActivity（Manifest）` |
| 3 | 引导说明页 | CheckPermissionActivity（权限自检页）+ 明文文案「请单击以启用辅助功能。」「请求可访问权」 | onCreate/onResume 检测无障碍服务未启用 | 不可静态还原（资源键 go_to_accessibility_setting 与 accessibility_service_description 已确认存在） | **原文**：请单击以启用辅助功能。 / 请求可访问权 / 如果没有开启权限 会影响部分功能的正常使用。<br>**译注**：“请单击以启用辅助功能”“请求可访问权”“如果没有开启权限，会影响部分功能的正常使用” | 引导用户点击以启用无障碍服务；拒绝后以“功能受损”施压，是否可取消不可静态确认 | `resources.arsc 明文串 请单击以启用辅助功能。 / 请求可访问权 / go_to_accessibility_setting；...ui.CheckPermissionActivity（Manifest）` |
| 4 | 跳受限设置 / 跳无障碍设置 | 系统「设置 → 无障碍 → 已安装的服务」列表页，列表项名称为 Identitas Kependudukan Digital | 点击引导按钮后以 ACTION_ACCESSIBILITY_SETTINGS 跳转（调用点位于加密载荷，未静态还原） | 系统无障碍页 | **原文**：Identitas Kependudukan Digital（服务 label 与 android:description 均为该名）<br>**译注**：系统无障碍服务列表中显示为“Identitas Kependudukan Digital”，不暴露真实用途 | 用户手动在系统列表中打开该服务开关；同时文案「1. 给出“ssoconnect 安全系统”“辅助功能”“辅助功能模式”“启用访问”」为分步教学口径 | `Manifest：...service.FocusService，android:label / android:description = Identitas Kependudukan Digital；res/xml/touch_accessibility_service_config.xml` |
| 5 | 拒权反馈循环 | WaitCheckActivity（等待校验页）+ 明文文案「取得权限失败…请『设置 → 应用程序 → 当前App → 权限』」 | 从系统设置返回 onResume 时轮询 AccessibilityManager 状态，未启用则停留/重跳 | 不可静态还原（透明 Activity TransplentPermissionActivity 亦被声明，可用于无感压栈） | **原文**：1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。<br>**译注**：“1.取得权限失败，无法执行操作。2.若先前拒绝了权限授予而没有出现权限请求画面，请进入『设置→应用程序→当前App→权限』把「%s」勾选允许。” | 按教学再次进入设置页勾选权限/开启服务；是否提供跳过不可静态确认 | `...ui.WaitCheckActivity / ...ui.TransplentPermissionActivity（Manifest）；resources.arsc 明文串` |
| 6 | 获权后动作 | FocusService（无障碍服务）+ SettingSafePwdActivity / SettingInquirePwdActivity / LoginActivity / FaceActivity / UploadIDPhotosActivity | onAccessibilityEvent 监听窗口变化（资源中已见 onAccessibilityEvent:rootNode1） | 不可静态还原（资源中硬编码 com.samsung.accessibility...subsettings、com.oplus.screenrecorder.FloatView、com.oplus.launcher:id/btn_negative 等 OEM 设置页控件 ID） | **原文**：onAccessibilityEvent:rootNode1 / 客户端收到27指令开始获取黑屏助手数据,检测到无障碍状态为：%s / 系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s<br>**译注**：无障碍事件回调记录；“收到 27 指令开始获取黑屏助手数据，检测无障碍状态”；“系统检测无障碍是否开启” | 无（获权后转为后台自动操作：读取屏幕、自动点击系统设置/授权弹窗、录屏与短信/联系人采集） | `...service.FocusService / ...record.ScreenRecordService / ...record.DisplayService（Manifest）；resources.arsc 明文串` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：android:label 与 android:description 均为「Identitas Kependudukan Digital」，不说明真实用途
- 解密后业务 Activity 内的权限引导页（CheckPermissionActivity / ActivationActivity）——布局位于加密载荷，静态不可读
- resources.arsc 明文资源串「请单击以启用辅助功能。」「请求可访问权」——由解密后 Activity 加载展示
- resources.arsc 明文串「1. 给出“ssoconnect 安全系统”“辅助功能”“辅助功能模式”“启用访问”」——跳转系统设置后的分步教学文案
- resources.arsc 明文串「1.取得权限失败，无法执行操作。2.若因先前拒绝了权限授予…请『设置 → 应用程序 → 当前App → 权限』」——拒权后的二次引导（简体与繁体两版）
- resources.arsc 明文串「如果没有开启权限 会影响部分功能的正常使用。」——弱化拒绝意愿的施压文案
- WaitCheckActivity 等待校验页（跳设置返回后轮询状态）——布局不可静态还原
- TransplentPermissionActivity 透明 Activity——可作为跳设置前的无感压栈/遮罩载体（形态不可静态确认）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| zh | 请单击以启用辅助功能。 | 请点击以启用辅助功能。 | `resources.arsc 字符串资源（明文）` | 受限设置分步教学 |
| zh | 请求可访问权 | 请求可访问权（申请无障碍权限） | `resources.arsc 字符串资源（明文）` | 受限设置分步教学 |
| zh | 1. 给出“ssoconnect 安全系统”“辅助功能”“辅助功能模式”“启用访问” | 1. 在“ssoconnect 安全系统”中依次选择“辅助功能”→“辅助功能模式”→“启用访问” | `resources.arsc 字符串资源（明文）` | 假反诈安全 |
| zh | 1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。 | 1. 获取权限失败，无法执行操作。2. 若因之前拒绝授权而未弹出权限请求框，请进入『设置 → 应用程序 → 当前App → 权限』把「%s」勾选为允许。 | `resources.arsc 字符串资源（明文，另有繁体版本）` | 受限设置分步教学 |
| zh | 如果没有开启权限 会影响部分功能的正常使用。 | 如果没有开启权限，会影响部分功能的正常使用。 | `resources.arsc 字符串资源（明文）` | 未知 |
| zh | 系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s | 系统检测无障碍是否开启：%s，应用内无状态服务对象是否允许：%s | `resources.arsc 字符串资源（明文）` | 未知 |
| zh | 客户端收到27指令开始获取黑屏助手数据,检测到无障碍状态为：%s | 客户端收到 27 号指令，开始获取“黑屏助手”数据，检测到无障碍状态为：%s | `resources.arsc 字符串资源（明文）` | 未知 |
| id | Identitas Kependudukan Digital | 数字居民身份（印尼官方电子身份证应用名称） | `AndroidManifest.xml android:label / android:description（无障碍服务 FocusService）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：推断为跳转系统设置后由 WaitCheckActivity 在 onResume/定时轮询 AccessibilityManager 状态，未启用则停留在等待页并重复提示「取得权限失败，无法执行操作」及跳设置教学（调用点位于加密载荷，未静态还原）；是否死循环重跳不可静态确认
- **遮罩叠层 / 高仿系统设置页**：资源中硬编码 com.samsung.accessibility.core.winset.activity.subsettings、com.oplus.screenrecorder.FloatView、com.oplus.launcher:id/btn_negative 等 OEM 设置页与弹窗控件 ID，表明获权后由 FocusService 对真实系统设置/授权弹窗做定向点击，而非自绘高仿开关页；另声明 TransplentPermissionActivity 透明页与 SYSTEM_ALERT_WINDOW 权限，具备压栈遮罩能力（形态不可静态确认）
- **Android 13+ 受限设置（Restricted Settings）应对**：有明确的分步教学文案「设置 → 应用程序 → 当前App → 权限」及「给出“ssoconnect 安全系统”“辅助功能”“辅助功能模式”“启用访问”」；是否针对 Android 13+ 应用详情右上角“允许受限设置”或 Session 安装器绕过，因代码加密不可静态确认
- **获权后即时行为与防撤权机制**：推断存在：FocusService 可读取窗口节点并点击（onAccessibilityEvent 回调 + OEM 控件 ID），具备在设置页自动确认/阻止撤权的技术条件；另有 asd.kkdaemon/kkalive 守护、BIND_DEVICE_ADMIN、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 防卸载保活。具体 GLOBAL_ACTION_BACK/HOME 阻断代码位于加密载荷，未静态还原
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以冷启动为起点全程录制：从 launcher 点击图标即开始 UTG 采集（壳解密约需数百毫秒，引导页紧随 SplashActivity 出现）；同时对 Activity 切换打点，一旦监测到 Activity 名包含 ActivationActivity / CheckPermissionActivity / WaitCheckActivity / TransplentPermissionActivity，或窗口为 com.android.settings 无障碍页时立即抓取节点树快照
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区在静态侧：业务 DEX 整体加密（assets/OoooooOooo + libdpt.so），跳转 ACTION_ACCESSIBILITY_SETTINGS 的具体调用点、弹窗布局与拒权重跳实现不可静态还原，须依赖运行期 UTG 补全；另资源中大量加密串（形如 Base64+“[.tnB]”标记）提示存在远端下发文案/配置的可能，若引导话术为云端下发则静态与首次运行均可能取不到全量文本。此外壳层多进程守护（:daemon/:assist1/:sync）可能在主进程被结束前后台重拉引导页。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗/激活页** | Activity 名 ...c903d816...ui.ActivationActivity 或 ...ui.CheckPermissionActivity 的窗口 | 这是诱导链的起点，决定是否存在“不可取消”的强制引导与初始话术 | 弹窗按钮文本集合（是否有“取消/跳过/以后再说”）；是否 setCancelable(false) 或返回键无效；文案关键词：辅助功能、请求可访问权、启用访问 |
| **跳转系统无障碍设置前的教学页** | 从 CheckPermissionActivity 跳转到 com.android.settings 无障碍页之前的画面；或 TransplentPermissionActivity 透明窗口 | 区分是“单纯跳设置”还是“叠层遮罩指引”，并抓取分步教学原文 | 页面文本是否包含“辅助功能模式”“启用访问”；是否为全屏/半透明覆盖层；目标设置页 package/class 名 |
| **系统无障碍服务列表项** | com.android.settings 无障碍服务列表中 label 为 Identitas Kependudukan Digital 的条目 | 核对系统侧呈现的服务名与描述是否与应用真实用途不符，是身份伪装最直接的运行期证据 | 服务条目 label 文本；系统是否弹出“此服务可查看屏幕内容/控制设备”警告及用户是否被引导忽略；应用是否在此时拉起悬浮窗/遮罩 |
| **返回后的等待校验页与拒权反馈** | Activity 名 ...ui.WaitCheckActivity；或用户按返回键离开系统设置后重新出现的引导页 | 判定拒绝后是否形成重跳/定时拉起闭环（诱导强度的关键指标） | 返回后 X 秒内是否再次跳转 ACCESSIBILITY_SETTINGS；重复出现的提示文案与次数；是否存在“取得权限失败”文案 |
| **获权后自动操作阶段** | FocusService 运行时叠加的悬浮窗/自动点击痕迹，以及 ScreenRecordService、SettingSafePwdActivity 等后续页 | 确认获权后是否立即转为自动点击系统弹窗与采集行为（授权即被利用） | 系统授权弹窗被非用户点击自动确认；屏幕录制/无障碍读屏指示图标出现；跳转到设置密码类页面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `<local_path> code:com.nashsiqiu.shell.ProxyApplication#attachBaseContext`
- `<local_path> code:com.nashsiqiu.shell.JniBridge#cbde`
- `<local_path> file:all（FocusService / ActivationActivity / CheckPermissionActivity / WaitCheckActivity / TransplentPermissionActivity 声明）`
- `<local_path> file:all（请单击以启用辅助功能。 / 请求可访问权 / go_to_accessibility_setting / accessibility_service_description）`
- `assets/OoooooOooo（加密业务 DEX 载荷，2.2MB，未还原）`
- `res/xml/touch_accessibility_service_config.xml（无障碍服务配置）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**静态可见性：`packed_or_encrypted`。** 该样本的 DEX 已被壳整体加密，因此无法直接查看无障碍引导的具体界面代码；但 Manifest 与 `resources.arsc` 的明文信息已足以还原出完整的权限获取链的骨架。

**已证实事实**

- **壳结构**：根目录 `classes.dex` 仅包含 6 个类，全部属于 `com.nashsiqiu.shell`（`ProxyApplication`、`ProxyComponentFactory`、`JniBridge`）和 `com.nash.dpt.MainActivity`，没有任何业务实现。
- **解密链**：[ProxyApplication.attachBaseContext()](<resource-unit:<local_path> code:com.nashsiqiu.shell.ProxyApplication#attachBaseContext>) 先从 `assets/app_name` 读出真实业务包名（`cc77874c9e1d94b9e8e054c66ff383450...`），随后调用 `JniBridge.loadShellLibs`、`JniBridge.ia()`、[JniBridge.cbde()](<resource-unit:<local_path> code:com.nashsiqiu.shell.JniBridge#cbde>)，由 native 逻辑解密 2.2 MB 的 `assets/OoooooOooo`（非 DEX 魔数），并替换 ClassLoader。`assets/vwwwwwvwww/{arm,arm64,x86,x86_64}/libdpt.so` 是壳本体。
- **身份伪装**：桌面显示名与无障碍服务标签和描述均为 `Identitas Kependudukan Digital`（印尼官方电子身份证应用），而实际包名为 `com.yqpmd.duxkj.kezuz.pxq`；Manifest 内还并存 `com.sextest.test`、`asd.fgh.*`、`asd.kkdaemon/kkalive.*` 等守护组件，以及 `AliasActivity`、`AliasTmpActivity`、`AliasGoogleActivity` 多个 activity-alias。
- **引导链组件（Manifest 明文）**：`...c903d816...ui.ActivationActivity`、`WaitCheckActivity`、`CheckPermissionActivity`、`TransplentPermissionActivity`（透明Activity，可做无感拉起）、`UploadIDPhotosActivity`、`LoginActivity`、`FaceActivity`，以及 `service.FocusService`（无障碍）、`ScreenRecordService`/`DisplayService`/`AudioService`/`CameraService`。
- **引导文案（resources.arsc 明文）**：存在 `go_to_accessibility_setting`、`accessibility_service_description`、`touch_accessibility_service_config` 资源键，以及「请单击以启用辅助功能。」「请求可访问权」「1. 给出“ssoconnect 安全系统”“辅助功能”“辅助功能模式”“启用访问”」「如果没有开启权限 会影响部分功能的正常使用。」「启动服务」等字符串。
- **高仿/自动化系统设置证据**：资源中直接硬编码了 `com.samsung.accessibility.core.winset.activity.subsettings`、`com.oplus.screenrecorder.FloatView`、`com.oplus.launcher:id/btn_negative`、`com.android.settings` 相关包名与控件 ID，说明 `FocusService` 具备对 OEM 设置页与弹窗做定向点击的能力（用于点击“确定/允许”类按钮）。
- **高风险权限组合**：`READ_SMS`/`RECEIVE_SMS`/`SEND_SMS`、`READ_CONTACTS`、`RECORD_AUDIO`、`CALL_PHONE`、`CAMERA`、`SYSTEM_ALERT_WINDOW`、`QUERY_ALL_PACKAGES`、`WRITE_SETTINGS`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`、`BIND_DEVICE_ADMIN`。

**推断（受限于加密载荷，需动态核实）**

- 冷启动或 `ActivationActivity` → `CheckPermissionActivity` 逐项申请运行时权限 → 跳转系统无障碍设置 → `WaitCheckActivity` 轮询 `AccessibilityManager` 状态 → 获权后由 `FocusService` 接管自动点击。`WaitCheckActivity` 的存在强烈暗示了“跳设置后回跳轮询”的闭环结构。
- `TransplentPermissionActivity` + `SYSTEM_ALERT_WINDOW` 支持“透明压栈/悬浮遮罩”形态，但具体是否叠层无法静态确认。

**覆盖边界**：解包目录被污染（`AndroidManifest.xml` 权限拒绝、文件名损坏），本次改为直接从 APK 手工提取 `classes.dex`/`AndroidManifest.xml`/`resources.arsc` 完成核验；`assets/OoooooOooo` 的 native 解密未还原，故无障碍引导的具体 Activity 跳转调用点与逐屏文案载体记为不可静态还原。

已登记风险 **R-001**（malware_trojan / high）：以印尼电子身份证品牌伪装、DEX 整体加密、无障碍服务 `FocusService` 与短信/联系人/录音/通话权限组合。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "根 classes.dex 仅含 6 个壳类（com.nashsiqiu.shell.ProxyApplication/ProxyComponentFactory/JniBridge、com.nash.dpt.MainActivity），真实业务 DEX 由 JniBridge.cbde 从 assets/OoooooOooo（2.2MB，非 DEX 魔数）经 libdpt.so native 解密后动态加载。无障碍引导的 Activity 跳转调用点、弹窗布局、ACTION_ACCESSIBILITY_SETTINGS 跳转代码全部位于加密载荷内，静态不可读；Manifest 组件声明、无障碍服务名/label/description、resources.arsc 明文文案与权限声明可见。",
  "summary_one_liner": "以印尼电子身份证应用「Identitas Kependudukan Digital」为名、实际为 com.yqpmd.duxkj.kezuz.pxq 的加密壳样本，通过 ActivationActivity→CheckPermissionActivity→WaitCheckActivity 激活校验链引导用户跳转系统无障碍设置开启 FocusService，并内置 OEM 设置页控件 ID 用于自动点击确认。",
  "disguise_identity": {
    "app_display_name": "Identitas Kependudukan Digital",
    "claimed_brand_or_persona": "印尼政府官方电子身份证应用 Identitas Kependudukan Digital（另在引导文案中自称“ssoconnect 安全系统”）",
    "a11y_service_label": "Identitas Kependudukan Digital",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.yqpmd.duxkj.kezuz.pxq 与显示名无关；真实业务类名与包名整体为 32 位十六进制随机串（cc77874c9e1d94b9e8e054c66ff383450.c55d9ec01b8784b91a95a7ca1a8cff4d5.c903d816578cf439da6f32d7171aa2271）；多个 activity-alias（AliasActivity/AliasTmpActivity/AliasGoogleActivity/AliasTmpActivity）做组件遮蔽；并存 com.sextest.test、asd.fgh.*、asd.kkdaemon/kkalive.* 守护组件与多进程（:daemon/:assist1/:sync/:mr2_process）保活；无障碍 description 仅写应用名而不说明用途，规避系统无障碍风险提示。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "ProxyApplication（壳）→ 解密后 SplashActivity / ActivationActivity",
      "trigger_event": "进程启动 attachBaseContext → JniBridge.cbde 解密加载真实 DEX，随后启动解密后业务入口",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（壳阶段无 UI）",
      "shown_text_zh": "无界面，完成载荷解密与 ClassLoader 替换",
      "user_action_requested": "无",
      "code_anchor": "com.nashsiqiu.shell.ProxyApplication.attachBaseContext（实际路径 gd_tmp/classes.dex）；解密后入口 cc77874c9e1d94b9e8e054c66ff383450...ui.SplashActivity（Manifest 声明）"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "ActivationActivity（Manifest 声明，:assist1 等辅助进程可达）",
      "trigger_event": "启动后进入“激活”流程，推断为权限/服务检查前置页",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（布局位于加密载荷）",
      "shown_text_zh": "激活引导页，用户须完成“激活”才能使用后续功能",
      "user_action_requested": "推断为点击“启动服务/开始激活”按钮（对应明文文案「启动服务」），取消/跳过按钮不可静态确认",
      "code_anchor": "...c903d816578cf439da6f32d7171aa2271.ui.ActivationActivity（Manifest）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "CheckPermissionActivity（权限自检页）+ 明文文案「请单击以启用辅助功能。」「请求可访问权」",
      "trigger_event": "onCreate/onResume 检测无障碍服务未启用",
      "ui_carrier": "不可静态还原（资源键 go_to_accessibility_setting 与 accessibility_service_description 已确认存在）",
      "shown_text_verbatim": "请单击以启用辅助功能。 / 请求可访问权 / 如果没有开启权限 会影响部分功能的正常使用。",
      "shown_text_zh": "“请单击以启用辅助功能”“请求可访问权”“如果没有开启权限，会影响部分功能的正常使用”",
      "user_action_requested": "引导用户点击以启用无障碍服务；拒绝后以“功能受损”施压，是否可取消不可静态确认",
      "code_anchor": "resources.arsc 明文串 请单击以启用辅助功能。 / 请求可访问权 / go_to_accessibility_setting；...ui.CheckPermissionActivity（Manifest）"
    },
    {
      "step": 4,
      "stage": "跳受限设置 / 跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍 → 已安装的服务」列表页，列表项名称为 Identitas Kependudukan Digital",
      "trigger_event": "点击引导按钮后以 ACTION_ACCESSIBILITY_SETTINGS 跳转（调用点位于加密载荷，未静态还原）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Identitas Kependudukan Digital（服务 label 与 android:description 均为该名）",
      "shown_text_zh": "系统无障碍服务列表中显示为“Identitas Kependudukan Digital”，不暴露真实用途",
      "user_action_requested": "用户手动在系统列表中打开该服务开关；同时文案「1. 给出“ssoconnect 安全系统”“辅助功能”“辅助功能模式”“启用访问”」为分步教学口径",
      "code_anchor": "Manifest：...service.FocusService，android:label / android:description = Identitas Kependudukan Digital；res/xml/touch_accessibility_service_config.xml"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "WaitCheckActivity（等待校验页）+ 明文文案「取得权限失败…请『设置 → 应用程序 → 当前App → 权限』」",
      "trigger_event": "从系统设置返回 onResume 时轮询 AccessibilityManager 状态，未启用则停留/重跳",
      "ui_carrier": "不可静态还原（透明 Activity TransplentPermissionActivity 亦被声明，可用于无感压栈）",
      "shown_text_verbatim": "1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。",
      "shown_text_zh": "“1.取得权限失败，无法执行操作。2.若先前拒绝了权限授予而没有出现权限请求画面，请进入『设置→应用程序→当前App→权限』把「%s」勾选允许。”",
      "user_action_requested": "按教学再次进入设置页勾选权限/开启服务；是否提供跳过不可静态确认",
      "code_anchor": "...ui.WaitCheckActivity / ...ui.TransplentPermissionActivity（Manifest）；resources.arsc 明文串"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "FocusService（无障碍服务）+ SettingSafePwdActivity / SettingInquirePwdActivity / LoginActivity / FaceActivity / UploadIDPhotosActivity",
      "trigger_event": "onAccessibilityEvent 监听窗口变化（资源中已见 onAccessibilityEvent:rootNode1）",
      "ui_carrier": "不可静态还原（资源中硬编码 com.samsung.accessibility...subsettings、com.oplus.screenrecorder.FloatView、com.oplus.launcher:id/btn_negative 等 OEM 设置页控件 ID）",
      "shown_text_verbatim": "onAccessibilityEvent:rootNode1 / 客户端收到27指令开始获取黑屏助手数据,检测到无障碍状态为：%s / 系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s",
      "shown_text_zh": "无障碍事件回调记录；“收到 27 指令开始获取黑屏助手数据，检测无障碍状态”；“系统检测无障碍是否开启”",
      "user_action_requested": "无（获权后转为后台自动操作：读取屏幕、自动点击系统设置/授权弹窗、录屏与短信/联系人采集）",
      "code_anchor": "...service.FocusService / ...record.ScreenRecordService / ...record.DisplayService（Manifest）；resources.arsc 明文串"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：android:label 与 android:description 均为「Identitas Kependudukan Digital」，不说明真实用途",
    "解密后业务 Activity 内的权限引导页（CheckPermissionActivity / ActivationActivity）——布局位于加密载荷，静态不可读",
    "resources.arsc 明文资源串「请单击以启用辅助功能。」「请求可访问权」——由解密后 Activity 加载展示",
    "resources.arsc 明文串「1. 给出“ssoconnect 安全系统”“辅助功能”“辅助功能模式”“启用访问”」——跳转系统设置后的分步教学文案",
    "resources.arsc 明文串「1.取得权限失败，无法执行操作。2.若因先前拒绝了权限授予…请『设置 → 应用程序 → 当前App → 权限』」——拒权后的二次引导（简体与繁体两版）",
    "resources.arsc 明文串「如果没有开启权限 会影响部分功能的正常使用。」——弱化拒绝意愿的施压文案",
    "WaitCheckActivity 等待校验页（跳设置返回后轮询状态）——布局不可静态还原",
    "TransplentPermissionActivity 透明 Activity——可作为跳设置前的无感压栈/遮罩载体（形态不可静态确认）"
  ],
  "verbatim_texts": [
    {
      "lang": "zh",
      "text_verbatim": "请单击以启用辅助功能。",
      "text_zh": "请点击以启用辅助功能。",
      "source_location": "resources.arsc 字符串资源（明文）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "请求可访问权",
      "text_zh": "请求可访问权（申请无障碍权限）",
      "source_location": "resources.arsc 字符串资源（明文）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "1. 给出“ssoconnect 安全系统”“辅助功能”“辅助功能模式”“启用访问”",
      "text_zh": "1. 在“ssoconnect 安全系统”中依次选择“辅助功能”→“辅助功能模式”→“启用访问”",
      "source_location": "resources.arsc 字符串资源（明文）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "zh",
      "text_verbatim": "1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。",
      "text_zh": "1. 获取权限失败，无法执行操作。2. 若因之前拒绝授权而未弹出权限请求框，请进入『设置 → 应用程序 → 当前App → 权限』把「%s」勾选为允许。",
      "source_location": "resources.arsc 字符串资源（明文，另有繁体版本）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "如果没有开启权限 会影响部分功能的正常使用。",
      "text_zh": "如果没有开启权限，会影响部分功能的正常使用。",
      "source_location": "resources.arsc 字符串资源（明文）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s",
      "text_zh": "系统检测无障碍是否开启：%s，应用内无状态服务对象是否允许：%s",
      "source_location": "resources.arsc 字符串资源（明文）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "客户端收到27指令开始获取黑屏助手数据,检测到无障碍状态为：%s",
      "text_zh": "客户端收到 27 号指令，开始获取“黑屏助手”数据，检测到无障碍状态为：%s",
      "source_location": "resources.arsc 字符串资源（明文）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "id",
      "text_verbatim": "Identitas Kependudukan Digital",
      "text_zh": "数字居民身份（印尼官方电子身份证应用名称）",
      "source_location": "AndroidManifest.xml android:label / android:description（无障碍服务 FocusService）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "推断为跳转系统设置后由 WaitCheckActivity 在 onResume/定时轮询 AccessibilityManager 状态，未启用则停留在等待页并重复提示「取得权限失败，无法执行操作」及跳设置教学（调用点位于加密载荷，未静态还原）；是否死循环重跳不可静态确认",
    "overlay_or_fake_settings": "资源中硬编码 com.samsung.accessibility.core.winset.activity.subsettings、com.oplus.screenrecorder.FloatView、com.oplus.launcher:id/btn_negative 等 OEM 设置页与弹窗控件 ID，表明获权后由 FocusService 对真实系统设置/授权弹窗做定向点击，而非自绘高仿开关页；另声明 TransplentPermissionActivity 透明页与 SYSTEM_ALERT_WINDOW 权限，具备压栈遮罩能力（形态不可静态确认）",
    "restricted_settings_13plus_coaching": "有明确的分步教学文案「设置 → 应用程序 → 当前App → 权限」及「给出“ssoconnect 安全系统”“辅助功能”“辅助功能模式”“启用访问”」；是否针对 Android 13+ 应用详情右上角“允许受限设置”或 Session 安装器绕过，因代码加密不可静态确认",
    "post_grant_anti_removal": "推断存在：FocusService 可读取窗口节点并点击（onAccessibilityEvent 回调 + OEM 控件 ID），具备在设置页自动确认/阻止撤权的技术条件；另有 asd.kkdaemon/kkalive 守护、BIND_DEVICE_ADMIN、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 防卸载保活。具体 GLOBAL_ACTION_BACK/HOME 阻断代码位于加密载荷，未静态还原",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以冷启动为起点全程录制：从 launcher 点击图标即开始 UTG 采集（壳解密约需数百毫秒，引导页紧随 SplashActivity 出现）；同时对 Activity 切换打点，一旦监测到 Activity 名包含 ActivationActivity / CheckPermissionActivity / WaitCheckActivity / TransplentPermissionActivity，或窗口为 com.android.settings 无障碍页时立即抓取节点树快照",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗/激活页",
        "page_identifier": "Activity 名 ...c903d816...ui.ActivationActivity 或 ...ui.CheckPermissionActivity 的窗口",
        "why_most_useful": "这是诱导链的起点，决定是否存在“不可取消”的强制引导与初始话术",
        "observable_utg_signals": ["弹窗按钮文本集合（是否有“取消/跳过/以后再说”）", "是否 setCancelable(false) 或返回键无效", "文案关键词：辅助功能、请求可访问权、启用访问"]
      },
      {
        "page_role": "跳转系统无障碍设置前的教学页",
        "page_identifier": "从 CheckPermissionActivity 跳转到 com.android.settings 无障碍页之前的画面；或 TransplentPermissionActivity 透明窗口",
        "why_most_useful": "区分是“单纯跳设置”还是“叠层遮罩指引”，并抓取分步教学原文",
        "observable_utg_signals": ["页面文本是否包含“辅助功能模式”“启用访问”", "是否为全屏/半透明覆盖层", "目标设置页 package/class 名"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍服务列表中 label 为 Identitas Kependudukan Digital 的条目",
        "why_most_useful": "核对系统侧呈现的服务名与描述是否与应用真实用途不符，是身份伪装最直接的运行期证据",
        "observable_utg_signals": ["服务条目 label 文本", "系统是否弹出“此服务可查看屏幕内容/控制设备”警告及用户是否被引导忽略", "应用是否在此时拉起悬浮窗/遮罩"]
      },
      {
        "page_role": "返回后的等待校验页与拒权反馈",
        "page_identifier": "Activity 名 ...ui.WaitCheckActivity；或用户按返回键离开系统设置后重新出现的引导页",
        "why_most_useful": "判定拒绝后是否形成重跳/定时拉起闭环（诱导强度的关键指标）",
        "observable_utg_signals": ["返回后 X 秒内是否再次跳转 ACCESSIBILITY_SETTINGS", "重复出现的提示文案与次数", "是否存在“取得权限失败”文案"]
      },
      {
        "page_role": "获权后自动操作阶段",
        "page_identifier": "FocusService 运行时叠加的悬浮窗/自动点击痕迹，以及 ScreenRecordService、SettingSafePwdActivity 等后续页",
        "why_most_useful": "确认获权后是否立即转为自动点击系统弹窗与采集行为（授权即被利用）",
        "observable_utg_signals": ["系统授权弹窗被非用户点击自动确认", "屏幕录制/无障碍读屏指示图标出现", "跳转到设置密码类页面"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区在静态侧：业务 DEX 整体加密（assets/OoooooOooo + libdpt.so），跳转 ACTION_ACCESSIBILITY_SETTINGS 的具体调用点、弹窗布局与拒权重跳实现不可静态还原，须依赖运行期 UTG 补全；另资源中大量加密串（形如 Base64+“[.tnB]”标记）提示存在远端下发文案/配置的可能，若引导话术为云端下发则静态与首次运行均可能取不到全量文本。此外壳层多进程守护（:daemon/:assist1/:sync）可能在主进程被结束前后台重拉引导页。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "<local_path> code:com.nashsiqiu.shell.ProxyApplication#attachBaseContext",
    "<local_path> code:com.nashsiqiu.shell.JniBridge#cbde",
    "<local_path> file:all（FocusService / ActivationActivity / CheckPermissionActivity / WaitCheckActivity / TransplentPermissionActivity 声明）",
    "<local_path> file:all（请单击以启用辅助功能。 / 请求可访问权 / go_to_accessibility_setting / accessibility_service_description）",
    "assets/OoooooOooo（加密业务 DEX 载荷，2.2MB，未还原）",
    "res/xml/touch_accessibility_service_config.xml（无障碍服务配置）"
  ]
}
```

</details>
