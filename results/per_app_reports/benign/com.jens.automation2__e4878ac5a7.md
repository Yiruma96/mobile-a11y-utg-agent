# BN_046__e4878ac5a7｜系统效率与通用辅助 — Automation

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：124.0s

## 1. 一句话核心结论

- **核心申请方式**：该应用在冷启动或缺权限时进入自建权限说明 Activity，逐项原生弹窗教学，用户点击继续后经系统 AlertDialog 提示，再以 Intent(android.settings.ACCESSIBILITY_SETTINGS) 跳系统无障碍页手动开启，全程透明可取消且服务本体仅用于执行用户自定义规则动作。
- **静态可见性说明**：全部引导逻辑位于 classes.dex 的 ActivityPermissions 及其内部类、strings.xml 与 res/xml/config_accessibility_service.xml，均为明文可静态还原；无障碍服务本体为空实现，无加壳、无 AES 载荷、无远端 HTML、无 WebView。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e4878ac5a7308f886747214168abffa332f8ae5577bcd1ab9ea8d6a41e84df87` |
| 包名 / 年份 | `com.jens.automation2` / 2025-2026 |
| 家族 / 品类 | **系统效率与通用辅助**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.jens.automation2_149.apk |
| 桌面显示名 | Automation |
| 引导页宣称品牌/身份 | Automation（com.jens.automation2，开源规则自动化工具，未冒充系统或其他品牌） |
| 系统无障碍列表服务名 | Automation（service android:label=@string/app_name） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.jens.automation2.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `BIND_NOTIFICATION_LISTENER_SERVICE, CALL_PHONE, PROCESS_OUTGOING_CALLS, QUERY_ALL_PACKAGES, READ_CONTACTS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Required for certain actions. / Required for certain actions. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.jens.automation2.ActivityMainTabLayout（LAUNCHER，singleTask）承载 com.jens.automation2.ActivityMainScreen 标签页 | 用户点击桌面图标冷启动，ActivityMainScreen.onCreate 内判断 ActivityPermissions.needMorePermissions(this) 为真 | 原生Activity | **原文**：Automation requires more permissions to fully function. Click on this text to find out more and request them.<br>**译注**：Automation 需要更多权限才能完整运行。点击此文本了解详情并发起申请。 | 自动跳转到权限说明页（也可稍后点主界面提示文本再次进入），主界面仍可取消返回并停留在受限模式 | `com.jens.automation2.ActivityMainScreen.onCreate / ActivityMainTabLayout.onCreate / strings.xml mainScreenPermissionNote` |
| 2 | 引导说明页 | com.jens.automation2.ActivityPermissions（layout/permissions_activity） | ActivityMainScreen.onCreate 中 startActivityForResult(new Intent(this, ActivityPermissions.class), 7000) | 原生Activity | **原文**：The app is current running in limited mode and has deactivated some features. To fully function it requires permissions. If you want to use all functionality you have to grant the permissions in the following rights dialogues. If you do, not certain rules can not be executed. In the following you are given an explanation for the requested permissions. Click continue, when you are ready to proceed.<br>**译注**：应用当前处于受限模式并已停用部分功能。完整运行需要权限。若想使用全部功能，需要在随后的权限对话框中授予权限。下面会说明所申请权限的用途。准备好后点击继续。 | 点击“继续”（bRequestPermissions）发起申请，或点击“取消”（bCancelPermissions）直接 finish 退出，无强制跳过障碍 | `com.jens.automation2.ActivityPermissions.onCreate / fillExplanationText / ActivityPermissions$1.onClick / strings.xml permissionsExplanationGeneric` |
| 3 | 跳受限设置 | 按权限逐项跳转：android.settings.action.MANAGE_WRITE_SETTINGS、DeviceAdmin 授权、android.settings.NOTIFICATION_POLICY_ACCESS_SETTINGS、SYSTEM_ALERT_WINDOW 弹窗、android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS | 点击继续后 ActivityPermissions$2.onClick → requestPermissions(list,false) 遍历所需权限 | 原生Dialog | **原文**：After clicking OK you'll be sent to a system dialog. Please select Automation there and allow Display over other apps.<br>**译注**：点击确定后您将被送到系统对话框，请在其中选择 Automation 并允许“显示在其他应用上层”。 | 在系统设置页手动授予对应权限，可随时返回；未授予则后续步骤继续但功能受限 | `com.jens.automation2.ActivityPermissions.requestPermissions / strings.xml overlayPermissionHint` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表中的 Automation 项） | 命中 BIND_ACCESSIBILITY_SERVICE 时弹出 AlertDialog，用户点击确定触发 OnDismissListener(ActivityPermissions$4) → ActivityPermissions.requestBindAccessibilityService() | 系统无障碍页 | **原文**：After clicking OK you'll be sent to a system dialog. Please select Automation there and allow Allow accessibility API.<br>**译注**：点击确定后您将被送到系统对话框，请在其中选择 Automation 并允许“无障碍 API”。 | 点击弹窗“确定”，在系统无障碍页手动为 Automation 打开开关；系统无障碍列表中该项说明为 Required for certain actions.（仅用于某些动作） | `com.jens.automation2.ActivityPermissions.requestPermissions / ActivityPermissions$4.onDismiss / ActivityPermissions.requestBindAccessibilityService / res/xml/config_accessibility_service.xml` |
| 5 | 拒权反馈循环 | com.jens.automation2.ActivityPermissions.onActivityResult / onResume | 从系统无障碍页返回触发 onActivityResult(requestCodeForPermissionsAccessibility)，随后 onResume 校验 getRequiredPermissions() | 原生Activity | 无 | 用户可随时点“取消”退出；无定时器拉起、无返回死循环、无悬浮窗遮罩 | `com.jens.automation2.ActivityPermissions.onActivityResult / onResume` |
| 6 | 获权后动作 | com.jens.automation2.ActivityPermissions.setHaveAllPermissions → finish()；后续由 com.jens.automation2.MyAccessibilityService 与 AutomationService 提供能力 | onResume 检测所有所需权限齐备后调用 setHaveAllPermissions() | 原生Activity | 无 | 无额外操作；不自动点击确认、不监听设置页阻止撤权；MyAccessibilityService.onAccessibilityEvent 为空实现，能力仅在用户配置的规则动作中按需调用（如 Actions.takeScreenshot 的 performGlobalAction） | `com.jens.automation2.ActivityPermissions.setHaveAllPermissions / com.jens.automation2.MyAccessibilityService.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- ActivityMainScreen 主界面可点击提示 TextView（tvMainScreenNotePermissions，strings.xml mainScreenPermissionNote）
- ActivityPermissions 引导说明页（layout/permissions_activity）：正文 permissionsExplanationGeneric + fillExplanationText 逐条权限名称与原因（Html.fromHtml 渲染），下方 tvPermissionsExplanationSystemSettings 显示 systemSettingsNote1/2 系统设置说明
- ActivityPermissions 各权限前置系统 AlertDialog：overlayPermissionHint、accessibilityApiPermissionHint、notificationAccessAndroid13、alarmsPermissionHint、pleaseGiveBgLocation、writeSecureSettingsNotice（标题均为 strings.xml info）
- 系统无障碍列表服务项：android:label=@string/app_name（Automation），android:description=@string/accessibility_service_explanation（Required for certain actions.）
- AutomationService.checkStartupRequirements 缺权限时的 Toast（serviceWontStartPermissions / permissionForegroundServiceTypeSpecialUseRequired）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | After clicking OK you'll be sent to a system dialog. Please select Automation there and allow Allow accessibility API. | 点击确定后您将被送到系统对话框，请在其中选择 Automation 并允许“无障碍 API”。 | `res/values/strings.xml key=accessibilityApiPermissionHint` | 受限设置分步教学 |
| en | Required for certain actions. | 仅用于某些动作。 | `res/values/strings.xml key=accessibility_service_explanation（config_accessibility_service.xml android:description）` | 良性透明说明 |
| en | The app is current running in limited mode and has deactivated some features. To fully function it requires permissions. If you want to use all functionality you have to grant the permissions in the following rights dialogues. If you do, not certain rules can not be executed. In the following you are given an explanation for the requested permissions. Click continue, when you are ready to proceed. | 应用当前处于受限模式并已停用部分功能。完整运行需要权限。若想使用全部功能，需要在随后的权限对话框中授予权限。否则某些规则将无法执行。下面会说明所申请权限的用途。准备好后点击继续。 | `res/values/strings.xml key=permissionsExplanationGeneric` | 良性透明说明 |
| en | Automation requires more permissions to fully function. Click on this text to find out more and request them. | Automation 需要更多权限才能完整运行。点击此文本了解详情并发起申请。 | `res/values/strings.xml key=mainScreenPermissionNote` | 良性透明说明 |
| en | To enable the feature you just tried to use more permissions are required. Click continue to request them. | 要启用您刚才尝试使用的功能，需要更多权限。点击继续进行申请。 | `res/values/strings.xml key=permissionsExplanationSmall（ActivityPermissions.onCreate 带 specificPermissionsToRequest 时使用）` | 良性透明说明 |
| en | After clicking OK you'll be sent to a system dialog. Please select Automation there and allow Display over other apps. | 点击确定后您将被送到系统对话框，请在其中选择 Automation 并允许“显示在其他应用上层”。 | `res/values/strings.xml key=overlayPermissionHint` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性安全降级：从系统无障碍页返回后 onActivityResult 仅在 havePermission 为真时继续后续权限请求，onResume 未齐备则静默停留；无定时器重跳、无 onResume 死循环，用户可点 bCancelPermissions 直接 finish 并以受限模式使用主界面
- **遮罩叠层 / 高仿系统设置页**：无。未发现全屏悬浮窗遮罩、半透明引导层或高仿系统无障碍开关页；无障碍配置 canRetrieveWindowContent=false、flagDefault，服务无任何窗口内容读取或手势注入
- **Android 13+ 受限设置（Restricted Settings）应对**：无。ACTION_APPLICATION_DETAILS_SETTINGS 仅出现在 ActivityPermissions$7.onDismiss，用于 Android 10+ 后台定位补充授权，未教唆开启 Android 13+ 受限设置或使用 Session 安装器绕过
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅写日志，无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权（performGlobalAction 仅用于 Actions.takeScreenshot 截图能力）
- **良性降级 / 替代方案**：有。说明页明确声明“当前处于受限模式并已停用部分功能”，可取消；主界面常驻提示文本可随时再发起；AutomationService.checkStartupRequirements 缺权限时 Toast 提示并拒绝启动服务而非强制索权

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后监测到 Activity 切换为 com.jens.automation2.ActivityPermissions（尤其 onCreate 后 7000 请求码的 startActivityForResult），或监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 发出的瞬间；亦可在主界面点击 tvMainScreenNotePermissions 时拉起
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：无纯图片引导、无 WebView/远端 HTML、无一阶段 Dropper、未加壳。唯一需注意的时序特征是冷启动即跳权限说明页，若 UTG 仅在点击后开始采集可能错过该自动跳转，建议启动即抓取 Activity 栈。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页** | com.jens.automation2.ActivityPermissions + layout/permissions_activity，含 bCancelPermissions/bRequestPermissions 两个按钮与权限原因列表 | 该页是权限索取总入口，能直接区分“透明说明+可取消”与“不可取消强制引导” | 是否存在可点击的取消按钮（bCancelPermissions 文本）；正文是否为权限用途逐条说明（permissionsExplanationGeneric）；是否有跳过/稍后按钮 |
| **跳转前无障碍教学弹窗** | AlertDialog 标题 info，正文 accessibilityApiPermissionHint，确定按钮 | 该弹窗是进入系统无障碍页的唯一前导，文案是否如实说明去向与操作为核心判据 | 正文是否含 ACCESSIBILITY/无障碍 与 Automation 服务名；标题是否为中性的 info 而非恐吓性文案；按钮是否仅“确定”无取消 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务 → Automation（label=@string/app_name，summary=Required for certain actions.） | 核验服务名与说明是否与桌面显示名一致，是否存在空白挤出、同形字或伪造说明 | 服务项显示名是否等于 Automation；说明文本是否为 Required for certain actions.；是否存在多余同名服务项或别名项 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.jens.automation2.ActivityPermissions.requestBindAccessibilityService`
- `com.jens.automation2.ActivityPermissions.requestPermissions`
- `com.jens.automation2.ActivityPermissions$4.onDismiss`
- `com.jens.automation2.ActivityMainScreen.onCreate`
- `com.jens.automation2.MyAccessibilityService.onAccessibilityEvent`
- `res/xml/config_accessibility_service.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，共 13 次工具调用）

**可见性**：完全静态可见，没有加壳、没有密文载荷、没有远端 HTML；引导全部由原生 `Activity`、`Dialog` 和 `strings.xml` 承载。

**UTG 页面流转主线**（`com.jens.automation2`，显示名 Automation，良性开源自动化工具）：

1. **冷启动入口**：LAUNCHER 是 [ActivityMainTabLayout.onCreate()](<resource-unit:#1.dex1 code:com.jens.automation2.ActivityMainTabLayout#onCreate>)，其内容为 `ActivityMainScreen` 标签页。`ActivityMainScreen.onCreate` 中先判断 `ActivityPermissions.needMorePermissions(this)`；一旦缺少权限，就自动 `startActivityForResult(ActivityPermissions, 7000)`，也就是冷启动即弹出权限说明页。
2. **引导说明页**：`ActivityPermissions` 加载布局 `R$layout.permissions_activity`，正文来自 `R$string.permissionsExplanationGeneric`，并用 `fillExplanationText()` 通过 `Html.fromHtml` 逐条列出每个权限名称及其原因；页面底部有**明确的“取消”按钮** `bCancelPermissions`（`ActivityPermissions$1.onClick` → `finish()`），因此用户拒绝后不会陷入重跳循环。
3. **跳转受限设置**：点击“继续”（`ActivityPermissions$2.onClick`）后进入 `requestPermissions(list,false)`，按 `WRITE_SETTINGS → DEVICE_ADMIN → NOTIFICATION_POLICY → SYSTEM_ALERT_WINDOW → BIND_ACCESSIBILITY_SERVICE` 的顺序逐项处理。每项跳转前，都会先弹出原生 `AlertDialog` 教学说明。
4. **无障碍专项**：命中 `BIND_ACCESSIBILITY_SERVICE` 时，会弹出 `Miscellaneous.messageBox(info, R$string.accessibilityApiPermissionHint)`；其文案为“After clicking OK you'll be sent to a system dialog. Please select Automation there and allow Allow accessibility API.”。该弹窗的 `OnDismissListener`（[ActivityPermissions$4.onDismiss](<resource-unit:#1.dex1 code:com.jens.automation2.ActivityPermissions$4#onDismiss>)）会触发 [requestBindAccessibilityService()](<resource-unit:#1.dex1 code:com.jens.automation2.ActivityPermissions#requestBindAccessibilityService>)；该函数使用 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 和 `FLAG_ACTIVITY_NEW_TASK`，跳转到系统无障碍设置页。
5. **获权后动作**：`onActivityResult` 检测到 `havePermission("android.permission.BIND_ACCESSIBILITY_SERVICE")` 后，继续请求剩余权限；`onResume` 若所需权限全部齐备，则调用 `setHaveAllPermissions()` → `finish()`。整个过程没有自点确认、没有自授权，也没有用 `GLOBAL_ACTION_BACK` 或 `HOME` 阻止撤权。
6. **权限需求按规则动态计算**：`getRequiredPermissions()` 仅依据已配置的规则和配置档来收集权限（如 `ActivityManageRule$3.onClick` 场景），因此属于“按需申请”而非一次性索权；`AutomationService.checkStartupRequirements` 缺权限时也只 `Toast` 提示并返回 false（安全降级）。
7. **无障碍服务本体极简**：[MyAccessibilityService](<resource-unit:#1.dex1 code:com.jens.automation2.MyAccessibilityService#onAccessibilityEvent>) 的 `onAccessibilityEvent`、`onInterrupt` 为空实现，`onServiceConnected` 仅写日志；[config_accessibility_service.xml](<resource-unit:#1 file:res/xml/config_accessibility_service.xml>) 中 `canRetrieveWindowContent="false"`、`canRequestFilterKeyEvents="false"`、`flagDefault`。全包没有 `dispatchGesture` 和 `getRootInActiveWindow` 调用；`performGlobalAction` 仅在 `Actions.takeScreenshot` 中用于截图能力（该动作是用户显式配置的规则动作）。
8. **身份一致**：无障碍服务 `android:label="@string/app_name"`（Automation），`android:description="Required for certain actions."`；没有空白或换行挤占警告信息、没有同形字、没有多 `activity-alias`、没有伪造 `isAccessibilityTool`。未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 的“受限设置”教唆；唯一的 `APPLICATION_DETAILS_SETTINGS` 出现在 `ActivityPermissions$7.onDismiss`，只用于 Android 10+ 后台定位的补充授权，与无障碍无关。

**判定**：引导流程透明、可取消、有降级路径，符合良性应用特征，**未发现诱导、强制、伪装或拒权循环类风险**。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于 classes.dex 的 ActivityPermissions 及其内部类、strings.xml 与 res/xml/config_accessibility_service.xml，均为明文可静态还原；无障碍服务本体为空实现，无加壳、无 AES 载荷、无远端 HTML、无 WebView。",
  "summary_one_liner": "该应用在冷启动或缺权限时进入自建权限说明 Activity，逐项原生弹窗教学，用户点击继续后经系统 AlertDialog 提示，再以 Intent(android.settings.ACCESSIBILITY_SETTINGS) 跳系统无障碍页手动开启，全程透明可取消且服务本体仅用于执行用户自定义规则动作。",
  "disguise_identity": {
    "app_display_name": "Automation",
    "claimed_brand_or_persona": "Automation（com.jens.automation2，开源规则自动化工具，未冒充系统或其他品牌）",
    "a11y_service_label": "Automation（service android:label=@string/app_name）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.jens.automation2.ActivityMainTabLayout（LAUNCHER，singleTask）承载 com.jens.automation2.ActivityMainScreen 标签页",
      "trigger_event": "用户点击桌面图标冷启动，ActivityMainScreen.onCreate 内判断 ActivityPermissions.needMorePermissions(this) 为真",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Automation requires more permissions to fully function. Click on this text to find out more and request them.",
      "shown_text_zh": "Automation 需要更多权限才能完整运行。点击此文本了解详情并发起申请。",
      "user_action_requested": "自动跳转到权限说明页（也可稍后点主界面提示文本再次进入），主界面仍可取消返回并停留在受限模式",
      "code_anchor": "com.jens.automation2.ActivityMainScreen.onCreate / ActivityMainTabLayout.onCreate / strings.xml mainScreenPermissionNote"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.jens.automation2.ActivityPermissions（layout/permissions_activity）",
      "trigger_event": "ActivityMainScreen.onCreate 中 startActivityForResult(new Intent(this, ActivityPermissions.class), 7000)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "The app is current running in limited mode and has deactivated some features. To fully function it requires permissions. If you want to use all functionality you have to grant the permissions in the following rights dialogues. If you do, not certain rules can not be executed. In the following you are given an explanation for the requested permissions. Click continue, when you are ready to proceed.",
      "shown_text_zh": "应用当前处于受限模式并已停用部分功能。完整运行需要权限。若想使用全部功能，需要在随后的权限对话框中授予权限。下面会说明所申请权限的用途。准备好后点击继续。",
      "user_action_requested": "点击“继续”（bRequestPermissions）发起申请，或点击“取消”（bCancelPermissions）直接 finish 退出，无强制跳过障碍",
      "code_anchor": "com.jens.automation2.ActivityPermissions.onCreate / fillExplanationText / ActivityPermissions$1.onClick / strings.xml permissionsExplanationGeneric"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "按权限逐项跳转：android.settings.action.MANAGE_WRITE_SETTINGS、DeviceAdmin 授权、android.settings.NOTIFICATION_POLICY_ACCESS_SETTINGS、SYSTEM_ALERT_WINDOW 弹窗、android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS",
      "trigger_event": "点击继续后 ActivityPermissions$2.onClick → requestPermissions(list,false) 遍历所需权限",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "After clicking OK you'll be sent to a system dialog. Please select Automation there and allow Display over other apps.",
      "shown_text_zh": "点击确定后您将被送到系统对话框，请在其中选择 Automation 并允许“显示在其他应用上层”。",
      "user_action_requested": "在系统设置页手动授予对应权限，可随时返回；未授予则后续步骤继续但功能受限",
      "code_anchor": "com.jens.automation2.ActivityPermissions.requestPermissions / strings.xml overlayPermissionHint"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表中的 Automation 项）",
      "trigger_event": "命中 BIND_ACCESSIBILITY_SERVICE 时弹出 AlertDialog，用户点击确定触发 OnDismissListener(ActivityPermissions$4) → ActivityPermissions.requestBindAccessibilityService()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "After clicking OK you'll be sent to a system dialog. Please select Automation there and allow Allow accessibility API.",
      "shown_text_zh": "点击确定后您将被送到系统对话框，请在其中选择 Automation 并允许“无障碍 API”。",
      "user_action_requested": "点击弹窗“确定”，在系统无障碍页手动为 Automation 打开开关；系统无障碍列表中该项说明为 Required for certain actions.（仅用于某些动作）",
      "code_anchor": "com.jens.automation2.ActivityPermissions.requestPermissions / ActivityPermissions$4.onDismiss / ActivityPermissions.requestBindAccessibilityService / res/xml/config_accessibility_service.xml"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.jens.automation2.ActivityPermissions.onActivityResult / onResume",
      "trigger_event": "从系统无障碍页返回触发 onActivityResult(requestCodeForPermissionsAccessibility)，随后 onResume 校验 getRequiredPermissions()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（仅静默校验；未授予则停在权限说明页等待用户再次操作，不自动重跳）",
      "user_action_requested": "用户可随时点“取消”退出；无定时器拉起、无返回死循环、无悬浮窗遮罩",
      "code_anchor": "com.jens.automation2.ActivityPermissions.onActivityResult / onResume"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.jens.automation2.ActivityPermissions.setHaveAllPermissions → finish()；后续由 com.jens.automation2.MyAccessibilityService 与 AutomationService 提供能力",
      "trigger_event": "onResume 检测所有所需权限齐备后调用 setHaveAllPermissions()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（关闭权限页并取消通知 id 1001，回到主界面显示服务状态）",
      "user_action_requested": "无额外操作；不自动点击确认、不监听设置页阻止撤权；MyAccessibilityService.onAccessibilityEvent 为空实现，能力仅在用户配置的规则动作中按需调用（如 Actions.takeScreenshot 的 performGlobalAction）",
      "code_anchor": "com.jens.automation2.ActivityPermissions.setHaveAllPermissions / com.jens.automation2.MyAccessibilityService.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "ActivityMainScreen 主界面可点击提示 TextView（tvMainScreenNotePermissions，strings.xml mainScreenPermissionNote）",
    "ActivityPermissions 引导说明页（layout/permissions_activity）：正文 permissionsExplanationGeneric + fillExplanationText 逐条权限名称与原因（Html.fromHtml 渲染），下方 tvPermissionsExplanationSystemSettings 显示 systemSettingsNote1/2 系统设置说明",
    "ActivityPermissions 各权限前置系统 AlertDialog：overlayPermissionHint、accessibilityApiPermissionHint、notificationAccessAndroid13、alarmsPermissionHint、pleaseGiveBgLocation、writeSecureSettingsNotice（标题均为 strings.xml info）",
    "系统无障碍列表服务项：android:label=@string/app_name（Automation），android:description=@string/accessibility_service_explanation（Required for certain actions.）",
    "AutomationService.checkStartupRequirements 缺权限时的 Toast（serviceWontStartPermissions / permissionForegroundServiceTypeSpecialUseRequired）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "After clicking OK you'll be sent to a system dialog. Please select Automation there and allow Allow accessibility API.",
      "text_zh": "点击确定后您将被送到系统对话框，请在其中选择 Automation 并允许“无障碍 API”。",
      "source_location": "res/values/strings.xml key=accessibilityApiPermissionHint",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Required for certain actions.",
      "text_zh": "仅用于某些动作。",
      "source_location": "res/values/strings.xml key=accessibility_service_explanation（config_accessibility_service.xml android:description）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The app is current running in limited mode and has deactivated some features. To fully function it requires permissions. If you want to use all functionality you have to grant the permissions in the following rights dialogues. If you do, not certain rules can not be executed. In the following you are given an explanation for the requested permissions. Click continue, when you are ready to proceed.",
      "text_zh": "应用当前处于受限模式并已停用部分功能。完整运行需要权限。若想使用全部功能，需要在随后的权限对话框中授予权限。否则某些规则将无法执行。下面会说明所申请权限的用途。准备好后点击继续。",
      "source_location": "res/values/strings.xml key=permissionsExplanationGeneric",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Automation requires more permissions to fully function. Click on this text to find out more and request them.",
      "text_zh": "Automation 需要更多权限才能完整运行。点击此文本了解详情并发起申请。",
      "source_location": "res/values/strings.xml key=mainScreenPermissionNote",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To enable the feature you just tried to use more permissions are required. Click continue to request them.",
      "text_zh": "要启用您刚才尝试使用的功能，需要更多权限。点击继续进行申请。",
      "source_location": "res/values/strings.xml key=permissionsExplanationSmall（ActivityPermissions.onCreate 带 specificPermissionsToRequest 时使用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "After clicking OK you'll be sent to a system dialog. Please select Automation there and allow Display over other apps.",
      "text_zh": "点击确定后您将被送到系统对话框，请在其中选择 Automation 并允许“显示在其他应用上层”。",
      "source_location": "res/values/strings.xml key=overlayPermissionHint",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性安全降级：从系统无障碍页返回后 onActivityResult 仅在 havePermission 为真时继续后续权限请求，onResume 未齐备则静默停留；无定时器重跳、无 onResume 死循环，用户可点 bCancelPermissions 直接 finish 并以受限模式使用主界面",
    "overlay_or_fake_settings": "无。未发现全屏悬浮窗遮罩、半透明引导层或高仿系统无障碍开关页；无障碍配置 canRetrieveWindowContent=false、flagDefault，服务无任何窗口内容读取或手势注入",
    "restricted_settings_13plus_coaching": "无。ACTION_APPLICATION_DETAILS_SETTINGS 仅出现在 ActivityPermissions$7.onDismiss，用于 Android 10+ 后台定位补充授权，未教唆开启 Android 13+ 受限设置或使用 Session 安装器绕过",
    "post_grant_anti_removal": "无。onServiceConnected 仅写日志，无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权（performGlobalAction 仅用于 Actions.takeScreenshot 截图能力）",
    "benign_graceful_degradation": "有。说明页明确声明“当前处于受限模式并已停用部分功能”，可取消；主界面常驻提示文本可随时再发起；AutomationService.checkStartupRequirements 缺权限时 Toast 提示并拒绝启动服务而非强制索权"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后监测到 Activity 切换为 com.jens.automation2.ActivityPermissions（尤其 onCreate 后 7000 请求码的 startActivityForResult），或监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 发出的瞬间；亦可在主界面点击 tvMainScreenNotePermissions 时拉起",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页",
        "page_identifier": "com.jens.automation2.ActivityPermissions + layout/permissions_activity，含 bCancelPermissions/bRequestPermissions 两个按钮与权限原因列表",
        "why_most_useful": "该页是权限索取总入口，能直接区分“透明说明+可取消”与“不可取消强制引导”",
        "observable_utg_signals": ["是否存在可点击的取消按钮（bCancelPermissions 文本）", "正文是否为权限用途逐条说明（permissionsExplanationGeneric）", "是否有跳过/稍后按钮"]
      },
      {
        "page_role": "跳转前无障碍教学弹窗",
        "page_identifier": "AlertDialog 标题 info，正文 accessibilityApiPermissionHint，确定按钮",
        "why_most_useful": "该弹窗是进入系统无障碍页的唯一前导，文案是否如实说明去向与操作为核心判据",
        "observable_utg_signals": ["正文是否含 ACCESSIBILITY/无障碍 与 Automation 服务名", "标题是否为中性的 info 而非恐吓性文案", "按钮是否仅“确定”无取消"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务 → Automation（label=@string/app_name，summary=Required for certain actions.）",
        "why_most_useful": "核验服务名与说明是否与桌面显示名一致，是否存在空白挤出、同形字或伪造说明",
        "observable_utg_signals": ["服务项显示名是否等于 Automation", "说明文本是否为 Required for certain actions.", "是否存在多余同名服务项或别名项"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：无纯图片引导、无 WebView/远端 HTML、无一阶段 Dropper、未加壳。唯一需注意的时序特征是冷启动即跳权限说明页，若 UTG 仅在点击后开始采集可能错过该自动跳转，建议启动即抓取 Activity 栈。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.jens.automation2.ActivityPermissions.requestBindAccessibilityService",
    "com.jens.automation2.ActivityPermissions.requestPermissions",
    "com.jens.automation2.ActivityPermissions$4.onDismiss",
    "com.jens.automation2.ActivityMainScreen.onCreate",
    "com.jens.automation2.MyAccessibilityService.onAccessibilityEvent",
    "res/xml/config_accessibility_service.xml"
  ]
}
```

</details>
