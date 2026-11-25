# BN_042__c646c2899b｜残障辅助与无障碍支持 — SpeakThat!

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：161.0s

## 1. 一句话核心结论

- **核心申请方式**：SpeakThat! 仅在用户主动进入通用设置或打开 Press to Stop 开关时，弹出带 Cancel 的原生说明弹窗，透明告知无障碍权限完全可选、数据仅本地处理，点击后才跳转系统 ACCESSIBILITY_SETTINGS，无强制、无遮罩、无拒权循环。
- **静态可见性说明**：全部关键逻辑静态可见：Manifest、accessibility_service_config.xml、strings.xml 明文文案、GeneralSettingsActivity/GestureSection 原生弹窗与 Intent 跳转代码均可直接反编译读取；无加壳、无 AES 载荷、无动态加载 dex、无本地/远端 HTML 承载引导文案。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c646c2899b3de1a1aea5470e7d63a58dd1b103898fd6cd3158f9481aae0a0299` |
| 包名 / 年份 | `com.micoyc.speakthat` / 2025-2026 |
| 家族 / 品类 | **残障辅助与无障碍支持**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.micoyc.speakthat_63.apk |
| 桌面显示名 | SpeakThat! |
| 引导页宣称品牌/身份 | SpeakThat!（F-Droid 开源通知朗读应用，真实身份） |
| 系统无障碍列表服务名 | SpeakThat Accessibility |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.micoyc.speakthat.SpeakThatAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `BIND_NOTIFICATION_LISTENER_SERVICE, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Enables advanced control features for SpeakThat including volume button shortcuts to stop/pause notification reading. This service is completely optional and all processing stays on your device. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.micoyc.speakthat.MainActivity → com.micoyc.speakthat.OnboardingActivity（ViewPager2 引导，含 fragment_onboarding_permission 页） | MainActivity.onCreate 检测 !OnboardingActivity.Companion.hasSeenOnboarding() 时 startActivity(OnboardingActivity) 并 finish() | 原生Activity | **原文**：Notification Access Required / SpeakThat requires notifications access to read aloud incoming notifications. / Tip: In the list, tap 'SpeakThat' to enable<br>**译注**：需要通知访问权限 / SpeakThat 需要通知访问权限才能朗读收到的通知 / 提示：在列表中点击“SpeakThat”以启用 | 引导页第 4 页点击 Open Settings 授予“通知使用权”（非无障碍）；Next 按钮在未授权时被拦截但不弹无障碍；有 Back 与跳过路径 | `com.micoyc.speakthat.OnboardingActivity#setupOnboarding$lambda$11；OnboardingPagerAdapterNew$PermissionViewHolder#openNotificationSettings；res/values/strings.xml#onboarding_permission_title` |
| 2 | 引导说明页 | com.micoyc.speakthat.GeneralSettingsActivity 内“Accessibility Permission”行（R.id.buttonAccessibilityPermission） | 用户点击该行 → lambda$setupAccessibilityPermission$18 检测 isAccessibilityServiceEnabled() 为 false 时调用 showAccessibilityPermissionDialog() | 原生Dialog | **原文**：Accessibility Service Permission / SpeakThat! uses the AccessibilityService API to provide optional control features such as pausing speech using hardware buttons and smoother integration with media apps. This permission allows the app to detect button presses and user interface actions, giving you more ways to control readouts. No personal or sensitive user data is collected, stored, or shared — all processing happens entirely on your device. This permission is completely optional; SpeakThat! will still function without it.<br>**译注**：无障碍服务权限 / SpeakThat! 使用 AccessibilityService API 提供可选控制功能，例如用硬件按键暂停朗读、与媒体应用更顺畅地配合。该权限让应用检测按键与界面操作，为你提供更多朗读控制方式。不会收集、存储或共享任何个人或敏感用户数据——所有处理完全在你的设备上进行。该权限完全可选；即使没有它，SpeakThat! 仍可正常工作。 | 可选“Open Accessibility Settings”（正按钮）或“Cancel”（负按钮，listener 为 null 直接关闭） | `com.micoyc.speakthat.GeneralSettingsActivity#showAccessibilityPermissionDialog；res/values/strings.xml#accessibility_permission_explanation_message` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 弹窗正按钮 onClick → lambda$showAccessibilityPermissionDialog$19 | 系统无障碍页 | **原文**：Please find 'SpeakThat Accessibility' in the list and enable it<br>**译注**：请在列表中找到“SpeakThat Accessibility”并启用它（Toast 提示） | 在系统无障碍列表中手动找到 SpeakThat Accessibility 开关并打开；用户可随时返回或按 Home 放弃 | `com.micoyc.speakthat.GeneralSettingsActivity#lambda$showAccessibilityPermissionDialog$19` |
| 4 | 业务功能触发 | com.micoyc.speakthat.settings.sections.GestureSection 中 Press to Stop 开关 | 开关 onCheckedChanged 置为 true 且 isAccessibilityServiceEnabled() 为 false → lambda$bind$10 | 原生Dialog | **原文**：Accessibility Permission Required / Press to Stop requires the accessibility permission to detect volume button presses. Please enable it in General Settings first. / Open Accessibility Settings / Cancel<br>**译注**：需要无障碍权限 / “按键停止”需要无障碍权限来检测音量键按下。请先在通用设置中启用该权限。 / 打开无障碍设置 / 取消 | 可选择跳转设置或取消；无论选择与否开关立即被 setChecked(false) 回退为关闭 | `com.micoyc.speakthat.settings.sections.GestureSection#lambda$bind$10；#showAccessibilityPermissionRequiredDialog；#lambda$showAccessibilityPermissionRequiredDialog$24` |
| 5 | 拒权反馈循环 | GeneralSettingsActivity.onResume / MainActivity.onResume | 从系统设置返回触发 onResume | 原生Activity | **原文**：Accessibility permission granted / Accessibility permission denied<br>**译注**：已授予无障碍权限 / 无障碍权限未授予 | 仅同步状态与徽标，不重复拉起设置页；用户可永久停留在功能关闭状态正常使用通知朗读 | `com.micoyc.speakthat.GeneralSettingsActivity#onResume；com.micoyc.speakthat.permissions.PermissionSyncSession#onResume` |
| 6 | 获权后动作 | com.micoyc.speakthat.SpeakThatAccessibilityService | onServiceConnected / onKeyEvent / onAccessibilityEvent | 原生Activity | 无 | 无；不自动点击确认、不监听设置页阻止撤权 | `com.micoyc.speakthat.SpeakThatAccessibilityService#onServiceConnected；#onKeyEvent；#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- GeneralSettingsActivity 内 R.id.buttonAccessibilityPermission 行下方的说明文字（strings.xml general_accessibility_permission_description：Enable advanced controls like volume button shortcuts (completely optional)）
- GeneralSettingsActivity.showAccessibilityPermissionDialog() 弹出的原生 AlertDialog（可取消，含 Cancel）
- Behavior Settings 页 GestureSection 的 Press to Stop 开关触发的原生 MaterialAlertDialog（可取消，含 Cancel）
- 跳转系统设置后由 Toast 承载的操作指引（“Please find 'SpeakThat Accessibility' in the list and enable it”）
- 系统无障碍列表中的服务条目：label @string/accessibility_service_name = “SpeakThat Accessibility”，description = “Enables advanced control features ... completely optional and all processing stays on your device.”（res/xml/accessibility_service_config.xml 引用）
- OnboardingActivity 引导页（仅通知读取权限相关，含 onboarding_permission_* 系列文案与 bullets），与无障碍权限无关
- 未使用：WebView / 本地或远端 HTML / 悬浮窗遮罩 / 高仿系统无障碍页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility Service Permission | 无障碍服务权限 | `res/values/strings.xml key=accessibility_permission_explanation_title` | 良性透明说明 |
| en | SpeakThat! uses the AccessibilityService API to provide optional control features such as pausing speech using hardware buttons and smoother integration with media apps. This permission allows the app to detect button presses and user interface actions, giving you more ways to control readouts. No personal or sensitive user data is collected, stored, or shared — all processing happens entirely on your device. This permission is completely optional; SpeakThat! will still function without it. | SpeakThat! 使用 AccessibilityService API 提供可选控制功能，例如用硬件按键暂停朗读、与媒体应用更顺畅地配合。该权限让应用检测按键与界面操作，为你提供更多朗读控制方式。不会收集、存储或共享任何个人或敏感用户数据——所有处理完全在你的设备上进行。该权限完全可选；即使没有它，SpeakThat! 仍可正常工作。 | `res/values/strings.xml key=accessibility_permission_explanation_message` | 隐私承诺 |
| en | Enables advanced control features for SpeakThat including volume button shortcuts to stop/pause notification reading. This service is completely optional and all processing stays on your device. | 为 SpeakThat 启用高级控制功能，包括用音量键快捷键停止/暂停通知朗读。该服务完全可选，所有处理都在你的设备上进行。 | `res/values/strings.xml key=accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 引用，显示于系统无障碍列表）` | 良性透明说明 |
| en | Accessibility Permission Required | 需要无障碍权限 | `res/values/strings.xml key=accessibility_permission_required_title` | 受限设置分步教学 |
| en | Press to Stop requires the accessibility permission to detect volume button presses. Please enable it in General Settings first. | “按键停止”需要无障碍权限来检测音量键按下。请先在通用设置中启用该权限。 | `res/values/strings.xml key=accessibility_permission_required_message` | 良性透明说明 |
| en | Open Accessibility Settings | 打开无障碍设置 | `res/values/strings.xml key=accessibility_permission_open_settings / open_accessibility_settings` | 受限设置分步教学 |
| en | Please find 'SpeakThat Accessibility' in the list and enable it | 请在列表中找到“SpeakThat Accessibility”并启用它 | `com.micoyc.speakthat.GeneralSettingsActivity#lambda$showAccessibilityPermissionDialog$19（硬编码 Toast 文案）` | 受限设置分步教学 |
| en | Enable advanced controls like volume button shortcuts (completely optional) | 启用高级控制，如音量键快捷键（完全可选） | `res/values/strings.xml key=general_accessibility_permission_description` | 良性透明说明 |
| en | Accessibility permission granted | 已授予无障碍权限 | `res/values/strings.xml key=accessibility_permission_granted` | 良性透明说明 |
| en | Notification Access Required | 需要通知访问权限 | `res/values/strings.xml key=onboarding_permission_title` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。拒绝（点 Cancel）后弹窗直接关闭；从系统设置返回仅 onResume 刷新状态徽标与 Toast 提示，不重跳设置页，无定时器拉起；Press to Stop 开关在未授权时被强制回退为关闭状态，用户仍可正常使用通知朗读主功能。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 叠层引导，也未实现高仿系统无障碍开关页；全部为原生 AlertDialog + 真实系统设置页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅 setServiceInfo 并读取 Press to Stop 偏好；onAccessibilityEvent 仅把前台包名写入 ForegroundAppTracker；未出现 GLOBAL_ACTION_BACK/HOME、未监听设置页自点确认或阻止撤权。
- **良性降级 / 替代方案**：有。文案明确声明权限完全可选（completely optional；will still function without it），未授权时应用仍可完成通知读取与朗读；Press to Stop 开关在未授权时保持关闭，仅该可选增强功能不可用。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以“GeneralSettingsActivity 中 R.id.buttonAccessibilityPermission 被点击且 isAccessibilityServiceEnabled() 为 false”或“Behavior Settings 中 Press to Stop 开关被置为 true 且未授权”为拉起瞬间；如需捕获完整链路，可在检测到 ACTION_ACCESSIBILITY_SETTINGS 的 startActivity 调用后立即抓取上一页弹窗与随后的系统列表页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一需要注意的弱信号是 accessibility_service_config.xml 声明 canRetrieveWindowContent=true、flagRetrieveInteractiveWindows 与点击/焦点/窗口变化事件，能力面宽于“音量键检测”所述用途；但对应实现仅将前台包名写入 ForegroundAppTracker，未见窗口文本读取或外发，UTG 侧应结合网络流量确认无内容外传。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **按需触发的无障碍说明弹窗页** | GeneralSettingsActivity 上的 AlertDialog，标题“Accessibility Service Permission”，含 Open Accessibility Settings / Cancel 双按钮 | 这是本应用唯一的无障碍权限说明载体，其可取消性、隐私承诺与“完全可选”表述是区分良性透明说明与诱导的关键判别点 | 弹窗标题与正文全文（含 completely optional 与本地处理声明）；存在可点击的 Cancel 负按钮；无悬浮窗/无全屏遮罩层节点；正按钮文案为 Open Accessibility Settings 而非伪装按钮 |
| **功能开关触发的权限要求弹窗页** | Press to Stop 开关旁弹出的 MaterialAlertDialog，标题“Accessibility Permission Required” | 验证是否为“用户主动开启功能才索取权限”的按需模式，并可直接观察开关是否被回退，排除强制引导 | 弹窗原文“Please enable it in General Settings first.”；开关控件状态在弹窗关闭后为未选中；无自动跳转、无倒计时按钮 |
| **系统无障碍服务列表项** | Settings → Accessibility 中条目“SpeakThat Accessibility”，描述为 “Enables advanced control features ... completely optional and all processing stays on your device.” | 核对服务标签与描述是否与真实身份/用途一致，确认无系统或品牌仿冒 | 服务名称与 app 名称一致（SpeakThat）；描述文本含 completely optional 与本地处理声明；同页不存在同名多实例或多 alias 条目 |
| **跳转设置后的 Toast 指引与返回态** | Toast 文本“Please find 'SpeakThat Accessibility' in the list and enable it”；返回后 GeneralSettingsActivity 状态行 | 确认拒绝/返回后无死循环重跳，验证拒权反馈为一次性提示 | 返回后 5 秒内未再次出现 ACCESSIBILITY_SETTINGS 页面；无 overlay 窗口节点；状态徽标显示未授予而非阻断性遮罩 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.micoyc.speakthat.GeneralSettingsActivity#lambda$setupAccessibilityPermission$18`
- `com.micoyc.speakthat.GeneralSettingsActivity#showAccessibilityPermissionDialog`
- `com.micoyc.speakthat.GeneralSettingsActivity#lambda$showAccessibilityPermissionDialog$19`
- `com.micoyc.speakthat.settings.sections.GestureSection#lambda$bind$10`
- `com.micoyc.speakthat.settings.sections.GestureSection#showAccessibilityPermissionRequiredDialog`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（Manifest、无障碍服务实现、三处跳转点、文案资源），结论如下。

