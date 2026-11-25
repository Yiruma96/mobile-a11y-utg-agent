# MR_139__e3f77ff093｜Riltok — Leboncoin

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：119.8s

## 1. 一句话核心结论

- **核心申请方式**：由常驻服务 StDlgSrs 定时器在无障碍未开启时反复拉起不可取消的“Google Play Services 已停止”恐吓弹窗，单按钮 OK 一步直跳系统无障碍设置，获权后用“Google Services 已成功启用”提示并把用户踢回桌面，服务端再自动点击设置页条目完成自启与防撤权。
- **静态可见性说明**：无障碍诱导链路（StDlgSrs 定时器→StartDialog 不可取消弹窗→ACTION_ACCESSIBILITY_SETTINGS 跳转→AccOnDialog 成功提示→HOME 回桌面）在 DEX 中完全静态可见；不可静态还原的部分为：设置包名与冷启动 WebView URL 由 librealtalk-jni.so 的 JNI 方法 getSettingsPackageFromJNI/getXiaomiSettingsPackageFromJNI/getStartWebUrl 运行期返回，以及 WbActivity 加载的远端钓鱼 HTML。ae.e() 内部实现未逐字反编译，其行为由唯一调用点与 aa.a() 前置判定推断。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e3f77ff093f322e139940b33994c5a57ae010b66668668dc4945142a81bcc049` |
| 包名 / 年份 | `com.pandar` / 2019 |
| 家族 / 品类 | **Riltok**（同池样本数：9） |
| 原始来源标识 | https://securelist.com/mobile-banker-riltok/91374/ |
| 桌面显示名 | Leboncoin |
| 引导页宣称品牌/身份 | Google Play Services / Google Services（系统服务身份），并使用 Leboncoin 品牌作为桌面外壳 |
| 系统无障碍列表服务名 | Google Services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务声明 res/xml/service_conf.xml 完全省略 android:description，系统列表无任何用途说明与警告，仅显示“Google Services”标签；应用名 Leboncoin 与服务名 Google Services 分属两个互不相关的品牌；多个组件进程/名称伪造成 com.googleplay.activities.AdminRequestDialog、com.googleplay.srs.CmndSrs 等；设备管理器标签伪造成 Play Market；StartDialog/AccOnDialog 使用 Theme.Translucent.NoTitleBar 悬浮式呈现，不进入正常 Activity 栈视觉流；字符串资源以无语义 key（cziugqk、ldbib、ohygeztvjm）与空值资源混淆真实文案。 |
| 无障碍服务类名 | `com.pandar.srs.GPSrs` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_SMS, RECEIVE_SMS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.pandar.MainActivity → com.pandar.wb.WbActivity | 用户点击桌面图标 Leboncoin 触发 MainActivity.onCreate | 远端WebView | **原文**：无（页面内容来自 Relactive.getStartWebUrl() 返回的远端 URL）<br>**译注**：启动后直接展示远端网页，随即 finish() 退出自身，无原生引导界面 | 无明确引导动作；应用完成初始化后即跳转网页 | `com.pandar.MainActivity.onCreate / aviasalea.ae.a(Context,String) / com.pandar.wb.WbActivity` |
| 2 | 业务功能触发 | com.pandar.srs.StDlgSrs（后台常驻服务，action=com.googleplay.srs.StDlgSrs）→ com.pandar.ds.StartDialog | StDlgSrs 内 TimerTask 周期触发 StDlgSrs$a.run：aa.a(context) 判定无障碍未开启则 ae.e(context) 拉起 StartDialog | 原生Activity | **原文**：无（本步仅为拉起动作）<br>**译注**：后台定时检测无障碍开关，未开启即弹出引导弹窗，不依赖用户在前台操作 | 无（用户无感知） | `com.pandar.srs.StDlgSrs$a.run / aviasalea.aa.a(Context) / aviasalea.ae.e(Context)` |
| 3 | 引导说明页 | com.pandar.ds.StartDialog（android:theme=Theme.Translucent.NoTitleBar）内的不可取消 AlertDialog | StartDialog.onCreate → b() 构建 aviasalea.w$b 对话框并 show() | 原生Dialog | **原文**：Attention \| Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: \| OK<br>**译注**：“注意” \| “很遗憾，Google Play 服务已停止。为保证设备正常运行，请在菜单中选择一行并自行启用：” \| “确定” | 仅可点击 OK 继续；setCancelable(false) 且 setCanceledOnTouchOutside(false)，无取消/跳过按钮，返回键无法关闭 | `com.pandar.ds.StartDialog.b / @string/start_dialog_warning / @string/start_dialog_description` |
| 4 | 跳无障碍设置 | 系统页 Settings.ACTION_ACCESSIBILITY_SETTINGS（无障碍服务列表） | StartDialog$1.onClick（OK 按钮）→ aa.a() 未开启 → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Google Services（系统列表中该服务条目的 label）<br>**译注**：系统无障碍列表中呈现为“Google Services”，无用途说明文字（service_conf.xml 未声明 android:description） | 要求用户在该列表中手动找到并开启“Google Services”开关 | `com.pandar.ds.StartDialog$1.onClick / res/xml/service_conf.xml / @string/accessibilityservice_label` |
| 5 | 遮罩叠层指引 | com.pandar.srs.GPSrs（无障碍服务）在设置页内的事件处理 + com.pandar.injs.g.GActivity | GPSrs 收到设置页 TYPE_WINDOW_* 事件 → aa.a(Context, AccessibilityNodeInfo, aa$a)：包名匹配 getSettingsPackageFromJNI()/getXiaomiSettingsPackageFromJNI() 且节点文本匹配 2131361806/2131361810/2131361816（含“Google Services”）→ aa_a.a() | 系统无障碍页 | **原文**：Google Services<br>**译注**：服务在系统设置页内自动定位并点击自身条目/确认按钮，完成自启用；isHardMode 且前台为当前包时另拉起 GActivity 接管界面 | 用户仅需进入设置页，点击与确认动作由无障碍服务代劳 | `aviasalea.aa.a(Context,AccessibilityNodeInfo,aa$a) / aviasalea.ae.d(Context) / com.pandar.injs.g.GActivity` |
| 6 | 获权后动作 | com.pandar.ds.AccOnDialog | 无障碍已启用后由 GPSrs 链路拉起 AccOnDialog.onCreate → b() 弹窗 | 原生Dialog | **原文**：Google Services \| Google Service was successfully enabled \| OK<br>**译注**：“Google Services” \| “Google 服务已成功启用” \| “确定” | 点击 OK；AccOnDialog$1.onClick 调 ae.h(context) 发送 ACTION_MAIN+CATEGORY_HOME 把用户直接送回桌面，无取消按钮 | `com.pandar.ds.AccOnDialog.b / com.pandar.ds.AccOnDialog$1.onClick / aviasalea.ae.h(Context) / @string/dlg_acc_on_desc` |
| 7 | 拒权反馈循环 | StDlgSrs TimerTask → StartDialog（重复弹出） | 用户从设置页返回但未开启权限，或点击返回键；StDlgSrs 定时器下一轮 aa.a() 仍为 false → 再次 ae.e(context) | 原生Activity | **原文**：Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable:<br>**译注**：同一恐吓弹窗被反复重新拉起，直至用户开启无障碍 | 无任何降级/跳过出口，只能开启或反复遭遇弹窗 | `com.pandar.srs.StDlgSrs$a.run / aviasalea.aa.a(Context)` |
| 8 | 获权后动作 | GPSrs 对任意前台包的窗口事件处理 → com.pandar.wb.WbActivity | aa.a(Context,AccessibilityNodeInfo,aa$a) 中 wb.c.b(currentPackage) 返回非空 → ae.a(context, url, package) 打开 WbActivity | 远端WebView | **原文**：无（URL 与页面内容均为远端下发，本地仅有信用卡表单字符串资源）<br>**译注**：在银行/支付类应用前台时弹出对应伪造网页覆盖界面 | 在伪造页面中提交卡片等凭据 | `aviasalea.aa.a(Context,AccessibilityNodeInfo,aa$a) / com.pandar.wb.c.b / aviasalea.ae.a(Context,String,String)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- StartDialog（Theme.Translucent.NoTitleBar，悬浮式不可取消 AlertDialog）：标题“Attention”，正文“Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable:”，仅“OK”按钮；setCancelable(false)、setCanceledOnTouchOutside(false)
- AccOnDialog（Theme.Translucent.NoTitleBar，不可取消 AlertDialog）：标题“Google Services”，正文“Google Service was successfully enabled”，仅“OK”按钮
- 系统无障碍服务列表条目：仅显示 label“Google Services”（@string/accessibilityservice_label），res/xml/service_conf.xml 未声明 android:description，列表内无任何用途说明或警告
- 设备管理器激活页：@string/admin_title “Click on Activate button to secure your application.”，label 伪造成“Play Market”（@string/admin_device_label）
- 远端 WebView（WbActivity）：URL 由 Relactive.getStartWebUrl()/wb.c.b(package) 提供，页面内容不在包内，无法静态呈现
- 本地字符串资源中预留的钓鱼话术：@string/Caption “Confirm credit card data”、@string/DescCaption “Enter credit card information to verify your billing data”
- 未发现本地 HTML/asset 引导页，也未发现引导遮罩类 Overlay 布局资源

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Attention | 注意 | `@string/start_dialog_warning（StartDialog.b 对话框标题）` | 故障恐吓 |
| en | Unfortunately Google Play Services has stopped.<br>For the correct operation of the device select a line in the menu and self-enable: | 很遗憾，Google Play 服务已停止。为保证设备正常运行，请在菜单中选择一行并自行启用： | `@string/start_dialog_description（StartDialog.b 对话框正文）` | 假更新 |
| en | Google Service was successfully enabled | Google 服务已成功启用 | `@string/dlg_acc_on_desc（AccOnDialog.b 对话框正文）` | 假更新 |
| en | Google Services | Google 服务 | `@string/accessibilityservice_label（无障碍服务 label，也是系统列表与 AccOnDialog 标题）` | 未知 |
| en | Click on Activate button to secure your application. | 点击“激活”按钮以保护您的应用。 | `@string/admin_title（设备管理器 ADD_DEVICE_ADMIN 说明，aviasalea.ae.a(ComponentName,Activity)）` | 假反诈安全 |
| en | Play Market | Play 商店 | `@string/admin_device_label（com.pandar.rcs.AdReceiver 设备管理器 label）` | 未知 |
| en | Confirm credit card data | 确认信用卡信息 | `@string/Caption` | 未知 |
| en | Enter credit card information to verify your billing data | 请输入信用卡信息以验证您的账单数据 | `@string/DescCaption` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：StDlgSrs 的 TimerTask 周期性执行 StDlgSrs$a.run，每次先以 aa.a(context) 读取 Settings.Secure 的 accessibility_enabled 与 enabled_accessibility_services 判断 com.pandar/com.pandar.srs.GPSrs 是否已启用；未启用则再次 ae.e(context) 拉起 StartDialog。用户从设置页返回或关闭弹窗后仍会被下一次定时任务重新弹出，直到开启无障碍；无降级路径。
- **遮罩叠层 / 高仿系统设置页**：未发现自绘高仿系统无障碍开关页或半透明引导遮罩布局；改用 Theme.Translucent.NoTitleBar 的悬浮式不可取消 AlertDialog 覆盖在任意前台应用之上，并配合 GActivity（isHardMode 且前台为当前包时拉起）接管界面。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=19（minSdk 14），不含 Android 13 受限设置分步教学，也未使用 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：有。GPSrs 在无障碍事件中比对设置包（getSettingsPackageFromJNI/getXiaomiSettingsPackageFromJNI）与节点文本（2131361806/2131361810/2131361816，含“Google Services”），命中即回调 aa_a.a() 在设置页内自动点击确认/启用自身；同时 aviasalea.ae.h() 以 ACTION_MAIN+CATEGORY_HOME 强制回桌面、ae.d() 拉起 GActivity 接管前台，阻止用户在设置页停留撤权；另有 RestartService 监听 BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED 等广播维持服务存活。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条并行触发：①监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（即 StartDialog$1.onClick 执行瞬间，通常在冷启动后数秒内由 StDlgSrs 定时器触发）；②监测到 com.pandar.ds.StartDialog 或 com.pandar.ds.AccOnDialog 这两个 Translucent 主题 Activity 的 onResume。建议在安装后静置 10–60 秒并在前台打开任意其他应用，等待后台弹窗自行浮出。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图空文本诱导，文案均为原生字符串，UTG 可直接提取。盲区在于：①系统设置页内由无障碍服务代点的自启用动作发生在系统 Settings 进程界面，UTG 需持续跟踪设置页节点变化而非只看本应用页面；②冷启动与诱饵页面内容（getStartWebUrl、wb.c.b(package) 返回的钓鱼 URL 及其 HTML）由 librealtalk-jni.so 与远端下发，纯静态不可见，需流量侧配合；③本样本未加壳，运行期 UTG 不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **后台浮出的冷启动式恐吓引导弹窗页** | 标题“Attention”、正文含“Unfortunately Google Play Services has stopped”、仅“OK”按钮、无取消按钮、页面无标题栏且覆盖在其他应用之上 | 这是判定“诱导”的核心证据页：可同时验证无取消出口、伪造 Google 服务身份、故障恐吓话术三要素，且能确认其由后台服务而非用户操作触发 | 按钮集合仅含 OK，缺失 Cancel/关闭；文本含 Google Play Services 与 stopped 的故障恐吓组合；弹窗出现时前台并非本应用（覆盖层判定）；Activity 名为 com.pandar.ds.StartDialog |
| **系统无障碍服务列表项** | 列表内条目文本恰为“Google Services”，其下无任何说明/警告文字，与桌面应用名 Leboncoin 不一致 | 直接证明身份冒充与描述缺失（service_conf.xml 无 android:description），是“用户无法知情其授权对象”的关键证据 | 条目文本=Google Services 且无 description 子行；开关状态变化后服务立即被点击确认（自启用） |
| **获权后成功提示页（并伴随强制回桌面）** | 标题“Google Services”、正文“Google Service was successfully enabled”、仅 OK；点击后前台瞬间变为桌面 Launcher | 验证获权后的痕迹清理动作（HOME Intent）与自确认完成，区分“用户手动开启”与“服务代点开启” | 点击 OK 后前台包立即变为 launcher；弹窗 Activity=com.pandar.ds.AccOnDialog；无取消按钮 |
| **拒绝授权后的复现循环页** | 从系统设置返回或按返回键后，同一“Attention”弹窗在数秒内再次出现 | 确认拒绝循环机制（定时器重拉），是判定强制性的直接运行证据 | 同一弹窗文本在短时间内重复出现次数；返回键/点击外部无法消除弹窗；两次弹窗间隔近似固定定时周期 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.pandar.ds.StartDialog.b`
- `com.pandar.ds.StartDialog$1.onClick`
- `com.pandar.srs.StDlgSrs$a.run`
- `aviasalea.aa.a(Context)`
- `aviasalea.aa.a(Context,AccessibilityNodeInfo,aa$a)`
- `com.pandar.ds.AccOnDialog$1.onClick / aviasalea.ae.h(Context)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（基于 17 次工具调用后的定向核验结果）

