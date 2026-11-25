# BN_039__565b571848｜极简桌面与双击锁屏 — KISS launcher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：155.0s

## 1. 一句话核心结论

- **核心申请方式**：KISS Launcher 仅在用户主动开启『双击锁屏』后于桌面双击时弹出带取消按钮的原生说明弹窗，以诚实文案说明无障碍 API 用途与不采集数据，点击 OK 才跳转系统无障碍设置页；服务本身只执行一次锁屏动作，事件回调为空。
- **静态可见性说明**：全链路静态可见：无障碍服务实现、服务配置 XML、引导弹窗构建代码、跳转 Intent、文案字符串均在 DEX 与 res 中直接还原，无加壳、无 AES 密文、无远端 HTML、无动态加载载荷。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `565b571848a3bfd9a356db98e9e6b26d9fdac7fa2ee8f46923f0396429418bdc` |
| 包名 / 年份 | `fr.neamar.kiss` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/fr.neamar.kiss_228.apk |
| 桌面显示名 | KISS launcher |
| 引导页宣称品牌/身份 | KISS Launcher（F-Droid 开源极简桌面，真实身份，无伪装） |
| 系统无障碍列表服务名 | KISS launcher（系统列表项标题取 android:label=@string/app_name，描述为 'Lock screen from KISS Launcher'） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未使用空白/换行挤出警告、同形字、多 activity-alias，也未伪造 isAccessibilityTool；服务名与描述均直白指向锁屏用途。 |
| 无障碍服务类名 | `fr.neamar.kiss.utils.LockAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS` |
| 系统设置项说明 (`android:description`) | Lock screen from KISS Launcher |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | SettingsActivity 内的『双击锁屏』偏好开关（SharedPreferences key = "double-tap"） | 用户在设置页手动打开该开关（写入 prefs 布尔值 double-tap=true） | 原生Activity | **原文**：无（开关项标题/摘要取自本地 strings 资源）<br>**译注**：用户在设置中自行开启『双击锁屏』功能开关 | 用户主动点击开关；不开启则该功能与无障碍引导完全不出现 | `fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap / onSingleTapUp（读取 getBoolean("double-tap", false)）` |
| 2 | 业务功能触发 | MainActivity 桌面空白区手势检测（GestureDetector，ExperienceTweaks$1） | 用户在桌面空白处双击（onDoubleTap）且 SDK_INT>=28 且 double-tap 开关已开 | 原生Activity | 无 | 无（系统状态自检：AccessibilityManager.getEnabledAccessibilityServiceList 中查找 fr.neamar.kiss.utils.LockAccessibilityService） | `fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap` |
| 3 | 引导说明页 | MaterialAlertDialogBuilder 构建的原生 AlertDialog（MainActivity 之上） | 步骤 2 自检发现本包无障碍服务未启用时，同步构建并 show() | 原生Dialog | **原文**：Double-tap to lock needs the Android Accessibility API. No data is processed, no data is stored. To use this feature, enable KISS in the following screen.<br>**译注**：双击锁屏需要 Android 无障碍 API。不会处理任何数据，也不会存储任何数据。要使用该功能，请在接下来的界面中启用 KISS。 | 提供 OK 与 Cancel 两个按钮；点 Cancel 直接关闭弹窗、功能保持未生效，不重试、不循环 | `res/values/strings.xml#L83 (enable_double_tap_to_lock, id 0x7f110067) / ExperienceTweaks$1.onDoubleTap` |
| 4 | 跳无障碍设置 | 系统『设置 → 无障碍 → 已下载的服务』列表（android.settings.ACCESSIBILITY_SETTINGS） | 用户点击弹窗 OK，触发 DialogInterface.OnClickListener（R8 classId=0 分支） | 系统无障碍页 | **原文**：Lock screen from KISS Launcher（系统列表项描述，android:description=@string/lock_service_description）<br>**译注**：系统无障碍列表中显示名为 KISS launcher、说明为『从 KISS Launcher 锁屏』的服务项，由用户自行决定是否开启 | 用户自行在系统页打开开关；应用不做任何自动勾选、无悬浮层指引、无高仿系统开关页 | `fr.neamar.kiss.forwarder.ExperienceTweaks$1$$ExternalSyntheticLambda0.onClick（new Intent("android.settings.ACCESSIBILITY_SETTINGS") + FLAG_ACTIVITY_NEW_TASK + startActivity）` |
| 5 | 获权后动作 | LockAccessibilityService（被 startService 唤起）→ 系统锁屏 | 用户在系统页开启服务后，返回桌面再次双击；onDoubleTap 自检通过 → startService(Intent action="fr.neamar.kiss.LOCK") | 系统无障碍页 | 无 | 无 | `fr.neamar.kiss.utils.LockAccessibilityService.onStartCommand` |
| 6 | 拒权反馈循环 | 从系统无障碍设置返回 MainActivity（onResume） | 用户未开启服务直接返回桌面 | 原生Activity | 无 | 无强制动作（良性降级） | `fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap（无 onResume/Timer 重跳逻辑）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 之上由 MaterialAlertDialogBuilder 构建的原生 AlertDialog，正文为 res/values/strings.xml 的 enable_double_tap_to_lock，带 OK / Cancel 两个按钮（可取消）
- 系统无障碍服务列表项：标题取 android:label=@string/app_name（KISS launcher），描述取 @string/lock_service_description（Lock screen from KISS Launcher），由 res/xml/lock_accessibility_service_config.xml 声明
- 设置搜索结果列表：SearchProvider.reload 中生成的跳转项，指向 android.settings.ACCESSIBILITY_SETTINGS（用户主动搜索才会看到）
- 设置页『双击锁屏』偏好开关本身（SharedPreferences key = double-tap）的标题与摘要，取自本地 strings 资源
- 未使用 WebView / HTML / 悬浮窗 Overlay / 通知栏 / 引导 GIF 图片承载说明文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Double-tap to lock needs the Android Accessibility API. No data is processed, no data is stored. To use this feature, enable KISS in the following screen. | 双击锁屏需要 Android 无障碍 API。不会处理任何数据，也不会存储任何数据。要使用该功能，请在接下来的界面中启用 KISS。 | `res/values/strings.xml#L83 key=enable_double_tap_to_lock（另见 res/values-en-rGB/strings.xml#L82），由 fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap 引用资源 id 2131820647` | 良性透明说明 |
| en | Lock screen from KISS Launcher | 从 KISS Launcher 锁屏 | `res/xml/lock_accessibility_service_config.xml 中 android:description=@string/lock_service_description（系统无障碍列表项描述）` | 良性透明说明 |
| en | OK | 确定 | `R$string.ok，ExperienceTweaks$1.onDoubleTap setPositiveButton → 跳转 android.settings.ACCESSIBILITY_SETTINGS` | 受限设置分步教学 |
| en | Cancel | 取消 | `R$string.cancel，ExperienceTweaks$1.onDoubleTap setNegativeButton → 仅关闭弹窗，无后续强制` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无拒绝循环。从系统无障碍设置返回后不重跳、不弹二次提示、无 Timer 轮询拉起；只有在用户下一次在桌面空白处双击且服务仍未启用时，才会再次显示同一个可取消的说明弹窗。
- **遮罩叠层 / 高仿系统设置页**：无。既无半透明引导遮罩、无全屏悬浮窗，也无高仿系统无障碍开关页；跳转目标为系统原生 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现引导进入应用详情点右上角菜单允许『受限设置』的文案或代码，也未使用 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。获权后未自点确认、未自授权，未监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权；performGlobalAction(8) 仅对应 GLOBAL_ACTION_LOCK_SCREEN，用于正常锁屏功能。
- **良性降级 / 替代方案**：良性降级明确：不开启无障碍时应用全部桌面功能照常可用，仅『双击锁屏』不生效；弹窗可点 Cancel 关闭，用户也可在设置中关掉 double-tap 开关彻底停止该引导。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条等价触发点：①在设置中开启 double-tap 后于桌面空白处双击，捕获随即 show() 的 MaterialAlertDialog（弹窗出现到点 OK 之间有充分停留时间）；②直接监测 startActivity 到 android.settings.ACCESSIBILITY_SETTINGS 的瞬间，验证跳转前是否仅有一层可取消的原生弹窗、无遮罩叠层。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。说明文字全部为本地 strings 文本，无图片引导、无空文本图形诱饵、无远端 HTML、无第一阶段 Dropper、无加壳；纯 UTG 文本提取即可完整判别。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **业务触发后的引导弹窗页** | MainActivity 上覆盖的 AlertDialog，正文含 'Double-tap to lock needs the Android Accessibility API'，按钮为 OK / Cancel | 这是全流程唯一的信息披露面，直接决定是否存在恐吓、伪装或隐私误导；同时可验证 Cancel 是否真实可用（无跳过则属强制） | 弹窗文本与 strings 资源一致且为透明说明；存在可点击的 Cancel 按钮；无倒计时、无遮罩、无二次弹窗叠加；弹窗层级为 Dialog 而非全屏 Overlay |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务中的 'KISS launcher' 项，摘要 'Lock screen from KISS Launcher' | 验证服务名/描述是否与真实身份一致，是否通过空白、同形字或伪造 isAccessibilityTool 隐藏真实用途 | 服务标题为真实应用名 KISS launcher；描述明示锁屏用途；不存在同名重复服务项或多 alias 条目 |
| **从系统设置返回后的桌面页** | MainActivity 桌面（无障碍服务仍关闭） | 验证拒权后是否死循环重跳或强制阻断使用，区分按需引导与胁迫式引导 | 返回后无弹窗重跳；桌面正常可用、可继续搜索与启动应用；再次双击才重新出现同一可取消弹窗 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap`
- `fr.neamar.kiss.forwarder.ExperienceTweaks$1$$ExternalSyntheticLambda0.onClick`
- `fr.neamar.kiss.utils.LockAccessibilityService.onStartCommand`
- `res/xml/lock_accessibility_service_config.xml`
- `res/values/strings.xml#L83（enable_double_tap_to_lock）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（KISS Launcher 无障碍权限引导路径）

