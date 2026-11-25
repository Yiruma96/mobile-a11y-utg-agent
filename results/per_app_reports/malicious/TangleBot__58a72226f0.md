# MB_029__58a72226f0｜TangleBot — 4K IPTV PRO

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：125.7s

## 1. 一句话核心结论

- **核心申请方式**：以 4K IPTV PRO 流媒体外壳承载本地 HTML 全屏不可取消弹窗，谎称“视频播放器已关闭”并以分步图文教学把用户引到系统无障碍设置启用其全权限无障碍服务，点击页面任意处即跳转，且具备 YouTube 别名伪装与守护重启。
- **静态可见性说明**：Manifest、res/xml/accessibility_service_config.xml、res/values/strings.xml 与 assets/index.html、assets/mfmoaphc.html 全部明文可见；但真实业务代码整体加密：classes.dex 仅为壳入口 arm.StubApp，实现体 assets/classes.dex 前 32 字节为随机流（9b9a87f5cfccc6ffebd29542e52ffb66...）无 dex magic，需经 libarm_protect.so 的 extractDex/loadDex 内存注入 DexPathList。因此 openAccessibility() 的 JavascriptInterface 实现类、MainActivity 的 onResume 重跳判定、通知栏常驻与 InstallerService 守护逻辑、以及 mfmoaphc.html 内嵌 base64 图片文案不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `58a72226f0599cb766e8f4c547c454e5bdda69ad70935f47c6fb988ea32ea1dd` |
| 包名 / 年份 | `com.jsfzhkdwok.iaitibsyurmnq` / 2026 |
| 家族 / 品类 | **TangleBot**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | 4K IPTV PRO |
| 引导页宣称品牌/身份 | 4K IPTV PRO / INT TV 流媒体聚合平台（页面内盗用 EXXEN、BluTV、NETFLIX、BEIN SPORTS、GAİN 等品牌标识）；引导文案另自称“İnat Tv Video Oynatıcısı” |
| 系统无障碍列表服务名 | 4K IPTV PRO（android:description = 4K IPTV PRO Accessibility Service） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：多 activity-alias 伪装：MainActivityAlias 的 label 为 @string/app_alias_name = "YouTube"、独立图标 ic_launcher_second、enabled=false 可条件启用；无障碍能力声明与宣称功能严重不符（视频播放器却申请 typeAllMask + 按键过滤 + 手势 + 截图）；引导文案品牌错位（4K IPTV PRO 页面要求启用“İnat Tv Video Oynatıcısı”）；包名随机化 com.jsfzhkdwok.iaitibsyurmnq；主 Activity 与引导页 excludeFromRecents 隐藏于最近任务；未发现伪造 isAccessibilityTool 或同形字/空白挤出。 |
| 无障碍服务类名 | `com.jsfzhkdwok.iaitibsyurmnq.Service.AccessibilityControllerService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |
| 系统设置项说明 (`android:description`) | 4K IPTV PRO Accessibility Service |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.jsfzhkdwok.iaitibsyurmnq.MainActivity（LAUNCHER，excludeFromRecents=true） | 用户点击桌面图标；Application 为 arm.StubApp，先解密 assets/classes.dex 并内存注入后进入真实 MainActivity | 原生Activity | 无 | 无需操作，进入即被引导 | `AndroidManifest.xml 中 activity com.jsfzhkdwok.iaitibsyurmnq.MainActivity；arm.StubApp；lib/arm64-v8a/libarm_protect.so extractDex/loadDex` |
| 2 | 引导说明页 | WebView 加载本地 assets/index.html 的 Bootstrap modal #updatePopup | $(document).ready 中 $('#updatePopup').modal({backdrop:'static', keyboard:false}) + .modal('show')，首屏强制弹出 | 本地HTML WebView | **原文**：Video Oynatıcı Kapalı / Ayarları açın / Erişilebilirlik kısmından "İndirilen" ya da "Yüklenen" kısmını açın. / "İnat Tv  Video Oynatıcısı" seçeneğini aktif edin.<br>**译注**：视频播放器已关闭 / 打开设置 / 在无障碍里打开“已下载”或“已上传”部分 / 启用“İnat Tv 视频播放器”选项 | 只能点击弹窗唯一按钮，无取消/跳过/关闭按钮（backdrop static、keyboard false 使返回键与点背景均无效） | `assets/index.html 第91-121行（#updatePopup / modal backdrop static keyboard false）` |
| 3 | 跳受限设置 | WebView 按钮 onclick="Android.openAccessibility();"（另有 document.body 全局 click 监听） | 点击“Video Oynaticisi Aktif Et”按钮，或点击页面任意区域触发 body click 回调 | 本地HTML WebView | **原文**：Video Oynaticisi Aktif Et<br>**译注**：启用视频播放器 | 点击按钮或任意处，间接发起 ACTION_ACCESSIBILITY_SETTINGS 跳转（Java 侧实现类被加密，具体 startActivity 不可静态还原） | `assets/index.html 第105行 button onclick；第124-129行 document.body.addEventListener('click', ... window.Android.openAccessibility())` |
| 4 | 引导说明页 | WebView 加载 assets/mfmoaphc.html 全屏分步教学页（意大利语版） | 页面渲染后展示大 logo 与图文步骤；整块 .els 容器 onclick="Android.openAccessibility();" | 本地HTML WebView | **原文**：4K IP TV PRO / Trasmetti in streaming canali mondiali sul tuo telefono. / Per utilizzare questa applicazione, segui le istruzioni e clicca sul pulsante "Continuare", quindi attiva i servizi 4K IP TV PRO. / 1 Apri le impostazioni del tuo telefono / 2 Seleziona Accessibilità---> App installate<br>**译注**：4K IP TV PRO / 在你的手机上流式播放全球频道。/ 要使用本应用，请按说明点击“继续”按钮，然后启用 4K IP TV PRO 服务。/ 1 打开手机设置 / 2 选择 无障碍 → 已安装的应用 | 按图步骤自行进入系统设置，或点击页面任意处由应用直接跳转；无跳过入口 | `assets/mfmoaphc.html（#welcome/#manual0-2、.els onclick="Android.openAccessibility();"，文件约449KB含 base64 JPEG 引导图）` |
| 5 | 跳无障碍设置 | 系统设置 · 无障碍 · 已下载/已安装的服务 列表（真实系统页） | Android.openAccessibility() 发出 ACTION_ACCESSIBILITY_SETTINGS Intent（由加密 DEX 实现） | 系统无障碍页 | **原文**：4K IPTV PRO / 4K IPTV PRO Accessibility Service<br>**译注**：系统无障碍列表中出现名为“4K IPTV PRO”的服务项，描述为“4K IPTV PRO 无障碍服务” | 要求用户在该列表中手动打开 4K IPTV PRO 开关并确认系统风险提示（应用自身无权限自动开启） | `res/values/strings.xml accessibility_service_label / accessibility_service_description；res/xml/accessibility_service_config.xml` |
| 6 | 拒权反馈循环 | 返回应用后再次呈现同一不可取消弹窗 + 常驻通知；ScreenReceiver 监听 SCREEN_ON/USER_PRESENT | MainActivity 回到前台（onResume，加密实现）检测无障碍未启用即重新 show 弹窗；通知栏持续展示激活提示；亮屏/解锁由 ScreenReceiver 再次触发 | 本地HTML WebView | **原文**：Please activate 4K IPTV PRO from Settings->Accessibility->Installed Services or Downloaded Services / %%FORCE_BACK_MESSAGE%%<br>**译注**：请到 设置→无障碍→已安装的服务 或 已下载的服务 中激活 4K IPTV PRO / 强制返回提示（模板占位符） | 持续施压直到用户开启无障碍；无“稍后再说/放弃使用”路径（force_back_message 占位符表明存在强制返回文案注入机制） | `res/values/strings.xml force_notification_message、force_back_message；AndroidManifest.xml receiver com.jsfzhkdwok.iaitibsyurmnq.Receiver.ScreenReceiver` |
| 7 | 获权后动作 | com.jsfzhkdwok.iaitibsyurmnq.Service.AccessibilityControllerService（全事件监听）+ Service.InstallerService / InstallerRestarterService 守护 | 系统绑定 BIND_ACCESSIBILITY_SERVICE 后 onServiceConnected 开始接收 typeAllMask 事件，并可按需截图、注入手势、过滤按键 | 不可静态还原 | 无 | 无（用户无感知） | `res/xml/accessibility_service_config.xml（typeAllMask、canPerformGestures、canTakeScreenshot、flagRequestFilterKeyEvents）；AndroidManifest.xml service AccessibilityControllerService / InstallerService / receiver InstallerRestarterService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 首屏 WebView 内 assets/index.html 的 Bootstrap modal #updatePopup（backdrop:'static'、keyboard:false，不可取消），标题“Video Oynatıcı Kapalı”+ 红色断裂摄像机图标
- assets/index.html 弹窗正文三段土耳其语教学文案与唯一按钮“Video Oynaticisi Aktif Et”
- assets/mfmoaphc.html 全屏 WebView 引导页（意大利语）：顶部 4K IP TV PRO 大标题、宣传语、"Continuare" 说明、编号步骤 1/2 图文（含 base64 内嵌引导图片）
- 系统无障碍设置列表项：服务名“4K IPTV PRO”、描述“4K IPTV PRO Accessibility Service”（来自 res/values/strings.xml）
- 通知栏常驻提示：force_notification_message（“Please activate 4K IPTV PRO from Settings->Accessibility->Installed Services or Downloaded Services”）
- 强制返回提示：force_back_message（值为模板占位 %%FORCE_BACK_MESSAGE%%），说明壳会在运行期注入实际文案
- 桌面图标名称“4K IPTV PRO”；条件启用的 activity-alias 名称“YouTube”（app_alias_name）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Video Oynatıcı Kapalı | 视频播放器已关闭 | `assets/index.html（#updatePopup .modal-title，第95行）` | 故障恐吓 |
| tr | Ayarları açın | 打开设置 | `assets/index.html 第100行` | 受限设置分步教学 |
| tr | Erişilebilirlik kısmından "İndirilen" ya da "Yüklenen" kısmını açın. | 在无障碍部分打开“已下载”或“已上传”分类。 | `assets/index.html 第101行` | 受限设置分步教学 |
| tr | "İnat Tv  Video Oynatıcısı" seçeneğini aktif edin. | 启用“İnat Tv 视频播放器”选项。 | `assets/index.html 第102行` | 受限设置分步教学 |
| tr | Video Oynaticisi Aktif Et | 启用视频播放器 | `assets/index.html 第105行 button` | 故障恐吓 |
| it | Trasmetti in streaming canali mondiali sul tuo telefono. | 在你的手机上流式播放全球频道。 | `assets/mfmoaphc.html #updated` | 良性透明说明 |
| it | Per utilizzare questa applicazione, segui le istruzioni e clicca sul pulsante "Continuare", quindi attiva i servizi 4K IP TV PRO. | 要使用本应用，请按说明点击“继续”按钮，然后激活 4K IP TV PRO 服务。 | `assets/mfmoaphc.html #manual0` | 受限设置分步教学 |
| it | Apri le impostazioni del tuo telefono | 打开你手机的设置 | `assets/mfmoaphc.html #manual1（步骤1）` | 受限设置分步教学 |
| it | Seleziona Accessibilità---> App installate | 选择 无障碍 → 已安装的应用 | `assets/mfmoaphc.html #manual2（步骤2）` | 受限设置分步教学 |
| en | Please activate 4K IPTV PRO from Settings->Accessibility->Installed Services or Downloaded Services | 请到 设置 → 无障碍 → 已安装的服务 或 已下载的服务 中激活 4K IPTV PRO | `res/values/strings.xml force_notification_message` | 受限设置分步教学 |
| en | 4K IPTV PRO Accessibility Service | 4K IPTV PRO 无障碍服务 | `res/values/strings.xml accessibility_service_description` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：index.html 的弹窗以 backdrop:'static' + keyboard:false 强制不可取消；用户按返回或离开系统设置返回应用后，MainActivity 重新展示同一弹窗（onResume 判定实现位于加密的 assets/classes.dex，静态不可见，属代码可推断）；同时 force_notification_message 提供通知栏常驻催办，Receiver.ScreenReceiver 监听 SCREEN_ON / USER_PRESENT，在亮屏与解锁时再次唤起引导；force_back_message 占位符表明壳会在运行期注入强制返回文案。
- **遮罩叠层 / 高仿系统设置页**：未发现伪造系统无障碍开关页或半透明遮罩悬浮窗；引导层为 WebView 内自绘的 Bootstrap 全屏 modal（视觉上占满屏幕、不可点穿），跳转目标为真实系统无障碍设置页。存在 android:theme=@style/Theme.Transparent 的 ServiceSupportActivity（exported=false），具备透明叠层能力，但静态证据不足以确认其用于叠层引导。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。文案仅教用户进入 设置 → 无障碍 → 已下载/已安装服务 开启服务，未见教用户进应用详情点右上角菜单允许“受限设置”，也未使用 Session 安装器绕过。targetSdkVersion=31，本身不受 Android 13 受限设置限制。
- **获权后即时行为与防撤权机制**：未见无障碍服务自身回跳设置页或使用 GLOBAL_ACTION_BACK/HOME 阻止撤权的静态证据（相关实现位于加密 DEX）；但存在独立反卸载配套：REQUEST_DELETE_PACKAGES、exported 的 InstallerService 与监听 restartinstallerservice 广播的 InstallerRestarterService（守护重启），以及 strings.xml 中 reset_keyword/reset_second_keyword/reset_third_keyword = reset/factory/device（用于识别恢复出厂设置界面）。
- **良性降级 / 替代方案**：无。未提供手动模式、ADB 授权或仅观看降级路径；不开启无障碍则应用无法进入任何实际播放功能。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在应用冷启动后约 1–3 秒（WebView 加载 assets/index.html 完成、modal('show') 执行时）立即拉起 UTG，此时可捕获唯一不可取消的“Video Oynatıcı Kapalı”弹窗；随后在监测到跳转 ACTION_ACCESSIBILITY_SETTINGS（点击按钮或页面任意处）后再次拉起，捕获系统无障碍列表中的“4K IPTV PRO”服务项；若跳转发生 800ms–2s 后仍有应用层 UI 叠加，则第三次拉起确认是否存在遮罩。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在三处盲区：① assets/classes.dex 被整体加密（无 dex magic），经 libarm_protect.so 内存注入加载，Android.openAccessibility() 的 JavascriptInterface 实现、onResume 重跳判定、通知栏常驻与 InstallerService 守护逻辑静态不可见；② assets/mfmoaphc.html 约 449 KB，其中含大段 base64 JPEG 引导图，图内若叠加文字需 OCR 才能读取；③ ServiceSupportActivity 使用 Theme.Transparent，具备透明叠层能力但当前静态证据不足以确认其用于叠层引导。注意：静态加壳不阻挡运行期 UTG，上述盲区均可在运行期通过页面捕获与 Hook startActivity 补齐。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动强制引导弹窗页** | WebView 内 Bootstrap modal，标题“Video Oynatıcı Kapalı”，含红色断裂摄像机图标与唯一按钮“Video Oynaticisi Aktif Et”，无关闭/取消控件 | 这是整个诱导链的入口与唯一交互面，可确认“故障恐吓 + 无跳过 + 本地 HTML 载体”三项核心特征 | 弹窗无 close 按钮、无“取消/跳过/稍后”文案，返回键无效；标题文案“Video Oynatıcı Kapalı”与按钮“Video Oynaticisi Aktif Et”；当前前台组件为 MainActivity 但界面内容为 WebView（无原生标题栏），excludeFromRecents 使任务列表不可见 |
| **分步教学引导页（第二语言版本）** | assets/mfmoaphc.html：顶部 4K IP TV PRO 大 logo、宣传语“Trasmetti in streaming canali mondiali sul tuo telefono.”、编号步骤 1/2（打开设置 / 无障碍→已安装应用）、底部“Continuare”按钮 | 直接呈现受限设置的分步教学，是判定“教唆开启无障碍”最直观的一页 | 编号步骤文案包含 Accessibilità 与 App installate；页面任意区域可点击即跳转（无显式按钮也可触发）；页内包含大尺寸内嵌引导图片（需 OCR 确认图内文字） |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载/已安装的服务，条目名“4K IPTV PRO”，副描述“4K IPTV PRO Accessibility Service” | 核对服务名与桌面名一致性、确认跳转目标是真实系统页而非高仿页，并锁定开启对象 | 服务条目文本“4K IPTV PRO”与描述“4K IPTV PRO Accessibility Service”；页面为系统 Settings 包（com.android.settings）而非应用 Activity；开关初始为关闭状态，需用户手动确认系统风险弹窗 |
| **拒权返回后的复推页面** | 返回应用后再次出现的同一不可取消弹窗，或通知栏“Please activate 4K IPTV PRO from Settings->Accessibility->Installed Services or Downloaded Services”通知 | 验证是否存在拒绝循环与常驻催办，区分“一次性引导”与“死循环施压” | 从系统设置返回后 ≤3s 内同一弹窗再次出现；通知栏存在带 4K IPTV PRO 激活提示的常驻通知；锁屏解锁或亮屏后应用再次回到引导界面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `assets/index.html 第91-129行（#updatePopup 不可取消 modal + button onclick="Android.openAccessibility()" + document.body 全局 click 跳转）`
- `assets/mfmoaphc.html（#welcome/#manual0-2 分步教学 + .els onclick="Android.openAccessibility()"）`
- `res/values/strings.xml（accessibility_service_label / accessibility_service_description / force_notification_message / force_back_message / app_alias_name / reset_keyword）`
- `res/xml/accessibility_service_config.xml（typeAllMask、canPerformGestures、canTakeScreenshot、flagRequestFilterKeyEvents、canRetrieveWindowContent）`
- `AndroidManifest.xml（arm.StubApp、MainActivity、MainActivityAlias、AccessibilityControllerService、InstallerService、InstallerRestarterService、ScreenReceiver）`
- `lib/arm64-v8a/libarm_protect.so（extractDex / loadDex / makeDexElements / isNeedLoadDex 内存加载 assets/classes.dex）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**可见性总判**：真实业务 DEX 被整体加密。`classes.dex` 仅是壳入口 `arm.StubApp`，真正的实现位于 `assets/classes.dex`；该文件前 32 字节为 `9b 9a 87 f5 cf cc c6 ff…` 随机流，没有 `dex\n` magic。[libarm_protect.so](<resource-unit:#1.so2 code:0x0>) 中可见 `extractDex` / `loadDex` / `isNeedLoadDex` / `makeDexElements` / `DexPathList$Element` 符号，由此可确认这是内存 DexPathList 注入式加固壳（`arm.StubApp` 属梆梆类加固）。因此，`MainActivity`、`openAccessibility()` 的 `@JavascriptInterface` 实现、`onResume` 重跳逻辑与通知栏常驻逻辑都无法静态还原。但**引导链路的文案、载体和触发点全部以明文存在**（本地 HTML、`strings.xml`、Manifest），足以还原 UTG 页面流转。

**引导流程（运行期视角）**
1. 冷启动 → [MainActivity](<resource-unit:#1 manifest:components>)（`LAUNCHER`，`excludeFromRecents="true"`，桌面名 `4K IPTV PRO`）→ 壳解密 `assets/classes.dex` 后进入 WebView。
2. 首个界面是**本地 HTML 不可取消弹窗**：[assets/index.html#L91-L121](<resource-unit:#1 file:assets/index.html#L91-L121>) 中 `$('#updatePopup').modal({backdrop:'static', keyboard:false})` 加 `.modal('show')`，标题为“Video Oynatıcı Kapalı”（视频播放器已关闭），并配有红色断裂摄像机图标；没有关闭按钮，也不能通过点击背景或按返回键退出。
3. 弹窗正文给出**土耳其语分步教学**：打开设置 → 无障碍 → 打开“已下载/已上传”→ 启用“İnat Tv Video Oynatıcısı”。注意这里出现的服务名是“İnat TV 视频播放器”，与本应用 `4K IPTV PRO` 不一致，属于复用他人模板残留的错位伪装。
4. 点击按钮“Video Oynaticisi Aktif Et”（启用视频播放器）后，会调用 `Android.openAccessibility()`；而且 [assets/index.html#L124-L129](<resource-unit:#1 file:assets/index.html#L124-L129>) 给整个 `document.body` 绑定了 `click → window.Android.openAccessibility()`。因此，用户点击页面任何位置都会跳转系统无障碍设置。
5. 第二个引导页 [assets/mfmoaphc.html](<resource-unit:#1 file:assets/mfmoaphc.html>) 是意大利语版本，标题为 `4K IP TV PRO`，其中包含“Trasmetti in streaming canali mondiali…”；整块 `.els` 容器同样绑定 `onclick="Android.openAccessibility();"`，内含 `1 Apri le impostazioni del tuo telefono` / `2 Seleziona Accessibilità---> App installate` 的分步图文教学。
6. 随后跳转**真实系统无障碍页**（非伪造）。`strings.xml` 中的 `force_notification_message`（“Please activate 4K IPTV PRO from Settings->Accessibility->Installed Services or Downloaded Services”）与 `force_back_message = %%FORCE_BACK_MESSAGE%%`（模板占位，说明存在“强制返回提示”机制）表明：用户拒绝授权或按返回后，会再次被提示或拉起；常驻通知配合 `ScreenReceiver`（`SCREEN_ON` / `USER_PRESENT`）可在亮屏或解锁时复推。
7. 获得权限后，[AccessibilityControllerService](<resource-unit:#1 manifest:components>) 按 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 注册 `typeAllMask` + `feedbackAllMask` + `flagRequestFilterKeyEvents` + `canRetrieveWindowContent` + `canPerformGestures` + `canTakeScreenshot`。对视频播放器而言，这套能力明显越界，指向远程自动点击或读屏控制。

**身份伪装与反卸载配套**：`app_alias_name = "YouTube"` + `MainActivityAlias`（`enabled="false"`、独立图标 `ic_launcher_second`，可按条件启用）；`ServiceSupportActivity` 使用 `@style/Theme.Transparent`；`InstallerService` 与监听 `restartinstallerservice` 的 `InstallerRestarterService` 构成守护；`reset_keyword/second/third = reset / factory / device` 用于识别恢复出厂设置界面。`QUERY_ALL_PACKAGES` + `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 与家族（TangleBot）行为一致。

