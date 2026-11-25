# MR_129__cb1cbb2cad｜hawkshaw — System Settings

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：202.9s

## 1. 一句话核心结论

- **核心申请方式**：伪装为 System Settings 的恶意面板在强制 Firebase 登录后，按 onActivityResult 链依次把用户送往忽略电池优化→无障碍设置→录屏授权→设备管理器→厂商自启动页，并用 Settings.Secure 自检确认 Keylogger 无障碍服务已启用后隐藏桌面图标。
- **静态可见性说明**：全部引导逻辑位于 classes.dex 的 me.baldpanel.activities.HomeActivity 及其内部类，资源位于 resources.arsc 与 res/menu/main_activity.xml、res/xml/accessibility_service_config.xml；无加壳、无 AES/远端 HTML 载荷、无 WebView 或悬浮窗载体，静态可见性完整。仅个别字符串资源（如登录框标题/按钮、设备管理器说明 2131623990）未能从 ARSC 直接解析原文，但对应调用点与控件已定位。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `cb1cbb2cadb2f265b38fae9bad0d622cdf4d7c071924a0346679fb3decafa95c` |
| 包名 / 年份 | `me.bladpanel` / 2021 |
| 家族 / 品类 | **hawkshaw**（同池样本数：48） |
| 原始来源标识 | https://research.checkpoint.com/2021/going-rogue-a-mastermind-behind-android-malware-returns-with-a-new-rat/ |
| 桌面显示名 | System Settings |
| 引导页宣称品牌/身份 | 系统设置（System Settings）；代码内实际自述为 Bald / Bald Quiz 社交答题面板（bald-panel.appspot.com） |
| 系统无障碍列表服务名 | System Settings |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面 label(@7F0E001E)与无障碍服务 label(@7F0E001C)同取 'System Settings'，冒充系统设置；无同形字/空白挤出/多 activity-alias；无障碍配置刻意省略 android:description，使系统无障碍列表不展示任何服务用途说明；获权后 setComponentEnabledSetting(MainActivity, DISABLED) 隐藏启动图标（F()）；无 isAccessibilityTool 伪造 |
| 无障碍服务类名 | `me.baldpanel.tasks.Keylogger` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | me.baldpanel.activities.MainActivity（LAUNCHER） | onCreate | 原生Activity | 无 | 无（自动跳转，用户无感知） | `me.baldpanel.activities.MainActivity#onCreate` |
| 2 | 引导说明页 | HomeActivity 强制登录 AlertDialog（res/layout/login_dialog.xml，含 login_name / login_password 输入框） | HomeActivity.onCreate → p()，检测 FirebaseAuth.getCurrentUser()==null 时弹出 | 原生Dialog | **原文**：title=@string/2131624015（未能解析原文）；positive=2131624014；neutral=2131624027；negative=2131623969<br>**译注**：要求输入面板账号（邮箱）与密码的登录框，是进入后续权限引导的门禁 | 必须登录；setCancelable(false) 不可取消，另有中性/否定按钮（新建账号/取消） | `me.baldpanel.activities.HomeActivity#p / #s` |
| 3 | 获权后动作 | HomeActivity.q() → r()/D()/F()：启用 BootReceiver、上报设备信息、隐藏启动图标 | 登录成功回调 HomeActivity$h.a / HomeActivity$m.a → q() | 通知栏 | **原文**：无（仅 Toast 2131623968）<br>**译注**：静默完成开机自启注册、UUID(HW-<android_id>) 生成与 users/{uid}/apps/{uuid} 信息上报，并禁用 MainActivity 组件隐藏桌面图标 | 无 | `me.baldpanel.activities.HomeActivity#q / #r / #D / #F` |
| 4 | 业务功能触发 | HomeActivity 权限申请回调 → t() → u()：android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS（package:me.bladpanel） | onRequestPermissionsResult → t()；u() 先查 PowerManager.isIgnoringBatteryOptimizations，未豁免则跳系统页 | 系统无障碍页 | **原文**：无（复用系统电池优化豁免页，ADD_EXPLANATION 类文案未自定义）<br>**译注**：跳转系统『忽略电池优化』授权页，为后台常驻做准备 | 在系统页点『允许』；可直接返回，返回后 onActivityResult(0) 仍继续下一步 | `me.baldpanel.activities.HomeActivity#t / #u` |
| 5 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（startActivityForResult，requestCode=1） | onActivityResult(0) → v()；v() 先调用 w() 读取 Settings.Secure.accessibility_enabled 与 enabled_accessibility_services 是否含 me.bladpanel/me.baldpanel.tasks.Keylogger | 系统无障碍页 | **原文**：Enable Accessibility / Enable Accessibility Settings<br>**译注**：『启用无障碍』/『启用无障碍设置』——对应菜单项与引导文案，跳转系统无障碍列表让用户自行打开名为 System Settings 的服务 | 在系统无障碍列表中手动打开该服务开关；无应用内遮罩或高亮指引，无应用内取消按钮 | `me.baldpanel.activities.HomeActivity#v / #w；res/menu/main_activity.xml（item 2131165190）` |
| 6 | 获权后动作 | MediaProjectionManager.createScreenCaptureIntent()（requestCode=2） | onActivityResult(1) → x()（SDK_INT>=21） | 原生Activity | **原文**：无（系统录屏授权弹窗原文由系统提供）<br>**译注**：无障碍授权返回后立即弹系统『开始录制或投射屏幕内容』授权，为持续截屏/录屏做准备 | 点击系统『立即开始』；可拒绝，流程继续 | `me.baldpanel.activities.HomeActivity#x` |
| 7 | 跳受限设置 | android.app.action.ADD_DEVICE_ADMIN（组件 me.baldpanel.receiver.MyDeviceAdminReceiver，label 'Bald Device Admin'，策略含 wipe-data / reset-password / force-lock / disable-camera / encrypted-storage） | onActivityResult(2) → y()；先 isAdminActive 判定 | 原生Activity | **原文**：Enable Device Admin；android.app.extra.ADD_EXPLANATION=@string/2131623990（未能解析原文）<br>**译注**：『启用设备管理器』——引导用户激活设备管理员权限（含远程擦除、改锁屏密码） | 在系统页点『激活』；可取消，流程继续 | `me.baldpanel.activities.HomeActivity#y；res/xml/my_admin.xml` |
| 8 | 跳受限设置 | com.miui.securitycenter/com.miui.permcenter.permissions.PermissionsEditorActivity（miui.intent.action.APP_PERM_EDITOR，extra_pkgname=me.bladpanel） | onActivityResult(3) → z()，仅 Build.MANUFACTURER 含 xiaomi 时执行 | 原生Activity | 无 | 在 MIUI 权限页逐项允许；非小米设备直接跳过 | `me.baldpanel.activities.HomeActivity#z` |
| 9 | 拒权反馈循环 | HomeActivity.A()：按厂商跳 自启动管理页（com.miui.permcenter.autostart.AutoStartManagementActivity / com.coloros.safecenter.permission.startup.StartupAppListActivity / com.vivo.permissionmanager.activity.BgStartUpManagerActivity），找不到则 Toast | onActivityResult(5) → A()；或菜单项 2131165252；A() 先 queryIntentActivities 判定组件是否存在 | 原生Dialog | **原文**：Enable Auto Start / Locate app Bald and enable autostart. / Settings not found, you have to enable auto start from settings for Bald app<br>**译注**：『启用自启动』弹窗（setCancelable(false)）说明『找到 Bald 应用并开启自启动』；若厂商页面不存在则 Toast 提示需自行到设置中为 Bald 应用开启自启动 | 点击『确定』跳厂商自启动页；否定按钮可退出弹窗，但弹窗本身不可取消 | `me.baldpanel.activities.HomeActivity#A；HomeActivity$b#onClick；HomeActivity$c` |
| 10 | 获权后动作 | HomeActivity.F()：禁用 MainActivity 组件并 onBackPressed()，同时写 Firebase user-data/{uid}/{uuid}/app/hidden=true | onActivityResult(default) → F()；或菜单『start』按钮 HomeActivity$j.onClick | 通知栏 | **原文**：无（Toast 2131623968）<br>**译注**：权限链收尾：桌面图标消失、应用从最近任务与启动器视图退场，只留后台无障碍/监听服务运行 | 无 | `me.baldpanel.activities.HomeActivity#F` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- HomeActivity.onCreate→p() 弹出的不可取消 AlertDialog（res/layout/login_dialog.xml），标题/按钮取自 strings 2131624015/2131624014/2131624027/2131623969
- 应用桌面与无障碍列表名称：AndroidManifest application android:label=@7F0E001E 与 Keylogger service android:label=@7F0E001C，均为 'System Settings'
- res/xml/accessibility_service_config.xml：仅 eventTypes/feedbackType/flags/canRetrieveWindowContent，无 android:description（系统无障碍列表中无任何用途说明）
- res/menu/main_activity.xml 选项菜单文案：'Enable Accessibility'、'Enable Auto Start'、'Enable Device Admin'（分别触发 v()/A()/y()）
- HomeActivity.A() 的自启动引导 AlertDialog（setCancelable(false)）：'Enable Auto Start' + 'Locate app Bald and enable autostart.'
- HomeActivity.A() 组件不存在时的 Toast：'Settings not found, you have to enable auto start from settings for Bald app'
- resources.arsc 中未被代码直接引用的同类文案：'Enable Accessibility Settings'、'Locate app Bald and enable accessibility.'
- 系统页面承接：ACCESSIBILITY_SETTINGS、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、MediaProjection、ADD_DEVICE_ADMIN、MIUI PermissionsEditorActivity、厂商自启动页（均为系统/厂商原生页，应用不叠加遮罩）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | System Settings | 系统设置 | `resources.arsc：application android:label=@7F0E001E 与 Keylogger service android:label=@7F0E001C` | 未知 |
| en | Enable Accessibility | 启用无障碍 | `resources.arsc（res/menu/main_activity.xml 菜单项，item id 2131165190 → HomeActivity.v()）` | 受限设置分步教学 |
| en | Enable Accessibility Settings | 启用无障碍设置 | `resources.arsc` | 受限设置分步教学 |
| en | Locate app Bald and enable accessibility. | 找到 Bald 应用并启用无障碍。 | `resources.arsc` | 受限设置分步教学 |
| en | Enable Auto Start | 启用自启动 | `resources.arsc（HomeActivity.A() AlertDialog 标题 2131623995）` | 受限设置分步教学 |
| en | Locate app Bald and enable autostart. | 找到 Bald 应用并开启自启动。 | `resources.arsc（HomeActivity.A() AlertDialog 正文 2131623996）` | 受限设置分步教学 |
| en | Settings not found, you have to enable auto start from settings for Bald app | 未找到相关设置，你需要到系统设置中为 Bald 应用开启自启动 | `resources.arsc（HomeActivity.A() Toast 2131623998）` | 受限设置分步教学 |
| en | Enable Device Admin | 启用设备管理器 | `resources.arsc（HomeActivity.y() 设备管理器 ADD_EXPLANATION 流程 2131623990 关联文案）` | 受限设置分步教学 |
| en | Bald Device Admin | Bald 设备管理器 | `AndroidManifest：receiver me.baldpanel.receiver.MyDeviceAdminReceiver android:label` | 未知 |
| en | Bald Quiz is an intelligent, colorful and entertaining social quiz game where you can challenge your friends and other quizzers to games of trivia | Bald Quiz 是一款智能、多彩、有趣的社交答题游戏，你可以和朋友及其他答题者进行知识竞赛 | `resources.arsc（应用描述字符串，未被界面引用）` | 未知 |
| en | App Uninstalled! | 应用已卸载！ | `resources.arsc` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无 onResume 死循环、无定时器重跳。用户从 ACCESSIBILITY_SETTINGS 返回后走 onActivityResult(1) 直接推进到录屏授权 x()，即使未授权无障碍也不重试、只继续下一权限环节；真正的强制点是登录框（setCancelable(false)）与自启动 AlertDialog（setCancelable(false)），必须点按钮才继续
- **遮罩叠层 / 高仿系统设置页**：无。全部跳转真实系统/厂商页面，未叠半透明遮罩、未做高仿无障碍开关页；应用侧仅用原生菜单项与 AlertDialog 文案提示
- **Android 13+ 受限设置（Restricted Settings）应对**：无。无应用详情页右上角『允许受限设置』教学，无 Session 安装器绕过（targetSdkVersion=21，不触发 13+ 受限设置机制）
- **获权后即时行为与防撤权机制**：未发现自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但获权后立即 setComponentEnabledSetting(MainActivity, DISABLED) 隐藏桌面图标、启用 BootReceiver 开机自启，并写 Firebase app/hidden=true，显著抬高用户撤回与卸载难度
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS（HomeActivity.v()，requestCode=1）的瞬间，或检测到 HomeActivity 弹出 setCancelable(false) 的登录框时即拉起 UTG；另建议在 onActivityResult(1)→MediaProjection 与 ADD_DEVICE_ADMIN 弹窗时各截一次，以证明权限链串联
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本样本无纯图空文本引导，无需 OCR。潜在盲区：①登录门禁需要有效 Firebase 账号才能进入后续权限链，若无法登录则 UTG 只能停在登录框，需预先准备账号或 Hook FirebaseAuth 登录态；②获权后桌面图标被 setComponentEnabledSetting 禁用，UTG 若按包名找启动入口可能失败，应按进程/服务维度追踪；③无障碍事件文本外发走 Firebase Realtime Database 长连接，需同时抓包才能佐证键击外泄。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/登录门禁弹窗页** | HomeActivity 上的 AlertDialog，含两个 EditText（login_name/login_password），无取消能力 | 这是所有权限引导的前置门禁，证明引导并非良性透明说明而是受控面板准入；也是判定恶意主体（Firebase 账号体系）的关键 | Dialog 节点存在且 cancelable=false；存在 2 个 EditText 且无 description 文案；同一 Activity 后续触发系统设置跳转 |
| **系统无障碍服务列表项** | Settings 的 Accessibility 页面，列表中出现名为 'System Settings' 的服务项且无用途描述 | 直接证明身份伪装（应用自称 System Settings）与无障碍配置缺失 description 的实际呈现效果，是诱导用户开启的核心取证点 | 服务项文本 == 'System Settings'；该条目无副标题/说明文本；与桌面图标 label 同名 |
| **跳转前引导弹窗/菜单页** | HomeActivity 选项菜单（Enable Accessibility / Enable Auto Start / Enable Device Admin）与 A() 自启动 AlertDialog | 捕获应用侧主动文案（'Locate app Bald and enable accessibility.'），暴露 Bald 面板真身与 System Settings 伪装的矛盾 | 菜单项文本 'Enable Accessibility'；AlertDialog 文案含 'Bald'；点击后 Activity 切换为系统设置页 |
| **设置页返回后的权限接力页** | MediaProjection 录屏授权弹窗 / ADD_DEVICE_ADMIN 激活页 | 证明无障碍只是链条一环，获权后立刻索取录屏与设备管理员，量化危害等级 | 系统录屏授权弹窗出现在无障碍返回后 <1s；设备管理器激活页显示 'Bald Device Admin' 及擦除数据等策略 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `me.baldpanel.activities.HomeActivity#v`
- `me.baldpanel.activities.HomeActivity#w`
- `me.baldpanel.activities.HomeActivity#onActivityResult`
- `me.baldpanel.activities.HomeActivity#A`
- `me.baldpanel.activities.HomeActivity#F`
- `me.baldpanel.tasks.Keylogger#a(android.view.accessibility.AccessibilityEvent)`
- `res/xml/accessibility_service_config.xml`
- `res/menu/main_activity.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：完整（clear）** — 没有加壳，也没有 AES 或远端 HTML 载荷；无障碍引导流程全部由 `classes.dex` 中的 `HomeActivity` 实现，界面载体都是原生 Dialog、原生 Activity 和系统设置页，没有 WebView 或悬浮窗。

**引导主线（一条串联的 `onActivityResult` 向导，并非冷启动就直接弹出的弹窗）**

1. 冷启动：`MainActivity` 只执行跳转（`startActivity(HomeActivity)` + `finish()`），不会展示任何引导内容。
2. 登录强制限制：`HomeActivity.onCreate → p()` 弹出 `setCancelable(false)` 的 Firebase 邮箱/密码登录框（`login_dialog.xml`）；未登录就无法进入后续流程。这是恶意代码用来控制设备准入和回传的唯一入口。
3. 登录成功后，`q() → r()/D()/F()`：启用 `BootReceiver` 组件以实现开机自启，用 `HW-<android_id>` 生成设备唯一标识，并把 `name/username/timestamp/fcm-token` 写入 `users/{uid}/apps/{uuid}`，最后 `F()` 用 `setComponentEnabledSetting(MainActivity, DISABLED)` 隐藏桌面图标。
4. 权限流程：运行时权限回调 `onRequestPermissionsResult → t() → u()` 跳 `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`（`package:<pkg>`）。
5. 无障碍跳转：`onActivityResult(0)` → `v()`；`v()` 先通过 `w()` 读取 `Settings.Secure.accessibility_enabled` 和 `enabled_accessibility_services` 中是否包含 `me.bladpanel/me.baldpanel.tasks.Keylogger`，如果未开启，才执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1)`。这是全应用**唯一**的无障碍跳转点，并且会先做自我状态检测（已授权则直接跳过）。
6. 获权后自动接力：`onActivityResult(1) → x()` 弹出 MediaProjection 录屏授权 → `y()` 弹出 `ADD_DEVICE_ADMIN` 设备管理器 → `z()` 跳小米 `PermissionsEditorActivity` → `A()` 针对 xiaomi/oppo/vivo 弹自启动页并提示 → `F()` 隐藏图标并 `onBackPressed`。无障碍只是这条权限链的中间环节，并不是终点。
7. 也可手动入口：菜单 `res/menu/main_activity.xml` 中 `2131165190`（Enable Accessibility）、`2131165252`（Enable Auto Start）、`2131165277`（Enable Device Admin）分别调用 `v()`、`A()`、`y()`。

