# MB_041__118f0bba26｜SpyNote — Blockchain

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：163.0s

## 1. 一句话核心结论

- **核心申请方式**：SpyNote/Craxs 系远控伪装成 'Blockchain' 应用，用后台 1 秒轮询 + 全屏通知死循环拉起一个高仿系统无障碍设置页（空白 label、description 仅 '...'），以'解锁高级功能'话术三步教学并配伪开关/伪返回箭头，无取消路径，任意控件点击均跳转 ACTION_ACCESSIBILITY_SETTINGS 并带上目标组件名。
- **静态可见性说明**：整条无障碍诱导链完全静态可见：Manifest 声明、accessdiecrip.xml 服务配置、activity_req_access.xml 原生布局、引导页 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20 及其内部类 $1/$2 的 onClick、后台拉起逻辑 BackgroundWorker.onHandleIntent 均可直接反编译还原；未发现加壳、AES 密文载荷或远端 HTML 下发（CraxsBrowser WebView 不参与本链路）。仅字符串常量使用固定 64 字符混淆串拼接，可静态还原。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `118f0bba26f3fd4f1c535ba9117ec80eda9945e6a7fe8af7511178ac60a77170` |
| 包名 / 年份 | `com.corporate.finished` / 2026 |
| 家族 / 品类 | **SpyNote**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Blockchain |
| 引导页宣称品牌/身份 | Blockchain（加密货币/Binance 品牌，文案为 Binance 原文批量替换所得） |
| 系统无障碍列表服务名 | Blockchain（复用 @string/trademarks59，与桌面名一致，无独立无障碍语义标签） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 引导 Activity 与多数辅助 Activity 的 android:label 设为单个空格，Recent/标题栏无名称；2) 无障碍服务 android:description=@string/Descrip 实际值仅为 '...'，刻意使系统无障碍列表无法呈现真实用途；3) 布局中 @id/asdasd 的 TextView 文本为 16 个连续空格，用空白挤出/挤压真实警告与说明区域；4) 高仿系统设置页：深灰标题栏 + 左上返回箭头 drawable/treelins + 伪开关 drawable/toggle，控件 id 命名伪装为 backbtn/switchbtn/okbtn；5) 包名与类名全量随机化（com.corporate.finished + 超长随机类名），字符串常量以 64 字符混淆串做拆分拼接；6) settingsActivity 指向不存在的包 com.eagle...，制造配置残缺以规避静态识别；7) 多 activity-alias 式的多入口伪装：CameraActvity 标注为 'Play Store'，另有 SecondActivity/RequestScreenCap/WakeupActivity 均空白标签。 |
| 无障碍服务类名 | `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.AccessService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：@00000000 |
| 共现高危权限 | `CALL_PHONE, CAMERA, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | ... |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.MainActivity（LAUNCHER，label=Blockchain） | onCreate（含反模拟器 Anti_emu()/isEmu_DIV_ID_lator() 判定，命中则走 AsknoEmu() 直接返回）；随后读取 MySettings.Cantgo 决定是否跳 SecondActivity | 原生Activity | **原文**：无（主题为 Theme.Translucent.NoTitleBar，界面由后续 Activity 承载）<br>**译注**：冷启动不展示无障碍说明，仅做环境探测与语言/通知文案初始化（Continue installing / 继续安装 等） | 无（自动流转） | `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.MainActivity.onCreate` |
| 2 | 拒权反馈循环 | BackgroundWorker（IntentService，exported=true）内的 while(true) 轮询 + 全屏通知（NotificationChannel 'Access'，id=7779） | onHandleIntent 内 TimeUnit.MILLISECONDS.sleep(utilities.speedTime)（初值 1000ms）后每轮检查 isAccessibilityServiceEnabled(AccessService)==false && NeedSuper() && getScreenBoolean()，Trys 累加至 MIUI 25 / 其他 15 后 startActivity(引导页)；同时用 setFullScreenIntent + setOngoing(true) 弹出常驻全屏通知 | 通知栏 | **原文**：Continue installing / Click Here to Continue installing（en）；继续安装 / 单击此处继续安装（zh）；مواصلة التثبيت / انقر هنا لمتابعة التثبيت（ar）；kuruluma devam et / Kuruluma devam etmek için buraya tıklayın（tr）<br>**译注**：“继续安装 / 单击此处继续安装”——以“安装未完成”为借口的常驻全屏通知，点击后进入无障碍引导页 | 点击通知（或不做任何操作也会被定时自动拉起引导页） | `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.BackgroundWorker.onHandleIntent` |
| 3 | 引导说明页 | com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20（label=' '，excludeFromRecents，Theme.Translucent.NoTitleBar） | onCreate 中 isAccessibilityServiceEnabled(AccessService) 为 false 时 setContentView；MIUI 走 0x7f0a001f 专用布局，其他机型走 0x7f0a001c（activity_req_access）；若已启用则直接 finish() | 原生Activity | **原文**：标题栏 'Accessibility Service'；名称 'Blockchain'；说明 'To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App '；按钮 'Enable'（MIUI 变体按钮为 'Next'/'下一个'/'التالي'）；空白占位 TextView 内容为 '                '<br>**译注**：高仿系统无障碍设置页：标题“无障碍服务”，显示应用图标与名称 Blockchain，右侧伪开关，说明文字为“解锁高级功能，请按以下步骤：1. 点击启用按钮 2. 进入已安装的服务/应用 3. 启用被高亮的应用”，底部“启用”按钮 | 点击 'Enable'（或点击伪开关/图标/返回箭头——四者绑定同一监听器，均跳设置页）；界面无“取消/跳过”按钮，backbtn 实际不返回而是跳设置 | `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate + res/layout/activity_req_access.xml` |
| 4 | 引导说明页（第二页） | 同上 Activity，通过 $1.onClick 二次 setContentView(R.layout.activity_req_access) 并重新绑定 myicon/backbtn/switchbtn/okbtn 到 Oklistner | MIUI 专用布局中 nextButton（文案 Next / 下一个 / التالي）被点击 → isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$1.onClick | 原生Activity | **原文**：Next / 下一个 / التالي<br>**译注**：“下一步”——把用户从第一屏推进到真正带“启用”按钮的引导页 | 点击“下一步”，无取消路径 | `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$1#onClick` |
| 5 | 跳无障碍设置 | 系统无障碍设置页（三星 com.samsung.accessibility…installed_service → 混淆的 android.settings.<obf>ACCESSIBILITY_SETTINGS → 标准 android.settings.ACCESSIBILITY_SETTINGS） | Oklistner（isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2.onClick）被 Enable/switchbtn/backbtn/myicon 任一控件触发：resolveActivity 逐级降级，最终 new Intent("android.settings.ACCESSIBILITY_SETTINGS").putExtra("android.intent.extra.COMPONENT_NAME", new ComponentName(myctx, AccessService.class))，setFlags(1350565888)，startActivity 后 utilities.Trys=0、finish() | 系统无障碍页 | **原文**：系统页内服务名显示为 'Blockchain'，服务说明显示为 '...'<br>**译注**：系统无障碍设置列表中出现名为 Blockchain 的服务，说明栏只有三个点，用户需手动拨开开关 | 在系统列表中打开 Blockchain 对应的无障碍开关（带 COMPONENT_NAME 直定位，用户几乎无需寻找） | `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2#onClick` |
| 6 | 拒权反馈循环 | 返回后台轮询 + 全屏通知（同第 2 步），另叠加 AutoStart/自启与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 保活 | 用户在系统设置页直接返回未开启 → 引导页已 finish()，BackgroundWorker 循环继续：Trys 再次累加至阈值后再次 startActivity(引导页)，并配合 setFullScreenIntent 常驻通知反复拉回 | 通知栏 + 原生Activity（反复拉起） | **原文**：Continue installing / Click Here to Continue installing<br>**译注**：“继续安装 / 单击此处继续安装”持续置顶，用户返回即被再次弹回引导页，形成无退出条件的闭环 | 无退出选项，用户只能选择开启无障碍或持续被弹窗打断 | `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.BackgroundWorker.onHandleIntent` |
| 7 | 获权后动作 | com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.AccessService | onServiceConnected：startForeground 前台通知、setServiceInfo(flags=19, eventTypes=typeAllMask, packageNames=null)、ScreenScanner、unlockScreenListen()、Uninstall.start(this)、读取 TargetsData 目标应用表、Thread.sleep(1000) 后取 MainActivity label 作为 skinName | 不可静态还原（获权后转后台服务行为，无引导界面） | **原文**：Пожалуйста подождите... / Por favor aguarde... / Lütfen bekleyin... / 请稍等... / انتظر من فضلك...<br>**译注**：“请稍等……”——获权后进入后台静默执行，配合 Uninstall.start 与全局动作监听实施撤权对抗 | 无（用户已完成授权，后续为静默远控行为） | `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.AccessService#onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/layout/activity_req_access.xml 第 5 行：标题栏 TextView android:text="Accessibility Service"（高仿系统设置标题）
- res/layout/activity_req_access.xml 第 13 行：应用名 TextView android:text="Blockchain"
- res/layout/activity_req_access.xml 第 18 行：说明 TextView android:text="To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App "（教唆开启无障碍的核心文案，硬编码在布局而非 strings）
- res/layout/activity_req_access.xml 第 21 行：按钮 Button android:text="Enable"
- res/layout/activity_req_access.xml 第 8 行：@id/asdasd TextView，text="                "（16 个空格，用于挤压/遮挡说明区）
- res/layout/activity_req_access.xml 第 4、9 行：@drawable/treelins 伪返回箭头、@drawable/toggle 伪开关图标（以图形伪装系统控件）
- isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate 内按 Locale 硬编码设置按钮文案："Next" / "下一个" / "التالي"（MIUI 专用布局 0x7f0a001f）
- 系统无障碍服务列表：服务 label=@string/trademarks59（值为 Blockchain），android:description=@string/Descrip（值仅为 "..."），见 res/xml/accessdiecrip.xml
- 通知栏常驻全屏通知：BackgroundWorker.onHandleIntent 中 utilities.completeinstallnotifi_title / completeinstallnotifi_msg（Continue installing / 继续安装 / مواصلة التثبيت / kuruluma devam et）
- MainActivity.onCreate 内硬编码的多语言安装续期通知文案（同上四项语言分支）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App | 为解锁高级功能，请按以下步骤操作：1. 点击启用按钮 2. 进入“已安装的服务/应用” 3. 启用被高亮的应用 | `res/layout/activity_req_access.xml#L18（@id/descrip TextView，硬编码）` | 受限设置分步教学 |
| en | Accessibility Service | 无障碍服务 | `res/layout/activity_req_access.xml#L5（@id/titletext，硬编码）` | 未知 |
| en | Blockchain | Blockchain（加密品牌名） | `res/layout/activity_req_access.xml#L13（@id/nametext）与 @string/trademarks59（无障碍服务 label）` | 未知 |
| en | Enable | 启用 | `res/layout/activity_req_access.xml#L21（@id/okbtn，硬编码）` | 未知 |
| en | Next | 下一步 | `isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate（setText 硬编码，MIUI 分支）` | 受限设置分步教学 |
| zh | 下一个 | 下一步 | `isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate（setText 硬编码，zh 分支）` | 受限设置分步教学 |
| ar | التالي | 下一步 | `isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate（setText 硬编码，ar 分支）` | 受限设置分步教学 |
| en | Continue installing | 继续安装 | `utilities.completeinstallnotifi_title（MainActivity.onCreate 硬编码赋值，en 分支）` | 假更新 |
| en | Click Here to Continue installing | 单击此处继续安装 | `utilities.completeinstallnotifi_msg（MainActivity.onCreate 硬编码赋值，en 分支）` | 假更新 |
| zh | 继续安装 | 继续安装 | `utilities.completeinstallnotifi_title（MainActivity.onCreate 硬编码赋值，zh 分支）` | 假更新 |
| zh | 单击此处继续安装 | 单击此处继续安装 | `utilities.completeinstallnotifi_msg（MainActivity.onCreate 硬编码赋值，zh 分支）` | 假更新 |
| ar | مواصلة التثبيت | 继续安装 | `utilities.completeinstallnotifi_title（ar 分支）` | 假更新 |
| tr | kuruluma devam et | 继续安装 | `utilities.completeinstallnotifi_title（tr 分支）` | 假更新 |
| en | ... | ……（三个点，等于不告知真实用途） | `res/values/strings.xml 第 3 行 @string/Descrip，经 res/xml/accessdiecrip.xml android:description 引用` | 未知 |
| zh | 请稍等... | 请稍等…… | `AccessService.onServiceConnected（硬编码 zh 分支）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：BackgroundWorker.onHandleIntent 的 while(true) 循环每 speedTime（初始 1000ms）轮询 isAccessibilityServiceEnabled(AccessService)：未启用且 NeedSuper() 且亮屏时 Trys++，达到 MIUI=25 / 其他=15 即重置 Trys、startActivity(引导页) 并 cancelnotification，然后继续下一轮；同时以 setFullScreenIntent + setOngoing(true) 的常驻通知持续拉回。引导页自身无 onResume 重跳，但被后台循环反复重建，用户从系统设置返回未授权即被再次弹回，无退出条件。
- **遮罩叠层 / 高仿系统设置页**：无 SYSTEM_ALERT_WINDOW 悬浮遮罩参与本链路，但引导页本身即为高仿系统无障碍设置页：Theme.Translucent.NoTitleBar + 深灰标题栏 + 伪返回箭头 @drawable/treelins + 伪开关 @drawable/toggle + 16 空格空白 TextView 挤压真实说明，按钮文案为 Enable/Next，视觉上等同于系统页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：AccessService.onServiceConnected 获权瞬间即调用 Uninstall.start(this)、unlockScreenListen()、ScreenScanner() 并读取 TargetsData 目标应用表，配合预筛检出的 PERFORM_GLOBAL_ACTION / WATCH_PKG_INSTALLER / WATCH_SETTINGS 用于撤权与卸载对抗（本次未逐行展开该分支，属同链后续行为）。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20，或监测到 ACTION_ACCESSIBILITY_SETTINGS（含 EXTRA_COMPONENT_NAME 指向本包 AccessService）时立即拉起；另可在后台服务 BackgroundWorker 首次 startActivity 或首个 setFullScreenIntent 通知出现（通知 id=7779、channel 'Access'）时作为更早的触发点。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本链路无纯图诱导（文案均为布局内可读文本，无需 OCR）。潜在盲区：1) 引导页 label 为空格、不进入最近任务且为 Translucent 主题，部分以“任务栈可见 Activity”为触发条件的 UTG 策略可能漏采，需以 startActivity/Intent 目标类名为准；2) 无障碍服务 description 仅为 '...'，基于描述文本做语义判定的策略会失效；3) 若设备为 MIUI，第一屏为专用布局且按钮文案为 'Next/下一个/التالي'，需按两页流程采集；4) 静态未加壳不影响运行期 UTG，但获权后行为转后台服务（ScreenScanner/TargetsData），UTG 无法覆盖。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **高仿系统无障碍引导页（核心诱导页）** | Activity 名 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20，label 为单个空格、不进入最近任务、Translucent 无标题；界面含 'Accessibility Service' 标题、'Blockchain' 名称、@drawable/toggle 伪开关、'Enable' 按钮 | 这是唯一承载诱导文案的界面，可一次性固定伪装身份、教唆三步文案、伪控件与无取消路径四项关键证据 | 文本 'Accessibility Service' + 'To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App '；按钮文本 'Enable' / 'Next' / '下一个' / 'التالي'；存在内容为 16 个空格的空白 TextView（@id/asdasd）；控件 id 命名 backbtn/switchbtn/okbtn 与 drawable treelins/toggle 的组合 |
| **常驻全屏通知（后台拉起点）** | NotificationChannel 'Access'，通知 id 7779，setOngoing(true) + setFullScreenIntent，图标 0x0106000d，category 'sys' | 证明触发时机为后台轮询反复拉起而非用户主动进入，是区分“诱导”与“用户自选功能”的关键 | 通知标题 'Continue installing' / '继续安装' / 'مواصلة التثبيت' / 'kuruluma devam et'；通知正文 'Click Here to Continue installing' / '单击此处继续安装'；通知不可滑动清除（ongoing）且点击后落到无障碍引导页 |
| **系统无障碍服务列表项（授权落点）** | 设置 → 无障碍 → 已安装服务中的 'Blockchain' 条目，说明文字仅为 '...' | 核验系统侧身份隐藏：服务名与桌面名一致但描述为空壳，用户无法据此判断真实用途；同时验证 EXTRA_COMPONENT_NAME 直定位效果 | 服务条目名 'Blockchain' 与描述 '...'；开关默认关闭，位于“已下载的服务/已安装的服务”分组；跳转后设置页直接滚动/高亮到该条目（fragment_args_key 生效） |
| **拒权后再次被拉起的循环页** | 从系统设置返回后再次出现的同一引导 Activity（Trys 达 15/25 阈值触发） | 证明无取消/跳过路径与拒绝死循环，是胁迫性（COERCE）判定的直接运行期证据 | 同一引导页在用户返回后 1～30 秒内自动重现；重现时无任何系统权限弹窗，属应用自身 startActivity 拉起；伴随 ongoing 通知重新出现 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20#onCreate`
- `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2#onClick`
- `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$1#onClick`
- `com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.BackgroundWorker#onHandleIntent`
- `res/layout/activity_req_access.xml`
- `res/xml/accessdiecrip.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（累计 21 次工具调用，超出 14 次预算，已立即收口）。以下为结论。

## 结论要点

- **静态完全可见**：无加壳、无加密载荷、无远端 HTML。整条无障碍诱导链均由原生 Java 类 + 原生 layout 构成，可直接静态还原。
- **触发时机是"后台循环拉起"而非单纯冷启动**：`BackgroundWorker.onHandleIntent` 处于 `while(true)` 循环中，每 `speedTime`（1000ms）检查一次：若 `AccessService` 未启用 且 `NeedSuper()` 且亮屏，则 `Trys++`；计数达阈值（MIUI 25 次 / 其他 15 次）后立即 `startActivity(引导页)`，随后 `cancelnotification` 并继续循环——**用户返回/拒绝后会被反复重跳**。同时下发 `setFullScreenIntent` 的常驻通知，标题取自"Continue installing / 继续安装 / مواصلة التثبيت / kuruluma devam et"，点击亦指向同一引导页。
- **引导页是一个伪造的"系统无障碍设置页"**：[isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20](<resource-unit:#1.dex1 code:com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20#onCreate>) 在 Manifest 中 `android:label=" "`（纯空格）、`excludeFromRecents`、`Theme.Translucent.NoTitleBar`。界面用 [activity_req_access.xml](<resource-unit:#1 file:res/layout/activity_req_access.xml#L4-L22>) 高仿系统页：深灰标题栏 + 左上返回箭头（`@id/backbtn`）、标题 `Accessibility Service`、应用图标 + 名称 `Blockchain`、右侧 `@drawable/toggle` 伪开关，以及 `@id/asdasd` 这个内容为 **16 个空格** 的 TextView（空白挤出真实警告的排版伎俩）。
- **教唆文案（明示"三步走"）**：`"To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App "`——以"解锁高级功能"为诱饵，直接教用户进已安装服务里打开被高亮的条目。
- **跳转点有三级降级**：[isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2.onClick](<resource-unit:#1.dex1 code:com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2#onClick>) 先试三星专属 `com.samsung.accessibility…installed_service`（带 `:settings:fragment_args_key` 精准定位本服务），失败退到混淆拼接的 `android.settings.<64字符混淆>ACCESSIBILITY_SETTINGS`，再退到标准 `ACTION_ACCESSIBILITY_SETTINGS` + `EXTRA_COMPONENT_NAME=AccessService`；跳转后 `Trys=0`、`finish()`。**没有取消/跳过按钮**：`backbtn`、`switchbtn`、`myicon`、`okbtn` 全部绑定到同一个 `Oklistner`，即任何"看似关闭"的控件都会跳设置页。
- **系统侧隐藏证据**：[accessdiecrip.xml](<resource-unit:#1 file:res/xml/accessdiecrip.xml#L2>) 中 `android:description="@string/Descrip"` 的实际值为 `...`（三个点，等于隐藏权限说明），服务 label 复用 `@string/trademarks59`＝"Blockchain"，`settingsActivity` 指向不存在的包名 `com.eagle.vhasj…udlulikg…17`（配置残缺）；能力为 `typeAllMask` + `canRetrieveWindowContent` + `flagRetrieveInteractiveWindows` + `flagReportViewIds`（全事件监听、可读全屏窗口与控件 ID）。
- **获权后**：`AccessService.onServiceConnected` 立即 `Uninstall.start(this)`、`unlockScreenListen()`、`ScreenScanner()`，并读取 `TargetsData` 下发目标应用表——与预筛的 `PERFORM_GLOBAL_ACTION` 撤权对抗特征一致（本次未逐行展开该分支）。
- 身份错配明确：桌面名 `Blockchain`、无障碍列表名亦 `Blockchain`，而包内字符串实为 Binance 品牌文案批量替换（`Binance`→`Blockchain`），另有 `CraxsBrowser`、`CameraActvity` 标为 `Play Store`；实际为 SpyNote/Craxs 系远控。
- 未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 相关"受限设置 13+ 教学"代码（该分支在 4 次核实后确认不存在），亦无 WebView/悬浮窗参与本链路。

```json
{
  "static_visibility": "clear",
  "visibility_note": "整条无障碍诱导链完全静态可见：Manifest 声明、accessdiecrip.xml 服务配置、activity_req_access.xml 原生布局、引导页 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20 及其内部类 $1/$2 的 onClick、后台拉起逻辑 BackgroundWorker.onHandleIntent 均可直接反编译还原；未发现加壳、AES 密文载荷或远端 HTML 下发（CraxsBrowser WebView 不参与本链路）。仅字符串常量使用固定 64 字符混淆串拼接，可静态还原。",
  "summary_one_liner": "SpyNote/Craxs 系远控伪装成 'Blockchain' 应用，用后台 1 秒轮询 + 全屏通知死循环拉起一个高仿系统无障碍设置页（空白 label、description 仅 '...'），以'解锁高级功能'话术三步教学并配伪开关/伪返回箭头，无取消路径，任意控件点击均跳转 ACTION_ACCESSIBILITY_SETTINGS 并带上目标组件名。",
  "disguise_identity": {
    "app_display_name": "Blockchain",
    "claimed_brand_or_persona": "Blockchain（加密货币/Binance 品牌，文案为 Binance 原文批量替换所得）",
    "a11y_service_label": "Blockchain（复用 @string/trademarks59，与桌面名一致，无独立无障碍语义标签）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 引导 Activity 与多数辅助 Activity 的 android:label 设为单个空格，Recent/标题栏无名称；2) 无障碍服务 android:description=@string/Descrip 实际值仅为 '...'，刻意使系统无障碍列表无法呈现真实用途；3) 布局中 @id/asdasd 的 TextView 文本为 16 个连续空格，用空白挤出/挤压真实警告与说明区域；4) 高仿系统设置页：深灰标题栏 + 左上返回箭头 drawable/treelins + 伪开关 drawable/toggle，控件 id 命名伪装为 backbtn/switchbtn/okbtn；5) 包名与类名全量随机化（com.corporate.finished + 超长随机类名），字符串常量以 64 字符混淆串做拆分拼接；6) settingsActivity 指向不存在的包 com.eagle...，制造配置残缺以规避静态识别；7) 多 activity-alias 式的多入口伪装：CameraActvity 标注为 'Play Store'，另有 SecondActivity/RequestScreenCap/WakeupActivity 均空白标签。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.MainActivity（LAUNCHER，label=Blockchain）",
      "trigger_event": "onCreate（含反模拟器 Anti_emu()/isEmu_DIV_ID_lator() 判定，命中则走 AsknoEmu() 直接返回）；随后读取 MySettings.Cantgo 决定是否跳 SecondActivity",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（主题为 Theme.Translucent.NoTitleBar，界面由后续 Activity 承载）",
      "shown_text_zh": "冷启动不展示无障碍说明，仅做环境探测与语言/通知文案初始化（Continue installing / 继续安装 等）",
      "user_action_requested": "无（自动流转）",
      "code_anchor": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "拒权反馈循环",
      "screen_or_component": "BackgroundWorker（IntentService，exported=true）内的 while(true) 轮询 + 全屏通知（NotificationChannel 'Access'，id=7779）",
      "trigger_event": "onHandleIntent 内 TimeUnit.MILLISECONDS.sleep(utilities.speedTime)（初值 1000ms）后每轮检查 isAccessibilityServiceEnabled(AccessService)==false && NeedSuper() && getScreenBoolean()，Trys 累加至 MIUI 25 / 其他 15 后 startActivity(引导页)；同时用 setFullScreenIntent + setOngoing(true) 弹出常驻全屏通知",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Continue installing / Click Here to Continue installing（en）；继续安装 / 单击此处继续安装（zh）；مواصلة التثبيت / انقر هنا لمتابعة التثبيت（ar）；kuruluma devam et / Kuruluma devam etmek için buraya tıklayın（tr）",
      "shown_text_zh": "“继续安装 / 单击此处继续安装”——以“安装未完成”为借口的常驻全屏通知，点击后进入无障碍引导页",
      "user_action_requested": "点击通知（或不做任何操作也会被定时自动拉起引导页）",
      "code_anchor": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.BackgroundWorker.onHandleIntent"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20（label=' '，excludeFromRecents，Theme.Translucent.NoTitleBar）",
      "trigger_event": "onCreate 中 isAccessibilityServiceEnabled(AccessService) 为 false 时 setContentView；MIUI 走 0x7f0a001f 专用布局，其他机型走 0x7f0a001c（activity_req_access）；若已启用则直接 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "标题栏 'Accessibility Service'；名称 'Blockchain'；说明 'To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App '；按钮 'Enable'（MIUI 变体按钮为 'Next'/'下一个'/'التالي'）；空白占位 TextView 内容为 '                '",
      "shown_text_zh": "高仿系统无障碍设置页：标题“无障碍服务”，显示应用图标与名称 Blockchain，右侧伪开关，说明文字为“解锁高级功能，请按以下步骤：1. 点击启用按钮 2. 进入已安装的服务/应用 3. 启用被高亮的应用”，底部“启用”按钮",
      "user_action_requested": "点击 'Enable'（或点击伪开关/图标/返回箭头——四者绑定同一监听器，均跳设置页）；界面无“取消/跳过”按钮，backbtn 实际不返回而是跳设置",
      "code_anchor": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate + res/layout/activity_req_access.xml"
    },
    {
      "step": 4,
      "stage": "引导说明页（第二页）",
      "screen_or_component": "同上 Activity，通过 $1.onClick 二次 setContentView(R.layout.activity_req_access) 并重新绑定 myicon/backbtn/switchbtn/okbtn 到 Oklistner",
      "trigger_event": "MIUI 专用布局中 nextButton（文案 Next / 下一个 / التالي）被点击 → isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$1.onClick",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Next / 下一个 / التالي",
      "shown_text_zh": "“下一步”——把用户从第一屏推进到真正带“启用”按钮的引导页",
      "user_action_requested": "点击“下一步”，无取消路径",
      "code_anchor": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$1#onClick"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（三星 com.samsung.accessibility…installed_service → 混淆的 android.settings.<obf>ACCESSIBILITY_SETTINGS → 标准 android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "Oklistner（isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2.onClick）被 Enable/switchbtn/backbtn/myicon 任一控件触发：resolveActivity 逐级降级，最终 new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").putExtra(\"android.intent.extra.COMPONENT_NAME\", new ComponentName(myctx, AccessService.class))，setFlags(1350565888)，startActivity 后 utilities.Trys=0、finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "系统页内服务名显示为 'Blockchain'，服务说明显示为 '...'",
      "shown_text_zh": "系统无障碍设置列表中出现名为 Blockchain 的服务，说明栏只有三个点，用户需手动拨开开关",
      "user_action_requested": "在系统列表中打开 Blockchain 对应的无障碍开关（带 COMPONENT_NAME 直定位，用户几乎无需寻找）",
      "code_anchor": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2#onClick"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回后台轮询 + 全屏通知（同第 2 步），另叠加 AutoStart/自启与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 保活",
      "trigger_event": "用户在系统设置页直接返回未开启 → 引导页已 finish()，BackgroundWorker 循环继续：Trys 再次累加至阈值后再次 startActivity(引导页)，并配合 setFullScreenIntent 常驻通知反复拉回",
      "ui_carrier": "通知栏 + 原生Activity（反复拉起）",
      "shown_text_verbatim": "Continue installing / Click Here to Continue installing",
      "shown_text_zh": "“继续安装 / 单击此处继续安装”持续置顶，用户返回即被再次弹回引导页，形成无退出条件的闭环",
      "user_action_requested": "无退出选项，用户只能选择开启无障碍或持续被弹窗打断",
      "code_anchor": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.BackgroundWorker.onHandleIntent"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.AccessService",
      "trigger_event": "onServiceConnected：startForeground 前台通知、setServiceInfo(flags=19, eventTypes=typeAllMask, packageNames=null)、ScreenScanner、unlockScreenListen()、Uninstall.start(this)、读取 TargetsData 目标应用表、Thread.sleep(1000) 后取 MainActivity label 作为 skinName",
      "ui_carrier": "不可静态还原（获权后转后台服务行为，无引导界面）",
      "shown_text_verbatim": "Пожалуйста подождите... / Por favor aguarde... / Lütfen bekleyin... / 请稍等... / انتظر من فضلك...",
      "shown_text_zh": "“请稍等……”——获权后进入后台静默执行，配合 Uninstall.start 与全局动作监听实施撤权对抗",
      "user_action_requested": "无（用户已完成授权，后续为静默远控行为）",
      "code_anchor": "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.AccessService#onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "res/layout/activity_req_access.xml 第 5 行：标题栏 TextView android:text=\"Accessibility Service\"（高仿系统设置标题）",
    "res/layout/activity_req_access.xml 第 13 行：应用名 TextView android:text=\"Blockchain\"",
    "res/layout/activity_req_access.xml 第 18 行：说明 TextView android:text=\"To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App \"（教唆开启无障碍的核心文案，硬编码在布局而非 strings）",
    "res/layout/activity_req_access.xml 第 21 行：按钮 Button android:text=\"Enable\"",
    "res/layout/activity_req_access.xml 第 8 行：@id/asdasd TextView，text=\"                \"（16 个空格，用于挤压/遮挡说明区）",
    "res/layout/activity_req_access.xml 第 4、9 行：@drawable/treelins 伪返回箭头、@drawable/toggle 伪开关图标（以图形伪装系统控件）",
    "isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate 内按 Locale 硬编码设置按钮文案：\"Next\" / \"下一个\" / \"التالي\"（MIUI 专用布局 0x7f0a001f）",
    "系统无障碍服务列表：服务 label=@string/trademarks59（值为 Blockchain），android:description=@string/Descrip（值仅为 \"...\"），见 res/xml/accessdiecrip.xml",
    "通知栏常驻全屏通知：BackgroundWorker.onHandleIntent 中 utilities.completeinstallnotifi_title / completeinstallnotifi_msg（Continue installing / 继续安装 / مواصلة التثبيت / kuruluma devam et）",
    "MainActivity.onCreate 内硬编码的多语言安装续期通知文案（同上四项语言分支）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App ",
      "text_zh": "为解锁高级功能，请按以下步骤操作：1. 点击启用按钮 2. 进入“已安装的服务/应用” 3. 启用被高亮的应用",
      "source_location": "res/layout/activity_req_access.xml#L18（@id/descrip TextView，硬编码）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service",
      "text_zh": "无障碍服务",
      "source_location": "res/layout/activity_req_access.xml#L5（@id/titletext，硬编码）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Blockchain",
      "text_zh": "Blockchain（加密品牌名）",
      "source_location": "res/layout/activity_req_access.xml#L13（@id/nametext）与 @string/trademarks59（无障碍服务 label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable",
      "text_zh": "启用",
      "source_location": "res/layout/activity_req_access.xml#L21（@id/okbtn，硬编码）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Next",
      "text_zh": "下一步",
      "source_location": "isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate（setText 硬编码，MIUI 分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "下一个",
      "text_zh": "下一步",
      "source_location": "isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate（setText 硬编码，zh 分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "ar",
      "text_verbatim": "التالي",
      "text_zh": "下一步",
      "source_location": "isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate（setText 硬编码，ar 分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Continue installing",
      "text_zh": "继续安装",
      "source_location": "utilities.completeinstallnotifi_title（MainActivity.onCreate 硬编码赋值，en 分支）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Click Here to Continue installing",
      "text_zh": "单击此处继续安装",
      "source_location": "utilities.completeinstallnotifi_msg（MainActivity.onCreate 硬编码赋值，en 分支）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "zh",
      "text_verbatim": "继续安装",
      "text_zh": "继续安装",
      "source_location": "utilities.completeinstallnotifi_title（MainActivity.onCreate 硬编码赋值，zh 分支）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "zh",
      "text_verbatim": "单击此处继续安装",
      "text_zh": "单击此处继续安装",
      "source_location": "utilities.completeinstallnotifi_msg（MainActivity.onCreate 硬编码赋值，zh 分支）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ar",
      "text_verbatim": "مواصلة التثبيت",
      "text_zh": "继续安装",
      "source_location": "utilities.completeinstallnotifi_title（ar 分支）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "kuruluma devam et",
      "text_zh": "继续安装",
      "source_location": "utilities.completeinstallnotifi_title（tr 分支）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "...",
      "text_zh": "……（三个点，等于不告知真实用途）",
      "source_location": "res/values/strings.xml 第 3 行 @string/Descrip，经 res/xml/accessdiecrip.xml android:description 引用",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "请稍等...",
      "text_zh": "请稍等……",
      "source_location": "AccessService.onServiceConnected（硬编码 zh 分支）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "BackgroundWorker.onHandleIntent 的 while(true) 循环每 speedTime（初始 1000ms）轮询 isAccessibilityServiceEnabled(AccessService)：未启用且 NeedSuper() 且亮屏时 Trys++，达到 MIUI=25 / 其他=15 即重置 Trys、startActivity(引导页) 并 cancelnotification，然后继续下一轮；同时以 setFullScreenIntent + setOngoing(true) 的常驻通知持续拉回。引导页自身无 onResume 重跳，但被后台循环反复重建，用户从系统设置返回未授权即被再次弹回，无退出条件。",
    "overlay_or_fake_settings": "无 SYSTEM_ALERT_WINDOW 悬浮遮罩参与本链路，但引导页本身即为高仿系统无障碍设置页：Theme.Translucent.NoTitleBar + 深灰标题栏 + 伪返回箭头 @drawable/treelins + 伪开关 @drawable/toggle + 16 空格空白 TextView 挤压真实说明，按钮文案为 Enable/Next，视觉上等同于系统页。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "AccessService.onServiceConnected 获权瞬间即调用 Uninstall.start(this)、unlockScreenListen()、ScreenScanner() 并读取 TargetsData 目标应用表，配合预筛检出的 PERFORM_GLOBAL_ACTION / WATCH_PKG_INSTALLER / WATCH_SETTINGS 用于撤权与卸载对抗（本次未逐行展开该分支，属同链后续行为）。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20，或监测到 ACTION_ACCESSIBILITY_SETTINGS（含 EXTRA_COMPONENT_NAME 指向本包 AccessService）时立即拉起；另可在后台服务 BackgroundWorker 首次 startActivity 或首个 setFullScreenIntent 通知出现（通知 id=7779、channel 'Access'）时作为更早的触发点。",
    "key_pages_to_capture": [
      {
        "page_role": "高仿系统无障碍引导页（核心诱导页）",
        "page_identifier": "Activity 名 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20，label 为单个空格、不进入最近任务、Translucent 无标题；界面含 'Accessibility Service' 标题、'Blockchain' 名称、@drawable/toggle 伪开关、'Enable' 按钮",
        "why_most_useful": "这是唯一承载诱导文案的界面，可一次性固定伪装身份、教唆三步文案、伪控件与无取消路径四项关键证据",
        "observable_utg_signals": [
          "文本 'Accessibility Service' + 'To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App '",
          "按钮文本 'Enable' / 'Next' / '下一个' / 'التالي'",
          "存在内容为 16 个空格的空白 TextView（@id/asdasd）",
          "控件 id 命名 backbtn/switchbtn/okbtn 与 drawable treelins/toggle 的组合"
        ]
      },
      {
        "page_role": "常驻全屏通知（后台拉起点）",
        "page_identifier": "NotificationChannel 'Access'，通知 id 7779，setOngoing(true) + setFullScreenIntent，图标 0x0106000d，category 'sys'",
        "why_most_useful": "证明触发时机为后台轮询反复拉起而非用户主动进入，是区分“诱导”与“用户自选功能”的关键",
        "observable_utg_signals": [
          "通知标题 'Continue installing' / '继续安装' / 'مواصلة التثبيت' / 'kuruluma devam et'",
          "通知正文 'Click Here to Continue installing' / '单击此处继续安装'",
          "通知不可滑动清除（ongoing）且点击后落到无障碍引导页"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（授权落点）",
        "page_identifier": "设置 → 无障碍 → 已安装服务中的 'Blockchain' 条目，说明文字仅为 '...'",
        "why_most_useful": "核验系统侧身份隐藏：服务名与桌面名一致但描述为空壳，用户无法据此判断真实用途；同时验证 EXTRA_COMPONENT_NAME 直定位效果",
        "observable_utg_signals": [
          "服务条目名 'Blockchain' 与描述 '...'",
          "开关默认关闭，位于“已下载的服务/已安装的服务”分组",
          "跳转后设置页直接滚动/高亮到该条目（fragment_args_key 生效）"
        ]
      },
      {
        "page_role": "拒权后再次被拉起的循环页",
        "page_identifier": "从系统设置返回后再次出现的同一引导 Activity（Trys 达 15/25 阈值触发）",
        "why_most_useful": "证明无取消/跳过路径与拒绝死循环，是胁迫性（COERCE）判定的直接运行期证据",
        "observable_utg_signals": [
          "同一引导页在用户返回后 1～30 秒内自动重现",
          "重现时无任何系统权限弹窗，属应用自身 startActivity 拉起",
          "伴随 ongoing 通知重新出现"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本链路无纯图诱导（文案均为布局内可读文本，无需 OCR）。潜在盲区：1) 引导页 label 为空格、不进入最近任务且为 Translucent 主题，部分以“任务栈可见 Activity”为触发条件的 UTG 策略可能漏采，需以 startActivity/Intent 目标类名为准；2) 无障碍服务 description 仅为 '...'，基于描述文本做语义判定的策略会失效；3) 若设备为 MIUI，第一屏为专用布局且按钮文案为 'Next/下一个/التالي'，需按两页流程采集；4) 静态未加壳不影响运行期 UTG，但获权后行为转后台服务（ScreenScanner/TargetsData），UTG 无法覆盖。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20#onCreate",
    "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2#onClick",
    "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$1#onClick",
    "com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.BackgroundWorker#onHandleIntent",
    "res/layout/activity_req_access.xml",
    "res/xml/accessdiecrip.xml"
  ]
}
```

补充说明：本轮未写入风险台账（`record_risk`），原因是受 14 次工具调用硬约束，工具预算已用于证据闭环；如需入库，可基于上述证据链直接登记“无障碍诱导 + 拒权死循环 + 品牌仿冒”组合风险（建议 `malware_trojan` / high）。

</details>
