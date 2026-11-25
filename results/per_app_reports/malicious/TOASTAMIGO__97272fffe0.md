# MR_058__97272fffe0｜TOASTAMIGO — Smart AppLocker

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：177.9s

## 1. 一句话核心结论

- **核心申请方式**：冷启动零步检测本包无障碍服务，未启用即弹出不可取消的 Attention 说明框，确认后跳系统无障碍设置并立刻用 TYPE_SYSTEM_ALERT 全屏半透明 GIF 教学遮罩覆盖，取消则直接退出应用并循环重弹。
- **静态可见性说明**：无障碍引导全链路（检测、弹窗、跳转、遮罩）均在 classes.dex 明文可读，无加壳、无加密载荷、无远端 HTML；跳转目标另存在 com.amigo.asframework.task.ASTask 云控任务通道（accessibility/detail/usage_access），但冷启动实际路径使用硬编码 Intent，不依赖云端下发，故静态完整可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `97272fffe08226996d1ccffc7bc6d6e77125117dc5244504790de5c161bba4ee` |
| 包名 / 年份 | `com.goami.applocker` / 2017 |
| 家族 / 品类 | **TOASTAMIGO**（同池样本数：44） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/k/toast-overlay-weaponized-install-android-malware-single-attack-chain.html |
| 桌面显示名 | Smart AppLocker |
| 引导页宣称品牌/身份 | Smart AppLocker（应用锁工具，自称 App Locker / Appz Lock Preference） |
| 系统无障碍列表服务名 | App Locker（服务名 com.goami.applocker.AppLocker.MyAccessibilityServiceTmp，系统列表描述为 "The service for the purpose of Android 4.0.3 and above to lock apps easily."） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务描述与正文把申请理由弱化为“Android 4.0.3 以上方便锁应用”，但实际配置 typeAllMask、canRetrieveWindowContent=true、canRequestFilterKeyEvents=true，并可执行 PERFORM_GLOBAL_ACTION；服务类继承 com.luna.powersaver.gp.service.a（与包名 goami 不一致的 luna/powersaver 命名）；正文存在排版瑕疵 ".Please" 与多余空格；Android 5.0+ 通过 setCancelable(false) 屏蔽取消。 |
| 无障碍服务类名 | `com.goami.applocker.AppLocker.MyAccessibilityServiceTmp` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.miui.home,com.umiplus.screenlock,com.android.vending,com.android.settings,com.android.packageinstaller,com.google.android.packageinstaller,com.sec.android.app.launcher,com.bbk.launcher2,com.oppo.launcher |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | The service for the purpose of Android 4.0.3 and above to lock apps easily. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.goami.applocker.AppLocker.ApplicationListActivity（唯一 LAUNCHER Activity） | onCreate 中 Build.VERSION.SDK_INT >= 15 时调用 d()，d() 先调 g() 用 getEnabledAccessibilityServiceList(-1) 比对 "com.goami.applocker/.AppLocker.MyAccessibilityServiceTmp"，未命中则调 f() | 原生Dialog | **原文**：Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.<br>**译注**：注意 / 本设备版本高于 Android 4.0.3，请前往 设置→无障碍服务→App Locker 并将其打开。 | 点击确认前往开启；另有取消按钮，但 setCancelable(SDK_INT < 20) 使 Android 5.0+ 无法通过返回键或点击外部关闭 | `com.goami.applocker.AppLocker.ApplicationListActivity#f / #d / #g，文案 res/values/strings.xml alp_42447968_cmd_Attention、alp_42447968_cmd_android_m_above` |
| 2 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 确认按钮回调 ApplicationListActivity$4.a(Dialog) 调用 e()，执行 startActivity(r)（r 为静态字段 new Intent("android.settings.ACCESSIBILITY_SETTINGS")） | 系统无障碍页 | 无 | 在系统无障碍列表中找到 App Locker 服务并打开开关 | `com.goami.applocker.AppLocker.ApplicationListActivity#e，字段 ApplicationListActivity.r` |
| 3 | 遮罩叠层指引 | WindowManager 全屏悬浮窗（inflate res/layout/hint_set_accessibility.xml） | e() 在 startActivity 之后立即 addView，LayoutParams type=2005(TYPE_SYSTEM_ALERT)、flags=526208、MATCH_PARENT、format=1 | 悬浮窗Overlay | **原文**：Get It<br>**译注**：背景为 #aa000000 半透明全屏黑，中间播放 GIF 操作演示 pic_accessibility_guide（0.9 屏宽，1000ms 循环），下方蓝色渐变按钮“Get It” | 观看演示动画并点击 Get It 关闭遮罩（点击后仅 removeView，不做任何校验） | `com.goami.applocker.AppLocker.ApplicationListActivity#e、ApplicationListActivity$3#onClick、res/layout/hint_set_accessibility.xml` |
| 4 | 拒权反馈循环 | ApplicationListActivity 自身 finish() 后返回桌面 | 取消按钮回调 ApplicationListActivity$5.a 执行 finish()；用户重开应用时 onCreate 再走 d()，onResume 经 k.a(...,800L) 延时 800ms 执行 $2.run 复查 g() | 原生Activity | 无 | 无替代路径：只能选择开启无障碍，或退出应用 | `com.goami.applocker.AppLocker.ApplicationListActivity$5#a、ApplicationListActivity#onResume、ApplicationListActivity$2#run` |
| 5 | 获权后动作 | DetectorService（com.goami.applocker.AppLocker.Service.DetectorService） | d() 中 g() 返回 true 后跳过 f()，依次 i() stopService 与 h() startService 重启 DetectorService | 原生Activity | 无 | 无，自动进入功能界面 | `com.goami.applocker.AppLocker.ApplicationListActivity#d、#h、#i` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动自定义 AlertDialog（com.goami.applocker.AppLocker.a.b）：标题“Attention”+正文“This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.”
- 系统无障碍服务列表项说明：res/xml/phone_accessibility.xml 的 android:description = @string/accessibility_service_description（“The service for the purpose of Android 4.0.3 and above to lock apps easily.”）
- 跳转系统设置后叠放的 TYPE_SYSTEM_ALERT 全屏悬浮窗 res/layout/hint_set_accessibility.xml：半透明黑背景 + GIF 演示图 drawable/pic_accessibility_guide + 按钮文本 @string/str_get_it（“Get It”）
- res/values/strings.xml 中未在主链路引用的备用提示：alp_42447968_cmd_android_m_above_toast（“Find Setting->AccessibilityService->App Locker and Open it.”）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Attention | 注意 | `res/values/strings.xml key=alp_42447968_cmd_Attention（供 ApplicationListActivity#f 对话框标题）` | 受限设置分步教学 |
| en | This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. | 本设备版本高于 Android 4.0.3，请前往 设置→无障碍服务→App Locker 并将其打开。 | `res/values/strings.xml key=alp_42447968_cmd_android_m_above（ApplicationListActivity#f 对话框正文）` | 受限设置分步教学 |
| en | The service for the purpose of Android 4.0.3 and above to lock apps easily. | 该服务用于在 Android 4.0.3 及以上版本中方便地锁定应用。 | `res/values/strings.xml key=accessibility_service_description，经 res/xml/phone_accessibility.xml 显示于系统无障碍列表` | 隐私承诺 |
| en | Get It | 知道了 / 立即获取 | `res/values/strings.xml key=str_get_it（res/layout/hint_set_accessibility.xml 悬浮遮罩按钮）` | 受限设置分步教学 |
| en | Find Setting->AccessibilityService->App Locker and Open it. | 找到 设置→无障碍服务→App Locker 并打开它。 | `res/values/strings.xml key=alp_42447968_cmd_android_m_above_toast（备用 Toast 文案）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：点击取消即 finish() 退出应用，用户无法进入任何功能界面；重新启动时 onCreate 的 d() 与 onResume 中 k.a(...,800L) 延时 800ms 的 $2.run 再次调用 g() 复查，未启用则重复弹窗，构成启动即循环。
- **遮罩叠层 / 高仿系统设置页**：跳转系统无障碍设置后立即用 WindowManager.addView 叠放 type=2005（TYPE_SYSTEM_ALERT）全屏悬浮窗，背景 #aa000000 半透明黑，内含 GIF 操作演示与“Get It”按钮；是覆盖真实系统设置页的教学遮罩，非高仿系统开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=24，未涉及 Android 13 受限设置或 Session 安装器绕过；APPLICATION_DETAILS_SETTINGS 跳转能力存在于 com.amigo.asframework.task.ASTask 云控通道，但本引导链未使用）
- **获权后即时行为与防撤权机制**：获权后无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权；但无障碍服务继承 com.luna.powersaver.gp.service.a 并接入 ASTask 云控任务框架（PERFORM_GLOBAL_ACTION、WATCH_SETTINGS、WATCH_PKG_INSTALLER 能力位存在于 DEX 线索中），属潜在反撤权能力，本次未在引导链中直接触发。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 ApplicationListActivity 后 800ms 内出现首个 Dialog（onCreate 的 d() 与 onResume 的 800ms 延时任务会先后触发），以及紧随其后的 startActivity("android.settings.ACCESSIBILITY_SETTINGS") —— 监测到该 Intent 跳转即为最佳抓取瞬间，因为同一方法内会立刻压栈全屏悬浮窗。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：主要引导文案均为可读文本，UTG 可完整提取；但第三段遮罩的核心教学信息完全承载于 GIF 动画 drawable/pic_accessibility_guide（纯图无文本），需 OCR/录屏才能判读其演示内容是否教授具体开关路径。另注意该样本未加壳，运行期 UTG 不受静态保护影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 包名 com.goami.applocker 的自定义 Dialog，标题“Attention”，正文含“Go Setting->AccessibilityService->App Locker”，两个按钮且返回键无效 | 证明零步强制索取无障碍，是判定诱导而非按需触发的关键证据 | Dialog 文本“Attention”与“Android 4.0.3”；返回键按下后 Dialog 不消失（Android 5.0+）；取消按钮触发 Activity finish 回桌面 |
| **设置页后压栈遮罩页** | TYPE_SYSTEM_ALERT 全屏悬浮窗，半透明黑底 + GIF 动画 + 蓝色“Get It”按钮，覆盖在系统无障碍设置之上 | 证明应用在系统设置界面之上叠层接管操作路径，且遮罩关闭不做任何真实校验 | 页面层级出现非系统 Window（type 2005）；遮罩文本“Get It”；遮罩背景 #aa000000 半透明且覆盖设置列表 |
| **系统无障碍服务列表项** | 设置→无障碍 中名为 App Locker 的服务项，描述“The service for the purpose of Android 4.0.3 and above to lock apps easily.” | 核对系统侧呈现的身份与描述是否弱化真实权限能力 | 服务项显示名 App Locker；描述文本与包名 com.goami.applocker 的对应关系 |
| **获权后功能页** | ApplicationListActivity 应用列表，无任何提示直接可用 | 对比获权前后行为差异，确认权限是使用前提而非功能需要 | 无弹窗直接进入列表；DetectorService 前台/后台服务启动 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.goami.applocker.AppLocker.ApplicationListActivity#f`
- `com.goami.applocker.AppLocker.ApplicationListActivity#e`
- `com.goami.applocker.AppLocker.ApplicationListActivity#g`
- `com.goami.applocker.AppLocker.ApplicationListActivity$5#a`
- `res/layout/hint_set_accessibility.xml`
- `res/xml/phone_accessibility.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **入口固定、零步触发**：应用唯一的 LAUNCHER Activity 是 `ApplicationListActivity`；其 `onCreate` 在 `SDK_INT >= 15` 时直接进入权限自检，不经过任何引导页或功能介绍。
- **检测方式**：`g()` 用 `AccessibilityManager.getEnabledAccessibilityServiceList(-1)` 比对 `com.goami.applocker/.AppLocker.MyAccessibilityServiceTmp`，只判断本包服务是否在启用列表中。
- **第一段引导（原生 Dialog）**：未启用即 `f()` 弹出自定义对话框 `com.goami.applocker.AppLocker.a.b`，标题 "Attention"、正文为"设备版本高于 Android 4.0.3，请去 设置→无障碍→App Locker 打开"，并 `setCancelable(SDK_INT < 20)`，即 Android 5.0+ 上返回键/点击外部均无效。
- **第二段引导（跳系统设置）**：确认按钮回调 `$4.a` 先 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，把用户直接送进系统无障碍列表，没有任何前置解释页或 WebView。
- **第三段引导（全屏遮罩接管）**：跳转后同一方法内立即用 `WindowManager.addView`，以 `type=2005`（TYPE_SYSTEM_ALERT）、`flags=526208`、`MATCH_PARENT` 叠放 `hint_set_accessibility.xml`（背景 `#aa000000` 半透明黑），内容为 GIF 演示动画 `pic_accessibility_guide` + "Get It" 按钮；遮罩覆盖在系统无障碍页之上，是操作教学叠层，不是伪造系统开关页。
- **拒绝即被阻断**：取消回调 `$5.a` 直接 `finish()` 退出，用户无法使用任何功能；重开应用时 `onCreate` 与 `onResume` 的 800ms 延时任务 `$2.run` 再次复查 `g()`，未启用则重复弹窗，形成无跳过、无降级的闭环。
- **获权后动作**：`d()` 中 `g()` 返回真后跳过弹窗，转去 `stopService/startService DetectorService` 启动锁屏检测服务，说明无障碍权限并非"锁应用"所必需，而是为后续窗口内容读取与全局操作能力铺垫。
- **系统列表中的说明文字**：`res/xml/phone_accessibility.xml` 的 `android:description` 为 "The service for the purpose of Android 4.0.3 and above to lock apps easily."，同时配置 `typeAllMask`、`canRetrieveWindowContent=true`、`canRequestFilterKeyEvents=true`，与说明文字所暗示的"方便锁应用"能力范围严重不匹配。
- **静态可见性**：全链路均在 `classes.dex` 明文可见，无加壳、无远端 HTML、无加密载荷；跳转目标由 `com.amigo.asframework.task.ASTask#getIntent` 的 `"accessibility"/"detail"/"usage_access"` 分支提供（云控任务通道），但本应用实际冷启动路径使用硬编码 Intent，不依赖云端下发。

