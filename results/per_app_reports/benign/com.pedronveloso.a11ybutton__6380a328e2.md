# BN_032__6380a328e2｜极简桌面与双击锁屏 — Accessibility Button Launcher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：143.0s

## 1. 一句话核心结论

- **核心申请方式**：以原生 Compose 分步引导页透明说明无障碍用途、提供 Skip setup 取消路径，仅由用户点击主按钮跳转系统 ACCESSIBILITY_SETTINGS，服务本身收紧事件监听仅响应无障碍按钮回调拉起用户选定应用。
- **静态可见性说明**：DEX 未加壳（R8 混淆但结构完整可读），引导界面为 Compose 原生实现；无 WebView/HTML、无加密资源、无二阶段载荷，引导与跳转逻辑全部静态可还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6380a328e2a7c3f453bb7fe3d2fd2e090b8c5fdf7d21d02f2f99766e8c21413a` |
| 包名 / 年份 | `com.pedronveloso.a11ybutton` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.pedronveloso.a11ybutton_4.apk |
| 桌面显示名 | Accessibility Button Launcher |
| 引导页宣称品牌/身份 | Accessibility Button Launcher（Pedro Veloso 开源项目，Apache 2.0） |
| 系统无障碍列表服务名 | Accessibility Button Launcher |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无；名称与功能一致，无障碍服务标签、android:description 与桌面显示名统一，无同形字、无空白挤出、无多 activity-alias、未伪造 isAccessibilityTool |
| 无障碍服务类名 | `com.pedronveloso.a11ybutton.service.ShortcutLaunchAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |
| 系统设置项说明 (`android:description`) | Launches your selected app from the accessibility button or shortcut. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.pedronveloso.a11ybutton.MainActivity（Compose onboarding 欢迎步，onboarding_step 计数） | onCreate → jp.a(this, new op(...)) 渲染引导首页；首次安装未完成 onboarding_completed 时展示 | 原生Activity | **原文**：One button, one app / Once you enable Android’s Accessibility button and choose an app or app shortcut, you can open it while using other apps. The button belongs to Android itself. It may appear in the navigation bar or float at the edge of your screen, depending on your device and settings. / Accept and continue<br>**译注**：一个按钮，一个应用；启用 Android 的无障碍按钮并选择应用或应用快捷方式后，即可在其他应用中打开它。该按钮属于 Android 本身，可能出现在导航栏或屏幕边缘。/ 接受并继续 | 点击“Accept and continue”继续；亦可点击“Skip setup”跳过（有二次确认） | `c81#d（onboarding_primary_button / onboarding_skip_button）+ res/values/strings.xml onboarding_welcome_*` |
| 2 | 引导说明页 | MainActivity onboarding「Turn on the service」步骤页（Step %1$d of %2$d） | 欢迎步点击 Continue 后进入；主按钮回调触发跳转 | 原生Activity | **原文**：Turn on the service / Android needs you to switch it on in Accessibility settings. Look for "Accessibility Button Launcher" and turn it on. On some phones, like Samsung, you'll need to tap "Installed apps" first to find it.<br>**译注**：开启服务；Android 需要你在无障碍设置中手动开启它，找到“Accessibility Button Launcher”并打开。部分机型（如三星）需先点“已安装的应用”。 | 点击主按钮前往系统无障碍设置；也可 Back 返回或 Skip setup | `res/values/strings.xml onboarding_service_title/onboarding_service_body；onboarding_back_button` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 用户点击引导主按钮 → p1.a() case 3/4 → Context.startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(FLAG_ACTIVITY_NEW_TASK)) | 系统无障碍页 | **原文**：Opening accessibility settings（代码日志文案）；系统页展示服务项：Accessibility Button Launcher / Launches your selected app from the accessibility button or shortcut.<br>**译注**：打开无障碍设置；系统列表项显示服务名与描述“通过无障碍按钮或快捷方式启动你选择的应用”。 | 用户在系统列表中手动找到并开启该服务（无任何自动化代点） | `p1.a() case 3 / case 4；res/values/strings.xml accessibility_service_label / accessibility_service_description` |
| 4 | 业务功能触发 | MainActivity onboarding「Pick what the button opens」→ 应用选择器（picker_title） | 设置页返回后继续引导；选择应用或应用快捷方式 | 原生Activity | **原文**：Pick what the button opens / Choose an app, or a specific action inside an app.<br>**译注**：选择按钮要打开的内容；选择一个应用，或应用内的某个具体操作（应用快捷方式）。 | 选择目标应用/快捷方式（可 Back 返回，可 Skip setup） | `res/values/strings.xml onboarding_action_*、picker_title、picker_mode_apps/picker_mode_shortcuts` |
| 5 | 引导说明页 | MainActivity onboarding「Keep it running」电池优化说明步 | 选择目标后进入；主按钮 → p1.a() case 7 打开 IGNORE_BATTERY_OPTIMIZATION_SETTINGS 列表页 | 原生Activity | **原文**：Keep it running / Some phones put background apps to sleep, which can stop the button from working. Allowing unrestricted battery use prevents that.<br>**译注**：保持运行；部分手机让后台应用休眠，会导致按钮失效，允许不受限电池使用可避免。 | 点击“Allow Unrestricted Battery Access”/“Open Battery Settings”进入系统电池优化页；可跳过该步 | `p1.a() case 7；res/values/strings.xml onboarding_battery_*、background_protection_request_battery_exemption` |
| 6 | 获权后动作 | onboarding 完成页（You're all set）→ 首页 Shortcut ready 清单 | 完成引导或跳过引导后；ServiceCheckWorker/首页清单读取服务连接状态 | 原生Activity | **原文**：You're all set / Press the accessibility button any time to open your app. You can revisit these steps from the Home screen.<br>**译注**：全部就绪；随时按下无障碍按钮打开你的应用，可从首页重新查看这些步骤。 | 点击“Done”结束引导 | `res/values/strings.xml onboarding_complete_*；c81#d onboarding_finish` |
| 7 | 拒权反馈循环 | 通知栏 Service status 通知（Accessibility shortcut is off）+ OpenSettingsReceiver | 服务被关闭（如应用更新后）→ 发通知；用户点击通知动作“Open Settings” → OpenSettingsReceiver.onReceive 取消通知并跳 ACCESSIBILITY_SETTINGS | 通知栏 | **原文**：Accessibility shortcut is off / The accessibility service was disabled. This can happen after an app update. Tap Open Settings to re-enable it. / Open Settings / Don't remind me<br>**译注**：无障碍快捷方式已关闭；服务被停用，可能是应用更新导致，点“打开设置”重新启用。/ 打开设置 / 别再提醒我 | 用户可选“Open Settings”重新启用，或“Don't remind me”永久不再提醒（OptOutReceiver）；非强制、不循环 | `com.pedronveloso.a11ybutton.receiver.OpenSettingsReceiver.onReceive；com.pedronveloso.a11ybutton.receiver.OptOutReceiver；notification_service_disabled_*、notification_action_opt_out` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内 Compose 引导页（onboarding 多步：欢迎/开启服务/选择目标/电池说明/完成），非系统 Dialog 也非 WebView
- 首页 Home 清单与披露卡：main_disclosure_title / main_disclosure_body（“Why Accessibility access is required”）
- 首页行动按钮 main_action_open_settings（“Open Accessibility Settings”）
- 系统无障碍服务列表项：android:label=“Accessibility Button Launcher”、android:description=“Launches your selected app from the accessibility button or shortcut.”
- 通知栏 Service status 频道通知（notification_service_disabled_title/body + Open Settings / Don't remind me 两个动作）
- Service Help 页（AccessibilityServiceSettingsActivity）：service_settings_body 说明“Open the App / Open App Info”排障入口
- FAQ 页：faq_question_button / main_troubleshooting_button 等问答文本
- 跳过确认弹窗：onboarding_skip_confirmation_title/body（Skip setup? / Skip for now / Continue setup）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | The service listens for the system Accessibility trigger and launches only the app you select. It does not add automation or overlays. | 该服务仅监听系统无障碍触发事件并启动你所选择的应用，不添加自动化或悬浮层。 | `res/values/strings.xml key=main_disclosure_body` | 良性透明说明 |
| en | Android needs you to switch it on in Accessibility settings. Look for "Accessibility Button Launcher" and turn it on. On some phones, like Samsung, you'll need to tap "Installed apps" first to find it. | Android 需要你在无障碍设置中手动开启它。找到“Accessibility Button Launcher”并打开；部分机型（如三星）需先点“已安装的应用”。 | `res/values/strings.xml key=onboarding_service_body` | 良性透明说明 |
| en | Launches your selected app from the accessibility button or shortcut. | 通过无障碍按钮或快捷方式启动你选择的应用。 | `res/values/strings.xml key=accessibility_service_description（Manifest service android:description）` | 良性透明说明 |
| en | You can finish setting up later from the Home screen. It's easier to follow these steps now, especially the first time. | 你可以稍后在首页完成设置；现在按步骤做会更简单，尤其是第一次使用。 | `res/values/strings.xml key=onboarding_skip_confirmation_body` | 良性透明说明 |
| en | Some phones put background apps to sleep, which can stop the button from working. Allowing unrestricted battery use prevents that. | 部分手机让后台应用休眠，会导致按钮失效；允许不受限电池使用可避免此问题。 | `res/values/strings.xml key=onboarding_battery_body` | 良性透明说明 |
| en | The accessibility service was disabled. This can happen after an app update. Tap Open Settings to re-enable it. | 无障碍服务已被停用，可能是应用更新所致；点“打开设置”重新启用。 | `res/values/strings.xml key=notification_service_disabled_body` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性降级：从系统设置返回后停留在首页/引导页并显示 Setup needed 状态，不自动重跳；用户可点“Skip setup”并在二次确认中选择“Skip for now”退出引导；服务被系统关闭时只发一次可关闭的通知，并提供“Don't remind me”（OptOutReceiver）永久停止提醒，无 Timer 拉起、无 onResume 死循环。
- **遮罩叠层 / 高仿系统设置页**：无；不使用悬浮窗/半透明遮罩，也不伪造系统无障碍开关页，跳转的是真实 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无；未出现“应用详情→右上角菜单→允许受限设置”的分步教学，也未使用 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无；获权后仅注册 AccessibilityButtonController 回调并在点击时 startActivity 拉起用户选定目标；未自点确认、未监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权，onAccessibilityEvent 为空实现。
- **良性降级 / 替代方案**：提供 Skip setup（含 Skip for now 二次确认）稍后从首页继续；FAQ 与 Service Help 页提供手动排障（Open the App / Open App Info）；服务未启用或目标不可用时回跳 MainActivity 显示 Last trigger result 并给出重新选择提示，功能明确不可用时降级提示而非反复索取权限。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 MainActivity 出现 onboarding 欢迎步（“One button, one app”/“Accept and continue”）时即拉起 UTG 抓页；其次在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（p1.a case 3/4 或 OpenSettingsReceiver）前 500ms 抓取上一页；再次在系统无障碍列表中定位服务项文本时抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导全为原生 Compose 文本，UTG 可直接提取；注意本应用为 R8 混淆（类名 c81/p1 等短名），静态定位需借助 strings 资源锚定；电池优化权限虽已声明但仅打开系统电池优化列表页而非直接请求豁免弹窗，勿误判为绕过系统授权。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页** | MainActivity Compose onboarding：标题“One button, one app”与按钮“Accept and continue”“Skip setup” | 决定是否存在强制/不可取消引导，以及引导文案是否如实说明用途 | 是否存在可见的 Skip setup 按钮；文案是否提及“launches only the app you select”；是否出现故障恐吓/假更新/安全反诈类词汇 |
| **跳转前“Turn on the service”教学页** | 标题“Turn on the service”、正文含“Accessibility Button Launcher”“Installed apps”、步骤计数“Step X of Y” | 区分正常指路（告知真实服务名）与伪造系统页/教唆忽略警告 | 是否指名真实服务标签；是否要求关闭安全防护或忽略系统警告；主按钮文本是否为 Open Accessibility Settings |
| **系统无障碍服务列表项** | Settings 无障碍页中条目“Accessibility Button Launcher”，副标题“Launches your selected app from the accessibility button or shortcut.” | 核对系统侧展示名/描述与应用内宣称是否一致，验证无身份混淆 | 服务名与包显示名是否一致；描述是否与实际能力（仅启动选定应用）一致；是否存在多个同名/近名服务项 |
| **拒权返回后首页/通知** | 首页“Setup needed”状态与通知栏“Accessibility shortcut is off”通知（含 Open Settings / Don't remind me） | 判定是否存在拒权重跳循环或强制催促 | 返回后是否再次自动弹设置页；通知是否可关闭且含 Don't remind me；是否存在定时重复通知 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.pedronveloso.a11ybutton.MainActivity.onCreate / MainActivity.i`
- `p1.a()（case 3/4 → android.settings.ACCESSIBILITY_SETTINGS；case 1 → APPLICATION_DETAILS_SETTINGS；case 7 → IGNORE_BATTERY_OPTIMIZATION_SETTINGS）`
- `com.pedronveloso.a11ybutton.receiver.OpenSettingsReceiver.onReceive`
- `com.pedronveloso.a11ybutton.service.ShortcutLaunchAccessibilityService.onServiceConnected / onAccessibilityEvent / b`
- `res/values/strings.xml（onboarding_service_body、main_disclosure_body、accessibility_service_description、notification_service_disabled_body）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向审计）

