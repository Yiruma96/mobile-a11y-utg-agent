# BN_047__5303b2ac80｜系统效率与通用辅助 — SwiftSlate

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：100.8s

## 1. 一句话核心结论

- **核心申请方式**：SwiftSlate 仅在用户点击 Dashboard 的 Enable 按钮时跳转系统无障碍设置页，并以服务状态卡片与可关闭的故障提示做说明，无遮罩、无强制、无受限设置教学。
- **静态可见性说明**：全部关键路径静态可见：Manifest、res/xml/accessibility_service_config.xml、res/values/strings.xml 明文，跳转逻辑位于 R8 混淆后的 iv.a()（上下文可完整反编译），未发现加壳、AES 密文载荷或远端 HTML 引导页。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5303b2ac80c3861b05092494f593a267085636dfd34f37e00c3c7a8d5dce2597` |
| 包名 / 年份 | `com.musheer360.swiftslate` / 2025-2026 |
| 家族 / 品类 | **系统效率与通用辅助**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.musheer360.swiftslate_299.apk |
| 桌面显示名 | SwiftSlate |
| 引导页宣称品牌/身份 | SwiftSlate（真实开发者署名 Musheer Alam，F-Droid 开源 AI 文本助手） |
| 系统无障碍列表服务名 | SwiftSlate Assistant |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.musheer360.swiftslate.service.AssistantService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | Provides system-wide AI text replacements when trigger commands are typed. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.musheer360.swiftslate.MainActivity（Compose 单 Activity） | onCreate / LAUNCHER 启动 | 原生Activity | **原文**：SwiftSlate / Dashboard / Enable / Active / Inactive<br>**译注**：应用名 SwiftSlate；仪表盘页；启用按钮；已启用/未启用状态 | 浏览仪表盘，可自行选择点击 Enable 或忽略；无强制弹窗，无倒计时 | `com.musheer360.swiftslate.MainActivity#onCreate` |
| 2 | 业务功能触发 | Dashboard 服务状态卡片（基于 c5.j 的 AccessibilityManager 查询结果） | 界面渲染/状态刷新，onAccessibilityStateChanged 回调 | 原生Activity | **原文**：Enable / Active / Inactive<br>**译注**：启用 / 已启用 / 未启用 | 用户点击 Enable 按钮；存在隐式跳过（不点即可正常使用应用设置页） | `c5#j` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 用户点击 Enable 后的协程 case 0：清除 service_died_at、置状态为 false，再 startActivity | 系统无障碍页 | **原文**：无（应用侧未注入任何覆盖文案）<br>**译注**：跳转至系统无障碍设置页，由用户自行找到并开启服务 | 用户在系统页面手动开启「SwiftSlate Assistant」；可随时返回不开启 | `iv#a` |
| 4 | 引导说明页 | 系统无障碍服务列表条目（服务元数据） | 系统读取 res/xml/accessibility_service_config.xml 与 strings | 系统无障碍页 | **原文**：SwiftSlate Assistant / Provides system-wide AI text replacements when trigger commands are typed.<br>**译注**：SwiftSlate 助手 / 在输入触发指令时提供系统级 AI 文本替换。 | 用户阅读说明后决定是否开启 | `res/xml/accessibility_service_config.xml, res/values/strings.xml (accessibility_service_desc, accessibility_service_label)` |
| 5 | 拒权反馈循环 | MainActivity Dashboard（状态卡片回退为 Inactive） | 用户从系统设置返回，c5.j 重新查询已启用服务列表 | 原生Activity | **原文**：Inactive / Enable<br>**译注**：未启用 / 启用 | 无强制要求；仅显示状态，用户可继续使用其他功能 | `c5#j, qd#r` |
| 6 | 获权后动作 | com.musheer360.swiftslate.service.AssistantService | 系统绑定服务 → onServiceConnected | 原生Activity | 无 | 无额外动作；用户可随时在系统设置中关闭 | `com.musheer360.swiftslate.service.AssistantService#onServiceConnected` |
| 7 | 拒权反馈循环 | MainActivity 对话框（服务异常终止提示） | ru1.uncaughtException 写入 service_died_at 后，qd.r 读取并驱动界面弹出 | 原生Dialog | **原文**：SwiftSlate was interrupted / The background service stopped unexpectedly. Re-enable it in accessibility settings to keep using commands. / Dismiss<br>**译注**：SwiftSlate 被中断 / 后台服务意外停止，请到无障碍设置中重新启用以便继续使用命令。/ 关闭 | 用户可点击 Dismiss 关闭；仅告知故障，不自动重跳设置页 | `ru1#uncaughtException, qd#r, res/values/strings.xml (dashboard_service_killed_title/message/dismiss)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml 中 accessibility_service_desc / accessibility_service_label → 呈现于系统无障碍服务列表条目（服务名 + 说明）
- MainActivity（Compose）Dashboard 服务状态卡片：service_enable / service_status_active / service_status_inactive
- MainActivity 内原生 Dialog：dashboard_service_killed_title + dashboard_service_killed_message + dashboard_service_killed_dismiss（可关闭的故障告知）
- res/xml/accessibility_service_config.xml：android:description 指向上述字符串，供系统设置展示
- 未出现：WebView 本地/远端 HTML 引导页、悬浮窗遮罩、仿系统开关页、通知栏引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Provides system-wide AI text replacements when trigger commands are typed. | 在输入触发指令时提供系统级 AI 文本替换。 | `res/values/strings.xml → accessibility_service_desc` | 良性透明说明 |
| en | SwiftSlate Assistant | SwiftSlate 助手 | `res/values/strings.xml → accessibility_service_label` | 良性透明说明 |
| en | SwiftSlate was interrupted | SwiftSlate 被中断 | `res/values/strings.xml → dashboard_service_killed_title` | 良性透明说明 |
| en | The background service stopped unexpectedly. Re-enable it in accessibility settings to keep using commands. | 后台服务意外停止，请到无障碍设置中重新启用以便继续使用命令。 | `res/values/strings.xml → dashboard_service_killed_message` | 故障恐吓 |
| en | Dismiss | 关闭 | `res/values/strings.xml → dashboard_service_killed_dismiss` | 良性透明说明 |
| en | Enable | 启用 | `res/values/strings.xml → service_enable` | 良性透明说明 |
| en | Add an API key to get started. | 添加 API 密钥以开始使用。 | `res/values/strings.xml → dashboard_add_key_hint` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性安全降级：用户从系统设置返回后 c5.j 仅重新查询 AccessibilityManager 已启用服务列表，Dashboard 显示 Inactive，不重跳设置页、无定时器拉起；无 onResume 死循环。
- **遮罩叠层 / 高仿系统设置页**：无：未使用 TYPE_ACCESSIBILITY_OVERLAY、未申请悬浮窗权限、未发现仿系统无障碍开关页或半透明引导遮罩。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（全包未出现 ACTION_APPLICATION_DETAILS_SETTINGS，亦无 Session 安装器绕过逻辑）
- **获权后即时行为与防撤权机制**：无（未发现 performGlobalAction / GLOBAL_ACTION_BACK / GLOBAL_ACTION_HOME 干预撤权，onDestroy 仅做状态清理）
- **良性降级 / 替代方案**：未开启服务时应用设置、命令管理、API Key 配置及 PROCESS_TEXT 手动调用路径仍可用，仅系统级键入触发失效；服务崩溃后以可关闭的提示告知并可选择忽略。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Intent action == android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 调用（唯一跳转点，位于 iv.a case 0），或冷启动后 Dashboard 上 service_enable 按钮点击；两者均可稳定捕获到引导链路。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区；代码经 R8 混淆但控制流完整可见，无加壳/密文载荷/远端下发文案，运行期 UTG 可完整覆盖。唯一需注意：若仅观察冷启动而不点击 Enable，将看不到设置跳转，易误判为『无引导』。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（服务名与说明）** | Settings → Accessibility → 已下载的服务中出现 'SwiftSlate Assistant' 及描述文本 | 系统无障碍列表的服务名与 android:description 是判定身份一致性与用途透明度的最直接证据，可识别空白/同形字伪装或虚假 isAccessibilityTool 说明。 | 服务标签 SwiftSlate Assistant；描述 Provides system-wide AI text replacements when trigger commands are typed.；无其他包名相似条目/无多别名条目 |
| **跳转前 Dashboard 服务状态卡片** | MainActivity 中 Enable / Active / Inactive 状态组件 | 可区分『用户点击触发』与『冷启动强制弹窗』，并确认无遮罩层覆盖。 | Enable 按钮文本；Inactive/Active 状态文本；页面无全屏半透明浮层节点 |
| **设置页后压栈遮罩页（预期不存在）** | 从系统设置返回后 800ms 内前台窗口是否为应用自绘悬浮/遮罩窗口 | 验证是否存在叠层指引或高仿系统页；本应用预期为纯系统设置页，若出现遮罩即为异常偏离。 | 前台窗口包名仍为 com.musheer360.swiftslate 的悬浮窗口；窗口类型为 TYPE_ACCESSIBILITY_OVERLAY；页面文本与系统无障碍设置高度相似 |
| **服务异常终止提示对话框** | MainActivity 内标题为 'SwiftSlate was interrupted' 的 Dialog | 确认该提示是否可关闭、是否带强制跳转按钮，判断是否构成拒权/故障恐吓循环。 | Dismiss 按钮可点击关闭；对话框无『去开启』强制唯一按钮；关闭后不再自动重弹 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `iv#a`
- `c5#j`
- `qd#r`
- `ru1#uncaughtException`
- `com.musheer360.swiftslate.MainActivity#onCreate`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验，未启动动态分析）

