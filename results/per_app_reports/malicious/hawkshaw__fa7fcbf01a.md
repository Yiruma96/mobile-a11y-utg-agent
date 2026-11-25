# MR_177__fa7fcbf01a｜hawkshaw — Idea Security

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：169.8s

## 1. 一句话核心结论

- **核心申请方式**：伪装成安全工具 Idea Security 的 Hawkshaw 远控木马，在登录后立即弹出不可取消的原生 AlertDialog，把用户直接送到系统 ACCESSIBILITY_SETTINGS 页开启其全量窗口读取的无障碍服务，未开启则返回即重弹，并串行索取电池白名单、录屏、通知监听、设备管理器、悬浮窗等权限，获权瞬间用 GLOBAL_ACTION_BACK 关闭设置页。
- **静态可见性说明**：引导链完整静态可见：无加壳、无 AES/Blowfish 加密的引导文案、无远端 HTML 教学页、无 WebView 与悬浮遮罩。仅 Manifest meta-data 中 EMAIL/PASSWORD 使用 Blowfish/CBC 解密（用于登录远控后台），不影响无障碍引导路径的还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fa7fcbf01a252e1f0d3028512e5d58ab18674bc415d4956e28d1e3fea835d724` |
| 包名 / 年份 | `com.demo.testing` / 2021 |
| 家族 / 品类 | **hawkshaw**（同池样本数：48） |
| 原始来源标识 | https://research.checkpoint.com/2021/going-rogue-a-mastermind-behind-android-malware-returns-with-a-new-rat/ |
| 桌面显示名 | Idea Security |
| 引导页宣称品牌/身份 | Idea Security（自称可保护/加固设备安全的工具），内部真实身份为 Hawkshaw 远控木马（命名空间 me.hawkshaw、Firebase 项目 hawkshaw-cae48、类 com.hawkshawspy.MainActivity） |
| 系统无障碍列表服务名 | Idea Security |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.demo.testing 与显示名 Idea Security、内部命名空间 me.hawkshaw 三者不一致；字符串残留 hw_app_name="System Settings" 用于把自身描述成系统组件；无障碍描述仅一句泛化的安全承诺（Accessibility helps us to secure your device），完全不披露读取全部窗口内容、模拟点击、全局返回等实际能力；应用首次授权完成后通过 setComponentEnabledSetting 隐藏桌面图标（SDK<29 分支）并跳回系统设置页。 |
| 无障碍服务类名 | `me.hawkshaw.tasks.Accessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Accessibility helps us to secure your device |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.hawkshawspy.MainActivity（LAUNCHER 入口，布局 2131361820） | onCreate → j()，读取 SharedPreferences 键 IS_PERMISSIONS_GIVEN | 原生Activity | 无 | 无交互，自动跳转；IS_PERMISSIONS_GIVEN 已为 true 时改为隐藏图标并 startActivity(android.settings.SETTINGS) | `com.hawkshawspy.MainActivity#j` |
| 2 | 业务功能触发 | me.hawkshaw.HawkshawMainActivity（布局 activity_main_lib，含 login_form/login/register 控件） | onCreate：setContentView 后检查 Intent extra ForceOpenPermissions 与 IS_PERMISSIONS_GIVEN；随后用 meta-data 中 Blowfish 解密的 EMAIL/PASSWORD 调用 fVar.a(str, str3) 自动登录远控后台 | 原生Activity | **原文**：无（登录表单文案为控件默认，未见额外引导字符串）<br>**译注**：登录/注册界面，用户在此完成账号登录后才会进入权限引导 | 输入账号密码点击登录/注册；若自动登录成功则无需操作 | `me.hawkshaw.HawkshawMainActivity#onCreate / me.hawkshaw.HawkshawMainActivity#a(HawkshawMainActivity)` |
| 3 | 引导说明页 | AlertDialog（AlertDialog.Builder，无自定义布局，系统原生样式） | 登录回调 HawkshawMainActivity$c#b(Boolean=true) → HawkshawMainActivity.a(this,0,1,null)；若 k() 已返回 true 则跳过弹窗直接放行 | 原生Dialog | **原文**：Enable Accessibility Settings / Locate app System Settings and enable accessibility.<br>**译注**：标题「启用无障碍设置」；正文「找到系统设置并开启无障碍功能。」 | 点击 OK 前往系统无障碍设置；点击 Cancel 则关闭弹窗并把结果置 0 继续下一权限步骤。弹窗 setCancelable(false)，点外部与返回键无法关闭 | `me.hawkshaw.HawkshawMainActivity#a(me.hawkshaw.HawkshawMainActivity,int,int,Object) / res/values/strings.xml enable_accessibility_header、enable_accessibility_message` |
| 4 | 跳无障碍设置 | 系统「设置 → 无障碍 → 已安装的服务」列表页（android.settings.ACCESSIBILITY_SETTINGS），其中列表项显示为 Idea Security | 对话框正按钮 onClick（new c(0, i, activity)） | 系统无障碍页 | **原文**：Idea Security / Accessibility helps us to secure your device<br>**译注**：系统无障碍列表显示服务名「Idea Security」，说明为「无障碍功能帮助我们保护您的设备」 | 用户在系统页找到 Idea Security 并把开关打开、在系统二次确认框中点「允许」；此步为真实系统页，无应用叠加内容 | `c#onClick / res/xml/accessibility_service_config.xml / res/values/strings.xml accessibility_service_label、accessibility_service_description` |
| 5 | 拒权反馈循环 | HawkshawMainActivity.onActivityResult(requestCode=0) 再次弹出同一 AlertDialog | 用户从设置页返回触发 onActivityResult；k() 通过 AccessibilityManager.getEnabledAccessibilityServiceList 比对 "包名/me.hawkshaw.tasks.Accessibility" 结果为 false | 原生Dialog | **原文**：Enable Accessibility Settings / Locate app System Settings and enable accessibility.<br>**译注**：原样重复同一「启用无障碍设置」不可取消弹窗，直到用户真正开启服务 | 无跳过路径：只能再次点 OK 回设置页或点 Cancel（Cancel 不结束流程，仅把结果置 0 后继续下一项权限） | `me.hawkshaw.HawkshawMainActivity#onActivityResult (case 0) / me.hawkshaw.HawkshawMainActivity#k` |
| 6 | 获权后动作 | me.hawkshaw.tasks.Accessibility 服务（onServiceConnected），以及紧随其后的 onActivityResult case 1~7 权限流水线 | 系统绑定无障碍服务后回调 onServiceConnected；同时上层流程在 k() 为 true 时调用 j() 请求运行时权限并继续 case 1 起的电池优化/录屏/通知/设备管理器/自启动/悬浮窗 | 系统无障碍页 | **原文**：Enable Read Notifications / Locate System Settings in settings and enable it. Push notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings<br>**译注**：服务一连接即执行 GLOBAL_ACTION_BACK 关闭当前系统页并在 300ms 后继续动作；随后弹出「启用读取通知」说明（称推送能提升体验与学习进度，可随时在应用设置中更改）继续索取通知监听权限 | 用户被要求继续在系统设置中开启通知使用权；无任何提示说明无障碍已可读取全部界面内容与模拟点击 | `me.hawkshaw.tasks.Accessibility#onServiceConnected / me.hawkshaw.HawkshawMainActivity#onActivityResult (case 3)` |
| 7 | 引导说明页（附加权限教学） | AlertDialog「Additional Permissions」，随后跳 android.settings.APPLICATION_DETAILS_SETTINGS | onActivityResult case 7 弹出；正按钮 d#onClick（new d(0, i11, this)）跳应用详情页 | 原生Dialog | **原文**：Please take a look at settings and provide extra permissions if needed.<br> 1. Enable AutoStart.<br> 2. Allow display pop-up window from "Other Permissions".<br> 3. Disable any battery saver for the app.<br> 4. Disable Notifications.<br>**译注**：「请查看设置并在需要时提供额外权限：1. 开启自启动；2. 在“其他权限”中允许显示弹窗；3. 关闭针对本应用的任何电池优化；4. 关闭通知。」（原文末尾的 Disable Notifications 与上下文自相矛盾，疑为复用模板未清理） | 点 OK 进入本应用详情页，按清单手工开启自启动/悬浮窗/关闭省电与通知；点 Cancel 直接进入收尾 | `me.hawkshaw.HawkshawMainActivity#onActivityResult (case 7) / d#onClick / res/values/strings.xml additional_permissions_text` |
| 8 | 获权后动作（收尾隐藏） | onActivityResult default 分支 + MainActivity#j 隐藏图标逻辑 | 权限流水线走完后回调 requestCode 大于 7 的 onActivityResult | 原生Activity | 无 | 无；用户此后无法从桌面图标发现或卸载该应用 | `me.hawkshaw.HawkshawMainActivity#onActivityResult (default) / com.hawkshawspy.MainActivity#j` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- HawkshawMainActivity.a 构建的不可取消原生 AlertDialog：标题 enable_accessibility_header，正文 enable_accessibility_message（res/values/strings.xml 第 61-62 行）
- 系统无障碍列表项：服务标签 accessibility_service_label = Idea Security，描述 accessibility_service_description = Accessibility helps us to secure your device（res/values/strings.xml 第 30-31 行，经 res/xml/accessibility_service_config.xml 引用）
- 同一弹窗在 onActivityResult case 0 的拒权分支中被重复使用，构成返回即重弹的循环呈现
- onActivityResult case 3 硬编码 Java 字符串构成的「Enable Read Notifications」通知监听说明弹窗
- onActivityResult case 7 的「Additional Permissions」弹窗，正文来自 res/values/strings.xml additional_permissions_text（第 32-36 行，含 <b>Other Permissions</b> 富文本）
- 设备管理器授权页说明文案 device_admin_explanation = Click on Activate button to secure your application.（strings.xml 第 60 行，经 ADD_DEVICE_ADMIN 的 EXTRA_ADD_EXPLANATION 传入）
- 自启动引导字符串 enable_auto_start / enable_auto_start_message / error_auto_start（strings.xml 第 63-65 行），用于小米等 OEM 跳转失败时提示
- 应用显示名 app_name = Idea Security（strings.xml 第 39 行），用于桌面图标与系统权限弹窗署名
- 未发现 assets 内 HTML/JS 引导页、远端 WebView 教学页、半透明引导遮罩或高仿系统无障碍开关页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility helps us to secure your device | 无障碍功能帮助我们保护您的设备。 | `res/values/strings.xml: accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用）` | 假反诈安全 |
| en | Enable Accessibility Settings | 启用无障碍设置 | `res/values/strings.xml: enable_accessibility_header（HawkshawMainActivity#a）` | 受限设置分步教学 |
| en | Locate app System Settings and enable accessibility. | 找到本应用的系统设置并开启无障碍功能。 | `res/values/strings.xml: enable_accessibility_message（HawkshawMainActivity#a）` | 受限设置分步教学 |
| en | Please take a look at settings and provide extra permissions if needed.<br> 1. Enable AutoStart.<br> 2. Allow display pop-up window from "Other Permissions".<br> 3. Disable any battery saver for the app.<br> 4. Disable Notifications. | 请查看设置并在需要时提供额外权限：1. 开启自启动；2. 在“其他权限”中允许显示弹窗；3. 关闭针对本应用的任何电池优化；4. 关闭通知。 | `res/values/strings.xml: additional_permissions_text（onActivityResult case 7 的 Additional Permissions 弹窗）` | 清理工具伪装 |
| en | Enable Read Notifications | 启用读取通知 | `me.hawkshaw.HawkshawMainActivity#onActivityResult case 3 硬编码字符串` | 未知 |
| en | Locate System Settings in settings and enable it.<br>Push notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings | 在系统设置中找到并开启它。推送通知能带来更好的使用体验并促进你的学习进度，你可以随时在应用设置中更改。 | `me.hawkshaw.HawkshawMainActivity#onActivityResult case 3 硬编码字符串` | 隐私承诺 |
| en | Click on Activate button to secure your application. | 点击「激活」按钮以保护你的应用。 | `res/values/strings.xml: device_admin_explanation（onActivityResult case 4，ADD_DEVICE_ADMIN 的 EXTRA_ADD_EXPLANATION）` | 假反诈安全 |
| en | Enable Auto Start | 启用自启动 | `res/values/strings.xml: enable_auto_start / enable_auto_start_message` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onActivityResult(requestCode=0) 中 k() 判定 AccessibilityManager 已启用列表不含 "com.demo.testing/me.hawkshaw.tasks.Accessibility" 时，再次调用 HawkshawMainActivity.a(this,0,1,null) 弹出同一个 setCancelable(false) 弹窗；用户从系统设置返回即被重新拦截，Cancel 分支不结束流程而是把结果置 0 后继续进入电池优化等后续权限索取，直到服务真正启用才进入 j() 运行时权限步骤。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 叠加半透明引导遮罩（预筛 overlay 为空与代码一致），也未实现高仿系统无障碍开关页；全部依赖真实系统 ACCESSIBILITY_SETTINGS 页 + 原生 AlertDialog 文字指引。
- **Android 13+ 受限设置（Restricted Settings）应对**：无 Android 13+ 受限设置教学（targetSdkVersion=28，代码中无「允许受限设置」相关文案或 Settings.ACTION 教学）。但 case 7 的 Additional Permissions 步骤会跳 android.settings.APPLICATION_DETAILS_SETTINGS 引导用户手工开启自启动/悬浮窗/关电池优化。Session 安装器绕过在本次核验的引导链中未发现可确认实现。
- **获权后即时行为与防撤权机制**：有。Accessibility#onServiceConnected 在服务连接瞬间执行 performGlobalAction(1)（GLOBAL_ACTION_BACK）并 postDelayed(Accessibility$c, 300ms)，用于关闭刚打开的设置界面并掩盖跳转；配合预筛的 WATCH_SETTINGS / WATCH_PKG_INSTALLER 监听设置页事件、以及 MainActivity 在 SDK<29 时 setComponentEnabledSetting(...,2,1) 隐藏桌面图标，形成阻止用户撤回权限与卸载的机制。
- **良性降级 / 替代方案**：无。未提供手动模式、ADB 指引、仅观看模式等降级路径；未获无障碍权限时流程只会在同一弹窗上循环，不会以功能受限方式继续提供所谓「安全防护」。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 com.hawkshawspy.MainActivity 冷启动后 2 秒内出现 HawkshawMainActivity 的不可取消 AlertDialog（标题 Enable Accessibility Settings）时立即抓取 UI 树；同时在 hook 到 startActivity/startActivityForResult 的 intent action 为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间标记「即将跳转」，跳转前 1 帧与系统页返回后 500ms 各抓一次。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导链全部为系统原生 Dialog/Activity 与真实系统设置页，无图片诱饵、无 WebView、无悬浮遮罩，UTG 可直接读取文本，无显著盲区。唯一需注意：服务连接后 performGlobalAction(BACK) 会在数百毫秒内关闭系统设置页，若采样间隔过长可能错过系统无障碍页的停留画面，建议在跳转 intent hook 后 300ms 内高频抓帧。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（登录成功后立即出现）** | AlertDialog：title=Enable Accessibility Settings，message=Locate app System Settings and enable accessibility.，仅 OK/Cancel 两个按钮，包名 com.demo.testing | 这是整个诱导链唯一由应用自绘的文字载体，能直接证明「以安全为名索取无障碍」以及弹窗不可取消（返回键/点外部无效） | 弹窗标题与正文文本；按钮集合仅 2 个（OK/Cancel）且无「跳过/稍后」；连续按返回键后弹窗仍在（不可取消）；弹窗出现前是否已有登录表单页 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载/已安装的服务，条目文本 Idea Security，副文本 Accessibility helps us to secure your device | 证明系统层面的身份伪装：列表显示的是良性安全品牌而非真实木马名，且描述与真实能力（读取全部窗口内容、模拟点击）严重不符 | 服务条目名称 Idea Security；描述文本 Accessibility helps us to secure your device；对应包名为 com.demo.testing（可通过 adb dumpsys accessibility 交叉核对） |
| **拒权返回后的重弹页** | 从系统设置页按返回后 1 秒内，屏幕再次出现同一 Enable Accessibility Settings 弹窗 | 这是区分「良性透明说明」与「强制诱导」的决定性观察点：良性应用会降级或提供跳过，该样本返回即重弹 | 返回后弹窗重复出现的次数与时间间隔；是否存在任何可跳过路径；取消后是否继续弹出后续权限弹窗（电池优化/录屏） |
| **Additional Permissions 附加权限教学弹窗及跳转后应用详情页** | AlertDialog title=Additional Permissions，正文含 Enable AutoStart / Other Permissions / battery saver / Disable Notifications；OK 后进入 com.demo.testing 的 android.settings.APPLICATION_DETAILS_SETTINGS 页 | 证明权限索取是成套流水线而非单点，并暴露「关闭通知」等自相矛盾文案与 OEM 手工设置教学 | 弹窗四步编号文本；跳转后页面为应用详情页而非系统权限总览；OK/Cancel 之后是否还有新权限弹窗 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `me.hawkshaw.HawkshawMainActivity#a(me.hawkshaw.HawkshawMainActivity,int,int,Object)`
- `c#onClick`
- `me.hawkshaw.HawkshawMainActivity#onActivityResult`
- `me.hawkshaw.HawkshawMainActivity#k`
- `me.hawkshaw.tasks.Accessibility#onServiceConnected`
- `res/values/strings.xml (accessibility_service_label / accessibility_service_description / enable_accessibility_header / enable_accessibility_message / additional_permissions_text)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态可见性：clear）

**一、冷启动即强制引导，无业务前置**
- 启动器 Activity 为 [com.hawkshawspy.MainActivity#j](<resource-unit:#1.dex1 code:com.hawkshawspy.MainActivity#j>)：`IS_PERMISSIONS_GIVEN=false` 时直接 `startActivity(HawkshawMainActivity)`，桌面图标点开就进入授权流水线，而非真实安全功能。
- 引导用 `HawkshawMainActivity` 的 `onCreate` 先走 Firebase 登录/注册表单（`login_form`、`login`/`register` 按钮），登录回调 [HawkshawMainActivity$c#b](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity$c#b>) 成功后立刻进入无障碍弹窗 —— 用户必须先"登录"才看到权限请求。

**二、无障碍弹窗为不可取消的原生 AlertDialog**
- [HawkshawMainActivity#a](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity#a>)：`setCancelable(false)`，标题 `Enable Accessibility Settings`，正文 `Locate app System Settings and enable accessibility.`，只有 OK / Cancel；弹窗前先调 [k()](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity#k>) 用 `getEnabledAccessibilityServiceList` 比对 `包名/me.hawkshaw.tasks.Accessibility`，已开启则静默跳过。
- 正按钮 [c#onClick](<resource-unit:#1.dex1 code:c#onClick>) 直接 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，跳到真实系统页，**无高仿设置页、无悬浮遮罩、无 WebView/HTML 教学页**（预筛 overlay 为空与代码一致）。

**三、拒权循环 + 后续权限流水线**
- [onActivityResult](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity#onActivityResult>) case 0：`k()` 为 false 时再次 `a(this,0,1,null)` 重弹同一个不可取消弹窗，用户从设置页返回即被再次拦截（点 Cancel 也只是把结果置 0 后继续下一步，流程不终止）。
- 同一 switch 链依次串起：电池优化白名单（`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`）→ 屏幕录制 `MediaProjection` → 通知监听（硬编码 `Enable Read Notifications` 弹窗）→ 设备管理器（`ADD_DEVICE_ADMIN`）→ 小米自启动页（`miui.intent.action.APP_PERM_EDITOR`）→ 悬浮窗（`MANAGE_OVERLAY_PERMISSION`）→ `Additional Permissions` 弹窗，其 OK 分支 [d#onClick](<resource-unit:#1.dex1 code:d#onClick>) 跳 `android.settings.APPLICATION_DETAILS_SETTINGS`（用于自启动/弹窗/电池/通知等 OEM 设置，**不是** Android 13+ 受限设置教学）。最终 default 分支写入 `IS_PERMISSIONS_GIVEN=true` 并 finish。

**四、伪装与获权后反移除**
- 桌面名 `Idea Security`、无障碍列表标签 `Idea Security`、描述 `Accessibility helps us to secure your device`，而包名 `com.demo.testing`、内部命名空间 `me.hawkshaw`、Firebase 项目 `hawkshaw-cae48` 均指向 Hawkshaw 远控木马；字符串里还残留 `hw_app_name = System Settings` 这类品牌混淆痕迹。
- [Accessibility#onServiceConnected](<resource-unit:#1.dex1 code:me.hawkshaw.tasks.Accessibility#onServiceConnected>) 一连接即 `performGlobalAction(1)`（GLOBAL_ACTION_BACK）+ 300ms 后 `Accessibility$c`，用于在授权瞬间关闭系统设置界面、掩盖跳转痕迹并配合设置页监听阻止撤权；配置为 `typeAllMask`/`canRetrieveWindowContent=true` 的全量窗口读取。

**五、静态可见性**
无加壳、无加密载荷、无远端 HTML，引导链 100% 可静态还原；引导文案全部来自 `res/values/strings.xml` 与少量硬编码 Java 字符串。

已登记风险：R-001（autonomous_audit / high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链完整静态可见：无加壳、无 AES/Blowfish 加密的引导文案、无远端 HTML 教学页、无 WebView 与悬浮遮罩。仅 Manifest meta-data 中 EMAIL/PASSWORD 使用 Blowfish/CBC 解密（用于登录远控后台），不影响无障碍引导路径的还原。",
  "summary_one_liner": "伪装成安全工具 Idea Security 的 Hawkshaw 远控木马，在登录后立即弹出不可取消的原生 AlertDialog，把用户直接送到系统 ACCESSIBILITY_SETTINGS 页开启其全量窗口读取的无障碍服务，未开启则返回即重弹，并串行索取电池白名单、录屏、通知监听、设备管理器、悬浮窗等权限，获权瞬间用 GLOBAL_ACTION_BACK 关闭设置页。",
  "disguise_identity": {
    "app_display_name": "Idea Security",
    "claimed_brand_or_persona": "Idea Security（自称可保护/加固设备安全的工具），内部真实身份为 Hawkshaw 远控木马（命名空间 me.hawkshaw、Firebase 项目 hawkshaw-cae48、类 com.hawkshawspy.MainActivity）",
    "a11y_service_label": "Idea Security",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.demo.testing 与显示名 Idea Security、内部命名空间 me.hawkshaw 三者不一致；字符串残留 hw_app_name=\"System Settings\" 用于把自身描述成系统组件；无障碍描述仅一句泛化的安全承诺（Accessibility helps us to secure your device），完全不披露读取全部窗口内容、模拟点击、全局返回等实际能力；应用首次授权完成后通过 setComponentEnabledSetting 隐藏桌面图标（SDK<29 分支）并跳回系统设置页。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.hawkshawspy.MainActivity（LAUNCHER 入口，布局 2131361820）",
      "trigger_event": "onCreate → j()，读取 SharedPreferences 键 IS_PERMISSIONS_GIVEN",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见文案，直接以 startActivity 跳转，用户几乎看不到此页",
      "user_action_requested": "无交互，自动跳转；IS_PERMISSIONS_GIVEN 已为 true 时改为隐藏图标并 startActivity(android.settings.SETTINGS)",
      "code_anchor": "com.hawkshawspy.MainActivity#j"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "me.hawkshaw.HawkshawMainActivity（布局 activity_main_lib，含 login_form/login/register 控件）",
      "trigger_event": "onCreate：setContentView 后检查 Intent extra ForceOpenPermissions 与 IS_PERMISSIONS_GIVEN；随后用 meta-data 中 Blowfish 解密的 EMAIL/PASSWORD 调用 fVar.a(str, str3) 自动登录远控后台",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（登录表单文案为控件默认，未见额外引导字符串）",
      "shown_text_zh": "登录/注册界面，用户在此完成账号登录后才会进入权限引导",
      "user_action_requested": "输入账号密码点击登录/注册；若自动登录成功则无需操作",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity#onCreate / me.hawkshaw.HawkshawMainActivity#a(HawkshawMainActivity)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "AlertDialog（AlertDialog.Builder，无自定义布局，系统原生样式）",
      "trigger_event": "登录回调 HawkshawMainActivity$c#b(Boolean=true) → HawkshawMainActivity.a(this,0,1,null)；若 k() 已返回 true 则跳过弹窗直接放行",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Accessibility Settings / Locate app System Settings and enable accessibility.",
      "shown_text_zh": "标题「启用无障碍设置」；正文「找到系统设置并开启无障碍功能。」",
      "user_action_requested": "点击 OK 前往系统无障碍设置；点击 Cancel 则关闭弹窗并把结果置 0 继续下一权限步骤。弹窗 setCancelable(false)，点外部与返回键无法关闭",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity#a(me.hawkshaw.HawkshawMainActivity,int,int,Object) / res/values/strings.xml enable_accessibility_header、enable_accessibility_message"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍 → 已安装的服务」列表页（android.settings.ACCESSIBILITY_SETTINGS），其中列表项显示为 Idea Security",
      "trigger_event": "对话框正按钮 onClick（new c(0, i, activity)）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Idea Security / Accessibility helps us to secure your device",
      "shown_text_zh": "系统无障碍列表显示服务名「Idea Security」，说明为「无障碍功能帮助我们保护您的设备」",
      "user_action_requested": "用户在系统页找到 Idea Security 并把开关打开、在系统二次确认框中点「允许」；此步为真实系统页，无应用叠加内容",
      "code_anchor": "c#onClick / res/xml/accessibility_service_config.xml / res/values/strings.xml accessibility_service_label、accessibility_service_description"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "HawkshawMainActivity.onActivityResult(requestCode=0) 再次弹出同一 AlertDialog",
      "trigger_event": "用户从设置页返回触发 onActivityResult；k() 通过 AccessibilityManager.getEnabledAccessibilityServiceList 比对 \"包名/me.hawkshaw.tasks.Accessibility\" 结果为 false",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Accessibility Settings / Locate app System Settings and enable accessibility.",
      "shown_text_zh": "原样重复同一「启用无障碍设置」不可取消弹窗，直到用户真正开启服务",
      "user_action_requested": "无跳过路径：只能再次点 OK 回设置页或点 Cancel（Cancel 不结束流程，仅把结果置 0 后继续下一项权限）",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity#onActivityResult (case 0) / me.hawkshaw.HawkshawMainActivity#k"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "me.hawkshaw.tasks.Accessibility 服务（onServiceConnected），以及紧随其后的 onActivityResult case 1~7 权限流水线",
      "trigger_event": "系统绑定无障碍服务后回调 onServiceConnected；同时上层流程在 k() 为 true 时调用 j() 请求运行时权限并继续 case 1 起的电池优化/录屏/通知/设备管理器/自启动/悬浮窗",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable Read Notifications / Locate System Settings in settings and enable it. Push notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings",
      "shown_text_zh": "服务一连接即执行 GLOBAL_ACTION_BACK 关闭当前系统页并在 300ms 后继续动作；随后弹出「启用读取通知」说明（称推送能提升体验与学习进度，可随时在应用设置中更改）继续索取通知监听权限",
      "user_action_requested": "用户被要求继续在系统设置中开启通知使用权；无任何提示说明无障碍已可读取全部界面内容与模拟点击",
      "code_anchor": "me.hawkshaw.tasks.Accessibility#onServiceConnected / me.hawkshaw.HawkshawMainActivity#onActivityResult (case 3)"
    },
    {
      "step": 7,
      "stage": "引导说明页（附加权限教学）",
      "screen_or_component": "AlertDialog「Additional Permissions」，随后跳 android.settings.APPLICATION_DETAILS_SETTINGS",
      "trigger_event": "onActivityResult case 7 弹出；正按钮 d#onClick（new d(0, i11, this)）跳应用详情页",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": " Please take a look at settings and provide extra permissions if needed.\n 1. Enable AutoStart.\n 2. Allow display pop-up window from \"Other Permissions\".\n 3. Disable any battery saver for the app.\n 4. Disable Notifications.",
      "shown_text_zh": "「请查看设置并在需要时提供额外权限：1. 开启自启动；2. 在“其他权限”中允许显示弹窗；3. 关闭针对本应用的任何电池优化；4. 关闭通知。」（原文末尾的 Disable Notifications 与上下文自相矛盾，疑为复用模板未清理）",
      "user_action_requested": "点 OK 进入本应用详情页，按清单手工开启自启动/悬浮窗/关闭省电与通知；点 Cancel 直接进入收尾",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity#onActivityResult (case 7) / d#onClick / res/values/strings.xml additional_permissions_text"
    },
    {
      "step": 8,
      "stage": "获权后动作（收尾隐藏）",
      "screen_or_component": "onActivityResult default 分支 + MainActivity#j 隐藏图标逻辑",
      "trigger_event": "权限流水线走完后回调 requestCode 大于 7 的 onActivityResult",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "写入 IS_PERMISSIONS_GIVEN=true 并 finish；下次启动在 SDK<29 时用 setComponentEnabledSetting(componentName, 2, 1) 隐藏桌面图标并跳回系统设置页",
      "user_action_requested": "无；用户此后无法从桌面图标发现或卸载该应用",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity#onActivityResult (default) / com.hawkshawspy.MainActivity#j"
    }
  ],
  "text_presentation_locations": [
    "HawkshawMainActivity.a 构建的不可取消原生 AlertDialog：标题 enable_accessibility_header，正文 enable_accessibility_message（res/values/strings.xml 第 61-62 行）",
    "系统无障碍列表项：服务标签 accessibility_service_label = Idea Security，描述 accessibility_service_description = Accessibility helps us to secure your device（res/values/strings.xml 第 30-31 行，经 res/xml/accessibility_service_config.xml 引用）",
    "同一弹窗在 onActivityResult case 0 的拒权分支中被重复使用，构成返回即重弹的循环呈现",
    "onActivityResult case 3 硬编码 Java 字符串构成的「Enable Read Notifications」通知监听说明弹窗",
    "onActivityResult case 7 的「Additional Permissions」弹窗，正文来自 res/values/strings.xml additional_permissions_text（第 32-36 行，含 <b>Other Permissions</b> 富文本）",
    "设备管理器授权页说明文案 device_admin_explanation = Click on Activate button to secure your application.（strings.xml 第 60 行，经 ADD_DEVICE_ADMIN 的 EXTRA_ADD_EXPLANATION 传入）",
    "自启动引导字符串 enable_auto_start / enable_auto_start_message / error_auto_start（strings.xml 第 63-65 行），用于小米等 OEM 跳转失败时提示",
    "应用显示名 app_name = Idea Security（strings.xml 第 39 行），用于桌面图标与系统权限弹窗署名",
    "未发现 assets 内 HTML/JS 引导页、远端 WebView 教学页、半透明引导遮罩或高仿系统无障碍开关页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility helps us to secure your device",
      "text_zh": "无障碍功能帮助我们保护您的设备。",
      "source_location": "res/values/strings.xml: accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Settings",
      "text_zh": "启用无障碍设置",
      "source_location": "res/values/strings.xml: enable_accessibility_header（HawkshawMainActivity#a）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate app System Settings and enable accessibility.",
      "text_zh": "找到本应用的系统设置并开启无障碍功能。",
      "source_location": "res/values/strings.xml: enable_accessibility_message（HawkshawMainActivity#a）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": " Please take a look at settings and provide extra permissions if needed.\n 1. Enable AutoStart.\n 2. Allow display pop-up window from \"Other Permissions\".\n 3. Disable any battery saver for the app.\n 4. Disable Notifications.",
      "text_zh": "请查看设置并在需要时提供额外权限：1. 开启自启动；2. 在“其他权限”中允许显示弹窗；3. 关闭针对本应用的任何电池优化；4. 关闭通知。",
      "source_location": "res/values/strings.xml: additional_permissions_text（onActivityResult case 7 的 Additional Permissions 弹窗）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Read Notifications",
      "text_zh": "启用读取通知",
      "source_location": "me.hawkshaw.HawkshawMainActivity#onActivityResult case 3 硬编码字符串",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate System Settings in settings and enable it.\nPush notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings",
      "text_zh": "在系统设置中找到并开启它。推送通知能带来更好的使用体验并促进你的学习进度，你可以随时在应用设置中更改。",
      "source_location": "me.hawkshaw.HawkshawMainActivity#onActivityResult case 3 硬编码字符串",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on Activate button to secure your application.",
      "text_zh": "点击「激活」按钮以保护你的应用。",
      "source_location": "res/values/strings.xml: device_admin_explanation（onActivityResult case 4，ADD_DEVICE_ADMIN 的 EXTRA_ADD_EXPLANATION）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Auto Start",
      "text_zh": "启用自启动",
      "source_location": "res/values/strings.xml: enable_auto_start / enable_auto_start_message",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onActivityResult(requestCode=0) 中 k() 判定 AccessibilityManager 已启用列表不含 \"com.demo.testing/me.hawkshaw.tasks.Accessibility\" 时，再次调用 HawkshawMainActivity.a(this,0,1,null) 弹出同一个 setCancelable(false) 弹窗；用户从系统设置返回即被重新拦截，Cancel 分支不结束流程而是把结果置 0 后继续进入电池优化等后续权限索取，直到服务真正启用才进入 j() 运行时权限步骤。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 叠加半透明引导遮罩（预筛 overlay 为空与代码一致），也未实现高仿系统无障碍开关页；全部依赖真实系统 ACCESSIBILITY_SETTINGS 页 + 原生 AlertDialog 文字指引。",
    "restricted_settings_13plus_coaching": "无 Android 13+ 受限设置教学（targetSdkVersion=28，代码中无「允许受限设置」相关文案或 Settings.ACTION 教学）。但 case 7 的 Additional Permissions 步骤会跳 android.settings.APPLICATION_DETAILS_SETTINGS 引导用户手工开启自启动/悬浮窗/关电池优化。Session 安装器绕过在本次核验的引导链中未发现可确认实现。",
    "post_grant_anti_removal": "有。Accessibility#onServiceConnected 在服务连接瞬间执行 performGlobalAction(1)（GLOBAL_ACTION_BACK）并 postDelayed(Accessibility$c, 300ms)，用于关闭刚打开的设置界面并掩盖跳转；配合预筛的 WATCH_SETTINGS / WATCH_PKG_INSTALLER 监听设置页事件、以及 MainActivity 在 SDK<29 时 setComponentEnabledSetting(...,2,1) 隐藏桌面图标，形成阻止用户撤回权限与卸载的机制。",
    "benign_graceful_degradation": "无。未提供手动模式、ADB 指引、仅观看模式等降级路径；未获无障碍权限时流程只会在同一弹窗上循环，不会以功能受限方式继续提供所谓「安全防护」。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 com.hawkshawspy.MainActivity 冷启动后 2 秒内出现 HawkshawMainActivity 的不可取消 AlertDialog（标题 Enable Accessibility Settings）时立即抓取 UI 树；同时在 hook 到 startActivity/startActivityForResult 的 intent action 为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间标记「即将跳转」，跳转前 1 帧与系统页返回后 500ms 各抓一次。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（登录成功后立即出现）",
        "page_identifier": "AlertDialog：title=Enable Accessibility Settings，message=Locate app System Settings and enable accessibility.，仅 OK/Cancel 两个按钮，包名 com.demo.testing",
        "why_most_useful": "这是整个诱导链唯一由应用自绘的文字载体，能直接证明「以安全为名索取无障碍」以及弹窗不可取消（返回键/点外部无效）",
        "observable_utg_signals": ["弹窗标题与正文文本", "按钮集合仅 2 个（OK/Cancel）且无「跳过/稍后」", "连续按返回键后弹窗仍在（不可取消）", "弹窗出现前是否已有登录表单页"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载/已安装的服务，条目文本 Idea Security，副文本 Accessibility helps us to secure your device",
        "why_most_useful": "证明系统层面的身份伪装：列表显示的是良性安全品牌而非真实木马名，且描述与真实能力（读取全部窗口内容、模拟点击）严重不符",
        "observable_utg_signals": ["服务条目名称 Idea Security", "描述文本 Accessibility helps us to secure your device", "对应包名为 com.demo.testing（可通过 adb dumpsys accessibility 交叉核对）"]
      },
      {
        "page_role": "拒权返回后的重弹页",
        "page_identifier": "从系统设置页按返回后 1 秒内，屏幕再次出现同一 Enable Accessibility Settings 弹窗",
        "why_most_useful": "这是区分「良性透明说明」与「强制诱导」的决定性观察点：良性应用会降级或提供跳过，该样本返回即重弹",
        "observable_utg_signals": ["返回后弹窗重复出现的次数与时间间隔", "是否存在任何可跳过路径", "取消后是否继续弹出后续权限弹窗（电池优化/录屏）"]
      },
      {
        "page_role": "Additional Permissions 附加权限教学弹窗及跳转后应用详情页",
        "page_identifier": "AlertDialog title=Additional Permissions，正文含 Enable AutoStart / Other Permissions / battery saver / Disable Notifications；OK 后进入 com.demo.testing 的 android.settings.APPLICATION_DETAILS_SETTINGS 页",
        "why_most_useful": "证明权限索取是成套流水线而非单点，并暴露「关闭通知」等自相矛盾文案与 OEM 手工设置教学",
        "observable_utg_signals": ["弹窗四步编号文本", "跳转后页面为应用详情页而非系统权限总览", "OK/Cancel 之后是否还有新权限弹窗"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导链全部为系统原生 Dialog/Activity 与真实系统设置页，无图片诱饵、无 WebView、无悬浮遮罩，UTG 可直接读取文本，无显著盲区。唯一需注意：服务连接后 performGlobalAction(BACK) 会在数百毫秒内关闭系统设置页，若采样间隔过长可能错过系统无障碍页的停留画面，建议在跳转 intent hook 后 300ms 内高频抓帧。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "me.hawkshaw.HawkshawMainActivity#a(me.hawkshaw.HawkshawMainActivity,int,int,Object)",
    "c#onClick",
    "me.hawkshaw.HawkshawMainActivity#onActivityResult",
    "me.hawkshaw.HawkshawMainActivity#k",
    "me.hawkshaw.tasks.Accessibility#onServiceConnected",
    "res/values/strings.xml (accessibility_service_label / accessibility_service_description / enable_accessibility_header / enable_accessibility_message / additional_permissions_text)"
  ]
}
```

</details>
