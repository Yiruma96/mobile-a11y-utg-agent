# MR_161__6eae6ac151｜Monokle — UzbekChat

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：98.2s

## 1. 一句话核心结论

- **核心申请方式**：该应用不向用户做任何无障碍引导，而是用 Xposed 钩子篡改 enabled_accessibility_services 的读取返回值自授权 AccessService，静默获得全设备键盘记录能力。
- **静态可见性说明**：无障碍相关全部逻辑位于明文 DEX 的 com.system.security_update.xposed.keylogger 包（共 269 个类，无加壳、无加密载荷），Manifest、AccessService、Xposed 钩子与主界面代码均完整静态可见；不存在远端 HTML 或二阶段载荷承担该逻辑。唯一运行期依赖是设备需已 root 并具备 Xposed 框架。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6eae6ac151c5366b3d001382775192e98a4ed118050d8435b00cd35f01ad4b22` |
| 包名 / 年份 | `com.wUzbekChat1` / 2019 |
| 家族 / 品类 | **Monokle**（同池样本数：25） |
| 原始来源标识 | https://www.lookout.com/documents/threat-reports/lookout-discovers-monokle-threat-report.pdf |
| 桌面显示名 | UzbekChat |
| 引导页宣称品牌/身份 | Telegram（重打包的 org.telegram.messenger 客户端，Telegram Messenger LLP 品牌） |
| 系统无障碍列表服务名 | 无（服务未在 Manifest 声明，系统无障碍列表不显示任何条目） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无空白/换行挤出警告、无同形字、无 activity-alias；主要手法是「隐藏」而非「伪装」：无障碍服务不写入 Manifest，改由 Xposed 钩子伪造系统设置读取结果，使设置页无条目可查；恶意模块使用 com.system.security_update（伪装成系统安全更新）与 com.smartagents.system_service 等系统化命名，并配套 com.system.security_update.xposed.HideApp.ActivityHider 做界面隐藏 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | org.telegram.ui.LaunchActivity（MAIN/LAUNCHER）→ 恶意模块 com.system.security_update.MainActivity | 用户点击桌面图标，Activity.onCreate | 原生Activity | **原文**：无（activity_main 布局仅含两个 Button，第三个按钮 setVisibility(8) 被隐藏）<br>**译注**：无引导文案，界面只有按钮，无任何无障碍相关说明 | 无特定要求，可直接点击按钮继续 | `com.system.security_update.MainActivity.onCreate` |
| 2 | 业务功能触发 | 系统运行时权限对话框（ActivityCompat.requestPermissions，requestCode=101） | onCreate 中 Build.VERSION.SDK_INT >= 23 且非 root 时调用 RequestUserPermissions() | 原生Activity | **原文**：无（使用系统原生权限弹窗，样本未提供自定义文案）<br>**译注**：系统原生权限弹窗，一次性索要 16 项高危权限：RECEIVE_SMS/READ_SMS/SEND_SMS/READ_CALENDAR/CAMERA/READ_CONTACTS/ACCESS_FINE_LOCATION/RECORD_AUDIO/READ+WRITE_EXTERNAL_STORAGE/READ_PHONE_STATE/WRITE_CALL_LOG/GET_ACCOUNTS/READ_CALL_LOG/ACCESS_NOTIFICATION_POLICY | 点击「允许」；不含无障碍权限，因此这一步与无障碍引导无关 | `com.system.security_update.MainActivity.RequestUserPermissions` |
| 3 | 获权后动作 | com.system.security_update.BackgroundService（导出服务，permission=com.system.security_update.permission.SERVICE） | MainActivity$1.onClick 中 startService(new Intent(this, BackgroundService.class)) | 不可静态还原 | 无 | 无（用户看不到任何提示） | `com.system.security_update.MainActivity$1.onClick` |
| 4 | 获权后动作 | Xposed 钩子：AccessibilityManager.onAccessibilityEvent 与 Settings 读取方法 | XposedEntryPoint 加载后执行 KeyLogger.hookAccessibility0 注册钩子 | 不可静态还原 | **原文**：enabled_accessibility_services<br>**译注**：钩子匹配系统读取「已启用无障碍服务」的键名，随即把返回值替换为自身组件 | 无任何用户操作；用户从未进入无障碍设置页，也未勾选任何开关 | `com.system.security_update.xposed.keylogger.KeyLogger$11.afterHookedMethod` |
| 5 | 获权后动作 | com.system.security_update.xposed.keylogger.AccessService（AccessibilityService 实例） | onServiceConnected / onAccessibilityEvent 回调 | 不可静态还原 | **原文**：com.system.security_update.xposed.ontextchanged<br>**译注**：按前台包名归类记录 TYPE_VIEW_TEXT_CHANGED 输入文本与窗口状态变化，通过广播与缓冲外发 | 无 | `com.system.security_update.xposed.keylogger.AccessService.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 不存在任何无障碍引导/说明文字：样本内无 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 跳转代码，无引导弹窗、无教学 WebView、无悬浮遮罩
- 系统无障碍列表无条目可显示：Manifest 未声明 BIND_ACCESSIBILITY_SERVICE 服务，故无 android:label / android:description 呈现
- 唯一可见的用户交互文案来自系统原生运行时权限弹窗（16 项权限批量申请），由 ActivityCompat.requestPermissions 触发，样本未自定义任何说明
- MainActivity 界面仅 activity_main 布局的两个按钮（第三个按钮 setVisibility(8) 隐藏），无解释性文本
- 恶意模块的说明性字符串仅出现在 XposedLog 日志（如 enabled_accessibility_services、readComponentNamesFromSettingLocked），不面向用户展示
- 预筛列出的 Google Play services 提示串来自 com.google.android.gms 标准资源，与无障碍无关

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | enabled_accessibility_services | 已启用的无障碍服务（系统设置键名，钩子据此拦截并伪造返回值） | `com.system.security_update.xposed.keylogger.KeyLogger$11.afterHookedMethod / KeyLogger$10.afterHookedMethod` | 未知 |
| en | readComponentNamesFromSettingLocked | 从设置中读取组件名（加锁）——被挂钩的系统方法名，日志输出 | `com.system.security_update.xposed.keylogger.KeyLogger$11.afterHookedMethod` | 未知 |
| en | com.system.security_update.xposed.ontextchanged | 自定义广播：输入文本已变化（键盘记录数据外发通道） | `com.system.security_update.xposed.keylogger.AccessService.ONTEXTCHANGED_BROADCAST_FILTER` | 未知 |
| en | AnalyticsQ | 分析服务 Q（com.cuebiq.cuebiqsdk.model.Collector 的服务标签，用于弱化感知） | `AndroidManifest.xml service com.cuebiq.cuebiqsdk.model.Collector android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无。不存在跳转系统设置的动作，因此也不存在拒绝或返回后的重跳循环；无障碍能力由 Xposed 钩子直接伪造授权获得，用户无拒绝入口
- **遮罩叠层 / 高仿系统设置页**：无遮罩、无悬浮引导窗、无高仿系统无障碍开关页；取而代之的是让系统设置「看起来没有该服务」——KeyLogger$11 篡改 enabled_accessibility_services 读取结果，使真实条目对设置界面不可见
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：用户无法在设置中撤权，因为服务未在 Manifest 声明且系统读取结果被钩子替换；此外 com.system.security_update.xposed.HideApp.ActivityHider 与 LockScreenCtrl 提供界面隐藏与锁屏控制能力，进一步压制用户排查与卸载
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本无跳转点可钩，纯 UTG 应按「冷启动即采集」策略拉起：启动应用后 0–3 秒内连续截取 MainActivity 与系统运行时权限弹窗；并在任意应用内键盘输入时采集屏幕，重点比对「无障碍能力生效但系统设置中无对应条目」的矛盾，同时 hook 或监测 com.system.security_update 进程/模块加载与 com.system.security_update.xposed.ontextchanged 广播。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：本样本完全不使用页面引导，UTG 若只在页面流转中查找无障碍引导文案会完全空检；且恶意无障碍服务不写入 Manifest，系统设置中无条目可截。另需注意设备须 root + Xposed 才可复现自授权行为，普通环境运行只能看到壳层 Telegram 与批量权限申请，极易误判为良性。静态无加壳，不影响运行期 UTG 取证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动主界面（恶意模块入口）** | com.system.security_update.MainActivity，activity_main 布局，两个可点按钮 + 一个隐藏按钮 | 这是恶意模块唯一自研 UI，确认外壳与载荷的分离，以及无障碍引导的「缺席」本身即为关键证据 | 界面无任何无障碍说明文案或引导控件；按钮文本与 Telegram 品牌不一致；点击后无跳转设置页行为 |
| **系统运行时权限批量弹窗** | 系统权限对话框，requestCode=101，含短信/通话记录/相机/录音/联系人等 16 项 | 证明该样本的授权策略是一次性批量索要高危权限，而非分步无障碍教学，可与预筛的权限共现清单对齐 | 同一弹窗链连续索要短信与通话记录权限；弹窗中不含无障碍权限项 |
| **系统无障碍服务列表（预期为空）** | Settings → Accessibility → 已下载/已安装服务列表 | 捕获到「列表中无 UzbekChat/无 com.system.security_update 条目」而键盘输入仍被记录，即为 Xposed 自授权的决定性运行期佐证 | 列表无本应用条目；对比输入后 ontextchanged 广播仍触发 |
| **任意第三方应用输入界面（记录验证）** | 聊天/浏览器/银行类应用的输入框页面 | 验证获权后动作：AccessService 是否按前台包名缓存 TYPE_VIEW_TEXT_CHANGED 文本 | 输入内容被记录；前台包名变化被跟踪；无任何可见 UI 反馈 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.system.security_update.xposed.keylogger.KeyLogger.hookAccessibility0`
- `com.system.security_update.xposed.keylogger.KeyLogger$11.afterHookedMethod`
- `com.system.security_update.xposed.keylogger.AccessService.onAccessibilityEvent`
- `com.system.security_update.MainActivity.onCreate`
- `com.system.security_update.MainActivity.RequestUserPermissions`
- `com.system.security_update.MainActivity$1.onClick`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**该应用不存在“引导用户开启无障碍权限”的任何界面流程。** 无障碍权限通过 Xposed 钩子在运行期静默伪造，不经过用户授权。

