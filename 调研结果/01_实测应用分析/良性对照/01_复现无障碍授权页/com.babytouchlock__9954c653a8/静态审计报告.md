# BN_041__9954c653a8｜残障辅助与无障碍支持 — Baby Touch Lock

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：129.7s

## 1. 一句话核心结论

- **核心申请方式**：主界面状态卡 + 'Enable Service' 按钮触发带 Cancel 的原生说明弹窗（含隐私承诺），用户点 Accept & Continue 后跳系统无障碍设置页；返回仅刷新状态，不循环重跳、不伪造设置页、不阻止撤权，属透明的良性授权引导。
- **静态可见性说明**：全部引导逻辑位于单个 classes.dex（Kotlin，无加固、无 VMP、无加密二阶段载荷）；引导文案均在 res/values/strings.xml，界面为原生 MaterialAlertDialog + Activity；assets/ 目录无 HTML/JS 引导页，无远端下发页面，运行期引导流程可完整静态还原。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9954c653a8e05cb96ba3ac15817eb7a76b9c0519a4fa51454dc9247d4c0d5577` |
| 包名 / 年份 | `com.babytouchlock` / 2025-2026 |
| 家族 / 品类 | **残障辅助与无障碍支持**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.babytouchlock_4.apk |
| 桌面显示名 | Baby Touch Lock |
| 引导页宣称品牌/身份 | Baby Touch Lock（F-Droid 开源儿童防误触工具，与包名 com.babytouchlock 一致） |
| 系统无障碍列表服务名 | Baby Touch Lock Service |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务标签、磁贴名（Baby Lock）、android:description 与实际实现（拦截触摸/手势/通知栏/音量键）一致；无同形字、空白或换行挤出、无 activity-alias 伪装、未伪造 isAccessibilityTool 标志。 |
| 无障碍服务类名 | `com.babytouchlock.BabyTouchLockAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | Prevents accidental touches, navigation gestures, notification shade expansion, and volume key presses to protect media playback. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.babytouchlock.MainActivity（AppCompatActivity，ActivityMainBinding 布局） | LAUNCHER 冷启动 onCreate → setupButtons()/checkPermissionsUI()；onResume 再次 checkPermissionsUI() | 原生Activity | **原文**：Baby Touch Lock / Screen and buttons lock for kids<br>**译注**：应用主标题“Baby Touch Lock”与副标题“为孩子锁定屏幕和按键” | 仅展示主界面，不强制弹窗；用户可自由离开 | `com.babytouchlock.MainActivity.onCreate / onResume / checkPermissionsUI（R$string.main_title、main_subtitle）` |
| 2 | 引导说明页 | MainActivity 状态卡 cardStatus（tvStatusTitle/tvStatusDesc）+ 按钮 btnGrantAccessibility | checkPermissionsUI() 中 BabyTouchLockAccessibilityService.Companion.getInstance() == null 时置为告警态并显示授权按钮 | 原生Activity | **原文**：Activation Required / Enable the Accessibility Service to intercept touches and buttons. / Enable Service<br>**译注**：“需要激活 / 请启用无障碍服务以拦截触摸和按键 / 启用服务”（已授权时变为 Protection Ready / Accessibility service is active and running.） | 用户点击“Enable Service”按钮（非强制，可忽略并退出） | `MainActivity.checkPermissionsUI（R$string.status_inactive_title、status_inactive_desc、grant_permission；R$id.btn_grant_accessibility）` |
| 3 | 跳无障碍设置 | MaterialAlertDialog：Accessibility Service Disclosure（由 showAccessibilityConsentDialog() 构建） | 点击 btnGrantAccessibility → setupButtons$lambda$9 → showAccessibilityConsentDialog() | 原生Dialog | **原文**：Accessibility Service Disclosure / Baby Touch Lock uses Android's AccessibilityService API solely to block accidental screen taps, navigation gestures, and hardware buttons during media viewing.<br><br>🔒 100% Local & Private: No screen content, keystrokes, or personal data is ever accessed, stored, or transmitted over the internet. / Accept & Continue / Cancel<br>**译注**：“无障碍服务说明：Baby Touch Lock 仅使用 Android AccessibilityService API 在观看媒体时阻断误触、导航手势和硬件按键；🔒 100% 本地与私密：绝不访问、存储或经网络传输屏幕内容、按键记录或个人信息。”按钮为“接受并继续 / 取消” | 用户选择“Accept & Continue”（同意）或“Cancel”（取消，不跳转） | `MainActivity.showAccessibilityConsentDialog（R$string.disclosure_dialog_title、disclosure_dialog_text、dialog_consent_agree、dialog_consent_cancel）` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（Android 无障碍服务列表） | 同意按钮回调 showAccessibilityConsentDialog$lambda$14：dialogInterface.dismiss() 后 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Baby Touch Lock Service — Prevents accidental touches, navigation gestures, notification shade expansion, and volume key presses to protect media playback.<br>**译注**：系统无障碍列表中显示服务名“Baby Touch Lock Service”，说明为“防止误触、导航手势、通知栏下拉和音量键按下，以保护媒体播放” | 用户在系统页面手动找到该服务并开启开关（本应用不代点、不自动开启） | `MainActivity.showAccessibilityConsentDialog$lambda$14；res/xml/accessibility_service_config.xml（@string/accessibility_service_label、accessibility_service_description）` |
| 5 | 拒权反馈循环 | MainActivity 返回栈（onResume → checkPermissionsUI） | 从系统设置页返回应用（无论是否开启）触发 onResume | 原生Activity | **原文**：Activation Required / Enable the Accessibility Service to intercept touches and buttons.<br>**译注**：未开启则状态卡回到“需要激活”并重新显示“启用服务”按钮；已开启则切换为“Protection Ready”。不弹窗、不重跳 | 无强制操作；用户可再次点击按钮重试，或直接退出应用 | `MainActivity.onResume → checkPermissionsUI` |
| 6 | 业务功能触发 | MainActivity “Lock Now”（btnTestLock）按钮 | setupButtons$lambda$13：服务实例为空时 Toast + 再次打开同一说明弹窗；已授权时直接 lock() 并 moveTaskToBack(true) | 原生Dialog | **原文**：Please enable the Baby Touch Lock Accessibility Service first.<br>**译注**：“请先启用 Baby Touch Lock 无障碍服务。”随后弹出同一份 Accessibility Service Disclosure 说明弹窗 | 按需选择“Accept & Continue”跳设置，或“Cancel”取消；无强制循环 | `MainActivity.setupButtons$lambda$13（R$string.accessibility_needed_toast、btn_test_lock）` |
| 7 | 获权后动作 | com.babytouchlock.BabyTouchLockAccessibilityService.showLockWindows()：TYPE_ACCESSIBILITY_OVERLAY(2032) 全屏遮罩 + 右下角 BabyTouchLockUnlockView 解锁手柄；onKeyEvent 拦截 BACK/HOME/音量/电源键 | onServiceConnected() 注册 SCREEN_OFF 广播并更新磁贴；用户经磁贴/按钮调用 lock() → showLockWindows() | 悬浮窗Overlay | **原文**：🔒 / Tap the lock icon in the bottom right corner and slide it upwards.<br>**译注**：锁定态显示锁形图标，提示“点击右下角锁形图标并向上滑动即可解锁”（解锁后可校验 PIN 码） | 上滑解锁手柄（可选 PIN 码校验）；onUnbind/onDestroy 时自动 unlock 并移除悬浮窗 | `BabyTouchLockAccessibilityService.showLockWindows / onKeyEvent / collapseSystemUI / onUnbind（R$string.lock_icon_locked、guide_deactivate_desc）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 主界面状态卡 cardStatus：标题/描述随授权状态切换（status_active_title、status_inactive_title、status_active_desc、status_inactive_desc）
- MainActivity 主界面按钮 btnGrantAccessibility（grant_permission = 'Enable Service'），未授权时可见可点
- MainActivity 不可忽略但可取消的 MaterialAlertDialog：showAccessibilityConsentDialog()，标题 disclosure_dialog_title，正文 disclosure_dialog_text（含隐私承诺段落），正向 'Accept & Continue'、负向 'Cancel'
- MainActivity 隐私说明对话框：点击 tvPrivacyInfo（privacy_info_link = 'Privacy Policy and Accessibility Disclosure'）触发 showPrivacyDisclosureDialog()
- MainActivity 'Lock Now' 未授权时的 Toast：accessibility_needed_toast
- 系统无障碍服务列表项：android:label=@string/accessibility_service_label（'Baby Touch Lock Service'）+ android:description=@string/accessibility_service_description
- 快速设置磁贴与手动添加指引：tile_label='Baby Lock'，非 Android 13+ 时 showManualAddGuideDialog() 展示 manual_add_dialog_title/manual_add_dialog_message（纯使用教学，不涉及权限申请）
- 锁定态悬浮窗内的解锁提示文案：lock_icon_locked、guide_deactivate_title/desc
- 无 assets/ 下的本地 HTML/WebView 引导页，无远端 WebView，无伪造系统设置界面

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please enable the Baby Touch Lock Accessibility Service first. | 请先启用 Baby Touch Lock 无障碍服务。 | `res/values/strings.xml → accessibility_needed_toast（Toast.makeText，MainActivity.setupButtons$lambda$13）` | 良性透明说明 |
| en | Accessibility Service Disclosure | 无障碍服务说明 | `res/values/strings.xml → disclosure_dialog_title（MainActivity.showAccessibilityConsentDialog）` | 良性透明说明 |
| en | Baby Touch Lock uses Android's AccessibilityService API solely to block accidental screen taps, navigation gestures, and hardware buttons during media viewing.<br><br>🔒 100% Local & Private: No screen content, keystrokes, or personal data is ever accessed, stored, or transmitted over the internet. | Baby Touch Lock 仅使用 Android 的 AccessibilityService API，在观看媒体期间阻断误触、导航手势和硬件按键。🔒 100% 本地与私密：绝不访问、存储或通过互联网传输屏幕内容、按键记录或个人数据。 | `res/values/strings.xml → disclosure_dialog_text（MainActivity.showAccessibilityConsentDialog / showPrivacyDisclosureDialog）` | 隐私承诺 |
| en | Accept & Continue | 接受并继续 | `res/values/strings.xml → dialog_consent_agree（MaterialAlertDialog 正向按钮）` | 良性透明说明 |
| en | Cancel | 取消 | `res/values/strings.xml → dialog_consent_cancel（MaterialAlertDialog 负向按钮，点击仅 dismiss，不跳转）` | 良性透明说明 |
| en | Activation Required | 需要激活 | `res/values/strings.xml → status_inactive_title（MainActivity.checkPermissionsUI 状态卡）` | 良性透明说明 |
| en | Enable the Accessibility Service to intercept touches and buttons. | 启用无障碍服务以拦截触摸和按键。 | `res/values/strings.xml → status_inactive_desc（MainActivity.checkPermissionsUI 状态卡）` | 良性透明说明 |
| en | Enable Service | 启用服务 | `res/values/strings.xml → grant_permission（btnGrantAccessibility 按钮文本）` | 良性透明说明 |
| en | Prevents accidental touches, navigation gestures, notification shade expansion, and volume key presses to protect media playback. | 防止误触、导航手势、通知栏下拉和音量键按下，以保护媒体播放。 | `res/values/strings.xml → accessibility_service_description（res/xml/accessibility_service_config.xml android:description）` | 良性透明说明 |
| en | Baby Touch Lock Service | Baby Touch Lock 服务 | `res/values/strings.xml → accessibility_service_label（Manifest service android:label）` | 良性透明说明 |
| en | Protection Ready | 防护就绪 | `res/values/strings.xml → status_active_title（MainActivity.checkPermissionsUI 已授权态）` | 良性透明说明 |
| en | Tap the lock icon in the bottom right corner and slide it upwards. | 点击右下角的锁形图标并向上滑动。 | `res/values/strings.xml → guide_deactivate_desc（悬浮窗解锁手柄提示）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无拒绝循环。取消弹窗仅 dismiss 不跳转；从系统设置返回后 onResume 只调用 checkPermissionsUI() 重绘状态卡（未授权则保持 'Activation Required' + 'Enable Service' 按钮），不自动重弹对话框、无定时器拉起、无 startActivity 重跳。
- **遮罩叠层 / 高仿系统设置页**：无引导型遮罩或伪造设置页。唯一的悬浮窗是获权后业务锁定时使用 TYPE_ACCESSIBILITY_OVERLAY(2032) 的全屏触摸拦截层 + 右下角解锁手柄（BabyTouchLockUnlockView），与权限申请引导无关。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包未出现 android.settings.APPLICATION_DETAILS_SETTINGS 调用点（仅 androidx.core.content.IntentCompat 内部工具方法引用该字符串，未被本应用引导路径使用），无“允许受限设置”分步教学、无 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅注册 SCREEN_OFF 广播并更新磁贴；performGlobalAction(15) 仅用于锁定态收起通知栏（collapseSystemUI），未在设置页使用 BACK/HOME 阻止撤权；onUnbind/onDestroy 主动 unlock() 并移除悬浮窗，instance 置空。
- **良性降级 / 替代方案**：是。服务未启用时主界面仍可正常打开，仅显示 'Activation Required' 状态卡；用户可完全忽略授权（点 Cancel 或直接退出）。另有独立于无障碍服务的 Quick Settings 磁贴（BabyTouchLockTileService）与手动添加指引（manual_add_dialog_message），并提供 PIN 码设置/校验（showSetPinDialog/showVerifyPinDialog）作为解锁替代路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳抓取时机为：监测到 Intent 'android.settings.ACCESSIBILITY_SETTINGS' 启动的瞬间（唯一跳转点，showAccessibilityConsentDialog$lambda$14）——此时应已采集到其前置的 'Accessibility Service Disclosure' 原生弹窗页；以及冷启动进入 MainActivity 时采集未授权状态卡（'Activation Required' / 'Enable Service'）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。无静态加壳、无加密载荷、无远端 HTML 或云控开关；全部引导文案为原生 strings.xml 纯文本，UTG 可直接提取。唯一需注意：获权后锁定态的 TYPE_ACCESSIBILITY_OVERLAY 全屏层会遮挡下方应用内容，UTG 抓取时应区分该业务遮罩与权限引导界面。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/主界面未授权状态卡页** | com.babytouchlock.MainActivity，cardStatus 卡片文案 'Activation Required'，可见按钮文本 'Enable Service'（resource-id btn_grant_accessibility） | 判定引导是否冷启动即出现、是否存在不可取消强制弹窗，以及授权按钮是否为主界面唯一强提示 | 状态卡标题/描述原文（Activation Required / Enable the Accessibility Service to intercept touches and buttons.）；btn_grant_accessibility 的可见性与文本；是否叠加任何非系统悬浮窗（应无） |
| **跳转前原生说明弹窗页** | MaterialAlertDialog，标题 'Accessibility Service Disclosure'，正文含 'Baby Touch Lock uses Android's AccessibilityService API solely to...' 与 '🔒 100% Local & Private' | 这是权限申请的唯一告知载体，直接决定是否属于透明告知还是话术包装；同时可核对是否存在 Cancel 按钮 | 弹窗标题与完整正文文本；正向按钮 'Accept & Continue' 与负向按钮 'Cancel' 是否同时存在；弹窗是否可被返回键/点击外部取消；文案与实际行为（canRetrieveWindowContent=false、空 onAccessibilityEvent）是否一致 |
| **系统无障碍服务列表项** | 系统 Settings 无障碍列表，条目名 'Baby Touch Lock Service'，摘要 'Prevents accidental touches, navigation gestures...' | 核对系统侧展示名/描述与应用内宣称是否一致，是否存在身份混淆或描述与实际能力不符 | 服务名与摘要原文；是否由应用代点开启（应无，用户手动操作）；列表项是否被应用叠加遮罩覆盖或高亮引导 |
| **返回应用后的拒权反馈页** | 从系统设置返回后的 com.babytouchlock.MainActivity | 判定是否存在 onResume 死循环重跳设置或定时器反复拉起；本应用应表现为静默刷新状态卡 | 返回后是否立即再次出现系统无障碍页或说明弹窗；状态卡文案是否仅做 active/inactive 切换；是否出现重复 startActivity 的堆栈抖动 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.babytouchlock.MainActivity.showAccessibilityConsentDialog`
- `com.babytouchlock.MainActivity.showAccessibilityConsentDialog$lambda$14`
- `com.babytouchlock.MainActivity.checkPermissionsUI`
- `com.babytouchlock.MainActivity.setupButtons$lambda$13`
- `com.babytouchlock.BabyTouchLockAccessibilityService.showLockWindows`
- `res/xml/accessibility_service_config.xml + res/values/strings.xml（disclosure_dialog_text / accessibility_service_description / grant_permission）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（良性无障碍应用，纯运行期 UTG 视角）

