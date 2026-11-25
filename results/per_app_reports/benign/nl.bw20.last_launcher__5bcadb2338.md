# BN_040__5bcadb2338｜极简桌面与双击锁屏 — Last Launcher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：173.9s

## 1. 一句话核心结论

- **核心申请方式**：极简桌面在设置页以『双击锁屏』为唯一目的按需展示说明并跳转系统原生无障碍设置页，服务仅调用 GLOBAL_ACTION_LOCK_SCREEN，无遮罩、无循环、无伪装。
- **静态可见性说明**：无加壳、无加密载荷、无远端HTML；引导逻辑由 Flutter AOT 字符串表（libapp.so 内 l10n 文本）与 Java 侧 MethodChannel 分发器 W0.c#h 完整暴露。唯一限制：APK 仅含 lib/x86_64/libapp.so，Blutter 需 arm64 故未做 Dart 函数级反编译，但字符串与通道分支已足以还原全流程。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5bcadb23383c09896d2e3e2db272491329ce57a7d323ea1877cc3f8a7b4e7cf1` |
| 包名 / 年份 | `nl.bw20.last_launcher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/nl.bw20.last_launcher_213.apk |
| 桌面显示名 | Last Launcher |
| 引导页宣称品牌/身份 | Last Launcher（F-Droid 开源极简文本桌面，真实身份） |
| 系统无障碍列表服务名 | Last Launcher（系统无障碍列表显示 android:label，说明为 'Allows Last Launcher to lock the screen on double tap.'） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `nl.bw20.last_launcher.LockAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Allows Last Launcher to lock the screen on double tap. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | nl.bw20.last_launcher.MainActivity（Flutter 引擎承载，LAUNCHER + HOME intent-filter） | onCreate / HOME 启动，Flutter 首帧渲染桌面 | 原生Activity | 无 | 无需任何操作（无弹窗、无遮罩） | `AndroidManifest.xml application/activity MainActivity；libapp.so strings 'package:last_launcher/main.dart'` |
| 2 | 业务功能触发 | 桌面手势层（features/home/shell_gestures.dart）与提示文案 hints.dart | 用户在桌面双击空白区域（doubleTap） | 原生Activity | **原文**：Double tap to sleep<br>**译注**：双击休眠 | 提示该手势功能，未开启服务时功能不可用（不阻塞其他桌面功能） | `libapp.so strings: 'Double tap to sleep' / 'init:doubleTapToSleep' / 'package:last_launcher/shared/data/hints.dart'` |
| 3 | 引导说明页 | SettingsScreen 中的无障碍开关项（features/settings/screens/settings_screen.dart） | 用户主动进入设置页并点击 'Turn on accessibility service' 项 | 原生Activity | **原文**：Turn on accessibility service / This uses the AccessibilityService API to lock the screen when you double-tap. It does nothing else. You will be redirected to system settings to turn it on.<br>**译注**：开启无障碍服务 / 这会使用 AccessibilityService API，在你双击时锁定屏幕，不做任何其他事情。你将被带到系统设置中开启它。 | 用户可点击进入系统设置，也可直接返回放弃；无强制、无倒计时 | `libapp.so strings 'Turn on accessibility service'、'This uses the AccessibilityService API to lock the screen when you double-tap. It does nothing else. You will be redirected to system settings to turn it on.'；zh 文本 '这会使用 AccessibilityService API，在你双击时锁定屏幕，不做任何其他事情。你将被带到系统设置中开启它。'` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS） | MethodChannel 方法 openAccessibilitySettings 被调用，且 LockAccessibilityService.e == null（服务未启用） | 系统无障碍页 | **原文**：无（跳转系统原生页面，应用不自绘任何设置界面）<br>**译注**：直接拉起系统无障碍设置列表，由用户在系统页面内手动为 Last Launcher 打开开关 | 用户在系统页手动开启 Last Launcher 的无障碍开关；可随时返回，应用不做拦截 | `W0.c#h 分支 L7c5/L7cf：new Intent("android.settings.ACCESSIBILITY_SETTINGS") + startActivity` |
| 5 | 拒权反馈循环 | 设置页无障碍项的状态显示 | 用户返回后 isAccessibilityServiceEnabled 判定仍为 false | 原生Activity | **原文**：Requires accessibility service enabled in system settings / 需要在系统设置中启用无障碍服务<br>**译注**：需要在系统设置中启用无障碍服务 | 仅静态提示；无 onResume 死循环重跳、无 Timer 轮询拉起、无悬浮遮罩施压 | `libapp.so strings 'Requires accessibility service enabled in system settings'、'需要在系统设置中启用无障碍服务'、'isAccessibilityServiceEnabled'、'Failed to check accessibility service: '` |
| 6 | 获权后动作 | nl.bw20.last_launcher.LockAccessibilityService + 桌面双击手势 | 系统绑定服务触发 onServiceConnected；此后用户双击桌面 → MethodChannel 'lockScreen' | 原生Activity | 无 | 无额外授权动作；用户可在系统设置随时关闭该服务 | `nl.bw20.last_launcher.LockAccessibilityService#onServiceConnected、#onAccessibilityEvent；W0.c#h 分支 L23a/L244 lockScreen → performGlobalAction(8)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项说明：res/xml/accessibility_service_config.xml 的 android:description → res/values/strings.xml#accessibility_service_description（'Allows Last Launcher to lock the screen on double tap.'，多语言 values-* 同 key）
- 设置页无障碍开关项标题：Flutter l10n 字符串 'Turn on accessibility service'（package:last_launcher/features/settings/screens/settings_screen.dart 渲染）
- 设置页/说明文案正文：Flutter l10n 字符串 'This uses the AccessibilityService API to lock the screen when you double-tap. It does nothing else. You will be redirected to system settings to turn it on.' 及中文对应文本（libapp.so 内 UTF-8 与 UTF-16 双份）
- 未开启时的状态提示：'Requires accessibility service enabled in system settings' / '需要在系统设置中启用无障碍服务'
- 桌面手势提示文案：'Double tap to sleep' / '双击休眠'（hints.dart）
- 跳转目标为系统原生 android.settings.ACCESSIBILITY_SETTINGS 页面，应用内不存在自绘设置页、WebView 教学页或悬浮引导层

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Allows Last Launcher to lock the screen on double tap. | 允许 Last Launcher 在双击时锁定屏幕。 | `res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）` | 良性透明说明 |
| en | This uses the AccessibilityService API to lock the screen when you double-tap. It does nothing else. You will be redirected to system settings to turn it on. | 这会使用 AccessibilityService API，在你双击时锁定屏幕，不做任何其他事情。你将被带到系统设置中开启它。 | `lib/x86_64/libapp.so 字符串表（Flutter l10n，settings_screen 相关）` | 良性透明说明 |
| zh | 这会使用 AccessibilityService API，在你双击时锁定屏幕，不做任何其他事情。你将被带到系统设置中开启它。 | 同原文（中文版说明） | `lib/x86_64/libapp.so 字符串表（UTF-16LE 编码的 zh 本地化文本）` | 良性透明说明 |
| en | Turn on accessibility service | 开启无障碍服务 | `lib/x86_64/libapp.so 字符串表（设置页开关项标题）` | 良性透明说明 |
| en | Requires accessibility service enabled in system settings | 需要在系统设置中启用无障碍服务 | `lib/x86_64/libapp.so 字符串表（未启用状态提示）` | 良性透明说明 |
| zh | 需要在系统设置中启用无障碍服务 | 同原文（中文版状态提示） | `lib/x86_64/libapp.so 字符串表（UTF-16LE 编码）` | 良性透明说明 |
| en | Double tap to sleep | 双击休眠 | `lib/x86_64/libapp.so 字符串表（桌面手势提示）` | 良性透明说明 |
| zh | 双击休眠 | 同原文（中文版手势提示） | `lib/x86_64/libapp.so 字符串表（UTF-16LE 编码）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。返回系统设置后仅由 isAccessibilityServiceEnabled 重新读取状态并显示静态提示 'Requires accessibility service enabled in system settings'；不存在 onResume 死循环重跳、Timer 轮询拉起或不可取消弹窗。
- **遮罩叠层 / 高仿系统设置页**：无。跳转目标为系统原生 android.settings.ACCESSIBILITY_SETTINGS；应用未使用 TYPE_APPLICATION_OVERLAY / SYSTEM_ALERT_WINDOW（Manifest 无该权限），无遮罩叠层、无高仿系统开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。虽存在 android.settings.APPLICATION_DETAILS_SETTINGS 通道（openOwnAppInfo 分支），但用于跳转自身应用详情，未出现引导用户点右上角菜单开启『受限设置』的教学文案或流程。
- **获权后即时行为与防撤权机制**：无。服务不监听设置页，不使用 GLOBAL_ACTION_BACK/HOME 阻止撤权，也不自点确认；获权后仅保留静态引用供 lockScreen 调用。
- **良性降级 / 替代方案**：仅影响『双击锁屏』这一附加手势，桌面启动器主功能（应用抽屉、搜索、隐藏应用、任务模块）完全不受影响；未开启时功能入口保持可用但动作返回 false，不做强制阻断。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（由 MethodChannel 方法名 openAccessibilitySettings 触发）时拉起 UTG；或用户进入设置页点击 'Turn on accessibility service' 项时同步录制。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一注意点：APK 仅打包 x86_64 libapp.so，若检测环境仅支持 arm64 动态运行可能无法直接启动该包；另外 Flutter 文本位于 AOT 字符串表而非 strings.xml，纯资源层扫描会漏掉引导文案，需结合运行期 UTG 或 libapp.so 字符串抽取。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前的设置页无障碍开关项与说明文案** | Flutter 设置页中文本为 'Turn on accessibility service' 的列表项及其下方说明段落 | 该页是唯一的说服环节，可直接判断说明是否与真实能力（仅锁屏）一致、是否存在夸大或功能错配 | 列表项文本 'Turn on accessibility service'；说明正文 'This uses the AccessibilityService API ... It does nothing else.'；无倒计时/无强制遮罩（页面可正常返回） |
| **系统无障碍服务列表项** | Settings → Accessibility 列表中 'Last Launcher' 条目及其描述文本 | 核验 android:description 是否被改写、服务名是否与显示名一致、是否为空白/同形字伪装 | 条目名称 'Last Launcher'；描述 'Allows Last Launcher to lock the screen on double tap.'；开关初始为关闭 |
| **返回后未授权状态提示** | 从系统设置返回设置页时的提示 'Requires accessibility service enabled in system settings' | 区分良性降级与拒权施压：确认无自动重跳、无定时轮询、无悬浮遮罩 | 静态提示文本一次出现；页面未被自动重新拉起（无重复 Activity 栈）；无悬浮窗/遮罩层 |
| **获权后双击锁屏动作** | 桌面双击后屏幕立即熄灭（系统锁屏） | 确认无障碍能力仅用于锁屏，未伴随读屏、自动点击等越权行为 | 双击后进入系统 Keyguard；无障碍事件流中无窗口内容抓取；无其他应用被自动操作 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `nl.bw20.last_launcher.LockAccessibilityService#onServiceConnected`
- `nl.bw20.last_launcher.LockAccessibilityService#onAccessibilityEvent`
- `W0.c#h`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml#accessibility_service_description`
- `package:last_launcher/features/settings/screens/settings_screen.dart`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**判定：良性、透明的无障碍申请流程，未发现诱导、遮罩或拒权循环。**

