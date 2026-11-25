# BN_052__e5938503b3｜系统效率与通用辅助 — Middor

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：108.4s

## 1. 一句话核心结论

- **核心申请方式**：Middor 在设置页的 Permissions 区以「Request」按钮按需跳转系统无障碍设置，文案透明说明仅用于手势回放、可跳过且提供仅观看降级，无强制弹窗、无遮罩、无拒绝循环，属良性开源无障碍申请流程。
- **静态可见性说明**：全部关键证据静态可见：无障碍跳转 intent（android.settings.ACCESSIBILITY_SETTINGS）、悬浮窗与应用详情跳转（MANAGE_OVERLAY_PERMISSION / APPLICATION_DETAILS_SETTINGS）均在 r41.a / r3.a 协程状态机中明文可见；全部引导文案在 res/values/strings.xml 明文；assets 仅有 dexopt 目录，无 HTML/WebView/远端页面，无加壳或加密载荷。仅 Compose 页面组合位于 R8 混淆导航图中，无法逐页命名，但不影响行为判定。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e5938503b3ef4e591c7101839c2d68c94dc3642ed7dfaf8095ad346c7dbe69f4` |
| 包名 / 年份 | `org.nktnet.middor` / 2025-2026 |
| 家族 / 品类 | **系统效率与通用辅助**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/org.nktnet.middor_9.apk |
| 桌面显示名 | Middor |
| 引导页宣称品牌/身份 | Middor（F-Droid 开源 HUD 镜像/水平翻转工具） |
| 系统无障碍列表服务名 | Middor Touch |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。无空白/换行挤出警告、无同形字、无多 activity-alias；无障碍配置显式 android:isAccessibilityTool="false"，未伪造无障碍工具身份。 |
| 无障碍服务类名 | `org.nktnet.middor.services.MirrorInputService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Enables touch controls by intercepting and replaying your gestures while mirroring. Does not read accessibility window content or store or share gesture data. Turn off touch controls or this service to stop replay. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | org.nktnet.middor.MainActivity（LAUNCHER，singleTask，Compose 单 Activity） | onCreate（系统点击图标启动） | 原生Activity | **原文**：Start Mirror Display Overlay / Instructions / Help<br>**译注**：开始镜像悬浮显示 / 使用说明 / 帮助 | 无强制操作；首页为功能入口，可自由浏览或退出（无权限阻塞） | `org.nktnet.middor.MainActivity.onCreate；res/values/strings.xml button_start_mirror_display / instructions_title / help_title` |
| 2 | 业务功能触发 | 设置页 Permissions 分区（settings_permissions_title），Accessibility 行（settings_accessibility_permission_label） | 用户主动进入 Settings 并点击 Request（settings_request_text_button） | 原生Activity | **原文**：Accessibility<br>Enable Middor Touch in Android Accessibility settings for touch controls. Not needed for view-only mirroring. If it stops working after an update, turn it off and on.<br>Request<br>**译注**：无障碍<br>在 Android 无障碍设置中启用 Middor Touch 以使用触控；仅观看镜像不需要。若更新后失效，请关闭再重新开启。<br>申请 | 点击 Request 按钮发起跳转；也可不点、不开启，继续使用仅观看模式 | `res/values/strings.xml settings_accessibility_permission_label / settings_accessibility_permission_info / settings_request_text_button / settings_granted_text_button` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（应用无障碍服务列表，含 Middor Touch） | Request 点击触发的协程 lambda 执行 startActivity | 系统无障碍页 | **原文**：Middor Touch<br>Enables touch controls by intercepting and replaying your gestures while mirroring. Does not read accessibility window content or store or share gesture data. Turn off touch controls or this service to stop replay.<br>**译注**：Middor Touch<br>在镜像期间通过拦截并回放你的手势来启用触控。不读取无障碍窗口内容，不存储也不共享手势数据。关闭触控功能或本服务即可停止回放。 | 在系统无障碍列表中手动找到并开启 Middor Touch（由系统 UI 控制，应用不代点、不监听） | `r41.a → new Intent("android.settings.ACCESSIBILITY_SETTINGS").startActivity；res/xml/mirror_accessibility_service.xml（accessibilityEventTypes=typeTouchInteractionEnd\|typeTouchInteractionStart, canRetrieveWindowContent=false, canPerformGestures=true, isAccessibilityTool=false）` |
| 4 | 跳受限设置 | 系统设置页 android.settings.action.MANAGE_OVERLAY_PERMISSION（package:org.nktnet.middor） | Overlay 行 Request 点击触发的协程 lambda | 系统无障碍页 | **原文**：Overlay<br>Required to show the mirror over other apps.<br>Request<br>**译注**：悬浮窗<br>用于在其他应用之上显示镜像。<br>申请 | 用户可在系统页授予悬浮窗权限；未授予时仅提示 settings_accessibility_overlay_error | `r3.a → Intent("android.settings.action.MANAGE_OVERLAY_PERMISSION", Uri.parse("package:org.nktnet.middor"))；res/values/strings.xml settings_overlay_permission_label / settings_overlay_permission_info` |
| 5 | 跳受限设置 | 系统应用详情页 android.settings.APPLICATION_DETAILS_SETTINGS（package:org.nktnet.middor） | 设置页 App Info（settings_app_info）点击 | 系统无障碍页 | **原文**：App Info<br>**译注**：应用信息 | 仅打开本应用详情页供查看/调整权限，无任何“允许受限设置”的分步教唆文案 | `r3.a → Intent("android.settings.APPLICATION_DETAILS_SETTINGS").setData(Uri.fromParts("package", pkgName, null))；res/values/strings.xml settings_app_info` |
| 6 | 拒权反馈循环 | 返回应用后的设置页/主页状态提示（Compose 内联文本，非弹窗） | 从系统设置返回后按无障碍连接状态刷新 UI | 原生Activity | **原文**：Middor Touch is unavailable. Check Accessibility.<br>Enable Middor Touch in Accessibility settings.<br>**译注**：Middor Touch 不可用，请检查无障碍设置。<br>请在无障碍设置中启用 Middor Touch。 | 仅作提示，可忽略继续使用仅观看镜像；无强制重跳、无不可取消弹窗、无遮罩叠层 | `res/values/strings.xml settings_accessibility_not_connected / settings_accessibility_permission_error；MirrorInputService 回调 ok0.onTouchExplorationStateChanged（仅状态观测，无重跳）` |
| 7 | 获权后动作 | org.nktnet.middor.services.MirrorInputService（无障碍服务）+ MirrorService（mediaProjection 前台服务） | 系统绑定 BIND_ACCESSIBILITY_SERVICE 后服务 onServiceConnected / onAccessibilityEvent | 原生Activity | **原文**：Enables touch controls by intercepting and replaying your gestures while mirroring. Does not read accessibility window content or store or share gesture data. Turn off touch controls or this service to stop replay.<br>**译注**：仅在镜像期间拦截并回放手势以实现触控，不读取窗口内容、不存储不共享手势数据；关闭触控或本服务即停止回放。 | 获权后仅回放手势；不阻止用户关闭服务，无 GLOBAL_ACTION_BACK/HOME 撤权对抗，无自授权 | `org.nktnet.middor.services.MirrorInputService.c / e（手势回放与 touch exploration 状态）；res/xml/mirror_accessibility_service.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项描述：android:description = res/values/strings.xml accessibility_service_description（经 res/xml/mirror_accessibility_service.xml 引用），系统设置页展示
- 系统无障碍列表服务名：res/values/strings.xml accessibility_service_label = "Middor Touch"，由 Manifest 的 service android:label 引用
- 应用内设置页 Permissions 分区：Accessibility 行标题 settings_accessibility_permission_label + 说明 settings_accessibility_permission_info + Request/Granted 按钮（settings_request_text_button / settings_granted_text_button）
- 应用内设置页 Permissions 分区：Overlay 行（settings_overlay_permission_label/info）、Notifications 行（settings_notifications_permission_label/info，标注 Optional）
- 应用内设置页触控开关说明：settings_touch_controls_label "Enable Touch Controls" + settings_touch_controls_note（明确“关闭即变为仅观看并阻止触控”）
- 应用内帮助页（Help）分步说明：help_overlay_note / help_overlay_step / help_notification_step / help_accessibility_step / help_start_button_step / help_single_app_step / help_select_app_step / help_exit_overlay_step
- 应用内状态提示（非弹窗，内联文本）：settings_accessibility_not_connected、settings_accessibility_permission_error、settings_accessibility_overlay_error、settings_touch_routing_error
- 系统悬浮窗权限页与应用详情页：由 MANAGE_OVERLAY_PERMISSION / APPLICATION_DETAILS_SETTINGS 跳转，文本由系统提供，应用未注入任何自定义引导文案
- 通知栏：notification_content_title "Mirror Display Overlay"、notification_exit_action "Exit"（用于退出镜像，非引导授权）
- 无 assets HTML/WebView、无悬浮遮罩引导窗、无伪造系统无障碍开关页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enables touch controls by intercepting and replaying your gestures while mirroring. Does not read accessibility window content or store or share gesture data. Turn off touch controls or this service to stop replay. | 在镜像期间通过拦截并回放你的手势来启用触控。不读取无障碍窗口内容，不存储也不共享手势数据。关闭触控功能或本服务即可停止回放。 | `res/values/strings.xml accessibility_service_description（经 res/xml/mirror_accessibility_service.xml android:description 引用）` | 隐私承诺 |
| en | Enable Middor Touch in Android Accessibility settings for touch controls. Not needed for view-only mirroring. If it stops working after an update, turn it off and on. | 在 Android 无障碍设置中启用 Middor Touch 以使用触控；仅观看镜像不需要。若更新后失效，请关闭再重新开启。 | `res/values/strings.xml settings_accessibility_permission_info` | 良性透明说明 |
| en | 3. For touch controls, enable Middor Touch in Android Accessibility settings. Skip this for view-only mirroring. | 3. 如需触控，请在 Android 无障碍设置中启用 Middor Touch。仅观看镜像可跳过此步。 | `res/values/strings.xml help_accessibility_step` | 受限设置分步教学 |
| en | Enable Middor Touch in Android Accessibility settings to tap and swipe the mirror. Gestures replay after you lift your fingers. Turning this off makes the mirror view-only and blocks touches to the hidden app. Restart to apply. | 在 Android 无障碍设置中启用 Middor Touch 后即可点击和滑动镜像。手势会在你抬指后回放。关闭此项后镜像变为仅观看，并阻止对被隐藏应用的触摸。重启后生效。 | `res/values/strings.xml settings_touch_controls_note` | 良性透明说明 |
| en | Middor Touch is unavailable. Check Accessibility. | Middor Touch 不可用，请检查无障碍设置。 | `res/values/strings.xml settings_accessibility_not_connected` | 良性透明说明 |
| en | Open Settings and grant %1$s the overlay permission. This is for displaying an overlay over other apps. | 打开设置并为 %1$s 授予悬浮窗权限，用于在其他应用之上显示悬浮层。 | `res/values/strings.xml help_overlay_step` | 受限设置分步教学 |
| en | To exit, tap on the red Close (×) icon in the configured corner of the overlay (top right by default). Alternatively, you can pull down on your status bar and tap the notification. | 退出时，点击悬浮层指定角落（默认右上角）的红色关闭（×）图标；也可以下拉状态栏并点击通知退出。 | `res/values/strings.xml help_exit_overlay_step` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。未授权或从系统设置返回后仅以内联文本提示（settings_accessibility_not_connected / settings_accessibility_permission_error），不自动重跳、无定时器拉起、无不可取消弹窗；用户可继续使用仅观看镜像。
- **遮罩叠层 / 高仿系统设置页**：无。未叠放半透明引导遮罩、无全屏悬浮窗引导、无高仿系统无障碍开关页；悬浮窗仅用于镜像显示本身。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。APPLICATION_DETAILS_SETTINGS 仅作为普通“App Info”入口，无“点右上角菜单允许受限设置”或 Session 安装器绕过等教唆文案。
- **获权后即时行为与防撤权机制**：无。无障碍服务仅监听 touchInteractionStart/End 并回放手势（canRetrieveWindowContent=false），未实现自点确认、自授权或 GLOBAL_ACTION_BACK/HOME 阻止撤权。
- **良性降级 / 替代方案**：有。明确提供仅观看模式：文案多处标注“Not needed for view-only mirroring / Skip this for view-only mirroring”，关闭触控后镜像仍可查看（仅阻止对被隐藏应用的触摸）。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测 startActivity 的 intent action 为 android.settings.ACCESSIBILITY_SETTINGS（由 r41.a 发起）或 MANAGE_OVERLAY_PERMISSION / APPLICATION_DETAILS_SETTINGS（由 r3.a 发起）的瞬间；以及冷启动 MainActivity 后进入 Settings → Permissions 分区的时刻。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。文本全为 strings.xml 明文字符串，无图片/纯图诱导；Compose 页面为原生节点，UTG 可正常取文本。唯一需注意：引导页组合在 R8 混淆导航图中，页面层级命名不可预期，应按文本内容而非类名匹配。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动入口页（MainActivity Compose 首页）** | org.nktnet.middor/.MainActivity，含 Start Mirror Display Overlay / Instructions / Help | 确认是否冷启动即弹不可取消引导；本应用此处无权限弹窗，可用于反证“0 步强制引导” | 首页无 Dialog/无障碍弹窗节点；存在可关闭的普通功能按钮；无悬浮窗遮罩层节点 |
| **跳转前应用内设置页 Permissions 分区** | Settings 页面含 Accessibility / Overlay / Notifications 行与 Request、Granted 按钮 | 判定引导是否由用户主动点 Request 触发（按需）且说明文案是否透明、是否含跳过/降级提示 | settings_accessibility_permission_info 全文可提取；Request 按钮可点击且存在返回/不操作路径；标注 Not needed for view-only mirroring |
| **系统无障碍服务列表项** | android.settings.ACCESSIBILITY_SETTINGS 中 "Middor Touch" 条目及其描述文本 | 核对服务名与描述是否如实（不读取窗口内容/不共享数据），并与桌面名 Middor 比对身份一致性 | 条目文本 Middor Touch；描述含 Does not read accessibility window content；条目由用户手动开关（应用无代点行为） |
| **拒权返回后的应用内反馈页** | 返回 MainActivity/Settings 后显示 Middor Touch is unavailable. Check Accessibility. | 验证是否存在拒绝循环（onResume 重跳/Timer 拉起）——本应用应停留原页并允许继续 | 无自动跳转系统设置页；无每秒重复弹窗/遮罩；仍可操作仅观看模式入口 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `r41.a（协程分支：new Intent("android.settings.ACCESSIBILITY_SETTINGS").startActivity）`
- `r3.a（Intent("android.settings.action.MANAGE_OVERLAY_PERMISSION", package:pkg) 与 Intent("android.settings.APPLICATION_DETAILS_SETTINGS", package:pkg)）`
- `org.nktnet.middor.MainActivity.onCreate`
- `org.nktnet.middor.services.MirrorInputService.c / MirrorInputService.e`
- `res/xml/mirror_accessibility_service.xml`
- `res/values/strings.xml#L3-L49`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，共 14 次工具调用后结束分析）

