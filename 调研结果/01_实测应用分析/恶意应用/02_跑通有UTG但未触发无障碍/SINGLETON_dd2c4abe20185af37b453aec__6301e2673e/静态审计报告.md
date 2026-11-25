# MR_046__6301e2673e｜SINGLETON:dd2c4abe20185af37b453aec5a99c165 — System Update

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：112.5s

## 1. 一句话核心结论

- **核心申请方式**：该样本不做任何无障碍引导教学，只以无描述、名为“Android Service”的隐藏服务静默等待授权，同时用透明 Activity 每 3 秒循环跳转电池优化白名单并靠无障碍事件反复重拉主界面与服务来保活。
- **静态可见性说明**：无障碍服务实现、MainActivity 定时重跳逻辑、GoogleServices 保活与采集器注册均在 classes.dex 中完整静态可见，无加壳、无 assets/HTML、无远端下发页面。需说明的是：静态可见的结论本身是“应用内不存在任何无障碍引导页面/文案/遮罩”，该缺失是事实而非被加密隐藏；全部界面文字仅有 strings.xml 中的 app_name 与 accessibility_service_label。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6301e2673e7495ebdfd34fe51792e97c0ac01221a53219424973d851e7a2ac93` |
| 包名 / 年份 | `com.update.system.important` / 2021 |
| 家族 / 品类 | **SINGLETON:dd2c4abe20185af37b453aec5a99c165**（同池样本数：1） |
| 原始来源标识 | https://blog.zimperium.com/new-advanced-android-malware-posing-as-system-update/ |
| 桌面显示名 | System Update |
| 引导页宣称品牌/身份 | 冒充系统更新/Google 服务组件（包名 com.update.system.important、服务名 Android Service、依赖 GMS/Firebase 库文案），无任何真实厂商身份 |
| 系统无障碍列表服务名 | Android Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签为泛化“Android Service”且完全缺失 android:description，系统授权页无法说明用途；MainActivity/Main2Activity 无 LAUNCHER 入口（仅 LeanbackLauncherActivity 带 LEANBACK_LAUNCHER），手机桌面不显示图标；三个 Activity 均为 Theme.Translucent.NoTitleBar.Fullscreen + excludeFromRecents + autoRemoveFromRecents，界面一闪即隐，不留最近任务痕迹；无伪造 isAccessibilityTool，无多 activity-alias 与同形字。 |
| 无障碍服务类名 | `com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.facebook.orca,com.whatsapp |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.update.system.important.MainActivity（Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents/autoRemoveFromRecents） | 由 GoogleServices.onCreate 的 j.v() 或系统白名单授予后自调用拉起；onCreate 内先执行 b() | 原生Activity | 无 | 无任何交互提示（无取消/跳过按钮） | `com.update.system.important.MainActivity#onCreate` |
| 2 | 跳受限设置 | 系统页 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS（data=package:<pkg>） | MainActivity.b()：SDK_INT>=23 且 PowerManager.isIgnoringBatteryOptimizations(pkg)==false 时 startActivity | 系统无障碍页 | **原文**：无（应用不叠加任何自绘文字）<br>**译注**：直接弹出系统“忽略电池优化”确认页，应用侧无任何解释说明 | 要求用户在该系统页点“允许/Allow”；页面自带取消，但应用随后循环重跳 | `com.update.system.important.MainActivity#b` |
| 3 | 拒权反馈循环 | MainActivity 内部 java.util.Timer + MainActivity$a | onCreate 中 Timer.scheduleAtFixedRate(new MainActivity$a(this), 500L, 3000L)，每 3 秒再次调用 b() | 原生Activity | 无 | 只能点“允许”才会停止循环（w5 置 true 后走第 4 步） | `com.update.system.important.MainActivity$a#run` |
| 4 | 获权后动作 | b.c.a.a.p.j.C() → 再次 startActivity(MainActivity) + startService(GoogleServices)，随后 finishAndRemoveTask() | MainActivity.b() 判定 w5==true 后调用 b.c.a.a.p.j.C(getBaseContext(),false,false,false) | 原生Activity | 无 | 无（无确认、无说明） | `b.c.a.a.p.j#C / com.update.system.important.MainActivity#finish` |
| 5 | 引导说明页（缺失环节） | 无对应组件——不存在无障碍引导 Dialog/Activity/WebView/悬浮窗 | 不适用：代码中无 ACTION_ACCESSIBILITY_SETTINGS、无 Settings$Secure 写 enabled_accessibility_services、无 com.android.settings 字符串 | 不可静态还原 | 无 | 无应用内引导；用户须自行进入系统设置 → 无障碍 → 已下载服务 → Android Service 手动开启 | `res/xml/accessibility_service_config.xml / res/values/strings.xml(accessibility_service_label)` |
| 6 | 获权后动作（采集与自愈） | com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService → MyAccessibilityService$a | onAccessibilityEvent 命中 com.whatsapp / com.facebook.orca 后 AsyncTask 执行 run()，800ms 节流 | 原生Activity | **原文**：onAccessibilityEventForRoot:<br>**译注**：后台抓取 WhatsApp/Facebook 会话根节点交给采集器处理后，每次再调用 j.C() 重新拉起 MainActivity 与 GoogleServices，实现撤权/清后台后的自愈 | 无（后台静默） | `com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService$a#run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目：res/values/strings.xml 的 accessibility_service_label = "Android Service"（android:label=@string/accessibility_service_label），且 res/xml/accessibility_service_config.xml 未声明 android:description，条目下无任何用途说明
- 桌面/最近任务：android:label=@string/app_name = "System Update"；三个 Activity 均 excludeFromRecents+autoRemoveFromRecents，任务栈不留卡片
- 电池优化白名单系统页：应用侧零文案，完全无自绘说明或悬浮引导层
- strings.xml 中 common_google_play_services_* 系列文案（"%1$s won't work unless you enable Google Play services." 等）来自 GMS 库资源，应用自身未在引导流程中引用，属库默认弹窗文本
- 不存在：无障碍引导弹窗、assets 本地 HTML、远端 WebView 教学页、半透明遮罩指引、高仿无障碍开关页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Android Service | 安卓服务 | `res/values/strings.xml key=accessibility_service_label（用于 AndroidManifest 中 MyAccessibilityService 的 android:label）` | 假更新 |
| en | System Update | 系统更新 | `res/values/strings.xml key=app_name` | 假更新 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 在启用 Google Play 服务之前无法工作。 | `res/values/strings.xml key=common_google_play_services_enable_text（GMS 库默认资源，非应用自撰文案）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：电池优化白名单页被拒或返回后，MainActivity 内 Timer 以 500ms 首延时、3000ms 周期反复调用 b() 重跳该页，直到 isIgnoringBatteryOptimizations 为真；无障碍服务被撤销后，onAccessibilityEvent 处理完毕与广播 b.c.a.a.l.a.onReceive 都会调用 j.C() 重新拉起 MainActivity/GoogleServices，形成自愈式重入，但不会重跳无障碍设置页。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 绘制引导遮罩，也未伪造无障碍开关页；仅使用透明全屏 Activity 与系统真实设置页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=21，代码中无应用详情页受限设置教学、无 SESSION_INSTALLER 会话安装逻辑的跳转引导。
- **获权后即时行为与防撤权机制**：存在弱形式的撤权对抗：无障碍事件回调内 800ms 节流后调用 j.C() 重启主界面与服务、GoogleServices.onCreate 用 j.v() 重注册两个启动入口并清除首启标记，可在服务被杀后自动复活；但未发现 GLOBAL_ACTION_BACK/HOME 阻止用户进入设置页撤权，也未发现自动点击确认授权。
- **良性降级 / 替代方案**：无。未提供手动模式、仅观看模式或 ADB 授权等降级路径；未授予电池白名单时应用不做功能降级而是持续弹窗。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 b.c.a.a.p.j#C 为最佳拉起钩子（MainActivity 与 GoogleServices 的统一重入口），以及 MainActivity#b 中 ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 的 startActivity 调用瞬间；同时监听无障碍事件后 800ms 内 j.C() 的二次拉起，用于捕获撤权后的自愈行为。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区在于“引导阶段完全无文本”：应用从不自撰任何无障碍说明文案，纯图/空文本问题在此表现为零文案，UTG 文本判定会直接空转，必须改用“系统页循环次数 + 服务名伪装 + 无 description + packageNames 仅 WhatsApp/Facebook”组合特征。此外无障碍授权非应用内跳转触发，若用户从未手动开启，UTG 全程只能看到电池白名单循环，无障碍链不会激活。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前透明壳页（无文案）** | com.update.system.important.MainActivity，Theme.Translucent.NoTitleBar.Fullscreen，界面为空 | 确认应用自产界面零文案、零控件，可据此排除“诱导教学页”假设，把检测重心转向循环跳转与系统服务伪装 | Activity 名 MainActivity 且无可见文本节点；任务栈无卡片（excludeFromRecents）；启动后 500ms 内即出现系统白名单页 |
| **循环跳转的电池优化白名单系统页** | 系统页 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，data=package:com.update.system.important | 这是应用唯一主动引导的受限设置，且以 3 秒周期循环重跳，是最强的“拒权循环/强制授权”判别信号 | 同一系统页在 3 秒内重复出现 ≥2 次；目标包名 com.update.system.important；应用侧无任何解释文本叠加 |
| **系统无障碍服务列表项（授权入口）** | 系统设置 → 无障碍 → 已下载服务，条目名 “Android Service”，无描述子文本 | 该页是授权发生地，条目名伪装成系统组件且无用途说明，是身份冒充与知情同意缺失的直接证据 | 条目文本 Android Service 且无 description 行；服务包名 com.update.system.important；开启后应用无任何界面反馈 |
| **获权后自愈重拉（撤权测试页）** | 手动关闭无障碍后 1-2 秒内 MainActivity 与 GoogleServices 重新出现 | 验证 onAccessibilityEvent/j.C() 的重入链是否形成撤权对抗 | 撤权后前台再次出现 MainActivity；GoogleServices 服务进程复现；任务栈仍无可见卡片 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.update.system.important.MainActivity#onCreate`
- `com.update.system.important.MainActivity#b`
- `com.update.system.important.MainActivity$a#run`
- `b.c.a.a.p.j#C`
- `com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService$a#run`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（代码级定向核验）

