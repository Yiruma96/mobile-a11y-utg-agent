# MR_130__ec5c0f1288｜TOASTAMIGO — Migo AppLocker

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：148.2s

## 1. 一句话核心结论

- **核心申请方式**：应用冷启动即在 ApplicationListActivity 弹出可取消的 'Attention' 原生引导框，教用户去 设置->无障碍->App Locker 打开开关，点确认后跳转系统无障碍页并同时压一层 #aa000000 半透明全屏 Toast 遮罩提示 'Find out Migo Applocker and open its accessibility switch'，取消则直接 finish 退出，每次 onResume 校验未获权就重弹，形成拒权回环。
- **静态可见性说明**：无障碍申请全链路（权限检测、引导弹窗、跳转 ACTION_ACCESSIBILITY_SETTINGS、全屏 Toast 遮罩、拒权回环）全部为明文 Java + 本地资源，可完整静态还原；唯一未静态可见部分是 onResume 中由 http://amigo.ws/get/ 下发的 'Version Check' 弹窗正文 updatetip 文案与是否弹出（update 字段），该部分属远端下发，但不影响无障碍引导判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ec5c0f12884158b179a5592002c8e9c10f17035afb27c1f66e53fca8b983e2c0` |
| 包名 / 年份 | `com.luna.applocker.gp` / 2017 |
| 家族 / 品类 | **TOASTAMIGO**（同池样本数：44） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/k/toast-overlay-weaponized-install-android-malware-single-attack-chain.html |
| 桌面显示名 | Migo AppLocker |
| 引导页宣称品牌/身份 | Migo AppLocker（自有品牌，配套域名 amigo.ws / 包名前缀 com.luna、com.noahmob） |
| 系统无障碍列表服务名 | Migo AppLocker |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅无障碍 description 存在拼写错误 'thr purpose'（非规避技巧）；未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool 字段。 |
| 无障碍服务类名 | `com.luna.applocker.gp.AppLocker.Service.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | The Service for thr purpose of Android 4.0.3 and above to lock apps easily. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.luna.applocker.gp.AppLocker.ApplicationListActivity（LAUNCHER，excludeFromRecents，singleInstance） | onCreate：读取 SharedPreferences 'data'.isfirst 判断首启；非首启 setContentView 并异步加载应用列表，随后 SDK>=15 调用 a(true) | 原生Activity | **原文**：Please wait / Gathering application...<br>**译注**：请稍候 / 正在收集应用…（加载进度框） | 无（等待列表加载完成） | `com.luna.applocker.gp.AppLocker.ApplicationListActivity.onCreate` |
| 2 | 冷启动入口 | SetPasswordActivity（首启分支） | onCreate 中 i() 返回 false（isfirst 未置位）时 finish() 并 startActivity(SetPasswordActivity)，埋点 FIRST_OPEN | 原生Activity | **原文**：无（密码设置页，字符串未在本轮核验）<br>**译注**：首次启动强制设置解锁密码 | 设置密码（前置必经步骤，完成后回到列表页） | `com.luna.applocker.gp.AppLocker.ApplicationListActivity.onCreate / i()` |
| 3 | 引导说明页 | com.luna.applocker.gp.AppLocker.a.b 自定义 AlertDialog（由 ApplicationListActivity.d() 构建） | a(boolean) 中 e()/f() 判定无障碍未启用 → g() 启动 DetectorService 前台服务 → d() 弹窗；onResume 中同样在未启用时调用 d() | 原生Dialog | **原文**：Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.<br>**译注**：注意 / 本设备版本高于 Android 4.0.3。请前往 设置->无障碍服务->App Locker 并将其打开。 | 点确定（跳转系统无障碍设置）或点取消（应用直接 finish 退出）；对话框 setCancelable(true)，可返回键取消 | `com.luna.applocker.gp.AppLocker.ApplicationListActivity.d；strings: alp_42447968_cmd_Attention / alp_42447968_cmd_android_m_above` |
| 4 | 跳无障碍设置 | 系统无障碍设置页（静态字段 k = new Intent("android.settings.ACCESSIBILITY_SETTINGS")） | ApplicationListActivity$4.a(Dialog)：上报埋点 ACCESS_START → ApplicationListActivity.c(this) → startActivity(k) | 系统无障碍页 | **原文**：Migo AppLocker / The Service for thr purpose of Android 4.0.3 and above to lock apps easily.<br>**译注**：Migo AppLocker / 该服务用于 Android 4.0.3 及以上系统以便捷地锁定应用。（系统无障碍列表中的服务名与说明） | 在系统无障碍列表中手动找到 Migo AppLocker 并打开其开关（无任何系统级跳转直达，需用户自行滑动查找） | `com.luna.applocker.gp.AppLocker.ApplicationListActivity.c；res/xml/phone_accessibility.xml；strings: accessibility_service_description` |
| 5 | 遮罩叠层指引 | 全屏 Toast 遮罩（layout hint_set_accessibility，背景 #aa000000，gravity=TOP，width/height=屏幕像素） | 与 startActivity(k) 同一方法体内立即 toast.show()，覆盖在刚跳转的系统设置页之上 | 悬浮窗Overlay | **原文**：Find out Migo Applocker and open its accessibility switch.<br>**译注**：找到 Migo Applocker 并打开它的无障碍开关。 | 按遮罩提示在设置页中找到对应条目并打开开关；遮罩 Toast 时长为 0（LONG），会自动消失 | `com.luna.applocker.gp.AppLocker.ApplicationListActivity.c；res/layout/hint_set_accessibility.xml；strings: str_set_accessibility_hint` |
| 6 | 拒权反馈循环 | 返回 ApplicationListActivity 的 onResume → 再次 d() 弹出同一 'Attention' 引导框；或用户点取消 → ApplicationListActivity$5.a → finish() 退出应用 | onResume：m 为 false 时执行 e()（getEnabledAccessibilityServiceList）与 f()（Settings.Secure.enabled_accessibility_services 含本服务 ID）双校验，均未通过则 d() | 原生Dialog | **原文**：Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.<br>**译注**：注意 / 本设备版本高于 Android 4.0.3。请前往 设置->无障碍服务->App Locker 并将其打开。 | 每次回到前台都必须再面对同一弹窗；取消即退出应用，无跳过或仅观看模式 | `com.luna.applocker.gp.AppLocker.ApplicationListActivity.onResume / e() / f() / ApplicationListActivity$5.a` |
| 7 | 引导说明页 | 远端下发 'Version Check' AlertDialog（a(ApplicationListActivity, String) 构建，setCancelable(false)、setCanceledOnTouchOutside(false)） | onResume → a() → accessibility.c.a() 请求 http://amigo.ws/get/?pakcage=com.luna.applocker.gp&vc=7&cn=0；响应 c==0 且 update==1 时置 m=true 并调用 a(this, jSONObject.optString("updatetip", ...)) | 原生Dialog | **原文**：Version Check / <updatetip 远端下发> / Go to Google Play<br>**译注**：版本检查 / 远端下发的更新提示文案 / 前往 Google Play | 仅有一个 'Go to Google Play' 按钮（ApplicationListActivity$3），不可取消、不可点外部关闭 | `com.luna.applocker.gp.AppLocker.ApplicationListActivity.a(ApplicationListActivity, String)；ApplicationListActivity$1.a；accessibility.c.a；strings: setting_item_service_upgrade / str_dialog_btn_go_store` |
| 8 | 获权后动作 | com.luna.applocker.gp.AppLocker.Service.MyAccessibilityService（无障碍服务本体）+ LockScreenActivity / LockScreenPatternActivity | onServiceConnected：注册 com.noahmob.AppLocker.applicationpassedtest 广播、上报 Flurry 'ACCESS_OPEN'、stopService(DetectorService)；onAccessibilityEvent 收到 TYPE_WINDOW_STATE_CHANGED(32) 且包名不在白名单时 b(pkgName) | 原生Activity | **原文**：无（锁屏页文案未在本轮核验）<br>**译注**：获权后按用户勾选的列表拦截目标应用，跳转密码/图案解锁页 | 输入预设密码或图案解锁被锁应用 | `com.luna.applocker.gp.AppLocker.Service.MyAccessibilityService.onServiceConnected / onAccessibilityEvent / a(String,String)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- ApplicationListActivity 内由 d() 构建的自定义 AlertDialog（com.luna.applocker.gp.AppLocker.a.b）：标题 'Attention'，正文为完整 Settings->AccessibilityService->App Locker 分步教学文案；setCancelable(true)
- 系统无障碍设置页中本服务条目：服务名 'Migo AppLocker'（@string/app_name）+ android:description 'The Service for thr purpose of Android 4.0.3 and above to lock apps easily.'（res/xml/phone_accessibility.xml 引用）
- 跳转 ACTION_ACCESSIBILITY_SETTINGS 后立即压栈的全屏 Toast 遮罩：res/layout/hint_set_accessibility.xml（#aa000000 半透明全屏）+ @string/str_set_accessibility_hint 'Find out Migo Applocker and open its accessibility switch.'
- 列表页加载时的 ProgressDialog：'Please wait' / 'Gathering application... '
- 远端下发后弹出的不可取消 'Version Check' 对话框：标题 @string/setting_item_service_upgrade、正文远端 updatetip、按钮 @string/str_dialog_btn_go_store 'Go to Google Play'
- 字符串资源中另存一条备用提示 @string/alp_42447968_cmd_android_m_above_toast 'Find Setting->AccessibilityService->App Locker and Open it.'（本轮未见调用点，疑为备用/Toast 变体）
- 无障碍服务异常/中断的反馈文案未在本次核验范围内（基类 com.luna.powersaver.gp.service.a 未展开）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Attention | 注意 | `res/values/strings.xml key=alp_42447968_cmd_Attention（被 ApplicationListActivity.d() 用作对话框标题）` | 受限设置分步教学 |
| en | This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. | 本设备版本高于 Android 4.0.3。请前往 设置->无障碍服务->App Locker 并将其打开。 | `res/values/strings.xml key=alp_42447968_cmd_android_m_above（ApplicationListActivity.d() 对话框正文）` | 受限设置分步教学 |
| en | Find Setting->AccessibilityService->App Locker and Open it. | 找到 设置->无障碍服务->App Locker 并打开它。 | `res/values/strings.xml key=alp_42447968_cmd_android_m_above_toast` | 受限设置分步教学 |
| en | Find out Migo Applocker and open its accessibility switch. | 找到 Migo Applocker 并打开它的无障碍开关。 | `res/values/strings.xml key=str_set_accessibility_hint（用于 res/layout/hint_set_accessibility.xml 全屏 Toast 遮罩）` | 受限设置分步教学 |
| en | The Service for thr purpose of Android 4.0.3 and above to lock apps easily. | 该服务用于 Android 4.0.3 及以上系统以便捷地锁定应用。 | `res/values/strings.xml key=accessibility_service_description（res/xml/phone_accessibility.xml 引用）` | 良性透明说明 |
| en | Version Check | 版本检查 | `res/values/strings.xml key=setting_item_service_upgrade（远端更新对话框标题）` | 假更新 |
| en | Go to Google Play | 前往 Google Play | `res/values/strings.xml key=str_dialog_btn_go_store（远端更新对话框唯一按钮）` | 假更新 |
| en | Please wait / Gathering application... | 请稍候 / 正在收集应用… | `ApplicationListActivity.onCreate 中 ProgressDialog.show 硬编码字符串` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：onResume 每次回到前台都以 e()（AccessibilityManager.getEnabledAccessibilityServiceList 遍历匹配 '<pkg>/.AppLocker.Service.MyAccessibilityService'）与 f()（读 Settings.Secure.accessibility_enabled 与 enabled_accessibility_services 冒号分隔列表）双重复核；两者均未通过就再次调用 d() 弹出同一 'Attention' 引导框。因此从系统设置页返回但未开启开关会立刻被再次弹窗；点负向按钮则 ApplicationListActivity$5.a 直接 finish() 退出应用，无跳过、无仅观看模式。另 DetectorService 会作为前台服务常驻并带通知保活，直到无障碍开启后由 onServiceConnected 停止。
- **遮罩叠层 / 高仿系统设置页**：跳转系统无障碍页的同时弹出全屏 Toast 遮罩：layout hint_set_accessibility（LinearLayout fill_parent、背景 #aa000000 半透明黑、gravity=TOP、TextView 白色文字 'Find out Migo Applocker and open its accessibility switch.'），以应用 Context 的 Toast（duration=0，即 LONG）覆盖在系统设置页之上作叠层指引。非高仿系统开关页，也未使用 SYSTEM_ALERT_WINDOW 悬浮窗（权限虽申请但本链用 Toast 实现遮罩）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。仅教用户走 设置->无障碍服务 路径，未出现进入应用详情页点右上角菜单允许受限设置的 13+ 教学，也未使用 Session 安装器绕过；未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转点（全包无该 action 调用点）。
- **获权后即时行为与防撤权机制**：本次核验范围内未见自点确认或自授权：onServiceConnected 仅 registerReceiver(com.noahmob.AppLocker.applicationpassedtest)、上报 Flurry 'ACCESS_OPEN'、stopService(DetectorService)。预筛线索提示无障碍基类 com.luna.powersaver.gp.service.a 含 PERFORM_GLOBAL_ACTION 等能力，该基类本轮未展开取证，撤权阻止行为待进一步确认。
- **良性降级 / 替代方案**：无。未提供手动模式、ADB 授权或仅观看等替代路径；用户拒绝即 finish() 退出应用，属强制前置授权而非降级运行。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 Activity 启动为钩子：检测到 com.luna.applocker.gp.AppLocker.ApplicationListActivity 的 onCreate/onResume（冷启动 0 步即弹窗），以及紧随其后的 startActivity(Intent action=android.settings.ACCESSIBILITY_SETTINGS) 跳转瞬间——该瞬间是抓取'跳转 + 全屏 Toast 遮罩'同帧证据的最佳时机。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：盲区有两处：一是远端 'Version Check' 弹窗正文 updatetip 与是否弹出由 http://amigo.ws/get/ 响应决定，纯静态不可见，需抓包或运行时观测；二是无障碍基类 com.luna.powersaver.gp.service.a（预筛含 PERFORM_GLOBAL_ACTION / WATCH_SETTINGS 等能力）本轮未展开，获权后是否存在撤权阻止/自动返回等行为需动态 Hook 或进一步逆向确认。引导文案全部为纯文本节点，无图片诱导，无需 OCR。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | ApplicationListActivity 之上叠加的自定义 AlertDialog，标题 'Attention'，正文含 'Settings->AccessibilityService->App Locker' | 这是全链路唯一的分步教学入口，可直接判定是否在启动即强推无障碍授权、是否提供取消路径 | AlertDialog 标题/正文文本节点 'Attention' 与 'Please Go Setting->AccessibilityService->App Locker and Open it.'；对话框按钮数量与是否可取消（两个按钮：确定/取消）；底层 Activity 为 ApplicationListActivity 且 excludeFromRecents |
| **设置页后压栈遮罩页** | 系统无障碍设置页上方叠加的半透明黑色全屏 Toast（#aa000000）+ 白色文字 'Find out Migo Applocker and open its accessibility switch.' | 验证是否用遮罩叠层把用户视线钉在系统设置页并给出具体开关指引，是区分'正常引导'与'压栈诱导'的关键证据 | 跳转后出现的全屏半透明覆盖节点与文本；覆盖层与系统设置页共存（叠层而非替换）；Toast 持续时长与消失后是否立即重跳 |
| **系统无障碍服务列表项** | 设置->无障碍 中的 'Migo AppLocker' 条目及说明 'The Service for thr purpose of Android 4.0.3 and above to lock apps easily.' | 核对服务名与桌面显示名是否一致、description 是否足以让用户知情（含 canRetrieveWindowContent=true 却未在说明中披露） | 条目名称 'Migo AppLocker'；description 原文与拼写错误 'thr purpose'；开关初始状态 |
| **拒权返回后的重弹页** | 从系统设置返回（未开启开关）后 ApplicationListActivity.onResume 再次弹出的同一 'Attention' 对话框 | 证明存在 onResume 级拒权回环而非一次性引导 | 返回前台后同一对话框文本再次出现的时间戳；取消按钮点击后应用进程/Activity 直接结束（finish）；多次往返的弹窗计数 |
| **远端假更新弹窗页** | 标题 'Version Check'、唯一按钮 'Go to Google Play'、setCancelable(false) 的 AlertDialog | 确认 amigo.ws 云控是否开启 update 分支（此时会置 m=true 并抑制无障碍弹窗），区分两条并行诱导链 | 对话框标题 'Version Check' 与按钮 'Go to Google Play'；无取消按钮/点击外部不消失；同一会话内无障碍弹窗是否被抑制 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.luna.applocker.gp.AppLocker.ApplicationListActivity.d`
- `com.luna.applocker.gp.AppLocker.ApplicationListActivity.c`
- `com.luna.applocker.gp.AppLocker.ApplicationListActivity.onResume`
- `com.luna.applocker.gp.AppLocker.ApplicationListActivity.e / f`
- `res/layout/hint_set_accessibility.xml`
- `res/xml/phone_accessibility.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：** 无障碍引导全链路（检测→弹窗→跳转→遮罩提示）全部为明文 Java 代码与本地资源，无加壳/加密；仅"版本检查"弹窗的提示文案来自远端 `http://amigo.ws/get/`。

