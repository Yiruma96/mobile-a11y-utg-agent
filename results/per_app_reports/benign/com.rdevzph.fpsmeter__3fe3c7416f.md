# BN_019__3fe3c7416f｜显示调节、截屏与分屏效率 — FPS Meter

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：146.8s

## 1. 一句话核心结论

- **核心申请方式**：用户在设置页主动点击开关时才出现原生 Compose 卡片与可关闭弹窗，用真实用途说明并跳系统无障碍设置页，另提供 Shizuku 代开启替代路径，全程无遮罩、无伪造、无循环逼迫。
- **静态可见性说明**：无障碍申请全链路均为本地静态可见：MainActivity(Compose) 状态刷新 -> FpsViewModel.e() 授权检测 -> strings.xml 原生文案 -> tw.a()/wc.a() 原生 Intent 跳 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS。无加壳、无加密载荷、无远端 HTML/WebView 承载文案。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3fe3c7416ffa46642f52f3ab8399dce257cc8722f227211ac6028959b3c68777` |
| 包名 / 年份 | `com.rdevzph.fpsmeter` / 2025-2026 |
| 家族 / 品类 | **显示调节、截屏与分屏效率**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.rdevzph.fpsmeter_28.apk |
| 桌面显示名 | FPS Meter |
| 引导页宣称品牌/身份 | FPS Meter（rdevz-ph 开源项目，Gaming Performance Monitor） |
| 系统无障碍列表服务名 | FPS Meter（@string/app_name，与桌面图标一致） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未设置 android:isAccessibilityTool，未使用多 activity-alias 变脸，未用空白/换行/同形字挤掉系统警告文案，description 与真实用途一致。 |
| 无障碍服务类名 | `com.rdevzph.fpsmeter.accessibility.FpsAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Automatically activates or deactivates the FPS overlay when designated apps and games are launched or closed. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.rdevzph.fpsmeter.MainActivity（Compose 主界面） | onCreate 初始化通知渠道与 ViewModel；onResume 调用 FpsViewModel.i()/e()/f() 刷新权限状态 | 原生Activity | **原文**：无（冷启动不弹任何无障碍引导）<br>**译注**：冷启动直接进入主界面，不强制弹窗 | 无强制操作 | `com.rdevzph.fpsmeter.MainActivity.onCreate / onResume` |
| 2 | 业务功能触发 | 主界面自动启动/游戏监测设置区（Compose 卡片） | 用户打开“启动时/按应用自动显示 FPS 悬浮窗”相关开关或进入设置区时读取授权态 | 原生Activity | **原文**：Accessibility Service Required / Enable FPS Meter in Accessibility so it can detect foreground games.<br>**译注**：需要无障碍服务 / 请在无障碍设置中启用 FPS Meter，以便检测前台游戏。 | 阅读说明后点击卡片按钮进入系统无障碍设置；可忽略不点，功能降级为手动悬浮窗 | `com.rdevzph.fpsmeter.viewmodel.FpsViewModel.e() + res/values/strings.xml#accessibility_required(_desc)` |
| 3 | 跳无障碍设置 | 系统设置：设置 > 无障碍 > 已下载的服务（FPS Meter） | 点击卡片“Enable / Open settings”按钮（Compose onClick -> tw.a() 默认分支） | 系统无障碍页 | **原文**：Automatically activates or deactivates the FPS overlay when designated apps and games are launched or closed.<br>**译注**：当指定应用和游戏启动或关闭时，自动开启或关闭 FPS 悬浮窗。 | 用户在系统页手动打开 FPS Meter 开关（Android 13+ 需确认“允许受限设置”）；可直接返回取消 | `tw.a() -> new Intent("android.settings.ACCESSIBILITY_SETTINGS")；res/xml/accessibility_service_config.xml android:description` |
| 4 | 拒权反馈循环 | 回到 MainActivity，onResume 重新检测授权态 | 从系统设置返回时 onResume -> FpsViewModel.i() -> e(context) | 原生Activity | 无 | 无强制操作，用户可继续使用手动悬浮窗 | `com.rdevzph.fpsmeter.MainActivity.onResume -> FpsViewModel.e()` |
| 5 | 跳受限设置 | 系统设置：应用详情页（com.rdevzph.fpsmeter） | 用户点击“App Info / Force Stop & Reset”类按钮，tw.a() case 3/4 置标记后 startActivity | 原生Activity + 系统设置页 | **原文**：App Info / Force Stop & Reset<br>**译注**：应用信息 / 强制停止并重置 | 按说明在应用详情页强制停止或允许受限设置后返回重新开启，属公开的排障引导 | `tw.a() case 3/4 -> android.settings.APPLICATION_DETAILS_SETTINGS；strings#accessibility_app_info / accessibility_force_stop_shizuku` |
| 6 | 引导说明页 | 原生 AlertDialog：Accessibility Service Stopped | 检测到服务曾在设置中开启但进程被系统杀死（e() 返回 false 且 Secure 表内含本组件）后由界面状态触发 | 原生Dialog | **原文**：Android stopped the FPS Meter accessibility service. To fix this, we need to re-enable the accessibility service under settings. If auto-start overlay still does not work after re-enabling the accessibility service, force stopping the app can fix it.<br><br>Steps:<br>1. Tap "Force Stop & Reset" below (or force stop in App Info).<br>2. Re-open FPS Meter.<br>3. Tap "Via Shizuku" or "Enable" to activate it cleanly.<br>**译注**：Android 停止了 FPS Meter 无障碍服务。要修复此问题，需要在设置中重新启用无障碍服务；若重新启用后自动启动悬浮窗仍不生效，强制停止应用可修复。步骤：1. 点击下方“强制停止并重置”（或在应用信息中强制停止）；2. 重新打开 FPS Meter；3. 点击“Via Shizuku”或“Enable”干净地重新激活。 | 按步骤操作，可关闭对话框；属故障说明而非恐吓式诱导 | `res/values/strings.xml#accessibility_malfunctioning_title / _dialog_msg` |
| 7 | 获权后动作 | FpsAccessibilityService + FpsOverlayService（specialUse 前台服务） | onServiceConnected 置 isServiceRunning=true；onAccessibilityEvent(typeWindowStateChanged/typeWindowsChanged) 解析前台包名 | 原生Activity | 无 | 无；获权后不自动点击确认、不监听设置页阻止撤权 | `com.rdevzph.fpsmeter.accessibility.FpsAccessibilityService.onAccessibilityEvent / onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity（Compose）主界面设置区的“Accessibility Service Required”卡片文本：res/values/strings.xml accessibility_required / accessibility_required_desc
- 主界面可关闭的原生 AlertDialog：“Accessibility Service Stopped” + 三步排障说明（accessibility_malfunctioning_title / _dialog_msg），含 Force Stop & Reset 按钮
- 系统无障碍服务列表项：res/xml/accessibility_service_config.xml 的 android:description -> @string/accessibility_service_desc（Automatically activates or deactivates the FPS overlay…）
- Toast/Snackbar 类结果反馈：accessibility_enable_success / accessibility_enable_failed / accessibility_restart_success / accessibility_restart_failed / accessibility_starting / accessibility_restarting
- 无 WebView / assets HTML / 悬浮遮罩 / 高仿系统设置页承载任何引导文案（assets 目录内无引导页面，代码中亦无 ACCESSIBILITY_SETTINGS 相关 WebView 载入）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility Service Required | 需要无障碍服务 | `res/values/strings.xml accessibility_required` | 良性透明说明 |
| en | Enable FPS Meter in Accessibility so it can detect foreground games. | 请在无障碍设置中启用 FPS Meter，以便检测前台游戏。 | `res/values/strings.xml accessibility_required_desc` | 良性透明说明 |
| en | Automatically activates or deactivates the FPS overlay when designated apps and games are launched or closed. | 当指定应用和游戏启动或关闭时，自动开启或关闭 FPS 悬浮窗。 | `res/values/strings.xml accessibility_service_desc（系统无障碍列表 description）` | 良性透明说明 |
| en | Accessibility Service Stopped | 无障碍服务已停止 | `res/values/strings.xml accessibility_malfunctioning_title` | 良性透明说明 |
| en | Android stopped the FPS Meter accessibility service. To fix this, we need to re-enable the accessibility service under settings. If auto-start overlay still does not work after re-enabling the accessibility service, force stopping the app can fix it.<br><br>Steps:<br>1. Tap "Force Stop & Reset" below (or force stop in App Info).<br>2. Re-open FPS Meter.<br>3. Tap "Via Shizuku" or "Enable" to activate it cleanly. | Android 停止了 FPS Meter 的无障碍服务。要修复此问题，需要在设置中重新启用无障碍服务；若重新启用后自动启动悬浮窗仍不生效，强制停止应用可修复。步骤：1. 点击下方“强制停止并重置”（或在应用信息中强制停止）；2. 重新打开 FPS Meter；3. 点击“Via Shizuku”或“Enable”干净地重新激活。 | `res/values/strings.xml accessibility_malfunctioning_dialog_msg` | 良性透明说明 |
| en | Force Stop & Reset | 强制停止并重置 | `res/values/strings.xml accessibility_force_stop_shizuku` | 良性透明说明 |
| en | Accessibility service enabled successfully / Failed to start accessibility service via Shizuku | 无障碍服务启用成功 / 通过 Shizuku 启动无障碍服务失败 | `res/values/strings.xml accessibility_enable_success / accessibility_enable_failed` | 良性透明说明 |
| en | Free and open source. No advertisements, no telemetry, and no network tracking. | 免费开源。无广告、无遥测、无网络追踪。 | `res/values/strings.xml about_feature7_desc` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。从系统设置返回仅触发 MainActivity.onResume -> FpsViewModel.e() 刷新授权态；未获权则卡片保持提示，用户可继续使用手动悬浮窗，不重复拉起设置页、无定时器强制重跳。
- **遮罩叠层 / 高仿系统设置页**：无。无半透明引导遮罩、无全屏悬浮窗指引、无高仿系统无障碍开关页；唯一的悬浮窗为 FpsOverlayService 的 FPS 数据展示层，与授权引导无关。
- **Android 13+ 受限设置（Restricted Settings）应对**：存在轻度引导但为公开排障性质：tw.a() case 3/4 置标记后跳 android.settings.APPLICATION_DETAILS_SETTINGS 应用详情页，配合“Force Stop & Reset / App Info”文案让用户自行强制停止或处理受限设置；未教用户点右上角菜单“允许受限设置”的成段图文教学，未使用 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。获权后不自点确认、不自动授予其他权限，未使用 GLOBAL_ACTION_BACK/HOME 或监听设置页阻止撤权；仅在服务被系统杀死后弹出说明性对话框。
- **良性降级 / 替代方案**：有。无障碍仅用于“按应用自动启停悬浮窗”；未授权时仍可通过主界面手动启动 FPS 悬浮窗（FpsOverlayService + SYSTEM_ALERT_WINDOW 授权），并提供 Shizuku（moe.shizuku.api.permission.SHIZUKU）代开启路径作为替代。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在检测到 startActivity("android.settings.ACCESSIBILITY_SETTINGS") 或 startActivity("android.settings.APPLICATION_DETAILS_SETTINGS") 时拉起 UTG，并同时截取跳转前的当前 Activity（MainActivity Compose 界面）与返回后的界面，用于确认是否存在遮罩或循环重跳。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区：无纯图空文本引导页、无 WebView 承载说明、无加壳/加密载荷。注意本应用存在 Shizuku 代开启路径，若检测逻辑把“程序化开启无障碍”一律视为恶意会误判；该路径在 UI 上明示为 Via Shizuku 替代方式，且需用户安装并授权 Shizuku。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前说明页（主界面无障碍提示卡片）** | com.rdevzph.fpsmeter.MainActivity，含文本 Accessibility Service Required 与 Enable/App Info 按钮 | 确认文案是否仅为真实用途说明、是否伴随取消/跳过选项，是区分良性说明与恐吓诱导的核心页面 | 文本节点 Accessibility Service Required；按钮文本 Enable / Open settings / App Info；是否存在无法关闭的全屏遮罩节点 |
| **系统无障碍服务列表项** | com.android.settings 无障碍列表中的 FPS Meter 条目 | 核对系统侧展示的服务名与描述是否与应用真实身份一致，排除同形字/空白挤出警告 | 条目标题 FPS Meter；摘要文本 Automatically activates or deactivates the FPS overlay…；是否存在截断或异常空白字符 |
| **故障说明弹窗页** | 原生 AlertDialog 标题 Accessibility Service Stopped | 确认弹窗是否可取消、按钮是否为 Force Stop & Reset 与关闭，判断是否构成逼迫式循环 | 对话框标题与步骤文本；按钮集合（Force Stop & Reset / 取消）；是否存在遮罩层阻挡返回键 |
| **返回应用后的状态页** | 从系统设置返回后的 MainActivity | 验证拒权后是否再次自动拉起设置页（循环重跳） | 短时间内是否重复出现 settings 包名页面；无障碍卡片是否保持提示态而非阻塞主界面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.rdevzph.fpsmeter.viewmodel.FpsViewModel.e`
- `tw.a`
- `wc.a`
- `com.rdevzph.fpsmeter.accessibility.FpsAccessibilityService.onAccessibilityEvent`
- `res/values/strings.xml#L20-L39`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**未发现诱导或欺骗式无障碍权限获取；这是 F-Droid 开源应用的良性透明说明流程。**

