# MR_126__dac40ca71d｜Lucy — Video Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：107.5s

## 1. 一句话核心结论

- **核心申请方式**：以'视频播放器需要开启 Android Video Optimization 才能继续观看'为借口，用不可取消的原生 AlertDialog 一键跳转系统无障碍设置页并在返回后循环重弹，同时在系统无障碍列表用约 57 个换行把服务标签撑出屏幕、以开源播放器长文掩盖读取屏幕与派发手势能力，获权后立即加左缘悬浮遮罩并自动点击系统授权弹窗。
- **静态可见性说明**：引导链路（弹窗文案、按钮、跳转 Intent、回环、无障碍服务回调与手势自动点击）全部为明文 DEX + res/values/strings.xml 静态可见，无加壳、无 AES 载荷、无 HTML/WebView 资源。仅两处未在本次预算内展开：桌面入口 pdrdtectpd 自身的私有方法 a()，以及 JobScheduler 调起的 xsklpilmpn(Word service) 后续业务；二者不影响无障碍引导流程的判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `dac40ca71dab0a40ed4d7de64b463f7b91ecd473a279451788369087edfff8d0` |
| 包名 / 年份 | `dtlrquunob.ntrbhppvnr.dbawnbxoxz` / 2020 |
| 家族 / 品类 | **Lucy**（同池样本数：81） |
| 原始来源标识 | https://research.checkpoint.com/2020/lucys-back-ransomware-goes-mobile/ |
| 桌面显示名 | Video Player |
| 引导页宣称品牌/身份 | Android Video Optimization（伪装成系统级视频流优化/开源视频播放器优化组件） |
| 系统无障碍列表服务名 | Android Video Optimization \n\n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n. |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 服务标签 fake_label 在'Android Video Optimization'后填充约 57 个换行再加一个句点，把系统无障碍列表中'该服务可读取屏幕全部内容'的警示行推出可视区域；2) android:description 使用大段开源视频播放器优越性论述（采购门槛、私有源码、许可费用、安全补丁），只字不提 canRetrieveWindowContent/dispatchGesture/悬浮窗；3) 应用名'Video Player'与入口 Activity 标签'ReqPerm'、服务标签'Android Video Optimization'三套身份并存；4) 同一 DEX 内并存 FBI 勒索文案与支付卡采集界面，与播放器身份完全无关；5) 服务名与类名全量混淆（rikobysdrr/uhqpnqvpnt/cbrqbncpnu）。 |
| 无障碍服务类名 | `dtlrquunob.ntrbhppvnr.dbawnbxoxz.rikobysdrr` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Android Optimization must be enable, for play video in your phone.<br> Video player offer some advantages over players developed with proprietary software. Many businesses and individual users prefer to go the open source route as it does away with the procurement barrier. <br> Video players built with proprietary software use private source code and is offered via licensing where users need to pay for and agree to the different terms and conditions before being able to use the player. <br> Given the vastly improved scrutiny around security, the availability of patches and bug fixes, open source video players are free to use without licensing fees and cumbersome, contracts. Some additional benefits include |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | dtlrquunob.ntrbhppvnr.dbawnbxoxz.pdrdtectpd（MAIN/LAUNCHER，theme=@android:style/Theme.Translucent.NoTitleBar） | onCreate → setContentView(2131165199) → 自身 a() → SDK>=23 时调用 d.a(getApplicationContext()) 提交 JobScheduler 任务（最小延迟 5s、requiresDeviceIdle=true、网络类型 2） | 原生Activity | 无 | 点击桌面图标启动（无其他交互） | `dtlrquunob.ntrbhppvnr.dbawnbxoxz.pdrdtectpd.onCreate / dtlrquunob.ntrbhppvnr.dbawnbxoxz.d.a(Context)` |
| 2 | 引导说明页 | dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt（权限引导 Activity，setContentView(2131165199)） | onCreate → 置 rikobysdrr.a=true → registerReceiver(CLOSE_SYSTEM_DIALOGS) → a()：若 rikobysdrr.b（已启用无障碍）为 false 则构建并 show() 弹窗；另由 rikobysdrr.a() 在服务上下文以 FLAG_ACTIVITY_NEW_TASK 拉起 | 原生Dialog | **原文**：Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. [确定]<br>**译注**：标题：注意。正文：为了继续观看视频文件，需要开启 Android Video Optimization（视频流优化），请把它开启。按钮：确定。 | 只能点击'确定'；setCancelable(false)、无取消/跳过按钮，SDK<23 时 window 类型置 2010 使弹窗覆盖其他界面 | `dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt.a() / res/values/strings.xml#Activate_Access / #Attention` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装服务列表（android.settings.ACCESSIBILITY_SETTINGS） | 弹窗唯一按钮 onClick → startActivityForResult(new Intent(ACTION_ACCESSIBILITY_SETTINGS).addFlags(8388608 /*FLAG_ACTIVITY_NEW_TASK*/), 0) | 系统无障碍页 | **原文**：Android Video Optimization \n\n\n…\n. （服务项，标签被换行撑高）<br>**译注**：系统无障碍列表中显示一个名为 'Android Video Optimization' 的服务项，其后的空白换行使系统安全警示文本落在屏幕外 | 用户需在系统列表中点击该服务并确认'开启/允许' | `dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt$1.onClick / res/xml/dqdootkrqb.xml / res/values/strings.xml#fake_label` |
| 4 | 拒权反馈循环 | uhqpnqvpnt.onActivityResult → 再次 show() 同一不可取消 AlertDialog | 从系统设置返回触发 onActivityResult → 无条件调用 a() → 若仍未启用则重建弹窗并 show() | 原生Dialog | **原文**：Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее.<br>**译注**：返回后未授权则再次弹出同一'必须开启优化才能看视频'弹窗，无降级路径 | 再次被要求点击'确定'重新跳转；按 Home/最近任务时由 CLOSE_SYSTEM_DIALOGS 接收器 dismiss 弹窗并 finish（临时隐匿，下次启动再来） | `dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt.onActivityResult / uhqpnqvpnt$a.onReceive` |
| 5 | 跳受限设置 | 系统设置 → 显示在其他应用上层（android.settings.action.MANAGE_OVERLAY_PERMISSION?package=<pkg>），承载 Activity 为 cbrqbncpnu | cbrqbncpnu.onCreate → a() → startActivityForResult(intent, 0)；onActivityResult 后再次 a() 形成回环 | 系统无障碍页 | **原文**：无（直接跳转系统悬浮窗授权页，无自有文案）<br>**译注**：无自有文案，直接把用户送到本应用的'显示在其他应用上层'开关页 | 打开悬浮窗开关后返回；未开启则返回即再次跳转（回环） | `dtlrquunob.ntrbhppvnr.dbawnbxoxz.cbrqbncpnu.a() / cbrqbncpnu.onActivityResult` |
| 6 | 遮罩叠层指引 | rikobysdrr.onCreate 添加 WindowManager 视图（30px 宽、全高、type=2002 SYSTEM_ALERT_WINDOW、gravity=51 左缘、flags=262184） | 无障碍服务 onCreate 即执行 windowManager.addView(linearLayout, LayoutParams)，并 setOnTouchListener(this) | 悬浮窗Overlay | 无 | 无显式请求；用户左缘滑动被拦截 | `dtlrquunob.ntrbhppvnr.dbawnbxoxz.rikobysdrr.onCreate` |
| 7 | 获权后动作 | rikobysdrr.onServiceConnected + onAccessibilityEvent（自动手势/节点点击）+ AlarmManager 60s 重复拉起 bntcoupsvn | 无障碍服务连接成功 → 以 exit=true 拉起 uhqpnqvpnt 令引导页关闭、设置 flags=19/eventTypes=-1 全事件监听；随后每次无障碍事件：findAccessibilityNodeInfosByText("Allow display over other apps"/"Permit drawing over other apps"/"DONE"/"CLEAR ALL") 用 dispatchGesture 模拟点击，findAccessibilityNodeInfosByText("OK") 直接 performAction(16) | 悬浮窗Overlay | **原文**：Allow display over other apps / Permit drawing over other apps / If you don’t want / DONE / CLEAR ALL / OK<br>**译注**：由服务自动点击系统'允许显示在其他应用上层''不允许''完成''全部清除''确定'等按钮，替用户完成授权与弹窗清理 | 无需用户操作——授权动作被自动化；同时监听 com.android.vending 事件并检查 SharedPreferences("Data").Card 标记 | `dtlrquunob.ntrbhppvnr.dbawnbxoxz.rikobysdrr.onServiceConnected / rikobysdrr.onAccessibilityEvent / rikobysdrr.a(AccessibilityEvent, String, int)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- uhqpnqvpnt.a(Context, String, Intent)：原生 AlertDialog（theme 5，SDK<23 时 window type=2010 系统级弹窗），setCancelable(false)，仅 positiveButton，标题取 res/values/strings.xml#Attention（'Внимание'），正文取 #Activate_Access（俄语'继续看视频必须开启 Android Video Optimization'）
- 系统无障碍设置列表项：res/values/strings.xml#fake_label 作为 service android:label（'Android Video Optimization' + 约 57 个换行 + '.'），把系统安全警示挤到屏幕外
- 系统无障碍详情说明：res/values/strings.xml#accessibility_service_description，由 res/xml/dqdootkrqb.xml 的 android:description 引用，内容为开源视频播放器优点长文
- cbrqbncpnu：无自有文案，直接跳 android.settings.action.MANAGE_OVERLAY_PERMISSION 系统页
- 悬浮层：rikobysdrr.onCreate 添加的 30px 左缘全高透明窗口（TYPE_SYSTEM_ALERT_WINDOW），无文字，仅拦截触控
- 同包勒索界面文案（与本播放器身份无关）：res/values/strings.xml#Text（伪造 FBI 通知全文）、#titleWhere（'To pay fine, you need purchase a OneVanilla Card $500 …'）、#textSend、#string_pay、#Caption

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. | 为了继续观看视频文件，需要开启 Android Video Optimization（视频流优化），请把它开启。 | `res/values/strings.xml key=Activate_Access，由 uhqpnqvpnt.a() 作为 AlertDialog message 展示` | 假更新 |
| ru | Внимание | 注意 | `res/values/strings.xml key=Attention（AlertDialog 标题）` | 故障恐吓 |
| en | Android Optimization must be enable, for play video in your phone. Video player offer some advantages over players developed with proprietary software. Many businesses and individual users prefer to go the open source route as it does away with the procurement barrier. Video players built with proprietary software use private source code and is offered via licensing where users need to pay for and agree to the different terms and conditions before being able to use the player. Given the vastly improved scrutiny around security, the availability of patches and bug fixes, open source video players are free to use without licensing fees and cumbersome, contracts. Some additional benefits include | 必须开启 Android 优化才能在你手机上播放视频。视频播放器相比专有软件开发的产品有一些优势：许多企业和个人用户偏好开源路线，因为它免除了采购门槛；专有软件的视频播放器使用私有源码并通过许可提供，用户需付费并同意各种条款才能使用；鉴于安全审查、补丁与缺陷修复的可用性大幅改善，开源视频播放器可免费使用，无需许可费与繁琐合同。其他好处还包括…… | `res/values/strings.xml key=accessibility_service_description，经 res/xml/dqdootkrqb.xml android:description 呈现于系统无障碍详情` | 隐私承诺 |
| en | Android Video Optimization <br><br><br><br><br><br><br><br><br> <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>. | Android Video Optimization（后接约 57 个空行，再一个句点） | `res/values/strings.xml key=fake_label，作为无障碍 service android:label` | 教唆忽视警告 |
| en | DEPARTMENT OF JUSTICE FEDERAL BUREAU OF INVESTIGATION FBI HEADQUARTERS WASHINGTON DC DEPARTMENT, USA — AS A RESULT OF FULL SCANNING OF YOUR DEVICE, SOME SUSPICIOUS FILES HAVE BEEN FOUND AND YOUR ATTENDANCE OF THE FORBIDDEN PORNOGRAPHIC SITES HAS BEEN FIXED. FOR THIS REASON YOUR DEVICE HAS BEEN LOCKED AND DATA ENCRYPTED. … THE SIZE OF THE PENALTY IS $500.00 … DISCONNECTION OR DISPOSAL OF THE DEVICE OR YOUR ATTEMPTS TO UNLOCK THE DEVICE INDEPENDENTLY WILL BE APPREHENDED AS UNAPPROVED ACTIONS INTERFERING THE EXECUTION OF THE LAW OF THE UNITED STATES OF AMERICA | 美国司法部/联邦调查局总部——经全面扫描你的设备，发现可疑文件，并已记录你访问被禁色情网站的行为，因此你的设备已被锁定、数据已被加密……罚金金额为 500.00 美元……断开或丢弃设备、或尝试自行解锁，将被视为干扰美国法律执行的未授权行为。 | `res/values/strings.xml key=Text（伪造执法勒索页面 HTML 片段）` | 假反诈安全 |
| en | To pay fine, you need purchase a OneVanilla Card $500 at any of these retail locations | 要缴纳罚金，你需要在以下任一零售点购买一张 500 美元的 OneVanilla 卡。 | `res/values/strings.xml key=titleWhere（支付卡引导页）` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：uhqpnqvpnt.onActivityResult 无条件再次调用 a()，只要 AccessibilityManager 中仍未出现本包服务就立刻重建并 show() 同一 setCancelable(false) 弹窗，形成'返回设置页→再弹→再跳'的死循环；同时 rikobysdrr.a() 在服务上下文以 FLAG_ACTIVITY_NEW_TASK 主动拉起该引导 Activity，实现从后台再次弹窗。用户按 Home/最近任务时 CLOSE_SYSTEM_DIALOGS 接收器会 dismiss 并 finish 以暂时隐藏，下次进入继续。
- **遮罩叠层 / 高仿系统设置页**：未伪造系统设置页；但在获权后由 rikobysdrr.onCreate 立刻以 WindowManager 添加 30px 宽、全高、type=2002（SYSTEM_ALERT_WINDOW）、gravity=51（左缘）的透明触控条并绑定 onTouchListener，用于拦截左缘手势/返回滑动；配合 cbrqbncpnu 反复跳转 MANAGE_OVERLAY_PERMISSION 骗取悬浮窗权限。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（compileSdk/target 为 28，未实现 Android 13 受限设置的'应用详情右上角菜单→允许受限设置'分步教学，也未使用 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：获权后不自点确认开关（系统会自行开启），但会：1) onServiceConnected 以 exit=true 拉起引导页使其关闭、并设置 eventTypes=-1 监听全部事件；2) onAccessibilityEvent 用 findAccessibilityNodeInfosByText + dispatchGesture 自动点击 'Allow display over other apps'/'Permit drawing over other apps'/'DONE'/'CLEAR ALL'，并对所有 'OK' 节点 performAction(16)，自动完成悬浮窗授权与弹窗清理；3) 左缘悬浮触控条拦截边缘手势；4) AlarmManager 每 60 秒重复触发 bntcoupsvn 保活。未观察到监听设置页后按 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接实现。
- **良性降级 / 替代方案**：无。未授权时仅 finish 或重复弹窗，没有手动模式、仅观看模式或任何降级路径，'Video Player' 本身也不提供真实播放功能。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条最佳时机：① 监测到 startActivity(Intent action=android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（由 uhqpnqvpnt$1.onClick 触发，此时前一张不可取消弹窗仍在栈内，可同时截取弹窗与系统列表）；② 从系统无障碍页返回触发 uhqpnqvpnt.onActivityResult 后立即再弹窗的瞬间（验证拒权回环）。悬浮窗权限链路则在监测到 action=android.settings.action.MANAGE_OVERLAY_PERMISSION 且 data=package:<pkg> 时拉起。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本样本无纯图空文本诱导，文字均为原生字符串，UTG 文本可直接提取。潜在盲区：① 桌面入口 pdrdtectpd 为半透明无界面 Activity，冷启动瞬间可能只捕获到空白/透明窗口，需以 JobScheduler(xsklpilmpn) 与 uhqpnqvpnt 的弹出为锚点而非首屏；② 左缘悬浮条本身无文字，纯 UTG 文本检测不可见，需结合窗口层级/尺寸信号；③ 部分行为在设备 idle + 非计费网络条件下由 JobScheduler 触发（5s 最小延迟、requiresDeviceIdle=true），模拟器/在线设备不满足条件时可能不触发；④ 静态未加壳，运行期 UTG 不受壳影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（不可取消）** | 包 dtlrquunob.ntrbhppvnr.dbawnbxoxz 的 uhqpnqvpnt 之上覆盖的原生 AlertDialog：标题'Внимание'、正文俄语'…нужно включить Android Video Optimization…'、唯一按钮'确定' | 这是诱导的唯一说理环节，弹窗无取消按钮且文案与'Video Player'真实功能不符，是判定诱导+无跳过路径的最直接证据 | dialog 节点仅含 1 个可点击按钮（确定），无'取消/稍后/跳过'节点；标题文本包含 Attention/Внимание，正文包含 Android Video Optimization；弹窗下方 Activity 为 uhqpnqvpnt，包名 dtlrquunob.ntrbhppvnr.dbawnbxoxz |
| **系统无障碍服务列表项（标签空白挤出）** | android.settings.ACCESSIBILITY_SETTINGS 列表中 label='Android Video Optimization' 且该项高度异常大、其后为大段空白 | 可直接用 UTG 证明'空白/换行挤出系统安全警示'的伪装手法，是身份欺骗的关键物证 | 服务项文本节点以 'Android Video Optimization' 开头、以单个 '.' 结尾，中间为大量换行空白；该项 bounds 高度显著大于相邻服务项，系统'可读取屏幕内容'警示文本不在可视 bounds 内；同一页面其余应用服务项高度正常，形成对照 |
| **设置页返回后重弹的拒权回环页** | 从 ACCESSIBILITY_SETTINGS 返回后 0–800ms 内，uhqpnqvpnt 再次显示同一不可取消 AlertDialog（同一标题/正文） | 区分'一次性提示'与'拒绝即循环强制'，直接支撑 COERCE_REFUSAL_LOOP_RELAUNCH | 连续两次截图出现内容完全相同的弹窗（无取消按钮）；返回键/Home 后短时间内弹窗再次出现或引导页被 FLAG_ACTIVITY_NEW_TASK 重新压栈；logcat 中反复出现 CLOSE_SYSTEM_DIALOGS 注册与 ACCESSIBILITY_SETTINGS 启动 |
| **获权后左缘悬浮遮罩条** | TYPE_SYSTEM_ALERT_WINDOW 全高 30px 宽、贴左缘（gravity=51）的透明 Window；同时在无障碍设置页出现自动点击'Allow display over other apps'的行为 | 证明授权后行为已越过'视频优化'声称范围，进入屏幕操控与边缘手势拦截 | 窗口层级 dump 中存在 30x屏幕高、位于左边缘、包名归属本应用的 overlay 窗口；无用户输入情况下悬浮窗授权页的'允许'按钮被点击（dispatchGesture 触发）；无障碍服务事件流中出现 eventTypes=-1 全事件监听与对 OK 节点的 ACTION_CLICK |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt.a(Context, String, Intent)`
- `dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt$1.onClick`
- `dtlrquunob.ntrbhppvnr.dbawnbxoxz.rikobysdrr.a()`
- `dtlrquunob.ntrbhppvnr.dbawnbxoxz.rikobysdrr.onAccessibilityEvent`
- `dtlrquunob.ntrbhppvnr.dbawnbxoxz.cbrqbncpnu.a()`
- `res/values/strings.xml#fake_label`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **无障碍引导为纯原生链路，无 WebView/HTML**：入口为 `ReqPerm` 风格权限页 `uhqpnqvpnt`，`onCreate` 立即弹出 **`setCancelable(false)` 的 AlertDialog**，标题 `Внимание`（注意），正文用俄语谎称"要继续看视频必须开启 Android Video Optimization（视频流优化）"，只有"确定"一个按钮，无取消/跳过。
- **确认即跳系统无障碍页**：`uhqpnqvpnt$1.onClick` → `startActivityForResult(ACTION_ACCESSIBILITY_SETTINGS, FLAG_ACTIVITY_NEW_TASK)`；返回后 `onActivityResult` **无条件再次调用 `a()`**，未授权就重弹同一不可取消弹窗 → **拒权回环**。
- **自检式状态机**：`rikobysdrr.a(Context)` 通过 `AccessibilityManager.getEnabledAccessibilityServiceList(-1)` 判断自身服务是否已启用；已启用则 `finish()`，未启用则弹窗，`onServiceConnected` 时以 `exit=true` 拉起引导页令其关闭。
- **身份伪装**：无障碍服务标签 `fake_label` = `"Android Video Optimization "` + **约 57 个换行** + `"."`，把系统"此服务可读取屏幕全部内容"的警示挤出可视区；`android:description` 用一大段"开源视频播放器优于专有软件"的良性说辞，**完全不说明读取屏幕/派发手势/悬浮窗能力**。
- **获权后并非良性**：服务 `onCreate` 立刻加 30px 宽、全高、`TYPE_SYSTEM_ALERT_WINDOW` 的**左缘触控遮罩条**并注册 60s 重复 Alarm；`onAccessibilityEvent` 用 `dispatchGesture` **自动点击**"Allow display over other apps"/"Permit drawing over other apps"/"DONE"/"CLEAR ALL"，并 `performAction(16)` 点击所有 `OK` 节点（自授权悬浮窗、清理弹窗）；同时监听 `com.android.vending` 事件（支付/卡相关），与 strings 中 FBI 恐吓 + $500 OneVanilla 卡勒索文案构成同一载荷。
- **另一条受限设置路径**：`cbrqbncpnu.a()` 跳 `ACTION_MANAGE_OVERLAY_PERMISSION?package=` 并在 `onActivityResult` 回环重跳（悬浮窗权限分步教学），与 `SYSTEM_ALERT_WINDOW` 共现权限对应。
- **未观察到**：Android 13+ 受限设置逐条教学（targetSdk 28）、高仿系统设置页、多 `activity-alias`、伪造 `isAccessibilityTool`。
- 静态完全可见（未加壳、无加密资产、无 HTML）。`pdrdtectpd`（桌面入口）自身的 `a()` 与 `JobScheduler→xsklpilmpn` 后续载荷因调用预算未展开，已在 `visibility_note` 标注。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链路（弹窗文案、按钮、跳转 Intent、回环、无障碍服务回调与手势自动点击）全部为明文 DEX + res/values/strings.xml 静态可见，无加壳、无 AES 载荷、无 HTML/WebView 资源。仅两处未在本次预算内展开：桌面入口 pdrdtectpd 自身的私有方法 a()，以及 JobScheduler 调起的 xsklpilmpn(Word service) 后续业务；二者不影响无障碍引导流程的判定。",
  "summary_one_liner": "以'视频播放器需要开启 Android Video Optimization 才能继续观看'为借口，用不可取消的原生 AlertDialog 一键跳转系统无障碍设置页并在返回后循环重弹，同时在系统无障碍列表用约 57 个换行把服务标签撑出屏幕、以开源播放器长文掩盖读取屏幕与派发手势能力，获权后立即加左缘悬浮遮罩并自动点击系统授权弹窗。",
  "disguise_identity": {
    "app_display_name": "Video Player",
    "claimed_brand_or_persona": "Android Video Optimization（伪装成系统级视频流优化/开源视频播放器优化组件）",
    "a11y_service_label": "Android Video Optimization \\n\\n\\n\\n\\n\\n\\n\\n\\n \\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n.",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 服务标签 fake_label 在'Android Video Optimization'后填充约 57 个换行再加一个句点，把系统无障碍列表中'该服务可读取屏幕全部内容'的警示行推出可视区域；2) android:description 使用大段开源视频播放器优越性论述（采购门槛、私有源码、许可费用、安全补丁），只字不提 canRetrieveWindowContent/dispatchGesture/悬浮窗；3) 应用名'Video Player'与入口 Activity 标签'ReqPerm'、服务标签'Android Video Optimization'三套身份并存；4) 同一 DEX 内并存 FBI 勒索文案与支付卡采集界面，与播放器身份完全无关；5) 服务名与类名全量混淆（rikobysdrr/uhqpnqvpnt/cbrqbncpnu）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "dtlrquunob.ntrbhppvnr.dbawnbxoxz.pdrdtectpd（MAIN/LAUNCHER，theme=@android:style/Theme.Translucent.NoTitleBar）",
      "trigger_event": "onCreate → setContentView(2131165199) → 自身 a() → SDK>=23 时调用 d.a(getApplicationContext()) 提交 JobScheduler 任务（最小延迟 5s、requiresDeviceIdle=true、网络类型 2）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "桌面图标 'Video Player'，启动后为无标题半透明 Activity，不呈现明显业务界面",
      "user_action_requested": "点击桌面图标启动（无其他交互）",
      "code_anchor": "dtlrquunob.ntrbhppvnr.dbawnbxoxz.pdrdtectpd.onCreate / dtlrquunob.ntrbhppvnr.dbawnbxoxz.d.a(Context)"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt（权限引导 Activity，setContentView(2131165199)）",
      "trigger_event": "onCreate → 置 rikobysdrr.a=true → registerReceiver(CLOSE_SYSTEM_DIALOGS) → a()：若 rikobysdrr.b（已启用无障碍）为 false 则构建并 show() 弹窗；另由 rikobysdrr.a() 在服务上下文以 FLAG_ACTIVITY_NEW_TASK 拉起",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. [确定]",
      "shown_text_zh": "标题：注意。正文：为了继续观看视频文件，需要开启 Android Video Optimization（视频流优化），请把它开启。按钮：确定。",
      "user_action_requested": "只能点击'确定'；setCancelable(false)、无取消/跳过按钮，SDK<23 时 window 类型置 2010 使弹窗覆盖其他界面",
      "code_anchor": "dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt.a() / res/values/strings.xml#Activate_Access / #Attention"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装服务列表（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "弹窗唯一按钮 onClick → startActivityForResult(new Intent(ACTION_ACCESSIBILITY_SETTINGS).addFlags(8388608 /*FLAG_ACTIVITY_NEW_TASK*/), 0)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Android Video Optimization \\n\\n\\n…\\n. （服务项，标签被换行撑高）",
      "shown_text_zh": "系统无障碍列表中显示一个名为 'Android Video Optimization' 的服务项，其后的空白换行使系统安全警示文本落在屏幕外",
      "user_action_requested": "用户需在系统列表中点击该服务并确认'开启/允许'",
      "code_anchor": "dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt$1.onClick / res/xml/dqdootkrqb.xml / res/values/strings.xml#fake_label"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "uhqpnqvpnt.onActivityResult → 再次 show() 同一不可取消 AlertDialog",
      "trigger_event": "从系统设置返回触发 onActivityResult → 无条件调用 a() → 若仍未启用则重建弹窗并 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Внимание / Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее.",
      "shown_text_zh": "返回后未授权则再次弹出同一'必须开启优化才能看视频'弹窗，无降级路径",
      "user_action_requested": "再次被要求点击'确定'重新跳转；按 Home/最近任务时由 CLOSE_SYSTEM_DIALOGS 接收器 dismiss 弹窗并 finish（临时隐匿，下次启动再来）",
      "code_anchor": "dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt.onActivityResult / uhqpnqvpnt$a.onReceive"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置 → 显示在其他应用上层（android.settings.action.MANAGE_OVERLAY_PERMISSION?package=<pkg>），承载 Activity 为 cbrqbncpnu",
      "trigger_event": "cbrqbncpnu.onCreate → a() → startActivityForResult(intent, 0)；onActivityResult 后再次 a() 形成回环",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（直接跳转系统悬浮窗授权页，无自有文案）",
      "shown_text_zh": "无自有文案，直接把用户送到本应用的'显示在其他应用上层'开关页",
      "user_action_requested": "打开悬浮窗开关后返回；未开启则返回即再次跳转（回环）",
      "code_anchor": "dtlrquunob.ntrbhppvnr.dbawnbxoxz.cbrqbncpnu.a() / cbrqbncpnu.onActivityResult"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "rikobysdrr.onCreate 添加 WindowManager 视图（30px 宽、全高、type=2002 SYSTEM_ALERT_WINDOW、gravity=51 左缘、flags=262184）",
      "trigger_event": "无障碍服务 onCreate 即执行 windowManager.addView(linearLayout, LayoutParams)，并 setOnTouchListener(this)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "屏幕左缘覆盖一条 30px 宽的全高透明触控条，拦截边缘手势/返回滑动，不使用户看到引导文字",
      "user_action_requested": "无显式请求；用户左缘滑动被拦截",
      "code_anchor": "dtlrquunob.ntrbhppvnr.dbawnbxoxz.rikobysdrr.onCreate"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "rikobysdrr.onServiceConnected + onAccessibilityEvent（自动手势/节点点击）+ AlarmManager 60s 重复拉起 bntcoupsvn",
      "trigger_event": "无障碍服务连接成功 → 以 exit=true 拉起 uhqpnqvpnt 令引导页关闭、设置 flags=19/eventTypes=-1 全事件监听；随后每次无障碍事件：findAccessibilityNodeInfosByText(\"Allow display over other apps\"/\"Permit drawing over other apps\"/\"DONE\"/\"CLEAR ALL\") 用 dispatchGesture 模拟点击，findAccessibilityNodeInfosByText(\"OK\") 直接 performAction(16)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Allow display over other apps / Permit drawing over other apps / If you don’t want / DONE / CLEAR ALL / OK",
      "shown_text_zh": "由服务自动点击系统'允许显示在其他应用上层''不允许''完成''全部清除''确定'等按钮，替用户完成授权与弹窗清理",
      "user_action_requested": "无需用户操作——授权动作被自动化；同时监听 com.android.vending 事件并检查 SharedPreferences(\"Data\").Card 标记",
      "code_anchor": "dtlrquunob.ntrbhppvnr.dbawnbxoxz.rikobysdrr.onServiceConnected / rikobysdrr.onAccessibilityEvent / rikobysdrr.a(AccessibilityEvent, String, int)"
    }
  ],
  "text_presentation_locations": [
    "uhqpnqvpnt.a(Context, String, Intent)：原生 AlertDialog（theme 5，SDK<23 时 window type=2010 系统级弹窗），setCancelable(false)，仅 positiveButton，标题取 res/values/strings.xml#Attention（'Внимание'），正文取 #Activate_Access（俄语'继续看视频必须开启 Android Video Optimization'）",
    "系统无障碍设置列表项：res/values/strings.xml#fake_label 作为 service android:label（'Android Video Optimization' + 约 57 个换行 + '.'），把系统安全警示挤到屏幕外",
    "系统无障碍详情说明：res/values/strings.xml#accessibility_service_description，由 res/xml/dqdootkrqb.xml 的 android:description 引用，内容为开源视频播放器优点长文",
    "cbrqbncpnu：无自有文案，直接跳 android.settings.action.MANAGE_OVERLAY_PERMISSION 系统页",
    "悬浮层：rikobysdrr.onCreate 添加的 30px 左缘全高透明窗口（TYPE_SYSTEM_ALERT_WINDOW），无文字，仅拦截触控",
    "同包勒索界面文案（与本播放器身份无关）：res/values/strings.xml#Text（伪造 FBI 通知全文）、#titleWhere（'To pay fine, you need purchase a OneVanilla Card $500 …'）、#textSend、#string_pay、#Caption"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее.",
      "text_zh": "为了继续观看视频文件，需要开启 Android Video Optimization（视频流优化），请把它开启。",
      "source_location": "res/values/strings.xml key=Activate_Access，由 uhqpnqvpnt.a() 作为 AlertDialog message 展示",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": "Внимание",
      "text_zh": "注意",
      "source_location": "res/values/strings.xml key=Attention（AlertDialog 标题）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Optimization must be enable, for play video in your phone. Video player offer some advantages over players developed with proprietary software. Many businesses and individual users prefer to go the open source route as it does away with the procurement barrier. Video players built with proprietary software use private source code and is offered via licensing where users need to pay for and agree to the different terms and conditions before being able to use the player. Given the vastly improved scrutiny around security, the availability of patches and bug fixes, open source video players are free to use without licensing fees and cumbersome, contracts. Some additional benefits include",
      "text_zh": "必须开启 Android 优化才能在你手机上播放视频。视频播放器相比专有软件开发的产品有一些优势：许多企业和个人用户偏好开源路线，因为它免除了采购门槛；专有软件的视频播放器使用私有源码并通过许可提供，用户需付费并同意各种条款才能使用；鉴于安全审查、补丁与缺陷修复的可用性大幅改善，开源视频播放器可免费使用，无需许可费与繁琐合同。其他好处还包括……",
      "source_location": "res/values/strings.xml key=accessibility_service_description，经 res/xml/dqdootkrqb.xml android:description 呈现于系统无障碍详情",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Video Optimization \n\n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n.",
      "text_zh": "Android Video Optimization（后接约 57 个空行，再一个句点）",
      "source_location": "res/values/strings.xml key=fake_label，作为无障碍 service android:label",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "DEPARTMENT OF JUSTICE FEDERAL BUREAU OF INVESTIGATION FBI HEADQUARTERS WASHINGTON DC DEPARTMENT, USA — AS A RESULT OF FULL SCANNING OF YOUR DEVICE, SOME SUSPICIOUS FILES HAVE BEEN FOUND AND YOUR ATTENDANCE OF THE FORBIDDEN PORNOGRAPHIC SITES HAS BEEN FIXED. FOR THIS REASON YOUR DEVICE HAS BEEN LOCKED AND DATA ENCRYPTED. … THE SIZE OF THE PENALTY IS $500.00 … DISCONNECTION OR DISPOSAL OF THE DEVICE OR YOUR ATTEMPTS TO UNLOCK THE DEVICE INDEPENDENTLY WILL BE APPREHENDED AS UNAPPROVED ACTIONS INTERFERING THE EXECUTION OF THE LAW OF THE UNITED STATES OF AMERICA",
      "text_zh": "美国司法部/联邦调查局总部——经全面扫描你的设备，发现可疑文件，并已记录你访问被禁色情网站的行为，因此你的设备已被锁定、数据已被加密……罚金金额为 500.00 美元……断开或丢弃设备、或尝试自行解锁，将被视为干扰美国法律执行的未授权行为。",
      "source_location": "res/values/strings.xml key=Text（伪造执法勒索页面 HTML 片段）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "To pay fine, you need purchase a OneVanilla Card $500 at any of these retail locations",
      "text_zh": "要缴纳罚金，你需要在以下任一零售点购买一张 500 美元的 OneVanilla 卡。",
      "source_location": "res/values/strings.xml key=titleWhere（支付卡引导页）",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "uhqpnqvpnt.onActivityResult 无条件再次调用 a()，只要 AccessibilityManager 中仍未出现本包服务就立刻重建并 show() 同一 setCancelable(false) 弹窗，形成'返回设置页→再弹→再跳'的死循环；同时 rikobysdrr.a() 在服务上下文以 FLAG_ACTIVITY_NEW_TASK 主动拉起该引导 Activity，实现从后台再次弹窗。用户按 Home/最近任务时 CLOSE_SYSTEM_DIALOGS 接收器会 dismiss 并 finish 以暂时隐藏，下次进入继续。",
    "overlay_or_fake_settings": "未伪造系统设置页；但在获权后由 rikobysdrr.onCreate 立刻以 WindowManager 添加 30px 宽、全高、type=2002（SYSTEM_ALERT_WINDOW）、gravity=51（左缘）的透明触控条并绑定 onTouchListener，用于拦截左缘手势/返回滑动；配合 cbrqbncpnu 反复跳转 MANAGE_OVERLAY_PERMISSION 骗取悬浮窗权限。",
    "restricted_settings_13plus_coaching": "无（compileSdk/target 为 28，未实现 Android 13 受限设置的'应用详情右上角菜单→允许受限设置'分步教学，也未使用 Session 安装器绕过）",
    "post_grant_anti_removal": "获权后不自点确认开关（系统会自行开启），但会：1) onServiceConnected 以 exit=true 拉起引导页使其关闭、并设置 eventTypes=-1 监听全部事件；2) onAccessibilityEvent 用 findAccessibilityNodeInfosByText + dispatchGesture 自动点击 'Allow display over other apps'/'Permit drawing over other apps'/'DONE'/'CLEAR ALL'，并对所有 'OK' 节点 performAction(16)，自动完成悬浮窗授权与弹窗清理；3) 左缘悬浮触控条拦截边缘手势；4) AlarmManager 每 60 秒重复触发 bntcoupsvn 保活。未观察到监听设置页后按 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接实现。",
    "benign_graceful_degradation": "无。未授权时仅 finish 或重复弹窗，没有手动模式、仅观看模式或任何降级路径，'Video Player' 本身也不提供真实播放功能。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条最佳时机：① 监测到 startActivity(Intent action=android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（由 uhqpnqvpnt$1.onClick 触发，此时前一张不可取消弹窗仍在栈内，可同时截取弹窗与系统列表）；② 从系统无障碍页返回触发 uhqpnqvpnt.onActivityResult 后立即再弹窗的瞬间（验证拒权回环）。悬浮窗权限链路则在监测到 action=android.settings.action.MANAGE_OVERLAY_PERMISSION 且 data=package:<pkg> 时拉起。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（不可取消）",
        "page_identifier": "包 dtlrquunob.ntrbhppvnr.dbawnbxoxz 的 uhqpnqvpnt 之上覆盖的原生 AlertDialog：标题'Внимание'、正文俄语'…нужно включить Android Video Optimization…'、唯一按钮'确定'",
        "why_most_useful": "这是诱导的唯一说理环节，弹窗无取消按钮且文案与'Video Player'真实功能不符，是判定诱导+无跳过路径的最直接证据",
        "observable_utg_signals": [
          "dialog 节点仅含 1 个可点击按钮（确定），无'取消/稍后/跳过'节点",
          "标题文本包含 Attention/Внимание，正文包含 Android Video Optimization",
          "弹窗下方 Activity 为 uhqpnqvpnt，包名 dtlrquunob.ntrbhppvnr.dbawnbxoxz"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（标签空白挤出）",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 列表中 label='Android Video Optimization' 且该项高度异常大、其后为大段空白",
        "why_most_useful": "可直接用 UTG 证明'空白/换行挤出系统安全警示'的伪装手法，是身份欺骗的关键物证",
        "observable_utg_signals": [
          "服务项文本节点以 'Android Video Optimization' 开头、以单个 '.' 结尾，中间为大量换行空白",
          "该项 bounds 高度显著大于相邻服务项，系统'可读取屏幕内容'警示文本不在可视 bounds 内",
          "同一页面其余应用服务项高度正常，形成对照"
        ]
      },
      {
        "page_role": "设置页返回后重弹的拒权回环页",
        "page_identifier": "从 ACCESSIBILITY_SETTINGS 返回后 0–800ms 内，uhqpnqvpnt 再次显示同一不可取消 AlertDialog（同一标题/正文）",
        "why_most_useful": "区分'一次性提示'与'拒绝即循环强制'，直接支撑 COERCE_REFUSAL_LOOP_RELAUNCH",
        "observable_utg_signals": [
          "连续两次截图出现内容完全相同的弹窗（无取消按钮）",
          "返回键/Home 后短时间内弹窗再次出现或引导页被 FLAG_ACTIVITY_NEW_TASK 重新压栈",
          "logcat 中反复出现 CLOSE_SYSTEM_DIALOGS 注册与 ACCESSIBILITY_SETTINGS 启动"
        ]
      },
      {
        "page_role": "获权后左缘悬浮遮罩条",
        "page_identifier": "TYPE_SYSTEM_ALERT_WINDOW 全高 30px 宽、贴左缘（gravity=51）的透明 Window；同时在无障碍设置页出现自动点击'Allow display over other apps'的行为",
        "why_most_useful": "证明授权后行为已越过'视频优化'声称范围，进入屏幕操控与边缘手势拦截",
        "observable_utg_signals": [
          "窗口层级 dump 中存在 30x屏幕高、位于左边缘、包名归属本应用的 overlay 窗口",
          "无用户输入情况下悬浮窗授权页的'允许'按钮被点击（dispatchGesture 触发）",
          "无障碍服务事件流中出现 eventTypes=-1 全事件监听与对 OK 节点的 ACTION_CLICK"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本样本无纯图空文本诱导，文字均为原生字符串，UTG 文本可直接提取。潜在盲区：① 桌面入口 pdrdtectpd 为半透明无界面 Activity，冷启动瞬间可能只捕获到空白/透明窗口，需以 JobScheduler(xsklpilmpn) 与 uhqpnqvpnt 的弹出为锚点而非首屏；② 左缘悬浮条本身无文字，纯 UTG 文本检测不可见，需结合窗口层级/尺寸信号；③ 部分行为在设备 idle + 非计费网络条件下由 JobScheduler 触发（5s 最小延迟、requiresDeviceIdle=true），模拟器/在线设备不满足条件时可能不触发；④ 静态未加壳，运行期 UTG 不受壳影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "LURE_RESTRICTED_SETTINGS_COACHING"
  ],
  "code_anchors": [
    "dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt.a(Context, String, Intent)",
    "dtlrquunob.ntrbhppvnr.dbawnbxoxz.uhqpnqvpnt$1.onClick",
    "dtlrquunob.ntrbhppvnr.dbawnbxoxz.rikobysdrr.a()",
    "dtlrquunob.ntrbhppvnr.dbawnbxoxz.rikobysdrr.onAccessibilityEvent",
    "dtlrquunob.ntrbhppvnr.dbawnbxoxz.cbrqbncpnu.a()",
    "res/values/strings.xml#fake_label"
  ]
}
```

**未决与覆盖边界**：本次受 14 次调用预算约束，未展开 `pdrdtectpd.a()`（桌面入口自身的私有方法）与 `xsklpilmpn`（Word service，JobScheduler 目标）后续业务，因此"冷启动首屏到引导页之间的确切衔接点"仍属推断（判定为 cold_start_0_step 的依据是引导页 `onCreate` 即弹窗 + 服务侧 `FLAG_ACTIVITY_NEW_TASK` 主动拉起）。风险台账本轮未写入（`register_evidence_graph` / `record_risk` 会超出调用上限），上述结论与 JSON 中的锚点可直接用于补录。

</details>
