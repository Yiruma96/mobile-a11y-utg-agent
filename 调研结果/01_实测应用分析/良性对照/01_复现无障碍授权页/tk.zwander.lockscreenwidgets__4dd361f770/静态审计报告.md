# BN_067__4dd361f770｜锁屏与悬浮组件辅助 — Widgets Anywhere

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：129.0s

## 1. 一句话核心结论

- **核心申请方式**：开源锁屏组件应用在冷启动或无障碍未开启时进入原生 Compose 引导页，以隐私承诺与用途说明文案配合可跳过的二次确认弹窗，一步直达系统『已安装的无障碍服务』列表，无遮罩、无拒权循环、无受限设置教学。
- **静态可见性说明**：无障碍授权引导链完全静态可见：入口（MainActivity.onCreate）、引导页（Compose IntroSlidesKt）、确认弹窗、跳转实现（AccessibilityUtilsKt.openAccessibilitySettings）与全部文案资源（res/values/strings.xml、res/xml/accessibility.xml）均已定位，无加壳、无 AES 载荷、无远端 HTML 或动态下发文案。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `4dd361f77009594715db64c2b751ce8fd1683567d10b9916f3cac215caaef26c` |
| 包名 / 年份 | `tk.zwander.lockscreenwidgets` / 2025-2026 |
| 家族 / 品类 | **锁屏与悬浮组件辅助**（同池样本数：1） |
| 原始来源标识 | https://apt.izzysoft.de/fdroid/repo/tk.zwander.lockscreenwidgets_221.apk |
| 桌面显示名 | Widgets Anywhere |
| 引导页宣称品牌/身份 | Widgets Anywhere（IzzyOnDroid 开源项目，作者 Zachary Wander，真实身份） |
| 系统无障碍列表服务名 | Widgets Anywhere（accessibility-service 未单独声明 android:label，系统列表沿用应用名） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `tk.zwander.lockscreenwidgets.services.Accessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Widgets Anywhere requires an Accessibility Service to display widgets on the lock screen and in the notification center. No data is collected, and no actions will be performed on the device. This permission is optional if you are only using the home screen widget stacks. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | tk.zwander.lockscreenwidgets.MainActivity（LAUNCHER 入口，Compose 主界面） | onCreate 中判断 PrefManager.getFirstRun() \|\| !AccessibilityUtilsKt.isAccessibilityEnabled()，成立则 OnboardingActivity.Companion.startForResult(this, introRequest, firstRun ? RetroMode.NONE : RetroMode.ACCESSIBILITY) | 原生Activity | 无 | 无强制操作，用户可返回退出 | `tk.zwander.lockscreenwidgets.MainActivity#onCreate` |
| 2 | 引导说明页 | tk.zwander.common.activities.OnboardingActivity（Compose IntroSlider，无障碍专用页） | rememberIntroSlides 在 startReason==NONE 或 ACCESSIBILITY 时向 slides 添加该页；LifecycleEffect(RESUMED) 刷新 hasAccessibility 状态 | 原生Activity | **原文**：Accessibility / To be able to display on the lock screen, you'll need to activate Widgets Anywhere's Accessibility Service. This app doesn't collect any data from your screen.<br>**译注**：无障碍 / 为了能在锁屏上显示，你需要启用 Widgets Anywhere 的无障碍服务。本应用不会收集你屏幕上的任何数据。 | 点击页内按钮继续（按钮可用性由 hasAccessibility 状态控制）；引导流程末页/弹窗提供跳过入口，无强制锁定 | `tk.zwander.common.compose.data.IntroSlidesKt#rememberIntroSlides / res/values/strings.xml intro_accessibility_title, intro_accessibility_desc` |
| 3 | 引导说明页（二次确认弹窗） | IntroSlides 无障碍页内 AlertDialog（AndroidAlertDialog_androidKt.AlertDialog） | 点击无障碍页按钮后 mutableState 置 true 触发弹窗；确认按钮回调 invokeSuspend$lambda$13$5$1$0$0 | 原生Dialog | **原文**：无（弹窗正文与按钮文案由 ComposableSingletons$IntroSlidesKt 内联字符串资源提供，本次未逐字解析）<br>**译注**：弹窗说明无障碍用途并提供『前往设置』与另一枚可结束引导的 TextButton（可跳过） | 选择前往设置，或点击第二个 TextButton 执行 finish 回调结束引导；存在跳过路径 | `tk.zwander.common.compose.data.IntroSlidesKt$rememberIntroSlides$4$1#invokeSuspend$lambda$13$5 / #invokeSuspend$lambda$13$5$2` |
| 4 | 跳无障碍设置 | 系统设置 com.android.settings / Settings$AccessibilityInstalledServiceActivity（回退 android.settings.ACCESSIBILITY_SETTINGS → android.settings.SETTINGS） | openAccessibilitySettings(context) 依次 startActivity，全部失败时 Toast R.string.unable_to_open_settings | 系统无障碍页 | **原文**：Widgets Anywhere requires an Accessibility Service to display widgets on the lock screen and in the notification center. No data is collected, and no actions will be performed on the device. This permission is optional if you are only using the home screen widget stacks.<br>**译注**：Widgets Anywhere 需要无障碍服务以在锁屏和通知中心显示组件。不会收集任何数据，也不会在设备上执行任何操作。若仅使用主屏组件堆叠，此权限是可选的。 | 用户在系统『已安装的服务』列表中自行找到 Widgets Anywhere 并手动开启开关；应用不做任何自动点击或诱导性遮罩 | `tk.zwander.common.util.AccessibilityUtilsKt#openAccessibilitySettings / res/xml/accessibility.xml android:description` |
| 5 | 拒权反馈循环 | 返回 OnboardingActivity / MainActivity 主界面 AccessibilityCard | 未开启无障碍时返回，OnboardingActivity 的 LifecycleEffect(RESUMED) 仅刷新状态；主界面渲染 errorContainer 色卡片，内含『Accessibility Settings』按钮供用户再次手动跳转 | 原生Activity | **原文**：Accessibility Settings / The Accessibility Service isn't currently running. This may be because you need to allowlist Widgets Anywhere from your phone's battery optimizations, or you may just need to toggle it off and on again in Settings.<br>**译注**：无障碍设置 / 无障碍服务当前未运行。这可能是因为需要把 Widgets Anywhere 加入电池优化白名单，或者只是需要在设置中关闭再重新打开一次。 | 用户可自由忽略该提示继续使用非无障碍功能（桌面组件堆叠），无定时重跳、无 onResume 死循环、无弹窗阻塞 | `tk.zwander.common.compose.main.AccessibilityCardKt#AccessibilityCard / tk.zwander.common.compose.main.AccessibilityCardKt#AccessibilityCard$lambda$0$1$6$0` |
| 6 | 获权后动作 | tk.zwander.lockscreenwidgets.services.Accessibility（AccessibilityService，锁屏帧 WidgetFrameDelegate / 抽屉 DrawerDelegate） | onServiceConnected 初始化帧与抽屉代理，onAccessibilityEvent 监听窗口内容/窗口状态变化以维持锁屏帧显示 | 原生Activity | **原文**：The Accessibility Service hasn't started yet. Please wait.<br>**译注**：无障碍服务尚未启动，请稍候。（仅状态提示，无自动确认授权、无阻止撤权动作） | 无额外操作；未见自点确认、自授权或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权 | `tk.zwander.lockscreenwidgets.services.Accessibility#onServiceConnected / #onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- OnboardingActivity（原生 Compose IntroSlider）无障碍专用页正文：res/values/strings.xml intro_accessibility_title + intro_accessibility_desc
- OnboardingActivity 无障碍页内 AndroidAlertDialog 二次确认弹窗（可跳过）
- 系统无障碍『已安装的服务』列表项描述：res/xml/accessibility.xml android:description = @string/accessibility_service_desc
- 主界面 AccessibilityCard（errorContainer 警示色卡片，按钮文案 res/values/strings.xml accessibility_settings = 'Accessibility Settings'）
- 主界面状态文案 main_screen_accessibility_not_started（服务未运行时的电池优化/重开开关提示）
- 服务状态 Toast：res/values/strings.xml accessibility_not_started、unable_to_open_settings

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To be able to display on the lock screen, you'll need to activate Widgets Anywhere's Accessibility Service. This app doesn't collect any data from your screen. | 为了能在锁屏上显示，你需要启用 Widgets Anywhere 的无障碍服务。本应用不会收集你屏幕上的任何数据。 | `res/values/strings.xml key=intro_accessibility_desc` | 隐私承诺 |
| en | Widgets Anywhere requires an Accessibility Service to display widgets on the lock screen and in the notification center. No data is collected, and no actions will be performed on the device. This permission is optional if you are only using the home screen widget stacks. | Widgets Anywhere 需要无障碍服务以在锁屏和通知中心显示组件。不会收集任何数据，也不会在设备上执行任何操作。若仅使用主屏组件堆叠，此权限是可选的。 | `res/values/strings.xml key=accessibility_service_desc（由 res/xml/accessibility.xml android:description 引用）` | 良性透明说明 |
| en | The Accessibility Service isn't currently running. This may be because you need to allowlist Widgets Anywhere from your phone's battery optimizations, or you may just need to toggle it off and on again in Settings. | 无障碍服务当前未运行。这可能是因为需要把 Widgets Anywhere 加入电池优化白名单，或者只是需要在设置中关闭再重新打开一次。 | `res/values/strings.xml key=main_screen_accessibility_not_started` | 良性透明说明 |
| en | Accessibility Settings | 无障碍设置 | `res/values/strings.xml key=accessibility_settings（AccessibilityCard 按钮文案）` | 受限设置分步教学 |
| en | The Accessibility Service hasn't started yet. Please wait. | 无障碍服务尚未启动，请稍候。 | `res/values/strings.xml key=accessibility_not_started` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环：MainActivity 仅在 onCreate 判断一次；OnboardingActivity 返回后只用 LifecycleEffect(RESUMED) 刷新 hasAccessibility 状态，未在 onResume 重跳、无 Timer 拉起、无后台重弹。未开启无障碍时安全降级为主界面 AccessibilityCard 静态提示 + 手动按钮。
- **遮罩叠层 / 高仿系统设置页**：无。仅使用系统原生设置页；无半透明遮罩、无全屏悬浮窗引导、无高仿无障碍开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。未发现自点确认、自授权或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权（预筛的 PERFORM_GLOBAL_ACTION/WATCH_SETTINGS 未追至撤权阻止逻辑，不据此认定）
- **良性降级 / 替代方案**：有。android:description 明确『若仅使用主屏组件堆叠则该权限可选』；通知监听、读取存储等引导页亦注明『You don't have to grant this right now』；未授权时主界面与桌面组件堆叠功能仍可用。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 com.android.settings/Settings$AccessibilityInstalledServiceActivity 或 ACTION_ACCESSIBILITY_SETTINGS 的瞬间拉起 UTG；或在 MainActivity.onCreate 后 OnboardingActivity 首次呈现无障碍引导页时截图。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。文案全部为 strings.xml 文本资源、无图片化诱导、无远端 HTML。唯一注意点：AlertDialog 的按钮文案由 ComposableSingletons$IntroSlidesKt 内联字符串资源提供，静态未逐字还原，需以运行期 UTG 文本节点补全；另预筛 PERFORM_GLOBAL_ACTION/WATCH_SETTINGS 未在本轮追溯至撤权阻止逻辑，属本次定向范围边界而非不可见代码。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/回访引导页（无障碍专用 IntroPage）** | OnboardingActivity 内标题『Accessibility』+ 正文『To be able to display on the lock screen…』的 Compose 页面 | 这是唯一承载授权说服文案的载体，可直接判断是否存在恐吓/伪装/隐私虚假承诺 | 标题与正文文本节点（Accessibility / intro_accessibility_desc 原文）；按钮可点击性（hasAccessibility 控制）；是否为系统设置页伪造（包名仍为 tk.zwander.lockscreenwidgets） |
| **二次确认弹窗页** | 覆盖在 OnboardingActivity 上的 AlertDialog，含两枚 TextButton | 验证是否存在『不可取消/无跳过』的强制结构 | 按钮数量与文案（是否同时存在前往设置与结束引导两枚按钮）；弹窗是否可 back 关闭；是否叠加半透明遮罩或指向性箭头 |
| **系统无障碍服务列表项** | com.android.settings Settings$AccessibilityInstalledServiceActivity 中的『Widgets Anywhere』条目 | 核对服务名与 android:description 是否与引导文案一致，排除身份冒充与虚假能力声明 | 服务显示名（应为 Widgets Anywhere）；描述文本是否含『No data is collected…optional』；是否出现系统受限设置警告（未声明 isAccessibilityTool 时会提示完整能力） |
| **拒权返回后的主界面卡片** | MainActivity 内 errorContainer 色 AccessibilityCard，按钮『Accessibility Settings』 | 确认拒绝授权后是否安全降级、有无定时重跳或阻塞 | 卡片文案（服务未运行 + 电池优化建议）；是否存在自动跳转（观察停留时长）；其它功能入口是否仍可操作 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `tk.zwander.lockscreenwidgets.MainActivity#onCreate`
- `tk.zwander.common.util.AccessibilityUtilsKt#openAccessibilitySettings`
- `tk.zwander.common.compose.data.IntroSlidesKt#rememberIntroSlides`
- `tk.zwander.common.compose.data.IntroSlidesKt$rememberIntroSlides$4$1#invokeSuspend$lambda$13$5`
- `tk.zwander.common.compose.main.AccessibilityCardKt#AccessibilityCard`
- `res/xml/accessibility.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期引导链，静态已闭环）

**判定：良性透明的无障碍授权引导，未见诱导、遮罩或拒权循环。**

引导链完整可静态还原，共 4 个入口，均指向同一个跳转函数：

1. **冷启动/回访拦截**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:tk.zwander.lockscreenwidgets.MainActivity#onCreate>) 判断 `getFirstRun() || !isAccessibilityEnabled()`，成立即 `OnboardingActivity.Companion.startForResult(..., firstRun ? RetroMode.NONE : RetroMode.ACCESSIBILITY)`——首次启动走完整引导，非首次但无障碍未开启时只投递**单个无障碍引导页**。
2. **引导页（原生 Compose Activity，非 WebView）**：[rememberIntroSlides$4$1.invokeSuspend()](<resource-unit:#1.dex1 code:tk.zwander.common.compose.data.IntroSlidesKt$rememberIntroSlides$4$1#invokeSuspend>) 仅在 `startReason==NONE||ACCESSIBILITY` 时插入无障碍页，标题/正文取 `intro_accessibility_title` / [intro_accessibility_desc](<resource-unit:#1 file:res/values/strings.xml#L207-L208>)，主按钮回调 `invokeSuspend$lambda$13$5$1$0$0`。
3. **二次确认弹窗**：同一引导页的 [invokeSuspend$lambda$13$5()](<resource-unit:#1.dex1 code:tk.zwander.common.compose.data.IntroSlidesKt$rememberIntroSlides$4$1#invokeSuspend$lambda$13$5>) 渲染 `AlertDialog`，两个 `TextButton`：一个调 `openAccessibilitySettings` 并置 `showDialog=false`，另一个直接执行 `finish` 回调（**可跳过，无强制**）。
4. **统一跳转实现**：[openAccessibilitySettings()](<resource-unit:#1.dex1 code:tk.zwander.common.util.AccessibilityUtilsKt#openAccessibilitySettings>) 优先 `ComponentName("com.android.settings","Settings$AccessibilityInstalledServiceActivity")` 直达**已安装服务列表**，异常回退 `ACTION_ACCESSIBILITY_SETTINGS`，再回退 `ACTION_SETTINGS`，最终 Toast `unable_to_open_settings`。全程无自定义遮罩、无高仿开关页、无 `APPLICATION_DETAILS_SETTINGS` 用于受限设置教学。

**辅助入口**：主界面的 [AccessibilityCard](<resource-unit:#1.dex1 code:tk.zwander.common.compose.main.AccessibilityCardKt#AccessibilityCard>)（errorContainer 警示色卡片，正文仅「Accessibility Settings」按钮）同样调用上述跳转；`ComposeFrameSettingsActivity` 内 3 处同类回调。

**权限声明与文案一致性**：[accessibility.xml](<resource-unit:#1 file:res/xml/accessibility.xml>) 仅 `canRetrieveWindowContent=true`、窗口内容变更/窗口状态事件、`flagIncludeNotImportantViews|flagReportViewIds|flagRetrieveInteractiveWindows`，**未申请** `canPerformGestures`、按键过滤、`canRequestTouchExplorationMode=false`；`android:description` 明确「No data is collected…This permission is optional if you are only using the home screen widget stacks」，与代码行为一致，且明确提供**无无障碍的替代路径**（仅桌面组件堆叠）。服务名沿用应用名 `Widgets Anywhere`，无同形字/空白挤出/多 alias 伪装。

**覆盖边界**：预筛标记的 `PERFORM_GLOBAL_ACTION`、`WATCH_SETTINGS` 未在本次定向链路中追至撤权阻止逻辑（`Accessibility.onServiceConnected/onEvent` 主要服务于锁屏帧与抽屉的显示状态），不据此认定为反卸载；`isAccessibilityTool` 未声明（系统将按非工具类服务给出完整警告，属透明行为）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍授权引导链完全静态可见：入口（MainActivity.onCreate）、引导页（Compose IntroSlidesKt）、确认弹窗、跳转实现（AccessibilityUtilsKt.openAccessibilitySettings）与全部文案资源（res/values/strings.xml、res/xml/accessibility.xml）均已定位，无加壳、无 AES 载荷、无远端 HTML 或动态下发文案。",
  "summary_one_liner": "开源锁屏组件应用在冷启动或无障碍未开启时进入原生 Compose 引导页，以隐私承诺与用途说明文案配合可跳过的二次确认弹窗，一步直达系统『已安装的无障碍服务』列表，无遮罩、无拒权循环、无受限设置教学。",
  "disguise_identity": {
    "app_display_name": "Widgets Anywhere",
    "claimed_brand_or_persona": "Widgets Anywhere（IzzyOnDroid 开源项目，作者 Zachary Wander，真实身份）",
    "a11y_service_label": "Widgets Anywhere（accessibility-service 未单独声明 android:label，系统列表沿用应用名）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "tk.zwander.lockscreenwidgets.MainActivity（LAUNCHER 入口，Compose 主界面）",
      "trigger_event": "onCreate 中判断 PrefManager.getFirstRun() || !AccessibilityUtilsKt.isAccessibilityEnabled()，成立则 OnboardingActivity.Companion.startForResult(this, introRequest, firstRun ? RetroMode.NONE : RetroMode.ACCESSIBILITY)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "主界面先正常渲染，同时拉起引导页；无任何弹窗恐吓或遮罩",
      "user_action_requested": "无强制操作，用户可返回退出",
      "code_anchor": "tk.zwander.lockscreenwidgets.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "tk.zwander.common.activities.OnboardingActivity（Compose IntroSlider，无障碍专用页）",
      "trigger_event": "rememberIntroSlides 在 startReason==NONE 或 ACCESSIBILITY 时向 slides 添加该页；LifecycleEffect(RESUMED) 刷新 hasAccessibility 状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility / To be able to display on the lock screen, you'll need to activate Widgets Anywhere's Accessibility Service. This app doesn't collect any data from your screen.",
      "shown_text_zh": "无障碍 / 为了能在锁屏上显示，你需要启用 Widgets Anywhere 的无障碍服务。本应用不会收集你屏幕上的任何数据。",
      "user_action_requested": "点击页内按钮继续（按钮可用性由 hasAccessibility 状态控制）；引导流程末页/弹窗提供跳过入口，无强制锁定",
      "code_anchor": "tk.zwander.common.compose.data.IntroSlidesKt#rememberIntroSlides / res/values/strings.xml intro_accessibility_title, intro_accessibility_desc"
    },
    {
      "step": 3,
      "stage": "引导说明页（二次确认弹窗）",
      "screen_or_component": "IntroSlides 无障碍页内 AlertDialog（AndroidAlertDialog_androidKt.AlertDialog）",
      "trigger_event": "点击无障碍页按钮后 mutableState 置 true 触发弹窗；确认按钮回调 invokeSuspend$lambda$13$5$1$0$0",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无（弹窗正文与按钮文案由 ComposableSingletons$IntroSlidesKt 内联字符串资源提供，本次未逐字解析）",
      "shown_text_zh": "弹窗说明无障碍用途并提供『前往设置』与另一枚可结束引导的 TextButton（可跳过）",
      "user_action_requested": "选择前往设置，或点击第二个 TextButton 执行 finish 回调结束引导；存在跳过路径",
      "code_anchor": "tk.zwander.common.compose.data.IntroSlidesKt$rememberIntroSlides$4$1#invokeSuspend$lambda$13$5 / #invokeSuspend$lambda$13$5$2"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 com.android.settings / Settings$AccessibilityInstalledServiceActivity（回退 android.settings.ACCESSIBILITY_SETTINGS → android.settings.SETTINGS）",
      "trigger_event": "openAccessibilitySettings(context) 依次 startActivity，全部失败时 Toast R.string.unable_to_open_settings",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Widgets Anywhere requires an Accessibility Service to display widgets on the lock screen and in the notification center. No data is collected, and no actions will be performed on the device. This permission is optional if you are only using the home screen widget stacks.",
      "shown_text_zh": "Widgets Anywhere 需要无障碍服务以在锁屏和通知中心显示组件。不会收集任何数据，也不会在设备上执行任何操作。若仅使用主屏组件堆叠，此权限是可选的。",
      "user_action_requested": "用户在系统『已安装的服务』列表中自行找到 Widgets Anywhere 并手动开启开关；应用不做任何自动点击或诱导性遮罩",
      "code_anchor": "tk.zwander.common.util.AccessibilityUtilsKt#openAccessibilitySettings / res/xml/accessibility.xml android:description"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 OnboardingActivity / MainActivity 主界面 AccessibilityCard",
      "trigger_event": "未开启无障碍时返回，OnboardingActivity 的 LifecycleEffect(RESUMED) 仅刷新状态；主界面渲染 errorContainer 色卡片，内含『Accessibility Settings』按钮供用户再次手动跳转",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility Settings / The Accessibility Service isn't currently running. This may be because you need to allowlist Widgets Anywhere from your phone's battery optimizations, or you may just need to toggle it off and on again in Settings.",
      "shown_text_zh": "无障碍设置 / 无障碍服务当前未运行。这可能是因为需要把 Widgets Anywhere 加入电池优化白名单，或者只是需要在设置中关闭再重新打开一次。",
      "user_action_requested": "用户可自由忽略该提示继续使用非无障碍功能（桌面组件堆叠），无定时重跳、无 onResume 死循环、无弹窗阻塞",
      "code_anchor": "tk.zwander.common.compose.main.AccessibilityCardKt#AccessibilityCard / tk.zwander.common.compose.main.AccessibilityCardKt#AccessibilityCard$lambda$0$1$6$0"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "tk.zwander.lockscreenwidgets.services.Accessibility（AccessibilityService，锁屏帧 WidgetFrameDelegate / 抽屉 DrawerDelegate）",
      "trigger_event": "onServiceConnected 初始化帧与抽屉代理，onAccessibilityEvent 监听窗口内容/窗口状态变化以维持锁屏帧显示",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "The Accessibility Service hasn't started yet. Please wait.",
      "shown_text_zh": "无障碍服务尚未启动，请稍候。（仅状态提示，无自动确认授权、无阻止撤权动作）",
      "user_action_requested": "无额外操作；未见自点确认、自授权或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权",
      "code_anchor": "tk.zwander.lockscreenwidgets.services.Accessibility#onServiceConnected / #onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "OnboardingActivity（原生 Compose IntroSlider）无障碍专用页正文：res/values/strings.xml intro_accessibility_title + intro_accessibility_desc",
    "OnboardingActivity 无障碍页内 AndroidAlertDialog 二次确认弹窗（可跳过）",
    "系统无障碍『已安装的服务』列表项描述：res/xml/accessibility.xml android:description = @string/accessibility_service_desc",
    "主界面 AccessibilityCard（errorContainer 警示色卡片，按钮文案 res/values/strings.xml accessibility_settings = 'Accessibility Settings'）",
    "主界面状态文案 main_screen_accessibility_not_started（服务未运行时的电池优化/重开开关提示）",
    "服务状态 Toast：res/values/strings.xml accessibility_not_started、unable_to_open_settings"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To be able to display on the lock screen, you'll need to activate Widgets Anywhere's Accessibility Service. This app doesn't collect any data from your screen.",
      "text_zh": "为了能在锁屏上显示，你需要启用 Widgets Anywhere 的无障碍服务。本应用不会收集你屏幕上的任何数据。",
      "source_location": "res/values/strings.xml key=intro_accessibility_desc",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Widgets Anywhere requires an Accessibility Service to display widgets on the lock screen and in the notification center. No data is collected, and no actions will be performed on the device. This permission is optional if you are only using the home screen widget stacks.",
      "text_zh": "Widgets Anywhere 需要无障碍服务以在锁屏和通知中心显示组件。不会收集任何数据，也不会在设备上执行任何操作。若仅使用主屏组件堆叠，此权限是可选的。",
      "source_location": "res/values/strings.xml key=accessibility_service_desc（由 res/xml/accessibility.xml android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The Accessibility Service isn't currently running. This may be because you need to allowlist Widgets Anywhere from your phone's battery optimizations, or you may just need to toggle it off and on again in Settings.",
      "text_zh": "无障碍服务当前未运行。这可能是因为需要把 Widgets Anywhere 加入电池优化白名单，或者只是需要在设置中关闭再重新打开一次。",
      "source_location": "res/values/strings.xml key=main_screen_accessibility_not_started",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Settings",
      "text_zh": "无障碍设置",
      "source_location": "res/values/strings.xml key=accessibility_settings（AccessibilityCard 按钮文案）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The Accessibility Service hasn't started yet. Please wait.",
      "text_zh": "无障碍服务尚未启动，请稍候。",
      "source_location": "res/values/strings.xml key=accessibility_not_started",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环：MainActivity 仅在 onCreate 判断一次；OnboardingActivity 返回后只用 LifecycleEffect(RESUMED) 刷新 hasAccessibility 状态，未在 onResume 重跳、无 Timer 拉起、无后台重弹。未开启无障碍时安全降级为主界面 AccessibilityCard 静态提示 + 手动按钮。",
    "overlay_or_fake_settings": "无。仅使用系统原生设置页；无半透明遮罩、无全屏悬浮窗引导、无高仿无障碍开关页。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。未发现自点确认、自授权或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权（预筛的 PERFORM_GLOBAL_ACTION/WATCH_SETTINGS 未追至撤权阻止逻辑，不据此认定）",
    "benign_graceful_degradation": "有。android:description 明确『若仅使用主屏组件堆叠则该权限可选』；通知监听、读取存储等引导页亦注明『You don't have to grant this right now』；未授权时主界面与桌面组件堆叠功能仍可用。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 com.android.settings/Settings$AccessibilityInstalledServiceActivity 或 ACTION_ACCESSIBILITY_SETTINGS 的瞬间拉起 UTG；或在 MainActivity.onCreate 后 OnboardingActivity 首次呈现无障碍引导页时截图。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/回访引导页（无障碍专用 IntroPage）",
        "page_identifier": "OnboardingActivity 内标题『Accessibility』+ 正文『To be able to display on the lock screen…』的 Compose 页面",
        "why_most_useful": "这是唯一承载授权说服文案的载体，可直接判断是否存在恐吓/伪装/隐私虚假承诺",
        "observable_utg_signals": ["标题与正文文本节点（Accessibility / intro_accessibility_desc 原文）", "按钮可点击性（hasAccessibility 控制）", "是否为系统设置页伪造（包名仍为 tk.zwander.lockscreenwidgets）"]
      },
      {
        "page_role": "二次确认弹窗页",
        "page_identifier": "覆盖在 OnboardingActivity 上的 AlertDialog，含两枚 TextButton",
        "why_most_useful": "验证是否存在『不可取消/无跳过』的强制结构",
        "observable_utg_signals": ["按钮数量与文案（是否同时存在前往设置与结束引导两枚按钮）", "弹窗是否可 back 关闭", "是否叠加半透明遮罩或指向性箭头"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings Settings$AccessibilityInstalledServiceActivity 中的『Widgets Anywhere』条目",
        "why_most_useful": "核对服务名与 android:description 是否与引导文案一致，排除身份冒充与虚假能力声明",
        "observable_utg_signals": ["服务显示名（应为 Widgets Anywhere）", "描述文本是否含『No data is collected…optional』", "是否出现系统受限设置警告（未声明 isAccessibilityTool 时会提示完整能力）"]
      },
      {
        "page_role": "拒权返回后的主界面卡片",
        "page_identifier": "MainActivity 内 errorContainer 色 AccessibilityCard，按钮『Accessibility Settings』",
        "why_most_useful": "确认拒绝授权后是否安全降级、有无定时重跳或阻塞",
        "observable_utg_signals": ["卡片文案（服务未运行 + 电池优化建议）", "是否存在自动跳转（观察停留时长）", "其它功能入口是否仍可操作"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。文案全部为 strings.xml 文本资源、无图片化诱导、无远端 HTML。唯一注意点：AlertDialog 的按钮文案由 ComposableSingletons$IntroSlidesKt 内联字符串资源提供，静态未逐字还原，需以运行期 UTG 文本节点补全；另预筛 PERFORM_GLOBAL_ACTION/WATCH_SETTINGS 未在本轮追溯至撤权阻止逻辑，属本次定向范围边界而非不可见代码。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "tk.zwander.lockscreenwidgets.MainActivity#onCreate",
    "tk.zwander.common.util.AccessibilityUtilsKt#openAccessibilitySettings",
    "tk.zwander.common.compose.data.IntroSlidesKt#rememberIntroSlides",
    "tk.zwander.common.compose.data.IntroSlidesKt$rememberIntroSlides$4$1#invokeSuspend$lambda$13$5",
    "tk.zwander.common.compose.main.AccessibilityCardKt#AccessibilityCard",
    "res/xml/accessibility.xml"
  ]
}
```

</details>
