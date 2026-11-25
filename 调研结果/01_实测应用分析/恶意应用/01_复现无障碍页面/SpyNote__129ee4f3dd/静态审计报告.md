# MB_040__129ee4f3dd｜SpyNote — nered

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：155.4s

## 1. 一句话核心结论

- **核心申请方式**：应用以「解锁高级功能」为诱饵，后台反复弹起一个高仿系统无障碍设置页（假顶栏+假开关+Enable 按钮），点按后直跳系统无障碍设置并指定自身服务，同时把服务名与描述伪造成不可读的 DEL 控制字符与「...」，形成拒权后重跳的死循环。
- **静态可见性说明**：未加壳（apkid 初判 False）。无障碍服务声明、引导布局、跳转 Intent 与后台拉起逻辑均完整静态可见；仅部分字符串用 stuoxctjtdaoeuivbicuhkpiflkolbbmlmpdazwmgcmmbmmdif53 做混淆拼接（如 android.settings.ACCESSIBILITY_SETTINGS、com.samsung.accessibility...installed_service），可通过反编译直接还原明文。远端 WebView 内容（FloatingView/CraxsBrowser 承载的钓鱼页）属另一条业务链，与本无障碍诱导链无关。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `129ee4f3dd5ecd07a3f815616300a2adcd6702239c1ae3e31a3d61cf7913c4cb` |
| 包名 / 年份 | `com.duke.centers` / 2026 |
| 家族 / 品类 | **SpyNote**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | nered |
| 引导页宣称品牌/身份 | 伪装为系统级「Accessibility Service / 已安装服务」设置界面，并以「premium feature 解锁」名义自称增值服务提供方 |
| 系统无障碍列表服务名 | nered（取自 @string/trademarks59，实为 DEL 控制字符 0x7F + "nered"；android:description = "..."） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 应用名、无障碍服务名均以 DEL(0x7F) 控制字符开头，在系统无障碍列表/授权弹窗中渲染为空白或乱码，用户无法识别；2) android:description 仅为 "..."，隐藏真实用途；3) 引导 Activity 的 android:label 设为单个空格；4) 引导页自绘顶栏「Accessibility Service」+ 返回箭头 + 假 toggle 开关，全屏仿系统设置页；5) MIUI 分支用预置背景图 @drawable/en_access 做分步截图教学；6) 引导 Activity 类名整段随机化（isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20），且 excludeFromRecents=true 不在最近任务中留痕；7) 跳转后立即 finish() 自身，避免用户回退发现。 |
| 无障碍服务类名 | `com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.AccessService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：@00000000 |
| 共现高危权限 | `CALL_PHONE, CAMERA, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | ... |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.MainActivity（LAUNCHER，Theme.Translucent.NoTitleBar） | onCreate：先 utilities.Anti_emu()/isEmu_DIV_ID_lator() 模拟器检测（命中则 AsknoEmu 并 return），随后按 Locale 设置安装通知文案、utilities.SetJob 注册 Job、按 NeedAutoStart 弹自启动权限 AlertDialog、Settings.canDrawOverlays 判断悬浮窗授权 | 原生Activity + 原生Dialog | **原文**：this App request Auto Start/Run in Background Permission to work properly（标题取自 R.string，图标为应用图标，仅 OK/好的/Tamam/موافق 一个按钮）<br>**译注**：本应用需要自启动/后台运行权限才能正常工作（仅一个确认按钮，无拒绝选项） | 仅可点击「OK」；无拒绝/跳过按钮，点后进入系统自启动设置 | `MainActivity.onCreate / MainActivity$7` |
| 2 | 后台拉起引导页 | com.duke...isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20（exported=true、excludeFromRecents=true、label=" "、Translucent） | BackgroundWorker.onHandleIntent 与 lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38$_srv_worker_con_#doInBackground 中 startActivity(new Intent(ctx, 该Activity.class).addFlags(NEW_TASK).addFlags(NEW_TASK)) | 原生Activity（后台强制压栈弹出，非用户主动点击） | **原文**：无（启动行为本身无文案）<br>**译注**：无 | 无（被动弹出，用户被强行带到下一步界面） | `BackgroundWorker.onHandleIntent / tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38$_srv_worker_con_#doInBackground` |
| 3 | 引导说明页（仿系统设置页） | 同一 Activity，onCreate 首行 utilities.isAccessibilityServiceEnabled(this, AccessService.class)==false 时 setContentView(R.layout.activity_req_access) | onCreate 检测无障碍未启用 | 原生Activity（自绘全屏页面，仿系统设置界面） | **原文**：Accessibility Service / nered / To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App / Enable<br>**译注**：顶栏「无障碍服务」；应用名显示为不可读控制字符 nered；正文「要解锁高级功能，请按以下步骤：1. 点击启用按钮 2. 前往『已安装的服务/应用』 3. 开启高亮的那个应用」；底部按钮「启用」 | 点击底部 Enable 按钮（无取消、无跳过、无稍后按钮，仅系统返回键可退出） | `isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate → res/layout/activity_req_access.xml` |
| 4 | 引导说明页（MIUI 变体，截图分步教学） | 同一 Activity，utilities.isMIUI(ctx)==true 时 setContentView(R.layout.miui_access_act) | onCreate 检测到 MIUI 机型 | 原生Activity（全屏预置背景图 + 单按钮） | **原文**：Next / 下一个 / التالي（按钮文案随语言切换，主体内容为 @drawable/en_access 背景图）<br>**译注**：「下一步」（页面主体是一张事先做好的分步操作截图，教用户如何在 MIUI 中开启无障碍） | 点击 Next 按钮继续（无取消/跳过） | `isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate → res/layout/miui_access_act.xml / @drawable/en_access` |
| 5 | 跳无障碍设置（含受限设置教学深链） | 系统无障碍设置页：com.samsung.accessibility...installed_service → android.settings.ACCESSIBILITY_SETTINGS（带 EXTRA_COMPONENT_NAME=AccessService）→ Settings 深链 :settings:fragment_args_key / :settings:show_fragment_args | 点击 Enable/Next 触发 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2.onClick | 系统无障碍页（Intent 三级 fallback，跳转后调用 finish() 关闭自身） | **原文**：android.settings.ACCESSIBILITY_SETTINGS / android.intent.extra.COMPONENT_NAME / :settings:fragment_args_key / :settings:show_fragment_args<br>**译注**：直接打开系统无障碍服务列表，并通过 COMPONENT_NAME 把本应用服务高亮定位；跳转后引导页自我销毁 | 在系统无障碍列表中找到并开启「nered」服务（服务名不可读、描述为「...」） | `isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2.onClick` |
| 6 | 拒权反馈循环 | 再次回到 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20 引导页 | 用户从系统设置返回且无障碍仍未启用 → 后台 worker（BackgroundWorker / tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38）下一次 startActivity 再次压栈，onCreate 重新判定 isAccessibilityServiceEnabled==false 再次展示引导页 | 原生Activity（后台重复拉起，无次数上限） | **原文**：To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App<br>**译注**：同一段「解锁高级功能」话术反复出现，用户无法通过返回永久摆脱 | 反复要求点击 Enable 并前往系统设置开启服务 | `BackgroundWorker.onHandleIntent / tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38$_srv_worker_con_#doInBackground` |
| 7 | 获权后动作（反移除/自动导航） | AccessService（无障碍服务）→ 系统「应用详情」页 / 各厂商自启动与后台管理页 | onAccessibilityEvent 收到窗口事件，命中 android.settings.APPLICATION_DETAILS_SETTINGS 等页面时执行节点搜索与自动点击 | 系统应用详情页（由无障碍服务自动点按导航） | **原文**：android.settings.APPLICATION_DETAILS_SETTINGS<br>**译注**：在系统应用详情/权限管理页内自动定位并点击目标控件，帮助完成授权、保活与阻止撤销 | 无需用户操作（服务代替用户点击） | `AccessService.onAccessibilityEvent / Perfct.goToOppoAppDetails / RequestOPPOB.openNextActivity` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 后台强拉的独立 Activity（类名随机化 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20，excludeFromRecents，不在最近任务中留痕）——所有诱导文案的唯一载体
- res/layout/activity_req_access.xml：自绘「Accessibility Service」深灰顶栏 + 返回箭头 + 假 toggle 开关 + 应用图标/名称 + 蓝底说明文字 + Enable 按钮（全屏仿系统设置页）
- res/layout/miui_access_act.xml：MIUI 专用，全屏背景图 @drawable/en_access（预置分步截图教学）+ Next 按钮
- res/values/strings.xml：android:label=@string/trademarks59 = "\u007fnered"（DEL 控制字符 + nered），android:description=@string/Descrip = "..."
- res/xml/accessdiecrip.xml：无障碍服务声明（description="..."，settingsActivity 指向混淆类 udlulikgqndphqbmkgvudxfevutjfxlaynwrlvgbgzubcxwqxw17）
- MainActivity.onCreate 中的原生 AlertDialog（图标+标题+单 OK 按钮）："this App request Auto Start/Run in Background Permission to work properly"，无拒绝选项
- 系统无障碍服务列表项：显示为不可读的「nered」+ 描述「...」，用户无法从系统 UI 判断该服务可读取全部界面内容

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App | 要解锁高级功能，请按以下步骤：1. 点击「启用」按钮 2. 前往「已安装的服务 / 应用」 3. 开启高亮显示的那个应用 | `res/layout/activity_req_access.xml（android:id=@id/descrip 的 TextView，硬编码）` | 受限设置分步教学 |
| en | Accessibility Service | 无障碍服务 | `res/layout/activity_req_access.xml（@id/titletext，顶栏标题）` | 未知 |
| en | Enable | 启用 | `res/layout/activity_req_access.xml（@id/okbtn 按钮）` | 未知 |
| en | Next | 下一步 | `res/layout/miui_access_act.xml（@id/nextButton；代码中另有「下一个」「التالي」分支）` | 受限设置分步教学 |
| en | this App request Auto Start/Run in Background Permission to work properly | 本应用需要自启动/后台运行权限才能正常工作 | `MainActivity.onCreate 硬编码字符串（标题取 R.string 0x7f0c0043，按钮仅 OK/好的/Tamam/موافق）` | 故障恐吓 |
| en | nered | （DEL 控制字符）+ nered，在系统界面中渲染为空白或乱码，无可读名称 | `res/values/strings.xml key=trademarks59（application android:label、无障碍服务 android:label、activity_req_access 的 @id/nametext）` | 未知 |
| en | ... | 「...」（三个点，实际用途完全隐藏） | `res/values/strings.xml key=Descrip → res/xml/accessdiecrip.xml 的 android:description` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：引导页 onCreate 首行判定 utilities.isAccessibilityServiceEnabled==false 即重建引导 UI；跳转系统设置后自身 finish()，但常驻后台 worker（BackgroundWorker.onHandleIntent 与 tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38 内的 _srv_worker_con_#doInBackground）会再次以 FLAG_ACTIVITY_NEW_TASK 拉起该 Activity，用户从系统设置返回后又被弹回同一「解锁高级功能」页，无次数上限、无「不再提醒」状态位。
- **遮罩叠层 / 高仿系统设置页**：是。activity_req_access.xml 为全屏自绘页面，包含仿系统深灰顶栏（#ff263238）、返回箭头 @drawable/treelins、标题「Accessibility Service」、自绘假开关 @drawable/toggle 以及蓝底说明块，整体高仿厂商无障碍设置页；MIUI 分支更用预置截图 @drawable/en_access 作为全屏背景伪装成真实设置流程。
- **Android 13+ 受限设置（Restricted Settings）应对**：有分级教学：三级 Intent fallback（三星 com.samsung.accessibility...installed_service → android.settings.ACCESSIBILITY_SETTINGS 带 EXTRA_COMPONENT_NAME → Settings 深链 :settings:fragment_args_key / :settings:show_fragment_args）用于直达可开启页；获权阶段另通过无障碍服务自动点进 APPLICATION_DETAILS_SETTINGS 等页面完成后续授权导航。
- **获权后即时行为与防撤权机制**：是。AccessService.onAccessibilityEvent 监视 android.settings.APPLICATION_DETAILS_SETTINGS 等系统设置窗口并执行节点搜索/自动点击（Perfct.goToOppoAppDetails、goToXiaomioAppSettingDetails、RequestOPPOB.openNextActivity、searchAndClickOppoBatteryNotYh），用于自动完成授权与保活设置；服务以 android:stopWithTask="false" + priority=999 常驻，另有 BootReceiver 开机自启。
- **良性降级 / 替代方案**：无。不存在「稍后再说」「手动模式」「仅观看模式」等降级路径，用户唯一选择是被反复弹窗直至开启服务。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到启动 Activity 名为 com.duke...isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20（或任意 Activity 的首帧文本包含「Accessibility Service」+「To unlock premium feature」）时立即抓取 UTG；若来不及，则在捕获到 android.settings.ACCESSIBILITY_SETTINGS 跳转的同一时刻回溯抓取前一帧，并在用户按返回后的 1–3 秒内再次抓取以确认重跳。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：1) MIUI 分支的诱导内容全部承载于预置背景图 @drawable/en_access，纯 UTG 只能看到单个 Next 按钮，需 OCR 才能读出分步教学内容；2) 无障碍服务名与描述为 DEL 控制字符 + "..."，UTG 文本可能为空或乱码，不能据『无文本』判定为良性，需结合包名/Activity 名特征。另注：本样本未加壳，静态可见性良好，不构成运行期盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/后台强拉的诱导说明页（核心取证页）** | 顶栏文本「Accessibility Service」+ 假 toggle 图标 + 应用名「nered」+ 蓝底说明 + 底部「Enable」按钮；Activity 名随机化且 excludeFromRecents | 这一页同时证明三件事：伪造系统设置外观、使用「解锁高级功能」作为诱饵、完全没有取消/跳过出口——是判定诱导最关键的单帧证据 | 顶栏 title 文本 == 'Accessibility Service'（非系统 Settings 包名）；按钮文本 == 'Enable' / 'Next'，且同屏不存在 'Cancel'/'Not now'/'Skip'/'稍后' 任一节点；页面无系统设置的 Settings 包名/Activity 特征，却呈现设置页视觉结构（深灰标题栏 + 开关控件）；应用名节点文本以不可见控制字符开头（长度 >0 但渲染为空） |
| **跳转前的分步教学页（MIUI 变体）** | 全屏背景图 @drawable/en_access + 底部单个 Next 按钮，无任何文本段落 | 证明厂商定制化教学是预置图片而非真实系统页面，属刻意规避纯文本检测的图文诱导 | 整屏仅一个可点击按钮，无文字说明节点（纯图承载）；按钮文本随语言切换为 Next/下一个/التالي |
| **系统无障碍服务列表项** | 系统 Settings 无障碍页中名为「nered」（渲染空白/乱码）的服务条目，摘要为「...」 | 证明服务名与描述被伪造成不可读内容，用户在授权弹窗中无法识别这是读取全部界面内容的高危权限，构成身份混淆与知情同意破坏 | 列表项 label 为空或含控制字符，content-desc/description == '...'；同页开启开关后服务立即常驻（stopWithTask=false） |
| **拒权返回后的重跳页** | 用户从系统设置返回 1–3 秒内，同一「Accessibility Service / Enable」页面再次出现在前台 | 直接证明存在强制循环重跳，是「无取消出口」的运行时铁证，可区分一次性引导与持续性胁迫 | 相同 Activity 在用户返回后重复进入前台（时间戳间隔短、次数 >1）；页面无任何『已拒绝/稍后』状态文案变化，始终为同一话术 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate`
- `com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2.onClick`
- `com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.BackgroundWorker.onHandleIntent`
- `com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.AccessService.onAccessibilityEvent`
- `res/layout/activity_req_access.xml`
- `res/xml/accessdiecrip.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**静态可见性：基本完整**（未加壳，字符串与跳转逻辑均静态可还原，仅混淆字符串需运行时拼接）。

