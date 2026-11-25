# MR_017__df61a75b7c｜Asacub — Пoсланиe

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：77.4s

## 1. 一句话核心结论

- **核心申请方式**：伪装短信应用「Пoсланиe」首启即自禁用图标，随后以 9.7 秒节流的不可取消「系统故障」AlertDialog 给出三步教程，唯一按钮直达 ACCESSIBILITY_SETTINGS，引导用户手动开启同形字冒充「Cистемный прoцесс」的无障碍服务，无遮罩、无 WebView、无前置受限设置教学。
- **静态可见性说明**：引导链全部位于 classes.dex 明文代码与本地 XML 资源中：弹窗文案硬编码在 org.baseball.pie.CommonEscape#a，跳转点唯一且明文，无障碍配置为 res/xml/zvyfvfp.xml 明文，无加壳、无 DEX 加密、无 WebView/HTML 资源、无远端下发 UI。仅远端 http://whengoup.com/fjufyv6rc9kos8ragua4/index.php 的业务指令不可静态还原，与本引导流程无关。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `df61a75b7cfa128d4912e5cb648cfc504a8e7b25f6c83ed19194905fef8624c8` |
| 包名 / 年份 | `org.baseball.pie` / 2018 |
| 家族 / 品类 | **Asacub**（同池样本数：9） |
| 原始来源标识 | https://securelist.com/the-rise-of-mobile-banker-asacub/87591/ |
| 桌面显示名 | Пoсланиe |
| 引导页宣称品牌/身份 | 系统短信应用 + 无障碍服务冒充系统进程（Cистемный прoцесс） |
| 系统无障碍列表服务名 | Cистемный прoцесс |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：①同形字混排：全流程用拉丁 о/п/e/a/c/т 替换西里尔字母，形成 Пoсланиe、Cистемный прoцесс、Системная неполaдка、нeoбходимо、cтрaницу наcтроeк、Включитe、Пeрейти к наcтрoйкaм，规避 OCR 与字符串关键词识别；②无障碍服务 android:description 缺失，系统列表中不显示能力说明；③首启调用 setComponentEnabledSetting(Feature,2,1) 禁用自身 LAUNCHER 组件隐藏图标；④唯一引导 Activity CommonEscape 无 launcher、无别名，仅由后台 b.b 以 FLAG_ACTIVITY_NEW_TASK 拉起。 |
| 无障碍服务类名 | `org.baseball.pie.MakeIntroduction` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | org.baseball.pie.Feature（MAIN/LAUNCHER，android:noHistory=true） | onCreate 被系统启动器调用 | 原生Activity | 无 | 无交互，用户看不到任何页面，图标随即从桌面消失 | `org.baseball.pie.Feature#onCreate / org.baseball.pie.Feature#a` |
| 2 | 业务功能触发 | org.baseball.pie.b#a(Context,long) → b#b(Context,long) | 冷启动 b.f()、以及 Investment.onReceive(BOOT_COMPLETED/USER_PRESENT/PHONE_STATE)、FeverGround.onReceive(SMS_DELIVER/SMS_RECEIVED)、Addicted.onReceive(WAP_PUSH_DELIVER)、ExplosionBeg.onStartJob 均调用 b.f() | 不可静态还原（纯逻辑判定，无界面） | 无 | 无，弹窗由后台自动拉起，可跨应用覆盖当前界面 | `org.baseball.pie.b#a(Context,long) / org.baseball.pie.b#b(Context,long) / org.baseball.pie.b#h(Context)` |
| 3 | 引导说明页 | org.baseball.pie.CommonEscape（Theme.Translucent.NoTitleBar）内的原生 AlertDialog | CommonEscape.onCreate → a() | 原生Dialog | **原文**：标题：Системная неполaдка｜正文：Для устрaннения проблемы Вам нeoбходимо включить 'Cистемный прoцесс'\n1.Для этoго пeрeйдите на cтрaницу наcтроeк\n2.Выберите из cпиcка 'Cистемный прoцесс'\n3.Включитe егo.｜按钮：Пeрейти к наcтрoйкaм<br>**译注**：标题「系统故障」；正文「为排除该问题，您需要开启『系统进程』：1. 为此请前往设置页；2. 从列表中选择『系统进程』；3. 将其开启。」；唯一按钮「前往设置」 | 只能点击「前往设置」；setCancelable(false) 且无负向按钮，返回键/外部点击均无法关闭，用户仅能按 Home 离开 | `org.baseball.pie.CommonEscape#a` |
| 4 | 跳受限设置 | 系统页面 android.settings.ACCESSIBILITY_SETTINGS | 用户点击「前往设置」→ CommonEscape$1.onClick → CommonEscape.b() | 系统无障碍页 | **原文**：无（应用侧无自定义界面）<br>**译注**：以 new Intent("android.settings.ACCESSIBILITY_SETTINGS") + addFlags(268435456) 启动系统无障碍设置页，并立即 finish() 自身，用户回退时无法回到弹窗 | 用户须在系统设置页手动找到并打开「Cистемный прoцесс」开关；应用不提供任何引导遮罩或自动开启手段 | `org.baseball.pie.CommonEscape#b / org.baseball.pie.CommonEscape$1#onClick` |
| 5 | 遮罩叠层指引 | 系统无障碍服务列表项（org.baseball.pie.MakeIntroduction） | 用户进入无障碍设置页浏览服务列表 | 系统无障碍页 | **原文**：Cистемный прoцесс（无 description 描述行）<br>**译注**：列表中仅显示同形字伪造的服务名「系统进程」，因 res/xml/zvyfvfp.xml 未声明 android:description，系统不展示任何能力说明，用户无法得知该服务可读取全部窗口内容 | 用户手动点击开关开启服务 | `res/xml/zvyfvfp.xml / #1 manifest:components（service android:label）` |
| 6 | 拒权反馈循环 | org.baseball.pie.b#b(Context,long) 再次拉起 CommonEscape | 用户返回未开启无障碍，随后任一广播触发 b.f()（开机、解锁、来电、收短信、彩信、JobService） | 原生Dialog | **原文**：Системная неполaдка / Пeрейти к наcтрoйкaм（同步骤 3 文案重复出现）<br>**译注**：同一「系统故障」弹窗被反复重弹，节流为每次至少间隔 9709ms，无上限、无「不再提示」记忆位；用户离开设置页不会立即被重跳，但会在下一次系统事件时再次被弹窗拦截 | 再次只能点击「前往设置」 | `org.baseball.pie.b#b(Context,long) / org.baseball.pie.Investment#onReceive / org.baseball.pie.FeverGround#onReceive` |
| 7 | 获权后动作 | org.baseball.pie.MakeIntroduction（AccessibilityService）→ b.f() → Staff/MorselLawyer/ExplosionBeg | onServiceConnected() 回调；以及 b.a(String,String,PendingIntent) 发送短信前调用 MakeIntroduction.a(true) 置位静态标志 | 不可静态还原（后台服务，无界面） | **原文**：да / ок / подтвердить / разрешить / отправить / активировать<br>**译注**：获权后立即拉起常驻服务；在 onAccessibilityEvent 中当标志位置位时递归遍历节点，按 android:id/button1、right_button、restricted_action、action_button、com.android.settings:id/action_button、com.android.settings:id/restricted_action 以及「是/确定/确认/允许/发送/激活」等文本执行 performAction(16) 自动点击授权确认；对命中包执行 performGlobalAction(2) 强制 BACK | 无，全部为静默自动点击与静默退栈 | `org.baseball.pie.MakeIntroduction#onServiceConnected / org.baseball.pie.MakeIntroduction#a(AccessibilityNodeInfo) / org.baseball.pie.MakeIntroduction#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- CommonEscape 的原生 AlertDialog（setCancelable(false)）：标题「Системная неполaдка」+ 三步教程正文 + 唯一按钮「Пeрейти к наcтрoйкaм」，文案全部硬编码在 org.baseball.pie.CommonEscape#a，未使用 strings.xml
- AndroidManifest.xml 中 accessibility service 的 android:label="Cистемный прoцесс"，显示在系统设置 → 无障碍 → 已下载/可用服务列表项标题
- res/xml/zvyfvfp.xml 未声明 android:description，故系统无障碍列表项无副标题说明（信息缺失本身即伪装手段）
- 应用桌面名称 android:label="Пoсланиe"（Manifest application 节点），首启后该图标被禁用而不再可见
- 无 assets/*.html、无 WebView、无悬浮窗 Overlay、无高仿系统开关页、无通知栏引导文本

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Системная неполaдка | 系统故障 | `org.baseball.pie.CommonEscape#a（setTitle 硬编码）` | 故障恐吓 |
| ru | Для устрaннения проблемы Вам нeoбходимо включить 'Cистемный прoцесс'<br>1.Для этoго пeрeйдите на cтрaницу наcтроeк<br>2.Выберите из cпиcка 'Cистемный прoцесс'<br>3.Включитe егo. | 为排除该问题，您需要开启「系统进程」：1. 为此请前往设置页；2. 从列表中选择「系统进程」；3. 将其开启。 | `org.baseball.pie.CommonEscape#a（setMessage 硬编码）` | 受限设置分步教学 |
| ru | Пeрейти к наcтрoйкaм | 前往设置 | `org.baseball.pie.CommonEscape#a（setPositiveButton 硬编码）` | 故障恐吓 |
| ru | Cистемный прoцесс | 系统进程 | `AndroidManifest.xml accessibility service android:label` | 假反诈安全 |
| ru | Пoсланиe | 消息 | `AndroidManifest.xml application android:label` | 假更新 |
| ru | да / ок / подтвердить / разрешить / отправить / активировать | 是 / 确定 / 确认 / 允许 / 发送 / 激活 | `org.baseball.pie.MakeIntroduction 字段 a（自动点击授权文本白名单）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无 onResume/定时器死循环重跳；但 b.f() 被 BOOT_COMPLETED、USER_PRESENT、PHONE_STATE、SMS_DELIVER/SMS_RECEIVED、WAP_PUSH_DELIVER、JobService 及无障碍 onServiceConnected 共 7 处以上调用，每次经 j - a > 9709 节流后重新 startActivity(CommonEscape) 弹出同一个不可取消对话框，形成跨重启、跨应用场景的长期反复骚扰，直到 Settings.Secure.enabled_accessibility_services 中出现 org.baseball.pie 才停止（b#h 判定）。
- **遮罩叠层 / 高仿系统设置页**：无。既无半透明引导遮罩、无全屏悬浮窗、也无高仿系统无障碍开关页；跳转后完全交给系统设置页，应用不做任何视觉叠加。
- **Android 13+ 受限设置（Restricted Settings）应对**：无前置教学。应用 targetSdk 为 25（platformBuildVersionCode=27），未出现 ACTION_APPLICATION_DETAILS_SETTINGS、Session 安装器或「应用详情右上角允许受限设置」文案；仅在获权后由 MakeIntroduction 自动点击 android:id/restricted_action 与 com.android.settings:id/restricted_action 事后代劳。
- **获权后即时行为与防撤权机制**：有。onServiceConnected 立即调用 b.f() 拉起常驻 Staff/MorselLawyer/ExplosionBeg 并持 PowerManager 唤醒锁（tag=Husband）；onAccessibilityEvent 在静态标志位 b 置位时递归遍历窗口节点，按 button1/right_button/restricted_action/action_button/com.android.settings:id/action_button/com.android.settings:id/restricted_action 及「да/ок/подтвердить/разрешить/отправить/активировать」文本执行 performAction(16) 自动确认授权弹窗与受限设置；同时若事件包名命中本地列表则 performGlobalAction(2) 发送 BACK 强制退出该界面。
- **良性降级 / 替代方案**：无。未提供手动模式、ADB 引导、仅观看模式或任何「暂不开启」降级路径；用户唯一选项是前往设置或按 Home 离开（弹窗仍会再次出现）。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在首启 Feature.onCreate 之后立即拉起监测：Hook ActivityManager/Instrumentation 或轮询当前窗口，一旦出现 android.settings.ACCESSIBILITY_SETTINGS 或 Activity 栈顶为 org.baseball.pie.CommonEscape，即开始全量 UTG 抓取；由于弹窗为后台 startActivity(FLAG_ACTIVITY_NEW_TASK)，须允许捕获非用户主动触发的界面跳变。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图空文本盲区（文案全为可提取文本）。主要盲区在时序：弹窗由后台广播/服务以 9709ms 节流异步拉起，若 UTG 仅在用户主动操作后采样会漏采；另远端 http://whengoup.com/fjufyv6rc9kos8ragua4/index.php 下发的后续诈骗/短信窃取指令不可静态还原，运行期需结合流量分析。本样本静态未加壳，不构成运行期 UTG 阻碍。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | Activity org.baseball.pie.CommonEscape + 窗口 title「Системная неполaдка」/ 按钮「Пeрейти к наcтрoйкaм」，且 cancelable=false、无负向按钮 | 这是整条诱导链唯一的说明与决策节点，能直接证明「故障恐吓 + 三步教程 + 无跳过」的强迫式设计，也是同形字文本的唯一来源 | Dialog 节点 cancelable=false 且仅 1 个 clickable 按钮；标题与正文含拉丁-西里尔混排字符（可用 unicode script 混检命中）；正文包含「设置页 / 选择 / 开启」三步编号文本；窗口所属包名为 org.baseball.pie 但文本呈现为系统故障语义 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中 label 为「Cистемный прoцесс」的列表项，副标题/描述为空 | 验证伪装身份落地效果：服务名同形字冒充系统进程、且因缺 android:description 而不暴露 canRetrieveWindowContent 能力，是身份混淆的关键可观测证据 | 列表项文本「Cистемный прoцесс」与真实系统进程名高度相似但含拉丁字符；该项无 description 摘要行；开关状态为关闭（未获权）或开启（已获权） |
| **设置页后压栈遮罩页** | 预期不存在 overlay；若出现则应为 org.baseball.pie 的非透明/半透明窗口叠于 com.android.settings 之上 | 用于证伪：本样本未实现遮罩或高仿开关页，抓取该页为空可确认其诱导完全依赖原生弹窗与系统页，便于与其他家族样本区分 | 窗口栈顶包名仍为 com.android.settings（无第三方 overlay）；无悬浮窗类型窗口；无伪造的开关控件节点 |
| **获权后自动点击/退栈现场** | 任意授权类弹窗（含 restricted_action）被瞬时点击关闭；或命中包界面被 BACK 立即退出 | 证明服务开启后具备自动确认授权与强制退栈能力，是引导链的闭环终点 | 无障碍事件后弹窗在数百毫秒内消失且无用户触摸记录；系统设置页出现「允许受限设置」后被自动点击；目标应用界面在无输入情况下被弹出 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `org.baseball.pie.Feature#onCreate`
- `org.baseball.pie.b#b(android.content.Context, long)`
- `org.baseball.pie.CommonEscape#a`
- `org.baseball.pie.CommonEscape#b`
- `org.baseball.pie.MakeIntroduction#onAccessibilityEvent`
- `res/xml/zvyfvfp.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验：工具调用共 8 次，链路完全静态可见（无加壳、无 WebView、无 overlay、无远端 HTML）。

## 结论要点

- **入口**：`MAIN/LAUNCHER` 的 `Feature` 在 `onCreate` 里依次调用 `b.f()`（唤醒锁和常驻服务编排）、`b.a(ctx, now)`（节流弹窗判定）、`a()`（`setComponentEnabledSetting(...,2,1)` 自禁用启动图标）、`finish()`。**应用图标在首次启动后立即消失**，但引导弹窗已在后台被拉起。
- **弹窗载体**：`CommonEscape`（`Theme.Translucent.NoTitleBar`）+ 原生 `AlertDialog`，`setCancelable(false)`，**只有一个正向按钮**，没有“跳过/稍后”。
- **话术**：标题 `Системная неполaдка`（系统故障），正文以“排除故障”为框架给出**三步无障碍开启教程**，按钮 `Пeрейти к наcтрoйкaм`（前往设置）。关键元音被拉丁/西里尔同形字替换（`неполaдка`/`нeoбходимо`/`cтрaницу`/`наcтроeк`/`Включитe`），用于规避 OCR 与关键词扫描。
- **跳转**：`CommonEscape.b()` 是**全应用唯一的 `ACTION_ACCESSIBILITY_SETTINGS` 跳转点**（`FLAG_ACTIVITY_NEW_TASK`，跳完 `finish()`）；**不存在** `ACTION_APPLICATION_DETAILS_SETTINGS`、Session 安装器、受限设置前置教学、悬浮遮罩或高仿设置页。
- **系统侧呈现**：服务 `MakeIntroduction` 的 `android:label="Cистемный прoцесс"`（同形字伪造“系统进程”），`res/xml/zvyfvfp.xml` **无 `android:description`**，`canRetrieveWindowContent=true`，事件类型含 `typeWindowContentChanged|typeWindowStateChanged|typeWindowsChanged`。
- **拒权反馈**：无 `onResume` 死循环或紧耦合重跳；但 `b.f()` 被 `BOOT_COMPLETED`/`USER_PRESENT`/`PHONE_STATE`/`SMS_DELIVER`/`WAP_PUSH_DELIVER`/JobService/无障碍 `onServiceConnected` 共 7+ 处调用，经 `j - a > 9709` 节流后可**无限次重复弹窗**（每次 9.7 秒以上一次），形成骚扰式回拉而非硬阻断。
- **获权后**：`onServiceConnected` → `b.f()` 拉起 `Staff`/`MorselLawyer` 常驻；`onAccessibilityEvent` 在 `b==true` 时对当前窗口递归 `findAccessibilityNodeInfosByViewId` 点击 `restricted_action`/`com.android.settings:id/restricted_action`/`button1` 等（自点授权），并对命中包执行 `performGlobalAction(2)`（BACK 强制退出）。
- **证据边界**：远端 `http://whengoup.com/fjufyv6rc9kos8ragua4/index.php` 下发的指令内容不可静态还原，但**诱导授权链本身 100% 位于本地代码**，无加密/动态载荷。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链全部位于 classes.dex 明文代码与本地 XML 资源中：弹窗文案硬编码在 org.baseball.pie.CommonEscape#a，跳转点唯一且明文，无障碍配置为 res/xml/zvyfvfp.xml 明文，无加壳、无 DEX 加密、无 WebView/HTML 资源、无远端下发 UI。仅远端 http://whengoup.com/fjufyv6rc9kos8ragua4/index.php 的业务指令不可静态还原，与本引导流程无关。",
  "summary_one_liner": "伪装短信应用「Пoсланиe」首启即自禁用图标，随后以 9.7 秒节流的不可取消「系统故障」AlertDialog 给出三步教程，唯一按钮直达 ACCESSIBILITY_SETTINGS，引导用户手动开启同形字冒充「Cистемный прoцесс」的无障碍服务，无遮罩、无 WebView、无前置受限设置教学。",
  "disguise_identity": {
    "app_display_name": "Пoсланиe",
    "claimed_brand_or_persona": "系统短信应用 + 无障碍服务冒充系统进程（Cистемный прoцесс）",
    "a11y_service_label": "Cистемный прoцесс",
    "identity_mismatch": true,
    "obfuscation_tricks": "①同形字混排：全流程用拉丁 о/п/e/a/c/т 替换西里尔字母，形成 Пoсланиe、Cистемный прoцесс、Системная неполaдка、нeoбходимо、cтрaницу наcтроeк、Включитe、Пeрейти к наcтрoйкaм，规避 OCR 与字符串关键词识别；②无障碍服务 android:description 缺失，系统列表中不显示能力说明；③首启调用 setComponentEnabledSetting(Feature,2,1) 禁用自身 LAUNCHER 组件隐藏图标；④唯一引导 Activity CommonEscape 无 launcher、无别名，仅由后台 b.b 以 FLAG_ACTIVITY_NEW_TASK 拉起。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "org.baseball.pie.Feature（MAIN/LAUNCHER，android:noHistory=true）",
      "trigger_event": "onCreate 被系统启动器调用",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 无任何界面内容，仅执行逻辑：先 b.f(getApplicationContext()) 编排唤醒锁与常驻服务，再 b.a(ctx, 当前时间) 触发节流弹窗，最后 a() 禁用自身启动图标并 finish()",
      "user_action_requested": "无交互，用户看不到任何页面，图标随即从桌面消失",
      "code_anchor": "org.baseball.pie.Feature#onCreate / org.baseball.pie.Feature#a"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "org.baseball.pie.b#a(Context,long) → b#b(Context,long)",
      "trigger_event": "冷启动 b.f()、以及 Investment.onReceive(BOOT_COMPLETED/USER_PRESENT/PHONE_STATE)、FeverGround.onReceive(SMS_DELIVER/SMS_RECEIVED)、Addicted.onReceive(WAP_PUSH_DELIVER)、ExplosionBeg.onStartJob 均调用 b.f()",
      "ui_carrier": "不可静态还原（纯逻辑判定，无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "先用 Settings.Secure 读取 enabled_accessibility_services，若字符串包含 org.baseball.pie 说明已获权则直接返回不再弹窗；否则以 j - a > 9709 毫秒节流后 startActivity(CommonEscape)，标志位 0x70000000",
      "user_action_requested": "无，弹窗由后台自动拉起，可跨应用覆盖当前界面",
      "code_anchor": "org.baseball.pie.b#a(Context,long) / org.baseball.pie.b#b(Context,long) / org.baseball.pie.b#h(Context)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "org.baseball.pie.CommonEscape（Theme.Translucent.NoTitleBar）内的原生 AlertDialog",
      "trigger_event": "CommonEscape.onCreate → a()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "标题：Системная неполaдка｜正文：Для устрaннения проблемы Вам нeoбходимо включить 'Cистемный прoцесс'\\n1.Для этoго пeрeйдите на cтрaницу наcтроeк\\n2.Выберите из cпиcка 'Cистемный прoцесс'\\n3.Включитe егo.｜按钮：Пeрейти к наcтрoйкaм",
      "shown_text_zh": "标题「系统故障」；正文「为排除该问题，您需要开启『系统进程』：1. 为此请前往设置页；2. 从列表中选择『系统进程』；3. 将其开启。」；唯一按钮「前往设置」",
      "user_action_requested": "只能点击「前往设置」；setCancelable(false) 且无负向按钮，返回键/外部点击均无法关闭，用户仅能按 Home 离开",
      "code_anchor": "org.baseball.pie.CommonEscape#a"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统页面 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户点击「前往设置」→ CommonEscape$1.onClick → CommonEscape.b()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧无自定义界面）",
      "shown_text_zh": "以 new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + addFlags(268435456) 启动系统无障碍设置页，并立即 finish() 自身，用户回退时无法回到弹窗",
      "user_action_requested": "用户须在系统设置页手动找到并打开「Cистемный прoцесс」开关；应用不提供任何引导遮罩或自动开启手段",
      "code_anchor": "org.baseball.pie.CommonEscape#b / org.baseball.pie.CommonEscape$1#onClick"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍服务列表项（org.baseball.pie.MakeIntroduction）",
      "trigger_event": "用户进入无障碍设置页浏览服务列表",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Cистемный прoцесс（无 description 描述行）",
      "shown_text_zh": "列表中仅显示同形字伪造的服务名「系统进程」，因 res/xml/zvyfvfp.xml 未声明 android:description，系统不展示任何能力说明，用户无法得知该服务可读取全部窗口内容",
      "user_action_requested": "用户手动点击开关开启服务",
      "code_anchor": "res/xml/zvyfvfp.xml / #1 manifest:components（service android:label）"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "org.baseball.pie.b#b(Context,long) 再次拉起 CommonEscape",
      "trigger_event": "用户返回未开启无障碍，随后任一广播触发 b.f()（开机、解锁、来电、收短信、彩信、JobService）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Системная неполaдка / Пeрейти к наcтрoйкaм（同步骤 3 文案重复出现）",
      "shown_text_zh": "同一「系统故障」弹窗被反复重弹，节流为每次至少间隔 9709ms，无上限、无「不再提示」记忆位；用户离开设置页不会立即被重跳，但会在下一次系统事件时再次被弹窗拦截",
      "user_action_requested": "再次只能点击「前往设置」",
      "code_anchor": "org.baseball.pie.b#b(Context,long) / org.baseball.pie.Investment#onReceive / org.baseball.pie.FeverGround#onReceive"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "org.baseball.pie.MakeIntroduction（AccessibilityService）→ b.f() → Staff/MorselLawyer/ExplosionBeg",
      "trigger_event": "onServiceConnected() 回调；以及 b.a(String,String,PendingIntent) 发送短信前调用 MakeIntroduction.a(true) 置位静态标志",
      "ui_carrier": "不可静态还原（后台服务，无界面）",
      "shown_text_verbatim": "да / ок / подтвердить / разрешить / отправить / активировать",
      "shown_text_zh": "获权后立即拉起常驻服务；在 onAccessibilityEvent 中当标志位置位时递归遍历节点，按 android:id/button1、right_button、restricted_action、action_button、com.android.settings:id/action_button、com.android.settings:id/restricted_action 以及「是/确定/确认/允许/发送/激活」等文本执行 performAction(16) 自动点击授权确认；对命中包执行 performGlobalAction(2) 强制 BACK",
      "user_action_requested": "无，全部为静默自动点击与静默退栈",
      "code_anchor": "org.baseball.pie.MakeIntroduction#onServiceConnected / org.baseball.pie.MakeIntroduction#a(AccessibilityNodeInfo) / org.baseball.pie.MakeIntroduction#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "CommonEscape 的原生 AlertDialog（setCancelable(false)）：标题「Системная неполaдка」+ 三步教程正文 + 唯一按钮「Пeрейти к наcтрoйкaм」，文案全部硬编码在 org.baseball.pie.CommonEscape#a，未使用 strings.xml",
    "AndroidManifest.xml 中 accessibility service 的 android:label=\"Cистемный прoцесс\"，显示在系统设置 → 无障碍 → 已下载/可用服务列表项标题",
    "res/xml/zvyfvfp.xml 未声明 android:description，故系统无障碍列表项无副标题说明（信息缺失本身即伪装手段）",
    "应用桌面名称 android:label=\"Пoсланиe\"（Manifest application 节点），首启后该图标被禁用而不再可见",
    "无 assets/*.html、无 WebView、无悬浮窗 Overlay、无高仿系统开关页、无通知栏引导文本"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Системная неполaдка",
      "text_zh": "系统故障",
      "source_location": "org.baseball.pie.CommonEscape#a（setTitle 硬编码）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Для устрaннения проблемы Вам нeoбходимо включить 'Cистемный прoцесс'\n1.Для этoго пeрeйдите на cтрaницу наcтроeк\n2.Выберите из cпиcка 'Cистемный прoцесс'\n3.Включитe егo.",
      "text_zh": "为排除该问题，您需要开启「系统进程」：1. 为此请前往设置页；2. 从列表中选择「系统进程」；3. 将其开启。",
      "source_location": "org.baseball.pie.CommonEscape#a（setMessage 硬编码）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ru",
      "text_verbatim": "Пeрейти к наcтрoйкaм",
      "text_zh": "前往设置",
      "source_location": "org.baseball.pie.CommonEscape#a（setPositiveButton 硬编码）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Cистемный прoцесс",
      "text_zh": "系统进程",
      "source_location": "AndroidManifest.xml accessibility service android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "ru",
      "text_verbatim": "Пoсланиe",
      "text_zh": "消息",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": "да / ок / подтвердить / разрешить / отправить / активировать",
      "text_zh": "是 / 确定 / 确认 / 允许 / 发送 / 激活",
      "source_location": "org.baseball.pie.MakeIntroduction 字段 a（自动点击授权文本白名单）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无 onResume/定时器死循环重跳；但 b.f() 被 BOOT_COMPLETED、USER_PRESENT、PHONE_STATE、SMS_DELIVER/SMS_RECEIVED、WAP_PUSH_DELIVER、JobService 及无障碍 onServiceConnected 共 7 处以上调用，每次经 j - a > 9709 节流后重新 startActivity(CommonEscape) 弹出同一个不可取消对话框，形成跨重启、跨应用场景的长期反复骚扰，直到 Settings.Secure.enabled_accessibility_services 中出现 org.baseball.pie 才停止（b#h 判定）。",
    "overlay_or_fake_settings": "无。既无半透明引导遮罩、无全屏悬浮窗、也无高仿系统无障碍开关页；跳转后完全交给系统设置页，应用不做任何视觉叠加。",
    "restricted_settings_13plus_coaching": "无前置教学。应用 targetSdk 为 25（platformBuildVersionCode=27），未出现 ACTION_APPLICATION_DETAILS_SETTINGS、Session 安装器或「应用详情右上角允许受限设置」文案；仅在获权后由 MakeIntroduction 自动点击 android:id/restricted_action 与 com.android.settings:id/restricted_action 事后代劳。",
    "post_grant_anti_removal": "有。onServiceConnected 立即调用 b.f() 拉起常驻 Staff/MorselLawyer/ExplosionBeg 并持 PowerManager 唤醒锁（tag=Husband）；onAccessibilityEvent 在静态标志位 b 置位时递归遍历窗口节点，按 button1/right_button/restricted_action/action_button/com.android.settings:id/action_button/com.android.settings:id/restricted_action 及「да/ок/подтвердить/разрешить/отправить/активировать」文本执行 performAction(16) 自动确认授权弹窗与受限设置；同时若事件包名命中本地列表则 performGlobalAction(2) 发送 BACK 强制退出该界面。",
    "benign_graceful_degradation": "无。未提供手动模式、ADB 引导、仅观看模式或任何「暂不开启」降级路径；用户唯一选项是前往设置或按 Home 离开（弹窗仍会再次出现）。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在首启 Feature.onCreate 之后立即拉起监测：Hook ActivityManager/Instrumentation 或轮询当前窗口，一旦出现 android.settings.ACCESSIBILITY_SETTINGS 或 Activity 栈顶为 org.baseball.pie.CommonEscape，即开始全量 UTG 抓取；由于弹窗为后台 startActivity(FLAG_ACTIVITY_NEW_TASK)，须允许捕获非用户主动触发的界面跳变。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "Activity org.baseball.pie.CommonEscape + 窗口 title「Системная неполaдка」/ 按钮「Пeрейти к наcтрoйкaм」，且 cancelable=false、无负向按钮",
        "why_most_useful": "这是整条诱导链唯一的说明与决策节点，能直接证明「故障恐吓 + 三步教程 + 无跳过」的强迫式设计，也是同形字文本的唯一来源",
        "observable_utg_signals": ["Dialog 节点 cancelable=false 且仅 1 个 clickable 按钮", "标题与正文含拉丁-西里尔混排字符（可用 unicode script 混检命中）", "正文包含「设置页 / 选择 / 开启」三步编号文本", "窗口所属包名为 org.baseball.pie 但文本呈现为系统故障语义"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中 label 为「Cистемный прoцесс」的列表项，副标题/描述为空",
        "why_most_useful": "验证伪装身份落地效果：服务名同形字冒充系统进程、且因缺 android:description 而不暴露 canRetrieveWindowContent 能力，是身份混淆的关键可观测证据",
        "observable_utg_signals": ["列表项文本「Cистемный прoцесс」与真实系统进程名高度相似但含拉丁字符", "该项无 description 摘要行", "开关状态为关闭（未获权）或开启（已获权）"]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "预期不存在 overlay；若出现则应为 org.baseball.pie 的非透明/半透明窗口叠于 com.android.settings 之上",
        "why_most_useful": "用于证伪：本样本未实现遮罩或高仿开关页，抓取该页为空可确认其诱导完全依赖原生弹窗与系统页，便于与其他家族样本区分",
        "observable_utg_signals": ["窗口栈顶包名仍为 com.android.settings（无第三方 overlay）", "无悬浮窗类型窗口", "无伪造的开关控件节点"]
      },
      {
        "page_role": "获权后自动点击/退栈现场",
        "page_identifier": "任意授权类弹窗（含 restricted_action）被瞬时点击关闭；或命中包界面被 BACK 立即退出",
        "why_most_useful": "证明服务开启后具备自动确认授权与强制退栈能力，是引导链的闭环终点",
        "observable_utg_signals": ["无障碍事件后弹窗在数百毫秒内消失且无用户触摸记录", "系统设置页出现「允许受限设置」后被自动点击", "目标应用界面在无输入情况下被弹出"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图空文本盲区（文案全为可提取文本）。主要盲区在时序：弹窗由后台广播/服务以 9709ms 节流异步拉起，若 UTG 仅在用户主动操作后采样会漏采；另远端 http://whengoup.com/fjufyv6rc9kos8ragua4/index.php 下发的后续诈骗/短信窃取指令不可静态还原，运行期需结合流量分析。本样本静态未加壳，不构成运行期 UTG 阻碍。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "org.baseball.pie.Feature#onCreate",
    "org.baseball.pie.b#b(android.content.Context, long)",
    "org.baseball.pie.CommonEscape#a",
    "org.baseball.pie.CommonEscape#b",
    "org.baseball.pie.MakeIntroduction#onAccessibilityEvent",
    "res/xml/zvyfvfp.xml"
  ]
}
```

</details>
