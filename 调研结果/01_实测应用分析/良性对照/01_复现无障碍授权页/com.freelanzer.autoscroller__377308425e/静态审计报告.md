# BN_045__377308425e｜系统效率与通用辅助 — AutoScroller

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：119.2s

## 1. 一句话核心结论

- **核心申请方式**：首次启动展示透明 EULA 说明，用户点击“Open Accessibility Settings”后仅一次跳转系统无障碍详情页，返回后只读 Settings.Secure 刷新状态，无诱导、无遮罩、无重跳。
- **静态可见性说明**：完整静态可见：MainActivity 为纯 Jetpack Compose 原生界面，权限引导文案全部位于 res/values/strings.xml，跳转逻辑位于 lf.H 与状态检测位于 n11.a；无 WebView、无远端 HTML、无加壳或 AES 密文载荷，Native 库仅为 androidx.graphics.path 与 datastore 标准库。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `377308425e42e3313257d775ca67ff20e233945f97168bf4c4da9a7ad6afac2a` |
| 包名 / 年份 | `com.freelanzer.autoscroller` / 2025-2026 |
| 家族 / 品类 | **系统效率与通用辅助**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.freelanzer.autoscroller_2.apk |
| 桌面显示名 | AutoScroller |
| 引导页宣称品牌/身份 | AutoScroller（F-Droid 开源，Apache 2.0，数字健康/无障碍辅助工具，真实身份，无借用） |
| 系统无障碍列表服务名 | AutoScroller |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅代码经 R8 混淆（类名 lf/n11/ya1 等）属正常发布构建，UI 名称、服务标签与描述三者一致，无多 activity-alias、无空白/换行挤出、无伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.freelanzer.autoscroller.service.accessibility.AutoScrollService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | Enables automatic scrolling in vertical-video apps (Reels, TikTok, Shorts). AutoScroller only performs scroll gestures; it does not read, store or transmit your content. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.freelanzer.autoscroller.MainActivity（Compose 单 Activity） | onCreate → 挂载 Compose 内容 mj(-270309432, oj0(tv0VarA)) | 原生Activity | **原文**：AutoScroller automates scrolling in vertical-video apps to improve accessibility and digital wellbeing.<br>**译注**：AutoScroller 通过自动化滚动竖屏视频应用来改善无障碍体验与数字健康。 | 阅读首次启动说明；无隐藏或强制行为，可直接返回退出应用 | `com.freelanzer.autoscroller.MainActivity#onCreate / strings.xml eula_intro` |
| 2 | 引导说明页 | 首次启动 EULA 说明弹层（Compose Dialog，rs/dialog 宿主） | DataStore 键 eula_accepted 为 false 时展示 | 原生Dialog | **原文**：Before you start / Data and privacy / Digital wellbeing notice / License — Accept and continue<br>**译注**：「开始之前」弹层，含数据与隐私、数字健康提示、许可证三段说明，唯一按钮为“接受并继续”。 | 点击「Accept and continue」接受说明；可返回键关闭并退出，无恐吓性文案 | `strings.xml eula_title/eula_data_body/eula_wellbeing_body/eula_license_body/eula_accept；cq#m (eula_accepted)` |
| 3 | 业务功能触发 | 主设置页状态区（Compose） | n11.a() 返回 false（enabled_accessibility_services 未包含本服务） | 原生Activity | **原文**：Accessibility service disabled / To use AutoScroller you need to enable its accessibility service. Tap the button below, find "AutoScroller" in the list and turn on the toggle. / Open Accessibility Settings<br>**译注**：无障碍服务未启用；提示用户点击下方按钮，在列表中找到 AutoScroller 并打开开关。 | 用户主动点击「Open Accessibility Settings」按钮；同页仍可进入设置、添加目标应用、使用手动开关 | `strings.xml status_service_disabled/status_setup_body/status_open_accessibility；n11#a` |
| 4 | 跳无障碍设置 | 系统页 android.settings.ACCESSIBILITY_DETAILS_SETTINGS（失败回退 ACCESSIBILITY_SETTINGS） | 点击按钮 → lf.H(context)（调用方 ib.a / b.k） | 系统无障碍页 | **原文**：new Intent("android.settings.ACCESSIBILITY_DETAILS_SETTINGS"); intent.putExtra("android.intent.extra.COMPONENT_NAME", componentName.flattenToString()); ... new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(268435456)<br>**译注**：以 ComponentName 精确指向 AutoScroller/AutoScrollService 的无障碍详情页，异常时退回无障碍服务总列表；均带 FLAG_ACTIVITY_NEW_TASK。 | 由用户在系统页内自行打开 AutoScroller 开关；应用不代操作 | `lf#H` |
| 5 | 拒权反馈循环 | 返回主界面后的状态刷新 | 回到 MainActivity 重新读取 Settings.Secure.enabled_accessibility_services | 原生Activity | **原文**：Settings$Secure.getString(context.getContentResolver(), "enabled_accessibility_services")<br>**译注**：仅逐项比对冒号分隔的服务列表以判断本服务是否启用，未授权则继续显示未启用状态，不重跳、不弹窗、不阻断其他功能。 | 无强制操作；用户可继续使用手动模式或直接退出 | `n11#a` |
| 6 | 获权后动作 | AutoScrollService（无障碍服务）+ WellbeingService（前台服务，specialUse） | onServiceConnected / onAccessibilityEvent → handleSwipeActivation | 系统无障碍页 | **原文**：Inside an app from the list, swipe up several times and auto-scroll starts on its own.<br>**译注**：仅在用户加入列表的目标应用内、连续上滑达到设定次数后执行滚动；另以本地 Room 统计时长并在到达上限时发通知。 | 在目标应用内连续上滑以激活；点按或滑动即暂停自动滚动 | `AutoScrollService#handleSwipeActivation / strings.xml settings_swipe_activation_help` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：android:label=@string/accessibility_service_label（AutoScroller）+ android:description=@string/accessibility_service_description（主动声明仅执行滚动手势、不读取/存储/传输内容）
- 首次启动 Compose 原生弹层：eula_title / eula_intro / eula_data_title+eula_data_body / eula_wellbeing_title+eula_wellbeing_body / eula_license_title+eula_license_body，按钮 eula_accept（Accept and continue）
- 主设置页状态区（原生 Compose，非 WebView）：status_service_disabled、status_setup_body、status_open_accessibility 按钮
- 设置页功能区：settings_swipe_activation_help / settings_apps_help / settings_session_help / settings_pause_help / notif_channel_alert_desc
- 无任何 assets HTML、无 WebView、无悬浮窗 Overlay、无高仿系统无障碍开关页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enables automatic scrolling in vertical-video apps (Reels, TikTok, Shorts). AutoScroller only performs scroll gestures; it does not read, store or transmit your content. | 为竖屏视频应用（Reels、TikTok、Shorts）启用自动滚动。AutoScroller 仅执行滚动手势，不读取、不存储、不传输你的内容。 | `res/values/strings.xml accessibility_service_description` | 良性透明说明 |
| en | To use AutoScroller you need to enable its accessibility service. Tap the button below, find "AutoScroller" in the list and turn on the toggle. | 使用 AutoScroller 需要启用其无障碍服务。点击下方按钮，在列表中找到“AutoScroller”并打开开关。 | `res/values/strings.xml status_setup_body` | 良性透明说明 |
| en | AutoScroller stores usage statistics —duration of each session, number of swipes and the app it was used in— only on your device. This data is not sent to any server or shared with third parties, and the app does not access the content you view. If cloud sync or data collection is offered in the future, it will always be optional and require your explicit consent. | AutoScroller 的用量统计（会话时长、滑动次数、使用过的应用）仅保存在你的设备上，不发送到任何服务器、不与第三方共享，且不访问你浏览的内容。未来若提供云同步或数据收集，也始终可选并需你明确同意。 | `res/values/strings.xml eula_data_body` | 隐私承诺 |
| en | Prolonged use of vertical-video content can affect your wellbeing. AutoScroller is not responsible for the content it scrolls through or for the time you spend using third-party apps. Set a healthy time limit in the settings. | 长时间观看竖屏视频可能影响身心健康。AutoScroller 不对其滚动经过的内容或你在第三方应用中花费的时间负责，请在设置中设定健康的时间上限。 | `res/values/strings.xml eula_wellbeing_body` | 良性透明说明 |
| en | Turn auto-scroll on or off manually. You can still use the configured gestures. | 可手动开启或关闭自动滚动；已配置的手势依然可用。 | `res/values/strings.xml settings_session_help` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性降级：未授权时仅显示“Accessibility service disabled”状态与一个跳转按钮，用户返回后不会重跳、不弹窗、不锁屏；应用其余本地设置（目标应用列表、间隔、时长上限、手动会话开关）照常可用，可直接退出。
- **遮罩叠层 / 高仿系统设置页**：无。无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；跳转目标为真实系统设置页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。仅读取 Settings.Secure 判断状态，未写入、未自点确认，也未在设置页执行 GLOBAL_ACTION_BACK/HOME 阻止撤权。
- **良性降级 / 替代方案**：提供手动会话开关（settings_session_on/off，session 段可手动启停自动滚动），并保留已配置手势；无障碍未启用时主设置页与用量统计功能仍可访问。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到前台 Activity 从 com.freelanzer.autoscroller.MainActivity 跳转到 com.android.settings 的 AccessibilityDetailsSettings（ACTION=android.settings.ACCESSIBILITY_DETAILS_SETTINGS，extra COMPONENT_NAME 含 com.freelanzer.autoscroller/.service.accessibility.AutoScrollService）的瞬间拉起 UTG；同时可在首次冷启动 eula_accepted 未置位时立即截取 EULA 弹层。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。应用无加壳、无远端 HTML、无图片型诱导，运行期 UTG 可完整覆盖引导链路；唯一注意点是界面为 Jetpack Compose 渲染，需依赖无障碍节点树文本而非传统 View id 定位。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（首次安装）** | MainActivity 上的 Compose Dialog，含 Before you start / Data and privacy / Accept and continue | 判定应用是否在首次启动即以恐吓、假更新或隐私承诺话术铺垫权限申请；本应用此处为透明说明，可作为良性对照基准。 | 弹层文本是否含故障/风险/更新等恐吓词；按钮集合是否只有单一“接受”而无取消/跳过；是否引用无障碍或敏感权限且未说明用途 |
| **跳转前主设置页状态区** | MainActivity 内 status_service_disabled 文本 + Open Accessibility Settings 按钮 | 确认权限申请是用户主动点击触发（on-demand）还是自动拉起，并核验引导文案是否与 android:description 一致。 | 按钮点击前后是否发生自动跳转（无点击即跳为可疑）；文案是否含“受限设置/应用详情右上角菜单”教学；同页是否提供手动替代功能入口 |
| **系统无障碍服务列表项 / 详情页** | 设置页条目文本 AutoScroller + 描述 Enables automatic scrolling in vertical-video apps… | 核对系统展示的服务名与描述是否与桌面应用名一致，是否存在空白挤出、同形字或与真实功能不符的伪装描述。 | 服务名与 app 名是否一致；描述中是否包含用途与数据边界声明；是否存在多项同名/多 alias 条目 |
| **设置页返回后状态刷新页** | MainActivity 状态区由 disabled 变为 Accessibility service active | 确认返回后是否存在死循环重跳、遮罩压栈或强制二次授权等强制行为。 | 返回后 1–3 秒内是否再次跳转系统设置；是否出现悬浮窗/遮罩节点；拒绝授权后功能是否仍可用（降级） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.freelanzer.autoscroller.MainActivity#onCreate`
- `lf#H`
- `n11#a`
- `res/values/strings.xml`
- `com.freelanzer.autoscroller.service.accessibility.AutoScrollService#handleSwipeActivation`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**结论：这是一款完全透明的开源良性应用，未发现任何无障碍权限诱导或伪装行为。**