- **服务端能力极小**：[LockAccessibilityService](<resource-unit:#1.dex1 code:nl.bw20.last_launcher.LockAccessibilityService#onServiceConnected>) 的 `onServiceConnected()` 只把静态引用 `e = this` 保存下来；`onAccessibilityEvent()` 和 `onInterrupt()` 都是空实现，而且配置声明 `canRetrieveWindowContent="false"`、`canPerformGestures="false"`，因此它无法读取屏幕内容，也无法模拟点击。唯一的动作是 `lockScreen` 分支中的 `performGlobalAction(8)`（对应 `GLOBAL_ACTION_LOCK_SCREEN`，要求 SDK≥28），这正对应“双击锁屏”。
- **权限申请时机是按需触发**：只有在用户于设置页主动点击 `Turn on accessibility service` 时，`openAccessibilitySettings` 分支才会执行 `startActivity(ACTION_ACCESSIBILITY_SETTINGS)`，而且仅当服务尚未启用（`LockAccessibilityService.e == null`）时才会跳转，见 [W0.c#h](<resource-unit:#1.dex1 code:W0.c#h>)。冷启动时既不弹窗，也不轮询，更不会在 `onResume` 时反复重跳。
- **说明文案与功能一致**：`This uses the AccessibilityService API to lock the screen when you double-tap. It does nothing else. You will be redirected to system settings to turn it on.` 以及中文版“这会使用 AccessibilityService API，在你双击时锁定屏幕，不做任何其他事情。你将被带到系统设置中开启它。”都属于良性透明说明；未开启时只给出静态提示 `Requires accessibility service enabled in system settings`（中文：“需要在系统设置中启用无障碍服务”），并没有强制循环。
- **没有伪装**：显示名 `Last Launcher` 与服务说明 `Allows Last Launcher to lock the screen on double tap.`（[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>)）一致，不存在空白或同形字伪装，也没有伪造 `isAccessibilityTool`、没有多 alias，并且只使用系统原生的无障碍列表页。
- **限制边界**：应用仅打包 `x86_64` 架构的 libapp.so（Blutter 只支持 arm64），Dart 层无法反编译，但 Flutter 字符串表以及 Java 通道的分支逻辑足以确认全部流程；没有加壳，也没有远端 HTML 或二阶段载荷（`assets/flutter_assets` 中仅包含字体、shader 和 NOTICES）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无加壳、无加密载荷、无远端HTML；引导逻辑由 Flutter AOT 字符串表（libapp.so 内 l10n 文本）与 Java 侧 MethodChannel 分发器 W0.c#h 完整暴露。唯一限制：APK 仅含 lib/x86_64/libapp.so，Blutter 需 arm64 故未做 Dart 函数级反编译，但字符串与通道分支已足以还原全流程。",
  "summary_one_liner": "极简桌面在设置页以『双击锁屏』为唯一目的按需展示说明并跳转系统原生无障碍设置页，服务仅调用 GLOBAL_ACTION_LOCK_SCREEN，无遮罩、无循环、无伪装。",
  "disguise_identity": {
    "app_display_name": "Last Launcher",
    "claimed_brand_or_persona": "Last Launcher（F-Droid 开源极简文本桌面，真实身份）",
    "a11y_service_label": "Last Launcher（系统无障碍列表显示 android:label，说明为 'Allows Last Launcher to lock the screen on double tap.'）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "nl.bw20.last_launcher.MainActivity（Flutter 引擎承载，LAUNCHER + HOME intent-filter）",
      "trigger_event": "onCreate / HOME 启动，Flutter 首帧渲染桌面",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动不弹出任何无障碍引导、不请求无障碍权限",
      "user_action_requested": "无需任何操作（无弹窗、无遮罩）",
      "code_anchor": "AndroidManifest.xml application/activity MainActivity；libapp.so strings 'package:last_launcher/main.dart'"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "桌面手势层（features/home/shell_gestures.dart）与提示文案 hints.dart",
      "trigger_event": "用户在桌面双击空白区域（doubleTap）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Double tap to sleep",
      "shown_text_zh": "双击休眠",
      "user_action_requested": "提示该手势功能，未开启服务时功能不可用（不阻塞其他桌面功能）",
      "code_anchor": "libapp.so strings: 'Double tap to sleep' / 'init:doubleTapToSleep' / 'package:last_launcher/shared/data/hints.dart'"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "SettingsScreen 中的无障碍开关项（features/settings/screens/settings_screen.dart）",
      "trigger_event": "用户主动进入设置页并点击 'Turn on accessibility service' 项",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Turn on accessibility service / This uses the AccessibilityService API to lock the screen when you double-tap. It does nothing else. You will be redirected to system settings to turn it on.",
      "shown_text_zh": "开启无障碍服务 / 这会使用 AccessibilityService API，在你双击时锁定屏幕，不做任何其他事情。你将被带到系统设置中开启它。",
      "user_action_requested": "用户可点击进入系统设置，也可直接返回放弃；无强制、无倒计时",
      "code_anchor": "libapp.so strings 'Turn on accessibility service'、'This uses the AccessibilityService API to lock the screen when you double-tap. It does nothing else. You will be redirected to system settings to turn it on.'；zh 文本 '这会使用 AccessibilityService API，在你双击时锁定屏幕，不做任何其他事情。你将被带到系统设置中开启它。'"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "MethodChannel 方法 openAccessibilitySettings 被调用，且 LockAccessibilityService.e == null（服务未启用）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转系统原生页面，应用不自绘任何设置界面）",
      "shown_text_zh": "直接拉起系统无障碍设置列表，由用户在系统页面内手动为 Last Launcher 打开开关",
      "user_action_requested": "用户在系统页手动开启 Last Launcher 的无障碍开关；可随时返回，应用不做拦截",
      "code_anchor": "W0.c#h 分支 L7c5/L7cf：new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + startActivity"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "设置页无障碍项的状态显示",
      "trigger_event": "用户返回后 isAccessibilityServiceEnabled 判定仍为 false",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Requires accessibility service enabled in system settings / 需要在系统设置中启用无障碍服务",
      "shown_text_zh": "需要在系统设置中启用无障碍服务",
      "user_action_requested": "仅静态提示；无 onResume 死循环重跳、无 Timer 轮询拉起、无悬浮遮罩施压",
      "code_anchor": "libapp.so strings 'Requires accessibility service enabled in system settings'、'需要在系统设置中启用无障碍服务'、'isAccessibilityServiceEnabled'、'Failed to check accessibility service: '"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "nl.bw20.last_launcher.LockAccessibilityService + 桌面双击手势",
      "trigger_event": "系统绑定服务触发 onServiceConnected；此后用户双击桌面 → MethodChannel 'lockScreen'",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务仅保存静态引用；双击时执行 performGlobalAction(GLOBAL_ACTION_LOCK_SCREEN) 熄屏，不读取窗口内容、不注入点击、不自撤权防护",
      "user_action_requested": "无额外授权动作；用户可在系统设置随时关闭该服务",
      "code_anchor": "nl.bw20.last_launcher.LockAccessibilityService#onServiceConnected、#onAccessibilityEvent；W0.c#h 分支 L23a/L244 lockScreen → performGlobalAction(8)"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项说明：res/xml/accessibility_service_config.xml 的 android:description → res/values/strings.xml#accessibility_service_description（'Allows Last Launcher to lock the screen on double tap.'，多语言 values-* 同 key）",
    "设置页无障碍开关项标题：Flutter l10n 字符串 'Turn on accessibility service'（package:last_launcher/features/settings/screens/settings_screen.dart 渲染）",
    "设置页/说明文案正文：Flutter l10n 字符串 'This uses the AccessibilityService API to lock the screen when you double-tap. It does nothing else. You will be redirected to system settings to turn it on.' 及中文对应文本（libapp.so 内 UTF-8 与 UTF-16 双份）",
    "未开启时的状态提示：'Requires accessibility service enabled in system settings' / '需要在系统设置中启用无障碍服务'",
    "桌面手势提示文案：'Double tap to sleep' / '双击休眠'（hints.dart）",
    "跳转目标为系统原生 android.settings.ACCESSIBILITY_SETTINGS 页面，应用内不存在自绘设置页、WebView 教学页或悬浮引导层"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Allows Last Launcher to lock the screen on double tap.",
      "text_zh": "允许 Last Launcher 在双击时锁定屏幕。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This uses the AccessibilityService API to lock the screen when you double-tap. It does nothing else. You will be redirected to system settings to turn it on.",
      "text_zh": "这会使用 AccessibilityService API，在你双击时锁定屏幕，不做任何其他事情。你将被带到系统设置中开启它。",
      "source_location": "lib/x86_64/libapp.so 字符串表（Flutter l10n，settings_screen 相关）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "这会使用 AccessibilityService API，在你双击时锁定屏幕，不做任何其他事情。你将被带到系统设置中开启它。",
      "text_zh": "同原文（中文版说明）",
      "source_location": "lib/x86_64/libapp.so 字符串表（UTF-16LE 编码的 zh 本地化文本）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn on accessibility service",
      "text_zh": "开启无障碍服务",
      "source_location": "lib/x86_64/libapp.so 字符串表（设置页开关项标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Requires accessibility service enabled in system settings",
      "text_zh": "需要在系统设置中启用无障碍服务",
      "source_location": "lib/x86_64/libapp.so 字符串表（未启用状态提示）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "需要在系统设置中启用无障碍服务",
      "text_zh": "同原文（中文版状态提示）",
      "source_location": "lib/x86_64/libapp.so 字符串表（UTF-16LE 编码）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Double tap to sleep",
      "text_zh": "双击休眠",
      "source_location": "lib/x86_64/libapp.so 字符串表（桌面手势提示）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "双击休眠",
      "text_zh": "同原文（中文版手势提示）",
      "source_location": "lib/x86_64/libapp.so 字符串表（UTF-16LE 编码）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。返回系统设置后仅由 isAccessibilityServiceEnabled 重新读取状态并显示静态提示 'Requires accessibility service enabled in system settings'；不存在 onResume 死循环重跳、Timer 轮询拉起或不可取消弹窗。",
    "overlay_or_fake_settings": "无。跳转目标为系统原生 android.settings.ACCESSIBILITY_SETTINGS；应用未使用 TYPE_APPLICATION_OVERLAY / SYSTEM_ALERT_WINDOW（Manifest 无该权限），无遮罩叠层、无高仿系统开关页。",
    "restricted_settings_13plus_coaching": "无。虽存在 android.settings.APPLICATION_DETAILS_SETTINGS 通道（openOwnAppInfo 分支），但用于跳转自身应用详情，未出现引导用户点右上角菜单开启『受限设置』的教学文案或流程。",
    "post_grant_anti_removal": "无。服务不监听设置页，不使用 GLOBAL_ACTION_BACK/HOME 阻止撤权，也不自点确认；获权后仅保留静态引用供 lockScreen 调用。",
    "benign_graceful_degradation": "仅影响『双击锁屏』这一附加手势，桌面启动器主功能（应用抽屉、搜索、隐藏应用、任务模块）完全不受影响；未开启时功能入口保持可用但动作返回 false，不做强制阻断。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（由 MethodChannel 方法名 openAccessibilitySettings 触发）时拉起 UTG；或用户进入设置页点击 'Turn on accessibility service' 项时同步录制。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前的设置页无障碍开关项与说明文案",
        "page_identifier": "Flutter 设置页中文本为 'Turn on accessibility service' 的列表项及其下方说明段落",
        "why_most_useful": "该页是唯一的说服环节，可直接判断说明是否与真实能力（仅锁屏）一致、是否存在夸大或功能错配",
        "observable_utg_signals": ["列表项文本 'Turn on accessibility service'", "说明正文 'This uses the AccessibilityService API ... It does nothing else.'", "无倒计时/无强制遮罩（页面可正常返回）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility 列表中 'Last Launcher' 条目及其描述文本",
        "why_most_useful": "核验 android:description 是否被改写、服务名是否与显示名一致、是否为空白/同形字伪装",
        "observable_utg_signals": ["条目名称 'Last Launcher'", "描述 'Allows Last Launcher to lock the screen on double tap.'", "开关初始为关闭"]
      },
      {
        "page_role": "返回后未授权状态提示",
        "page_identifier": "从系统设置返回设置页时的提示 'Requires accessibility service enabled in system settings'",
        "why_most_useful": "区分良性降级与拒权施压：确认无自动重跳、无定时轮询、无悬浮遮罩",
        "observable_utg_signals": ["静态提示文本一次出现", "页面未被自动重新拉起（无重复 Activity 栈）", "无悬浮窗/遮罩层"]
      },
      {
        "page_role": "获权后双击锁屏动作",
        "page_identifier": "桌面双击后屏幕立即熄灭（系统锁屏）",
        "why_most_useful": "确认无障碍能力仅用于锁屏，未伴随读屏、自动点击等越权行为",
        "observable_utg_signals": ["双击后进入系统 Keyguard", "无障碍事件流中无窗口内容抓取", "无其他应用被自动操作"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一注意点：APK 仅打包 x86_64 libapp.so，若检测环境仅支持 arm64 动态运行可能无法直接启动该包；另外 Flutter 文本位于 AOT 字符串表而非 strings.xml，纯资源层扫描会漏掉引导文案，需结合运行期 UTG 或 libapp.so 字符串抽取。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "nl.bw20.last_launcher.LockAccessibilityService#onServiceConnected",
    "nl.bw20.last_launcher.LockAccessibilityService#onAccessibilityEvent",
    "W0.c#h",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml#accessibility_service_description",
    "package:last_launcher/features/settings/screens/settings_screen.dart"
  ]
}
```

</details>
