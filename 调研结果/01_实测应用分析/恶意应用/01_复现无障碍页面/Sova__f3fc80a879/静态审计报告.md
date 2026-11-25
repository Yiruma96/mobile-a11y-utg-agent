# MB_123__f3fc80a879｜Sova — PancakeSwap

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：186.1s

## 1. 一句话核心结论

- **核心申请方式**：以 PancakeSwap 名义伪装、借『无障碍自检/保护你的数据』话术，用本地 HTML 高仿 Android 无障碍设置页并配自动移动的动画鼠标分步演示，最后经 JS 桥 Android.finishInject() 拉起真实无障碍设置，全程无跳过、Reject 无响应。
- **静态可见性说明**：Manifest、res/values/strings.xml、res/xml/accessibilityservice.xml 与 assets/unique.html 完全静态可见，可完整还原伪系统无障碍设置的 5 幕引导文案与流程；但 Java 侧控制流缺失——classes.dex/classes2.dex 中检索不到 tapston、AccessibilityService、ACTION_ACCESSIBILITY_SETTINGS、unique.html、android_asset、PancakeSwap 任一字符串，仅存 com.card.gift 129 个桩类及 com.cow.inject 注入工具，故『哪个 Activity 加载 unique.html、Android.finishInject() 如何拉起系统设置、onResume 是否死循环重跳、获权后是否自点确认或阻止撤权』不可静态还原；另有 assets/gXQDo.json（2.3MB）与 EncryptorService 疑似承载加密载荷，未解密验证。
- **命中的行为模式标签**：`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `f3fc80a8793e60a901da44b9ab315931699e64a4f3eddb8aba839fe860de46dc` |
| 包名 / 年份 | `com.card.gift` / 2023 |
| 家族 / 品类 | **Sova**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | PancakeSwap |
| 引导页宣称品牌/身份 | PancakeSwap（去中心化交易所品牌）；页面内进一步伪装为 Android 系统『辅助功能/特殊能力』设置与系统授权确认框 |
| 系统无障碍列表服务名 | PancakeSwap |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.card.gift、代码命名空间 com.tapston.burgerking 与显示名 PancakeSwap 完全无关；无障碍 description 借用系统辅助功能自检话术（'Service allows Accessibility for Android to scan your device for accessibility issues.'）并保留 Accessibility Insights 变体字符串；HTML 内用 AC_NAME_HERE 占位符在运行期替换服务名以规避静态检索；webview 前先用 Google Translate 脚本把页面按 lng 强制机翻为俄语（googtrans=/ru/）；DEX 侧业务类全部缺席，仅剩桩类与注入工具 |
| 无障碍服务类名 | `com.tapston.burgerking.service.AppAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Service allows Accessibility for Android to scan your device for accessibility issues. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tapston.burgerking.ui.LauncherActivity（exported=true, singleInstance, noHistory, Theme.Translucent.NoTitleBar.Fullscreen，唯一 MAIN/LAUNCHER 入口） | 用户点击桌面 PancakeSwap 图标，LAUNCHER intent 触发 onCreate | 原生Activity | **原文**：无（全屏透明无标题栏，无可见文案）<br>**译注**：无可见界面，仅作为跳板静默转入引导页 | 无，用户仅看到图标被点击后的界面切换 | `AndroidManifest.xml: com.tapston.burgerking.ui.LauncherActivity` |
| 2 | 引导说明页 | com.tapston.burgerking.ui.AccessibilityGuideActivity / com.tapston.burgerking.ui.accesses.AccessibilityActivity（均 exported=true、noHistory、Theme.Light.NoTitleBar.Fullscreen，加载 assets/unique.html 的 WebView 宿主，绑定代码在加密载荷内） | LauncherActivity 启动后跳转；WebView 载入本地 assets/unique.html，页面 title=Get Accessibility | 本地HTML WebView | **原文**：To work correctly, your application requires Accessibility rights. See how to make them. / View training<br>**译注**：为了让应用正常工作，需要授予无障碍权限。看看怎么做。/ 查看教学 | 点击绿色按钮 View training（onclick 仅将 ticker 置 7 并自动翻页，无取消/跳过按钮） | `assets/unique.html#step0 (loader1) / res/values/strings.xml` |
| 3 | 遮罩叠层指引 | assets/unique.html #step1 —— 高仿『设置-辅助功能-特殊能力/已安装服务』页，服务名以 AC_NAME_HERE 占位后替换为 PancakeSwap，状态写 Turned off；SVG 鼠标指针由 perlin 噪声自动移动至 #click1 | ticker==7 时 setInterval 每秒递减切幕，自动显示 step1 | 本地HTML WebView | **原文**：Special abilities / Volume buttons  Disabled / Installed services / AC_NAME_HERE  Turned off / Reading the screen / Speech synthesis / Screen / Font size  Default / Screen image scale  Default / Dark theme / Increase  Disabled / Color correction  Disabled<br>**译注**：特殊能力/音量键 已停用/已安装的服务/PancakeSwap 已关闭/读取屏幕/语音合成/屏幕/字体大小 默认/屏幕图像缩放 默认/深色主题/放大 已停用/颜色校正 已停用 | 引导用户在自己手机上找到同名服务项并点进去（界面本身为伪造，点击 #click1 仅推进 HTML 动画） | `assets/unique.html#step1 (L107-L330)` |
| 4 | 引导说明页 | assets/unique.html #step2 —— 高仿无障碍『服务详情页』，含 Use the service 开关（#click2） | ticker==4 自动切幕，鼠标指针移动到 #click2 位置做『打开开关』演示 | 本地HTML WebView | **原文**：AC_NAME_HERE / Use the service<br>**译注**：PancakeSwap / 使用该服务 | 演示把服务开关拨到开启（真实操作需用户到系统页完成，此处为动画） | `assets/unique.html#step2 (L332-L385)` |
| 5 | 引导说明页 | assets/unique.html #step3 —— 仿系统无障碍授权确认弹窗（semantic-ui modal） | ticker==2 自动切幕并 $('.ui.modal').modal('show') | 本地HTML WebView | **原文**：Allow functions "AC_NAME_HERE" full phone control / Viewing Information and Controlling Screen Operation — The app can read all the content on the screen and display the content on top of other apps. / Viewing Information and performing actions — An app can track interactions with apps or hardware sensors and interact with apps on your behalf. / Allow / Reject<br>**译注**：允许「PancakeSwap」完全控制手机 / 查看信息并控制屏幕操作——该应用可读取屏幕全部内容并显示在其他应用之上 / 查看信息并执行操作——该应用可跟踪与其他应用或硬件传感器的交互，并代表你与其他应用交互 / 允许 / 拒绝 | 点 Allow（#click3，指针自动移入演示）；Reject 为纯文本、未绑定任何事件，点了无反应 | `assets/unique.html#step3 (L387-L439)` |
| 6 | 拒权反馈循环 | assets/unique.html #step4 —— 'How you can grant rights to the application!' 页，含 Repeat training 与绿色 Give rights | ticker==0 时隐藏 modal 并显示 step4 | 本地HTML WebView | **原文**：How you can grant rights to the application! / Repeat training / Give rights<br>**译注**：如何把权限授予该应用！/ 重看教学 / 授予权限 | 点 Give rights 调 JS 桥 Android.finishInject()；点 Repeat training 仅 restart() 把 ticker 重置为 7，回到第 2 步循环教学，无任何『跳过/暂不』出口 | `assets/unique.html#step4 (L441-L452) 与 restart()/ticker 定时器` |
| 7 | 跳无障碍设置 | JS 桥 Android.finishInject() → 原生侧跳转（预期为 ACTION_ACCESSIBILITY_SETTINGS，DEX 中无该常量与对应类，控制流在加密载荷内） | 用户点击 Give rights 触发 WebView JavascriptInterface 回调 | 不可静态还原 | **原文**：无（离开 WebView 进入系统无障碍列表，列表项显示 PancakeSwap / Service allows Accessibility for Android to scan your device for accessibility issues.）<br>**译注**：进入系统无障碍设置，服务名显示为 PancakeSwap，说明为『该服务允许 Android 无障碍功能扫描你设备上的无障碍问题』 | 用户在真实系统页手动打开 PancakeSwap 服务开关（该页为系统页，不可伪造） | `assets/unique.html onclick="Android.finishInject()" / res/xml/accessibilityservice.xml / AndroidManifest.xml AppAccessibilityService` |
| 8 | 获权后动作 | com.tapston.burgerking.service.AppAccessibilityService（typeAllMask, canRetrieveWindowContent, canPerformGestures）+ com.tapston.burgerking.service.OverlayService + NotificationService + MyAdminReceiver/AdminActivity + IgnoreBatteryOptimizationsActivity | 系统 BIND_ACCESSIBILITY_SERVICE 绑定服务后 onServiceConnected（服务实现体不在可静态还原范围内） | 不可静态还原 | **原文**：Accessibility service must be enabled to protect your data! / Allow pop-ups / Checking system / Checking<br>**译注**：必须启用无障碍服务才能保护你的数据！/ 允许弹窗 / 正在检查系统 / 检查中 | 预期继续索取悬浮窗、忽略电池优化、设备管理器等权限（对应 PermissionsActivity、IgnoreBatteryOptimizationsActivity、AdminActivity，具体顺序不可静态还原） | `AndroidManifest.xml 组件声明 / res/values/strings.xml#str4,#miuipopup,#managing_service_title` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务标签 PancakeSwap（res/values/strings.xml accessibility_service_label），说明文字 'Service allows Accessibility for Android to scan your device for accessibility issues.'（@string/accessibility_service_description，res/xml/accessibilityservice.xml 引用）
- 本地 WebView 页面 assets/unique.html：title 'Get Accessibility'，第 0 幕提示 'To work correctly, your application requires Accessibility rights...' 与按钮 'View training'
- assets/unique.html 第 1 幕：伪造的『设置-特殊能力/已安装服务/屏幕』列表页，服务名经 AC_NAME_HERE 替换为 PancakeSwap，状态 'Turned off'
- assets/unique.html 第 2 幕：伪造的服务详情页，'Use the service' 开关（#click2）
- assets/unique.html 第 3 幕：伪造的系统授权确认弹窗 'Allow functions "AC_NAME_HERE" full phone control' + Allow/Reject
- assets/unique.html 第 4 幕：'How you can grant rights to the application!' 页，Repeat training / Give rights 按钮
- 页面内叠加的 SVG 鼠标指针动画（perlin 噪声驱动，自动移动到 #click1/#click2/#click3），以图形化『手指演示』替代文字说明
- res/values/strings.xml 中保留但需原生层调用的文案：enable_accessibility_title 'Update app accesses'、enable_accessibility_message 'Enable access for "PancakeSwap"'、str1-str4 三步教学、'Accessibility service must be enabled to protect your data!'、managing_service_title 'Checking system'、miuipopup 'Allow pop-ups'（原生弹窗/Toast/悬浮窗载体，控制流在加密载荷内）
- assets/chrome.html 与 assets/nointernet.html：配合 BrowserActivity（noHistory、全屏）使用的仿浏览器/断网页载体，用于承载后续钓鱼页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To work correctly, your application requires Accessibility rights. See how to make them. | 为了让应用正常工作，需要授予无障碍权限。看看该怎么做。 | `assets/unique.html#step0 loader1` | 受限设置分步教学 |
| en | View training | 查看教学 | `assets/unique.html#step0 绿色按钮` | 受限设置分步教学 |
| en | Special abilities | 特殊能力 | `assets/unique.html#step1 顶部固定菜单（仿系统辅助功能页标题）` | 未知 |
| en | Installed services / AC_NAME_HERE / Turned off | 已安装的服务 / PancakeSwap / 已关闭 | `assets/unique.html#step1 #click1` | 受限设置分步教学 |
| en | Use the service | 使用该服务 | `assets/unique.html#step2 #click2` | 受限设置分步教学 |
| en | Allow functions "AC_NAME_HERE" full phone control | 允许「PancakeSwap」完全控制手机 | `assets/unique.html#step3 伪系统授权弹窗标题` | 受限设置分步教学 |
| en | Viewing Information and Controlling Screen Operation — The app can read all the content on the screen and display the content on top of other apps. | 查看信息并控制屏幕操作——该应用可以读取屏幕上的全部内容，并把内容显示在其他应用之上。 | `assets/unique.html#step3 能力说明第 1 条` | 受限设置分步教学 |
| en | Viewing Information and performing actions — An app can track interactions with apps or hardware sensors and interact with apps on your behalf. | 查看信息并执行操作——该应用可以跟踪你与其他应用或硬件传感器的交互，并代表你与其他应用交互。 | `assets/unique.html#step3 能力说明第 2 条` | 受限设置分步教学 |
| en | How you can grant rights to the application! / Repeat training / Give rights | 如何把权限授予该应用！/ 重看教学 / 授予权限 | `assets/unique.html#step4` | 受限设置分步教学 |
| en | Accessibility service must be enabled to protect your data! | 必须启用无障碍服务才能保护你的数据！ | `res/values/strings.xml key=str4` | 假反诈安全 |
| en | Update app accesses | 更新应用访问权限 | `res/values/strings.xml key=enable_accessibility_title` | 假更新 |
| en | Enable access for "PancakeSwap" | 为「PancakeSwap」启用访问权限 | `res/values/strings.xml key=enable_accessibility_message` | 假更新 |
| en | Checking system / Checking | 正在检查系统 / 检查中 | `res/values/strings.xml key=managing_service_title, managing_service_message` | 清理工具伪装 |
| en | 1. Open the Accessibility settings  2. Select Enable Accessibility Service  3. Slide the switch to enable | 1. 打开无障碍设置  2. 选择『启用无障碍服务』  3. 滑动开关以启用 | `res/values/strings.xml key=str1,str2,str3` | 受限设置分步教学 |
| en | Service allows Accessibility for Android to scan your device for accessibility issues. | 该服务允许 Android 无障碍功能扫描你设备上的无障碍问题。 | `res/values/strings.xml key=accessibility_service_description（由 res/xml/accessibilityservice.xml android:description 引用，显示于系统无障碍服务列表）` | 良性透明说明 |
| en | Service allows Accessibility Insights for Android to scan your device for accessibility issues | 该服务允许 Android 无障碍洞察功能扫描你设备上的无障碍问题 | `res/values/strings.xml key=accessibility_insights_service_description` | 良性透明说明 |
| en | Allow pop-ups | 允许弹窗 | `res/values/strings.xml key=miuipopup（MIUI 悬浮窗权限引导文案）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：HTML 层无任何取消/跳过出口：step3 的 Reject 为未绑定事件的纯文本，点击无反应；step4 的 Repeat training 仅把 ticker 重置为 7，重新播放整套教学并再次走到 Give rights；ticker 每 1 秒自动递减强制翻页，用户无法停留在中间页。原生层是否在 onResume 检测未获权后再次拉起 AccessibilityGuideActivity 属于加密载荷内逻辑，本次不可静态还原。
- **遮罩叠层 / 高仿系统设置页**：有。assets/unique.html 内含高仿系统无障碍『特殊能力/已安装服务』列表页、高仿服务详情开关页以及高仿系统授权确认弹窗（Allow/Reject）；另声明 com.tapston.burgerking.service.OverlayService 与 SYSTEM_ALERT_WINDOW/ACTION_MANAGE_OVERLAY_PERMISSION 权限，用于在真实系统页之上叠加半透明引导窗（叠加时机与内容不可静态还原）；SVG 鼠标指针以噪声动画模拟手指在伪设置页上自动点击。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：不可静态还原（服务实现体与 onResume 逻辑不在 DEX 内；但已声明 MyAdminReceiver/BIND_DEVICE_ADMIN、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED + BootReceiver、AlarmBroadcastReceiver、NotificationService，具备抗撤权/自启动的组件基础）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动点击图标后，监测到 Theme.Light.NoTitleBar.Fullscreen 且非系统包的全屏 Activity（预期为 com.tapston.burgerking.ui.AccessibilityGuideActivity / ui.accesses.AccessibilityActivity）出现并承载 WebView 的瞬间立即拉起 UTG；次优触发点为监测到 Android.finishInject() 后跳转 android.settings.ACCESSIBILITY_SETTINGS，以及之后 SYSTEM_ALERT_WINDOW 类型的 OverlayService 悬浮窗出现时。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两类盲区：其一，Java 侧控制流不在 DEX 中（classes.dex/classes2.dex 检索不到 tapston、AccessibilityService、ACTION_ACCESSIBILITY_SETTINGS、unique.html 等字符串，业务类整体缺席，仅剩 com.card.gift 桩类与 com.cow.inject 注入工具），故『哪个 Activity 加载 unique.html、finishInject 如何跳设置、onResume 是否死循环重跳、获权后是否自点确认或阻止撤权』必须靠运行期 UTG 观测补齐；其二，assets/gXQDo.json（2.3MB）与 EncryptorService 疑似加密载荷，若真实恶意面板与云控只在解密后出现，纯静态与单次 UTG 均可能只见『温和外壳』。另注意页面会通过 Google Translate 脚本按系统语言把自身机翻为俄语（googtrans=/ru/），UTG 文本采集需兼容多语言匹配。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后第一步教学提示页（step0 loader1）** | 全屏无标题栏 WebView，标题 'Get Accessibility'，正文含 'your application requires Accessibility rights'，单个绿色按钮 'View training' | 这是整个诱导链的起点，能证明应用一启动就以『需要无障碍权限才能正常工作』为前置条件，且界面上不存在跳过/取消按钮 | 无跳过/取消控件，仅单个 View training 按钮；文案包含 Accessibility rights 与 See how to make them；页面为本地 assets 加载（URL 为 file:///android_asset/unique.html 或空 referer） |
| **高仿系统无障碍设置页（step1/step2）** | WebView 内渲染出 'Special abilities' 标题、'Installed services' 分组、服务项显示为 PancakeSwap 且状态 'Turned off'，随后切到 'Use the service' 开关页 | 这是区分『正常引导用户去系统设置』与『伪造系统界面欺骗用户』的决定性证据：真实系统页不会出现在应用 WebView 内，且不会由应用自己渲染 PancakeSwap 服务条目 | 页面由应用进程 WebView 渲染而非系统设置（无 com.android.settings 包名）；出现 'Installed services'、'Turned off' 等系统页同款字段；存在自动移动的 SVG 鼠标指针叠加元素 |
| **伪造系统授权确认弹窗（step3）** | WebView 内 modal：'Allow functions "PancakeSwap" full phone control'，两条能力说明 + 'Allow' / 'Reject' | 证明应用伪造系统级授权确认框，并刻意让 Reject 失效（点击无响应），构成无退出路径的同意压迫 | Reject 文本无可点击属性/点击后界面无变化；弹窗文案与系统无障碍授权页原文高度一致但位于应用 WebView 内；弹窗出现后 1 秒内自动被 step4 覆盖，用户无操作窗口 |
| **设置页后的悬浮遮罩引导窗** | TYPE_APPLICATION_OVERLAY / TYPE_SYSTEM_ALERT 窗口，由 com.tapston.burgerking.service.OverlayService 创建，覆盖在 android.settings.ACCESSIBILITY_SETTINGS 之上 | 用于确认应用在真实系统页之上叠加遮罩/引导，是『遮罩叠层指引』这一强制手段的直接运行期证据 | 顶层窗口包名为 com.card.gift 且窗口类型为系统悬浮窗；系统无障碍设置页被非系统窗口遮挡；悬浮窗内文本指向 PancakeSwap 服务开关位置 |
| **系统无障碍服务列表项（真实系统页）** | com.android.settings 无障碍列表中出现条目 'PancakeSwap'，副标题 'Service allows Accessibility for Android to scan your device for accessibility issues.' | 核对系统侧实际呈现的服务名与说明是否与显示名一致、是否借用系统自检话术掩盖真实读屏/代点能力 | 服务标签 PancakeSwap 与包名 com.card.gift 不一致；description 使用『scan your device for accessibility issues』话术；服务项未标注为系统无障碍工具 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `AndroidManifest.xml: service com.tapston.burgerking.service.AppAccessibilityService (android:label=@string/app_name, android:permission=BIND_ACCESSIBILITY_SERVICE, meta-data android.accessibilityservice=@xml/accessibilityservice)`
- `res/xml/accessibilityservice.xml: android:description=@string/accessibility_service_description, accessibilityEventTypes=typeAllMask, flags=flagDefault|flagIncludeNotImportantViews|flagReportViewIds|flagRequestTouchExplorationMode, canRetrieveWindowContent=true, canPerformGestures=true`
- `res/values/strings.xml: accessibility_service_label/app_name=PancakeSwap, enable_accessibility_title='Update app accesses', enable_accessibility_message, str1-str4, managing_service_title='Checking system', miuipopup='Allow pop-ups'`
- `assets/unique.html#step0-step4（L77-L452）：伪造无障碍设置五幕流程 + AC_NAME_HERE 占位替换`
- `assets/unique.html onclick="Android.finishInject()"（step4 Give rights 按钮）与 restart()/ticker 定时器`
- `AndroidManifest.xml: com.tapston.burgerking.ui.AccessibilityGuideActivity / ui.accesses.AccessibilityActivity / ui.BrowserActivity / service.OverlayService / service.EncryptorService`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 核验结论（定向、静态）

