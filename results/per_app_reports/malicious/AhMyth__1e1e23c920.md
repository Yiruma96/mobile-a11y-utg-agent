# MB_026__1e1e23c920｜AhMyth — Flashlight

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：154.4s

## 1. 一句话核心结论

- **核心申请方式**：伪装成手电筒的工具应用在冷启动连续权限弹窗中夹带一条英文原生 AlertDialog，仅以“请允许无障碍权限以继续”为由诱导用户点 Yes 直接跳转系统无障碍列表开启一个只监听 WhatsApp/Facebook/Twitter 窗口内容的后台服务。
- **静态可见性说明**：无障碍引导全链路（弹窗文案、按钮回调、跳转 Intent、服务配置、系统列表显示名）均为明文静态可见，无加壳、无 AES 载荷、无远端 HTML；唯一静态缺口是 R8 将 showDialogForAccessiblityPermission 的调用点折叠为 synthetic lambda，MCP 交叉引用未给出 handleAllPermissions 到该弹窗的显式调用边。未遍历 assets/ 目录，但字符串与代码结构显示不存在 WebView 引导。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1e1e23c920eeaca8e9ffc1f946fcb978fa2419815b7b5dcf9a1cca9b934f8c4b` |
| 包名 / 年份 | `com.android.vendng` / 2024 |
| 家族 / 品类 | **AhMyth**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Flashlight |
| 引导页宣称品牌/身份 | Flashlight（手电筒/来电闪光工具） |
| 系统无障碍列表服务名 | Flashlight（服务 android:description 直接复用 @string/app_name，未提供任何功能说明） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无空白/换行挤出、无同形字、无多 activity-alias、无伪造 isAccessibilityTool。仅利用 android:description 复用应用名，使系统无障碍列表显示为无害的“Flashlight”，从而隐藏其 com.whatsapp\|com.facebook.katana\|com.twitter.android\|com.facebook.orca 的窗口内容读取用途。 |
| 无障碍服务类名 | `com.android.vendng.service.AppAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.whatsapp|com.facebook.katana|com.twitter.android|com.facebook.orca |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Flashlight / Flashlight |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.android.vendng.ui.activity.MainActivity（LAUNCHER，portrait，taskAffinity=app.one） | onCreate：setContentView 后调用 startForeground() 与 handleAllPermissions() | 原生Activity | **原文**：无（主界面为手电筒功能布局 activity_main）<br>**译注**：手电筒主界面 | 无，进入即自动触发后续权限链 | `com.android.vendng.ui.activity.MainActivity.onCreate` |
| 2 | 引导说明页 | handleAllPermissions 连续弹出的系统对话框链：运行时权限（READ_SMS/READ_CONTACTS/CAMERA/RECORD_AUDIO 等）、GPS 开启、电池优化白名单、悬浮窗、存储管理、MIUI 自启动提示 | onCreate → handleAllPermissions 顺序执行 PermissionHelper.requestPermissions、GPSHelper.enableLocation、PermissionHelper.requestBatteryOptimization、showDialogForOverlayPermission、showDialogForManageStoragePermission | 原生Dialog | **原文**：Please allow draw app on top permission to proceed<br>**译注**：请允许“显示在其他应用上层”权限以继续 | 点 Yes 前往悬浮窗授权；点 No 关闭本弹窗（后续弹窗继续弹出） | `com.android.vendng.ui.activity.MainActivity.showDialogForOverlayPermission / handleAllPermissions` |
| 3 | 引导说明页 | android.app.AlertDialog（MainActivity 内，非 Material） | showDialogForAccessiblityPermission()：先 isAccessibilitySettingsOn() 判定未开启才 show() | 原生Dialog | **原文**：Please allow accessibility permission to proceed（按钮：Yes / No）<br>**译注**：请允许无障碍权限以继续（按钮：是 / 否） | 点 Yes 跳转系统无障碍设置；点 No 关闭。弹窗不说明读取范围、不说明仅监听 WhatsApp/Facebook/Twitter，也无任何功能关联解释 | `com.android.vendng.ui.activity.MainActivity.showDialogForAccessiblityPermission` |
| 4 | 跳无障碍设置 | 系统设置：android.settings.ACCESSIBILITY_SETTINGS（列表项显示为 Flashlight） | Yes 按钮回调 lambda$3：若 isAccessibilitySettingsOn 仍为 false，则 new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(FLAG_ACTIVITY_NEW_TASK) + startActivity | 系统无障碍页 | **原文**：无（界面为系统无障碍服务列表，条目文本取自 android:description=@string/app_name，即 Flashlight）<br>**译注**：系统无障碍服务列表中的“Flashlight”开关项 | 用户需在列表中手动找到“Flashlight”并打开开关、在系统风险确认框中点允许 | `com.android.vendng.ui.activity.MainActivity#showDialogForAccessiblityPermission$lambda$3` |
| 5 | 获权后动作 | com.android.vendng.service.AppAccessibilityService（独立进程 :accessProcess） | onServiceConnected 注册后，onAccessibilityEvent 对 whatsapp/katana/twitter/orca 的 typeAllMask 事件执行 traverseAndLogViewIds / traverseNodeAndLogText / traverseNodesAndDetermineMessages / logTextForWhatsAppId | 不可静态还原（无 UI，后台静默读取窗口内容） | 无 | 无（用户无感知） | `com.android.vendng.service.AppAccessibilityService.onAccessibilityEvent` |
| 6 | 冷启动入口 | MainActivity 欢迎层（llWelcome 可见、container 隐藏）→ 系统设置首页 android.settings.SETTINGS | Intent extra from=boot 时，Handler.postDelayed(500ms) 后执行 onCreate$lambda$0：startActivity(new Intent("android.settings.SETTINGS")) | 系统无障碍页 | **原文**：无（直接跳转系统设置首页）<br>**译注**：直接进入系统设置首页，用户可自行进入“无障碍”分区 | 无显式文案要求；靠用户自行在系统设置中寻找无障碍入口 | `com.android.vendng.ui.activity.MainActivity#onCreate$lambda$0` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内的原生 AlertDialog（android.app.AlertDialog$Builder）：文案硬编码 "Please allow accessibility permission to proceed"，按钮 "Yes"/"No"，仅在 isAccessibilitySettingsOn() 返回 false 时弹出
- 系统无障碍服务列表项：文本取自 res/xml/accessibility_service_config.xml 的 android:description=@string/app_name，即 strings.xml 第 33 行 "Flashlight"
- MainActivity 连续弹窗链中的相邻弹窗（悬浮窗 "Please allow draw app on top permission to proceed"、通知 "Please allow notification permission to proceed"、AutoStart 提示），用于在无障碍弹窗前后制造“配置工具”氛围
- res/layout/permission_dialog.xml 中另有 TextView 硬编码 "Please allow notification permission to proceed"，供通知权限弹窗使用
- HomeFragment.showPermissionDialog 使用 strings.xml 的 allow_perm + permission_desc（"Please allow read state and make phone call permission for incoming call notification and SOS feature."），仅在功能触发时弹出，与无障碍无直接关联
- 未发现 assets 下的 HTML 教学页、WebView 引导、悬浮窗遮罩引导或伪造的系统无障碍开关页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please allow accessibility permission to proceed | 请允许无障碍权限以继续 | `com.android.vendng.ui.activity.MainActivity.showDialogForAccessiblityPermission 硬编码字符串` | 受限设置分步教学 |
| en | Yes | 是 | `com.android.vendng.ui.activity.MainActivity.showDialogForAccessiblityPermission setPositiveButton` | 未知 |
| en | No | 否 | `com.android.vendng.ui.activity.MainActivity.showDialogForAccessiblityPermission setNegativeButton` | 未知 |
| en | Flashlight | 手电筒 | `res/values/strings.xml 第 33 行 key=app_name，被 res/xml/accessibility_service_config.xml 的 android:description 引用，成为系统无障碍列表中的服务名` | 清理工具伪装 |
| en | Please allow draw app on top permission to proceed | 请允许“显示在其他应用上层”权限以继续 | `com.android.vendng.ui.activity.MainActivity.showDialogForOverlayPermission 硬编码字符串` | 未知 |
| en | Please allow notification permission to proceed | 请允许通知权限以继续 | `com.android.vendng.ui.activity.MainActivity.showDialogForNotification 硬编码字符串；res/layout/permission_dialog.xml 第 4 行 TextView 同文案` | 未知 |
| en | Please allow read state and make phone call permission for incoming call notification and SOS feature. | 请允许读取状态和拨打电话权限，用于来电通知和 SOS 功能。 | `res/values/strings.xml 第 247 行 key=permission_desc` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：弹窗提供 No 按钮（setNegativeButton "No" → MainActivity$$ExternalSyntheticLambda1），静态未发现 onResume 死循环重跳、Timer 轮询拉起或返回键拦截；若用户点 Yes 但返回时仍未授权，仅在 Yes 回调内再次判定 isAccessibilitySettingsOn 为 false 才跳设置页，不具备强制回跳循环。
- **遮罩叠层 / 高仿系统设置页**：无。未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 与悬浮窗弹窗仅用于开启通用悬浮窗权限（后续被 SocketManager.x0000rm/launchHome 用作前置条件），未用于叠层指引无障碍。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、右上角菜单受限设置教学或 Session 安装器（SessionInstaller）绕过路径。
- **获权后即时行为与防撤权机制**：无。无障碍服务 onAccessibilityEvent 未发现监听系统设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；未发现自点确认或自授权代码。
- **良性降级 / 替代方案**：无。手电筒核心功能（turnFlash/屏幕照明）与无障碍服务无任何依赖关系，未提供替代路径或降级说明。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测冷启动后 Activity 栈变化：出现 MainActivity 且系统弹窗层出现含“accessibility”文本的 Dialog 时立即截图；以及监测 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 触发的瞬间（Activity 切换到 com.android.settings 无障碍列表）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。本样本引导全程为明文原生控件，无需 OCR。需注意两点：一是无障碍弹窗的静态调用点被 R8 折叠为 synthetic lambda，纯静态 xref 可能漏掉调用边，UTG 运行期观测可补齐；二是该 APK 同时携带 SocketManager 远控指令通道（x0000sm/x0000fm/x0000ca/x0000rm 等），实际窃取行为在获权后由远端下发，UTG 仅能捕获授权动作本身，后续数据外发需流量侧配合。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（无障碍诱导弹窗）** | MainActivity 之上的原生 AlertDialog，正文含“Please allow accessibility permission to proceed”，按钮 Yes/No | 这是唯一直接索要无障碍权限的 UI 节点，能确定诱导动机、文案强度与是否给出用途说明 | 弹窗标题/正文文本节点；Yes 与 No 两个按钮的文本与可点击性；弹窗背后的页面是否仍为手电筒功能界面（证明与功能无关） |
| **系统无障碍服务列表项** | com.android.settings 无障碍页面中服务条目文本为 Flashlight | 验证 android:description 复用应用名造成的身份遮蔽效果，确认用户在系统层看到的名称与实际权限范围不符 | 服务条目显示名 Flashlight；条目是否展示任何用途说明子文本；开关当前状态 |
| **连续权限弹窗链（权限包夹上下文）** | 同一 MainActivity 生命周期内连续出现的悬浮窗、通知、电池优化、存储管理弹窗 | 证明无障碍弹窗被夹在多个“工具配置”弹窗之间，用户易在连续点确定中误授权 | 弹窗出现顺序与时间间隔；各弹窗文案是否为同一句式 Please allow ... to proceed；是否出现系统风险警告页 |
| **开机/自启拉起后跳系统设置首页** | MainActivity 欢迎层（llWelcome 可见）随后跳转 com.android.settings 首页 | 验证 from=boot 路径下 500ms 后直跳系统设置的引导链路是否真实可达 | 欢迎层是否短暂可见；500ms 后顶层 Activity 是否变为系统设置；是否伴随 BootReceiver 触发的进程拉起 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.android.vendng.ui.activity.MainActivity#showDialogForAccessiblityPermission`
- `com.android.vendng.ui.activity.MainActivity#showDialogForAccessiblityPermission$lambda$3`
- `com.android.vendng.ui.activity.MainActivity#isAccessibilitySettingsOn`
- `com.android.vendng.ui.activity.MainActivity#handleAllPermissions`
- `com.android.vendng.ui.activity.MainActivity#onCreate$lambda$0`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

