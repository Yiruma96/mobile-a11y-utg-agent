# MR_097__1f5850b3a3｜hawkshaw — System Settings

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：169.5s

## 1. 一句话核心结论

- **核心申请方式**：以“System Settings”冒充系统设置，通过不可取消的连环原生对话框权限向导，在批量索取短信/通讯录/录音/摄像头权限后直接把用户导向 android.settings.ACCESSIBILITY_SETTINGS 开启同名无障碍键控服务，取消按钮仍继续推进后续高危授权，完成后禁用桌面图标隐藏。
- **静态可见性说明**：全部引导逻辑位于 classes.dex 明文，无加壳、无 AES 密文、无远端 HTML；界面均为原生 AlertDialog 与原生 Activity，静态即可完整还原无障碍引导链。仅 Keylogger 内部按键记录与外发细节未展开。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1f5850b3a38df372cc40987b376cbf093ed5dd5d9e99e3ead61b24aa8cc82976` |
| 包名 / 年份 | `me.hawkshaw` / 2021 |
| 家族 / 品类 | **hawkshaw**（同池样本数：48） |
| 原始来源标识 | https://research.checkpoint.com/2021/going-rogue-a-mastermind-behind-android-malware-returns-with-a-new-rat/ |
| 桌面显示名 | System Settings |
| 引导页宣称品牌/身份 | System Settings（系统设置），实际应用自称 Hawkshaw 社交问答游戏 |
| 系统无障碍列表服务名 | System Settings |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：app_name=System Settings 与 app_name_alias=Hawkshaw 双名并存；无障碍服务 label 与系统设置同名、description 谎称“Accessibility helps us to secure your device”；IntermediateActivity 用空白 TextView 作内容视图形成无界面过渡；流程末尾 setComponentEnabledSetting(MainActivity, COMPONENT_DISABLED, 1) 隐藏桌面图标并向 Firebase 上报 app/hidden=true |
| 无障碍服务类名 | `me.baldpanel.tasks.Keylogger` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS` |
| 系统设置项说明 (`android:description`) | Accessibility helps us to secure your device |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | me.baldpanel.ui.activities.MainActivity → me.baldpanel.ui.activities.IntermediateActivity | MainActivity.onCreate 执行后立即 startActivity(IntermediateActivity) 并 finish() | 原生Activity | 无 | 无需操作，自动跳转 | `me.baldpanel.ui.activities.MainActivity#onCreate / me.baldpanel.ui.activities.IntermediateActivity#onCreate` |
| 2 | 引导说明页 | me.baldpanel.ui.activities.PermissionsActivity（运行时权限请求） | PermissionsActivity.onCreate → v() → requestPermissions(me.baldpanel.utils.a.c.b(), 16)；SDK<23 直接回调 onRequestPermissionsResult | 系统无障碍页 | 无 | 在系统权限弹窗中逐项点击“允许”；无跳过入口，onRequestPermissionsResult 无条件继续下一步 | `me.baldpanel.ui.activities.PermissionsActivity#v / me.baldpanel.ui.activities.PermissionsActivity#onRequestPermissionsResult` |
| 3 | 跳受限设置 | 系统电池优化白名单页（android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS） | onRequestPermissionsResult → u() → n()，SDK>=23 且未忽略电池优化时 startActivityForResult(intent, 0) | 系统无障碍页 | 无 | 选择“允许”以忽略电池优化；返回后 onActivityResult(0) 立即进入无障碍引导 | `me.baldpanel.ui.activities.PermissionsActivity#n` |
| 4 | 引导说明页 | 原生 AlertDialog（PermissionsActivity.o()），不可取消 | onActivityResult(requestCode=0) → o()；先以 x() 检测 Settings.Secure 中 accessibility_enabled 与 enabled_accessibility_services，未启用才弹框 | 原生Dialog | **原文**：Enable Accessibility Settings / Locate app System Settings and enable accessibility. / Enable Accessibility / Cancel<br>**译注**：标题“启用无障碍设置”，正文“找到名为 System Settings 的应用并开启无障碍”，按钮“启用无障碍”与“取消” | 要求点击“Enable Accessibility”跳系统无障碍页；虽有 Cancel，但点击后流程并不终止 | `me.baldpanel.ui.activities.PermissionsActivity#o / res/values/strings.xml (enable_accessibility_header, enable_accessibility_message, enable_accessibility)` |
| 5 | 跳无障碍设置 | 系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS） | me.baldpanel.ui.activities.h.onClick 构造 Intent("android.settings.ACCESSIBILITY_SETTINGS") 后 startActivityForResult(intent, 1) | 系统无障碍页 | **原文**：Accessibility helps us to secure your device<br>**译注**：系统无障碍服务列表中显示为“System Settings”，说明文字为“无障碍可帮助我们保护您的设备” | 要求用户在系统无障碍列表中找到名为 System Settings 的服务并手动开启开关 | `me.baldpanel.ui.activities.h#onClick / res/xml/accessibility_service_config.xml / res/values/strings.xml (accessibility_service_label, accessibility_service_description)` |
| 6 | 拒权反馈循环 | 原生 AlertDialog 取消分支（me.baldpanel.ui.activities.i）→ onActivityResult(1,-1,null) | 用户在无障碍引导框点击 Cancel，或在系统无障碍页直接返回（resultCode 不被校验） | 原生Dialog | **原文**：Media Projection / Please select **don't show again** ! ! !<br>**译注**：取消无障碍后立刻弹出“Media Projection”录屏索取框，并诱导用户勾选“不再提示” | 继续要求点击 OK 授权屏幕捕获；i.onClick 仅 dialog.cancel() 后立即推进，无退出路径 | `me.baldpanel.ui.activities.i#onClick / me.baldpanel.ui.activities.PermissionsActivity#r / res/values/strings.xml (media_projection_message)` |
| 7 | 拒权反馈循环 | 设备管理器、通知监听、国产 ROM 自启动引导（PermissionsActivity.q()/s()/p()/w()） | onActivityResult(2)→q() 设备管理器；onActivityResult(3)→s() 通知监听；onActivityResult(4)→w() MIUI 权限编辑；onActivityResult(5)→p() 自启动管理 | 原生Dialog | **原文**：Enable Read Notifications / Locate System Settings in settings and enable it.\nPush notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings / Click on Activate button to secure your application.<br>**译注**：“启用读取通知：在设置中找到 System Settings 并开启；推送通知能提升体验并促进学习进度”以及设备管理器激活说明“点击激活按钮以保护你的应用” | 逐项点击 OK/Activate 完成设备管理器激活、通知使用权开启与 ROM 自启动授权；每个对话框均 setCancelable(false) | `me.baldpanel.ui.activities.PermissionsActivity#q / #s / #p / #w / res/values/strings.xml (device_admin_explanation)` |
| 8 | 获权后动作 | PermissionsActivity.t() → HomeActivity；同时禁用 MainActivity 组件 | 任一分支返回后调用 t()，或取消分支经 onActivityResult(5) 落入 t() | 原生Activity | **原文**：App Uninstalled!<br>**译注**：向导结束后禁用桌面图标组件并上报 hidden=true，桌面入口消失，呈现“应用已卸载”的假象文案 | 无提示直接进入 HomeActivity 主界面 | `me.baldpanel.ui.activities.PermissionsActivity#t / res/values/strings.xml (app_uninstalled)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- PermissionsActivity.o() 弹出的不可取消 AlertDialog：标题 Enable Accessibility Settings、正文 Locate app System Settings and enable accessibility.
- 系统无障碍设置页中该服务条目：label=System Settings、description=Accessibility helps us to secure your device（res/values/strings.xml + res/xml/accessibility_service_config.xml）
- PermissionsActivity.r() 弹出的录屏索取 AlertDialog：Media Projection / Please select **don't show again** ! ! !
- PermissionsActivity.s() 弹出的通知监听 AlertDialog：Enable Read Notifications 及硬编码正文（类内字符串常量）
- PermissionsActivity.q() 触发的系统设备管理器激活页，附加说明取自 device_admin_explanation：Click on Activate button to secure your application.
- PermissionsActivity.p()/w() 弹窗：Enable Auto Start / Locate app System Settings and enable autostart.，失败时 Toast 输出 error_auto_start
- 桌面图标名称：app_name=System Settings（application label），主 Activity 使用 app_name_alias=Hawkshaw
- 无 assets 内 HTML 引导页、无 WebView、无悬浮窗遮罩层

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable Accessibility Settings | 启用无障碍设置 | `res/values/strings.xml key=enable_accessibility_header（PermissionsActivity.o() 引用）` | 假反诈安全 |
| en | Locate app System Settings and enable accessibility. | 找到名为 System Settings 的应用并开启无障碍。 | `res/values/strings.xml key=enable_accessibility_message` | 受限设置分步教学 |
| en | Accessibility helps us to secure your device | 无障碍功能可帮助我们保护您的设备 | `res/values/strings.xml key=accessibility_service_description → res/xml/accessibility_service_config.xml` | 假反诈安全 |
| en | System Settings | 系统设置 | `res/values/strings.xml key=accessibility_service_label 与 key=app_name` | 未知 |
| en | Locate app System Settings and enable autostart. | 找到名为 System Settings 的应用并开启自启动。 | `res/values/strings.xml key=enable_auto_start_message（PermissionsActivity.p()）` | 受限设置分步教学 |
| en | Please select **don't show again** ! ! ! | 请勾选“不再提示”！！！ | `res/values/strings.xml key=media_projection_message（PermissionsActivity.r()）` | 教唆忽视警告 |
| en | Locate System Settings in settings and enable it.\nPush notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings | 在设置中找到 System Settings 并开启它。推送通知能带来更好的体验并促进你的学习进度，你可随时在应用设置中更改。 | `me.baldpanel.ui.activities.PermissionsActivity#s() 方法内硬编码字符串` | 隐私承诺 |
| en | Click on Activate button to secure your application. | 点击激活按钮以保护你的应用。 | `res/values/strings.xml key=device_admin_explanation（PermissionsActivity.q() 作为 ADD_EXPLANATION 传入）` | 假反诈安全 |
| en | App Uninstalled! | 应用已卸载！ | `res/values/strings.xml key=app_uninstalled（配合 t() 禁用桌面图标组件）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无障碍引导框虽设 Cancel，但 me.baldpanel.ui.activities.i.onClick 仅 dialog.cancel() 后立即回调 onActivityResult(1,-1,null)，resultCode 不做校验，流程直接进入 r() 索取录屏，随后连续推进设备管理器、通知监听、ROM 自启动，用户无法退出向导；t() 为唯一终点
- **遮罩叠层 / 高仿系统设置页**：无。未叠放半透明遮罩或高仿系统无障碍开关页，仅使用不可取消原生 AlertDialog + 真实系统设置页跳转
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。x() 仅只读检测 accessibility_enabled / enabled_accessibility_services，未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权；但流程末尾 setComponentEnabledSetting(MainActivity, COMPONENT_DISABLED, 1) 隐藏桌面图标并向 Firebase 写入 app/hidden=true
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 PermissionsActivity 发起 Intent(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（或 Activity 切换至 com.android.settings 无障碍页时）立即抓取栈顶；此外冷启动 MainActivity→IntermediateActivity（空白 TextView）也应作为早期观测点
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：盲区较小：全程为原生文本控件，UTG 可直接取文本。需注意两点：IntermediateActivity 使用空白 TextView 无任何文本，冷启动首屏 UTG 可能只看到空页，应以无障碍设置跳转作为主触发；t() 完成后 MainActivity 被禁用、桌面图标消失，若在流程末端再拉起应用将无从桌面进入，需在向导阶段抓取。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **无障碍引导弹窗页（跳转前最后一屏）** | com.android.internal.app.AlertDialog，标题 Enable Accessibility Settings，正文 Locate app System Settings and enable accessibility.，按钮 Enable Accessibility / Cancel | 这是应用主动索取无障碍的唯一文案锚点，可直接判定是诱导而非功能所需说明，并验证弹窗不可取消与取消后不终止 | 标题文本 Enable Accessibility Settings；正文包含 System Settings 字样；仅两个按钮且无退出/跳过项；宿主包名为 me.hawkshaw 而非系统设置 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页，服务条目显示 System Settings，说明 Accessibility helps us to secure your device | 验证身份冒充——条目名与系统设置同名、描述与实际 typeAllMask/canRetrieveWindowContent 全量能力严重不符 | 服务名 System Settings 与页面上下文（系统设置）冲突；描述文本 Accessibility helps us to secure your device；同屏存在包名/图标与应用列表名不符 |
| **取消后立即弹出的录屏索取框（拒权反馈循环证据）** | AlertDialog 标题 Media Projection，正文 Please select **don't show again** ! ! ! | 证明取消无障碍不会终止向导，属强制串行收割而非良性降级 | 从系统设置返回后 1 秒内出现新弹窗；文案诱导勾选“不再提示”；弹窗按钮无退出项 |
| **系统无障碍设置页（用户实际操作页）** | android.settings.ACCESSIBILITY_SETTINGS 页面，包名 com.android.settings | 确认跳转目标确为无障碍设置而非其他页面，可与系统电池优化页、设备管理器页区分，形成步骤序列 | 页面标题含 Accessibility；Activity 类名 com.android.settings.accessibility.*；上一跳来源为 me.hawkshaw PermissionsActivity |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `me.baldpanel.ui.activities.PermissionsActivity#o`
- `me.baldpanel.ui.activities.h#onClick`
- `me.baldpanel.ui.activities.i#onClick`
- `me.baldpanel.ui.activities.PermissionsActivity#onActivityResult`
- `me.baldpanel.ui.activities.PermissionsActivity#t`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**可见性**：完全静态可见。应用未加壳，也没有使用 AES 加密或远端 HTML 载荷；全部引导逻辑都位于 `classes.dex` 明文中，界面载体均为原生 `AlertDialog`，没有使用 WebView、悬浮窗或遮罩层。

