# MB_128__7c805f51ee｜Sova — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：150.5s

## 1. 一句话核心结论

- **核心申请方式**：应用把自身伪装成 Chrome，冷启动经不可见最近任务的引导页用本地 HTML/原生弹窗以“更新应用访问权限”为名分步教学跳转系统无障碍设置，并配置读屏+手势权限、悬浮窗与设备管理员做配套，真正代码藏在加密二阶段载荷中。
- **静态可见性说明**：Manifest、res/values/strings.xml、res/xml/accessibilityservice.xml、assets/chrome.html 与 assets/unique.html 全部静态明文可见，可完整还原界面文案与伪装身份；但 Manifest 声明的全部业务组件类（com.devapprove.a.ru.news.MainActivity / LauncherActivity / AccessibilityGuideActivity / AccessibilityActivity / AppAccessibilityService 等）在 classes.dex 中零命中，classes.dex 仅含 com.bean.* 壳层代码，另存在 2.3MB 非文本加密资产 assets/CtaDwII.json 与 Ldalvik/system/DexClassLoader 引用，判定为加密二阶段载荷运行期解密加载；跳转触发点、拒权重跳循环、获权后自授权等代码逻辑不在静态可见范围。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `7c805f51ee3b2994e742d73954e51d7c2c24c76455b0b9a1b44d61cb4e280502` |
| 包名 / 年份 | `com.bean.cousin` / 2022 |
| 家族 / 品类 | **Sova**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Google Chrome 浏览器 |
| 系统无障碍列表服务名 | Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名为 com.bean.cousin，组件命名空间为 com.devapprove.a.ru.news，与宣称的 Chrome 完全不符；无障碍描述被写成低敏感的安全扫描话术（scan your device for accessibility issues）；引导页 Activity 使用 excludeFromRecents + singleInstance + noHistory 避免在最近任务中暴露；存在多个导出的全屏/透明引导 Activity（AccessibilityActivity、PermissionsActivity、BlankActivity、XiaomiLoadActivity）用于换壳与厂商适配；核心类整体移入加密载荷 assets/CtaDwII.json 由 DexClassLoader 加载 |
| 无障碍服务类名 | `com.devapprove.a.ru.news.service.AppAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.devapprove.a.ru.news.ui.LauncherActivity（LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen） | 用户点击桌面图标（MAIN/LAUNCHER intent-filter），onCreate 后按加密载荷内逻辑决定进入引导 | 原生Activity | **原文**：Chrome<br>**译注**：桌面图标名与启动瞬间界面无文案，仅显示应用名 Chrome | 无显式操作，透明全屏页自动流转（是否可返回/取消由加密载荷逻辑决定，静态不可确认） | `com.devapprove.a.ru.news.ui.LauncherActivity（AndroidManifest.xml 声明）；res/values/strings.xml#app_name` |
| 2 | 引导说明页 | com.devapprove.a.ru.news.ui.AccessibilityGuideActivity（@style/DTheme，excludeFromRecents，singleInstance，noHistory） | LauncherActivity 或业务逻辑跳入引导页（noHistory 保证返回不回到该页） | 本地HTML WebView | **原文**：Get Accessibility / To work correctly, your application requires Accessibility rights. See how to make them.<br>**译注**：“获取无障碍权限”“为正常使用，你的应用需要无障碍权限。查看如何开启。”并配鼠标/手指轨迹动画演示 | 点击进入教学/跳转按钮（页面为单向前进式，未见跳过或取消文案） | `assets/unique.html；com.devapprove.a.ru.news.ui.AccessibilityGuideActivity` |
| 3 | 引导说明页（品牌伪装版） | WebView 教学页（同一引导流程的另一套模板） | 引导页加载本地 chrome.html 或后续步骤点击“下一步” | 本地HTML WebView | **原文**：1. Open accessibility settings / 2. Select Chrome / GO TO SETTINGS<br>**译注**：“1. 打开无障碍设置　2. 选择 Chrome　3. 前往设置（GO TO SETTINGS）”三步教学，并引导在系统列表中选择名为 Chrome 的服务 | 点击 GO TO SETTINGS 按钮（未见取消/跳过按钮） | `assets/chrome.html` |
| 4 | 引导说明页（原生弹窗版） | 原生 Dialog / 全屏提示（文案来自 strings.xml，承载类位于加密载荷） | 冷启动或功能触发时弹出权限提示 | 原生Dialog | **原文**：Update app accesses / Enable access for "Chrome"<br>**译注**：标题“更新应用访问权限”，正文“为 Chrome 开启访问权限”，以版本更新/权限刷新为名索取无障碍 | 点击确认进入设置（文案中无“取消”“稍后”“跳过”） | `res/values/strings.xml#enable_accessibility_title、#enable_accessibility_message` |
| 5 | 跳无障碍设置 | 系统无障碍设置页（ACTION_ACCESSIBILITY_SETTINGS 目标），列表项显示为 Chrome | 引导页按钮/弹窗确认回调中启动 Settings.ACTION_ACCESSIBILITY_SETTINGS（跳转代码在加密载荷内，DEX 中无该 action 字符串） | 系统无障碍页 | **原文**：Chrome / Service allows Accessibility for Android to scan your device for accessibility issues.<br>**译注**：系统无障碍列表中服务名为 Chrome，说明文字为“允许 Accessibility for Android 扫描设备的无障碍问题”（伪装成辅助检查工具） | 要求用户手动找到 Chrome 条目并拨动开关启用；说明文字故意弱化“读取屏幕内容与模拟点击”的实际能力 | `res/xml/accessibilityservice.xml；res/values/strings.xml#accessibility_service_label、#accessibility_service_description` |
| 6 | 遮罩叠层指引 | com.devapprove.a.ru.news.service.OverlayService（悬浮窗）＋ AccessibilityActivity（导出的全屏透明页） | 进入设置页后由悬浮窗/透明 Activity 叠层提示操作位置（具体时序在加密载荷内，静态不可确认） | 悬浮窗Overlay | **原文**：1. Open the Accessibility settings / 2. Select Enable Accessibility Service / 3. Slide the switch to enable<br>**译注**：“1. 打开无障碍设置　2. 选择启用无障碍服务　3. 滑动开关启用”三步操作指引叠在系统设置页上方 | 按指引在系统页面手动拨动开关（指引层未提供取消/返回选项） | `res/values/strings.xml#str1、#str2、#str3；com.devapprove.a.ru.news.service.OverlayService；com.devapprove.a.ru.news.ui.accesses.AccessibilityActivity` |
| 7 | 拒权反馈循环 | 伪系统检查界面（managing_service_title/message）＋ AccessibilityActivity/PermissionsActivity 重入 | 用户在系统设置中返回而未启用时，由 onResume/定时器再次拉起引导（重跳机制位于加密载荷，静态不可确认） | 原生Activity | **原文**：Checking system / Checking<br>**译注**：“正在检查系统”“检查中”，以系统自检动画掩盖仍在等待授权，并持续把用户拉回设置流程 | 被迫继续前往设置或停留在引导，未见降级/跳过路径 | `res/values/strings.xml#managing_service_title、#managing_service_message；com.devapprove.a.ru.news.ui.accesses.PermissionsActivity` |
| 8 | 获权后动作 | AppAccessibilityService（typeAllMask + 读窗 + 手势）＋ NotificationService（通知监听）＋ OverlayService ＋ AdminActivity/MyAdminReceiver（设备管理员） | AccessibilityService.onServiceConnected 或轮询检测到服务已启用 | 不可静态还原 | **原文**：Allow pop-ups / Checking<br>**译注**：获权后弹出“允许弹窗”（小米等厂商悬浮窗授权引导），随后转入静默后台能力 | 可能要求再授予悬浮窗/忽略电池优化/设备管理员，以避免被撤销或卸载（具体动作在加密载荷内） | `com.devapprove.a.ru.news.service.AppAccessibilityService；com.devapprove.a.ru.news.service.NotificationService；com.devapprove.a.ru.news.MyAdminReceiver；res/values/strings.xml#miuipopup` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml#app_name = "Chrome"：桌面图标名与无障碍服务 label（AppAccessibilityService 的 android:label 引用 @string/app_name）
- res/values/strings.xml#accessibility_service_description：系统无障碍列表条目下方的说明文字，伪装为“扫描无障碍问题”
- res/values/strings.xml#enable_accessibility_title / #enable_accessibility_message：冷启动或触发时的原生 Dialog（“Update app accesses” / Enable access for "Chrome"）
- res/values/strings.xml#str1、#str2、#str3：原生引导页/悬浮窗中的三步操作教学文案
- res/values/strings.xml#managing_service_title / #managing_service_message：等待授权期间的伪系统“Checking system”检查界面
- assets/unique.html：AccessibilityGuideActivity 承载的 WebView 引导页（Get Accessibility 话术 + 轨迹动画）
- assets/chrome.html：WebView 分步教学页（1. Open accessibility settings / 2. Select Chrome / GO TO SETTINGS）
- res/values/strings.xml#miuipopup（Allow pop-ups）：获权后引导授予悬浮窗权限的提示

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome | Chrome（浏览器） | `res/values/strings.xml#app_name、#accessibility_service_label` | 假更新 |
| en | Update app accesses | 更新应用访问权限 | `res/values/strings.xml#enable_accessibility_title` | 假更新 |
| en | Enable access for "Chrome" | 为“Chrome”开启访问权限 | `res/values/strings.xml#enable_accessibility_message` | 假更新 |
| en | Service allows Accessibility for Android to scan your device for accessibility issues. | 该服务允许 Accessibility for Android 扫描你设备的无障碍问题。 | `res/values/strings.xml#accessibility_service_description（被 res/xml/accessibilityservice.xml 引用）` | 假反诈安全 |
| en | 1. Open the Accessibility settings | 1. 打开无障碍设置 | `res/values/strings.xml#str1` | 受限设置分步教学 |
| en | 2. Select Enable Accessibility Service | 2. 选择“启用无障碍服务” | `res/values/strings.xml#str2` | 受限设置分步教学 |
| en | 3. Slide the switch to enable | 3. 滑动开关以启用 | `res/values/strings.xml#str3` | 受限设置分步教学 |
| en | Get Accessibility | 获取无障碍权限 | `assets/unique.html（<title>）` | 假更新 |
| en | To work correctly, your application requires Accessibility rights. See how to make them. | 为正常使用，你的应用需要无障碍权限。查看如何开启。 | `assets/unique.html` | 假更新 |
| en | 1. Open accessibility settings | 1. 打开无障碍设置 | `assets/chrome.html` | 受限设置分步教学 |
| en | 2. Select Chrome | 2. 选择 Chrome | `assets/chrome.html` | 受限设置分步教学 |
| en | GO TO SETTINGS | 前往设置 | `assets/chrome.html` | 受限设置分步教学 |
| en | Checking system | 正在检查系统 | `res/values/strings.xml#managing_service_title` | 故障恐吓 |
| en | Allow pop-ups | 允许弹出窗口 | `res/values/strings.xml#miuipopup` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无取消路径的字符串设计 + 导出的 AccessibilityActivity/PermissionsActivity（noHistory、全屏透明）与 OverlayService 组合，指向返回设置页后再次拉起引导；但 onResume/定时重跳的具体实现位于加密二阶段载荷（classes.dex 中无相关类与 ACTION_ACCESSIBILITY_SETTINGS 字符串），静态不可确认循环周期与次数
- **遮罩叠层 / 高仿系统设置页**：存在 OverlayService 悬浮窗与 Theme.Translucent/Fullscreen 的导出 Activity，具备叠层指引能力；未见高仿系统无障碍开关页的布局资源（res/layout 下无任何布局文件），叠层形式为悬浮窗或透明页指引，具体样式在加密载荷内
- **Android 13+ 受限设置（Restricted Settings）应对**：未见应用详情右上角菜单允许受限设置、也未发现 Session 安装器绕过的静态痕迹（targetSdk 32，Manifest 中无相关字符串与资源）；不排除由加密载荷在运行期下发
- **获权后即时行为与防撤权机制**：具备防撤权/防卸载配套组件：设备管理员（AdminActivity + MyAdminReceiver + res/xml/admin）、NotificationListenerService 通知监听、OverlayService 悬浮窗、RECEIVE_BOOT_COMPLETED + AlarmBroadcastReceiver 自启；是否在获权后自点确认或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权需读取加密载荷，静态不可确认
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 LauncherActivity（Theme.Translucent.NoTitleBar.Fullscreen）后 1–3 秒内出现的首个非透明界面，以及 AccessibilityGuideActivity 启动瞬间；同时挂 ACTION_ACCESSIBILITY_SETTINGS 跳转监测，跳转后立即连拍系统设置页与其上叠加的悬浮窗
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区在于二阶段载荷：classes.dex 不含任何 com.devapprove 组件类与无障碍跳转字符串，Manifest 声明的业务组件由 DexClassLoader 从 2.3MB 加密资产 assets/CtaDwII.json 解密加载，因此跳转触发点、拒权重跳逻辑、获权后自授权/防撤权动作只能靠运行期 UTG 观测补全；另 OverlayService 悬浮层与 WebView 引导页若为纯图或 Canvas 绘制则需 OCR 辅助。静态资源本身明文可见，不构成加壳遮挡文案的问题。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页/教学 WebView 页** | AccessibilityGuideActivity（DTheme，单实例、不留在最近任务）内 WebView 渲染 assets/unique.html 或 assets/chrome.html | 此处决定是否构成“以 Chrome 品牌伪装 + 假更新话术”诱导，且文案为逐字可比对的静态真值，最能区分诱导与良性透明说明 | 标题 Get Accessibility；正文 requires Accessibility rights；1. Open accessibility settings / 2. Select Chrome 分步文案；GO TO SETTINGS 按钮文本；页面是否为全屏且无取消/跳过控件 |
| **冷启动原生引导弹窗** | 原生 Dialog，标题 Update app accesses，正文 Enable access for "Chrome" | 证明引导发生在冷启动 0 步而非用户功能触发，并体现“权限更新”伪装框架与是否可取消 | 标题文本 Update app accesses；按钮数量与文本（是否存在取消/稍后）；弹窗是否可返回键关闭 |
| **系统无障碍服务列表项** | Settings 无障碍页中名为 Chrome 的服务条目及其描述 | 核对系统侧展示名与描述是否与包名 com.bean.cousin 不符，以及描述是否被弱化 | 服务名 Chrome；描述 Service allows Accessibility for Android to scan your device；该条目是否被置顶或高亮 |
| **设置页后叠加的引导遮罩/伪检查页** | OverlayService 悬浮窗或 AccessibilityActivity 透明全屏页；文案 1./2./3. 步骤或 Checking system | 判定是否存在叠层指引与伪系统检查界面，以及用户从设置页返回后是否被立即重跳（拒权循环） | 悬浮窗/透明页上的步骤文案；Checking system 文本；返回后前台 Activity 是否再次变为 AccessibilityActivity/AccessibilityGuideActivity；重跳间隔与次数 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.devapprove.a.ru.news.ui.AccessibilityGuideActivity`
- `com.devapprove.a.ru.news.service.AppAccessibilityService`
- `res/xml/accessibilityservice.xml`
- `res/values/strings.xml#enable_accessibility_title / #enable_accessibility_message / #str1-#str3`
- `assets/unique.html`
- `assets/chrome.html`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **身份伪装**：桌面显示名、无障碍服务标签、无障碍服务说明全部伪装成 **Chrome**（`res/values/strings.xml` 中 `app_name`、`accessibility_service_label`、`enable_accessibility_message`），而真实包名是 `com.bean.cousin`，Manifest 声明的组件命名空间是 `com.devapprove.a.ru.news.*`。
- **无障碍配置伪装成“无障碍洞察扫描工具”**：`res/xml/accessibilityservice.xml` 声明 `typeAllMask`、`canRetrieveWindowContent=true`、`canPerformGestures=true`、`flagRequestTouchExplorationMode`，description 却写成“scan your device for accessibility issues”（扫描无障碍问题），属于用低敏感能力描述来掩盖读屏和模拟点击的能力。
- **引导内容有两套本地 HTML 教学页**：
  - `assets/chrome.html`（207KB）：`1. Open accessibility settings` → `2. Select Chrome` → `GO TO SETTINGS`，是 Chrome 品牌外观的分步教学页加跳转按钮；
  - `assets/unique.html`（21KB）：标题 `Get Accessibility`，正文 `To work correctly, your application requires Accessibility rights. See how to make them.`，并带 `.mouse` 鼠标或手指轨迹动画，属于“功能必需”的话术框架。
