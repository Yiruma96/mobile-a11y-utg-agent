# MR_168__2d8c7e26be｜Anubis — MX Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：113.6s

## 1. 一句话核心结论

- **核心申请方式**：该应用把无障碍服务伪装成系统级“Google Play Protect”，用不可取消的“系统故障/需要授权”弹窗加居中 Toast 文案引导，并通过后台定时服务每 700ms 反复强跳空白 Activity 打开系统无障碍设置页直至用户开启，获权后即监听全部事件做键盘记录并用 HOME+假系统错误弹窗阻断卸载。
- **静态可见性说明**：无障碍引导链、跳转 Intent、弹窗文案、Toast 文案全部在 classes.dex 明文可见，无加壳/无 DEX 加密/无 AES 二阶段载荷；仅 (1) Activity.lbdeyt 在 b.n 为真时用 WebView 加载服务端下发的 URL（b.o，来自远程配置）作为外壳页，(2) StringActivate/StringAccessibility/StringPermis 等提示文案默认硬编码于本地化字符串表 a.h/a.i/a.j，但可被远程 settings 接口（/private/getSettingsAll.php、setAllSettings.php）覆盖，故运行期实际文案可能变化。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `2d8c7e26be34608a9a78a7b9d0f8252f1ee7a910fbb540521f49af0c6ad513a8` |
| 包名 / 年份 | `ivo.baxkjggmgror.itiukv` / 2019 |
| 家族 / 品类 | **Anubis**（同池样本数：9） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | MX Player |
| 引导页宣称品牌/身份 | Google Play Protect（系统安全组件）；应用层同时冒充 MX Player 播放器 |
| 系统无障碍列表服务名 | Google Play Protect |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务类名与包内全部类名均为随机串（ivo.baxkjggmgror.itiukv.fkzjuttsqgbgcv）；android:label 直接写成 Google Play Protect；无障碍配置文件 res/xml/lgceikil.xml 残留原始开发工程包名 settingsActivity=com.example.root.myapplication.MainActivity；无障碍服务无 android:description（系统列表中不出现任何能力说明）；大量 Activity 的 label 置为空字符串并使用 @drawable/im 图标；ipnqp 等跳转 Activity 无可见 UI（setContentView 后立即 finish），使跳转过程无自有页面可识别；获权后用 HOME 键 + 'Sorry!/System Error 495' 假故障弹窗阻止卸载。 |
| 无障碍服务类名 | `ivo.baxkjggmgror.itiukv.fkzjuttsqgbgcv` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | ivo.baxkjggmgror.itiukv.Activity.lbdeyt（LAUNCHER Activity） | onCreate：startService(ipu)；若配置 b.n 为真则 new WebView + loadUrl(b.o)（远程 URL）覆盖界面；随后 setComponentEnabledSetting(lbdeyt, DISABLED) 自禁用并注册 Alarm 周期任务 | 远端WebView | **原文**：无（默认分支无界面，直接 startService + finish）<br>**译注**：默认情况下启动后无任何可见页面，转入后台服务；若服务端下发外壳 URL 则用 WebView 展示该远程页面 | 无显式交互；用户仅感知到“点开应用后闪退/无反应” | `ivo.baxkjggmgror.itiukv.Activity.lbdeyt#onCreate` |
| 2 | 引导说明页 | android.app.AlertDialog（由 ivo.baxkjggmgror.itiukv.c#c 构造，statistic 分支） | 后台/Activity 触发 c.c(context, "statistic")（由 Activity.bpmqrqohmttr/bqznoqviiezwos/jmfmnhanv、ipu$1.run、zwdtdo.a 等 20+ 处调用） | 原生Dialog | **原文**：Title: "Get permission"  Message: "The system does not work correctly, you need to enable access to the statistics 'MX Player'"  Button: "Enable now"  (setCancelable(false))<br>**译注**：标题“获取权限”，正文“系统无法正常工作，你需要开启对使用情况统计的访问权限 'MX Player'”，按钮“立即开启”；弹窗不可取消、无跳过/关闭按钮 | 只能点“Enable now”进入系统使用情况访问授权页；返回键被 setCancelable(false) 屏蔽 | `ivo.baxkjggmgror.itiukv.c#c(Context, String)` |
| 3 | 跳受限设置 | 系统页面 android.settings.USAGE_ACCESS_SETTINGS | c$1.onClick(DialogInterface, int) → startActivity(Intent("android.settings.USAGE_ACCESS_SETTINGS")) 后 dialog.cancel() | 系统无障碍页 | **原文**：无自有文案<br>**译注**：直接跳到系统“使用情况访问权限”列表页，由用户为 MX Player 手动打开开关 | 在系统页中为应用打开“使用情况访问权限”；无引导叠层，用户可拒绝并返回 | `ivo.baxkjggmgror.itiukv.c$1#onClick` |
| 4 | 遮罩叠层指引 | 居中 Toast（由服务 ivo.baxkjggmgror.itiukv.vpdfi.onStartCommand 弹出） | acuxuram.onHandleIntent 跳转 ipnqp 的同时 startService(vpdfi)（首次 d==0 时） | 悬浮窗Overlay | **原文**：this.a.d(this,"StringAccessibility") + " '" + "Google Play Protect" + "'"  →  "Enable access for 'Google Play Protect'"<br>**译注**：“为 'Google Play Protect' 开启访问权限”——用系统安全组件名冒充，诱使用户在无障碍列表里勾选该项 | 无按钮，仅提示；用户被引导在系统无障碍列表中查找并开启名为 Google Play Protect 的服务 | `ivo.baxkjggmgror.itiukv.vpdfi#onStartCommand` |
| 5 | 跳无障碍设置 | ivo.baxkjggmgror.itiukv.Activity.ipnqp（无 UI 空白 Activity，label 为空）→ 系统 android.settings.ACCESSIBILITY_SETTINGS | acuxuram.onHandleIntent：!c.g()（服务未启用）且（s==1/5/6 或 startRequest 含 Access=1）→ startActivity(ipnqp, FLAG_ACTIVITY_NEW_TASK\|FLAG_ACTIVITY_CLEAR_TASK)；ipnqp.onCreate → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) → finish() | 系统无障碍页 | **原文**：无自有文案（ipnqp 仅 setContentView(2130968576) 后立刻跳转并 finish）<br>**译注**：应用自身不展示任何说明页，直接弹出系统“无障碍”设置列表 | 在系统无障碍列表中点击“Google Play Protect”并确认授权；页面无应用侧取消/跳过入口 | `ivo.baxkjggmgror.itiukv.Activity.ipnqp#onCreate` |
| 6 | 拒权反馈循环 | acuxuram（IntentService）+ ipu/AlarmManager 周期任务 + ipnqp 反复重跳 | onHandleIntent 内 TimeUnit.MILLISECONDS.sleep(700) 后再次 startActivity(ipnqp)；计数 d 超过 25 后归 -1 继续；外层由 c.a(context,"startAlarm", Interval) 定时重启；c.g() 检测 getEnabledAccessibilityServiceList(-1) 中是否含本服务 | 系统无障碍页 | **原文**：无自有文案（循环仅重复跳转与 Toast）<br>**译注**：用户返回或拒绝后，约 0.7 秒即被重新拉回系统无障碍设置页，最多 25 次一轮，并由定时任务无限续期 | 无法通过返回键退出该循环，只能开启无障碍或强制停止应用 | `ivo.baxkjggmgror.itiukv.acuxuram#onHandleIntent` |
| 7 | 获权后动作 | ivo.baxkjggmgror.itiukv.fkzjuttsqgbgcv（AccessibilityService）+ 反卸载弹窗 Activity.wxhzuiwqtk | onServiceConnected 设 AccessibilityServiceInfo(eventTypes=-1, flags=1, feedbackType=16) 并累加 time_start_permission；onAccessibilityEvent 采集 TEXT/FOCUSED/按键文本写入 KEY1/KEY2/KEY3 并 POST /private/datakeylogger.php；a() 先发 HOME Intent 再 startActivity(wxhzuiwqtk,"blockDelete") | 原生Dialog | **原文**：Title: "Sorry!"  Message: "System Error 495"  Button: "ОК"  (setCancelable(false))<br>**译注**：获权后一旦用户试图进入应用详情卸载，应用先回桌面再弹出不可取消的“抱歉！系统错误 495”，伪装系统故障阻止卸载 | 只能点“ОК”，无法卸载；键盘与界面文本被持续记录并外传 | `ivo.baxkjggmgror.itiukv.fkzjuttsqgbgcv#onServiceConnected / #a()` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 居中 Toast：ivo.baxkjggmgror.itiukv.vpdfi.onStartCommand 弹出 "Enable access for 'Google Play Protect'"（setGravity(16,0,0)，Toast.LENGTH_SHORT），在跳无障碍设置的同时出现
- 不可取消系统 AlertDialog（使用情况统计引导）：ivo.baxkjggmgror.itiukv.c#c("statistic")，标题 "Get permission"、正文 "The system does not work correctly, you need to enable access to the statistics 'MX Player'"、唯一按钮 "Enable now"（俄/土/德/意/法/乌克兰语多语言分支同构）
- 不可取消系统 AlertDialog（定位引导）：ivo.baxkjggmgror.itiukv.c#c("gps")，标题 "Geolocation"、正文 "For correct operation of the system, you need to get the coordinates, you need to enable geolocation"、按钮 "Enable now"
- 不可取消系统 AlertDialog（反卸载）：ivo.baxkjggmgror.itiukv.Activity.wxhzuiwqtk#onCreate，标题 "Sorry!"、正文 "System Error 495"、按钮 "ОК"
- 系统无障碍列表项标签：AndroidManifest.xml 中 service fkzjuttsqgbgcv 的 android:label="Google Play Protect"（无 android:description，故系统列表不显示任何能力说明）
- 本地化字符串表（可被远程覆盖）：ivo.baxkjggmgror.itiukv.a 的字段 h/i/j/k，含 "[en]Enable access for"、"[ru]…"、"[zh]…" 等 80+ 语言映射，由 c#b(Context) 按 Locale 写入 StringAccessibility/StringActivate/StringPermis/StringYes
- 空白跳转载体：Activity.ipnqp（label 为空、icon=@drawable/im）不承载任何引导文字，只做 setContentView + 跳转 + finish

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable access for 'Google Play Protect' | 为 'Google Play Protect' 开启访问权限 | `ivo.baxkjggmgror.itiukv.vpdfi#onStartCommand（拼接 c.d(ctx,"StringAccessibility") 默认值 "Enable access for" 与硬编码 "Google Play Protect"）` | 假反诈安全 |
| en | Get permission | 获取权限 | `ivo.baxkjggmgror.itiukv.c#c(Context,String) statistic 分支 setTitle` | 故障恐吓 |
| en | The system does not work correctly, you need to enable access to the statistics 'MX Player' | 系统无法正常工作，你需要开启对使用情况统计的访问权限 'MX Player' | `ivo.baxkjggmgror.itiukv.c#c(Context,String) statistic 分支 setMessage（应用名由 c.i(context) 动态取得）` | 故障恐吓 |
| en | Enable now | 立即开启 | `ivo.baxkjggmgror.itiukv.c#c(Context,String) setNegativeButton` | 故障恐吓 |
| ru | Получить разрешение / Система не корректно работает, вам необходимо включить доступ к статистике 'MX Player' / Включить сейчас | 获取权限 / 系统运行不正常，您必须开启对统计的访问权限 'MX Player' / 立即开启 | `ivo.baxkjggmgror.itiukv.c#c(Context,String) RU 分支` | 故障恐吓 |
| en | Geolocation | 地理位置 | `ivo.baxkjggmgror.itiukv.c#c(Context,String) gps 分支 setTitle` | 故障恐吓 |
| en | For correct operation of the system, you need to get the coordinates, you need to enable geolocation | 为保证系统正常运行，需要获取坐标，您必须开启地理位置 | `ivo.baxkjggmgror.itiukv.c#c(Context,String) gps 分支 setMessage` | 故障恐吓 |
| en | Sorry! | 抱歉！ | `ivo.baxkjggmgror.itiukv.Activity.wxhzuiwqtk#onCreate setTitle` | 故障恐吓 |
| en | System Error 495 | 系统错误 495 | `ivo.baxkjggmgror.itiukv.Activity.wxhzuiwqtk#onCreate setMessage（setCancelable(false)，仅 "ОК" 按钮）` | 故障恐吓 |
| en | Google Play Protect | Google Play 保护机制（Google 官方安全组件名） | `AndroidManifest.xml service ivo.baxkjggmgror.itiukv.fkzjuttsqgbgcv 的 android:label` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：acuxuram.onHandleIntent 在 !c.g()（无障碍未启用）且满足 Access=1/策略位条件时，sleep(700) 后 startActivity(ipnqp) 强跳无障碍设置，计数 d 到 25 归 -1 无限续跳；ipnqp 无 UI、跳转后即 finish，用户返回桌面或从设置页退出都会被立即重新拉起。外层由 lbdeyt.onCreate 与 ipu.onHandleIntent 通过 c.a(context,"startAlarm", Interval) 注册 AlarmManager 周期广播（Receiver.ksenz）持续复活；另由 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON 等广播接收器（Receiver.hnnb）重启。系统页本身不叠加遮罩，但循环跳转构成事实上的强制。
- **遮罩叠层 / 高仿系统设置页**：无半透明遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅用居中 Toast "Enable access for 'Google Play Protect'" 做文字指引，随后直接拉起真实系统无障碍设置页（SYSTEM_ALERT_WINDOW 权限已声明但本链路未用于叠加遮罩）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。样本 targetSdkVersion=27（低于 30），未出现“应用详情→右上角菜单→允许受限设置”分步教学，也未使用 Session 安装器绕过；受限类权限（使用情况访问 PACKAGE_USAGE_STATS、电池优化白名单）通过故障恐吓弹窗 + 直接 startActivity("android.settings.USAGE_ACCESS_SETTINGS") 与 "android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS" 跳转实现。
- **获权后即时行为与防撤权机制**：获权后 fkzjuttsqgbgcv#onServiceConnected 立即设 eventTypes=-1、flags=1 监听全部无障碍事件并累加 time_start_permission；fkzjuttsqgbgcv#a() 先 startActivity(HOME) 回桌面，再 startActivity(wxhzuiwqtk,"blockDelete") 弹出 setCancelable(false) 的 "Sorry!/System Error 495" 弹窗阻断卸载流程；acuxuram 还会在 urls 为空且非设备管理员时跳 "android.settings.APPLICATION_DETAILS_SETTINGS"（deleteApp 分支），进入即触发上述反卸载弹窗；同时反复拉起设备管理器激活页（API.a.b）以获取卸载保护。
- **良性降级 / 替代方案**：无。未授权时不存在手动模式/仅观看模式/ADB 指引等降级路径，只有循环强跳。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 acuxuram.onHandleIntent 的 startActivity(Activity.ipnqp) 为最佳拦截点：一旦检测到从 IntentService 上下文以 FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TASK 拉起无 UI 的 ipnqp，或检测到应用调用 startActivity("android.settings.ACCESSIBILITY_SETTINGS") 时立即抓取整屏并录制 3–5 秒序列；同时抓取 Toast 出现瞬间（vpdfi 启动后）以记录 "Enable access for 'Google Play Protect'" 文案。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本样本引导文案均为原生文本节点（Toast/AlertDialog/系统列表项），UTG 可直接提取，无需 OCR。盲区在于：(1) 启动 Activity.lbdeyt 在配置 b.n 为真时会以 WebView 加载服务端下发的远程 URL（b.o），若该远端页承担说明文案则文本不在包内，需抓包或 WebView 文本节点补采；(2) 提示文案 StringAccessibility/StringActivate/StringPermis 可被远程 settings 接口覆盖，实际运行文案可能与静态默认值不同；(3) 应用无自有引导页（ipnqp 为空 Activity），若仅在“跳转前页面”采样会漏检，必须在系统设置页与 Toast 层采样。静态无加壳，运行期 UTG 不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（伪装项）** | 系统“无障碍/已下载的服务”列表中出现 label 为 "Google Play Protect"、无描述文字的服务条目（真实类名 fkzjuttsqgbgcv） | 这是用户被诱导勾选的最终落点，可同时验证服务名冒充与系统页无应用侧叠加遮罩两个关键事实 | 条目文本恰为 Google Play Protect 而应用自身为 MX Player；条目无 description 副标题；列表页顶部无应用自有引导视图/遮罩 |
| **跳转后 Toast 指引瞬间** | 屏幕正中（gravity=16）短暂出现的 "Enable access for 'Google Play Protect'" 文本节点 | 该 Toast 是应用唯一的口头引导文案，直接证明“品牌冒充 + 引导开启无障碍”的因果 | 居中位置的短时文本节点含 Enable access for 与 Google Play Protect；Toast 与系统无障碍页同屏出现 |
| **拒权后重跳循环序列** | 连续多次（间隔约 700ms）出现 ipnqp 空白 Activity 切换至系统无障碍页的屏幕变化 | 证明无取消/跳过路径与死循环强制，是区分“良性说明”与“诱导强制”的核心证据 | 0.5–1s 内反复出现同一系统设置页；期间无应用自有页面停留；按返回键后页面被再次压栈 |
| **冷启动引导弹窗页（使用情况统计）** | 不可取消 AlertDialog：标题 Get permission、正文含 "statistics 'MX Player'"、按钮 Enable now | 验证“系统故障恐吓 + 无跳过按钮”的受限设置引导手法，并与无障碍跳转形成完整链 | 弹窗仅有单个按钮且返回键无效；正文出现 statistics 与真实应用名 MX Player 的组合；点击后进入系统使用情况访问页 |
| **获权后反卸载假故障弹窗** | 标题 Sorry!、正文 System Error 495、按钮 ОК 的不可取消弹窗，出现前屏幕先回到桌面 | 证明获权后立即转为反卸载保护，闭环恶意目的 | 进入应用详情/卸载路径后先跳桌面再弹窗；弹窗无取消按钮；弹窗文本为伪造系统错误码 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `ivo.baxkjggmgror.itiukv.Activity.ipnqp#onCreate`
- `ivo.baxkjggmgror.itiukv.acuxuram#onHandleIntent`
- `ivo.baxkjggmgror.itiukv.vpdfi#onStartCommand`
- `ivo.baxkjggmgror.itiukv.c#c(Context, String)`
- `ivo.baxkjggmgror.itiukv.c$1#onClick`
- `res/xml/lgceikil.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **完全静态可见**：引导链全部在 DEX 明文实现，无加壳、无加密载荷、无本地/远端 HTML 教学页（仅启动 Activity 有一个可选 WebView 通道）。
- **身份伪装明确**：桌面名 `MX Player`，无障碍服务在系统列表中显示为 **`Google Play Protect`**，而服务类名是随机串 `fkzjuttsqgbgcv`；其 `res/xml/lgceikil.xml` 还残留开发者工程的 `settingsActivity="com.example.root.myapplication.MainActivity"`。
- **核心跳转极简且强制**：`Activity.ipnqp`（无标题、无 UI 的空白 Activity）在 `onCreate` 里立刻 `startActivity("android.settings.ACCESSIBILITY_SETTINGS")` 并 `finish()`，用户从来看不到自有引导页——**引导文字全靠 Toast + 一个不可取消的“系统故障”弹窗**。
- **引导文案**：`vpdfi.onStartCommand` 弹出居中 Toast：`"Enable access for" + " 'Google Play Protect'"`（文案取自本地化字符串表，可由服务端配置覆盖）。
- **受限设置（使用情况访问）用故障恐吓**：`c.c(ctx,"statistic")` 构造 `setCancelable(false)`、仅一个按钮的 AlertDialog，标题 `Get permission`，正文“系统不能正常工作，你需要开启对统计的访问权限 'MX Player'”，按钮 `Enable now` → `android.settings.USAGE_ACCESS_SETTINGS`。
- **拒权反馈循环**：`acuxuram.onHandleIntent` 每 ~700ms 睡眠后重跳 `ipnqp`（`NEW_TASK|CLEAR_TASK`），最多 25 次；再经 `AlarmManager` 周期任务反复重启，形成“回到桌面/退出设置即被重新拉起”的死循环。
- **获权后立即转为窃密与反卸载**：`fkzjuttsqgbgcv.onServiceConnected` 设 `eventTypes=-1`、`flags=1`（监听全部事件），`onAccessibilityEvent` 把文本/焦点内容按 `KEY1/KEY2/KEY3` 写入并 POST 到 `/private/datakeylogger.php`；`fkzjuttsqgbgcv.a()` 先回 HOME 再弹 `Sorry! / System Error 495` 不可取消弹窗，阻断进入应用详情卸载。
- 该样本与 Anubis 家族特征一致（C2 `https://ushxffxcdgff13ugyiugfebhjnhy.com`、`/private/*.php` 接口族、SMS 拦截/键盘记录/设备管理器/锁屏）。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链、跳转 Intent、弹窗文案、Toast 文案全部在 classes.dex 明文可见，无加壳/无 DEX 加密/无 AES 二阶段载荷；仅 (1) Activity.lbdeyt 在 b.n 为真时用 WebView 加载服务端下发的 URL（b.o，来自远程配置）作为外壳页，(2) StringActivate/StringAccessibility/StringPermis 等提示文案默认硬编码于本地化字符串表 a.h/a.i/a.j，但可被远程 settings 接口（/private/getSettingsAll.php、setAllSettings.php）覆盖，故运行期实际文案可能变化。",
  "summary_one_liner": "该应用把无障碍服务伪装成系统级“Google Play Protect”，用不可取消的“系统故障/需要授权”弹窗加居中 Toast 文案引导，并通过后台定时服务每 700ms 反复强跳空白 Activity 打开系统无障碍设置页直至用户开启，获权后即监听全部事件做键盘记录并用 HOME+假系统错误弹窗阻断卸载。",
  "disguise_identity": {
    "app_display_name": "MX Player",
    "claimed_brand_or_persona": "Google Play Protect（系统安全组件）；应用层同时冒充 MX Player 播放器",
    "a11y_service_label": "Google Play Protect",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务类名与包内全部类名均为随机串（ivo.baxkjggmgror.itiukv.fkzjuttsqgbgcv）；android:label 直接写成 Google Play Protect；无障碍配置文件 res/xml/lgceikil.xml 残留原始开发工程包名 settingsActivity=com.example.root.myapplication.MainActivity；无障碍服务无 android:description（系统列表中不出现任何能力说明）；大量 Activity 的 label 置为空字符串并使用 @drawable/im 图标；ipnqp 等跳转 Activity 无可见 UI（setContentView 后立即 finish），使跳转过程无自有页面可识别；获权后用 HOME 键 + 'Sorry!/System Error 495' 假故障弹窗阻止卸载。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "ivo.baxkjggmgror.itiukv.Activity.lbdeyt（LAUNCHER Activity）",
      "trigger_event": "onCreate：startService(ipu)；若配置 b.n 为真则 new WebView + loadUrl(b.o)（远程 URL）覆盖界面；随后 setComponentEnabledSetting(lbdeyt, DISABLED) 自禁用并注册 Alarm 周期任务",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无（默认分支无界面，直接 startService + finish）",
      "shown_text_zh": "默认情况下启动后无任何可见页面，转入后台服务；若服务端下发外壳 URL 则用 WebView 展示该远程页面",
      "user_action_requested": "无显式交互；用户仅感知到“点开应用后闪退/无反应”",
      "code_anchor": "ivo.baxkjggmgror.itiukv.Activity.lbdeyt#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "android.app.AlertDialog（由 ivo.baxkjggmgror.itiukv.c#c 构造，statistic 分支）",
      "trigger_event": "后台/Activity 触发 c.c(context, \"statistic\")（由 Activity.bpmqrqohmttr/bqznoqviiezwos/jmfmnhanv、ipu$1.run、zwdtdo.a 等 20+ 处调用）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: \"Get permission\"  Message: \"The system does not work correctly, you need to enable access to the statistics 'MX Player'\"  Button: \"Enable now\"  (setCancelable(false))",
      "shown_text_zh": "标题“获取权限”，正文“系统无法正常工作，你需要开启对使用情况统计的访问权限 'MX Player'”，按钮“立即开启”；弹窗不可取消、无跳过/关闭按钮",
      "user_action_requested": "只能点“Enable now”进入系统使用情况访问授权页；返回键被 setCancelable(false) 屏蔽",
      "code_anchor": "ivo.baxkjggmgror.itiukv.c#c(Context, String)"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统页面 android.settings.USAGE_ACCESS_SETTINGS",
      "trigger_event": "c$1.onClick(DialogInterface, int) → startActivity(Intent(\"android.settings.USAGE_ACCESS_SETTINGS\")) 后 dialog.cancel()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无自有文案",
      "shown_text_zh": "直接跳到系统“使用情况访问权限”列表页，由用户为 MX Player 手动打开开关",
      "user_action_requested": "在系统页中为应用打开“使用情况访问权限”；无引导叠层，用户可拒绝并返回",
      "code_anchor": "ivo.baxkjggmgror.itiukv.c$1#onClick"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "居中 Toast（由服务 ivo.baxkjggmgror.itiukv.vpdfi.onStartCommand 弹出）",
      "trigger_event": "acuxuram.onHandleIntent 跳转 ipnqp 的同时 startService(vpdfi)（首次 d==0 时）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "this.a.d(this,\"StringAccessibility\") + \" '\" + \"Google Play Protect\" + \"'\"  →  \"Enable access for 'Google Play Protect'\"",
      "shown_text_zh": "“为 'Google Play Protect' 开启访问权限”——用系统安全组件名冒充，诱使用户在无障碍列表里勾选该项",
      "user_action_requested": "无按钮，仅提示；用户被引导在系统无障碍列表中查找并开启名为 Google Play Protect 的服务",
      "code_anchor": "ivo.baxkjggmgror.itiukv.vpdfi#onStartCommand"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "ivo.baxkjggmgror.itiukv.Activity.ipnqp（无 UI 空白 Activity，label 为空）→ 系统 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "acuxuram.onHandleIntent：!c.g()（服务未启用）且（s==1/5/6 或 startRequest 含 Access=1）→ startActivity(ipnqp, FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TASK)；ipnqp.onCreate → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")) → finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无自有文案（ipnqp 仅 setContentView(2130968576) 后立刻跳转并 finish）",
      "shown_text_zh": "应用自身不展示任何说明页，直接弹出系统“无障碍”设置列表",
      "user_action_requested": "在系统无障碍列表中点击“Google Play Protect”并确认授权；页面无应用侧取消/跳过入口",
      "code_anchor": "ivo.baxkjggmgror.itiukv.Activity.ipnqp#onCreate"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "acuxuram（IntentService）+ ipu/AlarmManager 周期任务 + ipnqp 反复重跳",
      "trigger_event": "onHandleIntent 内 TimeUnit.MILLISECONDS.sleep(700) 后再次 startActivity(ipnqp)；计数 d 超过 25 后归 -1 继续；外层由 c.a(context,\"startAlarm\", Interval) 定时重启；c.g() 检测 getEnabledAccessibilityServiceList(-1) 中是否含本服务",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无自有文案（循环仅重复跳转与 Toast）",
      "shown_text_zh": "用户返回或拒绝后，约 0.7 秒即被重新拉回系统无障碍设置页，最多 25 次一轮，并由定时任务无限续期",
      "user_action_requested": "无法通过返回键退出该循环，只能开启无障碍或强制停止应用",
      "code_anchor": "ivo.baxkjggmgror.itiukv.acuxuram#onHandleIntent"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "ivo.baxkjggmgror.itiukv.fkzjuttsqgbgcv（AccessibilityService）+ 反卸载弹窗 Activity.wxhzuiwqtk",
      "trigger_event": "onServiceConnected 设 AccessibilityServiceInfo(eventTypes=-1, flags=1, feedbackType=16) 并累加 time_start_permission；onAccessibilityEvent 采集 TEXT/FOCUSED/按键文本写入 KEY1/KEY2/KEY3 并 POST /private/datakeylogger.php；a() 先发 HOME Intent 再 startActivity(wxhzuiwqtk,\"blockDelete\")",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: \"Sorry!\"  Message: \"System Error 495\"  Button: \"ОК\"  (setCancelable(false))",
      "shown_text_zh": "获权后一旦用户试图进入应用详情卸载，应用先回桌面再弹出不可取消的“抱歉！系统错误 495”，伪装系统故障阻止卸载",
      "user_action_requested": "只能点“ОК”，无法卸载；键盘与界面文本被持续记录并外传",
      "code_anchor": "ivo.baxkjggmgror.itiukv.fkzjuttsqgbgcv#onServiceConnected / #a()"
    }
  ],
  "text_presentation_locations": [
    "居中 Toast：ivo.baxkjggmgror.itiukv.vpdfi.onStartCommand 弹出 \"Enable access for 'Google Play Protect'\"（setGravity(16,0,0)，Toast.LENGTH_SHORT），在跳无障碍设置的同时出现",
    "不可取消系统 AlertDialog（使用情况统计引导）：ivo.baxkjggmgror.itiukv.c#c(\"statistic\")，标题 \"Get permission\"、正文 \"The system does not work correctly, you need to enable access to the statistics 'MX Player'\"、唯一按钮 \"Enable now\"（俄/土/德/意/法/乌克兰语多语言分支同构）",
    "不可取消系统 AlertDialog（定位引导）：ivo.baxkjggmgror.itiukv.c#c(\"gps\")，标题 \"Geolocation\"、正文 \"For correct operation of the system, you need to get the coordinates, you need to enable geolocation\"、按钮 \"Enable now\"",
    "不可取消系统 AlertDialog（反卸载）：ivo.baxkjggmgror.itiukv.Activity.wxhzuiwqtk#onCreate，标题 \"Sorry!\"、正文 \"System Error 495\"、按钮 \"ОК\"",
    "系统无障碍列表项标签：AndroidManifest.xml 中 service fkzjuttsqgbgcv 的 android:label=\"Google Play Protect\"（无 android:description，故系统列表不显示任何能力说明）",
    "本地化字符串表（可被远程覆盖）：ivo.baxkjggmgror.itiukv.a 的字段 h/i/j/k，含 \"[en]Enable access for\"、\"[ru]…\"、\"[zh]…\" 等 80+ 语言映射，由 c#b(Context) 按 Locale 写入 StringAccessibility/StringActivate/StringPermis/StringYes",
    "空白跳转载体：Activity.ipnqp（label 为空、icon=@drawable/im）不承载任何引导文字，只做 setContentView + 跳转 + finish"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable access for 'Google Play Protect'",
      "text_zh": "为 'Google Play Protect' 开启访问权限",
      "source_location": "ivo.baxkjggmgror.itiukv.vpdfi#onStartCommand（拼接 c.d(ctx,\"StringAccessibility\") 默认值 \"Enable access for\" 与硬编码 \"Google Play Protect\"）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Get permission",
      "text_zh": "获取权限",
      "source_location": "ivo.baxkjggmgror.itiukv.c#c(Context,String) statistic 分支 setTitle",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "The system does not work correctly, you need to enable access to the statistics 'MX Player'",
      "text_zh": "系统无法正常工作，你需要开启对使用情况统计的访问权限 'MX Player'",
      "source_location": "ivo.baxkjggmgror.itiukv.c#c(Context,String) statistic 分支 setMessage（应用名由 c.i(context) 动态取得）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable now",
      "text_zh": "立即开启",
      "source_location": "ivo.baxkjggmgror.itiukv.c#c(Context,String) setNegativeButton",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Получить разрешение / Система не корректно работает, вам необходимо включить доступ к статистике 'MX Player' / Включить сейчас",
      "text_zh": "获取权限 / 系统运行不正常，您必须开启对统计的访问权限 'MX Player' / 立即开启",
      "source_location": "ivo.baxkjggmgror.itiukv.c#c(Context,String) RU 分支",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Geolocation",
      "text_zh": "地理位置",
      "source_location": "ivo.baxkjggmgror.itiukv.c#c(Context,String) gps 分支 setTitle",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "For correct operation of the system, you need to get the coordinates, you need to enable geolocation",
      "text_zh": "为保证系统正常运行，需要获取坐标，您必须开启地理位置",
      "source_location": "ivo.baxkjggmgror.itiukv.c#c(Context,String) gps 分支 setMessage",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Sorry!",
      "text_zh": "抱歉！",
      "source_location": "ivo.baxkjggmgror.itiukv.Activity.wxhzuiwqtk#onCreate setTitle",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "System Error 495",
      "text_zh": "系统错误 495",
      "source_location": "ivo.baxkjggmgror.itiukv.Activity.wxhzuiwqtk#onCreate setMessage（setCancelable(false)，仅 \"ОК\" 按钮）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play Protect",
      "text_zh": "Google Play 保护机制（Google 官方安全组件名）",
      "source_location": "AndroidManifest.xml service ivo.baxkjggmgror.itiukv.fkzjuttsqgbgcv 的 android:label",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "acuxuram.onHandleIntent 在 !c.g()（无障碍未启用）且满足 Access=1/策略位条件时，sleep(700) 后 startActivity(ipnqp) 强跳无障碍设置，计数 d 到 25 归 -1 无限续跳；ipnqp 无 UI、跳转后即 finish，用户返回桌面或从设置页退出都会被立即重新拉起。外层由 lbdeyt.onCreate 与 ipu.onHandleIntent 通过 c.a(context,\"startAlarm\", Interval) 注册 AlarmManager 周期广播（Receiver.ksenz）持续复活；另由 BOOT_COMPLETED/USER_PRESENT/SCREEN_ON 等广播接收器（Receiver.hnnb）重启。系统页本身不叠加遮罩，但循环跳转构成事实上的强制。",
    "overlay_or_fake_settings": "无半透明遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅用居中 Toast \"Enable access for 'Google Play Protect'\" 做文字指引，随后直接拉起真实系统无障碍设置页（SYSTEM_ALERT_WINDOW 权限已声明但本链路未用于叠加遮罩）。",
    "restricted_settings_13plus_coaching": "无。样本 targetSdkVersion=27（低于 30），未出现“应用详情→右上角菜单→允许受限设置”分步教学，也未使用 Session 安装器绕过；受限类权限（使用情况访问 PACKAGE_USAGE_STATS、电池优化白名单）通过故障恐吓弹窗 + 直接 startActivity(\"android.settings.USAGE_ACCESS_SETTINGS\") 与 \"android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS\" 跳转实现。",
    "post_grant_anti_removal": "获权后 fkzjuttsqgbgcv#onServiceConnected 立即设 eventTypes=-1、flags=1 监听全部无障碍事件并累加 time_start_permission；fkzjuttsqgbgcv#a() 先 startActivity(HOME) 回桌面，再 startActivity(wxhzuiwqtk,\"blockDelete\") 弹出 setCancelable(false) 的 \"Sorry!/System Error 495\" 弹窗阻断卸载流程；acuxuram 还会在 urls 为空且非设备管理员时跳 \"android.settings.APPLICATION_DETAILS_SETTINGS\"（deleteApp 分支），进入即触发上述反卸载弹窗；同时反复拉起设备管理器激活页（API.a.b）以获取卸载保护。",
    "benign_graceful_degradation": "无。未授权时不存在手动模式/仅观看模式/ADB 指引等降级路径，只有循环强跳。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 acuxuram.onHandleIntent 的 startActivity(Activity.ipnqp) 为最佳拦截点：一旦检测到从 IntentService 上下文以 FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TASK 拉起无 UI 的 ipnqp，或检测到应用调用 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\") 时立即抓取整屏并录制 3–5 秒序列；同时抓取 Toast 出现瞬间（vpdfi 启动后）以记录 \"Enable access for 'Google Play Protect'\" 文案。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（伪装项）",
        "page_identifier": "系统“无障碍/已下载的服务”列表中出现 label 为 \"Google Play Protect\"、无描述文字的服务条目（真实类名 fkzjuttsqgbgcv）",
        "why_most_useful": "这是用户被诱导勾选的最终落点，可同时验证服务名冒充与系统页无应用侧叠加遮罩两个关键事实",
        "observable_utg_signals": ["条目文本恰为 Google Play Protect 而应用自身为 MX Player", "条目无 description 副标题", "列表页顶部无应用自有引导视图/遮罩"]
      },
      {
        "page_role": "跳转后 Toast 指引瞬间",
        "page_identifier": "屏幕正中（gravity=16）短暂出现的 \"Enable access for 'Google Play Protect'\" 文本节点",
        "why_most_useful": "该 Toast 是应用唯一的口头引导文案，直接证明“品牌冒充 + 引导开启无障碍”的因果",
        "observable_utg_signals": ["居中位置的短时文本节点含 Enable access for 与 Google Play Protect", "Toast 与系统无障碍页同屏出现"]
      },
      {
        "page_role": "拒权后重跳循环序列",
        "page_identifier": "连续多次（间隔约 700ms）出现 ipnqp 空白 Activity 切换至系统无障碍页的屏幕变化",
        "why_most_useful": "证明无取消/跳过路径与死循环强制，是区分“良性说明”与“诱导强制”的核心证据",
        "observable_utg_signals": ["0.5–1s 内反复出现同一系统设置页", "期间无应用自有页面停留", "按返回键后页面被再次压栈"]
      },
      {
        "page_role": "冷启动引导弹窗页（使用情况统计）",
        "page_identifier": "不可取消 AlertDialog：标题 Get permission、正文含 \"statistics 'MX Player'\"、按钮 Enable now",
        "why_most_useful": "验证“系统故障恐吓 + 无跳过按钮”的受限设置引导手法，并与无障碍跳转形成完整链",
        "observable_utg_signals": ["弹窗仅有单个按钮且返回键无效", "正文出现 statistics 与真实应用名 MX Player 的组合", "点击后进入系统使用情况访问页"]
      },
      {
        "page_role": "获权后反卸载假故障弹窗",
        "page_identifier": "标题 Sorry!、正文 System Error 495、按钮 ОК 的不可取消弹窗，出现前屏幕先回到桌面",
        "why_most_useful": "证明获权后立即转为反卸载保护，闭环恶意目的",
        "observable_utg_signals": ["进入应用详情/卸载路径后先跳桌面再弹窗", "弹窗无取消按钮", "弹窗文本为伪造系统错误码"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本样本引导文案均为原生文本节点（Toast/AlertDialog/系统列表项），UTG 可直接提取，无需 OCR。盲区在于：(1) 启动 Activity.lbdeyt 在配置 b.n 为真时会以 WebView 加载服务端下发的远程 URL（b.o），若该远端页承担说明文案则文本不在包内，需抓包或 WebView 文本节点补采；(2) 提示文案 StringAccessibility/StringActivate/StringPermis 可被远程 settings 接口覆盖，实际运行文案可能与静态默认值不同；(3) 应用无自有引导页（ipnqp 为空 Activity），若仅在“跳转前页面”采样会漏检，必须在系统设置页与 Toast 层采样。静态无加壳，运行期 UTG 不受影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "ivo.baxkjggmgror.itiukv.Activity.ipnqp#onCreate",
    "ivo.baxkjggmgror.itiukv.acuxuram#onHandleIntent",
    "ivo.baxkjggmgror.itiukv.vpdfi#onStartCommand",
    "ivo.baxkjggmgror.itiukv.c#c(Context, String)",
    "ivo.baxkjggmgror.itiukv.c$1#onClick",
    "res/xml/lgceikil.xml"
  ]
}
```

</details>
