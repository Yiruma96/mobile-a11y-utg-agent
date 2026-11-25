# MR_083__b5d008ab68｜GhostClicker — Flash light alerts

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：176.6s

## 1. 一句话核心结论

- **核心申请方式**：用户在主页打开“notification”开关时弹出一个不可绕过的原生说明对话框，点 Yes 即直跳系统无障碍设置页，用户需手动在无说明文本的服务列表中找到该应用并开启，返回后以 Settings.Secure 校验并回写开关，拒绝则静默复位、无死循环。
- **静态可见性说明**：全链路静态完整可见：无障碍引导为 MainActivity 内的原生 Dialog + 直接 Intent 跳转，文案取自 res/values/strings.xml，布局为 res/layout/popupscreen.xml；无加壳、无 WebView、无本地/远端 HTML、无二次解密载荷。唯一未逐条校验 arsc 的细节是 exitAppDialog1 中资源 ID 2130968614/2130968616 与 noti_text/noti_title 的对应关系（按布局默认绑定与取值语义推定）。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b5d008ab68e57b2a22f265eb405a3eb92d2ad2cee075d55e5ce4e05b51a40c8c` |
| 包名 / 年份 | `com.fashlightalerts.vnm` / 2017 |
| 家族 / 品类 | **GhostClicker**（同池样本数：4） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/h/ghostclicker-adware-is-a-phantomlike-android-click-fraud.html |
| 桌面显示名 | Flash light alerts |
| 引导页宣称品牌/身份 | 手电筒/来电与短信闪光工具（strings 中自称 Flash Alerts on Call and SMS），并以 com.google.android.gms.logs 命名空间与 Plus Service 标签冒充 Google Play services 组件 |
| 系统无障碍列表服务名 | 无 android:label、无 android:description；系统无障碍列表中仅以类名/应用名派生条目呈现（NotificationService，归属 Flash light alerts） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务刻意不声明 label 与 description，系统列表无任何用途说明；服务类名 NotificationService 为通用良性命名；组件使用 com.google.android.gms.logs 与 label="Plus Service" 冒充 Google 组件（见 R-001）；strings.xml 中 yes_title="Not now"、no_title="Now" 标签语义反转；未伪造 isAccessibilityTool（minSdk 9，早于 Android 11 机制），无多 activity-alias |
| 无障碍服务类名 | `com.dhama.international.flashalert.NotificationService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, RECEIVE_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.dhama.international.flashalert.SplashActivity | onCreate：Timer 每 300ms 执行 SplashActivity$1 做动画，另一个 Timer 在 splashDelay 后执行 SplashActivity$2 | 原生Activity | 无 | 无需操作，自动跳转 | `SplashActivity.onCreate / SplashActivity$2.run` |
| 2 | 业务功能触发 | com.dhama.international.flashalert.MainActivity（2130903042 布局） | onCreate：加载 AdMob 横幅与插屏；绑定三个 ToggleButton（tglInCall 2131099710 / tglMsg 2131099712 / tglNotification 2131099714）的 OnCheckedChangeListener | 原生Activity | **原文**：Incoming Call Setting / Sms Setting / notification / Flash Interval Time / Flash Duration Time / Settings<br>**译注**：主界面：来电闪光、短信闪光、通知闪光三个开关，配闪光间隔与时长滑块及设置入口，顶部为广告位 | 用户可自行点按任一开关；notification 开关默认值由 ToggleFlashPrefs.getNotificationEnable() 恢复，冷启动不会自动弹窗 | `MainActivity.onCreate / MainActivity.setSettings` |
| 3 | 引导说明页 | MainActivity.exitAppDialog1("notification") 创建的原生 Dialog（setContentView 2130903043，即 res/layout/popupscreen.xml，宽 fill_parent、高 wrap_content） | 用户把 tglNotification 由关拨到开 → onCheckedChanged(paramCompoundButton.getId()==2131099714 && paramBoolean==true) → exitAppDialog1("notification") | 原生Dialog | **原文**：Notification Alert — Notification requires accessibility service to be on. do you want to enable notification feature? — 按钮：Yes / No<br>**译注**：标题“通知提醒”；正文“通知功能需要开启无障碍服务。你想启用通知功能吗？”；按钮“是 / 否” | 点 Yes 继续去系统无障碍设置；点 No 直接关闭对话框并取消本次开启（有明确取消路径） | `MainActivity.exitAppDialog1 / MainActivity.onCheckedChanged / res/layout/popupscreen.xml / res/values/strings.xml(noti_title,noti_text)` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（通过 startActivityForResult，requestCode=100） | MainActivity$2.onClick：paramString 非 "exit" 分支 → dismiss 对话框 → setNotFeature() | 系统无障碍页 | **原文**：无（由系统渲染；服务条目因未声明 android:description 而无说明文本）<br>**译注**：跳转到系统“无障碍”设置页，用户需自行在服务列表中找到本应用条目并手动开启 | 用户手动查找并开启无障碍服务；应用未提供任何分步截图/遮罩/高亮引导 | `MainActivity$2.onClick / MainActivity.setNotFeature` |
| 5 | 拒权反馈循环 | MainActivity.onActivityResult（回到主界面） | 用户从系统设置返回 → onActivityResult → isNotificationEnabled() 读取 Settings.Secure.accessibility_enabled 与 enabled_accessibility_services 并判断是否包含 "com.dhama.international.flashalert" | 原生Activity | **原文**：无（仅 Log.i("ToggleFlash", "ACCESSIBILIY IS DISABLED") 等日志）<br>**译注**：未开启则 ToggleButton 复位为关并写入 SharedPreferences，界面留在主页，不再弹窗、不重复跳转 | 无强制动作；用户可再次拨动开关重新进入引导（非自动循环） | `MainActivity.onActivityResult / MainActivity.isNotificationEnabled` |
| 6 | 获权后动作 | com.dhama.international.flashalert.NotificationService（AccessibilityService）→ MessageReceivedService | onServiceConnected 设置 AccessibilityServiceInfo（packageNames=com.whatsapp/com.facebook.katana/com.google.android.gsf，eventTypes=64，notificationTimeout=100）；onAccessibilityEvent 收到 TYPE_NOTIFICATION_STATE_CHANGED 后检查 hasSystemFeature("android.hardware.camera.flash") 并 startService(MessageReceivedService, from=notification) | 不可静态还原 | 无 | 无 | `NotificationService.onServiceConnected / NotificationService.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内由 exitAppDialog1("notification") 创建的原生 Dialog（res/layout/popupscreen.xml），标题/正文运行时被替换为 strings.xml 的 noti_title / noti_text，按钮被硬编码为 Yes / No——这是本样本唯一呈现无障碍引导文案的位置
- res/values/strings.xml 中 noti_title="Notification Alert" 与 noti_text="Notification requires accessibility service to be on.\ndo you want to enable notification feature?"（含换行）
- res/layout/popupscreen.xml 默认绑定 exit_title / exit_text，仅在非 exit 分支被覆盖，故同一布局在“评分”场景显示 Rate Us!
- 系统无障碍设置页：服务未声明 android:label 与 android:description，页面中不呈现任何应用自述用途文字
- 无 WebView、无 assets HTML、无悬浮窗/遮罩层、无通知栏引导、无 GIF/图片教学

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Notification Alert | 通知提醒 | `res/values/strings.xml key=noti_title` | 良性透明说明 |
| en | Notification requires accessibility service to be on.<br>do you want to enable notification feature? | 通知功能需要开启无障碍服务。你想启用通知功能吗？ | `res/values/strings.xml key=noti_text` | 良性透明说明 |
| en | Yes / No | 是 / 否 | `MainActivity.exitAppDialog1 硬编码 setText("Yes") / setText("No")` | 良性透明说明 |
| en | Not now / Now | 现在不要 / 现在（语义与按钮顺序反转） | `res/values/strings.xml key=yes_title / no_title（popupscreen.xml 默认绑定，本无障碍路径被硬编码覆盖）` | 未知 |
| en | Flash light alerts | 闪光灯提醒 | `AndroidManifest.xml application android:label（无障碍服务未单独声明 label/description）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环：点 No 仅关闭对话框并 setChecked(false)；从系统设置返回后 onActivityResult 只做一次 Settings.Secure 校验，未开启则开关复位并留在主页，不重跳、无 Timer 拉起、无 onResume 死循环
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW/悬浮窗、无半透明遮罩、无高仿系统无障碍开关页；跳转后完全交给系统设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无障碍路径无自点确认/无 GLOBAL_ACTION_BACK 或 HOME 撤权阻断；但样本另注册了空策略设备管理器 com.google.android.gms.logs.b（res/xml/admin.xml 仅 <uses-policies />）用于保活与卸载门槛，属独立链路，见 R-001
- **良性降级 / 替代方案**：具降级路径：拒绝后 notification 开关复位且来电/短信闪光功能不受影响，用户可继续使用其余功能；文案直接说明所需能力（通知闪光），未虚构故障、未伪造系统更新

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳时机是“检测到应用拨动通知开关后弹出的原生 Dialog”，即在 MainActivity 前台且界面出现含 accessibility 关键词的原生对话框时拉起 UTG；次优时机为监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（本样本由 MainActivity.setNotFeature 在点击 Yes 后立即触发，requestCode=100）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本样本无障碍引导链无显著 UTG 盲区（纯文本原生 Dialog，非图片、非 WebView、非加壳）。真正需要另行关注的是同包内独立的高危链：com.google.android.gms.logs.* 组件以 label="Plus Service" 与透明 Activity（Theme.Translucent.NoTitleBar、noHistory）伪装系统组件，经 AlarmManager 6 小时周期拉起并经 sauvl.com 取回远端链接强制弹栈——该链路同样运行期可见但需在“非用户操作触发”时抓取，若只按“用户拨动开关”埋点会漏采。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **引导说明弹窗页（核心页）** | MainActivity 之上的自定义 Dialog，标题 Notification Alert，正文含 accessibility service，两个按钮 Yes/No，黑色底、非系统 AlertDialog 样式（res/layout/popupscreen.xml） | 这是全流程唯一呈现引导文案的界面，可直接判定诱导话术性质、是否存在取消路径、按钮文案是否被反转 | 对话框文本节点包含 "accessibility" 与 "enable notification feature"；按钮节点仅 Yes / No，无“稍后/跳过”以外的第三选项；对话框是否不可取消（能否点击外部或返回键关闭）；应用是否同时处于 MainActivity（而非 WebView/Overlay 容器） |
| **跳转前的意图与调用栈** | MainActivity.setNotFeature 发出 Intent action=android.settings.ACCESSIBILITY_SETTINGS，startActivityForResult requestCode=100 | 确认跳转是直接进入无障碍设置页而非应用详情/受限设置页，且是否伴随 setResult(-1) 之类的异常调用 | Intent action 精确等于 android.settings.ACCESSIBILITY_SETTINGS；无 ACTION_APPLICATION_DETAILS_SETTINGS 或 Session 安装器调用；跳转前对话框已 dismiss（无遮罩压栈） |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已安装服务中归属 Flash light alerts 的条目，无 description 文本 | 核对系统侧呈现给用户的说明是否为空，判断用户是否只能凭应用名盲选服务，属身份误导的关键观测点 | 服务条目下无用途说明文字（android:description 缺失）；条目名称与桌面名 Flash light alerts 的对应关系；开启后是否出现系统确认弹窗及用户实际点击结果 |
| **拒权返回后的主界面状态** | 返回 MainActivity 后 tglNotification 保持关闭、无新弹窗 | 验证是否存在拒绝循环/定时重跳，是区分“诱导”与“骚扰式强迫”的决定性观测 | 返回后 3~10 秒内是否再次出现同一对话框；开关控件状态是否复位为关；是否出现其他弹窗或悬浮层 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.dhama.international.flashalert.MainActivity.onCheckedChanged`
- `com.dhama.international.flashalert.MainActivity.exitAppDialog1`
- `com.dhama.international.flashalert.MainActivity.setNotFeature`
- `com.dhama.international.flashalert.MainActivity.isNotificationEnabled`
- `com.dhama.international.flashalert.NotificationService.onServiceConnected`
- `res/layout/popupscreen.xml + res/values/strings.xml(noti_title,noti_text)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 无障碍权限引导流程核验结论（纯运行期 UTG 视角）

