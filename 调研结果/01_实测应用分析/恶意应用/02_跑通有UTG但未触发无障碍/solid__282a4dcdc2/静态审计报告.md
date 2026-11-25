# MR_095__282a4dcdc2｜solid — Dr. Security

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：237.3s

## 1. 一句话核心结论

- **核心申请方式**：以“电池优化/防应用重启”为名，在权限引导列表与省电页原生弹窗两处入口跳转系统无障碍设置，1 秒后压栈文字引导页，并在服务描述中明示“可忽略隐私警告”，获权后借无障碍在系统应用详情页自动点击“强行停止/确定”以抗撤销。
- **静态可见性说明**：无障碍引导链（权限列表点击、省电页原生Dialog、ACTION_ACCESSIBILITY_SETTINGS跳转、延时压栈AccessibilityDialogActivity、系统无障碍描述、获权后设置页自动点击）全部位于 classes.dex 的 Java 实现与本地 res/values/strings.xml、res/xml/top_accessbility.xml 中，无加壳、无 AES 载荷、无远端 HTML 下发；仅 assets/privacy.html 与 terms.html 为本地静态 Google Docs 导出页，与无障碍引导无关。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `282a4dcdc285324befe001e4dbf791cfce76eeea190d1a1dc68425ce9ea2aee9` |
| 包名 / 年份 | `com.clean.antivirus.security` / 2018 |
| 家族 / 品类 | **solid**（同池样本数：60） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/18/a/apps-disguised-security-tools-bombard-users-ads-track-users-location.html |
| 桌面显示名 | Dr. Security |
| 引导页宣称品牌/身份 | Dr. Security（自称设备优化/电池管家与安全工具，冒充系统级优化组件） |
| 系统无障碍列表服务名 | Dr. Security |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务描述文本中直接写入“You can have the privacy warning ignored.”，主动劝用户忽略系统隐私警告；服务类命名为 BatteryOptimizeService（电池优化），而实际能力为 flagReportViewIds + canRetrieveWindowContent + 自动点击；入口分散在权限引导列表项与省电页弹窗两处，降低单点可见性；代码层使用 ns.pa / ns.qf 等短包名混淆。 |
| 无障碍服务类名 | `com.anti.security.service.BatteryOptimizeService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability.Dr. Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>    You can have the privacy warning ignored. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.anti.security.activity.GrantPermissonsActivity（权限引导列表页） | 列表项 onClick：图标 id 2130837588 且 BatteryOptimizeService.a() 返回 false（无障碍未启用） | 原生Activity | **原文**：Please find and enalbe Dr. Security for system optimization and phone security.<br>**译注**：请找到并启用 Dr. Security 以进行系统优化和手机安全保护。 | 点击“无障碍”条目即被直接跳转到系统无障碍设置（无二次确认） | `com.anti.security.activity.GrantPermissonsActivity$4#onClick → ns.pa#a(android.app.Activity,int)；文案 res/values/strings.xml#accessibility_desc` |
| 2 | 引导说明页 | ns.qf（原生 Dialog，布局 dialog_battery_accessibility_layout） | BatterySaverSelectActivity.onCreate 中 new qf(this) 并在用户点优化/省电时 show() | 原生Dialog | **原文**：Dr. Security use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%.<br>**译注**：Dr. Security 使用无障碍功能帮你停止不必要的应用，可将电池续航与手机性能提升 50% 以上。 | 点击弹窗中的启用按钮（qf$2 → onEnable），另一按钮（qf$1）可关闭弹窗 | `ns.qf#onCreate；com.anti.security.activity.BatterySaverSelectActivity#onCreate；res/values/strings.xml#battery_permission_desc` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | BatterySaverSelectActivity.onEnable() / GrantPermissonsActivity$4.onClick 调用 ns.pa.a(activity, code)，内部 startActivityForResult | 系统无障碍页 | 无 | 在系统列表中手动找到 “Dr. Security” 并打开开关（系统页操作，应用无按钮控制） | `ns.pa#a(android.app.Activity,int)（new Intent("android.settings.ACCESSIBILITY_SETTINGS")）` |
| 4 | 遮罩叠层指引 | com.anti.security.activity.AccessibilityDialogActivity（压在系统设置页之上的文字指引页） | onEnable 内 mHandler.postDelayed(BatterySaverSelectActivity$8, 1000L) → showAccessibilityToast() → startActivity(AccessibilityDialogActivity)，onCreate 将 Intent.content 写入 TextView | 原生Activity | **原文**：To prevent apps from restarting and save battery power, please find and enable Dr. Security.<br>**译注**：为防止应用自动重启并节省电量，请找到并启用 Dr. Security。 | 按提示在系统无障碍列表中定位并启用 Dr. Security（该页本身无启用/跳过按钮） | `com.anti.security.activity.BatterySaverSelectActivity#showAccessibilityToast；com.anti.security.activity.AccessibilityDialogActivity#onCreate；res/values/strings.xml#accessibility_toast_text` |
| 5 | 引导说明页 | 系统无障碍列表条目说明（android:description） | 用户在系统无障碍列表中点击服务条目查看说明 | 系统无障碍页 | **原文**：Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability.Dr. Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe. You can have the privacy warning ignored.<br>**译注**：无障碍可阻止不需要的应用重新打开，还能延长电池寿命与耐用度。Dr. Security 仅用于优化设备功能，我们保证你的隐私与个人数据完全安全。你可以忽略隐私警告。 | 确认开启（描述中直接教唆忽略系统隐私警告） | `res/xml/top_accessbility.xml（@string/boost_tag_acc_kill_service_description）；res/values/strings.xml 第 157 行` |
| 6 | 获权后动作 | com.anti.security.service.BatteryOptimizeService（无障碍服务 onAccessibilityEvent） | 服务启用后收到 com.android.settings 的 TYPE_WINDOW_STATE_CHANGED 事件（含 InstalledAppDetailsTop / InstalledAppDetailsActivity） | 系统无障碍页 | **原文**：无（通过 createPackageContext("com.android.settings",3) 反射读取系统字符串 force_stop / dlg_ok / yes，小米为 finish_application）<br>**译注**：自动匹配系统“强行停止”“确定”按钮并 performAction(ACTION_CLICK) 代用户点击，阻止用户停用应用 | 无需用户操作——服务代替用户点击系统确认弹窗 | `com.anti.security.service.BatteryOptimizeService#onCreate / #onAccessibilityEvent / #a(android.view.accessibility.AccessibilityEvent)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 权限引导列表页 GrantPermissonsActivity 的“无障碍”条目（点击即跳设置，无中间说明页）
- BatterySaverSelectActivity 上的原生 Dialog（ns.qf / dialog_battery_accessibility_layout），文案取 strings.xml#battery_permission_desc
- 跳转系统设置后 1 秒压栈的 AccessibilityDialogActivity，文案取 strings.xml#accessibility_toast_text（经 Intent extra "content" 注入 TextView）
- 系统无障碍服务列表条目名 “Dr. Security” 与说明 android:description = boost_tag_acc_kill_service_description
- strings.xml#accessibility_desc 作为定位/提示文案
- 悬浮窗权限引导 Dialog（ns.pi，跳 ACTION_MANAGE_OVERLAY_PERMISSION），为无障碍前置的叠加层权限铺垫

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability.Dr. Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe. You can have the privacy warning ignored. | 无障碍可阻止不需要的应用重新打开，还能延长电池寿命与耐用度。Dr. Security 仅用于优化设备功能，我们保证你的隐私与个人数据完全安全。你可以忽略隐私警告。 | `res/values/strings.xml key=boost_tag_acc_kill_service_description（被 res/xml/top_accessbility.xml 引用）` | 教唆忽视警告 |
| en | Please find and enalbe Dr. Security for system optimization and phone security. | 请找到并启用 Dr. Security，用于系统优化与手机安全保护。 | `res/values/strings.xml key=accessibility_desc` | 清理工具伪装 |
| en | To prevent apps from restarting and save battery power, please find and enable Dr. Security. | 为防止应用自动重启并节省电量，请找到并启用 Dr. Security。 | `res/values/strings.xml key=accessibility_toast_text（用于 AccessibilityDialogActivity）` | 假反诈安全 |
| en | Dr. Security use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%. | Dr. Security 使用无障碍功能帮你停止不必要的应用，可将电池续航与手机性能提升 50% 以上。 | `res/values/strings.xml key=battery_permission_desc（ns.qf 弹窗）` | 清理工具伪装 |
| en | Accessibility | 无障碍 | `res/values/strings.xml key=acessibility` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：非强制死循环：从系统设置返回后 GrantPermissonsActivity.onResume 仅 updateData() 刷新列表，无障碍项仍显示未启用，用户可再次点击；但每次点击都会再次跳转设置并在 1 秒后压栈 AccessibilityDialogActivity 指引页（postDelayed 1000ms），形成反复拉起的引导压力。BatterySaverSelectActivity.onResume 亦仅清空 Handler 回调。
- **遮罩叠层 / 高仿系统设置页**：不使用全屏悬浮窗伪装系统开关；但通过延时 1 秒 startActivity(AccessibilityDialogActivity) 在系统无障碍设置页之上压入文字指引页（视觉上与设置页交替出现），并另有 ns.pi 原生 Dialog 先行索要悬浮窗权限（ACTION_MANAGE_OVERLAY_PERMISSION）作为前置铺垫。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：有：BatteryOptimizeService 获权后，onCreate 反射读取 com.android.settings 的 force_stop / dlg_ok / yes（小米 finish_application）等按钮文案；onAccessibilityEvent 针对 com.android.settings 的 InstalledAppDetailsTop / InstalledAppDetailsActivity 及普通设置页，用 findAccessibilityNodeInfosByText 匹配按钮文本并 performAction(ACTION_CLICK)，a(AccessibilityEvent) 进一步对 android.widget.Button 节点强制点击，代用户确认“强行停止/确定”，阻断用户停用与撤权操作。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以无障碍权限引导为目标时，最佳 UTG 拉起点为：①监测到 GrantPermissonsActivity 列表“无障碍”条目点击或 BatterySaverSelectActivity 弹窗启用按钮点击后的 startActivityForResult(ACTION_ACCESSIBILITY_SETTINGS)；②紧随其后 1000ms 内 AccessibilityDialogActivity 压栈瞬间（此时可同时抓到设置页与压栈指引页两层）。冷启动直弹引导弹窗场景不存在，需先进入权限/省电页面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导文案全部为可提取文本，无图片化诱导；但需注意 ①两个入口均位于二级页面（权限引导列表、电池省电页），冷启动首屏不弹窗，若仅截首屏会漏检；②AccessibilityDialogActivity 在系统设置页之上压栈，UTG 抓取需以当前 top activity 而非应用包名判定；③获权后的自动点击发生在 com.android.settings 前台，需在系统设置页内做事件时序比对才能观测。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **省电页无障碍说明弹窗（原生 Dialog）** | com.anti.security.activity.BatterySaverSelectActivity 上的 ns.qf Dialog，布局 dialog_battery_accessibility_layout，含两枚 TextView 按钮（启用/关闭） | 这是应用唯一的“事前说明”环节，可直接比较其声称的电池优化目的与实际申请的高危无障碍能力是否匹配 | 弹窗文本包含 “accessibility” + “battery”/“50%” 组合；按钮数量为 2 且无隐私政策或权限范围说明；点击后 1 秒内 Activity 切换为系统设置页 |
| **跳转后压栈的引导页** | com.anti.security.activity.AccessibilityDialogActivity（theme NoActionBar，文字来自 Intent extra content） | 证明应用在用户离开自身界面进入系统设置后仍主动叠层指引，属于跨界面持续引导的关键证据 | 包名仍为 com.clean.antivirus.security 但内容为纯指引文字；页面无启用开关，仅要求“find and enable Dr. Security”；出现时刻与 ACCESSIBILITY_SETTINGS 跳转相差约 1000ms |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载服务中的 “Dr. Security” 条目 | 核对服务显示名与桌面名是否一致、description 是否包含忽略隐私警告话术 | 服务名 “Dr. Security”；描述文本含 “You can have the privacy warning ignored”；开关默认关闭且无系统二次确认（targetSdk 22） |
| **获权后系统应用详情页自动点击现场** | com.android.settings 的 InstalledAppDetailsTop / InstalledAppDetailsActivity 页面（点击“强行停止”后的确认弹窗） | 验证抗撤销行为：确认弹窗被无障碍自动点击，用户无法完成停用 | 确认弹窗出现后极短时间内自动消失；无用户触摸事件但按钮被触发；日志/事件中出现 com.anti.security.security 对 settings 页的 TYPE_WINDOW_STATE_CHANGED 处理 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `ns.pa#a(android.app.Activity, int)`
- `com.anti.security.activity.GrantPermissonsActivity$4#onClick`
- `com.anti.security.activity.BatterySaverSelectActivity#onEnable`
- `com.anti.security.activity.BatterySaverSelectActivity#showAccessibilityToast`
- `com.anti.security.service.BatteryOptimizeService#onAccessibilityEvent`
- `res/xml/top_accessbility.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验完成）

**整体判断：静态完全可见，没有加壳，也没有远端 HTML 动态加载。** 无障碍权限引导全部由原生 Java 代码和本地 strings.xml 实现，可以完整还原整条运行期页面流转。

**逐步流转链（两个入口最终汇合到同一个跳转函数）：**

1. **入口 A：权限引导列表**：`GrantPermissonsActivity` 的列表项点击回调（`GrantPermissonsActivity$4.onClick`）发现 `BatteryOptimizeService.a()` 为 false（无障碍未启用），于是调用 `pa.a(this, ACCESS_REQUEST_CODE)`，并用 `postDelayed(1000ms)` 延迟弹出提示。
2. **入口 B：电池省电页弹窗**：`BatterySaverSelectActivity.onCreate` 构造原生 Dialog `qf`（布局 `dialog_battery_accessibility_layout`，文案 `battery_permission_desc`）；用户点击“启用”按钮（`qf$2`）后，`onEnable()` 同样调用 `pa.a(...)`，并延时 1 秒。
3. **跳受限设置**：`ns.pa.a(Activity,int)` 执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，直接跳转到系统无障碍列表。
4. **遮罩/压栈指引**：延时 1 秒后，`showAccessibilityToast()` 执行 `startActivity(AccessibilityDialogActivity)`，把 `Intent.content` 写入 TextView，压在系统设置页之上。该 Activity 主题未设透明，但 `excludeFromRecents` 类风格的单任务跳转使指引层与设置页交替出现。此外还有 `pi` 悬浮窗 Dialog 处理 `MANAGE_OVERLAY_PERMISSION` 跳转（先要求悬浮窗权限）。
5. **系统无障碍列表项**：`android:label` 为 “Dr. Security”，`android:description` 为 `boost_tag_acc_kill_service_description`，明文教用户“忽略隐私警告”。
6. **获权后动作**：`BatteryOptimizeService.onCreate` 用 `createPackageContext("com.android.settings",3)` 反射获取系统 `force_stop`/`dlg_ok`/`yes`（小米取 `finish_application`）文案；`onAccessibilityEvent` 只处理 `com.android.settings` 的 `TYPE_WINDOW_STATE_CHANGED`，在 `InstalledAppDetailsTop` 和普通设置页上 `findAccessibilityNodeInfosByText` + `performAction(16)` 自动点击“强行停止/确定”按钮。

**关键性质**：能力（读窗口内容 + 遍历控件 + 模拟点击）远超“电池优化/防重启”声称范围；文案主动劝用户忽略系统隐私警告；获权后可在系统设置页代用户确认，构成抗停用、抗卸载；**无** Android 13 受限设置分步教学（targetSdk 22，2018 年样本无此机制），**无** `isAccessibilityTool` 伪造。

**已登记风险**：R-001（high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链（权限列表点击、省电页原生Dialog、ACTION_ACCESSIBILITY_SETTINGS跳转、延时压栈AccessibilityDialogActivity、系统无障碍描述、获权后设置页自动点击）全部位于 classes.dex 的 Java 实现与本地 res/values/strings.xml、res/xml/top_accessbility.xml 中，无加壳、无 AES 载荷、无远端 HTML 下发；仅 assets/privacy.html 与 terms.html 为本地静态 Google Docs 导出页，与无障碍引导无关。",
  "summary_one_liner": "以“电池优化/防应用重启”为名，在权限引导列表与省电页原生弹窗两处入口跳转系统无障碍设置，1 秒后压栈文字引导页，并在服务描述中明示“可忽略隐私警告”，获权后借无障碍在系统应用详情页自动点击“强行停止/确定”以抗撤销。",
  "disguise_identity": {
    "app_display_name": "Dr. Security",
    "claimed_brand_or_persona": "Dr. Security（自称设备优化/电池管家与安全工具，冒充系统级优化组件）",
    "a11y_service_label": "Dr. Security",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务描述文本中直接写入“You can have the privacy warning ignored.”，主动劝用户忽略系统隐私警告；服务类命名为 BatteryOptimizeService（电池优化），而实际能力为 flagReportViewIds + canRetrieveWindowContent + 自动点击；入口分散在权限引导列表项与省电页弹窗两处，降低单点可见性；代码层使用 ns.pa / ns.qf 等短包名混淆。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.anti.security.activity.GrantPermissonsActivity（权限引导列表页）",
      "trigger_event": "列表项 onClick：图标 id 2130837588 且 BatteryOptimizeService.a() 返回 false（无障碍未启用）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please find and enalbe Dr. Security for system optimization and phone security.",
      "shown_text_zh": "请找到并启用 Dr. Security 以进行系统优化和手机安全保护。",
      "user_action_requested": "点击“无障碍”条目即被直接跳转到系统无障碍设置（无二次确认）",
      "code_anchor": "com.anti.security.activity.GrantPermissonsActivity$4#onClick → ns.pa#a(android.app.Activity,int)；文案 res/values/strings.xml#accessibility_desc"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "ns.qf（原生 Dialog，布局 dialog_battery_accessibility_layout）",
      "trigger_event": "BatterySaverSelectActivity.onCreate 中 new qf(this) 并在用户点优化/省电时 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Dr. Security use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%.",
      "shown_text_zh": "Dr. Security 使用无障碍功能帮你停止不必要的应用，可将电池续航与手机性能提升 50% 以上。",
      "user_action_requested": "点击弹窗中的启用按钮（qf$2 → onEnable），另一按钮（qf$1）可关闭弹窗",
      "code_anchor": "ns.qf#onCreate；com.anti.security.activity.BatterySaverSelectActivity#onCreate；res/values/strings.xml#battery_permission_desc"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "BatterySaverSelectActivity.onEnable() / GrantPermissonsActivity$4.onClick 调用 ns.pa.a(activity, code)，内部 startActivityForResult",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍服务列表，可见条目名 “Dr. Security” 及其描述文本",
      "user_action_requested": "在系统列表中手动找到 “Dr. Security” 并打开开关（系统页操作，应用无按钮控制）",
      "code_anchor": "ns.pa#a(android.app.Activity,int)（new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.anti.security.activity.AccessibilityDialogActivity（压在系统设置页之上的文字指引页）",
      "trigger_event": "onEnable 内 mHandler.postDelayed(BatterySaverSelectActivity$8, 1000L) → showAccessibilityToast() → startActivity(AccessibilityDialogActivity)，onCreate 将 Intent.content 写入 TextView",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "To prevent apps from restarting and save battery power, please find and enable Dr. Security.",
      "shown_text_zh": "为防止应用自动重启并节省电量，请找到并启用 Dr. Security。",
      "user_action_requested": "按提示在系统无障碍列表中定位并启用 Dr. Security（该页本身无启用/跳过按钮）",
      "code_anchor": "com.anti.security.activity.BatterySaverSelectActivity#showAccessibilityToast；com.anti.security.activity.AccessibilityDialogActivity#onCreate；res/values/strings.xml#accessibility_toast_text"
    },
    {
      "step": 5,
      "stage": "引导说明页",
      "screen_or_component": "系统无障碍列表条目说明（android:description）",
      "trigger_event": "用户在系统无障碍列表中点击服务条目查看说明",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability.Dr. Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe. You can have the privacy warning ignored.",
      "shown_text_zh": "无障碍可阻止不需要的应用重新打开，还能延长电池寿命与耐用度。Dr. Security 仅用于优化设备功能，我们保证你的隐私与个人数据完全安全。你可以忽略隐私警告。",
      "user_action_requested": "确认开启（描述中直接教唆忽略系统隐私警告）",
      "code_anchor": "res/xml/top_accessbility.xml（@string/boost_tag_acc_kill_service_description）；res/values/strings.xml 第 157 行"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.anti.security.service.BatteryOptimizeService（无障碍服务 onAccessibilityEvent）",
      "trigger_event": "服务启用后收到 com.android.settings 的 TYPE_WINDOW_STATE_CHANGED 事件（含 InstalledAppDetailsTop / InstalledAppDetailsActivity）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（通过 createPackageContext(\"com.android.settings\",3) 反射读取系统字符串 force_stop / dlg_ok / yes，小米为 finish_application）",
      "shown_text_zh": "自动匹配系统“强行停止”“确定”按钮并 performAction(ACTION_CLICK) 代用户点击，阻止用户停用应用",
      "user_action_requested": "无需用户操作——服务代替用户点击系统确认弹窗",
      "code_anchor": "com.anti.security.service.BatteryOptimizeService#onCreate / #onAccessibilityEvent / #a(android.view.accessibility.AccessibilityEvent)"
    }
  ],
  "text_presentation_locations": [
    "权限引导列表页 GrantPermissonsActivity 的“无障碍”条目（点击即跳设置，无中间说明页）",
    "BatterySaverSelectActivity 上的原生 Dialog（ns.qf / dialog_battery_accessibility_layout），文案取 strings.xml#battery_permission_desc",
    "跳转系统设置后 1 秒压栈的 AccessibilityDialogActivity，文案取 strings.xml#accessibility_toast_text（经 Intent extra \"content\" 注入 TextView）",
    "系统无障碍服务列表条目名 “Dr. Security” 与说明 android:description = boost_tag_acc_kill_service_description",
    "strings.xml#accessibility_desc 作为定位/提示文案",
    "悬浮窗权限引导 Dialog（ns.pi，跳 ACTION_MANAGE_OVERLAY_PERMISSION），为无障碍前置的叠加层权限铺垫"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability.Dr. Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe. You can have the privacy warning ignored.",
      "text_zh": "无障碍可阻止不需要的应用重新打开，还能延长电池寿命与耐用度。Dr. Security 仅用于优化设备功能，我们保证你的隐私与个人数据完全安全。你可以忽略隐私警告。",
      "source_location": "res/values/strings.xml key=boost_tag_acc_kill_service_description（被 res/xml/top_accessbility.xml 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Please find and enalbe Dr. Security for system optimization and phone security.",
      "text_zh": "请找到并启用 Dr. Security，用于系统优化与手机安全保护。",
      "source_location": "res/values/strings.xml key=accessibility_desc",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "To prevent apps from restarting and save battery power, please find and enable Dr. Security.",
      "text_zh": "为防止应用自动重启并节省电量，请找到并启用 Dr. Security。",
      "source_location": "res/values/strings.xml key=accessibility_toast_text（用于 AccessibilityDialogActivity）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Dr. Security use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%.",
      "text_zh": "Dr. Security 使用无障碍功能帮你停止不必要的应用，可将电池续航与手机性能提升 50% 以上。",
      "source_location": "res/values/strings.xml key=battery_permission_desc（ns.qf 弹窗）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility",
      "text_zh": "无障碍",
      "source_location": "res/values/strings.xml key=acessibility",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "非强制死循环：从系统设置返回后 GrantPermissonsActivity.onResume 仅 updateData() 刷新列表，无障碍项仍显示未启用，用户可再次点击；但每次点击都会再次跳转设置并在 1 秒后压栈 AccessibilityDialogActivity 指引页（postDelayed 1000ms），形成反复拉起的引导压力。BatterySaverSelectActivity.onResume 亦仅清空 Handler 回调。",
    "overlay_or_fake_settings": "不使用全屏悬浮窗伪装系统开关；但通过延时 1 秒 startActivity(AccessibilityDialogActivity) 在系统无障碍设置页之上压入文字指引页（视觉上与设置页交替出现），并另有 ns.pi 原生 Dialog 先行索要悬浮窗权限（ACTION_MANAGE_OVERLAY_PERMISSION）作为前置铺垫。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "有：BatteryOptimizeService 获权后，onCreate 反射读取 com.android.settings 的 force_stop / dlg_ok / yes（小米 finish_application）等按钮文案；onAccessibilityEvent 针对 com.android.settings 的 InstalledAppDetailsTop / InstalledAppDetailsActivity 及普通设置页，用 findAccessibilityNodeInfosByText 匹配按钮文本并 performAction(ACTION_CLICK)，a(AccessibilityEvent) 进一步对 android.widget.Button 节点强制点击，代用户确认“强行停止/确定”，阻断用户停用与撤权操作。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以无障碍权限引导为目标时，最佳 UTG 拉起点为：①监测到 GrantPermissonsActivity 列表“无障碍”条目点击或 BatterySaverSelectActivity 弹窗启用按钮点击后的 startActivityForResult(ACTION_ACCESSIBILITY_SETTINGS)；②紧随其后 1000ms 内 AccessibilityDialogActivity 压栈瞬间（此时可同时抓到设置页与压栈指引页两层）。冷启动直弹引导弹窗场景不存在，需先进入权限/省电页面。",
    "key_pages_to_capture": [
      {
        "page_role": "省电页无障碍说明弹窗（原生 Dialog）",
        "page_identifier": "com.anti.security.activity.BatterySaverSelectActivity 上的 ns.qf Dialog，布局 dialog_battery_accessibility_layout，含两枚 TextView 按钮（启用/关闭）",
        "why_most_useful": "这是应用唯一的“事前说明”环节，可直接比较其声称的电池优化目的与实际申请的高危无障碍能力是否匹配",
        "observable_utg_signals": ["弹窗文本包含 “accessibility” + “battery”/“50%” 组合", "按钮数量为 2 且无隐私政策或权限范围说明", "点击后 1 秒内 Activity 切换为系统设置页"]
      },
      {
        "page_role": "跳转后压栈的引导页",
        "page_identifier": "com.anti.security.activity.AccessibilityDialogActivity（theme NoActionBar，文字来自 Intent extra content）",
        "why_most_useful": "证明应用在用户离开自身界面进入系统设置后仍主动叠层指引，属于跨界面持续引导的关键证据",
        "observable_utg_signals": ["包名仍为 com.clean.antivirus.security 但内容为纯指引文字", "页面无启用开关，仅要求“find and enable Dr. Security”", "出现时刻与 ACCESSIBILITY_SETTINGS 跳转相差约 1000ms"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载服务中的 “Dr. Security” 条目",
        "why_most_useful": "核对服务显示名与桌面名是否一致、description 是否包含忽略隐私警告话术",
        "observable_utg_signals": ["服务名 “Dr. Security”", "描述文本含 “You can have the privacy warning ignored”", "开关默认关闭且无系统二次确认（targetSdk 22）"]
      },
      {
        "page_role": "获权后系统应用详情页自动点击现场",
        "page_identifier": "com.android.settings 的 InstalledAppDetailsTop / InstalledAppDetailsActivity 页面（点击“强行停止”后的确认弹窗）",
        "why_most_useful": "验证抗撤销行为：确认弹窗被无障碍自动点击，用户无法完成停用",
        "observable_utg_signals": ["确认弹窗出现后极短时间内自动消失", "无用户触摸事件但按钮被触发", "日志/事件中出现 com.anti.security.security 对 settings 页的 TYPE_WINDOW_STATE_CHANGED 处理"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导文案全部为可提取文本，无图片化诱导；但需注意 ①两个入口均位于二级页面（权限引导列表、电池省电页），冷启动首屏不弹窗，若仅截首屏会漏检；②AccessibilityDialogActivity 在系统设置页之上压栈，UTG 抓取需以当前 top activity 而非应用包名判定；③获权后的自动点击发生在 com.android.settings 前台，需在系统设置页内做事件时序比对才能观测。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "ns.pa#a(android.app.Activity, int)",
    "com.anti.security.activity.GrantPermissonsActivity$4#onClick",
    "com.anti.security.activity.BatterySaverSelectActivity#onEnable",
    "com.anti.security.activity.BatterySaverSelectActivity#showAccessibilityToast",
    "com.anti.security.service.BatteryOptimizeService#onAccessibilityEvent",
    "res/xml/top_accessbility.xml"
  ]
}
```

</details>
