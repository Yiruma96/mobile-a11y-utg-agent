# BN_065__71c752dab6｜远程协助与跨设备互联 — droidVNC-NG

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：108.0s

## 1. 一句话核心结论

- **核心申请方式**：用户点击启动 VNC 服务后，应用以不可取消但可拒绝的原生弹窗说明无障碍用途，确认后带 fragment_args_key 跳转系统无障碍设置页预高亮自身服务，拒绝即安全降级，属良性透明申请。
- **静态可见性说明**：无障碍申请全链路（触发点、原生 Dialog、跳系统设置 Intent、结果回传）均在 classes.dex 与 res/values/strings.xml、res/xml/input_service_config.xml 中完整静态可见，无加壳、无密文载荷、无远端下发文案；assets/novnc 的 HTML 属 VNC 查看器前端，与无障碍引导无关。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `71c752dab6c948c0e1ea06916f2ffd484bbc7c57a48af0ee05a718aca3adab8b` |
| 包名 / 年份 | `net.christianbeier.droidvnc_ng` / 2025-2026 |
| 家族 / 品类 | **远程协助与跨设备互联**（同池样本数：1） |
| 原始来源标识 | https://github.com/bk138/droidVNC-NG/releases/download/v2.22.3/droidvnc-ng-2.22.3.apk |
| 桌面显示名 | droidVNC-NG |
| 引导页宣称品牌/身份 | droidVNC-NG（真实开源项目身份，标签与描述一致） |
| 系统无障碍列表服务名 | droidVNC-NG |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅有一个 activity-alias（net.christianbeier.droidvnc_ng.MainActivity → net.christianbeier.droidvnc_ng.ui.MainActivity）用于 LAUNCHER 入口，label 与主应用相同，非伪装；未发现空白挤出、同形字、伪造 isAccessibilityTool 等手法。 |
| 无障碍服务类名 | `net.christianbeier.droidvnc_ng.InputService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | This allows droidVNC-NG to post input events to the Android operating system, thus allowing remote control from a connected VNC viewer. All entered input is directly posted to Android, no input is logged, saved or shared. / This allows droidVNC-NG to post input events to the Android operating system, thus allowing remote control from a connected VNC viewer. All entered input is directly posted to Android, no input is logged, saved or shared. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | net.christianbeier.droidvnc_ng.ui.MainActivity（经 activity-alias net.christianbeier.droidvnc_ng.MainActivity 启动） | onCreate / onResume → updatePermissionsDisplay() | 原生Activity | **原文**：droidVNC-NG Admin Panel / Accessibility disabled / Permissions Dashboard<br>**译注**：droidVNC-NG 管理面板；权限面板显示“无障碍：未启用”状态，不主动弹窗。 | 仅展示状态，不强制任何操作；用户可自行点击各权限项或启动按钮 | `net.christianbeier.droidvnc_ng.ui.MainActivity.onCreate / updatePermissionsDisplay` |
| 2 | 业务功能触发 | MainActivity 启动/停止按钮 → net.christianbeier.droidvnc_ng.MainService（ACTION_START） | mButtonToggle.setOnClickListener → startForegroundService(ACTION_START) | 原生Activity | 无 | 点击服务开关 | `net.christianbeier.droidvnc_ng.ui.MainActivity$$ExternalSyntheticLambda3.onClick(case 0)` |
| 3 | 引导说明页 | net.christianbeier.droidvnc_ng.MainService.onStartCommand → InputRequestActivity.requestIfNeededAndPostResult() | onStartCommand 中 ACTION_START 分支，在 !InputService.isConnected() 时 startActivity(InputRequestActivity) | 原生Activity | 无 | 无（自动进入下一步弹窗） | `net.christianbeier.droidvnc_ng.MainService.onStartCommand → net.christianbeier.droidvnc_ng.input.InputRequestActivity.requestIfNeededAndPostResult` |
| 4 | 引导说明页 | InputRequestActivity 原生 AlertDialog | onCreate → new AlertDialog.Builder(this).setCancelable(false).show() | 原生Dialog | **原文**：Accessibility disabled / To be able to remotely control your device, you need to enable accessibility for droidVNC-NG. Do you want to enable accessibility now?<br>**译注**：标题“无障碍未启用”，正文说明“要远程控制您的设备，需要为 droidVNC-NG 启用无障碍，是否现在启用？”（若开启开机自启则追加相应说明） | 选择“Yes”（前往系统无障碍设置）或“No”（放弃并继续无输入能力运行）；不可点外部/返回取消，但存在明确否定按钮 | `net.christianbeier.droidvnc_ng.input.InputRequestActivity.onCreate；strings: input_a11y_title / input_a11y_msg_input / input_a11y_msg_boot / input_a11y_msg_input_and_boot` |
| 5 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（带 :settings:fragment_args_key 预定位 net.christianbeier.droidvnc_ng.InputService） | Dialog 正向按钮 onClick(case 0) → startActivityForResult(intent, 43) | 系统无障碍页 | 无 | 在系统页手动打开 droidVNC-NG 无障碍服务开关（或返回放弃） | `net.christianbeier.droidvnc_ng.input.InputRequestActivity$$ExternalSyntheticLambda0.onClick(case 0)` |
| 6 | 跳受限设置 | 系统设置 android.settings.SETTINGS（回退路径） | ACCESSIBILITY_SETTINGS 无解析结果或解析到 Stub 时，弹出提示后 onClick(case 2) | 系统无障碍页 | **原文**：Could not find the default accessibility settings activity. Please enable droidVNC-NG in system accessibility settings manually.<br>**译注**：“未找到默认无障碍设置页面，请在系统无障碍设置中手动启用 droidVNC-NG。”随后打开系统设置主页。 | 按提示手动进入系统无障碍设置开启（或直接放弃） | `net.christianbeier.droidvnc_ng.input.InputRequestActivity$$ExternalSyntheticLambda0.onClick(case 2)；strings: input_a11y_act_not_found_msg` |
| 7 | 拒权反馈循环 | InputRequestActivity.onActivityResult(43) → MainService.action_handle_a11y_result | 从系统设置返回后 onActivityResult，或点击“No”时 postResult(false) | 原生Dialog | 无 | 无；可正常返回主面板，服务器以无输入能力（含仅观看）方式运行或停止 | `net.christianbeier.droidvnc_ng.input.InputRequestActivity.onActivityResult / postResult；MainActivity.onResume / onWindowFocusChanged` |
| 8 | 获权后动作 | net.christianbeier.droidvnc_ng.InputService.onServiceConnected（无障碍服务本体） | 系统绑定服务后回调 onServiceConnected | 不可静态还原 | 无 | 无 | `net.christianbeier.droidvnc_ng.InputService.onServiceConnected / onKeyEvent / performShortcut` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 权限面板状态文本（“Accessibility disabled”/已启用）——updatePermissionsDisplay() 设置的 TextView 状态标签，非弹窗
- InputRequestActivity 原生 AlertDialog（setCancelable(false)）：标题 input_a11y_title + 正文 input_a11y_msg_input / input_a11y_msg_boot / input_a11y_msg_input_and_boot + Yes/No 按钮
- 系统无障碍服务列表条目：android:label=@string/app_name（droidVNC-NG），android:description=@string/input_a11y_service_description（来自 res/xml/input_service_config.xml）
- 跳转失败提示 AlertDialog：input_a11y_act_not_found_msg + OK
- res/values/strings.xml 本地化文案（仅英文默认值；未见多语言引导变体）
- 通知权限同类提示 notification_title / notification_msg（同类权限引导，非无障碍）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility disabled | 无障碍未启用 | `res/values/strings.xml key=input_a11y_title` | 良性透明说明 |
| en | To be able to remotely control your device, you need to enable accessibility for droidVNC-NG. Do you want to enable accessibility now? | 要远程控制您的设备，需要为 droidVNC-NG 启用无障碍功能。是否现在启用无障碍？ | `res/values/strings.xml key=input_a11y_msg_input` | 良性透明说明 |
| en | To enable start on boot for droidVNC-NG, you need to enable accessibility for it. Do you want to enable accessibility now? | 要启用 droidVNC-NG 的开机自启，需要为其开启无障碍。是否现在启用无障碍？ | `res/values/strings.xml key=input_a11y_msg_boot` | 良性透明说明 |
| en | To be able to remotely control your device and to enable start on boot for droidVNC-NG, you need to enable accessibility for it. Do you want to enable accessibility now? | 要远程控制您的设备并启用 droidVNC-NG 开机自启，需要为其开启无障碍。是否现在启用无障碍？ | `res/values/strings.xml key=input_a11y_msg_input_and_boot` | 良性透明说明 |
| en | This allows droidVNC-NG to post input events to the Android operating system, thus allowing remote control from a connected VNC viewer. All entered input is directly posted to Android, no input is logged, saved or shared. | 此功能允许 droidVNC-NG 向 Android 系统注入输入事件，从而允许已连接的 VNC 查看器远程控制本机。所有输入均直接发送到 Android，不会被记录、保存或共享。 | `res/values/strings.xml key=input_a11y_service_description（经 res/xml/input_service_config.xml android:description 呈现于系统无障碍列表）` | 隐私承诺 |
| en | Could not find the default accessibility settings activity. Please enable droidVNC-NG in system accessibility settings manually. | 未找到默认的无障碍设置页面，请在系统无障碍设置中手动启用 droidVNC-NG。 | `res/values/strings.xml key=input_a11y_act_not_found_msg` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。点击“No”仅 postResult(false) 并 finish()；从系统设置返回后 onActivityResult(43) 依 InputService.isConnected() 上报结果并结束，MainActivity 仅刷新状态文本，不会在 onResume/onWindowFocusChanged 中再次拉起弹窗。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW 悬浮窗、无半透明引导遮罩、无高仿系统无障碍开关页；跳转的是真实系统设置 Activity（带 fragment_args_key 预高亮，属 AOSP 标准用法）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现 APPLICATION_DETAILS_SETTINGS 中“允许受限设置”的分步教学，也未使用 Session 安装器绕过；APPLICATION_DETAILS_SETTINGS 仅在通知权限项点击时用于打开本应用详情页。
- **获权后即时行为与防撤权机制**：无。获权后 onServiceConnected 仅初始化输入上下文、放大监听与快捷键表；performGlobalAction 用于执行 VNC 客户端下发的 HOME/BACK/RECENTS 快捷键，未用于监听设置页阻止撤权，也无自点确认或自授权行为。
- **良性降级 / 替代方案**：有。拒绝后服务器仍可启动：输入能力按 settings_view_only 降级为仅观看，开机自启在 Android 11+ 无 InputService 时直接放弃（OnBootReceiver 记录并 return），跳转失败时引导用户手动开启。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 InputRequestActivity（透明主题 Activity，包名 net.christianbeier.droidvnc_ng）被拉起并显示 AlertDialog 的瞬间开始采集，并在其 onClick 触发 startActivityForResult 跳 android.settings.ACCESSIBILITY_SETTINGS 时进入系统页采集；该跳转仅在用户点击启动服务按钮后发生，冷启动不会出现。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：文案为 strings.xml 纯文本、原生 Dialog 可被 UTG 直接提取。仅需注意弹窗可能因 input_requested/start_on_boot_requested 组合呈现三种不同正文，采集时应覆盖“远程输入”“开机自启”“两者同时”三种分支。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **按需触发的无障碍申请弹窗页** | InputRequestActivity 上的 AlertDialog：标题“Accessibility disabled”，正文含“you need to enable accessibility for droidVNC-NG”，按钮 Yes/No | 该页是唯一的无障碍申请入口，可直接判定是否存在恐吓、伪装身份、无可取消与话术误导 | 标题/正文完整文本（可与 input_a11y_msg_* 比对）；按钮集合是否含否定项（No）；弹窗是否可被返回键/外部点击取消；所属 Activity 类名与是否透明主题 |
| **系统无障碍服务列表项** | 设置页中 droidVNC-NG 条目及其描述文本，开关初始为关闭 | 核对服务标签与描述是否与桌面身份一致，是否存在空白/同形字挤出或伪造系统警告 | 服务条目标签文本；description 全文；跳转后是否自动预高亮该条目；是否存在叠加遮罩窗口（可通过窗口层级与 overlay 权限判断） |
| **拒权后返回主面板页** | MainActivity 权限面板，无障碍项显示未启用状态 | 验证拒绝后是否安全降级而非反复重跳或强制阻断 | 无障碍状态文本与颜色；返回后是否再次出现 InputRequestActivity；主界面是否仍可操作（启动/停止按钮可用性） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `net.christianbeier.droidvnc_ng.MainService.onStartCommand`
- `net.christianbeier.droidvnc_ng.input.InputRequestActivity.requestIfNeededAndPostResult`
- `net.christianbeier.droidvnc_ng.input.InputRequestActivity.onCreate`
- `net.christianbeier.droidvnc_ng.input.InputRequestActivity$$ExternalSyntheticLambda0.onClick`
- `res/values/strings.xml（input_a11y_title / input_a11y_msg_input / input_a11y_msg_boot / input_a11y_msg_input_and_boot / input_a11y_service_description）`
- `res/xml/input_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

