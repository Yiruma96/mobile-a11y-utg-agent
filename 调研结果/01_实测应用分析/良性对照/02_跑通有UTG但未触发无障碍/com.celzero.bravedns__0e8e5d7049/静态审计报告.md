# BN_068__0e8e5d7049｜隐私指示与安全防护工具 — Rethink

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：109.3s

## 1. 一句话核心结论

- **核心申请方式**：Rethink 在用户主动开启通用防火墙的“后台应用阻断”开关时才弹出不可取消但可取消操作的原生说明弹窗，用透明口径解释无障碍仅用于前台/后台判定并跳转系统无障碍设置，拒绝后自动复位开关并安全降级，无伪装、无遮罩、无重跳循环。
- **静态可见性说明**：无障碍权限引导全链路静态可见：Manifest 服务声明、accessibility_service_config.xml、strings.xml 文案、UniversalFirewallSettingsActivity.recheckFirewallBackgroundMode 弹窗与 ACCESSIBILITY_SETTINGS 跳转、onResume 回读与降级逻辑均在 DEX 与资源中完整还原；未发现加壳、AES 载荷、远端 HTML 或动态加载引导页。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0e8e5d70496b506038ca4afaef868fadaac6e0b5416b80aa6e139174fa181004` |
| 包名 / 年份 | `com.celzero.bravedns` / 2025-2026 |
| 家族 / 品类 | **隐私指示与安全防护工具**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.celzero.bravedns_709.apk |
| 桌面显示名 | Rethink |
| 引导页宣称品牌/身份 | Rethink: DNS + Firewall + VPN（F-Droid 开源隐私防护工具，真实身份） |
| 系统无障碍列表服务名 | Rethink |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务标签、android:description 与弹窗正文口径一致，均如实说明“用于识别前台/后台应用以实施防火墙，不收集不出售信息”；应用内的 activity-alias（com.celzero.bravedns.ui.LauncherAliasHome / LauncherAliasAppLock）服务于应用锁的图标隐藏功能，不参与无障碍引导，也未用于混淆无障碍入口。 |
| 无障碍服务类名 | `com.celzero.bravedns.util.BackgroundAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Rethink uses accessibility service to detect and firewall background applications. Rethink does not collect or sell any information. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.celzero.bravedns.ui.HomeScreenActivity（单 Task 主界面） | onCreate/onResume | 原生Activity | **原文**：无（冷启动不弹任何无障碍引导）<br>**译注**：冷启动仅展示主界面与 VPN 状态，不主动索取无障碍权限 | 无 | `com.celzero.bravedns.ui.HomeScreenActivity.onCreate / onResume` |
| 2 | 业务功能触发 | com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity（通用防火墙设置页） | 用户点击“Block apps when not in use”开关或该行文字（$$ExternalSyntheticLambda2.onClick case 12/13） | 原生Activity | **原文**：无（页面为常规设置项列表）<br>**译注**：用户主动进入设置开启“后台应用阻断”功能 | 点击开关（可随时返回，无强制） | `com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity$$ExternalSyntheticLambda2.onClick` |
| 3 | 引导说明页 | MaterialAlertDialog（AlertController$AlertParams.mCancelable = false） | recheckFirewallBackgroundMode(true) 中 isAccessibilityServiceEnabled 与 isAccessibilityServiceEnabledViaSettingsSecure 均为 false | 原生Dialog | **原文**：Title: Permission - Accessibility / Message: Rethink uses accessibility service to track which apps are in-use (foreground) versus those that are not in-use (background).<br><br>Rethink does not collect any information or spy on you in any way. / Positive: univ_accessibility_dialog_positive / Negative: univ_accessibility_dialog_negative<br>**译注**：标题“权限 - 无障碍”；正文“Rethink 使用无障碍服务来判断哪些应用正在使用（前台）、哪些未在使用（后台）。Rethink 不会收集任何信息，也不会以任何方式窥探你。”；正按钮为继续/前往设置（univ_accessibility_dialog_positive），负按钮为取消（univ_accessibility_dialog_negative，本次未逐字读取其文本） | 可点正按钮前往系统无障碍设置，也可点负按钮取消（有取消路径；但返回键/点击外部无法关闭该弹窗） | `com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity#recheckFirewallBackgroundMode（strings: alert_permission_accessibility / alert_firewall_accessibility_explanation / univ_accessibility_dialog_positive / univ_accessibility_dialog_negative）` |
| 4 | 跳无障碍设置 | 系统设置：android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表，显示标签 Rethink） | 弹窗正按钮 onClick（CaptureManager$$ExternalSyntheticLambda2，classId 8） | 系统无障碍页 | **原文**：Rethink uses accessibility service to detect and firewall background applications. Rethink does not collect or sell any information.<br>**译注**：系统无障碍列表中该服务下方说明：“Rethink 使用无障碍服务检测并对后台应用实施防火墙。Rethink 不收集、不出售任何信息。” | 用户在系统页手动找到 Rethink 并打开开关；失败时 Toast 提示 Failure opening Accessibility Settings. Try again later! | `com.journeyapps.barcodescanner.CaptureManager$$ExternalSyntheticLambda2#onClick / res/xml/accessibility_service_config.xml（android:description=@string/accessibility_service_description）` |
| 5 | 拒权反馈循环 | UniversalFirewallSettingsActivity.onResume + Toast | 从系统设置返回（onResume）且 blockAppWhenBackground 为 true 但服务仍未启用 | 原生Activity | **原文**：Rethink accessibility service has stopped or crashed. No longer blocking backgrounded apps.<br>**译注**：“Rethink 无障碍服务已停止或崩溃，不再阻断后台应用。”——随后自动把开关与持久化状态复位为关闭 | 无强制重试；用户可稍后再次手动开启，不会自动重跳设置页 | `com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity#onResume（strings: accessibility_failure_toast）` |
| 6 | 获权后动作 | com.celzero.bravedns.util.BackgroundAccessibilityService + com.celzero.bravedns.service.BraveVPNService + 通知栏 | 服务被系统绑定后 onAccessibilityEvent(typeAllMask) 回调；服务被系统杀死/崩溃时 AccessibilityStateChangeListener | 通知栏 | **原文**：Rethink accessibility service has stopped or crashed. No longer blocking backgrounded apps. Tap to re-enable.<br>**译注**：服务异常停止时发通知：“Rethink 无障碍服务已停止或崩溃，不再阻断后台应用。点击重新启用。”——点击进入应用恢复，非自授权、非阻止撤权 | 点击通知回到应用重新开启（用户主动操作） | `com.celzero.bravedns.util.BackgroundAccessibilityService#onAccessibilityEvent / com.celzero.bravedns.service.BraveVPNService#accessibilityServiceFunctional / #handleAccessibilityFailure` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- UniversalFirewallSettingsActivity 内 MaterialAlertDialog（mCancelable=false）标题与正文：Permission - Accessibility / alert_firewall_accessibility_explanation
- 系统无障碍服务列表条目说明：res/xml/accessibility_service_config.xml 的 android:description → @string/accessibility_service_description
- 系统无障碍列表中服务名称：Manifest 中 service android:label="@string/app_name"（显示为 Rethink）
- UniversalFirewallSettingsActivity.onResume 的居中 Toast：@string/accessibility_failure_toast
- 通知栏通知正文（服务崩溃/停止时）：@string/accessibility_notification_content
- 跳转系统设置失败时的 Toast：@string/alert_firewall_accessibility_exception
- res/values/strings.xml 中另存有 alert_firewall_accessibility_regrant_explanation（引导用户去设置强制停止后重启以恢复该功能，属常规故障提示，未在本次核验的弹窗路径中调用）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Rethink uses accessibility service to detect and firewall background applications. Rethink does not collect or sell any information. | Rethink 使用无障碍服务来检测并对后台应用实施防火墙。Rethink 不收集、不出售任何信息。 | `res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）` | 良性透明说明 |
| en | Rethink uses accessibility service to track which apps are in-use (foreground) versus those that are not in-use (background).<br><br>Rethink does not collect any information or spy on you in any way. | Rethink 使用无障碍服务来区分哪些应用正在使用（前台）、哪些未在使用（后台）。Rethink 不会收集任何信息，也不会以任何方式窥探你。 | `res/values/strings.xml → alert_firewall_accessibility_explanation（UniversalFirewallSettingsActivity.recheckFirewallBackgroundMode 弹窗正文）` | 良性透明说明 |
| en | Permission - Accessibility | 权限 - 无障碍 | `res/values/strings.xml → alert_permission_accessibility（弹窗标题）` | 良性透明说明 |
| en | Rethink accessibility service has stopped or crashed. No longer blocking backgrounded apps. | Rethink 无障碍服务已停止或崩溃。不再阻断后台应用。 | `res/values/strings.xml → accessibility_failure_toast（onResume 降级 Toast）` | 良性透明说明 |
| en | Rethink accessibility service has stopped or crashed. No longer blocking backgrounded apps. Tap to re-enable. | Rethink 无障碍服务已停止或崩溃。不再阻断后台应用。点击以重新启用。 | `res/values/strings.xml → accessibility_notification_content（通知栏）` | 良性透明说明 |
| en | Failure opening Accessibility Settings. Try again later! | 打开无障碍设置失败，请稍后再试！ | `res/values/strings.xml → alert_firewall_accessibility_exception（ActivityNotFoundException 分支 Toast）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无重跳循环。用户从系统设置返回后 onResume 仅回读状态：若服务未启用则把 blockAppWhenBackground 复位为 false、开关置灰关闭并弹一次 accessibility_failure_toast，界面停留在通用防火墙设置页，用户可继续使用其余规则或稍后再开；未使用定时器、通知或 onResume 死循环强行拉起设置页。
- **遮罩叠层 / 高仿系统设置页**：无。跳转后不叠加半透明遮罩、不绘制全屏悬浮窗、不伪造系统无障碍开关页；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现引导进入“应用详情 → 右上角菜单 → 允许受限设置”的分步教学，也无 Session 安装器绕过逻辑。
- **获权后即时行为与防撤权机制**：无。获权后不自点确认、不自行授权；BraveVPNService 仅在服务异常停止时发通知提示用户手动重新开启，未监听设置页执行 GLOBAL_ACTION_BACK/HOME 阻止撤权。
- **良性降级 / 替代方案**：有。无障碍未开启时“后台应用阻断”开关自动复位并保持关闭，防火墙其余规则（DNS 拦截、按应用联网、锁定模式等）继续可用；用户亦可仅使用 VPN/DNS 模式而不开启无障碍。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到宿主进程 startActivity 携带 action=android.settings.ACCESSIBILITY_SETTINGS 的瞬间（唯一跳转点位于 CaptureManager$$ExternalSyntheticLambda2.onClick 的 classId 8 分支），并在其前 300–800ms 抓取同进程弹出的 Dialog 窗口；若需覆盖功能入口，可在用户点击 UniversalFirewallSettingsActivity 中“Block apps when not in use”开关时立即采样。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。本应用未加壳、无密文载荷、无远端 HTML 引导页，弹窗为系统原生 MaterialAlertDialog，文本可被 UTG 直接提取。唯一需注意的温和点：弹窗设置 mCancelable=false（返回键不可关闭），若检测器仅以“能否用返回键关闭”判断强制程度会误报，应同时检查是否存在负按钮；另 activity-alias（LauncherAliasHome/LauncherAliasAppLock）会在桌面图标层面切换入口，但不影响无障碍引导路径的捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **引导说明弹窗页（跳转前唯一文案载体）** | 包名 com.celzero.bravedns 的 Dialog 窗口，标题文本 Permission - Accessibility，正/负两按钮 | 该弹窗是应用唯一向用户解释无障碍用途的界面，其文案、按钮数量与可取消性直接决定是“透明说明+可取消”还是“无退出诱导” | 标题与正文完整文本可提取（含 Rethink does not collect any information 声明）；按钮节点数量为 2（存在负按钮=存在取消路径）；弹窗是否可通过返回键关闭（mCancelable=false 的可见表现） |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中 label=Rethink 的服务条目及其 summary 文本 | 用于核验系统侧展示的服务名与说明是否与应用内声称一致，识别标签冒充或说明空洞 | 服务条目 label 文本 = Rethink；summary 文本是否包含用途与不收集声明；列表是否出现多个同名/相似名服务条目 |
| **跳转设置页后返回的降级反馈页** | 返回 com.celzero.bravedns 通用防火墙设置页，开关处于关闭态并出现 Toast | 区分“拒权后死循环重跳”与“良性安全降级”，是判定诱导强度差异的关键观测点 | 返回后是否再次出现无障碍弹窗或直接再次跳系统设置；前台 Activity 是否为 UniversalFirewallSettingsActivity 且开关未勾选；Toast 文本是否为 accessibility_failure_toast |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity#recheckFirewallBackgroundMode`
- `com.journeyapps.barcodescanner.CaptureManager$$ExternalSyntheticLambda2#onClick`
- `com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity#onResume`
- `com.celzero.bravedns.util.BackgroundAccessibilityService#onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml（accessibility_service_description / alert_firewall_accessibility_explanation / accessibility_notification_content）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **纯运行期引导路径已完整静态还原**：没有加壳、没有密文加载、没有远端 HTML，也没有 WebView 或悬浮窗参与无障碍权限引导。整个过程由原生 `MaterialAlertDialog`、`Intent` 和系统无障碍设置页构成。
- **触发时机为“按需（用户打开功能开关）”**：入口是 `Universal Firewall`（通用防火墙）设置页中的“Block apps when not in use / 后台应用阻断”开关，冷启动时不会弹出任何无障碍引导。
- **关键实现**：[UniversalFirewallSettingsActivity.recheckFirewallBackgroundMode()](<resource-unit:#1.dex1 code:com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity#recheckFirewallBackgroundMode>) 检测 `Utilities.isAccessibilityServiceEnabled` 与 `isAccessibilityServiceEnabledViaSettingsSecure` 均未开启后，弹出**不可通过返回键或点击外部取消**的对话框（`mCancelable = false`），标题 `Permission - Accessibility`，正文为“仅用于区分前台/后台应用 + 不收集不窥探”的透明说明；正按钮回调 [CaptureManager$$ExternalSyntheticLambda2.onClick](<resource-unit:#1.dex1 code:com.journeyapps.barcodescanner.CaptureManager$$ExternalSyntheticLambda2#onClick>)（`$r8$classId == 8` 分支）直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，负按钮为“取消”。
- **拒绝或返回后不会形成死循环**：`onResume` 只做状态回读，若服务未开启则把开关复位为关闭，并弹出 toast `accessibility_failure_toast`；没有定时器重新拉起设置页，也没有 `GLOBAL_ACTION_BACK/HOME` 阻止撤权，也没有 13+ 受限设置分步教学。
- **身份真实、无伪装**：显示名 `Rethink`、服务标签 `Rethink`、`android:description` 与弹窗正文口径一致，均明示用途且声明不收集信息；`activity-alias`（`LauncherAliasHome`/`LauncherAliasAppLock`）属于应用锁的图标切换功能，与本条无障碍引导无关。
- **权限面偏宽但用途可解释**：`accessibility_service_config.xml` 声明 `typeAllMask`、`canRetrieveWindowContent`、`flagRetrieveInteractiveWindows`，实际 [BackgroundAccessibilityService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.celzero.bravedns.util.BackgroundAccessibilityService#onAccessibilityEvent>) 仅用于前台/后台判定；属功能必要能力，非隐蔽采集。
- **结论：本专题（无障碍权限诱导）不成立风险命题**，未登记风险；仅存在“弹窗不可取消”这一轻度强制感设计，已由负按钮与安全降级抵消。

## 逐步引导流程（UTG 视角）

| 步 | 阶段 | 组件 | 触发 | 载体 |
|---|---|---|---|---|
| 1 | 业务功能触发 | `HomeScreenActivity` → Universal Firewall 设置 | 用户进入设置 | 原生 Activity |
| 2 | 引导说明页（弹窗） | `UniversalFirewallSettingsActivity` 内 `MaterialAlertDialog`（不可取消） | 点击“Block apps when not in use”开关或其文字 | 原生 Dialog |
| 3 | 跳受限设置（无障碍页） | `android.settings.ACCESSIBILITY_SETTINGS` | 弹窗正按钮 | 系统无障碍页 |
| 4 | 拒权反馈 | `onResume` 复位开关 + Toast | 从设置页返回且服务未开 | 原生 Toast |
| 5 | 获权后动作 | `BraveVPNService.accessibilityServiceFunctional` 生效后台阻断；服务崩溃时通知栏“Tap to re-enable” | 服务已启用/异常停止 | 通知栏 |

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍权限引导全链路静态可见：Manifest 服务声明、accessibility_service_config.xml、strings.xml 文案、UniversalFirewallSettingsActivity.recheckFirewallBackgroundMode 弹窗与 ACCESSIBILITY_SETTINGS 跳转、onResume 回读与降级逻辑均在 DEX 与资源中完整还原；未发现加壳、AES 载荷、远端 HTML 或动态加载引导页。",
  "summary_one_liner": "Rethink 在用户主动开启通用防火墙的“后台应用阻断”开关时才弹出不可取消但可取消操作的原生说明弹窗，用透明口径解释无障碍仅用于前台/后台判定并跳转系统无障碍设置，拒绝后自动复位开关并安全降级，无伪装、无遮罩、无重跳循环。",
  "disguise_identity": {
    "app_display_name": "Rethink",
    "claimed_brand_or_persona": "Rethink: DNS + Firewall + VPN（F-Droid 开源隐私防护工具，真实身份）",
    "a11y_service_label": "Rethink",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务标签、android:description 与弹窗正文口径一致，均如实说明“用于识别前台/后台应用以实施防火墙，不收集不出售信息”；应用内的 activity-alias（com.celzero.bravedns.ui.LauncherAliasHome / LauncherAliasAppLock）服务于应用锁的图标隐藏功能，不参与无障碍引导，也未用于混淆无障碍入口。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.celzero.bravedns.ui.HomeScreenActivity（单 Task 主界面）",
      "trigger_event": "onCreate/onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（冷启动不弹任何无障碍引导）",
      "shown_text_zh": "冷启动仅展示主界面与 VPN 状态，不主动索取无障碍权限",
      "user_action_requested": "无",
      "code_anchor": "com.celzero.bravedns.ui.HomeScreenActivity.onCreate / onResume"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity（通用防火墙设置页）",
      "trigger_event": "用户点击“Block apps when not in use”开关或该行文字（$$ExternalSyntheticLambda2.onClick case 12/13）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（页面为常规设置项列表）",
      "shown_text_zh": "用户主动进入设置开启“后台应用阻断”功能",
      "user_action_requested": "点击开关（可随时返回，无强制）",
      "code_anchor": "com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity$$ExternalSyntheticLambda2.onClick"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "MaterialAlertDialog（AlertController$AlertParams.mCancelable = false）",
      "trigger_event": "recheckFirewallBackgroundMode(true) 中 isAccessibilityServiceEnabled 与 isAccessibilityServiceEnabledViaSettingsSecure 均为 false",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: Permission - Accessibility / Message: Rethink uses accessibility service to track which apps are in-use (foreground) versus those that are not in-use (background).\n\nRethink does not collect any information or spy on you in any way. / Positive: univ_accessibility_dialog_positive / Negative: univ_accessibility_dialog_negative",
      "shown_text_zh": "标题“权限 - 无障碍”；正文“Rethink 使用无障碍服务来判断哪些应用正在使用（前台）、哪些未在使用（后台）。Rethink 不会收集任何信息，也不会以任何方式窥探你。”；正按钮为继续/前往设置（univ_accessibility_dialog_positive），负按钮为取消（univ_accessibility_dialog_negative，本次未逐字读取其文本）",
      "user_action_requested": "可点正按钮前往系统无障碍设置，也可点负按钮取消（有取消路径；但返回键/点击外部无法关闭该弹窗）",
      "code_anchor": "com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity#recheckFirewallBackgroundMode（strings: alert_permission_accessibility / alert_firewall_accessibility_explanation / univ_accessibility_dialog_positive / univ_accessibility_dialog_negative）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置：android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表，显示标签 Rethink）",
      "trigger_event": "弹窗正按钮 onClick（CaptureManager$$ExternalSyntheticLambda2，classId 8）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Rethink uses accessibility service to detect and firewall background applications. Rethink does not collect or sell any information.",
      "shown_text_zh": "系统无障碍列表中该服务下方说明：“Rethink 使用无障碍服务检测并对后台应用实施防火墙。Rethink 不收集、不出售任何信息。”",
      "user_action_requested": "用户在系统页手动找到 Rethink 并打开开关；失败时 Toast 提示 Failure opening Accessibility Settings. Try again later!",
      "code_anchor": "com.journeyapps.barcodescanner.CaptureManager$$ExternalSyntheticLambda2#onClick / res/xml/accessibility_service_config.xml（android:description=@string/accessibility_service_description）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "UniversalFirewallSettingsActivity.onResume + Toast",
      "trigger_event": "从系统设置返回（onResume）且 blockAppWhenBackground 为 true 但服务仍未启用",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Rethink accessibility service has stopped or crashed. No longer blocking backgrounded apps.",
      "shown_text_zh": "“Rethink 无障碍服务已停止或崩溃，不再阻断后台应用。”——随后自动把开关与持久化状态复位为关闭",
      "user_action_requested": "无强制重试；用户可稍后再次手动开启，不会自动重跳设置页",
      "code_anchor": "com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity#onResume（strings: accessibility_failure_toast）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.celzero.bravedns.util.BackgroundAccessibilityService + com.celzero.bravedns.service.BraveVPNService + 通知栏",
      "trigger_event": "服务被系统绑定后 onAccessibilityEvent(typeAllMask) 回调；服务被系统杀死/崩溃时 AccessibilityStateChangeListener",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Rethink accessibility service has stopped or crashed. No longer blocking backgrounded apps. Tap to re-enable.",
      "shown_text_zh": "服务异常停止时发通知：“Rethink 无障碍服务已停止或崩溃，不再阻断后台应用。点击重新启用。”——点击进入应用恢复，非自授权、非阻止撤权",
      "user_action_requested": "点击通知回到应用重新开启（用户主动操作）",
      "code_anchor": "com.celzero.bravedns.util.BackgroundAccessibilityService#onAccessibilityEvent / com.celzero.bravedns.service.BraveVPNService#accessibilityServiceFunctional / #handleAccessibilityFailure"
    }
  ],
  "text_presentation_locations": [
    "UniversalFirewallSettingsActivity 内 MaterialAlertDialog（mCancelable=false）标题与正文：Permission - Accessibility / alert_firewall_accessibility_explanation",
    "系统无障碍服务列表条目说明：res/xml/accessibility_service_config.xml 的 android:description → @string/accessibility_service_description",
    "系统无障碍列表中服务名称：Manifest 中 service android:label=\"@string/app_name\"（显示为 Rethink）",
    "UniversalFirewallSettingsActivity.onResume 的居中 Toast：@string/accessibility_failure_toast",
    "通知栏通知正文（服务崩溃/停止时）：@string/accessibility_notification_content",
    "跳转系统设置失败时的 Toast：@string/alert_firewall_accessibility_exception",
    "res/values/strings.xml 中另存有 alert_firewall_accessibility_regrant_explanation（引导用户去设置强制停止后重启以恢复该功能，属常规故障提示，未在本次核验的弹窗路径中调用）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Rethink uses accessibility service to detect and firewall background applications. Rethink does not collect or sell any information.",
      "text_zh": "Rethink 使用无障碍服务来检测并对后台应用实施防火墙。Rethink 不收集、不出售任何信息。",
      "source_location": "res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Rethink uses accessibility service to track which apps are in-use (foreground) versus those that are not in-use (background).\n\nRethink does not collect any information or spy on you in any way.",
      "text_zh": "Rethink 使用无障碍服务来区分哪些应用正在使用（前台）、哪些未在使用（后台）。Rethink 不会收集任何信息，也不会以任何方式窥探你。",
      "source_location": "res/values/strings.xml → alert_firewall_accessibility_explanation（UniversalFirewallSettingsActivity.recheckFirewallBackgroundMode 弹窗正文）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Permission - Accessibility",
      "text_zh": "权限 - 无障碍",
      "source_location": "res/values/strings.xml → alert_permission_accessibility（弹窗标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Rethink accessibility service has stopped or crashed. No longer blocking backgrounded apps.",
      "text_zh": "Rethink 无障碍服务已停止或崩溃。不再阻断后台应用。",
      "source_location": "res/values/strings.xml → accessibility_failure_toast（onResume 降级 Toast）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Rethink accessibility service has stopped or crashed. No longer blocking backgrounded apps. Tap to re-enable.",
      "text_zh": "Rethink 无障碍服务已停止或崩溃。不再阻断后台应用。点击以重新启用。",
      "source_location": "res/values/strings.xml → accessibility_notification_content（通知栏）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Failure opening Accessibility Settings. Try again later!",
      "text_zh": "打开无障碍设置失败，请稍后再试！",
      "source_location": "res/values/strings.xml → alert_firewall_accessibility_exception（ActivityNotFoundException 分支 Toast）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无重跳循环。用户从系统设置返回后 onResume 仅回读状态：若服务未启用则把 blockAppWhenBackground 复位为 false、开关置灰关闭并弹一次 accessibility_failure_toast，界面停留在通用防火墙设置页，用户可继续使用其余规则或稍后再开；未使用定时器、通知或 onResume 死循环强行拉起设置页。",
    "overlay_or_fake_settings": "无。跳转后不叠加半透明遮罩、不绘制全屏悬浮窗、不伪造系统无障碍开关页；跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无。未出现引导进入“应用详情 → 右上角菜单 → 允许受限设置”的分步教学，也无 Session 安装器绕过逻辑。",
    "post_grant_anti_removal": "无。获权后不自点确认、不自行授权；BraveVPNService 仅在服务异常停止时发通知提示用户手动重新开启，未监听设置页执行 GLOBAL_ACTION_BACK/HOME 阻止撤权。",
    "benign_graceful_degradation": "有。无障碍未开启时“后台应用阻断”开关自动复位并保持关闭，防火墙其余规则（DNS 拦截、按应用联网、锁定模式等）继续可用；用户亦可仅使用 VPN/DNS 模式而不开启无障碍。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到宿主进程 startActivity 携带 action=android.settings.ACCESSIBILITY_SETTINGS 的瞬间（唯一跳转点位于 CaptureManager$$ExternalSyntheticLambda2.onClick 的 classId 8 分支），并在其前 300–800ms 抓取同进程弹出的 Dialog 窗口；若需覆盖功能入口，可在用户点击 UniversalFirewallSettingsActivity 中“Block apps when not in use”开关时立即采样。",
    "key_pages_to_capture": [
      {
        "page_role": "引导说明弹窗页（跳转前唯一文案载体）",
        "page_identifier": "包名 com.celzero.bravedns 的 Dialog 窗口，标题文本 Permission - Accessibility，正/负两按钮",
        "why_most_useful": "该弹窗是应用唯一向用户解释无障碍用途的界面，其文案、按钮数量与可取消性直接决定是“透明说明+可取消”还是“无退出诱导”",
        "observable_utg_signals": ["标题与正文完整文本可提取（含 Rethink does not collect any information 声明）", "按钮节点数量为 2（存在负按钮=存在取消路径）", "弹窗是否可通过返回键关闭（mCancelable=false 的可见表现）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中 label=Rethink 的服务条目及其 summary 文本",
        "why_most_useful": "用于核验系统侧展示的服务名与说明是否与应用内声称一致，识别标签冒充或说明空洞",
        "observable_utg_signals": ["服务条目 label 文本 = Rethink", "summary 文本是否包含用途与不收集声明", "列表是否出现多个同名/相似名服务条目"]
      },
      {
        "page_role": "跳转设置页后返回的降级反馈页",
        "page_identifier": "返回 com.celzero.bravedns 通用防火墙设置页，开关处于关闭态并出现 Toast",
        "why_most_useful": "区分“拒权后死循环重跳”与“良性安全降级”，是判定诱导强度差异的关键观测点",
        "observable_utg_signals": ["返回后是否再次出现无障碍弹窗或直接再次跳系统设置", "前台 Activity 是否为 UniversalFirewallSettingsActivity 且开关未勾选", "Toast 文本是否为 accessibility_failure_toast"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。本应用未加壳、无密文载荷、无远端 HTML 引导页，弹窗为系统原生 MaterialAlertDialog，文本可被 UTG 直接提取。唯一需注意的温和点：弹窗设置 mCancelable=false（返回键不可关闭），若检测器仅以“能否用返回键关闭”判断强制程度会误报，应同时检查是否存在负按钮；另 activity-alias（LauncherAliasHome/LauncherAliasAppLock）会在桌面图标层面切换入口，但不影响无障碍引导路径的捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity#recheckFirewallBackgroundMode",
    "com.journeyapps.barcodescanner.CaptureManager$$ExternalSyntheticLambda2#onClick",
    "com.celzero.bravedns.ui.activity.UniversalFirewallSettingsActivity#onResume",
    "com.celzero.bravedns.util.BackgroundAccessibilityService#onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml（accessibility_service_description / alert_firewall_accessibility_explanation / accessibility_notification_content）"
  ]
}
```

</details>
