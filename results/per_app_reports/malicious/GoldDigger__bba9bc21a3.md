# MB_004__bba9bc21a3｜GoldDigger — PLN Mobile

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：188.0s

## 1. 一句话核心结论

- **核心申请方式**：冒用 PLN Mobile 身份、把无障碍服务声明为 isAccessibilityTool=true，并以专用 CheckPermissionActivity 原生开关清单（含 tvFz 辅助功能行）配合 native 解密的加密引导文案，将用户逐步引导至系统无障碍设置页开启 FocusService 全量窗口能力。
- **静态可见性说明**：DEX 未加壳，Manifest/无障碍配置/布局/服务声明完全可见；但 CheckPermissionActivity.initView/onResume/onBackPressed 为 native 实现，且全部引导文案以 .Lt9 密文存于 strings.xml（go_to_accessibility_setting、open_access_tip、permission_setting、app_jc_zb_title_1..15 等），由 libcccc.so 的 Dec.d 在运行期解密后渲染；无障碍设置页跳转 action 字面量在 DEX 中无命中，亦由 native 侧拼装，故逐字文案与确切 Intent 字符串不可静态还原。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `bba9bc21a322ea0e1737c5fa64057d12f133a3ebed6007ffed979b3d6099f6aa` |
| 包名 / 年份 | `com.aa.bb` / 2026 |
| 家族 / 品类 | **GoldDigger**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | PLN Mobile |
| 引导页宣称品牌/身份 | PLN Mobile（印尼国家电力公司 PLN 官方 App） |
| 系统无障碍列表服务名 | PLN Mobile |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签与 android:description 均只写品牌名 'PLN Mobile'，无任何功能说明；无障碍配置显式伪造 android:isAccessibilityTool="true"；包名 com.aa.bb 与类路径 hvghfdur.hfbuhgpg.ubjmglfd 完全无意义（随机化）；引导文案全部为 [.Lt9] 密文并置于自定义 .so 解密；DEX 中存在 asd.kkalive/kkdaemon/asd.fgh 多套 instrumentation 与多进程守护组件用于反移除 |
| 无障碍服务类名 | `hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | PLN Mobile |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | hvghfdur.hfbuhgpg.ubjmglfd.ui.SplashActivity（LAUNCHER） | 用户点击桌面图标，onCreate/onResume 进入启动页 | 原生Activity | **原文**：PLN Mobile<br>**译注**：启动页显示 PLN Mobile 品牌名与图标 ic_logo | 无，自动跳转下一页面 | `hvghfdur.hfbuhgpg.ubjmglfd.ui.SplashActivity` |
| 2 | 业务功能触发 | hvghfdur.hfbuhgpg.ubjmglfd.ui.RegisterFirst2Activity / LoginActivity / ActivationActivity | 启动页跳转；RegisterFirst2Activity 构造时即调用 ᡚ.㪖.isAccessibilityOpened() 判定无障碍状态 | 原生Activity | **原文**：不可静态还原（文案为 [.Lt9] 密文）<br>**译注**：登录/激活/注册流程，以 PLN Mobile 身份要求用户登录；注册页在构造阶段即检查无障碍是否已开启 | 输入账号密码并登录（存在登录、查询密码、安全密码等页面），无跳过入口 | `ngodanao.fdsnofdno.fdsfnso.RegisterFirst2Activity.㯺 → ᡚ.㪖.isAccessibilityOpened` |
| 3 | 引导说明页 | hvghfdur.hfbuhgpg.ubjmglfd.ui.CheckPermissionActivity（路由 /app/check/permission，可由 GlobalBroadcast.ACTION_SHOW_CHECK_PERMISSION_ACTIVITY 广播拉起） | 登录后跳转，或收到 ACTION_SHOW_CHECK_PERMISSION_ACTIVITY 广播；onCreate→initView()（native）渲染开关清单 | 原生Activity | **原文**：tvFz: @string/app_jc_zb_title_1 = "6HZFPYMWV6bQ8JG7J1EHo/m+UoTDBRUHvteEOpNN8EH8tysoLzFhwDq2uvcJSdydfD7M1OQcX8DNW0XK1uqKk0lPCXVfkuInRAcNhZMvHW4=[.Lt9]"；按钮 tvFzOpen: @string/app_jc_zb_open_title = "+1VqA+q2iQsGG4YD0b5ZIQ==[.Lt9]"；标题 @string/app_jc_zb_title<br>**译注**：原生“权限开启”清单页：第一行为辅助功能（tvFz/ivFz/app_open_selector 勾选状态图标 + tvFzOpen「打开」按钮），其下依次为录屏（tvVideo）、悬浮窗（tvXf，默认 visibility=gone）、短信（tvMsg，默认 gone）等行；标题与按钮文字为运行期解密文本 | 点击各行的「打开」按钮逐项开启；页面无取消/跳过控件，onBackPressed 由 native 接管 | `res/layout/activity_check_permission.xml + hvghfdur.hfbuhgpg.ubjmglfd.ui.CheckPermissionActivity#initView（native）` |
| 4 | 跳无障碍设置 | 系统设置无障碍服务列表（或 com.android.settings.InstalledAppDetails 应用详情页） | 点击 tvFzOpen「打开」按钮 → native 实现中构造 Intent 跳转（DEX 内无 ACTION_ACCESSIBILITY_SETTINGS 字面量，action 由 libcccc.so 解密拼装） | 系统无障碍页 | **原文**：PLN Mobile（服务名）；android:description = "PLN Mobile"<br>**译注**：跳入系统无障碍设置，服务列表中该项仅显示「PLN Mobile」，描述同样仅为「PLN Mobile」，无功能说明；并因 isAccessibilityTool=true 被系统当作无障碍工具呈现 | 用户需在系统列表中找到「PLN Mobile」并手动打开开关 | `res/xml/touch_accessibility_service_config.xml + hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService（BIND_ACCESSIBILITY_SERVICE）` |
| 5 | 拒权反馈循环 | 返回 CheckPermissionActivity 后 onResume → native 逻辑 checkResultWhenResume / isResumedCheck 复查；配合 com.bw.dialog.TipsDialog / TopDialog 弹窗 | 用户从系统设置返回（onResume）；若 FocusService 单例未连接则 isAccessibilityOpened() 仍为 false，停留在本页并可再次点击「打开」 | 原生Activity + 原生Dialog | **原文**：permission_form_deny_prompt: "1.取得权限失败，无法执行操作。<br><br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。"<br>**译注**：「1.取得权限失败，无法执行操作。2.若因先前拒绝了权限授予，而没有出现权限请求画面，请至『设置→应用程序→当前App→权限』，将「%s」勾选允许。」——以“操作失败”话术把责任推给用户，并给出进入应用设置页手动勾选的分步教学 | 按提示再次进入系统设置手动勾选/开启；页面不提供降级或跳过路径 | `res/values/strings.xml#permission_form_deny_prompt + libcccc.so 字符串 CheckPermissionActivity>>checkResultWhenResume>>>isResumedCheck>>> + com.bw.dialog.TipsDialog` |
| 6 | 遮罩叠层指引 | com.lzf.easyfloat FloatWindow / hvghfdur.hfbuhgpg.ubjmglfd.service.floatwindow.FocusFloatWindow / ViewVideoMaskFloatWindowBinding（FocusService.showMask / newMaskFloat） | 悬浮窗权限就绪后（ᡚ.㪖.isHaveFloatWindow → com.lzf.easyfloat.permission），在引导/设置页之上叠加悬浮遮罩 | 悬浮窗Overlay | **原文**：float_window_permission_tip = "C8FDtx2vtkz5+NKVRjX8AM9UlS4wr++PAWLxsrFC0uJRNvCZEWJPgyAtF9HxVhyd[.Lt9]"；open_float_tip = "haa1444CvLaI2DvN+FI9uKsrrPYm8ZlEaUrCWmrIQ1Y=[.Lt9]"<br>**译注**：悬浮窗权限与引导提示（密文，运行期解密）；遮罩窗口用于在目标页面之上覆盖显示或黑屏替换 | 按遮罩提示继续操作（可静态确认的是悬浮窗实现与遮罩窗口体系存在） | `hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService#showMask / #newMaskFloat / res/values/strings.xml#float_window_permission_tip` |
| 7 | 获权后动作 | hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService（onServiceConnected 后全量窗口监听） | 用户在系统设置中开启「PLN Mobile」无障碍开关 → onServiceConnected → isAccessibilityOn=true | 不可静态还原 | 无 | 无（后台静默执行） | `hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService#onServiceConnected / #traverseNode / #sendCurrentPage / #autoClickConfirm / #toDisableSelf` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务标签 @string/app_name_input = "PLN Mobile"（AndroidManifest 中 FocusService 的 android:label）
- 系统无障碍服务描述：@string/accessibility_service_description = "PLN Mobile"（res/values/strings.xml 第 30 行，由 touch_accessibility_service_config.xml 的 android:description 引用）
- CheckPermissionActivity 原生开关清单页：res/layout/activity_check_permission.xml 的 tvFz（app_jc_zb_title_1）、tvFzOpen/tvVideoOpen（app_jc_zb_open_title「打开」）、tvVideo、tvXf、tvMsg 各行，文案均为 [.Lt9] 密文运行期解密
- 引导/说明密文资源集中存放于 res/values/strings.xml：go_to_accessibility_setting、open_access_tip、permission_setting、open_float_tip、float_window_permission_tip、app_opened、app_to_open、app_jc_zb_title_1..15
- 拒权提示弹窗（TipsDialog/TopDialog 或 Activity 内 TextView）：permission_form_deny_prompt / permission_form_deny_prompt2 明文，教用户进『设置→应用→当前App→权限』勾选
- 悬浮窗叠层：FocusFloatWindow / FloatWindow（com.lzf.easyfloat）+ ViewVideoMaskFloatWindowBinding，用于在设置页或目标页之上叠加提示/遮罩
- 应用桌面与通知栏标识：@string/app_name = "PLN Mobile"、mipmap/ic_logo
- 未发现 assets/ 目录与本地 HTML 引导页；引导均以原生页面 + 密文文本 + 悬浮窗承载

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | PLN Mobile | PLN Mobile（印尼国家电力公司品牌名，同时作为应用名、无障碍服务名与服务描述） | `res/values/strings.xml → app_name_input / app_name / accessibility_service_description` | 未知 |
| zh | 1.取得权限失败，无法执行操作。<br><br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。 | 1.取得权限失败，无法执行操作。2.若因先前拒绝了权限授予，而没有出现权限请求画面，请至『设置→应用程序→当前App→权限』，将「%s」勾选允许。 | `res/values/strings.xml → permission_form_deny_prompt` | 受限设置分步教学 |
| zh | 1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。 | 同上简体版本：以“操作失败”为前提，指导用户进入应用详情页手动勾选被拒权限。 | `res/values/strings.xml → permission_form_deny_prompt2` | 受限设置分步教学 |
| zh | 获取权限失败，继续保存图片 | 获取权限失败，继续保存图片（权限失败仍继续动作，弱化权限缺失的严重性） | `res/values/strings.xml → permission_failed_and_save_image` | 故障恐吓 |
| zh | 获取系统录音权限被拒绝 / 获取系统相机权限被拒绝 | 获取系统录音权限被拒绝 / 获取系统相机权限被拒绝 | `res/values/strings.xml → selector_audio_permission_ungranted / selector_camera_permission_ungranted` | 故障恐吓 |
| zh | 3zlhHYHKi2QQi1tWNI1PeFODxrbtK6/5hDSWWV0bFOImnLoYQ0qJRazow+mzJTBs[.Lt9] | 密文，运行期由 libcccc.so 解密；键名 go_to_accessibility_setting 表明其为“前往无障碍设置”的按钮/提示文案（明文逐字不可静态还原） | `res/values/strings.xml → go_to_accessibility_setting` | 未知 |
| zh | 6HZFPYMWV6bQ8JG7J1EHo/m+UoTDBRUHvteEOpNN8EH8tysoLzFhwDq2uvcJSdydfD7M1OQcX8DNW0XK1uqKk0lPCXVfkuInRAcNhZMvHW4=[.Lt9] | 密文，CheckPermissionActivity 第一行（辅助功能项）的标题文案，运行期解密（明文逐字不可静态还原） | `res/values/strings.xml → app_jc_zb_title_1（被 activity_check_permission.xml 的 tvFz 引用）` | 未知 |
| zh | +1VqA+q2iQsGG4YD0b5ZIQ==[.Lt9] | 密文，各权限行的「打开」按钮文字（app_jc_zb_open_title / app_jc_zb_title_4 / app_jc_zb_title_5 共用同一密文） | `res/values/strings.xml → app_jc_zb_open_title` | 未知 |
| zh | C8FDtx2vtkz5+NKVRjX8AM9UlS4wr++PAWLxsrFC0uJRNvCZEWJPgyAtF9HxVhyd[.Lt9] | 密文，悬浮窗权限提示文案（float_window_permission_tip），运行期解密 | `res/values/strings.xml → float_window_permission_tip` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：从系统设置返回后 CheckPermissionActivity.onResume 触发 native 复查（libcccc.so 中可见字符串 CheckPermissionActivity>>checkResultWhenResume>>>isResumedCheck>>>），若 FocusService 单例未连接则 isAccessibilityOpened()（= isHaveAccessibility() || isHaveAccessibilityPluginPackage）仍为 false，页面停留在原生开关清单并允许无限次再次点击「打开」重跳设置；onBackPressed 亦为 native 接管，存在阻断返回的判定空间。是否含定时器强制重跳未取得直接证据。
- **遮罩叠层 / 高仿系统设置页**：不伪造系统设置页；但在跳转/引导期间使用 com.lzf.easyfloat 的 FloatWindow/FocusFloatWindow 与 ViewVideoMaskFloatWindowBinding（FocusService.showMask/newMaskFloat/hideOtherMask、maskWindows、maskFloatWindowPath）叠放悬浮窗/遮罩层，可在设置页之上提供悬浮指引或后续黑屏替换。
- **Android 13+ 受限设置（Restricted Settings）应对**：明文存在同类分步教学话术：permission_form_deny_prompt / permission_form_deny_prompt2 指导用户进入『设置→应用程序→当前App→权限』手动勾选「%s」；libcccc.so 同时含 android.settings.APPLICATION_DETAILS_SETTINGS、com.android.settings.InstalledAppDetails、getAppDetailSettingIntent，具备跳应用详情页（受限设置入口）的实现。未发现 Session 安装器绕过逻辑。
- **获权后即时行为与防撤权机制**：存在撤权对抗组件：FocusService.toDisableSelf、onInterrupt、checkMainService/onDisconnectedRunnable，以及 Manifest 中 asd.kkalive.Keep111Instrumentation、asd.kkdaemon.RunInstrumentation 多进程守护（:resident/:daemon/:assist1-3）与 com.aa.bb.matrix.permission.PROCESS_SUPERVISOR；DEX 预筛亦命中 PERFORM_GLOBAL_ACTION（可用于监听设置页后按 BACK/HOME 阻止撤权）。具体 GLOBAL_ACTION 使用点未在本轮逐条取证。
- **良性降级 / 替代方案**：无。页面无跳过/取消控件，未开启即无法进入后续业务；不提供手动模式或替代路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到应用进程发出跳转 ACTION_ACCESSIBILITY_SETTINGS（或异常以 APPLICATION_DETAILS_SETTINGS + InstalledAppDetails 形式跳应用详情页）的瞬间拉起 UTG；次优时机为 CheckPermissionActivity 首次 onResume 呈现开关清单时（该页 onResume 为 native 实现，建议 Hook Activity.onResume 按类名过滤）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：全部核心引导文案以 [.Lt9] 密文存于 strings.xml 并由 libcccc.so 在运行期解密，CheckPermissionActivity.initView/onResume/onBackPressed 亦为 native 实现，静态侧只能读到键名与密文，无法获得逐字原文与跳转 action 字面量；同时 DEX 中存在 asd.kkalive/asd.kkdaemon 多进程守护与 toDisableSelf 自禁用逻辑，运行期可能干扰 UTG 采集稳定性。应用本身未加壳，运行期 UTG 不受影响，但若仅在纯静态阶段评估会严重低估诱导话术。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/登录后的引导开关清单页** | hvghfdur.hfbuhgpg.ubjmglfd.ui.CheckPermissionActivity，layout 含 id tvFz/tvFzOpen/tvVideo/tvXf/tvMsg、ImageView ivFz 背景 app_open_selector | 这是全部诱导的策源地：可直接证明应用在正常业务流中强制要求开启辅助功能，且无跳过入口 | 控件 id 组合 tvFz + tvFzOpen + app_open_selector 背景；页面标题与按钮文本为运行期解密后文字（非资源表可见文本）；无任何 skip/cancel/close 控件；首行为辅助功能、其下为录屏/悬浮窗/短信，形成递进索取 |
| **跳转前的说明/弹窗层** | com.bw.dialog.TipsDialog 或 com.bw.dialog.TopDialog 弹窗（自定义 View，非系统 AlertDialog），可能叠加 FocusFloatWindow 悬浮层 | 解密后的诱导话术在此首次以可读形式出现，是判断话术性质（假更新/故障恐吓/安全恐吓）的关键取证点 | 自定义 Dialog 类名不在 android.app.AlertDialog 体系；弹窗按钮仅有确认/「打开」，无取消；文本内容与 strings.xml 中 [.Lt9] 密文键位对应（可回指 go_to_accessibility_setting / open_access_tip / app_jc_zb_title_*） |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中的 "PLN Mobile" 条目，subtitle/description 同为 "PLN Mobile" | 证明身份伪装落地：用户在系统层面看到的是银行/电力品牌而非功能说明，且 isAccessibilityTool=true 使其被归类为无障碍工具 | 服务名与描述完全相同的品牌名、无功能描述；同页可见应用包名 com.aa.bb 与品牌不符；开关被打开后立即返回应用即恢复业务流 |
| **设置页返回后的复查/再引导页** | CheckPermissionActivity 再次 onResume 或 TipsDialog 二次弹出；可能伴 FocusFloatWindow 遮罩 | 用于判定拒权闭环：是否死循环重跳、是否以“操作失败”话术施压 | 返回应用后立刻重复出现同一开关清单或弹窗；出现 permission_form_deny_prompt 的“取得权限失败，无法执行操作”文案；页面层级中出现悬浮窗（TYPE_APPLICATION_OVERLAY）窗口 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `hvghfdur.hfbuhgpg.ubjmglfd.ui.CheckPermissionActivity#initView / #onResume / #onBackPressed（native，实现于 libcccc.so）`
- `hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService#onServiceConnected / #showMask / #toDisableSelf`
- `ᡚ.㪖#isAccessibilityOpened / #isHaveAccessibility`
- `res/layout/activity_check_permission.xml（tvFz / tvFzOpen / tvVideo / tvXf / tvMsg）`
- `res/xml/touch_accessibility_service_config.xml（isAccessibilityTool=true, typeAllMask, canPerformGestures）`
- `res/values/strings.xml（accessibility_service_description=PLN Mobile；go_to_accessibility_setting、app_jc_zb_title_1、app_jc_zb_open_title 等 .Lt9 密文）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，含效率约束说明）

> 说明：本轮实际调用已超预算（约 23 次），以下结论基于已取得的静态证据直接收口，不再继续探索。

**1. 伪装身份：完全冒用 PLN（印尼国家电力公司）品牌**
- 桌面名与无障碍服务标签、服务描述全部为 `PLN Mobile`：`@string/app_name_input`、`@string/accessibility_service_description`（值为 `PLN Mobile`）。系统无障碍列表中看到的只有“PLN Mobile”，没有任何功能性说明。
- 无障碍配置 [touch_accessibility_service_config.xml](<resource-unit:#1 file:res/xml/touch_accessibility_service_config.xml>) 显式声明 `android:isAccessibilityTool="true"`，主动伪装成“无障碍工具”以降低系统/用户警惕；同时申请 `typeAllMask`、`canRetrieveWindowContent`、`canPerformGestures`、`flagRetrieveInteractiveWindows` 的全量窗口能力。

**2. 引导流程：专用“权限检查”页 + 逐项开关 + 跳系统设置**
- 入口 [SplashActivity](<resource-unit:#1 manifest:components>) → 登录/激活链路（`RegisterFirst2Activity`、`LoginActivity`、`ActivationActivity`）→ [CheckPermissionActivity](<resource-unit:#1.dex1 code:hvghfdur.hfbuhgpg.ubjmglfd.ui.CheckPermissionActivity>)（路由 `/app/check/permission`，亦由 `GlobalBroadcast.ACTION_SHOW_CHECK_PERMISSION_ACTIVITY` 广播拉起）。
- 页面载体 [activity_check_permission.xml](<resource-unit:#1 file:res/layout/activity_check_permission.xml>) 是原生列表式“开关清单”：`tvFz`/`tvFzOpen`（辅助功能行）、`tvVideo`、`tvXf`（悬浮窗行）、`tvMsg`（短信行），每行右侧配“打开”按钮（`@string/app_jc_zb_open_title`）。用户被要求逐项开启，其中第一项即无障碍。
- 关键跳转与状态判定**不在 DEX 中**：`CheckPermissionActivity.initView()`、`onResume()`、`onBackPressed()` 均为 `native` 声明，实现位于 `libcccc.so`（其中含 `CheckPermissionActivity>>checkResultWhenResume>>>isResumedCheck>>>`、`com.android.settings.InstalledAppDetails`、`android.settings.APPLICATION_DETAILS_SETTINGS`、`getAppDetailSettingIntent` 等字符串）。DEX 中检索 `ACTION_ACCESSIBILITY_SETTINGS` 无命中，说明无障碍页跳转 action 由 native 侧解密后拼装。

**3. 文案全量加密，规避静态文本扫描**
- 所有引导/诱导文案在 [strings.xml](<resource-unit:#1 file:res/values/strings.xml#L105-L121>) 中均为 `...[.Lt9]` 密文：`go_to_accessibility_setting`、`open_access_tip`、`permission_setting`、`app_opened`、`app_to_open`、`open_float_tip`、`float_window_permission_tip`、`app_jc_zb_title_1..15`。运行时由 `Dec.d()` → `libcccc.so` 解密渲染，因此无法从静态资源读到引导原文。
- 仅少数文案为明文，且属**运行时权限**分步教学：`permission_form_deny_prompt`「1.取得权限失败，无法执行操作。2.若因先前拒绝了权限授予…請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。」——这是拒权后的“回设置手动勾选”话术范式，无障碍引导复用同一套交互骨架。

**4. 拒权反馈与叠层能力**
- 状态判定 `ᡚ.㪖.isAccessibilityOpened()` = `isHaveAccessibility() || isHaveAccessibilityPluginPackage`，`isHaveAccessibility()` 直接查 `FocusService` 单例是否已连接（`getAccessibilityService()` + `isAccessibilityOn()`）。`CheckPermissionActivity.<init>` 与 `RegisterFirst2Activity` 均引用该判定，构成“未开启→停留/重跳本页”的闭环依据（`onResume` 中 `checkResultWhenResume/isResumedCheck` 由 native 执行，即返回设置页后立即复查）。
- 内置 `com.bw.dialog.TipsDialog` / `TopDialog` 自定义弹窗与 `FloatWindow`/`FocusFloatWindow`、`ViewVideoMaskFloatWindowBinding`、`maskWindows` 等悬浮/遮罩窗口体系（`SYSTEM_ALERT_WINDOW` 已申请），具备“跳设置后叠层指引/遮罩”的实现基础；`FocusService` 侧另有 `showMask`、`hideOtherMask`、`newMaskFloat`、`getMaskFloatWindowPath`。

**5. 获权后能力（与已登记 R-001 一致）**
`FocusService` 具备 `traverseNode`、`sendCurrentPage`、`autoClickConfirm`、`toDisableSelf`、`getPasswordCapture`、`getBcaInputPwdWindow`/`getBmriInputPwdWindow`/`getBniInputPwdWindow`、`recordPage`、`createBlackPageWsPublisher` 等——窗口读取、自动点击、密码截取、黑屏替换、自禁用规避，均依赖该无障碍授权。

**覆盖边界**：`libcccc.so` 的 `Dec.d` 解密算法与 `CheckPermissionActivity.initView/onResume` 的 JNI 实现未做函数级逆向，故 `.Lt9` 密文的**逐字原文**与跳转 action 的确切字面量无法给出（表中标注为不可静态还原）；引导页存在性、控件结构、服务伪装与跳转范式均已由资源与符号证实。该主题的实质风险已由项目既有 R-001 覆盖，本次不重复登记。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "DEX 未加壳，Manifest/无障碍配置/布局/服务声明完全可见；但 CheckPermissionActivity.initView/onResume/onBackPressed 为 native 实现，且全部引导文案以 .Lt9 密文存于 strings.xml（go_to_accessibility_setting、open_access_tip、permission_setting、app_jc_zb_title_1..15 等），由 libcccc.so 的 Dec.d 在运行期解密后渲染；无障碍设置页跳转 action 字面量在 DEX 中无命中，亦由 native 侧拼装，故逐字文案与确切 Intent 字符串不可静态还原。",
  "summary_one_liner": "冒用 PLN Mobile 身份、把无障碍服务声明为 isAccessibilityTool=true，并以专用 CheckPermissionActivity 原生开关清单（含 tvFz 辅助功能行）配合 native 解密的加密引导文案，将用户逐步引导至系统无障碍设置页开启 FocusService 全量窗口能力。",
  "disguise_identity": {
    "app_display_name": "PLN Mobile",
    "claimed_brand_or_persona": "PLN Mobile（印尼国家电力公司 PLN 官方 App）",
    "a11y_service_label": "PLN Mobile",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签与 android:description 均只写品牌名 'PLN Mobile'，无任何功能说明；无障碍配置显式伪造 android:isAccessibilityTool=\"true\"；包名 com.aa.bb 与类路径 hvghfdur.hfbuhgpg.ubjmglfd 完全无意义（随机化）；引导文案全部为 [.Lt9] 密文并置于自定义 .so 解密；DEX 中存在 asd.kkalive/kkdaemon/asd.fgh 多套 instrumentation 与多进程守护组件用于反移除"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "hvghfdur.hfbuhgpg.ubjmglfd.ui.SplashActivity（LAUNCHER）",
      "trigger_event": "用户点击桌面图标，onCreate/onResume 进入启动页",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "PLN Mobile",
      "shown_text_zh": "启动页显示 PLN Mobile 品牌名与图标 ic_logo",
      "user_action_requested": "无，自动跳转下一页面",
      "code_anchor": "hvghfdur.hfbuhgpg.ubjmglfd.ui.SplashActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "hvghfdur.hfbuhgpg.ubjmglfd.ui.RegisterFirst2Activity / LoginActivity / ActivationActivity",
      "trigger_event": "启动页跳转；RegisterFirst2Activity 构造时即调用 ᡚ.㪖.isAccessibilityOpened() 判定无障碍状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "不可静态还原（文案为 [.Lt9] 密文）",
      "shown_text_zh": "登录/激活/注册流程，以 PLN Mobile 身份要求用户登录；注册页在构造阶段即检查无障碍是否已开启",
      "user_action_requested": "输入账号密码并登录（存在登录、查询密码、安全密码等页面），无跳过入口",
      "code_anchor": "ngodanao.fdsnofdno.fdsfnso.RegisterFirst2Activity.㯺 → ᡚ.㪖.isAccessibilityOpened"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "hvghfdur.hfbuhgpg.ubjmglfd.ui.CheckPermissionActivity（路由 /app/check/permission，可由 GlobalBroadcast.ACTION_SHOW_CHECK_PERMISSION_ACTIVITY 广播拉起）",
      "trigger_event": "登录后跳转，或收到 ACTION_SHOW_CHECK_PERMISSION_ACTIVITY 广播；onCreate→initView()（native）渲染开关清单",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "tvFz: @string/app_jc_zb_title_1 = \"6HZFPYMWV6bQ8JG7J1EHo/m+UoTDBRUHvteEOpNN8EH8tysoLzFhwDq2uvcJSdydfD7M1OQcX8DNW0XK1uqKk0lPCXVfkuInRAcNhZMvHW4=[.Lt9]\"；按钮 tvFzOpen: @string/app_jc_zb_open_title = \"+1VqA+q2iQsGG4YD0b5ZIQ==[.Lt9]\"；标题 @string/app_jc_zb_title",
      "shown_text_zh": "原生“权限开启”清单页：第一行为辅助功能（tvFz/ivFz/app_open_selector 勾选状态图标 + tvFzOpen「打开」按钮），其下依次为录屏（tvVideo）、悬浮窗（tvXf，默认 visibility=gone）、短信（tvMsg，默认 gone）等行；标题与按钮文字为运行期解密文本",
      "user_action_requested": "点击各行的「打开」按钮逐项开启；页面无取消/跳过控件，onBackPressed 由 native 接管",
      "code_anchor": "res/layout/activity_check_permission.xml + hvghfdur.hfbuhgpg.ubjmglfd.ui.CheckPermissionActivity#initView（native）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置无障碍服务列表（或 com.android.settings.InstalledAppDetails 应用详情页）",
      "trigger_event": "点击 tvFzOpen「打开」按钮 → native 实现中构造 Intent 跳转（DEX 内无 ACTION_ACCESSIBILITY_SETTINGS 字面量，action 由 libcccc.so 解密拼装）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "PLN Mobile（服务名）；android:description = \"PLN Mobile\"",
      "shown_text_zh": "跳入系统无障碍设置，服务列表中该项仅显示「PLN Mobile」，描述同样仅为「PLN Mobile」，无功能说明；并因 isAccessibilityTool=true 被系统当作无障碍工具呈现",
      "user_action_requested": "用户需在系统列表中找到「PLN Mobile」并手动打开开关",
      "code_anchor": "res/xml/touch_accessibility_service_config.xml + hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService（BIND_ACCESSIBILITY_SERVICE）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 CheckPermissionActivity 后 onResume → native 逻辑 checkResultWhenResume / isResumedCheck 复查；配合 com.bw.dialog.TipsDialog / TopDialog 弹窗",
      "trigger_event": "用户从系统设置返回（onResume）；若 FocusService 单例未连接则 isAccessibilityOpened() 仍为 false，停留在本页并可再次点击「打开」",
      "ui_carrier": "原生Activity + 原生Dialog",
      "shown_text_verbatim": "permission_form_deny_prompt: \"1.取得权限失败，无法执行操作。<br><br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。\"",
      "shown_text_zh": "「1.取得权限失败，无法执行操作。2.若因先前拒绝了权限授予，而没有出现权限请求画面，请至『设置→应用程序→当前App→权限』，将「%s」勾选允许。」——以“操作失败”话术把责任推给用户，并给出进入应用设置页手动勾选的分步教学",
      "user_action_requested": "按提示再次进入系统设置手动勾选/开启；页面不提供降级或跳过路径",
      "code_anchor": "res/values/strings.xml#permission_form_deny_prompt + libcccc.so 字符串 CheckPermissionActivity>>checkResultWhenResume>>>isResumedCheck>>> + com.bw.dialog.TipsDialog"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.lzf.easyfloat FloatWindow / hvghfdur.hfbuhgpg.ubjmglfd.service.floatwindow.FocusFloatWindow / ViewVideoMaskFloatWindowBinding（FocusService.showMask / newMaskFloat）",
      "trigger_event": "悬浮窗权限就绪后（ᡚ.㪖.isHaveFloatWindow → com.lzf.easyfloat.permission），在引导/设置页之上叠加悬浮遮罩",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "float_window_permission_tip = \"C8FDtx2vtkz5+NKVRjX8AM9UlS4wr++PAWLxsrFC0uJRNvCZEWJPgyAtF9HxVhyd[.Lt9]\"；open_float_tip = \"haa1444CvLaI2DvN+FI9uKsrrPYm8ZlEaUrCWmrIQ1Y=[.Lt9]\"",
      "shown_text_zh": "悬浮窗权限与引导提示（密文，运行期解密）；遮罩窗口用于在目标页面之上覆盖显示或黑屏替换",
      "user_action_requested": "按遮罩提示继续操作（可静态确认的是悬浮窗实现与遮罩窗口体系存在）",
      "code_anchor": "hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService#showMask / #newMaskFloat / res/values/strings.xml#float_window_permission_tip"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService（onServiceConnected 后全量窗口监听）",
      "trigger_event": "用户在系统设置中开启「PLN Mobile」无障碍开关 → onServiceConnected → isAccessibilityOn=true",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务连上后进入窗口监听：traverseNode 遍历节点、sendCurrentPage 上报当前页、autoClickConfirm 自动点击、passwordCapture 与 bca/bmri/bniInputPwdWindow 截取输入密码、recordPage/createBlackPageWsPublisher 录屏与黑屏替换；toDisableSelf 用于规避撤权检测",
      "user_action_requested": "无（后台静默执行）",
      "code_anchor": "hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService#onServiceConnected / #traverseNode / #sendCurrentPage / #autoClickConfirm / #toDisableSelf"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务标签 @string/app_name_input = \"PLN Mobile\"（AndroidManifest 中 FocusService 的 android:label）",
    "系统无障碍服务描述：@string/accessibility_service_description = \"PLN Mobile\"（res/values/strings.xml 第 30 行，由 touch_accessibility_service_config.xml 的 android:description 引用）",
    "CheckPermissionActivity 原生开关清单页：res/layout/activity_check_permission.xml 的 tvFz（app_jc_zb_title_1）、tvFzOpen/tvVideoOpen（app_jc_zb_open_title「打开」）、tvVideo、tvXf、tvMsg 各行，文案均为 [.Lt9] 密文运行期解密",
    "引导/说明密文资源集中存放于 res/values/strings.xml：go_to_accessibility_setting、open_access_tip、permission_setting、open_float_tip、float_window_permission_tip、app_opened、app_to_open、app_jc_zb_title_1..15",
    "拒权提示弹窗（TipsDialog/TopDialog 或 Activity 内 TextView）：permission_form_deny_prompt / permission_form_deny_prompt2 明文，教用户进『设置→应用→当前App→权限』勾选",
    "悬浮窗叠层：FocusFloatWindow / FloatWindow（com.lzf.easyfloat）+ ViewVideoMaskFloatWindowBinding，用于在设置页或目标页之上叠加提示/遮罩",
    "应用桌面与通知栏标识：@string/app_name = \"PLN Mobile\"、mipmap/ic_logo",
    "未发现 assets/ 目录与本地 HTML 引导页；引导均以原生页面 + 密文文本 + 悬浮窗承载"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "PLN Mobile",
      "text_zh": "PLN Mobile（印尼国家电力公司品牌名，同时作为应用名、无障碍服务名与服务描述）",
      "source_location": "res/values/strings.xml → app_name_input / app_name / accessibility_service_description",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "1.取得权限失败，无法执行操作。<br><br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，請至『設定→應用程式→當前App→權限』，將「%s」勾選允許。",
      "text_zh": "1.取得权限失败，无法执行操作。2.若因先前拒绝了权限授予，而没有出现权限请求画面，请至『设置→应用程序→当前App→权限』，将「%s」勾选允许。",
      "source_location": "res/values/strings.xml → permission_form_deny_prompt",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "1.取得权限失败，无法执行操作。 2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。",
      "text_zh": "同上简体版本：以“操作失败”为前提，指导用户进入应用详情页手动勾选被拒权限。",
      "source_location": "res/values/strings.xml → permission_form_deny_prompt2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "获取权限失败，继续保存图片",
      "text_zh": "获取权限失败，继续保存图片（权限失败仍继续动作，弱化权限缺失的严重性）",
      "source_location": "res/values/strings.xml → permission_failed_and_save_image",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "zh",
      "text_verbatim": "获取系统录音权限被拒绝 / 获取系统相机权限被拒绝",
      "text_zh": "获取系统录音权限被拒绝 / 获取系统相机权限被拒绝",
      "source_location": "res/values/strings.xml → selector_audio_permission_ungranted / selector_camera_permission_ungranted",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "zh",
      "text_verbatim": "3zlhHYHKi2QQi1tWNI1PeFODxrbtK6/5hDSWWV0bFOImnLoYQ0qJRazow+mzJTBs[.Lt9]",
      "text_zh": "密文，运行期由 libcccc.so 解密；键名 go_to_accessibility_setting 表明其为“前往无障碍设置”的按钮/提示文案（明文逐字不可静态还原）",
      "source_location": "res/values/strings.xml → go_to_accessibility_setting",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "6HZFPYMWV6bQ8JG7J1EHo/m+UoTDBRUHvteEOpNN8EH8tysoLzFhwDq2uvcJSdydfD7M1OQcX8DNW0XK1uqKk0lPCXVfkuInRAcNhZMvHW4=[.Lt9]",
      "text_zh": "密文，CheckPermissionActivity 第一行（辅助功能项）的标题文案，运行期解密（明文逐字不可静态还原）",
      "source_location": "res/values/strings.xml → app_jc_zb_title_1（被 activity_check_permission.xml 的 tvFz 引用）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "+1VqA+q2iQsGG4YD0b5ZIQ==[.Lt9]",
      "text_zh": "密文，各权限行的「打开」按钮文字（app_jc_zb_open_title / app_jc_zb_title_4 / app_jc_zb_title_5 共用同一密文）",
      "source_location": "res/values/strings.xml → app_jc_zb_open_title",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "C8FDtx2vtkz5+NKVRjX8AM9UlS4wr++PAWLxsrFC0uJRNvCZEWJPgyAtF9HxVhyd[.Lt9]",
      "text_zh": "密文，悬浮窗权限提示文案（float_window_permission_tip），运行期解密",
      "source_location": "res/values/strings.xml → float_window_permission_tip",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "从系统设置返回后 CheckPermissionActivity.onResume 触发 native 复查（libcccc.so 中可见字符串 CheckPermissionActivity>>checkResultWhenResume>>>isResumedCheck>>>），若 FocusService 单例未连接则 isAccessibilityOpened()（= isHaveAccessibility() || isHaveAccessibilityPluginPackage）仍为 false，页面停留在原生开关清单并允许无限次再次点击「打开」重跳设置；onBackPressed 亦为 native 接管，存在阻断返回的判定空间。是否含定时器强制重跳未取得直接证据。",
    "overlay_or_fake_settings": "不伪造系统设置页；但在跳转/引导期间使用 com.lzf.easyfloat 的 FloatWindow/FocusFloatWindow 与 ViewVideoMaskFloatWindowBinding（FocusService.showMask/newMaskFloat/hideOtherMask、maskWindows、maskFloatWindowPath）叠放悬浮窗/遮罩层，可在设置页之上提供悬浮指引或后续黑屏替换。",
    "restricted_settings_13plus_coaching": "明文存在同类分步教学话术：permission_form_deny_prompt / permission_form_deny_prompt2 指导用户进入『设置→应用程序→当前App→权限』手动勾选「%s」；libcccc.so 同时含 android.settings.APPLICATION_DETAILS_SETTINGS、com.android.settings.InstalledAppDetails、getAppDetailSettingIntent，具备跳应用详情页（受限设置入口）的实现。未发现 Session 安装器绕过逻辑。",
    "post_grant_anti_removal": "存在撤权对抗组件：FocusService.toDisableSelf、onInterrupt、checkMainService/onDisconnectedRunnable，以及 Manifest 中 asd.kkalive.Keep111Instrumentation、asd.kkdaemon.RunInstrumentation 多进程守护（:resident/:daemon/:assist1-3）与 com.aa.bb.matrix.permission.PROCESS_SUPERVISOR；DEX 预筛亦命中 PERFORM_GLOBAL_ACTION（可用于监听设置页后按 BACK/HOME 阻止撤权）。具体 GLOBAL_ACTION 使用点未在本轮逐条取证。",
    "benign_graceful_degradation": "无。页面无跳过/取消控件，未开启即无法进入后续业务；不提供手动模式或替代路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到应用进程发出跳转 ACTION_ACCESSIBILITY_SETTINGS（或异常以 APPLICATION_DETAILS_SETTINGS + InstalledAppDetails 形式跳应用详情页）的瞬间拉起 UTG；次优时机为 CheckPermissionActivity 首次 onResume 呈现开关清单时（该页 onResume 为 native 实现，建议 Hook Activity.onResume 按类名过滤）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/登录后的引导开关清单页",
        "page_identifier": "hvghfdur.hfbuhgpg.ubjmglfd.ui.CheckPermissionActivity，layout 含 id tvFz/tvFzOpen/tvVideo/tvXf/tvMsg、ImageView ivFz 背景 app_open_selector",
        "why_most_useful": "这是全部诱导的策源地：可直接证明应用在正常业务流中强制要求开启辅助功能，且无跳过入口",
        "observable_utg_signals": ["控件 id 组合 tvFz + tvFzOpen + app_open_selector 背景", "页面标题与按钮文本为运行期解密后文字（非资源表可见文本）", "无任何 skip/cancel/close 控件", "首行为辅助功能、其下为录屏/悬浮窗/短信，形成递进索取"]
      },
      {
        "page_role": "跳转前的说明/弹窗层",
        "page_identifier": "com.bw.dialog.TipsDialog 或 com.bw.dialog.TopDialog 弹窗（自定义 View，非系统 AlertDialog），可能叠加 FocusFloatWindow 悬浮层",
        "why_most_useful": "解密后的诱导话术在此首次以可读形式出现，是判断话术性质（假更新/故障恐吓/安全恐吓）的关键取证点",
        "observable_utg_signals": ["自定义 Dialog 类名不在 android.app.AlertDialog 体系", "弹窗按钮仅有确认/「打开」，无取消", "文本内容与 strings.xml 中 [.Lt9] 密文键位对应（可回指 go_to_accessibility_setting / open_access_tip / app_jc_zb_title_*）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中的 \"PLN Mobile\" 条目，subtitle/description 同为 \"PLN Mobile\"",
        "why_most_useful": "证明身份伪装落地：用户在系统层面看到的是银行/电力品牌而非功能说明，且 isAccessibilityTool=true 使其被归类为无障碍工具",
        "observable_utg_signals": ["服务名与描述完全相同的品牌名、无功能描述", "同页可见应用包名 com.aa.bb 与品牌不符", "开关被打开后立即返回应用即恢复业务流"]
      },
      {
        "page_role": "设置页返回后的复查/再引导页",
        "page_identifier": "CheckPermissionActivity 再次 onResume 或 TipsDialog 二次弹出；可能伴 FocusFloatWindow 遮罩",
        "why_most_useful": "用于判定拒权闭环：是否死循环重跳、是否以“操作失败”话术施压",
        "observable_utg_signals": ["返回应用后立刻重复出现同一开关清单或弹窗", "出现 permission_form_deny_prompt 的“取得权限失败，无法执行操作”文案", "页面层级中出现悬浮窗（TYPE_APPLICATION_OVERLAY）窗口"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：全部核心引导文案以 [.Lt9] 密文存于 strings.xml 并由 libcccc.so 在运行期解密，CheckPermissionActivity.initView/onResume/onBackPressed 亦为 native 实现，静态侧只能读到键名与密文，无法获得逐字原文与跳转 action 字面量；同时 DEX 中存在 asd.kkalive/asd.kkdaemon 多进程守护与 toDisableSelf 自禁用逻辑，运行期可能干扰 UTG 采集稳定性。应用本身未加壳，运行期 UTG 不受影响，但若仅在纯静态阶段评估会严重低估诱导话术。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "hvghfdur.hfbuhgpg.ubjmglfd.ui.CheckPermissionActivity#initView / #onResume / #onBackPressed（native，实现于 libcccc.so）",
    "hvghfdur.hfbuhgpg.ubjmglfd.service.FocusService#onServiceConnected / #showMask / #toDisableSelf",
    "ᡚ.㪖#isAccessibilityOpened / #isHaveAccessibility",
    "res/layout/activity_check_permission.xml（tvFz / tvFzOpen / tvVideo / tvXf / tvMsg）",
    "res/xml/touch_accessibility_service_config.xml（isAccessibilityTool=true, typeAllMask, canPerformGestures）",
    "res/values/strings.xml（accessibility_service_description=PLN Mobile；go_to_accessibility_setting、app_jc_zb_title_1、app_jc_zb_open_title 等 .Lt9 密文）"
  ]
}
```

</details>
