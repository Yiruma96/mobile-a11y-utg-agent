# MB_075__917d7a3dff｜SharkBot — Antivirus Y5, Cleaner, Booster

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：179.4s

## 1. 一句话核心结论

- **核心申请方式**：以杀毒清理工具身份，在 MainActivity 每次 onResume 检测无障碍未开即弹无取消按钮的 'Permission Needed / Grant Now' 原生弹窗，点击后同时跳系统无障碍设置页并压入 'Find X and grant Y' 自绘引导页，拒权后反复重弹，获权后按云控脚本执行全局点击/返回/滚动。
- **静态可见性说明**：无障碍诱导链路（弹窗、跳转、引导页、服务配置、事件处理框架）全部静态可见、无加壳无加密；仅云控 JSON 任务脚本（SharedPreferences 'lopanel' 经 d.e.a.a.e.a#c 解密、或 this.w.b() 远端下发）与 status 门控值位于服务端/加密存储，不影响本诱导流程的还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `917d7a3dff486a6b2908607dccf5d8a2929e05bb1ce988aec40bcb194d999bd0` |
| 包名 / 年份 | `com.fastcleaner.forphoneandroid.freenoads` / 2022 |
| 家族 / 品类 | **SharkBot**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Antivirus Y5, Cleaner, Booster |
| 引导页宣称品牌/身份 | Antivirus Y5（伪装为杀毒/深度清理工具，无障碍说明中又自称 Super Cleaner） |
| 系统无障碍列表服务名 | Antivirus Y5, Cleaner, Booster |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍 android:description 正文自称 'Super Cleaner' 与桌面名 'Antivirus Y5, Cleaner, Booster' 不一致；description 中插入 '\n \n' 空行把真实用途（列表中找到本应用并开启开关）挤出可视区，并含拼写错误 'Accessiblility'、'warinings'、'orther'；Manifest 同时内置 com.security.applock.* 与 com.testapp.duplicatefileremover.* 两套平行无障碍引导实现，形成多套别名式引导入口。 |
| 无障碍服务类名 | `com.fastcleaner.forphoneandroid.freenoads.service.ForceStopAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | SplashActivity -> com.fastcleaner.forphoneandroid.freenoads.screen.main.MainActivity | onCreate 启动 ServiceManager 前台服务并构建三页 ViewPager；onResume 立即调用基类 W() | 原生Activity | **原文**：Antivirus Y5, Cleaner, Booster<br>**译注**：桌面与应用内标题显示为“Antivirus Y5 清理与加速” | 无需操作，进入首页即触发后续权限检测 | `com.fastcleaner.forphoneandroid.freenoads.screen.main.MainActivity#onCreate / #onResume` |
| 2 | 业务功能触发 | d.e.a.a.j.r#W（MainActivity 基类，每次 onResume 复用） | onResume -> W()：读取云控 JSON（status=='skip' 则返回），再 this.w.c(this, ForceStopAccessibility.class) 检测无障碍是否已启用 | 不可静态还原 | 无 | 无 | `d.e.a.a.j.r#W / d.e.a.a.j.r#a0` |
| 3 | 引导说明页 | com.fastcleaner.forphoneandroid.freenoads.dialog.DialogAskPermission（layout: dialog_ask_permission.xml，含 Lottie robo_permission.json） | d.e.a.a.j.r#e0 -> DialogAskPermission.N0("android.settings.ACCESSIBILITY_SETTINGS", new c(this)).M0(...) 显示 | 原生Dialog | **原文**：Permission Needed<br>Grant Now<br>**译注**：标题“需要权限”，唯一按钮“立即授予”（正文由 O0() 按跳转目标设置为字符串资源 2131951653） | 只能点击 Grant Now（id 2131362572）；布局中不存在取消/跳过/关闭按钮 | `com.fastcleaner.forphoneandroid.freenoads.dialog.DialogAskPermission#O0 / #click / res/layout/dialog_ask_permission.xml` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | DialogAskPermission#click -> 回调 d.e.a.a.j.c#a -> startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | 无 | 要求用户在该列表中找到并打开本应用开关 | `d.e.a.a.j.c#a` |
| 5 | 遮罩叠层指引 | com.fastcleaner.forphoneandroid.freenoads.screen.guildPermission.GuildPermissionActivity | 同一回调紧接着 GuildPermissionActivity.g0(rVar, "android.settings.ACCESSIBILITY_SETTINGS")，将引导页压到设置页之上；onCreate 按 intent 的 "permission name" 取文案 | 原生Activity（叠在系统设置页栈顶的自绘全屏引导页，非系统遮罩悬浮窗） | **原文**：Find %s and grant %s  /  accessibility permission<br>**译注**：“在列表中找到 Antivirus Y5, Cleaner, Booster 并授予 accessibility permission（无障碍权限）” | 按提示在系统设置中手动开启；页面提供两个按钮（id 2131362082 / 2131362159，分别为 b(this)、a(this) 监听器） | `com.fastcleaner.forphoneandroid.freenoads.screen.guildPermission.GuildPermissionActivity#onCreate / #g0` |
| 6 | 跳无障碍设置 | 系统无障碍列表中的服务条目（label=@string/app_name，description=@string/accessibility_service_description） | 用户在列表中看到服务项并点开开关 | 系统无障碍页 | **原文**：Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.<br>**译注**：“点击右上角使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。开启无障碍服务时你需要接受 Android 系统警告。Clean master 不会将这些用于此处列明之外的任何其他用途。” | 在系统警告弹窗上点“允许/确定”，打开本应用无障碍开关 | `res/xml/accessibility_service_config.xml / res/values/strings.xml#accessibility_service_description` |
| 7 | 拒权反馈循环 | MainActivity.onResume -> d.e.a.a.j.r#a0 -> #e0 -> DialogAskPermission | 用户从设置页返回（未开启或开启后又关闭）触发 onResume；a0() 判定无障碍仍未启用则返回 true，并再次 e0() 弹窗 | 原生Dialog | **原文**：Permission Needed<br>Grant Now<br>**译注**：同一弹窗再次出现；同时 a0()==true 使存储/用量/悬浮窗等其它授权流程（P/Q/X）直接短路返回 | 再次被迫点击 Grant Now，无取消路径 | `d.e.a.a.j.r#a0 / #W / com.fastcleaner.forphoneandroid.freenoads.screen.main.MainActivity#onResume` |
| 8 | 获权后动作 | com.fastcleaner.forphoneandroid.freenoads.service.ForceStopAccessibility（android:process=":BackgroundService"） | 服务连接后 onAccessibilityEvent 读取云控 JSONArray（this.e），按 event/action/nodes 脚本在第三方应用窗口操作；W() 在确认已开启后继续跳 android.settings.MANAGE_UNKNOWN_APP_SOURCES | 不可静态还原（脚本内容来自远端/加密 lopanel） | 无 | 无（用户已完成授权，后续界面操作为自动化模拟） | `com.fastcleaner.forphoneandroid.freenoads.service.ForceStopAccessibility#onAccessibilityEvent / #b` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 触发的原生 DialogFragment（dialog_ask_permission.xml）：标题 'Permission Needed'、按钮 'Grant Now'，布局中无取消/跳过控件
- GuildPermissionActivity 自绘全屏 Activity（叠在系统无障碍设置页之上）：'Find %s and grant %s' 模板 + 'accessibility permission'
- 系统无障碍服务列表条目的 android:description（accessibility_service_description）：'Tap on top right use to Accessiblility service...' 长文本，夹带空行与拼写错误
- 无障碍服务 label（@string/app_name）：'Antivirus Y5, Cleaner, Booster'
- strings.xml 中备用文案：'Grant permission to Running a malware scan'（accessibility_setting_permission）、'Grant App Usage Permission for a comprehensive phone scan effect'（grant_app_permission，其它权限分支使用）
- Lottie 动画资源 robo_permission.json 作为弹窗顶部视觉元素（非文本，起“安全/机器人守卫”心理暗示作用）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Permission Needed | 需要权限 | `res/values/strings.xml key=permission_needed（dialog_ask_permission.xml tv_title）` | 假反诈安全 |
| en | Grant Now | 立即授予 | `res/values/strings.xml key=grant_now（dialog_ask_permission.xml tv_action_1）` | 假反诈安全 |
| en | Find %s and grant %s | 在列表中找到 %s 并授予 %s | `res/values/strings.xml key=find_and_grant（GuildPermissionActivity.onCreate 用 2131951810 渲染）` | 受限设置分步教学 |
| en | accessibility permission | 无障碍权限 | `res/values/strings.xml key=accessibility_permission` | 受限设置分步教学 |
| en | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. | 点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。开启无障碍服务时你须接受 Android 系统警告。Clean master 不会将其用于此处列明之外的任何用途。 | `res/values/strings.xml key=accessibility_service_description（accessibility_service_config.xml 引用）` | 清理工具伪装 |
| en | Grant permission to Running a malware scan | 授予权限以运行恶意软件扫描 | `res/values/strings.xml key=accessibility_setting_permission` | 假反诈安全 |
| en | Grant App Usage Permission for a comprehensive phone scan effect | 授予应用使用情况权限以获得完整的手机扫描效果 | `res/values/strings.xml key=grant_app_permission（dialog_ask_permission.xml 默认 tv_content）` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：从系统设置返回即触发 MainActivity.onResume -> W() -> a0() 判定未启用 -> 再次 e0() 弹出同一 'Permission Needed/Grant Now' 弹窗；同时 a0() 返回 true 使存储、用量统计、悬浮窗等其它授权入口（P/Q/X）直接短路，无法绕过无障碍先完成任何业务。
- **遮罩叠层 / 高仿系统设置页**：未发现半透明悬浮遮罩或高仿系统无障碍开关页；但在 startActivity(ACCESSIBILITY_SETTINGS) 之后立即用 GuildPermissionActivity 全屏自绘引导页压栈，形成“系统设置页 + 应用自绘教学页”叠加效果。
- **Android 13+ 受限设置（Restricted Settings）应对**：包内未发现跳转 ACTION_APPLICATION_DETAILS_SETTINGS 的“右上角菜单允许受限设置”教学；但获权后 W() 会自动跳 android.settings.MANAGE_UNKNOWN_APP_SOURCES（package:本应用），onAccessibilityEvent 的 intent 动作同样跳该页，属自动引导未知来源安装授权。
- **获权后即时行为与防撤权机制**：onAccessibilityEvent 具备 performGlobalAction(1)（BACK）能力并在脚本结束后主动返回，可在设置页执行返回键；未发现监听无障碍设置页阻止撤权的专用逻辑。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 MainActivity.onResume 后 0~2s 内出现包内 DialogFragment（标题 'Permission Needed'）时立即抓 UTG；或监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间抓栈，随后 300~800ms 再抓一次以捕获压栈的 GuildPermissionActivity。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：弹窗、引导页、系统服务说明均为纯文本可 UTG 提取。需注意两点：一是云控 status=='skip' 时应用会完全不弹窗（首启可能静默），建议连续冷启动 2~3 次或联网后复测；二是无障碍开启后的自动化点击脚本来自远端/加密 lopanel，UTG 仅能观察行为结果（第三方页面被自动点击/返回），无法直接读到任务 JSON。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 包名 com.fastcleaner.forphoneandroid.freenoads 下的 DialogFragment，含文本 'Permission Needed' 与按钮 'Grant Now'，顶部为 Lottie robo_permission.json 动画 | 这是诱导链的起点，可直接证明应用在冷启动即主动索取无障碍，且只有一个按钮、无取消项 | 文本 'Permission Needed' / 'Grant Now'；弹窗内可点击节点仅 1 个（无 cancel/skip/close）；无触摸即自动出现，非用户功能触发 |
| **跳转前引导页（压栈 Activity）** | GuildPermissionActivity 全屏页，文本形如 'Find Antivirus Y5, Cleaner, Booster and grant accessibility permission' | 证明应用不满足于打开系统设置，还额外自绘分步教学页指明“在列表中找本应用并打开开关”，是诱导意图的直接证据 | 'Find ... and grant ...' 文本模板；页面上方为系统设置页残留，说明叠层于系统设置之上；页面按钮数量与文案 |
| **系统无障碍服务列表项** | Settings 应用无障碍列表中的 'Antivirus Y5, Cleaner, Booster' 条目及其 description 文本 | 核对系统侧实际展示的服务名与说明，验证与桌面名/自称品牌的错位及空行挤占效果 | 服务 label 与 app 名一致；description 中出现 'Super Cleaner' 与 'Clean master' 自称；description 中的空行与拼写错误 |
| **拒权返回后的重弹弹窗页** | 从设置页按返回后 1s 内再次出现的同一 'Permission Needed' 弹窗 | 验证拒权循环（onResume 重跳/重弹）与无法降级，是判定强制诱导而非良性说明的关键 | 返回后弹窗重复出现次数；是否存在任何替代路径页面（手动清理模式）；弹窗出现延迟（与 onResume 同步） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.fastcleaner.forphoneandroid.freenoads.screen.main.MainActivity#onResume`
- `d.e.a.a.j.r#W`
- `d.e.a.a.j.r#e0`
- `d.e.a.a.j.c#a`
- `com.fastcleaner.forphoneandroid.freenoads.screen.guildPermission.GuildPermissionActivity#onCreate`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**无障碍权限引导流程在静态代码中完整可见（cloud 脚本内容除外）**，核心是“清理/杀毒工具身份 + 原生弹窗 + 系统无障碍页 + 自绘引导页”三连，且每次返回都会被重新拉起。

