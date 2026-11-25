# MB_079__b4a031c108｜SharkBot — Atom Clean-Booster, Antivirus

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：142.0s

## 1. 一句话核心结论

- **核心申请方式**：以清理工具外壳，冷启动/回前台即弹不可跳过的授权弹窗，点 Grant Now 后跳系统无障碍设置并同时压入伪装系统开关的悬浮遮罩层，获权后由无障碍服务自动 BACK 退出设置页并按云端脚本自动点按。
- **静态可见性说明**：DEX 未加壳，引导链路的 Activity/Dialog/遮罩布局与跳转代码完全静态可见；仅云控会话 JSON（RSA/AES 加密的 SESSION）与下发的 ATS 无障碍脚本步骤来自 http://statscodicefiscale.xyz/stats/，属远端内容，不影响 UTG 页面流转判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b4a031c10801de4e89d7d66f26824d9066c4c217c06386dc102a08c26a81d4f0` |
| 包名 / 年份 | `com.abbondioendrizzi.tools.supercleaner` / 2022 |
| 家族 / 品类 | **SharkBot**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Atom Clean-Booster, Antivirus |
| 引导页宣称品牌/身份 | 伪装为手机清理/加速/杀毒工具（描述文本中自称 Super Cleaner、Clean master，与桌面显示名 Atom Clean-Booster 不一致） |
| 系统无障碍列表服务名 | Atom Clean-Booster, Antivirus（服务 android:label 直接复用 @string/app_name，未声明独立无障碍服务名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍描述中插入大量空行与换行挤开系统警告文案（"Tap on top right use to Accessiblility service." 后接多空行），并用错拼 warinings/orther 规避关键词；无障碍服务 label 复用应用名以隐藏真实用途；遮罩层用 checked=true 且 clickable=false 的 SwitchCompat 伪造系统开关状态；描述中品牌名（Super Cleaner / Clean master）与包名及 app_name 不一致。 |
| 无障碍服务类名 | `com.abbondioendrizzi.tools.supercleaner.service.ForceStopAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.abbondioendrizzi.tools.supercleaner.screen.main.MainActivity | onResume（每次回到前台都会重新执行） | 原生Activity | 无 | 无，用户被动进入 | `MainActivity.onResume -> d.a.a.a.j.s.Y` |
| 2 | 业务功能触发 | d.a.a.a.j.s（BaseActivity）与远端 http://statscodicefiscale.xyz/stats/ | Y() 读取 SharedPreferences SESSION，经 d.a.a.a.c.d 解密失败则本地构造 c0() 并 POST 上报（APP_NAME=cleaner1、CLIENT_ID、机型、locale、已装应用列表 apps2、overlay、source） | 不可静态还原 | **原文**：无（网络请求，无 UI）<br>**译注**：云端返回 status=needInstall 时进入无障碍授权流程 | 无 | `d.a.a.a.j.s#Y / #i0 / #c0` |
| 3 | 引导说明页 | com.abbondioendrizzi.tools.supercleaner.dialog.DialogAskPermission（DialogFragment，内容由 g0() 以 android.settings.ACCESSIBILITY_SETTINGS 构造） | Y() 中 U() 判定未授予无障碍权限后调用 g0()；d0() 在 status=needInstall 且未授权时同样调用 g0() | 原生Dialog | **原文**：Permission Needed / Grant App Usage Permission for a comprehensive phone scan effect / Grant Now（Lottie robo_permission.json 机器人动画；O0 对 ACCESSIBILITY_SETTINGS 改用 2131951653 文案）<br>**译注**：“需要权限” / “授予应用使用权限以获得全面的手机扫描效果” / “立即授权” | 点击唯一按钮 Grant Now 前往授权；无 Cancel 按钮，但 Dialog 被设为 setCancelable(true)、setCanceledOnTouchOutside(true)，可返回键或点外部关闭 | `DialogAskPermission#K0 / #O0 / #click / #k0，res/layout/dialog_ask_permission.xml` |
| 4 | 跳无障碍设置 | 系统 Settings 的 ACTION_ACCESSIBILITY_SETTINGS 页 | 点击 Grant Now → DialogAskPermission#click → d.a.a.a.j.c#a | 系统无障碍页 | **原文**：无（直接 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))）<br>**译注**：打开系统无障碍服务列表，要求用户找到本应用并开启 | 在系统列表中找到 Atom Clean-Booster, Antivirus 并打开开关 | `d.a.a.a.j.c#a` |
| 5 | 遮罩叠层指引 | com.abbondioendrizzi.tools.supercleaner.screen.guildPermission.GuildPermissionActivity（全屏半透明遮罩 + 底部卡片，模拟系统开关行） | 同一次点击中紧跟 startActivity 调用 GuildPermissionActivity.j0(context, "android.settings.ACCESSIBILITY_SETTINGS")，压栈叠在系统设置页之上 | 悬浮窗Overlay | **原文**：Find %s and grant %s（实际渲染为 Find Atom Clean-Booster, Antivirus and grant <权限说明>）+ 应用图标 + 应用名 + 已勾选且不可点击的 SwitchCompat + pointing_hand 手势图 + 右上角关闭图标<br>**译注**：“找到 Atom Clean-Booster, Antivirus 并授予权限”，并显示一个已处于开启状态的开关与指向手势，诱导用户照此在系统页操作 | 按遮罩指引在系统无障碍页找到该条目并打开开关；右上角有关闭图标可退出遮罩 | `GuildPermissionActivity#onCreate / #j0，res/layout/activity_guide_setting.xml，res/values/strings.xml#find_and_grant` |
| 6 | 获权后动作 | com.abbondioendrizzi.tools.supercleaner.service.ForceStopAccessibility（独立进程 :BackgroundService） | onServiceConnected 回调；此前 Y() 已通过 S("atsFull") 用 Intent extra 注入云端下发的 ats 脚本与 clienid | 不可静态还原 | **原文**：无（performGlobalAction(1) 即 GLOBAL_ACTION_BACK，200ms 后 a(this)）<br>**译注**：获权瞬间自动模拟返回键退出系统设置页并跳回主界面，用户看不到停留过程 | 无 | `ForceStopAccessibility#onServiceConnected / #onAccessibilityEvent / #onStartCommand` |
| 7 | 拒权反馈循环 | MainActivity.onResume → d.a.a.a.j.s#Y / #d0 → g0() | 用户从设置页返回但未开启服务时再次触发 onResume | 原生Dialog | **原文**：Permission Needed / Grant Now（重复出现）<br>**译注**：再次弹出同一授权弹窗，直到云控 status 变为 skip（并写入 1 小时 skip 时间戳）或授权成功 | 反复要求点击 Grant Now；U() 中 skip 超过 3600000ms 后会重新拉取会话再次要求 | `MainActivity#onResume，d.a.a.a.j.s#Y / #d0 / #U` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目描述：res/values/strings.xml 的 accessibility_service_description（多空行排版，含 warinings 错拼）
- 应用内不可省略的授权弹窗：res/layout/dialog_ask_permission.xml（tv_title=permission_needed、tv_content=grant_app_permission、tv_action_1=grant_now），文案由 DialogAskPermission#O0 按权限类型切换
- 设置页之上的全屏半透明遮罩卡片：res/layout/activity_guide_setting.xml（find_and_grant、app_name、checked=true 的 SwitchCompat、pointing_hand 图、ic_close）
- GuildPermissionActivity.onCreate 动态拼接：getString(2131951809, app_name, 权限说明)，对 ACCESSIBILITY_SETTINGS 使用 2131951651 作为权限说明
- 云端 ATS 脚本随 Intent extra "ats" 传入 ForceStopAccessibility，脚本内含的节点匹配/点击文本静态不可见

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. | 点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。启用无障碍服务时你需要在 Android 系统警告中点击接受。Clean master 不会将这些权限用于此处列明之外的任何其他用途。 | `res/values/strings.xml key=accessibility_service_description` | 教唆忽视警告 |
| en | Permission Needed | 需要权限 | `res/values/strings.xml key=permission_needed（dialog_ask_permission.xml tv_title）` | 清理工具伪装 |
| en | Grant App Usage Permission for a comprehensive phone scan effect | 授予应用使用权限，以获得全面的手机扫描效果 | `res/values/strings.xml key=grant_app_permission（dialog_ask_permission.xml tv_content）` | 清理工具伪装 |
| en | Grant Now | 立即授权 | `res/values/strings.xml key=grant_now（dialog_ask_permission.xml tv_action_1）` | 未知 |
| en | Find %s and grant %s | 找到 %s 并授予 %s | `res/values/strings.xml key=find_and_grant（activity_guide_setting.xml tv_content）` | 受限设置分步教学 |
| en | Grant permission to use accessibility service | 授予使用无障碍服务的权限 | `res/values/strings.xml key=accessibility_setting_permission` | 受限设置分步教学 |
| en | Atom Clean-Booster, Antivirus | Atom 清理加速与杀毒（伪装成清理/杀毒工具的应用名，同时作为无障碍服务在系统列表中的显示名） | `res/values/strings.xml key=app_name（Manifest service android:label 引用同一 key）` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：弹窗本身可返回键或点击外部关闭（setCancelable(true)、setCanceledOnTouchOutside(true)），但 MainActivity.onResume 每次都会重跑 Y()/d0()，只要云控 status 仍为 needInstall 且未检测到 ForceStopAccessibility 已启用，就再次调用 g0() 弹出同一授权弹窗；只有云端下发 status=skip（并写入 skip 时间戳，超过 3600000ms 后还会重新拉取会话再要求）才停止。从系统设置页返回但未开启服务时，即触发该循环。
- **遮罩叠层 / 高仿系统设置页**：是。点击 Grant Now 后除跳转 android.settings.ACCESSIBILITY_SETTINGS 外，同一动作立即 startActivity 一个全屏半透明（#66000000）GuildPermissionActivity 叠在系统设置页之上，卡片内伪造系统开关行：应用图标 + app_name + checked=true 且 clickable=false 的 SwitchCompat + pointing_hand 手势图，文案 Find %s and grant %s，右上角仅有关闭图标。
- **Android 13+ 受限设置（Restricted Settings）应对**：无障碍环节未见“应用详情右上角菜单允许受限设置”的教学；但同一 Y() 流程在 canRequestPackageInstalls() 为 false 时会跳 android.settings.MANAGE_UNKNOWN_APP_SOURCES（package:<自身包名>），并在 ForceStopAccessibility 的脚本分支中按 data=source 再次拉起该页，属安装来源受限设置的引导。
- **获权后即时行为与防撤权机制**：获权瞬间 ForceStopAccessibility.onServiceConnected 直接 performGlobalAction(1)（GLOBAL_ACTION_BACK）自动退出系统设置页，200ms 后执行后续动作；脚本分支走完后同样 performGlobalAction(1) 并拉起 MainActivity。此外服务以云端下发的 ATS 脚本遍历无障碍节点执行 performAction(16) 自动点击（可用于自动确认系统弹窗、自动开启 MANAGE_OVERLAY_PERMISSION / MANAGE_UNKNOWN_APP_SOURCES），但未观察到监听设置页阻止用户撤销无障碍权限的代码。
- **良性降级 / 替代方案**：无。无替代的手动模式或仅观看模式；未授权时持续重复弹窗，且核心逻辑（远端 status/atsFull 驱动）直接依赖该服务。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动或 MainActivity 回到前台后立即监测两类事件：① 出现本应用 DialogFragment（robo_permission Lottie + 文本 Permission Needed / Grant Now）时立刻截图；② 监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 后 300–800ms 内立即抓取，此时 GuildPermissionActivity 遮罩已压栈，可捕获“系统设置页 + 伪造开关卡片”叠层画面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区在云端：会话 JSON 以 RSA/AES 加密存于 SharedPreferences 并由 http://statscodicefiscale.xyz/stats/ 下发，其中的 ATS 无障碍脚本（节点匹配与自动点击序列）静态不可见，获权后的自动点按行为需动态抓包或 Hook ForceStopAccessibility.onAccessibilityEvent 才能完整还原；此外 O0 中的权限说明字符串 id（如 2131951653）未逐一反查到资源 key。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | DialogFragment，含 LottieAnimationView(robo_permission.json)、TextView "Permission Needed"、按钮 "Grant Now"，无 Cancel 按钮，背景 dim 0.7 | 这是用户首次被要求授权的入口，能确认引导是冷启动即弹且话术以“全面扫描效果”包装 | 文本节点 Permission Needed；文本节点 Grant Now；Lottie 动画节点存在；仅一个可点击按钮、无 Cancel 文本；对话框层级属于 com.abbondioendrizzi.tools.supercleaner |
| **跳转后叠在系统无障碍设置页上的遮罩卡片** | GuildPermissionActivity（Theme.AppCompat.Translucent），底部约 120sdp 卡片，含 RoundedImageView(logo)、app_name 文本、checked=true 的 SwitchCompat、pointing_hand 图片、右上角 ic_close | 伪造系统开关是区分诱导与正常授权请求的最关键证据，可直接证明其刻意模仿系统 UI 状态 | 文本节点 Find Atom Clean-Booster, Antivirus and grant …；SwitchCompat checked=true 且 clickable=false；pointing_hand 图标节点；页面与系统 Settings 包名不同却覆盖在其上；半透明背景可见下层系统无障碍列表 |
| **系统无障碍服务列表项** | Settings 的 Accessibility 列表中名为 Atom Clean-Booster, Antivirus 的条目，描述为多空行 + Tap on top right use to Accessiblility service | 验证服务名复用应用名、描述教唆忽略系统警告，且与桌面品牌（Super Cleaner/Clean master）不一致 | 条目文本等于 app_name；描述含 warinings 错拼与大量空行；描述中出现 Super Cleaner / Clean master 品牌名 |
| **拒权返回后的重复弹窗页** | 从系统设置返回未开启服务后，再次出现的同一 Permission Needed 弹窗 | 证明存在 onResume 驱动的拒绝循环，而非一次性请求 | 同一弹窗文本在短时间内重复出现；弹窗出现时机与 MainActivity 回前台一致 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `d.a.a.a.j.s#Y`
- `d.a.a.a.j.s#d0`
- `com.abbondioendrizzi.tools.supercleaner.dialog.DialogAskPermission#O0`
- `d.a.a.a.j.c#a`
- `com.abbondioendrizzi.tools.supercleaner.screen.guildPermission.GuildPermissionActivity#onCreate`
- `com.abbondioendrizzi.tools.supercleaner.service.ForceStopAccessibility#onServiceConnected`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（静态可见，未遇加壳）。

