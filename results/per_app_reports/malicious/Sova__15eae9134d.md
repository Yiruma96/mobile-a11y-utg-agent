# MB_127__15eae9134d｜Sova — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：148.1s

## 1. 一句话核心结论

- **核心申请方式**：以本地俄语系 HTML 引导页把恶意无障碍服务包装成'应用正常运行权限'乃至'Chrome services'，用 View training→图文教学→Give rights 三步诱导用户手动进入系统无障碍设置开启全事件监听+读屏+手势服务。
- **静态可见性说明**：引导文案、分步教学页面、授权按钮与无障碍配置全部静态可见（assets/unique.html、assets/chrome.html、res/xml/accessibilityservice.xml、res/values/strings.xml）；但承担跳转与遮罩逻辑的 com.tapston.* 类在 DEX 中完全缺失，主逻辑由 com.civil.concert.PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi 在 attachBaseContext 内经 paddletotal/chroniceducate/luxuryalbum 解密链装载（另见 APK Sig Block 42 签名块载荷），ACTION_ACCESSIBILITY_SETTINGS 实际调用点、拒权重跳与叠层实现不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `15eae9134dac9268cbf005c23299c88dd5c5176a240201da751691a543375360` |
| 包名 / 年份 | `com.civil.concert` / 2023 |
| 家族 / 品类 | **Sova**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | 未确认（Manifest 使用 @string/app_name，预筛显示名为空） |
| 引导页宣称品牌/身份 | Chrome（chrome.html 将无障碍服务称为 Chrome services）；同时以 com.tapston.burgerking 快餐品牌化命名与 com.civil.concert 包名形成三重错配 |
| 系统无障碍列表服务名 | 应用名 @string/app_name（与桌面名一致，未暴露任何真实用途） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍描述仅写'扫描无障碍问题'以弱化读屏/手势能力；服务名直接复用 app_name；引导文案伪装为 Chrome 组件；内嵌 Google Translate 按系统语言机翻（pageLanguage:'ru'、googtrans=/ru/），面向俄语用户定向投放；DEX 类名/字段名全量随机混淆（PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi、paddletotal 等） |
| 无障碍服务类名 | `com.tapston.burgerking.service.AppAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tapston.burgerking.ui.LauncherActivity（LAUNCHER，singleInstance、noHistory、Translucent.NoTitleBar.Fullscreen） | 用户点击桌面图标，ACTION_MAIN/LAUNCHER 启动 | 原生Activity | **原文**：无（全屏透明无标题，静态不可见文本）<br>**译注**：无可见文本，静默转场，掩盖引导页来源 | 无主动交互，自动跳转至引导页；无取消/跳过入口 | `AndroidManifest.xml com.tapston.burgerking.ui.LauncherActivity` |
| 2 | 引导说明页 | com.tapston.burgerking.ui.AccessibilityGuideActivity / ui.BrowserActivity（WebView 加载 assets/unique.html） | LauncherActivity 启动后加载本地 HTML，loader1 区块在短暂 Loading 后显示 | 本地HTML WebView | **原文**：To work correctly, your application requires Accessibility rights. See how to make them. / View training<br>**译注**：为让应用正常运行，需要授予无障碍权限。查看如何开启。/ 查看教学 | 仅有一个绿色按钮 'View training'，无取消、跳过或'暂不开启'选项 | `assets/unique.html#L97-L101（onclick="javascript: ticker=7;"）` |
| 3 | 引导说明页 | unique.html #step1 分步图文教学（顶部固定菜单 'Special abilities'，assets/qidao/img_0~img_11.png 共 12 张分步截图） | ticker 计时器驱动，依次切换 step1 → step2 的图文步骤 | 本地HTML WebView | **原文**：Special abilities<br>**译注**：特殊能力（以截图逐步演示如何在系统设置中开启该服务） | 跟随图片逐屏模仿操作，步骤由 ticker 自动推进，无跳过按钮 | `assets/unique.html#L107-L114；assets/qidao/img_*.png` |
| 4 | 跳受限设置 | unique.html #step2 授权按钮 → JS 桥 Android.finishInject() → 原生跳转系统无障碍设置 | 用户点击绿色按钮 'Give rights'，触发 WebView JS 接口 finishInject() | 本地HTML WebView | **原文**：Give rights<br>**译注**：授予权限 | 点击按钮后被带离应用，进入系统设置；按钮为该页唯一出路，无取消分支 | `assets/unique.html#L449（onclick="Android.finishInject();"）` |
| 5 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务列表项（label=@string/app_name，描述='Service allows Accessibility for Android to scan your device for accessibility issues.'） | finishInject() 原生实现（com.tapston.* 类已加密隐藏，具体 ACTION_ACCESSIBILITY_SETTINGS 调用点静态不可见） | 系统无障碍页 | **原文**：Service allows Accessibility for Android to scan your device for accessibility issues.<br>**译注**：该服务允许 Android 无障碍功能扫描你设备上的无障碍问题。 | 在系统列表中手动找到本应用条目并打开开关——真正的授权动作发生在系统 UI，应用自身规避了权限告知 | `res/xml/accessibilityservice.xml；res/values/strings.xml#L31` |
| 6 | 遮罩叠层指引 | com.tapston.burgerking.service.OverlayService（SYSTEM_ALERT_WINDOW 已声明） | 跳转设置期间由服务拉起悬浮层（运行期行为，静态仅确认服务声明与权限） | 悬浮窗Overlay | **原文**：不可静态还原（OverlayService 实现类位于加密载荷中）<br>**译注**：推测为压栈在设置页之上的高亮指引遮罩，指向具体开关位置 | 跟随悬浮指示点击系统开关，无法返回应用 | `AndroidManifest.xml service com.tapston.burgerking.service.OverlayService` |
| 7 | 拒权反馈循环 | 不可静态还原（预期回到 AccessibilityGuideActivity / BrowserActivity 或重跳设置） | 用户按返回键或未开启服务回到应用（onResume 分支，位于加密载荷） | 不可静态还原 | **原文**：不可静态还原<br>**译注**：预期重新展示 'To work correctly, your application requires Accessibility rights' 并再次拉起教学/设置页 | 循环回到第 2 步，直至开启服务 | `不可静态还原（com.tapston.* 类缺失）` |
| 8 | 获权后动作 | com.tapston.burgerking.service.AppAccessibilityService + WorkerService/NotificationService/HeadlessSmsSendService | 系统绑定无障碍服务后 onServiceConnected，接收 typeAllMask 全量事件 | 原生Activity | 无 | 无（用户已无可感知提示） | `AndroidManifest.xml service com.tapston.burgerking.service.AppAccessibilityService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets/unique.html #loader1（第 92-104 行）：WebView 内联提示 'To work correctly, your application requires Accessibility rights. See how to make them.' + 绿色按钮 'View training'
- assets/unique.html #step1（第 107-331 行）：顶部固定菜单标题 'Special abilities' + assets/qidao/img_0~img_11.png 十二张分步截图教学
- assets/unique.html #step2（第 332-450 行）：绿色按钮 'Give rights'（onclick=Android.finishInject()）
- assets/chrome.html 第 243 行：WebView 内 'To use this application, click the "Continue" button and then enable Chrome services.'（伪装 Chrome 组件）
- 系统无障碍服务列表：服务名 = @string/app_name，描述 = res/values/strings.xml 第 31 行 'Service allows Accessibility for Android to scan your device for accessibility issues.'
- com.tapston.burgerking.service.OverlayService：SYSTEM_ALERT_WINDOW 悬浮层（实现不可静态还原，预期压栈于系统设置页之上）
- 无任何 res/layout 原生 Dialog、无 strings.xml 中的引导文案（引导文案全部由 HTML 承担，strings 中仅有无障碍描述一条）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To work correctly, your application requires Accessibility rights. See how to make them. | 为让应用正常运行，需要授予无障碍权限。查看如何开启。 | `assets/unique.html 第 97 行（#loader1）` | 受限设置分步教学 |
| en | View training | 查看教学 | `assets/unique.html 第 101 行` | 受限设置分步教学 |
| en | Special abilities | 特殊能力 | `assets/unique.html 第 114 行（#step1 顶栏）` | 受限设置分步教学 |
| en | Give rights | 授予权限 | `assets/unique.html 第 449 行（#step2，onclick=Android.finishInject()）` | 受限设置分步教学 |
| en | To use this application, click the "Continue" button and then enable Chrome services. | 要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务。 | `assets/chrome.html 第 243 行（#manual0）` | 教唆忽视警告 |
| en | Service allows Accessibility for Android to scan your device for accessibility issues. | 该服务允许 Android 无障碍功能扫描你设备上的无障碍问题。 | `res/values/strings.xml key=accessibility_service_description（第 31 行），经 res/xml/accessibilityservice.xml 引用` | 清理工具伪装 |
| en | Get Accessibility | 获取无障碍权限 | `assets/unique.html 第 3 行 <title>` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：预期在用户返回或未开启服务时重新展示 'To work correctly, your application requires Accessibility rights' 并再次推进 ticker 教学/重跳设置；具体 onResume 重跳与计时器实现位于加密载荷 com.tapston.* 中，静态不可还原，需 UTG 运行期验证
- **遮罩叠层 / 高仿系统设置页**：已声明 com.tapston.burgerking.service.OverlayService 与 SYSTEM_ALERT_WINDOW 权限，具备在系统设置页之上叠加引导遮罩的能力；未发现高仿系统无障碍开关页的布局资源（res/layout 中无对应伪造页），实现体在加密载荷内
- **Android 13+ 受限设置（Restricted Settings）应对**：引导页明确以图片分步教学演示如何在系统界面逐屏操作开启服务（assets/qidao/img_0~img_11.png，'View training'/'Special abilities'）；未发现针对 Android 13+ 应用详情页'允许受限设置'菜单或 Session 安装器绕过的专门文案
- **获权后即时行为与防撤权机制**：静态未确认。已声明 DeviceAdmin（MyAdminReceiver，BIND_DEVICE_ADMIN）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED，具备防卸载/自启动条件；但监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码位于加密载荷，需运行期验证
- **良性降级 / 替代方案**：无。页面仅提供唯一'View training → Give rights'路径，无手动模式、ADB 说明、仅观看模式或任何降级方案，也未说明权限用途与可随时关闭

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 com.tapston.burgerking.ui.LauncherActivity 启动后 3 秒内前台变为 BrowserActivity/AccessibilityGuideActivity 且存在 WebView 节点时立即截图；或监测到 finishInject() 桥调用后 ACTION_ACCESSIBILITY_SETTINGS 跳转瞬间（跳转前 1 帧抓取 step2 'Give rights' 页，跳转后 800ms 抓取悬浮遮罩）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：其一，step1 教学页主要由 assets/qidao/img_*.png 十二张图片构成，UTG 文本树可能几乎为空，需 OCR 才能读出截图内的系统设置路径文字；其二，全部 com.tapston.* 原生类（含 OverlayService、finishInject 实现、拒权重跳逻辑）由 com.civil.concert.PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi 在 attachBaseContext 解密装载，静态不可见，其行为只能靠 UTG 运行期观测；APK 内存在 APK Sig Block 42 签名块载荷痕迹，属一阶段 Dropper 特征，完整恶意能力（短信拦截、转账覆盖层）可能在下阶段载荷中。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首个引导页（WebView loader1）** | 包名 com.civil.concert 前台 + WebView 节点文本 'To work correctly, your application requires Accessibility rights.' / 按钮 'View training' | 这是诱导链的起点，直接证明应用在零功能使用前即索要无障碍权限，且无取消选项 | WebView 内可见文本 'requires Accessibility rights'；仅存在单个按钮节点 'View training'（无取消/跳过控件）；页面来自 file:///android_asset/unique.html |
| **分步教学页（step1 图文指引）** | 顶栏文本 'Special abilities' + 全屏图片轮播（qidao/img_*.png），无输入控件 | 证明存在系统性的手动开启教学，而非一次性跳转，属'受限设置分步教学'的直接运行证据 | 顶栏 'Special abilities'；连续多帧仅图片+无文本的截图教学页；ticker 自动翻页（无用户操作也变化） |
| **授权按钮页（step2 'Give rights'）** | WebView 内绿色按钮 'Give rights'，点击后前台切换至 com.android.settings 无障碍页 | 这是应用侧到系统侧的交接点，可确定诱导链的最终动作与跳转目标 | 按钮文本 'Give rights'；点击后 intent 目标为 Settings$AccessibilitySettings；跳转前无任何权限用途说明弹窗 |
| **系统无障碍服务列表项（含压栈遮罩）** | com.android.settings 无障碍页 + 条目文本为应用名及 'Service allows Accessibility for Android to scan your device for accessibility issues.'，若存在则叠加 OverlayService 悬浮层 | 可核对系统侧呈现的弱化描述与真实能力（全事件/读屏/手势）之间的落差，并检出是否压栈半透明引导遮罩 | 无障碍条目描述为 'scan your device for accessibility issues'；设置页之上存在非系统来源的悬浮视图节点；开关切换后是否自动返回应用或继续停留 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `assets/unique.html#L97-L101（loader1 提示 + View training 按钮）`
- `assets/unique.html#L449（step2 Give rights，onclick=Android.finishInject()）`
- `assets/chrome.html#L243（伪装 Chrome services 的 manual0 文案）`
- `res/xml/accessibilityservice.xml（typeAllMask + canRetrieveWindowContent + canPerformGestures）`
- `res/values/strings.xml#L31（accessibility_service_description 弱化描述）`
- `com.civil.concert.PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi#attachBaseContext（解密装载 com.tapston.* 主逻辑）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**一句话**：无障碍权限的申请完全由本地 HTML 引导页承担——页面把无障碍服务说成"应用正常运行所需的权限"，甚至称为 **"Chrome services"**，再用"View training → 分步图文教学 → Give rights"三步把用户推入系统无障碍列表手动开启。

**关键事实**

- **服务声明**：[AndroidManifest](<resource-unit:#1 manifest:components>) 注册 `com.tapston.burgerking.service.AppAccessibilityService`，`android:label="@string/app_name"`（即应用名），能力配置为 [accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml>)：`typeAllMask` + `canRetrieveWindowContent=true` + `canPerformGestures=true` + `flagIncludeNotImportantViews|flagReportViewIds|flagRequestTouchExplorationMode`——全事件监听＋读屏＋模拟手势，这是典型无障碍木马的权限组合。
- **系统列表文案严重弱化**：[strings.xml 第31行](<resource-unit:#1 file:res/values/strings.xml#L31>) 描述为 *"Service allows Accessibility for Android to scan your device for accessibility issues."*（宣称"扫描无障碍问题"），与真实能力完全不符；用户侧仅看到应用名 + 该"扫描器"描述，无任何恶意告知。
- **引导载体是本地 WebView HTML**：[unique.html 第97行](<resource-unit:#1 file:assets/unique.html#L97-L101>) 标题 `Get Accessibility`，正文 *"To work correctly, your application requires Accessibility rights. See how to make them."*，按钮 *"View training"*；第 107 行 `step1` 为图文教学（顶栏 *"Special abilities"*）；[第449行](<resource-unit:#1 file:assets/unique.html#L449>) `step2` 的绿色按钮 *"Give rights"* 绑定 `onclick="Android.finishInject();"` —— 由 JS 桥回调原生跳转系统设置。
- **品牌伪装**：[chrome.html 第243行](<resource-unit:#1 file:assets/chrome.html#L243>) 同一套文案改成 *"click the "Continue" button and then enable Chrome services"*，把恶意无障碍服务冒称为 Chrome 组件，利用用户对 Chrome 的信任；包名 `com.civil.concert`、服务包 `com.tapston.burgerking`（快餐品牌化命名）与应用实际身份三重错配。
- **多语言投放痕迹**：`unique.html` 内嵌 Google Translate 脚本（`setCookie('googtrans','/ru/'+lng)`、`pageLanguage:'ru'`），说明引导页面向俄语用户定向投放，文案随系统语言机翻。
- **配套权限漏斗组件**：`ui.AccessibilityGuideActivity`（全屏无标题、noHistory、singleInstance）、`ui.BrowserActivity`（WebView 承载）、`ui.accesses.AccessibilityActivity`、`service.OverlayService`、`ui.accesses.IgnoreBatteryOptimizationsActivity`、`ui.accesses.PermissionsActivity`——构成"引导页 → 教学 WebView → 无障碍设置 → 悬浮层"的完整递进链。

**覆盖边界（重要）**：`com.tapston.*` 全部类在 DEX 中不可见（`strings` 与代码工具均无匹配），主逻辑由 `com.civil.concert.PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi`（[attachBaseContext](<resource-unit:#1.dex1 code:com.civil.concert.PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi#attachBaseContext>) 内 `paddletotal/chroniceducate/luxuryalbum` 解密链）在运行期解密装载，APK 内亦检测到 `APK Sig Block 42` 签名块载荷痕迹。因此 **`ACTION_ACCESSIBILITY_SETTINGS` 的具体调用点、弹窗/悬浮层实现、拒权重跳逻辑均无法静态定位**，只能确认 HTML 侧的 `Android.finishInject()` 桥接意图。引导流程的静态证据强度以 HTML 资源 + Manifest 组件为准，拒绝反馈循环与叠层遮罩需 UTG 运行期确认。

---

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "引导文案、分步教学页面、授权按钮与无障碍配置全部静态可见（assets/unique.html、assets/chrome.html、res/xml/accessibilityservice.xml、res/values/strings.xml）；但承担跳转与遮罩逻辑的 com.tapston.* 类在 DEX 中完全缺失，主逻辑由 com.civil.concert.PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi 在 attachBaseContext 内经 paddletotal/chroniceducate/luxuryalbum 解密链装载（另见 APK Sig Block 42 签名块载荷），ACTION_ACCESSIBILITY_SETTINGS 实际调用点、拒权重跳与叠层实现不可静态还原。",
  "summary_one_liner": "以本地俄语系 HTML 引导页把恶意无障碍服务包装成'应用正常运行权限'乃至'Chrome services'，用 View training→图文教学→Give rights 三步诱导用户手动进入系统无障碍设置开启全事件监听+读屏+手势服务。",
  "disguise_identity": {
    "app_display_name": "未确认（Manifest 使用 @string/app_name，预筛显示名为空）",
    "claimed_brand_or_persona": "Chrome（chrome.html 将无障碍服务称为 Chrome services）；同时以 com.tapston.burgerking 快餐品牌化命名与 com.civil.concert 包名形成三重错配",
    "a11y_service_label": "应用名 @string/app_name（与桌面名一致，未暴露任何真实用途）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍描述仅写'扫描无障碍问题'以弱化读屏/手势能力；服务名直接复用 app_name；引导文案伪装为 Chrome 组件；内嵌 Google Translate 按系统语言机翻（pageLanguage:'ru'、googtrans=/ru/），面向俄语用户定向投放；DEX 类名/字段名全量随机混淆（PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi、paddletotal 等）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tapston.burgerking.ui.LauncherActivity（LAUNCHER，singleInstance、noHistory、Translucent.NoTitleBar.Fullscreen）",
      "trigger_event": "用户点击桌面图标，ACTION_MAIN/LAUNCHER 启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（全屏透明无标题，静态不可见文本）",
      "shown_text_zh": "无可见文本，静默转场，掩盖引导页来源",
      "user_action_requested": "无主动交互，自动跳转至引导页；无取消/跳过入口",
      "code_anchor": "AndroidManifest.xml com.tapston.burgerking.ui.LauncherActivity"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.tapston.burgerking.ui.AccessibilityGuideActivity / ui.BrowserActivity（WebView 加载 assets/unique.html）",
      "trigger_event": "LauncherActivity 启动后加载本地 HTML，loader1 区块在短暂 Loading 后显示",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "To work correctly, your application requires Accessibility rights. See how to make them. / View training",
      "shown_text_zh": "为让应用正常运行，需要授予无障碍权限。查看如何开启。/ 查看教学",
      "user_action_requested": "仅有一个绿色按钮 'View training'，无取消、跳过或'暂不开启'选项",
      "code_anchor": "assets/unique.html#L97-L101（onclick=\"javascript: ticker=7;\"）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "unique.html #step1 分步图文教学（顶部固定菜单 'Special abilities'，assets/qidao/img_0~img_11.png 共 12 张分步截图）",
      "trigger_event": "ticker 计时器驱动，依次切换 step1 → step2 的图文步骤",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Special abilities",
      "shown_text_zh": "特殊能力（以截图逐步演示如何在系统设置中开启该服务）",
      "user_action_requested": "跟随图片逐屏模仿操作，步骤由 ticker 自动推进，无跳过按钮",
      "code_anchor": "assets/unique.html#L107-L114；assets/qidao/img_*.png"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "unique.html #step2 授权按钮 → JS 桥 Android.finishInject() → 原生跳转系统无障碍设置",
      "trigger_event": "用户点击绿色按钮 'Give rights'，触发 WebView JS 接口 finishInject()",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Give rights",
      "shown_text_zh": "授予权限",
      "user_action_requested": "点击按钮后被带离应用，进入系统设置；按钮为该页唯一出路，无取消分支",
      "code_anchor": "assets/unique.html#L449（onclick=\"Android.finishInject();\"）"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务列表项（label=@string/app_name，描述='Service allows Accessibility for Android to scan your device for accessibility issues.'）",
      "trigger_event": "finishInject() 原生实现（com.tapston.* 类已加密隐藏，具体 ACTION_ACCESSIBILITY_SETTINGS 调用点静态不可见）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "shown_text_zh": "该服务允许 Android 无障碍功能扫描你设备上的无障碍问题。",
      "user_action_requested": "在系统列表中手动找到本应用条目并打开开关——真正的授权动作发生在系统 UI，应用自身规避了权限告知",
      "code_anchor": "res/xml/accessibilityservice.xml；res/values/strings.xml#L31"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.tapston.burgerking.service.OverlayService（SYSTEM_ALERT_WINDOW 已声明）",
      "trigger_event": "跳转设置期间由服务拉起悬浮层（运行期行为，静态仅确认服务声明与权限）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "不可静态还原（OverlayService 实现类位于加密载荷中）",
      "shown_text_zh": "推测为压栈在设置页之上的高亮指引遮罩，指向具体开关位置",
      "user_action_requested": "跟随悬浮指示点击系统开关，无法返回应用",
      "code_anchor": "AndroidManifest.xml service com.tapston.burgerking.service.OverlayService"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "不可静态还原（预期回到 AccessibilityGuideActivity / BrowserActivity 或重跳设置）",
      "trigger_event": "用户按返回键或未开启服务回到应用（onResume 分支，位于加密载荷）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "不可静态还原",
      "shown_text_zh": "预期重新展示 'To work correctly, your application requires Accessibility rights' 并再次拉起教学/设置页",
      "user_action_requested": "循环回到第 2 步，直至开启服务",
      "code_anchor": "不可静态还原（com.tapston.* 类缺失）"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.tapston.burgerking.service.AppAccessibilityService + WorkerService/NotificationService/HeadlessSmsSendService",
      "trigger_event": "系统绑定无障碍服务后 onServiceConnected，接收 typeAllMask 全量事件",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "引导界面消失，转入静默后台：读屏、模拟点击、拦截短信/通知",
      "user_action_requested": "无（用户已无可感知提示）",
      "code_anchor": "AndroidManifest.xml service com.tapston.burgerking.service.AppAccessibilityService"
    }
  ],
  "text_presentation_locations": [
    "assets/unique.html #loader1（第 92-104 行）：WebView 内联提示 'To work correctly, your application requires Accessibility rights. See how to make them.' + 绿色按钮 'View training'",
    "assets/unique.html #step1（第 107-331 行）：顶部固定菜单标题 'Special abilities' + assets/qidao/img_0~img_11.png 十二张分步截图教学",
    "assets/unique.html #step2（第 332-450 行）：绿色按钮 'Give rights'（onclick=Android.finishInject()）",
    "assets/chrome.html 第 243 行：WebView 内 'To use this application, click the \"Continue\" button and then enable Chrome services.'（伪装 Chrome 组件）",
    "系统无障碍服务列表：服务名 = @string/app_name，描述 = res/values/strings.xml 第 31 行 'Service allows Accessibility for Android to scan your device for accessibility issues.'",
    "com.tapston.burgerking.service.OverlayService：SYSTEM_ALERT_WINDOW 悬浮层（实现不可静态还原，预期压栈于系统设置页之上）",
    "无任何 res/layout 原生 Dialog、无 strings.xml 中的引导文案（引导文案全部由 HTML 承担，strings 中仅有无障碍描述一条）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To work correctly, your application requires Accessibility rights. See how to make them.",
      "text_zh": "为让应用正常运行，需要授予无障碍权限。查看如何开启。",
      "source_location": "assets/unique.html 第 97 行（#loader1）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "View training",
      "text_zh": "查看教学",
      "source_location": "assets/unique.html 第 101 行",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Special abilities",
      "text_zh": "特殊能力",
      "source_location": "assets/unique.html 第 114 行（#step1 顶栏）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Give rights",
      "text_zh": "授予权限",
      "source_location": "assets/unique.html 第 449 行（#step2，onclick=Android.finishInject()）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "To use this application, click the \"Continue\" button and then enable Chrome services.",
      "text_zh": "要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务。",
      "source_location": "assets/chrome.html 第 243 行（#manual0）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "text_zh": "该服务允许 Android 无障碍功能扫描你设备上的无障碍问题。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（第 31 行），经 res/xml/accessibilityservice.xml 引用",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Get Accessibility",
      "text_zh": "获取无障碍权限",
      "source_location": "assets/unique.html 第 3 行 <title>",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "预期在用户返回或未开启服务时重新展示 'To work correctly, your application requires Accessibility rights' 并再次推进 ticker 教学/重跳设置；具体 onResume 重跳与计时器实现位于加密载荷 com.tapston.* 中，静态不可还原，需 UTG 运行期验证",
    "overlay_or_fake_settings": "已声明 com.tapston.burgerking.service.OverlayService 与 SYSTEM_ALERT_WINDOW 权限，具备在系统设置页之上叠加引导遮罩的能力；未发现高仿系统无障碍开关页的布局资源（res/layout 中无对应伪造页），实现体在加密载荷内",
    "restricted_settings_13plus_coaching": "引导页明确以图片分步教学演示如何在系统界面逐屏操作开启服务（assets/qidao/img_0~img_11.png，'View training'/'Special abilities'）；未发现针对 Android 13+ 应用详情页'允许受限设置'菜单或 Session 安装器绕过的专门文案",
    "post_grant_anti_removal": "静态未确认。已声明 DeviceAdmin（MyAdminReceiver，BIND_DEVICE_ADMIN）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED，具备防卸载/自启动条件；但监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码位于加密载荷，需运行期验证",
    "benign_graceful_degradation": "无。页面仅提供唯一'View training → Give rights'路径，无手动模式、ADB 说明、仅观看模式或任何降级方案，也未说明权限用途与可随时关闭"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 com.tapston.burgerking.ui.LauncherActivity 启动后 3 秒内前台变为 BrowserActivity/AccessibilityGuideActivity 且存在 WebView 节点时立即截图；或监测到 finishInject() 桥调用后 ACTION_ACCESSIBILITY_SETTINGS 跳转瞬间（跳转前 1 帧抓取 step2 'Give rights' 页，跳转后 800ms 抓取悬浮遮罩）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首个引导页（WebView loader1）",
        "page_identifier": "包名 com.civil.concert 前台 + WebView 节点文本 'To work correctly, your application requires Accessibility rights.' / 按钮 'View training'",
        "why_most_useful": "这是诱导链的起点，直接证明应用在零功能使用前即索要无障碍权限，且无取消选项",
        "observable_utg_signals": ["WebView 内可见文本 'requires Accessibility rights'", "仅存在单个按钮节点 'View training'（无取消/跳过控件）", "页面来自 file:///android_asset/unique.html"]
      },
      {
        "page_role": "分步教学页（step1 图文指引）",
        "page_identifier": "顶栏文本 'Special abilities' + 全屏图片轮播（qidao/img_*.png），无输入控件",
        "why_most_useful": "证明存在系统性的手动开启教学，而非一次性跳转，属'受限设置分步教学'的直接运行证据",
        "observable_utg_signals": ["顶栏 'Special abilities'", "连续多帧仅图片+无文本的截图教学页", "ticker 自动翻页（无用户操作也变化）"]
      },
      {
        "page_role": "授权按钮页（step2 'Give rights'）",
        "page_identifier": "WebView 内绿色按钮 'Give rights'，点击后前台切换至 com.android.settings 无障碍页",
        "why_most_useful": "这是应用侧到系统侧的交接点，可确定诱导链的最终动作与跳转目标",
        "observable_utg_signals": ["按钮文本 'Give rights'", "点击后 intent 目标为 Settings$AccessibilitySettings", "跳转前无任何权限用途说明弹窗"]
      },
      {
        "page_role": "系统无障碍服务列表项（含压栈遮罩）",
        "page_identifier": "com.android.settings 无障碍页 + 条目文本为应用名及 'Service allows Accessibility for Android to scan your device for accessibility issues.'，若存在则叠加 OverlayService 悬浮层",
        "why_most_useful": "可核对系统侧呈现的弱化描述与真实能力（全事件/读屏/手势）之间的落差，并检出是否压栈半透明引导遮罩",
        "observable_utg_signals": ["无障碍条目描述为 'scan your device for accessibility issues'", "设置页之上存在非系统来源的悬浮视图节点", "开关切换后是否自动返回应用或继续停留"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在两处盲区：其一，step1 教学页主要由 assets/qidao/img_*.png 十二张图片构成，UTG 文本树可能几乎为空，需 OCR 才能读出截图内的系统设置路径文字；其二，全部 com.tapston.* 原生类（含 OverlayService、finishInject 实现、拒权重跳逻辑）由 com.civil.concert.PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi 在 attachBaseContext 解密装载，静态不可见，其行为只能靠 UTG 运行期观测；APK 内存在 APK Sig Block 42 签名块载荷痕迹，属一阶段 Dropper 特征，完整恶意能力（短信拦截、转账覆盖层）可能在下阶段载荷中。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "assets/unique.html#L97-L101（loader1 提示 + View training 按钮）",
    "assets/unique.html#L449（step2 Give rights，onclick=Android.finishInject()）",
    "assets/chrome.html#L243（伪装 Chrome services 的 manual0 文案）",
    "res/xml/accessibilityservice.xml（typeAllMask + canRetrieveWindowContent + canPerformGestures）",
    "res/values/strings.xml#L31（accessibility_service_description 弱化描述）",
    "com.civil.concert.PFuBnIfGmAcCqRcZmPfQcFdRjXxAnZdOeBfAfTtYhGoLoGi#attachBaseContext（解密装载 com.tapston.* 主逻辑）"
  ]
}
```

</details>
