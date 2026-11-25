# MR_140__eabc604fe6｜Asacub — СМС - Послaние

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：95.2s

## 1. 一句话核心结论

- **核心申请方式**：冷启动先弹'图片无法显示/正在删除/已删除'三个 Toast 并自禁用桌面图标制造'应用已消失'假象，78 秒后由后台 IntentService 每约 10 秒无限重弹不可取消的'系统故障'原生 AlertDialog，三步教学把用户送进系统无障碍设置页，获权后自动点击确认按钮并对远端下发包名执行 GLOBAL_ACTION_BACK 阻止撤权。
- **静态可见性说明**：全部引导链、文案与跳转均为未加壳 DEX 内硬编码（Broccoli/OffsetUser/Fragrant/PushStable），无 WebView、无本地或远端 HTML、无加密载荷；仅远端 C2（http://myownbehap.com/i7ux8p8nhfvt/index.php）下发的拦截包名列表属运行期数据，不影响无障碍引导链的静态可见性。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `eabc604fe6b5943187c12b8635755c303c450f718cc0c8e561df22a27264f101` |
| 包名 / 年份 | `com.petty.account` / 2018 |
| 家族 / 品类 | **Asacub**（同池样本数：9） |
| 原始来源标识 | https://securelist.com/the-rise-of-mobile-banker-asacub/87591/ |
| 桌面显示名 | СМС - Послaние |
| 引导页宣称品牌/身份 | 系统/系统主进程（'Cиcтeмная неполадкa' 系统故障提示 + 'Ocнoвнoй процecс' 主进程）与短信应用 |
| 系统无障碍列表服务名 | Ocнoвнoй процecс |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：西里尔/拉丁同形字混排：显示名 'СМС - Послaние'、服务名 'Ocнoвнoй процecс'（仿 'Основной процесс'）、弹窗标题 'Cиcтeмная неполадкa'、正文 'Для устраннения прoблемы...' 均夹入拉丁 o/c/e/a/p；无障碍配置 res/xml/wyzqy.xml 完全省略 android:description，使系统服务列表说明列为空白以回避审查提示；LAUNCHER Activity 启动后立即 setComponentEnabledSetting(...,2,1) 自禁用，制造'应用已被删除'的组件级伪装。 |
| 无障碍服务类名 | `com.petty.account.PushStable` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.petty.account.Broccoli（LAUNCHER Activity，Theme.Translucent.NoTitleBar） | onCreate：先 d.e() 启动 Clash/Fragrant 后台服务，再连弹 Toast，最后 finish() | 通知栏 | **原文**：К сожалению изобрaжeние не может быть отoбражeно. / Удаляем приложeниe... / Приложeниe удaлeнo!<br>**译注**：很遗憾，图片无法显示。／正在删除应用……／应用已删除！ | 无需操作，仅 3 个连续 Toast；随后桌面图标被自禁用，无取消或跳过入口 | `com.petty.account.Broccoli.onCreate` |
| 2 | 冷启动入口 | PackageManager 组件状态（桌面图标） | Broccoli.b() 调用 setComponentEnabledSetting(a(), 2, 1) 禁用自身 | 不可静态还原 | 无 | 无；用户只能通过后续自动弹出的对话框继续被引导 | `com.petty.account.Broccoli#b` |
| 3 | 业务功能触发 | com.petty.account.Fragrant（IntentService）循环 + com.petty.account.d 判定 | onHandleIntent → a()：首次把激活时间写为 now+78210ms；到点后检查 Settings.Secure.enabled_accessibility_services 是否含 com.petty.account | 不可静态还原 | 无 | 无 | `com.petty.account.Fragrant.a / com.petty.account.d.f` |
| 4 | 引导说明页 | com.petty.account.OffsetUser（原生 Activity）中的 AlertDialog | d.b(Context, long) 节流通过后 startActivity(OffsetUser)（FLAG_ACTIVITY_NEW_TASK\|FLAG_ACTIVITY_CLEAR_TOP）→ OffsetUser.onCreate 构窗 | 原生Dialog | **原文**：标题：Cиcтeмная неполадкa<br>正文：Для устраннения прoблемы Вам нeобходимо включить 'Ocнoвнoй процecс'<br>1.Для этого перейдитe нa cтрaницу наcтроек<br>2.Выберите из спиcка 'Ocнoвнoй процecс'<br>3.Включите его.<br>按钮：Перeйти к нacтрoйкам<br>**译注**：标题：系统故障。正文：为解决该问题，您需要启用「主进程」：1. 请前往设置页面；2. 从列表中选择「主进程」；3. 将其启用。按钮：前往设置。 | 只提供一个正向按钮'前往设置'；setCancelable(false)，无取消、无跳过、无关闭，按返回键亦无法正常退出引导 | `com.petty.account.OffsetUser.onCreate` |
| 5 | 跳无障碍设置 | 系统 Settings 无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS） | OffsetUser$1.onClick → OffsetUser.a()：startActivity(Intent(ACCESSIBILITY_SETTINGS).addFlags(FLAG_ACTIVITY_NEW_TASK))，随后 finish() | 系统无障碍页 | **原文**：无（应用自身不提供任何说明页；系统列表项名称即 'Ocнoвнoй процecс'，说明列为空）<br>**译注**：应用直接进入系统无障碍设置，用户需在列表中找到伪装为「主进程」的条目并打开 | 要求用户在系统设置中手动开启 Ocнoвнoй процecс 服务；应用未提供任何取消或跳过分支 | `com.petty.account.OffsetUser#a` |
| 6 | 拒权反馈循环 | Fragrant 自重启循环 → 再次 startActivity(OffsetUser) 并重弹同一 AlertDialog | Fragrant.a() 的 finally 块 d.a(350) + d.d() 每轮重启自身；d.b() 以 9951ms 节流在未获权时再次拉起 OffsetUser | 原生Dialog | **原文**：Cиcтeмнaя неполадкa / Для устраннения прoблемы Вам нeобходимо включить 'Ocнoвнoй процecс'<br>**译注**：同一'系统故障'弹窗周期性无限重弹（约每 10 秒一次），用户返回或拒绝后仍会被再次打断 | 反复要求点击'前往设置'并开启服务，无降级路径、无'稍后再说'、无退出按钮 | `com.petty.account.Fragrant#a / com.petty.account.d#b(android.content.Context, long)` |
| 7 | 获权后动作 | com.petty.account.PushStable（AccessibilityService）+ 系统设置页/授权确认弹窗 | onServiceConnected → d.e() 拉起主业务；onAccessibilityEvent 收到 WindowStateChanged/ContentChanged 后遍历节点 | 系统无障碍页 | **原文**：匹配的节点 id：android:id/button1、android:id/right_button、android:id/restricted_action、android:id/action_button、com.android.settings:id/action_button、com.android.settings:id/restricted_action；文本匹配：да / ок / подтвердить / разрешить / отправить / активировать<br>**译注**：自动点击系统对话框的'确定/允许/受限设置允许'类按钮完成自授权；对远端下发包名列表命中的界面执行 GLOBAL_ACTION_BACK（返回）以阻止用户撤销无障碍授权 | 无需用户操作；由服务代替用户确认，并在用户试图关闭授权时被强制退回 | `com.petty.account.PushStable.onAccessibilityEvent / com.petty.account.PushStable#a(android.view.accessibility.AccessibilityNodeInfo)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Broccoli.onCreate 内 3 个连续 Toast（硬编码字符串）：'К сожалению изобрaжeние не может быть отoбражeно.'、'Удаляем приложeниe...'、'Приложeниe удaлeнo!'
- OffsetUser.onCreate 中不可取消的原生 AlertDialog：标题 'Cиcтeмная неполадкa' + 三步教学正文 + 单一按钮 'Перeйти к нacтрoйкам'（均为 Java 硬编码，未走 strings.xml）
- AndroidManifest 中无障碍服务 android:label="Ocнoвнoй процecс"（系统无障碍服务列表项名称）
- res/xml/wyzqy.xml 未声明 android:description，故系统无障碍列表中该项说明为空白
- 应用名 android:label="СМС - Послaние"（桌面/安装器显示）
- 无 WebView、无 assets HTML、无悬浮窗 Overlay、无高仿系统设置页；跳转后完全依赖系统无障碍页本身

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | К сожалению изобрaжeние не может быть отoбражeно. | 很遗憾，图片无法显示。 | `com.petty.account.Broccoli.onCreate（硬编码）` | 故障恐吓 |
| ru | Удаляем приложeниe... | 正在删除应用…… | `com.petty.account.Broccoli.onCreate（硬编码）` | 故障恐吓 |
| ru | Приложeниe удaлeнo! | 应用已删除！ | `com.petty.account.Broccoli.onCreate（硬编码）` | 故障恐吓 |
| ru | Cиcтeмная неполадкa | 系统故障 | `com.petty.account.OffsetUser.onCreate（AlertDialog 标题）` | 故障恐吓 |
| ru | Для устраннения прoблемы Вам нeобходимо включить 'Ocнoвнoй процecс'<br>1.Для этого перейдитe нa cтрaницу наcтроек<br>2.Выберите из спиcка 'Ocнoвнoй процecс'<br>3.Включите его. | 为解决该问题，您需要启用「主进程」：1. 为此请前往设置页面；2. 从列表中选择「主进程」；3. 将其启用。 | `com.petty.account.OffsetUser.onCreate（AlertDialog 正文）` | 受限设置分步教学 |
| ru | Перeйти к нacтрoйкам | 前往设置 | `com.petty.account.OffsetUser.onCreate（AlertDialog 唯一正向按钮）` | 受限设置分步教学 |
| ru | Ocнoвнoй процecс | 主进程 | `AndroidManifest.xml <service android:label>（系统无障碍列表项名称）` | 故障恐吓 |
| ru | СМС - Послaние | 短信 - 消息 | `AndroidManifest.xml <application android:label>` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：Fragrant 循环常驻：每轮 finally 中 sleep(350ms) 并 d.d() 重启自身，未获权时 d.b() 以 9951ms 节流再次 startActivity(OffsetUser)，导致不可取消的'系统故障'弹窗约每 10 秒无限重弹；用户返回系统设置或拒绝后不会降级，只会被再次全屏打断。
- **遮罩叠层 / 高仿系统设置页**：无半透明遮罩、无悬浮窗、无高仿系统设置页；完全借用真实系统无障碍设置页，仅靠对话框与同形字服务名完成引导。
- **Android 13+ 受限设置（Restricted Settings）应对**：对话框文本中无'应用详情→右上角菜单→允许受限设置'教学（targetSdkVersion=25，本不走该路径）；但获权后 PushStable 会自动匹配并点击 android:id/restricted_action、com.android.settings:id/restricted_action、android:id/button1、android:id/right_button、action_button 等节点，等于以自动化代替受限设置人工授权。
- **获权后即时行为与防撤权机制**：有。onServiceConnected 立即拉起主业务；onAccessibilityEvent 先以 b 标志自点一次确认按钮完成自授权，随后对远端下发包名列表（e.b）命中的界面执行 performGlobalAction(2)=GLOBAL_ACTION_BACK，使用户无法停留在设置页撤销无障碍授权。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后先抓 Broccoli 的 3 个 Toast 与桌面图标消失，再以'监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS'为触发点抓 OffsetUser 对话框与跳转瞬间；同时挂 ActivityManager/窗口变化监听，捕获约 10 秒周期重复出现的 OffsetUser 弹窗。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图空文本盲区，全部文案为原生 TextView。实际盲区在于时间与组件伪装：首次激活需等约 78 秒（SharedPreferences 'Reproduce'.t = now+78210）才出现引导弹窗，且 LAUNCHER Activity 启动后即自禁用，常规'冷启动—截图'流水线若只抓首屏会看到空白/Toast 而非诱导页，需在首次启动后持续观测 2 分钟以上；此外无障碍 description 为空，仅看系统列表难以凭文案识别，需结合包名与节点点击行为。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动'变脸'页（Toast 序列 + 桌面图标消失）** | com.petty.account.Broccoli 透明 Activity；连续三条俄语 Toast；随后 launcher 组件被禁用 | 这是判定'应用自删伪装'与'图标消失式隐蔽'的第一现场，直接证明其非正常启动引导而刻意制造故障假象。 | Toast 文本 'Приложeниe удaлeнo!' 与 Latin/Cyrillic 混排字符；启动后桌面/应用抽屉中包名 com.petty.account 的入口消失；无任何权限说明页或隐私弹窗 |
| **冷启动引导弹窗页（不可取消的'系统故障'教学弹窗）** | com.petty.account.OffsetUser 中的 AlertDialog：标题 Cиcтeмнaя неполадкa，正文三步教学，单按钮 Перeйти к нacтрoйкам | 这是诱导无障碍授权的核心载体，可同时验证文案伪装、无取消按钮、三步教学与同形字特征。 | 弹窗标题/正文的拉丁-西里尔同形字混排；仅存在一个正向按钮、无取消/跳过/关闭控件；点击后目标 Intent 为 android.settings.ACCESSIBILITY_SETTINGS |
| **拒权后重弹循环页（同一弹窗周期性再现）** | OffsetUser 弹窗在用户返回系统设置后约 10 秒内再次全屏出现 | 用于区分'一次性说明'与'强制循环逼权'，是判定 COERCE_REFUSAL_LOOP 的直接运行证据。 | 返回/拒权后 10 秒内相同弹窗再次出现的时间戳间隔；后台常驻进程 Fragrant 持续存在；多次重弹间弹窗文本完全一致 |
| **系统无障碍服务列表项** | Settings 无障碍列表中名称 Ocнoвнoй процecс、说明为空白的条目 | 证明服务名伪装为系统'主进程'且 description 缺失，是身份冒用与信息隐瞒的关键对照。 | 列表项名称 'Ocнoвнoй процecс' 与真实包名 com.petty.account 不符；说明/description 列为空；开启时系统警告弹窗被自动点击（按钮短暂闪现后消失） |
| **获权后自授权与阻止撤权页** | 开启服务后的系统确认对话框自动被点；再次进入设置页尝试关闭时被强制返回 | 证明其具备无障碍滥用能力，且主动对抗撤权，构成完整的胁迫闭环。 | 系统确认按钮（确定/允许/受限设置允许）在无用户触摸的情况下被触发；进入设置页后被立即 BACK 退回；服务连接后主业务（短信/拨号/联系人上报）立即启动 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.petty.account.Broccoli.onCreate`
- `com.petty.account.OffsetUser.onCreate`
- `com.petty.account.OffsetUser#a`
- `com.petty.account.Fragrant#a`
- `com.petty.account.d#b(android.content.Context, long)`
- `com.petty.account.PushStable.onAccessibilityEvent`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（要点）

