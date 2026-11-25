# BN_053__8c946cbb7c｜系统清理与省电冻结 — PingOff

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：132.2s

## 1. 一句话核心结论

- **核心申请方式**：PingOff 仅在用户主动把「应用检测方式」切换为无障碍服务时，弹出一个原生、可取消、且明确警告『无障碍可被用来监视用户、请三思』的说明对话框，用户点 OK 后才跳转系统无障碍设置页，全程无遮罩、无死循环、无身份伪装。
- **静态可见性说明**：全部引导逻辑与文案静态可见：DEX 仅经 R8 名称混淆（类名 gp0/ip0/b61 等），Manifest、res/xml/accessibility_service.xml、res/values/strings.xml 中全部引导文案为明文，无加壳、无 VMP、无 AES 密文资产、无远端 HTML/WebView 引导页。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8c946cbb7c8cf0cf16e2d50d7af6b6e9abb642cc4ac0c03000f5d58fef08e4b1` |
| 包名 / 年份 | `com.jarsilio.android.pingoff` / 2025-2026 |
| 家族 / 品类 | **系统清理与省电冻结**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.jarsilio.android.pingoff_18.apk |
| 桌面显示名 | PingOff |
| 引导页宣称品牌/身份 | PingOff（开源项目 juanitobananas / Juan García Basilio，GPLv3，F-Droid 分发） |
| 系统无障碍列表服务名 | PingOff |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务 label 直接复用 @string/app_name；无障碍 description 如实说明仅用于检测前台应用；无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.jarsilio.android.pingoff.services.AppLaunchDetectionService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |
| 系统设置项说明 (`android:description`) | This service is used to detect activity launches, which allows us to know which app is currently running in the foreground. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.jarsilio.android.pingoff.MainActivity（含 MainActivity$a 设置偏好 Fragment） | onCreate 载入设置界面；onStart 检查 Usage Access / DND 状态 | 原生Activity | **原文**：无（此步仅渲染设置列表，缺失权限时才在 onStart 跳到 AppIntro）<br>**译注**：进入应用主设置页，展示「App detection method」等偏好项。 | 无强制操作；用户可自由浏览或退出 | `com.jarsilio.android.pingoff.MainActivity#onCreate / #onStart` |
| 2 | 业务功能触发 | MainActivity$a 设置页的 ListPreference「App detection method」（pref_use_accessibility_service） | onViewCreated 给偏好项注册 gp0 点击/变更监听；用户主动选择 “Accessibility Service” | 原生Activity | **原文**：App detection method / "Use 'Accessibility Service' instead of 'Usage Access' to detect currently running app."<br>**译注**：「应用检测方式」：可选择用「无障碍服务」替代「使用情况访问」来检测当前运行的应用。 | 用户在设置中主动切换检测方式（可选 Usage Access 作为替代路径） | `com.jarsilio.android.pingoff.MainActivity$a#onViewCreated → gp0#b；res/xml/root_preferences.xml（pref_use_accessibility_service）` |
| 3 | 引导说明页 | MaterialAlertDialog（up0/t3 构建），按钮 OK / Cancel | gp0#b 默认分支：读取 b61.b 开关，未关闭时弹窗；点击 OK 进入下一步，Cancel 仅关闭 | 原生Dialog | **原文**：<b>App detection: Accessibility Service</b>" <br><br>PingOff can be used as an 'Accessibility Service' to detect the currently running app more reliably on some devices. <br><br>Granting an app Accessibility Service allows it to spy on the user if it wants to. It also allows an app to use specific functions that wouldn't be available otherwise. For example PingOff uses an "<i>AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED</i>" to detect if an app has been launched and is therefore in the foreground. <br><br>"<b>Please think twice before trusting apps!</b>" <br><br>PingOff is open source software so please go ahead and check the code (or ask a friend to do it) to make sure we are not doing anything evil (we promise we are not, but you really shouldn't take our word for it). <br><br>Do you want to set PingOff as an Accessibility Service? You'll have to grant the privileges manually in the next screen.<br>**译注**：「应用检测：无障碍服务」——在某些设备上，PingOff 可作为无障碍服务更可靠地检测当前运行的应用。授予无障碍服务会让应用有能力监视用户，也解锁普通应用没有的特定能力；例如 PingOff 使用 TYPE_WINDOW_STATE_CHANGED 事件判断某应用是否被启动到前台。请三思后再信任应用！PingOff 是开源软件，请直接查看代码确认我们没有做坏事（我们承诺没有，但你不该只听我们的）。要把 PingOff 设为无障碍服务吗？你需要在下一屏手动授予权限。 | 用户可选择 OK（继续去系统设置）或 Cancel（放弃），弹窗不可点外部关闭但提供显式取消按钮 | `gp0#b（正文 2131886108 = @string/accessibility_service_explanation）；res/values/strings.xml#L24-L34` |
| 4 | 跳无障碍设置 | 系统 Settings.ACCESSIBILITY_SETTINGS 无障碍服务列表 | ip0#onClick（对话框 OK 按钮回调）启动 new Intent("android.settings.ACCESSIBILITY_SETTINGS") | 系统无障碍页 | **原文**：This service is used to detect activity launches, which allows us to know which app is currently running in the foreground.<br>**译注**：系统无障碍列表中 PingOff 条目下的说明：本服务用于检测 Activity 启动，从而得知当前处于前台的应用。 | 由用户在系统页面自行勾选并确认开启（应用不做任何自动点击或替用户确认） | `ip0#onClick；res/xml/accessibility_service.xml；@string/accessibility_service_description` |
| 5 | 拒权反馈循环 | 返回 MainActivity / MainActivity$a | 用户从系统设置返回后 onResume（仅 invalidateOptionsMenu 与刷新偏好监听）/ 用户点 Cancel | 原生Activity | 无 | 无（不重复拉起、不阻止返回） | `com.jarsilio.android.pingoff.MainActivity#onResume / MainActivity$a#onResume` |
| 6 | 获权后动作 | AppLaunchDetectionService（前台应用检测）+ PersistentService（前台常驻通知） | 系统绑定无障碍服务后 onAccessibilityEvent(typeWindowStateChanged) 持续回调 | 通知栏 | **原文**：PingOff<br>**译注**：仅在状态栏显示常驻通知，按前台应用切换勿扰模式。 | 无；用户可随时在系统无障碍列表关闭该服务 | `com.jarsilio.android.pingoff.services.AppLaunchDetectionService#onAccessibilityEvent；com.jarsilio.android.pingoff.services.PersistentService` |
| 7 | 引导说明页 | com.jarsilio.android.pingoff.appintro.AppIntro（AppIntro 幻灯片，仅在缺 Usage Access/DND 时由 MainActivity.onStart 启动） | MainActivity#onStart：无 Usage Access/Accessibility 或 DND 策略未授予时启动 AppIntro | 原生Activity | **原文**："Please select PingOff and check 'Permit usage access' after tapping on the button below." / "Please allow PingOff to ignore the battery optimizations after tapping on the button below."<br>**译注**：分步指引：点下方按钮后选择 PingOff 并勾选「允许使用情况访问」；允许忽略电池优化等。 | 逐页点 NEXT/请求权限；SKIP 按钮被禁用但每页有 BACK 且最终页 DONE 可退出 | `com.jarsilio.android.pingoff.appintro.AppIntro#onCreate（setSkipButtonEnabled(false)）；res/values/strings.xml#L48-L72` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表条目说明：res/xml/accessibility_service.xml → @string/accessibility_service_description（明文如实描述前台检测用途）
- 无障碍申请引导弹窗：gp0#b 中 MaterialAlertDialog 正文 @string/accessibility_service_explanation（含『无障碍可被用于监视用户』『请三思』），按钮 @string/ok / @string/cancel
- 应用设置页偏好项：pref_use_accessibility_service / pref_use_accessibility_service_summary（MainActivity$a 加载的 root_preferences.xml）
- 冷启动缺失权限时的 AppIntro 幻灯片：res/values/strings.xml 中 appintro_usage_access_* / appintro_dnd_* / appintro_battery_optimization_* / appintro_post_notifications_* / appintro_dontkillmyapp_* 明文文案
- 关于/隐私页：MainActivity#onOptionsItemSelected 将内联 HTML 传入 com.jarsilio.android.common.html.HtmlTextActivity（本地字符串拼装，非远端 URL）
- 未出现：悬浮窗 Overlay、本地/远端 WebView 引导页、高仿系统无障碍开关页、图片/GIF 引导素材

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | This service is used to detect activity launches, which allows us to know which app is currently running in the foreground. | 本服务用于检测 Activity 启动，从而得知当前哪个应用在前台运行。 | `res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service.xml 引用）` | 良性透明说明 |
| en | Granting an app Accessibility Service allows it to spy on the user if it wants to. | 授予无障碍服务会让应用有能力监视用户（如果它想这么做的话）。 | `res/values/strings.xml → accessibility_service_explanation（L28）` | 良性透明说明 |
| en | "Please think twice before trusting apps!" | 「请三思后再信任应用！」 | `res/values/strings.xml → accessibility_service_explanation（L30）` | 良性透明说明 |
| en | PingOff is open source software so please go ahead and check the code (or ask a friend to do it) to make sure we are not doing anything evil (we promise we are not, but you really shouldn't take our word for it). | PingOff 是开源软件，请直接去检查代码（或请朋友帮忙检查），确认我们没有做坏事（我们保证没有，但你真的不该只听我们的一面之词）。 | `res/values/strings.xml → accessibility_service_explanation（L32）` | 良性透明说明 |
| en | Do you want to set PingOff as an Accessibility Service? You'll have to grant the privileges manually in the next screen. | 要把 PingOff 设为无障碍服务吗？你需要在下一屏手动授予权限。 | `res/values/strings.xml → accessibility_service_explanation（L34）` | 受限设置分步教学 |
| en | "Please select PingOff and check 'Permit usage access' after tapping on the button below." | 点击下方按钮后，请选择 PingOff 并勾选「允许使用情况访问」。 | `res/values/strings.xml → appintro_usage_access_plea（L72）` | 受限设置分步教学 |
| en | To silence notifications while active, PingOff needs access to Do Not Disturb mode. | 为了在被选定应用运行时静音通知，PingOff 需要勿扰模式访问权限。 | `res/values/strings.xml → appintro_dnd_explanation（L52）` | 良性透明说明 |
| en | "Use 'Accessibility Service' instead of 'Usage Access' to detect currently running app." | 使用「无障碍服务」替代「使用情况访问」来检测当前运行的应用。 | `res/values/strings.xml → pref_use_accessibility_service_summary（L156）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性降级：点 Cancel 仅关闭 AlertDialog 并保留原检测方式；从系统设置返回时 MainActivity#onResume 只刷新菜单与偏好监听，不重跳、不弹二次提示；未授予无障碍时应用继续可用 Usage Access 检测前台应用。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW、无悬浮引导遮罩、无高仿系统无障碍开关页；跳转目标为系统真实 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无。服务无 GLOBAL_ACTION_BACK/HOME、无监听设置页阻止撤权、无自动确认点击；预筛线索中的 WATCH_SETTINGS 未在本链路代码中找到对应实现。
- **良性降级 / 替代方案**：有：无障碍为可选检测方式，用户可保持默认的 Usage Access（PACKAGE_USAGE_STATS）方案；AppIntro 每页提供 BACK，最终页 DONE 可退出，未获权也不阻断主功能。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 的前 1 秒（弹窗 OK 点击瞬间），以及在 MainActivity 中点击「App detection method」偏好项时拉起，用于捕获原生说明对话框全貌与按钮集合。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。纯 UTG 文本即可判定：无图片空文本诱导、无温和外壳、无二阶段 Dropper、无加壳/密文载荷（R8 仅重命名内部类，文案与资源明文）。唯一注意点是无障碍链路仅在用户主动切换检测方式后才出现，冷启动直接抓屏可能只看到设置页或 AppIntro。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **无障碍申请引导弹窗页** | MaterialAlertDialog，标题/正文含 “App detection: Accessibility Service” 与 “spy on the user”，按钮为 OK / CANCEL | 这是唯一承载『要不要开无障碍』说服内容的界面，其文本是否自曝风险、是否有取消按钮、是否可外部关闭，直接决定诱导性质判定 | 弹窗文本包含 spy on the user / think twice 等自曝风险语句；存在可点击的 CANCEL 按钮；无图片/GIF、无伪造系统 UI 元素；按钮点击后 intent 目标为系统 ACCESSIBILITY_SETTINGS |
| **设置页偏好入口** | MainActivity 设置列表中的 ListPreference「App detection method」，选项含 Usage Access / Accessibility Service | 证明无障碍是用户主动选择的检测方式而非冷启动强制，且存在 Usage Access 替代路径 | 偏好项文本与 summary 原文；默认值为 Usage Access 而非无障碍；切换后才触发弹窗 |
| **系统无障碍服务列表项** | Settings.ACCESSIBILITY_SETTINGS 中 label=PingOff 的条目及其 description 文本 | 核对系统侧展示的服务名与说明是否与应用宣称一致（无身份混淆） | 服务 label 为 PingOff；description 为前台检测说明；未被预先勾选/自动开启 |
| **冷启动权限引导页** | AppIntro 幻灯片（Usage Access / DND / 电池优化 / 通知 / dontkillmyapp / Ready to go） | 确认冷启动引导不含无障碍页、SKIP 被禁用但存在 BACK/DONE，属良性分步教学 | 幻灯片标题序列中无无障碍申请页；SKIP 按钮不可见/禁用；BACK 与 DONE 可点击退出 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.jarsilio.android.pingoff.MainActivity$a#onViewCreated`
- `gp0#b`
- `ip0#onClick`
- `com.jarsilio.android.pingoff.MainActivity#onStart`
- `res/xml/accessibility_service.xml`
- `res/values/strings.xml#L23-L34`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（PingOff / com.jarsilio.android.pingoff）

**总体判断：良性、透明的无障碍申请流程，未发现诱导、欺骗或强制行为。**

1. **无障碍申请仅走“按需功能开关”路径，不是冷启动强推**
   - 无障碍服务本身（[AppLaunchDetectionService](<resource-unit:#1.dex1 code:com.jarsilio.android.pingoff.services.AppLaunchDetectionService#onAccessibilityEvent>)）只重写 `onAccessibilityEvent`/`onInterrupt`，事件类型限定为 `typeWindowStateChanged`，用于前台应用识别（DND 静音），没有任何手势注入、`GLOBAL_ACTION_*`、读取窗口文本外发等越权动作。
   - 用户必须先在设置页的 “App detection method” 列表项里选择 “Accessibility Service”，才会触发引导（[MainActivity$a.onViewCreated()](<resource-unit:#1.dex1 code:com.jarsilio.android.pingoff.MainActivity$a#onViewCreated>) 为该偏好项挂 `gp0` 监听）。

2. **引导载体是原生 AlertDialog + 一次系统设置跳转，有明确的取消按钮**
   - [gp0.b()](<resource-unit:#1.dex1 code:gp0#b>) 弹 `MaterialAlertDialog`，正文取 `accessibility_service_explanation`，按钮为 OK/Cancel；点 OK 才由 [ip0.onClick()](<resource-unit:#1.dex1 code:ip0#onClick>) 发出 `android.settings.ACCESSIBILITY_SETTINGS`。无悬浮窗、无遮罩、无本地/远端 WebView、无高仿设置页。
   - `APPLICATION_DETAILS_SETTINGS` 仅在 `tf.onClick` 中出现（应用详情跳转），未参与无障碍链路。

3. **文案高度自曝风险（反向证明非诱导）**
   - 无障碍说明原文直接写 “Granting an app Accessibility Service allows it to spy on the user if it wants to.”、“Please think twice before trusting apps!”，并指向开源代码与 GitLab 隐私政策，属于典型良性透明说明。

4. **拒权反馈为良性降级，无死循环**
   - 取消对话框仅关闭弹窗；`MainActivity.onResume` 只做菜单刷新；`onStart` 在缺 Usage Access / DND 时跳到 `AppIntro` 分步引导（`setSkipButtonEnabled(false)`，但每页有 BACK 与 DONE），未发现 onResume 反复重跳、定时器拉起、获权后监听设置页阻止撤权等行为。
   - 无障碍在 `AppIntro` 中不是强制页（slide 仅为 usage access / DND / 电池优化 / 通知 / dontkillmyapp / 结束页）。

5. **未确认项（覆盖边界）**：预筛线索中的 `WATCH_SETTINGS` 未在无障碍链路找到对应实现（无 `GLOBAL_ACTION`、无设置页监听）；`tf.onClick` 的应用详情跳转未逐行展开。R8 仅重命名内部类（`gp0`/`ip0`/`b61` 等），资源名与全部文案明文可读，**无加壳、无密文载荷、无动态下发**。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑与文案静态可见：DEX 仅经 R8 名称混淆（类名 gp0/ip0/b61 等），Manifest、res/xml/accessibility_service.xml、res/values/strings.xml 中全部引导文案为明文，无加壳、无 VMP、无 AES 密文资产、无远端 HTML/WebView 引导页。",
  "summary_one_liner": "PingOff 仅在用户主动把「应用检测方式」切换为无障碍服务时，弹出一个原生、可取消、且明确警告『无障碍可被用来监视用户、请三思』的说明对话框，用户点 OK 后才跳转系统无障碍设置页，全程无遮罩、无死循环、无身份伪装。",
  "disguise_identity": {
    "app_display_name": "PingOff",
    "claimed_brand_or_persona": "PingOff（开源项目 juanitobananas / Juan García Basilio，GPLv3，F-Droid 分发）",
    "a11y_service_label": "PingOff",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务 label 直接复用 @string/app_name；无障碍 description 如实说明仅用于检测前台应用；无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.jarsilio.android.pingoff.MainActivity（含 MainActivity$a 设置偏好 Fragment）",
      "trigger_event": "onCreate 载入设置界面；onStart 检查 Usage Access / DND 状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（此步仅渲染设置列表，缺失权限时才在 onStart 跳到 AppIntro）",
      "shown_text_zh": "进入应用主设置页，展示「App detection method」等偏好项。",
      "user_action_requested": "无强制操作；用户可自由浏览或退出",
      "code_anchor": "com.jarsilio.android.pingoff.MainActivity#onCreate / #onStart"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity$a 设置页的 ListPreference「App detection method」（pref_use_accessibility_service）",
      "trigger_event": "onViewCreated 给偏好项注册 gp0 点击/变更监听；用户主动选择 “Accessibility Service”",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "App detection method / \"Use 'Accessibility Service' instead of 'Usage Access' to detect currently running app.\"",
      "shown_text_zh": "「应用检测方式」：可选择用「无障碍服务」替代「使用情况访问」来检测当前运行的应用。",
      "user_action_requested": "用户在设置中主动切换检测方式（可选 Usage Access 作为替代路径）",
      "code_anchor": "com.jarsilio.android.pingoff.MainActivity$a#onViewCreated → gp0#b；res/xml/root_preferences.xml（pref_use_accessibility_service）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "MaterialAlertDialog（up0/t3 构建），按钮 OK / Cancel",
      "trigger_event": "gp0#b 默认分支：读取 b61.b 开关，未关闭时弹窗；点击 OK 进入下一步，Cancel 仅关闭",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "<b>App detection: Accessibility Service</b>\" \n\nPingOff can be used as an 'Accessibility Service' to detect the currently running app more reliably on some devices. \n\nGranting an app Accessibility Service allows it to spy on the user if it wants to. It also allows an app to use specific functions that wouldn't be available otherwise. For example PingOff uses an \"<i>AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED</i>\" to detect if an app has been launched and is therefore in the foreground. \n\n\"<b>Please think twice before trusting apps!</b>\" \n\nPingOff is open source software so please go ahead and check the code (or ask a friend to do it) to make sure we are not doing anything evil (we promise we are not, but you really shouldn't take our word for it). \n\nDo you want to set PingOff as an Accessibility Service? You'll have to grant the privileges manually in the next screen.",
      "shown_text_zh": "「应用检测：无障碍服务」——在某些设备上，PingOff 可作为无障碍服务更可靠地检测当前运行的应用。授予无障碍服务会让应用有能力监视用户，也解锁普通应用没有的特定能力；例如 PingOff 使用 TYPE_WINDOW_STATE_CHANGED 事件判断某应用是否被启动到前台。请三思后再信任应用！PingOff 是开源软件，请直接查看代码确认我们没有做坏事（我们承诺没有，但你不该只听我们的）。要把 PingOff 设为无障碍服务吗？你需要在下一屏手动授予权限。",
      "user_action_requested": "用户可选择 OK（继续去系统设置）或 Cancel（放弃），弹窗不可点外部关闭但提供显式取消按钮",
      "code_anchor": "gp0#b（正文 2131886108 = @string/accessibility_service_explanation）；res/values/strings.xml#L24-L34"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings.ACCESSIBILITY_SETTINGS 无障碍服务列表",
      "trigger_event": "ip0#onClick（对话框 OK 按钮回调）启动 new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "This service is used to detect activity launches, which allows us to know which app is currently running in the foreground.",
      "shown_text_zh": "系统无障碍列表中 PingOff 条目下的说明：本服务用于检测 Activity 启动，从而得知当前处于前台的应用。",
      "user_action_requested": "由用户在系统页面自行勾选并确认开启（应用不做任何自动点击或替用户确认）",
      "code_anchor": "ip0#onClick；res/xml/accessibility_service.xml；@string/accessibility_service_description"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 MainActivity / MainActivity$a",
      "trigger_event": "用户从系统设置返回后 onResume（仅 invalidateOptionsMenu 与刷新偏好监听）/ 用户点 Cancel",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无额外提示、无重复弹窗；应用保持原状，用户可继续用 Usage Access 方案或再次手动切换。",
      "user_action_requested": "无（不重复拉起、不阻止返回）",
      "code_anchor": "com.jarsilio.android.pingoff.MainActivity#onResume / MainActivity$a#onResume"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "AppLaunchDetectionService（前台应用检测）+ PersistentService（前台常驻通知）",
      "trigger_event": "系统绑定无障碍服务后 onAccessibilityEvent(typeWindowStateChanged) 持续回调",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "PingOff",
      "shown_text_zh": "仅在状态栏显示常驻通知，按前台应用切换勿扰模式。",
      "user_action_requested": "无；用户可随时在系统无障碍列表关闭该服务",
      "code_anchor": "com.jarsilio.android.pingoff.services.AppLaunchDetectionService#onAccessibilityEvent；com.jarsilio.android.pingoff.services.PersistentService"
    },
    {
      "step": 7,
      "stage": "引导说明页",
      "screen_or_component": "com.jarsilio.android.pingoff.appintro.AppIntro（AppIntro 幻灯片，仅在缺 Usage Access/DND 时由 MainActivity.onStart 启动）",
      "trigger_event": "MainActivity#onStart：无 Usage Access/Accessibility 或 DND 策略未授予时启动 AppIntro",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "\"Please select PingOff and check 'Permit usage access' after tapping on the button below.\" / \"Please allow PingOff to ignore the battery optimizations after tapping on the button below.\"",
      "shown_text_zh": "分步指引：点下方按钮后选择 PingOff 并勾选「允许使用情况访问」；允许忽略电池优化等。",
      "user_action_requested": "逐页点 NEXT/请求权限；SKIP 按钮被禁用但每页有 BACK 且最终页 DONE 可退出",
      "code_anchor": "com.jarsilio.android.pingoff.appintro.AppIntro#onCreate（setSkipButtonEnabled(false)）；res/values/strings.xml#L48-L72"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表条目说明：res/xml/accessibility_service.xml → @string/accessibility_service_description（明文如实描述前台检测用途）",
    "无障碍申请引导弹窗：gp0#b 中 MaterialAlertDialog 正文 @string/accessibility_service_explanation（含『无障碍可被用于监视用户』『请三思』），按钮 @string/ok / @string/cancel",
    "应用设置页偏好项：pref_use_accessibility_service / pref_use_accessibility_service_summary（MainActivity$a 加载的 root_preferences.xml）",
    "冷启动缺失权限时的 AppIntro 幻灯片：res/values/strings.xml 中 appintro_usage_access_* / appintro_dnd_* / appintro_battery_optimization_* / appintro_post_notifications_* / appintro_dontkillmyapp_* 明文文案",
    "关于/隐私页：MainActivity#onOptionsItemSelected 将内联 HTML 传入 com.jarsilio.android.common.html.HtmlTextActivity（本地字符串拼装，非远端 URL）",
    "未出现：悬浮窗 Overlay、本地/远端 WebView 引导页、高仿系统无障碍开关页、图片/GIF 引导素材"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "This service is used to detect activity launches, which allows us to know which app is currently running in the foreground.",
      "text_zh": "本服务用于检测 Activity 启动，从而得知当前哪个应用在前台运行。",
      "source_location": "res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Granting an app Accessibility Service allows it to spy on the user if it wants to.",
      "text_zh": "授予无障碍服务会让应用有能力监视用户（如果它想这么做的话）。",
      "source_location": "res/values/strings.xml → accessibility_service_explanation（L28）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "\"Please think twice before trusting apps!\"",
      "text_zh": "「请三思后再信任应用！」",
      "source_location": "res/values/strings.xml → accessibility_service_explanation（L30）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "PingOff is open source software so please go ahead and check the code (or ask a friend to do it) to make sure we are not doing anything evil (we promise we are not, but you really shouldn't take our word for it).",
      "text_zh": "PingOff 是开源软件，请直接去检查代码（或请朋友帮忙检查），确认我们没有做坏事（我们保证没有，但你真的不该只听我们的一面之词）。",
      "source_location": "res/values/strings.xml → accessibility_service_explanation（L32）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Do you want to set PingOff as an Accessibility Service? You'll have to grant the privileges manually in the next screen.",
      "text_zh": "要把 PingOff 设为无障碍服务吗？你需要在下一屏手动授予权限。",
      "source_location": "res/values/strings.xml → accessibility_service_explanation（L34）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "\"Please select PingOff and check 'Permit usage access' after tapping on the button below.\"",
      "text_zh": "点击下方按钮后，请选择 PingOff 并勾选「允许使用情况访问」。",
      "source_location": "res/values/strings.xml → appintro_usage_access_plea（L72）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "To silence notifications while active, PingOff needs access to Do Not Disturb mode.",
      "text_zh": "为了在被选定应用运行时静音通知，PingOff 需要勿扰模式访问权限。",
      "source_location": "res/values/strings.xml → appintro_dnd_explanation（L52）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "\"Use 'Accessibility Service' instead of 'Usage Access' to detect currently running app.\"",
      "text_zh": "使用「无障碍服务」替代「使用情况访问」来检测当前运行的应用。",
      "source_location": "res/values/strings.xml → pref_use_accessibility_service_summary（L156）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性降级：点 Cancel 仅关闭 AlertDialog 并保留原检测方式；从系统设置返回时 MainActivity#onResume 只刷新菜单与偏好监听，不重跳、不弹二次提示；未授予无障碍时应用继续可用 Usage Access 检测前台应用。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW、无悬浮引导遮罩、无高仿系统无障碍开关页；跳转目标为系统真实 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无。服务无 GLOBAL_ACTION_BACK/HOME、无监听设置页阻止撤权、无自动确认点击；预筛线索中的 WATCH_SETTINGS 未在本链路代码中找到对应实现。",
    "benign_graceful_degradation": "有：无障碍为可选检测方式，用户可保持默认的 Usage Access（PACKAGE_USAGE_STATS）方案；AppIntro 每页提供 BACK，最终页 DONE 可退出，未获权也不阻断主功能。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 的前 1 秒（弹窗 OK 点击瞬间），以及在 MainActivity 中点击「App detection method」偏好项时拉起，用于捕获原生说明对话框全貌与按钮集合。",
    "key_pages_to_capture": [
      {
        "page_role": "无障碍申请引导弹窗页",
        "page_identifier": "MaterialAlertDialog，标题/正文含 “App detection: Accessibility Service” 与 “spy on the user”，按钮为 OK / CANCEL",
        "why_most_useful": "这是唯一承载『要不要开无障碍』说服内容的界面，其文本是否自曝风险、是否有取消按钮、是否可外部关闭，直接决定诱导性质判定",
        "observable_utg_signals": ["弹窗文本包含 spy on the user / think twice 等自曝风险语句", "存在可点击的 CANCEL 按钮", "无图片/GIF、无伪造系统 UI 元素", "按钮点击后 intent 目标为系统 ACCESSIBILITY_SETTINGS"]
      },
      {
        "page_role": "设置页偏好入口",
        "page_identifier": "MainActivity 设置列表中的 ListPreference「App detection method」，选项含 Usage Access / Accessibility Service",
        "why_most_useful": "证明无障碍是用户主动选择的检测方式而非冷启动强制，且存在 Usage Access 替代路径",
        "observable_utg_signals": ["偏好项文本与 summary 原文", "默认值为 Usage Access 而非无障碍", "切换后才触发弹窗"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings.ACCESSIBILITY_SETTINGS 中 label=PingOff 的条目及其 description 文本",
        "why_most_useful": "核对系统侧展示的服务名与说明是否与应用宣称一致（无身份混淆）",
        "observable_utg_signals": ["服务 label 为 PingOff", "description 为前台检测说明", "未被预先勾选/自动开启"]
      },
      {
        "page_role": "冷启动权限引导页",
        "page_identifier": "AppIntro 幻灯片（Usage Access / DND / 电池优化 / 通知 / dontkillmyapp / Ready to go）",
        "why_most_useful": "确认冷启动引导不含无障碍页、SKIP 被禁用但存在 BACK/DONE，属良性分步教学",
        "observable_utg_signals": ["幻灯片标题序列中无无障碍申请页", "SKIP 按钮不可见/禁用", "BACK 与 DONE 可点击退出"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。纯 UTG 文本即可判定：无图片空文本诱导、无温和外壳、无二阶段 Dropper、无加壳/密文载荷（R8 仅重命名内部类，文案与资源明文）。唯一注意点是无障碍链路仅在用户主动切换检测方式后才出现，冷启动直接抓屏可能只看到设置页或 AppIntro。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.jarsilio.android.pingoff.MainActivity$a#onViewCreated",
    "gp0#b",
    "ip0#onClick",
    "com.jarsilio.android.pingoff.MainActivity#onStart",
    "res/xml/accessibility_service.xml",
    "res/values/strings.xml#L23-L34"
  ]
}
```

</details>
