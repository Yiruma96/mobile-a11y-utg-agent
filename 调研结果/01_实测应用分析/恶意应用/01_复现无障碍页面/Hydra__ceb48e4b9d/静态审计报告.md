# MB_056__ceb48e4b9d｜Hydra — Commerzbank Sicherheitszertifikat

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：146.3s

## 1. 一句话核心结论

- **核心申请方式**：DexProtector 加壳的 Hydra 家族银行木马，伪装成德国商业银行安全证书，用『安全更新+关闭 Play Protect/Scan device』恐吓话术加 4 步 Settings→Accessibility→Installed Services 分步教学，配合全屏悬浮窗引导，把用户骗去开启一个在系统列表中无名称无说明的 InjAccessibilityService。
- **静态可见性说明**：DEX 主体被 DexProtector 整体加密：classes.dex 仅含 xyz.magicph.dexpro.ProxyApplication 与 adrt.ADRTLogSender 壳存根，真实业务代码在 dp/a.a（约 987KB 高熵密文，文件头 2d7c73c1… 非 DEX 魔数），assets/classes.dex.dat 仅 37 字节水印 'Secured by dexprotector of magicph :)'。因此跳转 ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 的具体调用点、计时器/onResume 重跳逻辑、悬浮层压栈时机均无法静态还原。可静态确认的部分为：Manifest 组件声明、无障碍配置 res/o5.xml、引导布局 res/02.xml、dD.xml、8C.xml、tR.xml、以及 resources.arsc 中完整的 4 步教学与反系统防护文案（含多语言）。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ceb48e4b9d82b2ab7b486393048cdc78c6dfaf88799521e63677b06975f707cd` |
| 包名 / 年份 | `com.grand.dogla` / 2024 |
| 家族 / 品类 | **Hydra**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Commerzbank Sicherheitszertifikat |
| 引导页宣称品牌/身份 | Commerzbank（德国商业银行）官方安全证书/安全更新组件 |
| 系统无障碍列表服务名 | 未声明 android:label，也未声明 android:description；系统无障碍列表回退显示应用名 'Commerzbank Sicherheitszertifikat'（res/o5.xml 仅有 settingsActivity、事件类型与 canPerformGestures 等能力项） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍配置刻意不写 label/description，使系统列表项完全借用银行名称，隐藏'注入/自动化'用途；2) 同名 activity-alias 与真实 Activity 重名（com.grand.snail.MainActivity 同时作为 activity 和 activity-alias），另有 enabled=false 的 MainActivity2 别名使用独立 label(@7F070001) 与 icon(@7F020003)，可按需切换桌面身份；3) 两个入口 Activity 均 excludeFromRecents，进入后不在最近任务留痕；4) 包名 com.grand.dogla 与内部代码包 com.grand.snail 不一致，dexpro-build.properties 残留 build.package_name=com.grand.snail；5) 资源/布局全部重命名为无意义短名（02.xml、8C.xml、o5.xml、dD.xml 等）并直接承载钓鱼文案；6) DexProtector 整体加密 DEX，防静态还原。 |
| 无障碍服务类名 | `com.grand.snail.bot.components.injects.system.InjAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.grand.snail.MainActivity（LAUNCHER + 同名 activity-alias，excludeFromRecents=true） | 用户点击桌面图标（图标名 Commerzbank Sicherheitszertifikat）→ onCreate/onResume | 原生Activity | **原文**：无（该 Activity 自身文案由加密载荷渲染，静态不可读）<br>**译注**：启动后未见静态可见文案，界面内容由 dp/a.a 内解密逻辑决定 | 无可静态确认的取消入口；两个入口 Activity 均不保留最近任务卡片，用户难以返回退出 | `AndroidManifest: activity/activity-alias com.grand.snail.MainActivity（实现位于加密 dp/a.a）` |
| 2 | 引导说明页 | com.grand.snail.bot.PermissionsActivity | 启动后由加密逻辑拉起（PermissionsActivity 为独立非导出 Activity，excludeFromRecents=true） | 原生Activity（布局含 ScrollView+TextView+Button，资源 res/02.xml、res/dD.xml） | **原文**：In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below:<br>**译注**：为了让最新版本的 %s 正常工作，您需要开启无障碍功能。请按以下步骤操作： | 按页面引导继续下一步（%s 处由代码填入伪造的应用/服务名），未提供取消或跳过路径 | `resources.arsc: instruction_step_* / tv_instruction_step_3 / tv_instruction_step_4；布局 res/02.xml、res/dD.xml；组件 com.grand.snail.bot.PermissionsActivity` |
| 3 | 引导说明页（分步教学，4 步 + 机型变体） | 同一原生引导页内的分步文案区 + 'Go to settings' 按钮（bt_goto_settings / ic_settings_main） | 用户点击 'Go to settings' 按钮（instruction_button_activate）或滚动查看步骤 | 原生Activity | **原文**：Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Step 4 - Turn %s on / Go to settings<br>**译注**：第 1 步 - 打开“设置”；第 2 步 - 打开“无障碍”；第 3 步 - 打开“已安装的服务”；第 4 步 - 打开 %s 的开关；前往设置 | 严格按 4 步手动操作，最终在无障碍服务列表里打开目标服务开关 | `resources.arsc: instruction_step_1/2/3/4、samsung_instruction_step_2、xiaomi_instruction_step_1、bt_goto_settings` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载/已安装的服务（Settings.ACTION_ACCESSIBILITY_SETTINGS） | 'Go to settings' 按钮点击后由加密代码 startActivity 跳转（具体调用点不可静态还原） | 系统无障碍页 | **原文**：Please enable Portal service under Accessibility settings / Check in 'Downloaded Services' list: %s<br>**译注**：请在无障碍设置中启用 Portal 服务 / 请在“已下载的服务”列表中查找：%s | 在系统列表中定位并打开以银行名显示的无障碍服务开关（无取消/跳过提示） | `resources.arsc: 字符串 'Please enable Portal service under Accessibility settings'、check_in_services_message；组件 com.grand.snail.bot.components.injects.system.InjAccessibilityService` |
| 5 | 跳受限设置 / 悬浮窗授权 | 系统应用详情页（ACTION_APPLICATION_DETAILS_SETTINGS）或系统'显示在其他应用上层'授权页 | 引导流程中按需跳转；由加密代码决定触发顺序（SYSTEM_ALERT_WINDOW 权限已声明） | 系统无障碍页 / 系统设置页 | **原文**：Step 2 - Allow to display pop-up windows from background mode / Step 2 - Give permission to "Appear on top" / Allow pop-up windows for the correct application work:<br>**译注**：第 2 步 - 允许后台模式下显示弹窗 / 第 2 步 - 授予“显示在其他应用上层”权限 / 请允许弹窗以便应用正常工作： | 在系统设置中打开“显示在其他应用上层”开关；未提供取消路径 | `resources.arsc: 'Step 2 - Allow to display pop-up windows from background mode'、'Step 2 - Give permission to "Appear on top"'、'Allow pop-up windows for the correct application work:'` |
| 6 | 遮罩叠层指引 | com.grand.snail.bot.components.injects.system.FullscreenOverlayService（无绑定权限、无类型限制声明）+ 系统设置页之上 | 跳转设置页后由服务/定时器拉起悬浮层（时机在加密载荷内） | 悬浮窗Overlay | **原文**：Go to settings / Please enable Portal service under Accessibility settings / Check in 'Downloaded Services' list: %s<br>**译注**：前往设置 / 请在无障碍设置中启用 Portal 服务 / 请在“已下载的服务”列表中查找：%s | 在悬浮指引下继续在系统页内点击开关，用户无法区分应用界面与系统界面 | `AndroidManifest: service com.grand.snail.bot.components.injects.system.FullscreenOverlayService；resources.arsc 同上` |
| 7 | 拒权反馈循环（关闭系统防护的诱导分支） | 原生引导页 + 可能的悬浮层；Play Protect / Scan device / 电池优化设置页 | 检测到无障碍未开启，或检测到 Google Play Protect / 设备扫描功能仍启用时触发 | 原生Activity / 悬浮窗Overlay / 系统设置页 | **原文**：Google - do not disable this app / To install Security update you must disable 'Scan device' option! / Enable control over your battery usage. Press 'Activate' button in the next window / Scan device for<br>**译注**：Google - 请勿停用此应用 / 要安装安全更新，您必须关闭“扫描设备”选项！/ 请允许控制电池使用，在下一窗口点击“激活”按钮 / 扫描设备以… | 关闭 Play Protect 校验、关闭 Scan device、忽略电池优化，为后续静默安装/后台常驻铺路 | `resources.arsc: do_not_disable、enablePlayProtect_message、services_playProtect*、services_playScanningDisableBtn、enable_control_battery_usage、'To install Security update you must disable \'Scan device\' option!'` |
| 8 | 引导说明页（假更新遮罩） | 假更新进度页（布局 res/8C.xml：LinearLayout+RelativeLayout+TextView）或 WebViewActivity 远端页 | 获权前后由加密代码展示，掩盖实际后台动作 | 原生Activity / 远端WebView | **原文**：Installing updates... / It can takes a few moments<br>**译注**：正在安装更新… / 可能需要一点时间 | 等待（无按钮、无取消），用于消磨用户操作空窗期 | `布局 res/8C.xml（含 'Installing updates...'、'It can takes a few moments'）；组件 com.grand.snail.WebViewActivity + 布局 res/tR.xml（WebView）` |
| 9 | 获权后动作 | InjAccessibilityService（canRetrieveWindowContent + canPerformGestures + canRequestFilterKeyEvents）、ScreencastService、Socks5ProxyService、NLService、LockerActivity | 用户在系统页打开开关后 onServiceConnected（实现位于加密 dp/a.a，静态不可还原） | 不可静态还原 | 无 | 无需用户操作；服务在后台按远程指令执行 | `AndroidManifest: InjAccessibilityService / FullscreenOverlayService / ScreencastService / Socks5ProxyService / NLService；res/o5.xml 无障碍能力声明` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 引导说明页 com.grand.snail.bot.PermissionsActivity（原生 Activity，ScrollView+TextView 分步文案，布局 res/02.xml / res/dD.xml）
- 'Go to settings' 按钮（bt_goto_settings / ic_settings_main / instruction_button_activate）所在的原生引导页
- 系统无障碍服务列表项：InjAccessibilityService 未声明 android:label 与 android:description（res/o5.xml），列表仅显示应用名 'Commerzbank Sicherheitszertifikat'
- 系统设置页之上的全屏悬浮窗 FullscreenOverlayService（配合 SYSTEM_ALERT_WINDOW），承载 'Go to settings'、'Please enable Portal service…'、'Check in Downloaded Services list' 等指引
- Play Protect / Scan device / 电池优化分支文案（resources.arsc: do_not_disable、enablePlayProtect_message、services_playProtect*、enable_control_battery_usage）
- 假更新遮罩页布局 res/8C.xml（'Installing updates...'、'It can takes a few moments'）
- WebView 载体：com.grand.snail.WebViewActivity（独立 taskAffinity .webViewTask）+ 纯 WebView 布局 res/tR.xml，可加载远端 HTML 教学页
- NotificationListener 服务 NLService 的 android:label 直接设为 'Commerzbank Sicherheitszertifikat'，在通知使用权列表中同样冒用银行名
- 桌面图标与名称（LAUNCHER activity-alias 与 label/icon @7F070001/@7F020003 备用别名）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below: | 为了让最新版本的 %s 正常工作，您需要开启无障碍功能。请按以下步骤操作： | `resources.arsc（instruction_step 引导段首句）` | 假更新 |
| en | Step 1 - Go to “Settings” | 第 1 步 - 打开“设置” | `resources.arsc: instruction_step_1` | 受限设置分步教学 |
| en | Step 2 - Open “Accessibility” | 第 2 步 - 打开“无障碍” | `resources.arsc: instruction_step_2（另有 samsung_instruction_step_2 机型变体）` | 受限设置分步教学 |
| en | Step 3 - Open “Installed Services” | 第 3 步 - 打开“已安装的服务” | `resources.arsc: instruction_step_3 / tv_instruction_step_3` | 受限设置分步教学 |
| en | Step 4 - Turn %s on | 第 4 步 - 打开 %s 的开关 | `resources.arsc: instruction_step_4 / tv_instruction_step_4` | 受限设置分步教学 |
| en | Please enable Portal service under Accessibility settings | 请在无障碍设置中启用 Portal 服务 | `resources.arsc（无障碍引导提示）` | 受限设置分步教学 |
| en | Check in 'Downloaded Services' list: %s | 请在“已下载的服务”列表中查找：%s | `resources.arsc: check_in_services_message` | 受限设置分步教学 |
| en | To install Security update you must disable 'Scan device' option! | 要安装安全更新，您必须关闭“扫描设备”选项！ | `resources.arsc（反系统防护诱导文案）` | 教唆忽视警告 |
| en | Google - do not disable this app | Google - 请勿停用此应用 | `resources.arsc: do_not_disable` | 教唆忽视警告 |
| en | Enable control over your battery usage. Press 'Activate' button in the next window | 请允许控制电池使用，在下一窗口点击“激活”按钮 | `resources.arsc: enable_control_battery_usage` | 清理工具伪装 |
| en | Step 2 - Allow to display pop-up windows from background mode | 第 2 步 - 允许后台模式下显示弹窗 | `resources.arsc（悬浮窗授权教学）` | 受限设置分步教学 |
| en | Step 2 - Give permission to "Appear on top" | 第 2 步 - 授予“显示在其他应用上层”权限 | `resources.arsc（悬浮窗授权教学）` | 受限设置分步教学 |
| en | Allow pop-up windows for the correct application work: | 请允许弹窗，以便应用正常工作： | `resources.arsc（悬浮窗授权教学首句）` | 假更新 |
| en | Installing updates... It can takes a few moments | 正在安装更新… 可能需要一点时间 | `布局资源 res/8C.xml（两个 TextView 的 text 属性）` | 假更新 |
| en | Scan device for | 扫描设备以…（配合 'Scan device' 设置项，用于引导关闭设备扫描） | `resources.arsc（Scan device 分支文案，多语言版本如 't scannen nach'、'Scansiona dispositivo per'）` | 教唆忽视警告 |
| de | Check in der Liste 'Heruntergeladene Dienste': %s / Deinstallieren | 请在“已下载的服务”列表中查找：%s / 卸载 | `resources.arsc（德语资源，说明面向德语区用户）` | 受限设置分步教学 |
| tr | Google - bu uygulamayı devre dışı bırakmayın | Google - 请勿停用此应用 | `resources.arsc（土耳其语资源，do_not_disable 译文）` | 教唆忽视警告 |
| es | Compruebe en la lista 'Servicios descargados': %s | 请在“已下载的服务”列表中查找：%s | `resources.arsc（西班牙语资源，check_in_services_message 译文）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：拒绝/返回后的具体反应位于加密载荷 dp/a.a，静态不可还原。可确认的相关支撑：入口 MainActivity 与 PermissionsActivity 均 excludeFromRecents=true（返回即离开，无法从最近任务回到中断点，用户只能重开应用再次进入引导）；FullscreenOverlayService 与 SYSTEM_ALERT_WINDOW 权限已具备在设置页之上反复拉起引导层的条件；MainReceiver/PeriodicJobReceiver 监听 BOOT_COMPLETED、USER_PRESENT、SCREEN_ON、PACKAGE_ADDED 等广播，具备开机/解锁/装包后再次触发引导的通道。
- **遮罩叠层 / 高仿系统设置页**：存在全屏悬浮层：com.grand.snail.bot.components.injects.system.FullscreenOverlayService（Manifest 中无 BIND 权限、无类型约束），配合 'Appear on top' 授权教学文案，可在系统无障碍页上叠放半透明引导遮罩；未发现自绘高仿系统无障碍开关页的静态证据。
- **Android 13+ 受限设置（Restricted Settings）应对**：未见针对 Android 13+『允许受限设置』（应用详情右上角菜单）的专门文案；其引导路径是传统的 Settings→Accessibility→Installed Services/Downloaded Services 4 步教学，并额外教用户关闭 Play Protect 与 'Scan device' 以绕过安装校验。
- **获权后即时行为与防撤权机制**：未获静态证据：GLOBAL_ACTION_BACK/HOME 撤权拦截逻辑位于加密 dp/a.a。但 LockerActivity 已声明 HOME category（enabled=false 可动态启用）与 HelperAdmin 设备管理器（watch-login/force-lock/wipe-data 策略），具备劫持 Home 键与设备管理的持久化/对抗卸载条件。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条互补触发：(1) 冷启动后立即监测 com.grand.snail.MainActivity / com.grand.snail.bot.PermissionsActivity 进入前台并出现含 'Go to settings' 按钮的引导页时开始录制；(2) 监测到当前包名切换为系统 Settings（无障碍/应用详情/显示在其他应用上层页）而屏幕上仍存在非系统的半透明浮层或提示文字时，判定为叠层指引窗口。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：DEX 主体被 DexProtector 整体加密（dp/a.a），跳转调用点、拒权重跳的定时/onResume 逻辑、%s 占位符的实际填充值、获权后的注入动作均需运行期观测或脱壳才能确认；本报告结论基于 Manifest + 资源字符串 + 布局 XML 的结构性证据。运行期 UTG 不受静态加壳影响，仍可完整捕获页面流转。另需注意：本样本另带 Play Protect/Scan device 关闭诱导与设备管理器、通知监听、屏幕录制、SOCKS5 代理能力，无障碍只是整条攻击链的其中一环。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（4 步教学首屏）** | activity=com.grand.snail.bot.PermissionsActivity 或 com.grand.snail.MainActivity；视图含 ScrollView + 多个 TextView（Step 1/2/3/4）与 text='Go to settings' 的 Button | 这是'应用主动教用户开无障碍'的直接意图证据，且 %s 占位符被填入的真实服务名/伪造名只有运行期可见 | activity 类名与 excludeFromRecents 无最近任务卡片；Text 'Step 1 - Go to “Settings”' / 'Step 3 - Open “Installed Services”'；Button text 'Go to settings'；是否存在取消/跳过按钮（预期无） |
| **跳转前的点击点** | 'Go to settings' 按钮点击瞬间（Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS） | 把静态文案与运行期实际跳转目标绑定，补上加密载荷中无法静态还原的 startActivity 目标 | 点击后前台 activity 变为 com.android.settings/.Settings$AccessibilitySettingsActivity；跳转前是否有倒计时/不可关闭遮罩；跳转前是否弹出第二个说明层 |
| **系统无障碍服务列表项** | Settings 无障碍 → 已安装/已下载的服务列表中的 'Commerzbank Sicherheitszertifikat' 条目 | 该服务无 label/无 description，列表项完全冒用银行名称，是身份伪装与'零说明授权'的核心证据页 | 列表项文本恰为应用名而非功能名；条目下方无任何用途说明文字；条目旁的服务名是否出现 'Portal service' 等伪造名称 |
| **系统设置页之上的悬浮引导层** | 前台为 Settings 且存在非 Settings 包名的 TYPE_APPLICATION_OVERLAY 窗口（FullscreenOverlayService） | 区分'仅教学'与'在系统页上叠层诱导/误导点击'，是判定 COERCE_OVERLAY_STACK_ON_SETTINGS 的关键 | 窗口归属包名 com.grand.dogla 而前台 activity 属于 com.android.settings；浮层内文本 'Please enable Portal service under Accessibility settings'；浮层是否覆盖开关位置或添加手指指示 |
| **假更新遮罩页 / WebView 教学页** | 布局 res/8C.xml 的 'Installing updates...' 页面，或 com.grand.snail.WebViewActivity（taskAffinity .webViewTask）加载的远端 URL | 验证是否用假更新页面掩盖获权后的实际动作，以及是否从远端下发可变引导文案 | Text 'Installing updates...' / 'It can takes a few moments'；WebView 加载的 URL 域名与页面语言；页面无任何取消按钮且持续停留 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.grand.snail.bot.components.injects.system.InjAccessibilityService（Manifest 声明，实现位于加密 dp/a.a）`
- `res/o5.xml（无障碍配置：settingsActivity、canRetrieveWindowContent、canPerformGestures、canRequestFilterKeyEvents；无 label/description）`
- `resources.arsc: instruction_step_1/2/3/4、check_in_services_message、do_not_disable、enable_control_battery_usage、services_playProtect*`
- `com.grand.snail.bot.PermissionsActivity / com.grand.snail.WebViewActivity / com.grand.snail.bot.components.injects.system.FullscreenOverlayService`
- `res/8C.xml（'Installing updates...' 假更新遮罩）、res/tR.xml（WebView 载体）`
- `xyz.magicph.dexpro.ProxyApplication + dp/a.a（DexProtector 加密载荷，约 987KB）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

- **静态可见性：整体加壳。** `classes.dex` 只包含 3 个类，都是壳的存根：[ProxyApplication](<resource-unit:#1.dex1 code:xyz.magicph.dexpro.ProxyApplication>) 和 `adrt.ADRTLogSender`；真正的业务代码（约 987 KB）在 [dp/a.a](<resource-unit:#1 file:dp/a.a>) 中，由 DexProtector 加密（`dexpro-build.properties` 明确写着 "Secured by dexprotector of magicph"，并带有作者水印 `Modded by 👽🅰︎🅝︎🅘︎🅺︎555`）。因此，**“谁在什么条件下调用 startActivity 跳转到系统设置”这一具体代码无法静态还原**。
- **但引导链的外层结构仍然完整可见**：Manifest 组件、无障碍配置 XML、布局 XML 和资源字符串池共同构成了完整的 4 步教学文案；并且同一文案有 en/de/tr/es/it/pt 多种语言，这说明它是一套面向多国的批量钓鱼引导框架，而不是某个国家的本地化应用。
- **身份伪装明确**：包名 `com.grand.dogla`，桌面显示名 `Commerzbank Sicherheitszertifikat`（德国商业银行"安全证书"），而真实包名前缀是 `com.grand.snail`（Hydra/Hook 家族）。Manifest 中还有同名 `activity-alias`，以及一个 `enabled=false`、使用另一套 label/icon（`@7F070001`/`@7F020003`）的 `MainActivity2` 别名，并且两个入口 Activity 都设置了 `excludeFromRecents="true"`。
- **无障碍服务在系统列表中"无名"**：`InjAccessibilityService` 的配置 [res/o5.xml](<resource-unit:#1 file:res/o5.xml>) 只声明了 `settingsActivity`、事件类型、`canRetrieveWindowContent`、`canPerformGestures`、`canRequestFilterKeyEvents`，**既没有 `android:label`，也没有 `android:description`**，因此系统无障碍列表里只能显示应用名"Commerzbank Sicherheitszertifikat"，不展示任何"注入/自动化"用途说明。
- **引导话术的三种套路同时使用**：(1) 冒充安全更新/证书（`To install Security update you must disable 'Scan device' option!`、布局 [res/8C.xml](<resource-unit:#1 file:res/8C.xml>) 中的 `Installing updates...`）；(2) 教用户关闭系统防护（`Google - do not disable this app`、`Scan device for ...`、Play Protect 相关 key `services_playProtect*`）；(3) 分步教学开启无障碍（`Step 1 - Go to “Settings”` → `Step 2 - Open “Accessibility”` → `Step 3 - Open “Installed Services”` → `Step 4 - Turn %s on`，以及 `Please enable Portal service under Accessibility settings`、`Check in 'Downloaded Services' list: %s`）。
- **存在悬浮窗叠层与二次诱导载体**：`FullscreenOverlayService`（无权限声明限制、配合 `SYSTEM_ALERT_WINDOW`）与文案 `Step 2 - Allow to display pop-up windows from background mode`、`Step 2 - Give permission to "Appear on top"`、`Allow pop-up windows for the correct application work:` 相呼应，说明引导不止发生在应用内页面，还会以悬浮层压在系统设置页之上；另有 [res/tR.xml](<resource-unit:#1 file:res/tR.xml>)（纯 `WebView` 布局）和 `com.grand.snail.WebViewActivity`（独立 taskAffinity），远端 HTML 教学页是合理的载体。
- **获权后行为（注入、点击、屏幕录制、SOCKS5、短信监听）** 全部在加密载荷内，本次只能确认能力声明，无法确认具体实现。

> 说明：受本轮 14 次工具调用上限约束，未再写入风险台账（`record_risk`）；本回复即为该样本无障碍诱导链的完整证据输出。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "DEX 主体被 DexProtector 整体加密：classes.dex 仅含 xyz.magicph.dexpro.ProxyApplication 与 adrt.ADRTLogSender 壳存根，真实业务代码在 dp/a.a（约 987KB 高熵密文，文件头 2d7c73c1… 非 DEX 魔数），assets/classes.dex.dat 仅 37 字节水印 'Secured by dexprotector of magicph :)'。因此跳转 ACTION_ACCESSIBILITY_SETTINGS/ACTION_APPLICATION_DETAILS_SETTINGS 的具体调用点、计时器/onResume 重跳逻辑、悬浮层压栈时机均无法静态还原。可静态确认的部分为：Manifest 组件声明、无障碍配置 res/o5.xml、引导布局 res/02.xml、dD.xml、8C.xml、tR.xml、以及 resources.arsc 中完整的 4 步教学与反系统防护文案（含多语言）。",
  "summary_one_liner": "DexProtector 加壳的 Hydra 家族银行木马，伪装成德国商业银行安全证书，用『安全更新+关闭 Play Protect/Scan device』恐吓话术加 4 步 Settings→Accessibility→Installed Services 分步教学，配合全屏悬浮窗引导，把用户骗去开启一个在系统列表中无名称无说明的 InjAccessibilityService。",
  "disguise_identity": {
    "app_display_name": "Commerzbank Sicherheitszertifikat",
    "claimed_brand_or_persona": "Commerzbank（德国商业银行）官方安全证书/安全更新组件",
    "a11y_service_label": "未声明 android:label，也未声明 android:description；系统无障碍列表回退显示应用名 'Commerzbank Sicherheitszertifikat'（res/o5.xml 仅有 settingsActivity、事件类型与 canPerformGestures 等能力项）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍配置刻意不写 label/description，使系统列表项完全借用银行名称，隐藏'注入/自动化'用途；2) 同名 activity-alias 与真实 Activity 重名（com.grand.snail.MainActivity 同时作为 activity 和 activity-alias），另有 enabled=false 的 MainActivity2 别名使用独立 label(@7F070001) 与 icon(@7F020003)，可按需切换桌面身份；3) 两个入口 Activity 均 excludeFromRecents，进入后不在最近任务留痕；4) 包名 com.grand.dogla 与内部代码包 com.grand.snail 不一致，dexpro-build.properties 残留 build.package_name=com.grand.snail；5) 资源/布局全部重命名为无意义短名（02.xml、8C.xml、o5.xml、dD.xml 等）并直接承载钓鱼文案；6) DexProtector 整体加密 DEX，防静态还原。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.grand.snail.MainActivity（LAUNCHER + 同名 activity-alias，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标（图标名 Commerzbank Sicherheitszertifikat）→ onCreate/onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该 Activity 自身文案由加密载荷渲染，静态不可读）",
      "shown_text_zh": "启动后未见静态可见文案，界面内容由 dp/a.a 内解密逻辑决定",
      "user_action_requested": "无可静态确认的取消入口；两个入口 Activity 均不保留最近任务卡片，用户难以返回退出",
      "code_anchor": "AndroidManifest: activity/activity-alias com.grand.snail.MainActivity（实现位于加密 dp/a.a）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.grand.snail.bot.PermissionsActivity",
      "trigger_event": "启动后由加密逻辑拉起（PermissionsActivity 为独立非导出 Activity，excludeFromRecents=true）",
      "ui_carrier": "原生Activity（布局含 ScrollView+TextView+Button，资源 res/02.xml、res/dD.xml）",
      "shown_text_verbatim": "In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below:",
      "shown_text_zh": "为了让最新版本的 %s 正常工作，您需要开启无障碍功能。请按以下步骤操作：",
      "user_action_requested": "按页面引导继续下一步（%s 处由代码填入伪造的应用/服务名），未提供取消或跳过路径",
      "code_anchor": "resources.arsc: instruction_step_* / tv_instruction_step_3 / tv_instruction_step_4；布局 res/02.xml、res/dD.xml；组件 com.grand.snail.bot.PermissionsActivity"
    },
    {
      "step": 3,
      "stage": "引导说明页（分步教学，4 步 + 机型变体）",
      "screen_or_component": "同一原生引导页内的分步文案区 + 'Go to settings' 按钮（bt_goto_settings / ic_settings_main）",
      "trigger_event": "用户点击 'Go to settings' 按钮（instruction_button_activate）或滚动查看步骤",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Step 4 - Turn %s on / Go to settings",
      "shown_text_zh": "第 1 步 - 打开“设置”；第 2 步 - 打开“无障碍”；第 3 步 - 打开“已安装的服务”；第 4 步 - 打开 %s 的开关；前往设置",
      "user_action_requested": "严格按 4 步手动操作，最终在无障碍服务列表里打开目标服务开关",
      "code_anchor": "resources.arsc: instruction_step_1/2/3/4、samsung_instruction_step_2、xiaomi_instruction_step_1、bt_goto_settings"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载/已安装的服务（Settings.ACTION_ACCESSIBILITY_SETTINGS）",
      "trigger_event": "'Go to settings' 按钮点击后由加密代码 startActivity 跳转（具体调用点不可静态还原）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please enable Portal service under Accessibility settings / Check in 'Downloaded Services' list: %s",
      "shown_text_zh": "请在无障碍设置中启用 Portal 服务 / 请在“已下载的服务”列表中查找：%s",
      "user_action_requested": "在系统列表中定位并打开以银行名显示的无障碍服务开关（无取消/跳过提示）",
      "code_anchor": "resources.arsc: 字符串 'Please enable Portal service under Accessibility settings'、check_in_services_message；组件 com.grand.snail.bot.components.injects.system.InjAccessibilityService"
    },
    {
      "step": 5,
      "stage": "跳受限设置 / 悬浮窗授权",
      "screen_or_component": "系统应用详情页（ACTION_APPLICATION_DETAILS_SETTINGS）或系统'显示在其他应用上层'授权页",
      "trigger_event": "引导流程中按需跳转；由加密代码决定触发顺序（SYSTEM_ALERT_WINDOW 权限已声明）",
      "ui_carrier": "系统无障碍页 / 系统设置页",
      "shown_text_verbatim": "Step 2 - Allow to display pop-up windows from background mode / Step 2 - Give permission to \"Appear on top\" / Allow pop-up windows for the correct application work:",
      "shown_text_zh": "第 2 步 - 允许后台模式下显示弹窗 / 第 2 步 - 授予“显示在其他应用上层”权限 / 请允许弹窗以便应用正常工作：",
      "user_action_requested": "在系统设置中打开“显示在其他应用上层”开关；未提供取消路径",
      "code_anchor": "resources.arsc: 'Step 2 - Allow to display pop-up windows from background mode'、'Step 2 - Give permission to \"Appear on top\"'、'Allow pop-up windows for the correct application work:'"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.grand.snail.bot.components.injects.system.FullscreenOverlayService（无绑定权限、无类型限制声明）+ 系统设置页之上",
      "trigger_event": "跳转设置页后由服务/定时器拉起悬浮层（时机在加密载荷内）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Go to settings / Please enable Portal service under Accessibility settings / Check in 'Downloaded Services' list: %s",
      "shown_text_zh": "前往设置 / 请在无障碍设置中启用 Portal 服务 / 请在“已下载的服务”列表中查找：%s",
      "user_action_requested": "在悬浮指引下继续在系统页内点击开关，用户无法区分应用界面与系统界面",
      "code_anchor": "AndroidManifest: service com.grand.snail.bot.components.injects.system.FullscreenOverlayService；resources.arsc 同上"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环（关闭系统防护的诱导分支）",
      "screen_or_component": "原生引导页 + 可能的悬浮层；Play Protect / Scan device / 电池优化设置页",
      "trigger_event": "检测到无障碍未开启，或检测到 Google Play Protect / 设备扫描功能仍启用时触发",
      "ui_carrier": "原生Activity / 悬浮窗Overlay / 系统设置页",
      "shown_text_verbatim": "Google - do not disable this app / To install Security update you must disable 'Scan device' option! / Enable control over your battery usage. Press 'Activate' button in the next window / Scan device for",
      "shown_text_zh": "Google - 请勿停用此应用 / 要安装安全更新，您必须关闭“扫描设备”选项！/ 请允许控制电池使用，在下一窗口点击“激活”按钮 / 扫描设备以…",
      "user_action_requested": "关闭 Play Protect 校验、关闭 Scan device、忽略电池优化，为后续静默安装/后台常驻铺路",
      "code_anchor": "resources.arsc: do_not_disable、enablePlayProtect_message、services_playProtect*、services_playScanningDisableBtn、enable_control_battery_usage、'To install Security update you must disable \\'Scan device\\' option!'"
    },
    {
      "step": 8,
      "stage": "引导说明页（假更新遮罩）",
      "screen_or_component": "假更新进度页（布局 res/8C.xml：LinearLayout+RelativeLayout+TextView）或 WebViewActivity 远端页",
      "trigger_event": "获权前后由加密代码展示，掩盖实际后台动作",
      "ui_carrier": "原生Activity / 远端WebView",
      "shown_text_verbatim": "Installing updates... / It can takes a few moments",
      "shown_text_zh": "正在安装更新… / 可能需要一点时间",
      "user_action_requested": "等待（无按钮、无取消），用于消磨用户操作空窗期",
      "code_anchor": "布局 res/8C.xml（含 'Installing updates...'、'It can takes a few moments'）；组件 com.grand.snail.WebViewActivity + 布局 res/tR.xml（WebView）"
    },
    {
      "step": 9,
      "stage": "获权后动作",
      "screen_or_component": "InjAccessibilityService（canRetrieveWindowContent + canPerformGestures + canRequestFilterKeyEvents）、ScreencastService、Socks5ProxyService、NLService、LockerActivity",
      "trigger_event": "用户在系统页打开开关后 onServiceConnected（实现位于加密 dp/a.a，静态不可还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后无可见提示，转入读取窗口内容、模拟手势、屏幕录制与通知监听等隐蔽行为",
      "user_action_requested": "无需用户操作；服务在后台按远程指令执行",
      "code_anchor": "AndroidManifest: InjAccessibilityService / FullscreenOverlayService / ScreencastService / Socks5ProxyService / NLService；res/o5.xml 无障碍能力声明"
    }
  ],
  "text_presentation_locations": [
    "引导说明页 com.grand.snail.bot.PermissionsActivity（原生 Activity，ScrollView+TextView 分步文案，布局 res/02.xml / res/dD.xml）",
    "'Go to settings' 按钮（bt_goto_settings / ic_settings_main / instruction_button_activate）所在的原生引导页",
    "系统无障碍服务列表项：InjAccessibilityService 未声明 android:label 与 android:description（res/o5.xml），列表仅显示应用名 'Commerzbank Sicherheitszertifikat'",
    "系统设置页之上的全屏悬浮窗 FullscreenOverlayService（配合 SYSTEM_ALERT_WINDOW），承载 'Go to settings'、'Please enable Portal service…'、'Check in Downloaded Services list' 等指引",
    "Play Protect / Scan device / 电池优化分支文案（resources.arsc: do_not_disable、enablePlayProtect_message、services_playProtect*、enable_control_battery_usage）",
    "假更新遮罩页布局 res/8C.xml（'Installing updates...'、'It can takes a few moments'）",
    "WebView 载体：com.grand.snail.WebViewActivity（独立 taskAffinity .webViewTask）+ 纯 WebView 布局 res/tR.xml，可加载远端 HTML 教学页",
    "NotificationListener 服务 NLService 的 android:label 直接设为 'Commerzbank Sicherheitszertifikat'，在通知使用权列表中同样冒用银行名",
    "桌面图标与名称（LAUNCHER activity-alias 与 label/icon @7F070001/@7F020003 备用别名）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below:",
      "text_zh": "为了让最新版本的 %s 正常工作，您需要开启无障碍功能。请按以下步骤操作：",
      "source_location": "resources.arsc（instruction_step 引导段首句）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1 - Go to “Settings”",
      "text_zh": "第 1 步 - 打开“设置”",
      "source_location": "resources.arsc: instruction_step_1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2 - Open “Accessibility”",
      "text_zh": "第 2 步 - 打开“无障碍”",
      "source_location": "resources.arsc: instruction_step_2（另有 samsung_instruction_step_2 机型变体）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 3 - Open “Installed Services”",
      "text_zh": "第 3 步 - 打开“已安装的服务”",
      "source_location": "resources.arsc: instruction_step_3 / tv_instruction_step_3",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 4 - Turn %s on",
      "text_zh": "第 4 步 - 打开 %s 的开关",
      "source_location": "resources.arsc: instruction_step_4 / tv_instruction_step_4",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enable Portal service under Accessibility settings",
      "text_zh": "请在无障碍设置中启用 Portal 服务",
      "source_location": "resources.arsc（无障碍引导提示）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Check in 'Downloaded Services' list: %s",
      "text_zh": "请在“已下载的服务”列表中查找：%s",
      "source_location": "resources.arsc: check_in_services_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "To install Security update you must disable 'Scan device' option!",
      "text_zh": "要安装安全更新，您必须关闭“扫描设备”选项！",
      "source_location": "resources.arsc（反系统防护诱导文案）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Google - do not disable this app",
      "text_zh": "Google - 请勿停用此应用",
      "source_location": "resources.arsc: do_not_disable",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable control over your battery usage. Press 'Activate' button in the next window",
      "text_zh": "请允许控制电池使用，在下一窗口点击“激活”按钮",
      "source_location": "resources.arsc: enable_control_battery_usage",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2 - Allow to display pop-up windows from background mode",
      "text_zh": "第 2 步 - 允许后台模式下显示弹窗",
      "source_location": "resources.arsc（悬浮窗授权教学）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2 - Give permission to \"Appear on top\"",
      "text_zh": "第 2 步 - 授予“显示在其他应用上层”权限",
      "source_location": "resources.arsc（悬浮窗授权教学）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow pop-up windows for the correct application work:",
      "text_zh": "请允许弹窗，以便应用正常工作：",
      "source_location": "resources.arsc（悬浮窗授权教学首句）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Installing updates... It can takes a few moments",
      "text_zh": "正在安装更新… 可能需要一点时间",
      "source_location": "布局资源 res/8C.xml（两个 TextView 的 text 属性）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Scan device for",
      "text_zh": "扫描设备以…（配合 'Scan device' 设置项，用于引导关闭设备扫描）",
      "source_location": "resources.arsc（Scan device 分支文案，多语言版本如 't scannen nach'、'Scansiona dispositivo per'）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "de",
      "text_verbatim": "Check in der Liste 'Heruntergeladene Dienste': %s / Deinstallieren",
      "text_zh": "请在“已下载的服务”列表中查找：%s / 卸载",
      "source_location": "resources.arsc（德语资源，说明面向德语区用户）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Google - bu uygulamayı devre dışı bırakmayın",
      "text_zh": "Google - 请勿停用此应用",
      "source_location": "resources.arsc（土耳其语资源，do_not_disable 译文）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "es",
      "text_verbatim": "Compruebe en la lista 'Servicios descargados': %s",
      "text_zh": "请在“已下载的服务”列表中查找：%s",
      "source_location": "resources.arsc（西班牙语资源，check_in_services_message 译文）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "拒绝/返回后的具体反应位于加密载荷 dp/a.a，静态不可还原。可确认的相关支撑：入口 MainActivity 与 PermissionsActivity 均 excludeFromRecents=true（返回即离开，无法从最近任务回到中断点，用户只能重开应用再次进入引导）；FullscreenOverlayService 与 SYSTEM_ALERT_WINDOW 权限已具备在设置页之上反复拉起引导层的条件；MainReceiver/PeriodicJobReceiver 监听 BOOT_COMPLETED、USER_PRESENT、SCREEN_ON、PACKAGE_ADDED 等广播，具备开机/解锁/装包后再次触发引导的通道。",
    "overlay_or_fake_settings": "存在全屏悬浮层：com.grand.snail.bot.components.injects.system.FullscreenOverlayService（Manifest 中无 BIND 权限、无类型约束），配合 'Appear on top' 授权教学文案，可在系统无障碍页上叠放半透明引导遮罩；未发现自绘高仿系统无障碍开关页的静态证据。",
    "restricted_settings_13plus_coaching": "未见针对 Android 13+『允许受限设置』（应用详情右上角菜单）的专门文案；其引导路径是传统的 Settings→Accessibility→Installed Services/Downloaded Services 4 步教学，并额外教用户关闭 Play Protect 与 'Scan device' 以绕过安装校验。",
    "post_grant_anti_removal": "未获静态证据：GLOBAL_ACTION_BACK/HOME 撤权拦截逻辑位于加密 dp/a.a。但 LockerActivity 已声明 HOME category（enabled=false 可动态启用）与 HelperAdmin 设备管理器（watch-login/force-lock/wipe-data 策略），具备劫持 Home 键与设备管理的持久化/对抗卸载条件。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条互补触发：(1) 冷启动后立即监测 com.grand.snail.MainActivity / com.grand.snail.bot.PermissionsActivity 进入前台并出现含 'Go to settings' 按钮的引导页时开始录制；(2) 监测到当前包名切换为系统 Settings（无障碍/应用详情/显示在其他应用上层页）而屏幕上仍存在非系统的半透明浮层或提示文字时，判定为叠层指引窗口。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（4 步教学首屏）",
        "page_identifier": "activity=com.grand.snail.bot.PermissionsActivity 或 com.grand.snail.MainActivity；视图含 ScrollView + 多个 TextView（Step 1/2/3/4）与 text='Go to settings' 的 Button",
        "why_most_useful": "这是'应用主动教用户开无障碍'的直接意图证据，且 %s 占位符被填入的真实服务名/伪造名只有运行期可见",
        "observable_utg_signals": ["activity 类名与 excludeFromRecents 无最近任务卡片", "Text 'Step 1 - Go to “Settings”' / 'Step 3 - Open “Installed Services”'", "Button text 'Go to settings'", "是否存在取消/跳过按钮（预期无）"]
      },
      {
        "page_role": "跳转前的点击点",
        "page_identifier": "'Go to settings' 按钮点击瞬间（Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS）",
        "why_most_useful": "把静态文案与运行期实际跳转目标绑定，补上加密载荷中无法静态还原的 startActivity 目标",
        "observable_utg_signals": ["点击后前台 activity 变为 com.android.settings/.Settings$AccessibilitySettingsActivity", "跳转前是否有倒计时/不可关闭遮罩", "跳转前是否弹出第二个说明层"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍 → 已安装/已下载的服务列表中的 'Commerzbank Sicherheitszertifikat' 条目",
        "why_most_useful": "该服务无 label/无 description，列表项完全冒用银行名称，是身份伪装与'零说明授权'的核心证据页",
        "observable_utg_signals": ["列表项文本恰为应用名而非功能名", "条目下方无任何用途说明文字", "条目旁的服务名是否出现 'Portal service' 等伪造名称"]
      },
      {
        "page_role": "系统设置页之上的悬浮引导层",
        "page_identifier": "前台为 Settings 且存在非 Settings 包名的 TYPE_APPLICATION_OVERLAY 窗口（FullscreenOverlayService）",
        "why_most_useful": "区分'仅教学'与'在系统页上叠层诱导/误导点击'，是判定 COERCE_OVERLAY_STACK_ON_SETTINGS 的关键",
        "observable_utg_signals": ["窗口归属包名 com.grand.dogla 而前台 activity 属于 com.android.settings", "浮层内文本 'Please enable Portal service under Accessibility settings'", "浮层是否覆盖开关位置或添加手指指示"]
      },
      {
        "page_role": "假更新遮罩页 / WebView 教学页",
        "page_identifier": "布局 res/8C.xml 的 'Installing updates...' 页面，或 com.grand.snail.WebViewActivity（taskAffinity .webViewTask）加载的远端 URL",
        "why_most_useful": "验证是否用假更新页面掩盖获权后的实际动作，以及是否从远端下发可变引导文案",
        "observable_utg_signals": ["Text 'Installing updates...' / 'It can takes a few moments'", "WebView 加载的 URL 域名与页面语言", "页面无任何取消按钮且持续停留"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：DEX 主体被 DexProtector 整体加密（dp/a.a），跳转调用点、拒权重跳的定时/onResume 逻辑、%s 占位符的实际填充值、获权后的注入动作均需运行期观测或脱壳才能确认；本报告结论基于 Manifest + 资源字符串 + 布局 XML 的结构性证据。运行期 UTG 不受静态加壳影响，仍可完整捕获页面流转。另需注意：本样本另带 Play Protect/Scan device 关闭诱导与设备管理器、通知监听、屏幕录制、SOCKS5 代理能力，无障碍只是整条攻击链的其中一环。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.grand.snail.bot.components.injects.system.InjAccessibilityService（Manifest 声明，实现位于加密 dp/a.a）",
    "res/o5.xml（无障碍配置：settingsActivity、canRetrieveWindowContent、canPerformGestures、canRequestFilterKeyEvents；无 label/description）",
    "resources.arsc: instruction_step_1/2/3/4、check_in_services_message、do_not_disable、enable_control_battery_usage、services_playProtect*",
    "com.grand.snail.bot.PermissionsActivity / com.grand.snail.WebViewActivity / com.grand.snail.bot.components.injects.system.FullscreenOverlayService",
    "res/8C.xml（'Installing updates...' 假更新遮罩）、res/tR.xml（WebView 载体）",
    "xyz.magicph.dexpro.ProxyApplication + dp/a.a（DexProtector 加密载荷，约 987KB）"
  ]
}
```

</details>
