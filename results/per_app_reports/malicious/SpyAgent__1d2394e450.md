# MR_013__1d2394e450｜SpyAgent — Google Play Service

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：108.6s

## 1. 一句话核心结论

- **核心申请方式**：该应用不做任何应用内引导，直接把自身伪装成'Google Play Service'注册为无障碍服务，冷启动即隐藏桌面图标并转入后台静默采集各应用窗口文本，靠外部渠道骗取用户手动开启无障碍。
- **静态可见性说明**：无障碍相关代码与资源完全静态可见：服务声明、配置 xml、采集逻辑均在明文 DEX 中，未加壳、无加密载荷、无远端 HTML。需注意本样本的'引导'环节并不在包内，诱导话术来自外部投放渠道，因此包内检索不到任何跳转/弹窗属于事实本身，而非可见性受限。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1d2394e4501d1ed83259333e5aa81cdbc58557c42a4d4976982d84dd6fdd4128` |
| 包名 / 年份 | `com.system.android.updater` / 2018 |
| 家族 / 品类 | **SpyAgent**（同池样本数：12） |
| 原始来源标识 | https://ti.360.net/blog/articles/analysis-of-donot-andriod-sample/ |
| 桌面显示名 | Google Play Service |
| 引导页宣称品牌/身份 | Google Play Service（Google 官方服务，纯属伪造；包名为 com.system.android.updater，与 Google 无关） |
| 系统无障碍列表服务名 | Google Play Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：三重身份复用：android:label、无障碍服务 android:label、无障碍 android:description 全部指向同一 @string/app_name='Google Play Service'；类名与包名数字混淆（nine.ninere、ten、eleven、thirteen）；首次启动后 setComponentEnabledSetting(...,2,1) 禁用启动组件并广播 UNINSTALL_SHORTCUT 删除桌面快捷方式，使用户无法从桌面进入应用撤销授权；未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.system.android.updater.nine.ninere` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Google Play Service |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.system.android.updater.MainActivity | LAUNCHER 图标点击触发 onCreate | 不可静态还原 | 无 | 无任何用户操作请求；应用在用户毫无感知的情况下完成后续动作 | `com.system.android.updater.MainActivity.onCreate` |
| 2 | 冷启动入口 | MainActivity.removeShortcut() → PackageManager / com.android.launcher.action.UNINSTALL_SHORTCUT 广播 | onCreate 内同步调用 removeShortcut() | 不可静态还原 | **原文**：ServiceUpdate（作为 shortcut NAME 传入的广播附加项）<br>**译注**：以'ServiceUpdate'名义移除快捷方式，同时禁用 MainActivity 组件，桌面图标消失 | 无需用户操作；副作用是用户失去通过桌面图标进入应用、关闭无障碍服务的入口 | `com.system.android.updater.MainActivity.removeShortcut` |
| 3 | 冷启动入口 | com.system.android.updater.ten.ten（IntentService，清单中无权限保护） | MainActivity.onCreate 中 startService(new Intent(this, ten.class)) | 不可静态还原 | 无 | 无 | `com.system.android.updater.ten.ten.onStartCommand` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装服务列表项 'Google Play Service' | 由应用外部的投放渠道（短信/钓鱼落地页/话术）引导用户自行进入系统设置开启；包内不存在任何 startActivity(ACTION_ACCESSIBILITY_SETTINGS) 调用 | 系统无障碍页 | **原文**：Google Play Service<br>**译注**：系统无障碍列表中显示的服务名与说明均为'Google Play Service'，用户在系统原生界面手动拨动开关 | 用户在系统无障碍页手动开启该服务（无应用内引导、无取消/跳过按钮，因为应用本身不呈现任何界面） | `#1 file:res/xml/accessibility.xml#L2；#1 file:res/values/strings.xml#L19；#1 manifest:components` |
| 5 | 获权后动作 | com.system.android.updater.nine.ninere（AccessibilityService） | onServiceConnected 初始化 ninelo 列表；随后 onAccessibilityEvent 在 klog.wm 为真时处理 TYPE_WINDOW_STATE_CHANGED(32)/TYPE_VIEW_TEXT_CHANGED(16)/TYPE_WINDOW_CONTENT_CHANGED(8) | 不可静态还原 | 无 | 无；用户完全无感知 | `com.system.android.updater.nine.ninere.onAccessibilityEvent / addnew / newjson；com.system.android.updater.nine.ninere$keyclass.run` |
| 6 | 业务功能触发 | com.system.android.updater.nine.nine.isAccessibilitySettingsOn(Context) | 读取 Settings.Secure 'accessibility_enabled' 与 'enabled_accessibility_services' 自检本服务是否已启用 | 不可静态还原 | 无 | 无 | `com.system.android.updater.nine.nine.isAccessibilitySettingsOn` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务名与说明均为 'Google Play Service'（@string/app_name，经 res/xml/accessibility.xml 的 android:description 复用），这是全应用唯一对外呈现的无障碍相关文字
- 桌面启动图标名称：'Google Play Service'（AndroidManifest 的 application android:label），但首次启动后该组件即被 setComponentEnabledSetting(...,2,1) 禁用并从桌面移除
- 应用内：无任何位置。不存在 AlertDialog、Activity 布局文案、assets/ HTML 教学页、WebView、悬浮引导窗或通知栏引导
- 外部渠道（包外）：诱导开启无障碍的话术由投放侧的短信/落地页承担，不在 APK 内，静态不可见

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Play Service | 谷歌 Play 服务 | `res/values/strings.xml app_name（同时用于 application android:label、无障碍服务 android:label、无障碍 android:description）` | 未知 |
| en | ServiceUpdate | 服务更新 | `com.system.android.updater.MainActivity.removeShortcut() 中 EXTRA_SHORTCUT_NAME 硬编码` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无拒绝反馈循环：应用内既无跳转无障碍设置，也无 onResume 死循环重跳、无定时器拉起；用户若不在系统设置中开启，应用不会做出任何提示或反应，仅保持后台静默运行
- **遮罩叠层 / 高仿系统设置页**：无：未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无主动阻止撤权行为（无 GLOBAL_ACTION_BACK/HOME 监听、无自点确认）；但通过禁用自身启动组件并删除桌面快捷方式，从入口层面使用户难以回到应用，属于入口级反移除
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：不要等应用冷启动弹窗（不存在）。应在外部短信/落地页触发跳转 'android.settings.ACCESSIBILITY_SETTINGS' 的瞬间拉起 UTG，并在用户拨动开关、服务被启用后 1~2 秒内再次采集，确认 AccessibilityService 已绑定且出现 'Google Play Service' 服务项。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：(1) 诱导话术完全在包外的投放渠道，纯 APK 运行期 UTG 无法捕获'引导'环节，只能捕获系统无障碍列表项的伪装名称；(2) 应用冷启动后桌面图标被移除、且无任何界面，UTG 在应用侧几乎采不到页面，须以系统设置页与 logcat 作为主要观测面。本样本未加壳，静态可见性不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（核心判别页）** | 系统设置无障碍页中名称为 'Google Play Service' 的服务条目，其包名对应 com.system.android.updater | 这是全应用唯一对外暴露的无障碍文字，也是判断'名称伪装 + 包名不符'的唯一直接证据 | 服务名文本 'Google Play Service'；同屏存在包名 com.system.android.updater 或其它非 Google 签名线索；开关从 OFF 变为 ON 的瞬时状态 |
| **冷启动瞬间的桌面/应用页（验证无引导）** | 点击图标后立即出现的界面，预期为空白/直接回到桌面，无任何对话框或 Activity 内容 | 证明不存在冷启动引导弹窗，从而把'诱导'归因到外部渠道而非应用内 UI | 无任何应用内文本节点；返回桌面后应用图标/快捷方式消失；无 AlertDialog 类窗口 |
| **获权后的前台目标应用页（验证采集行为）** | 任意含输入框/聊天内容的应用界面，配合日志标签 'Nine Text' 与 'NINE' 出现 | 确认服务真正在读取窗口文本并归集，闭合'获权→窃取'链路 | logcat 出现 'Nine Text' 与包名；logcat 出现 'NINE' accessibilityEnabled=1；Dname 数据库写入增长 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.system.android.updater.MainActivity.onCreate`
- `com.system.android.updater.MainActivity.removeShortcut`
- `com.system.android.updater.nine.ninere.onAccessibilityEvent`
- `com.system.android.updater.nine.ninere.addnew`
- `com.system.android.updater.nine.nine.isAccessibilitySettingsOn`
- `res/xml/accessibility.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（共 12 次工具调用）

