# BN_014__b1702e69f0｜按键映射与手势导航 — Key Mapper

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：141.7s

## 1. 一句话核心结论

- **核心申请方式**：Key Mapper 在主界面以错误提示条＋原生说明对话框的方式，向用户解释按键重映射为何需要无障碍服务，并由用户点击按钮后一次性跳转系统无障碍设置页，失败时降级为 ADB/WRITE_SECURE_SETTINGS 或 Expert Mode 方案，全程无遮罩、无拒权循环、无撤权对抗。
- **静态可见性说明**：无障碍引导全链路（入口 Activity 意图分发、跳转方法、失败回调对话框、系统无障碍配置与全部文案）均可在 classes.dex 与 res/ 中静态完整还原；无加壳、无 VMP、无 AES 密文载荷、无远端 HTML，R8 仅做类名重命名不影响逻辑还原。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b1702e69f0f083a9f88a0ffb4e22d92ce99b72307155d941451eb6cc820a7125` |
| 包名 / 年份 | `io.github.sds100.keymapper` / 2025-2026 |
| 家族 / 品类 | **按键映射与手势导航**（同池样本数：1） |
| 原始来源标识 | https://github.com/keymapperorg/KeyMapper/releases/download/v4.7.1/keymapper-4.7.1-foss.apk |
| 桌面显示名 | Key Mapper |
| 引导页宣称品牌/身份 | Key Mapper（开源按键重映射工具，真实身份，未冒用任何第三方品牌） |
| 系统无障碍列表服务名 | 未设置 android:label，系统无障碍列表中显示为应用名 "Key Mapper"（组件 io.github.sds100.keymapper/.system.accessibility.MyAccessibilityService） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `io.github.sds100.keymapper.system.accessibility.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Key Mapper requires the use of an accessibility service so that it can detect and change what your button presses do while you are outside of the app. Your key maps will only work once you have enabled the accessibility service. It must also be turned on to create a trigger and test actions. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | io.github.sds100.keymapper.MainActivity（基类 j20，Compose 单 Activity 架构） | onCreate / onNewIntent 调用 j20.s(Intent)，按 action 字符串分发 ACTION_SHOW_ACCESSIBILITY_SETTINGS_NOT_FOUND_DIALOG 与 ACTION_START_SYSTEM_BRIDGE | 原生Activity | **原文**：无（本步仅做意图分发，不直接展示引导文案）<br>**译注**：冷启动进入主界面，不弹出任何强制引导层 | 无强制动作；可直接使用应用其余界面 | `j20.s(android.content.Intent)` |
| 2 | 业务功能触发 | 主界面（Home）错误/状态提示条 + "Enable accessibility service" 按钮 | 界面根据无障碍服务启用状态渲染：未启用时展示错误提示条与使能按钮（isAccessibilityServiceEnabled 状态流驱动） | 原生Activity | **原文**：The accessibility service needs to be turned on for your key maps to work! / Enable accessibility service<br>**译注**：无障碍服务需要开启，你的按键映射才能生效 / 启用无障碍服务 | 点击"Enable accessibility service"按钮（提示条非模态，可忽略并继续浏览/编辑按键映射） | `res/values/strings.xml: home_error_accessibility_service_is_disabled, button_enable_accessibility_service` |
| 3 | 引导说明页 | 原生说明对话框（标题 Accessibility service must be enabled，正文复用 accessibility_service_explanation） | 用户点击使能按钮/相关设置项时由 ViewModel 触发展示说明对话框 | 原生Dialog | **原文**：Key Mapper requires the use of an accessibility service so that it can detect and change what your button presses do while you are outside of the app. Your key maps will only work once you have enabled the accessibility service. It must also be turned on to create a trigger and test actions.<br>**译注**：Key Mapper 需要使用无障碍服务，以便在应用之外检测并改变按键按下后的行为。只有启用无障碍服务后按键映射才会生效；录制触发器和测试动作也必须开启该服务。 | 阅读说明后确认（对话框按钮为 Fix / Proceed 类常规确认），可返回取消 | `res/values/strings.xml: dialog_title_accessibility_service_explanation, dialog_message_accessibility_service_explanation, accessibility_service_explanation` |
| 4 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（android.settings.ACCESSIBILITY_SETTINGS） | d4.e() 被 o01.b() / d4.a / d4.h 调用；仅当未授予 WRITE_SECURE_SETTINGS 时才走跳转分支（日志 "Restarting service by opening accessibility settings"） | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS（Intent action，非应用自绘界面）<br>**译注**：直接打开系统原生无障碍设置列表，用户在其中手动找到 Key Mapper 并开启 | 在系统页面手动开启 Key Mapper 无障碍服务；应用不叠加遮罩、不代点、不模拟系统开关 | `d4.e()（new Intent("android.settings.ACCESSIBILITY_SETTINGS"), setFlags(0x50800000), context.startActivity）` |
| 5 | 拒权反馈循环 | 系统无障碍列表项的说明文案（config_accessibility_service.xml 的 android:description） | 用户停留在系统无障碍列表时由系统渲染服务描述 | 系统无障碍页 | **原文**：Key Mapper requires the use of an accessibility service so that it can detect and change what your button presses do while you are outside of the app.<br>**译注**：与步骤 3 同一段真实功能说明，向系统页面如实披露能力范围 | 用户可自由返回；应用不会 onResume 重跳或定时拉起 | `res/xml/config_accessibility_service.xml` |
| 6 | 拒权反馈循环 | 原生对话框 Can't find the accessibility settings page（仅在系统无该设置页时） | d4.e() 抛 ActivityNotFoundException 返回 false → dv3.invokeSuspend 发出 io.github.sds100.keymapper.base.ACTION_SHOW_ACCESSIBILITY_SETTINGS_NOT_FOUND_DIALOG → j20.s(Intent) 分发至 y9 ViewModel 弹窗 | 原生Dialog | **原文**：Your device doesn't seem to have an accessibility services settings page. You can set up Expert Mode or run the ADB command "adb shell pm grant io.github.sds100.keymapper android.permission.WRITE_SECURE_SETTINGS".<br>**译注**：你的设备似乎没有无障碍服务设置页。你可以配置 Expert Mode，或执行 ADB 命令 adb shell pm grant io.github.sds100.keymapper android.permission.WRITE_SECURE_SETTINGS。 | 选择替代授权路径或关闭对话框（无强制重试、无恐吓话术） | `dv3.invokeSuspend, j20.s(android.content.Intent), res/values/strings.xml: dialog_title_cant_find_accessibility_settings_page, dialog_message_cant_find_accessibility_settings_page` |
| 7 | 获权后动作 | 主界面状态提示条 / 崩溃重启通知 | 无障碍服务状态变更回调（AccessibilityServiceEvent 流）后主界面刷新；服务被系统杀死时发通知 | 原生Activity | **原文**：The accessibility service is enabled! Your key maps should work. / Your phone killed Key Mapper when it was in the background or it crashed!<br>**译注**：无障碍服务已启用！你的按键映射应该可以工作了。/ 你的手机在 Key Mapper 处于后台时杀掉了它，或它崩溃了！ | 仅展示状态与可选的重启指引（关闭再开启服务），不自动代点确认、不阻止用户撤权 | `res/values/strings.xml: home_success_accessibility_service_is_enabled, home_error_accessibility_service_is_crashed, notification_accessibility_service_crashed_*` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 主界面（MainActivity，Compose）非模态错误提示条：home_error_accessibility_service_is_disabled / home_error_accessibility_service_is_crashed + 按钮 button_enable_accessibility_service
- 原生说明对话框：标题 dialog_title_accessibility_service_explanation（Accessibility service must be enabled），正文复用 accessibility_service_explanation（dialog_message_accessibility_service_explanation 指向同一字符串）
- 系统无障碍设置列表项描述：res/xml/config_accessibility_service.xml 的 android:description="@string/accessibility_service_explanation"
- 系统无该设置页时的降级对话框：dialog_title_cant_find_accessibility_settings_page / dialog_message_cant_find_accessibility_settings_page（含 ADB 命令原文）
- Expert Mode 设置向导分步页：expert_mode_setup_wizard_title（Setup wizard）+ expert_mode_setup_wizard_step_n（Step %d of %d）+ enable_accessibility_service_title/description/button
- 通知栏：notification_accessibility_service_crashed_title/text（服务被系统杀死后提示点击重启）
- 崩溃/重启说明对话框：dialog_title_key_mapper_crashed（Accessibility service needs restarting）/ dialog_message_key_mapper_crashed / dialog_message_restart_accessibility_service

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Key Mapper requires the use of an accessibility service so that it can detect and change what your button presses do while you are outside of the app. Your key maps will only work once you have enabled the accessibility service. It must also be turned on to create a trigger and test actions. | Key Mapper 需要使用无障碍服务，以便在应用之外检测并改变按键按下后的行为。只有启用无障碍服务后按键映射才会生效；录制触发器和测试动作也必须开启该服务。 | `res/values/strings.xml → accessibility_service_explanation（同时供 dialog_message_accessibility_service_explanation 与 config_accessibility_service.xml 的 android:description 使用）` | 良性透明说明 |
| en | Accessibility service must be enabled | 必须启用无障碍服务 | `res/values/strings.xml → dialog_title_accessibility_service_explanation` | 良性透明说明 |
| en | The accessibility service needs to be turned on for your key maps to work! | 无障碍服务需要开启，你的按键映射才能生效！ | `res/values/strings.xml → home_error_accessibility_service_is_disabled` | 良性透明说明 |
| en | Enable accessibility service | 启用无障碍服务 | `res/values/strings.xml → button_enable_accessibility_service` | 良性透明说明 |
| en | Your device doesn't seem to have an accessibility services settings page. You can set up Expert Mode or run the ADB command "adb shell pm grant io.github.sds100.keymapper android.permission.WRITE_SECURE_SETTINGS". | 你的设备似乎没有无障碍服务设置页。你可以配置 Expert Mode，或执行 ADB 命令 adb shell pm grant io.github.sds100.keymapper android.permission.WRITE_SECURE_SETTINGS。 | `res/values/strings.xml → dialog_message_cant_find_accessibility_settings_page` | 受限设置分步教学 |
| en | Key Mapper uses this service to help with setup. It's also needed for ordinary key maps. | Key Mapper 使用该服务协助完成配置，普通按键映射同样需要它。 | `res/values/strings.xml → expert_mode_setup_wizard_enable_accessibility_service_description` | 良性透明说明 |
| en | Your phone killed Key Mapper when it was in the background or it crashed! | 你的手机在 Key Mapper 处于后台时杀掉了它，或它崩溃了！ | `res/values/strings.xml → home_error_accessibility_service_is_crashed` | 良性透明说明 |
| en | The accessibility service is enabled! Your key maps should work. | 无障碍服务已启用！你的按键映射应该可以工作了。 | `res/values/strings.xml → home_success_accessibility_service_is_enabled` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环机制：跳转仅由用户点击触发一次；从系统设置返回后主界面仅刷新状态提示条（home_error_* / home_success_*），不会 onResume 重跳、无定时器拉起、无模态阻塞。若系统不存在无障碍设置页，d4.e() 捕获 ActivityNotFoundException 返回 false，经 dv3.invokeSuspend 发出 ACTION_SHOW_ACCESSIBILITY_SETTINGS_NOT_FOUND_DIALOG，j20.s(Intent) 弹出降级说明对话框后流程结束。
- **遮罩叠层 / 高仿系统设置页**：无。Manifest 未申请 SYSTEM_ALERT_WINDOW / TYPE_APPLICATION_OVERLAY，全包 WebView 零命中，无自绘仿系统无障碍开关页；跳转后完全交给系统原生设置界面。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包无 ACTION_APPLICATION_DETAILS_SETTINGS 引用，不存在"进应用详情→右上角菜单→允许受限设置"的分步教学；仅在设备缺少无障碍设置页时提供 ADB 命令与 Expert Mode 两条替代路径。
- **获权后即时行为与防撤权机制**：无
- **良性降级 / 替代方案**：有。多级降级：① 若已授予 WRITE_SECURE_SETTINGS（o01.b 通过 zj.b(n64.p) 判定），直接走 Settings.Secure 读写 enabled_accessibility_services 而不跳设置页；② 系统无无障碍设置页时提示执行 adb shell pm grant ... WRITE_SECURE_SETTINGS；③ 提供 Expert Mode 设置向导（Step %d of %d，含 ADB/无线调试/本地网络分步引导，带 Skip 按钮）作为不依赖无障碍服务的替代模式；④ 服务被系统杀死时仅发通知提示手动关闭再开启。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳拉起时机为：① 检测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（即 d4.e() 执行后）以及随后约 500–800ms 系统无障碍列表页已渲染时；② 冷启动 MainActivity 后主界面出现 "The accessibility service needs to be turned on for your key maps to work!" 提示条时；③ 出现 "Can't find the accessibility settings page" 对话框时。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。引导全链路为原生控件＋系统设置页，纯 UTG 文本即可判别；包内无 WebView、无远端 HTML、无悬浮窗，也不存在一阶段 Dropper 或加密二阶段载荷。唯一需注意：无障碍服务本身具备 canRetrieveWindowContent / canPerformGestures / canRequestFilterKeyEvents 能力，若需评估获权后的实际输入操控与内容读取行为，需在授权后另行做运行期行为观测，本视角（UTG 引导流转）不覆盖。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **主界面未授权状态提示条页** | io.github.sds100.keymapper.MainActivity 首屏，含文本 The accessibility service needs to be turned on for your key maps to work! 与按钮 Enable accessibility service | 确认引导是常驻非模态提示（可忽略）还是不可取消的阻塞层，是区分良性按需引导与强制诱导的第一判据 | 提示条是否为非模态、可滚动离开；是否存在全屏遮罩或屏蔽返回键；按钮文案是否为中性使能措辞 |
| **跳转前原生说明对话框** | 标题 Accessibility service must be enabled，正文以 Key Mapper requires the use of an accessibility service 开头的系统原生 Dialog | 捕获该对话框可核对说明文本是否如实披露能力范围、是否含恐吓/假更新/假安全话术，以及是否提供取消路径 | 对话框为系统原生样式而非 WebView 自绘；正文与 android:description 完全一致；存在取消/返回可关闭 |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载的服务列表中条目 "Key Mapper"（组件 io.github.sds100.keymapper/.system.accessibility.MyAccessibilityService） | 验证系统列表中显示名与描述是否诚实、是否存在空白名/同形字/伪造 isAccessibilityTool 等身份混淆手法 | 条目显示名是否为 Key Mapper 而非空/乱码/冒充品牌；描述文本是否为真实功能说明；是否存在异常多条目（多 alias） |
| **设置页返回后的状态反馈页** | 返回 MainActivity 后的提示条，成功为 The accessibility service is enabled! Your key maps should work.，失败回到未启用提示 | 判断是否存在拒权后立即重跳设置页的强制循环或反复弹窗骚扰 | 返回后是否再次自动跳设置页；是否出现密集重复弹窗；提示是否仅为静态状态展示 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `d4.e() —— 唯一无障碍设置页跳转实现（new Intent("android.settings.ACCESSIBILITY_SETTINGS"), setFlags(0x50800000), startActivity，ActivityNotFoundException 捕获）`
- `o01.b() —— 跳转决策分支：已授予 WRITE_SECURE_SETTINGS 时走 Settings.Secure 直改，否则调用 d4.e() 跳设置页`
- `d4.a(d4, n01) —— 通过 Settings.Secure 读写 enabled_accessibility_services 完成服务启停（含 disableSelf 回退）`
- `dv3.invokeSuspend —— 发出 io.github.sds100.keymapper.base.ACTION_SHOW_ACCESSIBILITY_SETTINGS_NOT_FOUND_DIALOG 降级信号`
- `j20.s(android.content.Intent) —— MainActivity 意图分发（onCreate/onNewIntent 调用），弹出降级对话框`
- `res/xml/config_accessibility_service.xml —— android:description=@string/accessibility_service_explanation，canRetrieveWindowContent/canPerformGestures/canRequestFilterKeyEvents 声明`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验，工具调用 12 次后结束调查。以下为结论。