**核心事实：这是一个透明说明、可跳过、无诱导的良性无障碍申请流程。**

1. **入口与载体**：全部引导都在 [MainActivity](<resource-unit:#1.dex1 code:com.pedronveloso.a11ybutton.MainActivity>) 内以 Jetpack Compose 原生界面实现（`c81#d` 渲染 onboarding_primary_button / onboarding_skip_button / onboarding_back_button / onboarding_step 计数器），**无 WebView、无本地 HTML、无悬浮窗遮罩**；`assets/` 与 `res/` 下未发现引导 HTML。
2. **无障碍跳转点仅两处，均由用户点击触发**：
   - [p1.a()](<resource-unit:#1.dex1 code:p1#a>) 的 `case 3/4` 显式构造 `Intent("android.settings.ACCESSIBILITY_SETTINGS")`（日志文案 `Opening accessibility settings`），由引导页"主按钮"与首页 `main_action_open_settings`（"Open Accessibility Settings"）驱动；
   - [OpenSettingsReceiver.onReceive()](<resource-unit:#1.dex1 code:com.pedronveloso.a11ybutton.receiver.OpenSettingsReceiver#onReceive>) 取消通知后跳同一设置页，仅在**用户点击通知栏 "Open Settings"** 时触发，且通知带 `notification_action_opt_out`（"Don't remind me"）→ [OptOutReceiver](<resource-unit:#1.dex1 code:com.pedronveloso.a11ybutton.receiver.OptOutReceiver>)，一次性提醒、无死循环重跳。
   - 同方法还提供 `ACTION_APPLICATION_DETAILS_SETTINGS`（`Open App Info`）与 `IGNORE_BATTERY_OPTIMIZATION_SETTINGS`（`Open Battery Settings`），均为用户主动的排障入口，**未见 13+ 受限设置（"允许受限设置"）分步教学，也未见 Session/安装器绕过**。
3. **文案诚实、可取消**：`main_disclosure_title`="Why Accessibility access is required"、`main_disclosure_body`="The service listens for the system Accessibility trigger and launches only the app you select. It does not add automation or overlays."；`onboarding_service_body` 明确指路"Look for \"Accessibility Button Launcher\" and turn it on"（Samsung 需先点 "Installed apps"）；`onboarding_skip`/`onboarding_skip_confirmation_*` 提供 "Skip setup → Skip for now"，属显式降级路径（`onboarding_skip_confirmation_body`："You can finish setting up later from the Home screen"）。
4. **能力与声明一致，无越权面**：[onServiceConnected()](<resource-unit:#1.dex1 code:com.pedronveloso.a11ybutton.service.ShortcutLaunchAccessibilityService#onServiceConnected>) 主动将 `eventTypes=0`、`notificationTimeout=0`、`feedbackType=16` 收紧，[onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.pedronveloso.a11ybutton.service.ShortcutLaunchAccessibilityService#onAccessibilityEvent>) 为空实现，仅注册 `AccessibilityButtonController` 回调；获权后动作只有 `startActivity` 拉起用户选定目标（`b()` 解析 ComponentName，`a()` 解析 shortcut），失败时回跳 MainActivity 弹 `Last trigger result`（含 `Dismiss` 按钮）。无自点确认、无 GLOBAL_ACTION 阻止撤权、无 `isAccessibilityTool` 伪造。
5. **身份一致**：显示名、无障碍服务标签、`android:description` 三者均为真实名称 "Accessibility Button Launcher"，无同形字/空白挤出/多 activity-alias。
6. **唯一可讨论项**：声明 `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`，但代码并未调用 `ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 直接弹系统授权框，只打开电池优化设置列表页（用户自行操作），且文案如实解释原因（"Some phones put background apps to sleep…"），不构成恶意诱导。

**结论：未发现诱导或欺诈性无障碍权限获取行为，无需登记风险。** 静态可见性完整（无加壳，`static_visibility=clear`）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳（R8 混淆但结构完整可读），引导界面为 Compose 原生实现；无 WebView/HTML、无加密资源、无二阶段载荷，引导与跳转逻辑全部静态可还原。",
  "summary_one_liner": "以原生 Compose 分步引导页透明说明无障碍用途、提供 Skip setup 取消路径，仅由用户点击主按钮跳转系统 ACCESSIBILITY_SETTINGS，服务本身收紧事件监听仅响应无障碍按钮回调拉起用户选定应用。",
  "disguise_identity": {
    "app_display_name": "Accessibility Button Launcher",
    "claimed_brand_or_persona": "Accessibility Button Launcher（Pedro Veloso 开源项目，Apache 2.0）",
    "a11y_service_label": "Accessibility Button Launcher",
    "identity_mismatch": false,
    "obfuscation_tricks": "无；名称与功能一致，无障碍服务标签、android:description 与桌面显示名统一，无同形字、无空白挤出、无多 activity-alias、未伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.pedronveloso.a11ybutton.MainActivity（Compose onboarding 欢迎步，onboarding_step 计数）",
      "trigger_event": "onCreate → jp.a(this, new op(...)) 渲染引导首页；首次安装未完成 onboarding_completed 时展示",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "One button, one app / Once you enable Android’s Accessibility button and choose an app or app shortcut, you can open it while using other apps. The button belongs to Android itself. It may appear in the navigation bar or float at the edge of your screen, depending on your device and settings. / Accept and continue",
      "shown_text_zh": "一个按钮，一个应用；启用 Android 的无障碍按钮并选择应用或应用快捷方式后，即可在其他应用中打开它。该按钮属于 Android 本身，可能出现在导航栏或屏幕边缘。/ 接受并继续",
      "user_action_requested": "点击“Accept and continue”继续；亦可点击“Skip setup”跳过（有二次确认）",
      "code_anchor": "c81#d（onboarding_primary_button / onboarding_skip_button）+ res/values/strings.xml onboarding_welcome_*"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity onboarding「Turn on the service」步骤页（Step %1$d of %2$d）",
      "trigger_event": "欢迎步点击 Continue 后进入；主按钮回调触发跳转",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Turn on the service / Android needs you to switch it on in Accessibility settings. Look for \"Accessibility Button Launcher\" and turn it on. On some phones, like Samsung, you'll need to tap \"Installed apps\" first to find it.",
      "shown_text_zh": "开启服务；Android 需要你在无障碍设置中手动开启它，找到“Accessibility Button Launcher”并打开。部分机型（如三星）需先点“已安装的应用”。",
      "user_action_requested": "点击主按钮前往系统无障碍设置；也可 Back 返回或 Skip setup",
      "code_anchor": "res/values/strings.xml onboarding_service_title/onboarding_service_body；onboarding_back_button"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户点击引导主按钮 → p1.a() case 3/4 → Context.startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(FLAG_ACTIVITY_NEW_TASK))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Opening accessibility settings（代码日志文案）；系统页展示服务项：Accessibility Button Launcher / Launches your selected app from the accessibility button or shortcut.",
      "shown_text_zh": "打开无障碍设置；系统列表项显示服务名与描述“通过无障碍按钮或快捷方式启动你选择的应用”。",
      "user_action_requested": "用户在系统列表中手动找到并开启该服务（无任何自动化代点）",
      "code_anchor": "p1.a() case 3 / case 4；res/values/strings.xml accessibility_service_label / accessibility_service_description"
    },
    {
      "step": 4,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity onboarding「Pick what the button opens」→ 应用选择器（picker_title）",
      "trigger_event": "设置页返回后继续引导；选择应用或应用快捷方式",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Pick what the button opens / Choose an app, or a specific action inside an app.",
      "shown_text_zh": "选择按钮要打开的内容；选择一个应用，或应用内的某个具体操作（应用快捷方式）。",
      "user_action_requested": "选择目标应用/快捷方式（可 Back 返回，可 Skip setup）",
      "code_anchor": "res/values/strings.xml onboarding_action_*、picker_title、picker_mode_apps/picker_mode_shortcuts"
    },
    {
      "step": 5,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity onboarding「Keep it running」电池优化说明步",
      "trigger_event": "选择目标后进入；主按钮 → p1.a() case 7 打开 IGNORE_BATTERY_OPTIMIZATION_SETTINGS 列表页",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Keep it running / Some phones put background apps to sleep, which can stop the button from working. Allowing unrestricted battery use prevents that.",
      "shown_text_zh": "保持运行；部分手机让后台应用休眠，会导致按钮失效，允许不受限电池使用可避免。",
      "user_action_requested": "点击“Allow Unrestricted Battery Access”/“Open Battery Settings”进入系统电池优化页；可跳过该步",
      "code_anchor": "p1.a() case 7；res/values/strings.xml onboarding_battery_*、background_protection_request_battery_exemption"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "onboarding 完成页（You're all set）→ 首页 Shortcut ready 清单",
      "trigger_event": "完成引导或跳过引导后；ServiceCheckWorker/首页清单读取服务连接状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "You're all set / Press the accessibility button any time to open your app. You can revisit these steps from the Home screen.",
      "shown_text_zh": "全部就绪；随时按下无障碍按钮打开你的应用，可从首页重新查看这些步骤。",
      "user_action_requested": "点击“Done”结束引导",
      "code_anchor": "res/values/strings.xml onboarding_complete_*；c81#d onboarding_finish"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "通知栏 Service status 通知（Accessibility shortcut is off）+ OpenSettingsReceiver",
      "trigger_event": "服务被关闭（如应用更新后）→ 发通知；用户点击通知动作“Open Settings” → OpenSettingsReceiver.onReceive 取消通知并跳 ACCESSIBILITY_SETTINGS",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Accessibility shortcut is off / The accessibility service was disabled. This can happen after an app update. Tap Open Settings to re-enable it. / Open Settings / Don't remind me",
      "shown_text_zh": "无障碍快捷方式已关闭；服务被停用，可能是应用更新导致，点“打开设置”重新启用。/ 打开设置 / 别再提醒我",
      "user_action_requested": "用户可选“Open Settings”重新启用，或“Don't remind me”永久不再提醒（OptOutReceiver）；非强制、不循环",
      "code_anchor": "com.pedronveloso.a11ybutton.receiver.OpenSettingsReceiver.onReceive；com.pedronveloso.a11ybutton.receiver.OptOutReceiver；notification_service_disabled_*、notification_action_opt_out"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内 Compose 引导页（onboarding 多步：欢迎/开启服务/选择目标/电池说明/完成），非系统 Dialog 也非 WebView",
    "首页 Home 清单与披露卡：main_disclosure_title / main_disclosure_body（“Why Accessibility access is required”）",
    "首页行动按钮 main_action_open_settings（“Open Accessibility Settings”）",
    "系统无障碍服务列表项：android:label=“Accessibility Button Launcher”、android:description=“Launches your selected app from the accessibility button or shortcut.”",
    "通知栏 Service status 频道通知（notification_service_disabled_title/body + Open Settings / Don't remind me 两个动作）",
    "Service Help 页（AccessibilityServiceSettingsActivity）：service_settings_body 说明“Open the App / Open App Info”排障入口",
    "FAQ 页：faq_question_button / main_troubleshooting_button 等问答文本",
    "跳过确认弹窗：onboarding_skip_confirmation_title/body（Skip setup? / Skip for now / Continue setup）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "The service listens for the system Accessibility trigger and launches only the app you select. It does not add automation or overlays.",
      "text_zh": "该服务仅监听系统无障碍触发事件并启动你所选择的应用，不添加自动化或悬浮层。",
      "source_location": "res/values/strings.xml key=main_disclosure_body",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Android needs you to switch it on in Accessibility settings. Look for \"Accessibility Button Launcher\" and turn it on. On some phones, like Samsung, you'll need to tap \"Installed apps\" first to find it.",
      "text_zh": "Android 需要你在无障碍设置中手动开启它。找到“Accessibility Button Launcher”并打开；部分机型（如三星）需先点“已安装的应用”。",
      "source_location": "res/values/strings.xml key=onboarding_service_body",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Launches your selected app from the accessibility button or shortcut.",
      "text_zh": "通过无障碍按钮或快捷方式启动你选择的应用。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（Manifest service android:description）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "You can finish setting up later from the Home screen. It's easier to follow these steps now, especially the first time.",
      "text_zh": "你可以稍后在首页完成设置；现在按步骤做会更简单，尤其是第一次使用。",
      "source_location": "res/values/strings.xml key=onboarding_skip_confirmation_body",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Some phones put background apps to sleep, which can stop the button from working. Allowing unrestricted battery use prevents that.",
      "text_zh": "部分手机让后台应用休眠，会导致按钮失效；允许不受限电池使用可避免此问题。",
      "source_location": "res/values/strings.xml key=onboarding_battery_body",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The accessibility service was disabled. This can happen after an app update. Tap Open Settings to re-enable it.",
      "text_zh": "无障碍服务已被停用，可能是应用更新所致；点“打开设置”重新启用。",
      "source_location": "res/values/strings.xml key=notification_service_disabled_body",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性降级：从系统设置返回后停留在首页/引导页并显示 Setup needed 状态，不自动重跳；用户可点“Skip setup”并在二次确认中选择“Skip for now”退出引导；服务被系统关闭时只发一次可关闭的通知，并提供“Don't remind me”（OptOutReceiver）永久停止提醒，无 Timer 拉起、无 onResume 死循环。",
    "overlay_or_fake_settings": "无；不使用悬浮窗/半透明遮罩，也不伪造系统无障碍开关页，跳转的是真实 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无；未出现“应用详情→右上角菜单→允许受限设置”的分步教学，也未使用 Session 安装器绕过。",
    "post_grant_anti_removal": "无；获权后仅注册 AccessibilityButtonController 回调并在点击时 startActivity 拉起用户选定目标；未自点确认、未监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权，onAccessibilityEvent 为空实现。",
    "benign_graceful_degradation": "提供 Skip setup（含 Skip for now 二次确认）稍后从首页继续；FAQ 与 Service Help 页提供手动排障（Open the App / Open App Info）；服务未启用或目标不可用时回跳 MainActivity 显示 Last trigger result 并给出重新选择提示，功能明确不可用时降级提示而非反复索取权限。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 MainActivity 出现 onboarding 欢迎步（“One button, one app”/“Accept and continue”）时即拉起 UTG 抓页；其次在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（p1.a case 3/4 或 OpenSettingsReceiver）前 500ms 抓取上一页；再次在系统无障碍列表中定位服务项文本时抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页",
        "page_identifier": "MainActivity Compose onboarding：标题“One button, one app”与按钮“Accept and continue”“Skip setup”",
        "why_most_useful": "决定是否存在强制/不可取消引导，以及引导文案是否如实说明用途",
        "observable_utg_signals": ["是否存在可见的 Skip setup 按钮", "文案是否提及“launches only the app you select”", "是否出现故障恐吓/假更新/安全反诈类词汇"]
      },
      {
        "page_role": "跳转前“Turn on the service”教学页",
        "page_identifier": "标题“Turn on the service”、正文含“Accessibility Button Launcher”“Installed apps”、步骤计数“Step X of Y”",
        "why_most_useful": "区分正常指路（告知真实服务名）与伪造系统页/教唆忽略警告",
        "observable_utg_signals": ["是否指名真实服务标签", "是否要求关闭安全防护或忽略系统警告", "主按钮文本是否为 Open Accessibility Settings"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中条目“Accessibility Button Launcher”，副标题“Launches your selected app from the accessibility button or shortcut.”",
        "why_most_useful": "核对系统侧展示名/描述与应用内宣称是否一致，验证无身份混淆",
        "observable_utg_signals": ["服务名与包显示名是否一致", "描述是否与实际能力（仅启动选定应用）一致", "是否存在多个同名/近名服务项"]
      },
      {
        "page_role": "拒权返回后首页/通知",
        "page_identifier": "首页“Setup needed”状态与通知栏“Accessibility shortcut is off”通知（含 Open Settings / Don't remind me）",
        "why_most_useful": "判定是否存在拒权重跳循环或强制催促",
        "observable_utg_signals": ["返回后是否再次自动弹设置页", "通知是否可关闭且含 Don't remind me", "是否存在定时重复通知"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导全为原生 Compose 文本，UTG 可直接提取；注意本应用为 R8 混淆（类名 c81/p1 等短名），静态定位需借助 strings 资源锚定；电池优化权限虽已声明但仅打开系统电池优化列表页而非直接请求豁免弹窗，勿误判为绕过系统授权。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.pedronveloso.a11ybutton.MainActivity.onCreate / MainActivity.i",
    "p1.a()（case 3/4 → android.settings.ACCESSIBILITY_SETTINGS；case 1 → APPLICATION_DETAILS_SETTINGS；case 7 → IGNORE_BATTERY_OPTIMIZATION_SETTINGS）",
    "com.pedronveloso.a11ybutton.receiver.OpenSettingsReceiver.onReceive",
    "com.pedronveloso.a11ybutton.service.ShortcutLaunchAccessibilityService.onServiceConnected / onAccessibilityEvent / b",
    "res/values/strings.xml（onboarding_service_body、main_disclosure_body、accessibility_service_description、notification_service_disabled_body）"
  ]
}
```

</details>
