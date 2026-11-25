# BN_038__8e03f060a2｜极简桌面与双击锁屏 — Vulcan

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：260.7s

## 1. 一句话核心结论

- **核心申请方式**：Vulcan 在用户触发锁屏/最近任务等手势时弹出原生说明弹窗，明确告知用途与可跳过，用户点 Agree 后仅通过 startActivity 跳系统无障碍设置页手动开启 'Vulcan actions'，服务被限制为不读屏且不联网。
- **静态可见性说明**：DEX 未加壳未加密，Manifest、res/xml/action_service.xml、res/values/strings.xml 与 classes.dex 字符串表均完整可读；仅 MCP 代码服务本轮连接失败，改用 androguard/strings 完成定向核验，结论不依赖动态脱壳。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8e03f060a2c23a7bbb24bbc3e643710b2e0085d37b688ec921b475d0a6cf7052` |
| 包名 / 年份 | `dev.vulcanlauncher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/dev.vulcanlauncher_27.apk |
| 桌面显示名 | Vulcan |
| 引导页宣称品牌/身份 | Vulcan（F-Droid 开源极简桌面，自称无网络、无广告、无追踪） |
| 系统无障碍列表服务名 | Vulcan actions |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅有代码层标识符混淆（a.A0、a.B1 等单字母类名），属 R8 常规压缩，不影响界面身份；服务标签、包名、android:description 三者语义一致，无空白/换行挤出、无同形字、无多 activity-alias、无伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `dev.vulcanlauncher.ActionService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：dev.vulcanlauncher |
| 共现高危权限 | `READ_CONTACTS` |
| 系统设置项说明 (`android:description`) | Lets Vulcan lock the screen, open recent apps, quick settings and the power menu from a gesture. It reads no screen content. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | dev.vulcanlauncher.MainActivity（HOME/LAUNCHER，singleTask） | onCreate（作为默认桌面启动） | 原生Activity | 无 | 无强制操作；可正常使用桌面，无需授权 | `dev.vulcanlauncher.MainActivity#onCreate / AndroidManifest.xml android.intent.category.HOME` |
| 2 | 业务功能触发 | MainActivity 内的手势/快捷方式动作设置（动作项 lock、recents、notifications、quicksettings、power 等） | 用户为某个手势或快捷方式选择需要无障碍的动作（如 Screen lock / Recent apps / Expand quick settings / Power menu） | 原生Activity | **原文**：Screen lock / Recent apps / Expand notifications / Expand quick settings / Power menu<br>**译注**：锁屏 / 最近任务 / 展开通知 / 展开快捷设置 / 电源菜单 | 选择该动作；此时动作尚未具备执行能力，触发下一步说明 | `res/values/strings.xml: action_lock, action_recents, action_notifications, action_quicksettings, action_power` |
| 3 | 引导说明页 | MainActivity 内原生说明对话框（标题 accessibility_title + 正文 accessibility_text + Agree 按钮） | 步骤 2 选中需无障碍的动作后弹出 | 原生Dialog | **原文**：Turn on the accessibility service / Vulcan uses the AccessibilityService API only when you trigger a gesture or shortcut to lock the screen, open recent apps, notifications, quick settings or the power menu. The service does not read screen content, record your interactions, or collect or share personal data. It only performs the action you request. Access is optional; the rest of the launcher works without it. You can turn it off at any time in Android Accessibility settings. Tap Agree and open settings to continue, then enable Vulcan actions.<br>**译注**：开启无障碍服务。Vulcan 仅在你通过手势或快捷方式触发锁屏、最近任务、通知、快捷设置或电源菜单时使用 AccessibilityService API。该服务不读取屏幕内容、不记录你的操作、不收集或共享个人数据，只执行你请求的动作。授权是可选的，桌面其余功能无需授权即可使用，你也可随时在 Android 无障碍设置中关闭。点「同意并打开设置」继续，然后启用 Vulcan actions。 | 点击 Agree and open settings（同意并打开设置）继续；对话框为说明性质，可返回/取消而不被阻断 | `res/values/strings.xml#L8-L13 (accessibility_text, accessibility_title)` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载/已安装的服务列表中的 Vulcan actions | 步骤 3 点击 Agree 后 startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Vulcan actions / Lets Vulcan lock the screen, open recent apps, quick settings and the power menu from a gesture. It reads no screen content.<br>**译注**：Vulcan actions / 让 Vulcan 通过手势锁屏、打开最近任务、快捷设置与电源菜单；不读取屏幕内容。 | 由用户在系统页手动将 Vulcan actions 开关打开（应用无法代点、无遮罩、无高仿开关页） | `classes.dex 字符串 "android.settings.ACCESSIBILITY_SETTINGS"；res/xml/action_service.xml；res/values/strings.xml: action_service_label, action_service_description` |
| 5 | 获权后动作 | dev.vulcanlauncher.ActionService（AccessibilityService） | 用户再次触发已绑定的手势/快捷方式 → 服务执行 performGlobalAction（锁屏、最近任务、通知/快捷设置面板、电源菜单） | 系统无障碍页 | 无 | 无需额外操作；可在系统设置中随时关闭 | `dev.vulcanlauncher.ActionService#onAccessibilityEvent / res/xml/action_service.xml (canRetrieveWindowContent=false, packageNames=dev.vulcanlauncher)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内的原生说明对话框：标题 strings.xml/accessibility_title（Turn on the accessibility service），正文 strings.xml/accessibility_text（含用途、隐私承诺、可选授权与撤权说明）
- 系统无障碍服务列表项：服务标签 action_service_label（Vulcan actions）与 android:description=action_service_description（经 res/xml/action_service.xml 的 android:description 引用）
- 桌面设置页相关条目：strings.xml 的 page_accessibility（Accessibility settings）、perm_accessibility（Accessibility service）、perm_accessibility_info（Screen lock, recent apps and the power menu from gestures）
- 无 assets 内本地 HTML 引导页、无远端 WebView 页面、无悬浮窗/遮罩层承载该引导文案（Manifest 无 INTERNET 与 SYSTEM_ALERT_WINDOW 权限）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Turn on the accessibility service | 开启无障碍服务 | `res/values/strings.xml: accessibility_title` | 良性透明说明 |
| en | Vulcan uses the AccessibilityService API only when you trigger a gesture or shortcut to lock the screen, open recent apps, notifications, quick settings or the power menu.<br><br>The service does not read screen content, record your interactions, or collect or share personal data. It only performs the action you request. Access is optional; the rest of the launcher works without it. You can turn it off at any time in Android Accessibility settings.<br><br>Tap Agree and open settings to continue, then enable Vulcan actions. | Vulcan 仅在你通过手势或快捷方式触发锁屏、打开最近任务、通知、快捷设置或电源菜单时使用 AccessibilityService API。该服务不读取屏幕内容、不记录你的操作、不收集或共享个人数据，只执行你请求的动作。授权是可选的，桌面其余功能无需授权即可使用，你也可随时在 Android 无障碍设置中关闭。点「同意并打开设置」继续，然后启用 Vulcan actions。 | `res/values/strings.xml: accessibility_text` | 隐私承诺 |
| en | Agree and open settings | 同意并打开设置 | `res/values/strings.xml / classes.dex（预筛字符串命中）` | 受限设置分步教学 |
| en | Lets Vulcan lock the screen, open recent apps, quick settings and the power menu from a gesture. It reads no screen content. | 让 Vulcan 通过手势锁屏、打开最近任务、快捷设置与电源菜单。它不读取屏幕内容。 | `res/values/strings.xml: action_service_description（res/xml/action_service.xml android:description 引用）` | 良性透明说明 |
| en | Screen lock, recent apps and the power menu from gestures | 通过手势实现锁屏、最近任务与电源菜单 | `res/values/strings.xml: perm_accessibility_info` | 良性透明说明 |
| en | A home screen with no network access: no ads, analytics or tracking. Everything stays on this device. | 一个无网络访问的桌面：没有广告、分析和追踪。一切都留在本设备上。 | `res/values/strings.xml: about_text` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无重跳循环：未授权或从系统设置返回后不主动再弹窗、无 onResume 死循环、无定时器拉起；仅在用户再次主动选择需要无障碍的动作时才会重新展示说明弹窗，桌面其余功能正常可用（accessibility_text 明示 Access is optional）
- **遮罩叠层 / 高仿系统设置页**：无。Manifest 未申请 SYSTEM_ALERT_WINDOW，无半透明遮罩层，无高仿系统无障碍开关页；跳转目标为真实系统 android.settings.ACCESSIBILITY_SETTINGS
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中未见 android.settings.APPLICATION_DETAILS_SETTINGS 及「右上角菜单允许受限设置」类分步教学文案，也无 Session 安装器绕过逻辑
- **获权后即时行为与防撤权机制**：无。未见获权后自点确认、自授权或通过 GLOBAL_ACTION_BACK/HOME 阻断撤权；PERFORM_GLOBAL_ACTION 仅用于执行用户请求的锁屏/最近任务/电源菜单动作
- **良性降级 / 替代方案**：有。授权为可选，未开启时仅相关手势动作不可用，桌面启动器核心功能（应用抽屉、页面、文件夹、壁纸等）完全正常；用户可随时在系统无障碍设置中关闭服务

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在用户首次为某手势/快捷方式选择需无障碍的动作（如 Screen lock / Recent apps / Power menu）后立即拉起 UTG 采集；或在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间及返回前台时各采集一次
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。纯静态加壳不阻挡运行期 UTG，而本包本身未加壳未加密；应用无 INTERNET 权限，不存在远端下发文案导致 UTG 看到的内容与静态资源不一致的情况；唯一可见性限制是本轮 MCP 代码服务连接失败，改用 androguard 定向核验，未做全量调用图还原。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **引导说明弹窗页（原生 Dialog）** | MainActivity 之上的原生 AlertDialog，标题 'Turn on the accessibility service'，含 Agree and open settings 按钮 | 该页一次性呈现用途、隐私承诺与可跳过声明，是判断是否诱导（恐吓/假更新/清理伪装）的唯一文案载体 | 标题与正文是否与 strings.xml accessibility_text 一致；是否存在取消/返回按钮，是否可关闭；是否存在夸大危害、假安全、倒计时等恐吓性措辞 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已安装服务中的 'Vulcan actions' 条目及其 description 文本 | 验证服务标签与说明是否与实际能力一致，是否存在标签伪装或空白挤出排序技巧 | 服务标签与 android:description 原文；开关初始为关闭（应用未代点）；是否存在叠加在设置页之上的悬浮引导层 |
| **跳转后返回前台的桌面页** | MainActivity 恢复前台（launcher 界面） | 区分良性降级与拒绝循环：观察返回后是否立即重复弹窗或反复跳设置页 | 返回后 3~5 秒内是否再次出现同一弹窗；是否出现持续遮罩或不可退出的页面；手势动作是否静默失效（降级） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `res/xml/action_service.xml（canRetrieveWindowContent=false, packageNames=dev.vulcanlauncher, accessibilityEventTypes=typeWindowStateChanged）`
- `res/values/strings.xml: accessibility_title / accessibility_text（引导弹窗文案与 Agree and open settings 声明）`
- `res/values/strings.xml: action_service_label / action_service_description（系统无障碍列表标签与说明）`
- `classes.dex 字符串 android.settings.ACCESSIBILITY_SETTINGS（跳转系统无障碍设置的 Intent action）`
- `AndroidManifest.xml: service dev.vulcanlauncher.ActionService（BIND_ACCESSIBILITY_SERVICE，exported=true）`
- `dev.vulcanlauncher.ActionService#onAccessibilityEvent（获权后按用户请求执行全局动作）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验）

