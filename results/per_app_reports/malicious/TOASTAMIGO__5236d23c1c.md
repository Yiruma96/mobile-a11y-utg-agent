# MR_007__5236d23c1c｜TOASTAMIGO — Smart AppLocker

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：138.2s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即检测自身无障碍服务是否开启，未开启则以不可取消原生 Dialog（Attention + 教用户进设置页）阻断使用，确认后跳系统无障碍列表并立刻用 TYPE_SYSTEM_ALERT 全屏半透明 GIF 遮罩指引点击，返回未开启则 800ms 后重弹，取消即退出应用。
- **静态可见性说明**：无障碍引导全链路（判定→Dialog→startActivity→悬浮遮罩→onResume 重弹）均由 DEX 明文实现，字符串与 layout 资源完整可读，未加壳；仅 com.luna.powersaver.gp 侧的远端任务配置（自动点击/安装任务脚本）来自网络下发，不影响本引导流程的静态可见性。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5236d23c1c97fbf88f6aea34a2eaceaed085224d65d2322e94a8f5bc0a8002e9` |
| 包名 / 年份 | `com.agomi.applocker` / 2017 |
| 家族 / 品类 | **TOASTAMIGO**（同池样本数：44） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/k/toast-overlay-weaponized-install-android-malware-single-attack-chain.html |
| 桌面显示名 | Smart AppLocker |
| 引导页宣称品牌/身份 | 自称应用锁工具 App Locker（内部标签 Appz Lock Preference），代码主体实际为 com.luna.powersaver 电量/广告任务与自动安装框架 |
| 系统无障碍列表服务名 | 服务未声明 android:label，系统无障碍列表显示应用名 Smart AppLocker |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.agomi.applocker 与代码内实际命名空间 com.goami.applocker 存在拼写不一致的品牌/域名混淆；无障碍 android:description 仅声明“锁应用”，与实际 typeAllMask + canRetrieveWindowContent + canRequestFilterKeyEvents 的自动化能力范围不符；未使用同形字、activity-alias 或伪造 isAccessibilityTool |
| 无障碍服务类名 | `com.goami.applocker.AppLocker.MyAccessibilityServiceTmp` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.miui.home,com.umiplus.screenlock,com.android.vending,com.android.settings,com.android.packageinstaller,com.google.android.packageinstaller,com.sec.android.app.launcher,com.bbk.launcher2,com.oppo.launcher |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | The service for the purpose of Android 4.0.3 and above to lock apps easily. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.goami.applocker.AppLocker.ApplicationListActivity（LAUNCHER，singleInstance） | onCreate → d() → g()：读取已启用的无障碍服务列表，比对 id 是否等于 <包名>/com.goami.applocker.AppLocker.MyAccessibilityServiceTmp | 原生Activity | 无 | 无（自动判定，用户无感知） | `com.goami.applocker.AppLocker.ApplicationListActivity.onCreate / d / g` |
| 2 | 引导说明页 | 自定义原生 Dialog com.goami.applocker.AppLocker.a.b（layout dialog_confirm，主题 2131362032） | g() 返回 false 时 f() 构造并 show()；Android 5.0+ 设置 setCancelable(false) | 原生Dialog | **原文**：Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm<br>**译注**：注意：本设备版本高于 Android 4.0.3，请前往 设置->辅助功能服务->App Locker 并将其打开。按钮为“取消”“确认”。 | 点击 Confirm 前往系统无障碍设置；点击 Cancel 则 finish() 退出应用；API≥20 时返回键/点击外部无法取消 | `com.goami.applocker.AppLocker.ApplicationListActivity.f / com.goami.applocker.AppLocker.a.b.<init>；strings: alp_42447968_cmd_Attention、alp_42447968_cmd_android_m_above、str_dialog_btn_cancel、str_dialog_btn_confirm` |
| 3 | 跳受限设置 | 系统无障碍设置页（Intent android.settings.ACCESSIBILITY_SETTINGS） | Dialog 确认回调 ApplicationListActivity$4.a → ApplicationListActivity.e() → startActivity(r)（r 为静态 Intent） | 系统无障碍页 | **原文**：无（由系统页面渲染）<br>**译注**：系统“无障碍/辅助功能”列表页，用户需在其中找到 Smart AppLocker 并打开开关 | 在系统列表中找到本应用的无障碍服务并开启开关 | `com.goami.applocker.AppLocker.ApplicationListActivity$4.a / ApplicationListActivity.e；字段 ApplicationListActivity#r` |
| 4 | 遮罩叠层指引 | WindowManager 全屏悬浮层（type=2005 TYPE_SYSTEM_ALERT，flags=526208，layout hint_set_accessibility，背景 #aa000000） | e() 中 startActivity 之后立即 addView；GIF 由 pl.droidsonroids.gif.GifImageView 播放 pic_accessibility_guide | 悬浮窗Overlay | **原文**：Get It<br>**译注**：半透明黑色全屏遮罩 + 无障碍操作指引动图（GIF）+“知道了/去设置”按钮 Get It | 在遮罩上点击 Get It 移除遮罩（移除后露出系统无障碍页继续操作）；无跳转按钮，需用户自己在系统页点开关 | `com.goami.applocker.AppLocker.ApplicationListActivity.e；res/layout/hint_set_accessibility.xml；res/values/strings.xml#str_get_it` |
| 5 | 拒权反馈循环 | ApplicationListActivity.onResume + TimerTask ApplicationListActivity$2（延迟 800ms） | 从系统设置返回触发 onResume → k.a(...,800L) → 再次 g() 判定，仍为 false 则再次 f() 弹出同一 Dialog | 原生Dialog | **原文**：Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.<br>**译注**：每次返回应用都会被再次要求去开启无障碍，形成循环；用户只能点 Cancel 退出应用 | 再次确认跳设置，或 Cancel 退出 | `com.goami.applocker.AppLocker.ApplicationListActivity.onResume / ApplicationListActivity$2.run` |
| 6 | 获权后动作 | com.goami.applocker.AppLocker.MyAccessibilityServiceTmp（onServiceConnected） | 系统启用服务后回调 onServiceConnected → b.a.i() 为真则上报 ACCESS_OPEN、写 SharedPreferences 标志、初始化 com.luna.powersaver.gp 无障碍任务引擎 | 不可静态还原 | 无 | 无 | `com.goami.applocker.AppLocker.MyAccessibilityServiceTmp.onServiceConnected / com.goami.applocker.AppLocker.b.a.a` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- ApplicationListActivity 冷启动即弹出的自定义原生 AlertDialog（layout dialog_confirm）：标题 Attention、正文教用户进 设置->辅助功能服务->App Locker 打开，按钮 Cancel/Confirm
- 跳转系统无障碍页后立即叠加的全屏悬浮层 res/layout/hint_set_accessibility.xml：GIF 指引图 pic_accessibility_guide + Get It 按钮（背景 #aa000000）
- 系统无障碍服务列表项文本：服务无 android:label，显示应用名 Smart AppLocker；下方说明为 res/xml/phone_accessibility.xml 引用的 accessibility_service_description = The service for the purpose of Android 4.0.3 and above to lock apps easily.
- 未使用的备用文案 res/values/strings.xml：alp_42447968_cmd_android_m_above_toast = Find Setting->AccessibilityService->App Locker and Open it.（用于 Toast 提示路径）
- com.luna.powersaver.gp 模块另有一条独立的 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 路径（com.luna.powersaver.gp.g.b.a），可在后台任务中直接拉起系统无障碍页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Attention | 注意 | `strings.xml key alp_42447968_cmd_Attention（Dialog 标题）` | 受限设置分步教学 |
| en | This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. | 本设备版本高于 Android 4.0.3，请前往 设置->辅助功能服务->App Locker 并打开它。 | `strings.xml key alp_42447968_cmd_android_m_above（ApplicationListActivity.f 设为 Dialog 正文）` | 受限设置分步教学 |
| en | Find Setting->AccessibilityService->App Locker and Open it. | 找到 设置->辅助功能服务->App Locker 并打开。 | `strings.xml key alp_42447968_cmd_android_m_above_toast` | 受限设置分步教学 |
| en | The service for the purpose of Android 4.0.3 and above to lock apps easily. | 本服务用于 Android 4.0.3 及以上系统便捷地锁定应用。 | `res/xml/phone_accessibility.xml android:description → strings.xml key accessibility_service_description（系统无障碍列表可见）` | 良性透明说明 |
| en | Get It | 去设置 / 知道了 | `strings.xml key str_get_it（res/layout/hint_set_accessibility.xml 悬浮层按钮）` | 受限设置分步教学 |
| en | Cancel | 取消 | `strings.xml key str_dialog_btn_cancel（Dialog 取消按钮）` | 良性透明说明 |
| en | Confirm | 确认 | `strings.xml key str_dialog_btn_confirm（Dialog 确认按钮）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：onResume 中通过 k.a(Runnable, 800L) 延迟 800ms 重新检测 g()，未开启则重新弹出同一 Dialog；从系统设置返回即触发，形成“返回就重弹”的循环；Dialog 的 Cancel 按钮回调直接 finish() 退出应用，不存在“暂不开启继续使用”的降级路径
- **遮罩叠层 / 高仿系统设置页**：确认跳转后在系统无障碍设置页之上用 WindowManager 叠加全屏半透明（#aa000000）TYPE_SYSTEM_ALERT 悬浮层，内含 GIF 操作指引与 Get It 按钮；不是高仿系统开关页，属遮罩式指引
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion 24，未见应用详情右上角菜单/受限设置教学；仅存在通用的 APPLICATION_DETAILS_SETTINGS 跳转工具方法，未在本引导链路中使用）
- **获权后即时行为与防撤权机制**：无（本链路获权后仅上报 ACCESS_OPEN 与初始化 powersaver 任务引擎，未发现监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码）
- **良性降级 / 替代方案**：无（拒绝授权即无法使用并退出应用，无手动模式或仅观看模式）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：应用冷启动后首次 ApplicationListActivity 弹出 Attention Dialog 的瞬间；以及随后检测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 后 300~1500ms 内悬浮层 addView 的窗口变化（type=2005）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：悬浮遮罩的指引主体是 GIF 动图（pic_accessibility_guide），纯文本 UTG 只能取到 Get It 按钮，需 OCR/截图补充；获权后的自动化行为（自动点击安装、远端任务脚本）依赖网络下发配置，静态不可完全还原；此外 com.luna.powersaver.gp.g.b.a 可在后台任务中直接拉起无障碍设置页，不经过首屏 Dialog，UTG 需同时监控该 Intent。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动阻断引导弹窗页** | com.goami.applocker.AppLocker.ApplicationListActivity 之上的自定义 Dialog，文本含 Attention / Please Go Setting->AccessibilityService | 这是判定“是否以不可取消弹窗在首屏强制索取无障碍”的第一现场，可同时取得文案与按钮结构（Cancel/Confirm） | Dialog 文本节点 Attention 与 Please Go Setting->AccessibilityService；Confirm/Cancel 两个按钮节点；返回键无法关闭（窗口未消失） |
| **跳转后的系统无障碍列表项** | Settings 无障碍页中出现 Smart AppLocker 条目及其描述 The service for the purpose of Android 4.0.3 and above to lock apps easily. | 确认用户被导向的具体系统条目与服务自述用途，可与实际能力范围对比 | 条目文本 Smart AppLocker；条目副标题 description 文本；开关节点 checked=false 初态 |
| **设置页之上的全屏遮罩指引页** | type=2005 悬浮窗，背景 #aa000000，含 GIF 图与 Get It 文本按钮 | 遮罩叠在系统设置之上是区分“正常引导”与“强制诱导”的关键特征，UTG 可读到 Get It 按钮与底层设置页节点共存 | 同一时刻既有无障碍设置列表节点又有 Get It 按钮节点；Get It 点击后遮罩窗口消失；GIF 区域无文本（需图像） |
| **拒权返回后的重弹页** | 从设置返回后约 800ms 再次出现的同一 Attention Dialog | 验证拒权循环：返回即重弹，可证明用户无法在不授权的情况下使用应用 | 返回键后 800ms 内 Dialog 文本再次出现；连续多次返回重复出现；点 Cancel 后进程/Activity 结束 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.goami.applocker.AppLocker.ApplicationListActivity.onCreate`
- `com.goami.applocker.AppLocker.ApplicationListActivity.g`
- `com.goami.applocker.AppLocker.ApplicationListActivity.f`
- `com.goami.applocker.AppLocker.ApplicationListActivity.e`
- `com.goami.applocker.AppLocker.ApplicationListActivity$2.run`
- `res/layout/hint_set_accessibility.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**结论：完整静态可见，属于“冷启动强制引导、跳转系统设置页、叠加悬浮遮罩”的流程，未见加壳或密文载荷参与该链路。**

- **入口即阻断**：`ApplicationListActivity.onCreate` 调用 `d()`，后者调用 `g()`，用 `AccessibilityManager.getEnabledAccessibilityServiceList(-1)` 逐项比对 `包名/com.goami.applocker.AppLocker.MyAccessibilityServiceTmp`。未开启就调用 `f()` 弹出自定义 Dialog，首屏即进入权限引导流程。
- **说明文字承载**：原生自定义 Dialog（`com.goami.applocker.AppLocker.a.b`，layout `dialog_confirm`）标题 `Attention`，正文 `This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.`，按钮 `Cancel` / `Confirm`。`setCancelable(Build.VERSION.SDK_INT < 20)` 表示 Android 5.0 及以上无法用返回键或点击外部取消。
- **跳转点**：确认后 `ApplicationListActivity$4.a` 调用 `e()`，执行 `startActivity(r)`（静态常量 `Intent("android.settings.ACCESSIBILITY_SETTINGS")`），随后立即用 `WindowManager.addView`（type=2005，`TYPE_SYSTEM_ALERT`）叠一层**全屏半透明遮罩** `#aa000000`，内含 GIF `pic_accessibility_guide` 和 `Get It` 按钮（layout `hint_set_accessibility`），形成“设置页上压指引图”的典型 UTG 场景。
- **拒权反馈循环**：`onResume` 中 `k.a(new ApplicationListActivity$2(this), 800L)` 延迟 800ms 再判 `g()`；若仍未开启则重新弹出同一 Dialog。点击 `Cancel` 则 `finish()` 退出应用，属于“要么开启、要么退出”。
- **获权后**：`MyAccessibilityServiceTmp.onServiceConnected` 上报 `ACCESS_OPEN`、写 SharedPreferences 标志，并初始化 `com.luna.powersaver.gp` 无障碍任务引擎（后续可自动点击安装对话框、`testRun("accessibility")` 跳转等）；该部分与主流程分离，属另一条能力链。
- **无障碍声明**：`res/xml/phone_accessibility.xml` 为 `typeAllMask` + `canRetrieveWindowContent=true` + `canRequestFilterKeyEvents=true`，但 `android:description` 只写“锁应用”用途，与上述自动化能力范围不一致。

