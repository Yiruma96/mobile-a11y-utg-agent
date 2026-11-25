# MR_008__8d4e75cb28｜Xavier — S6 Launcher

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：113.2s

## 1. 一句话核心结论

- **核心申请方式**：以 S6 Launcher 桌面美化名义，在设置页通知相关开关被点击时弹出原生 AlertDialog 说明并一键跳系统无障碍设置，拒权后仅回读状态不重跳，获权后仅用无障碍服务广播回传通知图标与文本供桌面显示。
- **静态可见性说明**：无障碍引导链（Manifest 服务声明、res/xml/notification_accessibility_service.xml、strings.xml 文案、LauncherSetting.c() 弹窗、qw/qx.onClick 系统设置跳转、onActivityResult 回读）全部静态可见，未加壳、无 AES 密文引导页、无远端 HTML 承载引导。assets 下 Privacy.html/help.html/licenses.html 为本地静态说明页，未参与无障碍引导。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8d4e75cb28b8091d79b3f175020bf7ec8d01468ac75569a7c526c59737875594` |
| 包名 / 年份 | `com.helpdesk.slauncher` / 2017 |
| 家族 / 品类 | **Xavier**（同池样本数：41） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/f/analyzing-xavier-information-stealing-ad-library-android.html |
| 桌面显示名 | S6 Launcher |
| 引导页宣称品牌/身份 | S6 Launcher（借三星 Galaxy S6 桌面/Launcher 品牌身份） |
| 系统无障碍列表服务名 | S6 Launcher（service 未声明 android:label，回落到 @string/application_name；描述为 To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting.） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.helpdesk.slauncher 与类路径 com.helpdesk.* 与宣称的三星 S6 品牌不一致；服务列表项复用应用名而非独立服务名，使系统无障碍列表直接呈现品牌名；未发现空白/换行挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool（targetSdk 19，无该字段） |
| 无障碍服务类名 | `com.helpdesk.accessibility.NotificationAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, READ_CONTACTS, READ_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.helpdesk.slauncher.LauncherSetting（PreferenceActivity，入口 VIEW com.helpdesk.slauncher://kk_setting） | 用户进入设置页后点击“显示通知内容”相关 Preference 的 onPreferenceClick（调用 LauncherSetting.c(LauncherSetting)） | 原生Activity | **原文**：（设置页自身文案未逐字核验）<br>**译注**：桌面设置页中的通知显示开关项 | 用户需主动点击该设置项开关，无强制，可退出设置页 | `com.helpdesk.slauncher.LauncherSetting.onResume / com.helpdesk.slauncher.pr.onPreferenceClick 等 → LauncherSetting.c(LauncherSetting)` |
| 2 | 引导说明页 | 原生 AlertDialog（标题 pref_desktop_show_notification_title，正文 pref_desktop_show_notification_content，按钮 yes/no） | 点击通知相关设置开关后立即弹出（c(LauncherSetting) 内 AlertDialog$Builder 构建） | 原生Dialog | **原文**：To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting. <br>Do you want to open Accessibility Settings?<br>**译注**：要启用通知功能，请在“无障碍设置”中开启 S6 Launcher 无障碍服务。是否要打开无障碍设置？ | 点击“是/yes”跳转系统无障碍设置；点击“否/no”直接关闭（setNegativeButton 监听器为 null，可取消，非强制） | `com.helpdesk.slauncher.LauncherSetting.c(LauncherSetting) + res/values/strings.xml: pref_desktop_show_notification_content` |
| 3 | 跳受限设置 | 系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS | 用户在弹窗点“是” → qw.onClick(DialogInterface,int) | 系统无障碍页 | 无 | 用户在系统页面手动找到 S6 Launcher 条目并打开开关 | `com.helpdesk.slauncher.qw.onClick（startActivityForResult("android.settings.ACCESSIBILITY_SETTINGS", 2001)）` |
| 4 | 拒权反馈循环 | 返回 LauncherSetting，onActivityResult(requestCode=2001) 回读服务真实启用状态 | 用户从系统无障碍设置返回（无论是否开启） | 原生Activity | 无 | 无需操作；未开启时保持未勾选，无重跳、无定时拉起、无遮罩 | `com.helpdesk.slauncher.LauncherSetting.onActivityResult case 2001 + com.helpdesk.slauncher.util.u.a(Context,String)` |
| 5 | 跳受限设置 | android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS（SDK>=18）或 ACCESSIBILITY_SETTINGS（SDK<18） | 另一通知权限设置项点击 → qx.onClick | 系统无障碍页 | 无 | 用户手动勾选授权；同样可取消返回 | `com.helpdesk.slauncher.qx.onClick` |
| 6 | 获权后动作 | NotificationAccessibilityService（startService）+ Launcher 内 CHANGE_NOTIFICATION 广播接收器 | Launcher.a(boolean) 中 this.cj 为真时调用 NotificationAccessibilityService.a(this)；服务 onServiceConnected 后开始接收通知事件 | 系统无障碍页 | 无 | 无；未见获权后自动点确认、自动授权或阻止撤权动作 | `com.helpdesk.slauncher.Launcher.a(boolean) + NotificationAccessibilityService.onAccessibilityEvent + NotificationAccessibilityService.a(Context)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- LauncherSetting 内原生不可持久 AlertDialog：标题 pref_desktop_show_notification_title + 正文 pref_desktop_show_notification_content（含“是否要打开无障碍设置”问句），按钮 yes/no
- 系统无障碍列表条目描述：res/xml/notification_accessibility_service.xml 的 android:description → @string/accessibility_service_description（字符串硬编码 S6 Launcher 品牌）
- 系统无障碍列表条目名称：service 未设 android:label，回落到 application 的 @string/application_name = S6 Launcher
- 本地静态 HTML assets/Privacy.html、assets/help.html、assets/licenses.html：为隐私政策/帮助/开源许可说明，未承载无障碍引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting. <br>Do you want to open Accessibility Settings? | 要启用通知功能，请在“无障碍设置”中开启 S6 Launcher 无障碍服务。是否要打开无障碍设置？ | `res/values/strings.xml key=pref_desktop_show_notification_content（LauncherSetting.c(LauncherSetting) 作为 AlertDialog message）` | 良性透明说明 |
| en | To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting. | 要启用通知功能，请在“无障碍设置”中开启 S6 Launcher 无障碍服务。 | `res/values/strings.xml key=accessibility_service_description（res/xml/notification_accessibility_service.xml android:description）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无强制循环：onActivityResult(requestCode=2001) 仅回读 util.u.a() 真实启用状态并同步 CheckBox，返回设置页或退出均不再重跳；onResume 未包含无障碍跳转或定时器拉起逻辑
- **遮罩叠层 / 高仿系统设置页**：无。未使用 TYPE_ACCESSIBILITY_OVERLAY / SYSTEM_ALERT_WINDOW 叠放引导遮罩，未实现高仿系统无障碍开关页，跳转为真实系统设置 Activity
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk 19，无“允许受限设置”分步教学；未见 SESSION_INSTALLER 落地代码）
- **获权后即时行为与防撤权机制**：无。未见获权后自动点击确认、自动授权或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权；仅存在用户主动触发的 stopService 撤权路径
- **良性降级 / 替代方案**：具降级机制：用户拒绝授权时弹窗可取消、返回后仅保持开关未勾选，桌面其余功能继续可用，通知显示能力单独缺失

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测 LauncherSetting 页面内弹出 AlertDialog 的瞬间（标题/正文含 'S6 Launcher Accessibility Service'），以及紧随其后的 startActivityForResult('android.settings.ACCESSIBILITY_SETTINGS') / startActivity('android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS') 调用；也可在跳转系统设置 800ms 后截取无障碍列表条目
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导链纯文本、纯原生控件，静态与 UTG 均可读。仅需注意无障碍服务在系统列表中呈现的是应用名 'S6 Launcher' 而非服务类名，按类名检索会漏；另本轮未覆盖 com.helpdesk.ad 广告 SDK 与 update.* 自更新链的后续诱导，若关注 Xavier 家族典型载荷需另开链核验。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **设置页通知开关触发的引导弹窗页** | LauncherSetting Activity 上的 AlertDialog：标题含 notification，正文含 'S6 Launcher Accessibility Service'，按钮为 yes/no | 这是该应用唯一的无障碍劝导载体，可确认是否可取消、文案是否如实说明用途，是区分良性说明与诱导的关键页 | 弹窗正文文本 'To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting.'；存在 no 取消按钮（可点关闭）；弹窗下方仍为设置项列表，非全屏遮罩 |
| **系统无障碍服务列表项** | 系统设置无障碍列表中的 'S6 Launcher' 条目及其描述文本 | 核验无障碍列表项名称是否借用 S6 品牌、描述是否与实际能力（仅通知事件、canRetrieveWindowContent=false）一致 | 条目名称 'S6 Launcher'；描述 'To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting.'；开关初始为关闭且无自动开启 |
| **返回设置页后的状态回写页** | LauncherSetting 中通知相关 CheckBoxPreference 的勾选状态 | 验证拒权后是否发生重跳/循环压迫（本应用预期为无循环、状态如实回写） | 返回后无新弹窗；开关未勾选且无倒计时/二次劝导；未出现悬浮遮罩层 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.helpdesk.slauncher.LauncherSetting.c(com.helpdesk.slauncher.LauncherSetting)`
- `com.helpdesk.slauncher.qw.onClick(android.content.DialogInterface,int)`
- `com.helpdesk.slauncher.qx.onClick(android.content.DialogInterface,int)`
- `com.helpdesk.slauncher.LauncherSetting.onActivityResult(int,int,android.content.Intent)`
- `com.helpdesk.slauncher.Launcher.a(boolean)`
- `res/values/strings.xml (pref_desktop_show_notification_content / accessibility_service_description)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

