# MR_050__6032c1a8b5｜LeifAccess — SystemSecurityServices

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：159.2s

## 1. 一句话核心结论

- **核心申请方式**：以 SystemSecurityServices 名义冒用系统安全组件，用『保护手机免受病毒』文案与 guide.gif 图文教用户开启无障碍，并靠 Settings$Secure 轮询在未授权时反复重跳系统无障碍设置页，获权后自动点击/手势/填充文本。
- **静态可见性说明**：一阶段 APK 为空壳：入口 com.axl.mngp.dibd 不含业务逻辑，全部关键字符串由 com.axl.mngp.g#b 的 Base64+16轮XOR 加密，真实主体位于 assets/fields.css（跳过前32字节、尾部16字节为XOR密钥）解出的 fields.jar/classes.dex，由 DexClassLoader 装载 com.inter.interfaces.InterInterfaceImpl。该二阶段载荷已在静态层面完整还原并分析，引导/跳转/自动点击链路全部可见；仅后续远控指令（com.inter.obfuscated.hk 的网络拉取与 36000000ms 轮询）内容依赖运行时下发。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6032c1a8b54f3daf9697a49fdd398d3ebe35f3fec3d945d6d8e9588043332969` |
| 包名 / 年份 | `com.services.ibgpe.hflbsqqjrmlfej` / 2020 |
| 家族 / 品类 | **LeifAccess**（同池样本数：1） |
| 原始来源标识 | https://www.mcafee.com/blogs/other-blogs/mcafee-labs/android-leifaccess-a-is-the-silent-fake-reviewer-trojan/?hilite=%27Android%27%2C%27Malware%27 |
| 桌面显示名 | SystemSecurityServices |
| 引导页宣称品牌/身份 | SystemSecurityServices（伪造的系统级安全/杀毒服务） |
| 系统无障碍列表服务名 | SystemSecurityServices |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：类名混淆为 com.inter.obfuscated.a~z；全部关键字符串（Action、类名、方法名、日志文案）经 Base64+16轮循环 XOR 加密；二阶段 DEX 以 assets/fields.css 伪装为样式文件并以 DexClassLoader 动态装载；入口 Activity 无 UI 仅做反射分发；application 与 service 复用同一 @string/access_name 强化系统组件假象。未使用空白/换行挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.services.AccService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Please click the button in the top right corner.<br><br>Turn on accessibility to better protect your phone from viruses.<br><br>Please feel free to open. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.axl.mngp.dibd（Manifest 中唯一 MAIN Activity，无布局、无业务界面） | onCreate | 原生Activity | 无 | 无需用户操作，用户仅看到应用一闪而过 | `com.axl.mngp.dibd#onCreate` |
| 2 | 冷启动入口 | com.axl.mngp.h#a → com.axl.mngp.i#a → 二阶段 com.inter.interfaces.InterInterfaceImpl#startA | onCreate 中调用 h.a(ctx, g.a("VjFKVVRx..."), {Context,Activity,Intent}, {ctx,this,intent})，字符串解密后为 startA；i#a 在工作线程反射 invoke | 不可静态还原 | 无 | 无 | `com.axl.mngp.h#a / com.axl.mngp.i#a / com.inter.interfaces.InterInterfaceImpl#startA` |
| 3 | 业务功能触发 | InterInterfaceImpl.startA 的 switch(int extra)，extra key 取 com.inter.obfuscated.hm.c | getIntExtra(hm.c, 0) 命中 case 40/50/60/70/71/80/90/91 等分支，分支内调用 com.inter.obfuscated.hi#a(Intent)、finish() 及 ap/v/ac/ar/av 等流程对象 | 不可静态还原 | 无 | 无（参数由调用方/自身服务与广播传入） | `com.inter.interfaces.InterInterfaceImpl#startA` |
| 4 | 跳无障碍设置 | com.inter.obfuscated.an#b(Context) 拉起系统 Settings.ACTION_ACCESSIBILITY_SETTINGS | 由 com.inter.obfuscated.ap#a、v#a、ac#a、ar#b、av#onClick 等流程节点调用（av#onClick 为用户点击触发） | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：系统无障碍服务列表页，列表中出现 SystemSecurityServices 项 | 要求用户在该列表中点击 SystemSecurityServices 并打开开关；系统页无本应用提供的取消/跳过按钮 | `com.inter.obfuscated.an#b` |
| 5 | 引导说明页 | assets/guide.gif 图文操作指引 + 无障碍列表项描述 res/values/strings.xml access_desc | 跳转设置前后与设置页内持续可见 | 原生Activity | **原文**：Please click the button in the top right corner.<br><br>Turn on accessibility to better protect your phone from viruses.<br><br>Please feel free to open.<br>**译注**：请点击右上角的按钮。开启无障碍，以更好地保护您的手机免受病毒侵害。请放心开启。 | 要求用户点击右上角按钮并开启无障碍开关，无取消/跳过说明 | `#1 file:assets/guide.gif / #1 file:res/values/strings.xml#L4-L8 / #1 file:res/xml/config.xml#L2-L3` |
| 6 | 拒权反馈循环 | com.inter.obfuscated.an#a(Context) 读 Settings$Secure 判定 → 未授权时再次调用 an#b(Context) | 读取 accessibility_enabled 与 enabled_accessibility_services，用 toLowerCase().contains(packageName) 判定；返回 false 即重跳 | 系统无障碍页 | **原文**：accessibility_enabled / enabled_accessibility_services<br>**译注**：以系统设置项作为闸门，未授权则循环回到无障碍列表页 | 用户返回或拒绝后仍被重新送入设置页，无退出路径 | `com.inter.obfuscated.an#a(Context)` |
| 7 | 获权后动作 | com.services.AccService#onAccessibilityEvent → com.axl.mngp.a#a → 二阶段 setAccessEvent；节点操作为 com.inter.obfuscated.an 各重载 | 无障碍事件回调（AccessibilityEvent）与 onInterrupt | 不可静态还原 | **原文**：setAccessEvent / setAccessInterrupt<br>**译注**：接管全部无障碍事件，并对当前窗口节点执行点击、手势与文本填充 | 无，完全后台自动执行 | `com.services.AccService#onAccessibilityEvent / com.axl.mngp.a#a / com.inter.obfuscated.an#a(AccessibilityService,String)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：res/values/strings.xml 中 @string/access_desc（经 res/xml/config.xml android:description 引用）
- 系统无障碍服务名称：@string/access_name = SystemSecurityServices（同时作为 application android:label）
- assets/guide.gif：图文操作指引素材，展示点击右上角按钮开启开关的步骤
- 未发现本地 HTML/WebView 教学页、未发现确认的悬浮窗遮罩层、未发现不可取消的自定义 AlertDialog（引导文案全部寄生于系统无障碍页）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please click the button in the top right corner.<br><br>Turn on accessibility to better protect your phone from viruses.<br><br>Please feel free to open. | 请点击右上角的按钮。开启无障碍，以更好地保护您的手机免受病毒侵害。请放心开启。 | `res/values/strings.xml key=access_desc（由 res/xml/config.xml android:description 引用）` | 假反诈安全 |
| en | SystemSecurityServices | 系统安全服务（伪造的系统级安全组件名称） | `res/values/strings.xml key=access_name（application android:label 与 service android:label）` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：an#a(Context) 通过 Settings$Secure 的 accessibility_enabled 与 enabled_accessibility_services 判定本包是否已授权，返回 false 时由 an#b(Context) 再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)，用户返回或拒绝后被重新送入系统无障碍列表页，无退出或降级分支。
- **遮罩叠层 / 高仿系统设置页**：未发现叠层遮罩、全屏悬浮窗或高仿无障碍开关页；SYSTEM_ALERT_WINDOW 权限已声明但未定位到对应叠层实现，引导依赖系统无障碍页本身与 guide.gif 图文说明。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=21，未发现跳转 ACTION_APPLICATION_DETAILS_SETTINGS 的受限设置分步教学，也未发现 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：未发现监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；但获权后 an 类具备 performAction(16) 自动点击与 dispatchGesture 坐标手势能力，可用于静默点击确认类界面。
- **良性降级 / 替代方案**：无。不存在手动模式、ADB 引导或仅观看模式等替代路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 com.axl.mngp.dibd 后立即拉起采集，并以监测到 Activity 切换为 android.settings.ACCESSIBILITY_SETTINGS（settings 包无障碍页）作为关键锚点；用户从设置页返回时再次触发同一锚点，即可验证拒权重跳循环。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案寄生于系统无障碍页而非应用自有页面，若仅在应用进程内采集 UTG 会漏掉核心引导帧，必须覆盖 com.android.settings 前台窗口；另应用无自有引导界面，冷启动后立即跳转，启动瞬间画面极短易漏采。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转后的系统无障碍服务列表页** | 包名 com.android.settings、界面含无障碍服务列表且出现条目 SystemSecurityServices | 该页同时给出应用宣称身份与用户被要求执行的动作，是判定诱导授权最直接的一帧 | 列表项文本 SystemSecurityServices；列表项描述含 protect your phone from viruses；存在可点击开关控件且当前为关闭态 |
| **拒权后重跳循环验证页** | 连续两次进入 com.android.settings 无障碍页，间隔内无用户主动操作 | 区分『一次性引导』与『强制循环』，是定性 coercion 的关键 | 两次无障碍设置页的 Activity 出现时间戳；返回键后无本应用降级页出现；循环次数≥2 |
| **获权后的自动点击现场** | 本应用无障碍开关被打开后，前台窗口节点被 performAction/dispatchGesture 触发点击 | 证明权限被用于代替用户操作，而非宣称的病毒防护 | 非用户输入产生的点击事件；窗口内容在无触摸输入下发生变化；剪贴板内容被写入并粘贴到输入框 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.axl.mngp.dibd#onCreate`
- `com.axl.mngp.f#b`
- `com.axl.mngp.h#a`
- `com.inter.interfaces.InterInterfaceImpl#startA`
- `com.inter.obfuscated.an#b`
- `com.inter.obfuscated.an#a(Context)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**该样本的一阶段 APK 只是一个外壳，真正的主体被加密隐藏在 `assets/fields.css` 中，我已在静态层面完整还原。**

**1. 载荷隐藏方式（静态可见性）**
- `com.axl.mngp.dibd.onCreate` 不含任何业务逻辑，只把控制权交给一个 Base64/XOR 加密的类名；该字符串解出为 `startA`。
- `com.axl.mngp.f#b` 用“跳过前 32 字节、以尾部 16 字节作 XOR 密钥”的方式解出 `assets/fields.css`，还原得到含 502KB `classes.dex` 的 `fields.jar`，再由 `DexClassLoader` 装载，入口为 `com.inter.interfaces.InterInterfaceImpl`。
- 所有关键字符串由 `com.axl.mngp.g#b`（Base64 + 16 轮循环 XOR）加密，因此常规字符串检索查不到任何诱导文案或设置 Action。**我已离线解出全部字符串，并从二阶段 DEX 静态贯通整条引导链。**