**核心发现：该样本并不存在“引导用户开启无障碍”的 UI 流程。** 静态代码中完全没有 `ACTION_ACCESSIBILITY_SETTINGS` 跳转，没有 `com.android.settings` 字符串，没有 assets/HTML/WebView，也没有无障碍说明页；搜索 `ACCESSIBILITY_SETTINGS`、`installed_service`、`Settings$Accessibility` 均无命中，只有系统资源 ID 中的 `accessibility_*` 常量。无障碍权限完全靠**“声明一个无描述、名称伪装的系统级服务，静默等待用户或外部渠道开启”**，而应用自身可见的 UI 只用于**后台保活与自启动循环**。

**运行期实际可见的页面流转（已静态还原）**
1. `MainActivity` 为 `Theme.Translucent.NoTitleBar.Fullscreen`，`excludeFromRecents`/`autoRemoveFromRecents`，且**没有 MAIN/LAUNCHER intent-filter**（只有 `LeanbackLauncherActivity` 带 `LEANBACK_LAUNCHER`），手机桌面无图标，属隐藏启动。
2. `MainActivity.onCreate` → `b()`：SDK≥23 且未加入电池白名单时，直接 `startActivity(ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)`，置 `w5=false`；随后 `Timer.scheduleAtFixedRate(500ms, 3000ms)` 每 3 秒再调 `b()`，形成**拒权/返回后反复重跳系统白名单页的循环**，用户不授予就一直弹。
3. 授予后 `w5=true` → `b.c.a.a.p.j.C()` → 再次启动 `MainActivity` + `startService(GoogleServices)` → `finishAndRemoveTask()`，全程无任何说明文字。
4. `GoogleServices.onCreate` 用 `j.v()` 重新激活 `MainActivity`/`LeanbackLauncherActivity` 两个入口并清除首次标记 `B0`，随后注册联系人/通话记录/图片/视频 ContentObserver、剪贴板监听、亮灭屏广播、FCM 通道——真正的业务在服务里。
5. 无障碍服务 `MyAccessibilityService` 在系统列表显示为 **“Android Service”**（`res/values/strings.xml` 的 `accessibility_service_label`），**无 `android:description`**（预筛为 `[]`，XML 亦未声明），配置只监控 `com.whatsapp`、`com.facebook.orca`，`canRetrieveWindowContent=true`，事件回调里 `getRootInActiveWindow()` 抓取会话节点交给 `b.c.a.a.h.j.b.c` / `b.c.a.a.h.j.c.c` 处理，**并且每次处理后（800ms 节流）再调 `j.C()` 重启主界面与服务**，即“获权后自愈式重拉”。
6. 另有 `b.c.a.a.l.a.onReceive` 广播同样触发 `j.C()`，构成多处重入点。

