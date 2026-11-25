# MR_041__bbfb6dedc0｜BanBra — DEFENSOR ID

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：145.2s

## 1. 一句话核心结论

- **核心申请方式**：空壳主界面冷启动即弹出唯一按钮的不可取消 "Warning / Permission is needed" 弹窗，一步直跳系统无障碍列表，并在拒绝悬浮窗授权时递归重跳；获权后把设备注册为 Firebase 远控节点，执行锁屏/点击/文本读取/卸载等指令，锁屏由全屏 WebView GIF 遮罩实现。
- **静态可见性说明**：无障碍引导链 100% 静态可见：MainActivity.onCreate→Check_over_permission（悬浮窗跳转，requestCode 12）→AccessEnable_Check（读 Settings.Secure）→SetAccessEnable（不可取消 AlertDialog）→MainActivity$1.onClick（直跳 ACTION_ACCESSIBILITY_SETTINGS，requestCode 11）；获权后 CommandService 通过 Firebase Realtime Database 下发指令，指令值本身来自远端节点（remotebrazil.firebaseio.com），但本地解析与执行逻辑（command_run 的 14 个指令分支）完整静态可见。无加壳、无 DEX 密文二阶段、无远端 HTML 引导页（help.html 为本地 assets）。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `bbfb6dedc01492ca3ac0c4f77343a22162518b306660e9ce958f2a6369ffaf13` |
| 包名 / 年份 | `com.secure.protect.world` / 2020 |
| 家族 / 品类 | **BanBra**（同池样本数：2） |
| 原始来源标识 | https://www.welivesecurity.com/2020/05/22/insidious-android-malware-gives-up-all-malicious-features-but-one-gain-stealth/ |
| 桌面显示名 | DEFENSOR ID |
| 引导页宣称品牌/身份 | DEFENSOR ID（公共辩护人/身份保护类安全工具人设） |
| 系统无障碍列表服务名 | DEFENSOR ID |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍 android:description 被压缩为极简模糊文案 "Please check the permission for App"，不披露 typeAllMask 全事件监听、canRetrieveWindowContent 读取全部窗口内容与 canPerformGestures 手势注入；服务标签复用 app_name 冒充同一安全品牌；assets/help.html 标题残留 "FakeLock \| Help" 与 author=varunon9，泄露真实用途为远程锁屏控制；未使用空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool |
| 无障碍服务类名 | `com.brazil.android.free.CommandService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Please check the permission for App |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.brazil.android.free.MainActivity（LAUNCHER，AppCompatActivity） | onCreate() 无条件顺序调用 Check_over_permission() → AccessEnable_Check() → SetAccessEnable() → setTime_android() | 原生Activity | **原文**：Beginning Android<br>**译注**：界面唯一可见文字为 "Beginning Android"，无任何业务功能控件（空壳主界面） | 无显式要求；用户仅看到空壳页面，随即被后续设置页与弹窗接管 | `com.brazil.android.free.MainActivity.onCreate / res/layout/activity_main.xml` |
| 2 | 跳受限设置 | 系统悬浮窗授权页 android.settings.action.MANAGE_OVERLAY_PERMISSION（startActivityForResult，requestCode 12） | onCreate 中 Check_over_permission()：Build.VERSION.SDK_INT >= 23 且 Settings.canDrawOverlays(this) 为 false | 系统设置页 | **原文**：无（应用不自绘文案，直接拉起系统悬浮窗权限页）<br>**译注**：系统「显示在其他应用上层」授权页，无任何前置说明 | 要求用户在系统页允许悬浮窗权限；应用侧未提供跳过路径 | `com.brazil.android.free.MainActivity.Check_over_permission` |
| 3 | 引导说明页 | 原生 AlertDialog（androidx.appcompat.app.AlertDialog.Builder） | AccessEnable_Check() 返回 false（Settings.Secure.accessibility_enabled != 1 或 enabled_accessibility_services 不含 "com.secure.protect.world/com.brazil.android.free.CommandService"） | 原生Dialog | **原文**：Title: Warning \| Message: Permission is needed \| PositiveButton: OK<br>**译注**：标题「警告」，正文「需要权限」，唯一按钮「确定」 | 只能点击「OK」；setCancelable(false) 且无 NegativeButton/NeutralButton，返回键与点击外部均无法关闭，无取消或跳过选项 | `com.brazil.android.free.MainActivity.SetAccessEnable` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表 android.settings.ACCESSIBILITY_SETTINGS（startActivityForResult，requestCode 11） | 用户在步骤 3 弹窗点击 OK → MainActivity$1.onClick(DialogInterface, int) | 系统无障碍页 | **原文**：无（应用不自绘教学页/遮罩，直接跳系统列表；列表项名称取自 android:label="@string/app_name"）<br>**译注**：系统无障碍列表中出现名为「DEFENSOR ID」的服务项，其说明为「Please check the permission for App（请为应用检查该权限）」 | 要求用户自行在系统列表中找到「DEFENSOR ID」并手动开启开关；无分步图示教学、无设置页叠加引导窗 | `com.brazil.android.free.MainActivity$1.onClick / res/xml/config_service.xml / res/values/strings.xml(description)` |
| 5 | 拒权反馈循环 | MainActivity.onActivityResult 递归重跳 MANAGE_OVERLAY_PERMISSION；无障碍弹窗不重复 | onActivityResult(requestCode=12) 未获授权 → 再次调用 Check_over_permission()；requestCode=11 无任何处理分支，onResume() 无逻辑 | 系统设置页 | 无 | 循环要求授予悬浮窗权限；无障碍环节无运行期强制重弹 | `com.brazil.android.free.MainActivity.onActivityResult` |
| 6 | 获权后动作 | com.brazil.android.free.CommandService（AccessibilityService）→ Firebase Realtime Database 指令节点 → com.brazil.android.free.TopService 全屏 WebView 遮罩 | onServiceConnected() 设置 eventTypes=-1/flags=89 后 Configure_command() 建立 /<android_id>/cmd 子节点监听；CommandService$2.onChildChanged 触发 command_run()；收到 lock 指令时 startService(TopService) | 悬浮窗Overlay | **原文**：FakeLock \| Help（help.html <title>）；页面主体为 <img src="sample.gif">；通知文案 "DEFENSOR ID is running in background"<br>**译注**：全屏悬浮 WebView 仅展示一张 GIF 图片，标题残留「FakeLock \| Help」；前台通知自称「DEFENSOR ID 正在后台运行」 | 无正常交互可能：onTouch 恒返回 true 吞掉全部触摸，用户无法操作或关闭该层；同时可被远程执行 back/home/recent/click/text/uninstall 等指令 | `com.brazil.android.free.CommandService.onServiceConnected / Configure_command / command_run / com.brazil.android.free.TopService.onCreate / assets/help.html` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 冷启动原生 AlertDialog（setCancelable(false)，标题 "Warning"、正文 "Permission is needed"、唯一按钮 "OK"）——无障碍申请的唯一解释性文案载体
- 系统无障碍服务列表项：android:label="@string/app_name" 显示为 "DEFENSOR ID"，android:description="Please check the permission for App"（res/values/strings.xml 中 key=description）
- 系统悬浮窗授权页 MANAGE_OVERLAY_PERMISSION：应用不自绘任何说明，直接跳转
- 主界面 res/layout/activity_main.xml 仅一个 TextView 文本 "Beginning Android"（空壳，无引导文字）
- TopService 全屏悬浮窗 WebView 加载 file:///android_asset/help.html：<title>FakeLock | Help</title>，正文仅 <img src="sample.gif">，页面无文字说明
- 前台通知：NotificationChannel "DEFENSOR ID" / 通知标题 "DEFENSOR ID is running in background"
- 无障碍权限被拒后的唯一反馈为反复拉起系统悬浮窗授权页，无文字提示

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Warning | 警告 | `硬编码类 com.brazil.android.free.MainActivity#SetAccessEnable（AlertDialog.setTitle）` | 故障恐吓 |
| en | Permission is needed | 需要权限 | `硬编码类 com.brazil.android.free.MainActivity#SetAccessEnable（AlertDialog.setMessage）` | 假反诈安全 |
| en | Please check the permission for App | 请为应用检查该权限 | `res/values/strings.xml key=description（config_service.xml android:description）` | 未知 |
| en | Beginning Android | 开始使用 Android | `res/layout/activity_main.xml（TextView android:text）` | 未知 |
| en | FakeLock \| Help | FakeLock｜帮助 | `assets/help.html <title>` | 未知 |
| en | DEFENSOR ID is running in background | DEFENSOR ID 正在后台运行 | `硬编码类 com.brazil.android.free.CommandService#startMyOwnForeground（NotificationCompat setContentTitle）` | 良性透明说明 |
| en | %1$s is having trouble with Google Play services. Please try again. | %1$s 无法访问 Google Play 服务，请重试。 | `res/values/strings.xml key=common_google_play_services_unknown_issue（GMS 标准资源，非自研文案）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无障碍弹窗本身为 setCancelable(false) 且无取消按钮；requestCode=11 无处理、onResume() 无逻辑，故从无障碍设置返回不会立即重弹（需再次冷启动）。但前置的悬浮窗环节 requestCode=12 未授权时 onActivityResult 直接递归调用 Check_over_permission()，形成无限次拉起 MANAGE_OVERLAY_PERMISSION 的拒权循环。
- **遮罩叠层 / 高仿系统设置页**：无设置页遮罩、无高仿无障碍开关页；但获权后由远控 lock 指令启动 TopService，以 TYPE_APPLICATION_OVERLAY 全屏 WebView（help.html + sample.gif，onTouch 恒 true）叠放整屏遮罩，吞掉全部触摸阻止用户操作。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无自点确认/自授权；performGlobalAction 仅作为远控 back/home/recent 指令使用，未见监听设置页并阻止撤权的逻辑
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 MainActivity 冷启动后监测到 intent 目标为 android.settings.action.MANAGE_OVERLAY_PERMISSION 或 android.settings.ACCESSIBILITY_SETTINGS 的瞬间拉起 UTG；并同步在 MainActivity.onCreate 返回后（首个 AlertDialog 显示）立即抓取当前窗口层级。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：引导链本体无盲区（文案为硬编码字符串，非远端 HTML/AES）。存在两点需注意：其一，TopService 遮罩页仅呈现 assets/sample.gif 图片，纯 UTG 文本抓取为空，需 OCR 或截图比对才能识别其内容；其二，远控指令集来自 Firebase 远端节点（remotebrazil.firebaseio.com），指令内容与下发时机无法静态枚举，需运行期抓包/DNS 观察才能确认实际触发的行为（如 lock、uninstall）。另，应用自述名称 DEFENSOR ID 属人设伪装，非静态加壳，不影响运行期 UTG 捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 包名 com.secure.protect.world 的 AlertDialog 窗口，标题 "Warning"、正文 "Permission is needed"、仅一个 "OK" 按钮 | 这是该应用唯一的无障碍申请解释文案载体，且不可取消、无拒绝按钮，可直接证明诱导与无退出路径 | Dialog 节点 cancelable=false / 无 negative/neutral button；标题与正文文案原文；弹窗出现时机紧接冷启动（0 步交互） |
| **系统悬浮窗授权页（跳转前置页）** | com.android.settings 的 MANAGE_OVERLAY_PERMISSION 页面，由 requestCode 12 拉起 | 证明应用在无障碍之前先索要悬浮窗（后续全屏遮罩所必需），且拒绝后会被递归重跳，是判定拒权循环的关键 | 同一 intent 在短时间内多次重复出现；拒绝后 1~2 秒内再次进入该页；页面出现时应用自身无任何说明 UI |
| **系统无障碍服务列表项** | Settings 无障碍列表中 label="DEFENSOR ID"、summary="Please check the permission for App" 的服务条目 | 核对系统侧展示名与描述是否与实际能力（全事件监听 + 读窗口内容 + 手势注入）严重不符，是身份误导的直接证据 | 服务条目文本 DEFENSOR ID；说明文本 Please check the permission for App；条目与桌面应用名完全一致（无二次辨识信息） |
| **获权后远控锁屏遮罩页** | 非 Activity 的全屏 TYPE_APPLICATION_OVERLAY WebView，内容为单张 GIF，页面标题 FakeLock \| Help | 证明无障碍权限被用于远程控制与锁屏压制，而非宣称的安全防护；同时说明遮罩拦截触摸使受害者无法自救 | 窗口类型为 overlay 且覆盖全屏（非应用自身 Activity）；WebView 内容仅一张图片、无文字节点；所有触摸事件被消费、界面无响应；前台通知 DEFENSOR ID is running in background 同时存在 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.brazil.android.free.MainActivity.onCreate`
- `com.brazil.android.free.MainActivity.SetAccessEnable`
- `com.brazil.android.free.MainActivity$1.onClick`
- `com.brazil.android.free.MainActivity.onActivityResult`
- `res/xml/config_service.xml`
- `assets/help.html`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**权限引导链（纯运行期 UTG 视角，全部静态可见，无加壳、无密文载荷）**

