# MR_060__61f9f37672｜Monokle — Signal

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：129.2s

## 1. 一句话核心结论

- **核心申请方式**：应用不在前台做任何说明式引导，而由后台服务在配置开关为真时静默连续拉起系统无障碍设置页、通知监听设置页与悬浮窗授权页，未授权即被反复重跳，无障碍服务标签伪装为 AndroidSecurity。
- **静态可见性说明**：无障碍服务类、跳转 Intent、a11y 配置 XML 与 Manifest 声明全部静态可见；但触发开关 wQuqU.wQlkkq() 依赖加密配置/下发值，且同一序列中 wQUWQp、wQvQmN、wQuiNB 三个跳转目标未在本次预算内逐一展开，重跳周期未核实。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `61f9f376728b19a992d6ea5bddb907eaeabf5fa85aaf97bd4c5d4030b523d9a7` |
| 包名 / 年份 | `org.thoughtcrime.securesms` / 2019 |
| 家族 / 品类 | **Monokle**（同池样本数：25） |
| 原始来源标识 | https://www.lookout.com/documents/threat-reports/lookout-discovers-monokle-threat-report.pdf |
| 桌面显示名 | Signal |
| 引导页宣称品牌/身份 | Signal（org.thoughtcrime.securesms，官方开源加密通讯应用） |
| 系统无障碍列表服务名 | AndroidSecurity |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 完全缺失，系统无障碍列表仅显示伪装标签 AndroidSecurity；同模块通知监听服务标签为 AndroidNotificationSecure，均仿系统安全组件命名；真实模块包名为 com.system.security_update 而宿主包名冒用 org.thoughtcrime.securesms；类名/方法名整体混淆（wQqBQ、wQnm、wQQiP）。未发现同形字、多 activity-alias 或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.system.security_update.accessibility.services.AccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.system.security_update.BackgroundService（独立进程后台服务，非 Activity） | onCreate()：App.reInit 后广播 CLIENT_SERVICE_START，读取 wQuqU 配置，若 wQqKkQm().wQBu 为假则 new Thread(wQLKWN.INSTANCE).start() | 不可静态还原 | 无 | 无（用户不可见，无取消/跳过选项） | `com.system.security_update.BackgroundService.onCreate` |
| 2 | 业务功能触发 | com.system.security_update.wQLKWN.run → BackgroundService.wQqpwMU | 后台线程 run() 回调，判定 wQuqU.getInstance().wQlkkq()（下发配置开关）为真后调用 wQqBQ.wQnm() | 不可静态还原 | 无 | 无 | `com.system.security_update.BackgroundService.wQqpwMU` |
| 3 | 跳受限设置 | 系统悬浮窗授权页（android.settings.action.MANAGE_OVERLAY_PERMISSION，定向 package:org.thoughtcrime.securesms） | wQnm() 顺序调用 wQlMupM()，仅当 SDK>=23 且 Settings.canDrawOverlays() 为 false 时 startActivity | 系统无障碍页 | **原文**：无（应用侧未附加任何说明文案）<br>**译注**：直接展示系统「显示在其他应用上层」授权页，应用未作任何前置解释 | 要求用户在该系统页手动打开悬浮窗开关；应用侧无取消/跳过按钮，用户只能按返回键退出 | `com.system.security_update.wQqBQ.wQlMupM` |
| 4 | 跳无障碍设置 | 系统无障碍设置列表（android.settings.ACCESSIBILITY_SETTINGS），列表项标签 AndroidSecurity | wQnm() 调用 wQQiP()，判定 AccessibilityService.wQqp(App.getContext()) 为 false（服务未启用）即 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(FLAG_ACTIVITY_NEW_TASK)) | 系统无障碍页 | **原文**：AndroidSecurity<br>**译注**：系统无障碍列表中出现名为「AndroidSecurity」的服务项，无任何功能说明（android:description 缺失） | 要求用户在系统列表中进入 AndroidSecurity 并开启开关；应用侧无说明页、无取消/跳过路径 | `com.system.security_update.wQqBQ.wQQiP；AndroidManifest.xml service android:label="AndroidSecurity"` |
| 5 | 跳受限设置 | 系统通知使用权页（android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS），服务标签 AndroidNotificationSecure | wQnm() 调用 wQNILMU()，SDK>=22 且 NotificationListener.wQMwn() 为 false 时 startActivity | 系统无障碍页 | **原文**：AndroidNotificationSecure<br>**译注**：系统「通知使用权」列表中出现伪装为安全组件的 AndroidNotificationSecure 项 | 要求用户手动授权通知使用权；无解释文案、无跳过 | `com.system.security_update.wQqBQ.wQNILMU` |
| 6 | 拒权反馈循环 | wQLKWN 后台线程 → wQqBQ.wQnm 序列反复执行 | 用户从系统设置返回后，后台线程再次回调 wQqpwMU；wQQiP 以「服务是否已启用」为唯一判定，未启用则再次 startActivity | 不可静态还原 | 无 | 无合法退出路径：应用不提供「暂不开启」或替代使用模式 | `com.system.security_update.wQqBQ.wQQiP / com.system.security_update.accessibility.services.AccessibilityService.wQqp` |
| 7 | 获权后动作 | com.system.security_update.accessibility.services.AccessibilityService | onServiceConnected() 启动消费线程，onAccessibilityEvent() 将全部事件（typeAllMask、含不重要的视图、可读取窗口内容）入队 wQii | 不可静态还原 | 无 | 无；未发现自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权等反撤权逻辑（撤权对抗由 root 侧写 settings 完成，见既有风险） | `com.system.security_update.accessibility.services.AccessibilityService.onServiceConnected / onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无任何应用侧引导/说明文字：全库仅 1 处 ACCESSIBILITY_SETTINGS 字面量，且紧邻代码为 startActivity，不含 Dialog/Toast/WebView
- 系统无障碍服务列表项标签：AndroidManifest.xml 中 android:label="AndroidSecurity"（该标签是用户唯一能看到的文本）
- 系统无障碍服务详情页描述：res/xml/accessibility_service_config.xml 未设置 android:description，因此描述区域为空
- 系统通知使用权列表项标签：android:label="AndroidNotificationSecure"
- 悬浮窗授权页：仅系统自带文案，应用未注入任何说明

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | AndroidSecurity | 安卓安全（伪装为系统安全组件） | `AndroidManifest.xml service android:name=com.system.security_update.accessibility.services.AccessibilityService 的 android:label` | 假反诈安全 |
| en | AndroidNotificationSecure | 安卓通知安全（伪装为系统通知安全组件） | `AndroidManifest.xml service android:name=com.system.security_update.data.NotificationListener 的 android:label` | 假反诈安全 |
| en | android.settings.ACCESSIBILITY_SETTINGS | 系统无障碍设置页（直接跳转，无前置说明） | `com.system.security_update.wQqBQ.wQQiP 硬编码 Intent action` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：wQQiP 以 AccessibilityService.wQqp()（服务是否已启用）为唯一前置判定，未启用即 startActivity 拉起系统无障碍页；该序列由 wQLKWN 后台线程反复回调 wQqpwMU 驱动，用户按返回退出设置页后会被再次拉起，且应用不提供降级或「稍后再说」路径。重跳的具体时间间隔未在本次核验范围内确认。
- **遮罩叠层 / 高仿系统设置页**：无。未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；悬浮窗权限申请仅为跳转 MANAGE_OVERLAY_PERMISSION 系统页，未见用于叠层指引的悬浮 View 文案。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全库未出现 ACTION_APPLICATION_DETAILS_SETTINGS 或「受限设置」相关引导；targetSdkVersion 为 26，未针对 Android 13 受限设置做教学式规避。
- **获权后即时行为与防撤权机制**：未发现无障碍服务内自点确认或监听设置页使用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑（该服务的 onAccessibilityEvent 仅将事件入队）。撤权对抗由 root 侧静默写 settings 实现，属另一命题。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到任何 Activity 启动 Intent 的 action 为 android.settings.ACCESSIBILITY_SETTINGS、android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS 或 android.settings.action.MANAGE_OVERLAY_PERMISSION 的瞬间（这三者由后台线程无界面连续发起，是最可靠的拉起点）；其次可监听 com.system.security_update.BackgroundService 启动后 1–3 秒窗口。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在盲区：本样本全程无任何应用侧引导文本（无弹窗、无 WebView、无遮罩），纯 UTG 只能捕获到系统设置页，若仅依赖「非系统包名页面上的诱导文案」规则会漏判；必须以「后台无提示直跳受限设置 + 循环重跳 + 服务标签伪装」作为判别特征。另触发受下发配置开关 wQuqU.wQlkkq() 控制，若服务端未开启则该跳转链在运行期可能完全不出现。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转链首个受限设置页（悬浮窗授权）** | package com.android.settings 的 DrawOverlayDetail/ManageOverlayPermission 页，标题为「显示在其他应用上层」 | 此处能证明跳转是后台无提示发起、且用户未做任何功能操作，直接否定「业务功能触发」的良性解释 | 栈中前一页面为 Signal 主界面或无任何页面（纯后台发起）；页面文案完全为系统原文，无应用自定义说明 |
| **系统无障碍服务列表项（关键伪装页）** | com.android.settings AccessibilitySettings 页，列表项文本 AndroidSecurity，描述区为空 | 标签 AndroidSecurity + 空描述 + 宿主为 Signal，是身份伪装的直接可观测证据 | 列表项 label 文本 AndroidSecurity；条目下无描述文本；同一列表中不存在 Signal 相关无障碍条目 |
| **系统通知使用权列表项** | NotificationAccessSettings 页，条目文本 AndroidNotificationSecure | 与无障碍项成对出现，说明同一序列批量索权而非单一功能需求 | 条目 label AndroidNotificationSecure；出现时序紧随无障碍页跳转 |
| **拒权后重跳观测** | 从设置页返回后再次出现的 AccessibilitySettings / ManageOverlayPermission 页 | 验证循环重跳，区分「一次性申请」与「强制索权」 | 返回主界面后短时间内同一系统页再次压栈；期间无应用侧 Toast/Dialog 说明 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.system.security_update.wQqBQ.wQQiP`
- `com.system.security_update.wQqBQ.wQnm`
- `com.system.security_update.wQqBQ.wQNILMU`
- `com.system.security_update.wQqBQ.wQlMupM`
- `com.system.security_update.BackgroundService.wQqpwMU`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验：无障碍权限引导链路）