**核心事实（已静态确认）**

- **仅一个入口，无自动拉起**：只有 `com.babytouchlock.MainActivity` 会拉起引导流程。它没有在 `onCreate` 或 `onResume` 中主动弹出对话框；`onResume` 仅调用 `checkPermissionsUI()` 刷新状态卡的颜色、文案以及“Enable Service”按钮的可见性。用户从系统设置返回后，本应用会正常停留在本页，不会反复重跳。
- **引导链路**：状态卡（未授权时显示 `Activation Required` / `Enable the Service`）→ 用户点击 `btnGrantAccessibility` → `showAccessibilityConsentDialog()` 弹出 `MaterialAlertDialog`（标题为 `Accessibility Service Disclosure`，正文含“100% Local & Private”隐私承诺）→ 点击 `Accept & Continue` → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。对话框设有 **Cancel** 负向按钮，用户可随时放弃。
- **次级触发点**：当服务尚未启用时，用户点击“Lock Now”（`setupButtons$lambda$13`）会先弹出 Toast `Please enable the Baby Touch Lock Accessibility Service first.`，随后打开同一个同意对话框。这是功能按需触发，并非冷启动强制。
- **未发现下列诱导特征**：没有跳转 `ACTION_APPLICATION_DETAILS_SETTINGS`，没有“受限设置/允许受限设置”分步教学，没有伪造系统无障碍开关页，没有在设置页压栈半透明引导遮罩，也没有 `performGlobalAction(BACK/HOME)` 阻止撤权；`onUnbind`/`onDestroy` 会主动 `unlock()` 并清除悬浮窗，撤权后会自动降级。
- **悬浮窗仅用于真实业务**：`showLockWindows()` 使用 `TYPE_ACCESSIBILITY_OVERLAY(2032)` 铺满屏幕以拦截触摸，并叠加 `BabyTouchLockUnlockView` 解锁手柄；锁定期间 `onKeyEvent` 拦截 BACK/HOME/音量/电源键，`collapseSystemUI()` 用 `performGlobalAction(15)` 收起通知栏。这些都是“防误触”功能本身，并配套上滑解锁 + PIN 码（`showSetPinDialog`/`showVerifyPinDialog`）作为退出路径。
- **身份一致**：应用名 `Baby Touch Lock`、服务标签 `Baby Touch Lock Service`、磁贴 `Baby Lock`、`android:description` 与实际行为（阻断触摸、手势和按键）一致，无同形字、空白挤出或 `activity-alias` 混淆；`canRetrieveWindowContent="false"`、`accessibilityEventTypes=""`、`onAccessibilityEvent` 空实现，不具备读屏或窃取能力。
- **配置面**：`assets/` 无 HTML 引导页，全部文案为原生 `strings.xml` + Material Dialog，静态完全可见。

