# BN_008__82fc2c66db｜专注自律与防沉迷管控 — Why am I here?

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：181.5s

## 1. 一句话核心结论

- **核心申请方式**：该应用在自有设置页以静态说明文字+状态指示呈现无障碍服务用途，仅由用户主动点击“Open service settings”跳转系统无障碍列表，回页后读取状态刷新，无弹窗胁迫、无遮罩、无拒权循环。
- **静态可见性说明**：全量静态可见：无加壳（预筛 False 且 apkid 特征未见）、无加密载荷、无动态加载 dex、无 WebView/远端 HTML、无 INTERNET 权限，引导流程全部由 res/values/strings.xml 与 Compose 代码静态呈现。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `82fc2c66db147ae2ec23076a04a50fffee59fcea2b3138c67437c5765f4298c4` |
| 包名 / 年份 | `dev.cena.whyiamhere` / 2025-2026 |
| 家族 / 品类 | **专注自律与防沉迷管控**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/dev.cena.whyiamhere_7.apk |
| 桌面显示名 | Why am I here? |
| 引导页宣称品牌/身份 | Why am I here?（F-Droid 开源专注自律工具，开发者 cena） |
| 系统无障碍列表服务名 | Why am I here? |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `dev.cena.whyiamhere.WhyService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | Asks for a goal when you open selected apps, reminds you of the time, and returns to the home screen when the session ends. Uses the package name of the active window. Screen text, passwords, and messages are not stored or transmitted. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | dev.cena.whyiamhere.SettingsActivity（唯一 LAUNCHER Activity，Jetpack Compose 设置主页） | 用户点击桌面图标，Activity.onCreate | 原生Activity | **原文**：Open apps with a purpose. Make time for what matters.<br>**译注**：带着目的去打开应用。把时间留给重要的事。 | 无强制操作；可自由浏览设置项，无弹窗、无定时跳转、无取消/跳过语义需求 | `dev.cena.whyiamhere.SettingsActivity#onCreate + strings.xml/settings_intro` |
| 2 | 业务功能触发 | SettingsActivity 内“Accessibility service”分区（service_title 区块） | 用户滚动至无障碍分区 / Activity.onResume 时刷新状态 | 原生Activity | **原文**：The service detects the open app, shows your goal, and returns home when time runs out. Your data stays on your phone. Text inside other apps is not read.<br>**译注**：该服务检测当前打开的应用，展示你的目标，并在时间用尽时返回桌面。你的数据留在手机上。不会读取其他应用内的文字。 | 阅读说明，自行决定是否点击“Open service settings”；未开启时界面显示 Disabled — the goal form and widget are not active | `dev.cena.whyiamhere.SettingsActivity#onResume + strings.xml/service_explanation, service_disabled` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 用户点击按钮（对应字符串 open_service_settings）后触发 od.a() | 系统无障碍页 | **原文**：Open service settings<br>**译注**：打开服务设置 | 用户在系统无障碍列表中手动找到“Why am I here?”并开启；系统页本身提供返回，无应用侧强制 | `od.a() -> new Intent("android.settings.ACCESSIBILITY_SETTINGS").startActivity + strings.xml/open_service_settings` |
| 4 | 引导说明页 | SettingsActivity 无障碍分区内的静态提示文本（同一 Compose 页面，无独立弹窗） | 页面渲染即显示，无交互触发 | 原生Activity | **原文**：Android 13+: if the switch is unavailable, open App info → ⋮ → Allow restricted settings. Names may differ on your phone.<br>**译注**：Android 13+：若开关不可用，请打开应用信息 → ⋮ → 允许受限设置。你手机上的名称可能不同。 | 仅文字告知，不自动拉起 App info 页面、无分步图文引导、无安装器绕过；用户可忽略 | `strings.xml/restricted_settings_help` |
| 5 | 拒权反馈循环 | SettingsActivity 回到前台（onResume 重新查询 AccessibilityManager） | 从系统设置返回触发的 Activity.onResume | 原生Activity | **原文**：Enabled but not connected. Turn the service off and on again in Android settings.<br>**译注**：已启用但未连接。请在 Android 设置中关闭再重新开启该服务。 | 仅状态文本与建议，不自动重跳设置页、无循环拉起；用户可永久不授权继续使用设置页 | `dev.cena.whyiamhere.SettingsActivity#onResume + strings.xml/service_disconnected` |
| 6 | 获权后动作 | dev.cena.whyiamhere.WhyService.onServiceConnected | 系统绑定无障碍服务后回调 onServiceConnected | 不可静态还原 | 无 | 无 | `dev.cena.whyiamhere.WhyService#onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项描述：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_description（"Asks for a goal when you open selected apps... Screen text, passwords, and messages are not stored or transmitted."）
- 应用自有设置页（SettingsActivity，Jetpack Compose 原生界面）的“Accessibility service”分区：service_title / service_explanation / service_disabled / service_running / service_disconnected / restricted_settings_help
- 同一设置页内的按钮文字：open_service_settings（"Open service settings"）
- 同一设置页的省电提示：battery_help（"If the service stops working, allow autostart and remove battery restrictions in your phone settings."）
- 跳转失败时的降级提示：error_service_settings（"Open Accessibility manually in Android settings."）
- 不存在的位置：无 AlertDialog 弹窗、无 WebView 本地/远端 HTML、无悬浮窗遮罩、无通知栏引导、无高仿系统开关页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Asks for a goal when you open selected apps, reminds you of the time, and returns to the home screen when the session ends. Uses the package name of the active window. Screen text, passwords, and messages are not stored or transmitted. | 在你打开选定应用时询问你的目标，提醒剩余时间，并在会话结束时返回桌面。使用当前活动窗口的包名。不存储也不传输屏幕文本、密码和消息。 | `res/values/strings.xml: accessibility_description（经 res/xml/accessibility_service_config.xml 引用为 android:description）` | 隐私承诺 |
| en | The service detects the open app, shows your goal, and returns home when time runs out. Your data stays on your phone. Text inside other apps is not read. | 该服务检测当前打开的应用，展示你的目标，并在时间用尽时返回桌面。你的数据留在手机上。不会读取其他应用内的文字。 | `res/values/strings.xml: service_explanation` | 良性透明说明 |
| en | Android 13+: if the switch is unavailable, open App info → ⋮ → Allow restricted settings. Names may differ on your phone. | Android 13+：若开关不可用，请打开应用信息 → ⋮ → 允许受限设置。你手机上的名称可能不同。 | `res/values/strings.xml: restricted_settings_help` | 受限设置分步教学 |
| en | Disabled — the goal form and widget are not active | 已禁用 —— 目标填写表单与小组件不生效 | `res/values/strings.xml: service_disabled` | 良性透明说明 |
| en | Enabled but not connected. Turn the service off and on again in Android settings. | 已启用但未连接。请在 Android 设置中关闭再重新开启该服务。 | `res/values/strings.xml: service_disconnected` | 良性透明说明 |
| en | If the service stops working, allow autostart and remove battery restrictions in your phone settings. | 如果服务停止工作，请在手机设置中允许自启动并解除电池限制。 | `res/values/strings.xml: battery_help` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环：从系统设置返回仅触发 SettingsActivity.onResume 重新读取 AccessibilityManager 状态并更新 Compose 状态文本（Disabled / Enabled but not connected / Running），不自动重新 startActivity，无定时器重复拉起；用户可永久不授权，应用保持 settings 页可用。
- **遮罩叠层 / 高仿系统设置页**：无。无 SYSTEM_ALERT_WINDOW 权限、无悬浮窗/遮罩代码、无仿系统开关页，跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：仅有一句静态说明文字（restricted_settings_help："Android 13+: if the switch is unavailable, open App info → ⋮ → Allow restricted settings."），不自动拉起 App info、无分步图文引导、无 Session 安装器绕过，且明确提示“名称可能不同”，属合规告知。
- **获权后即时行为与防撤权机制**：无。WhyService.onServiceConnected 仅初始化窗口过滤与注册 SCREEN_OFF/USER_PRESENT 广播；PERFORM_GLOBAL_ACTION 用于到时返回桌面（业务行为），未见监听设置页自点确认或 GLOBAL_ACTION_BACK 阻止撤权。
- **良性降级 / 替代方案**：服务未开启时设置页明确显示 service_disabled（目标表单与小组件不生效），用户仍可配置应用列表/时长/警告；跳转失败时降级提示 error_service_settings 引导手动进入系统设置。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的前一帧（用户点击“Open service settings”时），或冷启动后停留在 SettingsActivity 无障碍分区时；本应用无冷启动自动跳转，因此纯冷启动监测不会命中诱导行为。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：应用无 INTERNET 权限、无 WebView、无悬浮窗、无动态加载，运行期 UI 与静态资源一致。唯一需注意的是“诱导强度弱”——纯冷启动监测可能完全无信号，须以 ACCESSIBILITY_SETTINGS 跳转事件或设置页无障碍分区作为触发点。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **应用自有设置页的无障碍分区（跳转前唯一说明位置）** | dev.cena.whyiamhere.SettingsActivity，含标题“Accessibility service”、按钮“Open service settings”、状态行“Running/Disabled/Enabled but not connected” | 该页是全部权限话术的唯一载体；若存在伪装或恐吓，必然出现在此处的文本与按钮组合中 | 是否存在不可取消弹窗或遮罩层覆盖该页；按钮文字是否为“立即开启/修复/更新”等诱导措辞而非“Open service settings”；状态行是否使用故障恐吓措辞；是否存在图文分步引导或伪造系统开关控件 |
| **系统无障碍服务列表项（授权目标页）** | 系统 Settings 中“Why am I here?”服务条目及其描述文字 | 验证服务标签与描述是否与桌面名一致、是否为隐私承诺型透明声明，可排除同形字/空白挤出与仿冒 | 服务名是否与 app_name 完全一致；描述是否与 accessibility_description 原文一致（含“not stored or transmitted”）；是否存在同一包下多个无障碍服务条目 |
| **从系统设置返回后的设置页状态** | SettingsActivity onResume 后状态文本（Disabled / Enabled but not connected / Running） | 判定是否存在拒权后的死循环重跳或压迫式反馈，是本应用与恶意样本最关键的区分点 | 返回后是否立即再次跳转系统设置页；是否出现叠加遮罩或全屏不可关闭引导；状态文本是否为中性事实描述 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `dev.cena.whyiamhere.SettingsActivity#onResume`
- `dev.cena.whyiamhere.SettingsActivity#onCreate`
- `od#a（Intent android.settings.ACCESSIBILITY_SETTINGS + startActivity）`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml（accessibility_description / service_explanation / restricted_settings_help / open_service_settings）`
- `dev.cena.whyiamhere.WhyService#onServiceConnected`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态核验已完成）

