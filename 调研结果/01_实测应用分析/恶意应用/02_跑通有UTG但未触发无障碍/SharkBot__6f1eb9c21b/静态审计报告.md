# MB_078__6f1eb9c21b｜SharkBot — Phone AID, Cleaner, Booster

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：198.3s

## 1. 一句话核心结论

- **核心申请方式**：以清理工具为外壳，在“高级保护”入口同时跳系统无障碍设置并压栈全屏半透明遮罩页，用指向手势图标与“Find <应用名> and grant <权限>”及“Grant Now”单按钮弹窗，将无障碍权限包装成清理加速收益并教用户忽略系统警告。
- **静态可见性说明**：引导链（跳转点、遮罩 Activity、布局、文案、无障碍配置与描述）全部静态可读，无加壳/加密/DEX 动态加载；唯一不可静态确认的是无障碍服务在 Manifest 中未声明 BIND_ACCESSIBILITY_SERVICE，实际可启用对象需运行期核对是否动态注册。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6f1eb9c21b026eecfd65459ec4cffe3954d24619010741e18722108d7bacf3d1` |
| 包名 / 年份 | `com.sidalistudio.developer.app` / 2022 |
| 家族 / 品类 | **SharkBot**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Phone AID, Cleaner, Booster |
| 引导页宣称品牌/身份 | Super Cleaner / Clean master（清理加速、深度清垃圾、休眠耗电应用） |
| 系统无障碍列表服务名 | 未在 Manifest 声明无障碍服务项（res/xml/accessibility_service_config.xml 与类 e.n.a.h.d 存在但未挂载），系统无障碍列表预期不显示该应用条目 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：同一应用内并存三个身份：桌面名“Phone AID, Cleaner, Booster”、无障碍描述自称“Super Cleaner”“Clean master”；文案含“Accessiblility”“warinings”“orther”等拼写错误说明为手工拼装诱导页；Manifest 内混入 com.security.applock.*、com.testapp.duplicatefileremover.* 两套第三方包名组件（多 Activity 复用同一引导页），加大组件归属混淆 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sidalistudio.developer.app.screen.splash.SplashActivity（LAUNCHER）→ MainActivity | onCreate（点击桌面图标） | 原生Activity | **原文**：无（冷启动路径未见无障碍引导弹窗）<br>**译注**：无 | 无，直接进入主界面 | `com.sidalistudio.developer.app.screen.splash.SplashActivity / screen.main.MainActivity` |
| 2 | 业务功能触发 | 高级保护开关（FragmentAdvancedProtection 菜单项） | 用户点击“Advanced protection”菜单项 → com.security.applock.widget.MenuFunction$b.onClick → e.n.a.k.d.onClick → e.n.a.i.h.e#a | 原生Activity | **原文**：Advanced protection<br>**译注**：高级保护（诱导用户主动点击以获得“更强防护”） | 点击开关；此时应用先检测无障碍服务是否已启用，未启用即进入下一步 | `e.n.a.i.h.e#a` |
| 3 | 引导说明页 | com.security.applock.ui.guildPermission.GuildPermissionActivity（android:theme=@style/Theme.Transparent，excludeFromRecents） | GuildPermissionActivity.g0(ctx, "android.settings.ACCESSIBILITY_SETTINGS") 在跳设置之后立即 startActivity 压栈 | 原生Activity | **原文**：Find %s and grant %s  →  实际渲染为 Find Phone AID, Cleaner, Booster and grant accessibility permission<br>**译注**：“找到『Phone AID, Cleaner, Booster』并授予无障碍权限”，配合警示图标、应用图标与右下角手指指向图标 | 按手指指引到系统设置页找到本应用并打开开关；右上角 ic_close 可关闭（有跳过出口） | `com.security.applock.ui.guildPermission.GuildPermissionActivity#g0；res/layout/activity_guide_setting.xml；res/values/strings.xml#L214 (find_and_grant)` |
| 4 | 跳受限设置 | 系统设置：android.settings.ACCESSIBILITY_SETTINGS（requestCode 1111） | startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1111) | 系统无障碍页 | **原文**：无（应用侧不注入内容）<br>**译注**：系统无障碍服务列表页 | 在系统列表中找到该应用并打开无障碍开关（该 build 未声明服务，实际列表中预期无本应用条目） | `e.n.a.i.b#a；e.n.a.i.h.e#a；com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity#onCreate` |
| 5 | 引导说明页 | com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity（另一套同功能引导页，包名 com.sidalistudio 侧） | GuildPermissionActivity.f0(ctx, "android.settings.ACCESSIBILITY_SETTINGS")；onCreate 依 intent 的 permission name 选择文案 | 原生Activity | **原文**：Find %s and grant %s  →  Find Phone AID, Cleaner, Booster and grant accessibility permission<br>**译注**：同上前一步：指引用户到系统设置授予无障碍 | 点击底部按钮跳系统设置（findViewById(2131362105) / findViewById(2131362183) 两个点击区） | `com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity#onCreate / #f0` |
| 6 | 遮罩叠层指引 | DialogAskPermission（BaseDialogFragment） | M0(Bundle) → inflate dialog_ask_permission → Q0() 依 s0 选文案 | 原生Dialog | **原文**：Permission Needed / Grant App Usage Permission for a comprehensive phone scan effect / Grant Now（配 Lottie robo_permission.json 循环动画）<br>**译注**：“需要权限”/“授予应用使用权限以获得全面的手机扫描效果”/“立即授予”，仅有“Grant Now”一个按钮，无取消 | 点击“Grant Now”跳转系统设置授权；本弹窗无取消/跳过按钮 | `com.sidalistudio.developer.app.dialog.DialogAskPermission#M0 / #Q0；res/layout/dialog_ask_permission.xml；res/values/strings.xml#L232,L472,L233` |
| 7 | 拒权反馈循环 | GuildPermissionActivity（onResume 未重写）与入口开关回调 | 用户从系统设置返回或点 ic_close 关闭遮罩；未获权状态下再次点击“高级保护”会重新走 e.n.a.i.h.e#a 分支 | 原生Activity | **原文**：无（未见重跳提示文案）<br>**译注**：无自动死循环重跳；但入口每次点击都会再次拉起跳设置 + 遮罩 | 可退出；再次触发入口会重复引导 | `com.security.applock.ui.guildPermission.GuildPermissionActivity#onCreate（无 onResume）；e.n.a.i.h.e#a` |
| 8 | 获权后动作 | e.n.a.h.d（AccessibilityService 实现）→ com.security.applock.service.AntiTheftService | onAccessibilityEvent(event) → c.c(this).a() 判定后 c.c(this).e(AntiTheftService.class) 拉起保活服务 | 不可静态还原 | 无 | 无需用户操作 | `e.n.a.h.d#onAccessibilityEvent；res/xml/accessibility_service_config.xml（typeAllMask、canRetrieveWindowContent=true、notificationTimeout=50）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表项描述：res/xml/accessibility_service_config.xml 的 android:description → res/values/strings.xml#L40-L47（自称 Super Cleaner/Clean master，明示“需接受系统警告”）
- 全屏半透明遮罩引导页：res/layout/activity_guide_setting.xml（背景 #66000000）+ res/values/strings.xml#L214 find_and_grant，承载于 com.security.applock.ui.guildPermission.GuildPermissionActivity 与 com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity
- 不可取消型权限弹窗：res/layout/dialog_ask_permission.xml（Permission Needed / Grant App Usage Permission… / Grant Now + Lottie robo_permission.json），由 DialogAskPermission#Q0 按 action 选择 accessibility_setting_permission 文案
- 开关旁的功能说明文案：res/values/strings.xml#L140（Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%）
- 跳系统设置后的同栈遮罩：跳转 ACCESSIBILITY_SETTINGS 后立即压栈的透明 Activity，用户返回设置页时仍看到指向手势层
- 应用详情页引导：e.n.a.i.h.c#call 与 e.o.a.a.a.b.j$b#onClick 以 package: 数据跳 android.settings.APPLICATION_DETAILS_SETTINGS（受限设置场景常规引导，具体文案未取到）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. | 点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾；休眠耗电应用。启用无障碍服务时你将不得不接受 Android 系统警告。Clean master 不会将这些权限用于此处列明之外的任何其他目的。 | `res/values/strings.xml#L40-L47（accessibility_service_description，被 res/xml/accessibility_service_config.xml 引用）` | 清理工具伪装 |
| en | Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50% | 请授予无障碍权限以关闭以下自启动应用。加速效果可提升 50%。 | `res/values/strings.xml#L140（content_permission_1）` | 清理工具伪装 |
| en | Find %s and grant %s | 找到 %s 并授予 %s（实际渲染：找到“Phone AID, Cleaner, Booster”并授予“无障碍权限”） | `res/values/strings.xml#L214（find_and_grant，用于 res/layout/activity_guide_setting.xml 的 tv_content）` | 受限设置分步教学 |
| en | Permission Needed | 需要权限 | `res/values/strings.xml#L472（permission_needed，用于 dialog_ask_permission.xml tv_title）` | 清理工具伪装 |
| en | Grant App Usage Permission for a comprehensive phone scan effect | 授予应用使用权限以获得全面的手机扫描效果 | `res/values/strings.xml#L232（grant_app_permission，用于 dialog_ask_permission.xml tv_content）` | 清理工具伪装 |
| en | Grant Now | 立即授予 | `res/values/strings.xml#L233（grant_now，dialog_ask_permission.xml 唯一按钮 tv_action_1）` | 受限设置分步教学 |
| en | Grant permission to use accessibility service | 授予使用无障碍服务的权限 | `res/values/strings.xml#L48（accessibility_setting_permission，DialogAskPermission#Q0 无障碍分支 / GuildPermissionActivity#onCreate）` | 受限设置分步教学 |
| en | Advanced protection | 高级保护 | `res/values/strings.xml#L62（advanced_protection），入口由 e.n.a.i.h.e#a 处理` | 假反诈安全 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无 onResume 死循环、无定时器重跳：GuildPermissionActivity 未重写 onResume，遮罩页右上角 ic_close 可退出；但权限弹窗 DialogAskPermission 仅有 Grant Now 单一出口，无取消；用户每次再点“高级保护”入口即重新拉起“跳系统设置 + 压栈遮罩”，形成被动重复引导。
- **遮罩叠层 / 高仿系统设置页**：存在遮罩叠层但非高仿系统开关页：activity_guide_setting.xml 为全屏 #66000000 半透明层，含 ic_warning 警示图标、应用 logo + app_name、右下角 pointing_hand 手指指向图标，正文为 find_and_grant；该 Activity 以 android:theme=@style/Theme.Transparent + excludeFromRecents 压栈于系统设置之上。
- **Android 13+ 受限设置（Restricted Settings）应对**：存在跳 android.settings.APPLICATION_DETAILS_SETTINGS（data=package:<包名>）的代码路径（e.n.a.i.h.c#call、e.o.a.a.a.b.j$b#onClick），属 13+ 受限设置场景的应用详情页引导；未取到“点右上角菜单允许受限设置”的逐字文案，Session 安装器绕过逻辑本次未展开。
- **获权后即时行为与防撤权机制**：未发现获权后自点确认、自授权或 GLOBAL_ACTION_BACK/HOME 阻止撤权；获权后 onAccessibilityEvent 仅拉起 AntiTheftService 保活（e.n.a.h.d#onAccessibilityEvent）。
- **良性降级 / 替代方案**：无。跳转与遮罩均以“获得权限”为唯一目标，未提供手动模式、仅观看或功能降级替代路径；且 Manifest 未声明无障碍服务，引导页指向的开关对象在系统列表中预期不存在，不构成良性降级。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity/startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS（本样本 requestCode=1111）或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间即拉起 UTG；次优时机为用户点击“Advanced protection”菜单项后 800ms 内。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无静态加壳阻挡（静态加壳不影响运行期 UTG）。真实盲区为：Manifest 未声明无障碍服务，若该服务由运行期动态组件注册，则无障碍列表与获权后自动化行为无法仅凭静态或单次 UTG 捕获；另获权后动作（模拟点击、窗口内容读取）在纯页面截图中不可见，需配合事件与流量观测。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳设置后压栈的全屏半透明遮罩引导页** | com.security.applock.ui.guildPermission.GuildPermissionActivity / com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity，Theme.Transparent，#66000000 背景 + 手指图标 + ic_close | 该层是“分步教学 + 指向手势”的直接物证，且与系统设置页同栈，可证明引导与跳转是同步设计的成套动作而非单次系统弹窗 | TextView 文本匹配 Find .* and grant .*；drawable pointing_hand 手势图标节点；activity 名含 guildPermission 且窗口背景为半透明；同栈存在系统设置 Activity |
| **单按钮权限弹窗页** | DialogAskPermission，标题 Permission Needed，正文 Grant App Usage Permission for a comprehensive phone scan effect，唯一按钮 Grant Now，含 LottieAnimationView | 无取消按钮 + 清理扫描话术 + 动画伪装，是“不可拒绝型诱导”与“权限收益错配”的直接证据 | 存在 LottieAnimationView（robo_permission.json）；按钮集合中仅存在 Grant Now，无 Cancel/Skip/Not now；文本 Permission Needed 与 accessibility 语义无直接对应 |
| **系统无障碍服务列表项** | 系统 Settings 无障碍页（预期无本应用条目） | 验证“引导目标与真实可启用对象是否一致”——该 build 未声明 BIND_ACCESSIBILITY_SERVICE，列表缺项可证明指向对象不存在，是欺骗性引导的关键判别点 | 列表中存在与 app_name 匹配的服务条目；列表条目描述包含 Super Cleaner / Clean master 或 Accessiblility；列表未出现该应用条目（缺项即为异常引导） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `e.n.a.i.h.e#a`
- `e.n.a.i.b#a`
- `com.security.applock.ui.guildPermission.GuildPermissionActivity#g0`
- `com.sidalistudio.developer.app.dialog.DialogAskPermission#Q0`
- `res/layout/activity_guide_setting.xml`
- `res/values/strings.xml#L40-L47`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**整体判断：这是一条完整的“运行期 UTG 分步引导”链，并非良性透明说明。** 该样本以清理工具身份作为外壳，在“高级保护”入口被触发后，同时执行**跳转系统无障碍设置页**和**压栈全屏半透明引导遮罩页**这两个动作，并用 Lottie 动画弹窗和指向手势图标指示用户到设置页里找到本应用、打开开关。

