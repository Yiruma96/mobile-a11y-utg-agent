# MR_003__05bbe4182b｜Lucy — Video Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：97.8s

## 1. 一句话核心结论

- **核心申请方式**：以“Video Player”外壳在冷启动后自禁用桌面图标并经 JobScheduler 延迟拉起不可取消的原生弹窗，谎称必须开启“Android Video Optimization”，仅提供 OK 按钮跳转系统无障碍页，返回即无限重弹，获权后立刻自杀弹窗并用无障碍节点查找+performAction/dispatchGesture 自动点掉 ALLOW/OK 与悬浮窗授权。
- **静态可见性说明**：未加壳、无加密载荷、无动态加载代码；引导弹窗、跳转 Intent、无障碍服务自动点击逻辑与全部文案均在 classes.dex 与 res/values/strings.xml 中明文可见。无障碍 XML 未声明 canPerformGestures，但运行期 dispatchGesture 代码存在，属声明缺失而非不可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `05bbe4182b890c91ff96ef7bf39e5dd94feae83d5067ccdc9703a05278b9983d` |
| 包名 / 年份 | `gcoojdprtw.tsqrstjtdi.crwrnqoqur` / 2020 |
| 家族 / 品类 | **Lucy**（同池样本数：81） |
| 原始来源标识 | https://research.checkpoint.com/2020/lucys-back-ransomware-goes-mobile/ |
| 桌面显示名 | Video Player |
| 引导页宣称品牌/身份 | Android Video Optimization（伪造的系统级视频优化能力） |
| 系统无障碍列表服务名 | Android Video Optimization \n\n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n. |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务标签使用「Android Video Optimization 」后接数十个换行符再跟一个句点，把系统无障碍列表中的风险警告文字挤出可视区域；android:description 用大段开源播放器免授权费/补丁及时的良性说辞掩盖读屏与模拟点击能力；启动器 Activity 在 onCreate 中立即 setComponentEnabledSetting(DISABLED) 自禁用图标；targetSdk 26 未使用 isAccessibilityTool 声明。 |
| 无障碍服务类名 | `gcoojdprtw.tsqrstjtdi.crwrnqoqur.tfpnnoqcrp` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Android Optimization must be enable, for play video in your phone.<br> Video player offer some advantages over players developed with proprietary software. Many businesses and individual users prefer to go the open source route as it does away with the procurement barrier. <br> Video players built with proprietary software use private source code and is offered via licensing where users need to pay for and agree to the different terms and conditions before being able to use the player. <br> Given the vastly improved scrutiny around security, the availability of patches and bug fixes, open source video players are free to use without licensing fees and cumbersome, contracts. Some additional benefits include |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | gcoojdprtw.tsqrstjtdi.crwrnqoqur.orohspqojr（LAUNCHER Activity，label=ReqPerm） | onCreate：setContentView 后调用 a() 自禁用组件，再调用 c.a(context) 投递 JobScheduler | 原生Activity | **原文**：无（该页无可见引导文案）<br>**译注**：无可见文案；应用启动即隐藏桌面图标并把后续动作交给 5 秒延迟的 Job 与常驻服务 | 无（用户仅看到启动后立即跳走/消失） | `orohspqojr.onCreate / orohspqojr.a / c.a` |
| 2 | 引导说明页 | gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq 上的 AlertDialog（theme 5，SDK<23 时 window type=2010 TYPE_SYSTEM_ALERT） | xqbbbwdsrq.onCreate → a()；条件 tfpnnoqcrp.b == false（无障碍服务未连接）；亦由 onActivityResult 与 tfpnnoqcrp.a() 反复触发 | 原生Dialog | **原文**：Title: Внимание / Attention；Message: Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее.；按钮：ok<br>**译注**：标题“注意”；正文“为了继续观看视频文件，需要开启 Android Video Optimization（视频流优化），请开启它。”；仅一个 OK 按钮 | 只能点击 OK；setCancelable(false)，无取消/跳过按钮，返回键与点击外部均无法关闭 | `xqbbbwdsrq.a(Context,String,Intent) / res/values/strings.xml: Activate_Access, Attention` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | AlertDialog 正按钮回调 xqbbbwdsrq$1.onClick → startActivityForResult(intent, 0) | 系统无障碍页 | **原文**：无（应用自身不渲染该页）<br>**译注**：进入系统无障碍设置列表，其中列出名为“Android Video Optimization”+大量空白的服务项 | 要求用户自行找到该服务项并打开开关；应用侧无任何操作指引或高亮 | `xqbbbwdsrq$1.onClick / xqbbbwdsrq.a() 中的 Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(8388608)` |
| 4 | 拒权反馈循环 | xqbbbwdsrq.onActivityResult → a() → 同一不可取消 AlertDialog | 用户从系统设置页返回（无论是否开启）触发 onActivityResult；若 tfpnnoqcrp.b 仍为 false 则重新弹窗 | 原生Dialog | **原文**：Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее.<br>**译注**：同一步骤 2 的俄文“必须开启优化才能看视频”提示再次弹出，无跳过路径 | 只能再次点 OK 回到无障碍设置，形成无限循环；按 Home/最近任务时 CLOSE_SYSTEM_DIALOGS 接收器会 dismiss 并 finish，但服务侧 a() 仍会再次拉起 | `xqbbbwdsrq.onActivityResult / xqbbbwdsrq$a.onReceive / tfpnnoqcrp.a()` |
| 5 | 获权后动作 | gcoojdprtw.tsqrstjtdi.crwrnqoqur.tfpnnoqcrp（无障碍服务） | onServiceConnected：置 b=true，以 exit=true 启动 xqbbbwdsrq 令其 finish（弹窗自动消失），setServiceInfo(flags=19, eventTypes=-1, notificationTimeout=100) | 系统无障碍页 | **原文**：自动匹配节点文本：Allow display over other apps / Permit drawing over other apps / If you don’t want / DONE / CLEAR ALL / ALLOW / OK<br>**译注**：服务自行在系统授权弹窗中查找并点击“允许在其他应用上层显示”“允许绘制”“ALLOW”“OK”“DONE”“CLEAR ALL”等按钮 | 无需用户操作：应用用 performAction(16) 与 dispatchGesture 以坐标手势自动点掉悬浮窗授权与系统允许按钮，实现无真实同意的自授权 | `tfpnnoqcrp.onServiceConnected / tfpnnoqcrp.onAccessibilityEvent / tfpnnoqcrp.a(AccessibilityEvent,String)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- xqbbbwdsrq 上不可取消的 AlertDialog（setCancelable(false)，仅 OK 按钮；SDK<23 以 TYPE_SYSTEM_ALERT 悬浮窗类型显示）——正文 Activate_Access 俄文提示
- 同一 AlertDialog 的标题 Attention / Внимание
- 系统无障碍服务列表项标签 @string/fake_label："Android Video Optimization " + 数十个换行 + "."（用空白把风险警告挤出可视区）
- 系统无障碍服务详情页 android:description = @string/accessibility_service_description（长篇“开源播放器免授权费/补丁及时/更安全”的良性说辞）
- res/values/strings.xml 中的同包勒索/欺诈文案：titleWhere（OneVanilla Card $500）、textSend（Card sent for verification…）、Caption（Enter the data to pay the fine）——不参与无障碍引导，属后续欺诈环节
- 无 WebView / 本地 HTML / 远端 HTML / 悬浮遮罩引导窗，全部引导文字仅上述原生 Dialog 与系统无障碍页两处

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее. | 为了继续观看视频文件，需要开启 Android Video Optimization（视频流优化），请开启它。 | `res/values/strings.xml key=Activate_Access，由 xqbbbwdsrq.a() 以 getResources().getString(2131296256) 作为 AlertDialog message` | 假更新 |
| ru | Внимание | 注意 | `res/values/strings.xml key=Attention，xqbbbwdsrq.a() 中 setTitle(getString(2131296257))` | 故障恐吓 |
| en | Android Video Optimization <br><br><br><br><br><br><br><br><br> <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>. | Android Video Optimization（其后大量换行与一个句点，用于把系统风险警告文字挤出可见区域） | `res/values/strings.xml key=fake_label，Manifest 中 accessibility service 的 android:label` | 假更新 |
| en | Android Optimization must be enable, for play video in your phone. Video player offer some advantages over players developed with proprietary software. Many businesses and individual users prefer to go the open source route as it does away with the procurement barrier. Video players built with proprietary software use private source code and is offered via licensing where users need to pay for and agree to the different terms and conditions before being able to use the player. Given the vastly improved scrutiny around security, the availability of patches and bug fixes, open source video players are free to use without licensing fees and cumbersome, contracts. Some additional benefits include | 为在手机上播放视频必须开启 Android Optimization。视频播放器相比专有软件播放器有一些优势：许多企业和个人用户倾向开源路线，因为免去采购门槛……开源播放器可免费使用、无需授权费和繁琐合同，还享有更好的安全审查与补丁更新。其他额外好处包括…… | `res/values/strings.xml key=accessibility_service_description，Manifest 服务 meta-data res/xml/ytgpqornrt.xml 的 android:description` | 假更新 |
| en | Allow display over other apps | 允许在其他应用上层显示（悬浮窗授权弹窗按钮文本，被服务自动点击） | `tfpnnoqcrp.onAccessibilityEvent 中硬编码的 findAccessibilityNodeInfosByText 目标串` | 未知 |
| en | Permit drawing over other apps | 允许绘制在其他应用上层（悬浮窗授权弹窗按钮文本，被服务自动点击） | `tfpnnoqcrp.onAccessibilityEvent 中硬编码的 findAccessibilityNodeInfosByText 目标串` | 未知 |
| en | To pay fine, you need purchase a OneVanilla Card $500 at any of these retail locations | 为缴纳罚款，你需要到以下任一零售点购买一张 500 美元的 OneVanilla 预付卡 | `res/values/strings.xml key=titleWhere（同包后续欺诈/锁屏环节文案，非无障碍引导页）` | 假反诈安全 |
| en | Card sent for verification. If there are no problems with paying the fine, the device will unlock automatically. | 卡信息已发送核验。若缴纳罚款无问题，设备将自动解锁。 | `res/values/strings.xml key=textSend（同包后续欺诈/锁屏环节文案）` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：从系统无障碍页返回即触发 xqbbbwdsrq.onActivityResult 无条件调用 a()；若 tfpnnoqcrp.b 仍为 false 则再次弹出同一不可取消 AlertDialog（仅 OK），用户只能反复回到设置页；按 Home/最近任务时 CLOSE_SYSTEM_DIALOGS 接收器 dismiss 弹窗并 finish，但无障碍服务 a() 检测到未启用会再次 startActivity 拉起，形成跨页面死循环；此外 orohspqojr 启动时投递的 JobScheduler（5 秒、需网络与空闲）与常驻服务 ppduosmcrx 保证后台重复拉起。
- **遮罩叠层 / 高仿系统设置页**：无高仿系统设置页；但 SDK<23 时弹窗以 window type 2010（TYPE_SYSTEM_ALERT）悬浮窗方式显示，且申请 SYSTEM_ALERT_WINDOW 权限，获权后自行点掉悬浮窗授权以维持叠层能力。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：获权后 onServiceConnected 以 exit=true 启动 xqbbbwdsrq 使其自行 finish（关闭诱导弹窗），随后 onAccessibilityEvent 用 findAccessibilityNodeInfosByText 匹配 "ALLOW"/"OK" 并 performAction(16)，以及 dispatchGesture 按节点 Rect 坐标点击 "Allow display over other apps"/"Permit drawing over other apps"/"If you don’t want"/"DONE"/"CLEAR ALL"，自动完成悬浮窗与系统权限授权；未见 GLOBAL_ACTION_BACK/HOME 阻止撤权逻辑。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：纯 UTG 检测应在两处拉起：①冷启动后 5 秒内（orohspqojr 自禁用 + Job 延迟）首个 Activity 变为 xqbbbwdsrq 且屏幕出现不可取消 Dialog 时；②监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS（或从设置页返回 onActivityResult 后同一 Dialog 再次出现）的瞬间，此时最能体现“返回即重弹”的拒权循环。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本样本无图片诱导、无 WebView/HTML 载体，纯原生 Dialog + 系统页面，UTG 文本节点即可完整判别。潜在盲区：无障碍配置未声明 canPerformGestures，dispatchGesture 在部分 ROM 可能静默失败，导致“自动点悬浮窗授权”在真机上不一定成功，但 performAction(16) 路径不受影响；另启动器图标被自禁用后可能被误判为“无桌面入口”的静默安装体，需以 Job/服务拉起作为观测起点。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | Activity gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq 上的 Dialog，标题 Attention/Внимание，正文含 "Android Video Optimization" 与 "потоковую оптимизацию видео"，仅一个 OK 按钮 | 该弹窗是整条诱导链的起点，可直接证明不可取消、无跳过按钮、以“必须开启优化才能播放”为由强迫用户前往无障碍设置 | Dialog 可点击按钮数量为 1（仅 OK），无取消/返回关闭；正文出现 "Android Video Optimization" 与 "просмотр видео" 组合的伪系统优化话术；按下返回键或 Home 后弹窗仍复现（循环证据） |
| **系统无障碍服务列表项** | 系统设置 无障碍 → 已下载的服务，条目名称以 "Android Video Optimization " 开头并带大量空白后跟 "."；详情描述为开源播放器免授权费的长段英文 | 直接暴露空白挤出警告的伪装手法与标签/描述与实际读屏+模拟点击能力不符的身份错配 | 服务项标签文本含连续换行/大段空白（可对节点文本长度与可见字符比做异常判定）；描述文本出现 "open source"、"licensing fees" 等与视频优化无关的良性说辞；服务名与实际应用名 "Video Player" 不一致 |
| **跳转后压栈的悬浮窗/权限授权页** | 系统 "Allow display over other apps" / "Permit drawing over other apps" 页面或运行时权限 ALLOW 弹窗 | 验证获权后应用通过无障碍节点查找 + performAction/dispatchGesture 自动点击系统按钮的自动化授权行为，这是最关键的越权证据 | 授权弹窗在无真实点击事件注入的情况下自动消失（按钮被程序点击）；logcat 出现 EVENT_CHANGEDeG / EVENT_CHANGED source2 / Start vending 等该家族特征日志；悬浮窗授权被授予但用户未操作 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq.a(Context,String,Intent)`
- `gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq.onActivityResult`
- `gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq$1.onClick`
- `gcoojdprtw.tsqrstjtdi.crwrnqoqur.tfpnnoqcrp.onAccessibilityEvent`
- `gcoojdprtw.tsqrstjtdi.crwrnqoqur.tfpnnoqcrp.onServiceConnected`
- `res/values/strings.xml (Activate_Access / Attention / fake_label / accessibility_service_description) 与 res/xml/ytgpqornrt.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（14 次工具调用内收口）。样本未加壳，无障碍诱导链路 100% 静态可见。

## 结论要点

**入口与“隐身”启动**
- 桌面启动的是 [orohspqojr.onCreate()](<resource-unit:#1.dex1 code:gcoojdprtw.tsqrstjtdi.crwrnqoqur.orohspqojr#onCreate>)：加载布局后立即调用 `setComponentEnabledSetting(..., 2, 1)` 把自身启动器组件**禁用**（图标消失），再通过 [c.a()](<resource-unit:#1.dex1 code:gcoojdprtw.tsqrstjtdi.crwrnqoqur.c#a>) 投递 5 秒延迟的 JobScheduler 任务（`glukmrqfob`），并拉起 `ppduosmcrx` 常驻服务。

**第 1 步：不可取消的原生弹窗**
- [xqbbbwdsrq.onCreate()](<resource-unit:#1.dex1 code:gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq#onCreate>) 注册 `CLOSE_SYSTEM_DIALOGS` 接收器后进入 `a()`：若无障碍服务未连接（`tfpnnoqcrp.b == false`），弹出 `AlertDialog`（theme 5），标题 `Attention`、正文 `Activate_Access`（俄文“需开启 Android Video Optimization 才能继续看视频”），**`setCancelable(false)`、只有 OK 一个按钮**；SDK<23 时用 `TYPE_SYSTEM_ALERT` 悬浮窗窗口类型显示。
- 用户按 Home/最近任务时，[xqbbbwdsrq$a.onReceive()](<resource-unit:#1.dex1 code:gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq$a#onReceive>) 反而 dismiss 弹窗并 finish（避免被系统弹窗清理器留证），服务侧 `a()` 会再把它拉起。

**第 2 步：跳转系统无障碍页**
- 点 OK → [xqbbbwdsrq$1.onClick()](<resource-unit:#1.dex1 code:gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq$1#onClick>) 执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(FLAG_ACTIVITY_NEW_TASK))`。全包仅此一处 `ACCESSIBILITY_SETTINGS`，无 `ACTION_APPLICATION_DETAILS_SETTINGS`、无受限设置教学、无 `isAccessibilityTool`。