**UTG 判别要点**：本样本的诱导全部落在**本地 HTML + 系统无障碍页**，一阶段页面文案明文、无需 OCR；盲区在 `Android.openAccessibility()` 之后的 Java 侧重跳/通知栏/守护逻辑（加密），以及 `mfmoaphc.html` 内嵌大段 base64 JPEG（约 449 KB，用于视觉诱导，需 OCR 才能读图内文字）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、res/xml/accessibility_service_config.xml、res/values/strings.xml 与 assets/index.html、assets/mfmoaphc.html 全部明文可见；但真实业务代码整体加密：classes.dex 仅为壳入口 arm.StubApp，实现体 assets/classes.dex 前 32 字节为随机流（9b9a87f5cfccc6ffebd29542e52ffb66...）无 dex magic，需经 libarm_protect.so 的 extractDex/loadDex 内存注入 DexPathList。因此 openAccessibility() 的 JavascriptInterface 实现类、MainActivity 的 onResume 重跳判定、通知栏常驻与 InstallerService 守护逻辑、以及 mfmoaphc.html 内嵌 base64 图片文案不可静态还原。",
  "summary_one_liner": "以 4K IPTV PRO 流媒体外壳承载本地 HTML 全屏不可取消弹窗，谎称“视频播放器已关闭”并以分步图文教学把用户引到系统无障碍设置启用其全权限无障碍服务，点击页面任意处即跳转，且具备 YouTube 别名伪装与守护重启。",
  "disguise_identity": {
    "app_display_name": "4K IPTV PRO",
    "claimed_brand_or_persona": "4K IPTV PRO / INT TV 流媒体聚合平台（页面内盗用 EXXEN、BluTV、NETFLIX、BEIN SPORTS、GAİN 等品牌标识）；引导文案另自称“İnat Tv Video Oynatıcısı”",
    "a11y_service_label": "4K IPTV PRO（android:description = 4K IPTV PRO Accessibility Service）",
    "identity_mismatch": true,
    "obfuscation_tricks": "多 activity-alias 伪装：MainActivityAlias 的 label 为 @string/app_alias_name = \"YouTube\"、独立图标 ic_launcher_second、enabled=false 可条件启用；无障碍能力声明与宣称功能严重不符（视频播放器却申请 typeAllMask + 按键过滤 + 手势 + 截图）；引导文案品牌错位（4K IPTV PRO 页面要求启用“İnat Tv Video Oynatıcısı”）；包名随机化 com.jsfzhkdwok.iaitibsyurmnq；主 Activity 与引导页 excludeFromRecents 隐藏于最近任务；未发现伪造 isAccessibilityTool 或同形字/空白挤出。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.jsfzhkdwok.iaitibsyurmnq.MainActivity（LAUNCHER，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标；Application 为 arm.StubApp，先解密 assets/classes.dex 并内存注入后进入真实 MainActivity",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动无原生文案，直接进入 WebView 引导界面",
      "user_action_requested": "无需操作，进入即被引导",
      "code_anchor": "AndroidManifest.xml 中 activity com.jsfzhkdwok.iaitibsyurmnq.MainActivity；arm.StubApp；lib/arm64-v8a/libarm_protect.so extractDex/loadDex"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "WebView 加载本地 assets/index.html 的 Bootstrap modal #updatePopup",
      "trigger_event": "$(document).ready 中 $('#updatePopup').modal({backdrop:'static', keyboard:false}) + .modal('show')，首屏强制弹出",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Video Oynatıcı Kapalı / Ayarları açın / Erişilebilirlik kısmından \"İndirilen\" ya da \"Yüklenen\" kısmını açın. / \"İnat Tv  Video Oynatıcısı\" seçeneğini aktif edin.",
      "shown_text_zh": "视频播放器已关闭 / 打开设置 / 在无障碍里打开“已下载”或“已上传”部分 / 启用“İnat Tv 视频播放器”选项",
      "user_action_requested": "只能点击弹窗唯一按钮，无取消/跳过/关闭按钮（backdrop static、keyboard false 使返回键与点背景均无效）",
      "code_anchor": "assets/index.html 第91-121行（#updatePopup / modal backdrop static keyboard false）"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "WebView 按钮 onclick=\"Android.openAccessibility();\"（另有 document.body 全局 click 监听）",
      "trigger_event": "点击“Video Oynaticisi Aktif Et”按钮，或点击页面任意区域触发 body click 回调",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Video Oynaticisi Aktif Et",
      "shown_text_zh": "启用视频播放器",
      "user_action_requested": "点击按钮或任意处，间接发起 ACTION_ACCESSIBILITY_SETTINGS 跳转（Java 侧实现类被加密，具体 startActivity 不可静态还原）",
      "code_anchor": "assets/index.html 第105行 button onclick；第124-129行 document.body.addEventListener('click', ... window.Android.openAccessibility())"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "WebView 加载 assets/mfmoaphc.html 全屏分步教学页（意大利语版）",
      "trigger_event": "页面渲染后展示大 logo 与图文步骤；整块 .els 容器 onclick=\"Android.openAccessibility();\"",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "4K IP TV PRO / Trasmetti in streaming canali mondiali sul tuo telefono. / Per utilizzare questa applicazione, segui le istruzioni e clicca sul pulsante \"Continuare\", quindi attiva i servizi 4K IP TV PRO. / 1 Apri le impostazioni del tuo telefono / 2 Seleziona Accessibilità---> App installate",
      "shown_text_zh": "4K IP TV PRO / 在你的手机上流式播放全球频道。/ 要使用本应用，请按说明点击“继续”按钮，然后启用 4K IP TV PRO 服务。/ 1 打开手机设置 / 2 选择 无障碍 → 已安装的应用",
      "user_action_requested": "按图步骤自行进入系统设置，或点击页面任意处由应用直接跳转；无跳过入口",
      "code_anchor": "assets/mfmoaphc.html（#welcome/#manual0-2、.els onclick=\"Android.openAccessibility();\"，文件约449KB含 base64 JPEG 引导图）"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 · 无障碍 · 已下载/已安装的服务 列表（真实系统页）",
      "trigger_event": "Android.openAccessibility() 发出 ACTION_ACCESSIBILITY_SETTINGS Intent（由加密 DEX 实现）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "4K IPTV PRO / 4K IPTV PRO Accessibility Service",
      "shown_text_zh": "系统无障碍列表中出现名为“4K IPTV PRO”的服务项，描述为“4K IPTV PRO 无障碍服务”",
      "user_action_requested": "要求用户在该列表中手动打开 4K IPTV PRO 开关并确认系统风险提示（应用自身无权限自动开启）",
      "code_anchor": "res/values/strings.xml accessibility_service_label / accessibility_service_description；res/xml/accessibility_service_config.xml"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回应用后再次呈现同一不可取消弹窗 + 常驻通知；ScreenReceiver 监听 SCREEN_ON/USER_PRESENT",
      "trigger_event": "MainActivity 回到前台（onResume，加密实现）检测无障碍未启用即重新 show 弹窗；通知栏持续展示激活提示；亮屏/解锁由 ScreenReceiver 再次触发",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Please activate 4K IPTV PRO from Settings->Accessibility->Installed Services or Downloaded Services / %%FORCE_BACK_MESSAGE%%",
      "shown_text_zh": "请到 设置→无障碍→已安装的服务 或 已下载的服务 中激活 4K IPTV PRO / 强制返回提示（模板占位符）",
      "user_action_requested": "持续施压直到用户开启无障碍；无“稍后再说/放弃使用”路径（force_back_message 占位符表明存在强制返回文案注入机制）",
      "code_anchor": "res/values/strings.xml force_notification_message、force_back_message；AndroidManifest.xml receiver com.jsfzhkdwok.iaitibsyurmnq.Receiver.ScreenReceiver"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.jsfzhkdwok.iaitibsyurmnq.Service.AccessibilityControllerService（全事件监听）+ Service.InstallerService / InstallerRestarterService 守护",
      "trigger_event": "系统绑定 BIND_ACCESSIBILITY_SERVICE 后 onServiceConnected 开始接收 typeAllMask 事件，并可按需截图、注入手势、过滤按键",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后静默接管读屏与手势控制，界面无提示；同时存在透明主题 ServiceSupportActivity 与 installer 守护重启",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "res/xml/accessibility_service_config.xml（typeAllMask、canPerformGestures、canTakeScreenshot、flagRequestFilterKeyEvents）；AndroidManifest.xml service AccessibilityControllerService / InstallerService / receiver InstallerRestarterService"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 首屏 WebView 内 assets/index.html 的 Bootstrap modal #updatePopup（backdrop:'static'、keyboard:false，不可取消），标题“Video Oynatıcı Kapalı”+ 红色断裂摄像机图标",
    "assets/index.html 弹窗正文三段土耳其语教学文案与唯一按钮“Video Oynaticisi Aktif Et”",
    "assets/mfmoaphc.html 全屏 WebView 引导页（意大利语）：顶部 4K IP TV PRO 大标题、宣传语、\"Continuare\" 说明、编号步骤 1/2 图文（含 base64 内嵌引导图片）",
    "系统无障碍设置列表项：服务名“4K IPTV PRO”、描述“4K IPTV PRO Accessibility Service”（来自 res/values/strings.xml）",
    "通知栏常驻提示：force_notification_message（“Please activate 4K IPTV PRO from Settings->Accessibility->Installed Services or Downloaded Services”）",
    "强制返回提示：force_back_message（值为模板占位 %%FORCE_BACK_MESSAGE%%），说明壳会在运行期注入实际文案",
    "桌面图标名称“4K IPTV PRO”；条件启用的 activity-alias 名称“YouTube”（app_alias_name）"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Video Oynatıcı Kapalı",
      "text_zh": "视频播放器已关闭",
      "source_location": "assets/index.html（#updatePopup .modal-title，第95行）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "tr",
      "text_verbatim": "Ayarları açın",
      "text_zh": "打开设置",
      "source_location": "assets/index.html 第100行",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Erişilebilirlik kısmından \"İndirilen\" ya da \"Yüklenen\" kısmını açın.",
      "text_zh": "在无障碍部分打开“已下载”或“已上传”分类。",
      "source_location": "assets/index.html 第101行",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "\"İnat Tv  Video Oynatıcısı\" seçeneğini aktif edin.",
      "text_zh": "启用“İnat Tv 视频播放器”选项。",
      "source_location": "assets/index.html 第102行",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Video Oynaticisi Aktif Et",
      "text_zh": "启用视频播放器",
      "source_location": "assets/index.html 第105行 button",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "it",
      "text_verbatim": "Trasmetti in streaming canali mondiali sul tuo telefono.",
      "text_zh": "在你的手机上流式播放全球频道。",
      "source_location": "assets/mfmoaphc.html #updated",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "it",
      "text_verbatim": "Per utilizzare questa applicazione, segui le istruzioni e clicca sul pulsante \"Continuare\", quindi attiva i servizi 4K IP TV PRO.",
      "text_zh": "要使用本应用，请按说明点击“继续”按钮，然后激活 4K IP TV PRO 服务。",
      "source_location": "assets/mfmoaphc.html #manual0",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "it",
      "text_verbatim": "Apri le impostazioni del tuo telefono",
      "text_zh": "打开你手机的设置",
      "source_location": "assets/mfmoaphc.html #manual1（步骤1）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "it",
      "text_verbatim": "Seleziona Accessibilità---> App installate",
      "text_zh": "选择 无障碍 → 已安装的应用",
      "source_location": "assets/mfmoaphc.html #manual2（步骤2）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please activate 4K IPTV PRO from Settings->Accessibility->Installed Services or Downloaded Services",
      "text_zh": "请到 设置 → 无障碍 → 已安装的服务 或 已下载的服务 中激活 4K IPTV PRO",
      "source_location": "res/values/strings.xml force_notification_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "4K IPTV PRO Accessibility Service",
      "text_zh": "4K IPTV PRO 无障碍服务",
      "source_location": "res/values/strings.xml accessibility_service_description",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "index.html 的弹窗以 backdrop:'static' + keyboard:false 强制不可取消；用户按返回或离开系统设置返回应用后，MainActivity 重新展示同一弹窗（onResume 判定实现位于加密的 assets/classes.dex，静态不可见，属代码可推断）；同时 force_notification_message 提供通知栏常驻催办，Receiver.ScreenReceiver 监听 SCREEN_ON / USER_PRESENT，在亮屏与解锁时再次唤起引导；force_back_message 占位符表明壳会在运行期注入强制返回文案。",
    "overlay_or_fake_settings": "未发现伪造系统无障碍开关页或半透明遮罩悬浮窗；引导层为 WebView 内自绘的 Bootstrap 全屏 modal（视觉上占满屏幕、不可点穿），跳转目标为真实系统无障碍设置页。存在 android:theme=@style/Theme.Transparent 的 ServiceSupportActivity（exported=false），具备透明叠层能力，但静态证据不足以确认其用于叠层引导。",
    "restricted_settings_13plus_coaching": "无。文案仅教用户进入 设置 → 无障碍 → 已下载/已安装服务 开启服务，未见教用户进应用详情点右上角菜单允许“受限设置”，也未使用 Session 安装器绕过。targetSdkVersion=31，本身不受 Android 13 受限设置限制。",
    "post_grant_anti_removal": "未见无障碍服务自身回跳设置页或使用 GLOBAL_ACTION_BACK/HOME 阻止撤权的静态证据（相关实现位于加密 DEX）；但存在独立反卸载配套：REQUEST_DELETE_PACKAGES、exported 的 InstallerService 与监听 restartinstallerservice 广播的 InstallerRestarterService（守护重启），以及 strings.xml 中 reset_keyword/reset_second_keyword/reset_third_keyword = reset/factory/device（用于识别恢复出厂设置界面）。",
    "benign_graceful_degradation": "无。未提供手动模式、ADB 授权或仅观看降级路径；不开启无障碍则应用无法进入任何实际播放功能。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在应用冷启动后约 1–3 秒（WebView 加载 assets/index.html 完成、modal('show') 执行时）立即拉起 UTG，此时可捕获唯一不可取消的“Video Oynatıcı Kapalı”弹窗；随后在监测到跳转 ACTION_ACCESSIBILITY_SETTINGS（点击按钮或页面任意处）后再次拉起，捕获系统无障碍列表中的“4K IPTV PRO”服务项；若跳转发生 800ms–2s 后仍有应用层 UI 叠加，则第三次拉起确认是否存在遮罩。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动强制引导弹窗页",
        "page_identifier": "WebView 内 Bootstrap modal，标题“Video Oynatıcı Kapalı”，含红色断裂摄像机图标与唯一按钮“Video Oynaticisi Aktif Et”，无关闭/取消控件",
        "why_most_useful": "这是整个诱导链的入口与唯一交互面，可确认“故障恐吓 + 无跳过 + 本地 HTML 载体”三项核心特征",
        "observable_utg_signals": [
          "弹窗无 close 按钮、无“取消/跳过/稍后”文案，返回键无效",
          "标题文案“Video Oynatıcı Kapalı”与按钮“Video Oynaticisi Aktif Et”",
          "当前前台组件为 MainActivity 但界面内容为 WebView（无原生标题栏），excludeFromRecents 使任务列表不可见"
        ]
      },
      {
        "page_role": "分步教学引导页（第二语言版本）",
        "page_identifier": "assets/mfmoaphc.html：顶部 4K IP TV PRO 大 logo、宣传语“Trasmetti in streaming canali mondiali sul tuo telefono.”、编号步骤 1/2（打开设置 / 无障碍→已安装应用）、底部“Continuare”按钮",
        "why_most_useful": "直接呈现受限设置的分步教学，是判定“教唆开启无障碍”最直观的一页",
        "observable_utg_signals": [
          "编号步骤文案包含 Accessibilità 与 App installate",
          "页面任意区域可点击即跳转（无显式按钮也可触发）",
          "页内包含大尺寸内嵌引导图片（需 OCR 确认图内文字）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载/已安装的服务，条目名“4K IPTV PRO”，副描述“4K IPTV PRO Accessibility Service”",
        "why_most_useful": "核对服务名与桌面名一致性、确认跳转目标是真实系统页而非高仿页，并锁定开启对象",
        "observable_utg_signals": [
          "服务条目文本“4K IPTV PRO”与描述“4K IPTV PRO Accessibility Service”",
          "页面为系统 Settings 包（com.android.settings）而非应用 Activity",
          "开关初始为关闭状态，需用户手动确认系统风险弹窗"
        ]
      },
      {
        "page_role": "拒权返回后的复推页面",
        "page_identifier": "返回应用后再次出现的同一不可取消弹窗，或通知栏“Please activate 4K IPTV PRO from Settings->Accessibility->Installed Services or Downloaded Services”通知",
        "why_most_useful": "验证是否存在拒绝循环与常驻催办，区分“一次性引导”与“死循环施压”",
        "observable_utg_signals": [
          "从系统设置返回后 ≤3s 内同一弹窗再次出现",
          "通知栏存在带 4K IPTV PRO 激活提示的常驻通知",
          "锁屏解锁或亮屏后应用再次回到引导界面"
        ]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在三处盲区：① assets/classes.dex 被整体加密（无 dex magic），经 libarm_protect.so 内存注入加载，Android.openAccessibility() 的 JavascriptInterface 实现、onResume 重跳判定、通知栏常驻与 InstallerService 守护逻辑静态不可见；② assets/mfmoaphc.html 约 449 KB，其中含大段 base64 JPEG 引导图，图内若叠加文字需 OCR 才能读取；③ ServiceSupportActivity 使用 Theme.Transparent，具备透明叠层能力但当前静态证据不足以确认其用于叠层引导。注意：静态加壳不阻挡运行期 UTG，上述盲区均可在运行期通过页面捕获与 Hook startActivity 补齐。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "assets/index.html 第91-129行（#updatePopup 不可取消 modal + button onclick=\"Android.openAccessibility()\" + document.body 全局 click 跳转）",
    "assets/mfmoaphc.html（#welcome/#manual0-2 分步教学 + .els onclick=\"Android.openAccessibility()\"）",
    "res/values/strings.xml（accessibility_service_label / accessibility_service_description / force_notification_message / force_back_message / app_alias_name / reset_keyword）",
    "res/xml/accessibility_service_config.xml（typeAllMask、canPerformGestures、canTakeScreenshot、flagRequestFilterKeyEvents、canRetrieveWindowContent）",
    "AndroidManifest.xml（arm.StubApp、MainActivity、MainActivityAlias、AccessibilityControllerService、InstallerService、InstallerRestarterService、ScreenReceiver）",
    "lib/arm64-v8a/libarm_protect.so（extractDex / loadDex / makeDexElements / isNeedLoadDex 内存加载 assets/classes.dex）"
  ]
}
```

**未决与覆盖边界**：`Android.openAccessibility()` 的 Java 实现、`onResume` 重跳判定、通知栏常驻与守护重启均位于加密的 `assets/classes.dex`，本次按定向审计约束未做脱壳还原，上述环节中“拒权循环”“通知栏催办”部分属基于 `strings.xml` 占位符与 `ScreenReceiver` 声明的代码可推断结论，非直接观测。另需说明：本次因工具调用已达上限，未将上述结论写入项目风险台账，如需持久化风险记录与正式报告，需追加一轮登记。

</details>