**引导链路（已逐层核实）：**
1. 冷启动入口为 `ApplicationListActivity`（LAUNCHER，`excludeFromRecents`）。`onCreate` 首次启动走设密码流程，非首次则加载应用列表；`SDK>=15` 时调用 `a(true)`：已启用无障碍则停 `DetectorService`，**未启用则启动前台服务 + 立刻弹窗**。
2. 弹窗由 [d()](<resource-unit:#1.dex1 code:com.luna.applocker.gp.AppLocker.ApplicationListActivity#d>) 构建：标题 `alp_42447968_cmd_Attention`="Attention"，正文 `alp_42447968_cmd_android_m_above`="This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it."，`setCancelable(true)`，正/负两个按钮。
3. 正向按钮 `ApplicationListActivity$4.a` → 埋点 `ACCESS_START` → 调 [c()](<resource-unit:#1.dex1 code:com.luna.applocker.gp.AppLocker.ApplicationListActivity#c>)：`startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 同时 `Toast` 全屏压栈遮罩（`hint_set_accessibility`，背景 `#aa000000`，文字 "Find out Migo Applocker and open its accessibility switch."）。
4. 负向按钮 `ApplicationListActivity$5.a` → `finish()` 直接退出应用（不是降级）。
5. **拒权回环**：[onResume()](<resource-unit:#1.dex1 code:com.luna.applocker.gp.AppLocker.ApplicationListActivity#onResume>) 每次回到前台都做 `e()`（`getEnabledAccessibilityServiceList`）/`f()`（读 `Settings.Secure.enabled_accessibility_services`）双重校验，未开启就再次 `d()` 弹同一个不可跳过的引导框；从系统设置页返回未开开关即再次被弹。
6. **伴随的假更新诱导**：`onResume` 里 `accessibility.c.a()` 请求 `http://amigo.ws/get/?pakcage=com.luna.applocker.gp&vc=7&cn=0`，返回 `update==1` 时置 `m=true`（同时抑制无障碍弹窗）并弹出**不可取消**的 "Version Check" 对话框，正文为远端 `updatetip`，唯一按钮 `str_dialog_btn_go_store`="Go to Google Play"。
7. **获权后**：`MyAccessibilityService.onServiceConnected` 停止 `DetectorService`、注册 `com.noahmob.AppLocker.applicationpassedtest` 广播、上报 Flurry `ACCESS_OPEN`；`onAccessibilityEvent` 只处理 `TYPE_WINDOW_STATE_CHANGED(32)` 做应用锁拦截，跳过 `systemui`/`inputmethod`/`packageinstaller` 等，未在本链中发现自点确认式自授权。

**身份：** 显示名、无障碍服务标签、description 三处一致为 "Migo AppLocker"（description 有拼写错误 "thr purpose"），未发现品牌冒充或空白挤出技巧。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍申请全链路（权限检测、引导弹窗、跳转 ACTION_ACCESSIBILITY_SETTINGS、全屏 Toast 遮罩、拒权回环）全部为明文 Java + 本地资源，可完整静态还原；唯一未静态可见部分是 onResume 中由 http://amigo.ws/get/ 下发的 'Version Check' 弹窗正文 updatetip 文案与是否弹出（update 字段），该部分属远端下发，但不影响无障碍引导判定。",
  "summary_one_liner": "应用冷启动即在 ApplicationListActivity 弹出可取消的 'Attention' 原生引导框，教用户去 设置->无障碍->App Locker 打开开关，点确认后跳转系统无障碍页并同时压一层 #aa000000 半透明全屏 Toast 遮罩提示 'Find out Migo Applocker and open its accessibility switch'，取消则直接 finish 退出，每次 onResume 校验未获权就重弹，形成拒权回环。",
  "disguise_identity": {
    "app_display_name": "Migo AppLocker",
    "claimed_brand_or_persona": "Migo AppLocker（自有品牌，配套域名 amigo.ws / 包名前缀 com.luna、com.noahmob）",
    "a11y_service_label": "Migo AppLocker",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅无障碍 description 存在拼写错误 'thr purpose'（非规避技巧）；未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool 字段。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.luna.applocker.gp.AppLocker.ApplicationListActivity（LAUNCHER，excludeFromRecents，singleInstance）",
      "trigger_event": "onCreate：读取 SharedPreferences 'data'.isfirst 判断首启；非首启 setContentView 并异步加载应用列表，随后 SDK>=15 调用 a(true)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please wait / Gathering application... ",
      "shown_text_zh": "请稍候 / 正在收集应用…（加载进度框）",
      "user_action_requested": "无（等待列表加载完成）",
      "code_anchor": "com.luna.applocker.gp.AppLocker.ApplicationListActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "SetPasswordActivity（首启分支）",
      "trigger_event": "onCreate 中 i() 返回 false（isfirst 未置位）时 finish() 并 startActivity(SetPasswordActivity)，埋点 FIRST_OPEN",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（密码设置页，字符串未在本轮核验）",
      "shown_text_zh": "首次启动强制设置解锁密码",
      "user_action_requested": "设置密码（前置必经步骤，完成后回到列表页）",
      "code_anchor": "com.luna.applocker.gp.AppLocker.ApplicationListActivity.onCreate / i()"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.luna.applocker.gp.AppLocker.a.b 自定义 AlertDialog（由 ApplicationListActivity.d() 构建）",
      "trigger_event": "a(boolean) 中 e()/f() 判定无障碍未启用 → g() 启动 DetectorService 前台服务 → d() 弹窗；onResume 中同样在未启用时调用 d()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "shown_text_zh": "注意 / 本设备版本高于 Android 4.0.3。请前往 设置->无障碍服务->App Locker 并将其打开。",
      "user_action_requested": "点确定（跳转系统无障碍设置）或点取消（应用直接 finish 退出）；对话框 setCancelable(true)，可返回键取消",
      "code_anchor": "com.luna.applocker.gp.AppLocker.ApplicationListActivity.d；strings: alp_42447968_cmd_Attention / alp_42447968_cmd_android_m_above"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（静态字段 k = new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")）",
      "trigger_event": "ApplicationListActivity$4.a(Dialog)：上报埋点 ACCESS_START → ApplicationListActivity.c(this) → startActivity(k)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Migo AppLocker / The Service for thr purpose of Android 4.0.3 and above to lock apps easily.",
      "shown_text_zh": "Migo AppLocker / 该服务用于 Android 4.0.3 及以上系统以便捷地锁定应用。（系统无障碍列表中的服务名与说明）",
      "user_action_requested": "在系统无障碍列表中手动找到 Migo AppLocker 并打开其开关（无任何系统级跳转直达，需用户自行滑动查找）",
      "code_anchor": "com.luna.applocker.gp.AppLocker.ApplicationListActivity.c；res/xml/phone_accessibility.xml；strings: accessibility_service_description"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "全屏 Toast 遮罩（layout hint_set_accessibility，背景 #aa000000，gravity=TOP，width/height=屏幕像素）",
      "trigger_event": "与 startActivity(k) 同一方法体内立即 toast.show()，覆盖在刚跳转的系统设置页之上",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Find out Migo Applocker and open its accessibility switch.",
      "shown_text_zh": "找到 Migo Applocker 并打开它的无障碍开关。",
      "user_action_requested": "按遮罩提示在设置页中找到对应条目并打开开关；遮罩 Toast 时长为 0（LONG），会自动消失",
      "code_anchor": "com.luna.applocker.gp.AppLocker.ApplicationListActivity.c；res/layout/hint_set_accessibility.xml；strings: str_set_accessibility_hint"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 ApplicationListActivity 的 onResume → 再次 d() 弹出同一 'Attention' 引导框；或用户点取消 → ApplicationListActivity$5.a → finish() 退出应用",
      "trigger_event": "onResume：m 为 false 时执行 e()（getEnabledAccessibilityServiceList）与 f()（Settings.Secure.enabled_accessibility_services 含本服务 ID）双校验，均未通过则 d()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "shown_text_zh": "注意 / 本设备版本高于 Android 4.0.3。请前往 设置->无障碍服务->App Locker 并将其打开。",
      "user_action_requested": "每次回到前台都必须再面对同一弹窗；取消即退出应用，无跳过或仅观看模式",
      "code_anchor": "com.luna.applocker.gp.AppLocker.ApplicationListActivity.onResume / e() / f() / ApplicationListActivity$5.a"
    },
    {
      "step": 7,
      "stage": "引导说明页",
      "screen_or_component": "远端下发 'Version Check' AlertDialog（a(ApplicationListActivity, String) 构建，setCancelable(false)、setCanceledOnTouchOutside(false)）",
      "trigger_event": "onResume → a() → accessibility.c.a() 请求 http://amigo.ws/get/?pakcage=com.luna.applocker.gp&vc=7&cn=0；响应 c==0 且 update==1 时置 m=true 并调用 a(this, jSONObject.optString(\"updatetip\", ...))",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Version Check / <updatetip 远端下发> / Go to Google Play",
      "shown_text_zh": "版本检查 / 远端下发的更新提示文案 / 前往 Google Play",
      "user_action_requested": "仅有一个 'Go to Google Play' 按钮（ApplicationListActivity$3），不可取消、不可点外部关闭",
      "code_anchor": "com.luna.applocker.gp.AppLocker.ApplicationListActivity.a(ApplicationListActivity, String)；ApplicationListActivity$1.a；accessibility.c.a；strings: setting_item_service_upgrade / str_dialog_btn_go_store"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.luna.applocker.gp.AppLocker.Service.MyAccessibilityService（无障碍服务本体）+ LockScreenActivity / LockScreenPatternActivity",
      "trigger_event": "onServiceConnected：注册 com.noahmob.AppLocker.applicationpassedtest 广播、上报 Flurry 'ACCESS_OPEN'、stopService(DetectorService)；onAccessibilityEvent 收到 TYPE_WINDOW_STATE_CHANGED(32) 且包名不在白名单时 b(pkgName)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（锁屏页文案未在本轮核验）",
      "shown_text_zh": "获权后按用户勾选的列表拦截目标应用，跳转密码/图案解锁页",
      "user_action_requested": "输入预设密码或图案解锁被锁应用",
      "code_anchor": "com.luna.applocker.gp.AppLocker.Service.MyAccessibilityService.onServiceConnected / onAccessibilityEvent / a(String,String)"
    }
  ],
  "text_presentation_locations": [
    "ApplicationListActivity 内由 d() 构建的自定义 AlertDialog（com.luna.applocker.gp.AppLocker.a.b）：标题 'Attention'，正文为完整 Settings->AccessibilityService->App Locker 分步教学文案；setCancelable(true)",
    "系统无障碍设置页中本服务条目：服务名 'Migo AppLocker'（@string/app_name）+ android:description 'The Service for thr purpose of Android 4.0.3 and above to lock apps easily.'（res/xml/phone_accessibility.xml 引用）",
    "跳转 ACTION_ACCESSIBILITY_SETTINGS 后立即压栈的全屏 Toast 遮罩：res/layout/hint_set_accessibility.xml（#aa000000 半透明全屏）+ @string/str_set_accessibility_hint 'Find out Migo Applocker and open its accessibility switch.'",
    "列表页加载时的 ProgressDialog：'Please wait' / 'Gathering application... '",
    "远端下发后弹出的不可取消 'Version Check' 对话框：标题 @string/setting_item_service_upgrade、正文远端 updatetip、按钮 @string/str_dialog_btn_go_store 'Go to Google Play'",
    "字符串资源中另存一条备用提示 @string/alp_42447968_cmd_android_m_above_toast 'Find Setting->AccessibilityService->App Locker and Open it.'（本轮未见调用点，疑为备用/Toast 变体）",
    "无障碍服务异常/中断的反馈文案未在本次核验范围内（基类 com.luna.powersaver.gp.service.a 未展开）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Attention",
      "text_zh": "注意",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_Attention（被 ApplicationListActivity.d() 用作对话框标题）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "本设备版本高于 Android 4.0.3。请前往 设置->无障碍服务->App Locker 并将其打开。",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_android_m_above（ApplicationListActivity.d() 对话框正文）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Find Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "找到 设置->无障碍服务->App Locker 并打开它。",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_android_m_above_toast",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Find out Migo Applocker and open its accessibility switch.",
      "text_zh": "找到 Migo Applocker 并打开它的无障碍开关。",
      "source_location": "res/values/strings.xml key=str_set_accessibility_hint（用于 res/layout/hint_set_accessibility.xml 全屏 Toast 遮罩）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The Service for thr purpose of Android 4.0.3 and above to lock apps easily.",
      "text_zh": "该服务用于 Android 4.0.3 及以上系统以便捷地锁定应用。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（res/xml/phone_accessibility.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Version Check",
      "text_zh": "版本检查",
      "source_location": "res/values/strings.xml key=setting_item_service_upgrade（远端更新对话框标题）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to Google Play",
      "text_zh": "前往 Google Play",
      "source_location": "res/values/strings.xml key=str_dialog_btn_go_store（远端更新对话框唯一按钮）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Please wait / Gathering application... ",
      "text_zh": "请稍候 / 正在收集应用…",
      "source_location": "ApplicationListActivity.onCreate 中 ProgressDialog.show 硬编码字符串",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "onResume 每次回到前台都以 e()（AccessibilityManager.getEnabledAccessibilityServiceList 遍历匹配 '<pkg>/.AppLocker.Service.MyAccessibilityService'）与 f()（读 Settings.Secure.accessibility_enabled 与 enabled_accessibility_services 冒号分隔列表）双重复核；两者均未通过就再次调用 d() 弹出同一 'Attention' 引导框。因此从系统设置页返回但未开启开关会立刻被再次弹窗；点负向按钮则 ApplicationListActivity$5.a 直接 finish() 退出应用，无跳过、无仅观看模式。另 DetectorService 会作为前台服务常驻并带通知保活，直到无障碍开启后由 onServiceConnected 停止。",
    "overlay_or_fake_settings": "跳转系统无障碍页的同时弹出全屏 Toast 遮罩：layout hint_set_accessibility（LinearLayout fill_parent、背景 #aa000000 半透明黑、gravity=TOP、TextView 白色文字 'Find out Migo Applocker and open its accessibility switch.'），以应用 Context 的 Toast（duration=0，即 LONG）覆盖在系统设置页之上作叠层指引。非高仿系统开关页，也未使用 SYSTEM_ALERT_WINDOW 悬浮窗（权限虽申请但本链用 Toast 实现遮罩）。",
    "restricted_settings_13plus_coaching": "无。仅教用户走 设置->无障碍服务 路径，未出现进入应用详情页点右上角菜单允许受限设置的 13+ 教学，也未使用 Session 安装器绕过；未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转点（全包无该 action 调用点）。",
    "post_grant_anti_removal": "本次核验范围内未见自点确认或自授权：onServiceConnected 仅 registerReceiver(com.noahmob.AppLocker.applicationpassedtest)、上报 Flurry 'ACCESS_OPEN'、stopService(DetectorService)。预筛线索提示无障碍基类 com.luna.powersaver.gp.service.a 含 PERFORM_GLOBAL_ACTION 等能力，该基类本轮未展开取证，撤权阻止行为待进一步确认。",
    "benign_graceful_degradation": "无。未提供手动模式、ADB 授权或仅观看等替代路径；用户拒绝即 finish() 退出应用，属强制前置授权而非降级运行。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 Activity 启动为钩子：检测到 com.luna.applocker.gp.AppLocker.ApplicationListActivity 的 onCreate/onResume（冷启动 0 步即弹窗），以及紧随其后的 startActivity(Intent action=android.settings.ACCESSIBILITY_SETTINGS) 跳转瞬间——该瞬间是抓取'跳转 + 全屏 Toast 遮罩'同帧证据的最佳时机。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "ApplicationListActivity 之上叠加的自定义 AlertDialog，标题 'Attention'，正文含 'Settings->AccessibilityService->App Locker'",
        "why_most_useful": "这是全链路唯一的分步教学入口，可直接判定是否在启动即强推无障碍授权、是否提供取消路径",
        "observable_utg_signals": ["AlertDialog 标题/正文文本节点 'Attention' 与 'Please Go Setting->AccessibilityService->App Locker and Open it.'", "对话框按钮数量与是否可取消（两个按钮：确定/取消）", "底层 Activity 为 ApplicationListActivity 且 excludeFromRecents"]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "系统无障碍设置页上方叠加的半透明黑色全屏 Toast（#aa000000）+ 白色文字 'Find out Migo Applocker and open its accessibility switch.'",
        "why_most_useful": "验证是否用遮罩叠层把用户视线钉在系统设置页并给出具体开关指引，是区分'正常引导'与'压栈诱导'的关键证据",
        "observable_utg_signals": ["跳转后出现的全屏半透明覆盖节点与文本", "覆盖层与系统设置页共存（叠层而非替换）", "Toast 持续时长与消失后是否立即重跳"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置->无障碍 中的 'Migo AppLocker' 条目及说明 'The Service for thr purpose of Android 4.0.3 and above to lock apps easily.'",
        "why_most_useful": "核对服务名与桌面显示名是否一致、description 是否足以让用户知情（含 canRetrieveWindowContent=true 却未在说明中披露）",
        "observable_utg_signals": ["条目名称 'Migo AppLocker'", "description 原文与拼写错误 'thr purpose'", "开关初始状态"]
      },
      {
        "page_role": "拒权返回后的重弹页",
        "page_identifier": "从系统设置返回（未开启开关）后 ApplicationListActivity.onResume 再次弹出的同一 'Attention' 对话框",
        "why_most_useful": "证明存在 onResume 级拒权回环而非一次性引导",
        "observable_utg_signals": ["返回前台后同一对话框文本再次出现的时间戳", "取消按钮点击后应用进程/Activity 直接结束（finish）", "多次往返的弹窗计数"]
      },
      {
        "page_role": "远端假更新弹窗页",
        "page_identifier": "标题 'Version Check'、唯一按钮 'Go to Google Play'、setCancelable(false) 的 AlertDialog",
        "why_most_useful": "确认 amigo.ws 云控是否开启 update 分支（此时会置 m=true 并抑制无障碍弹窗），区分两条并行诱导链",
        "observable_utg_signals": ["对话框标题 'Version Check' 与按钮 'Go to Google Play'", "无取消按钮/点击外部不消失", "同一会话内无障碍弹窗是否被抑制"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "盲区有两处：一是远端 'Version Check' 弹窗正文 updatetip 与是否弹出由 http://amigo.ws/get/ 响应决定，纯静态不可见，需抓包或运行时观测；二是无障碍基类 com.luna.powersaver.gp.service.a（预筛含 PERFORM_GLOBAL_ACTION / WATCH_SETTINGS 等能力）本轮未展开，获权后是否存在撤权阻止/自动返回等行为需动态 Hook 或进一步逆向确认。引导文案全部为纯文本节点，无图片诱导，无需 OCR。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION"
  ],
  "code_anchors": [
    "com.luna.applocker.gp.AppLocker.ApplicationListActivity.d",
    "com.luna.applocker.gp.AppLocker.ApplicationListActivity.c",
    "com.luna.applocker.gp.AppLocker.ApplicationListActivity.onResume",
    "com.luna.applocker.gp.AppLocker.ApplicationListActivity.e / f",
    "res/layout/hint_set_accessibility.xml",
    "res/xml/phone_accessibility.xml"
  ]
}
```

</details>
