# MB_039__3dc24332f8｜SpyNote — Blockchain

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：210.5s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 Blockchain 的 SpyNote 远控样本，冷启动先反模拟器拦截，再用全屏图片式引导页（任意可点区域共用同一监听）一键跳转 android.settings.ACCESSIBILITY_SETTINGS 并带 EXTRA_COMPONENT_NAME 直达自身无障碍开关，服务名同为 Blockchain 且 description 仅填 "..."。
- **静态可见性说明**：无障碍诱导链在 classes.dex 中完整静态可见：引导 Activity、点击回调、三级 Intent 降级与 AccessService 组件名均可反编译还原。字符串经 utilities.epncfbkgiy…53(String) 运行时解密并附带超长随机后缀，但解密入参为明文常量，可静态还原。引导页正文由背景/前景图片承载（布局 0x7f0a001c / 0x7f0a001f），需 OCR 才能获得逐字文案。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3dc24332f897ef758c38e4959624606236a3c63a1ba2e0b3d268ed6ce40b5c1a` |
| 包名 / 年份 | `com.definitely.cell` / 2026 |
| 家族 / 品类 | **SpyNote**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Blockchain |
| 引导页宣称品牌/身份 | Blockchain（区块链/钱包品牌），并混用 Binance、Play Store、com.samsung.accessibility 伪组件与 CraxsBrowser 远控模块命名 |
| 系统无障碍列表服务名 | Blockchain（service 与 application 均引用 @string/syracusedcentreso59，值为 Blockchain） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) android:description 仅填 "..."，系统无障碍列表看不到真实用途；2) FirstLauncherAlias 使用 android:label=" " 与 android:icon=@android:color/transparent 且 enabled=false，SecondLauncherAlias 常驻，构成多 activity-alias 交替伪装；3) zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20、FloatingView、WakeupActivity、RequestUninstall 等多个组件 label=" "；4) CameraActvity 的 label 伪装为 "Play Store"；5) strings.xml 将原文品牌词批量替换为 Blockchain（如 last Blockchain Fri %s）；6) 跳转意图以混淆字符串拼接 com.samsung.accessibility…installed_service；7) 关键字符串常量带 200+ 字符随机后缀并由解密函数还原；8) accessdiecrip.xml 的 settingsActivity 指向不存在的 com.eagle.* 包。 |
| 无障碍服务类名 | `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.izslnugibofsewfchgnsgwkoulrdrnjwlcnzwkhncjuoskhsxn3.AccessService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：@00000000 |
| 共现高危权限 | `CALL_PHONE, CAMERA, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | ... |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.MainActivity（Theme.Translucent.NoTitleBar，taskAffinity=app.one） | Launcher 点击 / MAIN 入口触发 onCreate | 原生Activity | **原文**：无（透明无标题主题，仅记录 ScreenWidth/ScreenHight）<br>**译注**：无可视界面，透明 Activity 先做环境探测与本地配置写入 | 无 | `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.MainActivity#onCreate` |
| 2 | 冷启动入口 | MainActivity 内 AlertDialog（主题 0x7f0d0002，标题取自 0x7f0c0043，图标为应用自身图标） | onCreate 中 utilities.NeedAutoStart() 为真且 MySettings.AutoStartOn 未记录、isAutoStartPermissionAvailable() 可用 | 原生Dialog | **原文**：this App request Auto Start/Run in Background Permission to work properly / 此应用程序请求自动启动和在后台运行权限才能正常工作 / Bu uygulama, düzgün çalışması için hem otomatik başlatma hem de arka planda çalıştırma izinlerini ister / يطلب هذا التطبيق كلاً من بدء التشغيل التلقائي والتشغيل في أذونات الخلفية للعمل بشكل صحيح<br>**译注**：本应用需要自启动/后台运行权限才能正常工作（四语硬编码：英/中/土/阿） | 仅可点 OK/Tamam/好的/موافق（setPositiveButton 单按钮，未设置取消或跳过） | `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.MainActivity#onCreate / MainActivity$7#onClick` |
| 3 | 引导说明页 | com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20（excludeFromRecents=true，label=" "） | onCreate 中 utilities.isAccessibilityServiceEnabled(this, AccessService.class) 返回 false 时 setContentView 引导布局 | 原生Activity（全屏图片式引导，MIUI 分支布局 0x7f0a001f，通用分支布局 0x7f0a001c） | **原文**：Next / 下一个 / التالي<br>**译注**：引导页按钮文案“下一步”；页面主体为背景图 + 应用图标 ImageView（图标取自 com.definitely.cell），正文文本由图片承载 | 点击页面任意可点元素（nextButton 及多个 ImageView 全部绑定同一 Oklistner），未见取消/跳过/返回入口 | `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20#onCreate / res/layout 0x7f0a001c、0x7f0a001f` |
| 4 | 跳无障碍设置 | 系统无障碍设置页（Intent android.settings.ACCESSIBILITY_SETTINGS，携带 EXTRA_COMPONENT_NAME=ComponentName(pkg, AccessService.class)） | 引导页 Oklistner → zgoz…20$2#onClick | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS / android.intent.extra.COMPONENT_NAME / com.samsung.accessibility….installed_service<br>**译注**：三级降级：先尝试伪三星组件 installed_service → 再尝试带随机后缀的 android.settings.*ACCESSIBILITY_SETTINGS → 最终使用原生 android.settings.ACCESSIBILITY_SETTINGS 并指定自身 AccessService 组件，使系统直接定位到本应用开关项 | 用户在系统无障碍列表中手动打开 “Blockchain” 开关（列表仅显示服务名 Blockchain，描述为 "..."） | `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20$2#onClick` |
| 5 | 拒权反馈循环 | zgoz…20 再次 onCreate（由后台/服务侧重新拉起，未在本次范围内完整闭环） | onCreate 复检 isAccessibilityServiceEnabled 仍为 false；onClick 成功后 utilities.Trys = 0 并 finish() | 原生Activity | **原文**：无新增文案<br>**译注**：返回后若开关仍未打开，引导页可被再次拉起；静态未见 onResume 死循环重跳代码 | 再次点击“下一步”重复跳转 | `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20#onCreate / utilities.isAccessibilityServiceEnabled` |
| 6 | 获权后动作 | com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.izslnugibofsewfchgnsgwkoulrdrnjwlcnzwkhncjuoskhsxn3.AccessService（flagRetrieveInteractiveWindows + canRetrieveWindowContent + typeAllMask） | 系统绑定 BIND_ACCESSIBILITY_SERVICE 后 onServiceConnected | 不可静态还原（服务侧行为未在本轮展开） | 无 | 无 | `res/xml/accessdiecrip.xml / com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.Perfct#goToSetting` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity.onCreate 内的自启动/后台运行 AlertDialog（setPositiveButton 单按钮，四语硬编码字符串，标题取资源 0x7f0c0043）
- 引导 Activity zgoz…20 的全屏图片式布局（0x7f0a001c 通用 / 0x7f0a001f MIUI），正文文字由背景与前景图片承载，仅按钮为文本：Next / 下一个 / التالي
- 系统无障碍列表项：服务名显示为 Blockchain（@string/syracusedcentreso59），android:description 仅为 "..."，settingsActivity 指向不存在的 com.eagle.* 包
- 系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS + EXTRA_COMPONENT_NAME 直达本应用开关项），页面本身无自定义引导文案
- 其他组件的空白标签：FirstLauncherAlias/SecondLauncherAlias（label=" "）、FloatingView、WakeupActivity、RequestUninstall、RequestScreenCap 等 label=" "

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | this App request Auto Start/Run in Background Permission to work properly | 本应用请求自启动/后台运行权限以便正常工作 | `MainActivity#onCreate 硬编码字符串常量` | 受限设置分步教学 |
| zh | 此应用程序请求自动启动和在后台运行权限才能正常工作 | 此应用程序请求自动启动和在后台运行权限才能正常工作 | `MainActivity#onCreate 硬编码字符串常量（zh 分支）` | 受限设置分步教学 |
| tr | Bu uygulama, düzgün çalışması için hem otomatik başlatma hem de arka planda çalıştırma izinlerini ister | 本应用需要自启动和后台运行权限才能正常工作 | `MainActivity#onCreate 硬编码字符串常量（tr 分支）` | 受限设置分步教学 |
| ar | يطلب هذا التطبيق كلاً من بدء التشغيل التلقائي والتشغيل في أذونات الخلفية للعمل بشكل صحيح | 本应用请求自启动和后台运行权限以便正常工作 | `MainActivity#onCreate 硬编码字符串常量（ar 分支）` | 受限设置分步教学 |
| en | Next | 下一步 | `zgoz…20#onCreate 按钮文案（对应布局 0x7f0a001c/0x7f0a001f 的 nextButton）` | 受限设置分步教学 |
| zh | 下一个 | 下一步 | `zgoz…20#onCreate 按钮文案（zh 分支）` | 受限设置分步教学 |
| ar | التالي | 下一步 | `zgoz…20#onCreate 按钮文案（ar 分支）` | 受限设置分步教学 |
| en | ... | 省略号占位（无实际说明文字） | `res/values/strings.xml key=Descrip，被 res/xml/accessdiecrip.xml 的 android:description 引用` | 教唆忽视警告 |
| en | Blockchain | Blockchain（伪装品牌名） | `res/values/strings.xml key=syracusedcentreso59（application/activity/service label）` | 假反诈安全 |
| en | Play Store | Play 商店 | `AndroidManifest.xml CameraActvity android:label` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态可见的机制为：zgoz…20#onCreate 每次启动都复检 isAccessibilityServiceEnabled，未开启即重新 setContentView 引导页；点击跳转后 finish() 并把 utilities.Trys 置 0。未见 onResume 死循环重跳或定时器拉起代码，实际重复拉起依赖后台服务侧（本轮未完整闭环）。
- **遮罩叠层 / 高仿系统设置页**：无半透明遮罩或高仿系统开关页；采用全屏不透明图片式引导 Activity（excludeFromRecents，label=" "），叠加真系统无障碍设置页。SYSTEM_ALERT_WINDOW 权限与 FloatingView Activity 存在，但未在无障碍引导链中使用。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包未检索到 ACTION_APPLICATION_DETAILS_SETTINGS 调用，无“应用详情→右上角菜单→允许受限设置”分步教学，也无 Session 安装器绕过；targetSdk=29 亦不触发 Android 13 受限设置限制。
- **获权后即时行为与防撤权机制**：存在 WATCH_PKG_INSTALLER / WATCH_SETTINGS 与 PERFORM_GLOBAL_ACTION 线索及 Perfct#goToSetting/goToOppoBattery/goToHuaWeiBattery 的设置页节点搜索逻辑，指向用 GLOBAL_ACTION_BACK/HOME 自动操作设置页；本轮未展开确认其在撤权时的具体使用。
- **良性降级 / 替代方案**：无。未发现手动模式、仅观看模式或明确的拒权降级路径；拒权后仍是同一图片引导页复现。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以“启动 Activity 名 = com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20”或“发出 Intent action 含 ACCESSIBILITY_SETTINGS”为触发点：冷启动 MainActivity 后 1~2 秒内，无障碍未开启即会拉起该图片引导页；点击任意区域后约数百毫秒内压栈系统无障碍设置页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：主要盲区有三：1) 引导页正文以图片承载，纯文本 UTG 提取不到内容，必须 OCR 才能判断是否存在虚假安全承诺/恐吓话术；2) 冷启动前有 Anti_emu()/isEmu_DIV_ID_lator() 反模拟器分支，命中即 AsknoEmu 后 return，模拟器环境可能完全看不到引导链；3) 引导页的重复拉起依赖后台服务侧（utilities.Trys 语义未闭环），若仅做前台冷启动抓取，可能漏掉返回后的二次施压行为。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动图片式无障碍引导页** | Activity zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20；全屏无标题、无 ActionBar，含一个 “Next/下一个/التالي” 按钮与多个可点 ImageView，任务列表不可见（excludeFromRecents） | 这是诱导链条唯一的“说服”环节，其图片内容与“下一步”按钮直接决定是否存在欺骗性引导，是区分恶意诱导与良性授权请求的核心页面 | UI 层级中是否存在 Cancel/Skip/Back 等退出控件（预期缺失）；按钮文本与 locale 的对应（Next/下一个/التالي）；页面节点文本几乎为空而存在大面积 ImageView，说明文案在图片里；Activity 名与 excludeFromRecents/label=" " 的空白标题特征 |
| **系统无障碍服务列表项** | Settings → Accessibility → Installed services 中的 “Blockchain” 条目，其描述显示为 "..." | 直接验证伪装身份与服务描述空白化，是识别身份混淆最有力的运行期证据 | 服务名文本 = Blockchain；描述文本 = "..."（无实质说明）；该条目所属包名 com.definitely.cell 与桌面名一致性 |
| **跳转后的系统无障碍开关页（直达组件）** | android.settings.ACCESSIBILITY_SETTINGS 页面，因 EXTRA_COMPONENT_NAME 指向 com.definitely.cell/…AccessService 而直接定位到本应用开关 | 证明跳转不是泛化打开设置页，而是精确定位自身开关项，缩短用户操作路径、降低怀疑 | 页面直接落在本应用服务条目而非列表顶部；Intent extra 中 EXTRA_COMPONENT_NAME 的值；返回后引导页是否再次出现 |
| **冷启动自启动权限弹窗** | MainActivity 上的 AlertDialog，标题为应用名，正文为“此应用程序请求自动启动和在后台运行权限才能正常工作”，仅一个 OK 按钮 | 证明存在零可选性权限索取，且与后续无障碍引导构成连续施压链条 | 弹窗按钮数量（预期仅 1 个）；正文语言随系统 locale 切换；点击后是否立即进入图片引导页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20#onCreate`
- `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20$2#onClick`
- `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.MainActivity#onCreate`
- `com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.ikdveueesncetizdsovdwjoqijrojicxahikmgqliknocqeijk4.utilities#isAccessibilityServiceEnabled`
- `res/xml/accessdiecrip.xml`
- `res/values/strings.xml（key=Descrip、key=syracusedcentreso59）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**静态可见性：clear** — 无障碍诱导链在 DEX 中完整可读，字符串虽经 `utilities.epncfbkgiy…53()` 运行时解密，但解密调用点与参数均为明文常量，可静态还原。

**引导链路（运行期 UTG 视角）**

1. **冷启动拦截**：`MainActivity.onCreate` 先做反模拟器判定（`utilities.Anti_emu()` / `isEmu_DIV_ID_lator()` / `AsknoEmu()`），命中则直接 `return` 不进入业务；随后写入屏幕尺寸、`SetJob`、并弹 AutoStart 自启引导 `AlertDialog`（**仅 PositiveButton，无取消/跳过**），语言按 `zh/tr/en/ar` 四语硬编码。
2. **引导说明页**：无障碍未开启时进入全屏图片式引导 Activity `zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20`，MIUI 走专用布局（`0x7f0a001f` + `nextButton`，文案 `Next/下一个/التالي`），其他 ROM 走通用布局（`0x7f0a001c`），并把**多个 ImageView / Button 全部挂同一个 `Oklistner`**——点页面任意可点区域都会跳设置。
3. **跳受限设置（无障碍页）**：`$2#onClick` 用混淆拼接构造 `com.samsung.accessibility….installed_service` 伪三星组件意图 → 解析失败降级 `android.settings.…ACCESSIBILITY_SETTINGS` → 再失败降级原生 `android.settings.ACCESSIBILITY_SETTINGS` 并带 `EXTRA_COMPONENT_NAME = ComponentName(pkg, AccessService.class)` **直达本应用开关项**；跳转后立即 `finish()` 并 `utilities.Trys = 0`。
4. **获权判定**：`utilities.isAccessibilityServiceEnabled()` 读 `Settings.Secure.enabled_accessibility_services` 判断是否已开启，已开启则走另一条 `setContentView` 分支（跳过引导）。