- **入口与身份**：`com.android.vendng` 的桌面名称为 `Flashlight`（[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L33>)），`MainActivity` 是唯一的 LAUNCHER 入口。无障碍服务在 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 中的 `android:description` 直接复用 `@string/app_name`，因此系统无障碍列表里显示的就是“Flashlight”，用户看不到任何“读取聊天内容”的说明。
- **监控范围与宣称功能不符**：同一配置把 `packageNames` 限定为 `com.whatsapp|com.facebook.katana|com.twitter.android|com.facebook.orca`，并开启 `canRetrieveWindowContent=true`、`typeAllMask`、`flagRetrieveInteractiveWindows`。手电筒不需要读取即时通讯窗口内容，这属于典型的 AhMyth 消息窃取面。
- **引导方式极其简陋（非精细社工）**：没有 HTML 教学页、没有悬浮遮罩、没有伪造系统开关页，也没有教用户开启“受限设置”。只有一条原生 `AlertDialog`：`Please allow accessibility permission to proceed`，带 `Yes`/`No` 两个按钮。用户点击 `Yes` 后，会直接通过 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 跳到系统无障碍列表。
- **权限包夹**：`MainActivity.onCreate` → `handleAllPermissions` 一次性连续触发运行时权限、GPS、电池优化白名单、悬浮窗弹窗、存储管理弹窗；在 MIUI 等品牌下还会额外弹出 `showAutoStartPermission`，并 `launchHome`（`launchHome` 以 `Settings.canDrawOverlays` 为前置条件）。无障碍弹窗混在这一串弹窗中，用户更容易在“连续点确定”时进入设置页。
- **补充事实**：当 `from=boot` 时（由 `BootActivity` 或开机广播链路拉起），`onCreate` 会先显示欢迎层，并在 500ms 后调用 `startActivity("android.settings.SETTINGS")`，直接把用户带到系统设置首页，为后续进入无障碍设置铺路。
- **证据边界**：`showDialogForAccessiblityPermission()` 与 `showDialogForNotification()` 的直接调用点被 R8 折叠进 synthetic lambda，静态交叉引用没有给出 `handleAllPermissions` 到该弹窗的显式调用边；弹窗本身、文案、按钮回调和跳转 Intent 均已逐字确认。未遍历 `assets/`，但从字符串与结构看，不存在远端或本地 HTML 引导。

