# MB_125__bbaf483c2b｜Sova — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：175.2s

## 1. 一句话核心结论

- **核心申请方式**：冒名 Chrome 的恶意样本以本地 HTML WebView 假‘浏览器更新成功’+按机型定制的三步无障碍教学，配以‘开启无障碍才能保护数据’的假安全弹窗，把用户一步步引导到系统无障碍页开启名为 Chrome 的高权限服务，真正驱动跳转的代码藏于加密 DEX 载荷。
- **静态可见性说明**：引导文案与教学页（assets/chrome.html）、原生 strings/layout、无障碍服务配置均明文可见；但 Manifest 声明的 by.onliner.catalog.* 全部 Activity/Service（含 LauncherActivity、AccessibilityGuideActivity、OverlayService、AppAccessibilityService 及 JS 桥 finishInject）在 classes.dex/classes2.dex 中不存在，classes.dex 含 Dalvik/system/DexClassLoader 字符串，assets/imbb.json 为 2.3MB 高熵加密载荷，跳转与循环逻辑属运行期解密的二阶段 DEX，静态不可还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `bbaf483c2b6f67f22eb6e1fa00f200e9c1e201b0110070acaefd416cf846b1aa` |
| 包名 / 年份 | `com.crop.horse` / 2023 |
| 家族 / 品类 | **Sova**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Google Chrome（浏览器更新/无障碍服务） |
| 系统无障碍列表服务名 | Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.crop.horse 与代码命名空间 by.onliner.catalog 冒充 Google Chrome；无障碍 description 使用通用‘scan your device for accessibility issues’话术掩盖 canRetrieveWindowContent/canPerformGestures/typeAllMask 高危能力；LauncherActivity 为 Theme.Translucent.NoTitleBar.Fullscreen 且 excludeFromRecents，弱化‘已安装应用’的可见性；无 activity-alias 或多别名伪装（未发现）；无伪造 isAccessibilityTool 字段（配置未声明） |
| 无障碍服务类名 | `by.onliner.catalog.service.AppAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | by.onliner.catalog.ui.LauncherActivity（android.intent.category.LAUNCHER，singleInstance、noHistory、Theme.Translucent.NoTitleBar.Fullscreen、excludeFromRecents） | 用户点击桌面图标启动（onCreate） | 不可静态还原 | 无 | 点击桌面图标 | `AndroidManifest.xml: by.onliner.catalog.ui.LauncherActivity（类体不在 classes.dex/classes2.dex）` |
| 2 | 引导说明页 | by.onliner.catalog.ui.AccessibilityGuideActivity / BrowserActivity 承载的本地 WebView（assets/chrome.html） | 冷启动或由加密载荷调起后加载本地 HTML（loadUrl 实现不可静态还原） | 本地HTML WebView | **原文**：Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. / 1. Open settings / 2. Select Accessibility / 3. Slide the switch to enable / CONTINUE<br>**译注**：欢迎使用 Chrome / 浏览器已更新成功 / 要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务 / 1. 打开设置 / 2. 选择无障碍 / 3. 滑动开关以启用 / 继续 | 仅提供 CONTINUE 按钮（onclick=Android.finishInject()），页面无取消或跳过入口 | `assets/chrome.html#L239-L277；Manifest: by.onliner.catalog.ui.AccessibilityGuideActivity` |
| 3 | 跳受限设置 | 系统无障碍设置页（预期 ACTION_ACCESSIBILITY_SETTINGS），由 WebView JS 桥 Android.finishInject() 触发 | 点击 CONTINUE 调用 finishInject() | 系统无障碍页 | 无 | 点击 CONTINUE 后离开应用进入系统设置 | `assets/chrome.html#L248-L277（onclick="Android.finishInject();"）；JS 桥实现不可静态还原` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载/已安装的服务列表项 “Chrome” | 进入系统无障碍列表 | 系统无障碍页 | **原文**：Chrome / Service allows Accessibility for Android to scan your device for accessibility issues.<br>**译注**：Chrome / 该服务允许 Android 无障碍功能扫描您设备上的无障碍问题 | 在该列表项上滑动开关启用服务 | `res/xml/accessibilityservice.xml#L2；res/values/strings.xml#L31-L34` |
| 5 | 遮罩叠层指引 | by.onliner.catalog.service.OverlayService + res/layout/overlay_loading.xml | 服务启动后显示悬浮/全屏遮罩（触发点不可静态还原） | 悬浮窗Overlay | **原文**：Android is starting ...<br>**译注**：Android 正在启动……（黑底白字全屏，伪造系统启动/异常状态） | 无明确按钮，属伪造系统状态的遮盖层 | `res/layout/overlay_loading.xml；Manifest: by.onliner.catalog.service.OverlayService` |
| 6 | 拒权反馈循环 | 原生引导弹窗（guide_layout.xml：str0-str3 + OK）与字符串 enable_accessibility_title/message | 检测到未开启无障碍时弹出（判定逻辑在加密载荷内） | 原生Dialog | **原文**：Update app accesses / Enable access for "Chrome" / Accessibility service must be enabled to protect your data!<br>**译注**：更新应用访问权限 / 为“Chrome”启用访问权限 / 必须启用无障碍服务才能保护你的数据！ | 点击 OK 前往开启；是否存在重复弹出/死循环不可静态确认 | `res/values/strings.xml#L54-L64；res/layout/guide_layout.xml` |
| 7 | 获权后动作 | by.onliner.catalog.service.AppAccessibilityService（typeAllMask、flagRequestTouchExplorationMode、canPerformGestures） | 服务被系统绑定后 onServiceConnected（实现不可静态还原） | 不可静态还原 | 无 | 无 | `res/xml/accessibilityservice.xml#L2；Manifest: by.onliner.catalog.service.AppAccessibilityService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets/chrome.html（本地 WebView 教学页）：Welcome to Chrome / Browser updated successfully / To use this application, click the "Continue" button and then enable Chrome services. + 三步教程 + CONTINUE 按钮
- assets/chrome.html 内嵌 objLang 多语言字典（es/fr/hu/el 等），并通过 translate.googleapis.com 实时翻译页面文字
- res/values/strings.xml：enable_accessibility_title="Update app accesses"、enable_accessibility_message='Enable access for "Chrome"'（原生弹窗标题/正文）
- res/values/strings.xml：str1/str2/str3/str4（原生分步教学与“必须开启才能保护数据”恐吓文案），渲染于 res/layout/guide_layout.xml 的 str1-str3 TextView 与 OK 按钮
- 系统无障碍服务列表项：label "Chrome"（@string/app_name / accessibility_service_label）+ android:description "Service allows Accessibility for Android to scan your device for accessibility issues."
- res/layout/overlay_loading.xml 全屏黑底遮罩文字 "Android is starting ..."（OverlayService 悬浮层）
- com.cow.s.n.NotifyGuideActivity 通知权限 Lottie 引导（assets/notify_p/notify_p_guide.json，layout permission_guide_layout），非无障碍引导但同属权限索取视觉引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Welcome to Chrome | 欢迎使用 Chrome | `assets/chrome.html#L239 (#welcome)` | 假更新 |
| en | Browser updated successfully | 浏览器已更新成功 | `assets/chrome.html#L241 (#updated)` | 假更新 |
| en | To use this application, click the "Continue" button and then enable Chrome services. | 要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务。 | `assets/chrome.html#L243 (#manual0)` | 受限设置分步教学 |
| en | 1. Open settings / 2. Select Accessibility / 3. Slide the switch to enable | 1. 打开设置 / 2. 选择无障碍 / 3. 滑动开关以启用 | `assets/chrome.html#L262-L270（另有 strings.xml str1-str3）` | 受限设置分步教学 |
| en | Go to Installed apps / Go to Downloaded apps / Go to Accessibility features / Find and enable <pkgname> | 进入已安装应用 / 进入已下载应用 / 进入无障碍功能 / 找到并启用 <包名> | `assets/chrome.html#L306-L313（m5、m5_1、m6、m7、m8，按 model 含 oppo/xiaomi 分支改写）` | 受限设置分步教学 |
| en | Update app accesses | 更新应用访问权限 | `res/values/strings.xml#L55 (enable_accessibility_title)` | 假更新 |
| en | Enable access for "Chrome" | 为“Chrome”启用访问权限 | `res/values/strings.xml#L54 (enable_accessibility_message)` | 假更新 |
| en | Accessibility service must be enabled to protect your data! | 必须启用无障碍服务才能保护你的数据！ | `res/values/strings.xml#L64 (str4)` | 假反诈安全 |
| en | Service allows Accessibility for Android to scan your device for accessibility issues. | 该服务允许 Android 无障碍功能扫描您设备上的无障碍问题。 | `res/values/strings.xml#L31 → res/xml/accessibilityservice.xml android:description` | 隐私承诺 |
| en | Android is starting ... | Android 正在启动…… | `res/layout/overlay_loading.xml` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态确认：判定与重跳逻辑位于加密二阶段 DEX（by.onliner.catalog.* 类体缺失），无法静态核实是否存在 onResume 重跳或定时拉起；明文侧仅见引导弹窗文案与教学页
- **遮罩叠层 / 高仿系统设置页**：存在 by.onliner.catalog.service.OverlayService 与 res/layout/overlay_loading.xml（黑底全屏 "Android is starting ..."），具备伪造系统状态遮罩的素材与通道；是否在系统设置页之上叠放高仿无障碍开关页不可静态确认
- **Android 13+ 受限设置（Restricted Settings）应对**：未发现针对 Android 13+ 受限设置（应用详情→右上角菜单→允许受限设置）或 Session 安装器绕过的明文教学；chrome.html 的教学仅覆盖到‘进入无障碍功能/找到并启用’层级
- **获权后即时行为与防撤权机制**：不可静态确认：无障碍服务已声明 typeAllMask + canPerformGestures，具备用 GLOBAL_ACTION_BACK/HOME 阻止撤权的技术前提，但对应实现位于加密载荷，未见明文证据
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 LauncherActivity 后首次出现全屏 WebView 教学页（含 'Welcome to Chrome' / 'CONTINUE'）或监测到页面文本出现 'Select Accessibility'/'Slide the switch to enable'；其次在 finishInject 触发跳转 ACTION_ACCESSIBILITY_SETTINGS 的瞬间
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：Manifest 声明的 by.onliner.catalog.* 全部类体不在明文 DEX，核心跳转/循环逻辑位于 assets/imbb.json（2.3MB 高熵）经 DexClassLoader 解密加载的二阶段载荷，纯静态无法确认 finishInject 的目标 Intent、拒权重跳机制与获权后反移除行为；另 OverlayService 遮罩文本为纯文本可被 UTG 读取，但若后续改用图片引导则需 OCR。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的本地 HTML 教学页（假浏览器更新）** | 全屏 WebView，文本包含 'Welcome to Chrome'、'Browser updated successfully'、'CONTINUE'，URL 指向 assets/chrome.html 或 file:// 本地路径 | 该页是诱导链的起点与教学载体，文案本身即构成假更新+分步教唆的直接证据 | WebView 显示本地 file:// 或 assets 路径；页面仅有一个 CONTINUE 按钮、无取消/跳过控件；文本含 Chrome 品牌名但应用包名为 com.crop.horse；页面调用 translate.googleapis.com 做多语言改写 |
| **跳转前分步教学区（按机型改写文案）** | 页面内编号列表：'Open settings' / 'Select Accessibility' / 'Slide the switch to enable'，或 OPPO/小米机型的 'Go to Installed apps'、'Find and enable <pkgname>' | 证明教学是按厂商 UI 定制、精确指向无障碍开关路径，而非笼统提示 | 列表项文本随设备型号变化；文案中出现本应用包名/应用名；编号步骤 1-3 与系统无障碍路径一一对应 |
| **系统无障碍服务列表项** | 设置→无障碍→已下载/已安装服务，条目名 'Chrome'，说明为 'scan your device for accessibility issues' | 确认最终被开启的对象是冒名 Chrome 的高权限服务，是身份冒用的落点证据 | 服务名与包名不一致（Chrome vs com.crop.horse）；描述为通用无障碍扫描话术；开关处于关闭并等待用户滑动 |
| **设置页返回后的遮罩/回跳页** | 全屏黑底文字 'Android is starting ...'，或再次出现教学页/引导弹窗 | 区分是否存在拒权循环与伪造系统状态遮盖，是判定强迫性最关键的一环（静态不可确认） | 从设置返回后 1-3 秒内重复弹出引导；出现 TYPE_APPLICATION_OVERLAY 悬浮层；遮罩文本为系统启动/异常类文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `assets/chrome.html#L239-L277（假更新 + 三步无障碍教学 + CONTINUE→Android.finishInject()）`
- `res/xml/accessibilityservice.xml#L2（typeAllMask / canRetrieveWindowContent / canPerformGestures）`
- `res/values/strings.xml#L31-L34（accessibility_service_label=Chrome、app_name=Chrome、通用扫描描述）`
- `res/values/strings.xml#L54-L64（Update app accesses / Enable access for "Chrome" / protect your data / str1-str3 教学）`
- `res/layout/overlay_loading.xml（黑底全屏 "Android is starting ..." 伪造系统状态遮罩）`
- `AndroidManifest.xml: by.onliner.catalog.ui.LauncherActivity / AccessibilityGuideActivity / service.OverlayService / service.AppAccessibilityService（类体在加密载荷中，静态不可还原）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**1. 身份伪装已经明确（静态可证）**
- `app_name` 与无障碍服务 label 均为 **"Chrome"**（[res/values/strings.xml (L32-L34)](<resource-unit:#1 file:res/values/strings.xml#L32-L34>)），但包名为 `com.crop.horse`，实际代码命名空间为 `by.onliner.catalog`，与 Google Chrome 无关 → 属品牌冒名。
- 系统无障碍列表中展示的说明被写成通用“无障碍扫描”措辞：`Service allows Accessibility for Android to scan your device for accessibility issues.`（[accessibilityservice.xml (L2)](<resource-unit:#1 file:res/xml/accessibilityservice.xml#L2>)），刻意弱化“读取窗口内容 + 执行手势”的高危能力（`canRetrieveWindowContent=true`、`canPerformGestures=true`、`typeAllMask`）。

**2. 引导文案与教学页静态可见（本地 HTML）**
- 包内存在本地教学页 [assets/chrome.html (L239-L277)](<resource-unit:#1 file:assets/chrome.html#L239-L277>)：以 “Welcome to Chrome / Browser updated successfully” 假更新开场，随后给出 **1. Open settings → 2. Select Accessibility → 3. Slide the switch to enable** 的分步教程，并有按机型/包名动态改写的分支（`m1`–`m8`：`Go to Installed apps`、`Go to Additional Settings`、`Go to Accessibility features`、`Go to Downloaded apps`、`Find and enable <pkgname>`），页面唯一按钮为 `CONTINUE`（`onclick="Android.finishInject()"`），**无取消/跳过**。这正是“按厂商 UI 差异化教学开启无障碍”的典型实现。
- 另有原生引导字符串族 `str1`–`str4`（[strings.xml (L61-L64)](<resource-unit:#1 file:res/values/strings.xml#L61-L64>)，其中 `Accessibility service must be enabled to protect your data!` 属假安全恐吓）与 `enable_accessibility_title="Update app accesses"` / `enable_accessibility_message='Enable access for "Chrome"'`（L54-L55，假更新弹窗文案），配套布局 `guide_layout.xml`（含 `str0`–`str3`、`OK` 按钮）。

**3. 承载跳转的驱动代码不在明文 DEX 中**
- Manifest 声明了 `by.onliner.catalog.ui.LauncherActivity`（LAUNCHER，Translucent 全屏、`excludeFromRecents`）、`ui.accesses.AccessibilityActivity`、`ui.AccessibilityGuideActivity`、`ui.BrowserActivity`、`service.OverlayService`、`service.AppAccessibilityService` 等（[#1 manifest:components](<resource-unit:#1 manifest:components>)），但 `classes.dex`/`classes2.dex` 中**检索不到 `by.onliner` 任何类**；同时 `classes.dex` 含 `Ldalvik/system/DexClassLoader;` 字符串，包内 `assets/imbb.json` 为 2.3MB 高熵二进制。综合判断：真正执行 `ACTION_ACCESSIBILITY_SETTINGS` 跳转、悬浮遮罩与拒权重跳的逻辑位于**运行期解密的二阶段 DEX 载荷**中，静态不可还原。
- 明文可见的 `OverlayService` 配套布局 [res/layout/overlay_loading.xml](<resource-unit:#1 file:res/layout/overlay_loading.xml>) 内容为黑底白字 `Android is starting ...`，即伪造系统启动/故障的遮罩素材。

**4. 可判定的诱导链（运行期 UTG 视角）**
冷启动（Translucent 全屏 LauncherActivity，无正常桌面图标态）→ 本地 WebView 教学页（假“Chrome 更新成功”，分机型三步教学，仅 CONTINUE）→ 跳系统无障碍设置 → 系统列表内以 “Chrome” 名义出现并被要求开启 → 获权后由无障碍服务执行读取窗口/手势（后续动作逻辑在加密载荷内）。原生 `NotifyGuideActivity`（`com.cow.s.n`）为**通知权限**的 Lottie 引导，`onTouchEvent`/`onKeyDown` 均直接 `finish()`，可取消，不属无障碍强迫链。

**未决/覆盖边界**：`by.onliner.*` 全部类体（含 `finishInject` 桥、拒权 `onResume` 重跳、获权后反移除）未静态获取；`assets/imbb.json` 未解密还原。故“是否存在拒权死循环、是否叠放高仿设置页、是否 13+ 受限设置分步教唆”只能标为不可静态确认。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "引导文案与教学页（assets/chrome.html）、原生 strings/layout、无障碍服务配置均明文可见；但 Manifest 声明的 by.onliner.catalog.* 全部 Activity/Service（含 LauncherActivity、AccessibilityGuideActivity、OverlayService、AppAccessibilityService 及 JS 桥 finishInject）在 classes.dex/classes2.dex 中不存在，classes.dex 含 Dalvik/system/DexClassLoader 字符串，assets/imbb.json 为 2.3MB 高熵加密载荷，跳转与循环逻辑属运行期解密的二阶段 DEX，静态不可还原。",
  "summary_one_liner": "冒名 Chrome 的恶意样本以本地 HTML WebView 假‘浏览器更新成功’+按机型定制的三步无障碍教学，配以‘开启无障碍才能保护数据’的假安全弹窗，把用户一步步引导到系统无障碍页开启名为 Chrome 的高权限服务，真正驱动跳转的代码藏于加密 DEX 载荷。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Google Chrome（浏览器更新/无障碍服务）",
    "a11y_service_label": "Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.crop.horse 与代码命名空间 by.onliner.catalog 冒充 Google Chrome；无障碍 description 使用通用‘scan your device for accessibility issues’话术掩盖 canRetrieveWindowContent/canPerformGestures/typeAllMask 高危能力；LauncherActivity 为 Theme.Translucent.NoTitleBar.Fullscreen 且 excludeFromRecents，弱化‘已安装应用’的可见性；无 activity-alias 或多别名伪装（未发现）；无伪造 isAccessibilityTool 字段（配置未声明）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "by.onliner.catalog.ui.LauncherActivity（android.intent.category.LAUNCHER，singleInstance、noHistory、Theme.Translucent.NoTitleBar.Fullscreen、excludeFromRecents）",
      "trigger_event": "用户点击桌面图标启动（onCreate）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该类在明文 DEX 中不存在，实际冷启动界面不可静态获取；Manifest 仅显示为全屏半透明无标题窗口",
      "user_action_requested": "点击桌面图标",
      "code_anchor": "AndroidManifest.xml: by.onliner.catalog.ui.LauncherActivity（类体不在 classes.dex/classes2.dex）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "by.onliner.catalog.ui.AccessibilityGuideActivity / BrowserActivity 承载的本地 WebView（assets/chrome.html）",
      "trigger_event": "冷启动或由加密载荷调起后加载本地 HTML（loadUrl 实现不可静态还原）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Welcome to Chrome / Browser updated successfully / To use this application, click the \"Continue\" button and then enable Chrome services. / 1. Open settings / 2. Select Accessibility / 3. Slide the switch to enable / CONTINUE",
      "shown_text_zh": "欢迎使用 Chrome / 浏览器已更新成功 / 要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务 / 1. 打开设置 / 2. 选择无障碍 / 3. 滑动开关以启用 / 继续",
      "user_action_requested": "仅提供 CONTINUE 按钮（onclick=Android.finishInject()），页面无取消或跳过入口",
      "code_anchor": "assets/chrome.html#L239-L277；Manifest: by.onliner.catalog.ui.AccessibilityGuideActivity"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统无障碍设置页（预期 ACTION_ACCESSIBILITY_SETTINGS），由 WebView JS 桥 Android.finishInject() 触发",
      "trigger_event": "点击 CONTINUE 调用 finishInject()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳转代码位于加密二阶段 DEX，静态不可还原；HTML 中所有可点击元素均绑定 Android.finishInject()",
      "user_action_requested": "点击 CONTINUE 后离开应用进入系统设置",
      "code_anchor": "assets/chrome.html#L248-L277（onclick=\"Android.finishInject();\"）；JS 桥实现不可静态还原"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载/已安装的服务列表项 “Chrome”",
      "trigger_event": "进入系统无障碍列表",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Chrome / Service allows Accessibility for Android to scan your device for accessibility issues.",
      "shown_text_zh": "Chrome / 该服务允许 Android 无障碍功能扫描您设备上的无障碍问题",
      "user_action_requested": "在该列表项上滑动开关启用服务",
      "code_anchor": "res/xml/accessibilityservice.xml#L2；res/values/strings.xml#L31-L34"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "by.onliner.catalog.service.OverlayService + res/layout/overlay_loading.xml",
      "trigger_event": "服务启动后显示悬浮/全屏遮罩（触发点不可静态还原）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Android is starting ...",
      "shown_text_zh": "Android 正在启动……（黑底白字全屏，伪造系统启动/异常状态）",
      "user_action_requested": "无明确按钮，属伪造系统状态的遮盖层",
      "code_anchor": "res/layout/overlay_loading.xml；Manifest: by.onliner.catalog.service.OverlayService"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "原生引导弹窗（guide_layout.xml：str0-str3 + OK）与字符串 enable_accessibility_title/message",
      "trigger_event": "检测到未开启无障碍时弹出（判定逻辑在加密载荷内）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Update app accesses / Enable access for \"Chrome\" / Accessibility service must be enabled to protect your data!",
      "shown_text_zh": "更新应用访问权限 / 为“Chrome”启用访问权限 / 必须启用无障碍服务才能保护你的数据！",
      "user_action_requested": "点击 OK 前往开启；是否存在重复弹出/死循环不可静态确认",
      "code_anchor": "res/values/strings.xml#L54-L64；res/layout/guide_layout.xml"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "by.onliner.catalog.service.AppAccessibilityService（typeAllMask、flagRequestTouchExplorationMode、canPerformGestures）",
      "trigger_event": "服务被系统绑定后 onServiceConnected（实现不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后可读取全部窗口内容并执行手势，用于后续读取短信/联系人/覆盖银行页面等动作，具体实现在加密载荷中",
      "user_action_requested": "无",
      "code_anchor": "res/xml/accessibilityservice.xml#L2；Manifest: by.onliner.catalog.service.AppAccessibilityService"
    }
  ],
  "text_presentation_locations": [
    "assets/chrome.html（本地 WebView 教学页）：Welcome to Chrome / Browser updated successfully / To use this application, click the \"Continue\" button and then enable Chrome services. + 三步教程 + CONTINUE 按钮",
    "assets/chrome.html 内嵌 objLang 多语言字典（es/fr/hu/el 等），并通过 translate.googleapis.com 实时翻译页面文字",
    "res/values/strings.xml：enable_accessibility_title=\"Update app accesses\"、enable_accessibility_message='Enable access for \"Chrome\"'（原生弹窗标题/正文）",
    "res/values/strings.xml：str1/str2/str3/str4（原生分步教学与“必须开启才能保护数据”恐吓文案），渲染于 res/layout/guide_layout.xml 的 str1-str3 TextView 与 OK 按钮",
    "系统无障碍服务列表项：label \"Chrome\"（@string/app_name / accessibility_service_label）+ android:description \"Service allows Accessibility for Android to scan your device for accessibility issues.\"",
    "res/layout/overlay_loading.xml 全屏黑底遮罩文字 \"Android is starting ...\"（OverlayService 悬浮层）",
    "com.cow.s.n.NotifyGuideActivity 通知权限 Lottie 引导（assets/notify_p/notify_p_guide.json，layout permission_guide_layout），非无障碍引导但同属权限索取视觉引导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Welcome to Chrome",
      "text_zh": "欢迎使用 Chrome",
      "source_location": "assets/chrome.html#L239 (#welcome)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Browser updated successfully",
      "text_zh": "浏览器已更新成功",
      "source_location": "assets/chrome.html#L241 (#updated)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "To use this application, click the \"Continue\" button and then enable Chrome services.",
      "text_zh": "要使用本应用，请点击“继续”按钮，然后启用 Chrome 服务。",
      "source_location": "assets/chrome.html#L243 (#manual0)",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Open settings / 2. Select Accessibility / 3. Slide the switch to enable",
      "text_zh": "1. 打开设置 / 2. 选择无障碍 / 3. 滑动开关以启用",
      "source_location": "assets/chrome.html#L262-L270（另有 strings.xml str1-str3）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to Installed apps / Go to Downloaded apps / Go to Accessibility features / Find and enable <pkgname>",
      "text_zh": "进入已安装应用 / 进入已下载应用 / 进入无障碍功能 / 找到并启用 <包名>",
      "source_location": "assets/chrome.html#L306-L313（m5、m5_1、m6、m7、m8，按 model 含 oppo/xiaomi 分支改写）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Update app accesses",
      "text_zh": "更新应用访问权限",
      "source_location": "res/values/strings.xml#L55 (enable_accessibility_title)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable access for \"Chrome\"",
      "text_zh": "为“Chrome”启用访问权限",
      "source_location": "res/values/strings.xml#L54 (enable_accessibility_message)",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service must be enabled to protect your data!",
      "text_zh": "必须启用无障碍服务才能保护你的数据！",
      "source_location": "res/values/strings.xml#L64 (str4)",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "text_zh": "该服务允许 Android 无障碍功能扫描您设备上的无障碍问题。",
      "source_location": "res/values/strings.xml#L31 → res/xml/accessibilityservice.xml android:description",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Android is starting ...",
      "text_zh": "Android 正在启动……",
      "source_location": "res/layout/overlay_loading.xml",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态确认：判定与重跳逻辑位于加密二阶段 DEX（by.onliner.catalog.* 类体缺失），无法静态核实是否存在 onResume 重跳或定时拉起；明文侧仅见引导弹窗文案与教学页",
    "overlay_or_fake_settings": "存在 by.onliner.catalog.service.OverlayService 与 res/layout/overlay_loading.xml（黑底全屏 \"Android is starting ...\"），具备伪造系统状态遮罩的素材与通道；是否在系统设置页之上叠放高仿无障碍开关页不可静态确认",
    "restricted_settings_13plus_coaching": "未发现针对 Android 13+ 受限设置（应用详情→右上角菜单→允许受限设置）或 Session 安装器绕过的明文教学；chrome.html 的教学仅覆盖到‘进入无障碍功能/找到并启用’层级",
    "post_grant_anti_removal": "不可静态确认：无障碍服务已声明 typeAllMask + canPerformGestures，具备用 GLOBAL_ACTION_BACK/HOME 阻止撤权的技术前提，但对应实现位于加密载荷，未见明文证据",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 LauncherActivity 后首次出现全屏 WebView 教学页（含 'Welcome to Chrome' / 'CONTINUE'）或监测到页面文本出现 'Select Accessibility'/'Slide the switch to enable'；其次在 finishInject 触发跳转 ACTION_ACCESSIBILITY_SETTINGS 的瞬间",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的本地 HTML 教学页（假浏览器更新）",
        "page_identifier": "全屏 WebView，文本包含 'Welcome to Chrome'、'Browser updated successfully'、'CONTINUE'，URL 指向 assets/chrome.html 或 file:// 本地路径",
        "why_most_useful": "该页是诱导链的起点与教学载体，文案本身即构成假更新+分步教唆的直接证据",
        "observable_utg_signals": ["WebView 显示本地 file:// 或 assets 路径", "页面仅有一个 CONTINUE 按钮、无取消/跳过控件", "文本含 Chrome 品牌名但应用包名为 com.crop.horse", "页面调用 translate.googleapis.com 做多语言改写"]
      },
      {
        "page_role": "跳转前分步教学区（按机型改写文案）",
        "page_identifier": "页面内编号列表：'Open settings' / 'Select Accessibility' / 'Slide the switch to enable'，或 OPPO/小米机型的 'Go to Installed apps'、'Find and enable <pkgname>'",
        "why_most_useful": "证明教学是按厂商 UI 定制、精确指向无障碍开关路径，而非笼统提示",
        "observable_utg_signals": ["列表项文本随设备型号变化", "文案中出现本应用包名/应用名", "编号步骤 1-3 与系统无障碍路径一一对应"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已下载/已安装服务，条目名 'Chrome'，说明为 'scan your device for accessibility issues'",
        "why_most_useful": "确认最终被开启的对象是冒名 Chrome 的高权限服务，是身份冒用的落点证据",
        "observable_utg_signals": ["服务名与包名不一致（Chrome vs com.crop.horse）", "描述为通用无障碍扫描话术", "开关处于关闭并等待用户滑动"]
      },
      {
        "page_role": "设置页返回后的遮罩/回跳页",
        "page_identifier": "全屏黑底文字 'Android is starting ...'，或再次出现教学页/引导弹窗",
        "why_most_useful": "区分是否存在拒权循环与伪造系统状态遮盖，是判定强迫性最关键的一环（静态不可确认）",
        "observable_utg_signals": ["从设置返回后 1-3 秒内重复弹出引导", "出现 TYPE_APPLICATION_OVERLAY 悬浮层", "遮罩文本为系统启动/异常类文案"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：Manifest 声明的 by.onliner.catalog.* 全部类体不在明文 DEX，核心跳转/循环逻辑位于 assets/imbb.json（2.3MB 高熵）经 DexClassLoader 解密加载的二阶段载荷，纯静态无法确认 finishInject 的目标 Intent、拒权重跳机制与获权后反移除行为；另 OverlayService 遮罩文本为纯文本可被 UTG 读取，但若后续改用图片引导则需 OCR。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "assets/chrome.html#L239-L277（假更新 + 三步无障碍教学 + CONTINUE→Android.finishInject()）",
    "res/xml/accessibilityservice.xml#L2（typeAllMask / canRetrieveWindowContent / canPerformGestures）",
    "res/values/strings.xml#L31-L34（accessibility_service_label=Chrome、app_name=Chrome、通用扫描描述）",
    "res/values/strings.xml#L54-L64（Update app accesses / Enable access for \"Chrome\" / protect your data / str1-str3 教学）",
    "res/layout/overlay_loading.xml（黑底全屏 \"Android is starting ...\" 伪造系统状态遮罩）",
    "AndroidManifest.xml: by.onliner.catalog.ui.LauncherActivity / AccessibilityGuideActivity / service.OverlayService / service.AppAccessibilityService（类体在加密载荷中，静态不可还原）"
  ]
}
```

</details>