**核心链路（无障碍诱导，运行期页面流转）**

1. **冷启动**：`MainActivity`（`taskAffinity="app.one"`、`Theme.Translucent.NoTitleBar`）为 LAUNCHER 入口，onCreate 中先做模拟器检测（`utilities.Anti_emu()` / `isEmu_DIV_ID_lator()`），再按语言设置"继续安装"通知文案，随后 `Work()`、`Settings.canDrawOverlays` 分支处理悬浮窗授权。
2. **后台拉起引导页**：`BackgroundWorker.onHandleIntent` 与常驻服务 `tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38` 内的 `_srv_worker_con_#doInBackground` 都会 `startActivity(new Intent(ctx, isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.class).addFlags(FLAG_ACTIVITY_NEW_TASK).addFlags(FLAG_ACTIVITY_CLEAR_TOP))`——即**该引导页不是用户点出来的，而是后台轮询/事件触发反复压栈弹起**。
3. **伪造"系统设置页"**：未检测到无障碍已启用时，`onCreate` 立即 `setContentView` 伪装布局：
   - 非 MIUI：`res/layout/activity_req_access.xml` —— 深灰顶栏（`#ff263238`）+ 返回箭头 `@drawable/treelins` + 标题 **"Accessibility Service"**，一行自绘假开关 `@drawable/toggle`，应用图标 + 名称 `\u007fnered`，蓝底（`#ff002751`）说明文字，底部 `Enable` 按钮。整体观感刻意模仿 MIUI/EMUI 的"无障碍服务"设置页。
   - MIUI 分支：`res/layout/miui_access_act.xml` —— 全屏背景图 `@drawable/en_access`（预先做好的分步截图教学）+ `Next` 按钮，按钮文案随语言切换（Next / 下一个 / التالي）。
