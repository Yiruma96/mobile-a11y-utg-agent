# MR_098__79b0f540de｜TOASTAMIGO — Smart AppLocker

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：126.1s

## 1. 一句话核心结论

- **核心申请方式**：以「Smart AppLocker 应用锁」为外壳，冷启动/回前台 800ms 后静默自检无障碍服务，未启用即弹出 Android 5.0+ 上不可取消的 Attention 引导框，确认后跳系统无障碍设置并立刻叠加 TYPE_SYSTEM_ALERT 全屏半透明遮罩 + GIF 分步教程，关闭遮罩返回后再次检测形成无跳过按钮的循环引导，且申请的是全窗口内容读取与按键过滤能力。
- **静态可见性说明**：无障碍引导全链路（自检、引导框、跳转、悬浮遮罩、GIF 教程、循环判定）均在 classes.dex 与 res/ 中完整静态可见；无加壳、无 AES 密文、无远端 HTML 承载引导文案。仅 GIF 教程图 pic_accessibility_guide 为图片资源，其内部步骤文字需 OCR 才能逐字提取。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `79b0f540de2b82075f42725e8ba8ccfc2748ff6f7826bff7920ce18904d14983` |
| 包名 / 年份 | `com.agomi.applocker` / 2017 |
| 家族 / 品类 | **TOASTAMIGO**（同池样本数：44） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/k/toast-overlay-weaponized-install-android-malware-single-attack-chain.html |
| 桌面显示名 | Smart AppLocker |
| 引导页宣称品牌/身份 | Smart AppLocker（应用锁 / App Locker，宣称用于「轻松锁定应用」） |
| 系统无障碍列表服务名 | Smart AppLocker（服务未声明 android:label，系统无障碍列表回退显示应用名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未声明 android:label，系统列表直接沿用应用名以维持「应用锁」形象；android:description 仅一句良性用途说明，未披露 typeAllMask 全窗口内容读取与 canRequestFilterKeyEvents 按键拦截；服务类名以 Tmp 结尾伪装为临时占位，实际继承捆绑的 com.luna.powersaver.gp.service.a 省电模块基类，核心逻辑位于混淆包 com.luna.powersaver.gp / com.amigo.faldaldk 下 |
| 无障碍服务类名 | `com.goami.applocker.AppLocker.MyAccessibilityServiceTmp` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.miui.home,com.umiplus.screenlock,com.android.vending,com.android.settings,com.android.packageinstaller,com.google.android.packageinstaller,com.sec.android.app.launcher,com.bbk.launcher2,com.oppo.launcher |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | The service for the purpose of Android 4.0.3 and above to lock apps easily. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.goami.applocker.AppLocker.ApplicationListActivity（LAUNCHER，singleInstance，label=@string/app_name） | onResume() 中 k.a(new ApplicationListActivity$2(this), 800L) 起 800ms 延时任务 | 原生Activity | **原文**：无（本步为应用列表主界面，不呈现引导文案）<br>**译注**：应用锁主列表界面，用户此时尚看不到任何权限提示 | 无需操作；仅需打开应用或从后台返回前台 | `com.goami.applocker.AppLocker.ApplicationListActivity.onResume` |
| 2 | 业务功能触发 | ApplicationListActivity$2.run → ApplicationListActivity.g() | 800ms 定时到点；getEnabledAccessibilityServiceList(-1) 比对 "com.agomi.applocker/com.goami.applocker.AppLocker.MyAccessibilityServiceTmp" 是否已启用，未启用则调用 f() | 不可静态还原（无界面，纯后台判定） | 无 | 无 | `com.goami.applocker.AppLocker.ApplicationListActivity.g` |
| 3 | 引导说明页 | 自定义 Dialog com.goami.applocker.AppLocker.a.b（由 ApplicationListActivity.f() 创建并 show） | f() 检测到服务未启用，构造 dialog：标题 getString(2131165276)、正文 getString(2131165277)、setCancelable(Build.VERSION.SDK_INT < 20) | 原生Dialog | **原文**：Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.<br>**译注**：注意 / 本设备版本高于 Android 4.0.3，请前往 设置->无障碍服务->App Locker 并将其开启。 | 点击确认按钮前往设置（$4 回调）；Android 5.0 及以上 setCancelable(false)，返回键与点击外部均无法关闭 | `com.goami.applocker.AppLocker.ApplicationListActivity.f / res/values/strings.xml#L94-L95 (alp_42447968_cmd_Attention, alp_42447968_cmd_android_m_above)` |
| 4 | 跳受限设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（Intent 常量 ApplicationListActivity.r） | ApplicationListActivity$4.a(Dialog) 先调用 e()，e() 内 startActivity(r) 跳转系统无障碍设置页 | 系统无障碍页 | **原文**：无（应用自身不渲染该页，仅发起 Intent）<br>**译注**：跳转到系统「无障碍」设置列表，用户需在此找到 Smart AppLocker 并手动打开开关 | 在系统无障碍列表中找到 Smart AppLocker 并开启 | `com.goami.applocker.AppLocker.ApplicationListActivity.e / ApplicationListActivity$4.a` |
| 5 | 遮罩叠层指引 | WindowManager 叠加视图 res/layout/hint_set_accessibility.xml（TYPE_SYSTEM_ALERT=2005，-1×-1，flags=526208，背景 #aa000000） | e() 在 startActivity 后立即 addView 全屏遮罩；内部 GifImageView 加载 pic_accessibility_guide 并 cVar.a(1000).start() 播放 | 悬浮窗Overlay | **原文**：Get It（按钮文本 str_get_it；其余步骤说明以 GIF 动图形式呈现，无文本）<br>**译注**：半透明全屏遮罩上循环播放 GIF 教程演示如何开启无障碍，底部「知道了/开始」按钮 | 观看 GIF 教程后点击 Get It 关闭遮罩（$3.onClick 仅 removeView），无取消或跳过分支 | `com.goami.applocker.AppLocker.ApplicationListActivity.e / res/layout/hint_set_accessibility.xml / res/values/strings.xml#L183 (str_get_it)` |
| 6 | 拒权反馈循环 | ApplicationListActivity（遮罩关闭后回到本 Activity）→ onResume → $2.run → g() → f() | 遮罩按钮 removeView 后 Activity 重新获得焦点，onResume 再次启动 800ms 延时检测；若服务仍未启用则重新弹框并再次跳设置 | 原生Dialog | **原文**：Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.<br>**译注**：再次弹出同一 Attention 提示，用户不授权即无法正常使用应用列表功能 | 只能再次前往设置开启，无「以后再说」「跳过」等退出路径（SDK≥20 时弹框不可取消） | `com.goami.applocker.AppLocker.ApplicationListActivity$3.onClick → ApplicationListActivity.onResume → ApplicationListActivity$2.run` |
| 7 | 获权后动作 | com.goami.applocker.AppLocker.MyAccessibilityServiceTmp（extends com.luna.powersaver.gp.service.a），onServiceConnected 起开始接收事件 | 用户在系统无障碍列表勾选服务后，系统绑定服务并回调 onServiceConnected；此后 $2.run 的 g() 返回 true，不再弹引导 | 不可静态还原（服务运行态，无界面） | 无 | 无 | `com.goami.applocker.AppLocker.MyAccessibilityServiceTmp.onServiceConnected / res/xml/phone_accessibility.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- ApplicationListActivity.f() 弹出的自定义原生 Dialog com.goami.applocker.AppLocker.a.b：标题「Attention」、正文「This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.」（来源 res/values/strings.xml 的 alp_42447968_cmd_Attention / alp_42447968_cmd_android_m_above）
- 跳转 ACCESSIBILITY_SETTINGS 后立即叠加的全屏 TYPE_SYSTEM_ALERT 悬浮窗 res/layout/hint_set_accessibility.xml：背景 #aa000000，内含 GIF 图 res/drawable/pic_accessibility_guide 与按钮文本「Get It」（str_get_it）
- 系统无障碍服务列表条目：服务未设 android:label，显示应用名「Smart AppLocker」；说明文字来自 res/xml/phone_accessibility.xml → @string/accessibility_service_description「The service for the purpose of Android 4.0.3 and above to lock apps easily.」
- Manifest 中 application android:label=@string/app_name（Smart AppLocker），桌面图标与名称与引导流程保持同一「应用锁」身份
- 无本地或远端 HTML/WebView 承载引导文案；GIF 教程图内的分步文字为纯图片内容，需 OCR 提取

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Attention | 注意 | `res/values/strings.xml key=alp_42447968_cmd_Attention（getString(2131165276)）` | 受限设置分步教学 |
| en | This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. | 本设备版本高于 Android 4.0.3。请前往 设置->无障碍服务->App Locker 并将其开启。 | `res/values/strings.xml key=alp_42447968_cmd_android_m_above（getString(2131165277)）` | 受限设置分步教学 |
| en | The service for the purpose of Android 4.0.3 and above to lock apps easily. | 本服务用于在 Android 4.0.3 及以上系统中轻松锁定应用。 | `res/values/strings.xml key=accessibility_service_description（经 res/xml/phone_accessibility.xml android:description 引用，显示于系统无障碍列表）` | 良性透明说明 |
| en | Get It | 知道了 / 开始 | `res/values/strings.xml key=str_get_it（res/layout/hint_set_accessibility.xml 按钮 android:text）` | 受限设置分步教学 |
| en | Smart AppLocker | 智能应用锁 | `res/values/strings.xml key=app_name（AndroidManifest application android:label；无障碍服务未声明 label 时系统列表同样显示此项）` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onResume 每次都以 k.a(..., 800L) 重新起 800ms 延时检测；遮罩 Get It 仅 removeView 回到本 Activity，未授权即再次弹框并再次 startActivity(ACCESSIBILITY_SETTINGS)，形成「关闭遮罩→返回→再弹框→再跳设置」的无限循环；SDK_INT>=20 时 Dialog setCancelable(false)，返回键与点外部均无法取消。
- **遮罩叠层 / 高仿系统设置页**：跳转系统无障碍设置后立即通过 WindowManager 以 type=2005(TYPE_SYSTEM_ALERT)、-1×-1、flags=526208 叠加全屏半透明黑色（#aa000000）遮罩，内嵌循环播放的 GIF 教程与 Get It 按钮，属压在真实系统设置页之上的叠层引导；不是自绘高仿无障碍开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。目标 SDK 为 24，代码中未见引导进入应用详情页右上角菜单允许受限设置，也未见 Session 安装器绕过逻辑（预筛 SESSION_INSTALLER 线索未在本无障碍链路中被调用）。
- **获权后即时行为与防撤权机制**：无。获权后 $2.run 的 g() 返回 true 即停止弹框，未发现自点确认、自授权或在设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；预筛的 PERFORM_GLOBAL_ACTION 未出现在本引导链路。
- **良性降级 / 替代方案**：无。未授权时不存在手动模式、仅观看模式或功能降级路径，唯一分支是「已启用/未启用」。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以「Activity 切换到 com.android.settings/.Settings$AccessibilitySettings（或 Settings$AccessibilitySettingsActivity）」为首要触发点——应用在 startActivity 后同一方法内立刻 addView 全屏 TYPE_SYSTEM_ALERT 遮罩，跳转后 200~1000ms 内截图/UTG 即可同时抓到系统无障碍列表与压在其上的引导遮罩；次选触发点为 ApplicationListActivity 冷启动 onResume 后 800ms 处的自定义 Attention Dialog 出现瞬间。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：GIF 教程图 res/drawable/pic_accessibility_guide 内的分步文字为纯图片内容，UTG 文本树无法提取，需 OCR；遮罩为全屏且覆盖系统设置页，部分设备上会遮挡系统设置节点的可读性，需以窗口层级（WindowManager 多窗口）而非单窗口文本判定。应用未加壳，运行期行为可完整观测；预筛中的 Facebook / Google Play services 文案均属三方 SDK 资源，与引导链路无关，不构成误判干扰。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（跳转前）** | 包名 com.agomi.applocker 的 Dialog，标题文本 Attention，正文含「Please Go Setting->AccessibilityService->App Locker and Open it.」，无「取消/跳过/以后再说」按钮 | 直接证明引导为冷启动即触发且不可取消，是区分「按需说明」与「前置强制」的关键 | 对话框标题文本 Attention；正文含 AccessibilityService 与 App Locker 字样；按钮集合中无取消类文案；返回键无效（SDK>=20） |
| **系统无障碍服务列表页（跳转目标）** | Settings$AccessibilitySettings，列表中出现 Smart AppLocker 条目及其说明「The service for the purpose of Android 4.0.3 and above to lock apps easily.」 | 核对系统侧告知文本与实际申请的全窗口内容读取/按键过滤能力之间的落差 | 服务条目名 Smart AppLocker；描述文本仅提 lock apps easily；开关初始为关闭状态 |
| **设置页之上的全屏遮罩与 GIF 教学层** | TYPE_SYSTEM_ALERT 悬浮窗：全屏 #aa000000 半透明黑底 + GIF 动图 + 蓝色渐变按钮「Get It」 | 这是该样本最具特征的诱导形态——在真实系统设置页上叠层演示，且无跳过入口 | 同一画面中同时存在系统设置列表文本与半透明遮罩层；按钮文本 Get It；存在 GIF 动图区域（多帧变化）；遮罩覆盖全屏且无法通过返回键退出 |
| **关闭遮罩后的循环回跳页** | 点击 Get It 后回到 com.agomi.applocker 主界面，约 800ms 后重新出现同一 Attention Dialog 并再次跳设置 | 验证拒权后无降级、无跳过，构成强制循环而非一次性提示 | 同一 Dialog 文本在 1~2 秒内重复出现；Activity 在 AppLocker 与 Settings 之间反复切换；SharedPreferences 中无记录已拒绝的跳过标记 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.goami.applocker.AppLocker.ApplicationListActivity.onResume`
- `com.goami.applocker.AppLocker.ApplicationListActivity.f`
- `com.goami.applocker.AppLocker.ApplicationListActivity.e`
- `com.goami.applocker.AppLocker.ApplicationListActivity.g`
- `com.goami.applocker.AppLocker.ApplicationListActivity$4.a`
- `res/xml/phone_accessibility.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**静态可见性：完整清晰**——无加壳、无加密载荷，无障碍引导链路全部在 `classes.dex` 与 `res/` 中可直接还原。

**引导链路（运行期 UTG 视角，共 6 步）**

1. **冷启动/回前台入口**：`ApplicationListActivity`（LAUNCHER，singleInstance）在 `onResume()` 中用 `k.a(runnable, 800L)` 起 **800ms 延时**自检。
2. **权限自检**：`g()` 调 `getEnabledAccessibilityServiceList(-1)`，比对 `包名/com.goami.applocker.AppLocker.MyAccessibilityServiceTmp` 是否在已启用列表；未启用 → `f()`。
3. **不可取消的原生引导框**：`com.goami.applocker.AppLocker.a.b` 自定义 Dialog，标题 `alp_42447968_cmd_Attention`（"Attention"），正文 `alp_42447968_cmd_android_m_above`（"This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it."），`setCancelable(Build.VERSION.SDK_INT < 20)`——**Android 5.0+ 上点外部/返回键不可关闭**。
4. **确认即跳系统设置**：确认回调 `ApplicationListActivity$4.a(Dialog)` 先执行 `e()`，再 `dialog.dismiss()`。
5. **跳转 + 全屏悬浮遮罩叠层**：`e()` 先 `startActivity("android.settings.ACCESSIBILITY_SETTINGS")`，紧接着用 `WindowManager.addView` 以 `type=2005`(TYPE_SYSTEM_ALERT)、`-1×-1`、`flags=526208` 叠加 [hint_set_accessibility.xml](<resource-unit:#1 file:res/layout/hint_set_accessibility.xml>)：根背景 `#aa000000` 半透明全屏黑，内嵌 **GIF 教程图** `pic_accessibility_guide` + "Get It" 按钮，即压在系统无障碍列表之上的操作演示层。
6. **关闭即回到检测（引导循环）**："Get It" 的 `$3.onClick` 仅 `removeView`，回到本 Activity → `onResume` → 800ms → 再检测 → 未授权则再次弹框+跳设置，无跳过/降级分支。