**判定**：属透明的良性无障碍授权引导（`BENIGN_TRANSPARENT_RATIONALE` + `BENIGN_EXPLICIT_CANCEL_DEGRADATION`），不构成诱导攻击，未登记风险。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于单个 classes.dex（Kotlin，无加固、无 VMP、无加密二阶段载荷）；引导文案均在 res/values/strings.xml，界面为原生 MaterialAlertDialog + Activity；assets/ 目录无 HTML/JS 引导页，无远端下发页面，运行期引导流程可完整静态还原。",
  "summary_one_liner": "主界面状态卡 + 'Enable Service' 按钮触发带 Cancel 的原生说明弹窗（含隐私承诺），用户点 Accept & Continue 后跳系统无障碍设置页；返回仅刷新状态，不循环重跳、不伪造设置页、不阻止撤权，属透明的良性授权引导。",
  "disguise_identity": {
    "app_display_name": "Baby Touch Lock",
    "claimed_brand_or_persona": "Baby Touch Lock（F-Droid 开源儿童防误触工具，与包名 com.babytouchlock 一致）",
    "a11y_service_label": "Baby Touch Lock Service",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务标签、磁贴名（Baby Lock）、android:description 与实际实现（拦截触摸/手势/通知栏/音量键）一致；无同形字、空白或换行挤出、无 activity-alias 伪装、未伪造 isAccessibilityTool 标志。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.babytouchlock.MainActivity（AppCompatActivity，ActivityMainBinding 布局）",
      "trigger_event": "LAUNCHER 冷启动 onCreate → setupButtons()/checkPermissionsUI()；onResume 再次 checkPermissionsUI()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Baby Touch Lock / Screen and buttons lock for kids",
      "shown_text_zh": "应用主标题“Baby Touch Lock”与副标题“为孩子锁定屏幕和按键”",
      "user_action_requested": "仅展示主界面，不强制弹窗；用户可自由离开",
      "code_anchor": "com.babytouchlock.MainActivity.onCreate / onResume / checkPermissionsUI（R$string.main_title、main_subtitle）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 状态卡 cardStatus（tvStatusTitle/tvStatusDesc）+ 按钮 btnGrantAccessibility",
      "trigger_event": "checkPermissionsUI() 中 BabyTouchLockAccessibilityService.Companion.getInstance() == null 时置为告警态并显示授权按钮",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Activation Required / Enable the Accessibility Service to intercept touches and buttons. / Enable Service",
      "shown_text_zh": "“需要激活 / 请启用无障碍服务以拦截触摸和按键 / 启用服务”（已授权时变为 Protection Ready / Accessibility service is active and running.）",
      "user_action_requested": "用户点击“Enable Service”按钮（非强制，可忽略并退出）",
      "code_anchor": "MainActivity.checkPermissionsUI（R$string.status_inactive_title、status_inactive_desc、grant_permission；R$id.btn_grant_accessibility）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "MaterialAlertDialog：Accessibility Service Disclosure（由 showAccessibilityConsentDialog() 构建）",
      "trigger_event": "点击 btnGrantAccessibility → setupButtons$lambda$9 → showAccessibilityConsentDialog()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Accessibility Service Disclosure / Baby Touch Lock uses Android's AccessibilityService API solely to block accidental screen taps, navigation gestures, and hardware buttons during media viewing.\n\n🔒 100% Local & Private: No screen content, keystrokes, or personal data is ever accessed, stored, or transmitted over the internet. / Accept & Continue / Cancel",
      "shown_text_zh": "“无障碍服务说明：Baby Touch Lock 仅使用 Android AccessibilityService API 在观看媒体时阻断误触、导航手势和硬件按键；🔒 100% 本地与私密：绝不访问、存储或经网络传输屏幕内容、按键记录或个人信息。”按钮为“接受并继续 / 取消”",
      "user_action_requested": "用户选择“Accept & Continue”（同意）或“Cancel”（取消，不跳转）",
      "code_anchor": "MainActivity.showAccessibilityConsentDialog（R$string.disclosure_dialog_title、disclosure_dialog_text、dialog_consent_agree、dialog_consent_cancel）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（Android 无障碍服务列表）",
      "trigger_event": "同意按钮回调 showAccessibilityConsentDialog$lambda$14：dialogInterface.dismiss() 后 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Baby Touch Lock Service — Prevents accidental touches, navigation gestures, notification shade expansion, and volume key presses to protect media playback.",
      "shown_text_zh": "系统无障碍列表中显示服务名“Baby Touch Lock Service”，说明为“防止误触、导航手势、通知栏下拉和音量键按下，以保护媒体播放”",
      "user_action_requested": "用户在系统页面手动找到该服务并开启开关（本应用不代点、不自动开启）",
      "code_anchor": "MainActivity.showAccessibilityConsentDialog$lambda$14；res/xml/accessibility_service_config.xml（@string/accessibility_service_label、accessibility_service_description）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 返回栈（onResume → checkPermissionsUI）",
      "trigger_event": "从系统设置页返回应用（无论是否开启）触发 onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Activation Required / Enable the Accessibility Service to intercept touches and buttons.",
      "shown_text_zh": "未开启则状态卡回到“需要激活”并重新显示“启用服务”按钮；已开启则切换为“Protection Ready”。不弹窗、不重跳",
      "user_action_requested": "无强制操作；用户可再次点击按钮重试，或直接退出应用",
      "code_anchor": "MainActivity.onResume → checkPermissionsUI"
    },
    {
      "step": 6,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity “Lock Now”（btnTestLock）按钮",
      "trigger_event": "setupButtons$lambda$13：服务实例为空时 Toast + 再次打开同一说明弹窗；已授权时直接 lock() 并 moveTaskToBack(true)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please enable the Baby Touch Lock Accessibility Service first.",
      "shown_text_zh": "“请先启用 Baby Touch Lock 无障碍服务。”随后弹出同一份 Accessibility Service Disclosure 说明弹窗",
      "user_action_requested": "按需选择“Accept & Continue”跳设置，或“Cancel”取消；无强制循环",
      "code_anchor": "MainActivity.setupButtons$lambda$13（R$string.accessibility_needed_toast、btn_test_lock）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.babytouchlock.BabyTouchLockAccessibilityService.showLockWindows()：TYPE_ACCESSIBILITY_OVERLAY(2032) 全屏遮罩 + 右下角 BabyTouchLockUnlockView 解锁手柄；onKeyEvent 拦截 BACK/HOME/音量/电源键",
      "trigger_event": "onServiceConnected() 注册 SCREEN_OFF 广播并更新磁贴；用户经磁贴/按钮调用 lock() → showLockWindows()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "🔒 / Tap the lock icon in the bottom right corner and slide it upwards.",
      "shown_text_zh": "锁定态显示锁形图标，提示“点击右下角锁形图标并向上滑动即可解锁”（解锁后可校验 PIN 码）",
      "user_action_requested": "上滑解锁手柄（可选 PIN 码校验）；onUnbind/onDestroy 时自动 unlock 并移除悬浮窗",
      "code_anchor": "BabyTouchLockAccessibilityService.showLockWindows / onKeyEvent / collapseSystemUI / onUnbind（R$string.lock_icon_locked、guide_deactivate_desc）"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 主界面状态卡 cardStatus：标题/描述随授权状态切换（status_active_title、status_inactive_title、status_active_desc、status_inactive_desc）",
    "MainActivity 主界面按钮 btnGrantAccessibility（grant_permission = 'Enable Service'），未授权时可见可点",
    "MainActivity 不可忽略但可取消的 MaterialAlertDialog：showAccessibilityConsentDialog()，标题 disclosure_dialog_title，正文 disclosure_dialog_text（含隐私承诺段落），正向 'Accept & Continue'、负向 'Cancel'",
    "MainActivity 隐私说明对话框：点击 tvPrivacyInfo（privacy_info_link = 'Privacy Policy and Accessibility Disclosure'）触发 showPrivacyDisclosureDialog()",
    "MainActivity 'Lock Now' 未授权时的 Toast：accessibility_needed_toast",
    "系统无障碍服务列表项：android:label=@string/accessibility_service_label（'Baby Touch Lock Service'）+ android:description=@string/accessibility_service_description",
    "快速设置磁贴与手动添加指引：tile_label='Baby Lock'，非 Android 13+ 时 showManualAddGuideDialog() 展示 manual_add_dialog_title/manual_add_dialog_message（纯使用教学，不涉及权限申请）",
    "锁定态悬浮窗内的解锁提示文案：lock_icon_locked、guide_deactivate_title/desc",
    "无 assets/ 下的本地 HTML/WebView 引导页，无远端 WebView，无伪造系统设置界面"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please enable the Baby Touch Lock Accessibility Service first.",
      "text_zh": "请先启用 Baby Touch Lock 无障碍服务。",
      "source_location": "res/values/strings.xml → accessibility_needed_toast（Toast.makeText，MainActivity.setupButtons$lambda$13）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service Disclosure",
      "text_zh": "无障碍服务说明",
      "source_location": "res/values/strings.xml → disclosure_dialog_title（MainActivity.showAccessibilityConsentDialog）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Baby Touch Lock uses Android's AccessibilityService API solely to block accidental screen taps, navigation gestures, and hardware buttons during media viewing.\n\n🔒 100% Local & Private: No screen content, keystrokes, or personal data is ever accessed, stored, or transmitted over the internet.",
      "text_zh": "Baby Touch Lock 仅使用 Android 的 AccessibilityService API，在观看媒体期间阻断误触、导航手势和硬件按键。🔒 100% 本地与私密：绝不访问、存储或通过互联网传输屏幕内容、按键记录或个人数据。",
      "source_location": "res/values/strings.xml → disclosure_dialog_text（MainActivity.showAccessibilityConsentDialog / showPrivacyDisclosureDialog）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Accept & Continue",
      "text_zh": "接受并继续",
      "source_location": "res/values/strings.xml → dialog_consent_agree（MaterialAlertDialog 正向按钮）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Cancel",
      "text_zh": "取消",
      "source_location": "res/values/strings.xml → dialog_consent_cancel（MaterialAlertDialog 负向按钮，点击仅 dismiss，不跳转）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Activation Required",
      "text_zh": "需要激活",
      "source_location": "res/values/strings.xml → status_inactive_title（MainActivity.checkPermissionsUI 状态卡）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable the Accessibility Service to intercept touches and buttons.",
      "text_zh": "启用无障碍服务以拦截触摸和按键。",
      "source_location": "res/values/strings.xml → status_inactive_desc（MainActivity.checkPermissionsUI 状态卡）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Service",
      "text_zh": "启用服务",
      "source_location": "res/values/strings.xml → grant_permission（btnGrantAccessibility 按钮文本）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Prevents accidental touches, navigation gestures, notification shade expansion, and volume key presses to protect media playback.",
      "text_zh": "防止误触、导航手势、通知栏下拉和音量键按下，以保护媒体播放。",
      "source_location": "res/values/strings.xml → accessibility_service_description（res/xml/accessibility_service_config.xml android:description）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Baby Touch Lock Service",
      "text_zh": "Baby Touch Lock 服务",
      "source_location": "res/values/strings.xml → accessibility_service_label（Manifest service android:label）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Protection Ready",
      "text_zh": "防护就绪",
      "source_location": "res/values/strings.xml → status_active_title（MainActivity.checkPermissionsUI 已授权态）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Tap the lock icon in the bottom right corner and slide it upwards.",
      "text_zh": "点击右下角的锁形图标并向上滑动。",
      "source_location": "res/values/strings.xml → guide_deactivate_desc（悬浮窗解锁手柄提示）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无拒绝循环。取消弹窗仅 dismiss 不跳转；从系统设置返回后 onResume 只调用 checkPermissionsUI() 重绘状态卡（未授权则保持 'Activation Required' + 'Enable Service' 按钮），不自动重弹对话框、无定时器拉起、无 startActivity 重跳。",
    "overlay_or_fake_settings": "无引导型遮罩或伪造设置页。唯一的悬浮窗是获权后业务锁定时使用 TYPE_ACCESSIBILITY_OVERLAY(2032) 的全屏触摸拦截层 + 右下角解锁手柄（BabyTouchLockUnlockView），与权限申请引导无关。",
    "restricted_settings_13plus_coaching": "无。全包未出现 android.settings.APPLICATION_DETAILS_SETTINGS 调用点（仅 androidx.core.content.IntentCompat 内部工具方法引用该字符串，未被本应用引导路径使用），无“允许受限设置”分步教学、无 Session 安装器绕过。",
    "post_grant_anti_removal": "无。onServiceConnected 仅注册 SCREEN_OFF 广播并更新磁贴；performGlobalAction(15) 仅用于锁定态收起通知栏（collapseSystemUI），未在设置页使用 BACK/HOME 阻止撤权；onUnbind/onDestroy 主动 unlock() 并移除悬浮窗，instance 置空。",
    "benign_graceful_degradation": "是。服务未启用时主界面仍可正常打开，仅显示 'Activation Required' 状态卡；用户可完全忽略授权（点 Cancel 或直接退出）。另有独立于无障碍服务的 Quick Settings 磁贴（BabyTouchLockTileService）与手动添加指引（manual_add_dialog_message），并提供 PIN 码设置/校验（showSetPinDialog/showVerifyPinDialog）作为解锁替代路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳抓取时机为：监测到 Intent 'android.settings.ACCESSIBILITY_SETTINGS' 启动的瞬间（唯一跳转点，showAccessibilityConsentDialog$lambda$14）——此时应已采集到其前置的 'Accessibility Service Disclosure' 原生弹窗页；以及冷启动进入 MainActivity 时采集未授权状态卡（'Activation Required' / 'Enable Service'）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/主界面未授权状态卡页",
        "page_identifier": "com.babytouchlock.MainActivity，cardStatus 卡片文案 'Activation Required'，可见按钮文本 'Enable Service'（resource-id btn_grant_accessibility）",
        "why_most_useful": "判定引导是否冷启动即出现、是否存在不可取消强制弹窗，以及授权按钮是否为主界面唯一强提示",
        "observable_utg_signals": ["状态卡标题/描述原文（Activation Required / Enable the Accessibility Service to intercept touches and buttons.）", "btn_grant_accessibility 的可见性与文本", "是否叠加任何非系统悬浮窗（应无）"]
      },
      {
        "page_role": "跳转前原生说明弹窗页",
        "page_identifier": "MaterialAlertDialog，标题 'Accessibility Service Disclosure'，正文含 'Baby Touch Lock uses Android's AccessibilityService API solely to...' 与 '🔒 100% Local & Private'",
        "why_most_useful": "这是权限申请的唯一告知载体，直接决定是否属于透明告知还是话术包装；同时可核对是否存在 Cancel 按钮",
        "observable_utg_signals": ["弹窗标题与完整正文文本", "正向按钮 'Accept & Continue' 与负向按钮 'Cancel' 是否同时存在", "弹窗是否可被返回键/点击外部取消", "文案与实际行为（canRetrieveWindowContent=false、空 onAccessibilityEvent）是否一致"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍列表，条目名 'Baby Touch Lock Service'，摘要 'Prevents accidental touches, navigation gestures...'",
        "why_most_useful": "核对系统侧展示名/描述与应用内宣称是否一致，是否存在身份混淆或描述与实际能力不符",
        "observable_utg_signals": ["服务名与摘要原文", "是否由应用代点开启（应无，用户手动操作）", "列表项是否被应用叠加遮罩覆盖或高亮引导"]
      },
      {
        "page_role": "返回应用后的拒权反馈页",
        "page_identifier": "从系统设置返回后的 com.babytouchlock.MainActivity",
        "why_most_useful": "判定是否存在 onResume 死循环重跳设置或定时器反复拉起；本应用应表现为静默刷新状态卡",
        "observable_utg_signals": ["返回后是否立即再次出现系统无障碍页或说明弹窗", "状态卡文案是否仅做 active/inactive 切换", "是否出现重复 startActivity 的堆栈抖动"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。无静态加壳、无加密载荷、无远端 HTML 或云控开关；全部引导文案为原生 strings.xml 纯文本，UTG 可直接提取。唯一需注意：获权后锁定态的 TYPE_ACCESSIBILITY_OVERLAY 全屏层会遮挡下方应用内容，UTG 抓取时应区分该业务遮罩与权限引导界面。"
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
    "com.babytouchlock.MainActivity.showAccessibilityConsentDialog",
    "com.babytouchlock.MainActivity.showAccessibilityConsentDialog$lambda$14",
    "com.babytouchlock.MainActivity.checkPermissionsUI",
    "com.babytouchlock.MainActivity.setupButtons$lambda$13",
    "com.babytouchlock.BabyTouchLockAccessibilityService.showLockWindows",
    "res/xml/accessibility_service_config.xml + res/values/strings.xml（disclosure_dialog_text / accessibility_service_description / grant_permission）"
  ]
}
```

</details>