**2. 引导/强制的 UTG 流转**
- 主 Activity 启动即把控制权交给 `InterInterfaceImpl.startA(Context, Activity, Intent)`；该方法按 Intent 中的 int extra 分派，没有正常业务界面。
- 跳转点唯一且明确：`com.inter.obfuscated.an#b(Context)` 构造 `Intent("android.settings.ACCESSIBILITY_SETTINGS")`，`addFlags(0x10000000)` 后 `startActivity`，直接把用户送到系统无障碍服务列表页。
- 授权状态判断：`an#a(Context)` 读取 `Settings$Secure` 的 `accessibility_enabled` 与 `enabled_accessibility_services`，再用小写 `contains(packageName)` 判断是否已授权；返回 false 时再次跳转设置页，**形成没有取消或跳过入口的反馈循环**。
- 引导载体是 `assets/guide.gif` 图文步骤与 `@string/access_desc`（系统列表项描述），文案教用户“点击右上角按钮”开启开关；**没有本地 HTML、没有 WebView 教学页，也没有确认存在的悬浮遮罩**（`SYSTEM_ALERT_WINDOW` 已声明，但未找到实际叠层代码）。
- `targetSdkVersion=21`，未发现 `APPLICATION_DETAILS_SETTINGS` 跳转或 Android 13 受限设置分步教学。