## 关键代码锚点

- 入口判定与首屏弹窗：[ApplicationListActivity.onCreate()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity#onCreate>)、[ApplicationListActivity.g()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity#g>)、[ApplicationListActivity.f()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity#f>)
- 跳转与悬浮遮罩：[ApplicationListActivity.e()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity#e>)、[hint_set_accessibility.xml](<resource-unit:#1 file:res/layout/hint_set_accessibility.xml#L1-L6>)
- 拒权循环：[ApplicationListActivity.onResume()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity#onResume>)、[ApplicationListActivity$2.run()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity$2#run>)
- 确认/取消回调：[ApplicationListActivity$4.a()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity$4#a>)、[ApplicationListActivity$5.a()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.ApplicationListActivity$5#a>)
- 服务声明与描述：[phone_accessibility.xml](<resource-unit:#1 file:res/xml/phone_accessibility.xml#L1-L3>)、[strings.xml 无障碍文案](<resource-unit:#1 file:res/values/strings.xml#L93-L95>)
- 获权回调：[MyAccessibilityServiceTmp.onServiceConnected()](<resource-unit:#1.dex1 code:com.goami.applocker.AppLocker.MyAccessibilityServiceTmp#onServiceConnected>)

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（判定→Dialog→startActivity→悬浮遮罩→onResume 重弹）均由 DEX 明文实现，字符串与 layout 资源完整可读，未加壳；仅 com.luna.powersaver.gp 侧的远端任务配置（自动点击/安装任务脚本）来自网络下发，不影响本引导流程的静态可见性。",
  "summary_one_liner": "冷启动即检测自身无障碍服务是否开启，未开启则以不可取消原生 Dialog（Attention + 教用户进设置页）阻断使用，确认后跳系统无障碍列表并立刻用 TYPE_SYSTEM_ALERT 全屏半透明 GIF 遮罩指引点击，返回未开启则 800ms 后重弹，取消即退出应用。",
  "disguise_identity": {
    "app_display_name": "Smart AppLocker",
    "claimed_brand_or_persona": "自称应用锁工具 App Locker（内部标签 Appz Lock Preference），代码主体实际为 com.luna.powersaver 电量/广告任务与自动安装框架",
    "a11y_service_label": "服务未声明 android:label，系统无障碍列表显示应用名 Smart AppLocker",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.agomi.applocker 与代码内实际命名空间 com.goami.applocker 存在拼写不一致的品牌/域名混淆；无障碍 android:description 仅声明“锁应用”，与实际 typeAllMask + canRetrieveWindowContent + canRequestFilterKeyEvents 的自动化能力范围不符；未使用同形字、activity-alias 或伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.goami.applocker.AppLocker.ApplicationListActivity（LAUNCHER，singleInstance）",
      "trigger_event": "onCreate → d() → g()：读取已启用的无障碍服务列表，比对 id 是否等于 <包名>/com.goami.applocker.AppLocker.MyAccessibilityServiceTmp",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（仅做状态检测，未开启即进入弹窗分支）",
      "user_action_requested": "无（自动判定，用户无感知）",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity.onCreate / d / g"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "自定义原生 Dialog com.goami.applocker.AppLocker.a.b（layout dialog_confirm，主题 2131362032）",
      "trigger_event": "g() 返回 false 时 f() 构造并 show()；Android 5.0+ 设置 setCancelable(false)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Cancel / Confirm",
      "shown_text_zh": "注意：本设备版本高于 Android 4.0.3，请前往 设置->辅助功能服务->App Locker 并将其打开。按钮为“取消”“确认”。",
      "user_action_requested": "点击 Confirm 前往系统无障碍设置；点击 Cancel 则 finish() 退出应用；API≥20 时返回键/点击外部无法取消",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity.f / com.goami.applocker.AppLocker.a.b.<init>；strings: alp_42447968_cmd_Attention、alp_42447968_cmd_android_m_above、str_dialog_btn_cancel、str_dialog_btn_confirm"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统无障碍设置页（Intent android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "Dialog 确认回调 ApplicationListActivity$4.a → ApplicationListActivity.e() → startActivity(r)（r 为静态 Intent）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（由系统页面渲染）",
      "shown_text_zh": "系统“无障碍/辅助功能”列表页，用户需在其中找到 Smart AppLocker 并打开开关",
      "user_action_requested": "在系统列表中找到本应用的无障碍服务并开启开关",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity$4.a / ApplicationListActivity.e；字段 ApplicationListActivity#r"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WindowManager 全屏悬浮层（type=2005 TYPE_SYSTEM_ALERT，flags=526208，layout hint_set_accessibility，背景 #aa000000）",
      "trigger_event": "e() 中 startActivity 之后立即 addView；GIF 由 pl.droidsonroids.gif.GifImageView 播放 pic_accessibility_guide",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Get It",
      "shown_text_zh": "半透明黑色全屏遮罩 + 无障碍操作指引动图（GIF）+“知道了/去设置”按钮 Get It",
      "user_action_requested": "在遮罩上点击 Get It 移除遮罩（移除后露出系统无障碍页继续操作）；无跳转按钮，需用户自己在系统页点开关",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity.e；res/layout/hint_set_accessibility.xml；res/values/strings.xml#str_get_it"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "ApplicationListActivity.onResume + TimerTask ApplicationListActivity$2（延迟 800ms）",
      "trigger_event": "从系统设置返回触发 onResume → k.a(...,800L) → 再次 g() 判定，仍为 false 则再次 f() 弹出同一 Dialog",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "shown_text_zh": "每次返回应用都会被再次要求去开启无障碍，形成循环；用户只能点 Cancel 退出应用",
      "user_action_requested": "再次确认跳设置，或 Cancel 退出",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity.onResume / ApplicationListActivity$2.run"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.goami.applocker.AppLocker.MyAccessibilityServiceTmp（onServiceConnected）",
      "trigger_event": "系统启用服务后回调 onServiceConnected → b.a.i() 为真则上报 ACCESS_OPEN、写 SharedPreferences 标志、初始化 com.luna.powersaver.gp 无障碍任务引擎",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见界面，静默完成权限落地与任务引擎初始化（后续可自动点击安装/权限对话框）",
      "user_action_requested": "无",
      "code_anchor": "com.goami.applocker.AppLocker.MyAccessibilityServiceTmp.onServiceConnected / com.goami.applocker.AppLocker.b.a.a"
    }
  ],
  "text_presentation_locations": [
    "ApplicationListActivity 冷启动即弹出的自定义原生 AlertDialog（layout dialog_confirm）：标题 Attention、正文教用户进 设置->辅助功能服务->App Locker 打开，按钮 Cancel/Confirm",
    "跳转系统无障碍页后立即叠加的全屏悬浮层 res/layout/hint_set_accessibility.xml：GIF 指引图 pic_accessibility_guide + Get It 按钮（背景 #aa000000）",
    "系统无障碍服务列表项文本：服务无 android:label，显示应用名 Smart AppLocker；下方说明为 res/xml/phone_accessibility.xml 引用的 accessibility_service_description = The service for the purpose of Android 4.0.3 and above to lock apps easily.",
    "未使用的备用文案 res/values/strings.xml：alp_42447968_cmd_android_m_above_toast = Find Setting->AccessibilityService->App Locker and Open it.（用于 Toast 提示路径）",
    "com.luna.powersaver.gp 模块另有一条独立的 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 路径（com.luna.powersaver.gp.g.b.a），可在后台任务中直接拉起系统无障碍页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Attention",
      "text_zh": "注意",
      "source_location": "strings.xml key alp_42447968_cmd_Attention（Dialog 标题）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "本设备版本高于 Android 4.0.3，请前往 设置->辅助功能服务->App Locker 并打开它。",
      "source_location": "strings.xml key alp_42447968_cmd_android_m_above（ApplicationListActivity.f 设为 Dialog 正文）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Find Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "找到 设置->辅助功能服务->App Locker 并打开。",
      "source_location": "strings.xml key alp_42447968_cmd_android_m_above_toast",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The service for the purpose of Android 4.0.3 and above to lock apps easily.",
      "text_zh": "本服务用于 Android 4.0.3 及以上系统便捷地锁定应用。",
      "source_location": "res/xml/phone_accessibility.xml android:description → strings.xml key accessibility_service_description（系统无障碍列表可见）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Get It",
      "text_zh": "去设置 / 知道了",
      "source_location": "strings.xml key str_get_it（res/layout/hint_set_accessibility.xml 悬浮层按钮）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Cancel",
      "text_zh": "取消",
      "source_location": "strings.xml key str_dialog_btn_cancel（Dialog 取消按钮）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Confirm",
      "text_zh": "确认",
      "source_location": "strings.xml key str_dialog_btn_confirm（Dialog 确认按钮）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "onResume 中通过 k.a(Runnable, 800L) 延迟 800ms 重新检测 g()，未开启则重新弹出同一 Dialog；从系统设置返回即触发，形成“返回就重弹”的循环；Dialog 的 Cancel 按钮回调直接 finish() 退出应用，不存在“暂不开启继续使用”的降级路径",
    "overlay_or_fake_settings": "确认跳转后在系统无障碍设置页之上用 WindowManager 叠加全屏半透明（#aa000000）TYPE_SYSTEM_ALERT 悬浮层，内含 GIF 操作指引与 Get It 按钮；不是高仿系统开关页，属遮罩式指引",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion 24，未见应用详情右上角菜单/受限设置教学；仅存在通用的 APPLICATION_DETAILS_SETTINGS 跳转工具方法，未在本引导链路中使用）",
    "post_grant_anti_removal": "无（本链路获权后仅上报 ACCESS_OPEN 与初始化 powersaver 任务引擎，未发现监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码）",
    "benign_graceful_degradation": "无（拒绝授权即无法使用并退出应用，无手动模式或仅观看模式）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "应用冷启动后首次 ApplicationListActivity 弹出 Attention Dialog 的瞬间；以及随后检测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 后 300~1500ms 内悬浮层 addView 的窗口变化（type=2005）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动阻断引导弹窗页",
        "page_identifier": "com.goami.applocker.AppLocker.ApplicationListActivity 之上的自定义 Dialog，文本含 Attention / Please Go Setting->AccessibilityService",
        "why_most_useful": "这是判定“是否以不可取消弹窗在首屏强制索取无障碍”的第一现场，可同时取得文案与按钮结构（Cancel/Confirm）",
        "observable_utg_signals": ["Dialog 文本节点 Attention 与 Please Go Setting->AccessibilityService", "Confirm/Cancel 两个按钮节点", "返回键无法关闭（窗口未消失）"]
      },
      {
        "page_role": "跳转后的系统无障碍列表项",
        "page_identifier": "Settings 无障碍页中出现 Smart AppLocker 条目及其描述 The service for the purpose of Android 4.0.3 and above to lock apps easily.",
        "why_most_useful": "确认用户被导向的具体系统条目与服务自述用途，可与实际能力范围对比",
        "observable_utg_signals": ["条目文本 Smart AppLocker", "条目副标题 description 文本", "开关节点 checked=false 初态"]
      },
      {
        "page_role": "设置页之上的全屏遮罩指引页",
        "page_identifier": "type=2005 悬浮窗，背景 #aa000000，含 GIF 图与 Get It 文本按钮",
        "why_most_useful": "遮罩叠在系统设置之上是区分“正常引导”与“强制诱导”的关键特征，UTG 可读到 Get It 按钮与底层设置页节点共存",
        "observable_utg_signals": ["同一时刻既有无障碍设置列表节点又有 Get It 按钮节点", "Get It 点击后遮罩窗口消失", "GIF 区域无文本（需图像）"]
      },
      {
        "page_role": "拒权返回后的重弹页",
        "page_identifier": "从设置返回后约 800ms 再次出现的同一 Attention Dialog",
        "why_most_useful": "验证拒权循环：返回即重弹，可证明用户无法在不授权的情况下使用应用",
        "observable_utg_signals": ["返回键后 800ms 内 Dialog 文本再次出现", "连续多次返回重复出现", "点 Cancel 后进程/Activity 结束"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "悬浮遮罩的指引主体是 GIF 动图（pic_accessibility_guide），纯文本 UTG 只能取到 Get It 按钮，需 OCR/截图补充；获权后的自动化行为（自动点击安装、远端任务脚本）依赖网络下发配置，静态不可完全还原；此外 com.luna.powersaver.gp.g.b.a 可在后台任务中直接拉起无障碍设置页，不经过首屏 Dialog，UTG 需同时监控该 Intent。"
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
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE"
  ],
  "code_anchors": [
    "com.goami.applocker.AppLocker.ApplicationListActivity.onCreate",
    "com.goami.applocker.AppLocker.ApplicationListActivity.g",
    "com.goami.applocker.AppLocker.ApplicationListActivity.f",
    "com.goami.applocker.AppLocker.ApplicationListActivity.e",
    "com.goami.applocker.AppLocker.ApplicationListActivity$2.run",
    "res/layout/hint_set_accessibility.xml"
  ]
}
```

**补充说明（边界）**：本次为定向核验，未展开 `com.luna.powersaver.gp` 任务引擎（`ASAction.perform` 的 `performGlobalAction` 自动点击、`bgAutoInstallPage`/`bgAutoSureDialog` 自动安装 `com.photos.android.helper_release_241.apk`）的完整证据链；该部分属“获权后动作”，与本引导流程分离，若需定级需单独追溯。

</details>