**身份与告知落差**：服务 `android:label` 未声明，系统列表显示应用名 "Smart AppLocker"；描述仅一句 "The service for the purpose of Android 4.0.3 and above to lock apps easily."，而 `phone_accessibility.xml` 实际申请 `typeAllMask` + `canRetrieveWindowContent=true` + `canRequestFilterKeyEvents=true`（全窗口内容读取 + 按键过滤）。此外该服务类直接继承 `com.luna.powersaver.gp.service.a`（省电模块基类），Manifest 中另有 `com.luna.powersaver.gp.service.GuardService`，说明无障碍能力实际由捆绑的 powersaver/ad 模块承载。

**其他观察**：预筛中的 Facebook / Google Play services 字符串均来自三方 SDK 的 strings.xml，与本引导链路无关；`WRITE_SETTINGS`/`PACKAGE_USAGE_STATS`/`CAMERA` 等共现权限未在本链路使用。

已登记风险 **R-001**（privacy_spyware / high）：以应用锁名义冷启动延时自检、不可取消引导、跳设置后全屏遮罩 + GIF 教学、拒权循环。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（自检、引导框、跳转、悬浮遮罩、GIF 教程、循环判定）均在 classes.dex 与 res/ 中完整静态可见；无加壳、无 AES 密文、无远端 HTML 承载引导文案。仅 GIF 教程图 pic_accessibility_guide 为图片资源，其内部步骤文字需 OCR 才能逐字提取。",
  "summary_one_liner": "以「Smart AppLocker 应用锁」为外壳，冷启动/回前台 800ms 后静默自检无障碍服务，未启用即弹出 Android 5.0+ 上不可取消的 Attention 引导框，确认后跳系统无障碍设置并立刻叠加 TYPE_SYSTEM_ALERT 全屏半透明遮罩 + GIF 分步教程，关闭遮罩返回后再次检测形成无跳过按钮的循环引导，且申请的是全窗口内容读取与按键过滤能力。",
  "disguise_identity": {
    "app_display_name": "Smart AppLocker",
    "claimed_brand_or_persona": "Smart AppLocker（应用锁 / App Locker，宣称用于「轻松锁定应用」）",
    "a11y_service_label": "Smart AppLocker（服务未声明 android:label，系统无障碍列表回退显示应用名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未声明 android:label，系统列表直接沿用应用名以维持「应用锁」形象；android:description 仅一句良性用途说明，未披露 typeAllMask 全窗口内容读取与 canRequestFilterKeyEvents 按键拦截；服务类名以 Tmp 结尾伪装为临时占位，实际继承捆绑的 com.luna.powersaver.gp.service.a 省电模块基类，核心逻辑位于混淆包 com.luna.powersaver.gp / com.amigo.faldaldk 下"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.goami.applocker.AppLocker.ApplicationListActivity（LAUNCHER，singleInstance，label=@string/app_name）",
      "trigger_event": "onResume() 中 k.a(new ApplicationListActivity$2(this), 800L) 起 800ms 延时任务",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（本步为应用列表主界面，不呈现引导文案）",
      "shown_text_zh": "应用锁主列表界面，用户此时尚看不到任何权限提示",
      "user_action_requested": "无需操作；仅需打开应用或从后台返回前台",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity.onResume"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "ApplicationListActivity$2.run → ApplicationListActivity.g()",
      "trigger_event": "800ms 定时到点；getEnabledAccessibilityServiceList(-1) 比对 \"com.agomi.applocker/com.goami.applocker.AppLocker.MyAccessibilityServiceTmp\" 是否已启用，未启用则调用 f()",
      "ui_carrier": "不可静态还原（无界面，纯后台判定）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静默检测自身无障碍服务是否已在系统列表中被勾选",
      "user_action_requested": "无",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity.g"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "自定义 Dialog com.goami.applocker.AppLocker.a.b（由 ApplicationListActivity.f() 创建并 show）",
      "trigger_event": "f() 检测到服务未启用，构造 dialog：标题 getString(2131165276)、正文 getString(2131165277)、setCancelable(Build.VERSION.SDK_INT < 20)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "shown_text_zh": "注意 / 本设备版本高于 Android 4.0.3，请前往 设置->无障碍服务->App Locker 并将其开启。",
      "user_action_requested": "点击确认按钮前往设置（$4 回调）；Android 5.0 及以上 setCancelable(false)，返回键与点击外部均无法关闭",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity.f / res/values/strings.xml#L94-L95 (alp_42447968_cmd_Attention, alp_42447968_cmd_android_m_above)"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（Intent 常量 ApplicationListActivity.r）",
      "trigger_event": "ApplicationListActivity$4.a(Dialog) 先调用 e()，e() 内 startActivity(r) 跳转系统无障碍设置页",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用自身不渲染该页，仅发起 Intent）",
      "shown_text_zh": "跳转到系统「无障碍」设置列表，用户需在此找到 Smart AppLocker 并手动打开开关",
      "user_action_requested": "在系统无障碍列表中找到 Smart AppLocker 并开启",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity.e / ApplicationListActivity$4.a"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WindowManager 叠加视图 res/layout/hint_set_accessibility.xml（TYPE_SYSTEM_ALERT=2005，-1×-1，flags=526208，背景 #aa000000）",
      "trigger_event": "e() 在 startActivity 后立即 addView 全屏遮罩；内部 GifImageView 加载 pic_accessibility_guide 并 cVar.a(1000).start() 播放",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Get It（按钮文本 str_get_it；其余步骤说明以 GIF 动图形式呈现，无文本）",
      "shown_text_zh": "半透明全屏遮罩上循环播放 GIF 教程演示如何开启无障碍，底部「知道了/开始」按钮",
      "user_action_requested": "观看 GIF 教程后点击 Get It 关闭遮罩（$3.onClick 仅 removeView），无取消或跳过分支",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity.e / res/layout/hint_set_accessibility.xml / res/values/strings.xml#L183 (str_get_it)"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "ApplicationListActivity（遮罩关闭后回到本 Activity）→ onResume → $2.run → g() → f()",
      "trigger_event": "遮罩按钮 removeView 后 Activity 重新获得焦点，onResume 再次启动 800ms 延时检测；若服务仍未启用则重新弹框并再次跳设置",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "shown_text_zh": "再次弹出同一 Attention 提示，用户不授权即无法正常使用应用列表功能",
      "user_action_requested": "只能再次前往设置开启，无「以后再说」「跳过」等退出路径（SDK≥20 时弹框不可取消）",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity$3.onClick → ApplicationListActivity.onResume → ApplicationListActivity$2.run"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.goami.applocker.AppLocker.MyAccessibilityServiceTmp（extends com.luna.powersaver.gp.service.a），onServiceConnected 起开始接收事件",
      "trigger_event": "用户在系统无障碍列表勾选服务后，系统绑定服务并回调 onServiceConnected；此后 $2.run 的 g() 返回 true，不再弹引导",
      "ui_carrier": "不可静态还原（服务运行态，无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "引导停止，服务开始按 typeAllMask / canRetrieveWindowContent / canRequestFilterKeyEvents 接收全量无障碍事件",
      "user_action_requested": "无",
      "code_anchor": "com.goami.applocker.AppLocker.MyAccessibilityServiceTmp.onServiceConnected / res/xml/phone_accessibility.xml"
    }
  ],
  "text_presentation_locations": [
    "ApplicationListActivity.f() 弹出的自定义原生 Dialog com.goami.applocker.AppLocker.a.b：标题「Attention」、正文「This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.」（来源 res/values/strings.xml 的 alp_42447968_cmd_Attention / alp_42447968_cmd_android_m_above）",
    "跳转 ACCESSIBILITY_SETTINGS 后立即叠加的全屏 TYPE_SYSTEM_ALERT 悬浮窗 res/layout/hint_set_accessibility.xml：背景 #aa000000，内含 GIF 图 res/drawable/pic_accessibility_guide 与按钮文本「Get It」（str_get_it）",
    "系统无障碍服务列表条目：服务未设 android:label，显示应用名「Smart AppLocker」；说明文字来自 res/xml/phone_accessibility.xml → @string/accessibility_service_description「The service for the purpose of Android 4.0.3 and above to lock apps easily.」",
    "Manifest 中 application android:label=@string/app_name（Smart AppLocker），桌面图标与名称与引导流程保持同一「应用锁」身份",
    "无本地或远端 HTML/WebView 承载引导文案；GIF 教程图内的分步文字为纯图片内容，需 OCR 提取"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Attention",
      "text_zh": "注意",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_Attention（getString(2131165276)）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "本设备版本高于 Android 4.0.3。请前往 设置->无障碍服务->App Locker 并将其开启。",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_android_m_above（getString(2131165277)）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The service for the purpose of Android 4.0.3 and above to lock apps easily.",
      "text_zh": "本服务用于在 Android 4.0.3 及以上系统中轻松锁定应用。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（经 res/xml/phone_accessibility.xml android:description 引用，显示于系统无障碍列表）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Get It",
      "text_zh": "知道了 / 开始",
      "source_location": "res/values/strings.xml key=str_get_it（res/layout/hint_set_accessibility.xml 按钮 android:text）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Smart AppLocker",
      "text_zh": "智能应用锁",
      "source_location": "res/values/strings.xml key=app_name（AndroidManifest application android:label；无障碍服务未声明 label 时系统列表同样显示此项）",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onResume 每次都以 k.a(..., 800L) 重新起 800ms 延时检测；遮罩 Get It 仅 removeView 回到本 Activity，未授权即再次弹框并再次 startActivity(ACCESSIBILITY_SETTINGS)，形成「关闭遮罩→返回→再弹框→再跳设置」的无限循环；SDK_INT>=20 时 Dialog setCancelable(false)，返回键与点外部均无法取消。",
    "overlay_or_fake_settings": "跳转系统无障碍设置后立即通过 WindowManager 以 type=2005(TYPE_SYSTEM_ALERT)、-1×-1、flags=526208 叠加全屏半透明黑色（#aa000000）遮罩，内嵌循环播放的 GIF 教程与 Get It 按钮，属压在真实系统设置页之上的叠层引导；不是自绘高仿无障碍开关页。",
    "restricted_settings_13plus_coaching": "无。目标 SDK 为 24，代码中未见引导进入应用详情页右上角菜单允许受限设置，也未见 Session 安装器绕过逻辑（预筛 SESSION_INSTALLER 线索未在本无障碍链路中被调用）。",
    "post_grant_anti_removal": "无。获权后 $2.run 的 g() 返回 true 即停止弹框，未发现自点确认、自授权或在设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；预筛的 PERFORM_GLOBAL_ACTION 未出现在本引导链路。",
    "benign_graceful_degradation": "无。未授权时不存在手动模式、仅观看模式或功能降级路径，唯一分支是「已启用/未启用」。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以「Activity 切换到 com.android.settings/.Settings$AccessibilitySettings（或 Settings$AccessibilitySettingsActivity）」为首要触发点——应用在 startActivity 后同一方法内立刻 addView 全屏 TYPE_SYSTEM_ALERT 遮罩，跳转后 200~1000ms 内截图/UTG 即可同时抓到系统无障碍列表与压在其上的引导遮罩；次选触发点为 ApplicationListActivity 冷启动 onResume 后 800ms 处的自定义 Attention Dialog 出现瞬间。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（跳转前）",
        "page_identifier": "包名 com.agomi.applocker 的 Dialog，标题文本 Attention，正文含「Please Go Setting->AccessibilityService->App Locker and Open it.」，无「取消/跳过/以后再说」按钮",
        "why_most_useful": "直接证明引导为冷启动即触发且不可取消，是区分「按需说明」与「前置强制」的关键",
        "observable_utg_signals": ["对话框标题文本 Attention", "正文含 AccessibilityService 与 App Locker 字样", "按钮集合中无取消类文案", "返回键无效（SDK>=20）"]
      },
      {
        "page_role": "系统无障碍服务列表页（跳转目标）",
        "page_identifier": "Settings$AccessibilitySettings，列表中出现 Smart AppLocker 条目及其说明「The service for the purpose of Android 4.0.3 and above to lock apps easily.」",
        "why_most_useful": "核对系统侧告知文本与实际申请的全窗口内容读取/按键过滤能力之间的落差",
        "observable_utg_signals": ["服务条目名 Smart AppLocker", "描述文本仅提 lock apps easily", "开关初始为关闭状态"]
      },
      {
        "page_role": "设置页之上的全屏遮罩与 GIF 教学层",
        "page_identifier": "TYPE_SYSTEM_ALERT 悬浮窗：全屏 #aa000000 半透明黑底 + GIF 动图 + 蓝色渐变按钮「Get It」",
        "why_most_useful": "这是该样本最具特征的诱导形态——在真实系统设置页上叠层演示，且无跳过入口",
        "observable_utg_signals": ["同一画面中同时存在系统设置列表文本与半透明遮罩层", "按钮文本 Get It", "存在 GIF 动图区域（多帧变化）", "遮罩覆盖全屏且无法通过返回键退出"]
      },
      {
        "page_role": "关闭遮罩后的循环回跳页",
        "page_identifier": "点击 Get It 后回到 com.agomi.applocker 主界面，约 800ms 后重新出现同一 Attention Dialog 并再次跳设置",
        "why_most_useful": "验证拒权后无降级、无跳过，构成强制循环而非一次性提示",
        "observable_utg_signals": ["同一 Dialog 文本在 1~2 秒内重复出现", "Activity 在 AppLocker 与 Settings 之间反复切换", "SharedPreferences 中无记录已拒绝的跳过标记"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "GIF 教程图 res/drawable/pic_accessibility_guide 内的分步文字为纯图片内容，UTG 文本树无法提取，需 OCR；遮罩为全屏且覆盖系统设置页，部分设备上会遮挡系统设置节点的可读性，需以窗口层级（WindowManager 多窗口）而非单窗口文本判定。应用未加壳，运行期行为可完整观测；预筛中的 Facebook / Google Play services 文案均属三方 SDK 资源，与引导链路无关，不构成误判干扰。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.goami.applocker.AppLocker.ApplicationListActivity.onResume",
    "com.goami.applocker.AppLocker.ApplicationListActivity.f",
    "com.goami.applocker.AppLocker.ApplicationListActivity.e",
    "com.goami.applocker.AppLocker.ApplicationListActivity.g",
    "com.goami.applocker.AppLocker.ApplicationListActivity$4.a",
    "res/xml/phone_accessibility.xml"
  ]
}
```

</details>
