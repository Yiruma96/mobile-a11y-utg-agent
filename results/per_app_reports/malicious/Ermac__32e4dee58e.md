# MB_007__32e4dee58e｜Ermac — HookAPP

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：134.3s

## 1. 一句话核心结论

- **核心申请方式**：应用以 HookAPP 上架，冷启动即用 WindowManager 全屏 WebView 悬浮层把无障碍开关改称“Chrome Update Service”并按系统语言显示伪造“启用”按钮，点击后跳 ACTION_ACCESSIBILITY_SETTINGS 并同时压入第二层 WebView 教学页，配合 isAccessibilityTool=true 绕过 Android 13 受限设置、按返回键即重弹形成死循环。
- **静态可见性说明**：Manifest、无障碍服务配置、WebView 悬浮层构建、ACTION_ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS 跳转、vutapokutaso 教学页压栈、拒权回跳循环与 36 语种伪造开关文案均完整静态可见；仅引导 HTML 正文由 m3.e 懒加载 Provider 运行期提供（dirate$b/$c.o() 反编译返回空串），正文排版需运行期抓取。样本未加壳、无 VMP、无加密二阶段 DEX。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `32e4dee58ea17addc5df4ffb862ab3a8df1697598cb6437f92de4075665812c2` |
| 包名 / 年份 | `com.gejalevubakupa.sugi` / 2024 |
| 家族 / 品类 | **Ermac**（同池样本数：14） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | HookAPP |
| 引导页宣称品牌/身份 | Chrome Update Service（伪装成 Chrome 浏览器更新服务/系统更新组件） |
| 系统无障碍列表服务名 | HookAPPService |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置伪造 android:isAccessibilityTool="true" 冒充系统无障碍工具以规避 Android 13+ 受限设置；内置 Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram 共 10 个 activity-alias（enabled=false，带官方图标）指向同一 duso，可随时改头换面；主 Activity 为透明主题+excludeFromRecents+noHistory，界面以 type=2006 悬浮窗呈现不进入任务栈；应用整体类名/资源名随机化（com.nadebumazoyi.dowaxuca.*、pehibova.xml）；无障碍描述使用“先关闭再打开”话术而非功能说明。 |
| 无障碍服务类名 | `com.nadebumazoyi.dowaxuca.muduyicigumaga.risudunururi` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | If accessibility permission has been on, please turn off then turn on. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.gejalevubakupa.sugi.duso（继承 com.nadebumazoyi.dowaxuca.dirate，透明主题 @style/ACL，excludeFromRecents+noHistory） | 用户点击桌面图标 HookAPP（MAIN/LAUNCHER）→ onCreate | 原生Activity | 无 | 无（无感知进入） | `com.nadebumazoyi.dowaxuca.dirate#onCreate` |
| 2 | 遮罩叠层指引 | WindowManager.addView 全屏 WebView 悬浮层（LayoutParams(-1,-1,type=2,flags=262144,-2)），含 JavascriptInterface "Android" | onResume → s()；判定 d2.a.a(context)==false（无障碍未开启）且 z==true | 悬浮窗Overlay | **原文**：Chrome Update Service / Enable（zh:启用, ru:Включить, fr:Activer, ar:يُمكّن …共36语种）<br>**译注**：把无障碍开关的服务名替换为“Chrome 更新服务”，并提供本地化“启用”按钮，外观模拟系统设置页 | 点击伪造的“启用”开关（页面无取消/关闭入口） | `com.nadebumazoyi.dowaxuca.dirate#s + k3.g（w 多语种词表、d/e/f HTML 片段）` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（列表项 HookAPPService） | 悬浮层 JS 经 "Android" 接口回调 → k3.d.c() → k3.d.b() | 系统无障碍页 | **原文**：If accessibility permission has been on, please turn off then turn on.<br>**译注**：“如果无障碍权限已开启，请先关闭再重新打开。”——以故障修复口吻促使反复操作，不说明任何功能用途 | 在系统无障碍列表中找到 HookAPPService 并开启（服务名与“Chrome 更新服务”不一致，无解释） | `k3.d#b + res/values/strings.xml#text_accessibility_service_description` |
| 4 | 跳转后压栈教学页 | com.nadebumazoyi.dowaxuca.nakulafefo.vutapokutaso（WebView Activity，NEW_TASK，SDK≥29 或小米另加 0x20000/0x800000） | k3.d.b() 在 startActivity(ACCESSIBILITY_SETTINGS) 之后立刻 startActivity(vutapokutaso) | 本地HTML WebView | **原文**：（正文由 m3.e 懒加载 Provider 运行期注入，静态视图为空串）<br>**译注**：在系统设置页之上叠加应用自己的 WebView 指引页，边跳系统页边演示如何勾选开关 | 按页面指引在设置页勾选服务开关 | `k3.d#b + com.nadebumazoyi.dowaxuca.nakulafefo.vutapokutaso#onCreate` |
| 5 | 拒权反馈循环 | dirate.onBackPressed → s()；onResume → s() | 用户在设置页未开启即返回，或按物理返回键离开当前界面 | 悬浮窗Overlay | **原文**：Chrome Update Service / Enable<br>**译注**：返回后立即重新弹出“Chrome 更新服务”全屏悬浮层并再次跳转设置页，直到无障碍被开启 | 无取消、无跳过、无“稍后再说”，只能开启或杀进程 | `com.nadebumazoyi.dowaxuca.dirate#onBackPressed + dirate#onResume` |
| 6 | 获权后动作 | com.nadebumazoyi.dowaxuca.muduyicigumaga.risudunururi（AccessibilityService，isAccessibilityTool=true）+ com.nadebumazoyi.dowaxuca.nakulafefo.decinakometuguzo（前台通知） | 无障碍服务连接后；监听设置页/安装器事件 | 系统无障碍页 | **原文**：Chrome Update Service<br>**译注**：在设置页按文本“Chrome Update Service”定位节点并执行 GLOBAL_ACTION_BACK 退出设置页（自点确认/防撤权），并持续监听设置页与安装器 | 用户无需操作；应用自动回退设置页并阻断撤权路径 | `com.nadebumazoyi.dowaxuca.muduyicigumaga.risudunururi#h / #i + decinakometuguzo#onStartCommand` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动后 WindowManager.addView 的全屏 WebView 悬浮层（dirate#s 内 loadDataWithBaseURL(null, html, "text/html", "UTF-8", null)，覆盖在桌面/任何前台应用之上）
- 上述 HTML 中被字符串替换的占位符 %Enable_Accessibility_Service% → "Chrome Update Service"，开关按钮文案取自 k3.g.w 的 36 语种映射
- 跳转 ACCESSIBILITY_SETTINGS 后立即压栈的 vutapokutaso WebView Activity（第二层教学/指引页）
- 系统无障碍服务列表项：label="HookAPPService"、android:description="If accessibility permission has been on, please turn off then turn on."
- 应用内无任何原生 Dialog/layout 文案（应用主题为 Theme.Translucent.NoTitleBar，界面全部由 WebView 承载）
- 获权后前台通知由 decinakometuguzo#onStartCommand 拼接 " Chrome Update Service" 维持伪装

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Chrome Update Service | Chrome 更新服务 | `com.nadebumazoyi.dowaxuca.dirate#s 内 f4.i.T(..., "%Enable_Accessibility_Service%", "Chrome Update Service")` | 假更新 |
| en | Enable | 启用 | `k3.g.w（多语种映射 en:Enable）` | 假更新 |
| zh | 启用 | 启用 | `k3.g.w（多语种映射 zh:启用）` | 假更新 |
| ru | Включить | 开启 | `k3.g.w（多语种映射 ru:Включить）` | 假更新 |
| en | If accessibility permission has been on, please turn off then turn on. | 如果无障碍权限已经开启，请先关闭再重新打开。 | `res/values/strings.xml key=text_accessibility_service_description（被 res/xml/pehibova.xml 的 android:description 引用）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：onResume 与 onBackPressed 均无条件调用 s()：用户从系统设置页返回或按返回键，立即重新以 WindowManager 添加全屏 WebView 悬浮层并再次 startActivity(ACCESSIBILITY_SETTINGS)，无任何退出分支，直至无障碍服务被开启；仅当 Intent 携带 FromPush=true 或 HTML 源为空时 z 才置 false 暂停遮罩。
- **遮罩叠层 / 高仿系统设置页**：是。以 LayoutParams(-1,-1,type=2,flags=262144,-2) 的全屏 WebView 悬浮层覆盖屏幕，HTML 内把服务名替换为“Chrome Update Service”、按钮文案按 36 种语言本地化，外观模拟系统无障碍开关页；跳转设置后再叠加 vutapokutaso WebView 教学页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无显式“应用详情→右上角菜单→允许受限设置”文字教学，但通过在 res/xml/pehibova.xml 中伪造 android:isAccessibilityTool="true" 与 accessibilityDataSensitive="no"，使该服务被系统当作无障碍工具，直接绕过 Android 13+ 对非无障碍工具服务的受限设置拦截。
- **获权后即时行为与防撤权机制**：是。无障碍服务 risudunururi 的 h()/i() 用 findAccessibilityNodeInfosByText("Chrome Update Service") 定位设置页节点，并以 GLOBAL_ACTION_BACK 回退退出设置页（代替用户完成确认/快速逃离），同时注册 WATCH_SETTINGS、WATCH_PKG_INSTALLER 与 PERFORM_GLOBAL_ACTION 监听设置页与安装器，阻止撤权；另有 DeviceAdmin（HookAPPAdmin）与 BOOT_COMPLETED 接收器维持常驻。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到应用发起 Intent(action=android.settings.ACCESSIBILITY_SETTINGS) 或 WindowManager.addView 新增全屏 WebView 时立即抓取 UTG；更稳妥的是 Hook AccessibilityManagerService/无障碍状态查询，在 d2.a.a() 首次返回 false 的同一时刻开始录屏+抓取 UI 树。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导文案为真实 DOM 文本（WebView HTML），UTG 可直接读取；但引导 HTML 正文由 m3.e 懒加载 Provider 运行期注入，纯静态无法还原排版，需运行期抓取。样本无加壳/VMP，静态加壳不构成运行期 UTG 障碍。另需注意获权后 risudunururi 会主动 GLOBAL_ACTION_BACK 退出设置页，UTG 采集应在此前完成，否则设置页会被自动关闭而丢失列表项证据。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动全屏伪造开关遮罩页** | 无 Activity 归属的全屏 WebView 悬浮层（type=2 overlay），根节点为 android.webkit.WebView，页面文本含“Chrome Update Service”与本地化“启用/Enable” | 这是“身份冒充+伪造系统设置页”的核心证据，可同时证明服务名被篡改、无关闭入口、覆盖在桌面/其他应用之上 | WebView 节点文本 "Chrome Update Service"；本地化开关文案（zh=启用/ru=Включить）；页面无取消/关闭/稍后按钮；覆盖层无标题栏且不属于任何 Activity 任务栈 |
| **系统无障碍服务列表项** | Settings$AccessibilitySettings 列表中的 item，title="HookAPPService"，summary="If accessibility permission has been on, please turn off then turn on." | 证明应用向系统提交的身份（HookAPPService）与悬浮层宣称的“Chrome Update Service”不一致，且描述为促操作话术而非功能说明 | 服务项文本 HookAPPService；描述文本先关闭再打开的诱导话术；服务项缺少“无障碍工具”应有的功能说明 |
| **设置页之后压栈的 WebView 教学页** | com.nadebumazoyi.dowaxuca.nakulafefo.vutapokutaso（WebView Activity，NEW_TASK，位于 Settings 之上） | 验证“边跳系统页边叠层教学”的第二步引导，运行期可取到静态不可见的 HTML 正文 | Settings 页面之上出现应用自有 WebView 窗口；页面含指向无障碍开关位置的图示/文字指引；页面无法通过返回键关闭（返回即重跳设置） |
| **拒权返回后的循环重跳观测** | 连续两次 Settings$AccessibilitySettings 进入记录 + 遮罩层重复出现 | 以时序证据证明死循环强制，而非一次性的引导 | 返回操作后 <2s 内重新出现 ACCESSIBILITY_SETTINGS 页面；遮罩 WebView 节点文本重复出现；始终不存在取消/跳过控件 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.nadebumazoyi.dowaxuca.dirate#s`
- `com.nadebumazoyi.dowaxuca.dirate#onResume`
- `com.nadebumazoyi.dowaxuca.dirate#onBackPressed`
- `k3.d#b`
- `com.nadebumazoyi.dowaxuca.nakulafefo.vutapokutaso#onCreate`
- `res/xml/pehibova.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论（Ermac 系 2024 样本，无障碍权限 UTG 全链路）

**1. 冷启动入口与伪装身份**
- 桌面入口为 `com.gejalevubakupa.sugi.duso`（label=`HookAPP`），`duso.onCreate` 直接转入 [dirate.onCreate](<resource-unit:#1.dex1 code:com.nadebumazoyi.dowaxuca.dirate#onCreate>)，把窗口设为 `type=2006`（系统级悬浮窗）+ 透明主题、`excludeFromRecents/noHistory`，自身不留任务栈痕迹。
- Manifest 内置 10 个 `activity-alias`（Facebook / Google Play / Gmail / Contacts / WhatsApp / Youtube / Chrome / Instagram / TikTok / Telegram，各自带官方图标，`enabled=false` 待远程开启），全部指向同一 `duso`，构成 ID 伪装与图标替换储备（[manifest:components](<resource-unit:#1 manifest:components>)）。

**2. 三步式引导：全屏 WebView 悬浮层 → 系统无障碍页 → 再叠一层 WebView 教学页**
- [dirate.onResume()](<resource-unit:#1.dex1 code:com.nadebumazoyi.dowaxuca.dirate#onResume>) 每次都调 `s()`。`s()` 先判 `d2.a.a(this)`（无障碍是否已开）；未开且 `z==true` 时：新建 WebView（`setJavaScriptEnabled`、`addJavascriptInterface(..., "Android")`），把 Base64 内嵌 HTML 中的 `%Enable_Accessibility_Service%` 替换为 **"Chrome Update Service"**，再把 `<html lang="en">` 与 `var lang='en'` 按系统语言重写，最后 `WindowManager.addView(webView, (-1,-1, type=2, flags=262144, -2))` 以**全屏悬浮层**盖在任何界面之上（[dirate#s](<resource-unit:#1.dex1 code:com.nadebumazoyi.dowaxuca.dirate#s>)）。
- 开关文案本地化词表 `k3.g.w` 覆盖 36 种语言（`zh:启用`、`en:Enable`、`ru:Включить`…），即伪造的“启用”按钮随语言变化。
- 点击后经 [k3.d.b()](<resource-unit:#1.dex1 code:k3.d#b>) 执行 `Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(0x14000000)`（NEW_TASK|CLEAR_TOP）跳到系统无障碍列表；紧接着再 `startActivity(vutapokutaso)`（另一个 WebView Activity，`NEW_TASK`，小米/SDK≥29 另加 `0x20000/0x800000`）——**跳设置的同时把引导页压栈到设置页之上**，形成“边跳系统页边指引”的叠层教学。

**3. 系统无障碍列表项的欺骗性**
- 服务名 `HookAPPService`；`android:description` = `If accessibility permission has been on, please turn off then turn on.`（[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L49>)），用“先关闭再打开”的话术促使用户反复进设置操作。
- 配置 [res/xml/pehibova.xml](<resource-unit:#1 file:res/xml/pehibova.xml>) 声明 `android:isAccessibilityTool="true"` + `canTakeScreenshot` + `flagRequestFilterKeyEvents` + `canPerformGestures` + `typeAllMask`：**伪造“无障碍工具”自证**以规避 Android 13+ 的受限设置拦截，同时取得截屏、按键过滤、手势点击能力。

**4. 拒权反馈循环**
- [dirate.onBackPressed()](<resource-unit:#1.dex1 code:com.nadebumazoyi.dowaxuca.dirate#onBackPressed>) 直接再调 `s()`；叠加 `onResume` 每次重入 `s()`，即从设置页返回（未开启）就再次弹全屏悬浮层/重跳设置，**无取消、无跳过、无降级路径**（`z` 仅在 `FromPush` 或 HTML 源为空时才被置 false，正常冷启动不成立）。

**5. 获权后动作（与撤权对抗）**
- 无障碍服务 `risudunururi` 在 `h()/i()` 中 `findAccessibilityNodeInfosByText("Chrome Update Service")` 定位设置页节点并 `GLOBAL_ACTION_BACK` 回退，配合 `PERFORM_GLOBAL_ACTION` / `WATCH_SETTINGS` / `WATCH_PKG_INSTALLER` 监听设置页与安装器，实现“自点确认 + 阻止撤权”；`decinakometuguzo#onStartCommand` 还拼接 `" Chrome Update Service"` 维持前台通知伪装。

