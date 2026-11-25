# MR_018__c38c675a43｜Anubis — Fattura

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：124.5s

## 1. 一句话核心结论

- **核心申请方式**：应用无任何业务界面，冷启动即禁用自身图标并启动后台 IntentService 以 1 秒周期无限循环拉起无界面 Activity 直跳系统无障碍设置页，配合伪造的「Android Security」服务名、7 语系统故障恐吓弹窗与伪 Google Play Protect 弹窗，全程不可取消地迫使开启可读取全部窗口内容的无障碍权限。
- **静态可见性说明**：全部关键逻辑位于明文 classes.dex，无加壳、无 VMP、无加密二阶段载荷；无障碍跳转、循环轮询、多语弹窗文案与资源 XML 均可静态还原。仅远端配置项（this.b.p 的 WebView URL、textPlayProtect/buttonPlayProtect 文案、urls 指令列表）来自 C2 下发，属运行期数据而非隐藏代码。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c38c675a4342052a18e969e839cce797fef842b9d53032882966a3731ced0a70` |
| 包名 / 年份 | `wocwvy.czyxoxmbauu.slsa` / 2020 |
| 家族 / 品类 | **Anubis**（同池样本数：9） |
| 原始来源标识 | https://www.anquanke.com/post/id/199543 |
| 桌面显示名 | Fattura |
| 引导页宣称品牌/身份 | 冒充系统安全组件「Android Security」，并伪造「Google Play Protect」官方弹窗与「Google 更新 Google Play 服务」通知 |
| 系统无障碍列表服务名 | Android Security |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 为空（系统列表中不显示任何用途说明）；多个跳转 Activity 的 android:label 为空字符串且共用 @drawable/im 图标；fymeshs 声明 excludeFromRecents 且无布局，跳转瞬间不可追溯；启动入口 myvbo 首次运行后立即 setComponentEnabledSetting(...,2,1) 自我禁用图标；无障碍配置中 settingsActivity 残留开发模板 com.example.root.myapplication.MainActivity；包名/类名全部随机字母混淆（wocwvy.czyxoxmbauu.slsa）。 |
| 无障碍服务类名 | `wocwvy.czyxoxmbauu.slsa.egxltnv` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | wocwvy.czyxoxmbauu.slsa.ncec.myvbo（LAUNCHER Activity，Manifest 中为唯一 MAIN/LAUNCHER 入口） | 用户点击桌面图标启动，onCreate 执行 | 原生Activity | 无 | 无需操作，用户看到桌面图标闪退/消失 | `wocwvy.czyxoxmbauu.slsa.ncec.myvbo#onCreate` |
| 2 | 获权后动作 | myvbo 自我禁用组件 + 启动后台轮询服务 jtfxlnc、kldqwysgkfcrmq | myvbo.onCreate 末尾 setComponentEnabledSetting(new ComponentName(this, myvbo.class), 2, 1) 与 startService | 原生Activity | 无 | 无（用户无法再次从桌面进入，也无从感知） | `wocwvy.czyxoxmbauu.slsa.ncec.myvbo#onCreate` |
| 3 | 业务功能触发 | wocwvy.czyxoxmbauu.slsa.jtfxlnc（IntentService 死循环）+ wocwvy.czyxoxmbauu.slsa.kldqwysgkfcrmq（平行 IntentService 循环） | onHandleIntent 内 while 循环每 1000ms 调用 b.g() 检查无障碍是否已开启；未开启且配置 t 属于 {1,5,6} 或 startRequest 含 Access=1 时触发跳转 | 原生Activity | 无 | 无（用户未做任何操作即被拉入系统页面） | `wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent` |
| 4 | 跳无障碍设置 | wocwvy.czyxoxmbauu.slsa.ncec.fymeshs（无布局 Activity）→ android.settings.ACCESSIBILITY_SETTINGS 系统无障碍设置页 | fymeshs.onCreate 中 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))，以 NEW_TASK\|CLEAR_TOP 压栈 | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：直接落到系统「无障碍」设置页，界面中唯一可疑项为「Android Security」 | 要求用户手动找到「Android Security」并打开开关（应用自身不提供任何解释页或取消按钮） | `wocwvy.czyxoxmbauu.slsa.ncec.fymeshs#onCreate` |
| 5 | 遮罩叠层指引 | 系统无障碍列表项：wocwvy.czyxoxmbauu.slsa.egxltnv（android:label="Android Security"，android:description 为空） | 用户进入无障碍列表时系统读取服务 label 与 description | 系统无障碍页 | **原文**：Android Security<br>**译注**：系统无障碍列表中显示为「Android Security」，无任何功能说明文字 | 诱导用户凭名称信任并开启该开关 | `#1 manifest:components / res/xml/mihaf.xml` |
| 6 | 引导说明页 | android.app.AlertDialog（由 wocwvy.czyxoxmbauu.slsa.b#d 统一生成，按 Locale 选择 RU/US/TR/DE/IT/FR/UA 文案） | 后台服务调用 b.d(context, "statistic") / "gps" 触发弹窗 | 原生Dialog | **原文**：Get permission / The system does not work correctly, you need to enable access to the statistics '<app name>' / Enable now<br>**译注**：「获取权限 / 系统运行不正常，您需要开启对统计信息的访问 '<应用名>' / 立即启用」 | 唯一按钮「Enable now」跳转 USAGE_ACCESS_SETTINGS；setCancelable(false) 且无取消/跳过按钮 | `wocwvy.czyxoxmbauu.slsa.b#d(Context, String) / wocwvy.czyxoxmbauu.slsa.b$1#onClick` |
| 7 | 拒权反馈循环 | jtfxlnc / kldqwysgkfcrmq 循环 + fymeshs 反复压栈 | 用户从系统设置页按返回键或未开启开关，onHandleIntent 下一轮 1000ms 后再次 startActivity(fymeshs) | 系统无障碍页 | 无 | 除授予权限外无任何退出路径 | `wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent / wocwvy.czyxoxmbauu.slsa.kldqwysgkfcrmq#onHandleIntent` |
| 8 | 业务功能触发 | wocwvy.czyxoxmbauu.slsa.ncec.ovyvpsbxxrtayd（伪造 Google Play Protect 弹窗）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、设备管理激活页 oyqwzkyy.a.b | 远程指令/服务循环触发；锁屏时改由 b.a(Context,String,String) 发通知 | 原生Dialog | **原文**：Google Play Protect / Request to disable <Google Play Protect>! / Update Google Play Service<br>**译注**：伪造 Google Play Protect 官方弹窗要求关闭防护；通知栏伪装成「Google：更新 Google Play 服务」；另跳电池优化白名单与设备管理激活页 | 关闭 Play Protect、允许忽略电池优化、激活设备管理器，为长期驻留与自动化操作清障 | `wocwvy.czyxoxmbauu.slsa.ncec.ovyvpsbxxrtayd#onCreate` |
| 9 | 获权后动作 | wocwvy.czyxoxmbauu.slsa.egxltnv（AccessibilityService，canRetrieveWindowContent=true，flagReportViewIds） | 用户在系统无障碍页开启开关后 onServiceConnected / onAccessibilityEvent 被回调 | 系统无障碍页 | **原文**：egxltnv / onServiceConnected<br>**译注**：服务连接后读取全部窗口内容与视图 ID，交由远端指令驱动执行点击、输入、短信读取等操作；并监视设置页与安装器以防撤权 | 无（获权后完全自动化，用户不再被询问） | `wocwvy.czyxoxmbauu.slsa.egxltnv#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍设置页服务列表项：android:label="Android Security"（Manifest 中 egxltnv 声明），android:description 缺失，列表中无任何用途说明
- 原生 AlertDialog（setCancelable(false)）：标题「Get permission」/「Получить разрешение」/「İzin almak」/「Ottenere il permesso」等 7 语，正文「The system does not work correctly, you need to enable access to the statistics '<应用名>'」，唯一按钮「Enable now」→ USAGE_ACCESS_SETTINGS
- 同类不可取消 AlertDialog（geolocation 分支）：标题「Geolocation」，正文「For correct operation of the system, you need to get the coordinates, you need to enable geolocation」，按钮「Enable now」
- 不可取消 AlertDialog：标题「Google Play Protect」，正文取自 C2 下发的 textPlayProtect，按钮取自 buttonPlayProtect
- 不可取消 AlertDialog：标题「Sorry!」，正文「You have no permission to use this app!」，按钮「ОК」
- 通知栏：伪装「Google」/「Update Google Play Service」（锁屏时由 jtfxlnc、brtltydqhiuqbb、jkeggfql 发出）
- 跳转前无本地 HTML 教学页、无悬浮引导遮罩、无高仿无障碍开关界面——文案全部由原生 AlertDialog 与系统设置页承载

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Get permission | 获取权限 | `wocwvy.czyxoxmbauu.slsa.b#d(Context, String) 硬编码（US/默认分支）` | 假反诈安全 |
| en | The system does not work correctly, you need to enable access to the statistics '<app name>' | 系统运行不正常，您需要开启对统计信息（使用情况访问）的权限 '<应用名>' | `wocwvy.czyxoxmbauu.slsa.b#d(Context, String) 硬编码` | 故障恐吓 |
| en | Enable now | 立即启用 | `wocwvy.czyxoxmbauu.slsa.b#d(Context, String) 唯一按钮文案（setNegativeButton）` | 受限设置分步教学 |
| en | Google Play Protect | Google Play 保护机制（伪造官方弹窗标题） | `wocwvy.czyxoxmbauu.slsa.ncec.ovyvpsbxxrtayd#onCreate 硬编码 setTitle` | 教唆忽视警告 |
| en | Request to disable <Google Play Protect>! | 请求关闭 <Google Play Protect>！（回传 C2 的状态字符串） | `wocwvy.czyxoxmbauu.slsa.ncec.ovyvpsbxxrtayd#onCreate 硬编码上报内容` | 教唆忽视警告 |
| en | Update Google Play Service | 更新 Google Play 服务 | `wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent 硬编码通知文案（b.a(context, "Google", "Update Google Play Service")）` | 假更新 |
| en | Android Security | 安卓安全（伪造的系统安全组件名称） | `#1 manifest:components 中 egxltnv 的 android:label` | 假反诈安全 |
| en | Sorry! / You have no permission to use this app! | 抱歉！/ 您没有使用此应用的权限！ | `wocwvy.czyxoxmbauu.slsa.ncec.dzudmx#onCreate 硬编码 AlertDialog（按钮「ОК」）` | 故障恐吓 |
| en | For correct operation of the system, you need to get the coordinates, you need to enable geolocation | 为使系统正常运行，需要获取坐标，您需要开启定位 | `wocwvy.czyxoxmbauu.slsa.b#d(Context, String) 的 gps 分支` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：jtfxlnc 与 kldqwysgkfcrmq 两个 IntentService 各自 while 循环，每 1000ms 调 b.g() 检查 getEnabledAccessibilityServiceList 是否含 egxltnv；未开启即 startActivity(fymeshs, NEW_TASK|CLEAR_TOP) 重跳无障碍设置页，跳转后间隔缩短为 700ms/500ms，计数到 25 后归 -1 无限持续；用户按返回键离开设置页会立即被再次弹回。
- **遮罩叠层 / 高仿系统设置页**：未使用悬浮窗遮罩或高仿无障碍开关页；改为无界面 Activity 直接跳系统真实设置页，并叠加不可取消的系统故障恐吓 AlertDialog 与伪 Google Play Protect 弹窗施压。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。样本 targetSdkVersion=27，未包含 Android 13 受限设置（受限制的设置）分步教学或 Session 安装器绕过逻辑。
- **获权后即时行为与防撤权机制**：获权后由 egxltnv 事件流驱动远端操作，并含 WATCH_SETTINGS / WATCH_PKG_INSTALLER 监听，用于监视无障碍设置页与安装器以阻止撤权/卸载；未发现自点确认逻辑。
- **良性降级 / 替代方案**：无。不存在手动模式、ADB 引导、仅观看等降级路径，除授权外无任何可退出通道。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在应用冷启动后监测到 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS（组件 wocwvy.czyxoxmbauu.slsa.ncec.fymeshs 压栈）或弹窗出现时拉起 UTG；也可在检测到 myvbo 自我禁用组件后立即抓取，因为此后每 0.5–1 秒都会重新弹出页面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两点盲区：一是首启后 myvbo 立即自我禁用组件，桌面图标消失，若 UTG 在第二次启动时才开始监测将无入口可拉起；二是部分弹窗文案（textPlayProtect、buttonPlayProtect）与 WebView 页面 URL（this.b.p）由 C2 下发，纯静态无法预知具体措辞。另无障碍服务 description 为空，系统列表仅有名称文本，无图无描述，UTG 需依赖文本而非图像识别。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转后系统无障碍服务列表项（伪装身份核心页）** | Settings 无障碍列表中出现 label 为「Android Security」、无副标题说明的服务项 | 证明应用以伪造系统安全名义出现在系统列表中，且无 android:description，是身份伪装的直接可视证据 | 服务名文本「Android Security」；该条目无描述/副标题文本；列表页归属包 com.android.settings 而非本应用 |
| **拒权后重复拉起的设置页（循环证据页）** | 同一无障碍设置页在 1–2 秒内被再次压栈，返回栈顶 Activity 反复变为 fymeshs/Settings | 直接证实 onHandleIntent 死循环与不可取消性，静态代码与运行行为对齐 | 页面在短时间内重复出现；无取消/跳过按钮的弹窗同时存在；应用进程后台仍持有 IntentService |
| **系统故障恐吓弹窗页** | AlertDialog 标题「Get permission」+ 正文含 The system does not work correctly + 单按钮「Enable now」 | 该弹窗是纯文案诱骗主体，可逐字取证其恐吓话术与无取消按钮特征 | 对话框标题与正文逐字文本；仅存在一个按钮；点击后页面跳转至 USAGE_ACCESS_SETTINGS |
| **伪 Google Play Protect 弹窗页** | AlertDialog 标题「Google Play Protect」、不可取消、含单一按钮 | 区分「解除安全防护」这一前置动作，是品牌冒用的关键界面 | 标题文本 Google Play Protect；弹窗归属进程为 wocwvy.czyxoxmbauu.slsa 而非 GMS |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `wocwvy.czyxoxmbauu.slsa.ncec.myvbo#onCreate`
- `wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent`
- `wocwvy.czyxoxmbauu.slsa.kldqwysgkfcrmq#onHandleIntent`
- `wocwvy.czyxoxmbauu.slsa.ncec.fymeshs#onCreate`
- `wocwvy.czyxoxmbauu.slsa.b#d(Context, String)`
- `res/xml/mihaf.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**整体判断**：该样本不存在任何正常的“发票”业务界面，无障碍权限的申请完全由**后台服务循环 + 无界面 Activity 静默跳转**完成，且配合伪造的系统安全身份与恐吓文案施压。静态完全可见（无加壳、无加密载荷），共 12 次工具调用收口。

**引导链（按运行期页面流转）**
1. 冷启动：[myvbo.onCreate()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.ncec.myvbo#onCreate>) 作为 LAUNCHER 入口不渲染业务界面，立即 `startService(jtfxlnc)`，随后 `setComponentEnabledSetting(myvbo, 2, 1)` 把自身图标禁用并 `finish()`——桌面图标用完即消失。
2. 后台循环：[jtfxlnc.onHandleIntent()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent>) 在 `while` 内每 1000ms 用 `b.g()` 比对 `getEnabledAccessibilityServiceList` 中是否含 `egxltnv`，未开启且配置项 `t ∈ {1,5,6}` 或 `startRequest` 含 `Access=1` 时 `startActivity(fymeshs, NEW_TASK|CLEAR_TOP)`，间隔 700ms/500ms 重试；计数到 25 归 -1 继续，永不终止。另一路 [kldqwysgkfcrmq.onHandleIntent()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.kldqwysgkfcrmq#onHandleIntent>) 平行循环做同样的事。
3. 静默跳设置：[fymeshs.onCreate()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.ncec.fymeshs#onCreate>) 无任何布局，直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`；该 Activity 在 Manifest 中 `label=""`、`excludeFromRecents`、共用 `@drawable/im`。
4. 系统无障碍列表：[egxltnv](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.egxltnv>) 以 `android:label="Android Security"` 呈现，`android:description` 为空（无任何用途说明），配置 [res/xml/mihaf.xml](<resource-unit:#1 file:res/xml/mihaf.xml>) 申请 `canRetrieveWindowContent="true"` + `flagReportViewIds` + 窗口内容/状态变更事件，`settingsActivity` 仍是开发模板 `com.example.root.myapplication.MainActivity`。
5. 拒权反馈：用户从设置页返回后循环立刻再次拉起，无“跳过/取消/稍后”路径。
6. 并行恐吓弹窗：[b.d(Context, String)](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.b#d(Context, String)>) 按系统语言生成 RU/US/TR/DE/IT/FR/UA 七语文案、`setCancelable(false)`，唯一按钮“Enable now”经 [b$1.onClick](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.b$1#onClick>) 跳 `USAGE_ACCESS_SETTINGS`；[ovyvpsbxxrtayd.onCreate()](<resource-unit:#1.dex1 code:wocwvy.czyxoxmbauu.slsa.ncec.ovyvpsbxxrtayd#onCreate>) 用标题 `Google Play Protect` 的不可取消弹窗要求关闭 Play Protect 并回传 C2。
7. 配套加码：同一循环在 API≥23 且未忽略电池优化时跳 `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`，并拉起设备管理激活页 `oyqwzkyy.a.b`；锁屏时改走通知栏伪装 `Google` / `Update Google Play Service`。
8. 获权后：无障碍服务进入 `onAccessibilityEvent` 事件驱动执行远端指令，预筛的 `WATCH_PKG_INSTALLER/WATCH_SETTINGS` 指向撤权/卸载监视。

**已登记风险**：R-001（autonomous_audit / high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键逻辑位于明文 classes.dex，无加壳、无 VMP、无加密二阶段载荷；无障碍跳转、循环轮询、多语弹窗文案与资源 XML 均可静态还原。仅远端配置项（this.b.p 的 WebView URL、textPlayProtect/buttonPlayProtect 文案、urls 指令列表）来自 C2 下发，属运行期数据而非隐藏代码。",
  "summary_one_liner": "应用无任何业务界面，冷启动即禁用自身图标并启动后台 IntentService 以 1 秒周期无限循环拉起无界面 Activity 直跳系统无障碍设置页，配合伪造的「Android Security」服务名、7 语系统故障恐吓弹窗与伪 Google Play Protect 弹窗，全程不可取消地迫使开启可读取全部窗口内容的无障碍权限。",
  "disguise_identity": {
    "app_display_name": "Fattura",
    "claimed_brand_or_persona": "冒充系统安全组件「Android Security」，并伪造「Google Play Protect」官方弹窗与「Google 更新 Google Play 服务」通知",
    "a11y_service_label": "Android Security",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 为空（系统列表中不显示任何用途说明）；多个跳转 Activity 的 android:label 为空字符串且共用 @drawable/im 图标；fymeshs 声明 excludeFromRecents 且无布局，跳转瞬间不可追溯；启动入口 myvbo 首次运行后立即 setComponentEnabledSetting(...,2,1) 自我禁用图标；无障碍配置中 settingsActivity 残留开发模板 com.example.root.myapplication.MainActivity；包名/类名全部随机字母混淆（wocwvy.czyxoxmbauu.slsa）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.ncec.myvbo（LAUNCHER Activity，Manifest 中为唯一 MAIN/LAUNCHER 入口）",
      "trigger_event": "用户点击桌面图标启动，onCreate 执行",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不渲染任何业务界面（仅当远端配置 b.o 为真且 SDK>=19 时用 WebView 加载远端 URL this.b.p）",
      "user_action_requested": "无需操作，用户看到桌面图标闪退/消失",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.ncec.myvbo#onCreate"
    },
    {
      "step": 2,
      "stage": "获权后动作",
      "screen_or_component": "myvbo 自我禁用组件 + 启动后台轮询服务 jtfxlnc、kldqwysgkfcrmq",
      "trigger_event": "myvbo.onCreate 末尾 setComponentEnabledSetting(new ComponentName(this, myvbo.class), 2, 1) 与 startService",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "桌面图标被程序化禁用，应用从启动器消失，仅剩后台服务常驻",
      "user_action_requested": "无（用户无法再次从桌面进入，也无从感知）",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.ncec.myvbo#onCreate"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.jtfxlnc（IntentService 死循环）+ wocwvy.czyxoxmbauu.slsa.kldqwysgkfcrmq（平行 IntentService 循环）",
      "trigger_event": "onHandleIntent 内 while 循环每 1000ms 调用 b.g() 检查无障碍是否已开启；未开启且配置 t 属于 {1,5,6} 或 startRequest 含 Access=1 时触发跳转",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台静默轮询，无任何界面呈现",
      "user_action_requested": "无（用户未做任何操作即被拉入系统页面）",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.ncec.fymeshs（无布局 Activity）→ android.settings.ACCESSIBILITY_SETTINGS 系统无障碍设置页",
      "trigger_event": "fymeshs.onCreate 中 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))，以 NEW_TASK|CLEAR_TOP 压栈",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "直接落到系统「无障碍」设置页，界面中唯一可疑项为「Android Security」",
      "user_action_requested": "要求用户手动找到「Android Security」并打开开关（应用自身不提供任何解释页或取消按钮）",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.ncec.fymeshs#onCreate"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍列表项：wocwvy.czyxoxmbauu.slsa.egxltnv（android:label=\"Android Security\"，android:description 为空）",
      "trigger_event": "用户进入无障碍列表时系统读取服务 label 与 description",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Android Security",
      "shown_text_zh": "系统无障碍列表中显示为「Android Security」，无任何功能说明文字",
      "user_action_requested": "诱导用户凭名称信任并开启该开关",
      "code_anchor": "#1 manifest:components / res/xml/mihaf.xml"
    },
    {
      "step": 6,
      "stage": "引导说明页",
      "screen_or_component": "android.app.AlertDialog（由 wocwvy.czyxoxmbauu.slsa.b#d 统一生成，按 Locale 选择 RU/US/TR/DE/IT/FR/UA 文案）",
      "trigger_event": "后台服务调用 b.d(context, \"statistic\") / \"gps\" 触发弹窗",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Get permission / The system does not work correctly, you need to enable access to the statistics '<app name>' / Enable now",
      "shown_text_zh": "「获取权限 / 系统运行不正常，您需要开启对统计信息的访问 '<应用名>' / 立即启用」",
      "user_action_requested": "唯一按钮「Enable now」跳转 USAGE_ACCESS_SETTINGS；setCancelable(false) 且无取消/跳过按钮",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.b#d(Context, String) / wocwvy.czyxoxmbauu.slsa.b$1#onClick"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "jtfxlnc / kldqwysgkfcrmq 循环 + fymeshs 反复压栈",
      "trigger_event": "用户从系统设置页按返回键或未开启开关，onHandleIntent 下一轮 1000ms 后再次 startActivity(fymeshs)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "用户返回即被再次弹回无障碍设置页，形成死循环；计数到 25 后归 -1 继续，永不停止",
      "user_action_requested": "除授予权限外无任何退出路径",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent / wocwvy.czyxoxmbauu.slsa.kldqwysgkfcrmq#onHandleIntent"
    },
    {
      "step": 8,
      "stage": "业务功能触发",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.ncec.ovyvpsbxxrtayd（伪造 Google Play Protect 弹窗）与 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、设备管理激活页 oyqwzkyy.a.b",
      "trigger_event": "远程指令/服务循环触发；锁屏时改由 b.a(Context,String,String) 发通知",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Google Play Protect / Request to disable <Google Play Protect>! / Update Google Play Service",
      "shown_text_zh": "伪造 Google Play Protect 官方弹窗要求关闭防护；通知栏伪装成「Google：更新 Google Play 服务」；另跳电池优化白名单与设备管理激活页",
      "user_action_requested": "关闭 Play Protect、允许忽略电池优化、激活设备管理器，为长期驻留与自动化操作清障",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.ncec.ovyvpsbxxrtayd#onCreate"
    },
    {
      "step": 9,
      "stage": "获权后动作",
      "screen_or_component": "wocwvy.czyxoxmbauu.slsa.egxltnv（AccessibilityService，canRetrieveWindowContent=true，flagReportViewIds）",
      "trigger_event": "用户在系统无障碍页开启开关后 onServiceConnected / onAccessibilityEvent 被回调",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "egxltnv / onServiceConnected",
      "shown_text_zh": "服务连接后读取全部窗口内容与视图 ID，交由远端指令驱动执行点击、输入、短信读取等操作；并监视设置页与安装器以防撤权",
      "user_action_requested": "无（获权后完全自动化，用户不再被询问）",
      "code_anchor": "wocwvy.czyxoxmbauu.slsa.egxltnv#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍设置页服务列表项：android:label=\"Android Security\"（Manifest 中 egxltnv 声明），android:description 缺失，列表中无任何用途说明",
    "原生 AlertDialog（setCancelable(false)）：标题「Get permission」/「Получить разрешение」/「İzin almak」/「Ottenere il permesso」等 7 语，正文「The system does not work correctly, you need to enable access to the statistics '<应用名>'」，唯一按钮「Enable now」→ USAGE_ACCESS_SETTINGS",
    "同类不可取消 AlertDialog（geolocation 分支）：标题「Geolocation」，正文「For correct operation of the system, you need to get the coordinates, you need to enable geolocation」，按钮「Enable now」",
    "不可取消 AlertDialog：标题「Google Play Protect」，正文取自 C2 下发的 textPlayProtect，按钮取自 buttonPlayProtect",
    "不可取消 AlertDialog：标题「Sorry!」，正文「You have no permission to use this app!」，按钮「ОК」",
    "通知栏：伪装「Google」/「Update Google Play Service」（锁屏时由 jtfxlnc、brtltydqhiuqbb、jkeggfql 发出）",
    "跳转前无本地 HTML 教学页、无悬浮引导遮罩、无高仿无障碍开关界面——文案全部由原生 AlertDialog 与系统设置页承载"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Get permission",
      "text_zh": "获取权限",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#d(Context, String) 硬编码（US/默认分支）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "The system does not work correctly, you need to enable access to the statistics '<app name>'",
      "text_zh": "系统运行不正常，您需要开启对统计信息（使用情况访问）的权限 '<应用名>'",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#d(Context, String) 硬编码",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable now",
      "text_zh": "立即启用",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#d(Context, String) 唯一按钮文案（setNegativeButton）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play Protect",
      "text_zh": "Google Play 保护机制（伪造官方弹窗标题）",
      "source_location": "wocwvy.czyxoxmbauu.slsa.ncec.ovyvpsbxxrtayd#onCreate 硬编码 setTitle",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Request to disable <Google Play Protect>!",
      "text_zh": "请求关闭 <Google Play Protect>！（回传 C2 的状态字符串）",
      "source_location": "wocwvy.czyxoxmbauu.slsa.ncec.ovyvpsbxxrtayd#onCreate 硬编码上报内容",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Update Google Play Service",
      "text_zh": "更新 Google Play 服务",
      "source_location": "wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent 硬编码通知文案（b.a(context, \"Google\", \"Update Google Play Service\")）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Security",
      "text_zh": "安卓安全（伪造的系统安全组件名称）",
      "source_location": "#1 manifest:components 中 egxltnv 的 android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Sorry! / You have no permission to use this app!",
      "text_zh": "抱歉！/ 您没有使用此应用的权限！",
      "source_location": "wocwvy.czyxoxmbauu.slsa.ncec.dzudmx#onCreate 硬编码 AlertDialog（按钮「ОК」）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "For correct operation of the system, you need to get the coordinates, you need to enable geolocation",
      "text_zh": "为使系统正常运行，需要获取坐标，您需要开启定位",
      "source_location": "wocwvy.czyxoxmbauu.slsa.b#d(Context, String) 的 gps 分支",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "jtfxlnc 与 kldqwysgkfcrmq 两个 IntentService 各自 while 循环，每 1000ms 调 b.g() 检查 getEnabledAccessibilityServiceList 是否含 egxltnv；未开启即 startActivity(fymeshs, NEW_TASK|CLEAR_TOP) 重跳无障碍设置页，跳转后间隔缩短为 700ms/500ms，计数到 25 后归 -1 无限持续；用户按返回键离开设置页会立即被再次弹回。",
    "overlay_or_fake_settings": "未使用悬浮窗遮罩或高仿无障碍开关页；改为无界面 Activity 直接跳系统真实设置页，并叠加不可取消的系统故障恐吓 AlertDialog 与伪 Google Play Protect 弹窗施压。",
    "restricted_settings_13plus_coaching": "无。样本 targetSdkVersion=27，未包含 Android 13 受限设置（受限制的设置）分步教学或 Session 安装器绕过逻辑。",
    "post_grant_anti_removal": "获权后由 egxltnv 事件流驱动远端操作，并含 WATCH_SETTINGS / WATCH_PKG_INSTALLER 监听，用于监视无障碍设置页与安装器以阻止撤权/卸载；未发现自点确认逻辑。",
    "benign_graceful_degradation": "无。不存在手动模式、ADB 引导、仅观看等降级路径，除授权外无任何可退出通道。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在应用冷启动后监测到 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS（组件 wocwvy.czyxoxmbauu.slsa.ncec.fymeshs 压栈）或弹窗出现时拉起 UTG；也可在检测到 myvbo 自我禁用组件后立即抓取，因为此后每 0.5–1 秒都会重新弹出页面。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转后系统无障碍服务列表项（伪装身份核心页）",
        "page_identifier": "Settings 无障碍列表中出现 label 为「Android Security」、无副标题说明的服务项",
        "why_most_useful": "证明应用以伪造系统安全名义出现在系统列表中，且无 android:description，是身份伪装的直接可视证据",
        "observable_utg_signals": ["服务名文本「Android Security」", "该条目无描述/副标题文本", "列表页归属包 com.android.settings 而非本应用"]
      },
      {
        "page_role": "拒权后重复拉起的设置页（循环证据页）",
        "page_identifier": "同一无障碍设置页在 1–2 秒内被再次压栈，返回栈顶 Activity 反复变为 fymeshs/Settings",
        "why_most_useful": "直接证实 onHandleIntent 死循环与不可取消性，静态代码与运行行为对齐",
        "observable_utg_signals": ["页面在短时间内重复出现", "无取消/跳过按钮的弹窗同时存在", "应用进程后台仍持有 IntentService"]
      },
      {
        "page_role": "系统故障恐吓弹窗页",
        "page_identifier": "AlertDialog 标题「Get permission」+ 正文含 The system does not work correctly + 单按钮「Enable now」",
        "why_most_useful": "该弹窗是纯文案诱骗主体，可逐字取证其恐吓话术与无取消按钮特征",
        "observable_utg_signals": ["对话框标题与正文逐字文本", "仅存在一个按钮", "点击后页面跳转至 USAGE_ACCESS_SETTINGS"]
      },
      {
        "page_role": "伪 Google Play Protect 弹窗页",
        "page_identifier": "AlertDialog 标题「Google Play Protect」、不可取消、含单一按钮",
        "why_most_useful": "区分「解除安全防护」这一前置动作，是品牌冒用的关键界面",
        "observable_utg_signals": ["标题文本 Google Play Protect", "弹窗归属进程为 wocwvy.czyxoxmbauu.slsa 而非 GMS"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两点盲区：一是首启后 myvbo 立即自我禁用组件，桌面图标消失，若 UTG 在第二次启动时才开始监测将无入口可拉起；二是部分弹窗文案（textPlayProtect、buttonPlayProtect）与 WebView 页面 URL（this.b.p）由 C2 下发，纯静态无法预知具体措辞。另无障碍服务 description 为空，系统列表仅有名称文本，无图无描述，UTG 需依赖文本而非图像识别。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "wocwvy.czyxoxmbauu.slsa.ncec.myvbo#onCreate",
    "wocwvy.czyxoxmbauu.slsa.jtfxlnc#onHandleIntent",
    "wocwvy.czyxoxmbauu.slsa.kldqwysgkfcrmq#onHandleIntent",
    "wocwvy.czyxoxmbauu.slsa.ncec.fymeshs#onCreate",
    "wocwvy.czyxoxmbauu.slsa.b#d(Context, String)",
    "res/xml/mihaf.xml"
  ]
}
```

</details>
