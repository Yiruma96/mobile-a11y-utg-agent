# MR_043__d240e9809b｜BoostClicker — SystemSecurityServices

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：91.7s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 SystemSecurityServices 的样本冷启动即无界面反射装载加密类，用「点右上角开启无障碍防病毒」的图片/悬浮引导把用户推向系统无障碍开关，真实引导 UI 藏在字符串与类名加密层后。
- **静态可见性说明**：DEX 结构完整可读（无壳、15 个类），但关键类名/方法名/参数与界面文案均以 Base64+自定义算法（g.a/g.b）加密后经反射 newInstance 动态装载，入口 dibd.onCreate 无任何布局；assets/fields.css 为非 UTF-8 明文（偏移 44 出现 0xa3，疑加密），assets/guide.gif 为图片引导。真实引导弹窗与 ACCESSIBILITY_SETTINGS 跳转点无法静态还原，需运行期解密或动态观测补齐。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d240e9809bfe98ed6af4b8853b7556a9207e6e3c325f200e9df0fdc63582fddc` |
| 包名 / 年份 | `com.services.ndtdq.swsloflgfkcj` / 2020 |
| 家族 / 品类 | **BoostClicker**（同池样本数：2） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/20/b/malicious-apps-on-google-play-communicate-with-trojans-install-malware-perform-mobile-ad-fraud.html |
| 桌面显示名 | SystemSecurityServices |
| 引导页宣称品牌/身份 | 系统安全服务（SystemSecurityServices，冒充系统级手机防病毒安全组件） |
| 系统无障碍列表服务名 | SystemSecurityServices |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 应用 label 与无障碍服务 label 复用同一字符串 @string/access_name，桌面名与无障碍列表项完全一致，制造系统组件错觉；2) access_desc 使用 \n\n 空行把系统无障碍确认页的高风险提示挤出可视区；3) 主入口 Activity 无布局、无界面，直接反射装载由加密串决定的类；4) 申请 INSTALL_SHORTCUT/UNINSTALL_SHORTCUT 便于隐藏或替换启动入口。 |
| 无障碍服务类名 | `com.services.AccService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Please click the button in the top right corner.<br><br>Turn on accessibility to better protect your phone from viruses.<br><br>Please feel free to open. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.axl.mngp.dibd（Manifest 中唯一带 MAIN action 的 Activity） | onCreate 被调用（桌面点击图标即触发，无任何前置界面） | 不可静态还原 | 无 | 无需用户操作，点击图标即静默执行后续反射装载流程 | `com.axl.mngp.dibd.onCreate → com.axl.mngp.h.a / com.axl.mngp.g.a` |
| 2 | 业务功能触发 | com.axl.mngp.c + com.axl.mngp.i 反射装载器（目标类名由 g.a 解密得出） | h.a(context, g.a("VjFKVVRxNmZ1…"), {Context,Activity,Intent}, {…}) 提交到单线程 ExecutorService，c.a(b) 内 getMethod(g.a(...)).newInstance() 成功后 sendEmptyMessage(10) 回调 | 不可静态还原 | **原文**：无（类名/方法名密文，静态解密仅得中间串 "V1JUTq6fuHvUdGzfBEPCEpWLkgRWmpsOJ0C649"）<br>**译注**：解密后动态实例化的类承载真正的引导逻辑，静态无法确定其界面形态 | 不可静态还原 | `com.axl.mngp.h.a / com.axl.mngp.c.a(com.axl.mngp.b) / com.axl.mngp.g.a` |
| 3 | 引导说明页 | 图片/遮罩式引导（assets/guide.gif + assets/fields.css，疑加密），由反射装载类拉起 | 反射装载类初始化后（step 2 回调）拉起引导 | 悬浮窗Overlay | **原文**：无（assets 中无 HTML/文本引导，仅 guide.gif 与疑似加密的 fields.css）<br>**译注**：以动图演示操作步骤的引导层，文字内容不可静态提取 | 按动图指示前往系统设置开启无障碍；取消/跳过入口不可静态确认 | `assets/guide.gif / assets/fields.css / AndroidManifest.xml(SYSTEM_ALERT_WINDOW)` |
| 4 | 跳无障碍设置 | 系统「设置 → 无障碍 → 已下载的服务」列表项 SystemSecurityServices | 跳转 Intent（ACTION_ACCESSIBILITY_SETTINGS，位于加密串/反射装载类中，静态不可定位）后系统页展示服务项 | 系统无障碍页 | **原文**：SystemSecurityServices<br><br>Please click the button in the top right corner.<br><br>Turn on accessibility to better protect your phone from viruses.<br><br>Please feel free to open.<br>**译注**：SystemSecurityServices（系统安全服务）／请点击右上角的按钮。／开启无障碍以更好地保护你的手机免受病毒侵害。／请放心开启。 | 要求用户点击屏幕右上角开关位开启无障碍；系统页本身提供返回/取消，但应用侧的返回反应不可静态确认 | `res/values/strings.xml (access_name / access_desc) / res/xml/config.xml / com.services.AccService` |
| 5 | 获权后动作 | com.services.AccService.onAccessibilityEvent → com.axl.mngp.a.a(this,1,event) | 无障碍事件回调（获权后系统持续投递 TYPE_WINDOW_STATE_CHANGED 等事件） | 不可静态还原 | 无 | 无（用户不再被提示，后台静默执行） | `com.services.AccService.onAccessibilityEvent / com.services.AccService.onInterrupt` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项名称与说明：application@label 与 service@label 均为 @string/access_name = "SystemSecurityServices"，说明为 @string/access_desc（res/values/strings.xml），即用户唯一可静态确认的引导文案位置
- 无障碍配置引用：res/xml/config.xml（android:description 指向 access_desc，metadata android.accessibilityservice）
- 资产目录图片引导：assets/guide.gif（动图演示操作步骤，无文本层）
- 疑似加密样式/资产：assets/fields.css（非 UTF-8 明文，偏移 44 出现 0xa3），可能为引导层样式，内容不可读
- 冷启动界面：com.axl.mngp.dibd 无 setContentView，屏幕上不出现任何说明文字
- 反射装载类（类名由 g.a 加密）内的弹窗/WebView/悬浮引导：静态不可还原，未发现本地 HTML 页面

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | SystemSecurityServices | 系统安全服务 | `res/values/strings.xml key=access_name（同时用作 application@label 与 accessibility service@label）` | 假反诈安全 |
| en | Please click the button in the top right corner.<br><br>Turn on accessibility to better protect your phone from viruses.<br><br>Please feel free to open. | 请点击右上角的按钮。开启无障碍以更好地保护你的手机免受病毒侵害。请放心开启。 | `res/values/strings.xml key=access_desc（经 res/xml/config.xml 的 android:description 呈现于系统无障碍确认页）` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态确认：主入口 dibd.onCreate 无界面、直接反射装载加密类，未观察到降级分支；是否存在 onResume/定时器重跳或返回后再次拉起，取决于加密类名所指类的实现（另有 MainService 与 PACKAGE_ADDED/BOOT_COMPLETED/USER_PRESENT 接收器 com.axl.mngp.lwwny，具备后台重拉与重新引导的条件）
- **遮罩叠层 / 高仿系统设置页**：已声明 SYSTEM_ALERT_WINDOW 并内置 assets/guide.gif 图片引导，具备在系统设置页之上叠放半透明图片/悬浮引导层的条件；未发现伪造系统无障碍开关页的资源或布局证据
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk 21，早于 Android 13 受限设置机制；"click the button in the top right corner" 语义上指系统页右上角开关位，而非应用详情页菜单的「允许受限设置」）
- **获权后即时行为与防撤权机制**：静态未见自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码；但 AccService 获权后把全部事件转发至 com.axl.mngp.a.a，其内部逻辑加密，不能排除运行期撤权干扰
- **良性降级 / 替代方案**：无（未见手动模式、仅观看模式或明示取消后降级路径；主入口完全不渲染界面，无良性说明载体）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 com.axl.mngp.dibd.onCreate 返回后、以及监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间拉起 UTG；同时可 Hook com.axl.mngp.c.a(com.axl.mngp.b) 中 getMethod/newInstance 成功点，捕获反射装载类的首个界面
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在三处盲区：1) 主入口 dibd.onCreate 不渲染任何界面，纯 UTG 在冷启动瞬间可能只抓到空屏，需按 Activity 生命周期而非首屏文本触发；2) 引导以 assets/guide.gif 动图承载、无文本层，必须 OCR；3) 类名与界面文案经 g.a/g.b 加密 + 反射 newInstance 动态装载，assets/fields.css 亦非明文，静态无法列出完整页面清单，纯 UTG 需覆盖「反射装载后任意新 Activity/Overlay」而非固定类名白名单。静态加壳判定为 False，不阻挡运行期 UTG。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首个界面（判断是否直弹引导弹窗/悬浮层）** | 包名 com.services.ndtdq.swsloflgfkcj 下 onCreate 之后出现的首个 Activity 或 TYPE_APPLICATION 悬浮窗口；或 guide.gif 动图渲染的 ImageView/Overlay | 该应用主入口无布局，真实引导载体全部在反射装载类中，此处是唯一能直接看到诱导文案与按钮的时刻 | 界面无任何取消/关闭按钮的文本节点；出现「protect your phone from viruses」「top right corner」类文案；界面为单张 GIF 动图 + 无文字说明 |
| **跳转前/跳转瞬间的悬浮指引层** | 设置页之上叠加的 WindowManager TYPE_SYSTEM_ALERT/TYPE_APPLICATION_OVERLAY 视图（权限 SYSTEM_ALERT_WINDOW 已声明） | 家族特征是在系统无障碍页压栈图片指引，直接决定是否构成叠层诱导 | 系统无障碍页 UI 树之上出现本包窗口节点；遮罩层含箭头/手指指向右上角开关位；遮罩层拦截返回或点击穿透 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务，条目文本 SystemSecurityServices | 确认伪装身份与 description 排版规避是否在真机生效（空行把风险提示挤出可视区） | 列表项名称与系统类服务同名；description 含连续空行、风险提示不可见；服务项与桌面应用名一致造成系统组件错觉 |
| **获权后首屏动作** | 无障碍开启后由 com.services.AccService 触发的前台窗口/点击目标（event source package） | 验证获权是否立即转入自动点击或第三方应用窗口操作，界定恶意用途 | 无障碍事件后短时间内出现跨包窗口切换；出现非用户操作的点击/滚动；返回键被消费或无法撤权 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.axl.mngp.dibd.onCreate`
- `com.axl.mngp.h.a`
- `com.axl.mngp.c.a(com.axl.mngp.b)`
- `com.axl.mngp.g.a`
- `com.services.AccService.onAccessibilityEvent`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，共 14 次工具调用内收口）

**一句话：** 桌面图标名为 `SystemSecurityServices` 的应用在冷启动时**不渲染任何界面**（`onCreate` 没有调用 `setContentView`），直接把加密的类名交给反射装载器执行后续流程；其无障碍服务同样以“系统安全服务”身份注册，并通过 `android:description` 中的换行排版要求用户“点右上角开启无障碍，以保护手机免受病毒侵害”。真正的引导 UI 与跳转逻辑位于字符串和类名加密层之后。

**已证实事实**
- Manifest：`minSdk 8 / targetSdk 21`，`application@label` 与无障碍 `service@label` **同为一个值** `@string/access_name = SystemSecurityServices`，即桌面名=无障碍列表项名，伪装成系统安全服务。
- 无障碍声明：[res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3-L8>) 的 `access_desc` 使用 `\n\n` 空行分隔，内容为“点右上角按钮 / 开启无障碍以更好地防病毒 / 放心开启”；配置在 `res/xml/config.xml`。
- 关键权限：`SYSTEM_ALERT_WINDOW`（悬浮窗）、`GET_TASKS`、`RECEIVE_BOOT_COMPLETED`、`INSTALL_SHORTCUT/UNINSTALL_SHORTCUT` —— 具备叠层遮罩、任务枚举、开机重拉与快捷方式隐藏的能力组合。
- 入口无 UI：[com.axl.mngp.dibd#onCreate](<resource-unit:#1.dex1 code:com.axl.mngp.dibd#onCreate>) 只执行 `h.a(ctx, g.a("<base64>"), {Context,Activity,Intent}, {…})`，没有任何布局或弹窗代码。
- 反射装载器：[com.axl.mngp.h#a](<resource-unit:#1.dex1 code:com.axl.mngp.h#a>) → [com.axl.mngp.c#a(com.axl.mngp.b)](<resource-unit:#1.dex1 code:com.axl.mngp.c#a(com.axl.mngp.b)>) 用 `getClass().getMethod(g.a(...)).newInstance()` 按**解密后的类名**实例化类，再 `sendEmptyMessage(10)` 回调执行；类名、方法名、参数均为 `g.a()` 解密结果（`g.a` = Base64 + 自定义 `g.b` 二次解密，实测第一层 Base64 已可解出中间串）。
- 无障碍侧：[com.services.AccService#onAccessibilityEvent](<resource-unit:#1.dex1 code:com.services.AccService#onAccessibilityEvent>) 仅转发给 `com.axl.mngp.a.a(this,1,event)`，核心点击/窗口逻辑在 `a` 类内（同样依赖 `g.a` 解密串）。
- 资产：`assets/guide.gif`（图片式操作引导）+ `assets/fields.css`（**非 UTF-8 明文，位置 44 出现 0xa3，疑为加密/编码资产**），**无本地 HTML 页面**。

**分析判断（受加密层限制）**
- “点右上角按钮”指向系统页面右上角开关位（2020 年样本、targetSdk 21，早于 Android 13 受限设置机制，故不属于受限设置教学；语义上仍属“分步教学用户自行去开关”）。
- 存在 `guide.gif` + `SYSTEM_ALERT_WINDOW` 的组合，符合“跳系统设置后叠图片/遮罩指引”的家族特征，但**具体叠层代码位于加密类名所指类中，静态不可还原**。
- `access_desc` 的多空行排版会把系统无障碍确认页中的高风险提示挤到可视区外，属典型文案规避手法。

**未决与边界**
- 反射装载的目标类名、引导弹窗文案、`ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 的具体跳转点均在 `g.b` 加密串中；`fields.css` 与 `guide.gif` 承载的界面内容未解码。未使用动态分析（无在线设备前提未知，静态链已足够定性为伪装型无障碍诱导）。
- 因本次硬性工具预算已用尽，未写入风险台账；如需台账与 HTML 报告，请在放宽预算后授权续跑。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "DEX 结构完整可读（无壳、15 个类），但关键类名/方法名/参数与界面文案均以 Base64+自定义算法（g.a/g.b）加密后经反射 newInstance 动态装载，入口 dibd.onCreate 无任何布局；assets/fields.css 为非 UTF-8 明文（偏移 44 出现 0xa3，疑加密），assets/guide.gif 为图片引导。真实引导弹窗与 ACCESSIBILITY_SETTINGS 跳转点无法静态还原，需运行期解密或动态观测补齐。",
  "summary_one_liner": "伪装成 SystemSecurityServices 的样本冷启动即无界面反射装载加密类，用「点右上角开启无障碍防病毒」的图片/悬浮引导把用户推向系统无障碍开关，真实引导 UI 藏在字符串与类名加密层后。",
  "disguise_identity": {
    "app_display_name": "SystemSecurityServices",
    "claimed_brand_or_persona": "系统安全服务（SystemSecurityServices，冒充系统级手机防病毒安全组件）",
    "a11y_service_label": "SystemSecurityServices",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 应用 label 与无障碍服务 label 复用同一字符串 @string/access_name，桌面名与无障碍列表项完全一致，制造系统组件错觉；2) access_desc 使用 \\n\\n 空行把系统无障碍确认页的高风险提示挤出可视区；3) 主入口 Activity 无布局、无界面，直接反射装载由加密串决定的类；4) 申请 INSTALL_SHORTCUT/UNINSTALL_SHORTCUT 便于隐藏或替换启动入口。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.axl.mngp.dibd（Manifest 中唯一带 MAIN action 的 Activity）",
      "trigger_event": "onCreate 被调用（桌面点击图标即触发，无任何前置界面）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 未调用 setContentView，不显示任何界面，用户看不到任何说明",
      "user_action_requested": "无需用户操作，点击图标即静默执行后续反射装载流程",
      "code_anchor": "com.axl.mngp.dibd.onCreate → com.axl.mngp.h.a / com.axl.mngp.g.a"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.axl.mngp.c + com.axl.mngp.i 反射装载器（目标类名由 g.a 解密得出）",
      "trigger_event": "h.a(context, g.a(\"VjFKVVRxNmZ1…\"), {Context,Activity,Intent}, {…}) 提交到单线程 ExecutorService，c.a(b) 内 getMethod(g.a(...)).newInstance() 成功后 sendEmptyMessage(10) 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（类名/方法名密文，静态解密仅得中间串 \"V1JUTq6fuHvUdGzfBEPCEpWLkgRWmpsOJ0C649\"）",
      "shown_text_zh": "解密后动态实例化的类承载真正的引导逻辑，静态无法确定其界面形态",
      "user_action_requested": "不可静态还原",
      "code_anchor": "com.axl.mngp.h.a / com.axl.mngp.c.a(com.axl.mngp.b) / com.axl.mngp.g.a"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "图片/遮罩式引导（assets/guide.gif + assets/fields.css，疑加密），由反射装载类拉起",
      "trigger_event": "反射装载类初始化后（step 2 回调）拉起引导",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（assets 中无 HTML/文本引导，仅 guide.gif 与疑似加密的 fields.css）",
      "shown_text_zh": "以动图演示操作步骤的引导层，文字内容不可静态提取",
      "user_action_requested": "按动图指示前往系统设置开启无障碍；取消/跳过入口不可静态确认",
      "code_anchor": "assets/guide.gif / assets/fields.css / AndroidManifest.xml(SYSTEM_ALERT_WINDOW)"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍 → 已下载的服务」列表项 SystemSecurityServices",
      "trigger_event": "跳转 Intent（ACTION_ACCESSIBILITY_SETTINGS，位于加密串/反射装载类中，静态不可定位）后系统页展示服务项",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "SystemSecurityServices\n\nPlease click the button in the top right corner.\n\nTurn on accessibility to better protect your phone from viruses.\n\nPlease feel free to open.",
      "shown_text_zh": "SystemSecurityServices（系统安全服务）／请点击右上角的按钮。／开启无障碍以更好地保护你的手机免受病毒侵害。／请放心开启。",
      "user_action_requested": "要求用户点击屏幕右上角开关位开启无障碍；系统页本身提供返回/取消，但应用侧的返回反应不可静态确认",
      "code_anchor": "res/values/strings.xml (access_name / access_desc) / res/xml/config.xml / com.services.AccService"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.services.AccService.onAccessibilityEvent → com.axl.mngp.a.a(this,1,event)",
      "trigger_event": "无障碍事件回调（获权后系统持续投递 TYPE_WINDOW_STATE_CHANGED 等事件）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后进入事件驱动的自动操作逻辑（转发至 a.a，内部依赖 g.a 解密串），具体点击/窗口行为静态不可还原",
      "user_action_requested": "无（用户不再被提示，后台静默执行）",
      "code_anchor": "com.services.AccService.onAccessibilityEvent / com.services.AccService.onInterrupt"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项名称与说明：application@label 与 service@label 均为 @string/access_name = \"SystemSecurityServices\"，说明为 @string/access_desc（res/values/strings.xml），即用户唯一可静态确认的引导文案位置",
    "无障碍配置引用：res/xml/config.xml（android:description 指向 access_desc，metadata android.accessibilityservice）",
    "资产目录图片引导：assets/guide.gif（动图演示操作步骤，无文本层）",
    "疑似加密样式/资产：assets/fields.css（非 UTF-8 明文，偏移 44 出现 0xa3），可能为引导层样式，内容不可读",
    "冷启动界面：com.axl.mngp.dibd 无 setContentView，屏幕上不出现任何说明文字",
    "反射装载类（类名由 g.a 加密）内的弹窗/WebView/悬浮引导：静态不可还原，未发现本地 HTML 页面"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "SystemSecurityServices",
      "text_zh": "系统安全服务",
      "source_location": "res/values/strings.xml key=access_name（同时用作 application@label 与 accessibility service@label）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Please click the button in the top right corner.\n\nTurn on accessibility to better protect your phone from viruses.\n\nPlease feel free to open.",
      "text_zh": "请点击右上角的按钮。开启无障碍以更好地保护你的手机免受病毒侵害。请放心开启。",
      "source_location": "res/values/strings.xml key=access_desc（经 res/xml/config.xml 的 android:description 呈现于系统无障碍确认页）",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态确认：主入口 dibd.onCreate 无界面、直接反射装载加密类，未观察到降级分支；是否存在 onResume/定时器重跳或返回后再次拉起，取决于加密类名所指类的实现（另有 MainService 与 PACKAGE_ADDED/BOOT_COMPLETED/USER_PRESENT 接收器 com.axl.mngp.lwwny，具备后台重拉与重新引导的条件）",
    "overlay_or_fake_settings": "已声明 SYSTEM_ALERT_WINDOW 并内置 assets/guide.gif 图片引导，具备在系统设置页之上叠放半透明图片/悬浮引导层的条件；未发现伪造系统无障碍开关页的资源或布局证据",
    "restricted_settings_13plus_coaching": "无（targetSdk 21，早于 Android 13 受限设置机制；\"click the button in the top right corner\" 语义上指系统页右上角开关位，而非应用详情页菜单的「允许受限设置」）",
    "post_grant_anti_removal": "静态未见自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权代码；但 AccService 获权后把全部事件转发至 com.axl.mngp.a.a，其内部逻辑加密，不能排除运行期撤权干扰",
    "benign_graceful_degradation": "无（未见手动模式、仅观看模式或明示取消后降级路径；主入口完全不渲染界面，无良性说明载体）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 com.axl.mngp.dibd.onCreate 返回后、以及监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间拉起 UTG；同时可 Hook com.axl.mngp.c.a(com.axl.mngp.b) 中 getMethod/newInstance 成功点，捕获反射装载类的首个界面",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首个界面（判断是否直弹引导弹窗/悬浮层）",
        "page_identifier": "包名 com.services.ndtdq.swsloflgfkcj 下 onCreate 之后出现的首个 Activity 或 TYPE_APPLICATION 悬浮窗口；或 guide.gif 动图渲染的 ImageView/Overlay",
        "why_most_useful": "该应用主入口无布局，真实引导载体全部在反射装载类中，此处是唯一能直接看到诱导文案与按钮的时刻",
        "observable_utg_signals": ["界面无任何取消/关闭按钮的文本节点", "出现「protect your phone from viruses」「top right corner」类文案", "界面为单张 GIF 动图 + 无文字说明"]
      },
      {
        "page_role": "跳转前/跳转瞬间的悬浮指引层",
        "page_identifier": "设置页之上叠加的 WindowManager TYPE_SYSTEM_ALERT/TYPE_APPLICATION_OVERLAY 视图（权限 SYSTEM_ALERT_WINDOW 已声明）",
        "why_most_useful": "家族特征是在系统无障碍页压栈图片指引，直接决定是否构成叠层诱导",
        "observable_utg_signals": ["系统无障碍页 UI 树之上出现本包窗口节点", "遮罩层含箭头/手指指向右上角开关位", "遮罩层拦截返回或点击穿透"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，条目文本 SystemSecurityServices",
        "why_most_useful": "确认伪装身份与 description 排版规避是否在真机生效（空行把风险提示挤出可视区）",
        "observable_utg_signals": ["列表项名称与系统类服务同名", "description 含连续空行、风险提示不可见", "服务项与桌面应用名一致造成系统组件错觉"]
      },
      {
        "page_role": "获权后首屏动作",
        "page_identifier": "无障碍开启后由 com.services.AccService 触发的前台窗口/点击目标（event source package）",
        "why_most_useful": "验证获权是否立即转入自动点击或第三方应用窗口操作，界定恶意用途",
        "observable_utg_signals": ["无障碍事件后短时间内出现跨包窗口切换", "出现非用户操作的点击/滚动", "返回键被消费或无法撤权"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在三处盲区：1) 主入口 dibd.onCreate 不渲染任何界面，纯 UTG 在冷启动瞬间可能只抓到空屏，需按 Activity 生命周期而非首屏文本触发；2) 引导以 assets/guide.gif 动图承载、无文本层，必须 OCR；3) 类名与界面文案经 g.a/g.b 加密 + 反射 newInstance 动态装载，assets/fields.css 亦非明文，静态无法列出完整页面清单，纯 UTG 需覆盖「反射装载后任意新 Activity/Overlay」而非固定类名白名单。静态加壳判定为 False，不阻挡运行期 UTG。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.axl.mngp.dibd.onCreate",
    "com.axl.mngp.h.a",
    "com.axl.mngp.c.a(com.axl.mngp.b)",
    "com.axl.mngp.g.a",
    "com.services.AccService.onAccessibilityEvent",
    "res/values/strings.xml"
  ]
}
```

</details>
