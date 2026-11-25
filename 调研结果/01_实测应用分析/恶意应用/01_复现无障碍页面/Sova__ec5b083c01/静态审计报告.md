# MB_124__ec5b083c01｜Sova — Tinder Platinum

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：139.6s

## 1. 一句话核心结论

- **核心申请方式**：应用以 Tinder Platinum 为外壳、以伪装成 Chrome 更新的本地 HTML 分步教学 + 整屏红色悬浮遮罩 + 谎称无障碍检测工具的受限设置页，诱导用户手动开启一个可读窗口内容并模拟手势的无障碍服务。
- **静态可见性说明**：Manifest 声明的全部业务组件 com.tapston.burgerking.*（AppAccessibilityService、AccessibilityGuideActivity、BrowserActivity、AccessibilityActivity、OverlayService、AdminActivity 等）在两个 DEX 中均无字符串命中（com/tapston=0），业务实现位于二阶段：Application 类 com.royal.bottom.PTyXaWpQsLzAgLtHnRlMnLgZlTxGlYrYeGaDwTyGlOjNwNyTbUjYjUf 在 attachBaseContext 中经 unhappybaby/afraidpupil/acquirenotable/flipevoke 解密字符串并使用 DexClassLoader，配合 2.29MB 加密资产 assets/TWfA.json。因此跳转 Intent、拒权循环定时器、获权后自保等 Java 逻辑不可静态还原；但 Manifest 组件/主题、res/layout（guide_layout、access_push）、res/xml/accessibilityservice.xml、strings.xml 与 assets/chrome.html、unique.html 明文可见，引导链形态可确证。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ec5b083c017570f846f6925b7c79d9e5886525a9b7ba7e514dabad0325c0af5e` |
| 包名 / 年份 | `com.royal.bottom` / 2023 |
| 家族 / 品类 | **Sova**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Tinder Platinum |
| 引导页宣称品牌/身份 | Tinder Platinum（同时伪装 Google Chrome 浏览器更新与 Accessibility Insights 无障碍检测工具） |
| 系统无障碍列表服务名 | Tinder Platinum |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.royal.bottom 与显示名/服务名 Tinder Platinum 完全无关；无障碍服务 description 直接冒用官方工具话术 'Service allows Accessibility for Android to scan your device for accessibility issues.'（另有 accessibility_insights_service_description 仿 Accessibility Insights）；本地 HTML 伪装 Chrome 更新成功页（'The browser has been updated successfully'）；AndroidManifest 声明多个全屏/半透明/无标题 Activity（BlankActivity、AdminActivity Theme.Translucent、BrowserActivity excludeFromRecents）及单实例 LauncherActivity 以隐藏真实流程；Application 类名为随机大小写长串（PTyXaWpQsLzAgLtHnRlMnLgZlTxGlYrYeGaDwTyGlOjNwNyTbUjYjUf）并对全部字符串做解密以规避静态检测；服务实际能力（canRetrieveWindowContent + canPerformGestures + typeAllMask + flagRequestTouchExplorationMode）远超其声明的'扫描无障碍问题'。 |
| 无障碍服务类名 | `com.tapston.burgerking.service.AppAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Service allows Accessibility for Android to scan your device for accessibility issues. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tapston.burgerking.ui.LauncherActivity（MAIN/LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen，singleInstance，noHistory） | 用户点击桌面图标（ACTION_MAIN/LAUNCHER） | 原生Activity | **原文**：无（半透明无标题全屏，自身不呈现文案）<br>**译注**：无可见界面，静默决定后续路由 | 无（用户仅看到桌面点击动作） | `AndroidManifest.xml: com.tapston.burgerking.ui.LauncherActivity` |
| 2 | 引导说明页 | com.tapston.burgerking.ui.AccessibilityGuideActivity + res/layout/guide_layout.xml | LauncherActivity 跳转（onCreate/onResume，实现位于加密二阶段） | 原生Activity | **原文**：Tinder Platinum / 1. Open the Accessibility settings / 2. Select Enable Accessibility Service / Accessibility service must be enabled to protect your data! / OK<br>**译注**：标题为应用名 Tinder Platinum；步骤一“打开无障碍设置”；步骤二“选择启用无障碍服务”；“必须启用无障碍服务才能保护你的数据！”；唯一按钮 OK | 仅能点击 OK 继续（布局中只有 ok_button，无取消/跳过/关闭） | `res/layout/guide_layout.xml; res/values/strings.xml: app_name, str1, str2, str4, enable_accessibility_title(Update app accesses), enable_accessibility_message` |
| 3 | 引导说明页 | com.tapston.burgerking.ui.BrowserActivity（noHistory、excludeFromRecents、全屏）内 WebView 加载本地 HTML | 引导页 OK 或后台配置触发 WebView 加载 assets/chrome.html 或 assets/unique.html | 本地HTML WebView | **原文**：Welcome to Chrome / The browser has been updated successfully / To use this application, click on the "Continue" button and then enable the Chrome services. / Open settings / Select Accessibility / Slide the switch to enable / CONTINUE<br>**译注**：“欢迎使用 Chrome / 浏览器已成功更新 / 要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务 / 打开设置 / 选择无障碍 / 滑动开关以启用 / 继续” | 点击 CONTINUE（触发 JS 桥 Android.finishInject()）后按 OEM 定制路径手动操作设置 | `assets/chrome.html L251-L277, L306-L348（m1~m8 文案与 oppo/xiaomi/samsung/huawei/honor 分支）, L351-L357 多语言表` |
| 4 | 引导说明页 | 同 BrowserActivity 加载 assets/unique.html（Get Accessibility 页 + 高仿系统设置页 step1） | 另一引导分支（ticker=7 倒计时 / View training 点击） | 本地HTML WebView | **原文**：Get Accessibility / To work correctly, your application requires Accessibility rights. See how to make them. / View training / Special abilities / Volume buttons / Disabled<br>**译注**：“获取无障碍权限 / 为使应用正常工作，需要无障碍权限。查看如何开启 / 查看教程 / 特殊能力 / 音量键 / 已禁用” | 点击 View training 观看分步教程（页内另有倒计时 ticker 推进） | `assets/unique.html L3, L92-L104, L107-L145` |
| 5 | 跳受限设置 | 系统设置：无障碍（ACTION_ACCESSIBILITY_SETTINGS）或应用详情（ACTION_APPLICATION_DETAILS_SETTINGS） | WebView JS 桥 Android.finishInject() 回调或 AccessibilityActivity（exported、Theme.Light.NoTitleBar.Fullscreen、noHistory）启动 Intent | 系统无障碍页 | **原文**：无（由系统设置页呈现）<br>**译注**：跳转目标为系统无障碍服务列表，需用户在其中找到 Tinder Platinum 并开启 | 在系统列表中定位并打开服务开关（OEM 路径由 HTML 预先教学） | `AndroidManifest.xml: com.tapston.burgerking.ui.accesses.AccessibilityActivity / BrowserActivity; 跳转 Intent 实现位于加密二阶段 DEX` |
| 6 | 遮罩叠层指引 | com.tapston.burgerking.service.OverlayService + res/layout/access_push.xml（SYSTEM_ALERT_WINDOW） | 悬浮窗服务启动后在系统设置页之上叠加（触发时机实现位于加密二阶段） | 悬浮窗Overlay | **原文**：Accessibility service must be enabled to protect your data! / OK<br>**译注**：“必须启用无障碍服务才能保护你的数据！” + 应用图标 + OK 按钮，整屏红色背景（#ffff0000） | 按遮罩提示回到开关并开启（遮罩覆盖设置界面形成强指引/干扰） | `res/layout/access_push.xml; AndroidManifest.xml: com.tapston.burgerking.service.OverlayService` |
| 7 | 拒权反馈循环 | AccessibilityGuideActivity / AccessibilityActivity（均 noHistory）重复拉起 | 用户返回或未开启开关时再次进入引导（推测为 onResume/定时器，实现不可静态还原） | 不可静态还原 | **原文**：Accessibility service must be enabled to protect your data!<br>**译注**：重复以“不开启就无法保护数据”施压，且引导页无取消入口 | 被迫再次前往设置开启；未见安全降级或跳过路径 | `AndroidManifest.xml: AccessibilityGuideActivity(noHistory) / AccessibilityActivity(noHistory, exported); 循环逻辑位于加密二阶段` |
| 8 | 获权后动作 | com.tapston.burgerking.service.AppAccessibilityService（typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRequestTouchExplorationMode） | 用户在系统设置中启用该服务后由系统绑定 | 不可静态还原 | 无 | 无（后台静默执行） | `res/xml/accessibilityservice.xml; AndroidManifest.xml: com.tapston.burgerking.service.AppAccessibilityService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务标签 'Tinder Platinum'，android:description = 'Service allows Accessibility for Android to scan your device for accessibility issues.'（res/values/strings.xml: accessibility_service_label / accessibility_service_description）
- 原生全屏引导页 AccessibilityGuideActivity：guide_layout.xml 中 TextView @string/app_name、str0~str3 与唯一 OK 按钮（无取消）
- 本地 WebView 教学页 assets/chrome.html：伪装 Chrome 更新成功页 + OEM 定制分步教学 + CONTINUE 按钮（多语言经 translate.googleapis.com 在线翻译）
- 本地 WebView 页 assets/unique.html：Get Accessibility 提示 + View training 按钮 + step1 高仿系统设置页（Special abilities / Volume buttons Disabled）
- 悬浮窗遮罩 OverlayService 加载 access_push.xml：整屏红色背景 + 应用图标 + 'Accessibility service must be enabled to protect your data!' + OK
- strings.xml 预留但需二阶段调用的文案：enable_accessibility_title 'Update app accesses'、enable_accessibility_message 'Enable access for "Tinder Platinum"'、str4 'Accessibility service must be enabled to protect your data!'
- Manifest 声明的辅助跳转/掩护页面：BlankActivity、AdminActivity（Theme.Translucent）、PermissionsActivity（Theme.Translucent）、IgnoreBatteryOptimizationsActivity、XiaomiLoadActivity

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Service allows Accessibility for Android to scan your device for accessibility issues. | 该服务允许 Android 的无障碍功能扫描你设备上的无障碍问题。 | `res/values/strings.xml: accessibility_service_description（被 res/xml/accessibilityservice.xml 引用）` | 清理工具伪装 |
| en | Welcome to Chrome | 欢迎使用 Chrome | `assets/chrome.html (objLang/默认文案, L351-L357)` | 假更新 |
| en | The browser has been updated successfully | 浏览器已成功更新。 | `assets/chrome.html (objLang updated 字段, L351-L353)` | 假更新 |
| en | To use this application, click on the "Continue" button and then enable the Chrome services. | 要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务。 | `assets/chrome.html (manual0 文案, L351-L357)` | 受限设置分步教学 |
| en | Open settings | 打开设置 | `assets/chrome.html L262, L306 (const m1)` | 受限设置分步教学 |
| en | Select Accessibility | 选择无障碍 | `assets/chrome.html L266, L307 (const m2)` | 受限设置分步教学 |
| en | Slide the switch to enable | 滑动开关以启用 | `assets/chrome.html L270, L308 (const m3)` | 受限设置分步教学 |
| en | Go to Installed apps | 前往已安装的应用 | `assets/chrome.html L312 (const m6，samsung 分支)` | 受限设置分步教学 |
| en | Find and enable | 找到并启用（后接包名） | `assets/chrome.html L310 (const m5，samsung/huawei 分支)` | 受限设置分步教学 |
| en | Go to Accessibility features | 前往无障碍功能 | `assets/chrome.html L313 (const m7，huawei/honor 分支)` | 受限设置分步教学 |
| en | CONTINUE | 继续 | `assets/chrome.html L277（onclick="Android.finishInject();"）` | 受限设置分步教学 |
| en | Get Accessibility | 获取无障碍权限 | `assets/unique.html L3 (<title>)` | 受限设置分步教学 |
| en | To work correctly, your application requires Accessibility rights. See how to make them. | 为使应用正常工作，需要无障碍权限。查看如何开启。 | `assets/unique.html L97` | 受限设置分步教学 |
| en | View training | 查看教程 | `assets/unique.html L101（onclick="javascript: ticker=7;"）` | 受限设置分步教学 |
| en | Accessibility service must be enabled to protect your data! | 必须启用无障碍服务才能保护你的数据！ | `res/values/strings.xml: str4（用于 res/layout/access_push.xml 悬浮遮罩）` | 故障恐吓 |
| en | Update app accesses | 更新应用访问权限 | `res/values/strings.xml: enable_accessibility_title` | 假更新 |
| en | Enable access for "Tinder Platinum" | 为“Tinder Platinum”启用访问权限 | `res/values/strings.xml: enable_accessibility_message` | 受限设置分步教学 |
| en | 1. Open the Accessibility settings | 1. 打开无障碍设置 | `res/values/strings.xml: str1（guide_layout.xml 中 @id/str1）` | 受限设置分步教学 |
| en | 2. Select Enable Accessibility Service | 2. 选择“启用无障碍服务” | `res/values/strings.xml: str2（guide_layout.xml 中 @id/str2）` | 受限设置分步教学 |
| fr | Bienvenue à Chrome / Le navigateur a été mis à jour avec succès / Pour utiliser cette application, cliquez sur le bouton "Continuer", puis activez les services Chrome. / Faites glisser l'interrupteur pour activer | 欢迎使用 Chrome / 浏览器已成功更新 / 要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务 / 滑动开关以启用 | `assets/chrome.html L353 (objLang.fr)` | 假更新 |
| es | Bienvenido a Chrome / El navegador se ha actualizado correctamente / Seleccione la accesibilidad | 欢迎使用 Chrome / 浏览器已正确更新 / 选择无障碍 | `assets/chrome.html L351 (objLang.es)` | 假更新 |
| hu | Üdvözöljük a Chrome-ban / A böngésző sikeresen frissült / Válassza a Hozzáférhetőséget | 欢迎使用 Chrome / 浏览器已成功更新 / 选择无障碍 | `assets/chrome.html L355 (objLang.hu)` | 假更新 |
| el | Καλώς ήρθατε στο Chrome / Το πρόγραμμα περιήγησης ενημερώθηκε επιτυχώς / Επιλέξτε Προσβασιμότητα | 欢迎使用 Chrome / 浏览器已成功更新 / 选择无障碍 | `assets/chrome.html L357 (objLang.el)` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：AccessibilityGuideActivity 与 AccessibilityActivity 均声明 android:noHistory="true"，且 guide_layout.xml 只提供单一 ok_button，无取消/跳过/返回控件；LauncherActivity 为 singleInstance+translucent，用户无法在应用内“留在本页”。拒权或从系统设置返回后的具体重跳逻辑（onResume 死循环或定时器拉起）位于加密二阶段 DEX，静态不可确认，但组件声明已排除良性降级入口。
- **遮罩叠层 / 高仿系统设置页**：是：OverlayService（SYSTEM_ALERT_WINDOW）加载 access_push.xml 整屏红色（#ffff0000）遮罩，叠在系统设置页之上，内容为应用图标 + 'Accessibility service must be enabled to protect your data!' + OK；另 assets/unique.html 的 step1 直接绘制高仿系统设置界面（Special abilities / Volume buttons Disabled）；assets/chrome.html 伪装 Chrome 更新页。
- **Android 13+ 受限设置（Restricted Settings）应对**：未发现针对 Android 13 受限设置的“应用详情→右上角菜单→允许受限设置”教学或 Session 安装器绕过（应用 targetSdkVersion=32，HTML 教学仅为各 OEM 的无障碍入口路径）
- **获权后即时行为与防撤权机制**：未在静态可见层确认（无 GLOBAL_ACTION_BACK/HOME 拦截、无自授权代码可读）；但应用同时声明 DeviceAdmin（MyAdminReceiver + res/xml/admin）、NotificationListenerService、BootReceiver 与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，抗撤权/抗卸载能力需在二阶段还原后判定
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条并行钩子：①监测到以 FLAG_ACTIVITY_NEW_TASK 拉起 Settings.ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间立即截屏/取 UTG（此时 OverlayService 遮罩通常已在压栈中）；②冷启动后 0-3 秒内 AccessibilityGuideActivity（Theme.Light.NoTitleBar.Fullscreen）或 BrowserActivity（excludeFromRecents 全屏 WebView）出现在顶层时立刻抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在盲区：①业务组件全部由二阶段 DexClassLoader 从加密资产 assets/TWfA.json 加载，跳转 Intent、拒权循环与获权后动作无法静态阅读，UTG 只能捕捉表现不能替代代码证据；②若远端下发开关关闭引导链，运行期可能完全不弹页面（纯云控门控），单次运行可能出现“无异常”假阴性；③引导文案经 translate.googleapis.com 在线翻译，界面文字随设备语言变化，UTG 文本匹配需按多语言归一；④应用声明 Theme.Translucent 的 AdminActivity/BlankActivity 与 noHistory 全屏页，可能在 UTG 采样间隙快速切换，需要高频采样。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动原生引导页** | com.tapston.burgerking.ui.AccessibilityGuideActivity，全屏浅色无标题，含应用图标 + 'Tinder Platinum' + 两行编号步骤 + 唯一 OK 按钮 | 这是应用自己承认的引导入口，且布局中不存在取消按钮，可直接证明“无跳过路径”的强制引导形态 | 文本节点 'Tinder Platinum' 与 'Open the Accessibility settings'/'Select Enable Accessibility Service'；仅存在 1 个可点击按钮 ok_button，无 Cancel/Skip/Close 节点；Activity 类名 AccessibilityGuideActivity 与无标题全屏窗口属性 |
| **跳转前 WebView 教学页（伪装 Chrome 更新）** | com.tapston.burgerking.ui.BrowserActivity 内的 WebView，页面标题/正文含 'Welcome to Chrome'、'The browser has been updated successfully'、三步教学与 CONTINUE 按钮 | 假更新话术 + OEM 定制无障碍路径教学同时出现，是“假更新诱导开启无障碍”的核心铁证，可区分普通权限说明与伪装欺骗 | WebView 节点中的 'Welcome to Chrome' / 'updated successfully'；步骤文本 'Open settings' → 'Select Accessibility' → 'Slide the switch to enable'；CONTINUE 按钮及其触发的 finishInject JS 桥（可配合 WebView 调试观察）；URL 含 model 与 pkgname 参数 |
| **设置页之上压栈的红色悬浮遮罩** | TYPE_APPLICATION_OVERLAY 窗口，整屏红色背景 + 应用图标 + 'Accessibility service must be enabled to protect your data!' + OK | 证明应用在用户即将操作系统开关时叠加恐吓遮罩，属于典型的遮罩叠层施压而非透明说明 | 窗口层级中出现与 Settings 同屏的非系统 overlay 窗口；红色背景块 + 该恐吓文案文本节点；当前前台为 com.android.settings 但顶层可点击区域被 overlay 覆盖 |
| **系统无障碍服务列表项** | Settings → Accessibility 中名为 'Tinder Platinum' 的服务条目，副标题为 'Service allows Accessibility for Android to scan your device for accessibility issues.' | 核对服务名与描述的身份冒用（Tinder 品牌 + 无障碍检测工具话术），与包名 com.royal.bottom 形成身份矛盾 | 条目文本 'Tinder Platinum'；描述文本 'scan your device for accessibility issues'；条目对应的包名 com.royal.bottom |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.tapston.burgerking.service.AppAccessibilityService（AndroidManifest.xml，label=@string/app_name，meta-data=@xml/accessibilityservice）`
- `com.tapston.burgerking.ui.AccessibilityGuideActivity + res/layout/guide_layout.xml（仅 ok_button，无取消）`
- `com.tapston.burgerking.ui.BrowserActivity + assets/chrome.html（L251-L277 教学步骤 / L306-L348 OEM 分支 / L351-L357 多语言）`
- `assets/unique.html（L3 Get Accessibility / L92-L104 View training + ticker=7 / L107-L145 高仿设置页）`
- `com.tapston.burgerking.service.OverlayService + res/layout/access_push.xml（整屏红色遮罩 + str4 恐吓文案）`
- `com.royal.bottom.PTyXaWpQsLzAgLtHnRlMnLgZlTxGlYrYeGaDwTyGlOjNwNyTbUjYjUf#attachBaseContext（字符串解密 + DexClassLoader 二阶段加载，配合 assets/TWfA.json）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向审计结论（围绕“引导开启无障碍”的运行期页面流转）

**可见性判断：`packed_or_encrypted`。** 关键证据：Manifest 声明的全部业务组件（`com.tapston.burgerking.*`，含无障碍服务、引导 Activity、OverlayService）在两个 DEX 中**均无任何字符串命中**（`com/tapston` 命中 0，`com/royal/bottom` 命中 589），而 `Application` 类 [PTyXaWpQsLzAgLtHnRlMnLgZlTxGlYrYeGaDwTyGlOjNwNyTbUjYjUf](<resource-unit:#1.dex1 code:com.royal.bottom.PTyXaWpQsLzAgLtHnRlMnLgZlTxGlYrYeGaDwTyGlOjNwNyTbUjYjUf#attachBaseContext>) 在 `attachBaseContext` 中做 `unhappybaby/afraidpupil/acquirenotable/flipevoke` 字符串解密并出现 `DexClassLoader`，配合 2.29 MB 加密资产 [assets/TWfA.json](<resource-unit:#1 file:assets/TWfA.json>) 构成二阶段加载。因此**页面流转的 Java 实现不可静态还原**，但 Manifest 组件声明、`res/` 布局、`strings.xml` 与本地 HTML 完整暴露了引导链的形态。

**可确证的行为链（资源/声明层）**
1. 冷启动入口为 [LauncherActivity](<resource-unit:#1 manifest:components>)（`LAUNCHER`、`Theme.Translucent.NoTitleBar.Fullscreen`、`singleInstance`、`noHistory`）——本身无可见界面，静默跳转。
2. 原生引导页 `AccessibilityGuideActivity` 使用 [guide_layout.xml](<resource-unit:#1 file:res/layout/guide_layout.xml>)：图标 + `@string/app_name`（= **Tinder Platinum**）+ `str0~str3` 步骤文本 + **仅一个 OK 按钮，无取消/跳过**。
3. 跳设置前的“教学页”由 `BrowserActivity`（`excludeFromRecents`、全屏）加载本地 HTML：
   - [assets/chrome.html](<resource-unit:#1 file:assets/chrome.html#L251-L277>) 伪装“Chrome 已成功更新”，分步教学 `Open settings → Select Accessibility → Slide the switch to enable`，按 OEM 下发不同路径（oppo/xiaomi→“Installed apps”+包名；samsung→“Accessibility”→“Installed apps”；huawei/honor→“Accessibility features”），`CONTINUE` 触发 JS 桥 `Android.finishInject()`；文本通过 `translate.googleapis.com` 在线翻译成用户语言。
   - [assets/unique.html](<resource-unit:#1 file:assets/unique.html#L92-L104>) 标题 `Get Accessibility`，正文 “To work correctly, your application requires Accessibility rights.”，`View training` 按钮（`ticker=7` 倒计时），后续 `step1` 高仿系统设置页（`Special abilities` / `Volume buttons Disabled`）。
4. 系统无障碍列表项由 [accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml>) 定义：`typeAllMask`、`flagIncludeNotImportantViews`、`flagReportViewIds`、`flagRequestTouchExplorationMode`、`canRetrieveWindowContent=true`、`canPerformGestures=true`；`android:description` 谎称为 “scan your device for accessibility issues”（仿 Accessibility Insights 工具），标签为 **Tinder Platinum**。
5. 设置页遮罩由 `OverlayService` + [access_push.xml](<resource-unit:#1 file:res/layout/access_push.xml>)（整屏红色 `#ffff0000` + 应用图标 + 恐吓文案 + OK）承担。
6. 拒权反馈循环、获权后自保等动作位于加密二阶段，静态不可确认，如实标注为缺口。

