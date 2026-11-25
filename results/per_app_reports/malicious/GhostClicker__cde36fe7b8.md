# MR_122__cde36fe7b8｜GhostClicker —  Flash Alerts on Call and SMS

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：148.1s

## 1. 一句话核心结论

- **核心申请方式**：闪光提醒外壳应用在用户打开“通知闪光”开关时弹出文案与按钮语义倒置的自绘 Dialog，以“通知功能需要无障碍服务”为由一步直达系统无障碍列表，服务无任何 description/label 说明且仅监听 WhatsApp/Facebook/GSF 通知。
- **静态可见性说明**：全部静态可见：无加壳、无 VMP、无加密 DEX/HTML；无障碍引导弹窗为本地 res/layout/exit_screen.xml + res/values/strings.xml 资源，跳转 Intent 为明文 android.settings.ACCESSIBILITY_SETTINGS，服务实现完整可读。仅 com.google.android.gms.logs.* 内的指令字符串采用 base64 双层解码（z()），属可静态还原的轻量混淆，不影响无障碍链判定。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `cde36fe7b8835a219b3cb87a4c3db3daea84e378fe9f146ddb165b1f488e1135` |
| 包名 / 年份 | `com.flashalertsoncalltt.vnm` / 2017 |
| 家族 / 品类 | **GhostClicker**（同池样本数：4） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/h/ghostclicker-adware-is-a-phantomlike-android-click-fraud.html |
| 桌面显示名 | Flash Alerts on Call and SMS |
| 引导页宣称品牌/身份 | Avlon Mobile Apps 出品的“来电/短信闪光提醒”工具（桌面名首字符为空格；Manifest 内另含伪造 Google GMS 包名组件 com.google.android.gms.logs.*，并以 Google Play services 提示文案作外壳） |
| 系统无障碍列表服务名 | NotificationService（Manifest 未设 android:label，系统列表显示类名派生名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 应用名 android:label 前置一个空格“ Flash Alerts on Call and SMS”，与 strings.xml 的 app_name="Flash Alerts/Notification" 不一致，用于在列表中挤出/规避精确名称比对；2) 无障碍服务既不声明 android:description 也不声明 android:label，系统无障碍列表无任何用途说明；3) 引导弹窗按钮文案与行为倒置——yes_title="Not now" 实为“去开启”，no_title="Now" 实为“关闭页面”；4) 复用“Rate Us”退出弹窗布局 exit_screen.xml 承载权限引导文案；5) 自有恶意组件占用 com.google.android.gms.logs 包名并配以 Google Play services 官方提示字符串；6) Logger 内指令串经 base64 双层编码由 z() 运行时解码。 |
| 无障碍服务类名 | `com.avlon.flashalerts.NotificationService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, RECEIVE_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.avlon.flashalerts.SplashScreenActivity | onCreate（LAUNCHER 入口） | 原生Activity | **原文**：FLASH ON CALL / FLASH ON SMS / RATE US / GET MORE / SHARE<br>**译注**：闪光功能入口页，仅展示应用标题与评分/更多应用/分享按钮，无权限引导 | 点击设置图标进入功能开关页（id 2131034141） | `SplashScreenActivity.onCreate / SplashScreenActivity.onClick` |
| 2 | 业务功能触发 | com.avlon.flashalerts.ToggleFlashSettings（res/layout/setting.xml） | onCreate → addListener() 绑定三个 ToggleButton 的 OnCheckedChangeListener | 原生Activity | **原文**：FLASH ON CALL / FLASH ON SMS / FLASH ON NOTIFICATION<br>**译注**：三个闪光开关页；第三个开关（通知闪光）即无障碍引导触发器 | 用户手动打开“FLASH ON NOTIFICATION”开关（控件 id 2131034133） | `ToggleFlashSettings.addListener / ToggleFlashSettings.bindView` |
| 3 | 引导说明页 | Dialog + res/layout/exit_screen.xml（复用 Rate Us 退出弹窗布局） | onCheckedChanged()：buttonView.getId()==2131034133 且 isChecked 为 true → exitAppDialog("notification") | 原生Dialog | **原文**：notification requires accessibility service to be on.<br>do you want to enable notification feature?  [Not now] [Now]<br>**译注**：通知功能需要开启无障碍服务。你想启用通知功能吗？（左侧按钮显示“Not now”，右侧按钮显示“Now”） | 点击左侧“Not now”按钮（btnYes，实际执行去开启）；右侧“Now”按钮（btnNo）实际为关闭页面，无真正取消语义、无“暂不”降级路径 | `ToggleFlashSettings.onCheckedChanged / ToggleFlashSettings.exitAppDialog / res/values/strings.xml#L37-L40` |
| 4 | 跳无障碍设置 | 系统设置：android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | ToggleFlashSettings$3.onClick：dialog.dismiss() 后调用 setNotFeature() | 系统无障碍页 | **原文**：无（应用内无二次说明页、无 WebView、无图片指引；直接跳系统页）<br>**译注**：直接进入系统无障碍列表，由用户自行找到并勾选 NotificationService（该条目无 description 说明） | 在系统无障碍列表中手动定位并开启 NotificationService | `ToggleFlashSettings.setNotFeature（new Intent("android.settings.ACCESSIBILITY_SETTINGS") + startActivityForResult(…, 100)）` |
| 5 | 拒权反馈循环 | ToggleFlashSettings.onActivityResult（requestCode 100） | 从系统设置页返回时回调 | 原生Activity | 无 | 无强制动作（用户可退出页面） | `ToggleFlashSettings.onActivityResult / ToggleFlashSettings.isNotificationEnabled` |
| 6 | 获权后动作 | com.avlon.flashalerts.NotificationService → com.avlon.flashalerts.MessageReceivedService | onServiceConnected 配置 AccessibilityServiceInfo；onAccessibilityEvent 收到 TYPE_NOTIFICATION_STATE_CHANGED（eventType 64） | 不可静态还原（后台服务，无界面） | 无 | 无 | `NotificationService.onServiceConnected / NotificationService.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- ToggleFlashSettings 内自绘 Dialog（res/layout/exit_screen.xml，标题 id 2131034117 / 正文 2131034118 / 按钮 2131034119、2131034120），文案取自 strings.xml 的 noti_text、yes_title、no_title —— 唯一的无障碍用途说明载体
- res/values/strings.xml 的 noti_text（第 37-38 行）与 yes_title/no_title（第 39-40 行）
- 系统无障碍服务列表条目：Manifest 未设 android:description 与 android:label，条目无任何说明文字（仅显示派生类名 NotificationService）
- res/values/strings.xml 的 sorry_text="Sorry"、feature_text="your device does not support this feature."（设备不支持时的降级提示，与无障碍引导无关）
- 桌面/最近任务名称：Manifest android:label=" Flash Alerts on Call and SMS"（首字符为空格）
- 未发现：WebView/HTML 引导页、悬浮窗遮罩、高仿系统无障碍开关页、图片/GIF 分步教学、通知栏引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | notification requires accessibility service to be on.<br>do you want to enable notification feature? | 通知功能需要开启无障碍服务。你想启用通知功能吗？ | `res/values/strings.xml key=noti_text（第 37-38 行），经 exitAppDialog 写入 tvDialogText` | 良性透明说明 |
| en | Not now | 现在不（但该按钮实际执行“前往无障碍设置开启”） | `res/values/strings.xml key=yes_title（第 39 行），绑定 btnYes(2131034119) → setNotFeature()` | 未知 |
| en | Now | 现在（但该按钮实际执行 finish() 关闭页面） | `res/values/strings.xml key=no_title（第 40 行），绑定 btnNo(2131034120) → ToggleFlashSettings$4.onClick → finish()` | 未知 |
| en | Flash Alerts on Call and SMS | 来电与短信闪光提醒（名称前置一个空格） | `AndroidManifest.xml application/@android:label` | 良性透明说明 |
| en | your device does not support this feature. | 你的设备不支持此功能。 | `res/values/strings.xml key=feature_text（第 42 行）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无死循环。从系统设置页返回时 onActivityResult(100) 仅读取 Settings.Secure.enabled_accessibility_services 判断是否已开启并回写开关状态；未开启则开关回弹为关闭，不自动重新弹窗、不轮询重跳，用户可直接离开页面。
- **遮罩叠层 / 高仿系统设置页**：无。未使用悬浮窗/半透明遮罩叠加在系统设置页之上，也未绘制高仿系统无障碍开关页；引导完全依赖应用内一次性自绘 Dialog + 系统原生无障碍列表。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=19，且代码中无跳转 ACTION_APPLICATION_DETAILS_SETTINGS、无“允许受限设置”菜单教学、无 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：无。NotificationService.onServiceConnected 仅调用 setServiceInfo 配置监听范围；未发现监听设置页后使用 GLOBAL_ACTION_BACK/HOME 阻止撤权，也未自点确认或自授权。
- **良性降级 / 替代方案**：无。引导弹窗不存在真正的“暂不启用”分支：显示“Now”的按钮直接 finish() 关闭整个设置页，显示“Not now”的按钮反而执行去开启，用户无法在不离开页面的前提下继续使用闪光功能；应用层面亦未提供手动闪光/仅来电短信模式作为替代。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：优先在监测到 com.avlon.flashalerts.ToggleFlashSettings 启动后的 UI 树中出现含文本“notification requires accessibility service to be on”的 Dialog 时立即抓取（此时尚未跳转，可完整捕获诱导弹窗与按钮布局）；次级锚点为捕获到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivityForResult（requestCode 100）瞬间，以及随后从系统设置页返回时 ToggleFlashSettings 的 onActivityResult 回写瞬间。冷启动阶段无需布控（无引导）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区不在图文诱饵（全程为纯文本原生 Dialog，无图片/GIF/WebView），而在于：1) 该样本同时含伪 Google GMS 包名的设备管理器组件（com.google.android.gms.logs.Logger/b/c，ACTION_ADD_DEVICE_ADMIN，附多语种“Press 'Activate' to use the application”说明）与 base64 双层编码指令串，纯无障碍 UTG 视角不会覆盖这条独立提权链，需另设 ADD_DEVICE_ADMIN 跳转锚点；2) 无障碍服务在系统列表无任何描述文本，若仅按“description 文本关键词”布控会漏检，须改为按包名/类名条目定位；3) 静态加壳不存在，不构成 UTG 盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **功能开关页触发后的自绘引导弹窗页** | ToggleFlashSettings 之上的 Dialog，根布局为 exit_screen.xml（tvDialogTitle/tvDialogText/btnYes/btnNo），正文含 accessibility service 字样 | 这是整个无障碍引导唯一的说明载体，能同时取证“以功能需要为名索权”与“按钮文案与行为倒置”两个欺骗要点 | 弹窗文本是否出现 accessibility service 且未说明具体读取范围；左侧按钮文本为 Not now 但点击后是否发生跳转（文案/行为倒置）；是否存在真正的取消/跳过分支（点右侧按钮后页面是否直接 finish）；弹窗是否为不可取消（back 键能否关闭） |
| **系统无障碍服务列表条目页** | android.settings.ACCESSIBILITY_SETTINGS 中 com.flashalertsoncalltt.vnm / NotificationService 条目 | 验证系统侧该服务条目是否完全没有用途说明（description 为空），判断用户是否在信息不充分条件下授权 | 条目摘要/描述区域是否为空或仅显示类名；服务名称是否为 NotificationService 派生名而非应用品牌名；列表页是否出现应用叠加的悬浮遮罩或引导层 |
| **授权返回后的开关状态回写页** | ToggleFlashSettings 返回前台，FLASH ON NOTIFICATION 开关状态与 Settings.Secure 读取结果 | 区分“按需软诱导 + 状态回写”与“循环重跳强制”两类行为，确认是否构成拒绝循环 | 返回后是否再次弹出同一引导弹窗；开关是否按 accessibility 实际状态回写；是否存在定时器/onResume 反复拉起系统设置页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.avlon.flashalerts.ToggleFlashSettings.onCheckedChanged`
- `com.avlon.flashalerts.ToggleFlashSettings.exitAppDialog`
- `com.avlon.flashalerts.ToggleFlashSettings.setNotFeature`
- `com.avlon.flashalerts.ToggleFlashSettings.onActivityResult`
- `com.avlon.flashalerts.NotificationService.onServiceConnected`
- `res/layout/exit_screen.xml + res/values/strings.xml#L37-L40`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**整体判断：** 该样本的无障碍引导是“功能开关按需触发 + 自绘原生弹窗 + 直达系统无障碍列表”的单步软诱导，**没有**悬浮遮罩、伪造设置页、`onResume` 循环重跳，也没有 Android 13 受限设置教学。静态完全可见，未加壳。

