# MB_074__dd0641f261｜SharkBot — Antivirus, Super Cleaner

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：145.3s

## 1. 一句话核心结论

- **核心申请方式**：伪装成清理/杀毒工具的 SharkBot 家族样本，在每次 onResume 依据远端 SESSION 的 atsFull 标记弹不可取消的 Grant Now 原生弹窗，跳转系统无障碍设置后立刻压上带伪开关与手指指引的半透明高仿遮罩，获权后自动 GLOBAL_ACTION_BACK 退出设置页并由无障碍服务执行远端脚本跨应用自动点击。
- **静态可见性说明**：无障碍诱导全链路（触发判定、弹窗布局、跳转 Intent、叠层引导 Activity、获权后 GLOBAL_ACTION_BACK）均在 classes.dex 与 res/ 中明文可见，无加壳无加密载荷；仅触发开关值（SESSION 中 atsFull/status/package/cacheFile）与获权后执行的 ATS 脚本步骤来自远端 C2，本地以 AES 密钥 IIBCgKCntNatAu9qo1QgM8FH7 加密存放，属动态下发内容而非隐藏代码。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `dd0641f261d75864b164a7f963b45dc43c6c815ad01e5f51c29504c668e6d5ec` |
| 包名 / 年份 | `com.abbondioendrizzi.antivirus.supercleaner` / 2022 |
| 家族 / 品类 | **SharkBot**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Antivirus, Super Cleaner |
| 引导页宣称品牌/身份 | 伪装为杀毒+清理工具（自称 Super Cleaner，描述文案中又称 Clean master），并在无障碍说明中宣称仅用于深度清理隐藏垃圾与休眠耗电应用 |
| 系统无障碍列表服务名 | Antivirus, Super Cleaner（service android:label=@string/app_name，与桌面名一致，进程 :BackgroundService） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍 description 用 ' \n \n' 连续空行把关键声明挤出可视区；2) 说明内预先要求用户'接受 Android 系统警告'以降低对系统警告的警觉；3) 多处拼写错误（Accessiblility、warinings、orther）规避文本匹配；4) 包内并行嵌入 com.security.applock.*（应用锁，含独立 SplashActivity/MainActivity/PasswordActivity）与 com.testapp.duplicatefileremover.* 两套独立应用骨架，多 Activity 别名互相掩护；5) 服务运行于独立进程 :BackgroundService 并与 ServiceManager 前台服务共存；6) 无障碍配置 typeAllMask + feedbackAllMask + canRetrieveWindowContent=true，远超'清理垃圾'所需。 |
| 无障碍服务类名 | `com.abbondioendrizzi.antivirus.supercleaner.service.ForceStopAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.abbondioendrizzi.antivirus.supercleaner.screen.splash.SplashActivity → com.abbondioendrizzi.antivirus.supercleaner.screen.main.MainActivity | LAUNCHER 启动；MainActivity.onCreate 内 startForegroundService(ServiceManager) 并装配 Home/Tool/Personal 三页；MainActivity.onResume() 立即调用 Y() | 原生Activity | **原文**：无（本步不展示引导文案，仅进入判定）<br>**译注**：无 | 无需操作，用户进入首页即触发远端配置判定 | `com.abbondioendrizzi.antivirus.supercleaner.screen.main.MainActivity#onResume → d.a.a.a.j.s#Y` |
| 2 | 业务功能触发 | d.a.a.a.j.s.Y()（读取 SharedPreferences "prferences" 的 SESSION，AES 解密后取远端 JSON） | Y() 中 U() 返回 false 且 V(false)==false 时走无障碍分支：this.s.put("status","needInstall")；若 !y.c(this, ForceStopAccessibility.class) 则 S("atsFull") + h0("waitA11") + this.r=1 + f0() | 不可静态还原（开关值来自远端） | 无 | 无（自动判定） | `d.a.a.a.j.s#Y / d.a.a.a.j.s#U / d.a.a.a.j.s#c0` |
| 3 | 引导说明页 | com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission（DialogFragment，layout dialog_ask_permission.xml） | d.a.a.a.j.s#f0() 调用 DialogAskPermission.N0("android.settings.ACCESSIBILITY_SETTINGS", new o(this)).M0(C(), ...)，在 MainActivity 上 show | 原生Dialog | **原文**：Permission Needed \| Grant App Usage Permission for a comprehensive phone scan effect \| Grant Now（含 Lottie 动画 robo_permission.json）<br>**译注**：需要权限 / 授予应用使用权限以获得全面的手机扫描效果 / 立即授予（动画为循环播放的机器人动效） | 只能点击唯一按钮 Grant Now；该布局仅含 tv_action_1 一个按钮，无取消/跳过控件，仅可返回键退出 | `com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission#O0 / res/layout/dialog_ask_permission.xml / res/raw/robo_permission.json` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 点击 Grant Now（view id 2131362572）→ DialogAskPermission.click 先 J0(false,false) 关闭弹窗 → 回调 o.a() | 系统无障碍页 | **原文**：无（应用侧不展示）<br>**译注**：系统无障碍服务列表，其中一项显示 Antivirus, Super Cleaner | 用户在系统页中手动找到并打开本应用的无障碍开关 | `com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission#click → d.a.a.a.j.o#a` |
| 5 | 遮罩叠层指引 | com.abbondioendrizzi.antivirus.supercleaner.screen.guildPermission.GuildPermissionActivity（theme Theme.AppCompat.Translucent，layout activity_guide_setting.xml） | o.a() 在 startActivity(ACCESSIBILITY_SETTINGS) 之后同一方法内立即调用 GuildPermissionActivity.i0(sVar, "android.settings.ACCESSIBILITY_SETTINGS")，压栈到系统设置页之上；onCreate 按 intent 的 "permission name" 取 2131951651 文案 setText | 悬浮窗Overlay（半透明 Activity 叠层，非 SYSTEM_ALERT_WINDOW） | **原文**：@string/find_and_grant（顶部蓝色条 + ic_warning 警告图标）；卡片行：logo + @string/app_name + SwitchCompat(checked=true, clickable=false) + drawable/pointing_hand；遮罩底色 #66000000<br>**译注**：顶部警告条引导“找到并开启”；下方伪系统条目：本应用图标与名称、一个已显示为开启状态的灰色开关、一只手指图标指向该开关 | 按手指指引点开同名开关；仅右上角 ic_close 可关闭该引导层，但关闭后回到系统页仍需自行操作 | `com.abbondioendrizzi.antivirus.supercleaner.screen.guildPermission.GuildPermissionActivity#onCreate / res/layout/activity_guide_setting.xml` |
| 6 | 获权后动作 | com.abbondioendrizzi.antivirus.supercleaner.service.ForceStopAccessibility（process :BackgroundService） | 用户开启开关 → onServiceConnected()：this.f!=null 时立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）退出系统设置页，并 postDelayed(a(this), 200) 执行远端脚本；f==null 时直接 startActivity(MainActivity) | 系统无障碍页（被自动返回）+ 原生Activity | 无 | 无需操作（用户点击开关后即被强制退出设置页） | `com.abbondioendrizzi.antivirus.supercleaner.service.ForceStopAccessibility#onServiceConnected / #onAccessibilityEvent` |
| 7 | 拒权反馈循环 | MainActivity.onResume → d.a.a.a.j.s.c0() / f0() 再次弹 DialogAskPermission | 用户返回应用（未开启无障碍）→ onResume 再次执行 Y()/c0()：若 s 含 atsFull 且服务仍未启用则 S("atsFull")+h0("waitA11")+f0()，重新弹出 Grant Now 弹窗；仅当 status=="skip" 且 skip 时间戳在 3600000ms 内才放行 | 原生Dialog | **原文**：Permission Needed \| Grant App Usage Permission for a comprehensive phone scan effect \| Grant Now<br>**译注**：每次回到应用都会重新弹出同一索权弹窗，最长 1 小时后才可能按远端 skip 状态暂停 | 只能再次点 Grant Now 或返回键退出，无持久“拒绝并不再提示”选项 | `d.a.a.a.j.s#c0 / d.a.a.a.j.s#U / d.a.a.a.j.s#f0` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项描述：res/values/strings.xml 的 accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用），服务标签为 app_name「Antivirus, Super Cleaner」
- 冷启动/回前台不可取消的 DialogFragment：dialog_ask_permission.xml（Permission Needed / Grant App Usage Permission for a comprehensive phone scan effect / Grant Now + Lottie robo_permission.json 动画）
- 跳转系统设置后叠加的半透明引导 Activity：activity_guide_setting.xml（#66000000 全屏遮罩 + 警告条 @string/find_and_grant + 应用图标与名称 + 伪已开启 SwitchCompat + pointing_hand 手指图标）
- 同一索权文案在 DialogAskPermission.O0 中按权限类型分派，无障碍分支使用资源 id 2131951653；GuildPermissionActivity.onCreate 无障碍分支使用格式化资源 2131951809 拼接 app_name 与 2131951651
- 应用锁模块独立副本：com.security.applock.ui.guildPermission.GuildPermissionActivity.X() 复用同一套文案与跳转（d.m.a.i.b#a 中 startActivityForResult(ACCESSIBILITY_SETTINGS, 1111)）
- 设置/首页功能位旁的功能性文案（非索权）：accessibility_permission「accessibility permission」、accessibility_setting_permission「Grant permission to Running a malware scan」、Notificationbarcleanup_RightNow「Enable now」、advanced_protection「Advanced protection」

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. | 点击右上角即可使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾；休眠耗电应用。开启无障碍服务时你必须接受 Android 系统的警告。Clean master 不会将这些权限用于此处列明之外的任何其他用途。 | `res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service_config.xml 的 android:description 引用）` | 清理工具伪装 |
| en | You will have to accept Android system warinings when enabling Accessibility service. | 开启无障碍服务时你必须接受 Android 系统的警告。 | `res/values/strings.xml → accessibility_service_description 内嵌句` | 教唆忽视警告 |
| en | Clean master will not use these for any orther purpose than listed here. | Clean master 不会将这些权限用于此处列明之外的任何其他用途。 | `res/values/strings.xml → accessibility_service_description 内嵌句` | 隐私承诺 |
| en | Permission Needed | 需要权限 | `res/values/strings.xml → permission_needed（dialog_ask_permission.xml 的 tv_title）` | 假反诈安全 |
| en | Grant App Usage Permission for a comprehensive phone scan effect | 授予应用使用权限，以获得全面的手机扫描效果。 | `res/values/strings.xml → grant_app_permission（dialog_ask_permission.xml 的 tv_content）` | 假反诈安全 |
| en | Grant Now | 立即授予 | `res/values/strings.xml → grant_now（dialog_ask_permission.xml 唯一按钮 tv_action_1）` | 清理工具伪装 |
| en | Grant permission to Running a malware scan | 授予权限以运行恶意软件扫描。 | `res/values/strings.xml → accessibility_setting_permission` | 假反诈安全 |
| en | accessibility permission | 无障碍权限 | `res/values/strings.xml → accessibility_permission` | 良性透明说明 |
| en | Enable now | 立即启用 | `res/values/strings.xml → Notificationbarcleanup_RightNow` | 清理工具伪装 |
| en | @string/find_and_grant（顶部警告条文案，具体文本未在本次静态读取中逐字确认） | 找到并开启（引导用户在系统设置中找到本应用并打开开关） | `res/layout/activity_guide_setting.xml → tv_content 引用 @string/find_and_grant` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：MainActivity.onResume 每次回到应用都重新执行 Y()/c0()：只要 SESSION 中 atsFull 已置位且 ForceStopAccessibility 仍未启用，就再次 S("atsFull")+h0("waitA11")+f0() 重新弹出 Grant Now 弹窗；仅当远端把 status 置为 skip 且 skip 时间戳距今不足 3600000ms（1 小时冷却）时才会暂时放行，冷却过后再判一次。用户仅能用返回键关闭弹窗，不存在持久的“拒绝并不再提示”路径。
- **遮罩叠层 / 高仿系统设置页**：有。点击 Grant Now 后先 startActivity(ACTION_ACCESSIBILITY_SETTINGS)，紧接着在同一方法内启动 GuildPermissionActivity（Theme.AppCompat.Translucent），以 #66000000 全屏半透明遮罩覆盖系统无障碍页，底部绘制高仿系统条目：本应用 logo + app_name + 一个 clickable=false、checked=true 的 SwitchCompat（伪造已开启状态）+ pointing_hand 手指图标指向该开关，另配 ic_warning 与 find_and_grant 警告条。属半透明引导遮罩+高仿系统开关条目，非 SYSTEM_ALERT_WINDOW 悬浮窗。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、未发现“进应用详情点右上角菜单允许受限设置”的教学文案或 Session 安装器绕过；Manifest targetSdkVersion=30，本身不触发 Android 13 受限设置限制。
- **获权后即时行为与防撤权机制**：有（自退出而非阻止撤权）。ForceStopAccessibility.onServiceConnected() 在连上后立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）关闭系统设置页并 postDelayed 200ms 执行远端脚本；onAccessibilityEvent 中脚本执行完毕（this.g 到达末尾）时同样 performGlobalAction(1) 并拉起 MainActivity。同时服务以 typeAllMask 监听全部事件，可读取系统设置页节点（canRetrieveWindowContent=true），具备监听设置页并模拟点击/回退的能力；未发现主动阻止用户进入设置关闭开关的循环逻辑。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 am start 目标为 android.settings.ACCESSIBILITY_SETTINGS（或本应用启动后 3 秒内出现 DialogFragment 弹窗）的瞬间开始逐帧采集：因为跳转与叠层启动在同一次点击回调内顺序完成，设置页与引导遮罩会同时出现在窗口栈中，此刻采集可一次拿到系统设置页 + 伪开关遮罩两张关键页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：纯 UTG 的主要盲区不在文本而在开关状态：引导遮罩中的 SwitchCompat 为 android:clickable="false"，UTG 若仅按“可点击开关”匹配会漏检，需按“checked=true 且 clickable=false 的伪开关节点 + 遮罩叠在 Settings 之上”组合判定。另需注意：应用未加壳（静态可见），但 atsFull/status 等触发值来自远端 SESSION，若 C2 不下发 atsFull 则运行期不会出现该弹窗，属一阶段 Dropper/云控门控盲区；本次未发现纯图空文本诱导，Lottie 动画仅作装饰。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（不可取消原生 DialogFragment）** | DialogFragment 容器 + 循环 Lottie 动画 + 标题 Permission Needed + 唯一按钮 Grant Now（无 cancel/skip 控件） | 这是诱导链的第一跳，可确认索权发生时机（onResume/冷启动）与是否提供拒绝路径，并固定“清理扫描”话术与无障碍权限的绑定关系。 | 弹窗文本 Permission Needed / Grant App Usage Permission for a comprehensive phone scan effect / Grant Now；弹窗节点树中只有 1 个可点击按钮（无 Skip/Cancel）；弹窗出现与 Activity 生命周期/前台切换的时序关系 |
| **跳转后 0～800ms 压栈的半透明引导遮罩页** | 全屏半透明遮罩 + 底部卡片：应用图标 + Antivirus, Super Cleaner + 已 checked 的 SwitchCompat + 手指图标 + 警告图标与 find_and_grant 文案；包名 com.abbondioendrizzi.antivirus.supercleaner.screen.guildPermission.GuildPermissionActivity | 这是区分“良性跳设置”与“诱导/高仿系统开关”的决定性证据：遮罩直接叠在系统无障碍页之上并伪造开关已开启状态与点击位置。 | 窗口栈顶层为 Translucent Activity 且其下为 Settings 无障碍页；存在 clickable=false 但 checked=true 的 Switch 节点（伪开关）；顶部警告条文案与 pointing_hand 图标位置；遮罩底色 #66000000 造成的系统页半可见状态 |
| **系统无障碍服务列表项** | Settings 无障碍列表中 label=Antivirus, Super Cleaner、进程 :BackgroundService 的 ForceStopAccessibility 条目及其描述展开文本 | 核对系统侧最终呈现的身份与描述是否与代码行为一致，并验证用户在系统警告页看到的原文（含空行挤占与拼写错误）。 | 服务条目名称与桌面应用名一致但功能描述为清理/休眠；描述文本含连续空行与拼写错误；开关切换后是否立即被 GLOBAL_ACTION_BACK 弹出 |
| **获权瞬间的设置页退出与回应用页** | 开关开启后系统设置页在数百毫秒内消失，前台变为 MainActivity（或直接进入远端脚本驱动的目标应用界面） | 验证 onServiceConnected 的 performGlobalAction(1) 自动返回行为，以及获权后是否立刻开始跨应用自动点击（后续权限/安装跳转）。 | 开关 ON 与窗口返回应用的时差 < 1s；返回后短时间内出现 MANAGE_UNKNOWN_APP_SOURCES / MANAGE_OVERLAY_PERMISSION 页面；无障碍服务事件流中非本应用包名的窗口内容读取 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.abbondioendrizzi.antivirus.supercleaner.screen.main.MainActivity#onResume → d.a.a.a.j.s#Y`
- `d.a.a.a.j.s#c0 / d.a.a.a.j.s#U（atsFull 判定与 1 小时 skip 冷却）`
- `d.a.a.a.j.s#f0 → com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission#N0 / #O0`
- `com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission#click → d.a.a.a.j.o#a`
- `com.abbondioendrizzi.antivirus.supercleaner.screen.guildPermission.GuildPermissionActivity#onCreate / #i0`
- `com.abbondioendrizzi.antivirus.supercleaner.service.ForceStopAccessibility#onServiceConnected / #onAccessibilityEvent`
- `res/layout/dialog_ask_permission.xml、res/layout/activity_guide_setting.xml、res/xml/accessibility_service_config.xml、res/values/strings.xml(accessibility_service_description)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**该应用是伪装成“Antivirus, Super Cleaner”的清理工具，其无障碍权限申请完全由远端 SESSION 配置驱动，并通过三步递进式页面诱导用户开启权限：原生弹窗 → 跳转系统设置 → 在设置页上方覆盖一层伪开关引导遮罩。**

1. **触发链（运行期真实可达）**：`MainActivity.onResume()` → `d.a.a.a.j.s.Y()`。`Y()` 先解密本地 `SESSION`（AES 密钥 `IIBCgKCntNatAu9qo1QgM8FH7`）取得服务端下发的 JSON；若 `atsFull` 已置位且 `ForceStopAccessibility` 未启用，则调用 `S("atsFull")`、`h0("waitA11")`、`f0()` 重新弹出无障碍申请弹窗。**每次 onResume（冷启动/切回前台）都会重新进入该判断**，属于典型的“冷启动+回前台”反复索权。
2. **第一步：原生 DialogFragment**：`DialogAskPermission` 加载 [dialog_ask_permission.xml](<resource-unit:#1 file:res/layout/dialog_ask_permission.xml>)。界面包含 Lottie 动画 `robo_permission.json`、标题 `Permission Needed`、正文 `Grant App Usage Permission for a comprehensive phone scan effect`，**只有一个 `Grant Now` 按钮，没有取消或跳过控件**。
3. **第二步：跳系统无障碍页并叠层**：点击 `Grant Now` → [DialogAskPermission.click()](<resource-unit:#1.dex1 code:com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission#click>) 先关闭弹窗 → [d.a.a.a.j.o#a](<resource-unit:#1.dex1 code:d.a.a.a.j.o#a>) 执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，**紧接着** 启动 [GuildPermissionActivity.i0()](<resource-unit:#1.dex1 code:com.abbondioendrizzi.antivirus.supercleaner.screen.guildPermission.GuildPermissionActivity#i0>)，把半透明引导 Activity 压到系统设置页之上。
4. **引导遮罩为高仿开关**：[activity_guide_setting.xml](<resource-unit:#1 file:res/layout/activity_guide_setting.xml>) 全屏 `#66000000` 半透明遮罩，底部卡片含警告图标、引导文案、本应用图标加应用名、一个 `android:clickable="false"` 且 `android:checked="true"` 的 `SwitchCompat`（伪造“已开启”开关状态）以及 `pointing_hand` 手指图标指向该开关，视觉上模拟系统无障碍条目。
5. **获权后自动退出设置页**：[ForceStopAccessibility.onServiceConnected()](<resource-unit:#1.dex1 code:com.abbondioendrizzi.antivirus.supercleaner.service.ForceStopAccessibility#onServiceConnected>) 一旦连上即 `performGlobalAction(1)`（GLOBAL_ACTION_BACK）并延时 200ms 执行后续动作，用户刚点完开关就被弹回应用；服务同时以 `typeAllMask` + `canRetrieveWindowContent=true` 采集他人应用窗口内容，并执行远端脚本（`performAction(16)` 点击、`SCROLL_BACKWARD`，甚至再跳 `MANAGE_OVERLAY_PERMISSION` / `MANAGE_UNKNOWN_APP_SOURCES`）。
6. **身份与用途不一致**：系统无障碍列表名 = `app_name`（`Antivirus, Super Cleaner`），`android:description` 自称仅用于“深度清理隐藏垃圾/休眠耗电应用”，并预告“你需要在开启无障碍时接受 Android 系统警告”，同时以拼写错误的 `Accessiblility / warinings / orther` 与 `\n \n` 空行填充拉开警告间距；实际代码与“清理”无关，是服务端脚本化的跨应用自动点击。包内还并行嵌入 `com.security.applock.*`、`com.testapp.duplicatefileremover.*` 两套独立应用骨架作多重伪装。
7. **静态可见性**：DEX 未加壳，引导链 100% 静态可还原；仅“下发什么 `atsFull` 指令、脚本步骤内容”位于远端（本地以 AES 存储 SESSION），不影响本问题的页面流转结论。
8. **Android 13+ 受限设置**：未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转或受限设置分步教学（targetSdk 30 亦不受该限制约束），此项为“无”。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导全链路（触发判定、弹窗布局、跳转 Intent、叠层引导 Activity、获权后 GLOBAL_ACTION_BACK）均在 classes.dex 与 res/ 中明文可见，无加壳无加密载荷；仅触发开关值（SESSION 中 atsFull/status/package/cacheFile）与获权后执行的 ATS 脚本步骤来自远端 C2，本地以 AES 密钥 IIBCgKCntNatAu9qo1QgM8FH7 加密存放，属动态下发内容而非隐藏代码。",
  "summary_one_liner": "伪装成清理/杀毒工具的 SharkBot 家族样本，在每次 onResume 依据远端 SESSION 的 atsFull 标记弹不可取消的 Grant Now 原生弹窗，跳转系统无障碍设置后立刻压上带伪开关与手指指引的半透明高仿遮罩，获权后自动 GLOBAL_ACTION_BACK 退出设置页并由无障碍服务执行远端脚本跨应用自动点击。",
  "disguise_identity": {
    "app_display_name": "Antivirus, Super Cleaner",
    "claimed_brand_or_persona": "伪装为杀毒+清理工具（自称 Super Cleaner，描述文案中又称 Clean master），并在无障碍说明中宣称仅用于深度清理隐藏垃圾与休眠耗电应用",
    "a11y_service_label": "Antivirus, Super Cleaner（service android:label=@string/app_name，与桌面名一致，进程 :BackgroundService）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍 description 用 ' \\n \\n' 连续空行把关键声明挤出可视区；2) 说明内预先要求用户'接受 Android 系统警告'以降低对系统警告的警觉；3) 多处拼写错误（Accessiblility、warinings、orther）规避文本匹配；4) 包内并行嵌入 com.security.applock.*（应用锁，含独立 SplashActivity/MainActivity/PasswordActivity）与 com.testapp.duplicatefileremover.* 两套独立应用骨架，多 Activity 别名互相掩护；5) 服务运行于独立进程 :BackgroundService 并与 ServiceManager 前台服务共存；6) 无障碍配置 typeAllMask + feedbackAllMask + canRetrieveWindowContent=true，远超'清理垃圾'所需。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.abbondioendrizzi.antivirus.supercleaner.screen.splash.SplashActivity → com.abbondioendrizzi.antivirus.supercleaner.screen.main.MainActivity",
      "trigger_event": "LAUNCHER 启动；MainActivity.onCreate 内 startForegroundService(ServiceManager) 并装配 Home/Tool/Personal 三页；MainActivity.onResume() 立即调用 Y()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（本步不展示引导文案，仅进入判定）",
      "shown_text_zh": "无",
      "user_action_requested": "无需操作，用户进入首页即触发远端配置判定",
      "code_anchor": "com.abbondioendrizzi.antivirus.supercleaner.screen.main.MainActivity#onResume → d.a.a.a.j.s#Y"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "d.a.a.a.j.s.Y()（读取 SharedPreferences \"prferences\" 的 SESSION，AES 解密后取远端 JSON）",
      "trigger_event": "Y() 中 U() 返回 false 且 V(false)==false 时走无障碍分支：this.s.put(\"status\",\"needInstall\")；若 !y.c(this, ForceStopAccessibility.class) 则 S(\"atsFull\") + h0(\"waitA11\") + this.r=1 + f0()",
      "ui_carrier": "不可静态还原（开关值来自远端）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务端下发 atsFull/status 决定是否进入无障碍索取；本次不满足条件则先走 MANAGE_UNKNOWN_APP_SOURCES 安装未知来源分支",
      "user_action_requested": "无（自动判定）",
      "code_anchor": "d.a.a.a.j.s#Y / d.a.a.a.j.s#U / d.a.a.a.j.s#c0"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission（DialogFragment，layout dialog_ask_permission.xml）",
      "trigger_event": "d.a.a.a.j.s#f0() 调用 DialogAskPermission.N0(\"android.settings.ACCESSIBILITY_SETTINGS\", new o(this)).M0(C(), ...)，在 MainActivity 上 show",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission Needed | Grant App Usage Permission for a comprehensive phone scan effect | Grant Now（含 Lottie 动画 robo_permission.json）",
      "shown_text_zh": "需要权限 / 授予应用使用权限以获得全面的手机扫描效果 / 立即授予（动画为循环播放的机器人动效）",
      "user_action_requested": "只能点击唯一按钮 Grant Now；该布局仅含 tv_action_1 一个按钮，无取消/跳过控件，仅可返回键退出",
      "code_anchor": "com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission#O0 / res/layout/dialog_ask_permission.xml / res/raw/robo_permission.json"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "点击 Grant Now（view id 2131362572）→ DialogAskPermission.click 先 J0(false,false) 关闭弹窗 → 回调 o.a()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧不展示）",
      "shown_text_zh": "系统无障碍服务列表，其中一项显示 Antivirus, Super Cleaner",
      "user_action_requested": "用户在系统页中手动找到并打开本应用的无障碍开关",
      "code_anchor": "com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission#click → d.a.a.a.j.o#a"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.abbondioendrizzi.antivirus.supercleaner.screen.guildPermission.GuildPermissionActivity（theme Theme.AppCompat.Translucent，layout activity_guide_setting.xml）",
      "trigger_event": "o.a() 在 startActivity(ACCESSIBILITY_SETTINGS) 之后同一方法内立即调用 GuildPermissionActivity.i0(sVar, \"android.settings.ACCESSIBILITY_SETTINGS\")，压栈到系统设置页之上；onCreate 按 intent 的 \"permission name\" 取 2131951651 文案 setText",
      "ui_carrier": "悬浮窗Overlay（半透明 Activity 叠层，非 SYSTEM_ALERT_WINDOW）",
      "shown_text_verbatim": "@string/find_and_grant（顶部蓝色条 + ic_warning 警告图标）；卡片行：logo + @string/app_name + SwitchCompat(checked=true, clickable=false) + drawable/pointing_hand；遮罩底色 #66000000",
      "shown_text_zh": "顶部警告条引导“找到并开启”；下方伪系统条目：本应用图标与名称、一个已显示为开启状态的灰色开关、一只手指图标指向该开关",
      "user_action_requested": "按手指指引点开同名开关；仅右上角 ic_close 可关闭该引导层，但关闭后回到系统页仍需自行操作",
      "code_anchor": "com.abbondioendrizzi.antivirus.supercleaner.screen.guildPermission.GuildPermissionActivity#onCreate / res/layout/activity_guide_setting.xml"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.abbondioendrizzi.antivirus.supercleaner.service.ForceStopAccessibility（process :BackgroundService）",
      "trigger_event": "用户开启开关 → onServiceConnected()：this.f!=null 时立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）退出系统设置页，并 postDelayed(a(this), 200) 执行远端脚本；f==null 时直接 startActivity(MainActivity)",
      "ui_carrier": "系统无障碍页（被自动返回）+ 原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无障碍服务连上即自动返回键关闭设置页，用户被瞬间带回应用，随后由服务端脚本驱动跨应用自动点击",
      "user_action_requested": "无需操作（用户点击开关后即被强制退出设置页）",
      "code_anchor": "com.abbondioendrizzi.antivirus.supercleaner.service.ForceStopAccessibility#onServiceConnected / #onAccessibilityEvent"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onResume → d.a.a.a.j.s.c0() / f0() 再次弹 DialogAskPermission",
      "trigger_event": "用户返回应用（未开启无障碍）→ onResume 再次执行 Y()/c0()：若 s 含 atsFull 且服务仍未启用则 S(\"atsFull\")+h0(\"waitA11\")+f0()，重新弹出 Grant Now 弹窗；仅当 status==\"skip\" 且 skip 时间戳在 3600000ms 内才放行",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission Needed | Grant App Usage Permission for a comprehensive phone scan effect | Grant Now",
      "shown_text_zh": "每次回到应用都会重新弹出同一索权弹窗，最长 1 小时后才可能按远端 skip 状态暂停",
      "user_action_requested": "只能再次点 Grant Now 或返回键退出，无持久“拒绝并不再提示”选项",
      "code_anchor": "d.a.a.a.j.s#c0 / d.a.a.a.j.s#U / d.a.a.a.j.s#f0"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项描述：res/values/strings.xml 的 accessibility_service_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用），服务标签为 app_name「Antivirus, Super Cleaner」",
    "冷启动/回前台不可取消的 DialogFragment：dialog_ask_permission.xml（Permission Needed / Grant App Usage Permission for a comprehensive phone scan effect / Grant Now + Lottie robo_permission.json 动画）",
    "跳转系统设置后叠加的半透明引导 Activity：activity_guide_setting.xml（#66000000 全屏遮罩 + 警告条 @string/find_and_grant + 应用图标与名称 + 伪已开启 SwitchCompat + pointing_hand 手指图标）",
    "同一索权文案在 DialogAskPermission.O0 中按权限类型分派，无障碍分支使用资源 id 2131951653；GuildPermissionActivity.onCreate 无障碍分支使用格式化资源 2131951809 拼接 app_name 与 2131951651",
    "应用锁模块独立副本：com.security.applock.ui.guildPermission.GuildPermissionActivity.X() 复用同一套文案与跳转（d.m.a.i.b#a 中 startActivityForResult(ACCESSIBILITY_SETTINGS, 1111)）",
    "设置/首页功能位旁的功能性文案（非索权）：accessibility_permission「accessibility permission」、accessibility_setting_permission「Grant permission to Running a malware scan」、Notificationbarcleanup_RightNow「Enable now」、advanced_protection「Advanced protection」"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "text_zh": "点击右上角即可使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾；休眠耗电应用。开启无障碍服务时你必须接受 Android 系统的警告。Clean master 不会将这些权限用于此处列明之外的任何其他用途。",
      "source_location": "res/values/strings.xml → accessibility_service_description（被 res/xml/accessibility_service_config.xml 的 android:description 引用）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "You will have to accept Android system warinings when enabling Accessibility service.",
      "text_zh": "开启无障碍服务时你必须接受 Android 系统的警告。",
      "source_location": "res/values/strings.xml → accessibility_service_description 内嵌句",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Clean master will not use these for any orther purpose than listed here.",
      "text_zh": "Clean master 不会将这些权限用于此处列明之外的任何其他用途。",
      "source_location": "res/values/strings.xml → accessibility_service_description 内嵌句",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Permission Needed",
      "text_zh": "需要权限",
      "source_location": "res/values/strings.xml → permission_needed（dialog_ask_permission.xml 的 tv_title）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant App Usage Permission for a comprehensive phone scan effect",
      "text_zh": "授予应用使用权限，以获得全面的手机扫描效果。",
      "source_location": "res/values/strings.xml → grant_app_permission（dialog_ask_permission.xml 的 tv_content）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant Now",
      "text_zh": "立即授予",
      "source_location": "res/values/strings.xml → grant_now（dialog_ask_permission.xml 唯一按钮 tv_action_1）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant permission to Running a malware scan",
      "text_zh": "授予权限以运行恶意软件扫描。",
      "source_location": "res/values/strings.xml → accessibility_setting_permission",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "accessibility permission",
      "text_zh": "无障碍权限",
      "source_location": "res/values/strings.xml → accessibility_permission",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable now",
      "text_zh": "立即启用",
      "source_location": "res/values/strings.xml → Notificationbarcleanup_RightNow",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "@string/find_and_grant（顶部警告条文案，具体文本未在本次静态读取中逐字确认）",
      "text_zh": "找到并开启（引导用户在系统设置中找到本应用并打开开关）",
      "source_location": "res/layout/activity_guide_setting.xml → tv_content 引用 @string/find_and_grant",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "MainActivity.onResume 每次回到应用都重新执行 Y()/c0()：只要 SESSION 中 atsFull 已置位且 ForceStopAccessibility 仍未启用，就再次 S(\"atsFull\")+h0(\"waitA11\")+f0() 重新弹出 Grant Now 弹窗；仅当远端把 status 置为 skip 且 skip 时间戳距今不足 3600000ms（1 小时冷却）时才会暂时放行，冷却过后再判一次。用户仅能用返回键关闭弹窗，不存在持久的“拒绝并不再提示”路径。",
    "overlay_or_fake_settings": "有。点击 Grant Now 后先 startActivity(ACTION_ACCESSIBILITY_SETTINGS)，紧接着在同一方法内启动 GuildPermissionActivity（Theme.AppCompat.Translucent），以 #66000000 全屏半透明遮罩覆盖系统无障碍页，底部绘制高仿系统条目：本应用 logo + app_name + 一个 clickable=false、checked=true 的 SwitchCompat（伪造已开启状态）+ pointing_hand 手指图标指向该开关，另配 ic_warning 与 find_and_grant 警告条。属半透明引导遮罩+高仿系统开关条目，非 SYSTEM_ALERT_WINDOW 悬浮窗。",
    "restricted_settings_13plus_coaching": "无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、未发现“进应用详情点右上角菜单允许受限设置”的教学文案或 Session 安装器绕过；Manifest targetSdkVersion=30，本身不触发 Android 13 受限设置限制。",
    "post_grant_anti_removal": "有（自退出而非阻止撤权）。ForceStopAccessibility.onServiceConnected() 在连上后立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）关闭系统设置页并 postDelayed 200ms 执行远端脚本；onAccessibilityEvent 中脚本执行完毕（this.g 到达末尾）时同样 performGlobalAction(1) 并拉起 MainActivity。同时服务以 typeAllMask 监听全部事件，可读取系统设置页节点（canRetrieveWindowContent=true），具备监听设置页并模拟点击/回退的能力；未发现主动阻止用户进入设置关闭开关的循环逻辑。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 am start 目标为 android.settings.ACCESSIBILITY_SETTINGS（或本应用启动后 3 秒内出现 DialogFragment 弹窗）的瞬间开始逐帧采集：因为跳转与叠层启动在同一次点击回调内顺序完成，设置页与引导遮罩会同时出现在窗口栈中，此刻采集可一次拿到系统设置页 + 伪开关遮罩两张关键页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（不可取消原生 DialogFragment）",
        "page_identifier": "DialogFragment 容器 + 循环 Lottie 动画 + 标题 Permission Needed + 唯一按钮 Grant Now（无 cancel/skip 控件）",
        "why_most_useful": "这是诱导链的第一跳，可确认索权发生时机（onResume/冷启动）与是否提供拒绝路径，并固定“清理扫描”话术与无障碍权限的绑定关系。",
        "observable_utg_signals": ["弹窗文本 Permission Needed / Grant App Usage Permission for a comprehensive phone scan effect / Grant Now", "弹窗节点树中只有 1 个可点击按钮（无 Skip/Cancel）", "弹窗出现与 Activity 生命周期/前台切换的时序关系"]
      },
      {
        "page_role": "跳转后 0～800ms 压栈的半透明引导遮罩页",
        "page_identifier": "全屏半透明遮罩 + 底部卡片：应用图标 + Antivirus, Super Cleaner + 已 checked 的 SwitchCompat + 手指图标 + 警告图标与 find_and_grant 文案；包名 com.abbondioendrizzi.antivirus.supercleaner.screen.guildPermission.GuildPermissionActivity",
        "why_most_useful": "这是区分“良性跳设置”与“诱导/高仿系统开关”的决定性证据：遮罩直接叠在系统无障碍页之上并伪造开关已开启状态与点击位置。",
        "observable_utg_signals": ["窗口栈顶层为 Translucent Activity 且其下为 Settings 无障碍页", "存在 clickable=false 但 checked=true 的 Switch 节点（伪开关）", "顶部警告条文案与 pointing_hand 图标位置", "遮罩底色 #66000000 造成的系统页半可见状态"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中 label=Antivirus, Super Cleaner、进程 :BackgroundService 的 ForceStopAccessibility 条目及其描述展开文本",
        "why_most_useful": "核对系统侧最终呈现的身份与描述是否与代码行为一致，并验证用户在系统警告页看到的原文（含空行挤占与拼写错误）。",
        "observable_utg_signals": ["服务条目名称与桌面应用名一致但功能描述为清理/休眠", "描述文本含连续空行与拼写错误", "开关切换后是否立即被 GLOBAL_ACTION_BACK 弹出"]
      },
      {
        "page_role": "获权瞬间的设置页退出与回应用页",
        "page_identifier": "开关开启后系统设置页在数百毫秒内消失，前台变为 MainActivity（或直接进入远端脚本驱动的目标应用界面）",
        "why_most_useful": "验证 onServiceConnected 的 performGlobalAction(1) 自动返回行为，以及获权后是否立刻开始跨应用自动点击（后续权限/安装跳转）。",
        "observable_utg_signals": ["开关 ON 与窗口返回应用的时差 < 1s", "返回后短时间内出现 MANAGE_UNKNOWN_APP_SOURCES / MANAGE_OVERLAY_PERMISSION 页面", "无障碍服务事件流中非本应用包名的窗口内容读取"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "纯 UTG 的主要盲区不在文本而在开关状态：引导遮罩中的 SwitchCompat 为 android:clickable=\"false\"，UTG 若仅按“可点击开关”匹配会漏检，需按“checked=true 且 clickable=false 的伪开关节点 + 遮罩叠在 Settings 之上”组合判定。另需注意：应用未加壳（静态可见），但 atsFull/status 等触发值来自远端 SESSION，若 C2 不下发 atsFull 则运行期不会出现该弹窗，属一阶段 Dropper/云控门控盲区；本次未发现纯图空文本诱导，Lottie 动画仅作装饰。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.abbondioendrizzi.antivirus.supercleaner.screen.main.MainActivity#onResume → d.a.a.a.j.s#Y",
    "d.a.a.a.j.s#c0 / d.a.a.a.j.s#U（atsFull 判定与 1 小时 skip 冷却）",
    "d.a.a.a.j.s#f0 → com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission#N0 / #O0",
    "com.abbondioendrizzi.antivirus.supercleaner.dialog.DialogAskPermission#click → d.a.a.a.j.o#a",
    "com.abbondioendrizzi.antivirus.supercleaner.screen.guildPermission.GuildPermissionActivity#onCreate / #i0",
    "com.abbondioendrizzi.antivirus.supercleaner.service.ForceStopAccessibility#onServiceConnected / #onAccessibilityEvent",
    "res/layout/dialog_ask_permission.xml、res/layout/activity_guide_setting.xml、res/xml/accessibility_service_config.xml、res/values/strings.xml(accessibility_service_description)"
  ]
}
```

**补充说明与边界**：`activity_guide_setting.xml` 顶部警告条引用 `@string/find_and_grant`，其逐字文本未在本次静态读取中直接确认（已在 `verbatim_texts` 中如实标注）；GuildPermissionActivity 使用的资源 id 2131951651 / 2131951653 与 `accessibility_setting_permission` 的对应关系基于上下文推断，未做 public.xml 逐条比对。本次为高效率定向审计，未执行动态验证，`atsFull` 实际下发与否未观测。

</details>
