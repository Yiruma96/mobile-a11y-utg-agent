# MB_025__3eb7efa716｜MaliBot — Amazon App

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：176.9s

## 1. 一句话核心结论

- **核心申请方式**：以「Amazon App」为名、沿用卡车停车游戏 Application 类名的套壳应用，运行期解密 819KB 载荷接管全部业务，并用透明 AccessibilityRequestActivity 与「Update settings / Enable accessibility access」分步文案，诱导用户把全量读取与手势模拟权限授予伪装成「无障碍问题扫描」的服务。
- **静态可见性说明**：Manifest、无障碍配置、引导文案与载荷容器均静态可见；但真实业务类（com.slhytrowb.wfxaicaiw.cryptor.*，含 AccessibilityRequestActivity、BrowserActivity、AccessibilityService 实现）在 classes.dex 中完全不存在（检索 slhytrowb 得 0 类），由 XOR 字符串混淆的 Application 存根 com.car.parking.master.puzzle.truck.games.k#a 将 applicationInfo.className 改写为 cryptor.core.App 后，从包内高熵资产 assets/8uggjfH/UHoy9Ikfa1.ykp（819KB，随机名、无 lib/）解密加载；故跳转逻辑、弹窗/遮罩、拒绝循环等运行期页面流转全部藏于该加密载荷，静态不可还原。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3eb7efa71648ae819f1bff89399717805129487081e8261dd65bf596f2467054` |
| 包名 / 年份 | `com.slhytrowb.wfxaicaiw` / 2022 |
| 家族 / 品类 | **MaliBot**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Amazon App |
| 引导页宣称品牌/身份 | Amazon（亚马逊）官方应用；无障碍服务自述为「Android 无障碍问题扫描服务」 |
| 系统无障碍列表服务名 | Amazon App（@string/app_name，系统无障碍列表显示） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.slhytrowb.wfxaicaiw 与品牌无关；Application 类名沿用无关的卡车停车小游戏 com.car.parking.master.puzzle.truck.games.k 作为壳存根；残留 Launcher3 全套资源并将 PixelLauncher 声明为 HOME 桌面；混入 WeTV/Tencent 视频 Logo 与 assets/tcaptcha_webview.html 腾讯验证码页面（多模板复用）；服务描述以「扫描无障碍问题」淡化实际的全量窗口读取与手势模拟能力；关键字符串以 XOR 逐字节编码并在运行时按索引解码。 |
| 无障碍服务类名 | `com.slhytrowb.wfxaicaiw.cryptor.services.AccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Service allows Accessibility for Android to scan your device for accessibility issues. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.slhytrowb.wfxaicaiw.cryptor.ui.activities.StartActivity（LAUNCHER，@style/AppTheme1.Transparent） | 用户点击桌面图标（MAIN/LAUNCHER intent-filter），进程启动时先执行 Application 存根 attachBaseContext/onCreate | 原生Activity（透明主题） | **原文**：无（StartActivity 类体位于加密载荷内，静态不可见）<br>**译注**：无可见静态文案；该 Activity 为透明主题启动壳，实际界面由解密后的载荷决定 | 点击图标启动；后续请求不可静态确认 | `#1 manifest:components（StartActivity）；com.car.parking.master.puzzle.truck.games.k#onCreate` |
| 2 | 冷启动入口（载荷接管） | Application 存根 com.car.parking.master.puzzle.truck.games.k → 被替换为 com.slhytrowb.wfxaicaiw.cryptor.core.App | Application.onCreate 中通过反射（c.a/c.b）调用，并强制改写 LoadedApk 内两处 ApplicationInfo.className | 不可静态还原 | **原文**：applicationInfo.className = "com.slhytrowb.wfxaicaiw.cryptor.core.App";<br>**译注**：运行时把真实 Application 类名替换为 cryptor.core.App，由其从加密载荷中装载真实业务代码 | 无（用户不可见） | `com.car.parking.master.puzzle.truck.games.k#a；assets/8uggjfH/UHoy9Ikfa1.ykp` |
| 3 | 引导说明页 | com.slhytrowb.wfxaicaiw.cryptor.ui.activities.AccessibilityRequestActivity（exported=false、noHistory、portrait、@style/AppTheme1.Transparent） | 由载荷内业务代码启动（具体触发点在加密载荷内，静态不可确认是否为冷启动即弹） | 原生Activity（透明主题，可叠悬浮/遮罩；SYSTEM_ALERT_WINDOW 已申请） | **原文**：Update %1$s settings / Enable accessibility access<br>**译注**：「更新 %1$s 的设置」/「启用无障碍访问」——以系统设置更新的名义请求开启无障碍 | 按提示前往系统设置开启；是否存在取消/跳过按钮不可静态确认 | `res/values/strings.xml（enable_accessibility_title、enable_accessibility_message）；#1 manifest:components（AccessibilityRequestActivity）` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装的服务（Settings.ACTION_ACCESSIBILITY_SETTINGS） | AccessibilityRequestActivity 内的 Intent 跳转（实现位于加密载荷，静态不可见；classes.dex 中无 ACTION_ACCESSIBILITY_SETTINGS 明文） | 系统无障碍页 | **原文**：Service allows Accessibility for Android to scan your device for accessibility issues.<br>**译注**：「该服务允许 Android 无障碍功能扫描您设备上的无障碍问题。」——在系统服务列表中显示的说明，弱化实际的全量读取与手势能力 | 在列表中点击「Amazon App」并打开开关；无取消引导说明 | `res/xml/accessibilityservice.xml（android:description=@string/accessibility_service_description）；res/values/strings.xml` |
| 5 | 遮罩叠层指引 | 系统无障碍设置页上叠加的悬浮引导层（推断，承载代码在加密载荷内） | 跳转后由 AccessibilityRequestActivity/悬浮窗在设置页之上绘制（不可静态确认时序） | 悬浮窗Overlay（SYSTEM_ALERT_WINDOW 已声明；AccessibilityRequestActivity 使用透明主题） | **原文**：Enable accessibility to %1$s. Settings-> Accessibility-> Installed services-> %1$s-> ON<br>**译注**：「请为 %1$s 启用无障碍：设置 → 无障碍 → 已安装的服务 → %1$s → 打开」——分步教学式指引 | 严格按步骤点击开关，不得离开设置页 | `res/values/strings.xml（enable_to_asb、enable_to_asb_short）` |
| 6 | 拒权反馈循环 | AccessibilityRequestActivity（noHistory，返回即销毁并重拉）/ 无障碍设置页 | 用户返回或未开启开关时由 onResume/定时器重新拉起（实现位于加密载荷，静态不可确认） | 不可静态还原 | **原文**：无（classes.dex 中无对应明文文案）<br>**译注**：无法静态确认是否强制循环重跳或提供安全降级 | 不可静态确认 | `#1 manifest:components（AccessibilityRequestActivity noHistory=true）` |
| 7 | 获权后动作 | com.slhytrowb.wfxaicaiw.cryptor.services.AccessibilityService（typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRequestTouchExplorationMode） | 系统绑定无障碍服务后由载荷内 onAccessibilityEvent/onServiceConnected 处理（类体位于加密载荷） | 不可静态还原（能力侧已确证：可读取全窗口内容 + 模拟手势） | 无 | 无（后台自动执行） | `res/xml/accessibilityservice.xml；#1 manifest:components（AccessibilityService、BrowserActivity、CaptureActivity、NotificationService、SMSReceiver）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统设置→无障碍→已安装服务列表项描述：res/values/strings.xml 的 accessibility_service_description（经 res/xml/accessibilityservice.xml 的 android:description 引用），服务名取自 @string/app_name（Amazon App）
- 专用请求页 AccessibilityRequestActivity（透明主题、noHistory、竖屏、exported=false）：引导文案 enable_accessibility_title=「Update %1$s settings」、enable_accessibility_message=「Enable accessibility access」
- 分步教学文案 enable_to_asb / enable_to_asb_short：「Enable accessibility to %1$s. Settings-> Accessibility-> Installed services-> %1$s-> ON」，预期以设置页上方悬浮层或遮罩形式呈现（时序不可静态确认）
- WebView 载体 BrowserActivity / BrowserAppActivity（Theme.Light.NoTitleBar.Fullscreen、noHistory、excludeFromRecents）可用于加载远端钓鱼/引导 HTML；包内仅见 assets/tcaptcha_webview.html（腾讯验证码）
- 桌面层：PixelLauncher 被声明为 HOME 桌面（Launcher3 资源整体残留），可承载伪装图标与「App isn't installed / This app is not installed / %1$s waiting to install」类提示文案
- 所有弹窗、遮罩、点击引导的实际绘制代码位于加密载荷 assets/8uggjfH/UHoy9Ikfa1.ykp，静态不可见

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Service allows Accessibility for Android to scan your device for accessibility issues. | 该服务允许 Android 无障碍功能扫描您设备上的无障碍问题。 | `res/values/strings.xml → accessibility_service_description（被 res/xml/accessibilityservice.xml 引用）` | 假反诈安全 |
| en | Update %1$s settings | 更新 %1$s 的设置 | `res/values/strings.xml → enable_accessibility_title` | 假更新 |
| en | Enable accessibility access | 启用无障碍访问 | `res/values/strings.xml → enable_accessibility_message` | 受限设置分步教学 |
| en | Enable accessibility to %1$s. Settings-> Accessibility-> Installed services-> %1$s-> ON | 请为 %1$s 启用无障碍：设置 → 无障碍 → 已安装的服务 → %1$s → 打开。 | `res/values/strings.xml → enable_to_asb` | 受限设置分步教学 |
| en | Enable accessibility to %1$s. Installed services-> %1$s-> ON | 请为 %1$s 启用无障碍：已安装的服务 → %1$s → 打开。 | `res/values/strings.xml → enable_to_asb_short` | 受限设置分步教学 |
| en | applicationInfo.className = "com.slhytrowb.wfxaicaiw.cryptor.core.App"; | 运行时将 Application 类名替换为 com.slhytrowb.wfxaicaiw.cryptor.core.App（解密载荷入口） | `classes.dex → com.car.parking.master.puzzle.truck.games.k#a（XOR 解码字符串）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态确认。AccessibilityRequestActivity 声明 noHistory=true 且使用透明主题，返回即销毁、可被载荷内逻辑反复重建，符合「返回设置页即重跳」的常见构造；但 onResume 重跳、定时器拉起等具体实现位于加密载荷 assets/8uggjfH/UHoy9Ikfa1.ykp，未取得静态证据，故不作已证实结论。
- **遮罩叠层 / 高仿系统设置页**：已确证具备叠层条件：申请 SYSTEM_ALERT_WINDOW，且 AccessibilityRequestActivity 使用 @style/AppTheme1.Transparent 透明主题，无障碍服务开启 canPerformGestures 与 flagRequestTouchExplorationMode；但未见高仿系统无障碍开关页的静态资源，实际遮罩/伪造设置页的绘制代码在加密载荷内，未能静态确认。
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据。targetSdkVersion=28，包内未发现应用详情页/受限设置（Allow restricted settings）或 Session 安装器绕过的明文引导文案与代码。
- **获权后即时行为与防撤权机制**：不可静态确认。已确证具备实现条件（全量窗口读取 + 模拟手势可自点确认，或监听设置页执行 GLOBAL_ACTION_BACK/HOME），但相关代码位于加密载荷，未取得静态证据。
- **良性降级 / 替代方案**：无。未见任何取消、跳过、仅观看模式或手动替代路径的明文文案；相反文案为单向强制式教学（Settings-> Accessibility-> Installed services-> %1$s-> ON）。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到启动 com.slhytrowb.wfxaicaiw.cryptor.ui.activities.AccessibilityRequestActivity（透明主题、noHistory、竖屏）即拉起 UTG；并在检测到跳转 Settings.ACTION_ACCESSIBILITY_SETTINGS 后 500–1500ms 内再次抓取，以捕获叠加在系统设置页之上的引导遮罩。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：真实业务类全部缺失于 classes.dex（检索 com.slhytrowb 得 0 类），由 Application 存根 com.car.parking.master.puzzle.truck.games.k#a 以 XOR 解码字符串 + 反射将 applicationInfo.className 改写为 cryptor.core.App，再从 assets/8uggjfH/UHoy9Ikfa1.ykp（819KB、随机名、无 lib/）解密加载，因此跳转 Intent、弹窗/遮罩、拒绝循环、获权后动作均无法静态确认；纯静态 UTG 只能拿到 Manifest/无障碍配置/strings 骨架。注意：静态加密本身不阻挡运行期 UTG——页面一旦真正渲染，UTG 仍可捕获文本与层级，故应以运行期抓取补齐此盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/请求页：无障碍请求专用透明 Activity** | com.slhytrowb.wfxaicaiw.cryptor.ui.activities.AccessibilityRequestActivity；透明主题、无标题、竖屏、无历史栈 | 这是应用自建的、专为拉起无障碍设置而存在的页面，捕获即可直接证明「应用主动索取无障碍」而非系统行为 | Activity 类名含 AccessibilityRequest；界面文本含 Enable accessibility access / Update ... settings；是否存在取消/关闭按钮；页面是否透明且下层可见 |
| **跳转后压栈遮罩页：系统无障碍设置之上的悬浮引导层** | 系统设置无障碍页（Settings$AccessibilitySettings 或 InstalledServices 列表）之上叠加的 View/悬浮窗节点 | 区分「正常跳设置」与「叠遮罩强迫操作」的关键证据，也是判断是否有分步教学（enable_to_asb）的直接依据 | 设置页上方出现非系统节点/悬浮窗；文本含 Settings-> Accessibility-> Installed services-> ...-> ON；遮罩是否遮挡返回按钮/其他服务项 |
| **系统无障碍服务列表项（受害者视角）** | Settings 无障碍已安装服务列表中的「Amazon App」条目 | 核对服务名与描述是否与真实品牌一致，验证身份冒用与能力弱化描述 | 条目名称 Amazon App；描述文本 Service allows Accessibility for Android to scan your device for accessibility issues.；开启后是否被自动勾选 |
| **获权后 WebView 钓鱼/引导页** | com.slhytrowb.wfxaicaiw.cryptor.ui.activities.BrowserActivity / BrowserAppActivity（全屏、无标题、无历史、不进入最近任务） | 确认获权后的真实业务目的（钓鱼页面/凭证窃取），区别于「无障碍工具」的自我描述 | WebView 加载的 URL/域名；页面标题与品牌标识；输入框类型（账号/卡号/密码/验证码） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.car.parking.master.puzzle.truck.games.k#a`
- `res/xml/accessibilityservice.xml`
- `res/values/strings.xml#enable_to_asb`
- `res/values/strings.xml#accessibility_service_description`
- `assets/8uggjfH/UHoy9Ikfa1.ykp`
- `AndroidManifest.xml → com.slhytrowb.wfxaicaiw.cryptor.ui.activities.AccessibilityRequestActivity`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（工具调用已达上限，立即收敛）

