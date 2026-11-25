# BN_024__868b2fe374｜极简桌面与双击锁屏 — Multi Launcher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：208.3s

## 1. 一句话核心结论

- **核心申请方式**：该应用仅在用户主动使用锁屏/快捷设置功能且无障碍服务未连接时，用一条说明弹窗（可取消）+ 携带 :settings:fragment_args_key 的 ACTION_ACCESSIBILITY_SETTINGS 意图直接定位到自身服务条目，理由与实现一致、无诱导与伪装。
- **静态可见性说明**：全部静态可见：Manifest、accessibility_service_config.xml、strings.xml 及各引导/跳转代码（ex0.I、ex0.T、ex0.m、nq1、oq1、MainActivity、OnboardingActivity、ActionService）均为明文 DEX/资源，仅经 R8 混淆（类名短化），无加壳、无 AES/远端 HTML、无二阶段载荷。未展开项仅为 AlertDialog 两个按钮文案资源 id（0x7f110055 / 0x7f1100b7）的具体取值。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `868b2fe374f8dcc14baadddc928d588a75ed75c94f741809a49770b89d4ebb5e` |
| 包名 / 年份 | `app.mlauncher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/app.mlauncher_1120300.apk |
| 桌面显示名 | Multi Launcher |
| 引导页宣称品牌/身份 | Multi Launcher（Multi Launcher ‧ Home Screen，F-Droid 开源极简桌面） |
| 系统无障碍列表服务名 | MultiLauncher Action Services |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务标签、应用名与包名 app.mlauncher 一致；android:description 与 accessibility_service_more_info 均如实说明用途（锁屏、打开快捷设置）与不收集不共享数据，与 ActionService 实际实现（仅保存弱引用、onAccessibilityEvent 不做任何采集）一致。未声明 android:isAccessibilityTool，因此 Android 13+ 会正常弹出系统「受限设置」提示，属如实暴露而非规避；无空白/换行挤出警告、无同形字、无多 activity-alias 伪装。 |
| 无障碍服务类名 | `com.github.codeworkscreativehub.mlauncher.services.ActionService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：app.mlauncher.debug, app.mlauncher |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, READ_CONTACTS` |
| 系统设置项说明 (`android:description`) | This accessibility service allows MultiLauncher to do certain actions such as locking the screen or opening the quick settings. Our accessibility service does not collect or share any data. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.github.codeworkscreativehub.mlauncher.MainActivity → com.github.codeworkscreativehub.mlauncher.ui.onboarding.OnboardingActivity | MainActivity.onCreate 读取 SharedPreferences 的 ONBOARDING_COMPLETED，为 false 时 startActivity(OnboardingActivity) 并 finish() | 原生Activity | **原文**：无（引导页内容由 lq1 分页承载，布局 id 2131558429，未展开逐页文案）<br>**译注**：首次启动进入桌面功能引导页，本步不涉及无障碍权限申请 | 浏览/跳过桌面引导（与无障碍无关） | `com.github.codeworkscreativehub.mlauncher.MainActivity.onCreate；com.github.codeworkscreativehub.mlauncher.ui.onboarding.OnboardingActivity.onCreate` |
| 2 | 业务功能触发 | com.github.codeworkscreativehub.mlauncher.ui.HomeFragment.T → ex0.m(Context) | 用户使用需要无障碍能力的功能（如双击锁屏）时调用；ex0.m 先取 ActionService.p 弱引用，为空（服务未连接）才进入引导 | 原生Activity | 无 | 用户主动触发该功能，无强制冷启动拦截 | `com.github.codeworkscreativehub.mlauncher.ui.HomeFragment.T；ex0.m` |
| 3 | 引导说明页 | 原生 AlertDialog（pe1 = AlertDialog.Builder 包装） | nq1.onClick(View) case 0：设置 title=0x7f110021、message=0x7f11001f，正向按钮回调 oq1(0)，负向按钮 oq1(1)，o4Var.k=true（可取消） | 原生Dialog | **原文**：Why We Need Accessibility Permission / MultiLauncher requires access to the Accessibility Service to enable features such as: • Locking the screen with a gesture or shortcut • Ope…<br>**译注**：标题「为什么我们需要无障碍权限」；正文说明需无障碍服务以实现「用手势或快捷方式锁屏」「打开快捷设置」等功能 | 可选择同意进入系统无障碍设置，或点负向按钮（0x7f1100b7）由 oq1 case 1 → qq1.S() 关闭对话框放弃 | `nq1.onClick；oq1.onClick；res/values/strings.xml（accessibility_service_why_we_need、accessibility_service_more_info）` |
| 4 | 跳无障碍设置 | 系统设置页 Settings$AccessibilitySettings（带 :settings:fragment_args_key 直接定位到 ActionService 条目） | 对话框正向按钮 oq1.onClick case 0 → ex0.I(context)；另 ex0.m 在服务未连接时也会直接调用 ex0.I | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS（Intent action）；":settings:fragment_args_key" / ":settings:show_fragment_args" 携带 ComponentName(context.getPackageName(), ActionService.class.getName()).flattenToString()<br>**译注**：跳转系统无障碍设置并滚动定位到「MultiLauncher Action Services」条目，由用户自行在系统页开启 | 在系统无障碍列表中手动打开「MultiLauncher Action Services」开关；不做任何自动勾选或点击 | `ex0.I；ex0.m` |
| 5 | 拒权反馈循环 | 返回应用后的桌面（HomeFragment） | 从设置返回后 ActionService.p 仍为空；仅在用户再次触发该功能时重复第 2 步，无 onResume 强制重跳、无定时器拉起 | 原生Activity | 无 | 无强制动作；可继续使用其他桌面功能 | `ex0.m（仅由功能触发点调用）；com.github.codeworkscreativehub.mlauncher.services.ActionService.a（节流判定）` |
| 6 | 获权后动作 | com.github.codeworkscreativehub.mlauncher.services.ActionService | onServiceConnected() 仅 new WeakReference(this)；onAccessibilityEvent 仅调用 System.currentTimeMillis()；onUnbind 清空弱引用 | 不可静态还原 | 无 | 无 | `com.github.codeworkscreativehub.mlauncher.services.ActionService.onServiceConnected / onAccessibilityEvent / onUnbind` |
| 7 | 跳受限设置 | 系统设置页 Settings$UsageAccessDetails（ACTION_USAGE_ACCESS_SETTINGS，data=package:app.mlauncher） | nq1.onClick case 3 → ex0.T(context) | 系统无障碍页 | **原文**：To proceed, please enable permission to access usage data in your device settings.<br>**译注**：提示前往系统设置为本应用开启「使用情况访问权限」 | 在系统使用情况访问页为 app.mlauncher 手动开启；失败仅 printStackTrace，无循环施压 | `ex0.T；nq1.onClick case 3` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表服务条目说明：res/xml/accessibility_service_config.xml 的 android:description → strings.xml accessibility_service_description
- 系统无障碍列表服务名称：Manifest service android:label → strings.xml accessibility_service_name（MultiLauncher Action Services）
- 应用内原生 AlertDialog（nq1.onClick 构建，pe1/AlertDialog.Builder）：标题 accessibility_service_why_we_need、正文 accessibility_service_more_info
- 首次启动 OnboardingActivity 引导页（setContentView 2131558429 + lq1 分页），承载桌面功能说明而非权限施压
- strings.xml 中未被代码引用的说明性文案：accessibility_access_permission、grant_accessibility_permission、reason_accessibility_permission（预留/文档用途，未发现运行期强制弹出点）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | This accessibility service allows MultiLauncher to do certain actions such as locking the screen or opening the quick settings. Our accessibility service does not collect or share any data. | 本无障碍服务允许 MultiLauncher 执行锁屏、打开快捷设置等操作。我们的无障碍服务不收集也不共享任何数据。 | `res/values/strings.xml → accessibility_service_description（由 accessibility_service_config.xml android:description 引用）` | 良性透明说明 |
| en | Why We Need Accessibility Permission | 为什么我们需要无障碍权限 | `res/values/strings.xml → accessibility_service_why_we_need（0x7f110021），nq1.onClick 用作对话框标题` | 受限设置分步教学 |
| en | MultiLauncher requires access to the Accessibility Service to enable features such as: • Locking the screen with a gesture or shortcut • Ope… | MultiLauncher 需要无障碍服务以启用以下功能：• 通过手势或快捷方式锁屏 • 打开（快捷设置）…… | `res/values/strings.xml → accessibility_service_more_info（0x7f11001f），nq1.onClick 用作对话框正文` | 良性透明说明 |
| en | MultiLauncher needs Accessibility permission to provide enhanced features, such as locking the screen and opening quick settings. These functions help improve usability. We do not collect or share any data. | MultiLauncher 需要无障碍权限以提供锁屏、打开快捷设置等增强功能，这些功能提升易用性。我们不收集也不共享任何数据。 | `res/values/strings.xml → reason_accessibility_permission` | 隐私承诺 |
| en | To proceed, please enable permission to access usage data in your device settings. | 如需继续，请在设备设置中开启使用情况数据访问权限。 | `res/values/strings.xml（使用情况访问引导文案），对应 ex0.T 跳转 ACTION_USAGE_ACCESS_SETTINGS` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。对话框 setCancelable(true) 且带负向按钮（oq1 case 1 → qq1.S() 关闭）；从系统设置返回后不监听 onResume 重跳、无 Timer 拉起，仅当用户再次触发依赖功能且 ActionService.p 仍为空时才重新进入引导（ActionService.a() 还做了时间节流）。
- **遮罩叠层 / 高仿系统设置页**：无。不叠放遮罩/悬浮窗，不伪造系统无障碍开关页；跳转的是真实系统 Settings，仅通过 :settings:fragment_args_key 定位到自身服务条目。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现引导进入应用详情点右上角菜单开启「允许受限设置」的文案或跳转（未引用 ACTION_APPLICATION_DETAILS_SETTINGS），亦无 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅保存 WeakReference，onAccessibilityEvent 不读取节点、不监听设置页，未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权；performGlobalAction 仅用于用户触发的锁屏动作。
- **良性降级 / 替代方案**：有。无障碍未授权时仅相关功能（锁屏/快捷设置）不可用，应用提示后留在桌面正常使用；拒绝授权后不再打扰，符合开源桌面应用的功能降级模型。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在检测到 ex0.I 发起 ACTION_ACCESSIBILITY_SETTINGS（携带 :settings:fragment_args_key）跳转的瞬间拉起 UTG，或在首次启动 MainActivity→OnboardingActivity 之后、用户触发锁屏功能导致弹窗出现时拉起；重点抓系统无障碍设置页与本应用弹窗两帧。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。全部引导文案为可读文本节点（原生 Dialog + 系统设置 + strings.xml），无纯图片诱导、无远端 HTML、无一阶段 Dropper、无静态加壳；唯一非文本环节为 OnboardingActivity 内部分页布局内容未逐页展开，但其与无障碍授权无关联。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页** | com.github.codeworkscreativehub.mlauncher.ui.onboarding.OnboardingActivity（布局 2131558429，lq1 分页） | 确认首启流程是否夹带无障碍施压，本应用此处仅为桌面功能引导 | Activity 名为 OnboardingActivity 而非无障碍设置或伪造页面；页面节点文本不含权限索取语句 |
| **跳转前说明弹窗页** | 原生 AlertDialog，标题文本 "Why We Need Accessibility Permission" | 区分「一次性可取消的如实说明」与「不可取消的恐吓/伪造故障诱导」 | 对话框同时存在正向与负向按钮节点（可取消）；正文文案与 android:description 语义一致，无「不开启将损坏设备/病毒」类话术 |
| **系统无障碍服务列表项** | Settings$AccessibilitySettings，条目文本 "MultiLauncher Action Services"，说明文本为 accessibility_service_description | 核对是否为真实系统设置页（非高仿）以及服务名/描述是否与实际实现一致 | 窗口属于 com.android.settings 而非应用包名；服务条目描述为锁屏/快捷设置与不收集数据声明；若为 Android 13+ 出现系统「受限设置」原生提示 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `ex0.I`
- `ex0.m`
- `ex0.T`
- `nq1.onClick`
- `oq1.onClick`
- `com.github.codeworkscreativehub.mlauncher.services.ActionService.onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态，可见性完整）

