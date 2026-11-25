# MR_006__3dc2f2a200｜hawkshaw — SecurIt

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：131.6s

## 1. 一句话核心结论

- **核心申请方式**：以“SecurIt/隐私工具”外壳在登录后冷启动即弹出不可取消的原生弹窗，诱骗用户为冒名“System Settings”的无障碍服务授权，取消不生效、未授权返回即重弹，随后串行索取通知使用权、设备管理器、录屏、悬浮窗并引导进应用详情页开启受限设置，获权瞬间用 GLOBAL_ACTION_BACK 自动退出设置页。
- **静态可见性说明**：无障碍引导全链路（HawkshawMainActivity 冷启动→不可取消 AlertDialog→ACTION_ACCESSIBILITY_SETTINGS→onActivityResult 回检与重弹→后续权限阶梯→Accessibility.onServiceConnected 自动返回键）均为明文 DEX 代码，未见加壳/VMP/密文动态加载；仅 R.string.enable_accessibility_header/message 与 additional_permissions_text 的字面值位于 resources.arsc（解包目录无 values/ 未逐字还原），res/xml/accessibility_service_config.xml 为二进制 XML 但 label/description 已由 Manifest 视图确认。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3dc2f2a200630294fc0af904ddf611f9ecfe8a4c65899aff8d6b56aed53177f8` |
| 包名 / 年份 | `se.joscarsson.privify.spitfire` / 2021 |
| 家族 / 品类 | **hawkshaw**（同池样本数：48） |
| 原始来源标识 | https://research.checkpoint.com/2021/going-rogue-a-mastermind-behind-android-malware-returns-with-a-new-rat/ |
| 桌面显示名 | SecurIt |
| 引导页宣称品牌/身份 | SecurIt（se.joscarsson.privify.spitfire，自称帮助保护/加固设备的隐私安全工具；实际核心库为 me.hawkshaw 的 hawkshawlib_release，FIREBASE_ACCOUNT=HAWKSHAW） |
| 系统无障碍列表服务名 | System Settings |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务在系统列表中直接冒用系统组件名“System Settings”（R.string @7F0E001C），配以笼统的隐私承诺式 description“Accessibility helps us to secure your device”；服务真实类 me.hawkshaw.tasks.Accessibility 与包名 se.joscarsson.privify 无命名关联，入口 Activity HawkshawMainActivity 设 excludeFromRecents 不在桌面暴露；无空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool 的证据 |
| 无障碍服务类名 | `me.hawkshaw.tasks.Accessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Accessibility helps us to secure your device |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | se.joscarsson.privify.ui.MainActivity（LAUNCHER）→ me.hawkshaw.HawkshawMainActivity（excludeFromRecents） | onCreate：!isPermissionsGiven() 或 intent extra FORCE_OPEN_PERMISSIONS=true 时执行 LoginUtils.initLogin()，登录成功回调 HawkshawMainActivity$onCreate$1.invoke(true) | 原生Activity | **原文**：activityStarted<br>**译注**：启动即向全局命令 LiveData 投递“activityStarted”（非 UI 文案）；界面为 R$layout.activity_main_lib + 进度条 | 完成登录/等待初始化（无跳过权限的入口） | `me.hawkshaw.HawkshawMainActivity.onCreate；me.hawkshaw.HawkshawMainActivity$onCreate$1.invoke` |
| 2 | 引导说明页 | HawkshawMainActivity 内 AlertDialog（enableAccessibility） | 登录成功回调 → HawkshawMainActivity.a(this,0,1,null)；若 b()（已启用无障碍）为 false 则 show() | 原生Dialog | **原文**：R.string.enable_accessibility_header / R.string.enable_accessibility_message（resources.arsc，未逐字取回）；按钮 "R.string.ok" / "R.string.cancel"<br>**译注**：标题与正文为“开启无障碍”说明文案（具体字面值位于 resources.arsc），按钮为“确定/取消”；对话框 setCancelable(false) 不可点外部或返回键关闭 | 点“确定”前往无障碍设置；点“取消”同样继续后续权限链，无真正跳过 | `me.hawkshaw.HawkshawMainActivity.a(HawkshawMainActivity,int,int,Object)（enableAccessibility）` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 确定按钮 onClick → startActivityForResult(intent, requestCode=0) | 系统无障碍页 | 无 | 在系统列表中找到“System Settings”并打开其开关（无应用内引导遮罩或高亮提示） | `me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick；res/xml/accessibility_service_config.xml；Manifest service me.hawkshaw.tasks.Accessibility（label @7F0E001C）` |
| 4 | 拒权反馈循环 | HawkshawMainActivity.onActivityResult(requestCode=0) → 重入 enableAccessibility | 用户从无障碍设置返回；b() 仍为 false | 原生Dialog | **原文**：R.string.enable_accessibility_header / R.string.enable_accessibility_message<br>**译注**：未授权即再次弹出同一不可取消的引导对话框，循环直至授权 | 只能再次点“确定”去授权（取消分支仅推进到下一权限步骤，不结束流程） | `me.hawkshaw.HawkshawMainActivity.onActivityResult（case 0）；me.hawkshaw.HawkshawMainActivity$enableAccessibility$2.onClick` |
| 5 | 拒权反馈循环 | 系统权限对话框 / 通知使用权说明 Dialog / ADD_DEVICE_ADMIN / MANAGE_OVERLAY_PERMISSION | 无障碍步骤结束后 requestCode 1→6 串行推进；onRequestPermissionsResult 中 tries（初值3）递减后重新 requestPermissions | 原生Dialog | **原文**：Enable Read Notifications / Locate System Settings in settings and enable it.<br>Push notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings<br>**译注**：“启用通知读取：在设置中找到系统设置并开启它。推送通知能带来更好的体验并促进你的学习进度，你随时可在应用设置中更改”（setCancelable(false)，OK/Cancel） | 开启通知使用权、忽略电池优化、录屏、设备管理器、悬浮窗；运行时权限最多被重复索取 3 轮 | `me.hawkshaw.HawkshawMainActivity.onActivityResult（case 1-6）；me.hawkshaw.HawkshawMainActivity.onRequestPermissionsResult` |
| 6 | 引导说明页 | Additional Permissions Dialog → 系统 android.settings.APPLICATION_DETAILS_SETTINGS（应用详情页） | requestCode=7：AlertDialog setCancelable(false)，确定按钮 HawkshawMainActivity$openAppSettings$1.onClick | 原生Dialog | **原文**：Additional Permissions；R.string.additional_permissions_text = "Please take a look at settings and provide extra permissions if needed. 1. Enable AutoStart. 2. Allow display pop-up window from Other Permi…"<br>**译注**：“请查看设置并按需提供额外权限：1. 开启自启动；2. 允许来自其他应用的弹出窗口…”——典型受限设置分步教学，引导进应用详情页（右上角菜单允许受限设置），并针对小米跳转 miui.intent.action.APP_PERM_EDITOR | 进入应用详情页手动放开受限设置/自启动/后台弹出，无跳过路径 | `me.hawkshaw.HawkshawMainActivity.onActivityResult（case 7）；me.hawkshaw.HawkshawMainActivity$openAppSettings$1.onClick；me.hawkshaw.HawkshawMainActivity.a(int)（MIUI PermissionsEditorActivity）` |
| 7 | 获权后动作 | me.hawkshaw.tasks.Accessibility.onServiceConnected | 用户开启服务后系统回调 onServiceConnected；isActivityRunning 为真 | 系统无障碍页 | 无 | 无（用户无操作，界面被自动退出） | `me.hawkshaw.tasks.Accessibility.onServiceConnected；me.hawkshaw.tasks.Accessibility$onServiceConnected$1.run；me.hawkshaw.tasks.Accessibility$grantPermissions$2.run` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- HawkshawMainActivity 内 setCancelable(false) 的原生 AlertDialog（标题/正文取 R.string.enable_accessibility_header / enable_accessibility_message），在登录成功后与用户从设置返回未授权时反复弹出
- 同一 Activity 内 setCancelable(false) 的“Enable Read Notifications”原生 Dialog（硬编码英文正文，含“Locate System Settings in settings and enable it”）
- 同一 Activity 内 setCancelable(false) 的“Additional Permissions”原生 Dialog，正文取 R.string.additional_permissions_text（自启动/后台弹窗分步教学）
- 系统无障碍服务列表项：service label=R.string @7F0E001C = “System Settings”，android:description = “Accessibility helps us to secure your device”（res/xml/accessibility_service_config.xml）
- 系统应用详情页（android.settings.APPLICATION_DETAILS_SETTINGS）——应用自身不绘制内容，仅负责跳转
- 小米设备跳转 com.miui.securitycenter/com.miui.permcenter.permissions.PermissionsEditorActivity（miui.intent.action.APP_PERM_EDITOR）
- 未发现本地 HTML/WebView 引导页、GIF/图片引导或叠放在系统设置页上的半透明遮罩层

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | System Settings | 系统设置 | `AndroidManifest.xml service me.hawkshaw.tasks.Accessibility android:label=@7F0E001C（res/values 内 R.string，已由 Manifest 视图确认字面值）` | 未知 |
| en | Accessibility helps us to secure your device | 无障碍功能帮助我们保护你的设备安全 | `res/xml/accessibility_service_config.xml → android:description（Manifest meta-data @7F110000）` | 隐私承诺 |
| en | Enable Read Notifications | 启用通知读取 | `me.hawkshaw.HawkshawMainActivity.onActivityResult case 3（硬编码 AlertDialog.setTitle）` | 良性透明说明 |
| en | Locate System Settings in settings and enable it.<br>Push notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings | 在设置中找到“系统设置”并开启它。推送通知能带来更好的使用体验并促进你的学习进度。你随时可以在应用设置中更改。 | `me.hawkshaw.HawkshawMainActivity.onActivityResult case 3（硬编码 AlertDialog.setMessage）` | 受限设置分步教学 |
| en | Additional Permissions | 附加权限 | `me.hawkshaw.HawkshawMainActivity.onActivityResult case 7（AlertDialog.setTitle）` | 受限设置分步教学 |
| en | Please take a look at settings and provide extra permissions if needed. 1. Enable AutoStart. 2. Allow display pop-up window from Other Permi… | 请查看设置并按需提供额外权限：1. 开启自启动。2. 允许来自其他应用的弹出窗口… | `R.string.additional_permissions_text（resources.arsc，预筛字符串命中，代码引用点 HawkshawMainActivity.onActivityResult case 7）` | 受限设置分步教学 |
| en | Enable Google Play services | 启用 Google Play 服务 | `Google Play services 缺失提示（预筛字符串，com.google.android.gms 标准错误对话框资源）` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：两层循环：①无障碍——从 ACCESSIBILITY_SETTINGS 返回后 onActivityResult(case 0) 重新判断 b()，未授权即再次 show() 同一个 setCancelable(false) 的引导对话框，形成设置页与弹窗之间的往复；②运行时权限——onRequestPermissionsResult 中任一权限被拒即 tries-1 并重新 requestPermissions，初值 3 轮；此外取消按钮（$enableAccessibility$2.onClick）不中断流程，直接以 onActivityResult(i,…) 推进到下一项权限索取
- **遮罩叠层 / 高仿系统设置页**：无。未发现叠放半透明引导遮罩、全屏悬浮窗指引或高仿系统无障碍开关页；悬浮窗（SYSTEM_ALERT_WINDOW）仅是权限阶梯中的独立一环，用于后续能力而非无障碍引导
- **Android 13+ 受限设置（Restricted Settings）应对**：有。“Additional Permissions”不可取消弹窗列出“1. Enable AutoStart 2. Allow display pop-up window from Other Permi…”，确定后经 android.settings.APPLICATION_DETAILS_SETTINGS 打开本应用详情页，引导用户手动放开受限设置；小米设备另走 miui.intent.action.APP_PERM_EDITOR（com.miui.securitycenter PermissionsEditorActivity）。未见 Session 安装器绕过方式
- **获权后即时行为与防撤权机制**：有。Accessibility.onServiceConnected 在 isActivityRunning 为真时立即 performGlobalAction(1)（GLOBAL_ACTION_BACK），并 postDelayed 300ms 再次触发返回动作，自动退出无障碍设置页；类内另有 grantPermissions（经 Accessibility$grantPermissions$2.run 使用 performGlobalAction 遍历节点点击确认）与 preventUninstall 方法，具备获权后自点授权与阻止撤权的实现
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 HawkshawMainActivity 前台（excludeFromRecents、包名 se.joscarsson.privify.spitfire、Activity 类名含 me.hawkshaw）且出现 setCancelable(false) 的 AlertDialog 时立即抓取；或 Hook startActivityForResult 中 action=android.settings.ACCESSIBILITY_SETTINGS（调用方 me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick）时同步抓取跳转前一帧，并在返回本应用后 1 秒内再次抓取以捕获重弹循环
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导全部为原生文本控件（AlertDialog + 系统设置页），UTG 文本可直接提取，无纯图空文本盲区；但系统无障碍设置页与应用内弹窗之间切换极快（获权后 300ms 内两次 GLOBAL_ACTION_BACK 自动退出），若抓取频率低可能漏掉“已开启服务瞬间”的页面；resources.arsc 中 enable_accessibility_header/message 的原文需以运行期 UTG 文本补全，静态侧仅确认资源 key

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（无障碍授权前）** | 包名 se.joscarsson.privify.spitfire，Activity me.hawkshaw.HawkshawMainActivity，不可取消 AlertDialog，按钮文本为 OK/Cancel | 这是判定“冷启动即强制索取无障碍”的直接证据，且可确认是否存在取消/跳过路径 | 对话框是否可点外部/返回键关闭（cancelable=false）；标题/正文文本与按钮文本；弹出时机是否在登录完成回调之后立即出现；是否同时出现 progress 进度条隐藏后的页面（activity_main_lib） |
| **系统无障碍服务列表项** | android.settings.ACCESSIBILITY_SETTINGS 页面中名为“System Settings”的服务条目及其描述文本 | 直接证明身份冒用：服务名与系统设置同名，描述为笼统隐私承诺，是判定伪装与诱导的核心页面 | 条目名称文本 System Settings；描述文本 Accessibility helps us to secure your device；条目归属应用为 SecurIt / se.joscarsson.privify.spitfire；开关初始为关闭 |
| **从设置返回后的重弹遮罩/弹窗页** | 返回本应用 1 秒内再次出现的同一 AlertDialog（相同标题与按钮） | 区分“一次性说明”与“拒权死循环强制”，是判定强制性与无降级路径的关键 | 未授权返回后同一对话框重复出现次数；是否存在退出/跳过按钮；返回键是否可关闭对话框；是否伴随 Activity 栈在设置页与本应用间往复 |
| **附加权限与受限设置教学弹窗** | 标题 Additional Permissions 的不可取消 AlertDialog，以及随后打开的 android.settings.APPLICATION_DETAILS_SETTINGS 应用详情页 | 证明应用在无障碍之外继续诱导开启自启动/后台弹窗等受限设置，属分步教学与提权链延伸 | 弹窗标题与正文条目（Enable AutoStart / 后台弹窗）；跳转 intent action 是否为 APPLICATION_DETAILS_SETTINGS；是否出现 MIUI PermissionsEditorActivity；无障碍授权成功后是否自动返回键退出设置页（GLOBAL_ACTION_BACK 造成的界面跳变） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `me.hawkshaw.HawkshawMainActivity.onCreate`
- `me.hawkshaw.HawkshawMainActivity.a(HawkshawMainActivity,int,int,Object)（enableAccessibility，setCancelable(false) 引导弹窗）`
- `me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick（startActivityForResult android.settings.ACCESSIBILITY_SETTINGS）`
- `me.hawkshaw.HawkshawMainActivity.onActivityResult（case 0 重弹 / case 3 通知使用权 / case 6 悬浮窗 / case 7 APPLICATION_DETAILS_SETTINGS 受限设置教学）`
- `me.hawkshaw.HawkshawMainActivity.onRequestPermissionsResult（tries 递减重请求）`
- `me.hawkshaw.tasks.Accessibility.onServiceConnected（GLOBAL_ACTION_BACK + 300ms 延迟返回）`
- `res/xml/accessibility_service_config.xml（android:description=Accessibility helps us to secure your device）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**流程（纯静态可完整还原，无加壳）**

1. **冷启动入口**：Launcher 为 `se.joscarsson.privify.ui.MainActivity`（显示名 SecurIt），流程最终落到 Manifest 中登记的隐藏入口 [me.hawkshaw.HawkshawMainActivity](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity>)（`excludeFromRecents`）。其 `onCreate` 强制 `setContentView(R$layout.activity_main_lib)`、向全局 `LiveData` 投递 `"activityStarted"`，并在 `!isPermissionsGiven()` 或带 `FORCE_OPEN_PERMISSIONS` extra 时执行 `LoginUtils.initLogin()`；登录成功回调后立即进入无障碍引导，失败则 `showLoginUI`，即**权限引导被放在 Firebase 登录之后，且与主业务无关**。
2. **引导弹窗**：[HawkshawMainActivity.a(HawkshawMainActivity,int,int,Object)](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity#a>) 即 `enableAccessibility`：`AlertDialog.Builder(...).setCancelable(false)`，标题/正文取 `R.string.enable_accessibility_header` / `enable_accessibility_message`（位于 `resources.arsc`，未解码出 `values/`）。若 `b()`（`AccessibilityManager.getEnabledAccessibilityServiceList` 中已存在 `包名/me.hawkshaw.tasks.Accessibility`）为真则跳过，否则弹窗。
3. **跳系统无障碍页**：确定按钮 [HawkshawMainActivity$enableAccessibility$1.onClick](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity$enableAccessibility$1#onClick>) 直接 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`；**取消按钮（`$enableAccessibility$2.onClick`）并不终止流程**，而是同样回调 `onActivityResult(i,…)` 推进到下一权限步骤。
4. **拒权反馈循环**：`onActivityResult` case 0 中，若 `b()` 仍为 false，则再次 `a(this,0,1,null)` **重弹同一个不可取消对话框**；后续运行时权限在 `onRequestPermissionsResult` 中以 `tries`（初值 3）计数，任一拒绝即 `tries--` 后重新 `requestPermissions`，最多连拉 3 轮。
5. **权限链式阶梯（同一 Activity 内 requestCode 0→7 串行）**：无障碍(0) → 忽略电池优化(1) → MediaProjection 录屏(2) → 通知使用权(3，`setCancelable(false)`，文案"Locate System Settings in settings and enable it…promote your learning progress") → 设备管理器 `ADD_DEVICE_ADMIN`(4) → 小米 MIUI `miui.intent.action.APP_PERM_EDITOR`(5) → 悬浮窗 `MANAGE_OVERLAY_PERMISSION`(6) → "Additional Permissions" 弹窗(7) 引导到 `android.settings.APPLICATION_DETAILS_SETTINGS`（[HawkshawMainActivity$openAppSettings$1.onClick](<resource-unit:#1.dex1 code:me.hawkshaw.HawkshawMainActivity$openAppSettings$1#onClick>)）打开应用详情页，即 Android 13+ 受限设置分步教学。全部通过后才写 `IS_PERMISSIONS_GIVEN=true` 并 `finish()`。
6. **获权后对抗**：[Accessibility.onServiceConnected](<resource-unit:#1.dex1 code:me.hawkshaw.tasks.Accessibility#onServiceConnected>) 在 `isActivityRunning` 为真时立即 `performGlobalAction(1)`（`GLOBAL_ACTION_BACK`）并 `postDelayed(300ms)` 再触发一次返回，即用户刚开启服务就自动退出设置页；类内另有 `grantPermissions`（`Accessibility$grantPermissions$2.run` 内 `performGlobalAction`）与 `preventUninstall`，属获权后自点授权/阻止撤权能力。

**身份伪装**：无障碍服务在系统列表中显示 `@7F0E001C` = **"System Settings"**，`android:description` = "Accessibility helps us to secure your device"，而真实服务类为 `me.hawkshaw.tasks.Accessibility`（`hawkshawlib_release` 库，与包名 `se.joscarsson.privify` 无命名关联），Manifest 另存 `FIREBASE_ACCOUNT=HAWKSHAW`。**未发现**空白/换行挤出警告、同形字、多 `activity-alias` 或伪造 `isAccessibilityTool`；**未发现**针对无障碍引导的半透明遮罩/高仿系统开关页（悬浮窗权限是链上独立一环，用于其他能力）。

**边界**：`enable_accessibility_header/message`、`additional_permissions_text` 原文位于 `resources.arsc` 内（解包目录无 `values/`），本次仅按资源 key 定位，未逐字取回；`$enableAccessibility$2.onClick` 内部实现按调用关系推断，未逐行读取。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（HawkshawMainActivity 冷启动→不可取消 AlertDialog→ACTION_ACCESSIBILITY_SETTINGS→onActivityResult 回检与重弹→后续权限阶梯→Accessibility.onServiceConnected 自动返回键）均为明文 DEX 代码，未见加壳/VMP/密文动态加载；仅 R.string.enable_accessibility_header/message 与 additional_permissions_text 的字面值位于 resources.arsc（解包目录无 values/ 未逐字还原），res/xml/accessibility_service_config.xml 为二进制 XML 但 label/description 已由 Manifest 视图确认。",
  "summary_one_liner": "以“SecurIt/隐私工具”外壳在登录后冷启动即弹出不可取消的原生弹窗，诱骗用户为冒名“System Settings”的无障碍服务授权，取消不生效、未授权返回即重弹，随后串行索取通知使用权、设备管理器、录屏、悬浮窗并引导进应用详情页开启受限设置，获权瞬间用 GLOBAL_ACTION_BACK 自动退出设置页。",
  "disguise_identity": {
    "app_display_name": "SecurIt",
    "claimed_brand_or_persona": "SecurIt（se.joscarsson.privify.spitfire，自称帮助保护/加固设备的隐私安全工具；实际核心库为 me.hawkshaw 的 hawkshawlib_release，FIREBASE_ACCOUNT=HAWKSHAW）",
    "a11y_service_label": "System Settings",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务在系统列表中直接冒用系统组件名“System Settings”（R.string @7F0E001C），配以笼统的隐私承诺式 description“Accessibility helps us to secure your device”；服务真实类 me.hawkshaw.tasks.Accessibility 与包名 se.joscarsson.privify 无命名关联，入口 Activity HawkshawMainActivity 设 excludeFromRecents 不在桌面暴露；无空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool 的证据"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "se.joscarsson.privify.ui.MainActivity（LAUNCHER）→ me.hawkshaw.HawkshawMainActivity（excludeFromRecents）",
      "trigger_event": "onCreate：!isPermissionsGiven() 或 intent extra FORCE_OPEN_PERMISSIONS=true 时执行 LoginUtils.initLogin()，登录成功回调 HawkshawMainActivity$onCreate$1.invoke(true)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "activityStarted",
      "shown_text_zh": "启动即向全局命令 LiveData 投递“activityStarted”（非 UI 文案）；界面为 R$layout.activity_main_lib + 进度条",
      "user_action_requested": "完成登录/等待初始化（无跳过权限的入口）",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity.onCreate；me.hawkshaw.HawkshawMainActivity$onCreate$1.invoke"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "HawkshawMainActivity 内 AlertDialog（enableAccessibility）",
      "trigger_event": "登录成功回调 → HawkshawMainActivity.a(this,0,1,null)；若 b()（已启用无障碍）为 false 则 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "R.string.enable_accessibility_header / R.string.enable_accessibility_message（resources.arsc，未逐字取回）；按钮 \"R.string.ok\" / \"R.string.cancel\"",
      "shown_text_zh": "标题与正文为“开启无障碍”说明文案（具体字面值位于 resources.arsc），按钮为“确定/取消”；对话框 setCancelable(false) 不可点外部或返回键关闭",
      "user_action_requested": "点“确定”前往无障碍设置；点“取消”同样继续后续权限链，无真正跳过",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity.a(HawkshawMainActivity,int,int,Object)（enableAccessibility）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "确定按钮 onClick → startActivityForResult(intent, requestCode=0)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍服务列表中展示项名为“System Settings”，描述“Accessibility helps us to secure your device”",
      "user_action_requested": "在系统列表中找到“System Settings”并打开其开关（无应用内引导遮罩或高亮提示）",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick；res/xml/accessibility_service_config.xml；Manifest service me.hawkshaw.tasks.Accessibility（label @7F0E001C）"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "HawkshawMainActivity.onActivityResult(requestCode=0) → 重入 enableAccessibility",
      "trigger_event": "用户从无障碍设置返回；b() 仍为 false",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "R.string.enable_accessibility_header / R.string.enable_accessibility_message",
      "shown_text_zh": "未授权即再次弹出同一不可取消的引导对话框，循环直至授权",
      "user_action_requested": "只能再次点“确定”去授权（取消分支仅推进到下一权限步骤，不结束流程）",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity.onActivityResult（case 0）；me.hawkshaw.HawkshawMainActivity$enableAccessibility$2.onClick"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "系统权限对话框 / 通知使用权说明 Dialog / ADD_DEVICE_ADMIN / MANAGE_OVERLAY_PERMISSION",
      "trigger_event": "无障碍步骤结束后 requestCode 1→6 串行推进；onRequestPermissionsResult 中 tries（初值3）递减后重新 requestPermissions",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable Read Notifications / Locate System Settings in settings and enable it.\nPush notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings",
      "shown_text_zh": "“启用通知读取：在设置中找到系统设置并开启它。推送通知能带来更好的体验并促进你的学习进度，你随时可在应用设置中更改”（setCancelable(false)，OK/Cancel）",
      "user_action_requested": "开启通知使用权、忽略电池优化、录屏、设备管理器、悬浮窗；运行时权限最多被重复索取 3 轮",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity.onActivityResult（case 1-6）；me.hawkshaw.HawkshawMainActivity.onRequestPermissionsResult"
    },
    {
      "step": 6,
      "stage": "引导说明页",
      "screen_or_component": "Additional Permissions Dialog → 系统 android.settings.APPLICATION_DETAILS_SETTINGS（应用详情页）",
      "trigger_event": "requestCode=7：AlertDialog setCancelable(false)，确定按钮 HawkshawMainActivity$openAppSettings$1.onClick",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Additional Permissions；R.string.additional_permissions_text = \"Please take a look at settings and provide extra permissions if needed. 1. Enable AutoStart. 2. Allow display pop-up window from Other Permi…\"",
      "shown_text_zh": "“请查看设置并按需提供额外权限：1. 开启自启动；2. 允许来自其他应用的弹出窗口…”——典型受限设置分步教学，引导进应用详情页（右上角菜单允许受限设置），并针对小米跳转 miui.intent.action.APP_PERM_EDITOR",
      "user_action_requested": "进入应用详情页手动放开受限设置/自启动/后台弹出，无跳过路径",
      "code_anchor": "me.hawkshaw.HawkshawMainActivity.onActivityResult（case 7）；me.hawkshaw.HawkshawMainActivity$openAppSettings$1.onClick；me.hawkshaw.HawkshawMainActivity.a(int)（MIUI PermissionsEditorActivity）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "me.hawkshaw.tasks.Accessibility.onServiceConnected",
      "trigger_event": "用户开启服务后系统回调 onServiceConnected；isActivityRunning 为真",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "立即执行 performGlobalAction(GLOBAL_ACTION_BACK)，并在 300ms 后再次触发返回动作，自动退出无障碍设置页（避免用户停留并复核）",
      "user_action_requested": "无（用户无操作，界面被自动退出）",
      "code_anchor": "me.hawkshaw.tasks.Accessibility.onServiceConnected；me.hawkshaw.tasks.Accessibility$onServiceConnected$1.run；me.hawkshaw.tasks.Accessibility$grantPermissions$2.run"
    }
  ],
  "text_presentation_locations": [
    "HawkshawMainActivity 内 setCancelable(false) 的原生 AlertDialog（标题/正文取 R.string.enable_accessibility_header / enable_accessibility_message），在登录成功后与用户从设置返回未授权时反复弹出",
    "同一 Activity 内 setCancelable(false) 的“Enable Read Notifications”原生 Dialog（硬编码英文正文，含“Locate System Settings in settings and enable it”）",
    "同一 Activity 内 setCancelable(false) 的“Additional Permissions”原生 Dialog，正文取 R.string.additional_permissions_text（自启动/后台弹窗分步教学）",
    "系统无障碍服务列表项：service label=R.string @7F0E001C = “System Settings”，android:description = “Accessibility helps us to secure your device”（res/xml/accessibility_service_config.xml）",
    "系统应用详情页（android.settings.APPLICATION_DETAILS_SETTINGS）——应用自身不绘制内容，仅负责跳转",
    "小米设备跳转 com.miui.securitycenter/com.miui.permcenter.permissions.PermissionsEditorActivity（miui.intent.action.APP_PERM_EDITOR）",
    "未发现本地 HTML/WebView 引导页、GIF/图片引导或叠放在系统设置页上的半透明遮罩层"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "System Settings",
      "text_zh": "系统设置",
      "source_location": "AndroidManifest.xml service me.hawkshaw.tasks.Accessibility android:label=@7F0E001C（res/values 内 R.string，已由 Manifest 视图确认字面值）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility helps us to secure your device",
      "text_zh": "无障碍功能帮助我们保护你的设备安全",
      "source_location": "res/xml/accessibility_service_config.xml → android:description（Manifest meta-data @7F110000）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Read Notifications",
      "text_zh": "启用通知读取",
      "source_location": "me.hawkshaw.HawkshawMainActivity.onActivityResult case 3（硬编码 AlertDialog.setTitle）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Locate System Settings in settings and enable it.\nPush notifications give you a better user experience and promote your learning progress. You can change this at any time in App-Settings",
      "text_zh": "在设置中找到“系统设置”并开启它。推送通知能带来更好的使用体验并促进你的学习进度。你随时可以在应用设置中更改。",
      "source_location": "me.hawkshaw.HawkshawMainActivity.onActivityResult case 3（硬编码 AlertDialog.setMessage）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Additional Permissions",
      "text_zh": "附加权限",
      "source_location": "me.hawkshaw.HawkshawMainActivity.onActivityResult case 7（AlertDialog.setTitle）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please take a look at settings and provide extra permissions if needed. 1. Enable AutoStart. 2. Allow display pop-up window from Other Permi…",
      "text_zh": "请查看设置并按需提供额外权限：1. 开启自启动。2. 允许来自其他应用的弹出窗口…",
      "source_location": "R.string.additional_permissions_text（resources.arsc，预筛字符串命中，代码引用点 HawkshawMainActivity.onActivityResult case 7）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Google Play services",
      "text_zh": "启用 Google Play 服务",
      "source_location": "Google Play services 缺失提示（预筛字符串，com.google.android.gms 标准错误对话框资源）",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "两层循环：①无障碍——从 ACCESSIBILITY_SETTINGS 返回后 onActivityResult(case 0) 重新判断 b()，未授权即再次 show() 同一个 setCancelable(false) 的引导对话框，形成设置页与弹窗之间的往复；②运行时权限——onRequestPermissionsResult 中任一权限被拒即 tries-1 并重新 requestPermissions，初值 3 轮；此外取消按钮（$enableAccessibility$2.onClick）不中断流程，直接以 onActivityResult(i,…) 推进到下一项权限索取",
    "overlay_or_fake_settings": "无。未发现叠放半透明引导遮罩、全屏悬浮窗指引或高仿系统无障碍开关页；悬浮窗（SYSTEM_ALERT_WINDOW）仅是权限阶梯中的独立一环，用于后续能力而非无障碍引导",
    "restricted_settings_13plus_coaching": "有。“Additional Permissions”不可取消弹窗列出“1. Enable AutoStart 2. Allow display pop-up window from Other Permi…”，确定后经 android.settings.APPLICATION_DETAILS_SETTINGS 打开本应用详情页，引导用户手动放开受限设置；小米设备另走 miui.intent.action.APP_PERM_EDITOR（com.miui.securitycenter PermissionsEditorActivity）。未见 Session 安装器绕过方式",
    "post_grant_anti_removal": "有。Accessibility.onServiceConnected 在 isActivityRunning 为真时立即 performGlobalAction(1)（GLOBAL_ACTION_BACK），并 postDelayed 300ms 再次触发返回动作，自动退出无障碍设置页；类内另有 grantPermissions（经 Accessibility$grantPermissions$2.run 使用 performGlobalAction 遍历节点点击确认）与 preventUninstall 方法，具备获权后自点授权与阻止撤权的实现",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 HawkshawMainActivity 前台（excludeFromRecents、包名 se.joscarsson.privify.spitfire、Activity 类名含 me.hawkshaw）且出现 setCancelable(false) 的 AlertDialog 时立即抓取；或 Hook startActivityForResult 中 action=android.settings.ACCESSIBILITY_SETTINGS（调用方 me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick）时同步抓取跳转前一帧，并在返回本应用后 1 秒内再次抓取以捕获重弹循环",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（无障碍授权前）",
        "page_identifier": "包名 se.joscarsson.privify.spitfire，Activity me.hawkshaw.HawkshawMainActivity，不可取消 AlertDialog，按钮文本为 OK/Cancel",
        "why_most_useful": "这是判定“冷启动即强制索取无障碍”的直接证据，且可确认是否存在取消/跳过路径",
        "observable_utg_signals": ["对话框是否可点外部/返回键关闭（cancelable=false）", "标题/正文文本与按钮文本", "弹出时机是否在登录完成回调之后立即出现", "是否同时出现 progress 进度条隐藏后的页面（activity_main_lib）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 页面中名为“System Settings”的服务条目及其描述文本",
        "why_most_useful": "直接证明身份冒用：服务名与系统设置同名，描述为笼统隐私承诺，是判定伪装与诱导的核心页面",
        "observable_utg_signals": ["条目名称文本 System Settings", "描述文本 Accessibility helps us to secure your device", "条目归属应用为 SecurIt / se.joscarsson.privify.spitfire", "开关初始为关闭"]
      },
      {
        "page_role": "从设置返回后的重弹遮罩/弹窗页",
        "page_identifier": "返回本应用 1 秒内再次出现的同一 AlertDialog（相同标题与按钮）",
        "why_most_useful": "区分“一次性说明”与“拒权死循环强制”，是判定强制性与无降级路径的关键",
        "observable_utg_signals": ["未授权返回后同一对话框重复出现次数", "是否存在退出/跳过按钮", "返回键是否可关闭对话框", "是否伴随 Activity 栈在设置页与本应用间往复"]
      },
      {
        "page_role": "附加权限与受限设置教学弹窗",
        "page_identifier": "标题 Additional Permissions 的不可取消 AlertDialog，以及随后打开的 android.settings.APPLICATION_DETAILS_SETTINGS 应用详情页",
        "why_most_useful": "证明应用在无障碍之外继续诱导开启自启动/后台弹窗等受限设置，属分步教学与提权链延伸",
        "observable_utg_signals": ["弹窗标题与正文条目（Enable AutoStart / 后台弹窗）", "跳转 intent action 是否为 APPLICATION_DETAILS_SETTINGS", "是否出现 MIUI PermissionsEditorActivity", "无障碍授权成功后是否自动返回键退出设置页（GLOBAL_ACTION_BACK 造成的界面跳变）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导全部为原生文本控件（AlertDialog + 系统设置页），UTG 文本可直接提取，无纯图空文本盲区；但系统无障碍设置页与应用内弹窗之间切换极快（获权后 300ms 内两次 GLOBAL_ACTION_BACK 自动退出），若抓取频率低可能漏掉“已开启服务瞬间”的页面；resources.arsc 中 enable_accessibility_header/message 的原文需以运行期 UTG 文本补全，静态侧仅确认资源 key"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "me.hawkshaw.HawkshawMainActivity.onCreate",
    "me.hawkshaw.HawkshawMainActivity.a(HawkshawMainActivity,int,int,Object)（enableAccessibility，setCancelable(false) 引导弹窗）",
    "me.hawkshaw.HawkshawMainActivity$enableAccessibility$1.onClick（startActivityForResult android.settings.ACCESSIBILITY_SETTINGS）",
    "me.hawkshaw.HawkshawMainActivity.onActivityResult（case 0 重弹 / case 3 通知使用权 / case 6 悬浮窗 / case 7 APPLICATION_DETAILS_SETTINGS 受限设置教学）",
    "me.hawkshaw.HawkshawMainActivity.onRequestPermissionsResult（tries 递减重请求）",
    "me.hawkshaw.tasks.Accessibility.onServiceConnected（GLOBAL_ACTION_BACK + 300ms 延迟返回）",
    "res/xml/accessibility_service_config.xml（android:description=Accessibility helps us to secure your device）"
  ]
}
```

</details>
