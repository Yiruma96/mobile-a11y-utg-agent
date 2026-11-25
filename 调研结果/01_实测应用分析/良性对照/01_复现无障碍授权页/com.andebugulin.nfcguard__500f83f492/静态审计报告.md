# BN_002__500f83f492｜专注自律与防沉迷管控 — nfcGuard

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：175.8s

## 1. 一句话核心结论

- **核心申请方式**：nfcGuard 在应用内 Compose 引导页逐项列出无障碍/用量访问/悬浮窗/电池/自启动的真实授权状态，用户点 GRANT 后仅调用标准 ACTION_ACCESSIBILITY_SETTINGS 打开系统无障碍列表，文案透明说明仅读取前台包名且明确表示不开启也能用（降级为全屏黑罩），无强制、无循环、无遮罩伪造。
- **静态可见性说明**：全流程静态可见：无障碍服务配置、服务实现、权限状态检测（U1.h.*）、引导页 composable（e2.q.b）与跳转实现（e2.m.c）均可静态还原；引导界面由 Jetpack Compose 运行时构建，反编译部分退化为指令流，但全部文案来自本地 res/values/strings.xml，未发现远端 HTML/WebView 或加密载荷承载引导文案。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `500f83f492ef46a28334fba815b31179b7ea8a4de040b6d68bef8a42783b69bb` |
| 包名 / 年份 | `com.andebugulin.nfcguard` / 2025-2026 |
| 家族 / 品类 | **专注自律与防沉迷管控**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.andebugulin.nfcguard_25.apk |
| 桌面显示名 | nfcGuard |
| 引导页宣称品牌/身份 | nfcGuard（F-Droid 开源 NFC 专注自律/防沉迷工具，真实身份） |
| 系统无障碍列表服务名 | 未在 AndroidManifest 中为服务声明 android:label，系统无障碍列表将回退显示应用名 nfcGuard（@string/app_name）；服务说明为 res/values/strings.xml 的 accessibility_service_description |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。虽经 R8 混淆（类名如 e2.q、U1.h），但为常规代码压缩，未使用空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool；服务声明与说明文案一致。 |
| 无障碍服务类名 | `com.andebugulin.nfcguard.service.ForegroundDetectorService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | NFCGUARD uses this to reliably detect which app is in the foreground. This is needed on some devices (like Pixel) where the standard detection method fails when returning from the recent apps screen. NFCGUARD does NOT read any screen content or user data. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.andebugulin.nfcguard.ui.MainActivity（Compose 内容，根 composable 由 Y.a(..., new F(this,1), true) 设置） | onCreate → setContent(...) 渲染主界面/引导清单 | 原生Activity | **原文**：GET STARTED / ACCESSIBILITY ACCESS / USAGE ACCESS / DISPLAY OVER APPS / BATTERY / AUTOSTART / NOTIFICATIONS<br>**译注**：开始使用；无障碍访问、用量访问、叠加显示在其他应用上层、电池、自启动、通知（权限清单标题） | 浏览权限清单，逐项决定是否授予；存在 BACK 返回与跳过式继续（未开启也可继续使用） | `com.andebugulin.nfcguard.ui.MainActivity.onCreate；res/values/strings.xml（onb_get_started、onb_accessibility_access、onb_usage_access、onb_display_over_apps、onb_battery、onb_autostart、onb_notifications、onb_back）` |
| 2 | 引导说明页 | Compose 引导 composable e2.q.b（权限状态行 + 说明文案），状态由 U1.h.a/d/e/c 实时检测 | 进入引导页时组合执行；U1.h.a 检测无障碍是否已启用、U1.h.d 检测悬浮窗、U1.h.e 检测用量访问、U1.h.c 检测电池优化白名单 | 原生Activity | **原文**：nfcGuard uses Android's Accessibility API only to see which app is in the foreground, so it can close a blocked app instantly instead of covering it.<br><br>It never reads, records, or sends screen content, typed text, or any other personal data - on this device or anywhere else.<br>**译注**：nfcGuard 仅使用 Android 无障碍 API 判断哪个应用在前台，从而能立即关闭被屏蔽的应用，而不是覆盖它。它从不读取、记录或发送屏幕内容、输入的文字或任何其他个人数据——在本机或任何其他地方。 | 阅读说明后点击该行 GRANT 按钮（已授权则显示 GRANTED）；无强制，可返回或继续其他步骤 | `e2.q.b；U1.h.a / U1.h.d / U1.h.e / U1.h.c；strings.xml: onb_nfcguard_uses_androids_accessibility_api、onb_nfcguard_needs_to_know_which、onb_lets_nfcguard_close_a_blocked、onb_grant、onb_granted` |
| 3 | 跳无障碍设置 | 系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS），由 q.d(context, intent) 启动 | 用户点击无障碍行的 GRANT 按钮 → 协程回调 e2.m.c()（case 0：setValue(FALSE) 后 startActivity 跳系统无障碍列表） | 系统无障碍页 | **原文**：NFCGUARD uses this to reliably detect which app is in the foreground. This is needed on some devices (like Pixel) where the standard detection method fails when returning from the recent apps screen. NFCGUARD does NOT read any screen content or user data.<br>**译注**：NFCGUARD 使用此权限可靠判断哪个应用位于前台。在部分设备（如 Pixel）从最近任务返回时标准检测方式失效，因此需要它。NFCGUARD 不读取任何屏幕内容或用户数据。 | 在系统列表中找到 nfcGuard 并手动打开开关（应用无法自行授权，未做任何自动点击或跳转遮挡） | `e2.m.c；res/xml/accessibility_service_config.xml（android:description=@string/accessibility_service_description）` |
| 4 | 拒权反馈循环 | 返回 MainActivity 后重新渲染引导页，U1.h.a 仍返回 false，该行保持 GRANT 状态 | 从系统设置返回（Activity 恢复）后 Compose 重组重新检测状态 | 原生Activity | **原文**：Blocking works fine without this.<br>**译注**：不开这个权限，屏蔽也照常可用。 | 可再次点击 GRANT，也可直接放弃继续使用；无死循环重跳、无定时拉起、无遮挡系统设置页 | `e2.q.b（U1.h.a 结果驱动行状态）；strings.xml: onb_blocking_works_fine_without_this` |
| 5 | 获权后动作 | ForegroundDetectorService.onServiceConnected → 恢复 BlockerService 与告警调度 | 系统绑定服务回调 onServiceConnected | 系统无障碍页 | **原文**：ForegroundDetectorService connected / Blocking restored on accessibility connect<br>**译注**：（日志）前台检测服务已连接；无障碍连接时已恢复屏蔽 | 无；仅重建 setServiceInfo(eventTypes=32, notificationTimeout=100) 并恢复屏蔽状态，未自动点击确认、未阻止撤权 | `com.andebugulin.nfcguard.service.ForegroundDetectorService.onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内 Compose 引导页（e2.q.b）逐行说明 + GRANT/GRANTED 按钮，文案取自 res/values/strings.xml 的 onb_* 键（原生 Activity，非 WebView）
- 系统无障碍服务列表项说明：res/xml/accessibility_service_config.xml 的 android:description → @string/accessibility_service_description（AccessibilityService 列表页展示）
- 应用内信息/说明页文案：info_a_full_screen_black_panel、info_closes_the_app_instantly_needs、info_u2022_enable_accessibility_for_the、home_accessibility_off_overlay_mode_active、home_accessibility_on_force_close_avoids
- 未发现 assets 内 HTML/WebView 教学页、未发现半透明引导遮罩或全屏悬浮指引窗承载引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | NFCGUARD uses this to reliably detect which app is in the foreground. This is needed on some devices (like Pixel) where the standard detection method fails when returning from the recent apps screen. NFCGUARD does NOT read any screen content or user data. | NFCGUARD 使用此权限可靠判断哪个应用位于前台。在部分设备（如 Pixel）从最近任务返回时标准检测方式失效，因此需要它。NFCGUARD 不读取任何屏幕内容或用户数据。 | `res/values/strings.xml → accessibility_service_description（系统无障碍列表展示）` | 良性透明说明 |
| en | nfcGuard uses Android's Accessibility API only to see which app is in the foreground, so it can close a blocked app instantly instead of covering it.<br><br>It never reads, records, or sends screen content, typed text, or any other personal data - on this device or anywhere else. | nfcGuard 仅使用 Android 无障碍 API 判断哪个应用在前台，从而立即关闭被屏蔽的应用而非覆盖它。它从不读取、记录或发送屏幕内容、输入文字或任何其他个人数据——本机或任何其他地方都不会。 | `res/values/strings.xml → onb_nfcguard_uses_androids_accessibility_api（引导页正文）` | 良性透明说明 |
| en | nfcGuard needs to know which app is in the foreground to block the right one. It cannot see anything inside your apps. | nfcGuard 需要知道哪个应用在前台才能屏蔽正确的应用。它看不到你应用内部的任何内容。 | `res/values/strings.xml → onb_nfcguard_needs_to_know_which` | 隐私承诺 |
| en | Lets nfcGuard close a blocked app instantly instead of covering it. nfcGuard only reads which app is in front - never screen content. | 让 nfcGuard 立即关闭被屏蔽的应用，而不是覆盖它。nfcGuard 只读取哪个应用在前台——从不读取屏幕内容。 | `res/values/strings.xml → onb_lets_nfcguard_close_a_blocked` | 良性透明说明 |
| en | Your device has a detection bug that makes blocking unreliable without this. nfcGuard only reads which app is in front - never screen content. | 你的设备存在检测缺陷，没有这个权限屏蔽会不可靠。nfcGuard 只读取哪个应用在前台——从不读取屏幕内容。 | `res/values/strings.xml → onb_your_device_has_a_detection` | 良性透明说明 |
| en | Blocking works fine without this. | 不开这个也能正常屏蔽。 | `res/values/strings.xml → onb_blocking_works_fine_without_this` | 良性透明说明 |
| en | A full-screen black panel covers the blocked app until you tap your tag. Used automatically whenever the Accessibility Service is off. | 在你刷标签之前，全屏黑色面板会覆盖被屏蔽的应用。无障碍服务关闭时自动使用此方式。 | `res/values/strings.xml → info_a_full_screen_black_panel（降级路径说明）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无死循环：从系统设置返回后仅重新检测状态并保持该行 GRANT，用户可再次点击或直接放弃；无障碍关闭时自动降级为全屏黑色遮罩屏蔽（info_a_full_screen_black_panel），功能不被阻断。
- **遮罩叠层 / 高仿系统设置页**：无。未叠放半透明引导遮罩、未使用全屏悬浮窗指引，也未渲染高仿系统无障碍开关页；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未引导进入应用详情右上角菜单开启受限设置，也未使用 Session 安装器绕过；仅使用 android.settings.APPLICATION_DETAILS_SETTINGS 作为常规应用信息页入口（Y1.G#c），且未发现教唆忽略系统警告的文案。
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅重建 ServiceInfo 并恢复屏蔽状态；未自动点击确认、未监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权（DEX 中 PERFORM_GLOBAL_ACTION/WATCH_SETTINGS 线索未落在无障碍引导链上，服务实现内无此类调用）。
- **良性降级 / 替代方案**：有。无障碍关闭时自动切换为全屏黑色面板覆盖模式（info_a_full_screen_black_panel、home_accessibility_off_overlay_mode_active）；引导页明确写有 Blocking works fine without this，另有 usage access / 电池优化 / 自启动 等非必需项均标注可选。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 指向 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（e2.m.c 分支），以及冷启动进入 MainActivity 后引导页首帧渲染时（无需任何用户操作即可出现权限清单）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。引导文案全部为本地 strings.xml 文本，无纯图空文本诱导、无远端下发文案；静态未加壳（加壳初判 False，仅 R8 混淆类名），运行期 UTG 可完整观测。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导权限清单页** | MainActivity 内 Compose 页面，含 GET STARTED / ACCESSIBILITY ACCESS / USAGE ACCESS / DISPLAY OVER APPS / BATTERY / AUTOSTART / NOTIFICATIONS 与每行 GRANT 按钮 | 该页是唯一的引导载体，可判断是否存在强制、遮罩、恐吓文案；本例应显示为逐项可选、可返回的透明清单 | 是否存在不可取消弹窗或全屏遮罩；每项是否都有 GRANT 与已授权 GRANTED 双态；是否出现假更新/故障恐吓/仿反诈等诱导措辞；是否有 BACK/跳过入口 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务中的 nfcGuard 条目及展开后的服务说明 | 核对服务说明与实现是否一致（本例说明仅检测前台应用、声明不读屏幕内容），并确认应用未使用同形字/空白挤出等伪装 | 服务名称是否为 nfcGuard 而非仿冒系统组件；说明文字是否为透明用途描述；是否存在空白/换行导致的警告挤出 |
| **返回应用后的拒权状态页** | 从系统设置返回 MainActivity 后重新渲染的引导页（该行仍为 GRANT） | 区分良性降级与拒权循环：观察是否被定时/onResume 强制重跳系统设置或叠加遮罩 | 返回后 3 秒内是否自动再次跳转设置页；是否出现悬浮遮罩覆盖界面；是否出现不可关闭的催促弹窗 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `e2.q.b（Compose 引导权限清单页，调用 U1.h.a/d/e/c 检测各项授权状态）`
- `e2.m.c（GRANT 按钮回调：startActivity android.settings.ACCESSIBILITY_SETTINGS / 电池优化设置）`
- `U1.h.a / U1.h.d / U1.h.e / U1.h.c（无障碍、悬浮窗、用量访问、电池白名单真实状态检测）`
- `com.andebugulin.nfcguard.service.ForegroundDetectorService.onAccessibilityEvent / onServiceConnected`
- `res/xml/accessibility_service_config.xml（canRetrieveWindowContent=false，仅 typeWindowStateChanged）`
- `res/values/strings.xml（accessibility_service_description、onb_*、info_a_full_screen_black_panel）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，静态可见性 clear）