**总体判断：未发现诱导/强制开启无障碍权限的行为，属透明、用户主动触发的良性实现。**

- **入口与身份一致**：桌面名 `SwiftSlate`（`app_name`）、无障碍服务标签 `SwiftSlate Assistant`（`accessibility_service_label`）、`android:description` 明确说明用途（"Provides system-wide AI text replacements when trigger commands are typed."），三者语义一致，无空白/换行挤出、无同形字、无多 activity-alias 伪装。Manifest 仅 `MainActivity`（LAUNCHER）+ `ProcessTextActivity`（PROCESS_TEXT/VIEW）。
- **唯一跳转点**：[iv.a()](<resource-unit:#1.dex1 code:iv#a>) 中 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，且仅在 `case 0` 分支执行——即由用户点击 Dashboard 的 `Enable`（`service_enable`）按钮触发的协程恢复点；`default` 分支仅清理 `service_died_at` 状态、不跳转。**全包未出现 `ACTION_APPLICATION_DETAILS_SETTINGS`**，即无 Android 13+ 受限设置分步教学。
- **无遮罩/无悬浮/无 WebView**：未发现 `TYPE_ACCESSIBILITY_OVERLAY`、`performGlobalAction`、`GLOBAL_ACTION_BACK/HOME`、悬浮窗类型或任何 WebView 加载本地/远端 HTML 的引导页。
- **拒绝后行为良性降级**：[c5.j()](<resource-unit:#1.dex1 code:c5#j>) 通过 `AccessibilityManager.getEnabledAccessibilityServiceList(16)` 轮询本包服务是否启用，Dashboard 仅显示 `Active`/`Inactive`（`service_status_active`/`service_status_inactive`），无 `onResume` 死循环重跳、无定时器拉起。
- **异常反馈可取消**：[ru1.uncaughtException](<resource-unit:#1.dex1 code:ru1#uncaughtException>) 记录 `service_died_at`，[qd.r()](<resource-unit:#1.dex1 code:qd#r>) 读取后返回状态对象，界面弹出标题 `SwiftSlate was interrupted` 的对话框，含 `Dismiss` 按钮（`dashboard_service_killed_dismiss`），文案为故障说明+提示重新启用，属"故障告知"而非恐吓式强迫。
- **能力边界**：`isAccessibilityTool="true"` 与 `canRetrieveWindowContent="true"`、事件类型仅 `typeViewTextChanged`，与其"键入触发词替换文本"的真实功能相符，非伪造 isAccessibilityTool；服务 `onServiceConnected` 仅初始化命令仓库与网络客户端，`onDestroy` 做状态清理，无自授权、无阻止撤权。
- **覆盖边界**：应用为 R8 混淆（类名 `iv`/`qd`/`c5`），但控制流与字符串资源完整静态可见，未发现加壳、AES 密文载荷或远端下发引导文案；未做动态复现（无在线设备需求，静态证据已闭环）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键路径静态可见：Manifest、res/xml/accessibility_service_config.xml、res/values/strings.xml 明文，跳转逻辑位于 R8 混淆后的 iv.a()（上下文可完整反编译），未发现加壳、AES 密文载荷或远端 HTML 引导页。",
  "summary_one_liner": "SwiftSlate 仅在用户点击 Dashboard 的 Enable 按钮时跳转系统无障碍设置页，并以服务状态卡片与可关闭的故障提示做说明，无遮罩、无强制、无受限设置教学。",
  "disguise_identity": {
    "app_display_name": "SwiftSlate",
    "claimed_brand_or_persona": "SwiftSlate（真实开发者署名 Musheer Alam，F-Droid 开源 AI 文本助手）",
    "a11y_service_label": "SwiftSlate Assistant",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.musheer360.swiftslate.MainActivity（Compose 单 Activity）",
      "trigger_event": "onCreate / LAUNCHER 启动",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "SwiftSlate / Dashboard / Enable / Active / Inactive",
      "shown_text_zh": "应用名 SwiftSlate；仪表盘页；启用按钮；已启用/未启用状态",
      "user_action_requested": "浏览仪表盘，可自行选择点击 Enable 或忽略；无强制弹窗，无倒计时",
      "code_anchor": "com.musheer360.swiftslate.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "Dashboard 服务状态卡片（基于 c5.j 的 AccessibilityManager 查询结果）",
      "trigger_event": "界面渲染/状态刷新，onAccessibilityStateChanged 回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Enable / Active / Inactive",
      "shown_text_zh": "启用 / 已启用 / 未启用",
      "user_action_requested": "用户点击 Enable 按钮；存在隐式跳过（不点即可正常使用应用设置页）",
      "code_anchor": "c5#j"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户点击 Enable 后的协程 case 0：清除 service_died_at、置状态为 false，再 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧未注入任何覆盖文案）",
      "shown_text_zh": "跳转至系统无障碍设置页，由用户自行找到并开启服务",
      "user_action_requested": "用户在系统页面手动开启「SwiftSlate Assistant」；可随时返回不开启",
      "code_anchor": "iv#a"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "系统无障碍服务列表条目（服务元数据）",
      "trigger_event": "系统读取 res/xml/accessibility_service_config.xml 与 strings",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "SwiftSlate Assistant / Provides system-wide AI text replacements when trigger commands are typed.",
      "shown_text_zh": "SwiftSlate 助手 / 在输入触发指令时提供系统级 AI 文本替换。",
      "user_action_requested": "用户阅读说明后决定是否开启",
      "code_anchor": "res/xml/accessibility_service_config.xml, res/values/strings.xml (accessibility_service_desc, accessibility_service_label)"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity Dashboard（状态卡片回退为 Inactive）",
      "trigger_event": "用户从系统设置返回，c5.j 重新查询已启用服务列表",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Inactive / Enable",
      "shown_text_zh": "未启用 / 启用",
      "user_action_requested": "无强制要求；仅显示状态，用户可继续使用其他功能",
      "code_anchor": "c5#j, qd#r"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.musheer360.swiftslate.service.AssistantService",
      "trigger_event": "系统绑定服务 → onServiceConnected",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务初始化命令仓库、网络客户端并开始监听 typeViewTextChanged 事件，无自点击确认、无阻止撤权行为",
      "user_action_requested": "无额外动作；用户可随时在系统设置中关闭",
      "code_anchor": "com.musheer360.swiftslate.service.AssistantService#onServiceConnected"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 对话框（服务异常终止提示）",
      "trigger_event": "ru1.uncaughtException 写入 service_died_at 后，qd.r 读取并驱动界面弹出",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "SwiftSlate was interrupted / The background service stopped unexpectedly. Re-enable it in accessibility settings to keep using commands. / Dismiss",
      "shown_text_zh": "SwiftSlate 被中断 / 后台服务意外停止，请到无障碍设置中重新启用以便继续使用命令。/ 关闭",
      "user_action_requested": "用户可点击 Dismiss 关闭；仅告知故障，不自动重跳设置页",
      "code_anchor": "ru1#uncaughtException, qd#r, res/values/strings.xml (dashboard_service_killed_title/message/dismiss)"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml 中 accessibility_service_desc / accessibility_service_label → 呈现于系统无障碍服务列表条目（服务名 + 说明）",
    "MainActivity（Compose）Dashboard 服务状态卡片：service_enable / service_status_active / service_status_inactive",
    "MainActivity 内原生 Dialog：dashboard_service_killed_title + dashboard_service_killed_message + dashboard_service_killed_dismiss（可关闭的故障告知）",
    "res/xml/accessibility_service_config.xml：android:description 指向上述字符串，供系统设置展示",
    "未出现：WebView 本地/远端 HTML 引导页、悬浮窗遮罩、仿系统开关页、通知栏引导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Provides system-wide AI text replacements when trigger commands are typed.",
      "text_zh": "在输入触发指令时提供系统级 AI 文本替换。",
      "source_location": "res/values/strings.xml → accessibility_service_desc",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "SwiftSlate Assistant",
      "text_zh": "SwiftSlate 助手",
      "source_location": "res/values/strings.xml → accessibility_service_label",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "SwiftSlate was interrupted",
      "text_zh": "SwiftSlate 被中断",
      "source_location": "res/values/strings.xml → dashboard_service_killed_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The background service stopped unexpectedly. Re-enable it in accessibility settings to keep using commands.",
      "text_zh": "后台服务意外停止，请到无障碍设置中重新启用以便继续使用命令。",
      "source_location": "res/values/strings.xml → dashboard_service_killed_message",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Dismiss",
      "text_zh": "关闭",
      "source_location": "res/values/strings.xml → dashboard_service_killed_dismiss",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable",
      "text_zh": "启用",
      "source_location": "res/values/strings.xml → service_enable",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Add an API key to get started.",
      "text_zh": "添加 API 密钥以开始使用。",
      "source_location": "res/values/strings.xml → dashboard_add_key_hint",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性安全降级：用户从系统设置返回后 c5.j 仅重新查询 AccessibilityManager 已启用服务列表，Dashboard 显示 Inactive，不重跳设置页、无定时器拉起；无 onResume 死循环。",
    "overlay_or_fake_settings": "无：未使用 TYPE_ACCESSIBILITY_OVERLAY、未申请悬浮窗权限、未发现仿系统无障碍开关页或半透明引导遮罩。",
    "restricted_settings_13plus_coaching": "无（全包未出现 ACTION_APPLICATION_DETAILS_SETTINGS，亦无 Session 安装器绕过逻辑）",
    "post_grant_anti_removal": "无（未发现 performGlobalAction / GLOBAL_ACTION_BACK / GLOBAL_ACTION_HOME 干预撤权，onDestroy 仅做状态清理）",
    "benign_graceful_degradation": "未开启服务时应用设置、命令管理、API Key 配置及 PROCESS_TEXT 手动调用路径仍可用，仅系统级键入触发失效；服务崩溃后以可关闭的提示告知并可选择忽略。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Intent action == android.settings.ACCESSIBILITY_SETTINGS 的 startActivity 调用（唯一跳转点，位于 iv.a case 0），或冷启动后 Dashboard 上 service_enable 按钮点击；两者均可稳定捕获到引导链路。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（服务名与说明）",
        "page_identifier": "Settings → Accessibility → 已下载的服务中出现 'SwiftSlate Assistant' 及描述文本",
        "why_most_useful": "系统无障碍列表的服务名与 android:description 是判定身份一致性与用途透明度的最直接证据，可识别空白/同形字伪装或虚假 isAccessibilityTool 说明。",
        "observable_utg_signals": ["服务标签 SwiftSlate Assistant", "描述 Provides system-wide AI text replacements when trigger commands are typed.", "无其他包名相似条目/无多别名条目"]
      },
      {
        "page_role": "跳转前 Dashboard 服务状态卡片",
        "page_identifier": "MainActivity 中 Enable / Active / Inactive 状态组件",
        "why_most_useful": "可区分『用户点击触发』与『冷启动强制弹窗』，并确认无遮罩层覆盖。",
        "observable_utg_signals": ["Enable 按钮文本", "Inactive/Active 状态文本", "页面无全屏半透明浮层节点"]
      },
      {
        "page_role": "设置页后压栈遮罩页（预期不存在）",
        "page_identifier": "从系统设置返回后 800ms 内前台窗口是否为应用自绘悬浮/遮罩窗口",
        "why_most_useful": "验证是否存在叠层指引或高仿系统页；本应用预期为纯系统设置页，若出现遮罩即为异常偏离。",
        "observable_utg_signals": ["前台窗口包名仍为 com.musheer360.swiftslate 的悬浮窗口", "窗口类型为 TYPE_ACCESSIBILITY_OVERLAY", "页面文本与系统无障碍设置高度相似"]
      },
      {
        "page_role": "服务异常终止提示对话框",
        "page_identifier": "MainActivity 内标题为 'SwiftSlate was interrupted' 的 Dialog",
        "why_most_useful": "确认该提示是否可关闭、是否带强制跳转按钮，判断是否构成拒权/故障恐吓循环。",
        "observable_utg_signals": ["Dismiss 按钮可点击关闭", "对话框无『去开启』强制唯一按钮", "关闭后不再自动重弹"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区；代码经 R8 混淆但控制流完整可见，无加壳/密文载荷/远端下发文案，运行期 UTG 可完整覆盖。唯一需注意：若仅观察冷启动而不点击 Enable，将看不到设置跳转，易误判为『无引导』。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "iv#a",
    "c5#j",
    "qd#r",
    "ru1#uncaughtException",
    "com.musheer360.swiftslate.MainActivity#onCreate",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
