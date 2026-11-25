# MR_053__b57d2cef44｜EventBot — Microsoft Word

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：113.6s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即 finish 隐藏界面，由后台 service 的 while(true) 线程每 15 秒拉起自建 Activity，弹出 setCancelable(false) 且 setType(2003) 的悬浮 WebView 弹窗，用 Microsoft Word 假身份图文教用户去系统无障碍列表开启其服务，唯一按钮直跳 ACCESSIBILITY_SETTINGS，拒权后无限重弹直至获权。
- **静态可见性说明**：无障碍引导全链路（MainActivity 静默启动 → service/func 定时拉权线程 → activity mode=2 → 不可取消 AlertDialog + WebView 本地 HTML → func$3 跳 ACCESSIBILITY_SETTINGS → isA11y 循环）均以明文 DEX 与 strings.xml/assets 图片静态可见，无加壳、无 AES、无加密载荷；仅后续 C2 gate URL 与 pinned 遮罩 HTML/bg 由远端下发，不影响本命题判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b57d2cef4419ca3dfac736825dc0e444e52d22bb517ca185d415f13af856d966` |
| 包名 / 年份 | `com.example.eventbot` / 2020 |
| 家族 / 品类 | **EventBot**（同池样本数：124） |
| 原始来源标识 | https://www.cybereason.com/blog/eventbot-a-new-mobile-banking-trojan-is-born |
| 桌面显示名 | Microsoft Word |
| 引导页宣称品牌/身份 | Microsoft Word（并借用 Google Play services 的"不开启无法运行"措辞营造系统依赖感） |
| 系统无障碍列表服务名 | Microsoft Word |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.example.eventbot 与品牌 Microsoft Word 完全不符；类名简写混淆（func、cfg、events、activity）；桌面图标 ic_launcher 直接使用 Word 名称；无障碍说明以"Microsoft Word will not work correctly"把恶意权限包装成微软产品自身功能缺失。未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool 手法。 |
| 无障碍服务类名 | `com.example.eventbot.events` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | You must enable Microsoft Word in order to get full functionality of the application. Microsoft Word will not work correctly. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.example.eventbot.MainActivity（LAUNCHER） | onCreate（用户点击桌面图标） | 原生Activity | 无 | 无需操作，进程转入后台静默驻留 | `com.example.eventbot.MainActivity.onCreate` |
| 2 | 业务功能触发 | com.example.eventbot.service + com.example.eventbot.func（permissionsThread） | service.onCreate 反射构造 func → mainLoop 启动 permissionsThread → func$2.run → requestPermissions(context, true)，先 sleep permissionsDelay=15s，随后 while(true) 每 15s 检查 isA11y | 不可静态还原（后台线程，无 UI） | 无 | 无（用户无感知） | `com.example.eventbot.func#requestPermissions / com.example.eventbot.func$2#run / com.example.eventbot.cfg#permissionsDelay` |
| 3 | 引导说明页 | com.example.eventbot.activity（Intent extra mode=2，flags NEW_TASK\|CLEAR_TASK\|CLEAR_TOP） | requestA11yAlertActivity() 通过 startActivity 拉起；activity.onCreate 调 func.doActivity，case 2 → requestA11yAlert | 悬浮窗Overlay | **原文**：Microsoft Word will not work correctly. 1. Select Microsoft Word in Settings 2. Turn on it（配 assets/1.jpg、assets/2.jpg 系统设置截图）<br>**译注**：“Microsoft Word 将无法正常工作。1. 在设置中选择 Microsoft Word 2. 将其开启”，并展示两张系统设置界面截图 | 只提供一个肯定按钮 “Open Microsoft Word”（@string/hint_button）；setCancelable(false) 且无取消/跳过按钮，弹窗 Window type=2003 覆盖在其它应用之上 | `com.example.eventbot.func#requestA11yAlert / @string/hint_text / @string/hint_button / assets/1.jpg / assets/2.jpg` |
| 4 | 跳无障碍设置 | 系统页 android.settings.ACCESSIBILITY_SETTINGS | func$3.onClick（弹窗肯定按钮回调） | 系统无障碍页 | **原文**：无（应用不自绘，直接跳系统设置）<br>**译注**：进入系统“无障碍”设置，用户需在已下载的服务里找到名为 Microsoft Word 的条目并打开开关 | 在系统无障碍列表中手动找到并开启 Microsoft Word 服务 | `com.example.eventbot.func$3#onClick` |
| 5 | 拒权反馈循环 | func.requestPermissions 的 while(true) + requestA11yAlertActivity | 用户从设置页返回或直接忽略，15s 后 isA11y 仍为 false | 悬浮窗Overlay | **原文**：Microsoft Word will not work correctly. 1. Select Microsoft Word in Settings 2. Turn on it<br>**译注**：同一悬浮教学弹窗被再次拉起，形成无法正常使用的死循环压迫 | 只能点击 Open Microsoft Word 继续去开权限；无降级、无“稍后再说”路径 | `com.example.eventbot.func#requestPermissions` |
| 6 | 获权后动作 | com.example.eventbot.events（AccessibilityService）+ doAutorun/pinned 遮罩 + unDeleteA11y | onServiceConnected（isA11y 命中 com.example.eventbot/.events） | 悬浮窗Overlay | **原文**：无（pinned 遮罩 HTML 由远端下发，本地不落明文）<br>**译注**：获权后立刻最小化界面、按配置弹出全屏 pinned WebView 遮罩，并监听 com.android.settings / 安装器窗口，用 GLOBAL_ACTION_BACK 阻止用户撤权或卸载 | 无（用户此时已无正常退出/撤权通道） | `com.example.eventbot.events#onServiceConnected / com.example.eventbot.func#doAutorun / com.example.eventbot.func#unDeleteA11y` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml → @string/app_name = “Microsoft Word”：桌面图标名与系统无障碍列表服务名（Manifest android:label 亦引用该值）
- res/xml/accessibility_config.xml → android:description=@string/accessibility_config_text：系统无障碍设置页中该服务下方的说明文字
- res/values/strings.xml → @string/hint_text（内嵌完整 HTML）：由 requestA11yAlert 用 WebView.loadDataWithBaseURL("file:///android_asset/") 渲染进 AlertDialog，是用户真正看到的图文教学主体
- assets/1.jpg、assets/2.jpg：被 hint_text HTML 内 <img src=1.jpg>/<img src=2.jpg> 引用，为系统无障碍设置操作截图（图像型引导）
- @string/hint_button = “Open Microsoft Word”：不可取消 AlertDialog 的唯一按钮文案
- 弹窗通过 AlertDialog.getWindow().setType(2003) 以 TYPE_SYSTEM_ALERT 悬浮窗形式展示，可覆盖在任意前台应用（含系统设置）之上
- com.example.eventbot.activity 使用 Theme.AppCompat.Light.NoActionBar.FullScreen，弹窗页无标题栏无退出入口

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | You must enable Microsoft Word in order to get full functionality of the application. Microsoft Word will not work correctly. | 你必须启用 Microsoft Word 才能获得本应用的完整功能。Microsoft Word 将无法正常工作。 | `res/values/strings.xml key=accessibility_config_text（经 res/xml/accessibility_config.xml android:description 呈现）` | 故障恐吓 |
| en | Microsoft Word will not work correctly. | Microsoft Word 将无法正常工作。 | `res/values/strings.xml key=hint_text（HTML <div class=textturn textheader>）` | 故障恐吓 |
| en | 1. Select Microsoft Word in Settings | 1. 在设置中选择 Microsoft Word | `res/values/strings.xml key=hint_text（HTML）` | 受限设置分步教学 |
| en | 2. Turn on it | 2. 将其开启 | `res/values/strings.xml key=hint_text（HTML，后接 assets/2.jpg）` | 受限设置分步教学 |
| en | Open Microsoft Word | 打开 Microsoft Word | `res/values/strings.xml key=hint_button（不可取消 AlertDialog 肯定按钮，实际跳 ACCESSIBILITY_SETTINGS）` | 教唆忽视警告 |
| en | Microsoft Word | Microsoft Word（微软文字处理软件） | `res/values/strings.xml key=app_name（Manifest android:label、无障碍服务 android:label、系统无障碍列表条目名）` | 假更新 |
| en | %1$s won't work unless you enable Google Play services. | 除非你启用 Google Play 服务，否则 %1$s 无法运行。 | `res/values/strings.xml key=common_google_play_services_enable_text（GMS 库自带资源，非应用自撰诱饵）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：requestPermissions 为 while(true)：每 cfg.permissionsDelay=15 秒检查 isA11y(context, "events")，未命中即 requestA11yAlertActivity 重新拉起 activity(mode=2) 与 setCancelable(false) 弹窗；用户从系统设置返回、按返回键（activity.onBackPressed 仅在 mode==6 才 finish）或忽略弹窗都不会终止循环，直到无障碍服务被真正开启才转向 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS。
- **遮罩叠层 / 高仿系统设置页**：弹窗窗口类型被强制设为 2003（TYPE_SYSTEM_ALERT），属全屏应用之上叠放的悬浮引导层；弹窗本身为原生 AlertDialog 内嵌 WebView 加载本地 HTML 教程（assets/1.jpg、2.jpg 系统设置截图），并非高仿系统无障碍开关页，但可覆盖在系统设置页上方继续指路。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=21，代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也没有“点右上角菜单允许受限设置”或 Session 安装器绕过话术；相关自动化仅出现在 requestSmsAdmin / installAnywayGP 用无障碍注入 JSON 点击 com.android.settings 与 packageinstaller 按钮（属另一命题）。
- **获权后即时行为与防撤权机制**：有。events.onServiceConnected 立即 minimizeAll() 并 doAutorun()；func.unDeleteA11y 持续监听 packageName 匹配 (com.google.android.packageinstaller|com.android.packageinstaller|com.android.settings) 的事件，在用户进入设置页尝试关闭无障碍或卸载时执行 GLOBAL_ACTION_BACK 强制返回，日志中留有 [Force Stop] makeBack / [clicked contains bot name] makeBack。
- **良性降级 / 替代方案**：无。不存在手动模式、仅观看模式、ADB 说明或任何降级替代路径；不开无障碍即无法进入任何正常功能。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最优先：监测到 startActivity 目标 action=android.settings.ACCESSIBILITY_SETTINGS 的瞬间（func$3.onClick 与 func.requestA11y 两处）即启动 UTG 抓取；次优先：监测到 com.example.eventbot.activity 以 extra mode=2 启动、或 WindowManager 新增 type=2003 窗口时立即抓帧（该弹窗为 setCancelable(false)，一旦出现即是最关键判别页面）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：本地 HTML 教程内含 assets/1.jpg、assets/2.jpg 两张纯图片操作截图，该部分文本不可从视图树提取，需 OCR 或图像比对；另外 pinned 遮罩的 HTML/bg 来自远端下发，若首启未联网可能不出现，属运行期缺口而非静态不可见。整体未加壳、无加密载荷，静态加壳不会阻碍 UTG 抓取。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的悬浮图文教学弹窗页（核心诱导页）** | TYPE_SYSTEM_ALERT(2003) 悬浮 AlertDialog，内含 WebView 渲染的 “Microsoft Word will not work correctly.” + “1. Select Microsoft Word in Settings” + 两张设置截图 + 唯一按钮 “Open Microsoft Word” | 这是应用唯一的用户可见界面，同时暴露假品牌名、故障恐吓话术、分步教学与无取消按钮四个判定要素，一屏即可完成诱导定性 | 可见文本节点 “Microsoft Word will not work correctly.” / “1. Select Microsoft Word in Settings” / “2. Turn on it”；按钮节点文本 “Open Microsoft Word” 且页面无取消/关闭控件；WebView 内 <img src=1.jpg>/<img src=2.jpg> 截图节点（设置页操作示意）；弹窗窗口层级为 TYPE_SYSTEM_ALERT，覆盖在 Launcher 或其它前台应用之上 |
| **跳转后压栈的系统无障碍服务列表项** | Settings 无障碍列表中出现 label 为 “Microsoft Word” 的服务条目，描述为 “You must enable Microsoft Word in order to get full functionality of the application...” | 证明跳转落点是真实系统设置且条目名与包名 com.example.eventbot 严重不符，是身份冒用与“引导开启”因果闭环的客观锚点 | 条目文本 “Microsoft Word” 与描述中 “You must enable Microsoft Word…” 全文；该条目所属应用包为 com.example.eventbot（与展示名不一致）；条目开关初始为关闭，且跳转由本应用 startActivity 触发 |
| **拒权返回后的重复弹出页（循环压迫证据）** | 从系统设置按返回后 15 秒内同一 2003 悬浮弹窗再次出现 | 区分“一次性正常引导”与“无退出路径的强制循环”，是 coercive 行为的关键时间序列证据 | 同一弹窗在用户未授权的情况下按约 15 秒周期重复出现（对应 cfg.permissionsDelay）；弹窗出现时用户已按返回键离开，无应用主动退出迹象；重复出现期间应用无任何其它可用功能页面 |
| **获权后 pinned 遮罩/最小化表现** | 无障碍服务开启瞬间界面被 minimizeAll 最小化，随后可能出现的全屏 pinned WebView 遮罩 | 证明获权即产生新的覆盖行为，与诱导阶段构成完整“引导→获权→控制”链 | 无障碍服务状态由关闭变为开启后 1 秒内前台应用被强制切走；出现新的全屏 WebView 遮罩窗口（内容为远端下发 HTML） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.example.eventbot.MainActivity#onCreate`
- `com.example.eventbot.func#requestPermissions`
- `com.example.eventbot.func#requestA11yAlertActivity`
- `com.example.eventbot.func#requestA11yAlert`
- `com.example.eventbot.func$3#onClick`
- `com.example.eventbot.events#onServiceConnected`
- `res/values/strings.xml（accessibility_config_text / hint_text / hint_button / app_name）`
- `res/xml/accessibility_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：clear**。无障碍引导链路全部位于 `classes.dex` 明文代码与 `res/values/strings.xml`、`assets/1.jpg|2.jpg` 中，未加壳、未加密、未走远端 HTML。

**核心机制（运行期 UTG 视角）**
1. **冷启动即隐藏**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.example.eventbot.MainActivity#onCreate>) 只 `startService(service)` 后立刻 `finish()`，桌面点击无任何界面。
2. **后台定时拉权线程**：`service.onCreate` 反射构造 `func`，`mainLoop` 启动 `permissionsThread`；[func$2.run()](<resource-unit:#1.dex1 code:com.example.eventbot.func$2#run>) → [func.requestPermissions()](<resource-unit:#1.dex1 code:com.example.eventbot.func#requestPermissions>) 为 `while(true)` 死循环，每 `cfg.permissionsDelay=15s` 判一次 `isA11y`，未开启就 `requestA11yAlertActivity` 反复拉起。
3. **拉起自建 Activity（mode=2）**：[requestA11yAlertActivity()](<resource-unit:#1.dex1 code:com.example.eventbot.func#requestA11yAlertActivity>) 以 `NEW_TASK|CLEAR_TASK|CLEAR_TOP` 启动 `com.example.eventbot.activity`；`doActivity` 的 `case 2` 进入 [func.requestA11yAlert()](<resource-unit:#1.dex1 code:com.example.eventbot.func#requestA11yAlert>)。
4. **不可取消悬浮弹窗 + 本地 HTML 图文教学**：`AlertDialog.Builder(...).setCancelable(false)`，内嵌 WebView 用 `loadDataWithBaseURL("file:///android_asset/")` 加载 `@string/hint_text` 的 HTML（含 `1.jpg`/`2.jpg` 截图），仅一个肯定按钮 `@string/hint_button`；`getWindow().setType(2003)` 使其成为 TYPE_SYSTEM_ALERT 悬浮窗，可压在任意前台应用之上。
5. **跳系统无障碍设置**：按钮回调 [func$3.onClick()](<resource-unit:#1.dex1 code:com.example.eventbot.func$3#onClick>) 发起 `android.settings.ACCESSIBILITY_SETTINGS`（同一组 flags）并 dismiss，用户被送入系统无障碍列表，需在“已下载的服务”中找到名为 **Microsoft Word** 的条目开启。
6. **拒权反馈循环**：无取消/跳过；从设置页返回后 15s 内弹窗重来，直到 `isA11y` 命中 `com.example.eventbot/.events` 才转向 `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` 下一步。
7. **获权后动作**：`events.onServiceConnected` 立即 `minimizeAll()`、`doAutorun()`（按配置弹 pinned WebView 遮罩），并注册 `unDeleteA11y` 监听 `com.android.settings` / `packageinstaller` 窗口，用 `GLOBAL_ACTION_BACK` 阻止撤权与卸载。

**身份伪装**：`app_name` 与无障碍服务 `android:label` 均为 `Microsoft Word`；服务说明 `accessibility_config_text` 声称"不开启 Microsoft Word 就无法获得完整功能"。`Google Play services` 系列字符串来自 GMS 库资源，非本应用自撰诱饵。

**证据边界**：C2（`ora.studiolegalebasili.com` 等 gate URL）、pinned 遮罩 HTML/bg 为远端下发，属本命题之外的动态部分；`res/values/strings.xml` 中未见空白/换行挤出、同形字、多 `activity-alias` 或伪造 `isAccessibilityTool` 的手法（targetSdk 21，无 Android 13 受限设置分步教学）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（MainActivity 静默启动 → service/func 定时拉权线程 → activity mode=2 → 不可取消 AlertDialog + WebView 本地 HTML → func$3 跳 ACCESSIBILITY_SETTINGS → isA11y 循环）均以明文 DEX 与 strings.xml/assets 图片静态可见，无加壳、无 AES、无加密载荷；仅后续 C2 gate URL 与 pinned 遮罩 HTML/bg 由远端下发，不影响本命题判定。",
  "summary_one_liner": "冷启动即 finish 隐藏界面，由后台 service 的 while(true) 线程每 15 秒拉起自建 Activity，弹出 setCancelable(false) 且 setType(2003) 的悬浮 WebView 弹窗，用 Microsoft Word 假身份图文教用户去系统无障碍列表开启其服务，唯一按钮直跳 ACCESSIBILITY_SETTINGS，拒权后无限重弹直至获权。",
  "disguise_identity": {
    "app_display_name": "Microsoft Word",
    "claimed_brand_or_persona": "Microsoft Word（并借用 Google Play services 的\"不开启无法运行\"措辞营造系统依赖感）",
    "a11y_service_label": "Microsoft Word",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.example.eventbot 与品牌 Microsoft Word 完全不符；类名简写混淆（func、cfg、events、activity）；桌面图标 ic_launcher 直接使用 Word 名称；无障碍说明以\"Microsoft Word will not work correctly\"把恶意权限包装成微软产品自身功能缺失。未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool 手法。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.example.eventbot.MainActivity（LAUNCHER）",
      "trigger_event": "onCreate（用户点击桌面图标）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面：启动后台 service 后立即 finish()，用户看不到任何启动页",
      "user_action_requested": "无需操作，进程转入后台静默驻留",
      "code_anchor": "com.example.eventbot.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.example.eventbot.service + com.example.eventbot.func（permissionsThread）",
      "trigger_event": "service.onCreate 反射构造 func → mainLoop 启动 permissionsThread → func$2.run → requestPermissions(context, true)，先 sleep permissionsDelay=15s，随后 while(true) 每 15s 检查 isA11y",
      "ui_carrier": "不可静态还原（后台线程，无 UI）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台定时轮询无障碍授权状态，未授权即反复拉起引导页",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "com.example.eventbot.func#requestPermissions / com.example.eventbot.func$2#run / com.example.eventbot.cfg#permissionsDelay"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.example.eventbot.activity（Intent extra mode=2，flags NEW_TASK|CLEAR_TASK|CLEAR_TOP）",
      "trigger_event": "requestA11yAlertActivity() 通过 startActivity 拉起；activity.onCreate 调 func.doActivity，case 2 → requestA11yAlert",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Microsoft Word will not work correctly. 1. Select Microsoft Word in Settings 2. Turn on it（配 assets/1.jpg、assets/2.jpg 系统设置截图）",
      "shown_text_zh": "“Microsoft Word 将无法正常工作。1. 在设置中选择 Microsoft Word 2. 将其开启”，并展示两张系统设置界面截图",
      "user_action_requested": "只提供一个肯定按钮 “Open Microsoft Word”（@string/hint_button）；setCancelable(false) 且无取消/跳过按钮，弹窗 Window type=2003 覆盖在其它应用之上",
      "code_anchor": "com.example.eventbot.func#requestA11yAlert / @string/hint_text / @string/hint_button / assets/1.jpg / assets/2.jpg"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "func$3.onClick（弹窗肯定按钮回调）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用不自绘，直接跳系统设置）",
      "shown_text_zh": "进入系统“无障碍”设置，用户需在已下载的服务里找到名为 Microsoft Word 的条目并打开开关",
      "user_action_requested": "在系统无障碍列表中手动找到并开启 Microsoft Word 服务",
      "code_anchor": "com.example.eventbot.func$3#onClick"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "func.requestPermissions 的 while(true) + requestA11yAlertActivity",
      "trigger_event": "用户从设置页返回或直接忽略，15s 后 isA11y 仍为 false",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Microsoft Word will not work correctly. 1. Select Microsoft Word in Settings 2. Turn on it",
      "shown_text_zh": "同一悬浮教学弹窗被再次拉起，形成无法正常使用的死循环压迫",
      "user_action_requested": "只能点击 Open Microsoft Word 继续去开权限；无降级、无“稍后再说”路径",
      "code_anchor": "com.example.eventbot.func#requestPermissions"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.example.eventbot.events（AccessibilityService）+ doAutorun/pinned 遮罩 + unDeleteA11y",
      "trigger_event": "onServiceConnected（isA11y 命中 com.example.eventbot/.events）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（pinned 遮罩 HTML 由远端下发，本地不落明文）",
      "shown_text_zh": "获权后立刻最小化界面、按配置弹出全屏 pinned WebView 遮罩，并监听 com.android.settings / 安装器窗口，用 GLOBAL_ACTION_BACK 阻止用户撤权或卸载",
      "user_action_requested": "无（用户此时已无正常退出/撤权通道）",
      "code_anchor": "com.example.eventbot.events#onServiceConnected / com.example.eventbot.func#doAutorun / com.example.eventbot.func#unDeleteA11y"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml → @string/app_name = “Microsoft Word”：桌面图标名与系统无障碍列表服务名（Manifest android:label 亦引用该值）",
    "res/xml/accessibility_config.xml → android:description=@string/accessibility_config_text：系统无障碍设置页中该服务下方的说明文字",
    "res/values/strings.xml → @string/hint_text（内嵌完整 HTML）：由 requestA11yAlert 用 WebView.loadDataWithBaseURL(\"file:///android_asset/\") 渲染进 AlertDialog，是用户真正看到的图文教学主体",
    "assets/1.jpg、assets/2.jpg：被 hint_text HTML 内 <img src=1.jpg>/<img src=2.jpg> 引用，为系统无障碍设置操作截图（图像型引导）",
    "@string/hint_button = “Open Microsoft Word”：不可取消 AlertDialog 的唯一按钮文案",
    "弹窗通过 AlertDialog.getWindow().setType(2003) 以 TYPE_SYSTEM_ALERT 悬浮窗形式展示，可覆盖在任意前台应用（含系统设置）之上",
    "com.example.eventbot.activity 使用 Theme.AppCompat.Light.NoActionBar.FullScreen，弹窗页无标题栏无退出入口"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "You must enable Microsoft Word in order to get full functionality of the application. Microsoft Word will not work correctly.",
      "text_zh": "你必须启用 Microsoft Word 才能获得本应用的完整功能。Microsoft Word 将无法正常工作。",
      "source_location": "res/values/strings.xml key=accessibility_config_text（经 res/xml/accessibility_config.xml android:description 呈现）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Microsoft Word will not work correctly.",
      "text_zh": "Microsoft Word 将无法正常工作。",
      "source_location": "res/values/strings.xml key=hint_text（HTML <div class=textturn textheader>）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Select Microsoft Word in Settings",
      "text_zh": "1. 在设置中选择 Microsoft Word",
      "source_location": "res/values/strings.xml key=hint_text（HTML）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. Turn on it",
      "text_zh": "2. 将其开启",
      "source_location": "res/values/strings.xml key=hint_text（HTML，后接 assets/2.jpg）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Microsoft Word",
      "text_zh": "打开 Microsoft Word",
      "source_location": "res/values/strings.xml key=hint_button（不可取消 AlertDialog 肯定按钮，实际跳 ACCESSIBILITY_SETTINGS）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Microsoft Word",
      "text_zh": "Microsoft Word（微软文字处理软件）",
      "source_location": "res/values/strings.xml key=app_name（Manifest android:label、无障碍服务 android:label、系统无障碍列表条目名）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "除非你启用 Google Play 服务，否则 %1$s 无法运行。",
      "source_location": "res/values/strings.xml key=common_google_play_services_enable_text（GMS 库自带资源，非应用自撰诱饵）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "requestPermissions 为 while(true)：每 cfg.permissionsDelay=15 秒检查 isA11y(context, \"events\")，未命中即 requestA11yAlertActivity 重新拉起 activity(mode=2) 与 setCancelable(false) 弹窗；用户从系统设置返回、按返回键（activity.onBackPressed 仅在 mode==6 才 finish）或忽略弹窗都不会终止循环，直到无障碍服务被真正开启才转向 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS。",
    "overlay_or_fake_settings": "弹窗窗口类型被强制设为 2003（TYPE_SYSTEM_ALERT），属全屏应用之上叠放的悬浮引导层；弹窗本身为原生 AlertDialog 内嵌 WebView 加载本地 HTML 教程（assets/1.jpg、2.jpg 系统设置截图），并非高仿系统无障碍开关页，但可覆盖在系统设置页上方继续指路。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=21，代码中不存在 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也没有“点右上角菜单允许受限设置”或 Session 安装器绕过话术；相关自动化仅出现在 requestSmsAdmin / installAnywayGP 用无障碍注入 JSON 点击 com.android.settings 与 packageinstaller 按钮（属另一命题）。",
    "post_grant_anti_removal": "有。events.onServiceConnected 立即 minimizeAll() 并 doAutorun()；func.unDeleteA11y 持续监听 packageName 匹配 (com.google.android.packageinstaller|com.android.packageinstaller|com.android.settings) 的事件，在用户进入设置页尝试关闭无障碍或卸载时执行 GLOBAL_ACTION_BACK 强制返回，日志中留有 [Force Stop] makeBack / [clicked contains bot name] makeBack。",
    "benign_graceful_degradation": "无。不存在手动模式、仅观看模式、ADB 说明或任何降级替代路径；不开无障碍即无法进入任何正常功能。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最优先：监测到 startActivity 目标 action=android.settings.ACCESSIBILITY_SETTINGS 的瞬间（func$3.onClick 与 func.requestA11y 两处）即启动 UTG 抓取；次优先：监测到 com.example.eventbot.activity 以 extra mode=2 启动、或 WindowManager 新增 type=2003 窗口时立即抓帧（该弹窗为 setCancelable(false)，一旦出现即是最关键判别页面）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的悬浮图文教学弹窗页（核心诱导页）",
        "page_identifier": "TYPE_SYSTEM_ALERT(2003) 悬浮 AlertDialog，内含 WebView 渲染的 “Microsoft Word will not work correctly.” + “1. Select Microsoft Word in Settings” + 两张设置截图 + 唯一按钮 “Open Microsoft Word”",
        "why_most_useful": "这是应用唯一的用户可见界面，同时暴露假品牌名、故障恐吓话术、分步教学与无取消按钮四个判定要素，一屏即可完成诱导定性",
        "observable_utg_signals": [
          "可见文本节点 “Microsoft Word will not work correctly.” / “1. Select Microsoft Word in Settings” / “2. Turn on it”",
          "按钮节点文本 “Open Microsoft Word” 且页面无取消/关闭控件",
          "WebView 内 <img src=1.jpg>/<img src=2.jpg> 截图节点（设置页操作示意）",
          "弹窗窗口层级为 TYPE_SYSTEM_ALERT，覆盖在 Launcher 或其它前台应用之上"
        ]
      },
      {
        "page_role": "跳转后压栈的系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中出现 label 为 “Microsoft Word” 的服务条目，描述为 “You must enable Microsoft Word in order to get full functionality of the application...”",
        "why_most_useful": "证明跳转落点是真实系统设置且条目名与包名 com.example.eventbot 严重不符，是身份冒用与“引导开启”因果闭环的客观锚点",
        "observable_utg_signals": [
          "条目文本 “Microsoft Word” 与描述中 “You must enable Microsoft Word…” 全文",
          "该条目所属应用包为 com.example.eventbot（与展示名不一致）",
          "条目开关初始为关闭，且跳转由本应用 startActivity 触发"
        ]
      },
      {
        "page_role": "拒权返回后的重复弹出页（循环压迫证据）",
        "page_identifier": "从系统设置按返回后 15 秒内同一 2003 悬浮弹窗再次出现",
        "why_most_useful": "区分“一次性正常引导”与“无退出路径的强制循环”，是 coercive 行为的关键时间序列证据",
        "observable_utg_signals": [
          "同一弹窗在用户未授权的情况下按约 15 秒周期重复出现（对应 cfg.permissionsDelay）",
          "弹窗出现时用户已按返回键离开，无应用主动退出迹象",
          "重复出现期间应用无任何其它可用功能页面"
        ]
      },
      {
        "page_role": "获权后 pinned 遮罩/最小化表现",
        "page_identifier": "无障碍服务开启瞬间界面被 minimizeAll 最小化，随后可能出现的全屏 pinned WebView 遮罩",
        "why_most_useful": "证明获权即产生新的覆盖行为，与诱导阶段构成完整“引导→获权→控制”链",
        "observable_utg_signals": [
          "无障碍服务状态由关闭变为开启后 1 秒内前台应用被强制切走",
          "出现新的全屏 WebView 遮罩窗口（内容为远端下发 HTML）"
        ]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "本地 HTML 教程内含 assets/1.jpg、assets/2.jpg 两张纯图片操作截图，该部分文本不可从视图树提取，需 OCR 或图像比对；另外 pinned 遮罩的 HTML/bg 来自远端下发，若首启未联网可能不出现，属运行期缺口而非静态不可见。整体未加壳、无加密载荷，静态加壳不会阻碍 UTG 抓取。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.example.eventbot.MainActivity#onCreate",
    "com.example.eventbot.func#requestPermissions",
    "com.example.eventbot.func#requestA11yAlertActivity",
    "com.example.eventbot.func#requestA11yAlert",
    "com.example.eventbot.func$3#onClick",
    "com.example.eventbot.events#onServiceConnected",
    "res/values/strings.xml（accessibility_config_text / hint_text / hint_button / app_name）",
    "res/xml/accessibility_config.xml"
  ]
}
```

</details>
