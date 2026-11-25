# MB_023__1faeeec490｜BingoMod — Sicurezza Dispositivo

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：157.8s

## 1. 一句话核心结论

- **核心申请方式**：以意大利语安全工具外壳呈现'必须允许全部权限'的单按钮本地HTML引导页，用户点'Prosegui'后被跳至应用详情/无障碍设置，服务连接后由自身无障碍服务读取设置页节点并用dispatchGesture自动点开开关、以GLOBAL_ACTION关闭系统界面。
- **静态可见性说明**：本地 assets/index1.html、indexloading.html、loadingscreen.html 与无障碍配置 XML 均为明文可见，引导文案与按钮流程完整可读；但 DEX 经控制流平坦化+字符串表解密（pabd43f57$pcfbb0ac7$p7c2dd2fd.a(long)），WebView loadUrl 的 URL、JavascriptInterface 名称、跳转 Intent action 均为密文，未能静态还原其真实取值，且不排除运行期切换为远端页面。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1faeeec49012ef73fbe7fabcb325b0b849f64a967c9d0d777c80da9870a34b70` |
| 包名 / 年份 | `p50f9cd20.pe806e63b.pe1a3069b` / 2025 |
| 家族 / 品类 | **BingoMod**（同池样本数：2） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Sicurezza Dispositivo |
| 引导页宣称品牌/身份 | Sicurezza Dispositivo（意大利语'设备安全'，自称为设备安全检测/扫描工具，页面标题伪装为'ANALISI SICUREZZA / Scansione in corso'） |
| 系统无障碍列表服务名 | 无独立服务标签：accessibility_service_description.xml 未声明 android:label 与 android:description，系统列表仅显示应用名 Sicurezza Dispositivo |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置不写 android:description/android:label，使系统列表中无法呈现任何用途说明；HTML 标题写作 'AnroidRAA'（错拼）；主主题名为 Theme.ChromeUpdate 却与浏览器更新无关；三个 exported 透明主题 Activity（p311ed7aa/p925bbf4f/p1d08eb3f）均可独立 MAIN 启动形成多入口；DEX 控制流平坦化+字符串解密；无障碍 XML 伪造 isAccessibilityTool=true 以规避系统'非无障碍工具'警告 |
| 无障碍服务类名 | `p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | 启动 Activity p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60（LAUNCHER，全屏 WebView） | onCreate → setContentView → WebView 配置（setJavaScriptEnabled/addJavascriptInterface/setAllowFileAccess）→ loadUrl(解密字符串) | 本地HTML WebView | **原文**：Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante "Prosegui" in basso per continuare.<br>**译注**：要正确启用本应用，必须允许全部权限。请点击下方"继续"按钮以继续。 | 仅有一个橙色描边按钮 'Prosegui'；页面无取消、无跳过、无返回入口 | `p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60.onCreate + assets/index1.html` |
| 2 | 引导说明页 | WebView 加载的加载/扫描伪装页（indexloading.html、loadingscreen.html） | 引导页跳转或运行期由解密 URL 加载的过渡页 | 本地HTML WebView | **原文**：Aspetta un minuto, stiamo verificando la disponibilità della sicurezza per il tuo dispositivo. / ANALISI SICUREZZA / Scansione in corso... / Ti invitiamo a non interagire in alcun modo con il dispositivo per evitare disconnessioni.<br>**译注**：请稍候一分钟，我们正在核查您设备的安全可用性。/ 安全分析 / 扫描进行中… / 请勿以任何方式操作设备，以免连接中断。 | 不要求操作，反而要求用户'不要操作设备'，为后台自动点击争取时间窗口 | `assets/indexloading.html / assets/loadingscreen.html` |
| 3 | 跳受限设置 | 系统'应用详情'页（Intent 携带 data=package:<包名>，FLAG_ACTIVITY_NEW_TASK） | WebView 按钮 onclick=notifyButtonClick() → Android.onButtonClicked()（@JavascriptInterface） | 系统无障碍页 | **原文**：无（由应用侧构造 Intent 跳转，页面文案来自系统设置）<br>**译注**：跳转至本应用详情页，用于引导用户进入右上角菜单开启'允许受限设置' | 要求用户进入应用详情 → 右上角菜单 → 允许受限设置（Android 13+ 侧载应用开启无障碍的前置条件） | `peb3e8c60$p7234657f.onButtonClicked；p01c5e02b.J（intent.setData(Uri.parse("package:"+getPackageName()))）` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表 → Sicurezza Dispositivo 开关 | 受限设置放行后继续跳转（action 由字符串表解密），或服务 J() 每轮循环重新拉起 | 系统无障碍页 | **原文**：无（系统页面；应用侧未提供 android:description 说明文字）<br>**译注**：系统无障碍列表中仅有应用名，无任何服务用途描述 | 手动打开无障碍服务开关；系统因 isAccessibilityTool=true 不弹出'非无障碍工具'拦截提示 | `p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.J；res/xml/accessibility_service_description.xml` |
| 5 | 遮罩叠层指引 | 无障碍服务内自建隐藏 WebView（this.d）+ WindowManager 悬浮层（字段 A/B/C）+ 透明主题 Activity | onServiceConnected 创建 WebView 与 Handler/Looper.post，启动 $7 线程与多个 Timer | 悬浮窗Overlay | **原文**：无（页面内容由解密 URL 决定，静态未还原）<br>**译注**：获权后在系统设置页之上叠放引导/遮罩层，掩盖真实操作 | 无明确要求，用户在遮罩下继续点击时由服务代操作 | `p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.onServiceConnected（new WebView(this)、WindowManager A/e、Timer i~n）` |
| 6 | 获权后动作 | 无障碍服务自动操作：读取设置页根节点并模拟点击 + dispatchGesture 手势 | p01c5e02b$7.run → J()：startActivity(设置页) → Thread.sleep(2000) → getRootInActiveWindow() → performAction(16) / A(left,top) → dispatchGesture | 悬浮窗Overlay | 无 | 无需用户操作，用户一旦开启服务即被代操作 | `p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.J / A(int,int) / onAccessibilityEvent(performGlobalAction)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets/index1.html：全屏 WebView 引导页，盾牌图 + '必须允许全部权限'+ 唯一 'Prosegui' 按钮（无取消/跳过）
- assets/indexloading.html：'请稍候，正在核查设备安全可用性' + 盾牌图，用于拖延并掩盖后台动作
- assets/loadingscreen.html：'ANALISI SICUREZZA / Scansione in corso…' + 要求用户'不要操作设备'
- res/values/strings.xml:31 app_name = Sicurezza Dispositivo（桌面图标与系统无障碍列表显示名）
- res/xml/accessibility_service_description.xml：仅声明能力与 isAccessibilityTool=true，未提供 android:label / android:description，系统无障碍列表无用途说明
- res/values/strings.xml:40 device_admin_description：'This app requires device administration privileges to perform certain functions.'（设备管理员激活弹窗文案）
- 无障碍服务 onServiceConnected 内自建隐藏 WebView + WindowManager 悬浮层：获权后叠放于系统设置页之上的运行期引导/遮罩

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| it | Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante "Prosegui" in basso per continuare. | 要正确启用本应用，必须允许全部权限。请点击下方"继续"按钮以继续。 | `assets/index1.html（h2.continue-text）` | 教唆忽视警告 |
| it | Aspetta un minuto, stiamo verificando la disponibilità della sicurezza per il tuo dispositivo. | 请稍候一分钟，我们正在核查您设备的安全可用性。 | `assets/indexloading.html（div.loading-text）` | 假反诈安全 |
| it | ANALISI SICUREZZA / Scansione in corso... / Ti invitiamo a non interagire in alcun modo con il dispositivo per evitare disconnessioni. | 安全分析 / 扫描进行中… / 请勿以任何方式操作设备，以免连接中断。 | `assets/loadingscreen.html（h1 / h2 / p）` | 故障恐吓 |
| it | Prosegui | 继续 | `assets/index1.html（button.continue-button，onclick=notifyButtonClick()）` | 教唆忽视警告 |
| en | This app requires device administration privileges to perform certain functions. | 本应用需要设备管理权限以执行某些功能。 | `res/values/strings.xml key=device_admin_description` | 假反诈安全 |
| zh | 不在允许的范围内：%1$s | 不在允许的范围内：%1$s | `res/values-zh-rCN/strings.xml（预筛线索，系统/库异常提示复用）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无障碍服务 J() 在跳设置页后 Thread.sleep(2000) 再读取当前窗口点击，循环内继续迭代节点列表并再次拉起跳转；服务侧 $7 线程与多个 Timer(i~n) 常驻，配合 p1d08eb3f$1 线程在 onActivityResult 后重新 startActivityForResult 媒体投影请求，形成持续重试；未观察到良性安全降级分支
- **遮罩叠层 / 高仿系统设置页**：是：无障碍服务内自建 WebView（this.d）+ WindowManager 悬浮窗字段（A/B/C）+ 三个 exported 透明主题 Activity（p311ed7aa/p925bbf4f/p1d08eb3f）可叠加于系统设置页之上；未发现完整复刻系统无障碍开关控件的高仿页
- **Android 13+ 受限设置（Restricted Settings）应对**：有：J() 构造 data=package:<包名>、FLAG_ACTIVITY_NEW_TASK 的 Intent 跳转应用详情页，对应 Android 13+ 侧载应用先'允许受限设置'再开无障碍的分步教学路径（action 字符串经解密，未逐字还原）
- **获权后即时行为与防撤权机制**：有：服务在 onAccessibilityEvent 及多个子线程中调用 performGlobalAction（BACK/HOME 类全局动作）关闭系统设置界面，并注册设备管理员（BIND_DEVICE_ADMIN + DEVICE_ADMIN_ENABLED），增加撤权与卸载阻力
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 peb3e8c60 后首次 WebView 首帧渲染（出现盾牌图 + 唯一 'Prosegui' 按钮）即拉起；并同步在监测到 startActivity 目标为应用详情/无障碍设置、以及无障碍服务 onServiceConnected 后约 2000ms（J() sleep 结束）这两个时刻补抓，覆盖'跳设置页→自动点击'的关键瞬间。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：盲区一：引导页 URL、JavascriptInterface 名与跳转 action 均由字符串表解密，运行期可能改为远端 HTML，静态无法确认最终页面内容；盲区二：获权后的遮罩/教学页完全由服务内隐藏 WebView 与解密 URL 承载，纯静态不可还原，需运行期捕获；盲区三：p1d08eb3f 启动即申请媒体投影，录屏画面内容不可静态判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（本地 HTML 单按钮）** | 全屏 WebView，盾牌图片 + 文案'必须允许全部权限' + 底部橙色描边 'Prosegui' 按钮，无标题栏/无关闭按钮 | 这是用户被要求授权的唯一决策点，可判定是否构成不可取消的强制引导，并核对文案与真实用途（安全检测 vs 后续代操作）之间的落差 | 页面仅一个可点击控件 'Prosegui'；无取消/跳过/返回控件节点；文案含 'consentire tutti i permessi'（允许全部权限）；标题/包名为 Sicurezza Dispositivo 但无厂商标识 |
| **跳转前/获权后 WebView 教学与遮罩页** | indexloading.html 或 loadingscreen.html 内容：'Scansione in corso...'、'请勿操作设备'；或服务内隐藏 WebView 覆盖在设置页之上 | 识别'假扫描+禁止交互'的时间窗利用手法，以及获权后叠层代操作，区分纯引导与真实代点击 | 出现 'ANALISI SICUREZZA'/'Scansione in corso' 字样；当前 Activity 仍为本应用而背景为系统设置页；同一屏幕同时存在系统开关节点与应用悬浮/WebView 节点 |
| **系统应用详情页（受限设置引导）** | Settings 的应用详情页，标题为 Sicurezza Dispositivo，右上角三点菜单 | 确认是否走 Android 13+ 受限设置绕过路径，这是侧载恶意样本启用无障碍的典型必要步骤 | 当前前台为 com.android.settings 应用详情页；目标包名 p50f9cd20.pe806e63b.pe1a3069b；出现'允许受限设置'菜单项 |
| **系统无障碍服务列表项** | 设置→无障碍→已下载的服务，列表项仅有应用名 Sicurezza Dispositivo，无副标题描述 | 验证 isAccessibilityTool=true 与缺失 android:description 造成的用途不可见，以及是否存在'非无障碍工具'系统警告被规避 | 列表项描述文字为空；无系统'此服务非无障碍工具'警示弹窗；开关被应用自身手势点开（点击来源非用户触摸） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60.onCreate（WebView 引导页 + addJavascriptInterface + loadUrl 解密 URL）`
- `p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60$p7234657f.onButtonClicked（'Prosegui' → startActivity 跳设置）`
- `p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.onServiceConnected（获权后建隐藏 WebView/悬浮层/线程与 Timer）`
- `p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.J（跳设置 → sleep(2000) → 读根节点 → performAction(16)）`
- `p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.A(int,int)（dispatchGesture 模拟点击坐标）`
- `res/xml/accessibility_service_description.xml（isAccessibilityTool=true、canTakeScreenshot、无 label/description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（BingoMod 样本，包名 `p50f9cd20.pe806e63b.pe1a3069b`）