**核验方式**：MCP 代码服务本轮连接失败（`ConnectError`），已改用 `androguard` + `strings` 对 `classes.dex` 做定向字符串/类结构核验，足以覆盖本次「引导开启无障碍」的页面流转链路。

- **身份与声明一致，无伪装**：桌面显示名 `Vulcan`，无障碍服务类 `dev.vulcanlauncher.ActionService`，系统列表标签 `Vulcan actions`（`action_service_label`），`android:description` 为坦诚的功能说明「只在你触发手势时锁屏/最近任务/快捷设置/电源菜单，不读取屏幕内容」。无空白/换行挤出、无多 `activity-alias`、无同形字。
- **服务能力被真实收窄**（与文案一致）：[action_service.xml](<resource-unit:#1 file:res/xml/action_service.xml>) 声明 `canRetrieveWindowContent="false"`、事件仅 `typeWindowStateChanged`、`packageNames="dev.vulcanlauncher"`（只监听自身包），不具备读屏能力，无法实现读屏窃取类滥用。
- **不存在远端诱导载体**：Manifest 权限表**无 `INTERNET`**、无 `SYSTEM_ALERT_WINDOW`、无 `QUERY_ALL_PACKAGES`，因此「远端 WebView 教学页」「设置页上压悬浮遮罩」在工程上不可达；应用内也无 `assets` HTML 引导页参与该流程。
- **引导文案为显式同意 + 可跳过**：[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L8-L13>) 中 `accessibility_title`=「Turn on the accessibility service」，`accessibility_text` 明示「Access is optional; the rest of the launcher works without it」「Tap Agree and open settings to continue, then enable Vulcan actions.」——是「Agree and open settings」的主动同意按钮，非不可取消强制弹窗。
- **跳转点**：DEX 中存在 `android.settings.ACCESSIBILITY_SETTINGS` 字面量（`classes.dex` 字符串表），即点击后直接 `startActivity` 跳到系统无障碍设置页，由用户手动开启；代码中未见 `ACTION_APPLICATION_DETAILS_SETTINGS`（无「允许受限设置」分步教学），未见 `onResume` 重跳/定时拉起、未见 `GLOBAL_ACTION_BACK/HOME` 阻止撤权（`PERFORM_GLOBAL_ACTION` 仅用于执行用户请求的锁屏/最近任务/电源菜单动作）。
- **拒权行为**：属良性降级——未授权时相关手势动作无效，桌面其余功能正常；`READ_CONTACTS` 与本链路无关（联系人搜索类桌面功能），未出现在无障碍引导路径。

**结论**：该应用以「按需功能触发 → 原生说明弹窗（含隐私承诺与可跳过声明）→ 用户点 Agree → 跳系统无障碍页手动开启」的透明单步引导获取无障碍权限，未发现诱导、恐吓、遮罩、拒绝循环或身份伪装，未发现可单独判定成立的风险命题，故不写入风险台账。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳未加密，Manifest、res/xml/action_service.xml、res/values/strings.xml 与 classes.dex 字符串表均完整可读；仅 MCP 代码服务本轮连接失败，改用 androguard/strings 完成定向核验，结论不依赖动态脱壳。",
  "summary_one_liner": "Vulcan 在用户触发锁屏/最近任务等手势时弹出原生说明弹窗，明确告知用途与可跳过，用户点 Agree 后仅通过 startActivity 跳系统无障碍设置页手动开启 'Vulcan actions'，服务被限制为不读屏且不联网。",
  "disguise_identity": {
    "app_display_name": "Vulcan",
    "claimed_brand_or_persona": "Vulcan（F-Droid 开源极简桌面，自称无网络、无广告、无追踪）",
    "a11y_service_label": "Vulcan actions",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅有代码层标识符混淆（a.A0、a.B1 等单字母类名），属 R8 常规压缩，不影响界面身份；服务标签、包名、android:description 三者语义一致，无空白/换行挤出、无同形字、无多 activity-alias、无伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "dev.vulcanlauncher.MainActivity（HOME/LAUNCHER，singleTask）",
      "trigger_event": "onCreate（作为默认桌面启动）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动直接进入桌面，不弹出任何无障碍引导或阻断性对话框",
      "user_action_requested": "无强制操作；可正常使用桌面，无需授权",
      "code_anchor": "dev.vulcanlauncher.MainActivity#onCreate / AndroidManifest.xml android.intent.category.HOME"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity 内的手势/快捷方式动作设置（动作项 lock、recents、notifications、quicksettings、power 等）",
      "trigger_event": "用户为某个手势或快捷方式选择需要无障碍的动作（如 Screen lock / Recent apps / Expand quick settings / Power menu）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Screen lock / Recent apps / Expand notifications / Expand quick settings / Power menu",
      "shown_text_zh": "锁屏 / 最近任务 / 展开通知 / 展开快捷设置 / 电源菜单",
      "user_action_requested": "选择该动作；此时动作尚未具备执行能力，触发下一步说明",
      "code_anchor": "res/values/strings.xml: action_lock, action_recents, action_notifications, action_quicksettings, action_power"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 内原生说明对话框（标题 accessibility_title + 正文 accessibility_text + Agree 按钮）",
      "trigger_event": "步骤 2 选中需无障碍的动作后弹出",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Turn on the accessibility service / Vulcan uses the AccessibilityService API only when you trigger a gesture or shortcut to lock the screen, open recent apps, notifications, quick settings or the power menu. The service does not read screen content, record your interactions, or collect or share personal data. It only performs the action you request. Access is optional; the rest of the launcher works without it. You can turn it off at any time in Android Accessibility settings. Tap Agree and open settings to continue, then enable Vulcan actions.",
      "shown_text_zh": "开启无障碍服务。Vulcan 仅在你通过手势或快捷方式触发锁屏、最近任务、通知、快捷设置或电源菜单时使用 AccessibilityService API。该服务不读取屏幕内容、不记录你的操作、不收集或共享个人数据，只执行你请求的动作。授权是可选的，桌面其余功能无需授权即可使用，你也可随时在 Android 无障碍设置中关闭。点「同意并打开设置」继续，然后启用 Vulcan actions。",
      "user_action_requested": "点击 Agree and open settings（同意并打开设置）继续；对话框为说明性质，可返回/取消而不被阻断",
      "code_anchor": "res/values/strings.xml#L8-L13 (accessibility_text, accessibility_title)"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载/已安装的服务列表中的 Vulcan actions",
      "trigger_event": "步骤 3 点击 Agree 后 startActivity(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Vulcan actions / Lets Vulcan lock the screen, open recent apps, quick settings and the power menu from a gesture. It reads no screen content.",
      "shown_text_zh": "Vulcan actions / 让 Vulcan 通过手势锁屏、打开最近任务、快捷设置与电源菜单；不读取屏幕内容。",
      "user_action_requested": "由用户在系统页手动将 Vulcan actions 开关打开（应用无法代点、无遮罩、无高仿开关页）",
      "code_anchor": "classes.dex 字符串 \"android.settings.ACCESSIBILITY_SETTINGS\"；res/xml/action_service.xml；res/values/strings.xml: action_service_label, action_service_description"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "dev.vulcanlauncher.ActionService（AccessibilityService）",
      "trigger_event": "用户再次触发已绑定的手势/快捷方式 → 服务执行 performGlobalAction（锁屏、最近任务、通知/快捷设置面板、电源菜单）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务按用户请求执行单一全局动作；仅监听本包 typeWindowStateChanged 事件，不读取窗口内容，无自点确认、无撤权阻断",
      "user_action_requested": "无需额外操作；可在系统设置中随时关闭",
      "code_anchor": "dev.vulcanlauncher.ActionService#onAccessibilityEvent / res/xml/action_service.xml (canRetrieveWindowContent=false, packageNames=dev.vulcanlauncher)"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内的原生说明对话框：标题 strings.xml/accessibility_title（Turn on the accessibility service），正文 strings.xml/accessibility_text（含用途、隐私承诺、可选授权与撤权说明）",
    "系统无障碍服务列表项：服务标签 action_service_label（Vulcan actions）与 android:description=action_service_description（经 res/xml/action_service.xml 的 android:description 引用）",
    "桌面设置页相关条目：strings.xml 的 page_accessibility（Accessibility settings）、perm_accessibility（Accessibility service）、perm_accessibility_info（Screen lock, recent apps and the power menu from gestures）",
    "无 assets 内本地 HTML 引导页、无远端 WebView 页面、无悬浮窗/遮罩层承载该引导文案（Manifest 无 INTERNET 与 SYSTEM_ALERT_WINDOW 权限）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Turn on the accessibility service",
      "text_zh": "开启无障碍服务",
      "source_location": "res/values/strings.xml: accessibility_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Vulcan uses the AccessibilityService API only when you trigger a gesture or shortcut to lock the screen, open recent apps, notifications, quick settings or the power menu.\n\nThe service does not read screen content, record your interactions, or collect or share personal data. It only performs the action you request. Access is optional; the rest of the launcher works without it. You can turn it off at any time in Android Accessibility settings.\n\nTap Agree and open settings to continue, then enable Vulcan actions.",
      "text_zh": "Vulcan 仅在你通过手势或快捷方式触发锁屏、打开最近任务、通知、快捷设置或电源菜单时使用 AccessibilityService API。该服务不读取屏幕内容、不记录你的操作、不收集或共享个人数据，只执行你请求的动作。授权是可选的，桌面其余功能无需授权即可使用，你也可随时在 Android 无障碍设置中关闭。点「同意并打开设置」继续，然后启用 Vulcan actions。",
      "source_location": "res/values/strings.xml: accessibility_text",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Agree and open settings",
      "text_zh": "同意并打开设置",
      "source_location": "res/values/strings.xml / classes.dex（预筛字符串命中）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Lets Vulcan lock the screen, open recent apps, quick settings and the power menu from a gesture. It reads no screen content.",
      "text_zh": "让 Vulcan 通过手势锁屏、打开最近任务、快捷设置与电源菜单。它不读取屏幕内容。",
      "source_location": "res/values/strings.xml: action_service_description（res/xml/action_service.xml android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Screen lock, recent apps and the power menu from gestures",
      "text_zh": "通过手势实现锁屏、最近任务与电源菜单",
      "source_location": "res/values/strings.xml: perm_accessibility_info",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "A home screen with no network access: no ads, analytics or tracking. Everything stays on this device.",
      "text_zh": "一个无网络访问的桌面：没有广告、分析和追踪。一切都留在本设备上。",
      "source_location": "res/values/strings.xml: about_text",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无重跳循环：未授权或从系统设置返回后不主动再弹窗、无 onResume 死循环、无定时器拉起；仅在用户再次主动选择需要无障碍的动作时才会重新展示说明弹窗，桌面其余功能正常可用（accessibility_text 明示 Access is optional）",
    "overlay_or_fake_settings": "无。Manifest 未申请 SYSTEM_ALERT_WINDOW，无半透明遮罩层，无高仿系统无障碍开关页；跳转目标为真实系统 android.settings.ACCESSIBILITY_SETTINGS",
    "restricted_settings_13plus_coaching": "无。代码中未见 android.settings.APPLICATION_DETAILS_SETTINGS 及「右上角菜单允许受限设置」类分步教学文案，也无 Session 安装器绕过逻辑",
    "post_grant_anti_removal": "无。未见获权后自点确认、自授权或通过 GLOBAL_ACTION_BACK/HOME 阻断撤权；PERFORM_GLOBAL_ACTION 仅用于执行用户请求的锁屏/最近任务/电源菜单动作",
    "benign_graceful_degradation": "有。授权为可选，未开启时仅相关手势动作不可用，桌面启动器核心功能（应用抽屉、页面、文件夹、壁纸等）完全正常；用户可随时在系统无障碍设置中关闭服务"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在用户首次为某手势/快捷方式选择需无障碍的动作（如 Screen lock / Recent apps / Power menu）后立即拉起 UTG 采集；或在监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间及返回前台时各采集一次",
    "key_pages_to_capture": [
      {
        "page_role": "引导说明弹窗页（原生 Dialog）",
        "page_identifier": "MainActivity 之上的原生 AlertDialog，标题 'Turn on the accessibility service'，含 Agree and open settings 按钮",
        "why_most_useful": "该页一次性呈现用途、隐私承诺与可跳过声明，是判断是否诱导（恐吓/假更新/清理伪装）的唯一文案载体",
        "observable_utg_signals": ["标题与正文是否与 strings.xml accessibility_text 一致", "是否存在取消/返回按钮，是否可关闭", "是否存在夸大危害、假安全、倒计时等恐吓性措辞"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已安装服务中的 'Vulcan actions' 条目及其 description 文本",
        "why_most_useful": "验证服务标签与说明是否与实际能力一致，是否存在标签伪装或空白挤出排序技巧",
        "observable_utg_signals": ["服务标签与 android:description 原文", "开关初始为关闭（应用未代点）", "是否存在叠加在设置页之上的悬浮引导层"]
      },
      {
        "page_role": "跳转后返回前台的桌面页",
        "page_identifier": "MainActivity 恢复前台（launcher 界面）",
        "why_most_useful": "区分良性降级与拒绝循环：观察返回后是否立即重复弹窗或反复跳设置页",
        "observable_utg_signals": ["返回后 3~5 秒内是否再次出现同一弹窗", "是否出现持续遮罩或不可退出的页面", "手势动作是否静默失效（降级）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。纯静态加壳不阻挡运行期 UTG，而本包本身未加壳未加密；应用无 INTERNET 权限，不存在远端下发文案导致 UTG 看到的内容与静态资源不一致的情况；唯一可见性限制是本轮 MCP 代码服务连接失败，改用 androguard 定向核验，未做全量调用图还原。"
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
    "res/xml/action_service.xml（canRetrieveWindowContent=false, packageNames=dev.vulcanlauncher, accessibilityEventTypes=typeWindowStateChanged）",
    "res/values/strings.xml: accessibility_title / accessibility_text（引导弹窗文案与 Agree and open settings 声明）",
    "res/values/strings.xml: action_service_label / action_service_description（系统无障碍列表标签与说明）",
    "classes.dex 字符串 android.settings.ACCESSIBILITY_SETTINGS（跳转系统无障碍设置的 Intent action）",
    "AndroidManifest.xml: service dev.vulcanlauncher.ActionService（BIND_ACCESSIBILITY_SERVICE，exported=true）",
    "dev.vulcanlauncher.ActionService#onAccessibilityEvent（获权后按用户请求执行全局动作）"
  ]
}
```

</details>
