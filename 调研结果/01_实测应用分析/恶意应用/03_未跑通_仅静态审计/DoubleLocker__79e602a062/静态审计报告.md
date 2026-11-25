# MR_044__79e602a062｜DoubleLocker — Adobe Flash Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：206.2s

## 1. 一句话核心结论

- **核心申请方式**：以 Adobe Flash Player 为外壳、把无障碍服务伪装成 Google Play services，冷启动静默装服务后用半透明悬浮窗+100ms 定时器反复催促用户开启无障碍，开启后由服务自行模拟点击系统授权/卸载弹窗并屏蔽返回键，获权后改锁屏密码实现勒索。
- **静态可见性说明**：无加壳（预筛 False，DEX 可直接反编译），无 AES/远端 HTML，无内嵌二阶段 APK；引导文案为类内 XOR 字符串表（密钥 12,46,67,51,73），无障碍服务的 c[] 表已完整还原。仅悬浮窗引导类 s/E 的逐字文案表本轮未解码，属静态可还原但未展开。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `79e602a062d05fbb1409afc16e6d41ac0645576b2b5c1899dc93e6852c30a71f` |
| 包名 / 年份 | `owd.qusutsqfdo.mbpepvxhxly` / 2017 |
| 家族 / 品类 | **DoubleLocker**（同池样本数：1） |
| 原始来源标识 | https://www.welivesecurity.com/2017/10/13/doublelocker-innovative-android-malware/ |
| 桌面显示名 | Adobe Flash Player |
| 引导页宣称品牌/身份 | Adobe Flash Player（桌面入口）/ Google Play services（无障碍服务）/ Android default launcher（HOME 入口） |
| 系统无障碍列表服务名 | Google Play services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：三套互不一致的身份（Flash 播放器、Google Play 服务、默认桌面）；双入口伪装——LAUNCHER 类别 Activity 用 @string/app_name，另有 HOME 类别 Activity 用 @string/launcher_desc="Android default launcher" 且 excludeFromRecents+Fullscreen；无障碍服务 android:label 与 android:description 均写 "Google Play services"，description 与真实用途（自动点击系统弹窗、改锁屏密码）完全不符；命中特定窗口后 setComponentEnabledSetting 关闭自身启动器组件以隐藏图标；类名与字符串全量 XOR 混淆。 |
| 无障碍服务类名 | `.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_CONTACTS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Google Play services |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | owd.qusutsqfdo.mbpepvxhxly.LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll（LAUNCHER Activity，label=@string/app_name） | onCreate（用户点击“Adobe Flash Player”图标） | 原生Activity | **原文**：Adobe Flash Player<br>**译注**：桌面图标名“Adobe Flash Player”，点开后无任何界面 | 无交互；onCreate 内强制 setWifiEnabled(true)、反射开启数据网络、startService 拉起 IlllIIlllLllIllIIlllIllIlllIIIllIlIlILlLIllllIlIIIlLlIll 与 lLllIIllllIlllIlIIlILIIlIlLlIIllLlllllIIIllIlllllllIIlII 后立即 finish()，无取消/跳过按钮 | `owd.qusutsqfdo.mbpepvxhxly.LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll.onCreate` |
| 2 | 冷启动入口 | owd.qusutsqfdo.mbpepvxhxly.IlllIllIlIIlllllIlllllIIllIllIIIIllIlllllLllllLIILLIIIIl（HOME 类别 Activity，label=@string/launcher_desc） | onCreate，且 resolveActivity(MAIN/HOME) 结果指向自身包名时（被设为默认桌面后） | 原生Activity | **原文**：Android default launcher<br>**译注**：伪装成“Android 默认桌面”，全屏无标题、excludeFromRecents，并加 FLAG_SHOW_WHEN_LOCKED\|FLAG_DISMISS_KEYGUARD 以便在锁屏上显示 | 无交互；onCreate 内继续 startService 两个服务，并在 SDK<24 时 resetPassword(随机密码) 与 disableKeyguard() | `owd.qusutsqfdo.mbpepvxhxly.IlllIllIlIIlllllIlllllIIllIllIIIIllIlllllLllllLIILLIIIIl.onCreate / res/layout（setContentView 2130903044）` |
| 3 | 引导说明页 | 悬浮窗（WindowManager.addView，type=2010 TYPE_PHONE，dimAmount=0.65，layout 2130903041，含 Button 2131296291 与两个 TextView） | s.onClick(View) 被触发；正文用 Html.fromHtml(a[0]) 渲染，标题 a[1]；随后由 C 定时器（1000ms 延迟 / 100ms 周期）与 z 定时器反复重建 | 悬浮窗Overlay | **原文**：无（正文来自类 s 的 XOR 字符串表 a[0]/a[1]，本轮未解码，非 strings.xml 亦非 HTML 资源）<br>**译注**：半透明遮罩层上的一段 HTML 富文本说明 + 一个确认按钮，具体话术本轮未能逐字取得 | 点击遮罩上的确认 Button（E 为 OnClickListener）；遮罩层无取消/关闭入口，返回键被 F 广播回调以 performGlobalAction(2) 拦截 | `owd.qusutsqfdo.mbpepvxhxly.s.onClick / owd.qusutsqfdo.mbpepvxhxly.E / res/layout（2130903041）` |
| 4 | 跳受限设置 | 系统弹窗自动点击：com.android.packageinstaller.permission.ui.GrantPermissionsActivity、com.android.settings.DeviceAdminAdd、com.android.internal.app.ResolverActivity、com.android.phone.MobileNetworkSettings、com.android.packageinstaller.UninstallerActivity | onAccessibilityEvent(TYPE_WINDOW_STATE_CHANGED) 取 getRootInActiveWindow()，按窗口类名 switch 分派，对 android:id/button1、android:id/button_always、com.android.settings:id/action_button、android:id/cancel_button 等节点 performAction(16) 点击 | 系统无障碍页 | **原文**：android:id/button1;android:id/button_always;com.android.settings:id/action_button;com.android.settings:id/cancel_button<br>**译注**：直接点系统对话框的“确定/始终允许/激活”按钮（并可能点掉“取消”），由服务代替用户完成权限、设备管理器与卸载确认 | 用户无需操作；服务自动确认。未发现 ACTION_ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS 跳转，即应用不“教”用户去开无障碍，而是开启后接管系统弹窗 | `owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII.onAccessibilityEvent / #a` |
| 5 | 拒权反馈循环 | 定时器 C(1000ms,100ms) 与 z(1000ms,1000ms) + 悬浮窗重绘 + F 广播接收器 | onAccessibilityEvent 内 new C(this,1000,100).start()；异常分支 new z(this,1000,1000).start()；F 收到广播即 performGlobalAction(2) | 悬浮窗Overlay | 无 | 只能点确认按钮；无取消/跳过路径 | `owd.qusutsqfdo.mbpepvxhxly.C#<init> / owd.qusutsqfdo.mbpepvxhxly.z#<init> / owd.qusutsqfdo.mbpepvxhxly.F#onReceive` |
| 6 | 获权后动作 | 无障碍服务回调 + 自身组件开关 + 系统设置页 | onServiceConnected 设 flags=91/eventTypes=-1；onAccessibilityEvent 命中目标窗口后 setComponentEnabledSetting(自身启动器组件, DISABLED)，随后 startActivity(MAIN+HOME)+performGlobalAction(1)；f.onPostExecute 中 removeActiveAdmin、resetPassword、disableKeyguard、startActivity(APPLICATION_DETAILS_SETTINGS) | 系统无障碍页 | **原文**：android.intent.action.MAIN;android.intent.category.HOME<br>**译注**：隐藏桌面图标并跳回桌面以规避检测；改锁屏密码后弹出应用详情页引导卸载（DoubleLocker 勒索/锁屏模式） | 无；服务自点确认、自撤权后跳应用详情页 | `owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII#onServiceConnected / owd.qusutsqfdo.mbpepvxhxly.f#onPostExecute` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：android:label=@string/acs_desc="Google Play services"，android:description=@string/acs_desc（同一条字符串，用于欺骗用户在无障碍列表里认为这是 Google 服务）
- 桌面图标名：@string/app_name="Adobe Flash Player"（LAUNCHER Activity LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll）
- HOME 入口名：@string/launcher_desc="Android default launcher"（HOME 类别 Activity IlllIllIlIIlllllIlllllIIllIllIIIIllIlllllLllllLIILLIIIIl，被设为默认桌面时呈现）
- 悬浮窗遮罩：s.onClick 通过 WindowManager.addView(type=2010, dimAmount=0.65) 叠加 layout 2130903041，正文 TextView 用 Html.fromHtml(a[0])、标题 a[1]，文案在类 s 的 XOR 字符串表中（非 strings.xml、非 assets HTML）
- 无 strings.xml 长文案、无 assets/ HTML 页面、无 WebView 引导页；未发现 AlertDialog 或 Toast 形式文案（全 DEX 无 AlertDialog/setMessage 调用点）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Adobe Flash Player | Adobe Flash 播放器 | `res/values/strings.xml key=app_name（LAUNCHER Activity 的 android:label）` | 假更新 |
| en | Google Play services | Google Play 服务 | `res/values/strings.xml key=acs_desc（无障碍服务 android:label 与 android:description）` | 未知 |
| en | Android default launcher | Android 默认桌面 | `res/values/strings.xml key=launcher_desc（HOME 类别 Activity 的 android:label）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onAccessibilityEvent 内 new C(this,1000,100).start() 以 1s 延迟、100ms 周期不断重建悬浮窗；异常路径 new z(this,1000,1000).start()；F 注册广播接收器，onReceive 直接 performGlobalAction(2) 发 GLOBAL_ACTION_BACK，把用户从设置页/弹窗顶回，形成无法退出的循环；无障碍服务 flags=91 含 FILTER_KEY_EVENTS 与 RETRIEVE_INTERACTIVE_WINDOWS 支撑该拦截
- **遮罩叠层 / 高仿系统设置页**：是——WindowManager.addView type=2010(TYPE_PHONE)、dimAmount=0.65 的半透明遮罩引导窗，可叠加在系统设置/安装器/权限弹窗之上；未见高仿系统无障碍开关页（无自绘 toggle 界面，靠遮罩文案+按钮）
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk=16，无应用详情右上角受限设置教学、无 Session 安装器绕过逻辑）
- **获权后即时行为与防撤权机制**：有——F 广播回调 performGlobalAction(2) 阻止返回/撤权；获权后自点系统弹窗按钮（button1/button_always/action_button）完成自授权与自卸载确认；并 setComponentEnabledSetting 关闭自身启动器组件隐藏图标，startActivity(MAIN+HOME)+performGlobalAction(1) 回桌面规避
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两个时机：①进程启动后 LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll.onCreate 的 finish() 之后立即截屏（确认“无 UI 直启服务”）；②监测到 WindowManager.addView(type=2010) 或任何无障碍服务 enabled 事件后 300–800ms 截屏，抓取悬浮引导遮罩与其覆盖的底层页面。若设备已授予无障碍，则改为监测 GrantPermissionsActivity / DeviceAdminAdd 窗口出现瞬间截屏。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：①引导文案与按钮文字位于类 s/E 的 XOR 字符串表（本轮未解码），UTG 若只取无障碍服务 description 会漏掉真正话术，需在悬浮窗出现时 OCR/取文本；②应用会 setComponentEnabledSetting 关闭启动器组件并回桌面，图标消失后可能被误判为“未启动成功”，需以进程存活+悬浮窗出现为准；无纯图空文本诱导、无远端 HTML、无加壳（静态加壳不影响运行期 UTG）。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首个可见画面（应为空/桌面，用于证明零交互直装服务）** | 启动器 Activity 立即 finish，无布局；屏幕停留在桌面或上一应用 | 确认恶意行为不依赖任何用户点击业务入口，属 cold_start_0_step 静默链 | 无应用界面残留；系统桌面/锁屏层级；状态栏出现应用启动痕迹后立即消失 |
| **悬浮遮罩引导页（核心诱导页）** | type=2010 悬浮窗，全屏半透明压暗（dimAmount 0.65），含一段富文本说明与一个确认按钮 | 这是唯一承载引导话术的 UI，可据此判定诱导性质（假更新/故障恐吓/无障碍教学）并取得逐字文案 | 半透明遮罩下底层页面仍可见；遮罩无取消/关闭控件；按钮文本；正文富文本片段 |
| **系统无障碍服务列表项** | 设置 > 无障碍 中显示为 Google Play services 的服务条目 | 核对身份冒用（应用名 Adobe Flash Player 与服务名不一致），并作为开启无障碍的观测点 | 服务条目名称文本；条目描述文本；开关状态变化 |
| **设置页/弹窗被自动点击的瞬间** | GrantPermissionsActivity、DeviceAdminAdd、UninstallerActivity、ResolverActivity 窗口短暂出现后自行消失 | 证明授权与卸载确认由服务代点，而非用户操作；区分“教用户开无障碍”与“自行接管系统弹窗”两种完全不同性质 | 系统弹窗闪现后自动关闭；按钮被高亮点击痕迹；返回键无效 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `owd.qusutsqfdo.mbpepvxhxly.LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll.onCreate`
- `owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII.onAccessibilityEvent`
- `owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII#onServiceConnected`
- `owd.qusutsqfdo.mbpepvxhxly.s.onClick`
- `owd.qusutsqfdo.mbpepvxhxly.F.onReceive`
- `res/values/strings.xml（app_name / acs_desc / launcher_desc）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已按定向路径核验完毕（Manifest、资源、启动链、无障碍服务、悬浮窗与定时器）。核心结论如下。

**结论要点**

- **身份完全伪造**：桌面名 `Adobe Flash Player`，无障碍服务标签与 `android:description` 均伪装为 `Google Play services`；另有 HOME 类别 Activity 标签为 `Android default launcher`。三个名称互不相干，属于典型的品牌与系统组件冒用。
- **静态未见 `ACTION_ACCESSIBILITY_SETTINGS` 跳转**：全 DEX 搜索 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`android.settings` 均无命中；无障碍服务的 `c[]` 字符串表（XOR 解密后）只含系统组件类名与控件 ID（`GrantPermissionsActivity`、`DeviceAdminAdd`、`UninstallerActivity`、`android:id/button_always` 等），**没有设置页 URI**。也就是说，它**不教用户去点无障碍开关**，而是引导用户打开无障碍后，**由服务自己模拟点击系统弹窗**完成授权与卸载拦截。
- **真正的引导载体是悬浮窗遮罩**：[s.onClick()](<resource-unit:#1.dex1 code:owd.qusutsqfdo.mbpepvxhxly.s#onClick>) 以 `TYPE_PHONE(2010)`、`dimAmount=0.65` 的 `WindowManager.addView` 叠一层半透明引导窗（layout `2130903041`），正文由 `Html.fromHtml()` 渲染，并带一个确认 Button（`E`）。配合 [C](<resource-unit:#1.dex1 code:owd.qusutsqfdo.mbpepvxhxly.C#<init>>) 定时器（1000ms 延迟、100ms 周期）反复拉起，形成拒权重弹循环；[F.onReceive()](<resource-unit:#1.dex1 code:owd.qusutsqfdo.mbpepvxhxly.F#onReceive>) 在无障碍回调里注册广播，收到即 `performGlobalAction(2)`（GLOBAL_ACTION_BACK），阻断用户返回撤权。
- **无障碍服务本身是"自动授权/自动卸载"机器人**：[onServiceConnected()](<resource-unit:#1.dex1 code:owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII#onServiceConnected>) 设 `flags=91`（含 RETRIEVE_INTERACTIVE_WINDOWS 与 FILTER_KEY_EVENTS）、`eventTypes=-1`；[onAccessibilityEvent()](<resource-unit:#1.dex1 code:owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII#onAccessibilityEvent>) 按窗口类名分派，对 `android:id/button1`、`button_always`、`action_button` 直接 `performAction(16)` 点击；命中特定窗口时还用 `setComponentEnabledSetting` 关闭自身启动器组件（隐藏图标），并拉起 `MAIN+HOME` 后 `performGlobalAction(1)` 回桌面规避检测。
- **获权后（DoubleLocker 家族特征）**：`resetPassword()` 随机改锁屏密码、`disableKeyguard()`、`removeActiveAdmin`，并跳 `ACTION_APPLICATION_DETAILS_SETTINGS` 卸载自身。
- **未决项**：悬浮窗与 `E` 按钮的逐字文案位于 `s`/`E` 自身 XOR 字符串表，本轮未解码，因此遮罩页具体话术未能逐字引用。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无加壳（预筛 False，DEX 可直接反编译），无 AES/远端 HTML，无内嵌二阶段 APK；引导文案为类内 XOR 字符串表（密钥 12,46,67,51,73），无障碍服务的 c[] 表已完整还原。仅悬浮窗引导类 s/E 的逐字文案表本轮未解码，属静态可还原但未展开。",
  "summary_one_liner": "以 Adobe Flash Player 为外壳、把无障碍服务伪装成 Google Play services，冷启动静默装服务后用半透明悬浮窗+100ms 定时器反复催促用户开启无障碍，开启后由服务自行模拟点击系统授权/卸载弹窗并屏蔽返回键，获权后改锁屏密码实现勒索。",
  "disguise_identity": {
    "app_display_name": "Adobe Flash Player",
    "claimed_brand_or_persona": "Adobe Flash Player（桌面入口）/ Google Play services（无障碍服务）/ Android default launcher（HOME 入口）",
    "a11y_service_label": "Google Play services",
    "identity_mismatch": true,
    "obfuscation_tricks": "三套互不一致的身份（Flash 播放器、Google Play 服务、默认桌面）；双入口伪装——LAUNCHER 类别 Activity 用 @string/app_name，另有 HOME 类别 Activity 用 @string/launcher_desc=\"Android default launcher\" 且 excludeFromRecents+Fullscreen；无障碍服务 android:label 与 android:description 均写 \"Google Play services\"，description 与真实用途（自动点击系统弹窗、改锁屏密码）完全不符；命中特定窗口后 setComponentEnabledSetting 关闭自身启动器组件以隐藏图标；类名与字符串全量 XOR 混淆。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "owd.qusutsqfdo.mbpepvxhxly.LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll（LAUNCHER Activity，label=@string/app_name）",
      "trigger_event": "onCreate（用户点击“Adobe Flash Player”图标）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Adobe Flash Player",
      "shown_text_zh": "桌面图标名“Adobe Flash Player”，点开后无任何界面",
      "user_action_requested": "无交互；onCreate 内强制 setWifiEnabled(true)、反射开启数据网络、startService 拉起 IlllIIlllLllIllIIlllIllIlllIIIllIlIlILlLIllllIlIIIlLlIll 与 lLllIIllllIlllIlIIlILIIlIlLlIIllLlllllIIIllIlllllllIIlII 后立即 finish()，无取消/跳过按钮",
      "code_anchor": "owd.qusutsqfdo.mbpepvxhxly.LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "owd.qusutsqfdo.mbpepvxhxly.IlllIllIlIIlllllIlllllIIllIllIIIIllIlllllLllllLIILLIIIIl（HOME 类别 Activity，label=@string/launcher_desc）",
      "trigger_event": "onCreate，且 resolveActivity(MAIN/HOME) 结果指向自身包名时（被设为默认桌面后）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Android default launcher",
      "shown_text_zh": "伪装成“Android 默认桌面”，全屏无标题、excludeFromRecents，并加 FLAG_SHOW_WHEN_LOCKED|FLAG_DISMISS_KEYGUARD 以便在锁屏上显示",
      "user_action_requested": "无交互；onCreate 内继续 startService 两个服务，并在 SDK<24 时 resetPassword(随机密码) 与 disableKeyguard()",
      "code_anchor": "owd.qusutsqfdo.mbpepvxhxly.IlllIllIlIIlllllIlllllIIllIllIIIIllIlllllLllllLIILLIIIIl.onCreate / res/layout（setContentView 2130903044）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "悬浮窗（WindowManager.addView，type=2010 TYPE_PHONE，dimAmount=0.65，layout 2130903041，含 Button 2131296291 与两个 TextView）",
      "trigger_event": "s.onClick(View) 被触发；正文用 Html.fromHtml(a[0]) 渲染，标题 a[1]；随后由 C 定时器（1000ms 延迟 / 100ms 周期）与 z 定时器反复重建",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（正文来自类 s 的 XOR 字符串表 a[0]/a[1]，本轮未解码，非 strings.xml 亦非 HTML 资源）",
      "shown_text_zh": "半透明遮罩层上的一段 HTML 富文本说明 + 一个确认按钮，具体话术本轮未能逐字取得",
      "user_action_requested": "点击遮罩上的确认 Button（E 为 OnClickListener）；遮罩层无取消/关闭入口，返回键被 F 广播回调以 performGlobalAction(2) 拦截",
      "code_anchor": "owd.qusutsqfdo.mbpepvxhxly.s.onClick / owd.qusutsqfdo.mbpepvxhxly.E / res/layout（2130903041）"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统弹窗自动点击：com.android.packageinstaller.permission.ui.GrantPermissionsActivity、com.android.settings.DeviceAdminAdd、com.android.internal.app.ResolverActivity、com.android.phone.MobileNetworkSettings、com.android.packageinstaller.UninstallerActivity",
      "trigger_event": "onAccessibilityEvent(TYPE_WINDOW_STATE_CHANGED) 取 getRootInActiveWindow()，按窗口类名 switch 分派，对 android:id/button1、android:id/button_always、com.android.settings:id/action_button、android:id/cancel_button 等节点 performAction(16) 点击",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android:id/button1;android:id/button_always;com.android.settings:id/action_button;com.android.settings:id/cancel_button",
      "shown_text_zh": "直接点系统对话框的“确定/始终允许/激活”按钮（并可能点掉“取消”），由服务代替用户完成权限、设备管理器与卸载确认",
      "user_action_requested": "用户无需操作；服务自动确认。未发现 ACTION_ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS 跳转，即应用不“教”用户去开无障碍，而是开启后接管系统弹窗",
      "code_anchor": "owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII.onAccessibilityEvent / #a"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "定时器 C(1000ms,100ms) 与 z(1000ms,1000ms) + 悬浮窗重绘 + F 广播接收器",
      "trigger_event": "onAccessibilityEvent 内 new C(this,1000,100).start()；异常分支 new z(this,1000,1000).start()；F 收到广播即 performGlobalAction(2)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "高频重复压栈遮罩并回送 GLOBAL_ACTION_BACK，用户按返回即被顶回，无法退出引导层",
      "user_action_requested": "只能点确认按钮；无取消/跳过路径",
      "code_anchor": "owd.qusutsqfdo.mbpepvxhxly.C#<init> / owd.qusutsqfdo.mbpepvxhxly.z#<init> / owd.qusutsqfdo.mbpepvxhxly.F#onReceive"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务回调 + 自身组件开关 + 系统设置页",
      "trigger_event": "onServiceConnected 设 flags=91/eventTypes=-1；onAccessibilityEvent 命中目标窗口后 setComponentEnabledSetting(自身启动器组件, DISABLED)，随后 startActivity(MAIN+HOME)+performGlobalAction(1)；f.onPostExecute 中 removeActiveAdmin、resetPassword、disableKeyguard、startActivity(APPLICATION_DETAILS_SETTINGS)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.intent.action.MAIN;android.intent.category.HOME",
      "shown_text_zh": "隐藏桌面图标并跳回桌面以规避检测；改锁屏密码后弹出应用详情页引导卸载（DoubleLocker 勒索/锁屏模式）",
      "user_action_requested": "无；服务自点确认、自撤权后跳应用详情页",
      "code_anchor": "owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII#onServiceConnected / owd.qusutsqfdo.mbpepvxhxly.f#onPostExecute"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：android:label=@string/acs_desc=\"Google Play services\"，android:description=@string/acs_desc（同一条字符串，用于欺骗用户在无障碍列表里认为这是 Google 服务）",
    "桌面图标名：@string/app_name=\"Adobe Flash Player\"（LAUNCHER Activity LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll）",
    "HOME 入口名：@string/launcher_desc=\"Android default launcher\"（HOME 类别 Activity IlllIllIlIIlllllIlllllIIllIllIIIIllIlllllLllllLIILLIIIIl，被设为默认桌面时呈现）",
    "悬浮窗遮罩：s.onClick 通过 WindowManager.addView(type=2010, dimAmount=0.65) 叠加 layout 2130903041，正文 TextView 用 Html.fromHtml(a[0])、标题 a[1]，文案在类 s 的 XOR 字符串表中（非 strings.xml、非 assets HTML）",
    "无 strings.xml 长文案、无 assets/ HTML 页面、无 WebView 引导页；未发现 AlertDialog 或 Toast 形式文案（全 DEX 无 AlertDialog/setMessage 调用点）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Adobe Flash Player",
      "text_zh": "Adobe Flash 播放器",
      "source_location": "res/values/strings.xml key=app_name（LAUNCHER Activity 的 android:label）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play services",
      "text_zh": "Google Play 服务",
      "source_location": "res/values/strings.xml key=acs_desc（无障碍服务 android:label 与 android:description）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Android default launcher",
      "text_zh": "Android 默认桌面",
      "source_location": "res/values/strings.xml key=launcher_desc（HOME 类别 Activity 的 android:label）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onAccessibilityEvent 内 new C(this,1000,100).start() 以 1s 延迟、100ms 周期不断重建悬浮窗；异常路径 new z(this,1000,1000).start()；F 注册广播接收器，onReceive 直接 performGlobalAction(2) 发 GLOBAL_ACTION_BACK，把用户从设置页/弹窗顶回，形成无法退出的循环；无障碍服务 flags=91 含 FILTER_KEY_EVENTS 与 RETRIEVE_INTERACTIVE_WINDOWS 支撑该拦截",
    "overlay_or_fake_settings": "是——WindowManager.addView type=2010(TYPE_PHONE)、dimAmount=0.65 的半透明遮罩引导窗，可叠加在系统设置/安装器/权限弹窗之上；未见高仿系统无障碍开关页（无自绘 toggle 界面，靠遮罩文案+按钮）",
    "restricted_settings_13plus_coaching": "无（targetSdk=16，无应用详情右上角受限设置教学、无 Session 安装器绕过逻辑）",
    "post_grant_anti_removal": "有——F 广播回调 performGlobalAction(2) 阻止返回/撤权；获权后自点系统弹窗按钮（button1/button_always/action_button）完成自授权与自卸载确认；并 setComponentEnabledSetting 关闭自身启动器组件隐藏图标，startActivity(MAIN+HOME)+performGlobalAction(1) 回桌面规避",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两个时机：①进程启动后 LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll.onCreate 的 finish() 之后立即截屏（确认“无 UI 直启服务”）；②监测到 WindowManager.addView(type=2010) 或任何无障碍服务 enabled 事件后 300–800ms 截屏，抓取悬浮引导遮罩与其覆盖的底层页面。若设备已授予无障碍，则改为监测 GrantPermissionsActivity / DeviceAdminAdd 窗口出现瞬间截屏。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首个可见画面（应为空/桌面，用于证明零交互直装服务）",
        "page_identifier": "启动器 Activity 立即 finish，无布局；屏幕停留在桌面或上一应用",
        "why_most_useful": "确认恶意行为不依赖任何用户点击业务入口，属 cold_start_0_step 静默链",
        "observable_utg_signals": ["无应用界面残留", "系统桌面/锁屏层级", "状态栏出现应用启动痕迹后立即消失"]
      },
      {
        "page_role": "悬浮遮罩引导页（核心诱导页）",
        "page_identifier": "type=2010 悬浮窗，全屏半透明压暗（dimAmount 0.65），含一段富文本说明与一个确认按钮",
        "why_most_useful": "这是唯一承载引导话术的 UI，可据此判定诱导性质（假更新/故障恐吓/无障碍教学）并取得逐字文案",
        "observable_utg_signals": ["半透明遮罩下底层页面仍可见", "遮罩无取消/关闭控件", "按钮文本", "正文富文本片段"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 > 无障碍 中显示为 Google Play services 的服务条目",
        "why_most_useful": "核对身份冒用（应用名 Adobe Flash Player 与服务名不一致），并作为开启无障碍的观测点",
        "observable_utg_signals": ["服务条目名称文本", "条目描述文本", "开关状态变化"]
      },
      {
        "page_role": "设置页/弹窗被自动点击的瞬间",
        "page_identifier": "GrantPermissionsActivity、DeviceAdminAdd、UninstallerActivity、ResolverActivity 窗口短暂出现后自行消失",
        "why_most_useful": "证明授权与卸载确认由服务代点，而非用户操作；区分“教用户开无障碍”与“自行接管系统弹窗”两种完全不同性质",
        "observable_utg_signals": ["系统弹窗闪现后自动关闭", "按钮被高亮点击痕迹", "返回键无效"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：①引导文案与按钮文字位于类 s/E 的 XOR 字符串表（本轮未解码），UTG 若只取无障碍服务 description 会漏掉真正话术，需在悬浮窗出现时 OCR/取文本；②应用会 setComponentEnabledSetting 关闭启动器组件并回桌面，图标消失后可能被误判为“未启动成功”，需以进程存活+悬浮窗出现为准；无纯图空文本诱导、无远端 HTML、无加壳（静态加壳不影响运行期 UTG）。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "owd.qusutsqfdo.mbpepvxhxly.LlIIllllllLlllIlLIlllIllLlIllIlllIIlIIlIlIllIIIIlIIlIlll.onCreate",
    "owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII.onAccessibilityEvent",
    "owd.qusutsqfdo.mbpepvxhxly.lIllIIIllLlllIIIllIIlllLIlllIllIllIllLllIIILllIllllllIII#onServiceConnected",
    "owd.qusutsqfdo.mbpepvxhxly.s.onClick",
    "owd.qusutsqfdo.mbpepvxhxly.F.onReceive",
    "res/values/strings.xml（app_name / acs_desc / launcher_desc）"
  ]
}
```

**覆盖边界与未决**：本轮在 14 次调用约束下未解码悬浮窗类 `s`/`E` 的 XOR 文案表，故 `shown_text_verbatim` 如实标注为未取得；同时未对 DoubleLocker 特征链（`resetPassword`/勒索落地页）做独立定性与风险登记。

</details>