**核验范围与结果：**

- **无障碍服务实现诚实、最小化**：`ForegroundDetectorService` 的配置 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml#L1-L3>) 仅注册 `typeWindowStateChanged`，并显式声明 `canRetrieveWindowContent="false"`；[ForegroundDetectorService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.andebugulin.nfcguard.service.ForegroundDetectorService#onAccessibilityEvent>) 只取 `getPackageName()`，过滤 `com.android.systemui`，用于判断前台应用并按需恢复 `BlockerService`，**不读取节点内容、不执行 GLOBAL_ACTION、不监听设置页撤权**。
- **权限引导采用 Compose 原生引导页（onboarding），不是遮罩或高仿系统页面**：`U1.h.*` 分别检测无障碍、Usage Access、悬浮窗、电池优化、通知的真实状态；[e2.q.b()](<resource-unit:#1.dex1 code:e2.q#b>) 按检测结果渲染各行 "GRANT / GRANTED" 与说明文案；点击后由 [e2.m.c()](<resource-unit:#1.dex1 code:e2.m#c>) 发起 `android.settings.ACCESSIBILITY_SETTINGS` 跳转（电池项回退到 `IGNORE_BATTERY_OPTIMIZATION_SETTINGS`），属于标准"按钮打开对应系统设置页"的做法。
- **没有强制、没有循环、没有遮罩**：没有任何不可取消的 Dialog，没有在 `onResume` 中强制重新跳转，也没有全屏悬浮引导层或伪造无障碍开关页；引导页提供 `BACK`，并明确写有 "Blocking works fine without this."（不开启也照常可用）。
- **降级路径真实存在**：无障碍关闭时使用全屏黑色遮罩（"A full-screen black panel covers the blocked app until you tap your tag"），说明该权限只是加速路径，不是功能前提。
- **文案属透明说明**，直接解释用途与隐私边界（不读屏幕内容、不外发），与 `canRetrieveWindowContent=false` 的实现一致，没有身份冒充或警告挤出。

**边界说明：** 引导页为 Jetpack Compose 运行时构建的界面，静态仅能还原到 composable 与字符串资源层级（`e2.q.b` 反编译部分降级为指令流），但界面文案全部来自本地 `strings.xml`，未发现远端 HTML/WebView 下发文案的路径。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全流程静态可见：无障碍服务配置、服务实现、权限状态检测（U1.h.*）、引导页 composable（e2.q.b）与跳转实现（e2.m.c）均可静态还原；引导界面由 Jetpack Compose 运行时构建，反编译部分退化为指令流，但全部文案来自本地 res/values/strings.xml，未发现远端 HTML/WebView 或加密载荷承载引导文案。",
  "summary_one_liner": "nfcGuard 在应用内 Compose 引导页逐项列出无障碍/用量访问/悬浮窗/电池/自启动的真实授权状态，用户点 GRANT 后仅调用标准 ACTION_ACCESSIBILITY_SETTINGS 打开系统无障碍列表，文案透明说明仅读取前台包名且明确表示不开启也能用（降级为全屏黑罩），无强制、无循环、无遮罩伪造。",
  "disguise_identity": {
    "app_display_name": "nfcGuard",
    "claimed_brand_or_persona": "nfcGuard（F-Droid 开源 NFC 专注自律/防沉迷工具，真实身份）",
    "a11y_service_label": "未在 AndroidManifest 中为服务声明 android:label，系统无障碍列表将回退显示应用名 nfcGuard（@string/app_name）；服务说明为 res/values/strings.xml 的 accessibility_service_description",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。虽经 R8 混淆（类名如 e2.q、U1.h），但为常规代码压缩，未使用空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool；服务声明与说明文案一致。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.andebugulin.nfcguard.ui.MainActivity（Compose 内容，根 composable 由 Y.a(..., new F(this,1), true) 设置）",
      "trigger_event": "onCreate → setContent(...) 渲染主界面/引导清单",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "GET STARTED / ACCESSIBILITY ACCESS / USAGE ACCESS / DISPLAY OVER APPS / BATTERY / AUTOSTART / NOTIFICATIONS",
      "shown_text_zh": "开始使用；无障碍访问、用量访问、叠加显示在其他应用上层、电池、自启动、通知（权限清单标题）",
      "user_action_requested": "浏览权限清单，逐项决定是否授予；存在 BACK 返回与跳过式继续（未开启也可继续使用）",
      "code_anchor": "com.andebugulin.nfcguard.ui.MainActivity.onCreate；res/values/strings.xml（onb_get_started、onb_accessibility_access、onb_usage_access、onb_display_over_apps、onb_battery、onb_autostart、onb_notifications、onb_back）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "Compose 引导 composable e2.q.b（权限状态行 + 说明文案），状态由 U1.h.a/d/e/c 实时检测",
      "trigger_event": "进入引导页时组合执行；U1.h.a 检测无障碍是否已启用、U1.h.d 检测悬浮窗、U1.h.e 检测用量访问、U1.h.c 检测电池优化白名单",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "nfcGuard uses Android's Accessibility API only to see which app is in the foreground, so it can close a blocked app instantly instead of covering it.\n\nIt never reads, records, or sends screen content, typed text, or any other personal data - on this device or anywhere else.",
      "shown_text_zh": "nfcGuard 仅使用 Android 无障碍 API 判断哪个应用在前台，从而能立即关闭被屏蔽的应用，而不是覆盖它。它从不读取、记录或发送屏幕内容、输入的文字或任何其他个人数据——在本机或任何其他地方。",
      "user_action_requested": "阅读说明后点击该行 GRANT 按钮（已授权则显示 GRANTED）；无强制，可返回或继续其他步骤",
      "code_anchor": "e2.q.b；U1.h.a / U1.h.d / U1.h.e / U1.h.c；strings.xml: onb_nfcguard_uses_androids_accessibility_api、onb_nfcguard_needs_to_know_which、onb_lets_nfcguard_close_a_blocked、onb_grant、onb_granted"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS），由 q.d(context, intent) 启动",
      "trigger_event": "用户点击无障碍行的 GRANT 按钮 → 协程回调 e2.m.c()（case 0：setValue(FALSE) 后 startActivity 跳系统无障碍列表）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "NFCGUARD uses this to reliably detect which app is in the foreground. This is needed on some devices (like Pixel) where the standard detection method fails when returning from the recent apps screen. NFCGUARD does NOT read any screen content or user data.",
      "shown_text_zh": "NFCGUARD 使用此权限可靠判断哪个应用位于前台。在部分设备（如 Pixel）从最近任务返回时标准检测方式失效，因此需要它。NFCGUARD 不读取任何屏幕内容或用户数据。",
      "user_action_requested": "在系统列表中找到 nfcGuard 并手动打开开关（应用无法自行授权，未做任何自动点击或跳转遮挡）",
      "code_anchor": "e2.m.c；res/xml/accessibility_service_config.xml（android:description=@string/accessibility_service_description）"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 MainActivity 后重新渲染引导页，U1.h.a 仍返回 false，该行保持 GRANT 状态",
      "trigger_event": "从系统设置返回（Activity 恢复）后 Compose 重组重新检测状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Blocking works fine without this.",
      "shown_text_zh": "不开这个权限，屏蔽也照常可用。",
      "user_action_requested": "可再次点击 GRANT，也可直接放弃继续使用；无死循环重跳、无定时拉起、无遮挡系统设置页",
      "code_anchor": "e2.q.b（U1.h.a 结果驱动行状态）；strings.xml: onb_blocking_works_fine_without_this"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "ForegroundDetectorService.onServiceConnected → 恢复 BlockerService 与告警调度",
      "trigger_event": "系统绑定服务回调 onServiceConnected",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "ForegroundDetectorService connected / Blocking restored on accessibility connect",
      "shown_text_zh": "（日志）前台检测服务已连接；无障碍连接时已恢复屏蔽",
      "user_action_requested": "无；仅重建 setServiceInfo(eventTypes=32, notificationTimeout=100) 并恢复屏蔽状态，未自动点击确认、未阻止撤权",
      "code_anchor": "com.andebugulin.nfcguard.service.ForegroundDetectorService.onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内 Compose 引导页（e2.q.b）逐行说明 + GRANT/GRANTED 按钮，文案取自 res/values/strings.xml 的 onb_* 键（原生 Activity，非 WebView）",
    "系统无障碍服务列表项说明：res/xml/accessibility_service_config.xml 的 android:description → @string/accessibility_service_description（AccessibilityService 列表页展示）",
    "应用内信息/说明页文案：info_a_full_screen_black_panel、info_closes_the_app_instantly_needs、info_u2022_enable_accessibility_for_the、home_accessibility_off_overlay_mode_active、home_accessibility_on_force_close_avoids",
    "未发现 assets 内 HTML/WebView 教学页、未发现半透明引导遮罩或全屏悬浮指引窗承载引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "NFCGUARD uses this to reliably detect which app is in the foreground. This is needed on some devices (like Pixel) where the standard detection method fails when returning from the recent apps screen. NFCGUARD does NOT read any screen content or user data.",
      "text_zh": "NFCGUARD 使用此权限可靠判断哪个应用位于前台。在部分设备（如 Pixel）从最近任务返回时标准检测方式失效，因此需要它。NFCGUARD 不读取任何屏幕内容或用户数据。",
      "source_location": "res/values/strings.xml → accessibility_service_description（系统无障碍列表展示）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "nfcGuard uses Android's Accessibility API only to see which app is in the foreground, so it can close a blocked app instantly instead of covering it.\n\nIt never reads, records, or sends screen content, typed text, or any other personal data - on this device or anywhere else.",
      "text_zh": "nfcGuard 仅使用 Android 无障碍 API 判断哪个应用在前台，从而立即关闭被屏蔽的应用而非覆盖它。它从不读取、记录或发送屏幕内容、输入文字或任何其他个人数据——本机或任何其他地方都不会。",
      "source_location": "res/values/strings.xml → onb_nfcguard_uses_androids_accessibility_api（引导页正文）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "nfcGuard needs to know which app is in the foreground to block the right one. It cannot see anything inside your apps.",
      "text_zh": "nfcGuard 需要知道哪个应用在前台才能屏蔽正确的应用。它看不到你应用内部的任何内容。",
      "source_location": "res/values/strings.xml → onb_nfcguard_needs_to_know_which",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Lets nfcGuard close a blocked app instantly instead of covering it. nfcGuard only reads which app is in front - never screen content.",
      "text_zh": "让 nfcGuard 立即关闭被屏蔽的应用，而不是覆盖它。nfcGuard 只读取哪个应用在前台——从不读取屏幕内容。",
      "source_location": "res/values/strings.xml → onb_lets_nfcguard_close_a_blocked",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Your device has a detection bug that makes blocking unreliable without this. nfcGuard only reads which app is in front - never screen content.",
      "text_zh": "你的设备存在检测缺陷，没有这个权限屏蔽会不可靠。nfcGuard 只读取哪个应用在前台——从不读取屏幕内容。",
      "source_location": "res/values/strings.xml → onb_your_device_has_a_detection",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Blocking works fine without this.",
      "text_zh": "不开这个也能正常屏蔽。",
      "source_location": "res/values/strings.xml → onb_blocking_works_fine_without_this",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "A full-screen black panel covers the blocked app until you tap your tag. Used automatically whenever the Accessibility Service is off.",
      "text_zh": "在你刷标签之前，全屏黑色面板会覆盖被屏蔽的应用。无障碍服务关闭时自动使用此方式。",
      "source_location": "res/values/strings.xml → info_a_full_screen_black_panel（降级路径说明）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无死循环：从系统设置返回后仅重新检测状态并保持该行 GRANT，用户可再次点击或直接放弃；无障碍关闭时自动降级为全屏黑色遮罩屏蔽（info_a_full_screen_black_panel），功能不被阻断。",
    "overlay_or_fake_settings": "无。未叠放半透明引导遮罩、未使用全屏悬浮窗指引，也未渲染高仿系统无障碍开关页；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无。未引导进入应用详情右上角菜单开启受限设置，也未使用 Session 安装器绕过；仅使用 android.settings.APPLICATION_DETAILS_SETTINGS 作为常规应用信息页入口（Y1.G#c），且未发现教唆忽略系统警告的文案。",
    "post_grant_anti_removal": "无。onServiceConnected 仅重建 ServiceInfo 并恢复屏蔽状态；未自动点击确认、未监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权（DEX 中 PERFORM_GLOBAL_ACTION/WATCH_SETTINGS 线索未落在无障碍引导链上，服务实现内无此类调用）。",
    "benign_graceful_degradation": "有。无障碍关闭时自动切换为全屏黑色面板覆盖模式（info_a_full_screen_black_panel、home_accessibility_off_overlay_mode_active）；引导页明确写有 Blocking works fine without this，另有 usage access / 电池优化 / 自启动 等非必需项均标注可选。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 指向 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（e2.m.c 分支），以及冷启动进入 MainActivity 后引导页首帧渲染时（无需任何用户操作即可出现权限清单）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导权限清单页",
        "page_identifier": "MainActivity 内 Compose 页面，含 GET STARTED / ACCESSIBILITY ACCESS / USAGE ACCESS / DISPLAY OVER APPS / BATTERY / AUTOSTART / NOTIFICATIONS 与每行 GRANT 按钮",
        "why_most_useful": "该页是唯一的引导载体，可判断是否存在强制、遮罩、恐吓文案；本例应显示为逐项可选、可返回的透明清单",
        "observable_utg_signals": ["是否存在不可取消弹窗或全屏遮罩", "每项是否都有 GRANT 与已授权 GRANTED 双态", "是否出现假更新/故障恐吓/仿反诈等诱导措辞", "是否有 BACK/跳过入口"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务中的 nfcGuard 条目及展开后的服务说明",
        "why_most_useful": "核对服务说明与实现是否一致（本例说明仅检测前台应用、声明不读屏幕内容），并确认应用未使用同形字/空白挤出等伪装",
        "observable_utg_signals": ["服务名称是否为 nfcGuard 而非仿冒系统组件", "说明文字是否为透明用途描述", "是否存在空白/换行导致的警告挤出"]
      },
      {
        "page_role": "返回应用后的拒权状态页",
        "page_identifier": "从系统设置返回 MainActivity 后重新渲染的引导页（该行仍为 GRANT）",
        "why_most_useful": "区分良性降级与拒权循环：观察是否被定时/onResume 强制重跳系统设置或叠加遮罩",
        "observable_utg_signals": ["返回后 3 秒内是否自动再次跳转设置页", "是否出现悬浮遮罩覆盖界面", "是否出现不可关闭的催促弹窗"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。引导文案全部为本地 strings.xml 文本，无纯图空文本诱导、无远端下发文案；静态未加壳（加壳初判 False，仅 R8 混淆类名），运行期 UTG 可完整观测。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "e2.q.b（Compose 引导权限清单页，调用 U1.h.a/d/e/c 检测各项授权状态）",
    "e2.m.c（GRANT 按钮回调：startActivity android.settings.ACCESSIBILITY_SETTINGS / 电池优化设置）",
    "U1.h.a / U1.h.d / U1.h.e / U1.h.c（无障碍、悬浮窗、用量访问、电池白名单真实状态检测）",
    "com.andebugulin.nfcguard.service.ForegroundDetectorService.onAccessibilityEvent / onServiceConnected",
    "res/xml/accessibility_service_config.xml（canRetrieveWindowContent=false，仅 typeWindowStateChanged）",
    "res/values/strings.xml（accessibility_service_description、onb_*、info_a_full_screen_black_panel）"
  ]
}
```

</details>