**1. 身份与伪装**
- 桌面名为 `Sicurezza Dispositivo`（意大利语“设备安全”），主题为 `Theme.ChromeUpdate`，但没有任何真实厂商信息；无障碍配置声明 `isAccessibilityTool="true"`，却**不设置 `android:description` 和 `android:label`**，因此系统无障碍列表中不会出现任何用途说明，用户只能看到应用名。
- 无障碍能力范围达到最高级别：`typeAllMask`、`flagRetrieveInteractiveWindows`、`canRetrieveWindowContent`、`canPerformGestures`、`canTakeScreenshot`。

**2. 引导链（运行期页面流转）**
- 冷启动入口 [peb3e8c60.onCreate](<resource-unit:#1.dex1 code:p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60#onCreate>) 创建一个全屏 WebView，开启 `setJavaScriptEnabled`、`addJavascriptInterface`、`setAllowFileAccess`，加载经过字符串解密还原的 URL；本地配套页面为 [assets/index1.html](<resource-unit:#1 file:assets/index1.html>)，其中只有盾牌图和一个 **“Prosegui”（继续）按钮**，文案要求“必须允许全部权限”，没有取消或跳过按钮。
- 另外还有两张欺骗性页面：[assets/indexloading.html](<resource-unit:#1 file:assets/indexloading.html>)（“请稍候，正在核查设备安全可用性”）与 [assets/loadingscreen.html](<resource-unit:#1 file:assets/loadingscreen.html>)（“ANALISI SICUREZZA / 扫描中…/ 请勿以任何方式操作设备，以免断开连接”）。后者一边营造“正在扫描”的假象，一边要求用户不要操作设备，实际是在为后台自动点击争取时间。
- 点击“Prosegui”后，[onButtonClicked](<resource-unit:#1.dex1 code:p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60$p7234657f#onButtonClicked>) 会用解密出的 action 字符串执行 `startActivity`；应用内另有透明主题 Activity `p311ed7aa`、`p925bbf4f`、`p1d08eb3f`，其中 [p1d08eb3f.onCreate](<resource-unit:#1.dex1 code:p50f9cd20.pe806e63b.pe1a3069b.p1d08eb3f#onCreate>) 会立即申请媒体投影（`createScreenCaptureIntent`，requestCode 69），用于录屏。

**3. 获取权限后自动代用户操作（关键点）**
- 无障碍服务一旦连接，[onServiceConnected](<resource-unit:#1.dex1 code:p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b#onServiceConnected>) 会创建隐藏 WebView，并启动 `$7` 线程调用 [J()](<resource-unit:#1.dex1 code:p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b#J>)：先 `startActivity` 跳到设置页（`setData("package:"+包名)` + `FLAG_ACTIVITY_NEW_TASK`，与 `ACTION_APPLICATION_DETAILS_SETTINGS` 的受限设置引导结构一致），再 `Thread.sleep(2000)` 取 `getRootInActiveWindow()`，对节点执行 `performAction(16)` 点击，并按 `getBoundsInScreen` 调用 [A(x,y)](<resource-unit:#1.dex1 code:p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b#A>) → `dispatchGesture` 模拟点击。
- 类中还大量使用 `performGlobalAction`（BACK/HOME 类全局动作）关闭系统界面，形成“跳设置页 + 自动点开关 + 关掉系统 UI”的闭环；同时配备 `READ_SMS/RECEIVE_SMS/SEND_SMS`（SMS_DELIVER 优先级最高）、设备管理员、`QUERY_ALL_PACKAGES`、`WRITE_SETTINGS`、忽略电池优化。

**4. 静态可见性边界**
DEX 采用控制流平坦化加字符串解密（`pabd43f57$pcfbb0ac7$p7c2dd2fd.a(long)` 查表），跳转 action 与 WebView URL 均以密文出现；本地 HTML 明文可读，因此整条引导链机制清晰，但部分字符串与远端页面内容未静态还原。

已登记风险：R-001（high / malware_trojan）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "本地 assets/index1.html、indexloading.html、loadingscreen.html 与无障碍配置 XML 均为明文可见，引导文案与按钮流程完整可读；但 DEX 经控制流平坦化+字符串表解密（pabd43f57$pcfbb0ac7$p7c2dd2fd.a(long)），WebView loadUrl 的 URL、JavascriptInterface 名称、跳转 Intent action 均为密文，未能静态还原其真实取值，且不排除运行期切换为远端页面。",
  "summary_one_liner": "以意大利语安全工具外壳呈现'必须允许全部权限'的单按钮本地HTML引导页，用户点'Prosegui'后被跳至应用详情/无障碍设置，服务连接后由自身无障碍服务读取设置页节点并用dispatchGesture自动点开开关、以GLOBAL_ACTION关闭系统界面。",
  "disguise_identity": {
    "app_display_name": "Sicurezza Dispositivo",
    "claimed_brand_or_persona": "Sicurezza Dispositivo（意大利语'设备安全'，自称为设备安全检测/扫描工具，页面标题伪装为'ANALISI SICUREZZA / Scansione in corso'）",
    "a11y_service_label": "无独立服务标签：accessibility_service_description.xml 未声明 android:label 与 android:description，系统列表仅显示应用名 Sicurezza Dispositivo",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置不写 android:description/android:label，使系统列表中无法呈现任何用途说明；HTML 标题写作 'AnroidRAA'（错拼）；主主题名为 Theme.ChromeUpdate 却与浏览器更新无关；三个 exported 透明主题 Activity（p311ed7aa/p925bbf4f/p1d08eb3f）均可独立 MAIN 启动形成多入口；DEX 控制流平坦化+字符串解密；无障碍 XML 伪造 isAccessibilityTool=true 以规避系统'非无障碍工具'警告"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "启动 Activity p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60（LAUNCHER，全屏 WebView）",
      "trigger_event": "onCreate → setContentView → WebView 配置（setJavaScriptEnabled/addJavascriptInterface/setAllowFileAccess）→ loadUrl(解密字符串)",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante \"Prosegui\" in basso per continuare.",
      "shown_text_zh": "要正确启用本应用，必须允许全部权限。请点击下方\"继续\"按钮以继续。",
      "user_action_requested": "仅有一个橙色描边按钮 'Prosegui'；页面无取消、无跳过、无返回入口",
      "code_anchor": "p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60.onCreate + assets/index1.html"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "WebView 加载的加载/扫描伪装页（indexloading.html、loadingscreen.html）",
      "trigger_event": "引导页跳转或运行期由解密 URL 加载的过渡页",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Aspetta un minuto, stiamo verificando la disponibilità della sicurezza per il tuo dispositivo. / ANALISI SICUREZZA / Scansione in corso... / Ti invitiamo a non interagire in alcun modo con il dispositivo per evitare disconnessioni.",
      "shown_text_zh": "请稍候一分钟，我们正在核查您设备的安全可用性。/ 安全分析 / 扫描进行中… / 请勿以任何方式操作设备，以免连接中断。",
      "user_action_requested": "不要求操作，反而要求用户'不要操作设备'，为后台自动点击争取时间窗口",
      "code_anchor": "assets/indexloading.html / assets/loadingscreen.html"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统'应用详情'页（Intent 携带 data=package:<包名>，FLAG_ACTIVITY_NEW_TASK）",
      "trigger_event": "WebView 按钮 onclick=notifyButtonClick() → Android.onButtonClicked()（@JavascriptInterface）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（由应用侧构造 Intent 跳转，页面文案来自系统设置）",
      "shown_text_zh": "跳转至本应用详情页，用于引导用户进入右上角菜单开启'允许受限设置'",
      "user_action_requested": "要求用户进入应用详情 → 右上角菜单 → 允许受限设置（Android 13+ 侧载应用开启无障碍的前置条件）",
      "code_anchor": "peb3e8c60$p7234657f.onButtonClicked；p01c5e02b.J（intent.setData(Uri.parse(\"package:\"+getPackageName()))）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表 → Sicurezza Dispositivo 开关",
      "trigger_event": "受限设置放行后继续跳转（action 由字符串表解密），或服务 J() 每轮循环重新拉起",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页面；应用侧未提供 android:description 说明文字）",
      "shown_text_zh": "系统无障碍列表中仅有应用名，无任何服务用途描述",
      "user_action_requested": "手动打开无障碍服务开关；系统因 isAccessibilityTool=true 不弹出'非无障碍工具'拦截提示",
      "code_anchor": "p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.J；res/xml/accessibility_service_description.xml"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "无障碍服务内自建隐藏 WebView（this.d）+ WindowManager 悬浮层（字段 A/B/C）+ 透明主题 Activity",
      "trigger_event": "onServiceConnected 创建 WebView 与 Handler/Looper.post，启动 $7 线程与多个 Timer",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（页面内容由解密 URL 决定，静态未还原）",
      "shown_text_zh": "获权后在系统设置页之上叠放引导/遮罩层，掩盖真实操作",
      "user_action_requested": "无明确要求，用户在遮罩下继续点击时由服务代操作",
      "code_anchor": "p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.onServiceConnected（new WebView(this)、WindowManager A/e、Timer i~n）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务自动操作：读取设置页根节点并模拟点击 + dispatchGesture 手势",
      "trigger_event": "p01c5e02b$7.run → J()：startActivity(设置页) → Thread.sleep(2000) → getRootInActiveWindow() → performAction(16) / A(left,top) → dispatchGesture",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务在跳转 2 秒后自动点击设置页上的开关位置，并用手势点击坐标；同时以 performGlobalAction 关闭系统界面，阻止用户干预或撤权",
      "user_action_requested": "无需用户操作，用户一旦开启服务即被代操作",
      "code_anchor": "p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.J / A(int,int) / onAccessibilityEvent(performGlobalAction)"
    }
  ],
  "text_presentation_locations": [
    "assets/index1.html：全屏 WebView 引导页，盾牌图 + '必须允许全部权限'+ 唯一 'Prosegui' 按钮（无取消/跳过）",
    "assets/indexloading.html：'请稍候，正在核查设备安全可用性' + 盾牌图，用于拖延并掩盖后台动作",
    "assets/loadingscreen.html：'ANALISI SICUREZZA / Scansione in corso…' + 要求用户'不要操作设备'",
    "res/values/strings.xml:31 app_name = Sicurezza Dispositivo（桌面图标与系统无障碍列表显示名）",
    "res/xml/accessibility_service_description.xml：仅声明能力与 isAccessibilityTool=true，未提供 android:label / android:description，系统无障碍列表无用途说明",
    "res/values/strings.xml:40 device_admin_description：'This app requires device administration privileges to perform certain functions.'（设备管理员激活弹窗文案）",
    "无障碍服务 onServiceConnected 内自建隐藏 WebView + WindowManager 悬浮层：获权后叠放于系统设置页之上的运行期引导/遮罩"
  ],
  "verbatim_texts": [
    {
      "lang": "it",
      "text_verbatim": "Per abilitare correttamente l'app è necessario consentire tutti i permessi. Clicca sul pulsante \"Prosegui\" in basso per continuare.",
      "text_zh": "要正确启用本应用，必须允许全部权限。请点击下方\"继续\"按钮以继续。",
      "source_location": "assets/index1.html（h2.continue-text）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "it",
      "text_verbatim": "Aspetta un minuto, stiamo verificando la disponibilità della sicurezza per il tuo dispositivo.",
      "text_zh": "请稍候一分钟，我们正在核查您设备的安全可用性。",
      "source_location": "assets/indexloading.html（div.loading-text）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "it",
      "text_verbatim": "ANALISI SICUREZZA / Scansione in corso... / Ti invitiamo a non interagire in alcun modo con il dispositivo per evitare disconnessioni.",
      "text_zh": "安全分析 / 扫描进行中… / 请勿以任何方式操作设备，以免连接中断。",
      "source_location": "assets/loadingscreen.html（h1 / h2 / p）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "it",
      "text_verbatim": "Prosegui",
      "text_zh": "继续",
      "source_location": "assets/index1.html（button.continue-button，onclick=notifyButtonClick()）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "This app requires device administration privileges to perform certain functions.",
      "text_zh": "本应用需要设备管理权限以执行某些功能。",
      "source_location": "res/values/strings.xml key=device_admin_description",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "zh",
      "text_verbatim": "不在允许的范围内：%1$s",
      "text_zh": "不在允许的范围内：%1$s",
      "source_location": "res/values-zh-rCN/strings.xml（预筛线索，系统/库异常提示复用）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无障碍服务 J() 在跳设置页后 Thread.sleep(2000) 再读取当前窗口点击，循环内继续迭代节点列表并再次拉起跳转；服务侧 $7 线程与多个 Timer(i~n) 常驻，配合 p1d08eb3f$1 线程在 onActivityResult 后重新 startActivityForResult 媒体投影请求，形成持续重试；未观察到良性安全降级分支",
    "overlay_or_fake_settings": "是：无障碍服务内自建 WebView（this.d）+ WindowManager 悬浮窗字段（A/B/C）+ 三个 exported 透明主题 Activity（p311ed7aa/p925bbf4f/p1d08eb3f）可叠加于系统设置页之上；未发现完整复刻系统无障碍开关控件的高仿页",
    "restricted_settings_13plus_coaching": "有：J() 构造 data=package:<包名>、FLAG_ACTIVITY_NEW_TASK 的 Intent 跳转应用详情页，对应 Android 13+ 侧载应用先'允许受限设置'再开无障碍的分步教学路径（action 字符串经解密，未逐字还原）",
    "post_grant_anti_removal": "有：服务在 onAccessibilityEvent 及多个子线程中调用 performGlobalAction（BACK/HOME 类全局动作）关闭系统设置界面，并注册设备管理员（BIND_DEVICE_ADMIN + DEVICE_ADMIN_ENABLED），增加撤权与卸载阻力",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 peb3e8c60 后首次 WebView 首帧渲染（出现盾牌图 + 唯一 'Prosegui' 按钮）即拉起；并同步在监测到 startActivity 目标为应用详情/无障碍设置、以及无障碍服务 onServiceConnected 后约 2000ms（J() sleep 结束）这两个时刻补抓，覆盖'跳设置页→自动点击'的关键瞬间。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（本地 HTML 单按钮）",
        "page_identifier": "全屏 WebView，盾牌图片 + 文案'必须允许全部权限' + 底部橙色描边 'Prosegui' 按钮，无标题栏/无关闭按钮",
        "why_most_useful": "这是用户被要求授权的唯一决策点，可判定是否构成不可取消的强制引导，并核对文案与真实用途（安全检测 vs 后续代操作）之间的落差",
        "observable_utg_signals": ["页面仅一个可点击控件 'Prosegui'", "无取消/跳过/返回控件节点", "文案含 'consentire tutti i permessi'（允许全部权限）", "标题/包名为 Sicurezza Dispositivo 但无厂商标识"]
      },
      {
        "page_role": "跳转前/获权后 WebView 教学与遮罩页",
        "page_identifier": "indexloading.html 或 loadingscreen.html 内容：'Scansione in corso...'、'请勿操作设备'；或服务内隐藏 WebView 覆盖在设置页之上",
        "why_most_useful": "识别'假扫描+禁止交互'的时间窗利用手法，以及获权后叠层代操作，区分纯引导与真实代点击",
        "observable_utg_signals": ["出现 'ANALISI SICUREZZA'/'Scansione in corso' 字样", "当前 Activity 仍为本应用而背景为系统设置页", "同一屏幕同时存在系统开关节点与应用悬浮/WebView 节点"]
      },
      {
        "page_role": "系统应用详情页（受限设置引导）",
        "page_identifier": "Settings 的应用详情页，标题为 Sicurezza Dispositivo，右上角三点菜单",
        "why_most_useful": "确认是否走 Android 13+ 受限设置绕过路径，这是侧载恶意样本启用无障碍的典型必要步骤",
        "observable_utg_signals": ["当前前台为 com.android.settings 应用详情页", "目标包名 p50f9cd20.pe806e63b.pe1a3069b", "出现'允许受限设置'菜单项"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已下载的服务，列表项仅有应用名 Sicurezza Dispositivo，无副标题描述",
        "why_most_useful": "验证 isAccessibilityTool=true 与缺失 android:description 造成的用途不可见，以及是否存在'非无障碍工具'系统警告被规避",
        "observable_utg_signals": ["列表项描述文字为空", "无系统'此服务非无障碍工具'警示弹窗", "开关被应用自身手势点开（点击来源非用户触摸）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "盲区一：引导页 URL、JavascriptInterface 名与跳转 action 均由字符串表解密，运行期可能改为远端 HTML，静态无法确认最终页面内容；盲区二：获权后的遮罩/教学页完全由服务内隐藏 WebView 与解密 URL 承载，纯静态不可还原，需运行期捕获；盲区三：p1d08eb3f 启动即申请媒体投影，录屏画面内容不可静态判定。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL"
  ],
  "code_anchors": [
    "p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60.onCreate（WebView 引导页 + addJavascriptInterface + loadUrl 解密 URL）",
    "p50f9cd20.pe806e63b.pe1a3069b.peb3e8c60$p7234657f.onButtonClicked（'Prosegui' → startActivity 跳设置）",
    "p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.onServiceConnected（获权后建隐藏 WebView/悬浮层/线程与 Timer）",
    "p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.J（跳设置 → sleep(2000) → 读根节点 → performAction(16)）",
    "p50f9cd20.pe806e63b.pe1a3069b.p01c5e02b.A(int,int)（dispatchGesture 模拟点击坐标）",
    "res/xml/accessibility_service_description.xml（isAccessibilityTool=true、canTakeScreenshot、无 label/description）"
  ]
}
```

</details>