**核心发现：本应用没有采用"引导说明 → 弹窗/教学页 → 用户手动开启"的常规诱导流程；它由后台服务在代码中直接、无提示地跳转到系统设置页。**

已核实的事实链（均来自静态代码，非推测）：

1. **入口在后台服务，不在 Activity 或引导页。** [BackgroundService.onCreate()](<resource-unit:#1.dex1 code:com.system.security_update.BackgroundService#onCreate>) 读取加密配置后启动线程 `wQLKWN.INSTANCE`，线程回调 [BackgroundService.wQqpwMU()](<resource-unit:#1.dex1 code:com.system.security_update.BackgroundService#wQqpwMU>) 仅在 `wQuqU.getInstance().wQlkkq()` 为真（配置开关）时调用 `wQqBQ.wQnm()`。即**是否跳设置页由下发的配置决定**，而非用户点击某个功能。

2. **一次调用连续打开多个受限设置页。** [wQqBQ.wQnm()](<resource-unit:#1.dex1 code:com.system.security_update.wQqBQ#wQnm>) 顺序调用 `wQUWQp`、`wQvQmN`、`wQlMupM`、`wQuiNB`、`wQQiP`、`wQNILMU`：
   - [wQQiP()](<resource-unit:#1.dex1 code:com.system.security_update.wQqBQ#wQQiP>) → `Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `FLAG_ACTIVITY_NEW_TASK`；
   - [wQNILMU()](<resource-unit:#1.dex1 code:com.system.security_update.wQqBQ#wQNILMU>) → `ACTION_NOTIFICATION_LISTENER_SETTINGS`；
   - [wQlMupM()](<resource-unit:#1.dex1 code:com.system.security_update.wQqBQ#wQlMupM>) → `MANAGE_OVERLAY_PERMISSION`（`package:` 定向）。
   三处均**无任何说明文本、无 Dialog、无 WebView、无悬浮遮罩**，直接 `startActivity`。

3. **拒绝后循环重跳。** `wQQiP` 的唯一判定是 [AccessibilityService.wQqp()](<resource-unit:#1.dex1 code:com.system.security_update.accessibility.services.AccessibilityService#wQqp>)（即 `wQLKWN.wQii()` 检测服务是否已启用）：**未启用就直接拉起，启用才返回**。该函数由后台线程 `wQLKWN.run` 驱动反复执行，用户返回系统设置后不会进入降级页面，而是被再次拉回无障碍设置页。（重跳的精确周期未在本次调用预算内核实，属未决细节。）

4. **无障碍服务本身是静默采集器，不是"引导展示器"。** [AccessibilityService](<resource-unit:#1.dex1 code:com.system.security_update.accessibility.services.AccessibilityService>) 仅 `onAccessibilityEvent` 入队 `LinkedBlockingQueue`，`onServiceConnected` 启动消费线程；配置 [res/xml/accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 为 `typeAllMask` + `flagIncludeNotImportantViews` + `canRetrieveWindowContent="true"`，**无 `android:description`、无 `isAccessibilityTool`**，系统列表里只有标签 "AndroidSecurity"。

5. **身份伪装。** Manifest 中该服务 label 为 `AndroidSecurity`，同模块通知监听服务 label 为 `AndroidNotificationSecure`，而宿主包名/显示名为 Signal（`org.thoughtcrime.securesms`），内部模块包名 `com.system.security_update` —— 用户在系统无障碍列表中看到的是"AndroidSecurity"，与实际应用身份不一致。

6. **未发现** `ACTION_APPLICATION_DETAILS_SETTINGS` 或"受限设置"分步教学、Session 安装器绕过、伪造高仿开关页或 Gif 引导（全库仅 1 处 `ACCESSIBILITY_SETTINGS` 字面量，无 `isAccessibilityTool`）。因此 Android 13+ 的受限设置门槛在该样本中**未做引导式规避**，其规避手段依赖 root 静默写 settings（既有风险 R-003 已覆盖）。

风险登记：该行为已由既有条目 R-003（静默开启无障碍/通知监听）与 R-001 覆盖，本次为同一命题的定向证据补充，不新增风险条目。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍服务类、跳转 Intent、a11y 配置 XML 与 Manifest 声明全部静态可见；但触发开关 wQuqU.wQlkkq() 依赖加密配置/下发值，且同一序列中 wQUWQp、wQvQmN、wQuiNB 三个跳转目标未在本次预算内逐一展开，重跳周期未核实。",
  "summary_one_liner": "应用不在前台做任何说明式引导，而由后台服务在配置开关为真时静默连续拉起系统无障碍设置页、通知监听设置页与悬浮窗授权页，未授权即被反复重跳，无障碍服务标签伪装为 AndroidSecurity。",
  "disguise_identity": {
    "app_display_name": "Signal",
    "claimed_brand_or_persona": "Signal（org.thoughtcrime.securesms，官方开源加密通讯应用）",
    "a11y_service_label": "AndroidSecurity",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 完全缺失，系统无障碍列表仅显示伪装标签 AndroidSecurity；同模块通知监听服务标签为 AndroidNotificationSecure，均仿系统安全组件命名；真实模块包名为 com.system.security_update 而宿主包名冒用 org.thoughtcrime.securesms；类名/方法名整体混淆（wQqBQ、wQnm、wQQiP）。未发现同形字、多 activity-alias 或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.system.security_update.BackgroundService（独立进程后台服务，非 Activity）",
      "trigger_event": "onCreate()：App.reInit 后广播 CLIENT_SERVICE_START，读取 wQuqU 配置，若 wQqKkQm().wQBu 为假则 new Thread(wQLKWN.INSTANCE).start()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面元素，服务启动不显示任何内容",
      "user_action_requested": "无（用户不可见，无取消/跳过选项）",
      "code_anchor": "com.system.security_update.BackgroundService.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.system.security_update.wQLKWN.run → BackgroundService.wQqpwMU",
      "trigger_event": "后台线程 run() 回调，判定 wQuqU.getInstance().wQlkkq()（下发配置开关）为真后调用 wQqBQ.wQnm()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；是否进入设置页流转由服务端下发配置控制，而非用户操作",
      "user_action_requested": "无",
      "code_anchor": "com.system.security_update.BackgroundService.wQqpwMU"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统悬浮窗授权页（android.settings.action.MANAGE_OVERLAY_PERMISSION，定向 package:org.thoughtcrime.securesms）",
      "trigger_event": "wQnm() 顺序调用 wQlMupM()，仅当 SDK>=23 且 Settings.canDrawOverlays() 为 false 时 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧未附加任何说明文案）",
      "shown_text_zh": "直接展示系统「显示在其他应用上层」授权页，应用未作任何前置解释",
      "user_action_requested": "要求用户在该系统页手动打开悬浮窗开关；应用侧无取消/跳过按钮，用户只能按返回键退出",
      "code_anchor": "com.system.security_update.wQqBQ.wQlMupM"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置列表（android.settings.ACCESSIBILITY_SETTINGS），列表项标签 AndroidSecurity",
      "trigger_event": "wQnm() 调用 wQQiP()，判定 AccessibilityService.wQqp(App.getContext()) 为 false（服务未启用）即 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(FLAG_ACTIVITY_NEW_TASK))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "AndroidSecurity",
      "shown_text_zh": "系统无障碍列表中出现名为「AndroidSecurity」的服务项，无任何功能说明（android:description 缺失）",
      "user_action_requested": "要求用户在系统列表中进入 AndroidSecurity 并开启开关；应用侧无说明页、无取消/跳过路径",
      "code_anchor": "com.system.security_update.wQqBQ.wQQiP；AndroidManifest.xml service android:label=\"AndroidSecurity\""
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统通知使用权页（android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS），服务标签 AndroidNotificationSecure",
      "trigger_event": "wQnm() 调用 wQNILMU()，SDK>=22 且 NotificationListener.wQMwn() 为 false 时 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "AndroidNotificationSecure",
      "shown_text_zh": "系统「通知使用权」列表中出现伪装为安全组件的 AndroidNotificationSecure 项",
      "user_action_requested": "要求用户手动授权通知使用权；无解释文案、无跳过",
      "code_anchor": "com.system.security_update.wQqBQ.wQNILMU"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "wQLKWN 后台线程 → wQqBQ.wQnm 序列反复执行",
      "trigger_event": "用户从系统设置返回后，后台线程再次回调 wQqpwMU；wQQiP 以「服务是否已启用」为唯一判定，未启用则再次 startActivity",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无提示、无降级页；用户返回即被再次拉回系统设置页（重跳精确周期未核实）",
      "user_action_requested": "无合法退出路径：应用不提供「暂不开启」或替代使用模式",
      "code_anchor": "com.system.security_update.wQqBQ.wQQiP / com.system.security_update.accessibility.services.AccessibilityService.wQqp"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.system.security_update.accessibility.services.AccessibilityService",
      "trigger_event": "onServiceConnected() 启动消费线程，onAccessibilityEvent() 将全部事件（typeAllMask、含不重要的视图、可读取窗口内容）入队 wQii",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后无任何界面反馈，服务静默采集全局无障碍事件与窗口内容",
      "user_action_requested": "无；未发现自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权等反撤权逻辑（撤权对抗由 root 侧写 settings 完成，见既有风险）",
      "code_anchor": "com.system.security_update.accessibility.services.AccessibilityService.onServiceConnected / onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "无任何应用侧引导/说明文字：全库仅 1 处 ACCESSIBILITY_SETTINGS 字面量，且紧邻代码为 startActivity，不含 Dialog/Toast/WebView",
    "系统无障碍服务列表项标签：AndroidManifest.xml 中 android:label=\"AndroidSecurity\"（该标签是用户唯一能看到的文本）",
    "系统无障碍服务详情页描述：res/xml/accessibility_service_config.xml 未设置 android:description，因此描述区域为空",
    "系统通知使用权列表项标签：android:label=\"AndroidNotificationSecure\"",
    "悬浮窗授权页：仅系统自带文案，应用未注入任何说明"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "AndroidSecurity",
      "text_zh": "安卓安全（伪装为系统安全组件）",
      "source_location": "AndroidManifest.xml service android:name=com.system.security_update.accessibility.services.AccessibilityService 的 android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "AndroidNotificationSecure",
      "text_zh": "安卓通知安全（伪装为系统通知安全组件）",
      "source_location": "AndroidManifest.xml service android:name=com.system.security_update.data.NotificationListener 的 android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "text_zh": "系统无障碍设置页（直接跳转，无前置说明）",
      "source_location": "com.system.security_update.wQqBQ.wQQiP 硬编码 Intent action",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "wQQiP 以 AccessibilityService.wQqp()（服务是否已启用）为唯一前置判定，未启用即 startActivity 拉起系统无障碍页；该序列由 wQLKWN 后台线程反复回调 wQqpwMU 驱动，用户按返回退出设置页后会被再次拉起，且应用不提供降级或「稍后再说」路径。重跳的具体时间间隔未在本次核验范围内确认。",
    "overlay_or_fake_settings": "无。未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；悬浮窗权限申请仅为跳转 MANAGE_OVERLAY_PERMISSION 系统页，未见用于叠层指引的悬浮 View 文案。",
    "restricted_settings_13plus_coaching": "无。全库未出现 ACTION_APPLICATION_DETAILS_SETTINGS 或「受限设置」相关引导；targetSdkVersion 为 26，未针对 Android 13 受限设置做教学式规避。",
    "post_grant_anti_removal": "未发现无障碍服务内自点确认或监听设置页使用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑（该服务的 onAccessibilityEvent 仅将事件入队）。撤权对抗由 root 侧静默写 settings 实现，属另一命题。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到任何 Activity 启动 Intent 的 action 为 android.settings.ACCESSIBILITY_SETTINGS、android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS 或 android.settings.action.MANAGE_OVERLAY_PERMISSION 的瞬间（这三者由后台线程无界面连续发起，是最可靠的拉起点）；其次可监听 com.system.security_update.BackgroundService 启动后 1–3 秒窗口。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转链首个受限设置页（悬浮窗授权）",
        "page_identifier": "package com.android.settings 的 DrawOverlayDetail/ManageOverlayPermission 页，标题为「显示在其他应用上层」",
        "why_most_useful": "此处能证明跳转是后台无提示发起、且用户未做任何功能操作，直接否定「业务功能触发」的良性解释",
        "observable_utg_signals": ["栈中前一页面为 Signal 主界面或无任何页面（纯后台发起）", "页面文案完全为系统原文，无应用自定义说明"]
      },
      {
        "page_role": "系统无障碍服务列表项（关键伪装页）",
        "page_identifier": "com.android.settings AccessibilitySettings 页，列表项文本 AndroidSecurity，描述区为空",
        "why_most_useful": "标签 AndroidSecurity + 空描述 + 宿主为 Signal，是身份伪装的直接可观测证据",
        "observable_utg_signals": ["列表项 label 文本 AndroidSecurity", "条目下无描述文本", "同一列表中不存在 Signal 相关无障碍条目"]
      },
      {
        "page_role": "系统通知使用权列表项",
        "page_identifier": "NotificationAccessSettings 页，条目文本 AndroidNotificationSecure",
        "why_most_useful": "与无障碍项成对出现，说明同一序列批量索权而非单一功能需求",
        "observable_utg_signals": ["条目 label AndroidNotificationSecure", "出现时序紧随无障碍页跳转"]
      },
      {
        "page_role": "拒权后重跳观测",
        "page_identifier": "从设置页返回后再次出现的 AccessibilitySettings / ManageOverlayPermission 页",
        "why_most_useful": "验证循环重跳，区分「一次性申请」与「强制索权」",
        "observable_utg_signals": ["返回主界面后短时间内同一系统页再次压栈", "期间无应用侧 Toast/Dialog 说明"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在盲区：本样本全程无任何应用侧引导文本（无弹窗、无 WebView、无遮罩），纯 UTG 只能捕获到系统设置页，若仅依赖「非系统包名页面上的诱导文案」规则会漏判；必须以「后台无提示直跳受限设置 + 循环重跳 + 服务标签伪装」作为判别特征。另触发受下发配置开关 wQuqU.wQlkkq() 控制，若服务端未开启则该跳转链在运行期可能完全不出现。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.system.security_update.wQqBQ.wQQiP",
    "com.system.security_update.wQqBQ.wQnm",
    "com.system.security_update.wQqBQ.wQNILMU",
    "com.system.security_update.wQqBQ.wQlMupM",
    "com.system.security_update.BackgroundService.wQqpwMU",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