**身份伪装事实**：桌面名 `Blockchain`（`@string/syracusedcentreso59`）；无障碍列表服务名同为 `Blockchain`；`android:description` 为 `"..."`（**空白占位，系统列表看不到任何用途说明**）；`FirstLauncherAlias` 为 `android:label=" "` + 透明图标且 `enabled="false"`，`SecondLauncherAlias` 常驻；多个 Activity 标签为 `" "`，`CameraActvity` 标签伪装成 `Play Store`。字符串表大量把原文里的品牌词替换成 `Blockchain`（如 "last Blockchain Fri %s"），属品牌词批量置换伪装。

**未发现**：无 `ACTION_APPLICATION_DETAILS_SETTINGS` 调用（**未见 Android 13+ 受限设置分步教学**）；`onCreate`/`onClick` 中未见 `onResume` 死循环重跳；无 `isAccessibilityTool` 伪造声明；`settingsActivity` 指向不存在的 `com.eagle.…` 包（无效指向）。

**覆盖边界**：`onResume` 与后台服务侧的重复拉起（`utilities.Trys` 计数语义）未逐一闭环；引导页文案以图片承载，需 OCR 才能取到逐字文本。因工具调用已超出本轮硬性预算，未写入 `record_risk` 风险台账。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导链在 classes.dex 中完整静态可见：引导 Activity、点击回调、三级 Intent 降级与 AccessService 组件名均可反编译还原。字符串经 utilities.epncfbkgiy…53(String) 运行时解密并附带超长随机后缀，但解密入参为明文常量，可静态还原。引导页正文由背景/前景图片承载（布局 0x7f0a001c / 0x7f0a001f），需 OCR 才能获得逐字文案。",
  "summary_one_liner": "伪装成 Blockchain 的 SpyNote 远控样本，冷启动先反模拟器拦截，再用全屏图片式引导页（任意可点区域共用同一监听）一键跳转 android.settings.ACCESSIBILITY_SETTINGS 并带 EXTRA_COMPONENT_NAME 直达自身无障碍开关，服务名同为 Blockchain 且 description 仅填 \"...\"。",
  "disguise_identity": {
    "app_display_name": "Blockchain",
    "claimed_brand_or_persona": "Blockchain（区块链/钱包品牌），并混用 Binance、Play Store、com.samsung.accessibility 伪组件与 CraxsBrowser 远控模块命名",
    "a11y_service_label": "Blockchain（service 与 application 均引用 @string/syracusedcentreso59，值为 Blockchain）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) android:description 仅填 \"...\"，系统无障碍列表看不到真实用途；2) FirstLauncherAlias 使用 android:label=\" \" 与 android:icon=@android:color/transparent 且 enabled=false，SecondLauncherAlias 常驻，构成多 activity-alias 交替伪装；3) zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20、FloatingView、WakeupActivity、RequestUninstall 等多个组件 label=\" \"；4) CameraActvity 的 label 伪装为 \"Play Store\"；5) strings.xml 将原文品牌词批量替换为 Blockchain（如 last Blockchain Fri %s）；6) 跳转意图以混淆字符串拼接 com.samsung.accessibility…installed_service；7) 关键字符串常量带 200+ 字符随机后缀并由解密函数还原；8) accessdiecrip.xml 的 settingsActivity 指向不存在的 com.eagle.* 包。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.MainActivity（Theme.Translucent.NoTitleBar，taskAffinity=app.one）",
      "trigger_event": "Launcher 点击 / MAIN 入口触发 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（透明无标题主题，仅记录 ScreenWidth/ScreenHight）",
      "shown_text_zh": "无可视界面，透明 Activity 先做环境探测与本地配置写入",
      "user_action_requested": "无",
      "code_anchor": "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "MainActivity 内 AlertDialog（主题 0x7f0d0002，标题取自 0x7f0c0043，图标为应用自身图标）",
      "trigger_event": "onCreate 中 utilities.NeedAutoStart() 为真且 MySettings.AutoStartOn 未记录、isAutoStartPermissionAvailable() 可用",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "this App request Auto Start/Run in Background Permission to work properly / 此应用程序请求自动启动和在后台运行权限才能正常工作 / Bu uygulama, düzgün çalışması için hem otomatik başlatma hem de arka planda çalıştırma izinlerini ister / يطلب هذا التطبيق كلاً من بدء التشغيل التلقائي والتشغيل في أذونات الخلفية للعمل بشكل صحيح",
      "shown_text_zh": "本应用需要自启动/后台运行权限才能正常工作（四语硬编码：英/中/土/阿）",
      "user_action_requested": "仅可点 OK/Tamam/好的/موافق（setPositiveButton 单按钮，未设置取消或跳过）",
      "code_anchor": "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.MainActivity#onCreate / MainActivity$7#onClick"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20（excludeFromRecents=true，label=\" \"）",
      "trigger_event": "onCreate 中 utilities.isAccessibilityServiceEnabled(this, AccessService.class) 返回 false 时 setContentView 引导布局",
      "ui_carrier": "原生Activity（全屏图片式引导，MIUI 分支布局 0x7f0a001f，通用分支布局 0x7f0a001c）",
      "shown_text_verbatim": "Next / 下一个 / التالي",
      "shown_text_zh": "引导页按钮文案“下一步”；页面主体为背景图 + 应用图标 ImageView（图标取自 com.definitely.cell），正文文本由图片承载",
      "user_action_requested": "点击页面任意可点元素（nextButton 及多个 ImageView 全部绑定同一 Oklistner），未见取消/跳过/返回入口",
      "code_anchor": "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20#onCreate / res/layout 0x7f0a001c、0x7f0a001f"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（Intent android.settings.ACCESSIBILITY_SETTINGS，携带 EXTRA_COMPONENT_NAME=ComponentName(pkg, AccessService.class)）",
      "trigger_event": "引导页 Oklistner → zgoz…20$2#onClick",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS / android.intent.extra.COMPONENT_NAME / com.samsung.accessibility….installed_service",
      "shown_text_zh": "三级降级：先尝试伪三星组件 installed_service → 再尝试带随机后缀的 android.settings.*ACCESSIBILITY_SETTINGS → 最终使用原生 android.settings.ACCESSIBILITY_SETTINGS 并指定自身 AccessService 组件，使系统直接定位到本应用开关项",
      "user_action_requested": "用户在系统无障碍列表中手动打开 “Blockchain” 开关（列表仅显示服务名 Blockchain，描述为 \"...\"）",
      "code_anchor": "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20$2#onClick"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "zgoz…20 再次 onCreate（由后台/服务侧重新拉起，未在本次范围内完整闭环）",
      "trigger_event": "onCreate 复检 isAccessibilityServiceEnabled 仍为 false；onClick 成功后 utilities.Trys = 0 并 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无新增文案",
      "shown_text_zh": "返回后若开关仍未打开，引导页可被再次拉起；静态未见 onResume 死循环重跳代码",
      "user_action_requested": "再次点击“下一步”重复跳转",
      "code_anchor": "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20#onCreate / utilities.isAccessibilityServiceEnabled"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.izslnugibofsewfchgnsgwkoulrdrnjwlcnzwkhncjuoskhsxn3.AccessService（flagRetrieveInteractiveWindows + canRetrieveWindowContent + typeAllMask）",
      "trigger_event": "系统绑定 BIND_ACCESSIBILITY_SERVICE 后 onServiceConnected",
      "ui_carrier": "不可静态还原（服务侧行为未在本轮展开）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后服务具备全量事件监听、窗口内容抓取与全局动作能力，配合 Perfct#goToSetting/goToOppoBattery 等节点搜索逻辑做设置页自动操作",
      "user_action_requested": "无",
      "code_anchor": "res/xml/accessdiecrip.xml / com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.Perfct#goToSetting"
    }
  ],
  "text_presentation_locations": [
    "MainActivity.onCreate 内的自启动/后台运行 AlertDialog（setPositiveButton 单按钮，四语硬编码字符串，标题取资源 0x7f0c0043）",
    "引导 Activity zgoz…20 的全屏图片式布局（0x7f0a001c 通用 / 0x7f0a001f MIUI），正文文字由背景与前景图片承载，仅按钮为文本：Next / 下一个 / التالي",
    "系统无障碍列表项：服务名显示为 Blockchain（@string/syracusedcentreso59），android:description 仅为 \"...\"，settingsActivity 指向不存在的 com.eagle.* 包",
    "系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS + EXTRA_COMPONENT_NAME 直达本应用开关项），页面本身无自定义引导文案",
    "其他组件的空白标签：FirstLauncherAlias/SecondLauncherAlias（label=\" \"）、FloatingView、WakeupActivity、RequestUninstall、RequestScreenCap 等 label=\" \""
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "this App request Auto Start/Run in Background Permission to work properly",
      "text_zh": "本应用请求自启动/后台运行权限以便正常工作",
      "source_location": "MainActivity#onCreate 硬编码字符串常量",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "此应用程序请求自动启动和在后台运行权限才能正常工作",
      "text_zh": "此应用程序请求自动启动和在后台运行权限才能正常工作",
      "source_location": "MainActivity#onCreate 硬编码字符串常量（zh 分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Bu uygulama, düzgün çalışması için hem otomatik başlatma hem de arka planda çalıştırma izinlerini ister",
      "text_zh": "本应用需要自启动和后台运行权限才能正常工作",
      "source_location": "MainActivity#onCreate 硬编码字符串常量（tr 分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ar",
      "text_verbatim": "يطلب هذا التطبيق كلاً من بدء التشغيل التلقائي والتشغيل في أذونات الخلفية للعمل بشكل صحيح",
      "text_zh": "本应用请求自启动和后台运行权限以便正常工作",
      "source_location": "MainActivity#onCreate 硬编码字符串常量（ar 分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Next",
      "text_zh": "下一步",
      "source_location": "zgoz…20#onCreate 按钮文案（对应布局 0x7f0a001c/0x7f0a001f 的 nextButton）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "下一个",
      "text_zh": "下一步",
      "source_location": "zgoz…20#onCreate 按钮文案（zh 分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ar",
      "text_verbatim": "التالي",
      "text_zh": "下一步",
      "source_location": "zgoz…20#onCreate 按钮文案（ar 分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "...",
      "text_zh": "省略号占位（无实际说明文字）",
      "source_location": "res/values/strings.xml key=Descrip，被 res/xml/accessdiecrip.xml 的 android:description 引用",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Blockchain",
      "text_zh": "Blockchain（伪装品牌名）",
      "source_location": "res/values/strings.xml key=syracusedcentreso59（application/activity/service label）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Play Store",
      "text_zh": "Play 商店",
      "source_location": "AndroidManifest.xml CameraActvity android:label",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态可见的机制为：zgoz…20#onCreate 每次启动都复检 isAccessibilityServiceEnabled，未开启即重新 setContentView 引导页；点击跳转后 finish() 并把 utilities.Trys 置 0。未见 onResume 死循环重跳或定时器拉起代码，实际重复拉起依赖后台服务侧（本轮未完整闭环）。",
    "overlay_or_fake_settings": "无半透明遮罩或高仿系统开关页；采用全屏不透明图片式引导 Activity（excludeFromRecents，label=\" \"），叠加真系统无障碍设置页。SYSTEM_ALERT_WINDOW 权限与 FloatingView Activity 存在，但未在无障碍引导链中使用。",
    "restricted_settings_13plus_coaching": "无。全包未检索到 ACTION_APPLICATION_DETAILS_SETTINGS 调用，无“应用详情→右上角菜单→允许受限设置”分步教学，也无 Session 安装器绕过；targetSdk=29 亦不触发 Android 13 受限设置限制。",
    "post_grant_anti_removal": "存在 WATCH_PKG_INSTALLER / WATCH_SETTINGS 与 PERFORM_GLOBAL_ACTION 线索及 Perfct#goToSetting/goToOppoBattery/goToHuaWeiBattery 的设置页节点搜索逻辑，指向用 GLOBAL_ACTION_BACK/HOME 自动操作设置页；本轮未展开确认其在撤权时的具体使用。",
    "benign_graceful_degradation": "无。未发现手动模式、仅观看模式或明确的拒权降级路径；拒权后仍是同一图片引导页复现。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以“启动 Activity 名 = com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20”或“发出 Intent action 含 ACCESSIBILITY_SETTINGS”为触发点：冷启动 MainActivity 后 1~2 秒内，无障碍未开启即会拉起该图片引导页；点击任意区域后约数百毫秒内压栈系统无障碍设置页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动图片式无障碍引导页",
        "page_identifier": "Activity zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20；全屏无标题、无 ActionBar，含一个 “Next/下一个/التالي” 按钮与多个可点 ImageView，任务列表不可见（excludeFromRecents）",
        "why_most_useful": "这是诱导链条唯一的“说服”环节，其图片内容与“下一步”按钮直接决定是否存在欺骗性引导，是区分恶意诱导与良性授权请求的核心页面",
        "observable_utg_signals": [
          "UI 层级中是否存在 Cancel/Skip/Back 等退出控件（预期缺失）",
          "按钮文本与 locale 的对应（Next/下一个/التالي）",
          "页面节点文本几乎为空而存在大面积 ImageView，说明文案在图片里",
          "Activity 名与 excludeFromRecents/label=\" \" 的空白标题特征"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility → Installed services 中的 “Blockchain” 条目，其描述显示为 \"...\"",
        "why_most_useful": "直接验证伪装身份与服务描述空白化，是识别身份混淆最有力的运行期证据",
        "observable_utg_signals": [
          "服务名文本 = Blockchain",
          "描述文本 = \"...\"（无实质说明）",
          "该条目所属包名 com.definitely.cell 与桌面名一致性"
        ]
      },
      {
        "page_role": "跳转后的系统无障碍开关页（直达组件）",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 页面，因 EXTRA_COMPONENT_NAME 指向 com.definitely.cell/…AccessService 而直接定位到本应用开关",
        "why_most_useful": "证明跳转不是泛化打开设置页，而是精确定位自身开关项，缩短用户操作路径、降低怀疑",
        "observable_utg_signals": [
          "页面直接落在本应用服务条目而非列表顶部",
          "Intent extra 中 EXTRA_COMPONENT_NAME 的值",
          "返回后引导页是否再次出现"
        ]
      },
      {
        "page_role": "冷启动自启动权限弹窗",
        "page_identifier": "MainActivity 上的 AlertDialog，标题为应用名，正文为“此应用程序请求自动启动和在后台运行权限才能正常工作”，仅一个 OK 按钮",
        "why_most_useful": "证明存在零可选性权限索取，且与后续无障碍引导构成连续施压链条",
        "observable_utg_signals": [
          "弹窗按钮数量（预期仅 1 个）",
          "正文语言随系统 locale 切换",
          "点击后是否立即进入图片引导页"
        ]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "主要盲区有三：1) 引导页正文以图片承载，纯文本 UTG 提取不到内容，必须 OCR 才能判断是否存在虚假安全承诺/恐吓话术；2) 冷启动前有 Anti_emu()/isEmu_DIV_ID_lator() 反模拟器分支，命中即 AsknoEmu 后 return，模拟器环境可能完全看不到引导链；3) 引导页的重复拉起依赖后台服务侧（utilities.Trys 语义未闭环），若仅做前台冷启动抓取，可能漏掉返回后的二次施压行为。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20#onCreate",
    "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.zgozvdaumbithjiidvaegtdxzaebjockkvfsyahfskbodtvjcj20$2#onClick",
    "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.MainActivity#onCreate",
    "com.definitely.ttxjwgufnyngkzawfubjkjorxxabsgsrkdfkbeiyakchqgvlym2.ikdveueesncetizdsovdwjoqijrojicxahikmgqliknocqeijk4.utilities#isAccessibilityServiceEnabled",
    "res/xml/accessdiecrip.xml",
    "res/values/strings.xml（key=Descrip、key=syracusedcentreso59）"
  ]
}
```

</details>