- **引导方式是“用户点击功能后按需触发”，不会在冷启动时立即弹出**：`MainActivity.onCreate` 只创建权限面板，并显示 `Accessibility disabled` 状态；只有在点击启动服务按钮（`mButtonToggle`）并触发 `MainService` 的 `ACTION_START` 后，才会进入申请无障碍权限的流程。
- **申请入口链路清晰，可完整静态还原**：[MainService.onStartCommand()](<resource-unit:#1.dex1 code:net.christianbeier.droidvnc_ng.MainService#onStartCommand>) 调用 [InputRequestActivity.requestIfNeededAndPostResult()](<resource-unit:#1.dex1 code:net.christianbeier.droidvnc_ng.input.InputRequestActivity#requestIfNeededAndPostResult>)；如果 `InputService.isConnected()` 为假，就启动透明主题的 `InputRequestActivity`。
- **提示弹窗为原生 `AlertDialog`，不可取消，但提供“No”退出路径**：[onCreate()](<resource-unit:#1.dex1 code:net.christianbeier.droidvnc_ng.input.InputRequestActivity#onCreate>) 使用 `setCancelable(false)`，标题为 `Accessibility disabled`，正文按“远程输入”或“开机自启”的组合选择 `input_a11y_msg_input`、`input_a11y_msg_boot` 或 `input_a11y_msg_input_and_boot`。
- **确认后直接跳系统无障碍页，并预高亮自身服务项**：[onClick()](<resource-unit:#1.dex1 code:net.christianbeier.droidvnc_ng.input.InputRequestActivity$$ExternalSyntheticLambda0#onClick>) 构造 `android.settings.ACCESSIBILITY_SETTINGS`，并把 `:settings:fragment_args_key` 设为 `包名/net.christianbeier.droidvnc_ng.InputService`，再以 `startActivityForResult(..., 43)` 跳转；如果解析失败，则退化为 `android.settings.SETTINGS`，并提示用户手动开启。
- **不存在拒绝循环或遮罩**：点“No”时只调用 `postResult(false)` 并 `finish()`；`onActivityResult(43)` 根据 `InputService.isConnected()` 上报结果后即结束，不会在 `onResume` 中重复跳转，也没有悬浮窗叠层或伪造系统开关页。
- **身份与文案一致，没有伪装**：桌面名与无障碍服务标签都是 `droidVNC-NG`（`android:label="@string/app_name"`），描述明确说明仅注入输入事件、不记录或共享输入；`performGlobalAction` 仅出现在远程快捷键映射（`InputService.performShortcut`）中，用于下发 BACK/HOME/RECENTS，不是撤权防护。
- **权限能力超出“仅输入注入”**：[input_service_config.xml](<resource-unit:#1 file:res/xml/input_service_config.xml>) 声明了 `canRetrieveWindowContent="true"` 与 `canControlMagnification="true"`，属于远程协助实现所需，但描述文本没有逐项披露，可作为范围差异记录（不构成诱导）。
- **判定：良性透明申请**。不存在假冒身份、恐吓话术、教唆受限设置绕过，或获权后阻止用户撤权等行为；`activity-alias` 仅用于 LAUNCHER 入口，标签相同，非多别名伪装。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请全链路（触发点、原生 Dialog、跳系统设置 Intent、结果回传）均在 classes.dex 与 res/values/strings.xml、res/xml/input_service_config.xml 中完整静态可见，无加壳、无密文载荷、无远端下发文案；assets/novnc 的 HTML 属 VNC 查看器前端，与无障碍引导无关。",
  "summary_one_liner": "用户点击启动 VNC 服务后，应用以不可取消但可拒绝的原生弹窗说明无障碍用途，确认后带 fragment_args_key 跳转系统无障碍设置页预高亮自身服务，拒绝即安全降级，属良性透明申请。",
  "disguise_identity": {
    "app_display_name": "droidVNC-NG",
    "claimed_brand_or_persona": "droidVNC-NG（真实开源项目身份，标签与描述一致）",
    "a11y_service_label": "droidVNC-NG",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅有一个 activity-alias（net.christianbeier.droidvnc_ng.MainActivity → net.christianbeier.droidvnc_ng.ui.MainActivity）用于 LAUNCHER 入口，label 与主应用相同，非伪装；未发现空白挤出、同形字、伪造 isAccessibilityTool 等手法。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "net.christianbeier.droidvnc_ng.ui.MainActivity（经 activity-alias net.christianbeier.droidvnc_ng.MainActivity 启动）",
      "trigger_event": "onCreate / onResume → updatePermissionsDisplay()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "droidVNC-NG Admin Panel / Accessibility disabled / Permissions Dashboard",
      "shown_text_zh": "droidVNC-NG 管理面板；权限面板显示“无障碍：未启用”状态，不主动弹窗。",
      "user_action_requested": "仅展示状态，不强制任何操作；用户可自行点击各权限项或启动按钮",
      "code_anchor": "net.christianbeier.droidvnc_ng.ui.MainActivity.onCreate / updatePermissionsDisplay"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity 启动/停止按钮 → net.christianbeier.droidvnc_ng.MainService（ACTION_START）",
      "trigger_event": "mButtonToggle.setOnClickListener → startForegroundService(ACTION_START)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户点击启动 VNC 服务，服务侧判断是否已具备无障碍输入能力。",
      "user_action_requested": "点击服务开关",
      "code_anchor": "net.christianbeier.droidvnc_ng.ui.MainActivity$$ExternalSyntheticLambda3.onClick(case 0)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "net.christianbeier.droidvnc_ng.MainService.onStartCommand → InputRequestActivity.requestIfNeededAndPostResult()",
      "trigger_event": "onStartCommand 中 ACTION_START 分支，在 !InputService.isConnected() 时 startActivity(InputRequestActivity)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务侧发现无障碍服务未连接，转入引导 Activity（透明主题，排除最近任务）。",
      "user_action_requested": "无（自动进入下一步弹窗）",
      "code_anchor": "net.christianbeier.droidvnc_ng.MainService.onStartCommand → net.christianbeier.droidvnc_ng.input.InputRequestActivity.requestIfNeededAndPostResult"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "InputRequestActivity 原生 AlertDialog",
      "trigger_event": "onCreate → new AlertDialog.Builder(this).setCancelable(false).show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Accessibility disabled / To be able to remotely control your device, you need to enable accessibility for droidVNC-NG. Do you want to enable accessibility now?",
      "shown_text_zh": "标题“无障碍未启用”，正文说明“要远程控制您的设备，需要为 droidVNC-NG 启用无障碍，是否现在启用？”（若开启开机自启则追加相应说明）",
      "user_action_requested": "选择“Yes”（前往系统无障碍设置）或“No”（放弃并继续无输入能力运行）；不可点外部/返回取消，但存在明确否定按钮",
      "code_anchor": "net.christianbeier.droidvnc_ng.input.InputRequestActivity.onCreate；strings: input_a11y_title / input_a11y_msg_input / input_a11y_msg_boot / input_a11y_msg_input_and_boot"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（带 :settings:fragment_args_key 预定位 net.christianbeier.droidvnc_ng.InputService）",
      "trigger_event": "Dialog 正向按钮 onClick(case 0) → startActivityForResult(intent, 43)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接跳转系统无障碍服务列表，并预高亮 droidVNC-NG 服务条目，由用户在系统页面自行确认开启。",
      "user_action_requested": "在系统页手动打开 droidVNC-NG 无障碍服务开关（或返回放弃）",
      "code_anchor": "net.christianbeier.droidvnc_ng.input.InputRequestActivity$$ExternalSyntheticLambda0.onClick(case 0)"
    },
    {
      "step": 6,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置 android.settings.SETTINGS（回退路径）",
      "trigger_event": "ACCESSIBILITY_SETTINGS 无解析结果或解析到 Stub 时，弹出提示后 onClick(case 2)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Could not find the default accessibility settings activity. Please enable droidVNC-NG in system accessibility settings manually.",
      "shown_text_zh": "“未找到默认无障碍设置页面，请在系统无障碍设置中手动启用 droidVNC-NG。”随后打开系统设置主页。",
      "user_action_requested": "按提示手动进入系统无障碍设置开启（或直接放弃）",
      "code_anchor": "net.christianbeier.droidvnc_ng.input.InputRequestActivity$$ExternalSyntheticLambda0.onClick(case 2)；strings: input_a11y_act_not_found_msg"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "InputRequestActivity.onActivityResult(43) → MainService.action_handle_a11y_result",
      "trigger_event": "从系统设置返回后 onActivityResult，或点击“No”时 postResult(false)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅上报“a11y enabled/disabled”结果给 MainService 并 finish()，主界面刷新状态；不重新拉起弹窗、不循环跳设置。",
      "user_action_requested": "无；可正常返回主面板，服务器以无输入能力（含仅观看）方式运行或停止",
      "code_anchor": "net.christianbeier.droidvnc_ng.input.InputRequestActivity.onActivityResult / postResult；MainActivity.onResume / onWindowFocusChanged"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "net.christianbeier.droidvnc_ng.InputService.onServiceConnected（无障碍服务本体）",
      "trigger_event": "系统绑定服务后回调 onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务注册放大监听、重建输入上下文与快捷键表，供 VNC 客户端下发键鼠/手势事件；不上报弹窗、不尝试自动撤权保护。",
      "user_action_requested": "无",
      "code_anchor": "net.christianbeier.droidvnc_ng.InputService.onServiceConnected / onKeyEvent / performShortcut"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 权限面板状态文本（“Accessibility disabled”/已启用）——updatePermissionsDisplay() 设置的 TextView 状态标签，非弹窗",
    "InputRequestActivity 原生 AlertDialog（setCancelable(false)）：标题 input_a11y_title + 正文 input_a11y_msg_input / input_a11y_msg_boot / input_a11y_msg_input_and_boot + Yes/No 按钮",
    "系统无障碍服务列表条目：android:label=@string/app_name（droidVNC-NG），android:description=@string/input_a11y_service_description（来自 res/xml/input_service_config.xml）",
    "跳转失败提示 AlertDialog：input_a11y_act_not_found_msg + OK",
    "res/values/strings.xml 本地化文案（仅英文默认值；未见多语言引导变体）",
    "通知权限同类提示 notification_title / notification_msg（同类权限引导，非无障碍）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility disabled",
      "text_zh": "无障碍未启用",
      "source_location": "res/values/strings.xml key=input_a11y_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To be able to remotely control your device, you need to enable accessibility for droidVNC-NG. Do you want to enable accessibility now?",
      "text_zh": "要远程控制您的设备，需要为 droidVNC-NG 启用无障碍功能。是否现在启用无障碍？",
      "source_location": "res/values/strings.xml key=input_a11y_msg_input",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To enable start on boot for droidVNC-NG, you need to enable accessibility for it. Do you want to enable accessibility now?",
      "text_zh": "要启用 droidVNC-NG 的开机自启，需要为其开启无障碍。是否现在启用无障碍？",
      "source_location": "res/values/strings.xml key=input_a11y_msg_boot",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To be able to remotely control your device and to enable start on boot for droidVNC-NG, you need to enable accessibility for it. Do you want to enable accessibility now?",
      "text_zh": "要远程控制您的设备并启用 droidVNC-NG 开机自启，需要为其开启无障碍。是否现在启用无障碍？",
      "source_location": "res/values/strings.xml key=input_a11y_msg_input_and_boot",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This allows droidVNC-NG to post input events to the Android operating system, thus allowing remote control from a connected VNC viewer. All entered input is directly posted to Android, no input is logged, saved or shared.",
      "text_zh": "此功能允许 droidVNC-NG 向 Android 系统注入输入事件，从而允许已连接的 VNC 查看器远程控制本机。所有输入均直接发送到 Android，不会被记录、保存或共享。",
      "source_location": "res/values/strings.xml key=input_a11y_service_description（经 res/xml/input_service_config.xml android:description 呈现于系统无障碍列表）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Could not find the default accessibility settings activity. Please enable droidVNC-NG in system accessibility settings manually.",
      "text_zh": "未找到默认的无障碍设置页面，请在系统无障碍设置中手动启用 droidVNC-NG。",
      "source_location": "res/values/strings.xml key=input_a11y_act_not_found_msg",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。点击“No”仅 postResult(false) 并 finish()；从系统设置返回后 onActivityResult(43) 依 InputService.isConnected() 上报结果并结束，MainActivity 仅刷新状态文本，不会在 onResume/onWindowFocusChanged 中再次拉起弹窗。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW 悬浮窗、无半透明引导遮罩、无高仿系统无障碍开关页；跳转的是真实系统设置 Activity（带 fragment_args_key 预高亮，属 AOSP 标准用法）。",
    "restricted_settings_13plus_coaching": "无。未出现 APPLICATION_DETAILS_SETTINGS 中“允许受限设置”的分步教学，也未使用 Session 安装器绕过；APPLICATION_DETAILS_SETTINGS 仅在通知权限项点击时用于打开本应用详情页。",
    "post_grant_anti_removal": "无。获权后 onServiceConnected 仅初始化输入上下文、放大监听与快捷键表；performGlobalAction 用于执行 VNC 客户端下发的 HOME/BACK/RECENTS 快捷键，未用于监听设置页阻止撤权，也无自点确认或自授权行为。",
    "benign_graceful_degradation": "有。拒绝后服务器仍可启动：输入能力按 settings_view_only 降级为仅观看，开机自启在 Android 11+ 无 InputService 时直接放弃（OnBootReceiver 记录并 return），跳转失败时引导用户手动开启。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 InputRequestActivity（透明主题 Activity，包名 net.christianbeier.droidvnc_ng）被拉起并显示 AlertDialog 的瞬间开始采集，并在其 onClick 触发 startActivityForResult 跳 android.settings.ACCESSIBILITY_SETTINGS 时进入系统页采集；该跳转仅在用户点击启动服务按钮后发生，冷启动不会出现。",
    "key_pages_to_capture": [
      {
        "page_role": "按需触发的无障碍申请弹窗页",
        "page_identifier": "InputRequestActivity 上的 AlertDialog：标题“Accessibility disabled”，正文含“you need to enable accessibility for droidVNC-NG”，按钮 Yes/No",
        "why_most_useful": "该页是唯一的无障碍申请入口，可直接判定是否存在恐吓、伪装身份、无可取消与话术误导",
        "observable_utg_signals": ["标题/正文完整文本（可与 input_a11y_msg_* 比对）", "按钮集合是否含否定项（No）", "弹窗是否可被返回键/外部点击取消", "所属 Activity 类名与是否透明主题"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置页中 droidVNC-NG 条目及其描述文本，开关初始为关闭",
        "why_most_useful": "核对服务标签与描述是否与桌面身份一致，是否存在空白/同形字挤出或伪造系统警告",
        "observable_utg_signals": ["服务条目标签文本", "description 全文", "跳转后是否自动预高亮该条目", "是否存在叠加遮罩窗口（可通过窗口层级与 overlay 权限判断）"]
      },
      {
        "page_role": "拒权后返回主面板页",
        "page_identifier": "MainActivity 权限面板，无障碍项显示未启用状态",
        "why_most_useful": "验证拒绝后是否安全降级而非反复重跳或强制阻断",
        "observable_utg_signals": ["无障碍状态文本与颜色", "返回后是否再次出现 InputRequestActivity", "主界面是否仍可操作（启动/停止按钮可用性）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：文案为 strings.xml 纯文本、原生 Dialog 可被 UTG 直接提取。仅需注意弹窗可能因 input_requested/start_on_boot_requested 组合呈现三种不同正文，采集时应覆盖“远程输入”“开机自启”“两者同时”三种分支。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "net.christianbeier.droidvnc_ng.MainService.onStartCommand",
    "net.christianbeier.droidvnc_ng.input.InputRequestActivity.requestIfNeededAndPostResult",
    "net.christianbeier.droidvnc_ng.input.InputRequestActivity.onCreate",
    "net.christianbeier.droidvnc_ng.input.InputRequestActivity$$ExternalSyntheticLambda0.onClick",
    "res/values/strings.xml（input_a11y_title / input_a11y_msg_input / input_a11y_msg_boot / input_a11y_msg_input_and_boot / input_a11y_service_description）",
    "res/xml/input_service_config.xml"
  ]
}
```

</details>