1. **Manifest 未声明无障碍服务**：`<application>` 全段没有任何 `BIND_ACCESSIBILITY_SERVICE` 声明或 `accessibilityservice` 意图过滤，与预筛 `无障碍服务类=[]` 一致。因此，系统设置的无障碍列表中不会出现本应用条目，也不存在 `android:description` 引导文案。
2. **无障碍类真实存在且属于间谍模块**：[AccessService](<resource-unit:#1.dex1 code:com.system.security_update.xposed.keylogger.AccessService#onAccessibilityEvent>) 继承 `AccessibilityService`，持有按包名分组的输入缓冲 `sAppToAccessBuffer` / `sAppToOntextchangeBuffer`、前台包名 `sForegroundPackage`，并实现 `getEventText`、`getCurrentStack`、`getForegroundPackage`，以及广播 `com.system.security_update.xposed.ontextchanged`。
3. **无障碍权限的获得方式是“自授权”**：[KeyLogger$11.afterHookedMethod](<resource-unit:#1.dex1 code:com.system.security_update.xposed.keylogger.KeyLogger$11#afterHookedMethod>) 在 `setting.contentEquals("enabled_accessibility_services")` 成立时，把 `ComponentName.unflattenFromString("com.system.security_update")` 写入 `param.args[2]`，直接替换系统对“已启用无障碍服务”的读取结果；钩子由 [KeyLogger.hookAccessibility0](<resource-unit:#1.dex1 code:com.system.security_update.xposed.keylogger.KeyLogger#hookAccessibility0>) 注册（`XposedHelpers.findAndHookMethod(accessibilityManager, "onAccessibilityEvent", ...)`）。
4. **没有跳转、没有引导**：对 `ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`isAccessibilityTool`、`openAccessibility` 的全文检索全部零命中。唯一的自研界面 [MainActivity.onCreate](<resource-unit:#1.dex1 code:com.system.security_update.MainActivity#onCreate>) 只做两件事：在冷启动时一次性批量申请 16 项运行时权限（短信、通话记录、相机、录音、联系人、存储等，**不含无障碍**），以及绑定按钮以启动 `BackgroundService`。
5. **外壳身份**：应用主体是重打包的 Telegram 客户端（`org.telegram.messenger.ApplicationLoader_`，显示名 `UzbekChat`），恶意模块 `com.system.security_update` 共 269 个明文类，含 `keylogger`、`HideApp`、`root`、`location`、`connect` 等子包，配合开机自启、屏幕、去电、SIM 变更等广播接收器持久化。静态可见性为 clear，无加壳。
6. **对 UTG 的含义**：仅靠页面流转取证会**完全空检**——不存在引导弹窗、教学页、遮罩或系统无障碍列表项。可判别的信号是“无障碍能力实际生效，却从未出现授权跳转”这一矛盾，以及 `com.system.security_update` 模块的存在。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍相关全部逻辑位于明文 DEX 的 com.system.security_update.xposed.keylogger 包（共 269 个类，无加壳、无加密载荷），Manifest、AccessService、Xposed 钩子与主界面代码均完整静态可见；不存在远端 HTML 或二阶段载荷承担该逻辑。唯一运行期依赖是设备需已 root 并具备 Xposed 框架。",
  "summary_one_liner": "该应用不向用户做任何无障碍引导，而是用 Xposed 钩子篡改 enabled_accessibility_services 的读取返回值自授权 AccessService，静默获得全设备键盘记录能力。",
  "disguise_identity": {
    "app_display_name": "UzbekChat",
    "claimed_brand_or_persona": "Telegram（重打包的 org.telegram.messenger 客户端，Telegram Messenger LLP 品牌）",
    "a11y_service_label": "无（服务未在 Manifest 声明，系统无障碍列表不显示任何条目）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无空白/换行挤出警告、无同形字、无 activity-alias；主要手法是「隐藏」而非「伪装」：无障碍服务不写入 Manifest，改由 Xposed 钩子伪造系统设置读取结果，使设置页无条目可查；恶意模块使用 com.system.security_update（伪装成系统安全更新）与 com.smartagents.system_service 等系统化命名，并配套 com.system.security_update.xposed.HideApp.ActivityHider 做界面隐藏"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "org.telegram.ui.LaunchActivity（MAIN/LAUNCHER）→ 恶意模块 com.system.security_update.MainActivity",
      "trigger_event": "用户点击桌面图标，Activity.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（activity_main 布局仅含两个 Button，第三个按钮 setVisibility(8) 被隐藏）",
      "shown_text_zh": "无引导文案，界面只有按钮，无任何无障碍相关说明",
      "user_action_requested": "无特定要求，可直接点击按钮继续",
      "code_anchor": "com.system.security_update.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "系统运行时权限对话框（ActivityCompat.requestPermissions，requestCode=101）",
      "trigger_event": "onCreate 中 Build.VERSION.SDK_INT >= 23 且非 root 时调用 RequestUserPermissions()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（使用系统原生权限弹窗，样本未提供自定义文案）",
      "shown_text_zh": "系统原生权限弹窗，一次性索要 16 项高危权限：RECEIVE_SMS/READ_SMS/SEND_SMS/READ_CALENDAR/CAMERA/READ_CONTACTS/ACCESS_FINE_LOCATION/RECORD_AUDIO/READ+WRITE_EXTERNAL_STORAGE/READ_PHONE_STATE/WRITE_CALL_LOG/GET_ACCOUNTS/READ_CALL_LOG/ACCESS_NOTIFICATION_POLICY",
      "user_action_requested": "点击「允许」；不含无障碍权限，因此这一步与无障碍引导无关",
      "code_anchor": "com.system.security_update.MainActivity.RequestUserPermissions"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "com.system.security_update.BackgroundService（导出服务，permission=com.system.security_update.permission.SERVICE）",
      "trigger_event": "MainActivity$1.onClick 中 startService(new Intent(this, BackgroundService.class))",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，静默启动后台服务承载远控与窃密通道",
      "user_action_requested": "无（用户看不到任何提示）",
      "code_anchor": "com.system.security_update.MainActivity$1.onClick"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "Xposed 钩子：AccessibilityManager.onAccessibilityEvent 与 Settings 读取方法",
      "trigger_event": "XposedEntryPoint 加载后执行 KeyLogger.hookAccessibility0 注册钩子",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "enabled_accessibility_services",
      "shown_text_zh": "钩子匹配系统读取「已启用无障碍服务」的键名，随即把返回值替换为自身组件",
      "user_action_requested": "无任何用户操作；用户从未进入无障碍设置页，也未勾选任何开关",
      "code_anchor": "com.system.security_update.xposed.keylogger.KeyLogger$11.afterHookedMethod"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.system.security_update.xposed.keylogger.AccessService（AccessibilityService 实例）",
      "trigger_event": "onServiceConnected / onAccessibilityEvent 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "com.system.security_update.xposed.ontextchanged",
      "shown_text_zh": "按前台包名归类记录 TYPE_VIEW_TEXT_CHANGED 输入文本与窗口状态变化，通过广播与缓冲外发",
      "user_action_requested": "无",
      "code_anchor": "com.system.security_update.xposed.keylogger.AccessService.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "不存在任何无障碍引导/说明文字：样本内无 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 跳转代码，无引导弹窗、无教学 WebView、无悬浮遮罩",
    "系统无障碍列表无条目可显示：Manifest 未声明 BIND_ACCESSIBILITY_SERVICE 服务，故无 android:label / android:description 呈现",
    "唯一可见的用户交互文案来自系统原生运行时权限弹窗（16 项权限批量申请），由 ActivityCompat.requestPermissions 触发，样本未自定义任何说明",
    "MainActivity 界面仅 activity_main 布局的两个按钮（第三个按钮 setVisibility(8) 隐藏），无解释性文本",
    "恶意模块的说明性字符串仅出现在 XposedLog 日志（如 enabled_accessibility_services、readComponentNamesFromSettingLocked），不面向用户展示",
    "预筛列出的 Google Play services 提示串来自 com.google.android.gms 标准资源，与无障碍无关"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "enabled_accessibility_services",
      "text_zh": "已启用的无障碍服务（系统设置键名，钩子据此拦截并伪造返回值）",
      "source_location": "com.system.security_update.xposed.keylogger.KeyLogger$11.afterHookedMethod / KeyLogger$10.afterHookedMethod",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "readComponentNamesFromSettingLocked",
      "text_zh": "从设置中读取组件名（加锁）——被挂钩的系统方法名，日志输出",
      "source_location": "com.system.security_update.xposed.keylogger.KeyLogger$11.afterHookedMethod",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "com.system.security_update.xposed.ontextchanged",
      "text_zh": "自定义广播：输入文本已变化（键盘记录数据外发通道）",
      "source_location": "com.system.security_update.xposed.keylogger.AccessService.ONTEXTCHANGED_BROADCAST_FILTER",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "AnalyticsQ",
      "text_zh": "分析服务 Q（com.cuebiq.cuebiqsdk.model.Collector 的服务标签，用于弱化感知）",
      "source_location": "AndroidManifest.xml service com.cuebiq.cuebiqsdk.model.Collector android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无。不存在跳转系统设置的动作，因此也不存在拒绝或返回后的重跳循环；无障碍能力由 Xposed 钩子直接伪造授权获得，用户无拒绝入口",
    "overlay_or_fake_settings": "无遮罩、无悬浮引导窗、无高仿系统无障碍开关页；取而代之的是让系统设置「看起来没有该服务」——KeyLogger$11 篡改 enabled_accessibility_services 读取结果，使真实条目对设置界面不可见",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "用户无法在设置中撤权，因为服务未在 Manifest 声明且系统读取结果被钩子替换；此外 com.system.security_update.xposed.HideApp.ActivityHider 与 LockScreenCtrl 提供界面隐藏与锁屏控制能力，进一步压制用户排查与卸载",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本无跳转点可钩，纯 UTG 应按「冷启动即采集」策略拉起：启动应用后 0–3 秒内连续截取 MainActivity 与系统运行时权限弹窗；并在任意应用内键盘输入时采集屏幕，重点比对「无障碍能力生效但系统设置中无对应条目」的矛盾，同时 hook 或监测 com.system.security_update 进程/模块加载与 com.system.security_update.xposed.ontextchanged 广播。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动主界面（恶意模块入口）",
        "page_identifier": "com.system.security_update.MainActivity，activity_main 布局，两个可点按钮 + 一个隐藏按钮",
        "why_most_useful": "这是恶意模块唯一自研 UI，确认外壳与载荷的分离，以及无障碍引导的「缺席」本身即为关键证据",
        "observable_utg_signals": ["界面无任何无障碍说明文案或引导控件", "按钮文本与 Telegram 品牌不一致", "点击后无跳转设置页行为"]
      },
      {
        "page_role": "系统运行时权限批量弹窗",
        "page_identifier": "系统权限对话框，requestCode=101，含短信/通话记录/相机/录音/联系人等 16 项",
        "why_most_useful": "证明该样本的授权策略是一次性批量索要高危权限，而非分步无障碍教学，可与预筛的权限共现清单对齐",
        "observable_utg_signals": ["同一弹窗链连续索要短信与通话记录权限", "弹窗中不含无障碍权限项"]
      },
      {
        "page_role": "系统无障碍服务列表（预期为空）",
        "page_identifier": "Settings → Accessibility → 已下载/已安装服务列表",
        "why_most_useful": "捕获到「列表中无 UzbekChat/无 com.system.security_update 条目」而键盘输入仍被记录，即为 Xposed 自授权的决定性运行期佐证",
        "observable_utg_signals": ["列表无本应用条目", "对比输入后 ontextchanged 广播仍触发"]
      },
      {
        "page_role": "任意第三方应用输入界面（记录验证）",
        "page_identifier": "聊天/浏览器/银行类应用的输入框页面",
        "why_most_useful": "验证获权后动作：AccessService 是否按前台包名缓存 TYPE_VIEW_TEXT_CHANGED 文本",
        "observable_utg_signals": ["输入内容被记录", "前台包名变化被跟踪", "无任何可见 UI 反馈"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：本样本完全不使用页面引导，UTG 若只在页面流转中查找无障碍引导文案会完全空检；且恶意无障碍服务不写入 Manifest，系统设置中无条目可截。另需注意设备须 root + Xposed 才可复现自授权行为，普通环境运行只能看到壳层 Telegram 与批量权限申请，极易误判为良性。静态无加壳，不影响运行期 UTG 取证。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "com.system.security_update.xposed.keylogger.KeyLogger.hookAccessibility0",
    "com.system.security_update.xposed.keylogger.KeyLogger$11.afterHookedMethod",
    "com.system.security_update.xposed.keylogger.AccessService.onAccessibilityEvent",
    "com.system.security_update.MainActivity.onCreate",
    "com.system.security_update.MainActivity.RequestUserPermissions",
    "com.system.security_update.MainActivity$1.onClick"
  ]
}
```

</details>