## 结论要点

- **申请方式为透明、按需触发**：核心跳转只有一处，即 `d4.e()` 中的 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，flags = `0x50800000`（`FLAG_ACTIVITY_NEW_TASK | NO_HISTORY | EXCLUDE_FROM_RECENTS`），不驻留最近任务。
- **全程无 WebView、无悬浮窗、无高仿设置页**：全包 `WebView` 零命中；Manifest 无 `SYSTEM_ALERT_WINDOW`/`TYPE_APPLICATION_OVERLAY` 权限；`assets/` 仅 `whats-new*.txt` 与 dexopt 基线文件，无 HTML 教学页。
- **无 `ACTION_APPLICATION_DETAILS_SETTINGS`**：应用不引导用户进应用详情页手动放行"受限设置"，与静态预筛的 `JUMP_A11Y_SETTINGS` 一致，未见 13+ 受限设置分步教学。
- **无拒权死循环、无撤权对抗**：跳转失败（`ActivityNotFoundException`）仅记录日志并返回，另由 `dv3.invokeSuspend` 发出 `ACTION_SHOW_ACCESSIBILITY_SETTINGS_NOT_FOUND_DIALOG`，`j20.s(Intent)` 收到后弹"找不到无障碍设置页"对话框，并给出 `adb shell pm grant ... WRITE_SECURE_SETTINGS` 的**替代授权路径**（良性降级）。
- **身份诚实**：桌面名 `Key Mapper`，无障碍服务无独立 label（系统列表回落为应用名），`android:description` 为真实功能说明；无空白/换行挤出、无同形字、无多 alias、无伪造 `isAccessibilityTool`。
- **代码混淆仅为 R8 常规重命名**（`d4`/`j20`/`dv3`/`o01`），服务类全名与组件名未被改写，可静态完整还原。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（入口 Activity 意图分发、跳转方法、失败回调对话框、系统无障碍配置与全部文案）均可在 classes.dex 与 res/ 中静态完整还原；无加壳、无 VMP、无 AES 密文载荷、无远端 HTML，R8 仅做类名重命名不影响逻辑还原。",
  "summary_one_liner": "Key Mapper 在主界面以错误提示条＋原生说明对话框的方式，向用户解释按键重映射为何需要无障碍服务，并由用户点击按钮后一次性跳转系统无障碍设置页，失败时降级为 ADB/WRITE_SECURE_SETTINGS 或 Expert Mode 方案，全程无遮罩、无拒权循环、无撤权对抗。",
  "disguise_identity": {
    "app_display_name": "Key Mapper",
    "claimed_brand_or_persona": "Key Mapper（开源按键重映射工具，真实身份，未冒用任何第三方品牌）",
    "a11y_service_label": "未设置 android:label，系统无障碍列表中显示为应用名 \"Key Mapper\"（组件 io.github.sds100.keymapper/.system.accessibility.MyAccessibilityService）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "io.github.sds100.keymapper.MainActivity（基类 j20，Compose 单 Activity 架构）",
      "trigger_event": "onCreate / onNewIntent 调用 j20.s(Intent)，按 action 字符串分发 ACTION_SHOW_ACCESSIBILITY_SETTINGS_NOT_FOUND_DIALOG 与 ACTION_START_SYSTEM_BRIDGE",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（本步仅做意图分发，不直接展示引导文案）",
      "shown_text_zh": "冷启动进入主界面，不弹出任何强制引导层",
      "user_action_requested": "无强制动作；可直接使用应用其余界面",
      "code_anchor": "j20.s(android.content.Intent)"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "主界面（Home）错误/状态提示条 + \"Enable accessibility service\" 按钮",
      "trigger_event": "界面根据无障碍服务启用状态渲染：未启用时展示错误提示条与使能按钮（isAccessibilityServiceEnabled 状态流驱动）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "The accessibility service needs to be turned on for your key maps to work! / Enable accessibility service",
      "shown_text_zh": "无障碍服务需要开启，你的按键映射才能生效 / 启用无障碍服务",
      "user_action_requested": "点击\"Enable accessibility service\"按钮（提示条非模态，可忽略并继续浏览/编辑按键映射）",
      "code_anchor": "res/values/strings.xml: home_error_accessibility_service_is_disabled, button_enable_accessibility_service"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "原生说明对话框（标题 Accessibility service must be enabled，正文复用 accessibility_service_explanation）",
      "trigger_event": "用户点击使能按钮/相关设置项时由 ViewModel 触发展示说明对话框",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Key Mapper requires the use of an accessibility service so that it can detect and change what your button presses do while you are outside of the app. Your key maps will only work once you have enabled the accessibility service. It must also be turned on to create a trigger and test actions.",
      "shown_text_zh": "Key Mapper 需要使用无障碍服务，以便在应用之外检测并改变按键按下后的行为。只有启用无障碍服务后按键映射才会生效；录制触发器和测试动作也必须开启该服务。",
      "user_action_requested": "阅读说明后确认（对话框按钮为 Fix / Proceed 类常规确认），可返回取消",
      "code_anchor": "res/values/strings.xml: dialog_title_accessibility_service_explanation, dialog_message_accessibility_service_explanation, accessibility_service_explanation"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "d4.e() 被 o01.b() / d4.a / d4.h 调用；仅当未授予 WRITE_SECURE_SETTINGS 时才走跳转分支（日志 \"Restarting service by opening accessibility settings\"）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS（Intent action，非应用自绘界面）",
      "shown_text_zh": "直接打开系统原生无障碍设置列表，用户在其中手动找到 Key Mapper 并开启",
      "user_action_requested": "在系统页面手动开启 Key Mapper 无障碍服务；应用不叠加遮罩、不代点、不模拟系统开关",
      "code_anchor": "d4.e()（new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), setFlags(0x50800000), context.startActivity）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "系统无障碍列表项的说明文案（config_accessibility_service.xml 的 android:description）",
      "trigger_event": "用户停留在系统无障碍列表时由系统渲染服务描述",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Key Mapper requires the use of an accessibility service so that it can detect and change what your button presses do while you are outside of the app.",
      "shown_text_zh": "与步骤 3 同一段真实功能说明，向系统页面如实披露能力范围",
      "user_action_requested": "用户可自由返回；应用不会 onResume 重跳或定时拉起",
      "code_anchor": "res/xml/config_accessibility_service.xml"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "原生对话框 Can't find the accessibility settings page（仅在系统无该设置页时）",
      "trigger_event": "d4.e() 抛 ActivityNotFoundException 返回 false → dv3.invokeSuspend 发出 io.github.sds100.keymapper.base.ACTION_SHOW_ACCESSIBILITY_SETTINGS_NOT_FOUND_DIALOG → j20.s(Intent) 分发至 y9 ViewModel 弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Your device doesn't seem to have an accessibility services settings page. You can set up Expert Mode or run the ADB command \"adb shell pm grant io.github.sds100.keymapper android.permission.WRITE_SECURE_SETTINGS\".",
      "shown_text_zh": "你的设备似乎没有无障碍服务设置页。你可以配置 Expert Mode，或执行 ADB 命令 adb shell pm grant io.github.sds100.keymapper android.permission.WRITE_SECURE_SETTINGS。",
      "user_action_requested": "选择替代授权路径或关闭对话框（无强制重试、无恐吓话术）",
      "code_anchor": "dv3.invokeSuspend, j20.s(android.content.Intent), res/values/strings.xml: dialog_title_cant_find_accessibility_settings_page, dialog_message_cant_find_accessibility_settings_page"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "主界面状态提示条 / 崩溃重启通知",
      "trigger_event": "无障碍服务状态变更回调（AccessibilityServiceEvent 流）后主界面刷新；服务被系统杀死时发通知",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "The accessibility service is enabled! Your key maps should work. / Your phone killed Key Mapper when it was in the background or it crashed!",
      "shown_text_zh": "无障碍服务已启用！你的按键映射应该可以工作了。/ 你的手机在 Key Mapper 处于后台时杀掉了它，或它崩溃了！",
      "user_action_requested": "仅展示状态与可选的重启指引（关闭再开启服务），不自动代点确认、不阻止用户撤权",
      "code_anchor": "res/values/strings.xml: home_success_accessibility_service_is_enabled, home_error_accessibility_service_is_crashed, notification_accessibility_service_crashed_*"
    }
  ],
  "text_presentation_locations": [
    "主界面（MainActivity，Compose）非模态错误提示条：home_error_accessibility_service_is_disabled / home_error_accessibility_service_is_crashed + 按钮 button_enable_accessibility_service",
    "原生说明对话框：标题 dialog_title_accessibility_service_explanation（Accessibility service must be enabled），正文复用 accessibility_service_explanation（dialog_message_accessibility_service_explanation 指向同一字符串）",
    "系统无障碍设置列表项描述：res/xml/config_accessibility_service.xml 的 android:description=\"@string/accessibility_service_explanation\"",
    "系统无该设置页时的降级对话框：dialog_title_cant_find_accessibility_settings_page / dialog_message_cant_find_accessibility_settings_page（含 ADB 命令原文）",
    "Expert Mode 设置向导分步页：expert_mode_setup_wizard_title（Setup wizard）+ expert_mode_setup_wizard_step_n（Step %d of %d）+ enable_accessibility_service_title/description/button",
    "通知栏：notification_accessibility_service_crashed_title/text（服务被系统杀死后提示点击重启）",
    "崩溃/重启说明对话框：dialog_title_key_mapper_crashed（Accessibility service needs restarting）/ dialog_message_key_mapper_crashed / dialog_message_restart_accessibility_service"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Key Mapper requires the use of an accessibility service so that it can detect and change what your button presses do while you are outside of the app. Your key maps will only work once you have enabled the accessibility service. It must also be turned on to create a trigger and test actions.",
      "text_zh": "Key Mapper 需要使用无障碍服务，以便在应用之外检测并改变按键按下后的行为。只有启用无障碍服务后按键映射才会生效；录制触发器和测试动作也必须开启该服务。",
      "source_location": "res/values/strings.xml → accessibility_service_explanation（同时供 dialog_message_accessibility_service_explanation 与 config_accessibility_service.xml 的 android:description 使用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service must be enabled",
      "text_zh": "必须启用无障碍服务",
      "source_location": "res/values/strings.xml → dialog_title_accessibility_service_explanation",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The accessibility service needs to be turned on for your key maps to work!",
      "text_zh": "无障碍服务需要开启，你的按键映射才能生效！",
      "source_location": "res/values/strings.xml → home_error_accessibility_service_is_disabled",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable accessibility service",
      "text_zh": "启用无障碍服务",
      "source_location": "res/values/strings.xml → button_enable_accessibility_service",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Your device doesn't seem to have an accessibility services settings page. You can set up Expert Mode or run the ADB command \"adb shell pm grant io.github.sds100.keymapper android.permission.WRITE_SECURE_SETTINGS\".",
      "text_zh": "你的设备似乎没有无障碍服务设置页。你可以配置 Expert Mode，或执行 ADB 命令 adb shell pm grant io.github.sds100.keymapper android.permission.WRITE_SECURE_SETTINGS。",
      "source_location": "res/values/strings.xml → dialog_message_cant_find_accessibility_settings_page",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Key Mapper uses this service to help with setup. It's also needed for ordinary key maps.",
      "text_zh": "Key Mapper 使用该服务协助完成配置，普通按键映射同样需要它。",
      "source_location": "res/values/strings.xml → expert_mode_setup_wizard_enable_accessibility_service_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Your phone killed Key Mapper when it was in the background or it crashed!",
      "text_zh": "你的手机在 Key Mapper 处于后台时杀掉了它，或它崩溃了！",
      "source_location": "res/values/strings.xml → home_error_accessibility_service_is_crashed",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The accessibility service is enabled! Your key maps should work.",
      "text_zh": "无障碍服务已启用！你的按键映射应该可以工作了。",
      "source_location": "res/values/strings.xml → home_success_accessibility_service_is_enabled",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环机制：跳转仅由用户点击触发一次；从系统设置返回后主界面仅刷新状态提示条（home_error_* / home_success_*），不会 onResume 重跳、无定时器拉起、无模态阻塞。若系统不存在无障碍设置页，d4.e() 捕获 ActivityNotFoundException 返回 false，经 dv3.invokeSuspend 发出 ACTION_SHOW_ACCESSIBILITY_SETTINGS_NOT_FOUND_DIALOG，j20.s(Intent) 弹出降级说明对话框后流程结束。",
    "overlay_or_fake_settings": "无。Manifest 未申请 SYSTEM_ALERT_WINDOW / TYPE_APPLICATION_OVERLAY，全包 WebView 零命中，无自绘仿系统无障碍开关页；跳转后完全交给系统原生设置界面。",
    "restricted_settings_13plus_coaching": "无。全包无 ACTION_APPLICATION_DETAILS_SETTINGS 引用，不存在\"进应用详情→右上角菜单→允许受限设置\"的分步教学；仅在设备缺少无障碍设置页时提供 ADB 命令与 Expert Mode 两条替代路径。",
    "post_grant_anti_removal": "无",
    "benign_graceful_degradation": "有。多级降级：① 若已授予 WRITE_SECURE_SETTINGS（o01.b 通过 zj.b(n64.p) 判定），直接走 Settings.Secure 读写 enabled_accessibility_services 而不跳设置页；② 系统无无障碍设置页时提示执行 adb shell pm grant ... WRITE_SECURE_SETTINGS；③ 提供 Expert Mode 设置向导（Step %d of %d，含 ADB/无线调试/本地网络分步引导，带 Skip 按钮）作为不依赖无障碍服务的替代模式；④ 服务被系统杀死时仅发通知提示手动关闭再开启。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳拉起时机为：① 检测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（即 d4.e() 执行后）以及随后约 500–800ms 系统无障碍列表页已渲染时；② 冷启动 MainActivity 后主界面出现 \"The accessibility service needs to be turned on for your key maps to work!\" 提示条时；③ 出现 \"Can't find the accessibility settings page\" 对话框时。",
    "key_pages_to_capture": [
      {
        "page_role": "主界面未授权状态提示条页",
        "page_identifier": "io.github.sds100.keymapper.MainActivity 首屏，含文本 The accessibility service needs to be turned on for your key maps to work! 与按钮 Enable accessibility service",
        "why_most_useful": "确认引导是常驻非模态提示（可忽略）还是不可取消的阻塞层，是区分良性按需引导与强制诱导的第一判据",
        "observable_utg_signals": ["提示条是否为非模态、可滚动离开", "是否存在全屏遮罩或屏蔽返回键", "按钮文案是否为中性使能措辞"]
      },
      {
        "page_role": "跳转前原生说明对话框",
        "page_identifier": "标题 Accessibility service must be enabled，正文以 Key Mapper requires the use of an accessibility service 开头的系统原生 Dialog",
        "why_most_useful": "捕获该对话框可核对说明文本是否如实披露能力范围、是否含恐吓/假更新/假安全话术，以及是否提供取消路径",
        "observable_utg_signals": ["对话框为系统原生样式而非 WebView 自绘", "正文与 android:description 完全一致", "存在取消/返回可关闭"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载的服务列表中条目 \"Key Mapper\"（组件 io.github.sds100.keymapper/.system.accessibility.MyAccessibilityService）",
        "why_most_useful": "验证系统列表中显示名与描述是否诚实、是否存在空白名/同形字/伪造 isAccessibilityTool 等身份混淆手法",
        "observable_utg_signals": ["条目显示名是否为 Key Mapper 而非空/乱码/冒充品牌", "描述文本是否为真实功能说明", "是否存在异常多条目（多 alias）"]
      },
      {
        "page_role": "设置页返回后的状态反馈页",
        "page_identifier": "返回 MainActivity 后的提示条，成功为 The accessibility service is enabled! Your key maps should work.，失败回到未启用提示",
        "why_most_useful": "判断是否存在拒权后立即重跳设置页的强制循环或反复弹窗骚扰",
        "observable_utg_signals": ["返回后是否再次自动跳设置页", "是否出现密集重复弹窗", "提示是否仅为静态状态展示"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。引导全链路为原生控件＋系统设置页，纯 UTG 文本即可判别；包内无 WebView、无远端 HTML、无悬浮窗，也不存在一阶段 Dropper 或加密二阶段载荷。唯一需注意：无障碍服务本身具备 canRetrieveWindowContent / canPerformGestures / canRequestFilterKeyEvents 能力，若需评估获权后的实际输入操控与内容读取行为，需在授权后另行做运行期行为观测，本视角（UTG 引导流转）不覆盖。"
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
    "d4.e() —— 唯一无障碍设置页跳转实现（new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), setFlags(0x50800000), startActivity，ActivityNotFoundException 捕获）",
    "o01.b() —— 跳转决策分支：已授予 WRITE_SECURE_SETTINGS 时走 Settings.Secure 直改，否则调用 d4.e() 跳设置页",
    "d4.a(d4, n01) —— 通过 Settings.Secure 读写 enabled_accessibility_services 完成服务启停（含 disableSelf 回退）",
    "dv3.invokeSuspend —— 发出 io.github.sds100.keymapper.base.ACTION_SHOW_ACCESSIBILITY_SETTINGS_NOT_FOUND_DIALOG 降级信号",
    "j20.s(android.content.Intent) —— MainActivity 意图分发（onCreate/onNewIntent 调用），弹出降级对话框",
    "res/xml/config_accessibility_service.xml —— android:description=@string/accessibility_service_explanation，canRetrieveWindowContent/canPerformGestures/canRequestFilterKeyEvents 声明"
  ]
}
```

</details>
