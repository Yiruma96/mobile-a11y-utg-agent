# MR_179__eed48f54be｜Xavier — Lollipop Launcher

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：135.5s

## 1. 一句话核心结论

- **核心申请方式**：该桌面应用采用用户主动开启功能后的透明说明型引导：点击通知栏克隆或自动休眠开关弹出说明对话框，用户确认后直接跳转系统 ACTION_ACCESSIBILITY_SETTINGS，无冷启动强制、无遮罩、无拒绝循环。
- **静态可见性说明**：无障碍引导全链路（Manifest 服务声明、xml 配置、strings 文案、跳转 onClick 实现）均在 classes.dex 与 res 中静态完整可见，未加壳、无 AES/远端 HTML 参与该流程；assets 下仅 help.html/about.html/licenses.html/translations.html 等本地说明页，与无障碍引导无关。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `eed48f54be3778b408f77c5416b3aad2bd3f715c72b574847e57690f847af021` |
| 包名 / 年份 | `com.minfivezz.launcher` / 2017 |
| 家族 / 品类 | **Xavier**（同池样本数：41） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/f/analyzing-xavier-information-stealing-ad-library-android.html |
| 桌面显示名 | Lollipop Launcher |
| 引导页宣称品牌/身份 | Lollipop Launcher（Android 5.0 风格桌面，基于 Android 4.4 的 KK Launcher 换皮） |
| 系统无障碍列表服务名 | Lollipop Launcher Accessibility Service（由 @string/accessibility_service_description 描述：To activate notification, please turn on Lollipop Launcher Accessibility Service on Accessibility Setting.） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。仅存在换皮残留：包名 com.minfivezz.launcher、内部 scheme kk_launcher_custompageview/kk_setting 源自 KK Launcher，且 start_service_details 文案仍写 AFast Launcher Accessibility Service（他名残留），属打包残留而非针对性伪装。 |
| 无障碍服务类名 | `com.minfivezz.accessibility.NotificationAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, READ_CONTACTS, READ_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | To activate notification, please turn on Lollipop Launcher Accessibility Service on Accessibility Setting. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.minfivezz.launcher.setting.pref.CommonPrefActivity / LauncherSetting（桌面设置-显示通知开关） | 用户在设置中切换“Show Notification”项，应用检测无障碍服务未启用时弹出确认对话框 | 原生Dialog | **原文**：To activate notification, please turn on Lollipop Launcher Accessibility Service on Accessibility Setting. <br>Do you want to open Accessibility Settings?<br>**译注**：要激活通知显示，请在无障碍设置中开启 Lollipop Launcher 无障碍服务。是否要打开无障碍设置？ | 点击“确定”打开系统无障碍设置；系统对话框自带“取消”，可跳过 | `res/values/strings.xml#pref_desktop_show_notification_content / com.minfivezz.launcher.ul#onClick` |
| 2 | 跳无障碍设置 | 系统设置 com.android.settings 无障碍服务列表页 | DialogInterface.OnClickListener 点击后执行 startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 2) | 系统无障碍页 | **原文**：无（跳转系统页，文案由系统渲染，服务项描述取 @string/accessibility_service_description）<br>**译注**：系统无障碍列表中出现 “Lollipop Launcher Accessibility Service” 条目，用户需手动开启开关 | 用户在系统列表中手动找到并开启服务开关，或返回放弃 | `com.minfivezz.launcher.ul#onClick` |
| 3 | 业务功能触发 | com.minfivezz.pusianwidget.toolbox.battery.HibernateActivity（电池工具箱-自动休眠） | 用户点击“Auto”按钮（start_service），弹出自定义说明对话框，含“Auto / Manually”两个按钮 | 原生Dialog | **原文**：To Auto-hibernate the selected apps, please turn on AFast Launcher Accessibility Service: <br><br> 1. Click bellow "Auto", <br> 2. Find the AFast Launcher in the list, click the item, <br> 3. Enable the switch on Top-Right bar<br><br> (If you click "Manually", please click "Force stop" manually to hibernate app)<br>**译注**：要自动休眠所选应用，请开启 AFast Launcher 无障碍服务：1. 点击下方“Auto”；2. 在列表中找到 AFast Launcher 并点击该项；3. 打开右上角开关。（若点击“Manually”，请手动点击“强制停止”来休眠应用） | 点击“Auto”跳转无障碍设置；或选择“Manually”走应用详情页手动强制停止（显式降级路径） | `res/values/strings.xml#start_service_details / com.minfivezz.pusianwidget.toolbox.battery.q#onClick` |
| 4 | 跳无障碍设置 | 系统设置无障碍服务列表页 | 用户点击“Auto”后执行 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | 无 | 手动开启或返回放弃；选择 Manually 时改跳 APPLICATION_DETAILS_SETTINGS 由用户点“强制停止” | `com.minfivezz.pusianwidget.toolbox.battery.q#onClick` |
| 5 | 获权后动作 | com.minfivezz.accessibility.NotificationAccessibilityService | 服务被系统绑定后接收 typeNotificationStateChanged / typeWindowStateChanged 事件（notificationTimeout=100ms） | 无界面（后台服务） | 无 | 无额外操作；未发现获权后自点确认、自授权或阻止撤权行为 | `res/xml/notification_accessibility_service.xml#L2 / AndroidManifest.xml service com.minfivezz.accessibility.NotificationAccessibilityService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目描述：@string/accessibility_service_description（res/xml/notification_accessibility_service.xml 的 android:description）
- 桌面设置“显示通知”开关后的原生 AlertDialog：@string/pref_desktop_show_notification_content（由 com.minfivezz.launcher.ul#onClick 处理按钮）
- 设置项摘要文本：@string/pref_desktop_show_notification_summary（Show notification on transparent status bar clone）
- 电池工具箱休眠页“Auto”按钮后的原生说明对话框：@string/start_service_details（含 3 步教学与 Manually 替代项）
- 休眠帮助标题/按钮：@string/start_hibernate_help（Notice）、@string/manually、@string/auto、@string/hibernate_notice_get（Got it）
- 设置项标题：@string/pref_more_enable_accessibility_title（Enable accessibility）
- assets/help.html、about.html、licenses.html、translations.html 为纯本地帮助/开源许可页，未承载无障碍引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To activate notification, please turn on Lollipop Launcher Accessibility Service on Accessibility Setting. | 要激活通知显示，请在无障碍设置中开启 Lollipop Launcher 无障碍服务。 | `res/values/strings.xml key=accessibility_service_description（同时作为 android:description 显示在系统无障碍列表）` | 良性透明说明 |
| en | To activate notification, please turn on Lollipop Launcher Accessibility Service on Accessibility Setting. <br>Do you want to open Accessibility Settings? | 要激活通知显示，请在无障碍设置中开启 Lollipop Launcher 无障碍服务。是否要打开无障碍设置？ | `res/values/strings.xml key=pref_desktop_show_notification_content` | 良性透明说明 |
| en | To Auto-hibernate the selected apps, please turn on AFast Launcher Accessibility Service: <br><br> 1. Click bellow "Auto", <br> 2. Find the AFast Launcher in the list, click the item, <br> 3. Enable the switch on Top-Right bar<br><br> (If you click "Manually", please click "Force stop" manually to hibernate app) | 要自动休眠所选应用，请开启 AFast Launcher 无障碍服务：1. 点击下方“Auto”；2. 在列表中找到 AFast Launcher 并点击该项；3. 打开右上角开关。（若点击“Manually”，请手动点击“强制停止”来休眠应用） | `res/values/strings.xml key=start_service_details` | 受限设置分步教学 |
| en | Show notification on transparent status bar clone | 在透明状态栏克隆上显示通知 | `res/values/strings.xml key=pref_desktop_show_notification_summary` | 良性透明说明 |
| en | The "App info" window will popup, please click "Force stop" to hibernate the app. | 将弹出“应用信息”窗口，请点击“强制停止”来休眠该应用。 | `res/values/strings.xml key=start_hibernate_details_bellow_android4_2` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无拒绝循环。跳转采用 startActivityForResult 后不重试；未发现 onResume/Timer 定时重跳或返回即弹回逻辑。用户取消对话框或从系统设置返回后仅保持功能未启用状态。
- **遮罩叠层 / 高仿系统设置页**：无。未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 权限存在但未用于此引导链路。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdk 23（minSdk 14），无 Android 13+ 受限设置教学，也无 Session 安装器绕过；APPLICATION_DETAILS_SETTINGS 跳转仅用于“应用信息-强制停止”手动休眠路径（Launcher#a、HibernateActivity#h）。
- **获权后即时行为与防撤权机制**：无。未发现获权后自点确认、自授权，或用 GLOBAL_ACTION_BACK/HOME 监听设置页阻止撤权；服务 canRetrieveWindowContent=false，未声明读取窗口内容能力。
- **良性降级 / 替代方案**：有。休眠功能提供“Manually”分支：不开启无障碍时跳转应用详情页由用户手动点“强制停止”完成同等效果；通知克隆功能不开启时仅不显示通知，桌面其余功能正常。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：纯 UTG 检测应在监测到应用发起 android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间拉起（或在其前一步抓取 LauncherSetting/HibernateActivity 上的说明对话框），二者可在同一次会话内顺序捕获。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本流程无纯图空文本诱导，文案均为可提取文本。潜在盲区：android:enabled 由 @bool/accesibility_service_enabled 资源控制，若该布尔在部分渠道包中被置 false，服务项可能在系统列表不可见，导致 UTG 抓取不到列表条目；另本轮未覆盖同一应用的通知栏工具、更新弹窗与 gameApps.db 相关外发行为，其恶意性需独立运行期验证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前说明对话框页（桌面设置-显示通知）** | LauncherSetting 上覆盖的原生 AlertDialog，正文含 "Lollipop Launcher Accessibility Service" 与 "Do you want to open Accessibility Settings?"，含确定/取消两按钮 | 该页是判定“透明说明 vs 恐吓诱导”的关键：文案是否如实说明服务用途、是否提供取消，可直接区分良性引导与恶意逼权 | 对话框正文关键词 Lollipop Launcher Accessibility Service；存在取消按钮（可跳过）；无“更新/病毒/故障”等恐吓词 |
| **跳转前分步教学对话框页（电池工具箱-自动休眠）** | HibernateActivity 上的自定义 Dialog，含 "1. Click bellow Auto"、"2. Find the AFast Launcher in the list"、"3. Enable the switch on Top-Right bar"，并有 Auto/Manually 两按钮 | 识别“分步教学式逼权”与替代路径：既有系统设置操作教学，也提供 Manually 手动降级，可据按钮结构判定是否给用户留退路 | Auto 与 Manually 双按钮并存；教学文案序号 1/2/3；文案中出现的服务名 AFast Launcher 与实际 Lollipop Launcher 不一致 |
| **系统无障碍服务列表项** | Settings 无障碍页中 "Lollipop Launcher Accessibility Service" 条目及其描述文字 | 核对系统实际展示的服务名与描述是否与对话框宣称一致，检测是否有名称混淆或空白/换行挤出 | 条目名称与包名 com.minfivezz.launcher 对应关系；描述文本是否与 accessibility_service_description 完全一致；是否存在空名称或异常空白条目 |
| **跳转后返回态页面** | 从系统设置返回后的 LauncherSetting / HibernateActivity 界面 | 验证是否存在拒绝循环重跳、遮罩叠层或强制停留 | 返回后 2 秒内是否再次弹出对话框或重跳设置；是否出现悬浮遮罩覆盖界面；是否出现“必须开启”类不可取消提示 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.minfivezz.launcher.ul#onClick`
- `com.minfivezz.pusianwidget.toolbox.battery.q#onClick`
- `res/xml/notification_accessibility_service.xml`
- `res/values/strings.xml (accessibility_service_description / pref_desktop_show_notification_content / start_service_details)`
- `com.minfivezz.accessibility.NotificationAccessibilityService`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（约 18 次工具调用，其中 MCP 并发繁忙重试 3 次）。结论如下。

