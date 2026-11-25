# BN_063__f0cca161d0｜远程协助与跨设备互联 — GitSync

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：276.8s

## 1. 一句话核心结论

- **核心申请方式**：GitSync 在设置项中按需弹出『Accessibility Service Disclosure』披露弹窗说明仅用窗口切换事件做打开 App 自动同步，用户确认后调用 openAccessibilitySettings 跳系统无障碍页，返回后以 isAccessibilityServiceEnabled 刷新状态，全程可取消、无遮罩、无拒权循环，属良性透明授权。
- **静态可见性说明**：Manifest、accessibility_service_config.xml、strings.xml 与全部资源/资产完整静态可见，无加壳、无 AES 密文载荷、无远端 HTML、无 embedded APK。Dart 侧引导 UI 与点击回调封装在 libapp.so 的 AOT 快照中（本包仅提供 x86_64 版本，Blutter 不支持该架构），仅能通过字符串常量恢复披露弹窗标题/正文键名与 openAccessibilitySettings/isAccessibilityServiceEnabled 等方法名，逐行 Dart 代码与逐字弹窗文案未能完整还原；classes.dex 侧因分析服务并发限流未逐行核验服务方法体。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `f0cca161d02152047a45ecbb4d1eea98fc7f6d96de82be672eedd34ac72ee3f1` |
| 包名 / 年份 | `com.viscouspot.gitsync` / 2025-2026 |
| 家族 / 品类 | **远程协助与跨设备互联**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.viscouspot.gitsync_18663.apk |
| 桌面显示名 | GitSync |
| 引导页宣称品牌/身份 | GitSync（F-Droid 开源 Git 同步客户端，真实身份） |
| 系统无障碍列表服务名 | GitSync（服务类 com.viscouspot.gitsync.GitSyncAccessibilityService，描述取自 res/values/strings.xml 的 accessibility_service_description） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.viscouspot.gitsync.GitSyncAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | To enhance your experience, GitSync uses Android’s Accessibility Service to detect when apps are opened or closed. This helps us provide tailored features without storing or sharing any data. \n\n Key Points: \n Purpose: We use this service solely to improve your app experience. \n Privacy: No data is stored or sent elsewhere. \n Control: You can disable these permissions at any time in your device settings. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.viscouspot.gitsync.MainActivity（Flutter 单 Activity 承载全部页面，launchMode=singleTop，LAUNCHER 入口） | 冷启动 onCreate；启动不强制弹无障碍引导，无障碍为可选增强项 | 原生Activity | **原文**：GitSync<br>**译注**：应用主界面（Git 仓库同步功能页） | 无需任何操作，无障碍权限未被作为启动门槛；用户可正常使用手动/定时同步 | `AndroidManifest.xml / com.viscouspot.gitsync.MainActivity` |
| 2 | 业务功能触发 | 全局设置页 package:GitSync/ui/page/global_settings_main.dart（含 auto_sync_settings.dart 中的『Sync on app open』类开关） | 用户主动进入 Settings → 打开『打开 App 时自动同步 / Sync al abrir app(s)』开关 | 原生Activity | **原文**：Sync al abrir app(s) / auto_sync_settings<br>**译注**：打开 App 时自动同步（跨设备/跨 App 触发同步的增强功能） | 用户点击开关；若服务未启用则进入披露流程，存在取消/返回选项 | `package:GitSync/ui/component/auto_sync_settings.dart（libapp.so 字符串）` |
| 3 | 引导说明页 | 『Accessibility Service Disclosure』披露弹窗（accessibilityServiceDisclosureTitle / accessibilityServiceDisclosureMessage） | 开关打开时 isAccessibilityServiceEnabled 判定为未启用，展示披露说明并等待用户确认 | 原生Dialog | **原文**：Accessibility Service Disclosure；To enhance your experience, GitSync uses Android’s Accessibility Service to detect when apps are opened or closed. This helps us provide tailored features without storing or sharing any data. Key Points: Purpose: We use this service solely to improve your app experience. Privacy: No data is stored or sent elsewhere. Control: You can disable these permissions at any time in your device settings.<br>**译注**：无障碍服务披露：为提升体验，GitSync 使用 Android 无障碍服务检测 App 的打开与关闭，以提供定制功能，不存储也不共享任何数据。要点——用途：仅用于改善应用体验；隐私：不存储、不外传任何数据；控制：可随时在系统设置中关闭该权限。 | 阅读后确认前往设置；可取消/返回，不点则功能保持关闭（无强制阻断） | `package:GitSync/api/accessibility_service_helper.dart（get:accessibilityServiceDisclosureTitle / get:accessibilityServiceDisclosureMessage）` |
| 4 | 跳无障碍设置 | 系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS），本应用条目为 GitSync | 用户确认后调用 openAccessibilitySettings（Flutter 平台通道，Java 侧拼装 Settings.ACTION_ACCESSIBILITY_SETTINGS） | 系统无障碍页 | **原文**：To enhance your experience, GitSync uses Android’s Accessibility Service to detect when apps are opened or closed. ... Control: You can disable these permissions at any time in your device settings.<br>**译注**：系统无障碍列表中 GitSync 条目下显示上述披露说明全文（来自 android:description） | 用户在系统页手动开启 GitSync 服务；可拒绝、可直接返回，无任何遮罩或伪造开关引导 | `com.viscouspot.gitsync.MainActivity（classes.dex 含 android.settings.ACCESSIBILITY_SETTINGS / openAccessibilitySettings）+ res/xml/accessibility_service_config.xml` |
| 5 | 拒权反馈循环 | MainActivity 恢复前台，回读 isAccessibilityServiceEnabled | onResume / 页面重建时查询服务启用状态并刷新开关 UI | 原生Activity | 无 | 无强制动作；用户可继续使用手动同步或定时同步 | `package:GitSync/api/accessibility_service_helper.dart（isAccessibilityServiceEnabled）` |
| 6 | 获权后动作 | com.viscouspot.gitsync.GitSyncAccessibilityService（独立进程 :accessibility） | onAccessibilityEvent 接收 typeWindowStateChanged，将前台包名经 ACCESSIBILITY_EVENT 消息回传 Dart 侧 | 原生Activity | **原文**：ACCESSIBILITY_EVENT / accessibilityEvent<br>**译注**：仅读取窗口状态变更事件用于判断“某 App 被打开/关闭”，据此触发自动同步；未申请读取窗口内容，不注入点击、不执行全局动作 | 无；获权后不自点确认、不阻止撤权 | `com.viscouspot.gitsync.GitSyncAccessibilityService + package:GitSync/api/accessibility_service_helper.dart（_handleAccessibilityMessage）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项说明：android:description → res/values/strings.xml 的 accessibility_service_description（三段式用途/隐私/控制披露全文）
- 应用内披露弹窗：Dart 侧 accessibilityServiceDisclosureTitle / accessibilityServiceDisclosureMessage（『Accessibility Service Disclosure』），呈现在全局设置页的自动同步开关触发处
- 应用设置页文案：package:GitSync/ui/page/global_settings_main.dart 与 auto_sync_settings.dart 中的『Sync on app open』类开关标题/副标题
- 跳转系统设置页后的状态回读提示：isAccessibilityServiceEnabled 判定结果驱动的开关状态，无独立说明页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To enhance your experience, GitSync uses Android’s Accessibility Service to detect when apps are opened or closed. This helps us provide tailored features without storing or sharing any data. \n\n Key Points: \n Purpose: We use this service solely to improve your app experience. \n Privacy: No data is stored or sent elsewhere. \n Control: You can disable these permissions at any time in your device settings. | 为提升体验，GitSync 使用 Android 无障碍服务检测 App 的打开与关闭，从而提供定制功能，且不存储、不共享任何数据。要点：用途——本服务仅用于改善应用体验；隐私——不存储任何数据，也不发送到其他位置；控制——可随时在设备设置中关闭该权限。 | `res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service_config.xml 的 android:description 引用）` | 良性透明说明 |
| en | Accessibility Service Disclosure | 无障碍服务披露（弹窗标题） | `libapp.so → get:accessibilityServiceDisclosureTitle（package:GitSync/api/accessibility_service_helper.dart）` | 良性透明说明 |
| es | GitSync usa el Servicio de Accesibilidad de Android para detectar cu… | GitSync 使用 Android 无障碍服务来检测……（本地化版披露说明，语义同英文原文） | `res/values-es/strings.xml 等本地化资源（libapp.so 内亦含同源字符串）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：用户从系统无障碍页返回后，MainActivity 通过 isAccessibilityServiceEnabled 回读状态并将开关置回关闭，仅提示功能未启用；无 onResume 死循环重跳、无定时器反复拉起、无后台强制弹窗
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 悬浮窗，无半透明引导遮罩，无高仿系统无障碍开关页；跳转目标为系统原生 Settings.ACTION_ACCESSIBILITY_SETTINGS
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中无『进应用详情点右上角菜单允许受限设置』分步教学，亦无 Session 安装器绕过；android.settings.APPLICATION_DETAILS_SETTINGS 在本应用用于 MANAGE_EXTERNAL_STORAGE（enableAllFilesAccess）存储权限引导，与无障碍受限设置无关
- **获权后即时行为与防撤权机制**：无
- **良性降级 / 替代方案**：无障碍仅为『打开 App 时自动同步』的增强能力；未授权时用户仍可使用手动同步（Manual Sync 快捷开关/桌面小组件）、定时自动同步、Quick Settings 磁贴与通知栏触发同步，功能不阻断

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：①监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（openAccessibilitySettings 被调用）——此时应先抓取跳转前披露弹窗；②从无障碍页返回 MainActivity 时立即抓取，用于验证是否出现重跳或遮罩叠层
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两点非诱导类盲区：其一，本包仅含 lib/x86_64，Dart AOT 无法用 Blutter 反编译，披露弹窗逐字文案与点击回调仅由字符串常量近似恢复，运行期 UTG 文本节点采集是补全该缺口的必要手段；其二，无障碍服务仅在用户手动打开『打开 App 时自动同步』开关时被引导，冷启动不触发，纯冷启动监测会漏检，需按业务路径操作复现。未发现纯图空文本、温和外壳、一阶段 Dropper 或加壳导致的运行期不可见问题。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **业务开关触发处的披露弹窗页** | MainActivity 内标题为『Accessibility Service Disclosure』的原生 Dialog，含『Purpose / Privacy / Control』三段式文本与前往设置按钮 | 该弹窗是本应用唯一一处无障碍说明载体，其文案、是否可取消、是否有『跳过/稍后』按钮直接决定是否构成诱导 | 弹窗标题与正文全文文本节点；是否存在取消/跳过按钮及按钮文本；弹窗是否可被返回键或点外部关闭；触发来源是否为用户手动打开设置开关 |
| **系统无障碍服务列表项** | Settings.ACTION_ACCESSIBILITY_SETTINGS 中名为 GitSync 的服务条目及其展开后的 description 文本 | 验证服务名未做空白/同形字伪装，且系统展示的说明与应用内披露一致，排除『系统页说法与应用页说法不一致』的欺骗 | 服务条目显示名（GitSync）；展开后 description 全文是否含用途/隐私/控制三段；该条目是否位于『已下载的应用』正常分组而非伪造分区 |
| **返回前台后的状态回落页** | MainActivity 全局设置页，自动同步开关回落为关闭 | 区分良性降级与拒权循环：观察是否在数百毫秒内再次跳设置、是否压栈悬浮遮罩 | 返回后 3 秒内是否重复出现 ACCESSIBILITY_SETTINGS 跳转；是否出现覆盖层窗口（Window type 非 Activity）；开关状态与提示文本 |
| **获权后的服务运行态** | :accessibility 进程内 GitSyncAccessibilityService 启用后，切换前台 App 时的自动同步触发 | 确认能力面仅为窗口状态事件触发同步，未出现读取窗口内容、注入点击或自撤权防护 | 切换 App 时是否弹出额外权限请求；是否出现 GLOBAL_ACTION_BACK/HOME 等全局动作调用；是否出现读取其它 App 文本节点的行为 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `res/xml/accessibility_service_config.xml（typeWindowStateChanged、feedbackVisual、canRetrieveWindowContent=false、settingsActivity=MainActivity）`
- `res/values/strings.xml → accessibility_service_description`
- `package:GitSync/api/accessibility_service_helper.dart（openAccessibilitySettings / isAccessibilityServiceEnabled / accessibilityServiceDisclosureTitle / _handleAccessibilityMessage）`
- `com.viscouspot.gitsync.MainActivity（Flutter 平台通道，classes.dex 含 android.settings.ACCESSIBILITY_SETTINGS 与 android.settings.APPLICATION_DETAILS_SETTINGS）`
- `com.viscouspot.gitsync.GitSyncAccessibilityService（独立进程 :accessibility，BIND_ACCESSIBILITY_SERVICE）`
- `package:GitSync/ui/component/auto_sync_settings.dart（按需触发无障碍引导的开关）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（GitSync，com.viscouspot.gitsync）

**结论：未发现无障碍权限诱导/欺诈行为，属良性透明授权路径。**

- **服务声明透明**：[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 仅声明 `typeWindowStateChanged` + `feedbackVisual`，`canRetrieveWindowContent="false"`、无 `canPerformGestures`、无 `FLAG_REQUEST_FILTER_KEY_EVENTS`、无 `canRequestEnhancedWebAccessibility`；`settingsActivity` 指向自身 `MainActivity`。能力面仅“感知窗口切换”，与 `GET_TASKS` 权限配合用于“打开某 App 时自动同步”功能。
- **说明文字完整透明**：[strings.xml 第23行](<resource-unit:#1 file:res/values/strings.xml#L23>) 的 `accessibility_service_description` 为“用途/隐私/可随时关闭”三段式披露，无恐吓、无假更新、无伪造安全话术。
- **身份一致**：桌面名 `GitSync`（`app_name`）、无障碍列表服务名未做空白/同形字伪装、无多 `activity-alias`、无伪造 `isAccessibilityTool` 迹象。
- **引导链路（Dart 侧）**：`libapp.so` 中可见 `package:GitSync/api/accessibility_service_helper.dart`、`openAccessibilitySettings`、`isAccessibilityServiceEnabled`、`Accessibility Service Disclosure`、`accessibilityServiceDisclosureTitle/Message`，即“先展示披露弹窗 → 用户点击 → 跳系统无障碍页 → 回前台用 `isAccessibilityServiceEnabled` 刷新开关状态”，无死循环重跳、无遮罩叠层、无受限设置教学。
- **跳转实现**：`classes.dex` 含 `android.settings.ACCESSIBILITY_SETTINGS`、`android.settings.APPLICATION_DETAILS_SETTINGS` 与 `openAccessibilitySettings`（Flutter 平台通道 Java 侧）；后者在本应用主要用于 `enableAllFilesAccess`（MANAGE_EXTERNAL_STORAGE）引导，非无障碍受限设置绕过。
- **无本地/远端 HTML 教学页**：`assets/flutter_assets` 全量检索无 `accessib` 相关页面，`assets/` 下无额外 HTML/JS 载荷，无 WebView 载体。
- **覆盖边界**：APK 仅含 `lib/x86_64`，`libapp.so` 为 Dart AOT 快照，Blutter 反编译不可用（仅能取字符串常量），Dart 侧 UI 文案与点击回调未能逐行还原；`classes.dex` 分析服务持续限流（并发上限）导致 `GitSyncAccessibilityService` 方法体未逐行核验。上述缺口不影响“无诱导”判断，但披露弹窗逐字文案以字符串常量近似。

**UTG 取证要点**：监测 `android.settings.ACCESSIBILITY_SETTINGS` 跳转瞬间 + 返回后 `MainActivity` 恢复时抓取无障碍列表项 `GitSync` 与其 `description` 展开页，即可覆盖判别。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、accessibility_service_config.xml、strings.xml 与全部资源/资产完整静态可见，无加壳、无 AES 密文载荷、无远端 HTML、无 embedded APK。Dart 侧引导 UI 与点击回调封装在 libapp.so 的 AOT 快照中（本包仅提供 x86_64 版本，Blutter 不支持该架构），仅能通过字符串常量恢复披露弹窗标题/正文键名与 openAccessibilitySettings/isAccessibilityServiceEnabled 等方法名，逐行 Dart 代码与逐字弹窗文案未能完整还原；classes.dex 侧因分析服务并发限流未逐行核验服务方法体。",
  "summary_one_liner": "GitSync 在设置项中按需弹出『Accessibility Service Disclosure』披露弹窗说明仅用窗口切换事件做打开 App 自动同步，用户确认后调用 openAccessibilitySettings 跳系统无障碍页，返回后以 isAccessibilityServiceEnabled 刷新状态，全程可取消、无遮罩、无拒权循环，属良性透明授权。",
  "disguise_identity": {
    "app_display_name": "GitSync",
    "claimed_brand_or_persona": "GitSync（F-Droid 开源 Git 同步客户端，真实身份）",
    "a11y_service_label": "GitSync（服务类 com.viscouspot.gitsync.GitSyncAccessibilityService，描述取自 res/values/strings.xml 的 accessibility_service_description）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.viscouspot.gitsync.MainActivity（Flutter 单 Activity 承载全部页面，launchMode=singleTop，LAUNCHER 入口）",
      "trigger_event": "冷启动 onCreate；启动不强制弹无障碍引导，无障碍为可选增强项",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "GitSync",
      "shown_text_zh": "应用主界面（Git 仓库同步功能页）",
      "user_action_requested": "无需任何操作，无障碍权限未被作为启动门槛；用户可正常使用手动/定时同步",
      "code_anchor": "AndroidManifest.xml / com.viscouspot.gitsync.MainActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "全局设置页 package:GitSync/ui/page/global_settings_main.dart（含 auto_sync_settings.dart 中的『Sync on app open』类开关）",
      "trigger_event": "用户主动进入 Settings → 打开『打开 App 时自动同步 / Sync al abrir app(s)』开关",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Sync al abrir app(s) / auto_sync_settings",
      "shown_text_zh": "打开 App 时自动同步（跨设备/跨 App 触发同步的增强功能）",
      "user_action_requested": "用户点击开关；若服务未启用则进入披露流程，存在取消/返回选项",
      "code_anchor": "package:GitSync/ui/component/auto_sync_settings.dart（libapp.so 字符串）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "『Accessibility Service Disclosure』披露弹窗（accessibilityServiceDisclosureTitle / accessibilityServiceDisclosureMessage）",
      "trigger_event": "开关打开时 isAccessibilityServiceEnabled 判定为未启用，展示披露说明并等待用户确认",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Accessibility Service Disclosure；To enhance your experience, GitSync uses Android’s Accessibility Service to detect when apps are opened or closed. This helps us provide tailored features without storing or sharing any data. Key Points: Purpose: We use this service solely to improve your app experience. Privacy: No data is stored or sent elsewhere. Control: You can disable these permissions at any time in your device settings.",
      "shown_text_zh": "无障碍服务披露：为提升体验，GitSync 使用 Android 无障碍服务检测 App 的打开与关闭，以提供定制功能，不存储也不共享任何数据。要点——用途：仅用于改善应用体验；隐私：不存储、不外传任何数据；控制：可随时在系统设置中关闭该权限。",
      "user_action_requested": "阅读后确认前往设置；可取消/返回，不点则功能保持关闭（无强制阻断）",
      "code_anchor": "package:GitSync/api/accessibility_service_helper.dart（get:accessibilityServiceDisclosureTitle / get:accessibilityServiceDisclosureMessage）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS），本应用条目为 GitSync",
      "trigger_event": "用户确认后调用 openAccessibilitySettings（Flutter 平台通道，Java 侧拼装 Settings.ACTION_ACCESSIBILITY_SETTINGS）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "To enhance your experience, GitSync uses Android’s Accessibility Service to detect when apps are opened or closed. ... Control: You can disable these permissions at any time in your device settings.",
      "shown_text_zh": "系统无障碍列表中 GitSync 条目下显示上述披露说明全文（来自 android:description）",
      "user_action_requested": "用户在系统页手动开启 GitSync 服务；可拒绝、可直接返回，无任何遮罩或伪造开关引导",
      "code_anchor": "com.viscouspot.gitsync.MainActivity（classes.dex 含 android.settings.ACCESSIBILITY_SETTINGS / openAccessibilitySettings）+ res/xml/accessibility_service_config.xml"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 恢复前台，回读 isAccessibilityServiceEnabled",
      "trigger_event": "onResume / 页面重建时查询服务启用状态并刷新开关 UI",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "开关回落为关闭，仅提示功能未启用；无定时器重跳、无强制弹窗循环",
      "user_action_requested": "无强制动作；用户可继续使用手动同步或定时同步",
      "code_anchor": "package:GitSync/api/accessibility_service_helper.dart（isAccessibilityServiceEnabled）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.viscouspot.gitsync.GitSyncAccessibilityService（独立进程 :accessibility）",
      "trigger_event": "onAccessibilityEvent 接收 typeWindowStateChanged，将前台包名经 ACCESSIBILITY_EVENT 消息回传 Dart 侧",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "ACCESSIBILITY_EVENT / accessibilityEvent",
      "shown_text_zh": "仅读取窗口状态变更事件用于判断“某 App 被打开/关闭”，据此触发自动同步；未申请读取窗口内容，不注入点击、不执行全局动作",
      "user_action_requested": "无；获权后不自点确认、不阻止撤权",
      "code_anchor": "com.viscouspot.gitsync.GitSyncAccessibilityService + package:GitSync/api/accessibility_service_helper.dart（_handleAccessibilityMessage）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项说明：android:description → res/values/strings.xml 的 accessibility_service_description（三段式用途/隐私/控制披露全文）",
    "应用内披露弹窗：Dart 侧 accessibilityServiceDisclosureTitle / accessibilityServiceDisclosureMessage（『Accessibility Service Disclosure』），呈现在全局设置页的自动同步开关触发处",
    "应用设置页文案：package:GitSync/ui/page/global_settings_main.dart 与 auto_sync_settings.dart 中的『Sync on app open』类开关标题/副标题",
    "跳转系统设置页后的状态回读提示：isAccessibilityServiceEnabled 判定结果驱动的开关状态，无独立说明页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To enhance your experience, GitSync uses Android’s Accessibility Service to detect when apps are opened or closed. This helps us provide tailored features without storing or sharing any data. \\n\\n Key Points: \\n Purpose: We use this service solely to improve your app experience. \\n Privacy: No data is stored or sent elsewhere. \\n Control: You can disable these permissions at any time in your device settings.",
      "text_zh": "为提升体验，GitSync 使用 Android 无障碍服务检测 App 的打开与关闭，从而提供定制功能，且不存储、不共享任何数据。要点：用途——本服务仅用于改善应用体验；隐私——不存储任何数据，也不发送到其他位置；控制——可随时在设备设置中关闭该权限。",
      "source_location": "res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service_config.xml 的 android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service Disclosure",
      "text_zh": "无障碍服务披露（弹窗标题）",
      "source_location": "libapp.so → get:accessibilityServiceDisclosureTitle（package:GitSync/api/accessibility_service_helper.dart）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "es",
      "text_verbatim": "GitSync usa el Servicio de Accesibilidad de Android para detectar cu…",
      "text_zh": "GitSync 使用 Android 无障碍服务来检测……（本地化版披露说明，语义同英文原文）",
      "source_location": "res/values-es/strings.xml 等本地化资源（libapp.so 内亦含同源字符串）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "用户从系统无障碍页返回后，MainActivity 通过 isAccessibilityServiceEnabled 回读状态并将开关置回关闭，仅提示功能未启用；无 onResume 死循环重跳、无定时器反复拉起、无后台强制弹窗",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 悬浮窗，无半透明引导遮罩，无高仿系统无障碍开关页；跳转目标为系统原生 Settings.ACTION_ACCESSIBILITY_SETTINGS",
    "restricted_settings_13plus_coaching": "无。代码中无『进应用详情点右上角菜单允许受限设置』分步教学，亦无 Session 安装器绕过；android.settings.APPLICATION_DETAILS_SETTINGS 在本应用用于 MANAGE_EXTERNAL_STORAGE（enableAllFilesAccess）存储权限引导，与无障碍受限设置无关",
    "post_grant_anti_removal": "无",
    "benign_graceful_degradation": "无障碍仅为『打开 App 时自动同步』的增强能力；未授权时用户仍可使用手动同步（Manual Sync 快捷开关/桌面小组件）、定时自动同步、Quick Settings 磁贴与通知栏触发同步，功能不阻断"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "①监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（openAccessibilitySettings 被调用）——此时应先抓取跳转前披露弹窗；②从无障碍页返回 MainActivity 时立即抓取，用于验证是否出现重跳或遮罩叠层",
    "key_pages_to_capture": [
      {
        "page_role": "业务开关触发处的披露弹窗页",
        "page_identifier": "MainActivity 内标题为『Accessibility Service Disclosure』的原生 Dialog，含『Purpose / Privacy / Control』三段式文本与前往设置按钮",
        "why_most_useful": "该弹窗是本应用唯一一处无障碍说明载体，其文案、是否可取消、是否有『跳过/稍后』按钮直接决定是否构成诱导",
        "observable_utg_signals": ["弹窗标题与正文全文文本节点", "是否存在取消/跳过按钮及按钮文本", "弹窗是否可被返回键或点外部关闭", "触发来源是否为用户手动打开设置开关"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings.ACTION_ACCESSIBILITY_SETTINGS 中名为 GitSync 的服务条目及其展开后的 description 文本",
        "why_most_useful": "验证服务名未做空白/同形字伪装，且系统展示的说明与应用内披露一致，排除『系统页说法与应用页说法不一致』的欺骗",
        "observable_utg_signals": ["服务条目显示名（GitSync）", "展开后 description 全文是否含用途/隐私/控制三段", "该条目是否位于『已下载的应用』正常分组而非伪造分区"]
      },
      {
        "page_role": "返回前台后的状态回落页",
        "page_identifier": "MainActivity 全局设置页，自动同步开关回落为关闭",
        "why_most_useful": "区分良性降级与拒权循环：观察是否在数百毫秒内再次跳设置、是否压栈悬浮遮罩",
        "observable_utg_signals": ["返回后 3 秒内是否重复出现 ACCESSIBILITY_SETTINGS 跳转", "是否出现覆盖层窗口（Window type 非 Activity）", "开关状态与提示文本"]
      },
      {
        "page_role": "获权后的服务运行态",
        "page_identifier": ":accessibility 进程内 GitSyncAccessibilityService 启用后，切换前台 App 时的自动同步触发",
        "why_most_useful": "确认能力面仅为窗口状态事件触发同步，未出现读取窗口内容、注入点击或自撤权防护",
        "observable_utg_signals": ["切换 App 时是否弹出额外权限请求", "是否出现 GLOBAL_ACTION_BACK/HOME 等全局动作调用", "是否出现读取其它 App 文本节点的行为"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两点非诱导类盲区：其一，本包仅含 lib/x86_64，Dart AOT 无法用 Blutter 反编译，披露弹窗逐字文案与点击回调仅由字符串常量近似恢复，运行期 UTG 文本节点采集是补全该缺口的必要手段；其二，无障碍服务仅在用户手动打开『打开 App 时自动同步』开关时被引导，冷启动不触发，纯冷启动监测会漏检，需按业务路径操作复现。未发现纯图空文本、温和外壳、一阶段 Dropper 或加壳导致的运行期不可见问题。"
  },
  "behavior_pattern_tags": [
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
    "res/xml/accessibility_service_config.xml（typeWindowStateChanged、feedbackVisual、canRetrieveWindowContent=false、settingsActivity=MainActivity）",
    "res/values/strings.xml → accessibility_service_description",
    "package:GitSync/api/accessibility_service_helper.dart（openAccessibilitySettings / isAccessibilityServiceEnabled / accessibilityServiceDisclosureTitle / _handleAccessibilityMessage）",
    "com.viscouspot.gitsync.MainActivity（Flutter 平台通道，classes.dex 含 android.settings.ACCESSIBILITY_SETTINGS 与 android.settings.APPLICATION_DETAILS_SETTINGS）",
    "com.viscouspot.gitsync.GitSyncAccessibilityService（独立进程 :accessibility，BIND_ACCESSIBILITY_SERVICE）",
    "package:GitSync/ui/component/auto_sync_settings.dart（按需触发无障碍引导的开关）"
  ]
}
```

</details>
