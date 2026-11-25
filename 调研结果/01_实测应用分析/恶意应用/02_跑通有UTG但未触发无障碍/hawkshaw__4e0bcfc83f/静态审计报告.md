# MR_057__4e0bcfc83f｜hawkshaw — AppleProtect

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：80.5s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 AppleProtect 安全工具的应用在隐藏登录成功后立刻弹出 setCancelable(false) 的原生弹窗，一键跳系统无障碍列表并靠 onActivityResult 死循环重弹逼迫用户为 me.hawkshaw.tasks.Accessibility 开启读屏权，随后连环索取通知监听/电池白名单/录屏/设备管理器/悬浮窗/受限设置。
- **静态可见性说明**：无障碍引导全链路（登录门槛→不可取消弹窗→跳 ACCESSIBILITY_SETTINGS→返回重弹→一揽子权限链→获权后 GLOBAL_ACTION_BACK）均在 DEX1 中完整静态可见；未加壳、无加密载荷、无远端 HTML/WebView 承载引导，引导文案全部来自 res/values/strings.xml 与硬编码字面量。未纳入本次核验的 me.hawkshaw.tasks.Accessibility.a(AccessibilityEvent) 具体窃取动作与远端 C2 指令解析不属于本轮 UTG 页面流转范围。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4e0bcfc83f8a2714acbf1725262827ec17f61c5826cd5cf0837d1642fdc5b25e` |
| 包名 / 年份 | `se.spitfire.appleprotect.it` / 2021 |
| 家族 / 品类 | **hawkshaw**（同池样本数：48） |
| 原始来源标识 | https://research.checkpoint.com/2021/going-rogue-a-mastermind-behind-android-malware-returns-with-a-new-rat/ |
| 桌面显示名 | AppleProtect |
| 引导页宣称品牌/身份 | AppleProtect（暗示 Apple / 苹果设备安全防护工具，实际与 Apple Inc. 无任何关系） |
| 系统无障碍列表服务名 | AppleProtect |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:label 与 app_name 同为 AppleProtect、android:description 写作 'Accessibility helps us to secure your device'，将读屏权包装为安全防护；包内同时残留 se.joscarsson.privify（Privify 照片保险箱）与 me.hawkshaw（远控框架）两套工程命名，与宣称品牌不一致。未使用空白/换行挤出警告、同形字、多 activity-alias，也未伪造 isAccessibilityTool（targetSdkVersion=21，该 API 不存在）。 |
| 无障碍服务类名 | `me.hawkshaw.tasks.Accessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Accessibility helps us to secure your device |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | me.hawkshaw.HawkshawMainActivity（activity_main_lib 布局）+ LoginUtils 登录表单 | onCreate() 检测 getIntent().getBooleanExtra(FORCE_OPEN_PERMISSIONS) 为真，或 Companion.isPermissionsGiven() 为假，调用 LoginUtils.initLogin() | 原生Activity | **原文**：Login / Password / OK（strings.xml: login, pass, ok）；凭据由 Manifest meta-data EMAIL=kioxZ6swXB14xxplXF1JXIGr5zK0Igqf、PASSWORD=5rAJl+VWaf0YH2EIjOtwMQ== 提供<br>**译注**：登录 / 密码 / 确定——登录表单实际由内置凭据自动完成，用户无需也无法真正输入 | 无有效用户决策；登录成功后由 onLogin 回调自动推进，无可跳过入口 | `me.hawkshaw.HawkshawMainActivity.onCreate / me.hawkshaw.utils.LoginUtils.initLogin` |
| 2 | 引导说明页 | 原生 AlertDialog（HawkshawMainActivity.a(HawkshawMainActivity,int,int,Object)） | HawkshawMainActivity$onCreate$1.invoke(boolean z) 中 z 为真（登录成功）后调用 HawkshawMainActivity.a(this,0,1,null) | 原生Dialog | **原文**：Enable Accessibility Settings / Locate app AppleProtect and enable accessibility. / OK / Cancel<br>**译注**：启用无障碍设置 / 在设置中找到 AppleProtect 应用并开启无障碍。 / 确定 / 取消 | 要求点击 OK 前往系统无障碍设置；弹窗 setCancelable(false)，返回键与点击外部均不可关闭；虽提供 Cancel 按钮，但点击后仍落入重弹分支，实质无法跳过 | `me.hawkshaw.HawkshawMainActivity.a(...) + res/values/strings.xml#enable_accessibility_header/#enable_accessibility_message` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（已安装服务列表中显示 AppleProtect 项） | 弹窗 OK 按钮 HawkshawMainActivity$enableAccessibility$1.onClick 执行 startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), reqCode) | 系统无障碍页 | **原文**：Accessibility helps us to secure your device（res/xml/accessibility_service_config.xml android:description → strings.xml accessibility_service_description）<br>**译注**：无障碍功能帮助我们保护您的设备安全——即系统无障碍列表条目下方显示的说明 | 要求用户在系统无障碍服务列表中找到 AppleProtect 并把开关拨到开启（需确认系统「可读取屏幕全部内容」警告） | `me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick / res/xml/accessibility_service_config.xml` |
| 4 | 拒权反馈循环 | HawkshawMainActivity.onActivityResult(requestCode=0) 再次拉起同一 AlertDialog | 从系统设置返回（resultCode 任意，含 Cancel 回传的 0）触发 onActivityResult；b() 遍历 getEnabledAccessibilityServiceList(-1) 未匹配 "se.spitfire.appleprotect.it/me.hawkshaw.tasks.Accessibility" 时调用 a(this,0,1,null) | 原生Dialog | **原文**：Enable Accessibility Settings / Locate app AppleProtect and enable accessibility. / OK / Cancel（原样重弹）<br>**译注**：启用无障碍设置 / 在设置中找到 AppleProtect 应用并开启无障碍。——同一不可取消弹窗无限重现 | 无退出路径：只能点击 OK 回到系统设置继续开启，或点击 Cancel 后再次被同一弹窗拦回 | `me.hawkshaw.HawkshawMainActivity.onActivityResult (case 0) / me.hawkshaw.HawkshawMainActivity.b()` |
| 5 | 获权后动作 | me.hawkshaw.tasks.Accessibility.onServiceConnected() | 用户在系统设置开启服务后系统绑定无障碍服务，回调 onServiceConnected() | 系统无障碍页 | **原文**：无（代码行为：performGlobalAction(1) 即 GLOBAL_ACTION_BACK，随后 new Handler().postDelayed(..., 300L)）<br>**译注**：服务一连接即自动执行“返回”，把系统无障碍设置页退栈，掩盖授权过程并回落到引导链下一环 | 无需用户操作；界面被程序自动退栈 | `me.hawkshaw.tasks.Accessibility.onServiceConnected` |
| 6 | 获权后动作 | onActivityResult 递增链：电池优化白名单 → 屏幕录制 → 通知监听弹窗 → 设备管理器 → 小米 APP_PERM_EDITOR 自启动 → MANAGE_OVERLAY_PERMISSION → Additional Permissions 弹窗 → APPLICATION_DETAILS_SETTINGS | 无障碍已开启时 case 0 调用 a() 进入 case 1；此后每步成功后以 requestCode+1 递归 onActivityResult 推进，直到 default 分支写入 IS_PERMISSIONS_GIVEN=true 并 finish() | 系统无障碍页 | **原文**：Enable Read Notifications / Locate AppleProtect in settings and enable it.<br>Push notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings；Additional Permissions / Please take a look at settings and provide extra permissions if needed. 1. Enable AutoStart. 2. Allow display pop-up window from "Other Permissions". 3. Disable any battery saver for the app. 4. Disable Notifications.；Click on Activate button to secure your application.<br>**译注**：启用读取通知 / 在设置中找到 AppleProtect 并开启。推送通知能带来更好的体验并促进你的学习进度，你随时可在应用设置中更改；附加权限 / 请查看设置并按需提供额外权限：1. 开启自启动 2. 允许“其他权限”中显示弹窗 3. 关闭任何电池省电限制 4. 关闭通知；点击激活按钮以保护你的应用 | 逐项前往系统页开启通知监听、电池优化白名单、屏幕录制、设备管理器激活、自启动、悬浮窗，最后在应用详情页放开受限设置并关闭通知/省电；通知弹窗与附加权限弹窗均 setCancelable(false) | `me.hawkshaw.HawkshawMainActivity.onActivityResult (case 1–7) / me.hawkshaw.HawkshawMainActivity.a(int) / HawkshawMainActivity$openAppSettings$1` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- HawkshawMainActivity.a(HawkshawMainActivity,int,int,Object) 构造的不可取消原生 AlertDialog（标题 enable_accessibility_header、正文 enable_accessibility_message，均取自 res/values/strings.xml 第 66–67 行）
- 系统无障碍服务列表条目：res/xml/accessibility_service_config.xml android:description → strings.xml accessibility_service_description = 'Accessibility helps us to secure your device'；android:label 复用 @string/app_name = AppleProtect
- onActivityResult case 3 内联硬编码的通知监听弹窗（'Enable Read Notifications' + 学习进度话术）
- onActivityResult case 7 的 Additional Permissions 弹窗，正文 res/values/strings.xml#additional_permissions_text（含 1. Enable AutoStart. 2. Allow display pop-up window from "Other Permissions". 3. Disable any battery saver 4. Disable Notifications.）
- 设备管理器激活页说明 strings.xml#device_admin_explanation = 'Click on Activate button to secure your application.'
- 屏幕录制授权页前置提示 strings.xml#media_projection_message = "Please select **don't show again** ! ! !"
- 登录页表单 res/values/strings.xml#login/#pass/#ok（配合 Manifest meta-data 内置 EMAIL/PASSWORD）
- 无本地 HTML/WebView 引导页、无悬浮窗遮罩引导（DEX 中 TYPE_APPLICATION_OVERLAY 与 SYSTEM_ALERT_WINDOW 均无调用点）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable Accessibility Settings | 启用无障碍设置 | `res/values/strings.xml key=enable_accessibility_header（HawkshawMainActivity.a 弹窗标题）` | 假反诈安全 |
| en | Locate app %1$s and enable accessibility. | 在设置中找到应用 %1$s 并开启无障碍。 | `res/values/strings.xml key=enable_accessibility_message（%1$s 实参为 app_name=AppleProtect）` | 受限设置分步教学 |
| en | Accessibility helps us to secure your device | 无障碍功能帮助我们保护您的设备安全 | `res/values/strings.xml key=accessibility_service_description，经 res/xml/accessibility_service_config.xml android:description 呈现于系统无障碍列表` | 假反诈安全 |
| en | Please take a look at settings and provide extra permissions if needed.<br> 1. Enable AutoStart.<br> 2. Allow display pop-up window from "Other Permissions".<br> 3. Disable any battery saver for the app.<br> 4. Disable Notifications. | 请查看设置并按需提供额外权限。1. 开启自启动。2. 允许“其他权限”中显示弹窗。3. 关闭该应用的任何电池省电策略。4. 关闭通知。 | `res/values/strings.xml key=additional_permissions_text（onActivityResult case 7 弹窗正文）` | 受限设置分步教学 |
| en | Click on Activate button to secure your application. | 点击激活按钮以保护你的应用。 | `res/values/strings.xml key=device_admin_explanation（ADD_DEVICE_ADMIN 说明，onActivityResult case 4）` | 假反诈安全 |
| en | Locate AppleProtect in settings and enable it.<br>Push notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings | 在设置中找到 AppleProtect 并开启它。推送通知能带来更好的使用体验并促进你的学习进度，你随时可在应用设置中更改。 | `me.hawkshaw.HawkshawMainActivity.onActivityResult case 3 内联硬编码字符串（标题 'Enable Read Notifications'）` | 教唆忽视警告 |
| en | Please select **don't show again** ! ! ! | 请勾选“不再显示”！！！ | `res/values/strings.xml key=media_projection_message（屏幕录制授权前置提示）` | 教唆忽视警告 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onActivityResult(requestCode=0) 用 b() 检查 getEnabledAccessibilityServiceList(-1) 是否含 "包名/me.hawkshaw.tasks.Accessibility"；未开启则无条件再次调用 a(this,0,1,null) 重弹同一 setCancelable(false) 弹窗。Cancel 按钮（enableAccessibility$2）仅回传 resultCode=0，同样进入重弹分支，因此返回系统设置页或点取消都会被立即拦回，形成无出口循环；只有真正开启服务后 b() 为真才放行进入下一项权限。
- **遮罩叠层 / 高仿系统设置页**：无。全包未使用悬浮窗遮罩或高仿系统开关页：DEX 中 TYPE_APPLICATION_OVERLAY 与 SYSTEM_ALERT_WINDOW 无任何调用点，me.hawkshaw.ui.TransparentActivity 仅承载 media_projection 授权透传且内容为空白 TextView；引导完全依赖系统原生 AlertDialog 与真实系统设置页。
- **Android 13+ 受限设置（Restricted Settings）应对**：有。onActivityResult case 7 弹出不可取消的 'Additional Permissions' 弹窗，正文 additional_permissions_text 逐条要求用户到设置中 1. 开启自启动 2. 在「其他权限」中允许显示弹窗 3. 关闭该应用的电池省电策略 4. 关闭通知；OK 按钮（openAppSettings$1）跳 android.settings.APPLICATION_DETAILS_SETTINGS 打开应用详情页，正是 Android 13+ 放开受限设置所需路径（另 case 5 针对 Xiaomi 直接跳 com.miui.securitycenter PermissionsEditorActivity 做自启动/后台权限放行）。未使用 SESSION_INSTALLER 绕过。
- **获权后即时行为与防撤权机制**：有。me.hawkshaw.tasks.Accessibility.onServiceConnected() 在服务连接后立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）并 Handler.postDelayed(300ms) 执行后续动作，自动把用户刚操作的系统无障碍设置页退栈；预筛同时提示 WATCH_SETTINGS / WATCH_PKG_INSTALLER / PERFORM_GLOBAL_ACTION 等反移除特征，用于在用户尝试撤销时把界面顶回。
- **良性降级 / 替代方案**：无。不存在“仅浏览模式/手动模式/ADB 说明”等降级路径；未授权时唯一出口就是反复弹窗，且 default 分支才会写入 IS_PERMISSIONS_GIVEN=true 并 finish()。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测两类瞬间：(1) 应用 Activity 启动后 0.5–3s 内出现标题为 'Enable Accessibility Settings' 的原生 AlertDialog（这是登录成功后的第一道闸口，需在包名 se.spitfire.appleprotect.it 前台时即刻截图）；(2) 捕获到 startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS（以及 android.settings.APPLICATION_DETAILS_SETTINGS、android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、android.settings.action.MANAGE_OVERLAY_PERMISSION、android.app.action.ADD_DEVICE_ADMIN）时立即 UTG 取当前栈顶页面。最佳做法：先用 Hook 记录 onActivityResult 的 requestCode 序列，按 0→1→2→3→4→5→6→7 的推进节奏逐帧抓图。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：所有引导文案均为原生控件文本，UTG 可直接提取，无需 OCR。需注意两点非盲区但易漏的情况：(1) 引导在登录成功后才出现，若设备无网络导致 LoginUtils.initLogin 不回调，将看不到弹窗——应以 FORCE_OPEN_PERMISSIONS extra 或预置 IS_PERMISSIONS_GIVEN=false 重新拉起；(2) 获权后 onServiceConnected 会 300ms 内自动 GLOBAL_ACTION_BACK，抓图必须高帧率，否则会错过系统设置页。本样本非加壳、非加密载荷、无远端 HTML，静态加壳不构成阻挡。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **登录门槛页（引导前置条件）** | me.hawkshaw.HawkshawMainActivity 前台，布局 activity_main_lib，可见 'Login' / 'Password' / 'OK' 文本与进度条 | 证明无障碍引导不以任何真实业务功能为触发前提，而是登录成功即索取读屏权；同时暴露隐藏凭据机制 | Activity 类名 me.hawkshaw.HawkshawMainActivity；文本节点 Login / Password / OK；无任何功能列表或内容区 |
| **冷启动引导弹窗页（核心诱导页）** | 系统 AlertDialog，标题 'Enable Accessibility Settings'，正文含 'AppleProtect' 与 'enable accessibility'，按钮 OK / Cancel | 这是唯一的话术载体，且 setCancelable(false)——UTG 可直接证明无取消路径、返回键无效；同时证明文案极简、无技术必要性说明 | Dialog 标题/正文精确文本；无关闭按钮与外部点击不可关闭；弹窗出现时机 = 登录回调后 0–1s |
| **系统无障碍服务列表项（伪装身份呈现处）** | android.settings.ACCESSIBILITY_SETTINGS，列表项名称 'AppleProtect'，描述 'Accessibility helps us to secure your device' | 直接固定应用在系统授权页对用户呈现的伪装身份与'安全防护'话术，是身份错配的强证据 | 服务名 AppleProtect；描述 'Accessibility helps us to secure your device'；开关初始为关闭状态（说明用户被引导手动开启） |
| **设置页后自动退栈/拒权重弹页** | 从 ACCESSIBILITY_SETTINGS 返回后 300ms 内，栈顶回到 'Enable Accessibility Settings' 弹窗（若未开启）；若已开启则迅速切至电池优化/录屏/通知监听/设备管理器页 | 捕获同一弹窗的重复出现可证明拒权循环；捕获 onServiceConnected 后 300ms 的自动 BACK 可证明获权后掩盖痕迹 | 同一弹窗文本在 5s 内重复出现 ≥2 次；系统设置页在前台停留时长 < 1s 即被弹回；前台 Activity 由设置页切回 me.hawkshaw.HawkshawMainActivity |
| **Additional Permissions 受限设置教学页** | 不可取消 AlertDialog，标题 'Additional Permissions'，正文含 'Enable AutoStart' / 'Other Permissions' / 'Disable Notifications' | 证明应用主动教用户放开 Android 13+ 受限设置并关闭通知/省电，是教唆忽视系统管控的关键画面 | 弹窗精确四条清单文本；OK 后目标为 APPLICATION_DETAILS_SETTINGS 的应用详情页；无跳过按钮 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `me.hawkshaw.HawkshawMainActivity.onCreate`
- `me.hawkshaw.HawkshawMainActivity.a(me.hawkshaw.HawkshawMainActivity,int,int,java.lang.Object)`
- `me.hawkshaw.HawkshawMainActivity.onActivityResult`
- `me.hawkshaw.HawkshawMainActivity.b()`
- `me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick`
- `me.hawkshaw.tasks.Accessibility.onServiceConnected`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，静态可见性：clear）