**UTG 观测建议**：在冷启动后 0–3 秒内密集截取连续弹窗链，重点抓取无障碍弹窗出现的瞬间，以及跳转 `ACCESSIBILITY_SETTINGS` 之后系统列表中的“Flashlight”条目文本。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（弹窗文案、按钮回调、跳转 Intent、服务配置、系统列表显示名）均为明文静态可见，无加壳、无 AES 载荷、无远端 HTML；唯一静态缺口是 R8 将 showDialogForAccessiblityPermission 的调用点折叠为 synthetic lambda，MCP 交叉引用未给出 handleAllPermissions 到该弹窗的显式调用边。未遍历 assets/ 目录，但字符串与代码结构显示不存在 WebView 引导。",
  "summary_one_liner": "伪装成手电筒的工具应用在冷启动连续权限弹窗中夹带一条英文原生 AlertDialog，仅以“请允许无障碍权限以继续”为由诱导用户点 Yes 直接跳转系统无障碍列表开启一个只监听 WhatsApp/Facebook/Twitter 窗口内容的后台服务。",
  "disguise_identity": {
    "app_display_name": "Flashlight",
    "claimed_brand_or_persona": "Flashlight（手电筒/来电闪光工具）",
    "a11y_service_label": "Flashlight（服务 android:description 直接复用 @string/app_name，未提供任何功能说明）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无空白/换行挤出、无同形字、无多 activity-alias、无伪造 isAccessibilityTool。仅利用 android:description 复用应用名，使系统无障碍列表显示为无害的“Flashlight”，从而隐藏其 com.whatsapp|com.facebook.katana|com.twitter.android|com.facebook.orca 的窗口内容读取用途。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.android.vendng.ui.activity.MainActivity（LAUNCHER，portrait，taskAffinity=app.one）",
      "trigger_event": "onCreate：setContentView 后调用 startForeground() 与 handleAllPermissions()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（主界面为手电筒功能布局 activity_main）",
      "shown_text_zh": "手电筒主界面",
      "user_action_requested": "无，进入即自动触发后续权限链",
      "code_anchor": "com.android.vendng.ui.activity.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "handleAllPermissions 连续弹出的系统对话框链：运行时权限（READ_SMS/READ_CONTACTS/CAMERA/RECORD_AUDIO 等）、GPS 开启、电池优化白名单、悬浮窗、存储管理、MIUI 自启动提示",
      "trigger_event": "onCreate → handleAllPermissions 顺序执行 PermissionHelper.requestPermissions、GPSHelper.enableLocation、PermissionHelper.requestBatteryOptimization、showDialogForOverlayPermission、showDialogForManageStoragePermission",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please allow draw app on top permission to proceed",
      "shown_text_zh": "请允许“显示在其他应用上层”权限以继续",
      "user_action_requested": "点 Yes 前往悬浮窗授权；点 No 关闭本弹窗（后续弹窗继续弹出）",
      "code_anchor": "com.android.vendng.ui.activity.MainActivity.showDialogForOverlayPermission / handleAllPermissions"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "android.app.AlertDialog（MainActivity 内，非 Material）",
      "trigger_event": "showDialogForAccessiblityPermission()：先 isAccessibilitySettingsOn() 判定未开启才 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please allow accessibility permission to proceed（按钮：Yes / No）",
      "shown_text_zh": "请允许无障碍权限以继续（按钮：是 / 否）",
      "user_action_requested": "点 Yes 跳转系统无障碍设置；点 No 关闭。弹窗不说明读取范围、不说明仅监听 WhatsApp/Facebook/Twitter，也无任何功能关联解释",
      "code_anchor": "com.android.vendng.ui.activity.MainActivity.showDialogForAccessiblityPermission"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置：android.settings.ACCESSIBILITY_SETTINGS（列表项显示为 Flashlight）",
      "trigger_event": "Yes 按钮回调 lambda$3：若 isAccessibilitySettingsOn 仍为 false，则 new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(FLAG_ACTIVITY_NEW_TASK) + startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（界面为系统无障碍服务列表，条目文本取自 android:description=@string/app_name，即 Flashlight）",
      "shown_text_zh": "系统无障碍服务列表中的“Flashlight”开关项",
      "user_action_requested": "用户需在列表中手动找到“Flashlight”并打开开关、在系统风险确认框中点允许",
      "code_anchor": "com.android.vendng.ui.activity.MainActivity#showDialogForAccessiblityPermission$lambda$3"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.android.vendng.service.AppAccessibilityService（独立进程 :accessProcess）",
      "trigger_event": "onServiceConnected 注册后，onAccessibilityEvent 对 whatsapp/katana/twitter/orca 的 typeAllMask 事件执行 traverseAndLogViewIds / traverseNodeAndLogText / traverseNodesAndDetermineMessages / logTextForWhatsAppId",
      "ui_carrier": "不可静态还原（无 UI，后台静默读取窗口内容）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，静默读取目标应用聊天窗口文本",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "com.android.vendng.service.AppAccessibilityService.onAccessibilityEvent"
    },
    {
      "step": 6,
      "stage": "冷启动入口",
      "screen_or_component": "MainActivity 欢迎层（llWelcome 可见、container 隐藏）→ 系统设置首页 android.settings.SETTINGS",
      "trigger_event": "Intent extra from=boot 时，Handler.postDelayed(500ms) 后执行 onCreate$lambda$0：startActivity(new Intent(\"android.settings.SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（直接跳转系统设置首页）",
      "shown_text_zh": "直接进入系统设置首页，用户可自行进入“无障碍”分区",
      "user_action_requested": "无显式文案要求；靠用户自行在系统设置中寻找无障碍入口",
      "code_anchor": "com.android.vendng.ui.activity.MainActivity#onCreate$lambda$0"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内的原生 AlertDialog（android.app.AlertDialog$Builder）：文案硬编码 \"Please allow accessibility permission to proceed\"，按钮 \"Yes\"/\"No\"，仅在 isAccessibilitySettingsOn() 返回 false 时弹出",
    "系统无障碍服务列表项：文本取自 res/xml/accessibility_service_config.xml 的 android:description=@string/app_name，即 strings.xml 第 33 行 \"Flashlight\"",
    "MainActivity 连续弹窗链中的相邻弹窗（悬浮窗 \"Please allow draw app on top permission to proceed\"、通知 \"Please allow notification permission to proceed\"、AutoStart 提示），用于在无障碍弹窗前后制造“配置工具”氛围",
    "res/layout/permission_dialog.xml 中另有 TextView 硬编码 \"Please allow notification permission to proceed\"，供通知权限弹窗使用",
    "HomeFragment.showPermissionDialog 使用 strings.xml 的 allow_perm + permission_desc（\"Please allow read state and make phone call permission for incoming call notification and SOS feature.\"），仅在功能触发时弹出，与无障碍无直接关联",
    "未发现 assets 下的 HTML 教学页、WebView 引导、悬浮窗遮罩引导或伪造的系统无障碍开关页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please allow accessibility permission to proceed",
      "text_zh": "请允许无障碍权限以继续",
      "source_location": "com.android.vendng.ui.activity.MainActivity.showDialogForAccessiblityPermission 硬编码字符串",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Yes",
      "text_zh": "是",
      "source_location": "com.android.vendng.ui.activity.MainActivity.showDialogForAccessiblityPermission setPositiveButton",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "No",
      "text_zh": "否",
      "source_location": "com.android.vendng.ui.activity.MainActivity.showDialogForAccessiblityPermission setNegativeButton",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Flashlight",
      "text_zh": "手电筒",
      "source_location": "res/values/strings.xml 第 33 行 key=app_name，被 res/xml/accessibility_service_config.xml 的 android:description 引用，成为系统无障碍列表中的服务名",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Please allow draw app on top permission to proceed",
      "text_zh": "请允许“显示在其他应用上层”权限以继续",
      "source_location": "com.android.vendng.ui.activity.MainActivity.showDialogForOverlayPermission 硬编码字符串",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Please allow notification permission to proceed",
      "text_zh": "请允许通知权限以继续",
      "source_location": "com.android.vendng.ui.activity.MainActivity.showDialogForNotification 硬编码字符串；res/layout/permission_dialog.xml 第 4 行 TextView 同文案",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Please allow read state and make phone call permission for incoming call notification and SOS feature.",
      "text_zh": "请允许读取状态和拨打电话权限，用于来电通知和 SOS 功能。",
      "source_location": "res/values/strings.xml 第 247 行 key=permission_desc",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "弹窗提供 No 按钮（setNegativeButton \"No\" → MainActivity$$ExternalSyntheticLambda1），静态未发现 onResume 死循环重跳、Timer 轮询拉起或返回键拦截；若用户点 Yes 但返回时仍未授权，仅在 Yes 回调内再次判定 isAccessibilitySettingsOn 为 false 才跳设置页，不具备强制回跳循环。",
    "overlay_or_fake_settings": "无。未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 与悬浮窗弹窗仅用于开启通用悬浮窗权限（后续被 SocketManager.x0000rm/launchHome 用作前置条件），未用于叠层指引无障碍。",
    "restricted_settings_13plus_coaching": "无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、右上角菜单受限设置教学或 Session 安装器（SessionInstaller）绕过路径。",
    "post_grant_anti_removal": "无。无障碍服务 onAccessibilityEvent 未发现监听系统设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；未发现自点确认或自授权代码。",
    "benign_graceful_degradation": "无。手电筒核心功能（turnFlash/屏幕照明）与无障碍服务无任何依赖关系，未提供替代路径或降级说明。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测冷启动后 Activity 栈变化：出现 MainActivity 且系统弹窗层出现含“accessibility”文本的 Dialog 时立即截图；以及监测 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 触发的瞬间（Activity 切换到 com.android.settings 无障碍列表）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（无障碍诱导弹窗）",
        "page_identifier": "MainActivity 之上的原生 AlertDialog，正文含“Please allow accessibility permission to proceed”，按钮 Yes/No",
        "why_most_useful": "这是唯一直接索要无障碍权限的 UI 节点，能确定诱导动机、文案强度与是否给出用途说明",
        "observable_utg_signals": ["弹窗标题/正文文本节点", "Yes 与 No 两个按钮的文本与可点击性", "弹窗背后的页面是否仍为手电筒功能界面（证明与功能无关）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页面中服务条目文本为 Flashlight",
        "why_most_useful": "验证 android:description 复用应用名造成的身份遮蔽效果，确认用户在系统层看到的名称与实际权限范围不符",
        "observable_utg_signals": ["服务条目显示名 Flashlight", "条目是否展示任何用途说明子文本", "开关当前状态"]
      },
      {
        "page_role": "连续权限弹窗链（权限包夹上下文）",
        "page_identifier": "同一 MainActivity 生命周期内连续出现的悬浮窗、通知、电池优化、存储管理弹窗",
        "why_most_useful": "证明无障碍弹窗被夹在多个“工具配置”弹窗之间，用户易在连续点确定中误授权",
        "observable_utg_signals": ["弹窗出现顺序与时间间隔", "各弹窗文案是否为同一句式 Please allow ... to proceed", "是否出现系统风险警告页"]
      },
      {
        "page_role": "开机/自启拉起后跳系统设置首页",
        "page_identifier": "MainActivity 欢迎层（llWelcome 可见）随后跳转 com.android.settings 首页",
        "why_most_useful": "验证 from=boot 路径下 500ms 后直跳系统设置的引导链路是否真实可达",
        "observable_utg_signals": ["欢迎层是否短暂可见", "500ms 后顶层 Activity 是否变为系统设置", "是否伴随 BootReceiver 触发的进程拉起"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。本样本引导全程为明文原生控件，无需 OCR。需注意两点：一是无障碍弹窗的静态调用点被 R8 折叠为 synthetic lambda，纯静态 xref 可能漏掉调用边，UTG 运行期观测可补齐；二是该 APK 同时携带 SocketManager 远控指令通道（x0000sm/x0000fm/x0000ca/x0000rm 等），实际窃取行为在获权后由远端下发，UTG 仅能捕获授权动作本身，后续数据外发需流量侧配合。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION"
  ],
  "code_anchors": [
    "com.android.vendng.ui.activity.MainActivity#showDialogForAccessiblityPermission",
    "com.android.vendng.ui.activity.MainActivity#showDialogForAccessiblityPermission$lambda$3",
    "com.android.vendng.ui.activity.MainActivity#isAccessibilitySettingsOn",
    "com.android.vendng.ui.activity.MainActivity#handleAllPermissions",
    "com.android.vendng.ui.activity.MainActivity#onCreate$lambda$0",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

补充说明：`behavior_pattern_tags` 中的 `BENIGN_EXPLICIT_CANCEL_DEGRADATION` 仅用于描述“弹窗确实提供 No 取消按钮”这一中性事实，不代表整体良性；本样本整体判定为恶意（已登记 R-001，`malware_trojan` / high）。

</details>