**权限申请路径（静态可见，均为原生 Compose UI 与系统设置页）**
1. 冷启动进入 [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.freelanzer.autoscroller.MainActivity#onCreate>)，该界面是纯 Jetpack Compose 界面，不含 WebView 或悬浮窗。
2. 首次启动时展示「Before you start」EULA 说明弹层，分「Data and privacy / Digital wellbeing notice / License」三段，仅有「Accept and continue」按钮；同意状态保存到 DataStore 键 `eula_accepted`。
3. 主界面在服务未启用时展示 `status_service_disabled` 和按钮「Open Accessibility Settings」；由用户主动点击，没有定时器自动拉起。
4. 点击后走 [lf.H()](<resource-unit:#1.dex1 code:lf#H>)，先尝试 `android.settings.ACCESSIBILITY_DETAILS_SETTINGS`，并用 `ComponentName(AutoScroller/AutoScrollService).flattenToString()` 作为 extra 定位本服务；如果抛异常，则回退到 `android.settings.ACCESSIBILITY_SETTINGS`。整个应用没有 `APPLICATION_DETAILS_SETTINGS` 跳转，也没有“允许受限设置”分步教学。
5. 返回后，[n11.a()](<resource-unit:#1.dex1 code:n11#a>) 读取 `Settings.Secure.enabled_accessibility_services`，仅用于读取状态并据此刷新 UI，没有改写，没有自授权，没有监听设置页并按返回键阻止撤权，也没有 onResume 强制循环。
6. 若未授权，应用会降级到「手动开关会话」等本地功能，见 `settings_session_help`。

**身份与文案**：显示名 `AutoScroller`、无障碍列表标签 `AutoScroller`、`android:description` 主动声明“仅执行滚动手势，不读取、不存储、不传输内容”，与实现一致，即服务内仅 `handleSwipeActivation`、`handleUserInteractionWhileScrolling`、`performGlobalAction` 等滚动逻辑，以及本地 Room 用量统计；无品牌借用、无同形字或空白挤出，也无伪造 `isAccessibilityTool`。全包无加壳、无加密资产、无二阶段载荷。

**合规判断**：属于“良性透明说明 + 系统无障碍页直达”，风险不成立。

```json
{
  "static_visibility": "clear",
  "visibility_note": "完整静态可见：MainActivity 为纯 Jetpack Compose 原生界面，权限引导文案全部位于 res/values/strings.xml，跳转逻辑位于 lf.H 与状态检测位于 n11.a；无 WebView、无远端 HTML、无加壳或 AES 密文载荷，Native 库仅为 androidx.graphics.path 与 datastore 标准库。",
  "summary_one_liner": "首次启动展示透明 EULA 说明，用户点击“Open Accessibility Settings”后仅一次跳转系统无障碍详情页，返回后只读 Settings.Secure 刷新状态，无诱导、无遮罩、无重跳。",
  "disguise_identity": {
    "app_display_name": "AutoScroller",
    "claimed_brand_or_persona": "AutoScroller（F-Droid 开源，Apache 2.0，数字健康/无障碍辅助工具，真实身份，无借用）",
    "a11y_service_label": "AutoScroller",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅代码经 R8 混淆（类名 lf/n11/ya1 等）属正常发布构建，UI 名称、服务标签与描述三者一致，无多 activity-alias、无空白/换行挤出、无伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.freelanzer.autoscroller.MainActivity（Compose 单 Activity）",
      "trigger_event": "onCreate → 挂载 Compose 内容 mj(-270309432, oj0(tv0VarA))",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "AutoScroller automates scrolling in vertical-video apps to improve accessibility and digital wellbeing.",
      "shown_text_zh": "AutoScroller 通过自动化滚动竖屏视频应用来改善无障碍体验与数字健康。",
      "user_action_requested": "阅读首次启动说明；无隐藏或强制行为，可直接返回退出应用",
      "code_anchor": "com.freelanzer.autoscroller.MainActivity#onCreate / strings.xml eula_intro"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "首次启动 EULA 说明弹层（Compose Dialog，rs/dialog 宿主）",
      "trigger_event": "DataStore 键 eula_accepted 为 false 时展示",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Before you start / Data and privacy / Digital wellbeing notice / License — Accept and continue",
      "shown_text_zh": "「开始之前」弹层，含数据与隐私、数字健康提示、许可证三段说明，唯一按钮为“接受并继续”。",
      "user_action_requested": "点击「Accept and continue」接受说明；可返回键关闭并退出，无恐吓性文案",
      "code_anchor": "strings.xml eula_title/eula_data_body/eula_wellbeing_body/eula_license_body/eula_accept；cq#m (eula_accepted)"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "主设置页状态区（Compose）",
      "trigger_event": "n11.a() 返回 false（enabled_accessibility_services 未包含本服务）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility service disabled / To use AutoScroller you need to enable its accessibility service. Tap the button below, find \"AutoScroller\" in the list and turn on the toggle. / Open Accessibility Settings",
      "shown_text_zh": "无障碍服务未启用；提示用户点击下方按钮，在列表中找到 AutoScroller 并打开开关。",
      "user_action_requested": "用户主动点击「Open Accessibility Settings」按钮；同页仍可进入设置、添加目标应用、使用手动开关",
      "code_anchor": "strings.xml status_service_disabled/status_setup_body/status_open_accessibility；n11#a"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统页 android.settings.ACCESSIBILITY_DETAILS_SETTINGS（失败回退 ACCESSIBILITY_SETTINGS）",
      "trigger_event": "点击按钮 → lf.H(context)（调用方 ib.a / b.k）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "new Intent(\"android.settings.ACCESSIBILITY_DETAILS_SETTINGS\"); intent.putExtra(\"android.intent.extra.COMPONENT_NAME\", componentName.flattenToString()); ... new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(268435456)",
      "shown_text_zh": "以 ComponentName 精确指向 AutoScroller/AutoScrollService 的无障碍详情页，异常时退回无障碍服务总列表；均带 FLAG_ACTIVITY_NEW_TASK。",
      "user_action_requested": "由用户在系统页内自行打开 AutoScroller 开关；应用不代操作",
      "code_anchor": "lf#H"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回主界面后的状态刷新",
      "trigger_event": "回到 MainActivity 重新读取 Settings.Secure.enabled_accessibility_services",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Settings$Secure.getString(context.getContentResolver(), \"enabled_accessibility_services\")",
      "shown_text_zh": "仅逐项比对冒号分隔的服务列表以判断本服务是否启用，未授权则继续显示未启用状态，不重跳、不弹窗、不阻断其他功能。",
      "user_action_requested": "无强制操作；用户可继续使用手动模式或直接退出",
      "code_anchor": "n11#a"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "AutoScrollService（无障碍服务）+ WellbeingService（前台服务，specialUse）",
      "trigger_event": "onServiceConnected / onAccessibilityEvent → handleSwipeActivation",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Inside an app from the list, swipe up several times and auto-scroll starts on its own.",
      "shown_text_zh": "仅在用户加入列表的目标应用内、连续上滑达到设定次数后执行滚动；另以本地 Room 统计时长并在到达上限时发通知。",
      "user_action_requested": "在目标应用内连续上滑以激活；点按或滑动即暂停自动滚动",
      "code_anchor": "AutoScrollService#handleSwipeActivation / strings.xml settings_swipe_activation_help"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：android:label=@string/accessibility_service_label（AutoScroller）+ android:description=@string/accessibility_service_description（主动声明仅执行滚动手势、不读取/存储/传输内容）",
    "首次启动 Compose 原生弹层：eula_title / eula_intro / eula_data_title+eula_data_body / eula_wellbeing_title+eula_wellbeing_body / eula_license_title+eula_license_body，按钮 eula_accept（Accept and continue）",
    "主设置页状态区（原生 Compose，非 WebView）：status_service_disabled、status_setup_body、status_open_accessibility 按钮",
    "设置页功能区：settings_swipe_activation_help / settings_apps_help / settings_session_help / settings_pause_help / notif_channel_alert_desc",
    "无任何 assets HTML、无 WebView、无悬浮窗 Overlay、无高仿系统无障碍开关页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enables automatic scrolling in vertical-video apps (Reels, TikTok, Shorts). AutoScroller only performs scroll gestures; it does not read, store or transmit your content.",
      "text_zh": "为竖屏视频应用（Reels、TikTok、Shorts）启用自动滚动。AutoScroller 仅执行滚动手势，不读取、不存储、不传输你的内容。",
      "source_location": "res/values/strings.xml accessibility_service_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "To use AutoScroller you need to enable its accessibility service. Tap the button below, find \"AutoScroller\" in the list and turn on the toggle.",
      "text_zh": "使用 AutoScroller 需要启用其无障碍服务。点击下方按钮，在列表中找到“AutoScroller”并打开开关。",
      "source_location": "res/values/strings.xml status_setup_body",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "AutoScroller stores usage statistics —duration of each session, number of swipes and the app it was used in— only on your device. This data is not sent to any server or shared with third parties, and the app does not access the content you view. If cloud sync or data collection is offered in the future, it will always be optional and require your explicit consent.",
      "text_zh": "AutoScroller 的用量统计（会话时长、滑动次数、使用过的应用）仅保存在你的设备上，不发送到任何服务器、不与第三方共享，且不访问你浏览的内容。未来若提供云同步或数据收集，也始终可选并需你明确同意。",
      "source_location": "res/values/strings.xml eula_data_body",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Prolonged use of vertical-video content can affect your wellbeing. AutoScroller is not responsible for the content it scrolls through or for the time you spend using third-party apps. Set a healthy time limit in the settings.",
      "text_zh": "长时间观看竖屏视频可能影响身心健康。AutoScroller 不对其滚动经过的内容或你在第三方应用中花费的时间负责，请在设置中设定健康的时间上限。",
      "source_location": "res/values/strings.xml eula_wellbeing_body",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn auto-scroll on or off manually. You can still use the configured gestures.",
      "text_zh": "可手动开启或关闭自动滚动；已配置的手势依然可用。",
      "source_location": "res/values/strings.xml settings_session_help",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性降级：未授权时仅显示“Accessibility service disabled”状态与一个跳转按钮，用户返回后不会重跳、不弹窗、不锁屏；应用其余本地设置（目标应用列表、间隔、时长上限、手动会话开关）照常可用，可直接退出。",
    "overlay_or_fake_settings": "无。无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；跳转目标为真实系统设置页。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。仅读取 Settings.Secure 判断状态，未写入、未自点确认，也未在设置页执行 GLOBAL_ACTION_BACK/HOME 阻止撤权。",
    "benign_graceful_degradation": "提供手动会话开关（settings_session_on/off，session 段可手动启停自动滚动），并保留已配置手势；无障碍未启用时主设置页与用量统计功能仍可访问。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到前台 Activity 从 com.freelanzer.autoscroller.MainActivity 跳转到 com.android.settings 的 AccessibilityDetailsSettings（ACTION=android.settings.ACCESSIBILITY_DETAILS_SETTINGS，extra COMPONENT_NAME 含 com.freelanzer.autoscroller/.service.accessibility.AutoScrollService）的瞬间拉起 UTG；同时可在首次冷启动 eula_accepted 未置位时立即截取 EULA 弹层。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（首次安装）",
        "page_identifier": "MainActivity 上的 Compose Dialog，含 Before you start / Data and privacy / Accept and continue",
        "why_most_useful": "判定应用是否在首次启动即以恐吓、假更新或隐私承诺话术铺垫权限申请；本应用此处为透明说明，可作为良性对照基准。",
        "observable_utg_signals": ["弹层文本是否含故障/风险/更新等恐吓词", "按钮集合是否只有单一“接受”而无取消/跳过", "是否引用无障碍或敏感权限且未说明用途"]
      },
      {
        "page_role": "跳转前主设置页状态区",
        "page_identifier": "MainActivity 内 status_service_disabled 文本 + Open Accessibility Settings 按钮",
        "why_most_useful": "确认权限申请是用户主动点击触发（on-demand）还是自动拉起，并核验引导文案是否与 android:description 一致。",
        "observable_utg_signals": ["按钮点击前后是否发生自动跳转（无点击即跳为可疑）", "文案是否含“受限设置/应用详情右上角菜单”教学", "同页是否提供手动替代功能入口"]
      },
      {
        "page_role": "系统无障碍服务列表项 / 详情页",
        "page_identifier": "设置页条目文本 AutoScroller + 描述 Enables automatic scrolling in vertical-video apps…",
        "why_most_useful": "核对系统展示的服务名与描述是否与桌面应用名一致，是否存在空白挤出、同形字或与真实功能不符的伪装描述。",
        "observable_utg_signals": ["服务名与 app 名是否一致", "描述中是否包含用途与数据边界声明", "是否存在多项同名/多 alias 条目"]
      },
      {
        "page_role": "设置页返回后状态刷新页",
        "page_identifier": "MainActivity 状态区由 disabled 变为 Accessibility service active",
        "why_most_useful": "确认返回后是否存在死循环重跳、遮罩压栈或强制二次授权等强制行为。",
        "observable_utg_signals": ["返回后 1–3 秒内是否再次跳转系统设置", "是否出现悬浮窗/遮罩节点", "拒绝授权后功能是否仍可用（降级）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。应用无加壳、无远端 HTML、无图片型诱导，运行期 UTG 可完整覆盖引导链路；唯一注意点是界面为 Jetpack Compose 渲染，需依赖无障碍节点树文本而非传统 View id 定位。"
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
    "com.freelanzer.autoscroller.MainActivity#onCreate",
    "lf#H",
    "n11#a",
    "res/values/strings.xml",
    "com.freelanzer.autoscroller.service.accessibility.AutoScrollService#handleSwipeActivation"
  ]
}
```

</details>
