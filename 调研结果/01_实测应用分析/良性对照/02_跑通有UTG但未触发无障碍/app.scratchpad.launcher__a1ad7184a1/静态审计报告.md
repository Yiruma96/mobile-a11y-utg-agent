# BN_026__a1ad7184a1｜极简桌面与双击锁屏 — Scratchpad Launcher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：203.2s

## 1. 一句话核心结论

- **核心申请方式**：仅在设置页「Double tap to lock」开关处弹出原生说明弹窗（含 Close 取消与外部帮助链接），用户点 Enable 才跳系统无障碍设置页，获权后仅用于双击锁屏（performGlobalAction LOCK_SCREEN），无遮罩、无循环重跳、无身份伪装。
- **静态可见性说明**：全部关键逻辑（弹窗构建、跳转点、权限校验、获权后回调）均静态可见于 classes.dex 与 res/ 资源；无加壳、无 AES 密文载荷、assets 目录为空、无 WebView/远端 HTML 参与引导。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a1ad7184a13bfcb2ed8e05606067682ecf7e29c676932c481f68d1e66135eb12` |
| 包名 / 年份 | `app.scratchpad.launcher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/app.scratchpad.launcher_22.apk |
| 桌面显示名 | Scratchpad Launcher |
| 引导页宣称品牌/身份 | Scratchpad Launcher（F-Droid 开源极简桌面，原作者 Olauncher/tanujnotes） |
| 系统无障碍列表服务名 | Scratchpad Launcher |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅存在一处无害遗留：accessibility_service_config.xml 中 android:settingsActivity 指向占位类 com.example.android.accessibility.ServiceSettingsActivity（未在 Manifest 声明，不可达）。 |
| 无障碍服务类名 | `app.olauncher.helper.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：app.scratchpad.launcher.debug, app.scratchpad.launcher |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Scratchpad Launcher via this service will not leave your device. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | app.olauncher.ui.SettingsFragment（设置页「Double tap to lock」开关行，view id 2131296828） | 用户主动点击该开关；或长按同一行触发 SettingsFragment.onLongClick（同样直接跳 ACCESSIBILITY_SETTINGS） | 原生Activity | **原文**：Please turn on double tap to lock<br>**译注**：请开启双击锁屏 | 点击开关开启「双击锁屏」功能；不点击则不会出现任何无障碍引导 | `app.olauncher.ui.SettingsFragment#onClick (case 2131296828) / app.olauncher.ui.SettingsFragment#onLongClick` |
| 2 | 引导说明页 | MaterialAlertDialog（MaterialAlertDialogBuilder，标题 @string/gestures） | onClick 中判定 LOCK_MODE==false 且 x0.b.q(N())==false（当前未启用无障碍）后 eVar.a().show() | 原生Dialog | **原文**：Gestures<br><br>Please turn on Scratchpad Launcher's accessibility service in your device's settings to enable Double tap to lock gesture. <br><br>Please note that this service is only used for this particular feature. Our accessibility service does not collect or share any data.<br><br>If the switch is greyed out (Android 13+): open App info → ⋮ → Allow restricted settings, then try again.<br><br>[Close] [Not working?] [Enable]<br>**译注**：手势<br><br>请在设备设置中开启 Scratchpad Launcher 的无障碍服务，以启用「双击锁屏」手势。请注意该服务仅用于此功能，我们的无障碍服务不收集也不共享任何数据。<br>（Android 13+）若开关置灰：进入应用信息 → ⋮ → 允许受限设置，然后重试。<br>[关闭] [用不了？] [启用] | 可点 Close 直接取消；可点「Not working?」打开外部帮助网页；点 Enable 才继续跳转系统设置 | `app.olauncher.ui.SettingsFragment#onClick (2131820684 / 2131820584 / 2131820844 / 2131820635 / 2131820815 / 2131820648-2131820655)` |
| 3 | 跳无障碍设置 | 系统设置「无障碍 → 已安装的服务」页（Intent android.settings.ACCESSIBILITY_SETTINGS） | 弹窗 Positive 按钮「Enable」→ A0.s0#onClick 默认分支 → this.g.R(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Scratchpad Launcher via this service will not leave your device.<br>**译注**：需要无障碍权限以启用「双击锁屏」手势。Scratchpad Launcher 通过该服务获取的任何数据都不会离开你的设备。 | 在系统无障碍列表中手动找到并打开「Scratchpad Launcher」服务开关；应用无法代为开启，也无自动点击确认 | `A0.s0#onClick / res/xml/accessibility_service_config.xml (android:description=@string/accessibility_service_description)` |
| 4 | 拒权反馈循环 | 返回设置页后的 SettingsFragment（Y() 刷新开关状态） | 从系统设置返回、SettingsFragment#Y 或 I 回调刷新 SwitchCompat.setChecked(z) | 原生Activity | **原文**：无（仅开关保持关闭状态，不弹任何二次提示）<br>**译注**：无额外提示，开关维持未开启 | 无强制动作，可正常使用其他桌面功能 | `app.olauncher.ui.SettingsFragment#Y / x0.b#q` |
| 5 | 获权后动作 | app.olauncher.helper.MyAccessibilityService（独立进程 :serviceProcess） | 系统绑定服务 → onServiceConnected() 写 SharedPreferences LOCK_MODE=true | 不可静态还原 | 无 | 无 | `app.olauncher.helper.MyAccessibilityService#onServiceConnected` |
| 6 | 获权后动作 | 桌面双击手势 → 锁屏控件点击 → MyAccessibilityService.onAccessibilityEvent | z0.c#onDoubleTap 检测到 LOCK_MODE=true 后调用 lockView.performClick()；服务收到 typeViewClicked 事件且 contentDescription==@string/lock_layout_description 时 performGlobalAction(8) | 不可静态还原 | **原文**：lock layout description to be used a unique id to lock screen<br>**译注**：用作锁屏唯一标识的布局描述 | 用户在桌面双击即锁屏 | `z0.c#onDoubleTap / app.olauncher.helper.MyAccessibilityService#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- SettingsFragment 内 MaterialAlertDialog（非全屏、可取消）：标题 @string/gestures，正文 @string/accessibility_disclosure，Android 13+ 追加 @string/restricted_settings_hint
- 系统无障碍服务列表项：android:label=@string/app_name（Scratchpad Launcher）与 android:description=@string/accessibility_service_description（来自 res/xml/accessibility_service_config.xml）
- 设置页开关行文案：@string/please_turn_on_double_tap_to_unlock（Please turn on double tap to lock）
- 「Not working?」按钮打开外部浏览器网页 https://tanujnotes.notion.site/Double-tap-to-lock-Olauncher-0f7fb103ec1f47d7a90cdfdcd7fb86ef（x0.b.y）
- 设备管理员（仅 Android 9 以下锁屏路径）说明文案 @string/admin_permission_message（'Scratchpad Launcher promises to use the accessibility permission responsibly. Scratchpad Launcher does not collect or share any data.'）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Please turn on Scratchpad Launcher's accessibility service in your device's settings to enable Double tap to lock gesture. <br><br>Please note that this service is only used for this particular feature. Our accessibility service does not collect or share any data. | 请在设备设置中开启 Scratchpad Launcher 的无障碍服务，以启用「双击锁屏」手势。请注意该服务仅用于此特定功能，我们的无障碍服务不收集也不共享任何数据。 | `res/values/strings.xml key=accessibility_disclosure` | 隐私承诺 |
| en | If the switch is greyed out (Android 13+): open App info → ⋮ → Allow restricted settings, then try again. | 若开关置灰（Android 13+）：进入应用信息 → ⋮ → 允许受限设置，然后重试。 | `res/values/strings.xml key=restricted_settings_hint` | 受限设置分步教学 |
| en | The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Scratchpad Launcher via this service will not leave your device. | 需要无障碍权限以启用「双击锁屏」手势。Scratchpad Launcher 通过该服务获取的任何数据都不会离开你的设备。 | `res/values/strings.xml key=accessibility_service_description（res/xml/accessibility_service_config.xml 引用）` | 良性透明说明 |
| en | Please turn on double tap to lock | 请开启双击锁屏 | `res/values/strings.xml key=please_turn_on_double_tap_to_unlock` | 良性透明说明 |
| en | Scratchpad Launcher promises to use the accessibility permission responsibly. Scratchpad Launcher does not collect or share any data. | Scratchpad Launcher 承诺负责任地使用无障碍权限，不收集也不共享任何数据。 | `res/values/strings.xml key=admin_permission_message（Android 9 以下设备管理员路径 ADD_EXPLANATION）` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。返回设置页后仅由 SettingsFragment#Y() 依据 LOCK_MODE 与 x0.b#q() 刷新开关勾选状态，开关保持关闭；MainActivity.onResume 只重置内部标志，不重跳设置页、不弹二次提示
- **遮罩叠层 / 高仿系统设置页**：无。未使用 TYPE_APPLICATION_OVERLAY/SYSTEM_ALERT_WINDOW，无半透明遮罩或高仿无障碍开关页；引导仅为一个可取消的原生 AlertDialog
- **Android 13+ 受限设置（Restricted Settings）应对**：有，但为透明说明：SDK_INT>=33 时弹窗正文追加 restricted_settings_hint（App info → ⋮ → Allow restricted settings 后重试）；未使用 Session 安装器绕过
- **获权后即时行为与防撤权机制**：无。服务无 GLOBAL_ACTION_BACK/HOME 撤权阻止、无自点确认、无监听设置页行为；onAccessibilityEvent 仅匹配 contentDescription==lock_layout_description 时执行 performGlobalAction(8) 锁屏
- **良性降级 / 替代方案**：有。关闭/取消弹窗后桌面其余功能（搜索、抽屉、便签）正常可用；Android 9 以下自动改用 DeviceAdmin（ADD_DEVICE_ADMIN, requestCode 666）实现锁屏，Android 10+ 才走无障碍路径

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：无需冷启动即拉起：先手动进入设置页点击「Double tap to lock」开关（或长按该行）捕获弹窗，再点 Enable 时以监测到 Activity 切换至 com.android.settings/.Settings$AccessibilitySettings（或 intent=android.settings.ACCESSIBILITY_SETTINGS）为拉起时机
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一需注意：Android 9 以下锁屏路径会触发 DeviceAdmin（android.app.action.ADD_DEVICE_ADMIN）系统页，属功能替代实现而非权限诱导，UTG 侧应区分处理；外部帮助链接指向浏览器网页，非应用内 WebView 引导。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **触发前的应用设置页（对照页）** | app.scratchpad.launcher 设置页，含文本 'Please turn on double tap to lock' 与 Switch 控件 | 确认引导不是冷启动强制弹出，而是用户点该功能开关后才出现，用于区分 on-demand 与 cold_start_block | 当前包名 app.scratchpad.launcher 且非系统设置；页面存在 'Please turn on double tap to lock' 文本节点；无弹窗/无遮罩节点 |
| **无障碍引导弹窗页** | 标题 'Gestures' 的 AlertDialog，按钮 'Close' / 'Not working?' / 'Enable' | 该页是全部说明文字的唯一载体，可直接判定是否存在恐吓、假更新、教唆忽视警告等话术，并验证取消路径是否存在 | 弹窗正文包含 'does not collect or share any data' 隐私承诺；存在 Close 取消按钮（可取消性）；按钮文本 Enable/Close/Not working?；无虚假系统弹窗样式（非 Settings 包名） |
| **系统无障碍服务列表项** | com.android.settings 无障碍服务列表中的 'Scratchpad Launcher' 条目及其 description 文本 | 核对服务名与描述是否与应用身份一致、有无空白/同形字伪装 | 服务标签恰为 'Scratchpad Launcher'；description 含 'will not leave your device'；无重复相似条目/多 alias |
| **获权后返回的应用设置页** | 设置页开关变为已选中状态 | 验证拒权不重跳、获权后状态刷新为真实值而非强制置真 | 返回后无新弹窗；Switch 状态与系统实际开启状态一致 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `app.olauncher.ui.SettingsFragment#onClick`
- `A0.s0#onClick`
- `x0.b#q`
- `app.olauncher.helper.MyAccessibilityService#onServiceConnected`
- `app.olauncher.helper.MyAccessibilityService#onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**定性：良性、透明的按需申请（on-demand），不存在诱导、伪装或强制循环。**

- **触发点唯一且与业务功能绑定**：无障碍开关只挂在设置页「Double tap to lock」这一行的点击事件上（`SettingsFragment.onClick`，view id `2131296828`）；冷启动和 `MainActivity.onResume` 都不会弹出引导或跳转设置。
- **引导载体为原生 AlertDialog**（`MaterialAlertDialogBuilder`），标题 `gestures`="Gestures"，正文为 `accessibility_disclosure` 原文；Android 13+ 追加 `restricted_settings_hint`（"App info → ⋮ → Allow restricted settings"）分步说明。
- **弹窗具备明确取消/退出**：Negative="Close"，Neutral="Not working?"（打开外部 Notion 帮助页 `tanujnotes.notion.site/Double-tap-to-lock-Olauncher-...`），Positive="Enable" → `new Intent("android.settings.ACCESSIBILITY_SETTINGS")` 经 `X.w.R()` 跳系统设置。
- **无遮罩/无假设置页/无 WebView/无 assets 内 HTML**：解包目录 `assets/` 为空，全包仅两处 `ACCESSIBILITY_SETTINGS` 跳转（`A0.s0#onClick` 弹窗按钮、`SettingsFragment#onLongClick` 长按同一行），未出现 `ACTION_APPLICATION_DETAILS_SETTINGS`、`isAccessibilityTool` 伪造、`GLOBAL_ACTION_BACK/HOME` 阻撤权。
- **拒权行为为良性降级**：`SettingsFragment#Y()` 仅在 `LOCK_MODE && (SDK<28 || x0.b#q())` 时把开关置为选中；返回设置页不重跳、不弹二次恐吓，开关保持关闭。
- **获权后动作**：`MyAccessibilityService.onServiceConnected()` 写入 `LOCK_MODE=true`；`onAccessibilityEvent` 仅当点击节点 contentDescription 等于 `lock_layout_description` 时执行 `performGlobalAction(8)`（锁屏）。服务配置 `packageNames` 限定为自身包名、事件类型仅 `typeViewClicked`，`canRetrieveWindowContent=true` 但代码未读取窗口内容外发。
- **身份一致**：应用名、服务 `android:label`、`android:description` 均为 "Scratchpad Launcher"，无品牌冒用、无同形字/换行挤出。遗留 `android:settingsActivity="com.example.android.accessibility.ServiceSettingsActivity"` 为未在 Manifest 声明的占位类，无害。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键逻辑（弹窗构建、跳转点、权限校验、获权后回调）均静态可见于 classes.dex 与 res/ 资源；无加壳、无 AES 密文载荷、assets 目录为空、无 WebView/远端 HTML 参与引导。",
  "summary_one_liner": "仅在设置页「Double tap to lock」开关处弹出原生说明弹窗（含 Close 取消与外部帮助链接），用户点 Enable 才跳系统无障碍设置页，获权后仅用于双击锁屏（performGlobalAction LOCK_SCREEN），无遮罩、无循环重跳、无身份伪装。",
  "disguise_identity": {
    "app_display_name": "Scratchpad Launcher",
    "claimed_brand_or_persona": "Scratchpad Launcher（F-Droid 开源极简桌面，原作者 Olauncher/tanujnotes）",
    "a11y_service_label": "Scratchpad Launcher",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅存在一处无害遗留：accessibility_service_config.xml 中 android:settingsActivity 指向占位类 com.example.android.accessibility.ServiceSettingsActivity（未在 Manifest 声明，不可达）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "app.olauncher.ui.SettingsFragment（设置页「Double tap to lock」开关行，view id 2131296828）",
      "trigger_event": "用户主动点击该开关；或长按同一行触发 SettingsFragment.onLongClick（同样直接跳 ACCESSIBILITY_SETTINGS）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please turn on double tap to lock",
      "shown_text_zh": "请开启双击锁屏",
      "user_action_requested": "点击开关开启「双击锁屏」功能；不点击则不会出现任何无障碍引导",
      "code_anchor": "app.olauncher.ui.SettingsFragment#onClick (case 2131296828) / app.olauncher.ui.SettingsFragment#onLongClick"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MaterialAlertDialog（MaterialAlertDialogBuilder，标题 @string/gestures）",
      "trigger_event": "onClick 中判定 LOCK_MODE==false 且 x0.b.q(N())==false（当前未启用无障碍）后 eVar.a().show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Gestures\n\nPlease turn on Scratchpad Launcher's accessibility service in your device's settings to enable Double tap to lock gesture. \n\nPlease note that this service is only used for this particular feature. Our accessibility service does not collect or share any data.\n\nIf the switch is greyed out (Android 13+): open App info → ⋮ → Allow restricted settings, then try again.\n\n[Close] [Not working?] [Enable]",
      "shown_text_zh": "手势\n\n请在设备设置中开启 Scratchpad Launcher 的无障碍服务，以启用「双击锁屏」手势。请注意该服务仅用于此功能，我们的无障碍服务不收集也不共享任何数据。\n（Android 13+）若开关置灰：进入应用信息 → ⋮ → 允许受限设置，然后重试。\n[关闭] [用不了？] [启用]",
      "user_action_requested": "可点 Close 直接取消；可点「Not working?」打开外部帮助网页；点 Enable 才继续跳转系统设置",
      "code_anchor": "app.olauncher.ui.SettingsFragment#onClick (2131820684 / 2131820584 / 2131820844 / 2131820635 / 2131820815 / 2131820648-2131820655)"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置「无障碍 → 已安装的服务」页（Intent android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "弹窗 Positive 按钮「Enable」→ A0.s0#onClick 默认分支 → this.g.R(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Scratchpad Launcher via this service will not leave your device.",
      "shown_text_zh": "需要无障碍权限以启用「双击锁屏」手势。Scratchpad Launcher 通过该服务获取的任何数据都不会离开你的设备。",
      "user_action_requested": "在系统无障碍列表中手动找到并打开「Scratchpad Launcher」服务开关；应用无法代为开启，也无自动点击确认",
      "code_anchor": "A0.s0#onClick / res/xml/accessibility_service_config.xml (android:description=@string/accessibility_service_description)"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回设置页后的 SettingsFragment（Y() 刷新开关状态）",
      "trigger_event": "从系统设置返回、SettingsFragment#Y 或 I 回调刷新 SwitchCompat.setChecked(z)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅开关保持关闭状态，不弹任何二次提示）",
      "shown_text_zh": "无额外提示，开关维持未开启",
      "user_action_requested": "无强制动作，可正常使用其他桌面功能",
      "code_anchor": "app.olauncher.ui.SettingsFragment#Y / x0.b#q"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "app.olauncher.helper.MyAccessibilityService（独立进程 :serviceProcess）",
      "trigger_event": "系统绑定服务 → onServiceConnected() 写 SharedPreferences LOCK_MODE=true",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，静默写入开关状态",
      "user_action_requested": "无",
      "code_anchor": "app.olauncher.helper.MyAccessibilityService#onServiceConnected"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "桌面双击手势 → 锁屏控件点击 → MyAccessibilityService.onAccessibilityEvent",
      "trigger_event": "z0.c#onDoubleTap 检测到 LOCK_MODE=true 后调用 lockView.performClick()；服务收到 typeViewClicked 事件且 contentDescription==@string/lock_layout_description 时 performGlobalAction(8)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "lock layout description to be used a unique id to lock screen",
      "shown_text_zh": "用作锁屏唯一标识的布局描述",
      "user_action_requested": "用户在桌面双击即锁屏",
      "code_anchor": "z0.c#onDoubleTap / app.olauncher.helper.MyAccessibilityService#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "SettingsFragment 内 MaterialAlertDialog（非全屏、可取消）：标题 @string/gestures，正文 @string/accessibility_disclosure，Android 13+ 追加 @string/restricted_settings_hint",
    "系统无障碍服务列表项：android:label=@string/app_name（Scratchpad Launcher）与 android:description=@string/accessibility_service_description（来自 res/xml/accessibility_service_config.xml）",
    "设置页开关行文案：@string/please_turn_on_double_tap_to_unlock（Please turn on double tap to lock）",
    "「Not working?」按钮打开外部浏览器网页 https://tanujnotes.notion.site/Double-tap-to-lock-Olauncher-0f7fb103ec1f47d7a90cdfdcd7fb86ef（x0.b.y）",
    "设备管理员（仅 Android 9 以下锁屏路径）说明文案 @string/admin_permission_message（'Scratchpad Launcher promises to use the accessibility permission responsibly. Scratchpad Launcher does not collect or share any data.'）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Please turn on Scratchpad Launcher's accessibility service in your device's settings to enable Double tap to lock gesture. \n\nPlease note that this service is only used for this particular feature. Our accessibility service does not collect or share any data.",
      "text_zh": "请在设备设置中开启 Scratchpad Launcher 的无障碍服务，以启用「双击锁屏」手势。请注意该服务仅用于此特定功能，我们的无障碍服务不收集也不共享任何数据。",
      "source_location": "res/values/strings.xml key=accessibility_disclosure",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "If the switch is greyed out (Android 13+): open App info → ⋮ → Allow restricted settings, then try again.",
      "text_zh": "若开关置灰（Android 13+）：进入应用信息 → ⋮ → 允许受限设置，然后重试。",
      "source_location": "res/values/strings.xml key=restricted_settings_hint",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The accessibility permission is required to enable the gesture - double tap to lock . Any data acquired by Scratchpad Launcher via this service will not leave your device.",
      "text_zh": "需要无障碍权限以启用「双击锁屏」手势。Scratchpad Launcher 通过该服务获取的任何数据都不会离开你的设备。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Please turn on double tap to lock",
      "text_zh": "请开启双击锁屏",
      "source_location": "res/values/strings.xml key=please_turn_on_double_tap_to_unlock",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Scratchpad Launcher promises to use the accessibility permission responsibly. Scratchpad Launcher does not collect or share any data.",
      "text_zh": "Scratchpad Launcher 承诺负责任地使用无障碍权限，不收集也不共享任何数据。",
      "source_location": "res/values/strings.xml key=admin_permission_message（Android 9 以下设备管理员路径 ADD_EXPLANATION）",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。返回设置页后仅由 SettingsFragment#Y() 依据 LOCK_MODE 与 x0.b#q() 刷新开关勾选状态，开关保持关闭；MainActivity.onResume 只重置内部标志，不重跳设置页、不弹二次提示",
    "overlay_or_fake_settings": "无。未使用 TYPE_APPLICATION_OVERLAY/SYSTEM_ALERT_WINDOW，无半透明遮罩或高仿无障碍开关页；引导仅为一个可取消的原生 AlertDialog",
    "restricted_settings_13plus_coaching": "有，但为透明说明：SDK_INT>=33 时弹窗正文追加 restricted_settings_hint（App info → ⋮ → Allow restricted settings 后重试）；未使用 Session 安装器绕过",
    "post_grant_anti_removal": "无。服务无 GLOBAL_ACTION_BACK/HOME 撤权阻止、无自点确认、无监听设置页行为；onAccessibilityEvent 仅匹配 contentDescription==lock_layout_description 时执行 performGlobalAction(8) 锁屏",
    "benign_graceful_degradation": "有。关闭/取消弹窗后桌面其余功能（搜索、抽屉、便签）正常可用；Android 9 以下自动改用 DeviceAdmin（ADD_DEVICE_ADMIN, requestCode 666）实现锁屏，Android 10+ 才走无障碍路径"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "无需冷启动即拉起：先手动进入设置页点击「Double tap to lock」开关（或长按该行）捕获弹窗，再点 Enable 时以监测到 Activity 切换至 com.android.settings/.Settings$AccessibilitySettings（或 intent=android.settings.ACCESSIBILITY_SETTINGS）为拉起时机",
    "key_pages_to_capture": [
      {
        "page_role": "触发前的应用设置页（对照页）",
        "page_identifier": "app.scratchpad.launcher 设置页，含文本 'Please turn on double tap to lock' 与 Switch 控件",
        "why_most_useful": "确认引导不是冷启动强制弹出，而是用户点该功能开关后才出现，用于区分 on-demand 与 cold_start_block",
        "observable_utg_signals": ["当前包名 app.scratchpad.launcher 且非系统设置", "页面存在 'Please turn on double tap to lock' 文本节点", "无弹窗/无遮罩节点"]
      },
      {
        "page_role": "无障碍引导弹窗页",
        "page_identifier": "标题 'Gestures' 的 AlertDialog，按钮 'Close' / 'Not working?' / 'Enable'",
        "why_most_useful": "该页是全部说明文字的唯一载体，可直接判定是否存在恐吓、假更新、教唆忽视警告等话术，并验证取消路径是否存在",
        "observable_utg_signals": ["弹窗正文包含 'does not collect or share any data' 隐私承诺", "存在 Close 取消按钮（可取消性）", "按钮文本 Enable/Close/Not working?", "无虚假系统弹窗样式（非 Settings 包名）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍服务列表中的 'Scratchpad Launcher' 条目及其 description 文本",
        "why_most_useful": "核对服务名与描述是否与应用身份一致、有无空白/同形字伪装",
        "observable_utg_signals": ["服务标签恰为 'Scratchpad Launcher'", "description 含 'will not leave your device'", "无重复相似条目/多 alias"]
      },
      {
        "page_role": "获权后返回的应用设置页",
        "page_identifier": "设置页开关变为已选中状态",
        "why_most_useful": "验证拒权不重跳、获权后状态刷新为真实值而非强制置真",
        "observable_utg_signals": ["返回后无新弹窗", "Switch 状态与系统实际开启状态一致"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一需注意：Android 9 以下锁屏路径会触发 DeviceAdmin（android.app.action.ADD_DEVICE_ADMIN）系统页，属功能替代实现而非权限诱导，UTG 侧应区分处理；外部帮助链接指向浏览器网页，非应用内 WebView 引导。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "app.olauncher.ui.SettingsFragment#onClick",
    "A0.s0#onClick",
    "x0.b#q",
    "app.olauncher.helper.MyAccessibilityService#onServiceConnected",
    "app.olauncher.helper.MyAccessibilityService#onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
