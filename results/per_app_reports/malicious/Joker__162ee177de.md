# MR_148__162ee177de｜Joker — Antivirus Security

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：154.0s

## 1. 一句话核心结论

- **核心申请方式**：以“延长电池续航、绝不收集个人信息”话术包装 ★★Antivirus Security★★ 无障碍服务，用底部仿系统已开启开关浮层配合业务页红点引导跳转系统无障碍列表，并在用户返回后由 2.5 秒定时器判定仍停留在设置页即自动重跳，形成无取消入口的拒权循环。
- **静态可见性说明**：无障碍引导主链路（服务声明与标签/描述、accessibility_config、PermissionGuideActivity 仿开关浮层、SecurityLevelActivity 跳 ACCESSIBILITY_SETTINGS、us.a 跳 APPLICATION_DETAILS_SETTINGS + 2500ms 定时器重跳判定）全部静态可见，未见加壳或密文动态加载；仅 onAccessibilityEvent 中获权后自动点击的具体目标集合未逐条穷举，以及资源 accessibility_message 未见代码引用点。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `162ee177dea9b94366063de63dffd97f92f7a50e0e429d54fea73dc3a52f1b3a` |
| 包名 / 年份 | `com.anti.mysecurity` / 2019 |
| 家族 / 品类 | **Joker**（同池样本数：4） |
| 原始来源标识 | https://medium.com/csis-techblog/analysis-of-joker-a-spy-premium-subscription-bot-on-googleplay-9ad24f044451 |
| 桌面显示名 | Antivirus Security |
| 引导页宣称品牌/身份 | Antivirus Security（伪装的杀毒/电池优化工具品牌，无障碍标签加 ★★ 装饰） |
| 系统无障碍列表服务名 | ★★Antivirus Security★★ |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 用 ★★ 星号包裹以在系统服务列表中视觉突出；android:description 声称仅用于电池优化并预先要求“若收到隐私警告请忽略”，与配置中 typeAllMask + canRetrieveWindowContent=true 的全局监听能力不符；PermissionGuideActivity 用 clickable=false 且 checked=true 的 SwitchCompat 伪造“权限已开启”状态，并叠加手指点击指引图模拟系统设置页；引导浮层无取消/跳过按钮，仅整屏连点两次或 4 秒超时自动关闭。 |
| 无障碍服务类名 | `com.bs.common.ui.service.BaseAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Enabling this option will help Antivirus shut down applications to extend the life of your battery.<br><br> Antivirus uses the accessibility service to optimize your device only. We will never use it to collect your personal information. If you have received a privacy warning, please ignore it. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.bs.antivirus.ui.welcome.WelcomeActivity（LAUNCHER）→ com.bs.antivirus.ui.main.activity.MainActivity | 点击桌面图标冷启动，WelcomeActivity 完成引导后进入 MainActivity | 原生Activity | **原文**：Terms of Service / Accept and continue<br>**译注**：服务条款 / 接受并继续 | 点击“Accept and continue”接受条款后进入主界面（该步为通用入口，不直接申请无障碍） | `AndroidManifest.xml activity WelcomeActivity / com.bs.antivirus.ui.welcome.WelcomeActivity` |
| 2 | 业务功能触发 | com.bs.junkclean.ui.activity.JunkCleanActivity / com.bs.batterysaver.BatterySaverActivity / com.bs.applock.ui.fragment.AppLockFragment | 用户点击垃圾清理、电池省电、应用锁等按钮，功能流程内调用 PermissionGuideActivity.a(ctx, new PermissionGuideResourceBean(R$string.permission_guide_accessibility, R$string.accessibility_label)) | 原生Dialog | **原文**：Enable Antivirus to close auto-starting apps.<br>**译注**：启用 Antivirus 以关闭自动启动的应用。 | 无明确按钮；用户只能点击浮层任意位置（连续两次关闭）或等待 4 秒自动消失 | `com.bs.junkclean.ui.activity.JunkCleanActivity$4#a → com.bs.common.ui.PermissionGuideActivity#a(Context, PermissionGuideResourceBean)` |
| 3 | 引导说明页（仿系统开关） | com.bs.common.ui.PermissionGuideActivity，布局 res/layout/activity_permission_guide.xml | Activity onCreate 经 SimpleActivity → PermissionGuideActivity.a(Bundle)：取 Intent 中的 PermissionGuideResourceBean 设置 tv_title/tv_name，并 tv_title.postDelayed(new tj(this), 4000L) | 原生Activity | **原文**：Enable Antivirus to close auto-starting apps. ／ 应用名 Antivirus Security + 一个 checked=true、clickable=false、rotation=180 的开关 + 手指点击指引图<br>**译注**：启用 Antivirus 以关闭自动启动的应用；浮层内展示应用图标、应用名与一个看似“已开启”且不可点击的开关，并配手指点击引导图 | 无“开启/取消/跳过”按钮，开关不可操作；点击整屏仅计数（fW++，≥2 时 finish），或 4 秒后自动 finish | `com.bs.common.ui.PermissionGuideActivity#a(Bundle)、#l(View)、g.c.tj#run；res/layout/activity_permission_guide.xml` |
| 4 | 跳受限设置 | com.bs.antivirus.ui.main.activity.SecurityLevelActivity 列表项“Accessibility”（未开启显示红点）→ 系统 android.settings.ACCESSIBILITY_SETTINGS | 用户点击 SecurityLevelBodayItem 的 case 4 项（SecurityLevelActivity.b(int,int)），或安全等级页通过 g.c.ev.a() 用 us.i() 判定未开启而显示该项 | 系统无障碍页 | **原文**：Accessibility ／ Close auto-starting , battery draining apps in order to extend your battery life.<br>**译注**：无障碍 ／ 关闭自动启动、耗电的应用以延长电池续航。 | 用户在系统无障碍列表中找到 “★★Antivirus Security★★” 并手动打开开关；跳转前应用未提供任何权限用途说明页 | `com.bs.antivirus.ui.main.activity.SecurityLevelActivity#b(int,int) → g.c.us#L(Context)；g.c.ev#a；res/values/strings.xml level_des_accessibility` |
| 5 | 拒权反馈循环 | 系统 android.settings.APPLICATION_DETAILS_SETTINGS（应用详情页）+ 应用内 CountDownTimer 判定 | g.c.us.a(String,Context,int) 跳应用详情页后 handler.post(new ut(i))；g.c.ut#run → g.c.us#q 起 hj(2500L,500L)，onFinish → g.c.us$1#bS → g.c.us#fC | 系统无障碍页 | **原文**：无（应用侧不展示文字，仅静默判定前台包名）<br>**译注**：应用在 2.5 秒后检查当前前台包名，若仍为 com.android.settings / com.miui.securitycenter / com.miui.appmanager / com.android.packageinstaller，则再次执行跳转分支 | 要求用户留在设置页完成开启；未开启即被定时器反复拉回设置页，无“稍后再说”降级路径 | `g.c.us#a(String,Context,int)、g.c.us#q(int)、g.c.us#fC()、g.c.ut#run、g.c.us$1#bS` |
| 6 | 获权后动作 | com.bs.common.ui.service.BaseAccessibilityService（onServiceConnected / onAccessibilityEvent / fi） | 用户开启服务后系统回调 onServiceConnected（eventTypes=4194336、flags=1、notificationTimeout=200），清理/加速流程注册 uu 节点操作器后进入 fi() | 不可静态还原 | 无 | 无需用户操作，服务自动读取窗口内容并模拟点击 | `com.bs.common.ui.service.BaseAccessibilityService#onServiceConnected、#fi()、#fj()；res/xml/accessibility_config.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：android:label = ★★Antivirus Security★★（res/values/strings.xml accessibility_label）
- 系统无障碍服务详情说明：android:description = accessibility_service_description（res/values/strings.xml），宣称仅用于电池优化、绝不收集个人信息、提示忽略隐私警告
- 安全等级页列表项：标题 Accessibility、描述 level_des_accessibility = “Close auto-starting , battery draining apps in order to extend your battery life.”（SecurityLevelActivity 列表，g.c.ev#a 构造）
- 业务功能触发的底部浮层：PermissionGuideActivity（res/layout/activity_permission_guide.xml），显示 permission_guide_accessibility = “Enable Antivirus to close auto-starting apps.” + 应用名 + 伪造已开启开关 + 手指指引图
- 未被代码引用的备用引导文案：res/values/strings.xml accessibility_message = “Scroll to find "%1$s" and turn it on”（资源中定义，静态未见调用点）
- 应用内统计埋点（非用户可见）：qj.a(...).k(this.aB, "启用辅助权限按钮") 记录点击无障碍引导按钮

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | ★★Antivirus Security★★ | ★★Antivirus Security★★（星号装饰的服务显示名） | `res/values/strings.xml accessibility_label` | 假反诈安全 |
| en | Enabling this option will help Antivirus shut down applications to extend the life of your battery.<br><br> Antivirus uses the accessibility service to optimize your device only. We will never use it to collect your personal information. If you have received a privacy warning, please ignore it. | 启用此选项将帮助 Antivirus 关闭应用以延长电池续航。Antivirus 仅使用无障碍服务优化您的设备。我们绝不会用它收集您的个人信息。如果您收到了隐私警告，请忽略它。 | `res/values/strings.xml accessibility_service_description（Manifest android:description）` | 教唆忽视警告 |
| en | Scroll to find "%1$s" and turn it on | 滑动找到“%1$s”并打开它 | `res/values/strings.xml accessibility_message（静态未见代码引用）` | 受限设置分步教学 |
| en | Enable Antivirus to close auto-starting apps. | 启用 Antivirus 以关闭自动启动的应用。 | `res/values/strings.xml permission_guide_accessibility（PermissionGuideActivity 标题）` | 清理工具伪装 |
| en | Close auto-starting , battery draining apps in order to extend your battery life. | 关闭自动启动、耗电的应用以延长电池续航。 | `res/values/strings.xml level_des_accessibility（SecurityLevelActivity 列表项描述）` | 清理工具伪装 |
| en | Accessibility | 无障碍 | `res/values/strings.xml accessibility` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：跳转设置页后 handler.post(new ut(i)) 启动 CountDownTimer(2500ms/500ms)，onFinish 回调 g.c.us.fC() 读取当前前台包名，若仍为 com.android.settings / com.miui.securitycenter / com.miui.appmanager / com.android.packageinstaller 则再次进入跳转分支；PermissionGuideActivity 亦无取消按钮，仅整屏连点两次或 4 秒超时自动关闭后仍会回到业务流程再次出现红点
- **遮罩叠层 / 高仿系统设置页**：PermissionGuideActivity 为应用内仿系统开关浮层：底部卡片含应用图标、应用名、clickable=false 且 checked=true 且旋转 180° 的 SwitchCompat、以及手指点击指引图，视觉上呈“权限已开启”但实际不可操作；另配置 SYSTEM_ALERT_WINDOW 权限用于清理过程悬浮进度层，未见全屏高仿系统无障碍设置页
- **Android 13+ 受限设置（Restricted Settings）应对**：无（跳转 ACCESSIBILITY_SETTINGS 为直接 Intent，未发现“进入应用详情→右上角菜单→允许受限设置”的分步教学文案或 Session 安装器绕过路径）
- **获权后即时行为与防撤权机制**：部分相关：g.c.us.fC() 对前台包名 com.android.settings / com.miui.securitycenter / com.miui.appmanager / com.android.packageinstaller 的停留状态做重跳判定，属设置页停留监控与重跳，未见 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接证据
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 Activity 启动为触发点：监测到 com.bs.common.ui.PermissionGuideActivity 启动（业务功能触发引导浮层），或监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS / android.settings.APPLICATION_DETAILS_SETTINGS（由 g.c.us.L 与 g.c.us.a 发起）时立即截图；另可在跳转后 2500ms 前后连续截屏以捕获重跳瞬间
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导浮层与列表文案均为可读文本，无纯图片诱导；但获权后 onAccessibilityEvent（1085 条指令）中的自动点击目标未逐条还原，若需判定其是否在系统设置页自动点开开关或阻止撤权，需运行期 Hook 或 UTG 连续采样；静态加壳初判为 False，运行期 UTG 不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **业务功能触发的仿系统开关引导浮层页** | com.bs.common.ui.PermissionGuideActivity，界面特征为底部绿色卡片 + 应用图标 + “Antivirus Security” + 右侧旋转的已勾选开关 + 手指点击指引图 | 该页是唯一向用户呈现“权限已开启”假象的载体，且无取消按钮、4 秒自动消失，是判定伪装与强迫式引导的最直接视觉证据 | SwitchCompat 控件 clickable=false 且 checked=true 的伪开启状态；无取消/跳过按钮的整屏可点浮层；手指点击指引图 drawable icon_permission_finger；4 秒后页面自动消失 |
| **跳转前的安全等级列表项（红点项）** | com.bs.antivirus.ui.main.activity.SecurityLevelActivity 列表中的 “Accessibility” 项及右侧红点 | 证明应用以“安全等级/未优化”红点方式施加心理压力，且点击后无任何说明直接跳系统无障碍页 | Accessibility 列表项文本；未开启时的红色角标/提示；点击后直接拉起系统无障碍设置（无中间说明页） |
| **系统无障碍服务列表项** | 系统 Settings 无障碍页中显示 “★★Antivirus Security★★” 的条目及其说明文本 | 核对 label 星号装饰与“仅用于电池优化、请忽略隐私警告”的说明是否如静态资源所述呈现，是身份伪装与告知失真的关键对照点 | 服务名 ★★Antivirus Security★★；说明文本含“we will never use it to collect your personal information / please ignore it”；开关初始为关闭状态 |
| **设置页返回/停留后的重跳瞬间** | 跳转 APPLICATION_DETAILS_SETTINGS 后约 2500ms，Activity 再次变为系统设置/无障碍页 | 直接验证拒权循环：用户未开启时是否被定时器自动拉回设置页，这是判定强迫性与审核规避的核心运行期证据 | 两次相邻截屏中前台均为 com.android.settings 系页面；无用户输入情况下 Activity 栈再次变化；PermissionGuideActivity 反复出现 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.bs.common.ui.PermissionGuideActivity#a(android.os.Bundle)`
- `com.bs.antivirus.ui.main.activity.SecurityLevelActivity#b(int,int)`
- `g.c.us#L(android.content.Context)`
- `g.c.us#a(java.lang.String, android.content.Context, int)`
- `g.c.us#fC()`
- `com.bs.common.ui.service.BaseAccessibilityService#onServiceConnected`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态核验，共 12 次工具调用）

