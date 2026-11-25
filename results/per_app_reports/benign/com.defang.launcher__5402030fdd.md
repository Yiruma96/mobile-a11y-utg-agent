# BN_028__5402030fdd｜极简桌面与双击锁屏 — Defang

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：192.3s

## 1. 一句话核心结论

- **核心申请方式**：Defang 以原生 Compose 设置卡片 + 冷启动按需触发，通过携带 :settings:fragment_args_key 的 ACTION_ACCESSIBILITY_SETTINGS 深链把用户直接送到自家服务开关，文案明示读取前台应用与地址栏 URL 且不记录浏览历史，无遮罩、无死循环、无伪造设置页。
- **静态可见性说明**：全部分析对象完整静态可见：Manifest、res/xml/accessibility_service_config.xml、res/values/strings.xml（含 accessibility_service_description、perm_accessibility_* 等）与 DEX 反编译代码均为明文；未发现加壳、AES 加密资源、二阶段载荷或远端 HTML，引导文案全部来自本地 strings.xml，无 WebView 承载。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5402030fddc9ba50f547bc52d28b3a8dd6f00797f87aca80b1fc7d5c1f47b8ca` |
| 包名 / 年份 | `com.defang.launcher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.defang.launcher_26.apk |
| 桌面显示名 | Defang |
| 引导页宣称品牌/身份 | Defang（F-Droid 开源极简桌面 / 数字自律 speed bump 工具，无第三方品牌冒用） |
| 系统无障碍列表服务名 | Defang launcher |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未发现空白/换行挤出警告、同形字、多 activity-alias 伪装或多入口诱导弹窗；accessibility_service_config.xml 未设置 android:isAccessibilityTool，不伪造无障碍工具以规避系统隐私提示；仅 R8 常规标识符混淆（类名 a/b/e3 等），不影响资源与文案可读性。 |
| 无障碍服务类名 | `com.defang.launcher.service.accessibility.DefangAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, READ_CONTACTS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Detects which app is in the foreground and reads the URL bar in your browser so Defang can show a pause screen before watched apps or adult websites open. Defang does not log, store, or transmit your browsing history. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.defang.launcher.ui.launcher.LauncherActivity（HOME/LAUNCHER，singleTask） | onResume → 协程 LauncherActivity$onResume$1.invokeSuspend 调用 GatePermissionPolicy.needsGatePermissions() | 原生Activity | **原文**：无（此步不显示文案，仅做条件判定）<br>**译注**：无 | 无需操作；仅在 hasWatched()/hasEnabled()/builtinAdultListEnabled 为真（用户已配置受管应用或成人网址拦截）时才进入后续权限流程 | `com.defang.launcher.ui.launcher.LauncherActivity$onResume$1#invokeSuspend / com.defang.launcher.util.GatePermissionPolicy#needsGatePermissions` |
| 2 | 跳受限设置 | 系统悬浮窗权限页 android.settings.action.MANAGE_OVERLAY_PERMISSION?package=com.defang.launcher | onResume 中 needsGatePermissions()==true 且 overlayPrompted==false 且 !Settings.canDrawOverlays() → startActivity，并置 overlayPrompted=true（每进程仅一次） | 系统无障碍页 | **原文**：perm_overlay_title: Draw over other apps / perm_overlay_body: Defang needs this to show the pause screen before watched apps open. Without it, the core feature doesn't work.<br>**译注**：标题「在其他应用上层显示」；说明「Defang 需要它在受管应用打开前显示暂停屏，没有它核心功能无法工作。」 | 在系统页手动打开「允许在其他应用上层显示」；可直接返回不授予（仅提示一次，不重复拉起） | `LauncherActivity$onResume$1#invokeSuspend / res/values/strings.xml perm_overlay_title, perm_overlay_body` |
| 3 | 跳无障碍设置 | 系统设置无障碍页（Intent android.settings.ACCESSIBILITY_SETTINGS + :settings:fragment_args_key 深链至 DefangAccessibilityService） | AccessibilityServiceHelper.ensureEnabled()：若 DefangAccessibilityService.Companion.isRunning() 为 false 且 tryEnableSelf() 失败且 !isEnabled() → openAccessibilitySettings() | 系统无障碍页 | **原文**：perm_accessibility_title: Accessibility permission / perm_accessibility_body: Defang needs to know when a watched app opens, and reads the browser's address bar to recognise adult domains. It never reads page content, messages, or anything you type — only the foreground app and the URL in the address field. / perm_accessibility_grant: Open accessibility settings<br>**译注**：标题「无障碍权限」；说明「Defang 需要知道受管应用何时打开，并读取浏览器地址栏以识别成人域名。它从不读取页面内容、消息或你输入的任何内容——只读取前台应用与地址栏中的 URL。」；按钮「打开无障碍设置」 | 在系统无障碍列表中把「Defang launcher」开关打开；可返回不开启（系统页本身可退出） | `com.defang.launcher.util.AccessibilityServiceHelper#ensureEnabled / #openAccessibilitySettings / #component / res/values/strings.xml perm_accessibility_*` |
| 4 | 引导说明页 | com.defang.launcher.ui.onboarding.OnboardingActivity（Compose 五页引导） | 首次启动进入 onCreate（也可从 Settings 的 settings_onboarding_replay「Read the intro again」重看） | 原生Activity | **原文**：This is a speed bump. Not a wall. / Some apps will block your phone completely. Some will go full grayscale through developer settings. This is not that. You can still open Instagram. You can still override the timer. Nothing here is impossible to bypass. / Skip<br>**译注**：「这是一道减速带，不是一堵墙。」「有些应用会彻底封锁手机，有些会通过开发者设置全屏灰阶。本应用不是那样。你仍然可以打开 Instagram，仍然可以覆盖计时器。这里没有任何东西是无法绕过的。」；按钮「跳过」 | 阅读后点「Next →」/「Continue to setup →」，或点「Skip」跳过；本页不索取任何权限 | `com.defang.launcher.ui.onboarding.OnboardingActivity#onCreate / res/values/strings.xml onboarding_1_heading, onboarding_1_body, onboarding_skip` |
| 5 | 引导说明页 | com.defang.launcher.ui.settings.SettingsActivity（Compose 权限卡片列表） | 用户在设置页点击「Accessibility permission」卡片 → SettingsActivity$onCreate$1$1.invoke$lambda$77$lambda$76 | 原生Activity | **原文**：Accessibility permission / Defang needs to know when a watched app opens, and reads the browser's address bar to recognise adult domains. It never reads page content, messages, or anything you type — only the foreground app and the URL in the address field. / Open accessibility settings<br>**译注**：「无障碍权限」卡片及上述同一段说明；操作按钮「打开无障碍设置」 | 点击卡片/按钮跳转系统无障碍设置；不点击则停留原页，无强制弹窗 | `com.defang.launcher.ui.settings.SettingsActivity$onCreate$1$1#invoke$lambda$77$lambda$76 / ComposableSingletons$SettingsActivityKt$lambda-58$1#invoke` |
| 6 | 拒权反馈循环 | Toast + 再次进入系统无障碍页（Handler 延迟 1500ms 后 openAccessibilitySettings） | ensureEnabled() 或设置页跳转后调用 verifyRebindLanded() → postDelayed(1500ms) → 若 !isRunning 且 now-lastAutoPromptMs >= 60000 则再次 openAccessibilitySettings | 通知栏 | **原文**：Accessibility service enabled / Already enabled — you can turn it off here<br>**译注**：「无障碍服务已启用」／「已启用——你可以在这里关闭它」 | 返回应用后若仍未开启，最多每 60 秒被再引导一次到系统设置页；无死循环、无定时器高频拉起，用户可忽略并继续使用桌面 | `com.defang.launcher.util.AccessibilityServiceHelper#verifyRebindLanded / #verifyRebindLanded$lambda$7（AUTO_PROMPT_COOLDOWN_MS = 60000）` |
| 7 | 获权后动作 | com.defang.launcher.service.accessibility.DefangAccessibilityService#onServiceConnected + OverlayManager 暂停屏 | 系统绑定服务后 onServiceConnected()：isRunning=true，注册 SCREEN_OFF/USER_PRESENT、NFC、QR 接收器并启动前台应用轮询协程 | 悬浮窗Overlay | **原文**：（暂停屏文案取自界面资源，本次未逐条展开）I need more time / Why do you need more time?<br>**译注**：「我需要更多时间」／「你为什么需要更多时间？」——受管应用打开前的暂停屏提问 | 在暂停屏上作答以继续使用受管应用；应用内提供关闭服务入口（Already enabled — you can turn it off here） | `com.defang.launcher.service.accessibility.DefangAccessibilityService#onServiceConnected / #onAccessibilityEvent` |
| 8 | 获权后动作 | 系统设置（WRITE_SECURE_SETTINGS 静默自开启路径，tryEnableSelf） | ensureEnabled()/设置页点击时，若 checkSelfPermission(WRITE_SECURE_SETTINGS)==0 → 直接 Settings.Secure.putString("enabled_accessibility_services", ...) 并 300ms 后写入 | 不可静态还原 | **原文**：Accessibility service enabled<br>**译注**：「无障碍服务已启用」（成功静默开启后的 Toast，无系统页） | 无用户交互；该路径仅在用户通过 adb/特权方式主动授予 WRITE_SECURE_SETTINGS 后可用，普通安装不触发 | `com.defang.launcher.util.AccessibilityServiceHelper#tryEnableSelf / #tryEnableSelf$enable` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表条目描述：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description（「Detects which app is in the foreground and reads the URL bar…」）
- 系统无障碍列表服务名称：AndroidManifest 中 service android:label=@string/accessibility_service_label（「Defang launcher」）
- 应用内设置页 Compose 权限卡片：SettingsActivity 中 perm_accessibility_title / perm_accessibility_body / perm_accessibility_grant 三串渲染（ComposableSingletons$SettingsActivityKt$lambda-58$1#invoke 渲染 body）
- 跳转前/拒权后的原生 Toast：SettingsActivity$onCreate$1$1.invoke$lambda$77$lambda$76 弹出 accessibility_already_on 或 accessibility_now_on
- 首次启动五页引导 Activity：OnboardingActivity 的 onboarding_1_heading/body … onboarding_5_heading/body，含 onboarding_next / onboarding_continue / onboarding_skip 按钮文案
- 同类相邻权限卡片（同一设置页内并列）：perm_overlay_title/body/grant、perm_usage_stats_title/body/grant、perm_battery_title/body/grant（Samsung 电池优化说明）
- 未使用 WebView / assets HTML / 悬浮遮罩承载引导文字；未发现空白挤出、换行藏字或图片化诱导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Detects which app is in the foreground and reads the URL bar in your browser so Defang can show a pause screen before watched apps or adult websites open. Defang does not log, store, or transmit your browsing history. | 检测哪个应用位于前台，并读取浏览器地址栏，以便 Defang 在受管应用或成人网站打开前显示暂停屏。Defang 不会记录、存储或传输你的浏览历史。 | `res/values/strings.xml key=accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）` | 隐私承诺 |
| en | Defang needs to know when a watched app opens, and reads the browser's address bar to recognise adult domains. It never reads page content, messages, or anything you type — only the foreground app and the URL in the address field. | Defang 需要知道受管应用何时打开，并读取浏览器地址栏以识别成人域名。它从不读取页面内容、消息或你输入的任何内容——只读取前台应用与地址栏中的 URL。 | `res/values/strings.xml key=perm_accessibility_body（SettingsActivity 卡片正文）` | 良性透明说明 |
| en | Accessibility permission | 无障碍权限 | `res/values/strings.xml key=perm_accessibility_title` | 良性透明说明 |
| en | Open accessibility settings | 打开无障碍设置 | `res/values/strings.xml key=perm_accessibility_grant` | 受限设置分步教学 |
| en | Already enabled — you can turn it off here | 已启用——你可以在这里关闭它 | `res/values/strings.xml key=accessibility_already_on（SettingsActivity$onCreate$1$1.invoke$lambda$77$lambda$76 Toast）` | 良性透明说明 |
| en | Accessibility service enabled | 无障碍服务已启用 | `res/values/strings.xml key=accessibility_now_on（tryEnableSelf 成功后的 Toast）` | 良性透明说明 |
| en | This is a speed bump. Not a wall. | 这是一道减速带，不是一堵墙。 | `res/values/strings.xml key=onboarding_1_heading（OnboardingActivity 第 1 页）` | 良性透明说明 |
| en | Some apps will block your phone completely. Some will go full grayscale through developer settings. This is not that. You can still open Instagram. You can still override the timer. Nothing here is impossible to bypass. | 有些应用会彻底封锁你的手机，有些会通过开发者设置进入全屏灰阶。本应用不是那样。你仍然可以打开 Instagram，仍然可以覆盖计时器。这里没有任何东西是无法绕过的。 | `res/values/strings.xml key=onboarding_1_body` | 良性透明说明 |
| en | Defang needs this to show the pause screen before watched apps open. Without it, the core feature doesn't work. | Defang 需要它在受管应用打开前显示暂停屏。没有它，核心功能无法工作。 | `res/values/strings.xml key=perm_overlay_body（MANAGE_OVERLAY_PERMISSION 卡片）` | 良性透明说明 |
| en | Samsung's battery management can kill background services, which would stop the session timer working. Tap to exclude Defang from battery optimisation. | 三星的电池管理会杀掉后台服务，导致会话计时器失效。点击将 Defang 排除出电池优化。 | `res/values/strings.xml key=perm_battery_body` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：非死循环：verifyRebindLanded() 在 1500ms 后检查 DefangAccessibilityService.Companion.isRunning()，仍未运行且距 lastAutoPromptMs 超过 AUTO_PROMPT_COOLDOWN_MS=60000ms 时才再次 openAccessibilitySettings；LauncherActivity 每次 onResume 会再走一次 ensureEnabled，但受同一 60s 冷却限制。用户返回后可直接使用桌面，无持续压栈、无定时器高频拉起。
- **遮罩叠层 / 高仿系统设置页**：无。不叠放半透明引导遮罩、不弹全屏悬浮窗、不绘制高仿系统无障碍开关页；引导仅由原生 Compose 卡片 + Toast 承担，跳转目标为真实系统设置页（携带 :settings:fragment_args_key 仅用于滚动定位到本服务项）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现「应用详情 → 右上角菜单 → 允许受限设置」的分步教学，也未使用 Session 安装器绕过；仅在自身已持有 WRITE_SECURE_SETTINGS（adb/特权授予）时静默写入 enabled_accessibility_services。
- **获权后即时行为与防撤权机制**：无。未见 performGlobalAction / GLOBAL_ACTION_BACK / GLOBAL_ACTION_HOME，未见监听设置页自点确认或拦截撤权；onInterrupt() 反而主动 dismissAll() 并清空待处理闸门，设置页文案明示「Already enabled — you can turn it off here」。
- **良性降级 / 替代方案**：具备：① 无障碍未开启时应用本身仍可作为 HOME 桌面运行，暂停屏失效但不阻断使用；② 权限流程仅在用户已配置受管应用/成人网址名单后触发，未配置时完全不打扰；③ 悬浮窗权限提示每进程仅一次（overlayPrompted）；④ 引导页提供 Skip，设置页提供「Read the intro again」可回看。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 且 extras 含 :settings:fragment_args_key 的瞬间抓取跳转前应用侧页面；同时捕获 LauncherActivity onResume（needsGatePermissions 为真时）与 SettingsActivity 无障碍卡片点击这两处前置帧。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。仅需注意 tryEnableSelf 分支在应用持有 WRITE_SECURE_SETTINGS 时会静默写入 enabled_accessibility_services 而不出现任何系统设置页，此时 UTG 看不到权限申请流程，需通过 Toast「Accessibility service enabled」与 Settings.Secure 变更观测；该权限普通安装无法获得，实际影响有限。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前应用内说明卡片页（SettingsActivity 无障碍权限卡片）** | 标题「Accessibility permission」+ 正文含「It never reads page content, messages, or anything you type」+ 按钮「Open accessibility settings」的 Compose 列表页 | 这是唯一显式向用户交代无障碍用途与边界的界面，可据此判断是透明告知还是话术包装 | 标题与正文是否与 AndroidManifest android:description 一致；是否存在「不授予就无法使用」等恐吓措辞；是否出现伪造系统控件或半透明遮罩 |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载/已安装服务中 label 为「Defang launcher」的条目及其 description 摘要 | 核对系统侧展示的服务名与说明是否与代码资源一致，识别空白挤出、同形字或 isAccessibilityTool 伪装 | 服务显示名是否为「Defang launcher」；描述是否被截断或替换为诱导文案；系统是否显示受限设置警告（未声明 isAccessibilityTool） |
| **冷启动/回桌面自动跳转前的过渡帧** | LauncherActivity 桌面帧之后直接切到系统无障碍页，无中间弹窗 | 验证自动跳转是否零说明直接压栈，还是先有说明卡片，从而区分按需触发与冷启动诱导 | 跳转前是否存在可取消的说明弹窗；从桌面到系统设置页的间隔是否异常短；返回桌面后是否立即再次跳转（60s 冷却是否生效） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.defang.launcher.util.AccessibilityServiceHelper#openAccessibilitySettings`
- `com.defang.launcher.util.AccessibilityServiceHelper#ensureEnabled`
- `com.defang.launcher.util.AccessibilityServiceHelper#verifyRebindLanded$lambda$7`
- `com.defang.launcher.ui.launcher.LauncherActivity$onResume$1#invokeSuspend`
- `com.defang.launcher.ui.settings.SettingsActivity$onCreate$1$1#invoke$lambda$77$lambda$76`
- `res/xml/accessibility_service_config.xml + res/values/strings.xml(accessibility_service_description, perm_accessibility_*, onboarding_1_body)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（静态核验，12 次工具内收口）

- **无加壳、无远端 HTML、无 WebView、无伪造设置页**：全部引导为原生 Compose 界面 + 系统设置页跳转，字符串资源明文本地可见，静态可见性完整。
- **无障碍申请入口有两条**：① 用户在设置页主动点「Accessibility permission」卡片 → `SettingsActivity$onCreate$1$1.invoke$lambda$77$lambda$76` → 未开启则 `openAccessibilitySettings()`；② 冷启动/回桌面时 `LauncherActivity.onResume` → `GatePermissionPolicy.needsGatePermissions()` 返回 true（仅在**已配置受管应用/受管网址/内置成人名单**时）→ `AccessibilityServiceHelper.ensureEnabled()` 自动拉起无障碍设置。
- **跳转采用「深链定位」而非泛跳**：`ACTION_ACCESSIBILITY_SETTINGS` 携带 `:settings:fragment_args_key` = 本服务 `ComponentName` 扁平串，直接把用户送到 Defang 服务开关项，省去在列表里找服务（属"受限设置分步教学"的良性变体）。
- **存在静默自开启通道但受限**：`tryEnableSelf()` 仅在自身持有 `WRITE_SECURE_SETTINGS`（adb/特权授予，普通安装不可得）时直接改写 `enabled_accessibility_services`，成功则只弹 Toast「Accessibility service enabled」；否则退回系统设置页。
- **拒权反馈为有限重跳而非死循环**：`verifyRebindLanded()` 延迟 1500ms 检查服务是否 `isRunning`，未运行且距上次自动提示 >60s（`AUTO_PROMPT_COOLDOWN_MS`）才再次跳设置页；无 `performGlobalAction`、无 BACK/HOME 阻止撤权、无监听设置页自点确认。
- **身份与文案诚实**：显示名 `Defang`、服务标签 `Defang launcher`、`android:description` 明确说明"读取前台应用与浏览器地址栏 URL，不记录/存储/传输浏览历史"；`accessibility_service_config.xml` 未声明 `isAccessibilityTool`，不冒充无障碍工具以规避系统隐私警告。
- **获权后行为**：`onAccessibilityEvent` 仅处理窗口状态变化、浏览器地址栏文本变化（2048）与自家 LauncherActivity 事件，配合 `OverlayManager` 弹"暂停屏"，属声明的核心功能，未见越权读取页面内容/消息/输入。

未发现诱导性伪装、恐吓话术或强制不可取消弹窗，未登记风险。唯一需备注的中性能力是 `WRITE_SECURE_SETTINGS` 静默自开启路径，其取得依赖用户自行 adb 授权，不构成越权。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部分析对象完整静态可见：Manifest、res/xml/accessibility_service_config.xml、res/values/strings.xml（含 accessibility_service_description、perm_accessibility_* 等）与 DEX 反编译代码均为明文；未发现加壳、AES 加密资源、二阶段载荷或远端 HTML，引导文案全部来自本地 strings.xml，无 WebView 承载。",
  "summary_one_liner": "Defang 以原生 Compose 设置卡片 + 冷启动按需触发，通过携带 :settings:fragment_args_key 的 ACTION_ACCESSIBILITY_SETTINGS 深链把用户直接送到自家服务开关，文案明示读取前台应用与地址栏 URL 且不记录浏览历史，无遮罩、无死循环、无伪造设置页。",
  "disguise_identity": {
    "app_display_name": "Defang",
    "claimed_brand_or_persona": "Defang（F-Droid 开源极简桌面 / 数字自律 speed bump 工具，无第三方品牌冒用）",
    "a11y_service_label": "Defang launcher",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未发现空白/换行挤出警告、同形字、多 activity-alias 伪装或多入口诱导弹窗；accessibility_service_config.xml 未设置 android:isAccessibilityTool，不伪造无障碍工具以规避系统隐私提示；仅 R8 常规标识符混淆（类名 a/b/e3 等），不影响资源与文案可读性。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.defang.launcher.ui.launcher.LauncherActivity（HOME/LAUNCHER，singleTask）",
      "trigger_event": "onResume → 协程 LauncherActivity$onResume$1.invokeSuspend 调用 GatePermissionPolicy.needsGatePermissions()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（此步不显示文案，仅做条件判定）",
      "shown_text_zh": "无",
      "user_action_requested": "无需操作；仅在 hasWatched()/hasEnabled()/builtinAdultListEnabled 为真（用户已配置受管应用或成人网址拦截）时才进入后续权限流程",
      "code_anchor": "com.defang.launcher.ui.launcher.LauncherActivity$onResume$1#invokeSuspend / com.defang.launcher.util.GatePermissionPolicy#needsGatePermissions"
    },
    {
      "step": 2,
      "stage": "跳受限设置",
      "screen_or_component": "系统悬浮窗权限页 android.settings.action.MANAGE_OVERLAY_PERMISSION?package=com.defang.launcher",
      "trigger_event": "onResume 中 needsGatePermissions()==true 且 overlayPrompted==false 且 !Settings.canDrawOverlays() → startActivity，并置 overlayPrompted=true（每进程仅一次）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "perm_overlay_title: Draw over other apps / perm_overlay_body: Defang needs this to show the pause screen before watched apps open. Without it, the core feature doesn't work.",
      "shown_text_zh": "标题「在其他应用上层显示」；说明「Defang 需要它在受管应用打开前显示暂停屏，没有它核心功能无法工作。」",
      "user_action_requested": "在系统页手动打开「允许在其他应用上层显示」；可直接返回不授予（仅提示一次，不重复拉起）",
      "code_anchor": "LauncherActivity$onResume$1#invokeSuspend / res/values/strings.xml perm_overlay_title, perm_overlay_body"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置无障碍页（Intent android.settings.ACCESSIBILITY_SETTINGS + :settings:fragment_args_key 深链至 DefangAccessibilityService）",
      "trigger_event": "AccessibilityServiceHelper.ensureEnabled()：若 DefangAccessibilityService.Companion.isRunning() 为 false 且 tryEnableSelf() 失败且 !isEnabled() → openAccessibilitySettings()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "perm_accessibility_title: Accessibility permission / perm_accessibility_body: Defang needs to know when a watched app opens, and reads the browser's address bar to recognise adult domains. It never reads page content, messages, or anything you type — only the foreground app and the URL in the address field. / perm_accessibility_grant: Open accessibility settings",
      "shown_text_zh": "标题「无障碍权限」；说明「Defang 需要知道受管应用何时打开，并读取浏览器地址栏以识别成人域名。它从不读取页面内容、消息或你输入的任何内容——只读取前台应用与地址栏中的 URL。」；按钮「打开无障碍设置」",
      "user_action_requested": "在系统无障碍列表中把「Defang launcher」开关打开；可返回不开启（系统页本身可退出）",
      "code_anchor": "com.defang.launcher.util.AccessibilityServiceHelper#ensureEnabled / #openAccessibilitySettings / #component / res/values/strings.xml perm_accessibility_*"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "com.defang.launcher.ui.onboarding.OnboardingActivity（Compose 五页引导）",
      "trigger_event": "首次启动进入 onCreate（也可从 Settings 的 settings_onboarding_replay「Read the intro again」重看）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "This is a speed bump. Not a wall. / Some apps will block your phone completely. Some will go full grayscale through developer settings. This is not that. You can still open Instagram. You can still override the timer. Nothing here is impossible to bypass. / Skip",
      "shown_text_zh": "「这是一道减速带，不是一堵墙。」「有些应用会彻底封锁手机，有些会通过开发者设置全屏灰阶。本应用不是那样。你仍然可以打开 Instagram，仍然可以覆盖计时器。这里没有任何东西是无法绕过的。」；按钮「跳过」",
      "user_action_requested": "阅读后点「Next →」/「Continue to setup →」，或点「Skip」跳过；本页不索取任何权限",
      "code_anchor": "com.defang.launcher.ui.onboarding.OnboardingActivity#onCreate / res/values/strings.xml onboarding_1_heading, onboarding_1_body, onboarding_skip"
    },
    {
      "step": 5,
      "stage": "引导说明页",
      "screen_or_component": "com.defang.launcher.ui.settings.SettingsActivity（Compose 权限卡片列表）",
      "trigger_event": "用户在设置页点击「Accessibility permission」卡片 → SettingsActivity$onCreate$1$1.invoke$lambda$77$lambda$76",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility permission / Defang needs to know when a watched app opens, and reads the browser's address bar to recognise adult domains. It never reads page content, messages, or anything you type — only the foreground app and the URL in the address field. / Open accessibility settings",
      "shown_text_zh": "「无障碍权限」卡片及上述同一段说明；操作按钮「打开无障碍设置」",
      "user_action_requested": "点击卡片/按钮跳转系统无障碍设置；不点击则停留原页，无强制弹窗",
      "code_anchor": "com.defang.launcher.ui.settings.SettingsActivity$onCreate$1$1#invoke$lambda$77$lambda$76 / ComposableSingletons$SettingsActivityKt$lambda-58$1#invoke"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "Toast + 再次进入系统无障碍页（Handler 延迟 1500ms 后 openAccessibilitySettings）",
      "trigger_event": "ensureEnabled() 或设置页跳转后调用 verifyRebindLanded() → postDelayed(1500ms) → 若 !isRunning 且 now-lastAutoPromptMs >= 60000 则再次 openAccessibilitySettings",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Accessibility service enabled / Already enabled — you can turn it off here",
      "shown_text_zh": "「无障碍服务已启用」／「已启用——你可以在这里关闭它」",
      "user_action_requested": "返回应用后若仍未开启，最多每 60 秒被再引导一次到系统设置页；无死循环、无定时器高频拉起，用户可忽略并继续使用桌面",
      "code_anchor": "com.defang.launcher.util.AccessibilityServiceHelper#verifyRebindLanded / #verifyRebindLanded$lambda$7（AUTO_PROMPT_COOLDOWN_MS = 60000）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.defang.launcher.service.accessibility.DefangAccessibilityService#onServiceConnected + OverlayManager 暂停屏",
      "trigger_event": "系统绑定服务后 onServiceConnected()：isRunning=true，注册 SCREEN_OFF/USER_PRESENT、NFC、QR 接收器并启动前台应用轮询协程",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "（暂停屏文案取自界面资源，本次未逐条展开）I need more time / Why do you need more time?",
      "shown_text_zh": "「我需要更多时间」／「你为什么需要更多时间？」——受管应用打开前的暂停屏提问",
      "user_action_requested": "在暂停屏上作答以继续使用受管应用；应用内提供关闭服务入口（Already enabled — you can turn it off here）",
      "code_anchor": "com.defang.launcher.service.accessibility.DefangAccessibilityService#onServiceConnected / #onAccessibilityEvent"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "系统设置（WRITE_SECURE_SETTINGS 静默自开启路径，tryEnableSelf）",
      "trigger_event": "ensureEnabled()/设置页点击时，若 checkSelfPermission(WRITE_SECURE_SETTINGS)==0 → 直接 Settings.Secure.putString(\"enabled_accessibility_services\", ...) 并 300ms 后写入",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Accessibility service enabled",
      "shown_text_zh": "「无障碍服务已启用」（成功静默开启后的 Toast，无系统页）",
      "user_action_requested": "无用户交互；该路径仅在用户通过 adb/特权方式主动授予 WRITE_SECURE_SETTINGS 后可用，普通安装不触发",
      "code_anchor": "com.defang.launcher.util.AccessibilityServiceHelper#tryEnableSelf / #tryEnableSelf$enable"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表条目描述：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_service_description（「Detects which app is in the foreground and reads the URL bar…」）",
    "系统无障碍列表服务名称：AndroidManifest 中 service android:label=@string/accessibility_service_label（「Defang launcher」）",
    "应用内设置页 Compose 权限卡片：SettingsActivity 中 perm_accessibility_title / perm_accessibility_body / perm_accessibility_grant 三串渲染（ComposableSingletons$SettingsActivityKt$lambda-58$1#invoke 渲染 body）",
    "跳转前/拒权后的原生 Toast：SettingsActivity$onCreate$1$1.invoke$lambda$77$lambda$76 弹出 accessibility_already_on 或 accessibility_now_on",
    "首次启动五页引导 Activity：OnboardingActivity 的 onboarding_1_heading/body … onboarding_5_heading/body，含 onboarding_next / onboarding_continue / onboarding_skip 按钮文案",
    "同类相邻权限卡片（同一设置页内并列）：perm_overlay_title/body/grant、perm_usage_stats_title/body/grant、perm_battery_title/body/grant（Samsung 电池优化说明）",
    "未使用 WebView / assets HTML / 悬浮遮罩承载引导文字；未发现空白挤出、换行藏字或图片化诱导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Detects which app is in the foreground and reads the URL bar in your browser so Defang can show a pause screen before watched apps or adult websites open. Defang does not log, store, or transmit your browsing history.",
      "text_zh": "检测哪个应用位于前台，并读取浏览器地址栏，以便 Defang 在受管应用或成人网站打开前显示暂停屏。Defang 不会记录、存储或传输你的浏览历史。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Defang needs to know when a watched app opens, and reads the browser's address bar to recognise adult domains. It never reads page content, messages, or anything you type — only the foreground app and the URL in the address field.",
      "text_zh": "Defang 需要知道受管应用何时打开，并读取浏览器地址栏以识别成人域名。它从不读取页面内容、消息或你输入的任何内容——只读取前台应用与地址栏中的 URL。",
      "source_location": "res/values/strings.xml key=perm_accessibility_body（SettingsActivity 卡片正文）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility permission",
      "text_zh": "无障碍权限",
      "source_location": "res/values/strings.xml key=perm_accessibility_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Open accessibility settings",
      "text_zh": "打开无障碍设置",
      "source_location": "res/values/strings.xml key=perm_accessibility_grant",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Already enabled — you can turn it off here",
      "text_zh": "已启用——你可以在这里关闭它",
      "source_location": "res/values/strings.xml key=accessibility_already_on（SettingsActivity$onCreate$1$1.invoke$lambda$77$lambda$76 Toast）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility service enabled",
      "text_zh": "无障碍服务已启用",
      "source_location": "res/values/strings.xml key=accessibility_now_on（tryEnableSelf 成功后的 Toast）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This is a speed bump. Not a wall.",
      "text_zh": "这是一道减速带，不是一堵墙。",
      "source_location": "res/values/strings.xml key=onboarding_1_heading（OnboardingActivity 第 1 页）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Some apps will block your phone completely. Some will go full grayscale through developer settings. This is not that. You can still open Instagram. You can still override the timer. Nothing here is impossible to bypass.",
      "text_zh": "有些应用会彻底封锁你的手机，有些会通过开发者设置进入全屏灰阶。本应用不是那样。你仍然可以打开 Instagram，仍然可以覆盖计时器。这里没有任何东西是无法绕过的。",
      "source_location": "res/values/strings.xml key=onboarding_1_body",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Defang needs this to show the pause screen before watched apps open. Without it, the core feature doesn't work.",
      "text_zh": "Defang 需要它在受管应用打开前显示暂停屏。没有它，核心功能无法工作。",
      "source_location": "res/values/strings.xml key=perm_overlay_body（MANAGE_OVERLAY_PERMISSION 卡片）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Samsung's battery management can kill background services, which would stop the session timer working. Tap to exclude Defang from battery optimisation.",
      "text_zh": "三星的电池管理会杀掉后台服务，导致会话计时器失效。点击将 Defang 排除出电池优化。",
      "source_location": "res/values/strings.xml key=perm_battery_body",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "非死循环：verifyRebindLanded() 在 1500ms 后检查 DefangAccessibilityService.Companion.isRunning()，仍未运行且距 lastAutoPromptMs 超过 AUTO_PROMPT_COOLDOWN_MS=60000ms 时才再次 openAccessibilitySettings；LauncherActivity 每次 onResume 会再走一次 ensureEnabled，但受同一 60s 冷却限制。用户返回后可直接使用桌面，无持续压栈、无定时器高频拉起。",
    "overlay_or_fake_settings": "无。不叠放半透明引导遮罩、不弹全屏悬浮窗、不绘制高仿系统无障碍开关页；引导仅由原生 Compose 卡片 + Toast 承担，跳转目标为真实系统设置页（携带 :settings:fragment_args_key 仅用于滚动定位到本服务项）。",
    "restricted_settings_13plus_coaching": "无。未出现「应用详情 → 右上角菜单 → 允许受限设置」的分步教学，也未使用 Session 安装器绕过；仅在自身已持有 WRITE_SECURE_SETTINGS（adb/特权授予）时静默写入 enabled_accessibility_services。",
    "post_grant_anti_removal": "无。未见 performGlobalAction / GLOBAL_ACTION_BACK / GLOBAL_ACTION_HOME，未见监听设置页自点确认或拦截撤权；onInterrupt() 反而主动 dismissAll() 并清空待处理闸门，设置页文案明示「Already enabled — you can turn it off here」。",
    "benign_graceful_degradation": "具备：① 无障碍未开启时应用本身仍可作为 HOME 桌面运行，暂停屏失效但不阻断使用；② 权限流程仅在用户已配置受管应用/成人网址名单后触发，未配置时完全不打扰；③ 悬浮窗权限提示每进程仅一次（overlayPrompted）；④ 引导页提供 Skip，设置页提供「Read the intro again」可回看。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 且 extras 含 :settings:fragment_args_key 的瞬间抓取跳转前应用侧页面；同时捕获 LauncherActivity onResume（needsGatePermissions 为真时）与 SettingsActivity 无障碍卡片点击这两处前置帧。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前应用内说明卡片页（SettingsActivity 无障碍权限卡片）",
        "page_identifier": "标题「Accessibility permission」+ 正文含「It never reads page content, messages, or anything you type」+ 按钮「Open accessibility settings」的 Compose 列表页",
        "why_most_useful": "这是唯一显式向用户交代无障碍用途与边界的界面，可据此判断是透明告知还是话术包装",
        "observable_utg_signals": ["标题与正文是否与 AndroidManifest android:description 一致", "是否存在「不授予就无法使用」等恐吓措辞", "是否出现伪造系统控件或半透明遮罩"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载/已安装服务中 label 为「Defang launcher」的条目及其 description 摘要",
        "why_most_useful": "核对系统侧展示的服务名与说明是否与代码资源一致，识别空白挤出、同形字或 isAccessibilityTool 伪装",
        "observable_utg_signals": ["服务显示名是否为「Defang launcher」", "描述是否被截断或替换为诱导文案", "系统是否显示受限设置警告（未声明 isAccessibilityTool）"]
      },
      {
        "page_role": "冷启动/回桌面自动跳转前的过渡帧",
        "page_identifier": "LauncherActivity 桌面帧之后直接切到系统无障碍页，无中间弹窗",
        "why_most_useful": "验证自动跳转是否零说明直接压栈，还是先有说明卡片，从而区分按需触发与冷启动诱导",
        "observable_utg_signals": ["跳转前是否存在可取消的说明弹窗", "从桌面到系统设置页的间隔是否异常短", "返回桌面后是否立即再次跳转（60s 冷却是否生效）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。仅需注意 tryEnableSelf 分支在应用持有 WRITE_SECURE_SETTINGS 时会静默写入 enabled_accessibility_services 而不出现任何系统设置页，此时 UTG 看不到权限申请流程，需通过 Toast「Accessibility service enabled」与 Settings.Secure 变更观测；该权限普通安装无法获得，实际影响有限。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
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
    "com.defang.launcher.util.AccessibilityServiceHelper#openAccessibilitySettings",
    "com.defang.launcher.util.AccessibilityServiceHelper#ensureEnabled",
    "com.defang.launcher.util.AccessibilityServiceHelper#verifyRebindLanded$lambda$7",
    "com.defang.launcher.ui.launcher.LauncherActivity$onResume$1#invokeSuspend",
    "com.defang.launcher.ui.settings.SettingsActivity$onCreate$1$1#invoke$lambda$77$lambda$76",
    "res/xml/accessibility_service_config.xml + res/values/strings.xml(accessibility_service_description, perm_accessibility_*, onboarding_1_body)"
  ]
}
```

</details>
