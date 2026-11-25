# BN_022__3495ff18fd｜显示调节、截屏与分屏效率 — Extend

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：193.2s

## 1. 一句话核心结论

- **核心申请方式**：Extend 在用户主动使用触控板/悬浮返回键时才弹出可拒绝的原生说明对话框，明示模拟手势与读取窗口用途及本地处理承诺，同意后跳系统无障碍设置（或在已授权 Shizuku 时直接写入 Secure 设置），无冷启动诱导、无死循环、无遮罩伪装。
- **静态可见性说明**：全链路静态完整可见：授权入口为原生 AccessibilityConsentActivity + MaterialAlertDialog，跳转为硬编码 android.settings.ACCESSIBILITY_SETTINGS；无加壳（apkid/预筛 packed=False）、无 AES/加密载荷、无 assets 内 HTML、无远端 WebView、无动态加载 DEX/SO。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3495ff18fdde91875762a8f6bbab86109d397ffd9d35d6fab5c36641fdb33231` |
| 包名 / 年份 | `io.github.jqssun.displayextend` / 2025-2026 |
| 家族 / 品类 | **显示调节、截屏与分屏效率**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/io.github.jqssun.displayextend_27.apk |
| 桌面显示名 | Extend |
| 引导页宣称品牌/身份 | Extend（F-Droid 开源，io.github.jqssun.displayextend，与 io.github.jqssun.displaymirror 同作者生态） |
| 系统无障碍列表服务名 | Extend（服务未声明 android:label，系统无障碍列表回退显示应用名；描述为 Accessibility service for simulating touch events on secondary screens） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅 R8 混淆（类名/资源 ID 混淆属常规构建），无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool（搜索 no_matches）。 |
| 无障碍服务类名 | `io.github.jqssun.displayextend.TouchpadAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Accessibility service for simulating touch events on secondary screens |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | io.github.jqssun.displayextend.MainActivity（NavHost + BottomNavigationView，默认进入 OverviewFragment） | LAUNCHER 图标点击 → MainActivity.onCreate / onResume | 原生Activity | **原文**：无（冷启动不弹任何权限或引导对话框）<br>**译注**：冷启动仅展示主界面与底部导航，不做无障碍权限提示 | 无强制动作；用户可自由浏览 | `io.github.jqssun.displayextend.MainActivity#onCreate / #onResume` |
| 2 | 业务功能触发 | DisplayDetailFragment / OverviewFragment 的"触控板""悬浮返回键"按钮与无障碍状态卡片；FloatingButtonService.startFloating；job.StartTouchPad | 用户点击触控板按钮（case 2）或无障碍卡片（case 1）→ 调用 ensureServiceAvailable(context, true) | 原生Activity | **原文**：Accessibility / Optional; only needed for popup and system surfaces on external displays<br>**译注**：概览页"无障碍"一行显示未启用状态，并提示该权限对外接显示器上的弹窗与系统界面为可选/必需 | 用户主动点击触控板或无障碍状态按钮，才进入授权流程 | `io.github.jqssun.displayextend.DisplayDetailFragment$$ExternalSyntheticLambda5#onClick; io.github.jqssun.displayextend.OverviewFragment#_updateAccessibilityStatus` |
| 3 | 引导说明页 | io.github.jqssun.displayextend.AccessibilityConsentActivity（@style/AppTheme.Transparent，excludeFromRecents=true）内的 MaterialAlertDialog | ensureServiceAvailable 检测到 accessibility_consent 未置位 → startActivity(AccessibilityConsentActivity)（FLAG_ACTIVITY_NEW_TASK）→ onCreate 直接 show() | 原生Dialog | **原文**：Enable accessibility access / Extend uses the Accessibility Service to operate your external displays: it simulates navigation actions for the on-screen touchpad and floating button, draws the on-screen cursor, and reads window details to direct your input to the focused window on the correct display. This information is used only on your device and is never collected, stored, or shared. Would you like to enable Accessibility Service? / Enable / Not now<br>**译注**：标题"开启无障碍权限"；正文说明 Extend 使用无障碍服务操作外接显示器：为屏幕触控板与悬浮按钮模拟导航动作、绘制屏幕光标、读取窗口详情以把输入定向到正确显示器上的焦点窗口；这些信息仅在本机使用，绝不收集、存储或共享；询问是否开启无障碍服务。按钮为"开启"与"暂不"。 | 选择"Enable"进入系统无障碍设置（或经 Shizuku 直接开启），或选择"Not now"放弃；对话框 mCancelable=false，但保留明确可点的拒绝按钮 | `io.github.jqssun.displayextend.AccessibilityConsentActivity#onCreate; res/values/strings.xml (accessibility_consent_title/message/agree/decline)` |
| 4 | 跳受限设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（服务列表项：Extend / Accessibility service for simulating touch events on secondary screens） | 点击"Enable" → 写 accessibility_consent=true → ensureServiceAvailable(context, true) → 无 Shizuku 权限且服务未启用 → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))，随后 finish() | 系统无障碍页 | **原文**：Accessibility service for simulating touch events on secondary screens<br>**译注**：系统无障碍服务列表中该服务描述为"用于在副屏模拟触摸事件的无障碍服务" | 用户在系统页面手动打开 Extend 的无障碍开关（无任何教唆忽略系统警告的文案，无跳转应用详情页开启受限设置的步骤） | `io.github.jqssun.displayextend.TouchpadAccessibilityService#ensureServiceAvailable; res/xml/accessibility_service_config.xml` |
| 5 | 拒权反馈循环 | AccessibilityConsentActivity 关闭后回到原页面；MainActivity.onResume / OverviewFragment 状态刷新 | 点"Not now" → AccessibilityConsentActivity$$ExternalSyntheticLambda0.onClick(default 分支) → finish()；返回后 onResume → State.refreshUI → _updateAccessibilityStatus 仅更新文案 | 原生Activity | **原文**：Accessibility / Required for controlling popup and system surfaces on external displays<br>**译注**：拒绝后停留在原页面，无障碍状态仍显示未启用并标注该权限对弹窗/系统界面为必需，功能优雅降级，不重复拉起 | 无强制动作；用户可继续使用其他功能，需要时再次手动点击 | `io.github.jqssun.displayextend.AccessibilityConsentActivity$$ExternalSyntheticLambda0#onClick; io.github.jqssun.displayextend.OverviewFragment#_updateAccessibilityStatus` |
| 6 | 获权后动作 | TouchpadAccessibilityService（onServiceConnected 仅置 instance、写日志、刷新 UI）；或 Shizuku 分支写入 Settings.Secure | 系统回调 onServiceConnected，或 ensureServiceAvailable 中 Sui.hasPermission() 为真时调用 startServiceByShizuku 写 enabled_accessibility_services / accessibility_enabled=1 | 原生Activity | **原文**：Enabled<br>**译注**：获权后无障碍状态显示"已启用"，授权按钮隐藏；服务不监听任何无障碍事件（onAccessibilityEvent 为空实现） | 无（不自动确认、不阻止用户撤销权限） | `io.github.jqssun.displayextend.TouchpadAccessibilityService#onServiceConnected; io.github.jqssun.displayextend.TouchpadAccessibilityService#startServiceByShizuku` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- AccessibilityConsentActivity 内的 MaterialAlertDialog（标题 accessibility_consent_title、正文 accessibility_consent_message、按钮 accessibility_consent_agree/decline），透明主题 Activity，不可点外部/返回键取消但含 Not now 按钮
- 系统无障碍服务列表项描述：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description（"Accessibility service for simulating touch events on secondary screens"），服务本身未声明 android:label，回退显示应用名 Extend
- 概览页（OverviewFragment）权限卡片与无障碍行：accessibility_permission_status / accessibility_status_enabled / accessibility_status_optional_for_touchpad_surfaces / accessibility_status_required_for_touchpad_surfaces / permissions_granted(_detail) / permissions_not_granted(_detail)
- 设置页开关项说明：touchpad_accessibility_overlay_desc、floating_button_desc、accessibility_consent 相关设置项文本
- 无 assets HTML、无 WebView、无悬浮窗遮罩、无高仿系统设置页承载任何引导文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable accessibility access | 开启无障碍权限 | `res/values/strings.xml: accessibility_consent_title` | 良性透明说明 |
| en | Extend uses the Accessibility Service to operate your external displays: it simulates navigation actions for the on-screen touchpad and floating button, draws the on-screen cursor, and reads window details to direct your input to the focused window on the correct display. This information is used only on your device and is never collected, stored, or shared. Would you like to enable Accessibility Service? | Extend 使用无障碍服务来操作您的外接显示器：它为屏幕触控板和悬浮按钮模拟导航动作、绘制屏幕光标，并读取窗口详情以把您的输入定向到正确显示器上的焦点窗口。这些信息仅在本机使用，绝不收集、存储或共享。是否开启无障碍服务？ | `res/values/strings.xml: accessibility_consent_message` | 隐私承诺 |
| en | Enable | 开启 | `res/values/strings.xml: accessibility_consent_agree` | 良性透明说明 |
| en | Not now | 暂不 | `res/values/strings.xml: accessibility_consent_decline` | 良性透明说明 |
| en | Accessibility service for simulating touch events on secondary screens | 用于在副屏模拟触摸事件的无障碍服务 | `res/values/strings.xml: accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 引用）` | 良性透明说明 |
| en | Required for controlling popup and system surfaces on external displays | 控制外接显示器上的弹窗与系统界面所必需 | `res/values/strings.xml: accessibility_status_required_for_touchpad_surfaces` | 良性透明说明 |
| en | Optional; only needed for popup and system surfaces on external displays | 可选；仅外接显示器上的弹窗与系统界面需要 | `res/values/strings.xml: accessibility_status_optional_for_touchpad_surfaces` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。点 Not now 仅 finish() 并留在原页面，无障碍状态行更新为未启用提示，无 onResume 重跳、无定时器拉起、无倒计时强制；用户可继续使用其他功能。
- **遮罩叠层 / 高仿系统设置页**：无。不叠放半透明遮罩、不建全屏悬浮引导窗、无高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于触控板/悬浮返回键本身的功能实现，与授权引导无关。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包搜索 APPLICATION_DETAILS_SETTINGS 无命中，不教用户进应用详情页开启受限设置，也无 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。onAccessibilityEvent 为空实现，不监听设置页；未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权，不自动点确认。
- **良性降级 / 替代方案**：有。无障碍为可选能力：概览页明确区分"可选"与"必需"两种场景；未授权时触控板/悬浮键相关路径仅提示并可继续使用其他显示管理功能；另有 Shizuku/Sui 授权与 ADB 侧通道作为替代开启方式（需用户自行通过 ADB 授权 Shizuku）。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测 AccessibilityConsentActivity 入栈（透明主题 + excludeFromRecents 特征）或 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间；触发前需先模拟点击 DisplayDetailFragment 的触控板按钮或 OverviewFragment 的无障碍卡片，冷启动无诱导页面可抓。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。全链路为原生 Dialog + 系统设置跳转，文本可被 UTG 直接提取；唯一需注意的旁路是 Shizuku/Sui 已授权时 startServiceByShizuku 会通过 WRITE_SECURE_SETTINGS 直接写入 enabled_accessibility_services 与 accessibility_enabled=1，从而不出现系统无障碍页面（此时 UTG 应改抓 Settings.Secure 写入与 TouchpadAccessibilityService.onServiceConnected 回调作为获权证据）；该路径受 accessibility_consent 标记门控且依赖用户事先主动通过 ADB/root 授权 Shizuku。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动主界面（基线页）** | io.github.jqssun.displayextend.MainActivity + BottomNavigationView + OverviewFragment 权限卡片 | 确认冷启动不存在任何无障碍诱导弹窗或强制跳设置，是区分"按需申请"与"冷启动 0 步劫持"的关键基线 | 无任何 Dialog 节点；无障碍行显示 Optional/Required 状态文案而非强制弹窗；无跳到系统设置页的 Activity 切换 |
| **授权说明对话框页** | AccessibilityConsentActivity 内的 MaterialAlertDialog：标题 Enable accessibility access，按钮 Enable / Not now | 该页是唯一引导文案载体，可判定是否可取消、是否含恐吓/假更新/教唆忽略警告话术、是否承诺隐私 | 存在 Not now 可点击节点（可取消）；正文含 "never collected, stored, or shared" 隐私承诺；无 LURE_* 类恐吓或假更新文案；对话框之外无遮罩层 |
| **系统无障碍服务列表项** | 系统设置 > 无障碍 > 已下载的服务，条目名 Extend，描述 Accessibility service for simulating touch events on secondary screens | 核对应用名、服务标签与描述是否一致、是否存在空白挤出/同形字伪装，以及是否为高仿页面 | 包名 io.github.jqssun.displayextend 与条目一致；描述文本与 strings 完全一致无异常空白/换行；页面包名为 com.android.settings（非应用自身绘制） |
| **拒绝返回后的降级页** | 返回 MainActivity/DisplayDetailFragment，无障碍状态文案更新 | 验证不存在拒权死循环重跳或定时器强拉，是良性降级与诱导攻击的分界点 | 返回后停留应用内而非立刻再次进入 ACCESSIBILITY_SETTINGS；无周期性 Activity 重入事件；状态文本变为 Required/Optional 提示 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `io.github.jqssun.displayextend.AccessibilityConsentActivity#onCreate`
- `io.github.jqssun.displayextend.AccessibilityConsentActivity$$ExternalSyntheticLambda0#onClick`
- `io.github.jqssun.displayextend.TouchpadAccessibilityService#ensureServiceAvailable`
- `io.github.jqssun.displayextend.TouchpadAccessibilityService#startServiceByShizuku`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml（accessibility_consent_title / _message / _agree / _decline / accessibility_service_description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 一、结论要点

