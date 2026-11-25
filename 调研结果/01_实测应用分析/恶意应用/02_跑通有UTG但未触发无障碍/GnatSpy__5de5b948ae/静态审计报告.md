# MR_036__5de5b948ae｜GnatSpy — App System Installer

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：102.5s

## 1. 一句话核心结论

- **核心申请方式**：该应用不在自己页面里教用户开无障碍，而是把“Turn on this service for free using MeetMe App”写进系统无障碍列表的服务描述，冷启动仅静默 startService 加 240 秒闹钟拉活，授权后由无障碍服务截获 USSD 弹窗自动 BACK 关闭并窃取本机号码。
- **静态可见性说明**：无障碍引导链全部静态可见：服务描述字符串、config_service.xml、AccessibilityService 实现、闹钟拉活逻辑均为明文 DEX/XML；应用无 assets 目录、无 WebView 引导页、无 ACTION_ACCESSIBILITY_SETTINGS 跳转点，因此不存在藏于加壳/AES/远端 HTML 的引导页面。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5de5b948aeca6e0811f9625dec48601133913c24e419ce99f75596cb04503141` |
| 包名 / 年份 | `com.fakebook` / 2017 |
| 家族 / 品类 | **GnatSpy**（同池样本数：2） |
| 原始来源标识 | https://blog.trendmicro.com/trendlabs-security-intelligence/new-gnatspy-mobile-malware-family-discovered/ |
| 桌面显示名 | App System Installer |
| 引导页宣称品牌/身份 | Facebook（入口 Activity label 与登录界面仿冒）/ MeetMe App（无障碍描述宣称）/ GooglePlay、Messenger、Instagram、WhatsApp（假更新弹窗） |
| 系统无障碍列表服务名 | com.fakebook.services.GetNumberUSSDService，系统列表描述为 "You should Turn on this service for free using MeetMe App."（无独立 label，显示为服务名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：三重身份错配：应用 label "App System Installer"、入口 Activity label "Facebook"、无障碍描述宣称 "MeetMe App"，而 config_service.xml 的 packageNames 指向无关的 com.times.ussd；多个 dialog 型 Activity（Fb_dialog/FbM_dialog/Insta_dialog/WApp_dialog/Gplay_dialog）使用 singleInstance + taskAffinity="" + excludeFromRecents，且 setFinishOnTouchOutside(false)，避免在最近任务中留下痕迹；服务名为 USSD/号码相关中性命名，不含 accessibility 字样。 |
| 无障碍服务类名 | `com.fakebook.services.GetNumberUSSDService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.times.ussd |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | You should Turn on this service for free using MeetMe App. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.fakebook.activities.Fb_Home（仿 Facebook 登录页，LAUNCHER 入口） | onCreate：setContentView 后读取 com.google 账号并预填到邮箱输入框 | 原生Activity | **原文**：无（界面取自 layout 资源，app_name="Facebook"）<br>**译注**：仿 Facebook 登录界面，自动填入设备上的 Google 账号名 | 输入密码并点击登录按钮（无跳过按钮，但可退出应用） | `com.fakebook.activities.Fb_Home.onCreate` |
| 2 | 业务功能触发 | ProgressDialog（不可取消）+ Fb_Home$2.onClick / Fb_Home#k | 点击登录按钮 → k() 弹出不可取消进度框并起线程；登录成功后 Fb_Home$3$1.run 调用 Fb_Home.a(Context) 跳转 Play 商店 com.facebook.katana 详情页 | 原生Dialog | **原文**：Please Wait ... / Redirecting to Google Play Store ... / Invalid Login / Your login was invalid. We dont find your data in our database, Please Register.<br>**译注**：请稍候…… / 正在跳转 Google Play 商店…… / 登录无效 / 你的登录信息无效，数据库中无你的数据，请注册 | 等待进度框（setCancelable(false)，无取消/跳过），随后被导向 Play 商店的 Facebook 页面 | `com.fakebook.activities.Fb_Home#k、com.fakebook.activities.Fb_Home#a(android.content.Context)` |
| 3 | 业务功能触发 | Fb_Home#j 静默 startService + AlarmManager 排 240s 闹钟 | onCreate 内 j()：若有网络则 startService(GetNumberUSSDService) 并 i.f(context, 240) | 不可静态还原 | **原文**：无（无任何 UI 呈现）<br>**译注**：无提示，静默尝试拉起无障碍服务并排 240 秒后的 TurnOnservicesReceiver 闹钟 | 无需操作；应用不弹任何“去设置开启无障碍”的页面 | `com.fakebook.activities.Fb_Home#j` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载服务列表项（com.fakebook.services.GetNumberUSSDService） | 无应用内跳转（静态检索无 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS），用户须自行进入系统设置查看 | 系统无障碍页 | **原文**：You should Turn on this service for free using MeetMe App.<br>**译注**：你应当为使用 MeetMe App 免费开启此服务 | 在系统无障碍列表中手动点开并开启该服务（无应用侧按钮、无取消/跳过逻辑） | `res/xml/config_service.xml（android:description=@string/USSD）、res/values/strings.xml#L29` |
| 5 | 获权后动作 | com.fakebook.services.GetNumberUSSDService#onServiceConnected / onAccessibilityEvent | 系统绑定服务后 onServiceConnected 重设 packageNames=com.android.phone、eventTypes=32；收到 android.app.AlertDialog 类型事件时 | 不可静态还原 | **原文**：无（代码内无文案；以 performGlobalAction(1) 主动关闭 USSD 弹窗）<br>**译注**：自动按下返回键关掉系统 USSD 弹窗，提取其中号码，若含 059 则保存为 mobile_number 并上报服务器 | 用户无感知；弹窗被自动消除，号码被静默窃取 | `com.fakebook.services.GetNumberUSSDService#onAccessibilityEvent` |
| 6 | 拒权反馈循环 | com.fakebook.receivers.TurnOnservicesReceiver（240s 闹钟到期） | onReceive：有网络时 i.q(context) 及按 WiFi/移动数据条件排 DeviceInfoService(30-60s)/ContactsService(120-180s)/SmsService(240-300s) | 不可静态还原 | 无 | 无需操作；未发现 onResume 死循环重跳或定时拉起设置页的强制循环 | `com.fakebook.receivers.TurnOnservicesReceiver#onReceive` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项描述：res/xml/config_service.xml 的 android:description=@string/USSD → "You should Turn on this service for free using MeetMe App."（res/values/strings.xml#L29）
- 仿 Facebook 登录页 Fb_Home（原生 Activity，layout 资源），含 app_name="Facebook"、Invalid Login/Invalid Msg/Signup_Toast 等文案
- 不可取消 ProgressDialog：Please Wait ... / Just a sec ... / Logging In / Redirecting to Google Play Store ...（strings.xml，由 Fb_Home#k 弹出）
- 假更新弹窗 Activity（Fb_dialog / FbM_dialog / Insta_dialog / WApp_dialog / Gplay_dialog，Theme Dialog + setFinishOnTouchOutside(false)）："A new version of Facebook/Messenger/Instagram/WhatsApp/GooglePlay is available and will be installed."
- 故障/卸载恐吓弹窗：Error_Alert="Stop Service!"、Error_Message="This version is not compatible with your device , It Will Be Uninstalled!"、uninstall_dialog_title="Uninstall Meet Me"、uninstall_dialog_text="This Application is outdated, you should uninstall it."
- Huawei 保活引导文案（huawei_title/huawei_message/huawei_button："Huawei Protected Apps"/"requires to be enabled in Protected Apps to function properly"/"Protected Apps"），属后台保活引导而非无障碍引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | You should Turn on this service for free using MeetMe App. | 你应当为使用 MeetMe App 免费开启此服务。 | `res/values/strings.xml key=USSD（被 res/xml/config_service.xml 的 android:description 引用）` | 教唆忽视警告 |
| en | A new version of Facebook is available and will be installed. | Facebook 有新版本可用，即将安装。 | `res/values/strings.xml key=Fb_Update_dialog_text（Fb_dialog 使用）` | 假更新 |
| en | A new version of Messenger is available and will be installed. | Messenger 有新版本可用，即将安装。 | `res/values/strings.xml key=FbM_Update_dialog_text（FbM_dialog 使用）` | 假更新 |
| en | A new version of Instagram is available and will be installed. | Instagram 有新版本可用，即将安装。 | `res/values/strings.xml key=Insta_Update_dialog_text（Insta_dialog 使用）` | 假更新 |
| en | A new version of GooglePlay is available and will be installed. | GooglePlay 有新版本可用，即将安装。 | `res/values/strings.xml key=Gplay_Update_dialog_text（Gplay_dialog 使用）` | 假更新 |
| en | This version is not compatible with your device , It Will Be Uninstalled! | 此版本与你的设备不兼容，它将被卸载！ | `res/values/strings.xml key=Error_Message` | 故障恐吓 |
| en | Stop Service! | 停止服务！ | `res/values/strings.xml key=Error_Alert` | 故障恐吓 |
| en | This Application is outdated, you should uninstall it. | 此应用已过期，你应当卸载它。 | `res/values/strings.xml key=uninstall_dialog_text（标题 uninstall_dialog_title="Uninstall Meet Me"，UninstallDialog）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：未发现针对无障碍设置页的拒权循环：无 onResume 重跳、无定时拉起设置页、无 OVERLAY 压栈提示；未授权时 Fb_Home#j 的 startService 静默失败，240 秒后 TurnOnservicesReceiver 仅按网络类型继续排 DeviceInfo/Contacts/Sms 采集服务（后台保活与采集推进，而非再弹引导）。
- **遮罩叠层 / 高仿系统设置页**：无。包内无 assets/、无 WebView、无自定义高仿无障碍开关页；仅 OverlayShowingService 存在（exported=false，用于其他悬浮展示），未见用于叠放无障碍引导遮罩的调用链。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。应用 targetSdkVersion=22，无 Android 13 受限设置（应用详情右上角菜单允许受限设置）或 Session 安装器绕过的教学文案/代码。
- **获权后即时行为与防撤权机制**：获权后由 GetNumberUSSDService#onAccessibilityEvent 对 android.app.AlertDialog 事件执行 performGlobalAction(1)（GLOBAL_ACTION_BACK）主动关闭 USSD 弹窗，属于自动消隐/干扰而非撤权拦截；未见监听设置页以 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：优先在冷启动 Fb_Home.onCreate 完成后、以及 startService(GetNumberUSSDService)+240s 闹钟触发瞬间拉 UTG；同时在系统无障碍设置页停留期间抓取服务列表项描述（本样本的引导文案只存在于该处，不在应用 UI 内）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：盲区在于“引导”发生在应用之外的系统无障碍列表描述中：若 UTG 只停留在应用自身窗口栈，将看不到任何开启无障碍的诱导文案，易误判为无引导；另外应用从不主动跳转设置页，纯 UTG 若只监听 Activity 跳转（ACCESSIBILITY_SETTINGS/APP_DETAILS）会完全漏检，需改为监听 startService(GetNumberUSSDService) 与无障碍服务绑定事件。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载服务中名为 GetNumberUSSDService 的条目及其描述文本 | 本样本唯一的“引导文案”载体，直接决定是否存在借系统列表实施诱导/身份冒充 | 描述文本 "You should Turn on this service for free using MeetMe App."；服务名不含 accessibility 语义、与描述宣称品牌 MeetMe 不一致；列表项与桌面应用名 App System Installer 不一致 |
| **冷启动入口登录页** | com.fakebook.activities.Fb_Home，含预填 Google 账号的登录表单 | 确认仿冒 Facebook 身份与是否存在登录后跳商店/假更新引导 | 标题/品牌字样 Facebook 与桌面名 App System Installer 不一致；邮箱框已被自动填入设备 Google 账号；登录按钮点击后出现不可取消 Please Wait 进度框 |
| **假更新/故障恐吓弹窗** | Theme.Dialog 型 Activity：Fb_dialog / FbM_dialog / Insta_dialog / WApp_dialog / Gplay_dialog / UninstallDialog | 区分诱导话术属于假更新还是故障恐吓，并观察是否借“即将安装”引导安装内嵌 APK | 文案 "A new version of X is available and will be installed."；弹窗点击外部不消失（setFinishOnTouchOutside(false)）；确认后跳系统安装器（android.intent.action.VIEW + application/vnd.android.package-archive） |
| **获权后 USSD 弹窗被自动消隐** | com.android.phone 的 USSD/AlertDialog 窗口瞬间消失，无障碍服务为 GetNumberUSSDService | 直接验证无障碍权限被用于自动 BACK 关闭弹窗并窃取号码 | USSD 弹窗出现后约 100ms 内被 BACK 关闭；无用户触摸输入却发生窗口状态变化；设备号码被写入 Prefs key mobile_number |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.fakebook.services.GetNumberUSSDService#onAccessibilityEvent`
- `com.fakebook.services.GetNumberUSSDService#onServiceConnected`
- `res/xml/config_service.xml`
- `com.fakebook.activities.Fb_Home#j`
- `com.fakebook.receivers.TurnOnservicesReceiver#onReceive`
- `com.fakebook.activities.Fb_dialog#a`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（UTG 运行期视角）

