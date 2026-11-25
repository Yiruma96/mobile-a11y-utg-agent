# MR_028__97f855edff｜PUXIS — Raiffeisen SmsSecurity

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：125.0s

## 1. 一句话核心结论

- **核心申请方式**：该样本完全不向用户做任何无障碍开启引导，而是以无 label/无 description 的空壳无障碍服务静默预置、专监听 com.android.phone 的 AlertDialog/USSD 弹窗，配合伪造的不可取消系统级"System/Error"弹窗完成话术欺骗。
- **静态可见性说明**：无障碍服务声明、idle_service_config.xml、ServiceDialog 弹窗文案与 onAccessibilityEvent 判定逻辑均为明文 DEX/XML 可见；全包不存在 ACCESSIBILITY_SETTINGS 或 APPLICATION_DETAILS_SETTINGS 跳转点，故无需还原即确认不存在引导链。未发现加壳、AES 载荷或远端 HTML 引导页。
- **命中的行为模式标签**：`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `97f855edffd0394f772fe2558eed4e28b757760d16ac125a352d5459497249ac` |
| 包名 / 年份 | `org.thoughtcrime.securesms` / 2016 |
| 家族 / 品类 | **PUXIS**（同池样本数：4） |
| 原始来源标识 | https://blog.trendmicro.com/trendlabs-security-intelligence/operation-emmental-revisited-malicious-apps-lock-users-out/ |
| 桌面显示名 | Raiffeisen SmsSecurity |
| 引导页宣称品牌/身份 | Raiffeisen（奥地利莱夫艾森银行）+ SmsSecurity 安全短信外壳，底层复用 TextSecure/Signal 开源包名 org.thoughtcrime.securesms |
| 系统无障碍列表服务名 | 服务未声明 android:label 与 android:description，系统无障碍列表仅回落到应用名 Raiffeisen SmsSecurity，无任何功能说明文字 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务刻意留空 label 与 description 以避免暴露用途；弹窗以硬编码 "System" 为标题冒充系统；主入口使用 NoAnimation.Theme.BlackScreen 黑屏主题实现无痕路由；额外声明 xpack.ActUpdate / xpack.ActDefault / FirstActivity 三个自有 action 的隐藏入口 Activity；应用 debuggable=true 且 targetSdkVersion=19（低版本以规避新版权限管控） |
| 无障碍服务类名 | `org.thoughtcrime.securesms.xservices.IdleService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.android.phone |
| 共现高危权限 | `READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | org.thoughtcrime.securesms.RoutingActivity（LAUNCHER，theme=@style/NoAnimation.Theme.BlackScreen，launchMode=singleTask） | 用户点击桌面图标，MAIN/LAUNCHER intent 触发 onCreate 路由分发 | 原生Activity | 无 | 无（无需用户操作，自动跳转） | `AndroidManifest.xml: org.thoughtcrime.securesms.RoutingActivity / @style/NoAnimation.Theme.BlackScreen` |
| 2 | 引导说明页 | org.thoughtcrime.securesms.FirstActivity（action=org.thoughtcrime.securesms.firstact，layout id 2130903065） | onCreate 中 setContentView 后由 doNext(View) 读取 getIntent().getParcelableExtra("next_intent") 直接 startActivity 并 finish | 原生Activity | 无 | 无显式操作；页面被设计为一次性无痕透传 | `org.thoughtcrime.securesms.FirstActivity#onCreate / #doNext` |
| 3 | 跳无障碍设置 | 不存在：全包无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 调用；仅 ApplicationPreferencesActivity#b 使用 android.settings.WIRELESS_SETTINGS | 无触发点（静态确认缺失） | 不可静态还原 | 无 | 无 | `search_function_callsites(ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS)=no_matches；ApplicationPreferencesActivity#b` |
| 4 | 遮罩叠层指引 | org.thoughtcrime.securesms.xservices.ServiceDialog（android:label=@string/title_activity_service_dialog，window type 2003） | onCreate 中 AlertDialog.Builder.setCancelable(false).create()，再 getWindow().setType(2003) 与 setFlags(1024,1024) 后 show() | 悬浮窗Overlay | **原文**：System / Error / OK<br>**译注**：以"系统"为标题的"错误"提示框，只有一个 OK 按钮；不可取消、返回键与 Home 键被吞掉，只能点 OK | 仅允许点击 OK；setCancelable(false) 且 onKeyDown 对 KEYCODE_BACK(4)、KEYCODE_HOME(3) 返回 true，无取消/跳过路径 | `org.thoughtcrime.securesms.xservices.ServiceDialog#onCreate / #onKeyDown；res/values/strings.xml: service_dialog_error="Error"` |
| 5 | 获权后动作 | org.thoughtcrime.securesms.xservices.IdleService（AccessibilityService，packageNames=com.android.phone） | onAccessibilityEvent 收到 TYPE_WINDOW_STATE_CHANGED(32)，比对 getClassName() 是否属于 android.app.AlertDialog / com.mediatek.phone.UssdAlertActivity / com.htc.widget.HtcAlertDialog | 不可静态还原 | **原文**：无（服务本身无 UI，仅后台读取窗口状态与内容）<br>**译注**：后台静默监听电话应用弹出的运营商/USSD/系统提示框，具备 canRetrieveWindowContent 读取窗口内容能力 | 无 | `org.thoughtcrime.securesms.xservices.IdleService#onAccessibilityEvent；res/xml/idle_service_config.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无任何无障碍引导文案：res/values*/strings.xml 中不含 accessibility 相关字符串，idle_service_config.xml 无 android:description，Manifest service 标签无 android:label
- org.thoughtcrime.securesms.xservices.ServiceDialog：系统级悬浮窗（type=2003）中不可取消 AlertDialog，标题硬编码 "System"、正文 res/values/strings.xml#service_dialog_error("Error")、按钮 "OK"
- AndroidManifest.xml 中自定义签名权限标签 "Access to SmsSecure Secrets"（org.thoughtcrime.securesms.ACCESS_SECRETS，protectionLevel=signature），仅在安装/权限信息页可见
- Activity 标题栏：title_activity_service_dialog="ServiceDialog"、title_activity_black、@string/app_name（Raiffeisen SmsSecurity）
- FirstActivity / RoutingActivity / BlackActivity：空壳或黑屏，无任何展示文字，不承载引导内容

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | System | 系统 | `org.thoughtcrime.securesms.xservices.ServiceDialog#onCreate 硬编码 alertDialog$Builder.setTitle("System")` | 假更新 |
| en | Error | 错误 | `res/values/strings.xml key=service_dialog_error（id 0x7f0d0233，被 ServiceDialog.onCreate setMessage(2131558963) 引用）` | 故障恐吓 |
| en | OK | 确定 | `org.thoughtcrime.securesms.xservices.ServiceDialog#onCreate 硬编码 setPositiveButton("OK")` | 未知 |
| en | Access to SmsSecure Secrets | 访问 SmsSecure 机密数据 | `AndroidManifest.xml <permission android:name="org.thoughtcrime.securesms.ACCESS_SECRETS" android:label="Access to SmsSecure Secrets">` | 隐私承诺 |
| en | ServiceDialog | 服务对话框 | `res/values/strings.xml key=title_activity_service_dialog（Manifest 中 ServiceDialog 的 android:label）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不存在引导-拒绝-重跳循环：应用从不跳转系统无障碍设置页，因此无 onResume 重跳、无定时器拉起；用户拒绝的唯一交互对象是 ServiceDialog 的 OK 按钮，该弹窗 setCancelable(false) 且 onKeyDown 吞掉 BACK/HOME，只能正向确认
- **遮罩叠层 / 高仿系统设置页**：存在系统级悬浮窗欺骗但非无障碍引导遮罩：ServiceDialog 以 Window type=2003（TYPE_SYSTEM_ALERT）+ setFlags(1024,1024) 全屏显示，伪装成系统错误提示；未发现高仿系统无障碍开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无（未发现监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；onKeyDown 屏蔽 BACK/HOME 仅作用于 ServiceDialog 弹窗本身）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以窗口类型而非 Activity 跳转作为触发点：监测到 WindowManager.LayoutParams.type=2003（TYPE_SYSTEM_ALERT）且标题文本为 "System" 的弹窗，或前台切换到 org.thoughtcrime.securesms.xservices.ServiceDialog / RoutingActivity 时立即抓取；本样本不存在 ACCESSIBILITY_SETTINGS 跳转可作为 hook，不能沿用常规"跳设置页即抓"策略
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：该样本完全没有无障碍引导链，若 UTG 检测器以"跳转 ACCESSIBILITY_SETTINGS 后抓页"为唯一触发条件将全程漏检，必须改用系统级悬浮窗(type=2003)/伪造系统标题作为触发信号；另外无障碍服务本身零文案，纯 UTG 文本提取在服务列表页拿不到任何判别语义，需结合弹窗与电话/USSD 场景联动观测。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统级伪造错误弹窗页** | Window type=2003、标题 "System"、正文 "Error"、仅一个 OK 按钮、BACK/HOME 无效 | 这是该样本唯一的用户可见话术载体，直接证明其以系统身份冒充并强制单向确认，是区分欺骗行为与良性安全提示的关键页 | 弹窗标题/正文文本 System\|Error；按钮集合仅 OK 且无取消；弹窗覆盖在电话/短信界面之上而非应用自身 Activity 内；按返回键无效、界面不退出 |
| **系统无障碍服务列表项** | 设置→无障碍→已安装服务中的 Raiffeisen SmsSecurity 条目，无描述文字 | 核实服务是否无 label/无 description 且已被勾选，直接验证"静默预置、无说明"的无障碍滥用形态 | 条目仅显示应用名、无功能说明；开关状态为已开启；点击条目无任何说明页内容 |
| **冷启动路由页与后续落地页** | RoutingActivity（黑屏、无动画、无文字）→ FirstActivity（空壳透传）→ 实际落地 Activity | 确认冷启动 0 步内是否直接弹出话术界面，以及是否存在可取消/可跳过的说明页 | 启动后极短时间出现无文字黑屏帧；无任何按钮或跳过控件；落地页与桌面图标名称不一致 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `org.thoughtcrime.securesms.xservices.IdleService#onAccessibilityEvent`
- `org.thoughtcrime.securesms.xservices.ServiceDialog#onCreate`
- `org.thoughtcrime.securesms.xservices.ServiceDialog#onKeyDown`
- `org.thoughtcrime.securesms.FirstActivity#doNext`
- `res/xml/idle_service_config.xml`
- `AndroidManifest.xml: service org.thoughtcrime.securesms.xservices.IdleService (BIND_ACCESSIBILITY_SERVICE)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（定向核验结果）

**核心事实：本样本不存在"引导用户开启无障碍"的页面流转链。** 全包内 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 的调用点数为 **0**（`search_function_callsites` 与 `search_text_in_app` 双向核验），唯一的 `android.settings.*` 跳转是 `ApplicationPreferencesActivity#b` 中的 `android.settings.WIRELESS_SETTINGS`，与无障碍无关。因此不存在引导弹窗、分步教学页、WebView 教程、遮罩叠层或拒绝后重跳循环。

