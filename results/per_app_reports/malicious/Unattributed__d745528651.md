# MB_168__d745528651｜Unattributed — ConfigService Core

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：200.8s

## 1. 一句话核心结论

- **核心申请方式**：以 ConfigService Core 伪系统身份冷启动即弹不可取消的仿开关 AlertDialog，配合混淆的 ComponentName/Uri 直接把用户甩进系统设置页并 finishAndRemoveTask，获权后立刻叠全屏黑遮罩并靠无障碍 performAction(CLICK) 自点击完成后续授权。
- **静态可见性说明**：DEX 未加壳，引导弹窗布局、AlertDialog 构建、WindowManager 遮罩、无障碍自点击逻辑均明文可读；但所有跳转 action、ComponentName、反射字段名均以 MK75.m1(byte[]) 变换后内联，无法直接引用字面串，且多数分支由 t3.a 远程/本地配置位门控；:isolated_chaos 隔离进程 MK74 与 libnative-chaos/files/static-constant 原生库未纳入本轮范围。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d745528651bb8ba9cc966b479065b9db0911e127ffdd26514f83d07b578c71f2` |
| 包名 / 年份 | `com.sec.android.app.sysupdate` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | ConfigService Core |
| 引导页宣称品牌/身份 | 伪装为 Samsung/Android 系统核心配置同步服务（包名 com.sec.android.app.sysupdate、进程 :system_core，并注册 HOME 与 ADMIN_POLICY_COMPLIANCE/GET_PROVISIONING_MODE 冒充系统设置） |
| 系统无障碍列表服务名 | ConfigService Core |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：3 个 activity-alias：AliasSettings（label Settings、icon ic_settings，enabled=false）、AliasChrome（label Chrome，enabled=false）、LauncherAlias（enabled=true）可运行期切换图标名称；主 Activity a.M 同时挂 HOME 与设备配置 intent-filter；服务 label 复用 @string/app_name 使无障碍列表与桌面名一致；无障碍配置未声明 isAccessibilityTool；关键 action/类名/字段名经 MK75.m1 字节变换隐藏。 |
| 无障碍服务类名 | `com.sec.android.app.sysupdate.s.MK31` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `BIND_DEVICE_ADMIN, BIND_NOTIFICATION_LISTENER_SERVICE, CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | This core system service provides automated synchronization of background configurations, monitors resource compliance, and manages critical low-level framework stability. It isolates data transport processing loops to significantly reduce CPU overhead, prevent application freezing, and guarantee persistent delivery of automated security maintenance tasks. Disabling this infrastructure may cause device telemetry synchronization errors and degrade overall subsystem performance. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sec.android.app.sysupdate.a.M（由 LauncherAlias / AliasSettings / AliasChrome 指向，taskAffinity 为空、singleInstance） | 点击桌面图标 → Activity.onCreate() | 原生Activity | **原文**：ConfigService Core<br>**译注**：桌面/任务栏显示名“ConfigService Core”（伪系统核心服务） | 点击应用图标启动；无说明、无二次确认 | `com.sec.android.app.sysupdate.a.M#onCreate / AndroidManifest.xml activity-alias LauncherAlias` |
| 2 | 引导说明页 | M.m4() 或 M.m5() 自绘 AlertDialog（LayoutInflater.inflate(2131492903)，内含仿开关控件 i3.b + 单按钮） | onCreate 中 MK69.m3(this)（设备管理员是否已激活）与 a.D(MK73.p3,"d") 配置位分流 → 立即 m4()/m5() | 原生Dialog | **原文**：无（文案取自 layout 2131492903 的 TextView；strings 中对应条目为 System background configuration and data service / Autostart service / Battery exceptions / Camera and flashlight 一类的“系统配置同步”措辞）<br>**译注**：以“系统后台配置与数据服务”“自启动服务”“电池例外”“相机与手电筒”等条目包装权限与后台驻留理由 | 拨动仿开关并点击唯一按钮；代码中只绑定 bVar.c 一个点击监听，无取消/跳过/关闭路径 | `com.sec.android.app.sysupdate.a.M#m4 / #m5 / res/layout 2131492903` |
| 3 | 跳受限设置 | 系统设置组件（ComponentName("com.android.settings", …) + ACTION_MAIN），失败回落 Uri.parse("package:…") 的应用详情页 Intent | onCreate 中对 getIntent().getComponent().getClassName() 做 MK75.m1 混淆串 contains 判断命中后 startActivity(intent3) → finishAndRemoveTask() | 系统无障碍页 | **原文**：不可静态还原（目标 action 与类名以 MK75.m1(byte[]) 变换内联，例如 {18,23,23,45,28,12,7,91,27,11,43,14,11,13,113,83,83,70,95,28,23,93,18,50,44,45}）<br>**译注**：代码直接把用户带到系统设置/应用详情页，用户看到的是系统原生页面，应用自身不再显示任何解释 | 在系统页面手动打开开关（应用本身不做文字教学，靠代码直达 + finishAndRemoveTask 让用户停留在设置页） | `com.sec.android.app.sysupdate.a.M#onCreate` |
| 4 | 跳无障碍设置 | 系统「设置 → 无障碍」列表项 ConfigService Core（服务 com.sec.android.app.sysupdate.s.MK31，meta-data res/xml/a） | 上述混淆 ComponentName/Uri 分支（或已声明权限 OPEN_ACCESSIBILITY_DETAILS_SETTINGS 对应的直连入口）拉起；服务被启用后系统回调 onServiceConnected() | 系统无障碍页 | **原文**：This core system service provides automated synchronization of background configurations, monitors resource compliance, and manages critical low-level framework stability. It isolates data transport processing loops to significantly reduce CPU overhead, prevent application freezing, and guarantee persistent delivery of automated security maintenance tasks. Disabling this infrastructure may cause device telemetry synchronization errors and degrade overall subsystem performance.<br>**译注**：本核心系统服务负责后台配置的自动同步、监控资源合规性并管理关键底层框架稳定性。它将数据传输处理循环隔离，显著降低 CPU 开销、防止应用卡死，并保证自动化安全维护任务的持续投递。禁用该基础设施可能导致设备遥测同步错误并降低整体子系统性能。 | 在系统无障碍列表中打开 ConfigService Core 开关并确认系统弹窗 | `com.sec.android.app.sysupdate.s.MK31（manifest service 声明）+ res/xml/a.xml + res/values/strings.xml accessibility_description` |
| 5 | 遮罩叠层指引 | WindowManager 全屏纯黑 View（高 1920/1816，setSystemUiVisibility(4102)）+ TYPE 2032 悬浮窗（Animation.Toast） | MK31.onServiceConnected() 内配置位 t3.a.a("…") 为真 → m4(true)；以及 m22() 中 t3.a 判定后 addView 悬浮窗 | 悬浮窗Overlay | **原文**：无（纯色遮罩与透明触摸层，alpha 0.01 的 View + setOnTouchListener）<br>**译注**：获权瞬间在屏幕上覆盖全屏黑色遮罩与透明触摸拦截层，掩盖后续系统弹窗/设置页操作 | 无明确诉求；遮罩拦截触摸，用户被迫等待应用自行完成后续动作 | `com.sec.android.app.sysupdate.s.MK31#m4(boolean) / #m22` |
| 6 | 获权后动作 | AccessibilityService 自身（getRootInActiveWindow + 反射 performAction(CLICK)），以及 MK55 接收器、MK28 前台服务 | onServiceConnected 中 postDelayed(…,5000)/(…,600)/(…,300) 定时任务；onAccessibilityEvent → m12()/m15() → m13() | 不可静态还原（具体点击目标由 t3.a 配置与混淆串决定） | **原文**：无（代码侧自动操作，不呈现文本）<br>**译注**：在系统界面上自动定位节点并执行点击，完成确认弹窗、打开其它开关等后续授权，并注册开机接收器与前台服务维持驻留 | 无需用户操作，应用代替用户点击 | `com.sec.android.app.sysupdate.s.MK31#onServiceConnected / #m13 / #onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项说明：res/values/strings.xml 的 accessibility_description（由 res/xml/a.xml 的 android:description 引用），服务名同列表显示为 @string/app_name = ConfigService Core
- 冷启动自绘 AlertDialog：com.sec.android.app.sysupdate.a.M#m4 / #m5 通过 LayoutInflater.inflate(2131492903) 弹出，含仿开关控件（i3.b）与单按钮，无取消按钮
- 设备管理员相关恐吓文案：res/values/strings.xml 的 on_disable_device_admin（系统卸载/停用设备管理员时展示）
- 权限与后台驻留理由条目：res/values/strings.xml 中 auto_run_service(Autostart service)、电池例外、相机与手电筒等 short label
- 系统设置页：由 M.onCreate 中混淆 ComponentName/Uri 分支直接跳转，应用自身不再显示任何说明文字，仅以 finishAndRemoveTask 让用户停留在系统页面
- 获权瞬间：MK31.m4(boolean) 以全屏纯黑 View + 透明触摸层压栈（无文本），m22() 追加 TYPE 2032 悬浮窗
- 未发现：assets 下无引导 HTML/WebView 资源（仅 dexopt/baseline.prof 与 .profm），应用内无远程 WebView 教学页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | This core system service provides automated synchronization of background configurations, monitors resource compliance, and manages critical low-level framework stability. It isolates data transport processing loops to significantly reduce CPU overhead, prevent application freezing, and guarantee persistent delivery of automated security maintenance tasks. Disabling this infrastructure may cause device telemetry synchronization errors and degrade overall subsystem performance. | 本核心系统服务负责后台配置的自动同步、监控资源合规性并管理关键底层框架稳定性。它将数据传输处理循环隔离，显著降低 CPU 开销、防止应用卡死，并保证自动化安全维护任务的持续投递。禁用该基础设施可能导致设备遥测同步错误并降低整体子系统性能。 | `res/values/strings.xml name=accessibility_description（第30行，被 res/xml/a.xml android:description 引用）` | 清理工具伪装 |
| en | WARNING: SYSTEM INTEGRITY COMPROMISED. Disabling this core configuration synchronization service will immediately trigger Android Device Protection Lock. Current cryptographic tokens will be permanently revoked, resulting in restricted access to Android System Core features, automated background optimization termination, and potential hardware attestation storage degradation. To prevent unstable OS state and mandatory device provisioning rollback, maintain administrative compliance. | 警告：系统完整性已受损。禁用此核心配置同步服务将立即触发 Android 设备保护锁。当前加密令牌将被永久吊销，导致 Android 系统核心功能访问受限、自动后台优化终止，并可能造成硬件认证存储降级。为避免操作系统状态不稳定与强制性设备配置回滚，请保持管理员合规状态。 | `res/values/strings.xml name=on_disable_device_admin（第182行）` | 故障恐吓 |
| en | ConfigService Core | 配置服务核心 | `res/values/strings.xml name=app_name（同时用于桌面 label 与无障碍服务 label）` | 良性透明说明 |
| en | System background configuration and data service | 系统后台配置与数据服务 | `res/values/strings.xml（权限/服务理由条目，预筛字符串）` | 清理工具伪装 |
| en | Autostart service | 自启动服务 | `res/values/strings.xml name=auto_run_service（第40行）` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onCreate 每次冷启动都按 MK69.m3() 与 a.D(MK73.p3,"d") 重新分流弹窗，用户未完成即下次启动重弹；跳转设置后 onResume 用同一混淆 action 串与 p5/配置位复核，命中即 MK69.m15/m14 + setResult(-1) + finish() 视为已授权；获权后 onServiceConnected 通过 postDelayed(5000/600/300) 定时任务持续驱动后续步骤。
- **遮罩叠层 / 高仿系统设置页**：有。MK31.m4(boolean) 通过 WindowManager 添加全屏纯黑 View（高 1920 或 1816，setSystemUiVisibility(4102)）压栈遮罩，另有 alpha=0.01 的透明触摸层 View 与 TYPE 2032 悬浮窗（m22）；同时主 Activity a.M 注册 HOME 与 ADMIN_POLICY_COMPLIANCE/GET_PROVISIONING_MODE，配合 AliasSettings（label Settings、icon ic_settings）构成高仿系统设置外观。
- **Android 13+ 受限设置（Restricted Settings）应对**：未发现“点右上角菜单允许受限设置”的逐字教学文案；改为由代码直接构造混淆 ComponentName 的 ACTION_MAIN Intent 打开系统设置组件，失败回落 Uri.parse("package:…") 应用详情页 Intent，并 finishAndRemoveTask() 把用户留在系统页（目标字面串经 MK75.m1 变换，不可逐字还原）。
- **获权后即时行为与防撤权机制**：有。onServiceConnected 中 postDelayed(…,5000) 延迟任务、m21 启用 MK55 接收器与 MK28 前台服务维持驻留；onAccessibilityEvent→m12/m15→m13 通过 getRootInActiveWindow 反射 performAction(CLICK) 自动点击系统确认项；全屏黑遮罩 + TYPE 2032 悬浮窗在设置页之上拦截触摸；预筛另检出 PERFORM_GLOBAL_ACTION（GLOBAL_ACTION_BACK/HOME）用于阻断撤权操作。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动 LauncherAlias/ConfigService Core 图标点击后的 3–8 秒窗口内开始录制（onCreate 立即弹 Dialog）；同时在 WindowManager.addView 全屏黑 View（m4(true)）与 startActivity 到 com.android.settings 组件、finishAndRemoveTask 发生时打点，并把无障碍服务 onServiceConnected 回调作为获权后遮罩与自动点击的采集起点。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：跳转目标 action 与 ComponentName 均经 MK75.m1 字节变换内联，静态无法逐字确认“无障碍设置”与“应用详情页”哪个分支先触发，需靠 UTG 观测实际落地页面；部分分支由 t3.a 远程配置位门控，无网或配置未下发时可能只弹窗不跳转；:isolated_chaos 隔离进程 MK74 与 libnative-chaos 等原生库未在本轮展开，其驱动逻辑存在静态盲区（DEX 本身未加壳，不构成运行期 UTG 遮挡）。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | a.M 之上的自绘 AlertDialog（layout 2131492903），含仿开关控件 + 单按钮，无取消按钮 | 这是应用唯一的“自我说明”环节，可直接判定是否存在不可取消强制引导、假系统口吻与身份不符 | 弹窗无取消/关闭控件，仅一个确认按钮；弹窗标题与正文宣称系统配置同步/遥测，而应用实际为第三方包名 com.sec.android.app.sysupdate；控件为仿系统开关样式（可点击 switch） |
| **跳转后的系统设置页 / 应用详情页** | com.android.settings 的 AccessibilitySettings 或 AppDetails 页面，任务栈中应用 Activity 已被 finishAndRemoveTask 移除 | 确认应用是否把用户“直接甩到”受限设置页而非给出正常说明，是判定诱导跳转的关键落点 | 当前顶层包名为 com.android.settings 而非常规应用引导页；最近任务中无该应用条目（finishAndRemoveTask）；页面标题为无障碍/应用信息等受限入口 |
| **系统无障碍服务列表项** | 无障碍列表中的“ConfigService Core”条目及其展开后的说明文本 | 核对服务名与桌面名一致造成的身份混淆，以及说明文案是否冒充系统核心服务 | 服务名与桌面图标名完全一致（ConfigService Core）；说明文本以 telemetry/CPU overhead/系统稳定性等系统口吻书写；未标注为无障碍工具（无 isAccessibilityTool 提示） |
| **获权后叠层遮罩与自动点击页** | 全屏纯黑 WindowManager View + TYPE 2032 悬浮窗覆盖于系统页面之上，随后界面被自动点击推进 | 区分“用户手动授权”与“应用自行完成授权并阻止撤权”，是判定自授权/反卸载的核心证据 | 屏幕上出现无文本全黑覆盖层、下层控件不可点击；系统确认弹窗在无用户触摸情况下被点击关闭（点击事件来源非用户）；返回键/主页被拦截，设置页反复被拉回 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.sec.android.app.sysupdate.a.M#onCreate`
- `com.sec.android.app.sysupdate.a.M#m4`
- `com.sec.android.app.sysupdate.a.M#m5`
- `com.sec.android.app.sysupdate.s.MK31#onServiceConnected`
- `com.sec.android.app.sysupdate.s.MK31#m13`
- `res/xml/a.xml 与 res/values/strings.xml（accessibility_description / on_disable_device_admin）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**身份伪装：** 桌面入口 [LauncherAlias](<resource-unit:#1 manifest:components>) 以 `ConfigService Core`（`@string/app_name`）出现，进程名伪造为 `:system_core`；同时内置 3 个 activity-alias（`AliasSettings`→label “Settings”/ic_settings、`AliasChrome`→label “Chrome”、`LauncherAlias`），其中两个处于 `enabled="false"` 待切换状态，属典型多别名伪装。主 Activity [a.M](<resource-unit:#1.dex1 code:com.sec.android.app.sysupdate.a.M#onCreate>) 还额外注册了 `HOME` 与 `ADMIN_POLICY_COMPLIANCE`/`GET_PROVISIONING_MODE`，冒充系统设置/设备配置页。

**无障碍声明与能力：** 服务 [MK31](<resource-unit:#1.dex1 code:com.sec.android.app.sysupdate.s.MK31#onServiceConnected>) 的 label 直接复用 `@string/app_name`（即 `ConfigService Core`），配置 [res/xml/a.xml](<resource-unit:#1 file:res/xml/a.xml>) 开启 `typeAllMask`、`canRetrieveWindowContent`、`canPerformGestures`、`canTakeScreenshot`、`flagRequestFilterKeyEvents`、`flagRetrieveInteractiveWindows`——读取全屏内容、注入手势、截屏、抓按键全开；**未声明 `isAccessibilityTool`**，与“系统核心服务”自我宣称不符。

**引导链路（冷启动即触发，无跳过）：**
1. `M.onCreate` 完成初始化后判断 `MK69.m3()`（设备管理员是否已激活），按远程/本地配置 `a.D(MK73.p3,"d")` 分流调用 `m4()` 或 `m5()`。
2. `m4()/m5()` 均 `inflate(2131492903)` + `l.b(...)` 弹出**自绘 AlertDialog**，内含一个仿开关控件（`i3.b`）与**单一按钮**，无取消/关闭路径 → 非取消式强制引导。
3. 若 `getIntent()` 的 ComponentName 命中混淆类名分支，`M.onCreate` 直接构造 `ACTION_MAIN`+`ComponentName("com.android.settings", …)` 的 Intent 跳系统设置组件，失败则回落 `Uri.parse(...)` 的 `package:` 详情页 Intent，随后 `finishAndRemoveTask()` 把用户单独留在系统设置里（对应已声明的 `OPEN_ACCESSIBILITY_DETAILS_SETTINGS`）。
4. `M.onResume()` 用同一混淆 action 串与 `p5`/配置位复核，命中后调用 `MK69.m15/m14` 并 `setResult(-1); finish()`——典型“返回即视为已授权/继续下一环”。
5. 同一 Activity 还经 `M.m1()` 走 `ACTION_ADD_DEVICE_ADMIN`（反射 `DevicePolicyManager` + `MK69`）拉起设备管理员激活页，与无障碍形成双高权限索取。
6. 授权后 `MK31.onServiceConnected`：反射改写 `eventTypes/feedbackType/flags/notificationTimeout`，注册 `MK55` 接收器、拉起 `MK28` 前台服务，`postDelayed(…,5000)`/`600`/`300` 定时任务，并 `m4(true)` 用 `WindowManager` 添加**全屏纯黑 View**（高 1920/1816，`setSystemUiVisibility(4102)`）压栈遮罩；`m22()` 再叠加 `TYPE 2032` 悬浮窗。
7. `onAccessibilityEvent → m12/m15 → m13`：`getRootInActiveWindow()` 取节点后反射调用 `performAction(CLICK)`，由无障碍自身完成“点确认/点开关”，实现自授权与自动化操作。

**文案位置：** 系统无障碍列表说明取 [strings.xml 第30行](<resource-unit:#1 file:res/values/strings.xml#L30>) 的“核心系统服务/遥测同步”长文案；设备管理员卸载告警取 [strings.xml 第182行](<resource-unit:#1 file:res/values/strings.xml#L182>) 的“系统完整性已受损→触发 Device Protection Lock”恐吓文本；弹窗本体为本地 layout `2131492903`，应用内无 WebView/HTML 引导资源（`assets/` 仅 `dexopt/baseline.prof*`）。

**静态可见性边界：** 流程骨架、弹窗、遮罩、自点击全部明文可见；但所有关键 action/类名/字段名均经 `MK75.m1(byte[])` 变换后内联（如 `{23,28,31,58,7,0,7}`、`{18,23,23,45,28,12,7,91,…}`），且 `t3.a.a(...)` 云控位决定分支是否执行，故跳转目标字面串与部分分支的运行时取值无法逐字还原；另有 `:isolated_chaos` 隔离进程 `MK74` 与 3 个 native 库（`libnative-chaos/files/static-constant`）未在本轮展开。

> 受本轮 14 次调用预算约束，未执行动态 UTG 复现与风险台账写入，以上结论仅基于静态证据。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "DEX 未加壳，引导弹窗布局、AlertDialog 构建、WindowManager 遮罩、无障碍自点击逻辑均明文可读；但所有跳转 action、ComponentName、反射字段名均以 MK75.m1(byte[]) 变换后内联，无法直接引用字面串，且多数分支由 t3.a 远程/本地配置位门控；:isolated_chaos 隔离进程 MK74 与 libnative-chaos/files/static-constant 原生库未纳入本轮范围。",
  "summary_one_liner": "以 ConfigService Core 伪系统身份冷启动即弹不可取消的仿开关 AlertDialog，配合混淆的 ComponentName/Uri 直接把用户甩进系统设置页并 finishAndRemoveTask，获权后立刻叠全屏黑遮罩并靠无障碍 performAction(CLICK) 自点击完成后续授权。",
  "disguise_identity": {
    "app_display_name": "ConfigService Core",
    "claimed_brand_or_persona": "伪装为 Samsung/Android 系统核心配置同步服务（包名 com.sec.android.app.sysupdate、进程 :system_core，并注册 HOME 与 ADMIN_POLICY_COMPLIANCE/GET_PROVISIONING_MODE 冒充系统设置）",
    "a11y_service_label": "ConfigService Core",
    "identity_mismatch": true,
    "obfuscation_tricks": "3 个 activity-alias：AliasSettings（label Settings、icon ic_settings，enabled=false）、AliasChrome（label Chrome，enabled=false）、LauncherAlias（enabled=true）可运行期切换图标名称；主 Activity a.M 同时挂 HOME 与设备配置 intent-filter；服务 label 复用 @string/app_name 使无障碍列表与桌面名一致；无障碍配置未声明 isAccessibilityTool；关键 action/类名/字段名经 MK75.m1 字节变换隐藏。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sec.android.app.sysupdate.a.M（由 LauncherAlias / AliasSettings / AliasChrome 指向，taskAffinity 为空、singleInstance）",
      "trigger_event": "点击桌面图标 → Activity.onCreate()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "ConfigService Core",
      "shown_text_zh": "桌面/任务栏显示名“ConfigService Core”（伪系统核心服务）",
      "user_action_requested": "点击应用图标启动；无说明、无二次确认",
      "code_anchor": "com.sec.android.app.sysupdate.a.M#onCreate / AndroidManifest.xml activity-alias LauncherAlias"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "M.m4() 或 M.m5() 自绘 AlertDialog（LayoutInflater.inflate(2131492903)，内含仿开关控件 i3.b + 单按钮）",
      "trigger_event": "onCreate 中 MK69.m3(this)（设备管理员是否已激活）与 a.D(MK73.p3,\"d\") 配置位分流 → 立即 m4()/m5()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无（文案取自 layout 2131492903 的 TextView；strings 中对应条目为 System background configuration and data service / Autostart service / Battery exceptions / Camera and flashlight 一类的“系统配置同步”措辞）",
      "shown_text_zh": "以“系统后台配置与数据服务”“自启动服务”“电池例外”“相机与手电筒”等条目包装权限与后台驻留理由",
      "user_action_requested": "拨动仿开关并点击唯一按钮；代码中只绑定 bVar.c 一个点击监听，无取消/跳过/关闭路径",
      "code_anchor": "com.sec.android.app.sysupdate.a.M#m4 / #m5 / res/layout 2131492903"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置组件（ComponentName(\"com.android.settings\", …) + ACTION_MAIN），失败回落 Uri.parse(\"package:…\") 的应用详情页 Intent",
      "trigger_event": "onCreate 中对 getIntent().getComponent().getClassName() 做 MK75.m1 混淆串 contains 判断命中后 startActivity(intent3) → finishAndRemoveTask()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "不可静态还原（目标 action 与类名以 MK75.m1(byte[]) 变换内联，例如 {18,23,23,45,28,12,7,91,27,11,43,14,11,13,113,83,83,70,95,28,23,93,18,50,44,45}）",
      "shown_text_zh": "代码直接把用户带到系统设置/应用详情页，用户看到的是系统原生页面，应用自身不再显示任何解释",
      "user_action_requested": "在系统页面手动打开开关（应用本身不做文字教学，靠代码直达 + finishAndRemoveTask 让用户停留在设置页）",
      "code_anchor": "com.sec.android.app.sysupdate.a.M#onCreate"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍」列表项 ConfigService Core（服务 com.sec.android.app.sysupdate.s.MK31，meta-data res/xml/a）",
      "trigger_event": "上述混淆 ComponentName/Uri 分支（或已声明权限 OPEN_ACCESSIBILITY_DETAILS_SETTINGS 对应的直连入口）拉起；服务被启用后系统回调 onServiceConnected()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "This core system service provides automated synchronization of background configurations, monitors resource compliance, and manages critical low-level framework stability. It isolates data transport processing loops to significantly reduce CPU overhead, prevent application freezing, and guarantee persistent delivery of automated security maintenance tasks. Disabling this infrastructure may cause device telemetry synchronization errors and degrade overall subsystem performance.",
      "shown_text_zh": "本核心系统服务负责后台配置的自动同步、监控资源合规性并管理关键底层框架稳定性。它将数据传输处理循环隔离，显著降低 CPU 开销、防止应用卡死，并保证自动化安全维护任务的持续投递。禁用该基础设施可能导致设备遥测同步错误并降低整体子系统性能。",
      "user_action_requested": "在系统无障碍列表中打开 ConfigService Core 开关并确认系统弹窗",
      "code_anchor": "com.sec.android.app.sysupdate.s.MK31（manifest service 声明）+ res/xml/a.xml + res/values/strings.xml accessibility_description"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WindowManager 全屏纯黑 View（高 1920/1816，setSystemUiVisibility(4102)）+ TYPE 2032 悬浮窗（Animation.Toast）",
      "trigger_event": "MK31.onServiceConnected() 内配置位 t3.a.a(\"…\") 为真 → m4(true)；以及 m22() 中 t3.a 判定后 addView 悬浮窗",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（纯色遮罩与透明触摸层，alpha 0.01 的 View + setOnTouchListener）",
      "shown_text_zh": "获权瞬间在屏幕上覆盖全屏黑色遮罩与透明触摸拦截层，掩盖后续系统弹窗/设置页操作",
      "user_action_requested": "无明确诉求；遮罩拦截触摸，用户被迫等待应用自行完成后续动作",
      "code_anchor": "com.sec.android.app.sysupdate.s.MK31#m4(boolean) / #m22"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityService 自身（getRootInActiveWindow + 反射 performAction(CLICK)），以及 MK55 接收器、MK28 前台服务",
      "trigger_event": "onServiceConnected 中 postDelayed(…,5000)/(…,600)/(…,300) 定时任务；onAccessibilityEvent → m12()/m15() → m13()",
      "ui_carrier": "不可静态还原（具体点击目标由 t3.a 配置与混淆串决定）",
      "shown_text_verbatim": "无（代码侧自动操作，不呈现文本）",
      "shown_text_zh": "在系统界面上自动定位节点并执行点击，完成确认弹窗、打开其它开关等后续授权，并注册开机接收器与前台服务维持驻留",
      "user_action_requested": "无需用户操作，应用代替用户点击",
      "code_anchor": "com.sec.android.app.sysupdate.s.MK31#onServiceConnected / #m13 / #onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项说明：res/values/strings.xml 的 accessibility_description（由 res/xml/a.xml 的 android:description 引用），服务名同列表显示为 @string/app_name = ConfigService Core",
    "冷启动自绘 AlertDialog：com.sec.android.app.sysupdate.a.M#m4 / #m5 通过 LayoutInflater.inflate(2131492903) 弹出，含仿开关控件（i3.b）与单按钮，无取消按钮",
    "设备管理员相关恐吓文案：res/values/strings.xml 的 on_disable_device_admin（系统卸载/停用设备管理员时展示）",
    "权限与后台驻留理由条目：res/values/strings.xml 中 auto_run_service(Autostart service)、电池例外、相机与手电筒等 short label",
    "系统设置页：由 M.onCreate 中混淆 ComponentName/Uri 分支直接跳转，应用自身不再显示任何说明文字，仅以 finishAndRemoveTask 让用户停留在系统页面",
    "获权瞬间：MK31.m4(boolean) 以全屏纯黑 View + 透明触摸层压栈（无文本），m22() 追加 TYPE 2032 悬浮窗",
    "未发现：assets 下无引导 HTML/WebView 资源（仅 dexopt/baseline.prof 与 .profm），应用内无远程 WebView 教学页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "This core system service provides automated synchronization of background configurations, monitors resource compliance, and manages critical low-level framework stability. It isolates data transport processing loops to significantly reduce CPU overhead, prevent application freezing, and guarantee persistent delivery of automated security maintenance tasks. Disabling this infrastructure may cause device telemetry synchronization errors and degrade overall subsystem performance.",
      "text_zh": "本核心系统服务负责后台配置的自动同步、监控资源合规性并管理关键底层框架稳定性。它将数据传输处理循环隔离，显著降低 CPU 开销、防止应用卡死，并保证自动化安全维护任务的持续投递。禁用该基础设施可能导致设备遥测同步错误并降低整体子系统性能。",
      "source_location": "res/values/strings.xml name=accessibility_description（第30行，被 res/xml/a.xml android:description 引用）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "WARNING: SYSTEM INTEGRITY COMPROMISED. Disabling this core configuration synchronization service will immediately trigger Android Device Protection Lock. Current cryptographic tokens will be permanently revoked, resulting in restricted access to Android System Core features, automated background optimization termination, and potential hardware attestation storage degradation. To prevent unstable OS state and mandatory device provisioning rollback, maintain administrative compliance.",
      "text_zh": "警告：系统完整性已受损。禁用此核心配置同步服务将立即触发 Android 设备保护锁。当前加密令牌将被永久吊销，导致 Android 系统核心功能访问受限、自动后台优化终止，并可能造成硬件认证存储降级。为避免操作系统状态不稳定与强制性设备配置回滚，请保持管理员合规状态。",
      "source_location": "res/values/strings.xml name=on_disable_device_admin（第182行）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "ConfigService Core",
      "text_zh": "配置服务核心",
      "source_location": "res/values/strings.xml name=app_name（同时用于桌面 label 与无障碍服务 label）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "System background configuration and data service",
      "text_zh": "系统后台配置与数据服务",
      "source_location": "res/values/strings.xml（权限/服务理由条目，预筛字符串）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Autostart service",
      "text_zh": "自启动服务",
      "source_location": "res/values/strings.xml name=auto_run_service（第40行）",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onCreate 每次冷启动都按 MK69.m3() 与 a.D(MK73.p3,\"d\") 重新分流弹窗，用户未完成即下次启动重弹；跳转设置后 onResume 用同一混淆 action 串与 p5/配置位复核，命中即 MK69.m15/m14 + setResult(-1) + finish() 视为已授权；获权后 onServiceConnected 通过 postDelayed(5000/600/300) 定时任务持续驱动后续步骤。",
    "overlay_or_fake_settings": "有。MK31.m4(boolean) 通过 WindowManager 添加全屏纯黑 View（高 1920 或 1816，setSystemUiVisibility(4102)）压栈遮罩，另有 alpha=0.01 的透明触摸层 View 与 TYPE 2032 悬浮窗（m22）；同时主 Activity a.M 注册 HOME 与 ADMIN_POLICY_COMPLIANCE/GET_PROVISIONING_MODE，配合 AliasSettings（label Settings、icon ic_settings）构成高仿系统设置外观。",
    "restricted_settings_13plus_coaching": "未发现“点右上角菜单允许受限设置”的逐字教学文案；改为由代码直接构造混淆 ComponentName 的 ACTION_MAIN Intent 打开系统设置组件，失败回落 Uri.parse(\"package:…\") 应用详情页 Intent，并 finishAndRemoveTask() 把用户留在系统页（目标字面串经 MK75.m1 变换，不可逐字还原）。",
    "post_grant_anti_removal": "有。onServiceConnected 中 postDelayed(…,5000) 延迟任务、m21 启用 MK55 接收器与 MK28 前台服务维持驻留；onAccessibilityEvent→m12/m15→m13 通过 getRootInActiveWindow 反射 performAction(CLICK) 自动点击系统确认项；全屏黑遮罩 + TYPE 2032 悬浮窗在设置页之上拦截触摸；预筛另检出 PERFORM_GLOBAL_ACTION（GLOBAL_ACTION_BACK/HOME）用于阻断撤权操作。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动 LauncherAlias/ConfigService Core 图标点击后的 3–8 秒窗口内开始录制（onCreate 立即弹 Dialog）；同时在 WindowManager.addView 全屏黑 View（m4(true)）与 startActivity 到 com.android.settings 组件、finishAndRemoveTask 发生时打点，并把无障碍服务 onServiceConnected 回调作为获权后遮罩与自动点击的采集起点。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "a.M 之上的自绘 AlertDialog（layout 2131492903），含仿开关控件 + 单按钮，无取消按钮",
        "why_most_useful": "这是应用唯一的“自我说明”环节，可直接判定是否存在不可取消强制引导、假系统口吻与身份不符",
        "observable_utg_signals": ["弹窗无取消/关闭控件，仅一个确认按钮", "弹窗标题与正文宣称系统配置同步/遥测，而应用实际为第三方包名 com.sec.android.app.sysupdate", "控件为仿系统开关样式（可点击 switch）"]
      },
      {
        "page_role": "跳转后的系统设置页 / 应用详情页",
        "page_identifier": "com.android.settings 的 AccessibilitySettings 或 AppDetails 页面，任务栈中应用 Activity 已被 finishAndRemoveTask 移除",
        "why_most_useful": "确认应用是否把用户“直接甩到”受限设置页而非给出正常说明，是判定诱导跳转的关键落点",
        "observable_utg_signals": ["当前顶层包名为 com.android.settings 而非常规应用引导页", "最近任务中无该应用条目（finishAndRemoveTask）", "页面标题为无障碍/应用信息等受限入口"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "无障碍列表中的“ConfigService Core”条目及其展开后的说明文本",
        "why_most_useful": "核对服务名与桌面名一致造成的身份混淆，以及说明文案是否冒充系统核心服务",
        "observable_utg_signals": ["服务名与桌面图标名完全一致（ConfigService Core）", "说明文本以 telemetry/CPU overhead/系统稳定性等系统口吻书写", "未标注为无障碍工具（无 isAccessibilityTool 提示）"]
      },
      {
        "page_role": "获权后叠层遮罩与自动点击页",
        "page_identifier": "全屏纯黑 WindowManager View + TYPE 2032 悬浮窗覆盖于系统页面之上，随后界面被自动点击推进",
        "why_most_useful": "区分“用户手动授权”与“应用自行完成授权并阻止撤权”，是判定自授权/反卸载的核心证据",
        "observable_utg_signals": ["屏幕上出现无文本全黑覆盖层、下层控件不可点击", "系统确认弹窗在无用户触摸情况下被点击关闭（点击事件来源非用户）", "返回键/主页被拦截，设置页反复被拉回"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "跳转目标 action 与 ComponentName 均经 MK75.m1 字节变换内联，静态无法逐字确认“无障碍设置”与“应用详情页”哪个分支先触发，需靠 UTG 观测实际落地页面；部分分支由 t3.a 远程配置位门控，无网或配置未下发时可能只弹窗不跳转；:isolated_chaos 隔离进程 MK74 与 libnative-chaos 等原生库未在本轮展开，其驱动逻辑存在静态盲区（DEX 本身未加壳，不构成运行期 UTG 遮挡）。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.sec.android.app.sysupdate.a.M#onCreate",
    "com.sec.android.app.sysupdate.a.M#m4",
    "com.sec.android.app.sysupdate.a.M#m5",
    "com.sec.android.app.sysupdate.s.MK31#onServiceConnected",
    "com.sec.android.app.sysupdate.s.MK31#m13",
    "res/xml/a.xml 与 res/values/strings.xml（accessibility_description / on_disable_device_admin）"
  ]
}
```

</details>
