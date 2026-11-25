# MR_037__96de80ed5f｜boogr — System Update

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：135.0s

## 1. 一句话核心结论

- **核心申请方式**：以“System Update”名义分发的间谍应用对无障碍权限采取零告知零引导的静默植入：冷启动只强推电池优化白名单并立即隐藏桌面图标，无障碍服务在系统列表中仅以通用名“Android Service”示人，获权后专职抓取 WhatsApp/Messenger 聊天界面内容回传。
- **静态可见性说明**：APK 未加壳，DEX 完整可反编译，无障碍服务配置、标签与采集逻辑均静态可见。仅两点不在静态范围内：其一，远端 Firebase/FCM 指令（ConstantAppString 中 MAIN_URL_WAL/ABD/OTH 等后端地址与 GoogleServices.checkForCommands 的命令处理）可能在下发后改变行为；其二，代码中根本不存在无障碍引导 UI，因此不存在可静态还原的引导流程。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `96de80ed5ff6ac9faa1b3a2b0d67cee8259fda9f6ad79841c341b1c3087e4c92` |
| 包名 / 年份 | `com.update.system.important` / 2021 |
| 家族 / 品类 | **boogr**（同池样本数：2） |
| 原始来源标识 | https://blog.zimperium.com/new-advanced-android-malware-posing-as-system-update/ |
| 桌面显示名 | System Update |
| 引导页宣称品牌/身份 | 系统更新（冒充 Android 系统 OTA 更新服务） |
| 系统无障碍列表服务名 | Android Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签使用通用且中性的“Android Service”，与桌面名“System Update”及真实用途（读取 WhatsApp/Messenger 会话）均不一致；accessibility_service_config.xml 未声明 android:description，也未声明 android:settingsActivity，系统无障碍列表项无任何用途说明；MainActivity 与 LeanbackLauncherActivity 均采用 Theme.Translucent.NoTitleBar.Fullscreen 且 autoRemoveFromRecents/excludeFromRecents，启动后即 setComponentEnabledSetting(..., 2, 1) 隐藏图标（Utility.hideIcon），用户无法回溯检查或撤销权限；双入口（LAUNCHER + LEANBACK_LAUNCHER）互为备份；服务端地址以 char 数组逐字符拼接构造（ConstantAppString.MAIN_URL_*），规避字符串检索。 |
| 无障碍服务类名 | `com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.facebook.orca,com.whatsapp |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.update.system.important.MainActivity（android:theme=@android:style/Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents=true） | 用户点击桌面图标“System Update”触发 onCreate | 原生Activity | 无 | 无提示，用户仅看到短暂空白/闪烁 | `com.update.system.important.MainActivity#onCreate` |
| 2 | 引导说明页（缺失） | 不存在——无 Dialog、无引导 Activity、无本地或远端 WebView、无悬浮遮罩 | 无 | 不可静态还原 | 无 | 无 | `全包检索 ACTION_ACCESSIBILITY_SETTINGS / android.settings.* / enabled_accessibility_services 均无应用自身命中` |
| 3 | 跳受限设置 | 系统页 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS（电池优化忽略白名单），由 MainActivity 以 startActivityForResult(intent, 23) 拉起 | checkBattery()：Build.VERSION.SDK_INT>=23 且 PowerManager.isIgnoringBatteryOptimizations(packageName)==false | 系统无障碍页（此处为系统电池优化设置页，非无障碍页） | **原文**：无应用自绘文字（系统页文本由 OS 提供）<br>**译注**：系统弹出的“是否允许应用忽略电池优化”对话框 | 要求用户点击“允许/Allow”；无应用侧取消或跳过按钮 | `com.update.system.important.MainActivity#checkBattery` |
| 4 | 拒权反馈循环 | MainActivity 内 Timer（scheduleAtFixedRate(1000L, 500L)）+ MainActivity$1.run → checkBattery | 定时器每 500ms 回调；若 this.a（已加入白名单标记）仍为 false，则 runApp 不取消定时器且再次 startActivityForResult | 系统无障碍页 | 无 | 强制用户允许忽略电池优化；无跳过选项 | `com.update.system.important.MainActivity$1#run / com.update.system.important.MainActivity#checkBattery` |
| 5 | 获权后动作 | Utility.startService（启动 GoogleServices 前台服务）+ Utility.hideIcon(MainActivity.class) + finish() | onActivityResult(23, RESULT_OK) → runApp()；或 SDK<23/异常时 checkBattery 直接置 this.a=true 后 runApp() | 通知栏 | **原文**：System Update / Searching for update（ConstantAppString.SEARCHING_FOR_UPDATE）<br>**译注**：通知栏前台通知，标题为应用名“System Update”，正文为“正在搜索更新” | 无需用户操作；同时桌面图标被禁用，用户失去入口 | `com.update.system.important.MainActivity#runApp / com.update.system.important.utility.Utility#hideIcon / com.update.system.important.GoogleServices#displayForegroundService` |
| 6 | 获权后动作 | 后台 Main2Activity（由 GoogleServices.checkForCommands / mScreenStateReceiver / BatteryCharging 经 Utility.displayActivity 拉起，120 秒节流） | 亮/灭屏广播、充电广播、服务端命令轮询；Handler.postDelayed(Main2Activity$1, REFRESH_TIME) | 原生Activity | 无 | 无 | `com.update.system.important.utility.Utility#displayActivity / com.update.system.important.Main2Activity#onCreate` |
| 7 | 获权后动作 | com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService（系统无障碍服务，标签“Android Service”） | 用户在系统设置中自行开启该服务后，onAccessibilityEvent 每次事件触发 AsyncTask.execute(MyAccessibilityService$1) | 系统无障碍页 | **原文**：Android Service<br>**译注**：系统无障碍服务列表项显示名仅为“Android Service”，无描述说明 | 需用户在系统设置中手动开启；应用全程无任何引导（无弹窗、无跳转、无教学） | `com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService#onAccessibilityEvent / com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService$1#run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml 的 accessibility_service_label = "Android Service"，经 Manifest 中 android:label 呈现在系统“无障碍 → 已安装服务”列表项上
- res/xml/accessibility_service_config.xml 未声明 android:description，系统无障碍服务详情页无任何用途说明文字（空白）
- res/values/strings.xml 的 app_name = "System Update"，呈现在桌面图标名与前台服务通知标题（GoogleServices#displayForegroundService 的 setContentTitle）
- 通知栏正文 "Searching for update"（ConstantAppString.SEARCHING_FOR_UPDATE），构成“正在检查系统更新”的假更新语境
- res/values/strings.xml 中 common_google_play_services_* 系列（"%1$s won't work unless you enable Google Play services." 等）仅为 Google Play services 库自带资源，未被本应用引导流程使用
- 应用不存在任何自绘引导弹窗、引导 Activity、本地/远端 WebView 页面或悬浮遮罩——无文字呈现位置

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | System Update | 系统更新 | `res/values/strings.xml  key=app_name` | 假更新 |
| en | Android Service | 安卓服务 | `res/values/strings.xml  key=accessibility_service_label（Manifest 中无障碍服务 android:label）` | 未知 |
| en | Searching for update | 正在搜索更新 | `com.update.system.important.utility.ConstantAppString#SEARCHING_FOR_UPDATE，用于 GoogleServices#displayForegroundService 前台通知正文` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：对无障碍无任何重跳机制（无 ACTION_ACCESSIBILITY_SETTINGS 构造、无 onResume 检测）。存在的循环仅针对电池优化白名单：MainActivity 的 Timer 以 1000ms 初始延迟、500ms 周期调用 checkBattery，未获白名单即重复 startActivityForResult 拉起系统页，直至 onActivityResult(23, RESULT_OK) 才 cancel。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 绘制引导遮罩，无高仿系统无障碍开关页，无全屏悬浮窗引导；仅存在 Theme.Translucent.NoTitleBar.Fullscreen 的空白全屏 Activity。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权。但采用另一类抗撤除手段：runApp 与 GoogleServices.onCreate 调用 Utility.hideIcon（setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP)）禁用 MainActivity 与 LeanbackLauncherActivity，使用户失去桌面入口、难以回到应用检查或关闭已授予的权限。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：纯 UTG 检测不宜等待“跳转无障碍设置”瞬间（该跳转在代码中不存在）。应锚定两个时机：①冷启动后 MainActivity 立即拉起 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 系统页的瞬间（首帧 1 秒内）；②用户在系统设置中开启“Android Service”无障碍后，任意 WhatsApp/Messenger 界面事件触发 onAccessibilityEvent 的瞬间（可用 Monkey/UI 操作进入 WhatsApp 聊天页触发）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在结构性盲区：本应用对无障碍权限完全无引导，因此“UTG 检测无障碍诱导页”这一信号在本样本上必然为空——若检测模型仅依赖“引导弹窗/教学页/悬浮遮罩”特征将漏判。此外无障碍服务标签为通用词“Android Service”且无 description，系统列表页本身不呈现任何可疑文案；行为触发依赖远端 Firebase/FCM 指令（GoogleServices.checkForCommands + MAIN_URL_WAL/ABD/OTH 后端），静态无法完全枚举下发的具体命令。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动即弹出的系统电池优化授权页（唯一的“引导”动作）** | 包名 com.android.settings，界面含“忽略电池优化/Ignore battery optimizations”，来源 Activity 为 com.update.system.important.MainActivity 且自身为全屏半透明空白 | 证明应用冷启动 0 步即强推系统受限授权、且自身无任何说明文字，是“零告知 + 立即索取系统特权”的关键证据；同时可观察 500ms 周期重复拉起行为 | 系统页与背后空白透明 Activity 的层级关系（应用未绘制任何说明文本）；返回后 500ms 内再次弹出同一系统页（拒权循环）；设置页返回后桌面图标随即消失（hideIcon 生效） |
| **系统无障碍服务列表项（唯一的无障碍身份呈现面）** | com.android.settings 无障碍列表中出现 label="Android Service"、包名 com.update.system.important 的服务项，无 description 副文本 | 直接固化身份错配证据：桌面名“System Update”与列表名“Android Service”不一致、无用途说明；可核对应用是否真的没有任何“去开启”引导（用户需完全自行找到此页） | 服务项 label 文本 "Android Service" 与 summary/description 为空；进入应用后无任何页面跳转到该设置页（无跳转动作可观测）；列表项所属包名 com.update.system.important 与显示名不符 |
| **获权后前台服务通知（假更新语境）** | 通知栏通知，标题 "System Update"、正文 "Searching for update"，channel 由 GoogleServices.createNotificationChannel 创建 | 证明应用以“系统更新检查”为伪装持续前台驻留，且该通知与无障碍采集同时存在，可关联无障碍被用于会话窃取的用途 | 通知标题/正文文本；通知出现时桌面已无应用图标（component disabled）；无障碍服务已 enabled 与该通知共存 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.update.system.important.MainActivity#checkBattery`
- `com.update.system.important.MainActivity#runApp`
- `com.update.system.important.utility.Utility#hideIcon`
- `com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService#onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml（accessibility_service_label / app_name）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**该应用不存在任何无障碍权限引导流程**：以下结论均为在静态全量检索和代码核验中确认的否定性事实。

- **无跳转点**：全包检索 `ACTION_ACCESSIBILITY_SETTINGS`、`android.settings.*`、`Settings$Secure`、`enabled_accessibility_services`、`isAccessibilityTool`，应用自身代码**均无命中**。仅存两处 `android.settings` 分别是 Google Play services 库内部的 `APPLICATION_DETAILS_SETTINGS`，以及 [MainActivity.checkBattery()](<resource-unit:#1.dex1 code:com.update.system.important.MainActivity#checkBattery>) 的 `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`（电池优化白名单，不是无障碍）。
- **无载体**：`assets/` 目录不存在，无 HTML/WebView；`res/layout*` 下无自定义引导页；无悬浮窗引导代码；无任何说明弹窗。
- **唯一面向用户的“无障碍文本”**是系统列表里的服务标签：`accessibility_service_label` = `Android Service`，且 [accessibility_service_config.xml (lines 2-3)](<resource-unit:#1 file:res/xml/accessibility_service_config.xml#L2-L3>) **未声明 `android:description`**，用户看不到任何用途说明。
- **冷启动实际做的引导只针对电池优化**：`MainActivity` 使用全屏半透明主题，`onCreate` 后由 500ms 周期定时器反复调用 `checkBattery`；未加入白名单即 `startActivityForResult` 跳系统电池优化页，形成拒权循环重跳。
- **获权后立即隐藏入口**：`runApp` 与 `GoogleServices.onCreate` 都调用 `Utility.hideIcon`（`setComponentEnabledSetting(..., 2, 1)`）禁用 `MainActivity`/`LeanbackLauncherActivity`，用户无法从桌面回去撤销权限。
- **无障碍服务真实用途**：[MyAccessibilityService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService#onAccessibilityEvent>) 在每次事件都会异步执行 [MyAccessibilityService$1.run()](<resource-unit:#1.dex1 code:com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService$1#run>)，抓取 `getRootInActiveWindow()`，并限定 `packageNames="com.facebook.orca,com.whatsapp"`、`canRetrieveWindowContent=true`、`typeAllMask`，按包名分流到 `WhatsProcessManager` / `MessagesProcessManager` 解析会话，再调 `Utility.startService` 维持 `GoogleServices` 常驻。

即：**无障碍是“零告知、零引导、仅靠通用标签藏于系统列表”的静默植入型 spyware 能力，引导链实际服务于电池优化白名单与图标隐藏，而非无障碍授权。**

```json
{
  "static_visibility": "clear",
  "visibility_note": "APK 未加壳，DEX 完整可反编译，无障碍服务配置、标签与采集逻辑均静态可见。仅两点不在静态范围内：其一，远端 Firebase/FCM 指令（ConstantAppString 中 MAIN_URL_WAL/ABD/OTH 等后端地址与 GoogleServices.checkForCommands 的命令处理）可能在下发后改变行为；其二，代码中根本不存在无障碍引导 UI，因此不存在可静态还原的引导流程。",
  "summary_one_liner": "以“System Update”名义分发的间谍应用对无障碍权限采取零告知零引导的静默植入：冷启动只强推电池优化白名单并立即隐藏桌面图标，无障碍服务在系统列表中仅以通用名“Android Service”示人，获权后专职抓取 WhatsApp/Messenger 聊天界面内容回传。",
  "disguise_identity": {
    "app_display_name": "System Update",
    "claimed_brand_or_persona": "系统更新（冒充 Android 系统 OTA 更新服务）",
    "a11y_service_label": "Android Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签使用通用且中性的“Android Service”，与桌面名“System Update”及真实用途（读取 WhatsApp/Messenger 会话）均不一致；accessibility_service_config.xml 未声明 android:description，也未声明 android:settingsActivity，系统无障碍列表项无任何用途说明；MainActivity 与 LeanbackLauncherActivity 均采用 Theme.Translucent.NoTitleBar.Fullscreen 且 autoRemoveFromRecents/excludeFromRecents，启动后即 setComponentEnabledSetting(..., 2, 1) 隐藏图标（Utility.hideIcon），用户无法回溯检查或撤销权限；双入口（LAUNCHER + LEANBACK_LAUNCHER）互为备份；服务端地址以 char 数组逐字符拼接构造（ConstantAppString.MAIN_URL_*），规避字符串检索。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.update.system.important.MainActivity（android:theme=@android:style/Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标“System Update”触发 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全屏半透明无标题 Activity，不绘制任何界面内容，无任何文字",
      "user_action_requested": "无提示，用户仅看到短暂空白/闪烁",
      "code_anchor": "com.update.system.important.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页（缺失）",
      "screen_or_component": "不存在——无 Dialog、无引导 Activity、无本地或远端 WebView、无悬浮遮罩",
      "trigger_event": "无",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "应用未提供任何无障碍权限的告知或说明页面；assets/ 目录不存在，res/layout* 下无引导布局，代码中无 ACTION_ACCESSIBILITY_SETTINGS 构造",
      "user_action_requested": "无",
      "code_anchor": "全包检索 ACTION_ACCESSIBILITY_SETTINGS / android.settings.* / enabled_accessibility_services 均无应用自身命中"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统页 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS（电池优化忽略白名单），由 MainActivity 以 startActivityForResult(intent, 23) 拉起",
      "trigger_event": "checkBattery()：Build.VERSION.SDK_INT>=23 且 PowerManager.isIgnoringBatteryOptimizations(packageName)==false",
      "ui_carrier": "系统无障碍页（此处为系统电池优化设置页，非无障碍页）",
      "shown_text_verbatim": "无应用自绘文字（系统页文本由 OS 提供）",
      "shown_text_zh": "系统弹出的“是否允许应用忽略电池优化”对话框",
      "user_action_requested": "要求用户点击“允许/Allow”；无应用侧取消或跳过按钮",
      "code_anchor": "com.update.system.important.MainActivity#checkBattery"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 内 Timer（scheduleAtFixedRate(1000L, 500L)）+ MainActivity$1.run → checkBattery",
      "trigger_event": "定时器每 500ms 回调；若 this.a（已加入白名单标记）仍为 false，则 runApp 不取消定时器且再次 startActivityForResult",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户返回或拒绝后，约每 500ms 再次拉起电池优化设置页，直至用户允许",
      "user_action_requested": "强制用户允许忽略电池优化；无跳过选项",
      "code_anchor": "com.update.system.important.MainActivity$1#run / com.update.system.important.MainActivity#checkBattery"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "Utility.startService（启动 GoogleServices 前台服务）+ Utility.hideIcon(MainActivity.class) + finish()",
      "trigger_event": "onActivityResult(23, RESULT_OK) → runApp()；或 SDK<23/异常时 checkBattery 直接置 this.a=true 后 runApp()",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "System Update / Searching for update（ConstantAppString.SEARCHING_FOR_UPDATE）",
      "shown_text_zh": "通知栏前台通知，标题为应用名“System Update”，正文为“正在搜索更新”",
      "user_action_requested": "无需用户操作；同时桌面图标被禁用，用户失去入口",
      "code_anchor": "com.update.system.important.MainActivity#runApp / com.update.system.important.utility.Utility#hideIcon / com.update.system.important.GoogleServices#displayForegroundService"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "后台 Main2Activity（由 GoogleServices.checkForCommands / mScreenStateReceiver / BatteryCharging 经 Utility.displayActivity 拉起，120 秒节流）",
      "trigger_event": "亮/灭屏广播、充电广播、服务端命令轮询；Handler.postDelayed(Main2Activity$1, REFRESH_TIME)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面文字，仅用于后台保活/刷新链路的定时拉起",
      "user_action_requested": "无",
      "code_anchor": "com.update.system.important.utility.Utility#displayActivity / com.update.system.important.Main2Activity#onCreate"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService（系统无障碍服务，标签“Android Service”）",
      "trigger_event": "用户在系统设置中自行开启该服务后，onAccessibilityEvent 每次事件触发 AsyncTask.execute(MyAccessibilityService$1)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Android Service",
      "shown_text_zh": "系统无障碍服务列表项显示名仅为“Android Service”，无描述说明",
      "user_action_requested": "需用户在系统设置中手动开启；应用全程无任何引导（无弹窗、无跳转、无教学）",
      "code_anchor": "com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService#onAccessibilityEvent / com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService$1#run"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml 的 accessibility_service_label = \"Android Service\"，经 Manifest 中 android:label 呈现在系统“无障碍 → 已安装服务”列表项上",
    "res/xml/accessibility_service_config.xml 未声明 android:description，系统无障碍服务详情页无任何用途说明文字（空白）",
    "res/values/strings.xml 的 app_name = \"System Update\"，呈现在桌面图标名与前台服务通知标题（GoogleServices#displayForegroundService 的 setContentTitle）",
    "通知栏正文 \"Searching for update\"（ConstantAppString.SEARCHING_FOR_UPDATE），构成“正在检查系统更新”的假更新语境",
    "res/values/strings.xml 中 common_google_play_services_* 系列（\"%1$s won't work unless you enable Google Play services.\" 等）仅为 Google Play services 库自带资源，未被本应用引导流程使用",
    "应用不存在任何自绘引导弹窗、引导 Activity、本地/远端 WebView 页面或悬浮遮罩——无文字呈现位置"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "System Update",
      "text_zh": "系统更新",
      "source_location": "res/values/strings.xml  key=app_name",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Service",
      "text_zh": "安卓服务",
      "source_location": "res/values/strings.xml  key=accessibility_service_label（Manifest 中无障碍服务 android:label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Searching for update",
      "text_zh": "正在搜索更新",
      "source_location": "com.update.system.important.utility.ConstantAppString#SEARCHING_FOR_UPDATE，用于 GoogleServices#displayForegroundService 前台通知正文",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "对无障碍无任何重跳机制（无 ACTION_ACCESSIBILITY_SETTINGS 构造、无 onResume 检测）。存在的循环仅针对电池优化白名单：MainActivity 的 Timer 以 1000ms 初始延迟、500ms 周期调用 checkBattery，未获白名单即重复 startActivityForResult 拉起系统页，直至 onActivityResult(23, RESULT_OK) 才 cancel。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 绘制引导遮罩，无高仿系统无障碍开关页，无全屏悬浮窗引导；仅存在 Theme.Translucent.NoTitleBar.Fullscreen 的空白全屏 Activity。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权。但采用另一类抗撤除手段：runApp 与 GoogleServices.onCreate 调用 Utility.hideIcon（setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED, DONT_KILL_APP)）禁用 MainActivity 与 LeanbackLauncherActivity，使用户失去桌面入口、难以回到应用检查或关闭已授予的权限。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "纯 UTG 检测不宜等待“跳转无障碍设置”瞬间（该跳转在代码中不存在）。应锚定两个时机：①冷启动后 MainActivity 立即拉起 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 系统页的瞬间（首帧 1 秒内）；②用户在系统设置中开启“Android Service”无障碍后，任意 WhatsApp/Messenger 界面事件触发 onAccessibilityEvent 的瞬间（可用 Monkey/UI 操作进入 WhatsApp 聊天页触发）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动即弹出的系统电池优化授权页（唯一的“引导”动作）",
        "page_identifier": "包名 com.android.settings，界面含“忽略电池优化/Ignore battery optimizations”，来源 Activity 为 com.update.system.important.MainActivity 且自身为全屏半透明空白",
        "why_most_useful": "证明应用冷启动 0 步即强推系统受限授权、且自身无任何说明文字，是“零告知 + 立即索取系统特权”的关键证据；同时可观察 500ms 周期重复拉起行为",
        "observable_utg_signals": [
          "系统页与背后空白透明 Activity 的层级关系（应用未绘制任何说明文本）",
          "返回后 500ms 内再次弹出同一系统页（拒权循环）",
          "设置页返回后桌面图标随即消失（hideIcon 生效）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（唯一的无障碍身份呈现面）",
        "page_identifier": "com.android.settings 无障碍列表中出现 label=\"Android Service\"、包名 com.update.system.important 的服务项，无 description 副文本",
        "why_most_useful": "直接固化身份错配证据：桌面名“System Update”与列表名“Android Service”不一致、无用途说明；可核对应用是否真的没有任何“去开启”引导（用户需完全自行找到此页）",
        "observable_utg_signals": [
          "服务项 label 文本 \"Android Service\" 与 summary/description 为空",
          "进入应用后无任何页面跳转到该设置页（无跳转动作可观测）",
          "列表项所属包名 com.update.system.important 与显示名不符"
        ]
      },
      {
        "page_role": "获权后前台服务通知（假更新语境）",
        "page_identifier": "通知栏通知，标题 \"System Update\"、正文 \"Searching for update\"，channel 由 GoogleServices.createNotificationChannel 创建",
        "why_most_useful": "证明应用以“系统更新检查”为伪装持续前台驻留，且该通知与无障碍采集同时存在，可关联无障碍被用于会话窃取的用途",
        "observable_utg_signals": [
          "通知标题/正文文本",
          "通知出现时桌面已无应用图标（component disabled）",
          "无障碍服务已 enabled 与该通知共存"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在结构性盲区：本应用对无障碍权限完全无引导，因此“UTG 检测无障碍诱导页”这一信号在本样本上必然为空——若检测模型仅依赖“引导弹窗/教学页/悬浮遮罩”特征将漏判。此外无障碍服务标签为通用词“Android Service”且无 description，系统列表页本身不呈现任何可疑文案；行为触发依赖远端 Firebase/FCM 指令（GoogleServices.checkForCommands + MAIN_URL_WAL/ABD/OTH 后端），静态无法完全枚举下发的具体命令。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.update.system.important.MainActivity#checkBattery",
    "com.update.system.important.MainActivity#runApp",
    "com.update.system.important.utility.Utility#hideIcon",
    "com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService#onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml（accessibility_service_label / app_name）"
  ]
}
```

</details>