**核心结论：该样本不存在任何“引导用户开启无障碍”的运行期流程。** 在 DEX 全量检索中，`android.settings.ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`AlertDialog`、WebView、悬浮窗引导代码全部不存在，`MainActivity` 也没有任何 UI 展示。

**已核实的链路**

1. **冷启动直接转入后台**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.system.android.updater.MainActivity#onCreate>) 只调用 [removeShortcut()](<resource-unit:#1.dex1 code:com.system.android.updater.MainActivity#removeShortcut>) 与 `startService(ten)`，不执行 `setContentView`，也不弹出任何说明页、弹窗或跳转。这种设计方式意味着“没有引导”，而不是“引导藏在远端”。
2. **先隐藏自身**：`removeShortcut()` 通过 `setComponentEnabledSetting(getComponentName(), 2, 1)` 禁用启动组件，并广播 `com.android.launcher.action.UNINSTALL_SHORTCUT`，使桌面图标消失；这会同时阻断用户日后进入设置、关闭无障碍服务的路径。
3. **引导完全依赖外部渠道**：包内唯一与无障碍相关的判断是 [isAccessibilitySettingsOn()](<resource-unit:#1.dex1 code:com.system.android.updater.nine.nine#isAccessibilitySettingsOn>)，它读取 `enabled_accessibility_services` 后，仅用于自检是否已启用；并且静态无调用点。诱导开启的话术（短信、钓鱼落地页）不在应用内。
4. **伪装身份**：应用名、无障碍服务 `android:label` 与 [accessibility.xml](<resource-unit:#1 file:res/xml/accessibility.xml#L2>) 的 `android:description` 三处统一使用 `@string/app_name` = `Google Play Service`（[strings.xml#L19](<resource-unit:#1 file:res/values/strings.xml#L19>)），但实际包名为 `com.system.android.updater`。该配置开启了 `canRetrieveWindowContent="true"`，并监听 `typeViewTextChanged|typeWindowStateChanged`。
5. **获权后即窃取**：[onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.system.android.updater.nine.ninere#onAccessibilityEvent>) 在 `klog.wm` 为真时，把 `event.getText()` 与来源包名交由 [addnew()](<resource-unit:#1.dex1 code:com.system.android.updater.nine.ninere#addnew>) 按应用归类，再启动 `keyclass` 线程，经 [newjson()](<resource-unit:#1.dex1 code:com.system.android.updater.nine.ninere#newjson>) 组装成 `{application, value:[{title,time,message}]}` 形式的明文 JSON 并留存，准备外发。

**UTG 视角要点**：由于引导页面全部位于包外，纯运行期采集在冷启动时不会看到任何弹窗；唯一可直接观测的判别信号，是系统无障碍列表中出现一条名为 `Google Play Service` 的服务项，以及桌面图标缺失。因此，建议把采集时机放在“外部落地页、短信触发跳转系统设置”的瞬间，而不是应用冷启动瞬间。

**覆盖边界**：未逐条还原 `ten$runto.two()` 的网络外发实现，C2 端点与协议尚未确认；未深挖 `eleven`、`thirteen` 等上报模块。无障碍“无引导”结论基于 DEX 全量字符串与类结构检索，若存在运行时反射拼接 action 的情形则静态不可见（可能性低）。

已登记风险：R-001（autonomous_audit / high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍相关代码与资源完全静态可见：服务声明、配置 xml、采集逻辑均在明文 DEX 中，未加壳、无加密载荷、无远端 HTML。需注意本样本的'引导'环节并不在包内，诱导话术来自外部投放渠道，因此包内检索不到任何跳转/弹窗属于事实本身，而非可见性受限。",
  "summary_one_liner": "该应用不做任何应用内引导，直接把自身伪装成'Google Play Service'注册为无障碍服务，冷启动即隐藏桌面图标并转入后台静默采集各应用窗口文本，靠外部渠道骗取用户手动开启无障碍。",
  "disguise_identity": {
    "app_display_name": "Google Play Service",
    "claimed_brand_or_persona": "Google Play Service（Google 官方服务，纯属伪造；包名为 com.system.android.updater，与 Google 无关）",
    "a11y_service_label": "Google Play Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "三重身份复用：android:label、无障碍服务 android:label、无障碍 android:description 全部指向同一 @string/app_name='Google Play Service'；类名与包名数字混淆（nine.ninere、ten、eleven、thirteen）；首次启动后 setComponentEnabledSetting(...,2,1) 禁用启动组件并广播 UNINSTALL_SHORTCUT 删除桌面快捷方式，使用户无法从桌面进入应用撤销授权；未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.system.android.updater.MainActivity",
      "trigger_event": "LAUNCHER 图标点击触发 onCreate",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面内容：onCreate 未调用 setContentView，不弹窗、不跳转、不显示说明页",
      "user_action_requested": "无任何用户操作请求；应用在用户毫无感知的情况下完成后续动作",
      "code_anchor": "com.system.android.updater.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "MainActivity.removeShortcut() → PackageManager / com.android.launcher.action.UNINSTALL_SHORTCUT 广播",
      "trigger_event": "onCreate 内同步调用 removeShortcut()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "ServiceUpdate（作为 shortcut NAME 传入的广播附加项）",
      "shown_text_zh": "以'ServiceUpdate'名义移除快捷方式，同时禁用 MainActivity 组件，桌面图标消失",
      "user_action_requested": "无需用户操作；副作用是用户失去通过桌面图标进入应用、关闭无障碍服务的入口",
      "code_anchor": "com.system.android.updater.MainActivity.removeShortcut"
    },
    {
      "step": 3,
      "stage": "冷启动入口",
      "screen_or_component": "com.system.android.updater.ten.ten（IntentService，清单中无权限保护）",
      "trigger_event": "MainActivity.onCreate 中 startService(new Intent(this, ten.class))",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台服务启动后初始化数据库 Dname、SharedPreferences 与各采集模块（One/two/three/four/five/eleven/thirteen），并启动 ten$runto 线程；全程无界面",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.updater.ten.ten.onStartCommand"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装服务列表项 'Google Play Service'",
      "trigger_event": "由应用外部的投放渠道（短信/钓鱼落地页/话术）引导用户自行进入系统设置开启；包内不存在任何 startActivity(ACTION_ACCESSIBILITY_SETTINGS) 调用",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Play Service",
      "shown_text_zh": "系统无障碍列表中显示的服务名与说明均为'Google Play Service'，用户在系统原生界面手动拨动开关",
      "user_action_requested": "用户在系统无障碍页手动开启该服务（无应用内引导、无取消/跳过按钮，因为应用本身不呈现任何界面）",
      "code_anchor": "#1 file:res/xml/accessibility.xml#L2；#1 file:res/values/strings.xml#L19；#1 manifest:components"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.system.android.updater.nine.ninere（AccessibilityService）",
      "trigger_event": "onServiceConnected 初始化 ninelo 列表；随后 onAccessibilityEvent 在 klog.wm 为真时处理 TYPE_WINDOW_STATE_CHANGED(32)/TYPE_VIEW_TEXT_CHANGED(16)/TYPE_WINDOW_CONTENT_CHANGED(8)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静默记录每个前台应用的窗口文本，按包名归集为 JSON：{application:包名, value:[{title,time,message}]}，供后续外发",
      "user_action_requested": "无；用户完全无感知",
      "code_anchor": "com.system.android.updater.nine.ninere.onAccessibilityEvent / addnew / newjson；com.system.android.updater.nine.ninere$keyclass.run"
    },
    {
      "step": 6,
      "stage": "业务功能触发",
      "screen_or_component": "com.system.android.updater.nine.nine.isAccessibilitySettingsOn(Context)",
      "trigger_event": "读取 Settings.Secure 'accessibility_enabled' 与 'enabled_accessibility_services' 自检本服务是否已启用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅做状态自检（日志标签 NINE），不构成引导；且静态检索无任何调用点，说明作者未打算用它驱动任何提示界面",
      "user_action_requested": "无",
      "code_anchor": "com.system.android.updater.nine.nine.isAccessibilitySettingsOn"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务名与说明均为 'Google Play Service'（@string/app_name，经 res/xml/accessibility.xml 的 android:description 复用），这是全应用唯一对外呈现的无障碍相关文字",
    "桌面启动图标名称：'Google Play Service'（AndroidManifest 的 application android:label），但首次启动后该组件即被 setComponentEnabledSetting(...,2,1) 禁用并从桌面移除",
    "应用内：无任何位置。不存在 AlertDialog、Activity 布局文案、assets/ HTML 教学页、WebView、悬浮引导窗或通知栏引导",
    "外部渠道（包外）：诱导开启无障碍的话术由投放侧的短信/落地页承担，不在 APK 内，静态不可见"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Play Service",
      "text_zh": "谷歌 Play 服务",
      "source_location": "res/values/strings.xml app_name（同时用于 application android:label、无障碍服务 android:label、无障碍 android:description）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "ServiceUpdate",
      "text_zh": "服务更新",
      "source_location": "com.system.android.updater.MainActivity.removeShortcut() 中 EXTRA_SHORTCUT_NAME 硬编码",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无拒绝反馈循环：应用内既无跳转无障碍设置，也无 onResume 死循环重跳、无定时器拉起；用户若不在系统设置中开启，应用不会做出任何提示或反应，仅保持后台静默运行",
    "overlay_or_fake_settings": "无：未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无主动阻止撤权行为（无 GLOBAL_ACTION_BACK/HOME 监听、无自点确认）；但通过禁用自身启动组件并删除桌面快捷方式，从入口层面使用户难以回到应用，属于入口级反移除",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "不要等应用冷启动弹窗（不存在）。应在外部短信/落地页触发跳转 'android.settings.ACCESSIBILITY_SETTINGS' 的瞬间拉起 UTG，并在用户拨动开关、服务被启用后 1~2 秒内再次采集，确认 AccessibilityService 已绑定且出现 'Google Play Service' 服务项。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（核心判别页）",
        "page_identifier": "系统设置无障碍页中名称为 'Google Play Service' 的服务条目，其包名对应 com.system.android.updater",
        "why_most_useful": "这是全应用唯一对外暴露的无障碍文字，也是判断'名称伪装 + 包名不符'的唯一直接证据",
        "observable_utg_signals": ["服务名文本 'Google Play Service'", "同屏存在包名 com.system.android.updater 或其它非 Google 签名线索", "开关从 OFF 变为 ON 的瞬时状态"]
      },
      {
        "page_role": "冷启动瞬间的桌面/应用页（验证无引导）",
        "page_identifier": "点击图标后立即出现的界面，预期为空白/直接回到桌面，无任何对话框或 Activity 内容",
        "why_most_useful": "证明不存在冷启动引导弹窗，从而把'诱导'归因到外部渠道而非应用内 UI",
        "observable_utg_signals": ["无任何应用内文本节点", "返回桌面后应用图标/快捷方式消失", "无 AlertDialog 类窗口"]
      },
      {
        "page_role": "获权后的前台目标应用页（验证采集行为）",
        "page_identifier": "任意含输入框/聊天内容的应用界面，配合日志标签 'Nine Text' 与 'NINE' 出现",
        "why_most_useful": "确认服务真正在读取窗口文本并归集，闭合'获权→窃取'链路",
        "observable_utg_signals": ["logcat 出现 'Nine Text' 与包名", "logcat 出现 'NINE' accessibilityEnabled=1", "Dname 数据库写入增长"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：(1) 诱导话术完全在包外的投放渠道，纯 APK 运行期 UTG 无法捕获'引导'环节，只能捕获系统无障碍列表项的伪装名称；(2) 应用冷启动后桌面图标被移除、且无任何界面，UTG 在应用侧几乎采不到页面，须以系统设置页与 logcat 作为主要观测面。本样本未加壳，静态可见性不受影响。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY"
  ],
  "code_anchors": [
    "com.system.android.updater.MainActivity.onCreate",
    "com.system.android.updater.MainActivity.removeShortcut",
    "com.system.android.updater.nine.ninere.onAccessibilityEvent",
    "com.system.android.updater.nine.ninere.addnew",
    "com.system.android.updater.nine.nine.isAccessibilitySettingsOn",
    "res/xml/accessibility.xml"
  ]
}
```

</details>