**整体判断：良性透明实现，无诱导、无伪装、无遮罩、无拒权死循环。** 全程静态可见，未加壳（`apk` 无壳特征，DEX 仅 R8 混淆，字符串与资源明文可读）。

**引导链路（运行期 UTG 视角）**

1. **冷启动**：`MainActivity.onCreate` 检查 `ONBOARDING_COMPLETED`，为 false 时启动 `OnboardingActivity` 并 `finish()` —— 首次启动进入引导页（`OnboardingActivity.onCreate` → `setContentView(2131558429)` + `lq1` 分页内容），而非无障碍权限页。
2. **按需触发**：仅当用户使用依赖无障碍的功能时，`HomeFragment.T` 调用 `ex0.m(context)`；若 `ActionService.p` 弱引用为空（服务未连接），才打开设置。
3. **跳转受限设置**：[ex0.I()](<resource-unit:#1.dex1 code:ex0#I>) 构造 `Intent("android.settings.ACCESSIBILITY_SETTINGS")`，并用 `ComponentName(pkg, ActionService).flattenToString()` 作为 `:settings:fragment_args_key` / `:settings:show_fragment_args`，**直接定位到本应用自己的无障碍服务条目**（不伪造页面、不覆盖系统 UI），随后记录日志 "Accessibility Settings Opened"。
4. **说明弹窗**：由 [nq1.onClick()](<resource-unit:#1.dex1 code:nq1#onClick>) case 0 构建 `AlertDialog`，标题取 `0x7f110021`（`accessibility_service_why_we_need` = "Why We Need Accessibility Permission"），正文取 `0x7f11001f`（`accessibility_service_more_info` = "MultiLauncher requires access to the Accessibility Service to enable features such as: …"），正向按钮回调 [oq1.onClick()](<resource-unit:#1.dex1 code:oq1#onClick>) case 0 → `ex0.I()`；负向按钮走 case 1 → `qq1.S()`（关闭，**存在取消路径**，`setCancelable(true)`）。
5. **同类权限**：case 3 → [ex0.T()](<resource-unit:#1.dex1 code:ex0#T>) 打开 `ACTION_USAGE_ACCESS_SETTINGS`（带 `package:`），对应预筛的 `PACKAGE_USAGE_STATS`。
6. **获权后动作**：`ActionService.onServiceConnected` 只保存 `WeakReference(this)`；`onAccessibilityEvent` 仅取 `System.currentTimeMillis()`，不做任何读取/转发；`onAccessibilityEvent` 无节点内容采集。`a()` 为 1 次/间隔的节流开关，供 `HomeFragment.T` 锁屏（`performGlobalAction`）使用。**无撤权对抗、无自点确认、无 `GLOBAL_ACTION_BACK` 监听。**

**服务声明的透明度**：[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml#L1-L3>) 中 `packageNames="app.mlauncher.debug, app.mlauncher"`（作用域收窄到自身）、`canRetrieveWindowContent="true"` 但代码未使用窗口内容；`android:description` 如实声明"锁屏/打开快捷设置、不收集不共享数据"，与实现一致。未声明 `android:isAccessibilityTool`，Android 13+ 会触发系统"受限设置"提示，属如实暴露而非规避。

**覆盖边界**：未对 R8 混淆后的 `pe1`（`AlertDialog.Builder` 包装）内部按钮文案资源 `0x7f110055` / `0x7f1100b7` 逐条展开取值；未做动态验证（结论基于代码与资源闭环，静态证据已足够定性）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部静态可见：Manifest、accessibility_service_config.xml、strings.xml 及各引导/跳转代码（ex0.I、ex0.T、ex0.m、nq1、oq1、MainActivity、OnboardingActivity、ActionService）均为明文 DEX/资源，仅经 R8 混淆（类名短化），无加壳、无 AES/远端 HTML、无二阶段载荷。未展开项仅为 AlertDialog 两个按钮文案资源 id（0x7f110055 / 0x7f1100b7）的具体取值。",
  "summary_one_liner": "该应用仅在用户主动使用锁屏/快捷设置功能且无障碍服务未连接时，用一条说明弹窗（可取消）+ 携带 :settings:fragment_args_key 的 ACTION_ACCESSIBILITY_SETTINGS 意图直接定位到自身服务条目，理由与实现一致、无诱导与伪装。",
  "disguise_identity": {
    "app_display_name": "Multi Launcher",
    "claimed_brand_or_persona": "Multi Launcher（Multi Launcher ‧ Home Screen，F-Droid 开源极简桌面）",
    "a11y_service_label": "MultiLauncher Action Services",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务标签、应用名与包名 app.mlauncher 一致；android:description 与 accessibility_service_more_info 均如实说明用途（锁屏、打开快捷设置）与不收集不共享数据，与 ActionService 实际实现（仅保存弱引用、onAccessibilityEvent 不做任何采集）一致。未声明 android:isAccessibilityTool，因此 Android 13+ 会正常弹出系统「受限设置」提示，属如实暴露而非规避；无空白/换行挤出警告、无同形字、无多 activity-alias 伪装。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.github.codeworkscreativehub.mlauncher.MainActivity → com.github.codeworkscreativehub.mlauncher.ui.onboarding.OnboardingActivity",
      "trigger_event": "MainActivity.onCreate 读取 SharedPreferences 的 ONBOARDING_COMPLETED，为 false 时 startActivity(OnboardingActivity) 并 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（引导页内容由 lq1 分页承载，布局 id 2131558429，未展开逐页文案）",
      "shown_text_zh": "首次启动进入桌面功能引导页，本步不涉及无障碍权限申请",
      "user_action_requested": "浏览/跳过桌面引导（与无障碍无关）",
      "code_anchor": "com.github.codeworkscreativehub.mlauncher.MainActivity.onCreate；com.github.codeworkscreativehub.mlauncher.ui.onboarding.OnboardingActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.github.codeworkscreativehub.mlauncher.ui.HomeFragment.T → ex0.m(Context)",
      "trigger_event": "用户使用需要无障碍能力的功能（如双击锁屏）时调用；ex0.m 先取 ActionService.p 弱引用，为空（服务未连接）才进入引导",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "功能不可用时判定无障碍服务未连接，转入权限说明/跳转流程",
      "user_action_requested": "用户主动触发该功能，无强制冷启动拦截",
      "code_anchor": "com.github.codeworkscreativehub.mlauncher.ui.HomeFragment.T；ex0.m"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "原生 AlertDialog（pe1 = AlertDialog.Builder 包装）",
      "trigger_event": "nq1.onClick(View) case 0：设置 title=0x7f110021、message=0x7f11001f，正向按钮回调 oq1(0)，负向按钮 oq1(1)，o4Var.k=true（可取消）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Why We Need Accessibility Permission / MultiLauncher requires access to the Accessibility Service to enable features such as: • Locking the screen with a gesture or shortcut • Ope…",
      "shown_text_zh": "标题「为什么我们需要无障碍权限」；正文说明需无障碍服务以实现「用手势或快捷方式锁屏」「打开快捷设置」等功能",
      "user_action_requested": "可选择同意进入系统无障碍设置，或点负向按钮（0x7f1100b7）由 oq1 case 1 → qq1.S() 关闭对话框放弃",
      "code_anchor": "nq1.onClick；oq1.onClick；res/values/strings.xml（accessibility_service_why_we_need、accessibility_service_more_info）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings$AccessibilitySettings（带 :settings:fragment_args_key 直接定位到 ActionService 条目）",
      "trigger_event": "对话框正向按钮 oq1.onClick case 0 → ex0.I(context)；另 ex0.m 在服务未连接时也会直接调用 ex0.I",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS（Intent action）；\":settings:fragment_args_key\" / \":settings:show_fragment_args\" 携带 ComponentName(context.getPackageName(), ActionService.class.getName()).flattenToString()",
      "shown_text_zh": "跳转系统无障碍设置并滚动定位到「MultiLauncher Action Services」条目，由用户自行在系统页开启",
      "user_action_requested": "在系统无障碍列表中手动打开「MultiLauncher Action Services」开关；不做任何自动勾选或点击",
      "code_anchor": "ex0.I；ex0.m"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回应用后的桌面（HomeFragment）",
      "trigger_event": "从设置返回后 ActionService.p 仍为空；仅在用户再次触发该功能时重复第 2 步，无 onResume 强制重跳、无定时器拉起",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "拒绝授权后应用正常降级，不弹二次施压、不循环跳转",
      "user_action_requested": "无强制动作；可继续使用其他桌面功能",
      "code_anchor": "ex0.m（仅由功能触发点调用）；com.github.codeworkscreativehub.mlauncher.services.ActionService.a（节流判定）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.github.codeworkscreativehub.mlauncher.services.ActionService",
      "trigger_event": "onServiceConnected() 仅 new WeakReference(this)；onAccessibilityEvent 仅调用 System.currentTimeMillis()；onUnbind 清空弱引用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务连接后不采集窗口内容、不外发事件，仅作为锁屏/快捷设置动作的载体；无自点确认、无阻止撤权",
      "user_action_requested": "无",
      "code_anchor": "com.github.codeworkscreativehub.mlauncher.services.ActionService.onServiceConnected / onAccessibilityEvent / onUnbind"
    },
    {
      "step": 7,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置页 Settings$UsageAccessDetails（ACTION_USAGE_ACCESS_SETTINGS，data=package:app.mlauncher）",
      "trigger_event": "nq1.onClick case 3 → ex0.T(context)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "To proceed, please enable permission to access usage data in your device settings.",
      "shown_text_zh": "提示前往系统设置为本应用开启「使用情况访问权限」",
      "user_action_requested": "在系统使用情况访问页为 app.mlauncher 手动开启；失败仅 printStackTrace，无循环施压",
      "code_anchor": "ex0.T；nq1.onClick case 3"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表服务条目说明：res/xml/accessibility_service_config.xml 的 android:description → strings.xml accessibility_service_description",
    "系统无障碍列表服务名称：Manifest service android:label → strings.xml accessibility_service_name（MultiLauncher Action Services）",
    "应用内原生 AlertDialog（nq1.onClick 构建，pe1/AlertDialog.Builder）：标题 accessibility_service_why_we_need、正文 accessibility_service_more_info",
    "首次启动 OnboardingActivity 引导页（setContentView 2131558429 + lq1 分页），承载桌面功能说明而非权限施压",
    "strings.xml 中未被代码引用的说明性文案：accessibility_access_permission、grant_accessibility_permission、reason_accessibility_permission（预留/文档用途，未发现运行期强制弹出点）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "This accessibility service allows MultiLauncher to do certain actions such as locking the screen or opening the quick settings. Our accessibility service does not collect or share any data.",
      "text_zh": "本无障碍服务允许 MultiLauncher 执行锁屏、打开快捷设置等操作。我们的无障碍服务不收集也不共享任何数据。",
      "source_location": "res/values/strings.xml → accessibility_service_description（由 accessibility_service_config.xml android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Why We Need Accessibility Permission",
      "text_zh": "为什么我们需要无障碍权限",
      "source_location": "res/values/strings.xml → accessibility_service_why_we_need（0x7f110021），nq1.onClick 用作对话框标题",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "MultiLauncher requires access to the Accessibility Service to enable features such as: • Locking the screen with a gesture or shortcut • Ope…",
      "text_zh": "MultiLauncher 需要无障碍服务以启用以下功能：• 通过手势或快捷方式锁屏 • 打开（快捷设置）……",
      "source_location": "res/values/strings.xml → accessibility_service_more_info（0x7f11001f），nq1.onClick 用作对话框正文",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "MultiLauncher needs Accessibility permission to provide enhanced features, such as locking the screen and opening quick settings. These functions help improve usability. We do not collect or share any data.",
      "text_zh": "MultiLauncher 需要无障碍权限以提供锁屏、打开快捷设置等增强功能，这些功能提升易用性。我们不收集也不共享任何数据。",
      "source_location": "res/values/strings.xml → reason_accessibility_permission",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "To proceed, please enable permission to access usage data in your device settings.",
      "text_zh": "如需继续，请在设备设置中开启使用情况数据访问权限。",
      "source_location": "res/values/strings.xml（使用情况访问引导文案），对应 ex0.T 跳转 ACTION_USAGE_ACCESS_SETTINGS",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。对话框 setCancelable(true) 且带负向按钮（oq1 case 1 → qq1.S() 关闭）；从系统设置返回后不监听 onResume 重跳、无 Timer 拉起，仅当用户再次触发依赖功能且 ActionService.p 仍为空时才重新进入引导（ActionService.a() 还做了时间节流）。",
    "overlay_or_fake_settings": "无。不叠放遮罩/悬浮窗，不伪造系统无障碍开关页；跳转的是真实系统 Settings，仅通过 :settings:fragment_args_key 定位到自身服务条目。",
    "restricted_settings_13plus_coaching": "无。未发现引导进入应用详情点右上角菜单开启「允许受限设置」的文案或跳转（未引用 ACTION_APPLICATION_DETAILS_SETTINGS），亦无 Session 安装器绕过。",
    "post_grant_anti_removal": "无。onServiceConnected 仅保存 WeakReference，onAccessibilityEvent 不读取节点、不监听设置页，未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权；performGlobalAction 仅用于用户触发的锁屏动作。",
    "benign_graceful_degradation": "有。无障碍未授权时仅相关功能（锁屏/快捷设置）不可用，应用提示后留在桌面正常使用；拒绝授权后不再打扰，符合开源桌面应用的功能降级模型。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在检测到 ex0.I 发起 ACTION_ACCESSIBILITY_SETTINGS（携带 :settings:fragment_args_key）跳转的瞬间拉起 UTG，或在首次启动 MainActivity→OnboardingActivity 之后、用户触发锁屏功能导致弹窗出现时拉起；重点抓系统无障碍设置页与本应用弹窗两帧。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页",
        "page_identifier": "com.github.codeworkscreativehub.mlauncher.ui.onboarding.OnboardingActivity（布局 2131558429，lq1 分页）",
        "why_most_useful": "确认首启流程是否夹带无障碍施压，本应用此处仅为桌面功能引导",
        "observable_utg_signals": ["Activity 名为 OnboardingActivity 而非无障碍设置或伪造页面", "页面节点文本不含权限索取语句"]
      },
      {
        "page_role": "跳转前说明弹窗页",
        "page_identifier": "原生 AlertDialog，标题文本 \"Why We Need Accessibility Permission\"",
        "why_most_useful": "区分「一次性可取消的如实说明」与「不可取消的恐吓/伪造故障诱导」",
        "observable_utg_signals": ["对话框同时存在正向与负向按钮节点（可取消）", "正文文案与 android:description 语义一致，无「不开启将损坏设备/病毒」类话术"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings$AccessibilitySettings，条目文本 \"MultiLauncher Action Services\"，说明文本为 accessibility_service_description",
        "why_most_useful": "核对是否为真实系统设置页（非高仿）以及服务名/描述是否与实际实现一致",
        "observable_utg_signals": ["窗口属于 com.android.settings 而非应用包名", "服务条目描述为锁屏/快捷设置与不收集数据声明", "若为 Android 13+ 出现系统「受限设置」原生提示"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。全部引导文案为可读文本节点（原生 Dialog + 系统设置 + strings.xml），无纯图片诱导、无远端 HTML、无一阶段 Dropper、无静态加壳；唯一非文本环节为 OnboardingActivity 内部分页布局内容未逐页展开，但其与无障碍授权无关联。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE"
  ],
  "code_anchors": [
    "ex0.I",
    "ex0.m",
    "ex0.T",
    "nq1.onClick",
    "oq1.onClick",
    "com.github.codeworkscreativehub.mlauncher.services.ActionService.onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