**结论：应用自身代码在运行时被整体加密载荷取代，无障碍诱导页面的流程无法静态还原，但“伪装身份 + 全权限无障碍服务 + 专用请求页”的骨架已确证。**

已确认事实：

1. **宿主壳**：Manifest 的 `android:name` 指向 [com.car.parking.master.puzzle.truck.games.k](<resource-unit:#1.dex1 code:com.car.parking.master.puzzle.truck.games.k#a>)，它只做一件事——解码 XOR 字符串并**强行把 `applicationInfo.className` 改写为 `com.slhytrowb.wfxaicaiw.cryptor.core.App`**（两处 ApplicationInfo 均被改写），即真正的 Application 不是它。
2. **真实业务类不在 DEX 中**：`list_codebase` 检索 `slhytrowb` 得到 **0 个类**；`classes.dex` 全文也搜不到 `AccessibilityRequest`、`enable_accessibility`、`ACTION_ACCESSIBILITY_SETTINGS` 等明文。而 Manifest 声明的 `cryptor.ui.activities.*`、`cryptor.services.*` 全部缺失 → 这些类来自包内唯一的高熵载荷 [assets/8uggjfH/UHoy9Ikfa1.ykp](<resource-unit:#1 file:assets/8uggjfH/UHoy9Ikfa1.ykp>)（819,120 字节、随机目录/文件名、`lib/` 目录为空、`extractNativeLibs=false`），运行期解密后加载。
3. **无障碍能力已确证为“全量控制级”**：[res/xml/accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml>) 配置 `typeAllMask`、`canRetrieveWindowContent=true`、`canPerformGestures=true`、`flagRequestTouchExplorationMode`，可读取全部界面内容并模拟手势点击。
4. **身份三重错位**：包名 `com.slhytrowb.wfxaicaiw`、桌面名 `Amazon App`、Application 类名却沿用“卡车停车小游戏”（`com.car.parking.master.puzzle.truck.games`）；同时残留 Launcher3 全套资源（`PixelLauncher` 声明为 HOME、`LauncherProvider`），并混入 WeTV/Tencent 视频 Logo 与 `assets/tcaptcha_webview.html`（腾讯验证码），属于多模板钓鱼套件。
5. **专用诱导页已存在**：Manifest 声明 `cryptor.ui.activities.AccessibilityRequestActivity`（`exported=false`、`noHistory`、`portrait`、`@style/AppTheme1.Transparent` 透明主题）——这是专为“拉起系统无障碍设置”设计的页面，透明主题通常配合悬浮指引/遮罩；另有 `BrowserActivity`/`BrowserAppActivity`（WebView 钓鱼载体）、`CaptureActivity`（截屏）、`NotificationService`（通知监听）、`SMSReceiver`（短信拦截）、`BootReceiver`（开机自启）。
6. **引导文案已确证存在**：[res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml>) 中 `enable_accessibility_title` = `Update %1$s settings`、`enable_accessibility_message` = `Enable accessibility access`、`enable_to_asb` = `Enable accessibility to %1$s. Settings-> Accessibility-> Installed services-> %1$s-> ON`，以及系统列表描述 `Service allows Accessibility for Android to scan your device for accessibility issues.`（伪装成“无障碍问题扫描”工具）。
7. **未决边界**：`AccessibilityRequestActivity` 的 `onCreate/onResume` 是否 `startActivity(ACTION_ACCESSIBILITY_SETTINGS)`、是否 `onResume` 死循环重跳、是否叠悬浮遮罩、是否监听设置页 `GLOBAL_ACTION_BACK` 阻止撤权，全部位于 `.ykp` 解密载荷内，静态不可见；亦未见任何取消/跳过/降级路径的明文证据。故 `static_visibility = packed_or_encrypted`，步骤流转只能给出“声明骨架级”推断，不做已证实断言。

**UTG 检测建议**：不必等静态还原——在**冷启动拉起透明 `AccessibilityRequestActivity`** 与**跳转 `ACCESSIBILITY_SETTINGS` 后 500–1500ms 内的压栈窗口**两个瞬间抓取即可命中诱导主链路。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍配置、引导文案与载荷容器均静态可见；但真实业务类（com.slhytrowb.wfxaicaiw.cryptor.*，含 AccessibilityRequestActivity、BrowserActivity、AccessibilityService 实现）在 classes.dex 中完全不存在（检索 slhytrowb 得 0 类），由 XOR 字符串混淆的 Application 存根 com.car.parking.master.puzzle.truck.games.k#a 将 applicationInfo.className 改写为 cryptor.core.App 后，从包内高熵资产 assets/8uggjfH/UHoy9Ikfa1.ykp（819KB，随机名、无 lib/）解密加载；故跳转逻辑、弹窗/遮罩、拒绝循环等运行期页面流转全部藏于该加密载荷，静态不可还原。",
  "summary_one_liner": "以「Amazon App」为名、沿用卡车停车游戏 Application 类名的套壳应用，运行期解密 819KB 载荷接管全部业务，并用透明 AccessibilityRequestActivity 与「Update settings / Enable accessibility access」分步文案，诱导用户把全量读取与手势模拟权限授予伪装成「无障碍问题扫描」的服务。",
  "disguise_identity": {
    "app_display_name": "Amazon App",
    "claimed_brand_or_persona": "Amazon（亚马逊）官方应用；无障碍服务自述为「Android 无障碍问题扫描服务」",
    "a11y_service_label": "Amazon App（@string/app_name，系统无障碍列表显示）",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.slhytrowb.wfxaicaiw 与品牌无关；Application 类名沿用无关的卡车停车小游戏 com.car.parking.master.puzzle.truck.games.k 作为壳存根；残留 Launcher3 全套资源并将 PixelLauncher 声明为 HOME 桌面；混入 WeTV/Tencent 视频 Logo 与 assets/tcaptcha_webview.html 腾讯验证码页面（多模板复用）；服务描述以「扫描无障碍问题」淡化实际的全量窗口读取与手势模拟能力；关键字符串以 XOR 逐字节编码并在运行时按索引解码。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.slhytrowb.wfxaicaiw.cryptor.ui.activities.StartActivity（LAUNCHER，@style/AppTheme1.Transparent）",
      "trigger_event": "用户点击桌面图标（MAIN/LAUNCHER intent-filter），进程启动时先执行 Application 存根 attachBaseContext/onCreate",
      "ui_carrier": "原生Activity（透明主题）",
      "shown_text_verbatim": "无（StartActivity 类体位于加密载荷内，静态不可见）",
      "shown_text_zh": "无可见静态文案；该 Activity 为透明主题启动壳，实际界面由解密后的载荷决定",
      "user_action_requested": "点击图标启动；后续请求不可静态确认",
      "code_anchor": "#1 manifest:components（StartActivity）；com.car.parking.master.puzzle.truck.games.k#onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口（载荷接管）",
      "screen_or_component": "Application 存根 com.car.parking.master.puzzle.truck.games.k → 被替换为 com.slhytrowb.wfxaicaiw.cryptor.core.App",
      "trigger_event": "Application.onCreate 中通过反射（c.a/c.b）调用，并强制改写 LoadedApk 内两处 ApplicationInfo.className",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "applicationInfo.className = \"com.slhytrowb.wfxaicaiw.cryptor.core.App\";",
      "shown_text_zh": "运行时把真实 Application 类名替换为 cryptor.core.App，由其从加密载荷中装载真实业务代码",
      "user_action_requested": "无（用户不可见）",
      "code_anchor": "com.car.parking.master.puzzle.truck.games.k#a；assets/8uggjfH/UHoy9Ikfa1.ykp"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.slhytrowb.wfxaicaiw.cryptor.ui.activities.AccessibilityRequestActivity（exported=false、noHistory、portrait、@style/AppTheme1.Transparent）",
      "trigger_event": "由载荷内业务代码启动（具体触发点在加密载荷内，静态不可确认是否为冷启动即弹）",
      "ui_carrier": "原生Activity（透明主题，可叠悬浮/遮罩；SYSTEM_ALERT_WINDOW 已申请）",
      "shown_text_verbatim": "Update %1$s settings / Enable accessibility access",
      "shown_text_zh": "「更新 %1$s 的设置」/「启用无障碍访问」——以系统设置更新的名义请求开启无障碍",
      "user_action_requested": "按提示前往系统设置开启；是否存在取消/跳过按钮不可静态确认",
      "code_anchor": "res/values/strings.xml（enable_accessibility_title、enable_accessibility_message）；#1 manifest:components（AccessibilityRequestActivity）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装的服务（Settings.ACTION_ACCESSIBILITY_SETTINGS）",
      "trigger_event": "AccessibilityRequestActivity 内的 Intent 跳转（实现位于加密载荷，静态不可见；classes.dex 中无 ACTION_ACCESSIBILITY_SETTINGS 明文）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "shown_text_zh": "「该服务允许 Android 无障碍功能扫描您设备上的无障碍问题。」——在系统服务列表中显示的说明，弱化实际的全量读取与手势能力",
      "user_action_requested": "在列表中点击「Amazon App」并打开开关；无取消引导说明",
      "code_anchor": "res/xml/accessibilityservice.xml（android:description=@string/accessibility_service_description）；res/values/strings.xml"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍设置页上叠加的悬浮引导层（推断，承载代码在加密载荷内）",
      "trigger_event": "跳转后由 AccessibilityRequestActivity/悬浮窗在设置页之上绘制（不可静态确认时序）",
      "ui_carrier": "悬浮窗Overlay（SYSTEM_ALERT_WINDOW 已声明；AccessibilityRequestActivity 使用透明主题）",
      "shown_text_verbatim": "Enable accessibility to %1$s. Settings-> Accessibility-> Installed services-> %1$s-> ON",
      "shown_text_zh": "「请为 %1$s 启用无障碍：设置 → 无障碍 → 已安装的服务 → %1$s → 打开」——分步教学式指引",
      "user_action_requested": "严格按步骤点击开关，不得离开设置页",
      "code_anchor": "res/values/strings.xml（enable_to_asb、enable_to_asb_short）"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "AccessibilityRequestActivity（noHistory，返回即销毁并重拉）/ 无障碍设置页",
      "trigger_event": "用户返回或未开启开关时由 onResume/定时器重新拉起（实现位于加密载荷，静态不可确认）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（classes.dex 中无对应明文文案）",
      "shown_text_zh": "无法静态确认是否强制循环重跳或提供安全降级",
      "user_action_requested": "不可静态确认",
      "code_anchor": "#1 manifest:components（AccessibilityRequestActivity noHistory=true）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.slhytrowb.wfxaicaiw.cryptor.services.AccessibilityService（typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRequestTouchExplorationMode）",
      "trigger_event": "系统绑定无障碍服务后由载荷内 onAccessibilityEvent/onServiceConnected 处理（类体位于加密载荷）",
      "ui_carrier": "不可静态还原（能力侧已确证：可读取全窗口内容 + 模拟手势）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后可读取任意界面文本并模拟点击/手势，配合 BrowserActivity、BrowserAppActivity（WebView）、CaptureActivity（截屏）、NotificationService（通知监听）、SMSReceiver（短信拦截）构成钓鱼与凭证窃取链路；具体动作不可静态还原",
      "user_action_requested": "无（后台自动执行）",
      "code_anchor": "res/xml/accessibilityservice.xml；#1 manifest:components（AccessibilityService、BrowserActivity、CaptureActivity、NotificationService、SMSReceiver）"
    }
  ],
  "text_presentation_locations": [
    "系统设置→无障碍→已安装服务列表项描述：res/values/strings.xml 的 accessibility_service_description（经 res/xml/accessibilityservice.xml 的 android:description 引用），服务名取自 @string/app_name（Amazon App）",
    "专用请求页 AccessibilityRequestActivity（透明主题、noHistory、竖屏、exported=false）：引导文案 enable_accessibility_title=「Update %1$s settings」、enable_accessibility_message=「Enable accessibility access」",
    "分步教学文案 enable_to_asb / enable_to_asb_short：「Enable accessibility to %1$s. Settings-> Accessibility-> Installed services-> %1$s-> ON」，预期以设置页上方悬浮层或遮罩形式呈现（时序不可静态确认）",
    "WebView 载体 BrowserActivity / BrowserAppActivity（Theme.Light.NoTitleBar.Fullscreen、noHistory、excludeFromRecents）可用于加载远端钓鱼/引导 HTML；包内仅见 assets/tcaptcha_webview.html（腾讯验证码）",
    "桌面层：PixelLauncher 被声明为 HOME 桌面（Launcher3 资源整体残留），可承载伪装图标与「App isn't installed / This app is not installed / %1$s waiting to install」类提示文案",
    "所有弹窗、遮罩、点击引导的实际绘制代码位于加密载荷 assets/8uggjfH/UHoy9Ikfa1.ykp，静态不可见"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Service allows Accessibility for Android to scan your device for accessibility issues.",
      "text_zh": "该服务允许 Android 无障碍功能扫描您设备上的无障碍问题。",
      "source_location": "res/values/strings.xml → accessibility_service_description（被 res/xml/accessibilityservice.xml 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Update %1$s settings",
      "text_zh": "更新 %1$s 的设置",
      "source_location": "res/values/strings.xml → enable_accessibility_title",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable accessibility access",
      "text_zh": "启用无障碍访问",
      "source_location": "res/values/strings.xml → enable_accessibility_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable accessibility to %1$s. Settings-> Accessibility-> Installed services-> %1$s-> ON",
      "text_zh": "请为 %1$s 启用无障碍：设置 → 无障碍 → 已安装的服务 → %1$s → 打开。",
      "source_location": "res/values/strings.xml → enable_to_asb",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable accessibility to %1$s. Installed services-> %1$s-> ON",
      "text_zh": "请为 %1$s 启用无障碍：已安装的服务 → %1$s → 打开。",
      "source_location": "res/values/strings.xml → enable_to_asb_short",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "applicationInfo.className = \"com.slhytrowb.wfxaicaiw.cryptor.core.App\";",
      "text_zh": "运行时将 Application 类名替换为 com.slhytrowb.wfxaicaiw.cryptor.core.App（解密载荷入口）",
      "source_location": "classes.dex → com.car.parking.master.puzzle.truck.games.k#a（XOR 解码字符串）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态确认。AccessibilityRequestActivity 声明 noHistory=true 且使用透明主题，返回即销毁、可被载荷内逻辑反复重建，符合「返回设置页即重跳」的常见构造；但 onResume 重跳、定时器拉起等具体实现位于加密载荷 assets/8uggjfH/UHoy9Ikfa1.ykp，未取得静态证据，故不作已证实结论。",
    "overlay_or_fake_settings": "已确证具备叠层条件：申请 SYSTEM_ALERT_WINDOW，且 AccessibilityRequestActivity 使用 @style/AppTheme1.Transparent 透明主题，无障碍服务开启 canPerformGestures 与 flagRequestTouchExplorationMode；但未见高仿系统无障碍开关页的静态资源，实际遮罩/伪造设置页的绘制代码在加密载荷内，未能静态确认。",
    "restricted_settings_13plus_coaching": "无静态证据。targetSdkVersion=28，包内未发现应用详情页/受限设置（Allow restricted settings）或 Session 安装器绕过的明文引导文案与代码。",
    "post_grant_anti_removal": "不可静态确认。已确证具备实现条件（全量窗口读取 + 模拟手势可自点确认，或监听设置页执行 GLOBAL_ACTION_BACK/HOME），但相关代码位于加密载荷，未取得静态证据。",
    "benign_graceful_degradation": "无。未见任何取消、跳过、仅观看模式或手动替代路径的明文文案；相反文案为单向强制式教学（Settings-> Accessibility-> Installed services-> %1$s-> ON）。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到启动 com.slhytrowb.wfxaicaiw.cryptor.ui.activities.AccessibilityRequestActivity（透明主题、noHistory、竖屏）即拉起 UTG；并在检测到跳转 Settings.ACTION_ACCESSIBILITY_SETTINGS 后 500–1500ms 内再次抓取，以捕获叠加在系统设置页之上的引导遮罩。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/请求页：无障碍请求专用透明 Activity",
        "page_identifier": "com.slhytrowb.wfxaicaiw.cryptor.ui.activities.AccessibilityRequestActivity；透明主题、无标题、竖屏、无历史栈",
        "why_most_useful": "这是应用自建的、专为拉起无障碍设置而存在的页面，捕获即可直接证明「应用主动索取无障碍」而非系统行为",
        "observable_utg_signals": ["Activity 类名含 AccessibilityRequest", "界面文本含 Enable accessibility access / Update ... settings", "是否存在取消/关闭按钮", "页面是否透明且下层可见"]
      },
      {
        "page_role": "跳转后压栈遮罩页：系统无障碍设置之上的悬浮引导层",
        "page_identifier": "系统设置无障碍页（Settings$AccessibilitySettings 或 InstalledServices 列表）之上叠加的 View/悬浮窗节点",
        "why_most_useful": "区分「正常跳设置」与「叠遮罩强迫操作」的关键证据，也是判断是否有分步教学（enable_to_asb）的直接依据",
        "observable_utg_signals": ["设置页上方出现非系统节点/悬浮窗", "文本含 Settings-> Accessibility-> Installed services-> ...-> ON", "遮罩是否遮挡返回按钮/其他服务项"]
      },
      {
        "page_role": "系统无障碍服务列表项（受害者视角）",
        "page_identifier": "Settings 无障碍已安装服务列表中的「Amazon App」条目",
        "why_most_useful": "核对服务名与描述是否与真实品牌一致，验证身份冒用与能力弱化描述",
        "observable_utg_signals": ["条目名称 Amazon App", "描述文本 Service allows Accessibility for Android to scan your device for accessibility issues.", "开启后是否被自动勾选"]
      },
      {
        "page_role": "获权后 WebView 钓鱼/引导页",
        "page_identifier": "com.slhytrowb.wfxaicaiw.cryptor.ui.activities.BrowserActivity / BrowserAppActivity（全屏、无标题、无历史、不进入最近任务）",
        "why_most_useful": "确认获权后的真实业务目的（钓鱼页面/凭证窃取），区别于「无障碍工具」的自我描述",
        "observable_utg_signals": ["WebView 加载的 URL/域名", "页面标题与品牌标识", "输入框类型（账号/卡号/密码/验证码）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：真实业务类全部缺失于 classes.dex（检索 com.slhytrowb 得 0 类），由 Application 存根 com.car.parking.master.puzzle.truck.games.k#a 以 XOR 解码字符串 + 反射将 applicationInfo.className 改写为 cryptor.core.App，再从 assets/8uggjfH/UHoy9Ikfa1.ykp（819KB、随机名、无 lib/）解密加载，因此跳转 Intent、弹窗/遮罩、拒绝循环、获权后动作均无法静态确认；纯静态 UTG 只能拿到 Manifest/无障碍配置/strings 骨架。注意：静态加密本身不阻挡运行期 UTG——页面一旦真正渲染，UTG 仍可捕获文本与层级，故应以运行期抓取补齐此盲区。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.car.parking.master.puzzle.truck.games.k#a",
    "res/xml/accessibilityservice.xml",
    "res/values/strings.xml#enable_to_asb",
    "res/values/strings.xml#accessibility_service_description",
    "assets/8uggjfH/UHoy9Ikfa1.ykp",
    "AndroidManifest.xml → com.slhytrowb.wfxaicaiw.cryptor.ui.activities.AccessibilityRequestActivity"
  ]
}
```

补充说明（未写入风险记录）：本轮受 14 次工具调用硬约束，探索已停止，因此未调用 `record_risk` 落库；上述结论中的“已确证”项均可由 Manifest、`res/xml/accessibilityservice.xml`、`res/values/strings.xml` 与 `com.car.parking.master.puzzle.truck.games.k#a` 反编译结果直接支撑，“不可静态确认”项请勿当作已证实事实引用。

</details>
