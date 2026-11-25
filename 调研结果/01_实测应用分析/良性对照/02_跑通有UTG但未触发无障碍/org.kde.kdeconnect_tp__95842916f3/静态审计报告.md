# BN_051__95842916f3｜系统效率与通用辅助 — KDE Connect

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：109.8s

## 1. 一句话核心结论

- **核心申请方式**：KDE Connect 仅在用户启用远程鼠标/远程键盘插件且检测到无障碍未授权时，弹出一个可取消的原生说明弹窗，点击『打开无障碍设置』直达系统无障碍页，返回后重载插件读取真实授权状态，无循环重跳、无遮罩、无伪装。
- **静态可见性说明**：无障碍引导链完整静态可见：服务实现、配置XML、跳转Intent action、弹窗Builder与strings原文均可直接读取；无加壳、无AES/密文载荷、无远端HTML下发。仅StartActivityAlertDialogFragment.onCreate方法体未逐行反编译，结论由类字段与Builder配置支撑。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `95842916f30215c56b051d2068b258cfb156de93984a4ea79e7ce250bb22e14f` |
| 包名 / 年份 | `org.kde.kdeconnect_tp` / 2025-2026 |
| 家族 / 品类 | **系统效率与通用辅助**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/org.kde.kdeconnect_tp_13703.apk |
| 桌面显示名 | KDE Connect |
| 引导页宣称品牌/身份 | KDE Connect（KDE 官方开源项目，身份真实） |
| 系统无障碍列表服务名 | KDE Connect（服务未单独声明android:label，系统列表回退为应用名，描述为 Receive remote mouse movement and Keyboard input） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `org.kde.kdeconnect.KdeConnectAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Receive remote mouse movement and Keyboard input / Receive remote mouse movement and Keyboard input |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | org.kde.kdeconnect.ui.MainActivity | LAUNCHER 冷启动 onCreate | 原生Activity | 无 | 无强制操作；冷启动不涉及无障碍申请 | `org.kde.kdeconnect.ui.MainActivity` |
| 2 | 业务功能触发 | org.kde.kdeconnect.ui.DeviceFragment 插件列表（Remote input / Mouse receiver、Remote keyboard 插件项） | 用户配对桌面设备后，在设备详情页查看/启用插件，refreshUI 检测该插件所需无障碍权限未授予 | 原生Activity | **原文**：To receive touch inputs remotely you need to grant Accessibility permissions<br>**译注**：要远程接收触控输入，你需要授予无障碍权限 | 点击插件权限提示项以查看说明弹窗 | `org.kde.kdeconnect.ui.DeviceFragment#refreshUI$lambda$0$0$0$6$0` |
| 3 | 引导说明页 | org.kde.kdeconnect.ui.StartActivityAlertDialogFragment（AlertDialogFragment 子类） | MouseReceiverPlugin.getPermissionExplanationDialog() / RemoteKeyboardPlugin.getPermissionExplanationDialog() 返回该 DialogFragment 并被 show | 原生Dialog | **原文**：title: Receive remote mouse movement \| message: To receive touch inputs remotely you need to grant Accessibility permissions \| positive: Open accessibility settings \| negative: cancel<br>**译注**：标题『接收远程鼠标移动』；正文『要远程接收触控输入，你需要授予无障碍权限』；按钮『打开无障碍设置』/『取消』 | 点击『打开无障碍设置』继续，或点击『取消』放弃（存在明确取消按钮，可跳过） | `org.kde.kdeconnect.plugins.mousereceiver.MouseReceiverPlugin#getPermissionExplanationDialog` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 点击正按钮，StartActivityAlertDialogFragment 以 ActivityResultLauncher 启动 setIntentAction 指定的 ACTION_ACCESSIBILITY_SETTINGS | 系统无障碍页 | 无 | 用户自行在系统列表中勾选 KDE Connect 服务并确认系统弹窗（应用不代点、不叠加遮罩） | `org.kde.kdeconnect.ui.StartActivityAlertDialogFragment#onCreate` |
| 5 | 获权后动作 | KdeConnectAccessibilityService 启动 + 插件重载（ActivityResultLauncher 回调 reloadPluginsOnResultLauncher） | 用户返回应用，ActivityResult 回调触发 reloadPluginsOnResult，重新查询真实授权状态并启用插件 | 原生Activity | 无 | 无进一步操作；应用不自点确认、不拦截撤权 | `org.kde.kdeconnect.KdeConnectAccessibilityService#onServiceConnected` |
| 6 | 拒权反馈循环 | StartActivityAlertDialogFragment 关闭后回到 DeviceFragment | 点击『取消』或从系统设置返回但未开启服务 | 原生Activity | 无 | 可继续使用剪贴板、文件传输等无需无障碍的功能 | `org.kde.kdeconnect.ui.StartActivityAlertDialogFragment#reloadPluginsOnResultLauncher$lambda$0` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目描述：res/xml/mouse_receiver_service.xml 的 android:description=@string/mouse_keyboard_receiver_service_description（原文 Receive remote mouse movement and Keyboard input）
- 插件未授权提示弹窗正文：strings.xml mouse_receiver_no_permissions（To receive touch inputs remotely you need to grant Accessibility permissions），由 StartActivityAlertDialogFragment 以原生 AlertDialog 呈现
- 弹窗标题：strings.xml mouse_receiver_plugin_description（Receive remote mouse movement），id 0x7f120155
- 弹窗正按钮：strings.xml open_accessibility_settings（Open accessibility settings），id 0x7f1201f3
- 弹窗负按钮：strings.xml cancel（cancel），id 0x7f120060
- Remote keyboard 插件复用同一弹窗与同一 ACTION_ACCESSIBILITY_SETTINGS 跳转（RemoteKeyboardPlugin#getPermissionExplanationDialog）
- 无 WebView/HTML 引导页、无悬浮窗引导遮罩、无高仿系统设置页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To receive touch inputs remotely you need to grant Accessibility permissions | 要远程接收触控输入，你需要授予无障碍权限 | `res/values/strings.xml key=mouse_receiver_no_permissions (line 211)` | 良性透明说明 |
| en | Receive remote mouse movement | 接收远程鼠标移动 | `res/values/strings.xml key=mouse_receiver_plugin_description (0x7f120155)，用作弹窗标题` | 良性透明说明 |
| en | Open accessibility settings | 打开无障碍设置 | `res/values/strings.xml key=open_accessibility_settings (0x7f1201f3)，弹窗正按钮` | 受限设置分步教学 |
| en | Receive remote mouse movement and Keyboard input | 接收远程鼠标移动与键盘输入 | `res/values/strings.xml key=mouse_keyboard_receiver_service_description (line 210)，对应 res/xml/mouse_receiver_service.xml android:description` | 良性透明说明 |
| en | cancel | 取消 | `res/values/strings.xml key=cancel (0x7f120060)，弹窗负按钮` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环：弹窗由插件权限检测单次触发，类内 launched 标志位防止重复启动；用户点『取消』即关闭弹窗，从系统设置返回但未授权时仅通过 ActivityResultLauncher 回调重载插件并保持禁用状态，未发现 onResume 重跳、Timer 定时拉起或通知栏反复催促
- **遮罩叠层 / 高仿系统设置页**：无。无障碍服务仅在 onServiceConnected 通过 WindowManager 添加一个 8px 可见性（setVisibility(8)）的鼠标指针 View 作为光标叠层，非引导遮罩；无全屏悬浮窗、无高仿系统无障碍开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转或『右上角菜单允许受限设置』类分步教学，直接跳 ACTION_ACCESSIBILITY_SETTINGS
- **获权后即时行为与防撤权机制**：无。performGlobalAction(1/2/3/21) 仅由已配对桌面端鼠标点击/双击报文触发，用于模拟 BACK/HOME/RECENTS/右键，不存在监听设置页或阻止撤权的逻辑；未发现自点确认或自授权代码
- **良性降级 / 替代方案**：具备：拒绝授权后仅『远程鼠标/远程键盘』插件不可用，剪贴板同步、文件传输、通知同步、多媒体控制等其余插件不受影响；弹窗提供明确 cancel 退出路径

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在用户配对设备后进入 DeviceFragment 并点击『Remote input / Remote keyboard』插件项、或点击该插件的权限提示时拉起；亦可监测 Activity 启动 intent action == android.settings.ACCESSIBILITY_SETTINGS 的瞬间抓取跳转前弹窗与跳转后系统页
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。该应用无加壳、无动态加载、无远端 HTML 引导；唯一轻度盲区为无障碍配置声明 canRetrieveWindowContent=true 而 onAccessibilityEvent 为空实现（能力超声明但未使用），纯 UTG 无法观察『未使用』这一事实，需结合静态代码确认。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **按需权限说明弹窗页（跳转前）** | org.kde.kdeconnect.ui.StartActivityAlertDialogFragment 呈现的原生 AlertDialog，标题『接收远程鼠标移动』+ 正文『要远程接收触控输入…』+ 按钮『打开无障碍设置』/『取消』 | 这是全应用唯一的无障碍引导面，可确认是否具备取消按钮、文案是否如实说明用途、有无恐吓/伪造措辞 | 存在可点击的『取消』按钮节点（可判定非不可取消强制）；弹窗文本节点与 strings.xml 原文一致，无空白/换行挤出警告的异常节点；无覆盖屏幕的额外悬浮窗节点（无遮罩栈） |
| **系统无障碍服务列表项** | 设置 > 无障碍 > 已下载/已安装的服务中 KDE Connect 条目，副标题『接收远程鼠标移动与键盘输入』 | 核对系统侧展示的服务名与描述是否与应用真实身份、真实能力一致，排除冒名与超范围声明 | 条目名称为 KDE Connect，未使用同形字或空白填充；描述文本与 android:description 完全一致；开关初始为关闭，需用户主动开启 |
| **返回应用后的插件状态页** | DeviceFragment 中 Remote input 插件项由『未授权』变为可用 | 验证是否存在返回后死循环重跳设置页或反复弹窗的诱导行为 | 返回后停留在应用界面，未自动再次跳转 ACCESSIBILITY_SETTINGS；无新增悬浮窗/通知催促节点；未授权时功能项保持禁用但应用其余功能可用 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `org.kde.kdeconnect.plugins.mousereceiver.MouseReceiverPlugin#getPermissionExplanationDialog`
- `org.kde.kdeconnect.plugins.remotekeyboard.RemoteKeyboardPlugin#getPermissionExplanationDialog`
- `org.kde.kdeconnect.ui.StartActivityAlertDialogFragment#onCreate`
- `org.kde.kdeconnect.KdeConnectAccessibilityService#onServiceConnected`
- `res/xml/mouse_receiver_service.xml`
- `res/values/strings.xml (mouse_receiver_no_permissions / open_accessibility_settings)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（KDE Connect 无障碍权限引导链）

**核心事实（纯静态可见，无加壳/无密文载荷）**

- 无障碍服务 [KdeConnectAccessibilityService](<resource-unit:#1.dex1 code:org.kde.kdeconnect.KdeConnectAccessibilityService>) 仅在 `onServiceConnected` 中 inflate 一个光标 View（`2131492956`）并 `WindowManager.addView`，作为远程鼠标指针叠层；`onAccessibilityEvent`、`onInterrupt` 均为空实现 —— **不读取屏幕内容、不监听用户操作**，与 `mouse_receiver_service.xml` 声明的能力相匹配（`canRetrieveWindowContent="true"` 属超声明但未被使用）。
- `performGlobalAction` 仅由**已配对桌面端**下发的鼠标报文驱动（`singleclick/doubleclick/middleclick/backclick` → `click()` / `performGlobalAction(1/2/3/21)`），属功能实现，不构成撤权拦截。
- 引导链只有**一条**：`MouseReceiverPlugin.getPermissionExplanationDialog()` / `RemoteKeyboardPlugin.getPermissionExplanationDialog()` 构造 [StartActivityAlertDialogFragment](<resource-unit:#1.dex1 code:org.kde.kdeconnect.ui.StartActivityAlertDialogFragment>)（`setIntentAction("android.settings.ACCESSIBILITY_SETTINGS")`、`setReloadPluginsOnResult(true)`），由 `DeviceFragment.refreshUI$lambda$0$0$0$6$0` 在**插件权限缺失时**弹出。
- 弹窗为标题+说明+「打开无障碍设置」+「取消」四要素，`launched` 标志位 + `ActivityResultLauncher` 回调（返回后重载插件）表明**单次触发、返回即重新读取真实授权状态**，未见 `onResume` 死循环重跳、定时拉起、悬浮遮罩或高仿系统设置页。
- 系统无障碍列表中展示的应用名 `KDE Connect` 与 android:description `Receive remote mouse movement and Keyboard input` 如实描述用途，**无身份伪装、无空白/同形字挤出、无多 alias、无伪造 isAccessibilityTool**。
- 预筛的 `JUMP_A11Y_SETTINGS` 即上述合法跳转；`PERFORM_GLOBAL_ACTION` 为远程点击模拟；`SYSTEM_ALERT_WINDOW`/`QUERY_ALL_PACKAGES` 等属该开源跨设备工具既有功能面，未与无障碍引导链耦合。

**判定**：该应用属**按需引导 + 明确可取消 + 获权后无驻留滥用**的良性无障碍使用模式，未发现权限诱导、恐吓循环或遮罩欺骗。无已确认风险可登记。

**覆盖边界**：`StartActivityAlertDialogFragment.onCreate` 未逐行反编译，其"仅首次启动 + 结果回调重载"结论由类骨架字段（`launched`、`reloadPluginsOnResultLauncher`）与 Builder 配置推断；字符串与弹窗文案已核实原文。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链完整静态可见：服务实现、配置XML、跳转Intent action、弹窗Builder与strings原文均可直接读取；无加壳、无AES/密文载荷、无远端HTML下发。仅StartActivityAlertDialogFragment.onCreate方法体未逐行反编译，结论由类字段与Builder配置支撑。",
  "summary_one_liner": "KDE Connect 仅在用户启用远程鼠标/远程键盘插件且检测到无障碍未授权时，弹出一个可取消的原生说明弹窗，点击『打开无障碍设置』直达系统无障碍页，返回后重载插件读取真实授权状态，无循环重跳、无遮罩、无伪装。",
  "disguise_identity": {
    "app_display_name": "KDE Connect",
    "claimed_brand_or_persona": "KDE Connect（KDE 官方开源项目，身份真实）",
    "a11y_service_label": "KDE Connect（服务未单独声明android:label，系统列表回退为应用名，描述为 Receive remote mouse movement and Keyboard input）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "org.kde.kdeconnect.ui.MainActivity",
      "trigger_event": "LAUNCHER 冷启动 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅展示设备列表，不弹出任何无障碍引导",
      "user_action_requested": "无强制操作；冷启动不涉及无障碍申请",
      "code_anchor": "org.kde.kdeconnect.ui.MainActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "org.kde.kdeconnect.ui.DeviceFragment 插件列表（Remote input / Mouse receiver、Remote keyboard 插件项）",
      "trigger_event": "用户配对桌面设备后，在设备详情页查看/启用插件，refreshUI 检测该插件所需无障碍权限未授予",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "To receive touch inputs remotely you need to grant Accessibility permissions",
      "shown_text_zh": "要远程接收触控输入，你需要授予无障碍权限",
      "user_action_requested": "点击插件权限提示项以查看说明弹窗",
      "code_anchor": "org.kde.kdeconnect.ui.DeviceFragment#refreshUI$lambda$0$0$0$6$0"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "org.kde.kdeconnect.ui.StartActivityAlertDialogFragment（AlertDialogFragment 子类）",
      "trigger_event": "MouseReceiverPlugin.getPermissionExplanationDialog() / RemoteKeyboardPlugin.getPermissionExplanationDialog() 返回该 DialogFragment 并被 show",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "title: Receive remote mouse movement | message: To receive touch inputs remotely you need to grant Accessibility permissions | positive: Open accessibility settings | negative: cancel",
      "shown_text_zh": "标题『接收远程鼠标移动』；正文『要远程接收触控输入，你需要授予无障碍权限』；按钮『打开无障碍设置』/『取消』",
      "user_action_requested": "点击『打开无障碍设置』继续，或点击『取消』放弃（存在明确取消按钮，可跳过）",
      "code_anchor": "org.kde.kdeconnect.plugins.mousereceiver.MouseReceiverPlugin#getPermissionExplanationDialog"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "点击正按钮，StartActivityAlertDialogFragment 以 ActivityResultLauncher 启动 setIntentAction 指定的 ACTION_ACCESSIBILITY_SETTINGS",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "进入系统无障碍服务列表，条目显示 KDE Connect 及描述『接收远程鼠标移动与键盘输入』",
      "user_action_requested": "用户自行在系统列表中勾选 KDE Connect 服务并确认系统弹窗（应用不代点、不叠加遮罩）",
      "code_anchor": "org.kde.kdeconnect.ui.StartActivityAlertDialogFragment#onCreate"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "KdeConnectAccessibilityService 启动 + 插件重载（ActivityResultLauncher 回调 reloadPluginsOnResultLauncher）",
      "trigger_event": "用户返回应用，ActivityResult 回调触发 reloadPluginsOnResult，重新查询真实授权状态并启用插件",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "插件变为可用；服务 onServiceConnected 添加隐藏的鼠标指针叠层，仅在收到已配对桌面端鼠标报文时显示与移动",
      "user_action_requested": "无进一步操作；应用不自点确认、不拦截撤权",
      "code_anchor": "org.kde.kdeconnect.KdeConnectAccessibilityService#onServiceConnected"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "StartActivityAlertDialogFragment 关闭后回到 DeviceFragment",
      "trigger_event": "点击『取消』或从系统设置返回但未开启服务",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "弹窗关闭，插件保持禁用状态，功能不可用但不阻断其他功能，无自动重跳",
      "user_action_requested": "可继续使用剪贴板、文件传输等无需无障碍的功能",
      "code_anchor": "org.kde.kdeconnect.ui.StartActivityAlertDialogFragment#reloadPluginsOnResultLauncher$lambda$0"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目描述：res/xml/mouse_receiver_service.xml 的 android:description=@string/mouse_keyboard_receiver_service_description（原文 Receive remote mouse movement and Keyboard input）",
    "插件未授权提示弹窗正文：strings.xml mouse_receiver_no_permissions（To receive touch inputs remotely you need to grant Accessibility permissions），由 StartActivityAlertDialogFragment 以原生 AlertDialog 呈现",
    "弹窗标题：strings.xml mouse_receiver_plugin_description（Receive remote mouse movement），id 0x7f120155",
    "弹窗正按钮：strings.xml open_accessibility_settings（Open accessibility settings），id 0x7f1201f3",
    "弹窗负按钮：strings.xml cancel（cancel），id 0x7f120060",
    "Remote keyboard 插件复用同一弹窗与同一 ACTION_ACCESSIBILITY_SETTINGS 跳转（RemoteKeyboardPlugin#getPermissionExplanationDialog）",
    "无 WebView/HTML 引导页、无悬浮窗引导遮罩、无高仿系统设置页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To receive touch inputs remotely you need to grant Accessibility permissions",
      "text_zh": "要远程接收触控输入，你需要授予无障碍权限",
      "source_location": "res/values/strings.xml key=mouse_receiver_no_permissions (line 211)",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Receive remote mouse movement",
      "text_zh": "接收远程鼠标移动",
      "source_location": "res/values/strings.xml key=mouse_receiver_plugin_description (0x7f120155)，用作弹窗标题",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Open accessibility settings",
      "text_zh": "打开无障碍设置",
      "source_location": "res/values/strings.xml key=open_accessibility_settings (0x7f1201f3)，弹窗正按钮",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Receive remote mouse movement and Keyboard input",
      "text_zh": "接收远程鼠标移动与键盘输入",
      "source_location": "res/values/strings.xml key=mouse_keyboard_receiver_service_description (line 210)，对应 res/xml/mouse_receiver_service.xml android:description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "cancel",
      "text_zh": "取消",
      "source_location": "res/values/strings.xml key=cancel (0x7f120060)，弹窗负按钮",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环：弹窗由插件权限检测单次触发，类内 launched 标志位防止重复启动；用户点『取消』即关闭弹窗，从系统设置返回但未授权时仅通过 ActivityResultLauncher 回调重载插件并保持禁用状态，未发现 onResume 重跳、Timer 定时拉起或通知栏反复催促",
    "overlay_or_fake_settings": "无。无障碍服务仅在 onServiceConnected 通过 WindowManager 添加一个 8px 可见性（setVisibility(8)）的鼠标指针 View 作为光标叠层，非引导遮罩；无全屏悬浮窗、无高仿系统无障碍开关页",
    "restricted_settings_13plus_coaching": "无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转或『右上角菜单允许受限设置』类分步教学，直接跳 ACTION_ACCESSIBILITY_SETTINGS",
    "post_grant_anti_removal": "无。performGlobalAction(1/2/3/21) 仅由已配对桌面端鼠标点击/双击报文触发，用于模拟 BACK/HOME/RECENTS/右键，不存在监听设置页或阻止撤权的逻辑；未发现自点确认或自授权代码",
    "benign_graceful_degradation": "具备：拒绝授权后仅『远程鼠标/远程键盘』插件不可用，剪贴板同步、文件传输、通知同步、多媒体控制等其余插件不受影响；弹窗提供明确 cancel 退出路径"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在用户配对设备后进入 DeviceFragment 并点击『Remote input / Remote keyboard』插件项、或点击该插件的权限提示时拉起；亦可监测 Activity 启动 intent action == android.settings.ACCESSIBILITY_SETTINGS 的瞬间抓取跳转前弹窗与跳转后系统页",
    "key_pages_to_capture": [
      {
        "page_role": "按需权限说明弹窗页（跳转前）",
        "page_identifier": "org.kde.kdeconnect.ui.StartActivityAlertDialogFragment 呈现的原生 AlertDialog，标题『接收远程鼠标移动』+ 正文『要远程接收触控输入…』+ 按钮『打开无障碍设置』/『取消』",
        "why_most_useful": "这是全应用唯一的无障碍引导面，可确认是否具备取消按钮、文案是否如实说明用途、有无恐吓/伪造措辞",
        "observable_utg_signals": [
          "存在可点击的『取消』按钮节点（可判定非不可取消强制）",
          "弹窗文本节点与 strings.xml 原文一致，无空白/换行挤出警告的异常节点",
          "无覆盖屏幕的额外悬浮窗节点（无遮罩栈）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 > 无障碍 > 已下载/已安装的服务中 KDE Connect 条目，副标题『接收远程鼠标移动与键盘输入』",
        "why_most_useful": "核对系统侧展示的服务名与描述是否与应用真实身份、真实能力一致，排除冒名与超范围声明",
        "observable_utg_signals": [
          "条目名称为 KDE Connect，未使用同形字或空白填充",
          "描述文本与 android:description 完全一致",
          "开关初始为关闭，需用户主动开启"
        ]
      },
      {
        "page_role": "返回应用后的插件状态页",
        "page_identifier": "DeviceFragment 中 Remote input 插件项由『未授权』变为可用",
        "why_most_useful": "验证是否存在返回后死循环重跳设置页或反复弹窗的诱导行为",
        "observable_utg_signals": [
          "返回后停留在应用界面，未自动再次跳转 ACCESSIBILITY_SETTINGS",
          "无新增悬浮窗/通知催促节点",
          "未授权时功能项保持禁用但应用其余功能可用"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。该应用无加壳、无动态加载、无远端 HTML 引导；唯一轻度盲区为无障碍配置声明 canRetrieveWindowContent=true 而 onAccessibilityEvent 为空实现（能力超声明但未使用），纯 UTG 无法观察『未使用』这一事实，需结合静态代码确认。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "org.kde.kdeconnect.plugins.mousereceiver.MouseReceiverPlugin#getPermissionExplanationDialog",
    "org.kde.kdeconnect.plugins.remotekeyboard.RemoteKeyboardPlugin#getPermissionExplanationDialog",
    "org.kde.kdeconnect.ui.StartActivityAlertDialogFragment#onCreate",
    "org.kde.kdeconnect.KdeConnectAccessibilityService#onServiceConnected",
    "res/xml/mouse_receiver_service.xml",
    "res/values/strings.xml (mouse_receiver_no_permissions / open_accessibility_settings)"
  ]
}
```

</details>