## 结论要点

- **核心手法：清理工具伪装 + 遮罩叠层伪装系统开关 + 云控 ATS 脚本自动点按**。无障碍服务在 Manifest 中 label 复用 `@string/app_name`（“Atom Clean-Booster, Antivirus”），系统无障碍列表里看不出功能差异；其 `android:description` 却自称 “Super Cleaner / Clean master”，与桌面品牌不一致，并**明文教唆用户忽略 Android 系统警告**。
- **引导链路（运行期页面流转）**：`MainActivity.onResume` → `Y()` 判定云控会话状态 → 无无障碍权限时 `S("atsFull")` 拉起无障碍服务并把远端下发的 ATS 脚本塞进 `Intent`，同时 `g0()` 弹出 [DialogAskPermission](<resource-unit:#1.dex1 code:com.abbondioendrizzi.tools.supercleaner.dialog.DialogAskPermission#O0>)（Lottie 机器人动画 + “Permission Needed” + 唯一按钮 “Grant Now”）。
- 点击 “Grant Now” → `d.a.a.a.j.c#a` 先 `startActivity("android.settings.ACCESSIBILITY_SETTINGS")`，**紧接着** `GuildPermissionActivity.j0(...)` 把 [activity_guide_setting.xml](<resource-unit:#1 file:res/layout/activity_guide_setting.xml>) 全屏半透明遮罩（`#66000000`）压在系统设置页之上：卡片显示本应用图标 + 应用名 + **已勾选且 `clickable="false"` 的 SwitchCompat** + “pointing_hand” 手势图，文案 “Find %s and grant %s”，即高仿系统无障碍开关项。
- **获权后动作**：[ForceStopAccessibility.onServiceConnected](<resource-unit:#1.dex1 code:com.abbondioendrizzi.tools.supercleaner.service.ForceStopAccessibility#onServiceConnected>) 直接 `performGlobalAction(1)`（GLOBAL_ACTION_BACK）自动退离设置页，200ms 后回到主界面；随后 `onAccessibilityEvent` 按远端 ATS 脚本遍历节点 `performAction(16)` 自动点击，并支持自行跳 `MANAGE_OVERLAY_PERMISSION` / `MANAGE_UNKNOWN_APP_SOURCES`。
- **拒权反馈循环**：弹窗可被返回/点外部取消，但每次 `MainActivity.onResume` 都会重跑 `Y()`，只要未授权且云控 `status` 仍为 `needInstall` 就再次弹窗，形成反复拉起。

## 引导步骤拆解

| 步 | 阶段 | 载体 | 关键原文 | 锚点 |
|---|---|---|---|---|
| 1 | 冷启动/回前台触发 | MainActivity.onResume | 无（静默判定） | `MainActivity#onResume` → `d.a.a.a.j.s#Y` |
| 2 | 云端会话决策 | 远端 `http://statscodicefiscale.xyz/stats/` | `status=needInstall`、`atsFull` | `d.a.a.a.j.s#Y` / `#i0` / `#c0` |
| 3 | 引导说明页 | 原生 DialogFragment | “Permission Needed” / “Grant App Usage Permission for a comprehensive phone scan effect” / “Grant Now” | `DialogAskPermission#K0/#O0`，`res/layout/dialog_ask_permission.xml` |
| 4 | 跳系统无障碍设置 + 同时压遮罩 | 系统页 + 悬浮 Activity | “Find Atom Clean-Booster, Antivirus and grant …” | `d.a.a.a.j.c#a`，`GuildPermissionActivity#j0`，`res/layout/activity_guide_setting.xml` |
| 5 | 获权后自动退页并接管 | AccessibilityService | 无（静默 `performGlobalAction(1)`） | `ForceStopAccessibility#onServiceConnected` |

## 文本呈现位置

1. 系统无障碍列表条目描述：`res/values/strings.xml` 的 `accessibility_service_description`（多空行、错拼 “warinings”）。
2. 应用内弹窗：`res/layout/dialog_ask_permission.xml`（标题/正文/按钮三处字符串）。
3. 设置页叠层：`res/layout/activity_guide_setting.xml`（`find_and_grant` + `app_name` + 假开关 + 手势图）。
4. `GuildPermissionActivity.onCreate` 按 `permission name` 动态换文案（`getString(2131951809, app_name, <权限说明>)`）。

## 需说明的边界

- 云控下发内容经 RSA/AES 加密（`"IIBCgKCAQEitAu9qo1QgM8FH7"` 前缀）从 `statscodicefiscale.xyz` 取回，具体 ATS 脚本步骤静态不可见；页面流转骨架则完全静态可见。
- `2131951653` 等字符串 id 未逐一反查确认到 key，已在 `verbatim_texts` 中标注为 layout 默认文案。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 未加壳，引导链路的 Activity/Dialog/遮罩布局与跳转代码完全静态可见；仅云控会话 JSON（RSA/AES 加密的 SESSION）与下发的 ATS 无障碍脚本步骤来自 http://statscodicefiscale.xyz/stats/，属远端内容，不影响 UTG 页面流转判定。",
  "summary_one_liner": "以清理工具外壳，冷启动/回前台即弹不可跳过的授权弹窗，点 Grant Now 后跳系统无障碍设置并同时压入伪装系统开关的悬浮遮罩层，获权后由无障碍服务自动 BACK 退出设置页并按云端脚本自动点按。",
  "disguise_identity": {
    "app_display_name": "Atom Clean-Booster, Antivirus",
    "claimed_brand_or_persona": "伪装为手机清理/加速/杀毒工具（描述文本中自称 Super Cleaner、Clean master，与桌面显示名 Atom Clean-Booster 不一致）",
    "a11y_service_label": "Atom Clean-Booster, Antivirus（服务 android:label 直接复用 @string/app_name，未声明独立无障碍服务名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍描述中插入大量空行与换行挤开系统警告文案（\"Tap on top right use to Accessiblility service.\" 后接多空行），并用错拼 warinings/orther 规避关键词；无障碍服务 label 复用应用名以隐藏真实用途；遮罩层用 checked=true 且 clickable=false 的 SwitchCompat 伪造系统开关状态；描述中品牌名（Super Cleaner / Clean master）与包名及 app_name 不一致。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.abbondioendrizzi.tools.supercleaner.screen.main.MainActivity",
      "trigger_event": "onResume（每次回到前台都会重新执行）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "主界面无提示，静默进入云端会话判定",
      "user_action_requested": "无，用户被动进入",
      "code_anchor": "MainActivity.onResume -> d.a.a.a.j.s.Y"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "d.a.a.a.j.s（BaseActivity）与远端 http://statscodicefiscale.xyz/stats/",
      "trigger_event": "Y() 读取 SharedPreferences SESSION，经 d.a.a.a.c.d 解密失败则本地构造 c0() 并 POST 上报（APP_NAME=cleaner1、CLIENT_ID、机型、locale、已装应用列表 apps2、overlay、source）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（网络请求，无 UI）",
      "shown_text_zh": "云端返回 status=needInstall 时进入无障碍授权流程",
      "user_action_requested": "无",
      "code_anchor": "d.a.a.a.j.s#Y / #i0 / #c0"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.abbondioendrizzi.tools.supercleaner.dialog.DialogAskPermission（DialogFragment，内容由 g0() 以 android.settings.ACCESSIBILITY_SETTINGS 构造）",
      "trigger_event": "Y() 中 U() 判定未授予无障碍权限后调用 g0()；d0() 在 status=needInstall 且未授权时同样调用 g0()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission Needed / Grant App Usage Permission for a comprehensive phone scan effect / Grant Now（Lottie robo_permission.json 机器人动画；O0 对 ACCESSIBILITY_SETTINGS 改用 2131951653 文案）",
      "shown_text_zh": "“需要权限” / “授予应用使用权限以获得全面的手机扫描效果” / “立即授权”",
      "user_action_requested": "点击唯一按钮 Grant Now 前往授权；无 Cancel 按钮，但 Dialog 被设为 setCancelable(true)、setCanceledOnTouchOutside(true)，可返回键或点外部关闭",
      "code_anchor": "DialogAskPermission#K0 / #O0 / #click / #k0，res/layout/dialog_ask_permission.xml"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统 Settings 的 ACTION_ACCESSIBILITY_SETTINGS 页",
      "trigger_event": "点击 Grant Now → DialogAskPermission#click → d.a.a.a.j.c#a",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（直接 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))）",
      "shown_text_zh": "打开系统无障碍服务列表，要求用户找到本应用并开启",
      "user_action_requested": "在系统列表中找到 Atom Clean-Booster, Antivirus 并打开开关",
      "code_anchor": "d.a.a.a.j.c#a"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.abbondioendrizzi.tools.supercleaner.screen.guildPermission.GuildPermissionActivity（全屏半透明遮罩 + 底部卡片，模拟系统开关行）",
      "trigger_event": "同一次点击中紧跟 startActivity 调用 GuildPermissionActivity.j0(context, \"android.settings.ACCESSIBILITY_SETTINGS\")，压栈叠在系统设置页之上",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Find %s and grant %s（实际渲染为 Find Atom Clean-Booster, Antivirus and grant <权限说明>）+ 应用图标 + 应用名 + 已勾选且不可点击的 SwitchCompat + pointing_hand 手势图 + 右上角关闭图标",
      "shown_text_zh": "“找到 Atom Clean-Booster, Antivirus 并授予权限”，并显示一个已处于开启状态的开关与指向手势，诱导用户照此在系统页操作",
      "user_action_requested": "按遮罩指引在系统无障碍页找到该条目并打开开关；右上角有关闭图标可退出遮罩",
      "code_anchor": "GuildPermissionActivity#onCreate / #j0，res/layout/activity_guide_setting.xml，res/values/strings.xml#find_and_grant"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.abbondioendrizzi.tools.supercleaner.service.ForceStopAccessibility（独立进程 :BackgroundService）",
      "trigger_event": "onServiceConnected 回调；此前 Y() 已通过 S(\"atsFull\") 用 Intent extra 注入云端下发的 ats 脚本与 clienid",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（performGlobalAction(1) 即 GLOBAL_ACTION_BACK，200ms 后 a(this)）",
      "shown_text_zh": "获权瞬间自动模拟返回键退出系统设置页并跳回主界面，用户看不到停留过程",
      "user_action_requested": "无",
      "code_anchor": "ForceStopAccessibility#onServiceConnected / #onAccessibilityEvent / #onStartCommand"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onResume → d.a.a.a.j.s#Y / #d0 → g0()",
      "trigger_event": "用户从设置页返回但未开启服务时再次触发 onResume",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Permission Needed / Grant Now（重复出现）",
      "shown_text_zh": "再次弹出同一授权弹窗，直到云控 status 变为 skip（并写入 1 小时 skip 时间戳）或授权成功",
      "user_action_requested": "反复要求点击 Grant Now；U() 中 skip 超过 3600000ms 后会重新拉取会话再次要求",
      "code_anchor": "MainActivity#onResume，d.a.a.a.j.s#Y / #d0 / #U"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目描述：res/values/strings.xml 的 accessibility_service_description（多空行排版，含 warinings 错拼）",
    "应用内不可省略的授权弹窗：res/layout/dialog_ask_permission.xml（tv_title=permission_needed、tv_content=grant_app_permission、tv_action_1=grant_now），文案由 DialogAskPermission#O0 按权限类型切换",
    "设置页之上的全屏半透明遮罩卡片：res/layout/activity_guide_setting.xml（find_and_grant、app_name、checked=true 的 SwitchCompat、pointing_hand 图、ic_close）",
    "GuildPermissionActivity.onCreate 动态拼接：getString(2131951809, app_name, 权限说明)，对 ACCESSIBILITY_SETTINGS 使用 2131951651 作为权限说明",
    "云端 ATS 脚本随 Intent extra \"ats\" 传入 ForceStopAccessibility，脚本内含的节点匹配/点击文本静态不可见"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "text_zh": "点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾、休眠耗电应用。启用无障碍服务时你需要在 Android 系统警告中点击接受。Clean master 不会将这些权限用于此处列明之外的任何其他用途。",
      "source_location": "res/values/strings.xml key=accessibility_service_description",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Permission Needed",
      "text_zh": "需要权限",
      "source_location": "res/values/strings.xml key=permission_needed（dialog_ask_permission.xml tv_title）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant App Usage Permission for a comprehensive phone scan effect",
      "text_zh": "授予应用使用权限，以获得全面的手机扫描效果",
      "source_location": "res/values/strings.xml key=grant_app_permission（dialog_ask_permission.xml tv_content）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant Now",
      "text_zh": "立即授权",
      "source_location": "res/values/strings.xml key=grant_now（dialog_ask_permission.xml tv_action_1）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Find %s and grant %s",
      "text_zh": "找到 %s 并授予 %s",
      "source_location": "res/values/strings.xml key=find_and_grant（activity_guide_setting.xml tv_content）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant permission to use accessibility service",
      "text_zh": "授予使用无障碍服务的权限",
      "source_location": "res/values/strings.xml key=accessibility_setting_permission",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Atom Clean-Booster, Antivirus",
      "text_zh": "Atom 清理加速与杀毒（伪装成清理/杀毒工具的应用名，同时作为无障碍服务在系统列表中的显示名）",
      "source_location": "res/values/strings.xml key=app_name（Manifest service android:label 引用同一 key）",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "弹窗本身可返回键或点击外部关闭（setCancelable(true)、setCanceledOnTouchOutside(true)），但 MainActivity.onResume 每次都会重跑 Y()/d0()，只要云控 status 仍为 needInstall 且未检测到 ForceStopAccessibility 已启用，就再次调用 g0() 弹出同一授权弹窗；只有云端下发 status=skip（并写入 skip 时间戳，超过 3600000ms 后还会重新拉取会话再要求）才停止。从系统设置页返回但未开启服务时，即触发该循环。",
    "overlay_or_fake_settings": "是。点击 Grant Now 后除跳转 android.settings.ACCESSIBILITY_SETTINGS 外，同一动作立即 startActivity 一个全屏半透明（#66000000）GuildPermissionActivity 叠在系统设置页之上，卡片内伪造系统开关行：应用图标 + app_name + checked=true 且 clickable=false 的 SwitchCompat + pointing_hand 手势图，文案 Find %s and grant %s，右上角仅有关闭图标。",
    "restricted_settings_13plus_coaching": "无障碍环节未见“应用详情右上角菜单允许受限设置”的教学；但同一 Y() 流程在 canRequestPackageInstalls() 为 false 时会跳 android.settings.MANAGE_UNKNOWN_APP_SOURCES（package:<自身包名>），并在 ForceStopAccessibility 的脚本分支中按 data=source 再次拉起该页，属安装来源受限设置的引导。",
    "post_grant_anti_removal": "获权瞬间 ForceStopAccessibility.onServiceConnected 直接 performGlobalAction(1)（GLOBAL_ACTION_BACK）自动退出系统设置页，200ms 后执行后续动作；脚本分支走完后同样 performGlobalAction(1) 并拉起 MainActivity。此外服务以云端下发的 ATS 脚本遍历无障碍节点执行 performAction(16) 自动点击（可用于自动确认系统弹窗、自动开启 MANAGE_OVERLAY_PERMISSION / MANAGE_UNKNOWN_APP_SOURCES），但未观察到监听设置页阻止用户撤销无障碍权限的代码。",
    "benign_graceful_degradation": "无。无替代的手动模式或仅观看模式；未授权时持续重复弹窗，且核心逻辑（远端 status/atsFull 驱动）直接依赖该服务。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动或 MainActivity 回到前台后立即监测两类事件：① 出现本应用 DialogFragment（robo_permission Lottie + 文本 Permission Needed / Grant Now）时立刻截图；② 监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 后 300–800ms 内立即抓取，此时 GuildPermissionActivity 遮罩已压栈，可捕获“系统设置页 + 伪造开关卡片”叠层画面。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "DialogFragment，含 LottieAnimationView(robo_permission.json)、TextView \"Permission Needed\"、按钮 \"Grant Now\"，无 Cancel 按钮，背景 dim 0.7",
        "why_most_useful": "这是用户首次被要求授权的入口，能确认引导是冷启动即弹且话术以“全面扫描效果”包装",
        "observable_utg_signals": ["文本节点 Permission Needed", "文本节点 Grant Now", "Lottie 动画节点存在", "仅一个可点击按钮、无 Cancel 文本", "对话框层级属于 com.abbondioendrizzi.tools.supercleaner"]
      },
      {
        "page_role": "跳转后叠在系统无障碍设置页上的遮罩卡片",
        "page_identifier": "GuildPermissionActivity（Theme.AppCompat.Translucent），底部约 120sdp 卡片，含 RoundedImageView(logo)、app_name 文本、checked=true 的 SwitchCompat、pointing_hand 图片、右上角 ic_close",
        "why_most_useful": "伪造系统开关是区分诱导与正常授权请求的最关键证据，可直接证明其刻意模仿系统 UI 状态",
        "observable_utg_signals": ["文本节点 Find Atom Clean-Booster, Antivirus and grant …", "SwitchCompat checked=true 且 clickable=false", "pointing_hand 图标节点", "页面与系统 Settings 包名不同却覆盖在其上", "半透明背景可见下层系统无障碍列表"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 的 Accessibility 列表中名为 Atom Clean-Booster, Antivirus 的条目，描述为多空行 + Tap on top right use to Accessiblility service",
        "why_most_useful": "验证服务名复用应用名、描述教唆忽略系统警告，且与桌面品牌（Super Cleaner/Clean master）不一致",
        "observable_utg_signals": ["条目文本等于 app_name", "描述含 warinings 错拼与大量空行", "描述中出现 Super Cleaner / Clean master 品牌名"]
      },
      {
        "page_role": "拒权返回后的重复弹窗页",
        "page_identifier": "从系统设置返回未开启服务后，再次出现的同一 Permission Needed 弹窗",
        "why_most_useful": "证明存在 onResume 驱动的拒绝循环，而非一次性请求",
        "observable_utg_signals": ["同一弹窗文本在短时间内重复出现", "弹窗出现时机与 MainActivity 回前台一致"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区在云端：会话 JSON 以 RSA/AES 加密存于 SharedPreferences 并由 http://statscodicefiscale.xyz/stats/ 下发，其中的 ATS 无障碍脚本（节点匹配与自动点击序列）静态不可见，获权后的自动点按行为需动态抓包或 Hook ForceStopAccessibility.onAccessibilityEvent 才能完整还原；此外 O0 中的权限说明字符串 id（如 2131951653）未逐一反查到资源 key。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "d.a.a.a.j.s#Y",
    "d.a.a.a.j.s#d0",
    "com.abbondioendrizzi.tools.supercleaner.dialog.DialogAskPermission#O0",
    "d.a.a.a.j.c#a",
    "com.abbondioendrizzi.tools.supercleaner.screen.guildPermission.GuildPermissionActivity#onCreate",
    "com.abbondioendrizzi.tools.supercleaner.service.ForceStopAccessibility#onServiceConnected"
  ]
}
```

</details>