1. **触发时机**：`MainActivity.onResume` 每次都调用基类 `d.e.a.a.j.r#W`，先用 `this.w.c(this, ForceStopAccessibility.class)` 检测无障碍是否已开；未开启即置 `s=1` 并调 `e0()` 弹窗。冷启动与从任何页面返回都会重复触发。
2. **弹窗载体**：原生 DialogFragment [DialogAskPermission](<resource-unit:#1.dex1 code:com.fastcleaner.forphoneandroid.freenoads.dialog.DialogAskPermission#K0>)，布局 [dialog_ask_permission.xml](<resource-unit:#1 file:res/layout/dialog_ask_permission.xml#L1-L10>) 含 Lottie 动画 `robo_permission.json`、标题 `Permission Needed`、正文、**唯一按钮 `Grant Now`**，布局中无取消/跳过控件。
3. **跳转动作**：点击后走 [d.e.a.a.j.c#a](<resource-unit:#1.dex1 code:d.e.a.a.j.c#a>)，先 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 打开系统无障碍列表，**紧接着**用 `GuildPermissionActivity.g0(...)` 把自绘引导页压到同一任务栈上——用户从设置页返回就会看到“Find %s and grant %s”的教学文案。
4. **身份与文案错位**：桌面名与无障碍服务 label 均为 `Antivirus Y5, Cleaner, Booster`，但 `android:description` 正文自称 **“Super Cleaner”**，并夹带空行/拼写错误（`Accessiblility`），把开关动作包装成“清理隐藏垃圾、休眠耗电应用”。
5. **拒权循环**：`a0()` 在无障碍未开启时返回 `true`，不仅让 `P/Q/X`（存储、用量、悬浮窗）等其它授权流程直接短路，也导致 `onResume → W → a0 → e0` 反复重弹同一弹窗；布局层面无可点关闭入口。
6. **获权后即用**：`ForceStopAccessibility` 以 `typeAllMask` + `canRetrieveWindowContent="true"` 注册（[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml#L1-L2>)），[onAccessibilityEvent](<resource-unit:#1.dex1 code:com.fastcleaner.forphoneandroid.freenoads.service.ForceStopAccessibility#onAccessibilityEvent>) 按服务端下发 JSON 在第三方应用内按 id/text 查节点并 `CLICK(16)`/`BACK(1)`/`SCROLL(8192)`，还能自动跳 `MANAGE_UNKNOWN_APP_SOURCES`；随后 `W()` 继续推进受限设置（未知来源安装）。
7. **证据边界**：具体任务脚本来自远端/加密存储（`SharedPreferences "lopanel"` 经 `d.e.a.a.e.a#c` 解密），包内无明文任务清单；`status == "skip"` 的云控门控也在服务端。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导链路（弹窗、跳转、引导页、服务配置、事件处理框架）全部静态可见、无加壳无加密；仅云控 JSON 任务脚本（SharedPreferences 'lopanel' 经 d.e.a.a.e.a#c 解密、或 this.w.b() 远端下发）与 status 门控值位于服务端/加密存储，不影响本诱导流程的还原。",
  "summary_one_liner": "以杀毒清理工具身份，在 MainActivity 每次 onResume 检测无障碍未开即弹无取消按钮的 'Permission Needed / Grant Now' 原生弹窗，点击后同时跳系统无障碍设置页并压入 'Find X and grant Y' 自绘引导页，拒权后反复重弹，获权后按云控脚本执行全局点击/返回/滚动。",
  "disguise_identity": {
    "app_display_name": "Antivirus Y5, Cleaner, Booster",
    "claimed_brand_or_persona": "Antivirus Y5（伪装为杀毒/深度清理工具，无障碍说明中又自称 Super Cleaner）",
    "a11y_service_label": "Antivirus Y5, Cleaner, Booster",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍 android:description 正文自称 'Super Cleaner' 与桌面名 'Antivirus Y5, Cleaner, Booster' 不一致；description 中插入 '\\n \\n' 空行把真实用途（列表中找到本应用并开启开关）挤出可视区，并含拼写错误 'Accessiblility'、'warinings'、'orther'；Manifest 同时内置 com.security.applock.* 与 com.testapp.duplicatefileremover.* 两套平行无障碍引导实现，形成多套别名式引导入口。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "SplashActivity -> com.fastcleaner.forphoneandroid.freenoads.screen.main.MainActivity",
      "trigger_event": "onCreate 启动 ServiceManager 前台服务并构建三页 ViewPager；onResume 立即调用基类 W()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Antivirus Y5, Cleaner, Booster",
      "shown_text_zh": "桌面与应用内标题显示为“Antivirus Y5 清理与加速”",
      "user_action_requested": "无需操作，进入首页即触发后续权限检测",
      "code_anchor": "com.fastcleaner.forphoneandroid.freenoads.screen.main.MainActivity#onCreate / #onResume"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "d.e.a.a.j.r#W（MainActivity 基类，每次 onResume 复用）",
      "trigger_event": "onResume -> W()：读取云控 JSON（status=='skip' 则返回），再 this.w.c(this, ForceStopAccessibility.class) 检测无障碍是否已启用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，纯判断逻辑；未开启则 s=1 并调用 e0()",
      "user_action_requested": "无",
      "code_anchor": "d.e.a.a.j.r#W / d.e.a.a.j.r#a0"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.fastcleaner.forphoneandroid.freenoads.dialog.DialogAskPermission（layout: dialog_ask_permission.xml，含 Lottie robo_permission.json）",
      "trigger_event": "d.e.a.a.j.r#e0 -> DialogAskPermission.N0(\"android.settings.ACCESSIBILITY_SETTINGS\", new c(this)).M0(...) 显示",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission Needed\nGrant Now",
      "shown_text_zh": "标题“需要权限”，唯一按钮“立即授予”（正文由 O0() 按跳转目标设置为字符串资源 2131951653）",
      "user_action_requested": "只能点击 Grant Now（id 2131362572）；布局中不存在取消/跳过/关闭按钮",
      "code_anchor": "com.fastcleaner.forphoneandroid.freenoads.dialog.DialogAskPermission#O0 / #click / res/layout/dialog_ask_permission.xml"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "DialogAskPermission#click -> 回调 d.e.a.a.j.c#a -> startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接打开系统“无障碍/已下载的服务”列表",
      "user_action_requested": "要求用户在该列表中找到并打开本应用开关",
      "code_anchor": "d.e.a.a.j.c#a"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.fastcleaner.forphoneandroid.freenoads.screen.guildPermission.GuildPermissionActivity",
      "trigger_event": "同一回调紧接着 GuildPermissionActivity.g0(rVar, \"android.settings.ACCESSIBILITY_SETTINGS\")，将引导页压到设置页之上；onCreate 按 intent 的 \"permission name\" 取文案",
      "ui_carrier": "原生Activity（叠在系统设置页栈顶的自绘全屏引导页，非系统遮罩悬浮窗）",
      "shown_text_verbatim": "Find %s and grant %s  /  accessibility permission",
      "shown_text_zh": "“在列表中找到 Antivirus Y5, Cleaner, Booster 并授予 accessibility permission（无障碍权限）”",
      "user_action_requested": "按提示在系统设置中手动开启；页面提供两个按钮（id 2131362082 / 2131362159，分别为 b(this)、a(this) 监听器）",
      "code_anchor": "com.fastcleaner.forphoneandroid.freenoads.screen.guildPermission.GuildPermissionActivity#onCreate / #g0"
    },
    {
      "step": 6,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍列表中的服务条目（label=@string/app_name，description=@string/accessibility_service_description）",
      "trigger_event": "用户在列表中看到服务项并点开开关",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "shown_text_zh": "“点击右上角使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。开启无障碍服务时你需要接受 Android 系统警告。Clean master 不会将这些用于此处列明之外的任何其他用途。”",
      "user_action_requested": "在系统警告弹窗上点“允许/确定”，打开本应用无障碍开关",
      "code_anchor": "res/xml/accessibility_service_config.xml / res/values/strings.xml#accessibility_service_description"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onResume -> d.e.a.a.j.r#a0 -> #e0 -> DialogAskPermission",
      "trigger_event": "用户从设置页返回（未开启或开启后又关闭）触发 onResume；a0() 判定无障碍仍未启用则返回 true，并再次 e0() 弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission Needed\nGrant Now",
      "shown_text_zh": "同一弹窗再次出现；同时 a0()==true 使存储/用量/悬浮窗等其它授权流程（P/Q/X）直接短路返回",
      "user_action_requested": "再次被迫点击 Grant Now，无取消路径",
      "code_anchor": "d.e.a.a.j.r#a0 / #W / com.fastcleaner.forphoneandroid.freenoads.screen.main.MainActivity#onResume"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "com.fastcleaner.forphoneandroid.freenoads.service.ForceStopAccessibility（android:process=\":BackgroundService\"）",
      "trigger_event": "服务连接后 onAccessibilityEvent 读取云控 JSONArray（this.e），按 event/action/nodes 脚本在第三方应用窗口操作；W() 在确认已开启后继续跳 android.settings.MANAGE_UNKNOWN_APP_SOURCES",
      "ui_carrier": "不可静态还原（脚本内容来自远端/加密 lopanel）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静默执行：performAction(16) 点击、performGlobalAction(1) 返回、performAction(8192) 滚动，可自动打开未知来源安装设置，脚本结束后 performGlobalAction(1) 并跳回 MainActivity",
      "user_action_requested": "无（用户已完成授权，后续界面操作为自动化模拟）",
      "code_anchor": "com.fastcleaner.forphoneandroid.freenoads.service.ForceStopAccessibility#onAccessibilityEvent / #b"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 触发的原生 DialogFragment（dialog_ask_permission.xml）：标题 'Permission Needed'、按钮 'Grant Now'，布局中无取消/跳过控件",
    "GuildPermissionActivity 自绘全屏 Activity（叠在系统无障碍设置页之上）：'Find %s and grant %s' 模板 + 'accessibility permission'",
    "系统无障碍服务列表条目的 android:description（accessibility_service_description）：'Tap on top right use to Accessiblility service...' 长文本，夹带空行与拼写错误",
    "无障碍服务 label（@string/app_name）：'Antivirus Y5, Cleaner, Booster'",
    "strings.xml 中备用文案：'Grant permission to Running a malware scan'（accessibility_setting_permission）、'Grant App Usage Permission for a comprehensive phone scan effect'（grant_app_permission，其它权限分支使用）",
    "Lottie 动画资源 robo_permission.json 作为弹窗顶部视觉元素（非文本，起“安全/机器人守卫”心理暗示作用）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Permission Needed",
      "text_zh": "需要权限",
      "source_location": "res/values/strings.xml key=permission_needed（dialog_ask_permission.xml tv_title）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant Now",
      "text_zh": "立即授予",
      "source_location": "res/values/strings.xml key=grant_now（dialog_ask_permission.xml tv_action_1）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Find %s and grant %s",
      "text_zh": "在列表中找到 %s 并授予 %s",
      "source_location": "res/values/strings.xml key=find_and_grant（GuildPermissionActivity.onCreate 用 2131951810 渲染）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "accessibility permission",
      "text_zh": "无障碍权限",
      "source_location": "res/values/strings.xml key=accessibility_permission",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "text_zh": "点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。开启无障碍服务时你须接受 Android 系统警告。Clean master 不会将其用于此处列明之外的任何用途。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（accessibility_service_config.xml 引用）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant permission to Running a malware scan",
      "text_zh": "授予权限以运行恶意软件扫描",
      "source_location": "res/values/strings.xml key=accessibility_setting_permission",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant App Usage Permission for a comprehensive phone scan effect",
      "text_zh": "授予应用使用情况权限以获得完整的手机扫描效果",
      "source_location": "res/values/strings.xml key=grant_app_permission（dialog_ask_permission.xml 默认 tv_content）",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "从系统设置返回即触发 MainActivity.onResume -> W() -> a0() 判定未启用 -> 再次 e0() 弹出同一 'Permission Needed/Grant Now' 弹窗；同时 a0() 返回 true 使存储、用量统计、悬浮窗等其它授权入口（P/Q/X）直接短路，无法绕过无障碍先完成任何业务。",
    "overlay_or_fake_settings": "未发现半透明悬浮遮罩或高仿系统无障碍开关页；但在 startActivity(ACCESSIBILITY_SETTINGS) 之后立即用 GuildPermissionActivity 全屏自绘引导页压栈，形成“系统设置页 + 应用自绘教学页”叠加效果。",
    "restricted_settings_13plus_coaching": "包内未发现跳转 ACTION_APPLICATION_DETAILS_SETTINGS 的“右上角菜单允许受限设置”教学；但获权后 W() 会自动跳 android.settings.MANAGE_UNKNOWN_APP_SOURCES（package:本应用），onAccessibilityEvent 的 intent 动作同样跳该页，属自动引导未知来源安装授权。",
    "post_grant_anti_removal": "onAccessibilityEvent 具备 performGlobalAction(1)（BACK）能力并在脚本结束后主动返回，可在设置页执行返回键；未发现监听无障碍设置页阻止撤权的专用逻辑。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 MainActivity.onResume 后 0~2s 内出现包内 DialogFragment（标题 'Permission Needed'）时立即抓 UTG；或监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间抓栈，随后 300~800ms 再抓一次以捕获压栈的 GuildPermissionActivity。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "包名 com.fastcleaner.forphoneandroid.freenoads 下的 DialogFragment，含文本 'Permission Needed' 与按钮 'Grant Now'，顶部为 Lottie robo_permission.json 动画",
        "why_most_useful": "这是诱导链的起点，可直接证明应用在冷启动即主动索取无障碍，且只有一个按钮、无取消项",
        "observable_utg_signals": ["文本 'Permission Needed' / 'Grant Now'", "弹窗内可点击节点仅 1 个（无 cancel/skip/close）", "无触摸即自动出现，非用户功能触发"]
      },
      {
        "page_role": "跳转前引导页（压栈 Activity）",
        "page_identifier": "GuildPermissionActivity 全屏页，文本形如 'Find Antivirus Y5, Cleaner, Booster and grant accessibility permission'",
        "why_most_useful": "证明应用不满足于打开系统设置，还额外自绘分步教学页指明“在列表中找本应用并打开开关”，是诱导意图的直接证据",
        "observable_utg_signals": ["'Find ... and grant ...' 文本模板", "页面上方为系统设置页残留，说明叠层于系统设置之上", "页面按钮数量与文案"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 应用无障碍列表中的 'Antivirus Y5, Cleaner, Booster' 条目及其 description 文本",
        "why_most_useful": "核对系统侧实际展示的服务名与说明，验证与桌面名/自称品牌的错位及空行挤占效果",
        "observable_utg_signals": ["服务 label 与 app 名一致", "description 中出现 'Super Cleaner' 与 'Clean master' 自称", "description 中的空行与拼写错误"]
      },
      {
        "page_role": "拒权返回后的重弹弹窗页",
        "page_identifier": "从设置页按返回后 1s 内再次出现的同一 'Permission Needed' 弹窗",
        "why_most_useful": "验证拒权循环（onResume 重跳/重弹）与无法降级，是判定强制诱导而非良性说明的关键",
        "observable_utg_signals": ["返回后弹窗重复出现次数", "是否存在任何替代路径页面（手动清理模式）", "弹窗出现延迟（与 onResume 同步）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：弹窗、引导页、系统服务说明均为纯文本可 UTG 提取。需注意两点：一是云控 status=='skip' 时应用会完全不弹窗（首启可能静默），建议连续冷启动 2~3 次或联网后复测；二是无障碍开启后的自动化点击脚本来自远端/加密 lopanel，UTG 仅能观察行为结果（第三方页面被自动点击/返回），无法直接读到任务 JSON。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.fastcleaner.forphoneandroid.freenoads.screen.main.MainActivity#onResume",
    "d.e.a.a.j.r#W",
    "d.e.a.a.j.r#e0",
    "d.e.a.a.j.c#a",
    "com.fastcleaner.forphoneandroid.freenoads.screen.guildPermission.GuildPermissionActivity#onCreate",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
