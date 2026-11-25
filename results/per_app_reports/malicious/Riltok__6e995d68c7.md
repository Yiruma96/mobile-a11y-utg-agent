# MR_107__6e995d68c7｜Riltok — Avito Pay

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：161.4s

## 1. 一句话核心结论

- **核心申请方式**：应用冷启动即自禁用桌面图标并启动后台服务，用 Timer 每隔数秒弹出一个只含 OK 按钮的俄语『系统严重故障』原生弹窗，谎称需手动开启名为『Безопасность системы』的无障碍服务，点 OK 即跳转无障碍设置页，未开启则无限重弹。
- **静态可见性说明**：全部引导链路在 classes.dex 中静态可见（MainActivity→StDlgSrs→Timer→StartDialog→ACTION_ACCESSIBILITY_SETTINGS），文案在 resources.arsc 字符串池，无障碍配置 res/xml/service_conf.xml 已解码确认无 description；JNI 仅返回设置包名/应用包名等判定字符串，未隐藏引导逻辑，未发现 AES/远端 HTML 二阶段载荷。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6e995d68c724f121d43ec2ff59bc4e536192360afa3beaec5646f01094f0b745` |
| 包名 / 年份 | `com.realtalk` / 2019 |
| 家族 / 品类 | **Riltok**（同池样本数：9） |
| 原始来源标识 | https://securelist.com/mobile-banker-riltok/91374/ |
| 桌面显示名 | Avito Pay |
| 引导页宣称品牌/身份 | 系统安全组件『Безопасность системы』（假借 Android 系统故障修复与 Avito/Google Pay 支付外壳） |
| 系统无障碍列表服务名 | Безопасность системы |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签伪装为系统安全组件而应用名为 Avito Pay；android:description 与 service_conf.xml 均无说明文案，系统无障碍列表中无用途披露；MainActivity 在 onCreate 中 setComponentEnabledSetting 禁用自身 LAUNCHER 组件（隐藏桌面入口）；AdRequestDialog 的 android:process 伪造成 com.realtalk.activities.AdminRequestDialog 以掩盖真实组件名 |
| 无障碍服务类名 | `com.realtalk.srs.RtlkAccSrs` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.realtalk.MainActivity（LAUNCHER） | 用户点击桌面图标 → Activity.onCreate | 原生Activity | 无 | 仅一次点击图标，无任何提示 | `com.realtalk.MainActivity.onCreate` |
| 2 | 冷启动入口 | com.realtalk.MainActivity（自禁用） + com.realtalk.srs.StDlgSrs / com.realtalk.srs.CmndSrs 服务 | onCreate 内 jj.a(this)、jj.b(this)、setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 后 finish() | 原生Activity | 无 | 无可操作界面（用户已失去桌面入口） | `com.realtalk.MainActivity.onCreate → com.realtalk.jj#a / com.realtalk.jj#b` |
| 3 | 拒权反馈循环 | com.realtalk.srs.StDlgSrs$1 → StDlgSrs$b（java.util.Timer） | StDlgSrs.onStartCommand → b() 起线程 → new Timer().schedule(task, 0, StDlgSrs.a) 周期回调 | 后台Service+定时器 | 无 | 无（强制重复拉起） | `com.realtalk.srs.StDlgSrs$1.run / com.realtalk.srs.StDlgSrs$b.run / com.realtalk.jg.a` |
| 4 | 引导说明页 | com.realtalk.ds.StartDialog（原生 AlertDialog） | jg.a(context) 返回 false（未开启无障碍）→ startActivity(StartDialog) | 原生Dialog | **原文**：Произошел критический системный сбой! Для продолжения корректной работы устройства необходимо: Самостоятельно выбрать строку в меню и включить: Безопасность системы<br>**译注**：发生严重系统故障！为使设备继续正常工作，需自行在菜单中选择并开启：系统安全 | 只能点击唯一按钮“OK”，无取消/跳过/关闭选项 | `com.realtalk.ds.StartDialog.onCreate（getString 0x7F0C0081 + 0x7F0C003A，按钮 "OK"）` |
| 5 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | StartDialog$1.onClick → jg.a 仍为 false → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) 后 finish() | 系统无障碍页 | 无 | 手动点击服务项并在确认弹窗中允许；此页无本应用提供的任何说明文字 | `com.realtalk.ds.StartDialog$1.onClick` |
| 6 | 拒权反馈循环 | 返回后 StartDialog 再次压栈（Timer 周期） | 用户返回/拒绝 → Timer 下一周期 jg.a 仍为 false → 再次 startActivity(StartDialog) | 原生Dialog | **原文**：Произошел критический системный сбой! Для продолжения корректной работы устройства необходимо: Самостоятельно выбрать строку в меню и включить: Безопасность системы<br>**译注**：同一“系统故障”弹窗无限重弹，无法退出该流程 | 无合法退出路径，只能开启无障碍或强制停止应用 | `com.realtalk.srs.StDlgSrs$b.run + com.realtalk.jg.a` |
| 7 | 获权后动作 | com.realtalk.srs.RtlkAccSrs（无障碍服务） | onServiceConnected → setServiceInfo(flags=19, eventTypes=-1, notificationTimeout=250) | 系统无障碍页 | 无 | 无（自动化代替用户操作） | `com.realtalk.srs.RtlkAccSrs.onServiceConnected` |
| 8 | 获权后动作 | Settings 页面节点自动点击 + 伪造支付/广告 Activity（AdRequestDialog / GActivity / SSplashActivity） | onAccessibilityEvent：命中设置包名时 jl.a(source,"com.android.settings:id/action_button")、jl.b(source, getString(0x7F0C003A)) 自动点击；命中 GPlay/Sber 包名时 startActivity(GActivity/SSplashActivity)；命中应用/管理标签时 jj.d() 回 HOME | 悬浮窗Overlay | **原文**：Click on Activate button to secure your application. / Уважаемый пользователь, после критического сбоя в системе, Необходимо подтвердить платежную информацию<br>**译注**：点击激活按钮以保护您的应用 / 尊敬的用户，系统发生严重故障后需确认支付信息 | 在伪造的 Google Pay/Avito 支付页填写卡号；打开设置或卸载入口时被强制弹回桌面 | `com.realtalk.srs.RtlkAccSrs.onAccessibilityEvent / com.realtalk.jj#c / com.realtalk.jj#d` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- com.realtalk.ds.StartDialog 的 onCreate 中构造的原生 AlertDialog（唯一 OK 按钮，无取消）：正文 = resources.arsc 字符串 0x7F0C0081（『Произошел критический системный сбой!…включить:』）+ 空格 + 0x7F0C003A（无障碍服务标签『Безопасность системы』），标题取自 0x7F0C0082
- 系统无障碍服务列表项文本：AndroidManifest 中 service com.realtalk.srs.RtlkAccSrs 的 android:label="@7F0C003A"（Безопасность системы），且 res/xml/service_conf.xml（0x7F0F0001）只声明 accessibilityEventTypes/FeedbackType/Flags/canRetrieveWindowContent，无 android:description 与 summary
- 跳转后由系统设置页承载，本应用不叠加遮罩或引导浮层，改由无障碍服务在设置页内自动点击 action_button/button1 与按文本匹配的服务项代替用户操作
- 伪造支付页文本位于 com.realtalk.injs.g.GActivity / com.realtalk.injs.s.SSplashActivity 的界面资源（Avito/Google Pay 卡信息与隐私承诺文案）以及 com.realtalk.checkui.AdRequestDialog 弹窗
- 设备管理器请求文案位于 com.realtalk.rcs.AdReceiver（android:description="@7F0C003B"，label 0x7F0C003C）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Произошел критический системный сбой! Для продолжения корректной работы устройства необходимо: Самостоятельно выбрать строку в меню и включить: | 发生严重系统故障！为使设备继续正常工作，需自行在菜单中选择并开启： | `resources.arsc 字符串 0x7F0C0081，由 com.realtalk.ds.StartDialog.onCreate 读取` | 故障恐吓 |
| ru | Безопасность системы | 系统安全 | `resources.arsc 字符串 0x7F0C003A；同时作为 RtlkAccSrs 的 android:label，并被拼接到弹窗正文末尾` | 假反诈安全 |
| en | Click on Activate button to secure your application. | 点击激活按钮以保护您的应用。 | `resources.arsc 字符串池（设备管理器/激活引导文案）` | 假反诈安全 |
| ru | Уважаемый пользователь, после критического сбоя в системе, Необходимо подтвердить платежную информацию | 尊敬的用户，系统发生严重故障后，需确认支付信息 | `resources.arsc 字符串 Alert_Google_Play（伪造 Google Pay 页）` | 假更新 |
| ru | Информация о карте передается в процессинговый центр в зашифрованном виде по защищённому протоколу HTTPS/SSL. Avito не имеет доступа к вводимым данным. | 卡片信息以加密方式通过 HTTPS/SSL 安全协议传输至处理中心。Avito 无法访问您输入的数据。 | `resources.arsc 字符串池（伪造 Avito 支付页隐私说明）` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：MainActivity 启动的 StDlgSrs 用 java.util.Timer 按固定周期（StDlgSrs.a）回调，每次回调先以 jg.a 读取 Settings.Secure 的 accessibility_enabled/enabled_accessibility_services 判定 RtlkAccSrs 是否已启用；未启用即 startActivity(StartDialog)。用户在 StartDialog 点击 OK 进入无障碍设置后若返回而不开启，下一周期立即重弹；StDlgSrs.onDestroy 还会 sendBroadcast("RestartService") 由 com.realtalk.rcs.RestartService 重新拉起服务，且 RestartService 同时监听 BOOT_COMPLETED/USER_PRESENT/PACKAGE_REMOVED 等广播，使循环在重启后继续。
- **遮罩叠层 / 高仿系统设置页**：不使用 SYSTEM_ALERT_WINDOW 遮罩，也未伪造高仿系统无障碍开关页；改为在真实系统设置页内由无障碍服务自动点击 com.android.settings:id/action_button、android:id/button1，并用 jl.b 按『Безопасность системы』文本匹配服务项执行点击，代替用户完成开启动作。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion 19，2019 年样本，未包含 Android 13 受限设置分步教学或 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：有：onAccessibilityEvent 在设置/应用详情相关包内命中应用名或设备管理标签文本时调用 jj.d() 以 ACTION_MAIN+HOME 强制回到桌面；同时在 GPlay 包内拉起 GActivity、Sber 包内拉起 SSplashActivity、并周期性 jj.c() 拉起 AdRequestDialog，通过抢占前台阻断用户查看或卸载；另请求 ACTION_CHANGE_DEFAULT 抢占默认短信应用。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 AccessibilityService/RtlkAccSrs 尚未启用前，Hook Context.startActivity 监测 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（由 com.realtalk.ds.StartDialog$1.onClick 发起）与 Activity 启动目标 com.realtalk.ds.StartDialog；冷启动 com.realtalk.MainActivity 后 0–3 秒内即出现首个弹窗，可作为最早截屏时机。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：全部文案为原生文本与资源字符串，非纯图引导。需注意两点运行期陷阱——桌面图标在首次启动后即被 setComponentEnabledSetting 禁用，UTG 若按包名从桌面启动将失败，应改用 am start / monkey 以组件 com.realtalk.MainActivity 冷启动；另外该 MainActivity 也会被后续启动禁用，必要时先清除组件状态或重装。静态未加壳，不构成 UTG 盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | com.realtalk.ds.StartDialog 呈现的原生 AlertDialog（单按钮 OK，正文含『критический системный сбой』与『Безопасность системы』） | 该弹窗是诱导链路的唯一说明载体，正文把无障碍服务名包装成系统安全项，且无取消按钮，直接证明恐吓式伪装与不可拒绝 | 弹窗正文与按钮文本；按钮数量（仅 OK，无取消/跳过）；弹窗所属 Activity 组件名 com.realtalk.ds.StartDialog |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已安装服务中的『Безопасность системы』条目（com.realtalk.srs.RtlkAccSrs） | 验证服务标签伪装为系统安全且无任何用途描述，与桌面名 Avito Pay 形成身份错配 | 服务条目显示名；是否显示 description/summary（应缺失）；开关初始为关闭 |
| **设置页返回后的重复压栈页** | 从无障碍设置返回后再次出现的同一 StartDialog | 证明拒绝/返回后定时器死循环重弹，是判定强制性的关键运行期证据 | 两次弹窗出现的时间间隔；返回操作后弹窗立即重现；桌面无应用图标（LAUNCHER 已被禁用） |
| **获权后的伪造支付/自动操作页** | com.realtalk.injs.s.SSplashActivity 或 com.realtalk.injs.g.GActivity（Avito/Google Pay 卡信息页）、com.realtalk.checkui.AdRequestDialog | 说明获取无障碍的真实目的（覆盖银行/支付界面、窃取卡数据与短信），支撑恶意性定级 | 目标包名触发后自动跳转的 Activity；页面中的卡号输入控件与隐私承诺文案；设置页被自动点击的控件 id |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.realtalk.MainActivity.onCreate`
- `com.realtalk.jj.a / com.realtalk.jj.b（拉起 StDlgSrs 与 CmndSrs）`
- `com.realtalk.srs.StDlgSrs$1.run / com.realtalk.srs.StDlgSrs$b.run（Timer 周期判定与重弹）`
- `com.realtalk.ds.StartDialog.onCreate / com.realtalk.ds.StartDialog$1.onClick`
- `com.realtalk.srs.RtlkAccSrs.onServiceConnected / onAccessibilityEvent`
- `res/xml/service_conf.xml（0x7F0F0001，无 description）+ resources.arsc 0x7F0C0081 / 0x7F0C003A`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（纯运行期 UTG 视角）

- **冷启动后立即进入阻塞式循环**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.realtalk.MainActivity#onCreate>) 中，应用先执行 `jj.a(this)` 启动 [StDlgSrs](<resource-unit:#1.dex1 code:com.realtalk.srs.StDlgSrs#onStartCommand>)，再执行 `jj.b(this)` 启动 `CmndSrs`，随后调用 `setComponentEnabledSetting(..., 2, 1)` **禁用自身的 LAUNCHER 组件**并 `finish()`；因此，桌面图标消失，用户之后无法从桌面再次进入应用。
- **Timer 周期性检测并重新拉起**：[StDlgSrs$1.run()](<resource-unit:#1.dex1 code:com.realtalk.srs.StDlgSrs$1#run>) 调用 `new Timer().schedule(new StDlgSrs$b(ctx), 0, StDlgSrs.a)`；[StDlgSrs$b.run()](<resource-unit:#1.dex1 code:com.realtalk.srs.StDlgSrs$b#run>) 每次都会先调用 [jg.a()](<resource-unit:#1.dex1 code:com.realtalk.jg#a>) 读取 `Settings.Secure.accessibility_enabled` 和 `enabled_accessibility_services`，校验 `com.realtalk/com.realtalk.srs.RtlkAccSrs`。**如果未开启，就立即 `startActivity(StartDialog)`**，形成不会自行停止的重复拉起（既有风险记录中的周期为 3 秒）。
- **弹窗使用“系统安全”伪装和恐吓文案**：[StartDialog.onCreate()](<resource-unit:#1.dex1 code:com.realtalk.ds.StartDialog#onCreate>) 用原生 AlertDialog 拼接 `getString(0x7F0C0081) + " " + getString(0x7F0C003A)`，也就是“Произошел критический системный сбой!…Самостоятельно выбрать строку в меню и включить: **Безопасность системы**”，其中 `0x7F0C003A` 正是无障碍服务标签；该弹窗**只有一个 `OK` 按钮，没有取消或跳过按钮**。
- **点击 OK 直接跳转到受限设置**：[StartDialog$1.onClick()](<resource-unit:#1.dex1 code:com.realtalk.ds.StartDialog$1#onClick>) 再次确认未授权后，调用 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 并 `finish()`；随后 Timer 仍在运行，因此用户返回后会再次弹出弹窗（拒绝后循环）。
- **获得权限后自动操作设置页**：[RtlkAccSrs.onServiceConnected()](<resource-unit:#1.dex1 code:com.realtalk.srs.RtlkAccSrs#onServiceConnected>) 设置 `flags=19`、`eventTypes=-1`、`notificationTimeout=250`，全量高频抓取事件；[onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.realtalk.srs.RtlkAccSrs#onAccessibilityEvent>) 在 Settings 包内自动点击 `com.android.settings:id/action_button`、`android:id/button1`，并按 `Безопасность системы` 文本执行 `jl.b` 点击；命中应用或设备管理标签文本时调用 `jj.d()`（跳转 HOME，防止卸载），并定期拉起 `jj.c()` 的 `AdRequestDialog`、`GActivity`、`SSplashActivity`（伪造 Google Pay 和 Sber 支付页），还请求 `ACTION_CHANGE_DEFAULT` 抢占默认短信应用。
- **身份错配**：桌面名称为 `Avito Pay`（0x7F0C004C），无障碍服务标签为 `Безопасность системы`，且 `android:description` 缺失；无障碍配置 `service_conf.xml` 也没有 description 和 summary 字段，因此系统列表中用户只看到“系统安全”字样，没有用途说明。
- 静态可见性完整：无加壳，逻辑全在 `classes.dex`，JNI 仅提供包名和时间戳白名单。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导链路在 classes.dex 中静态可见（MainActivity→StDlgSrs→Timer→StartDialog→ACTION_ACCESSIBILITY_SETTINGS），文案在 resources.arsc 字符串池，无障碍配置 res/xml/service_conf.xml 已解码确认无 description；JNI 仅返回设置包名/应用包名等判定字符串，未隐藏引导逻辑，未发现 AES/远端 HTML 二阶段载荷。",
  "summary_one_liner": "应用冷启动即自禁用桌面图标并启动后台服务，用 Timer 每隔数秒弹出一个只含 OK 按钮的俄语『系统严重故障』原生弹窗，谎称需手动开启名为『Безопасность системы』的无障碍服务，点 OK 即跳转无障碍设置页，未开启则无限重弹。",
  "disguise_identity": {
    "app_display_name": "Avito Pay",
    "claimed_brand_or_persona": "系统安全组件『Безопасность системы』（假借 Android 系统故障修复与 Avito/Google Pay 支付外壳）",
    "a11y_service_label": "Безопасность системы",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签伪装为系统安全组件而应用名为 Avito Pay；android:description 与 service_conf.xml 均无说明文案，系统无障碍列表中无用途披露；MainActivity 在 onCreate 中 setComponentEnabledSetting 禁用自身 LAUNCHER 组件（隐藏桌面入口）；AdRequestDialog 的 android:process 伪造成 com.realtalk.activities.AdminRequestDialog 以掩盖真实组件名"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.realtalk.MainActivity（LAUNCHER）",
      "trigger_event": "用户点击桌面图标 → Activity.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见界面：setContentView 后立即启动后台服务并 finish",
      "user_action_requested": "仅一次点击图标，无任何提示",
      "code_anchor": "com.realtalk.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.realtalk.MainActivity（自禁用） + com.realtalk.srs.StDlgSrs / com.realtalk.srs.CmndSrs 服务",
      "trigger_event": "onCreate 内 jj.a(this)、jj.b(this)、setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 后 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "桌面图标被禁用，用户无法再从桌面进入或找到应用；后台服务常驻",
      "user_action_requested": "无可操作界面（用户已失去桌面入口）",
      "code_anchor": "com.realtalk.MainActivity.onCreate → com.realtalk.jj#a / com.realtalk.jj#b"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.realtalk.srs.StDlgSrs$1 → StDlgSrs$b（java.util.Timer）",
      "trigger_event": "StDlgSrs.onStartCommand → b() 起线程 → new Timer().schedule(task, 0, StDlgSrs.a) 周期回调",
      "ui_carrier": "后台Service+定时器",
      "shown_text_verbatim": "无",
      "shown_text_zh": "每到一个周期检查无障碍是否开启，未开启则拉起 StartDialog",
      "user_action_requested": "无（强制重复拉起）",
      "code_anchor": "com.realtalk.srs.StDlgSrs$1.run / com.realtalk.srs.StDlgSrs$b.run / com.realtalk.jg.a"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "com.realtalk.ds.StartDialog（原生 AlertDialog）",
      "trigger_event": "jg.a(context) 返回 false（未开启无障碍）→ startActivity(StartDialog)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Произошел критический системный сбой! Для продолжения корректной работы устройства необходимо: Самостоятельно выбрать строку в меню и включить: Безопасность системы",
      "shown_text_zh": "发生严重系统故障！为使设备继续正常工作，需自行在菜单中选择并开启：系统安全",
      "user_action_requested": "只能点击唯一按钮“OK”，无取消/跳过/关闭选项",
      "code_anchor": "com.realtalk.ds.StartDialog.onCreate（getString 0x7F0C0081 + 0x7F0C003A，按钮 \"OK\"）"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "StartDialog$1.onClick → jg.a 仍为 false → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")) 后 finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "进入系统无障碍列表，需用户手动找到并开启『Безопасность системы』",
      "user_action_requested": "手动点击服务项并在确认弹窗中允许；此页无本应用提供的任何说明文字",
      "code_anchor": "com.realtalk.ds.StartDialog$1.onClick"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回后 StartDialog 再次压栈（Timer 周期）",
      "trigger_event": "用户返回/拒绝 → Timer 下一周期 jg.a 仍为 false → 再次 startActivity(StartDialog)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Произошел критический системный сбой! Для продолжения корректной работы устройства необходимо: Самостоятельно выбрать строку в меню и включить: Безопасность системы",
      "shown_text_zh": "同一“系统故障”弹窗无限重弹，无法退出该流程",
      "user_action_requested": "无合法退出路径，只能开启无障碍或强制停止应用",
      "code_anchor": "com.realtalk.srs.StDlgSrs$b.run + com.realtalk.jg.a"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.realtalk.srs.RtlkAccSrs（无障碍服务）",
      "trigger_event": "onServiceConnected → setServiceInfo(flags=19, eventTypes=-1, notificationTimeout=250)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "以最高频全事件抓取模式接入，随后在设置页自动点按开关/确认按钮",
      "user_action_requested": "无（自动化代替用户操作）",
      "code_anchor": "com.realtalk.srs.RtlkAccSrs.onServiceConnected"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "Settings 页面节点自动点击 + 伪造支付/广告 Activity（AdRequestDialog / GActivity / SSplashActivity）",
      "trigger_event": "onAccessibilityEvent：命中设置包名时 jl.a(source,\"com.android.settings:id/action_button\")、jl.b(source, getString(0x7F0C003A)) 自动点击；命中 GPlay/Sber 包名时 startActivity(GActivity/SSplashActivity)；命中应用/管理标签时 jj.d() 回 HOME",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Click on Activate button to secure your application. / Уважаемый пользователь, после критического сбоя в системе, Необходимо подтвердить платежную информацию",
      "shown_text_zh": "点击激活按钮以保护您的应用 / 尊敬的用户，系统发生严重故障后需确认支付信息",
      "user_action_requested": "在伪造的 Google Pay/Avito 支付页填写卡号；打开设置或卸载入口时被强制弹回桌面",
      "code_anchor": "com.realtalk.srs.RtlkAccSrs.onAccessibilityEvent / com.realtalk.jj#c / com.realtalk.jj#d"
    }
  ],
  "text_presentation_locations": [
    "com.realtalk.ds.StartDialog 的 onCreate 中构造的原生 AlertDialog（唯一 OK 按钮，无取消）：正文 = resources.arsc 字符串 0x7F0C0081（『Произошел критический системный сбой!…включить:』）+ 空格 + 0x7F0C003A（无障碍服务标签『Безопасность системы』），标题取自 0x7F0C0082",
    "系统无障碍服务列表项文本：AndroidManifest 中 service com.realtalk.srs.RtlkAccSrs 的 android:label=\"@7F0C003A\"（Безопасность системы），且 res/xml/service_conf.xml（0x7F0F0001）只声明 accessibilityEventTypes/FeedbackType/Flags/canRetrieveWindowContent，无 android:description 与 summary",
    "跳转后由系统设置页承载，本应用不叠加遮罩或引导浮层，改由无障碍服务在设置页内自动点击 action_button/button1 与按文本匹配的服务项代替用户操作",
    "伪造支付页文本位于 com.realtalk.injs.g.GActivity / com.realtalk.injs.s.SSplashActivity 的界面资源（Avito/Google Pay 卡信息与隐私承诺文案）以及 com.realtalk.checkui.AdRequestDialog 弹窗",
    "设备管理器请求文案位于 com.realtalk.rcs.AdReceiver（android:description=\"@7F0C003B\"，label 0x7F0C003C）"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Произошел критический системный сбой! Для продолжения корректной работы устройства необходимо: Самостоятельно выбрать строку в меню и включить:",
      "text_zh": "发生严重系统故障！为使设备继续正常工作，需自行在菜单中选择并开启：",
      "source_location": "resources.arsc 字符串 0x7F0C0081，由 com.realtalk.ds.StartDialog.onCreate 读取",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "ru",
      "text_verbatim": "Безопасность системы",
      "text_zh": "系统安全",
      "source_location": "resources.arsc 字符串 0x7F0C003A；同时作为 RtlkAccSrs 的 android:label，并被拼接到弹窗正文末尾",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on Activate button to secure your application.",
      "text_zh": "点击激活按钮以保护您的应用。",
      "source_location": "resources.arsc 字符串池（设备管理器/激活引导文案）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "ru",
      "text_verbatim": "Уважаемый пользователь, после критического сбоя в системе, Необходимо подтвердить платежную информацию",
      "text_zh": "尊敬的用户，系统发生严重故障后，需确认支付信息",
      "source_location": "resources.arsc 字符串 Alert_Google_Play（伪造 Google Pay 页）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": "Информация о карте передается в процессинговый центр в зашифрованном виде по защищённому протоколу HTTPS/SSL. Avito не имеет доступа к вводимым данным.",
      "text_zh": "卡片信息以加密方式通过 HTTPS/SSL 安全协议传输至处理中心。Avito 无法访问您输入的数据。",
      "source_location": "resources.arsc 字符串池（伪造 Avito 支付页隐私说明）",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "MainActivity 启动的 StDlgSrs 用 java.util.Timer 按固定周期（StDlgSrs.a）回调，每次回调先以 jg.a 读取 Settings.Secure 的 accessibility_enabled/enabled_accessibility_services 判定 RtlkAccSrs 是否已启用；未启用即 startActivity(StartDialog)。用户在 StartDialog 点击 OK 进入无障碍设置后若返回而不开启，下一周期立即重弹；StDlgSrs.onDestroy 还会 sendBroadcast(\"RestartService\") 由 com.realtalk.rcs.RestartService 重新拉起服务，且 RestartService 同时监听 BOOT_COMPLETED/USER_PRESENT/PACKAGE_REMOVED 等广播，使循环在重启后继续。",
    "overlay_or_fake_settings": "不使用 SYSTEM_ALERT_WINDOW 遮罩，也未伪造高仿系统无障碍开关页；改为在真实系统设置页内由无障碍服务自动点击 com.android.settings:id/action_button、android:id/button1，并用 jl.b 按『Безопасность системы』文本匹配服务项执行点击，代替用户完成开启动作。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion 19，2019 年样本，未包含 Android 13 受限设置分步教学或 Session 安装器绕过）",
    "post_grant_anti_removal": "有：onAccessibilityEvent 在设置/应用详情相关包内命中应用名或设备管理标签文本时调用 jj.d() 以 ACTION_MAIN+HOME 强制回到桌面；同时在 GPlay 包内拉起 GActivity、Sber 包内拉起 SSplashActivity、并周期性 jj.c() 拉起 AdRequestDialog，通过抢占前台阻断用户查看或卸载；另请求 ACTION_CHANGE_DEFAULT 抢占默认短信应用。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 AccessibilityService/RtlkAccSrs 尚未启用前，Hook Context.startActivity 监测 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS（由 com.realtalk.ds.StartDialog$1.onClick 发起）与 Activity 启动目标 com.realtalk.ds.StartDialog；冷启动 com.realtalk.MainActivity 后 0–3 秒内即出现首个弹窗，可作为最早截屏时机。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "com.realtalk.ds.StartDialog 呈现的原生 AlertDialog（单按钮 OK，正文含『критический системный сбой』与『Безопасность системы』）",
        "why_most_useful": "该弹窗是诱导链路的唯一说明载体，正文把无障碍服务名包装成系统安全项，且无取消按钮，直接证明恐吓式伪装与不可拒绝",
        "observable_utg_signals": ["弹窗正文与按钮文本", "按钮数量（仅 OK，无取消/跳过）", "弹窗所属 Activity 组件名 com.realtalk.ds.StartDialog"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已安装服务中的『Безопасность системы』条目（com.realtalk.srs.RtlkAccSrs）",
        "why_most_useful": "验证服务标签伪装为系统安全且无任何用途描述，与桌面名 Avito Pay 形成身份错配",
        "observable_utg_signals": ["服务条目显示名", "是否显示 description/summary（应缺失）", "开关初始为关闭"]
      },
      {
        "page_role": "设置页返回后的重复压栈页",
        "page_identifier": "从无障碍设置返回后再次出现的同一 StartDialog",
        "why_most_useful": "证明拒绝/返回后定时器死循环重弹，是判定强制性的关键运行期证据",
        "observable_utg_signals": ["两次弹窗出现的时间间隔", "返回操作后弹窗立即重现", "桌面无应用图标（LAUNCHER 已被禁用）"]
      },
      {
        "page_role": "获权后的伪造支付/自动操作页",
        "page_identifier": "com.realtalk.injs.s.SSplashActivity 或 com.realtalk.injs.g.GActivity（Avito/Google Pay 卡信息页）、com.realtalk.checkui.AdRequestDialog",
        "why_most_useful": "说明获取无障碍的真实目的（覆盖银行/支付界面、窃取卡数据与短信），支撑恶意性定级",
        "observable_utg_signals": ["目标包名触发后自动跳转的 Activity", "页面中的卡号输入控件与隐私承诺文案", "设置页被自动点击的控件 id"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：全部文案为原生文本与资源字符串，非纯图引导。需注意两点运行期陷阱——桌面图标在首次启动后即被 setComponentEnabledSetting 禁用，UTG 若按包名从桌面启动将失败，应改用 am start / monkey 以组件 com.realtalk.MainActivity 冷启动；另外该 MainActivity 也会被后续启动禁用，必要时先清除组件状态或重装。静态未加壳，不构成 UTG 盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.realtalk.MainActivity.onCreate",
    "com.realtalk.jj.a / com.realtalk.jj.b（拉起 StDlgSrs 与 CmndSrs）",
    "com.realtalk.srs.StDlgSrs$1.run / com.realtalk.srs.StDlgSrs$b.run（Timer 周期判定与重弹）",
    "com.realtalk.ds.StartDialog.onCreate / com.realtalk.ds.StartDialog$1.onClick",
    "com.realtalk.srs.RtlkAccSrs.onServiceConnected / onAccessibilityEvent",
    "res/xml/service_conf.xml（0x7F0F0001，无 description）+ resources.arsc 0x7F0C0081 / 0x7F0C003A"
  ]
}
```

</details>