**强制与伪装特征**

- 无障碍本身**没有**遮罩叠层、没有伪造设置页、没有 `onResume` 死循环重跳、也没有 `isAccessibilityTool` 伪造；拒绝后系统设置页可退出，流程会继续走到下一步（无取消按钮的强制仅出现在登录框与自启动弹窗上）。
- 身份错位：桌面名与无障碍服务名均为 **System Settings**（`@7F0E001E`/`@7F0E001C`），而资源中的自述是 “Bald / Bald Quiz” 社交答题应用；引导文案直呼 “Locate app **Bald** and enable accessibility.”，与“系统设置”身份矛盾。
- 无障碍配置（`res/xml/accessibility_service_config.xml`）只有 `accessibilityEventTypes/accessibilityFeedbackType/notificationTimeout/accessibilityFlags/canRetrieveWindowContent`，**没有 `android:description`**，因此在系统无障碍列表中没有任何行为说明。
- 获权后 `Keylogger.onAccessibilityEvent` 会把 TEXT / FOCUSED / CLICKED 事件文本打上时间戳，经 `org.a.a.a.a` 异步写入 Firebase Realtime Database，即完整的键盘与输入内容窃取。

**说明**：本轮按 14 次调用的上限收口，未再追加 `register_evidence_graph`/`record_risk` 写入风险记录；以下事实链可直接作为登记依据（`HomeActivity#v/w/onActivityResult` + `Keylogger#a(AccessibilityEvent)` + `res/xml/accessibility_service_config.xml`）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于 classes.dex 的 me.baldpanel.activities.HomeActivity 及其内部类，资源位于 resources.arsc 与 res/menu/main_activity.xml、res/xml/accessibility_service_config.xml；无加壳、无 AES/远端 HTML 载荷、无 WebView 或悬浮窗载体，静态可见性完整。仅个别字符串资源（如登录框标题/按钮、设备管理器说明 2131623990）未能从 ARSC 直接解析原文，但对应调用点与控件已定位。",
  "summary_one_liner": "伪装为 System Settings 的恶意面板在强制 Firebase 登录后，按 onActivityResult 链依次把用户送往忽略电池优化→无障碍设置→录屏授权→设备管理器→厂商自启动页，并用 Settings.Secure 自检确认 Keylogger 无障碍服务已启用后隐藏桌面图标。",
  "disguise_identity": {
    "app_display_name": "System Settings",
    "claimed_brand_or_persona": "系统设置（System Settings）；代码内实际自述为 Bald / Bald Quiz 社交答题面板（bald-panel.appspot.com）",
    "a11y_service_label": "System Settings",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面 label(@7F0E001E)与无障碍服务 label(@7F0E001C)同取 'System Settings'，冒充系统设置；无同形字/空白挤出/多 activity-alias；无障碍配置刻意省略 android:description，使系统无障碍列表不展示任何服务用途说明；获权后 setComponentEnabledSetting(MainActivity, DISABLED) 隐藏启动图标（F()）；无 isAccessibilityTool 伪造"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "me.baldpanel.activities.MainActivity（LAUNCHER）",
      "trigger_event": "onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面内容，onCreate 立即 startActivity(HomeActivity) 并 finish()",
      "user_action_requested": "无（自动跳转，用户无感知）",
      "code_anchor": "me.baldpanel.activities.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "HomeActivity 强制登录 AlertDialog（res/layout/login_dialog.xml，含 login_name / login_password 输入框）",
      "trigger_event": "HomeActivity.onCreate → p()，检测 FirebaseAuth.getCurrentUser()==null 时弹出",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "title=@string/2131624015（未能解析原文）；positive=2131624014；neutral=2131624027；negative=2131623969",
      "shown_text_zh": "要求输入面板账号（邮箱）与密码的登录框，是进入后续权限引导的门禁",
      "user_action_requested": "必须登录；setCancelable(false) 不可取消，另有中性/否定按钮（新建账号/取消）",
      "code_anchor": "me.baldpanel.activities.HomeActivity#p / #s"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "HomeActivity.q() → r()/D()/F()：启用 BootReceiver、上报设备信息、隐藏启动图标",
      "trigger_event": "登录成功回调 HomeActivity$h.a / HomeActivity$m.a → q()",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "无（仅 Toast 2131623968）",
      "shown_text_zh": "静默完成开机自启注册、UUID(HW-<android_id>) 生成与 users/{uid}/apps/{uuid} 信息上报，并禁用 MainActivity 组件隐藏桌面图标",
      "user_action_requested": "无",
      "code_anchor": "me.baldpanel.activities.HomeActivity#q / #r / #D / #F"
    },
    {
      "step": 4,
      "stage": "业务功能触发",
      "screen_or_component": "HomeActivity 权限申请回调 → t() → u()：android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS（package:me.bladpanel）",
      "trigger_event": "onRequestPermissionsResult → t()；u() 先查 PowerManager.isIgnoringBatteryOptimizations，未豁免则跳系统页",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（复用系统电池优化豁免页，ADD_EXPLANATION 类文案未自定义）",
      "shown_text_zh": "跳转系统『忽略电池优化』授权页，为后台常驻做准备",
      "user_action_requested": "在系统页点『允许』；可直接返回，返回后 onActivityResult(0) 仍继续下一步",
      "code_anchor": "me.baldpanel.activities.HomeActivity#t / #u"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（startActivityForResult，requestCode=1）",
      "trigger_event": "onActivityResult(0) → v()；v() 先调用 w() 读取 Settings.Secure.accessibility_enabled 与 enabled_accessibility_services 是否含 me.bladpanel/me.baldpanel.tasks.Keylogger",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable Accessibility / Enable Accessibility Settings",
      "shown_text_zh": "『启用无障碍』/『启用无障碍设置』——对应菜单项与引导文案，跳转系统无障碍列表让用户自行打开名为 System Settings 的服务",
      "user_action_requested": "在系统无障碍列表中手动打开该服务开关；无应用内遮罩或高亮指引，无应用内取消按钮",
      "code_anchor": "me.baldpanel.activities.HomeActivity#v / #w；res/menu/main_activity.xml（item 2131165190）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "MediaProjectionManager.createScreenCaptureIntent()（requestCode=2）",
      "trigger_event": "onActivityResult(1) → x()（SDK_INT>=21）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（系统录屏授权弹窗原文由系统提供）",
      "shown_text_zh": "无障碍授权返回后立即弹系统『开始录制或投射屏幕内容』授权，为持续截屏/录屏做准备",
      "user_action_requested": "点击系统『立即开始』；可拒绝，流程继续",
      "code_anchor": "me.baldpanel.activities.HomeActivity#x"
    },
    {
      "step": 7,
      "stage": "跳受限设置",
      "screen_or_component": "android.app.action.ADD_DEVICE_ADMIN（组件 me.baldpanel.receiver.MyDeviceAdminReceiver，label 'Bald Device Admin'，策略含 wipe-data / reset-password / force-lock / disable-camera / encrypted-storage）",
      "trigger_event": "onActivityResult(2) → y()；先 isAdminActive 判定",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Enable Device Admin；android.app.extra.ADD_EXPLANATION=@string/2131623990（未能解析原文）",
      "shown_text_zh": "『启用设备管理器』——引导用户激活设备管理员权限（含远程擦除、改锁屏密码）",
      "user_action_requested": "在系统页点『激活』；可取消，流程继续",
      "code_anchor": "me.baldpanel.activities.HomeActivity#y；res/xml/my_admin.xml"
    },
    {
      "step": 8,
      "stage": "跳受限设置",
      "screen_or_component": "com.miui.securitycenter/com.miui.permcenter.permissions.PermissionsEditorActivity（miui.intent.action.APP_PERM_EDITOR，extra_pkgname=me.bladpanel）",
      "trigger_event": "onActivityResult(3) → z()，仅 Build.MANUFACTURER 含 xiaomi 时执行",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳厂商权限编辑页，引导用户为该应用开启全部权限",
      "user_action_requested": "在 MIUI 权限页逐项允许；非小米设备直接跳过",
      "code_anchor": "me.baldpanel.activities.HomeActivity#z"
    },
    {
      "step": 9,
      "stage": "拒权反馈循环",
      "screen_or_component": "HomeActivity.A()：按厂商跳 自启动管理页（com.miui.permcenter.autostart.AutoStartManagementActivity / com.coloros.safecenter.permission.startup.StartupAppListActivity / com.vivo.permissionmanager.activity.BgStartUpManagerActivity），找不到则 Toast",
      "trigger_event": "onActivityResult(5) → A()；或菜单项 2131165252；A() 先 queryIntentActivities 判定组件是否存在",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Auto Start / Locate app Bald and enable autostart. / Settings not found, you have to enable auto start from settings for Bald app",
      "shown_text_zh": "『启用自启动』弹窗（setCancelable(false)）说明『找到 Bald 应用并开启自启动』；若厂商页面不存在则 Toast 提示需自行到设置中为 Bald 应用开启自启动",
      "user_action_requested": "点击『确定』跳厂商自启动页；否定按钮可退出弹窗，但弹窗本身不可取消",
      "code_anchor": "me.baldpanel.activities.HomeActivity#A；HomeActivity$b#onClick；HomeActivity$c"
    },
    {
      "step": 10,
      "stage": "获权后动作",
      "screen_or_component": "HomeActivity.F()：禁用 MainActivity 组件并 onBackPressed()，同时写 Firebase user-data/{uid}/{uuid}/app/hidden=true",
      "trigger_event": "onActivityResult(default) → F()；或菜单『start』按钮 HomeActivity$j.onClick",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "无（Toast 2131623968）",
      "shown_text_zh": "权限链收尾：桌面图标消失、应用从最近任务与启动器视图退场，只留后台无障碍/监听服务运行",
      "user_action_requested": "无",
      "code_anchor": "me.baldpanel.activities.HomeActivity#F"
    }
  ],
  "text_presentation_locations": [
    "HomeActivity.onCreate→p() 弹出的不可取消 AlertDialog（res/layout/login_dialog.xml），标题/按钮取自 strings 2131624015/2131624014/2131624027/2131623969",
    "应用桌面与无障碍列表名称：AndroidManifest application android:label=@7F0E001E 与 Keylogger service android:label=@7F0E001C，均为 'System Settings'",
    "res/xml/accessibility_service_config.xml：仅 eventTypes/feedbackType/flags/canRetrieveWindowContent，无 android:description（系统无障碍列表中无任何用途说明）",
    "res/menu/main_activity.xml 选项菜单文案：'Enable Accessibility'、'Enable Auto Start'、'Enable Device Admin'（分别触发 v()/A()/y()）",
    "HomeActivity.A() 的自启动引导 AlertDialog（setCancelable(false)）：'Enable Auto Start' + 'Locate app Bald and enable autostart.'",
    "HomeActivity.A() 组件不存在时的 Toast：'Settings not found, you have to enable auto start from settings for Bald app'",
    "resources.arsc 中未被代码直接引用的同类文案：'Enable Accessibility Settings'、'Locate app Bald and enable accessibility.'",
    "系统页面承接：ACCESSIBILITY_SETTINGS、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、MediaProjection、ADD_DEVICE_ADMIN、MIUI PermissionsEditorActivity、厂商自启动页（均为系统/厂商原生页，应用不叠加遮罩）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "System Settings",
      "text_zh": "系统设置",
      "source_location": "resources.arsc：application android:label=@7F0E001E 与 Keylogger service android:label=@7F0E001C",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility",
      "text_zh": "启用无障碍",
      "source_location": "resources.arsc（res/menu/main_activity.xml 菜单项，item id 2131165190 → HomeActivity.v()）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Settings",
      "text_zh": "启用无障碍设置",
      "source_location": "resources.arsc",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate app Bald and enable accessibility.",
      "text_zh": "找到 Bald 应用并启用无障碍。",
      "source_location": "resources.arsc",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Auto Start",
      "text_zh": "启用自启动",
      "source_location": "resources.arsc（HomeActivity.A() AlertDialog 标题 2131623995）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate app Bald and enable autostart.",
      "text_zh": "找到 Bald 应用并开启自启动。",
      "source_location": "resources.arsc（HomeActivity.A() AlertDialog 正文 2131623996）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Settings not found, you have to enable auto start from settings for Bald app",
      "text_zh": "未找到相关设置，你需要到系统设置中为 Bald 应用开启自启动",
      "source_location": "resources.arsc（HomeActivity.A() Toast 2131623998）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Device Admin",
      "text_zh": "启用设备管理器",
      "source_location": "resources.arsc（HomeActivity.y() 设备管理器 ADD_EXPLANATION 流程 2131623990 关联文案）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Bald Device Admin",
      "text_zh": "Bald 设备管理器",
      "source_location": "AndroidManifest：receiver me.baldpanel.receiver.MyDeviceAdminReceiver android:label",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Bald Quiz is an intelligent, colorful and entertaining social quiz game where you can challenge your friends and other quizzers to games of trivia",
      "text_zh": "Bald Quiz 是一款智能、多彩、有趣的社交答题游戏，你可以和朋友及其他答题者进行知识竞赛",
      "source_location": "resources.arsc（应用描述字符串，未被界面引用）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "App Uninstalled!",
      "text_zh": "应用已卸载！",
      "source_location": "resources.arsc",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无 onResume 死循环、无定时器重跳。用户从 ACCESSIBILITY_SETTINGS 返回后走 onActivityResult(1) 直接推进到录屏授权 x()，即使未授权无障碍也不重试、只继续下一权限环节；真正的强制点是登录框（setCancelable(false)）与自启动 AlertDialog（setCancelable(false)），必须点按钮才继续",
    "overlay_or_fake_settings": "无。全部跳转真实系统/厂商页面，未叠半透明遮罩、未做高仿无障碍开关页；应用侧仅用原生菜单项与 AlertDialog 文案提示",
    "restricted_settings_13plus_coaching": "无。无应用详情页右上角『允许受限设置』教学，无 Session 安装器绕过（targetSdkVersion=21，不触发 13+ 受限设置机制）",
    "post_grant_anti_removal": "未发现自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但获权后立即 setComponentEnabledSetting(MainActivity, DISABLED) 隐藏桌面图标、启用 BootReceiver 开机自启，并写 Firebase app/hidden=true，显著抬高用户撤回与卸载难度",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS（HomeActivity.v()，requestCode=1）的瞬间，或检测到 HomeActivity 弹出 setCancelable(false) 的登录框时即拉起 UTG；另建议在 onActivityResult(1)→MediaProjection 与 ADD_DEVICE_ADMIN 弹窗时各截一次，以证明权限链串联",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/登录门禁弹窗页",
        "page_identifier": "HomeActivity 上的 AlertDialog，含两个 EditText（login_name/login_password），无取消能力",
        "why_most_useful": "这是所有权限引导的前置门禁，证明引导并非良性透明说明而是受控面板准入；也是判定恶意主体（Firebase 账号体系）的关键",
        "observable_utg_signals": ["Dialog 节点存在且 cancelable=false", "存在 2 个 EditText 且无 description 文案", "同一 Activity 后续触发系统设置跳转"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 的 Accessibility 页面，列表中出现名为 'System Settings' 的服务项且无用途描述",
        "why_most_useful": "直接证明身份伪装（应用自称 System Settings）与无障碍配置缺失 description 的实际呈现效果，是诱导用户开启的核心取证点",
        "observable_utg_signals": ["服务项文本 == 'System Settings'", "该条目无副标题/说明文本", "与桌面图标 label 同名"]
      },
      {
        "page_role": "跳转前引导弹窗/菜单页",
        "page_identifier": "HomeActivity 选项菜单（Enable Accessibility / Enable Auto Start / Enable Device Admin）与 A() 自启动 AlertDialog",
        "why_most_useful": "捕获应用侧主动文案（'Locate app Bald and enable accessibility.'），暴露 Bald 面板真身与 System Settings 伪装的矛盾",
        "observable_utg_signals": ["菜单项文本 'Enable Accessibility'", "AlertDialog 文案含 'Bald'", "点击后 Activity 切换为系统设置页"]
      },
      {
        "page_role": "设置页返回后的权限接力页",
        "page_identifier": "MediaProjection 录屏授权弹窗 / ADD_DEVICE_ADMIN 激活页",
        "why_most_useful": "证明无障碍只是链条一环，获权后立刻索取录屏与设备管理员，量化危害等级",
        "observable_utg_signals": ["系统录屏授权弹窗出现在无障碍返回后 <1s", "设备管理器激活页显示 'Bald Device Admin' 及擦除数据等策略"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本样本无纯图空文本引导，无需 OCR。潜在盲区：①登录门禁需要有效 Firebase 账号才能进入后续权限链，若无法登录则 UTG 只能停在登录框，需预先准备账号或 Hook FirebaseAuth 登录态；②获权后桌面图标被 setComponentEnabledSetting 禁用，UTG 若按包名找启动入口可能失败，应按进程/服务维度追踪；③无障碍事件文本外发走 Firebase Realtime Database 长连接，需同时抓包才能佐证键击外泄。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "me.baldpanel.activities.HomeActivity#v",
    "me.baldpanel.activities.HomeActivity#w",
    "me.baldpanel.activities.HomeActivity#onActivityResult",
    "me.baldpanel.activities.HomeActivity#A",
    "me.baldpanel.activities.HomeActivity#F",
    "me.baldpanel.tasks.Keylogger#a(android.view.accessibility.AccessibilityEvent)",
    "res/xml/accessibility_service_config.xml",
    "res/menu/main_activity.xml"
  ]
}
```

</details>
