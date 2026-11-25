# MR_052__1596644cdc｜RuMMS — СМC - Сooбщeниe

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：93.8s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即以假故障 Toast 加静默跳转 android.settings.ACCESSIBILITY_SETTINGS，并以约10秒节流的轮询死循环反复重跳，直到用户开启名为『主进程』的无障碍服务，全程无说明页、无取消按钮。
- **静态可见性说明**：无障碍引导链全部为明文 DEX 逻辑（CoalitionLick/Assignment/DieExpenditure/FindStunning/e/RecoverHerd），无加壳、无 AES 载荷、无 WebView/远端 HTML；远端 hellowopung.com/e8tmlzl7zeb7jynh5ii8/index.php 仅承载获权后的短信指令，不影响引导流程的静态可见性。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1596644cdc7494082d2afb371824f10afc880d00117a3451a4c3231ec230b56c` |
| 包名 / 年份 | `org.day.cold` / 2018 |
| 家族 / 品类 | **RuMMS**（同池样本数：516） |
| 原始来源标识 | https://www.zscaler.com/blogs/security-research/rumms-malware-back-enhancements |
| 桌面显示名 | СМC - Сooбщeниe |
| 引导页宣称品牌/身份 | 冒充系统级『主进程』（Оcновной прoцесc）与短信应用（СМC - Сooбщeниe，即 SMS - Message） |
| 系统无障碍列表服务名 | Оcновной прoцесc |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：同形字混淆：应用名与服务名中用拉丁字母 c/o 混入西里尔字母（『Сиcтeма』『Оcновной прoцесc』『прoцесc』）；无障碍配置 ercouhzjsf.xml 刻意不声明 android:description，系统列表无任何用途说明；以『статистике（统计）』指代无障碍权限，弱化敏感度；首次运行后 setComponentEnabledSetting 禁用启动器组件 CoalitionLick，桌面图标消失，仅能经前台通知『RecoverHerd/Recruit』通道再次拉起，规避用户卸载与二次核查。 |
| 无障碍服务类名 | `org.day.cold.RecoverHerd` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | org.day.cold.CoalitionLick（LAUNCHER Activity） | 用户点击桌面图标，onCreate | 原生Activity | 无 | 无（用户仅感知为『点了没反应』或一闪而过） | `org.day.cold.CoalitionLick#onCreate` |
| 2 | 冷启动入口 | org.day.cold.Assignment（Application）+ org.day.cold.FindStunning（前台 Service）+ 通知栏 | Application.onCreate：startForegroundService → FindStunning.onStartCommand → a() | 通知栏 | **原文**：Оcновной прoцесc / Сиcтeма нe корректнo рaботaeт, вaм нeобхoдимо включить дoступ к cтaтистике для 'Оcновной прoцесc'<br>**译注**：通知标题：主进程；正文：系统运行不正常，您需要为『主进程』开启统计访问权限 | 无明确要求，仅作为常驻伪装通知维持进程存活；同时 b() 调用 setComponentEnabledSetting(CoalitionLick, 2) 禁用桌面图标 | `org.day.cold.FindStunning#a / org.day.cold.FindStunning#b` |
| 3 | 引导说明页 | org.day.cold.DieExpenditure（无布局的透明 Activity，主题 Theme.Translucent.NoTitleBar.Fullscreen）+ Toast | e.a(context, now) → e.c(context, now)：距上次跳转超过 9952ms 时 startActivity(DieExpenditure) | 原生Activity | **原文**：Сиcтeма нe корректнo рaботaeт, вaм нeобхoдимо включить дoступ к cтaтистике для 'Оcновной прoцесc'<br>**译注**：系统运行不正常，您需要为『主进程』开启统计访问权限 | 无按钮、无取消/跳过选项，Toast 展示后立即跳转设置页并 finish()，用户只能被动跟随跳转 | `org.day.cold.DieExpenditure#onCreate（Toast + getString(2131034112)）` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍 → 已下载的服务列表） | DieExpenditure.onCreate 内 new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(0x10000000).startActivity() | 系统无障碍页 | **原文**：Оcновной прoцесc（系统列表中的服务项标签，无 description 说明）<br>**译注**：系统无障碍服务列表中出现一项名为『主进程』的服务，无任何用途描述 | 要求用户手动点开『Оcновной прoцесc』并开启开关（无应用内说明辅助，仅靠伪造的“系统故障”语境施压） | `org.day.cold.DieExpenditure#onCreate（Intent android.settings.ACCESSIBILITY_SETTINGS）` |
| 5 | 拒权反馈循环 | Assignment 静态 Handler 轮询线程 Assignment$1 + DieExpenditure 反复重启 | Assignment$1.run 每 1012ms 执行 e.b(ctx, now)：f(ctx) 读取 Settings.Secure.enabled_accessibility_services 不含 org.day.cold 时返回 false，随即 e.c 每 9952ms 再 startActivity(DieExpenditure) | 原生Activity | **原文**：Сиcтeма нe корректнo рaботaeт, вaм нeобхoдимо включить дoступ к cтaтистике для 'Оcновной прoцесc'<br>**译注**：系统运行不正常，您需要为『主进程』开启统计访问权限（每次重跳前重复弹出） | 用户按返回键退出设置页后约 10 秒内被再次强制拉回无障碍设置页，无退出或降级路径 | `org.day.cold.Assignment$1#run / org.day.cold.e#b / org.day.cold.e#c / org.day.cold.e#f` |
| 6 | 获权后动作 | 系统『更改默认短信应用』确认对话框 + RecoverHerd（无障碍服务）自动点击 | f(ctx) 为 true 后：stopService(FindStunning)；a() 内若 org.day.cold 非默认短信包则 startActivity(ACTION_CHANGE_DEFAULT, package=org.day.cold) 并 RecoverHerd.a(true) | 系统无障碍页 | **原文**：无（自动点击 android:id/button1 / android:id/right_button 完成确认）<br>**译注**：无障碍服务自动点击系统对话框的确认按钮，把本应用设为默认短信应用；并对远端配置的包名执行 GLOBAL_ACTION_BACK(2) 关闭其界面 | 无需用户操作；用户若尝试回到设置页撤权，服务会以 performGlobalAction(2) 返回键干扰 | `org.day.cold.Assignment$1#a / org.day.cold.RecoverHerd#onAccessibilityEvent / org.day.cold.RecoverHerd#a` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Toast（org.day.cold.DieExpenditure.onCreate，getString(2131034112)）——唯一“说明文字”，悬浮于系统无障碍设置页之上，无按钮、无取消
- 常驻前台通知（org.day.cold.FindStunning.a，频道 org.day.cold.GUARANTEE / 标题 getString(2131034113)『Оcновной прoцесc』，正文 getString(2131034112) 假故障文案），作为伪装进程与二次拉起入口
- 系统无障碍服务列表项标签：AndroidManifest 中 service android:label="Оcновной прoцесc"（引用 strings.xml accessibility_title）
- res/values/strings.xml：accessibility_desc（假故障长文案）、accessibility_title（主进程）、button_1=android:id/button1、button_right=android:id/right_button（自动点击目标 id）
- res/xml/ercouhzjsf.xml：无障碍能力声明（canRetrieveWindowContent=true、flagReportViewIds、监听 window 内容/状态变化），刻意不含 android:description，故系统列表无任何说明文字
- 无 assets/ 本地 HTML、无 WebView、无悬浮窗 Overlay、无高仿系统开关页、无应用内自定义引导 Dialog

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Сиcтeма нe корректнo рaботaeт, вaм нeобхoдимо включить дoступ к cтaтистике для 'Оcновной прoцесc' | 系统运行不正常，您需要为『主进程』开启统计访问权限 | `res/values/strings.xml key=accessibility_desc（代码引用 getString(2131034112)，用于 DieExpenditure Toast 与前台通知正文）` | 假更新 |
| ru | Оcновной прoцесc | 主进程 | `res/values/strings.xml key=accessibility_title；AndroidManifest 中 accessibility service 的 android:label；前台通知标题 getString(2131034113)` | 故障恐吓 |
| ru | СМC - Сooбщeниe | SMS - 消息 | `AndroidManifest application android:label（桌面显示名，拉丁 C/o 混入西里尔字母）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：Assignment$1.run 以 1012ms 周期轮询 Settings.Secure.enabled_accessibility_services 是否包含 org.day.cold；未开启时 e.c 以 9952ms 节流重新 startActivity(DieExpenditure)，即用户从设置页返回后约 10 秒内被再次弹假故障 Toast 并强制拉回无障碍设置页，形成不可退出的死循环；同时前台服务通知常驻、桌面图标已被禁用，用户无正常退出入口。
- **遮罩叠层 / 高仿系统设置页**：无半透明遮罩、无全屏悬浮窗、无高仿系统开关页；仅在系统无障碍设置页之上叠加一条 Toast 假故障提示（主题为 Theme.Translucent.NoTitleBar.Fullscreen 的空 Activity 负责弹出并立即 finish）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，样本 2018 年，不涉及 Android 13+ 受限设置引导）
- **获权后即时行为与防撤权机制**：获权后 RecoverHerd.a(true) 置标志位，onAccessibilityEvent 通过 findAccessibilityNodeInfosByViewId(android:id/button1、android:id/right_button) 自动 performAction(16) 点击系统确认框（用于自动将 org.day.cold 设为默认短信应用）；并对 SharedPreferences『Magnitude』中远端下发的包名执行 performGlobalAction(2)=GLOBAL_ACTION_BACK 关闭界面，干扰撤权与第三方安全界面。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（或当前前台包名由 org.day.cold 切换为 com.android.settings 无障碍页）的瞬间立即抓取；该动作在冷启动后 1 秒内首次触发，并在用户每次返回后约 10 秒重复触发，是稳定的 UTG 采样窗口。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无图空文本、无远端 HTML 外壳；但存在两处观测盲区：(1) 首次运行后桌面图标被 setComponentEnabledSetting 禁用，UTG 若按包名/图标枚举应用可能漏采，需以通知栏『Оcновной прoцесc』为入口或直接冷启动组件；(2) 获权后远端 hellowopung.com 下发短信指令与控制包名（SharedPreferences『Magnitude』），该部分为动态远端内容，静态不可见。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前 Toast 与瞬时透明 Activity** | 包名 org.day.cold 前台 + 无布局透明 Activity（DieExpenditure）+ Toast 文本『Сиcтeма нe корректнo рaботaeт…』 | 此处是唯一的“说明”载体，证明应用未提供任何可取消的引导页，直接以伪造系统故障话术推动用户跳设置 | Toast 节点文本含『Сиcтeма』『стaтистике』『Оcновной прoцесc』；页面无任何可点击按钮/取消控件；Activity 生命周期极短（onCreate 即 finish） |
| **系统无障碍服务列表项（Оcновной прoцесc）** | com.android.settings 无障碍页，列表项文本『Оcновной прoцесc』，无描述副标题 | 证明服务标签冒充系统“主进程”、且 android:description 缺失导致用户无从判断用途，是身份伪装的关键判据 | 列表项 label=Оcновной прoцесc 且 summary/description 为空；开关初始为关闭状态；同一页面短时间内被重复压栈/重复拉起 |
| **拒权后重跳循环页** | 返回键退出设置后约 10 秒，前台再次切回 org.day.cold（DieExpenditure）并跳转无障碍设置 | 直接观测『拒绝即重跳』的强制循环，是区分恶意诱导与良性引导的决定性动态证据 | ACCESSIBILITY_SETTINGS 跳转次数在 60 秒内≥3 次；两次跳转间隔约 10 秒；前台包名在 org.day.cold 与 com.android.settings 之间反复切换 |
| **获权后自动确认系统对话框** | 系统『更改默认短信应用』对话框，按钮被无障碍自动点击 | 验证获权后立即用于自授权与后续短信劫持，体现权限的真实用途 | 无障碍点击事件来源为 org.day.cold 服务；默认短信应用被改为 org.day.cold；对话框无用户实际操作即消失 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `org.day.cold.DieExpenditure#onCreate`
- `org.day.cold.Assignment$1#run`
- `org.day.cold.e#c`
- `org.day.cold.e#f`
- `org.day.cold.FindStunning#a`
- `res/values/strings.xml / res/xml/ercouhzjsf.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

分析已完成（已用满工具预算，因此停止继续探索，直接给出结论）。

**核心发现：该样本全程无任何“说明页/弹窗”，只用 Toast 和每 10 秒重新跳转设置页来强制用户开启无障碍。**

- 启动器 [CoalitionLick.onCreate()](<resource-unit:#1.dex1 code:org.day.cold.CoalitionLick#onCreate>) 只执行 `finish()`，因此点开图标后会立即消失，没有可见界面。
- [Assignment.onCreate()](<resource-unit:#1.dex1 code:org.day.cold.Assignment#onCreate>) 先启动前台服务 [FindStunning](<resource-unit:#1.dex1 code:org.day.cold.FindStunning#a>)，弹出标题为「Оcновной прoцесc」、正文为「系统运行不正常…需为'主进程'开启统计访问权限」的通知，再用 `setComponentEnabledSetting(..., 2)` 禁用启动器组件（桌面图标随之消失）。
- 唯一无障碍引导载体是 [DieExpenditure.onCreate()](<resource-unit:#1.dex1 code:org.day.cold.DieExpenditure#onCreate>)：先弹 Toast（假故障恐吓），再立刻 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 并 `finish()`。无确认弹窗、无取消或跳过、无 WebView、无悬浮遮罩。
- 拒绝循环：[Assignment$1.run()](<resource-unit:#1.dex1 code:org.day.cold.Assignment$1#run>) 每 1012ms 轮询，[e.b()/e.f()](<resource-unit:#1.dex1 code:org.day.cold.e#f>) 读取 `Settings.Secure.enabled_accessibility_services` 判断是否含 `org.day.cold`；未开启时由 [e.c()](<resource-unit:#1.dex1 code:org.day.cold.e#c>) 以 9952ms 节流反复重跳无障碍设置页，形成无法退出的死循环。
- 获权后反制：`stopService` 停前台服务 → 若未成默认短信应用则跳 `ACTION_CHANGE_DEFAULT`（package=org.day.cold），并置 `RecoverHerd.a(true)`；[RecoverHerd.onAccessibilityEvent()](<resource-unit:#1.dex1 code:org.day.cold.RecoverHerd#onAccessibilityEvent>) 通过 `findAccessibilityNodeInfosByViewId` 命中 `android:id/button1`/`right_button` 自动 `performAction(16)` 点掉系统确认框，并对远端配置包名执行 `performGlobalAction(2)`（返回）阻止撤权。
- 伪装：应用名「СМC - Сooбщeниe」、服务名「Оcновной прoцесc」均用拉丁 c/o 混入西里尔字母做同形字混淆；`ercouhzjsf.xml` 未声明 `android:description`，系统无障碍列表仅显示“主进程”标签、无任何风险说明。目标 SDK 27，故无 Android 13+ 受限设置分步教学。
- 静态可见性：无障碍诱导链全部为明文 DEX 逻辑，无加壳、无加密载荷、无远端 HTML；远端 `hellowopung.com/.../index.php` 仅用于短信指令下发（属后续远控链，不参与引导流程）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链全部为明文 DEX 逻辑（CoalitionLick/Assignment/DieExpenditure/FindStunning/e/RecoverHerd），无加壳、无 AES 载荷、无 WebView/远端 HTML；远端 hellowopung.com/e8tmlzl7zeb7jynh5ii8/index.php 仅承载获权后的短信指令，不影响引导流程的静态可见性。",
  "summary_one_liner": "冷启动即以假故障 Toast 加静默跳转 android.settings.ACCESSIBILITY_SETTINGS，并以约10秒节流的轮询死循环反复重跳，直到用户开启名为『主进程』的无障碍服务，全程无说明页、无取消按钮。",
  "disguise_identity": {
    "app_display_name": "СМC - Сooбщeниe",
    "claimed_brand_or_persona": "冒充系统级『主进程』（Оcновной прoцесc）与短信应用（СМC - Сooбщeниe，即 SMS - Message）",
    "a11y_service_label": "Оcновной прoцесc",
    "identity_mismatch": true,
    "obfuscation_tricks": "同形字混淆：应用名与服务名中用拉丁字母 c/o 混入西里尔字母（『Сиcтeма』『Оcновной прoцесc』『прoцесc』）；无障碍配置 ercouhzjsf.xml 刻意不声明 android:description，系统列表无任何用途说明；以『статистике（统计）』指代无障碍权限，弱化敏感度；首次运行后 setComponentEnabledSetting 禁用启动器组件 CoalitionLick，桌面图标消失，仅能经前台通知『RecoverHerd/Recruit』通道再次拉起，规避用户卸载与二次核查。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "org.day.cold.CoalitionLick（LAUNCHER Activity）",
      "trigger_event": "用户点击桌面图标，onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见界面，super.onCreate 后立即 finish()，界面一闪即逝",
      "user_action_requested": "无（用户仅感知为『点了没反应』或一闪而过）",
      "code_anchor": "org.day.cold.CoalitionLick#onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "org.day.cold.Assignment（Application）+ org.day.cold.FindStunning（前台 Service）+ 通知栏",
      "trigger_event": "Application.onCreate：startForegroundService → FindStunning.onStartCommand → a()",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Оcновной прoцесc / Сиcтeма нe корректнo рaботaeт, вaм нeобхoдимо включить дoступ к cтaтистике для 'Оcновной прoцесc'",
      "shown_text_zh": "通知标题：主进程；正文：系统运行不正常，您需要为『主进程』开启统计访问权限",
      "user_action_requested": "无明确要求，仅作为常驻伪装通知维持进程存活；同时 b() 调用 setComponentEnabledSetting(CoalitionLick, 2) 禁用桌面图标",
      "code_anchor": "org.day.cold.FindStunning#a / org.day.cold.FindStunning#b"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "org.day.cold.DieExpenditure（无布局的透明 Activity，主题 Theme.Translucent.NoTitleBar.Fullscreen）+ Toast",
      "trigger_event": "e.a(context, now) → e.c(context, now)：距上次跳转超过 9952ms 时 startActivity(DieExpenditure)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Сиcтeма нe корректнo рaботaeт, вaм нeобхoдимо включить дoступ к cтaтистике для 'Оcновной прoцесc'",
      "shown_text_zh": "系统运行不正常，您需要为『主进程』开启统计访问权限",
      "user_action_requested": "无按钮、无取消/跳过选项，Toast 展示后立即跳转设置页并 finish()，用户只能被动跟随跳转",
      "code_anchor": "org.day.cold.DieExpenditure#onCreate（Toast + getString(2131034112)）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍 → 已下载的服务列表）",
      "trigger_event": "DieExpenditure.onCreate 内 new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(0x10000000).startActivity()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Оcновной прoцесc（系统列表中的服务项标签，无 description 说明）",
      "shown_text_zh": "系统无障碍服务列表中出现一项名为『主进程』的服务，无任何用途描述",
      "user_action_requested": "要求用户手动点开『Оcновной прoцесc』并开启开关（无应用内说明辅助，仅靠伪造的“系统故障”语境施压）",
      "code_anchor": "org.day.cold.DieExpenditure#onCreate（Intent android.settings.ACCESSIBILITY_SETTINGS）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "Assignment 静态 Handler 轮询线程 Assignment$1 + DieExpenditure 反复重启",
      "trigger_event": "Assignment$1.run 每 1012ms 执行 e.b(ctx, now)：f(ctx) 读取 Settings.Secure.enabled_accessibility_services 不含 org.day.cold 时返回 false，随即 e.c 每 9952ms 再 startActivity(DieExpenditure)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Сиcтeма нe корректнo рaботaeт, вaм нeобхoдимо включить дoступ к cтaтистике для 'Оcновной прoцесc'",
      "shown_text_zh": "系统运行不正常，您需要为『主进程』开启统计访问权限（每次重跳前重复弹出）",
      "user_action_requested": "用户按返回键退出设置页后约 10 秒内被再次强制拉回无障碍设置页，无退出或降级路径",
      "code_anchor": "org.day.cold.Assignment$1#run / org.day.cold.e#b / org.day.cold.e#c / org.day.cold.e#f"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "系统『更改默认短信应用』确认对话框 + RecoverHerd（无障碍服务）自动点击",
      "trigger_event": "f(ctx) 为 true 后：stopService(FindStunning)；a() 内若 org.day.cold 非默认短信包则 startActivity(ACTION_CHANGE_DEFAULT, package=org.day.cold) 并 RecoverHerd.a(true)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（自动点击 android:id/button1 / android:id/right_button 完成确认）",
      "shown_text_zh": "无障碍服务自动点击系统对话框的确认按钮，把本应用设为默认短信应用；并对远端配置的包名执行 GLOBAL_ACTION_BACK(2) 关闭其界面",
      "user_action_requested": "无需用户操作；用户若尝试回到设置页撤权，服务会以 performGlobalAction(2) 返回键干扰",
      "code_anchor": "org.day.cold.Assignment$1#a / org.day.cold.RecoverHerd#onAccessibilityEvent / org.day.cold.RecoverHerd#a"
    }
  ],
  "text_presentation_locations": [
    "Toast（org.day.cold.DieExpenditure.onCreate，getString(2131034112)）——唯一“说明文字”，悬浮于系统无障碍设置页之上，无按钮、无取消",
    "常驻前台通知（org.day.cold.FindStunning.a，频道 org.day.cold.GUARANTEE / 标题 getString(2131034113)『Оcновной прoцесc』，正文 getString(2131034112) 假故障文案），作为伪装进程与二次拉起入口",
    "系统无障碍服务列表项标签：AndroidManifest 中 service android:label=\"Оcновной прoцесc\"（引用 strings.xml accessibility_title）",
    "res/values/strings.xml：accessibility_desc（假故障长文案）、accessibility_title（主进程）、button_1=android:id/button1、button_right=android:id/right_button（自动点击目标 id）",
    "res/xml/ercouhzjsf.xml：无障碍能力声明（canRetrieveWindowContent=true、flagReportViewIds、监听 window 内容/状态变化），刻意不含 android:description，故系统列表无任何说明文字",
    "无 assets/ 本地 HTML、无 WebView、无悬浮窗 Overlay、无高仿系统开关页、无应用内自定义引导 Dialog"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Сиcтeма нe корректнo рaботaeт, вaм нeобхoдимо включить дoступ к cтaтистике для 'Оcновной прoцесc'",
      "text_zh": "系统运行不正常，您需要为『主进程』开启统计访问权限",
      "source_location": "res/values/strings.xml key=accessibility_desc（代码引用 getString(2131034112)，用于 DieExpenditure Toast 与前台通知正文）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": "Оcновной прoцесc",
      "text_zh": "主进程",
      "source_location": "res/values/strings.xml key=accessibility_title；AndroidManifest 中 accessibility service 的 android:label；前台通知标题 getString(2131034113)",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "СМC - Сooбщeниe",
      "text_zh": "SMS - 消息",
      "source_location": "AndroidManifest application android:label（桌面显示名，拉丁 C/o 混入西里尔字母）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "Assignment$1.run 以 1012ms 周期轮询 Settings.Secure.enabled_accessibility_services 是否包含 org.day.cold；未开启时 e.c 以 9952ms 节流重新 startActivity(DieExpenditure)，即用户从设置页返回后约 10 秒内被再次弹假故障 Toast 并强制拉回无障碍设置页，形成不可退出的死循环；同时前台服务通知常驻、桌面图标已被禁用，用户无正常退出入口。",
    "overlay_or_fake_settings": "无半透明遮罩、无全屏悬浮窗、无高仿系统开关页；仅在系统无障碍设置页之上叠加一条 Toast 假故障提示（主题为 Theme.Translucent.NoTitleBar.Fullscreen 的空 Activity 负责弹出并立即 finish）。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，样本 2018 年，不涉及 Android 13+ 受限设置引导）",
    "post_grant_anti_removal": "获权后 RecoverHerd.a(true) 置标志位，onAccessibilityEvent 通过 findAccessibilityNodeInfosByViewId(android:id/button1、android:id/right_button) 自动 performAction(16) 点击系统确认框（用于自动将 org.day.cold 设为默认短信应用）；并对 SharedPreferences『Magnitude』中远端下发的包名执行 performGlobalAction(2)=GLOBAL_ACTION_BACK 关闭界面，干扰撤权与第三方安全界面。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（或当前前台包名由 org.day.cold 切换为 com.android.settings 无障碍页）的瞬间立即抓取；该动作在冷启动后 1 秒内首次触发，并在用户每次返回后约 10 秒重复触发，是稳定的 UTG 采样窗口。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前 Toast 与瞬时透明 Activity",
        "page_identifier": "包名 org.day.cold 前台 + 无布局透明 Activity（DieExpenditure）+ Toast 文本『Сиcтeма нe корректнo рaботaeт…』",
        "why_most_useful": "此处是唯一的“说明”载体，证明应用未提供任何可取消的引导页，直接以伪造系统故障话术推动用户跳设置",
        "observable_utg_signals": ["Toast 节点文本含『Сиcтeма』『стaтистике』『Оcновной прoцесc』", "页面无任何可点击按钮/取消控件", "Activity 生命周期极短（onCreate 即 finish）"]
      },
      {
        "page_role": "系统无障碍服务列表项（Оcновной прoцесc）",
        "page_identifier": "com.android.settings 无障碍页，列表项文本『Оcновной прoцесc』，无描述副标题",
        "why_most_useful": "证明服务标签冒充系统“主进程”、且 android:description 缺失导致用户无从判断用途，是身份伪装的关键判据",
        "observable_utg_signals": ["列表项 label=Оcновной прoцесc 且 summary/description 为空", "开关初始为关闭状态", "同一页面短时间内被重复压栈/重复拉起"]
      },
      {
        "page_role": "拒权后重跳循环页",
        "page_identifier": "返回键退出设置后约 10 秒，前台再次切回 org.day.cold（DieExpenditure）并跳转无障碍设置",
        "why_most_useful": "直接观测『拒绝即重跳』的强制循环，是区分恶意诱导与良性引导的决定性动态证据",
        "observable_utg_signals": ["ACCESSIBILITY_SETTINGS 跳转次数在 60 秒内≥3 次", "两次跳转间隔约 10 秒", "前台包名在 org.day.cold 与 com.android.settings 之间反复切换"]
      },
      {
        "page_role": "获权后自动确认系统对话框",
        "page_identifier": "系统『更改默认短信应用』对话框，按钮被无障碍自动点击",
        "why_most_useful": "验证获权后立即用于自授权与后续短信劫持，体现权限的真实用途",
        "observable_utg_signals": ["无障碍点击事件来源为 org.day.cold 服务", "默认短信应用被改为 org.day.cold", "对话框无用户实际操作即消失"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无图空文本、无远端 HTML 外壳；但存在两处观测盲区：(1) 首次运行后桌面图标被 setComponentEnabledSetting 禁用，UTG 若按包名/图标枚举应用可能漏采，需以通知栏『Оcновной прoцесc』为入口或直接冷启动组件；(2) 获权后远端 hellowopung.com 下发短信指令与控制包名（SharedPreferences『Magnitude』），该部分为动态远端内容，静态不可见。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "org.day.cold.DieExpenditure#onCreate",
    "org.day.cold.Assignment$1#run",
    "org.day.cold.e#c",
    "org.day.cold.e#f",
    "org.day.cold.FindStunning#a",
    "res/values/strings.xml / res/xml/ercouhzjsf.xml"
  ]
}
```

补充说明（覆盖边界）：受本轮工具调用上限约束，未再执行 `register_evidence_graph` / `record_risk` 落库，以上结论未写入项目风险台账；同时未展开远端 `hellowopung.com` 的短信远控指令集与 `Mirror`/`d` 上报链，该部分属获权后行为，不影响本次“无障碍权限诱导”命题的判定。

</details>