## 引导链（运行期 UTG 视角）

| 步骤 | 载体 | 触发 | 用户请求 |
|---|---|---|---|
| 1 | 原生 Dialog `AppLocker.a.b` | `onCreate → d() → g()` 为假 | 点确认或取消（Android 5.0+ 不可取消） |
| 2 | 系统无障碍设置页 | `$4.a` 点击确认 | 在系统列表中找到 App Locker 并打开 |
| 3 | TYPE_SYSTEM_ALERT 全屏 GIF 遮罩 | `e()` 紧随 `startActivity` | 观看演示后点 "Get It" 关闭 |
| 4 | 退出 | `$5.a` 点击取消 | 再次打开应用，回到步骤 1 |

## 已登记风险

R-001（high / deceptive_behavior）：冷启动强制无障碍引导三段式索取，证据图 EG-4D1D9BE6C207。

关键锚点：[ApplicationListActivity.f()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity#f>)、[ApplicationListActivity.e()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity#e>)、[hint_set_accessibility.xml](<resource-unit:#1 file:res/layout/hint_set_accessibility.xml>)、[phone_accessibility.xml](<resource-unit:#1 file:res/xml/phone_accessibility.xml>)、[strings.xml (lines 65-70)](<resource-unit:#1 file:res/values/strings.xml#L65-L70>)。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（检测、弹窗、跳转、遮罩）均在 classes.dex 明文可读，无加壳、无加密载荷、无远端 HTML；跳转目标另存在 com.amigo.asframework.task.ASTask 云控任务通道（accessibility/detail/usage_access），但冷启动实际路径使用硬编码 Intent，不依赖云端下发，故静态完整可见。",
  "summary_one_liner": "冷启动零步检测本包无障碍服务，未启用即弹出不可取消的 Attention 说明框，确认后跳系统无障碍设置并立刻用 TYPE_SYSTEM_ALERT 全屏半透明 GIF 教学遮罩覆盖，取消则直接退出应用并循环重弹。",
  "disguise_identity": {
    "app_display_name": "Smart AppLocker",
    "claimed_brand_or_persona": "Smart AppLocker（应用锁工具，自称 App Locker / Appz Lock Preference）",
    "a11y_service_label": "App Locker（服务名 com.goami.applocker.AppLocker.MyAccessibilityServiceTmp，系统列表描述为 \"The service for the purpose of Android 4.0.3 and above to lock apps easily.\"）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务描述与正文把申请理由弱化为“Android 4.0.3 以上方便锁应用”，但实际配置 typeAllMask、canRetrieveWindowContent=true、canRequestFilterKeyEvents=true，并可执行 PERFORM_GLOBAL_ACTION；服务类继承 com.luna.powersaver.gp.service.a（与包名 goami 不一致的 luna/powersaver 命名）；正文存在排版瑕疵 \".Please\" 与多余空格；Android 5.0+ 通过 setCancelable(false) 屏蔽取消。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.goami.applocker.AppLocker.ApplicationListActivity（唯一 LAUNCHER Activity）",
      "trigger_event": "onCreate 中 Build.VERSION.SDK_INT >= 15 时调用 d()，d() 先调 g() 用 getEnabledAccessibilityServiceList(-1) 比对 \"com.goami.applocker/.AppLocker.MyAccessibilityServiceTmp\"，未命中则调 f()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "shown_text_zh": "注意 / 本设备版本高于 Android 4.0.3，请前往 设置→无障碍服务→App Locker 并将其打开。",
      "user_action_requested": "点击确认前往开启；另有取消按钮，但 setCancelable(SDK_INT < 20) 使 Android 5.0+ 无法通过返回键或点击外部关闭",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity#f / #d / #g，文案 res/values/strings.xml alp_42447968_cmd_Attention、alp_42447968_cmd_android_m_above"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "确认按钮回调 ApplicationListActivity$4.a(Dialog) 调用 e()，执行 startActivity(r)（r 为静态字段 new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍服务列表页，用户需在列表中找到 “App Locker” 项并手动开启",
      "user_action_requested": "在系统无障碍列表中找到 App Locker 服务并打开开关",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity#e，字段 ApplicationListActivity.r"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WindowManager 全屏悬浮窗（inflate res/layout/hint_set_accessibility.xml）",
      "trigger_event": "e() 在 startActivity 之后立即 addView，LayoutParams type=2005(TYPE_SYSTEM_ALERT)、flags=526208、MATCH_PARENT、format=1",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Get It",
      "shown_text_zh": "背景为 #aa000000 半透明全屏黑，中间播放 GIF 操作演示 pic_accessibility_guide（0.9 屏宽，1000ms 循环），下方蓝色渐变按钮“Get It”",
      "user_action_requested": "观看演示动画并点击 Get It 关闭遮罩（点击后仅 removeView，不做任何校验）",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity#e、ApplicationListActivity$3#onClick、res/layout/hint_set_accessibility.xml"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "ApplicationListActivity 自身 finish() 后返回桌面",
      "trigger_event": "取消按钮回调 ApplicationListActivity$5.a 执行 finish()；用户重开应用时 onCreate 再走 d()，onResume 经 k.a(...,800L) 延时 800ms 执行 $2.run 复查 g()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "应用直接退出，无任何降级或手动模式；再次启动时同一弹窗重复出现，形成闭环",
      "user_action_requested": "无替代路径：只能选择开启无障碍，或退出应用",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity$5#a、ApplicationListActivity#onResume、ApplicationListActivity$2#run"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "DetectorService（com.goami.applocker.AppLocker.Service.DetectorService）",
      "trigger_event": "d() 中 g() 返回 true 后跳过 f()，依次 i() stopService 与 h() startService 重启 DetectorService",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不再显示任何提示，直接进入应用列表并启动后台锁屏检测服务",
      "user_action_requested": "无，自动进入功能界面",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity#d、#h、#i"
    }
  ],
  "text_presentation_locations": [
    "冷启动自定义 AlertDialog（com.goami.applocker.AppLocker.a.b）：标题“Attention”+正文“This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.”",
    "系统无障碍服务列表项说明：res/xml/phone_accessibility.xml 的 android:description = @string/accessibility_service_description（“The service for the purpose of Android 4.0.3 and above to lock apps easily.”）",
    "跳转系统设置后叠放的 TYPE_SYSTEM_ALERT 全屏悬浮窗 res/layout/hint_set_accessibility.xml：半透明黑背景 + GIF 演示图 drawable/pic_accessibility_guide + 按钮文本 @string/str_get_it（“Get It”）",
    "res/values/strings.xml 中未在主链路引用的备用提示：alp_42447968_cmd_android_m_above_toast（“Find Setting->AccessibilityService->App Locker and Open it.”）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Attention",
      "text_zh": "注意",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_Attention（供 ApplicationListActivity#f 对话框标题）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "本设备版本高于 Android 4.0.3，请前往 设置→无障碍服务→App Locker 并将其打开。",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_android_m_above（ApplicationListActivity#f 对话框正文）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The service for the purpose of Android 4.0.3 and above to lock apps easily.",
      "text_zh": "该服务用于在 Android 4.0.3 及以上版本中方便地锁定应用。",
      "source_location": "res/values/strings.xml key=accessibility_service_description，经 res/xml/phone_accessibility.xml 显示于系统无障碍列表",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Get It",
      "text_zh": "知道了 / 立即获取",
      "source_location": "res/values/strings.xml key=str_get_it（res/layout/hint_set_accessibility.xml 悬浮遮罩按钮）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Find Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "找到 设置→无障碍服务→App Locker 并打开它。",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_android_m_above_toast（备用 Toast 文案）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "点击取消即 finish() 退出应用，用户无法进入任何功能界面；重新启动时 onCreate 的 d() 与 onResume 中 k.a(...,800L) 延时 800ms 的 $2.run 再次调用 g() 复查，未启用则重复弹窗，构成启动即循环。",
    "overlay_or_fake_settings": "跳转系统无障碍设置后立即用 WindowManager.addView 叠放 type=2005（TYPE_SYSTEM_ALERT）全屏悬浮窗，背景 #aa000000 半透明黑，内含 GIF 操作演示与“Get It”按钮；是覆盖真实系统设置页的教学遮罩，非高仿系统开关页。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=24，未涉及 Android 13 受限设置或 Session 安装器绕过；APPLICATION_DETAILS_SETTINGS 跳转能力存在于 com.amigo.asframework.task.ASTask 云控通道，但本引导链未使用）",
    "post_grant_anti_removal": "获权后无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权；但无障碍服务继承 com.luna.powersaver.gp.service.a 并接入 ASTask 云控任务框架（PERFORM_GLOBAL_ACTION、WATCH_SETTINGS、WATCH_PKG_INSTALLER 能力位存在于 DEX 线索中），属潜在反撤权能力，本次未在引导链中直接触发。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 ApplicationListActivity 后 800ms 内出现首个 Dialog（onCreate 的 d() 与 onResume 的 800ms 延时任务会先后触发），以及紧随其后的 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\") —— 监测到该 Intent 跳转即为最佳抓取瞬间，因为同一方法内会立刻压栈全屏悬浮窗。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "包名 com.goami.applocker 的自定义 Dialog，标题“Attention”，正文含“Go Setting->AccessibilityService->App Locker”，两个按钮且返回键无效",
        "why_most_useful": "证明零步强制索取无障碍，是判定诱导而非按需触发的关键证据",
        "observable_utg_signals": ["Dialog 文本“Attention”与“Android 4.0.3”", "返回键按下后 Dialog 不消失（Android 5.0+）", "取消按钮触发 Activity finish 回桌面"]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "TYPE_SYSTEM_ALERT 全屏悬浮窗，半透明黑底 + GIF 动画 + 蓝色“Get It”按钮，覆盖在系统无障碍设置之上",
        "why_most_useful": "证明应用在系统设置界面之上叠层接管操作路径，且遮罩关闭不做任何真实校验",
        "observable_utg_signals": ["页面层级出现非系统 Window（type 2005）", "遮罩文本“Get It”", "遮罩背景 #aa000000 半透明且覆盖设置列表"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍 中名为 App Locker 的服务项，描述“The service for the purpose of Android 4.0.3 and above to lock apps easily.”",
        "why_most_useful": "核对系统侧呈现的身份与描述是否弱化真实权限能力",
        "observable_utg_signals": ["服务项显示名 App Locker", "描述文本与包名 com.goami.applocker 的对应关系"]
      },
      {
        "page_role": "获权后功能页",
        "page_identifier": "ApplicationListActivity 应用列表，无任何提示直接可用",
        "why_most_useful": "对比获权前后行为差异，确认权限是使用前提而非功能需要",
        "observable_utg_signals": ["无弹窗直接进入列表", "DetectorService 前台/后台服务启动"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "主要引导文案均为可读文本，UTG 可完整提取；但第三段遮罩的核心教学信息完全承载于 GIF 动画 drawable/pic_accessibility_guide（纯图无文本），需 OCR/录屏才能判读其演示内容是否教授具体开关路径。另注意该样本未加壳，运行期 UTG 不受静态保护影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "LURE_PRIVACY_GUARANTEE_CLAIM"
  ],
  "code_anchors": [
    "com.goami.applocker.AppLocker.ApplicationListActivity#f",
    "com.goami.applocker.AppLocker.ApplicationListActivity#e",
    "com.goami.applocker.AppLocker.ApplicationListActivity#g",
    "com.goami.applocker.AppLocker.ApplicationListActivity$5#a",
    "res/layout/hint_set_accessibility.xml",
    "res/xml/phone_accessibility.xml"
  ]
}
```

</details>