**1. 引导入口不经过任何业务功能页，而是以登录作为前置门槛**
[HawkshawMainActivity.onCreate()](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity#onCreate>) 只在 `FORCE_OPEN_PERMISSIONS` 额外参数为真、或本地 `IS_PERMISSIONS_GIVEN` 未置位时进入 `LoginUtils.initLogin()`；登录表单为 `username/password`，而账号密码硬编码在 Manifest 元数据 `EMAIL`/`PASSWORD` 中（用户根本无从得知）。登录成功回调 [HawkshawMainActivity$onCreate$1#invoke](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity$onCreate$1#invoke>) 判定 `z` 为真后直接调用 `HawkshawMainActivity.a(this,0,1,null)` 弹出无障碍引导框——**没有功能页、没有说明页，登录一完成就索取读屏权**。

**2. 引导弹窗为原生 AlertDialog，`setCancelable(false)` 且文案极简**
[HawkshawMainActivity#a(...)](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity#void a(me.hawkshaw.HawkshawMainActivity, int, int, java.lang.Object)>) 使用 `setCancelable(false)`，标题 `Enable Accessibility Settings`，正文 `Locate app %1$s and enable accessibility.`（%1$s = `AppleProtect`），按钮 OK / Cancel。值得注意的是：如果检测到服务已开启（`b()`），它会**自动跳过弹窗、直接递归 `onActivityResult` 进入下一项权限**——即弹窗只是“未授权时”的必经闸口。

**3. OK 直接跳系统无障碍列表，无任何本地教学页 / WebView**
[HawkshawMainActivity$enableAccessibility$1#onClick](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity$enableAccessibility$1#onClick>) 仅一行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), reqCode)`。全包未使用本地 HTML/WebView 承载引导（assets 无引导页，`TYPE_APPLICATION_OVERLAY`/`SYSTEM_ALERT_WINDOW` 在 DEX 中**无任何调用点**）——因此**不存在悬浮遮罩叠层或高仿系统开关页**，这一点与预筛的 `A11Y_OVERLAY` 线索不符，实测为纯系统页跳转。

**4. 拒权反馈：Cancel 与返回都回到同一不可取消弹窗，构成死循环**
[HawkshawMainActivity#onActivityResult](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity#onActivityResult>) 的 `case 0` 用 [b()](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity#b>) 遍历 `getEnabledAccessibilityServiceList(-1)` 比对 `包名/me.hawkshaw.tasks.Accessibility`；未命中则再次 `a(this,0,1,null)` 重弹。Cancel 按钮（`enableAccessibility$2`）只是把 resultCode=0 回传，**同样落入重弹分支**——取消按钮实质无效。

**5. 获权后立刻“关门”：自点返回键**
[Accessibility#onServiceConnected()](<resource-unit:#1.dex1 code:me.hawkshaw.tasks.Accessibility#onServiceConnected>) 在 `this.a` 为真时立即 `performGlobalAction(1)`（GLOBAL_ACTION_BACK），并 `postDelayed(300ms)` 执行后续动作——用户在设置页刚点开开关，界面就被自动退栈，掩盖授权痕迹。

**6. 无障碍之后的“一揽子授权”长链**
同一 `onActivityResult` 以 requestCode 递增串行推进：`case 1` 电池优化白名单 → `case 2` 屏幕录制 `createScreenCaptureIntent` → `case 3` 通知监听（同样 `setCancelable(false)`，文案 “Enable Read Notifications … promote your learning progress”）→ `case 4` 设备管理器 `ADD_DEVICE_ADMIN`（“Click on Activate button to secure your application.”）→ `case 5` 小米 `APP_PERM_EDITOR` 自启动 → `case 6` `MANAGE_OVERLAY_PERMISSION` → `case 7` “Additional Permissions” 不可取消框，OK 跳 `android.settings.APPLICATION_DETAILS_SETTINGS`。

**7. 身份错配**
桌面名 `AppleProtect`、无障碍列表名同为 `AppleProtect`、说明 “Accessibility helps us to secure your device”，而工程内是 `se.joscarsson.privify`（Privify 照片保险箱）+ `me.hawkshaw`（远控框架）两套遗留命名；Manifest 同时声明 `READ_SMS/SEND_SMS/CALL_PHONE/RECORD_AUDIO/CAMERA/READ_CONTACTS` 等与“苹果设备保护”完全无关的权限，并内置 `CallRecorder`、`CameraRecorder`、`LocationMonitor`、`ScreenRecord` 等采集服务。无空白/同形字伪装，也未声明 `isAccessibilityTool`（targetSdk 21，该属性不存在）。

**8. 与既有风险的关系**
该链路已由项目风险 R-001（`malware_trojan` / high，autonomous_audit）完整登记，本次核验未发现需修订之处，故不重复写入。受限设置教学（`additional_permissions_text`）为 Android 13+ 应用详情页“允许受限设置”的分步教唆，属 R-001 证据范围。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（登录门槛→不可取消弹窗→跳 ACCESSIBILITY_SETTINGS→返回重弹→一揽子权限链→获权后 GLOBAL_ACTION_BACK）均在 DEX1 中完整静态可见；未加壳、无加密载荷、无远端 HTML/WebView 承载引导，引导文案全部来自 res/values/strings.xml 与硬编码字面量。未纳入本次核验的 me.hawkshaw.tasks.Accessibility.a(AccessibilityEvent) 具体窃取动作与远端 C2 指令解析不属于本轮 UTG 页面流转范围。",
  "summary_one_liner": "伪装成 AppleProtect 安全工具的应用在隐藏登录成功后立刻弹出 setCancelable(false) 的原生弹窗，一键跳系统无障碍列表并靠 onActivityResult 死循环重弹逼迫用户为 me.hawkshaw.tasks.Accessibility 开启读屏权，随后连环索取通知监听/电池白名单/录屏/设备管理器/悬浮窗/受限设置。",
  "disguise_identity": {
    "app_display_name": "AppleProtect",
    "claimed_brand_or_persona": "AppleProtect（暗示 Apple / 苹果设备安全防护工具，实际与 Apple Inc. 无任何关系）",
    "a11y_service_label": "AppleProtect",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:label 与 app_name 同为 AppleProtect、android:description 写作 'Accessibility helps us to secure your device'，将读屏权包装为安全防护；包内同时残留 se.joscarsson.privify（Privify 照片保险箱）与 me.hawkshaw（远控框架）两套工程命名，与宣称品牌不一致。未使用空白/换行挤出警告、同形字、多 activity-alias，也未伪造 isAccessibilityTool（targetSdkVersion=21，该 API 不存在）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "me.hawkshaw.HawkshawMainActivity（activity_main_lib 布局）+ LoginUtils 登录表单",
      "trigger_event": "onCreate() 检测 getIntent().getBooleanExtra(FORCE_OPEN_PERMISSIONS) 为真，或 Companion.isPermissionsGiven() 为假，调用 LoginUtils.initLogin()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Login / Password / OK（strings.xml: login, pass, ok）；凭据由 Manifest meta-data EMAIL=kioxZ6swXB14xxplXF1JXIGr5zK0Igqf、PASSWORD=5rAJl+VWaf0YH2EIjOtwMQ== 提供",
      "shown_text_zh": "登录 / 密码 / 确定——登录表单实际由内置凭据自动完成，用户无需也无法真正输入",
      "user_action_requested": "无有效用户决策；登录成功后由 onLogin 回调自动推进，无可跳过入口",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity.onCreate / me.hawkshaw.utils.LoginUtils.initLogin"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "原生 AlertDialog（HawkshawMainActivity.a(HawkshawMainActivity,int,int,Object)）",
      "trigger_event": "HawkshawMainActivity$onCreate$1.invoke(boolean z) 中 z 为真（登录成功）后调用 HawkshawMainActivity.a(this,0,1,null)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Accessibility Settings / Locate app AppleProtect and enable accessibility. / OK / Cancel",
      "shown_text_zh": "启用无障碍设置 / 在设置中找到 AppleProtect 应用并开启无障碍。 / 确定 / 取消",
      "user_action_requested": "要求点击 OK 前往系统无障碍设置；弹窗 setCancelable(false)，返回键与点击外部均不可关闭；虽提供 Cancel 按钮，但点击后仍落入重弹分支，实质无法跳过",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity.a(...) + res/values/strings.xml#enable_accessibility_header/#enable_accessibility_message"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（已安装服务列表中显示 AppleProtect 项）",
      "trigger_event": "弹窗 OK 按钮 HawkshawMainActivity$enableAccessibility$1.onClick 执行 startActivityForResult(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), reqCode)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility helps us to secure your device（res/xml/accessibility_service_config.xml android:description → strings.xml accessibility_service_description）",
      "shown_text_zh": "无障碍功能帮助我们保护您的设备安全——即系统无障碍列表条目下方显示的说明",
      "user_action_requested": "要求用户在系统无障碍服务列表中找到 AppleProtect 并把开关拨到开启（需确认系统「可读取屏幕全部内容」警告）",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick / res/xml/accessibility_service_config.xml"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "HawkshawMainActivity.onActivityResult(requestCode=0) 再次拉起同一 AlertDialog",
      "trigger_event": "从系统设置返回（resultCode 任意，含 Cancel 回传的 0）触发 onActivityResult；b() 遍历 getEnabledAccessibilityServiceList(-1) 未匹配 \"se.spitfire.appleprotect.it/me.hawkshaw.tasks.Accessibility\" 时调用 a(this,0,1,null)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Accessibility Settings / Locate app AppleProtect and enable accessibility. / OK / Cancel（原样重弹）",
      "shown_text_zh": "启用无障碍设置 / 在设置中找到 AppleProtect 应用并开启无障碍。——同一不可取消弹窗无限重现",
      "user_action_requested": "无退出路径：只能点击 OK 回到系统设置继续开启，或点击 Cancel 后再次被同一弹窗拦回",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity.onActivityResult (case 0) / me.hawkshaw.HawkshawMainActivity.b()"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "me.hawkshaw.tasks.Accessibility.onServiceConnected()",
      "trigger_event": "用户在系统设置开启服务后系统绑定无障碍服务，回调 onServiceConnected()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（代码行为：performGlobalAction(1) 即 GLOBAL_ACTION_BACK，随后 new Handler().postDelayed(..., 300L)）",
      "shown_text_zh": "服务一连接即自动执行“返回”，把系统无障碍设置页退栈，掩盖授权过程并回落到引导链下一环",
      "user_action_requested": "无需用户操作；界面被程序自动退栈",
      "code_anchor": "me.hawkshaw.tasks.Accessibility.onServiceConnected"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "onActivityResult 递增链：电池优化白名单 → 屏幕录制 → 通知监听弹窗 → 设备管理器 → 小米 APP_PERM_EDITOR 自启动 → MANAGE_OVERLAY_PERMISSION → Additional Permissions 弹窗 → APPLICATION_DETAILS_SETTINGS",
      "trigger_event": "无障碍已开启时 case 0 调用 a() 进入 case 1；此后每步成功后以 requestCode+1 递归 onActivityResult 推进，直到 default 分支写入 IS_PERMISSIONS_GIVEN=true 并 finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable Read Notifications / Locate AppleProtect in settings and enable it.\nPush notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings；Additional Permissions / Please take a look at settings and provide extra permissions if needed. 1. Enable AutoStart. 2. Allow display pop-up window from \"Other Permissions\". 3. Disable any battery saver for the app. 4. Disable Notifications.；Click on Activate button to secure your application.",
      "shown_text_zh": "启用读取通知 / 在设置中找到 AppleProtect 并开启。推送通知能带来更好的体验并促进你的学习进度，你随时可在应用设置中更改；附加权限 / 请查看设置并按需提供额外权限：1. 开启自启动 2. 允许“其他权限”中显示弹窗 3. 关闭任何电池省电限制 4. 关闭通知；点击激活按钮以保护你的应用",
      "user_action_requested": "逐项前往系统页开启通知监听、电池优化白名单、屏幕录制、设备管理器激活、自启动、悬浮窗，最后在应用详情页放开受限设置并关闭通知/省电；通知弹窗与附加权限弹窗均 setCancelable(false)",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity.onActivityResult (case 1–7) / me.hawkshaw.HawkshawMainActivity.a(int) / HawkshawMainActivity$openAppSettings$1"
    }
  ],
  "text_presentation_locations": [
    "HawkshawMainActivity.a(HawkshawMainActivity,int,int,Object) 构造的不可取消原生 AlertDialog（标题 enable_accessibility_header、正文 enable_accessibility_message，均取自 res/values/strings.xml 第 66–67 行）",
    "系统无障碍服务列表条目：res/xml/accessibility_service_config.xml android:description → strings.xml accessibility_service_description = 'Accessibility helps us to secure your device'；android:label 复用 @string/app_name = AppleProtect",
    "onActivityResult case 3 内联硬编码的通知监听弹窗（'Enable Read Notifications' + 学习进度话术）",
    "onActivityResult case 7 的 Additional Permissions 弹窗，正文 res/values/strings.xml#additional_permissions_text（含 1. Enable AutoStart. 2. Allow display pop-up window from \"Other Permissions\". 3. Disable any battery saver 4. Disable Notifications.）",
    "设备管理器激活页说明 strings.xml#device_admin_explanation = 'Click on Activate button to secure your application.'",
    "屏幕录制授权页前置提示 strings.xml#media_projection_message = \"Please select **don't show again** ! ! !\"",
    "登录页表单 res/values/strings.xml#login/#pass/#ok（配合 Manifest meta-data 内置 EMAIL/PASSWORD）",
    "无本地 HTML/WebView 引导页、无悬浮窗遮罩引导（DEX 中 TYPE_APPLICATION_OVERLAY 与 SYSTEM_ALERT_WINDOW 均无调用点）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Settings",
      "text_zh": "启用无障碍设置",
      "source_location": "res/values/strings.xml key=enable_accessibility_header（HawkshawMainActivity.a 弹窗标题）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate app %1$s and enable accessibility.",
      "text_zh": "在设置中找到应用 %1$s 并开启无障碍。",
      "source_location": "res/values/strings.xml key=enable_accessibility_message（%1$s 实参为 app_name=AppleProtect）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility helps us to secure your device",
      "text_zh": "无障碍功能帮助我们保护您的设备安全",
      "source_location": "res/values/strings.xml key=accessibility_service_description，经 res/xml/accessibility_service_config.xml android:description 呈现于系统无障碍列表",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Please take a look at settings and provide extra permissions if needed.\n 1. Enable AutoStart.\n 2. Allow display pop-up window from \"Other Permissions\".\n 3. Disable any battery saver for the app.\n 4. Disable Notifications.",
      "text_zh": "请查看设置并按需提供额外权限。1. 开启自启动。2. 允许“其他权限”中显示弹窗。3. 关闭该应用的任何电池省电策略。4. 关闭通知。",
      "source_location": "res/values/strings.xml key=additional_permissions_text（onActivityResult case 7 弹窗正文）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on Activate button to secure your application.",
      "text_zh": "点击激活按钮以保护你的应用。",
      "source_location": "res/values/strings.xml key=device_admin_explanation（ADD_DEVICE_ADMIN 说明，onActivityResult case 4）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate AppleProtect in settings and enable it.\nPush notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings",
      "text_zh": "在设置中找到 AppleProtect 并开启它。推送通知能带来更好的使用体验并促进你的学习进度，你随时可在应用设置中更改。",
      "source_location": "me.hawkshaw.HawkshawMainActivity.onActivityResult case 3 内联硬编码字符串（标题 'Enable Read Notifications'）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Please select **don't show again** ! ! !",
      "text_zh": "请勾选“不再显示”！！！",
      "source_location": "res/values/strings.xml key=media_projection_message（屏幕录制授权前置提示）",
      "rhetorical_frame": "教唆忽视警告"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onActivityResult(requestCode=0) 用 b() 检查 getEnabledAccessibilityServiceList(-1) 是否含 \"包名/me.hawkshaw.tasks.Accessibility\"；未开启则无条件再次调用 a(this,0,1,null) 重弹同一 setCancelable(false) 弹窗。Cancel 按钮（enableAccessibility$2）仅回传 resultCode=0，同样进入重弹分支，因此返回系统设置页或点取消都会被立即拦回，形成无出口循环；只有真正开启服务后 b() 为真才放行进入下一项权限。",
    "overlay_or_fake_settings": "无。全包未使用悬浮窗遮罩或高仿系统开关页：DEX 中 TYPE_APPLICATION_OVERLAY 与 SYSTEM_ALERT_WINDOW 无任何调用点，me.hawkshaw.ui.TransparentActivity 仅承载 media_projection 授权透传且内容为空白 TextView；引导完全依赖系统原生 AlertDialog 与真实系统设置页。",
    "restricted_settings_13plus_coaching": "有。onActivityResult case 7 弹出不可取消的 'Additional Permissions' 弹窗，正文 additional_permissions_text 逐条要求用户到设置中 1. 开启自启动 2. 在「其他权限」中允许显示弹窗 3. 关闭该应用的电池省电策略 4. 关闭通知；OK 按钮（openAppSettings$1）跳 android.settings.APPLICATION_DETAILS_SETTINGS 打开应用详情页，正是 Android 13+ 放开受限设置所需路径（另 case 5 针对 Xiaomi 直接跳 com.miui.securitycenter PermissionsEditorActivity 做自启动/后台权限放行）。未使用 SESSION_INSTALLER 绕过。",
    "post_grant_anti_removal": "有。me.hawkshaw.tasks.Accessibility.onServiceConnected() 在服务连接后立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）并 Handler.postDelayed(300ms) 执行后续动作，自动把用户刚操作的系统无障碍设置页退栈；预筛同时提示 WATCH_SETTINGS / WATCH_PKG_INSTALLER / PERFORM_GLOBAL_ACTION 等反移除特征，用于在用户尝试撤销时把界面顶回。",
    "benign_graceful_degradation": "无。不存在“仅浏览模式/手动模式/ADB 说明”等降级路径；未授权时唯一出口就是反复弹窗，且 default 分支才会写入 IS_PERMISSIONS_GIVEN=true 并 finish()。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测两类瞬间：(1) 应用 Activity 启动后 0.5–3s 内出现标题为 'Enable Accessibility Settings' 的原生 AlertDialog（这是登录成功后的第一道闸口，需在包名 se.spitfire.appleprotect.it 前台时即刻截图）；(2) 捕获到 startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS（以及 android.settings.APPLICATION_DETAILS_SETTINGS、android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、android.settings.action.MANAGE_OVERLAY_PERMISSION、android.app.action.ADD_DEVICE_ADMIN）时立即 UTG 取当前栈顶页面。最佳做法：先用 Hook 记录 onActivityResult 的 requestCode 序列，按 0→1→2→3→4→5→6→7 的推进节奏逐帧抓图。",
    "key_pages_to_capture": [
      {
        "page_role": "登录门槛页（引导前置条件）",
        "page_identifier": "me.hawkshaw.HawkshawMainActivity 前台，布局 activity_main_lib，可见 'Login' / 'Password' / 'OK' 文本与进度条",
        "why_most_useful": "证明无障碍引导不以任何真实业务功能为触发前提，而是登录成功即索取读屏权；同时暴露隐藏凭据机制",
        "observable_utg_signals": ["Activity 类名 me.hawkshaw.HawkshawMainActivity", "文本节点 Login / Password / OK", "无任何功能列表或内容区"]
      },
      {
        "page_role": "冷启动引导弹窗页（核心诱导页）",
        "page_identifier": "系统 AlertDialog，标题 'Enable Accessibility Settings'，正文含 'AppleProtect' 与 'enable accessibility'，按钮 OK / Cancel",
        "why_most_useful": "这是唯一的话术载体，且 setCancelable(false)——UTG 可直接证明无取消路径、返回键无效；同时证明文案极简、无技术必要性说明",
        "observable_utg_signals": ["Dialog 标题/正文精确文本", "无关闭按钮与外部点击不可关闭", "弹窗出现时机 = 登录回调后 0–1s"]
      },
      {
        "page_role": "系统无障碍服务列表项（伪装身份呈现处）",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS，列表项名称 'AppleProtect'，描述 'Accessibility helps us to secure your device'",
        "why_most_useful": "直接固定应用在系统授权页对用户呈现的伪装身份与'安全防护'话术，是身份错配的强证据",
        "observable_utg_signals": ["服务名 AppleProtect", "描述 'Accessibility helps us to secure your device'", "开关初始为关闭状态（说明用户被引导手动开启）"]
      },
      {
        "page_role": "设置页后自动退栈/拒权重弹页",
        "page_identifier": "从 ACCESSIBILITY_SETTINGS 返回后 300ms 内，栈顶回到 'Enable Accessibility Settings' 弹窗（若未开启）；若已开启则迅速切至电池优化/录屏/通知监听/设备管理器页",
        "why_most_useful": "捕获同一弹窗的重复出现可证明拒权循环；捕获 onServiceConnected 后 300ms 的自动 BACK 可证明获权后掩盖痕迹",
        "observable_utg_signals": ["同一弹窗文本在 5s 内重复出现 ≥2 次", "系统设置页在前台停留时长 < 1s 即被弹回", "前台 Activity 由设置页切回 me.hawkshaw.HawkshawMainActivity"]
      },
      {
        "page_role": "Additional Permissions 受限设置教学页",
        "page_identifier": "不可取消 AlertDialog，标题 'Additional Permissions'，正文含 'Enable AutoStart' / 'Other Permissions' / 'Disable Notifications'",
        "why_most_useful": "证明应用主动教用户放开 Android 13+ 受限设置并关闭通知/省电，是教唆忽视系统管控的关键画面",
        "observable_utg_signals": ["弹窗精确四条清单文本", "OK 后目标为 APPLICATION_DETAILS_SETTINGS 的应用详情页", "无跳过按钮"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：所有引导文案均为原生控件文本，UTG 可直接提取，无需 OCR。需注意两点非盲区但易漏的情况：(1) 引导在登录成功后才出现，若设备无网络导致 LoginUtils.initLogin 不回调，将看不到弹窗——应以 FORCE_OPEN_PERMISSIONS extra 或预置 IS_PERMISSIONS_GIVEN=false 重新拉起；(2) 获权后 onServiceConnected 会 300ms 内自动 GLOBAL_ACTION_BACK，抓图必须高帧率，否则会错过系统设置页。本样本非加壳、非加密载荷、无远端 HTML，静态加壳不构成阻挡。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "me.hawkshaw.HawkshawMainActivity.onCreate",
    "me.hawkshaw.HawkshawMainActivity.a(me.hawkshaw.HawkshawMainActivity,int,int,java.lang.Object)",
    "me.hawkshaw.HawkshawMainActivity.onActivityResult",
    "me.hawkshaw.HawkshawMainActivity.b()",
    "me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick",
    "me.hawkshaw.tasks.Accessibility.onServiceConnected"
  ]
}
```

</details>