**对 UTG 检测的直接含义**：不存在“引导弹窗/教学页/遮罩/高仿设置页”可截取，唯一可稳定捕获的应用自产页面是**透明的电池优化白名单跳转（3 秒循环）**与**系统无障碍列表中名为“Android Service”的空描述条目**；诱导文本为零，识别必须依赖“循环跳转 + 系统服务名伪装 + 无描述 + 目标包名仅 WhatsApp/Facebook”的组合特征，而非 OCR 文案。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍服务实现、MainActivity 定时重跳逻辑、GoogleServices 保活与采集器注册均在 classes.dex 中完整静态可见，无加壳、无 assets/HTML、无远端下发页面。需说明的是：静态可见的结论本身是“应用内不存在任何无障碍引导页面/文案/遮罩”，该缺失是事实而非被加密隐藏；全部界面文字仅有 strings.xml 中的 app_name 与 accessibility_service_label。",
  "summary_one_liner": "该样本不做任何无障碍引导教学，只以无描述、名为“Android Service”的隐藏服务静默等待授权，同时用透明 Activity 每 3 秒循环跳转电池优化白名单并靠无障碍事件反复重拉主界面与服务来保活。",
  "disguise_identity": {
    "app_display_name": "System Update",
    "claimed_brand_or_persona": "冒充系统更新/Google 服务组件（包名 com.update.system.important、服务名 Android Service、依赖 GMS/Firebase 库文案），无任何真实厂商身份",
    "a11y_service_label": "Android Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签为泛化“Android Service”且完全缺失 android:description，系统授权页无法说明用途；MainActivity/Main2Activity 无 LAUNCHER 入口（仅 LeanbackLauncherActivity 带 LEANBACK_LAUNCHER），手机桌面不显示图标；三个 Activity 均为 Theme.Translucent.NoTitleBar.Fullscreen + excludeFromRecents + autoRemoveFromRecents，界面一闪即隐，不留最近任务痕迹；无伪造 isAccessibilityTool，无多 activity-alias 与同形字。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.update.system.important.MainActivity（Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents/autoRemoveFromRecents）",
      "trigger_event": "由 GoogleServices.onCreate 的 j.v() 或系统白名单授予后自调用拉起；onCreate 内先执行 b()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全透明无标题全屏页面，不渲染任何文本或控件",
      "user_action_requested": "无任何交互提示（无取消/跳过按钮）",
      "code_anchor": "com.update.system.important.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "跳受限设置",
      "screen_or_component": "系统页 android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS（data=package:<pkg>）",
      "trigger_event": "MainActivity.b()：SDK_INT>=23 且 PowerManager.isIgnoringBatteryOptimizations(pkg)==false 时 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用不叠加任何自绘文字）",
      "shown_text_zh": "直接弹出系统“忽略电池优化”确认页，应用侧无任何解释说明",
      "user_action_requested": "要求用户在该系统页点“允许/Allow”；页面自带取消，但应用随后循环重跳",
      "code_anchor": "com.update.system.important.MainActivity#b"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 内部 java.util.Timer + MainActivity$a",
      "trigger_event": "onCreate 中 Timer.scheduleAtFixedRate(new MainActivity$a(this), 500L, 3000L)，每 3 秒再次调用 b()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户返回或拒绝后，每 3 秒重新拉起系统白名单页，形成无法退出的循环弹窗",
      "user_action_requested": "只能点“允许”才会停止循环（w5 置 true 后走第 4 步）",
      "code_anchor": "com.update.system.important.MainActivity$a#run"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "b.c.a.a.p.j.C() → 再次 startActivity(MainActivity) + startService(GoogleServices)，随后 finishAndRemoveTask()",
      "trigger_event": "MainActivity.b() 判定 w5==true 后调用 b.c.a.a.p.j.C(getBaseContext(),false,false,false)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "白名单通过后立即重启主界面与后台服务并清空任务栈，界面消失，用户看不到任何后续说明",
      "user_action_requested": "无（无确认、无说明）",
      "code_anchor": "b.c.a.a.p.j#C / com.update.system.important.MainActivity#finish"
    },
    {
      "step": 5,
      "stage": "引导说明页（缺失环节）",
      "screen_or_component": "无对应组件——不存在无障碍引导 Dialog/Activity/WebView/悬浮窗",
      "trigger_event": "不适用：代码中无 ACTION_ACCESSIBILITY_SETTINGS、无 Settings$Secure 写 enabled_accessibility_services、无 com.android.settings 字符串",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "应用从不向用户解释无障碍用途，也不主动跳转无障碍设置页，授权完全依赖用户在系统列表中自行找到“Android Service”并开启",
      "user_action_requested": "无应用内引导；用户须自行进入系统设置 → 无障碍 → 已下载服务 → Android Service 手动开启",
      "code_anchor": "res/xml/accessibility_service_config.xml / res/values/strings.xml(accessibility_service_label)"
    },
    {
      "step": 6,
      "stage": "获权后动作（采集与自愈）",
      "screen_or_component": "com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService → MyAccessibilityService$a",
      "trigger_event": "onAccessibilityEvent 命中 com.whatsapp / com.facebook.orca 后 AsyncTask 执行 run()，800ms 节流",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "onAccessibilityEventForRoot: ",
      "shown_text_zh": "后台抓取 WhatsApp/Facebook 会话根节点交给采集器处理后，每次再调用 j.C() 重新拉起 MainActivity 与 GoogleServices，实现撤权/清后台后的自愈",
      "user_action_requested": "无（后台静默）",
      "code_anchor": "com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService$a#run"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目：res/values/strings.xml 的 accessibility_service_label = \"Android Service\"（android:label=@string/accessibility_service_label），且 res/xml/accessibility_service_config.xml 未声明 android:description，条目下无任何用途说明",
    "桌面/最近任务：android:label=@string/app_name = \"System Update\"；三个 Activity 均 excludeFromRecents+autoRemoveFromRecents，任务栈不留卡片",
    "电池优化白名单系统页：应用侧零文案，完全无自绘说明或悬浮引导层",
    "strings.xml 中 common_google_play_services_* 系列文案（\"%1$s won't work unless you enable Google Play services.\" 等）来自 GMS 库资源，应用自身未在引导流程中引用，属库默认弹窗文本",
    "不存在：无障碍引导弹窗、assets 本地 HTML、远端 WebView 教学页、半透明遮罩指引、高仿无障碍开关页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Android Service",
      "text_zh": "安卓服务",
      "source_location": "res/values/strings.xml key=accessibility_service_label（用于 AndroidManifest 中 MyAccessibilityService 的 android:label）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "System Update",
      "text_zh": "系统更新",
      "source_location": "res/values/strings.xml key=app_name",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 在启用 Google Play 服务之前无法工作。",
      "source_location": "res/values/strings.xml key=common_google_play_services_enable_text（GMS 库默认资源，非应用自撰文案）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "电池优化白名单页被拒或返回后，MainActivity 内 Timer 以 500ms 首延时、3000ms 周期反复调用 b() 重跳该页，直到 isIgnoringBatteryOptimizations 为真；无障碍服务被撤销后，onAccessibilityEvent 处理完毕与广播 b.c.a.a.l.a.onReceive 都会调用 j.C() 重新拉起 MainActivity/GoogleServices，形成自愈式重入，但不会重跳无障碍设置页。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 绘制引导遮罩，也未伪造无障碍开关页；仅使用透明全屏 Activity 与系统真实设置页。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=21，代码中无应用详情页受限设置教学、无 SESSION_INSTALLER 会话安装逻辑的跳转引导。",
    "post_grant_anti_removal": "存在弱形式的撤权对抗：无障碍事件回调内 800ms 节流后调用 j.C() 重启主界面与服务、GoogleServices.onCreate 用 j.v() 重注册两个启动入口并清除首启标记，可在服务被杀后自动复活；但未发现 GLOBAL_ACTION_BACK/HOME 阻止用户进入设置页撤权，也未发现自动点击确认授权。",
    "benign_graceful_degradation": "无。未提供手动模式、仅观看模式或 ADB 授权等降级路径；未授予电池白名单时应用不做功能降级而是持续弹窗。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 b.c.a.a.p.j#C 为最佳拉起钩子（MainActivity 与 GoogleServices 的统一重入口），以及 MainActivity#b 中 ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 的 startActivity 调用瞬间；同时监听无障碍事件后 800ms 内 j.C() 的二次拉起，用于捕获撤权后的自愈行为。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前透明壳页（无文案）",
        "page_identifier": "com.update.system.important.MainActivity，Theme.Translucent.NoTitleBar.Fullscreen，界面为空",
        "why_most_useful": "确认应用自产界面零文案、零控件，可据此排除“诱导教学页”假设，把检测重心转向循环跳转与系统服务伪装",
        "observable_utg_signals": ["Activity 名 MainActivity 且无可见文本节点", "任务栈无卡片（excludeFromRecents）", "启动后 500ms 内即出现系统白名单页"]
      },
      {
        "page_role": "循环跳转的电池优化白名单系统页",
        "page_identifier": "系统页 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，data=package:com.update.system.important",
        "why_most_useful": "这是应用唯一主动引导的受限设置，且以 3 秒周期循环重跳，是最强的“拒权循环/强制授权”判别信号",
        "observable_utg_signals": ["同一系统页在 3 秒内重复出现 ≥2 次", "目标包名 com.update.system.important", "应用侧无任何解释文本叠加"]
      },
      {
        "page_role": "系统无障碍服务列表项（授权入口）",
        "page_identifier": "系统设置 → 无障碍 → 已下载服务，条目名 “Android Service”，无描述子文本",
        "why_most_useful": "该页是授权发生地，条目名伪装成系统组件且无用途说明，是身份冒充与知情同意缺失的直接证据",
        "observable_utg_signals": ["条目文本 Android Service 且无 description 行", "服务包名 com.update.system.important", "开启后应用无任何界面反馈"]
      },
      {
        "page_role": "获权后自愈重拉（撤权测试页）",
        "page_identifier": "手动关闭无障碍后 1-2 秒内 MainActivity 与 GoogleServices 重新出现",
        "why_most_useful": "验证 onAccessibilityEvent/j.C() 的重入链是否形成撤权对抗",
        "observable_utg_signals": ["撤权后前台再次出现 MainActivity", "GoogleServices 服务进程复现", "任务栈仍无可见卡片"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区在于“引导阶段完全无文本”：应用从不自撰任何无障碍说明文案，纯图/空文本问题在此表现为零文案，UTG 文本判定会直接空转，必须改用“系统页循环次数 + 服务名伪装 + 无 description + packageNames 仅 WhatsApp/Facebook”组合特征。此外无障碍授权非应用内跳转触发，若用户从未手动开启，UTG 全程只能看到电池白名单循环，无障碍链不会激活。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "LURE_FAKE_UPDATE_OR_INSTALL"
  ],
  "code_anchors": [
    "com.update.system.important.MainActivity#onCreate",
    "com.update.system.important.MainActivity#b",
    "com.update.system.important.MainActivity$a#run",
    "b.c.a.a.p.j#C",
    "com.update.system.important.collector.socialmessages.accessibility.MyAccessibilityService$a#run",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

**覆盖边界说明**：本次在工具预算内完成 Manifest、无障碍配置、启动链、保活链与无障碍事件链的静态核验，未启动动态分析，也未登记项目风险条目（受 14 次调用上限约束）。核心结论“应用内不存在无障碍引导 UI、以系统页循环 + 服务名伪装实现授权”为代码已证实事实；无障碍授权实际由何渠道触发（用户手动或投放侧指引）不在包内，属包外边界。

</details>
