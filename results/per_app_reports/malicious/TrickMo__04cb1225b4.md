# MB_129__04cb1225b4｜TrickMo — Google Play Services

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：97.4s

## 1. 一句话核心结论

- **核心申请方式**：壳 Application 动态装载加密 DEX，再以本地 HTML 白屏加载页把自身伪装成 Google Play Services，用『开启无障碍服务以保证应用正常运行』的分步教学（设置→已下载服务→启用）诱导用户手动打开 typeAllMask+canPerformGestures+canTakeScreenshot 且伪造 isAccessibilityTool=true 的无障碍服务
- **静态可见性说明**：明文 classes.dex 仅含壳 Application（com.tlraljjy.uvsrucinvtsb.Fezxfaprhxzidvoe），真实业务类（Activity/无障碍服务/Receiver）全部位于 assets 下经 XOR/Base64 字符串解密的加密 DEX 载荷中，由 attachBaseContext 通过自定义 ClassLoader 动态装载并用反射实例化真实 Application；因此无障碍引导页的 HTML/文案资源完全静态可见（assets/www/index.html、res/xml/accessibilityservice.xml、strings.xml），但 JS Bridge、startActivity(ACTION_ACCESSIBILITY_SETTINGS) 跳转、拒权后 onResume 重跳、获权后动作等编排逻辑无法静态还原，需运行期观测
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `04cb1225b4a5a0c256234a9b027408994c45911041766fe0b7e691c44a29389d` |
| 包名 / 年份 | `monger.discard.wheneer52` / 2025 |
| 家族 / 品类 | **TrickMo**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google Play Services |
| 引导页宣称品牌/身份 | Google Play Services（Google 官方后台系统组件） |
| 系统无障碍列表服务名 | Google Play Services（@string/accessibility_service_name） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务伪造 isAccessibilityTool=true 冒充『无障碍工具』；服务 android:description 用『优化隐私设置/同步个人数据/提升定位精度/省电』的系统级措辞掩盖 typeAllMask 读屏、canPerformGestures 模拟点击、canTakeScreenshot 截屏能力；HTML 内 app_title 硬编码 'Google Play Services' 并复用官方 GMS 提示语（'%1$s won't work unless you enable Google Play services.'）；启动类全部 excludeFromRecents+noHistory 且 launchMode=singleInstance、taskAffinity 置空以减少残留痕迹；无障碍服务与通知监听服务 exported=false 但通过加密载荷编排；HTML 内含 #wrap 半透明黑遮罩与 #window 伪造系统弹窗，并针对小米/三星定制菜单名以避免用户找不到入口 |
| 无障碍服务类名 | `monger.discard.wheneer52.wF3Ecy` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, RECORD_AUDIO` |
| 系统设置项说明 (`android:description`) | This background system module ensures your device runs smoothly by handling important tasks like login support, syncing personal data, optimizing privacy settings, and improving location accuracy while saving battery. It also boosts the performance of various apps, enabling quicker responses, better interactive content, and more reliable offline features. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | monger.discard.wheneer52.wKjSMJm（exported=true，excludeFromRecents=true，noHistory=true，label=@string/activity_name，icon=@mipmap/ic_launcher） | 用户点击桌面图标启动；类本体位于加密 DEX，由壳 Fezxfaprhxzidvoe.attachBaseContext 反射装载 | 不可静态还原 | **原文**：Google Play Services<br>**译注**：Google Play 服务（桌面图标名与启动页标题） | 用户点击应用图标打开应用，无取消/跳过选项 | `AndroidManifest.xml <activity android:name="monger.discard.wheneer52.wKjSMJm">；壳入口 com.tlraljjy.uvsrucinvtsb.Fezxfaprhxzidvoe.attachBaseContext` |
| 2 | 引导说明页 | WebView 加载本地页 file:///android_asset/www/index.html（宿主 Activity 位于加密载荷） | 启动后由加密载荷中的 Activity 创建 WebView 并 loadUrl 本地 HTML；页面先显示 #spinner-container 白色全屏转圈，隐藏 #main-content，模拟『系统服务自检中』 | 本地HTML WebView | **原文**：Activate <span style="color:#0B57CF;">Accessibility services</span> for the correct application work.<br>**译注**：请启用无障碍服务，以保证应用正常运行。 | 阅读说明；页面无『取消』『跳过』按钮，仅有继续按钮 | `assets/www/index.html#L59（foAccess，default/en 分支）` |
| 3 | 引导说明页 | 同一 WebView 内的分步教学列表（step_1 / step_2 / step_2_xiaomi / step_2_samsung / step_3） | 文案随 navigator.language 前两位切换 es/fr/de/en，并按 %IS_XIAOMI% / %IS_SAMSUNG% 选择『已下载的应用』『已下载的服务』『已安装的应用』菜单名 | 本地HTML WebView | **原文**：Step 1. - Go to Settings / Step 2. - Open "Downloaded Services" / Step 3. - Activate services for the <a>Google Play Services</a><br>**译注**：第 1 步 - 进入设置；第 2 步 - 打开『已下载的服务』；第 3 步 - 为『Google Play Services』启用服务 | 按三步指引自行到系统设置手动开启该服务；无跳过入口 | `assets/www/index.html#L60-L64（default/en），#L29-L33（es），#L40-L44（fr），#L50-L54（de）` |
| 4 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（列表项显示 label=Google Play Services） | 点击 HTML 底部按钮 btn1（id 与 onclick 在 index.html 后半段的表单区，实际点击经 JS Bridge 回调原生 startActivity）；桥接与 Intent 构造代码位于加密 DEX，静态不可见 | 系统无障碍页 | **原文**：Go to Settings<br>**译注**：前往设置 | 点击按钮跳转系统无障碍设置，然后在列表中手动打开『Google Play Services』开关（系统会弹出『此服务可查看屏幕内容、模拟点击』警告，应用侧不提供任何解释或劝阻） | `assets/www/index.html#L65（btn1='Go to Settings'）；Intent 构造点位于加密载荷，明文 dex 中无 ACTION_ACCESSIBILITY_SETTINGS 字符串` |
| 5 | 遮罩叠层指引 | index.html 内 #wrap（position:fixed 全屏、background rgba(1,1,1,0.725)、z-index:100）与 #window（白色卡片、红色描边、header2 + text + 单个『Dalej』按钮） | 页面事件驱动 show/hide（hideAll() 等内联函数），在引导与设置往返期间叠加半透明遮罩与仿系统提示卡片 | 本地HTML WebView | **原文**：Identyfikator / Identyfikator powinno zawierać: od 6 do 16 znaków. / Dalej<br>**译注**：标识符 / 标识符应包含 6 至 16 个字符。/ 下一步（波兰语） | 点击『Dalej』关闭遮罩；该卡片只有一个确认按钮，无取消路径 | `assets/www/index.html#L383-L402（#window/#wrap），#L194-L206（#wrap 样式），#L381（#black_lay）` |
| 6 | 获权后动作 | monger.discard.wheneer52.wF3Ecy（BIND_ACCESSIBILITY_SERVICE，exported=false）+ 通知监听服务 FlD_es5loUXSIYaLs42 + 前台服务 Q9NSNrJMVUUwVHwbs / PushService | 系统绑定无障碍服务后 onServiceConnected（实现位于加密载荷），随后凭 typeAllMask 读屏、canPerformGestures 模拟点击、canTakeScreenshot 截屏；同时 inject.js 在命中 smartclickhub 页面后 1s/5s 两次请求忽略电池优化以保活 | 系统无障碍页 | **原文**：This background system module ensures your device runs smoothly by handling important tasks like login support, syncing personal data, optimizing privacy settings, and improving location accuracy while saving battery.<br>**译注**：此后台系统模块通过处理登录支持、同步个人数据、优化隐私设置、提升定位精度并节省电量等任务，确保您的设备运行顺畅。 | 获权后无需用户再操作，服务静默获得读屏/点击/截屏能力 | `res/xml/accessibilityservice.xml#L1-L3（isAccessibilityTool=true、typeAllMask、canPerformGestures、canTakeScreenshot）；assets/www/inject.js#L1-L10（requestIgnoreBatteryOptimizations）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets/www/index.html 本地 WebView 引导页正文：foAccess（无障碍服务启用说明）+ step_1/step_2/step_3 分步教学 + btn1 跳转按钮（多语言 es/fr/de/en 由 navigator.language 切换）
- assets/www/index.html 的 #wrap 全屏半透明遮罩（rgba(1,1,1,0.725)）与 #window 仿系统弹窗卡片（波兰语 Identyfikator 文案 + 『Dalej』按钮）
- assets/www/index.html 的 #spinner-container 全屏白色加载转圈，先于 #main-content 显示，制造『系统自检中』氛围
- 系统设置→无障碍→已下载的服务列表项：服务名 @string/accessibility_service_name = 『Google Play Services』
- 系统无障碍详情页描述：@string/accessibility_service_description（『This background system module ensures your device runs smoothly by handling important tasks like login support, syncing personal data, optimizing privacy settings, and improving location accuracy while saving battery...』）
- 应用桌面图标与启动页标题：@string/application_name / @string/activity_name = 『Google Play Services』，图标 @mipmap/ic_launcher
- strings.xml 内嵌的 GMS 官方提示语（『%1$s won't work unless you enable Google Play services.』『Enable Google Play services』『Google Play services error』等）用于强化 Google 官方身份错觉

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Activate Accessibility services for the correct application work. | 请启用无障碍服务，以保证应用正常运行。 | `assets/www/index.html#L59（foAccess，default 分支）` | 故障恐吓 |
| en | Step 1. - Go to Settings | 第 1 步 - 进入设置 | `assets/www/index.html#L60（step_1）` | 受限设置分步教学 |
| en | Step 2. - Open "Downloaded Services" | 第 2 步 - 打开『已下载的服务』 | `assets/www/index.html#L61（step_2，另 L62 xiaomi『Downloaded apps』/L63 samsung『Installed apps』）` | 受限设置分步教学 |
| en | Step 3. - Activate services for the <a>Google Play Services</a> | 第 3 步 - 为『Google Play Services』启用服务 | `assets/www/index.html#L64（step_3，app_title 硬编码于 L14）` | 受限设置分步教学 |
| en | Go to Settings | 前往设置 | `assets/www/index.html#L65（btn1）` | 受限设置分步教学 |
| es | Activar los servicios de accesibilidad para el correcto funcionamiento de la aplicación. | 请启用无障碍服务，以保证应用正常运行。 | `assets/www/index.html#L28（foAccess，es 分支）` | 故障恐吓 |
| fr | Activez les services d'accessibilité pour les travaux d'application corrects. | 请启用无障碍服务，以保证应用正常工作。 | `assets/www/index.html#L39（foAccess，fr 分支）` | 故障恐吓 |
| de | Aktivieren Sie Barrierefreiberdienste für die richtige Anwendungsarbeit. | 请启用无障碍服务，以保证应用正常工作。 | `assets/www/index.html#L49（foAccess，de 分支）` | 故障恐吓 |
| pl | Identyfikator powinno zawierać: od 6 do 16 znaków. | 标识符应包含 6 至 16 个字符。 | `assets/www/index.html#L385-L390（#window 弹窗，按钮『Dalej』L394）` | 假更新 |
| en | This background system module ensures your device runs smoothly by handling important tasks like login support, syncing personal data, optimizing privacy settings, and improving location accuracy while saving battery. It also boosts the performance of various apps, enabling quicker responses, better interactive content, and more reliable offline features. | 此后台系统模块通过处理登录支持、同步个人数据、优化隐私设置、提升定位精度并节省电量等任务，确保您的设备运行顺畅。它还能提升各类应用的性能，带来更快的响应、更好的交互内容和更可靠的离线功能。 | `res/values/strings.xml → accessibility_service_description（res/xml/accessibilityservice.xml 引用）` | 清理工具伪装 |
| en | %1$s won't work unless you enable Google Play services. | 除非您启用 Google Play 服务，否则 %1$s 将无法运行。 | `res/values/strings.xml（复用 GMS 官方提示语，强化品牌身份）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：HTML 引导页仅有『Go to Settings』单一按钮，无跳过/取消；从系统设置返回后的行为由加密 DEX 中的宿主 Activity（excludeFromRecents+noHistory，Activity 被销毁重建）决定，明文 dex 中无 onResume 判定逻辑可静态确认，推测为重新拉起同一引导页形成循环，需运行期 UTG 观测确认
- **遮罩叠层 / 高仿系统设置页**：是：本地 HTML 内叠加 #wrap 全屏半透明黑遮罩（rgba(1,1,1,0.725)，z-index:100）+ #window 仿系统提示卡片（红描边、单确认按钮），并以 #spinner-container 全屏白色加载页掩盖真实内容，营造系统级组件假象
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=31，引导路径只教用户进设置→已下载的服务→启用该服务，未见 Android 13+『应用详情右上角菜单允许受限设置』或 Session 安装器绕过文案
- **获权后即时行为与防撤权机制**：明文资源中未见自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权逻辑（无障碍服务实现位于加密载荷，未能静态确认；服务声明 canPerformGestures=true 具备实施该行为的底层能力）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后 WebView 出现本地页面 file:///android_asset/www/index.html（特征：白色 spinner 转圈后出现『Activate Accessibility services』文案与『Go to Settings』按钮）；以及随后监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：真实编排逻辑（JS Bridge、startActivity、onResume 重跳、获权后动作）全部位于 assets 下加密 DEX 载荷，静态不可还原，只能靠运行期 UTG 观测；壳 Application 在 attachBaseContext 中用 System.currentTimeMillis()%2 做无意义分支并输出『Loader / Junk check passed』日志，可用于运行期快速识别；另存在 smartclickhub 页面注入的 requestIgnoreBatteryOptimizations 二次保活弹窗，属易被忽略的次要诱导点

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（本地 HTML WebView）** | WebView 承载 file:///android_asset/www/index.html，页面含文本『Activate Accessibility services for the correct application work.』与按钮『Go to Settings』 | 该页是整个诱导链的起点与唯一用户可见界面，其『启用无障碍以保证应用运行』的措辞可直接判定为功能胁迫式诱导 | 按钮文案 Go to Settings / 多语言 foAccess 文本；页面无取消或跳过按钮的控件树结构；WebView 内 #spinner-container / #wrap 遮罩节点的可见性 |
| **系统无障碍服务列表项（设置页）** | Settings → 无障碍 → 已下载的服务，列表项 label 为『Google Play Services』，description 为『This background system module ensures your device runs smoothly...』 | 直接证明服务名与描述对系统官方品牌的冒用，以及 isAccessibilityTool=true 导致的『无障碍工具』式弱警告呈现 | 列表项文本 Google Play Services 与包名 monger.discard.wheneer52 的错配；服务详情页描述文本是否为系统优化措辞；系统警告弹窗是否被弱化为工具类提示 |
| **设置页返回后的压栈遮罩页** | WebView 重新出现并显示 #wrap 半透明黑遮罩 + #window 红框卡片（Identyfikator / Dalej） | 验证拒权/未启用后是否循环重跳，是判定『无跳过强制诱导』的关键运行证据 | 返回设置后 1-3 秒内是否再次出现同一引导页；遮罩层 z-index/透明度特征节点；页面点击区域是否仅剩单一确认按钮 |
| **获权后界面（验证是否降级或直接进入静默态）** | 无障碍开关打开后 Activity 是否 finish 且不再显示任何界面，同时出现忽略电池优化系统弹窗 | 区分『获权即静默』的恶意形态与良性降级路径，并捕捉 inject.js 触发的电池优化绕过弹窗 | 电池优化豁免请求弹窗（应用名 Google Play Services）；应用界面是否消失并转入后台服务；通知监听服务是否随之激活 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.tlraljjy.uvsrucinvtsb.Fezxfaprhxzidvoe.attachBaseContext（解密 assets 载荷并动态装载真实 Application）`
- `assets/www/index.html#L59-L65（无障碍引导文案 foAccess/step_1~3/btn1，多语言分支 L27-L66）`
- `assets/www/index.html#L376-L402（spinner 加载页、#black_lay、#wrap 遮罩与 #window 仿系统弹窗）`
- `res/xml/accessibilityservice.xml#L1-L3（isAccessibilityTool=true、typeAllMask、canPerformGestures、canTakeScreenshot）`
- `assets/www/inject.js#L1-L10（smartclickhub 页面 1s/5s 两次 requestIgnoreBatteryOptimizations）`
- `AndroidManifest.xml 无障碍服务 monger.discard.wheneer52.wF3Ecy（label=@string/accessibility_service_name，description=@string/accessibility_service_description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（14 次工具调用，按约束停止）。核心事实如下：

**1. 真正的业务代码不在明文 DEX 中，而位于加密资产里。**
`classes.dex` 只有一个包 `com.tlraljjy.uvsrucinvtsb`，其中仅有 Application 类 [attachBaseContext()](<resource-unit:#1.dex1 code:com.tlraljjy.uvsrucinvtsb.Fezxfaprhxzidvoe#attachBaseContext>)。该类通过 `zawslaozq(...)`（XOR 或 Base64 混淆字符串）解密出 `assets/` 下的多个条目，再交给 `jyvcorrjsxgi(ClassLoader, List<File>)` 动态装载；随后用 `Class.forName(mRealApp)` 反射实例化真实的 Application。因此，Manifest 中声明的 Activity、无障碍服务和 Receiver 类（`wKjSMJm`、`wF3Ecy`、`h76v` 等）**都不在明文 dex 中**，全部分布在加密载荷内。

**2. 无障碍引导页完全明文可见，是 TrickMo 经典的“无障碍服务分步教学”HTML。**
[assets/www/index.html (L59-L65)](<resource-unit:#1 file:assets/www/index.html#L59-L65>) 定义了 `foAccess`、`step_1~3`、`btn1` 等文案；`app_title` 被硬编码为 `Google Play Services`（L14），并针对小米、三星分别给出不同的菜单名（L22-L23、L61-L63）。页面使用 `#spinner-container` 白屏加载动画和 `#wrap` 半透明黑色遮罩（`rgba(1,1,1,0.725)`，z-index 100），并配有 `#window` 弹窗；整体呈现为“系统服务加载中”或“故障提示”式的外观。

