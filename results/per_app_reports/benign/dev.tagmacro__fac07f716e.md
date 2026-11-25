# BN_049__fac07f716e｜系统效率与通用辅助 — TagMacro

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：106.1s

## 1. 一句话核心结论

- **核心申请方式**：TagMacro 把无障碍服务当作可选的能力开关：仅在用户已启用含 Signal/WhatsApp/锁屏动作的宏时才在宏页提示，并在设置页提供带状态、可忽略的“Open accessibility settings”按钮跳转系统原生设置页，附带条件式的受限设置说明，全程无强制、无遮罩、无伪造界面。
- **静态可见性说明**：全部引导逻辑位于单一 classes.dex（360 个类，未混淆、无加固、无动态加载/加密载荷），界面由代码内 Ui 组件构建（无 WebView、无远端 HTML），文字集中于 MainActivity 硬编码字符串与 res/values/strings.xml，完整静态可见。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fac07f716e2bfefc836ea8a597d69297b539066fe34e15b69afaa17d42908525` |
| 包名 / 年份 | `dev.tagmacro` / 2025-2026 |
| 家族 / 品类 | **系统效率与通用辅助**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/dev.tagmacro_3.apk |
| 桌面显示名 | TagMacro |
| 引导页宣称品牌/身份 | TagMacro（F-Droid 开源 NFC 宏工具，真实身份） |
| 系统无障碍列表服务名 | TagMacro messaging |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `dev.tagmacro.SignalService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：org.thoughtcrime.securesms,com.whatsapp |
| 共现高危权限 | `CALL_PHONE, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Lets TagMacro send Signal and WhatsApp messages, share WhatsApp live location, and lock the screen when one of your macros asks it to. It only receives events from Signal and WhatsApp and does nothing unless a macro is running one of those actions. TagMacro has no internet access. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | dev.tagmacro.MainActivity（默认“Macros”宏列表页） | onCreate/render() 渲染宏列表；onResume 仅 updateReaderMode + Waits.rescheduleAll + render，不跳转任何设置页 | 原生Activity | **原文**：无（冷启动无引导弹窗、无遮罩、无自动跳转）<br>**译注**：无 | 无需任何操作，可自由浏览或退出 | `dev.tagmacro.MainActivity.onResume / MainActivity.macrosScreen` |
| 2 | 业务功能触发 | MainActivity.macrosScreen 顶部危险色卡片（仅当存在启用的 SIGNAL/WHATSAPP/WHATSAPP_LIVE/LOCK_SCREEN 动作且 SignalService.isEnabled()==false） | 渲染宏列表时检测到动作类型属于需无障碍的集合且服务未启用 | 原生Activity | **原文**：Some actions can't run yet / Signal, WhatsApp and lock-screen actions need the TagMacro accessibility service turned on. / Open Settings<br>**译注**：部分动作暂时无法运行 / Signal、WhatsApp 与锁屏动作需要开启 TagMacro 无障碍服务 / 打开设置 | 可选点击“Open Settings”进入应用设置页；卡片不阻塞列表，可直接忽略并使用其它宏 | `dev.tagmacro.MainActivity.macrosScreen` |
| 3 | 引导说明页 | MainActivity 设置标签页 → “Permissions” sectionCard | 用户切到设置页 render() | 原生Activity | **原文**：Permissions / Each one is optional, and only needed for the actions listed. TagMacro has no internet permission. / Accessibility service / Allowed \| Not allowed / For Signal, WhatsApp and Lock the screen. It only receives events from Signal and WhatsApp, and only reads the screen while a macro is sending. / Open accessibility settings<br>**译注**：权限 / 每一项都是可选的，仅对应列出的动作才需要。TagMacro 没有网络权限。/ 无障碍服务 / 已允许｜未允许 / 用于 Signal、WhatsApp 与锁屏。它只接收来自 Signal 和 WhatsApp 的事件，且仅在宏正在发送时读取屏幕。/ 打开无障碍设置 | 阅读说明后自行决定是否点击按钮；无倒计时、无必须勾选、可返回退出 | `dev.tagmacro.MainActivity.settingsScreen → permissionBlock(...)` |
| 4 | 跳无障碍设置 | 系统原生设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（其中的“TagMacro messaging”条目） | 点击“Open accessibility settings”按钮 | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS（系统页面，应用仅发起 Intent）；服务条目名取自 res/values/strings.xml a11y_label = "TagMacro messaging"<br>**译注**：跳转系统无障碍服务列表，用户需手动找到“TagMacro messaging”并开启 | 在系统页手动开启开关；也可直接返回应用不开启 | `dev.tagmacro.MainActivity.settingsScreen$lambda$1` |
| 5 | 拒权反馈循环（受限设置分步教学） | 设置页无障碍卡片内的附加说明 + textButton“Open App info”→ 系统应用详情页 Settings.ACTION_APPLICATION_DETAILS_SETTINGS | 无障碍卡片渲染时 granted==false（即未开启，包括被 Android 13+ 置灰的情形） | 原生Activity + 系统应用详情页 | **原文**：If the switch is greyed out as a restricted setting: open App info, tap the ⋮ menu, choose "Allow restricted settings", then try again. / Open App info<br>**译注**：如果开关因“受限设置”而置灰：打开应用信息，点击 ⋮ 菜单，选择“允许受限设置”，然后重试。/ 打开应用信息 | 可选按说明在系统应用信息页授权；无强制、无反复自动重跳 | `dev.tagmacro.MainActivity.settingsScreen$lambda$0 / settingsScreen$lambda$0$0` |
| 6 | 拒权反馈循环 | MainActivity.onResume → render()（返回应用后的状态刷新） | 从系统设置/应用详情返回触发的 onResume | 原生Activity | **原文**：无（仅重算 SignalService.Companion.isEnabled 并刷新 Allowed / Not allowed 标签）<br>**译注**：无提示，状态回显；不重跳设置页、不弹二次挽留 | 无 | `dev.tagmacro.MainActivity.onResume / MainActivity.render` |
| 7 | 获权后动作 | 设置页“Troubleshooting”区块（采集调试）与 SignalService 实际工作 | 点击调试按钮：若服务未启用则 toast，已启用则 setCaptureRequested(true) | 原生Activity + 无障碍 Service（SignalService） | **原文**：Turn on the accessibility service first / Now open the Signal or WhatsApp screen you want to inspect, then come back here / Shows what the accessibility service sees in Signal or WhatsApp, so you can update the labels above.<br>**译注**：请先开启无障碍服务 / 现在打开你想查看的 Signal 或 WhatsApp 界面，然后回到这里 / 显示无障碍服务在 Signal 或 WhatsApp 中看到的内容，便于你更新上面的标签。 | 可选使用调试采集功能，用于校准宏中的界面标签 | `dev.tagmacro.MainActivity.settingsScreen$lambda$34 / dev.tagmacro.SignalService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 设置页“Permissions”区块：sectionCard 说明“Each one is optional…” + permissionBlock 标题“Accessibility service”、状态“Allowed/Not allowed”、说明“For Signal, WhatsApp and Lock the screen…”与按钮“Open accessibility settings”（全部为代码内硬编码字符串）
- MainActivity 宏列表页顶部危险色卡片（条件出现，非模态）：“Some actions can't run yet” + “Signal, WhatsApp and lock-screen actions need the TagMacro accessibility service turned on.” + 按钮“Open Settings”
- MainActivity 设置页无障碍卡片附加说明：“If the switch is greyed out as a restricted setting: open App info, tap the ⋮ menu, choose "Allow restricted settings", then try again.” + 文字按钮“Open App info”
- 系统无障碍服务列表条目：服务标签 res/values/strings.xml a11y_label="TagMacro messaging"，说明 a11y_description（经 res/xml/accessibility_config.xml 的 android:description 引用）
- 设置页“Troubleshooting”区块与 toast 提示：“Shows what the accessibility service sees…”“Turn on the accessibility service first”“Now open the Signal or WhatsApp screen you want to inspect, then come back here”
- 无 WebView / HTML / 悬浮窗 / 自绘高仿设置页承载任何引导文字（全包无 TYPE_APPLICATION_OVERLAY 代码、无 assets 页面）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Lets TagMacro send Signal and WhatsApp messages, share WhatsApp live location, and lock the screen when one of your macros asks it to. It only receives events from Signal and WhatsApp and does nothing unless a macro is running one of those actions. TagMacro has no internet access. | 允许 TagMacro 在你某个宏要求时发送 Signal 与 WhatsApp 消息、共享 WhatsApp 实时位置并锁屏。它只接收来自 Signal 和 WhatsApp 的事件，且除非某个宏正在执行这些动作，否则不做任何事。TagMacro 没有网络访问权限。 | `res/values/strings.xml → a11y_description（被 res/xml/accessibility_config.xml 引用）` | 良性透明说明 |
| en | Each one is optional, and only needed for the actions listed. TagMacro has no internet permission. | 每一项都是可选的，仅对应列出的动作才需要。TagMacro 没有网络权限。 | `dev.tagmacro.MainActivity.settingsScreen（sectionCard 硬编码）` | 良性透明说明 |
| en | For Signal, WhatsApp and Lock the screen. It only receives events from Signal and WhatsApp, and only reads the screen while a macro is sending. | 用于 Signal、WhatsApp 与锁屏。它只接收来自 Signal 和 WhatsApp 的事件，并且仅在宏正在发送时读取屏幕。 | `dev.tagmacro.MainActivity.settingsScreen → permissionBlock(why)` | 良性透明说明 |
| en | Some actions can't run yet / Signal, WhatsApp and lock-screen actions need the TagMacro accessibility service turned on. / Open Settings | 部分动作暂时无法运行 / Signal、WhatsApp 与锁屏动作需要开启 TagMacro 无障碍服务 / 打开设置 | `dev.tagmacro.MainActivity.macrosScreen（硬编码）` | 良性透明说明 |
| en | If the switch is greyed out as a restricted setting: open App info, tap the ⋮ menu, choose "Allow restricted settings", then try again. | 如果开关因“受限设置”而置灰：打开应用信息，点击 ⋮ 菜单，选择“允许受限设置”，然后重试。 | `dev.tagmacro.MainActivity.settingsScreen$lambda$0（硬编码）` | 受限设置分步教学 |
| en | Turn on the accessibility service first / Now open the Signal or WhatsApp screen you want to inspect, then come back here | 请先开启无障碍服务 / 现在打开你想查看的 Signal 或 WhatsApp 界面，然后回到这里 | `dev.tagmacro.MainActivity.settingsScreen$lambda$34（toast 硬编码）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环：拒绝或从设置页返回后，onResume 仅重新渲染并刷新 Allowed/Not allowed 状态；宏页危险色卡片保持静态提示，不自动重跳、无定时器拉起、无二次挽留弹窗
- **遮罩叠层 / 高仿系统设置页**：无。全包无 TYPE_APPLICATION_OVERLAY / addView 到 WindowManager 的悬浮窗代码，无自绘无障碍开关页；跳转目标为系统原生 Settings.ACTION_ACCESSIBILITY_SETTINGS
- **Android 13+ 受限设置（Restricted Settings）应对**：有，但为条件式温和说明：设置页无障碍卡片在未开启时显示“If the switch is greyed out as a restricted setting: open App info, tap the ⋮ menu, choose "Allow restricted settings", then try again.”并提供“Open App info”按钮跳 Settings.ACTION_APPLICATION_DETAILS_SETTINGS；无 Session 安装器绕过、无诱导忽略安全警告
- **获权后即时行为与防撤权机制**：无。SignalService 未监听系统设置页、未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权，也未自点确认；撤权后应用仅降级提示
- **良性降级 / 替代方案**：有。权限区声明“Each one is optional, and only needed for the actions listed”；未开启无障碍时 NFC 标签读写、Wi-Fi/链接/联系人写入等宏仍可用，仅 Signal/WhatsApp/锁屏类动作被标注为暂不可运行（“Some actions can't run yet”），另有“Troubleshooting”采集提示引导用户自行校准

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS")) 时拉起 UTG，同时抓取跳转前 1~2 秒的应用内设置页快照；辅以冷启动后首屏快照以确认无自动跳转/无弹窗。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：无图片引导、无 WebView、无加固与动态加载，全部引导文案为可静态定位的明文字符串。唯一需注意的温和点是“受限设置分步教学”本身在纯 UTG 文本信号上可能与恶意诱导同构，须结合“是否有强制/遮罩/伪造UI/拒绝循环”综合判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前应用内设置页（Permissions 区块）** | dev.tagmacro.MainActivity，含“Permissions”“Accessibility service”“Allowed/Not allowed”“Open accessibility settings”文本与系统状态栏为应用自身包名 | 该页是全部无障碍引导文字的承载处，可判断是否存在恐吓/伪造系统UI/无取消按钮等诱导特征 | 文本“Each one is optional, and only needed for the actions listed.”与“TagMacro has no internet permission.”是否如实出现；是否存在“Open accessibility settings”以外的强制按钮或倒计时控件；页面是否为系统设置样式（状态栏/返回语义）而非自绘高仿页 |
| **系统无障碍服务列表项** | 系统设置 com.android.settings 的无障碍页，条目“TagMacro messaging”及其说明文本 | 核对服务标签与 description 是否与应用身份一致、是否被空白/同形字伪装或冒充系统/品牌组件 | 条目名是否严格为“TagMacro messaging”；说明文本是否与 strings.xml a11y_description 完全一致；是否同时出现多个可疑无障碍条目（多包伪装） |
| **宏列表页顶部危险色提示卡片** | dev.tagmacro.MainActivity 宏列表，“Some actions can't run yet”卡片与“Open Settings”按钮 | 判断引导是否为功能按需触发（需用户先启用含相关动作的宏），而非冷启动强制弹出 | 卡片出现条件是否依赖已有启用宏；是否可滚动离开/直接使用其它宏（非模态）；是否存在覆盖全屏的遮罩层 |
| **应用详情页（受限设置教学落地页）** | 系统 Settings.ACTION_APPLICATION_DETAILS_SETTINGS，包名 dev.tagmacro | 验证是否真的引导用户走系统“允许受限设置”流程，且未使用安装器/Session 绕过 | 是否停留在系统应用信息页（而非自绘仿页）；是否出现“允许受限设置”菜单项；返回后是否发生自动重跳循环 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `dev.tagmacro.MainActivity.settingsScreen$lambda$1（startActivity("android.settings.ACCESSIBILITY_SETTINGS")）`
- `dev.tagmacro.MainActivity.settingsScreen（permissionBlock 权限区块与无障碍说明文案）`
- `dev.tagmacro.MainActivity.settingsScreen$lambda$0 / settingsScreen$lambda$0$0（受限设置说明 + APPLICATION_DETAILS_SETTINGS 跳转）`
- `dev.tagmacro.MainActivity.macrosScreen（“Some actions can't run yet”按需提示卡片）`
- `res/xml/accessibility_config.xml（packageNames 限定 Signal/WhatsApp、canRetrieveWindowContent）`
- `res/values/strings.xml（a11y_label / a11y_description）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**性质判定：良性透明应用，未发现无障碍权限诱导/欺骗行为。**

1. **身份与范围如实披露**：桌面名 `TagMacro`、无障碍服务名 `TagMacro messaging`（`res/values/strings.xml` 的 `a11y_label`），`android:description` 明确写出“仅接收 Signal 与 WhatsApp 的事件、仅当宏执行相关动作时才工作、无网络访问”，与 [accessibility_config.xml](<resource-unit:#1 file:res/xml/accessibility_config.xml>) 中 `packageNames="org.thoughtcrime.securesms,com.whatsapp"`、`canRetrieveWindowContent=true` 的实际能力一致；Manifest 中确实**无 INTERNET 权限**，说明不假。
2. **无冷启动强制跳转**：`MainActivity.onCreate` 直接渲染宏列表，`onResume` 只做 `updateReaderMode / rescheduleAll / render`，不存在启动即弹窗或启动即跳 `ACCESSIBILITY_SETTINGS` 的路径。
3. **引导是“按需 + 可取消”**：只有当用户已启用某个含 `SIGNAL/WHATSAPP/WHATSAPP_LIVE/LOCK_SCREEN` 动作的宏、且服务未开时，宏页才出现危险色卡片“Some actions can't run yet…Open Settings”；设置页权限区块把无障碍与短信/电话/悬浮窗/修改系统设置并列为“Each one is optional”，带 `Allowed / Not allowed` 状态与显式按钮，用户可完全忽略。
4. **跳转点干净**：[settingsScreen$lambda$1](<resource-unit:#1.dex1 code:dev.tagmacro.MainActivity#settingsScreen$lambda$1>) 仅 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，跳系统原生设置页；`APPLICATION_DETAILS_SETTINGS` 仅用于“Open App info / 被永久拒绝后去应用详情”两个场景，无自建高仿开关页、无 WebView、无 Overlay（全包无 `TYPE_APPLICATION_OVERLAY` 代码，`SYSTEM_ALERT_WINDOW` 仅为“从宏启动其它应用”所需的声明）。
5. **有 Android 13+ 受限设置分步教学**（属 F-Droid 侧载通用说明，措辞为条件式“若开关置灰…”并附解释与 App info 入口），但**无恐吓话术、无拒绝死循环、无获权后自点确认或 GLOBAL_ACTION_BACK 阻止撤权**；返回应用后仅静默刷新状态。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于单一 classes.dex（360 个类，未混淆、无加固、无动态加载/加密载荷），界面由代码内 Ui 组件构建（无 WebView、无远端 HTML），文字集中于 MainActivity 硬编码字符串与 res/values/strings.xml，完整静态可见。",
  "summary_one_liner": "TagMacro 把无障碍服务当作可选的能力开关：仅在用户已启用含 Signal/WhatsApp/锁屏动作的宏时才在宏页提示，并在设置页提供带状态、可忽略的“Open accessibility settings”按钮跳转系统原生设置页，附带条件式的受限设置说明，全程无强制、无遮罩、无伪造界面。",
  "disguise_identity": {
    "app_display_name": "TagMacro",
    "claimed_brand_or_persona": "TagMacro（F-Droid 开源 NFC 宏工具，真实身份）",
    "a11y_service_label": "TagMacro messaging",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "dev.tagmacro.MainActivity（默认“Macros”宏列表页）",
      "trigger_event": "onCreate/render() 渲染宏列表；onResume 仅 updateReaderMode + Waits.rescheduleAll + render，不跳转任何设置页",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（冷启动无引导弹窗、无遮罩、无自动跳转）",
      "shown_text_zh": "无",
      "user_action_requested": "无需任何操作，可自由浏览或退出",
      "code_anchor": "dev.tagmacro.MainActivity.onResume / MainActivity.macrosScreen"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity.macrosScreen 顶部危险色卡片（仅当存在启用的 SIGNAL/WHATSAPP/WHATSAPP_LIVE/LOCK_SCREEN 动作且 SignalService.isEnabled()==false）",
      "trigger_event": "渲染宏列表时检测到动作类型属于需无障碍的集合且服务未启用",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Some actions can't run yet / Signal, WhatsApp and lock-screen actions need the TagMacro accessibility service turned on. / Open Settings",
      "shown_text_zh": "部分动作暂时无法运行 / Signal、WhatsApp 与锁屏动作需要开启 TagMacro 无障碍服务 / 打开设置",
      "user_action_requested": "可选点击“Open Settings”进入应用设置页；卡片不阻塞列表，可直接忽略并使用其它宏",
      "code_anchor": "dev.tagmacro.MainActivity.macrosScreen"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 设置标签页 → “Permissions” sectionCard",
      "trigger_event": "用户切到设置页 render()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Permissions / Each one is optional, and only needed for the actions listed. TagMacro has no internet permission. / Accessibility service / Allowed | Not allowed / For Signal, WhatsApp and Lock the screen. It only receives events from Signal and WhatsApp, and only reads the screen while a macro is sending. / Open accessibility settings",
      "shown_text_zh": "权限 / 每一项都是可选的，仅对应列出的动作才需要。TagMacro 没有网络权限。/ 无障碍服务 / 已允许｜未允许 / 用于 Signal、WhatsApp 与锁屏。它只接收来自 Signal 和 WhatsApp 的事件，且仅在宏正在发送时读取屏幕。/ 打开无障碍设置",
      "user_action_requested": "阅读说明后自行决定是否点击按钮；无倒计时、无必须勾选、可返回退出",
      "code_anchor": "dev.tagmacro.MainActivity.settingsScreen → permissionBlock(...)"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统原生设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（其中的“TagMacro messaging”条目）",
      "trigger_event": "点击“Open accessibility settings”按钮",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS（系统页面，应用仅发起 Intent）；服务条目名取自 res/values/strings.xml a11y_label = \"TagMacro messaging\"",
      "shown_text_zh": "跳转系统无障碍服务列表，用户需手动找到“TagMacro messaging”并开启",
      "user_action_requested": "在系统页手动开启开关；也可直接返回应用不开启",
      "code_anchor": "dev.tagmacro.MainActivity.settingsScreen$lambda$1"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环（受限设置分步教学）",
      "screen_or_component": "设置页无障碍卡片内的附加说明 + textButton“Open App info”→ 系统应用详情页 Settings.ACTION_APPLICATION_DETAILS_SETTINGS",
      "trigger_event": "无障碍卡片渲染时 granted==false（即未开启，包括被 Android 13+ 置灰的情形）",
      "ui_carrier": "原生Activity + 系统应用详情页",
      "shown_text_verbatim": "If the switch is greyed out as a restricted setting: open App info, tap the ⋮ menu, choose \"Allow restricted settings\", then try again. / Open App info",
      "shown_text_zh": "如果开关因“受限设置”而置灰：打开应用信息，点击 ⋮ 菜单，选择“允许受限设置”，然后重试。/ 打开应用信息",
      "user_action_requested": "可选按说明在系统应用信息页授权；无强制、无反复自动重跳",
      "code_anchor": "dev.tagmacro.MainActivity.settingsScreen$lambda$0 / settingsScreen$lambda$0$0"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onResume → render()（返回应用后的状态刷新）",
      "trigger_event": "从系统设置/应用详情返回触发的 onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅重算 SignalService.Companion.isEnabled 并刷新 Allowed / Not allowed 标签）",
      "shown_text_zh": "无提示，状态回显；不重跳设置页、不弹二次挽留",
      "user_action_requested": "无",
      "code_anchor": "dev.tagmacro.MainActivity.onResume / MainActivity.render"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "设置页“Troubleshooting”区块（采集调试）与 SignalService 实际工作",
      "trigger_event": "点击调试按钮：若服务未启用则 toast，已启用则 setCaptureRequested(true)",
      "ui_carrier": "原生Activity + 无障碍 Service（SignalService）",
      "shown_text_verbatim": "Turn on the accessibility service first / Now open the Signal or WhatsApp screen you want to inspect, then come back here / Shows what the accessibility service sees in Signal or WhatsApp, so you can update the labels above.",
      "shown_text_zh": "请先开启无障碍服务 / 现在打开你想查看的 Signal 或 WhatsApp 界面，然后回到这里 / 显示无障碍服务在 Signal 或 WhatsApp 中看到的内容，便于你更新上面的标签。",
      "user_action_requested": "可选使用调试采集功能，用于校准宏中的界面标签",
      "code_anchor": "dev.tagmacro.MainActivity.settingsScreen$lambda$34 / dev.tagmacro.SignalService"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 设置页“Permissions”区块：sectionCard 说明“Each one is optional…” + permissionBlock 标题“Accessibility service”、状态“Allowed/Not allowed”、说明“For Signal, WhatsApp and Lock the screen…”与按钮“Open accessibility settings”（全部为代码内硬编码字符串）",
    "MainActivity 宏列表页顶部危险色卡片（条件出现，非模态）：“Some actions can't run yet” + “Signal, WhatsApp and lock-screen actions need the TagMacro accessibility service turned on.” + 按钮“Open Settings”",
    "MainActivity 设置页无障碍卡片附加说明：“If the switch is greyed out as a restricted setting: open App info, tap the ⋮ menu, choose \"Allow restricted settings\", then try again.” + 文字按钮“Open App info”",
    "系统无障碍服务列表条目：服务标签 res/values/strings.xml a11y_label=\"TagMacro messaging\"，说明 a11y_description（经 res/xml/accessibility_config.xml 的 android:description 引用）",
    "设置页“Troubleshooting”区块与 toast 提示：“Shows what the accessibility service sees…”“Turn on the accessibility service first”“Now open the Signal or WhatsApp screen you want to inspect, then come back here”",
    "无 WebView / HTML / 悬浮窗 / 自绘高仿设置页承载任何引导文字（全包无 TYPE_APPLICATION_OVERLAY 代码、无 assets 页面）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Lets TagMacro send Signal and WhatsApp messages, share WhatsApp live location, and lock the screen when one of your macros asks it to. It only receives events from Signal and WhatsApp and does nothing unless a macro is running one of those actions. TagMacro has no internet access.",
      "text_zh": "允许 TagMacro 在你某个宏要求时发送 Signal 与 WhatsApp 消息、共享 WhatsApp 实时位置并锁屏。它只接收来自 Signal 和 WhatsApp 的事件，且除非某个宏正在执行这些动作，否则不做任何事。TagMacro 没有网络访问权限。",
      "source_location": "res/values/strings.xml → a11y_description（被 res/xml/accessibility_config.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Each one is optional, and only needed for the actions listed. TagMacro has no internet permission.",
      "text_zh": "每一项都是可选的，仅对应列出的动作才需要。TagMacro 没有网络权限。",
      "source_location": "dev.tagmacro.MainActivity.settingsScreen（sectionCard 硬编码）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "For Signal, WhatsApp and Lock the screen. It only receives events from Signal and WhatsApp, and only reads the screen while a macro is sending.",
      "text_zh": "用于 Signal、WhatsApp 与锁屏。它只接收来自 Signal 和 WhatsApp 的事件，并且仅在宏正在发送时读取屏幕。",
      "source_location": "dev.tagmacro.MainActivity.settingsScreen → permissionBlock(why)",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Some actions can't run yet / Signal, WhatsApp and lock-screen actions need the TagMacro accessibility service turned on. / Open Settings",
      "text_zh": "部分动作暂时无法运行 / Signal、WhatsApp 与锁屏动作需要开启 TagMacro 无障碍服务 / 打开设置",
      "source_location": "dev.tagmacro.MainActivity.macrosScreen（硬编码）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "If the switch is greyed out as a restricted setting: open App info, tap the ⋮ menu, choose \"Allow restricted settings\", then try again.",
      "text_zh": "如果开关因“受限设置”而置灰：打开应用信息，点击 ⋮ 菜单，选择“允许受限设置”，然后重试。",
      "source_location": "dev.tagmacro.MainActivity.settingsScreen$lambda$0（硬编码）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn on the accessibility service first / Now open the Signal or WhatsApp screen you want to inspect, then come back here",
      "text_zh": "请先开启无障碍服务 / 现在打开你想查看的 Signal 或 WhatsApp 界面，然后回到这里",
      "source_location": "dev.tagmacro.MainActivity.settingsScreen$lambda$34（toast 硬编码）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环：拒绝或从设置页返回后，onResume 仅重新渲染并刷新 Allowed/Not allowed 状态；宏页危险色卡片保持静态提示，不自动重跳、无定时器拉起、无二次挽留弹窗",
    "overlay_or_fake_settings": "无。全包无 TYPE_APPLICATION_OVERLAY / addView 到 WindowManager 的悬浮窗代码，无自绘无障碍开关页；跳转目标为系统原生 Settings.ACTION_ACCESSIBILITY_SETTINGS",
    "restricted_settings_13plus_coaching": "有，但为条件式温和说明：设置页无障碍卡片在未开启时显示“If the switch is greyed out as a restricted setting: open App info, tap the ⋮ menu, choose \"Allow restricted settings\", then try again.”并提供“Open App info”按钮跳 Settings.ACTION_APPLICATION_DETAILS_SETTINGS；无 Session 安装器绕过、无诱导忽略安全警告",
    "post_grant_anti_removal": "无。SignalService 未监听系统设置页、未使用 GLOBAL_ACTION_BACK/HOME 阻止撤权，也未自点确认；撤权后应用仅降级提示",
    "benign_graceful_degradation": "有。权限区声明“Each one is optional, and only needed for the actions listed”；未开启无障碍时 NFC 标签读写、Wi-Fi/链接/联系人写入等宏仍可用，仅 Signal/WhatsApp/锁屏类动作被标注为暂不可运行（“Some actions can't run yet”），另有“Troubleshooting”采集提示引导用户自行校准"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivity(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")) 时拉起 UTG，同时抓取跳转前 1~2 秒的应用内设置页快照；辅以冷启动后首屏快照以确认无自动跳转/无弹窗。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前应用内设置页（Permissions 区块）",
        "page_identifier": "dev.tagmacro.MainActivity，含“Permissions”“Accessibility service”“Allowed/Not allowed”“Open accessibility settings”文本与系统状态栏为应用自身包名",
        "why_most_useful": "该页是全部无障碍引导文字的承载处，可判断是否存在恐吓/伪造系统UI/无取消按钮等诱导特征",
        "observable_utg_signals": ["文本“Each one is optional, and only needed for the actions listed.”与“TagMacro has no internet permission.”是否如实出现", "是否存在“Open accessibility settings”以外的强制按钮或倒计时控件", "页面是否为系统设置样式（状态栏/返回语义）而非自绘高仿页"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 com.android.settings 的无障碍页，条目“TagMacro messaging”及其说明文本",
        "why_most_useful": "核对服务标签与 description 是否与应用身份一致、是否被空白/同形字伪装或冒充系统/品牌组件",
        "observable_utg_signals": ["条目名是否严格为“TagMacro messaging”", "说明文本是否与 strings.xml a11y_description 完全一致", "是否同时出现多个可疑无障碍条目（多包伪装）"]
      },
      {
        "page_role": "宏列表页顶部危险色提示卡片",
        "page_identifier": "dev.tagmacro.MainActivity 宏列表，“Some actions can't run yet”卡片与“Open Settings”按钮",
        "why_most_useful": "判断引导是否为功能按需触发（需用户先启用含相关动作的宏），而非冷启动强制弹出",
        "observable_utg_signals": ["卡片出现条件是否依赖已有启用宏", "是否可滚动离开/直接使用其它宏（非模态）", "是否存在覆盖全屏的遮罩层"]
      },
      {
        "page_role": "应用详情页（受限设置教学落地页）",
        "page_identifier": "系统 Settings.ACTION_APPLICATION_DETAILS_SETTINGS，包名 dev.tagmacro",
        "why_most_useful": "验证是否真的引导用户走系统“允许受限设置”流程，且未使用安装器/Session 绕过",
        "observable_utg_signals": ["是否停留在系统应用信息页（而非自绘仿页）", "是否出现“允许受限设置”菜单项", "返回后是否发生自动重跳循环"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：无图片引导、无 WebView、无加固与动态加载，全部引导文案为可静态定位的明文字符串。唯一需注意的温和点是“受限设置分步教学”本身在纯 UTG 文本信号上可能与恶意诱导同构，须结合“是否有强制/遮罩/伪造UI/拒绝循环”综合判定。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "dev.tagmacro.MainActivity.settingsScreen$lambda$1（startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\")）",
    "dev.tagmacro.MainActivity.settingsScreen（permissionBlock 权限区块与无障碍说明文案）",
    "dev.tagmacro.MainActivity.settingsScreen$lambda$0 / settingsScreen$lambda$0$0（受限设置说明 + APPLICATION_DETAILS_SETTINGS 跳转）",
    "dev.tagmacro.MainActivity.macrosScreen（“Some actions can't run yet”按需提示卡片）",
    "res/xml/accessibility_config.xml（packageNames 限定 Signal/WhatsApp、canRetrieveWindowContent）",
    "res/values/strings.xml（a11y_label / a11y_description）"
  ]
}
```

补充说明（证据边界）：本次为纯静态定向核验，未启动动态运行；结论基于 `classes.dex`（360 类、无加固/混淆、无动态加载入口）、Manifest 与资源文件，覆盖范围不含运行期系统设置页的实际渲染表现，UTG 环节建议按上表触发点取证。

</details>
