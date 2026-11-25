# MR_069__53b6cba100｜Anubis — Flash Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：148.5s

## 1. 一句话核心结论

- **核心申请方式**：以 'Flash Player' 为名、图标自禁用后由后台 Alarm 循环驱动，用无说明文案的 Activity 直接静默跳转 ACCESSIBILITY_SETTINGS，再叠加云端可配置的居中 Toast 'Enable access for Flash Player Service' 引导开启，获权后立即监听全部无障碍事件做键盘记录并弹假系统错误阻止卸载。
- **静态可见性说明**：DEX 完整可读、未加壳；跳转点、弹窗构建、Toast 逻辑均静态可见。但无障碍引导文案（StringAccessibility 默认 'Enable access for'、straccessibility、StringActivate、StringYes、uninstall1/2、vkladmin）与启动器 WebView 的 URL（SharedPreferences 键 urls，默认 https://comicwalker.at）均由 C2 下发覆盖；ecw 引导 Toast 服务在包内无静态调用点，触发链（远端指令/导出组件）不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `53b6cba10003af1392b9f30c98699b891711ffb94be2812d184a40abfd890641` |
| 包名 / 年份 | `kovvkynlzyyy.dfpn.iablbixbxg` / 2019 |
| 家族 / 品类 | **Anubis**（同池样本数：9） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | Flash Player |
| 引导页宣称品牌/身份 | Flash Player（冒充 Adobe Flash Player 播放器） |
| 系统无障碍列表服务名 | Flash Player Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：全部类名/包名随机化（kovvkynlzyyy.dfpn.iablbixbxg、gameaitvkv、qycizhfz.vchruwbih 等）；launcher Activity 首次运行后 setComponentEnabledSetting(DISABLED) 自禁用，图标从桌面消失以躲避用户排查；多个 Activity 声明 android:label="" 空标签、excludeFromRecents=true、launchMode=2（singleTask）避免出现在最近任务；无障碍 service 的 android:description 缺失（预筛为空），系统列表仅显示 'Flash Player Service' 名称而不给用途说明。 |
| 无障碍服务类名 | `kovvkynlzyyy.dfpn.iablbixbxg.gameaitvkv` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty（LAUNCHER Activity） | 用户点击桌面图标 onCreate() | 原生Activity | **原文**：无（setContentView(2130968580) 后立即 finish 或加载远端 WebView）<br>**译注**：无可读引导界面；若远端开关 b.n 为 true 则整屏替换为 WebView 加载服务端 URL | 无提示，用户仅看到一闪而过的界面；无取消/跳过按钮 | `kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty.onCreate` |
| 2 | 冷启动入口 | 同 launcher Activity 自禁用 + Alarm 注册 + IntentService kovvkynlzyyy.dfpn.iablbixbxg.dokmzmwozhpobpu | onCreate 末尾 setComponentEnabledSetting(自身, 2, 1)、a.a(this,"startAlarm",Interval) 默认 10000ms、finish() | 不可静态还原 | 无 | 无 | `kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty.onCreate` |
| 3 | 拒权反馈循环 | dokmzmwozhpobpu.onHandleIntent 轮询 + a.g(Context) 检测无障碍是否开启 | Alarm 每 Interval（默认 10s）唤醒，TimeUnit.MILLISECONDS.sleep 后判断 getEnabledAccessibilityServiceList 中是否存在 '包名/gameaitvkv' | 不可静态还原 | 无 | 无显式请求；用户返回后仍会被再次拉起 | `kovvkynlzyyy.dfpn.iablbixbxg.dokmzmwozhpobpu.onHandleIntent / kovvkynlzyyy.dfpn.iablbixbxg.a#g` |
| 4 | 跳受限设置 | qycizhfz.zsgtf（start=deleteApp）→ 系统「应用详情」页 | dokmzmwozhpobpu 在 urls 为空且设备管理器未激活时 startActivity(zsgtf, "start"="deleteApp")，zsgtf.onCreate 再 startActivity(APPLICATION_DETAILS_SETTINGS, package:自身) | 系统无障碍页 | 无 | 无文案要求；实际效果是把用户带到可点「强行停止/卸载」的位置以便反制或劫持返回 | `kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf.onCreate` |
| 5 | 引导说明页 | a.c(Context,"statistic") 不可取消 AlertDialog | zsgtf 收到 start=statistic（或后台下发）调用 aVar.c(this,"statistic")，按系统 Locale 选择语言分支后 dialog.show() | 原生Dialog | **原文**：Get permission / The system does not work correctly, you need to enable access to the statistics '<应用名>' / Enable now<br>**译注**：获取权限 / 系统运行不正常，您需要开启对统计信息的访问权限 '<应用名>' / 立即开启 | 仅一个 NegativeButton「Enable now」，setCancelable(false)，无取消/跳过；点击后 a$1.onClick 跳 android.settings.USAGE_ACCESS_SETTINGS | `kovvkynlzyyy.dfpn.iablbixbxg.a#c(Context, String) + kovvkynlzyyy.dfpn.iablbixbxg.a$1#onClick` |
| 6 | 跳无障碍设置 | qycizhfz.vchruwbih → 系统「无障碍」设置页（android.settings.ACCESSIBILITY_SETTINGS） | 该 Activity onCreate() 中 setContentView 之后无条件 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))；异常时 finish() | 系统无障碍页 | **原文**：无（本应用不提供任何说明文字，直接跳系统页）<br>**译注**：静默跳转到系统无障碍服务列表，用户只能看到系统列表里名为 'Flash Player Service' 的条目 | 用户需自行在系统列表中点击 'Flash Player Service' 并打开开关；本页无取消/跳过按钮，也无引导说明 | `kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.vchruwbih#onCreate` |
| 7 | 遮罩叠层指引 | 导出服务 kovvkynlzyyy.dfpn.iablbixbxg.ecw.onStartCommand 弹出的居中 Toast（覆盖在系统无障碍页上方） | ecw 被启动（exported=true，包内未发现静态调用点，推测由远端指令/其他导出组件拉起）后 onStartCommand | 悬浮窗Overlay | **原文**：Enable access for 'Flash Player Service'<br>**译注**：为 'Flash Player Service' 开启访问权限 | 提示用户在系统无障碍列表中找到并开启同名服务；无取消按钮（Toast 自动消失但由定时器重复拉起） | `kovvkynlzyyy.dfpn.iablbixbxg.ecw#onStartCommand（文案来自 a.d(this,"StringAccessibility")，默认 "Enable access for"）` |
| 8 | 获权后动作 | gameaitvkv.onServiceConnected / onAccessibilityEvent（键盘记录 + POST /private/datakeylogger.php） | 用户在系统设置中开启服务 → onServiceConnected；之后任意窗口事件触发 onAccessibilityEvent | 不可静态还原 | **原文**：无界面；数据侧字符串 'SEND KEL' / 'LOGER'<br>**译注**：开启后立即全量监听无障碍事件，把各界面文本累积写入 keys.log，超过 10000 字符即加密上传到 /private/datakeylogger.php | 无 | `kovvkynlzyyy.dfpn.iablbixbxg.gameaitvkv#onServiceConnected / kovvkynlzyyy.dfpn.iablbixbxg.gameaitvkv#onAccessibilityEvent` |
| 9 | 拒权反馈循环 | gameaitvkv.a() → HOME + qycizhfz.zsgtf(start=blockDelete) 不可取消 AlertDialog | 无障碍服务在检测到卸载/设置页时调用 a()：先 startActivity(ACTION_MAIN/CATEGORY_HOME) 回桌面，再弹假错误框 | 原生Dialog | **原文**：Sorry! / System Error 495 / ОК<br>**译注**：抱歉！/ 系统错误 495 / 确定 | 只能点「ОК」，setCancelable(false)，点后 finish()，用于打断用户撤权/卸载流程 | `kovvkynlzyyy.dfpn.iablbixbxg.gameaitvkv#a() + kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf#onCreate（blockDelete 分支）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务标签 'Flash Player Service'（AndroidManifest 中 service android:label，且 android:description 缺失，无用途说明）
- 覆盖在系统无障碍设置页上方的居中 Toast（Gravity=16）: "Enable access for 'Flash Player Service'"，由导出服务 ecw.onStartCommand 弹出，文案可由 C2 通过 SharedPreferences 键 StringAccessibility 改写
- 原生不可取消 AlertDialog（a.c(Context,"statistic")）: 标题 'Get permission'，正文 'The system does not work correctly, you need to enable access to the statistics '<应用名>''，唯一按钮 'Enable now'
- 原生不可取消 AlertDialog（zsgtf blockDelete 分支）: 标题 'Sorry!'，正文 'System Error 495'，按钮 'ОК'
- qycizhfz.vchruwbih 承载 layout 2130968590 但无任何引导文案，onCreate 内立即跳转系统 ACCESSIBILITY_SETTINGS
- launcher Activity 在远端开关开启时整屏替换为 WebView，加载服务端下发 URL（默认 https://comicwalker.at），该页文案不在包内

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable access for 'Flash Player Service' | 为 'Flash Player Service' 开启访问权限 | `kovvkynlzyyy.dfpn.iablbixbxg.ecw#onStartCommand（拼接 a.d(ctx,"StringAccessibility") 默认值 "Enable access for" + 服务标签 "Flash Player Service"）` | 受限设置分步教学 |
| en | Get permission | 获取权限 | `kovvkynlzyyy.dfpn.iablbixbxg.a#c(Context,String) 硬编码（statistic 分支默认语言）` | 故障恐吓 |
| en | The system does not work correctly, you need to enable access to the statistics '<应用名>' | 系统运行不正常，您需要开启对统计信息的访问权限 '<应用名>' | `kovvkynlzyyy.dfpn.iablbixbxg.a#c(Context,String) 硬编码字符串拼接` | 故障恐吓 |
| en | Enable now | 立即开启 | `kovvkynlzyyy.dfpn:iablbixbxg.a#c(Context,String) setNegativeButton 文案（其余语言分支为 'Включить сейчас'/'Şimdi etkinleştir'/'Aktivieren Sie jetzt'/'Attiva ora'/'Activer maintenant' 等）` | 受限设置分步教学 |
| en | Sorry! | 抱歉！ | `kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf#onCreate（blockDelete 分支 AlertDialog.setTitle）` | 故障恐吓 |
| en | System Error 495 | 系统错误 495 | `kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf#onCreate（blockDelete 分支 AlertDialog.setMessage）` | 故障恐吓 |
| en | Enable access for | 为……开启访问权限 | `kovvkynlzyyy.dfpn.iablbixbxg.a#b(Context) 中 d(context,"StringAccessibility","Enable access for") 默认值；同处还初始化 "StringActivate"="activate"、"StringYes"、"uninstall1/2"、"vkladmin" 等服务端可覆盖文案` | 受限设置分步教学 |
| en | activate | 激活 | `kovvkynlzyyy.dfpn.iablbixbxg.a#b(Context) d(context,"StringActivate","activate")；c.h 数组为 100+ 语言 'activate' 本地化表` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：后台 dokmzmwozhpobpu 由 startAlarm（默认 10s，可由服务端 Interval 调整）周期唤醒，循环内 a.g(Context) 用 getEnabledAccessibilityServiceList 判定未授权，即再次 startActivity 拉起 zsgtf→APPLICATION_DETAILS_SETTINGS 或无障碍跳转 Activity；用户按返回键不会终止该循环，只有服务被杀或授权成功才停止。
- **遮罩叠层 / 高仿系统设置页**：无高仿系统无障碍开关页；但在系统无障碍列表页之上叠放居中对齐（Gravity=16）的 Toast 提示 'Enable access for \'Flash Player Service\''，由导出服务 ecw 弹出，用于在系统页面之上补上本应用缺失的说明文字。
- **Android 13+ 受限设置（Restricted Settings）应对**：无；targetSdkVersion=27，未涉及 Android 13 受限设置分步教学，也未使用 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：有：获权后 gameaitvkv.a() 先发送 ACTION_MAIN/CATEGORY_HOME 回桌面，再拉起 zsgtf(start=blockDelete) 弹出不可取消的 'Sorry! / System Error 495' 假故障框打断撤权操作；同时 dokmzmwozhpobpu 检测 DevicePolicyManager.isAdminActive 状态，未激活则持续跳转应用详情页；gameaitvkv 还从 C2 读取 vkladmin、uninstall1/2 文案用于设备管理器与卸载页欺诈。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条最有效时机：① 监测到前台组件变为 com.android.settings 的 AccessibilitySettings（android.settings.ACCESSIBILITY_SETTINGS）且上一前台为本应用 Activity 时立即抓栈；② 监测到本应用导出服务 ecw 启动 / 屏幕中央出现短 Toast 时同步抓栈，此时系统无障碍列表与 Toast 可同帧捕获。冷启动 5 秒内亦应抓一次 launcher Activity 以防其自禁用后消失。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两类盲区：① 无障碍引导文案与启动器 WebView URL 由 C2 下发（SharedPreferences 键 StringAccessibility/straccessibility/urls），若服务端未下发或未连通，运行期只能看到默认值 'Enable access for' 或空 WebView，诱导可能完全不出现；② 导出服务 ecw 的触发源在包内无静态调用点，若远端未下发指令则 Toast 引导不出现，纯 UTG 可能只捕获到“静默跳转 + 系统列表”这一最小形态。静态加壳不存在，不构成 UTG 盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动入口页（自禁用前唯一可见帧）** | kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty，布局 2130968580；远端开关开启时为整屏 WebView | 确认应用是否存在一阶段外壳/远端 WebView 换脸，以及是否在首帧就完成组件自禁用（图标消失） | 前台 Activity 全名与 launcher 组件一致性；是否存在 WebView 节点及是否含 URL 输入框/加载态；界面停留时长（毫秒级即 finish 为强可疑） |
| **跳转前“无障碍引导”Activity 页** | kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.vchruwbih（layout 2130968590） | 验证本应用是否存在任何引导文案；若无任何文本且 onCreate 内直接跳系统设置，即为静默诱导的直接证据 | 页面文本节点是否为空；页面存活时间与随后前台是否为 AccessibilitySettings；是否出现权限/服务名关键词 |
| **系统无障碍服务列表项** | 系统 Settings 无障碍页，列表项文本 'Flash Player Service' | 确认服务名冒充与 description 缺失（列表项无副标题说明），是身份伪装的关键页面 | 列表项标题 'Flash Player Service'；是否存在用途描述副文本（预期为空）；开关初始状态 |
| **系统设置页之上的 Toast 引导层** | 居中 Toast：Enable access for 'Flash Player Service' | 直接捕获引导原文，判断是否为“受限设置分步教学”型引导及文案是否被远端改写 | Toast 文本与 Gravity 位置；Toast 出现次数/间隔（重复拉起即循环施压）；文案语言与设备 Locale 是否匹配 |
| **不可取消的恐吓弹窗页** | AlertDialog：Get permission / The system does not work correctly... / Enable now；或 Sorry! / System Error 495 | 区分“假故障恐吓”与“良性说明”，并确认按钮唯一（无取消）导致用户只能顺从 | 对话框按钮数量与文案（单按钮为强信号）；是否可点外部取消；标题/正文是否含 System Error 等伪系统术语 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.vchruwbih#onCreate`
- `kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty#onCreate`
- `kovvkynlzyyy.dfpn.iablbixbxg.dokmzmwozhpobpu#onHandleIntent`
- `kovvkynlzyyy.dfpn.iablbixbxg.a#c(Context, String)`
- `kovvkynlzyyy.dfpn.iablbixbxg.ecw#onStartCommand`
- `kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf#onCreate`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（已用 16 次工具调用完成收口）

