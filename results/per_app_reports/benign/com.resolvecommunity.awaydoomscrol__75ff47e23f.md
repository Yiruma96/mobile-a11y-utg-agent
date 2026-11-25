# BN_048__75ff47e23f｜系统效率与通用辅助 — AwayDoomscrollin'

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：129.4s

## 1. 一句话核心结论

- **核心申请方式**：冷启动 5 步 Compose 原生引导 → 可选电池豁免 → 原生 AlertDialog 知情同意 → 标准 ACCESSIBILITY_SETTINGS Intent 直达自身服务条目，全程可跳过、可拒绝，获权后仅做受限四包内的规则化 Back/tap/curtain 保护
- **静态可见性说明**：DEX（classes.dex）与全部资源可完整静态还原：无障碍服务类、Compose 引导流、AlertDialog、跳转 Intent 与全部 strings.xml 文案均可见；无加壳、无 AES 密文载荷、无远端 HTML、无 assets 内嵌引导页（assets 仅含 baseline.prof 等）
- **命中的行为模式标签**：`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `75ff47e23f552b72d0123c758c175781af2824b8d1396c9907836a2da3ca2bd9` |
| 包名 / 年份 | `com.resolvecommunity.awaydoomscrollin` / 2025-2026 |
| 家族 / 品类 | **系统效率与通用辅助**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.resolvecommunity.awaydoomscrollin_12.apk |
| 桌面显示名 | AwayDoomscrollin' |
| 引导页宣称品牌/身份 | AwayDoomscrollin'（F-Droid 开源防沉迷/打破刷屏循环工具，开发者 Resolve Community） |
| 系统无障碍列表服务名 | AwayDoomscrollin'（service 无独立 android:label，系统列表继承应用名；描述取 @string/accessibility_service_description） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未使用空白/换行挤出警告、同形字、多 activity-alias 伪装；android:isAccessibilityTool 显式声明为 false，未伪造系统工具身份；仅单一 launcher Activity 与单一无障碍 Service |
| 无障碍服务类名 | `com.resolvecommunity.awaydoomscrollin.AntiScrollService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：com.instagram.android,com.zhiliaoapp.musically,com.ss.android.ugc.trill,com.google.android.youtube |
| 共现高危权限 | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |
| 系统设置项说明 (`android:description`) | AwayDoomscrollin' examines accessibility text and labels, view identifiers, window changes, taps and scroll events on your device to recognize protected feeds and short videos in Instagram, TikTok and YouTube. It can show curtains in Instagram and YouTube and perform specific, rule-based Back, tap and scroll actions on protected screens. Screen information is processed only on your device and never sent to a server. On-screen text is not saved; a short troubleshooting log stays on the device only if you turn it on in About. Optional usage-data sharing is a separate choice. Changes to other apps' interfaces can affect detection. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | MainActivity（Compose，Theme.AwaySplashScreen）→ OnboardingScreen 第 1~4 步 | onCreate / LAUNCHER 启动且引导未完成（rememberSaveable 步进状态，显示 'Step %1$s / 5 ·'） | 原生Activity | **原文**：Step %1$s / 5 ·<br>**译注**：第 X 步 / 共 5 步 | 阅读介绍并下一步；页面为可滚动引导，可随时离开（无强制阻断） | `com.resolvecommunity.awaydoomscrollin.lc.OnboardingScreen / OnboardingStepOne~FourAppsAndPrefs / strings.xml main_step_x_5` |
| 2 | 引导说明页 | OnboardingStepFivePermissions（权限说明步，含 PermissionMatrixCard） | 引导进入第 5 步；rememberAccessibilityStatus 读取保护服务状态决定展示 'Access enabled' 或权限待开启 | 原生Activity | **原文**：AwayDoomscrollin' needs Accessibility access to recognize the feeds and short videos you choose to protect in Instagram, TikTok and YouTube. … This screen information is processed only on your device and is never sent to a server. … You can continue without granting access; protection will remain off.<br>**译注**：应用需要无障碍权限来识别你在 Instagram、TikTok、YouTube 中选择保护的动态与短视频；屏幕信息仅在本机处理、绝不发送到服务器；你可以在不授权的情况下继续使用，保护将保持关闭。 | 点击 'Turn on protection' 继续；页面同时提供 'Continue without permission' 跳过路径 | `com.resolvecommunity.awaydoomscrollin.lc.OnboardingStepFivePermissions / strings.xml main_awaydoomscrollin_needs_accessibility_access_to_r, main_turn_on_protection, main_continue_without_permission` |
| 3 | 跳受限设置 | 系统电池优化豁免页（REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，本包 URI），失败回退 IGNORE_BATTERY_OPTIMIZATION_SETTINGS 列表页 | OnboardingStepFivePermissions 中点击后经 m7.l 分支 0：若尚未允许后台运行则 startActivity(REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)；若已允许则直接 lc.H(context) | 系统无障碍页 | **原文**：Allow running in the background / main_battery_allowed=Allowed<br>**译注**：允许在后台运行；已允许。属电池优化豁免，不是“受限设置（13+）”教学 | 在系统页选择“允许”；可返回，不阻断后续引导 | `com.resolvecommunity.awaydoomscrollin.m7#l / com.resolvecommunity.awaydoomscrollin.lc#H / strings.xml main_battery_allow` |
| 4 | 引导说明页 | AccessibilityConsentDialog（Compose material3 AlertDialog） | 点击开启保护后，若 prefs 中 accessibility_disclosure_version < 1 则先弹知情同意对话框（h0.l default 分支：<1 置 showDialog=true，否则直接 lc.F 跳设置） | 原生Dialog | **原文**：Agree and open settings / Not now / Later<br>**译注**：同意并打开设置 / 暂不 / 稍后 | 选择“同意并打开设置”才继续跳系统无障碍页；存在明确的取消/稍后按钮，可取消 | `com.resolvecommunity.awaydoomscrollin.lc.AccessibilityConsentDialog / com.resolvecommunity.awaydoomscrollin.h0#l / strings.xml main_agree_and_open_settings, main_not_now, main_later` |
| 5 | 跳无障碍设置 | 系统设置：设置 > 无障碍 > 已安装/已下载的服务 > AwayDoomscrollin'（Intent android.settings.ACCESSIBILITY_SETTINGS + :settings:fragment_args_key=ComponentName(AntiScrollService)） | lc.u(context)：commit 写入 accessibility_disclosure_version=1 成功后调用 lc.F(context)；F 先 Toast 展示按厂商定制的设置路径，再 startActivity 无障碍设置 | 系统无障碍页 | **原文**：Settings > Accessibility > Downloaded apps (or Installed services) > AwayDoomscrollin'（另含华为/三星/小米/OPPO/vivo 变体文案 main_settings_additional_settings_accessibility_downl、main_settings_shortcuts_accessibility_accessibility_d 等）<br>**译注**：设置 > 无障碍 > 已下载的应用（或已安装的服务）> AwayDoomscrollin'；按手机品牌给出不同进入路径提示（Toast） | 在系统无障碍列表中手动找到并开启本应用服务；无自动勾选、无脚本代点 | `com.resolvecommunity.awaydoomscrollin.lc#F / com.resolvecommunity.awaydoomscrollin.lc#u / strings.xml main_settings_accessibility_downloaded_apps_or_instal` |
| 6 | 获权后动作 | MainActivity 主界面 / AntiScrollService 运行；主界面卡片显示 'Access enabled' | 返回应用后 rememberAccessibilityStatus 读取服务状态（sc.d 表示已连接）；服务 onAccessibilityEvent 仅在 com.instagram.android / com.zhiliaoapp.musically / com.ss.android.ugc.trill / com.google.android.youtube 内按规则执行 curtain/Back/tap/scroll | 原生Activity | **原文**：Access enabled / Accessibility is required for protection. Notifications are optional. / You can turn protection off at any time, in the app or in Android's accessibility settings.<br>**译注**：已启用 / 保护需要无障碍权限，通知是可选的 / 你可随时在应用内或系统无障碍设置中关闭保护 | 无进一步强制动作；用户可随时在应用内或系统设置关闭 | `com.resolvecommunity.awaydoomscrollin.lc#rememberAccessibilityStatus / com.resolvecommunity.awaydoomscrollin.AntiScrollService#onAccessibilityEvent / strings.xml main_access_enabled, main_you_can_turn_protection_off_at` |
| 7 | 拒权反馈循环 | 系统通知栏（ProtectionWatchdogReceiver 触发） | 看门狗定时/重启发：若 service_running_mark=true 且 watchdog_stop_suspected=true（服务被系统清除）→ 发通知，按钮携带 ACCESSIBILITY_SETTINGS Intent；非小米机型额外给出 Autostart 说明按钮 | 通知栏 | **原文**：Protection is disabled. If not re-enabled, your daily streak will reset in 24 hours. / Xiaomi stopped protection in the background. Turn on Autostart so it comes back by itself, then turn protection on again.<br>**译注**：保护已停用；若未重新开启，你的每日连续记录将在 24 小时后重置 / 小米在后台停止了保护，请开启自启动后重新开启保护 | 可选点击通知跳系统无障碍页重新开启；不点击不影响使用，无死循环重跳、无遮挡 | `com.resolvecommunity.awaydoomscrollin.ProtectionWatchdogReceiver#onReceive / strings.xml notif_protection_stopped_text, notif_xiaomi_stopped_text` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表描述：res/xml/accessibility_service_config.xml android:description=@string/accessibility_service_description（完整披露采集范围、本地处理与不落盘承诺）
- OnboardingStepFivePermissions 引导页正文：strings.xml main_awaydoomscrollin_needs_accessibility_access_to_r（长文披露）
- Compose AlertDialog（AccessibilityConsentDialog）：按钮 Agree and open settings / Not now / Later
- 主页/仪表盘卡片：main_turn_on_accessibility_so_awaydoomscrollin_can、main_accessibility_is_required_for_protection_notific、main_on_accessibility_permission_required、main_protection_stuck_hint
- 跳转前厂商定制 Toast：lc.F 按 Build.MANUFACTURER 选择 main_settings_accessibility_* 系列设置路径文案
- 电池豁免卡片：main_battery_allow、main_xiaomi_autostart_note（小米专属自启动说明）
- 系统通知栏：notif_protection_stopped_text / notif_xiaomi_stopped_text（含跳设置按钮）
- 无 WebView/HTML/悬浮窗承载任何引导文案（assets 目录仅 baseline.prof/dexopt，无引导页面）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | AwayDoomscrollin' examines accessibility text and labels, view identifiers, window changes, taps and scroll events on your device to recognize protected feeds and short videos in Instagram, TikTok and YouTube. It can show curtains in Instagram and YouTube and perform specific, rule-based Back, tap and scroll actions on protected screens. Screen information is processed only on your device and never sent to a server. | 本应用检查设备上的无障碍文本与标签、视图标识、窗口变化、点击与滚动事件，以识别 Instagram、TikTok 和 YouTube 中被保护的动态与短视频；可在 Instagram 和 YouTube 显示遮挡层，并在受保护页面上执行特定的、基于规则的返回、点击与滚动操作。屏幕信息仅在本机处理，绝不发送到服务器。 | `res/values/strings.xml / accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）` | 良性透明说明 |
| en | You can continue without granting access; protection will remain off. | 你可以在不授予权限的情况下继续使用；保护将保持关闭。 | `res/values/strings.xml / main_awaydoomscrollin_needs_accessibility_access_to_r` | 良性透明说明 |
| en | This screen information is processed only on your device and is never sent to a server. Text, labels and view identifiers are not saved; if you turn on the troubleshooting log in About, a short record of what protection did stays on your device for 24 hours, and sharing it is up to you. | 这些屏幕信息仅在本机处理，绝不发送到服务器；文本、标签与视图标识不会被保存；若你在“关于”中开启排障日志，保护行为的简短记录仅在本机保留 24 小时，是否分享由你决定。 | `res/values/strings.xml / main_awaydoomscrollin_needs_accessibility_access_to_r` | 隐私承诺 |
| en | Settings > Accessibility > Downloaded apps (or Installed services) > AwayDoomscrollin' | 设置 > 无障碍 > 已下载的应用（或已安装的服务）> AwayDoomscrollin' | `res/values/strings.xml / main_settings_accessibility_downloaded_apps_or_instal（另有华为/三星/小米/OPPO/vivo 变体）` | 受限设置分步教学 |
| en | You can turn protection off at any time, in the app or in Android's accessibility settings. | 你可随时在应用内或 Android 无障碍设置中关闭保护。 | `res/values/strings.xml / main_you_can_turn_protection_off_at` | 良性透明说明 |
| en | Turn on Accessibility so AwayDoomscrollin' can protect you automatically. | 开启无障碍，让 AwayDoomscrollin' 自动保护你。 | `res/values/strings.xml / main_turn_on_accessibility_so_awaydoomscrollin_can` | 良性透明说明 |
| en | Protection is disabled. If not re-enabled, your daily streak will reset in 24 hours. | 保护已停用；若未重新开启，你的每日连续记录将在 24 小时后重置。 | `res/values/strings.xml / notif_protection_stopped_text（ProtectionWatchdogReceiver 通知）` | 良性透明说明 |
| en | Android stopped protection in the background, but its switch still shows on. In Accessibility, turn AwayDoomscrollin' off and on again. | Android 在后台停止了保护，但开关仍显示为开启。请在无障碍中把 AwayDoomscrollin' 关闭再重新开启。 | `res/values/strings.xml / main_protection_stuck_hint` | 良性透明说明 |
| en | Agree and open settings | 同意并打开设置 | `res/values/strings.xml / main_agree_and_open_settings（AccessibilityConsentDialog 确认按钮）` | 良性透明说明 |
| en | Not now / Later / Continue without permission | 暂不 / 稍后 / 无权限继续使用 | `res/values/strings.xml / main_not_now, main_later, main_continue_without_permission` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环重跳。拒绝或从系统设置返回后，rememberAccessibilityStatus 仅把状态显示为未开启（'On; Accessibility permission required'），主界面保持可用并提供 'Continue without permission'；唯一再提示来自后台看门狗通知（ProtectionWatchdogReceiver，仅在用户曾开启保护且服务被系统清除时发出），通知可忽略、不遮挡界面、不自动反复拉起
- **遮罩叠层 / 高仿系统设置页**：无。无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；应用内的 curtain 遮挡层仅作用于 Instagram/YouTube 受保护页面（业务功能），不覆盖系统设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未使用 ACTION_APPLICATION_DETAILS_SETTINGS、未引导在应用详情右上角菜单开启“允许受限设置”，也未使用 Session 安装器绕过
- **获权后即时行为与防撤权机制**：无。PERFORM_GLOBAL_ACTION 用于受保护页面内的规则化 Back/Home 跳转与退出内容浏览，未监听设置页阻止撤权；文案明确告知用户可随时在系统无障碍设置关闭保护
- **良性降级 / 替代方案**：有：'Continue without permission' / 'You can continue without granting access; protection will remain off.'；可仅使用通知与提醒模式（Notifications are optional，无障碍为保护所必需但非强制）；小米机型额外提供 Autostart 与电池优化豁免的自助说明

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Activity 启动 Intent action == android.settings.ACCESSIBILITY_SETTINGS（且 extra :settings:fragment_args_key 指向 com.resolvecommunity.awaydoomscrollin.AntiScrollService）瞬间，或冷启动后首次出现 Compose AlertDialog（AccessibilityConsentDialog，按钮 'Agree and open settings'）时拉起 UTG
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。全部引导文案为 strings.xml 明文并由 Compose 渲染，UTG 可直接提取；应用无 WebView、无远端下发引导页、无加壳，运行期与静态一致。注意：应用在 Instagram/YouTube 上会挂载 curtain 遮挡层并执行 Back/tap/scroll，UTG 若在这些第三方包内采样需与设置引导流程区分，避免误判为遮挡诱导。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（第 5 步权限说明）** | MainActivity 内的 OnboardingStepFivePermissions，含 'Step 5 / 5' 与 'Turn on protection'、'Continue without permission' 按钮 | 此处决定应用是否以长文充分披露采集范围与本地处理承诺，是区分良性知情同意与诱导恐吓的关键页 | 存在可点击的 Continue without permission 跳过按钮；正文包含 only on your device / never sent to a server 等披露语句；无全屏遮罩或不可关闭对话框 |
| **跳转前知情同意弹窗页** | Compose AlertDialog，按钮文本 'Agree and open settings' 与 'Not now'/'Later' | 验证是否为可取消的原生对话框而非不可关闭的强制弹层，直接决定是否存在 COERCE_NO_SKIP_NON_CANCELABLE | 对话框存在取消/稍后按钮；对话框为系统/Compose 原生 AlertDialog 样式而非自绘高仿设置页；无倒计时强制按钮 |
| **跳转后系统无障碍服务列表项** | Settings 无障碍页，条目 'AwayDoomscrollin''，描述为 accessibility_service_description 长文 | 核对系统列表中显示的服务名与描述是否与应用身份一致、是否隐藏真实用途（身份一致性关键） | 条目名称与应用名一致；描述完整披露数据用途与本地处理；无空白名称或同形字混淆 |
| **后台看门狗通知页** | 通知栏 'Protection is disabled…' / 'Xiaomi stopped protection…'，含跳设置动作按钮 | 判定拒权/被清后台后是否形成骚扰式重拉，以及是否诱导关闭电池优化 | 通知是否可划掉；是否短时间内重复弹出；按钮文案是否恐吓式（streak reset） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.resolvecommunity.awaydoomscrollin.lc#F`
- `com.resolvecommunity.awaydoomscrollin.lc#u`
- `com.resolvecommunity.awaydoomscrollin.lc.AccessibilityConsentDialog`
- `com.resolvecommunity.awaydoomscrollin.lc.OnboardingStepFivePermissions`
- `com.resolvecommunity.awaydoomscrollin.m7#l`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（已核对 16 次调用，静态可见性完整）

