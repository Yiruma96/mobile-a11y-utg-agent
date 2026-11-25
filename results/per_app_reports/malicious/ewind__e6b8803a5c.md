# MR_089__e6b8803a5c｜ewind — Security Antivirus

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：155.3s

## 1. 一句话核心结论

- **核心申请方式**：以“省电优化/防应用自启动”为名，在权限引导页与省电页双入口弹原生对话框索要无障碍，点击后直接跳系统无障碍设置，并在 1 秒后叠压带手指动画的全屏半透明遮罩教学，未授权则每 500ms 轮询并反复重开权限页。
- **静态可见性说明**：无障碍申请全链路均在本地 DEX 与资源中明文可见：跳转点 ns.ne.a 硬编码 android.settings.ACCESSIBILITY_SETTINGS；引导弹窗为原生 Dialog（dialog_battery_accessibility_layout.xml）；跳转后遮罩页为本地 Activity + 本地布局 accessibility_toast_view.xml；文案全部来自 res/values/strings.xml。未发现加壳、AES 密文配置或远端 HTML 下发的引导页；assets/privacy.html 与 assets/terms.html 仅为 Google Docs 导出的隐私/条款静态页，不参与无障碍引导。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e6b8803a5ca0220b931f69f530916a7941732615d581842badd028d764c92f13` |
| 包名 / 年份 | `com.antivirus.booster.security` / 2018 |
| 家族 / 品类 | **ewind**（同池样本数：2） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/18/a/apps-disguised-security-tools-bombard-users-ads-track-users-location.html |
| 桌面显示名 | Security Antivirus |
| 引导页宣称品牌/身份 | Security Antivirus（自称杀毒/省电优化工具，文案中借“system optimization and phone security”“stop unnecessary app(s)”“boost phone performance more than 50%”塑造系统级安全与性能工具身份） |
| 系统无障碍列表服务名 | Security Antivirus（服务 android:label=@string/app_name，即桌面显示名，系统无障碍列表中无“省电/优化”等真实功能描述） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无空白挤出/同形字/多 activity-alias/伪造 isAccessibilityTool。但存在三类身份弱化手法：1) 无障碍服务类名 BatteryOptimizeService 与系统列表展示名 Security Antivirus 分离，用户难以从名称判断其为可读取窗口内容并模拟点击的服务；2) 跳转后用全屏 translucent_dark 遮罩 + 应用图标 + 手指点击动画覆盖在系统无障碍设置之上，形成“类系统引导页”视觉误导；3) android:description 与弹窗文案一致强调“隐私完全安全”，并主动给出“可忽略隐私警告”的免责提示，弱化用户对敏感权限的警觉。 |
| 无障碍服务类名 | `com.anti.security.service.BatteryOptimizeService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Security Antivirus only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>        You can have the privacy warning ignored. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | an.sc.clean.act.smstapge（SplashTheme 启动页）→ an.sc.clean.act.smmain（MainActivity）→ NavigationFragment 导航项 | LAUNCHER 启动进入主界面后，用户点击导航中的权限/安全等级入口（NavigationFragment$1.onClick） | 原生Activity | **原文**：无（该步无引导文案，仅导航入口图标）<br>**译注**：主界面导航项，无文字引导，点击进入权限页 | 点击导航项进入权限/安全等级页；可正常使用其他功能，无强制阻塞 | `com.anti.security.view.fragment.NavigationFragment$1.onClick` |
| 2 | 引导说明页 | com.anti.security.activity.GrantPermissonsActivity（layout activity_grant_permission，单实例） | onCreate → initData() → updateData() → updateView()，页面展示安全等级（basic→Full Protection） | 原生Activity | **原文**：Accessibility / System optimization and phone security；Notification / Assist to protect personal information；Usage / Protect app privacy；Please grant all permissions to enhance security level<br>**译注**：无障碍——系统优化与手机安全；通知——协助保护个人信息；使用情况——保护应用隐私；请授予全部权限以提升安全等级 | 逐项点击未开启的权限卡片（右侧 ENABLE 按钮或整卡点击）；顶部返回箭头可退出，无强制停留逻辑 | `com.anti.security.activity.GrantPermissonsActivity.initData / updateView` |
| 3 | 引导说明页（省电入口并行分支） | an.sc.clean.act.smbatsavsel（activity_battery_select_layout 省电优化页）+ 原生 Dialog an.sc.clean.v.smaccess | 省电页 trySuperSave()/onCreate 检测 BatteryOptimizeService.a() 为 false 时 batteryAccessibilityDialog.show() | 原生Dialog | **原文**：Enable Security Antivirus / Security Antivirus use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%. / NOT NOW / ENABLE<br>**译注**：启用 Security Antivirus / Security Antivirus 使用无障碍功能帮助您停止不必要的应用，可提升电池续航并让手机性能提升 50% 以上 / 暂不 / 启用 | 点击 ENABLE 继续，或点击 NOT NOW 关闭对话框（此时停留在省电页，不跳设置） | `an.sc.clean.v.smaccess.onCreate / dialog_battery_accessibility_layout.xml` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | GrantPermissonsActivity$4.onClick（无障碍卡）或 smbatsavsel.onEnable（对话框 ENABLE）→ ns.ne.a(activity, ACCESS_REQUEST_CODE) | 系统无障碍页 | **原文**：无（应用侧仅调用 startActivityForResult，不注入界面文字）<br>**译注**：直接跳转系统无障碍设置列表，由系统原生界面呈现 | 用户需在系统列表中自行找到并开启“Security Antivirus”服务；应用在此步不做节点自动点击（ne.a 仅置 k=true 标记，实际自动点击由服务运行期 onAccessibilityEvent 触发） | `ns.ne.a  → new Intent("android.settings.ACCESSIBILITY_SETTINGS")` |
| 5 | 遮罩叠层指引 | an.sc.clean.act.smaccessdia（layout accessibility_toast_view，PermissionToastView） | 跳转后 Handler.postDelayed(new GrantPermissonsActivity$4$1, 1000L) 触发 showAccessibilityToast()；省电页由 smbatsavsel$8 同样延迟 1000ms 触发 | 悬浮窗Overlay | **原文**：Please find and enalbe Security Antivirus for system optimization and phone security.；布局默认文案 To prevent apps from restarting and save battery power, please find and enable Security Antivirus.；按钮 GOT IT<br>**译注**：请找到并启用 Security Antivirus 以实现系统优化与手机安全；为防止应用重新启动并节省电量，请找到并启用 Security Antivirus；按钮“知道了” | 按手指动画指示在系统列表中查找并开启本应用服务，然后点击 GOT IT 关闭遮罩；遮罩全屏覆盖系统设置页，除 GOT IT 外无其他关闭控件 | `com.anti.security.activity.GrantPermissonsActivity.showAccessibilityToast / an.sc.clean.act.smaccessdia.onCreate / accessibility_toast_view.xml` |
| 6 | 拒权反馈循环 | GrantPermissonsActivity 自身（singleTask，反复 startActivity 重入） | showAccessibilityToast 末尾 post(checkAcessiblity)；GrantPermissonsActivity$3.run 每 500ms 检查 BatteryOptimizeService.a()；onResume 亦 removeCallbacksAndMessages(null) 后重算 | 原生Activity | **原文**：无新增文案（循环重开权限页，安全等级停留在 basic，仍显示 Please grant all permissions to enhance security level）<br>**译注**：未开启则每 500ms 重查并最终重新打开权限页，安全等级保持 basic 并持续提示授予全部权限 | 无跳过/不再提示选项；用户返回后仍会被重开权限页，只能通过开启服务或离开应用中断循环 | `com.anti.security.activity.GrantPermissonsActivity$3.run / jumpBackFrombackgroundSetting` |
| 7 | 获权后动作 | com.anti.security.service.BatteryOptimizeService（ns.ne）→ onAccessibilityEvent | 服务启用后收到 typeWindowStateChanged（eventType 32）事件，且 smsaverb.a().d() 为真、包名为 com.android.settings | 不可静态还原（运行期对系统设置页节点操作，无自定义 UI） | **原文**：无（服务不渲染界面，通过 findAccessibilityNodeInfosByText / findAccessibilityNodeInfosByViewId + performAction(16) 点击节点；并读取 com.android.settings 的 force_stop 字符串）<br>**译注**：服务在后台自动检索并点击系统设置页上的按钮节点，包括应用详情页的强制停止 | 无需用户操作；获权后由服务自动执行点击 | `ns.ne.onAccessibilityEvent / ns.ne.a(AccessibilityNodeInfo,String[])` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内 NavigationFragment 导航项 → 跳转 GrantPermissonsActivity（无引导文案，仅入口）
- GrantPermissonsActivity 列表三张权限卡（activity_grant_permission 布局）：标题与副标题来自 strings.xml 的 acessibility/acessibility_content、notification_usage/notification_content、app_with_usage/app_with_usage_content
- GrantPermissonsActivity 顶部安全等级区：security_level_secure/basic/best 与 security_level_tip_basic（“Please grant all permissions to enhance security level”）
- 省电优化页 smbatsavsel 弹出的不可取消遮罩式原生 Dialog（dialog_battery_accessibility_layout.xml，style upgrade_dialog_style）：enable_dr_security 标题 + battery_permission_desc 正文 + NOT NOW / ENABLE
- 跳转系统无障碍设置后 1 秒压栈的本地 Activity smaccessdia（accessibility_toast_view.xml）：全屏 translucent_dark 遮罩 + ic_launcher 图标 + tv_content（accessibility_desc 动态传入 / accessibility_toast_text 布局默认）+ RecyclerView 手指点击动画 + GOT IT 按钮
- 系统无障碍服务列表项：服务 label = @string/app_name（Security Antivirus），描述 = boost_tag_acc_kill_service_description（res/xml/top_accessbility.xml 引用）
- 跳转使用情况访问权限前弹出的引导 Dialog（ns.nh.a + dialog_usage_guide_content：“Please find and enalbe Security Antivirus for personal information protection.”）与 dialog_usage_content（“Turn on the usage to ensure proper operation of AppLock.”）
- 跳转悬浮窗权限前弹出的 EnableOverlayDIalog（an.sc.clean.u.smoverlay，EnableClickInterface.onContinue）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please find and enalbe Security Antivirus for system optimization and phone security. | 请找到并启用 Security Antivirus，以实现系统优化与手机安全。 | `res/values/strings.xml → key accessibility_desc；由 GrantPermissonsActivity.showAccessibilityToast 作为 extra 传入 smaccessdia` | 清理工具伪装 |
| en | To prevent apps from restarting and save battery power, please find and enable Security Antivirus. | 为防止应用重新启动并节省电量，请找到并启用 Security Antivirus。 | `res/values/strings.xml → key accessibility_toast_text；accessibility_toast_view.xml 中 tv_content 默认文案` | 清理工具伪装 |
| en | Enable Security Antivirus | 启用 Security Antivirus | `res/values/strings.xml → key enable_dr_security；dialog_battery_accessibility_layout.xml 标题` | 清理工具伪装 |
| en | Security Antivirus use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%. | Security Antivirus 使用无障碍功能帮助您停止不必要的应用，可提升电池续航并让手机性能提升 50% 以上。 | `res/values/strings.xml → key battery_permission_desc（formatted=false）；dialog_battery_accessibility_layout.xml 正文` | 清理工具伪装 |
| en | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Security Antivirus only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>        You can have the privacy warning ignored. | 无障碍可阻止不想要的应用重新打开，也能延长电池寿命与耐用性。Security Antivirus 仅用于优化设备功能，我们保证您的隐私与个人数据完全安全。您可以忽略隐私警告。 | `res/values/strings.xml → key boost_tag_acc_kill_service_description；经 res/xml/top_accessbility.xml 的 android:description 在系统无障碍列表展示` | 教唆忽视警告 |
| en | Accessibility | 无障碍 | `res/values/strings.xml → key acessibility；GrantPermissonsActivity.initData 列表项标题` | 良性透明说明 |
| en | System optimization and phone security | 系统优化与手机安全 | `res/values/strings.xml → key acessibility_content；GrantPermissonsActivity.initData 列表项副标题` | 清理工具伪装 |
| en | Please grant all permissions to enhance security level | 请授予全部权限以提升安全等级 | `res/values/strings.xml → key security_level_tip_basic；GrantPermissonsActivity.updateView` | 假反诈安全 |
| en | Please find and enalbe Security Antivirus for personal information protection. | 请找到并启用 Security Antivirus，以保护个人信息。 | `res/values/strings.xml → key dialog_usage_guide_content；GrantPermissonsActivity.jumpToUsageSetting 传入 ns.nh.a` | 隐私承诺 |
| en | Turn on the usage to ensure proper operation of AppLock. | 开启使用情况访问权限以确保应用锁正常运行。 | `res/values/strings.xml → key dialog_usage_content` | 受限设置分步教学 |
| en | For full & advanced protection, please enable Security Antivirus's system permission. | 为获得完整且高级的保护，请启用 Security Antivirus 的系统权限。 | `res/values/strings.xml → key dialog_usage_content_one` | 假反诈安全 |
| en | NO private data will be collected. | 不会收集任何私人数据。 | `res/values/strings.xml → key dialog_usage_content_two` | 隐私承诺 |
| en | GOT IT | 知道了 | `res/values/strings.xml → key usage_setting_guide_btn；accessibility_toast_view.xml 中 gotItBtn` | 受限设置分步教学 |
| en | NOT NOW | 暂不 | `res/values/strings.xml → key not_now；dialog_battery_accessibility_layout.xml 中 tv_cancel` | 良性透明说明 |
| en | ENABLE | 启用 | `res/values/strings.xml → key enable2；dialog_battery_accessibility_layout.xml 中 tv_enable` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：省电页对话框可点 NOT NOW 关闭且不跳转（仅本次关闭，无持久化“不再提示”标记，下次进入 trySuperSave 仍会 show）。权限引导页点击无障碍卡后进入严格循环：showAccessibilityToast 末尾 post(checkAcessiblity)，GrantPermissonsActivity$3.run 每 500ms 检查 BatteryOptimizeService.a()，未开启则 postDelayed 自身持续轮询；一旦判断分支结束即调用 jumpBackFrombackgroundSetting 以 singleTask 重新 startActivity(GrantPermissonsActivity)，onResume 又 removeCallbacksAndMessages(null) 并重算安全等级。用户从系统设置按返回后同样经 onResume/onActivityResult 重算并停留在权限页，形成“返回即被拉回权限页”的反馈压力。
- **遮罩叠层 / 高仿系统设置页**：是。跳转系统无障碍设置后 1 秒（postDelayed 1000ms）启动本地 Activity smaccessdia，加载 accessibility_toast_view.xml：全屏 translucent_dark maskLayout 覆盖系统设置页，内嵌应用图标、说明文案、RecyclerView 手指点击动画与 GOT IT 按钮，形成类系统引导叠层（非高仿系统开关，而是压栈式半透明遮罩教学）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、也未发现引导用户进入应用详情右上角菜单允许受限设置的文案或代码路径；预筛的 RESTRICTED_STR / SESSION_INSTALLER 线索未在无障碍引导链中落地。targetSdkVersion=22，本身不受 Android 13 受限设置机制约束。
- **获权后即时行为与防撤权机制**：服务侧具备替代用户在系统设置页操作的能力：ns.ne.onAccessibilityEvent 在 com.android.settings 的 typeWindowStateChanged 事件中，通过 findAccessibilityNodeInfosByViewId（flagReportViewIds）与 findAccessibilityNodeInfosByText 定位节点，ns.ne.a 以 performAction(16) 自动点击；并专门处理 InstalledAppDetailsTop / InstalledAppDetailsActivity 页面及读取系统 force_stop 字符串。静态代码中未发现直接用于阻止自身撤权的专用分支（如监听无障碍页后 GLOBAL_ACTION_BACK 返回），但该自动点击能力可用于关闭他人应用或代点设置项，越出所宣称的省电用途。
- **良性降级 / 替代方案**：无。未发现“仅使用手动清理/ADB 授权/观看模式”等替代路径；未授权时安全等级固定停留在 basic 并持续提示“Please grant all permissions to enhance security level”，无功能降级说明。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条最佳触发点：1) 冷启动进入 MainActivity 后点击导航权限入口，或直接以 am start 拉起 com.anti.security.activity.GrantPermissonsActivity，捕获“三权限卡 + 安全等级”页面；2) 在该页点击无障碍卡（或在省电页点 ENABLE）后立即开始 UTG 连续采集——前 0.5s 捕获 ACTION_ACCESSIBILITY_SETTINGS 跳转，约 1s 后必捕获全屏遮罩引导页 smaccessdia。若监测到 Window 变化包含 com.android.settings 无障碍页 + 随后出现的 translucent_dark 全屏窗口，即为该家族特征窗口序列。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：全部引导文案均为可读文本，遮罩页文字为真实 TextView（非图片），无需 OCR。需注意两点：1) 遮罩页的手指教学区域为 RecyclerView + 图片，若只看文本会漏掉“动画教学”语义，需结合窗口叠加与图像特征；2) 该包静态未加壳，运行期 UTG 完全可用；但获权后的服务行为（ns.ne.onAccessibilityEvent 自动点击系统设置节点）无自定义 UI，UTG 只能通过系统设置页上的焦点/点击变化间接观察，需配合无障碍事件日志或 Hook 佐证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **权限引导页（三权限卡 + 安全等级）** | Activity com.anti.security.activity.GrantPermissonsActivity，标题含“Accessibility / Notification / Usage”三行卡片，右上或顶部显示“Full Protection/basic”等级条 | 该页是全部无障碍引导的调度中心，能一次性看到应用把无障碍与通知、使用情况并列包装为“安全等级”，是判断工具伪装与诱导顺序的关键现场 | 三张权限卡文案 Accessibility / System optimization and phone security；安全等级提示 Please grant all permissions to enhance security level；卡片右侧 ENABLE 按钮与整卡可点击区域 |
| **省电页原生无障碍请求对话框** | Dialog 窗口（style upgrade_dialog_style）叠加在 an.sc.clean.act.smbatsavsel 之上，标题“Enable Security Antivirus”，按钮 NOT NOW / ENABLE | 该弹窗把无障碍权限直接包装为“提升续航 50%”的性能承诺，是叙事伪装最直白的一处，且是第二条独立入口 | 对话框标题 Enable Security Antivirus；正文 boost phone performance more than 50%；NOT NOW / ENABLE 双按钮 |
| **跳转前系统无障碍设置页** | 系统设置 Activity（com.android.settings 无障碍列表），列表中出现 label 为“Security Antivirus”的服务项 | 证明应用是直接跳系统无障碍列表而非走应用详情页，同时暴露服务在系统中的展示名与 description，用于比对身份宣称 | 包名 com.android.settings 的窗口；列表项文本 Security Antivirus；服务描述含 privacy and personal data is total safe 与 You can have the privacy warning ignored |
| **设置页后约 1 秒压栈的全屏遮罩引导页** | Activity an.sc.clean.act.smaccessdia（全屏 translucent_dark 窗口），含 ic_launcher 图标、手指点击动画区域与 GOT IT 按钮 | 这是该家族最具辨识度的诱导手法：在系统设置页之上压栈半透明遮罩并做手指动画教学，UTG 一旦抓到该窗口序列即可强判定“遮罩叠层指引” | 窗口类名 an.sc.clean.act.smaccessdia；全屏半透明遮罩 + 应用图标组合；GOT IT 按钮文本；说明文案 please find and enable Security Antivirus；手指点击动画区域（RecyclerView + hand 图） |
| **拒权后返回的循环重跳现场** | 从系统设置返回后再次出现的 GrantPermissonsActivity（singleTask 重入），安全等级仍为 basic | 通过连续 2-3 次按返回并记录窗口时间戳，可量化 500ms 轮询与 jumpBackFrombackgroundSetting 的重开频率，区分“一次性引导”与“死循环重跳” | 同一 GrantPermissonsActivity 在短时间内被多次重建（onCreate/onResume 序列）；无“不再提示”勾选项；安全等级提示文案持续存在 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `ns.ne.a(android.app.Activity, int) —— startActivityForResult("android.settings.ACCESSIBILITY_SETTINGS")`
- `com.anti.security.activity.GrantPermissonsActivity.showAccessibilityToast / $3.run / jumpBackFrombackgroundSetting`
- `com.anti.security.activity.GrantPermissonsActivity$4.onClick —— 三权限卡分发（无障碍/USAGE/MANAGE_OVERLAY_PERMISSION）`
- `an.sc.clean.v.smaccess.onCreate + res/layout/dialog_battery_accessibility_layout.xml`
- `an.sc.clean.act.smaccessdia.onCreate + res/layout/accessibility_toast_view.xml`
- `ns.ne.onAccessibilityEvent —— com.android.settings 节点检索与 performAction(16) 自动点击`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**静态可见性：完全可见（clear）**。无障碍引导全链在 DEX、布局、strings、xml 中均可静态还原，未加壳、无密文/远端 HTML 下发。