- **原生字符串同样构成“假更新”框架**：`enable_accessibility_title = Update app accesses`、`enable_accessibility_message = Enable access for "Chrome"`，即“更新应用访问权限”式弹窗；`str1/str2/str3` 是原生三步教学文案；另有 `managing_service_title = Checking system` / `managing_service_message = Checking` 的伪系统检查界面文案。
- **组件编排对应完整的诱导链**：`LauncherActivity`（LAUNCHER，`Theme.Translucent.NoTitleBar.Fullscreen`）→ `AccessibilityGuideActivity`（`excludeFromRecents`、`singleInstance`、`noHistory`、`@style/DTheme`，专门承载引导页且不留在最近任务）→ `AccessibilityActivity`/`PermissionsActivity`/`IgnoreBatteryOptimizationsActivity`（导出的全屏/透明权引导页）→ `OverlayService`（悬浮窗引导/遮罩）+ `AppAccessibilityService` + `NotificationService`（通知监听）+ `AdminActivity`/`MyAdminReceiver`（设备管理员，防卸载）。
- **静态可见性边界（关键）**：`classes.dex` 内**完全不含** `com/devapprove` 任何类与字符串（0 次命中），也无 `ACTION_ACCESSIBILITY_SETTINGS`；`assets/CtaDwII.json` 是 2.3MB 非文本二进制（magic `71 66 57 5c …`）的加密二阶段载荷，DEX 中存在 `Ldalvik/system/DexClassLoader` 引用。即 **Manifest 声明的全部业务组件（含无障碍服务与引导 Activity）实体代码不在 classes.dex，需运行期解密加载**。因此 UTG 页面文字、按钮流程可由资源还原，**跳转与拒权循环的具体代码逻辑无法静态确认**。
- 引导方式判定：冷启动即进入伪装成 Chrome 的“更新应用访问权限”引导，通过本地 HTML/原生弹窗分步教学跳转系统无障碍设置；无取消/跳过路径的证据（字符串与组件设计均指向强制推进），但拒权循环的代码实现位于加密载荷，属未决项。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、res/values/strings.xml、res/xml/accessibilityservice.xml、assets/chrome.html 与 assets/unique.html 全部静态明文可见，可完整还原界面文案与伪装身份；但 Manifest 声明的全部业务组件类（com.devapprove.a.ru.news.MainActivity / LauncherActivity / AccessibilityGuideActivity / AccessibilityActivity / AppAccessibilityService 等）在 classes.dex 中零命中，classes.dex 仅含 com.bean.* 壳层代码，另存在 2.3MB 非文本加密资产 assets/CtaDwII.json 与 Ldalvik/system/DexClassLoader 引用，判定为加密二阶段载荷运行期解密加载；跳转触发点、拒权重跳循环、获权后自授权等代码逻辑不在静态可见范围。",
  "summary_one_liner": "应用把自身伪装成 Chrome，冷启动经不可见最近任务的引导页用本地 HTML/原生弹窗以“更新应用访问权限”为名分步教学跳转系统无障碍设置，并配置读屏+手势权限、悬浮窗与设备管理员做配套，真正代码藏在加密二阶段载荷中。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Google Chrome 浏览器",
    "a11y_service_label": "Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名为 com.bean.cousin，组件命名空间为 com.devapprove.a.ru.news，与宣称的 Chrome 完全不符；无障碍描述被写成低敏感的安全扫描话术（scan your device for accessibility issues）；引导页 Activity 使用 excludeFromRecents + singleInstance + noHistory 避免在最近任务中暴露；存在多个导出的全屏/透明引导 Activity（AccessibilityActivity、PermissionsActivity、BlankActivity、XiaomiLoadActivity）用于换壳与厂商适配；核心类整体移入加密载荷 assets/CtaDwII.json 由 DexClassLoader 加载"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.devapprove.a.ru.news.ui.LauncherActivity（LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen）",
      "trigger_event": "用户点击桌面图标（MAIN/LAUNCHER intent-filter），onCreate 后按加密载荷内逻辑决定进入引导",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Chrome",
      "shown_text_zh": "桌面图标名与启动瞬间界面无文案，仅显示应用名 Chrome",
      "user_action_requested": "无显式操作，透明全屏页自动流转（是否可返回/取消由加密载荷逻辑决定，静态不可确认）",
      "code_anchor": "com.devapprove.a.ru.news.ui.LauncherActivity（AndroidManifest.xml 声明）；res/values/strings.xml#app_name"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.devapprove.a.ru.news.ui.AccessibilityGuideActivity（@style/DTheme，excludeFromRecents，singleInstance，noHistory）",
      "trigger_event": "LauncherActivity 或业务逻辑跳入引导页（noHistory 保证返回不回到该页）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Get Accessibility / To work correctly, your application requires Accessibility rights. See how to make them.",
      "shown_text_zh": "“获取无障碍权限”“为正常使用，你的应用需要无障碍权限。查看如何开启。”并配鼠标/手指轨迹动画演示",
      "user_action_requested": "点击进入教学/跳转按钮（页面为单向前进式，未见跳过或取消文案）",
      "code_anchor": "assets/unique.html；com.devapprove.a.ru.news.ui.AccessibilityGuideActivity"
    },
    {
      "step": 3,
      "stage": "引导说明页（品牌伪装版）",
      "screen_or_component": "WebView 教学页（同一引导流程的另一套模板）",
      "trigger_event": "引导页加载本地 chrome.html 或后续步骤点击“下一步”",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "1. Open accessibility settings / 2. Select Chrome / GO TO SETTINGS",
      "shown_text_zh": "“1. 打开无障碍设置　2. 选择 Chrome　3. 前往设置（GO TO SETTINGS）”三步教学，并引导在系统列表中选择名为 Chrome 的服务",
      "user_action_requested": "点击 GO TO SETTINGS 按钮（未见取消/跳过按钮）",
      "code_anchor": "assets/chrome.html"
    },
    {
      "step": 4,
      "stage": "引导说明页（原生弹窗版）",
      "screen_or_component": "原生 Dialog / 全屏提示（文案来自 strings.xml，承载类位于加密载荷）",
      "trigger_event": "冷启动或功能触发时弹出权限提示",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Update app accesses / Enable access for \"Chrome\"",
      "shown_text_zh": "标题“更新应用访问权限”，正文“为 Chrome 开启访问权限”，以版本更新/权限刷新为名索取无障碍",
      "user_action_requested": "点击确认进入设置（文案中无“取消”“稍后”“跳过”）",
      "code_anchor": "res/values/strings.xml#enable_accessibility_title、#enable_accessibility_message"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（ACTION_ACCESSIBILITY_SETTINGS 目标），列表项显示为 Chrome",
      "trigger_event": "引导页按钮/弹窗确认回调中启动 Settings.ACTION_ACCESSIBILITY_SETTINGS（跳转代码在加密载荷内，DEX 中无该 action 字符串）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Chrome / Service allows Accessibility for Android to scan your device for accessibility issues.",
      "shown_text_zh": "系统无障碍列表中服务名为 Chrome，说明文字为“允许 Accessibility for Android 扫描设备的无障碍问题”（伪装成辅助检查工具）",
      "user_action_requested": "要求用户手动找到 Chrome 条目并拨动开关启用；说明文字故意弱化“读取屏幕内容与模拟点击”的实际能力",
      "code_anchor": "res/xml/accessibilityservice.xml；res/values/strings.xml#accessibility_service_label、#accessibility_service_description"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.devapprove.a.ru.news.service.OverlayService（悬浮窗）＋ AccessibilityActivity（导出的全屏透明页）",
      "trigger_event": "进入设置页后由悬浮窗/透明 Activity 叠层提示操作位置（具体时序在加密载荷内，静态不可确认）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "1. Open the Accessibility settings / 2. Select Enable Accessibility Service / 3. Slide the switch to enable",
      "shown_text_zh": "“1. 打开无障碍设置　2. 选择启用无障碍服务　3. 滑动开关启用”三步操作指引叠在系统设置页上方",
      "user_action_requested": "按指引在系统页面手动拨动开关（指引层未提供取消/返回选项）",
      "code_anchor": "res/values/strings.xml#str1、#str2、#str3；com.devapprove.a.ru.news.service.OverlayService；com.devapprove.a.ru.news.ui.accesses.AccessibilityActivity"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "伪系统检查界面（managing_service_title/message）＋ AccessibilityActivity/PermissionsActivity 重入",
      "trigger_event": "用户在系统设置中返回而未启用时，由 onResume/定时器再次拉起引导（重跳机制位于加密载荷，静态不可确认）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Checking system / Checking",
      "shown_text_zh": "“正在检查系统”“检查中”，以系统自检动画掩盖仍在等待授权，并持续把用户拉回设置流程",
      "user_action_requested": "被迫继续前往设置或停留在引导，未见降级/跳过路径",
      "code_anchor": "res/values/strings.xml#managing_service_title、#managing_service_message；com.devapprove.a.ru.news.ui.accesses.PermissionsActivity"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "AppAccessibilityService（typeAllMask + 读窗 + 手势）＋ NotificationService（通知监听）＋ OverlayService ＋ AdminActivity/MyAdminReceiver（设备管理员）",
      "trigger_event": "AccessibilityService.onServiceConnected 或轮询检测到服务已启用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Allow pop-ups / Checking",
      "shown_text_zh": "获权后弹出“允许弹窗”（小米等厂商悬浮窗授权引导），随后转入静默后台能力",
      "user_action_requested": "可能要求再授予悬浮窗/忽略电池优化/设备管理员，以避免被撤销或卸载（具体动作在加密载荷内）",
      "code_anchor": "com.devapprove.a.ru.news.service.AppAccessibilityService；com.devapprove.a.ru.news.service.NotificationService；com.devapprove.a.ru.news.MyAdminReceiver；res/values/strings.xml#miuipopup"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml#app_name = \"Chrome\"：桌面图标名与无障碍服务 label（AppAccessibilityService 的 android:label 引用 @string/app_name）",
    "res/values/strings.xml#accessibility_service_description：系统无障碍列表条目下方的说明文字，伪装为“扫描无障碍问题”",
    "res/values/strings.xml#enable_accessibility_title / #enable_accessibility_message：冷启动或触发时的原生 Dialog（“Update app accesses” / Enable access for \"Chrome\"）",
    "res/values/strings.xml#str1、#str2、#str3：原生引导页/悬浮窗中的三步操作教学文案",
    "res/values/strings.xml#managing_service_title / #managing_service_message：等待授权期间的伪系统“Checking system”检查界面",
    "assets/unique.html：AccessibilityGuideActivity 承载的 WebView 引导页（Get Accessibility 话术 + 轨迹动画）",
    "assets/chrome.html：WebView 分步教学页（1. Open accessibility settings / 2. Select Chrome / GO TO SETTINGS）",
    "res/values/strings.xml#miuipopup（Allow pop-ups）：获权后引导授予悬浮窗权限的提示"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome",
      "text_zh": "Chrome（浏览器）",
      "source_location": "res/values/strings.xml#app_name、#accessibility_service_label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update app accesses",
      "text_zh": "更新应用访问权限",
      "source_location": "res/values/strings.xml#enable_accessibility_title",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable access for \"Chrome\"",
      "text_zh": "为“Chrome”开启访问权限",
      "source_location": "res/values/strings.xml#enable_accessibility_message",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "text_zh": "该服务允许 Accessibility for Android 扫描你设备的无障碍问题。",
      "source_location": "res/values/strings.xml#accessibility_service_description（被 res/xml/accessibilityservice.xml 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Open the Accessibility settings",
      "text_zh": "1. 打开无障碍设置",
      "source_location": "res/values/strings.xml#str1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. Select Enable Accessibility Service",
      "text_zh": "2. 选择“启用无障碍服务”",
      "source_location": "res/values/strings.xml#str2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "3. Slide the switch to enable",
      "text_zh": "3. 滑动开关以启用",
      "source_location": "res/values/strings.xml#str3",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Get Accessibility",
      "text_zh": "获取无障碍权限",
      "source_location": "assets/unique.html（<title>）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "To work correctly, your application requires Accessibility rights. See how to make them.",
      "text_zh": "为正常使用，你的应用需要无障碍权限。查看如何开启。",
      "source_location": "assets/unique.html",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Open accessibility settings",
      "text_zh": "1. 打开无障碍设置",
      "source_location": "assets/chrome.html",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. Select Chrome",
      "text_zh": "2. 选择 Chrome",
      "source_location": "assets/chrome.html",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "GO TO SETTINGS",
      "text_zh": "前往设置",
      "source_location": "assets/chrome.html",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Checking system",
      "text_zh": "正在检查系统",
      "source_location": "res/values/strings.xml#managing_service_title",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow pop-ups",
      "text_zh": "允许弹出窗口",
      "source_location": "res/values/strings.xml#miuipopup",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无取消路径的字符串设计 + 导出的 AccessibilityActivity/PermissionsActivity（noHistory、全屏透明）与 OverlayService 组合，指向返回设置页后再次拉起引导；但 onResume/定时重跳的具体实现位于加密二阶段载荷（classes.dex 中无相关类与 ACTION_ACCESSIBILITY_SETTINGS 字符串），静态不可确认循环周期与次数",
    "overlay_or_fake_settings": "存在 OverlayService 悬浮窗与 Theme.Translucent/Fullscreen 的导出 Activity，具备叠层指引能力；未见高仿系统无障碍开关页的布局资源（res/layout 下无任何布局文件），叠层形式为悬浮窗或透明页指引，具体样式在加密载荷内",
    "restricted_settings_13plus_coaching": "未见应用详情右上角菜单允许受限设置、也未发现 Session 安装器绕过的静态痕迹（targetSdk 32，Manifest 中无相关字符串与资源）；不排除由加密载荷在运行期下发",
    "post_grant_anti_removal": "具备防撤权/防卸载配套组件：设备管理员（AdminActivity + MyAdminReceiver + res/xml/admin）、NotificationListenerService 通知监听、OverlayService 悬浮窗、RECEIVE_BOOT_COMPLETED + AlarmBroadcastReceiver 自启；是否在获权后自点确认或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权需读取加密载荷，静态不可确认",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 LauncherActivity（Theme.Translucent.NoTitleBar.Fullscreen）后 1–3 秒内出现的首个非透明界面，以及 AccessibilityGuideActivity 启动瞬间；同时挂 ACTION_ACCESSIBILITY_SETTINGS 跳转监测，跳转后立即连拍系统设置页与其上叠加的悬浮窗",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页/教学 WebView 页",
        "page_identifier": "AccessibilityGuideActivity（DTheme，单实例、不留在最近任务）内 WebView 渲染 assets/unique.html 或 assets/chrome.html",
        "why_most_useful": "此处决定是否构成“以 Chrome 品牌伪装 + 假更新话术”诱导，且文案为逐字可比对的静态真值，最能区分诱导与良性透明说明",
        "observable_utg_signals": ["标题 Get Accessibility", "正文 requires Accessibility rights", "1. Open accessibility settings / 2. Select Chrome 分步文案", "GO TO SETTINGS 按钮文本", "页面是否为全屏且无取消/跳过控件"]
      },
      {
        "page_role": "冷启动原生引导弹窗",
        "page_identifier": "原生 Dialog，标题 Update app accesses，正文 Enable access for \"Chrome\"",
        "why_most_useful": "证明引导发生在冷启动 0 步而非用户功能触发，并体现“权限更新”伪装框架与是否可取消",
        "observable_utg_signals": ["标题文本 Update app accesses", "按钮数量与文本（是否存在取消/稍后）", "弹窗是否可返回键关闭"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中名为 Chrome 的服务条目及其描述",
        "why_most_useful": "核对系统侧展示名与描述是否与包名 com.bean.cousin 不符，以及描述是否被弱化",
        "observable_utg_signals": ["服务名 Chrome", "描述 Service allows Accessibility for Android to scan your device", "该条目是否被置顶或高亮"]
      },
      {
        "page_role": "设置页后叠加的引导遮罩/伪检查页",
        "page_identifier": "OverlayService 悬浮窗或 AccessibilityActivity 透明全屏页；文案 1./2./3. 步骤或 Checking system",
        "why_most_useful": "判定是否存在叠层指引与伪系统检查界面，以及用户从设置页返回后是否被立即重跳（拒权循环）",
        "observable_utg_signals": ["悬浮窗/透明页上的步骤文案", "Checking system 文本", "返回后前台 Activity 是否再次变为 AccessibilityActivity/AccessibilityGuideActivity", "重跳间隔与次数"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区在于二阶段载荷：classes.dex 不含任何 com.devapprove 组件类与无障碍跳转字符串，Manifest 声明的业务组件由 DexClassLoader 从 2.3MB 加密资产 assets/CtaDwII.json 解密加载，因此跳转触发点、拒权重跳逻辑、获权后自授权/防撤权动作只能靠运行期 UTG 观测补全；另 OverlayService 悬浮层与 WebView 引导页若为纯图或 Canvas 绘制则需 OCR 辅助。静态资源本身明文可见，不构成加壳遮挡文案的问题。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.devapprove.a.ru.news.ui.AccessibilityGuideActivity",
    "com.devapprove.a.ru.news.service.AppAccessibilityService",
    "res/xml/accessibilityservice.xml",
    "res/values/strings.xml#enable_accessibility_title / #enable_accessibility_message / #str1-#str3",
    "assets/unique.html",
    "assets/chrome.html"
  ]
}
```

**证据边界说明**：以上流程中第 1、2、4、6、7、8 步的界面文案、承载组件与伪装身份均由 Manifest、`res/values/strings.xml`、`res/xml/accessibilityservice.xml`、`assets/unique.html`、`assets/chrome.html` 静态证实；但触发跳转的具体调用点、拒权重跳机制与获权后动作因相关类全部位于加密二阶段载荷（`assets/CtaDwII.json` + `DexClassLoader`）而未能静态闭环，属于未决项，建议按上述 UTG 触发点做运行期补证。受本轮工具调用预算限制，未执行风险台账写入与报告生成。

</details>