**静态可见性**：`clear`。应用只有 3 个自身类（`MainActivity`、`MirrorInputService`、`MirrorService`），其余为 R8 混淆后的 Compose/AndroidX 代码；`assets/` 下只有 `dexopt/`，**没有 HTML、WebView 或远端引导页**。无障碍相关文本全部在 [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3-L49>) 中明文可见，相关跳转点在混淆类 `r41.a`、`r3.a` 中可以直接定位。没有加壳、没有密文载荷，也没有动态下发。

**无障碍申请的引导链（运行期视角）**

1. **冷启动入口**：`MainActivity` 是唯一的 LAUNCHER Activity，使用 Compose 单 Activity，`onCreate` 中没有任何强制弹窗；没有在启动时直接跳到系统设置页的代码，也没有与 `SYSTEM_ALERT_WINDOW` 或无障碍相关的“先申请权限”阻塞逻辑。
2. **用户按需触发**：只有当用户点击界面上的 Request（`settings_request_text_button`）或操作触控开关时，才会进入下一步。
3. **跳转无障碍设置**：[r41.a()](<resource-unit:#1.dex1 code:r41#a>) 中的协程状态机分支构造了 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 并调用 `startActivity`。这是应用唯一的无障碍设置跳转点，位于协程 lambda 中，不会自动重跳。
4. **跳转悬浮窗设置**：[r3.a()](<resource-unit:#1.dex1 code:r3#a>) 构造了 `Intent("android.settings.action.MANAGE_OVERLAY_PERMISSION", package:<pkg>)`。
5. **跳转应用详情页**：同一个方法构造了 `Intent("android.settings.APPLICATION_DETAILS_SETTINGS", package:<pkg>)`，用途是“App Info”入口，没有用来教用户开启受限设置。
6. **拒绝授权后的反馈**：返回应用后，界面根据连接状态显示内联提示 `settings_accessibility_not_connected`“Middor Touch is unavailable. Check Accessibility.” 或 `settings_accessibility_permission_error`。**没有 onResume 死循环重跳，没有定时器，也没有悬浮遮罩层**。降级路径明确：仅观看模式（view-only）不要求开启无障碍。
7. **授权后的动作**：`MirrorInputService` 只监听 `typeTouchInteractionStart|End`，`canRetrieveWindowContent="false"`、`canPerformGestures="true"`、`isAccessibilityTool="false"`（按实际情况声明为非无障碍工具），没有自点确认、自授权或 `GLOBAL_ACTION_BACK/HOME` 阻止撤权的实现。

**关键文本框架**：全部为“良性透明说明 + 受限设置分步教学（可跳过）”，其中包含明确的隐私承诺（不读取窗口内容、不存储或共享手势数据）以及“关闭服务即可停止回放”的退出说明；`help_accessibility_step` 明确写“Skip this for view-only mirroring”。

**身份一致性**：桌面名称 `Middor` = `app_name`，无障碍列表标签 `Middor Touch`，来源为 F-Droid 开源，没有同形字、没有用空白字符把警告挤出视野，也没有多个 activity-alias 伪装。

**未决/边界**：Compose UI 的具体页面组合位于 R8 混淆后的导航图中，无法逐页静态命名（例如 Permissions 区的实际布局容器）；但由于所有文本资源和跳转 intent 都已确认，这不会影响判定。没有在线设备，因此未做运行期验证。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键证据静态可见：无障碍跳转 intent（android.settings.ACCESSIBILITY_SETTINGS）、悬浮窗与应用详情跳转（MANAGE_OVERLAY_PERMISSION / APPLICATION_DETAILS_SETTINGS）均在 r41.a / r3.a 协程状态机中明文可见；全部引导文案在 res/values/strings.xml 明文；assets 仅有 dexopt 目录，无 HTML/WebView/远端页面，无加壳或加密载荷。仅 Compose 页面组合位于 R8 混淆导航图中，无法逐页命名，但不影响行为判定。",
  "summary_one_liner": "Middor 在设置页的 Permissions 区以「Request」按钮按需跳转系统无障碍设置，文案透明说明仅用于手势回放、可跳过且提供仅观看降级，无强制弹窗、无遮罩、无拒绝循环，属良性开源无障碍申请流程。",
  "disguise_identity": {
    "app_display_name": "Middor",
    "claimed_brand_or_persona": "Middor（F-Droid 开源 HUD 镜像/水平翻转工具）",
    "a11y_service_label": "Middor Touch",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。无空白/换行挤出警告、无同形字、无多 activity-alias；无障碍配置显式 android:isAccessibilityTool=\"false\"，未伪造无障碍工具身份。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "org.nktnet.middor.MainActivity（LAUNCHER，singleTask，Compose 单 Activity）",
      "trigger_event": "onCreate（系统点击图标启动）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Start Mirror Display Overlay / Instructions / Help",
      "shown_text_zh": "开始镜像悬浮显示 / 使用说明 / 帮助",
      "user_action_requested": "无强制操作；首页为功能入口，可自由浏览或退出（无权限阻塞）",
      "code_anchor": "org.nktnet.middor.MainActivity.onCreate；res/values/strings.xml button_start_mirror_display / instructions_title / help_title"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "设置页 Permissions 分区（settings_permissions_title），Accessibility 行（settings_accessibility_permission_label）",
      "trigger_event": "用户主动进入 Settings 并点击 Request（settings_request_text_button）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility\nEnable Middor Touch in Android Accessibility settings for touch controls. Not needed for view-only mirroring. If it stops working after an update, turn it off and on.\nRequest",
      "shown_text_zh": "无障碍\n在 Android 无障碍设置中启用 Middor Touch 以使用触控；仅观看镜像不需要。若更新后失效，请关闭再重新开启。\n申请",
      "user_action_requested": "点击 Request 按钮发起跳转；也可不点、不开启，继续使用仅观看模式",
      "code_anchor": "res/values/strings.xml settings_accessibility_permission_label / settings_accessibility_permission_info / settings_request_text_button / settings_granted_text_button"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（应用无障碍服务列表，含 Middor Touch）",
      "trigger_event": "Request 点击触发的协程 lambda 执行 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Middor Touch\nEnables touch controls by intercepting and replaying your gestures while mirroring. Does not read accessibility window content or store or share gesture data. Turn off touch controls or this service to stop replay.",
      "shown_text_zh": "Middor Touch\n在镜像期间通过拦截并回放你的手势来启用触控。不读取无障碍窗口内容，不存储也不共享手势数据。关闭触控功能或本服务即可停止回放。",
      "user_action_requested": "在系统无障碍列表中手动找到并开启 Middor Touch（由系统 UI 控制，应用不代点、不监听）",
      "code_anchor": "r41.a → new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").startActivity；res/xml/mirror_accessibility_service.xml（accessibilityEventTypes=typeTouchInteractionEnd|typeTouchInteractionStart, canRetrieveWindowContent=false, canPerformGestures=true, isAccessibilityTool=false）"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置页 android.settings.action.MANAGE_OVERLAY_PERMISSION（package:org.nktnet.middor）",
      "trigger_event": "Overlay 行 Request 点击触发的协程 lambda",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Overlay\nRequired to show the mirror over other apps.\nRequest",
      "shown_text_zh": "悬浮窗\n用于在其他应用之上显示镜像。\n申请",
      "user_action_requested": "用户可在系统页授予悬浮窗权限；未授予时仅提示 settings_accessibility_overlay_error",
      "code_anchor": "r3.a → Intent(\"android.settings.action.MANAGE_OVERLAY_PERMISSION\", Uri.parse(\"package:org.nktnet.middor\"))；res/values/strings.xml settings_overlay_permission_label / settings_overlay_permission_info"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统应用详情页 android.settings.APPLICATION_DETAILS_SETTINGS（package:org.nktnet.middor）",
      "trigger_event": "设置页 App Info（settings_app_info）点击",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "App Info",
      "shown_text_zh": "应用信息",
      "user_action_requested": "仅打开本应用详情页供查看/调整权限，无任何“允许受限设置”的分步教唆文案",
      "code_anchor": "r3.a → Intent(\"android.settings.APPLICATION_DETAILS_SETTINGS\").setData(Uri.fromParts(\"package\", pkgName, null))；res/values/strings.xml settings_app_info"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回应用后的设置页/主页状态提示（Compose 内联文本，非弹窗）",
      "trigger_event": "从系统设置返回后按无障碍连接状态刷新 UI",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Middor Touch is unavailable. Check Accessibility.\nEnable Middor Touch in Accessibility settings.",
      "shown_text_zh": "Middor Touch 不可用，请检查无障碍设置。\n请在无障碍设置中启用 Middor Touch。",
      "user_action_requested": "仅作提示，可忽略继续使用仅观看镜像；无强制重跳、无不可取消弹窗、无遮罩叠层",
      "code_anchor": "res/values/strings.xml settings_accessibility_not_connected / settings_accessibility_permission_error；MirrorInputService 回调 ok0.onTouchExplorationStateChanged（仅状态观测，无重跳）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "org.nktnet.middor.services.MirrorInputService（无障碍服务）+ MirrorService（mediaProjection 前台服务）",
      "trigger_event": "系统绑定 BIND_ACCESSIBILITY_SERVICE 后服务 onServiceConnected / onAccessibilityEvent",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Enables touch controls by intercepting and replaying your gestures while mirroring. Does not read accessibility window content or store or share gesture data. Turn off touch controls or this service to stop replay.",
      "shown_text_zh": "仅在镜像期间拦截并回放手势以实现触控，不读取窗口内容、不存储不共享手势数据；关闭触控或本服务即停止回放。",
      "user_action_requested": "获权后仅回放手势；不阻止用户关闭服务，无 GLOBAL_ACTION_BACK/HOME 撤权对抗，无自授权",
      "code_anchor": "org.nktnet.middor.services.MirrorInputService.c / e（手势回放与 touch exploration 状态）；res/xml/mirror_accessibility_service.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项描述：android:description = res/values/strings.xml accessibility_service_description（经 res/xml/mirror_accessibility_service.xml 引用），系统设置页展示",
    "系统无障碍列表服务名：res/values/strings.xml accessibility_service_label = \"Middor Touch\"，由 Manifest 的 service android:label 引用",
    "应用内设置页 Permissions 分区：Accessibility 行标题 settings_accessibility_permission_label + 说明 settings_accessibility_permission_info + Request/Granted 按钮（settings_request_text_button / settings_granted_text_button）",
    "应用内设置页 Permissions 分区：Overlay 行（settings_overlay_permission_label/info）、Notifications 行（settings_notifications_permission_label/info，标注 Optional）",
    "应用内设置页触控开关说明：settings_touch_controls_label \"Enable Touch Controls\" + settings_touch_controls_note（明确“关闭即变为仅观看并阻止触控”）",
    "应用内帮助页（Help）分步说明：help_overlay_note / help_overlay_step / help_notification_step / help_accessibility_step / help_start_button_step / help_single_app_step / help_select_app_step / help_exit_overlay_step",
    "应用内状态提示（非弹窗，内联文本）：settings_accessibility_not_connected、settings_accessibility_permission_error、settings_accessibility_overlay_error、settings_touch_routing_error",
    "系统悬浮窗权限页与应用详情页：由 MANAGE_OVERLAY_PERMISSION / APPLICATION_DETAILS_SETTINGS 跳转，文本由系统提供，应用未注入任何自定义引导文案",
    "通知栏：notification_content_title \"Mirror Display Overlay\"、notification_exit_action \"Exit\"（用于退出镜像，非引导授权）",
    "无 assets HTML/WebView、无悬浮遮罩引导窗、无伪造系统无障碍开关页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enables touch controls by intercepting and replaying your gestures while mirroring. Does not read accessibility window content or store or share gesture data. Turn off touch controls or this service to stop replay.",
      "text_zh": "在镜像期间通过拦截并回放你的手势来启用触控。不读取无障碍窗口内容，不存储也不共享手势数据。关闭触控功能或本服务即可停止回放。",
      "source_location": "res/values/strings.xml accessibility_service_description（经 res/xml/mirror_accessibility_service.xml android:description 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Middor Touch in Android Accessibility settings for touch controls. Not needed for view-only mirroring. If it stops working after an update, turn it off and on.",
      "text_zh": "在 Android 无障碍设置中启用 Middor Touch 以使用触控；仅观看镜像不需要。若更新后失效，请关闭再重新开启。",
      "source_location": "res/values/strings.xml settings_accessibility_permission_info",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "3. For touch controls, enable Middor Touch in Android Accessibility settings. Skip this for view-only mirroring.",
      "text_zh": "3. 如需触控，请在 Android 无障碍设置中启用 Middor Touch。仅观看镜像可跳过此步。",
      "source_location": "res/values/strings.xml help_accessibility_step",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Middor Touch in Android Accessibility settings to tap and swipe the mirror. Gestures replay after you lift your fingers. Turning this off makes the mirror view-only and blocks touches to the hidden app. Restart to apply.",
      "text_zh": "在 Android 无障碍设置中启用 Middor Touch 后即可点击和滑动镜像。手势会在你抬指后回放。关闭此项后镜像变为仅观看，并阻止对被隐藏应用的触摸。重启后生效。",
      "source_location": "res/values/strings.xml settings_touch_controls_note",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Middor Touch is unavailable. Check Accessibility.",
      "text_zh": "Middor Touch 不可用，请检查无障碍设置。",
      "source_location": "res/values/strings.xml settings_accessibility_not_connected",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Settings and grant %1$s the overlay permission. This is for displaying an overlay over other apps.",
      "text_zh": "打开设置并为 %1$s 授予悬浮窗权限，用于在其他应用之上显示悬浮层。",
      "source_location": "res/values/strings.xml help_overlay_step",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "To exit, tap on the red Close (×) icon in the configured corner of the overlay (top right by default). Alternatively, you can pull down on your status bar and tap the notification.",
      "text_zh": "退出时，点击悬浮层指定角落（默认右上角）的红色关闭（×）图标；也可以下拉状态栏并点击通知退出。",
      "source_location": "res/values/strings.xml help_exit_overlay_step",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。未授权或从系统设置返回后仅以内联文本提示（settings_accessibility_not_connected / settings_accessibility_permission_error），不自动重跳、无定时器拉起、无不可取消弹窗；用户可继续使用仅观看镜像。",
    "overlay_or_fake_settings": "无。未叠放半透明引导遮罩、无全屏悬浮窗引导、无高仿系统无障碍开关页；悬浮窗仅用于镜像显示本身。",
    "restricted_settings_13plus_coaching": "无。APPLICATION_DETAILS_SETTINGS 仅作为普通“App Info”入口，无“点右上角菜单允许受限设置”或 Session 安装器绕过等教唆文案。",
    "post_grant_anti_removal": "无。无障碍服务仅监听 touchInteractionStart/End 并回放手势（canRetrieveWindowContent=false），未实现自点确认、自授权或 GLOBAL_ACTION_BACK/HOME 阻止撤权。",
    "benign_graceful_degradation": "有。明确提供仅观看模式：文案多处标注“Not needed for view-only mirroring / Skip this for view-only mirroring”，关闭触控后镜像仍可查看（仅阻止对被隐藏应用的触摸）。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测 startActivity 的 intent action 为 android.settings.ACCESSIBILITY_SETTINGS（由 r41.a 发起）或 MANAGE_OVERLAY_PERMISSION / APPLICATION_DETAILS_SETTINGS（由 r3.a 发起）的瞬间；以及冷启动 MainActivity 后进入 Settings → Permissions 分区的时刻。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动入口页（MainActivity Compose 首页）",
        "page_identifier": "org.nktnet.middor/.MainActivity，含 Start Mirror Display Overlay / Instructions / Help",
        "why_most_useful": "确认是否冷启动即弹不可取消引导；本应用此处无权限弹窗，可用于反证“0 步强制引导”",
        "observable_utg_signals": ["首页无 Dialog/无障碍弹窗节点", "存在可关闭的普通功能按钮", "无悬浮窗遮罩层节点"]
      },
      {
        "page_role": "跳转前应用内设置页 Permissions 分区",
        "page_identifier": "Settings 页面含 Accessibility / Overlay / Notifications 行与 Request、Granted 按钮",
        "why_most_useful": "判定引导是否由用户主动点 Request 触发（按需）且说明文案是否透明、是否含跳过/降级提示",
        "observable_utg_signals": ["settings_accessibility_permission_info 全文可提取", "Request 按钮可点击且存在返回/不操作路径", "标注 Not needed for view-only mirroring"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 中 \"Middor Touch\" 条目及其描述文本",
        "why_most_useful": "核对服务名与描述是否如实（不读取窗口内容/不共享数据），并与桌面名 Middor 比对身份一致性",
        "observable_utg_signals": ["条目文本 Middor Touch", "描述含 Does not read accessibility window content", "条目由用户手动开关（应用无代点行为）"]
      },
      {
        "page_role": "拒权返回后的应用内反馈页",
        "page_identifier": "返回 MainActivity/Settings 后显示 Middor Touch is unavailable. Check Accessibility.",
        "why_most_useful": "验证是否存在拒绝循环（onResume 重跳/Timer 拉起）——本应用应停留原页并允许继续",
        "observable_utg_signals": ["无自动跳转系统设置页", "无每秒重复弹窗/遮罩", "仍可操作仅观看模式入口"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。文本全为 strings.xml 明文字符串，无图片/纯图诱导；Compose 页面为原生节点，UTG 可正常取文本。唯一需注意：引导页组合在 R8 混淆导航图中，页面层级命名不可预期，应按文本内容而非类名匹配。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "r41.a（协程分支：new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").startActivity）",
    "r3.a（Intent(\"android.settings.action.MANAGE_OVERLAY_PERMISSION\", package:pkg) 与 Intent(\"android.settings.APPLICATION_DETAILS_SETTINGS\", package:pkg)）",
    "org.nktnet.middor.MainActivity.onCreate",
    "org.nktnet.middor.services.MirrorInputService.c / MirrorInputService.e",
    "res/xml/mirror_accessibility_service.xml",
    "res/values/strings.xml#L3-L49"
  ]
}
```

</details>
