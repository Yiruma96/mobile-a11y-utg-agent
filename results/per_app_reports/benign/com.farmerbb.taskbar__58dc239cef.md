# BN_044__58dc239cef｜系统效率与通用辅助 — Taskbar

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：156.9s

## 1. 一句话核心结论

- **核心申请方式**：Taskbar 在用户启用按键/电源菜单等依赖无障碍的功能时，用原生 AlertDialog 如实说明无障碍用途并提供 Cancel/Activate，点 Activate 仅跳转系统 ACCESSIBILITY_SETTINGS 由用户自行开启，属透明、可取消、按需触发的良性引导。
- **静态可见性说明**：无障碍引导链完整静态可见：DummyActivity 弹窗文案取自 res/values/strings.xml（tb_permission_dialog_title / tb_enable_accessibility=tb_accessibility_service_description / tb_action_cancel / tb_action_activate），跳转为硬编码 Intent("android.settings.ACCESSIBILITY_SETTINGS")；无加壳、无加密载荷、无远端 HTML、无 assets 引导页。未核验部分仅限 TouchAbsorberActivity 的 GLOBAL_ACTION 细节，与本专题无关。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `58dc239cef19f05b527335e7b723dd3dfd1d8bb651a50ecc0f52402796e509d9` |
| 包名 / 年份 | `com.farmerbb.taskbar` / 2025-2026 |
| 家族 / 品类 | **系统效率与通用辅助**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.farmerbb.taskbar_208.apk |
| 桌面显示名 | Taskbar |
| 引导页宣称品牌/身份 | Taskbar（开源桌面任务栏/多窗口辅助，包名 com.farmerbb.taskbar） |
| 系统无障碍列表服务名 | Allows Taskbar to perform button press actions（系统无障碍列表 summary，服务类 com.farmerbb.taskbar.service.PowerMenuService） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅存在一个常规 activity-alias（com.farmerbb.taskbar.MainActivity → com.farmerbb.taskbar.activity.MainActivity）用于暴露 LAUNCHER 入口，非伪装；无空白/换行挤出、无同形字、无伪造 isAccessibilityTool（DEX 无该符号）。 |
| 无障碍服务类名 | `com.farmerbb.taskbar.service.PowerMenuService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Taskbar needs to be activated as an accessibility service in order to perform button press actions such as back, home, recents, and power, as well as displaying the notification tray.<br><br>This permission is used only to perform button press actions, and for no other purpose. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.farmerbb.taskbar.util.g0（静态工具类，由 ContextMenuActivity.onPreferenceClick / c0.w0.W0 / TouchAbsorberActivity.f 等调用） | 用户点击电源菜单、返回/主页/最近任务等按键动作项，或启动器需按键能力时调用 g0.n2(context, action, runnable) | 无界面（后台判定） | 无 | 无 | `com.farmerbb.taskbar.util.g0#n2` |
| 2 | 业务功能触发 | com.farmerbb.taskbar.util.g0#Q0 读取 Settings.Secure.enabled_accessibility_services | n2 中先 q2(context, PowerMenuService.class, true) 启用组件，再 Q0 判断 PowerMenuService 是否已出现在系统已启用无障碍服务列表 | 无界面（系统设置读取） | 无 | 无 | `com.farmerbb.taskbar.util.g0#Q0 / #q2` |
| 3 | 引导说明页 | com.farmerbb.taskbar.activity.DummyActivity（theme Taskbar.Incognito，excludeFromRecents，无可见布局：setContentView(new View(this))）+ 不可取消风格的 AlertDialog | 未启用无障碍且无 WRITE_SECURE_SETTINGS（N0()==false）→ g0.T1(context, Q) → g0.U1 处理悬浮窗权限后执行 Q.run → g0.I1 以 extra "accessibility"=true、FLAG_ACTIVITY_NEW_TASK\|CLEAR_TASK 拉起 DummyActivity，onResume 命中 hasExtra("accessibility") 弹出对话框 | 原生Dialog | **原文**：Permission needed / Taskbar needs to be activated as an accessibility service in order to perform button press actions such as back, home, recents, and power, as well as displaying the notification tray.<br><br>This permission is used only to perform button press actions, and for no other purpose. / Cancel / Activate<br>**译注**：标题“需要权限”；正文“Taskbar 需要被激活为无障碍服务，才能执行返回、主页、最近任务、电源等按键动作，以及显示通知栏。该权限仅用于执行按键动作，不作其他任何用途。”；按钮“取消”“激活” | 可点 Cancel（关闭对话框、功能降级不启用）或 Activate（跳转系统无障碍设置）；对话框 create 后调用 setCancelable(false)，但保留显式 Cancel 按钮，非强制单向路径 | `com.farmerbb.taskbar.activity.DummyActivity#onResume（R$string.h1=Permission needed, R$string.a0=tb_enable_accessibility, R$string.b=tb_action_cancel, R$string.a=tb_action_activate）` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 用户点 Activate → DialogInterface.OnClickListener（DummyActivity.f）先 g0.T1 再校验 disable_animations 后 addFlags(FLAG_ACTIVITY_NO_ANIMATION) 启动 Intent | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：系统“无障碍”设置页，用户在列表中自行找到 Taskbar 并开启 | 用户自行在系统无障碍列表中选择 Taskbar（Allows Taskbar to perform button press actions）并开启；应用不提供绕过系统开关的手段 | `com.farmerbb.taskbar.activity.DummyActivity#f` |
| 5 | 获权后动作 | com.farmerbb.taskbar.service.PowerMenuService（AccessibilityService） | 用户在系统页开启后，应用侧 Q0() 重新读 enabled_accessibility_services 返回 true，n2 直接发送 Intent("com.farmerbb.taskbar.ACCESSIBILITY_ACTION") 携带 action 执行按键动作 | 无界面（服务内执行） | **原文**：com.farmerbb.taskbar.ACCESSIBILITY_ACTION<br>**译注**：通过自定义广播 + AccessibilityService 执行返回/主页/最近任务/电源等全局动作，并读取通知栏内容用于展示通知托盘 | 无；不监听设置页、不自动点击确认、不阻止撤权 | `com.farmerbb.taskbar.util.g0#n2 / com.farmerbb.taskbar.util.g0#H1 / com.farmerbb.taskbar.service.PowerMenuService` |
| 6 | 业务功能触发 | com.farmerbb.taskbar.activity.EnableAdditionalSettingsActivity（可选提权页，主题 Taskbar.Dialog） | 用户在设置中点击“Enable additional settings”偏好项（Y.l.onPreferenceClick） | 原生Activity | **原文**：Taskbar can optionally use elevated permissions to improve your desktop mode experience. These permissions are granted by running an adb shell command. … adb shell pm grant %1$s %2$s<br>**译注**：可选提升权限说明页：明确告知需自行在电脑上执行 adb shell pm grant <包名> android.permission.WRITE_SECURE_SETTINGS，获权后应用可在连接显示器时直写 secure settings（含自动把自身加入 enabled_accessibility_services） | 用户自行决定是否用 ADB 授权；无诱导、无绕过系统无障碍开关的隐蔽自授权（无该权限时一律回退到弹窗引导） | `com.farmerbb.taskbar.activity.EnableAdditionalSettingsActivity#u0 / res/values/strings.xml tb_enable_additional_settings_message_1` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项说明：res/xml/tb_accessibility_service.xml 引用 @string/tb_accessibility_service_description（android:description）与 @string/tb_accessibility_service_summary（android:summary）
- DummyActivity 原生 AlertDialog：标题 tb_permission_dialog_title（Permission needed），正文 tb_enable_accessibility → 指向 tb_accessibility_service_description 全文，按钮 tb_action_cancel / tb_action_activate（strings.xml 第 98-105、257 行）
- 可选提权说明页 EnableAdditionalSettingsActivity：标题 tb_enable_additional_settings、正文 tb_enable_additional_settings_message_1/_2、命令模板 tb_adb_shell_command（strings.xml 第 121、258-262 行）
- 悬浮窗权限引导（非无障碍）：tb_permission_dialog_message / tb_permission_dialog_instructions_phone|tv（strings.xml 第 406-411 行），由 g0.A2 / g0.C2 弹出
- 未发现任何 WebView、assets HTML、远端页面或悬浮窗遮罩形式的无障碍引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Taskbar needs to be activated as an accessibility service in order to perform button press actions such as back, home, recents, and power, as well as displaying the notification tray.<br><br>This permission is used only to perform button press actions, and for no other purpose. | Taskbar 需要被激活为无障碍服务，才能执行返回、主页、最近任务、电源等按键动作，以及显示通知栏。该权限仅用于执行按键动作，不作其他任何用途。 | `res/values/strings.xml key=tb_accessibility_service_description（第 98-100 行），经 tb_enable_accessibility 复用为弹窗正文；同时用于 res/xml/tb_accessibility_service.xml android:description` | 良性透明说明 |
| en | Allows Taskbar to perform button press actions | 允许 Taskbar 执行按键动作 | `res/values/strings.xml key=tb_accessibility_service_summary（第 101 行）` | 良性透明说明 |
| en | Permission needed | 需要权限 | `res/values/strings.xml key=tb_permission_dialog_title（第 411 行），DummyActivity 弹窗标题 R$string.h1` | 良性透明说明 |
| en | Cancel / Activate | 取消 / 激活 | `res/values/strings.xml key=tb_action_cancel、tb_action_activate（第 102-103 行）` | 良性透明说明 |
| en | Taskbar can optionally use elevated permissions to improve your desktop mode experience. These permissions are granted by running an adb shell command. | Taskbar 可选择性地使用提权来改善桌面模式体验。这些权限需通过运行 adb shell 命令授予。 | `res/values/strings.xml key=tb_enable_additional_settings_message_1（第 259-261 行）` | 良性透明说明 |
| en | adb shell pm grant %1$s %2$s | adb shell pm grant <包名> <权限名> | `res/values/strings.xml key=tb_adb_shell_command（第 121 行），EnableAdditionalSettingsActivity#u0 填入 getPackageName() 与 android.permission.WRITE_SECURE_SETTINGS` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性安全降级：点 Cancel 由 DialogInterface.OnClickListener（DummyActivity.w）关闭弹窗并结束 InvisibleActivity 流程，不会 onResume 死循环重跳；仅当用户再次触发依赖按键功能时才会重新出现该弹窗。U1 中通过 SharedPreferences 的 disable_animations 与延时策略避免高频重复弹窗。
- **遮罩叠层 / 高仿系统设置页**：无。未叠放半透明引导遮罩，未实现高仿系统无障碍开关页；引导仅为一个原生 AlertDialog + 系统无障碍页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。无 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、无“点右上角菜单允许受限设置”教学、无 Session 安装器绕过；相关字符串仅为 ADB 提权的可选项说明。
- **获权后即时行为与防撤权机制**：无。未监听无障碍设置页，未用 GLOBAL_ACTION_BACK/HOME 阻止撤权，未自动点击确认。Q0/H1 直写 enabled_accessibility_services 仅在用户已通过 ADB 授予 WRITE_SECURE_SETTINGS 时生效，属公开说明的可选路径。
- **良性降级 / 替代方案**：有。无无障碍权限时按键类功能（返回/主页/最近任务/电源、通知托盘）不可用，其余桌面任务栏、多窗口、应用抽屉等功能不受影响；用户可 Cancel 继续使用，或按设置页指引通过 ADB 授权 WRITE_SECURE_SETTINGS 作为替代路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以系统无障碍页拉起为锚：监测 Activity 栈顶变为 com.android.settings/.Settings$AccessibilitySettings（或任何 Settings 子页）时立即抓取上一层栈快照；同时在该时刻回溯最近 1 秒内是否有 com.farmerbb.taskbar/.activity.DummyActivity 的 onCreate/onResume，以捕获“弹窗→跳转”配对。也可在 DummyActivity 出现时（主题 Incognito、excludeFromRecents、界面近乎空白）直接抓 UTG。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导全程为纯文本原生控件，UTG 可直接提取。需注意 DummyActivity 采用近乎空白的 Incognito 主题且 excludeFromRecents，单纯以“空白页”为恶意特征会误报；另应用未声明 android:isAccessibilityTool，系统可能显示“此服务可查看屏幕内容”类提示，属平台默认提示而非应用伪造。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前的原生引导弹窗页** | com.farmerbb.taskbar/.activity.DummyActivity 上的 AlertDialog：标题 Permission needed，正文含 “Taskbar needs to be activated as an accessibility service…”，按钮 Cancel / Activate | 该弹窗是本应用唯一的无障碍用途声明点，可直接比对正文所述范围（仅按键动作）与后续实际行为是否一致，判断是否为误导性说明 | dialog title = Permission needed；dialog message 含 accessibility service 与 for no other purpose 字样；button text Cancel / Activate 同时存在（可取消性）；宿主 Activity 无可见布局内容（setContentView(new View)） |
| **系统无障碍服务列表项** | Settings 无障碍页列表中出现 Taskbar / Allows Taskbar to perform button press actions | 确认应用是否如实以自身名称与 summary 出现在系统列表，而非伪装成系统组件或空白项 | 列表项文本 = Taskbar；summary = Allows Taskbar to perform button press actions；service component = com.farmerbb.taskbar/.service.PowerMenuService |
| **可选提权说明页（ADB）** | com.farmerbb.taskbar/.activity.EnableAdditionalSettingsActivity 弹窗式页面，含 adb shell pm grant 命令文本 | 区分“公开 ADB 提权说明”与“诱导绕过受限设置”的关键页面，确认无 ACTION_APPLICATION_DETAILS_SETTINGS 教学 | 正文含 adb shell pm grant 与 android.permission.WRITE_SECURE_SETTINGS；无“允许受限设置”字样；按钮为关闭/复制类，非跳转应用详情 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.farmerbb.taskbar.util.g0#n2`
- `com.farmerbb.taskbar.util.g0#I1`
- `com.farmerbb.taskbar.activity.DummyActivity#onResume`
- `com.farmerbb.taskbar.activity.DummyActivity#f`
- `res/xml/tb_accessibility_service.xml`
- `res/values/strings.xml（tb_accessibility_service_description / tb_permission_dialog_title / tb_action_cancel / tb_action_activate）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（静态可见性：clear）

**1. 不存在无障碍引导遮罩、假设置页或拒权死循环。** 全部引导由原生 `AlertDialog` 与 `strings.xml` 文案构成，无 WebView、无 assets HTML、无远端页面、无悬浮窗叠层（`overlay=[]` 与代码一致）。

**2. 触发方式是按需触发（user_feature_on_demand），不是冷启动强制。** 决策点在 [g0.n2()](<resource-unit:#1.dex1 code:com.farmerbb.taskbar.util.g0#n2>)：先 `setComponentEnabledSetting` 启用 `PowerMenuService`，再用 [g0.Q0()](<resource-unit:#1.dex1 code:com.farmerbb.taskbar.util.g0#Q0>) 读取 `Settings.Secure.enabled_accessibility_services` 判断服务是否已在系统无障碍列表中启用。未启用且无 `WRITE_SECURE_SETTINGS` 时，走 `T1 → U1`（先处理悬浮窗权限）后由 [g0.I1()](<resource-unit:#1.dex1 code:com.farmerbb.taskbar.util.g0#I1>) 带 `extra: accessibility=true` 拉起 `DummyActivity`。

**3. 引导弹窗内容如实说明用途，并有“Cancel”。** [DummyActivity.onResume()](<resource-unit:#1.dex1 code:com.farmerbb.taskbar.activity.DummyActivity#onResume>) 在 `hasExtra("accessibility")` 时构造 `AlertDialog`：标题 `tb_permission_dialog_title`="Permission needed"，正文 `tb_enable_accessibility` 即无障碍服务 `android:description` 全文（明确写“仅用于按键动作，不作他用”），按钮 `tb_action_cancel`="Cancel" / `tb_action_activate`="Activate"。点 Activate 由 [DummyActivity.f()](<resource-unit:#1.dex1 code:com.farmerbb.taskbar.activity.DummyActivity#f>) 用 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 跳系统页——**唯一跳转点**，且跳转前再次校验悬浮窗权限（`g0.T1`），不存在 `ACTION_APPLICATION_DETAILS_SETTINGS`、无 13+ 受限设置教学（受限设置教学仅出现在可选的 ADB 提权页）。

**4. 一处值得注意但不构成恶意：`enabled_accessibility_services` 直写。** [g0.n2()](<resource-unit:#1.dex1 code:com.farmerbb.taskbar.util.g0#n2>) 与 [g0.H1()](<resource-unit:#1.dex1 code:com.farmerbb.taskbar.util.g0#H1>) 会在 `N0()==true`（即已通过 `adb shell pm grant … WRITE_SECURE_SETTINGS` 获权）时直接改写无障碍服务列表以自动启用自身；无该权限则退回弹窗引导。属公开文档化的可选提权路径（[strings.xml `tb_enable_additional_settings_message_1`](<resource-unit:#1 file:res/values/strings.xml#L259-L261>) 明示需用户自行执行 adb 命令），非隐蔽自授权，也无需用户点“允许”。

**5. 身份一致，无伪装。** 无障碍列表项显示 `@string/tb_accessibility_service_description`，summary“Allows Taskbar to perform button press actions”，服务类 `PowerMenuService`，与 `Taskbar` 桌面任务栏定位一致；`activity-alias` 仅有 `com.farmerbb.taskbar.MainActivity` 一个（开源工程的常规改名），无多别名伪装、无空白挤出、无伪造 `isAccessibilityTool`（DEX 中无该符号）。

**6. 未发现已确认风险，故未登记风险条目。** 覆盖边界：`TouchAbsorberActivity` 的 `GLOBAL_ACTION` 使用属导航栏吸收功能，未做逐帧反编译核验（超出本轮无障碍引导专题）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链完整静态可见：DummyActivity 弹窗文案取自 res/values/strings.xml（tb_permission_dialog_title / tb_enable_accessibility=tb_accessibility_service_description / tb_action_cancel / tb_action_activate），跳转为硬编码 Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")；无加壳、无加密载荷、无远端 HTML、无 assets 引导页。未核验部分仅限 TouchAbsorberActivity 的 GLOBAL_ACTION 细节，与本专题无关。",
  "summary_one_liner": "Taskbar 在用户启用按键/电源菜单等依赖无障碍的功能时，用原生 AlertDialog 如实说明无障碍用途并提供 Cancel/Activate，点 Activate 仅跳转系统 ACCESSIBILITY_SETTINGS 由用户自行开启，属透明、可取消、按需触发的良性引导。",
  "disguise_identity": {
    "app_display_name": "Taskbar",
    "claimed_brand_or_persona": "Taskbar（开源桌面任务栏/多窗口辅助，包名 com.farmerbb.taskbar）",
    "a11y_service_label": "Allows Taskbar to perform button press actions（系统无障碍列表 summary，服务类 com.farmerbb.taskbar.service.PowerMenuService）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅存在一个常规 activity-alias（com.farmerbb.taskbar.MainActivity → com.farmerbb.taskbar.activity.MainActivity）用于暴露 LAUNCHER 入口，非伪装；无空白/换行挤出、无同形字、无伪造 isAccessibilityTool（DEX 无该符号）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.farmerbb.taskbar.util.g0（静态工具类，由 ContextMenuActivity.onPreferenceClick / c0.w0.W0 / TouchAbsorberActivity.f 等调用）",
      "trigger_event": "用户点击电源菜单、返回/主页/最近任务等按键动作项，或启动器需按键能力时调用 g0.n2(context, action, runnable)",
      "ui_carrier": "无界面（后台判定）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，纯逻辑判定",
      "user_action_requested": "无",
      "code_anchor": "com.farmerbb.taskbar.util.g0#n2"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.farmerbb.taskbar.util.g0#Q0 读取 Settings.Secure.enabled_accessibility_services",
      "trigger_event": "n2 中先 q2(context, PowerMenuService.class, true) 启用组件，再 Q0 判断 PowerMenuService 是否已出现在系统已启用无障碍服务列表",
      "ui_carrier": "无界面（系统设置读取）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "读取 enabled_accessibility_services，判断是否包含 com.farmerbb.taskbar/com.farmerbb.taskbar.service.PowerMenuService",
      "user_action_requested": "无",
      "code_anchor": "com.farmerbb.taskbar.util.g0#Q0 / #q2"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.farmerbb.taskbar.activity.DummyActivity（theme Taskbar.Incognito，excludeFromRecents，无可见布局：setContentView(new View(this))）+ 不可取消风格的 AlertDialog",
      "trigger_event": "未启用无障碍且无 WRITE_SECURE_SETTINGS（N0()==false）→ g0.T1(context, Q) → g0.U1 处理悬浮窗权限后执行 Q.run → g0.I1 以 extra \"accessibility\"=true、FLAG_ACTIVITY_NEW_TASK|CLEAR_TASK 拉起 DummyActivity，onResume 命中 hasExtra(\"accessibility\") 弹出对话框",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission needed / Taskbar needs to be activated as an accessibility service in order to perform button press actions such as back, home, recents, and power, as well as displaying the notification tray.\n\nThis permission is used only to perform button press actions, and for no other purpose. / Cancel / Activate",
      "shown_text_zh": "标题“需要权限”；正文“Taskbar 需要被激活为无障碍服务，才能执行返回、主页、最近任务、电源等按键动作，以及显示通知栏。该权限仅用于执行按键动作，不作其他任何用途。”；按钮“取消”“激活”",
      "user_action_requested": "可点 Cancel（关闭对话框、功能降级不启用）或 Activate（跳转系统无障碍设置）；对话框 create 后调用 setCancelable(false)，但保留显式 Cancel 按钮，非强制单向路径",
      "code_anchor": "com.farmerbb.taskbar.activity.DummyActivity#onResume（R$string.h1=Permission needed, R$string.a0=tb_enable_accessibility, R$string.b=tb_action_cancel, R$string.a=tb_action_activate）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户点 Activate → DialogInterface.OnClickListener（DummyActivity.f）先 g0.T1 再校验 disable_animations 后 addFlags(FLAG_ACTIVITY_NO_ANIMATION) 启动 Intent",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "系统“无障碍”设置页，用户在列表中自行找到 Taskbar 并开启",
      "user_action_requested": "用户自行在系统无障碍列表中选择 Taskbar（Allows Taskbar to perform button press actions）并开启；应用不提供绕过系统开关的手段",
      "code_anchor": "com.farmerbb.taskbar.activity.DummyActivity#f"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.farmerbb.taskbar.service.PowerMenuService（AccessibilityService）",
      "trigger_event": "用户在系统页开启后，应用侧 Q0() 重新读 enabled_accessibility_services 返回 true，n2 直接发送 Intent(\"com.farmerbb.taskbar.ACCESSIBILITY_ACTION\") 携带 action 执行按键动作",
      "ui_carrier": "无界面（服务内执行）",
      "shown_text_verbatim": "com.farmerbb.taskbar.ACCESSIBILITY_ACTION",
      "shown_text_zh": "通过自定义广播 + AccessibilityService 执行返回/主页/最近任务/电源等全局动作，并读取通知栏内容用于展示通知托盘",
      "user_action_requested": "无；不监听设置页、不自动点击确认、不阻止撤权",
      "code_anchor": "com.farmerbb.taskbar.util.g0#n2 / com.farmerbb.taskbar.util.g0#H1 / com.farmerbb.taskbar.service.PowerMenuService"
    },
    {
      "step": 6,
      "stage": "业务功能触发",
      "screen_or_component": "com.farmerbb.taskbar.activity.EnableAdditionalSettingsActivity（可选提权页，主题 Taskbar.Dialog）",
      "trigger_event": "用户在设置中点击“Enable additional settings”偏好项（Y.l.onPreferenceClick）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Taskbar can optionally use elevated permissions to improve your desktop mode experience. These permissions are granted by running an adb shell command. … adb shell pm grant %1$s %2$s",
      "shown_text_zh": "可选提升权限说明页：明确告知需自行在电脑上执行 adb shell pm grant <包名> android.permission.WRITE_SECURE_SETTINGS，获权后应用可在连接显示器时直写 secure settings（含自动把自身加入 enabled_accessibility_services）",
      "user_action_requested": "用户自行决定是否用 ADB 授权；无诱导、无绕过系统无障碍开关的隐蔽自授权（无该权限时一律回退到弹窗引导）",
      "code_anchor": "com.farmerbb.taskbar.activity.EnableAdditionalSettingsActivity#u0 / res/values/strings.xml tb_enable_additional_settings_message_1"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项说明：res/xml/tb_accessibility_service.xml 引用 @string/tb_accessibility_service_description（android:description）与 @string/tb_accessibility_service_summary（android:summary）",
    "DummyActivity 原生 AlertDialog：标题 tb_permission_dialog_title（Permission needed），正文 tb_enable_accessibility → 指向 tb_accessibility_service_description 全文，按钮 tb_action_cancel / tb_action_activate（strings.xml 第 98-105、257 行）",
    "可选提权说明页 EnableAdditionalSettingsActivity：标题 tb_enable_additional_settings、正文 tb_enable_additional_settings_message_1/_2、命令模板 tb_adb_shell_command（strings.xml 第 121、258-262 行）",
    "悬浮窗权限引导（非无障碍）：tb_permission_dialog_message / tb_permission_dialog_instructions_phone|tv（strings.xml 第 406-411 行），由 g0.A2 / g0.C2 弹出",
    "未发现任何 WebView、assets HTML、远端页面或悬浮窗遮罩形式的无障碍引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Taskbar needs to be activated as an accessibility service in order to perform button press actions such as back, home, recents, and power, as well as displaying the notification tray.\n\nThis permission is used only to perform button press actions, and for no other purpose.",
      "text_zh": "Taskbar 需要被激活为无障碍服务，才能执行返回、主页、最近任务、电源等按键动作，以及显示通知栏。该权限仅用于执行按键动作，不作其他任何用途。",
      "source_location": "res/values/strings.xml key=tb_accessibility_service_description（第 98-100 行），经 tb_enable_accessibility 复用为弹窗正文；同时用于 res/xml/tb_accessibility_service.xml android:description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Allows Taskbar to perform button press actions",
      "text_zh": "允许 Taskbar 执行按键动作",
      "source_location": "res/values/strings.xml key=tb_accessibility_service_summary（第 101 行）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Permission needed",
      "text_zh": "需要权限",
      "source_location": "res/values/strings.xml key=tb_permission_dialog_title（第 411 行），DummyActivity 弹窗标题 R$string.h1",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Cancel / Activate",
      "text_zh": "取消 / 激活",
      "source_location": "res/values/strings.xml key=tb_action_cancel、tb_action_activate（第 102-103 行）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Taskbar can optionally use elevated permissions to improve your desktop mode experience. These permissions are granted by running an adb shell command.",
      "text_zh": "Taskbar 可选择性地使用提权来改善桌面模式体验。这些权限需通过运行 adb shell 命令授予。",
      "source_location": "res/values/strings.xml key=tb_enable_additional_settings_message_1（第 259-261 行）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "adb shell pm grant %1$s %2$s",
      "text_zh": "adb shell pm grant <包名> <权限名>",
      "source_location": "res/values/strings.xml key=tb_adb_shell_command（第 121 行），EnableAdditionalSettingsActivity#u0 填入 getPackageName() 与 android.permission.WRITE_SECURE_SETTINGS",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性安全降级：点 Cancel 由 DialogInterface.OnClickListener（DummyActivity.w）关闭弹窗并结束 InvisibleActivity 流程，不会 onResume 死循环重跳；仅当用户再次触发依赖按键功能时才会重新出现该弹窗。U1 中通过 SharedPreferences 的 disable_animations 与延时策略避免高频重复弹窗。",
    "overlay_or_fake_settings": "无。未叠放半透明引导遮罩，未实现高仿系统无障碍开关页；引导仅为一个原生 AlertDialog + 系统无障碍页。",
    "restricted_settings_13plus_coaching": "无。无 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、无“点右上角菜单允许受限设置”教学、无 Session 安装器绕过；相关字符串仅为 ADB 提权的可选项说明。",
    "post_grant_anti_removal": "无。未监听无障碍设置页，未用 GLOBAL_ACTION_BACK/HOME 阻止撤权，未自动点击确认。Q0/H1 直写 enabled_accessibility_services 仅在用户已通过 ADB 授予 WRITE_SECURE_SETTINGS 时生效，属公开说明的可选路径。",
    "benign_graceful_degradation": "有。无无障碍权限时按键类功能（返回/主页/最近任务/电源、通知托盘）不可用，其余桌面任务栏、多窗口、应用抽屉等功能不受影响；用户可 Cancel 继续使用，或按设置页指引通过 ADB 授权 WRITE_SECURE_SETTINGS 作为替代路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以系统无障碍页拉起为锚：监测 Activity 栈顶变为 com.android.settings/.Settings$AccessibilitySettings（或任何 Settings 子页）时立即抓取上一层栈快照；同时在该时刻回溯最近 1 秒内是否有 com.farmerbb.taskbar/.activity.DummyActivity 的 onCreate/onResume，以捕获“弹窗→跳转”配对。也可在 DummyActivity 出现时（主题 Incognito、excludeFromRecents、界面近乎空白）直接抓 UTG。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前的原生引导弹窗页",
        "page_identifier": "com.farmerbb.taskbar/.activity.DummyActivity 上的 AlertDialog：标题 Permission needed，正文含 “Taskbar needs to be activated as an accessibility service…”，按钮 Cancel / Activate",
        "why_most_useful": "该弹窗是本应用唯一的无障碍用途声明点，可直接比对正文所述范围（仅按键动作）与后续实际行为是否一致，判断是否为误导性说明",
        "observable_utg_signals": ["dialog title = Permission needed", "dialog message 含 accessibility service 与 for no other purpose 字样", "button text Cancel / Activate 同时存在（可取消性）", "宿主 Activity 无可见布局内容（setContentView(new View)）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页列表中出现 Taskbar / Allows Taskbar to perform button press actions",
        "why_most_useful": "确认应用是否如实以自身名称与 summary 出现在系统列表，而非伪装成系统组件或空白项",
        "observable_utg_signals": ["列表项文本 = Taskbar", "summary = Allows Taskbar to perform button press actions", "service component = com.farmerbb.taskbar/.service.PowerMenuService"]
      },
      {
        "page_role": "可选提权说明页（ADB）",
        "page_identifier": "com.farmerbb.taskbar/.activity.EnableAdditionalSettingsActivity 弹窗式页面，含 adb shell pm grant 命令文本",
        "why_most_useful": "区分“公开 ADB 提权说明”与“诱导绕过受限设置”的关键页面，确认无 ACTION_APPLICATION_DETAILS_SETTINGS 教学",
        "observable_utg_signals": ["正文含 adb shell pm grant 与 android.permission.WRITE_SECURE_SETTINGS", "无“允许受限设置”字样", "按钮为关闭/复制类，非跳转应用详情"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导全程为纯文本原生控件，UTG 可直接提取。需注意 DummyActivity 采用近乎空白的 Incognito 主题且 excludeFromRecents，单纯以“空白页”为恶意特征会误报；另应用未声明 android:isAccessibilityTool，系统可能显示“此服务可查看屏幕内容”类提示，属平台默认提示而非应用伪造。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.farmerbb.taskbar.util.g0#n2",
    "com.farmerbb.taskbar.util.g0#I1",
    "com.farmerbb.taskbar.activity.DummyActivity#onResume",
    "com.farmerbb.taskbar.activity.DummyActivity#f",
    "res/xml/tb_accessibility_service.xml",
    "res/values/strings.xml（tb_accessibility_service_description / tb_permission_dialog_title / tb_action_cancel / tb_action_activate）"
  ]
}
```

</details>