4. **诱因话术**：说明文字为 `To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App`——以"解锁高级功能"作为交换，并要求用户到"已安装的服务/应用"里"开启高亮的那个应用"。**无取消、无跳过、无"稍后"按钮**，仅返回键可退出。
5. **跳转受限设置**：点击 Enable → `isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2#onClick`：
   - 先尝试 `com.samsung.accessibility...installed_service`（三星专用无障碍页）；
   - `resolveActivity` 为空则退回 `android.settings.ACCESSIBILITY_SETTINGS` 并 `putExtra(EXTRA_COMPONENT_NAME, ComponentName(pkg, AccessService.class))`；
   - 再退回带 `:settings:fragment_args_key` 的 Settings 深链；
   - 跳转后 `utilities.Trys = 0` 并 `finish()` 自身，规避用户回退到该页。
6. **拒权循环**：引导页 finish 后无障碍仍未开启 → 后台 worker 再次拉起同一 Activity（`isAccessibilityServiceEnabled` 判定在 onCreate 首行），形成"跳设置 → 返回 → 再弹"的闭环。
7. **获权后反移除**：`AccessService#onAccessibilityEvent` 内处理 `android.settings.APPLICATION_DETAILS_SETTINGS`，配合 `Perfct.goToOppoAppDetails / goToXiaomioAppSettingDetails / RequestOPPOB#openNextActivity` 等，用无障碍节点搜索自动点进应用详情与各厂商自启动/后台设置页；`ACCESSIBILITY_SETTINGS` 亦在事件侧被监视。