关键事实：

1. **触发时机是业务功能按需触发，而非冷启动**：冷启动走 [SplashActivity](<resource-unit:#1.dex1 code:com.sidalistudio.developer.app.screen.splash.SplashActivity>) → `MainActivity`，未在冷启动路径上发现无障碍弹窗；真正入口是“Advanced protection”开关回调 [e.n.a.i.h.e#a](<resource-unit:#1.dex1 code:e.n.a.i.h.e#a>)。

2. **双动作同步发起**：同一回调内先 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1111)`，随后立即 `GuildPermissionActivity.g0(...)` 压栈引导页（[e.n.a.i.b#a](<resource-unit:#1.dex1 code:e.n.a.i.b#a>)）。用户从系统设置返回时，看到的是压在栈上的遮罩指引页。

3. **遮罩页不是高仿设置页，而是“手指指向”教学层**：[activity_guide_setting.xml](<resource-unit:#1 file:res/layout/activity_guide_setting.xml>) 为全屏 `#66000000` 半透明背景，右上角 `ic_close`、`ic_warning` 警示图标、应用 logo + `app_name` 文本、右下角 `pointing_hand` 手势图标，正文取 [find_and_grant](<resource-unit:#1 file:res/values/strings.xml#L214>) = `"Find %s and grant %s"`（填入应用名与 `accessibility permission`）。