- **无障碍权限的“引导”并不存在于应用自己的页面中**：静态检索未发现任何 `android.settings.ACCESSIBILITY_SETTINGS` / `APPLICATION_DETAILS_SETTINGS` 跳转点，也没有 WebView/HTML 教学页、悬浮遮罩或高仿设置页（`assets/` 目录不存在，`res/layout*` 无相关引导布局）。唯一的“引导文案”是**系统无障碍列表里的服务描述**：`@string/USSD` = “You should Turn on this service for free using MeetMe App.”（[res/values/strings.xml#L29](<resource-unit:#1 file:res/values/strings.xml#L29>)），由 [res/xml/config_service.xml](<resource-unit:#1 file:res/xml/config_service.xml>) 的 `android:description` 引用，用户只能自行在系统设置里勾选，属于典型的“借系统列表当广告位”的冷启动 0 步诱导。
- **该服务本身是 USSD 截获器而非引导器**：`onServiceConnected` 把 `packageNames` 改为 `com.android.phone`、`eventTypes=32`（窗口状态变化）；`onAccessibilityEvent` 在事件类名为 `android.app.AlertDialog` 时先 `performGlobalAction(1)`（GLOBAL_ACTION_BACK）自行关掉弹窗，再用正则 `[^0-9?!\\.]` 提取号码，若含 `059` 就写入 `mobile_number` 并上报 —— 即窃取 USSD 弹窗中的本机号码并抹掉可见痕迹（[GetNumberUSSDService#onAccessibilityEvent](<resource-unit:#1.dex1 code:com.fakebook.services.GetNumberUSSDService#onAccessibilityEvent>)、[#onServiceConnected](<resource-unit:#1.dex1 code:com.fakebook.services.GetNumberUSSDService#onServiceConnected>)）。
- **冷启动只做“拉活 + 排闹钟”，不强制跳设置**：[Fb_Home#j](<resource-unit:#1.dex1 code:com.fakebook.activities.Fb_Home#j>) 在 `onCreate` 里 `startService(GetNumberUSSDService)`（未授权时无效）并排 240s 闹钟；[TurnOnservicesReceiver#onReceive](<resource-unit:#1.dex1 code:com.fakebook.receivers.TurnOnservicesReceiver#onReceive>) 到期后按 WiFi/移动数据条件拉起 DeviceInfo/Contacts/Sms 采集服务。未发现 onResume 死循环重跳或定时拉起设置页的拒权循环。
- **身份与话术高度分裂**：应用 label 为 `App System Installer`，入口 Activity 的 label 为 `Facebook`，无障碍描述却宣称 “MeetMe App”，服务目标包又是 `com.times.ussd`；配合 `Fb_Update_dialog_text` 等“假更新”文案和 `uninstall_dialog_title`=“Uninstall Meet Me” 的故障恐吓文案共同作为诱饵/掩护。
- **可见性**：该引导链（描述字符串、服务配置、onAccessibilityEvent 逻辑）全部明文可见，未加壳；无远端下发引导页。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链全部静态可见：服务描述字符串、config_service.xml、AccessibilityService 实现、闹钟拉活逻辑均为明文 DEX/XML；应用无 assets 目录、无 WebView 引导页、无 ACTION_ACCESSIBILITY_SETTINGS 跳转点，因此不存在藏于加壳/AES/远端 HTML 的引导页面。",
  "summary_one_liner": "该应用不在自己页面里教用户开无障碍，而是把“Turn on this service for free using MeetMe App”写进系统无障碍列表的服务描述，冷启动仅静默 startService 加 240 秒闹钟拉活，授权后由无障碍服务截获 USSD 弹窗自动 BACK 关闭并窃取本机号码。",
  "disguise_identity": {
    "app_display_name": "App System Installer",
    "claimed_brand_or_persona": "Facebook（入口 Activity label 与登录界面仿冒）/ MeetMe App（无障碍描述宣称）/ GooglePlay、Messenger、Instagram、WhatsApp（假更新弹窗）",
    "a11y_service_label": "com.fakebook.services.GetNumberUSSDService，系统列表描述为 \"You should Turn on this service for free using MeetMe App.\"（无独立 label，显示为服务名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "三重身份错配：应用 label \"App System Installer\"、入口 Activity label \"Facebook\"、无障碍描述宣称 \"MeetMe App\"，而 config_service.xml 的 packageNames 指向无关的 com.times.ussd；多个 dialog 型 Activity（Fb_dialog/FbM_dialog/Insta_dialog/WApp_dialog/Gplay_dialog）使用 singleInstance + taskAffinity=\"\" + excludeFromRecents，且 setFinishOnTouchOutside(false)，避免在最近任务中留下痕迹；服务名为 USSD/号码相关中性命名，不含 accessibility 字样。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.fakebook.activities.Fb_Home（仿 Facebook 登录页，LAUNCHER 入口）",
      "trigger_event": "onCreate：setContentView 后读取 com.google 账号并预填到邮箱输入框",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（界面取自 layout 资源，app_name=\"Facebook\"）",
      "shown_text_zh": "仿 Facebook 登录界面，自动填入设备上的 Google 账号名",
      "user_action_requested": "输入密码并点击登录按钮（无跳过按钮，但可退出应用）",
      "code_anchor": "com.fakebook.activities.Fb_Home.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "ProgressDialog（不可取消）+ Fb_Home$2.onClick / Fb_Home#k",
      "trigger_event": "点击登录按钮 → k() 弹出不可取消进度框并起线程；登录成功后 Fb_Home$3$1.run 调用 Fb_Home.a(Context) 跳转 Play 商店 com.facebook.katana 详情页",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please Wait ... / Redirecting to Google Play Store ... / Invalid Login / Your login was invalid. We dont find your data in our database, Please Register.",
      "shown_text_zh": "请稍候…… / 正在跳转 Google Play 商店…… / 登录无效 / 你的登录信息无效，数据库中无你的数据，请注册",
      "user_action_requested": "等待进度框（setCancelable(false)，无取消/跳过），随后被导向 Play 商店的 Facebook 页面",
      "code_anchor": "com.fakebook.activities.Fb_Home#k、com.fakebook.activities.Fb_Home#a(android.content.Context)"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "Fb_Home#j 静默 startService + AlarmManager 排 240s 闹钟",
      "trigger_event": "onCreate 内 j()：若有网络则 startService(GetNumberUSSDService) 并 i.f(context, 240)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（无任何 UI 呈现）",
      "shown_text_zh": "无提示，静默尝试拉起无障碍服务并排 240 秒后的 TurnOnservicesReceiver 闹钟",
      "user_action_requested": "无需操作；应用不弹任何“去设置开启无障碍”的页面",
      "code_anchor": "com.fakebook.activities.Fb_Home#j"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载服务列表项（com.fakebook.services.GetNumberUSSDService）",
      "trigger_event": "无应用内跳转（静态检索无 ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS），用户须自行进入系统设置查看",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "You should Turn on this service for free using MeetMe App.",
      "shown_text_zh": "你应当为使用 MeetMe App 免费开启此服务",
      "user_action_requested": "在系统无障碍列表中手动点开并开启该服务（无应用侧按钮、无取消/跳过逻辑）",
      "code_anchor": "res/xml/config_service.xml（android:description=@string/USSD）、res/values/strings.xml#L29"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.fakebook.services.GetNumberUSSDService#onServiceConnected / onAccessibilityEvent",
      "trigger_event": "系统绑定服务后 onServiceConnected 重设 packageNames=com.android.phone、eventTypes=32；收到 android.app.AlertDialog 类型事件时",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（代码内无文案；以 performGlobalAction(1) 主动关闭 USSD 弹窗）",
      "shown_text_zh": "自动按下返回键关掉系统 USSD 弹窗，提取其中号码，若含 059 则保存为 mobile_number 并上报服务器",
      "user_action_requested": "用户无感知；弹窗被自动消除，号码被静默窃取",
      "code_anchor": "com.fakebook.services.GetNumberUSSDService#onAccessibilityEvent"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.fakebook.receivers.TurnOnservicesReceiver（240s 闹钟到期）",
      "trigger_event": "onReceive：有网络时 i.q(context) 及按 WiFi/移动数据条件排 DeviceInfoService(30-60s)/ContactsService(120-180s)/SmsService(240-300s)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "未获无障碍权限时不会重跳设置页，而是继续排闹钟拉起设备信息、联系人、短信采集服务",
      "user_action_requested": "无需操作；未发现 onResume 死循环重跳或定时拉起设置页的强制循环",
      "code_anchor": "com.fakebook.receivers.TurnOnservicesReceiver#onReceive"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项描述：res/xml/config_service.xml 的 android:description=@string/USSD → \"You should Turn on this service for free using MeetMe App.\"（res/values/strings.xml#L29）",
    "仿 Facebook 登录页 Fb_Home（原生 Activity，layout 资源），含 app_name=\"Facebook\"、Invalid Login/Invalid Msg/Signup_Toast 等文案",
    "不可取消 ProgressDialog：Please Wait ... / Just a sec ... / Logging In / Redirecting to Google Play Store ...（strings.xml，由 Fb_Home#k 弹出）",
    "假更新弹窗 Activity（Fb_dialog / FbM_dialog / Insta_dialog / WApp_dialog / Gplay_dialog，Theme Dialog + setFinishOnTouchOutside(false)）：\"A new version of Facebook/Messenger/Instagram/WhatsApp/GooglePlay is available and will be installed.\"",
    "故障/卸载恐吓弹窗：Error_Alert=\"Stop Service!\"、Error_Message=\"This version is not compatible with your device , It Will Be Uninstalled!\"、uninstall_dialog_title=\"Uninstall Meet Me\"、uninstall_dialog_text=\"This Application is outdated, you should uninstall it.\"",
    "Huawei 保活引导文案（huawei_title/huawei_message/huawei_button：\"Huawei Protected Apps\"/\"requires to be enabled in Protected Apps to function properly\"/\"Protected Apps\"），属后台保活引导而非无障碍引导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "You should Turn on this service for free using MeetMe App.",
      "text_zh": "你应当为使用 MeetMe App 免费开启此服务。",
      "source_location": "res/values/strings.xml key=USSD（被 res/xml/config_service.xml 的 android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "A new version of Facebook is available and will be installed.",
      "text_zh": "Facebook 有新版本可用，即将安装。",
      "source_location": "res/values/strings.xml key=Fb_Update_dialog_text（Fb_dialog 使用）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "A new version of Messenger is available and will be installed.",
      "text_zh": "Messenger 有新版本可用，即将安装。",
      "source_location": "res/values/strings.xml key=FbM_Update_dialog_text（FbM_dialog 使用）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "A new version of Instagram is available and will be installed.",
      "text_zh": "Instagram 有新版本可用，即将安装。",
      "source_location": "res/values/strings.xml key=Insta_Update_dialog_text（Insta_dialog 使用）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "A new version of GooglePlay is available and will be installed.",
      "text_zh": "GooglePlay 有新版本可用，即将安装。",
      "source_location": "res/values/strings.xml key=Gplay_Update_dialog_text（Gplay_dialog 使用）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "This version is not compatible with your device , It Will Be Uninstalled!",
      "text_zh": "此版本与你的设备不兼容，它将被卸载！",
      "source_location": "res/values/strings.xml key=Error_Message",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Stop Service!",
      "text_zh": "停止服务！",
      "source_location": "res/values/strings.xml key=Error_Alert",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "This Application is outdated, you should uninstall it.",
      "text_zh": "此应用已过期，你应当卸载它。",
      "source_location": "res/values/strings.xml key=uninstall_dialog_text（标题 uninstall_dialog_title=\"Uninstall Meet Me\"，UninstallDialog）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "未发现针对无障碍设置页的拒权循环：无 onResume 重跳、无定时拉起设置页、无 OVERLAY 压栈提示；未授权时 Fb_Home#j 的 startService 静默失败，240 秒后 TurnOnservicesReceiver 仅按网络类型继续排 DeviceInfo/Contacts/Sms 采集服务（后台保活与采集推进，而非再弹引导）。",
    "overlay_or_fake_settings": "无。包内无 assets/、无 WebView、无自定义高仿无障碍开关页；仅 OverlayShowingService 存在（exported=false，用于其他悬浮展示），未见用于叠放无障碍引导遮罩的调用链。",
    "restricted_settings_13plus_coaching": "无。应用 targetSdkVersion=22，无 Android 13 受限设置（应用详情右上角菜单允许受限设置）或 Session 安装器绕过的教学文案/代码。",
    "post_grant_anti_removal": "获权后由 GetNumberUSSDService#onAccessibilityEvent 对 android.app.AlertDialog 事件执行 performGlobalAction(1)（GLOBAL_ACTION_BACK）主动关闭 USSD 弹窗，属于自动消隐/干扰而非撤权拦截；未见监听设置页以 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "优先在冷启动 Fb_Home.onCreate 完成后、以及 startService(GetNumberUSSDService)+240s 闹钟触发瞬间拉 UTG；同时在系统无障碍设置页停留期间抓取服务列表项描述（本样本的引导文案只存在于该处，不在应用 UI 内）。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载服务中名为 GetNumberUSSDService 的条目及其描述文本",
        "why_most_useful": "本样本唯一的“引导文案”载体，直接决定是否存在借系统列表实施诱导/身份冒充",
        "observable_utg_signals": ["描述文本 \"You should Turn on this service for free using MeetMe App.\"", "服务名不含 accessibility 语义、与描述宣称品牌 MeetMe 不一致", "列表项与桌面应用名 App System Installer 不一致"]
      },
      {
        "page_role": "冷启动入口登录页",
        "page_identifier": "com.fakebook.activities.Fb_Home，含预填 Google 账号的登录表单",
        "why_most_useful": "确认仿冒 Facebook 身份与是否存在登录后跳商店/假更新引导",
        "observable_utg_signals": ["标题/品牌字样 Facebook 与桌面名 App System Installer 不一致", "邮箱框已被自动填入设备 Google 账号", "登录按钮点击后出现不可取消 Please Wait 进度框"]
      },
      {
        "page_role": "假更新/故障恐吓弹窗",
        "page_identifier": "Theme.Dialog 型 Activity：Fb_dialog / FbM_dialog / Insta_dialog / WApp_dialog / Gplay_dialog / UninstallDialog",
        "why_most_useful": "区分诱导话术属于假更新还是故障恐吓，并观察是否借“即将安装”引导安装内嵌 APK",
        "observable_utg_signals": ["文案 \"A new version of X is available and will be installed.\"", "弹窗点击外部不消失（setFinishOnTouchOutside(false)）", "确认后跳系统安装器（android.intent.action.VIEW + application/vnd.android.package-archive）"]
      },
      {
        "page_role": "获权后 USSD 弹窗被自动消隐",
        "page_identifier": "com.android.phone 的 USSD/AlertDialog 窗口瞬间消失，无障碍服务为 GetNumberUSSDService",
        "why_most_useful": "直接验证无障碍权限被用于自动 BACK 关闭弹窗并窃取号码",
        "observable_utg_signals": ["USSD 弹窗出现后约 100ms 内被 BACK 关闭", "无用户触摸输入却发生窗口状态变化", "设备号码被写入 Prefs key mobile_number"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "盲区在于“引导”发生在应用之外的系统无障碍列表描述中：若 UTG 只停留在应用自身窗口栈，将看不到任何开启无障碍的诱导文案，易误判为无引导；另外应用从不主动跳转设置页，纯 UTG 若只监听 Activity 跳转（ACCESSIBILITY_SETTINGS/APP_DETAILS）会完全漏检，需改为监听 startService(GetNumberUSSDService) 与无障碍服务绑定事件。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.fakebook.services.GetNumberUSSDService#onAccessibilityEvent",
    "com.fakebook.services.GetNumberUSSDService#onServiceConnected",
    "res/xml/config_service.xml",
    "com.fakebook.activities.Fb_Home#j",
    "com.fakebook.receivers.TurnOnservicesReceiver#onReceive",
    "com.fakebook.activities.Fb_dialog#a"
  ]
}
```

</details>