- **无障碍服务本身的行为与"通知/桌面美化"说明一致**：[NotificationAccessibilityService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.helpdesk.accessibility.NotificationAccessibilityService#onAccessibilityEvent>) 只处理 `TYPE_NOTIFICATION_STATE_CHANGED(64)` 与 `TYPE_WINDOW_STATE_CHANGED(32)`，把通知包名、图标、`largeIcon` 与文本通过广播 `com.kk.launcher.accessibility.CHANGE_NOTIFICATION` 回传给桌面；配置 [res/xml/notification_accessibility_service.xml](<resource-unit:#1 file:res/xml/notification_accessibility_service.xml>) 声明 `canRetrieveWindowContent="false"`，即**不具备窗口内容读取、点击注入或遮罩能力**，这与 DEX 预筛里 `A11Y_OVERLAY` 的标签不一致（未见 overlay 实现）。
- **引导流程是"设置项按需触发 + 标准系统跳转"，不是冷启动强制**：唯一弹窗入口在 [LauncherSetting.c(LauncherSetting)](<resource-unit:#1.dex1 code:com.helpdesk.slauncher.LauncherSetting#c>)（`AlertDialog`，`setPositiveButton(R$string.yes, new qw(this))` / `setNegativeButton(R$string.no, null)`），由通知相关设置项的 `onPreferenceClick` 触发，文案即 `pref_desktop_show_notification_content`。
- **跳转点干净**：[qw.onClick()](<resource-unit:#1.dex1 code:com.helpdesk.slauncher.qw#onClick>) 用 `startActivityForResult("android.settings.ACCESSIBILITY_SETTINGS", 2001)`；[qx.onClick()](<resource-unit:#1.dex1 code:com.helpdesk.slauncher.qx#onClick>) 在 SDK≥18 跳 `ACTION_NOTIFICATION_LISTENER_SETTINGS`。均为系统设置页，**无高仿无障碍开关页、无悬浮遮罩、无 `TYPE_ACCESSIBILITY_OVERLAY`**。
- **拒权无循环压迫**：[LauncherSetting.onActivityResult()](<resource-unit:#1.dex1 code:com.helpdesk.slauncher.LauncherSetting#onActivityResult>) 的 `case 2001` 仅用 `util.u.a(this,"com.helpdesk.slauncher/...NotificationAccessibilityService")` 回读真实开关状态并 `U.setChecked(...)`，返回后不再重跳；`onResume` 也无定时/死循环拉起。属良性降级。
- **获权后动作**：[Launcher.a(boolean)](<resource-unit:#1.dex1 code:com.helpdesk.slauncher.Launcher#a>) 在 `this.cj` 为真时调用 `NotificationAccessibilityService.a(this)` → `startService`，并注册 `CHANGE_NOTIFICATION` 接收器；撤权路径 `b(Context)` 被 `qe/qf.onPreferenceClick` 调用，未发现监听设置页用 `GLOBAL_ACTION_BACK/HOME` 阻止撤权的代码。
- **身份层面存在轻度假冒**：包名 `com.helpdesk.slauncher`、类路径 `com.helpdesk.*`，但显示名与无障碍说明均自称 **S6 Launcher**，无障碍列表项（service 无独立 `android:label`，回落到 `@string/application_name`）显示 "S6 Launcher"，描述文案为 `To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting.`——借三星 Galaxy S6 桌面品牌取信，且该说明**未提及通知内容将被广播给桌面进程以外的用途**（实际仅进程内广播）。
- **覆盖边界**：本次按题面只做运行期引导链定向核验，未展开 `com.helpdesk.ad`（广告 SDK）、`update.*`（自更新）与 Xavier 家族典型静默安装/下载链；`restricted=['SESSION_INSTALLER']` 线索的落地代码未在本轮核实。引导链本身静态完整可见，无加壳/密文/远端 HTML 参与。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链（Manifest 服务声明、res/xml/notification_accessibility_service.xml、strings.xml 文案、LauncherSetting.c() 弹窗、qw/qx.onClick 系统设置跳转、onActivityResult 回读）全部静态可见，未加壳、无 AES 密文引导页、无远端 HTML 承载引导。assets 下 Privacy.html/help.html/licenses.html 为本地静态说明页，未参与无障碍引导。",
  "summary_one_liner": "以 S6 Launcher 桌面美化名义，在设置页通知相关开关被点击时弹出原生 AlertDialog 说明并一键跳系统无障碍设置，拒权后仅回读状态不重跳，获权后仅用无障碍服务广播回传通知图标与文本供桌面显示。",
  "disguise_identity": {
    "app_display_name": "S6 Launcher",
    "claimed_brand_or_persona": "S6 Launcher（借三星 Galaxy S6 桌面/Launcher 品牌身份）",
    "a11y_service_label": "S6 Launcher（service 未声明 android:label，回落到 @string/application_name；描述为 To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting.）",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.helpdesk.slauncher 与类路径 com.helpdesk.* 与宣称的三星 S6 品牌不一致；服务列表项复用应用名而非独立服务名，使系统无障碍列表直接呈现品牌名；未发现空白/换行挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool（targetSdk 19，无该字段）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.helpdesk.slauncher.LauncherSetting（PreferenceActivity，入口 VIEW com.helpdesk.slauncher://kk_setting）",
      "trigger_event": "用户进入设置页后点击“显示通知内容”相关 Preference 的 onPreferenceClick（调用 LauncherSetting.c(LauncherSetting)）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "（设置页自身文案未逐字核验）",
      "shown_text_zh": "桌面设置页中的通知显示开关项",
      "user_action_requested": "用户需主动点击该设置项开关，无强制，可退出设置页",
      "code_anchor": "com.helpdesk.slauncher.LauncherSetting.onResume / com.helpdesk.slauncher.pr.onPreferenceClick 等 → LauncherSetting.c(LauncherSetting)"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "原生 AlertDialog（标题 pref_desktop_show_notification_title，正文 pref_desktop_show_notification_content，按钮 yes/no）",
      "trigger_event": "点击通知相关设置开关后立即弹出（c(LauncherSetting) 内 AlertDialog$Builder 构建）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting. \nDo you want to open Accessibility Settings?",
      "shown_text_zh": "要启用通知功能，请在“无障碍设置”中开启 S6 Launcher 无障碍服务。是否要打开无障碍设置？",
      "user_action_requested": "点击“是/yes”跳转系统无障碍设置；点击“否/no”直接关闭（setNegativeButton 监听器为 null，可取消，非强制）",
      "code_anchor": "com.helpdesk.slauncher.LauncherSetting.c(LauncherSetting) + res/values/strings.xml: pref_desktop_show_notification_content"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户在弹窗点“是” → qw.onClick(DialogInterface,int)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍服务列表，其中条目名显示为 S6 Launcher，描述为“要启用通知，请在无障碍设置中开启 S6 Launcher 无障碍服务”",
      "user_action_requested": "用户在系统页面手动找到 S6 Launcher 条目并打开开关",
      "code_anchor": "com.helpdesk.slauncher.qw.onClick（startActivityForResult(\"android.settings.ACCESSIBILITY_SETTINGS\", 2001)）"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 LauncherSetting，onActivityResult(requestCode=2001) 回读服务真实启用状态",
      "trigger_event": "用户从系统无障碍设置返回（无论是否开启）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅把开关控件勾选状态同步为真实启用结果，不弹二次劝导",
      "user_action_requested": "无需操作；未开启时保持未勾选，无重跳、无定时拉起、无遮罩",
      "code_anchor": "com.helpdesk.slauncher.LauncherSetting.onActivityResult case 2001 + com.helpdesk.slauncher.util.u.a(Context,String)"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS（SDK>=18）或 ACCESSIBILITY_SETTINGS（SDK<18）",
      "trigger_event": "另一通知权限设置项点击 → qx.onClick",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统通知使用权/无障碍设置页，用于授予通知读取能力",
      "user_action_requested": "用户手动勾选授权；同样可取消返回",
      "code_anchor": "com.helpdesk.slauncher.qx.onClick"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "NotificationAccessibilityService（startService）+ Launcher 内 CHANGE_NOTIFICATION 广播接收器",
      "trigger_event": "Launcher.a(boolean) 中 this.cj 为真时调用 NotificationAccessibilityService.a(this)；服务 onServiceConnected 后开始接收通知事件",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无障碍服务把通知包名/图标/大图标/文本通过广播回传给桌面进程，用于状态栏通知图标与通知内容显示",
      "user_action_requested": "无；未见获权后自动点确认、自动授权或阻止撤权动作",
      "code_anchor": "com.helpdesk.slauncher.Launcher.a(boolean) + NotificationAccessibilityService.onAccessibilityEvent + NotificationAccessibilityService.a(Context)"
    }
  ],
  "text_presentation_locations": [
    "LauncherSetting 内原生不可持久 AlertDialog：标题 pref_desktop_show_notification_title + 正文 pref_desktop_show_notification_content（含“是否要打开无障碍设置”问句），按钮 yes/no",
    "系统无障碍列表条目描述：res/xml/notification_accessibility_service.xml 的 android:description → @string/accessibility_service_description（字符串硬编码 S6 Launcher 品牌）",
    "系统无障碍列表条目名称：service 未设 android:label，回落到 application 的 @string/application_name = S6 Launcher",
    "本地静态 HTML assets/Privacy.html、assets/help.html、assets/licenses.html：为隐私政策/帮助/开源许可说明，未承载无障碍引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting. \nDo you want to open Accessibility Settings?",
      "text_zh": "要启用通知功能，请在“无障碍设置”中开启 S6 Launcher 无障碍服务。是否要打开无障碍设置？",
      "source_location": "res/values/strings.xml key=pref_desktop_show_notification_content（LauncherSetting.c(LauncherSetting) 作为 AlertDialog message）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting.",
      "text_zh": "要启用通知功能，请在“无障碍设置”中开启 S6 Launcher 无障碍服务。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（res/xml/notification_accessibility_service.xml android:description）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无强制循环：onActivityResult(requestCode=2001) 仅回读 util.u.a() 真实启用状态并同步 CheckBox，返回设置页或退出均不再重跳；onResume 未包含无障碍跳转或定时器拉起逻辑",
    "overlay_or_fake_settings": "无。未使用 TYPE_ACCESSIBILITY_OVERLAY / SYSTEM_ALERT_WINDOW 叠放引导遮罩，未实现高仿系统无障碍开关页，跳转为真实系统设置 Activity",
    "restricted_settings_13plus_coaching": "无（targetSdk 19，无“允许受限设置”分步教学；未见 SESSION_INSTALLER 落地代码）",
    "post_grant_anti_removal": "无。未见获权后自动点击确认、自动授权或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权；仅存在用户主动触发的 stopService 撤权路径",
    "benign_graceful_degradation": "具降级机制：用户拒绝授权时弹窗可取消、返回后仅保持开关未勾选，桌面其余功能继续可用，通知显示能力单独缺失"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测 LauncherSetting 页面内弹出 AlertDialog 的瞬间（标题/正文含 'S6 Launcher Accessibility Service'），以及紧随其后的 startActivityForResult('android.settings.ACCESSIBILITY_SETTINGS') / startActivity('android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS') 调用；也可在跳转系统设置 800ms 后截取无障碍列表条目",
    "key_pages_to_capture": [
      {
        "page_role": "设置页通知开关触发的引导弹窗页",
        "page_identifier": "LauncherSetting Activity 上的 AlertDialog：标题含 notification，正文含 'S6 Launcher Accessibility Service'，按钮为 yes/no",
        "why_most_useful": "这是该应用唯一的无障碍劝导载体，可确认是否可取消、文案是否如实说明用途，是区分良性说明与诱导的关键页",
        "observable_utg_signals": ["弹窗正文文本 'To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting.'", "存在 no 取消按钮（可点关闭）", "弹窗下方仍为设置项列表，非全屏遮罩"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置无障碍列表中的 'S6 Launcher' 条目及其描述文本",
        "why_most_useful": "核验无障碍列表项名称是否借用 S6 品牌、描述是否与实际能力（仅通知事件、canRetrieveWindowContent=false）一致",
        "observable_utg_signals": ["条目名称 'S6 Launcher'", "描述 'To activate notification, please turn on S6 Launcher Accessibility Service on Accessibility Setting.'", "开关初始为关闭且无自动开启"]
      },
      {
        "page_role": "返回设置页后的状态回写页",
        "page_identifier": "LauncherSetting 中通知相关 CheckBoxPreference 的勾选状态",
        "why_most_useful": "验证拒权后是否发生重跳/循环压迫（本应用预期为无循环、状态如实回写）",
        "observable_utg_signals": ["返回后无新弹窗", "开关未勾选且无倒计时/二次劝导", "未出现悬浮遮罩层"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导链纯文本、纯原生控件，静态与 UTG 均可读。仅需注意无障碍服务在系统列表中呈现的是应用名 'S6 Launcher' 而非服务类名，按类名检索会漏；另本轮未覆盖 com.helpdesk.ad 广告 SDK 与 update.* 自更新链的后续诱导，若关注 Xavier 家族典型载荷需另开链核验。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION"
  ],
  "code_anchors": [
    "com.helpdesk.slauncher.LauncherSetting.c(com.helpdesk.slauncher.LauncherSetting)",
    "com.helpdesk.slauncher.qw.onClick(android.content.DialogInterface,int)",
    "com.helpdesk.slauncher.qx.onClick(android.content.DialogInterface,int)",
    "com.helpdesk.slauncher.LauncherSetting.onActivityResult(int,int,android.content.Intent)",
    "com.helpdesk.slauncher.Launcher.a(boolean)",
    "res/values/strings.xml (pref_desktop_show_notification_content / accessibility_service_description)"
  ]
}
```

</details>
