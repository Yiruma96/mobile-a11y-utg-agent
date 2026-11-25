# BN_017__6fe5e6bf33｜显示调节、截屏与分屏效率 — Screenshot Tile

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：163.9s

## 1. 一句话核心结论

- **核心申请方式**：该应用仅在用户主动开启“原生截屏方法”或悬浮按钮时，先弹出 Google Play 显著披露同意框，再（Android 13+）弹受限设置教学框，最后跳系统无障碍设置页并配合 Toast 提醒，全程可取消且保留传统 MediaProjection 降级路径。
- **静态可见性说明**：无障碍引导全链路均在 DEX 明文可见：MainActivity 的原生方法开关回调、Google Play 显著披露 AlertDialog、Android 13+ 受限设置教学弹窗、Companion.openAccessibilitySettings 的 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转与延迟 Toast，对应文案位于 res/values/strings.xml，示意图位于 res/drawable/restricted_settings 与 res/layout/activity_main.xml；未发现加壳、加密载荷或远端 HTML 引导页（assets 内仅 features.html / license.html / open_source_licenses.html 等本地静态说明）。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6fe5e6bf33dc38de7ed7e04474d9fe8d138cfe68a33766016d58329053b27c2d` |
| 包名 / 年份 | `com.github.cvzi.screenshottile` / 2025-2026 |
| 家族 / 品类 | **显示调节、截屏与分屏效率**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.github.cvzi.screenshottile_150.apk |
| 桌面显示名 | Screenshot Tile |
| 引导页宣称品牌/身份 | Screenshot Tile（开源截屏快捷磁贴工具，披露文案自称 “Screenshot Tile [No root]”，并主动声明“本应用不是无障碍工具”） |
| 系统无障碍列表服务名 | Screenshot Tile |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅观察到多数字符串带前导 U+200C（零宽非连接符），属排版/翻译处理痕迹，不影响可见文案语义；未发现空白挤出警告、同形字、多 activity-alias、伪造 isAccessibilityTool 或高仿系统设置页。 |
| 无障碍服务类名 | `com.github.cvzi.screenshottile.services.ScreenshotAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | ‌If this service is enabled, the app can simulate a power+home button press to take screenshots.<br>On some devices enabling this method may be more stable or faster than the default method.<br><br>If you enable the service here, you also need to enable the native method in the app settings. / ‌If this service is enabled, the app can simulate a power+home button press to take screenshots.<br>On some devices enabling this method may be more stable or faster than the default method.<br><br>If you enable the service here, you also need to enable the native method in the app settings. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.github.cvzi.screenshottile.activities.MainActivity（activity_main.xml 中 nativeCardView 内的 switchNative 开关） | 用户点击 “Use native screenshot method” 开关，触发 SwitchMaterial.onCheckedChanged → onCreate$lambda$14 | 原生Activity | **原文**：Native Method / Simulate home + power button press / Accessibility settings<br>**译注**：原生方法 / 模拟 Home + 电源键按下 / 无障碍设置（按钮） | 用户可随时不打开该开关，继续使用原有 MediaProjection 截屏方式；开关在未同意披露时会自动回滚为关闭 | `MainActivity#onCreate$lambda$14；res/layout/activity_main.xml（switchNative / textTitleNative / buttonAccessibilitySettings）` |
| 2 | 引导说明页 | MainActivity 内不可跳过的显著披露 AlertDialog（AppCompat AlertDialog） | onCreate$lambda$14 检测到 z==true 且 !accessibilityConsent 且 SDK>=28，回滚开关后调用 askToEnableAccessibility() | 原生Dialog | **原文**：Google Play Prominent Disclosure & Consent Requirement … This app - “Screenshot Tile [No root]“ - is not an accessibility tool. … This app requires access to Accessibility Services API in order to take a screenshot when the app is not in use. … Data is neither collected nor shared by this app using the accessibility capabilities. … Do you agree to authorize this app to gain access to the Accessibility Services API and to use the accessibility capabilities to record the screen?<br>**译注**：Google Play 显著披露与同意要求 …… 本应用 “Screenshot Tile [No root]” 不是无障碍工具。…… 本应用需要访问无障碍服务 API 以便在应用未使用时截屏。…… 本应用不会借助无障碍能力收集或共享数据。…… 您是否同意授权本应用访问无障碍服务 API 并使用无障碍能力录制屏幕？ | 点击 “I agree”（同意并继续跳转）或 “I refuse”（拒绝，停留在本页且不跳设置） | `MainActivity#askToEnableAccessibility；res/values/strings.xml googleplay_consent_title / line_0..7 / yes / no` |
| 3 | 拒权反馈循环 | MainActivity（拒绝后原地停留，无重跳） | askToEnableAccessibility 负按钮 onClick（googleplay_consent_no），listener 传 null 语义为仅关闭对话框；accessibilityConsent 保持 false | 原生Dialog | **原文**：I refuse<br>**译注**：我拒绝（关闭弹窗，开关保持关闭状态） | 无需操作；用户可继续使用 legacy 截屏方法，不会自动再次弹窗 | `MainActivity#askToEnableAccessibility（setNegativeButton R$string.googleplay_consent_no）` |
| 4 | 获权后动作 / 跳受限设置 | MainActivity 内 AlertDialog + 系统“应用信息”页（ACTION_APPLICATION_DETAILS_SETTINGS） | 同意披露后 openAccessibilitySettings 打开系统无障碍页并设置 return_if_accessibility；返回应用后 onResume → updateSwitches()，若 useNative 且 SDK>=33 且服务仍未连接则 informAboutRestrictedSettings() | 原生Dialog | **原文**：Enable accessibility service / If the accessibility settings are grayed out, you will need to allow the "restricted settings" first. The "restricted settings" can be found in the "App info": / Allow restricted settings / Open accessibility settings / Cancel<br>**译注**：启用无障碍服务 / 若无障碍设置项呈灰色不可选，需先允许“受限设置”，其位置在“应用信息”中： / 允许受限设置 / 打开无障碍设置 / 取消 | 可点 “Allow restricted settings” 进入应用详情页手动开启受限设置，或点 “Open accessibility settings” 直接进无障碍页，或点 “Cancel” 放弃 | `MainActivity#informAboutRestrictedSettings；MainActivity#informAboutRestrictedSettings$lambda$0；res/values/strings.xml restricted_settings_*；res/drawable/restricted_settings` |
| 5 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（ScreenshotAccessibilityService 列表项，标签 “Screenshot Tile”） | ScreenshotAccessibilityService$Companion.openAccessibilitySettings(Activity\|TileService, String) 被同意按钮 / 受限设置弹窗正按钮 / 悬浮按钮开关 / 磁贴入口调用 | 系统无障碍页 | **原文**：Please activate "%1s" in the accessibility settings（实际渲染为 Please activate "Screenshot Tile" in the accessibility settings）<br>**译注**：请在无障碍设置中启用“Screenshot Tile” | 在系统无障碍列表中手动点击 Screenshot Tile 并开启服务；用户可随时返回 | `ScreenshotAccessibilityService$Companion#openAccessibilitySettings；ScreenshotAccessibilityService$Companion#toastMessageAccessibility；res/values/strings.xml toast_open_accessibility_settings` |
| 6 | 遮罩叠层指引 | 系统设置页上方的应用 Toast（非悬浮窗、非遮罩） | openAccessibilitySettings 内 Handler.postDelayed(..., 2000L) 与 (..., 4000L) 各触发一次 toastMessageAccessibility | 通知栏 | **原文**：Please activate "Screenshot Tile" in the accessibility settings<br>**译注**：请在无障碍设置中启用“Screenshot Tile” | 仅提示，不拦截操作，不覆盖系统开关控件，不自动点击 | `ScreenshotAccessibilityService$Companion#openAccessibilitySettings（postDelayed 2000/4000ms）；openAccessibilitySettings$lambda$0$0 / $lambda$1$0` |
| 7 | 拒权反馈循环 | MainActivity.onResume → updateSwitches()（回归主界面，附可点击警示 TextView） | 用户从系统设置返回触发 onResume | 原生Activity | **原文**：⚠ Accessibility service is disabled<br>**译注**：⚠ 无障碍服务已禁用（点击该提示可再次前往无障碍设置） | 提示可点击重试，也可忽略继续使用 legacy 截屏；不自动重跳、无定时器强拉 | `MainActivity#onResume；MainActivity#updateSwitches；res/values/strings.xml use_native_screenshot_unavailable` |
| 8 | 获权后动作 | com.github.cvzi.screenshottile.services.ScreenshotAccessibilityService（悬浮按钮/截屏执行） | 服务连接后 onServiceConnected，updateSwitches 检测 getInstance()!=null 并移除警示；按 pref 显示悬浮按钮 | 悬浮窗Overlay | **原文**：无（悬浮按钮为图标控件，非文字引导）<br>**译注**：获权后按用户设置显示悬浮按钮/侧栏按钮，用于触发截屏 | 无强制动作；用户可随时在系统设置关闭服务 | `ScreenshotAccessibilityService#onServiceConnected；ScreenshotAccessibilityService#showFloatingButton；ScreenshotAccessibilityService#updateFloatingButton` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 主界面“Native Method”卡片正文（res/values/strings.xml main_native_method_text / main_native_method_text_android_since_11），说明需先在手机设置中启用无障碍服务并提示按下方按钮
- MainActivity 主界面 “Accessibility settings” 按钮（res/values/strings.xml main_accessibility_settings，activity_main.xml buttonAccessibilitySettings），点击直达系统无障碍页
- MainActivity 内 Google Play 显著披露 AlertDialog（可取消，正/负按钮 I agree / I refuse），文案来自 strings.xml googleplay_consent_line_0..7
- MainActivity 内 Android 13+ 受限设置教学 AlertDialog（含 res/drawable/restricted_settings 示意图，正/中性/负三按钮），文案来自 strings.xml restricted_settings_title / restricted_settings_text / restricted_settings_open_settings / restricted_settings_open_accessibility
- 主界面内嵌警示 TextView “⚠ Accessibility service is disabled”（updateSwitches 动态 addView 至 linearLayoutNative 索引 1，可点击跳设置）
- 系统无障碍设置页上的应用 Toast “Please activate "Screenshot Tile" in the accessibility settings”（strings.xml toast_open_accessibility_settings，跳转即刻 + 2s + 4s 三次）
- 系统无障碍列表中的服务项说明 android:description（strings.xml accessibility_service_description，如实说明模拟 Home+Power 截屏且需在应用设置中再启用原生方式）
- 本地静态说明页 assets/features.html（第 32-33 行描述 Native Method 机制，第 114 行描述 Restricted Settings Bypass 的应用内说明）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Play requires prominent disclosure of the Accessibility Services API’s use for an app that is not an accessibility tool. | 对于并非无障碍工具的应用，Google Play 要求就其使用无障碍服务 API 进行显著披露。 | `res/values/strings.xml googleplay_consent_line_0` | 良性透明说明 |
| en | This app - “Screenshot Tile [No root]“ - is not an accessibility tool. | 本应用——“Screenshot Tile [No root]”——不是无障碍工具。 | `res/values/strings.xml googleplay_consent_line_1` | 良性透明说明 |
| en | This app requires access to Accessibility Services API in order to take a screenshot when the app is not in use. | 本应用需要访问无障碍服务 API，以便在应用未被使用时截取屏幕。 | `res/values/strings.xml googleplay_consent_line_3` | 良性透明说明 |
| en | Access to Accessibility Services API will allow this app to record the screen. | 访问无障碍服务 API 将使本应用能够录制屏幕。 | `res/values/strings.xml googleplay_consent_line_4` | 良性透明说明 |
| en | Data is neither collected nor shared by this app using the accessibility capabilities. | 本应用不会通过无障碍能力收集或共享任何数据。 | `res/values/strings.xml googleplay_consent_line_6` | 隐私承诺 |
| en | Do you agree to authorize this app to gain access to the Accessibility Services API and to use the accessibility capabilities to record the screen? | 您是否同意授权本应用访问无障碍服务 API，并使用无障碍能力录制屏幕？ | `res/values/strings.xml googleplay_consent_line_7` | 良性透明说明 |
| en | I agree / I refuse | 我同意 / 我拒绝 | `res/values/strings.xml googleplay_consent_yes / googleplay_consent_no` | 良性透明说明 |
| en | Enable accessibility service | 启用无障碍服务 | `res/values/strings.xml restricted_settings_title` | 受限设置分步教学 |
| en | If the accessibility settings are grayed out, you will need to allow the "restricted settings" first. The "restricted settings" can be found in the "App info": | 若无障碍设置项呈灰色不可选，您需要先允许“受限设置”。“受限设置”可在“应用信息”中找到： | `res/values/strings.xml restricted_settings_text` | 受限设置分步教学 |
| en | Allow restricted settings / Open accessibility settings / Cancel | 允许受限设置 / 打开无障碍设置 / 取消 | `res/values/strings.xml restricted_settings_open_settings / restricted_settings_open_accessibility / android.R.string.cancel` | 受限设置分步教学 |
| en | Please activate "%1s" in the accessibility settings | 请在无障碍设置中启用“%1s”（实际渲染为 Screenshot Tile） | `res/values/strings.xml toast_open_accessibility_settings` | 良性透明说明 |
| en | If this service is enabled, the app can simulate a power+home button press to take screenshots.<br>On some devices enabling this method may be more stable or faster than the default method.<br><br>If you enable the service here, you also need to enable the native method in the app settings. | 若启用此服务，本应用可模拟“电源键+Home 键”按键来截屏。在某些设备上，启用此方式可能比默认方式更稳定或更快。若您在此处启用了服务，还需在应用设置中启用“原生方法”。 | `res/values/strings.xml accessibility_service_description（Manifest android:description）` | 良性透明说明 |
| en | The native method to take screenshots simulates a press of Home+Power button and uses the screenshot method of your device. Before you can take a screenshot you need to enable the accessibility service in the phone settings. Press the button below to open the accessibility settings. | 原生截屏方法模拟按下 Home+电源键并使用设备自带的截屏机制。截屏前您需要在手机设置中启用无障碍服务，请按下方按钮打开无障碍设置。 | `res/values/strings.xml main_native_method_text` | 受限设置分步教学 |
| en | ⚠ Accessibility service is disabled | ⚠ 无障碍服务已禁用 | `res/values/strings.xml use_native_screenshot_unavailable（MainActivity#updateSwitches 动态添加）` | 良性透明说明 |
| en | Restricted Settings Bypass: In-app instructions for enabling Accessibility services on Android 13+ devices where they might be restricted. | 受限设置绕过：在 Android 13+ 设备上为可能被限制的无障碍服务提供应用内启用说明。 | `assets/features.html 第 114 行` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环重跳。拒绝披露（I refuse）仅关闭对话框，开关回滚为关闭；从系统设置返回后 onResume 只调用 updateSwitches() 刷新界面并显示可点击的“⚠ Accessibility service is disabled”提示，不自动再次拉起设置页；仅在用户再次点击开关时才会重新进入引导流程。
- **遮罩叠层 / 高仿系统设置页**：无。既无半透明遮罩层、无全屏悬浮窗、也无高仿系统无障碍开关页；引导仅为原生 AlertDialog 与跳转后的应用 Toast（2s/4s 各一次），Toast 不拦截也不遮挡系统开关。
- **Android 13+ 受限设置（Restricted Settings）应对**：有，且为公开说明式教学：informAboutRestrictedSettings() 仅在 SDK_INT>=33、useNative 已启用且服务未连接时弹出，标题 “Enable accessibility service”，正文说明无障碍设置变灰时需先在“应用信息”中允许“受限设置”，中性按钮 “Allow restricted settings” 直接跳 ACTION_APPLICATION_DETAILS_SETTINGS(package:自身包名) 让用户自行手动操作，未使用 Session 安装器绕过，也未伪造系统页面。
- **获权后即时行为与防撤权机制**：无。未发现获权后自点确认、自动授权、监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权等行为；PERFORM_GLOBAL_ACTION 仅用于模拟 Home+Power 完成截屏。
- **良性降级 / 替代方案**：有。主界面保留 legacy 截屏方式（switchLegacy 对应 MediaProjection/快捷磁贴路径），用户拒绝披露或不启用无障碍服务时仍可正常截屏；披露弹窗与受限设置弹窗均可取消，主界面始终显示两种方法可切换。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS（data=package:com.github.cvzi.screenshottile）时立即开始 UTG 抓取，并回溯抓取其前置 AlertDialog；同时可在冷启动后点击“Use native screenshot method”开关以稳定复现完整链路。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本应用引导文案全部为文本，唯一图像为受限设置示意图（辅助说明，非诱导主体），无需 OCR；静态加壳初判为 False 且实际代码明文可读，不存在一阶段 Dropper 或远端 HTML 引导页导致的盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前显著披露同意弹窗页** | AppCompat AlertDialog，标题 “Google Play Prominent Disclosure & Consent Requirement”，正按钮 “I agree”、负按钮 “I refuse”，正文含 8 段披露文字 | 该弹窗是判断“是否使用恐吓/伪装话术诱导授权”的第一判据；此应用文案主动声明“不是无障碍工具”并说明数据不收集，可据此区分良性披露与恶意诱导。 | 对话框标题与正文完整文本（googleplay_consent_*）；是否存在负按钮/取消按钮及其可点击性；弹窗是否可返回键取消；弹窗是否覆盖系统设置页（叠加遮罩判别） |
| **Android 13+ 受限设置教学弹窗页** | AlertDialog，标题 “Enable accessibility service”，含 ImageView(res/drawable/restricted_settings) 与三按钮 Allow restricted settings / Open accessibility settings / Cancel | 受限设置教学是 13+ 诱导的高发点；此处可通过文案与按钮走向区分“如实教学”与“伪造系统 UI / 教唆绕过安全警告”。 | 标题与正文文本是否与 restricted_settings_* 一致；中性按钮是否直接跳到真实系统应用详情页（包名可见）；是否存在 Cancel 按钮；有无高仿系统开关控件 |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载/已安装的服务列表项，标签 “Screenshot Tile”，副标题为 accessibility_service_description | 核对无障碍服务标签与应用显示名是否一致，并确认系统呈现的用途说明是否如实，用于身份一致性判定。 | 服务标签文本与桌面应用名是否一致；服务说明文本内容；是否出现多个同名/多别名服务项 |
| **跳设置后提示与返回态页面** | 系统无障碍页上方的应用 Toast；返回后的 MainActivity 主界面（含 “⚠ Accessibility service is disabled” 可点击 TextView） | 用于判断是否存在遮罩叠层指引或拒权死循环重跳；本应用为 Toast 提示 + 原地提示，属良性表现。 | 设置页上方是否为 Toast 而非悬浮遮罩窗口；返回应用后是否自动再次跳设置（重跳计数）；主界面警示文本及开关状态 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.github.cvzi.screenshottile.activities.MainActivity#onCreate$lambda$14`
- `com.github.cvzi.screenshottile.activities.MainActivity#askToEnableAccessibility`
- `com.github.cvzi.screenshottile.activities.MainActivity#informAboutRestrictedSettings`
- `com.github.cvzi.screenshottile.services.ScreenshotAccessibilityService$Companion#openAccessibilitySettings`
- `res/values/strings.xml (googleplay_consent_line_0..7 / restricted_settings_* / toast_open_accessibility_settings)`
- `res/layout/activity_main.xml (switchNative / buttonAccessibilitySettings)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**总体判断：这是透明、合规的无障碍权限引导，未发现诱导或伪装。** 全流程为「用户主动打开功能开关 → 显著披露同意弹窗 → 系统无障碍设置页 → 提示性 Toast 提醒」，全程有取消按钮、无遮罩叠层、无拒权死循环重跳。

关键事实：

1. **入口是业务功能触发，并非冷启动强推**：[MainActivity.onCreate$lambda$14](<resource-unit:#1.dex1 code:com.github.cvzi.screenshottile.activities.MainActivity#onCreate$lambda$14>) 在 `switchNative`（"Use native screenshot method"）被打开时，若 `accessibilityConsent` 为假则回滚开关并调用 `askToEnableAccessibility()`；[MainActivity.onCreate$lambda$16](<resource-unit:#1.dex1 code:com.github.cvzi.screenshottile.activities.MainActivity#onCreate$lambda$16>) 的悬浮按钮开关走同一路径。
2. **第一层是 Google Play 显著披露弹窗（原生 AlertDialog，可拒绝）**：[askToEnableAccessibility()](<resource-unit:#1.dex1 code:com.github.cvzi.screenshottile.activities.MainActivity#askToEnableAccessibility>) 拼接 `googleplay_consent_line_0..7`，标题为 “Google Play Prominent Disclosure & Consent Requirement”，正按钮 “I agree” / 负按钮 “I refuse”。文案明确写「本应用不是无障碍工具」「数据不被收集或共享」。
3. **第二层是 Android 13+ 受限设置教学（可取消）**：[informAboutRestrictedSettings()](<resource-unit:#1.dex1 code:com.github.cvzi.screenshottile.activities.MainActivity#informAboutRestrictedSettings>) 仅在 `SDK_INT>=33` 且原生方法已启用、服务未连接时弹出，含示意图 `@drawable/restricted_settings`，中性按钮 “Allow restricted settings” → [APPLICATION_DETAILS_SETTINGS 跳转](<resource-unit:#1.dex1 code:com.github.cvzi.screenshottile.activities.MainActivity#informAboutRestrictedSettings$lambda$0>)，正按钮 “Open accessibility settings” → 无障碍页，负按钮 `android.R.string.cancel`。属于标准分步教学，非恐吓或假故障。
4. **第三层是跳系统无障碍页并附提示**：[openAccessibilitySettings()](<resource-unit:#1.dex1 code:com.github.cvzi.screenshottile.services.ScreenshotAccessibilityService$Companion#openAccessibilitySettings>) 先 `toastMessageAccessibility()` 显示 “Please activate "Screenshot Tile" in the accessibility settings”，再 `startActivity(ACTION_ACCESSIBILITY_SETTINGS)`，并用 `postDelayed` 在 2000ms/4000ms 各补一次 Toast 提醒（是 Toast，不是悬浮窗，不遮挡系统开关）。
5. **拒权行为良性**：`onResume` 只调用 `updateSwitches()` 刷新 UI 与“Accessibility service is disabled”提示，不回跳、不循环拉起；主界面保留 legacy MediaProjection 截屏路径（`switchLegacy`）作为降级方案。`assets/features.html` 亦公开写明 “Restricted Settings Bypass: In-app instructions...”。
6. **身份一致**：桌面名 `Screenshot Tile`、无障碍服务标签 `Screenshot Tile`、披露文案 “Screenshot Tile [No root]” 同源；`android:description` 如实说明模拟 Home+Power 截屏并需在应用设置中再启用原生方式。字符串虽普遍带前导 U+200C（零宽非连接符，为翻译/排版处理），不构成同形字或空白挤出伪装；未见 `isAccessibilityTool` 伪造、多 activity-alias、悬浮遮罩或自点确认防撤权。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路均在 DEX 明文可见：MainActivity 的原生方法开关回调、Google Play 显著披露 AlertDialog、Android 13+ 受限设置教学弹窗、Companion.openAccessibilitySettings 的 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转与延迟 Toast，对应文案位于 res/values/strings.xml，示意图位于 res/drawable/restricted_settings 与 res/layout/activity_main.xml；未发现加壳、加密载荷或远端 HTML 引导页（assets 内仅 features.html / license.html / open_source_licenses.html 等本地静态说明）。",
  "summary_one_liner": "该应用仅在用户主动开启“原生截屏方法”或悬浮按钮时，先弹出 Google Play 显著披露同意框，再（Android 13+）弹受限设置教学框，最后跳系统无障碍设置页并配合 Toast 提醒，全程可取消且保留传统 MediaProjection 降级路径。",
  "disguise_identity": {
    "app_display_name": "Screenshot Tile",
    "claimed_brand_or_persona": "Screenshot Tile（开源截屏快捷磁贴工具，披露文案自称 “Screenshot Tile [No root]”，并主动声明“本应用不是无障碍工具”）",
    "a11y_service_label": "Screenshot Tile",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅观察到多数字符串带前导 U+200C（零宽非连接符），属排版/翻译处理痕迹，不影响可见文案语义；未发现空白挤出警告、同形字、多 activity-alias、伪造 isAccessibilityTool 或高仿系统设置页。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.github.cvzi.screenshottile.activities.MainActivity（activity_main.xml 中 nativeCardView 内的 switchNative 开关）",
      "trigger_event": "用户点击 “Use native screenshot method” 开关，触发 SwitchMaterial.onCheckedChanged → onCreate$lambda$14",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Native Method / Simulate home + power button press / Accessibility settings",
      "shown_text_zh": "原生方法 / 模拟 Home + 电源键按下 / 无障碍设置（按钮）",
      "user_action_requested": "用户可随时不打开该开关，继续使用原有 MediaProjection 截屏方式；开关在未同意披露时会自动回滚为关闭",
      "code_anchor": "MainActivity#onCreate$lambda$14；res/layout/activity_main.xml（switchNative / textTitleNative / buttonAccessibilitySettings）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 内不可跳过的显著披露 AlertDialog（AppCompat AlertDialog）",
      "trigger_event": "onCreate$lambda$14 检测到 z==true 且 !accessibilityConsent 且 SDK>=28，回滚开关后调用 askToEnableAccessibility()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Google Play Prominent Disclosure & Consent Requirement … This app - “Screenshot Tile [No root]“ - is not an accessibility tool. … This app requires access to Accessibility Services API in order to take a screenshot when the app is not in use. … Data is neither collected nor shared by this app using the accessibility capabilities. … Do you agree to authorize this app to gain access to the Accessibility Services API and to use the accessibility capabilities to record the screen?",
      "shown_text_zh": "Google Play 显著披露与同意要求 …… 本应用 “Screenshot Tile [No root]” 不是无障碍工具。…… 本应用需要访问无障碍服务 API 以便在应用未使用时截屏。…… 本应用不会借助无障碍能力收集或共享数据。…… 您是否同意授权本应用访问无障碍服务 API 并使用无障碍能力录制屏幕？",
      "user_action_requested": "点击 “I agree”（同意并继续跳转）或 “I refuse”（拒绝，停留在本页且不跳设置）",
      "code_anchor": "MainActivity#askToEnableAccessibility；res/values/strings.xml googleplay_consent_title / line_0..7 / yes / no"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity（拒绝后原地停留，无重跳）",
      "trigger_event": "askToEnableAccessibility 负按钮 onClick（googleplay_consent_no），listener 传 null 语义为仅关闭对话框；accessibilityConsent 保持 false",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "I refuse",
      "shown_text_zh": "我拒绝（关闭弹窗，开关保持关闭状态）",
      "user_action_requested": "无需操作；用户可继续使用 legacy 截屏方法，不会自动再次弹窗",
      "code_anchor": "MainActivity#askToEnableAccessibility（setNegativeButton R$string.googleplay_consent_no）"
    },
    {
      "step": 4,
      "stage": "获权后动作 / 跳受限设置",
      "screen_or_component": "MainActivity 内 AlertDialog + 系统“应用信息”页（ACTION_APPLICATION_DETAILS_SETTINGS）",
      "trigger_event": "同意披露后 openAccessibilitySettings 打开系统无障碍页并设置 return_if_accessibility；返回应用后 onResume → updateSwitches()，若 useNative 且 SDK>=33 且服务仍未连接则 informAboutRestrictedSettings()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable accessibility service / If the accessibility settings are grayed out, you will need to allow the \"restricted settings\" first. The \"restricted settings\" can be found in the \"App info\": / Allow restricted settings / Open accessibility settings / Cancel",
      "shown_text_zh": "启用无障碍服务 / 若无障碍设置项呈灰色不可选，需先允许“受限设置”，其位置在“应用信息”中： / 允许受限设置 / 打开无障碍设置 / 取消",
      "user_action_requested": "可点 “Allow restricted settings” 进入应用详情页手动开启受限设置，或点 “Open accessibility settings” 直接进无障碍页，或点 “Cancel” 放弃",
      "code_anchor": "MainActivity#informAboutRestrictedSettings；MainActivity#informAboutRestrictedSettings$lambda$0；res/values/strings.xml restricted_settings_*；res/drawable/restricted_settings"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（ScreenshotAccessibilityService 列表项，标签 “Screenshot Tile”）",
      "trigger_event": "ScreenshotAccessibilityService$Companion.openAccessibilitySettings(Activity|TileService, String) 被同意按钮 / 受限设置弹窗正按钮 / 悬浮按钮开关 / 磁贴入口调用",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please activate \"%1s\" in the accessibility settings（实际渲染为 Please activate \"Screenshot Tile\" in the accessibility settings）",
      "shown_text_zh": "请在无障碍设置中启用“Screenshot Tile”",
      "user_action_requested": "在系统无障碍列表中手动点击 Screenshot Tile 并开启服务；用户可随时返回",
      "code_anchor": "ScreenshotAccessibilityService$Companion#openAccessibilitySettings；ScreenshotAccessibilityService$Companion#toastMessageAccessibility；res/values/strings.xml toast_open_accessibility_settings"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统设置页上方的应用 Toast（非悬浮窗、非遮罩）",
      "trigger_event": "openAccessibilitySettings 内 Handler.postDelayed(..., 2000L) 与 (..., 4000L) 各触发一次 toastMessageAccessibility",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Please activate \"Screenshot Tile\" in the accessibility settings",
      "shown_text_zh": "请在无障碍设置中启用“Screenshot Tile”",
      "user_action_requested": "仅提示，不拦截操作，不覆盖系统开关控件，不自动点击",
      "code_anchor": "ScreenshotAccessibilityService$Companion#openAccessibilitySettings（postDelayed 2000/4000ms）；openAccessibilitySettings$lambda$0$0 / $lambda$1$0"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onResume → updateSwitches()（回归主界面，附可点击警示 TextView）",
      "trigger_event": "用户从系统设置返回触发 onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "⚠ Accessibility service is disabled",
      "shown_text_zh": "⚠ 无障碍服务已禁用（点击该提示可再次前往无障碍设置）",
      "user_action_requested": "提示可点击重试，也可忽略继续使用 legacy 截屏；不自动重跳、无定时器强拉",
      "code_anchor": "MainActivity#onResume；MainActivity#updateSwitches；res/values/strings.xml use_native_screenshot_unavailable"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.github.cvzi.screenshottile.services.ScreenshotAccessibilityService（悬浮按钮/截屏执行）",
      "trigger_event": "服务连接后 onServiceConnected，updateSwitches 检测 getInstance()!=null 并移除警示；按 pref 显示悬浮按钮",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（悬浮按钮为图标控件，非文字引导）",
      "shown_text_zh": "获权后按用户设置显示悬浮按钮/侧栏按钮，用于触发截屏",
      "user_action_requested": "无强制动作；用户可随时在系统设置关闭服务",
      "code_anchor": "ScreenshotAccessibilityService#onServiceConnected；ScreenshotAccessibilityService#showFloatingButton；ScreenshotAccessibilityService#updateFloatingButton"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 主界面“Native Method”卡片正文（res/values/strings.xml main_native_method_text / main_native_method_text_android_since_11），说明需先在手机设置中启用无障碍服务并提示按下方按钮",
    "MainActivity 主界面 “Accessibility settings” 按钮（res/values/strings.xml main_accessibility_settings，activity_main.xml buttonAccessibilitySettings），点击直达系统无障碍页",
    "MainActivity 内 Google Play 显著披露 AlertDialog（可取消，正/负按钮 I agree / I refuse），文案来自 strings.xml googleplay_consent_line_0..7",
    "MainActivity 内 Android 13+ 受限设置教学 AlertDialog（含 res/drawable/restricted_settings 示意图，正/中性/负三按钮），文案来自 strings.xml restricted_settings_title / restricted_settings_text / restricted_settings_open_settings / restricted_settings_open_accessibility",
    "主界面内嵌警示 TextView “⚠ Accessibility service is disabled”（updateSwitches 动态 addView 至 linearLayoutNative 索引 1，可点击跳设置）",
    "系统无障碍设置页上的应用 Toast “Please activate \"Screenshot Tile\" in the accessibility settings”（strings.xml toast_open_accessibility_settings，跳转即刻 + 2s + 4s 三次）",
    "系统无障碍列表中的服务项说明 android:description（strings.xml accessibility_service_description，如实说明模拟 Home+Power 截屏且需在应用设置中再启用原生方式）",
    "本地静态说明页 assets/features.html（第 32-33 行描述 Native Method 机制，第 114 行描述 Restricted Settings Bypass 的应用内说明）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Play requires prominent disclosure of the Accessibility Services API’s use for an app that is not an accessibility tool.",
      "text_zh": "对于并非无障碍工具的应用，Google Play 要求就其使用无障碍服务 API 进行显著披露。",
      "source_location": "res/values/strings.xml googleplay_consent_line_0",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This app - “Screenshot Tile [No root]“ - is not an accessibility tool.",
      "text_zh": "本应用——“Screenshot Tile [No root]”——不是无障碍工具。",
      "source_location": "res/values/strings.xml googleplay_consent_line_1",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This app requires access to Accessibility Services API in order to take a screenshot when the app is not in use.",
      "text_zh": "本应用需要访问无障碍服务 API，以便在应用未被使用时截取屏幕。",
      "source_location": "res/values/strings.xml googleplay_consent_line_3",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Access to Accessibility Services API will allow this app to record the screen.",
      "text_zh": "访问无障碍服务 API 将使本应用能够录制屏幕。",
      "source_location": "res/values/strings.xml googleplay_consent_line_4",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Data is neither collected nor shared by this app using the accessibility capabilities.",
      "text_zh": "本应用不会通过无障碍能力收集或共享任何数据。",
      "source_location": "res/values/strings.xml googleplay_consent_line_6",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Do you agree to authorize this app to gain access to the Accessibility Services API and to use the accessibility capabilities to record the screen?",
      "text_zh": "您是否同意授权本应用访问无障碍服务 API，并使用无障碍能力录制屏幕？",
      "source_location": "res/values/strings.xml googleplay_consent_line_7",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "I agree / I refuse",
      "text_zh": "我同意 / 我拒绝",
      "source_location": "res/values/strings.xml googleplay_consent_yes / googleplay_consent_no",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable accessibility service",
      "text_zh": "启用无障碍服务",
      "source_location": "res/values/strings.xml restricted_settings_title",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "If the accessibility settings are grayed out, you will need to allow the \"restricted settings\" first. The \"restricted settings\" can be found in the \"App info\":",
      "text_zh": "若无障碍设置项呈灰色不可选，您需要先允许“受限设置”。“受限设置”可在“应用信息”中找到：",
      "source_location": "res/values/strings.xml restricted_settings_text",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow restricted settings / Open accessibility settings / Cancel",
      "text_zh": "允许受限设置 / 打开无障碍设置 / 取消",
      "source_location": "res/values/strings.xml restricted_settings_open_settings / restricted_settings_open_accessibility / android.R.string.cancel",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please activate \"%1s\" in the accessibility settings",
      "text_zh": "请在无障碍设置中启用“%1s”（实际渲染为 Screenshot Tile）",
      "source_location": "res/values/strings.xml toast_open_accessibility_settings",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "If this service is enabled, the app can simulate a power+home button press to take screenshots.\nOn some devices enabling this method may be more stable or faster than the default method.\n\nIf you enable the service here, you also need to enable the native method in the app settings.",
      "text_zh": "若启用此服务，本应用可模拟“电源键+Home 键”按键来截屏。在某些设备上，启用此方式可能比默认方式更稳定或更快。若您在此处启用了服务，还需在应用设置中启用“原生方法”。",
      "source_location": "res/values/strings.xml accessibility_service_description（Manifest android:description）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The native method to take screenshots simulates a press of Home+Power button and uses the screenshot method of your device. Before you can take a screenshot you need to enable the accessibility service in the phone settings. Press the button below to open the accessibility settings.",
      "text_zh": "原生截屏方法模拟按下 Home+电源键并使用设备自带的截屏机制。截屏前您需要在手机设置中启用无障碍服务，请按下方按钮打开无障碍设置。",
      "source_location": "res/values/strings.xml main_native_method_text",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "⚠ Accessibility service is disabled",
      "text_zh": "⚠ 无障碍服务已禁用",
      "source_location": "res/values/strings.xml use_native_screenshot_unavailable（MainActivity#updateSwitches 动态添加）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Restricted Settings Bypass: In-app instructions for enabling Accessibility services on Android 13+ devices where they might be restricted.",
      "text_zh": "受限设置绕过：在 Android 13+ 设备上为可能被限制的无障碍服务提供应用内启用说明。",
      "source_location": "assets/features.html 第 114 行",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环重跳。拒绝披露（I refuse）仅关闭对话框，开关回滚为关闭；从系统设置返回后 onResume 只调用 updateSwitches() 刷新界面并显示可点击的“⚠ Accessibility service is disabled”提示，不自动再次拉起设置页；仅在用户再次点击开关时才会重新进入引导流程。",
    "overlay_or_fake_settings": "无。既无半透明遮罩层、无全屏悬浮窗、也无高仿系统无障碍开关页；引导仅为原生 AlertDialog 与跳转后的应用 Toast（2s/4s 各一次），Toast 不拦截也不遮挡系统开关。",
    "restricted_settings_13plus_coaching": "有，且为公开说明式教学：informAboutRestrictedSettings() 仅在 SDK_INT>=33、useNative 已启用且服务未连接时弹出，标题 “Enable accessibility service”，正文说明无障碍设置变灰时需先在“应用信息”中允许“受限设置”，中性按钮 “Allow restricted settings” 直接跳 ACTION_APPLICATION_DETAILS_SETTINGS(package:自身包名) 让用户自行手动操作，未使用 Session 安装器绕过，也未伪造系统页面。",
    "post_grant_anti_removal": "无。未发现获权后自点确认、自动授权、监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权等行为；PERFORM_GLOBAL_ACTION 仅用于模拟 Home+Power 完成截屏。",
    "benign_graceful_degradation": "有。主界面保留 legacy 截屏方式（switchLegacy 对应 MediaProjection/快捷磁贴路径），用户拒绝披露或不启用无障碍服务时仍可正常截屏；披露弹窗与受限设置弹窗均可取消，主界面始终显示两种方法可切换。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS（data=package:com.github.cvzi.screenshottile）时立即开始 UTG 抓取，并回溯抓取其前置 AlertDialog；同时可在冷启动后点击“Use native screenshot method”开关以稳定复现完整链路。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前显著披露同意弹窗页",
        "page_identifier": "AppCompat AlertDialog，标题 “Google Play Prominent Disclosure & Consent Requirement”，正按钮 “I agree”、负按钮 “I refuse”，正文含 8 段披露文字",
        "why_most_useful": "该弹窗是判断“是否使用恐吓/伪装话术诱导授权”的第一判据；此应用文案主动声明“不是无障碍工具”并说明数据不收集，可据此区分良性披露与恶意诱导。",
        "observable_utg_signals": ["对话框标题与正文完整文本（googleplay_consent_*）", "是否存在负按钮/取消按钮及其可点击性", "弹窗是否可返回键取消", "弹窗是否覆盖系统设置页（叠加遮罩判别）"]
      },
      {
        "page_role": "Android 13+ 受限设置教学弹窗页",
        "page_identifier": "AlertDialog，标题 “Enable accessibility service”，含 ImageView(res/drawable/restricted_settings) 与三按钮 Allow restricted settings / Open accessibility settings / Cancel",
        "why_most_useful": "受限设置教学是 13+ 诱导的高发点；此处可通过文案与按钮走向区分“如实教学”与“伪造系统 UI / 教唆绕过安全警告”。",
        "observable_utg_signals": ["标题与正文文本是否与 restricted_settings_* 一致", "中性按钮是否直接跳到真实系统应用详情页（包名可见）", "是否存在 Cancel 按钮", "有无高仿系统开关控件"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载/已安装的服务列表项，标签 “Screenshot Tile”，副标题为 accessibility_service_description",
        "why_most_useful": "核对无障碍服务标签与应用显示名是否一致，并确认系统呈现的用途说明是否如实，用于身份一致性判定。",
        "observable_utg_signals": ["服务标签文本与桌面应用名是否一致", "服务说明文本内容", "是否出现多个同名/多别名服务项"]
      },
      {
        "page_role": "跳设置后提示与返回态页面",
        "page_identifier": "系统无障碍页上方的应用 Toast；返回后的 MainActivity 主界面（含 “⚠ Accessibility service is disabled” 可点击 TextView）",
        "why_most_useful": "用于判断是否存在遮罩叠层指引或拒权死循环重跳；本应用为 Toast 提示 + 原地提示，属良性表现。",
        "observable_utg_signals": ["设置页上方是否为 Toast 而非悬浮遮罩窗口", "返回应用后是否自动再次跳设置（重跳计数）", "主界面警示文本及开关状态"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本应用引导文案全部为文本，唯一图像为受限设置示意图（辅助说明，非诱导主体），无需 OCR；静态加壳初判为 False 且实际代码明文可读，不存在一阶段 Dropper 或远端 HTML 引导页导致的盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.github.cvzi.screenshottile.activities.MainActivity#onCreate$lambda$14",
    "com.github.cvzi.screenshottile.activities.MainActivity#askToEnableAccessibility",
    "com.github.cvzi.screenshottile.activities.MainActivity#informAboutRestrictedSettings",
    "com.github.cvzi.screenshottile.services.ScreenshotAccessibilityService$Companion#openAccessibilitySettings",
    "res/values/strings.xml (googleplay_consent_line_0..7 / restricted_settings_* / toast_open_accessibility_settings)",
    "res/layout/activity_main.xml (switchNative / buttonAccessibilitySettings)"
  ]
}
```

</details>
