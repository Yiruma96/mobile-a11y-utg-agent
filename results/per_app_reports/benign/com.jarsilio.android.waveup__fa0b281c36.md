# BN_011__fa0b281c36｜按键映射与手势导航 — WaveUp

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：202.9s

## 1. 一句话核心结论

- **核心申请方式**：WaveUp 仅在用户主动开启“锁屏”功能时，以透明开源说明弹窗提示用户前往系统无障碍页手动授权，并因 Google Play 政策在本构建中实际关闭了该无障碍服务，拒绝后安全降级为设备管理员或关闭选项。
- **静态可见性说明**：无障碍引导相关代码、Manifest 声明、accessibility_service_config.xml 与全部提示文案均在本地明文 DEX/资源中完整可见，无加壳、无 AES 密文载荷、无远端 HTML。唯一运行期差异是该构建 use_accessibility_service_to_lock=false，使无障碍服务未在系统列表中启用，属产品变体开关而非隐藏逻辑。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fa0b281c36cd66e7f0844402b5ce2d02d72b2f0160fd2a013c6ce68449d99e1a` |
| 包名 / 年份 | `com.jarsilio.android.waveup` / 2025-2026 |
| 家族 / 品类 | **按键映射与手势导航**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.jarsilio.android.waveup_145.apk |
| 桌面显示名 | WaveUp |
| 引导页宣称品牌/身份 | WaveUp（开源挥手亮屏/锁屏工具，com.jarsilio.android.waveup） |
| 系统无障碍列表服务名 | WaveUp（android:label="@string/app_name"，与桌面名一致） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务标签与桌面名一致，无空白/换行挤出警告、无同形字、无多 activity-alias 伪装；R8 混淆仅作用于普通代码（r8-map-id），非身份伪装；无伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.jarsilio.android.waveup.service.LockAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：@7F130140 |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.jarsilio.android.waveup.MainActivity（承载 MainActivity$SettingsFragment 设置页） | onCreate；仅当 Intent action 为 com.jarsilio.android.waveup.action.REQUEST_LOCK_PERMISSIONS（由 ShortcutActivity 快捷方式下发）时才进入授权引导分支，普通点击图标冷启动不弹无障碍引导 | 原生Activity | **原文**：Starting WaveUp MainActivity (GUI)<br>**译注**：日志：启动 WaveUp 主界面；普通冷启动仅加载设置页与“喜欢就支持一下”/无近距传感器提示，不涉及无障碍 | 无强制操作；可正常浏览设置项 | `com.jarsilio.android.waveup.MainActivity.onCreate` |
| 2 | 业务功能触发 | 设置页锁屏开关 pref_lock_screen（MainActivity$SettingsFragment） | onSharedPreferenceChanged 检测到 pref_lock_screen 变为 true 且 isLockScreen() 为真 | 原生Activity | **原文**：Showing dialog to see if the user wants to open Android's 'Accessibility Settings'<br>**译注**：日志：弹出对话框询问用户是否愿意打开安卓“无障碍设置”；仅在用户主动开启锁屏功能时才引导 | 用户主动打开锁屏开关（按需触发，非强制） | `com.jarsilio.android.waveup.MainActivity$SettingsFragment.onSharedPreferenceChanged` |
| 3 | 引导说明页 | MaterialAlertDialogBuilder 原生弹窗（标题缺省，正文为 accessibility_service_explanation） | PermissionsHandler.openLockDevicePermissionExplanationIfNecessary 在 isPieOrNewer 且 isAccessibilityServiceEnabled() 为 false 时构建并 show() | 原生Dialog | **原文**：Lock device: Accessibility Service / In order to lock the screen, we need to set WaveUp as an 'Accessibility Service'. Granting an app Accessibility Service allows it to spy on the user if it wants to. It also allows an app to use specific functions that wouldn't be available if not. For example WaveUp uses the AccessibilityService."GLOBAL_ACTION_LOCK_SCREEN" to lock the screen. Please think twice before trusting apps! WaveUp is open source software so please go ahead and check the code (or ask a friend to do it) to make sure we are not doing anything evil (we promise we are not, but you really shouldn't take our word for it). Do you want to set WaveUp as an Accessibility Service? You'll have to grant the privileges manually in the next screen.<br>**译注**：锁屏功能：无障碍服务。为了锁屏，需要把 WaveUp 设为“无障碍服务”。授予无障碍会让应用有能力窥探用户；同时也能使用原本不可用的特定功能，例如 WaveUp 使用 GLOBAL_ACTION_LOCK_SCREEN 锁屏。信任应用前请三思！WaveUp 是开源软件，欢迎自行（或请朋友）检查代码确认我们没有做坏事（我们保证没有，但你真的不该只听我们说）。是否将 WaveUp 设为无障碍服务？你需要在下一个界面手动授予权限。 | 确定（android.R.string.ok）/ 取消（android.R.string.cancel）；弹窗 mCancelable=false（点外部不消失）但提供可用的取消按钮 | `com.jarsilio.android.waveup.PermissionsHandler.openLockDevicePermissionExplanationIfNecessary；res/values/strings.xml#L30-L40` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 用户点击弹窗“确定”后 PermissionsHandler$$ExternalSyntheticLambda0.onClick（case 1）执行 startActivityForResult(Intent, 500) | 系统无障碍页 | **原文**：Opening Android's 'Accessibility Settings' activity<br>**译注**：日志：打开安卓无障碍设置界面；由用户点击触发，无悬浮遮罩、无高仿设置页覆盖 | 用户自行在系统无障碍列表中找到 WaveUp 并手动开启（该构建中该服务因 bool=false 未声明启用，实际列表可能不出现该项） | `com.jarsilio.android.waveup.PermissionsHandler$$ExternalSyntheticLambda0.onClick` |
| 5 | 拒权反馈循环 | 返回 MainActivity（onActivityResult requestCode=500） | 从系统设置返回后回调 onActivityResult(500, ...) | 原生Activity | **原文**：The user didn't enable the AccessibilityService. Won't be able to lock device.<br>**译注**：日志：用户未启用无障碍服务，将无法锁屏；随后调用 setLockScreen() 关闭锁屏选项，不重跳设置页、不再弹引导 | 无需操作；应用自动安全降级（关闭锁屏功能） | `com.jarsilio.android.waveup.MainActivity.onActivityResult` |
| 6 | 获权后动作 | ProximitySensorHandler.startOrStopListeningDependingOnConditions / LockAccessibilityService | onActivityResult(500) 检测到 isAccessibilityServiceEnabled() 为 true 后启动近距传感器监听；实际锁屏通过无障碍服务 GLOBAL_ACTION_LOCK_SCREEN 执行 | Service | **原文**：WaveUp Lock Command<br>**译注**：无障碍服务描述文案“WaveUp 锁屏命令”；获权后仅恢复近距传感器监听与锁屏动作，无自动点击确认、无监听设置页阻止撤权 | 无 | `com.jarsilio.android.waveup.MainActivity.onActivityResult；com.jarsilio.android.waveup.service.LockAccessibilityService.onAccessibilityEvent` |
| 7 | 拒权反馈循环 | 设置页 onResume 的 MaterialAlertDialogBuilder（标题 something_went_wrong） | SettingsFragment.onResume 发现 pref_lock_screen 为 true 但无障碍（Pie+）或设备管理员（Pie 前）权限缺失 | 原生Dialog | **原文**：WaveUp had to disable the 'lock' option due to a missing Accessibility Service permission. Please re-enable the option and set WaveUp as an Accessibility Service.<br>**译注**：由于缺少无障碍服务权限，WaveUp 不得不关闭“锁屏”选项。请重新开启该选项并把 WaveUp 设为无障碍服务。 | 仅“确定”按钮（mCancelable=false）；仅告知状态回退，不自动跳转、不循环重弹 | `com.jarsilio.android.waveup.MainActivity$SettingsFragment.onResume；res/values/strings.xml#L157` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内的 MaterialAlertDialogBuilder 原生弹窗：正文为 res/values/strings.xml 的 accessibility_service_explanation（开启锁屏功能时出现，含 OK/Cancel，点外部不消失）
- SettingsFragment.onResume 的“Something went wrong”原生弹窗：正文为 lock_disabled_warning_accessibility_settings_text（权限被收回后告知选项已被关闭）
- 系统无障碍列表条目：服务 android:label="@string/app_name"（WaveUp），说明由 res/xml/accessibility_service_config.xml 提供（未配置 android:description，description 为空）
- res/values/strings.xml 中 accessibility_service_text="WaveUp Lock Command"（无障碍相关短描述文案）
- 应用内帮助/FAQ 的 HTML 文本（com.jarsilio.android.common.html.HtmlTextActivity + 资源内嵌 HTML 字符串，如 ACRA/数据收集说明），非无障碍授权诱导载体
- 无 assets 下的引导 HTML/WebView、无悬浮窗遮罩、无伪造无障碍开关页、无图片引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Lock device: Accessibility Service — In order to lock the screen, we need to set WaveUp as an 'Accessibility Service'. Granting an app Accessibility Service allows it to spy on the user if it wants to. It also allows an app to use specific functions that wouldn't be available if not. For example WaveUp uses the AccessibilityService."GLOBAL_ACTION_LOCK_SCREEN" to lock the screen. Please think twice before trusting apps! WaveUp is open source software so please go ahead and check the code (or ask a friend to do it) to make sure we are not doing anything evil (we promise we are not, but you really shouldn't take our word for it). Do you want to set WaveUp as an Accessibility Service? You'll have to grant the privileges manually in the next screen. | 锁屏功能：无障碍服务——为了锁屏，需要把 WaveUp 设为“无障碍服务”。授予无障碍会让应用有能力窥探用户；也能使用原本不可用的特定功能，例如 WaveUp 使用 GLOBAL_ACTION_LOCK_SCREEN 锁屏。信任应用前请三思！WaveUp 是开源软件，欢迎自行（或请朋友）检查代码确认我们没有做坏事（我们保证没有，但你真的不该只听我们说）。是否将 WaveUp 设为无障碍服务？你需要在下一个界面手动授予权限。 | `res/values/strings.xml key=accessibility_service_explanation（#L30-L40）` | 良性透明说明 |
| en | WaveUp had to disable the 'lock' option due to a missing Accessibility Service permission. Please re-enable the option and set WaveUp as an Accessibility Service. | 由于缺少无障碍服务权限，WaveUp 不得不关闭“锁屏”选项。请重新开启该选项并把 WaveUp 设为无障碍服务。 | `res/values/strings.xml key=lock_disabled_warning_accessibility_settings_text（#L157），由 MainActivity$SettingsFragment.onResume 展示` | 良性透明说明 |
| en | Unfortunately the ✌️, 🦋, ❤, and 🔒 version of the app currently violate the Google Play policy because of an issue with Violation of... | 遗憾的是，✌️、🦋、❤、🔒 等版本的应用目前因违反 Google Play 政策而被下架/不合规…… | `res/values/strings.xml（预筛命中 DEFAULT 文案，说明锁屏相关变体因 Play 政策移除）` | 良性透明说明 |
| en | In order to lock the screen, we need to set WaveUp as a 'Device Administrator'. Once an app is a Device Administrator... | 为了锁屏，需要把 WaveUp 设为“设备管理员”。一旦应用成为设备管理员…… | `res/values/strings.xml key=lock_admin_rights_explanation（Pie 之前版本的替代说明）` | 受限设置分步教学 |
| en | WaveUp Lock Command | WaveUp 锁屏命令 | `res/values/strings.xml key=accessibility_service_text` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。用户取消弹窗则完全不跳转；从系统设置返回后 onActivityResult(500) 检测未启用即记录日志并 setLockScreen() 关闭锁屏选项，不重跳设置页；SettingsFragment.onResume 仅弹一次“Something went wrong”告知选项已被关闭（mCancelable=false，仅 OK），需用户手动再次开启开关才会重新出现引导。
- **遮罩叠层 / 高仿系统设置页**：无。无 SYSTEM_ALERT_WINDOW 悬浮遮罩、无半透明引导层、无高仿系统无障碍开关页，跳转即真实 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无“点右上角菜单允许受限设置”或 Session 安装器绕过教学。
- **获权后即时行为与防撤权机制**：无。获权后仅启动近距传感器监听与 GLOBAL_ACTION_LOCK_SCREEN 锁屏；无自动点击确认、无监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权（LockAccessibilityService 仅监听 typeNotificationStateChanged 且 packageNames 限定自身、canRetrieveWindowContent=false）。
- **良性降级 / 替代方案**：有。无障碍不可用/被拒绝时自动 setLockScreen() 关闭该选项，锁屏可改用设备管理员（LockScreenAdminReceiver，ACTION_ADD_DEVICE_ADMIN，requestCode 100）或直接关闭功能；本构建 bool use_accessibility_service_to_lock=false，即以非无障碍变体发布。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS（requestCode=500）的瞬间拉起 UTG 抓取跳转前弹窗与随后系统页；或监测 MainActivity 收到 action=com.jarsilio.android.waveup.action.REQUEST_LOCK_PERMISSIONS 的冷启动。普通点击图标冷启动不会弹无障碍引导，无需在冷启动 0 步抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一需注意：本构建 use_accessibility_service_to_lock=false，无障碍服务未在系统列表启用，纯 UTG 运行期可能完全看不到无障碍授权流程（引导代码为编译保留分支），此时应以 Manifest/bools/strings 静态证据判定，不应因“未见引导”而误判为隐藏行为；另无加壳/密文/远端 HTML 遮挡。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前引导弹窗页** | MaterialAlertDialog，正文含 "Lock device: Accessibility Service" / "GLOBAL_ACTION_LOCK_SCREEN" / "Please think twice before trusting apps!"，按钮 OK 与 Cancel | 该弹窗是全部无障碍引导文案的唯一载体，可直接判断话术是透明说明还是恐吓/伪装 | 文本包含 "Accessibility Service" 与 "spy on the user" 等风险自陈；同时存在 OK 与 Cancel 两个可点击按钮；无标题或标题为空、点外部不消失（mCancelable=false） |
| **系统无障碍服务列表项** | 设置页 com.android.settings/.Settings$AccessibilitySettingsActivity，列表项标签 WaveUp（如出现） | 核验服务是否真实注册、显示名是否与桌面名一致、描述是否为空 | 列表项文本为 WaveUp（无空白/换行挤出）；副标题/描述为空；该构建 bool=false 时列表可能无此条目 |
| **拒权返回后的设置页与回退提示** | WaveUp 设置页 + 标题 Something went wrong 的弹窗，正文含 "had to disable the 'lock' option" | 验证拒绝后是安全降级还是循环重跳，是区分良性/胁迫的关键 | 返回后停留在 WaveUp 设置页而非再次跳系统设置；锁屏开关呈关闭态；仅一个 OK 按钮 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.jarsilio.android.waveup.PermissionsHandler.openLockDevicePermissionExplanationIfNecessary`
- `com.jarsilio.android.waveup.PermissionsHandler$$ExternalSyntheticLambda0.onClick`
- `com.jarsilio.android.waveup.MainActivity.onActivityResult`
- `com.jarsilio.android.waveup.MainActivity$SettingsFragment.onSharedPreferenceChanged`
- `com.jarsilio.android.waveup.MainActivity$SettingsFragment.onResume`
- `res/xml/accessibility_service_config.xml / res/values/bools.xml / res/values/strings.xml#L30-L40`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**这是一次透明的、由功能按需触发的无障碍授权流程，未发现诱导或欺诈特征。**