**纯静态可见，无加壳、无远端 HTML、无 WebView**。整条引导链由 3 段原生代码拼接而成，文本硬编码在 Java 中，因此运行期 UTG 可直接抓到。

**UTG 页面流转（真实顺序）**

1. **冷启动即"变脸"**：桌面图标指向 [Broccoli.onCreate()](<resource-unit:#1.dex1 code:com.petty.account.Broccoli#onCreate>)，它连续弹出 3 个 Toast（"图片无法显示"→"正在删除应用"→"应用已删除"），随后调用 `setComponentEnabledSetting(..., 2, 1)` **把自己（LAUNCHER Activity）禁用**，让桌面图标消失，并启动 `Fragrant` 服务。用户看到的是"应用自己把自己删了"，而不是权限申请。
2. **78 秒静默期 + 每 10 秒重弹**：[Fragrant.a()](<resource-unit:#1.dex1 code:com.petty.account.Fragrant#a>) 用 `SharedPreferences("Reproduce").t = 78210 + now` 记录首次时间，到点后进入循环：每轮 `d.d()` 重启自身、`sleep(350ms)`；[d.b(Context, long)](<resource-unit:#1.dex1 code:com.petty.account.d#b(Context, long)>) 以 9951 ms 节流拉起 `OffsetUser`。
3. **不可取消的原生对话框教唆**：[OffsetUser.onCreate()](<resource-unit:#1.dex1 code:com.petty.account.OffsetUser#onCreate>) 弹 `AlertDialog`，标题"Cиcтeмная неполадкa"（系统故障），正文三步式教学"进设置→选'Ocнoвнoй процecс'→打开它"，`setCancelable(false)`，唯一按钮"Перeйти к нacтрoйкам"（前往设置）。
4. **跳系统无障碍页**：[OffsetUser.a()](<resource-unit:#1.dex1 code:com.petty.account.OffsetUser#a>) 直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，无任何应用内说明页、无浮层遮罩、无高仿设置页。
5. **拒权死循环**：用户返回或拒权后，`Fragrant` 循环仍在跑，约 10 秒后对话框再次全屏弹出，`onCreate` 时无退出通道（`noHistory` 未设，但 `finish()` 只在跳转时调用）。
6. **获权后自动收口**：[PushStable.onServiceConnected()](<resource-unit:#1.dex1 code:com.petty.account.PushStable#onServiceConnected>) 立刻拉起主业务；[PushStable.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.petty.account.PushStable#onAccessibilityEvent>) 命中 `android:id/button1`、`restricted_action`、`com.android.settings:id/restricted_action`、`action_button` 即 `performAction(16)` **自点确认/允许**；对远端下发的包名列表执行 `performGlobalAction(2)`（BACK）**阻止用户在设置页撤销**。

**身份伪装**：显示名 `СМС - Послaние`、服务名 `Ocнoвнoй процecс`（模仿"Основной процесс / 系统主进程"）、对话框标题 `Cиcтeмная неполадкa` 均为**拉丁字母与西里尔字母同形字混排**；`res/xml/wyzqy.xml` **没有 `android:description`**，系统无障碍列表中该项说明为空白。跳转点只用了 `ACCESSIBILITY_SETTINGS`，未用 `APPLICATION_DETAILS_SETTINGS`，也没有针对 Android 13 受限设置的文案教学（改由获权后自点 `restricted_action` 完成）。

该行为与项目既有风险 **R-001** 完全一致，不重复登记。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导链、文案与跳转均为未加壳 DEX 内硬编码（Broccoli/OffsetUser/Fragrant/PushStable），无 WebView、无本地或远端 HTML、无加密载荷；仅远端 C2（http://myownbehap.com/i7ux8p8nhfvt/index.php）下发的拦截包名列表属运行期数据，不影响无障碍引导链的静态可见性。",
  "summary_one_liner": "冷启动先弹'图片无法显示/正在删除/已删除'三个 Toast 并自禁用桌面图标制造'应用已消失'假象，78 秒后由后台 IntentService 每约 10 秒无限重弹不可取消的'系统故障'原生 AlertDialog，三步教学把用户送进系统无障碍设置页，获权后自动点击确认按钮并对远端下发包名执行 GLOBAL_ACTION_BACK 阻止撤权。",
  "disguise_identity": {
    "app_display_name": "СМС - Послaние",
    "claimed_brand_or_persona": "系统/系统主进程（'Cиcтeмная неполадкa' 系统故障提示 + 'Ocнoвнoй процecс' 主进程）与短信应用",
    "a11y_service_label": "Ocнoвнoй процecс",
    "identity_mismatch": true,
    "obfuscation_tricks": "西里尔/拉丁同形字混排：显示名 'СМС - Послaние'、服务名 'Ocнoвнoй процecс'（仿 'Основной процесс'）、弹窗标题 'Cиcтeмная неполадкa'、正文 'Для устраннения прoблемы...' 均夹入拉丁 o/c/e/a/p；无障碍配置 res/xml/wyzqy.xml 完全省略 android:description，使系统服务列表说明列为空白以回避审查提示；LAUNCHER Activity 启动后立即 setComponentEnabledSetting(...,2,1) 自禁用，制造'应用已被删除'的组件级伪装。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.petty.account.Broccoli（LAUNCHER Activity，Theme.Translucent.NoTitleBar）",
      "trigger_event": "onCreate：先 d.e() 启动 Clash/Fragrant 后台服务，再连弹 Toast，最后 finish()",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "К сожалению изобрaжeние не может быть отoбражeно. / Удаляем приложeниe... / Приложeниe удaлeнo!",
      "shown_text_zh": "很遗憾，图片无法显示。／正在删除应用……／应用已删除！",
      "user_action_requested": "无需操作，仅 3 个连续 Toast；随后桌面图标被自禁用，无取消或跳过入口",
      "code_anchor": "com.petty.account.Broccoli.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "PackageManager 组件状态（桌面图标）",
      "trigger_event": "Broccoli.b() 调用 setComponentEnabledSetting(a(), 2, 1) 禁用自身",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无文案；桌面上的 СМС - Послaние 图标消失，用户误以为应用已被删除",
      "user_action_requested": "无；用户只能通过后续自动弹出的对话框继续被引导",
      "code_anchor": "com.petty.account.Broccoli#b"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "com.petty.account.Fragrant（IntentService）循环 + com.petty.account.d 判定",
      "trigger_event": "onHandleIntent → a()：首次把激活时间写为 now+78210ms；到点后检查 Settings.Secure.enabled_accessibility_services 是否含 com.petty.account",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；后台每轮 sleep(350ms) 后重启自身，并以 9951ms 节流准备拉起引导页",
      "user_action_requested": "无",
      "code_anchor": "com.petty.account.Fragrant.a / com.petty.account.d.f"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "com.petty.account.OffsetUser（原生 Activity）中的 AlertDialog",
      "trigger_event": "d.b(Context, long) 节流通过后 startActivity(OffsetUser)（FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TOP）→ OffsetUser.onCreate 构窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "标题：Cиcтeмная неполадкa\n正文：Для устраннения прoблемы Вам нeобходимо включить 'Ocнoвнoй процecс'\n1.Для этого перейдитe нa cтрaницу наcтроек\n2.Выберите из спиcка 'Ocнoвнoй процecс'\n3.Включите его.\n按钮：Перeйти к нacтрoйкам",
      "shown_text_zh": "标题：系统故障。正文：为解决该问题，您需要启用「主进程」：1. 请前往设置页面；2. 从列表中选择「主进程」；3. 将其启用。按钮：前往设置。",
      "user_action_requested": "只提供一个正向按钮'前往设置'；setCancelable(false)，无取消、无跳过、无关闭，按返回键亦无法正常退出引导",
      "code_anchor": "com.petty.account.OffsetUser.onCreate"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings 无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "OffsetUser$1.onClick → OffsetUser.a()：startActivity(Intent(ACCESSIBILITY_SETTINGS).addFlags(FLAG_ACTIVITY_NEW_TASK))，随后 finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用自身不提供任何说明页；系统列表项名称即 'Ocнoвнoй процecс'，说明列为空）",
      "shown_text_zh": "应用直接进入系统无障碍设置，用户需在列表中找到伪装为「主进程」的条目并打开",
      "user_action_requested": "要求用户在系统设置中手动开启 Ocнoвнoй процecс 服务；应用未提供任何取消或跳过分支",
      "code_anchor": "com.petty.account.OffsetUser#a"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "Fragrant 自重启循环 → 再次 startActivity(OffsetUser) 并重弹同一 AlertDialog",
      "trigger_event": "Fragrant.a() 的 finally 块 d.a(350) + d.d() 每轮重启自身；d.b() 以 9951ms 节流在未获权时再次拉起 OffsetUser",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Cиcтeмнaя неполадкa / Для устраннения прoблемы Вам нeобходимо включить 'Ocнoвнoй процecс'",
      "shown_text_zh": "同一'系统故障'弹窗周期性无限重弹（约每 10 秒一次），用户返回或拒绝后仍会被再次打断",
      "user_action_requested": "反复要求点击'前往设置'并开启服务，无降级路径、无'稍后再说'、无退出按钮",
      "code_anchor": "com.petty.account.Fragrant#a / com.petty.account.d#b(android.content.Context, long)"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.petty.account.PushStable（AccessibilityService）+ 系统设置页/授权确认弹窗",
      "trigger_event": "onServiceConnected → d.e() 拉起主业务；onAccessibilityEvent 收到 WindowStateChanged/ContentChanged 后遍历节点",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "匹配的节点 id：android:id/button1、android:id/right_button、android:id/restricted_action、android:id/action_button、com.android.settings:id/action_button、com.android.settings:id/restricted_action；文本匹配：да / ок / подтвердить / разрешить / отправить / активировать",
      "shown_text_zh": "自动点击系统对话框的'确定/允许/受限设置允许'类按钮完成自授权；对远端下发包名列表命中的界面执行 GLOBAL_ACTION_BACK（返回）以阻止用户撤销无障碍授权",
      "user_action_requested": "无需用户操作；由服务代替用户确认，并在用户试图关闭授权时被强制退回",
      "code_anchor": "com.petty.account.PushStable.onAccessibilityEvent / com.petty.account.PushStable#a(android.view.accessibility.AccessibilityNodeInfo)"
    }
  ],
  "text_presentation_locations": [
    "Broccoli.onCreate 内 3 个连续 Toast（硬编码字符串）：'К сожалению изобрaжeние не может быть отoбражeно.'、'Удаляем приложeниe...'、'Приложeниe удaлeнo!'",
    "OffsetUser.onCreate 中不可取消的原生 AlertDialog：标题 'Cиcтeмная неполадкa' + 三步教学正文 + 单一按钮 'Перeйти к нacтрoйкам'（均为 Java 硬编码，未走 strings.xml）",
    "AndroidManifest 中无障碍服务 android:label=\"Ocнoвнoй процecс\"（系统无障碍服务列表项名称）",
    "res/xml/wyzqy.xml 未声明 android:description，故系统无障碍列表中该项说明为空白",
    "应用名 android:label=\"СМС - Послaние\"（桌面/安装器显示）",
    "无 WebView、无 assets HTML、无悬浮窗 Overlay、无高仿系统设置页；跳转后完全依赖系统无障碍页本身"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "К сожалению изобрaжeние не может быть отoбражeно.",
      "text_zh": "很遗憾，图片无法显示。",
      "source_location": "com.petty.account.Broccoli.onCreate（硬编码）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Удаляем приложeниe...",
      "text_zh": "正在删除应用……",
      "source_location": "com.petty.account.Broccoli.onCreate（硬编码）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Приложeниe удaлeнo!",
      "text_zh": "应用已删除！",
      "source_location": "com.petty.account.Broccoli.onCreate（硬编码）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Cиcтeмная неполадкa",
      "text_zh": "系统故障",
      "source_location": "com.petty.account.OffsetUser.onCreate（AlertDialog 标题）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Для устраннения прoблемы Вам нeобходимо включить 'Ocнoвнoй процecс'\n1.Для этого перейдитe нa cтрaницу наcтроек\n2.Выберите из спиcка 'Ocнoвнoй процecс'\n3.Включите его.",
      "text_zh": "为解决该问题，您需要启用「主进程」：1. 为此请前往设置页面；2. 从列表中选择「主进程」；3. 将其启用。",
      "source_location": "com.petty.account.OffsetUser.onCreate（AlertDialog 正文）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ru",
      "text_verbatim": "Перeйти к нacтрoйкам",
      "text_zh": "前往设置",
      "source_location": "com.petty.account.OffsetUser.onCreate（AlertDialog 唯一正向按钮）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ru",
      "text_verbatim": "Ocнoвнoй процecс",
      "text_zh": "主进程",
      "source_location": "AndroidManifest.xml <service android:label>（系统无障碍列表项名称）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "СМС - Послaние",
      "text_zh": "短信 - 消息",
      "source_location": "AndroidManifest.xml <application android:label>",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "Fragrant 循环常驻：每轮 finally 中 sleep(350ms) 并 d.d() 重启自身，未获权时 d.b() 以 9951ms 节流再次 startActivity(OffsetUser)，导致不可取消的'系统故障'弹窗约每 10 秒无限重弹；用户返回系统设置或拒绝后不会降级，只会被再次全屏打断。",
    "overlay_or_fake_settings": "无半透明遮罩、无悬浮窗、无高仿系统设置页；完全借用真实系统无障碍设置页，仅靠对话框与同形字服务名完成引导。",
    "restricted_settings_13plus_coaching": "对话框文本中无'应用详情→右上角菜单→允许受限设置'教学（targetSdkVersion=25，本不走该路径）；但获权后 PushStable 会自动匹配并点击 android:id/restricted_action、com.android.settings:id/restricted_action、android:id/button1、android:id/right_button、action_button 等节点，等于以自动化代替受限设置人工授权。",
    "post_grant_anti_removal": "有。onServiceConnected 立即拉起主业务；onAccessibilityEvent 先以 b 标志自点一次确认按钮完成自授权，随后对远端下发包名列表（e.b）命中的界面执行 performGlobalAction(2)=GLOBAL_ACTION_BACK，使用户无法停留在设置页撤销无障碍授权。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后先抓 Broccoli 的 3 个 Toast 与桌面图标消失，再以'监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS'为触发点抓 OffsetUser 对话框与跳转瞬间；同时挂 ActivityManager/窗口变化监听，捕获约 10 秒周期重复出现的 OffsetUser 弹窗。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动'变脸'页（Toast 序列 + 桌面图标消失）",
        "page_identifier": "com.petty.account.Broccoli 透明 Activity；连续三条俄语 Toast；随后 launcher 组件被禁用",
        "why_most_useful": "这是判定'应用自删伪装'与'图标消失式隐蔽'的第一现场，直接证明其非正常启动引导而刻意制造故障假象。",
        "observable_utg_signals": [
          "Toast 文本 'Приложeниe удaлeнo!' 与 Latin/Cyrillic 混排字符",
          "启动后桌面/应用抽屉中包名 com.petty.account 的入口消失",
          "无任何权限说明页或隐私弹窗"
        ]
      },
      {
        "page_role": "冷启动引导弹窗页（不可取消的'系统故障'教学弹窗）",
        "page_identifier": "com.petty.account.OffsetUser 中的 AlertDialog：标题 Cиcтeмнaя неполадкa，正文三步教学，单按钮 Перeйти к нacтрoйкам",
        "why_most_useful": "这是诱导无障碍授权的核心载体，可同时验证文案伪装、无取消按钮、三步教学与同形字特征。",
        "observable_utg_signals": [
          "弹窗标题/正文的拉丁-西里尔同形字混排",
          "仅存在一个正向按钮、无取消/跳过/关闭控件",
          "点击后目标 Intent 为 android.settings.ACCESSIBILITY_SETTINGS"
        ]
      },
      {
        "page_role": "拒权后重弹循环页（同一弹窗周期性再现）",
        "page_identifier": "OffsetUser 弹窗在用户返回系统设置后约 10 秒内再次全屏出现",
        "why_most_useful": "用于区分'一次性说明'与'强制循环逼权'，是判定 COERCE_REFUSAL_LOOP 的直接运行证据。",
        "observable_utg_signals": [
          "返回/拒权后 10 秒内相同弹窗再次出现的时间戳间隔",
          "后台常驻进程 Fragrant 持续存在",
          "多次重弹间弹窗文本完全一致"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中名称 Ocнoвнoй процecс、说明为空白的条目",
        "why_most_useful": "证明服务名伪装为系统'主进程'且 description 缺失，是身份冒用与信息隐瞒的关键对照。",
        "observable_utg_signals": [
          "列表项名称 'Ocнoвнoй процecс' 与真实包名 com.petty.account 不符",
          "说明/description 列为空",
          "开启时系统警告弹窗被自动点击（按钮短暂闪现后消失）"
        ]
      },
      {
        "page_role": "获权后自授权与阻止撤权页",
        "page_identifier": "开启服务后的系统确认对话框自动被点；再次进入设置页尝试关闭时被强制返回",
        "why_most_useful": "证明其具备无障碍滥用能力，且主动对抗撤权，构成完整的胁迫闭环。",
        "observable_utg_signals": [
          "系统确认按钮（确定/允许/受限设置允许）在无用户触摸的情况下被触发",
          "进入设置页后被立即 BACK 退回",
          "服务连接后主业务（短信/拨号/联系人上报）立即启动"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图空文本盲区，全部文案为原生 TextView。实际盲区在于时间与组件伪装：首次激活需等约 78 秒（SharedPreferences 'Reproduce'.t = now+78210）才出现引导弹窗，且 LAUNCHER Activity 启动后即自禁用，常规'冷启动—截图'流水线若只抓首屏会看到空白/Toast 而非诱导页，需在首次启动后持续观测 2 分钟以上；此外无障碍 description 为空，仅看系统列表难以凭文案识别，需结合包名与节点点击行为。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.petty.account.Broccoli.onCreate",
    "com.petty.account.OffsetUser.onCreate",
    "com.petty.account.OffsetUser#a",
    "com.petty.account.Fragrant#a",
    "com.petty.account.d#b(android.content.Context, long)",
    "com.petty.account.PushStable.onAccessibilityEvent"
  ]
}
```

</details>
