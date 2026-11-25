# BN_061__2580449196｜远程协助与跨设备互联 — Sefirah

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：134.7s

## 1. 一句话核心结论

- **核心申请方式**：在原生 Compose 引导页的权限清单中以“Shizuku 不可用时的剪贴板检测回退”透明说明无障碍服务，侧载安装时先弹受限设置六步教学对话框再跳应用详情/无障碍设置，无遮罩胁迫与拒绝循环
- **静态可见性说明**：无障碍服务配置、引导页 Compose 代码、点击分流逻辑与受限设置教学文案全部静态可见，无加壳、无加密载荷、无远端 HTML；仅确认按钮对应 lambda 的具体分支未逐行展开，按同类证据推定
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `25804491960a9ac3d56d75808df1ae892498cb2d7f1a5eb2f2806e5319af2d7f` |
| 包名 / 年份 | `com.castle.sefirah` / 2025-2026 |
| 家族 / 品类 | **远程协助与跨设备互联**（同池样本数：1） |
| 原始来源标识 | https://apt.izzysoft.de/fdroid/repo/com.castle.sefirah_38.apk |
| 桌面显示名 | Sefirah |
| 引导页宣称品牌/身份 | Sefirah（IzzyOnDroid 开源手机-桌面互联工具，真实品牌） |
| 系统无障碍列表服务名 | Sefirah（service 未声明 android:label，回落为 @string/app_name；无 android:description） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅有 R8 代码混淆（类名/合成 lambda）与合成 lambda 编号，不构成身份伪装；无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool |
| 无障碍服务类名 | `sefirah.clipboard.ClipboardAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | MainActivity（Compose 导航）→ onboarding 步骤 com.castle.sefirah.presentation.onboarding.PermissionStep | 首次启动进入 onboarding 权限步骤，PermissionStep.Content 组合渲染 | 原生Activity | **原文**：Accessibility Service / Fallback clipboard detection when Shizuku is unavailable<br>**译注**：无障碍服务 / Shizuku 不可用时的剪贴板检测回退方案 | 在权限清单中找到该条目并点击右侧 Grant 开关；页面底部有 Next/Finish，可跳过 | `PermissionStep.Content / PermissionStep$$ExternalSyntheticLambda15.invoke / PermissionStepKt.PermissionItem` |
| 2 | 业务功能触发 | PermissionItem 条目点击回调 | 用户点击无障碍权限项（Function0 = PermissionStep$$ExternalSyntheticLambda17 case 1） | 原生Dialog | **原文**：无（先执行渠道判定 isAppSideLoaded）<br>**译注**：先判断是否非 Play 商店安装 | 无（自动分支） | `PermissionStep$$ExternalSyntheticLambda17.invoke / PermissionStep.isAppSideLoaded` |
| 3 | 引导说明页 | Compose AlertDialog（PermissionRationaleDialog，restrictedSettings=2131755036 即 accessibility_service） | isAppSideLoaded 为 true（安装来源非 com.android.vending）时 setValue(PermissionRationaleDialog) | 原生Dialog | **原文**：Restricted settings — Due to security restrictions, you'll need to: 1. Try to enable the '%s' 2. Tap 'ok' on the warning and come back 3. Go to App Info 4. Open the overflow menu (3 dots) 5. Tap 'allow restricted settings' 6. Go back and try again to enable the '%s'<br>**译注**：受限设置 — 由于安全限制，你需要：1. 先尝试开启“%s”；2. 在警告上点“确定”后返回；3. 进入应用信息；4. 打开右上角三点菜单；5. 点“允许受限设置”；6. 返回并再次尝试开启“%s” | 按 6 步操作，或点取消/关闭放弃；对话框可关闭（AlertDialog 带 dismiss 回调） | `PermissionStep.Content（AlertDialog-Oix01E0 + AddressScreenKt$$ExternalSyntheticLambda9(3)）/ res/values/strings.xml restricted_settings_instruction` |
| 4 | 跳受限设置 | 系统“应用信息”页（android.settings.APPLICATION_DETAILS_SETTINGS） | 对话框确认按钮 → SMSHelper$$ExternalSyntheticLambda2（该 lambda 内含 APPLICATION_DETAILS_SETTINGS Intent） | 系统无障碍页 | **原文**：无（系统页面）<br>**译注**：跳转本应用详情页，供用户点右上角菜单“允许受限设置” | 在应用详情页菜单中允许受限设置后返回 | `sefirah.common.util.PermissionKt#openAppSettings / sefirah.communication.sms.SMSHelper$$ExternalSyntheticLambda2#invoke` |
| 5 | 跳无障碍设置 | 系统“无障碍”设置页（android.settings.ACCESSIBILITY_SETTINGS） | 再次点击无障碍权限项，且 isAppSideLoaded 为 false（Play 安装）时直接跳转；侧载用户在允许受限设置后重试进入该分支 | 系统无障碍页 | **原文**：无（系统页面，服务项显示名 Sefirah，无描述文案）<br>**译注**：系统无障碍服务列表中的 Sefirah 开关 | 在系统无障碍列表中找到 Sefirah 并手动开启 | `PermissionStep$$ExternalSyntheticLambda17.invoke（Intent "android.settings.ACCESSIBILITY_SETTINGS"）` |
| 6 | 拒权反馈循环 | 返回应用后的 PermissionStep 页面 | Lifecycle ON_RESUME → PermissionStepKt$$ExternalSyntheticLambda0（DisposableEffect 内刷新） | 原生Activity | **原文**：Accessibility Service（未获权时开关仍为关闭态）<br>**译注**：仅刷新权限状态，开关保持关闭，未自动重跳设置页 | 用户可再次点击或跳过该步骤 | `PermissionStepKt$$ExternalSyntheticLambda0 / PermissionStepKt.PermissionItem（hasRequestedPermission 判定）` |
| 7 | 获权后动作 | sefirah.clipboard.ClipboardAccessibilityService 作为剪贴板检测回退；Shizuku/ADB 为主路径 | 服务被系统绑定后按事件类型捕获剪贴板相关窗口变化 | 原生Activity | **原文**：Auto-detect clipboard changes on Android 10+ via Shizuku or desktop ADB.<br>**译注**：Android 10+ 通过 Shizuku 或桌面 ADB 自动检测剪贴板变化 | 无（获权后按剪贴板同步偏好工作） | `sefirah.clipboard.ClipboardAccessibilityService / res/xml/clipservice.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- onboarding 权限清单项标题与副标题：PermissionStep 中 PermissionItem 渲染的 accessibility_service / accessibility_service_rationale（strings.xml 第 13-14 行）
- 侧载安装时弹出的不可混淆的原生 Compose AlertDialog：restricted_settings_title + restricted_settings_instruction（strings.xml 第 197-204 行），含 6 步受限设置教学
- 系统无障碍设置页中的服务条目：仅显示应用名 Sefirah（service 未声明 label），无 android:description 说明文案（clipservice.xml 无 description 属性）
- 权限清单下方的分组标题文案（如 Device settings / Battery status 等，来自 strings.xml）
- Shizuku 权限项：shizuku_permission / shizuku_permission_rationale（strings.xml 第 216-217 行）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility Service | 无障碍服务 | `res/values/strings.xml key=accessibility_service` | 良性透明说明 |
| en | Fallback clipboard detection when Shizuku is unavailable | 当 Shizuku 不可用时的剪贴板检测回退方案 | `res/values/strings.xml key=accessibility_service_rationale` | 良性透明说明 |
| en | Restricted settings | 受限设置 | `res/values/strings.xml key=restricted_settings_title` | 受限设置分步教学 |
| en | Due to security restrictions, you'll need to: <br> 1. Try to enable the '%s' <br> 2. Tap 'ok' on the warning and come back <br> 3. Go to App Info <br> 4. Open the overflow menu (3 dots) <br> 5. Tap 'allow restricted settings' <br> 6. Go back and try again to enable the '%s' | 由于安全限制，你需要：1. 先尝试开启“%s”；2. 在警告上点“确定”后返回；3. 进入应用信息；4. 打开右上角三点菜单；5. 点“允许受限设置”；6. 返回并再次尝试开启“%s” | `res/values/strings.xml key=restricted_settings_instruction（PermissionStep.Content 的 AlertDialog）` | 受限设置分步教学 |
| en | Auto-detect clipboard changes on Android 10+ via Shizuku or desktop ADB. | 在 Android 10+ 上通过 Shizuku 或桌面 ADB 自动检测剪贴板变化 | `res/values/strings.xml key=clipboard_worker_subtitle` | 良性透明说明 |
| en | Used for clipboard auto-sync on Android 10+ | 用于 Android 10+ 上的剪贴板自动同步 | `res/values/strings.xml key=shizuku_permission_rationale` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无强制循环：返回应用后仅通过 Lifecycle 监听（PermissionStepKt$$ExternalSyntheticLambda0，DisposableEffect）刷新 permissionStates，开关保持关闭状态，用户可再次点击或跳过该 onboarding 步骤；未发现 Timer 定时拉起或 onResume 自动重跳 ACCESSIBILITY_SETTINGS
- **遮罩叠层 / 高仿系统设置页**：无。不使用 SYSTEM_ALERT_WINDOW 叠层遮罩引导无障碍，也无高仿系统无障碍开关页；引导均为标准 Material3 原生页面与 AlertDialog
- **Android 13+ 受限设置（Restricted Settings）应对**：有，且为显式教学：restricted_settings_instruction 明列 6 步（先触发警告→点确定→App Info→三点菜单→允许受限设置→返回重试），仅在 isAppSideLoaded() 判定为非 Play 商店安装时出现
- **获权后即时行为与防撤权机制**：无。未发现获权后自点确认、自授权、或利用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑
- **良性降级 / 替代方案**：有：剪贴板同步主路径为 Shizuku（moe.shizuku.privileged.api）或桌面 ADB，无障碍仅作回退；短信/通话/通知等权限项均为独立可选开关，未获权不影响应用其他功能

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 时拉起；侧载安装场景下应在 onboarding 页面点击无障碍项、PermissionRationaleDialog 弹出的瞬间先行截图（对话框先于跳转出现）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区；全部引导文案为原生文本可被 UTG 直接提取。唯一注意点是服务在系统列表无 android:description，若仅凭系统无障碍页取证会缺少“用途说明”证据，需回到应用内 onboarding 页取证

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **onboarding 权限清单页（含无障碍条目）** | Compose 页面标题含 Accessibility Service，副标题 Fallback clipboard detection when Shizuku is unavailable，条目右侧为 Grant/开关 | 确认引导是透明说明式清单而非恐吓/伪装，并核对是否有取消与跳过入口 | 标题与副标题文本；Grant 按钮与开关状态；Next/Finish 按钮存在性 |
| **受限设置六步教学 AlertDialog** | 对话框标题 Restricted settings，正文含 allow restricted settings 字样与编号 1-6 | 区分“合规教学”与“教唆绕过系统安全警告”，是最关键的判别页 | 对话框标题 Restricted settings；编号步骤文本；确定/取消按钮；是否仅有确认无取消 |
| **系统无障碍服务列表项** | Settings 页中 Sefirah 条目，无说明副标题 | 核对服务显示名与描述是否与页面宣称一致，是否存在空白挤出或伪造 isAccessibilityTool 标识 | 服务名 Sefirah；description 是否为空；是否存在异常换行/同形字 |
| **从系统设置返回后的应用页** | PermissionStep 页面，开关状态是否同步更新 | 确认拒权后是否出现重跳循环或遮罩压迫 | 返回后是否自动再跳设置；是否出现悬浮遮罩；开关状态与实际授权一致性 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.castle.sefirah.presentation.onboarding.PermissionStep#Content`
- `com.castle.sefirah.presentation.onboarding.PermissionStep$$ExternalSyntheticLambda17#invoke`
- `com.castle.sefirah.presentation.onboarding.PermissionStep#isAppSideLoaded`
- `com.castle.sefirah.presentation.onboarding.PermissionStepKt#PermissionItem`
- `res/values/strings.xml#L197-L204`
- `res/xml/clipservice.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**核心机制（静态可完整还原，无加壳）**

1. **无障碍服务本体**：[clipservice.xml](<resource-unit:#1 file:res/xml/clipservice.xml>) 声明的 `ClipboardAccessibilityService` 能力仅为事件监听（通知/点击/焦点/窗口内容变化 + `flagRetrieveInteractiveWindows`），Manifest 中该 service **无 `android:label`、无 `android:description`**，因此在系统无障碍列表里以应用名 `Sefirah` 呈现、无说明文案，属开源应用的常规“剪贴板回退”实现。
2. **引导入口是原生 Compose 引导页**：[PermissionStep.Content()](<resource-unit:#1.dex1 code:com.castle.sefirah.presentation.onboarding.PermissionStep#Content>) 在 onboarding 步骤里以 `ElevatedCard` + `PermissionItem` 逐项列出通知、联系人、短信、通话记录、悬浮窗、Shizuku、无障碍等权限项；无障碍项标题/副标题为 `Accessibility Service` / `Fallback clipboard detection when Shizuku is unavailable`（[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L13-L14>)），并在系统无障碍页里无描述。
3. **点击行为按安装渠道分流**：[PermissionStep$$ExternalSyntheticLambda17.invoke()](<resource-unit:#1.dex1 code:com.castle.sefirah.presentation.onboarding.PermissionStep$$ExternalSyntheticLambda17#invoke>) 的 accessibility 分支先调用 `isAppSideLoaded()`（[isAppSideLoaded()](<resource-unit:#1.dex1 code:com.castle.sefirah.presentation.onboarding.PermissionStep#isAppSideLoaded>)，判断安装来源是否 `com.android.vending`）。**非商店安装（侧载）时先弹说明对话框**（`PermissionRationaleDialog(2131755036, …)`），**否则直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`**。
4. **受限设置分步教学**：该对话框内容来自 [strings.xml 的 restricted_settings_instruction](<resource-unit:#1 file:res/values/strings.xml#L197-L203>)，明写“先点开启→在警告上点 ok 返回→进入 App Info→右上角三点→允许受限设置→再回来开启”，确认后经 `SMSHelper$$ExternalSyntheticLambda2` 打开 `APPLICATION_DETAILS_SETTINGS`（该 lambda 中同时存在该 Intent，属同一流程的确认跳转）。
5. **无诱导/胁迫特征**：无 `SYSTEM_ALERT_WINDOW` 叠层遮罩引导无障碍、无 `GLOBAL_ACTION_BACK/HOME` 撤权对抗、无 onResume 死循环重跳（仅在 `DisposableEffect(Lifecycle)` 中刷新 `permissionStates` 状态）、无伪造 `isAccessibilityTool`、无 WebView/远端 HTML 文案、无应用变脸与品牌伪装；`SYSTEM_ALERT_WINDOW` 仅用于权限列表项与业务悬浮展示。
6. **存在良性替代路径**：Shizuku / 桌面 ADB 检测剪贴板（`clipboard_worker_subtitle`、`shizuku_permission_rationale`），无障碍仅作回退。

**判定**：该应用属于“受限设置分步教学 + 透明说明”的良性引导，未发现诱导性无障碍权限滥用；全部引导文案与跳转逻辑均静态可见。

**覆盖边界**：确认按钮打开 `APPLICATION_DETAILS_SETTINGS` 的具体 lambda 分支、onboarding 步骤是否可跳过、`PermissionItem` 内二次 rationale 弹层的完整渲染逻辑未逐行展开（受 14 次调用上限约束，按同一类内证据推定）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍服务配置、引导页 Compose 代码、点击分流逻辑与受限设置教学文案全部静态可见，无加壳、无加密载荷、无远端 HTML；仅确认按钮对应 lambda 的具体分支未逐行展开，按同类证据推定",
  "summary_one_liner": "在原生 Compose 引导页的权限清单中以“Shizuku 不可用时的剪贴板检测回退”透明说明无障碍服务，侧载安装时先弹受限设置六步教学对话框再跳应用详情/无障碍设置，无遮罩胁迫与拒绝循环",
  "disguise_identity": {
    "app_display_name": "Sefirah",
    "claimed_brand_or_persona": "Sefirah（IzzyOnDroid 开源手机-桌面互联工具，真实品牌）",
    "a11y_service_label": "Sefirah（service 未声明 android:label，回落为 @string/app_name；无 android:description）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅有 R8 代码混淆（类名/合成 lambda）与合成 lambda 编号，不构成身份伪装；无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "MainActivity（Compose 导航）→ onboarding 步骤 com.castle.sefirah.presentation.onboarding.PermissionStep",
      "trigger_event": "首次启动进入 onboarding 权限步骤，PermissionStep.Content 组合渲染",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility Service / Fallback clipboard detection when Shizuku is unavailable",
      "shown_text_zh": "无障碍服务 / Shizuku 不可用时的剪贴板检测回退方案",
      "user_action_requested": "在权限清单中找到该条目并点击右侧 Grant 开关；页面底部有 Next/Finish，可跳过",
      "code_anchor": "PermissionStep.Content / PermissionStep$$ExternalSyntheticLambda15.invoke / PermissionStepKt.PermissionItem"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "PermissionItem 条目点击回调",
      "trigger_event": "用户点击无障碍权限项（Function0 = PermissionStep$$ExternalSyntheticLambda17 case 1）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无（先执行渠道判定 isAppSideLoaded）",
      "shown_text_zh": "先判断是否非 Play 商店安装",
      "user_action_requested": "无（自动分支）",
      "code_anchor": "PermissionStep$$ExternalSyntheticLambda17.invoke / PermissionStep.isAppSideLoaded"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "Compose AlertDialog（PermissionRationaleDialog，restrictedSettings=2131755036 即 accessibility_service）",
      "trigger_event": "isAppSideLoaded 为 true（安装来源非 com.android.vending）时 setValue(PermissionRationaleDialog)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Restricted settings — Due to security restrictions, you'll need to: 1. Try to enable the '%s' 2. Tap 'ok' on the warning and come back 3. Go to App Info 4. Open the overflow menu (3 dots) 5. Tap 'allow restricted settings' 6. Go back and try again to enable the '%s'",
      "shown_text_zh": "受限设置 — 由于安全限制，你需要：1. 先尝试开启“%s”；2. 在警告上点“确定”后返回；3. 进入应用信息；4. 打开右上角三点菜单；5. 点“允许受限设置”；6. 返回并再次尝试开启“%s”",
      "user_action_requested": "按 6 步操作，或点取消/关闭放弃；对话框可关闭（AlertDialog 带 dismiss 回调）",
      "code_anchor": "PermissionStep.Content（AlertDialog-Oix01E0 + AddressScreenKt$$ExternalSyntheticLambda9(3)）/ res/values/strings.xml restricted_settings_instruction"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统“应用信息”页（android.settings.APPLICATION_DETAILS_SETTINGS）",
      "trigger_event": "对话框确认按钮 → SMSHelper$$ExternalSyntheticLambda2（该 lambda 内含 APPLICATION_DETAILS_SETTINGS Intent）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页面）",
      "shown_text_zh": "跳转本应用详情页，供用户点右上角菜单“允许受限设置”",
      "user_action_requested": "在应用详情页菜单中允许受限设置后返回",
      "code_anchor": "sefirah.common.util.PermissionKt#openAppSettings / sefirah.communication.sms.SMSHelper$$ExternalSyntheticLambda2#invoke"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统“无障碍”设置页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "再次点击无障碍权限项，且 isAppSideLoaded 为 false（Play 安装）时直接跳转；侧载用户在允许受限设置后重试进入该分支",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页面，服务项显示名 Sefirah，无描述文案）",
      "shown_text_zh": "系统无障碍服务列表中的 Sefirah 开关",
      "user_action_requested": "在系统无障碍列表中找到 Sefirah 并手动开启",
      "code_anchor": "PermissionStep$$ExternalSyntheticLambda17.invoke（Intent \"android.settings.ACCESSIBILITY_SETTINGS\"）"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回应用后的 PermissionStep 页面",
      "trigger_event": "Lifecycle ON_RESUME → PermissionStepKt$$ExternalSyntheticLambda0（DisposableEffect 内刷新）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility Service（未获权时开关仍为关闭态）",
      "shown_text_zh": "仅刷新权限状态，开关保持关闭，未自动重跳设置页",
      "user_action_requested": "用户可再次点击或跳过该步骤",
      "code_anchor": "PermissionStepKt$$ExternalSyntheticLambda0 / PermissionStepKt.PermissionItem（hasRequestedPermission 判定）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "sefirah.clipboard.ClipboardAccessibilityService 作为剪贴板检测回退；Shizuku/ADB 为主路径",
      "trigger_event": "服务被系统绑定后按事件类型捕获剪贴板相关窗口变化",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Auto-detect clipboard changes on Android 10+ via Shizuku or desktop ADB.",
      "shown_text_zh": "Android 10+ 通过 Shizuku 或桌面 ADB 自动检测剪贴板变化",
      "user_action_requested": "无（获权后按剪贴板同步偏好工作）",
      "code_anchor": "sefirah.clipboard.ClipboardAccessibilityService / res/xml/clipservice.xml"
    }
  ],
  "text_presentation_locations": [
    "onboarding 权限清单项标题与副标题：PermissionStep 中 PermissionItem 渲染的 accessibility_service / accessibility_service_rationale（strings.xml 第 13-14 行）",
    "侧载安装时弹出的不可混淆的原生 Compose AlertDialog：restricted_settings_title + restricted_settings_instruction（strings.xml 第 197-204 行），含 6 步受限设置教学",
    "系统无障碍设置页中的服务条目：仅显示应用名 Sefirah（service 未声明 label），无 android:description 说明文案（clipservice.xml 无 description 属性）",
    "权限清单下方的分组标题文案（如 Device settings / Battery status 等，来自 strings.xml）",
    "Shizuku 权限项：shizuku_permission / shizuku_permission_rationale（strings.xml 第 216-217 行）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility Service",
      "text_zh": "无障碍服务",
      "source_location": "res/values/strings.xml key=accessibility_service",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Fallback clipboard detection when Shizuku is unavailable",
      "text_zh": "当 Shizuku 不可用时的剪贴板检测回退方案",
      "source_location": "res/values/strings.xml key=accessibility_service_rationale",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Restricted settings",
      "text_zh": "受限设置",
      "source_location": "res/values/strings.xml key=restricted_settings_title",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Due to security restrictions, you'll need to: \n 1. Try to enable the '%s' \n 2. Tap 'ok' on the warning and come back \n 3. Go to App Info \n 4. Open the overflow menu (3 dots) \n 5. Tap 'allow restricted settings' \n 6. Go back and try again to enable the '%s'",
      "text_zh": "由于安全限制，你需要：1. 先尝试开启“%s”；2. 在警告上点“确定”后返回；3. 进入应用信息；4. 打开右上角三点菜单；5. 点“允许受限设置”；6. 返回并再次尝试开启“%s”",
      "source_location": "res/values/strings.xml key=restricted_settings_instruction（PermissionStep.Content 的 AlertDialog）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Auto-detect clipboard changes on Android 10+ via Shizuku or desktop ADB.",
      "text_zh": "在 Android 10+ 上通过 Shizuku 或桌面 ADB 自动检测剪贴板变化",
      "source_location": "res/values/strings.xml key=clipboard_worker_subtitle",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Used for clipboard auto-sync on Android 10+",
      "text_zh": "用于 Android 10+ 上的剪贴板自动同步",
      "source_location": "res/values/strings.xml key=shizuku_permission_rationale",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无强制循环：返回应用后仅通过 Lifecycle 监听（PermissionStepKt$$ExternalSyntheticLambda0，DisposableEffect）刷新 permissionStates，开关保持关闭状态，用户可再次点击或跳过该 onboarding 步骤；未发现 Timer 定时拉起或 onResume 自动重跳 ACCESSIBILITY_SETTINGS",
    "overlay_or_fake_settings": "无。不使用 SYSTEM_ALERT_WINDOW 叠层遮罩引导无障碍，也无高仿系统无障碍开关页；引导均为标准 Material3 原生页面与 AlertDialog",
    "restricted_settings_13plus_coaching": "有，且为显式教学：restricted_settings_instruction 明列 6 步（先触发警告→点确定→App Info→三点菜单→允许受限设置→返回重试），仅在 isAppSideLoaded() 判定为非 Play 商店安装时出现",
    "post_grant_anti_removal": "无。未发现获权后自点确认、自授权、或利用 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑",
    "benign_graceful_degradation": "有：剪贴板同步主路径为 Shizuku（moe.shizuku.privileged.api）或桌面 ADB，无障碍仅作回退；短信/通话/通知等权限项均为独立可选开关，未获权不影响应用其他功能"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity 的 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 时拉起；侧载安装场景下应在 onboarding 页面点击无障碍项、PermissionRationaleDialog 弹出的瞬间先行截图（对话框先于跳转出现）",
    "key_pages_to_capture": [
      {
        "page_role": "onboarding 权限清单页（含无障碍条目）",
        "page_identifier": "Compose 页面标题含 Accessibility Service，副标题 Fallback clipboard detection when Shizuku is unavailable，条目右侧为 Grant/开关",
        "why_most_useful": "确认引导是透明说明式清单而非恐吓/伪装，并核对是否有取消与跳过入口",
        "observable_utg_signals": ["标题与副标题文本", "Grant 按钮与开关状态", "Next/Finish 按钮存在性"]
      },
      {
        "page_role": "受限设置六步教学 AlertDialog",
        "page_identifier": "对话框标题 Restricted settings，正文含 allow restricted settings 字样与编号 1-6",
        "why_most_useful": "区分“合规教学”与“教唆绕过系统安全警告”，是最关键的判别页",
        "observable_utg_signals": ["对话框标题 Restricted settings", "编号步骤文本", "确定/取消按钮", "是否仅有确认无取消"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 页中 Sefirah 条目，无说明副标题",
        "why_most_useful": "核对服务显示名与描述是否与页面宣称一致，是否存在空白挤出或伪造 isAccessibilityTool 标识",
        "observable_utg_signals": ["服务名 Sefirah", "description 是否为空", "是否存在异常换行/同形字"]
      },
      {
        "page_role": "从系统设置返回后的应用页",
        "page_identifier": "PermissionStep 页面，开关状态是否同步更新",
        "why_most_useful": "确认拒权后是否出现重跳循环或遮罩压迫",
        "observable_utg_signals": ["返回后是否自动再跳设置", "是否出现悬浮遮罩", "开关状态与实际授权一致性"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区；全部引导文案为原生文本可被 UTG 直接提取。唯一注意点是服务在系统列表无 android:description，若仅凭系统无障碍页取证会缺少“用途说明”证据，需回到应用内 onboarding 页取证"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.castle.sefirah.presentation.onboarding.PermissionStep#Content",
    "com.castle.sefirah.presentation.onboarding.PermissionStep$$ExternalSyntheticLambda17#invoke",
    "com.castle.sefirah.presentation.onboarding.PermissionStep#isAppSideLoaded",
    "com.castle.sefirah.presentation.onboarding.PermissionStepKt#PermissionItem",
    "res/values/strings.xml#L197-L204",
    "res/xml/clipservice.xml"
  ]
}
```

</details>