**3. 获权后的实际能力**
`AccService.onAccessibilityEvent` 将全部事件经 `a#a` 反射转发至二阶段 `setAccessEvent`；`an` 类具备 `findAccessibilityNodeInfosByViewId` + `performAction(16)` 自动点击、`dispatchGesture` 按坐标模拟点击、以及“剪贴板写入 + `performAction(1)/(32768)`”文本填充能力。

**4. 身份伪装**
应用 label 与无障碍服务名同为 `SystemSecurityServices`，配合“保护手机免受病毒”的虚假安全承诺，冒用系统安全组件身份；真实业务主体被完全隐藏在加密载荷中。

已登记风险 **R-001**（`deceptive_behavior` / high）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "一阶段 APK 为空壳：入口 com.axl.mngp.dibd 不含业务逻辑，全部关键字符串由 com.axl.mngp.g#b 的 Base64+16轮XOR 加密，真实主体位于 assets/fields.css（跳过前32字节、尾部16字节为XOR密钥）解出的 fields.jar/classes.dex，由 DexClassLoader 装载 com.inter.interfaces.InterInterfaceImpl。该二阶段载荷已在静态层面完整还原并分析，引导/跳转/自动点击链路全部可见；仅后续远控指令（com.inter.obfuscated.hk 的网络拉取与 36000000ms 轮询）内容依赖运行时下发。",
  "summary_one_liner": "以 SystemSecurityServices 名义冒用系统安全组件，用『保护手机免受病毒』文案与 guide.gif 图文教用户开启无障碍，并靠 Settings$Secure 轮询在未授权时反复重跳系统无障碍设置页，获权后自动点击/手势/填充文本。",
  "disguise_identity": {
    "app_display_name": "SystemSecurityServices",
    "claimed_brand_or_persona": "SystemSecurityServices（伪造的系统级安全/杀毒服务）",
    "a11y_service_label": "SystemSecurityServices",
    "identity_mismatch": true,
    "obfuscation_tricks": "类名混淆为 com.inter.obfuscated.a~z；全部关键字符串（Action、类名、方法名、日志文案）经 Base64+16轮循环 XOR 加密；二阶段 DEX 以 assets/fields.css 伪装为样式文件并以 DexClassLoader 动态装载；入口 Activity 无 UI 仅做反射分发；application 与 service 复用同一 @string/access_name 强化系统组件假象。未使用空白/换行挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.axl.mngp.dibd（Manifest 中唯一 MAIN Activity，无布局、无业务界面）",
      "trigger_event": "onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面呈现，启动即静默转交控制权",
      "user_action_requested": "无需用户操作，用户仅看到应用一闪而过",
      "code_anchor": "com.axl.mngp.dibd#onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.axl.mngp.h#a → com.axl.mngp.i#a → 二阶段 com.inter.interfaces.InterInterfaceImpl#startA",
      "trigger_event": "onCreate 中调用 h.a(ctx, g.a(\"VjFKVVRx...\"), {Context,Activity,Intent}, {ctx,this,intent})，字符串解密后为 startA；i#a 在工作线程反射 invoke",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "加密类名/方法名分发，无任何界面文案",
      "user_action_requested": "无",
      "code_anchor": "com.axl.mngp.h#a / com.axl.mngp.i#a / com.inter.interfaces.InterInterfaceImpl#startA"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "InterInterfaceImpl.startA 的 switch(int extra)，extra key 取 com.inter.obfuscated.hm.c",
      "trigger_event": "getIntExtra(hm.c, 0) 命中 case 40/50/60/70/71/80/90/91 等分支，分支内调用 com.inter.obfuscated.hi#a(Intent)、finish() 及 ap/v/ac/ar/av 等流程对象",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "按 Intent 参数选择动作码，不呈现文案",
      "user_action_requested": "无（参数由调用方/自身服务与广播传入）",
      "code_anchor": "com.inter.interfaces.InterInterfaceImpl#startA"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "com.inter.obfuscated.an#b(Context) 拉起系统 Settings.ACTION_ACCESSIBILITY_SETTINGS",
      "trigger_event": "由 com.inter.obfuscated.ap#a、v#a、ac#a、ar#b、av#onClick 等流程节点调用（av#onClick 为用户点击触发）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "系统无障碍服务列表页，列表中出现 SystemSecurityServices 项",
      "user_action_requested": "要求用户在该列表中点击 SystemSecurityServices 并打开开关；系统页无本应用提供的取消/跳过按钮",
      "code_anchor": "com.inter.obfuscated.an#b"
    },
    {
      "step": 5,
      "stage": "引导说明页",
      "screen_or_component": "assets/guide.gif 图文操作指引 + 无障碍列表项描述 res/values/strings.xml access_desc",
      "trigger_event": "跳转设置前后与设置页内持续可见",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please click the button in the top right corner.\n\nTurn on accessibility to better protect your phone from viruses.\n\nPlease feel free to open.",
      "shown_text_zh": "请点击右上角的按钮。开启无障碍，以更好地保护您的手机免受病毒侵害。请放心开启。",
      "user_action_requested": "要求用户点击右上角按钮并开启无障碍开关，无取消/跳过说明",
      "code_anchor": "#1 file:assets/guide.gif / #1 file:res/values/strings.xml#L4-L8 / #1 file:res/xml/config.xml#L2-L3"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.inter.obfuscated.an#a(Context) 读 Settings$Secure 判定 → 未授权时再次调用 an#b(Context)",
      "trigger_event": "读取 accessibility_enabled 与 enabled_accessibility_services，用 toLowerCase().contains(packageName) 判定；返回 false 即重跳",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "accessibility_enabled / enabled_accessibility_services",
      "shown_text_zh": "以系统设置项作为闸门，未授权则循环回到无障碍列表页",
      "user_action_requested": "用户返回或拒绝后仍被重新送入设置页，无退出路径",
      "code_anchor": "com.inter.obfuscated.an#a(Context)"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.services.AccService#onAccessibilityEvent → com.axl.mngp.a#a → 二阶段 setAccessEvent；节点操作为 com.inter.obfuscated.an 各重载",
      "trigger_event": "无障碍事件回调（AccessibilityEvent）与 onInterrupt",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "setAccessEvent / setAccessInterrupt",
      "shown_text_zh": "接管全部无障碍事件，并对当前窗口节点执行点击、手势与文本填充",
      "user_action_requested": "无，完全后台自动执行",
      "code_anchor": "com.services.AccService#onAccessibilityEvent / com.axl.mngp.a#a / com.inter.obfuscated.an#a(AccessibilityService,String)"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：res/values/strings.xml 中 @string/access_desc（经 res/xml/config.xml android:description 引用）",
    "系统无障碍服务名称：@string/access_name = SystemSecurityServices（同时作为 application android:label）",
    "assets/guide.gif：图文操作指引素材，展示点击右上角按钮开启开关的步骤",
    "未发现本地 HTML/WebView 教学页、未发现确认的悬浮窗遮罩层、未发现不可取消的自定义 AlertDialog（引导文案全部寄生于系统无障碍页）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please click the button in the top right corner.\n\nTurn on accessibility to better protect your phone from viruses.\n\nPlease feel free to open.",
      "text_zh": "请点击右上角的按钮。开启无障碍，以更好地保护您的手机免受病毒侵害。请放心开启。",
      "source_location": "res/values/strings.xml key=access_desc（由 res/xml/config.xml android:description 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "SystemSecurityServices",
      "text_zh": "系统安全服务（伪造的系统级安全组件名称）",
      "source_location": "res/values/strings.xml key=access_name（application android:label 与 service android:label）",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "an#a(Context) 通过 Settings$Secure 的 accessibility_enabled 与 enabled_accessibility_services 判定本包是否已授权，返回 false 时由 an#b(Context) 再次 startActivity(ACTION_ACCESSIBILITY_SETTINGS)，用户返回或拒绝后被重新送入系统无障碍列表页，无退出或降级分支。",
    "overlay_or_fake_settings": "未发现叠层遮罩、全屏悬浮窗或高仿无障碍开关页；SYSTEM_ALERT_WINDOW 权限已声明但未定位到对应叠层实现，引导依赖系统无障碍页本身与 guide.gif 图文说明。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=21，未发现跳转 ACTION_APPLICATION_DETAILS_SETTINGS 的受限设置分步教学，也未发现 Session 安装器绕过。",
    "post_grant_anti_removal": "未发现监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；但获权后 an 类具备 performAction(16) 自动点击与 dispatchGesture 坐标手势能力，可用于静默点击确认类界面。",
    "benign_graceful_degradation": "无。不存在手动模式、ADB 引导或仅观看模式等替代路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 com.axl.mngp.dibd 后立即拉起采集，并以监测到 Activity 切换为 android.settings.ACCESSIBILITY_SETTINGS（settings 包无障碍页）作为关键锚点；用户从设置页返回时再次触发同一锚点，即可验证拒权重跳循环。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转后的系统无障碍服务列表页",
        "page_identifier": "包名 com.android.settings、界面含无障碍服务列表且出现条目 SystemSecurityServices",
        "why_most_useful": "该页同时给出应用宣称身份与用户被要求执行的动作，是判定诱导授权最直接的一帧",
        "observable_utg_signals": ["列表项文本 SystemSecurityServices", "列表项描述含 protect your phone from viruses", "存在可点击开关控件且当前为关闭态"]
      },
      {
        "page_role": "拒权后重跳循环验证页",
        "page_identifier": "连续两次进入 com.android.settings 无障碍页，间隔内无用户主动操作",
        "why_most_useful": "区分『一次性引导』与『强制循环』，是定性 coercion 的关键",
        "observable_utg_signals": ["两次无障碍设置页的 Activity 出现时间戳", "返回键后无本应用降级页出现", "循环次数≥2"]
      },
      {
        "page_role": "获权后的自动点击现场",
        "page_identifier": "本应用无障碍开关被打开后，前台窗口节点被 performAction/dispatchGesture 触发点击",
        "why_most_useful": "证明权限被用于代替用户操作，而非宣称的病毒防护",
        "observable_utg_signals": ["非用户输入产生的点击事件", "窗口内容在无触摸输入下发生变化", "剪贴板内容被写入并粘贴到输入框"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案寄生于系统无障碍页而非应用自有页面，若仅在应用进程内采集 UTG 会漏掉核心引导帧，必须覆盖 com.android.settings 前台窗口；另应用无自有引导界面，冷启动后立即跳转，启动瞬间画面极短易漏采。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.axl.mngp.dibd#onCreate",
    "com.axl.mngp.f#b",
    "com.axl.mngp.h#a",
    "com.inter.interfaces.InterInterfaceImpl#startA",
    "com.inter.obfuscated.an#b",
    "com.inter.obfuscated.an#a(Context)"
  ]
}
```

</details>