## 结论要点

**无障碍申请方式：用户主动触发的“功能开启式”引导，无冷启动强制弹窗、无遮罩叠层、无拒绝循环、无受限设置教学。** 静态完整可见（DEX 未加壳，无加密载荷参与此流程）。

1. **服务声明**：[notification_accessibility_service.xml](<resource-unit:#1 file:res/xml/notification_accessibility_service.xml#L2>) 声明 `typeNotificationStateChanged|typeWindowStateChanged`、`canRetrieveWindowContent="false"`、`notificationTimeout=100`——仅为读取通知/窗口状态，不能读取窗口内容。`android:enabled="@bool/accesibility_service_enabled"` 由资源布尔控制，非硬编码启用。
2. **两条独立的跳转点**（均为用户点击“开启/自动”后的确认对话框按钮）：
   - 桌面“透明状态栏克隆显示通知”设置项：[com.minfivezz.launcher.ul#onClick](<resource-unit:#1.dex1 code:com.minfivezz.launcher.ul#onClick>) → `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 2)`，宿主为 `LauncherSetting`。
   - 电池工具箱“自动休眠应用”：[com.minfivezz.pusianwidget.toolbox.battery.q#onClick](<resource-unit:#1.dex1 code:com.minfivezz.pusianwidget.toolbox.battery.q#onClick>) → `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，宿主为 `HibernateActivity`。
3. **文案性质：良性透明说明 + 分步教学**。`accessibility_service_description` 与 `pref_desktop_show_notification_content` 明确说明“请在无障碍设置中开启 Lollipop Launcher 无障碍服务以激活通知”，并直接询问“是否打开无障碍设置？”；`start_service_details` 给出 3 步图文式操作说明（点 Auto → 列表找服务 → 打开右上开关），并保留“Manually”手动替代路径（点“强制停止”手动休眠）——属显式降级选项。
4. **身份不一致但非恶意伪装**：显示名/文案为 `Lollipop Launcher`，包名 `com.minfivezz.launcher`，内部 scheme 为 `kk_launcher_custompageview`/`kk_setting`（源自 KK Launcher 换皮），且 `start_service_details` 中残留“**AFast Launcher** Accessibility Service”他名残留——命名混杂，属换皮残留痕迹，未发现空白/换行挤出警告、同形字或多 alias 掩盖。
5. **未发现**：`isAccessibilityTool` 伪造（targetSdk 23，早于 Android 14 机制）、`APPLICATION_DETAILS_SETTINGS` 用于 13+ 受限设置教学（该跳转仅用于“应用信息/强制停止”，见 `Launcher#a`、`HibernateActivity#h`）、获权后自点确认或监听设置页阻止撤权。
6. **覆盖边界**：本结论仅覆盖“无障碍申请引导链路”。该样本 Manifest 另声明 `READ_SMS/READ_CONTACTS/CALL_PHONE/CAMERA/SYSTEM_ALERT_WINDOW/WRITE_SETTINGS` 与 `NotificationToolbar`、`update.CheckUpdateActivity`、`gameApps.db` 等组件，其数据外发与广告/静默安装行为未在本轮核查范围内，需另行审计。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（Manifest 服务声明、xml 配置、strings 文案、跳转 onClick 实现）均在 classes.dex 与 res 中静态完整可见，未加壳、无 AES/远端 HTML 参与该流程；assets 下仅 help.html/about.html/licenses.html/translations.html 等本地说明页，与无障碍引导无关。",
  "summary_one_liner": "该桌面应用采用用户主动开启功能后的透明说明型引导：点击通知栏克隆或自动休眠开关弹出说明对话框，用户确认后直接跳转系统 ACTION_ACCESSIBILITY_SETTINGS，无冷启动强制、无遮罩、无拒绝循环。",
  "disguise_identity": {
    "app_display_name": "Lollipop Launcher",
    "claimed_brand_or_persona": "Lollipop Launcher（Android 5.0 风格桌面，基于 Android 4.4 的 KK Launcher 换皮）",
    "a11y_service_label": "Lollipop Launcher Accessibility Service（由 @string/accessibility_service_description 描述：To activate notification, please turn on Lollipop Launcher Accessibility Service on Accessibility Setting.）",
    "identity_mismatch": false,
    "obfuscation_tricks": "未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。仅存在换皮残留：包名 com.minfivezz.launcher、内部 scheme kk_launcher_custompageview/kk_setting 源自 KK Launcher，且 start_service_details 文案仍写 AFast Launcher Accessibility Service（他名残留），属打包残留而非针对性伪装。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.minfivezz.launcher.setting.pref.CommonPrefActivity / LauncherSetting（桌面设置-显示通知开关）",
      "trigger_event": "用户在设置中切换“Show Notification”项，应用检测无障碍服务未启用时弹出确认对话框",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "To activate notification, please turn on Lollipop Launcher Accessibility Service on Accessibility Setting. \nDo you want to open Accessibility Settings?",
      "shown_text_zh": "要激活通知显示，请在无障碍设置中开启 Lollipop Launcher 无障碍服务。是否要打开无障碍设置？",
      "user_action_requested": "点击“确定”打开系统无障碍设置；系统对话框自带“取消”，可跳过",
      "code_anchor": "res/values/strings.xml#pref_desktop_show_notification_content / com.minfivezz.launcher.ul#onClick"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 com.android.settings 无障碍服务列表页",
      "trigger_event": "DialogInterface.OnClickListener 点击后执行 startActivityForResult(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), 2)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转系统页，文案由系统渲染，服务项描述取 @string/accessibility_service_description）",
      "shown_text_zh": "系统无障碍列表中出现 “Lollipop Launcher Accessibility Service” 条目，用户需手动开启开关",
      "user_action_requested": "用户在系统列表中手动找到并开启服务开关，或返回放弃",
      "code_anchor": "com.minfivezz.launcher.ul#onClick"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "com.minfivezz.pusianwidget.toolbox.battery.HibernateActivity（电池工具箱-自动休眠）",
      "trigger_event": "用户点击“Auto”按钮（start_service），弹出自定义说明对话框，含“Auto / Manually”两个按钮",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "To Auto-hibernate the selected apps, please turn on AFast Launcher Accessibility Service: \n\n 1. Click bellow \"Auto\", \n 2. Find the AFast Launcher in the list, click the item, \n 3. Enable the switch on Top-Right bar\n\n (If you click \"Manually\", please click \"Force stop\" manually to hibernate app)",
      "shown_text_zh": "要自动休眠所选应用，请开启 AFast Launcher 无障碍服务：1. 点击下方“Auto”；2. 在列表中找到 AFast Launcher 并点击该项；3. 打开右上角开关。（若点击“Manually”，请手动点击“强制停止”来休眠应用）",
      "user_action_requested": "点击“Auto”跳转无障碍设置；或选择“Manually”走应用详情页手动强制停止（显式降级路径）",
      "code_anchor": "res/values/strings.xml#start_service_details / com.minfivezz.pusianwidget.toolbox.battery.q#onClick"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置无障碍服务列表页",
      "trigger_event": "用户点击“Auto”后执行 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳转系统无障碍列表，由用户手动开启服务开关",
      "user_action_requested": "手动开启或返回放弃；选择 Manually 时改跳 APPLICATION_DETAILS_SETTINGS 由用户点“强制停止”",
      "code_anchor": "com.minfivezz.pusianwidget.toolbox.battery.q#onClick"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.minfivezz.accessibility.NotificationAccessibilityService",
      "trigger_event": "服务被系统绑定后接收 typeNotificationStateChanged / typeWindowStateChanged 事件（notificationTimeout=100ms）",
      "ui_carrier": "无界面（后台服务）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅读取通知与窗口状态变化用于透明状态栏克隆显示通知、自动休眠判定；canRetrieveWindowContent=false，不读取界面内容",
      "user_action_requested": "无额外操作；未发现获权后自点确认、自授权或阻止撤权行为",
      "code_anchor": "res/xml/notification_accessibility_service.xml#L2 / AndroidManifest.xml service com.minfivezz.accessibility.NotificationAccessibilityService"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目描述：@string/accessibility_service_description（res/xml/notification_accessibility_service.xml 的 android:description）",
    "桌面设置“显示通知”开关后的原生 AlertDialog：@string/pref_desktop_show_notification_content（由 com.minfivezz.launcher.ul#onClick 处理按钮）",
    "设置项摘要文本：@string/pref_desktop_show_notification_summary（Show notification on transparent status bar clone）",
    "电池工具箱休眠页“Auto”按钮后的原生说明对话框：@string/start_service_details（含 3 步教学与 Manually 替代项）",
    "休眠帮助标题/按钮：@string/start_hibernate_help（Notice）、@string/manually、@string/auto、@string/hibernate_notice_get（Got it）",
    "设置项标题：@string/pref_more_enable_accessibility_title（Enable accessibility）",
    "assets/help.html、about.html、licenses.html、translations.html 为纯本地帮助/开源许可页，未承载无障碍引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To activate notification, please turn on Lollipop Launcher Accessibility Service on Accessibility Setting.",
      "text_zh": "要激活通知显示，请在无障碍设置中开启 Lollipop Launcher 无障碍服务。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（同时作为 android:description 显示在系统无障碍列表）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To activate notification, please turn on Lollipop Launcher Accessibility Service on Accessibility Setting. \nDo you want to open Accessibility Settings?",
      "text_zh": "要激活通知显示，请在无障碍设置中开启 Lollipop Launcher 无障碍服务。是否要打开无障碍设置？",
      "source_location": "res/values/strings.xml key=pref_desktop_show_notification_content",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To Auto-hibernate the selected apps, please turn on AFast Launcher Accessibility Service: \n\n 1. Click bellow \"Auto\", \n 2. Find the AFast Launcher in the list, click the item, \n 3. Enable the switch on Top-Right bar\n\n (If you click \"Manually\", please click \"Force stop\" manually to hibernate app)",
      "text_zh": "要自动休眠所选应用，请开启 AFast Launcher 无障碍服务：1. 点击下方“Auto”；2. 在列表中找到 AFast Launcher 并点击该项；3. 打开右上角开关。（若点击“Manually”，请手动点击“强制停止”来休眠应用）",
      "source_location": "res/values/strings.xml key=start_service_details",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Show notification on transparent status bar clone",
      "text_zh": "在透明状态栏克隆上显示通知",
      "source_location": "res/values/strings.xml key=pref_desktop_show_notification_summary",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The \"App info\" window will popup, please click \"Force stop\" to hibernate the app.",
      "text_zh": "将弹出“应用信息”窗口，请点击“强制停止”来休眠该应用。",
      "source_location": "res/values/strings.xml key=start_hibernate_details_bellow_android4_2",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无拒绝循环。跳转采用 startActivityForResult 后不重试；未发现 onResume/Timer 定时重跳或返回即弹回逻辑。用户取消对话框或从系统设置返回后仅保持功能未启用状态。",
    "overlay_or_fake_settings": "无。未发现半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 权限存在但未用于此引导链路。",
    "restricted_settings_13plus_coaching": "无。targetSdk 23（minSdk 14），无 Android 13+ 受限设置教学，也无 Session 安装器绕过；APPLICATION_DETAILS_SETTINGS 跳转仅用于“应用信息-强制停止”手动休眠路径（Launcher#a、HibernateActivity#h）。",
    "post_grant_anti_removal": "无。未发现获权后自点确认、自授权，或用 GLOBAL_ACTION_BACK/HOME 监听设置页阻止撤权；服务 canRetrieveWindowContent=false，未声明读取窗口内容能力。",
    "benign_graceful_degradation": "有。休眠功能提供“Manually”分支：不开启无障碍时跳转应用详情页由用户手动点“强制停止”完成同等效果；通知克隆功能不开启时仅不显示通知，桌面其余功能正常。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "纯 UTG 检测应在监测到应用发起 android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间拉起（或在其前一步抓取 LauncherSetting/HibernateActivity 上的说明对话框），二者可在同一次会话内顺序捕获。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前说明对话框页（桌面设置-显示通知）",
        "page_identifier": "LauncherSetting 上覆盖的原生 AlertDialog，正文含 \"Lollipop Launcher Accessibility Service\" 与 \"Do you want to open Accessibility Settings?\"，含确定/取消两按钮",
        "why_most_useful": "该页是判定“透明说明 vs 恐吓诱导”的关键：文案是否如实说明服务用途、是否提供取消，可直接区分良性引导与恶意逼权",
        "observable_utg_signals": ["对话框正文关键词 Lollipop Launcher Accessibility Service", "存在取消按钮（可跳过）", "无“更新/病毒/故障”等恐吓词"]
      },
      {
        "page_role": "跳转前分步教学对话框页（电池工具箱-自动休眠）",
        "page_identifier": "HibernateActivity 上的自定义 Dialog，含 \"1. Click bellow Auto\"、\"2. Find the AFast Launcher in the list\"、\"3. Enable the switch on Top-Right bar\"，并有 Auto/Manually 两按钮",
        "why_most_useful": "识别“分步教学式逼权”与替代路径：既有系统设置操作教学，也提供 Manually 手动降级，可据按钮结构判定是否给用户留退路",
        "observable_utg_signals": ["Auto 与 Manually 双按钮并存", "教学文案序号 1/2/3", "文案中出现的服务名 AFast Launcher 与实际 Lollipop Launcher 不一致"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中 \"Lollipop Launcher Accessibility Service\" 条目及其描述文字",
        "why_most_useful": "核对系统实际展示的服务名与描述是否与对话框宣称一致，检测是否有名称混淆或空白/换行挤出",
        "observable_utg_signals": ["条目名称与包名 com.minfivezz.launcher 对应关系", "描述文本是否与 accessibility_service_description 完全一致", "是否存在空名称或异常空白条目"]
      },
      {
        "page_role": "跳转后返回态页面",
        "page_identifier": "从系统设置返回后的 LauncherSetting / HibernateActivity 界面",
        "why_most_useful": "验证是否存在拒绝循环重跳、遮罩叠层或强制停留",
        "observable_utg_signals": ["返回后 2 秒内是否再次弹出对话框或重跳设置", "是否出现悬浮遮罩覆盖界面", "是否出现“必须开启”类不可取消提示"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本流程无纯图空文本诱导，文案均为可提取文本。潜在盲区：android:enabled 由 @bool/accesibility_service_enabled 资源控制，若该布尔在部分渠道包中被置 false，服务项可能在系统列表不可见，导致 UTG 抓取不到列表条目；另本轮未覆盖同一应用的通知栏工具、更新弹窗与 gameApps.db 相关外发行为，其恶意性需独立运行期验证。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.minfivezz.launcher.ul#onClick",
    "com.minfivezz.pusianwidget.toolbox.battery.q#onClick",
    "res/xml/notification_accessibility_service.xml",
    "res/values/strings.xml (accessibility_service_description / pref_desktop_show_notification_content / start_service_details)",
    "com.minfivezz.accessibility.NotificationAccessibilityService"
  ]
}
```

</details>
