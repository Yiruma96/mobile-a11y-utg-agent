# BN_009__0d8956b479｜专注自律与防沉迷管控 — TimeLimit

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：205.7s

## 1. 一句话核心结论

- **核心申请方式**：TimeLimit 在设备/权限管理页列出无障碍权限项，未授予时先弹原生说明对话框（含 Cancel），用户点 Next 后直接跳转系统 ACCESSIBILITY_SETTINGS，文案如实说明用于锁屏前按 Home 键，无遮罩、无循环重跳、无受限设置绕过教学
- **静态可见性说明**：无障碍服务声明、跳转 Intent、确认对话框文案与按钮资源全部在 classes.dex 与 res/values/strings.xml、res/xml/accesibility.xml 中静态可见，无加壳、无加密载荷、无远端 HTML 教学页
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0d8956b479c988d5988d44badfb30b67eb1bccda8179228d60331dfdad422474` |
| 包名 / 年份 | `io.timelimit.android.aosp.direct` / 2025-2026 |
| 家族 / 品类 | **专注自律与防沉迷管控**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/io.timelimit.android.aosp.direct_233.apk |
| 桌面显示名 | TimeLimit |
| 引导页宣称品牌/身份 | TimeLimit（TimeLimit.io 开源专注自律/防沉迷管控应用） |
| 系统无障碍列表服务名 | TimeLimit（服务未设置 android:label，继承 application 的 @string/app_name） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。代码经 R8 混淆（包名压缩为 s9/nc/ab 等），但资源字符串、无障碍描述与系统设置跳转均为明文，未使用同形字、空白挤出、多 activity-alias 或伪造 isAccessibilityTool |
| 无障碍服务类名 | `io.timelimit.android.integration.platform.android.AccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | This is used to "press" the home button before showing the lock screen. This fixes blocking in some cases. Moreover, this is one way to allow TimeLimit at newer Android versions to open the lockscreen. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | io.timelimit.android.ui.MainActivity → 设备/权限管理页 io.timelimit.android.ui.manage.device.manage.ManageDeviceFragment | 用户主动进入“设备管理/权限”页面，onCreateView 绑定权限状态流时渲染缺失项 | 原生Activity | **原文**：Draw over other Apps or Accessibility service is required<br>**译注**：需要“在其他应用上层显示”权限或无障碍服务 | 查看缺失权限提示并点击 Modify 修改（非强制，可返回其他页面） | `io.timelimit.android.ui.manage.device.manage.ManageDeviceFragment#D / res/values/strings.xml activity_launch_permission_required_and_missing_title` |
| 2 | 引导说明页 | PermissionInfoConfirmDialog（nc.i，AppCompat AlertDialog） | 点击无障碍权限项 → s9.e#z 判定未授予且 pVar==p.f，add(PermissionInfoConfirmDialog) | 原生Dialog | **原文**：Accessibility service / This is used to "press" the home button before showing the lock screen. This fixes blocking in some cases. Moreover, this is one way to allow TimeLimit at newer Android versions to open the lockscreen.<br>**译注**：无障碍服务 / 该权限用于在显示锁屏前“按下”Home 键，修复部分场景下的阻断问题；同时也是让 TimeLimit 在较新 Android 版本上打开锁屏的一种方式。 | 点“Next”前往系统设置，或点“Cancel”取消（存在明确的取消/跳过路径） | `nc.i#d0（标题 2131886751=manage_device_permission_accessibility_title，正文 2131886750=manage_device_permission_accessibility_text，确认 2131887264=wiazrd_next，取消 2131886531=generic_cancel）` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装的服务（android.settings.ACCESSIBILITY_SETTINGS） | 对话框正按钮 onClick 回调 ab.d#onClick(default 分支) → s9.e.z(activity, o, p.g) → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(FLAG_ACTIVITY_NEW_TASK)) | 系统无障碍页 | **原文**：This is used to "press" the home button before showing the lock screen. This fixes blocking in some cases. Moreover, this is one way to allow TimeLimit at newer Android versions to open the lockscreen.<br>**译注**：系统无障碍列表中 TimeLimit 服务下方显示的说明文字，内容同上（诚实说明用途） | 用户在系统页面手动开启 TimeLimit 无障碍服务开关 | `s9.e#z / ab.d#onClick / res/xml/accesibility.xml（android:description=@string/manage_device_permission_accessibility_text）` |
| 4 | 拒权反馈循环 | 返回 ManageDeviceFragment，权限项仍显示未授予状态 | 从系统设置返回后权限状态流重新发射，仅刷新列表状态；跳转异常时 Toast(2131886521) | 原生Activity | **原文**：Accessibility service / not granted（manage_device_permission_status_not_granted）<br>**译注**：无障碍服务 / 未授予（状态标识，需用户再次主动点击） | 无强制动作，用户可离开页面；不存在 onResume 死循环重跳或定时器拉起 | `s9.e#z（catch 分支仅 Toast）/ io.timelimit.android.ui.manage.device.manage.ManageDeviceFragment#D` |
| 5 | 获权后动作 | io.timelimit.android.integration.platform.android.AccessibilityService（系统绑定后运行） | 系统 BIND_ACCESSIBILITY_SERVICE 绑定服务，服务在锁屏阻断场景执行 performGlobalAction(HOME) | 不可静态还原（运行期行为，未在本次定向核验中动态验证） | 无 | 无 | `io.timelimit.android.integration.platform.android.AccessibilityService / res/xml/accesibility.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 设备/权限管理页（ManageDeviceFragment，layout 2131492964 内 activityLaunchPermissionMissing 区块）显示“Draw over other Apps or Accessibility service is required”
- 未授予时弹出的原生 AlertDialog（PermissionInfoConfirmDialog / nc.i#d0）：标题“Accessibility service”，正文为 manage_device_permission_accessibility_text 全文，按钮 Next / Cancel
- 系统无障碍服务列表中 TimeLimit 服务项下方的 android:description（res/xml/accesibility.xml → @string/manage_device_permission_accessibility_text）
- 权限状态行文本 manage_device_permission_status_granted / not_granted 等状态标签（strings.xml）
- 无 WebView/HTML 教学页、无悬浮窗引导遮罩、无高仿系统设置界面

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility service | 无障碍服务 | `res/values/strings.xml: manage_device_permission_accessibility_title` | 良性透明说明 |
| en | This is used to "press" the home button before showing the lock screen. This fixes blocking in some cases. Moreover, this is one way to allow TimeLimit at newer Android versions to open the lockscreen. | 该权限用于在显示锁屏前“按下”Home 键，用于修复部分场景下的阻断问题；同时也是让 TimeLimit 在较新 Android 版本上打开锁屏的一种方式。 | `res/values/strings.xml: manage_device_permission_accessibility_text（同时作为 res/xml/accesibility.xml 的 android:description）` | 良性透明说明 |
| en | Draw over other Apps or Accessibility service is required | 需要“在其他应用上层显示”权限或无障碍服务 | `res/values/strings.xml: activity_launch_permission_required_and_missing_title（ManageDeviceFragment#D 引用 2131886133）` | 良性透明说明 |
| en | Next | 下一步 | `res/values/strings.xml: wiazrd_next（nc.i#d0 确认按钮 2131887264）` | 受限设置分步教学 |
| en | Cancel | 取消 | `res/values/strings.xml: generic_cancel（nc.i#d0 取消按钮 2131886531）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性安全降级：用户点 Cancel 仅关闭 PermissionInfoConfirmDialog；从系统设置返回后只按权限状态流刷新“not granted”标签，不自动重跳、无 onResume 死循环、无定时器拉起；仅当 startActivity 抛异常时 Toast(2131886521) 提示
- **遮罩叠层 / 高仿系统设置页**：无。全程使用 AppCompat 原生 AlertDialog + 真实系统设置页，未叠放半透明引导遮罩、未渲染高仿系统无障碍开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。DEX 中无 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无“点右上角菜单允许受限设置”或 Session 安装器绕过文案；受限设置相关预筛线索（RESTRICTED_STR / SESSION_INSTALLER）在本应用的权限引导链路上未被使用
- **获权后即时行为与防撤权机制**：无。未发现获权后自动点击确认、自动自授权，或监听设置页使用 GLOBAL_ACTION_BACK/HOME 阻止撤权；PERFORM_GLOBAL_ACTION 用于锁屏前返回桌面，与声明的无障碍用途一致
- **良性降级 / 替代方案**：具备：无障碍仅为可选权限项之一（与悬浮窗、使用情况访问、通知使用权、设备管理员并列），缺失时权限页仅显示提示与 Modify 按钮，应用继续可用；对话框提供 Cancel，跳转失败仅 Toast 提示，不阻断使用

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 的目标为 android.settings.ACCESSIBILITY_SETTINGS（来源 s9.e#z），或监测到 PermissionInfoConfirmDialog（标题“Accessibility service”、按钮“Next”/“Cancel”）被 add 到 FragmentManager 的瞬间拉起 UTG
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一未覆盖的是获权后 AccessibilityService 的运行期行为（锁屏前 performGlobalAction(HOME)），该行为已由 Manifest 与无障碍描述公开声明，不属隐藏载荷；本次未启动动态分析验证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前原生说明对话框页** | AppCompat AlertDialog，标题“Accessibility service”，正文以“This is used to "press" the home button before showing the lock screen”开头，按钮 Next / Cancel | 该对话框是唯一的获权前告知环节，可判定是否提供取消路径、文案是否与实际用途一致 | 存在“Cancel”可点击节点（可取消性）；正文文本与 strings.xml manage_device_permission_accessibility_text 一致；无图片/无伪造系统控件样式 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中 label=TimeLimit、描述为 Home 键/锁屏说明的服务条目 | 核对系统列表中展示的服务名与描述是否与包内资源一致，排除空白/同形字伪装 | 条目文本“TimeLimit”；描述文本与 manage_device_permission_accessibility_text 完全一致；无空白名称或异常长名称 |
| **权限管理页缺失提示区** | ManageDeviceFragment 布局内 activityLaunchPermissionMissing 区块，文本“Draw over other Apps or Accessibility service is required” | 确认触发时机为功能页按需引导而非冷启动强制阻塞 | 页面栈是否由 MainActivity 内导航进入；是否同时存在其他权限项（并列可选） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `s9.e#z`
- `nc.i#d0`
- `ab.d#onClick`
- `io.timelimit.android.ui.manage.device.manage.ManageDeviceFragment#D`
- `res/xml/accesibility.xml`
- `res/values/strings.xml (manage_device_permission_accessibility_text)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**无障碍权限申请路径完整静态可见，未发现诱导或伪装，属良性透明申请。**

- **跳转点唯一且集中**：整个 DEX 中只有一处 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(0x10000000))`，位于 [s9.e#z](<resource-unit:#1.dex1 code:s9.e#z>)（权限管理方法）。该方法按 `SystemPermission` 枚举分支处理：设备管理员（`ADD_DEVICE_ADMIN`/`SECURITY_SETTINGS`）、使用情况访问（`USAGE_ACCESS_SETTINGS`）、通知使用权、悬浮窗（`MANAGE_OVERLAY_PERMISSION`）、无障碍（`ACCESSIBILITY_SETTINGS`），跳转异常时只 `Toast` 提示（`2131886521`），无重试或循环。
- **跳转前有原生确认对话框，可取消**：`z()` 在 `pVar == p.f` 且权限未授予时先弹 `PermissionInfoConfirmDialog`（[nc.i#d0](<resource-unit:#1.dex1 code:nc.i#d0>)）。无障碍对应 `(title=2131886751, text=2131886750)`，即 `manage_device_permission_accessibility_title/text`；正按钮为 `2131887264` = `wiazrd_next`("Next")，负按钮为 `2131886531` = `generic_cancel`("Cancel")。用户点 Next 才由 [ab.d#onClick](<resource-unit:#1.dex1 code:ab.d#onClick>) 回调 `s9.e.z(..., p.g)` 真正拉起系统页；点 Cancel 则仅关闭对话框，无死循环重跳。
- **文案如实说明用途**：`strings.xml:703` 说明该服务用于“在显示锁屏前按 Home 键”并协助新系统打开锁屏，与锁屏阻断的实际用途一致；系统无障碍列表中的描述直接取自该资源（[accesibility.xml](<resource-unit:#1 file:res/xml/accesibility.xml>)），服务未设置 `android:label`，因此在系统列表显示应用名 `TimeLimit`，无空白或同形字伪装。
- **入口为功能页权限清单，不是冷启动阻塞**：`ManageDeviceFragment#D` 在“设备/权限管理”页用 `activityLaunchPermissionMissing` 区块展示 `2131886133`（`activity_launch_permission_required_and_missing_title`，“Draw over other Apps or Accessibility service is required”）和 Modify 按钮，属用户主动进入的权限配置页。
- **未发现**：`ACTION_APPLICATION_DETAILS_SETTINGS` 跳转、受限设置（Android 13+）分步教学、Session 安装器绕过、悬浮遮罩/高仿设置页、获权后 `GLOBAL_ACTION_BACK/HOME` 反撤权、WebView 远端教学页（包内无相关字符串命中）。`PERFORM_GLOBAL_ACTION` 类线索用于锁屏前返回桌面，与 Manifest 中的无障碍描述一致，属声明范围内的功能实现。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍服务声明、跳转 Intent、确认对话框文案与按钮资源全部在 classes.dex 与 res/values/strings.xml、res/xml/accesibility.xml 中静态可见，无加壳、无加密载荷、无远端 HTML 教学页",
  "summary_one_liner": "TimeLimit 在设备/权限管理页列出无障碍权限项，未授予时先弹原生说明对话框（含 Cancel），用户点 Next 后直接跳转系统 ACCESSIBILITY_SETTINGS，文案如实说明用于锁屏前按 Home 键，无遮罩、无循环重跳、无受限设置绕过教学",
  "disguise_identity": {
    "app_display_name": "TimeLimit",
    "claimed_brand_or_persona": "TimeLimit（TimeLimit.io 开源专注自律/防沉迷管控应用）",
    "a11y_service_label": "TimeLimit（服务未设置 android:label，继承 application 的 @string/app_name）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。代码经 R8 混淆（包名压缩为 s9/nc/ab 等），但资源字符串、无障碍描述与系统设置跳转均为明文，未使用同形字、空白挤出、多 activity-alias 或伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "io.timelimit.android.ui.MainActivity → 设备/权限管理页 io.timelimit.android.ui.manage.device.manage.ManageDeviceFragment",
      "trigger_event": "用户主动进入“设备管理/权限”页面，onCreateView 绑定权限状态流时渲染缺失项",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Draw over other Apps or Accessibility service is required",
      "shown_text_zh": "需要“在其他应用上层显示”权限或无障碍服务",
      "user_action_requested": "查看缺失权限提示并点击 Modify 修改（非强制，可返回其他页面）",
      "code_anchor": "io.timelimit.android.ui.manage.device.manage.ManageDeviceFragment#D / res/values/strings.xml activity_launch_permission_required_and_missing_title"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "PermissionInfoConfirmDialog（nc.i，AppCompat AlertDialog）",
      "trigger_event": "点击无障碍权限项 → s9.e#z 判定未授予且 pVar==p.f，add(PermissionInfoConfirmDialog)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Accessibility service / This is used to \"press\" the home button before showing the lock screen. This fixes blocking in some cases. Moreover, this is one way to allow TimeLimit at newer Android versions to open the lockscreen.",
      "shown_text_zh": "无障碍服务 / 该权限用于在显示锁屏前“按下”Home 键，修复部分场景下的阻断问题；同时也是让 TimeLimit 在较新 Android 版本上打开锁屏的一种方式。",
      "user_action_requested": "点“Next”前往系统设置，或点“Cancel”取消（存在明确的取消/跳过路径）",
      "code_anchor": "nc.i#d0（标题 2131886751=manage_device_permission_accessibility_title，正文 2131886750=manage_device_permission_accessibility_text，确认 2131887264=wiazrd_next，取消 2131886531=generic_cancel）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装的服务（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "对话框正按钮 onClick 回调 ab.d#onClick(default 分支) → s9.e.z(activity, o, p.g) → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(FLAG_ACTIVITY_NEW_TASK))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "This is used to \"press\" the home button before showing the lock screen. This fixes blocking in some cases. Moreover, this is one way to allow TimeLimit at newer Android versions to open the lockscreen.",
      "shown_text_zh": "系统无障碍列表中 TimeLimit 服务下方显示的说明文字，内容同上（诚实说明用途）",
      "user_action_requested": "用户在系统页面手动开启 TimeLimit 无障碍服务开关",
      "code_anchor": "s9.e#z / ab.d#onClick / res/xml/accesibility.xml（android:description=@string/manage_device_permission_accessibility_text）"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 ManageDeviceFragment，权限项仍显示未授予状态",
      "trigger_event": "从系统设置返回后权限状态流重新发射，仅刷新列表状态；跳转异常时 Toast(2131886521)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility service / not granted（manage_device_permission_status_not_granted）",
      "shown_text_zh": "无障碍服务 / 未授予（状态标识，需用户再次主动点击）",
      "user_action_requested": "无强制动作，用户可离开页面；不存在 onResume 死循环重跳或定时器拉起",
      "code_anchor": "s9.e#z（catch 分支仅 Toast）/ io.timelimit.android.ui.manage.device.manage.ManageDeviceFragment#D"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "io.timelimit.android.integration.platform.android.AccessibilityService（系统绑定后运行）",
      "trigger_event": "系统 BIND_ACCESSIBILITY_SERVICE 绑定服务，服务在锁屏阻断场景执行 performGlobalAction(HOME)",
      "ui_carrier": "不可静态还原（运行期行为，未在本次定向核验中动态验证）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无额外界面；按声明用途在显示锁屏前返回桌面，以便锁屏界面正常弹出",
      "user_action_requested": "无",
      "code_anchor": "io.timelimit.android.integration.platform.android.AccessibilityService / res/xml/accesibility.xml"
    }
  ],
  "text_presentation_locations": [
    "设备/权限管理页（ManageDeviceFragment，layout 2131492964 内 activityLaunchPermissionMissing 区块）显示“Draw over other Apps or Accessibility service is required”",
    "未授予时弹出的原生 AlertDialog（PermissionInfoConfirmDialog / nc.i#d0）：标题“Accessibility service”，正文为 manage_device_permission_accessibility_text 全文，按钮 Next / Cancel",
    "系统无障碍服务列表中 TimeLimit 服务项下方的 android:description（res/xml/accesibility.xml → @string/manage_device_permission_accessibility_text）",
    "权限状态行文本 manage_device_permission_status_granted / not_granted 等状态标签（strings.xml）",
    "无 WebView/HTML 教学页、无悬浮窗引导遮罩、无高仿系统设置界面"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility service",
      "text_zh": "无障碍服务",
      "source_location": "res/values/strings.xml: manage_device_permission_accessibility_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This is used to \"press\" the home button before showing the lock screen. This fixes blocking in some cases. Moreover, this is one way to allow TimeLimit at newer Android versions to open the lockscreen.",
      "text_zh": "该权限用于在显示锁屏前“按下”Home 键，用于修复部分场景下的阻断问题；同时也是让 TimeLimit 在较新 Android 版本上打开锁屏的一种方式。",
      "source_location": "res/values/strings.xml: manage_device_permission_accessibility_text（同时作为 res/xml/accesibility.xml 的 android:description）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Draw over other Apps or Accessibility service is required",
      "text_zh": "需要“在其他应用上层显示”权限或无障碍服务",
      "source_location": "res/values/strings.xml: activity_launch_permission_required_and_missing_title（ManageDeviceFragment#D 引用 2131886133）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Next",
      "text_zh": "下一步",
      "source_location": "res/values/strings.xml: wiazrd_next（nc.i#d0 确认按钮 2131887264）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Cancel",
      "text_zh": "取消",
      "source_location": "res/values/strings.xml: generic_cancel（nc.i#d0 取消按钮 2131886531）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性安全降级：用户点 Cancel 仅关闭 PermissionInfoConfirmDialog；从系统设置返回后只按权限状态流刷新“not granted”标签，不自动重跳、无 onResume 死循环、无定时器拉起；仅当 startActivity 抛异常时 Toast(2131886521) 提示",
    "overlay_or_fake_settings": "无。全程使用 AppCompat 原生 AlertDialog + 真实系统设置页，未叠放半透明引导遮罩、未渲染高仿系统无障碍开关页",
    "restricted_settings_13plus_coaching": "无。DEX 中无 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也无“点右上角菜单允许受限设置”或 Session 安装器绕过文案；受限设置相关预筛线索（RESTRICTED_STR / SESSION_INSTALLER）在本应用的权限引导链路上未被使用",
    "post_grant_anti_removal": "无。未发现获权后自动点击确认、自动自授权，或监听设置页使用 GLOBAL_ACTION_BACK/HOME 阻止撤权；PERFORM_GLOBAL_ACTION 用于锁屏前返回桌面，与声明的无障碍用途一致",
    "benign_graceful_degradation": "具备：无障碍仅为可选权限项之一（与悬浮窗、使用情况访问、通知使用权、设备管理员并列），缺失时权限页仅显示提示与 Modify 按钮，应用继续可用；对话框提供 Cancel，跳转失败仅 Toast 提示，不阻断使用"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 的目标为 android.settings.ACCESSIBILITY_SETTINGS（来源 s9.e#z），或监测到 PermissionInfoConfirmDialog（标题“Accessibility service”、按钮“Next”/“Cancel”）被 add 到 FragmentManager 的瞬间拉起 UTG",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前原生说明对话框页",
        "page_identifier": "AppCompat AlertDialog，标题“Accessibility service”，正文以“This is used to \"press\" the home button before showing the lock screen”开头，按钮 Next / Cancel",
        "why_most_useful": "该对话框是唯一的获权前告知环节，可判定是否提供取消路径、文案是否与实际用途一致",
        "observable_utg_signals": ["存在“Cancel”可点击节点（可取消性）", "正文文本与 strings.xml manage_device_permission_accessibility_text 一致", "无图片/无伪造系统控件样式"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中 label=TimeLimit、描述为 Home 键/锁屏说明的服务条目",
        "why_most_useful": "核对系统列表中展示的服务名与描述是否与包内资源一致，排除空白/同形字伪装",
        "observable_utg_signals": ["条目文本“TimeLimit”", "描述文本与 manage_device_permission_accessibility_text 完全一致", "无空白名称或异常长名称"]
      },
      {
        "page_role": "权限管理页缺失提示区",
        "page_identifier": "ManageDeviceFragment 布局内 activityLaunchPermissionMissing 区块，文本“Draw over other Apps or Accessibility service is required”",
        "why_most_useful": "确认触发时机为功能页按需引导而非冷启动强制阻塞",
        "observable_utg_signals": ["页面栈是否由 MainActivity 内导航进入", "是否同时存在其他权限项（并列可选）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一未覆盖的是获权后 AccessibilityService 的运行期行为（锁屏前 performGlobalAction(HOME)），该行为已由 Manifest 与无障碍描述公开声明，不属隐藏载荷；本次未启动动态分析验证。"
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
    "s9.e#z",
    "nc.i#d0",
    "ab.d#onClick",
    "io.timelimit.android.ui.manage.device.manage.ManageDeviceFragment#D",
    "res/xml/accesibility.xml",
    "res/values/strings.xml (manage_device_permission_accessibility_text)"
  ]
}
```

</details>