**第 3 步：拒权死循环**
- 从设置页返回 → [onActivityResult()](<resource-unit:#1.dex1 code:gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq#onActivityResult>) 无条件再调 `a()`：仍未授权就再次弹出同一不可取消弹窗，形成“返回即重弹”的无限循环；无任何降级或跳过路径。

**第 4 步：获权后自关弹窗 + 自动点系统按钮**
- [tfpnnoqcrp.onServiceConnected()](<resource-unit:#1.dex1 code:gcoojdprtw.tsqrstjtdi.crwrnqoqur.tfpnnoqcrp#onServiceConnected>) 置 `b=true`，以 `exit=true` 启动 `xqbbbwdsrq` 使其自杀（弹窗消失），并 `setServiceInfo(flags=19, eventTypes=-1, timeout=100ms)` 全量监听。
- [onAccessibilityEvent()](<resource-unit:#1.dex1 code:gcoojdprtw.tsqrstjtdi.crwrnqoqur.tfpnnoqcrp#onAccessibilityEvent>) 用 `findAccessibilityNodeInfosByText("ALLOW"/"OK")` + `performAction(16)`/`dispatchGesture` 自动点击：覆盖**悬浮窗授权弹窗**（“Allow display over other apps”“Permit drawing over other apps”）、系统权限 “ALLOW”、“OK”，以及 `canDrawOverlays` 后的 “If you don't want”/“DONE”/“CLEAR ALL”，即无需用户真实同意的批量自授权。

**伪装与文本位置**
- 服务标签 `fake_label` 为 `"Android Video Optimization "` + 数十个 `\n` + `"."`——用换行把系统无障碍列表里的风险警告挤出可视区（空白挤出手法）。
- `android:description`（[accessibility_service_description](<resource-unit:#1 file:res/values/strings.xml#L16-L19>)）是一段关于“开源视频播放器免授权费、补丁及时、更安全”的长篇良性说辞，完全不提实际能力（读屏内容 + 模拟点击）。
- 引导文字仅出现在两处：`Activate_Access`（俄文弹窗正文）与上述系统无障碍列表描述；**无 WebView/HTML/悬浮遮罩页**，纯原生 Dialog + 系统设置页。
- 同包另有明显勒索/欺诈文案（`titleWhere` “To pay fine, you need purchase a OneVanilla Card $500…”、`textSend` “Card sent for verification…”），说明本 a11y 授权是后续支付卡窃取/锁屏的前置能力。

**与既有风险的关系**：本次核验完全支撑已登记的 [R-001](<resource-unit:#1 manifest:components>)（无障碍强制诱导与自动授权），未发现需要新增的独立命题；本报告仅补充纯运行期 UTG 视角的步骤细节。

```json
{
  "static_visibility": "clear",
  "visibility_note": "未加壳、无加密载荷、无动态加载代码；引导弹窗、跳转 Intent、无障碍服务自动点击逻辑与全部文案均在 classes.dex 与 res/values/strings.xml 中明文可见。无障碍 XML 未声明 canPerformGestures，但运行期 dispatchGesture 代码存在，属声明缺失而非不可见。",
  "summary_one_liner": "以“Video Player”外壳在冷启动后自禁用桌面图标并经 JobScheduler 延迟拉起不可取消的原生弹窗，谎称必须开启“Android Video Optimization”，仅提供 OK 按钮跳转系统无障碍页，返回即无限重弹，获权后立刻自杀弹窗并用无障碍节点查找+performAction/dispatchGesture 自动点掉 ALLOW/OK 与悬浮窗授权。",
  "disguise_identity": {
    "app_display_name": "Video Player",
    "claimed_brand_or_persona": "Android Video Optimization（伪造的系统级视频优化能力）",
    "a11y_service_label": "Android Video Optimization \\n\\n\\n\\n\\n\\n\\n\\n\\n \\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n.",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务标签使用「Android Video Optimization 」后接数十个换行符再跟一个句点，把系统无障碍列表中的风险警告文字挤出可视区域；android:description 用大段开源播放器免授权费/补丁及时的良性说辞掩盖读屏与模拟点击能力；启动器 Activity 在 onCreate 中立即 setComponentEnabledSetting(DISABLED) 自禁用图标；targetSdk 26 未使用 isAccessibilityTool 声明。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "gcoojdprtw.tsqrstjtdi.crwrnqoqur.orohspqojr（LAUNCHER Activity，label=ReqPerm）",
      "trigger_event": "onCreate：setContentView 后调用 a() 自禁用组件，再调用 c.a(context) 投递 JobScheduler",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该页无可见引导文案）",
      "shown_text_zh": "无可见文案；应用启动即隐藏桌面图标并把后续动作交给 5 秒延迟的 Job 与常驻服务",
      "user_action_requested": "无（用户仅看到启动后立即跳走/消失）",
      "code_anchor": "orohspqojr.onCreate / orohspqojr.a / c.a"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq 上的 AlertDialog（theme 5，SDK<23 时 window type=2010 TYPE_SYSTEM_ALERT）",
      "trigger_event": "xqbbbwdsrq.onCreate → a()；条件 tfpnnoqcrp.b == false（无障碍服务未连接）；亦由 onActivityResult 与 tfpnnoqcrp.a() 反复触发",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: Внимание / Attention；Message: Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее.；按钮：ok",
      "shown_text_zh": "标题“注意”；正文“为了继续观看视频文件，需要开启 Android Video Optimization（视频流优化），请开启它。”；仅一个 OK 按钮",
      "user_action_requested": "只能点击 OK；setCancelable(false)，无取消/跳过按钮，返回键与点击外部均无法关闭",
      "code_anchor": "xqbbbwdsrq.a(Context,String,Intent) / res/values/strings.xml: Activate_Access, Attention"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "AlertDialog 正按钮回调 xqbbbwdsrq$1.onClick → startActivityForResult(intent, 0)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用自身不渲染该页）",
      "shown_text_zh": "进入系统无障碍设置列表，其中列出名为“Android Video Optimization”+大量空白的服务项",
      "user_action_requested": "要求用户自行找到该服务项并打开开关；应用侧无任何操作指引或高亮",
      "code_anchor": "xqbbbwdsrq$1.onClick / xqbbbwdsrq.a() 中的 Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(8388608)"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "xqbbbwdsrq.onActivityResult → a() → 同一不可取消 AlertDialog",
      "trigger_event": "用户从系统设置页返回（无论是否开启）触发 onActivityResult；若 tfpnnoqcrp.b 仍为 false 则重新弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее.",
      "shown_text_zh": "同一步骤 2 的俄文“必须开启优化才能看视频”提示再次弹出，无跳过路径",
      "user_action_requested": "只能再次点 OK 回到无障碍设置，形成无限循环；按 Home/最近任务时 CLOSE_SYSTEM_DIALOGS 接收器会 dismiss 并 finish，但服务侧 a() 仍会再次拉起",
      "code_anchor": "xqbbbwdsrq.onActivityResult / xqbbbwdsrq$a.onReceive / tfpnnoqcrp.a()"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "gcoojdprtw.tsqrstjtdi.crwrnqoqur.tfpnnoqcrp（无障碍服务）",
      "trigger_event": "onServiceConnected：置 b=true，以 exit=true 启动 xqbbbwdsrq 令其 finish（弹窗自动消失），setServiceInfo(flags=19, eventTypes=-1, notificationTimeout=100)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "自动匹配节点文本：Allow display over other apps / Permit drawing over other apps / If you don’t want / DONE / CLEAR ALL / ALLOW / OK",
      "shown_text_zh": "服务自行在系统授权弹窗中查找并点击“允许在其他应用上层显示”“允许绘制”“ALLOW”“OK”“DONE”“CLEAR ALL”等按钮",
      "user_action_requested": "无需用户操作：应用用 performAction(16) 与 dispatchGesture 以坐标手势自动点掉悬浮窗授权与系统允许按钮，实现无真实同意的自授权",
      "code_anchor": "tfpnnoqcrp.onServiceConnected / tfpnnoqcrp.onAccessibilityEvent / tfpnnoqcrp.a(AccessibilityEvent,String)"
    }
  ],
  "text_presentation_locations": [
    "xqbbbwdsrq 上不可取消的 AlertDialog（setCancelable(false)，仅 OK 按钮；SDK<23 以 TYPE_SYSTEM_ALERT 悬浮窗类型显示）——正文 Activate_Access 俄文提示",
    "同一 AlertDialog 的标题 Attention / Внимание",
    "系统无障碍服务列表项标签 @string/fake_label：\"Android Video Optimization \" + 数十个换行 + \".\"（用空白把风险警告挤出可视区）",
    "系统无障碍服务详情页 android:description = @string/accessibility_service_description（长篇“开源播放器免授权费/补丁及时/更安全”的良性说辞）",
    "res/values/strings.xml 中的同包勒索/欺诈文案：titleWhere（OneVanilla Card $500）、textSend（Card sent for verification…）、Caption（Enter the data to pay the fine）——不参与无障碍引导，属后续欺诈环节",
    "无 WebView / 本地 HTML / 远端 HTML / 悬浮遮罩引导窗，全部引导文字仅上述原生 Dialog 与系统无障碍页两处"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Для того что бы продолжить просмотр видео файла, нужно включить Android Video Optimization (потоковую оптимизацию видео), пожалуйста включите ее.",
      "text_zh": "为了继续观看视频文件，需要开启 Android Video Optimization（视频流优化），请开启它。",
      "source_location": "res/values/strings.xml key=Activate_Access，由 xqbbbwdsrq.a() 以 getResources().getString(2131296256) 作为 AlertDialog message",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": "Внимание",
      "text_zh": "注意",
      "source_location": "res/values/strings.xml key=Attention，xqbbbwdsrq.a() 中 setTitle(getString(2131296257))",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Video Optimization \n\n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n.",
      "text_zh": "Android Video Optimization（其后大量换行与一个句点，用于把系统风险警告文字挤出可见区域）",
      "source_location": "res/values/strings.xml key=fake_label，Manifest 中 accessibility service 的 android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Optimization must be enable, for play video in your phone. Video player offer some advantages over players developed with proprietary software. Many businesses and individual users prefer to go the open source route as it does away with the procurement barrier. Video players built with proprietary software use private source code and is offered via licensing where users need to pay for and agree to the different terms and conditions before being able to use the player. Given the vastly improved scrutiny around security, the availability of patches and bug fixes, open source video players are free to use without licensing fees and cumbersome, contracts. Some additional benefits include",
      "text_zh": "为在手机上播放视频必须开启 Android Optimization。视频播放器相比专有软件播放器有一些优势：许多企业和个人用户倾向开源路线，因为免去采购门槛……开源播放器可免费使用、无需授权费和繁琐合同，还享有更好的安全审查与补丁更新。其他额外好处包括……",
      "source_location": "res/values/strings.xml key=accessibility_service_description，Manifest 服务 meta-data res/xml/ytgpqornrt.xml 的 android:description",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow display over other apps",
      "text_zh": "允许在其他应用上层显示（悬浮窗授权弹窗按钮文本，被服务自动点击）",
      "source_location": "tfpnnoqcrp.onAccessibilityEvent 中硬编码的 findAccessibilityNodeInfosByText 目标串",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Permit drawing over other apps",
      "text_zh": "允许绘制在其他应用上层（悬浮窗授权弹窗按钮文本，被服务自动点击）",
      "source_location": "tfpnnoqcrp.onAccessibilityEvent 中硬编码的 findAccessibilityNodeInfosByText 目标串",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "To pay fine, you need purchase a OneVanilla Card $500 at any of these retail locations",
      "text_zh": "为缴纳罚款，你需要到以下任一零售点购买一张 500 美元的 OneVanilla 预付卡",
      "source_location": "res/values/strings.xml key=titleWhere（同包后续欺诈/锁屏环节文案，非无障碍引导页）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Card sent for verification. If there are no problems with paying the fine, the device will unlock automatically.",
      "text_zh": "卡信息已发送核验。若缴纳罚款无问题，设备将自动解锁。",
      "source_location": "res/values/strings.xml key=textSend（同包后续欺诈/锁屏环节文案）",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "从系统无障碍页返回即触发 xqbbbwdsrq.onActivityResult 无条件调用 a()；若 tfpnnoqcrp.b 仍为 false 则再次弹出同一不可取消 AlertDialog（仅 OK），用户只能反复回到设置页；按 Home/最近任务时 CLOSE_SYSTEM_DIALOGS 接收器 dismiss 弹窗并 finish，但无障碍服务 a() 检测到未启用会再次 startActivity 拉起，形成跨页面死循环；此外 orohspqojr 启动时投递的 JobScheduler（5 秒、需网络与空闲）与常驻服务 ppduosmcrx 保证后台重复拉起。",
    "overlay_or_fake_settings": "无高仿系统设置页；但 SDK<23 时弹窗以 window type 2010（TYPE_SYSTEM_ALERT）悬浮窗方式显示，且申请 SYSTEM_ALERT_WINDOW 权限，获权后自行点掉悬浮窗授权以维持叠层能力。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "获权后 onServiceConnected 以 exit=true 启动 xqbbbwdsrq 使其自行 finish（关闭诱导弹窗），随后 onAccessibilityEvent 用 findAccessibilityNodeInfosByText 匹配 \"ALLOW\"/\"OK\" 并 performAction(16)，以及 dispatchGesture 按节点 Rect 坐标点击 \"Allow display over other apps\"/\"Permit drawing over other apps\"/\"If you don’t want\"/\"DONE\"/\"CLEAR ALL\"，自动完成悬浮窗与系统权限授权；未见 GLOBAL_ACTION_BACK/HOME 阻止撤权逻辑。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "纯 UTG 检测应在两处拉起：①冷启动后 5 秒内（orohspqojr 自禁用 + Job 延迟）首个 Activity 变为 xqbbbwdsrq 且屏幕出现不可取消 Dialog 时；②监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS（或从设置页返回 onActivityResult 后同一 Dialog 再次出现）的瞬间，此时最能体现“返回即重弹”的拒权循环。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "Activity gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq 上的 Dialog，标题 Attention/Внимание，正文含 \"Android Video Optimization\" 与 \"потоковую оптимизацию видео\"，仅一个 OK 按钮",
        "why_most_useful": "该弹窗是整条诱导链的起点，可直接证明不可取消、无跳过按钮、以“必须开启优化才能播放”为由强迫用户前往无障碍设置",
        "observable_utg_signals": [
          "Dialog 可点击按钮数量为 1（仅 OK），无取消/返回关闭",
          "正文出现 \"Android Video Optimization\" 与 \"просмотр видео\" 组合的伪系统优化话术",
          "按下返回键或 Home 后弹窗仍复现（循环证据）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 无障碍 → 已下载的服务，条目名称以 \"Android Video Optimization \" 开头并带大量空白后跟 \".\"；详情描述为开源播放器免授权费的长段英文",
        "why_most_useful": "直接暴露空白挤出警告的伪装手法与标签/描述与实际读屏+模拟点击能力不符的身份错配",
        "observable_utg_signals": [
          "服务项标签文本含连续换行/大段空白（可对节点文本长度与可见字符比做异常判定）",
          "描述文本出现 \"open source\"、\"licensing fees\" 等与视频优化无关的良性说辞",
          "服务名与实际应用名 \"Video Player\" 不一致"
        ]
      },
      {
        "page_role": "跳转后压栈的悬浮窗/权限授权页",
        "page_identifier": "系统 \"Allow display over other apps\" / \"Permit drawing over other apps\" 页面或运行时权限 ALLOW 弹窗",
        "why_most_useful": "验证获权后应用通过无障碍节点查找 + performAction/dispatchGesture 自动点击系统按钮的自动化授权行为，这是最关键的越权证据",
        "observable_utg_signals": [
          "授权弹窗在无真实点击事件注入的情况下自动消失（按钮被程序点击）",
          "logcat 出现 EVENT_CHANGEDeG / EVENT_CHANGED source2 / Start vending 等该家族特征日志",
          "悬浮窗授权被授予但用户未操作"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本样本无图片诱导、无 WebView/HTML 载体，纯原生 Dialog + 系统页面，UTG 文本节点即可完整判别。潜在盲区：无障碍配置未声明 canPerformGestures，dispatchGesture 在部分 ROM 可能静默失败，导致“自动点悬浮窗授权”在真机上不一定成功，但 performAction(16) 路径不受影响；另启动器图标被自禁用后可能被误判为“无桌面入口”的静默安装体，需以 Job/服务拉起作为观测起点。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq.a(Context,String,Intent)",
    "gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq.onActivityResult",
    "gcoojdprtw.tsqrstjtdi.crwrnqoqur.xqbbbwdsrq$1.onClick",
    "gcoojdprtw.tsqrstjtdi.crwrnqoqur.tfpnnoqcrp.onAccessibilityEvent",
    "gcoojdprtw.tsqrstjtdi.crwrnqoqur.tfpnnoqcrp.onServiceConnected",
    "res/values/strings.xml (Activate_Access / Attention / fake_label / accessibility_service_description) 与 res/xml/ytgpqornrt.xml"
  ]
}
```

</details>
