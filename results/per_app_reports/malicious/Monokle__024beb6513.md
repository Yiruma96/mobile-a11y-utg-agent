# MR_132__024beb6513｜Monokle — Skype

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：160.1s

## 1. 一句话核心结论

- **核心申请方式**：该样本不使用任何无障碍引导 UI：无障碍服务 AccessService 未在 Manifest 注册，改由 Xposed 钩子伪造 Settings.Secure 的 enabled_accessibility_services/accessibility_enabled 返回值实现静默启用键盘记录。
- **静态可见性说明**：DEX 未加壳、未加密，secupd 家族代码（含无障碍服务实现与 Xposed 钩子）完全静态可见；不依赖远端 HTML 或动态载荷。经全包核验，不存在无障碍引导页面/文案/遮罩资源，故无隐藏的引导链路需要还原。唯一未静态展开的是 Xposed 框架外部注入时机（依赖设备侧 Xposed 环境）。
- **命中的行为模式标签**：`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_FAKE_IS_ACCESSIBILITY_TOOL`（伪造android:isAccessibilityTool="true"）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `024beb6513d8fc73839fa4f9e4a2790f1e71528256f2b88f89db1099b70b1096` |
| 包名 / 年份 | `com.skype.raider` / 2019 |
| 家族 / 品类 | **Monokle**（同池样本数：25） |
| 原始来源标识 | https://www.lookout.com/documents/threat-reports/lookout-discovers-monokle-threat-report.pdf |
| 桌面显示名 | Skype |
| 引导页宣称品牌/身份 | Skype / Microsoft（盗用正版 com.skype.raider 包名、SkypeApplication 与微软 MSA 登录 SDK 外壳） |
| 系统无障碍列表服务名 | 无（未在 Manifest 声明无障碍服务，系统无障碍列表不显示任何条目）；代码内服务 TAG 为 RecorderService，组件名为 com.system.security_update.xposed.keylogger.AccessService |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：借用正版 Skype 包名与微软在线身份 SDK（com.microsoft.onlineid.*、assets/msa/signup.live.com 页面）构建可信外壳；恶意无障碍服务完全不注册到系统，靠 Xposed 钩子伪造 Settings.Secure 读取结果，绕过系统无障碍列表与用户可见开关；恶意命名空间伪装为 com.system.security_update / com.smartagents.system_service 冒充系统安全更新组件。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.skype.android.SkypeApplication / 正版 Skype 启动 Activity（外壳正常业务） | 用户点击桌面 Skype 图标冷启动 | 原生Activity | 无 | 正常使用 Skype 功能；无要求开启无障碍的操作 | `#1 manifest:components（application android:name=com.skype.android.SkypeApplication）` |
| 2 | 业务功能触发 | com.skype.android.util.permission.PermissionDialog（运行时权限说明对话框） | 首次使用相机/麦克风/通讯录等业务功能时请求运行时权限；被永久拒绝后弹说明框 | 原生Dialog | **原文**：无（本次未逐条读取该 Dialog 的 strings 资源）<br>**译注**：标准 Android 运行时权限说明，引导用户前往应用详情页手动授予权限 | 点击确认按钮跳转系统应用详情页；含取消路径 | `com.skype.android.util.permission.PermissionDialog#onCreateDialog` |
| 3 | 跳受限设置 | 系统页面 android.settings.APPLICATION_DETAILS_SETTINGS（本应用详情页） | PermissionDialog$2.onClick 构造 Intent 并 startActivity（FLAG_ACTIVITY_NEW_TASK） | 系统无障碍页 | **原文**：android.settings.APPLICATION_DETAILS_SETTINGS<br>**译注**：跳转至系统「应用信息」页，供用户手动开启权限；与无障碍无关 | 用户手动点击权限开关；无强制、无循环重跳 | `com.skype.android.util.permission.PermissionDialog$2#onClick` |
| 4 | 获权后动作 | secupd.BackgroundService（android:exported=true，action com.smartagents.system_service.BackgroundService） | 服务 onCreate 调用 ServiceEngine.GrantAllPermissions()，在 root/NaNo 可用时批量执行 pm grant 与 appops set | 不可静态还原 | **原文**：pm grant <pkg> android.permission.SYSTEM_ALERT_WINDOW；appops set <pkg> android:system_alert_window allow；appops set <pkg> android:write_settings allow<br>**译注**：在无任何用户交互的情况下直接以 shell 身份授予短信、相机、通讯录、悬浮窗、写设置等权限 | 无任何用户操作，全程静默 | `secupd.ServiceEngine#GrantAllPermissions` |
| 5 | 获权后动作 | secupd.xposed.keylogger.AccessService（AccessibilityService 实现，未在 Manifest 注册） | Xposed 钩子 KeyLogger$10/$11 篡改 Settings.Secure.getStringForUser 返回，使系统与第三方判定该无障碍服务「已启用」；服务随即接收无障碍事件 | 不可静态还原 | **原文**：com.smartagents.system_service/com.system.security_update.xposed.keylogger.AccessService；accessibility_enabled -> 1<br>**译注**：系统无障碍列表与读取方被欺骗为服务已开启，用户从未看到过该条目；服务持续抓取前台包名与输入文本并经广播外发 | 无（用户无感知，也无从撤销） | `secupd.xposed.keylogger.KeyLogger$10#afterHookedMethod` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无任何无障碍引导/说明文字：AndroidManifest 中不存在 android.accessibilityservice 组件、android:description 或 accessibility-service 元数据
- res/ 全量 XML 中不存在 accessibility 相关配置（grep 零命中），因此系统无障碍列表不会出现本应用条目
- 全 DEX 搜索 ACCESSIBILITY_SETTINGS 零命中，代码中无跳转系统无障碍设置页的实现
- 唯一跳转受限设置的位置为运行时权限说明对话框 com.skype.android.util.permission.PermissionDialog，跳转目标为 APPLICATION_DETAILS_SETTINGS（应用详情页），与无障碍无关
- 无障碍启用状态呈现完全由 Xposed 钩子伪造（KeyLogger$10/$11 改写 Settings.Secure 返回值），不产生任何界面文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | enabled_accessibility_services | 已启用的无障碍服务（系统设置键名，被钩子篡改返回值为攻击者组件） | `secupd.xposed.keylogger.KeyLogger$10#afterHookedMethod / KeyLogger$11#afterHookedMethod（硬编码字符串）` | 未知 |
| en | com.smartagents.system_service/com.system.security_update.xposed.keylogger.AccessService | 伪造的「已启用无障碍服务」返回值，伪装为系统安全更新组件 | `secupd.xposed.keylogger.KeyLogger$10#afterHookedMethod（setResult 硬编码）` | 未知 |
| en | com.system.security_update.xposed.ontextchanged | 输入文本变更外发广播通道（伪装为系统安全更新） | `secupd.xposed.keylogger.AccessService 常量 ONTEXTCHANGED_BROADCAST_FILTER` | 未知 |
| en | %1$s won't run without Google Play services, which are missing from your phone. | 缺少 Google Play 服务，%1$s 无法运行。 | `Google Play services 标准 SDK 字符串资源（三方 SDK，非恶意诱导文案）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无。不存在无障碍引导流程，因此也没有拒绝后的重跳或定时拉起；唯一的系统设置跳转是运行时权限被永久拒绝后的一次性跳转应用详情页，用户返回后不会循环重跳。
- **遮罩叠层 / 高仿系统设置页**：无半透明引导遮罩、无全屏悬浮窗、无高仿无障碍开关页；SYSTEM_ALERT_WINDOW 权限存在，但在本次核验路径中用于后台控制而非无障碍引导。伪造发生在系统设置数据层（Xposed 钩子改写 Settings.Secure 读取结果），而非 UI 层。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现针对 Android 13+ 受限设置的「应用详情 → 右上角菜单 → 允许受限设置」分步教学，也未发现 SESSION_INSTALLER 相关调用点。
- **获权后即时行为与防撤权机制**：未发现监听无障碍设置页并以 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；但存在更强的隐蔽机制：用户界面显示的服务状态本身被伪造，实际启用状态与可见状态分离，常规撤权路径失效。另有 KeyLogger 钩子监听 enabled_accessibility_services 变更并记录日志。
- **良性降级 / 替代方案**：无（恶意实现）。应用无「仅观看模式/手动模式/ADB 说明」等替代降级路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本不存在无障碍引导 UI，纯 UTG 无法通过「引导弹窗/跳转无障碍设置」触发。有效观测点为：(1) 在 Xposed 环境下调用 Settings.Secure.getString 读取 enabled_accessibility_services / accessibility_enabled，对比系统无障碍设置页实际条目与返回值是否不一致；(2) 监听广播 com.system.security_update.xposed.ontextchanged 的发送时机；(3) 监听 secupd.BackgroundService（action com.smartagents.system_service.BackgroundService）启动后是否出现 pm grant / appops set 的 root 授权行为。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：纯 UTG 存在根本性盲区：该样本不通过任何界面引导无障碍，所有关键行为发生在系统设置数据层（Xposed 钩子伪造 Settings.Secure）与后台服务层（静默 pm grant/appops set），UTG 无法观测到「诱导」动作。此外恶意载荷依赖设备侧 Xposed 框架，未安装 Xposed 的普通设备上伪造分支不触发，此时应用表现为不含无障碍功能的 Skype 外壳，运行期 UTG 完全无异常信号。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表（用于证明应用条目缺失）** | Settings.ACTION_ACCESSIBILITY_SETTINGS 列表中不存在任何 com.skype.raider / com.system.security_update 条目 | 服务未注册是关键事实，捕获空列表即可证明用户从未被引导开启，与后续实际启用状态形成矛盾 | 无障碍列表无本应用条目；列表为空但系统 Settings.Secure 返回值为已启用 |
| **运行时权限说明弹窗（唯一存在的设置跳转入口）** | com.skype.android.util.permission.PermissionDialog 对话框，按钮点击后进入 Application Details | 用于确认应用唯一的「跳受限设置」行为属于常规权限流程，排除无障碍诱导误判 | 对话框文本为权限说明；跳转目标为 APPLICATION_DETAILS_SETTINGS 而非 ACCESSIBILITY_SETTINGS |
| **静默提权执行时刻（root 授权弹窗 / su 调用）** | secupd.BackgroundService 启动后出现 su 请求或 appops/pm grant 调用 | 该路径替代了无障碍引导，是用户实际被绕过的授权环节，最能佐证恶意意图 | su 授权弹窗出现；无 UI 交互即新增权限 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `secupd.xposed.keylogger.KeyLogger$10#afterHookedMethod`
- `secupd.xposed.keylogger.KeyLogger$11#afterHookedMethod`
- `secupd.xposed.keylogger.AccessService#onAccessibilityEvent`
- `secupd.ServiceEngine#GrantAllPermissions`
- `com.skype.android.util.permission.PermissionDialog$2#onClick`
- `AndroidManifest.xml（secupd.BackgroundService 导出声明，第 421-425 行）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，共 12 次工具调用）

**核心发现：该样本根本不存在"引导用户开启无障碍"的 UTG 页面流转，它的无障碍能力由 Xposed 钩子伪造系统设置读取结果静默获得。**

- **Manifest 中没有无障碍声明**：完整 `AndroidManifest.xml` 中既没有 `android.accessibilityservice` 组件，也没有 `BIND_ACCESSIBILITY_SERVICE` 权限、`accessibility-service` 元数据或任何 `res/xml` 无障碍配置文件（`grep res/` 搜索 `ccessib` 零命中）。
- **代码中确实存在无障碍服务实现，但服务未注册**：[secupd.xposed.keylogger.AccessService](<resource-unit:#1.dex1 code:secupd.xposed.keylogger.AccessService#onAccessibilityEvent>) 继承 `AccessibilityService`，TAG 为 `RecorderService`，抓取前台包名与控件文本，并通过广播 `com.system.security_update.xposed.ontextchanged` 外发。
- **伪造启用状态，绕过全部 UI**：[KeyLogger$10#afterHookedMethod](<resource-unit:#1.dex1 code:secupd.xposed.keylogger.KeyLogger$10#afterHookedMethod>) 在 `Settings.Secure.getStringForUser` 返回后，将 `enabled_accessibility_services` 改写为 `com.smartagents.system_service/com.system.security_update.xposed.keylogger.AccessService`，将 `accessibility_enabled` 改写为 `"1"`；[KeyLogger$11#afterHookedMethod](<resource-unit:#1.dex1 code:secupd.xposed.keylogger.KeyLogger$11#afterHookedMethod>) 逻辑相同。
- **唯一跳转受限设置的位置与无障碍无关**：全包搜索 `ACCESSIBILITY_SETTINGS` 零命中；`APPLICATION_DETAILS_SETTINGS` 仅有两处，其中一处在 [PermissionDialog$2#onClick](<resource-unit:#1.dex1 code:com.skype.android.util.permission.PermissionDialog$2#onClick>)，用于运行时权限被永久拒绝后引导用户进入应用详情页（标准 Android 6 权限流程）。
- **另一条无需用户操作的提权路径**：[secupd.ServiceEngine#GrantAllPermissions](<resource-unit:#1.dex1 code:secupd.ServiceEngine#GrantAllPermissions>) 在有 root 或 NaNo 时批量执行 `pm grant` 与 `appops set ... system_alert_window allow`、`write_settings allow`，由导出的 `secupd.BackgroundService` 在 `onCreate` 触发。
- **判定**：无引导页、无说明文案、无遮罩、无拒权循环，因为引导环节被完全跳过；系统无障碍开关显示状态与真实状态可能不一致，用户无法通过常规界面发现或撤销。已登记为 R-001（high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳、未加密，secupd 家族代码（含无障碍服务实现与 Xposed 钩子）完全静态可见；不依赖远端 HTML 或动态载荷。经全包核验，不存在无障碍引导页面/文案/遮罩资源，故无隐藏的引导链路需要还原。唯一未静态展开的是 Xposed 框架外部注入时机（依赖设备侧 Xposed 环境）。",
  "summary_one_liner": "该样本不使用任何无障碍引导 UI：无障碍服务 AccessService 未在 Manifest 注册，改由 Xposed 钩子伪造 Settings.Secure 的 enabled_accessibility_services/accessibility_enabled 返回值实现静默启用键盘记录。",
  "disguise_identity": {
    "app_display_name": "Skype",
    "claimed_brand_or_persona": "Skype / Microsoft（盗用正版 com.skype.raider 包名、SkypeApplication 与微软 MSA 登录 SDK 外壳）",
    "a11y_service_label": "无（未在 Manifest 声明无障碍服务，系统无障碍列表不显示任何条目）；代码内服务 TAG 为 RecorderService，组件名为 com.system.security_update.xposed.keylogger.AccessService",
    "identity_mismatch": true,
    "obfuscation_tricks": "借用正版 Skype 包名与微软在线身份 SDK（com.microsoft.onlineid.*、assets/msa/signup.live.com 页面）构建可信外壳；恶意无障碍服务完全不注册到系统，靠 Xposed 钩子伪造 Settings.Secure 读取结果，绕过系统无障碍列表与用户可见开关；恶意命名空间伪装为 com.system.security_update / com.smartagents.system_service 冒充系统安全更新组件。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.skype.android.SkypeApplication / 正版 Skype 启动 Activity（外壳正常业务）",
      "trigger_event": "用户点击桌面 Skype 图标冷启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "呈现正版 Skype 聊天/通话界面，无任何无障碍相关提示",
      "user_action_requested": "正常使用 Skype 功能；无要求开启无障碍的操作",
      "code_anchor": "#1 manifest:components（application android:name=com.skype.android.SkypeApplication）"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.skype.android.util.permission.PermissionDialog（运行时权限说明对话框）",
      "trigger_event": "首次使用相机/麦克风/通讯录等业务功能时请求运行时权限；被永久拒绝后弹说明框",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无（本次未逐条读取该 Dialog 的 strings 资源）",
      "shown_text_zh": "标准 Android 运行时权限说明，引导用户前往应用详情页手动授予权限",
      "user_action_requested": "点击确认按钮跳转系统应用详情页；含取消路径",
      "code_anchor": "com.skype.android.util.permission.PermissionDialog#onCreateDialog"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统页面 android.settings.APPLICATION_DETAILS_SETTINGS（本应用详情页）",
      "trigger_event": "PermissionDialog$2.onClick 构造 Intent 并 startActivity（FLAG_ACTIVITY_NEW_TASK）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.APPLICATION_DETAILS_SETTINGS",
      "shown_text_zh": "跳转至系统「应用信息」页，供用户手动开启权限；与无障碍无关",
      "user_action_requested": "用户手动点击权限开关；无强制、无循环重跳",
      "code_anchor": "com.skype.android.util.permission.PermissionDialog$2#onClick"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "secupd.BackgroundService（android:exported=true，action com.smartagents.system_service.BackgroundService）",
      "trigger_event": "服务 onCreate 调用 ServiceEngine.GrantAllPermissions()，在 root/NaNo 可用时批量执行 pm grant 与 appops set",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "pm grant <pkg> android.permission.SYSTEM_ALERT_WINDOW；appops set <pkg> android:system_alert_window allow；appops set <pkg> android:write_settings allow",
      "shown_text_zh": "在无任何用户交互的情况下直接以 shell 身份授予短信、相机、通讯录、悬浮窗、写设置等权限",
      "user_action_requested": "无任何用户操作，全程静默",
      "code_anchor": "secupd.ServiceEngine#GrantAllPermissions"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "secupd.xposed.keylogger.AccessService（AccessibilityService 实现，未在 Manifest 注册）",
      "trigger_event": "Xposed 钩子 KeyLogger$10/$11 篡改 Settings.Secure.getStringForUser 返回，使系统与第三方判定该无障碍服务「已启用」；服务随即接收无障碍事件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "com.smartagents.system_service/com.system.security_update.xposed.keylogger.AccessService；accessibility_enabled -> 1",
      "shown_text_zh": "系统无障碍列表与读取方被欺骗为服务已开启，用户从未看到过该条目；服务持续抓取前台包名与输入文本并经广播外发",
      "user_action_requested": "无（用户无感知，也无从撤销）",
      "code_anchor": "secupd.xposed.keylogger.KeyLogger$10#afterHookedMethod"
    }
  ],
  "text_presentation_locations": [
    "无任何无障碍引导/说明文字：AndroidManifest 中不存在 android.accessibilityservice 组件、android:description 或 accessibility-service 元数据",
    "res/ 全量 XML 中不存在 accessibility 相关配置（grep 零命中），因此系统无障碍列表不会出现本应用条目",
    "全 DEX 搜索 ACCESSIBILITY_SETTINGS 零命中，代码中无跳转系统无障碍设置页的实现",
    "唯一跳转受限设置的位置为运行时权限说明对话框 com.skype.android.util.permission.PermissionDialog，跳转目标为 APPLICATION_DETAILS_SETTINGS（应用详情页），与无障碍无关",
    "无障碍启用状态呈现完全由 Xposed 钩子伪造（KeyLogger$10/$11 改写 Settings.Secure 返回值），不产生任何界面文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "enabled_accessibility_services",
      "text_zh": "已启用的无障碍服务（系统设置键名，被钩子篡改返回值为攻击者组件）",
      "source_location": "secupd.xposed.keylogger.KeyLogger$10#afterHookedMethod / KeyLogger$11#afterHookedMethod（硬编码字符串）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "com.smartagents.system_service/com.system.security_update.xposed.keylogger.AccessService",
      "text_zh": "伪造的「已启用无障碍服务」返回值，伪装为系统安全更新组件",
      "source_location": "secupd.xposed.keylogger.KeyLogger$10#afterHookedMethod（setResult 硬编码）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "com.system.security_update.xposed.ontextchanged",
      "text_zh": "输入文本变更外发广播通道（伪装为系统安全更新）",
      "source_location": "secupd.xposed.keylogger.AccessService 常量 ONTEXTCHANGED_BROADCAST_FILTER",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't run without Google Play services, which are missing from your phone.",
      "text_zh": "缺少 Google Play 服务，%1$s 无法运行。",
      "source_location": "Google Play services 标准 SDK 字符串资源（三方 SDK，非恶意诱导文案）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无。不存在无障碍引导流程，因此也没有拒绝后的重跳或定时拉起；唯一的系统设置跳转是运行时权限被永久拒绝后的一次性跳转应用详情页，用户返回后不会循环重跳。",
    "overlay_or_fake_settings": "无半透明引导遮罩、无全屏悬浮窗、无高仿无障碍开关页；SYSTEM_ALERT_WINDOW 权限存在，但在本次核验路径中用于后台控制而非无障碍引导。伪造发生在系统设置数据层（Xposed 钩子改写 Settings.Secure 读取结果），而非 UI 层。",
    "restricted_settings_13plus_coaching": "无。未发现针对 Android 13+ 受限设置的「应用详情 → 右上角菜单 → 允许受限设置」分步教学，也未发现 SESSION_INSTALLER 相关调用点。",
    "post_grant_anti_removal": "未发现监听无障碍设置页并以 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；但存在更强的隐蔽机制：用户界面显示的服务状态本身被伪造，实际启用状态与可见状态分离，常规撤权路径失效。另有 KeyLogger 钩子监听 enabled_accessibility_services 变更并记录日志。",
    "benign_graceful_degradation": "无（恶意实现）。应用无「仅观看模式/手动模式/ADB 说明」等替代降级路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本不存在无障碍引导 UI，纯 UTG 无法通过「引导弹窗/跳转无障碍设置」触发。有效观测点为：(1) 在 Xposed 环境下调用 Settings.Secure.getString 读取 enabled_accessibility_services / accessibility_enabled，对比系统无障碍设置页实际条目与返回值是否不一致；(2) 监听广播 com.system.security_update.xposed.ontextchanged 的发送时机；(3) 监听 secupd.BackgroundService（action com.smartagents.system_service.BackgroundService）启动后是否出现 pm grant / appops set 的 root 授权行为。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表（用于证明应用条目缺失）",
        "page_identifier": "Settings.ACTION_ACCESSIBILITY_SETTINGS 列表中不存在任何 com.skype.raider / com.system.security_update 条目",
        "why_most_useful": "服务未注册是关键事实，捕获空列表即可证明用户从未被引导开启，与后续实际启用状态形成矛盾",
        "observable_utg_signals": ["无障碍列表无本应用条目", "列表为空但系统 Settings.Secure 返回值为已启用"]
      },
      {
        "page_role": "运行时权限说明弹窗（唯一存在的设置跳转入口）",
        "page_identifier": "com.skype.android.util.permission.PermissionDialog 对话框，按钮点击后进入 Application Details",
        "why_most_useful": "用于确认应用唯一的「跳受限设置」行为属于常规权限流程，排除无障碍诱导误判",
        "observable_utg_signals": ["对话框文本为权限说明", "跳转目标为 APPLICATION_DETAILS_SETTINGS 而非 ACCESSIBILITY_SETTINGS"]
      },
      {
        "page_role": "静默提权执行时刻（root 授权弹窗 / su 调用）",
        "page_identifier": "secupd.BackgroundService 启动后出现 su 请求或 appops/pm grant 调用",
        "why_most_useful": "该路径替代了无障碍引导，是用户实际被绕过的授权环节，最能佐证恶意意图",
        "observable_utg_signals": ["su 授权弹窗出现", "无 UI 交互即新增权限"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "纯 UTG 存在根本性盲区：该样本不通过任何界面引导无障碍，所有关键行为发生在系统设置数据层（Xposed 钩子伪造 Settings.Secure）与后台服务层（静默 pm grant/appops set），UTG 无法观测到「诱导」动作。此外恶意载荷依赖设备侧 Xposed 框架，未安装 Xposed 的普通设备上伪造分支不触发，此时应用表现为不含无障碍功能的 Skype 外壳，运行期 UTG 完全无异常信号。"
  },
  "behavior_pattern_tags": [
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_FAKE_IS_ACCESSIBILITY_TOOL",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "COERCE_REFUSAL_LOOP_RELAUNCH"
  ],
  "code_anchors": [
    "secupd.xposed.keylogger.KeyLogger$10#afterHookedMethod",
    "secupd.xposed.keylogger.KeyLogger$11#afterHookedMethod",
    "secupd.xposed.keylogger.AccessService#onAccessibilityEvent",
    "secupd.ServiceEngine#GrantAllPermissions",
    "com.skype.android.util.permission.PermissionDialog$2#onClick",
    "AndroidManifest.xml（secupd.BackgroundService 导出声明，第 421-425 行）"
  ]
}
```

> 说明：`CARRIER_SYSTEM_A11Y_DESCRIPTION` 与 `COERCE_REFUSAL_LOOP_RELAUNCH` 用于标注"系统无障碍条目层面的身份伪装"与"撤权/拒权反馈失效"的实际效果；本样本并不通过系统无障碍列表呈现条目，也未实现循环重跳，二者仅作为最接近的标准词表映射。

</details>