**身份伪装（核心特征）**
- 桌面名 `app_name` = `System Settings`，但 `app_name_alias` = `Hawkshaw`，`about_app` 自述为“social quiz game”；主 Activity 挂载 `@string/app_name_alias`，实际显示名与包身份不一致。
- 无障碍服务标签 `accessibility_service_label` = `System Settings`，描述 `Accessibility helps us to secure your device`，因此在系统无障碍列表中，该服务与真实的系统设置同名。
- 服务配置声明 `typeAllMask`、`feedbackAllMask`、`canRetrieveWindowContent="true"`，即读取全部窗口内容，与“保护设备”的说法不符。

**运行期页面流转（关键链路）**
1. `MainActivity.onCreate` 立即调用 `startActivity(IntermediateActivity)` 并执行 `finish()`；`IntermediateActivity` 使用空白 `TextView` 作为内容视图（用户看不到任何界面），再按登录状态跳转到 `LoginActivity` 或 `HomeActivity`。
2. `PermissionsActivity.v()` 申请运行时危险权限 → `onRequestPermissionsResult` 无条件调用 `u()`，而 `u()` 会调用 `z()`（启用 `BootReceiver` 并启动文件扫描线程）和 `n()`（请求忽略电池优化）。
3. `onActivityResult(0)` → `o()` 弹出无障碍引导框：标题 `Enable Accessibility Settings`、正文 `Locate app System Settings and enable accessibility.`、`setCancelable(false)`；点击 `Enable Accessibility` 后，由 `me.baldpanel.ui.activities.h.onClick` 发出 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 并调用 `startActivityForResult(...,1)`，直达系统无障碍页。
4. **取消按钮不能中止流程**：`i.onClick` 仅调用 `dialog.cancel()`，随后立刻回调 `onActivityResult(1,-1,null)` → `r()` 继续索取录屏（MediaProjection），随后 `q()` 索取设备管理器、`s()` 索取通知监听、`p()`/`w()` 引导国产 ROM 自启动，用户没有退出通道。
5. 流程末尾 `t()` 通过 `setComponentEnabledSetting(MainActivity, 2, 1)` 禁用桌面图标，并把 `user-data/<id>/app/hidden = "true"` 写入 Firebase，图标从桌面消失。