**核心机制（两条并行入口）**

1. **权限引导页入口**：主界面导航项 → [NavigationFragment$1.onClick](<resource-unit:#1.dex1 code:com.anti.security.view.fragment.NavigationFragment$1#onClick>) 启动 [GrantPermissonsActivity](<resource-unit:#1.dex1 code:com.anti.security.activity.GrantPermissonsActivity#onCreate>)，页面以「Accessibility / Notification / Usage」三张权限卡呈现安全等级；点击无障碍项未开启 → [GrantPermissonsActivity$4.onClick](<resource-unit:#1.dex1 code:com.anti.security.activity.GrantPermissonsActivity$4#onClick>) → [ns.ne#a](<resource-unit:#1.dex1 code:ns.ne#a>) 的 `startActivityForResult("android.settings.ACCESSIBILITY_SETTINGS")`。
2. **省电功能页入口**：省电优化页 [smbatsavsel#onCreate](<resource-unit:#1.dex1 code:an.sc.clean.act.smbatsavsel#onCreate>) 预置原生 Dialog [smaccess](<resource-unit:#1.dex1 code:an.sc.clean.v.smaccess#onCreate>)，文案「Enable Security Antivirus / …boost phone performance more than 50%」，按钮 NOT NOW / ENABLE；[onEnable](<resource-unit:#1.dex1 code:an.sc.clean.act.smbatsavsel#onEnable>) 走同一跳转。

**跳转后的关键诱导手法**
- **1 秒后压栈全屏遮罩**：[showAccessibilityToast](<resource-unit:#1.dex1 code:com.anti.security.activity.GrantPermissonsActivity#showAccessibilityToast>) 启动 [smaccessdia](<resource-unit:#1.dex1 code:an.sc.clean.act.smaccessdia#onCreate>)，加载 [accessibility_toast_view.xml](<resource-unit:#1 file:res/layout/accessibility_toast_view.xml>)——`translucent_dark` 全屏遮罩 + 应用图标 + 手指点击动画 RecyclerView + GOT IT，叠在系统无障碍设置之上教学。
- **拒权轮询循环**：[GrantPermissonsActivity$3#run](<resource-unit:#1.dex1 code:com.anti.security.activity.GrantPermissonsActivity$3#run>) 每 500ms 检查 `BatteryOptimizeService.a()`，未开启持续 `postDelayed`，结束后 [jumpBackFrombackgroundSetting](<resource-unit:#1.dex1 code:com.anti.security.activity.GrantPermissonsActivity#jumpBackFrombackgroundSetting>) 重新 `startActivity` 自身；`onResume` 亦 `removeCallbacksAndMessages(null)` 后重算，无「不再提示」持久化退出。
- **身份伪装**：服务 `android:label="@string/app_name"`（Security Antivirus），系统无障碍列表 description 见 [res/xml/top_accessbility.xml](<resource-unit:#1 file:res/xml/top_accessbility.xml>)，声称「防止应用重开、延长电池寿命…隐私数据完全安全」并主动提示「可忽略隐私警告」。
- **能力越界**：服务 `flagReportViewIds` + [ns.ne#onAccessibilityEvent](<resource-unit:#1.dex1 code:ns.ne#onAccessibilityEvent>) 在 `com.android.settings` 窗口按 viewId/文本检索节点，[ns.ne#a](<resource-unit:#1.dex1 code:ns.ne#a>) 用 `performAction(16)` 自动点击，并专门识别 `InstalledAppDetailsTop` 与系统 `force_stop` 字符串。
- **未发现**：`ACTION_APPLICATION_DETAILS_SETTINGS` 跳转、Android 13+ 受限设置分步教学、Session 安装器绕过（预筛 `RESTRICTED_STR`/`SESSION_INSTALLER` 在引导链中未落地为实际代码路径）。

**判定**：属工具型（省电/清理）伪装下的无障碍权限分步诱导 + 遮罩叠层教学 + 拒权重跳循环，已登记风险 R-001（high / deceptive_behavior）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请全链路均在本地 DEX 与资源中明文可见：跳转点 ns.ne.a 硬编码 android.settings.ACCESSIBILITY_SETTINGS；引导弹窗为原生 Dialog（dialog_battery_accessibility_layout.xml）；跳转后遮罩页为本地 Activity + 本地布局 accessibility_toast_view.xml；文案全部来自 res/values/strings.xml。未发现加壳、AES 密文配置或远端 HTML 下发的引导页；assets/privacy.html 与 assets/terms.html 仅为 Google Docs 导出的隐私/条款静态页，不参与无障碍引导。",
  "summary_one_liner": "以“省电优化/防应用自启动”为名，在权限引导页与省电页双入口弹原生对话框索要无障碍，点击后直接跳系统无障碍设置，并在 1 秒后叠压带手指动画的全屏半透明遮罩教学，未授权则每 500ms 轮询并反复重开权限页。",
  "disguise_identity": {
    "app_display_name": "Security Antivirus",
    "claimed_brand_or_persona": "Security Antivirus（自称杀毒/省电优化工具，文案中借“system optimization and phone security”“stop unnecessary app(s)”“boost phone performance more than 50%”塑造系统级安全与性能工具身份）",
    "a11y_service_label": "Security Antivirus（服务 android:label=@string/app_name，即桌面显示名，系统无障碍列表中无“省电/优化”等真实功能描述）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无空白挤出/同形字/多 activity-alias/伪造 isAccessibilityTool。但存在三类身份弱化手法：1) 无障碍服务类名 BatteryOptimizeService 与系统列表展示名 Security Antivirus 分离，用户难以从名称判断其为可读取窗口内容并模拟点击的服务；2) 跳转后用全屏 translucent_dark 遮罩 + 应用图标 + 手指点击动画覆盖在系统无障碍设置之上，形成“类系统引导页”视觉误导；3) android:description 与弹窗文案一致强调“隐私完全安全”，并主动给出“可忽略隐私警告”的免责提示，弱化用户对敏感权限的警觉。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "an.sc.clean.act.smstapge（SplashTheme 启动页）→ an.sc.clean.act.smmain（MainActivity）→ NavigationFragment 导航项",
      "trigger_event": "LAUNCHER 启动进入主界面后，用户点击导航中的权限/安全等级入口（NavigationFragment$1.onClick）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该步无引导文案，仅导航入口图标）",
      "shown_text_zh": "主界面导航项，无文字引导，点击进入权限页",
      "user_action_requested": "点击导航项进入权限/安全等级页；可正常使用其他功能，无强制阻塞",
      "code_anchor": "com.anti.security.view.fragment.NavigationFragment$1.onClick"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.anti.security.activity.GrantPermissonsActivity（layout activity_grant_permission，单实例）",
      "trigger_event": "onCreate → initData() → updateData() → updateView()，页面展示安全等级（basic→Full Protection）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility / System optimization and phone security；Notification / Assist to protect personal information；Usage / Protect app privacy；Please grant all permissions to enhance security level",
      "shown_text_zh": "无障碍——系统优化与手机安全；通知——协助保护个人信息；使用情况——保护应用隐私；请授予全部权限以提升安全等级",
      "user_action_requested": "逐项点击未开启的权限卡片（右侧 ENABLE 按钮或整卡点击）；顶部返回箭头可退出，无强制停留逻辑",
      "code_anchor": "com.anti.security.activity.GrantPermissonsActivity.initData / updateView"
    },
    {
      "step": 3,
      "stage": "引导说明页（省电入口并行分支）",
      "screen_or_component": "an.sc.clean.act.smbatsavsel（activity_battery_select_layout 省电优化页）+ 原生 Dialog an.sc.clean.v.smaccess",
      "trigger_event": "省电页 trySuperSave()/onCreate 检测 BatteryOptimizeService.a() 为 false 时 batteryAccessibilityDialog.show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Security Antivirus / Security Antivirus use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%. / NOT NOW / ENABLE",
      "shown_text_zh": "启用 Security Antivirus / Security Antivirus 使用无障碍功能帮助您停止不必要的应用，可提升电池续航并让手机性能提升 50% 以上 / 暂不 / 启用",
      "user_action_requested": "点击 ENABLE 继续，或点击 NOT NOW 关闭对话框（此时停留在省电页，不跳设置）",
      "code_anchor": "an.sc.clean.v.smaccess.onCreate / dialog_battery_accessibility_layout.xml"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "GrantPermissonsActivity$4.onClick（无障碍卡）或 smbatsavsel.onEnable（对话框 ENABLE）→ ns.ne.a(activity, ACCESS_REQUEST_CODE)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧仅调用 startActivityForResult，不注入界面文字）",
      "shown_text_zh": "直接跳转系统无障碍设置列表，由系统原生界面呈现",
      "user_action_requested": "用户需在系统列表中自行找到并开启“Security Antivirus”服务；应用在此步不做节点自动点击（ne.a 仅置 k=true 标记，实际自动点击由服务运行期 onAccessibilityEvent 触发）",
      "code_anchor": "ns.ne.a  → new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "an.sc.clean.act.smaccessdia（layout accessibility_toast_view，PermissionToastView）",
      "trigger_event": "跳转后 Handler.postDelayed(new GrantPermissonsActivity$4$1, 1000L) 触发 showAccessibilityToast()；省电页由 smbatsavsel$8 同样延迟 1000ms 触发",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Please find and enalbe Security Antivirus for system optimization and phone security.；布局默认文案 To prevent apps from restarting and save battery power, please find and enable Security Antivirus.；按钮 GOT IT",
      "shown_text_zh": "请找到并启用 Security Antivirus 以实现系统优化与手机安全；为防止应用重新启动并节省电量，请找到并启用 Security Antivirus；按钮“知道了”",
      "user_action_requested": "按手指动画指示在系统列表中查找并开启本应用服务，然后点击 GOT IT 关闭遮罩；遮罩全屏覆盖系统设置页，除 GOT IT 外无其他关闭控件",
      "code_anchor": "com.anti.security.activity.GrantPermissonsActivity.showAccessibilityToast / an.sc.clean.act.smaccessdia.onCreate / accessibility_toast_view.xml"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "GrantPermissonsActivity 自身（singleTask，反复 startActivity 重入）",
      "trigger_event": "showAccessibilityToast 末尾 post(checkAcessiblity)；GrantPermissonsActivity$3.run 每 500ms 检查 BatteryOptimizeService.a()；onResume 亦 removeCallbacksAndMessages(null) 后重算",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无新增文案（循环重开权限页，安全等级停留在 basic，仍显示 Please grant all permissions to enhance security level）",
      "shown_text_zh": "未开启则每 500ms 重查并最终重新打开权限页，安全等级保持 basic 并持续提示授予全部权限",
      "user_action_requested": "无跳过/不再提示选项；用户返回后仍会被重开权限页，只能通过开启服务或离开应用中断循环",
      "code_anchor": "com.anti.security.activity.GrantPermissonsActivity$3.run / jumpBackFrombackgroundSetting"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.anti.security.service.BatteryOptimizeService（ns.ne）→ onAccessibilityEvent",
      "trigger_event": "服务启用后收到 typeWindowStateChanged（eventType 32）事件，且 smsaverb.a().d() 为真、包名为 com.android.settings",
      "ui_carrier": "不可静态还原（运行期对系统设置页节点操作，无自定义 UI）",
      "shown_text_verbatim": "无（服务不渲染界面，通过 findAccessibilityNodeInfosByText / findAccessibilityNodeInfosByViewId + performAction(16) 点击节点；并读取 com.android.settings 的 force_stop 字符串）",
      "shown_text_zh": "服务在后台自动检索并点击系统设置页上的按钮节点，包括应用详情页的强制停止",
      "user_action_requested": "无需用户操作；获权后由服务自动执行点击",
      "code_anchor": "ns.ne.onAccessibilityEvent / ns.ne.a(AccessibilityNodeInfo,String[])"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内 NavigationFragment 导航项 → 跳转 GrantPermissonsActivity（无引导文案，仅入口）",
    "GrantPermissonsActivity 列表三张权限卡（activity_grant_permission 布局）：标题与副标题来自 strings.xml 的 acessibility/acessibility_content、notification_usage/notification_content、app_with_usage/app_with_usage_content",
    "GrantPermissonsActivity 顶部安全等级区：security_level_secure/basic/best 与 security_level_tip_basic（“Please grant all permissions to enhance security level”）",
    "省电优化页 smbatsavsel 弹出的不可取消遮罩式原生 Dialog（dialog_battery_accessibility_layout.xml，style upgrade_dialog_style）：enable_dr_security 标题 + battery_permission_desc 正文 + NOT NOW / ENABLE",
    "跳转系统无障碍设置后 1 秒压栈的本地 Activity smaccessdia（accessibility_toast_view.xml）：全屏 translucent_dark 遮罩 + ic_launcher 图标 + tv_content（accessibility_desc 动态传入 / accessibility_toast_text 布局默认）+ RecyclerView 手指点击动画 + GOT IT 按钮",
    "系统无障碍服务列表项：服务 label = @string/app_name（Security Antivirus），描述 = boost_tag_acc_kill_service_description（res/xml/top_accessbility.xml 引用）",
    "跳转使用情况访问权限前弹出的引导 Dialog（ns.nh.a + dialog_usage_guide_content：“Please find and enalbe Security Antivirus for personal information protection.”）与 dialog_usage_content（“Turn on the usage to ensure proper operation of AppLock.”）",
    "跳转悬浮窗权限前弹出的 EnableOverlayDIalog（an.sc.clean.u.smoverlay，EnableClickInterface.onContinue）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please find and enalbe Security Antivirus for system optimization and phone security.",
      "text_zh": "请找到并启用 Security Antivirus，以实现系统优化与手机安全。",
      "source_location": "res/values/strings.xml → key accessibility_desc；由 GrantPermissonsActivity.showAccessibilityToast 作为 extra 传入 smaccessdia",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "To prevent apps from restarting and save battery power, please find and enable Security Antivirus.",
      "text_zh": "为防止应用重新启动并节省电量，请找到并启用 Security Antivirus。",
      "source_location": "res/values/strings.xml → key accessibility_toast_text；accessibility_toast_view.xml 中 tv_content 默认文案",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Security Antivirus",
      "text_zh": "启用 Security Antivirus",
      "source_location": "res/values/strings.xml → key enable_dr_security；dialog_battery_accessibility_layout.xml 标题",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Security Antivirus use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%.",
      "text_zh": "Security Antivirus 使用无障碍功能帮助您停止不必要的应用，可提升电池续航并让手机性能提升 50% 以上。",
      "source_location": "res/values/strings.xml → key battery_permission_desc（formatted=false）；dialog_battery_accessibility_layout.xml 正文",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Security Antivirus only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.\n        You can have the privacy warning ignored.",
      "text_zh": "无障碍可阻止不想要的应用重新打开，也能延长电池寿命与耐用性。Security Antivirus 仅用于优化设备功能，我们保证您的隐私与个人数据完全安全。您可以忽略隐私警告。",
      "source_location": "res/values/strings.xml → key boost_tag_acc_kill_service_description；经 res/xml/top_accessbility.xml 的 android:description 在系统无障碍列表展示",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility",
      "text_zh": "无障碍",
      "source_location": "res/values/strings.xml → key acessibility；GrantPermissonsActivity.initData 列表项标题",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "System optimization and phone security",
      "text_zh": "系统优化与手机安全",
      "source_location": "res/values/strings.xml → key acessibility_content；GrantPermissonsActivity.initData 列表项副标题",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Please grant all permissions to enhance security level",
      "text_zh": "请授予全部权限以提升安全等级",
      "source_location": "res/values/strings.xml → key security_level_tip_basic；GrantPermissonsActivity.updateView",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Please find and enalbe Security Antivirus for personal information protection.",
      "text_zh": "请找到并启用 Security Antivirus，以保护个人信息。",
      "source_location": "res/values/strings.xml → key dialog_usage_guide_content；GrantPermissonsActivity.jumpToUsageSetting 传入 ns.nh.a",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn on the usage to ensure proper operation of AppLock.",
      "text_zh": "开启使用情况访问权限以确保应用锁正常运行。",
      "source_location": "res/values/strings.xml → key dialog_usage_content",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "For full & advanced protection, please enable Security Antivirus's system permission.",
      "text_zh": "为获得完整且高级的保护，请启用 Security Antivirus 的系统权限。",
      "source_location": "res/values/strings.xml → key dialog_usage_content_one",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "NO private data will be collected.",
      "text_zh": "不会收集任何私人数据。",
      "source_location": "res/values/strings.xml → key dialog_usage_content_two",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "GOT IT",
      "text_zh": "知道了",
      "source_location": "res/values/strings.xml → key usage_setting_guide_btn；accessibility_toast_view.xml 中 gotItBtn",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "NOT NOW",
      "text_zh": "暂不",
      "source_location": "res/values/strings.xml → key not_now；dialog_battery_accessibility_layout.xml 中 tv_cancel",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "ENABLE",
      "text_zh": "启用",
      "source_location": "res/values/strings.xml → key enable2；dialog_battery_accessibility_layout.xml 中 tv_enable",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "省电页对话框可点 NOT NOW 关闭且不跳转（仅本次关闭，无持久化“不再提示”标记，下次进入 trySuperSave 仍会 show）。权限引导页点击无障碍卡后进入严格循环：showAccessibilityToast 末尾 post(checkAcessiblity)，GrantPermissonsActivity$3.run 每 500ms 检查 BatteryOptimizeService.a()，未开启则 postDelayed 自身持续轮询；一旦判断分支结束即调用 jumpBackFrombackgroundSetting 以 singleTask 重新 startActivity(GrantPermissonsActivity)，onResume 又 removeCallbacksAndMessages(null) 并重算安全等级。用户从系统设置按返回后同样经 onResume/onActivityResult 重算并停留在权限页，形成“返回即被拉回权限页”的反馈压力。",
    "overlay_or_fake_settings": "是。跳转系统无障碍设置后 1 秒（postDelayed 1000ms）启动本地 Activity smaccessdia，加载 accessibility_toast_view.xml：全屏 translucent_dark maskLayout 覆盖系统设置页，内嵌应用图标、说明文案、RecyclerView 手指点击动画与 GOT IT 按钮，形成类系统引导叠层（非高仿系统开关，而是压栈式半透明遮罩教学）。",
    "restricted_settings_13plus_coaching": "无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、也未发现引导用户进入应用详情右上角菜单允许受限设置的文案或代码路径；预筛的 RESTRICTED_STR / SESSION_INSTALLER 线索未在无障碍引导链中落地。targetSdkVersion=22，本身不受 Android 13 受限设置机制约束。",
    "post_grant_anti_removal": "服务侧具备替代用户在系统设置页操作的能力：ns.ne.onAccessibilityEvent 在 com.android.settings 的 typeWindowStateChanged 事件中，通过 findAccessibilityNodeInfosByViewId（flagReportViewIds）与 findAccessibilityNodeInfosByText 定位节点，ns.ne.a 以 performAction(16) 自动点击；并专门处理 InstalledAppDetailsTop / InstalledAppDetailsActivity 页面及读取系统 force_stop 字符串。静态代码中未发现直接用于阻止自身撤权的专用分支（如监听无障碍页后 GLOBAL_ACTION_BACK 返回），但该自动点击能力可用于关闭他人应用或代点设置项，越出所宣称的省电用途。",
    "benign_graceful_degradation": "无。未发现“仅使用手动清理/ADB 授权/观看模式”等替代路径；未授权时安全等级固定停留在 basic 并持续提示“Please grant all permissions to enhance security level”，无功能降级说明。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条最佳触发点：1) 冷启动进入 MainActivity 后点击导航权限入口，或直接以 am start 拉起 com.anti.security.activity.GrantPermissonsActivity，捕获“三权限卡 + 安全等级”页面；2) 在该页点击无障碍卡（或在省电页点 ENABLE）后立即开始 UTG 连续采集——前 0.5s 捕获 ACTION_ACCESSIBILITY_SETTINGS 跳转，约 1s 后必捕获全屏遮罩引导页 smaccessdia。若监测到 Window 变化包含 com.android.settings 无障碍页 + 随后出现的 translucent_dark 全屏窗口，即为该家族特征窗口序列。",
    "key_pages_to_capture": [
      {
        "page_role": "权限引导页（三权限卡 + 安全等级）",
        "page_identifier": "Activity com.anti.security.activity.GrantPermissonsActivity，标题含“Accessibility / Notification / Usage”三行卡片，右上或顶部显示“Full Protection/basic”等级条",
        "why_most_useful": "该页是全部无障碍引导的调度中心，能一次性看到应用把无障碍与通知、使用情况并列包装为“安全等级”，是判断工具伪装与诱导顺序的关键现场",
        "observable_utg_signals": ["三张权限卡文案 Accessibility / System optimization and phone security", "安全等级提示 Please grant all permissions to enhance security level", "卡片右侧 ENABLE 按钮与整卡可点击区域"]
      },
      {
        "page_role": "省电页原生无障碍请求对话框",
        "page_identifier": "Dialog 窗口（style upgrade_dialog_style）叠加在 an.sc.clean.act.smbatsavsel 之上，标题“Enable Security Antivirus”，按钮 NOT NOW / ENABLE",
        "why_most_useful": "该弹窗把无障碍权限直接包装为“提升续航 50%”的性能承诺，是叙事伪装最直白的一处，且是第二条独立入口",
        "observable_utg_signals": ["对话框标题 Enable Security Antivirus", "正文 boost phone performance more than 50%", "NOT NOW / ENABLE 双按钮"]
      },
      {
        "page_role": "跳转前系统无障碍设置页",
        "page_identifier": "系统设置 Activity（com.android.settings 无障碍列表），列表中出现 label 为“Security Antivirus”的服务项",
        "why_most_useful": "证明应用是直接跳系统无障碍列表而非走应用详情页，同时暴露服务在系统中的展示名与 description，用于比对身份宣称",
        "observable_utg_signals": ["包名 com.android.settings 的窗口", "列表项文本 Security Antivirus", "服务描述含 privacy and personal data is total safe 与 You can have the privacy warning ignored"]
      },
      {
        "page_role": "设置页后约 1 秒压栈的全屏遮罩引导页",
        "page_identifier": "Activity an.sc.clean.act.smaccessdia（全屏 translucent_dark 窗口），含 ic_launcher 图标、手指点击动画区域与 GOT IT 按钮",
        "why_most_useful": "这是该家族最具辨识度的诱导手法：在系统设置页之上压栈半透明遮罩并做手指动画教学，UTG 一旦抓到该窗口序列即可强判定“遮罩叠层指引”",
        "observable_utg_signals": ["窗口类名 an.sc.clean.act.smaccessdia", "全屏半透明遮罩 + 应用图标组合", "GOT IT 按钮文本", "说明文案 please find and enable Security Antivirus", "手指点击动画区域（RecyclerView + hand 图）"]
      },
      {
        "page_role": "拒权后返回的循环重跳现场",
        "page_identifier": "从系统设置返回后再次出现的 GrantPermissonsActivity（singleTask 重入），安全等级仍为 basic",
        "why_most_useful": "通过连续 2-3 次按返回并记录窗口时间戳，可量化 500ms 轮询与 jumpBackFrombackgroundSetting 的重开频率，区分“一次性引导”与“死循环重跳”",
        "observable_utg_signals": ["同一 GrantPermissonsActivity 在短时间内被多次重建（onCreate/onResume 序列）", "无“不再提示”勾选项", "安全等级提示文案持续存在"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：全部引导文案均为可读文本，遮罩页文字为真实 TextView（非图片），无需 OCR。需注意两点：1) 遮罩页的手指教学区域为 RecyclerView + 图片，若只看文本会漏掉“动画教学”语义，需结合窗口叠加与图像特征；2) 该包静态未加壳，运行期 UTG 完全可用；但获权后的服务行为（ns.ne.onAccessibilityEvent 自动点击系统设置节点）无自定义 UI，UTG 只能通过系统设置页上的焦点/点击变化间接观察，需配合无障碍事件日志或 Hook 佐证。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "ns.ne.a(android.app.Activity, int) —— startActivityForResult(\"android.settings.ACCESSIBILITY_SETTINGS\")",
    "com.anti.security.activity.GrantPermissonsActivity.showAccessibilityToast / $3.run / jumpBackFrombackgroundSetting",
    "com.anti.security.activity.GrantPermissonsActivity$4.onClick —— 三权限卡分发（无障碍/USAGE/MANAGE_OVERLAY_PERMISSION）",
    "an.sc.clean.v.smaccess.onCreate + res/layout/dialog_battery_accessibility_layout.xml",
    "an.sc.clean.act.smaccessdia.onCreate + res/layout/accessibility_toast_view.xml",
    "ns.ne.onAccessibilityEvent —— com.android.settings 节点检索与 performAction(16) 自动点击"
  ]
}
```

</details>