**3. 系统无障碍列表中的条目伪装成 Google 官方组件。**
[accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml#L1-L3>) 声明了 `isAccessibilityTool="true"`（伪造“无障碍工具”身份）、`typeAllMask`、`canPerformGestures`、`canTakeScreenshot`、`canRequestFilterKeyEvents`；服务的 `android:label` 使用 `@string/accessibility_service_name`，`android:description` 则是一段“优化隐私设置、同步个人数据、提升定位精度、省电”的系统级措辞。整个配置完全不提示其实际具备读屏、模拟点击和截屏能力。

**4. 另有静默的持久化诱导。**
[assets/www/inject.js (L1-L10)](<resource-unit:#1 file:assets/www/inject.js#L1-L10>) 在 `DOMContentLoaded` 后，如果页面 URL 命中 `smartclickhub`，就会在 1 秒和 5 秒时各调用一次 `android.requestIgnoreBatteryOptimizations()`，以绕过电池优化、保活后台。

**5. 跳转代码本身无法静态还原。**
明文 dex 中不存在 `ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`DexClassLoader` 等任何字符串或调用点；点击 HTML 按钮后的 JS Bridge、`startActivity` 跳转、`onResume` 拒权重跳等逻辑都在加密载荷里，因此静态分析不可达。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "明文 classes.dex 仅含壳 Application（com.tlraljjy.uvsrucinvtsb.Fezxfaprhxzidvoe），真实业务类（Activity/无障碍服务/Receiver）全部位于 assets 下经 XOR/Base64 字符串解密的加密 DEX 载荷中，由 attachBaseContext 通过自定义 ClassLoader 动态装载并用反射实例化真实 Application；因此无障碍引导页的 HTML/文案资源完全静态可见（assets/www/index.html、res/xml/accessibilityservice.xml、strings.xml），但 JS Bridge、startActivity(ACTION_ACCESSIBILITY_SETTINGS) 跳转、拒权后 onResume 重跳、获权后动作等编排逻辑无法静态还原，需运行期观测",
  "summary_one_liner": "壳 Application 动态装载加密 DEX，再以本地 HTML 白屏加载页把自身伪装成 Google Play Services，用『开启无障碍服务以保证应用正常运行』的分步教学（设置→已下载服务→启用）诱导用户手动打开 typeAllMask+canPerformGestures+canTakeScreenshot 且伪造 isAccessibilityTool=true 的无障碍服务",
  "disguise_identity": {
    "app_display_name": "Google Play Services",
    "claimed_brand_or_persona": "Google Play Services（Google 官方后台系统组件）",
    "a11y_service_label": "Google Play Services（@string/accessibility_service_name）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务伪造 isAccessibilityTool=true 冒充『无障碍工具』；服务 android:description 用『优化隐私设置/同步个人数据/提升定位精度/省电』的系统级措辞掩盖 typeAllMask 读屏、canPerformGestures 模拟点击、canTakeScreenshot 截屏能力；HTML 内 app_title 硬编码 'Google Play Services' 并复用官方 GMS 提示语（'%1$s won't work unless you enable Google Play services.'）；启动类全部 excludeFromRecents+noHistory 且 launchMode=singleInstance、taskAffinity 置空以减少残留痕迹；无障碍服务与通知监听服务 exported=false 但通过加密载荷编排；HTML 内含 #wrap 半透明黑遮罩与 #window 伪造系统弹窗，并针对小米/三星定制菜单名以避免用户找不到入口"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "monger.discard.wheneer52.wKjSMJm（exported=true，excludeFromRecents=true，noHistory=true，label=@string/activity_name，icon=@mipmap/ic_launcher）",
      "trigger_event": "用户点击桌面图标启动；类本体位于加密 DEX，由壳 Fezxfaprhxzidvoe.attachBaseContext 反射装载",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Google Play Services",
      "shown_text_zh": "Google Play 服务（桌面图标名与启动页标题）",
      "user_action_requested": "用户点击应用图标打开应用，无取消/跳过选项",
      "code_anchor": "AndroidManifest.xml <activity android:name=\"monger.discard.wheneer52.wKjSMJm\">；壳入口 com.tlraljjy.uvsrucinvtsb.Fezxfaprhxzidvoe.attachBaseContext"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "WebView 加载本地页 file:///android_asset/www/index.html（宿主 Activity 位于加密载荷）",
      "trigger_event": "启动后由加密载荷中的 Activity 创建 WebView 并 loadUrl 本地 HTML；页面先显示 #spinner-container 白色全屏转圈，隐藏 #main-content，模拟『系统服务自检中』",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Activate <span style=\"color:#0B57CF;\">Accessibility services</span> for the correct application work.",
      "shown_text_zh": "请启用无障碍服务，以保证应用正常运行。",
      "user_action_requested": "阅读说明；页面无『取消』『跳过』按钮，仅有继续按钮",
      "code_anchor": "assets/www/index.html#L59（foAccess，default/en 分支）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "同一 WebView 内的分步教学列表（step_1 / step_2 / step_2_xiaomi / step_2_samsung / step_3）",
      "trigger_event": "文案随 navigator.language 前两位切换 es/fr/de/en，并按 %IS_XIAOMI% / %IS_SAMSUNG% 选择『已下载的应用』『已下载的服务』『已安装的应用』菜单名",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Step 1. - Go to Settings / Step 2. - Open \"Downloaded Services\" / Step 3. - Activate services for the <a>Google Play Services</a>",
      "shown_text_zh": "第 1 步 - 进入设置；第 2 步 - 打开『已下载的服务』；第 3 步 - 为『Google Play Services』启用服务",
      "user_action_requested": "按三步指引自行到系统设置手动开启该服务；无跳过入口",
      "code_anchor": "assets/www/index.html#L60-L64（default/en），#L29-L33（es），#L40-L44（fr），#L50-L54（de）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（列表项显示 label=Google Play Services）",
      "trigger_event": "点击 HTML 底部按钮 btn1（id 与 onclick 在 index.html 后半段的表单区，实际点击经 JS Bridge 回调原生 startActivity）；桥接与 Intent 构造代码位于加密 DEX，静态不可见",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Go to Settings",
      "shown_text_zh": "前往设置",
      "user_action_requested": "点击按钮跳转系统无障碍设置，然后在列表中手动打开『Google Play Services』开关（系统会弹出『此服务可查看屏幕内容、模拟点击』警告，应用侧不提供任何解释或劝阻）",
      "code_anchor": "assets/www/index.html#L65（btn1='Go to Settings'）；Intent 构造点位于加密载荷，明文 dex 中无 ACTION_ACCESSIBILITY_SETTINGS 字符串"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "index.html 内 #wrap（position:fixed 全屏、background rgba(1,1,1,0.725)、z-index:100）与 #window（白色卡片、红色描边、header2 + text + 单个『Dalej』按钮）",
      "trigger_event": "页面事件驱动 show/hide（hideAll() 等内联函数），在引导与设置往返期间叠加半透明遮罩与仿系统提示卡片",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Identyfikator / Identyfikator powinno zawierać: od 6 do 16 znaków. / Dalej",
      "shown_text_zh": "标识符 / 标识符应包含 6 至 16 个字符。/ 下一步（波兰语）",
      "user_action_requested": "点击『Dalej』关闭遮罩；该卡片只有一个确认按钮，无取消路径",
      "code_anchor": "assets/www/index.html#L383-L402（#window/#wrap），#L194-L206（#wrap 样式），#L381（#black_lay）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "monger.discard.wheneer52.wF3Ecy（BIND_ACCESSIBILITY_SERVICE，exported=false）+ 通知监听服务 FlD_es5loUXSIYaLs42 + 前台服务 Q9NSNrJMVUUwVHwbs / PushService",
      "trigger_event": "系统绑定无障碍服务后 onServiceConnected（实现位于加密载荷），随后凭 typeAllMask 读屏、canPerformGestures 模拟点击、canTakeScreenshot 截屏；同时 inject.js 在命中 smartclickhub 页面后 1s/5s 两次请求忽略电池优化以保活",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "This background system module ensures your device runs smoothly by handling important tasks like login support, syncing personal data, optimizing privacy settings, and improving location accuracy while saving battery.",
      "shown_text_zh": "此后台系统模块通过处理登录支持、同步个人数据、优化隐私设置、提升定位精度并节省电量等任务，确保您的设备运行顺畅。",
      "user_action_requested": "获权后无需用户再操作，服务静默获得读屏/点击/截屏能力",
      "code_anchor": "res/xml/accessibilityservice.xml#L1-L3（isAccessibilityTool=true、typeAllMask、canPerformGestures、canTakeScreenshot）；assets/www/inject.js#L1-L10（requestIgnoreBatteryOptimizations）"
    }
  ],
  "text_presentation_locations": [
    "assets/www/index.html 本地 WebView 引导页正文：foAccess（无障碍服务启用说明）+ step_1/step_2/step_3 分步教学 + btn1 跳转按钮（多语言 es/fr/de/en 由 navigator.language 切换）",
    "assets/www/index.html 的 #wrap 全屏半透明遮罩（rgba(1,1,1,0.725)）与 #window 仿系统弹窗卡片（波兰语 Identyfikator 文案 + 『Dalej』按钮）",
    "assets/www/index.html 的 #spinner-container 全屏白色加载转圈，先于 #main-content 显示，制造『系统自检中』氛围",
    "系统设置→无障碍→已下载的服务列表项：服务名 @string/accessibility_service_name = 『Google Play Services』",
    "系统无障碍详情页描述：@string/accessibility_service_description（『This background system module ensures your device runs smoothly by handling important tasks like login support, syncing personal data, optimizing privacy settings, and improving location accuracy while saving battery...』）",
    "应用桌面图标与启动页标题：@string/application_name / @string/activity_name = 『Google Play Services』，图标 @mipmap/ic_launcher",
    "strings.xml 内嵌的 GMS 官方提示语（『%1$s won't work unless you enable Google Play services.』『Enable Google Play services』『Google Play services error』等）用于强化 Google 官方身份错觉"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Activate Accessibility services for the correct application work.",
      "text_zh": "请启用无障碍服务，以保证应用正常运行。",
      "source_location": "assets/www/index.html#L59（foAccess，default 分支）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. - Go to Settings",
      "text_zh": "第 1 步 - 进入设置",
      "source_location": "assets/www/index.html#L60（step_1）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. - Open \"Downloaded Services\"",
      "text_zh": "第 2 步 - 打开『已下载的服务』",
      "source_location": "assets/www/index.html#L61（step_2，另 L62 xiaomi『Downloaded apps』/L63 samsung『Installed apps』）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 3. - Activate services for the <a>Google Play Services</a>",
      "text_zh": "第 3 步 - 为『Google Play Services』启用服务",
      "source_location": "assets/www/index.html#L64（step_3，app_title 硬编码于 L14）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to Settings",
      "text_zh": "前往设置",
      "source_location": "assets/www/index.html#L65（btn1）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "es",
      "text_verbatim": "Activar los servicios de accesibilidad para el correcto funcionamiento de la aplicación.",
      "text_zh": "请启用无障碍服务，以保证应用正常运行。",
      "source_location": "assets/www/index.html#L28（foAccess，es 分支）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "fr",
      "text_verbatim": "Activez les services d'accessibilité pour les travaux d'application corrects.",
      "text_zh": "请启用无障碍服务，以保证应用正常工作。",
      "source_location": "assets/www/index.html#L39（foAccess，fr 分支）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "de",
      "text_verbatim": "Aktivieren Sie Barrierefreiberdienste für die richtige Anwendungsarbeit.",
      "text_zh": "请启用无障碍服务，以保证应用正常工作。",
      "source_location": "assets/www/index.html#L49（foAccess，de 分支）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pl",
      "text_verbatim": "Identyfikator powinno zawierać: od 6 do 16 znaków.",
      "text_zh": "标识符应包含 6 至 16 个字符。",
      "source_location": "assets/www/index.html#L385-L390（#window 弹窗，按钮『Dalej』L394）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "This background system module ensures your device runs smoothly by handling important tasks like login support, syncing personal data, optimizing privacy settings, and improving location accuracy while saving battery. It also boosts the performance of various apps, enabling quicker responses, better interactive content, and more reliable offline features.",
      "text_zh": "此后台系统模块通过处理登录支持、同步个人数据、优化隐私设置、提升定位精度并节省电量等任务，确保您的设备运行顺畅。它还能提升各类应用的性能，带来更快的响应、更好的交互内容和更可靠的离线功能。",
      "source_location": "res/values/strings.xml → accessibility_service_description（res/xml/accessibilityservice.xml 引用）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "除非您启用 Google Play 服务，否则 %1$s 将无法运行。",
      "source_location": "res/values/strings.xml（复用 GMS 官方提示语，强化品牌身份）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "HTML 引导页仅有『Go to Settings』单一按钮，无跳过/取消；从系统设置返回后的行为由加密 DEX 中的宿主 Activity（excludeFromRecents+noHistory，Activity 被销毁重建）决定，明文 dex 中无 onResume 判定逻辑可静态确认，推测为重新拉起同一引导页形成循环，需运行期 UTG 观测确认",
    "overlay_or_fake_settings": "是：本地 HTML 内叠加 #wrap 全屏半透明黑遮罩（rgba(1,1,1,0.725)，z-index:100）+ #window 仿系统提示卡片（红描边、单确认按钮），并以 #spinner-container 全屏白色加载页掩盖真实内容，营造系统级组件假象",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=31，引导路径只教用户进设置→已下载的服务→启用该服务，未见 Android 13+『应用详情右上角菜单允许受限设置』或 Session 安装器绕过文案",
    "post_grant_anti_removal": "明文资源中未见自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权逻辑（无障碍服务实现位于加密载荷，未能静态确认；服务声明 canPerformGestures=true 具备实施该行为的底层能力）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后 WebView 出现本地页面 file:///android_asset/www/index.html（特征：白色 spinner 转圈后出现『Activate Accessibility services』文案与『Go to Settings』按钮）；以及随后监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（本地 HTML WebView）",
        "page_identifier": "WebView 承载 file:///android_asset/www/index.html，页面含文本『Activate Accessibility services for the correct application work.』与按钮『Go to Settings』",
        "why_most_useful": "该页是整个诱导链的起点与唯一用户可见界面，其『启用无障碍以保证应用运行』的措辞可直接判定为功能胁迫式诱导",
        "observable_utg_signals": ["按钮文案 Go to Settings / 多语言 foAccess 文本", "页面无取消或跳过按钮的控件树结构", "WebView 内 #spinner-container / #wrap 遮罩节点的可见性"]
      },
      {
        "page_role": "系统无障碍服务列表项（设置页）",
        "page_identifier": "Settings → 无障碍 → 已下载的服务，列表项 label 为『Google Play Services』，description 为『This background system module ensures your device runs smoothly...』",
        "why_most_useful": "直接证明服务名与描述对系统官方品牌的冒用，以及 isAccessibilityTool=true 导致的『无障碍工具』式弱警告呈现",
        "observable_utg_signals": ["列表项文本 Google Play Services 与包名 monger.discard.wheneer52 的错配", "服务详情页描述文本是否为系统优化措辞", "系统警告弹窗是否被弱化为工具类提示"]
      },
      {
        "page_role": "设置页返回后的压栈遮罩页",
        "page_identifier": "WebView 重新出现并显示 #wrap 半透明黑遮罩 + #window 红框卡片（Identyfikator / Dalej）",
        "why_most_useful": "验证拒权/未启用后是否循环重跳，是判定『无跳过强制诱导』的关键运行证据",
        "observable_utg_signals": ["返回设置后 1-3 秒内是否再次出现同一引导页", "遮罩层 z-index/透明度特征节点", "页面点击区域是否仅剩单一确认按钮"]
      },
      {
        "page_role": "获权后界面（验证是否降级或直接进入静默态）",
        "page_identifier": "无障碍开关打开后 Activity 是否 finish 且不再显示任何界面，同时出现忽略电池优化系统弹窗",
        "why_most_useful": "区分『获权即静默』的恶意形态与良性降级路径，并捕捉 inject.js 触发的电池优化绕过弹窗",
        "observable_utg_signals": ["电池优化豁免请求弹窗（应用名 Google Play Services）", "应用界面是否消失并转入后台服务", "通知监听服务是否随之激活"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "真实编排逻辑（JS Bridge、startActivity、onResume 重跳、获权后动作）全部位于 assets 下加密 DEX 载荷，静态不可还原，只能靠运行期 UTG 观测；壳 Application 在 attachBaseContext 中用 System.currentTimeMillis()%2 做无意义分支并输出『Loader / Junk check passed』日志，可用于运行期快速识别；另存在 smartclickhub 页面注入的 requestIgnoreBatteryOptimizations 二次保活弹窗，属易被忽略的次要诱导点"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.tlraljjy.uvsrucinvtsb.Fezxfaprhxzidvoe.attachBaseContext（解密 assets 载荷并动态装载真实 Application）",
    "assets/www/index.html#L59-L65（无障碍引导文案 foAccess/step_1~3/btn1，多语言分支 L27-L66）",
    "assets/www/index.html#L376-L402（spinner 加载页、#black_lay、#wrap 遮罩与 #window 仿系统弹窗）",
    "res/xml/accessibilityservice.xml#L1-L3（isAccessibilityTool=true、typeAllMask、canPerformGestures、canTakeScreenshot）",
    "assets/www/inject.js#L1-L10（smartclickhub 页面 1s/5s 两次 requestIgnoreBatteryOptimizations）",
    "AndroidManifest.xml 无障碍服务 monger.discard.wheneer52.wF3Ecy（label=@string/accessibility_service_name，description=@string/accessibility_service_description）"
  ]
}
```

</details>