**关键伪装点**：包名 `com.royal.bottom` / 品牌宣称 “Tinder Platinum” / 服务描述仿无障碍检测工具 / HTML 伪装 Chrome 更新——四层身份彼此不一致，且无障碍能力（读窗口+手势）远超“扫描无障碍问题”的声明范围。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest 声明的全部业务组件 com.tapston.burgerking.*（AppAccessibilityService、AccessibilityGuideActivity、BrowserActivity、AccessibilityActivity、OverlayService、AdminActivity 等）在两个 DEX 中均无字符串命中（com/tapston=0），业务实现位于二阶段：Application 类 com.royal.bottom.PTyXaWpQsLzAgLtHnRlMnLgZlTxGlYrYeGaDwTyGlOjNwNyTbUjYjUf 在 attachBaseContext 中经 unhappybaby/afraidpupil/acquirenotable/flipevoke 解密字符串并使用 DexClassLoader，配合 2.29MB 加密资产 assets/TWfA.json。因此跳转 Intent、拒权循环定时器、获权后自保等 Java 逻辑不可静态还原；但 Manifest 组件/主题、res/layout（guide_layout、access_push）、res/xml/accessibilityservice.xml、strings.xml 与 assets/chrome.html、unique.html 明文可见，引导链形态可确证。",
  "summary_one_liner": "应用以 Tinder Platinum 为外壳、以伪装成 Chrome 更新的本地 HTML 分步教学 + 整屏红色悬浮遮罩 + 谎称无障碍检测工具的受限设置页，诱导用户手动开启一个可读窗口内容并模拟手势的无障碍服务。",
  "disguise_identity": {
    "app_display_name": "Tinder Platinum",
    "claimed_brand_or_persona": "Tinder Platinum（同时伪装 Google Chrome 浏览器更新与 Accessibility Insights 无障碍检测工具）",
    "a11y_service_label": "Tinder Platinum",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.royal.bottom 与显示名/服务名 Tinder Platinum 完全无关；无障碍服务 description 直接冒用官方工具话术 'Service allows Accessibility for Android to scan your device for accessibility issues.'（另有 accessibility_insights_service_description 仿 Accessibility Insights）；本地 HTML 伪装 Chrome 更新成功页（'The browser has been updated successfully'）；AndroidManifest 声明多个全屏/半透明/无标题 Activity（BlankActivity、AdminActivity Theme.Translucent、BrowserActivity excludeFromRecents）及单实例 LauncherActivity 以隐藏真实流程；Application 类名为随机大小写长串（PTyXaWpQsLzAgLtHnRlMnLgZlTxGlYrYeGaDwTyGlOjNwNyTbUjYjUf）并对全部字符串做解密以规避静态检测；服务实际能力（canRetrieveWindowContent + canPerformGestures + typeAllMask + flagRequestTouchExplorationMode）远超其声明的'扫描无障碍问题'。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tapston.burgerking.ui.LauncherActivity（MAIN/LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen，singleInstance，noHistory）",
      "trigger_event": "用户点击桌面图标（ACTION_MAIN/LAUNCHER）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（半透明无标题全屏，自身不呈现文案）",
      "shown_text_zh": "无可见界面，静默决定后续路由",
      "user_action_requested": "无（用户仅看到桌面点击动作）",
      "code_anchor": "AndroidManifest.xml: com.tapston.burgerking.ui.LauncherActivity"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.tapston.burgerking.ui.AccessibilityGuideActivity + res/layout/guide_layout.xml",
      "trigger_event": "LauncherActivity 跳转（onCreate/onResume，实现位于加密二阶段）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Tinder Platinum / 1. Open the Accessibility settings / 2. Select Enable Accessibility Service / Accessibility service must be enabled to protect your data! / OK",
      "shown_text_zh": "标题为应用名 Tinder Platinum；步骤一“打开无障碍设置”；步骤二“选择启用无障碍服务”；“必须启用无障碍服务才能保护你的数据！”；唯一按钮 OK",
      "user_action_requested": "仅能点击 OK 继续（布局中只有 ok_button，无取消/跳过/关闭）",
      "code_anchor": "res/layout/guide_layout.xml; res/values/strings.xml: app_name, str1, str2, str4, enable_accessibility_title(Update app accesses), enable_accessibility_message"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.tapston.burgerking.ui.BrowserActivity（noHistory、excludeFromRecents、全屏）内 WebView 加载本地 HTML",
      "trigger_event": "引导页 OK 或后台配置触发 WebView 加载 assets/chrome.html 或 assets/unique.html",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Welcome to Chrome / The browser has been updated successfully / To use this application, click on the \"Continue\" button and then enable the Chrome services. / Open settings / Select Accessibility / Slide the switch to enable / CONTINUE",
      "shown_text_zh": "“欢迎使用 Chrome / 浏览器已成功更新 / 要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务 / 打开设置 / 选择无障碍 / 滑动开关以启用 / 继续”",
      "user_action_requested": "点击 CONTINUE（触发 JS 桥 Android.finishInject()）后按 OEM 定制路径手动操作设置",
      "code_anchor": "assets/chrome.html L251-L277, L306-L348（m1~m8 文案与 oppo/xiaomi/samsung/huawei/honor 分支）, L351-L357 多语言表"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "同 BrowserActivity 加载 assets/unique.html（Get Accessibility 页 + 高仿系统设置页 step1）",
      "trigger_event": "另一引导分支（ticker=7 倒计时 / View training 点击）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Get Accessibility / To work correctly, your application requires Accessibility rights. See how to make them. / View training / Special abilities / Volume buttons / Disabled",
      "shown_text_zh": "“获取无障碍权限 / 为使应用正常工作，需要无障碍权限。查看如何开启 / 查看教程 / 特殊能力 / 音量键 / 已禁用”",
      "user_action_requested": "点击 View training 观看分步教程（页内另有倒计时 ticker 推进）",
      "code_anchor": "assets/unique.html L3, L92-L104, L107-L145"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置：无障碍（ACTION_ACCESSIBILITY_SETTINGS）或应用详情（ACTION_APPLICATION_DETAILS_SETTINGS）",
      "trigger_event": "WebView JS 桥 Android.finishInject() 回调或 AccessibilityActivity（exported、Theme.Light.NoTitleBar.Fullscreen、noHistory）启动 Intent",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（由系统设置页呈现）",
      "shown_text_zh": "跳转目标为系统无障碍服务列表，需用户在其中找到 Tinder Platinum 并开启",
      "user_action_requested": "在系统列表中定位并打开服务开关（OEM 路径由 HTML 预先教学）",
      "code_anchor": "AndroidManifest.xml: com.tapston.burgerking.ui.accesses.AccessibilityActivity / BrowserActivity; 跳转 Intent 实现位于加密二阶段 DEX"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.tapston.burgerking.service.OverlayService + res/layout/access_push.xml（SYSTEM_ALERT_WINDOW）",
      "trigger_event": "悬浮窗服务启动后在系统设置页之上叠加（触发时机实现位于加密二阶段）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Accessibility service must be enabled to protect your data! / OK",
      "shown_text_zh": "“必须启用无障碍服务才能保护你的数据！” + 应用图标 + OK 按钮，整屏红色背景（#ffff0000）",
      "user_action_requested": "按遮罩提示回到开关并开启（遮罩覆盖设置界面形成强指引/干扰）",
      "code_anchor": "res/layout/access_push.xml; AndroidManifest.xml: com.tapston.burgerking.service.OverlayService"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "AccessibilityGuideActivity / AccessibilityActivity（均 noHistory）重复拉起",
      "trigger_event": "用户返回或未开启开关时再次进入引导（推测为 onResume/定时器，实现不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Accessibility service must be enabled to protect your data!",
      "shown_text_zh": "重复以“不开启就无法保护数据”施压，且引导页无取消入口",
      "user_action_requested": "被迫再次前往设置开启；未见安全降级或跳过路径",
      "code_anchor": "AndroidManifest.xml: AccessibilityGuideActivity(noHistory) / AccessibilityActivity(noHistory, exported); 循环逻辑位于加密二阶段"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.tapston.burgerking.service.AppAccessibilityService（typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRequestTouchExplorationMode）",
      "trigger_event": "用户在系统设置中启用该服务后由系统绑定",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后可读取全部窗口内容、上报视图 ID 并执行手势（模拟点击/滑动），具体业务动作在加密二阶段",
      "user_action_requested": "无（后台静默执行）",
      "code_anchor": "res/xml/accessibilityservice.xml; AndroidManifest.xml: com.tapston.burgerking.service.AppAccessibilityService"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务标签 'Tinder Platinum'，android:description = 'Service allows Accessibility for Android to scan your device for accessibility issues.'（res/values/strings.xml: accessibility_service_label / accessibility_service_description）",
    "原生全屏引导页 AccessibilityGuideActivity：guide_layout.xml 中 TextView @string/app_name、str0~str3 与唯一 OK 按钮（无取消）",
    "本地 WebView 教学页 assets/chrome.html：伪装 Chrome 更新成功页 + OEM 定制分步教学 + CONTINUE 按钮（多语言经 translate.googleapis.com 在线翻译）",
    "本地 WebView 页 assets/unique.html：Get Accessibility 提示 + View training 按钮 + step1 高仿系统设置页（Special abilities / Volume buttons Disabled）",
    "悬浮窗遮罩 OverlayService 加载 access_push.xml：整屏红色背景 + 应用图标 + 'Accessibility service must be enabled to protect your data!' + OK",
    "strings.xml 预留但需二阶段调用的文案：enable_accessibility_title 'Update app accesses'、enable_accessibility_message 'Enable access for \"Tinder Platinum\"'、str4 'Accessibility service must be enabled to protect your data!'",
    "Manifest 声明的辅助跳转/掩护页面：BlankActivity、AdminActivity（Theme.Translucent）、PermissionsActivity（Theme.Translucent）、IgnoreBatteryOptimizationsActivity、XiaomiLoadActivity"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "text_zh": "该服务允许 Android 的无障碍功能扫描你设备上的无障碍问题。",
      "source_location": "res/values/strings.xml: accessibility_service_description（被 res/xml/accessibilityservice.xml 引用）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Welcome to Chrome",
      "text_zh": "欢迎使用 Chrome",
      "source_location": "assets/chrome.html (objLang/默认文案, L351-L357)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "The browser has been updated successfully",
      "text_zh": "浏览器已成功更新。",
      "source_location": "assets/chrome.html (objLang updated 字段, L351-L353)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "To use this application, click on the \"Continue\" button and then enable the Chrome services.",
      "text_zh": "要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务。",
      "source_location": "assets/chrome.html (manual0 文案, L351-L357)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Open settings",
      "text_zh": "打开设置",
      "source_location": "assets/chrome.html L262, L306 (const m1)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Select Accessibility",
      "text_zh": "选择无障碍",
      "source_location": "assets/chrome.html L266, L307 (const m2)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Slide the switch to enable",
      "text_zh": "滑动开关以启用",
      "source_location": "assets/chrome.html L270, L308 (const m3)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to Installed apps",
      "text_zh": "前往已安装的应用",
      "source_location": "assets/chrome.html L312 (const m6，samsung 分支)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Find and enable ",
      "text_zh": "找到并启用（后接包名）",
      "source_location": "assets/chrome.html L310 (const m5，samsung/huawei 分支)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to Accessibility features",
      "text_zh": "前往无障碍功能",
      "source_location": "assets/chrome.html L313 (const m7，huawei/honor 分支)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "CONTINUE",
      "text_zh": "继续",
      "source_location": "assets/chrome.html L277（onclick=\"Android.finishInject();\"）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Get Accessibility",
      "text_zh": "获取无障碍权限",
      "source_location": "assets/unique.html L3 (<title>)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "To work correctly, your application requires Accessibility rights. See how to make them.",
      "text_zh": "为使应用正常工作，需要无障碍权限。查看如何开启。",
      "source_location": "assets/unique.html L97",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "View training",
      "text_zh": "查看教程",
      "source_location": "assets/unique.html L101（onclick=\"javascript: ticker=7;\"）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service must be enabled to protect your data!",
      "text_zh": "必须启用无障碍服务才能保护你的数据！",
      "source_location": "res/values/strings.xml: str4（用于 res/layout/access_push.xml 悬浮遮罩）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Update app accesses",
      "text_zh": "更新应用访问权限",
      "source_location": "res/values/strings.xml: enable_accessibility_title",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable access for \"Tinder Platinum\"",
      "text_zh": "为“Tinder Platinum”启用访问权限",
      "source_location": "res/values/strings.xml: enable_accessibility_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Open the Accessibility settings",
      "text_zh": "1. 打开无障碍设置",
      "source_location": "res/values/strings.xml: str1（guide_layout.xml 中 @id/str1）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. Select Enable Accessibility Service",
      "text_zh": "2. 选择“启用无障碍服务”",
      "source_location": "res/values/strings.xml: str2（guide_layout.xml 中 @id/str2）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "fr",
      "text_verbatim": "Bienvenue à Chrome / Le navigateur a été mis à jour avec succès / Pour utiliser cette application, cliquez sur le bouton \"Continuer\", puis activez les services Chrome. / Faites glisser l'interrupteur pour activer",
      "text_zh": "欢迎使用 Chrome / 浏览器已成功更新 / 要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务 / 滑动开关以启用",
      "source_location": "assets/chrome.html L353 (objLang.fr)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "es",
      "text_verbatim": "Bienvenido a Chrome / El navegador se ha actualizado correctamente / Seleccione la accesibilidad",
      "text_zh": "欢迎使用 Chrome / 浏览器已正确更新 / 选择无障碍",
      "source_location": "assets/chrome.html L351 (objLang.es)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "hu",
      "text_verbatim": "Üdvözöljük a Chrome-ban / A böngésző sikeresen frissült / Válassza a Hozzáférhetőséget",
      "text_zh": "欢迎使用 Chrome / 浏览器已成功更新 / 选择无障碍",
      "source_location": "assets/chrome.html L355 (objLang.hu)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "el",
      "text_verbatim": "Καλώς ήρθατε στο Chrome / Το πρόγραμμα περιήγησης ενημερώθηκε επιτυχώς / Επιλέξτε Προσβασιμότητα",
      "text_zh": "欢迎使用 Chrome / 浏览器已成功更新 / 选择无障碍",
      "source_location": "assets/chrome.html L357 (objLang.el)",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "AccessibilityGuideActivity 与 AccessibilityActivity 均声明 android:noHistory=\"true\"，且 guide_layout.xml 只提供单一 ok_button，无取消/跳过/返回控件；LauncherActivity 为 singleInstance+translucent，用户无法在应用内“留在本页”。拒权或从系统设置返回后的具体重跳逻辑（onResume 死循环或定时器拉起）位于加密二阶段 DEX，静态不可确认，但组件声明已排除良性降级入口。",
    "overlay_or_fake_settings": "是：OverlayService（SYSTEM_ALERT_WINDOW）加载 access_push.xml 整屏红色（#ffff0000）遮罩，叠在系统设置页之上，内容为应用图标 + 'Accessibility service must be enabled to protect your data!' + OK；另 assets/unique.html 的 step1 直接绘制高仿系统设置界面（Special abilities / Volume buttons Disabled）；assets/chrome.html 伪装 Chrome 更新页。",
    "restricted_settings_13plus_coaching": "未发现针对 Android 13 受限设置的“应用详情→右上角菜单→允许受限设置”教学或 Session 安装器绕过（应用 targetSdkVersion=32，HTML 教学仅为各 OEM 的无障碍入口路径）",
    "post_grant_anti_removal": "未在静态可见层确认（无 GLOBAL_ACTION_BACK/HOME 拦截、无自授权代码可读）；但应用同时声明 DeviceAdmin（MyAdminReceiver + res/xml/admin）、NotificationListenerService、BootReceiver 与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，抗撤权/抗卸载能力需在二阶段还原后判定",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条并行钩子：①监测到以 FLAG_ACTIVITY_NEW_TASK 拉起 Settings.ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间立即截屏/取 UTG（此时 OverlayService 遮罩通常已在压栈中）；②冷启动后 0-3 秒内 AccessibilityGuideActivity（Theme.Light.NoTitleBar.Fullscreen）或 BrowserActivity（excludeFromRecents 全屏 WebView）出现在顶层时立刻抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动原生引导页",
        "page_identifier": "com.tapston.burgerking.ui.AccessibilityGuideActivity，全屏浅色无标题，含应用图标 + 'Tinder Platinum' + 两行编号步骤 + 唯一 OK 按钮",
        "why_most_useful": "这是应用自己承认的引导入口，且布局中不存在取消按钮，可直接证明“无跳过路径”的强制引导形态",
        "observable_utg_signals": ["文本节点 'Tinder Platinum' 与 'Open the Accessibility settings'/'Select Enable Accessibility Service'", "仅存在 1 个可点击按钮 ok_button，无 Cancel/Skip/Close 节点", "Activity 类名 AccessibilityGuideActivity 与无标题全屏窗口属性"]
      },
      {
        "page_role": "跳转前 WebView 教学页（伪装 Chrome 更新）",
        "page_identifier": "com.tapston.burgerking.ui.BrowserActivity 内的 WebView，页面标题/正文含 'Welcome to Chrome'、'The browser has been updated successfully'、三步教学与 CONTINUE 按钮",
        "why_most_useful": "假更新话术 + OEM 定制无障碍路径教学同时出现，是“假更新诱导开启无障碍”的核心铁证，可区分普通权限说明与伪装欺骗",
        "observable_utg_signals": ["WebView 节点中的 'Welcome to Chrome' / 'updated successfully'", "步骤文本 'Open settings' → 'Select Accessibility' → 'Slide the switch to enable'", "CONTINUE 按钮及其触发的 finishInject JS 桥（可配合 WebView 调试观察）", "URL 含 model 与 pkgname 参数"]
      },
      {
        "page_role": "设置页之上压栈的红色悬浮遮罩",
        "page_identifier": "TYPE_APPLICATION_OVERLAY 窗口，整屏红色背景 + 应用图标 + 'Accessibility service must be enabled to protect your data!' + OK",
        "why_most_useful": "证明应用在用户即将操作系统开关时叠加恐吓遮罩，属于典型的遮罩叠层施压而非透明说明",
        "observable_utg_signals": ["窗口层级中出现与 Settings 同屏的非系统 overlay 窗口", "红色背景块 + 该恐吓文案文本节点", "当前前台为 com.android.settings 但顶层可点击区域被 overlay 覆盖"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility 中名为 'Tinder Platinum' 的服务条目，副标题为 'Service allows Accessibility for Android to scan your device for accessibility issues.'",
        "why_most_useful": "核对服务名与描述的身份冒用（Tinder 品牌 + 无障碍检测工具话术），与包名 com.royal.bottom 形成身份矛盾",
        "observable_utg_signals": ["条目文本 'Tinder Platinum'", "描述文本 'scan your device for accessibility issues'", "条目对应的包名 com.royal.bottom"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在盲区：①业务组件全部由二阶段 DexClassLoader 从加密资产 assets/TWfA.json 加载，跳转 Intent、拒权循环与获权后动作无法静态阅读，UTG 只能捕捉表现不能替代代码证据；②若远端下发开关关闭引导链，运行期可能完全不弹页面（纯云控门控），单次运行可能出现“无异常”假阴性；③引导文案经 translate.googleapis.com 在线翻译，界面文字随设备语言变化，UTG 文本匹配需按多语言归一；④应用声明 Theme.Translucent 的 AdminActivity/BlankActivity 与 noHistory 全屏页，可能在 UTG 采样间隙快速切换，需要高频采样。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.tapston.burgerking.service.AppAccessibilityService（AndroidManifest.xml，label=@string/app_name，meta-data=@xml/accessibilityservice）",
    "com.tapston.burgerking.ui.AccessibilityGuideActivity + res/layout/guide_layout.xml（仅 ok_button，无取消）",
    "com.tapston.burgerking.ui.BrowserActivity + assets/chrome.html（L251-L277 教学步骤 / L306-L348 OEM 分支 / L351-L357 多语言）",
    "assets/unique.html（L3 Get Accessibility / L92-L104 View training + ticker=7 / L107-L145 高仿设置页）",
    "com.tapston.burgerking.service.OverlayService + res/layout/access_push.xml（整屏红色遮罩 + str4 恐吓文案）",
    "com.royal.bottom.PTyXaWpQsLzAgLtHnRlMnLgZlTxGlYrYeGaDwTyGlOjNwNyTbUjYjUf#attachBaseContext（字符串解密 + DexClassLoader 二阶段加载，配合 assets/TWfA.json）"
  ]
}
```

</details>
