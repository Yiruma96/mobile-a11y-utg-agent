# BN_059__1f66ec8f83｜自动化与跳广告 — GKD

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：156.8s

## 1. 一句话核心结论

- **核心申请方式**：GKD 以真实品牌身份、诚实说明文案，仅在用户主动开启『触摸优化』等功能时按需跳转系统无障碍设置，并提供 ADB/Root/Shizuku 特权模式作为替代与降级路径，无强制拦截、无遮罩诱导、无撤权阻止。
- **静态可见性说明**：无障碍服务声明、三份 a11y_info XML、全部引导/说明字符串与两处设置跳转代码点均完整静态可见；Compose 多语言文案以 base64 存储在 assets/composeResources/li.gkd.app.resources/values(-zh)/strings.commonMain.cvr 中，可完整解码，无加壳、无远端 HTML 下发。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1f66ec8f832dafcb32f97c501aad964398a335862691752fa29a15fa91d724e2` |
| 包名 / 年份 | `li.songe.gkd` / 2025-2026 |
| 家族 / 品类 | **自动化与跳广告**（同池样本数：1） |
| 原始来源标识 | https://github.com/gkd-kit/gkd/releases/download/v1.13.2/gkd-v1.13.2.apk |
| 桌面显示名 | GKD |
| 引导页宣称品牌/身份 | GKD（开源自定义规则跳过开屏广告工具，真实品牌，无伪装） |
| 系统无障碍列表服务名 | GKD / GKD touch optimization (do not enable manually) / GKD companion service (do not enable manually)（中文：GKD / GKD 触摸优化（请勿手动开启）/ GKD 伴生服务（请勿手动开启）） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.google.android.accessibility.selecttospeak.SelectToSpeakService, com.google.android.accessibility.selecttospeak.SelectToSpeakServicePrivileged, com.google.android.accessibility.selecttospeak.SelectToSpeakServiceCompanion` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Managed automatically by GKD. Do not enable manually.<br><br>Reads screen content and matches rules. The privileged service performs clicks and swipes to reduce touch stutter. / Managed automatically by GKD. Do not enable manually.<br><br>Helps automation work in some apps and keeps GKD running in the background.<br><br>Accessibility capabilities are disabled; only the service remains running, with minimal overhead. Some apps may still detect accessibility as enabled. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | li.gkd.app.MainActivity（Compose 首页，singleTask，LAUNCHER） | onCreate / 冷启动进入首页 | 原生Activity | **原文**：无（冷启动不弹出任何权限引导弹窗）<br>**译注**：无：首页正常展示规则/应用列表，未无障碍权限时仅以状态卡片呈现，不拦截操作 | 无强制操作；用户可自由浏览、导入规则或进入设置 | `li.gkd.app.MainActivity（AndroidManifest.xml application/activity）` |
| 2 | 业务功能触发 | 设置页 li.gkd.app.ui.settings.TouchOptimizationPage（『触摸优化』工作模式页） | 用户点击该模式开关（Compose 点击回调，TouchOptimizationPage.kt:73 附近） | 原生Activity | **原文**：GKD touch optimization (do not enable manually) / 由 GKD 自动管理，请勿手动开启<br>**译注**：用户主动选择『触摸优化』模式后，页面提示该服务由 GKD 自动管理、请勿手动开启，随后跳转系统无障碍页 | 用户可点击开关进入系统设置，也可直接返回（无死循环重跳） | `p47#s → li.gkd.app.ui.settings.TouchOptimizationPage(TouchOptimizationPage.kt:73)` |
| 3 | 跳无障碍设置 | 系统设置页 com.android.settings/.accessibility.AccessibilitySettings | Intent(android.settings.ACCESSIBILITY_SETTINGS) 启动（App 单例 nt8.Y 或 Activity.startActivity） | 系统无障碍页 | **原文**：无（跳转系统页面）<br>**译注**：跳转前先经 lk1.e(...) 校验服务是否已启用，未启用才跳转；跳转不携带伪造参数 | 用户自行在系统列表中找到 GKD 服务并开启，应用不预勾选、不代操作 | `n54#s → li.gkd.app.util.IntentUtils.openA11ySettings(IntentUtils.kt:32)` |
| 4 | 引导说明页 | 系统无障碍列表中的服务条目说明（android:description） | 用户进入系统无障碍设置查看服务详情 | 系统无障碍页 | **原文**：Custom screen clicking based on advanced selectors and subscription rules.<br><br>Use custom selectors and subscription rules to click controls anywhere on screen and create custom shortcuts.<br>**译注**：基于高级选择器和订阅规则的屏幕自定义点击服务；使用自定义选择器与订阅规则在屏幕任意位置点击控件并创建自定义快捷方式 | 用户阅读说明后自主决定是否开启 | `res/xml/a11y_info_standard.xml → @string/a11y_desc（res/values/strings.xml、res/values-zh/strings.xml）` |
| 5 | 拒权反馈循环 | TouchOptimizationPage 工作模式选择区 / 特权服务页面（priv.kit.ui） | 用户从系统设置返回（未开启）或选择非无障碍模式 | 原生Activity | **原文**：当前 ADB 权限不完整，以下功能受到影响： / 已获得的应用权限仍可使用。可前往特权服务查看处理方式 / 系统限制应用自动管理无线调试，请在开发者选项中手动开启无线调试后重试。<br>**译注**：未开启无障碍时如实告知降级影响，并指引使用 ADB/Root/Shizuku 特权模式或开发者选项手动开启，无重复拉起设置页 | 用户可选择 ADB/Root 特权授权或放弃；存在明确的取消/返回路径 | `assets/composeResources/li.gkd.app.resources/values-zh/strings.commonMain.cvr（restriction_adb_intro / restriction_adb_footer / priv_ui_wireless_debugging_control_restricted）` |
| 6 | 获权后动作 | SelectToSpeakService / SelectToSpeakServicePrivileged / SelectToSpeakServiceCompanion | 系统绑定无障碍服务后 onServiceConnected / 事件回调（typeWindowContentChanged\|typeWindowStateChanged） | 原生Activity | 无 | 无；用户可随时在系统设置中关闭服务 | `res/xml/a11y_info_privileged.xml、res/xml/a11y_info_companion.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表服务条目说明：res/xml/a11y_info_standard.xml → @string/a11y_desc（『基于高级选择器和订阅规则的屏幕自定义点击服务…』）
- 系统无障碍列表服务条目说明：res/xml/a11y_info_privileged.xml → @string/privileged_a11y_desc（『由 GKD 自动管理，请勿手动开启…』）
- 系统无障碍列表服务条目说明：res/xml/a11y_info_companion.xml → @string/companion_a11y_desc（『…相关能力均已禁用，仅保留服务运行，日常运行开销很小』）
- 服务标签：@string/app_name（GKD）、@string/privileged_a11y_label、@string/companion_a11y_label
- 应用内『触摸优化』设置页（li.gkd.app.ui.settings.TouchOptimizationPage）的开关说明与跳转前提示（Compose 文案，存于 assets/composeResources/.../values(-zh)/strings.commonMain.cvr）
- 特权服务页面的权限不足提示与影响说明（priv_ui_* / restriction_adb_* 文案）
- 无 AlertDialog 强制弹窗、无 WebView/HTML 教学页、无悬浮窗遮罩引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Custom screen clicking based on advanced selectors and subscription rules.<br><br>Use custom selectors and subscription rules to click controls anywhere on screen and create custom shortcuts. | 基于高级选择器和订阅规则的屏幕自定义点击服务。使用自定义选择器与订阅规则，在屏幕任意位置点击控件并创建自定义快捷方式。 | `res/values/strings.xml → a11y_desc` | 良性透明说明 |
| zh | 基于高级选择器和订阅规则的屏幕自定义点击服务<br><br>使用自定义选择器与订阅规则点击屏幕任意位置的控件，并创建自定义快捷方式 | 同上，中文本地化版本 | `res/values-zh/strings.xml → a11y_desc` | 良性透明说明 |
| en | Managed automatically by GKD. Do not enable manually.<br><br>Reads screen content and matches rules. The privileged service performs clicks and swipes to reduce touch stutter. | 由 GKD 自动管理，请勿手动开启。读取屏幕内容并匹配规则；特权服务执行点击与滑动以减少触摸卡顿。 | `res/values/strings.xml → privileged_a11y_desc` | 良性透明说明 |
| zh | 由 GKD 自动管理，请勿手动开启<br><br>相关能力均已禁用，仅保留服务运行，日常运行开销很小。部分应用仍可能提示已开启无障碍 | 伴生服务说明：能力已禁用、仅保活，并如实提示部分应用仍可能检测到无障碍已开启。 | `res/values-zh/strings.xml → companion_a11y_desc` | 良性透明说明 |
| en | GKD touch optimization (do not enable manually) / GKD companion service (do not enable manually) | GKD 触摸优化（请勿手动开启）／GKD 伴生服务（请勿手动开启） | `res/values/strings.xml → privileged_a11y_label / companion_a11y_label` | 良性透明说明 |
| zh | 当前 ADB 权限不完整，以下功能受到影响： | 权限不足时的如实影响告知，指引用户走 ADB/Root 特权路径而非反复索要无障碍。 | `assets/composeResources/li.gkd.app.resources/values-zh/strings.commonMain.cvr → restriction_adb_intro` | 良性透明说明 |
| zh | 已获得的应用权限仍可使用。可前往特权服务查看处理方式 | 部分能力受限时的降级说明，提示已获权限继续可用。 | `assets/composeResources/li.gkd.app.resources/values-zh/strings.commonMain.cvr → restriction_adb_footer` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性安全降级：仅在 lk1.e 校验服务未启用时跳转一次 ACCESSIBILITY_SETTINGS；用户返回后停留在工作模式页，不重跳、不设定时器拉起，改为提示 ADB/Root/Shizuku 特权授权或开发者选项手动开启无线调试。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 叠加引导遮罩，无高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 用于截图按钮/文本卡片/操作轨迹等自建悬浮展示服务（ButtonService/ActivityService/EventService/TrackService）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现引导进入应用详情点右上角菜单允许受限设置的话术；仅在使用 ADB 授权时提示『系统限制应用自动管理无线调试，请在开发者选项中手动开启无线调试后重试』，属系统能力限制的真实说明，非绕过教学。
- **获权后即时行为与防撤权机制**：无。获权后无自点确认、无监听设置页，performGlobalAction 仅用于业务自动化点击（如返回/关闭广告页），未用于阻止撤权。
- **良性降级 / 替代方案**：提供多档替代路径：ADB（PrivilegeAdbPairingService 配对 + 无线调试）、Root、Shizuku（rikka.shizuku.ShizukuProvider），并在权限不完整时以 restriction_adb_* 文案说明受影响功能与已获权限仍可用。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在用户于应用内开启『触摸优化』等工作模式后、监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间拉起 UTG；以及从系统无障碍页返回应用后的下一帧（验证是否存在重跳/遮罩）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。该应用未加壳、无加密二阶段载荷、无远端 HTML 引导，运行期 UTG 可完整覆盖；唯一需注意点是多语言文案存于 Compose 资源 .cvr（base64），UTG 抓取到的是渲染后的本地化文本，与静态解码结果一致。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前的应用内工作模式页（TouchOptimizationPage）** | li.gkd.app.MainActivity 内 Compose 设置页，含『触摸优化』开关与『由 GKD 自动管理，请勿手动开启』说明文本 | 区分是用户主动开启功能后跳转，还是冷启动即被强制拦截的关键判据 | 存在可返回/取消的导航控件与开关；文案为如实功能说明而非恐吓或假更新；无全屏遮罩层节点 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中的 GKD 条目（标签 GKD touch optimization…） | 核对服务名与描述是否与真实品牌一致、是否被伪造成系统组件名 | 条目文本与 a11y_desc 完全一致；无空白/换行挤出警告的截断描述；开关由用户手动操作，未被自动勾选 |
| **从系统设置返回应用后的下一屏** | 应用恢复到前台的首个界面与窗口层级 | 检测是否存在 onResume 死循环重跳或悬浮窗叠层引导 | 无重复弹出设置跳转；无 SYSTEM_ALERT_WINDOW 类型遮罩窗口；显示降级提示或首页正常内容 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `li.gkd.app.util.IntentUtils.openA11ySettings（IntentUtils.kt:32）`
- `li.gkd.app.ui.settings.TouchOptimizationPage（TouchOptimizationPage.kt:73）`
- `res/xml/a11y_info_standard.xml`
- `res/xml/a11y_info_privileged.xml`
- `res/xml/a11y_info_companion.xml`
- `assets/composeResources/li.gkd.app.resources/values-zh/strings.commonMain.cvr`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **身份透明**：桌面名 `GKD`，无障碍服务标签在系统列表中为 `GKD` / `GKD touch optimization (do not enable manually)` / `GKD companion service (do not enable manually)`，中文为「GKD 触摸优化（请勿手动开启）」「GKD 伴生服务（请勿手动开启）」。三个服务与业务用途一致，无仿冒品牌、无空白挤出、无同形字。
- **说明文案诚实**：`android:description` 直接写明"基于高级选择器和订阅规则的屏幕自定义点击服务""由 GKD 自动管理，请勿手动开启…相关能力均已禁用，仅保留服务运行"，属良性透明说明，非恐吓/假更新/假反诈。
- **跳转路径常规**：仅两处 `android.settings.ACCESSIBILITY_SETTINGS` 跳转点——[IntentUtils.openA11ySettings (IntentUtils.kt:32)](<resource-unit:#1.dex1 code:n54#s>)（经 `lk1.e` 状态校验后 `nt8.Y` 启动）与 [TouchOptimizationPage.kt:73](<resource-unit:#1.dex1 code:p47#s>)（用户在"触摸优化"设置页主动开启开关时 `startActivity`）。均发生在**用户主动开启功能**之后，非冷启动强制拦截。
- **无诱导载体**：未发现 WebView 教学页、本地 HTML、高仿系统无障碍页、半透明遮罩叠层、悬浮窗引导，也无 onResume 死循环重跳或 `GLOBAL_ACTION_BACK/HOME` 阻止撤权（`performGlobalAction` 仅用于业务点击自动化）。
- **存在良性降级/替代路径**：ADB / Root / Shizuku 特权模式（`priv.kit.ui.PrivilegeAdbPairingService`、`rikka.shizuku.ShizukuProvider`），并在权限不完整时以 `restriction_adb_*` 文案如实提示影响范围，属"替代模式提供 + 显式取消降级"。
- **`isAccessibilityTool=true`** 由 [res/values/bools.xml](<resource-unit:#1 file:res/values/bools.xml>) 声明，对真实自动化工具属正当用途声明，非伪造。
- **未确认风险**：本专题（无障碍引导链路）未发现恶意诱导或权限滥用；`REQUEST_INSTALL_PACKAGES`/`QUERY_ALL_PACKAGES`/受限设置等线索属功能所需（规则订阅、应用识别、ADB 授权），未构成本次命题。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍服务声明、三份 a11y_info XML、全部引导/说明字符串与两处设置跳转代码点均完整静态可见；Compose 多语言文案以 base64 存储在 assets/composeResources/li.gkd.app.resources/values(-zh)/strings.commonMain.cvr 中，可完整解码，无加壳、无远端 HTML 下发。",
  "summary_one_liner": "GKD 以真实品牌身份、诚实说明文案，仅在用户主动开启『触摸优化』等功能时按需跳转系统无障碍设置，并提供 ADB/Root/Shizuku 特权模式作为替代与降级路径，无强制拦截、无遮罩诱导、无撤权阻止。",
  "disguise_identity": {
    "app_display_name": "GKD",
    "claimed_brand_or_persona": "GKD（开源自定义规则跳过开屏广告工具，真实品牌，无伪装）",
    "a11y_service_label": "GKD / GKD touch optimization (do not enable manually) / GKD companion service (do not enable manually)（中文：GKD / GKD 触摸优化（请勿手动开启）/ GKD 伴生服务（请勿手动开启））",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "li.gkd.app.MainActivity（Compose 首页，singleTask，LAUNCHER）",
      "trigger_event": "onCreate / 冷启动进入首页",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（冷启动不弹出任何权限引导弹窗）",
      "shown_text_zh": "无：首页正常展示规则/应用列表，未无障碍权限时仅以状态卡片呈现，不拦截操作",
      "user_action_requested": "无强制操作；用户可自由浏览、导入规则或进入设置",
      "code_anchor": "li.gkd.app.MainActivity（AndroidManifest.xml application/activity）"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "设置页 li.gkd.app.ui.settings.TouchOptimizationPage（『触摸优化』工作模式页）",
      "trigger_event": "用户点击该模式开关（Compose 点击回调，TouchOptimizationPage.kt:73 附近）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "GKD touch optimization (do not enable manually) / 由 GKD 自动管理，请勿手动开启",
      "shown_text_zh": "用户主动选择『触摸优化』模式后，页面提示该服务由 GKD 自动管理、请勿手动开启，随后跳转系统无障碍页",
      "user_action_requested": "用户可点击开关进入系统设置，也可直接返回（无死循环重跳）",
      "code_anchor": "p47#s → li.gkd.app.ui.settings.TouchOptimizationPage(TouchOptimizationPage.kt:73)"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 com.android.settings/.accessibility.AccessibilitySettings",
      "trigger_event": "Intent(android.settings.ACCESSIBILITY_SETTINGS) 启动（App 单例 nt8.Y 或 Activity.startActivity）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转系统页面）",
      "shown_text_zh": "跳转前先经 lk1.e(...) 校验服务是否已启用，未启用才跳转；跳转不携带伪造参数",
      "user_action_requested": "用户自行在系统列表中找到 GKD 服务并开启，应用不预勾选、不代操作",
      "code_anchor": "n54#s → li.gkd.app.util.IntentUtils.openA11ySettings(IntentUtils.kt:32)"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "系统无障碍列表中的服务条目说明（android:description）",
      "trigger_event": "用户进入系统无障碍设置查看服务详情",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Custom screen clicking based on advanced selectors and subscription rules.\n\nUse custom selectors and subscription rules to click controls anywhere on screen and create custom shortcuts.",
      "shown_text_zh": "基于高级选择器和订阅规则的屏幕自定义点击服务；使用自定义选择器与订阅规则在屏幕任意位置点击控件并创建自定义快捷方式",
      "user_action_requested": "用户阅读说明后自主决定是否开启",
      "code_anchor": "res/xml/a11y_info_standard.xml → @string/a11y_desc（res/values/strings.xml、res/values-zh/strings.xml）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "TouchOptimizationPage 工作模式选择区 / 特权服务页面（priv.kit.ui）",
      "trigger_event": "用户从系统设置返回（未开启）或选择非无障碍模式",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "当前 ADB 权限不完整，以下功能受到影响： / 已获得的应用权限仍可使用。可前往特权服务查看处理方式 / 系统限制应用自动管理无线调试，请在开发者选项中手动开启无线调试后重试。",
      "shown_text_zh": "未开启无障碍时如实告知降级影响，并指引使用 ADB/Root/Shizuku 特权模式或开发者选项手动开启，无重复拉起设置页",
      "user_action_requested": "用户可选择 ADB/Root 特权授权或放弃；存在明确的取消/返回路径",
      "code_anchor": "assets/composeResources/li.gkd.app.resources/values-zh/strings.commonMain.cvr（restriction_adb_intro / restriction_adb_footer / priv_ui_wireless_debugging_control_restricted）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "SelectToSpeakService / SelectToSpeakServicePrivileged / SelectToSpeakServiceCompanion",
      "trigger_event": "系统绑定无障碍服务后 onServiceConnected / 事件回调（typeWindowContentChanged|typeWindowStateChanged）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后仅执行规则匹配与手势点击（canPerformGestures/canTakeScreenshot），无自点确认、无监听设置页撤权、无 GLOBAL_ACTION_BACK/HOME 阻止关闭",
      "user_action_requested": "无；用户可随时在系统设置中关闭服务",
      "code_anchor": "res/xml/a11y_info_privileged.xml、res/xml/a11y_info_companion.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表服务条目说明：res/xml/a11y_info_standard.xml → @string/a11y_desc（『基于高级选择器和订阅规则的屏幕自定义点击服务…』）",
    "系统无障碍列表服务条目说明：res/xml/a11y_info_privileged.xml → @string/privileged_a11y_desc（『由 GKD 自动管理，请勿手动开启…』）",
    "系统无障碍列表服务条目说明：res/xml/a11y_info_companion.xml → @string/companion_a11y_desc（『…相关能力均已禁用，仅保留服务运行，日常运行开销很小』）",
    "服务标签：@string/app_name（GKD）、@string/privileged_a11y_label、@string/companion_a11y_label",
    "应用内『触摸优化』设置页（li.gkd.app.ui.settings.TouchOptimizationPage）的开关说明与跳转前提示（Compose 文案，存于 assets/composeResources/.../values(-zh)/strings.commonMain.cvr）",
    "特权服务页面的权限不足提示与影响说明（priv_ui_* / restriction_adb_* 文案）",
    "无 AlertDialog 强制弹窗、无 WebView/HTML 教学页、无悬浮窗遮罩引导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Custom screen clicking based on advanced selectors and subscription rules.\n\nUse custom selectors and subscription rules to click controls anywhere on screen and create custom shortcuts.",
      "text_zh": "基于高级选择器和订阅规则的屏幕自定义点击服务。使用自定义选择器与订阅规则，在屏幕任意位置点击控件并创建自定义快捷方式。",
      "source_location": "res/values/strings.xml → a11y_desc",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "基于高级选择器和订阅规则的屏幕自定义点击服务\n\n使用自定义选择器与订阅规则点击屏幕任意位置的控件，并创建自定义快捷方式",
      "text_zh": "同上，中文本地化版本",
      "source_location": "res/values-zh/strings.xml → a11y_desc",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Managed automatically by GKD. Do not enable manually.\n\nReads screen content and matches rules. The privileged service performs clicks and swipes to reduce touch stutter.",
      "text_zh": "由 GKD 自动管理，请勿手动开启。读取屏幕内容并匹配规则；特权服务执行点击与滑动以减少触摸卡顿。",
      "source_location": "res/values/strings.xml → privileged_a11y_desc",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "由 GKD 自动管理，请勿手动开启\n\n相关能力均已禁用，仅保留服务运行，日常运行开销很小。部分应用仍可能提示已开启无障碍",
      "text_zh": "伴生服务说明：能力已禁用、仅保活，并如实提示部分应用仍可能检测到无障碍已开启。",
      "source_location": "res/values-zh/strings.xml → companion_a11y_desc",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "GKD touch optimization (do not enable manually) / GKD companion service (do not enable manually)",
      "text_zh": "GKD 触摸优化（请勿手动开启）／GKD 伴生服务（请勿手动开启）",
      "source_location": "res/values/strings.xml → privileged_a11y_label / companion_a11y_label",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "当前 ADB 权限不完整，以下功能受到影响：",
      "text_zh": "权限不足时的如实影响告知，指引用户走 ADB/Root 特权路径而非反复索要无障碍。",
      "source_location": "assets/composeResources/li.gkd.app.resources/values-zh/strings.commonMain.cvr → restriction_adb_intro",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "已获得的应用权限仍可使用。可前往特权服务查看处理方式",
      "text_zh": "部分能力受限时的降级说明，提示已获权限继续可用。",
      "source_location": "assets/composeResources/li.gkd.app.resources/values-zh/strings.commonMain.cvr → restriction_adb_footer",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性安全降级：仅在 lk1.e 校验服务未启用时跳转一次 ACCESSIBILITY_SETTINGS；用户返回后停留在工作模式页，不重跳、不设定时器拉起，改为提示 ADB/Root/Shizuku 特权授权或开发者选项手动开启无线调试。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 叠加引导遮罩，无高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 用于截图按钮/文本卡片/操作轨迹等自建悬浮展示服务（ButtonService/ActivityService/EventService/TrackService）。",
    "restricted_settings_13plus_coaching": "无。未出现引导进入应用详情点右上角菜单允许受限设置的话术；仅在使用 ADB 授权时提示『系统限制应用自动管理无线调试，请在开发者选项中手动开启无线调试后重试』，属系统能力限制的真实说明，非绕过教学。",
    "post_grant_anti_removal": "无。获权后无自点确认、无监听设置页，performGlobalAction 仅用于业务自动化点击（如返回/关闭广告页），未用于阻止撤权。",
    "benign_graceful_degradation": "提供多档替代路径：ADB（PrivilegeAdbPairingService 配对 + 无线调试）、Root、Shizuku（rikka.shizuku.ShizukuProvider），并在权限不完整时以 restriction_adb_* 文案说明受影响功能与已获权限仍可用。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在用户于应用内开启『触摸优化』等工作模式后、监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间拉起 UTG；以及从系统无障碍页返回应用后的下一帧（验证是否存在重跳/遮罩）。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前的应用内工作模式页（TouchOptimizationPage）",
        "page_identifier": "li.gkd.app.MainActivity 内 Compose 设置页，含『触摸优化』开关与『由 GKD 自动管理，请勿手动开启』说明文本",
        "why_most_useful": "区分是用户主动开启功能后跳转，还是冷启动即被强制拦截的关键判据",
        "observable_utg_signals": ["存在可返回/取消的导航控件与开关", "文案为如实功能说明而非恐吓或假更新", "无全屏遮罩层节点"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中的 GKD 条目（标签 GKD touch optimization…）",
        "why_most_useful": "核对服务名与描述是否与真实品牌一致、是否被伪造成系统组件名",
        "observable_utg_signals": ["条目文本与 a11y_desc 完全一致", "无空白/换行挤出警告的截断描述", "开关由用户手动操作，未被自动勾选"]
      },
      {
        "page_role": "从系统设置返回应用后的下一屏",
        "page_identifier": "应用恢复到前台的首个界面与窗口层级",
        "why_most_useful": "检测是否存在 onResume 死循环重跳或悬浮窗叠层引导",
        "observable_utg_signals": ["无重复弹出设置跳转", "无 SYSTEM_ALERT_WINDOW 类型遮罩窗口", "显示降级提示或首页正常内容"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。该应用未加壳、无加密二阶段载荷、无远端 HTML 引导，运行期 UTG 可完整覆盖；唯一需注意点是多语言文案存于 Compose 资源 .cvr（base64），UTG 抓取到的是渲染后的本地化文本，与静态解码结果一致。"
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
    "li.gkd.app.util.IntentUtils.openA11ySettings（IntentUtils.kt:32）",
    "li.gkd.app.ui.settings.TouchOptimizationPage（TouchOptimizationPage.kt:73）",
    "res/xml/a11y_info_standard.xml",
    "res/xml/a11y_info_privileged.xml",
    "res/xml/a11y_info_companion.xml",
    "assets/composeResources/li.gkd.app.resources/values-zh/strings.commonMain.cvr"
  ]
}
```

</details>