4. **话术把无障碍与清理收益绑定，并明确教用户忽略系统警告**：[strings.xml#L40-L47](<resource-unit:#1 file:res/values/strings.xml#L40-L47>) 自称 “Super Cleaner”/“Clean master”，写 “Deep clean hidden junk / Hibernate draining apps”，并要求 “You will have to accept Android system warinings when enabling Accessibility service”；[#L140](<resource-unit:#1 file:res/values/strings.xml#L140>) 写 “Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%”。

5. **权限弹窗**：[DialogAskPermission#Q0](<resource-unit:#1.dex1 code:com.sidalistudio.developer.app.dialog.DialogAskPermission#Q0>) 按 action 选文案，无障碍分支用 `accessibility_setting_permission`（“Grant permission to use accessibility service”）；[dialog_ask_permission.xml](<resource-unit:#1 file:res/layout/dialog_ask_permission.xml>) 用 Lottie `robo_permission.json` + “Permission Needed” + “Grant App Usage Permission for a comprehensive phone scan effect” + 唯一按钮 “Grant Now”（**无取消按钮**）。

6. **身份三重错位**：桌面名/`app_name` = “Phone AID, Cleaner, Booster”，无障碍描述品牌 = “Super Cleaner” / “Clean master”，且存在 “Accessiblility”“warinings”“orther” 等拼写错误，说明文案是手工拼装的诱导页而非正规产品说明。

7. **重要覆盖边界**：Manifest **未声明** 任何 `BIND_ACCESSIBILITY_SERVICE` 服务项（`res/xml/accessibility_service_config.xml` 与代码类 `e.n.a.h.d` 均存在但未挂载），因此本 build 中系统无障碍列表里实际不会出现该服务条目。引导页的指向目标与真实可启用对象不一致，这本身加重了欺骗性，但需运行期核对是否有动态组件注册。已获权后逻辑仅见 [e.n.a.h.d#onAccessibilityEvent](<resource-unit:#1.dex1 code:e.n.a.h.d#onAccessibilityEvent>) 拉起 `AntiTheftService` 保活。

8. **受限设置引导存在但未闭环**：发现 `APPLICATION_DETAILS_SETTINGS` 跳转（[e.n.a.i.h.c#call](<resource-unit:#1.dex1 code:e.n.a.i.h.c#call>)），属 13+ 受限设置场景的常规引导手法，但本次未取到“点右上角菜单允许受限设置”的逐字文案。

9. **拒权无死循环**：`GuildPermissionActivity` 未重写 `onResume`，遮罩页有 `ic_close` 可退出；但权限弹窗仅 “Grant Now” 一个出口，属“单侧出口”强制型，而非死循环重跳。

已登记风险 **R-001**（high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链（跳转点、遮罩 Activity、布局、文案、无障碍配置与描述）全部静态可读，无加壳/加密/DEX 动态加载；唯一不可静态确认的是无障碍服务在 Manifest 中未声明 BIND_ACCESSIBILITY_SERVICE，实际可启用对象需运行期核对是否动态注册。",
  "summary_one_liner": "以清理工具为外壳，在“高级保护”入口同时跳系统无障碍设置并压栈全屏半透明遮罩页，用指向手势图标与“Find <应用名> and grant <权限>”及“Grant Now”单按钮弹窗，将无障碍权限包装成清理加速收益并教用户忽略系统警告。",
  "disguise_identity": {
    "app_display_name": "Phone AID, Cleaner, Booster",
    "claimed_brand_or_persona": "Super Cleaner / Clean master（清理加速、深度清垃圾、休眠耗电应用）",
    "a11y_service_label": "未在 Manifest 声明无障碍服务项（res/xml/accessibility_service_config.xml 与类 e.n.a.h.d 存在但未挂载），系统无障碍列表预期不显示该应用条目",
    "identity_mismatch": true,
    "obfuscation_tricks": "同一应用内并存三个身份：桌面名“Phone AID, Cleaner, Booster”、无障碍描述自称“Super Cleaner”“Clean master”；文案含“Accessiblility”“warinings”“orther”等拼写错误说明为手工拼装诱导页；Manifest 内混入 com.security.applock.*、com.testapp.duplicatefileremover.* 两套第三方包名组件（多 Activity 复用同一引导页），加大组件归属混淆"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sidalistudio.developer.app.screen.splash.SplashActivity（LAUNCHER）→ MainActivity",
      "trigger_event": "onCreate（点击桌面图标）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（冷启动路径未见无障碍引导弹窗）",
      "shown_text_zh": "无",
      "user_action_requested": "无，直接进入主界面",
      "code_anchor": "com.sidalistudio.developer.app.screen.splash.SplashActivity / screen.main.MainActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "高级保护开关（FragmentAdvancedProtection 菜单项）",
      "trigger_event": "用户点击“Advanced protection”菜单项 → com.security.applock.widget.MenuFunction$b.onClick → e.n.a.k.d.onClick → e.n.a.i.h.e#a",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Advanced protection",
      "shown_text_zh": "高级保护（诱导用户主动点击以获得“更强防护”）",
      "user_action_requested": "点击开关；此时应用先检测无障碍服务是否已启用，未启用即进入下一步",
      "code_anchor": "e.n.a.i.h.e#a"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.security.applock.ui.guildPermission.GuildPermissionActivity（android:theme=@style/Theme.Transparent，excludeFromRecents）",
      "trigger_event": "GuildPermissionActivity.g0(ctx, \"android.settings.ACCESSIBILITY_SETTINGS\") 在跳设置之后立即 startActivity 压栈",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Find %s and grant %s  →  实际渲染为 Find Phone AID, Cleaner, Booster and grant accessibility permission",
      "shown_text_zh": "“找到『Phone AID, Cleaner, Booster』并授予无障碍权限”，配合警示图标、应用图标与右下角手指指向图标",
      "user_action_requested": "按手指指引到系统设置页找到本应用并打开开关；右上角 ic_close 可关闭（有跳过出口）",
      "code_anchor": "com.security.applock.ui.guildPermission.GuildPermissionActivity#g0；res/layout/activity_guide_setting.xml；res/values/strings.xml#L214 (find_and_grant)"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置：android.settings.ACCESSIBILITY_SETTINGS（requestCode 1111）",
      "trigger_event": "startActivityForResult(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), 1111)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧不注入内容）",
      "shown_text_zh": "系统无障碍服务列表页",
      "user_action_requested": "在系统列表中找到该应用并打开无障碍开关（该 build 未声明服务，实际列表中预期无本应用条目）",
      "code_anchor": "e.n.a.i.b#a；e.n.a.i.h.e#a；com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity#onCreate"
    },
    {
      "step": 5,
      "stage": "引导说明页",
      "screen_or_component": "com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity（另一套同功能引导页，包名 com.sidalistudio 侧）",
      "trigger_event": "GuildPermissionActivity.f0(ctx, \"android.settings.ACCESSIBILITY_SETTINGS\")；onCreate 依 intent 的 permission name 选择文案",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Find %s and grant %s  →  Find Phone AID, Cleaner, Booster and grant accessibility permission",
      "shown_text_zh": "同上前一步：指引用户到系统设置授予无障碍",
      "user_action_requested": "点击底部按钮跳系统设置（findViewById(2131362105) / findViewById(2131362183) 两个点击区）",
      "code_anchor": "com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity#onCreate / #f0"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "DialogAskPermission（BaseDialogFragment）",
      "trigger_event": "M0(Bundle) → inflate dialog_ask_permission → Q0() 依 s0 选文案",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission Needed / Grant App Usage Permission for a comprehensive phone scan effect / Grant Now（配 Lottie robo_permission.json 循环动画）",
      "shown_text_zh": "“需要权限”/“授予应用使用权限以获得全面的手机扫描效果”/“立即授予”，仅有“Grant Now”一个按钮，无取消",
      "user_action_requested": "点击“Grant Now”跳转系统设置授权；本弹窗无取消/跳过按钮",
      "code_anchor": "com.sidalistudio.developer.app.dialog.DialogAskPermission#M0 / #Q0；res/layout/dialog_ask_permission.xml；res/values/strings.xml#L232,L472,L233"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "GuildPermissionActivity（onResume 未重写）与入口开关回调",
      "trigger_event": "用户从系统设置返回或点 ic_close 关闭遮罩；未获权状态下再次点击“高级保护”会重新走 e.n.a.i.h.e#a 分支",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（未见重跳提示文案）",
      "shown_text_zh": "无自动死循环重跳；但入口每次点击都会再次拉起跳设置 + 遮罩",
      "user_action_requested": "可退出；再次触发入口会重复引导",
      "code_anchor": "com.security.applock.ui.guildPermission.GuildPermissionActivity#onCreate（无 onResume）；e.n.a.i.h.e#a"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "e.n.a.h.d（AccessibilityService 实现）→ com.security.applock.service.AntiTheftService",
      "trigger_event": "onAccessibilityEvent(event) → c.c(this).a() 判定后 c.c(this).e(AntiTheftService.class) 拉起保活服务",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后以无障碍事件驱动自身服务保活；后续自动化动作（模拟点击等）不在本链可见范围",
      "user_action_requested": "无需用户操作",
      "code_anchor": "e.n.a.h.d#onAccessibilityEvent；res/xml/accessibility_service_config.xml（typeAllMask、canRetrieveWindowContent=true、notificationTimeout=50）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表项描述：res/xml/accessibility_service_config.xml 的 android:description → res/values/strings.xml#L40-L47（自称 Super Cleaner/Clean master，明示“需接受系统警告”）",
    "全屏半透明遮罩引导页：res/layout/activity_guide_setting.xml（背景 #66000000）+ res/values/strings.xml#L214 find_and_grant，承载于 com.security.applock.ui.guildPermission.GuildPermissionActivity 与 com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity",
    "不可取消型权限弹窗：res/layout/dialog_ask_permission.xml（Permission Needed / Grant App Usage Permission… / Grant Now + Lottie robo_permission.json），由 DialogAskPermission#Q0 按 action 选择 accessibility_setting_permission 文案",
    "开关旁的功能说明文案：res/values/strings.xml#L140（Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%）",
    "跳系统设置后的同栈遮罩：跳转 ACCESSIBILITY_SETTINGS 后立即压栈的透明 Activity，用户返回设置页时仍看到指向手势层",
    "应用详情页引导：e.n.a.i.h.c#call 与 e.o.a.a.a.b.j$b#onClick 以 package: 数据跳 android.settings.APPLICATION_DETAILS_SETTINGS（受限设置场景常规引导，具体文案未取到）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "text_zh": "点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾；休眠耗电应用。启用无障碍服务时你将不得不接受 Android 系统警告。Clean master 不会将这些权限用于此处列明之外的任何其他目的。",
      "source_location": "res/values/strings.xml#L40-L47（accessibility_service_description，被 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%",
      "text_zh": "请授予无障碍权限以关闭以下自启动应用。加速效果可提升 50%。",
      "source_location": "res/values/strings.xml#L140（content_permission_1）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Find %s and grant %s",
      "text_zh": "找到 %s 并授予 %s（实际渲染：找到“Phone AID, Cleaner, Booster”并授予“无障碍权限”）",
      "source_location": "res/values/strings.xml#L214（find_and_grant，用于 res/layout/activity_guide_setting.xml 的 tv_content）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Permission Needed",
      "text_zh": "需要权限",
      "source_location": "res/values/strings.xml#L472（permission_needed，用于 dialog_ask_permission.xml tv_title）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant App Usage Permission for a comprehensive phone scan effect",
      "text_zh": "授予应用使用权限以获得全面的手机扫描效果",
      "source_location": "res/values/strings.xml#L232（grant_app_permission，用于 dialog_ask_permission.xml tv_content）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant Now",
      "text_zh": "立即授予",
      "source_location": "res/values/strings.xml#L233（grant_now，dialog_ask_permission.xml 唯一按钮 tv_action_1）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant permission to use accessibility service",
      "text_zh": "授予使用无障碍服务的权限",
      "source_location": "res/values/strings.xml#L48（accessibility_setting_permission，DialogAskPermission#Q0 无障碍分支 / GuildPermissionActivity#onCreate）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Advanced protection",
      "text_zh": "高级保护",
      "source_location": "res/values/strings.xml#L62（advanced_protection），入口由 e.n.a.i.h.e#a 处理",
      "rhetorical_frame": "假反诈安全"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无 onResume 死循环、无定时器重跳：GuildPermissionActivity 未重写 onResume，遮罩页右上角 ic_close 可退出；但权限弹窗 DialogAskPermission 仅有 Grant Now 单一出口，无取消；用户每次再点“高级保护”入口即重新拉起“跳系统设置 + 压栈遮罩”，形成被动重复引导。",
    "overlay_or_fake_settings": "存在遮罩叠层但非高仿系统开关页：activity_guide_setting.xml 为全屏 #66000000 半透明层，含 ic_warning 警示图标、应用 logo + app_name、右下角 pointing_hand 手指指向图标，正文为 find_and_grant；该 Activity 以 android:theme=@style/Theme.Transparent + excludeFromRecents 压栈于系统设置之上。",
    "restricted_settings_13plus_coaching": "存在跳 android.settings.APPLICATION_DETAILS_SETTINGS（data=package:<包名>）的代码路径（e.n.a.i.h.c#call、e.o.a.a.a.b.j$b#onClick），属 13+ 受限设置场景的应用详情页引导；未取到“点右上角菜单允许受限设置”的逐字文案，Session 安装器绕过逻辑本次未展开。",
    "post_grant_anti_removal": "未发现获权后自点确认、自授权或 GLOBAL_ACTION_BACK/HOME 阻止撤权；获权后 onAccessibilityEvent 仅拉起 AntiTheftService 保活（e.n.a.h.d#onAccessibilityEvent）。",
    "benign_graceful_degradation": "无。跳转与遮罩均以“获得权限”为唯一目标，未提供手动模式、仅观看或功能降级替代路径；且 Manifest 未声明无障碍服务，引导页指向的开关对象在系统列表中预期不存在，不构成良性降级。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity/startActivityForResult 目标为 android.settings.ACCESSIBILITY_SETTINGS（本样本 requestCode=1111）或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间即拉起 UTG；次优时机为用户点击“Advanced protection”菜单项后 800ms 内。",
    "key_pages_to_capture": [
      {
        "page_role": "跳设置后压栈的全屏半透明遮罩引导页",
        "page_identifier": "com.security.applock.ui.guildPermission.GuildPermissionActivity / com.sidalistudio.developer.app.screen.guildPermission.GuildPermissionActivity，Theme.Transparent，#66000000 背景 + 手指图标 + ic_close",
        "why_most_useful": "该层是“分步教学 + 指向手势”的直接物证，且与系统设置页同栈，可证明引导与跳转是同步设计的成套动作而非单次系统弹窗",
        "observable_utg_signals": ["TextView 文本匹配 Find .* and grant .*", "drawable pointing_hand 手势图标节点", "activity 名含 guildPermission 且窗口背景为半透明", "同栈存在系统设置 Activity"]
      },
      {
        "page_role": "单按钮权限弹窗页",
        "page_identifier": "DialogAskPermission，标题 Permission Needed，正文 Grant App Usage Permission for a comprehensive phone scan effect，唯一按钮 Grant Now，含 LottieAnimationView",
        "why_most_useful": "无取消按钮 + 清理扫描话术 + 动画伪装，是“不可拒绝型诱导”与“权限收益错配”的直接证据",
        "observable_utg_signals": ["存在 LottieAnimationView（robo_permission.json）", "按钮集合中仅存在 Grant Now，无 Cancel/Skip/Not now", "文本 Permission Needed 与 accessibility 语义无直接对应"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页（预期无本应用条目）",
        "why_most_useful": "验证“引导目标与真实可启用对象是否一致”——该 build 未声明 BIND_ACCESSIBILITY_SERVICE，列表缺项可证明指向对象不存在，是欺骗性引导的关键判别点",
        "observable_utg_signals": ["列表中存在与 app_name 匹配的服务条目", "列表条目描述包含 Super Cleaner / Clean master 或 Accessiblility", "列表未出现该应用条目（缺项即为异常引导）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无静态加壳阻挡（静态加壳不影响运行期 UTG）。真实盲区为：Manifest 未声明无障碍服务，若该服务由运行期动态组件注册，则无障碍列表与获权后自动化行为无法仅凭静态或单次 UTG 捕获；另获权后动作（模拟点击、窗口内容读取）在纯页面截图中不可见，需配合事件与流量观测。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE"
  ],
  "code_anchors": [
    "e.n.a.i.h.e#a",
    "e.n.a.i.b#a",
    "com.security.applock.ui.guildPermission.GuildPermissionActivity#g0",
    "com.sidalistudio.developer.app.dialog.DialogAskPermission#Q0",
    "res/layout/activity_guide_setting.xml",
    "res/values/strings.xml#L40-L47"
  ]
}
```

</details>