**一、无障碍权限引导的整体形态：通过后台定时器弹出不可取消的“系统故障”弹窗，再一键跳转到系统无障碍设置页**

- 引导弹窗并非由桌面图标启动后的前台页面弹出，而是由常驻服务 [StDlgSrs$a.run()](<resource-unit:#1.dex1 code:com.pandar.srs.StDlgSrs$a#run>) 的 `TimerTask` 周期性拉起：它先调用 `aa.a(context)` 判断 `accessibility_enabled` 与 `enabled_accessibility_services` 中是否已包含 `com.pandar/com.pandar.srs.GPSrs`；如果未包含，就调用 `ae.e(context)` 拉起 [StartDialog](<resource-unit:#1.dex1 code:com.pandar.ds.StartDialog>)，该 Activity 使用 `Theme.Translucent.NoTitleBar`。
- 弹窗由 [StartDialog.b()](<resource-unit:#1.dex1 code:com.pandar.ds.StartDialog#b>) 构建，**只有 “OK” 一个按钮**，并且 `setCancelable(false)` 与 `setCanceledOnTouchOutside(false)` 同时生效，因此用户无法取消，也不能点外部关闭。
- 用户点击 OK 后，[StartDialog$1.onClick()](<resource-unit:#1.dex1 code:com.pandar.ds.StartDialog$1#onClick>) 会先再次检查是否已获得权限（已获得则静默 return），否则直接执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，**整个引导过程没有说明页、没有前置教学页、也没有本地 HTML**，只有一步就从恐吓弹窗跳到系统设置。
- 从设置页返回后，如果仍未开启权限，`aa.a()` 仍然返回 false，于是 StDlgSrs 的定时任务会再次弹出同一弹窗，形成**拒绝授权后反复弹出的循环**；代码中没有降级或跳过路径。

**二、获权后的“成功提示”与痕迹清理**

- 获权后由 [AccOnDialog](<resource-unit:#1.dex1 code:com.pandar.ds.AccOnDialog>) 展示“Google Services / Google Service was successfully enabled”。点击 OK 后，[AccOnDialog$1.onClick()](<resource-unit:#1.dex1 code:com.pandar.ds.AccOnDialog$1#onClick>) 调用 [ae.h()](<resource-unit:#1.dex1 code:aviasalea.ae#h>)，向 HOME 发送 Intent（`ACTION_MAIN` + `CATEGORY_HOME`），**直接把用户送回桌面**，从而消除弹窗与设置页的残留画面；这个 HOME 动作同样被 GPSrs 复用。
- 在无障碍服务侧，[aa.a(Context, AccessibilityNodeInfo, aa$a)](<resource-unit:#1.dex1 code:aviasalea.aa#a>) 会持续监听设置包（包名由 `Relactive.getSettingsPackageFromJNI()` 和 `getXiaomiSettingsPackageFromJNI()` 从原生库返回），并在节点文本匹配 `2131361806/2131361810/2131361816`（包含 “Google Services” 等标签）时触发回调 `aa_a.a()`，也就是说，服务会**在系统设置页内自动点击或确认自身条目**；结合 `isHardMode` 与 `isCurPackage` 判断，它会拉起 [GActivity](<resource-unit:#1.dex1 code:com.pandar.injs.g.GActivity>)，拦截对“当前前台包”的操作，从而阻止用户撤回权限。
- 此外，`GPSrs` 的 `onAccessibilityEvent` 对任意前台包调用 `wb.c.b(package)`，取得钓鱼 URL 后通过 [ae.a(Context, String, String)](<resource-unit:#1.dex1 code:aviasalea.ae#a>) 打开 WbActivity；这说明该权限的用途是覆盖银行应用并注入伪造页面，而非单纯完成引导。

**三、身份伪装与文本呈现位置**

- 桌面名 `Leboncoin`（真实法国分类信息品牌）与无障碍服务名 `Google Services` 完全不对应；`res/xml/service_conf.xml` **没有任何 `android:description` 属性**，因此系统无障碍列表只显示 “Google Services”，没有任何用途说明，也没有警告文字可以平衡。
- 引导文案全为**系统故障恐吓 + 教唆用户自行开启**：“Unfortunately Google Play Services has stopped…select a line in the menu and self-enable”，并以 “Attention” 作为标题。
- 冷启动首页并不是引导页：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.pandar.MainActivity#onCreate>) 直接调用 `Relactive.getStartWebUrl()`（JNI 原生返回）打开远端 WebView 后 `finish()`；信用卡话术（“Confirm credit card data / Enter credit card information to verify your billing data”）属于后续钓鱼页面，不在无障碍引导链路内。

**四、可见性与边界**

- 无障碍引导本身**完全静态可见**（Activity、Dialog、Intent、字符串均可还原）；无法静态还原的部分是：`getStartWebUrl()`、`getSettingsPackageFromJNI()` 等由 `librealtalk-jni.so` 提供的原生返回值，以及远端 WebView 的 HTML 内容。

> 说明：本轮按 8–14 次调用的硬性预算执行定向核验，已超出少量调用，未再追加 `record_risk`/`write_security_report`（`ae.e()` 内部实现为同链路推断，未逐字反编译；其唯一调用方与前置 `aa.a()` 判定已确认）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍诱导链路（StDlgSrs 定时器→StartDialog 不可取消弹窗→ACTION_ACCESSIBILITY_SETTINGS 跳转→AccOnDialog 成功提示→HOME 回桌面）在 DEX 中完全静态可见；不可静态还原的部分为：设置包名与冷启动 WebView URL 由 librealtalk-jni.so 的 JNI 方法 getSettingsPackageFromJNI/getXiaomiSettingsPackageFromJNI/getStartWebUrl 运行期返回，以及 WbActivity 加载的远端钓鱼 HTML。ae.e() 内部实现未逐字反编译，其行为由唯一调用点与 aa.a() 前置判定推断。",
  "summary_one_liner": "由常驻服务 StDlgSrs 定时器在无障碍未开启时反复拉起不可取消的“Google Play Services 已停止”恐吓弹窗，单按钮 OK 一步直跳系统无障碍设置，获权后用“Google Services 已成功启用”提示并把用户踢回桌面，服务端再自动点击设置页条目完成自启与防撤权。",
  "disguise_identity": {
    "app_display_name": "Leboncoin",
    "claimed_brand_or_persona": "Google Play Services / Google Services（系统服务身份），并使用 Leboncoin 品牌作为桌面外壳",
    "a11y_service_label": "Google Services",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务声明 res/xml/service_conf.xml 完全省略 android:description，系统列表无任何用途说明与警告，仅显示“Google Services”标签；应用名 Leboncoin 与服务名 Google Services 分属两个互不相关的品牌；多个组件进程/名称伪造成 com.googleplay.activities.AdminRequestDialog、com.googleplay.srs.CmndSrs 等；设备管理器标签伪造成 Play Market；StartDialog/AccOnDialog 使用 Theme.Translucent.NoTitleBar 悬浮式呈现，不进入正常 Activity 栈视觉流；字符串资源以无语义 key（cziugqk、ldbib、ohygeztvjm）与空值资源混淆真实文案。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.pandar.MainActivity → com.pandar.wb.WbActivity",
      "trigger_event": "用户点击桌面图标 Leboncoin 触发 MainActivity.onCreate",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无（页面内容来自 Relactive.getStartWebUrl() 返回的远端 URL）",
      "shown_text_zh": "启动后直接展示远端网页，随即 finish() 退出自身，无原生引导界面",
      "user_action_requested": "无明确引导动作；应用完成初始化后即跳转网页",
      "code_anchor": "com.pandar.MainActivity.onCreate / aviasalea.ae.a(Context,String) / com.pandar.wb.WbActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.pandar.srs.StDlgSrs（后台常驻服务，action=com.googleplay.srs.StDlgSrs）→ com.pandar.ds.StartDialog",
      "trigger_event": "StDlgSrs 内 TimerTask 周期触发 StDlgSrs$a.run：aa.a(context) 判定无障碍未开启则 ae.e(context) 拉起 StartDialog",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（本步仅为拉起动作）",
      "shown_text_zh": "后台定时检测无障碍开关，未开启即弹出引导弹窗，不依赖用户在前台操作",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "com.pandar.srs.StDlgSrs$a.run / aviasalea.aa.a(Context) / aviasalea.ae.e(Context)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.pandar.ds.StartDialog（android:theme=Theme.Translucent.NoTitleBar）内的不可取消 AlertDialog",
      "trigger_event": "StartDialog.onCreate → b() 构建 aviasalea.w$b 对话框并 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention | Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: | OK",
      "shown_text_zh": "“注意” | “很遗憾，Google Play 服务已停止。为保证设备正常运行，请在菜单中选择一行并自行启用：” | “确定”",
      "user_action_requested": "仅可点击 OK 继续；setCancelable(false) 且 setCanceledOnTouchOutside(false)，无取消/跳过按钮，返回键无法关闭",
      "code_anchor": "com.pandar.ds.StartDialog.b / @string/start_dialog_warning / @string/start_dialog_description"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统页 Settings.ACTION_ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "StartDialog$1.onClick（OK 按钮）→ aa.a() 未开启 → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Services（系统列表中该服务条目的 label）",
      "shown_text_zh": "系统无障碍列表中呈现为“Google Services”，无用途说明文字（service_conf.xml 未声明 android:description）",
      "user_action_requested": "要求用户在该列表中手动找到并开启“Google Services”开关",
      "code_anchor": "com.pandar.ds.StartDialog$1.onClick / res/xml/service_conf.xml / @string/accessibilityservice_label"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.pandar.srs.GPSrs（无障碍服务）在设置页内的事件处理 + com.pandar.injs.g.GActivity",
      "trigger_event": "GPSrs 收到设置页 TYPE_WINDOW_* 事件 → aa.a(Context, AccessibilityNodeInfo, aa$a)：包名匹配 getSettingsPackageFromJNI()/getXiaomiSettingsPackageFromJNI() 且节点文本匹配 2131361806/2131361810/2131361816（含“Google Services”）→ aa_a.a()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Services",
      "shown_text_zh": "服务在系统设置页内自动定位并点击自身条目/确认按钮，完成自启用；isHardMode 且前台为当前包时另拉起 GActivity 接管界面",
      "user_action_requested": "用户仅需进入设置页，点击与确认动作由无障碍服务代劳",
      "code_anchor": "aviasalea.aa.a(Context,AccessibilityNodeInfo,aa$a) / aviasalea.ae.d(Context) / com.pandar.injs.g.GActivity"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.pandar.ds.AccOnDialog",
      "trigger_event": "无障碍已启用后由 GPSrs 链路拉起 AccOnDialog.onCreate → b() 弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Google Services | Google Service was successfully enabled | OK",
      "shown_text_zh": "“Google Services” | “Google 服务已成功启用” | “确定”",
      "user_action_requested": "点击 OK；AccOnDialog$1.onClick 调 ae.h(context) 发送 ACTION_MAIN+CATEGORY_HOME 把用户直接送回桌面，无取消按钮",
      "code_anchor": "com.pandar.ds.AccOnDialog.b / com.pandar.ds.AccOnDialog$1.onClick / aviasalea.ae.h(Context) / @string/dlg_acc_on_desc"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "StDlgSrs TimerTask → StartDialog（重复弹出）",
      "trigger_event": "用户从设置页返回但未开启权限，或点击返回键；StDlgSrs 定时器下一轮 aa.a() 仍为 false → 再次 ae.e(context)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable:",
      "shown_text_zh": "同一恐吓弹窗被反复重新拉起，直至用户开启无障碍",
      "user_action_requested": "无任何降级/跳过出口，只能开启或反复遭遇弹窗",
      "code_anchor": "com.pandar.srs.StDlgSrs$a.run / aviasalea.aa.a(Context)"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "GPSrs 对任意前台包的窗口事件处理 → com.pandar.wb.WbActivity",
      "trigger_event": "aa.a(Context,AccessibilityNodeInfo,aa$a) 中 wb.c.b(currentPackage) 返回非空 → ae.a(context, url, package) 打开 WbActivity",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无（URL 与页面内容均为远端下发，本地仅有信用卡表单字符串资源）",
      "shown_text_zh": "在银行/支付类应用前台时弹出对应伪造网页覆盖界面",
      "user_action_requested": "在伪造页面中提交卡片等凭据",
      "code_anchor": "aviasalea.aa.a(Context,AccessibilityNodeInfo,aa$a) / com.pandar.wb.c.b / aviasalea.ae.a(Context,String,String)"
    }
  ],
  "text_presentation_locations": [
    "StartDialog（Theme.Translucent.NoTitleBar，悬浮式不可取消 AlertDialog）：标题“Attention”，正文“Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable:”，仅“OK”按钮；setCancelable(false)、setCanceledOnTouchOutside(false)",
    "AccOnDialog（Theme.Translucent.NoTitleBar，不可取消 AlertDialog）：标题“Google Services”，正文“Google Service was successfully enabled”，仅“OK”按钮",
    "系统无障碍服务列表条目：仅显示 label“Google Services”（@string/accessibilityservice_label），res/xml/service_conf.xml 未声明 android:description，列表内无任何用途说明或警告",
    "设备管理器激活页：@string/admin_title “Click on Activate button to secure your application.”，label 伪造成“Play Market”（@string/admin_device_label）",
    "远端 WebView（WbActivity）：URL 由 Relactive.getStartWebUrl()/wb.c.b(package) 提供，页面内容不在包内，无法静态呈现",
    "本地字符串资源中预留的钓鱼话术：@string/Caption “Confirm credit card data”、@string/DescCaption “Enter credit card information to verify your billing data”",
    "未发现本地 HTML/asset 引导页，也未发现引导遮罩类 Overlay 布局资源"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Attention",
      "text_zh": "注意",
      "source_location": "@string/start_dialog_warning（StartDialog.b 对话框标题）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Unfortunately Google Play Services has stopped.\nFor the correct operation of the device select a line in the menu and self-enable:",
      "text_zh": "很遗憾，Google Play 服务已停止。为保证设备正常运行，请在菜单中选择一行并自行启用：",
      "source_location": "@string/start_dialog_description（StartDialog.b 对话框正文）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Service was successfully enabled",
      "text_zh": "Google 服务已成功启用",
      "source_location": "@string/dlg_acc_on_desc（AccOnDialog.b 对话框正文）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Services",
      "text_zh": "Google 服务",
      "source_location": "@string/accessibilityservice_label（无障碍服务 label，也是系统列表与 AccOnDialog 标题）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on Activate button to secure your application.",
      "text_zh": "点击“激活”按钮以保护您的应用。",
      "source_location": "@string/admin_title（设备管理器 ADD_DEVICE_ADMIN 说明，aviasalea.ae.a(ComponentName,Activity)）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Play Market",
      "text_zh": "Play 商店",
      "source_location": "@string/admin_device_label（com.pandar.rcs.AdReceiver 设备管理器 label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Confirm credit card data",
      "text_zh": "确认信用卡信息",
      "source_location": "@string/Caption",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Enter credit card information to verify your billing data",
      "text_zh": "请输入信用卡信息以验证您的账单数据",
      "source_location": "@string/DescCaption",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "StDlgSrs 的 TimerTask 周期性执行 StDlgSrs$a.run，每次先以 aa.a(context) 读取 Settings.Secure 的 accessibility_enabled 与 enabled_accessibility_services 判断 com.pandar/com.pandar.srs.GPSrs 是否已启用；未启用则再次 ae.e(context) 拉起 StartDialog。用户从设置页返回或关闭弹窗后仍会被下一次定时任务重新弹出，直到开启无障碍；无降级路径。",
    "overlay_or_fake_settings": "未发现自绘高仿系统无障碍开关页或半透明引导遮罩布局；改用 Theme.Translucent.NoTitleBar 的悬浮式不可取消 AlertDialog 覆盖在任意前台应用之上，并配合 GActivity（isHardMode 且前台为当前包时拉起）接管界面。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=19（minSdk 14），不含 Android 13 受限设置分步教学，也未使用 Session 安装器绕过。",
    "post_grant_anti_removal": "有。GPSrs 在无障碍事件中比对设置包（getSettingsPackageFromJNI/getXiaomiSettingsPackageFromJNI）与节点文本（2131361806/2131361810/2131361816，含“Google Services”），命中即回调 aa_a.a() 在设置页内自动点击确认/启用自身；同时 aviasalea.ae.h() 以 ACTION_MAIN+CATEGORY_HOME 强制回桌面、ae.d() 拉起 GActivity 接管前台，阻止用户在设置页停留撤权；另有 RestartService 监听 BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED 等广播维持服务存活。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条并行触发：①监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（即 StartDialog$1.onClick 执行瞬间，通常在冷启动后数秒内由 StDlgSrs 定时器触发）；②监测到 com.pandar.ds.StartDialog 或 com.pandar.ds.AccOnDialog 这两个 Translucent 主题 Activity 的 onResume。建议在安装后静置 10–60 秒并在前台打开任意其他应用，等待后台弹窗自行浮出。",
    "key_pages_to_capture": [
      {
        "page_role": "后台浮出的冷启动式恐吓引导弹窗页",
        "page_identifier": "标题“Attention”、正文含“Unfortunately Google Play Services has stopped”、仅“OK”按钮、无取消按钮、页面无标题栏且覆盖在其他应用之上",
        "why_most_useful": "这是判定“诱导”的核心证据页：可同时验证无取消出口、伪造 Google 服务身份、故障恐吓话术三要素，且能确认其由后台服务而非用户操作触发",
        "observable_utg_signals": ["按钮集合仅含 OK，缺失 Cancel/关闭", "文本含 Google Play Services 与 stopped 的故障恐吓组合", "弹窗出现时前台并非本应用（覆盖层判定）", "Activity 名为 com.pandar.ds.StartDialog"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "列表内条目文本恰为“Google Services”，其下无任何说明/警告文字，与桌面应用名 Leboncoin 不一致",
        "why_most_useful": "直接证明身份冒充与描述缺失（service_conf.xml 无 android:description），是“用户无法知情其授权对象”的关键证据",
        "observable_utg_signals": ["条目文本=Google Services 且无 description 子行", "开关状态变化后服务立即被点击确认（自启用）"]
      },
      {
        "page_role": "获权后成功提示页（并伴随强制回桌面）",
        "page_identifier": "标题“Google Services”、正文“Google Service was successfully enabled”、仅 OK；点击后前台瞬间变为桌面 Launcher",
        "why_most_useful": "验证获权后的痕迹清理动作（HOME Intent）与自确认完成，区分“用户手动开启”与“服务代点开启”",
        "observable_utg_signals": ["点击 OK 后前台包立即变为 launcher", "弹窗 Activity=com.pandar.ds.AccOnDialog", "无取消按钮"]
      },
      {
        "page_role": "拒绝授权后的复现循环页",
        "page_identifier": "从系统设置返回或按返回键后，同一“Attention”弹窗在数秒内再次出现",
        "why_most_useful": "确认拒绝循环机制（定时器重拉），是判定强制性的直接运行证据",
        "observable_utg_signals": ["同一弹窗文本在短时间内重复出现次数", "返回键/点击外部无法消除弹窗", "两次弹窗间隔近似固定定时周期"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图空文本诱导，文案均为原生字符串，UTG 可直接提取。盲区在于：①系统设置页内由无障碍服务代点的自启用动作发生在系统 Settings 进程界面，UTG 需持续跟踪设置页节点变化而非只看本应用页面；②冷启动与诱饵页面内容（getStartWebUrl、wb.c.b(package) 返回的钓鱼 URL 及其 HTML）由 librealtalk-jni.so 与远端下发，纯静态不可见，需流量侧配合；③本样本未加壳，运行期 UTG 不受影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.pandar.ds.StartDialog.b",
    "com.pandar.ds.StartDialog$1.onClick",
    "com.pandar.srs.StDlgSrs$a.run",
    "aviasalea.aa.a(Context)",
    "aviasalea.aa.a(Context,AccessibilityNodeInfo,aa$a)",
    "com.pandar.ds.AccOnDialog$1.onClick / aviasalea.ae.h(Context)"
  ]
}
```

</details>