## 结论要点

- **无障碍申请路径完全由用户按需触发，不存在冷启动强制引导**：冷启动只有通知读取权限的 Onboarding（`OnboardingActivity`，第 4 页“Notification Access Required”，未授予则 Next 被拦），**该页与无障碍服务无关**；无障碍权限只在“通用设置”入口与“Press to Stop”开关两处按需弹出。
- **两个引导弹窗均为原生 `AlertDialog`，都带 `Cancel` 取消按钮**：`GeneralSettingsActivity.showAccessibilityPermissionDialog()`（标题 `Accessibility Service Permission`）与 `GestureSection.showAccessibilityPermissionRequiredDialog()`（标题 `Accessibility Permission Required`），点“打开无障碍设置”后直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，并 `Toast` 提示“在列表中找 'SpeakThat Accessibility' 并启用”。
- **文案高度透明**：明确写“此权限完全可选，无此权限 SpeakThat! 仍可正常工作”“不收集/不存储/不共享任何个人敏感数据，全部处理在设备本地完成”，与 `android:description`、服务标签一致，无假更新/故障恐吓/假安全等话术。
- **无诱导技术特征**：无悬浮窗遮罩、无高仿系统无障碍页、无 `ACTION_APPLICATION_DETAILS_SETTINGS`（无 Android 13 受限设置教学）、无拒绝后 `onResume` 死循环重跳、无获权后自点确认或 `GLOBAL_ACTION_BACK` 阻止撤权；`onAccessibilityEvent` 仅把前台包名写入 `ForegroundAppTracker`，`onKeyEvent` 仅在开关打开时拦截音量键。
- **一处可记录的能力面观察（非诱导风险）**：`accessibility_service_config.xml` 开启 `canRetrieveWindowContent="true"`、`flagRetrieveInteractiveWindows` 与点击/焦点/窗口变化事件，能力面大于“音量键检测”所述用途，但实际处理仅限前台包名追踪，未发现读取窗口文本外发。
- **静态可见性完整**：无加壳（预筛 `False` 一致）、无动态加载、无 WebView/远端 HTML 承载引导文案。

