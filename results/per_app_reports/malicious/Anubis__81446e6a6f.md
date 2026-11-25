# MR_109__81446e6a6f｜Anubis — TikTok

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：111.1s

## 1. 一句话核心结论

- **核心申请方式**：以「TikTok」为显示名和第三方无障碍服务名，由后台定时 Service 每 700ms 检查无障碍启用状态并以 NEW_TASK|CLEAR_TASK 反复强拉系统无障碍设置页（最多 25 次），配合不可取消的「系统故障需开启统计权限」弹窗与获权后 Toast 引导，零说明页、零取消入口地骗取无障碍授权。
- **静态可见性说明**：无障碍引导全链路（后台 Service 定时跳转、ActivityAccessibility 直跳系统设置、多语言恐吓弹窗、Toast 引导）均以明文 DEX 代码 + res/xml/serviceconfig.xml 静态可见，无加壳/加密/远端 HTML；仅 socks 模块通过 DexClassLoader 加载私有目录 apk 属二阶段载荷，不参与无障碍引导。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `81446e6a6f4439b9add71c175bc37cec08c3dda2ed14fe7374be865dead270d8` |
| 包名 / 年份 | `anubis.bot.myapplication` / 2019 |
| 家族 / 品类 | **Anubis**（同池样本数：9） |
| 原始来源标识 | https://ti.360.net/blog/articles/anubis-bank-trojan-counterfeiting-international-edition-attack-activity-disclosure/ |
| 桌面显示名 | TikTok |
| 引导页宣称品牌/身份 | TikTok（字节跳动短视频应用），弹窗内以「系统/统计」名义自称，实际为 Anubis 银行木马 |
| 系统无障碍列表服务名 | TikTok |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务无 android:description（系统列表说明区留空，仅显示伪造的 TikTok 名称）；settingsActivity 残留模板包名 com.example.root.myapplication.MainActivity 指向不存在的组件；全部辅助 Activity 的 android:label="" 使其在最近任务/切换器中无名称；应用主题为 Theme.Translucent.NoTitleBar 且 ActivityAccessibility 使用 Theme.NoDisplay，跳转瞬间几乎无可见界面 |
| 无障碍服务类名 | `anubis.bot.myapplication.ServiceAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | anubis.bot.myapplication.Receiver.ReceiverBoot → StartWhileGlobal(IntentService) → StartWhileRequest(IntentService) | BOOT_COMPLETED / QUICKBOOT_POWERON / USER_PRESENT / SCREEN_ON / CONNECTIVITY_CHANGE 等广播，以及 ReceiverAlarm 定时触发 startService(StartWhileRequest) | 不可静态还原（后台 Service，无界面） | 无 | 无（用户无感知） | `anubis.bot.myapplication.Receiver.ReceiverAlarm#a / anubis.bot.myapplication.StartWhileGlobal#onHandleIntent` |
| 2 | 跳无障碍设置 | StartWhileRequest.onHandleIntent → ActivityAccessibility → 系统「设置 > 无障碍」页 | IntentService 循环体内 i.e(context) 返回 false（本包无障碍服务未出现在 getEnabledAccessibilityServiceList 中），且服务端开关 s 为 1/5/6 或预置 startRequest 含 Access=1 | 原生Activity（Theme.NoDisplay，内容布局 2130968576 仅作过渡）+ 系统无障碍页 | **原文**：无（ActivityAccessibility 仅 setContentView(2130968576) 后立即 startActivity("android.settings.ACCESSIBILITY_SETTINGS")）<br>**译注**：无任何说明或解释，直接闪跳到系统无障碍服务列表，用户需自行找到「TikTok」并开启 | 在系统无障碍列表中手动开启名为 TikTok 的服务；页面无取消/跳过按钮，无任何来源说明 | `anubis.bot.myapplication.StartWhileRequest#onHandleIntent / anubis.bot.myapplication.Activity.ActivityAccessibility#onCreate` |
| 3 | 拒权反馈循环 | StartWhileRequest.onHandleIntent 的 while 循环（sleep(700ms) + startActivity NEW_TASK\|CLEAR_TASK，计数器 e ≤ 25） | 用户按返回键回到桌面或停留在设置页未开启服务，循环下一轮再次判定 i.e()==false | 原生Activity（反复重入系统无障碍页） | 无 | 无合法退出路径，只能开启服务或等待循环耗尽 | `anubis.bot.myapplication.StartWhileRequest#onHandleIntent（e<=25 循环与 500/700ms 间隔）` |
| 4 | 引导说明页 | i.f(Context, "statistic") 构建的 AlertDialog（ActivityAlert2 带 extra start=statistic 时进入） | ActivityAlert2.onCreate 收到 Intent extra "start" 含 "statistic"，或服务端指令经 ServiceCommands 拉起 | 原生Dialog（AlertDialog，setCancelable(false)） | **原文**：The system does not work correctly, you need to enable access to the statistics 'TikTok' / Get permission / Enable now（英文环境）；Система не корректно работает, вам необходимо включить доступ к статистике 'TikTok' / Получить разрешение / Включить сейчас（俄语）<br>**译注**：系统运行不正常，你需要开启对统计信息的访问权限「TikTok」/ 获取权限 / 立即启用 | 点击唯一按钮「Enable now」，跳转使用情况访问设置；对话框不可取消、无关闭/跳过按钮（返回键亦被 setCancelable(false) 屏蔽） | `anubis.bot.myapplication.i#f(Context,String) / anubis.bot.myapplication.g#onClick` |
| 5 | 跳受限设置 | g.onClick → 系统「使用情况访问权限」(android.settings.USAGE_ACCESS_SETTINGS) | 用户在步骤 4 对话框点击 negative button（Enable now） | 系统无障碍页（使用情况访问） | **原文**：无（应用侧无附加文案）<br>**译注**：进入系统使用情况访问授权页，用户需为 TikTok 开启 PACKAGE_USAGE_STATS | 在系统页手动授予使用情况访问权限；无跳过入口 | `anubis.bot.myapplication.g#onClick` |
| 6 | 获权后动作 | ServiceToast.onStartCommand（首次拉起时）+ ServiceAccessibility.onServiceConnected | StartWhileRequest 首次 startService(ServiceToast)；无障碍服务被系统绑定回调 onServiceConnected | 通知栏/Toast（Gravity.CENTER 居中 Toast） | **原文**：Enable access for 'TikTok'（Toast，由 StringAccessibility 动态拼接 + 固定 " 'TikTok'"）；onServiceConnected 另读取 StringActivate（默认 activate）、StringPermis（Allow）、StringYes（Yes）<br>**译注**：为「TikTok」启用访问权限 | 无（获权后即静默继续；文案仅为安抚/维持伪装） | `anubis.bot.myapplication.ServiceToast#onStartCommand / anubis.bot.myapplication.ServiceAccessibility#onServiceConnected` |
| 7 | 获权后动作 | ServiceAccessibility.a() → HOME Intent + ActivityAlert2(extra start=blockDelete) → 「Sorry! / System Error 495」对话框 | 无障碍服务检测到卸载/设置页操作（WATCH_SETTINGS / WATCH_PKG_INSTALLER 逻辑）后调用 a() | 原生Dialog（AlertDialog，setCancelable(false)）+ 系统桌面 | **原文**：Sorry! / System Error 495 / ОК<br>**译注**：抱歉！/ 系统错误 495 / 确定 | 仅能点「ОК」；同时先按 HOME 把用户踢出设置页，阻止撤销无障碍授权 | `anubis.bot.myapplication.ServiceAccessibility#a() / anubis.bot.myapplication.Activity.ActivityAlert2#onCreate(blockDelete)` |
| 8 | 跳受限设置 | StartWhileRequest.onHandleIntent → android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS / ActivityAlert2(extra start=deleteApp) → APPLICATION_DETAILS_SETTINGS | PowerManager.isIgnoringBatteryOptimizations 为 false；或服务端下发 deleteApp 指令 | 系统设置页（电池优化 / 应用详情） | 无 | 在系统页允许忽略电池优化 / 在应用详情页操作 | `anubis.bot.myapplication.StartWhileRequest#onHandleIntent / anubis.bot.myapplication.Activity.ActivityAlert2#onCreate(deleteApp)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- i.f(Context,String) 内构建的 AlertDialog（setCancelable(false)）：标题「Get permission」、正文「The system does not work correctly, you need to enable access to the statistics 'TikTok'」、唯一按钮「Enable now」——用于统计/GPS 权限诱导
- Toast（Gravity.CENTER）："Enable access for 'TikTok'"，由 ServiceToast.onStartCommand 读取 SharedPreferences 键 StringAccessibility 后拼接固定字符串 " 'TikTok'"
- SharedPreferences 键 StringActivate / StringPermis / StringYes / uninstall1 / uninstall2 / vkladmin / straccessibility / straccessibility2：由 f 类 100+ 语言的 [lang]前缀数组按系统语言注入，作为后续注入页文案（不含任何无障碍用途说明）
- res/xml/serviceconfig.xml：无 android:description，系统无障碍列表中「TikTok」条目下方说明区为空
- Manifest：application android:label="TikTok"、无障碍 service android:label="TikTok"；ActivityAccessibility 等内容 Activity 的 android:label=""
- ActivityAlert2 的「Sorry!」/「System Error 495」/「ОК」不可取消 AlertDialog：以系统错误话术阻止用户撤销授权或卸载
- ActivityAccessibility 布局 2130968576 存在但不呈现任何说明文字，onCreate 立即跳转系统无障碍页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | The system does not work correctly, you need to enable access to the statistics 'TikTok' | 系统运行不正常，你需要开启对统计信息的访问权限「TikTok」 | `anubis.bot.myapplication.i#f(Context,String) 硬编码字符串（拼接 i.i(context) 取得的应用名 TikTok）` | 故障恐吓 |
| en | Get permission | 获取权限 | `anubis.bot.myapplication.i#f 硬编码 setTitle` | 故障恐吓 |
| en | Enable now | 立即启用 | `anubis.bot.myapplication.i#f 硬编码 setNegativeButton` | 故障恐吓 |
| ru | Система не корректно работает, вам необходимо включить доступ к статистике 'TikTok' | 系统运行不正确，你需要开启对统计信息的访问权限「TikTok」 | `anubis.bot.myapplication.i#f（locale 含 RU 分支）` | 故障恐吓 |
| ru | Получить разрешение | 获取权限 | `anubis.bot.myapplication.i#f（RU 分支标题）` | 故障恐吓 |
| en | For correct operation of the system, you need to get the coordinates, you need to enable geolocation | 为使系统正常运行，需要获取坐标，你需要开启地理定位 | `anubis.bot.myapplication.i#f（gps 分支）` | 故障恐吓 |
| en | Enable access for 'TikTok' | 为「TikTok」启用访问权限 | `anubis.bot.myapplication.ServiceToast#onStartCommand + SharedPreferences 键 StringAccessibility（f.b 数组 [en]Enable access for）` | 教唆忽视警告 |
| en | activate | 激活 | `f.a 数组 [en]activate → SharedPreferences 键 StringActivate（onServiceConnected 读取）` | 未知 |
| en | Allow | 允许 | `f.c 数组 [en]Allow → SharedPreferences 键 StringPermis` | 未知 |
| en | Sorry! | 抱歉！ | `anubis.bot.myapplication.Activity.ActivityAlert2#onCreate（blockDelete 分支 setTitle）` | 故障恐吓 |
| en | System Error 495 | 系统错误 495 | `anubis.bot.myapplication.Activity.ActivityAlert2#onCreate（blockDelete 分支 setMessage）` | 故障恐吓 |
| ru | ОК | 确定 | `anubis.bot.myapplication.Activity.ActivityAlert2#onCreate（setNegativeButton）` | 故障恐吓 |
| en | uninstall ... to remove | 卸载 … 以移除 | `f.e / f.f 数组 [en] → SharedPreferences 键 uninstall1 / uninstall2` | 教唆忽视警告 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：StartWhileRequest.onHandleIntent 在 while 循环内 sleep(700ms) 后调用 i.e() 检查 getEnabledAccessibilityServiceList() 是否包含本包服务；未启用则 startActivity(ActivityAccessibility, FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TASK) 直接覆盖拉起系统无障碍页，计数 e 递增至 25 才退出，用户返回桌面会被立刻再次拉回；配套的 i.f() 弹窗 setCancelable(false)，无取消按钮
- **遮罩叠层 / 高仿系统设置页**：无半透明遮罩/悬浮窗/高仿系统开关页；ActivityAccessibility 使用 Theme.NoDisplay 与空内容布局，以近乎无界面的方式闪跳真实系统无障碍设置页（SYSTEM_ALERT_WINDOW 权限存在但本链路未使用悬浮窗）
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，未实现 13+ 受限设置的应用详情右上角菜单教学，也无 Session 安装器绕过；JUMP_A11Y_SETTINGS 未在引导链中触发）
- **获权后即时行为与防撤权机制**：有。ServiceAccessibility.a() 先发 ACTION_MAIN/HOME 把用户踢出设置页，再以 NEW_TASK 拉起 ActivityAlert2(extra start=blockDelete) 显示不可取消的「Sorry!/System Error 495」对话框；deleteApp 分支跳 APPLICATION_DETAILS_SETTINGS；服务同时监听设置页与安装器事件（WATCH_SETTINGS / WATCH_PKG_INSTALLER），并有 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 保活跳转
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 Activity 启动 intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.USAGE_ACCESS_SETTINGS 的瞬间开始连续截图；更早的触发点是 ActivityAccessibility（Theme.NoDisplay）被拉起的 onCreate，以及 ActivityAlert2 带 extra start=statistic/blockDelete 时弹出的 AlertDialog
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图/空文本诱导；但存在两点盲区：1) 引导入口是后台 IntentService（ReceiverBoot/ReceiverAlarm 广播与定时器），无前台界面，纯 UTG 只能捕获到跳转结果而非触发源；2) 弹窗与 Toast 文案取自 f 类 100+ 语言数组按 Locale 动态注入 SharedPreferences，非英文/俄语等未覆盖语言可能回落 en，需按设备语言核对；3) socks 模块经 DexClassLoader 加载私有目录 apk（apps.com.app.utils），与本无障碍引导链无关，纯 UTG 不可见但不影响本命题判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前恐吓弹窗页（统计权限）** | AlertDialog，标题 Get permission / Получить разрешение，正文含 "does not work correctly" 与 "statistics 'TikTok'"，唯一按钮 Enable now / Включить сейчас | 证明应用以系统故障话术强制引导、且无取消按钮，是区分恶意诱导与良性说明的决定性界面 | 弹窗无取消/关闭控件（仅一个按钮）；文案出现应用自身显示名 TikTok 与 statistics/permission 关键词；点击后前台 Activity 变为 com.android.settings 的使用情况访问页 |
| **系统无障碍服务列表项** | 设置 > 无障碍 列表中出现 label 为「TikTok」、说明区为空的条目；应用详情中服务类为 anubis.bot.myapplication.ServiceAccessibility | 直接对应伪装身份（显示名 = 服务名 = 知名品牌，无任何 description），是无障碍伪装的最强静态+界面双证 | 无障碍条目文本 TikTok 且无副标题/说明文字；系统设置页返回后 500~700ms 内被重新拉起（重入相同页面） |
| **设置页后强拒权循环** | 同一 ACCESSIBILITY_SETTINGS 页面在用户按返回后 0.5~0.7 秒内重复出现，最多约 25 次 | 以 UTG 时间序列直接证明 onHandleIntent 的循环重跳，非用户主动操作 | 页面返回序列出现 ACCESSIBILITY_SETTINGS 的规律性重入；前台 Activity 与 intent action 重复出现，间隔约 500~700ms；重入期间无任何应用自绘界面（Theme.NoDisplay） |
| **获权后抗撤权对话框** | 回到桌面后弹出的不可取消 AlertDialog：Sorry! / System Error 495 / ОК | 证明获权后主动阻止撤销与卸载，属恶意抗清除而非良性降级 | 先出现桌面（HOME）再出现应用对话框；弹窗文本含 System Error 495 等伪造错误码；弹窗无可取消按钮 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `anubis.bot.myapplication.StartWhileRequest#onHandleIntent`
- `anubis.bot.myapplication.Activity.ActivityAccessibility#onCreate`
- `anubis.bot.myapplication.i#f`
- `anubis.bot.myapplication.g#onClick`
- `anubis.bot.myapplication.ServiceToast#onStartCommand`
- `res/xml/serviceconfig.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **纯运行期链路已完整静态可见**：DEX 中未加壳、未加密，引导文字通过 `f` 类的多语言字符串数组，按系统语言写入 SharedPreferences 的 `StringActivate`/`StringAccessibility`/`StringPermis`/`StringYes`，没有远端 HTML，也没有 WebView 教学页。
- **跳转入口非常直接**：后台 Service 定时器循环里启动 [ActivityAccessibility](<resource-unit:#1.dex1 code:anubis.bot.myapplication.Activity.ActivityAccessibility#onCreate>)，它在 `onCreate` 中立刻调用 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`；该 Activity 的布局只是一个过渡页面，没有任何说明文字。
- **强拒权循环**：[StartWhileRequest.onHandleIntent](<resource-unit:#1.dex1 code:anubis.bot.myapplication.StartWhileRequest#onHandleIntent>) 每轮 `sleep(700ms)`，用 `i.e()` 检查 `getEnabledAccessibilityServiceList()` 中是否已包含本包服务；未启用就以 `NEW_TASK|CLEAR_TASK` 再次跳转，计数器 `e` 递增到 25 后才停止，因此用户返回后会被反复拉回设置页。
- **伪装身份**：`android:label="TikTok"`、无障碍服务 `android:label="TikTok"`，而 `res/xml/serviceconfig.xml` 没有任何 `android:description`，所以系统无障碍列表里只显示「TikTok」和一个空白说明；`settingsActivity` 还残留了原模板包名 `com.example.root.myapplication.MainActivity`。
- **配套恐吓文案**：[i.f()](<resource-unit:#1.dex1 code:anubis.bot.myapplication.i#f>) 弹出**不可取消**的 AlertDialog，英文原文为 “The system does not work correctly, you need to enable access to the statistics 'TikTok'”，按钮为 “Enable now”；点击后经 [g.onClick](<resource-unit:#1.dex1 code:anubis.bot.myapplication.g#onClick>) 跳到 `USAGE_ACCESS_SETTINGS`（使用情况访问），与无障碍设置形成“双权限”连续引导。
- **获权后**：[ServiceToast.onStartCommand](<resource-unit:#1.dex1 code:anubis.bot.myapplication.ServiceToast#onStartCommand>) 以居中 Toast 显示 “Enable access for 'TikTok'”，继续维持伪装；同时 `ServiceAccessibility.a()` 先按 HOME 键，再拉起不可取消的「Sorry! / System Error 495」对话框（`ActivityAlert2` 的 `blockDelete`），`deleteApp` 分支跳 `APPLICATION_DETAILS_SETTINGS`，属于防卸载动作。
- 未发现 13+ 受限设置（`JUMP_A11Y_SETTINGS` 未触发受限开关教学分支）或高仿系统开关页遮罩；`DexClassLoader` 二阶段（`apps.com.app.utils` 的 socks 模块）与本无障碍引导链无关。

---

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（后台 Service 定时跳转、ActivityAccessibility 直跳系统设置、多语言恐吓弹窗、Toast 引导）均以明文 DEX 代码 + res/xml/serviceconfig.xml 静态可见，无加壳/加密/远端 HTML；仅 socks 模块通过 DexClassLoader 加载私有目录 apk 属二阶段载荷，不参与无障碍引导。",
  "summary_one_liner": "以「TikTok」为显示名和第三方无障碍服务名，由后台定时 Service 每 700ms 检查无障碍启用状态并以 NEW_TASK|CLEAR_TASK 反复强拉系统无障碍设置页（最多 25 次），配合不可取消的「系统故障需开启统计权限」弹窗与获权后 Toast 引导，零说明页、零取消入口地骗取无障碍授权。",
  "disguise_identity": {
    "app_display_name": "TikTok",
    "claimed_brand_or_persona": "TikTok（字节跳动短视频应用），弹窗内以「系统/统计」名义自称，实际为 Anubis 银行木马",
    "a11y_service_label": "TikTok",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务无 android:description（系统列表说明区留空，仅显示伪造的 TikTok 名称）；settingsActivity 残留模板包名 com.example.root.myapplication.MainActivity 指向不存在的组件；全部辅助 Activity 的 android:label=\"\" 使其在最近任务/切换器中无名称；应用主题为 Theme.Translucent.NoTitleBar 且 ActivityAccessibility 使用 Theme.NoDisplay，跳转瞬间几乎无可见界面"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "anubis.bot.myapplication.Receiver.ReceiverBoot → StartWhileGlobal(IntentService) → StartWhileRequest(IntentService)",
      "trigger_event": "BOOT_COMPLETED / QUICKBOOT_POWERON / USER_PRESENT / SCREEN_ON / CONNECTIVITY_CHANGE 等广播，以及 ReceiverAlarm 定时触发 startService(StartWhileRequest)",
      "ui_carrier": "不可静态还原（后台 Service，无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台静默启动权限索取循环，无任何界面提示",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "anubis.bot.myapplication.Receiver.ReceiverAlarm#a / anubis.bot.myapplication.StartWhileGlobal#onHandleIntent"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "StartWhileRequest.onHandleIntent → ActivityAccessibility → 系统「设置 > 无障碍」页",
      "trigger_event": "IntentService 循环体内 i.e(context) 返回 false（本包无障碍服务未出现在 getEnabledAccessibilityServiceList 中），且服务端开关 s 为 1/5/6 或预置 startRequest 含 Access=1",
      "ui_carrier": "原生Activity（Theme.NoDisplay，内容布局 2130968576 仅作过渡）+ 系统无障碍页",
      "shown_text_verbatim": "无（ActivityAccessibility 仅 setContentView(2130968576) 后立即 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\")）",
      "shown_text_zh": "无任何说明或解释，直接闪跳到系统无障碍服务列表，用户需自行找到「TikTok」并开启",
      "user_action_requested": "在系统无障碍列表中手动开启名为 TikTok 的服务；页面无取消/跳过按钮，无任何来源说明",
      "code_anchor": "anubis.bot.myapplication.StartWhileRequest#onHandleIntent / anubis.bot.myapplication.Activity.ActivityAccessibility#onCreate"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "StartWhileRequest.onHandleIntent 的 while 循环（sleep(700ms) + startActivity NEW_TASK|CLEAR_TASK，计数器 e ≤ 25）",
      "trigger_event": "用户按返回键回到桌面或停留在设置页未开启服务，循环下一轮再次判定 i.e()==false",
      "ui_carrier": "原生Activity（反复重入系统无障碍页）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "返回即被再次强制拉起系统无障碍设置页，最多 25 轮，无退出提示",
      "user_action_requested": "无合法退出路径，只能开启服务或等待循环耗尽",
      "code_anchor": "anubis.bot.myapplication.StartWhileRequest#onHandleIntent（e<=25 循环与 500/700ms 间隔）"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "i.f(Context, \"statistic\") 构建的 AlertDialog（ActivityAlert2 带 extra start=statistic 时进入）",
      "trigger_event": "ActivityAlert2.onCreate 收到 Intent extra \"start\" 含 \"statistic\"，或服务端指令经 ServiceCommands 拉起",
      "ui_carrier": "原生Dialog（AlertDialog，setCancelable(false)）",
      "shown_text_verbatim": "The system does not work correctly, you need to enable access to the statistics 'TikTok' / Get permission / Enable now（英文环境）；Система не корректно работает, вам необходимо включить доступ к статистике 'TikTok' / Получить разрешение / Включить сейчас（俄语）",
      "shown_text_zh": "系统运行不正常，你需要开启对统计信息的访问权限「TikTok」/ 获取权限 / 立即启用",
      "user_action_requested": "点击唯一按钮「Enable now」，跳转使用情况访问设置；对话框不可取消、无关闭/跳过按钮（返回键亦被 setCancelable(false) 屏蔽）",
      "code_anchor": "anubis.bot.myapplication.i#f(Context,String) / anubis.bot.myapplication.g#onClick"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "g.onClick → 系统「使用情况访问权限」(android.settings.USAGE_ACCESS_SETTINGS)",
      "trigger_event": "用户在步骤 4 对话框点击 negative button（Enable now）",
      "ui_carrier": "系统无障碍页（使用情况访问）",
      "shown_text_verbatim": "无（应用侧无附加文案）",
      "shown_text_zh": "进入系统使用情况访问授权页，用户需为 TikTok 开启 PACKAGE_USAGE_STATS",
      "user_action_requested": "在系统页手动授予使用情况访问权限；无跳过入口",
      "code_anchor": "anubis.bot.myapplication.g#onClick"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "ServiceToast.onStartCommand（首次拉起时）+ ServiceAccessibility.onServiceConnected",
      "trigger_event": "StartWhileRequest 首次 startService(ServiceToast)；无障碍服务被系统绑定回调 onServiceConnected",
      "ui_carrier": "通知栏/Toast（Gravity.CENTER 居中 Toast）",
      "shown_text_verbatim": "Enable access for 'TikTok'（Toast，由 StringAccessibility 动态拼接 + 固定 \" 'TikTok'\"）；onServiceConnected 另读取 StringActivate（默认 activate）、StringPermis（Allow）、StringYes（Yes）",
      "shown_text_zh": "为「TikTok」启用访问权限",
      "user_action_requested": "无（获权后即静默继续；文案仅为安抚/维持伪装）",
      "code_anchor": "anubis.bot.myapplication.ServiceToast#onStartCommand / anubis.bot.myapplication.ServiceAccessibility#onServiceConnected"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "ServiceAccessibility.a() → HOME Intent + ActivityAlert2(extra start=blockDelete) → 「Sorry! / System Error 495」对话框",
      "trigger_event": "无障碍服务检测到卸载/设置页操作（WATCH_SETTINGS / WATCH_PKG_INSTALLER 逻辑）后调用 a()",
      "ui_carrier": "原生Dialog（AlertDialog，setCancelable(false)）+ 系统桌面",
      "shown_text_verbatim": "Sorry! / System Error 495 / ОК",
      "shown_text_zh": "抱歉！/ 系统错误 495 / 确定",
      "user_action_requested": "仅能点「ОК」；同时先按 HOME 把用户踢出设置页，阻止撤销无障碍授权",
      "code_anchor": "anubis.bot.myapplication.ServiceAccessibility#a() / anubis.bot.myapplication.Activity.ActivityAlert2#onCreate(blockDelete)"
    },
    {
      "step": 8,
      "stage": "跳受限设置",
      "screen_or_component": "StartWhileRequest.onHandleIntent → android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS / ActivityAlert2(extra start=deleteApp) → APPLICATION_DETAILS_SETTINGS",
      "trigger_event": "PowerManager.isIgnoringBatteryOptimizations 为 false；或服务端下发 deleteApp 指令",
      "ui_carrier": "系统设置页（电池优化 / 应用详情）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "引导用户关闭电池优化以保活，并进入应用详情页用于诱导卸载/授权操作",
      "user_action_requested": "在系统页允许忽略电池优化 / 在应用详情页操作",
      "code_anchor": "anubis.bot.myapplication.StartWhileRequest#onHandleIntent / anubis.bot.myapplication.Activity.ActivityAlert2#onCreate(deleteApp)"
    }
  ],
  "text_presentation_locations": [
    "i.f(Context,String) 内构建的 AlertDialog（setCancelable(false)）：标题「Get permission」、正文「The system does not work correctly, you need to enable access to the statistics 'TikTok'」、唯一按钮「Enable now」——用于统计/GPS 权限诱导",
    "Toast（Gravity.CENTER）：\"Enable access for 'TikTok'\"，由 ServiceToast.onStartCommand 读取 SharedPreferences 键 StringAccessibility 后拼接固定字符串 \" 'TikTok'\"",
    "SharedPreferences 键 StringActivate / StringPermis / StringYes / uninstall1 / uninstall2 / vkladmin / straccessibility / straccessibility2：由 f 类 100+ 语言的 [lang]前缀数组按系统语言注入，作为后续注入页文案（不含任何无障碍用途说明）",
    "res/xml/serviceconfig.xml：无 android:description，系统无障碍列表中「TikTok」条目下方说明区为空",
    "Manifest：application android:label=\"TikTok\"、无障碍 service android:label=\"TikTok\"；ActivityAccessibility 等内容 Activity 的 android:label=\"\"",
    "ActivityAlert2 的「Sorry!」/「System Error 495」/「ОК」不可取消 AlertDialog：以系统错误话术阻止用户撤销授权或卸载",
    "ActivityAccessibility 布局 2130968576 存在但不呈现任何说明文字，onCreate 立即跳转系统无障碍页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "The system does not work correctly, you need to enable access to the statistics 'TikTok'",
      "text_zh": "系统运行不正常，你需要开启对统计信息的访问权限「TikTok」",
      "source_location": "anubis.bot.myapplication.i#f(Context,String) 硬编码字符串（拼接 i.i(context) 取得的应用名 TikTok）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Get permission",
      "text_zh": "获取权限",
      "source_location": "anubis.bot.myapplication.i#f 硬编码 setTitle",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable now",
      "text_zh": "立即启用",
      "source_location": "anubis.bot.myapplication.i#f 硬编码 setNegativeButton",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Система не корректно работает, вам необходимо включить доступ к статистике 'TikTok'",
      "text_zh": "系统运行不正确，你需要开启对统计信息的访问权限「TikTok」",
      "source_location": "anubis.bot.myapplication.i#f（locale 含 RU 分支）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Получить разрешение",
      "text_zh": "获取权限",
      "source_location": "anubis.bot.myapplication.i#f（RU 分支标题）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "For correct operation of the system, you need to get the coordinates, you need to enable geolocation",
      "text_zh": "为使系统正常运行，需要获取坐标，你需要开启地理定位",
      "source_location": "anubis.bot.myapplication.i#f（gps 分支）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable access for 'TikTok'",
      "text_zh": "为「TikTok」启用访问权限",
      "source_location": "anubis.bot.myapplication.ServiceToast#onStartCommand + SharedPreferences 键 StringAccessibility（f.b 数组 [en]Enable access for）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "activate",
      "text_zh": "激活",
      "source_location": "f.a 数组 [en]activate → SharedPreferences 键 StringActivate（onServiceConnected 读取）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow",
      "text_zh": "允许",
      "source_location": "f.c 数组 [en]Allow → SharedPreferences 键 StringPermis",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Sorry!",
      "text_zh": "抱歉！",
      "source_location": "anubis.bot.myapplication.Activity.ActivityAlert2#onCreate（blockDelete 分支 setTitle）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "System Error 495",
      "text_zh": "系统错误 495",
      "source_location": "anubis.bot.myapplication.Activity.ActivityAlert2#onCreate（blockDelete 分支 setMessage）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "ОК",
      "text_zh": "确定",
      "source_location": "anubis.bot.myapplication.Activity.ActivityAlert2#onCreate（setNegativeButton）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "uninstall ... to remove",
      "text_zh": "卸载 … 以移除",
      "source_location": "f.e / f.f 数组 [en] → SharedPreferences 键 uninstall1 / uninstall2",
      "rhetorical_frame": "教唆忽视警告"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "StartWhileRequest.onHandleIntent 在 while 循环内 sleep(700ms) 后调用 i.e() 检查 getEnabledAccessibilityServiceList() 是否包含本包服务；未启用则 startActivity(ActivityAccessibility, FLAG_ACTIVITY_NEW_TASK|FLAG_ACTIVITY_CLEAR_TASK) 直接覆盖拉起系统无障碍页，计数 e 递增至 25 才退出，用户返回桌面会被立刻再次拉回；配套的 i.f() 弹窗 setCancelable(false)，无取消按钮",
    "overlay_or_fake_settings": "无半透明遮罩/悬浮窗/高仿系统开关页；ActivityAccessibility 使用 Theme.NoDisplay 与空内容布局，以近乎无界面的方式闪跳真实系统无障碍设置页（SYSTEM_ALERT_WINDOW 权限存在但本链路未使用悬浮窗）",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，未实现 13+ 受限设置的应用详情右上角菜单教学，也无 Session 安装器绕过；JUMP_A11Y_SETTINGS 未在引导链中触发）",
    "post_grant_anti_removal": "有。ServiceAccessibility.a() 先发 ACTION_MAIN/HOME 把用户踢出设置页，再以 NEW_TASK 拉起 ActivityAlert2(extra start=blockDelete) 显示不可取消的「Sorry!/System Error 495」对话框；deleteApp 分支跳 APPLICATION_DETAILS_SETTINGS；服务同时监听设置页与安装器事件（WATCH_SETTINGS / WATCH_PKG_INSTALLER），并有 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 保活跳转",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 Activity 启动 intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.USAGE_ACCESS_SETTINGS 的瞬间开始连续截图；更早的触发点是 ActivityAccessibility（Theme.NoDisplay）被拉起的 onCreate，以及 ActivityAlert2 带 extra start=statistic/blockDelete 时弹出的 AlertDialog",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前恐吓弹窗页（统计权限）",
        "page_identifier": "AlertDialog，标题 Get permission / Получить разрешение，正文含 \"does not work correctly\" 与 \"statistics 'TikTok'\"，唯一按钮 Enable now / Включить сейчас",
        "why_most_useful": "证明应用以系统故障话术强制引导、且无取消按钮，是区分恶意诱导与良性说明的决定性界面",
        "observable_utg_signals": ["弹窗无取消/关闭控件（仅一个按钮）", "文案出现应用自身显示名 TikTok 与 statistics/permission 关键词", "点击后前台 Activity 变为 com.android.settings 的使用情况访问页"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 > 无障碍 列表中出现 label 为「TikTok」、说明区为空的条目；应用详情中服务类为 anubis.bot.myapplication.ServiceAccessibility",
        "why_most_useful": "直接对应伪装身份（显示名 = 服务名 = 知名品牌，无任何 description），是无障碍伪装的最强静态+界面双证",
        "observable_utg_signals": ["无障碍条目文本 TikTok 且无副标题/说明文字", "系统设置页返回后 500~700ms 内被重新拉起（重入相同页面）"]
      },
      {
        "page_role": "设置页后强拒权循环",
        "page_identifier": "同一 ACCESSIBILITY_SETTINGS 页面在用户按返回后 0.5~0.7 秒内重复出现，最多约 25 次",
        "why_most_useful": "以 UTG 时间序列直接证明 onHandleIntent 的循环重跳，非用户主动操作",
        "observable_utg_signals": ["页面返回序列出现 ACCESSIBILITY_SETTINGS 的规律性重入", "前台 Activity 与 intent action 重复出现，间隔约 500~700ms", "重入期间无任何应用自绘界面（Theme.NoDisplay）"]
      },
      {
        "page_role": "获权后抗撤权对话框",
        "page_identifier": "回到桌面后弹出的不可取消 AlertDialog：Sorry! / System Error 495 / ОК",
        "why_most_useful": "证明获权后主动阻止撤销与卸载，属恶意抗清除而非良性降级",
        "observable_utg_signals": ["先出现桌面（HOME）再出现应用对话框", "弹窗文本含 System Error 495 等伪造错误码", "弹窗无可取消按钮"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图/空文本诱导；但存在两点盲区：1) 引导入口是后台 IntentService（ReceiverBoot/ReceiverAlarm 广播与定时器），无前台界面，纯 UTG 只能捕获到跳转结果而非触发源；2) 弹窗与 Toast 文案取自 f 类 100+ 语言数组按 Locale 动态注入 SharedPreferences，非英文/俄语等未覆盖语言可能回落 en，需按设备语言核对；3) socks 模块经 DexClassLoader 加载私有目录 apk（apps.com.app.utils），与本无障碍引导链无关，纯 UTG 不可见但不影响本命题判定。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "anubis.bot.myapplication.StartWhileRequest#onHandleIntent",
    "anubis.bot.myapplication.Activity.ActivityAccessibility#onCreate",
    "anubis.bot.myapplication.i#f",
    "anubis.bot.myapplication.g#onClick",
    "anubis.bot.myapplication.ServiceToast#onStartCommand",
    "res/xml/serviceconfig.xml"
  ]
}
```

> 说明：本次严格遵守 8–14 次工具调用的效率约束，未再做额外深挖（如 `ServiceCommands` 云控指令对 `s` 开关的下发路径、`f` 类剩余语言数组全文）。因此本报告未写入风险记录；如需登记，可在下一轮以本次证据直接补录。

</details>
