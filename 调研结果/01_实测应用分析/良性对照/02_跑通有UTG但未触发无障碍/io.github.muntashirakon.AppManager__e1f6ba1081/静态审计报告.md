# BN_054__e1f6ba1081｜系统清理与省电冻结 — App Manager

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：129.8s

## 1. 一句话核心结论

- **核心申请方式**：该应用仅在用户主动开启“前台窗口内容追踪”功能时，通过原生串行对话框按需引导至系统无障碍设置页，每步均提供 Go back 退出，无障碍说明与实际用途一致，属良性透明授权流程。
- **静态可见性说明**：全部静态可见：无障碍服务声明、配置 XML、引导对话框逻辑与全部文案均在 DEX 与 res/values/strings.xml 中明文可读，无加壳、无加密载荷、无远端 HTML 承载引导内容。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e1f6ba10812c74016ad626e11e27a1ae450aec2c0964a11466abb9e7a9c8ef84` |
| 包名 / 年份 | `io.github.muntashirakon.AppManager` / 2025-2026 |
| 家族 / 品类 | **系统清理与省电冻结**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/io.github.muntashirakon.AppManager_451.apk |
| 桌面显示名 | App Manager |
| 引导页宣称品牌/身份 | App Manager（io.github.muntashirakon.AppManager，开源应用管理工具，真实身份） |
| 系统无障碍列表服务名 | App Manager（无障碍服务未单独声明 android:label，继承 application 的 @string/app_name） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务未使用空白/换行挤出警告、同形字、多 activity-alias 伪装或伪造 isAccessibilityTool；Manifest 中的 activity-alias（EditorActivity、AppInfoActivity）均为常规功能别名，与应用身份一致。 |
| 无障碍服务类名 | `io.github.muntashirakon.AppManager.accessibility.NoRootAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Generic accessibility service to carry out certain operations such as clearing cache in no-root mode. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | io.github.muntashirakon.AppManager.AppManager（Application）→ 各 Activity | Application.onCreate / 主界面启动 | 原生Activity | 无 | 无（不请求任何权限） | `io.github.muntashirakon.AppManager.AppManager#onCreate` |
| 2 | 业务功能触发 | io.github.muntashirakon.AppManager.accessibility.activity.LeadingActivityTrackerActivity（exported=false，TransparentBackground 主题，excludeFromRecents） | 用户在设置/功能开关中主动启用“前台窗口内容追踪”，Activity 启动后进入 init() | 原生Activity | 无 | 无（由用户上一步主动操作触发） | `LeadingActivityTrackerActivity#init / AndroidManifest.xml activity 声明` |
| 3 | 跳受限设置 | MaterialAlertDialogBuilder 对话框（标题 Grant required permission）→ 系统 ACTION_MANAGE_OVERLAY_PERMISSION 页 | init() 检测 !Settings.canDrawOverlays(this) | 原生Dialog | **原文**：Grant required permission / Allow App Manager to display a floating window on top of all other windows / OK / Go back<br>**译注**：需要授予权限 / 允许 App Manager 在其他所有窗口之上显示悬浮窗 / 确定 / 返回 | 点击 OK 跳转悬浮窗授权页；点击 Go back 直接 finish() 退出，可取消 | `LeadingActivityTrackerActivity#init + lambda$init$2（ACTION_MANAGE_OVERLAY_PERMISSION）+ lambda$init$3（finish）` |
| 4 | 跳受限设置 | 使用情况访问授权（SelfPermissions.checkUsageStatsPermission 为 false 时经 ThreadUtils.postOnMainThread 拉起） | init() 检测缺少 PACKAGE_USAGE_STATS | 原生Dialog | **原文**：Grant usage access / Used to display app usage info.<br>**译注**：授予使用情况访问权限 / 用于显示应用使用信息 | 按提示进入系统使用情况访问设置并开启，可返回取消 | `LeadingActivityTrackerActivity#init + lambda$init$6；strings.xml grant_usage_access / grant_usage_acess_message` |
| 5 | 跳无障碍设置 | MaterialAlertDialogBuilder 对话框（setCancelable(false)）→ 系统 android.settings.ACCESSIBILITY_SETTINGS 页 | init() 检测 !NoRootAccessibilityService.isAccessibilityEnabled(this) | 原生Dialog | **原文**：Grant required permission / Allow App Manager to utilise the accessibility feature to track the contents of the leading window. / OK / Go back<br>**译注**：需要授予权限 / 允许 App Manager 使用无障碍功能跟踪前台窗口内容 / 确定 / 返回 | 点击 OK 经 ActivityResultLauncher 跳转系统无障碍设置页并自行开启服务；点击 Go back 直接 finish() 退出 | `LeadingActivityTrackerActivity#init + lambda$init$7（ACTION_ACCESSIBILITY_SETTINGS）+ lambda$init$8（finish）` |
| 6 | 获权后动作 | AccessibilityMultiplexer.getInstance().enableLeadingActivityTracker(true) 后 finish() | init() 三项检查全部通过（或用户从设置页返回后 onActivityResult 重新调用 init） | 原生Activity | 无 | 无 | `LeadingActivityTrackerActivity#init；lambda$new$0 / lambda$new$1（onActivityResult 复查）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项说明：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description，实际渲染系统设置→无障碍→已下载的服务中
- 应用内原生 AlertDialog（不可点外部取消，但含 Go back 负向按钮）：LeadingActivityTrackerActivity.init() 中的 MaterialAlertDialogBuilder，标题 @string/grant_required_permission，正文分别取 grant_overlay_permission_message、grant_accessibility_permission_for_tracking_window_contents
- 使用情况访问提示：strings.xml grant_usage_access / grant_usage_acess_message，经 postOnMainThread 弹出
- ADB 无线调试配对教学：strings.xml adb_pairing_instruction / adb_pairing_split_screen_message / manual_wireless_debugging_instructions（与无障碍授权无关，为 ADB 连接引导，含明确替代路径说明）
- 无 assets/ HTML WebView 承载引导、无悬浮窗遮罩引导页、无高仿系统设置页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Generic accessibility service to carry out certain operations such as clearing cache in no-root mode. | 用于在无 root 模式下执行清缓存等特定操作的通用无障碍服务。 | `res/values/strings.xml key=accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 呈现）` | 良性透明说明 |
| en | Grant required permission | 授予所需权限 | `res/values/strings.xml key=grant_required_permission（LeadingActivityTrackerActivity.init 对话框标题）` | 良性透明说明 |
| en | Allow App Manager to utilise the accessibility feature to track the contents of the leading window. | 允许 App Manager 使用无障碍功能跟踪前台窗口的内容。 | `res/values/strings.xml key=grant_accessibility_permission_for_tracking_window_contents` | 良性透明说明 |
| en | Allow App Manager to display a floating window on top of all other windows | 允许 App Manager 在其他所有窗口之上显示悬浮窗 | `res/values/strings.xml key=grant_overlay_permission_message` | 良性透明说明 |
| en | Go back | 返回 | `res/values/strings.xml key=go_back（各授权对话框负向按钮，触发 finish()）` | 良性透明说明 |
| en | Grant usage access | 授予使用情况访问权限 | `res/values/strings.xml key=grant_usage_access（配 grant_usage_acess_message="Used to display app usage info."）` | 良性透明说明 |
| en | Please navigate to the developer options to enable wireless debugging and generate a pairing code. Once a pairing code is generated, enter it in the popup notification to complete pairing. | 请前往开发者选项开启无线调试并生成配对码。生成配对码后，在弹出的通知中输入以完成配对。 | `res/values/strings.xml key=adb_pairing_instruction` | 受限设置分步教学 |
| en | This device supports neither notification-based pairing nor the multi-window mode required to enter a pairing code. As an alternative, you can use ADB over TCP if it has already been enabled. | 此设备既不支持基于通知的配对，也不支持输入配对码所需的多窗口模式。作为替代方案，若已启用 TCP ADB，您可以使用它。 | `res/values/strings.xml key=adb_pairing_unavailable_message` | 受限设置分步教学 |
| en | Actual installer | 实际安装器 | `res/values/strings.xml key=actual_installer（应用详情页安装器来源展示字段）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无拒绝循环。用户在系统设置页未开启即返回时，ActivityResultLauncher 的 onActivityResult（lambda$new$0 / lambda$new$1）会重新调用一次 init() 复查，若仍缺失则再次弹出同一可退出对话框；用户点 Go back 即 finish()，不通过定时器或 onResume 强制重跳。
- **遮罩叠层 / 高仿系统设置页**：无。不叠放半透明引导遮罩、不全屏悬浮窗、不高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于功能性的 TrackerWindow 前台窗口追踪浮窗，且经系统标准授权页申请。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。不存在教用户进应用详情页点右上角菜单开启“允许受限设置”的引导，也不使用 Session 安装器绕过该限制。
- **获权后即时行为与防撤权机制**：无。服务未使用 GLOBAL_ACTION_BACK/HOME 拦截撤权，未监听设置页阻止关闭；自动化点击仅限用户显式开启开关后对 com.android.packageinstaller 安装/卸载对话框（匹配 install/ok）与 com.android.settings 存储页（匹配 storage_settings_for_app）的文本点击。
- **良性降级 / 替代方案**：有。应用主功能默认走 root/ADB（无线调试或 Shizuku）模式；无障碍仅为 no-root 模式的可选替代路径。功能未获权时不启用（AccessibilityMultiplexer 开关保持关闭），用户可直接放弃该功能；ADB 配对流程亦提供 TCP ADB 等替代方案说明。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Activity 组件 LeadingActivityTrackerActivity 启动（透明主题、无界面）时立即开始 UTG 采集；其次以系统 Intent android.settings.ACCESSIBILITY_SETTINGS 被 startActivity 作为辅助触发点（注意冷启动不会触发任何一跳）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一需注意：无障碍服务在用户开启“前台窗口内容追踪”或安装/卸载自动化开关后会对 com.android.settings 与 com.android.packageinstaller 页面执行文本匹配自动点击，若 UTG 采集期间同时开启这些功能，可能出现自动化点击动作被误判为诱导操作，需结合当时功能开关状态区分。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **按需授权弹窗页（第一跳：悬浮窗）** | MaterialAlertDialogBuilder 对话框，标题 Grant required permission，正文含 floating window on top of all other windows，按钮 OK / Go back | 这是该应用唯一的授权引导入口，可判定其是否为串行权限索取、是否存在恐吓话术或不可退出设计 | 对话框是否可点外部/返回键取消；是否存在 Go back 负向按钮；文案是否描述真实用途；是否叠加悬浮遮罩 |
| **按需授权弹窗页（第三跳：无障碍）** | 标题 Grant required permission，正文 track the contents of the leading window，按钮 OK / Go back，随后跳 android.settings.ACCESSIBILITY_SETTINGS | 无障碍授权的关键一跳，用于确认是否存在冒充系统提示、是否有“忽略警告”类话术、是否强制不可跳过 | 点击 OK 后跳转的目标是否确为系统无障碍设置页（包名 com.android.settings）；对话框 setCancelable(false) 是否有等价退出通道；是否同时存在自绘高仿开关控件 |
| **系统无障碍服务列表项** | com.android.settings 无障碍 → 已下载的服务，条目名 App Manager，副标题为 Generic accessibility service to carry out certain operations such as clearing cache in no-root mode. | 核对系统侧呈现的服务名与说明是否与应用真实身份/用途一致，识别身份伪装与说明文字被压缩/同形字替换 | 服务名是否等于应用显示名；description 文案是否被空白/换行截断或改写；是否存在多个同类服务条目 |
| **跳转返回后的行为复查** | 用户从系统设置返回后，是否重新出现同一对话框或直接 finish | 区分“一次性提示 + 可退出”与“onResume 死循环重跳”的诱导模式 | 返回后 1 秒内是否再次弹出同一对话框；是否存在定时器周期性拉起；是否停留在原页面并允许离开 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `io.github.muntashirakon.AppManager.accessibility.activity.LeadingActivityTrackerActivity#init`
- `io.github.muntashirakon.AppManager.accessibility.activity.LeadingActivityTrackerActivity#lambda$init$7$io-github-muntashirakon-AppManager-accessibility-activity-LeadingActivityTrackerActivity`
- `io.github.muntashirakon.AppManager.accessibility.activity.LeadingActivityTrackerActivity#lambda$init$8$io-github-muntashirakon-AppManager-accessibility-activity-LeadingActivityTrackerActivity`
- `io.github.muntashirakon.AppManager.accessibility.BaseAccessibilityService#openAccessibilitySettings`
- `io.github.muntashirakon.AppManager.accessibility.NoRootAccessibilityService#onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**结论：未发现无障碍权限诱导行为，该应用属于良性透明实现。** 核心事实链如下：

**1. 无障碍服务声明与用途说明一致，无伪装**
- [NoRootAccessibilityService 的声明](<resource-unit:#1 manifest:components>) 使用 `BIND_ACCESSIBILITY_SERVICE` 绑定、`exported=false`，并通过 `meta-data` 指向 [res/xml/accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>)；该文件只声明了 `typeAllMask`、`canRetrieveWindowContent=true` 和 `feedbackGeneric`，没有 `android:label`，也没有 `isAccessibilityTool` 等伪造项。
- 系统无障碍列表中显示的服务说明就是应用真实用途：“Generic accessibility service to carry out certain operations such as clearing cache in no-root mode.”（在无 root 模式下执行清缓存等操作）。这段说明与 [NoRootAccessibilityService](<resource-unit:#1.dex1 code:io.github.muntashirakon.AppManager.accessibility.NoRootAccessibilityService>) 的实际能力（自动点击安装/卸载确认、跳转存储页清缓存）完全对应，不存在身份错配。

**2. 冷启动零引导，无任何权限强推**
- [AppManager.onCreate()](<resource-unit:#1.dex1 code:io.github.muntashirakon.AppManager#onCreate>) 只做异常处理、主题初始化和加密 Provider 注册，不会检查或拉起无障碍。
- 全包搜索 `ACTION_ACCESSIBILITY_SETTINGS` 只有 3 处调用点，没有任何冷启动路径。

**3. 唯一“引导页”是用户主动开启功能时的按需串行授权，且每步都可退出**
- 入口是 [LeadingActivityTrackerActivity.init()](<resource-unit:#1.dex1 code:io.github.muntashirakon.AppManager.accessibility.activity.LeadingActivityTrackerActivity#init>)。该 Activity 在 Manifest 中为 `exported=false` 和 `TransparentBackground`，只在用户开启“前台窗口内容追踪”功能时启动，不是桌面入口。
- `init()` 按 悬浮窗 → 使用情况访问 → 无障碍 顺序检查，缺哪项就弹对应的 `MaterialAlertDialogBuilder` 对话框。虽然使用 `setCancelable(false)`，但每个对话框都配了 `go_back` 负向按钮，点击后直接 `finish()` 退出，不存在不可跳过或死循环重跳。
- 无障碍对话框文案为 “Allow App Manager to utilise the accessibility feature to track the contents of the leading window.”（允许 App Manager 使用无障碍功能跟踪前台窗口内容），确认后经 `mSettingsLauncher.launch(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 跳系统无障碍设置页。这是标准系统页，没有高仿界面或遮罩叠层。

**4. 无拒权惩罚、无撤权对抗**
- [BaseAccessibilityService.openAccessibilitySettings()](<resource-unit:#1.dex1 code:io.github.muntashirakon.AppManager.accessibility.BaseAccessibilityService#openAccessibilitySettings>) 只是简单 `startActivity`，无调用者（`find_cross_references` 返回空）。
- 服务内无 `PERFORM_GLOBAL_ACTION` 反向拦截撤权，也没有监听设置页弹回；`automateInstallationUninstallation` / `navigateToStorageAndCache` 只在用户显式打开对应开关（`isInstallEnabled`、`enableNavigateToStorageAndCache`）时，对 `com.android.packageinstaller` 和 `com.android.settings` 页面做文本匹配点击，属功能性自动化。
- 无“允许受限设置”分步教学；`adb_pairing_*` / `manual_wireless_debugging_*` 系列文案是 ADB 无线调试配对说明，与无障碍授权无关，且明确给出替代路径。

**5. 静态完全可见**
无壳、无加密载荷、无 WebView 承载引导文案，全部为原生 Dialog + strings.xml。

**覆盖边界：** 未逐一复核 22 个 `accessibility.activity` 内部类（含 TrackerWindow 悬浮窗渲染），但已确认其均围绕前台窗口追踪功能，未见引导文案承载；`libam.so`/`librun_server.so` 为 ADB/Shizuku 服务端与本地执行引擎，与无障碍诱导无因果关系。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部静态可见：无障碍服务声明、配置 XML、引导对话框逻辑与全部文案均在 DEX 与 res/values/strings.xml 中明文可读，无加壳、无加密载荷、无远端 HTML 承载引导内容。",
  "summary_one_liner": "该应用仅在用户主动开启“前台窗口内容追踪”功能时，通过原生串行对话框按需引导至系统无障碍设置页，每步均提供 Go back 退出，无障碍说明与实际用途一致，属良性透明授权流程。",
  "disguise_identity": {
    "app_display_name": "App Manager",
    "claimed_brand_or_persona": "App Manager（io.github.muntashirakon.AppManager，开源应用管理工具，真实身份）",
    "a11y_service_label": "App Manager（无障碍服务未单独声明 android:label，继承 application 的 @string/app_name）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务未使用空白/换行挤出警告、同形字、多 activity-alias 伪装或伪造 isAccessibilityTool；Manifest 中的 activity-alias（EditorActivity、AppInfoActivity）均为常规功能别名，与应用身份一致。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "io.github.muntashirakon.AppManager.AppManager（Application）→ 各 Activity",
      "trigger_event": "Application.onCreate / 主界面启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动不呈现任何无障碍或权限引导内容",
      "user_action_requested": "无（不请求任何权限）",
      "code_anchor": "io.github.muntashirakon.AppManager.AppManager#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "io.github.muntashirakon.AppManager.accessibility.activity.LeadingActivityTrackerActivity（exported=false，TransparentBackground 主题，excludeFromRecents）",
      "trigger_event": "用户在设置/功能开关中主动启用“前台窗口内容追踪”，Activity 启动后进入 init()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 本身为透明无界面容器，仅承载后续权限检查与对话框",
      "user_action_requested": "无（由用户上一步主动操作触发）",
      "code_anchor": "LeadingActivityTrackerActivity#init / AndroidManifest.xml activity 声明"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "MaterialAlertDialogBuilder 对话框（标题 Grant required permission）→ 系统 ACTION_MANAGE_OVERLAY_PERMISSION 页",
      "trigger_event": "init() 检测 !Settings.canDrawOverlays(this)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Grant required permission / Allow App Manager to display a floating window on top of all other windows / OK / Go back",
      "shown_text_zh": "需要授予权限 / 允许 App Manager 在其他所有窗口之上显示悬浮窗 / 确定 / 返回",
      "user_action_requested": "点击 OK 跳转悬浮窗授权页；点击 Go back 直接 finish() 退出，可取消",
      "code_anchor": "LeadingActivityTrackerActivity#init + lambda$init$2（ACTION_MANAGE_OVERLAY_PERMISSION）+ lambda$init$3（finish）"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "使用情况访问授权（SelfPermissions.checkUsageStatsPermission 为 false 时经 ThreadUtils.postOnMainThread 拉起）",
      "trigger_event": "init() 检测缺少 PACKAGE_USAGE_STATS",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Grant usage access / Used to display app usage info.",
      "shown_text_zh": "授予使用情况访问权限 / 用于显示应用使用信息",
      "user_action_requested": "按提示进入系统使用情况访问设置并开启，可返回取消",
      "code_anchor": "LeadingActivityTrackerActivity#init + lambda$init$6；strings.xml grant_usage_access / grant_usage_acess_message"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "MaterialAlertDialogBuilder 对话框（setCancelable(false)）→ 系统 android.settings.ACCESSIBILITY_SETTINGS 页",
      "trigger_event": "init() 检测 !NoRootAccessibilityService.isAccessibilityEnabled(this)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Grant required permission / Allow App Manager to utilise the accessibility feature to track the contents of the leading window. / OK / Go back",
      "shown_text_zh": "需要授予权限 / 允许 App Manager 使用无障碍功能跟踪前台窗口内容 / 确定 / 返回",
      "user_action_requested": "点击 OK 经 ActivityResultLauncher 跳转系统无障碍设置页并自行开启服务；点击 Go back 直接 finish() 退出",
      "code_anchor": "LeadingActivityTrackerActivity#init + lambda$init$7（ACTION_ACCESSIBILITY_SETTINGS）+ lambda$init$8（finish）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityMultiplexer.getInstance().enableLeadingActivityTracker(true) 后 finish()",
      "trigger_event": "init() 三项检查全部通过（或用户从设置页返回后 onActivityResult 重新调用 init）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "权限齐备后直接启用功能并关闭透明页，无额外提示或跳转",
      "user_action_requested": "无",
      "code_anchor": "LeadingActivityTrackerActivity#init；lambda$new$0 / lambda$new$1（onActivityResult 复查）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项说明：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description，实际渲染系统设置→无障碍→已下载的服务中",
    "应用内原生 AlertDialog（不可点外部取消，但含 Go back 负向按钮）：LeadingActivityTrackerActivity.init() 中的 MaterialAlertDialogBuilder，标题 @string/grant_required_permission，正文分别取 grant_overlay_permission_message、grant_accessibility_permission_for_tracking_window_contents",
    "使用情况访问提示：strings.xml grant_usage_access / grant_usage_acess_message，经 postOnMainThread 弹出",
    "ADB 无线调试配对教学：strings.xml adb_pairing_instruction / adb_pairing_split_screen_message / manual_wireless_debugging_instructions（与无障碍授权无关，为 ADB 连接引导，含明确替代路径说明）",
    "无 assets/ HTML WebView 承载引导、无悬浮窗遮罩引导页、无高仿系统设置页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Generic accessibility service to carry out certain operations such as clearing cache in no-root mode.",
      "text_zh": "用于在无 root 模式下执行清缓存等特定操作的通用无障碍服务。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 呈现）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant required permission",
      "text_zh": "授予所需权限",
      "source_location": "res/values/strings.xml key=grant_required_permission（LeadingActivityTrackerActivity.init 对话框标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow App Manager to utilise the accessibility feature to track the contents of the leading window.",
      "text_zh": "允许 App Manager 使用无障碍功能跟踪前台窗口的内容。",
      "source_location": "res/values/strings.xml key=grant_accessibility_permission_for_tracking_window_contents",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow App Manager to display a floating window on top of all other windows",
      "text_zh": "允许 App Manager 在其他所有窗口之上显示悬浮窗",
      "source_location": "res/values/strings.xml key=grant_overlay_permission_message",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Go back",
      "text_zh": "返回",
      "source_location": "res/values/strings.xml key=go_back（各授权对话框负向按钮，触发 finish()）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant usage access",
      "text_zh": "授予使用情况访问权限",
      "source_location": "res/values/strings.xml key=grant_usage_access（配 grant_usage_acess_message=\"Used to display app usage info.\"）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Please navigate to the developer options to enable wireless debugging and generate a pairing code. Once a pairing code is generated, enter it in the popup notification to complete pairing.",
      "text_zh": "请前往开发者选项开启无线调试并生成配对码。生成配对码后，在弹出的通知中输入以完成配对。",
      "source_location": "res/values/strings.xml key=adb_pairing_instruction",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "This device supports neither notification-based pairing nor the multi-window mode required to enter a pairing code. As an alternative, you can use ADB over TCP if it has already been enabled.",
      "text_zh": "此设备既不支持基于通知的配对，也不支持输入配对码所需的多窗口模式。作为替代方案，若已启用 TCP ADB，您可以使用它。",
      "source_location": "res/values/strings.xml key=adb_pairing_unavailable_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Actual installer",
      "text_zh": "实际安装器",
      "source_location": "res/values/strings.xml key=actual_installer（应用详情页安装器来源展示字段）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无拒绝循环。用户在系统设置页未开启即返回时，ActivityResultLauncher 的 onActivityResult（lambda$new$0 / lambda$new$1）会重新调用一次 init() 复查，若仍缺失则再次弹出同一可退出对话框；用户点 Go back 即 finish()，不通过定时器或 onResume 强制重跳。",
    "overlay_or_fake_settings": "无。不叠放半透明引导遮罩、不全屏悬浮窗、不高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于功能性的 TrackerWindow 前台窗口追踪浮窗，且经系统标准授权页申请。",
    "restricted_settings_13plus_coaching": "无。不存在教用户进应用详情页点右上角菜单开启“允许受限设置”的引导，也不使用 Session 安装器绕过该限制。",
    "post_grant_anti_removal": "无。服务未使用 GLOBAL_ACTION_BACK/HOME 拦截撤权，未监听设置页阻止关闭；自动化点击仅限用户显式开启开关后对 com.android.packageinstaller 安装/卸载对话框（匹配 install/ok）与 com.android.settings 存储页（匹配 storage_settings_for_app）的文本点击。",
    "benign_graceful_degradation": "有。应用主功能默认走 root/ADB（无线调试或 Shizuku）模式；无障碍仅为 no-root 模式的可选替代路径。功能未获权时不启用（AccessibilityMultiplexer 开关保持关闭），用户可直接放弃该功能；ADB 配对流程亦提供 TCP ADB 等替代方案说明。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Activity 组件 LeadingActivityTrackerActivity 启动（透明主题、无界面）时立即开始 UTG 采集；其次以系统 Intent android.settings.ACCESSIBILITY_SETTINGS 被 startActivity 作为辅助触发点（注意冷启动不会触发任何一跳）。",
    "key_pages_to_capture": [
      {
        "page_role": "按需授权弹窗页（第一跳：悬浮窗）",
        "page_identifier": "MaterialAlertDialogBuilder 对话框，标题 Grant required permission，正文含 floating window on top of all other windows，按钮 OK / Go back",
        "why_most_useful": "这是该应用唯一的授权引导入口，可判定其是否为串行权限索取、是否存在恐吓话术或不可退出设计",
        "observable_utg_signals": ["对话框是否可点外部/返回键取消", "是否存在 Go back 负向按钮", "文案是否描述真实用途", "是否叠加悬浮遮罩"]
      },
      {
        "page_role": "按需授权弹窗页（第三跳：无障碍）",
        "page_identifier": "标题 Grant required permission，正文 track the contents of the leading window，按钮 OK / Go back，随后跳 android.settings.ACCESSIBILITY_SETTINGS",
        "why_most_useful": "无障碍授权的关键一跳，用于确认是否存在冒充系统提示、是否有“忽略警告”类话术、是否强制不可跳过",
        "observable_utg_signals": ["点击 OK 后跳转的目标是否确为系统无障碍设置页（包名 com.android.settings）", "对话框 setCancelable(false) 是否有等价退出通道", "是否同时存在自绘高仿开关控件"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍 → 已下载的服务，条目名 App Manager，副标题为 Generic accessibility service to carry out certain operations such as clearing cache in no-root mode.",
        "why_most_useful": "核对系统侧呈现的服务名与说明是否与应用真实身份/用途一致，识别身份伪装与说明文字被压缩/同形字替换",
        "observable_utg_signals": ["服务名是否等于应用显示名", "description 文案是否被空白/换行截断或改写", "是否存在多个同类服务条目"]
      },
      {
        "page_role": "跳转返回后的行为复查",
        "page_identifier": "用户从系统设置返回后，是否重新出现同一对话框或直接 finish",
        "why_most_useful": "区分“一次性提示 + 可退出”与“onResume 死循环重跳”的诱导模式",
        "observable_utg_signals": ["返回后 1 秒内是否再次弹出同一对话框", "是否存在定时器周期性拉起", "是否停留在原页面并允许离开"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一需注意：无障碍服务在用户开启“前台窗口内容追踪”或安装/卸载自动化开关后会对 com.android.settings 与 com.android.packageinstaller 页面执行文本匹配自动点击，若 UTG 采集期间同时开启这些功能，可能出现自动化点击动作被误判为诱导操作，需结合当时功能开关状态区分。"
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
    "io.github.muntashirakon.AppManager.accessibility.activity.LeadingActivityTrackerActivity#init",
    "io.github.muntashirakon.AppManager.accessibility.activity.LeadingActivityTrackerActivity#lambda$init$7$io-github-muntashirakon-AppManager-accessibility-activity-LeadingActivityTrackerActivity",
    "io.github.muntashirakon.AppManager.accessibility.activity.LeadingActivityTrackerActivity#lambda$init$8$io-github-muntashirakon-AppManager-accessibility-activity-LeadingActivityTrackerActivity",
    "io.github.muntashirakon.AppManager.accessibility.BaseAccessibilityService#openAccessibilitySettings",
    "io.github.muntashirakon.AppManager.accessibility.NoRootAccessibilityService#onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
