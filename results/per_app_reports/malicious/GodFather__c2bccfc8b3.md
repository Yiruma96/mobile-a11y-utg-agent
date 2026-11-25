# MB_097__c2bccfc8b3｜GodFather — Müzik İndir

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：198.5s

## 1. 一句话核心结论

- **核心申请方式**：音乐下载器外壳仅作投放器，用不可取消 AlertDialog 强推安装加密内嵌的第二个 APK，真正的无障碍服务藏在内层空标签应用中，靠云端下发的远端 WebView 页面与 WindowManager 悬浮遮罩完成诱导，服务连接瞬间自按返回键。
- **静态可见性说明**：两层结构均静态可见：外层投放器（Tatarian/Okawville）与内嵌载荷 assets/app.apk（com.opthalmologic.salicylize）已完整解包并反编译，无障碍服务清单、悬浮窗、PackageInstaller 会话逻辑均可还原。不可静态还原部分为：1) 所有 URL、键名、路径与云端配置键均以 AES/CBC + 硬编码密钥 B9M80O2RAK1VRJNV 加密（idololater.prewrapped / Cheston.Mohammedanism），需运行期或脚本解密；2) 实际引导/教学页面为远端 WebView（superfunctional.loadUrl 拼接云端 base + 路径 + 设备号 + 语言），HTML 内容与云控文案（mispoint 的悬浮层文本、cylindricality$19 的 di/gA 键值）完全依赖服务端下发，包内不存在。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c2bccfc8b3bdf2da5fb5c22055a9c4859256be7904933e9e0b92fa31fd0420d3` |
| 包名 / 年份 | `com.parcellize.unmatrimonial` / 2025 |
| 家族 / 品类 | **GodFather**（同池样本数：11） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Müzik İndir |
| 引导页宣称品牌/身份 | 音乐下载器（Music Downloader），并以『插件/eklenti』名义把恶意载荷包装成功能扩展组件 |
| 系统无障碍列表服务名 | Music Downloader（内层 app_name；服务声明 android:label=@string/app_name，应用级 android:label 为空字符串） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：内层 application android:label="" 空标签以在系统界面隐藏名称；无障碍服务借用通用名 Music Downloader 掩盖真实用途；res/values/strings.xml 混入伪造系统 UI 文案 appname="Settings"、allow="İzin Ver"、battery="Düşük Pil"；全部敏感字符串、URL、包名与云端配置键使用 AES/CBC 硬编码密钥加密；类名方法名替换为随机英文词（Okawville/cylindricality/mispoint）；载荷以 assets/app.apk 形式嵌入；外层三个 exported Activity 均无真实业务界面，Okawville 以 singleTask + 自定义 SESSION_API_PACKAGE_INSTALLED 动作承接安装结果。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.parcellize.unmatrimonial.Tatarian（LAUNCHER，singleTask） | onCreate 读取 SharedPreferences "setting" 中的 drop/ok/permission 键，决定跳转 botanics、跳转 Okawville 或展示引导布局 | 原生Activity | **原文**：无（setContentView(2131361820) + Button(2131165277)，文案资源未在 strings.xml 中显式命名）<br>**译注**：一个仅含单个按钮的极简引导页，无功能说明 | 点击页面唯一按钮进入下一步（无跳过/取消入口） | `com.parcellize.unmatrimonial.Tatarian.onCreate；Tatarian$1.onClick` |
| 2 | 业务功能触发 | com.parcellize.unmatrimonial.Okawville（exported，singleTask） | onResume 调用 isAppInstalled("com.opthalmologic.salicylize")，返回 false 时进入 showDialog() | 原生Activity | **原文**：无（该 Activity 仅 setContentView(2131361821)，无可见业务内容）<br>**译注**：空白过渡页面，随即被强制弹窗覆盖 | 无操作，被动进入弹窗 | `com.parcellize.unmatrimonial.Okawville.onResume / isAppInstalled` |
| 3 | 引导说明页 | AlertDialog（Okawville.bulten），标题 @string/information、正文 @string/message、唯一按钮 @string/ok | Okawville.showDialog() 由 onResume 触发；builder.setCancelable(false) 使其无法被返回键或点击外部取消 | 原生Dialog | **原文**：Bilgi / Uygulamamızı kullanabilmek için eklentiyi yüklemelisiniz. / YÜKLE<br>**译注**：「信息」/「要使用我们的应用，您必须安装该插件。」/「安装」 | 只能点击「YÜKLE（安装）」；对话框不可取消，无取消、跳过或关闭按钮，返回键无效 | `com.parcellize.unmatrimonial.Okawville.showDialog；res/values/strings.xml (information/message/ok)` |
| 4 | 拒权反馈循环 | Okawville$1.onClick → PackageInstaller 会话 + onNewIntent 状态分派 | 点击后 Toast 提示并 commit 安装会话；安装回调进入 onNewIntent，按 android.content.pm.extra.STATUS 分支：-1 转发安装器 Intent，0 启动已装插件，7 重新调用 onResume | 通知栏 | **原文**：Eklenti kuruluyor lütfen bekleyiniz.<br>**译注**：「插件正在安装，请稍候。」 | 无显式拒绝路径：用户若在系统安装器上取消（STATUS=7），流程回到 onResume 重新弹出同一个不可取消的「YÜKLE」对话框，形成强制重试循环 | `com.parcellize.unmatrimonial.Okawville$1.onClick；Okawville.onNewIntent；Okawville.addApkToInstallSession` |
| 5 | 获权后动作 | 内层载荷 com.opthalmologic.salicylize.awfullooking → quinanisole | 外层 onResume/onNewIntent 通过 getLaunchIntentForPackage 启动内层并附带 package=宿主包名、packagestp=botanics 类名；内层 onResume 写配置、起后台线程、申请 POST_NOTIFICATIONS（SDK>32 走 Unneapolitan/shouldShowRequestPermissionRationale，否则 shedevil），随后跳 quinanisole | 原生Activity | **原文**：无（内层 strings 中预留 perm="Uygulamanın tüm özelliklerini kullanmak için izin vermeniz gerekiyor."、allow="İzin Ver"）<br>**译注**：「为使用应用的全部功能，您需要授予权限。」/「允许」 | 授予通知等运行时权限；无障碍权限尚未在此步请求 | `com.opthalmologic.salicylize.awfullooking.onResume / Unneapolitan / shedevil；res/values/strings.xml (perm/allow)` |
| 6 | 遮罩叠层指引 | cylindricality.mispoint：WindowManager.addView(FrameLayout + ImageView + layout/mantels)，LayoutParams(type=2032, flags=2008, -3)，alpha 取自云端配置 | 无障碍服务 onAccessibilityEvent 内调用；先校验云端配置键值是否等于预期值，通过后叠加悬浮层，文本由 encyst.prelusively 解密云端下发内容 | 悬浮窗Overlay | **原文**：无（文本来自云端下发，静态不可得；关联资源 layout/mantels、R$id.hoistman、drawable/selfresigned、drawable/sphygmomanometers）<br>**译注**：在系统界面之上叠加的半透明引导层，含提示文字与图标，视觉与文案完全由服务端控制 | 按悬浮层指引继续操作（内容远端下发，静态无法确定） | `com.opthalmologic.salicylize.cylindricality.mispoint；res/layout/mantels` |
| 7 | 跳受限设置 | cylindricality$19.run → superfunctional（远端 WebView 载体） | 无障碍事件回调中解析云端下发的 di/gA 键值对（包名/类名），用 KeyguardManager.isKeyguardLocked() 确认未锁屏且设置开关匹配后，startActivity 拉起 superfunctional 并附 extras | 远端WebView | **原文**：无（loadUrl = 云端 base + 路径 + 参数 + 设备标识 + Locale 语言；页面内容不在包内）<br>**译注**：由服务端按设备号与语言下发的 HTML 引导/教学页面，静态包内不存在对应文本 | 不可静态还原（页面与按钮由远端 HTML 决定） | `com.opthalmologic.salicylize.cylindricality$19.run；com.opthalmologic.salicylize.superfunctional.onStart` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 外层 Okawville.showDialog() 的不可取消 AlertDialog（标题 @string/information、正文 @string/message、正按钮 @string/ok），位于 Okawville Activity 之上
- 外层 Okawville$1.onClick 中的 Toast：@string/click「Eklenti kuruluyor lütfen bekleyiniz.」
- 外层 Tatarian 引导布局 layout 2131361820 + Button 2131165277（文案资源未在 strings.xml 中显式命名）
- 内层无障碍服务 cylindricality.mispoint 通过 WindowManager 叠加的悬浮层（layout/mantels、R$id.hoistman TextView、drawable/selfresigned、drawable/sphygmomanometers），文字由 encyst.prelusively 解密云端内容
- 内层 superfunctional 的远端 WebView 页面（loadUrl 拼接云端 base、路径、设备标识与语言），无本地 assets HTML
- 内层 res/values/strings.xml 中预留但为伪造系统 UI 的文案：appname="Settings"、allow="İzin Ver"、battery="Düşük Pil"、perm="Uygulamanın tüm özelliklerini kullanmak için izin vermeniz gerekiyor."
- 系统无障碍服务列表中显示的服务名：内层 service android:label=@string/app_name → "Music Downloader"（无 android:description 说明文案）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Uygulamamızı kullanabilmek için eklentiyi yüklemelisiniz. | 要使用我们的应用，您必须安装该插件。 | `外层 res/values/strings.xml key=message（Okawville.showDialog setMessage(2131492894)）` | 假更新 |
| tr | Bilgi | 信息 | `外层 res/values/strings.xml key=information（Okawville.showDialog setTitle(2131492893)）` | 假更新 |
| tr | YÜKLE | 安装 | `外层 res/values/strings.xml key=ok（Okawville.showDialog setPositiveButton(2131492895)）` | 假更新 |
| tr | Eklenti kuruluyor lütfen bekleyiniz. | 插件正在安装，请稍候。 | `外层 res/values/strings.xml key=click（Okawville$1.onClick Toast, 2131492892）` | 假更新 |
| tr | Uygulamanın tüm özelliklerini kullanmak için izin vermeniz gerekiyor. | 为使用应用的全部功能，您需要授予权限。 | `内层 res/values/strings.xml key=perm` | 受限设置分步教学 |
| tr | İzin Ver | 允许 | `内层 res/values/strings.xml key=allow` | 受限设置分步教学 |
| en | Settings | 设置 | `内层 res/values/strings.xml key=appname` | 假反诈安全 |
| tr | Düşük Pil | 电量不足 | `内层 res/values/strings.xml key=battery` | 故障恐吓 |
| en | Music Downloader | 音乐下载器 | `内层 res/values/strings.xml key=app_name（无障碍服务 android:label）` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：Okawville.showDialog 设置 setCancelable(false) 且仅提供正按钮，用户无法取消或跳过。用户若在系统安装器取消安装，onNewIntent 收到 STATUS=7 后直接再次调用 onResume，重新走 isAppInstalled 检查并重弹同一个不可取消对话框，形成强制安装循环；STATUS=-1（安装器失败/需人工）则转发安装器 Intent，STATUS=0 才放行启动内层。
- **遮罩叠层 / 高仿系统设置页**：有。cylindricality.mispoint 通过 WindowManager.addView 叠加 FrameLayout(ImageView + layout/mantels) 悬浮层，LayoutParams 为 type=2032、flags=2008、-3，透明度由云端配置键读取后 setAlpha 动态设置；内层 strings 预留 appname="Settings"、allow="İzin Ver"、battery="Düşük Pil" 等伪造系统界面文案，说明存在高仿系统设置/引导页的视觉素材，但具体布局与文字由云端下发，静态不可见。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。应用自身代码中未出现 android.settings.APPLICATION_DETAILS_SETTINGS 或 ACTION_MANAGE_UNKNOWN_APP_SOURCES 跳转（前者仅出现在 GMS 库 com.google.android.gms.common.internal.zzt.zzc），未见教用户进应用详情右上角开启受限设置的文案或分步引导。
- **获权后即时行为与防撤权机制**：部分：cylindricality.onServiceConnected() 在无障碍服务连接成功的瞬间立即调用 performGlobalAction(1)（GLOBAL_ACTION_BACK），把用户从系统无障碍设置页弹回，缩短用户停留在设置页的时间；未发现 GLOBAL_ACTION_HOME、监听设置页并拦截撤权、或伪造 isAccessibilityTool 声明的代码。
- **良性降级 / 替代方案**：无。未提供手动模式、仅观看模式或 ADB 等替代路径；未安装插件时唯一路径是安装内嵌载荷。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到外层进程发起 PackageInstaller 会话提交（commit 携带 action com.example.android.apis.content.SESSION_API_PACKAGE_INSTALLED）或 startActivity 目标切换到 com.opthalmologic.salicylize 时拉起 UTG；进入内层后，以 com.opthalmologic.salicylize.cylindricality（无障碍服务）onServiceConnected 被调用、以及 WindowManager 出现 type=2032 覆盖层（悬浮窗新增）为第二触发点；同时在无障碍服务启用后监测是否有 GLOBAL_ACTION_BACK 全局动作（服务连接瞬间的自动返回）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：主要盲区有三：1) 引导文案与教学页面几乎全部由服务端下发（superfunctional 的远端 WebView、mispoint 的悬浮层文本、cylindricality$19 的 di/gA 键值），包内无本地 HTML，离线或断网时可能整条引导链静默不出现，导致 UTG 抓不到关键页面；2) 悬浮层含 drawable 图片引导（sphygmomanometers、selfresigned），若服务端只下发图片而文字为空，需 OCR 才能读出诱导内容；3) 载荷为两阶段投放，第一阶段（外层）本身不含任何无障碍代码与设置页跳转，若只静态审计外层会完全看不到无障碍能力，必须运行到内层安装完成才可见。此外静态加壳不阻挡运行期 UTG，本样本未加壳，仅对字符串做 AES 加密，不影响页面抓取。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动强制安装弹窗页** | Okawville Activity 之上的 AlertDialog：标题「Bilgi」、正文「Uygulamamızı kullanabilmek için eklentiyi yüklemelisiniz.」、单按钮「YÜKLE」，无取消/关闭控件 | 这是整个诱导链的起点与唯一强制门禁，其不可取消性是判定胁迫程度最直接的证据，也决定后续是否进入载荷安装 | Dialog 节点仅有 1 个 Button 且文本为 YÜKLE；节点树中不存在 negative/cancel 按钮与关闭图标；返回键后对话框仍存在（setCancelable(false)）；当前窗口包名 com.parcellize.unmatrimonial |
| **安装载荷后首次进入内层应用的引导/权限页** | com.opthalmologic.salicylize.awfullooking 及其跳转的 quinanisole，含 POST_NOTIFICATIONS 运行时权限弹窗与后续引导界面 | 确认外层投放与内层恶意载荷之间的接续关系，并捕获内层实际展示的引导文案（该层 label 为空，界面文本是判定伪装身份的关键） | 当前前台包名由 com.parcellize.unmatrimonial 切换为 com.opthalmologic.salicylize；出现系统通知权限授权框；界面中出现 İzin Ver / Settings 等伪造系统文案；应用名称显示为空或 Music Downloader |
| **设置页后压栈遮罩页（悬浮引导层）** | WindowManager 添加的 FrameLayout 覆盖层（type=2032、flags=2008），内含 layout/mantels 的 TextView 与 ImageView，透明度由云端配置控制 | 该层是覆盖在系统界面之上的引导载体，其文本与透明度来自云端下发，UTG 抓取可得到静态无法还原的诱导文案，是区分『良性说明』与『教唆开启无障碍』的决定性证据 | 节点树出现与前台 Activity 不同包名的悬浮窗口层级；悬浮层内 TextView 文本（云端下发）；悬浮层是否遮挡系统无障碍开关控件；悬浮层是否有箭头/手势指引指向无障碍开关 |
| **远端 WebView 教学页** | com.opthalmologic.salicylize.superfunctional 内 new WebView 加载的远端 URL（拼接云端 base + 路径 + 设备标识 + 语言） | 这是应用最主要的引导说明载体，HTML 完全由服务端下发，只有运行期 UTG 才能取得逐字教学文本与分步截图指引 | WebView 节点及其 url 属性（云端域名与路径）；页面内 button/a 文本与分步序号；页面是否出现无障碍设置/应用详情设置的截图或指向箭头；页面语言是否随 Locale 变化 |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载的服务中的 Music Downloader 条目（对应 com.opthalmologic.salicylize.cylindricality） | 确认最终用户被引导开启的正是内层恶意服务，并核对系统列表中呈现的名称与说明（该服务未声明 android:description，说明文案缺失本身即为可疑信号） | 服务条目文本 Music Downloader 与开关状态；是否存在 description 说明文字（预期为空）；开启瞬间页面是否被自动返回键弹回；开启后悬浮层是否立即出现 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.parcellize.unmatrimonial.Okawville.showDialog`
- `com.parcellize.unmatrimonial.Okawville$1.onClick`
- `com.parcellize.unmatrimonial.Okawville.onResume`
- `com.opthalmologic.salicylize.cylindricality.onServiceConnected`
- `com.opthalmologic.salicylize.cylindricality.mispoint`
- `com.opthalmologic.salicylize.superfunctional.onStart`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**结构：两层载荷与无障碍权限的真实归属**
- 外层包 `com.parcellize.unmatrimonial`（显示名 **Müzik İndir**）自身**没有任何无障碍服务**，Manifest 中也没有 `BIND_ACCESSIBILITY_SERVICE`；它是一个**投放器**：`Tatarian`（LAUNCHER）→ `Okawville` → 用 `PackageInstaller` Session 把加密内嵌的 `assets/app.apk` 安装进设备。
- 真正的无障碍服务在内层载荷 `com.opthalmologic.salicylize`（`cylindricality`，`typeAllMask` + `canRetrieveWindowContent` + `canPerformGestures`），`application android:label=""` 为空，服务 label 借用 `app_name` = **Music Downloader**。