**身份伪装要点**：桌面名 `\u007fnered`（仅含 DEL 0x7F 控制字符 + "nered"）、Activity `android:label=" "`（单空格）、无障碍服务 label 同为 `@string/trademarks59`= `\u007fnered`、`android:description`= `...`。在系统无障碍列表与授权确认弹窗里，用户看到的是一串**不可读的控制字符名**，用途说明是三个点——完全无法判断这是读取全部界面内容的高危权限。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "未加壳（apkid 初判 False）。无障碍服务声明、引导布局、跳转 Intent 与后台拉起逻辑均完整静态可见；仅部分字符串用 stuoxctjtdaoeuivbicuhkpiflkolbbmlmpdazwmgcmmbmmdif53 做混淆拼接（如 android.settings.ACCESSIBILITY_SETTINGS、com.samsung.accessibility...installed_service），可通过反编译直接还原明文。远端 WebView 内容（FloatingView/CraxsBrowser 承载的钓鱼页）属另一条业务链，与本无障碍诱导链无关。",
  "summary_one_liner": "应用以「解锁高级功能」为诱饵，后台反复弹起一个高仿系统无障碍设置页（假顶栏+假开关+Enable 按钮），点按后直跳系统无障碍设置并指定自身服务，同时把服务名与描述伪造成不可读的 DEL 控制字符与「...」，形成拒权后重跳的死循环。",
  "disguise_identity": {
    "app_display_name": "\u007fnered",
    "claimed_brand_or_persona": "伪装为系统级「Accessibility Service / 已安装服务」设置界面，并以「premium feature 解锁」名义自称增值服务提供方",
    "a11y_service_label": "\u007fnered（取自 @string/trademarks59，实为 DEL 控制字符 0x7F + \"nered\"；android:description = \"...\"）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 应用名、无障碍服务名均以 DEL(0x7F) 控制字符开头，在系统无障碍列表/授权弹窗中渲染为空白或乱码，用户无法识别；2) android:description 仅为 \"...\"，隐藏真实用途；3) 引导 Activity 的 android:label 设为单个空格；4) 引导页自绘顶栏「Accessibility Service」+ 返回箭头 + 假 toggle 开关，全屏仿系统设置页；5) MIUI 分支用预置背景图 @drawable/en_access 做分步截图教学；6) 引导 Activity 类名整段随机化（isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20），且 excludeFromRecents=true 不在最近任务中留痕；7) 跳转后立即 finish() 自身，避免用户回退发现。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.MainActivity（LAUNCHER，Theme.Translucent.NoTitleBar）",
      "trigger_event": "onCreate：先 utilities.Anti_emu()/isEmu_DIV_ID_lator() 模拟器检测（命中则 AsknoEmu 并 return），随后按 Locale 设置安装通知文案、utilities.SetJob 注册 Job、按 NeedAutoStart 弹自启动权限 AlertDialog、Settings.canDrawOverlays 判断悬浮窗授权",
      "ui_carrier": "原生Activity + 原生Dialog",
      "shown_text_verbatim": "this App request Auto Start/Run in Background Permission to work properly（标题取自 R.string，图标为应用图标，仅 OK/好的/Tamam/موافق 一个按钮）",
      "shown_text_zh": "本应用需要自启动/后台运行权限才能正常工作（仅一个确认按钮，无拒绝选项）",
      "user_action_requested": "仅可点击「OK」；无拒绝/跳过按钮，点后进入系统自启动设置",
      "code_anchor": "MainActivity.onCreate / MainActivity$7"
    },
    {
      "step": 2,
      "stage": "后台拉起引导页",
      "screen_or_component": "com.duke...isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20（exported=true、excludeFromRecents=true、label=\" \"、Translucent）",
      "trigger_event": "BackgroundWorker.onHandleIntent 与 lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38$_srv_worker_con_#doInBackground 中 startActivity(new Intent(ctx, 该Activity.class).addFlags(NEW_TASK).addFlags(NEW_TASK))",
      "ui_carrier": "原生Activity（后台强制压栈弹出，非用户主动点击）",
      "shown_text_verbatim": "无（启动行为本身无文案）",
      "shown_text_zh": "无",
      "user_action_requested": "无（被动弹出，用户被强行带到下一步界面）",
      "code_anchor": "BackgroundWorker.onHandleIntent / tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38$_srv_worker_con_#doInBackground"
    },
    {
      "step": 3,
      "stage": "引导说明页（仿系统设置页）",
      "screen_or_component": "同一 Activity，onCreate 首行 utilities.isAccessibilityServiceEnabled(this, AccessService.class)==false 时 setContentView(R.layout.activity_req_access)",
      "trigger_event": "onCreate 检测无障碍未启用",
      "ui_carrier": "原生Activity（自绘全屏页面，仿系统设置界面）",
      "shown_text_verbatim": "Accessibility Service / \u007fnered / To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App / Enable",
      "shown_text_zh": "顶栏「无障碍服务」；应用名显示为不可读控制字符 nered；正文「要解锁高级功能，请按以下步骤：1. 点击启用按钮 2. 前往『已安装的服务/应用』 3. 开启高亮的那个应用」；底部按钮「启用」",
      "user_action_requested": "点击底部 Enable 按钮（无取消、无跳过、无稍后按钮，仅系统返回键可退出）",
      "code_anchor": "isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate → res/layout/activity_req_access.xml"
    },
    {
      "step": 4,
      "stage": "引导说明页（MIUI 变体，截图分步教学）",
      "screen_or_component": "同一 Activity，utilities.isMIUI(ctx)==true 时 setContentView(R.layout.miui_access_act)",
      "trigger_event": "onCreate 检测到 MIUI 机型",
      "ui_carrier": "原生Activity（全屏预置背景图 + 单按钮）",
      "shown_text_verbatim": "Next / 下一个 / التالي（按钮文案随语言切换，主体内容为 @drawable/en_access 背景图）",
      "shown_text_zh": "「下一步」（页面主体是一张事先做好的分步操作截图，教用户如何在 MIUI 中开启无障碍）",
      "user_action_requested": "点击 Next 按钮继续（无取消/跳过）",
      "code_anchor": "isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate → res/layout/miui_access_act.xml / @drawable/en_access"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置（含受限设置教学深链）",
      "screen_or_component": "系统无障碍设置页：com.samsung.accessibility...installed_service → android.settings.ACCESSIBILITY_SETTINGS（带 EXTRA_COMPONENT_NAME=AccessService）→ Settings 深链 :settings:fragment_args_key / :settings:show_fragment_args",
      "trigger_event": "点击 Enable/Next 触发 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2.onClick",
      "ui_carrier": "系统无障碍页（Intent 三级 fallback，跳转后调用 finish() 关闭自身）",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS / android.intent.extra.COMPONENT_NAME / :settings:fragment_args_key / :settings:show_fragment_args",
      "shown_text_zh": "直接打开系统无障碍服务列表，并通过 COMPONENT_NAME 把本应用服务高亮定位；跳转后引导页自我销毁",
      "user_action_requested": "在系统无障碍列表中找到并开启「\u007fnered」服务（服务名不可读、描述为「...」）",
      "code_anchor": "isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2.onClick"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "再次回到 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20 引导页",
      "trigger_event": "用户从系统设置返回且无障碍仍未启用 → 后台 worker（BackgroundWorker / tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38）下一次 startActivity 再次压栈，onCreate 重新判定 isAccessibilityServiceEnabled==false 再次展示引导页",
      "ui_carrier": "原生Activity（后台重复拉起，无次数上限）",
      "shown_text_verbatim": "To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App",
      "shown_text_zh": "同一段「解锁高级功能」话术反复出现，用户无法通过返回永久摆脱",
      "user_action_requested": "反复要求点击 Enable 并前往系统设置开启服务",
      "code_anchor": "BackgroundWorker.onHandleIntent / tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38$_srv_worker_con_#doInBackground"
    },
    {
      "step": 7,
      "stage": "获权后动作（反移除/自动导航）",
      "screen_or_component": "AccessService（无障碍服务）→ 系统「应用详情」页 / 各厂商自启动与后台管理页",
      "trigger_event": "onAccessibilityEvent 收到窗口事件，命中 android.settings.APPLICATION_DETAILS_SETTINGS 等页面时执行节点搜索与自动点击",
      "ui_carrier": "系统应用详情页（由无障碍服务自动点按导航）",
      "shown_text_verbatim": "android.settings.APPLICATION_DETAILS_SETTINGS",
      "shown_text_zh": "在系统应用详情/权限管理页内自动定位并点击目标控件，帮助完成授权、保活与阻止撤销",
      "user_action_requested": "无需用户操作（服务代替用户点击）",
      "code_anchor": "AccessService.onAccessibilityEvent / Perfct.goToOppoAppDetails / RequestOPPOB.openNextActivity"
    }
  ],
  "text_presentation_locations": [
    "后台强拉的独立 Activity（类名随机化 isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20，excludeFromRecents，不在最近任务中留痕）——所有诱导文案的唯一载体",
    "res/layout/activity_req_access.xml：自绘「Accessibility Service」深灰顶栏 + 返回箭头 + 假 toggle 开关 + 应用图标/名称 + 蓝底说明文字 + Enable 按钮（全屏仿系统设置页）",
    "res/layout/miui_access_act.xml：MIUI 专用，全屏背景图 @drawable/en_access（预置分步截图教学）+ Next 按钮",
    "res/values/strings.xml：android:label=@string/trademarks59 = \"\\u007fnered\"（DEL 控制字符 + nered），android:description=@string/Descrip = \"...\"",
    "res/xml/accessdiecrip.xml：无障碍服务声明（description=\"...\"，settingsActivity 指向混淆类 udlulikgqndphqbmkgvudxfevutjfxlaynwrlvgbgzubcxwqxw17）",
    "MainActivity.onCreate 中的原生 AlertDialog（图标+标题+单 OK 按钮）：\"this App request Auto Start/Run in Background Permission to work properly\"，无拒绝选项",
    "系统无障碍服务列表项：显示为不可读的「\u007fnered」+ 描述「...」，用户无法从系统 UI 判断该服务可读取全部界面内容"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App",
      "text_zh": "要解锁高级功能，请按以下步骤：1. 点击「启用」按钮 2. 前往「已安装的服务 / 应用」 3. 开启高亮显示的那个应用",
      "source_location": "res/layout/activity_req_access.xml（android:id=@id/descrip 的 TextView，硬编码）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service",
      "text_zh": "无障碍服务",
      "source_location": "res/layout/activity_req_access.xml（@id/titletext，顶栏标题）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable",
      "text_zh": "启用",
      "source_location": "res/layout/activity_req_access.xml（@id/okbtn 按钮）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Next",
      "text_zh": "下一步",
      "source_location": "res/layout/miui_access_act.xml（@id/nextButton；代码中另有「下一个」「التالي」分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "this App request Auto Start/Run in Background Permission to work properly",
      "text_zh": "本应用需要自启动/后台运行权限才能正常工作",
      "source_location": "MainActivity.onCreate 硬编码字符串（标题取 R.string 0x7f0c0043，按钮仅 OK/好的/Tamam/موافق）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "\u007fnered",
      "text_zh": "（DEL 控制字符）+ nered，在系统界面中渲染为空白或乱码，无可读名称",
      "source_location": "res/values/strings.xml key=trademarks59（application android:label、无障碍服务 android:label、activity_req_access 的 @id/nametext）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "...",
      "text_zh": "「...」（三个点，实际用途完全隐藏）",
      "source_location": "res/values/strings.xml key=Descrip → res/xml/accessdiecrip.xml 的 android:description",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "引导页 onCreate 首行判定 utilities.isAccessibilityServiceEnabled==false 即重建引导 UI；跳转系统设置后自身 finish()，但常驻后台 worker（BackgroundWorker.onHandleIntent 与 tiioyslylawbjfcuduydnfhcaxjywhxvgxwusxnoltefbuxqqj38 内的 _srv_worker_con_#doInBackground）会再次以 FLAG_ACTIVITY_NEW_TASK 拉起该 Activity，用户从系统设置返回后又被弹回同一「解锁高级功能」页，无次数上限、无「不再提醒」状态位。",
    "overlay_or_fake_settings": "是。activity_req_access.xml 为全屏自绘页面，包含仿系统深灰顶栏（#ff263238）、返回箭头 @drawable/treelins、标题「Accessibility Service」、自绘假开关 @drawable/toggle 以及蓝底说明块，整体高仿厂商无障碍设置页；MIUI 分支更用预置截图 @drawable/en_access 作为全屏背景伪装成真实设置流程。",
    "restricted_settings_13plus_coaching": "有分级教学：三级 Intent fallback（三星 com.samsung.accessibility...installed_service → android.settings.ACCESSIBILITY_SETTINGS 带 EXTRA_COMPONENT_NAME → Settings 深链 :settings:fragment_args_key / :settings:show_fragment_args）用于直达可开启页；获权阶段另通过无障碍服务自动点进 APPLICATION_DETAILS_SETTINGS 等页面完成后续授权导航。",
    "post_grant_anti_removal": "是。AccessService.onAccessibilityEvent 监视 android.settings.APPLICATION_DETAILS_SETTINGS 等系统设置窗口并执行节点搜索/自动点击（Perfct.goToOppoAppDetails、goToXiaomioAppSettingDetails、RequestOPPOB.openNextActivity、searchAndClickOppoBatteryNotYh），用于自动完成授权与保活设置；服务以 android:stopWithTask=\"false\" + priority=999 常驻，另有 BootReceiver 开机自启。",
    "benign_graceful_degradation": "无。不存在「稍后再说」「手动模式」「仅观看模式」等降级路径，用户唯一选择是被反复弹窗直至开启服务。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到启动 Activity 名为 com.duke...isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20（或任意 Activity 的首帧文本包含「Accessibility Service」+「To unlock premium feature」）时立即抓取 UTG；若来不及，则在捕获到 android.settings.ACCESSIBILITY_SETTINGS 跳转的同一时刻回溯抓取前一帧，并在用户按返回后的 1–3 秒内再次抓取以确认重跳。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/后台强拉的诱导说明页（核心取证页）",
        "page_identifier": "顶栏文本「Accessibility Service」+ 假 toggle 图标 + 应用名「\u007fnered」+ 蓝底说明 + 底部「Enable」按钮；Activity 名随机化且 excludeFromRecents",
        "why_most_useful": "这一页同时证明三件事：伪造系统设置外观、使用「解锁高级功能」作为诱饵、完全没有取消/跳过出口——是判定诱导最关键的单帧证据",
        "observable_utg_signals": [
          "顶栏 title 文本 == 'Accessibility Service'（非系统 Settings 包名）",
          "按钮文本 == 'Enable' / 'Next'，且同屏不存在 'Cancel'/'Not now'/'Skip'/'稍后' 任一节点",
          "页面无系统设置的 Settings 包名/Activity 特征，却呈现设置页视觉结构（深灰标题栏 + 开关控件）",
          "应用名节点文本以不可见控制字符开头（长度 >0 但渲染为空）"
        ]
      },
      {
        "page_role": "跳转前的分步教学页（MIUI 变体）",
        "page_identifier": "全屏背景图 @drawable/en_access + 底部单个 Next 按钮，无任何文本段落",
        "why_most_useful": "证明厂商定制化教学是预置图片而非真实系统页面，属刻意规避纯文本检测的图文诱导",
        "observable_utg_signals": [
          "整屏仅一个可点击按钮，无文字说明节点（纯图承载）",
          "按钮文本随语言切换为 Next/下一个/التالي"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页中名为「\u007fnered」（渲染空白/乱码）的服务条目，摘要为「...」",
        "why_most_useful": "证明服务名与描述被伪造成不可读内容，用户在授权弹窗中无法识别这是读取全部界面内容的高危权限，构成身份混淆与知情同意破坏",
        "observable_utg_signals": [
          "列表项 label 为空或含控制字符，content-desc/description == '...'",
          "同页开启开关后服务立即常驻（stopWithTask=false）"
        ]
      },
      {
        "page_role": "拒权返回后的重跳页",
        "page_identifier": "用户从系统设置返回 1–3 秒内，同一「Accessibility Service / Enable」页面再次出现在前台",
        "why_most_useful": "直接证明存在强制循环重跳，是「无取消出口」的运行时铁证，可区分一次性引导与持续性胁迫",
        "observable_utg_signals": [
          "相同 Activity 在用户返回后重复进入前台（时间戳间隔短、次数 >1）",
          "页面无任何『已拒绝/稍后』状态文案变化，始终为同一话术"
        ]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在两处盲区：1) MIUI 分支的诱导内容全部承载于预置背景图 @drawable/en_access，纯 UTG 只能看到单个 Next 按钮，需 OCR 才能读出分步教学内容；2) 无障碍服务名与描述为 DEL 控制字符 + \"...\"，UTG 文本可能为空或乱码，不能据『无文本』判定为良性，需结合包名/Activity 名特征。另注：本样本未加壳，静态可见性良好，不构成运行期盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20.onCreate",
    "com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20$2.onClick",
    "com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.BackgroundWorker.onHandleIntent",
    "com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.lrnkvbkuoyhwwjjclyatabmdqjrxgnnkcjvzuleormlwhiwnjt3.AccessService.onAccessibilityEvent",
    "res/layout/activity_req_access.xml",
    "res/xml/accessdiecrip.xml"
  ]
}
```

</details>
