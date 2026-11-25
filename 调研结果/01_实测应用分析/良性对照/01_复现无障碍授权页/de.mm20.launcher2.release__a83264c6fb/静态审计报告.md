# BN_037__a83264c6fb｜极简桌面与双击锁屏 — Kvaesitso

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：114.2s

## 1. 一句话核心结论

- **核心申请方式**：用户主动使用锁屏/通知栏/最近任务等需要无障碍的手势时，弹出可关闭的原生 Compose 底部说明弹层，点击后才跳转 android.settings.ACCESSIBILITY_SETTINGS，无冷启动打扰、无拒绝循环、无防撤权行为。
- **静态可见性说明**：无障碍引导链完整静态可见：触发点、弹层文案、跳转 Intent、服务配置均在 DEX 与 res/xml/accessibility_service.xml、res/values/strings.xml 中明文可读，无加壳、无加密资产、无远端 HTML 或 WebView 承载的引导页。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a83264c6fb437aad083c61206a4e79dba555300dbd4578fa17c0c43f55798739` |
| 包名 / 年份 | `de.mm20.launcher2.release` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/de.mm20.launcher2.release_2026091500.apk |
| 桌面显示名 | Kvaesitso |
| 引导页宣称品牌/身份 | Kvaesitso（开源启动器，真实身份，无伪装对象） |
| 系统无障碍列表服务名 | Kvaesitso（服务未声明 android:label/android:description，系统无障碍列表回落到应用名，无功能说明文本） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `de.mm20.launcher2.globalactions.LauncherAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, REQUEST_INSTALL_PACKAGES` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | de.mm20.launcher2.ui.launcher.LauncherActivity（HOME/LAUNCHER，singleTask） | 用户按 Home 或点图标启动 | 原生Activity | 无 | 无（不涉及无障碍申请） | `de.mm20.launcher2.ui.launcher.LauncherActivity` |
| 2 | 业务功能触发 | ScreenOffComponent / PowerMenuComponent / RecentsComponent 的手势处理协程 | 用户执行已绑定为「Turn off screen / Power menu / Recent apps / Notifications / Quick settings」的双击或滑动等手势（LauncherScaffoldState.getCurrentGesture） | 原生Activity | 无 | 无（后台判定） | `de.mm20.launcher2.ui.launcher.scaffold.components.ScreenOffComponent$Component$1$1#invokeSuspend` |
| 3 | 引导说明页 | FailedGestureSheet（Compose DismissableBottomSheet 底部弹层）+ MissingPermissionBanner | checkPermissionOnce(PermissionGroup.Accessibility) 返回 false → LauncherBottomSheetManager.showFailedGestureSheet(currentGesture, action) | 原生Dialog | **原文**：You have performed a "%1$s" gesture. This gesture is currently set to trigger a "%2$s" action. However, the action could not be performed for the following reason: / The launcher's accessibility service needs to be enabled to perform this action.<br>**译注**：你执行了「双击」手势，该手势当前设置为触发「关闭屏幕」动作，但动作无法执行，原因如下：需要启用启动器的无障碍服务才能执行此操作。 | 点击横幅按钮前往开启；弹层本身可下滑/点击空白关闭（DismissableBottomSheet），无强制停留 | `de.mm20.launcher2.ui.launcher.sheets.FailedGestureSheetKt#$r8$lambda$M4i3i3Rikxsp2NJejpFJuobC_0E / de.mm20.launcher2.ui.component.MissingPermissionBannerKt#MissingPermissionBanner` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | 用户点击 MissingPermissionBanner 按钮 → FailedGestureSheetKt$$ExternalSyntheticLambda4 → FailedGestureSheetVM.requestPermission(Activity) → PermissionsManagerImpl.requestPermission case 9 | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：系统无障碍设置列表，用户需在其中找到 Kvaesitso 并手动开启服务 | 用户自行在系统页开启服务（无诱导文案、无自动点击） | `de.mm20.launcher2.permissions.PermissionsManagerImpl#requestPermission` |
| 5 | 业务功能触发（设置页路径） | de.mm20.launcher2.ui.settings.SettingsActivity → GestureSettingsScreen 手势设置项 | 用户进入设置-手势，点击被 GuardedPreference 包裹的需无障碍手势项 | 原生Activity | **原文**：This action requires the launcher's accessibility service to be enabled.<br>**译注**：此操作需要启用启动器的无障碍服务。 | 点击后同样跳转 ACCESSIBILITY_SETTINGS；可放弃不设置 | `de.mm20.launcher2.ui.settings.gestures.GestureSettingsScreenKt#GestureSettingsScreen$lambda$4$0$0$0` |
| 6 | 获权后动作 | de.mm20.launcher2.globalactions.LauncherAccessibilityService / GlobalActionsService | 用户在系统页开启服务 → onServiceConnected() | 系统无障碍页 | 无 | 无 | `de.mm20.launcher2.globalactions.LauncherAccessibilityService#onServiceConnected / de.mm20.launcher2.globalactions.GlobalActionsService#lockScreen` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- LauncherActivity 内的 Compose 底部弹层 FailedGestureSheet（可关闭的 DismissableBottomSheet，仅在用户执行需无障碍的手势失败后出现）
- 该弹层内的 MissingPermissionBanner 横幅（lock_24px 图标 + 说明文字 + 前往开启按钮）
- 设置页 GestureSettingsScreen 中每个需无障碍手势项下方的 GuardedPreference 提示文案
- 系统无障碍列表中的服务条目：无 android:label / android:description，仅显示应用名 Kvaesitso，无额外说明文字
- res/values/strings.xml 中的字符串资源（gesture_failed_message、missing_permission_accessibility_gesture_failed、missing_permission_accessibility_gesture_settings）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | The launcher's accessibility service needs to be enabled to perform this action. | 需要启用启动器的无障碍服务才能执行此操作。 | `res/values/strings.xml key: missing_permission_accessibility_gesture_failed` | 良性透明说明 |
| en | This action requires the launcher's accessibility service to be enabled. | 此操作需要启用启动器的无障碍服务。 | `res/values/strings.xml key: missing_permission_accessibility_gesture_settings` | 良性透明说明 |
| en | You have performed a "%1$s" gesture. This gesture is currently set to trigger a "%2$s" action. However, the action could not be performed for the following reason: | 你执行了「%1$s」手势，该手势当前设置为触发「%2$s」动作，但动作因以下原因无法执行： | `res/values/strings.xml key: gesture_failed_message` | 良性透明说明 |
| en | Turn off screen | 关闭屏幕 | `res/values/strings.xml key: gesture_action_lock_screen` | 良性透明说明 |
| en | Notifications | 通知栏 | `res/values/strings.xml key: gesture_action_notifications` | 良性透明说明 |
| en | Quick settings | 快捷设置 | `res/values/strings.xml key: gesture_action_quick_settings` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。跳转后仅将 PermissionGroup.Accessibility 加入 pendingPermissionRequests；返回应用不自动重跳，无 onResume 死循环、无定时器拉起，手势保持不可用状态，用户可再次主动触发
- **遮罩叠层 / 高仿系统设置页**：无。弹层为应用内 Compose 底部弹层，跳转后不叠任何遮罩/悬浮窗，也无高仿系统无障碍开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅上报状态，onAccessibilityEvent/onInterrupt 为空实现，仅使用 performGlobalAction 3/4/5/6/8，不含 GLOBAL_ACTION_BACK/HOME 阻止撤权
- **良性降级 / 替代方案**：有。未授权时仅对应手势功能不可用（提示后返回桌面），其余搜索、应用抽屉、桌面管理等功能不受影响；用户亦可仅使用无需无障碍的手势动作

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 LauncherActivity 前台时注入手势（双击屏幕中央，默认绑定 Turn off screen）或监控 Intent 为 android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 瞬间；两者任一时机即可捕获完整引导链
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区。唯一需注意：系统无障碍条目无 android:description，纯文本 UTG 可能取不到服务说明字段，需结合服务名与页面文案判定；另外 isAccessibilityTool="false" 会使 Android 13+ 系统页显示系统级警告，此为系统行为而非应用诱导，不应误判为教唆忽视警告。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **手势失败后的引导弹层页（核心判别页）** | LauncherActivity 上的 Compose BottomSheet，含文本 You have performed a "Double tap" gesture... 与 The launcher's accessibility service needs to be enabled to perform this action. 及锁形图标横幅按钮 | 该页是唯一呈现无障碍申请理由的界面，可直接判定是否存在恐吓/伪装/不可取消等诱导特征 | 弹层文本节点是否为真实功能说明而非安全/故障恐吓；是否存在关闭/下滑取消入口；是否叠放半透明遮罩或伪造系统开关控件；按钮文本与目标是否为系统无障碍设置 |
| **系统无障碍服务列表项** | 设置 > 无障碍 > 已下载的服务，条目显示 Kvaesitso | 核对服务标签与描述是否与真实功能一致，是否存在空白标签/同形字伪装 | 服务名是否为应用真名且无空白/换行填充；描述字段是否为空或伪造；是否出现多条目 alias 诱导 |
| **设置-手势页的权限守卫提示** | SettingsActivity > Gestures 页中被 GuardedPreference 包裹的手势项及其提示文案 | 验证引导仅为功能按需触发，而非冷启动或后台反复打扰 | 提示文案是否与缺失权限严格对应；未授权时手势项是否仍可浏览并放弃设置 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `de.mm20.launcher2.permissions.PermissionsManagerImpl#requestPermission`
- `de.mm20.launcher2.ui.launcher.sheets.FailedGestureSheetVM#requestPermission`
- `de.mm20.launcher2.ui.launcher.sheets.FailedGestureSheetKt#$r8$lambda$M4i3i3Rikxsp2NJejpFJuobC_0E`
- `de.mm20.launcher2.ui.launcher.scaffold.components.ScreenOffComponent$Component$1$1#invokeSuspend`
- `de.mm20.launcher2.ui.settings.gestures.GestureSettingsScreenKt#GestureSettingsScreen$lambda$4$0$0$0`
- `res/xml/accessibility_service.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**静态可见性：完全可见（clear）** — 无障碍逻辑全部位于 DEX 与本地 XML 资源中，无加壳、无 WebView/远端 HTML、无动态载荷。

**引导链（纯运行期 UTG 视角）**

1. **冷启动阶段没有任何无障碍相关行为**：`LauncherActivity`（HOME/LAUNCHER）仅作桌面渲染，未见 `onCreate`/`onResume` 检查或弹窗拉起无障碍设置。
2. **触发点为“用户主动使用需要无障碍的手势功能”**：`ScreenOffComponent`、`PowerMenuComponent`、`RecentsComponent` 在手势激活时先 `checkPermissionOnce(PermissionGroup.Accessibility)`；返回 false 才调用 `LauncherBottomSheetManager.showFailedGestureSheet(...)`。
3. **提示载体是原生 Compose 底部弹层（可关闭）**：`FailedGestureSheet` 由 `DismissableBottomSheet` 承载，含手势/动作说明文案 + `MissingPermissionBanner`（带图标与按钮），非全屏、非悬浮窗、非高仿系统页。
4. **点击按钮才跳系统无障碍页**：[FailedGestureSheetVM.requestPermission()](<resource-unit:#1.dex1 code:de.mm20.launcher2.ui.launcher.sheets.FailedGestureSheetVM#requestPermission>) → [PermissionsManagerImpl.requestPermission()](<resource-unit:#1.dex1 code:de.mm20.launcher2.permissions.PermissionsManagerImpl#requestPermission>) 的 `case 9` 直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，并登记 `pendingPermissionRequests`。
5. **设置页内同样路径**：`GestureSettingsScreen` 用 `GuardedPreference` 包裹需无障碍的手势项，点击时以同一 `missing_permission_accessibility_gesture_settings` 文案引导并跳转。
6. **拒绝/返回后没有任何循环**：跳转后仅记录 pending；无 `onResume` 重跳、无定时器拉起、无叠层遮罩。用户不授权则该手势保持不可用，属正常降级。
7. **获权后无防撤权动作**：[LauncherAccessibilityService.onServiceConnected()](<resource-unit:#1.dex1 code:de.mm20.launcher2.globalactions.LauncherAccessibilityService#onServiceConnected>) 仅上报状态；`onAccessibilityEvent`、`onInterrupt` 均为空实现；`GlobalActionsService` 只用 `performGlobalAction(3/4/5/6/8)`（Recents/通知栏/快捷设置/电源菜单/锁屏），**无 GLOBAL_ACTION_BACK(1)/HOME(2)**，不存在自点确认或阻止撤权。

**身份一致性**：服务声明无 `android:label`、无 `android:description`，`@xml/accessibility_service` 中 `accessibilityEventTypes=""`、`canRetrieveWindowContent="false"`、`isAccessibilityTool="false"`，系统列表显示应用名 `Kvaesitso`，功能范围（手势触发系统动作）与描述一致，无同形字/多 alias/空白挤出/伪造 `isAccessibilityTool`。

**结论**：该应用属于**功能按需（feature-on-demand）良性引导**，文案透明、载体为原生可取消弹层、无恐吓/伪装/拒绝循环，未发现诱导或滥用无障碍的行为。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链完整静态可见：触发点、弹层文案、跳转 Intent、服务配置均在 DEX 与 res/xml/accessibility_service.xml、res/values/strings.xml 中明文可读，无加壳、无加密资产、无远端 HTML 或 WebView 承载的引导页。",
  "summary_one_liner": "用户主动使用锁屏/通知栏/最近任务等需要无障碍的手势时，弹出可关闭的原生 Compose 底部说明弹层，点击后才跳转 android.settings.ACCESSIBILITY_SETTINGS，无冷启动打扰、无拒绝循环、无防撤权行为。",
  "disguise_identity": {
    "app_display_name": "Kvaesitso",
    "claimed_brand_or_persona": "Kvaesitso（开源启动器，真实身份，无伪装对象）",
    "a11y_service_label": "Kvaesitso（服务未声明 android:label/android:description，系统无障碍列表回落到应用名，无功能说明文本）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "de.mm20.launcher2.ui.launcher.LauncherActivity（HOME/LAUNCHER，singleTask）",
      "trigger_event": "用户按 Home 或点图标启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动直接进入桌面，无任何权限提示",
      "user_action_requested": "无（不涉及无障碍申请）",
      "code_anchor": "de.mm20.launcher2.ui.launcher.LauncherActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "ScreenOffComponent / PowerMenuComponent / RecentsComponent 的手势处理协程",
      "trigger_event": "用户执行已绑定为「Turn off screen / Power menu / Recent apps / Notifications / Quick settings」的双击或滑动等手势（LauncherScaffoldState.getCurrentGesture）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "手势被识别后先检查无障碍是否已授权",
      "user_action_requested": "无（后台判定）",
      "code_anchor": "de.mm20.launcher2.ui.launcher.scaffold.components.ScreenOffComponent$Component$1$1#invokeSuspend"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "FailedGestureSheet（Compose DismissableBottomSheet 底部弹层）+ MissingPermissionBanner",
      "trigger_event": "checkPermissionOnce(PermissionGroup.Accessibility) 返回 false → LauncherBottomSheetManager.showFailedGestureSheet(currentGesture, action)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "You have performed a \"%1$s\" gesture. This gesture is currently set to trigger a \"%2$s\" action. However, the action could not be performed for the following reason: / The launcher's accessibility service needs to be enabled to perform this action.",
      "shown_text_zh": "你执行了「双击」手势，该手势当前设置为触发「关闭屏幕」动作，但动作无法执行，原因如下：需要启用启动器的无障碍服务才能执行此操作。",
      "user_action_requested": "点击横幅按钮前往开启；弹层本身可下滑/点击空白关闭（DismissableBottomSheet），无强制停留",
      "code_anchor": "de.mm20.launcher2.ui.launcher.sheets.FailedGestureSheetKt#$r8$lambda$M4i3i3Rikxsp2NJejpFJuobC_0E / de.mm20.launcher2.ui.component.MissingPermissionBannerKt#MissingPermissionBanner"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户点击 MissingPermissionBanner 按钮 → FailedGestureSheetKt$$ExternalSyntheticLambda4 → FailedGestureSheetVM.requestPermission(Activity) → PermissionsManagerImpl.requestPermission case 9",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "系统无障碍设置列表，用户需在其中找到 Kvaesitso 并手动开启服务",
      "user_action_requested": "用户自行在系统页开启服务（无诱导文案、无自动点击）",
      "code_anchor": "de.mm20.launcher2.permissions.PermissionsManagerImpl#requestPermission"
    },
    {
      "step": 5,
      "stage": "业务功能触发（设置页路径）",
      "screen_or_component": "de.mm20.launcher2.ui.settings.SettingsActivity → GestureSettingsScreen 手势设置项",
      "trigger_event": "用户进入设置-手势，点击被 GuardedPreference 包裹的需无障碍手势项",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "This action requires the launcher's accessibility service to be enabled.",
      "shown_text_zh": "此操作需要启用启动器的无障碍服务。",
      "user_action_requested": "点击后同样跳转 ACCESSIBILITY_SETTINGS；可放弃不设置",
      "code_anchor": "de.mm20.launcher2.ui.settings.gestures.GestureSettingsScreenKt#GestureSettingsScreen$lambda$4$0$0$0"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "de.mm20.launcher2.globalactions.LauncherAccessibilityService / GlobalActionsService",
      "trigger_event": "用户在系统页开启服务 → onServiceConnected()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "仅记录 instance 与上报状态，随后手势通过 performGlobalAction 执行系统动作",
      "user_action_requested": "无",
      "code_anchor": "de.mm20.launcher2.globalactions.LauncherAccessibilityService#onServiceConnected / de.mm20.launcher2.globalactions.GlobalActionsService#lockScreen"
    }
  ],
  "text_presentation_locations": [
    "LauncherActivity 内的 Compose 底部弹层 FailedGestureSheet（可关闭的 DismissableBottomSheet，仅在用户执行需无障碍的手势失败后出现）",
    "该弹层内的 MissingPermissionBanner 横幅（lock_24px 图标 + 说明文字 + 前往开启按钮）",
    "设置页 GestureSettingsScreen 中每个需无障碍手势项下方的 GuardedPreference 提示文案",
    "系统无障碍列表中的服务条目：无 android:label / android:description，仅显示应用名 Kvaesitso，无额外说明文字",
    "res/values/strings.xml 中的字符串资源（gesture_failed_message、missing_permission_accessibility_gesture_failed、missing_permission_accessibility_gesture_settings）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "The launcher's accessibility service needs to be enabled to perform this action.",
      "text_zh": "需要启用启动器的无障碍服务才能执行此操作。",
      "source_location": "res/values/strings.xml key: missing_permission_accessibility_gesture_failed",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This action requires the launcher's accessibility service to be enabled.",
      "text_zh": "此操作需要启用启动器的无障碍服务。",
      "source_location": "res/values/strings.xml key: missing_permission_accessibility_gesture_settings",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "You have performed a \"%1$s\" gesture. This gesture is currently set to trigger a \"%2$s\" action. However, the action could not be performed for the following reason:",
      "text_zh": "你执行了「%1$s」手势，该手势当前设置为触发「%2$s」动作，但动作因以下原因无法执行：",
      "source_location": "res/values/strings.xml key: gesture_failed_message",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn off screen",
      "text_zh": "关闭屏幕",
      "source_location": "res/values/strings.xml key: gesture_action_lock_screen",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Notifications",
      "text_zh": "通知栏",
      "source_location": "res/values/strings.xml key: gesture_action_notifications",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Quick settings",
      "text_zh": "快捷设置",
      "source_location": "res/values/strings.xml key: gesture_action_quick_settings",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。跳转后仅将 PermissionGroup.Accessibility 加入 pendingPermissionRequests；返回应用不自动重跳，无 onResume 死循环、无定时器拉起，手势保持不可用状态，用户可再次主动触发",
    "overlay_or_fake_settings": "无。弹层为应用内 Compose 底部弹层，跳转后不叠任何遮罩/悬浮窗，也无高仿系统无障碍开关页",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。onServiceConnected 仅上报状态，onAccessibilityEvent/onInterrupt 为空实现，仅使用 performGlobalAction 3/4/5/6/8，不含 GLOBAL_ACTION_BACK/HOME 阻止撤权",
    "benign_graceful_degradation": "有。未授权时仅对应手势功能不可用（提示后返回桌面），其余搜索、应用抽屉、桌面管理等功能不受影响；用户亦可仅使用无需无障碍的手势动作"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 LauncherActivity 前台时注入手势（双击屏幕中央，默认绑定 Turn off screen）或监控 Intent 为 android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 瞬间；两者任一时机即可捕获完整引导链",
    "key_pages_to_capture": [
      {
        "page_role": "手势失败后的引导弹层页（核心判别页）",
        "page_identifier": "LauncherActivity 上的 Compose BottomSheet，含文本 You have performed a \"Double tap\" gesture... 与 The launcher's accessibility service needs to be enabled to perform this action. 及锁形图标横幅按钮",
        "why_most_useful": "该页是唯一呈现无障碍申请理由的界面，可直接判定是否存在恐吓/伪装/不可取消等诱导特征",
        "observable_utg_signals": ["弹层文本节点是否为真实功能说明而非安全/故障恐吓", "是否存在关闭/下滑取消入口", "是否叠放半透明遮罩或伪造系统开关控件", "按钮文本与目标是否为系统无障碍设置"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 > 无障碍 > 已下载的服务，条目显示 Kvaesitso",
        "why_most_useful": "核对服务标签与描述是否与真实功能一致，是否存在空白标签/同形字伪装",
        "observable_utg_signals": ["服务名是否为应用真名且无空白/换行填充", "描述字段是否为空或伪造", "是否出现多条目 alias 诱导"]
      },
      {
        "page_role": "设置-手势页的权限守卫提示",
        "page_identifier": "SettingsActivity > Gestures 页中被 GuardedPreference 包裹的手势项及其提示文案",
        "why_most_useful": "验证引导仅为功能按需触发，而非冷启动或后台反复打扰",
        "observable_utg_signals": ["提示文案是否与缺失权限严格对应", "未授权时手势项是否仍可浏览并放弃设置"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区。唯一需注意：系统无障碍条目无 android:description，纯文本 UTG 可能取不到服务说明字段，需结合服务名与页面文案判定；另外 isAccessibilityTool=\"false\" 会使 Android 13+ 系统页显示系统级警告，此为系统行为而非应用诱导，不应误判为教唆忽视警告。"
  },
  "behavior_pattern_tags": ["TRIG_FEATURE_ON_DEMAND", "CARRIER_NATIVE_DIALOG_OR_ACTIVITY", "CARRIER_SYSTEM_A11Y_DESCRIPTION", "BENIGN_TRANSPARENT_RATIONALE", "BENIGN_EXPLICIT_CANCEL_DEGRADATION", "BENIGN_HONEST_IDENTITY_AND_SCOPE", "BENIGN_ALTERNATIVE_MODE_OFFERED"],
  "code_anchors": [
    "de.mm20.launcher2.permissions.PermissionsManagerImpl#requestPermission",
    "de.mm20.launcher2.ui.launcher.sheets.FailedGestureSheetVM#requestPermission",
    "de.mm20.launcher2.ui.launcher.sheets.FailedGestureSheetKt#$r8$lambda$M4i3i3Rikxsp2NJejpFJuobC_0E",
    "de.mm20.launcher2.ui.launcher.scaffold.components.ScreenOffComponent$Component$1$1#invokeSuspend",
    "de.mm20.launcher2.ui.settings.gestures.GestureSettingsScreenKt#GestureSettingsScreen$lambda$4$0$0$0",
    "res/xml/accessibility_service.xml"
  ]
}
```

</details>
