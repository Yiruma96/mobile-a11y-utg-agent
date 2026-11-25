# BN_055__09abdca43d｜系统清理与省电冻结 — SuperFreezZ

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：99.1s

## 1. 一句话核心结论

- **核心申请方式**：SuperFreezZ 在 AppIntro 引导流程最后一页用 Yes/No 对等卡片说明无障碍服务的优缺点与作用范围，用户选 Yes 后弹出带取消按钮的说明弹窗，再跳转标准系统 ACTION_ACCESSIBILITY_SETTINGS 页，由用户自行开启，未授权则停留原页并提供手动冻结降级模式。
- **静态可见性说明**：全部引导文案与跳转逻辑均静态可见：res/values/strings.xml（accessibility_service、accessibility_service_description、accessibility_service_dialog_message、accessibility_arguments_yes/no）、res/layout/fragment_accessibility_service_chooser.xml、res/xml/accessibility_service.xml，以及 classes.dex 中 IntroActivity/AccessibilityServiceChooserFragment/GeneralUIKt 的完整实现。无加壳、无密文载荷、无远端 HTML、无 WebView。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `09abdca43d35df17040901e3bca6d6f97cb4a90c76845d01c7ab9ab08f44d152` |
| 包名 / 年份 | `superfreeze.tool.android` / 2025-2026 |
| 家族 / 品类 | **系统清理与省电冻结**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/superfreeze.tool.android_1001.apk |
| 桌面显示名 | SuperFreezZ |
| 引导页宣称品牌/身份 | SuperFreezZ（开源系统清理/省电冻结工具，F-Droid 分发） |
| 系统无障碍列表服务名 | SuperFreezZ（无障碍列表项由 android:label=@string/app_name 提供，description 为 accessibility_service_description） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。无空白/换行挤出警告文案、无同形字、无多 activity-alias、未伪造 isAccessibilityTool。仅 IntroActivity 支持额外 action superfreeze.tool.androidSHOW_ACCESSIBILITY_SERVICE_CHOOSER 以便从设置页直达选择页，属常规内部导航。 |
| 无障碍服务类名 | `superfreeze.tool.android.backend.FreezerService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.android.settings |
| 共现高危权限 | `PACKAGE_USAGE_STATS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Turning this on lets you automatically freeze apps. <br> <br>Advantages: <br>• No user interaction: Faster. No need to know how to do it. <br>• Disabled users can use the freeze shortcut (via speech recognition, for example), freezing all apps automatically. <br> <br>SuperFreezZ uses the accessibility service when tapping "FORCE STOP", "OK", and "Back". Retrieval of window content finds these buttons, and observation of actions is needed to know when they appear. <br> <br>The accessibility service can also be used to lock the screen after freezing on newer Android versions. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | superfreeze.tool.android.userInterface.mainActivity.MainActivity | onResume() 中 DatabaseKt.getPrefIntroAlreadyShown() 为真时 startActivity(IntroActivity) | 原生Activity | **原文**：无（仅跳转，无文案）<br>**译注**：首次启动直接进入引导流程页，不展示额外弹窗 | 无，自动跳转 | `MainActivity.onResume` |
| 2 | 引导说明页 | superfreeze.tool.android.userInterface.intro.IntroActivity（AppIntro，含 WelcomeFragment / 2×AppIntroFragment / IntroModesFragment / AccessibilityServiceChooserFragment） | IntroActivity.onCreate() 中 addSlide(...)，并 showSkipButton(false) 隐藏跳过按钮 | 原生Activity | **原文**：Accessibility Service / Automate the freezing of apps?<br>**译注**：「无障碍服务」「是否自动化冻结应用？」等分页标题与说明 | 逐页 NEXT（隐藏了 SKIP，但页面底部提供 BACK 与最终 DONE）；文案键 app_intro_skip_button 存在但被 showSkipButton(false) 关闭 | `IntroActivity.onCreate；strings.xml: accessibility_service / automate_the_freezing_of_apps` |
| 3 | 引导说明页 | AccessibilityServiceChooserFragment（fragment_accessibility_service_chooser.xml，Yes/No 对等卡片） | onCreateView() 为 R$id.accessibilityYes / R$id.accessibilityNo 分别 setOnClickListener | 原生Activity | **原文**：For: • Ease of use • Freezing a lot of apps / You will have to press "FORCE STOP", "OK" and "Back" manually to freeze an app. For: • Slow devices • Security concerns • No registration of SuperFreezZ as an accessibility service<br>**译注**：Yes 卡片列出「易用、可批量冻结大量应用」；No 卡片如实列出「需手动依次点击 FORCE STOP/OK/Back，适用于慢设备、有安全顾虑、不愿将 SuperFreezZ 注册为无障碍服务的用户」 | 点击 Yes（继续开启流程）或 No（结束引导、不使用无障碍）；本页 ISlidePolicy.isPolicyRespected() 恒为 false，滑动前进会被 onUserIllegallyRequestedNextPage() 拦下并 Toast 提示，但点击 No 可直接完成 | `AccessibilityServiceChooserFragment.onCreateView / isPolicyRespected / onUserIllegallyRequestedNextPage；res/layout/fragment_accessibility_service_chooser.xml` |
| 4 | 引导说明页 | AlertDialog（GeneralUIKt.showAccessibilityDialog 构造） | 点击 Yes → AccessibilityServiceChooserFragment$onCreateView$1.onClick → showAccessibilityDialog$default(context, null, null) | 原生Dialog | **原文**：SuperFreezZ needs the accessibility service in order to automate freezing.<br><br>Please select SuperFreezZ, then enable access.<br>**译注**：「SuperFreezZ 需要无障碍服务才能自动冻结应用。请在列表中选择 SuperFreezZ，然后开启访问权限。」 | 正向按钮（R$string 2131755066，即 enable/开启类文案）跳转系统无障碍设置；负向按钮 R$string.cancel（取消）关闭弹窗。setCancelable(false) 仅禁止点击外部/返回键取消，仍保留显式取消按钮 | `GeneralUIKt.showAccessibilityDialog；strings.xml: accessibility_service_dialog_message` |
| 5 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（由系统渲染，应用无自绘） | GeneralUIKt$showAccessibilityDialog$2.onClick 中 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))，随后注册 doOnResume 回调 | 系统无障碍页 | **原文**：无（系统页面，文案由 Android 系统与 accessibility_service_description 提供）<br>**译注**：系统无障碍服务列表中可见 SuperFreezZ 条目及其 description | 用户在系统页手动选中 SuperFreezZ 并开启；应用不做任何自动勾选、不叠遮罩、不模拟点击开关 | `GeneralUIKt$showAccessibilityDialog$2.onClick` |
| 6 | 拒权反馈循环 | IntroActivity / AccessibilityServiceChooserFragment | IntroActivity.onResume()：仅当 lastSlide && FreezerService.Companion.isEnabled() 为真时 done$…() 自动结束引导 | 原生Activity | 无 | 用户可再次点 Yes 重试，或点 No 结束引导进入手动模式 | `IntroActivity.onResume / done$superfreeze_tool_android_release` |
| 7 | 业务功能触发 | FreezeShortcutActivity（桌面快捷方式/桌面图标 "Freeze" 触发） | doNextFreezingStep()：FreezerService 未启用且 getPrefUseAccessibilityService() 为真 → promptForAccessibility()；否则弹 getPrefShowExplainingDialog 说明框 | 原生Dialog | **原文**：Freeze manually / I do not want to do this<br>**译注**：「是否自动化冻结应用？」说明框：正向 ok 继续自动化流程，负向「我不想这样做」转入手动逐应用冻结 | 选择自动化（复用无障碍说明弹窗）或手动模式（跳 APPLICATION_DETAILS_SETTINGS 由用户自己点 FORCE STOP） | `FreezeShortcutActivity.doNextFreezingStep / promptForAccessibility；strings.xml: freeze_manually / freeze_manually_no` |
| 8 | 获权后动作 | FreezerService（android:packageNames="com.android.settings" 限定的事件监听） | onAccessibilityEvent 监听 className == "com.android.settings.applications.InstalledAppDetailsTop"，再用 findAccessibilityNodeInfosByViewId("com.android.settings:id/force_stop_button") 点击 FORCE STOP、OK、Back | 系统无障碍页 | **原文**：无（后台执行，无界面）<br>**译注**：在用户发起的冻结流程中，代替用户点击系统应用详情页的强制停止与确认按钮，完成后返回；不做防撤权监听、不阻止用户关闭服务 | 无额外要求；用户可随时在系统设置中关闭该服务，设置页亦会主动提示关闭 | `FreezerService.onAccessibilityEvent / pressForceStopButton；res/xml/accessibility_service.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 引导说明页（原生 AppIntro Activity）：IntroActivity 的 5 张 slide，标题/正文来自 strings.xml（automate_the_freezing_of_apps 等）
- 选择页原生卡片布局：res/layout/fragment_accessibility_service_chooser.xml，Yes 卡片绑定 @string/yes + @string/accessibility_arguments_yes，No 卡片绑定 @string/no + @string/accessibility_arguments_no
- 原生 AlertDialog：GeneralUIKt.showAccessibilityDialog，标题 @string/accessibility_service，正文 @string/accessibility_service_dialog_message，正/负按钮为 R$string 2131755066 与 @string/cancel，图标 @mipmap/ic_launcher 对应资源 2131623936
- 系统无障碍服务列表项描述：res/xml/accessibility_service.xml 的 android:description=@string/accessibility_service_description（在系统设置页由 Android 展示）
- 业务触发说明框：FreezeShortcutActivity.doNextFreezingStep 的 AlertDialog（2131755073 标题 / 2131755009 正文 / @string/ok / 2131755074 = freeze_manually_no）
- 设置页提示：SettingsActivity$FreezingAppsPreferenceFragment 的 Toast「Please disable accessibility service for SuperFreezZ」及 accessibilityNo 相关偏好摘要
- 无 WebView、无 assets HTML、无悬浮窗 Overlay、无自绘高仿系统设置页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Turning this on lets you automatically freeze apps. <br> <br>Advantages: <br>• No user interaction: Faster. No need to know how to do it. <br>• Disabled users can use the freeze shortcut (via speech recognition, for example), freezing all apps automatically. <br> <br>SuperFreezZ uses the accessibility service when tapping "FORCE STOP", "OK", and "Back". Retrieval of window content finds these buttons, and observation of actions is needed to know when they appear. <br> <br>The accessibility service can also be used to lock the screen after freezing on newer Android versions. | 开启此项后即可自动冻结应用。优点：无需用户交互，更快，不必知道具体操作方式；行动不便的用户可通过语音识别等方式调用冻结快捷方式，自动冻结全部应用。SuperFreezZ 在点击「强制停止」「确定」和「返回」时使用无障碍服务；读取窗口内容用于找到这些按钮，观察操作则用于判断按钮何时出现。在较新的 Android 版本上，该无障碍服务还可用于在冻结后锁定屏幕。 | `res/values/strings.xml: accessibility_service_description（由 res/xml/accessibility_service.xml 的 android:description 引用）` | 良性透明说明 |
| en | SuperFreezZ needs the accessibility service in order to automate freezing.<br><br>Please select SuperFreezZ, then enable access. | SuperFreezZ 需要无障碍服务才能自动冻结应用。请在列表中选择 SuperFreezZ，然后开启访问权限。 | `res/values/strings.xml: accessibility_service_dialog_message（GeneralUIKt.showAccessibilityDialog 使用）` | 受限设置分步教学 |
| en | You will have to press "FORCE STOP", "OK" and "Back" manually to freeze an app. <br>For: <br>• Slow devices <br>• Security concerns <br>• No registration of SuperFreezZ as an accessibility service | 你将需要手动依次点击「强制停止」「确定」和「返回」来冻结应用。适用于：慢速设备、存在安全顾虑、不愿将 SuperFreezZ 注册为无障碍服务的用户。 | `res/values/strings.xml: accessibility_arguments_no（fragment_accessibility_service_chooser.xml 中 No 卡片）` | 良性透明说明 |
| en | For: <br>• Ease of use <br>• Freezing a lot of apps | 适用于：易用性、需要批量冻结大量应用。 | `res/values/strings.xml: accessibility_arguments_yes（fragment_accessibility_service_chooser.xml 中 Yes 卡片）` | 良性透明说明 |
| en | Accessibility Service | 无障碍服务 | `res/values/strings.xml: accessibility_service（弹窗标题）` | 良性透明说明 |
| en | Automate the freezing of apps? | 是否自动化冻结应用？ | `res/values/strings.xml: automate_the_freezing_of_apps` | 良性透明说明 |
| en | I do not want to do this | 我不想这样做 | `res/values/strings.xml: freeze_manually_no（FreezeShortcutActivity.doNextFreezingStep 负向按钮）` | 良性透明说明 |
| en | Please disable accessibility service for SuperFreezZ | 请关闭 SuperFreezZ 的无障碍服务 | `硬编码于 SettingsActivity$FreezingAppsPreferenceFragment$onCreate$1.onPreferenceClick` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无死循环。未授权返回后 IntroActivity.onResume 仅在 lastSlide 且 FreezerService.isEnabled() 为真时才自动结束，否则停留原页；用户点 No 卡片即 done()→finish() 结束引导。业务侧（FreezeShortcutActivity）拒绝后可转入手动逐应用冻结模式，不重复拉起。
- **遮罩叠层 / 高仿系统设置页**：无。跳转后为标准系统 ACTION_ACCESSIBILITY_SETTINGS 页，应用不叠任何半透明遮罩、全屏悬浮窗或自绘高仿无障碍开关页；无障碍服务配置中未申请 SYSTEM_ALERT_WINDOW。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。仅跳转 android.settings.ACCESSIBILITY_SETTINGS 与 android.settings.USAGE_ACCESS_SETTINGS（后者带 package:superfreeze.tool.android 定向），未教用户进应用详情点右上角菜单允许受限设置，也无 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。FreezerService 的 packageNames 限定为 com.android.settings，onAccessibilityEvent 仅处理 InstalledAppDetailsTop 以完成用户发起的冻结；PERFORM_GLOBAL_ACTION 用于执行 Back 收尾，不是监听设置页阻止撤权。设置页反而提示用户「请关闭 SuperFreezZ 的无障碍服务」。
- **良性降级 / 替代方案**：有。选择页 No 卡片如实列出不注册无障碍的后果；FreezeShortcutActivity.doNextFreezingStep 在未授权时弹说明框，负向「I do not want to do this」转入 freeze_manually 手动模式，由 Companion.freezeApp 跳 APPLICATION_DETAILS_SETTINGS 让用户自行点击 FORCE STOP/OK/Back。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后 IntroActivity（AppIntro）最后一页 AccessibilityServiceChooserFragment 出现时即可开始抓取；核心窗口切换点是监测到 Activity 跳转为 android.settings.ACCESSIBILITY_SETTINGS（对应 GeneralUIKt$showAccessibilityDialog$2.onClick）以及返回后的 IntroActivity.onResume。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。全部引导文案位于 res/values/strings.xml 与本地 layout，UTG 文本可直接提取；无图空文本页面、无 WebView、无远端下发、无加壳或密文载荷。唯一需注意的温和外壳是：引导以 AppIntro 多页形式呈现，若只抓首屏会漏掉最后的 Yes/No 选择页，应以 IntroActivity 全部 slide 遍历或按 accessibilityYes/accessibilityNo 控件出现为准。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导分页页（AppIntro 最后一页 Yes/No 选择页）** | Activity 为 superfreeze.tool.android.userInterface.intro.IntroActivity，含 accessibilityYes / accessibilityNo 两个可点击卡片及标题 Accessibility Service | 这是全流程唯一呈现「是否将本应用注册为无障碍服务」及其利弊的位置，能直接判断是否存在诱骗性话术与是否给出对等拒绝选项 | 页面同时存在 Yes 与 No 两个可点击卡片（拒绝路径对等可见）；No 卡片文本含 FORCE STOP / OK / Back 与 Security concerns 等如实风险描述；无 SKIP 按钮但存在最终 DONE 与 BACK |
| **跳转前说明弹窗页** | AlertDialog 标题 Accessibility Service、正文含 Please select SuperFreezZ, then enable access.，含正向（enable）与 cancel 两个按钮 | 确认引导弹窗是否可取消、文案是否明示需用户自行在系统页选择本应用，从而区分「告知式引导」与「强制无取消」 | 弹窗存在 cancel 负向按钮；弹窗正文明确指向系统设置中的 SuperFreezZ 条目；点击外部/返回不可关闭（setCancelable(false)） |
| **系统无障碍服务列表项** | android.settings.ACCESSIBILITY_SETTINGS 页面内 SuperFreezZ 条目及其描述文本 | 核对系统列表展示的服务名与 description 是否与应用真实身份一致、是否存在名称伪装或空白挤出警告文案 | 列表项名称与 app_name=SuperFreezZ 一致；描述文本与 accessibility_service_description 原文一致；开关状态初始为关闭，需用户手动打开 |
| **返回后状态页（拒权反馈）** | 返回后仍停留在 IntroActivity 的 AccessibilityServiceChooserFragment 或已 finish 回到 MainActivity 应用列表 | 验证是否存在 onResume 死循环重跳或定时器反复拉起系统设置页 | 返回后窗口未再次切至 ACCESSIBILITY_SETTINGS；未出现新的 Toast 惩罚提示；授权成功后自动 finish 回到主列表 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `superfreeze.tool.android.userInterface.intro.AccessibilityServiceChooserFragment#onCreateView`
- `superfreeze.tool.android.userInterface.GeneralUIKt#showAccessibilityDialog`
- `superfreeze.tool.android.userInterface.GeneralUIKt$showAccessibilityDialog$2#onClick`
- `superfreeze.tool.android.userInterface.intro.IntroActivity#onCreate`
- `superfreeze.tool.android.userInterface.FreezeShortcutActivity#doNextFreezingStep`
- `res/xml/accessibility_service.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 页面流转视角）

**判定：良性透明引导，未发现诱导/欺诈要素。** 无障碍授权引导全程为原生 AppIntro 引导页 + 不可取消说明弹窗 + 标准 `ACTION_ACCESSIBILITY_SETTINGS` 跳转，无 WebView、无悬浮窗遮罩、无高仿系统页、无拒权死循环、无受限设置（13+）教学、无假 `isAccessibilityTool`。

**逐级引导链（代码已核实）**

1. **冷启动入口**：[MainActivity.onResume()](<resource-unit:#1.dex1 code:superfreeze.tool.android.userInterface.mainActivity.MainActivity#onResume>) 判断 `DatabaseKt.getPrefIntroAlreadyShown()` 为真时 `startActivity(IntroActivity)`，首启进入引导。
2. **引导说明页**：[IntroActivity.onCreate()](<resource-unit:#1.dex1 code:superfreeze.tool.android.userInterface.intro.IntroActivity#onCreate>) 用 AppIntro 组装 5 张 slide：`WelcomeFragment` → 2 张 `AppIntroFragment` → `IntroModesFragment` → [AccessibilityServiceChooserFragment](<resource-unit:#1.dex1 code:superfreeze.tool.android.userInterface.intro.AccessibilityServiceChooserFragment>)，并 `showSkipButton(false)`。若 Intent action 为 `superfreeze.tool.androidSHOW_ACCESSIBILITY_SERVICE_CHOOSER`（从设置页进入）则只挂载选择页一张 slide。
3. **不可跳过的选择页**：`AccessibilityServiceChooserFragment` 实现 `ISlidePolicy.isPolicyRespected()` 恒返回 `false`，滑动前进被 `onUserIllegallyRequestedNextPage()` 拦下并弹 Toast；但页面本身提供 **Yes / No 两个对等入口**（[fragment_accessibility_service_chooser.xml](<resource-unit:#1 file:res/layout/fragment_accessibility_service_chooser.xml#L11-L18>)，Yes 列 `accessibility_arguments_yes` 优点、No 列 `accessibility_arguments_no` 缺点并明确写出「不注册无障碍服务」的后果）。点 No 走 `done()` → `IntroActivity.done$…()` → `finish()`，**存在显式拒绝/降级路径**。
4. **说明弹窗**：[GeneralUIKt.showAccessibilityDialog()](<resource-unit:#1.dex1 code:superfreeze.tool.android.userInterface.GeneralUIKt#showAccessibilityDialog>) 构造 `AlertDialog`，`setCancelable(false)` 但**带 cancel 负向按钮**；标题 `accessibility_service`（"Accessibility Service"）、正文 `accessibility_service_dialog_message`。
5. **跳系统无障碍页**：[GeneralUIKt$showAccessibilityDialog$2.onClick()](<resource-unit:#1.dex1 code:superfreeze.tool.android.userInterface.GeneralUIKt$showAccessibilityDialog$2#onClick>) 执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，无包名定向、无伪造页面，纯系统页。
6. **返回后反馈（非死循环）**：[IntroActivity.onResume()](<resource-unit:#1.dex1 code:superfreeze.tool.android.userInterface.intro.IntroActivity#onResume>) 仅在 `lastSlide && FreezerService.isEnabled()` 时自动 `done()`；未授权则**停留原页，不重跳**。
7. **业务触发路径**：[FreezeShortcutActivity.doNextFreezingStep()](<resource-unit:#1.dex1 code:superfreeze.tool.android.userInterface.FreezeShortcutActivity#doNextFreezingStep>) 在服务未启用且用户已开启「使用无障碍」偏好时调用 `promptForAccessibility()` 复用同一弹窗；否则弹「是否自动化冻结」说明框，负向按钮文案为 `freeze_manually_no` = *"I do not want to do this"*，转入手动模式（`FreezeShortcutActivity$Companion#freezeApp` 跳 `APPLICATION_DETAILS_SETTINGS` 由用户手点）。
8. **设置页入口**：[SettingsActivity$FreezingAppsPreferenceFragment$onCreate$1.onPreferenceClick()](<resource-unit:#1.dex1 code:superfreeze.tool.android.userInterface.settingsActivity.SettingsActivity$FreezingAppsPreferenceFragment$onCreate$1#onPreferenceClick>) 服务已启用时提示 "Please disable accessibility service for SuperFreezZ" 并跳设置页（**鼓励关闭**而非阻止撤权）。

**权限声明诚实性**：[accessibility_service.xml](<resource-unit:#1 file:res/xml/accessibility_service.xml#L2>) 将事件范围限定 `packageNames="com.android.settings"`、`typeWindowStateChanged`、`canRetrieveWindowContent="true"`，与 `android:description` 中「仅在点击 FORCE STOP / OK / Back 时使用，读取窗口内容以找到这些按钮」的描述完全一致；无 `canPerformGestures` 以外的越权配置。`PERFORM_GLOBAL_ACTION` 用于在设置页执行 Back 完成冻结流程，属功能必需，非防撤权。无 `isAccessibilityTool` 伪造、无空白/同形字伪装、无多 activity-alias。

**UTG 视角盲区**：无。全部引导文案均在 `res/values/strings.xml` 与本地 layout 中静态可见，不依赖 OCR 或远端下发。

**未写入风险台账**：本次未发现可独立成立的恶意/违规命题（应用为开源 SuperFreezZ，引导文案与 `android:description` 一致，且提供显式拒绝与手动降级模式），故不登记 `record_risk`。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导文案与跳转逻辑均静态可见：res/values/strings.xml（accessibility_service、accessibility_service_description、accessibility_service_dialog_message、accessibility_arguments_yes/no）、res/layout/fragment_accessibility_service_chooser.xml、res/xml/accessibility_service.xml，以及 classes.dex 中 IntroActivity/AccessibilityServiceChooserFragment/GeneralUIKt 的完整实现。无加壳、无密文载荷、无远端 HTML、无 WebView。",
  "summary_one_liner": "SuperFreezZ 在 AppIntro 引导流程最后一页用 Yes/No 对等卡片说明无障碍服务的优缺点与作用范围，用户选 Yes 后弹出带取消按钮的说明弹窗，再跳转标准系统 ACTION_ACCESSIBILITY_SETTINGS 页，由用户自行开启，未授权则停留原页并提供手动冻结降级模式。",
  "disguise_identity": {
    "app_display_name": "SuperFreezZ",
    "claimed_brand_or_persona": "SuperFreezZ（开源系统清理/省电冻结工具，F-Droid 分发）",
    "a11y_service_label": "SuperFreezZ（无障碍列表项由 android:label=@string/app_name 提供，description 为 accessibility_service_description）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。无空白/换行挤出警告文案、无同形字、无多 activity-alias、未伪造 isAccessibilityTool。仅 IntroActivity 支持额外 action superfreeze.tool.androidSHOW_ACCESSIBILITY_SERVICE_CHOOSER 以便从设置页直达选择页，属常规内部导航。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "superfreeze.tool.android.userInterface.mainActivity.MainActivity",
      "trigger_event": "onResume() 中 DatabaseKt.getPrefIntroAlreadyShown() 为真时 startActivity(IntroActivity)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅跳转，无文案）",
      "shown_text_zh": "首次启动直接进入引导流程页，不展示额外弹窗",
      "user_action_requested": "无，自动跳转",
      "code_anchor": "MainActivity.onResume"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "superfreeze.tool.android.userInterface.intro.IntroActivity（AppIntro，含 WelcomeFragment / 2×AppIntroFragment / IntroModesFragment / AccessibilityServiceChooserFragment）",
      "trigger_event": "IntroActivity.onCreate() 中 addSlide(...)，并 showSkipButton(false) 隐藏跳过按钮",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility Service / Automate the freezing of apps?",
      "shown_text_zh": "「无障碍服务」「是否自动化冻结应用？」等分页标题与说明",
      "user_action_requested": "逐页 NEXT（隐藏了 SKIP，但页面底部提供 BACK 与最终 DONE）；文案键 app_intro_skip_button 存在但被 showSkipButton(false) 关闭",
      "code_anchor": "IntroActivity.onCreate；strings.xml: accessibility_service / automate_the_freezing_of_apps"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "AccessibilityServiceChooserFragment（fragment_accessibility_service_chooser.xml，Yes/No 对等卡片）",
      "trigger_event": "onCreateView() 为 R$id.accessibilityYes / R$id.accessibilityNo 分别 setOnClickListener",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "For: • Ease of use • Freezing a lot of apps / You will have to press \"FORCE STOP\", \"OK\" and \"Back\" manually to freeze an app. For: • Slow devices • Security concerns • No registration of SuperFreezZ as an accessibility service",
      "shown_text_zh": "Yes 卡片列出「易用、可批量冻结大量应用」；No 卡片如实列出「需手动依次点击 FORCE STOP/OK/Back，适用于慢设备、有安全顾虑、不愿将 SuperFreezZ 注册为无障碍服务的用户」",
      "user_action_requested": "点击 Yes（继续开启流程）或 No（结束引导、不使用无障碍）；本页 ISlidePolicy.isPolicyRespected() 恒为 false，滑动前进会被 onUserIllegallyRequestedNextPage() 拦下并 Toast 提示，但点击 No 可直接完成",
      "code_anchor": "AccessibilityServiceChooserFragment.onCreateView / isPolicyRespected / onUserIllegallyRequestedNextPage；res/layout/fragment_accessibility_service_chooser.xml"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "AlertDialog（GeneralUIKt.showAccessibilityDialog 构造）",
      "trigger_event": "点击 Yes → AccessibilityServiceChooserFragment$onCreateView$1.onClick → showAccessibilityDialog$default(context, null, null)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "SuperFreezZ needs the accessibility service in order to automate freezing.\n\nPlease select SuperFreezZ, then enable access.",
      "shown_text_zh": "「SuperFreezZ 需要无障碍服务才能自动冻结应用。请在列表中选择 SuperFreezZ，然后开启访问权限。」",
      "user_action_requested": "正向按钮（R$string 2131755066，即 enable/开启类文案）跳转系统无障碍设置；负向按钮 R$string.cancel（取消）关闭弹窗。setCancelable(false) 仅禁止点击外部/返回键取消，仍保留显式取消按钮",
      "code_anchor": "GeneralUIKt.showAccessibilityDialog；strings.xml: accessibility_service_dialog_message"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（由系统渲染，应用无自绘）",
      "trigger_event": "GeneralUIKt$showAccessibilityDialog$2.onClick 中 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))，随后注册 doOnResume 回调",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页面，文案由 Android 系统与 accessibility_service_description 提供）",
      "shown_text_zh": "系统无障碍服务列表中可见 SuperFreezZ 条目及其 description",
      "user_action_requested": "用户在系统页手动选中 SuperFreezZ 并开启；应用不做任何自动勾选、不叠遮罩、不模拟点击开关",
      "code_anchor": "GeneralUIKt$showAccessibilityDialog$2.onClick"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "IntroActivity / AccessibilityServiceChooserFragment",
      "trigger_event": "IntroActivity.onResume()：仅当 lastSlide && FreezerService.Companion.isEnabled() 为真时 done$…() 自动结束引导",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "未开启无障碍则停留原页，无 Toast 惩罚、无定时器重跳、无 onResume 死循环",
      "user_action_requested": "用户可再次点 Yes 重试，或点 No 结束引导进入手动模式",
      "code_anchor": "IntroActivity.onResume / done$superfreeze_tool_android_release"
    },
    {
      "step": 7,
      "stage": "业务功能触发",
      "screen_or_component": "FreezeShortcutActivity（桌面快捷方式/桌面图标 \"Freeze\" 触发）",
      "trigger_event": "doNextFreezingStep()：FreezerService 未启用且 getPrefUseAccessibilityService() 为真 → promptForAccessibility()；否则弹 getPrefShowExplainingDialog 说明框",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Freeze manually / I do not want to do this",
      "shown_text_zh": "「是否自动化冻结应用？」说明框：正向 ok 继续自动化流程，负向「我不想这样做」转入手动逐应用冻结",
      "user_action_requested": "选择自动化（复用无障碍说明弹窗）或手动模式（跳 APPLICATION_DETAILS_SETTINGS 由用户自己点 FORCE STOP）",
      "code_anchor": "FreezeShortcutActivity.doNextFreezingStep / promptForAccessibility；strings.xml: freeze_manually / freeze_manually_no"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "FreezerService（android:packageNames=\"com.android.settings\" 限定的事件监听）",
      "trigger_event": "onAccessibilityEvent 监听 className == \"com.android.settings.applications.InstalledAppDetailsTop\"，再用 findAccessibilityNodeInfosByViewId(\"com.android.settings:id/force_stop_button\") 点击 FORCE STOP、OK、Back",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（后台执行，无界面）",
      "shown_text_zh": "在用户发起的冻结流程中，代替用户点击系统应用详情页的强制停止与确认按钮，完成后返回；不做防撤权监听、不阻止用户关闭服务",
      "user_action_requested": "无额外要求；用户可随时在系统设置中关闭该服务，设置页亦会主动提示关闭",
      "code_anchor": "FreezerService.onAccessibilityEvent / pressForceStopButton；res/xml/accessibility_service.xml"
    }
  ],
  "text_presentation_locations": [
    "引导说明页（原生 AppIntro Activity）：IntroActivity 的 5 张 slide，标题/正文来自 strings.xml（automate_the_freezing_of_apps 等）",
    "选择页原生卡片布局：res/layout/fragment_accessibility_service_chooser.xml，Yes 卡片绑定 @string/yes + @string/accessibility_arguments_yes，No 卡片绑定 @string/no + @string/accessibility_arguments_no",
    "原生 AlertDialog：GeneralUIKt.showAccessibilityDialog，标题 @string/accessibility_service，正文 @string/accessibility_service_dialog_message，正/负按钮为 R$string 2131755066 与 @string/cancel，图标 @mipmap/ic_launcher 对应资源 2131623936",
    "系统无障碍服务列表项描述：res/xml/accessibility_service.xml 的 android:description=@string/accessibility_service_description（在系统设置页由 Android 展示）",
    "业务触发说明框：FreezeShortcutActivity.doNextFreezingStep 的 AlertDialog（2131755073 标题 / 2131755009 正文 / @string/ok / 2131755074 = freeze_manually_no）",
    "设置页提示：SettingsActivity$FreezingAppsPreferenceFragment 的 Toast「Please disable accessibility service for SuperFreezZ」及 accessibilityNo 相关偏好摘要",
    "无 WebView、无 assets HTML、无悬浮窗 Overlay、无自绘高仿系统设置页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Turning this on lets you automatically freeze apps. \n \nAdvantages: \n• No user interaction: Faster. No need to know how to do it. \n• Disabled users can use the freeze shortcut (via speech recognition, for example), freezing all apps automatically. \n \nSuperFreezZ uses the accessibility service when tapping \"FORCE STOP\", \"OK\", and \"Back\". Retrieval of window content finds these buttons, and observation of actions is needed to know when they appear. \n \nThe accessibility service can also be used to lock the screen after freezing on newer Android versions.",
      "text_zh": "开启此项后即可自动冻结应用。优点：无需用户交互，更快，不必知道具体操作方式；行动不便的用户可通过语音识别等方式调用冻结快捷方式，自动冻结全部应用。SuperFreezZ 在点击「强制停止」「确定」和「返回」时使用无障碍服务；读取窗口内容用于找到这些按钮，观察操作则用于判断按钮何时出现。在较新的 Android 版本上，该无障碍服务还可用于在冻结后锁定屏幕。",
      "source_location": "res/values/strings.xml: accessibility_service_description（由 res/xml/accessibility_service.xml 的 android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "SuperFreezZ needs the accessibility service in order to automate freezing.\n\nPlease select SuperFreezZ, then enable access.",
      "text_zh": "SuperFreezZ 需要无障碍服务才能自动冻结应用。请在列表中选择 SuperFreezZ，然后开启访问权限。",
      "source_location": "res/values/strings.xml: accessibility_service_dialog_message（GeneralUIKt.showAccessibilityDialog 使用）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "You will have to press \"FORCE STOP\", \"OK\" and \"Back\" manually to freeze an app. \nFor: \n• Slow devices \n• Security concerns \n• No registration of SuperFreezZ as an accessibility service",
      "text_zh": "你将需要手动依次点击「强制停止」「确定」和「返回」来冻结应用。适用于：慢速设备、存在安全顾虑、不愿将 SuperFreezZ 注册为无障碍服务的用户。",
      "source_location": "res/values/strings.xml: accessibility_arguments_no（fragment_accessibility_service_chooser.xml 中 No 卡片）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "For: \n• Ease of use \n• Freezing a lot of apps",
      "text_zh": "适用于：易用性、需要批量冻结大量应用。",
      "source_location": "res/values/strings.xml: accessibility_arguments_yes（fragment_accessibility_service_chooser.xml 中 Yes 卡片）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service",
      "text_zh": "无障碍服务",
      "source_location": "res/values/strings.xml: accessibility_service（弹窗标题）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Automate the freezing of apps?",
      "text_zh": "是否自动化冻结应用？",
      "source_location": "res/values/strings.xml: automate_the_freezing_of_apps",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "I do not want to do this",
      "text_zh": "我不想这样做",
      "source_location": "res/values/strings.xml: freeze_manually_no（FreezeShortcutActivity.doNextFreezingStep 负向按钮）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Please disable accessibility service for SuperFreezZ",
      "text_zh": "请关闭 SuperFreezZ 的无障碍服务",
      "source_location": "硬编码于 SettingsActivity$FreezingAppsPreferenceFragment$onCreate$1.onPreferenceClick",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无死循环。未授权返回后 IntroActivity.onResume 仅在 lastSlide 且 FreezerService.isEnabled() 为真时才自动结束，否则停留原页；用户点 No 卡片即 done()→finish() 结束引导。业务侧（FreezeShortcutActivity）拒绝后可转入手动逐应用冻结模式，不重复拉起。",
    "overlay_or_fake_settings": "无。跳转后为标准系统 ACTION_ACCESSIBILITY_SETTINGS 页，应用不叠任何半透明遮罩、全屏悬浮窗或自绘高仿无障碍开关页；无障碍服务配置中未申请 SYSTEM_ALERT_WINDOW。",
    "restricted_settings_13plus_coaching": "无。仅跳转 android.settings.ACCESSIBILITY_SETTINGS 与 android.settings.USAGE_ACCESS_SETTINGS（后者带 package:superfreeze.tool.android 定向），未教用户进应用详情点右上角菜单允许受限设置，也无 Session 安装器绕过。",
    "post_grant_anti_removal": "无。FreezerService 的 packageNames 限定为 com.android.settings，onAccessibilityEvent 仅处理 InstalledAppDetailsTop 以完成用户发起的冻结；PERFORM_GLOBAL_ACTION 用于执行 Back 收尾，不是监听设置页阻止撤权。设置页反而提示用户「请关闭 SuperFreezZ 的无障碍服务」。",
    "benign_graceful_degradation": "有。选择页 No 卡片如实列出不注册无障碍的后果；FreezeShortcutActivity.doNextFreezingStep 在未授权时弹说明框，负向「I do not want to do this」转入 freeze_manually 手动模式，由 Companion.freezeApp 跳 APPLICATION_DETAILS_SETTINGS 让用户自行点击 FORCE STOP/OK/Back。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后 IntroActivity（AppIntro）最后一页 AccessibilityServiceChooserFragment 出现时即可开始抓取；核心窗口切换点是监测到 Activity 跳转为 android.settings.ACCESSIBILITY_SETTINGS（对应 GeneralUIKt$showAccessibilityDialog$2.onClick）以及返回后的 IntroActivity.onResume。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导分页页（AppIntro 最后一页 Yes/No 选择页）",
        "page_identifier": "Activity 为 superfreeze.tool.android.userInterface.intro.IntroActivity，含 accessibilityYes / accessibilityNo 两个可点击卡片及标题 Accessibility Service",
        "why_most_useful": "这是全流程唯一呈现「是否将本应用注册为无障碍服务」及其利弊的位置，能直接判断是否存在诱骗性话术与是否给出对等拒绝选项",
        "observable_utg_signals": ["页面同时存在 Yes 与 No 两个可点击卡片（拒绝路径对等可见）", "No 卡片文本含 FORCE STOP / OK / Back 与 Security concerns 等如实风险描述", "无 SKIP 按钮但存在最终 DONE 与 BACK"]
      },
      {
        "page_role": "跳转前说明弹窗页",
        "page_identifier": "AlertDialog 标题 Accessibility Service、正文含 Please select SuperFreezZ, then enable access.，含正向（enable）与 cancel 两个按钮",
        "why_most_useful": "确认引导弹窗是否可取消、文案是否明示需用户自行在系统页选择本应用，从而区分「告知式引导」与「强制无取消」",
        "observable_utg_signals": ["弹窗存在 cancel 负向按钮", "弹窗正文明确指向系统设置中的 SuperFreezZ 条目", "点击外部/返回不可关闭（setCancelable(false)）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 页面内 SuperFreezZ 条目及其描述文本",
        "why_most_useful": "核对系统列表展示的服务名与 description 是否与应用真实身份一致、是否存在名称伪装或空白挤出警告文案",
        "observable_utg_signals": ["列表项名称与 app_name=SuperFreezZ 一致", "描述文本与 accessibility_service_description 原文一致", "开关状态初始为关闭，需用户手动打开"]
      },
      {
        "page_role": "返回后状态页（拒权反馈）",
        "page_identifier": "返回后仍停留在 IntroActivity 的 AccessibilityServiceChooserFragment 或已 finish 回到 MainActivity 应用列表",
        "why_most_useful": "验证是否存在 onResume 死循环重跳或定时器反复拉起系统设置页",
        "observable_utg_signals": ["返回后窗口未再次切至 ACCESSIBILITY_SETTINGS", "未出现新的 Toast 惩罚提示", "授权成功后自动 finish 回到主列表"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。全部引导文案位于 res/values/strings.xml 与本地 layout，UTG 文本可直接提取；无图空文本页面、无 WebView、无远端下发、无加壳或密文载荷。唯一需注意的温和外壳是：引导以 AppIntro 多页形式呈现，若只抓首屏会漏掉最后的 Yes/No 选择页，应以 IntroActivity 全部 slide 遍历或按 accessibilityYes/accessibilityNo 控件出现为准。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "superfreeze.tool.android.userInterface.intro.AccessibilityServiceChooserFragment#onCreateView",
    "superfreeze.tool.android.userInterface.GeneralUIKt#showAccessibilityDialog",
    "superfreeze.tool.android.userInterface.GeneralUIKt$showAccessibilityDialog$2#onClick",
    "superfreeze.tool.android.userInterface.intro.IntroActivity#onCreate",
    "superfreeze.tool.android.userInterface.FreezeShortcutActivity#doNextFreezingStep",
    "res/xml/accessibility_service.xml"
  ]
}
```

</details>
