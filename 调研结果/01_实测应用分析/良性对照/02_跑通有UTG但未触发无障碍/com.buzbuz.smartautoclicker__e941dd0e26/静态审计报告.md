# BN_057__e941dd0e26｜自动化与跳广告 — Klick'r

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：111.7s

## 1. 一句话核心结论

- **核心申请方式**：开源自动点击工具在用户启用自动化功能时弹出可取消的原生说明弹窗，点授权后直接跳转系统无障碍设置并定位到本服务条目，文案坦陈用途并声明不收集数据，无遮罩、无拒权死循环、无受限设置教学。
- **静态可见性说明**：DEX 未加壳、无 AES/动态加载/远端 HTML；无障碍申请链路、弹窗布局与全部文案均静态可见于 res/layout/dialog_permission.xml、res/xml/accessibilityservice.xml 与 res/values/strings.xml，跳转逻辑位于 pn3.d 与 qn3.onClick，可完整还原。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `e941dd0e263136f88344c5d8bdaef7a3ec4f0514be7addef41a6e199fb69df6d` |
| 包名 / 年份 | `com.buzbuz.smartautoclicker` / 2025-2026 |
| 家族 / 品类 | **自动化与跳广告**（同池样本数：1） |
| 原始来源标识 | https://github.com/Nain57/Smart-AutoClicker/releases/download/4.1.2/smartautoclicker-fDroid-arm64-v8a-release.apk |
| 桌面显示名 | Klick'r |
| 引导页宣称品牌/身份 | Klick'r (Smart AutoClicker) 开源图像识别自动点击工具（GitHub 开源，真实身份） |
| 系统无障碍列表服务名 | Accessibility service（系统无障碍列表内服务名，description 为“This application needs this service to inject the clicks…”） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.buzbuz.smartautoclicker.SmartAutoClickerService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | This application needs this service to inject the clicks you have created into the other applications once the conditions have been detected.<br><br>No data will be collected from this application. Feel free to visit our github, the code is open source ! |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.buzbuz.smartautoclicker.scenarios.ScenarioActivity（MAIN/LAUNCHER，场景列表主界面） | onCreate / onResume（点击桌面图标冷启动） | 原生Activity | **原文**：Scenarios<br>**译注**：场景列表主界面，冷启动不弹权限阻断窗 | 浏览/创建自动化场景；可直接返回或退出，无强制跳转 | `com.buzbuz.smartautoclicker.scenarios.ScenarioActivity.onCreate / onResume` |
| 2 | 业务功能触发 | 权限校验 DialogFragment（sn3，布局 res/layout/dialog_permission.xml） | 用户启用自动化/开始点击（启动场景或快速设置磁贴 QSTileService）时检测到无障碍未开启，弹窗由 sn3.E 显示 | 原生Dialog | **原文**：Accessibility service<br>**译注**：标题为“无障碍服务”的原生说明弹窗 | 阅读说明后可选择授权或取消（存在取消按钮） | `sn3.W() + qn3.onClick` |
| 3 | 引导说明页 | dialog_permission 内容区（MaterialTextView 正文 + 两个 MaterialButton） | DialogFragment onCreateDialog/inflate 完成即展示 | 原生Dialog | **原文**：The accessibility service permission allows Klick'r to perform gestures on your device screen. This permission is required in order to execute the clicks and gestures you will create in your automations scenarios.<br><br>No data is collected by Klick'r<br><br>To grant the Accessibility service permission, click on the button bellow.<br>**译注**：无障碍服务权限允许 Klick'r 在你的设备屏幕上执行手势，这是运行你创建的点击与手势自动化所必需的。Klick'r 不收集任何数据。要授予无障碍服务权限，请点击下方按钮。 | 点击下方按钮授予权限，或点击取消/返回关闭 | `res/values/strings.xml#message_permission_desc_accessibility；res/layout/dialog_permission.xml` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（经 :settings:fragment_args_key 定位到本服务条目） | 点击弹窗授权按钮 → qn3.onClick(case 0) → on3.d(Activity) | 系统无障碍页 | **原文**：Intent intent = new Intent("android.settings.ACCESSIBILITY_SETTINGS"); intent.addFlags(1342177280); intent.putExtra(":settings:fragment_args_key", strFlattenToString);<br>**译注**：跳转系统无障碍设置页，并直接高亮本服务开关条目；同时向 SharedPreferences("permissions") 写入已请求标记 | 用户需在系统页面手动打开 Klick'r 服务开关（应用无法自行授权） | `pn3.d(gc) / qn3.onClick` |
| 5 | 拒权反馈循环 | 返回 ScenarioActivity；权限未开启时展示 dialog_title_permission_mandatory_denied / message_accessibility_issues | 从系统设置返回（onResume）或再次触发功能 | 原生Dialog | **原文**：This permission is mandatory for Klick'r. It won't be able to work correctly without it.<br>**译注**：该权限对 Klick'r 是必需的，缺少它应用无法正常工作。仅在再次使用功能时提示，不做自动重跳或定时拉起。 | 可继续取消并留在应用内编辑场景，无强制循环 | `res/values/strings.xml#message_permission_mandatory_denied；ScenarioActivity.onResume` |
| 6 | 获权后动作 | com.buzbuz.smartautoclicker.SmartAutoClickerService（foregroundServiceType=mediaProjection） | 系统绑定无障碍服务后 onServiceConnected，按场景条件执行点击手势 | 通知栏 | **原文**：This application needs this service to inject the clicks you have created into the other applications once the conditions have been detected.<br><br>No data will be collected from this application. Feel free to visit our github, the code is open source !<br>**译注**：本服务用于在条件被检测到后向你创建的目标应用注入点击；不收集任何数据，代码开源可查。 | 无需额外操作；通知栏可回到场景列表 | `res/xml/accessibilityservice.xml；com.buzbuz.smartautoclicker.SmartAutoClickerService.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表服务条目说明：res/xml/accessibilityservice.xml 的 android:description=@string/accessibility_service_description（含“不收集数据、代码开源”声明）
- 功能触发时的不可跳过内容但可取消的原生 Dialog：res/layout/dialog_permission.xml，标题 dialog_title_permission_accessibility=“Accessibility service”，正文 message_permission_desc_accessibility
- 拒权/权限被移除后的提示弹窗：message_permission_mandatory_denied 与排障说明 message_accessibility_issues（dialog_title_permission_issue=“Troubleshooting”，指向外部网站自助排查厂商杀后台）
- 悬浮窗权限单独说明弹窗：dialog_title_permission_overlay 与 message_permission_desc_overlay（说明用于在被自动化应用之上显示配置界面）
- 通知权限说明与请求：RequestNotificationPermissionActivity（透明 Activity）+ message_permission_desc_notification
- 教程页：com.buzbuz.smartautoclicker.feature.tutorial.ui.TutorialActivity（activity_tutorial_name=“Tutorial”）
- 未发现任何 WebView/本地或远端 HTML 引导页、半透明引导遮罩或仿冒系统无障碍开关页面

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | This application needs this service to inject the clicks you have created into the other applications once the conditions have been detected.<br><br>No data will be collected from this application. Feel free to visit our github, the code is open source ! | 本应用需要该服务，在条件被检测到后把你创建的点击注入到其他应用。本应用不会收集任何数据，欢迎访问我们的 GitHub，代码是开源的！ | `res/values/strings.xml#accessibility_service_description（供 res/xml/accessibilityservice.xml 使用）` | 良性透明说明 |
| en | The accessibility service permission allows Klick'r to perform gestures on your device screen. This permission is required in order to execute the clicks and gestures you will create in your automations scenarios.<br><br>No data is collected by Klick'r<br><br>To grant the Accessibility service permission, click on the button bellow. | 无障碍服务权限允许 Klick'r 在你的屏幕上执行手势，这是运行你在自动化场景中创建的点击与手势所必需的。Klick'r 不收集任何数据。要授予无障碍服务权限，请点击下方按钮。 | `res/values/strings.xml#message_permission_desc_accessibility` | 隐私承诺 |
| en | Accessibility service | 无障碍服务（权限弹窗标题，与系统设置页服务名一致，未伪装成系统组件或安全中心） | `res/values/strings.xml#dialog_title_permission_accessibility` | 良性透明说明 |
| en | This permission is mandatory for Klick'r. It won't be able to work correctly without it. | 该权限对 Klick'r 是必需的，缺少它应用将无法正常工作。 | `res/values/strings.xml#message_permission_mandatory_denied` | 良性透明说明 |
| en | It seems like the Accessibility Service permission has been removed several times. If you haven't changed it yourself, this means your device has removed it.<br><br> Some Android devices manufacturer are not respecting the standard behaviour about background applications, and depending on your device brand, you might need to perform additional configuration.<br><br> Please refer to the following website to find more insight about that issue and how you can improve the permission stability. | 无障碍服务权限似乎已被多次移除。如果你并未自行更改，说明是设备移除了它。部分 Android 厂商未遵循后台应用的标准行为，取决于你的设备品牌，你可能需要额外配置。请参考以下网站了解该问题及如何提升权限稳定性。 | `res/values/strings.xml#message_accessibility_issues` | 良性透明说明 |
| en | The overlay permission is required in order to show Klick'r interface over the applications you want to automate, allowing you to configure your scenario without stopping the other application. | 悬浮窗权限用于在被自动化的应用之上显示 Klick'r 界面，使你能在不中断目标应用的情况下配置场景。 | `res/values/strings.xml#message_permission_desc_overlay` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：用户取消或从系统设置返回后无自动重跳：ScenarioActivity.onResume 仅刷新界面，仅在再次启用自动化功能时重新弹出同一说明弹窗，并提示 message_permission_mandatory_denied；无定时器拉起、无 onResume 死循环、无后台重启跳转。
- **遮罩叠层 / 高仿系统设置页**：无。未发现叠放半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于在被自动化应用之上显示配置界面，跳转目标为真实系统设置页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。获权后仅在 SharedPreferences("permissions") 写入已请求标记；未发现自点系统确认、监听设置页并以 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；PERFORM_GLOBAL_ACTION 属场景内“System action”动作能力。
- **良性降级 / 替代方案**：有。取消权限后可继续在应用内创建/编辑场景（仅无法执行点击）；悬浮窗与通知权限均为可选并单独说明，教程页 TutorialActivity 提供使用引导，排障说明引导用户自行处理厂商杀后台问题。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在用户首次启用自动化功能（启动场景/点击快速设置磁贴）后、出现标题为“Accessibility service”的原生弹窗时开始采集；以及点击该弹窗授权按钮后监测到 intent action=android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。全部引导文案为原生 TextView 文本，可直接 UTG 提取；仅需注意该应用部分功能需 mediaProjection 屏幕捕获授权，冷启动初期可能先出现系统录屏授权框，勿误判为无障碍诱导。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **功能触发时的无障碍说明弹窗页** | DialogFragment 布局 dialog_permission：标题 “Accessibility service” + 正文说明 + 两个 MaterialButton（授权/取消） | 该页是应用唯一主动索取无障碍权限的界面，可直接判定文案是否如实陈述用途、是否提供取消入口、是否存在恐吓或隐瞒。 | 标题文本 “Accessibility service”；正文包含 “No data is collected by Klick'r” 与 “click on the button bellow”；同时存在两个可点击按钮（含取消） |
| **跳转系统设置后的目标页** | 系统 Settings 无障碍页，且高亮/定位到 Klick'r 服务条目（fragment_args_key 生效） | 区分“跳到真实系统设置”与“伪造设置页/叠压遮罩”两种关键路径，是纯 UTG 判定诱导与否的分水岭。 | 页面包名为 com.android.settings 而非本应用；当前栈顶为系统无障碍服务列表；未出现应用自绘的全屏悬浮层 |
| **拒权返回后的反馈页** | 回到 ScenarioActivity 场景列表，可能伴随 “Permission denied / mandatory” 提示弹窗 | 验证是否存在拒权重跳循环或强制阻断，良性实现应停留在主界面并允许继续编辑场景。 | 返回后栈顶仍为 com.buzbuz.smartautoclicker 主界面；无 2 秒级重复拉起 ACCESSIBILITY_SETTINGS；可点击取消/返回退出弹窗 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `pn3.d(gc)：new Intent("android.settings.ACCESSIBILITY_SETTINGS") + :settings:fragment_args_key 定位服务条目`
- `qn3.onClick：case 0 授权跳转并写 SharedPreferences("permissions")，case 1 取消关闭弹窗`
- `sn3.W()：inflate res/layout/dialog_permission.xml 并绑定两个 MaterialButton 点击监听`
- `res/xml/accessibilityservice.xml：description/canPerformGestures/canRetrieveWindowContent/canRequestFilterKeyEvents`
- `res/values/strings.xml#message_permission_desc_accessibility / #accessibility_service_description`
- `com.buzbuz.smartautoclicker.scenarios.ScenarioActivity.onCreate / onResume`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，未发现诱导行为）