- **触发时机：按需触发**。`MainActivity.onCreate/onResume` 只是刷新状态，没有冷启动强制弹窗、没有遮罩，也没有循环拉起。[FpsViewModel.e()](<resource-unit:#1.dex1 code:com.rdevzph.fpsmeter.viewmodel.FpsViewModel#e>) 用 `AccessibilityManager.getEnabledAccessibilityServiceList()` 和 `Settings.Secure.enabled_accessibility_services` 判定是否已授权，然后把结果写入两个 StateFlow（“已开启且运行中”和“已在设置中开启但服务未运行”）。
- **载体：原生 Compose 卡片和原生 AlertDialog**，文案直接来自 [res/values/strings.xml (lines 33-34)](<resource-unit:#1 file:res/values/strings.xml#L33-L34>)：“Accessibility Service Required” / “Enable FPS Meter in Accessibility so it can detect foreground games.”，只陈述用途。没有 WebView、没有本地或远端 HTML，也没有悬浮引导层。
- **跳转点**：[tw.a()](<resource-unit:#1.dex1 code:tw#a>) 默认分支 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`；[wc.a()](<resource-unit:#1.dex1 code:wc#a>) case 3 也同样跳到该设置页。这些都是用户点击“Enable/Open settings”后才发起。
- **另有一条 Shizuku 代开启路径**（`moe.shizuku.api.permission.SHIZUKU` + `ShizukuProvider`），文案 “Accessibility service enabled successfully / Failed to start accessibility service via Shizuku” 只是操作结果反馈，属于明确告知的替代路径，不是绕过用户确认的隐蔽手段。
- **Android 13+ 受限设置**：`tw.a()` 的 case 3/4 先把一个布尔标记置为 TRUE，然后跳到 `APPLICATION_DETAILS_SETTINGS`；结合 `accessibility_force_stop_shizuku`(“Force Stop & Reset”) 和故障弹窗中的三步说明，这属于公开的“去应用详情页处理/重置”引导，而不是伪造系统页。
- **拒权反馈**：返回后只重新执行 `e(context)` 刷新状态，不会循环重跳；弹窗可以关闭，设置页可以返回，属于良性降级。
- **服务能力最小化且诚实**：[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 中 `canRetrieveWindowContent="false"`，只订阅 `typeWindowStateChanged|typeWindowsChanged`；[FpsAccessibilityService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.rdevzph.fpsmeter.accessibility.FpsAccessibilityService#onAccessibilityEvent>) 只解析前台包名，再与用户配置的“自动启动/录制”列表比对，然后启停 `FpsOverlayService`。没有读取文本、没有注入点击，也没有隐藏开关。
- **身份一致**：显示名 `FPS Meter`、无障碍列表标签来自 `@string/app_name`，`android:description` 就是真实用途说明；未发现 `isAccessibilityTool` 伪造、activity-alias 变脸，也没有用空白或同形字挤出警告。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请全链路均为本地静态可见：MainActivity(Compose) 状态刷新 -> FpsViewModel.e() 授权检测 -> strings.xml 原生文案 -> tw.a()/wc.a() 原生 Intent 跳 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS。无加壳、无加密载荷、无远端 HTML/WebView 承载文案。",
  "summary_one_liner": "用户在设置页主动点击开关时才出现原生 Compose 卡片与可关闭弹窗，用真实用途说明并跳系统无障碍设置页，另提供 Shizuku 代开启替代路径，全程无遮罩、无伪造、无循环逼迫。",
  "disguise_identity": {
    "app_display_name": "FPS Meter",
    "claimed_brand_or_persona": "FPS Meter（rdevz-ph 开源项目，Gaming Performance Monitor）",
    "a11y_service_label": "FPS Meter（@string/app_name，与桌面图标一致）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未设置 android:isAccessibilityTool，未使用多 activity-alias 变脸，未用空白/换行/同形字挤掉系统警告文案，description 与真实用途一致。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.rdevzph.fpsmeter.MainActivity（Compose 主界面）",
      "trigger_event": "onCreate 初始化通知渠道与 ViewModel；onResume 调用 FpsViewModel.i()/e()/f() 刷新权限状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（冷启动不弹任何无障碍引导）",
      "shown_text_zh": "冷启动直接进入主界面，不强制弹窗",
      "user_action_requested": "无强制操作",
      "code_anchor": "com.rdevzph.fpsmeter.MainActivity.onCreate / onResume"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "主界面自动启动/游戏监测设置区（Compose 卡片）",
      "trigger_event": "用户打开“启动时/按应用自动显示 FPS 悬浮窗”相关开关或进入设置区时读取授权态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility Service Required / Enable FPS Meter in Accessibility so it can detect foreground games.",
      "shown_text_zh": "需要无障碍服务 / 请在无障碍设置中启用 FPS Meter，以便检测前台游戏。",
      "user_action_requested": "阅读说明后点击卡片按钮进入系统无障碍设置；可忽略不点，功能降级为手动悬浮窗",
      "code_anchor": "com.rdevzph.fpsmeter.viewmodel.FpsViewModel.e() + res/values/strings.xml#accessibility_required(_desc)"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置：设置 > 无障碍 > 已下载的服务（FPS Meter）",
      "trigger_event": "点击卡片“Enable / Open settings”按钮（Compose onClick -> tw.a() 默认分支）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Automatically activates or deactivates the FPS overlay when designated apps and games are launched or closed.",
      "shown_text_zh": "当指定应用和游戏启动或关闭时，自动开启或关闭 FPS 悬浮窗。",
      "user_action_requested": "用户在系统页手动打开 FPS Meter 开关（Android 13+ 需确认“允许受限设置”）；可直接返回取消",
      "code_anchor": "tw.a() -> new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")；res/xml/accessibility_service_config.xml android:description"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "回到 MainActivity，onResume 重新检测授权态",
      "trigger_event": "从系统设置返回时 onResume -> FpsViewModel.i() -> e(context)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅刷新卡片状态，不重复拉起设置页、不弹二次逼迫弹窗",
      "user_action_requested": "无强制操作，用户可继续使用手动悬浮窗",
      "code_anchor": "com.rdevzph.fpsmeter.MainActivity.onResume -> FpsViewModel.e()"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置：应用详情页（com.rdevzph.fpsmeter）",
      "trigger_event": "用户点击“App Info / Force Stop & Reset”类按钮，tw.a() case 3/4 置标记后 startActivity",
      "ui_carrier": "原生Activity + 系统设置页",
      "shown_text_verbatim": "App Info / Force Stop & Reset",
      "shown_text_zh": "应用信息 / 强制停止并重置",
      "user_action_requested": "按说明在应用详情页强制停止或允许受限设置后返回重新开启，属公开的排障引导",
      "code_anchor": "tw.a() case 3/4 -> android.settings.APPLICATION_DETAILS_SETTINGS；strings#accessibility_app_info / accessibility_force_stop_shizuku"
    },
    {
      "step": 6,
      "stage": "引导说明页",
      "screen_or_component": "原生 AlertDialog：Accessibility Service Stopped",
      "trigger_event": "检测到服务曾在设置中开启但进程被系统杀死（e() 返回 false 且 Secure 表内含本组件）后由界面状态触发",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Android stopped the FPS Meter accessibility service. To fix this, we need to re-enable the accessibility service under settings. If auto-start overlay still does not work after re-enabling the accessibility service, force stopping the app can fix it.\n\nSteps:\n1. Tap \"Force Stop & Reset\" below (or force stop in App Info).\n2. Re-open FPS Meter.\n3. Tap \"Via Shizuku\" or \"Enable\" to activate it cleanly.",
      "shown_text_zh": "Android 停止了 FPS Meter 无障碍服务。要修复此问题，需要在设置中重新启用无障碍服务；若重新启用后自动启动悬浮窗仍不生效，强制停止应用可修复。步骤：1. 点击下方“强制停止并重置”（或在应用信息中强制停止）；2. 重新打开 FPS Meter；3. 点击“Via Shizuku”或“Enable”干净地重新激活。",
      "user_action_requested": "按步骤操作，可关闭对话框；属故障说明而非恐吓式诱导",
      "code_anchor": "res/values/strings.xml#accessibility_malfunctioning_title / _dialog_msg"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "FpsAccessibilityService + FpsOverlayService（specialUse 前台服务）",
      "trigger_event": "onServiceConnected 置 isServiceRunning=true；onAccessibilityEvent(typeWindowStateChanged/typeWindowsChanged) 解析前台包名",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅当前台包命中用户自选列表时自动启停 FPS 悬浮窗；canRetrieveWindowContent=false，不读取界面文本",
      "user_action_requested": "无；获权后不自动点击确认、不监听设置页阻止撤权",
      "code_anchor": "com.rdevzph.fpsmeter.accessibility.FpsAccessibilityService.onAccessibilityEvent / onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "MainActivity（Compose）主界面设置区的“Accessibility Service Required”卡片文本：res/values/strings.xml accessibility_required / accessibility_required_desc",
    "主界面可关闭的原生 AlertDialog：“Accessibility Service Stopped” + 三步排障说明（accessibility_malfunctioning_title / _dialog_msg），含 Force Stop & Reset 按钮",
    "系统无障碍服务列表项：res/xml/accessibility_service_config.xml 的 android:description -> @string/accessibility_service_desc（Automatically activates or deactivates the FPS overlay…）",
    "Toast/Snackbar 类结果反馈：accessibility_enable_success / accessibility_enable_failed / accessibility_restart_success / accessibility_restart_failed / accessibility_starting / accessibility_restarting",
    "无 WebView / assets HTML / 悬浮遮罩 / 高仿系统设置页承载任何引导文案（assets 目录内无引导页面，代码中亦无 ACCESSIBILITY_SETTINGS 相关 WebView 载入）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service Required",
      "text_zh": "需要无障碍服务",
      "source_location": "res/values/strings.xml accessibility_required",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable FPS Meter in Accessibility so it can detect foreground games.",
      "text_zh": "请在无障碍设置中启用 FPS Meter，以便检测前台游戏。",
      "source_location": "res/values/strings.xml accessibility_required_desc",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Automatically activates or deactivates the FPS overlay when designated apps and games are launched or closed.",
      "text_zh": "当指定应用和游戏启动或关闭时，自动开启或关闭 FPS 悬浮窗。",
      "source_location": "res/values/strings.xml accessibility_service_desc（系统无障碍列表 description）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service Stopped",
      "text_zh": "无障碍服务已停止",
      "source_location": "res/values/strings.xml accessibility_malfunctioning_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Android stopped the FPS Meter accessibility service. To fix this, we need to re-enable the accessibility service under settings. If auto-start overlay still does not work after re-enabling the accessibility service, force stopping the app can fix it.\n\nSteps:\n1. Tap \"Force Stop & Reset\" below (or force stop in App Info).\n2. Re-open FPS Meter.\n3. Tap \"Via Shizuku\" or \"Enable\" to activate it cleanly.",
      "text_zh": "Android 停止了 FPS Meter 的无障碍服务。要修复此问题，需要在设置中重新启用无障碍服务；若重新启用后自动启动悬浮窗仍不生效，强制停止应用可修复。步骤：1. 点击下方“强制停止并重置”（或在应用信息中强制停止）；2. 重新打开 FPS Meter；3. 点击“Via Shizuku”或“Enable”干净地重新激活。",
      "source_location": "res/values/strings.xml accessibility_malfunctioning_dialog_msg",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Force Stop & Reset",
      "text_zh": "强制停止并重置",
      "source_location": "res/values/strings.xml accessibility_force_stop_shizuku",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service enabled successfully / Failed to start accessibility service via Shizuku",
      "text_zh": "无障碍服务启用成功 / 通过 Shizuku 启动无障碍服务失败",
      "source_location": "res/values/strings.xml accessibility_enable_success / accessibility_enable_failed",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Free and open source. No advertisements, no telemetry, and no network tracking.",
      "text_zh": "免费开源。无广告、无遥测、无网络追踪。",
      "source_location": "res/values/strings.xml about_feature7_desc",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。从系统设置返回仅触发 MainActivity.onResume -> FpsViewModel.e() 刷新授权态；未获权则卡片保持提示，用户可继续使用手动悬浮窗，不重复拉起设置页、无定时器强制重跳。",
    "overlay_or_fake_settings": "无。无半透明引导遮罩、无全屏悬浮窗指引、无高仿系统无障碍开关页；唯一的悬浮窗为 FpsOverlayService 的 FPS 数据展示层，与授权引导无关。",
    "restricted_settings_13plus_coaching": "存在轻度引导但为公开排障性质：tw.a() case 3/4 置标记后跳 android.settings.APPLICATION_DETAILS_SETTINGS 应用详情页，配合“Force Stop & Reset / App Info”文案让用户自行强制停止或处理受限设置；未教用户点右上角菜单“允许受限设置”的成段图文教学，未使用 Session 安装器绕过。",
    "post_grant_anti_removal": "无。获权后不自点确认、不自动授予其他权限，未使用 GLOBAL_ACTION_BACK/HOME 或监听设置页阻止撤权；仅在服务被系统杀死后弹出说明性对话框。",
    "benign_graceful_degradation": "有。无障碍仅用于“按应用自动启停悬浮窗”；未授权时仍可通过主界面手动启动 FPS 悬浮窗（FpsOverlayService + SYSTEM_ALERT_WINDOW 授权），并提供 Shizuku（moe.shizuku.api.permission.SHIZUKU）代开启路径作为替代。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在检测到 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\") 或 startActivity(\"android.settings.APPLICATION_DETAILS_SETTINGS\") 时拉起 UTG，并同时截取跳转前的当前 Activity（MainActivity Compose 界面）与返回后的界面，用于确认是否存在遮罩或循环重跳。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前说明页（主界面无障碍提示卡片）",
        "page_identifier": "com.rdevzph.fpsmeter.MainActivity，含文本 Accessibility Service Required 与 Enable/App Info 按钮",
        "why_most_useful": "确认文案是否仅为真实用途说明、是否伴随取消/跳过选项，是区分良性说明与恐吓诱导的核心页面",
        "observable_utg_signals": ["文本节点 Accessibility Service Required", "按钮文本 Enable / Open settings / App Info", "是否存在无法关闭的全屏遮罩节点"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍列表中的 FPS Meter 条目",
        "why_most_useful": "核对系统侧展示的服务名与描述是否与应用真实身份一致，排除同形字/空白挤出警告",
        "observable_utg_signals": ["条目标题 FPS Meter", "摘要文本 Automatically activates or deactivates the FPS overlay…", "是否存在截断或异常空白字符"]
      },
      {
        "page_role": "故障说明弹窗页",
        "page_identifier": "原生 AlertDialog 标题 Accessibility Service Stopped",
        "why_most_useful": "确认弹窗是否可取消、按钮是否为 Force Stop & Reset 与关闭，判断是否构成逼迫式循环",
        "observable_utg_signals": ["对话框标题与步骤文本", "按钮集合（Force Stop & Reset / 取消）", "是否存在遮罩层阻挡返回键"]
      },
      {
        "page_role": "返回应用后的状态页",
        "page_identifier": "从系统设置返回后的 MainActivity",
        "why_most_useful": "验证拒权后是否再次自动拉起设置页（循环重跳）",
        "observable_utg_signals": ["短时间内是否重复出现 settings 包名页面", "无障碍卡片是否保持提示态而非阻塞主界面"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区：无纯图空文本引导页、无 WebView 承载说明、无加壳/加密载荷。注意本应用存在 Shizuku 代开启路径，若检测逻辑把“程序化开启无障碍”一律视为恶意会误判；该路径在 UI 上明示为 Via Shizuku 替代方式，且需用户安装并授权 Shizuku。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.rdevzph.fpsmeter.viewmodel.FpsViewModel.e",
    "tw.a",
    "wc.a",
    "com.rdevzph.fpsmeter.accessibility.FpsAccessibilityService.onAccessibilityEvent",
    "res/values/strings.xml#L20-L39",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