**关键流程（已逐环核实）**
1. 冷启动 [SplashScreenActivity.onCreate()](<resource-unit:#1.dex1 code:com.avlon.flashalerts.SplashScreenActivity#onCreate>) 只加载广告和入口按钮，**无任何权限引导**。
2. 点击设置入口进入 [ToggleFlashSettings](<resource-unit:#1.dex1 code:com.avlon.flashalerts.ToggleFlashSettings#onCreate>)。
3. 用户打开 “FLASH ON NOTIFICATION” 开关（id `2131034133`）时，[onCheckedChanged()](<resource-unit:#1.dex1 code:com.avlon.flashalerts.ToggleFlashSettings#onCheckedChanged>) **不保存偏好**，直接调用 `exitAppDialog("notification")` 弹出引导框。
4. [exitAppDialog()](<resource-unit:#1.dex1 code:com.avlon.flashalerts.ToggleFlashSettings#exitAppDialog>) 用 `Dialog` 复用 [exit_screen.xml](<resource-unit:#1 file:res/layout/exit_screen.xml#L5-L16>)（“Rate Us” 布局），动态把标题/正文/按钮替换为 `noti_text` / `yes_title` / `no_title`。
5. 点击左侧按钮（btnYes）时，[ToggleFlashSettings$3.onClick()](<resource-unit:#1.dex1 code:com.avlon.flashalerts.ToggleFlashSettings$3#onClick>) 执行 `dismiss()`，再调用 [setNotFeature()](<resource-unit:#1.dex1 code:com.avlon.flashalerts.ToggleFlashSettings#setNotFeature>) → `startActivityForResult(Intent("android.settings.ACCESSIBILITY_SETTINGS"), 100)`。
6. 从系统页返回后，[onActivityResult()](<resource-unit:#1.dex1 code:com.avlon.flashalerts.ToggleFlashSettings#onActivityResult>) 用 [isNotificationEnabled()](<resource-unit:#1.dex1 code:com.avlon.flashalerts.ToggleFlashSettings#isNotificationEnabled>) 读取 `Settings.Secure.enabled_accessibility_services` 做包名子串匹配，并回写开关状态；**无强制重跳**。
7. 获权后，[NotificationService.onServiceConnected()](<resource-unit:#1.dex1 code:com.avlon.flashalerts.NotificationService#onServiceConnected>) 仅将 `packageNames` 限定为 WhatsApp、Facebook、GSF，`eventTypes=64`（通知状态变化），触发 `MessageReceivedService` 闪光。

**欺骗与身份要点**
- 桌面名 `" Flash Alerts on Call and SMS"` **前置一个空格**，用于在列表中挤出/规避精确匹配；`app_name` 资源却是 `Flash Alerts/Notification`。
- 无障碍服务在 Manifest 中**既无 `android:description` 也无 `android:label`**，系统无障碍列表只能显示类名派生名 `NotificationService`，用户看不到任何用途说明，唯一说明来自应用内自绘弹窗。
- 按钮文案与行为**倒置**：[strings.xml (lines 37-40)](<resource-unit:#1 file:res/values/strings.xml#L37-L40>) 中 `yes_title="Not now"`（btnYes，实际执行去开启），`no_title="Now"`（btnNo，实际 `finish()` 关页面）。

**范围外的旁证（同一 APK，非无障碍链）**：Manifest 中 `com.google.android.gms.logs.Logger`（Activity）、`com.google.android.gms.logs.b`（DeviceAdminReceiver）、`com.google.android.gms.logs.c`（Service）是**伪造 Google GMS 包名的自有组件**；[Logger.onCreate()](<resource-unit:#1.dex1 code:com.google.android.gms.logs.Logger#onCreate>) 用 base64 双层解码（`z()`）还原指令串，遇到 `show_admin` 时由 [Logger.d()](<resource-unit:#1.dex1 code:com.google.android.gms.logs.Logger#d) 发起 `ACTION_ADD_DEVICE_ADMIN`，附带多语种“Press 'Activate' to use the application”说明——属独立命题，本次按主题边界未单独登记。

**覆盖边界**：弹窗文本经资源 id（2131099680/682/693/694）引用，已映射到上述 strings；未做运行期截图/UTG 实测验证。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部静态可见：无加壳、无 VMP、无加密 DEX/HTML；无障碍引导弹窗为本地 res/layout/exit_screen.xml + res/values/strings.xml 资源，跳转 Intent 为明文 android.settings.ACCESSIBILITY_SETTINGS，服务实现完整可读。仅 com.google.android.gms.logs.* 内的指令字符串采用 base64 双层解码（z()），属可静态还原的轻量混淆，不影响无障碍链判定。",
  "summary_one_liner": "闪光提醒外壳应用在用户打开“通知闪光”开关时弹出文案与按钮语义倒置的自绘 Dialog，以“通知功能需要无障碍服务”为由一步直达系统无障碍列表，服务无任何 description/label 说明且仅监听 WhatsApp/Facebook/GSF 通知。",
  "disguise_identity": {
    "app_display_name": " Flash Alerts on Call and SMS",
    "claimed_brand_or_persona": "Avlon Mobile Apps 出品的“来电/短信闪光提醒”工具（桌面名首字符为空格；Manifest 内另含伪造 Google GMS 包名组件 com.google.android.gms.logs.*，并以 Google Play services 提示文案作外壳）",
    "a11y_service_label": "NotificationService（Manifest 未设 android:label，系统列表显示类名派生名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 应用名 android:label 前置一个空格“ Flash Alerts on Call and SMS”，与 strings.xml 的 app_name=\"Flash Alerts/Notification\" 不一致，用于在列表中挤出/规避精确名称比对；2) 无障碍服务既不声明 android:description 也不声明 android:label，系统无障碍列表无任何用途说明；3) 引导弹窗按钮文案与行为倒置——yes_title=\"Not now\" 实为“去开启”，no_title=\"Now\" 实为“关闭页面”；4) 复用“Rate Us”退出弹窗布局 exit_screen.xml 承载权限引导文案；5) 自有恶意组件占用 com.google.android.gms.logs 包名并配以 Google Play services 官方提示字符串；6) Logger 内指令串经 base64 双层编码由 z() 运行时解码。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.avlon.flashalerts.SplashScreenActivity",
      "trigger_event": "onCreate（LAUNCHER 入口）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "FLASH ON CALL / FLASH ON SMS / RATE US / GET MORE / SHARE",
      "shown_text_zh": "闪光功能入口页，仅展示应用标题与评分/更多应用/分享按钮，无权限引导",
      "user_action_requested": "点击设置图标进入功能开关页（id 2131034141）",
      "code_anchor": "SplashScreenActivity.onCreate / SplashScreenActivity.onClick"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.avlon.flashalerts.ToggleFlashSettings（res/layout/setting.xml）",
      "trigger_event": "onCreate → addListener() 绑定三个 ToggleButton 的 OnCheckedChangeListener",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "FLASH ON CALL / FLASH ON SMS / FLASH ON NOTIFICATION",
      "shown_text_zh": "三个闪光开关页；第三个开关（通知闪光）即无障碍引导触发器",
      "user_action_requested": "用户手动打开“FLASH ON NOTIFICATION”开关（控件 id 2131034133）",
      "code_anchor": "ToggleFlashSettings.addListener / ToggleFlashSettings.bindView"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "Dialog + res/layout/exit_screen.xml（复用 Rate Us 退出弹窗布局）",
      "trigger_event": "onCheckedChanged()：buttonView.getId()==2131034133 且 isChecked 为 true → exitAppDialog(\"notification\")",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "notification requires accessibility service to be on.\ndo you want to enable notification feature?  [Not now] [Now]",
      "shown_text_zh": "通知功能需要开启无障碍服务。你想启用通知功能吗？（左侧按钮显示“Not now”，右侧按钮显示“Now”）",
      "user_action_requested": "点击左侧“Not now”按钮（btnYes，实际执行去开启）；右侧“Now”按钮（btnNo）实际为关闭页面，无真正取消语义、无“暂不”降级路径",
      "code_anchor": "ToggleFlashSettings.onCheckedChanged / ToggleFlashSettings.exitAppDialog / res/values/strings.xml#L37-L40"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置：android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "ToggleFlashSettings$3.onClick：dialog.dismiss() 后调用 setNotFeature()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用内无二次说明页、无 WebView、无图片指引；直接跳系统页）",
      "shown_text_zh": "直接进入系统无障碍列表，由用户自行找到并勾选 NotificationService（该条目无 description 说明）",
      "user_action_requested": "在系统无障碍列表中手动定位并开启 NotificationService",
      "code_anchor": "ToggleFlashSettings.setNotFeature（new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + startActivityForResult(…, 100)）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "ToggleFlashSettings.onActivityResult（requestCode 100）",
      "trigger_event": "从系统设置页返回时回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "返回后读取 Settings.Secure.enabled_accessibility_services，按包名子串判断是否已开启并回写开关勾选状态；未开启则开关回弹为关闭，不重复弹窗、不循环重跳",
      "user_action_requested": "无强制动作（用户可退出页面）",
      "code_anchor": "ToggleFlashSettings.onActivityResult / ToggleFlashSettings.isNotificationEnabled"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.avlon.flashalerts.NotificationService → com.avlon.flashalerts.MessageReceivedService",
      "trigger_event": "onServiceConnected 配置 AccessibilityServiceInfo；onAccessibilityEvent 收到 TYPE_NOTIFICATION_STATE_CHANGED（eventType 64）",
      "ui_carrier": "不可静态还原（后台服务，无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务将监听范围限定为 com.whatsapp、com.facebook.katana、com.google.android.gsf 的通知，命中后启动 MessageReceivedService 调用摄像头闪光；未观察到自点确认、自动授权或拦截撤权行为",
      "user_action_requested": "无",
      "code_anchor": "NotificationService.onServiceConnected / NotificationService.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "ToggleFlashSettings 内自绘 Dialog（res/layout/exit_screen.xml，标题 id 2131034117 / 正文 2131034118 / 按钮 2131034119、2131034120），文案取自 strings.xml 的 noti_text、yes_title、no_title —— 唯一的无障碍用途说明载体",
    "res/values/strings.xml 的 noti_text（第 37-38 行）与 yes_title/no_title（第 39-40 行）",
    "系统无障碍服务列表条目：Manifest 未设 android:description 与 android:label，条目无任何说明文字（仅显示派生类名 NotificationService）",
    "res/values/strings.xml 的 sorry_text=\"Sorry\"、feature_text=\"your device does not support this feature.\"（设备不支持时的降级提示，与无障碍引导无关）",
    "桌面/最近任务名称：Manifest android:label=\" Flash Alerts on Call and SMS\"（首字符为空格）",
    "未发现：WebView/HTML 引导页、悬浮窗遮罩、高仿系统无障碍开关页、图片/GIF 分步教学、通知栏引导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "notification requires accessibility service to be on.\ndo you want to enable notification feature?",
      "text_zh": "通知功能需要开启无障碍服务。你想启用通知功能吗？",
      "source_location": "res/values/strings.xml key=noti_text（第 37-38 行），经 exitAppDialog 写入 tvDialogText",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Not now",
      "text_zh": "现在不（但该按钮实际执行“前往无障碍设置开启”）",
      "source_location": "res/values/strings.xml key=yes_title（第 39 行），绑定 btnYes(2131034119) → setNotFeature()",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Now",
      "text_zh": "现在（但该按钮实际执行 finish() 关闭页面）",
      "source_location": "res/values/strings.xml key=no_title（第 40 行），绑定 btnNo(2131034120) → ToggleFlashSettings$4.onClick → finish()",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": " Flash Alerts on Call and SMS",
      "text_zh": "来电与短信闪光提醒（名称前置一个空格）",
      "source_location": "AndroidManifest.xml application/@android:label",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "your device does not support this feature.",
      "text_zh": "你的设备不支持此功能。",
      "source_location": "res/values/strings.xml key=feature_text（第 42 行）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无死循环。从系统设置页返回时 onActivityResult(100) 仅读取 Settings.Secure.enabled_accessibility_services 判断是否已开启并回写开关状态；未开启则开关回弹为关闭，不自动重新弹窗、不轮询重跳，用户可直接离开页面。",
    "overlay_or_fake_settings": "无。未使用悬浮窗/半透明遮罩叠加在系统设置页之上，也未绘制高仿系统无障碍开关页；引导完全依赖应用内一次性自绘 Dialog + 系统原生无障碍列表。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=19，且代码中无跳转 ACTION_APPLICATION_DETAILS_SETTINGS、无“允许受限设置”菜单教学、无 Session 安装器绕过）",
    "post_grant_anti_removal": "无。NotificationService.onServiceConnected 仅调用 setServiceInfo 配置监听范围；未发现监听设置页后使用 GLOBAL_ACTION_BACK/HOME 阻止撤权，也未自点确认或自授权。",
    "benign_graceful_degradation": "无。引导弹窗不存在真正的“暂不启用”分支：显示“Now”的按钮直接 finish() 关闭整个设置页，显示“Not now”的按钮反而执行去开启，用户无法在不离开页面的前提下继续使用闪光功能；应用层面亦未提供手动闪光/仅来电短信模式作为替代。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "优先在监测到 com.avlon.flashalerts.ToggleFlashSettings 启动后的 UI 树中出现含文本“notification requires accessibility service to be on”的 Dialog 时立即抓取（此时尚未跳转，可完整捕获诱导弹窗与按钮布局）；次级锚点为捕获到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivityForResult（requestCode 100）瞬间，以及随后从系统设置页返回时 ToggleFlashSettings 的 onActivityResult 回写瞬间。冷启动阶段无需布控（无引导）。",
    "key_pages_to_capture": [
      {
        "page_role": "功能开关页触发后的自绘引导弹窗页",
        "page_identifier": "ToggleFlashSettings 之上的 Dialog，根布局为 exit_screen.xml（tvDialogTitle/tvDialogText/btnYes/btnNo），正文含 accessibility service 字样",
        "why_most_useful": "这是整个无障碍引导唯一的说明载体，能同时取证“以功能需要为名索权”与“按钮文案与行为倒置”两个欺骗要点",
        "observable_utg_signals": [
          "弹窗文本是否出现 accessibility service 且未说明具体读取范围",
          "左侧按钮文本为 Not now 但点击后是否发生跳转（文案/行为倒置）",
          "是否存在真正的取消/跳过分支（点右侧按钮后页面是否直接 finish）",
          "弹窗是否为不可取消（back 键能否关闭）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表条目页",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 中 com.flashalertsoncalltt.vnm / NotificationService 条目",
        "why_most_useful": "验证系统侧该服务条目是否完全没有用途说明（description 为空），判断用户是否在信息不充分条件下授权",
        "observable_utg_signals": [
          "条目摘要/描述区域是否为空或仅显示类名",
          "服务名称是否为 NotificationService 派生名而非应用品牌名",
          "列表页是否出现应用叠加的悬浮遮罩或引导层"
        ]
      },
      {
        "page_role": "授权返回后的开关状态回写页",
        "page_identifier": "ToggleFlashSettings 返回前台，FLASH ON NOTIFICATION 开关状态与 Settings.Secure 读取结果",
        "why_most_useful": "区分“按需软诱导 + 状态回写”与“循环重跳强制”两类行为，确认是否构成拒绝循环",
        "observable_utg_signals": [
          "返回后是否再次弹出同一引导弹窗",
          "开关是否按 accessibility 实际状态回写",
          "是否存在定时器/onResume 反复拉起系统设置页"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区不在图文诱饵（全程为纯文本原生 Dialog，无图片/GIF/WebView），而在于：1) 该样本同时含伪 Google GMS 包名的设备管理器组件（com.google.android.gms.logs.Logger/b/c，ACTION_ADD_DEVICE_ADMIN，附多语种“Press 'Activate' to use the application”说明）与 base64 双层编码指令串，纯无障碍 UTG 视角不会覆盖这条独立提权链，需另设 ADD_DEVICE_ADMIN 跳转锚点；2) 无障碍服务在系统列表无任何描述文本，若仅按“description 文本关键词”布控会漏检，须改为按包名/类名条目定位；3) 静态加壳不存在，不构成 UTG 盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "LURE_DISMISS_SYSTEM_WARNING"
  ],
  "code_anchors": [
    "com.avlon.flashalerts.ToggleFlashSettings.onCheckedChanged",
    "com.avlon.flashalerts.ToggleFlashSettings.exitAppDialog",
    "com.avlon.flashalerts.ToggleFlashSettings.setNotFeature",
    "com.avlon.flashalerts.ToggleFlashSettings.onActivityResult",
    "com.avlon.flashalerts.NotificationService.onServiceConnected",
    "res/layout/exit_screen.xml + res/values/strings.xml#L37-L40"
  ]
}
```

</details>
