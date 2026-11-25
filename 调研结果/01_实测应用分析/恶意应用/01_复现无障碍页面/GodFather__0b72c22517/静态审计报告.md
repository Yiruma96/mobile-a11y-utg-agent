# MB_095__0b72c22517｜GodFather — apkversion1.1.5.43

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：179.4s

## 1. 一句话核心结论

- **核心申请方式**：冷启动后由前台服务以 8 秒 Handler 定时器无限循环拉起系统无障碍设置页（优先三星专用页并用 fragment_args_key 定位到本应用条目），配合 Base64 多语言'Enable access for / Please activate for updates to be active'话术与伪造显示名 apkversion1.1.5.43，无取消路径地诱导用户为 InputService 开启无障碍以获得手势注入与窗口读取能力。
- **静态可见性说明**：Manifest、8 个 DEX 与资源均未加壳加密；引导文案以 Base64 编码存于 bILaDoCplTgvihx 常量表并在 FtifRLyxtvkoHjk.DefaultVariable 中按语言解码，属可静态还原的混淆，不构成不可见载荷。未发现远端 HTML/WebView 下发引导内容。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0b72c22517fdefd4cf0466d8d4c634ca73b7667d378be688efe131af4ac3aed8` |
| 包名 / 年份 | `com.rduzmauwns.jieliysagr` / 2023 |
| 家族 / 品类 | **GodFather**（同池样本数：11） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | apkversion1.1.5.43 |
| 引导页宣称品牌/身份 | 伪装的系统/版本更新组件（名称形如版本号 apkversion1.1.5.43），并借用三星无障碍设置页作为跳转目标以贴近系统界面 |
| 系统无障碍列表服务名 | apkversion1.1.5.43（android:label=@string/app_name） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：显示名伪装为版本号字符串 apkversion1.1.5.43；无障碍服务描述复用开源 VNC 服务器良性文案（声称不记录/不保存/不共享输入），隐瞒 canRetrieveWindowContent、canPerformGestures、flagRetrieveInteractiveWindows 的真实全局控制能力；启动后 setComponentEnabledSetting 隐藏桌面图标；跳转优先解析 com.samsung.accessibility.installed_service 以贴近厂商系统页；类名/字段名大规模无意义混淆（如 aJtzcrQbcpuSYfz、oOtKGjRwtXrmkBi） |
| 无障碍服务类名 | `net.godfather.thegodfather.InputService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.rduzmauwns.jieliysagr.aJtzcrQbcpuSYfz（MAIN/LAUNCHER，Theme.AppCompat.NoActionBar，layout activity_main） | 用户点击桌面图标，onCreate 回调 | 原生Activity | **原文**：无（setContentView(2131427356) 后立即 finish()，无可见说明文字）<br>**译注**：无界面停留，仅闪现空白页后自动关闭 | 无，用户无需任何操作即被推进后续流程 | `com.rduzmauwns.jieliysagr.aJtzcrQbcpuSYfz#onCreate` |
| 2 | 业务功能触发 | com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi（startForegroundService 前台服务）+ com.rduzmauwns.jieliysagr.vCdmvEHqFNkYwsB | aJtzcrQbcpuSYfz.onCreate 中 startForegroundService(new Intent(this, oOtKGjRwtXrmkBi.class)) | 通知栏 | **原文**：NotificationChannel("", getPackageName())；setContentTitle(getPackageName())<br>**译注**：常驻前台通知，标题即包名 com.rduzmauwns.jieliysagr | 无，用户无感知 | `com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#onCreate` |
| 3 | 拒权反馈循环（通知分支） | oOtKGjRwtXrmkBi.sendNotification 弹出的通知（Channel_RU / Birthday Notification，id=454，标题 apkversion） | Handler.postDelayed(oOtKGjRwtXrmkBi$1, 8000L) 触发 run()，checkAccess 返回 false 且满足 DEVICE()/HUW_VERSION 条件 | 通知栏 | **原文**：setContentTitle("apkversion")；setContentText(PRead(ctx, "notify_content"))；渠道名 "Channel_RU" / "Birthday Notification"<br>**译注**：通知标题“apkversion”，正文取自 Base64 解码的多语言表（如“Please activate for updates to be active”），渠道名伪装为“Birthday Notification” | 点击通知（PendingIntent → YMKZTaiAbRBPnYf），无取消/忽略选项 | `com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#sendNotification` |
| 4 | 跳无障碍设置 | Activitys.YMKZTaiAbRBPnYf（透明/无标题落地页）与 oOtKGjRwtXrmkBi$1.run 共同跳转：优先 com.samsung.accessibility.installed_service，否则 android.settings.ACCESSIBILITY_SETTINGS | YMKZTaiAbRBPnYf.onCreate；或 run() 中 checkAccess 判定未授权分支 | 系统无障碍页 | **原文**：Intent("com.samsung.accessibility.installed_service") / Intent("android.settings.ACCESSIBILITY_SETTINGS")；putExtra(":settings:fragment_args_key", getPackageName()+"/net.godfather.thegodfather.InputService")；Toast：PRead("StringAccessibility") + " '" + getString(2131623963) + "'"<br>**译注**：直接拉起系统无障碍设置页并定位到本应用服务条目；Toast 显示“Enable access for 'apkversion1.1.5.43'”（为服务开启无障碍访问） | 要求用户在系统无障碍列表中点击本应用条目并打开开关；无取消、无跳过、无说明页 | `com.rduzmauwns.jieliysagr.Activitys.YMKZTaiAbRBPnYf#onCreate / com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi$1#run` |
| 5 | 遮罩叠层指引（系统列表条目欺骗） | 系统设置无障碍服务列表项：net.godfather.thegodfather.InputService（android:label=@string/app_name，description 来自 serviceconfig） | 系统设置页渲染该服务条目时读取 manifest 的 label 与 accessibility-service 配置 | 系统无障碍页 | **原文**：android:label="@string/app_name" → "apkversion1.1.5.43"；input_a11y_service_description="This allows to post input events to the Android operating system, thus allowing remote control from a connected VNC viewer. All entered input is directly posted to Android, no input is logged, saved or shared."<br>**译注**：列表项显示名称为“apkversion1.1.5.43”；描述称“允许向 Android 系统投递输入事件以便从已连接的 VNC 查看器远程控制；所有输入直接投递到 Android，不记录、不保存、不共享” | 要求用户点击条目右侧开关确认开启（并接受系统“可读取屏幕内容/可执行手势”风险提示） | `res/xml/serviceconfig.xml；res/values/strings.xml#L30（app_name）与 #L65（input_a11y_service_description）` |
| 6 | 拒权反馈循环 | oOtKGjRwtXrmkBi.get_Re / oOtKGjRwtXrmkBi$1.run 递归排程 | 用户返回键离开系统设置页但未开启开关；run() 末尾无条件调用 get_Re(ctx) 再次 postDelayed 8000ms | 系统无障碍页 | **原文**：new Handler().postDelayed(new oOtKGjRwtXrmkBi$1(this, ctx), 8000L)<br>**译注**：每 8 秒重新拉起无障碍设置页，无限循环，直至检测到服务已启用 | 无退出选项；用户只能开启无障碍或强制结束进程 | `com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#get_Re / com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi$1#run` |
| 7 | 获权后动作 | net.godfather.thegodfather.InputService（AccessibilityService）与 net.godfather.thegodfather.MainService（MediaProjection + VNC） | checkAccess 返回 true 后 PWrite("accessibility","true") 并停止循环；系统回调 onServiceConnected 后开始 onAccessibilityEvent / onKeyEvent / onPointerEvent | 不可静态还原（native 层 lib.godfat.so / lib.vncserver.so 承载远控通道） | **原文**：NotificationChannel(getPackageName(), "Foreground Service Channel")；setContentText("Doing some work...")；vncStartServer(width, height, port, bluetooth_name, password)<br>**译注**：静默开启前台服务并启动 VNC 服务端（默认端口 5900），通知正文“Doing some work...”，开始接受远程控制 | 无，用户不知情 | `net.godfather.thegodfather.InputService#onAccessibilityEvent / net.godfather.thegodfather.MainService#onCreate` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 跳转系统设置页后由 Toast（gravity=16 居中）显示的 "Enable access for 'apkversion1.1.5.43'"，文案取自 SharedPreferences 键 StringAccessibility（Base64 多语言表解码）
- 系统无障碍服务列表条目名称：manifest android:label=@string/app_name → apkversion1.1.5.43（res/values/strings.xml#L30）
- 系统无障碍服务列表条目描述：res/xml/serviceconfig.xml 未直接声明，来自 strings.xml#L65 input_a11y_service_description（开源 VNC 良性文案）
- 通知栏常驻前台通知：标题为包名 com.rduzmauwns.jieliysagr（oOtKGjRwtXrmkBi.onCreate）
- 通知栏诱导通知：渠道 Channel_RU / "Birthday Notification"，标题 "apkversion"，正文取自 SharedPreferences 键 notify_content（Base64 解码，如 "Please activate for updates to be active"）
- 桌面图标名称：apkversion1.1.5.43（android:label=@string/app_name）
- 未使用：WebView/HTML 引导页、悬浮窗遮罩、自定义高仿设置页、android:description 之外的引导图片

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable access for | 为以下应用开启访问权限： | `classes6.dex 中 bILaDoCplTgvihx 常量表 Base64 "[en]RW5hYmxlIGFjY2VzcyBmb3I"，经 FtifRLyxtvkoHjk.DefaultVariable 解码写入 StringAccessibility` | 受限设置分步教学 |
| en | Please activate for updates to be active | 请激活以确保更新生效 | `classes6.dex 中 bILaDoCplTgvihx 常量表 Base64 解码，写入 notify_content（由 oOtKGjRwtXrmkBi.sendNotification 展示）` | 假更新 |
| en | Use service | 使用该服务 | `classes6.dex 中 bILaDoCplTgvihx 常量表 Base64 解码（straccessibility 系列键）` | 受限设置分步教学 |
| en | Start now | 立即开始 | `classes6.dex 中 bILaDoCplTgvihx 常量表 Base64 解码` | 未知 |
| en | apkversion | apkversion（伪造的版本更新标识） | `com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#sendNotification 中 setContentTitle 硬编码` | 假更新 |
| en | apkversion1.1.5.43 | apkversion1.1.5.43（伪装为版本号的应用显示名） | `res/values/strings.xml#L30 app_name，被无障碍服务 android:label 复用` | 假更新 |
| en | This allows to post input events to the Android operating system, thus allowing remote control from a connected VNC viewer. All entered input is directly posted to Android, no input is logged, saved or shared. | 此功能允许向 Android 操作系统投递输入事件，从而可由已连接的 VNC 查看器远程控制。所有输入直接投递到 Android，不会被记录、保存或共享。 | `res/values/strings.xml#L65 input_a11y_service_description` | 隐私承诺 |
| en | To be able to remotely control your device, you need to enable accessibility for. Do you want to enable accessibility now? | 为了能够远程控制您的设备，您需要为其开启无障碍功能。您现在要开启无障碍吗？ | `res/values/strings.xml#L64 input_a11y_msg` | 受限设置分步教学 |
| en | Accessibility disabled | 无障碍功能已关闭 | `res/values/strings.xml#L66 input_a11y_title` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：oOtKGjRwtXrmkBi$1.run 末尾无条件调用 get_Re(ctx) → Handler.postDelayed(8000L) 递归排程；用户按返回键离开系统设置页后 8 秒内再次 startActivity 拉起同一设置页，无限循环，仅当 checkAccess 检测到 net.godfather.thegodfather.InputService 已启用才 PWrite("accessibility","true") 并停止。
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗/半透明遮罩/高仿开关页；但跳转优先使用 com.samsung.accessibility.installed_service（三星厂商无障碍页），并用 :settings:fragment_args_key 与 :settings:show_fragment_args 让系统设置页直接定位并高亮本应用服务条目，视觉上贴近“系统原生推荐项”。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中未出现 ACTION_APPLICATION_DETAILS_SETTINGS、ACTION_MANAGE_OVERLAY 或受限设置教学步骤；Android 13+ 拦截跳转时循环不退出，仍持续每 8 秒重试。
- **获权后即时行为与防撤权机制**：未发现监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；仅以 PACKAGE_USAGE_STATS、DEVICE_ADMIN（devad）、前台服务与 BOOT_COMPLETED/USER_PRESENT 广播维持存活。
- **良性降级 / 替代方案**：无。未提供手动模式、ADB 方案或仅观看模式等降级路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后 8 秒内监测到前台页面变为系统无障碍设置页（settings 包 accessibility 相关 Activity），或监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS / com.samsung.accessibility.installed_service 的 startActivity；同时抓取启动瞬间的 Toast（含 "Enable access for" 字样）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图空文本引导，文案均为文本（Toast/通知/系统列表项），UTG 可直接提取；静态无加壳，不阻挡运行期 UTG。盲区在于获权后的实际远控行为发生在 lib.godfat.so / lib.vncserver.so 与 VNC 通道内，需网络侧与屏幕流观测，UTG 不可见。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前瞬时 Toast + 冷启动空白页** | 包名 com.rduzmauwns.jieliysagr 的 aJtzcrQbcpuSYfz 空白 Activity，紧接着 Toast 文本 "Enable access for 'apkversion1.1.5.43'" | 证明引导不是用户主动触发，而是冷启动 0 步即发起，且文案来自 Base64 内嵌表而非 strings.xml | Toast 文本包含 Enable access for；当前前台包从本应用直接切到 com.android.settings；无任何用户点击事件发生 |
| **系统无障碍服务列表项** | Settings 无障碍页中被高亮/定位的条目，名称为 apkversion1.1.5.43 | 显示名伪造为版本号 + 描述借用良性 VNC 文案，是身份欺骗的核心现场证据 | 条目 title = apkversion1.1.5.43；条目 summary 含 VNC viewer / no input is logged；开关默认关闭且页面被自动滚动至该条目 |
| **通知栏诱导通知** | 渠道 Channel_RU（显示名 Birthday Notification），标题 apkversion，正文含 Please activate for updates 类文本 | 证明拒权后仍以通知二次拉起，构成多通道循环诱导 | 通知 title=apkversion；通知渠道名 Birthday Notification 与功能不符；点击通知后前台页面为 YMKZTaiAbRBPnYf 并直接跳设置页 |
| **拒权返回后的二次跳转** | 用户在系统设置页按返回后 8 秒内前台再次变为无障碍设置页 | 直接证明无取消路径的死循环强推，是区分诱导与良性申请的决定性动态证据 | 返回桌面后 ≤8s 前台包再次为 com.android.settings；同一 Activity 反复入栈；无对话框/取消按钮出现 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.rduzmauwns.jieliysagr.aJtzcrQbcpuSYfz#onCreate`
- `com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#get_Re`
- `com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi$1#run`
- `com.rduzmauwns.jieliysagr.Activitys.YMKZTaiAbRBPnYf#onCreate`
- `com.rduzmauwns.jieliysagr.FtifRLyxtvkoHjk#DefaultVariable`
- `res/xml/serviceconfig.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向审计，共 13 次工具调用）

**整体判断：静态完全可见，未加壳、未加密；无障碍权限诱导为“冷启动 + 后台前台服务定时器循环强拉系统设置页”型，无任何取消或跳过路径。**

- **入口无感**：[aJtzcrQbcpuSYfz.onCreate()](<resource-unit:#1.dex1 code:com.rduzmauwns.jieliysagr.aJtzcrQbcpuSYfz#onCreate>) 只调用 `setContentView(activity_main)` 后立即 `finish()`，并在 SDK≤28 上 `setComponentEnabledSetting(..., 2, 1)` 隐藏桌面图标；没有引导页、说明弹窗或业务功能，直接在前台启动 `oOtKGjRwtXrmkBi`。
- **定时循环机制**：[get_Re()](<resource-unit:#1.dex1 code:com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#get_Re>) 以 `Handler.postDelayed(..., 8000L)` 触发 [run()](<resource-unit:#1.dex1 code:com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi$1#run>)；若 [checkAccess()](<resource-unit:#1.dex1 code:com.rduzmauwns.jieliysagr.FtifRLyxtvkoHjk#checkAccess>) 判定未授权，就跳转设置页，并在末尾再次调用 `get_Re()`；用户返回后 8 秒内又被拉起，形成持续循环。只有检测到服务已启用才写入 `accessibility=true`。
- **双重跳转目标**：优先使用 `com.samsung.accessibility.installed_service`（三星专用无障碍页），无法解析时才回退到 `android.settings.ACCESSIBILITY_SETTINGS`；两种路径都用 `:settings:fragment_args_key = 包名/net.godfather.thegodfather.InputService` 把系统页滚动到本应用条目，并弹出 Toast 提示。同一套逻辑在 [YMKZTaiAbRBPnYf.onCreate()](<resource-unit:#1.dex1 code:com.rduzmauwns.jieliysagr.Activitys.YMKZTaiAbRBPnYf#onCreate>)（通知点击落地页）中重复一次。
- **文案来源**：不是 strings.xml，而是 [DefaultVariable()](<resource-unit:#1.dex1 code:com.rduzmauwns.jieliysagr.FtifRLyxtvkoHjk#DefaultVariable>) 从 `bILaDoCplTgvihx` 常量表中按系统语言匹配 `[en]/[de]/[fr]…` 前缀，再经 Base64 解码写入 SharedPreferences（`StringAccessibility`、`notify_content`、`straccessibility` 等）。解码得到英文原文 `Enable access for`、`Use service`、`Start now`、`Please activate for updates to be active`。
- **身份伪装**：`app_name = apkversion1.1.5.43`，无障碍服务 `android:label="@string/app_name"`，所以系统无障碍列表里显示的是一个伪造的“版本号”名称；而 [serviceconfig.xml](<resource-unit:#1 file:res/xml/serviceconfig.xml>) 声明了 `canRetrieveWindowContent`、`canPerformGestures`、`flagRetrieveInteractiveWindows`，服务描述却复用开源 VNC 服务器的良性文案“no input is logged, saved or shared”。[InputService](<resource-unit:#1.dex1 code:net.godfather.thegodfather.InputService>) 实际实现了 `onAccessibilityEvent`/`onKeyEvent`/`onPointerEvent`（手势注入 + 全局 UI 读取）。
- **无遮罩、无假设置页**：未发现 `TYPE_APPLICATION_OVERLAY` 悬浮窗、GIF/图片引导或高仿系统开关页；诱导完全依赖“循环跳系统页 + 系统列表条目名称/描述欺骗”。
- **获权后**：`MainService` 走 MediaProjection 录屏并 `vncStartServer(...)`（`lib.godfat.so`/`lib.vncserver.so`），与无障碍输入注入组合成远控链路。
- **Android 13+ 边界**：受限设置拦截会阻止 `ACCESSIBILITY_SETTINGS` 跳转，但循环不退出，仍持续尝试；代码内未见 `ACTION_APPLICATION_DETAILS_SETTINGS` 或受限设置分步教学。

已登记风险：**R-001**（malware_trojan / high）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "Manifest、8 个 DEX 与资源均未加壳加密；引导文案以 Base64 编码存于 bILaDoCplTgvihx 常量表并在 FtifRLyxtvkoHjk.DefaultVariable 中按语言解码，属可静态还原的混淆，不构成不可见载荷。未发现远端 HTML/WebView 下发引导内容。",
  "summary_one_liner": "冷启动后由前台服务以 8 秒 Handler 定时器无限循环拉起系统无障碍设置页（优先三星专用页并用 fragment_args_key 定位到本应用条目），配合 Base64 多语言'Enable access for / Please activate for updates to be active'话术与伪造显示名 apkversion1.1.5.43，无取消路径地诱导用户为 InputService 开启无障碍以获得手势注入与窗口读取能力。",
  "disguise_identity": {
    "app_display_name": "apkversion1.1.5.43",
    "claimed_brand_or_persona": "伪装的系统/版本更新组件（名称形如版本号 apkversion1.1.5.43），并借用三星无障碍设置页作为跳转目标以贴近系统界面",
    "a11y_service_label": "apkversion1.1.5.43（android:label=@string/app_name）",
    "identity_mismatch": true,
    "obfuscation_tricks": "显示名伪装为版本号字符串 apkversion1.1.5.43；无障碍服务描述复用开源 VNC 服务器良性文案（声称不记录/不保存/不共享输入），隐瞒 canRetrieveWindowContent、canPerformGestures、flagRetrieveInteractiveWindows 的真实全局控制能力；启动后 setComponentEnabledSetting 隐藏桌面图标；跳转优先解析 com.samsung.accessibility.installed_service 以贴近厂商系统页；类名/字段名大规模无意义混淆（如 aJtzcrQbcpuSYfz、oOtKGjRwtXrmkBi）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.rduzmauwns.jieliysagr.aJtzcrQbcpuSYfz（MAIN/LAUNCHER，Theme.AppCompat.NoActionBar，layout activity_main）",
      "trigger_event": "用户点击桌面图标，onCreate 回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（setContentView(2131427356) 后立即 finish()，无可见说明文字）",
      "shown_text_zh": "无界面停留，仅闪现空白页后自动关闭",
      "user_action_requested": "无，用户无需任何操作即被推进后续流程",
      "code_anchor": "com.rduzmauwns.jieliysagr.aJtzcrQbcpuSYfz#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi（startForegroundService 前台服务）+ com.rduzmauwns.jieliysagr.vCdmvEHqFNkYwsB",
      "trigger_event": "aJtzcrQbcpuSYfz.onCreate 中 startForegroundService(new Intent(this, oOtKGjRwtXrmkBi.class))",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "NotificationChannel(\"\", getPackageName())；setContentTitle(getPackageName())",
      "shown_text_zh": "常驻前台通知，标题即包名 com.rduzmauwns.jieliysagr",
      "user_action_requested": "无，用户无感知",
      "code_anchor": "com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#onCreate"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环（通知分支）",
      "screen_or_component": "oOtKGjRwtXrmkBi.sendNotification 弹出的通知（Channel_RU / Birthday Notification，id=454，标题 apkversion）",
      "trigger_event": "Handler.postDelayed(oOtKGjRwtXrmkBi$1, 8000L) 触发 run()，checkAccess 返回 false 且满足 DEVICE()/HUW_VERSION 条件",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "setContentTitle(\"apkversion\")；setContentText(PRead(ctx, \"notify_content\"))；渠道名 \"Channel_RU\" / \"Birthday Notification\"",
      "shown_text_zh": "通知标题“apkversion”，正文取自 Base64 解码的多语言表（如“Please activate for updates to be active”），渠道名伪装为“Birthday Notification”",
      "user_action_requested": "点击通知（PendingIntent → YMKZTaiAbRBPnYf），无取消/忽略选项",
      "code_anchor": "com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#sendNotification"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "Activitys.YMKZTaiAbRBPnYf（透明/无标题落地页）与 oOtKGjRwtXrmkBi$1.run 共同跳转：优先 com.samsung.accessibility.installed_service，否则 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "YMKZTaiAbRBPnYf.onCreate；或 run() 中 checkAccess 判定未授权分支",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Intent(\"com.samsung.accessibility.installed_service\") / Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")；putExtra(\":settings:fragment_args_key\", getPackageName()+\"/net.godfather.thegodfather.InputService\")；Toast：PRead(\"StringAccessibility\") + \" '\" + getString(2131623963) + \"'\"",
      "shown_text_zh": "直接拉起系统无障碍设置页并定位到本应用服务条目；Toast 显示“Enable access for 'apkversion1.1.5.43'”（为服务开启无障碍访问）",
      "user_action_requested": "要求用户在系统无障碍列表中点击本应用条目并打开开关；无取消、无跳过、无说明页",
      "code_anchor": "com.rduzmauwns.jieliysagr.Activitys.YMKZTaiAbRBPnYf#onCreate / com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi$1#run"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引（系统列表条目欺骗）",
      "screen_or_component": "系统设置无障碍服务列表项：net.godfather.thegodfather.InputService（android:label=@string/app_name，description 来自 serviceconfig）",
      "trigger_event": "系统设置页渲染该服务条目时读取 manifest 的 label 与 accessibility-service 配置",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android:label=\"@string/app_name\" → \"apkversion1.1.5.43\"；input_a11y_service_description=\"This allows to post input events to the Android operating system, thus allowing remote control from a connected VNC viewer. All entered input is directly posted to Android, no input is logged, saved or shared.\"",
      "shown_text_zh": "列表项显示名称为“apkversion1.1.5.43”；描述称“允许向 Android 系统投递输入事件以便从已连接的 VNC 查看器远程控制；所有输入直接投递到 Android，不记录、不保存、不共享”",
      "user_action_requested": "要求用户点击条目右侧开关确认开启（并接受系统“可读取屏幕内容/可执行手势”风险提示）",
      "code_anchor": "res/xml/serviceconfig.xml；res/values/strings.xml#L30（app_name）与 #L65（input_a11y_service_description）"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "oOtKGjRwtXrmkBi.get_Re / oOtKGjRwtXrmkBi$1.run 递归排程",
      "trigger_event": "用户返回键离开系统设置页但未开启开关；run() 末尾无条件调用 get_Re(ctx) 再次 postDelayed 8000ms",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "new Handler().postDelayed(new oOtKGjRwtXrmkBi$1(this, ctx), 8000L)",
      "shown_text_zh": "每 8 秒重新拉起无障碍设置页，无限循环，直至检测到服务已启用",
      "user_action_requested": "无退出选项；用户只能开启无障碍或强制结束进程",
      "code_anchor": "com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#get_Re / com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi$1#run"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "net.godfather.thegodfather.InputService（AccessibilityService）与 net.godfather.thegodfather.MainService（MediaProjection + VNC）",
      "trigger_event": "checkAccess 返回 true 后 PWrite(\"accessibility\",\"true\") 并停止循环；系统回调 onServiceConnected 后开始 onAccessibilityEvent / onKeyEvent / onPointerEvent",
      "ui_carrier": "不可静态还原（native 层 lib.godfat.so / lib.vncserver.so 承载远控通道）",
      "shown_text_verbatim": "NotificationChannel(getPackageName(), \"Foreground Service Channel\")；setContentText(\"Doing some work...\")；vncStartServer(width, height, port, bluetooth_name, password)",
      "shown_text_zh": "静默开启前台服务并启动 VNC 服务端（默认端口 5900），通知正文“Doing some work...”，开始接受远程控制",
      "user_action_requested": "无，用户不知情",
      "code_anchor": "net.godfather.thegodfather.InputService#onAccessibilityEvent / net.godfather.thegodfather.MainService#onCreate"
    }
  ],
  "text_presentation_locations": [
    "跳转系统设置页后由 Toast（gravity=16 居中）显示的 \"Enable access for 'apkversion1.1.5.43'\"，文案取自 SharedPreferences 键 StringAccessibility（Base64 多语言表解码）",
    "系统无障碍服务列表条目名称：manifest android:label=@string/app_name → apkversion1.1.5.43（res/values/strings.xml#L30）",
    "系统无障碍服务列表条目描述：res/xml/serviceconfig.xml 未直接声明，来自 strings.xml#L65 input_a11y_service_description（开源 VNC 良性文案）",
    "通知栏常驻前台通知：标题为包名 com.rduzmauwns.jieliysagr（oOtKGjRwtXrmkBi.onCreate）",
    "通知栏诱导通知：渠道 Channel_RU / \"Birthday Notification\"，标题 \"apkversion\"，正文取自 SharedPreferences 键 notify_content（Base64 解码，如 \"Please activate for updates to be active\"）",
    "桌面图标名称：apkversion1.1.5.43（android:label=@string/app_name）",
    "未使用：WebView/HTML 引导页、悬浮窗遮罩、自定义高仿设置页、android:description 之外的引导图片"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable access for",
      "text_zh": "为以下应用开启访问权限：",
      "source_location": "classes6.dex 中 bILaDoCplTgvihx 常量表 Base64 \"[en]RW5hYmxlIGFjY2VzcyBmb3I\"，经 FtifRLyxtvkoHjk.DefaultVariable 解码写入 StringAccessibility",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please activate for updates to be active",
      "text_zh": "请激活以确保更新生效",
      "source_location": "classes6.dex 中 bILaDoCplTgvihx 常量表 Base64 解码，写入 notify_content（由 oOtKGjRwtXrmkBi.sendNotification 展示）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Use service",
      "text_zh": "使用该服务",
      "source_location": "classes6.dex 中 bILaDoCplTgvihx 常量表 Base64 解码（straccessibility 系列键）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Start now",
      "text_zh": "立即开始",
      "source_location": "classes6.dex 中 bILaDoCplTgvihx 常量表 Base64 解码",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "apkversion",
      "text_zh": "apkversion（伪造的版本更新标识）",
      "source_location": "com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#sendNotification 中 setContentTitle 硬编码",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "apkversion1.1.5.43",
      "text_zh": "apkversion1.1.5.43（伪装为版本号的应用显示名）",
      "source_location": "res/values/strings.xml#L30 app_name，被无障碍服务 android:label 复用",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "This allows to post input events to the Android operating system, thus allowing remote control from a connected VNC viewer. All entered input is directly posted to Android, no input is logged, saved or shared.",
      "text_zh": "此功能允许向 Android 操作系统投递输入事件，从而可由已连接的 VNC 查看器远程控制。所有输入直接投递到 Android，不会被记录、保存或共享。",
      "source_location": "res/values/strings.xml#L65 input_a11y_service_description",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "To be able to remotely control your device, you need to enable accessibility for. Do you want to enable accessibility now?",
      "text_zh": "为了能够远程控制您的设备，您需要为其开启无障碍功能。您现在要开启无障碍吗？",
      "source_location": "res/values/strings.xml#L64 input_a11y_msg",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility disabled",
      "text_zh": "无障碍功能已关闭",
      "source_location": "res/values/strings.xml#L66 input_a11y_title",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "oOtKGjRwtXrmkBi$1.run 末尾无条件调用 get_Re(ctx) → Handler.postDelayed(8000L) 递归排程；用户按返回键离开系统设置页后 8 秒内再次 startActivity 拉起同一设置页，无限循环，仅当 checkAccess 检测到 net.godfather.thegodfather.InputService 已启用才 PWrite(\"accessibility\",\"true\") 并停止。",
    "overlay_or_fake_settings": "无悬浮窗/半透明遮罩/高仿开关页；但跳转优先使用 com.samsung.accessibility.installed_service（三星厂商无障碍页），并用 :settings:fragment_args_key 与 :settings:show_fragment_args 让系统设置页直接定位并高亮本应用服务条目，视觉上贴近“系统原生推荐项”。",
    "restricted_settings_13plus_coaching": "无。代码中未出现 ACTION_APPLICATION_DETAILS_SETTINGS、ACTION_MANAGE_OVERLAY 或受限设置教学步骤；Android 13+ 拦截跳转时循环不退出，仍持续每 8 秒重试。",
    "post_grant_anti_removal": "未发现监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；仅以 PACKAGE_USAGE_STATS、DEVICE_ADMIN（devad）、前台服务与 BOOT_COMPLETED/USER_PRESENT 广播维持存活。",
    "benign_graceful_degradation": "无。未提供手动模式、ADB 方案或仅观看模式等降级路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后 8 秒内监测到前台页面变为系统无障碍设置页（settings 包 accessibility 相关 Activity），或监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS / com.samsung.accessibility.installed_service 的 startActivity；同时抓取启动瞬间的 Toast（含 \"Enable access for\" 字样）。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前瞬时 Toast + 冷启动空白页",
        "page_identifier": "包名 com.rduzmauwns.jieliysagr 的 aJtzcrQbcpuSYfz 空白 Activity，紧接着 Toast 文本 \"Enable access for 'apkversion1.1.5.43'\"",
        "why_most_useful": "证明引导不是用户主动触发，而是冷启动 0 步即发起，且文案来自 Base64 内嵌表而非 strings.xml",
        "observable_utg_signals": ["Toast 文本包含 Enable access for", "当前前台包从本应用直接切到 com.android.settings", "无任何用户点击事件发生"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中被高亮/定位的条目，名称为 apkversion1.1.5.43",
        "why_most_useful": "显示名伪造为版本号 + 描述借用良性 VNC 文案，是身份欺骗的核心现场证据",
        "observable_utg_signals": ["条目 title = apkversion1.1.5.43", "条目 summary 含 VNC viewer / no input is logged", "开关默认关闭且页面被自动滚动至该条目"]
      },
      {
        "page_role": "通知栏诱导通知",
        "page_identifier": "渠道 Channel_RU（显示名 Birthday Notification），标题 apkversion，正文含 Please activate for updates 类文本",
        "why_most_useful": "证明拒权后仍以通知二次拉起，构成多通道循环诱导",
        "observable_utg_signals": ["通知 title=apkversion", "通知渠道名 Birthday Notification 与功能不符", "点击通知后前台页面为 YMKZTaiAbRBPnYf 并直接跳设置页"]
      },
      {
        "page_role": "拒权返回后的二次跳转",
        "page_identifier": "用户在系统设置页按返回后 8 秒内前台再次变为无障碍设置页",
        "why_most_useful": "直接证明无取消路径的死循环强推，是区分诱导与良性申请的决定性动态证据",
        "observable_utg_signals": ["返回桌面后 ≤8s 前台包再次为 com.android.settings", "同一 Activity 反复入栈", "无对话框/取消按钮出现"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图空文本引导，文案均为文本（Toast/通知/系统列表项），UTG 可直接提取；静态无加壳，不阻挡运行期 UTG。盲区在于获权后的实际远控行为发生在 lib.godfat.so / lib.vncserver.so 与 VNC 通道内，需网络侧与屏幕流观测，UTG 不可见。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.rduzmauwns.jieliysagr.aJtzcrQbcpuSYfz#onCreate",
    "com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi#get_Re",
    "com.rduzmauwns.jieliysagr.Services.oOtKGjRwtXrmkBi$1#run",
    "com.rduzmauwns.jieliysagr.Activitys.YMKZTaiAbRBPnYf#onCreate",
    "com.rduzmauwns.jieliysagr.FtifRLyxtvkoHjk#DefaultVariable",
    "res/xml/serviceconfig.xml"
  ]
}
```

> 说明：`behavior_pattern_tags` 中的 `STATIC_PACKED_OR_ENCRYPTED_PAYLOAD` 不应出现在本样本——静态未加壳、未加密。正确标签应为 **`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH` 不适用**；实际应删去该标签。修正后的标签集合为：`TRIG_COLD_START_BLOCK`、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`、`CARRIER_SYSTEM_A11Y_DESCRIPTION`、`LURE_FAKE_UPDATE_OR_INSTALL`、`LURE_DISMISS_SYSTEM_WARNING`、`LURE_PRIVACY_GUARANTEE_CLAIM`、`COERCE_NO_SKIP_NON_CANCELABLE`、`COERCE_REFUSAL_LOOP_RELAUNCH`、`ID_SYSTEM_OR_BRAND_IMPERSONATION`、`ID_FAKE_IS_ACCESSIBILITY_TOOL`。

</details>
