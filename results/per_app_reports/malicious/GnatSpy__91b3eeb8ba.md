# MR_085__91b3eeb8ba｜GnatSpy — Facebook Update

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：129.7s

## 1. 一句话核心结论

- **核心申请方式**：该应用不在应用内做任何引导页或跳转，而是伪装成 Facebook 更新器，冷启动强制索取高危权限、拒权即弹不可取消 Snackbar 反复索要，并把无障碍服务的系统说明写成“为免费使用 Facebook 应开启此服务”，实际用于读取 com.android.phone 弹窗窃取本机号码。
- **静态可见性说明**：代码未加壳、未加密，全部引导逻辑、无障碍服务实现与字符串资源均可静态完整还原；应用不含 assets 目录、无 WebView、无远端 HTML，也不存在任何 ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 跳转点，因此无障碍开启完全依赖系统设置列表中的 description 文案诱导。仅 C2 地址（SPManager.NEW_SERVER_URL）为运行期下发，不影响本问题的静态可见性。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `91b3eeb8ba6853cab5f2669267cf9bccdba389149cc8b2c32656af62bd016b04` |
| 包名 / 年份 | `com.facebookupdate` / 2017 |
| 家族 / 品类 | **GnatSpy**（同池样本数：2） |
| 原始来源标识 | https://blog.trendmicro.com/trendlabs-security-intelligence/new-gnatspy-mobile-malware-family-discovered/ |
| 桌面显示名 | Facebook Update |
| 引导页宣称品牌/身份 | Facebook / Facebook Inc.（含 © 2017–2018 Facebook Inc.、Messenger/Instagram/WhatsApp/GooglePlay 假更新弹窗） |
| 系统无障碍列表服务名 | Facebook Update（服务未声明 android:label，系统无障碍列表回退显示应用名；说明文字为“You should Turn on this service for free using Facebook App.”） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍服务未设 android:label，列表中直接呈现应用名“Facebook Update”，与 Facebook 官方无签名/域名关联；2) config_service.xml 的 settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity，伪造设置入口；3) XML 声明 packageNames=com.times.ussd，运行时 onServiceConnected 改写为 com.android.phone，声明与实际监听目标不一致；4) description 用“免费使用 Facebook”话术替代真实用途（读通话/USSD 弹窗）；5) 5 个 excludeFromRecents + Dialog 主题的 activity 伪装成系统更新弹窗。 |
| 无障碍服务类名 | `com.facebookupdate.Services.GetNumberUSSDService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.times.ussd |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS` |
| 系统设置项说明 (`android:description`) | You should Turn on this service for free using Facebook App. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.facebookupdate.activities.FacebookUpdate（LAUNCHER Activity，layout: facebookupdate） | 用户点击桌面“Facebook Update”图标 → onCreate | 原生Activity | **原文**：Updating …（progressBar_update / textView_update 默认隐藏）；无网络时 Toast: No Internet Connection<br>**译注**：“正在更新……”进度条界面；无网络时提示“无网络连接” | 无主动请求，界面表现为正在更新（假进度） | `com.facebookupdate.activities.FacebookUpdate.onCreate + First_Run；res/values/strings.xml: updating_string / No_Internet` |
| 2 | 引导说明页（系统权限） | 系统运行时权限对话框（ActivityCompat.requestPermissions，requestCode=200） | onCreate 内 First_Run() 之后无条件调用 ActivityCompat.requestPermissions(this, PermissionsArray, 200) | 原生Activity | **原文**：android.permission.READ_CONTACTS / RECORD_AUDIO / READ_PHONE_STATE / RECEIVE_SMS / WRITE_EXTERNAL_STORAGE（系统标准文案，应用未提供任何 rationale 说明）<br>**译注**：系统标准权限弹窗，要求联系人、录音、电话状态、接收短信、写外部存储权限；应用未做任何用途说明 | 系统“允许/拒绝”按钮；应用侧无跳过、无说明页 | `com.facebookupdate.activities.FacebookUpdate.onCreate / PermissionsArray` |
| 3 | 拒权反馈循环 | 不可滑走的 Snackbar（Snackbar.make(layout, R.string.permissions, -2)） | onRequestPermissionsResult 中任一 grantResults == -1 且非“不再询问” | 原生Activity | **原文**：Please accept all the permissions to update Facebook  /  动作按钮: Accept<br>**译注**：“请接受全部权限以便更新 Facebook”，唯一按钮为“接受” | 只能点 Accept（触发 FacebookUpdate$4 重新 requestPermissions）；LENGTH_INDEFINITE 不可自动消失、无取消按钮；只有勾选“不再询问”才退出循环并上报 permission_full + Utility.disableReceivers | `com.facebookupdate.activities.FacebookUpdate.onRequestPermissionsResult / FacebookUpdate$4` |
| 4 | 拒权反馈循环（保活补充） | com.facebookupdate.utils.HuaweiUtils.showHuaweiAlert → AlertDialog（Huawei Protected Apps） | 全部权限授予后若 HuaweiUtils.isHuawei() 为真；同时 Handler.postDelayed(FacebookUpdate$3, 10000) | 原生Dialog | **原文**：Huawei Protected Apps / requires to be enabled in Protected Apps to function properly / 按钮: Protected Apps<br>**译注**：“华为受保护应用——需要在受保护应用中启用才能正常运行”，按钮“受保护应用”跳系统受保护应用列表 | 点击“Protected Apps”进入系统受保护应用设置并勾选本应用（保活，非无障碍） | `com.facebookupdate.utils.HuaweiUtils.showHuaweiAlert；strings.xml: huawei_title / huawei_message / huawei_button` |
| 5 | 获权后动作 | com.facebookupdate.Services.GetNumberUSSDService（无障碍服务，被 startService 拉起）+ AlarmManager 定时 | Complete_Process()：startService(GetNumberUSSDService) + scheduleTurnOnServicesReceiverAlarm(240) + Handler.postDelayed(FacebookUpdate$2, 5000) | 系统无障碍页（开启动作需用户手动完成） | **原文**：You should Turn on this service for free using Facebook App.<br>**译注**：“你应当通过 Facebook App 免费开启此服务。”（系统无障碍列表中的服务说明） | 要求用户在系统无障碍设置列表中自行找到该服务并打开开关；应用内无跳转按钮、无悬浮指引；服务 settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity | `com.facebookupdate.activities.FacebookUpdate.Complete_Process；res/xml/config_service.xml:2；strings.xml key=USSD` |
| 6 | 获权后动作 | com.facebookupdate.Receivers.TurnOnservicesReceiver（AlarmManager 每 240 秒重复）+ DeviceInfoService / ContactsService / SmsService 定时调度 | Complete_Process 设置的 240 秒闹钟；后续 TurnOnservicesReceiver.onReceive 每次重新调度 DeviceInfoService(30–60s)、ContactsService(120–180s)、SmsService(240s) | 通知栏（后台服务，无界面） | 无 | 无用户交互，后台自行重复拉起 | `com.facebookupdate.Receivers.TurnOnservicesReceiver.onReceive；Utility.scheduleTurnOnServicesReceiverAlarm / scheduleOneTimeService` |
| 7 | 遮罩叠层指引 | com.facebookupdate.HomeWatcher（Home/最近任务监听）→ FacebookUpdate$1.onHomePressed / onRecentAppsPressed → Complete_Process | 用户按 Home 键或最近任务键试图离开更新界面 | 原生Activity | 无 | 无；属于绕过用户退出的重入机制（非系统设置页遮罩） | `com.facebookupdate.activities.FacebookUpdate$1.onHomePressed / onRecentAppsPressed` |
| 8 | 获权后动作（真实行为） | com.facebookupdate.Services.GetNumberUSSDService.onAccessibilityEvent 监听 com.android.phone 的 AlertDialog | com.android.phone 弹出 USSD/通话弹窗（TYPE_WINDOW_STATE_CHANGED） | 系统无障碍页 | **原文**：Mobile Number : <抓取到的数字串>（上报字段）；performGlobalAction(1) 关闭系统弹窗<br>**译注**：先把系统弹窗自动点掉，再从文本抽取数字，命中 059 号段即作为本机号码回传服务器 | 无，静默执行；用户看不到弹窗也无法察觉读取 | `com.facebookupdate.Services.GetNumberUSSDService.onAccessibilityEvent / onServiceConnected；Utility.sendFeedBackRequest` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项的描述文字：res/xml/config_service.xml 的 android:description=@string/USSD（唯一直接面向用户的无障碍“开启引导”文案）
- 桌面图标名称与系统设置中的应用名：AndroidManifest android:label=@string/app_name = "Facebook Update"，图标 @drawable/facebook
- 冷启动 Activity 界面：com.facebookupdate.activities.FacebookUpdate + layout facebookupdate（progressBar_update / textView_update，文案 updating_string="Updating …"）
- 系统运行时权限对话框：ActivityCompat.requestPermissions(PermissionsArray, 200)，无应用侧 rationale 页
- 不可滑走的 Snackbar（LENGTH_INDEFINITE，黑底红字 + Accept 按钮）：strings.xml key=permissions / ok
- 华为机型原生 AlertDialog：HuaweiUtils.showHuaweiAlert（huawei_title / huawei_message / huawei_button）
- 假更新弹窗 Activity（excludeFromRecents + Dialog 主题）：Fb_dialog / FbM_dialog / Insta_dialog / WApp_dialog / Gplay_dialog 及 UninstallDialog，文案来自 *_Update_dialog_title / *_Update_dialog_text / uninstall_dialog_*
- 无网络 Toast：strings.xml key=No_Internet（"No Internet Connection"）
- 不存在的位置（已核实）：无 assets/*.html、无 WebView 页面、无悬浮窗 Overlay、无伪造系统无障碍设置页、无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | You should Turn on this service for free using Facebook App. | 你应当通过 Facebook App 免费开启此服务。 | `res/values/strings.xml key=USSD，被 res/xml/config_service.xml android:description 引用` | 假更新 |
| en | Please accept all the permissions to update Facebook | 请接受全部权限以便更新 Facebook。 | `res/values/strings.xml key=permissions；FacebookUpdate.onRequestPermissionsResult 中 LENGTH_INDEFINITE Snackbar` | 假更新 |
| en | Facebook Update | Facebook 更新（桌面显示名与假更新弹窗标题） | `res/values/strings.xml key=app_name / Fb_Update_dialog_title；AndroidManifest android:label` | 假更新 |
| en | A new version of Facebook is available and will be installed. | Facebook 有新版本可用，即将安装。 | `res/values/strings.xml key=Fb_Update_dialog_text（Fb_dialog Activity）` | 假更新 |
| en | A new version of Messenger is available and will be installed. | Messenger 有新版本可用，即将安装。 | `res/values/strings.xml key=FbM_Update_dialog_text（FbM_dialog Activity）` | 假更新 |
| en | A new version of GooglePlay is available and will be installed. | GooglePlay 有新版本可用，即将安装。 | `res/values/strings.xml key=Gplay_Update_dialog_text（Gplay_dialog Activity）` | 假更新 |
| en | This Application is outdated, you should uninstall it. | 此应用已过期，你应当卸载它。 | `res/values/strings.xml key=uninstall_dialog_text / uninstall_dialog_title（UninstallDialog Activity）` | 故障恐吓 |
| en | Huawei Protected Apps / requires to be enabled in Protected Apps to function properly / Protected Apps | 华为受保护应用 / 需要在“受保护应用”中启用才能正常运行 / 按钮：受保护应用 | `res/values/strings.xml key=huawei_title / huawei_message / huawei_button；HuaweiUtils.showHuaweiAlert` | 教唆忽视警告 |
| en | © 2017–2018 Facebook Inc. | © 2017–2018 Facebook 公司 | `res/values/strings.xml key=wa_year_inc_string` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：权限被拒后 onRequestPermissionsResult 用 LENGTH_INDEFINITE（-2）Snackbar 常驻提示“Please accept all the permissions to update Facebook”，唯一动作 Accept 重新 requestPermissions，形成无法关闭的重试环；用户勾选“不再询问”才跳出并把 NEVER_ASK_AGAIN 置真、上报 permission_full 并 disableReceivers。另 HomeWatcher 监听 Home/最近任务键，用户按 Home 离开时 onHomePressed 再次回调 Complete_Process 重启无障碍服务与 240 秒闹钟；TurnOnservicesReceiver 每 240 秒重复调度 DeviceInfoService/ContactsService/SmsService。
- **遮罩叠层 / 高仿系统设置页**：无。未发现悬浮窗/SYSTEM_ALERT_WINDOW 遮罩、无全屏引导层、无高仿系统无障碍开关页；但 config_service.xml 的 settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity，属伪造/失效的设置入口。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无障碍服务获得权限后，onAccessibilityEvent 检测到 android.app.AlertDialog 即调用 performGlobalAction(1)（GLOBAL_ACTION_BACK）自动关闭系统弹窗，使用户无法查看/确认该通话或 USSD 对话框；同时通过 AlarmManager（240 秒）+ HomeWatcher 重入持续复活服务，抵抗用户退出与清理。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动第一帧即拉起（监测 com.facebookupdate.activities.FacebookUpdate 进入前台或系统权限弹窗出现）；并在检测到 com.facebookupdate.Services.GetNumberUSSDService 在系统无障碍列表被开启、或 com.android.phone 的 AlertDialog 出现后 800ms 内被自动关闭时补抓一帧。由于应用全程不发送 ACTION_ACCESSIBILITY_SETTINGS 跳转，UTG 需依赖系统设置页与权限弹窗事件而非 Intent 跳转来触发。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两点盲区：1) 应用完全不跳转系统无障碍/应用详情设置页，纯 UTG 若只监听 ACCESSIBILITY_SETTINGS / APP_DETAILS 跳转将完全漏检，必须改为监听冷启动 Activity、系统权限弹窗与无障碍服务启用事件；2) 无障碍开关由用户在系统设置手动完成，应用侧无任何可视引导页，故“诱导”仅体现为系统列表 description 的一行文字，需专门抓取无障碍列表项文本。本样本未加壳、无加密载荷、无远端 HTML，静态加壳不构成阻碍。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动强制权限弹窗页** | com.facebookupdate.activities.FacebookUpdate 之上的系统权限对话框，同时申请 READ_CONTACTS/RECORD_AUDIO/READ_PHONE_STATE/RECEIVE_SMS/WRITE_EXTERNAL_STORAGE 五项 | 证明权限索取为冷启动 0 步强制、无任何用途说明前置，是“诱导”链条的起点 | 包名 com.facebookupdate 与显示名 Facebook Update 不一致；同一次弹窗请求 5 项高危权限且无 rationale 页；弹窗出现前无任何说明 Activity |
| **拒权后不可取消的 Snackbar 页** | 黑底红字 Snackbar，文本“Please accept all the permissions to update Facebook”，仅 Accept 按钮，无自动消失 | 直接体现“无跳过/无取消”的胁迫式索权，是区分正常应用与诱导样本的最强信号 | Snackbar 常驻不消失（LENGTH_INDEFINITE）；唯一可点元素为 Accept 且触发重复权限弹窗；文本明确绑定“更新 Facebook”话术 |
| **系统无障碍服务列表项（真实开启发生地）** | 系统“设置→无障碍”列表中名为 Facebook Update 的服务项，描述文字“You should Turn on this service for free using Facebook App.” | 这是应用唯一面向用户的无障碍引导文案，且与服务的真实监听目标（com.android.phone 弹窗）严重不符 | 服务名等于应用名 Facebook Update（未设独立 label）；description 使用“免费使用 Facebook”话术；点击该服务的设置图标无响应（settingsActivity 类不存在） |
| **获权后自动关闭系统弹窗的证据帧** | com.android.phone 的 USSD/通话 AlertDialog 出现后约 100–500ms 内被关闭，随后设备信息/号码上报请求发出 | 证明无障碍权限的真实用途是窃取本机号码而非“免费使用 Facebook” | 弹窗停留时间异常短（被 performGlobalAction BACK 关闭）；弹窗文本含 059 号段数字；紧接出现向 NEW_SERVER_URL 的反馈上报 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.facebookupdate.activities.FacebookUpdate.onCreate`
- `com.facebookupdate.activities.FacebookUpdate.onRequestPermissionsResult`
- `com.facebookupdate.activities.FacebookUpdate.Complete_Process`
- `com.facebookupdate.Services.GetNumberUSSDService.onAccessibilityEvent`
- `res/xml/config_service.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**身份伪装**：桌面名为 `Facebook Update`、图标为 `@drawable/facebook`、包名为 `com.facebookupdate`，`strings.xml` 中还含 `© 2017–2018 Facebook Inc.`，但代码与资源中没有一处 Facebook 官方签名或域名依据。

**无障碍“引导”并非页面流转，而是纯话术植入**：全包反编译搜索 `ACTION_ACCESSIBILITY_SETTINGS` 与 `ACTION_APPLICATION_DETAILS_SETTINGS` **均无命中**，也不存在 `assets/` 目录（无本地 HTML）。应用从不跳转系统设置，无障碍的开启完全依赖用户在系统列表中自行找到该服务，应用侧只提供一段误导性 `android:description`：

> `You should Turn on this service for free using Facebook App.`

**实际运行期流转**（[FacebookUpdate.onCreate()](<resource-unit:#1.dex1 code:com.facebookupdate.activities.FacebookUpdate#onCreate>) 起）：
1. 冷启动后立即弹出系统权限框，索取 `READ_CONTACTS / RECORD_AUDIO / READ_PHONE_STATE / RECEIVE_SMS / WRITE_EXTERNAL_STORAGE`，无任何说明前置。
2. 拒绝权限后，[onRequestPermissionsResult()](<resource-unit:#1.dex1 code:com.facebookupdate.activities.FacebookUpdate#onRequestPermissionsResult>) 弹出**不可滑走**的 `Snackbar`（`-2` = LENGTH_INDEFINITE）：`Please accept all the permissions to update Facebook`，仅有一个 `Accept` 动作回跳重试；只有勾选“不再询问”才停止并上报 `permission_full`。
3. 全部授权后，[Complete_Process()](<resource-unit:#1.dex1 code:com.facebookupdate.activities.FacebookUpdate#Complete_Process>) 直接 `startService(GetNumberUSSDService)`，并 `scheduleTurnOnServicesReceiverAlarm(240)` 每 240 秒重复拉起。
4. 华为机型额外弹 `Huawei Protected Apps` 引导加入受保护列表（保活）；`HomeWatcher.onHomePressed/onRecentAppsPressed` 也回调 `Complete_Process`，形成按下 Home 键即重启的循环。

**无障碍服务的真实用途与说明不符**：[config_service.xml 第2行](<resource-unit:#1 file:res/xml/config_service.xml#L2>) 声明 `settingsActivity="com.example.android.accessibility.ServiceSettingsActivity"`，该类在 Manifest 与 DEX 中均不存在，属于伪造或失效的设置入口；[onServiceConnected()](<resource-unit:#1.dex1 code:com.facebookupdate.Services.GetNumberUSSDService#onServiceConnected>) 把监听包名改写为 `com.android.phone`（与 XML 中的 `com.times.ussd` 不一致），[onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.facebookupdate.Services.GetNumberUSSDService#onAccessibilityEvent>) 在遇到 `android.app.AlertDialog` 时先 `performGlobalAction(1)` 自点返回关闭系统弹窗，再抽取文本数字、命中 `059` 号段即作为本机号码外发。

**UTG 盲区**：由于无跳转点、无悬浮遮罩、无 WebView，纯 UTG 只能捕获“冷启动强制权限 + 不可取消 Snackbar + 系统无障碍列表项的 description 文案”；真正的开启动作发生在用户手动进入的系统设置页，需同时抓取 `com.android.phone` 弹窗被自动关闭的痕迹才能佐证其真实用途。

```json
{
  "static_visibility": "clear",
  "visibility_note": "代码未加壳、未加密，全部引导逻辑、无障碍服务实现与字符串资源均可静态完整还原；应用不含 assets 目录、无 WebView、无远端 HTML，也不存在任何 ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 跳转点，因此无障碍开启完全依赖系统设置列表中的 description 文案诱导。仅 C2 地址（SPManager.NEW_SERVER_URL）为运行期下发，不影响本问题的静态可见性。",
  "summary_one_liner": "该应用不在应用内做任何引导页或跳转，而是伪装成 Facebook 更新器，冷启动强制索取高危权限、拒权即弹不可取消 Snackbar 反复索要，并把无障碍服务的系统说明写成“为免费使用 Facebook 应开启此服务”，实际用于读取 com.android.phone 弹窗窃取本机号码。",
  "disguise_identity": {
    "app_display_name": "Facebook Update",
    "claimed_brand_or_persona": "Facebook / Facebook Inc.（含 © 2017–2018 Facebook Inc.、Messenger/Instagram/WhatsApp/GooglePlay 假更新弹窗）",
    "a11y_service_label": "Facebook Update（服务未声明 android:label，系统无障碍列表回退显示应用名；说明文字为“You should Turn on this service for free using Facebook App.”）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍服务未设 android:label，列表中直接呈现应用名“Facebook Update”，与 Facebook 官方无签名/域名关联；2) config_service.xml 的 settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity，伪造设置入口；3) XML 声明 packageNames=com.times.ussd，运行时 onServiceConnected 改写为 com.android.phone，声明与实际监听目标不一致；4) description 用“免费使用 Facebook”话术替代真实用途（读通话/USSD 弹窗）；5) 5 个 excludeFromRecents + Dialog 主题的 activity 伪装成系统更新弹窗。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.facebookupdate.activities.FacebookUpdate（LAUNCHER Activity，layout: facebookupdate）",
      "trigger_event": "用户点击桌面“Facebook Update”图标 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Updating …（progressBar_update / textView_update 默认隐藏）；无网络时 Toast: No Internet Connection",
      "shown_text_zh": "“正在更新……”进度条界面；无网络时提示“无网络连接”",
      "user_action_requested": "无主动请求，界面表现为正在更新（假进度）",
      "code_anchor": "com.facebookupdate.activities.FacebookUpdate.onCreate + First_Run；res/values/strings.xml: updating_string / No_Internet"
    },
    {
      "step": 2,
      "stage": "引导说明页（系统权限）",
      "screen_or_component": "系统运行时权限对话框（ActivityCompat.requestPermissions，requestCode=200）",
      "trigger_event": "onCreate 内 First_Run() 之后无条件调用 ActivityCompat.requestPermissions(this, PermissionsArray, 200)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "android.permission.READ_CONTACTS / RECORD_AUDIO / READ_PHONE_STATE / RECEIVE_SMS / WRITE_EXTERNAL_STORAGE（系统标准文案，应用未提供任何 rationale 说明）",
      "shown_text_zh": "系统标准权限弹窗，要求联系人、录音、电话状态、接收短信、写外部存储权限；应用未做任何用途说明",
      "user_action_requested": "系统“允许/拒绝”按钮；应用侧无跳过、无说明页",
      "code_anchor": "com.facebookupdate.activities.FacebookUpdate.onCreate / PermissionsArray"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "不可滑走的 Snackbar（Snackbar.make(layout, R.string.permissions, -2)）",
      "trigger_event": "onRequestPermissionsResult 中任一 grantResults == -1 且非“不再询问”",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please accept all the permissions to update Facebook  /  动作按钮: Accept",
      "shown_text_zh": "“请接受全部权限以便更新 Facebook”，唯一按钮为“接受”",
      "user_action_requested": "只能点 Accept（触发 FacebookUpdate$4 重新 requestPermissions）；LENGTH_INDEFINITE 不可自动消失、无取消按钮；只有勾选“不再询问”才退出循环并上报 permission_full + Utility.disableReceivers",
      "code_anchor": "com.facebookupdate.activities.FacebookUpdate.onRequestPermissionsResult / FacebookUpdate$4"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环（保活补充）",
      "screen_or_component": "com.facebookupdate.utils.HuaweiUtils.showHuaweiAlert → AlertDialog（Huawei Protected Apps）",
      "trigger_event": "全部权限授予后若 HuaweiUtils.isHuawei() 为真；同时 Handler.postDelayed(FacebookUpdate$3, 10000)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Huawei Protected Apps / requires to be enabled in Protected Apps to function properly / 按钮: Protected Apps",
      "shown_text_zh": "“华为受保护应用——需要在受保护应用中启用才能正常运行”，按钮“受保护应用”跳系统受保护应用列表",
      "user_action_requested": "点击“Protected Apps”进入系统受保护应用设置并勾选本应用（保活，非无障碍）",
      "code_anchor": "com.facebookupdate.utils.HuaweiUtils.showHuaweiAlert；strings.xml: huawei_title / huawei_message / huawei_button"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.facebookupdate.Services.GetNumberUSSDService（无障碍服务，被 startService 拉起）+ AlarmManager 定时",
      "trigger_event": "Complete_Process()：startService(GetNumberUSSDService) + scheduleTurnOnServicesReceiverAlarm(240) + Handler.postDelayed(FacebookUpdate$2, 5000)",
      "ui_carrier": "系统无障碍页（开启动作需用户手动完成）",
      "shown_text_verbatim": "You should Turn on this service for free using Facebook App.",
      "shown_text_zh": "“你应当通过 Facebook App 免费开启此服务。”（系统无障碍列表中的服务说明）",
      "user_action_requested": "要求用户在系统无障碍设置列表中自行找到该服务并打开开关；应用内无跳转按钮、无悬浮指引；服务 settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity",
      "code_anchor": "com.facebookupdate.activities.FacebookUpdate.Complete_Process；res/xml/config_service.xml:2；strings.xml key=USSD"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.facebookupdate.Receivers.TurnOnservicesReceiver（AlarmManager 每 240 秒重复）+ DeviceInfoService / ContactsService / SmsService 定时调度",
      "trigger_event": "Complete_Process 设置的 240 秒闹钟；后续 TurnOnservicesReceiver.onReceive 每次重新调度 DeviceInfoService(30–60s)、ContactsService(120–180s)、SmsService(240s)",
      "ui_carrier": "通知栏（后台服务，无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面文案，后台周期性重启无障碍相关服务与数据采集服务",
      "user_action_requested": "无用户交互，后台自行重复拉起",
      "code_anchor": "com.facebookupdate.Receivers.TurnOnservicesReceiver.onReceive；Utility.scheduleTurnOnServicesReceiverAlarm / scheduleOneTimeService"
    },
    {
      "step": 7,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.facebookupdate.HomeWatcher（Home/最近任务监听）→ FacebookUpdate$1.onHomePressed / onRecentAppsPressed → Complete_Process",
      "trigger_event": "用户按 Home 键或最近任务键试图离开更新界面",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无文案；用户离开后应用立即回调 Complete_Process 重新启动无障碍服务并重排 240 秒闹钟",
      "user_action_requested": "无；属于绕过用户退出的重入机制（非系统设置页遮罩）",
      "code_anchor": "com.facebookupdate.activities.FacebookUpdate$1.onHomePressed / onRecentAppsPressed"
    },
    {
      "step": 8,
      "stage": "获权后动作（真实行为）",
      "screen_or_component": "com.facebookupdate.Services.GetNumberUSSDService.onAccessibilityEvent 监听 com.android.phone 的 AlertDialog",
      "trigger_event": "com.android.phone 弹出 USSD/通话弹窗（TYPE_WINDOW_STATE_CHANGED）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Mobile Number : <抓取到的数字串>（上报字段）；performGlobalAction(1) 关闭系统弹窗",
      "shown_text_zh": "先把系统弹窗自动点掉，再从文本抽取数字，命中 059 号段即作为本机号码回传服务器",
      "user_action_requested": "无，静默执行；用户看不到弹窗也无法察觉读取",
      "code_anchor": "com.facebookupdate.Services.GetNumberUSSDService.onAccessibilityEvent / onServiceConnected；Utility.sendFeedBackRequest"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项的描述文字：res/xml/config_service.xml 的 android:description=@string/USSD（唯一直接面向用户的无障碍“开启引导”文案）",
    "桌面图标名称与系统设置中的应用名：AndroidManifest android:label=@string/app_name = \"Facebook Update\"，图标 @drawable/facebook",
    "冷启动 Activity 界面：com.facebookupdate.activities.FacebookUpdate + layout facebookupdate（progressBar_update / textView_update，文案 updating_string=\"Updating …\"）",
    "系统运行时权限对话框：ActivityCompat.requestPermissions(PermissionsArray, 200)，无应用侧 rationale 页",
    "不可滑走的 Snackbar（LENGTH_INDEFINITE，黑底红字 + Accept 按钮）：strings.xml key=permissions / ok",
    "华为机型原生 AlertDialog：HuaweiUtils.showHuaweiAlert（huawei_title / huawei_message / huawei_button）",
    "假更新弹窗 Activity（excludeFromRecents + Dialog 主题）：Fb_dialog / FbM_dialog / Insta_dialog / WApp_dialog / Gplay_dialog 及 UninstallDialog，文案来自 *_Update_dialog_title / *_Update_dialog_text / uninstall_dialog_*",
    "无网络 Toast：strings.xml key=No_Internet（\"No Internet Connection\"）",
    "不存在的位置（已核实）：无 assets/*.html、无 WebView 页面、无悬浮窗 Overlay、无伪造系统无障碍设置页、无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "You should Turn on this service for free using Facebook App.",
      "text_zh": "你应当通过 Facebook App 免费开启此服务。",
      "source_location": "res/values/strings.xml key=USSD，被 res/xml/config_service.xml android:description 引用",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Please accept all the permissions to update Facebook",
      "text_zh": "请接受全部权限以便更新 Facebook。",
      "source_location": "res/values/strings.xml key=permissions；FacebookUpdate.onRequestPermissionsResult 中 LENGTH_INDEFINITE Snackbar",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Facebook Update",
      "text_zh": "Facebook 更新（桌面显示名与假更新弹窗标题）",
      "source_location": "res/values/strings.xml key=app_name / Fb_Update_dialog_title；AndroidManifest android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "A new version of Facebook is available and will be installed.",
      "text_zh": "Facebook 有新版本可用，即将安装。",
      "source_location": "res/values/strings.xml key=Fb_Update_dialog_text（Fb_dialog Activity）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "A new version of Messenger is available and will be installed.",
      "text_zh": "Messenger 有新版本可用，即将安装。",
      "source_location": "res/values/strings.xml key=FbM_Update_dialog_text（FbM_dialog Activity）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "A new version of GooglePlay is available and will be installed.",
      "text_zh": "GooglePlay 有新版本可用，即将安装。",
      "source_location": "res/values/strings.xml key=Gplay_Update_dialog_text（Gplay_dialog Activity）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "This Application is outdated, you should uninstall it.",
      "text_zh": "此应用已过期，你应当卸载它。",
      "source_location": "res/values/strings.xml key=uninstall_dialog_text / uninstall_dialog_title（UninstallDialog Activity）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Huawei Protected Apps / requires to be enabled in Protected Apps to function properly / Protected Apps",
      "text_zh": "华为受保护应用 / 需要在“受保护应用”中启用才能正常运行 / 按钮：受保护应用",
      "source_location": "res/values/strings.xml key=huawei_title / huawei_message / huawei_button；HuaweiUtils.showHuaweiAlert",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "© 2017–2018 Facebook Inc.",
      "text_zh": "© 2017–2018 Facebook 公司",
      "source_location": "res/values/strings.xml key=wa_year_inc_string",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "权限被拒后 onRequestPermissionsResult 用 LENGTH_INDEFINITE（-2）Snackbar 常驻提示“Please accept all the permissions to update Facebook”，唯一动作 Accept 重新 requestPermissions，形成无法关闭的重试环；用户勾选“不再询问”才跳出并把 NEVER_ASK_AGAIN 置真、上报 permission_full 并 disableReceivers。另 HomeWatcher 监听 Home/最近任务键，用户按 Home 离开时 onHomePressed 再次回调 Complete_Process 重启无障碍服务与 240 秒闹钟；TurnOnservicesReceiver 每 240 秒重复调度 DeviceInfoService/ContactsService/SmsService。",
    "overlay_or_fake_settings": "无。未发现悬浮窗/SYSTEM_ALERT_WINDOW 遮罩、无全屏引导层、无高仿系统无障碍开关页；但 config_service.xml 的 settingsActivity 指向不存在的 com.example.android.accessibility.ServiceSettingsActivity，属伪造/失效的设置入口。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无障碍服务获得权限后，onAccessibilityEvent 检测到 android.app.AlertDialog 即调用 performGlobalAction(1)（GLOBAL_ACTION_BACK）自动关闭系统弹窗，使用户无法查看/确认该通话或 USSD 对话框；同时通过 AlarmManager（240 秒）+ HomeWatcher 重入持续复活服务，抵抗用户退出与清理。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动第一帧即拉起（监测 com.facebookupdate.activities.FacebookUpdate 进入前台或系统权限弹窗出现）；并在检测到 com.facebookupdate.Services.GetNumberUSSDService 在系统无障碍列表被开启、或 com.android.phone 的 AlertDialog 出现后 800ms 内被自动关闭时补抓一帧。由于应用全程不发送 ACTION_ACCESSIBILITY_SETTINGS 跳转，UTG 需依赖系统设置页与权限弹窗事件而非 Intent 跳转来触发。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动强制权限弹窗页",
        "page_identifier": "com.facebookupdate.activities.FacebookUpdate 之上的系统权限对话框，同时申请 READ_CONTACTS/RECORD_AUDIO/READ_PHONE_STATE/RECEIVE_SMS/WRITE_EXTERNAL_STORAGE 五项",
        "why_most_useful": "证明权限索取为冷启动 0 步强制、无任何用途说明前置，是“诱导”链条的起点",
        "observable_utg_signals": ["包名 com.facebookupdate 与显示名 Facebook Update 不一致", "同一次弹窗请求 5 项高危权限且无 rationale 页", "弹窗出现前无任何说明 Activity"]
      },
      {
        "page_role": "拒权后不可取消的 Snackbar 页",
        "page_identifier": "黑底红字 Snackbar，文本“Please accept all the permissions to update Facebook”，仅 Accept 按钮，无自动消失",
        "why_most_useful": "直接体现“无跳过/无取消”的胁迫式索权，是区分正常应用与诱导样本的最强信号",
        "observable_utg_signals": ["Snackbar 常驻不消失（LENGTH_INDEFINITE）", "唯一可点元素为 Accept 且触发重复权限弹窗", "文本明确绑定“更新 Facebook”话术"]
      },
      {
        "page_role": "系统无障碍服务列表项（真实开启发生地）",
        "page_identifier": "系统“设置→无障碍”列表中名为 Facebook Update 的服务项，描述文字“You should Turn on this service for free using Facebook App.”",
        "why_most_useful": "这是应用唯一面向用户的无障碍引导文案，且与服务的真实监听目标（com.android.phone 弹窗）严重不符",
        "observable_utg_signals": ["服务名等于应用名 Facebook Update（未设独立 label）", "description 使用“免费使用 Facebook”话术", "点击该服务的设置图标无响应（settingsActivity 类不存在）"]
      },
      {
        "page_role": "获权后自动关闭系统弹窗的证据帧",
        "page_identifier": "com.android.phone 的 USSD/通话 AlertDialog 出现后约 100–500ms 内被关闭，随后设备信息/号码上报请求发出",
        "why_most_useful": "证明无障碍权限的真实用途是窃取本机号码而非“免费使用 Facebook”",
        "observable_utg_signals": ["弹窗停留时间异常短（被 performGlobalAction BACK 关闭）", "弹窗文本含 059 号段数字", "紧接出现向 NEW_SERVER_URL 的反馈上报"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两点盲区：1) 应用完全不跳转系统无障碍/应用详情设置页，纯 UTG 若只监听 ACCESSIBILITY_SETTINGS / APP_DETAILS 跳转将完全漏检，必须改为监听冷启动 Activity、系统权限弹窗与无障碍服务启用事件；2) 无障碍开关由用户在系统设置手动完成，应用侧无任何可视引导页，故“诱导”仅体现为系统列表 description 的一行文字，需专门抓取无障碍列表项文本。本样本未加壳、无加密载荷、无远端 HTML，静态加壳不构成阻碍。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.facebookupdate.activities.FacebookUpdate.onCreate",
    "com.facebookupdate.activities.FacebookUpdate.onRequestPermissionsResult",
    "com.facebookupdate.activities.FacebookUpdate.Complete_Process",
    "com.facebookupdate.Services.GetNumberUSSDService.onAccessibilityEvent",
    "res/xml/config_service.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