## 关键证据链

1. `MainActivity.onCreate` → 未见 `hasSeenOnboarding` → `OnboardingActivity`；`OnboardingActivity.checkAndUpdatePermissionStatus`/`setupOnboarding$lambda$11` 仅校验**通知监听**权限。
2. `GeneralSettingsActivity.onCreate` → `setupAccessibilityPermission()` 仅绑定 `buttonAccessibilityPermission` 点击监听 → `lambda$setupAccessibilityPermission$18` 判断 `isAccessibilityServiceEnabled()`，未启用才 `showAccessibilityPermissionDialog()`。
3. 弹窗正按钮 `lambda$showAccessibilityPermissionDialog$19` → 跳 `ACCESSIBILITY_SETTINGS` + Toast。
4. `GestureSection.lambda$bind$10`（开关打开且未授权）→ `showAccessibilityPermissionRequiredDialog()` 且 `setChecked(false)` 回退，`lambda$showAccessibilityPermissionRequiredDialog$24` 跳同一设置页。
5. `SpeakThatAccessibilityService.onServiceConnected/onKeyEvent/onAccessibilityEvent`：仅音量键（24/25）双击判定与前台包名上报，无越权动作。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键逻辑静态可见：Manifest、accessibility_service_config.xml、strings.xml 明文文案、GeneralSettingsActivity/GestureSection 原生弹窗与 Intent 跳转代码均可直接反编译读取；无加壳、无 AES 载荷、无动态加载 dex、无本地/远端 HTML 承载引导文案。",
  "summary_one_liner": "SpeakThat! 仅在用户主动进入通用设置或打开 Press to Stop 开关时，弹出带 Cancel 的原生说明弹窗，透明告知无障碍权限完全可选、数据仅本地处理，点击后才跳转系统 ACCESSIBILITY_SETTINGS，无强制、无遮罩、无拒权循环。",
  "disguise_identity": {
    "app_display_name": "SpeakThat!",
    "claimed_brand_or_persona": "SpeakThat!（F-Droid 开源通知朗读应用，真实身份）",
    "a11y_service_label": "SpeakThat Accessibility",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.micoyc.speakthat.MainActivity → com.micoyc.speakthat.OnboardingActivity（ViewPager2 引导，含 fragment_onboarding_permission 页）",
      "trigger_event": "MainActivity.onCreate 检测 !OnboardingActivity.Companion.hasSeenOnboarding() 时 startActivity(OnboardingActivity) 并 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Notification Access Required / SpeakThat requires notifications access to read aloud incoming notifications. / Tip: In the list, tap 'SpeakThat' to enable",
      "shown_text_zh": "需要通知访问权限 / SpeakThat 需要通知访问权限才能朗读收到的通知 / 提示：在列表中点击“SpeakThat”以启用",
      "user_action_requested": "引导页第 4 页点击 Open Settings 授予“通知使用权”（非无障碍）；Next 按钮在未授权时被拦截但不弹无障碍；有 Back 与跳过路径",
      "code_anchor": "com.micoyc.speakthat.OnboardingActivity#setupOnboarding$lambda$11；OnboardingPagerAdapterNew$PermissionViewHolder#openNotificationSettings；res/values/strings.xml#onboarding_permission_title"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.micoyc.speakthat.GeneralSettingsActivity 内“Accessibility Permission”行（R.id.buttonAccessibilityPermission）",
      "trigger_event": "用户点击该行 → lambda$setupAccessibilityPermission$18 检测 isAccessibilityServiceEnabled() 为 false 时调用 showAccessibilityPermissionDialog()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Accessibility Service Permission / SpeakThat! uses the AccessibilityService API to provide optional control features such as pausing speech using hardware buttons and smoother integration with media apps. This permission allows the app to detect button presses and user interface actions, giving you more ways to control readouts. No personal or sensitive user data is collected, stored, or shared — all processing happens entirely on your device. This permission is completely optional; SpeakThat! will still function without it.",
      "shown_text_zh": "无障碍服务权限 / SpeakThat! 使用 AccessibilityService API 提供可选控制功能，例如用硬件按键暂停朗读、与媒体应用更顺畅地配合。该权限让应用检测按键与界面操作，为你提供更多朗读控制方式。不会收集、存储或共享任何个人或敏感用户数据——所有处理完全在你的设备上进行。该权限完全可选；即使没有它，SpeakThat! 仍可正常工作。",
      "user_action_requested": "可选“Open Accessibility Settings”（正按钮）或“Cancel”（负按钮，listener 为 null 直接关闭）",
      "code_anchor": "com.micoyc.speakthat.GeneralSettingsActivity#showAccessibilityPermissionDialog；res/values/strings.xml#accessibility_permission_explanation_message"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "弹窗正按钮 onClick → lambda$showAccessibilityPermissionDialog$19",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please find 'SpeakThat Accessibility' in the list and enable it",
      "shown_text_zh": "请在列表中找到“SpeakThat Accessibility”并启用它（Toast 提示）",
      "user_action_requested": "在系统无障碍列表中手动找到 SpeakThat Accessibility 开关并打开；用户可随时返回或按 Home 放弃",
      "code_anchor": "com.micoyc.speakthat.GeneralSettingsActivity#lambda$showAccessibilityPermissionDialog$19"
    },
    {
      "step": 4,
      "stage": "业务功能触发",
      "screen_or_component": "com.micoyc.speakthat.settings.sections.GestureSection 中 Press to Stop 开关",
      "trigger_event": "开关 onCheckedChanged 置为 true 且 isAccessibilityServiceEnabled() 为 false → lambda$bind$10",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Accessibility Permission Required / Press to Stop requires the accessibility permission to detect volume button presses. Please enable it in General Settings first. / Open Accessibility Settings / Cancel",
      "shown_text_zh": "需要无障碍权限 / “按键停止”需要无障碍权限来检测音量键按下。请先在通用设置中启用该权限。 / 打开无障碍设置 / 取消",
      "user_action_requested": "可选择跳转设置或取消；无论选择与否开关立即被 setChecked(false) 回退为关闭",
      "code_anchor": "com.micoyc.speakthat.settings.sections.GestureSection#lambda$bind$10；#showAccessibilityPermissionRequiredDialog；#lambda$showAccessibilityPermissionRequiredDialog$24"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "GeneralSettingsActivity.onResume / MainActivity.onResume",
      "trigger_event": "从系统设置返回触发 onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility permission granted / Accessibility permission denied",
      "shown_text_zh": "已授予无障碍权限 / 无障碍权限未授予",
      "user_action_requested": "仅同步状态与徽标，不重复拉起设置页；用户可永久停留在功能关闭状态正常使用通知朗读",
      "code_anchor": "com.micoyc.speakthat.GeneralSettingsActivity#onResume；com.micoyc.speakthat.permissions.PermissionSyncSession#onResume"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.micoyc.speakthat.SpeakThatAccessibilityService",
      "trigger_event": "onServiceConnected / onKeyEvent / onAccessibilityEvent",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面文案；仅设置服务信息、拦截音量键（24/25）组合、把前台包名写入 ForegroundAppTracker",
      "user_action_requested": "无；不自动点击确认、不监听设置页阻止撤权",
      "code_anchor": "com.micoyc.speakthat.SpeakThatAccessibilityService#onServiceConnected；#onKeyEvent；#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "GeneralSettingsActivity 内 R.id.buttonAccessibilityPermission 行下方的说明文字（strings.xml general_accessibility_permission_description：Enable advanced controls like volume button shortcuts (completely optional)）",
    "GeneralSettingsActivity.showAccessibilityPermissionDialog() 弹出的原生 AlertDialog（可取消，含 Cancel）",
    "Behavior Settings 页 GestureSection 的 Press to Stop 开关触发的原生 MaterialAlertDialog（可取消，含 Cancel）",
    "跳转系统设置后由 Toast 承载的操作指引（“Please find 'SpeakThat Accessibility' in the list and enable it”）",
    "系统无障碍列表中的服务条目：label @string/accessibility_service_name = “SpeakThat Accessibility”，description = “Enables advanced control features ... completely optional and all processing stays on your device.”（res/xml/accessibility_service_config.xml 引用）",
    "OnboardingActivity 引导页（仅通知读取权限相关，含 onboarding_permission_* 系列文案与 bullets），与无障碍权限无关",
    "未使用：WebView / 本地或远端 HTML / 悬浮窗遮罩 / 高仿系统无障碍页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service Permission",
      "text_zh": "无障碍服务权限",
      "source_location": "res/values/strings.xml key=accessibility_permission_explanation_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "SpeakThat! uses the AccessibilityService API to provide optional control features such as pausing speech using hardware buttons and smoother integration with media apps. This permission allows the app to detect button presses and user interface actions, giving you more ways to control readouts. No personal or sensitive user data is collected, stored, or shared — all processing happens entirely on your device. This permission is completely optional; SpeakThat! will still function without it.",
      "text_zh": "SpeakThat! 使用 AccessibilityService API 提供可选控制功能，例如用硬件按键暂停朗读、与媒体应用更顺畅地配合。该权限让应用检测按键与界面操作，为你提供更多朗读控制方式。不会收集、存储或共享任何个人或敏感用户数据——所有处理完全在你的设备上进行。该权限完全可选；即使没有它，SpeakThat! 仍可正常工作。",
      "source_location": "res/values/strings.xml key=accessibility_permission_explanation_message",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Enables advanced control features for SpeakThat including volume button shortcuts to stop/pause notification reading. This service is completely optional and all processing stays on your device.",
      "text_zh": "为 SpeakThat 启用高级控制功能，包括用音量键快捷键停止/暂停通知朗读。该服务完全可选，所有处理都在你的设备上进行。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（经 res/xml/accessibility_service_config.xml android:description 引用，显示于系统无障碍列表）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Permission Required",
      "text_zh": "需要无障碍权限",
      "source_location": "res/values/strings.xml key=accessibility_permission_required_title",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Press to Stop requires the accessibility permission to detect volume button presses. Please enable it in General Settings first.",
      "text_zh": "“按键停止”需要无障碍权限来检测音量键按下。请先在通用设置中启用该权限。",
      "source_location": "res/values/strings.xml key=accessibility_permission_required_message",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Accessibility Settings",
      "text_zh": "打开无障碍设置",
      "source_location": "res/values/strings.xml key=accessibility_permission_open_settings / open_accessibility_settings",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please find 'SpeakThat Accessibility' in the list and enable it",
      "text_zh": "请在列表中找到“SpeakThat Accessibility”并启用它",
      "source_location": "com.micoyc.speakthat.GeneralSettingsActivity#lambda$showAccessibilityPermissionDialog$19（硬编码 Toast 文案）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable advanced controls like volume button shortcuts (completely optional)",
      "text_zh": "启用高级控制，如音量键快捷键（完全可选）",
      "source_location": "res/values/strings.xml key=general_accessibility_permission_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility permission granted",
      "text_zh": "已授予无障碍权限",
      "source_location": "res/values/strings.xml key=accessibility_permission_granted",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Notification Access Required",
      "text_zh": "需要通知访问权限",
      "source_location": "res/values/strings.xml key=onboarding_permission_title",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。拒绝（点 Cancel）后弹窗直接关闭；从系统设置返回仅 onResume 刷新状态徽标与 Toast 提示，不重跳设置页，无定时器拉起；Press to Stop 开关在未授权时被强制回退为关闭状态，用户仍可正常使用通知朗读主功能。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 叠层引导，也未实现高仿系统无障碍开关页；全部为原生 AlertDialog + 真实系统设置页。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。onServiceConnected 仅 setServiceInfo 并读取 Press to Stop 偏好；onAccessibilityEvent 仅把前台包名写入 ForegroundAppTracker；未出现 GLOBAL_ACTION_BACK/HOME、未监听设置页自点确认或阻止撤权。",
    "benign_graceful_degradation": "有。文案明确声明权限完全可选（completely optional；will still function without it），未授权时应用仍可完成通知读取与朗读；Press to Stop 开关在未授权时保持关闭，仅该可选增强功能不可用。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以“GeneralSettingsActivity 中 R.id.buttonAccessibilityPermission 被点击且 isAccessibilityServiceEnabled() 为 false”或“Behavior Settings 中 Press to Stop 开关被置为 true 且未授权”为拉起瞬间；如需捕获完整链路，可在检测到 ACTION_ACCESSIBILITY_SETTINGS 的 startActivity 调用后立即抓取上一页弹窗与随后的系统列表页。",
    "key_pages_to_capture": [
      {
        "page_role": "按需触发的无障碍说明弹窗页",
        "page_identifier": "GeneralSettingsActivity 上的 AlertDialog，标题“Accessibility Service Permission”，含 Open Accessibility Settings / Cancel 双按钮",
        "why_most_useful": "这是本应用唯一的无障碍权限说明载体，其可取消性、隐私承诺与“完全可选”表述是区分良性透明说明与诱导的关键判别点",
        "observable_utg_signals": ["弹窗标题与正文全文（含 completely optional 与本地处理声明）", "存在可点击的 Cancel 负按钮", "无悬浮窗/无全屏遮罩层节点", "正按钮文案为 Open Accessibility Settings 而非伪装按钮"]
      },
      {
        "page_role": "功能开关触发的权限要求弹窗页",
        "page_identifier": "Press to Stop 开关旁弹出的 MaterialAlertDialog，标题“Accessibility Permission Required”",
        "why_most_useful": "验证是否为“用户主动开启功能才索取权限”的按需模式，并可直接观察开关是否被回退，排除强制引导",
        "observable_utg_signals": ["弹窗原文“Please enable it in General Settings first.”", "开关控件状态在弹窗关闭后为未选中", "无自动跳转、无倒计时按钮"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility 中条目“SpeakThat Accessibility”，描述为 “Enables advanced control features ... completely optional and all processing stays on your device.”",
        "why_most_useful": "核对服务标签与描述是否与真实身份/用途一致，确认无系统或品牌仿冒",
        "observable_utg_signals": ["服务名称与 app 名称一致（SpeakThat）", "描述文本含 completely optional 与本地处理声明", "同页不存在同名多实例或多 alias 条目"]
      },
      {
        "page_role": "跳转设置后的 Toast 指引与返回态",
        "page_identifier": "Toast 文本“Please find 'SpeakThat Accessibility' in the list and enable it”；返回后 GeneralSettingsActivity 状态行",
        "why_most_useful": "确认拒绝/返回后无死循环重跳，验证拒权反馈为一次性提示",
        "observable_utg_signals": ["返回后 5 秒内未再次出现 ACCESSIBILITY_SETTINGS 页面", "无 overlay 窗口节点", "状态徽标显示未授予而非阻断性遮罩"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一需要注意的弱信号是 accessibility_service_config.xml 声明 canRetrieveWindowContent=true、flagRetrieveInteractiveWindows 与点击/焦点/窗口变化事件，能力面宽于“音量键检测”所述用途；但对应实现仅将前台包名写入 ForegroundAppTracker，未见窗口文本读取或外发，UTG 侧应结合网络流量确认无内容外传。"
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
    "com.micoyc.speakthat.GeneralSettingsActivity#lambda$setupAccessibilityPermission$18",
    "com.micoyc.speakthat.GeneralSettingsActivity#showAccessibilityPermissionDialog",
    "com.micoyc.speakthat.GeneralSettingsActivity#lambda$showAccessibilityPermissionDialog$19",
    "com.micoyc.speakthat.settings.sections.GestureSection#lambda$bind$10",
    "com.micoyc.speakthat.settings.sections.GestureSection#showAccessibilityPermissionRequiredDialog",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

本次核验未发现可单独定级的诱导/欺诈风险命题，故未写入风险台账；唯一遗留观察为无障碍服务能力声明偏宽（`canRetrieveWindowContent=true`）但实现未使用窗口文本，属能力面与描述不完全对齐，未构成恶意行为，已在上文与 JSON 盲区说明中记录。

</details>