**引导链（纯运行期页面流转）**
1. `Tatarian.onCreate` 读 SharedPreferences 的 `setting/drop/ok/permission`，决定进 `botanics` / `Okawville` / 展示引导布局（`layout 2131361820` 按钮）。
2. `Okawville.onResume` 用 `getPackageInfo("com.opthalmologic.salicylize")` 判断插件是否已安装；**未装 → `showDialog()` 弹不可取消 `AlertDialog`**（`setCancelable(false)`，仅有 "YÜKLE" 正按钮，无取消/返回），title「Bilgi」、message「Uygulamamızı kullanabilmek için eklentiyi yüklemelisiniz.」。
3. 点击 → Toast「Eklenti kuruluyor lütfen bekleyiniz.」→ `createSession` + `addApkToInstallSession` + `commit(SESSION_API_PACKAGE_INSTALLED)`；`onNewIntent` 按 `STATUS` 分派：`-1` 转发安装器 Intent、`0` 启动内层并传 `package`/`packagestp`、`7` 回到 `onResume` 重弹。
4. 内层 `awfullooking.onResume`：写配置、起线程、申请 `POST_NOTIFICATIONS`、跳 `quinanisole`。
5. 无障碍服务 `cylindricality.onServiceConnected()` 立即 `performGlobalAction(1)`（GLOBAL_ACTION_BACK），把用户从设置页弹回；`mispoint()` 用 `WindowManager`（type 2032、flags 2008、alpha 由云控配置）叠加 `FrameLayout + ImageView + layout/mantels` 悬浮引导层，文字来自云控；`cylindricality$19.run` 解析云端 `di/gA` 键值（包名/类名）后在锁屏未锁时 `startActivity(superfunctional, FLAG_ACTIVITY_NEW_TASK)`，由 `superfunctional.onStart` 载入**远端 WebView** 页面。

