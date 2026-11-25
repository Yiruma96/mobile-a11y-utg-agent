# MR_164__fde7ca904d｜donot — Android Sys

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：97.8s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即用不可取消的原生弹窗要求为与桌面同名的 'Android Sys' 无障碍服务授权，唯一按钮直达系统无障碍设置页，并在用户离开主界面时禁用自身启动组件以切断入口。
- **静态可见性说明**：无障碍引导链完全静态可见：MainActivity.onCreate 的不可取消 AlertDialog、b.b.a.a.a.onClick 的 ACCESSIBILITY_SETTINGS 跳转、accessibility.xml 与 strings.xml 中的同名 label/description 均可直接读取。未发现加壳、AES 载荷或远端 HTML 承载引导文案；布局中的 WebView 为 gone 状态且不参与引导。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fde7ca904d9ae72ea7e242ee31f7fbaee963937341ca2863d483300828a4c6e0` |
| 包名 / 年份 | `com.androidsys.app` / 2019 |
| 家族 / 品类 | **donot**（同池样本数：18） |
| 原始来源标识 | https://ti.360.net/blog/articles/donot-gang-mobile-new-attack-framework-tool-analysis/ |
| 桌面显示名 | Android Sys |
| 引导页宣称品牌/身份 | Android Sys（伪造系统级 Android 组件身份） |
| 系统无障碍列表服务名 | Android Sys |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用名、无障碍服务 android:label、android:description 三者同源指向 @string/app_name，使系统无障碍列表条目与桌面应用名完全一致，用户无法区分系统组件与第三方服务；代码经类名混淆（a.b/b.b.a.a 等）；onPause 与 onBackPressed 中 setComponentEnabledSetting 禁用启动组件并广播 UNINSTALL_SHORTCUT 移除名为 ServiceService 的快捷方式，属入口隐藏而非同形字或空白挤出；未见多 activity-alias 或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.qooqle.droid.mrch.ani.ninere` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Android Sys |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.qooqle.droid.mrch.MainActivity（LAUNCHER 入口 Activity） | onCreate 执行 setContentView 并 startService(new Intent(this, ate.class)) | 原生Activity | **原文**：Please Wait....<br>**译注**：请稍候……（进度条骨架页，无任何功能说明） | 无，页面仅为等待态 | `com.qooqle.droid.mrch.MainActivity.onCreate / res/layout/activity_main.xml` |
| 2 | 引导说明页 | AlertDialog（AlertDialog.Builder 构建，setCancelable(false)） | onCreate 内 MainActivity.a(Context) 检测 Settings.Secure 的 accessibility_enabled 与 enabled_accessibility_services 未包含 本包名/com.qooqle.droid.mrch.ani.ninere 时弹出 | 原生Dialog | **原文**：Please enable 'Accessibility' for 'Android Sys' to get this working. Tap on 'Ok' to go to Accessibility Settings.<br>**译注**：请为“Android Sys”启用“无障碍”功能以使其正常工作。点击“确定”前往无障碍设置。 | 仅有一个 'Ok' 正按钮；无取消、无跳过、无说明为何需要无障碍、无隐私或用途解释；setCancelable(false) 且 onBackPressed 不调用 super，返回键无法关闭 | `com.qooqle.droid.mrch.MainActivity.onCreate（硬编码字符串，getString(2131427344)=app_name）` |
| 3 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（android.settings.ACCESSIBILITY_SETTINGS） | 用户点击弹窗 'Ok' → b.b.a.a.a.onClick 执行 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | 无 | 用户需自行在列表中查找与应用同名的“Android Sys”条目并手动打开开关；应用不提供任何叠加遮罩或指引 | `b.b.a.a.a.onClick` |
| 4 | 拒权反馈循环 | MainActivity（无 onResume 重检测、无 Timer、无重弹） | 用户从系统设置返回或直接按 Home/返回键离开 → MainActivity.onPause / onBackPressed | 不可静态还原 | 无 | 无提示，用户不会被再次要求授权，但桌面入口同时消失，形成“拒绝即失去入口”的隐式胁迫 | `com.qooqle.droid.mrch.MainActivity.onPause / onBackPressed / a()` |
| 5 | 获权后动作 | com.qooqle.droid.mrch.ani.ninere（AccessibilityService，onServiceConnected） | 系统绑定无障碍服务后 onServiceConnected 初始化 MD5 与事件列表；随后 onAccessibilityEvent → ninere.a(AccessibilityEvent) | 不可静态还原 | 无 | 无 | `com.qooqle.droid.mrch.ani.ninere.onServiceConnected / com.qooqle.droid.mrch.ani.ninere.a(AccessibilityEvent)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity.onCreate 中的不可取消 AlertDialog 正文（硬编码英文字符串，插入 getString(2131427344) 即 strings.xml 的 app_name=Android Sys）
- 同一弹窗的唯一按钮文本 'Ok'（AlertDialog.Builder.setPositiveButton）
- res/layout/activity_main.xml 的等待态 TextView 文本 'Please Wait....'、不可用态 TextView 'Your Device is not Supported as of now.'、Button 'Uninstall'
- 系统无障碍服务列表条目：service android:label=@string/app_name 与 res/xml/accessibility.xml 的 android:description=@string/app_name，均显示为 'Android Sys'
- res/values/strings.xml 的 app_name=Android Sys（同时用作桌面名、服务名、无障碍说明）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please enable 'Accessibility' for 'Android Sys' to get this working. Tap on 'Ok' to go to Accessibility Settings. | 请为“Android Sys”启用“无障碍”功能以使其正常工作。点击“确定”前往无障碍设置。 | `com.qooqle.droid.mrch.MainActivity.onCreate 硬编码字符串 + strings.xml key app_name` | 受限设置分步教学 |
| en | Ok | 确定 | `MainActivity.onCreate AlertDialog.Builder.setPositiveButton` | 受限设置分步教学 |
| en | Please Wait.... | 请稍候…… | `res/layout/activity_main.xml @id/loading` | 良性透明说明 |
| en | Your Device is not Supported as of now. | 您的设备目前不受支持。 | `res/layout/activity_main.xml @id/textView` | 故障恐吓 |
| en | Uninstall | 卸载 | `res/layout/activity_main.xml @id/button` | 未知 |
| en | Android Sys | 安卓系统（系统化伪名） | `res/values/strings.xml key app_name，同时用于应用 label、service label 与 accessibility.xml description` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无 onResume 重弹、无 Timer 重跳、无死循环。实际反馈为：用户离开主界面（onPause）或按返回键（onBackPressed，未调用 super）时执行 setComponentEnabledSetting(getComponentName(), 2, 1) 禁用启动组件并广播 com.android.launcher.action.UNINSTALL_SHORTCUT 移除名为 ServiceService 的快捷方式，桌面入口消失；再次启动也不会重新校验，形成“拒绝即失去入口”的静默胁迫而非显式循环
- **遮罩叠层 / 高仿系统设置页**：无。未使用悬浮窗遮罩、未绘制高仿系统无障碍开关页，也未在设置页后压栈叠加引导层；跳转后即脱离应用控制
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：未发现。全包无 performGlobalAction、无 GLOBAL_ACTION_BACK/HOME、无监听设置页阻止撤权；仅有 onPause 禁用自身组件与移除快捷方式的入口隐藏行为
- **良性降级 / 替代方案**：无。未提供手动模式、ADB 路径或仅观看模式等替代方案

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 MainActivity（LAUNCHER 入口）onCreate 完成后、检测到 android.settings.ACCESSIBILITY_SETTINGS 即将跳转前拉起；最佳抓取点为冷启动后首个 Activity 出现 AlertDialog 的瞬间，以及点击 'Ok' 后 300–800ms 内系统无障碍列表页完成渲染时
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导文案为硬编码英文纯文本，非图片或远端 HTML。需注意两点：一是引导仅存在于冷启动 onCreate 一次，若设备已预先启用该服务则弹窗完全不出现，UTG 需在干净环境首次安装后立即抓取；二是获权后行为（WhatsApp 窗口文本抓取与本地落库）完全无界面，纯 UTG 无法观察，需配合无障碍事件 Hook 或数据库检查。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | com.qooqle.droid.mrch.MainActivity 上覆盖的 AlertDialog，仅一个 'Ok' 按钮、无取消按钮、返回键无响应 | 这是全包唯一的无障碍引导载体，直接证明引导时机为冷启动 0 步阻断且不可取消，是判定强制性的核心证据 | 弹窗文本 'Please enable Accessibility for Android Sys...'；正按钮集合仅含 'Ok'，无 'Cancel'/'Skip'/'Later' 节点；按返回键后弹窗仍存在（不可取消） |
| **系统无障碍服务列表项** | android.settings.ACCESSIBILITY_SETTINGS 页面中显示名称为 'Android Sys' 的条目 | 验证服务名与应用名完全一致的系统化伪装，且条目无任何辅助功能性质说明，是身份混淆的直接运行时证据 | 列表条目 text='Android Sys'，与应用桌面名完全相同；条目无 '屏幕朗读/辅助/服务' 类用途描述；开关初始为关闭，开启后服务被绑定 |
| **离开主界面后的桌面入口状态** | 返回桌面 / 再次点击图标时的 Launcher 状态 | 用于验证 onPause 触发的 setComponentEnabledSetting(2) 与 UNINSTALL_SHORTCUT 是否实际生效，即用户拒权或返回后入口消失的胁迫效果 | 桌面图标消失或点击无响应；应用列表中 com.androidsys.app 的 MainActivity 组件处于 disabled 状态；无 ServiceService 快捷方式残留 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.qooqle.droid.mrch.MainActivity.onCreate`
- `com.qooqle.droid.mrch.MainActivity.a`
- `com.qooqle.droid.mrch.MainActivity.onPause`
- `b.b.a.a.a.onClick`
- `res/xml/accessibility.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，14 次工具调用内收口）

- **引导方式极简、无任何教学页面**：全包仅在 [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.qooqle.droid.mrch.MainActivity#onCreate>) 出现一次无障碍引导，载体是**原生 AlertDialog**，不是 WebView、HTML 或悬浮窗。布局 [activity_main.xml](<resource-unit:#1 file:res/layout/activity_main.xml>) 虽有 WebView 容器，但 `visibility="gone"`，且与无障碍引导无关。
- **冷启动即阻断**：`setCancelable(false)` + 单一 `Ok` 正按钮，无取消/跳过；文案直白要求为 `Android Sys` 开启 Accessibility。点击后 [b.b.a.a.a.onClick()](<resource-unit:#1.dex1 code:b.b.a.a.a#onClick>) 仅执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`。
- **无拒权循环，但有"断退路"机制**：全包无 `onResume` 重弹、无 Timer 重跳、无 `GLOBAL_ACTION_BACK`、无 `APPLICATION_DETAILS_SETTINGS`（受限设置分步教学、Session 绕过均无）；但 [MainActivity.a()](<resource-unit:#1.dex1 code:com.qooqle.droid.mrch.MainActivity#a>) 在 `onPause`/`onBackPressed` 中调用 `setComponentEnabledSetting(...,2,1)` 禁用启动组件并广播 `UNINSTALL_SHORTCUT`（名 `ServiceService`），用户一离开主界面即失去入口。
- **身份伪装**：桌面名 `Android Sys`、服务 `android:label` 与 [accessibility.xml](<resource-unit:#1 file:res/xml/accessibility.xml>) 的 `android:description` 三者全部指向同一 [strings.xml](<resource-unit:#1 file:res/values/strings.xml>) 键 `app_name`，即系统无障碍列表中显示与应用完全同名的"系统化"条目，无任何辅助功能性质说明；同时声明 `canRetrieveWindowContent="true"` 监听点击/焦点/文本变化/窗口内容与状态。
- **获权后用途与名义背离**：[ninere.a(AccessibilityEvent)](<resource-unit:#1.dex1 code:com.qooqle.droid.mrch.ani.ninere#a>) 定向抓取 `com.whatsapp` 窗口节点文本并写入本地 `WappMap` 表（SQLite），属通信内容窃取，非无障碍辅助。
- **覆盖边界**：未发现加壳或密文动态加载，引导链完整静态可见；远端下发内容（`ate` IntentService 的 C2）不在本轮 UTG 引导专题范围内。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链完全静态可见：MainActivity.onCreate 的不可取消 AlertDialog、b.b.a.a.a.onClick 的 ACCESSIBILITY_SETTINGS 跳转、accessibility.xml 与 strings.xml 中的同名 label/description 均可直接读取。未发现加壳、AES 载荷或远端 HTML 承载引导文案；布局中的 WebView 为 gone 状态且不参与引导。",
  "summary_one_liner": "冷启动即用不可取消的原生弹窗要求为与桌面同名的 'Android Sys' 无障碍服务授权，唯一按钮直达系统无障碍设置页，并在用户离开主界面时禁用自身启动组件以切断入口。",
  "disguise_identity": {
    "app_display_name": "Android Sys",
    "claimed_brand_or_persona": "Android Sys（伪造系统级 Android 组件身份）",
    "a11y_service_label": "Android Sys",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用名、无障碍服务 android:label、android:description 三者同源指向 @string/app_name，使系统无障碍列表条目与桌面应用名完全一致，用户无法区分系统组件与第三方服务；代码经类名混淆（a.b/b.b.a.a 等）；onPause 与 onBackPressed 中 setComponentEnabledSetting 禁用启动组件并广播 UNINSTALL_SHORTCUT 移除名为 ServiceService 的快捷方式，属入口隐藏而非同形字或空白挤出；未见多 activity-alias 或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.qooqle.droid.mrch.MainActivity（LAUNCHER 入口 Activity）",
      "trigger_event": "onCreate 执行 setContentView 并 startService(new Intent(this, ate.class))",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please Wait....",
      "shown_text_zh": "请稍候……（进度条骨架页，无任何功能说明）",
      "user_action_requested": "无，页面仅为等待态",
      "code_anchor": "com.qooqle.droid.mrch.MainActivity.onCreate / res/layout/activity_main.xml"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "AlertDialog（AlertDialog.Builder 构建，setCancelable(false)）",
      "trigger_event": "onCreate 内 MainActivity.a(Context) 检测 Settings.Secure 的 accessibility_enabled 与 enabled_accessibility_services 未包含 本包名/com.qooqle.droid.mrch.ani.ninere 时弹出",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please enable 'Accessibility' for 'Android Sys' to get this working. Tap on 'Ok' to go to Accessibility Settings.",
      "shown_text_zh": "请为“Android Sys”启用“无障碍”功能以使其正常工作。点击“确定”前往无障碍设置。",
      "user_action_requested": "仅有一个 'Ok' 正按钮；无取消、无跳过、无说明为何需要无障碍、无隐私或用途解释；setCancelable(false) 且 onBackPressed 不调用 super，返回键无法关闭",
      "code_anchor": "com.qooqle.droid.mrch.MainActivity.onCreate（硬编码字符串，getString(2131427344)=app_name）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "用户点击弹窗 'Ok' → b.b.a.a.a.onClick 执行 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接进入系统无障碍服务列表，未做任何定位或高亮；列表中条目显示为“Android Sys”",
      "user_action_requested": "用户需自行在列表中查找与应用同名的“Android Sys”条目并手动打开开关；应用不提供任何叠加遮罩或指引",
      "code_anchor": "b.b.a.a.a.onClick"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity（无 onResume 重检测、无 Timer、无重弹）",
      "trigger_event": "用户从系统设置返回或直接按 Home/返回键离开 → MainActivity.onPause / onBackPressed",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无二次弹窗或循环拉起；取而代之的是在离开瞬间禁用自身启动组件并移除桌面快捷方式",
      "user_action_requested": "无提示，用户不会被再次要求授权，但桌面入口同时消失，形成“拒绝即失去入口”的隐式胁迫",
      "code_anchor": "com.qooqle.droid.mrch.MainActivity.onPause / onBackPressed / a()"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.qooqle.droid.mrch.ani.ninere（AccessibilityService，onServiceConnected）",
      "trigger_event": "系统绑定无障碍服务后 onServiceConnected 初始化 MD5 与事件列表；随后 onAccessibilityEvent → ninere.a(AccessibilityEvent)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台静默运行，无任何界面反馈；针对 com.whatsapp 抓取窗口节点文本并写入本地 SQLite（WappMap 表）",
      "user_action_requested": "无",
      "code_anchor": "com.qooqle.droid.mrch.ani.ninere.onServiceConnected / com.qooqle.droid.mrch.ani.ninere.a(AccessibilityEvent)"
    }
  ],
  "text_presentation_locations": [
    "MainActivity.onCreate 中的不可取消 AlertDialog 正文（硬编码英文字符串，插入 getString(2131427344) 即 strings.xml 的 app_name=Android Sys）",
    "同一弹窗的唯一按钮文本 'Ok'（AlertDialog.Builder.setPositiveButton）",
    "res/layout/activity_main.xml 的等待态 TextView 文本 'Please Wait....'、不可用态 TextView 'Your Device is not Supported as of now.'、Button 'Uninstall'",
    "系统无障碍服务列表条目：service android:label=@string/app_name 与 res/xml/accessibility.xml 的 android:description=@string/app_name，均显示为 'Android Sys'",
    "res/values/strings.xml 的 app_name=Android Sys（同时用作桌面名、服务名、无障碍说明）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please enable 'Accessibility' for 'Android Sys' to get this working. Tap on 'Ok' to go to Accessibility Settings.",
      "text_zh": "请为“Android Sys”启用“无障碍”功能以使其正常工作。点击“确定”前往无障碍设置。",
      "source_location": "com.qooqle.droid.mrch.MainActivity.onCreate 硬编码字符串 + strings.xml key app_name",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Ok",
      "text_zh": "确定",
      "source_location": "MainActivity.onCreate AlertDialog.Builder.setPositiveButton",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please Wait....",
      "text_zh": "请稍候……",
      "source_location": "res/layout/activity_main.xml @id/loading",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Your Device is not Supported as of now.",
      "text_zh": "您的设备目前不受支持。",
      "source_location": "res/layout/activity_main.xml @id/textView",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Uninstall",
      "text_zh": "卸载",
      "source_location": "res/layout/activity_main.xml @id/button",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Sys",
      "text_zh": "安卓系统（系统化伪名）",
      "source_location": "res/values/strings.xml key app_name，同时用于应用 label、service label 与 accessibility.xml description",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无 onResume 重弹、无 Timer 重跳、无死循环。实际反馈为：用户离开主界面（onPause）或按返回键（onBackPressed，未调用 super）时执行 setComponentEnabledSetting(getComponentName(), 2, 1) 禁用启动组件并广播 com.android.launcher.action.UNINSTALL_SHORTCUT 移除名为 ServiceService 的快捷方式，桌面入口消失；再次启动也不会重新校验，形成“拒绝即失去入口”的静默胁迫而非显式循环",
    "overlay_or_fake_settings": "无。未使用悬浮窗遮罩、未绘制高仿系统无障碍开关页，也未在设置页后压栈叠加引导层；跳转后即脱离应用控制",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "未发现。全包无 performGlobalAction、无 GLOBAL_ACTION_BACK/HOME、无监听设置页阻止撤权；仅有 onPause 禁用自身组件与移除快捷方式的入口隐藏行为",
    "benign_graceful_degradation": "无。未提供手动模式、ADB 路径或仅观看模式等替代方案"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 MainActivity（LAUNCHER 入口）onCreate 完成后、检测到 android.settings.ACCESSIBILITY_SETTINGS 即将跳转前拉起；最佳抓取点为冷启动后首个 Activity 出现 AlertDialog 的瞬间，以及点击 'Ok' 后 300–800ms 内系统无障碍列表页完成渲染时",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "com.qooqle.droid.mrch.MainActivity 上覆盖的 AlertDialog，仅一个 'Ok' 按钮、无取消按钮、返回键无响应",
        "why_most_useful": "这是全包唯一的无障碍引导载体，直接证明引导时机为冷启动 0 步阻断且不可取消，是判定强制性的核心证据",
        "observable_utg_signals": [
          "弹窗文本 'Please enable Accessibility for Android Sys...'",
          "正按钮集合仅含 'Ok'，无 'Cancel'/'Skip'/'Later' 节点",
          "按返回键后弹窗仍存在（不可取消）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 页面中显示名称为 'Android Sys' 的条目",
        "why_most_useful": "验证服务名与应用名完全一致的系统化伪装，且条目无任何辅助功能性质说明，是身份混淆的直接运行时证据",
        "observable_utg_signals": [
          "列表条目 text='Android Sys'，与应用桌面名完全相同",
          "条目无 '屏幕朗读/辅助/服务' 类用途描述",
          "开关初始为关闭，开启后服务被绑定"
        ]
      },
      {
        "page_role": "离开主界面后的桌面入口状态",
        "page_identifier": "返回桌面 / 再次点击图标时的 Launcher 状态",
        "why_most_useful": "用于验证 onPause 触发的 setComponentEnabledSetting(2) 与 UNINSTALL_SHORTCUT 是否实际生效，即用户拒权或返回后入口消失的胁迫效果",
        "observable_utg_signals": [
          "桌面图标消失或点击无响应",
          "应用列表中 com.androidsys.app 的 MainActivity 组件处于 disabled 状态",
          "无 ServiceService 快捷方式残留"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导文案为硬编码英文纯文本，非图片或远端 HTML。需注意两点：一是引导仅存在于冷启动 onCreate 一次，若设备已预先启用该服务则弹窗完全不出现，UTG 需在干净环境首次安装后立即抓取；二是获权后行为（WhatsApp 窗口文本抓取与本地落库）完全无界面，纯 UTG 无法观察，需配合无障碍事件 Hook 或数据库检查。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.qooqle.droid.mrch.MainActivity.onCreate",
    "com.qooqle.droid.mrch.MainActivity.a",
    "com.qooqle.droid.mrch.MainActivity.onPause",
    "b.b.a.a.a.onClick",
    "res/xml/accessibility.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