- **服务声明极简**：`LockAccessibilityService` 的配置仅监听 `typeNotificationStateChanged`、`packageNames` 限定为本应用自身、`canRetrieveWindowContent="false"`，没有任何读取窗口内容或监听全局事件的能力；其唯一用途是调用 `GLOBAL_ACTION_LOCK_SCREEN` 锁屏。见 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>)。
- **关键事实：当前构建未启用无障碍服务**。[bools.xml](<resource-unit:#1 file:res/values/bools.xml>) 中 `use_accessibility_service_to_lock=false`，Manifest 里 `android:enabled="@bool/use_accessibility_service_to_lock"`，因此系统无障碍列表中实际上不会出现该服务；这与资源里“某些版本因 Google Play 政策违规而移除”的说明一致，说明本包属于合规变体（锁屏回落到设备管理员或普通模式）。
- **触发时机是“用户主动打开锁屏开关”**，不是冷启动就弹出：[MainActivity$SettingsFragment#onSharedPreferenceChanged](<resource-unit:#1.dex1 code:com.jarsilio.android.waveup.MainActivity$SettingsFragment#onSharedPreferenceChanged>) 监听 `pref_lock_screen`，置为 true 后才调用 [PermissionsHandler#openLockDevicePermissionExplanationIfNecessary()](<resource-unit:#1.dex1 code:com.jarsilio.android.waveup.PermissionsHandler#openLockDevicePermissionExplanationIfNecessary>)。
- **说明文案高度透明且主动警示风险**：文案标题为 “Lock device: Accessibility Service”，明确告知“授予无障碍会让应用有能力窥探用户”，提示“信任应用前请三思”，并声明开源、请自行核查代码；无假更新、故障恐吓、清理工具伪装等话术。
- **跳转仅由用户点击“确定”触发**：[PermissionsHandler$$ExternalSyntheticLambda0#onClick](<resource-unit:#1.dex1 code:com.jarsilio.android.waveup.PermissionsHandler$$ExternalSyntheticLambda0#onClick>) 中 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 500)`，仅此一处跳转；未使用 `ACTION_APPLICATION_DETAILS_SETTINGS`，也没有 13+ 受限设置（Restricted Settings）分步教学。
- **拒绝或返回后安全降级，没有循环重跳**：[MainActivity#onActivityResult](<resource-unit:#1.dex1 code:com.jarsilio.android.waveup.MainActivity#onActivityResult>) 在 requestCode 500 返回时检查 `isAccessibilityServiceEnabled()`，若未开启仅日志记录并 `setLockScreen()` 关闭该选项，不重跳、不弹二次引导。
- **没有遮罩、没有伪造设置页、没有防撤权**：无 `SYSTEM_ALERT_WINDOW` 悬浮窗引导层，无高仿无障碍开关页，无 `PERFORM_GLOBAL_ACTION` 监听撤权，也没有 `setComponentEnabledSetting` 对自身组件做伪装或隐藏；`setComponentEnabledSetting` 仅用于动态启停 `CallStateReceiver`（通话中暂停监听）。
- **弹窗不可点击外部关闭但提供“取消”**：`mCancelable=false`，但 Positive=OK、Negative=Cancel 均存在，用户可拒绝。
- **唯一“恐吓式”文案属良性功能回退提示**：设置页 `onResume` 中，如果用户曾开启锁屏但权限被收回，会强制关闭该选项，并弹出 “Something went wrong” + “WaveUp had to disable the 'lock' option due to a missing Accessibility Service permission. Please re-enable the option and set WaveUp as an Accessibility Service.”——用于告知状态回退，不强制跳转。

覆盖边界：无障碍引导代码为编译保留分支，在本分发变体中因 `use_accessibility_service_to_lock=false` 实际不可达；此外未做动态运行验证（本任务按静态定向核验收口）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导相关代码、Manifest 声明、accessibility_service_config.xml 与全部提示文案均在本地明文 DEX/资源中完整可见，无加壳、无 AES 密文载荷、无远端 HTML。唯一运行期差异是该构建 use_accessibility_service_to_lock=false，使无障碍服务未在系统列表中启用，属产品变体开关而非隐藏逻辑。",
  "summary_one_liner": "WaveUp 仅在用户主动开启“锁屏”功能时，以透明开源说明弹窗提示用户前往系统无障碍页手动授权，并因 Google Play 政策在本构建中实际关闭了该无障碍服务，拒绝后安全降级为设备管理员或关闭选项。",
  "disguise_identity": {
    "app_display_name": "WaveUp",
    "claimed_brand_or_persona": "WaveUp（开源挥手亮屏/锁屏工具，com.jarsilio.android.waveup）",
    "a11y_service_label": "WaveUp（android:label=\"@string/app_name\"，与桌面名一致）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务标签与桌面名一致，无空白/换行挤出警告、无同形字、无多 activity-alias 伪装；R8 混淆仅作用于普通代码（r8-map-id），非身份伪装；无伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.jarsilio.android.waveup.MainActivity（承载 MainActivity$SettingsFragment 设置页）",
      "trigger_event": "onCreate；仅当 Intent action 为 com.jarsilio.android.waveup.action.REQUEST_LOCK_PERMISSIONS（由 ShortcutActivity 快捷方式下发）时才进入授权引导分支，普通点击图标冷启动不弹无障碍引导",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Starting WaveUp MainActivity (GUI)",
      "shown_text_zh": "日志：启动 WaveUp 主界面；普通冷启动仅加载设置页与“喜欢就支持一下”/无近距传感器提示，不涉及无障碍",
      "user_action_requested": "无强制操作；可正常浏览设置项",
      "code_anchor": "com.jarsilio.android.waveup.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "设置页锁屏开关 pref_lock_screen（MainActivity$SettingsFragment）",
      "trigger_event": "onSharedPreferenceChanged 检测到 pref_lock_screen 变为 true 且 isLockScreen() 为真",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Showing dialog to see if the user wants to open Android's 'Accessibility Settings'",
      "shown_text_zh": "日志：弹出对话框询问用户是否愿意打开安卓“无障碍设置”；仅在用户主动开启锁屏功能时才引导",
      "user_action_requested": "用户主动打开锁屏开关（按需触发，非强制）",
      "code_anchor": "com.jarsilio.android.waveup.MainActivity$SettingsFragment.onSharedPreferenceChanged"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "MaterialAlertDialogBuilder 原生弹窗（标题缺省，正文为 accessibility_service_explanation）",
      "trigger_event": "PermissionsHandler.openLockDevicePermissionExplanationIfNecessary 在 isPieOrNewer 且 isAccessibilityServiceEnabled() 为 false 时构建并 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Lock device: Accessibility Service / In order to lock the screen, we need to set WaveUp as an 'Accessibility Service'. Granting an app Accessibility Service allows it to spy on the user if it wants to. It also allows an app to use specific functions that wouldn't be available if not. For example WaveUp uses the AccessibilityService.\"GLOBAL_ACTION_LOCK_SCREEN\" to lock the screen. Please think twice before trusting apps! WaveUp is open source software so please go ahead and check the code (or ask a friend to do it) to make sure we are not doing anything evil (we promise we are not, but you really shouldn't take our word for it). Do you want to set WaveUp as an Accessibility Service? You'll have to grant the privileges manually in the next screen.",
      "shown_text_zh": "锁屏功能：无障碍服务。为了锁屏，需要把 WaveUp 设为“无障碍服务”。授予无障碍会让应用有能力窥探用户；同时也能使用原本不可用的特定功能，例如 WaveUp 使用 GLOBAL_ACTION_LOCK_SCREEN 锁屏。信任应用前请三思！WaveUp 是开源软件，欢迎自行（或请朋友）检查代码确认我们没有做坏事（我们保证没有，但你真的不该只听我们说）。是否将 WaveUp 设为无障碍服务？你需要在下一个界面手动授予权限。",
      "user_action_requested": "确定（android.R.string.ok）/ 取消（android.R.string.cancel）；弹窗 mCancelable=false（点外部不消失）但提供可用的取消按钮",
      "code_anchor": "com.jarsilio.android.waveup.PermissionsHandler.openLockDevicePermissionExplanationIfNecessary；res/values/strings.xml#L30-L40"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户点击弹窗“确定”后 PermissionsHandler$$ExternalSyntheticLambda0.onClick（case 1）执行 startActivityForResult(Intent, 500)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Opening Android's 'Accessibility Settings' activity",
      "shown_text_zh": "日志：打开安卓无障碍设置界面；由用户点击触发，无悬浮遮罩、无高仿设置页覆盖",
      "user_action_requested": "用户自行在系统无障碍列表中找到 WaveUp 并手动开启（该构建中该服务因 bool=false 未声明启用，实际列表可能不出现该项）",
      "code_anchor": "com.jarsilio.android.waveup.PermissionsHandler$$ExternalSyntheticLambda0.onClick"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 MainActivity（onActivityResult requestCode=500）",
      "trigger_event": "从系统设置返回后回调 onActivityResult(500, ...)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "The user didn't enable the AccessibilityService. Won't be able to lock device.",
      "shown_text_zh": "日志：用户未启用无障碍服务，将无法锁屏；随后调用 setLockScreen() 关闭锁屏选项，不重跳设置页、不再弹引导",
      "user_action_requested": "无需操作；应用自动安全降级（关闭锁屏功能）",
      "code_anchor": "com.jarsilio.android.waveup.MainActivity.onActivityResult"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "ProximitySensorHandler.startOrStopListeningDependingOnConditions / LockAccessibilityService",
      "trigger_event": "onActivityResult(500) 检测到 isAccessibilityServiceEnabled() 为 true 后启动近距传感器监听；实际锁屏通过无障碍服务 GLOBAL_ACTION_LOCK_SCREEN 执行",
      "ui_carrier": "Service",
      "shown_text_verbatim": "WaveUp Lock Command",
      "shown_text_zh": "无障碍服务描述文案“WaveUp 锁屏命令”；获权后仅恢复近距传感器监听与锁屏动作，无自动点击确认、无监听设置页阻止撤权",
      "user_action_requested": "无",
      "code_anchor": "com.jarsilio.android.waveup.MainActivity.onActivityResult；com.jarsilio.android.waveup.service.LockAccessibilityService.onAccessibilityEvent"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "设置页 onResume 的 MaterialAlertDialogBuilder（标题 something_went_wrong）",
      "trigger_event": "SettingsFragment.onResume 发现 pref_lock_screen 为 true 但无障碍（Pie+）或设备管理员（Pie 前）权限缺失",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "WaveUp had to disable the 'lock' option due to a missing Accessibility Service permission. Please re-enable the option and set WaveUp as an Accessibility Service.",
      "shown_text_zh": "由于缺少无障碍服务权限，WaveUp 不得不关闭“锁屏”选项。请重新开启该选项并把 WaveUp 设为无障碍服务。",
      "user_action_requested": "仅“确定”按钮（mCancelable=false）；仅告知状态回退，不自动跳转、不循环重弹",
      "code_anchor": "com.jarsilio.android.waveup.MainActivity$SettingsFragment.onResume；res/values/strings.xml#L157"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内的 MaterialAlertDialogBuilder 原生弹窗：正文为 res/values/strings.xml 的 accessibility_service_explanation（开启锁屏功能时出现，含 OK/Cancel，点外部不消失）",
    "SettingsFragment.onResume 的“Something went wrong”原生弹窗：正文为 lock_disabled_warning_accessibility_settings_text（权限被收回后告知选项已被关闭）",
    "系统无障碍列表条目：服务 android:label=\"@string/app_name\"（WaveUp），说明由 res/xml/accessibility_service_config.xml 提供（未配置 android:description，description 为空）",
    "res/values/strings.xml 中 accessibility_service_text=\"WaveUp Lock Command\"（无障碍相关短描述文案）",
    "应用内帮助/FAQ 的 HTML 文本（com.jarsilio.android.common.html.HtmlTextActivity + 资源内嵌 HTML 字符串，如 ACRA/数据收集说明），非无障碍授权诱导载体",
    "无 assets 下的引导 HTML/WebView、无悬浮窗遮罩、无伪造无障碍开关页、无图片引导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Lock device: Accessibility Service — In order to lock the screen, we need to set WaveUp as an 'Accessibility Service'. Granting an app Accessibility Service allows it to spy on the user if it wants to. It also allows an app to use specific functions that wouldn't be available if not. For example WaveUp uses the AccessibilityService.\"GLOBAL_ACTION_LOCK_SCREEN\" to lock the screen. Please think twice before trusting apps! WaveUp is open source software so please go ahead and check the code (or ask a friend to do it) to make sure we are not doing anything evil (we promise we are not, but you really shouldn't take our word for it). Do you want to set WaveUp as an Accessibility Service? You'll have to grant the privileges manually in the next screen.",
      "text_zh": "锁屏功能：无障碍服务——为了锁屏，需要把 WaveUp 设为“无障碍服务”。授予无障碍会让应用有能力窥探用户；也能使用原本不可用的特定功能，例如 WaveUp 使用 GLOBAL_ACTION_LOCK_SCREEN 锁屏。信任应用前请三思！WaveUp 是开源软件，欢迎自行（或请朋友）检查代码确认我们没有做坏事（我们保证没有，但你真的不该只听我们说）。是否将 WaveUp 设为无障碍服务？你需要在下一个界面手动授予权限。",
      "source_location": "res/values/strings.xml key=accessibility_service_explanation（#L30-L40）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "WaveUp had to disable the 'lock' option due to a missing Accessibility Service permission. Please re-enable the option and set WaveUp as an Accessibility Service.",
      "text_zh": "由于缺少无障碍服务权限，WaveUp 不得不关闭“锁屏”选项。请重新开启该选项并把 WaveUp 设为无障碍服务。",
      "source_location": "res/values/strings.xml key=lock_disabled_warning_accessibility_settings_text（#L157），由 MainActivity$SettingsFragment.onResume 展示",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Unfortunately the ✌️, 🦋, ❤, and 🔒 version of the app currently violate the Google Play policy because of an issue with Violation of...",
      "text_zh": "遗憾的是，✌️、🦋、❤、🔒 等版本的应用目前因违反 Google Play 政策而被下架/不合规……",
      "source_location": "res/values/strings.xml（预筛命中 DEFAULT 文案，说明锁屏相关变体因 Play 政策移除）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "In order to lock the screen, we need to set WaveUp as a 'Device Administrator'. Once an app is a Device Administrator...",
      "text_zh": "为了锁屏，需要把 WaveUp 设为“设备管理员”。一旦应用成为设备管理员……",
      "source_location": "res/values/strings.xml key=lock_admin_rights_explanation（Pie 之前版本的替代说明）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "WaveUp Lock Command",
      "text_zh": "WaveUp 锁屏命令",
      "source_location": "res/values/strings.xml key=accessibility_service_text",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。用户取消弹窗则完全不跳转；从系统设置返回后 onActivityResult(500) 检测未启用即记录日志并 setLockScreen() 关闭锁屏选项，不重跳设置页；SettingsFragment.onResume 仅弹一次“Something went wrong”告知选项已被关闭（mCancelable=false，仅 OK），需用户手动再次开启开关才会重新出现引导。",
    "overlay_or_fake_settings": "无。无 SYSTEM_ALERT_WINDOW 悬浮遮罩、无半透明引导层、无高仿系统无障碍开关页，跳转即真实 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无。代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无“点右上角菜单允许受限设置”或 Session 安装器绕过教学。",
    "post_grant_anti_removal": "无。获权后仅启动近距传感器监听与 GLOBAL_ACTION_LOCK_SCREEN 锁屏；无自动点击确认、无监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权（LockAccessibilityService 仅监听 typeNotificationStateChanged 且 packageNames 限定自身、canRetrieveWindowContent=false）。",
    "benign_graceful_degradation": "有。无障碍不可用/被拒绝时自动 setLockScreen() 关闭该选项，锁屏可改用设备管理员（LockScreenAdminReceiver，ACTION_ADD_DEVICE_ADMIN，requestCode 100）或直接关闭功能；本构建 bool use_accessibility_service_to_lock=false，即以非无障碍变体发布。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS（requestCode=500）的瞬间拉起 UTG 抓取跳转前弹窗与随后系统页；或监测 MainActivity 收到 action=com.jarsilio.android.waveup.action.REQUEST_LOCK_PERMISSIONS 的冷启动。普通点击图标冷启动不会弹无障碍引导，无需在冷启动 0 步抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前引导弹窗页",
        "page_identifier": "MaterialAlertDialog，正文含 \"Lock device: Accessibility Service\" / \"GLOBAL_ACTION_LOCK_SCREEN\" / \"Please think twice before trusting apps!\"，按钮 OK 与 Cancel",
        "why_most_useful": "该弹窗是全部无障碍引导文案的唯一载体，可直接判断话术是透明说明还是恐吓/伪装",
        "observable_utg_signals": ["文本包含 \"Accessibility Service\" 与 \"spy on the user\" 等风险自陈", "同时存在 OK 与 Cancel 两个可点击按钮", "无标题或标题为空、点外部不消失（mCancelable=false）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置页 com.android.settings/.Settings$AccessibilitySettingsActivity，列表项标签 WaveUp（如出现）",
        "why_most_useful": "核验服务是否真实注册、显示名是否与桌面名一致、描述是否为空",
        "observable_utg_signals": ["列表项文本为 WaveUp（无空白/换行挤出）", "副标题/描述为空", "该构建 bool=false 时列表可能无此条目"]
      },
      {
        "page_role": "拒权返回后的设置页与回退提示",
        "page_identifier": "WaveUp 设置页 + 标题 Something went wrong 的弹窗，正文含 \"had to disable the 'lock' option\"",
        "why_most_useful": "验证拒绝后是安全降级还是循环重跳，是区分良性/胁迫的关键",
        "observable_utg_signals": ["返回后停留在 WaveUp 设置页而非再次跳系统设置", "锁屏开关呈关闭态", "仅一个 OK 按钮"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一需注意：本构建 use_accessibility_service_to_lock=false，无障碍服务未在系统列表启用，纯 UTG 运行期可能完全看不到无障碍授权流程（引导代码为编译保留分支），此时应以 Manifest/bools/strings 静态证据判定，不应因“未见引导”而误判为隐藏行为；另无加壳/密文/远端 HTML 遮挡。"
  },
  "behavior_pattern_tags": ["TRIG_FEATURE_ON_DEMAND", "CARRIER_NATIVE_DIALOG_OR_ACTIVITY", "CARRIER_SYSTEM_A11Y_DESCRIPTION", "BENIGN_TRANSPARENT_RATIONALE", "BENIGN_EXPLICIT_CANCEL_DEGRADATION", "BENIGN_HONEST_IDENTITY_AND_SCOPE", "BENIGN_ALTERNATIVE_MODE_OFFERED"],
  "code_anchors": [
    "com.jarsilio.android.waveup.PermissionsHandler.openLockDevicePermissionExplanationIfNecessary",
    "com.jarsilio.android.waveup.PermissionsHandler$$ExternalSyntheticLambda0.onClick",
    "com.jarsilio.android.waveup.MainActivity.onActivityResult",
    "com.jarsilio.android.waveup.MainActivity$SettingsFragment.onSharedPreferenceChanged",
    "com.jarsilio.android.waveup.MainActivity$SettingsFragment.onResume",
    "res/xml/accessibility_service_config.xml / res/values/bools.xml / res/values/strings.xml#L30-L40"
  ]
}
```

</details>