**无障碍权限引导以“云端可配置文案 + 静默跳转 + 居中 Toast 悬浮提示”为主，没有本地 HTML 教学页，也没有伪造系统开关页。**

1. **冷启动入口自行禁用并消失**：LAUNCHER Activity `lubvupaubifhedty.onCreate` 先调用 `setContentView`，然后判断 `b.n`；如果 `b.n` 为 false，就 `startService(dokmzmwozhpobpu)`，否则用 `WebView` 加载远端 URL（`b.o`，启用 JS）；随后立刻调用 `setComponentEnabledSetting(自身, DISABLED)` 隐藏图标，注册 `startAlarm` 定时器，并调用 `finish()`。
2. **后台定时巡检**：`dokmzmwozhpobpu.onHandleIntent` 获取 WakeLock 后进入 `TimeUnit.sleep` 循环，用 `a.g(Context)` 判断无障碍是否已开启（通过 `getEnabledAccessibilityServiceList` 比对 `包名/gameaitvkv`）；未授权且设备管理器未激活时，拉起 `zsgtf`，并携带 `start=deleteApp`，进而跳转 `ACTION_APPLICATION_DETAILS_SETTINGS`。
3. **纯跳转型“引导页”**：`vchruwbih.onCreate` 先调用 `setContentView(2130968590)`，**紧接着**无条件调用 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，没有说明文案，也没有取消按钮，用户看不到任何解释。
4. **系统列表页上的悬浮提示**：导出的 `ecw.onStartCommand` 弹出 `setGravity(16,0,0)` 的居中 Toast：`StringAccessibility + " '" + "Flash Player Service" + "'"`，默认文案为 `Enable access for 'Flash Player Service'`；该文案由服务端配置（`a.d(context,"StringAccessibility")`，默认 `"Enable access for"`）。
5. **恐吓式弹窗只用于“用量统计”权限**：`a.c(Context,"statistic")` 构造 `setCancelable(false)` 的 AlertDialog，只有一个 NegativeButton，文案是“系统不能正常工作，需要开启统计访问权限 'Flash Player'”/“立即开启”，点击后跳 `USAGE_ACCESS_SETTINGS`；`zsgtf` 的 `blockDelete` 分支则弹出不可取消的 `Sorry! / System Error 495` 假故障框。
6. **获权后立即转为键盘记录与反卸载**：`gameaitvkv.onServiceConnected` 设置 `flags=1, eventTypes=-1`（监听全部事件），`onAccessibilityEvent` 将 `getText()` 内容写入 `keys.log`，并 POST 到 `/private/datakeylogger.php`；`gameaitvkv.a()` 先发送 `HOME`，再弹出 `blockDelete` 假错误框，以阻止用户进入卸载页。