- **静态可见性完整，无加壳、无 WebView、无远端 HTML**：整条引导链全部在 `classes.dex` 与 `res/layout/popupscreen.xml`、`res/values/strings.xml` 中，静态即可完整还原（`static_visibility = clear`）。
- **触发时机是“用户主动打开通知功能开关”，不是冷启动强制弹窗**：冷启动 [SplashActivity.onCreate()](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.SplashActivity#onCreate>) 仅用 `Timer` 在 300ms 与 `splashDelay` 后跳 [MainActivity](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.MainActivity#onCreate>)，主界面只加载 AdMob 横幅/插屏广告，无任何权限提示。
- **引导载体是一个原生 Dialog（`popupscreen.xml`），无遮罩、无高仿设置页**：用户把 “notification” ToggleButton 打开 → [onCheckedChanged()](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.MainActivity#onCheckedChanged>) → [exitAppDialog1("notification")](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.MainActivity#exitAppDialog1>) 弹出标题 `Notification Alert`、正文 `Notification requires accessibility service to be on. do you want to enable notification feature?`，按钮被硬编码覆盖为 `Yes` / `No`。
- **跳转点唯一且直接**：点 `Yes` → [MainActivity$2.onClick](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.MainActivity$2#onClick>) → [setNotFeature()](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.MainActivity#setNotFeature>) 发出 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 并 `startActivityForResult(...,100)`。**未见 `ACTION_APPLICATION_DETAILS_SETTINGS`、未见 Android 13 受限设置分步教学、未见 Session 安装器绕过**。
- **拒绝不构成循环**：点 `No` → [MainActivity$3.onClick](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.MainActivity$3#onClick>) 仅 `setChecked(false)` 并关闭对话框；返回后 [onActivityResult()](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.MainActivity#onActivityResult>) 调用 [isNotificationEnabled()](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.MainActivity#isNotificationEnabled>) 读 `Settings.Secure.accessibility_enabled` / `enabled_accessibility_services`，未开启则开关复位，不重跳、不常驻 Timer。
- **身份与文案存在错配，但文案本身是“功能性透明说明”**：桌面名为 `Flash light alerts`，`strings.xml` 的 `app_name` 却是 `Flash Alerts on Call and SMS`；无障碍服务在 Manifest 中**既无 `android:label` 也无 `android:description`**，系统无障碍列表里没有可读说明，用户只能凭类名/应用名判断。另注意 `yes_title="Not now"`、`no_title="Now"` 的标签语义被反转（本路径被硬编码 `Yes/No` 覆盖）。
- **获权后行为**：[NotificationService.onServiceConnected()](<resource-unit:#1.dex1 code:com.dhama.international.flashalert.NotificationService#onServiceConnected>) 将监听范围限定为 `com.whatsapp`、`com.facebook.katana`、`com.google.android.gsf` 的通知事件（eventTypes=64），`onAccessibilityEvent` 命中后启动 `MessageReceivedService` 触发闪光——与“通知闪光”宣称一致，未发现自点确认、`GLOBAL_ACTION_BACK` 阻止撤权等反移除逻辑。
- **与家族特征的关联不在无障碍链上**：真正的高危项是另一条独立链（`com.google.android.gms.logs.*` 伪装 + `sauvl.com` 远端广告下发 + 6 小时 Alarm 强制弹栈 + 空策略设备管理器），已登记为 R-001；无障碍服务在本样本中属于“功能性外壳”，其作用是为“通知闪光”提供必要能力并顺带获取第三方应用通知内容。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全链路静态完整可见：无障碍引导为 MainActivity 内的原生 Dialog + 直接 Intent 跳转，文案取自 res/values/strings.xml，布局为 res/layout/popupscreen.xml；无加壳、无 WebView、无本地/远端 HTML、无二次解密载荷。唯一未逐条校验 arsc 的细节是 exitAppDialog1 中资源 ID 2130968614/2130968616 与 noti_text/noti_title 的对应关系（按布局默认绑定与取值语义推定）。",
  "summary_one_liner": "用户在主页打开“notification”开关时弹出一个不可绕过的原生说明对话框，点 Yes 即直跳系统无障碍设置页，用户需手动在无说明文本的服务列表中找到该应用并开启，返回后以 Settings.Secure 校验并回写开关，拒绝则静默复位、无死循环。",
  "disguise_identity": {
    "app_display_name": "Flash light alerts",
    "claimed_brand_or_persona": "手电筒/来电与短信闪光工具（strings 中自称 Flash Alerts on Call and SMS），并以 com.google.android.gms.logs 命名空间与 Plus Service 标签冒充 Google Play services 组件",
    "a11y_service_label": "无 android:label、无 android:description；系统无障碍列表中仅以类名/应用名派生条目呈现（NotificationService，归属 Flash light alerts）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务刻意不声明 label 与 description，系统列表无任何用途说明；服务类名 NotificationService 为通用良性命名；组件使用 com.google.android.gms.logs 与 label=\"Plus Service\" 冒充 Google 组件（见 R-001）；strings.xml 中 yes_title=\"Not now\"、no_title=\"Now\" 标签语义反转；未伪造 isAccessibilityTool（minSdk 9，早于 Android 11 机制），无多 activity-alias"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.dhama.international.flashalert.SplashActivity",
      "trigger_event": "onCreate：Timer 每 300ms 执行 SplashActivity$1 做动画，另一个 Timer 在 splashDelay 后执行 SplashActivity$2",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全屏黑色无标题启动页，仅显示背景图，无文字、无权限提示",
      "user_action_requested": "无需操作，自动跳转",
      "code_anchor": "SplashActivity.onCreate / SplashActivity$2.run"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.dhama.international.flashalert.MainActivity（2130903042 布局）",
      "trigger_event": "onCreate：加载 AdMob 横幅与插屏；绑定三个 ToggleButton（tglInCall 2131099710 / tglMsg 2131099712 / tglNotification 2131099714）的 OnCheckedChangeListener",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Incoming Call Setting / Sms Setting / notification / Flash Interval Time / Flash Duration Time / Settings",
      "shown_text_zh": "主界面：来电闪光、短信闪光、通知闪光三个开关，配闪光间隔与时长滑块及设置入口，顶部为广告位",
      "user_action_requested": "用户可自行点按任一开关；notification 开关默认值由 ToggleFlashPrefs.getNotificationEnable() 恢复，冷启动不会自动弹窗",
      "code_anchor": "MainActivity.onCreate / MainActivity.setSettings"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity.exitAppDialog1(\"notification\") 创建的原生 Dialog（setContentView 2130903043，即 res/layout/popupscreen.xml，宽 fill_parent、高 wrap_content）",
      "trigger_event": "用户把 tglNotification 由关拨到开 → onCheckedChanged(paramCompoundButton.getId()==2131099714 && paramBoolean==true) → exitAppDialog1(\"notification\")",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Notification Alert — Notification requires accessibility service to be on. do you want to enable notification feature? — 按钮：Yes / No",
      "shown_text_zh": "标题“通知提醒”；正文“通知功能需要开启无障碍服务。你想启用通知功能吗？”；按钮“是 / 否”",
      "user_action_requested": "点 Yes 继续去系统无障碍设置；点 No 直接关闭对话框并取消本次开启（有明确取消路径）",
      "code_anchor": "MainActivity.exitAppDialog1 / MainActivity.onCheckedChanged / res/layout/popupscreen.xml / res/values/strings.xml(noti_title,noti_text)"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（通过 startActivityForResult，requestCode=100）",
      "trigger_event": "MainActivity$2.onClick：paramString 非 \"exit\" 分支 → dismiss 对话框 → setNotFeature()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（由系统渲染；服务条目因未声明 android:description 而无说明文本）",
      "shown_text_zh": "跳转到系统“无障碍”设置页，用户需自行在服务列表中找到本应用条目并手动开启",
      "user_action_requested": "用户手动查找并开启无障碍服务；应用未提供任何分步截图/遮罩/高亮引导",
      "code_anchor": "MainActivity$2.onClick / MainActivity.setNotFeature"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onActivityResult（回到主界面）",
      "trigger_event": "用户从系统设置返回 → onActivityResult → isNotificationEnabled() 读取 Settings.Secure.accessibility_enabled 与 enabled_accessibility_services 并判断是否包含 \"com.dhama.international.flashalert\"",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅 Log.i(\"ToggleFlash\", \"ACCESSIBILIY IS DISABLED\") 等日志）",
      "shown_text_zh": "未开启则 ToggleButton 复位为关并写入 SharedPreferences，界面留在主页，不再弹窗、不重复跳转",
      "user_action_requested": "无强制动作；用户可再次拨动开关重新进入引导（非自动循环）",
      "code_anchor": "MainActivity.onActivityResult / MainActivity.isNotificationEnabled"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.dhama.international.flashalert.NotificationService（AccessibilityService）→ MessageReceivedService",
      "trigger_event": "onServiceConnected 设置 AccessibilityServiceInfo（packageNames=com.whatsapp/com.facebook.katana/com.google.android.gsf，eventTypes=64，notificationTimeout=100）；onAccessibilityEvent 收到 TYPE_NOTIFICATION_STATE_CHANGED 后检查 hasSystemFeature(\"android.hardware.camera.flash\") 并 startService(MessageReceivedService, from=notification)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "监听指定三方应用的通知事件，触发相机闪光灯闪烁；未发现自点确认、返回键劫持或阻止撤权行为",
      "user_action_requested": "无",
      "code_anchor": "NotificationService.onServiceConnected / NotificationService.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内由 exitAppDialog1(\"notification\") 创建的原生 Dialog（res/layout/popupscreen.xml），标题/正文运行时被替换为 strings.xml 的 noti_title / noti_text，按钮被硬编码为 Yes / No——这是本样本唯一呈现无障碍引导文案的位置",
    "res/values/strings.xml 中 noti_title=\"Notification Alert\" 与 noti_text=\"Notification requires accessibility service to be on.\\ndo you want to enable notification feature?\"（含换行）",
    "res/layout/popupscreen.xml 默认绑定 exit_title / exit_text，仅在非 exit 分支被覆盖，故同一布局在“评分”场景显示 Rate Us!",
    "系统无障碍设置页：服务未声明 android:label 与 android:description，页面中不呈现任何应用自述用途文字",
    "无 WebView、无 assets HTML、无悬浮窗/遮罩层、无通知栏引导、无 GIF/图片教学"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Notification Alert",
      "text_zh": "通知提醒",
      "source_location": "res/values/strings.xml key=noti_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Notification requires accessibility service to be on.\ndo you want to enable notification feature?",
      "text_zh": "通知功能需要开启无障碍服务。你想启用通知功能吗？",
      "source_location": "res/values/strings.xml key=noti_text",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Yes / No",
      "text_zh": "是 / 否",
      "source_location": "MainActivity.exitAppDialog1 硬编码 setText(\"Yes\") / setText(\"No\")",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Not now / Now",
      "text_zh": "现在不要 / 现在（语义与按钮顺序反转）",
      "source_location": "res/values/strings.xml key=yes_title / no_title（popupscreen.xml 默认绑定，本无障碍路径被硬编码覆盖）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Flash light alerts",
      "text_zh": "闪光灯提醒",
      "source_location": "AndroidManifest.xml application android:label（无障碍服务未单独声明 label/description）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环：点 No 仅关闭对话框并 setChecked(false)；从系统设置返回后 onActivityResult 只做一次 Settings.Secure 校验，未开启则开关复位并留在主页，不重跳、无 Timer 拉起、无 onResume 死循环",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW/悬浮窗、无半透明遮罩、无高仿系统无障碍开关页；跳转后完全交给系统设置页",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无障碍路径无自点确认/无 GLOBAL_ACTION_BACK 或 HOME 撤权阻断；但样本另注册了空策略设备管理器 com.google.android.gms.logs.b（res/xml/admin.xml 仅 <uses-policies />）用于保活与卸载门槛，属独立链路，见 R-001",
    "benign_graceful_degradation": "具降级路径：拒绝后 notification 开关复位且来电/短信闪光功能不受影响，用户可继续使用其余功能；文案直接说明所需能力（通知闪光），未虚构故障、未伪造系统更新"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳时机是“检测到应用拨动通知开关后弹出的原生 Dialog”，即在 MainActivity 前台且界面出现含 accessibility 关键词的原生对话框时拉起 UTG；次优时机为监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS（本样本由 MainActivity.setNotFeature 在点击 Yes 后立即触发，requestCode=100）",
    "key_pages_to_capture": [
      {
        "page_role": "引导说明弹窗页（核心页）",
        "page_identifier": "MainActivity 之上的自定义 Dialog，标题 Notification Alert，正文含 accessibility service，两个按钮 Yes/No，黑色底、非系统 AlertDialog 样式（res/layout/popupscreen.xml）",
        "why_most_useful": "这是全流程唯一呈现引导文案的界面，可直接判定诱导话术性质、是否存在取消路径、按钮文案是否被反转",
        "observable_utg_signals": [
          "对话框文本节点包含 \"accessibility\" 与 \"enable notification feature\"",
          "按钮节点仅 Yes / No，无“稍后/跳过”以外的第三选项",
          "对话框是否不可取消（能否点击外部或返回键关闭）",
          "应用是否同时处于 MainActivity（而非 WebView/Overlay 容器）"
        ]
      },
      {
        "page_role": "跳转前的意图与调用栈",
        "page_identifier": "MainActivity.setNotFeature 发出 Intent action=android.settings.ACCESSIBILITY_SETTINGS，startActivityForResult requestCode=100",
        "why_most_useful": "确认跳转是直接进入无障碍设置页而非应用详情/受限设置页，且是否伴随 setResult(-1) 之类的异常调用",
        "observable_utg_signals": [
          "Intent action 精确等于 android.settings.ACCESSIBILITY_SETTINGS",
          "无 ACTION_APPLICATION_DETAILS_SETTINGS 或 Session 安装器调用",
          "跳转前对话框已 dismiss（无遮罩压栈）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已安装服务中归属 Flash light alerts 的条目，无 description 文本",
        "why_most_useful": "核对系统侧呈现给用户的说明是否为空，判断用户是否只能凭应用名盲选服务，属身份误导的关键观测点",
        "observable_utg_signals": [
          "服务条目下无用途说明文字（android:description 缺失）",
          "条目名称与桌面名 Flash light alerts 的对应关系",
          "开启后是否出现系统确认弹窗及用户实际点击结果"
        ]
      },
      {
        "page_role": "拒权返回后的主界面状态",
        "page_identifier": "返回 MainActivity 后 tglNotification 保持关闭、无新弹窗",
        "why_most_useful": "验证是否存在拒绝循环/定时重跳，是区分“诱导”与“骚扰式强迫”的决定性观测",
        "observable_utg_signals": [
          "返回后 3~10 秒内是否再次出现同一对话框",
          "开关控件状态是否复位为关",
          "是否出现其他弹窗或悬浮层"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本样本无障碍引导链无显著 UTG 盲区（纯文本原生 Dialog，非图片、非 WebView、非加壳）。真正需要另行关注的是同包内独立的高危链：com.google.android.gms.logs.* 组件以 label=\"Plus Service\" 与透明 Activity（Theme.Translucent.NoTitleBar、noHistory）伪装系统组件，经 AlarmManager 6 小时周期拉起并经 sauvl.com 取回远端链接强制弹栈——该链路同样运行期可见但需在“非用户操作触发”时抓取，若只按“用户拨动开关”埋点会漏采。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.dhama.international.flashalert.MainActivity.onCheckedChanged",
    "com.dhama.international.flashalert.MainActivity.exitAppDialog1",
    "com.dhama.international.flashalert.MainActivity.setNotFeature",
    "com.dhama.international.flashalert.MainActivity.isNotificationEnabled",
    "com.dhama.international.flashalert.NotificationService.onServiceConnected",
    "res/layout/popupscreen.xml + res/values/strings.xml(noti_title,noti_text)"
  ]
}
```

</details>