**静态可见性：完整清晰。** DEX 未加壳、无动态加载、无远端 HTML/WebView；引导文案全部来自 `res/values/strings.xml` 与 `res/layout/dialog_permission.xml`。

**无障碍申请路径（运行期 UTG 视角）**
1. 桌面入口为 [ScenarioActivity](<resource-unit:#1.dex1 code:com.buzbuz.smartautoclicker.scenarios.ScenarioActivity#onCreate>)（`MAIN/LAUNCHER`），冷启动**不**强制弹窗阻断；`onResume` 仅刷新列表，无死循环重跳。
2. 用户启用自动化功能时触发原生 `DialogFragment` 权限弹窗：[sn3.W()](<resource-unit:#1.dex1 code:sn3#W>) inflate `dialog_permission` 布局，标题 “Accessibility service”，正文为“说明 + 无数据收集声明 + 点击下方按钮授权”，含**两个按钮**（授权 / 取消）。
3. 点“授权”走 [qn3.onClick](<resource-unit:#1.dex1 code:qn3#onClick>) 的 case 0 → [pn3.d](<resource-unit:#1.dex1 code:pn3#d>)：`Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `FLAG_ACTIVITY_NEW_TASK|CLEAR_TASK`，并附带 `:settings:fragment_args_key = <服务组件名>`，即**直接定位到本服务条目**的系统无障碍页（属正常便利跳转，非仿冒页面）。
4. 点“取消”走 case 1 → `sn3.V(false,false)` 关闭弹窗，功能降级，无反复骚扰。
5. 未授权返回时仅出现 `message_permission_mandatory_denied` 的普通提示；**未发现** `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转，故无 Android 13+ 受限设置分步教学，也无 Session 安装器绕过。
6. 获权后写 `SharedPreferences("permissions")` 仅作“已请求过”标记；服务 [accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml>) 声明 `canPerformGestures/canRetrieveWindowContent/canRequestFilterKeyEvents`，与自动点击/识别业务一致。另有厂商杀后台的排障说明 `message_accessibility_issues`（指向外部网站自助排查），属良性透明度说明。
7. `SYSTEM_ALERT_WINDOW` 用途为在被自动化应用之上显示 Klick'r 配置界面（`message_permission_desc_overlay`），并非叠压系统设置页的引导遮罩；`PERFORM_GLOBAL_ACTION` 对应场景内“System action”动作能力，未见撤权后自点确认或 `GLOBAL_ACTION_BACK` 拦截撤权的代码。

**身份一致性：** 桌面名 `Klick'r`、无障碍列表服务名 “Accessibility service”（`dialog_title_permission_accessibility`）与开源仓库一致，无空白/换行挤出警告、无同形字、无多 `activity-alias`、无伪造 `isAccessibilityTool`（配置中未声明该属性，交由系统默认判定）。

**未决/边界：** 未做动态抓取；`dialog_permission` 布局中按钮文本引用的具体 string key 未逐字回读（由 `public.xml` 仅确认布局与文案资源存在），不影响诱导性判定。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳、无 AES/动态加载/远端 HTML；无障碍申请链路、弹窗布局与全部文案均静态可见于 res/layout/dialog_permission.xml、res/xml/accessibilityservice.xml 与 res/values/strings.xml，跳转逻辑位于 pn3.d 与 qn3.onClick，可完整还原。",
  "summary_one_liner": "开源自动点击工具在用户启用自动化功能时弹出可取消的原生说明弹窗，点授权后直接跳转系统无障碍设置并定位到本服务条目，文案坦陈用途并声明不收集数据，无遮罩、无拒权死循环、无受限设置教学。",
  "disguise_identity": {
    "app_display_name": "Klick'r",
    "claimed_brand_or_persona": "Klick'r (Smart AutoClicker) 开源图像识别自动点击工具（GitHub 开源，真实身份）",
    "a11y_service_label": "Accessibility service（系统无障碍列表内服务名，description 为“This application needs this service to inject the clicks…”）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.buzbuz.smartautoclicker.scenarios.ScenarioActivity（MAIN/LAUNCHER，场景列表主界面）",
      "trigger_event": "onCreate / onResume（点击桌面图标冷启动）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Scenarios",
      "shown_text_zh": "场景列表主界面，冷启动不弹权限阻断窗",
      "user_action_requested": "浏览/创建自动化场景；可直接返回或退出，无强制跳转",
      "code_anchor": "com.buzbuz.smartautoclicker.scenarios.ScenarioActivity.onCreate / onResume"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "权限校验 DialogFragment（sn3，布局 res/layout/dialog_permission.xml）",
      "trigger_event": "用户启用自动化/开始点击（启动场景或快速设置磁贴 QSTileService）时检测到无障碍未开启，弹窗由 sn3.E 显示",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Accessibility service",
      "shown_text_zh": "标题为“无障碍服务”的原生说明弹窗",
      "user_action_requested": "阅读说明后可选择授权或取消（存在取消按钮）",
      "code_anchor": "sn3.W() + qn3.onClick"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "dialog_permission 内容区（MaterialTextView 正文 + 两个 MaterialButton）",
      "trigger_event": "DialogFragment onCreateDialog/inflate 完成即展示",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "The accessibility service permission allows Klick'r to perform gestures on your device screen. This permission is required in order to execute the clicks and gestures you will create in your automations scenarios.\n\nNo data is collected by Klick'r\n\nTo grant the Accessibility service permission, click on the button bellow.",
      "shown_text_zh": "无障碍服务权限允许 Klick'r 在你的设备屏幕上执行手势，这是运行你创建的点击与手势自动化所必需的。Klick'r 不收集任何数据。要授予无障碍服务权限，请点击下方按钮。",
      "user_action_requested": "点击下方按钮授予权限，或点击取消/返回关闭",
      "code_anchor": "res/values/strings.xml#message_permission_desc_accessibility；res/layout/dialog_permission.xml"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（经 :settings:fragment_args_key 定位到本服务条目）",
      "trigger_event": "点击弹窗授权按钮 → qn3.onClick(case 0) → on3.d(Activity)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Intent intent = new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"); intent.addFlags(1342177280); intent.putExtra(\":settings:fragment_args_key\", strFlattenToString);",
      "shown_text_zh": "跳转系统无障碍设置页，并直接高亮本服务开关条目；同时向 SharedPreferences(\"permissions\") 写入已请求标记",
      "user_action_requested": "用户需在系统页面手动打开 Klick'r 服务开关（应用无法自行授权）",
      "code_anchor": "pn3.d(gc) / qn3.onClick"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 ScenarioActivity；权限未开启时展示 dialog_title_permission_mandatory_denied / message_accessibility_issues",
      "trigger_event": "从系统设置返回（onResume）或再次触发功能",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "This permission is mandatory for Klick'r. It won't be able to work correctly without it.",
      "shown_text_zh": "该权限对 Klick'r 是必需的，缺少它应用无法正常工作。仅在再次使用功能时提示，不做自动重跳或定时拉起。",
      "user_action_requested": "可继续取消并留在应用内编辑场景，无强制循环",
      "code_anchor": "res/values/strings.xml#message_permission_mandatory_denied；ScenarioActivity.onResume"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.buzbuz.smartautoclicker.SmartAutoClickerService（foregroundServiceType=mediaProjection）",
      "trigger_event": "系统绑定无障碍服务后 onServiceConnected，按场景条件执行点击手势",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "This application needs this service to inject the clicks you have created into the other applications once the conditions have been detected.\n\nNo data will be collected from this application. Feel free to visit our github, the code is open source !",
      "shown_text_zh": "本服务用于在条件被检测到后向你创建的目标应用注入点击；不收集任何数据，代码开源可查。",
      "user_action_requested": "无需额外操作；通知栏可回到场景列表",
      "code_anchor": "res/xml/accessibilityservice.xml；com.buzbuz.smartautoclicker.SmartAutoClickerService.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表服务条目说明：res/xml/accessibilityservice.xml 的 android:description=@string/accessibility_service_description（含“不收集数据、代码开源”声明）",
    "功能触发时的不可跳过内容但可取消的原生 Dialog：res/layout/dialog_permission.xml，标题 dialog_title_permission_accessibility=“Accessibility service”，正文 message_permission_desc_accessibility",
    "拒权/权限被移除后的提示弹窗：message_permission_mandatory_denied 与排障说明 message_accessibility_issues（dialog_title_permission_issue=“Troubleshooting”，指向外部网站自助排查厂商杀后台）",
    "悬浮窗权限单独说明弹窗：dialog_title_permission_overlay 与 message_permission_desc_overlay（说明用于在被自动化应用之上显示配置界面）",
    "通知权限说明与请求：RequestNotificationPermissionActivity（透明 Activity）+ message_permission_desc_notification",
    "教程页：com.buzbuz.smartautoclicker.feature.tutorial.ui.TutorialActivity（activity_tutorial_name=“Tutorial”）",
    "未发现任何 WebView/本地或远端 HTML 引导页、半透明引导遮罩或仿冒系统无障碍开关页面"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "This application needs this service to inject the clicks you have created into the other applications once the conditions have been detected.\n\nNo data will be collected from this application. Feel free to visit our github, the code is open source !",
      "text_zh": "本应用需要该服务，在条件被检测到后把你创建的点击注入到其他应用。本应用不会收集任何数据，欢迎访问我们的 GitHub，代码是开源的！",
      "source_location": "res/values/strings.xml#accessibility_service_description（供 res/xml/accessibilityservice.xml 使用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The accessibility service permission allows Klick'r to perform gestures on your device screen. This permission is required in order to execute the clicks and gestures you will create in your automations scenarios.\n\nNo data is collected by Klick'r\n\nTo grant the Accessibility service permission, click on the button bellow.",
      "text_zh": "无障碍服务权限允许 Klick'r 在你的屏幕上执行手势，这是运行你在自动化场景中创建的点击与手势所必需的。Klick'r 不收集任何数据。要授予无障碍服务权限，请点击下方按钮。",
      "source_location": "res/values/strings.xml#message_permission_desc_accessibility",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service",
      "text_zh": "无障碍服务（权限弹窗标题，与系统设置页服务名一致，未伪装成系统组件或安全中心）",
      "source_location": "res/values/strings.xml#dialog_title_permission_accessibility",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This permission is mandatory for Klick'r. It won't be able to work correctly without it.",
      "text_zh": "该权限对 Klick'r 是必需的，缺少它应用将无法正常工作。",
      "source_location": "res/values/strings.xml#message_permission_mandatory_denied",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "It seems like the Accessibility Service permission has been removed several times. If you haven't changed it yourself, this means your device has removed it.\n\n Some Android devices manufacturer are not respecting the standard behaviour about background applications, and depending on your device brand, you might need to perform additional configuration.\n\n Please refer to the following website to find more insight about that issue and how you can improve the permission stability.",
      "text_zh": "无障碍服务权限似乎已被多次移除。如果你并未自行更改，说明是设备移除了它。部分 Android 厂商未遵循后台应用的标准行为，取决于你的设备品牌，你可能需要额外配置。请参考以下网站了解该问题及如何提升权限稳定性。",
      "source_location": "res/values/strings.xml#message_accessibility_issues",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The overlay permission is required in order to show Klick'r interface over the applications you want to automate, allowing you to configure your scenario without stopping the other application.",
      "text_zh": "悬浮窗权限用于在被自动化的应用之上显示 Klick'r 界面，使你能在不中断目标应用的情况下配置场景。",
      "source_location": "res/values/strings.xml#message_permission_desc_overlay",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "用户取消或从系统设置返回后无自动重跳：ScenarioActivity.onResume 仅刷新界面，仅在再次启用自动化功能时重新弹出同一说明弹窗，并提示 message_permission_mandatory_denied；无定时器拉起、无 onResume 死循环、无后台重启跳转。",
    "overlay_or_fake_settings": "无。未发现叠放半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于在被自动化应用之上显示配置界面，跳转目标为真实系统设置页。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。获权后仅在 SharedPreferences(\"permissions\") 写入已请求标记；未发现自点系统确认、监听设置页并以 GLOBAL_ACTION_BACK/HOME 阻止撤权的逻辑；PERFORM_GLOBAL_ACTION 属场景内“System action”动作能力。",
    "benign_graceful_degradation": "有。取消权限后可继续在应用内创建/编辑场景（仅无法执行点击）；悬浮窗与通知权限均为可选并单独说明，教程页 TutorialActivity 提供使用引导，排障说明引导用户自行处理厂商杀后台问题。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在用户首次启用自动化功能（启动场景/点击快速设置磁贴）后、出现标题为“Accessibility service”的原生弹窗时开始采集；以及点击该弹窗授权按钮后监测到 intent action=android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间。",
    "key_pages_to_capture": [
      {
        "page_role": "功能触发时的无障碍说明弹窗页",
        "page_identifier": "DialogFragment 布局 dialog_permission：标题 “Accessibility service” + 正文说明 + 两个 MaterialButton（授权/取消）",
        "why_most_useful": "该页是应用唯一主动索取无障碍权限的界面，可直接判定文案是否如实陈述用途、是否提供取消入口、是否存在恐吓或隐瞒。",
        "observable_utg_signals": ["标题文本 “Accessibility service”", "正文包含 “No data is collected by Klick'r” 与 “click on the button bellow”", "同时存在两个可点击按钮（含取消）"]
      },
      {
        "page_role": "跳转系统设置后的目标页",
        "page_identifier": "系统 Settings 无障碍页，且高亮/定位到 Klick'r 服务条目（fragment_args_key 生效）",
        "why_most_useful": "区分“跳到真实系统设置”与“伪造设置页/叠压遮罩”两种关键路径，是纯 UTG 判定诱导与否的分水岭。",
        "observable_utg_signals": ["页面包名为 com.android.settings 而非本应用", "当前栈顶为系统无障碍服务列表", "未出现应用自绘的全屏悬浮层"]
      },
      {
        "page_role": "拒权返回后的反馈页",
        "page_identifier": "回到 ScenarioActivity 场景列表，可能伴随 “Permission denied / mandatory” 提示弹窗",
        "why_most_useful": "验证是否存在拒权重跳循环或强制阻断，良性实现应停留在主界面并允许继续编辑场景。",
        "observable_utg_signals": ["返回后栈顶仍为 com.buzbuz.smartautoclicker 主界面", "无 2 秒级重复拉起 ACCESSIBILITY_SETTINGS", "可点击取消/返回退出弹窗"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。全部引导文案为原生 TextView 文本，可直接 UTG 提取；仅需注意该应用部分功能需 mediaProjection 屏幕捕获授权，冷启动初期可能先出现系统录屏授权框，勿误判为无障碍诱导。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "pn3.d(gc)：new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + :settings:fragment_args_key 定位服务条目",
    "qn3.onClick：case 0 授权跳转并写 SharedPreferences(\"permissions\")，case 1 取消关闭弹窗",
    "sn3.W()：inflate res/layout/dialog_permission.xml 并绑定两个 MaterialButton 点击监听",
    "res/xml/accessibilityservice.xml：description/canPerformGestures/canRetrieveWindowContent/canRequestFilterKeyEvents",
    "res/values/strings.xml#message_permission_desc_accessibility / #accessibility_service_description",
    "com.buzbuz.smartautoclicker.scenarios.ScenarioActivity.onCreate / onResume"
  ]
}
```

</details>