1. **冷启动即拦截**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.brazil.android.free.MainActivity#onCreate>) 无任何条件分支地依次执行 `Check_over_permission()` → `AccessEnable_Check()` → `SetAccessEnable()`。主界面 [activity_main.xml](<resource-unit:#1 file:res/layout/activity_main.xml>) 仅有一个写着 "Beginning Android" 的 TextView，是典型空壳，无实际业务功能。
2. **先跳悬浮窗设置**：[Check_over_permission()](<resource-unit:#1.dex1 code:com.brazil.android.free.MainActivity#Check_over_permission>) 在 `canDrawOverlays` 为假时跳 `android.settings.action.MANAGE_OVERLAY_PERMISSION`（requestCode 12）；[onActivityResult()](<resource-unit:#1.dex1 code:com.brazil.android.free.MainActivity#onActivityResult>) 中 12 未授权即递归重跳，构成**拒权重跳循环**。
3. **不可取消的原生弹窗**：[SetAccessEnable()](<resource-unit:#1.dex1 code:com.brazil.android.free.MainActivity#SetAccessEnable>) 为 `AlertDialog`，`setTitle("Warning")`、`setMessage("Permission is needed")`、`setCancelable(false)`，**只有 "OK" 按钮，无取消/跳过/稍后**。
4. **一步直跳无障碍列表**：[MainActivity$1.onClick()](<resource-unit:#1.dex1 code:com.brazil.android.free.MainActivity$1#onClick>) 直接 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 11)`——**无分步教学、无 WebView 说明页、无高仿设置页、无设置页叠加遮罩**；`onResume` 无逻辑，requestCode 11 也无处理，返回后需冷启动才会重现弹窗。
5. **获权后立即转为远控**：[CommandService.onServiceConnected()](<resource-unit:#1.dex1 code:com.brazil.android.free.CommandService#onServiceConnected>) 设 `eventTypes=-1`、`flags=89`（全事件 + 读窗口内容 + 手势），以 `android_id` 在 Firebase（`remotebrazil.firebaseio.com`）注册 `cmd` 节点并监听，[command_run()](<resource-unit:#1.dex1 code:com.brazil.android.free.CommandService#command_run>) 执行 back/home/recent/click/text/uninstall/lock 等指令；`lock` 拉起 [TopService.onCreate()](<resource-unit:#1.dex1 code:com.brazil.android.free.TopService#onCreate>)，用全屏 WebView 加载 [assets/help.html](<resource-unit:#1 file:assets/help.html>)（仅一张 sample.gif，`onTouch` 恒返回 true 吞掉触摸）形成锁屏遮罩。

**伪装特征**：桌面名与服务标签均为 `DEFENSOR ID`（安全防护/身份名义），无障碍描述仅为 `Please check the permission for App`（[strings.xml](<resource-unit:#1 file:res/values/strings.xml>)），完全未告知"读取全部窗口内容 + 注入手势"；而 help.html 标题仍残留 `FakeLock | Help` 与作者 `github.com/varunon9`，暴露真实用途为远程锁屏控制。`config_service.xml` 声明 `typeAllMask`、`canRetrieveWindowContent`、`canPerformGestures`。

**边界说明**：预筛线索中的 `SESSION_INSTALLER` / `RESTRICTED_STR` 在本包应用代码中无对应实现（`RESTRICTED` 命中均为 androidx 框架字段），targetSdk 29 亦无 Android 13 受限设置分步教学；无 13+ 教唆、无自授权、无 `GLOBAL_ACTION_BACK` 阻止撤权（`performGlobalAction` 仅用于远控指令）。

已登记风险 **R-001**（malware_trojan / high）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链 100% 静态可见：MainActivity.onCreate→Check_over_permission（悬浮窗跳转，requestCode 12）→AccessEnable_Check（读 Settings.Secure）→SetAccessEnable（不可取消 AlertDialog）→MainActivity$1.onClick（直跳 ACTION_ACCESSIBILITY_SETTINGS，requestCode 11）；获权后 CommandService 通过 Firebase Realtime Database 下发指令，指令值本身来自远端节点（remotebrazil.firebaseio.com），但本地解析与执行逻辑（command_run 的 14 个指令分支）完整静态可见。无加壳、无 DEX 密文二阶段、无远端 HTML 引导页（help.html 为本地 assets）。",
  "summary_one_liner": "空壳主界面冷启动即弹出唯一按钮的不可取消 \"Warning / Permission is needed\" 弹窗，一步直跳系统无障碍列表，并在拒绝悬浮窗授权时递归重跳；获权后把设备注册为 Firebase 远控节点，执行锁屏/点击/文本读取/卸载等指令，锁屏由全屏 WebView GIF 遮罩实现。",
  "disguise_identity": {
    "app_display_name": "DEFENSOR ID",
    "claimed_brand_or_persona": "DEFENSOR ID（公共辩护人/身份保护类安全工具人设）",
    "a11y_service_label": "DEFENSOR ID",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍 android:description 被压缩为极简模糊文案 \"Please check the permission for App\"，不披露 typeAllMask 全事件监听、canRetrieveWindowContent 读取全部窗口内容与 canPerformGestures 手势注入；服务标签复用 app_name 冒充同一安全品牌；assets/help.html 标题残留 \"FakeLock | Help\" 与 author=varunon9，泄露真实用途为远程锁屏控制；未使用空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.brazil.android.free.MainActivity（LAUNCHER，AppCompatActivity）",
      "trigger_event": "onCreate() 无条件顺序调用 Check_over_permission() → AccessEnable_Check() → SetAccessEnable() → setTime_android()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Beginning Android",
      "shown_text_zh": "界面唯一可见文字为 \"Beginning Android\"，无任何业务功能控件（空壳主界面）",
      "user_action_requested": "无显式要求；用户仅看到空壳页面，随即被后续设置页与弹窗接管",
      "code_anchor": "com.brazil.android.free.MainActivity.onCreate / res/layout/activity_main.xml"
    },
    {
      "step": 2,
      "stage": "跳受限设置",
      "screen_or_component": "系统悬浮窗授权页 android.settings.action.MANAGE_OVERLAY_PERMISSION（startActivityForResult，requestCode 12）",
      "trigger_event": "onCreate 中 Check_over_permission()：Build.VERSION.SDK_INT >= 23 且 Settings.canDrawOverlays(this) 为 false",
      "ui_carrier": "系统设置页",
      "shown_text_verbatim": "无（应用不自绘文案，直接拉起系统悬浮窗权限页）",
      "shown_text_zh": "系统「显示在其他应用上层」授权页，无任何前置说明",
      "user_action_requested": "要求用户在系统页允许悬浮窗权限；应用侧未提供跳过路径",
      "code_anchor": "com.brazil.android.free.MainActivity.Check_over_permission"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "原生 AlertDialog（androidx.appcompat.app.AlertDialog.Builder）",
      "trigger_event": "AccessEnable_Check() 返回 false（Settings.Secure.accessibility_enabled != 1 或 enabled_accessibility_services 不含 \"com.secure.protect.world/com.brazil.android.free.CommandService\"）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: Warning | Message: Permission is needed | PositiveButton: OK",
      "shown_text_zh": "标题「警告」，正文「需要权限」，唯一按钮「确定」",
      "user_action_requested": "只能点击「OK」；setCancelable(false) 且无 NegativeButton/NeutralButton，返回键与点击外部均无法关闭，无取消或跳过选项",
      "code_anchor": "com.brazil.android.free.MainActivity.SetAccessEnable"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表 android.settings.ACCESSIBILITY_SETTINGS（startActivityForResult，requestCode 11）",
      "trigger_event": "用户在步骤 3 弹窗点击 OK → MainActivity$1.onClick(DialogInterface, int)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用不自绘教学页/遮罩，直接跳系统列表；列表项名称取自 android:label=\"@string/app_name\"）",
      "shown_text_zh": "系统无障碍列表中出现名为「DEFENSOR ID」的服务项，其说明为「Please check the permission for App（请为应用检查该权限）」",
      "user_action_requested": "要求用户自行在系统列表中找到「DEFENSOR ID」并手动开启开关；无分步图示教学、无设置页叠加引导窗",
      "code_anchor": "com.brazil.android.free.MainActivity$1.onClick / res/xml/config_service.xml / res/values/strings.xml(description)"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onActivityResult 递归重跳 MANAGE_OVERLAY_PERMISSION；无障碍弹窗不重复",
      "trigger_event": "onActivityResult(requestCode=12) 未获授权 → 再次调用 Check_over_permission()；requestCode=11 无任何处理分支，onResume() 无逻辑",
      "ui_carrier": "系统设置页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "拒绝悬浮窗权限会被无限次重新拉起系统授权页；从无障碍设置页直接返回则停在空壳主界面，需再次冷启动才会重新弹出步骤 3 弹窗",
      "user_action_requested": "循环要求授予悬浮窗权限；无障碍环节无运行期强制重弹",
      "code_anchor": "com.brazil.android.free.MainActivity.onActivityResult"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.brazil.android.free.CommandService（AccessibilityService）→ Firebase Realtime Database 指令节点 → com.brazil.android.free.TopService 全屏 WebView 遮罩",
      "trigger_event": "onServiceConnected() 设置 eventTypes=-1/flags=89 后 Configure_command() 建立 /<android_id>/cmd 子节点监听；CommandService$2.onChildChanged 触发 command_run()；收到 lock 指令时 startService(TopService)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "FakeLock | Help（help.html <title>）；页面主体为 <img src=\"sample.gif\">；通知文案 \"DEFENSOR ID is running in background\"",
      "shown_text_zh": "全屏悬浮 WebView 仅展示一张 GIF 图片，标题残留「FakeLock | Help」；前台通知自称「DEFENSOR ID 正在后台运行」",
      "user_action_requested": "无正常交互可能：onTouch 恒返回 true 吞掉全部触摸，用户无法操作或关闭该层；同时可被远程执行 back/home/recent/click/text/uninstall 等指令",
      "code_anchor": "com.brazil.android.free.CommandService.onServiceConnected / Configure_command / command_run / com.brazil.android.free.TopService.onCreate / assets/help.html"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 冷启动原生 AlertDialog（setCancelable(false)，标题 \"Warning\"、正文 \"Permission is needed\"、唯一按钮 \"OK\"）——无障碍申请的唯一解释性文案载体",
    "系统无障碍服务列表项：android:label=\"@string/app_name\" 显示为 \"DEFENSOR ID\"，android:description=\"Please check the permission for App\"（res/values/strings.xml 中 key=description）",
    "系统悬浮窗授权页 MANAGE_OVERLAY_PERMISSION：应用不自绘任何说明，直接跳转",
    "主界面 res/layout/activity_main.xml 仅一个 TextView 文本 \"Beginning Android\"（空壳，无引导文字）",
    "TopService 全屏悬浮窗 WebView 加载 file:///android_asset/help.html：<title>FakeLock | Help</title>，正文仅 <img src=\"sample.gif\">，页面无文字说明",
    "前台通知：NotificationChannel \"DEFENSOR ID\" / 通知标题 \"DEFENSOR ID is running in background\"",
    "无障碍权限被拒后的唯一反馈为反复拉起系统悬浮窗授权页，无文字提示"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Warning",
      "text_zh": "警告",
      "source_location": "硬编码类 com.brazil.android.free.MainActivity#SetAccessEnable（AlertDialog.setTitle）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Permission is needed",
      "text_zh": "需要权限",
      "source_location": "硬编码类 com.brazil.android.free.MainActivity#SetAccessEnable（AlertDialog.setMessage）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Please check the permission for App",
      "text_zh": "请为应用检查该权限",
      "source_location": "res/values/strings.xml key=description（config_service.xml android:description）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Beginning Android",
      "text_zh": "开始使用 Android",
      "source_location": "res/layout/activity_main.xml（TextView android:text）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "FakeLock | Help",
      "text_zh": "FakeLock｜帮助",
      "source_location": "assets/help.html <title>",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "DEFENSOR ID is running in background",
      "text_zh": "DEFENSOR ID 正在后台运行",
      "source_location": "硬编码类 com.brazil.android.free.CommandService#startMyOwnForeground（NotificationCompat setContentTitle）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s is having trouble with Google Play services. Please try again.",
      "text_zh": "%1$s 无法访问 Google Play 服务，请重试。",
      "source_location": "res/values/strings.xml key=common_google_play_services_unknown_issue（GMS 标准资源，非自研文案）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无障碍弹窗本身为 setCancelable(false) 且无取消按钮；requestCode=11 无处理、onResume() 无逻辑，故从无障碍设置返回不会立即重弹（需再次冷启动）。但前置的悬浮窗环节 requestCode=12 未授权时 onActivityResult 直接递归调用 Check_over_permission()，形成无限次拉起 MANAGE_OVERLAY_PERMISSION 的拒权循环。",
    "overlay_or_fake_settings": "无设置页遮罩、无高仿无障碍开关页；但获权后由远控 lock 指令启动 TopService，以 TYPE_APPLICATION_OVERLAY 全屏 WebView（help.html + sample.gif，onTouch 恒 true）叠放整屏遮罩，吞掉全部触摸阻止用户操作。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无自点确认/自授权；performGlobalAction 仅作为远控 back/home/recent 指令使用，未见监听设置页并阻止撤权的逻辑",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 MainActivity 冷启动后监测到 intent 目标为 android.settings.action.MANAGE_OVERLAY_PERMISSION 或 android.settings.ACCESSIBILITY_SETTINGS 的瞬间拉起 UTG；并同步在 MainActivity.onCreate 返回后（首个 AlertDialog 显示）立即抓取当前窗口层级。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "包名 com.secure.protect.world 的 AlertDialog 窗口，标题 \"Warning\"、正文 \"Permission is needed\"、仅一个 \"OK\" 按钮",
        "why_most_useful": "这是该应用唯一的无障碍申请解释文案载体，且不可取消、无拒绝按钮，可直接证明诱导与无退出路径",
        "observable_utg_signals": ["Dialog 节点 cancelable=false / 无 negative/neutral button", "标题与正文文案原文", "弹窗出现时机紧接冷启动（0 步交互）"]
      },
      {
        "page_role": "系统悬浮窗授权页（跳转前置页）",
        "page_identifier": "com.android.settings 的 MANAGE_OVERLAY_PERMISSION 页面，由 requestCode 12 拉起",
        "why_most_useful": "证明应用在无障碍之前先索要悬浮窗（后续全屏遮罩所必需），且拒绝后会被递归重跳，是判定拒权循环的关键",
        "observable_utg_signals": ["同一 intent 在短时间内多次重复出现", "拒绝后 1~2 秒内再次进入该页", "页面出现时应用自身无任何说明 UI"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中 label=\"DEFENSOR ID\"、summary=\"Please check the permission for App\" 的服务条目",
        "why_most_useful": "核对系统侧展示名与描述是否与实际能力（全事件监听 + 读窗口内容 + 手势注入）严重不符，是身份误导的直接证据",
        "observable_utg_signals": ["服务条目文本 DEFENSOR ID", "说明文本 Please check the permission for App", "条目与桌面应用名完全一致（无二次辨识信息）"]
      },
      {
        "page_role": "获权后远控锁屏遮罩页",
        "page_identifier": "非 Activity 的全屏 TYPE_APPLICATION_OVERLAY WebView，内容为单张 GIF，页面标题 FakeLock | Help",
        "why_most_useful": "证明无障碍权限被用于远程控制与锁屏压制，而非宣称的安全防护；同时说明遮罩拦截触摸使受害者无法自救",
        "observable_utg_signals": ["窗口类型为 overlay 且覆盖全屏（非应用自身 Activity）", "WebView 内容仅一张图片、无文字节点", "所有触摸事件被消费、界面无响应", "前台通知 DEFENSOR ID is running in background 同时存在"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "引导链本体无盲区（文案为硬编码字符串，非远端 HTML/AES）。存在两点需注意：其一，TopService 遮罩页仅呈现 assets/sample.gif 图片，纯 UTG 文本抓取为空，需 OCR 或截图比对才能识别其内容；其二，远控指令集来自 Firebase 远端节点（remotebrazil.firebaseio.com），指令内容与下发时机无法静态枚举，需运行期抓包/DNS 观察才能确认实际触发的行为（如 lock、uninstall）。另，应用自述名称 DEFENSOR ID 属人设伪装，非静态加壳，不影响运行期 UTG 捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS"
  ],
  "code_anchors": [
    "com.brazil.android.free.MainActivity.onCreate",
    "com.brazil.android.free.MainActivity.SetAccessEnable",
    "com.brazil.android.free.MainActivity$1.onClick",
    "com.brazil.android.free.MainActivity.onActivityResult",
    "res/xml/config_service.xml",
    "assets/help.html"
  ]
}
```

</details>
