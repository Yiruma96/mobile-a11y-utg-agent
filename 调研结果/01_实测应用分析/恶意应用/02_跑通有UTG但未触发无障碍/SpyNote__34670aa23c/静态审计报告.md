# MB_038__34670aa23c｜SpyNote — TG88

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：129.5s

## 1. 一句话核心结论

- **核心申请方式**：启动器加载远端WebView并请求悬浮窗权限后，由无标题空白标签的引导Activity展示高仿系统无障碍开关页（或MIUI全屏截图教学），任意点击即带自身服务组件名直接跳转系统无障碍设置，并在取消/未开启时由IntentService与前台服务反复拉起。
- **静态可见性说明**：无障碍诱导全链（检测未开启→空白标签引导Activity→高仿系统开关页/MIUI纯图教学→ACCESSIBILITY_SETTINGS显式跳转→服务内GLOBAL_ACTION干预）在DEX与资源中静态完整可见；仅主界面为远端WebView（https://dtlaxmiguptaclasses.in.net/），远端HTML文案与后续指令不可静态取得；onCreate部分方法体为指令级反编译回落，AskDraw弹窗内部文案未逐行还原。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `34670aa23c3e50240fab2f820652f3f5d6eabf7177c6d6d4bba6c39a7b11aff9` |
| 包名 / 年份 | `dtlaxmiguptaclasses.in.net` / 2026 |
| 家族 / 品类 | **SpyNote**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | TG88 |
| 引导页宣称品牌/身份 | 仿冒 WhatsApp 系即时通讯（字符串库将原品牌词整体替换为 TG88），并在引导页伪装为系统“应用信息/无障碍开关”设置界面 |
| 系统无障碍列表服务名 | TG88 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍说明(android:description)仅为一个裸URL https://dtlaxmiguptaclasses.in.net/ 而非功能说明；引导Activity android:label=" " 单空格并从最近任务排除；layout中 titletext/nametext/okbtn 全填 TG88、descrip 直接填URL，另用 TextView text="                " 空格占位排版；res/values app_name="System Keyboard" 与显示名 TG88 不一致；包名与全部类名均为随机长串（含 .vending./.apk./.id 伪包名查询）并叠加字符串混淆函数拼接 settings action；未使用 isAccessibilityTool（targetSdk 29）。 |
| 无障碍服务类名 | `dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.uwcynvwgdlqtpkqtoaliajvjajjhyjbwdbitrgjctjuycevtvw3.ljdzmgrvnbilsycsdqoogguxwawrsdzuqzhnjqusnqmukadcdt72` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：@00000000 |
| 共现高危权限 | `CALL_PHONE, CAMERA, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | https://dtlaxmiguptaclasses.in.net/ |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31（LAUNCHER，label=TG88） | onCreate：先执行 Anti_emu() 与 isEmu_DIV_ID_lator()，命中则 AsknoEmu() 并 return；否则记录屏幕宽高、按语言设置“继续安装”通知文案、读取 Cantgo 标记并加载远端 WebView | 原生Activity + 远端WebView | **原文**：https://dtlaxmiguptaclasses.in.net/ ；Continue installing / Click Here to Continue installing ；继续安装 / 单击此处继续安装 ；kuruluma devam et / Kuruluma devam etmek için buraya tıklayın<br>**译注**：主界面为远端网页（域名即无障碍说明中的同一域名）；同时预置“继续安装/点击此处继续安装”的多语安装诱导通知文案 | 在远端网页内按提示操作；无取消入口 | `aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31.onCreate / 字段 value="https://dtlaxmiguptaclasses.in.net/"` |
| 2 | 业务功能触发 | 系统悬浮窗授权页（android.settings.action.MANAGE_OVERLAY_PERMISSION） | aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31$1#onClick 与 $3#onCancel 均执行 startActivityForResult(new Intent("android.settings.action.MANAGE_OVERLAY_PERMISSION", package:...), 0) | 系统设置页 | **原文**：无（系统页文案）<br>**译注**：要求开启“显示在其他应用上层”，为用户拒绝后仍再次跳转 | 点击允许悬浮窗；取消也会被再次拉起 | `aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31$1#onClick / $3#onCancel` |
| 3 | 引导说明页 | dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20（Manifest label=" "，excludeFromRecents） | 由 Bwschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9worker#onHandleIntent 与 zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38con_#doInBackground 在 isAccessibilityServiceEnabled()==false 时以 NEW_TASK\|CLEAR_TOP 启动；进入后 onCreate 再次判空并渲染 | 原生Activity（非MIUI：高仿系统设置布局；MIUI：全屏图片） | **原文**：TG88（标题栏）/ TG88（应用名）/ https://dtlaxmiguptaclasses.in.net/（说明区）/ TG88（底部按钮）；MIUI分支：Next / 下一个 / التالي<br>**译注**：伪装成“TG88 应用信息 + 无障碍开关”页，开关与整页任意位置都可点击；MIUI 上改为全屏截图 + “下一步”按钮 | 点击开关/图标/按钮“下一步”继续；无取消、无跳过按钮（onBackPressed 仅 super 默认行为） | `akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20#onCreate / res/layout/activity_req_access.xml / res/layout/miui_access_act.xml` |
| 4 | 跳受限设置 | 先尝试 com.samsung.accessibility…installed_service，再尝试 android.settings.*ACCESSIBILITY_SETTINGS（混淆拼接），最后回落显式 android.settings.ACCESSIBILITY_SETTINGS | akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20$2#onClick（由 $1#onClick 转发），intent.setFlags(1350565888) 后 startActivity，随后 finish() 自身并把 Trys 归零 | 系统无障碍设置页 | **原文**：无（系统页文案）<br>**译注**：通过 EXTRA_COMPONENT_NAME 精确指向本应用无障碍服务条目，直接落在开关位置；随后关闭自身页面，抹去跳转来源 | 在系统列表中打开 TG88 服务开关 | `akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20$2#onClick` |
| 5 | 拒权反馈循环 | 前台服务 zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38 与 IntentService Bwschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9worker | 周期性/事件触发时再次 isAccessibilityServiceEnabled 判定为 false → 再次 startActivity 拉起步骤3的引导Activity；悬浮窗取消亦重跳 | 原生Activity（重复弹出）+ 通知栏 | **原文**：Continue installing / Click Here to Continue installing<br>**译注**：通过通知与再次弹页持续施压，直到无障碍开启 | 反复要求用户开启无障碍；用户无法通过返回/取消终止 | `zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38$…con_#doInBackground / Bwschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9worker#onHandleIntent` |
| 6 | 获权后动作 | 无障碍服务 dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.uwcynvwgdlqtpkqtoaliajvjajjhyjbwdbitrgjctjuycevtvw3.ljdzmgrvnbilsycsdqoogguxwawrsdzuqzhnjqusnqmukadcdt72 | 服务内 SW() 调用 performGlobalAction(1/2/3/8/9) | 系统无障碍能力（无界面） | 无 | 无 | `ljdzmgrvnbilsycsdqoogguxwawrsdzuqzhnjqusnqmukadcdt72#SW` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 引导Activity akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20 的原生布局 res/layout/activity_req_access.xml：标题栏 TG88、应用名 TG88、说明区裸URL、底部按钮 TG88，整页控件共用同一跳转监听
- MIUI 分支 res/layout/miui_access_act.xml：全屏图片 @drawable/en_access、ar_access、cn_access 作为“系统无障碍设置截图”，仅一个 Next/下一个/التالي 按钮，文案在图片内需 OCR
- Manifest 无障碍服务 android:description = @string/Descrip = https://dtlaxmiguptaclasses.in.net/（系统无障碍列表中显示为裸域名而非功能说明）
- Manifest 无障碍服务 android:label = @string/rallyceconomick59 = TG88（系统无障碍列表条目名）
- 启动器 Activity 内嵌远端 WebView（https://dtlaxmiguptaclasses.in.net/）承载主界面全部诱导文案，静态不可见
- 系统通知栏：预置“Continue installing / 继续安装 / kuruluma devam et / مواصلة التثبيت”安装诱导通知（wschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9.completeinstallnotifi_title/msg）
- res/values/strings.xml 整套 WhatsApp 文案（设备验证、双卡SIM、备份等）作为远端页面/诱导语境素材，非本地界面直接呈现

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | TG88 | TG88（仿冒品牌名，出现于引导页标题栏、应用名、确认按钮、无障碍服务标签、桌面图标名） | `res/layout/activity_req_access.xml（titletext/nametext/okbtn）；res/values/strings.xml key=rallyceconomick59` | 未知 |
| en | https://dtlaxmiguptaclasses.in.net/ | 说明区域直接显示该网址，充当“服务说明”文字 | `res/layout/activity_req_access.xml id=descrip；res/values/strings.xml key=Descrip；res/xml/accessdiecrip.xml android:description` | 教唆忽视警告 |
| en | Next | 下一步 | `res/layout/miui_access_act.xml id=nextButton（代码按语言覆盖为 下一个 / التالي）` | 受限设置分步教学 |
| zh | 下一个 | 下一步 | `akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20#onCreate（中文语言分支 nextButton.setText）` | 受限设置分步教学 |
| en | Click Here to Continue installing | 点击此处继续安装 | `aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31#onCreate（wschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9.completeinstallnotifi_msg）` | 假更新 |
| zh | 单击此处继续安装 | 单击此处继续安装 | `aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31#onCreate（中文分支通知文案）` | 假更新 |
| tr | Kuruluma devam etmek için buraya tıklayın | 点击此处以继续安装 | `aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31#onCreate（土耳其语分支通知文案）` | 假更新 |
| en | System Keyboard | 系统键盘（与实际显示名 TG88 不符的备用应用名） | `res/values/strings.xml key=app_name` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：引导Activity无取消/跳过入口（onBackPressed 仅 super）；悬浮窗授权在 onClick 与 onCancel 两处都会 startActivityForResult(MANAGE_OVERLAY_PERMISSION)；前台服务 …con_#doInBackground 与 IntentService Bwschq…worker#onHandleIntent 在每次判定 isAccessibilityServiceEnabled()==false 时再次以 NEW_TASK|CLEAR_TOP 拉起引导Activity；配合 Cantgo/Trys 计数控制重试节奏，形成拒权-重跳循环。
- **遮罩叠层 / 高仿系统设置页**：是。res/layout/activity_req_access.xml 为高仿系统“应用信息+无障碍开关”页面（深色标题栏+开关图 toggle+应用图标+名称+说明+确认按钮，任意位置可点）；MIUI 上改用全屏图片 en_access/cn_access/ar_access 伪装系统无障碍设置截图；另申请 SYSTEM_ALERT_WINDOW 具备叠层能力。
- **Android 13+ 受限设置（Restricted Settings）应对**：无明确分步教学文案（未发现“应用详情右上角菜单→允许受限设置”文本）；但跳转使用显式 EXTRA_COMPONENT_NAME 直接定位自身服务条目，等价于替用户完成“找到并点开本服务”的步骤。
- **获权后即时行为与防撤权机制**：服务内 SW() 调用 performGlobalAction(1/2/3/8/9)（BACK/HOME/RECENTS 等），可在系统设置页执行全局返回/回主页动作，用于干扰用户撤销授权；未发现自点确认授权逻辑。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到进程内 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 MANAGE_OVERLAY_PERMISSION 的瞬间，以及 Activity 栈顶变为 label=" " 的 …akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20 时立即抓取当前页；另在后台服务拉起时按 500ms 轮询抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：主要盲区：1) MIUI 分支为全屏位图教学，纯图无文本，UTG 需 OCR 才能取证；2) 主界面文案托管于远端 WebView，内容随云控变化，静态不可复现；3) 无障碍说明仅为裸 URL，文本层无任何诱导语句，纯文本规则易漏判；4) 无障碍服务标签与桌面名同为 TG88、引导Activity label 为单空格，页面归属识别困难。非加壳样本，运行期 UTG 不受阻碍。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **高仿系统无障碍开关页（非MIUI）** | Activity 名含 akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20，界面为深色标题栏 TG88 + 开关图 + 应用图标 + 裸URL 说明 + TG88 按钮 | 该页是“把系统设置伪装成应用内页面”的直接证据，可判定用户是否在误以为仅是应用内开关的情况下授权 | 无系统 ActionBar/返回键而标题栏文字为 TG88；存在 @drawable/toggle 图片与裸URL 文本并存；页面任意控件点击都跳系统设置（可对比点击前后页面变化） |
| **MIUI 全屏图片教学页** | Activity 同为 akkggiqdx…b20，背景为 en_access/cn_access/ar_access 位图，仅一个 Next/下一个/التالي 按钮 | 纯图引导是绕过文本审查与自动检测的典型手法，需 OCR 确认图片内容伪造系统界面 | 整屏无文本节点、仅一张全屏 ImageView；按钮文本随系统语言变化；无关闭控件 |
| **跳转瞬间的系统无障碍服务列表页** | com.android.settings 无障碍页，且已滚动/定位到 TG88 条目 | 证明跳转携带 EXTRA_COMPONENT_NAME 精准落位，且应用随后 finish 自身抹去来源 | 列表项名为 TG88 且描述为 https://dtlaxmiguptaclasses.in.net/；跳转前栈顶为引导Activity、跳转后本应用任务被清除；开关被用户开启后立即出现全局返回动作 |
| **冷启动远端 WebView 主界面** | LAUNCHER Activity aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31 内 WebView 加载 dtlaxmiguptaclasses.in.net | 确认诱导起点与远端文案载体，为云端可变内容取证 | WebView 节点与 URL 域名；页面是否出现 TG88 品牌伪装元素；随后是否弹出悬浮窗授权请求 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20#onCreate`
- `dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20$2#onClick`
- `dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31#onCreate`
- `dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.uwcynvwgdlqtpkqtoaliajvjajjhyjbwdbitrgjctjuycevtvw3.zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38$zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38con_#doInBackground`
- `res/layout/activity_req_access.xml`
- `res/xml/accessdiecrip.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验。本次共 15 次工具调用（含 1 次服务繁忙失败），已超出约束上限，故不再追加调用，直接收口。

## 分析结论（要点）

**1. 静态可见性**：引导流程的 Java 侧逻辑完整可见；仅主界面文案托管在远端 `https://dtlaxmiguptaclasses.in.net/`（WebView，`onCreate` 中 `value` 字段即该 URL），远端 HTML 内容不可静态取得。

