# MR_073__364a50a23c｜Ztorg — Money Converter

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：89.6s

## 1. 一句话核心结论

- **核心申请方式**：该货币转换器以开机/充电/亮屏/解锁等广播为触发，直接跳转系统无障碍设置页并叠压一个白底白字的全屏透明引导页，用『请开启无障碍以防止隐私被窃取』的话术把用户引到系统无障碍开关上，且无跳过按钮、每次广播都会重复拉起。
- **静态可见性说明**：无障碍引导全链路（广播触发 → 跳系统无障碍设置 → 透明引导页叠层 → 服务生效）均可在 classes.dex 与 res/values/strings.xml、res/xml/email_config.xml 中静态完整还原；未见加壳、未见远端 HTML 或加密载荷参与该引导流程，故无关键环节隐藏。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `364a50a23c2b11cd2007d7ee079fce5899c47f3c511b70933e0893cf2bcd21fc` |
| 包名 / 年份 | `com.countrys.converter.currency` / 2017 |
| 家族 / 品类 | **Ztorg**（同池样本数：5） |
| 原始来源标识 | https://securelist.com/ztorg-from-rooting-to-sms/78775/ |
| 桌面显示名 | Money Converter |
| 引导页宣称品牌/身份 | 以『隐私保护 / 防窃听防窃取』为名的安全防护者身份（Acccessibility Privacy protection），实为货币转换器外壳 |
| 系统无障碍列表服务名 | Acccessibility Privacy protection |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务标签『Acccessibility』为故意/拼写错误形态，与系统原生『Accessibility』仅差一个字母，易被用户当作系统项；引导页采用 Theme.Translucent.NoTitleBar + excludeFromRecents，无标题栏、不进最近任务，覆盖在系统无障碍设置页之上，使引导文字与系统开关同屏呈现；引导 Activity 另以 android.intent.action.MAIN + DEFAULT 过滤器导出，可由外部直接拉起。 |
| 无障碍服务类名 | `demo.LUAccessService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Please open the Acccessibility on, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | demo.OpenAccessReceiver（BroadcastReceiver） | 收到 ACTION_BOOT_COMPLETED / ACTION_POWER_CONNECTED / USER_PRESENT / SCREEN_ON / SCREEN_OFF / CONNECTIVITY_CHANGE / PACKAGE_ADDED / PACKAGE_REMOVED / DELETE 广播 | 不可静态还原 | 无 | 无（无需用户操作，开机或插电即触发） | `demo.OpenAccessReceiver.onReceive` |
| 2 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | onReceive 中 g.b(context)==false 且 m.a(context)==false（即无障碍服务未启用）→ 调用 o.c(context) | 系统无障碍页 | 无 | 要求用户在列表中点选并开启名为『Acccessibility Privacy protection』的服务 | `com.b.a.a.o.c` |
| 3 | 遮罩叠层指引 | demo.UponGuideActivity（Theme.Translucent.NoTitleBar，excludeFromRecents，FLAG_ACTIVITY_NEW_TASK 压栈） | o.c() 中紧随无障碍设置 Intent 之后立即 startActivity(UponGuideActivity) | 悬浮窗Overlay | **原文**：Please open the Acccessibility on, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.<br>**译注**：请开启无障碍（Acccessibility）开关，保护您的信息不被泄露、不被窃取，防止他人窥探您的隐私。 | 仅有『点击任意处关闭遮罩』一种交互（onClick → finish），无『取消/跳过/暂不』按钮；遮罩关闭后露出下方系统无障碍开关 | `demo.UponGuideActivity.onCreate / demo.UponGuideActivity$1.onClick / res/values/strings.xml#acc_tips` |
| 4 | 拒权反馈循环 | 下一次广播 / UCService 启动时的 o.c(context) 重放 | 每次 SCREEN_ON、ACTION_POWER_CONNECTED、USER_PRESENT、PACKAGE_ADDED 等广播到达，或 demo.UCService.onCreate/onStartCommand 执行 n.a(intent,…) 时，只要 m.a(context) 仍为 false 就再次跳设置并压遮罩 | 系统无障碍页 | **原文**：Please open the Acccessibility on, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.<br>**译注**：同一段隐私话术反复弹出，直到用户开启无障碍为止 | 无退出机制：返回键/关闭遮罩只结束本次引导，下一次亮屏或插电仍会重来 | `com.b.a.a.n.a(Intent,int,int) / demo.UCService.onCreate` |
| 5 | 获权后动作 | demo.LUAccessService → com.b.a.a.m（typeAllMask 监听 + flagReportViewIds） | 服务开启后 onAccessibilityEvent；仅当 k.b(s,"run",false) 为真且事件包名为 com.mobpower.a.g.g.a 时进入 m.b(event) | 不可静态还原 | **原文**：无（自动点击词表：ACCEPT/INSTALL/PROCEED、ACEPTAR/INSTALAR/CONTINUAR、ПРИНЯТЬ/УСТАНОВИТЬ/ПРОДОЛЖИТЬ 等）<br>**译注**：自动识别并点击广告落地页/安装器上的『接受』『安装』『继续』按钮 | 无（静默代为点击），随后 performGlobalAction(GLOBAL_ACTION_BACK) 关闭页面并广播 ACTION_CLOSE_VIEW | `demo.LUAccessService.onAccessibilityEvent / com.b.a.a.m.b(AccessibilityEvent) / com.b.a.a.m.a()` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项名称：android:label=@string/acc_title → 『Acccessibility Privacy protection』
- 系统无障碍列表项说明：res/xml/email_config.xml android:description=@string/acc_desc → 与 acc_tips 完全相同的隐私话术
- 跳转无障碍设置后立即压栈的透明全屏引导页 demo.UponGuideActivity：单个全屏 TextView，白底白字居中显示 @string/acc_tips，点击任意处关闭
- 每次广播/服务启动重放的同一引导页（无倒计时、无跳过按钮、无取消入口）
- 应用内另有 @string/accessibility_desc / accessibility_string = 『Accessibility Services』，用于设置页文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please open the Acccessibility on, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy. | 请开启无障碍（Acccessibility）开关，保护您的信息不被泄露、不被窃取，防止他人窥探您的隐私。 | `res/values/strings.xml key=acc_tips（同文复用于 acc_desc）` | 假反诈安全 |
| en | Acccessibility Privacy protection | 无障碍 隐私保护 | `res/values/strings.xml key=acc_title（Manifest service android:label）` | 隐私承诺 |
| en | Accessibility Services | 无障碍服务 | `res/values/strings.xml key=accessibility_desc / accessibility_string` | 良性透明说明 |
| en | Allow Ad to create a calendar event? | 允许广告创建日历事件？ | `res/values/strings.xml key=create_calendar_message` | 未知 |
| en | Allow Ad to store image in Picture gallery? | 允许广告将图片存入相册？ | `res/values/strings.xml（广告 SDK 权限提示）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无 onResume 轮询死循环，改为广播驱动的反复拉起：只要 m.a(context)（Settings.Secure.enabled_accessibility_services 中不含『包名/demo.LUAccessService』）为 false，每次 BOOT_COMPLETED、ACTION_POWER_CONNECTED、USER_PRESENT、SCREEN_ON、PACKAGE_ADDED/REMOVED 等广播，以及 demo.UCService.onCreate/onStartCommand 执行时，都会重新执行 o.c(context) 跳转无障碍设置并压上引导遮罩；用户按返回或点击遮罩关闭仅结束当次引导。
- **遮罩叠层 / 高仿系统设置页**：使用 Theme.Translucent.NoTitleBar 的全屏透明 Activity（demo.UponGuideActivity，excludeFromRecents）压栈在真实系统无障碍设置页之上，形成白底白字引导文字与系统无障碍开关同屏的叠层效果；不是自绘的高仿设置页，开关仍为系统原生控件。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：获权后 com.b.a.a.m.b() 在命中『下载中/正在下载』等词表节点时调用 performGlobalAction(1)（GLOBAL_ACTION_BACK）关闭当前页面并广播 ACTION_CLOSE_VIEW，用于自动关闭安装器/落地页而非阻止用户撤权；未见监听设置页阻止关闭无障碍开关的逻辑。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以广播触发为主：在设备上执行 adb shell am broadcast -a android.intent.action.ACTION_POWER_CONNECTED（或 SCREEN_ON/USER_PRESENT），或直接 adb shell am start -n com.countrys.converter.currency/demo.UponGuideActivity；UTG 应在监测到 Activity 栈顶出现 android.settings.ACCESSIBILITY_SETTINGS 后 500ms 内的下一次栈顶变化时立刻抓取（此时 UponGuideActivity 已压栈）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导全为纯文本节点，无图片诱饵，UTG 文本可直取。需注意两点：一是引导页为白底白字（背景 0x7FFFFFFF + 文字 -1），若 UTG 仅做对比度渲染采样可能漏看文字，应以控件树 text 属性为准；二是获权后的自动点击阶段发生在 com.mobpower.a.g.g.a 广告落地页，需先置 SharedPreferences 键『run』为 true 才会触发，纯 UTG 在该阶段前观察不到行为。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转后叠压的系统无障碍设置页 + 透明引导页合成画面** | Activity 栈顶为 demo.UponGuideActivity（Theme.Translucent.NoTitleBar），下层为 com.android.settings 无障碍列表 | 这是诱导的核心瞬间：透明引导文字直接覆盖在系统无障碍开关上方，可证明『系统设置页 + 自定义话术叠层』的引导手法 | Activity 栈顶 demo.UponGuideActivity 与下层 com.android.settings/.Settings$AccessibilitySettings 同时存在；全屏 TextView 文本含『Please open the Acccessibility on』；无可见的取消/跳过按钮节点 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务列表，条目文本『Acccessibility Privacy protection』及副标题隐私话术 | 证明服务名与说明文案的伪装身份，以及与『Money Converter』货币转换器功能完全无关 | 列表项 label 文本『Acccessibility Privacy protection』（含三 c 拼写）；description 文本与引导页文案完全一致；应用包名 com.countrys.converter.currency |
| **重复拉起验证页（拒权反馈）** | 返回后再次触发 SCREEN_ON/POWER_CONNECTED 广播，栈顶重新出现 ACCESSIBILITY_SETTINGS + UponGuideActivity | 证明拒权后无降级路径、由广播驱动无限重试 | 同一 Activity 组合在 30 秒内重复出现；两次拉起之间无任何用户可点的退出路径 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.b.a.a.o.c`
- `demo.OpenAccessReceiver.onReceive`
- `demo.UponGuideActivity.onCreate`
- `demo.UponGuideActivity$1.onClick`
- `com.b.a.a.m.a(Context)`
- `res/values/strings.xml#acc_tips / acc_desc / acc_title；res/xml/email_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验，共 12 次有效定位（超出建议上限，已立即收口，未再展开）。结论基于静态代码，无需动态验证即可闭合。

## 核心结论

1. **触发不依赖用户主动操作**：[demo.OpenAccessReceiver](<resource-unit:#1.dex1 code:demo.OpenAccessReceiver#onReceive>) 注册了 `BOOT_COMPLETED`、`ACTION_POWER_CONNECTED`、`USER_PRESENT`、`SCREEN_ON/OFF`、`CONNECTIVITY_CHANGE`、`PACKAGE_ADDED/REMOVED` 等广播（见 [components](<resource-unit:#1 manifest:components>)）。在收到广播后，只要无障碍服务尚未启用，它就调用 `o.c(context)` 直接启动系统无障碍设置页。
2. **跳转 + 叠层两步连贯完成**：[com.b.a.a.o#c](<resource-unit:#1.dex1 code:com.b.a.a.o#c>) 先以 `FLAG_ACTIVITY_NEW_TASK` 启动 `android.settings.ACCESSIBILITY_SETTINGS`，紧接着启动 `demo.UponGuideActivity`（`Theme.Translucent.NoTitleBar`、`excludeFromRecents`），形成"系统无障碍列表 + 全屏半透明引导文字"的叠层画面。
3. **引导文字只有一段"防隐私泄露"话术**：[UponGuideActivity.onCreate](<resource-unit:#1.dex1 code:demo.UponGuideActivity#onCreate>) 创建单个占满全屏的 `TextView`，内容取自 `acc_tips`（与 `acc_desc` 完全同文），白底白字、居中；点击任意位置只执行 `finish()`（[UponGuideActivity$1#onClick](<resource-unit:#1.dex1 code:demo.UponGuideActivity$1#onClick>)），无"拒绝/跳过"按钮，但点屏即可关闭遮罩——遮罩撤掉后下方正是已开启的系统无障碍开关页。
4. **无设置页轮询死循环，但存在广播驱动的重复拉起**：[UponGuideActivity](<resource-unit:#1.dex1 code:demo.UponGuideActivity#onCreate>) 无 `onResume` 重跳；重复引导来自 `OpenAccessReceiver` 的每次广播，以及 `UCService.onCreate/onStartCommand → n.a(intent,…)` 中再次执行的 `if (!m.a(u)) o.c(u)`，即每次亮屏、充电、解锁、安装包变化都会重走"跳设置 + 压遮罩"。
5. **判定开关来自本地偏好与系统设置双重读取**：[com.b.a.a.m#a(Context)](<resource-unit:#1.dex1 code:com.b.a.a.m#a>) 通过 `Settings.Secure.accessibility_enabled` 与 `enabled_accessibility_services` 精确比对 `包名/demo.LUAccessService`；`g.b()` 另受 `NRate_s_State` 偏好门控。
6. **服务名的欺骗性**：系统列表标签为 `Acccessibility Privacy protection`（`acc_title`，且 "Acccessibility" 本身是拼写错误），说明文字承诺"防止隐私被窃取"；而服务实际配置为 `typeAllMask` + `canRetrieveWindowContent` + `flagReportViewIds`（[email_config.xml](<resource-unit:#1 file:res/xml/email_config.xml#L1-L3>)），获权后仅在 `run` 标志为真时针对 `com.mobpower.a.g.g.a` 窗口按 `ACCEPT/INSTALL/INSTALAR` 等多语言词表自动点击，并用 `performGlobalAction(GLOBAL_ACTION_BACK)` 关闭页面——与本条已登记风险 [R-001] 完全一致，本轮不再重复登记。

可见性：`clear`，全部为本地 DEX 与本地 strings 资源，无加壳、无远端 HTML。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（广播触发 → 跳系统无障碍设置 → 透明引导页叠层 → 服务生效）均可在 classes.dex 与 res/values/strings.xml、res/xml/email_config.xml 中静态完整还原；未见加壳、未见远端 HTML 或加密载荷参与该引导流程，故无关键环节隐藏。",
  "summary_one_liner": "该货币转换器以开机/充电/亮屏/解锁等广播为触发，直接跳转系统无障碍设置页并叠压一个白底白字的全屏透明引导页，用『请开启无障碍以防止隐私被窃取』的话术把用户引到系统无障碍开关上，且无跳过按钮、每次广播都会重复拉起。",
  "disguise_identity": {
    "app_display_name": "Money Converter",
    "claimed_brand_or_persona": "以『隐私保护 / 防窃听防窃取』为名的安全防护者身份（Acccessibility Privacy protection），实为货币转换器外壳",
    "a11y_service_label": "Acccessibility Privacy protection",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务标签『Acccessibility』为故意/拼写错误形态，与系统原生『Accessibility』仅差一个字母，易被用户当作系统项；引导页采用 Theme.Translucent.NoTitleBar + excludeFromRecents，无标题栏、不进最近任务，覆盖在系统无障碍设置页之上，使引导文字与系统开关同屏呈现；引导 Activity 另以 android.intent.action.MAIN + DEFAULT 过滤器导出，可由外部直接拉起。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "demo.OpenAccessReceiver（BroadcastReceiver）",
      "trigger_event": "收到 ACTION_BOOT_COMPLETED / ACTION_POWER_CONNECTED / USER_PRESENT / SCREEN_ON / SCREEN_OFF / CONNECTIVITY_CHANGE / PACKAGE_ADDED / PACKAGE_REMOVED / DELETE 广播",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，纯后台判定",
      "user_action_requested": "无（无需用户操作，开机或插电即触发）",
      "code_anchor": "demo.OpenAccessReceiver.onReceive"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "onReceive 中 g.b(context)==false 且 m.a(context)==false（即无障碍服务未启用）→ 调用 o.c(context)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍设置页（含已安装无障碍服务列表）",
      "user_action_requested": "要求用户在列表中点选并开启名为『Acccessibility Privacy protection』的服务",
      "code_anchor": "com.b.a.a.o.c"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "demo.UponGuideActivity（Theme.Translucent.NoTitleBar，excludeFromRecents，FLAG_ACTIVITY_NEW_TASK 压栈）",
      "trigger_event": "o.c() 中紧随无障碍设置 Intent 之后立即 startActivity(UponGuideActivity)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Please open the Acccessibility on, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.",
      "shown_text_zh": "请开启无障碍（Acccessibility）开关，保护您的信息不被泄露、不被窃取，防止他人窥探您的隐私。",
      "user_action_requested": "仅有『点击任意处关闭遮罩』一种交互（onClick → finish），无『取消/跳过/暂不』按钮；遮罩关闭后露出下方系统无障碍开关",
      "code_anchor": "demo.UponGuideActivity.onCreate / demo.UponGuideActivity$1.onClick / res/values/strings.xml#acc_tips"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "下一次广播 / UCService 启动时的 o.c(context) 重放",
      "trigger_event": "每次 SCREEN_ON、ACTION_POWER_CONNECTED、USER_PRESENT、PACKAGE_ADDED 等广播到达，或 demo.UCService.onCreate/onStartCommand 执行 n.a(intent,…) 时，只要 m.a(context) 仍为 false 就再次跳设置并压遮罩",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please open the Acccessibility on, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.",
      "shown_text_zh": "同一段隐私话术反复弹出，直到用户开启无障碍为止",
      "user_action_requested": "无退出机制：返回键/关闭遮罩只结束本次引导，下一次亮屏或插电仍会重来",
      "code_anchor": "com.b.a.a.n.a(Intent,int,int) / demo.UCService.onCreate"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "demo.LUAccessService → com.b.a.a.m（typeAllMask 监听 + flagReportViewIds）",
      "trigger_event": "服务开启后 onAccessibilityEvent；仅当 k.b(s,\"run\",false) 为真且事件包名为 com.mobpower.a.g.g.a 时进入 m.b(event)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（自动点击词表：ACCEPT/INSTALL/PROCEED、ACEPTAR/INSTALAR/CONTINUAR、ПРИНЯТЬ/УСТАНОВИТЬ/ПРОДОЛЖИТЬ 等）",
      "shown_text_zh": "自动识别并点击广告落地页/安装器上的『接受』『安装』『继续』按钮",
      "user_action_requested": "无（静默代为点击），随后 performGlobalAction(GLOBAL_ACTION_BACK) 关闭页面并广播 ACTION_CLOSE_VIEW",
      "code_anchor": "demo.LUAccessService.onAccessibilityEvent / com.b.a.a.m.b(AccessibilityEvent) / com.b.a.a.m.a()"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项名称：android:label=@string/acc_title → 『Acccessibility Privacy protection』",
    "系统无障碍列表项说明：res/xml/email_config.xml android:description=@string/acc_desc → 与 acc_tips 完全相同的隐私话术",
    "跳转无障碍设置后立即压栈的透明全屏引导页 demo.UponGuideActivity：单个全屏 TextView，白底白字居中显示 @string/acc_tips，点击任意处关闭",
    "每次广播/服务启动重放的同一引导页（无倒计时、无跳过按钮、无取消入口）",
    "应用内另有 @string/accessibility_desc / accessibility_string = 『Accessibility Services』，用于设置页文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please open the Acccessibility on, protect your information not to be leaked, not to be stolen, to prevent others from spying on your privacy.",
      "text_zh": "请开启无障碍（Acccessibility）开关，保护您的信息不被泄露、不被窃取，防止他人窥探您的隐私。",
      "source_location": "res/values/strings.xml key=acc_tips（同文复用于 acc_desc）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Acccessibility Privacy protection",
      "text_zh": "无障碍 隐私保护",
      "source_location": "res/values/strings.xml key=acc_title（Manifest service android:label）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Services",
      "text_zh": "无障碍服务",
      "source_location": "res/values/strings.xml key=accessibility_desc / accessibility_string",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow Ad to create a calendar event?",
      "text_zh": "允许广告创建日历事件？",
      "source_location": "res/values/strings.xml key=create_calendar_message",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow Ad to store image in Picture gallery?",
      "text_zh": "允许广告将图片存入相册？",
      "source_location": "res/values/strings.xml（广告 SDK 权限提示）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无 onResume 轮询死循环，改为广播驱动的反复拉起：只要 m.a(context)（Settings.Secure.enabled_accessibility_services 中不含『包名/demo.LUAccessService』）为 false，每次 BOOT_COMPLETED、ACTION_POWER_CONNECTED、USER_PRESENT、SCREEN_ON、PACKAGE_ADDED/REMOVED 等广播，以及 demo.UCService.onCreate/onStartCommand 执行时，都会重新执行 o.c(context) 跳转无障碍设置并压上引导遮罩；用户按返回或点击遮罩关闭仅结束当次引导。",
    "overlay_or_fake_settings": "使用 Theme.Translucent.NoTitleBar 的全屏透明 Activity（demo.UponGuideActivity，excludeFromRecents）压栈在真实系统无障碍设置页之上，形成白底白字引导文字与系统无障碍开关同屏的叠层效果；不是自绘的高仿设置页，开关仍为系统原生控件。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "获权后 com.b.a.a.m.b() 在命中『下载中/正在下载』等词表节点时调用 performGlobalAction(1)（GLOBAL_ACTION_BACK）关闭当前页面并广播 ACTION_CLOSE_VIEW，用于自动关闭安装器/落地页而非阻止用户撤权；未见监听设置页阻止关闭无障碍开关的逻辑。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以广播触发为主：在设备上执行 adb shell am broadcast -a android.intent.action.ACTION_POWER_CONNECTED（或 SCREEN_ON/USER_PRESENT），或直接 adb shell am start -n com.countrys.converter.currency/demo.UponGuideActivity；UTG 应在监测到 Activity 栈顶出现 android.settings.ACCESSIBILITY_SETTINGS 后 500ms 内的下一次栈顶变化时立刻抓取（此时 UponGuideActivity 已压栈）。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转后叠压的系统无障碍设置页 + 透明引导页合成画面",
        "page_identifier": "Activity 栈顶为 demo.UponGuideActivity（Theme.Translucent.NoTitleBar），下层为 com.android.settings 无障碍列表",
        "why_most_useful": "这是诱导的核心瞬间：透明引导文字直接覆盖在系统无障碍开关上方，可证明『系统设置页 + 自定义话术叠层』的引导手法",
        "observable_utg_signals": [
          "Activity 栈顶 demo.UponGuideActivity 与下层 com.android.settings/.Settings$AccessibilitySettings 同时存在",
          "全屏 TextView 文本含『Please open the Acccessibility on』",
          "无可见的取消/跳过按钮节点"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务列表，条目文本『Acccessibility Privacy protection』及副标题隐私话术",
        "why_most_useful": "证明服务名与说明文案的伪装身份，以及与『Money Converter』货币转换器功能完全无关",
        "observable_utg_signals": [
          "列表项 label 文本『Acccessibility Privacy protection』（含三 c 拼写）",
          "description 文本与引导页文案完全一致",
          "应用包名 com.countrys.converter.currency"
        ]
      },
      {
        "page_role": "重复拉起验证页（拒权反馈）",
        "page_identifier": "返回后再次触发 SCREEN_ON/POWER_CONNECTED 广播，栈顶重新出现 ACCESSIBILITY_SETTINGS + UponGuideActivity",
        "why_most_useful": "证明拒权后无降级路径、由广播驱动无限重试",
        "observable_utg_signals": [
          "同一 Activity 组合在 30 秒内重复出现",
          "两次拉起之间无任何用户可点的退出路径"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导全为纯文本节点，无图片诱饵，UTG 文本可直取。需注意两点：一是引导页为白底白字（背景 0x7FFFFFFF + 文字 -1），若 UTG 仅做对比度渲染采样可能漏看文字，应以控件树 text 属性为准；二是获权后的自动点击阶段发生在 com.mobpower.a.g.g.a 广告落地页，需先置 SharedPreferences 键『run』为 true 才会触发，纯 UTG 在该阶段前观察不到行为。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.b.a.a.o.c",
    "demo.OpenAccessReceiver.onReceive",
    "demo.UponGuideActivity.onCreate",
    "demo.UponGuideActivity$1.onClick",
    "com.b.a.a.m.a(Context)",
    "res/values/strings.xml#acc_tips / acc_desc / acc_title；res/xml/email_config.xml"
  ]
}
```

</details>