**定性：良性透明授权流程，未发现诱导/欺诈性无障碍权限获取行为。** 静态可见性完整（无加壳、无加密载荷、无远端 HTML），全链路均为原生代码。

**实际路径（按运行期 UTG 视角）**

1. **冷启动无任何弹窗**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:io.github.jqssun.displayextend.MainActivity#onCreate>) 只做 EdgeToEdge、NavHost、DisplayManager/InputManager 注册，**不检查无障碍状态、不弹窗、不跳设置**；`onResume` 也不跳转。冷启动 0 步诱导不成立。
2. **按需触发**：只有在用户点"触控板 / 悬浮返回键 / 概览页无障碍卡片"时才进入授权链，例如 [DisplayDetailFragment$$ExternalSyntheticLambda5.onClick()](<resource-unit:#1.dex1 code:io.github.jqssun.displayextend.DisplayDetailFragment$$ExternalSyntheticLambda5#onClick>) case 2、[OverviewFragment$$ExternalSyntheticLambda1.onClick()](<resource-unit:#1.dex1 code:io.github.jqssun.displayextend.OverviewFragment$$ExternalSyntheticLambda1#onClick>) case 1、[FloatingButtonService.startFloating()](<resource-unit:#1.dex1 code:io.github.jqssun.displayextend.FloatingButtonService#startFloating>)。
3. **统一收口函数** [TouchpadAccessibilityService.ensureServiceAvailable()](<resource-unit:#1.dex1 code:io.github.jqssun.displayextend.TouchpadAccessibilityService#ensureServiceAvailable>)：已启用→直接 startService；未启用且无同意标记→拉起 `AccessibilityConsentActivity`；否则若 Sui/Shizuku 已授权→`startServiceByShizuku` 直接写 Secure 设置；最后才 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。
4. **同意弹窗**：[AccessibilityConsentActivity.onCreate()](<resource-unit:#1.dex1 code:io.github.jqssun.displayextend.AccessibilityConsentActivity#onCreate>) 用 MaterialAlertDialog 展示"Enable accessibility access"+"Enable"/"Not now"，**`mCancelable = false` 但保留明确的"Not now"拒绝按钮**；点"Not now"仅 `finish()`，无重跳、无死循环。点"Enable"写 `accessibility_consent=true` 后继续流程。
5. **无 APPLICATION_DETAILS_SETTINGS 跳转、无 13+ 受限设置分步教学、无 overlay 遮罩指引、无 GLOBAL_ACTION_BACK 防撤权**：全包搜索 `APPLICATION_DETAILS_SETTINGS`、`GLOBAL_ACTION_BACK` 均 `no_matches`；`onAccessibilityEvent` 为空实现，无事件监听自保。
6. **唯一需注意的实现细节（非恶意）**：`startServiceByShizuku` 在用户已授予 Shizuku/Sui 权限时会通过 `WRITE_SECURE_SETTINGS` 直接写入 `enabled_accessibility_services` 与 `accessibility_enabled=1`，跳过系统设置页。该能力依赖用户事先主动通过 ADB/root 授权 Shizuku，且被 `accessibility_consent` 标记门控，属常规开源方案，不构成静默越权。

**文案性质**：弹窗正文完整披露"模拟导航手势、绘制光标、读取窗口详情以定向输入"，并明确"仅在本机使用、绝不收集/存储/共享"，属**良性透明说明**；无障碍 `android:description` 与 UI 状态文案一致，无身份伪装、无空白挤出警告、无 `isAccessibilityTool` 伪造。

## 二、UTG 抓取建议（要点）

- 最佳触发点：点击"触控板/悬浮键"瞬间，或监测到 `AccessibilityConsentActivity` 入栈（透明主题、`excludeFromRecents`）；其次是 `ACTION_ACCESSIBILITY_SETTINGS` 跳转事件。
- 关键页面：同意 Dialog（判别是否可取消/是否恐吓文案）→ 系统无障碍服务列表项（判别标签/描述是否一致）→ 返回应用后的状态刷新（判别是否死循环重跳）。
- 盲区：无。无纯图引导、无远端 HTML、无 Dropper。

## 三、结构化结果

```json
{
  "static_visibility": "clear",
  "visibility_note": "全链路静态完整可见：授权入口为原生 AccessibilityConsentActivity + MaterialAlertDialog，跳转为硬编码 android.settings.ACCESSIBILITY_SETTINGS；无加壳（apkid/预筛 packed=False）、无 AES/加密载荷、无 assets 内 HTML、无远端 WebView、无动态加载 DEX/SO。",
  "summary_one_liner": "Extend 在用户主动使用触控板/悬浮返回键时才弹出可拒绝的原生说明对话框，明示模拟手势与读取窗口用途及本地处理承诺，同意后跳系统无障碍设置（或在已授权 Shizuku 时直接写入 Secure 设置），无冷启动诱导、无死循环、无遮罩伪装。",
  "disguise_identity": {
    "app_display_name": "Extend",
    "claimed_brand_or_persona": "Extend（F-Droid 开源，io.github.jqssun.displayextend，与 io.github.jqssun.displaymirror 同作者生态）",
    "a11y_service_label": "Extend（服务未声明 android:label，系统无障碍列表回退显示应用名；描述为 Accessibility service for simulating touch events on secondary screens）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅 R8 混淆（类名/资源 ID 混淆属常规构建），无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool（搜索 no_matches）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "io.github.jqssun.displayextend.MainActivity（NavHost + BottomNavigationView，默认进入 OverviewFragment）",
      "trigger_event": "LAUNCHER 图标点击 → MainActivity.onCreate / onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（冷启动不弹任何权限或引导对话框）",
      "shown_text_zh": "冷启动仅展示主界面与底部导航，不做无障碍权限提示",
      "user_action_requested": "无强制动作；用户可自由浏览",
      "code_anchor": "io.github.jqssun.displayextend.MainActivity#onCreate / #onResume"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "DisplayDetailFragment / OverviewFragment 的\"触控板\"\"悬浮返回键\"按钮与无障碍状态卡片；FloatingButtonService.startFloating；job.StartTouchPad",
      "trigger_event": "用户点击触控板按钮（case 2）或无障碍卡片（case 1）→ 调用 ensureServiceAvailable(context, true)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility / Optional; only needed for popup and system surfaces on external displays",
      "shown_text_zh": "概览页\"无障碍\"一行显示未启用状态，并提示该权限对外接显示器上的弹窗与系统界面为可选/必需",
      "user_action_requested": "用户主动点击触控板或无障碍状态按钮，才进入授权流程",
      "code_anchor": "io.github.jqssun.displayextend.DisplayDetailFragment$$ExternalSyntheticLambda5#onClick; io.github.jqssun.displayextend.OverviewFragment#_updateAccessibilityStatus"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "io.github.jqssun.displayextend.AccessibilityConsentActivity（@style/AppTheme.Transparent，excludeFromRecents=true）内的 MaterialAlertDialog",
      "trigger_event": "ensureServiceAvailable 检测到 accessibility_consent 未置位 → startActivity(AccessibilityConsentActivity)（FLAG_ACTIVITY_NEW_TASK）→ onCreate 直接 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable accessibility access / Extend uses the Accessibility Service to operate your external displays: it simulates navigation actions for the on-screen touchpad and floating button, draws the on-screen cursor, and reads window details to direct your input to the focused window on the correct display. This information is used only on your device and is never collected, stored, or shared. Would you like to enable Accessibility Service? / Enable / Not now",
      "shown_text_zh": "标题\"开启无障碍权限\"；正文说明 Extend 使用无障碍服务操作外接显示器：为屏幕触控板与悬浮按钮模拟导航动作、绘制屏幕光标、读取窗口详情以把输入定向到正确显示器上的焦点窗口；这些信息仅在本机使用，绝不收集、存储或共享；询问是否开启无障碍服务。按钮为\"开启\"与\"暂不\"。",
      "user_action_requested": "选择\"Enable\"进入系统无障碍设置（或经 Shizuku 直接开启），或选择\"Not now\"放弃；对话框 mCancelable=false，但保留明确可点的拒绝按钮",
      "code_anchor": "io.github.jqssun.displayextend.AccessibilityConsentActivity#onCreate; res/values/strings.xml (accessibility_consent_title/message/agree/decline)"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（服务列表项：Extend / Accessibility service for simulating touch events on secondary screens）",
      "trigger_event": "点击\"Enable\" → 写 accessibility_consent=true → ensureServiceAvailable(context, true) → 无 Shizuku 权限且服务未启用 → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))，随后 finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility service for simulating touch events on secondary screens",
      "shown_text_zh": "系统无障碍服务列表中该服务描述为\"用于在副屏模拟触摸事件的无障碍服务\"",
      "user_action_requested": "用户在系统页面手动打开 Extend 的无障碍开关（无任何教唆忽略系统警告的文案，无跳转应用详情页开启受限设置的步骤）",
      "code_anchor": "io.github.jqssun.displayextend.TouchpadAccessibilityService#ensureServiceAvailable; res/xml/accessibility_service_config.xml"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "AccessibilityConsentActivity 关闭后回到原页面；MainActivity.onResume / OverviewFragment 状态刷新",
      "trigger_event": "点\"Not now\" → AccessibilityConsentActivity$$ExternalSyntheticLambda0.onClick(default 分支) → finish()；返回后 onResume → State.refreshUI → _updateAccessibilityStatus 仅更新文案",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility / Required for controlling popup and system surfaces on external displays",
      "shown_text_zh": "拒绝后停留在原页面，无障碍状态仍显示未启用并标注该权限对弹窗/系统界面为必需，功能优雅降级，不重复拉起",
      "user_action_requested": "无强制动作；用户可继续使用其他功能，需要时再次手动点击",
      "code_anchor": "io.github.jqssun.displayextend.AccessibilityConsentActivity$$ExternalSyntheticLambda0#onClick; io.github.jqssun.displayextend.OverviewFragment#_updateAccessibilityStatus"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "TouchpadAccessibilityService（onServiceConnected 仅置 instance、写日志、刷新 UI）；或 Shizuku 分支写入 Settings.Secure",
      "trigger_event": "系统回调 onServiceConnected，或 ensureServiceAvailable 中 Sui.hasPermission() 为真时调用 startServiceByShizuku 写 enabled_accessibility_services / accessibility_enabled=1",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Enabled",
      "shown_text_zh": "获权后无障碍状态显示\"已启用\"，授权按钮隐藏；服务不监听任何无障碍事件（onAccessibilityEvent 为空实现）",
      "user_action_requested": "无（不自动确认、不阻止用户撤销权限）",
      "code_anchor": "io.github.jqssun.displayextend.TouchpadAccessibilityService#onServiceConnected; io.github.jqssun.displayextend.TouchpadAccessibilityService#startServiceByShizuku"
    }
  ],
  "text_presentation_locations": [
    "AccessibilityConsentActivity 内的 MaterialAlertDialog（标题 accessibility_consent_title、正文 accessibility_consent_message、按钮 accessibility_consent_agree/decline），透明主题 Activity，不可点外部/返回键取消但含 Not now 按钮",
    "系统无障碍服务列表项描述：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description（\"Accessibility service for simulating touch events on secondary screens\"），服务本身未声明 android:label，回退显示应用名 Extend",
    "概览页（OverviewFragment）权限卡片与无障碍行：accessibility_permission_status / accessibility_status_enabled / accessibility_status_optional_for_touchpad_surfaces / accessibility_status_required_for_touchpad_surfaces / permissions_granted(_detail) / permissions_not_granted(_detail)",
    "设置页开关项说明：touchpad_accessibility_overlay_desc、floating_button_desc、accessibility_consent 相关设置项文本",
    "无 assets HTML、无 WebView、无悬浮窗遮罩、无高仿系统设置页承载任何引导文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable accessibility access",
      "text_zh": "开启无障碍权限",
      "source_location": "res/values/strings.xml: accessibility_consent_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Extend uses the Accessibility Service to operate your external displays: it simulates navigation actions for the on-screen touchpad and floating button, draws the on-screen cursor, and reads window details to direct your input to the focused window on the correct display. This information is used only on your device and is never collected, stored, or shared. Would you like to enable Accessibility Service?",
      "text_zh": "Extend 使用无障碍服务来操作您的外接显示器：它为屏幕触控板和悬浮按钮模拟导航动作、绘制屏幕光标，并读取窗口详情以把您的输入定向到正确显示器上的焦点窗口。这些信息仅在本机使用，绝不收集、存储或共享。是否开启无障碍服务？",
      "source_location": "res/values/strings.xml: accessibility_consent_message",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable",
      "text_zh": "开启",
      "source_location": "res/values/strings.xml: accessibility_consent_agree",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Not now",
      "text_zh": "暂不",
      "source_location": "res/values/strings.xml: accessibility_consent_decline",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service for simulating touch events on secondary screens",
      "text_zh": "用于在副屏模拟触摸事件的无障碍服务",
      "source_location": "res/values/strings.xml: accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Required for controlling popup and system surfaces on external displays",
      "text_zh": "控制外接显示器上的弹窗与系统界面所必需",
      "source_location": "res/values/strings.xml: accessibility_status_required_for_touchpad_surfaces",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Optional; only needed for popup and system surfaces on external displays",
      "text_zh": "可选；仅外接显示器上的弹窗与系统界面需要",
      "source_location": "res/values/strings.xml: accessibility_status_optional_for_touchpad_surfaces",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。点 Not now 仅 finish() 并留在原页面，无障碍状态行更新为未启用提示，无 onResume 重跳、无定时器拉起、无倒计时强制；用户可继续使用其他功能。",
    "overlay_or_fake_settings": "无。不叠放半透明遮罩、不建全屏悬浮引导窗、无高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于触控板/悬浮返回键本身的功能实现，与授权引导无关。",
    "restricted_settings_13plus_coaching": "无。全包搜索 APPLICATION_DETAILS_SETTINGS 无命中，不教用户进应用详情页开启受限设置，也无 Session 安装器绕过。",
    "post_grant_anti_removal": "无。onAccessibilityEvent 为空实现，不监听设置页；未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权，不自动点确认。",
    "benign_graceful_degradation": "有。无障碍为可选能力：概览页明确区分\"可选\"与\"必需\"两种场景；未授权时触控板/悬浮键相关路径仅提示并可继续使用其他显示管理功能；另有 Shizuku/Sui 授权与 ADB 侧通道作为替代开启方式（需用户自行通过 ADB 授权 Shizuku）。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测 AccessibilityConsentActivity 入栈（透明主题 + excludeFromRecents 特征）或 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间；触发前需先模拟点击 DisplayDetailFragment 的触控板按钮或 OverviewFragment 的无障碍卡片，冷启动无诱导页面可抓。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动主界面（基线页）",
        "page_identifier": "io.github.jqssun.displayextend.MainActivity + BottomNavigationView + OverviewFragment 权限卡片",
        "why_most_useful": "确认冷启动不存在任何无障碍诱导弹窗或强制跳设置，是区分\"按需申请\"与\"冷启动 0 步劫持\"的关键基线",
        "observable_utg_signals": ["无任何 Dialog 节点", "无障碍行显示 Optional/Required 状态文案而非强制弹窗", "无跳到系统设置页的 Activity 切换"]
      },
      {
        "page_role": "授权说明对话框页",
        "page_identifier": "AccessibilityConsentActivity 内的 MaterialAlertDialog：标题 Enable accessibility access，按钮 Enable / Not now",
        "why_most_useful": "该页是唯一引导文案载体，可判定是否可取消、是否含恐吓/假更新/教唆忽略警告话术、是否承诺隐私",
        "observable_utg_signals": ["存在 Not now 可点击节点（可取消）", "正文含 \"never collected, stored, or shared\" 隐私承诺", "无 LURE_* 类恐吓或假更新文案", "对话框之外无遮罩层"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 > 无障碍 > 已下载的服务，条目名 Extend，描述 Accessibility service for simulating touch events on secondary screens",
        "why_most_useful": "核对应用名、服务标签与描述是否一致、是否存在空白挤出/同形字伪装，以及是否为高仿页面",
        "observable_utg_signals": ["包名 io.github.jqssun.displayextend 与条目一致", "描述文本与 strings 完全一致无异常空白/换行", "页面包名为 com.android.settings（非应用自身绘制）"]
      },
      {
        "page_role": "拒绝返回后的降级页",
        "page_identifier": "返回 MainActivity/DisplayDetailFragment，无障碍状态文案更新",
        "why_most_useful": "验证不存在拒权死循环重跳或定时器强拉，是良性降级与诱导攻击的分界点",
        "observable_utg_signals": ["返回后停留应用内而非立刻再次进入 ACCESSIBILITY_SETTINGS", "无周期性 Activity 重入事件", "状态文本变为 Required/Optional 提示"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。全链路为原生 Dialog + 系统设置跳转，文本可被 UTG 直接提取；唯一需注意的旁路是 Shizuku/Sui 已授权时 startServiceByShizuku 会通过 WRITE_SECURE_SETTINGS 直接写入 enabled_accessibility_services 与 accessibility_enabled=1，从而不出现系统无障碍页面（此时 UTG 应改抓 Settings.Secure 写入与 TouchpadAccessibilityService.onServiceConnected 回调作为获权证据）；该路径受 accessibility_consent 标记门控且依赖用户事先主动通过 ADB/root 授权 Shizuku。"
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
    "io.github.jqssun.displayextend.AccessibilityConsentActivity#onCreate",
    "io.github.jqssun.displayextend.AccessibilityConsentActivity$$ExternalSyntheticLambda0#onClick",
    "io.github.jqssun.displayextend.TouchpadAccessibilityService#ensureServiceAvailable",
    "io.github.jqssun.displayextend.TouchpadAccessibilityService#startServiceByShizuku",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml（accessibility_consent_title / _message / _agree / _decline / accessibility_service_description）"
  ]
}
```

**风险台账**：未发现可单独判定、定级的恶意/违规命题，故未写入 `record_risk`。分析边界：`SYSTEM_ALERT_WINDOW` 仅服务于触控板与悬浮返回键功能，`WRITE_SECURE_SETTINGS` 仅在 Shizuku/Sui 已被用户授权时用于开启无障碍，二者均未用于规避检测或阻止撤权。

</details>