- **入口与流程是纯 Compose 原生引导，无 WebView、无本地 HTML、无悬浮引导遮罩、无高仿设置页。** 冷启动由 `MainActivity` 承载的 Compose 引导流（`OnboardingScreen`，含 5 步，字符串 `Step %1$s / 5 ·`），无障碍开关仅在用户点 “Turn on protection” 后才跳转。
- **跳转点单一且标准**：[lc#F](<resource-unit:#1.dex1 code:com.resolvecommunity.awaydoomscrollin.lc#F>) 构造 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 并带 `:settings:fragment_args_key` 直达 `AntiScrollService` 条目，异常时降级到 `android.settings.SETTINGS`；无 `ACTION_APPLICATION_DETAILS_SETTINGS`、无“受限设置（13+）”教学、无 Session 安装器绕过。
- **电池优化豁免先于无障碍**：`OnboardingStepFivePermissions` → [m7#l](<resource-unit:#1.dex1 code:com.resolvecommunity.awaydoomscrollin.m7#l>) 先发 `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`（本包），失败降级 `IGNORE_BATTERY_OPTIMIZATION_SETTINGS` 列表页；随后才进入 `lc.u` → 写入 `accessibility_disclosure_version=1` → `lc.F` 跳无障碍页。
- **说明充分、可拒绝**：跳转前有 Compose `AlertDialog`（`AccessibilityConsentDialog`，按钮 “Agree and open settings” / “Not now”“Later”）；主页/引导页明确 “Continue without permission”“You can continue without granting access; protection will remain off.”，属良性显式降级。
- **身份诚实**：`android:isAccessibilityTool="false"`（未伪造工具标记），`packageNames` 仅限 Instagram/TikTok/YouTube 四包，事件类型与手势能力与说明一致；`android:description` 与代码行为吻合（本地处理、不落盘文本）。
- **唯一“主动重拉”来自后台看门狗**：[ProtectionWatchdogReceiver#onReceive](<resource-unit:#1.dex1 code:com.resolvecommunity.awaydoomscrollin.ProtectionWatchdogReceiver#onReceive>) 在检测到“服务被系统杀掉但开关仍显示开”时发通知（含跳无障碍页按钮，小米机型额外给 Autostart 指引），非阻塞式循环，非 onResume 死循环。
- 结论：**未发现诱导/伪装/强制类无障碍权限诱导风险**，未登记风险；`PERFORM_GLOBAL_ACTION` 用于受保护页面的规则化返回（业务功能），非撤权阻断。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX（classes.dex）与全部资源可完整静态还原：无障碍服务类、Compose 引导流、AlertDialog、跳转 Intent 与全部 strings.xml 文案均可见；无加壳、无 AES 密文载荷、无远端 HTML、无 assets 内嵌引导页（assets 仅含 baseline.prof 等）",
  "summary_one_liner": "冷启动 5 步 Compose 原生引导 → 可选电池豁免 → 原生 AlertDialog 知情同意 → 标准 ACCESSIBILITY_SETTINGS Intent 直达自身服务条目，全程可跳过、可拒绝，获权后仅做受限四包内的规则化 Back/tap/curtain 保护",
  "disguise_identity": {
    "app_display_name": "AwayDoomscrollin'",
    "claimed_brand_or_persona": "AwayDoomscrollin'（F-Droid 开源防沉迷/打破刷屏循环工具，开发者 Resolve Community）",
    "a11y_service_label": "AwayDoomscrollin'（service 无独立 android:label，系统列表继承应用名；描述取 @string/accessibility_service_description）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未使用空白/换行挤出警告、同形字、多 activity-alias 伪装；android:isAccessibilityTool 显式声明为 false，未伪造系统工具身份；仅单一 launcher Activity 与单一无障碍 Service"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "MainActivity（Compose，Theme.AwaySplashScreen）→ OnboardingScreen 第 1~4 步",
      "trigger_event": "onCreate / LAUNCHER 启动且引导未完成（rememberSaveable 步进状态，显示 'Step %1$s / 5 ·'）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Step %1$s / 5 ·",
      "shown_text_zh": "第 X 步 / 共 5 步",
      "user_action_requested": "阅读介绍并下一步；页面为可滚动引导，可随时离开（无强制阻断）",
      "code_anchor": "com.resolvecommunity.awaydoomscrollin.lc.OnboardingScreen / OnboardingStepOne~FourAppsAndPrefs / strings.xml main_step_x_5"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "OnboardingStepFivePermissions（权限说明步，含 PermissionMatrixCard）",
      "trigger_event": "引导进入第 5 步；rememberAccessibilityStatus 读取保护服务状态决定展示 'Access enabled' 或权限待开启",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "AwayDoomscrollin' needs Accessibility access to recognize the feeds and short videos you choose to protect in Instagram, TikTok and YouTube. … This screen information is processed only on your device and is never sent to a server. … You can continue without granting access; protection will remain off.",
      "shown_text_zh": "应用需要无障碍权限来识别你在 Instagram、TikTok、YouTube 中选择保护的动态与短视频；屏幕信息仅在本机处理、绝不发送到服务器；你可以在不授权的情况下继续使用，保护将保持关闭。",
      "user_action_requested": "点击 'Turn on protection' 继续；页面同时提供 'Continue without permission' 跳过路径",
      "code_anchor": "com.resolvecommunity.awaydoomscrollin.lc.OnboardingStepFivePermissions / strings.xml main_awaydoomscrollin_needs_accessibility_access_to_r, main_turn_on_protection, main_continue_without_permission"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统电池优化豁免页（REQUEST_IGNORE_BATTERY_OPTIMIZATIONS，本包 URI），失败回退 IGNORE_BATTERY_OPTIMIZATION_SETTINGS 列表页",
      "trigger_event": "OnboardingStepFivePermissions 中点击后经 m7.l 分支 0：若尚未允许后台运行则 startActivity(REQUEST_IGNORE_BATTERY_OPTIMIZATIONS)；若已允许则直接 lc.H(context)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Allow running in the background / main_battery_allowed=Allowed",
      "shown_text_zh": "允许在后台运行；已允许。属电池优化豁免，不是“受限设置（13+）”教学",
      "user_action_requested": "在系统页选择“允许”；可返回，不阻断后续引导",
      "code_anchor": "com.resolvecommunity.awaydoomscrollin.m7#l / com.resolvecommunity.awaydoomscrollin.lc#H / strings.xml main_battery_allow"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "AccessibilityConsentDialog（Compose material3 AlertDialog）",
      "trigger_event": "点击开启保护后，若 prefs 中 accessibility_disclosure_version < 1 则先弹知情同意对话框（h0.l default 分支：<1 置 showDialog=true，否则直接 lc.F 跳设置）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Agree and open settings / Not now / Later",
      "shown_text_zh": "同意并打开设置 / 暂不 / 稍后",
      "user_action_requested": "选择“同意并打开设置”才继续跳系统无障碍页；存在明确的取消/稍后按钮，可取消",
      "code_anchor": "com.resolvecommunity.awaydoomscrollin.lc.AccessibilityConsentDialog / com.resolvecommunity.awaydoomscrollin.h0#l / strings.xml main_agree_and_open_settings, main_not_now, main_later"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置：设置 > 无障碍 > 已安装/已下载的服务 > AwayDoomscrollin'（Intent android.settings.ACCESSIBILITY_SETTINGS + :settings:fragment_args_key=ComponentName(AntiScrollService)）",
      "trigger_event": "lc.u(context)：commit 写入 accessibility_disclosure_version=1 成功后调用 lc.F(context)；F 先 Toast 展示按厂商定制的设置路径，再 startActivity 无障碍设置",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Settings > Accessibility > Downloaded apps (or Installed services) > AwayDoomscrollin'（另含华为/三星/小米/OPPO/vivo 变体文案 main_settings_additional_settings_accessibility_downl、main_settings_shortcuts_accessibility_accessibility_d 等）",
      "shown_text_zh": "设置 > 无障碍 > 已下载的应用（或已安装的服务）> AwayDoomscrollin'；按手机品牌给出不同进入路径提示（Toast）",
      "user_action_requested": "在系统无障碍列表中手动找到并开启本应用服务；无自动勾选、无脚本代点",
      "code_anchor": "com.resolvecommunity.awaydoomscrollin.lc#F / com.resolvecommunity.awaydoomscrollin.lc#u / strings.xml main_settings_accessibility_downloaded_apps_or_instal"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "MainActivity 主界面 / AntiScrollService 运行；主界面卡片显示 'Access enabled'",
      "trigger_event": "返回应用后 rememberAccessibilityStatus 读取服务状态（sc.d 表示已连接）；服务 onAccessibilityEvent 仅在 com.instagram.android / com.zhiliaoapp.musically / com.ss.android.ugc.trill / com.google.android.youtube 内按规则执行 curtain/Back/tap/scroll",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Access enabled / Accessibility is required for protection. Notifications are optional. / You can turn protection off at any time, in the app or in Android's accessibility settings.",
      "shown_text_zh": "已启用 / 保护需要无障碍权限，通知是可选的 / 你可随时在应用内或系统无障碍设置中关闭保护",
      "user_action_requested": "无进一步强制动作；用户可随时在应用内或系统设置关闭",
      "code_anchor": "com.resolvecommunity.awaydoomscrollin.lc#rememberAccessibilityStatus / com.resolvecommunity.awaydoomscrollin.AntiScrollService#onAccessibilityEvent / strings.xml main_access_enabled, main_you_can_turn_protection_off_at"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "系统通知栏（ProtectionWatchdogReceiver 触发）",
      "trigger_event": "看门狗定时/重启发：若 service_running_mark=true 且 watchdog_stop_suspected=true（服务被系统清除）→ 发通知，按钮携带 ACCESSIBILITY_SETTINGS Intent；非小米机型额外给出 Autostart 说明按钮",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Protection is disabled. If not re-enabled, your daily streak will reset in 24 hours. / Xiaomi stopped protection in the background. Turn on Autostart so it comes back by itself, then turn protection on again.",
      "shown_text_zh": "保护已停用；若未重新开启，你的每日连续记录将在 24 小时后重置 / 小米在后台停止了保护，请开启自启动后重新开启保护",
      "user_action_requested": "可选点击通知跳系统无障碍页重新开启；不点击不影响使用，无死循环重跳、无遮挡",
      "code_anchor": "com.resolvecommunity.awaydoomscrollin.ProtectionWatchdogReceiver#onReceive / strings.xml notif_protection_stopped_text, notif_xiaomi_stopped_text"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表描述：res/xml/accessibility_service_config.xml android:description=@string/accessibility_service_description（完整披露采集范围、本地处理与不落盘承诺）",
    "OnboardingStepFivePermissions 引导页正文：strings.xml main_awaydoomscrollin_needs_accessibility_access_to_r（长文披露）",
    "Compose AlertDialog（AccessibilityConsentDialog）：按钮 Agree and open settings / Not now / Later",
    "主页/仪表盘卡片：main_turn_on_accessibility_so_awaydoomscrollin_can、main_accessibility_is_required_for_protection_notific、main_on_accessibility_permission_required、main_protection_stuck_hint",
    "跳转前厂商定制 Toast：lc.F 按 Build.MANUFACTURER 选择 main_settings_accessibility_* 系列设置路径文案",
    "电池豁免卡片：main_battery_allow、main_xiaomi_autostart_note（小米专属自启动说明）",
    "系统通知栏：notif_protection_stopped_text / notif_xiaomi_stopped_text（含跳设置按钮）",
    "无 WebView/HTML/悬浮窗承载任何引导文案（assets 目录仅 baseline.prof/dexopt，无引导页面）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "AwayDoomscrollin' examines accessibility text and labels, view identifiers, window changes, taps and scroll events on your device to recognize protected feeds and short videos in Instagram, TikTok and YouTube. It can show curtains in Instagram and YouTube and perform specific, rule-based Back, tap and scroll actions on protected screens. Screen information is processed only on your device and never sent to a server.",
      "text_zh": "本应用检查设备上的无障碍文本与标签、视图标识、窗口变化、点击与滚动事件，以识别 Instagram、TikTok 和 YouTube 中被保护的动态与短视频；可在 Instagram 和 YouTube 显示遮挡层，并在受保护页面上执行特定的、基于规则的返回、点击与滚动操作。屏幕信息仅在本机处理，绝不发送到服务器。",
      "source_location": "res/values/strings.xml / accessibility_service_description（经 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "You can continue without granting access; protection will remain off.",
      "text_zh": "你可以在不授予权限的情况下继续使用；保护将保持关闭。",
      "source_location": "res/values/strings.xml / main_awaydoomscrollin_needs_accessibility_access_to_r",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This screen information is processed only on your device and is never sent to a server. Text, labels and view identifiers are not saved; if you turn on the troubleshooting log in About, a short record of what protection did stays on your device for 24 hours, and sharing it is up to you.",
      "text_zh": "这些屏幕信息仅在本机处理，绝不发送到服务器；文本、标签与视图标识不会被保存；若你在“关于”中开启排障日志，保护行为的简短记录仅在本机保留 24 小时，是否分享由你决定。",
      "source_location": "res/values/strings.xml / main_awaydoomscrollin_needs_accessibility_access_to_r",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Settings > Accessibility > Downloaded apps (or Installed services) > AwayDoomscrollin'",
      "text_zh": "设置 > 无障碍 > 已下载的应用（或已安装的服务）> AwayDoomscrollin'",
      "source_location": "res/values/strings.xml / main_settings_accessibility_downloaded_apps_or_instal（另有华为/三星/小米/OPPO/vivo 变体）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "You can turn protection off at any time, in the app or in Android's accessibility settings.",
      "text_zh": "你可随时在应用内或 Android 无障碍设置中关闭保护。",
      "source_location": "res/values/strings.xml / main_you_can_turn_protection_off_at",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn on Accessibility so AwayDoomscrollin' can protect you automatically.",
      "text_zh": "开启无障碍，让 AwayDoomscrollin' 自动保护你。",
      "source_location": "res/values/strings.xml / main_turn_on_accessibility_so_awaydoomscrollin_can",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Protection is disabled. If not re-enabled, your daily streak will reset in 24 hours.",
      "text_zh": "保护已停用；若未重新开启，你的每日连续记录将在 24 小时后重置。",
      "source_location": "res/values/strings.xml / notif_protection_stopped_text（ProtectionWatchdogReceiver 通知）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Android stopped protection in the background, but its switch still shows on. In Accessibility, turn AwayDoomscrollin' off and on again.",
      "text_zh": "Android 在后台停止了保护，但开关仍显示为开启。请在无障碍中把 AwayDoomscrollin' 关闭再重新开启。",
      "source_location": "res/values/strings.xml / main_protection_stuck_hint",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Agree and open settings",
      "text_zh": "同意并打开设置",
      "source_location": "res/values/strings.xml / main_agree_and_open_settings（AccessibilityConsentDialog 确认按钮）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Not now / Later / Continue without permission",
      "text_zh": "暂不 / 稍后 / 无权限继续使用",
      "source_location": "res/values/strings.xml / main_not_now, main_later, main_continue_without_permission",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环重跳。拒绝或从系统设置返回后，rememberAccessibilityStatus 仅把状态显示为未开启（'On; Accessibility permission required'），主界面保持可用并提供 'Continue without permission'；唯一再提示来自后台看门狗通知（ProtectionWatchdogReceiver，仅在用户曾开启保护且服务被系统清除时发出），通知可忽略、不遮挡界面、不自动反复拉起",
    "overlay_or_fake_settings": "无。无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；应用内的 curtain 遮挡层仅作用于 Instagram/YouTube 受保护页面（业务功能），不覆盖系统设置页",
    "restricted_settings_13plus_coaching": "无。未使用 ACTION_APPLICATION_DETAILS_SETTINGS、未引导在应用详情右上角菜单开启“允许受限设置”，也未使用 Session 安装器绕过",
    "post_grant_anti_removal": "无。PERFORM_GLOBAL_ACTION 用于受保护页面内的规则化 Back/Home 跳转与退出内容浏览，未监听设置页阻止撤权；文案明确告知用户可随时在系统无障碍设置关闭保护",
    "benign_graceful_degradation": "有：'Continue without permission' / 'You can continue without granting access; protection will remain off.'；可仅使用通知与提醒模式（Notifications are optional，无障碍为保护所必需但非强制）；小米机型额外提供 Autostart 与电池优化豁免的自助说明"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Activity 启动 Intent action == android.settings.ACCESSIBILITY_SETTINGS（且 extra :settings:fragment_args_key 指向 com.resolvecommunity.awaydoomscrollin.AntiScrollService）瞬间，或冷启动后首次出现 Compose AlertDialog（AccessibilityConsentDialog，按钮 'Agree and open settings'）时拉起 UTG",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（第 5 步权限说明）",
        "page_identifier": "MainActivity 内的 OnboardingStepFivePermissions，含 'Step 5 / 5' 与 'Turn on protection'、'Continue without permission' 按钮",
        "why_most_useful": "此处决定应用是否以长文充分披露采集范围与本地处理承诺，是区分良性知情同意与诱导恐吓的关键页",
        "observable_utg_signals": ["存在可点击的 Continue without permission 跳过按钮", "正文包含 only on your device / never sent to a server 等披露语句", "无全屏遮罩或不可关闭对话框"]
      },
      {
        "page_role": "跳转前知情同意弹窗页",
        "page_identifier": "Compose AlertDialog，按钮文本 'Agree and open settings' 与 'Not now'/'Later'",
        "why_most_useful": "验证是否为可取消的原生对话框而非不可关闭的强制弹层，直接决定是否存在 COERCE_NO_SKIP_NON_CANCELABLE",
        "observable_utg_signals": ["对话框存在取消/稍后按钮", "对话框为系统/Compose 原生 AlertDialog 样式而非自绘高仿设置页", "无倒计时强制按钮"]
      },
      {
        "page_role": "跳转后系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页，条目 'AwayDoomscrollin''，描述为 accessibility_service_description 长文",
        "why_most_useful": "核对系统列表中显示的服务名与描述是否与应用身份一致、是否隐藏真实用途（身份一致性关键）",
        "observable_utg_signals": ["条目名称与应用名一致", "描述完整披露数据用途与本地处理", "无空白名称或同形字混淆"]
      },
      {
        "page_role": "后台看门狗通知页",
        "page_identifier": "通知栏 'Protection is disabled…' / 'Xiaomi stopped protection…'，含跳设置动作按钮",
        "why_most_useful": "判定拒权/被清后台后是否形成骚扰式重拉，以及是否诱导关闭电池优化",
        "observable_utg_signals": ["通知是否可划掉", "是否短时间内重复弹出", "按钮文案是否恐吓式（streak reset）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。全部引导文案为 strings.xml 明文并由 Compose 渲染，UTG 可直接提取；应用无 WebView、无远端下发引导页、无加壳，运行期与静态一致。注意：应用在 Instagram/YouTube 上会挂载 curtain 遮挡层并执行 Back/tap/scroll，UTG 若在这些第三方包内采样需与设置引导流程区分，避免误判为遮挡诱导。"
  },
  "behavior_pattern_tags": [
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.resolvecommunity.awaydoomscrollin.lc#F",
    "com.resolvecommunity.awaydoomscrollin.lc#u",
    "com.resolvecommunity.awaydoomscrollin.lc.AccessibilityConsentDialog",
    "com.resolvecommunity.awaydoomscrollin.lc.OnboardingStepFivePermissions",
    "com.resolvecommunity.awaydoomscrollin.m7#l",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