**2. 权限诱导由独立“假设置页”承担，而非正常业务页**：
- 引导页 Activity [akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20.onCreate()](<resource-unit:#1.dex1 code:dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20#onCreate>) 先判 `isAccessibilityServiceEnabled(...) == false` 才渲染；Manifest 中该 Activity `label=" "`（单空格）、`excludeFromRecents=true`，不可从桌面或最近任务识别。
- 非 MIUI 走 [activity_req_access.xml](<resource-unit:#1 file:res/layout/activity_req_access.xml>)：**高仿系统“应用信息+无障碍开关”页**——深色标题栏文字 `TG88`、开关图 `@drawable/toggle`、应用图标、名称 `TG88`、说明文字直接填 URL `https://dtlaxmiguptaclasses.in.net/`、底部按钮文字 `TG88`；整页任意控件（图标/返回键/开关/按钮）均绑定同一跳转监听，等于“点哪里都往下走”。
- MIUI 分支走 `miui_access_act`：**全屏静态图片** `en_access`/`cn_access`/`ar_access` + “Next/下一个/التالي”，即纯图分步教学（需 OCR 才能取文案）。

**3. 跳转链**：`$2.onClick` 先试三星专用 `com.samsung.accessibility…installed_service`，再试混淆前缀拼接出的 `android.settings.*ACCESSIBILITY_SETTINGS`，最后回落为显式 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `EXTRA_COMPONENT_NAME` 精确指向自身无障碍服务类，`setFlags(1350565888)` 后 `startActivity`，随即 `finish()` 自身并置 `Trys=0`——**用系统设置页掩盖“跳转由本应用发起”，并直接定位到自己的服务条目**。

**4. 拒绝反馈循环**：悬浮窗授权在点击（`$1.onClick`）与**取消（`$3.onCancel`）两处都 `startActivityForResult(MANAGE_OVERLAY_PERMISSION)`**；引导页由 `Bwschq…worker#onHandleIntent` 与前台服务 `…con_#doInBackground` 在检测到无障碍未开启时以 `NEW_TASK|CLEAR_TOP` 反复拉起；`Cantgo`/`Trys` 计数器参与重复判定。获权后由服务内 `SW()` 调用 `performGlobalAction(1/2/3/8/9)`（BACK/HOME/RECENTS 等）实施返回/回到主页干预。

**5. 身份伪装**：桌面名 `TG88`（`@string/rallyceconomick59`），无障碍列表标签同为 `TG88`，但 `android:description` 只是裸 URL 而非功能说明（`res/xml/accessdiecrip.xml` + `@string/Descrip`）；同时 `app_name="System Keyboard"` 与显示名不一致，字符串库整体为 WhatsApp 文案替换（`TG88` 替换原品牌词）——典型套壳换名。targetSdk 29，未使用 `isAccessibilityTool` 伪造。

**6. 边界**：远端 WebView 页面文案、`AskDraw` 内部弹窗细节（`onCreate` 反编译为指令级回落，未逐行还原）未展开，属覆盖缺口；不影响上述诱导链已证实。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍诱导全链（检测未开启→空白标签引导Activity→高仿系统开关页/MIUI纯图教学→ACCESSIBILITY_SETTINGS显式跳转→服务内GLOBAL_ACTION干预）在DEX与资源中静态完整可见；仅主界面为远端WebView（https://dtlaxmiguptaclasses.in.net/），远端HTML文案与后续指令不可静态取得；onCreate部分方法体为指令级反编译回落，AskDraw弹窗内部文案未逐行还原。",
  "summary_one_liner": "启动器加载远端WebView并请求悬浮窗权限后，由无标题空白标签的引导Activity展示高仿系统无障碍开关页（或MIUI全屏截图教学），任意点击即带自身服务组件名直接跳转系统无障碍设置，并在取消/未开启时由IntentService与前台服务反复拉起。",
  "disguise_identity": {
    "app_display_name": "TG88",
    "claimed_brand_or_persona": "仿冒 WhatsApp 系即时通讯（字符串库将原品牌词整体替换为 TG88），并在引导页伪装为系统“应用信息/无障碍开关”设置界面",
    "a11y_service_label": "TG88",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍说明(android:description)仅为一个裸URL https://dtlaxmiguptaclasses.in.net/ 而非功能说明；引导Activity android:label=\" \" 单空格并从最近任务排除；layout中 titletext/nametext/okbtn 全填 TG88、descrip 直接填URL，另用 TextView text=\"                \" 空格占位排版；res/values app_name=\"System Keyboard\" 与显示名 TG88 不一致；包名与全部类名均为随机长串（含 .vending./.apk./.id 伪包名查询）并叠加字符串混淆函数拼接 settings action；未使用 isAccessibilityTool（targetSdk 29）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31（LAUNCHER，label=TG88）",
      "trigger_event": "onCreate：先执行 Anti_emu() 与 isEmu_DIV_ID_lator()，命中则 AsknoEmu() 并 return；否则记录屏幕宽高、按语言设置“继续安装”通知文案、读取 Cantgo 标记并加载远端 WebView",
      "ui_carrier": "原生Activity + 远端WebView",
      "shown_text_verbatim": "https://dtlaxmiguptaclasses.in.net/ ；Continue installing / Click Here to Continue installing ；继续安装 / 单击此处继续安装 ；kuruluma devam et / Kuruluma devam etmek için buraya tıklayın",
      "shown_text_zh": "主界面为远端网页（域名即无障碍说明中的同一域名）；同时预置“继续安装/点击此处继续安装”的多语安装诱导通知文案",
      "user_action_requested": "在远端网页内按提示操作；无取消入口",
      "code_anchor": "aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31.onCreate / 字段 value=\"https://dtlaxmiguptaclasses.in.net/\""
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "系统悬浮窗授权页（android.settings.action.MANAGE_OVERLAY_PERMISSION）",
      "trigger_event": "aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31$1#onClick 与 $3#onCancel 均执行 startActivityForResult(new Intent(\"android.settings.action.MANAGE_OVERLAY_PERMISSION\", package:...), 0)",
      "ui_carrier": "系统设置页",
      "shown_text_verbatim": "无（系统页文案）",
      "shown_text_zh": "要求开启“显示在其他应用上层”，为用户拒绝后仍再次跳转",
      "user_action_requested": "点击允许悬浮窗；取消也会被再次拉起",
      "code_anchor": "aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31$1#onClick / $3#onCancel"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20（Manifest label=\" \"，excludeFromRecents）",
      "trigger_event": "由 Bwschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9worker#onHandleIntent 与 zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38con_#doInBackground 在 isAccessibilityServiceEnabled()==false 时以 NEW_TASK|CLEAR_TOP 启动；进入后 onCreate 再次判空并渲染",
      "ui_carrier": "原生Activity（非MIUI：高仿系统设置布局；MIUI：全屏图片）",
      "shown_text_verbatim": "TG88（标题栏）/ TG88（应用名）/ https://dtlaxmiguptaclasses.in.net/（说明区）/ TG88（底部按钮）；MIUI分支：Next / 下一个 / التالي",
      "shown_text_zh": "伪装成“TG88 应用信息 + 无障碍开关”页，开关与整页任意位置都可点击；MIUI 上改为全屏截图 + “下一步”按钮",
      "user_action_requested": "点击开关/图标/按钮“下一步”继续；无取消、无跳过按钮（onBackPressed 仅 super 默认行为）",
      "code_anchor": "akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20#onCreate / res/layout/activity_req_access.xml / res/layout/miui_access_act.xml"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "先尝试 com.samsung.accessibility…installed_service，再尝试 android.settings.*ACCESSIBILITY_SETTINGS（混淆拼接），最后回落显式 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20$2#onClick（由 $1#onClick 转发），intent.setFlags(1350565888) 后 startActivity，随后 finish() 自身并把 Trys 归零",
      "ui_carrier": "系统无障碍设置页",
      "shown_text_verbatim": "无（系统页文案）",
      "shown_text_zh": "通过 EXTRA_COMPONENT_NAME 精确指向本应用无障碍服务条目，直接落在开关位置；随后关闭自身页面，抹去跳转来源",
      "user_action_requested": "在系统列表中打开 TG88 服务开关",
      "code_anchor": "akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20$2#onClick"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "前台服务 zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38 与 IntentService Bwschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9worker",
      "trigger_event": "周期性/事件触发时再次 isAccessibilityServiceEnabled 判定为 false → 再次 startActivity 拉起步骤3的引导Activity；悬浮窗取消亦重跳",
      "ui_carrier": "原生Activity（重复弹出）+ 通知栏",
      "shown_text_verbatim": "Continue installing / Click Here to Continue installing",
      "shown_text_zh": "通过通知与再次弹页持续施压，直到无障碍开启",
      "user_action_requested": "反复要求用户开启无障碍；用户无法通过返回/取消终止",
      "code_anchor": "zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38$…con_#doInBackground / Bwschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9worker#onHandleIntent"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.uwcynvwgdlqtpkqtoaliajvjajjhyjbwdbitrgjctjuycevtvw3.ljdzmgrvnbilsycsdqoogguxwawrsdzuqzhnjqusnqmukadcdt72",
      "trigger_event": "服务内 SW() 调用 performGlobalAction(1/2/3/8/9)",
      "ui_carrier": "系统无障碍能力（无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "以 GLOBAL_ACTION_BACK/HOME/RECENTS 等全局动作干预界面，可用于在设置页快速返回、阻止用户撤销授权",
      "user_action_requested": "无",
      "code_anchor": "ljdzmgrvnbilsycsdqoogguxwawrsdzuqzhnjqusnqmukadcdt72#SW"
    }
  ],
  "text_presentation_locations": [
    "引导Activity akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20 的原生布局 res/layout/activity_req_access.xml：标题栏 TG88、应用名 TG88、说明区裸URL、底部按钮 TG88，整页控件共用同一跳转监听",
    "MIUI 分支 res/layout/miui_access_act.xml：全屏图片 @drawable/en_access、ar_access、cn_access 作为“系统无障碍设置截图”，仅一个 Next/下一个/التالي 按钮，文案在图片内需 OCR",
    "Manifest 无障碍服务 android:description = @string/Descrip = https://dtlaxmiguptaclasses.in.net/（系统无障碍列表中显示为裸域名而非功能说明）",
    "Manifest 无障碍服务 android:label = @string/rallyceconomick59 = TG88（系统无障碍列表条目名）",
    "启动器 Activity 内嵌远端 WebView（https://dtlaxmiguptaclasses.in.net/）承载主界面全部诱导文案，静态不可见",
    "系统通知栏：预置“Continue installing / 继续安装 / kuruluma devam et / مواصلة التثبيت”安装诱导通知（wschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9.completeinstallnotifi_title/msg）",
    "res/values/strings.xml 整套 WhatsApp 文案（设备验证、双卡SIM、备份等）作为远端页面/诱导语境素材，非本地界面直接呈现"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "TG88",
      "text_zh": "TG88（仿冒品牌名，出现于引导页标题栏、应用名、确认按钮、无障碍服务标签、桌面图标名）",
      "source_location": "res/layout/activity_req_access.xml（titletext/nametext/okbtn）；res/values/strings.xml key=rallyceconomick59",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "https://dtlaxmiguptaclasses.in.net/",
      "text_zh": "说明区域直接显示该网址，充当“服务说明”文字",
      "source_location": "res/layout/activity_req_access.xml id=descrip；res/values/strings.xml key=Descrip；res/xml/accessdiecrip.xml android:description",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Next",
      "text_zh": "下一步",
      "source_location": "res/layout/miui_access_act.xml id=nextButton（代码按语言覆盖为 下一个 / التالي）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "下一个",
      "text_zh": "下一步",
      "source_location": "akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20#onCreate（中文语言分支 nextButton.setText）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Click Here to Continue installing",
      "text_zh": "点击此处继续安装",
      "source_location": "aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31#onCreate（wschqghnwpuqjmpbobickxtjpuwclgmentobtrhlvggytbkdle9.completeinstallnotifi_msg）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "zh",
      "text_verbatim": "单击此处继续安装",
      "text_zh": "单击此处继续安装",
      "source_location": "aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31#onCreate（中文分支通知文案）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "Kuruluma devam etmek için buraya tıklayın",
      "text_zh": "点击此处以继续安装",
      "source_location": "aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31#onCreate（土耳其语分支通知文案）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "System Keyboard",
      "text_zh": "系统键盘（与实际显示名 TG88 不符的备用应用名）",
      "source_location": "res/values/strings.xml key=app_name",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "引导Activity无取消/跳过入口（onBackPressed 仅 super）；悬浮窗授权在 onClick 与 onCancel 两处都会 startActivityForResult(MANAGE_OVERLAY_PERMISSION)；前台服务 …con_#doInBackground 与 IntentService Bwschq…worker#onHandleIntent 在每次判定 isAccessibilityServiceEnabled()==false 时再次以 NEW_TASK|CLEAR_TOP 拉起引导Activity；配合 Cantgo/Trys 计数控制重试节奏，形成拒权-重跳循环。",
    "overlay_or_fake_settings": "是。res/layout/activity_req_access.xml 为高仿系统“应用信息+无障碍开关”页面（深色标题栏+开关图 toggle+应用图标+名称+说明+确认按钮，任意位置可点）；MIUI 上改用全屏图片 en_access/cn_access/ar_access 伪装系统无障碍设置截图；另申请 SYSTEM_ALERT_WINDOW 具备叠层能力。",
    "restricted_settings_13plus_coaching": "无明确分步教学文案（未发现“应用详情右上角菜单→允许受限设置”文本）；但跳转使用显式 EXTRA_COMPONENT_NAME 直接定位自身服务条目，等价于替用户完成“找到并点开本服务”的步骤。",
    "post_grant_anti_removal": "服务内 SW() 调用 performGlobalAction(1/2/3/8/9)（BACK/HOME/RECENTS 等），可在系统设置页执行全局返回/回主页动作，用于干扰用户撤销授权；未发现自点确认授权逻辑。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到进程内 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 MANAGE_OVERLAY_PERMISSION 的瞬间，以及 Activity 栈顶变为 label=\" \" 的 …akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20 时立即抓取当前页；另在后台服务拉起时按 500ms 轮询抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "高仿系统无障碍开关页（非MIUI）",
        "page_identifier": "Activity 名含 akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20，界面为深色标题栏 TG88 + 开关图 + 应用图标 + 裸URL 说明 + TG88 按钮",
        "why_most_useful": "该页是“把系统设置伪装成应用内页面”的直接证据，可判定用户是否在误以为仅是应用内开关的情况下授权",
        "observable_utg_signals": ["无系统 ActionBar/返回键而标题栏文字为 TG88", "存在 @drawable/toggle 图片与裸URL 文本并存", "页面任意控件点击都跳系统设置（可对比点击前后页面变化）"]
      },
      {
        "page_role": "MIUI 全屏图片教学页",
        "page_identifier": "Activity 同为 akkggiqdx…b20，背景为 en_access/cn_access/ar_access 位图，仅一个 Next/下一个/التالي 按钮",
        "why_most_useful": "纯图引导是绕过文本审查与自动检测的典型手法，需 OCR 确认图片内容伪造系统界面",
        "observable_utg_signals": ["整屏无文本节点、仅一张全屏 ImageView", "按钮文本随系统语言变化", "无关闭控件"]
      },
      {
        "page_role": "跳转瞬间的系统无障碍服务列表页",
        "page_identifier": "com.android.settings 无障碍页，且已滚动/定位到 TG88 条目",
        "why_most_useful": "证明跳转携带 EXTRA_COMPONENT_NAME 精准落位，且应用随后 finish 自身抹去来源",
        "observable_utg_signals": ["列表项名为 TG88 且描述为 https://dtlaxmiguptaclasses.in.net/", "跳转前栈顶为引导Activity、跳转后本应用任务被清除", "开关被用户开启后立即出现全局返回动作"]
      },
      {
        "page_role": "冷启动远端 WebView 主界面",
        "page_identifier": "LAUNCHER Activity aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31 内 WebView 加载 dtlaxmiguptaclasses.in.net",
        "why_most_useful": "确认诱导起点与远端文案载体，为云端可变内容取证",
        "observable_utg_signals": ["WebView 节点与 URL 域名", "页面是否出现 TG88 品牌伪装元素", "随后是否弹出悬浮窗授权请求"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "主要盲区：1) MIUI 分支为全屏位图教学，纯图无文本，UTG 需 OCR 才能取证；2) 主界面文案托管于远端 WebView，内容随云控变化，静态不可复现；3) 无障碍说明仅为裸 URL，文本层无任何诱导语句，纯文本规则易漏判；4) 无障碍服务标签与桌面名同为 TG88、引导Activity label 为单空格，页面归属识别困难。非加壳样本，运行期 UTG 不受阻碍。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20#onCreate",
    "dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.akkggiqdxjxbsmmldxaeoahntzgxxriknrzianehbninkbjbhb20$2#onClick",
    "dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.aksnmvsovloyugmwsdtlqnfhfrcgzqsbzucrnjqmxbsuwfmqbc31#onCreate",
    "dtlaxmiguptaclasses.in.ycizuxlrfhxzgjtcizwmxswdjjxtfgynwvmhdqycjfrgnqsqwi2.uwcynvwgdlqtpkqtoaliajvjajjhyjbwdbitrgjctjuycevtvw3.zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38$zguxtmaoafjyaszmzdqatvfgubxrvqshzrloednyyaafycyokm38con_#doInBackground",
    "res/layout/activity_req_access.xml",
    "res/xml/accessdiecrip.xml"
  ]
}
```

> 说明：因严格 14 次调用上限已用尽，本次未调用 `register_evidence_graph`/`record_risk` 写入风险台账。上述结论（恶意/欺诈性无障碍授权诱导，含假设置页伪装、无取消循环重拉、获权后 GLOBAL_ACTION 干预撤权）已具备完整静态证据链，如需入账可在后续会话按本回答的 `code_anchors` 直接登记为 `malware_trojan` / `deceptive_behavior` 高风险。

</details>