**核心事实链（共 9 次工具调用，没有遇到加壳或密文载荷，因此静态完全可见）**

1. **没有“诱导”式冷启动拦截**：唯一 LAUNCHER 入口是 [SettingsActivity](<resource-unit:#1.dex1 code:dev.cena.whyiamhere.SettingsActivity>)，`onCreate` 只做 `setContent`（Compose）。冷启动时既不弹权限弹窗，也不强制跳转，更不用定时器轮询。`GateActivity` 是防沉迷业务中的“目标填写页”，不是权限页。
2. **权限状态是“读取并展示”，不是“索取”**：`SettingsActivity.onResume` 通过 `AccessibilityManager.getEnabledAccessibilityServiceList(-1)` 遍历，比对 `serviceInfo.packageName == getPackageName()` 且 `serviceInfo.name == WhyService.class.getName()`，把结果写入 `MutableStateFlow<Boolean>` 驱动界面状态文本（Running / Disabled / Enabled but not connected）。回到本页即刷新，没有自动重新跳转。
3. **跳转点只有一个且是用户主动点击**：`od.a()` 构造 `new Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `startActivity`，仅在用户点击“Open service settings”按钮时执行；`startActivity` 抛出异常时降级为提示（`error_service_settings` = "Open Accessibility manually in Android settings."）。全 DEX 中**不存在** `ACTION_APPLICATION_DETAILS_SETTINGS`，也没有 `isAccessibilityTool` 伪造。
4. **没有遮罩、悬浮窗、WebView 或高仿真开关页**：无 `SYSTEM_ALERT_WINDOW` 权限，无 WebView 组件，`overlay=[]` 与代码一致；无多 activity-alias，服务 `android:label="@string/app_name"` 与桌面名完全一致，无空白或同形字伪装。
5. **受限设置（Android 13+）属于“说明性文字”而非分步弹窗引导**：`restricted_settings_help` 仅在设置页以静态说明文字呈现，无图文分步、无自动拉起 App info、无 Session 安装器绕过。
6. **无网络能力**：`uses-permission` 只有自签名动态广播权限，**无 `INTERNET`**，故不存在云控下发或远端 HTML 教学页的可能；`PERFORM_GLOBAL_ACTION` 服务于业务（到时 `GLOBAL_ACTION_HOME` 回桌面），`WATCH_PKG_INSTALLER`/包名监听服务于“已选应用被卸载”提示，与撤权反制无关。
7. **降级路径透明**：服务未开启时应用明确显示 `service_disabled`（"goal form and widget are not active"），用户可以永久不授权而仅使用设置页，构成显式可选退路。

**判定**：符合“良性透明说明”范式——权限说明以本地 `strings.xml` 资源呈现于应用自有设置页，无障碍 `android:description` 主动声明“不存储不传输屏幕文本/密码/消息”，身份、范围与代码实现一致。未发现诱导、恐吓、遮罩压迫或拒权循环。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全量静态可见：无加壳（预筛 False 且 apkid 特征未见）、无加密载荷、无动态加载 dex、无 WebView/远端 HTML、无 INTERNET 权限，引导流程全部由 res/values/strings.xml 与 Compose 代码静态呈现。",
  "summary_one_liner": "该应用在自有设置页以静态说明文字+状态指示呈现无障碍服务用途，仅由用户主动点击“Open service settings”跳转系统无障碍列表，回页后读取状态刷新，无弹窗胁迫、无遮罩、无拒权循环。",
  "disguise_identity": {
    "app_display_name": "Why am I here?",
    "claimed_brand_or_persona": "Why am I here?（F-Droid 开源专注自律工具，开发者 cena）",
    "a11y_service_label": "Why am I here?",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "dev.cena.whyiamhere.SettingsActivity（唯一 LAUNCHER Activity，Jetpack Compose 设置主页）",
      "trigger_event": "用户点击桌面图标，Activity.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Open apps with a purpose. Make time for what matters.",
      "shown_text_zh": "带着目的去打开应用。把时间留给重要的事。",
      "user_action_requested": "无强制操作；可自由浏览设置项，无弹窗、无定时跳转、无取消/跳过语义需求",
      "code_anchor": "dev.cena.whyiamhere.SettingsActivity#onCreate + strings.xml/settings_intro"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "SettingsActivity 内“Accessibility service”分区（service_title 区块）",
      "trigger_event": "用户滚动至无障碍分区 / Activity.onResume 时刷新状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "The service detects the open app, shows your goal, and returns home when time runs out. Your data stays on your phone. Text inside other apps is not read.",
      "shown_text_zh": "该服务检测当前打开的应用，展示你的目标，并在时间用尽时返回桌面。你的数据留在手机上。不会读取其他应用内的文字。",
      "user_action_requested": "阅读说明，自行决定是否点击“Open service settings”；未开启时界面显示 Disabled — the goal form and widget are not active",
      "code_anchor": "dev.cena.whyiamhere.SettingsActivity#onResume + strings.xml/service_explanation, service_disabled"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户点击按钮（对应字符串 open_service_settings）后触发 od.a()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Open service settings",
      "shown_text_zh": "打开服务设置",
      "user_action_requested": "用户在系统无障碍列表中手动找到“Why am I here?”并开启；系统页本身提供返回，无应用侧强制",
      "code_anchor": "od.a() -> new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").startActivity + strings.xml/open_service_settings"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "SettingsActivity 无障碍分区内的静态提示文本（同一 Compose 页面，无独立弹窗）",
      "trigger_event": "页面渲染即显示，无交互触发",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Android 13+: if the switch is unavailable, open App info → ⋮ → Allow restricted settings. Names may differ on your phone.",
      "shown_text_zh": "Android 13+：若开关不可用，请打开应用信息 → ⋮ → 允许受限设置。你手机上的名称可能不同。",
      "user_action_requested": "仅文字告知，不自动拉起 App info 页面、无分步图文引导、无安装器绕过；用户可忽略",
      "code_anchor": "strings.xml/restricted_settings_help"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "SettingsActivity 回到前台（onResume 重新查询 AccessibilityManager）",
      "trigger_event": "从系统设置返回触发的 Activity.onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Enabled but not connected. Turn the service off and on again in Android settings.",
      "shown_text_zh": "已启用但未连接。请在 Android 设置中关闭再重新开启该服务。",
      "user_action_requested": "仅状态文本与建议，不自动重跳设置页、无循环拉起；用户可永久不授权继续使用设置页",
      "code_anchor": "dev.cena.whyiamhere.SettingsActivity#onResume + strings.xml/service_disconnected"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "dev.cena.whyiamhere.WhyService.onServiceConnected",
      "trigger_event": "系统绑定无障碍服务后回调 onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面呈现；仅注册 SCREEN_OFF/USER_PRESENT 广播接收器并初始化窗口过滤，无自点确认、无阻止撤权动作",
      "user_action_requested": "无",
      "code_anchor": "dev.cena.whyiamhere.WhyService#onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项描述：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_description（\"Asks for a goal when you open selected apps... Screen text, passwords, and messages are not stored or transmitted.\"）",
    "应用自有设置页（SettingsActivity，Jetpack Compose 原生界面）的“Accessibility service”分区：service_title / service_explanation / service_disabled / service_running / service_disconnected / restricted_settings_help",
    "同一设置页内的按钮文字：open_service_settings（\"Open service settings\"）",
    "同一设置页的省电提示：battery_help（\"If the service stops working, allow autostart and remove battery restrictions in your phone settings.\"）",
    "跳转失败时的降级提示：error_service_settings（\"Open Accessibility manually in Android settings.\"）",
    "不存在的位置：无 AlertDialog 弹窗、无 WebView 本地/远端 HTML、无悬浮窗遮罩、无通知栏引导、无高仿系统开关页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Asks for a goal when you open selected apps, reminds you of the time, and returns to the home screen when the session ends. Uses the package name of the active window. Screen text, passwords, and messages are not stored or transmitted.",
      "text_zh": "在你打开选定应用时询问你的目标，提醒剩余时间，并在会话结束时返回桌面。使用当前活动窗口的包名。不存储也不传输屏幕文本、密码和消息。",
      "source_location": "res/values/strings.xml: accessibility_description（经 res/xml/accessibility_service_config.xml 引用为 android:description）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "The service detects the open app, shows your goal, and returns home when time runs out. Your data stays on your phone. Text inside other apps is not read.",
      "text_zh": "该服务检测当前打开的应用，展示你的目标，并在时间用尽时返回桌面。你的数据留在手机上。不会读取其他应用内的文字。",
      "source_location": "res/values/strings.xml: service_explanation",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Android 13+: if the switch is unavailable, open App info → ⋮ → Allow restricted settings. Names may differ on your phone.",
      "text_zh": "Android 13+：若开关不可用，请打开应用信息 → ⋮ → 允许受限设置。你手机上的名称可能不同。",
      "source_location": "res/values/strings.xml: restricted_settings_help",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Disabled — the goal form and widget are not active",
      "text_zh": "已禁用 —— 目标填写表单与小组件不生效",
      "source_location": "res/values/strings.xml: service_disabled",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enabled but not connected. Turn the service off and on again in Android settings.",
      "text_zh": "已启用但未连接。请在 Android 设置中关闭再重新开启该服务。",
      "source_location": "res/values/strings.xml: service_disconnected",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "If the service stops working, allow autostart and remove battery restrictions in your phone settings.",
      "text_zh": "如果服务停止工作，请在手机设置中允许自启动并解除电池限制。",
      "source_location": "res/values/strings.xml: battery_help",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环：从系统设置返回仅触发 SettingsActivity.onResume 重新读取 AccessibilityManager 状态并更新 Compose 状态文本（Disabled / Enabled but not connected / Running），不自动重新 startActivity，无定时器重复拉起；用户可永久不授权，应用保持 settings 页可用。",
    "overlay_or_fake_settings": "无。无 SYSTEM_ALERT_WINDOW 权限、无悬浮窗/遮罩代码、无仿系统开关页，跳转目标为真实 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "仅有一句静态说明文字（restricted_settings_help：\"Android 13+: if the switch is unavailable, open App info → ⋮ → Allow restricted settings.\"），不自动拉起 App info、无分步图文引导、无 Session 安装器绕过，且明确提示“名称可能不同”，属合规告知。",
    "post_grant_anti_removal": "无。WhyService.onServiceConnected 仅初始化窗口过滤与注册 SCREEN_OFF/USER_PRESENT 广播；PERFORM_GLOBAL_ACTION 用于到时返回桌面（业务行为），未见监听设置页自点确认或 GLOBAL_ACTION_BACK 阻止撤权。",
    "benign_graceful_degradation": "服务未开启时设置页明确显示 service_disabled（目标表单与小组件不生效），用户仍可配置应用列表/时长/警告；跳转失败时降级提示 error_service_settings 引导手动进入系统设置。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的前一帧（用户点击“Open service settings”时），或冷启动后停留在 SettingsActivity 无障碍分区时；本应用无冷启动自动跳转，因此纯冷启动监测不会命中诱导行为。",
    "key_pages_to_capture": [
      {
        "page_role": "应用自有设置页的无障碍分区（跳转前唯一说明位置）",
        "page_identifier": "dev.cena.whyiamhere.SettingsActivity，含标题“Accessibility service”、按钮“Open service settings”、状态行“Running/Disabled/Enabled but not connected”",
        "why_most_useful": "该页是全部权限话术的唯一载体；若存在伪装或恐吓，必然出现在此处的文本与按钮组合中",
        "observable_utg_signals": ["是否存在不可取消弹窗或遮罩层覆盖该页", "按钮文字是否为“立即开启/修复/更新”等诱导措辞而非“Open service settings”", "状态行是否使用故障恐吓措辞", "是否存在图文分步引导或伪造系统开关控件"]
      },
      {
        "page_role": "系统无障碍服务列表项（授权目标页）",
        "page_identifier": "系统 Settings 中“Why am I here?”服务条目及其描述文字",
        "why_most_useful": "验证服务标签与描述是否与桌面名一致、是否为隐私承诺型透明声明，可排除同形字/空白挤出与仿冒",
        "observable_utg_signals": ["服务名是否与 app_name 完全一致", "描述是否与 accessibility_description 原文一致（含“not stored or transmitted”）", "是否存在同一包下多个无障碍服务条目"]
      },
      {
        "page_role": "从系统设置返回后的设置页状态",
        "page_identifier": "SettingsActivity onResume 后状态文本（Disabled / Enabled but not connected / Running）",
        "why_most_useful": "判定是否存在拒权后的死循环重跳或压迫式反馈，是本应用与恶意样本最关键的区分点",
        "observable_utg_signals": ["返回后是否立即再次跳转系统设置页", "是否出现叠加遮罩或全屏不可关闭引导", "状态文本是否为中性事实描述"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：应用无 INTERNET 权限、无 WebView、无悬浮窗、无动态加载，运行期 UI 与静态资源一致。唯一需注意的是“诱导强度弱”——纯冷启动监测可能完全无信号，须以 ACCESSIBILITY_SETTINGS 跳转事件或设置页无障碍分区作为触发点。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "dev.cena.whyiamhere.SettingsActivity#onResume",
    "dev.cena.whyiamhere.SettingsActivity#onCreate",
    "od#a（Intent android.settings.ACCESSIBILITY_SETTINGS + startActivity）",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml（accessibility_description / service_explanation / restricted_settings_help / open_service_settings）",
    "dev.cena.whyiamhere.WhyService#onServiceConnected"
  ]
}
```

</details>
