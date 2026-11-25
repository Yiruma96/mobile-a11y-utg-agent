# MB_126__6f7e57ed72｜Sova — Aras Kargo

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：150.9s

## 1. 一句话核心结论

- **核心申请方式**：伪装成土耳其快递品牌 Aras Kargo 的 Sova 家族样本，用空壳全屏 Launcher 冷启动后由 DexClassLoader 加载加密载荷，先弹伪造系统检查框再以‘Update app accesses’三步教学把用户引导进无障碍设置，并在设置页叠加悬浮指引索权，无障碍服务在系统列表中被直接命名为 Aras Kargo。
- **静态可见性说明**：Manifest 组件、无障碍配置、全部诱导文案 strings 与空布局可见；但 com.tapston.burgerking.* 全部实现类（LauncherActivity、AccessibilityActivity、AppAccessibilityService、OverlayService）不在两个 DEX 中，classes.dex 仅含 DexClassLoader/Base64/zip 与 com.armed.little 随机名类，assets 下有 2.29MB 不透明 QM.json 与 509KB chrome.html，判定为二阶段加密/动态加载载荷，跳转逻辑与遮罩实现不可静态还原
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6f7e57ed7239905fafc3947160b5fc89ad615772d2a694299999d2fe080453f4` |
| 包名 / 年份 | `com.armed.little` / 2023 |
| 家族 / 品类 | **Sova**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Aras Kargo |
| 引导页宣称品牌/身份 | Aras Kargo（土耳其真实快递物流品牌，被冒用） |
| 系统无障碍列表服务名 | Aras Kargo |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:label 直接使用 @string/app_name（Aras Kargo），使系统无障碍列表项与应用图标同名，用户无法区分是在给第三方木马授权；android:description 借用开源 Accessibility Insights 文案洗白为‘扫描无障碍问题’；引导标题伪装成系统更新 Update app accesses、进度框伪装成 Checking system；授权页布局 activity_grant_accessibility.xml 为空 ConstraintLayout，真实界面运行期构建；LauncherActivity 为 Translucent+singleInstance+excludeFromRecents+noHistory，启动即隐去自身痕迹 |
| 无障碍服务类名 | `com.tapston.burgerking.service.AppAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tapston.burgerking.ui.LauncherActivity（Theme.Translucent.NoTitleBar.Fullscreen, singleInstance, excludeFromRecents, noHistory） | 用户点击桌面图标（android.intent.action.MAIN/LAUNCHER） | 原生Activity | 无 | 仅点击图标；页面无取消/跳过入口，且 excludeFromRecents 使最近任务中不留痕迹 | `AndroidManifest.xml application/activity[com.tapston.burgerking.ui.LauncherActivity]` |
| 2 | 引导说明页 | 运行期载荷内的 Dialog（伪装系统检查进度） | 载荷由 DexClassLoader 解密加载完成后由业务代码弹出 | 原生Dialog | **原文**：Checking system / Checking<br>**译注**：“正在检查系统”/“检查中”，伪装成系统自检过程 | 等待检查完成（无实际检查动作，仅制造‘系统正在处理’的心理预期） | `res/values/strings.xml#managing_service_title, #managing_service_message` |
| 3 | 引导说明页 | 权限引导弹窗/引导页（标题伪装为系统更新），承载 str1–str4 文案 | 检查框消失后立即展示（冷启动 0 步，无业务前置） | 原生Dialog | **原文**：Update app accesses / Enable access for "Aras Kargo" / 1. Open the Accessibility settings / 2. Select Enable Accessibility Service / 3. Slide the switch to enable / 4. Accessibility service must be enabled to protect your data!<br>**译注**：“更新应用访问权限”/“为 Aras Kargo 启用访问”/1.打开无障碍设置 2.选择 Enable Accessibility Service 3.拨动开关启用 4.必须启用无障碍服务才能保护您的数据！ | 按三步图文指引前往设置并开启服务；文案以‘必须’定性，无跳过/暂不开启选项 | `res/values/strings.xml#enable_accessibility_title, #enable_accessibility_message, #str1, #str2, #str3, #str4` |
| 4 | 跳无障碍设置 | com.tapston.burgerking.ui.AccessibilityActivity（Theme.Light.NoTitleBar.Fullscreen, noHistory, exported）→ 系统 Settings.ACTION_ACCESSIBILITY_SETTINGS 页 | 引导页确认按钮点击后由载荷内代码 startActivity 跳转（Intent 常量在加密载荷中，静态不可见） | 系统无障碍页 | **原文**：无（页面本身为空布局 activity_grant_accessibility.xml）<br>**译注**：应用侧无自有界面，直接把用户送到系统无障碍设置列表，列表中可见与 App 同名的 “Aras Kargo” 服务项 | 在系统列表中找到 Aras Kargo 并点入、开启开关；该步无应用侧取消入口 | `res/layout/activity_grant_accessibility.xml; AndroidManifest.xml activity[com.tapston.burgerking.ui.accesses.AccessibilityActivity]` |
| 5 | 遮罩叠层指引 | com.tapston.burgerking.service.OverlayService（SYSTEM_ALERT_WINDOW 悬浮窗），前置需 MIUI 弹出窗口权限 | 跳转设置同时或 onResume 后由服务拉起悬浮窗；未获悬浮窗权限时弹出伪装系统弹窗索取 | 悬浮窗Overlay | **原文**：Allow pop-ups<br>**译注**：“允许弹出窗口”——伪装成 MIUI 系统权限弹窗标题，引导用户授予悬浮窗以叠加设置页指引 | 允许悬浮窗权限，以便在系统设置页上方显示下一步操作指引 | `res/values/strings.xml#miuipopup; AndroidManifest.xml service[com.tapston.burgerking.service.OverlayService]` |
| 6 | 拒权反馈循环 | com.tapston.burgerking.ui.BlankActivity / BrowserActivity（Theme.Light.NoTitleBar.Fullscreen, noHistory） | 用户从系统设置返回但未开启服务时由主流程再次拉起（具体判定代码在加密载荷内） | 原生Activity | **原文**：无（BlankActivity 无内容；引导文案复用 str1–str4）<br>**译注**：以全屏空白页或内嵌页重新承接，配合 noHistory 让返回键无法退出，循环回到第 3–4 步继续索权 | 再次被要求前往设置开启无障碍；无安全降级路径 | `AndroidManifest.xml activity[com.tapston.burgerking.ui.BlankActivity], activity[com.tapston.burgerking.ui.BrowserActivity]` |
| 7 | 获权后动作 | com.tapston.burgerking.service.AppAccessibilityService（label=@string/app_name, BIND_ACCESSIBILITY_SERVICE, canRetrieveWindowContent=true, canPerformGestures=true, typeAllMask） | 系统绑定服务后 onServiceConnected（实现类在加密载荷内） | 不可静态还原 | 无 | 无需用户操作（权限已到手） | `res/xml/accessibilityservice.xml; AndroidManifest.xml service[com.tapston.burgerking.service.AppAccessibilityService]` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml#managing_service_title / #managing_service_message —— 运行期原生 Dialog，伪装系统检查进度（Checking system / Checking）
- res/values/strings.xml#enable_accessibility_title / #enable_accessibility_message —— 权限引导弹窗标题与正文（Update app accesses / Enable access for "Aras Kargo"）
- res/values/strings.xml#str1–#str4 —— 无障碍开启三步教学与‘必须开启’恐吓句，随引导弹窗/引导页呈现
- res/values/strings.xml#miuipopup —— 索取悬浮窗权限时伪装 MIUI 系统弹窗标题 Allow pop-ups
- res/values/strings.xml#accessibility_service_label / #app_name —— 系统无障碍服务列表项名称，直接显示为 Aras Kargo
- res/xml/accessibilityservice.xml#android:description（→@string/accessibility_service_description）—— 系统无障碍详情页的能力说明，洗白为‘扫描无障碍问题’
- res/layout/activity_grant_accessibility.xml —— 授权页布局为空 ConstraintLayout，说明真实引导界面由运行期注入/构建
- com.tapston.burgerking.service.OverlayService —— 跳设置后覆盖在系统无障碍页之上的悬浮指引层（布局在加密载荷内）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Update app accesses | 更新应用访问权限 | `res/values/strings.xml#enable_accessibility_title` | 假更新 |
| en | Enable access for "Aras Kargo" | 为 “Aras Kargo” 启用访问权限 | `res/values/strings.xml#enable_accessibility_message` | 教唆忽视警告 |
| en | 1. Open the Accessibility settings | 1. 打开无障碍设置 | `res/values/strings.xml#str1` | 受限设置分步教学 |
| en | 2. Select Enable Accessibility Service | 2. 选择 Enable Accessibility Service | `res/values/strings.xml#str2` | 受限设置分步教学 |
| en | 3. Slide the switch to enable | 3. 拨动开关以启用 | `res/values/strings.xml#str3` | 受限设置分步教学 |
| en | 4. Accessibility service must be enabled to protect your data! | 4. 必须启用无障碍服务才能保护您的数据！ | `res/values/strings.xml#str4` | 假反诈安全 |
| en | Checking system | 正在检查系统 | `res/values/strings.xml#managing_service_title` | 故障恐吓 |
| en | Checking | 检查中 | `res/values/strings.xml#managing_service_message` | 故障恐吓 |
| en | Allow pop-ups | 允许弹出窗口 | `res/values/strings.xml#miuipopup` | 教唆忽视警告 |
| en | Service allows Accessibility for Android to scan your device for accessibility issues. | 该服务允许 Accessibility for Android 扫描您设备的无障碍问题。 | `res/values/strings.xml#accessibility_service_description（res/xml/accessibilityservice.xml 引用）` | 隐私承诺 |
| tr | Aras Kargo | Aras Kargo（土耳其真实快递品牌名，被冒用为应用名与无障碍服务名） | `res/values/strings.xml#app_name, #accessibility_service_label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户从系统设置返回但未开启服务时，由 BlankActivity/BrowserActivity（全屏无标题、noHistory）再次承接并复用 str1–str4 重新引导跳转；noHistory 与 LauncherActivity 的 excludeFromRecents 使用户无法通过返回键或最近任务退出该流程（具体判定与重跳代码位于加密载荷内，静态不可见）
- **遮罩叠层 / 高仿系统设置页**：是。OverlayService 以 SYSTEM_ALERT_WINDOW 在系统无障碍设置页之上叠悬浮指引层，并先以伪装 MIUI 弹窗 “Allow pop-ups” 索取悬浮窗权限；另有 “Checking system/Checking” 伪装系统自检框，但未发现高仿系统无障碍开关页的静态证据（该界面可能在载荷内）
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk=32，未见应用详情右上角‘允许受限设置’或 Session 安装器绕过的静态文案）
- **获权后即时行为与防撤权机制**：不可静态还原：AppAccessibilityService 具备 typeAllMask/canPerformGestures/canRetrieveWindowContent，载荷内可能通过 GLOBAL_ACTION_BACK 阻止撤权，但静态无证据
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两个时机同时拉起：①冷启动点击图标后 0–3 秒（LauncherActivity 透明空壳阶段，捕获 ‘Checking system’ 伪检查框与 ‘Update app accesses’ 三步教学弹窗）；②监测到 Settings.ACTION_ACCESSIBILITY_SETTINGS 跳转后立即抓屏，并在 500–1500ms 后再抓一次以捕获 OverlayService 压在设置页上的悬浮指引
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著静态盲区：应用全部业务与引导实现类（com.tapston.burgerking.*）不在两个 DEX 中，classes.dex 仅保留 DexClassLoader/Base64/zip 加载器与 com.armed.little 随机名类，assets 下 2.29MB QM.json、509KB chrome.html 为可疑二阶段载荷；跳转 Intent 常量、onResume 重跳判定、悬浮窗布局、获权后抗撤权逻辑均藏于该加密/动态加载层内，静态只能确认装置与文案。纯运行期 UTG 不受此限制，但若载荷依赖云端下发才展示引导，则冷启动可能静默，需结合流量侧观察。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动伪系统检查弹窗页** | 无标题栏 Dialog，文本 Checking system / Checking，宿主为透明全屏 Activity（最近任务中无该页） | 证明诱导在 0 步冷启动即发起、且以伪造系统自检为前提，是‘假系统故障’话术的直接运行证据 | Dialog 标题文本 Checking system；无取消/关闭按钮；宿主窗口为 Translucent 全屏且 excludeFromRecents |
| **跳转前无障碍开启三步教学弹窗/引导页** | 标题 Update app accesses，正文含 ‘Enable access for "Aras Kargo"’ 与 1./2./3. 分步条目 | 这是‘如何一步步引导用户开启无障碍’的核心页面，可逐字核对分步教学与‘必须开启才能保护数据’的恐吓/安全话术 | 标题伪装为系统更新；存在编号 1/2/3 步骤文本；缺失‘跳过/暂不开启’按钮；文本中同时出现品牌名 Aras Kargo |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务中出现名为 ‘Aras Kargo’ 的条目，与应用图标同名 | 直接证明服务名冒用品牌、与系统提示‘可读取全部内容’形成对照，是身份混淆最客观的运行证据 | 服务条目文本 == 应用名 Aras Kargo；系统风险提示‘可查看和控制屏幕/读取内容’；条目描述为 scan your device for accessibility issues |
| **设置页后悬浮指引遮罩页** | 系统无障碍设置页上层出现半透明全屏或浮层引导（OverlayService），前置可能先出现 ‘Allow pop-ups’ 授权弹窗 | 区分‘正常跳设置’与‘设置页压栈遮罩强制指引’，是判定诱导强度与是否存在遮挡/劫持的关键 | 设置页 UI 被非系统浮层覆盖；浮层含手形/箭头指向开关的指引元素；出现 Allow pop-ups 授权弹窗文本 |
| **拒绝返回后的重跳循环页** | 从设置返回后再次出现全屏无标题空白页/内嵌页并迅速回到教学弹窗 | 证明无跳过路径且返回键无法脱离，是‘不可取消+循环重跳’的运行时证据 | 连续多次出现同一教学弹窗；返回键后界面立即复原；无安全降级或手动模式入口 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `res/values/strings.xml#enable_accessibility_title / #enable_accessibility_message / #str1 / #str2 / #str3 / #str4`
- `res/values/strings.xml#managing_service_title / #managing_service_message / #miuipopup`
- `res/values/strings.xml#app_name / #accessibility_service_label / #accessibility_service_description`
- `res/xml/accessibilityservice.xml（canRetrieveWindowContent=true, canPerformGestures=true, typeAllMask）`
- `AndroidManifest.xml#activity[com.tapston.burgerking.ui.LauncherActivity] / #activity[com.tapston.burgerking.ui.accesses.AccessibilityActivity] / #service[com.tapston.burgerking.service.OverlayService] / #service[com.tapston.burgerking.service.AppAccessibilityService]`
- `res/layout/activity_grant_accessibility.xml（空 ConstraintLayout，真实引导界面运行期注入）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论

**关键发现：应用自身业务代码不在 DEX 中，无障碍诱导链的运行期代码处于加密或动态加载载荷内**

- **Manifest 明示了一套完整诱导装置**：[AndroidManifest.xml](<resource-unit:#1 manifest:components>) 声明 `LauncherActivity`（`Theme.Translucent.NoTitleBar.Fullscreen`、`singleInstance`、`excludeFromRecents`、`noHistory`）、`AccessibilityActivity`（`Theme.Light.NoTitleBar.Fullscreen`、exported）、`BlankActivity`、`BrowserActivity`、`OverlayService`，以及带 `BIND_ACCESSIBILITY_SERVICE` 的 `AppAccessibilityService`。
- **但 `com.tapston.burgerking.*` 全部类在两个 DEX 中均不存在**：`classes.dex` 与 `classes2.dex` 里连 `tapston`/`burgerking` 字符串都没有；MCP 对 `AppAccessibilityService` 返回 `Class not found`，`search_text_in_app` 对 `AccessibilityService`/`ACTION_ACCESSIBILITY_SETTINGS` 均无命中。两个 DEX 中实际只有 `com.armed.little`（150 个随机名类）、`com.stripe.android`、`com.github.mikephil.charting`。
- `classes.dex` 含 `DexClassLoader`、`dalvik/system`、`Base64`、`zip`，`assets` 下有 2.29 MB 不透明 [assets/QM.json](<resource-unit:#1 file:assets/QM.json>) 与 509 KB [assets/chrome.html](<resource-unit:#1 file:assets/chrome.html>)。即 Sova 家族的典型二阶段：加密载荷随包，运行期解密后由 `DexClassLoader` 加载 `com.tapston.burgerking.*`，再执行无障碍服务与引导 UI。
- **残留的明文字符串与资源完整暴露了诱导文案与页面语义**（这是本次可静态确认的核心证据）：
  - 分步教学 `str1`–`str3`：打开无障碍设置 → 选择 Enable Accessibility Service → 拨动开关；`str4`：必须开启否则“保护你的数据”。
  - 伪装系统弹窗 `managing_service_title` = “Checking system”、`managing_service_message` = “Checking”；
  - 权限索取标题 `enable_accessibility_title` = “Update app accesses”、正文 `enable_accessibility_message` = `Enable access for "Aras Kargo"`；
  - `miuipopup` = “Allow pop-ups”（MIUI 悬浮窗授权伪装标题）；
  - 无障碍服务在系统列表中的名称被设为 **“Aras Kargo”**（与 `app_name` 相同，冒用土耳其 Aras Kargo 快递品牌），描述却写成 “Service allows Accessibility for Android to scan your device for accessibility issues.” —— 完全不提 `canRetrieveWindowContent`/`canPerformGestures`/`typeAllMask` 的实际能力。
  - `activity_grant_accessibility.xml` 为**空 ConstraintLayout**，说明授权页真实 UI 由运行期动态构建/注入，而非静态布局。

**还原的运行期 UTG 页面流转（依据资源语义 + Manifest 组件组合推断，代码本体在载荷内）**

1. 冷启动 → `LauncherActivity`（全屏半透明、不在最近任务中显示，无可见界面）→ 动态加载载荷；
2. 载荷内先弹伪装系统检查框 “Checking system / Checking”；
3. 引导页/弹窗给出三步无障碍开启教学，标题伪装成系统更新 “Update app accesses”；
4. 跳系统无障碍设置页（预期由 `AccessibilityActivity` 发起），`OverlayService` + `SYSTEM_ALERT_WINDOW` 在设置页之上叠悬浮指引/遮罩；若用户拒绝悬浮窗，用 “Allow pop-ups” 弹窗索取；
5. 返回后由 `BlankActivity`/`BrowserActivity`（全屏无标题、`noHistory`）承接，`noHistory` 设计使拒绝后返回键难以退出，形成重跳循环；
6. 获权后 `AppAccessibilityService` 以 `typeAllMask` + `canRetrieveWindowContent` + `canPerformGestures` 读取全部窗口内容并执行手势（后续为银行木马式覆盖/自动操作）。

**证据边界**：跳转 Intent 常量、`onResume` 死循环、遮罩具体布局、是否自点确认，均位于加密载荷内，静态无法还原；本次仅确认了装置、文案与能力声明。建议在真机冷启动后以 “跳转 ACCESSIBILITY_SETTINGS / 冷启动直弹框” 两个时机抓取 UTG。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest 组件、无障碍配置、全部诱导文案 strings 与空布局可见；但 com.tapston.burgerking.* 全部实现类（LauncherActivity、AccessibilityActivity、AppAccessibilityService、OverlayService）不在两个 DEX 中，classes.dex 仅含 DexClassLoader/Base64/zip 与 com.armed.little 随机名类，assets 下有 2.29MB 不透明 QM.json 与 509KB chrome.html，判定为二阶段加密/动态加载载荷，跳转逻辑与遮罩实现不可静态还原",
  "summary_one_liner": "伪装成土耳其快递品牌 Aras Kargo 的 Sova 家族样本，用空壳全屏 Launcher 冷启动后由 DexClassLoader 加载加密载荷，先弹伪造系统检查框再以‘Update app accesses’三步教学把用户引导进无障碍设置，并在设置页叠加悬浮指引索权，无障碍服务在系统列表中被直接命名为 Aras Kargo。",
  "disguise_identity": {
    "app_display_name": "Aras Kargo",
    "claimed_brand_or_persona": "Aras Kargo（土耳其真实快递物流品牌，被冒用）",
    "a11y_service_label": "Aras Kargo",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:label 直接使用 @string/app_name（Aras Kargo），使系统无障碍列表项与应用图标同名，用户无法区分是在给第三方木马授权；android:description 借用开源 Accessibility Insights 文案洗白为‘扫描无障碍问题’；引导标题伪装成系统更新 Update app accesses、进度框伪装成 Checking system；授权页布局 activity_grant_accessibility.xml 为空 ConstraintLayout，真实界面运行期构建；LauncherActivity 为 Translucent+singleInstance+excludeFromRecents+noHistory，启动即隐去自身痕迹"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tapston.burgerking.ui.LauncherActivity（Theme.Translucent.NoTitleBar.Fullscreen, singleInstance, excludeFromRecents, noHistory）",
      "trigger_event": "用户点击桌面图标（android.intent.action.MAIN/LAUNCHER）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全屏半透明空壳页，无可读文本，用户看不到任何品牌界面即进入后续流程",
      "user_action_requested": "仅点击图标；页面无取消/跳过入口，且 excludeFromRecents 使最近任务中不留痕迹",
      "code_anchor": "AndroidManifest.xml application/activity[com.tapston.burgerking.ui.LauncherActivity]"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "运行期载荷内的 Dialog（伪装系统检查进度）",
      "trigger_event": "载荷由 DexClassLoader 解密加载完成后由业务代码弹出",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Checking system / Checking",
      "shown_text_zh": "“正在检查系统”/“检查中”，伪装成系统自检过程",
      "user_action_requested": "等待检查完成（无实际检查动作，仅制造‘系统正在处理’的心理预期）",
      "code_anchor": "res/values/strings.xml#managing_service_title, #managing_service_message"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "权限引导弹窗/引导页（标题伪装为系统更新），承载 str1–str4 文案",
      "trigger_event": "检查框消失后立即展示（冷启动 0 步，无业务前置）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Update app accesses / Enable access for \"Aras Kargo\" / 1. Open the Accessibility settings / 2. Select Enable Accessibility Service / 3. Slide the switch to enable / 4. Accessibility service must be enabled to protect your data!",
      "shown_text_zh": "“更新应用访问权限”/“为 Aras Kargo 启用访问”/1.打开无障碍设置 2.选择 Enable Accessibility Service 3.拨动开关启用 4.必须启用无障碍服务才能保护您的数据！",
      "user_action_requested": "按三步图文指引前往设置并开启服务；文案以‘必须’定性，无跳过/暂不开启选项",
      "code_anchor": "res/values/strings.xml#enable_accessibility_title, #enable_accessibility_message, #str1, #str2, #str3, #str4"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "com.tapston.burgerking.ui.AccessibilityActivity（Theme.Light.NoTitleBar.Fullscreen, noHistory, exported）→ 系统 Settings.ACTION_ACCESSIBILITY_SETTINGS 页",
      "trigger_event": "引导页确认按钮点击后由载荷内代码 startActivity 跳转（Intent 常量在加密载荷中，静态不可见）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（页面本身为空布局 activity_grant_accessibility.xml）",
      "shown_text_zh": "应用侧无自有界面，直接把用户送到系统无障碍设置列表，列表中可见与 App 同名的 “Aras Kargo” 服务项",
      "user_action_requested": "在系统列表中找到 Aras Kargo 并点入、开启开关；该步无应用侧取消入口",
      "code_anchor": "res/layout/activity_grant_accessibility.xml; AndroidManifest.xml activity[com.tapston.burgerking.ui.accesses.AccessibilityActivity]"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.tapston.burgerking.service.OverlayService（SYSTEM_ALERT_WINDOW 悬浮窗），前置需 MIUI 弹出窗口权限",
      "trigger_event": "跳转设置同时或 onResume 后由服务拉起悬浮窗；未获悬浮窗权限时弹出伪装系统弹窗索取",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Allow pop-ups",
      "shown_text_zh": "“允许弹出窗口”——伪装成 MIUI 系统权限弹窗标题，引导用户授予悬浮窗以叠加设置页指引",
      "user_action_requested": "允许悬浮窗权限，以便在系统设置页上方显示下一步操作指引",
      "code_anchor": "res/values/strings.xml#miuipopup; AndroidManifest.xml service[com.tapston.burgerking.service.OverlayService]"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.tapston.burgerking.ui.BlankActivity / BrowserActivity（Theme.Light.NoTitleBar.Fullscreen, noHistory）",
      "trigger_event": "用户从系统设置返回但未开启服务时由主流程再次拉起（具体判定代码在加密载荷内）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（BlankActivity 无内容；引导文案复用 str1–str4）",
      "shown_text_zh": "以全屏空白页或内嵌页重新承接，配合 noHistory 让返回键无法退出，循环回到第 3–4 步继续索权",
      "user_action_requested": "再次被要求前往设置开启无障碍；无安全降级路径",
      "code_anchor": "AndroidManifest.xml activity[com.tapston.burgerking.ui.BlankActivity], activity[com.tapston.burgerking.ui.BrowserActivity]"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.tapston.burgerking.service.AppAccessibilityService（label=@string/app_name, BIND_ACCESSIBILITY_SERVICE, canRetrieveWindowContent=true, canPerformGestures=true, typeAllMask）",
      "trigger_event": "系统绑定服务后 onServiceConnected（实现类在加密载荷内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务静默运行，读取全部窗口内容并执行手势模拟；后续覆盖/自动操作界面不可静态还原",
      "user_action_requested": "无需用户操作（权限已到手）",
      "code_anchor": "res/xml/accessibilityservice.xml; AndroidManifest.xml service[com.tapston.burgerking.service.AppAccessibilityService]"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml#managing_service_title / #managing_service_message —— 运行期原生 Dialog，伪装系统检查进度（Checking system / Checking）",
    "res/values/strings.xml#enable_accessibility_title / #enable_accessibility_message —— 权限引导弹窗标题与正文（Update app accesses / Enable access for \"Aras Kargo\"）",
    "res/values/strings.xml#str1–#str4 —— 无障碍开启三步教学与‘必须开启’恐吓句，随引导弹窗/引导页呈现",
    "res/values/strings.xml#miuipopup —— 索取悬浮窗权限时伪装 MIUI 系统弹窗标题 Allow pop-ups",
    "res/values/strings.xml#accessibility_service_label / #app_name —— 系统无障碍服务列表项名称，直接显示为 Aras Kargo",
    "res/xml/accessibilityservice.xml#android:description（→@string/accessibility_service_description）—— 系统无障碍详情页的能力说明，洗白为‘扫描无障碍问题’",
    "res/layout/activity_grant_accessibility.xml —— 授权页布局为空 ConstraintLayout，说明真实引导界面由运行期注入/构建",
    "com.tapston.burgerking.service.OverlayService —— 跳设置后覆盖在系统无障碍页之上的悬浮指引层（布局在加密载荷内）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Update app accesses",
      "text_zh": "更新应用访问权限",
      "source_location": "res/values/strings.xml#enable_accessibility_title",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable access for \"Aras Kargo\"",
      "text_zh": "为 “Aras Kargo” 启用访问权限",
      "source_location": "res/values/strings.xml#enable_accessibility_message",
      "rhetorical_frame": "教唆忽视警告"
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
      "text_zh": "2. 选择 Enable Accessibility Service",
      "source_location": "res/values/strings.xml#str2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "3. Slide the switch to enable",
      "text_zh": "3. 拨动开关以启用",
      "source_location": "res/values/strings.xml#str3",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "4. Accessibility service must be enabled to protect your data!",
      "text_zh": "4. 必须启用无障碍服务才能保护您的数据！",
      "source_location": "res/values/strings.xml#str4",
      "rhetorical_frame": "假反诈安全"
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
      "text_verbatim": "Checking",
      "text_zh": "检查中",
      "source_location": "res/values/strings.xml#managing_service_message",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow pop-ups",
      "text_zh": "允许弹出窗口",
      "source_location": "res/values/strings.xml#miuipopup",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "text_zh": "该服务允许 Accessibility for Android 扫描您设备的无障碍问题。",
      "source_location": "res/values/strings.xml#accessibility_service_description（res/xml/accessibilityservice.xml 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "tr",
      "text_verbatim": "Aras Kargo",
      "text_zh": "Aras Kargo（土耳其真实快递品牌名，被冒用为应用名与无障碍服务名）",
      "source_location": "res/values/strings.xml#app_name, #accessibility_service_label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户从系统设置返回但未开启服务时，由 BlankActivity/BrowserActivity（全屏无标题、noHistory）再次承接并复用 str1–str4 重新引导跳转；noHistory 与 LauncherActivity 的 excludeFromRecents 使用户无法通过返回键或最近任务退出该流程（具体判定与重跳代码位于加密载荷内，静态不可见）",
    "overlay_or_fake_settings": "是。OverlayService 以 SYSTEM_ALERT_WINDOW 在系统无障碍设置页之上叠悬浮指引层，并先以伪装 MIUI 弹窗 “Allow pop-ups” 索取悬浮窗权限；另有 “Checking system/Checking” 伪装系统自检框，但未发现高仿系统无障碍开关页的静态证据（该界面可能在载荷内）",
    "restricted_settings_13plus_coaching": "无（targetSdk=32，未见应用详情右上角‘允许受限设置’或 Session 安装器绕过的静态文案）",
    "post_grant_anti_removal": "不可静态还原：AppAccessibilityService 具备 typeAllMask/canPerformGestures/canRetrieveWindowContent，载荷内可能通过 GLOBAL_ACTION_BACK 阻止撤权，但静态无证据",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两个时机同时拉起：①冷启动点击图标后 0–3 秒（LauncherActivity 透明空壳阶段，捕获 ‘Checking system’ 伪检查框与 ‘Update app accesses’ 三步教学弹窗）；②监测到 Settings.ACTION_ACCESSIBILITY_SETTINGS 跳转后立即抓屏，并在 500–1500ms 后再抓一次以捕获 OverlayService 压在设置页上的悬浮指引",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动伪系统检查弹窗页",
        "page_identifier": "无标题栏 Dialog，文本 Checking system / Checking，宿主为透明全屏 Activity（最近任务中无该页）",
        "why_most_useful": "证明诱导在 0 步冷启动即发起、且以伪造系统自检为前提，是‘假系统故障’话术的直接运行证据",
        "observable_utg_signals": ["Dialog 标题文本 Checking system", "无取消/关闭按钮", "宿主窗口为 Translucent 全屏且 excludeFromRecents"]
      },
      {
        "page_role": "跳转前无障碍开启三步教学弹窗/引导页",
        "page_identifier": "标题 Update app accesses，正文含 ‘Enable access for \"Aras Kargo\"’ 与 1./2./3. 分步条目",
        "why_most_useful": "这是‘如何一步步引导用户开启无障碍’的核心页面，可逐字核对分步教学与‘必须开启才能保护数据’的恐吓/安全话术",
        "observable_utg_signals": ["标题伪装为系统更新", "存在编号 1/2/3 步骤文本", "缺失‘跳过/暂不开启’按钮", "文本中同时出现品牌名 Aras Kargo"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务中出现名为 ‘Aras Kargo’ 的条目，与应用图标同名",
        "why_most_useful": "直接证明服务名冒用品牌、与系统提示‘可读取全部内容’形成对照，是身份混淆最客观的运行证据",
        "observable_utg_signals": ["服务条目文本 == 应用名 Aras Kargo", "系统风险提示‘可查看和控制屏幕/读取内容’", "条目描述为 scan your device for accessibility issues"]
      },
      {
        "page_role": "设置页后悬浮指引遮罩页",
        "page_identifier": "系统无障碍设置页上层出现半透明全屏或浮层引导（OverlayService），前置可能先出现 ‘Allow pop-ups’ 授权弹窗",
        "why_most_useful": "区分‘正常跳设置’与‘设置页压栈遮罩强制指引’，是判定诱导强度与是否存在遮挡/劫持的关键",
        "observable_utg_signals": ["设置页 UI 被非系统浮层覆盖", "浮层含手形/箭头指向开关的指引元素", "出现 Allow pop-ups 授权弹窗文本"]
      },
      {
        "page_role": "拒绝返回后的重跳循环页",
        "page_identifier": "从设置返回后再次出现全屏无标题空白页/内嵌页并迅速回到教学弹窗",
        "why_most_useful": "证明无跳过路径且返回键无法脱离，是‘不可取消+循环重跳’的运行时证据",
        "observable_utg_signals": ["连续多次出现同一教学弹窗", "返回键后界面立即复原", "无安全降级或手动模式入口"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著静态盲区：应用全部业务与引导实现类（com.tapston.burgerking.*）不在两个 DEX 中，classes.dex 仅保留 DexClassLoader/Base64/zip 加载器与 com.armed.little 随机名类，assets 下 2.29MB QM.json、509KB chrome.html 为可疑二阶段载荷；跳转 Intent 常量、onResume 重跳判定、悬浮窗布局、获权后抗撤权逻辑均藏于该加密/动态加载层内，静态只能确认装置与文案。纯运行期 UTG 不受此限制，但若载荷依赖云端下发才展示引导，则冷启动可能静默，需结合流量侧观察。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "res/values/strings.xml#enable_accessibility_title / #enable_accessibility_message / #str1 / #str2 / #str3 / #str4",
    "res/values/strings.xml#managing_service_title / #managing_service_message / #miuipopup",
    "res/values/strings.xml#app_name / #accessibility_service_label / #accessibility_service_description",
    "res/xml/accessibilityservice.xml（canRetrieveWindowContent=true, canPerformGestures=true, typeAllMask）",
    "AndroidManifest.xml#activity[com.tapston.burgerking.ui.LauncherActivity] / #activity[com.tapston.burgerking.ui.accesses.AccessibilityActivity] / #service[com.tapston.burgerking.service.OverlayService] / #service[com.tapston.burgerking.service.AppAccessibilityService]",
    "res/layout/activity_grant_accessibility.xml（空 ConstraintLayout，真实引导界面运行期注入）"
  ]
}
```

**说明与边界**：本次按 14 次工具调用上限收口，未执行 `record_risk` 登记与报告生成。若需要项目风险台账，可将上述“无障碍诱导授权 + 品牌冒用 + 伪装系统检查/更新话术 + 设置页悬浮遮罩 + 无跳过循环”作为独立命题登记（risk_family 建议 `malware_trojan` 或 `deceptive_behavior`，severity `high`），证据图起点用 Manifest 组件与 strings 资源、终点指向 `AppAccessibilityService` 配置与 `OverlayService` 声明，并将加密载荷（`assets/QM.json`、`DexClassLoader` 加载器）作为 visibility 缺口分支标注。

</details>