**6. 静态可见性边界**
- 引导 HTML 的正文经 `m3.e` 懒加载 Provider 取用（`dirate$b/$c.o()` 在反编译视图中返回空串，实际内容依赖运行期注入），因此**代码路径、跳转点、替换关键字与多语种文案完全静态可见，HTML 正文具体排版需运行期采集**；样本无加壳/VMP，不存在跳转逻辑不可还原问题。

> 该结论与本项目已登记风险 [R-001]（Ermac 以“Chrome Update Service”全屏遮罩诱导开启无障碍）为同一命题，本轮未重复登记。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍服务配置、WebView 悬浮层构建、ACTION_ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS 跳转、vutapokutaso 教学页压栈、拒权回跳循环与 36 语种伪造开关文案均完整静态可见；仅引导 HTML 正文由 m3.e 懒加载 Provider 运行期提供（dirate$b/$c.o() 反编译返回空串），正文排版需运行期抓取。样本未加壳、无 VMP、无加密二阶段 DEX。",
  "summary_one_liner": "应用以 HookAPP 上架，冷启动即用 WindowManager 全屏 WebView 悬浮层把无障碍开关改称“Chrome Update Service”并按系统语言显示伪造“启用”按钮，点击后跳 ACTION_ACCESSIBILITY_SETTINGS 并同时压入第二层 WebView 教学页，配合 isAccessibilityTool=true 绕过 Android 13 受限设置、按返回键即重弹形成死循环。",
  "disguise_identity": {
    "app_display_name": "HookAPP",
    "claimed_brand_or_persona": "Chrome Update Service（伪装成 Chrome 浏览器更新服务/系统更新组件）",
    "a11y_service_label": "HookAPPService",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置伪造 android:isAccessibilityTool=\"true\" 冒充系统无障碍工具以规避 Android 13+ 受限设置；内置 Facebook/Google Play/Gmail/Contacts/WhatsApp/Youtube/Chrome/Instagram/TikTok/Telegram 共 10 个 activity-alias（enabled=false，带官方图标）指向同一 duso，可随时改头换面；主 Activity 为透明主题+excludeFromRecents+noHistory，界面以 type=2006 悬浮窗呈现不进入任务栈；应用整体类名/资源名随机化（com.nadebumazoyi.dowaxuca.*、pehibova.xml）；无障碍描述使用“先关闭再打开”话术而非功能说明。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.gejalevubakupa.sugi.duso（继承 com.nadebumazoyi.dowaxuca.dirate，透明主题 @style/ACL，excludeFromRecents+noHistory）",
      "trigger_event": "用户点击桌面图标 HookAPP（MAIN/LAUNCHER）→ onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见界面；窗口被设为 type=2006、flags=0x40000 的系统级悬浮窗，立即转入无障碍状态判定",
      "user_action_requested": "无（无感知进入）",
      "code_anchor": "com.nadebumazoyi.dowaxuca.dirate#onCreate"
    },
    {
      "step": 2,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WindowManager.addView 全屏 WebView 悬浮层（LayoutParams(-1,-1,type=2,flags=262144,-2)），含 JavascriptInterface \"Android\"",
      "trigger_event": "onResume → s()；判定 d2.a.a(context)==false（无障碍未开启）且 z==true",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Chrome Update Service / Enable（zh:启用, ru:Включить, fr:Activer, ar:يُمكّن …共36语种）",
      "shown_text_zh": "把无障碍开关的服务名替换为“Chrome 更新服务”，并提供本地化“启用”按钮，外观模拟系统设置页",
      "user_action_requested": "点击伪造的“启用”开关（页面无取消/关闭入口）",
      "code_anchor": "com.nadebumazoyi.dowaxuca.dirate#s + k3.g（w 多语种词表、d/e/f HTML 片段）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（列表项 HookAPPService）",
      "trigger_event": "悬浮层 JS 经 \"Android\" 接口回调 → k3.d.c() → k3.d.b()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "shown_text_zh": "“如果无障碍权限已开启，请先关闭再重新打开。”——以故障修复口吻促使反复操作，不说明任何功能用途",
      "user_action_requested": "在系统无障碍列表中找到 HookAPPService 并开启（服务名与“Chrome 更新服务”不一致，无解释）",
      "code_anchor": "k3.d#b + res/values/strings.xml#text_accessibility_service_description"
    },
    {
      "step": 4,
      "stage": "跳转后压栈教学页",
      "screen_or_component": "com.nadebumazoyi.dowaxuca.nakulafefo.vutapokutaso（WebView Activity，NEW_TASK，SDK≥29 或小米另加 0x20000/0x800000）",
      "trigger_event": "k3.d.b() 在 startActivity(ACCESSIBILITY_SETTINGS) 之后立刻 startActivity(vutapokutaso)",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "（正文由 m3.e 懒加载 Provider 运行期注入，静态视图为空串）",
      "shown_text_zh": "在系统设置页之上叠加应用自己的 WebView 指引页，边跳系统页边演示如何勾选开关",
      "user_action_requested": "按页面指引在设置页勾选服务开关",
      "code_anchor": "k3.d#b + com.nadebumazoyi.dowaxuca.nakulafefo.vutapokutaso#onCreate"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "dirate.onBackPressed → s()；onResume → s()",
      "trigger_event": "用户在设置页未开启即返回，或按物理返回键离开当前界面",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Chrome Update Service / Enable",
      "shown_text_zh": "返回后立即重新弹出“Chrome 更新服务”全屏悬浮层并再次跳转设置页，直到无障碍被开启",
      "user_action_requested": "无取消、无跳过、无“稍后再说”，只能开启或杀进程",
      "code_anchor": "com.nadebumazoyi.dowaxuca.dirate#onBackPressed + dirate#onResume"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.nadebumazoyi.dowaxuca.muduyicigumaga.risudunururi（AccessibilityService，isAccessibilityTool=true）+ com.nadebumazoyi.dowaxuca.nakulafefo.decinakometuguzo（前台通知）",
      "trigger_event": "无障碍服务连接后；监听设置页/安装器事件",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Chrome Update Service",
      "shown_text_zh": "在设置页按文本“Chrome Update Service”定位节点并执行 GLOBAL_ACTION_BACK 退出设置页（自点确认/防撤权），并持续监听设置页与安装器",
      "user_action_requested": "用户无需操作；应用自动回退设置页并阻断撤权路径",
      "code_anchor": "com.nadebumazoyi.dowaxuca.muduyicigumaga.risudunururi#h / #i + decinakometuguzo#onStartCommand"
    }
  ],
  "text_presentation_locations": [
    "冷启动后 WindowManager.addView 的全屏 WebView 悬浮层（dirate#s 内 loadDataWithBaseURL(null, html, \"text/html\", \"UTF-8\", null)，覆盖在桌面/任何前台应用之上）",
    "上述 HTML 中被字符串替换的占位符 %Enable_Accessibility_Service% → \"Chrome Update Service\"，开关按钮文案取自 k3.g.w 的 36 语种映射",
    "跳转 ACCESSIBILITY_SETTINGS 后立即压栈的 vutapokutaso WebView Activity（第二层教学/指引页）",
    "系统无障碍服务列表项：label=\"HookAPPService\"、android:description=\"If accessibility permission has been on, please turn off then turn on.\"",
    "应用内无任何原生 Dialog/layout 文案（应用主题为 Theme.Translucent.NoTitleBar，界面全部由 WebView 承载）",
    "获权后前台通知由 decinakometuguzo#onStartCommand 拼接 \" Chrome Update Service\" 维持伪装"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Chrome Update Service",
      "text_zh": "Chrome 更新服务",
      "source_location": "com.nadebumazoyi.dowaxuca.dirate#s 内 f4.i.T(..., \"%Enable_Accessibility_Service%\", \"Chrome Update Service\")",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable",
      "text_zh": "启用",
      "source_location": "k3.g.w（多语种映射 en:Enable）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "zh",
      "text_verbatim": "启用",
      "text_zh": "启用",
      "source_location": "k3.g.w（多语种映射 zh:启用）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": "Включить",
      "text_zh": "开启",
      "source_location": "k3.g.w（多语种映射 ru:Включить）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "If accessibility permission has been on, please turn off then turn on.",
      "text_zh": "如果无障碍权限已经开启，请先关闭再重新打开。",
      "source_location": "res/values/strings.xml key=text_accessibility_service_description（被 res/xml/pehibova.xml 的 android:description 引用）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "onResume 与 onBackPressed 均无条件调用 s()：用户从系统设置页返回或按返回键，立即重新以 WindowManager 添加全屏 WebView 悬浮层并再次 startActivity(ACCESSIBILITY_SETTINGS)，无任何退出分支，直至无障碍服务被开启；仅当 Intent 携带 FromPush=true 或 HTML 源为空时 z 才置 false 暂停遮罩。",
    "overlay_or_fake_settings": "是。以 LayoutParams(-1,-1,type=2,flags=262144,-2) 的全屏 WebView 悬浮层覆盖屏幕，HTML 内把服务名替换为“Chrome Update Service”、按钮文案按 36 种语言本地化，外观模拟系统无障碍开关页；跳转设置后再叠加 vutapokutaso WebView 教学页。",
    "restricted_settings_13plus_coaching": "无显式“应用详情→右上角菜单→允许受限设置”文字教学，但通过在 res/xml/pehibova.xml 中伪造 android:isAccessibilityTool=\"true\" 与 accessibilityDataSensitive=\"no\"，使该服务被系统当作无障碍工具，直接绕过 Android 13+ 对非无障碍工具服务的受限设置拦截。",
    "post_grant_anti_removal": "是。无障碍服务 risudunururi 的 h()/i() 用 findAccessibilityNodeInfosByText(\"Chrome Update Service\") 定位设置页节点，并以 GLOBAL_ACTION_BACK 回退退出设置页（代替用户完成确认/快速逃离），同时注册 WATCH_SETTINGS、WATCH_PKG_INSTALLER 与 PERFORM_GLOBAL_ACTION 监听设置页与安装器，阻止撤权；另有 DeviceAdmin（HookAPPAdmin）与 BOOT_COMPLETED 接收器维持常驻。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到应用发起 Intent(action=android.settings.ACCESSIBILITY_SETTINGS) 或 WindowManager.addView 新增全屏 WebView 时立即抓取 UTG；更稳妥的是 Hook AccessibilityManagerService/无障碍状态查询，在 d2.a.a() 首次返回 false 的同一时刻开始录屏+抓取 UI 树。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动全屏伪造开关遮罩页",
        "page_identifier": "无 Activity 归属的全屏 WebView 悬浮层（type=2 overlay），根节点为 android.webkit.WebView，页面文本含“Chrome Update Service”与本地化“启用/Enable”",
        "why_most_useful": "这是“身份冒充+伪造系统设置页”的核心证据，可同时证明服务名被篡改、无关闭入口、覆盖在桌面/其他应用之上",
        "observable_utg_signals": [
          "WebView 节点文本 \"Chrome Update Service\"",
          "本地化开关文案（zh=启用/ru=Включить）",
          "页面无取消/关闭/稍后按钮",
          "覆盖层无标题栏且不属于任何 Activity 任务栈"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings$AccessibilitySettings 列表中的 item，title=\"HookAPPService\"，summary=\"If accessibility permission has been on, please turn off then turn on.\"",
        "why_most_useful": "证明应用向系统提交的身份（HookAPPService）与悬浮层宣称的“Chrome Update Service”不一致，且描述为促操作话术而非功能说明",
        "observable_utg_signals": [
          "服务项文本 HookAPPService",
          "描述文本先关闭再打开的诱导话术",
          "服务项缺少“无障碍工具”应有的功能说明"
        ]
      },
      {
        "page_role": "设置页之后压栈的 WebView 教学页",
        "page_identifier": "com.nadebumazoyi.dowaxuca.nakulafefo.vutapokutaso（WebView Activity，NEW_TASK，位于 Settings 之上）",
        "why_most_useful": "验证“边跳系统页边叠层教学”的第二步引导，运行期可取到静态不可见的 HTML 正文",
        "observable_utg_signals": [
          "Settings 页面之上出现应用自有 WebView 窗口",
          "页面含指向无障碍开关位置的图示/文字指引",
          "页面无法通过返回键关闭（返回即重跳设置）"
        ]
      },
      {
        "page_role": "拒权返回后的循环重跳观测",
        "page_identifier": "连续两次 Settings$AccessibilitySettings 进入记录 + 遮罩层重复出现",
        "why_most_useful": "以时序证据证明死循环强制，而非一次性的引导",
        "observable_utg_signals": [
          "返回操作后 <2s 内重新出现 ACCESSIBILITY_SETTINGS 页面",
          "遮罩 WebView 节点文本重复出现",
          "始终不存在取消/跳过控件"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导文案为真实 DOM 文本（WebView HTML），UTG 可直接读取；但引导 HTML 正文由 m3.e 懒加载 Provider 运行期注入，纯静态无法还原排版，需运行期抓取。样本无加壳/VMP，静态加壳不构成运行期 UTG 障碍。另需注意获权后 risudunururi 会主动 GLOBAL_ACTION_BACK 退出设置页，UTG 采集应在此前完成，否则设置页会被自动关闭而丢失列表项证据。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL"
  ],
  "code_anchors": [
    "com.nadebumazoyi.dowaxuca.dirate#s",
    "com.nadebumazoyi.dowaxuca.dirate#onResume",
    "com.nadebumazoyi.dowaxuca.dirate#onBackPressed",
    "k3.d#b",
    "com.nadebumazoyi.dowaxuca.nakulafefo.vutapokutaso#onCreate",
    "res/xml/pehibova.xml"
  ]
}
```

</details>