**未发现**：没有 13+ 受限设置分步教学，没有 Session 安装器绕过，也没有使用 GLOBAL_ACTION_BACK 阻止撤权；`x()` 只做 `accessibility_enabled` 与 `enabled_accessibility_services` 的只读检测。

**已登记风险**：R-001（autonomous_audit / high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于 classes.dex 明文，无加壳、无 AES 密文、无远端 HTML；界面均为原生 AlertDialog 与原生 Activity，静态即可完整还原无障碍引导链。仅 Keylogger 内部按键记录与外发细节未展开。",
  "summary_one_liner": "以“System Settings”冒充系统设置，通过不可取消的连环原生对话框权限向导，在批量索取短信/通讯录/录音/摄像头权限后直接把用户导向 android.settings.ACCESSIBILITY_SETTINGS 开启同名无障碍键控服务，取消按钮仍继续推进后续高危授权，完成后禁用桌面图标隐藏。",
  "disguise_identity": {
    "app_display_name": "System Settings",
    "claimed_brand_or_persona": "System Settings（系统设置），实际应用自称 Hawkshaw 社交问答游戏",
    "a11y_service_label": "System Settings",
    "identity_mismatch": true,
    "obfuscation_tricks": "app_name=System Settings 与 app_name_alias=Hawkshaw 双名并存；无障碍服务 label 与系统设置同名、description 谎称“Accessibility helps us to secure your device”；IntermediateActivity 用空白 TextView 作内容视图形成无界面过渡；流程末尾 setComponentEnabledSetting(MainActivity, COMPONENT_DISABLED, 1) 隐藏桌面图标并向 Firebase 上报 app/hidden=true"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "me.baldpanel.ui.activities.MainActivity → me.baldpanel.ui.activities.IntermediateActivity",
      "trigger_event": "MainActivity.onCreate 执行后立即 startActivity(IntermediateActivity) 并 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "IntermediateActivity 以空白 TextView 作为内容视图，用户看不到任何界面内容，仅按 flag 与登录态静默路由",
      "user_action_requested": "无需操作，自动跳转",
      "code_anchor": "me.baldpanel.ui.activities.MainActivity#onCreate / me.baldpanel.ui.activities.IntermediateActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "me.baldpanel.ui.activities.PermissionsActivity（运行时权限请求）",
      "trigger_event": "PermissionsActivity.onCreate → v() → requestPermissions(me.baldpanel.utils.a.c.b(), 16)；SDK<23 直接回调 onRequestPermissionsResult",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统运行时权限弹窗，一次性申请短信、通讯录、通话记录、录音、摄像头、定位、存储等权限",
      "user_action_requested": "在系统权限弹窗中逐项点击“允许”；无跳过入口，onRequestPermissionsResult 无条件继续下一步",
      "code_anchor": "me.baldpanel.ui.activities.PermissionsActivity#v / me.baldpanel.ui.activities.PermissionsActivity#onRequestPermissionsResult"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统电池优化白名单页（android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS）",
      "trigger_event": "onRequestPermissionsResult → u() → n()，SDK>=23 且未忽略电池优化时 startActivityForResult(intent, 0)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统“忽略电池优化”确认页，用于让后台服务不被省电策略杀死",
      "user_action_requested": "选择“允许”以忽略电池优化；返回后 onActivityResult(0) 立即进入无障碍引导",
      "code_anchor": "me.baldpanel.ui.activities.PermissionsActivity#n"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "原生 AlertDialog（PermissionsActivity.o()），不可取消",
      "trigger_event": "onActivityResult(requestCode=0) → o()；先以 x() 检测 Settings.Secure 中 accessibility_enabled 与 enabled_accessibility_services，未启用才弹框",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Accessibility Settings / Locate app System Settings and enable accessibility. / Enable Accessibility / Cancel",
      "shown_text_zh": "标题“启用无障碍设置”，正文“找到名为 System Settings 的应用并开启无障碍”，按钮“启用无障碍”与“取消”",
      "user_action_requested": "要求点击“Enable Accessibility”跳系统无障碍页；虽有 Cancel，但点击后流程并不终止",
      "code_anchor": "me.baldpanel.ui.activities.PermissionsActivity#o / res/values/strings.xml (enable_accessibility_header, enable_accessibility_message, enable_accessibility)"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "me.baldpanel.ui.activities.h.onClick 构造 Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") 后 startActivityForResult(intent, 1)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility helps us to secure your device",
      "shown_text_zh": "系统无障碍服务列表中显示为“System Settings”，说明文字为“无障碍可帮助我们保护您的设备”",
      "user_action_requested": "要求用户在系统无障碍列表中找到名为 System Settings 的服务并手动开启开关",
      "code_anchor": "me.baldpanel.ui.activities.h#onClick / res/xml/accessibility_service_config.xml / res/values/strings.xml (accessibility_service_label, accessibility_service_description)"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "原生 AlertDialog 取消分支（me.baldpanel.ui.activities.i）→ onActivityResult(1,-1,null)",
      "trigger_event": "用户在无障碍引导框点击 Cancel，或在系统无障碍页直接返回（resultCode 不被校验）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Media Projection / Please select **don't show again** ! ! !",
      "shown_text_zh": "取消无障碍后立刻弹出“Media Projection”录屏索取框，并诱导用户勾选“不再提示”",
      "user_action_requested": "继续要求点击 OK 授权屏幕捕获；i.onClick 仅 dialog.cancel() 后立即推进，无退出路径",
      "code_anchor": "me.baldpanel.ui.activities.i#onClick / me.baldpanel.ui.activities.PermissionsActivity#r / res/values/strings.xml (media_projection_message)"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "设备管理器、通知监听、国产 ROM 自启动引导（PermissionsActivity.q()/s()/p()/w()）",
      "trigger_event": "onActivityResult(2)→q() 设备管理器；onActivityResult(3)→s() 通知监听；onActivityResult(4)→w() MIUI 权限编辑；onActivityResult(5)→p() 自启动管理",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Read Notifications / Locate System Settings in settings and enable it.\\nPush notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings / Click on Activate button to secure your application.",
      "shown_text_zh": "“启用读取通知：在设置中找到 System Settings 并开启；推送通知能提升体验并促进学习进度”以及设备管理器激活说明“点击激活按钮以保护你的应用”",
      "user_action_requested": "逐项点击 OK/Activate 完成设备管理器激活、通知使用权开启与 ROM 自启动授权；每个对话框均 setCancelable(false)",
      "code_anchor": "me.baldpanel.ui.activities.PermissionsActivity#q / #s / #p / #w / res/values/strings.xml (device_admin_explanation)"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "PermissionsActivity.t() → HomeActivity；同时禁用 MainActivity 组件",
      "trigger_event": "任一分支返回后调用 t()，或取消分支经 onActivityResult(5) 落入 t()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "App Uninstalled!",
      "shown_text_zh": "向导结束后禁用桌面图标组件并上报 hidden=true，桌面入口消失，呈现“应用已卸载”的假象文案",
      "user_action_requested": "无提示直接进入 HomeActivity 主界面",
      "code_anchor": "me.baldpanel.ui.activities.PermissionsActivity#t / res/values/strings.xml (app_uninstalled)"
    }
  ],
  "text_presentation_locations": [
    "PermissionsActivity.o() 弹出的不可取消 AlertDialog：标题 Enable Accessibility Settings、正文 Locate app System Settings and enable accessibility.",
    "系统无障碍设置页中该服务条目：label=System Settings、description=Accessibility helps us to secure your device（res/values/strings.xml + res/xml/accessibility_service_config.xml）",
    "PermissionsActivity.r() 弹出的录屏索取 AlertDialog：Media Projection / Please select **don't show again** ! ! !",
    "PermissionsActivity.s() 弹出的通知监听 AlertDialog：Enable Read Notifications 及硬编码正文（类内字符串常量）",
    "PermissionsActivity.q() 触发的系统设备管理器激活页，附加说明取自 device_admin_explanation：Click on Activate button to secure your application.",
    "PermissionsActivity.p()/w() 弹窗：Enable Auto Start / Locate app System Settings and enable autostart.，失败时 Toast 输出 error_auto_start",
    "桌面图标名称：app_name=System Settings（application label），主 Activity 使用 app_name_alias=Hawkshaw",
    "无 assets 内 HTML 引导页、无 WebView、无悬浮窗遮罩层"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Settings",
      "text_zh": "启用无障碍设置",
      "source_location": "res/values/strings.xml key=enable_accessibility_header（PermissionsActivity.o() 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate app System Settings and enable accessibility.",
      "text_zh": "找到名为 System Settings 的应用并开启无障碍。",
      "source_location": "res/values/strings.xml key=enable_accessibility_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility helps us to secure your device",
      "text_zh": "无障碍功能可帮助我们保护您的设备",
      "source_location": "res/values/strings.xml key=accessibility_service_description → res/xml/accessibility_service_config.xml",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "System Settings",
      "text_zh": "系统设置",
      "source_location": "res/values/strings.xml key=accessibility_service_label 与 key=app_name",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate app System Settings and enable autostart.",
      "text_zh": "找到名为 System Settings 的应用并开启自启动。",
      "source_location": "res/values/strings.xml key=enable_auto_start_message（PermissionsActivity.p()）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please select **don't show again** ! ! !",
      "text_zh": "请勾选“不再提示”！！！",
      "source_location": "res/values/strings.xml key=media_projection_message（PermissionsActivity.r()）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate System Settings in settings and enable it.\\nPush notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings",
      "text_zh": "在设置中找到 System Settings 并开启它。推送通知能带来更好的体验并促进你的学习进度，你可随时在应用设置中更改。",
      "source_location": "me.baldpanel.ui.activities.PermissionsActivity#s() 方法内硬编码字符串",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on Activate button to secure your application.",
      "text_zh": "点击激活按钮以保护你的应用。",
      "source_location": "res/values/strings.xml key=device_admin_explanation（PermissionsActivity.q() 作为 ADD_EXPLANATION 传入）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "App Uninstalled!",
      "text_zh": "应用已卸载！",
      "source_location": "res/values/strings.xml key=app_uninstalled（配合 t() 禁用桌面图标组件）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无障碍引导框虽设 Cancel，但 me.baldpanel.ui.activities.i.onClick 仅 dialog.cancel() 后立即回调 onActivityResult(1,-1,null)，resultCode 不做校验，流程直接进入 r() 索取录屏，随后连续推进设备管理器、通知监听、ROM 自启动，用户无法退出向导；t() 为唯一终点",
    "overlay_or_fake_settings": "无。未叠放半透明遮罩或高仿系统无障碍开关页，仅使用不可取消原生 AlertDialog + 真实系统设置页跳转",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。x() 仅只读检测 accessibility_enabled / enabled_accessibility_services，未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权；但流程末尾 setComponentEnabledSetting(MainActivity, COMPONENT_DISABLED, 1) 隐藏桌面图标并向 Firebase 写入 app/hidden=true",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 PermissionsActivity 发起 Intent(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（或 Activity 切换至 com.android.settings 无障碍页时）立即抓取栈顶；此外冷启动 MainActivity→IntermediateActivity（空白 TextView）也应作为早期观测点",
    "key_pages_to_capture": [
      {
        "page_role": "无障碍引导弹窗页（跳转前最后一屏）",
        "page_identifier": "com.android.internal.app.AlertDialog，标题 Enable Accessibility Settings，正文 Locate app System Settings and enable accessibility.，按钮 Enable Accessibility / Cancel",
        "why_most_useful": "这是应用主动索取无障碍的唯一文案锚点，可直接判定是诱导而非功能所需说明，并验证弹窗不可取消与取消后不终止",
        "observable_utg_signals": ["标题文本 Enable Accessibility Settings", "正文包含 System Settings 字样", "仅两个按钮且无退出/跳过项", "宿主包名为 me.hawkshaw 而非系统设置"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页，服务条目显示 System Settings，说明 Accessibility helps us to secure your device",
        "why_most_useful": "验证身份冒充——条目名与系统设置同名、描述与实际 typeAllMask/canRetrieveWindowContent 全量能力严重不符",
        "observable_utg_signals": ["服务名 System Settings 与页面上下文（系统设置）冲突", "描述文本 Accessibility helps us to secure your device", "同屏存在包名/图标与应用列表名不符"]
      },
      {
        "page_role": "取消后立即弹出的录屏索取框（拒权反馈循环证据）",
        "page_identifier": "AlertDialog 标题 Media Projection，正文 Please select **don't show again** ! ! !",
        "why_most_useful": "证明取消无障碍不会终止向导，属强制串行收割而非良性降级",
        "observable_utg_signals": ["从系统设置返回后 1 秒内出现新弹窗", "文案诱导勾选“不再提示”", "弹窗按钮无退出项"]
      },
      {
        "page_role": "系统无障碍设置页（用户实际操作页）",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 页面，包名 com.android.settings",
        "why_most_useful": "确认跳转目标确为无障碍设置而非其他页面，可与系统电池优化页、设备管理器页区分，形成步骤序列",
        "observable_utg_signals": ["页面标题含 Accessibility", "Activity 类名 com.android.settings.accessibility.*", "上一跳来源为 me.hawkshaw PermissionsActivity"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "盲区较小：全程为原生文本控件，UTG 可直接取文本。需注意两点：IntermediateActivity 使用空白 TextView 无任何文本，冷启动首屏 UTG 可能只看到空页，应以无障碍设置跳转作为主触发；t() 完成后 MainActivity 被禁用、桌面图标消失，若在流程末端再拉起应用将无从桌面进入，需在向导阶段抓取。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "me.baldpanel.ui.activities.PermissionsActivity#o",
    "me.baldpanel.ui.activities.h#onClick",
    "me.baldpanel.ui.activities.i#onClick",
    "me.baldpanel.ui.activities.PermissionsActivity#onActivityResult",
    "me.baldpanel.ui.activities.PermissionsActivity#t",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