**覆盖边界**：无障碍引导文案（`StringAccessibility`/`straccessibility`/`StringActivate`）以及启动器 WebView 的 `urls`（默认 `https://comicwalker.at`）都由远端下发，本地只能看到默认值；`ecw` 在包内未发现静态调用点（导出服务，推测由远端指令或导出组件触发）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "DEX 完整可读、未加壳；跳转点、弹窗构建、Toast 逻辑均静态可见。但无障碍引导文案（StringAccessibility 默认 'Enable access for'、straccessibility、StringActivate、StringYes、uninstall1/2、vkladmin）与启动器 WebView 的 URL（SharedPreferences 键 urls，默认 https://comicwalker.at）均由 C2 下发覆盖；ecw 引导 Toast 服务在包内无静态调用点，触发链（远端指令/导出组件）不可静态还原。",
  "summary_one_liner": "以 'Flash Player' 为名、图标自禁用后由后台 Alarm 循环驱动，用无说明文案的 Activity 直接静默跳转 ACCESSIBILITY_SETTINGS，再叠加云端可配置的居中 Toast 'Enable access for Flash Player Service' 引导开启，获权后立即监听全部无障碍事件做键盘记录并弹假系统错误阻止卸载。",
  "disguise_identity": {
    "app_display_name": "Flash Player",
    "claimed_brand_or_persona": "Flash Player（冒充 Adobe Flash Player 播放器）",
    "a11y_service_label": "Flash Player Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "全部类名/包名随机化（kovvkynlzyyy.dfpn.iablbixbxg、gameaitvkv、qycizhfz.vchruwbih 等）；launcher Activity 首次运行后 setComponentEnabledSetting(DISABLED) 自禁用，图标从桌面消失以躲避用户排查；多个 Activity 声明 android:label=\"\" 空标签、excludeFromRecents=true、launchMode=2（singleTask）避免出现在最近任务；无障碍 service 的 android:description 缺失（预筛为空），系统列表仅显示 'Flash Player Service' 名称而不给用途说明。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty（LAUNCHER Activity）",
      "trigger_event": "用户点击桌面图标 onCreate()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（setContentView(2130968580) 后立即 finish 或加载远端 WebView）",
      "shown_text_zh": "无可读引导界面；若远端开关 b.n 为 true 则整屏替换为 WebView 加载服务端 URL",
      "user_action_requested": "无提示，用户仅看到一闪而过的界面；无取消/跳过按钮",
      "code_anchor": "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "同 launcher Activity 自禁用 + Alarm 注册 + IntentService kovvkynlzyyy.dfpn.iablbixbxg.dokmzmwozhpobpu",
      "trigger_event": "onCreate 末尾 setComponentEnabledSetting(自身, 2, 1)、a.a(this,\"startAlarm\",Interval) 默认 10000ms、finish()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "桌面图标消失，后续由定时 Alarm 拉起后台服务继续巡检与跳转",
      "user_action_requested": "无",
      "code_anchor": "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty.onCreate"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "dokmzmwozhpobpu.onHandleIntent 轮询 + a.g(Context) 检测无障碍是否开启",
      "trigger_event": "Alarm 每 Interval（默认 10s）唤醒，TimeUnit.MILLISECONDS.sleep 后判断 getEnabledAccessibilityServiceList 中是否存在 '包名/gameaitvkv'",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "未授权则反复进入下一步跳转，形成持续循环",
      "user_action_requested": "无显式请求；用户返回后仍会被再次拉起",
      "code_anchor": "kovvkynlzyyy.dfpn.iablbixbxg.dokmzmwozhpobpu.onHandleIntent / kovvkynlzyyy.dfpn.iablbixbxg.a#g"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "qycizhfz.zsgtf（start=deleteApp）→ 系统「应用详情」页",
      "trigger_event": "dokmzmwozhpobpu 在 urls 为空且设备管理器未激活时 startActivity(zsgtf, \"start\"=\"deleteApp\")，zsgtf.onCreate 再 startActivity(APPLICATION_DETAILS_SETTINGS, package:自身)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接跳到本应用的系统「应用信息」页面，无任何说明",
      "user_action_requested": "无文案要求；实际效果是把用户带到可点「强行停止/卸载」的位置以便反制或劫持返回",
      "code_anchor": "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf.onCreate"
    },
    {
      "step": 5,
      "stage": "引导说明页",
      "screen_or_component": "a.c(Context,\"statistic\") 不可取消 AlertDialog",
      "trigger_event": "zsgtf 收到 start=statistic（或后台下发）调用 aVar.c(this,\"statistic\")，按系统 Locale 选择语言分支后 dialog.show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Get permission / The system does not work correctly, you need to enable access to the statistics '<应用名>' / Enable now",
      "shown_text_zh": "获取权限 / 系统运行不正常，您需要开启对统计信息的访问权限 '<应用名>' / 立即开启",
      "user_action_requested": "仅一个 NegativeButton「Enable now」，setCancelable(false)，无取消/跳过；点击后 a$1.onClick 跳 android.settings.USAGE_ACCESS_SETTINGS",
      "code_anchor": "kovvkynlzyyy.dfpn.iablbixbxg.a#c(Context, String) + kovvkynlzyyy.dfpn.iablbixbxg.a$1#onClick"
    },
    {
      "step": 6,
      "stage": "跳无障碍设置",
      "screen_or_component": "qycizhfz.vchruwbih → 系统「无障碍」设置页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "该 Activity onCreate() 中 setContentView 之后无条件 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))；异常时 finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（本应用不提供任何说明文字，直接跳系统页）",
      "shown_text_zh": "静默跳转到系统无障碍服务列表，用户只能看到系统列表里名为 'Flash Player Service' 的条目",
      "user_action_requested": "用户需自行在系统列表中点击 'Flash Player Service' 并打开开关；本页无取消/跳过按钮，也无引导说明",
      "code_anchor": "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.vchruwbih#onCreate"
    },
    {
      "step": 7,
      "stage": "遮罩叠层指引",
      "screen_or_component": "导出服务 kovvkynlzyyy.dfpn.iablbixbxg.ecw.onStartCommand 弹出的居中 Toast（覆盖在系统无障碍页上方）",
      "trigger_event": "ecw 被启动（exported=true，包内未发现静态调用点，推测由远端指令/其他导出组件拉起）后 onStartCommand",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Enable access for 'Flash Player Service'",
      "shown_text_zh": "为 'Flash Player Service' 开启访问权限",
      "user_action_requested": "提示用户在系统无障碍列表中找到并开启同名服务；无取消按钮（Toast 自动消失但由定时器重复拉起）",
      "code_anchor": "kovvkynlzyyy.dfpn.iablbixbxg.ecw#onStartCommand（文案来自 a.d(this,\"StringAccessibility\")，默认 \"Enable access for\"）"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "gameaitvkv.onServiceConnected / onAccessibilityEvent（键盘记录 + POST /private/datakeylogger.php）",
      "trigger_event": "用户在系统设置中开启服务 → onServiceConnected；之后任意窗口事件触发 onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无界面；数据侧字符串 'SEND KEL' / 'LOGER'",
      "shown_text_zh": "开启后立即全量监听无障碍事件，把各界面文本累积写入 keys.log，超过 10000 字符即加密上传到 /private/datakeylogger.php",
      "user_action_requested": "无",
      "code_anchor": "kovvkynlzyyy.dfpn.iablbixbxg.gameaitvkv#onServiceConnected / kovvkynlzyyy.dfpn.iablbixbxg.gameaitvkv#onAccessibilityEvent"
    },
    {
      "step": 9,
      "stage": "拒权反馈循环",
      "screen_or_component": "gameaitvkv.a() → HOME + qycizhfz.zsgtf(start=blockDelete) 不可取消 AlertDialog",
      "trigger_event": "无障碍服务在检测到卸载/设置页时调用 a()：先 startActivity(ACTION_MAIN/CATEGORY_HOME) 回桌面，再弹假错误框",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Sorry! / System Error 495 / ОК",
      "shown_text_zh": "抱歉！/ 系统错误 495 / 确定",
      "user_action_requested": "只能点「ОК」，setCancelable(false)，点后 finish()，用于打断用户撤权/卸载流程",
      "code_anchor": "kovvkynlzyyy.dfpn.iablbixbxg.gameaitvkv#a() + kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf#onCreate（blockDelete 分支）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务标签 'Flash Player Service'（AndroidManifest 中 service android:label，且 android:description 缺失，无用途说明）",
    "覆盖在系统无障碍设置页上方的居中 Toast（Gravity=16）: \"Enable access for 'Flash Player Service'\"，由导出服务 ecw.onStartCommand 弹出，文案可由 C2 通过 SharedPreferences 键 StringAccessibility 改写",
    "原生不可取消 AlertDialog（a.c(Context,\"statistic\")）: 标题 'Get permission'，正文 'The system does not work correctly, you need to enable access to the statistics '<应用名>''，唯一按钮 'Enable now'",
    "原生不可取消 AlertDialog（zsgtf blockDelete 分支）: 标题 'Sorry!'，正文 'System Error 495'，按钮 'ОК'",
    "qycizhfz.vchruwbih 承载 layout 2130968590 但无任何引导文案，onCreate 内立即跳转系统 ACCESSIBILITY_SETTINGS",
    "launcher Activity 在远端开关开启时整屏替换为 WebView，加载服务端下发 URL（默认 https://comicwalker.at），该页文案不在包内"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable access for 'Flash Player Service'",
      "text_zh": "为 'Flash Player Service' 开启访问权限",
      "source_location": "kovvkynlzyyy.dfpn.iablbixbxg.ecw#onStartCommand（拼接 a.d(ctx,\"StringAccessibility\") 默认值 \"Enable access for\" + 服务标签 \"Flash Player Service\"）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Get permission",
      "text_zh": "获取权限",
      "source_location": "kovvkynlzyyy.dfpn.iablbixbxg.a#c(Context,String) 硬编码（statistic 分支默认语言）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "The system does not work correctly, you need to enable access to the statistics '<应用名>'",
      "text_zh": "系统运行不正常，您需要开启对统计信息的访问权限 '<应用名>'",
      "source_location": "kovvkynlzyyy.dfpn.iablbixbxg.a#c(Context,String) 硬编码字符串拼接",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable now",
      "text_zh": "立即开启",
      "source_location": "kovvkynlzyyy.dfpn:iablbixbxg.a#c(Context,String) setNegativeButton 文案（其余语言分支为 'Включить сейчас'/'Şimdi etkinleştir'/'Aktivieren Sie jetzt'/'Attiva ora'/'Activer maintenant' 等）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Sorry!",
      "text_zh": "抱歉！",
      "source_location": "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf#onCreate（blockDelete 分支 AlertDialog.setTitle）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "System Error 495",
      "text_zh": "系统错误 495",
      "source_location": "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf#onCreate（blockDelete 分支 AlertDialog.setMessage）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable access for",
      "text_zh": "为……开启访问权限",
      "source_location": "kovvkynlzyyy.dfpn.iablbixbxg.a#b(Context) 中 d(context,\"StringAccessibility\",\"Enable access for\") 默认值；同处还初始化 \"StringActivate\"=\"activate\"、\"StringYes\"、\"uninstall1/2\"、\"vkladmin\" 等服务端可覆盖文案",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "activate",
      "text_zh": "激活",
      "source_location": "kovvkynlzyyy.dfpn.iablbixbxg.a#b(Context) d(context,\"StringActivate\",\"activate\")；c.h 数组为 100+ 语言 'activate' 本地化表",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "后台 dokmzmwozhpobpu 由 startAlarm（默认 10s，可由服务端 Interval 调整）周期唤醒，循环内 a.g(Context) 用 getEnabledAccessibilityServiceList 判定未授权，即再次 startActivity 拉起 zsgtf→APPLICATION_DETAILS_SETTINGS 或无障碍跳转 Activity；用户按返回键不会终止该循环，只有服务被杀或授权成功才停止。",
    "overlay_or_fake_settings": "无高仿系统无障碍开关页；但在系统无障碍列表页之上叠放居中对齐（Gravity=16）的 Toast 提示 'Enable access for \\'Flash Player Service\\''，由导出服务 ecw 弹出，用于在系统页面之上补上本应用缺失的说明文字。",
    "restricted_settings_13plus_coaching": "无；targetSdkVersion=27，未涉及 Android 13 受限设置分步教学，也未使用 Session 安装器绕过。",
    "post_grant_anti_removal": "有：获权后 gameaitvkv.a() 先发送 ACTION_MAIN/CATEGORY_HOME 回桌面，再拉起 zsgtf(start=blockDelete) 弹出不可取消的 'Sorry! / System Error 495' 假故障框打断撤权操作；同时 dokmzmwozhpobpu 检测 DevicePolicyManager.isAdminActive 状态，未激活则持续跳转应用详情页；gameaitvkv 还从 C2 读取 vkladmin、uninstall1/2 文案用于设备管理器与卸载页欺诈。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条最有效时机：① 监测到前台组件变为 com.android.settings 的 AccessibilitySettings（android.settings.ACCESSIBILITY_SETTINGS）且上一前台为本应用 Activity 时立即抓栈；② 监测到本应用导出服务 ecw 启动 / 屏幕中央出现短 Toast 时同步抓栈，此时系统无障碍列表与 Toast 可同帧捕获。冷启动 5 秒内亦应抓一次 launcher Activity 以防其自禁用后消失。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动入口页（自禁用前唯一可见帧）",
        "page_identifier": "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty，布局 2130968580；远端开关开启时为整屏 WebView",
        "why_most_useful": "确认应用是否存在一阶段外壳/远端 WebView 换脸，以及是否在首帧就完成组件自禁用（图标消失）",
        "observable_utg_signals": ["前台 Activity 全名与 launcher 组件一致性", "是否存在 WebView 节点及是否含 URL 输入框/加载态", "界面停留时长（毫秒级即 finish 为强可疑）"]
      },
      {
        "page_role": "跳转前“无障碍引导”Activity 页",
        "page_identifier": "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.vchruwbih（layout 2130968590）",
        "why_most_useful": "验证本应用是否存在任何引导文案；若无任何文本且 onCreate 内直接跳系统设置，即为静默诱导的直接证据",
        "observable_utg_signals": ["页面文本节点是否为空", "页面存活时间与随后前台是否为 AccessibilitySettings", "是否出现权限/服务名关键词"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页，列表项文本 'Flash Player Service'",
        "why_most_useful": "确认服务名冒充与 description 缺失（列表项无副标题说明），是身份伪装的关键页面",
        "observable_utg_signals": ["列表项标题 'Flash Player Service'", "是否存在用途描述副文本（预期为空）", "开关初始状态"]
      },
      {
        "page_role": "系统设置页之上的 Toast 引导层",
        "page_identifier": "居中 Toast：Enable access for 'Flash Player Service'",
        "why_most_useful": "直接捕获引导原文，判断是否为“受限设置分步教学”型引导及文案是否被远端改写",
        "observable_utg_signals": ["Toast 文本与 Gravity 位置", "Toast 出现次数/间隔（重复拉起即循环施压）", "文案语言与设备 Locale 是否匹配"]
      },
      {
        "page_role": "不可取消的恐吓弹窗页",
        "page_identifier": "AlertDialog：Get permission / The system does not work correctly... / Enable now；或 Sorry! / System Error 495",
        "why_most_useful": "区分“假故障恐吓”与“良性说明”，并确认按钮唯一（无取消）导致用户只能顺从",
        "observable_utg_signals": ["对话框按钮数量与文案（单按钮为强信号）", "是否可点外部取消", "标题/正文是否含 System Error 等伪系统术语"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两类盲区：① 无障碍引导文案与启动器 WebView URL 由 C2 下发（SharedPreferences 键 StringAccessibility/straccessibility/urls），若服务端未下发或未连通，运行期只能看到默认值 'Enable access for' 或空 WebView，诱导可能完全不出现；② 导出服务 ecw 的触发源在包内无静态调用点，若远端未下发指令则 Toast 引导不出现，纯 UTG 可能只捕获到“静默跳转 + 系统列表”这一最小形态。静态加壳不存在，不构成 UTG 盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.vchruwbih#onCreate",
    "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.lubvupaubifhedty#onCreate",
    "kovvkynlzyyy.dfpn.iablbixbxg.dokmzmwozhpobpu#onHandleIntent",
    "kovvkynlzyyy.dfpn.iablbixbxg.a#c(Context, String)",
    "kovvkynlzyyy.dfpn.iablbixbxg.ecw#onStartCommand",
    "kovvkynlzyyy.dfpn.iablbixbxg.qycizhfz.zsgtf#onCreate"
  ]
}
```

</details>
