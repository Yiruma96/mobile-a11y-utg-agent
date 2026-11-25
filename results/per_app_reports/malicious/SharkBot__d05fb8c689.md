# MB_073__d05fb8c689｜SharkBot — Powerful Cleaner, Antivirus

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：199.3s

## 1. 一句话核心结论

- **核心申请方式**：以“跑一次恶意软件扫描”为由、无可取消按钮的原生弹窗反复诱导，点击后同时拉起系统无障碍设置页并在其上压入半透明遮罩，用静态置为“已开启”的假开关与指手图标教学用户手动打开本应用的无障碍开关
- **静态可见性说明**：无障碍诱导全链路（弹窗、跳转、遮罩引导页、无障碍描述文案、获权后自动返回）均为包内明文 Java/XML 资源，静态完整可见；仅后续点击脚本（SharedPreferences 中 SESSION 经 IIBCgKCntNatAu9qo1QgM8FH7 解密得到的 JSON 指令表）来自云端下发，与本条诱导流程判定无关
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d05fb8c6899c96d1519e46eaea848ead6a17c7ddd0e20228e83c1aa9f264011d` |
| 包名 / 年份 | `com.pagnotto28.sellsourcecode.supercleaner` / 2022 |
| 家族 / 品类 | **SharkBot**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Powerful Cleaner, Antivirus |
| 引导页宣称品牌/身份 | Super Cleaner / Clean master 手机清理与杀毒工具 |
| 系统无障碍列表服务名 | Powerful Cleaner, Antivirus |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍描述内用大量空行与换行把关键警告挤出可视区（strings.xml L39-L46 中 "Tap on top right use to Accessiblility service." 后接两处空行）；描述自称 Clean master（非本应用名）；拼写伪装 "Accessiblility"、"warinings"、"orther"；引导页开关硬编码 android:checked="true" 且 clickable=false 伪造“已开启”状态；包内另存 com.security.applock.ui.guildPermission.GuildPermissionActivity 与 com.testapp.duplicatefileremover.* 等多套同源复制工程类，形成同构多入口 |
| 无障碍服务类名 | `com.pagnotto28.sellsourcecode.supercleaner.service.ForceStopAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.pagnotto28.sellsourcecode.supercleaner.screen.main.MainActivity（含各子页 d.j.a.a.j.s 子类） | onResume 回调（每次返回前台都触发）→ d.j.a.a.j.s#Y() → 校验 d.j.a.a.l.d.c 未通过即调用 s#f0()；另 s#c0() 在 atsFull 条件下同样进入 f0() | 原生Dialog | **原文**：Permission Needed / Grant permission to Running a malware scan / Grant now<br>**译注**：需要权限 / 授予权限以运行一次恶意软件扫描 / 立即授予 | 只能点击“Grant now”（Grant now）；布局 dialog_ask_permission.xml 仅有 tv_action_1 一个按钮，无取消、稍后、跳过控件，点弹窗外或返回键关闭后下一次 onResume 会再次弹出 | `d.j.a.a.j.s#f0 / d.j.a.a.j.s#Y / DialogAskPermission#O0 / res/layout/dialog_ask_permission.xml` |
| 2 | 引导说明页 | DialogAskPermission 的 Lottie 动画 + 标题 tv_title + 正文 tv_content | DialogAskPermission#K0(Bundle) 创建对话框时 inflate dialog_ask_permission.xml 并调用 O0() 按权限名填文案 | 原生Dialog | **原文**：Permission Needed<br>**译注**：标题“需要权限”，配 robo_permission.json 循环播放的机器人动画，营造安全扫描氛围 | 无实际选择，仅作为点击“Grant now”前的说明页 | `DialogAskPermission#K0 / DialogAskPermission#O0 / res/values/strings.xml#L448 (permission_needed)` |
| 3 | 跳无障碍设置 | android.settings.ACCESSIBILITY_SETTINGS 系统无障碍设置页 + GuildPermissionActivity | DialogAskPermission#click 点击 2131362572（tv_action_1）→ 回调 DialogAskPermission$a#a → d.j.a.a.j.e#a() | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：通过裸 Action 拉起系统无障碍设置列表（不指定 package，迫使全列表检索）；随后立刻 startActivity(GuildPermissionActivity) 压栈 | 进入系统无障碍列表，自行找到 “Powerful Cleaner, Antivirus” 并开启开关 | `d.j.a.a.j.e#a / DialogAskPermission#click / GuildPermissionActivity#i0` |
| 4 | 遮罩叠层指引 | GuildPermissionActivity（Theme.AppCompat.Translucent 风格，覆盖在系统设置页之上） | GuildPermissionActivity.onCreate 中 setContentView(2131558441) 并按 intent extra "permission name" 填 tvContent；同时为 id 2131362082（ic_close）与 2131362159 绑定点击 | 悬浮窗Overlay | **原文**：Find Powerful Cleaner, Antivirus and grant accessibility permission<br>**译注**：“找到 Powerful Cleaner, Antivirus 并授予无障碍权限”；底部同时画出应用图标、应用名、一个已显示为开启状态的开关和一只指手图标 | 按指手图指引在系统列表中打开本应用无障碍开关；右上角有关闭图标可退出（但下次 onResume 会重来） | `GuildPermissionActivity#onCreate / res/layout/activity_guide_setting.xml / res/values/strings.xml#L203 (find_and_grant)` |
| 5 | 系统无障碍服务列表项 | 系统无障碍列表中的 “Powerful Cleaner, Antivirus” 条目描述区 | res/xml/accessibility_service_config.xml 的 android:description 引用 | 系统无障碍页 | **原文**：Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.<br>**译注**：“点右上角使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。启用无障碍服务时你必须接受安卓系统的警告。Clean master 不会将这些用于此处所列以外的任何用途。” | 阅读（被空行挤出的）描述后自行开启开关，并接受系统弹出的风险提示 | `res/xml/accessibility_service_config.xml / res/values/strings.xml#L39-L46` |
| 6 | 获权后动作 | com.pagnotto28.sellsourcecode.supercleaner.service.ForceStopAccessibility（android:process=":BackgroundService"） | 用户打开开关 → AccessibilityService.onServiceConnected() | 系统无障碍页 | **原文**：performGlobalAction(1)<br>**译注**：服务连接后立即发送 GLOBAL_ACTION_BACK 自动退出设置页，200ms 后再执行后续动作，用户几乎没有机会回看或复核描述内容 | 无（用户被自动带离设置页） | `ForceStopAccessibility#onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity/子页 onResume 触发的不可取消原生 AlertDialog（dialog_ask_permission.xml）：标题 permission_needed = “Permission Needed”，正文 accessibility_setting_permission = “Grant permission to Running a malware scan”，唯一按钮 grant_now = “Grant now”
- 同一弹窗内的 Lottie 动画 robo_permission.json（循环播放的机器人动画）作为“安全/杀毒”视觉暗示
- 拉起系统无障碍页后叠加的 GuildPermissionActivity 半透明遮罩（activity_guide_setting.xml，背景 #66000000），顶部 tv_content 显示 find_and_grant = “Find Powerful Cleaner, Antivirus and grant accessibility permission”，配 ic_warning 图标与 pointing_hand 指手图
- 同一遮罩内伪造的 SwitchCompat：android:checked="true" 且 android:clickable="false"，视觉上呈现“已开启”
- 系统无障碍服务列表项描述：res/xml/accessibility_service_config.xml → strings.xml accessibility_service_description（含大量空行）
- 应用内权限/功能页通用入口：strings.xml content_permission_1 = “Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%”（以提速 50% 为由的同类无障碍诱导文案）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Grant permission to Running a malware scan | 授予权限以运行一次恶意软件扫描 | `res/values/strings.xml key=accessibility_setting_permission (L47)，经 DialogAskPermission#O0 填入 tv_content` | 假反诈安全 |
| en | Permission Needed | 需要权限 | `res/values/strings.xml key=permission_needed (L448)，dialog_ask_permission.xml tv_title` | 故障恐吓 |
| en | Find Powerful Cleaner, Antivirus and grant accessibility permission | 找到 Powerful Cleaner, Antivirus 并授予无障碍权限 | `res/values/strings.xml key=find_and_grant (L203) + key=accessibility_permission (L38)，由 GuildPermissionActivity#onCreate 格式化；activity_guide_setting.xml tv_content` | 受限设置分步教学 |
| en | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. | 点右上角使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。启用无障碍服务时你将不得不接受安卓系统的警告。Clean master 不会将这些用于此处所列以外的任何用途。 | `res/values/strings.xml key=accessibility_service_description (L39-L46) → res/xml/accessibility_service_config.xml android:description` | 教唆忽视警告 |
| en | Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50% | 请授予无障碍权限以关闭以下自启动应用，加速效果可提升 50% | `res/values/strings.xml key=content_permission_1 (L131)` | 清理工具伪装 |
| en | Enable now | 立即启用 | `res/values/strings.xml key=Notificationbarcleanup_RightNow (L6)` | 清理工具伪装 |
| en | Grant App Usage Permission for a comprehensive phone scan effect | 授予应用使用情况权限以获得全面的手机扫描效果 | `res/values/strings.xml key=grant_app_permission (L222)，dialog_ask_permission.xml tv_content 默认值` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：弹窗无取消按钮；点击外部或返回键关闭后，下一次 MainActivity.onResume（含从系统设置页返回、切后台再回来、以及 s#c0() 在 atsFull 条件下的任意权限申请路径）都会重新走 s#Y()→s#f0() 再弹一次；引导页右上角 ic_close 可关闭，但不改变下次 onResume 重弹的事实
- **遮罩叠层 / 高仿系统设置页**：有：GuildPermissionActivity 以 Translucent 主题叠在系统无障碍设置页之上，activity_guide_setting.xml 为 #66000000 半透明全屏遮罩，内含应用图标 + 应用名 + android:checked="true" 且 clickable=false 的 SwitchCompat + pointing_hand 指手图，伪造“本应用开关已开启/应开启”的视觉指引（非高仿整页系统设置，但为针对该列表项的定点引导叠层）
- **Android 13+ 受限设置（Restricted Settings）应对**：本应用 targetSdkVersion=30，未实现 Android 13 应用详情页“允许受限设置”的菜单教学；但同一套 GuildPermissionActivity/find_and_grant 教学组件被复用于 OTHER 权限（USAGE_ACCESS_SETTINGS、ACTION_NOTIFICATION_LISTENER_SETTINGS、MANAGE_OVERLAY_PERMISSION、MANAGE_WRITE_SETTINGS），形成统一的“找到本应用并打开开关”分步教学模板
- **获权后即时行为与防撤权机制**：有：ForceStopAccessibility#onServiceConnected 在脚本态下立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）并 postDelayed 200ms 继续，自动把用户弹出系统设置页；服务另在 onAccessibilityEvent 中监听第三方包事件，可按脚本下发指令跳转 MANAGE_OVERLAY_PERMISSION / MANAGE_UNKNOWN_APP_SOURCES
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 MainActivity onResume 之后立即开始 UTG 抓取（应用每次回前台都会走 s#Y→s#f0）；或在监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间启动，并持续覆盖随后 1-2 秒（此时 GuildPermissionActivity 遮罩会压栈）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区：全链路文案均为可提取文本节点，遮罩为原生 View 而非纯图；但需注意应用同时内置 com.security.applock.ui.guildPermission.GuildPermissionActivity 与 com.testapp.duplicatefileremover.* 等同源复制工程类，若样本在不同构建中改用这些入口，页面类名会变化，建议以“文本 + 弹窗结构”而非固定类名做匹配；此外后续远程点击脚本（SESSION 解密后的 JSON 指令表）为云端下发，UTG 无法在诱导阶段观测到，需另做网络侧取证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/回前台引导弹窗页** | 包名 com.pagnotto28.sellsourcecode.supercleaner 的 Dialog 窗口，含文本 Permission Needed、Grant permission to Running a malware scan、Grant now，及 Lottie robo_permission | 这是唯一的选择入口，可直接证明“无取消按钮”与“以杀毒扫描为理由索要无障碍”两个关键判定要素 | 弹窗节点数量与可点击按钮列表（应仅 1 个）；正文文本 Grant permission to Running a malware scan；是否出现取消/稍后/跳过类节点 |
| **设置页后压栈的半透明遮罩引导页** | 系统无障碍设置页之上叠加的 GuildPermissionActivity 窗口，含 Find ... and grant accessibility permission、应用名、checked=true 的 Switch、指手图标 | 证明应用在系统设置页之上叠加伪造开关状态，实施定点视觉引导，是区分“良性跳设置”与“诱导”的决定性页面 | 同一时刻存在两个窗口/层级（系统设置 + 应用遮罩）；遮罩内 Switch 的 checked 状态为 true 但 clickable=false；遮罩文本包含应用名与 accessibility permission 字样 |
| **系统无障碍服务列表项** | Settings 无障碍列表中的 “Powerful Cleaner, Antivirus” 条目及其描述展开 | 核对系统侧实际呈现的描述文案是否与功能一致，以及用户是否被迫“接受系统警告” | 条目 label = Powerful Cleaner, Antivirus；描述文本含 Deep clean hidden junk / Hibernate draining apps；描述文本含 You will have to accept Android system warinings |
| **获权后自动返回瞬间** | 开启开关后无障碍设置页被 GLOBAL_ACTION_BACK 自动退出的界面变化 | 证明获权后立即主动终止用户在设置页的停留，属对抗性行为而非正常回跳 | 开关打开后 <500ms 内当前页从 Settings 变为应用主界面；无用户点击返回的输入事件记录 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.pagnotto28.sellsourcecode.supercleaner.screen.main.MainActivity#onResume → d.j.a.a.j.s#Y / d.j.a.a.j.s#f0`
- `com.pagnotto28.sellsourcecode.supercleaner.dialog.DialogAskPermission#O0 / #click / #K0`
- `d.j.a.a.j.e#a`
- `com.pagnotto28.sellsourcecode.supercleaner.screen.guildPermission.GuildPermissionActivity#onCreate / #i0`
- `com.pagnotto28.sellsourcecode.supercleaner.service.ForceStopAccessibility#onServiceConnected`
- `res/layout/dialog_ask_permission.xml / res/layout/activity_guide_setting.xml / res/xml/accessibility_service_config.xml / res/values/strings.xml (accessibility_setting_permission, find_and_grant, accessibility_service_description)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，共 14 次工具调用）

**结论：无障碍诱导流程完全可静态还原，代码清晰可见；无需加壳，也无需远端 HTML 配合。**

- **触发时机**：[MainActivity.onResume()](<resource-unit:#1.dex1 code:com.pagnotto28.sellsourcecode.supercleaner.screen.main.MainActivity#onResume>) 每次都会调用 `d.j.a.a.j.s#Y`；当无障碍未开启时，[s#f0()](<resource-unit:#1.dex1 code:d.j.a.a.j.s#f0>) 会构造并立即弹出 `DialogAskPermission`。这说明它是**反复回跳式**的，而不是只在冷启动时出现一次。
- **理由伪装**：[DialogAskPermission#O0](<resource-unit:#1.dex1 code:com.pagnotto28.sellsourcecode.supercleaner.dialog.DialogAskPermission#O0>) 对 `android.settings.ACCESSIBILITY_SETTINGS` 取 [strings.xml#L47](<resource-unit:#1 file:res/values/strings.xml#L47>) `accessibility_setting_permission` = `Grant permission to Running a malware scan`，把系统无障碍授权包装成“跑一次病毒扫描”。
- **无法拒绝**：[dialog_ask_permission.xml](<resource-unit:#1 file:res/layout/dialog_ask_permission.xml>) 只有一个 `tv_action_1`（`@string/grant_now`）按钮，没有取消、稍后或跳过按钮；[DialogAskPermission#click](<resource-unit:#1 code:com.pagnotto28.sellsourcecode.supercleaner.dialog.DialogAskPermission#click>) 只在该按钮被点击时触发回调。
- **分两步引导**：[e#a()](<resource-unit:#1.dex1 code:d.j.a.a.j.e#a>) 先调用 `startActivity("android.settings.ACCESSIBILITY_SETTINGS")` 拉起系统页，**紧接着**再调用 [GuildPermissionActivity.i0()](<resource-unit:#1.dex1 code:com.pagnotto28.sellsourcecode.supercleaner.screen.guildPermission.GuildPermissionActivity#i0>) 启动引导页，使其叠在系统设置页之上。
- **假开关遮罩**：[activity_guide_setting.xml](<resource-unit:#1 file:res/layout/activity_guide_setting.xml>) 是 `#66000000` 半透明全屏遮罩，底部为“应用图标 + 应用名 + `android:checked="true"` 且 `clickable="false"` 的 SwitchCompat + pointing_hand 指手图”，并在文案 [strings.xml#L203](<resource-unit:#1 file:res/values/strings.xml#L203>) `Find %s and grant %s` 中填入应用名与“accessibility permission”，实际效果是**教用户到系统列表里自己找到本应用并打开开关**。
- **系统列表文案**：[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 引用 [strings.xml#L39-L46](<resource-unit:#1 file:res/values/strings.xml#L39-L46>)，自称只用于“清理隐藏垃圾、休眠耗电应用”，并明确要求用户“You will have to accept Android system warinings”；但服务实际是 `ForceStopAccessibility#onAccessibilityEvent` 从 SharedPreferences 读取脚本 JSON，对任意第三方应用节点执行 `performAction(16)` 点击，并可跳转悬浮窗或未知来源设置，因此**功能声明与实际实现严重不符**。
- **获得权限后的对抗操作**：[ForceStopAccessibility#onServiceConnected()](<resource-unit:#1.dex1 code:com.pagnotto28.sellsourcecode.supercleaner.service.ForceStopAccessibility#onServiceConnected>) 在脚本态下立即 `performGlobalAction(1)`（GLOBAL_ACTION_BACK），并在 200ms 后继续，主动把用户“弹出”设置页。

已登记风险：R-001（high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导全链路（弹窗、跳转、遮罩引导页、无障碍描述文案、获权后自动返回）均为包内明文 Java/XML 资源，静态完整可见；仅后续点击脚本（SharedPreferences 中 SESSION 经 IIBCgKCntNatAu9qo1QgM8FH7 解密得到的 JSON 指令表）来自云端下发，与本条诱导流程判定无关",
  "summary_one_liner": "以“跑一次恶意软件扫描”为由、无可取消按钮的原生弹窗反复诱导，点击后同时拉起系统无障碍设置页并在其上压入半透明遮罩，用静态置为“已开启”的假开关与指手图标教学用户手动打开本应用的无障碍开关",
  "disguise_identity": {
    "app_display_name": "Powerful Cleaner, Antivirus",
    "claimed_brand_or_persona": "Super Cleaner / Clean master 手机清理与杀毒工具",
    "a11y_service_label": "Powerful Cleaner, Antivirus",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍描述内用大量空行与换行把关键警告挤出可视区（strings.xml L39-L46 中 \"Tap on top right use to Accessiblility service.\" 后接两处空行）；描述自称 Clean master（非本应用名）；拼写伪装 \"Accessiblility\"、\"warinings\"、\"orther\"；引导页开关硬编码 android:checked=\"true\" 且 clickable=false 伪造“已开启”状态；包内另存 com.security.applock.ui.guildPermission.GuildPermissionActivity 与 com.testapp.duplicatefileremover.* 等多套同源复制工程类，形成同构多入口"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.pagnotto28.sellsourcecode.supercleaner.screen.main.MainActivity（含各子页 d.j.a.a.j.s 子类）",
      "trigger_event": "onResume 回调（每次返回前台都触发）→ d.j.a.a.j.s#Y() → 校验 d.j.a.a.l.d.c 未通过即调用 s#f0()；另 s#c0() 在 atsFull 条件下同样进入 f0()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission Needed / Grant permission to Running a malware scan / Grant now",
      "shown_text_zh": "需要权限 / 授予权限以运行一次恶意软件扫描 / 立即授予",
      "user_action_requested": "只能点击“Grant now”（Grant now）；布局 dialog_ask_permission.xml 仅有 tv_action_1 一个按钮，无取消、稍后、跳过控件，点弹窗外或返回键关闭后下一次 onResume 会再次弹出",
      "code_anchor": "d.j.a.a.j.s#f0 / d.j.a.a.j.s#Y / DialogAskPermission#O0 / res/layout/dialog_ask_permission.xml"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "DialogAskPermission 的 Lottie 动画 + 标题 tv_title + 正文 tv_content",
      "trigger_event": "DialogAskPermission#K0(Bundle) 创建对话框时 inflate dialog_ask_permission.xml 并调用 O0() 按权限名填文案",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission Needed",
      "shown_text_zh": "标题“需要权限”，配 robo_permission.json 循环播放的机器人动画，营造安全扫描氛围",
      "user_action_requested": "无实际选择，仅作为点击“Grant now”前的说明页",
      "code_anchor": "DialogAskPermission#K0 / DialogAskPermission#O0 / res/values/strings.xml#L448 (permission_needed)"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS 系统无障碍设置页 + GuildPermissionActivity",
      "trigger_event": "DialogAskPermission#click 点击 2131362572（tv_action_1）→ 回调 DialogAskPermission$a#a → d.j.a.a.j.e#a()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "通过裸 Action 拉起系统无障碍设置列表（不指定 package，迫使全列表检索）；随后立刻 startActivity(GuildPermissionActivity) 压栈",
      "user_action_requested": "进入系统无障碍列表，自行找到 “Powerful Cleaner, Antivirus” 并开启开关",
      "code_anchor": "d.j.a.a.j.e#a / DialogAskPermission#click / GuildPermissionActivity#i0"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "GuildPermissionActivity（Theme.AppCompat.Translucent 风格，覆盖在系统设置页之上）",
      "trigger_event": "GuildPermissionActivity.onCreate 中 setContentView(2131558441) 并按 intent extra \"permission name\" 填 tvContent；同时为 id 2131362082（ic_close）与 2131362159 绑定点击",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Find Powerful Cleaner, Antivirus and grant accessibility permission",
      "shown_text_zh": "“找到 Powerful Cleaner, Antivirus 并授予无障碍权限”；底部同时画出应用图标、应用名、一个已显示为开启状态的开关和一只指手图标",
      "user_action_requested": "按指手图指引在系统列表中打开本应用无障碍开关；右上角有关闭图标可退出（但下次 onResume 会重来）",
      "code_anchor": "GuildPermissionActivity#onCreate / res/layout/activity_guide_setting.xml / res/values/strings.xml#L203 (find_and_grant)"
    },
    {
      "step": 5,
      "stage": "系统无障碍服务列表项",
      "screen_or_component": "系统无障碍列表中的 “Powerful Cleaner, Antivirus” 条目描述区",
      "trigger_event": "res/xml/accessibility_service_config.xml 的 android:description 引用",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "shown_text_zh": "“点右上角使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。启用无障碍服务时你必须接受安卓系统的警告。Clean master 不会将这些用于此处所列以外的任何用途。”",
      "user_action_requested": "阅读（被空行挤出的）描述后自行开启开关，并接受系统弹出的风险提示",
      "code_anchor": "res/xml/accessibility_service_config.xml / res/values/strings.xml#L39-L46"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.pagnotto28.sellsourcecode.supercleaner.service.ForceStopAccessibility（android:process=\":BackgroundService\"）",
      "trigger_event": "用户打开开关 → AccessibilityService.onServiceConnected()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "performGlobalAction(1)",
      "shown_text_zh": "服务连接后立即发送 GLOBAL_ACTION_BACK 自动退出设置页，200ms 后再执行后续动作，用户几乎没有机会回看或复核描述内容",
      "user_action_requested": "无（用户被自动带离设置页）",
      "code_anchor": "ForceStopAccessibility#onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "MainActivity/子页 onResume 触发的不可取消原生 AlertDialog（dialog_ask_permission.xml）：标题 permission_needed = “Permission Needed”，正文 accessibility_setting_permission = “Grant permission to Running a malware scan”，唯一按钮 grant_now = “Grant now”",
    "同一弹窗内的 Lottie 动画 robo_permission.json（循环播放的机器人动画）作为“安全/杀毒”视觉暗示",
    "拉起系统无障碍页后叠加的 GuildPermissionActivity 半透明遮罩（activity_guide_setting.xml，背景 #66000000），顶部 tv_content 显示 find_and_grant = “Find Powerful Cleaner, Antivirus and grant accessibility permission”，配 ic_warning 图标与 pointing_hand 指手图",
    "同一遮罩内伪造的 SwitchCompat：android:checked=\"true\" 且 android:clickable=\"false\"，视觉上呈现“已开启”",
    "系统无障碍服务列表项描述：res/xml/accessibility_service_config.xml → strings.xml accessibility_service_description（含大量空行）",
    "应用内权限/功能页通用入口：strings.xml content_permission_1 = “Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%”（以提速 50% 为由的同类无障碍诱导文案）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Grant permission to Running a malware scan",
      "text_zh": "授予权限以运行一次恶意软件扫描",
      "source_location": "res/values/strings.xml key=accessibility_setting_permission (L47)，经 DialogAskPermission#O0 填入 tv_content",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Permission Needed",
      "text_zh": "需要权限",
      "source_location": "res/values/strings.xml key=permission_needed (L448)，dialog_ask_permission.xml tv_title",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Find Powerful Cleaner, Antivirus and grant accessibility permission",
      "text_zh": "找到 Powerful Cleaner, Antivirus 并授予无障碍权限",
      "source_location": "res/values/strings.xml key=find_and_grant (L203) + key=accessibility_permission (L38)，由 GuildPermissionActivity#onCreate 格式化；activity_guide_setting.xml tv_content",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "text_zh": "点右上角使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。启用无障碍服务时你将不得不接受安卓系统的警告。Clean master 不会将这些用于此处所列以外的任何用途。",
      "source_location": "res/values/strings.xml key=accessibility_service_description (L39-L46) → res/xml/accessibility_service_config.xml android:description",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%",
      "text_zh": "请授予无障碍权限以关闭以下自启动应用，加速效果可提升 50%",
      "source_location": "res/values/strings.xml key=content_permission_1 (L131)",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable now",
      "text_zh": "立即启用",
      "source_location": "res/values/strings.xml key=Notificationbarcleanup_RightNow (L6)",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant App Usage Permission for a comprehensive phone scan effect",
      "text_zh": "授予应用使用情况权限以获得全面的手机扫描效果",
      "source_location": "res/values/strings.xml key=grant_app_permission (L222)，dialog_ask_permission.xml tv_content 默认值",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "弹窗无取消按钮；点击外部或返回键关闭后，下一次 MainActivity.onResume（含从系统设置页返回、切后台再回来、以及 s#c0() 在 atsFull 条件下的任意权限申请路径）都会重新走 s#Y()→s#f0() 再弹一次；引导页右上角 ic_close 可关闭，但不改变下次 onResume 重弹的事实",
    "overlay_or_fake_settings": "有：GuildPermissionActivity 以 Translucent 主题叠在系统无障碍设置页之上，activity_guide_setting.xml 为 #66000000 半透明全屏遮罩，内含应用图标 + 应用名 + android:checked=\"true\" 且 clickable=false 的 SwitchCompat + pointing_hand 指手图，伪造“本应用开关已开启/应开启”的视觉指引（非高仿整页系统设置，但为针对该列表项的定点引导叠层）",
    "restricted_settings_13plus_coaching": "本应用 targetSdkVersion=30，未实现 Android 13 应用详情页“允许受限设置”的菜单教学；但同一套 GuildPermissionActivity/find_and_grant 教学组件被复用于 OTHER 权限（USAGE_ACCESS_SETTINGS、ACTION_NOTIFICATION_LISTENER_SETTINGS、MANAGE_OVERLAY_PERMISSION、MANAGE_WRITE_SETTINGS），形成统一的“找到本应用并打开开关”分步教学模板",
    "post_grant_anti_removal": "有：ForceStopAccessibility#onServiceConnected 在脚本态下立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）并 postDelayed 200ms 继续，自动把用户弹出系统设置页；服务另在 onAccessibilityEvent 中监听第三方包事件，可按脚本下发指令跳转 MANAGE_OVERLAY_PERMISSION / MANAGE_UNKNOWN_APP_SOURCES",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 MainActivity onResume 之后立即开始 UTG 抓取（应用每次回前台都会走 s#Y→s#f0）；或在监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间启动，并持续覆盖随后 1-2 秒（此时 GuildPermissionActivity 遮罩会压栈）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/回前台引导弹窗页",
        "page_identifier": "包名 com.pagnotto28.sellsourcecode.supercleaner 的 Dialog 窗口，含文本 Permission Needed、Grant permission to Running a malware scan、Grant now，及 Lottie robo_permission",
        "why_most_useful": "这是唯一的选择入口，可直接证明“无取消按钮”与“以杀毒扫描为理由索要无障碍”两个关键判定要素",
        "observable_utg_signals": ["弹窗节点数量与可点击按钮列表（应仅 1 个）", "正文文本 Grant permission to Running a malware scan", "是否出现取消/稍后/跳过类节点"]
      },
      {
        "page_role": "设置页后压栈的半透明遮罩引导页",
        "page_identifier": "系统无障碍设置页之上叠加的 GuildPermissionActivity 窗口，含 Find ... and grant accessibility permission、应用名、checked=true 的 Switch、指手图标",
        "why_most_useful": "证明应用在系统设置页之上叠加伪造开关状态，实施定点视觉引导，是区分“良性跳设置”与“诱导”的决定性页面",
        "observable_utg_signals": ["同一时刻存在两个窗口/层级（系统设置 + 应用遮罩）", "遮罩内 Switch 的 checked 状态为 true 但 clickable=false", "遮罩文本包含应用名与 accessibility permission 字样"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中的 “Powerful Cleaner, Antivirus” 条目及其描述展开",
        "why_most_useful": "核对系统侧实际呈现的描述文案是否与功能一致，以及用户是否被迫“接受系统警告”",
        "observable_utg_signals": ["条目 label = Powerful Cleaner, Antivirus", "描述文本含 Deep clean hidden junk / Hibernate draining apps", "描述文本含 You will have to accept Android system warinings"]
      },
      {
        "page_role": "获权后自动返回瞬间",
        "page_identifier": "开启开关后无障碍设置页被 GLOBAL_ACTION_BACK 自动退出的界面变化",
        "why_most_useful": "证明获权后立即主动终止用户在设置页的停留，属对抗性行为而非正常回跳",
        "observable_utg_signals": ["开关打开后 <500ms 内当前页从 Settings 变为应用主界面", "无用户点击返回的输入事件记录"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区：全链路文案均为可提取文本节点，遮罩为原生 View 而非纯图；但需注意应用同时内置 com.security.applock.ui.guildPermission.GuildPermissionActivity 与 com.testapp.duplicatefileremover.* 等同源复制工程类，若样本在不同构建中改用这些入口，页面类名会变化，建议以“文本 + 弹窗结构”而非固定类名做匹配；此外后续远程点击脚本（SESSION 解密后的 JSON 指令表）为云端下发，UTG 无法在诱导阶段观测到，需另做网络侧取证。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.pagnotto28.sellsourcecode.supercleaner.screen.main.MainActivity#onResume → d.j.a.a.j.s#Y / d.j.a.a.j.s#f0",
    "com.pagnotto28.sellsourcecode.supercleaner.dialog.DialogAskPermission#O0 / #click / #K0",
    "d.j.a.a.j.e#a",
    "com.pagnotto28.sellsourcecode.supercleaner.screen.guildPermission.GuildPermissionActivity#onCreate / #i0",
    "com.pagnotto28.sellsourcecode.supercleaner.service.ForceStopAccessibility#onServiceConnected",
    "res/layout/dialog_ask_permission.xml / res/layout/activity_guide_setting.xml / res/xml/accessibility_service_config.xml / res/values/strings.xml (accessibility_setting_permission, find_and_grant, accessibility_service_description)"
  ]
}
```

</details>