**关键发现与边界**
- **静态未发现** `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转（后者仅出现在 GMS 库 `zzt.zzc`，非应用代码）；引导文案与"设置页"视觉主要靠**远端 WebView + 悬浮窗 + 伪造系统文案资源**（`appname="Settings"`、`allow="İzin Ver"`、`battery="Düşük Pil"`），这些远端 HTML 与云控文本（AES-CBC，硬编码密钥 `B9M80O2RAK1VRJNV`）无法静态还原，故无法逐字给出无障碍教学页原文。
- 未见 13+ 受限设置（应用详情右上角）分步教学代码，也未见 `GLOBAL_ACTION_HOME` 级撤权阻断。

**未写入风险记录**：本轮受 14 次工具调用硬约束收口，未调用 `record_risk`，结论以上述证据为准。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "两层结构均静态可见：外层投放器（Tatarian/Okawville）与内嵌载荷 assets/app.apk（com.opthalmologic.salicylize）已完整解包并反编译，无障碍服务清单、悬浮窗、PackageInstaller 会话逻辑均可还原。不可静态还原部分为：1) 所有 URL、键名、路径与云端配置键均以 AES/CBC + 硬编码密钥 B9M80O2RAK1VRJNV 加密（idololater.prewrapped / Cheston.Mohammedanism），需运行期或脚本解密；2) 实际引导/教学页面为远端 WebView（superfunctional.loadUrl 拼接云端 base + 路径 + 设备号 + 语言），HTML 内容与云控文案（mispoint 的悬浮层文本、cylindricality$19 的 di/gA 键值）完全依赖服务端下发，包内不存在。",
  "summary_one_liner": "音乐下载器外壳仅作投放器，用不可取消 AlertDialog 强推安装加密内嵌的第二个 APK，真正的无障碍服务藏在内层空标签应用中，靠云端下发的远端 WebView 页面与 WindowManager 悬浮遮罩完成诱导，服务连接瞬间自按返回键。",
  "disguise_identity": {
    "app_display_name": "Müzik İndir",
    "claimed_brand_or_persona": "音乐下载器（Music Downloader），并以『插件/eklenti』名义把恶意载荷包装成功能扩展组件",
    "a11y_service_label": "Music Downloader（内层 app_name；服务声明 android:label=@string/app_name，应用级 android:label 为空字符串）",
    "identity_mismatch": true,
    "obfuscation_tricks": "内层 application android:label=\"\" 空标签以在系统界面隐藏名称；无障碍服务借用通用名 Music Downloader 掩盖真实用途；res/values/strings.xml 混入伪造系统 UI 文案 appname=\"Settings\"、allow=\"İzin Ver\"、battery=\"Düşük Pil\"；全部敏感字符串、URL、包名与云端配置键使用 AES/CBC 硬编码密钥加密；类名方法名替换为随机英文词（Okawville/cylindricality/mispoint）；载荷以 assets/app.apk 形式嵌入；外层三个 exported Activity 均无真实业务界面，Okawville 以 singleTask + 自定义 SESSION_API_PACKAGE_INSTALLED 动作承接安装结果。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.parcellize.unmatrimonial.Tatarian（LAUNCHER，singleTask）",
      "trigger_event": "onCreate 读取 SharedPreferences \"setting\" 中的 drop/ok/permission 键，决定跳转 botanics、跳转 Okawville 或展示引导布局",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（setContentView(2131361820) + Button(2131165277)，文案资源未在 strings.xml 中显式命名）",
      "shown_text_zh": "一个仅含单个按钮的极简引导页，无功能说明",
      "user_action_requested": "点击页面唯一按钮进入下一步（无跳过/取消入口）",
      "code_anchor": "com.parcellize.unmatrimonial.Tatarian.onCreate；Tatarian$1.onClick"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.parcellize.unmatrimonial.Okawville（exported，singleTask）",
      "trigger_event": "onResume 调用 isAppInstalled(\"com.opthalmologic.salicylize\")，返回 false 时进入 showDialog()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该 Activity 仅 setContentView(2131361821)，无可见业务内容）",
      "shown_text_zh": "空白过渡页面，随即被强制弹窗覆盖",
      "user_action_requested": "无操作，被动进入弹窗",
      "code_anchor": "com.parcellize.unmatrimonial.Okawville.onResume / isAppInstalled"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "AlertDialog（Okawville.bulten），标题 @string/information、正文 @string/message、唯一按钮 @string/ok",
      "trigger_event": "Okawville.showDialog() 由 onResume 触发；builder.setCancelable(false) 使其无法被返回键或点击外部取消",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Bilgi / Uygulamamızı kullanabilmek için eklentiyi yüklemelisiniz. / YÜKLE",
      "shown_text_zh": "「信息」/「要使用我们的应用，您必须安装该插件。」/「安装」",
      "user_action_requested": "只能点击「YÜKLE（安装）」；对话框不可取消，无取消、跳过或关闭按钮，返回键无效",
      "code_anchor": "com.parcellize.unmatrimonial.Okawville.showDialog；res/values/strings.xml (information/message/ok)"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "Okawville$1.onClick → PackageInstaller 会话 + onNewIntent 状态分派",
      "trigger_event": "点击后 Toast 提示并 commit 安装会话；安装回调进入 onNewIntent，按 android.content.pm.extra.STATUS 分支：-1 转发安装器 Intent，0 启动已装插件，7 重新调用 onResume",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Eklenti kuruluyor lütfen bekleyiniz.",
      "shown_text_zh": "「插件正在安装，请稍候。」",
      "user_action_requested": "无显式拒绝路径：用户若在系统安装器上取消（STATUS=7），流程回到 onResume 重新弹出同一个不可取消的「YÜKLE」对话框，形成强制重试循环",
      "code_anchor": "com.parcellize.unmatrimonial.Okawville$1.onClick；Okawville.onNewIntent；Okawville.addApkToInstallSession"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "内层载荷 com.opthalmologic.salicylize.awfullooking → quinanisole",
      "trigger_event": "外层 onResume/onNewIntent 通过 getLaunchIntentForPackage 启动内层并附带 package=宿主包名、packagestp=botanics 类名；内层 onResume 写配置、起后台线程、申请 POST_NOTIFICATIONS（SDK>32 走 Unneapolitan/shouldShowRequestPermissionRationale，否则 shedevil），随后跳 quinanisole",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（内层 strings 中预留 perm=\"Uygulamanın tüm özelliklerini kullanmak için izin vermeniz gerekiyor.\"、allow=\"İzin Ver\"）",
      "shown_text_zh": "「为使用应用的全部功能，您需要授予权限。」/「允许」",
      "user_action_requested": "授予通知等运行时权限；无障碍权限尚未在此步请求",
      "code_anchor": "com.opthalmologic.salicylize.awfullooking.onResume / Unneapolitan / shedevil；res/values/strings.xml (perm/allow)"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "cylindricality.mispoint：WindowManager.addView(FrameLayout + ImageView + layout/mantels)，LayoutParams(type=2032, flags=2008, -3)，alpha 取自云端配置",
      "trigger_event": "无障碍服务 onAccessibilityEvent 内调用；先校验云端配置键值是否等于预期值，通过后叠加悬浮层，文本由 encyst.prelusively 解密云端下发内容",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（文本来自云端下发，静态不可得；关联资源 layout/mantels、R$id.hoistman、drawable/selfresigned、drawable/sphygmomanometers）",
      "shown_text_zh": "在系统界面之上叠加的半透明引导层，含提示文字与图标，视觉与文案完全由服务端控制",
      "user_action_requested": "按悬浮层指引继续操作（内容远端下发，静态无法确定）",
      "code_anchor": "com.opthalmologic.salicylize.cylindricality.mispoint；res/layout/mantels"
    },
    {
      "step": 7,
      "stage": "跳受限设置",
      "screen_or_component": "cylindricality$19.run → superfunctional（远端 WebView 载体）",
      "trigger_event": "无障碍事件回调中解析云端下发的 di/gA 键值对（包名/类名），用 KeyguardManager.isKeyguardLocked() 确认未锁屏且设置开关匹配后，startActivity 拉起 superfunctional 并附 extras",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "无（loadUrl = 云端 base + 路径 + 参数 + 设备标识 + Locale 语言；页面内容不在包内）",
      "shown_text_zh": "由服务端按设备号与语言下发的 HTML 引导/教学页面，静态包内不存在对应文本",
      "user_action_requested": "不可静态还原（页面与按钮由远端 HTML 决定）",
      "code_anchor": "com.opthalmologic.salicylize.cylindricality$19.run；com.opthalmologic.salicylize.superfunctional.onStart"
    }
  ],
  "text_presentation_locations": [
    "外层 Okawville.showDialog() 的不可取消 AlertDialog（标题 @string/information、正文 @string/message、正按钮 @string/ok），位于 Okawville Activity 之上",
    "外层 Okawville$1.onClick 中的 Toast：@string/click「Eklenti kuruluyor lütfen bekleyiniz.」",
    "外层 Tatarian 引导布局 layout 2131361820 + Button 2131165277（文案资源未在 strings.xml 中显式命名）",
    "内层无障碍服务 cylindricality.mispoint 通过 WindowManager 叠加的悬浮层（layout/mantels、R$id.hoistman TextView、drawable/selfresigned、drawable/sphygmomanometers），文字由 encyst.prelusively 解密云端内容",
    "内层 superfunctional 的远端 WebView 页面（loadUrl 拼接云端 base、路径、设备标识与语言），无本地 assets HTML",
    "内层 res/values/strings.xml 中预留但为伪造系统 UI 的文案：appname=\"Settings\"、allow=\"İzin Ver\"、battery=\"Düşük Pil\"、perm=\"Uygulamanın tüm özelliklerini kullanmak için izin vermeniz gerekiyor.\"",
    "系统无障碍服务列表中显示的服务名：内层 service android:label=@string/app_name → \"Music Downloader\"（无 android:description 说明文案）"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Uygulamamızı kullanabilmek için eklentiyi yüklemelisiniz.",
      "text_zh": "要使用我们的应用，您必须安装该插件。",
      "source_location": "外层 res/values/strings.xml key=message（Okawville.showDialog setMessage(2131492894)）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "Bilgi",
      "text_zh": "信息",
      "source_location": "外层 res/values/strings.xml key=information（Okawville.showDialog setTitle(2131492893)）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "YÜKLE",
      "text_zh": "安装",
      "source_location": "外层 res/values/strings.xml key=ok（Okawville.showDialog setPositiveButton(2131492895)）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "Eklenti kuruluyor lütfen bekleyiniz.",
      "text_zh": "插件正在安装，请稍候。",
      "source_location": "外层 res/values/strings.xml key=click（Okawville$1.onClick Toast, 2131492892）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "Uygulamanın tüm özelliklerini kullanmak için izin vermeniz gerekiyor.",
      "text_zh": "为使用应用的全部功能，您需要授予权限。",
      "source_location": "内层 res/values/strings.xml key=perm",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "İzin Ver",
      "text_zh": "允许",
      "source_location": "内层 res/values/strings.xml key=allow",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Settings",
      "text_zh": "设置",
      "source_location": "内层 res/values/strings.xml key=appname",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "tr",
      "text_verbatim": "Düşük Pil",
      "text_zh": "电量不足",
      "source_location": "内层 res/values/strings.xml key=battery",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Music Downloader",
      "text_zh": "音乐下载器",
      "source_location": "内层 res/values/strings.xml key=app_name（无障碍服务 android:label）",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "Okawville.showDialog 设置 setCancelable(false) 且仅提供正按钮，用户无法取消或跳过。用户若在系统安装器取消安装，onNewIntent 收到 STATUS=7 后直接再次调用 onResume，重新走 isAppInstalled 检查并重弹同一个不可取消对话框，形成强制安装循环；STATUS=-1（安装器失败/需人工）则转发安装器 Intent，STATUS=0 才放行启动内层。",
    "overlay_or_fake_settings": "有。cylindricality.mispoint 通过 WindowManager.addView 叠加 FrameLayout(ImageView + layout/mantels) 悬浮层，LayoutParams 为 type=2032、flags=2008、-3，透明度由云端配置键读取后 setAlpha 动态设置；内层 strings 预留 appname=\"Settings\"、allow=\"İzin Ver\"、battery=\"Düşük Pil\" 等伪造系统界面文案，说明存在高仿系统设置/引导页的视觉素材，但具体布局与文字由云端下发，静态不可见。",
    "restricted_settings_13plus_coaching": "无。应用自身代码中未出现 android.settings.APPLICATION_DETAILS_SETTINGS 或 ACTION_MANAGE_UNKNOWN_APP_SOURCES 跳转（前者仅出现在 GMS 库 com.google.android.gms.common.internal.zzt.zzc），未见教用户进应用详情右上角开启受限设置的文案或分步引导。",
    "post_grant_anti_removal": "部分：cylindricality.onServiceConnected() 在无障碍服务连接成功的瞬间立即调用 performGlobalAction(1)（GLOBAL_ACTION_BACK），把用户从系统无障碍设置页弹回，缩短用户停留在设置页的时间；未发现 GLOBAL_ACTION_HOME、监听设置页并拦截撤权、或伪造 isAccessibilityTool 声明的代码。",
    "benign_graceful_degradation": "无。未提供手动模式、仅观看模式或 ADB 等替代路径；未安装插件时唯一路径是安装内嵌载荷。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到外层进程发起 PackageInstaller 会话提交（commit 携带 action com.example.android.apis.content.SESSION_API_PACKAGE_INSTALLED）或 startActivity 目标切换到 com.opthalmologic.salicylize 时拉起 UTG；进入内层后，以 com.opthalmologic.salicylize.cylindricality（无障碍服务）onServiceConnected 被调用、以及 WindowManager 出现 type=2032 覆盖层（悬浮窗新增）为第二触发点；同时在无障碍服务启用后监测是否有 GLOBAL_ACTION_BACK 全局动作（服务连接瞬间的自动返回）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动强制安装弹窗页",
        "page_identifier": "Okawville Activity 之上的 AlertDialog：标题「Bilgi」、正文「Uygulamamızı kullanabilmek için eklentiyi yüklemelisiniz.」、单按钮「YÜKLE」，无取消/关闭控件",
        "why_most_useful": "这是整个诱导链的起点与唯一强制门禁，其不可取消性是判定胁迫程度最直接的证据，也决定后续是否进入载荷安装",
        "observable_utg_signals": ["Dialog 节点仅有 1 个 Button 且文本为 YÜKLE", "节点树中不存在 negative/cancel 按钮与关闭图标", "返回键后对话框仍存在（setCancelable(false)）", "当前窗口包名 com.parcellize.unmatrimonial"]
      },
      {
        "page_role": "安装载荷后首次进入内层应用的引导/权限页",
        "page_identifier": "com.opthalmologic.salicylize.awfullooking 及其跳转的 quinanisole，含 POST_NOTIFICATIONS 运行时权限弹窗与后续引导界面",
        "why_most_useful": "确认外层投放与内层恶意载荷之间的接续关系，并捕获内层实际展示的引导文案（该层 label 为空，界面文本是判定伪装身份的关键）",
        "observable_utg_signals": ["当前前台包名由 com.parcellize.unmatrimonial 切换为 com.opthalmologic.salicylize", "出现系统通知权限授权框", "界面中出现 İzin Ver / Settings 等伪造系统文案", "应用名称显示为空或 Music Downloader"]
      },
      {
        "page_role": "设置页后压栈遮罩页（悬浮引导层）",
        "page_identifier": "WindowManager 添加的 FrameLayout 覆盖层（type=2032、flags=2008），内含 layout/mantels 的 TextView 与 ImageView，透明度由云端配置控制",
        "why_most_useful": "该层是覆盖在系统界面之上的引导载体，其文本与透明度来自云端下发，UTG 抓取可得到静态无法还原的诱导文案，是区分『良性说明』与『教唆开启无障碍』的决定性证据",
        "observable_utg_signals": ["节点树出现与前台 Activity 不同包名的悬浮窗口层级", "悬浮层内 TextView 文本（云端下发）", "悬浮层是否遮挡系统无障碍开关控件", "悬浮层是否有箭头/手势指引指向无障碍开关"]
      },
      {
        "page_role": "远端 WebView 教学页",
        "page_identifier": "com.opthalmologic.salicylize.superfunctional 内 new WebView 加载的远端 URL（拼接云端 base + 路径 + 设备标识 + 语言）",
        "why_most_useful": "这是应用最主要的引导说明载体，HTML 完全由服务端下发，只有运行期 UTG 才能取得逐字教学文本与分步截图指引",
        "observable_utg_signals": ["WebView 节点及其 url 属性（云端域名与路径）", "页面内 button/a 文本与分步序号", "页面是否出现无障碍设置/应用详情设置的截图或指向箭头", "页面语言是否随 Locale 变化"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载的服务中的 Music Downloader 条目（对应 com.opthalmologic.salicylize.cylindricality）",
        "why_most_useful": "确认最终用户被引导开启的正是内层恶意服务，并核对系统列表中呈现的名称与说明（该服务未声明 android:description，说明文案缺失本身即为可疑信号）",
        "observable_utg_signals": ["服务条目文本 Music Downloader 与开关状态", "是否存在 description 说明文字（预期为空）", "开启瞬间页面是否被自动返回键弹回", "开启后悬浮层是否立即出现"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "主要盲区有三：1) 引导文案与教学页面几乎全部由服务端下发（superfunctional 的远端 WebView、mispoint 的悬浮层文本、cylindricality$19 的 di/gA 键值），包内无本地 HTML，离线或断网时可能整条引导链静默不出现，导致 UTG 抓不到关键页面；2) 悬浮层含 drawable 图片引导（sphygmomanometers、selfresigned），若服务端只下发图片而文字为空，需 OCR 才能读出诱导内容；3) 载荷为两阶段投放，第一阶段（外层）本身不含任何无障碍代码与设置页跳转，若只静态审计外层会完全看不到无障碍能力，必须运行到内层安装完成才可见。此外静态加壳不阻挡运行期 UTG，本样本未加壳，仅对字符串做 AES 加密，不影响页面抓取。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.parcellize.unmatrimonial.Okawville.showDialog",
    "com.parcellize.unmatrimonial.Okawville$1.onClick",
    "com.parcellize.unmatrimonial.Okawville.onResume",
    "com.opthalmologic.salicylize.cylindricality.onServiceConnected",
    "com.opthalmologic.salicylize.cylindricality.mispoint",
    "com.opthalmologic.salicylize.superfunctional.onStart"
  ]
}
```

</details>