**整体判断：良性、透明、按需触发，未发现诱导、强制或隐蔽手法。** 静态完全可见，无加壳、无密文载荷、无远端 HTML。

1. **无障碍服务本身极小且中性**：[LockAccessibilityService](<resource-unit:#1.dex1 code:fr.neamar.kiss.utils.LockAccessibilityService>) 仅覆写 `onStartCommand`，校验 action 为 `fr.neamar.kiss.LOCK` 且 `SDK_INT >= 28` 后调用 `performGlobalAction(8)`（GLOBAL_ACTION_LOCK_SCREEN）；[onAccessibilityEvent](<resource-unit:#1.dex1 code:fr.neamar.kiss.utils.LockAccessibilityService#onAccessibilityEvent>) 与 `onInterrupt` 均为空实现——**不读取任何界面内容**。预筛中 `PERFORM_GLOBAL_ACTION / WATCH_SETTINGS` 的“反移除”命中实为锁屏动作，未用于拦截撤权。
2. **配置声明透明**：[lock_accessibility_service_config.xml](<resource-unit:#1 file:res/xml/lock_accessibility_service_config.xml#L1-L3>) 仅声明 `description=@string/lock_service_description`（"Lock screen from KISS Launcher"）与 `settingsActivity=SettingsActivity`，未设 `canRetrieveWindowContent`、未设 `isAccessibilityTool=false` 伪装、无 `packageNames` 收敛以外的花招。
3. **引导仅在用户主动开启功能后按需出现**：用户在设置里打开 `double-tap` 开关后，在桌面空白处双击触发 [ExperienceTweaks$1.onDoubleTap](<resource-unit:#1.dex1 code:fr.neamar.kiss.forwarder.ExperienceTweaks$1#onDoubleTap>)；通过 `AccessibilityManager.getEnabledAccessibilityServiceList` 自检本包服务是否已启用。已启用则直接 `startService(fr.neamar.kiss.LOCK)` 锁屏；未启用则弹出 MaterialAlertDialog 说明。
4. **弹窗文案为诚实的隐私承诺 + 分步教学**，且带**明确的取消按钮**：`enable_double_tap_to_lock`（[strings.xml:83](<resource-unit:#1 file:res/values/strings.xml#L83>)）：“Double-tap to lock needs the Android Accessibility API. No data is processed, no data is stored. To use this feature, enable KISS in the following screen.” 点“OK”后由 [Lambda0.onClick](<resource-unit:#1.dex1 code:fr.neamar.kiss.forwarder.ExperienceTweaks$1$$ExternalSyntheticLambda0#onClick>) 构造 `android.settings.ACCESSIBILITY_SETTINGS` 跳转系统无障碍列表；点“Cancel”仅关闭。
5. **无拒绝反馈循环、无遮罩、无高仿开关页、无 13+ 受限设置教学、无 GLOBAL_ACTION_BACK 阻断撤权**：从系统设置返回后不重跳，只有用户再次双击才会重新弹窗；关闭 `double-tap` 开关即完全回到无该功能的普通桌面（良性降级）。
6. 另有 [SearchProvider.reload](<resource-unit:#1.dex1 code:fr.neamar.kiss.dataprovider.simpleprovider.SearchProvider#reload>) 在设置搜索结果中直接提供 `android.settings.ACCESSIBILITY_SETTINGS` 条目，属用户主动搜索进入的常规设置入口。

**覆盖边界**：本次未运行动态分析（无在线设备需求且静态证据已闭环）；`double-tap` 开关所在的设置 Preference 具体布局文件未逐一定位（仅确认其 key 为 `double-tap`，由 ExperienceTweaks 侧读取）。未登记风险——证据不支持任何恶意/违规命题。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全链路静态可见：无障碍服务实现、服务配置 XML、引导弹窗构建代码、跳转 Intent、文案字符串均在 DEX 与 res 中直接还原，无加壳、无 AES 密文、无远端 HTML、无动态加载载荷。",
  "summary_one_liner": "KISS Launcher 仅在用户主动开启『双击锁屏』后于桌面双击时弹出带取消按钮的原生说明弹窗，以诚实文案说明无障碍 API 用途与不采集数据，点击 OK 才跳转系统无障碍设置页；服务本身只执行一次锁屏动作，事件回调为空。",
  "disguise_identity": {
    "app_display_name": "KISS launcher",
    "claimed_brand_or_persona": "KISS Launcher（F-Droid 开源极简桌面，真实身份，无伪装）",
    "a11y_service_label": "KISS launcher（系统列表项标题取 android:label=@string/app_name，描述为 'Lock screen from KISS Launcher'）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未使用空白/换行挤出警告、同形字、多 activity-alias，也未伪造 isAccessibilityTool；服务名与描述均直白指向锁屏用途。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "SettingsActivity 内的『双击锁屏』偏好开关（SharedPreferences key = \"double-tap\"）",
      "trigger_event": "用户在设置页手动打开该开关（写入 prefs 布尔值 double-tap=true）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（开关项标题/摘要取自本地 strings 资源）",
      "shown_text_zh": "用户在设置中自行开启『双击锁屏』功能开关",
      "user_action_requested": "用户主动点击开关；不开启则该功能与无障碍引导完全不出现",
      "code_anchor": "fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap / onSingleTapUp（读取 getBoolean(\"double-tap\", false)）"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity 桌面空白区手势检测（GestureDetector，ExperienceTweaks$1）",
      "trigger_event": "用户在桌面空白处双击（onDoubleTap）且 SDK_INT>=28 且 double-tap 开关已开",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "桌面双击被识别为『锁屏』意图，随即自检本包无障碍服务是否已启用",
      "user_action_requested": "无（系统状态自检：AccessibilityManager.getEnabledAccessibilityServiceList 中查找 fr.neamar.kiss.utils.LockAccessibilityService）",
      "code_anchor": "fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "MaterialAlertDialogBuilder 构建的原生 AlertDialog（MainActivity 之上）",
      "trigger_event": "步骤 2 自检发现本包无障碍服务未启用时，同步构建并 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Double-tap to lock needs the Android Accessibility API. No data is processed, no data is stored. To use this feature, enable KISS in the following screen.",
      "shown_text_zh": "双击锁屏需要 Android 无障碍 API。不会处理任何数据，也不会存储任何数据。要使用该功能，请在接下来的界面中启用 KISS。",
      "user_action_requested": "提供 OK 与 Cancel 两个按钮；点 Cancel 直接关闭弹窗、功能保持未生效，不重试、不循环",
      "code_anchor": "res/values/strings.xml#L83 (enable_double_tap_to_lock, id 0x7f110067) / ExperienceTweaks$1.onDoubleTap"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统『设置 → 无障碍 → 已下载的服务』列表（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "用户点击弹窗 OK，触发 DialogInterface.OnClickListener（R8 classId=0 分支）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Lock screen from KISS Launcher（系统列表项描述，android:description=@string/lock_service_description）",
      "shown_text_zh": "系统无障碍列表中显示名为 KISS launcher、说明为『从 KISS Launcher 锁屏』的服务项，由用户自行决定是否开启",
      "user_action_requested": "用户自行在系统页打开开关；应用不做任何自动勾选、无悬浮层指引、无高仿系统开关页",
      "code_anchor": "fr.neamar.kiss.forwarder.ExperienceTweaks$1$$ExternalSyntheticLambda0.onClick（new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + FLAG_ACTIVITY_NEW_TASK + startActivity）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "LockAccessibilityService（被 startService 唤起）→ 系统锁屏",
      "trigger_event": "用户在系统页开启服务后，返回桌面再次双击；onDoubleTap 自检通过 → startService(Intent action=\"fr.neamar.kiss.LOCK\")",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务收到 LOCK action 后调用 performGlobalAction(8) 即 GLOBAL_ACTION_LOCK_SCREEN，设备锁屏；不采集界面内容、不修改系统设置",
      "user_action_requested": "无",
      "code_anchor": "fr.neamar.kiss.utils.LockAccessibilityService.onStartCommand"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "从系统无障碍设置返回 MainActivity（onResume）",
      "trigger_event": "用户未开启服务直接返回桌面",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "返回后不弹窗、不重跳、不提示；仅当用户下次再双击时才会重新出现同一说明弹窗，可随时点 Cancel 或关闭 double-tap 开关彻底退出该路径",
      "user_action_requested": "无强制动作（良性降级）",
      "code_anchor": "fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap（无 onResume/Timer 重跳逻辑）"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 之上由 MaterialAlertDialogBuilder 构建的原生 AlertDialog，正文为 res/values/strings.xml 的 enable_double_tap_to_lock，带 OK / Cancel 两个按钮（可取消）",
    "系统无障碍服务列表项：标题取 android:label=@string/app_name（KISS launcher），描述取 @string/lock_service_description（Lock screen from KISS Launcher），由 res/xml/lock_accessibility_service_config.xml 声明",
    "设置搜索结果列表：SearchProvider.reload 中生成的跳转项，指向 android.settings.ACCESSIBILITY_SETTINGS（用户主动搜索才会看到）",
    "设置页『双击锁屏』偏好开关本身（SharedPreferences key = double-tap）的标题与摘要，取自本地 strings 资源",
    "未使用 WebView / HTML / 悬浮窗 Overlay / 通知栏 / 引导 GIF 图片承载说明文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Double-tap to lock needs the Android Accessibility API. No data is processed, no data is stored. To use this feature, enable KISS in the following screen.",
      "text_zh": "双击锁屏需要 Android 无障碍 API。不会处理任何数据，也不会存储任何数据。要使用该功能，请在接下来的界面中启用 KISS。",
      "source_location": "res/values/strings.xml#L83 key=enable_double_tap_to_lock（另见 res/values-en-rGB/strings.xml#L82），由 fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap 引用资源 id 2131820647",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Lock screen from KISS Launcher",
      "text_zh": "从 KISS Launcher 锁屏",
      "source_location": "res/xml/lock_accessibility_service_config.xml 中 android:description=@string/lock_service_description（系统无障碍列表项描述）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "OK",
      "text_zh": "确定",
      "source_location": "R$string.ok，ExperienceTweaks$1.onDoubleTap setPositiveButton → 跳转 android.settings.ACCESSIBILITY_SETTINGS",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Cancel",
      "text_zh": "取消",
      "source_location": "R$string.cancel，ExperienceTweaks$1.onDoubleTap setNegativeButton → 仅关闭弹窗，无后续强制",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无拒绝循环。从系统无障碍设置返回后不重跳、不弹二次提示、无 Timer 轮询拉起；只有在用户下一次在桌面空白处双击且服务仍未启用时，才会再次显示同一个可取消的说明弹窗。",
    "overlay_or_fake_settings": "无。既无半透明引导遮罩、无全屏悬浮窗，也无高仿系统无障碍开关页；跳转目标为系统原生 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无。未出现引导进入应用详情点右上角菜单允许『受限设置』的文案或代码，也未使用 Session 安装器绕过。",
    "post_grant_anti_removal": "无。获权后未自点确认、未自授权，未监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权；performGlobalAction(8) 仅对应 GLOBAL_ACTION_LOCK_SCREEN，用于正常锁屏功能。",
    "benign_graceful_degradation": "良性降级明确：不开启无障碍时应用全部桌面功能照常可用，仅『双击锁屏』不生效；弹窗可点 Cancel 关闭，用户也可在设置中关掉 double-tap 开关彻底停止该引导。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条等价触发点：①在设置中开启 double-tap 后于桌面空白处双击，捕获随即 show() 的 MaterialAlertDialog（弹窗出现到点 OK 之间有充分停留时间）；②直接监测 startActivity 到 android.settings.ACCESSIBILITY_SETTINGS 的瞬间，验证跳转前是否仅有一层可取消的原生弹窗、无遮罩叠层。",
    "key_pages_to_capture": [
      {
        "page_role": "业务触发后的引导弹窗页",
        "page_identifier": "MainActivity 上覆盖的 AlertDialog，正文含 'Double-tap to lock needs the Android Accessibility API'，按钮为 OK / Cancel",
        "why_most_useful": "这是全流程唯一的信息披露面，直接决定是否存在恐吓、伪装或隐私误导；同时可验证 Cancel 是否真实可用（无跳过则属强制）",
        "observable_utg_signals": ["弹窗文本与 strings 资源一致且为透明说明", "存在可点击的 Cancel 按钮", "无倒计时、无遮罩、无二次弹窗叠加", "弹窗层级为 Dialog 而非全屏 Overlay"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务中的 'KISS launcher' 项，摘要 'Lock screen from KISS Launcher'",
        "why_most_useful": "验证服务名/描述是否与真实身份一致，是否通过空白、同形字或伪造 isAccessibilityTool 隐藏真实用途",
        "observable_utg_signals": ["服务标题为真实应用名 KISS launcher", "描述明示锁屏用途", "不存在同名重复服务项或多 alias 条目"]
      },
      {
        "page_role": "从系统设置返回后的桌面页",
        "page_identifier": "MainActivity 桌面（无障碍服务仍关闭）",
        "why_most_useful": "验证拒权后是否死循环重跳或强制阻断使用，区分按需引导与胁迫式引导",
        "observable_utg_signals": ["返回后无弹窗重跳", "桌面正常可用、可继续搜索与启动应用", "再次双击才重新出现同一可取消弹窗"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。说明文字全部为本地 strings 文本，无图片引导、无空文本图形诱饵、无远端 HTML、无第一阶段 Dropper、无加壳；纯 UTG 文本提取即可完整判别。"
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
    "fr.neamar.kiss.forwarder.ExperienceTweaks$1.onDoubleTap",
    "fr.neamar.kiss.forwarder.ExperienceTweaks$1$$ExternalSyntheticLambda0.onClick",
    "fr.neamar.kiss.utils.LockAccessibilityService.onStartCommand",
    "res/xml/lock_accessibility_service_config.xml",
    "res/values/strings.xml#L83（enable_double_tap_to_lock）"
  ]
}
```

</details>