**1. 身份伪装已确认**
- 桌面名与无障碍服务标签均为 `PancakeSwap`（`@string/app_name`、`@string/accessibility_service_label`），实际包名却是 `com.card.gift`、代码命名空间 `com.tapston.burgerking`，三者与"PancakeSwap 交易所"毫无关系。
- 无障碍服务的 `android:description` 借用系统"辅助功能扫描"话术：`Service allows Accessibility for Android to scan your device for accessibility issues.`，并保留了一个 `Accessibility Insights for Android` 变体字符串，属于典型"借用系统无障碍自检名义"。
- 服务能力开到最大：`typeAllMask`、`flagIncludeNotImportantViews`、`flagReportViewIds`、`flagRequestTouchExplorationMode`、`canRetrieveWindowContent="true"`、`canPerformGestures="true"`——即可读全屏内容并代替用户点击（配合 READ_SMS/SEND_SMS/CALL_PHONE/QUERY_ALL_PACKAGES，是 Sova 家族式银行木马的面板）。

**2. 引导载体是"本地 HTML 高仿无障碍设置流程"，不是原生弹窗**
[assets/unique.html](<resource-unit:#1 file:assets/unique.html>) 的标题就是 `Get Accessibility`，内含完整 5 幕伪系统界面（step0 提示 → step1 仿"设置-特殊能力/已安装服务"列表 → step2 仿"服务详情+Use the service 开关" → step3 仿系统授权确认框 → step4 "Give rights"），并用 `perlin.js` 噪声驱动一个 SVG 鼠标指针自动移动到 `#click1/#click2/#click3` 位置，用"动画手指演示点击"代替文字说明；`ticker` 每 1 秒递减自动翻页（8→0），全程无跳过入口。

**3. 关键文本已逐字取得**（见下方 verbatim_texts）
- 恐吓/假更新框架：`Update app accesses`、`Checking system`/`Checking`、`Accessibility service must be enabled to protect your data!`
- 分步教学：`1. Open the Accessibility settings` / `2. Select Enable Accessibility Service` / `3. Slide the switch to enable`
- 伪系统弹窗：`Allow functions "AC_NAME_HERE" full phone control`，两条能力说明直接照抄系统无障碍授权页文案，底部 `Allow` / `Reject`。

**4. 拒绝路径实际无效**：step3 的 `Reject` 只是纯文本 `<font color=blue>Reject</font>`，没有绑定任何事件；`Repeat training` 仅把 `ticker` 重置回 7，等于把用户送回循环。真正的前进按钮是 step4 的 `Give rights` → `Android.finishInject()`（JS 桥），由原生层拉起系统无障碍设置。

**5. 静态可见性受限（重要边界）**
`AndroidManifest.xml` 声明了 `com.tapston.burgerking.*` 全套组件（`AppAccessibilityService`、`AccessibilityGuideActivity`、`AccessibilityActivity`、`BrowserActivity`、`BlankActivity`、`OverlayService`、`EncryptorService`、`NotificationService`、`MyAdminReceiver`、`SmsReceiver(priority=9999)`、`PermissionsActivity`、`IgnoreBatteryOptimizationsActivity`），但两个 DEX 中 **完全不含** `tapston`、`AccessibilityService`、`ACTION_ACCESSIBILITY_SETTINGS`、`unique.html`、`android_asset`、`PancakeSwap` 等任何字符串（`com.card.gift` 仅 129 个桩类，含 `com.cow.inject` 注入工具）。即：**Manifest/资源侧的证据完整，Java 侧控制流（谁加载 unique.html、`finishInject()` 如何跳设置、onResume 是否死循环重跳、获权后是否自点确认/阻止撤权）不在可静态还原范围内**，另有 2.3MB `assets/gXQDo.json` 与 `EncryptorService` 高度疑似承载加密载荷（本次未解密验证）。

**6. UTG 抓取建议（纯运行期视角）**
最佳时机不是等系统设置页，而是**冷启动后 `AccessibilityGuideActivity`/`AccessibilityActivity` 全屏无标题栏页面出现的瞬间**——此时 fake-settings WebView 已在屏，`AC_NAME_HERE` 已被替换为 `PancakeSwap`，`step3` 伪授权框文本可直接 OCR/UTG 取到；次级时机是 `Android.finishInject()` 之后真实 `ACTION_ACCESSIBILITY_SETTINGS` 页面上叠加的 `OverlayService` 引导窗。

> 说明：本次为满足 14 次调用上限，未写入项目风险台账与生成报告；上述结论仅以 Manifest、`res/values/strings.xml`、`res/xml/accessibilityservice.xml`、`assets/unique.html` 的静态事实为据。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、res/values/strings.xml、res/xml/accessibilityservice.xml 与 assets/unique.html 完全静态可见，可完整还原伪系统无障碍设置的 5 幕引导文案与流程；但 Java 侧控制流缺失——classes.dex/classes2.dex 中检索不到 tapston、AccessibilityService、ACTION_ACCESSIBILITY_SETTINGS、unique.html、android_asset、PancakeSwap 任一字符串，仅存 com.card.gift 129 个桩类及 com.cow.inject 注入工具，故『哪个 Activity 加载 unique.html、Android.finishInject() 如何拉起系统设置、onResume 是否死循环重跳、获权后是否自点确认或阻止撤权』不可静态还原；另有 assets/gXQDo.json（2.3MB）与 EncryptorService 疑似承载加密载荷，未解密验证。",
  "summary_one_liner": "以 PancakeSwap 名义伪装、借『无障碍自检/保护你的数据』话术，用本地 HTML 高仿 Android 无障碍设置页并配自动移动的动画鼠标分步演示，最后经 JS 桥 Android.finishInject() 拉起真实无障碍设置，全程无跳过、Reject 无响应。",
  "disguise_identity": {
    "app_display_name": "PancakeSwap",
    "claimed_brand_or_persona": "PancakeSwap（去中心化交易所品牌）；页面内进一步伪装为 Android 系统『辅助功能/特殊能力』设置与系统授权确认框",
    "a11y_service_label": "PancakeSwap",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.card.gift、代码命名空间 com.tapston.burgerking 与显示名 PancakeSwap 完全无关；无障碍 description 借用系统辅助功能自检话术（'Service allows Accessibility for Android to scan your device for accessibility issues.'）并保留 Accessibility Insights 变体字符串；HTML 内用 AC_NAME_HERE 占位符在运行期替换服务名以规避静态检索；webview 前先用 Google Translate 脚本把页面按 lng 强制机翻为俄语（googtrans=/ru/）；DEX 侧业务类全部缺席，仅剩桩类与注入工具"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tapston.burgerking.ui.LauncherActivity（exported=true, singleInstance, noHistory, Theme.Translucent.NoTitleBar.Fullscreen，唯一 MAIN/LAUNCHER 入口）",
      "trigger_event": "用户点击桌面 PancakeSwap 图标，LAUNCHER intent 触发 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（全屏透明无标题栏，无可见文案）",
      "shown_text_zh": "无可见界面，仅作为跳板静默转入引导页",
      "user_action_requested": "无，用户仅看到图标被点击后的界面切换",
      "code_anchor": "AndroidManifest.xml: com.tapston.burgerking.ui.LauncherActivity"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.tapston.burgerking.ui.AccessibilityGuideActivity / com.tapston.burgerking.ui.accesses.AccessibilityActivity（均 exported=true、noHistory、Theme.Light.NoTitleBar.Fullscreen，加载 assets/unique.html 的 WebView 宿主，绑定代码在加密载荷内）",
      "trigger_event": "LauncherActivity 启动后跳转；WebView 载入本地 assets/unique.html，页面 title=Get Accessibility",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "To work correctly, your application requires Accessibility rights. See how to make them. / View training",
      "shown_text_zh": "为了让应用正常工作，需要授予无障碍权限。看看怎么做。/ 查看教学",
      "user_action_requested": "点击绿色按钮 View training（onclick 仅将 ticker 置 7 并自动翻页，无取消/跳过按钮）",
      "code_anchor": "assets/unique.html#step0 (loader1) / res/values/strings.xml"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "assets/unique.html #step1 —— 高仿『设置-辅助功能-特殊能力/已安装服务』页，服务名以 AC_NAME_HERE 占位后替换为 PancakeSwap，状态写 Turned off；SVG 鼠标指针由 perlin 噪声自动移动至 #click1",
      "trigger_event": "ticker==7 时 setInterval 每秒递减切幕，自动显示 step1",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Special abilities / Volume buttons  Disabled / Installed services / AC_NAME_HERE  Turned off / Reading the screen / Speech synthesis / Screen / Font size  Default / Screen image scale  Default / Dark theme / Increase  Disabled / Color correction  Disabled",
      "shown_text_zh": "特殊能力/音量键 已停用/已安装的服务/PancakeSwap 已关闭/读取屏幕/语音合成/屏幕/字体大小 默认/屏幕图像缩放 默认/深色主题/放大 已停用/颜色校正 已停用",
      "user_action_requested": "引导用户在自己手机上找到同名服务项并点进去（界面本身为伪造，点击 #click1 仅推进 HTML 动画）",
      "code_anchor": "assets/unique.html#step1 (L107-L330)"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "assets/unique.html #step2 —— 高仿无障碍『服务详情页』，含 Use the service 开关（#click2）",
      "trigger_event": "ticker==4 自动切幕，鼠标指针移动到 #click2 位置做『打开开关』演示",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "AC_NAME_HERE / Use the service",
      "shown_text_zh": "PancakeSwap / 使用该服务",
      "user_action_requested": "演示把服务开关拨到开启（真实操作需用户到系统页完成，此处为动画）",
      "code_anchor": "assets/unique.html#step2 (L332-L385)"
    },
    {
      "step": 5,
      "stage": "引导说明页",
      "screen_or_component": "assets/unique.html #step3 —— 仿系统无障碍授权确认弹窗（semantic-ui modal）",
      "trigger_event": "ticker==2 自动切幕并 $('.ui.modal').modal('show')",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Allow functions \"AC_NAME_HERE\" full phone control / Viewing Information and Controlling Screen Operation — The app can read all the content on the screen and display the content on top of other apps. / Viewing Information and performing actions — An app can track interactions with apps or hardware sensors and interact with apps on your behalf. / Allow / Reject",
      "shown_text_zh": "允许「PancakeSwap」完全控制手机 / 查看信息并控制屏幕操作——该应用可读取屏幕全部内容并显示在其他应用之上 / 查看信息并执行操作——该应用可跟踪与其他应用或硬件传感器的交互，并代表你与其他应用交互 / 允许 / 拒绝",
      "user_action_requested": "点 Allow（#click3，指针自动移入演示）；Reject 为纯文本、未绑定任何事件，点了无反应",
      "code_anchor": "assets/unique.html#step3 (L387-L439)"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "assets/unique.html #step4 —— 'How you can grant rights to the application!' 页，含 Repeat training 与绿色 Give rights",
      "trigger_event": "ticker==0 时隐藏 modal 并显示 step4",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "How you can grant rights to the application! / Repeat training / Give rights",
      "shown_text_zh": "如何把权限授予该应用！/ 重看教学 / 授予权限",
      "user_action_requested": "点 Give rights 调 JS 桥 Android.finishInject()；点 Repeat training 仅 restart() 把 ticker 重置为 7，回到第 2 步循环教学，无任何『跳过/暂不』出口",
      "code_anchor": "assets/unique.html#step4 (L441-L452) 与 restart()/ticker 定时器"
    },
    {
      "step": 7,
      "stage": "跳无障碍设置",
      "screen_or_component": "JS 桥 Android.finishInject() → 原生侧跳转（预期为 ACTION_ACCESSIBILITY_SETTINGS，DEX 中无该常量与对应类，控制流在加密载荷内）",
      "trigger_event": "用户点击 Give rights 触发 WebView JavascriptInterface 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（离开 WebView 进入系统无障碍列表，列表项显示 PancakeSwap / Service allows Accessibility for Android to scan your device for accessibility issues.）",
      "shown_text_zh": "进入系统无障碍设置，服务名显示为 PancakeSwap，说明为『该服务允许 Android 无障碍功能扫描你设备上的无障碍问题』",
      "user_action_requested": "用户在真实系统页手动打开 PancakeSwap 服务开关（该页为系统页，不可伪造）",
      "code_anchor": "assets/unique.html onclick=\"Android.finishInject()\" / res/xml/accessibilityservice.xml / AndroidManifest.xml AppAccessibilityService"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.tapston.burgerking.service.AppAccessibilityService（typeAllMask, canRetrieveWindowContent, canPerformGestures）+ com.tapston.burgerking.service.OverlayService + NotificationService + MyAdminReceiver/AdminActivity + IgnoreBatteryOptimizationsActivity",
      "trigger_event": "系统 BIND_ACCESSIBILITY_SERVICE 绑定服务后 onServiceConnected（服务实现体不在可静态还原范围内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Accessibility service must be enabled to protect your data! / Allow pop-ups / Checking system / Checking",
      "shown_text_zh": "必须启用无障碍服务才能保护你的数据！/ 允许弹窗 / 正在检查系统 / 检查中",
      "user_action_requested": "预期继续索取悬浮窗、忽略电池优化、设备管理器等权限（对应 PermissionsActivity、IgnoreBatteryOptimizationsActivity、AdminActivity，具体顺序不可静态还原）",
      "code_anchor": "AndroidManifest.xml 组件声明 / res/values/strings.xml#str4,#miuipopup,#managing_service_title"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务标签 PancakeSwap（res/values/strings.xml accessibility_service_label），说明文字 'Service allows Accessibility for Android to scan your device for accessibility issues.'（@string/accessibility_service_description，res/xml/accessibilityservice.xml 引用）",
    "本地 WebView 页面 assets/unique.html：title 'Get Accessibility'，第 0 幕提示 'To work correctly, your application requires Accessibility rights...' 与按钮 'View training'",
    "assets/unique.html 第 1 幕：伪造的『设置-特殊能力/已安装服务/屏幕』列表页，服务名经 AC_NAME_HERE 替换为 PancakeSwap，状态 'Turned off'",
    "assets/unique.html 第 2 幕：伪造的服务详情页，'Use the service' 开关（#click2）",
    "assets/unique.html 第 3 幕：伪造的系统授权确认弹窗 'Allow functions \"AC_NAME_HERE\" full phone control' + Allow/Reject",
    "assets/unique.html 第 4 幕：'How you can grant rights to the application!' 页，Repeat training / Give rights 按钮",
    "页面内叠加的 SVG 鼠标指针动画（perlin 噪声驱动，自动移动到 #click1/#click2/#click3），以图形化『手指演示』替代文字说明",
    "res/values/strings.xml 中保留但需原生层调用的文案：enable_accessibility_title 'Update app accesses'、enable_accessibility_message 'Enable access for \"PancakeSwap\"'、str1-str4 三步教学、'Accessibility service must be enabled to protect your data!'、managing_service_title 'Checking system'、miuipopup 'Allow pop-ups'（原生弹窗/Toast/悬浮窗载体，控制流在加密载荷内）",
    "assets/chrome.html 与 assets/nointernet.html：配合 BrowserActivity（noHistory、全屏）使用的仿浏览器/断网页载体，用于承载后续钓鱼页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To work correctly, your application requires Accessibility rights. See how to make them.",
      "text_zh": "为了让应用正常工作，需要授予无障碍权限。看看该怎么做。",
      "source_location": "assets/unique.html#step0 loader1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "View training",
      "text_zh": "查看教学",
      "source_location": "assets/unique.html#step0 绿色按钮",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Special abilities",
      "text_zh": "特殊能力",
      "source_location": "assets/unique.html#step1 顶部固定菜单（仿系统辅助功能页标题）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Installed services / AC_NAME_HERE / Turned off",
      "text_zh": "已安装的服务 / PancakeSwap / 已关闭",
      "source_location": "assets/unique.html#step1 #click1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Use the service",
      "text_zh": "使用该服务",
      "source_location": "assets/unique.html#step2 #click2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow functions \"AC_NAME_HERE\" full phone control",
      "text_zh": "允许「PancakeSwap」完全控制手机",
      "source_location": "assets/unique.html#step3 伪系统授权弹窗标题",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Viewing Information and Controlling Screen Operation — The app can read all the content on the screen and display the content on top of other apps.",
      "text_zh": "查看信息并控制屏幕操作——该应用可以读取屏幕上的全部内容，并把内容显示在其他应用之上。",
      "source_location": "assets/unique.html#step3 能力说明第 1 条",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Viewing Information and performing actions — An app can track interactions with apps or hardware sensors and interact with apps on your behalf.",
      "text_zh": "查看信息并执行操作——该应用可以跟踪你与其他应用或硬件传感器的交互，并代表你与其他应用交互。",
      "source_location": "assets/unique.html#step3 能力说明第 2 条",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "How you can grant rights to the application! / Repeat training / Give rights",
      "text_zh": "如何把权限授予该应用！/ 重看教学 / 授予权限",
      "source_location": "assets/unique.html#step4",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service must be enabled to protect your data!",
      "text_zh": "必须启用无障碍服务才能保护你的数据！",
      "source_location": "res/values/strings.xml key=str4",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Update app accesses",
      "text_zh": "更新应用访问权限",
      "source_location": "res/values/strings.xml key=enable_accessibility_title",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable access for \"PancakeSwap\"",
      "text_zh": "为「PancakeSwap」启用访问权限",
      "source_location": "res/values/strings.xml key=enable_accessibility_message",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Checking system / Checking",
      "text_zh": "正在检查系统 / 检查中",
      "source_location": "res/values/strings.xml key=managing_service_title, managing_service_message",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Open the Accessibility settings  2. Select Enable Accessibility Service  3. Slide the switch to enable",
      "text_zh": "1. 打开无障碍设置  2. 选择『启用无障碍服务』  3. 滑动开关以启用",
      "source_location": "res/values/strings.xml key=str1,str2,str3",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "text_zh": "该服务允许 Android 无障碍功能扫描你设备上的无障碍问题。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（由 res/xml/accessibilityservice.xml android:description 引用，显示于系统无障碍服务列表）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility Insights for Android to scan your device for accessibility issues",
      "text_zh": "该服务允许 Android 无障碍洞察功能扫描你设备上的无障碍问题",
      "source_location": "res/values/strings.xml key=accessibility_insights_service_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow pop-ups",
      "text_zh": "允许弹窗",
      "source_location": "res/values/strings.xml key=miuipopup（MIUI 悬浮窗权限引导文案）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "HTML 层无任何取消/跳过出口：step3 的 Reject 为未绑定事件的纯文本，点击无反应；step4 的 Repeat training 仅把 ticker 重置为 7，重新播放整套教学并再次走到 Give rights；ticker 每 1 秒自动递减强制翻页，用户无法停留在中间页。原生层是否在 onResume 检测未获权后再次拉起 AccessibilityGuideActivity 属于加密载荷内逻辑，本次不可静态还原。",
    "overlay_or_fake_settings": "有。assets/unique.html 内含高仿系统无障碍『特殊能力/已安装服务』列表页、高仿服务详情开关页以及高仿系统授权确认弹窗（Allow/Reject）；另声明 com.tapston.burgerking.service.OverlayService 与 SYSTEM_ALERT_WINDOW/ACTION_MANAGE_OVERLAY_PERMISSION 权限，用于在真实系统页之上叠加半透明引导窗（叠加时机与内容不可静态还原）；SVG 鼠标指针以噪声动画模拟手指在伪设置页上自动点击。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "不可静态还原（服务实现体与 onResume 逻辑不在 DEX 内；但已声明 MyAdminReceiver/BIND_DEVICE_ADMIN、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED + BootReceiver、AlarmBroadcastReceiver、NotificationService，具备抗撤权/自启动的组件基础）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动点击图标后，监测到 Theme.Light.NoTitleBar.Fullscreen 且非系统包的全屏 Activity（预期为 com.tapston.burgerking.ui.AccessibilityGuideActivity / ui.accesses.AccessibilityActivity）出现并承载 WebView 的瞬间立即拉起 UTG；次优触发点为监测到 Android.finishInject() 后跳转 android.settings.ACCESSIBILITY_SETTINGS，以及之后 SYSTEM_ALERT_WINDOW 类型的 OverlayService 悬浮窗出现时。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后第一步教学提示页（step0 loader1）",
        "page_identifier": "全屏无标题栏 WebView，标题 'Get Accessibility'，正文含 'your application requires Accessibility rights'，单个绿色按钮 'View training'",
        "why_most_useful": "这是整个诱导链的起点，能证明应用一启动就以『需要无障碍权限才能正常工作』为前置条件，且界面上不存在跳过/取消按钮",
        "observable_utg_signals": ["无跳过/取消控件，仅单个 View training 按钮", "文案包含 Accessibility rights 与 See how to make them", "页面为本地 assets 加载（URL 为 file:///android_asset/unique.html 或空 referer）"]
      },
      {
        "page_role": "高仿系统无障碍设置页（step1/step2）",
        "page_identifier": "WebView 内渲染出 'Special abilities' 标题、'Installed services' 分组、服务项显示为 PancakeSwap 且状态 'Turned off'，随后切到 'Use the service' 开关页",
        "why_most_useful": "这是区分『正常引导用户去系统设置』与『伪造系统界面欺骗用户』的决定性证据：真实系统页不会出现在应用 WebView 内，且不会由应用自己渲染 PancakeSwap 服务条目",
        "observable_utg_signals": ["页面由应用进程 WebView 渲染而非系统设置（无 com.android.settings 包名）", "出现 'Installed services'、'Turned off' 等系统页同款字段", "存在自动移动的 SVG 鼠标指针叠加元素"]
      },
      {
        "page_role": "伪造系统授权确认弹窗（step3）",
        "page_identifier": "WebView 内 modal：'Allow functions \"PancakeSwap\" full phone control'，两条能力说明 + 'Allow' / 'Reject'",
        "why_most_useful": "证明应用伪造系统级授权确认框，并刻意让 Reject 失效（点击无响应），构成无退出路径的同意压迫",
        "observable_utg_signals": ["Reject 文本无可点击属性/点击后界面无变化", "弹窗文案与系统无障碍授权页原文高度一致但位于应用 WebView 内", "弹窗出现后 1 秒内自动被 step4 覆盖，用户无操作窗口"]
      },
      {
        "page_role": "设置页后的悬浮遮罩引导窗",
        "page_identifier": "TYPE_APPLICATION_OVERLAY / TYPE_SYSTEM_ALERT 窗口，由 com.tapston.burgerking.service.OverlayService 创建，覆盖在 android.settings.ACCESSIBILITY_SETTINGS 之上",
        "why_most_useful": "用于确认应用在真实系统页之上叠加遮罩/引导，是『遮罩叠层指引』这一强制手段的直接运行期证据",
        "observable_utg_signals": ["顶层窗口包名为 com.card.gift 且窗口类型为系统悬浮窗", "系统无障碍设置页被非系统窗口遮挡", "悬浮窗内文本指向 PancakeSwap 服务开关位置"]
      },
      {
        "page_role": "系统无障碍服务列表项（真实系统页）",
        "page_identifier": "com.android.settings 无障碍列表中出现条目 'PancakeSwap'，副标题 'Service allows Accessibility for Android to scan your device for accessibility issues.'",
        "why_most_useful": "核对系统侧实际呈现的服务名与说明是否与显示名一致、是否借用系统自检话术掩盖真实读屏/代点能力",
        "observable_utg_signals": ["服务标签 PancakeSwap 与包名 com.card.gift 不一致", "description 使用『scan your device for accessibility issues』话术", "服务项未标注为系统无障碍工具"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两类盲区：其一，Java 侧控制流不在 DEX 中（classes.dex/classes2.dex 检索不到 tapston、AccessibilityService、ACTION_ACCESSIBILITY_SETTINGS、unique.html 等字符串，业务类整体缺席，仅剩 com.card.gift 桩类与 com.cow.inject 注入工具），故『哪个 Activity 加载 unique.html、finishInject 如何跳设置、onResume 是否死循环重跳、获权后是否自点确认或阻止撤权』必须靠运行期 UTG 观测补齐；其二，assets/gXQDo.json（2.3MB）与 EncryptorService 疑似加密载荷，若真实恶意面板与云控只在解密后出现，纯静态与单次 UTG 均可能只见『温和外壳』。另注意页面会通过 Google Translate 脚本按系统语言把自身机翻为俄语（googtrans=/ru/），UTG 文本采集需兼容多语言匹配。"
  },
  "behavior_pattern_tags": [
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "AndroidManifest.xml: service com.tapston.burgerking.service.AppAccessibilityService (android:label=@string/app_name, android:permission=BIND_ACCESSIBILITY_SERVICE, meta-data android.accessibilityservice=@xml/accessibilityservice)",
    "res/xml/accessibilityservice.xml: android:description=@string/accessibility_service_description, accessibilityEventTypes=typeAllMask, flags=flagDefault|flagIncludeNotImportantViews|flagReportViewIds|flagRequestTouchExplorationMode, canRetrieveWindowContent=true, canPerformGestures=true",
    "res/values/strings.xml: accessibility_service_label/app_name=PancakeSwap, enable_accessibility_title='Update app accesses', enable_accessibility_message, str1-str4, managing_service_title='Checking system', miuipopup='Allow pop-ups'",
    "assets/unique.html#step0-step4（L77-L452）：伪造无障碍设置五幕流程 + AC_NAME_HERE 占位替换",
    "assets/unique.html onclick=\"Android.finishInject()\"（step4 Give rights 按钮）与 restart()/ticker 定时器",
    "AndroidManifest.xml: com.tapston.burgerking.ui.AccessibilityGuideActivity / ui.accesses.AccessibilityActivity / ui.BrowserActivity / service.OverlayService / service.EncryptorService"
  ]
}
```

</details>
