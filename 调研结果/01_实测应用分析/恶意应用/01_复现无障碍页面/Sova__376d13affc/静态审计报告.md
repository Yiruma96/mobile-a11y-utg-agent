# MB_122__376d13affc｜Sova — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：193.0s

## 1. 一句话核心结论

- **核心申请方式**：以本地 HTML 逐屏复刻系统无障碍设置页与授权弹窗、并用动画假光标指引点击，把开启无障碍包装成'观看教学'，最后一步才跳真实系统设置页。
- **静态可见性说明**：引导流程的 HTML、文案、布局与无障碍配置均完整静态可见；但承载这些页面的 Activity/Service 实现类（com.tapston.burgerking.*）在 classes.dex 与 classes2.dex 中零命中，由 Application.attachBaseContext 的解密加载链（basketacquire/dreamfatal/garlicbrick）在运行期提供，assets/nx.json（2.29MB，高熵）为加密资产。故 WebView 装载方式、服务名占位符替换、Android.finishInject 的跳转 intent 以及 onResume 拒权重跳逻辑均未静态还原。另 assets/chrome.html（452KB 高仿 Chrome 界面）未展开分析。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `376d13affcbfc5d5358d39aba16b814f711f2e81632059a4bce5af060e038ea4` |
| 包名 / 年份 | `com.help.marine` / 2023 |
| 家族 / 品类 | **Sova**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Google Chrome / Android 系统无障碍设置（伪造系统 UI 与 Google 图标） |
| 系统无障碍列表服务名 | Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面名与无障碍服务标签统一伪装为 'Chrome'；无障碍描述复用开源 Accessibility Insights 文案（accessibility_insights_service_description 与 accessibility_service_description 双份）；服务名在页面中以 AC_NAME_HERE 占位符运行期注入，避免静态检索；类名全量无意义字母拼接（如 PQfIxWiKgUiYcNiXeCtIqLnOj）；Manifest 声明组件类不在 DEX 内，由 Application 解密加载；chrome.html 直接复刻 Chrome 品牌界面 |
| 无障碍服务类名 | `com.tapston.burgerking.service.AppAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Service allows Accessibility for Android to scan your device for accessibility issues. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tapston.burgerking.ui.LauncherActivity（LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents） | 用户点击桌面 'Chrome' 图标（ACTION_MAIN / LAUNCHER），onCreate 后立即转场 | 原生Activity | **原文**：无（透明全屏 Activity，无可见文案）<br>**译注**：透明中转页，用户看不到任何内容即被跳转 | 仅点击桌面图标，无选择权 | `AndroidManifest.xml: com.tapston.burgerking.ui.LauncherActivity（实现类不在 DEX，属解密加载）` |
| 2 | 引导说明页 | com.tapston.burgerking.ui.BrowserActivity / AccessibilityGuideActivity 内 WebView 加载 file:///android_asset/unique.html 的 step0 屏 | WebView 加载 unique.html 后 DOMContentLoaded，将 loader0 隐藏、loader1 显示（第 579-589 行） | 本地HTML WebView | **原文**：To work correctly, your application requires Accessibility rights. See how to make them. / View training<br>**译注**：为了让应用正常工作，你的应用需要无障碍权限。看看如何开启。/ 查看教学 | 点击绿色按钮 'View training'（实际点击只是把 ticker 置为 7 启动动画，无取消/跳过按钮） | `assets/unique.html#L92-L104（#loader1 与 onclick="javascript: ticker=7;"）` |
| 3 | 遮罩叠层指引（伪造系统无障碍列表） | unique.html step1 屏：伪造 'Special abilities' 页 + 'Installed services' 列表项（#click1） | setInterval 每秒递减 ticker，ticker==7 时 step0 隐藏、step1 显示（第 532-539 行） | 本地HTML WebView | **原文**：Special abilities / Installed services / AC_NAME_HERE / Turned off / Reading the screen / Volume buttons / Speech synthesis<br>**译注**：伪造系统无障碍设置页：已安装的服务列表中显示本应用服务名，状态写为'已关闭' | 观看假光标指向 'Turned off' 服务项并'点击'（页面 4 秒后自动切屏，用户无需也无法操作） | `assets/unique.html#L107-L178；假光标定位 unique.html#L487-L491（#click1）` |
| 4 | 遮罩叠层指引（伪造服务详情与开关） | unique.html step2 屏：伪造服务详情页与 'Use the service' 开关（#click2） | ticker==4 时切至 step2（第 541-546 行） | 本地HTML WebView | **原文**：Use the service / AC_NAME_HERE<br>**译注**：伪造服务详情页，展示'使用该服务'开关，演示将其打开 | 观看假光标指向伪造开关并拨动 | `assets/unique.html#L332-L384；假光标定位 unique.html#L492-L496（#click2）` |
| 5 | 遮罩叠层指引（伪造系统授权弹窗） | unique.html step3 屏：Semantic UI modal 伪造系统无障碍授权确认框（#click3） | ticker==2 时切至 step3 并执行 $('.ui.modal').modal('show')（第 548-558 行） | 本地HTML WebView | **原文**：Allow functions "AC_NAME_HERE" full phone control / Viewing Information and Controlling Screen Operation / The app can read all the content on the screen and display the content on top of other apps. / Viewing Information and performing actions / An app can track interactions with apps or hardware sensors and interact with apps on your behalf. / Allow / Reject<br>**译注**：伪造系统弹窗：'允许"Chrome"完全控制手机'，列出可读取屏幕全部内容、可代表用户操作其他应用等权限说明，并提供'允许'/'拒绝' | 演示点击 'Allow'；'Reject' 仅为静态文本，点击无任何行为，不构成真实拒绝路径 | `assets/unique.html#L387-L438；假光标定位 unique.html#L497-L501（#click3）` |
| 6 | 跳无障碍设置 / 获权后动作 | unique.html step4 屏 → 系统无障碍设置页（真实跳转目标由解密载荷决定） | ticker==0 时隐藏 modal、显示 step4（第 560-570 行）；用户点击 'Give rights' 触发 onclick="Android.finishInject();" | 本地HTML WebView + 系统无障碍页 | **原文**：How you can grant rights to the application! / Repeat training / Give rights<br>**译注**：如何授予应用权限！/ 重复教学 / 授予权限 | 点击 'Give rights' 后被送出应用进入真实系统无障碍设置；另有 'Repeat training' 可无限循环重放整段教学 | `assets/unique.html#L441-L452；restart() 见 unique.html#L575-L577；跳转实现 Android.finishInject 位于解密加载载荷（DEX 内无该方法名）` |
| 7 | 拒权反馈循环 | 原生兜底引导页（guide_layout.xml：str1 / str2）与 strings 中的无障碍引导文案 | 疑似服务/Activity 检测无障碍未启用时拉起；具体判定点位于 com.tapston.burgerking.* 解密载荷，未能静态还原 | 原生Activity | **原文**：Update app accesses / Enable access for "Chrome " / 1. Open the Accessibility settings / 2. Select Enable Accessibility Service / Accessibility service must be enabled to protect your data!<br>**译注**：更新应用访问权限 / 为"Chrome"启用访问 / 1. 打开无障碍设置 2. 选择启用无障碍服务 / 必须启用无障碍服务才能保护你的数据！ | 按步骤前往系统设置开启；无跳过/稍后按钮 | `res/layout/guide_layout.xml（str1/str2）；res/values/strings.xml（enable_accessibility_title、enable_accessibility_message、str1、str2、str4）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets/unique.html step0 屏（#loader1）：'To work correctly, your application requires Accessibility rights. See how to make them.' + 'View training' 按钮 —— 本地 HTML WebView 首屏
- assets/unique.html step1 屏：伪造系统页标题 'Special abilities'、分组 'Installed services'、服务名占位 'AC_NAME_HERE'、状态 'Turned off' —— 高仿系统无障碍列表
- assets/unique.html step2 屏：'Use the service' 开关行与 'AC_NAME_HERE' 服务名 —— 高仿服务详情页
- assets/unique.html step3 屏（Semantic UI modal）：'Allow functions "AC_NAME_HERE" full phone control' 及两条权限说明、'Allow'/'Reject' —— 高仿系统授权弹窗
- assets/unique.html step4 屏：'How you can grant rights to the application!'、'Repeat training'、'Give rights' —— 跳设置前的收口页
- res/layout/guide_layout.xml + res/values/strings.xml：原生引导页 TextView（str1/str2）与 enable_accessibility_title/message
- 系统无障碍列表项：android:label 引用 @string/app_name（Chrome），android:description 引用 @string/accessibility_service_description（'Service allows Accessibility for Android to scan your device for accessibility issues.'），见 res/xml/accessibilityservice.xml
- strings.xml 中另有恐吓式文案 'Accessibility service must be enabled to protect your data!'（str4）与 'Update app accesses'（enable_accessibility_title），用于原生引导/推送页（access_push.xml 引用 str4）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To work correctly, your application requires Accessibility rights. See how to make them. | 为了让应用正常工作，你的应用需要无障碍权限。看看如何开启。 | `assets/unique.html#L97（#loader1）` | 受限设置分步教学 |
| en | View training | 查看教学 | `assets/unique.html#L101` | 受限设置分步教学 |
| en | Installed services / AC_NAME_HERE / Turned off | 已安装的服务 / （本应用服务名） / 已关闭 | `assets/unique.html#L152-L178（step1 伪造系统列表）` | 受限设置分步教学 |
| en | Use the service | 使用该服务 | `assets/unique.html#L351（step2 伪造开关行）` | 受限设置分步教学 |
| en | Allow functions "AC_NAME_HERE" full phone control | 允许"（本应用服务名）"完全控制手机 | `assets/unique.html#L393-L394（step3 伪造系统授权弹窗）` | 受限设置分步教学 |
| en | The app can read all the content on the screen and display the content on top of other apps. | 该应用可以读取屏幕上的全部内容，并将内容显示在其他应用之上。 | `assets/unique.html#L407-L409` | 受限设置分步教学 |
| en | How you can grant rights to the application! | 如何给应用授予权限！ | `assets/unique.html#L445（step4）` | 受限设置分步教学 |
| en | Repeat training | 重复教学 | `assets/unique.html#L448` | 受限设置分步教学 |
| en | Give rights | 授予权限 | `assets/unique.html#L449（onclick=Android.finishInject()）` | 受限设置分步教学 |
| en | Service allows Accessibility for Android to scan your device for accessibility issues. | 该服务允许 Android 的无障碍功能扫描你的设备是否存在无障碍问题。 | `res/values/strings.xml: accessibility_service_description（经 res/xml/accessibilityservice.xml 的 android:description 引用）` | 隐私承诺 |
| en | Service allows Accessibility Insights for Android to scan your device for accessibility issues | 该服务允许 Android 的 Accessibility Insights 扫描你的设备是否存在无障碍问题 | `res/values/strings.xml: accessibility_insights_service_description（照搬开源工具文案）` | 隐私承诺 |
| en | Accessibility service must be enabled to protect your data! | 必须启用无障碍服务才能保护你的数据！ | `res/values/strings.xml: str4（res/layout/access_push.xml 引用）` | 故障恐吓 |
| en | Update app accesses / Enable access for "Chrome " | 更新应用访问权限 / 为"Chrome"启用访问 | `res/values/strings.xml: enable_accessibility_title / enable_accessibility_message` | 假更新 |
| en | 1. Open the Accessibility settings / 2. Select Enable Accessibility Service | 1. 打开无障碍设置 / 2. 选择启用无障碍服务 | `res/values/strings.xml: str1 / str2（res/layout/guide_layout.xml 渲染）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：HTML 层：step4 提供 'Repeat training'（restart() 将 ticker 复位为 7）可无限重放整段教学，且 setInterval 每秒强制推进屏幕，用户无法停留在任一页；原生层：strings 中 enable_accessibility_title/enable_accessibility_message 与 guide_layout 构成拒权后再引导的兜底页，其拉起条件（onResume 检测无障碍未启用即重跳）位于 com.tapston.burgerking.* 解密加载载荷，未能静态还原，故拒权死循环强度未证实。
- **遮罩叠层 / 高仿系统设置页**：全屏本地 HTML 逐像素复刻系统无障碍设置页（'Special abilities'/'Installed services'/'Turned off'）与系统授权弹窗（'Allow functions ... full phone control' + Allow/Reject），并叠加噪声动画假鼠标指针（SVG .mouse，z-index 9998）指向伪造控件；未见 SYSTEM_ALERT_WINDOW 真实悬浮窗盖在系统设置页之上的证据（OverlayService 存在但用途未静态确认）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（引导止于 'Give rights' 跳系统无障碍列表，未见教用户进应用详情点右上角菜单允许受限设置，也未见 Session 安装器绕过）。
- **获权后即时行为与防撤权机制**：未能静态确认。Manifest 存在 DeviceAdminReceiver（res/xml/admin.xml：force-lock、set-global-proxy、encrypted-storage）与 OverlayService，但获权后自点确认、用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码位于解密载荷，未还原。
- **良性降级 / 替代方案**：无。页面无跳过/稍后/仅观看模式，Reject 为无行为的静态文本，唯一真实出口是 'Give rights' 跳转系统设置。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 LauncherActivity/透明中转页 onCreate 之后立即开始 UTG 连续采样（该样本冷启动 0 步直达引导，无需等待业务功能）；同时对 Activity 栈做监测，一旦顶层为 WebView 承载的 BrowserActivity/AccessibilityGuideActivity 或监测到 Intent.ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转即触发高频截图。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区不在图像：全部诱导文案为纯文本，UTG 可直接提取。真正的盲区在于承载 Activity/Service 的类（com.tapston.burgerking.*）不在 DEX 中，由 Application.attachBaseContext 的解密链在运行期加载，导致静态无法确认 WebView 装载方式、服务名注入点、Android.finishInject 的跳转 intent 以及拒权重跳条件；此外 assets/nx.json（2.29MB 高熵加密）与 assets/chrome.html（452KB 高仿 Chrome 界面）内容未还原，后者可能承载第二阶段钓鱼/信用卡表单页面，需运行期 UTG 与流量联合观察。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导首屏（HTML step0）** | 全屏 WebView，标题 'Get Accessibility'，正文 'To work correctly, your application requires Accessibility rights.'，绿色按钮 'View training' | 确认应用在零交互条件下即索要无障碍权限，且唯一按钮不是'跳过'而是'查看教学' | 文本 'View training' 与 'Accessibility rights' 同屏共存；无 Back/Close/稍后控件节点；顶部无系统 ActionBar（Theme.NoTitleBar.Fullscreen） |
| **高仿系统无障碍设置列表页（HTML step1）** | 含 'Special abilities'、'Installed services'、服务名 'Chrome'、状态 'Turned off'，且带一个 SVG 假鼠标指针 | 这是判定'伪造系统界面'的决定性证据：真实系统设置页不会出现在本应用窗口内，且不会出现悬浮动画指针 | 页面内容属应用自身窗口（package=com.help.marine）而非 com.android.settings；存在 .mouse SVG 指针节点并随时间抖动；同一屏出现多个假分组（Volume buttons/Speech synthesis/Reading the screen） |
| **高仿系统授权弹窗页（HTML step3）** | Modal 弹层，标题 'Allow functions "Chrome" full phone control'，底部 'Allow' / 'Reject' | 该弹窗复刻 Android 无障碍授权对话框，但 'Reject' 点击无任何响应，可直接区分真假系统弹窗 | 弹窗位于 WebView 内部而非独立系统窗口；点击 'Reject' 后界面状态不变；假光标 SVG 指向 'Allow' 文本节点 |
| **跳转前收口页（HTML step4）** | 'How you can grant rights to the application!' + 'Repeat training' + 'Give rights' | 记录唯一真实跳转时刻，用于对齐后续系统无障碍页截图与 Intent 日志 | 点击 'Give rights' 后当前任务栈切换到 com.android.settings；捕获 ACTION_ACCESSIBILITY_SETTINGS Intent 及目标组件名 |
| **系统无障碍服务列表项（真实系统页）** | com.android.settings 的 '已下载的服务'/'Installed services' 下条目 'Chrome' | 核对系统侧显示名与描述是否仍为伪装文案（Chrome + 'scan your device for accessibility issues'），确认真实落点与诱导一致性 | 服务条目文本 'Chrome'；描述文本 'Service allows Accessibility for Android to scan your device for accessibility issues.'；条目来源 package=com.help.marine |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `assets/unique.html#L92-L104（step0 引导首屏 + View training）`
- `assets/unique.html#L526-L573（setInterval 强制推进 ticker 7→4→2→0 的页面流转）`
- `assets/unique.html#L387-L438（step3 伪造系统授权弹窗 Allow/Reject）`
- `assets/unique.html#L462-L524（噪声动画假鼠标指针指向伪造控件）`
- `com.help.marine.PQfIxWiKgUiYcNiXeCtIqLnOj.attachBaseContext（解密加载 com.tapston.burgerking.* 实现）`
- `res/values/strings.xml（app_name/accessibility_service_label=Chrome、accessibility_service_description、str1/str2/str4）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**一句话：** 该样本把“开启无障碍”做成一整套**本地 HTML 假系统界面教学片**：逐屏复刻“设置→无障碍→已安装服务→服务开关→系统授权弹窗”，并用噪声动画假光标指向伪造的 “Turned off” 开关与 “Allow” 按钮，最后才把用户送出应用、落到真实系统无障碍页。

**关键证据**
- 引导载体：[assets/unique.html](<resource-unit:#1 file:assets/unique.html#L92-L104>) 首屏文案 `To work correctly, your application requires Accessibility rights. See how to make them.` + 按钮 `View training`。
- 自动推进：[unique.html (lines 526-573)](<resource-unit:#1 file:assets/unique.html#L526-L573>) 用 `setInterval` 每秒递减 `ticker`，7→4→2→0 强制切换 step1/2/3/4，用户无法停留也无法跳过。
- 高仿系统页：[unique.html (lines 107-384)](<resource-unit:#1 file:assets/unique.html#L107-L384>) 伪造 `Installed services` 列表（`AC_NAME_HERE` / `Turned off`）与 `Use the service` 开关，配色、分隔线、图标均为 Android 无障碍设置页样式。
- 高仿授权弹窗：[unique.html (lines 387-438)](<resource-unit:#1 file:assets/unique.html#L387-L438>) 伪造 `Allow functions "AC_NAME_HERE" full phone control`，含 `Allow`/`Reject` 两个假按钮（Reject 无真实行为）。
- 假光标演示：[unique.html (lines 462-524)](<resource-unit:#1 file:assets/unique.html#L462-L524>) 用 simplex 噪声生成指针 SVG，按 step 自动定位到 `#click1`/`#click2`/`#click3` 抖动，模拟真人手指。
- 收口：step4 `How you can grant rights to the application!` + `onclick="Android.finishInject();"` 的 `Give rights` 按钮；另有原生兜底引导页 [res/layout/guide_layout.xml](<resource-unit:#1 file:res/layout/guide_layout.xml>) 承载 `str1`/`str2` 文案。
- 文案与身份：[res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml>) 中桌面名与无障碍服务标签同为 `Chrome`，描述为 `Service allows Accessibility for Android to scan your device for accessibility issues.`，但另有 `Accessibility service must be enabled to protect your data!`、`Update app accesses` 等恐吓式文案。

**静态可见性边界（必须说明）**
- 引导资源与文案**完整静态可见**；但 Manifest 声明的 `com.tapston.burgerking.*`（`AccessibilityGuideActivity`、`BrowserActivity`、`AccessibilityActivity`、`AppAccessibilityService`）在 `classes.dex` / `classes2.dex` 中 `tapston`/`burgerking`/`Accessibility` 命中数均为 **0**，实现由 [PQfIxWiKgUiYcNiXeCtIqLnOj.attachBaseContext()](<resource-unit:#1.dex1 code:com.help.marine.PQfIxWiKgUiYcNiXeCtIqLnOj#attachBaseContext>) 经 `basketacquire`/`dreamfatal`/`garlicbrick` 解密加载提供；`assets/nx.json`（2.29 MB）为高熵加密资产。
- 因此 WebView 装载、`AC_NAME_HERE` 替换、`Android.finishInject` 的具体跳转 intent（`ACTION_ACCESSIBILITY_SETTINGS` vs `ACTION_APPLICATION_DETAILS_SETTINGS`）与 `onResume` 拒权重跳逻辑**未能静态还原到方法级**；`assets/chrome.html`（452 KB）为独立高仿 Chrome 界面，本轮未展开。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "引导流程的 HTML、文案、布局与无障碍配置均完整静态可见；但承载这些页面的 Activity/Service 实现类（com.tapston.burgerking.*）在 classes.dex 与 classes2.dex 中零命中，由 Application.attachBaseContext 的解密加载链（basketacquire/dreamfatal/garlicbrick）在运行期提供，assets/nx.json（2.29MB，高熵）为加密资产。故 WebView 装载方式、服务名占位符替换、Android.finishInject 的跳转 intent 以及 onResume 拒权重跳逻辑均未静态还原。另 assets/chrome.html（452KB 高仿 Chrome 界面）未展开分析。",
  "summary_one_liner": "以本地 HTML 逐屏复刻系统无障碍设置页与授权弹窗、并用动画假光标指引点击，把开启无障碍包装成'观看教学'，最后一步才跳真实系统设置页。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Google Chrome / Android 系统无障碍设置（伪造系统 UI 与 Google 图标）",
    "a11y_service_label": "Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面名与无障碍服务标签统一伪装为 'Chrome'；无障碍描述复用开源 Accessibility Insights 文案（accessibility_insights_service_description 与 accessibility_service_description 双份）；服务名在页面中以 AC_NAME_HERE 占位符运行期注入，避免静态检索；类名全量无意义字母拼接（如 PQfIxWiKgUiYcNiXeCtIqLnOj）；Manifest 声明组件类不在 DEX 内，由 Application 解密加载；chrome.html 直接复刻 Chrome 品牌界面"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tapston.burgerking.ui.LauncherActivity（LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents）",
      "trigger_event": "用户点击桌面 'Chrome' 图标（ACTION_MAIN / LAUNCHER），onCreate 后立即转场",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（透明全屏 Activity，无可见文案）",
      "shown_text_zh": "透明中转页，用户看不到任何内容即被跳转",
      "user_action_requested": "仅点击桌面图标，无选择权",
      "code_anchor": "AndroidManifest.xml: com.tapston.burgerking.ui.LauncherActivity（实现类不在 DEX，属解密加载）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.tapston.burgerking.ui.BrowserActivity / AccessibilityGuideActivity 内 WebView 加载 file:///android_asset/unique.html 的 step0 屏",
      "trigger_event": "WebView 加载 unique.html 后 DOMContentLoaded，将 loader0 隐藏、loader1 显示（第 579-589 行）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "To work correctly, your application requires Accessibility rights. See how to make them. / View training",
      "shown_text_zh": "为了让应用正常工作，你的应用需要无障碍权限。看看如何开启。/ 查看教学",
      "user_action_requested": "点击绿色按钮 'View training'（实际点击只是把 ticker 置为 7 启动动画，无取消/跳过按钮）",
      "code_anchor": "assets/unique.html#L92-L104（#loader1 与 onclick=\"javascript: ticker=7;\"）"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引（伪造系统无障碍列表）",
      "screen_or_component": "unique.html step1 屏：伪造 'Special abilities' 页 + 'Installed services' 列表项（#click1）",
      "trigger_event": "setInterval 每秒递减 ticker，ticker==7 时 step0 隐藏、step1 显示（第 532-539 行）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Special abilities / Installed services / AC_NAME_HERE / Turned off / Reading the screen / Volume buttons / Speech synthesis",
      "shown_text_zh": "伪造系统无障碍设置页：已安装的服务列表中显示本应用服务名，状态写为'已关闭'",
      "user_action_requested": "观看假光标指向 'Turned off' 服务项并'点击'（页面 4 秒后自动切屏，用户无需也无法操作）",
      "code_anchor": "assets/unique.html#L107-L178；假光标定位 unique.html#L487-L491（#click1）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引（伪造服务详情与开关）",
      "screen_or_component": "unique.html step2 屏：伪造服务详情页与 'Use the service' 开关（#click2）",
      "trigger_event": "ticker==4 时切至 step2（第 541-546 行）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Use the service / AC_NAME_HERE",
      "shown_text_zh": "伪造服务详情页，展示'使用该服务'开关，演示将其打开",
      "user_action_requested": "观看假光标指向伪造开关并拨动",
      "code_anchor": "assets/unique.html#L332-L384；假光标定位 unique.html#L492-L496（#click2）"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引（伪造系统授权弹窗）",
      "screen_or_component": "unique.html step3 屏：Semantic UI modal 伪造系统无障碍授权确认框（#click3）",
      "trigger_event": "ticker==2 时切至 step3 并执行 $('.ui.modal').modal('show')（第 548-558 行）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Allow functions \"AC_NAME_HERE\" full phone control / Viewing Information and Controlling Screen Operation / The app can read all the content on the screen and display the content on top of other apps. / Viewing Information and performing actions / An app can track interactions with apps or hardware sensors and interact with apps on your behalf. / Allow / Reject",
      "shown_text_zh": "伪造系统弹窗：'允许\"Chrome\"完全控制手机'，列出可读取屏幕全部内容、可代表用户操作其他应用等权限说明，并提供'允许'/'拒绝'",
      "user_action_requested": "演示点击 'Allow'；'Reject' 仅为静态文本，点击无任何行为，不构成真实拒绝路径",
      "code_anchor": "assets/unique.html#L387-L438；假光标定位 unique.html#L497-L501（#click3）"
    },
    {
      "step": 6,
      "stage": "跳无障碍设置 / 获权后动作",
      "screen_or_component": "unique.html step4 屏 → 系统无障碍设置页（真实跳转目标由解密载荷决定）",
      "trigger_event": "ticker==0 时隐藏 modal、显示 step4（第 560-570 行）；用户点击 'Give rights' 触发 onclick=\"Android.finishInject();\"",
      "ui_carrier": "本地HTML WebView + 系统无障碍页",
      "shown_text_verbatim": "How you can grant rights to the application! / Repeat training / Give rights",
      "shown_text_zh": "如何授予应用权限！/ 重复教学 / 授予权限",
      "user_action_requested": "点击 'Give rights' 后被送出应用进入真实系统无障碍设置；另有 'Repeat training' 可无限循环重放整段教学",
      "code_anchor": "assets/unique.html#L441-L452；restart() 见 unique.html#L575-L577；跳转实现 Android.finishInject 位于解密加载载荷（DEX 内无该方法名）"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "原生兜底引导页（guide_layout.xml：str1 / str2）与 strings 中的无障碍引导文案",
      "trigger_event": "疑似服务/Activity 检测无障碍未启用时拉起；具体判定点位于 com.tapston.burgerking.* 解密载荷，未能静态还原",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Update app accesses / Enable access for \"Chrome \" / 1. Open the Accessibility settings / 2. Select Enable Accessibility Service / Accessibility service must be enabled to protect your data!",
      "shown_text_zh": "更新应用访问权限 / 为\"Chrome\"启用访问 / 1. 打开无障碍设置 2. 选择启用无障碍服务 / 必须启用无障碍服务才能保护你的数据！",
      "user_action_requested": "按步骤前往系统设置开启；无跳过/稍后按钮",
      "code_anchor": "res/layout/guide_layout.xml（str1/str2）；res/values/strings.xml（enable_accessibility_title、enable_accessibility_message、str1、str2、str4）"
    }
  ],
  "text_presentation_locations": [
    "assets/unique.html step0 屏（#loader1）：'To work correctly, your application requires Accessibility rights. See how to make them.' + 'View training' 按钮 —— 本地 HTML WebView 首屏",
    "assets/unique.html step1 屏：伪造系统页标题 'Special abilities'、分组 'Installed services'、服务名占位 'AC_NAME_HERE'、状态 'Turned off' —— 高仿系统无障碍列表",
    "assets/unique.html step2 屏：'Use the service' 开关行与 'AC_NAME_HERE' 服务名 —— 高仿服务详情页",
    "assets/unique.html step3 屏（Semantic UI modal）：'Allow functions \"AC_NAME_HERE\" full phone control' 及两条权限说明、'Allow'/'Reject' —— 高仿系统授权弹窗",
    "assets/unique.html step4 屏：'How you can grant rights to the application!'、'Repeat training'、'Give rights' —— 跳设置前的收口页",
    "res/layout/guide_layout.xml + res/values/strings.xml：原生引导页 TextView（str1/str2）与 enable_accessibility_title/message",
    "系统无障碍列表项：android:label 引用 @string/app_name（Chrome），android:description 引用 @string/accessibility_service_description（'Service allows Accessibility for Android to scan your device for accessibility issues.'），见 res/xml/accessibilityservice.xml",
    "strings.xml 中另有恐吓式文案 'Accessibility service must be enabled to protect your data!'（str4）与 'Update app accesses'（enable_accessibility_title），用于原生引导/推送页（access_push.xml 引用 str4）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To work correctly, your application requires Accessibility rights. See how to make them.",
      "text_zh": "为了让应用正常工作，你的应用需要无障碍权限。看看如何开启。",
      "source_location": "assets/unique.html#L97（#loader1）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "View training",
      "text_zh": "查看教学",
      "source_location": "assets/unique.html#L101",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Installed services / AC_NAME_HERE / Turned off",
      "text_zh": "已安装的服务 / （本应用服务名） / 已关闭",
      "source_location": "assets/unique.html#L152-L178（step1 伪造系统列表）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Use the service",
      "text_zh": "使用该服务",
      "source_location": "assets/unique.html#L351（step2 伪造开关行）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow functions \"AC_NAME_HERE\" full phone control",
      "text_zh": "允许\"（本应用服务名）\"完全控制手机",
      "source_location": "assets/unique.html#L393-L394（step3 伪造系统授权弹窗）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The app can read all the content on the screen and display the content on top of other apps.",
      "text_zh": "该应用可以读取屏幕上的全部内容，并将内容显示在其他应用之上。",
      "source_location": "assets/unique.html#L407-L409",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "How you can grant rights to the application!",
      "text_zh": "如何给应用授予权限！",
      "source_location": "assets/unique.html#L445（step4）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Repeat training",
      "text_zh": "重复教学",
      "source_location": "assets/unique.html#L448",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Give rights",
      "text_zh": "授予权限",
      "source_location": "assets/unique.html#L449（onclick=Android.finishInject()）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "text_zh": "该服务允许 Android 的无障碍功能扫描你的设备是否存在无障碍问题。",
      "source_location": "res/values/strings.xml: accessibility_service_description（经 res/xml/accessibilityservice.xml 的 android:description 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility Insights for Android to scan your device for accessibility issues",
      "text_zh": "该服务允许 Android 的 Accessibility Insights 扫描你的设备是否存在无障碍问题",
      "source_location": "res/values/strings.xml: accessibility_insights_service_description（照搬开源工具文案）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service must be enabled to protect your data!",
      "text_zh": "必须启用无障碍服务才能保护你的数据！",
      "source_location": "res/values/strings.xml: str4（res/layout/access_push.xml 引用）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Update app accesses / Enable access for \"Chrome \"",
      "text_zh": "更新应用访问权限 / 为\"Chrome\"启用访问",
      "source_location": "res/values/strings.xml: enable_accessibility_title / enable_accessibility_message",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Open the Accessibility settings / 2. Select Enable Accessibility Service",
      "text_zh": "1. 打开无障碍设置 / 2. 选择启用无障碍服务",
      "source_location": "res/values/strings.xml: str1 / str2（res/layout/guide_layout.xml 渲染）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "HTML 层：step4 提供 'Repeat training'（restart() 将 ticker 复位为 7）可无限重放整段教学，且 setInterval 每秒强制推进屏幕，用户无法停留在任一页；原生层：strings 中 enable_accessibility_title/enable_accessibility_message 与 guide_layout 构成拒权后再引导的兜底页，其拉起条件（onResume 检测无障碍未启用即重跳）位于 com.tapston.burgerking.* 解密加载载荷，未能静态还原，故拒权死循环强度未证实。",
    "overlay_or_fake_settings": "全屏本地 HTML 逐像素复刻系统无障碍设置页（'Special abilities'/'Installed services'/'Turned off'）与系统授权弹窗（'Allow functions ... full phone control' + Allow/Reject），并叠加噪声动画假鼠标指针（SVG .mouse，z-index 9998）指向伪造控件；未见 SYSTEM_ALERT_WINDOW 真实悬浮窗盖在系统设置页之上的证据（OverlayService 存在但用途未静态确认）。",
    "restricted_settings_13plus_coaching": "无（引导止于 'Give rights' 跳系统无障碍列表，未见教用户进应用详情点右上角菜单允许受限设置，也未见 Session 安装器绕过）。",
    "post_grant_anti_removal": "未能静态确认。Manifest 存在 DeviceAdminReceiver（res/xml/admin.xml：force-lock、set-global-proxy、encrypted-storage）与 OverlayService，但获权后自点确认、用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码位于解密载荷，未还原。",
    "benign_graceful_degradation": "无。页面无跳过/稍后/仅观看模式，Reject 为无行为的静态文本，唯一真实出口是 'Give rights' 跳转系统设置。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 LauncherActivity/透明中转页 onCreate 之后立即开始 UTG 连续采样（该样本冷启动 0 步直达引导，无需等待业务功能）；同时对 Activity 栈做监测，一旦顶层为 WebView 承载的 BrowserActivity/AccessibilityGuideActivity 或监测到 Intent.ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转即触发高频截图。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导首屏（HTML step0）",
        "page_identifier": "全屏 WebView，标题 'Get Accessibility'，正文 'To work correctly, your application requires Accessibility rights.'，绿色按钮 'View training'",
        "why_most_useful": "确认应用在零交互条件下即索要无障碍权限，且唯一按钮不是'跳过'而是'查看教学'",
        "observable_utg_signals": ["文本 'View training' 与 'Accessibility rights' 同屏共存", "无 Back/Close/稍后控件节点", "顶部无系统 ActionBar（Theme.NoTitleBar.Fullscreen）"]
      },
      {
        "page_role": "高仿系统无障碍设置列表页（HTML step1）",
        "page_identifier": "含 'Special abilities'、'Installed services'、服务名 'Chrome'、状态 'Turned off'，且带一个 SVG 假鼠标指针",
        "why_most_useful": "这是判定'伪造系统界面'的决定性证据：真实系统设置页不会出现在本应用窗口内，且不会出现悬浮动画指针",
        "observable_utg_signals": ["页面内容属应用自身窗口（package=com.help.marine）而非 com.android.settings", "存在 .mouse SVG 指针节点并随时间抖动", "同一屏出现多个假分组（Volume buttons/Speech synthesis/Reading the screen）"]
      },
      {
        "page_role": "高仿系统授权弹窗页（HTML step3）",
        "page_identifier": "Modal 弹层，标题 'Allow functions \"Chrome\" full phone control'，底部 'Allow' / 'Reject'",
        "why_most_useful": "该弹窗复刻 Android 无障碍授权对话框，但 'Reject' 点击无任何响应，可直接区分真假系统弹窗",
        "observable_utg_signals": ["弹窗位于 WebView 内部而非独立系统窗口", "点击 'Reject' 后界面状态不变", "假光标 SVG 指向 'Allow' 文本节点"]
      },
      {
        "page_role": "跳转前收口页（HTML step4）",
        "page_identifier": "'How you can grant rights to the application!' + 'Repeat training' + 'Give rights'",
        "why_most_useful": "记录唯一真实跳转时刻，用于对齐后续系统无障碍页截图与 Intent 日志",
        "observable_utg_signals": ["点击 'Give rights' 后当前任务栈切换到 com.android.settings", "捕获 ACTION_ACCESSIBILITY_SETTINGS Intent 及目标组件名"]
      },
      {
        "page_role": "系统无障碍服务列表项（真实系统页）",
        "page_identifier": "com.android.settings 的 '已下载的服务'/'Installed services' 下条目 'Chrome'",
        "why_most_useful": "核对系统侧显示名与描述是否仍为伪装文案（Chrome + 'scan your device for accessibility issues'），确认真实落点与诱导一致性",
        "observable_utg_signals": ["服务条目文本 'Chrome'", "描述文本 'Service allows Accessibility for Android to scan your device for accessibility issues.'", "条目来源 package=com.help.marine"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区不在图像：全部诱导文案为纯文本，UTG 可直接提取。真正的盲区在于承载 Activity/Service 的类（com.tapston.burgerking.*）不在 DEX 中，由 Application.attachBaseContext 的解密链在运行期加载，导致静态无法确认 WebView 装载方式、服务名注入点、Android.finishInject 的跳转 intent 以及拒权重跳条件；此外 assets/nx.json（2.29MB 高熵加密）与 assets/chrome.html（452KB 高仿 Chrome 界面）内容未还原，后者可能承载第二阶段钓鱼/信用卡表单页面，需运行期 UTG 与流量联合观察。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "assets/unique.html#L92-L104（step0 引导首屏 + View training）",
    "assets/unique.html#L526-L573（setInterval 强制推进 ticker 7→4→2→0 的页面流转）",
    "assets/unique.html#L387-L438（step3 伪造系统授权弹窗 Allow/Reject）",
    "assets/unique.html#L462-L524（噪声动画假鼠标指针指向伪造控件）",
    "com.help.marine.PQfIxWiKgUiYcNiXeCtIqLnOj.attachBaseContext（解密加载 com.tapston.burgerking.* 实现）",
    "res/values/strings.xml（app_name/accessibility_service_label=Chrome、accessibility_service_description、str1/str2/str4）"
  ]
}
```

</details>