**无障碍服务的身份伪装与文案**
- Manifest 声明 `com.bs.common.ui.service.BaseAccessibilityService`，`android:label` 取自 `strings.xml` 的 `★★Antivirus Security★★`（星号包裹以在系统无障碍列表中醒目），`android:description` 用“帮助 Antivirus 关闭应用以延长电池续航、绝不会收集个人信息、若收到隐私警告请忽略”这套话术（[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L39-L43>)）。
- [accessibility_config.xml](<resource-unit:#1 file:res/xml/accessibility_config.xml>) 实际申请 `typeAllMask` + `canRetrieveWindowContent="true"`，即全局界面事件监听与窗口内容读取，与“电池优化”宣称严重不符；`onServiceConnected` 中 `flags=1`、`notificationTimeout=200`。

**纯运行期 UTG 页面流转**
1. 业务功能触发：`JunkCleanActivity`、`BatterySaverActivity`、`AppLockFragment` 等在功能流程中调用 `PermissionGuideActivity.a(ctx, bean)` 弹出底部浮层。
2. 仿系统开关页：[PermissionGuideActivity.a(Bundle)](<resource-unit:#1.dex1 code:com.bs.common.ui.PermissionGuideActivity#a>) 载入 [activity_permission_guide.xml](<resource-unit:#1 file:res/layout/activity_permission_guide.xml>)：应用图标 + 应用名 + 一个 `clickable=false`、`checked=true`、旋转 180° 的 SwitchCompat + 手指点击指引图，伪装成“权限已开启”的系统设置样式；整屏可点但仅计数（[l()](<resource-unit:#1.dex1 code:com.bs.common.ui.PermissionGuideActivity#l>)，点两次才关闭），并且 `tv_title.postDelayed(4000ms)` 到点自动 `finish`，无“取消/跳过”文案。
3. 跳受限设置：[SecurityLevelActivity.b()](<resource-unit:#1.dex1 code:com.bs.antivirus.ui.main.activity.SecurityLevelActivity#b>) 的 `case 4`（“辅助权限”项，未开启时显示红点，由 [g.c.ev.a()](<resource-unit:#1.dex1 code:g.c.ev#a>) 结合 [us.i()](<resource-unit:#1.dex1 code:g.c.us#i>) 检测）直接调 [g.c.us.L()](<resource-unit:#1.dex1 code:g.c.us#L>) 跳 `android.settings.ACCESSIBILITY_SETTINGS`，跳转前无用途说明。
4. 拒权反馈循环：[g.c.us.a(pkg,ctx,1)](<resource-unit:#1.dex1 code:g.c.us#a>) 跳 `APPLICATION_DETAILS_SETTINGS` 后 `handler.post(new ut(i))` → [g.c.ut.run()](<resource-unit:#1.dex1 code:g.c.ut#run>) → [g.c.us.q()](<resource-unit:#1.dex1 code:g.c.us#q>) 起 `CountDownTimer(2500ms, 500ms)`，结束时 [fC()](<resource-unit:#1.dex1 code:g.c.us#fC>) 判断当前前台包名仍属 `com.android.settings`/`com.miui.securitycenter`/`com.miui.appmanager`/`com.android.packageinstaller` 就再次进入跳转分支，用户不开启会被反复拉回设置页。
5. 获权后动作：[BaseAccessibilityService.fi()](<resource-unit:#1.dex1 code:com.bs.common.ui.service.BaseAccessibilityService#fi>) 对窗口节点 `performAction(16)` 模拟点击执行“清理”，`fj()` 释放信号量推进下一个待处理应用。

**未闭合/边界**：未动态复现重跳时序；`accessibility_message`（“Scroll to find \"%1$s\" and turn it on”）仅在资源中定义、未见代码引用；`onAccessibilityEvent` 中 1085 条指令的完整自动点击目标未逐条穷举。

已登记风险：R-001（high / deceptive_behavior）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导主链路（服务声明与标签/描述、accessibility_config、PermissionGuideActivity 仿开关浮层、SecurityLevelActivity 跳 ACCESSIBILITY_SETTINGS、us.a 跳 APPLICATION_DETAILS_SETTINGS + 2500ms 定时器重跳判定）全部静态可见，未见加壳或密文动态加载；仅 onAccessibilityEvent 中获权后自动点击的具体目标集合未逐条穷举，以及资源 accessibility_message 未见代码引用点。",
  "summary_one_liner": "以“延长电池续航、绝不收集个人信息”话术包装 ★★Antivirus Security★★ 无障碍服务，用底部仿系统已开启开关浮层配合业务页红点引导跳转系统无障碍列表，并在用户返回后由 2.5 秒定时器判定仍停留在设置页即自动重跳，形成无取消入口的拒权循环。",
  "disguise_identity": {
    "app_display_name": "Antivirus Security",
    "claimed_brand_or_persona": "Antivirus Security（伪装的杀毒/电池优化工具品牌，无障碍标签加 ★★ 装饰）",
    "a11y_service_label": "★★Antivirus Security★★",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 用 ★★ 星号包裹以在系统服务列表中视觉突出；android:description 声称仅用于电池优化并预先要求“若收到隐私警告请忽略”，与配置中 typeAllMask + canRetrieveWindowContent=true 的全局监听能力不符；PermissionGuideActivity 用 clickable=false 且 checked=true 的 SwitchCompat 伪造“权限已开启”状态，并叠加手指点击指引图模拟系统设置页；引导浮层无取消/跳过按钮，仅整屏连点两次或 4 秒超时自动关闭。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.bs.antivirus.ui.welcome.WelcomeActivity（LAUNCHER）→ com.bs.antivirus.ui.main.activity.MainActivity",
      "trigger_event": "点击桌面图标冷启动，WelcomeActivity 完成引导后进入 MainActivity",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Terms of Service / Accept and continue",
      "shown_text_zh": "服务条款 / 接受并继续",
      "user_action_requested": "点击“Accept and continue”接受条款后进入主界面（该步为通用入口，不直接申请无障碍）",
      "code_anchor": "AndroidManifest.xml activity WelcomeActivity / com.bs.antivirus.ui.welcome.WelcomeActivity"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.bs.junkclean.ui.activity.JunkCleanActivity / com.bs.batterysaver.BatterySaverActivity / com.bs.applock.ui.fragment.AppLockFragment",
      "trigger_event": "用户点击垃圾清理、电池省电、应用锁等按钮，功能流程内调用 PermissionGuideActivity.a(ctx, new PermissionGuideResourceBean(R$string.permission_guide_accessibility, R$string.accessibility_label))",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Antivirus to close auto-starting apps.",
      "shown_text_zh": "启用 Antivirus 以关闭自动启动的应用。",
      "user_action_requested": "无明确按钮；用户只能点击浮层任意位置（连续两次关闭）或等待 4 秒自动消失",
      "code_anchor": "com.bs.junkclean.ui.activity.JunkCleanActivity$4#a → com.bs.common.ui.PermissionGuideActivity#a(Context, PermissionGuideResourceBean)"
    },
    {
      "step": 3,
      "stage": "引导说明页（仿系统开关）",
      "screen_or_component": "com.bs.common.ui.PermissionGuideActivity，布局 res/layout/activity_permission_guide.xml",
      "trigger_event": "Activity onCreate 经 SimpleActivity → PermissionGuideActivity.a(Bundle)：取 Intent 中的 PermissionGuideResourceBean 设置 tv_title/tv_name，并 tv_title.postDelayed(new tj(this), 4000L)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Enable Antivirus to close auto-starting apps. ／ 应用名 Antivirus Security + 一个 checked=true、clickable=false、rotation=180 的开关 + 手指点击指引图",
      "shown_text_zh": "启用 Antivirus 以关闭自动启动的应用；浮层内展示应用图标、应用名与一个看似“已开启”且不可点击的开关，并配手指点击引导图",
      "user_action_requested": "无“开启/取消/跳过”按钮，开关不可操作；点击整屏仅计数（fW++，≥2 时 finish），或 4 秒后自动 finish",
      "code_anchor": "com.bs.common.ui.PermissionGuideActivity#a(Bundle)、#l(View)、g.c.tj#run；res/layout/activity_permission_guide.xml"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "com.bs.antivirus.ui.main.activity.SecurityLevelActivity 列表项“Accessibility”（未开启显示红点）→ 系统 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户点击 SecurityLevelBodayItem 的 case 4 项（SecurityLevelActivity.b(int,int)），或安全等级页通过 g.c.ev.a() 用 us.i() 判定未开启而显示该项",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility ／ Close auto-starting , battery draining apps in order to extend your battery life.",
      "shown_text_zh": "无障碍 ／ 关闭自动启动、耗电的应用以延长电池续航。",
      "user_action_requested": "用户在系统无障碍列表中找到 “★★Antivirus Security★★” 并手动打开开关；跳转前应用未提供任何权限用途说明页",
      "code_anchor": "com.bs.antivirus.ui.main.activity.SecurityLevelActivity#b(int,int) → g.c.us#L(Context)；g.c.ev#a；res/values/strings.xml level_des_accessibility"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "系统 android.settings.APPLICATION_DETAILS_SETTINGS（应用详情页）+ 应用内 CountDownTimer 判定",
      "trigger_event": "g.c.us.a(String,Context,int) 跳应用详情页后 handler.post(new ut(i))；g.c.ut#run → g.c.us#q 起 hj(2500L,500L)，onFinish → g.c.us$1#bS → g.c.us#fC",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧不展示文字，仅静默判定前台包名）",
      "shown_text_zh": "应用在 2.5 秒后检查当前前台包名，若仍为 com.android.settings / com.miui.securitycenter / com.miui.appmanager / com.android.packageinstaller，则再次执行跳转分支",
      "user_action_requested": "要求用户留在设置页完成开启；未开启即被定时器反复拉回设置页，无“稍后再说”降级路径",
      "code_anchor": "g.c.us#a(String,Context,int)、g.c.us#q(int)、g.c.us#fC()、g.c.ut#run、g.c.us$1#bS"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.bs.common.ui.service.BaseAccessibilityService（onServiceConnected / onAccessibilityEvent / fi）",
      "trigger_event": "用户开启服务后系统回调 onServiceConnected（eventTypes=4194336、flags=1、notificationTimeout=200），清理/加速流程注册 uu 节点操作器后进入 fi()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务对当前窗口节点执行 performAction(16) 模拟点击以推进“关闭应用”流程，并通过信号量逐个处理待清理包名",
      "user_action_requested": "无需用户操作，服务自动读取窗口内容并模拟点击",
      "code_anchor": "com.bs.common.ui.service.BaseAccessibilityService#onServiceConnected、#fi()、#fj()；res/xml/accessibility_config.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：android:label = ★★Antivirus Security★★（res/values/strings.xml accessibility_label）",
    "系统无障碍服务详情说明：android:description = accessibility_service_description（res/values/strings.xml），宣称仅用于电池优化、绝不收集个人信息、提示忽略隐私警告",
    "安全等级页列表项：标题 Accessibility、描述 level_des_accessibility = “Close auto-starting , battery draining apps in order to extend your battery life.”（SecurityLevelActivity 列表，g.c.ev#a 构造）",
    "业务功能触发的底部浮层：PermissionGuideActivity（res/layout/activity_permission_guide.xml），显示 permission_guide_accessibility = “Enable Antivirus to close auto-starting apps.” + 应用名 + 伪造已开启开关 + 手指指引图",
    "未被代码引用的备用引导文案：res/values/strings.xml accessibility_message = “Scroll to find \"%1$s\" and turn it on”（资源中定义，静态未见调用点）",
    "应用内统计埋点（非用户可见）：qj.a(...).k(this.aB, \"启用辅助权限按钮\") 记录点击无障碍引导按钮"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "★★Antivirus Security★★",
      "text_zh": "★★Antivirus Security★★（星号装饰的服务显示名）",
      "source_location": "res/values/strings.xml accessibility_label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Enabling this option will help Antivirus shut down applications to extend the life of your battery.\n\n Antivirus uses the accessibility service to optimize your device only. We will never use it to collect your personal information. If you have received a privacy warning, please ignore it.",
      "text_zh": "启用此选项将帮助 Antivirus 关闭应用以延长电池续航。Antivirus 仅使用无障碍服务优化您的设备。我们绝不会用它收集您的个人信息。如果您收到了隐私警告，请忽略它。",
      "source_location": "res/values/strings.xml accessibility_service_description（Manifest android:description）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Scroll to find \"%1$s\" and turn it on",
      "text_zh": "滑动找到“%1$s”并打开它",
      "source_location": "res/values/strings.xml accessibility_message（静态未见代码引用）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Antivirus to close auto-starting apps.",
      "text_zh": "启用 Antivirus 以关闭自动启动的应用。",
      "source_location": "res/values/strings.xml permission_guide_accessibility（PermissionGuideActivity 标题）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Close auto-starting , battery draining apps in order to extend your battery life.",
      "text_zh": "关闭自动启动、耗电的应用以延长电池续航。",
      "source_location": "res/values/strings.xml level_des_accessibility（SecurityLevelActivity 列表项描述）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility",
      "text_zh": "无障碍",
      "source_location": "res/values/strings.xml accessibility",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "跳转设置页后 handler.post(new ut(i)) 启动 CountDownTimer(2500ms/500ms)，onFinish 回调 g.c.us.fC() 读取当前前台包名，若仍为 com.android.settings / com.miui.securitycenter / com.miui.appmanager / com.android.packageinstaller 则再次进入跳转分支；PermissionGuideActivity 亦无取消按钮，仅整屏连点两次或 4 秒超时自动关闭后仍会回到业务流程再次出现红点",
    "overlay_or_fake_settings": "PermissionGuideActivity 为应用内仿系统开关浮层：底部卡片含应用图标、应用名、clickable=false 且 checked=true 且旋转 180° 的 SwitchCompat、以及手指点击指引图，视觉上呈“权限已开启”但实际不可操作；另配置 SYSTEM_ALERT_WINDOW 权限用于清理过程悬浮进度层，未见全屏高仿系统无障碍设置页",
    "restricted_settings_13plus_coaching": "无（跳转 ACCESSIBILITY_SETTINGS 为直接 Intent，未发现“进入应用详情→右上角菜单→允许受限设置”的分步教学文案或 Session 安装器绕过路径）",
    "post_grant_anti_removal": "部分相关：g.c.us.fC() 对前台包名 com.android.settings / com.miui.securitycenter / com.miui.appmanager / com.android.packageinstaller 的停留状态做重跳判定，属设置页停留监控与重跳，未见 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接证据",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 Activity 启动为触发点：监测到 com.bs.common.ui.PermissionGuideActivity 启动（业务功能触发引导浮层），或监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS / android.settings.APPLICATION_DETAILS_SETTINGS（由 g.c.us.L 与 g.c.us.a 发起）时立即截图；另可在跳转后 2500ms 前后连续截屏以捕获重跳瞬间",
    "key_pages_to_capture": [
      {
        "page_role": "业务功能触发的仿系统开关引导浮层页",
        "page_identifier": "com.bs.common.ui.PermissionGuideActivity，界面特征为底部绿色卡片 + 应用图标 + “Antivirus Security” + 右侧旋转的已勾选开关 + 手指点击指引图",
        "why_most_useful": "该页是唯一向用户呈现“权限已开启”假象的载体，且无取消按钮、4 秒自动消失，是判定伪装与强迫式引导的最直接视觉证据",
        "observable_utg_signals": ["SwitchCompat 控件 clickable=false 且 checked=true 的伪开启状态", "无取消/跳过按钮的整屏可点浮层", "手指点击指引图 drawable icon_permission_finger", "4 秒后页面自动消失"]
      },
      {
        "page_role": "跳转前的安全等级列表项（红点项）",
        "page_identifier": "com.bs.antivirus.ui.main.activity.SecurityLevelActivity 列表中的 “Accessibility” 项及右侧红点",
        "why_most_useful": "证明应用以“安全等级/未优化”红点方式施加心理压力，且点击后无任何说明直接跳系统无障碍页",
        "observable_utg_signals": ["Accessibility 列表项文本", "未开启时的红色角标/提示", "点击后直接拉起系统无障碍设置（无中间说明页）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页中显示 “★★Antivirus Security★★” 的条目及其说明文本",
        "why_most_useful": "核对 label 星号装饰与“仅用于电池优化、请忽略隐私警告”的说明是否如静态资源所述呈现，是身份伪装与告知失真的关键对照点",
        "observable_utg_signals": ["服务名 ★★Antivirus Security★★", "说明文本含“we will never use it to collect your personal information / please ignore it”", "开关初始为关闭状态"]
      },
      {
        "page_role": "设置页返回/停留后的重跳瞬间",
        "page_identifier": "跳转 APPLICATION_DETAILS_SETTINGS 后约 2500ms，Activity 再次变为系统设置/无障碍页",
        "why_most_useful": "直接验证拒权循环：用户未开启时是否被定时器自动拉回设置页，这是判定强迫性与审核规避的核心运行期证据",
        "observable_utg_signals": ["两次相邻截屏中前台均为 com.android.settings 系页面", "无用户输入情况下 Activity 栈再次变化", "PermissionGuideActivity 反复出现"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导浮层与列表文案均为可读文本，无纯图片诱导；但获权后 onAccessibilityEvent（1085 条指令）中的自动点击目标未逐条还原，若需判定其是否在系统设置页自动点开开关或阻止撤权，需运行期 Hook 或 UTG 连续采样；静态加壳初判为 False，运行期 UTG 不受影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.bs.common.ui.PermissionGuideActivity#a(android.os.Bundle)",
    "com.bs.antivirus.ui.main.activity.SecurityLevelActivity#b(int,int)",
    "g.c.us#L(android.content.Context)",
    "g.c.us#a(java.lang.String, android.content.Context, int)",
    "g.c.us#fC()",
    "com.bs.common.ui.service.BaseAccessibilityService#onServiceConnected"
  ]
}
```

</details>