- **无障碍服务是"静默声明型"**：[IdleService](<resource-unit:#1.dex1 code:org.thoughtcrime.securesms.xservices.IdleService#onAccessibilityEvent>) 在 Manifest 中带 `BIND_ACCESSIBILITY_SERVICE` 权限与 `android.accessibilityservice.AccessibilityService` intent-filter 声明，配置文件 [res/xml/idle_service_config.xml](<resource-unit:#1 file:res/xml/idle_service_config.xml>) 中 `canRetrieveWindowContent="true"`、`packageNames="com.android.phone"`、事件类型仅 `typeWindowStateChanged`、`notificationTimeout="10"`；**既无 `android:label` 也无 `android:description`**，系统无障碍列表里没有任何功能说明，用户无从判断用途。
- **服务实际行为是"电话/运营商弹窗嗅探"**：`onAccessibilityEvent` 只对 `com.android.phone` 的窗口状态变化作出反应，且显式比对 `android.app.AlertDialog`、`com.mediatek.phone.UssdAlertActivity`、`com.htc.widget.HtcAlertDialog` 三类类名——这是典型的 USSD/运营商余额弹窗旁路识别逻辑，而非为用户提供辅助功能。
- **用户真正看到的界面是伪造"系统错误"弹窗**：[ServiceDialog.onCreate()](<resource-unit:#1.dex1 code:org.thoughtcrime.securesms.xservices.ServiceDialog#onCreate>) 构建不可取消的 `AlertDialog`，标题硬编码 `"System"`、正文取 `service_dialog_error`（值 `"Error"`）、按钮 `"OK"`，`getWindow().setType(2003)` 以系统级悬浮窗类型显示并置全屏 flag；`onKeyDown` 对 `KEYCODE_BACK(4)` 与 `KEYCODE_HOME(3)` 直接返回 `true` 吞掉。
- **入口侧**：[RoutingActivity](<resource-unit:#1 manifest:components>)（LAUNCHER，`NoAnimation.Theme.BlackScreen`）与 [FirstActivity.doNext()](<resource-unit:#1.dex1 code:org.thoughtcrime.securesms.FirstActivity#doNext>)（`org.thoughtcrime.securesms.firstact`，用 `next_intent` 透传跳转后 `finish`）构成无痕路由，均不承载任何说明文字。
- **身份错配**：应用名 `Raiffeisen SmsSecurity`（银行仿冒）叠加在 `org.thoughtcrime.securesms`（TextSecure/Signal 开源代码库）之上，并夹带 `xservices`/`xpack`/`xbroadcast` 私有包（`XSmsIncom`、`XRepeatSms`、`XUpdate`、`ActUpdate`），属二次打包变种。

**静态可见性**：无障碍相关逻辑、弹窗文案、配置文件全部明文可读，无加壳/加密载荷阻挡本议题的静态还原。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍服务声明、idle_service_config.xml、ServiceDialog 弹窗文案与 onAccessibilityEvent 判定逻辑均为明文 DEX/XML 可见；全包不存在 ACCESSIBILITY_SETTINGS 或 APPLICATION_DETAILS_SETTINGS 跳转点，故无需还原即确认不存在引导链。未发现加壳、AES 载荷或远端 HTML 引导页。",
  "summary_one_liner": "该样本完全不向用户做任何无障碍开启引导，而是以无 label/无 description 的空壳无障碍服务静默预置、专监听 com.android.phone 的 AlertDialog/USSD 弹窗，配合伪造的不可取消系统级\"System/Error\"弹窗完成话术欺骗。",
  "disguise_identity": {
    "app_display_name": "Raiffeisen SmsSecurity",
    "claimed_brand_or_persona": "Raiffeisen（奥地利莱夫艾森银行）+ SmsSecurity 安全短信外壳，底层复用 TextSecure/Signal 开源包名 org.thoughtcrime.securesms",
    "a11y_service_label": "服务未声明 android:label 与 android:description，系统无障碍列表仅回落到应用名 Raiffeisen SmsSecurity，无任何功能说明文字",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务刻意留空 label 与 description 以避免暴露用途；弹窗以硬编码 \"System\" 为标题冒充系统；主入口使用 NoAnimation.Theme.BlackScreen 黑屏主题实现无痕路由；额外声明 xpack.ActUpdate / xpack.ActDefault / FirstActivity 三个自有 action 的隐藏入口 Activity；应用 debuggable=true 且 targetSdkVersion=19（低版本以规避新版权限管控）"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "org.thoughtcrime.securesms.RoutingActivity（LAUNCHER，theme=@style/NoAnimation.Theme.BlackScreen，launchMode=singleTask）",
      "trigger_event": "用户点击桌面图标，MAIN/LAUNCHER intent 触发 onCreate 路由分发",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "黑屏主题路由页，不呈现任何文字，直接转向后续界面",
      "user_action_requested": "无（无需用户操作，自动跳转）",
      "code_anchor": "AndroidManifest.xml: org.thoughtcrime.securesms.RoutingActivity / @style/NoAnimation.Theme.BlackScreen"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "org.thoughtcrime.securesms.FirstActivity（action=org.thoughtcrime.securesms.firstact，layout id 2130903065）",
      "trigger_event": "onCreate 中 setContentView 后由 doNext(View) 读取 getIntent().getParcelableExtra(\"next_intent\") 直接 startActivity 并 finish",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "空壳中转页，仅透传 next_intent，无说明文案、无按钮（无跳过也无取消）",
      "user_action_requested": "无显式操作；页面被设计为一次性无痕透传",
      "code_anchor": "org.thoughtcrime.securesms.FirstActivity#onCreate / #doNext"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "不存在：全包无 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 调用；仅 ApplicationPreferencesActivity#b 使用 android.settings.WIRELESS_SETTINGS",
      "trigger_event": "无触发点（静态确认缺失）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "应用从不把用户引向系统无障碍设置页；IdleService 依靠 Manifest 预声明静默存在，等待被外部/其他途径启用",
      "user_action_requested": "无",
      "code_anchor": "search_function_callsites(ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS)=no_matches；ApplicationPreferencesActivity#b"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "org.thoughtcrime.securesms.xservices.ServiceDialog（android:label=@string/title_activity_service_dialog，window type 2003）",
      "trigger_event": "onCreate 中 AlertDialog.Builder.setCancelable(false).create()，再 getWindow().setType(2003) 与 setFlags(1024,1024) 后 show()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "System / Error / OK",
      "shown_text_zh": "以\"系统\"为标题的\"错误\"提示框，只有一个 OK 按钮；不可取消、返回键与 Home 键被吞掉，只能点 OK",
      "user_action_requested": "仅允许点击 OK；setCancelable(false) 且 onKeyDown 对 KEYCODE_BACK(4)、KEYCODE_HOME(3) 返回 true，无取消/跳过路径",
      "code_anchor": "org.thoughtcrime.securesms.xservices.ServiceDialog#onCreate / #onKeyDown；res/values/strings.xml: service_dialog_error=\"Error\""
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "org.thoughtcrime.securesms.xservices.IdleService（AccessibilityService，packageNames=com.android.phone）",
      "trigger_event": "onAccessibilityEvent 收到 TYPE_WINDOW_STATE_CHANGED(32)，比对 getClassName() 是否属于 android.app.AlertDialog / com.mediatek.phone.UssdAlertActivity / com.htc.widget.HtcAlertDialog",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（服务本身无 UI，仅后台读取窗口状态与内容）",
      "shown_text_zh": "后台静默监听电话应用弹出的运营商/USSD/系统提示框，具备 canRetrieveWindowContent 读取窗口内容能力",
      "user_action_requested": "无",
      "code_anchor": "org.thoughtcrime.securesms.xservices.IdleService#onAccessibilityEvent；res/xml/idle_service_config.xml"
    }
  ],
  "text_presentation_locations": [
    "无任何无障碍引导文案：res/values*/strings.xml 中不含 accessibility 相关字符串，idle_service_config.xml 无 android:description，Manifest service 标签无 android:label",
    "org.thoughtcrime.securesms.xservices.ServiceDialog：系统级悬浮窗（type=2003）中不可取消 AlertDialog，标题硬编码 \"System\"、正文 res/values/strings.xml#service_dialog_error(\"Error\")、按钮 \"OK\"",
    "AndroidManifest.xml 中自定义签名权限标签 \"Access to SmsSecure Secrets\"（org.thoughtcrime.securesms.ACCESS_SECRETS，protectionLevel=signature），仅在安装/权限信息页可见",
    "Activity 标题栏：title_activity_service_dialog=\"ServiceDialog\"、title_activity_black、@string/app_name（Raiffeisen SmsSecurity）",
    "FirstActivity / RoutingActivity / BlackActivity：空壳或黑屏，无任何展示文字，不承载引导内容"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "System",
      "text_zh": "系统",
      "source_location": "org.thoughtcrime.securesms.xservices.ServiceDialog#onCreate 硬编码 alertDialog$Builder.setTitle(\"System\")",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Error",
      "text_zh": "错误",
      "source_location": "res/values/strings.xml key=service_dialog_error（id 0x7f0d0233，被 ServiceDialog.onCreate setMessage(2131558963) 引用）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "OK",
      "text_zh": "确定",
      "source_location": "org.thoughtcrime.securesms.xservices.ServiceDialog#onCreate 硬编码 setPositiveButton(\"OK\")",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Access to SmsSecure Secrets",
      "text_zh": "访问 SmsSecure 机密数据",
      "source_location": "AndroidManifest.xml <permission android:name=\"org.thoughtcrime.securesms.ACCESS_SECRETS\" android:label=\"Access to SmsSecure Secrets\">",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "ServiceDialog",
      "text_zh": "服务对话框",
      "source_location": "res/values/strings.xml key=title_activity_service_dialog（Manifest 中 ServiceDialog 的 android:label）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不存在引导-拒绝-重跳循环：应用从不跳转系统无障碍设置页，因此无 onResume 重跳、无定时器拉起；用户拒绝的唯一交互对象是 ServiceDialog 的 OK 按钮，该弹窗 setCancelable(false) 且 onKeyDown 吞掉 BACK/HOME，只能正向确认",
    "overlay_or_fake_settings": "存在系统级悬浮窗欺骗但非无障碍引导遮罩：ServiceDialog 以 Window type=2003（TYPE_SYSTEM_ALERT）+ setFlags(1024,1024) 全屏显示，伪装成系统错误提示；未发现高仿系统无障碍开关页",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无（未发现监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；onKeyDown 屏蔽 BACK/HOME 仅作用于 ServiceDialog 弹窗本身）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以窗口类型而非 Activity 跳转作为触发点：监测到 WindowManager.LayoutParams.type=2003（TYPE_SYSTEM_ALERT）且标题文本为 \"System\" 的弹窗，或前台切换到 org.thoughtcrime.securesms.xservices.ServiceDialog / RoutingActivity 时立即抓取；本样本不存在 ACCESSIBILITY_SETTINGS 跳转可作为 hook，不能沿用常规\"跳设置页即抓\"策略",
    "key_pages_to_capture": [
      {
        "page_role": "系统级伪造错误弹窗页",
        "page_identifier": "Window type=2003、标题 \"System\"、正文 \"Error\"、仅一个 OK 按钮、BACK/HOME 无效",
        "why_most_useful": "这是该样本唯一的用户可见话术载体，直接证明其以系统身份冒充并强制单向确认，是区分欺骗行为与良性安全提示的关键页",
        "observable_utg_signals": ["弹窗标题/正文文本 System|Error", "按钮集合仅 OK 且无取消", "弹窗覆盖在电话/短信界面之上而非应用自身 Activity 内", "按返回键无效、界面不退出"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已安装服务中的 Raiffeisen SmsSecurity 条目，无描述文字",
        "why_most_useful": "核实服务是否无 label/无 description 且已被勾选，直接验证\"静默预置、无说明\"的无障碍滥用形态",
        "observable_utg_signals": ["条目仅显示应用名、无功能说明", "开关状态为已开启", "点击条目无任何说明页内容"]
      },
      {
        "page_role": "冷启动路由页与后续落地页",
        "page_identifier": "RoutingActivity（黑屏、无动画、无文字）→ FirstActivity（空壳透传）→ 实际落地 Activity",
        "why_most_useful": "确认冷启动 0 步内是否直接弹出话术界面，以及是否存在可取消/可跳过的说明页",
        "observable_utg_signals": ["启动后极短时间出现无文字黑屏帧", "无任何按钮或跳过控件", "落地页与桌面图标名称不一致"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：该样本完全没有无障碍引导链，若 UTG 检测器以\"跳转 ACCESSIBILITY_SETTINGS 后抓页\"为唯一触发条件将全程漏检，必须改用系统级悬浮窗(type=2003)/伪造系统标题作为触发信号；另外无障碍服务本身零文案，纯 UTG 文本提取在服务列表页拿不到任何判别语义，需结合弹窗与电话/USSD 场景联动观测。"
  },
  "behavior_pattern_tags": [
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE"
  ],
  "code_anchors": [
    "org.thoughtcrime.securesms.xservices.IdleService#onAccessibilityEvent",
    "org.thoughtcrime.securesms.xservices.ServiceDialog#onCreate",
    "org.thoughtcrime.securesms.xservices.ServiceDialog#onKeyDown",
    "org.thoughtcrime.securesms.FirstActivity#doNext",
    "res/xml/idle_service_config.xml",
    "AndroidManifest.xml: service org.thoughtcrime.securesms.xservices.IdleService (BIND_ACCESSIBILITY_SERVICE)"
  ]
}
```

</details>
