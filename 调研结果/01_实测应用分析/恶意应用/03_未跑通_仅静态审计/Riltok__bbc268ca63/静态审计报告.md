# MR_067__bbc268ca63｜Riltok — Play Market

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：147.7s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即拉起常驻服务并用 1500ms 定时器循环弹不可取消的"Google Play 服务已停止"假故障框，唯一 OK 按钮直跳系统无障碍设置，返回后无限重弹，直到用户开启伪装成 Google Servises 的恶意无障碍服务。
- **静态可见性说明**：无障碍引导链全部静态可见：MainActivity→StDlgSrs→Timer(1500ms)→StartDialog→ACCESSIBILITY_SETTINGS 均在 classes.dex 中完整反编译，文案位于 res/values/strings.xml，无障碍能力声明位于 res/xml/service_conf.xml。未发现加壳、AES 资源或远端 HTML 引导页。仅 AccOnDialog 的启动点（startDialogAccOn）在 Java 层无静态调用者，疑由原生层/反射触发。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `bbc268ca63eeb27e424fec1b3976bab550da304de18e29faff94d9057b1fa25a` |
| 包名 / 年份 | `com.googleplay` / 2019 |
| 家族 / 品类 | **Riltok**（同池样本数：9） |
| 原始来源标识 | https://securelist.com/mobile-banker-riltok/91374/ |
| 桌面显示名 | Play Market |
| 引导页宣称品牌/身份 | Google Play / Google Play Services（Google Servises） |
| 系统无障碍列表服务名 | Google Servises |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务名拼写错误伪装成 Google Services（Google Servises）；android:description 完全留空，系统无障碍列表不显示任何用途说明；android:label 指向 @string/accessibilityservice_label 而非真实功能名；设备管理 receiver 标签为 Play Market Admin；包名 com.googleplay 与主 Activity 隐藏（hideApp+finish）使桌面仅留 Google 品牌图标。 |
| 无障碍服务类名 | `com.googleplay.srs.RtlkAccSrs` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.googleplay.MainActivity（Manifest 唯一 LAUNCHER Activity，主题 Theme.Translucent.NoTitleBar） | onCreate | 原生Activity | 无 | 无（用户仅点击桌面 Play Market 图标，无任何业务界面出现） | `com.googleplay.MainActivity.onCreate` |
| 2 | 业务功能触发 | com.googleplay.srs.StDlgSrs（常驻 Service，stopWithTask=false） | IntTls.startDialogAccessService() 内 startService() 触发 onStartCommand | 不可静态还原 | 无 | 无 | `com.googleplay.srs.StDlgSrs.onStartCommand / StDlgSrs$1.run` |
| 3 | 拒权反馈循环（检测） | com.googleplay.srs.StDlgSrs$StartDialogAccessTimerTask | Timer 每 1500ms 回调 run() | 不可静态还原 | 无 | 无 | `com.googleplay.srs.StDlgSrs$StartDialogAccessTimerTask.run / com.googleplay.checktls.ASTls.isAccessibilitySettingsOn / com.googleplay.checktls.IntTls.startDialogAccess` |
| 4 | 引导说明页 | com.googleplay.ds.StartDialog（Manifest 声明 screenOrientation=portrait，无 export） | onCreate → showDialog() | 原生Dialog | **原文**：Attention / Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: Google Servises / OK<br>**译注**：注意 / 很遗憾，Google Play 服务已停止。为使设备正常工作，请在菜单中选择一行并自行启用：Google Servises / 确定 | 只能点击 OK；setCancelable(false) 且 setCanceledOnTouchOutside(false)，无取消、无跳过、无返回可用按钮 | `com.googleplay.ds.StartDialog.showDialog（R.string.start_dialog_warning / start_dialog_description / accessibilityservice_label）` |
| 5 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | StartDialog$1.onClick（点击唯一 OK 按钮，且 !ASTls.isAccessibilitySettingsOn 成立） | 系统无障碍页 | **原文**：无（系统页，由 ROM 呈现；列表项文案为 Google Servises，无 description）<br>**译注**：系统无障碍服务列表，用户需手动找到拼写错误的 "Google Servises" 并打开开关 | 要求用户手动在系统无障碍列表中找到并开启 Google Servises（本应用未提供任何选择或取消路径） | `com.googleplay.ds.StartDialog$1.onClick（new Intent("android.settings.ACCESSIBILITY_SETTINGS")）` |
| 6 | 拒权反馈循环（重弹） | StartDialog 再次被 Timer 拉起（onPause 仅 destroyDialog） | 用户从系统设置页返回后，下一轮 1500ms Timer 检测仍未开启 → 再次 startActivity(StartDialog) | 原生Dialog | **原文**：Attention / Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: Google Servises / OK<br>**译注**：同一假故障弹窗无限重复，用户无法回到任何正常界面 | 无退出路径；只有开启无障碍服务才能终止循环（无良性降级、无手动替代模式） | `com.googleplay.ds.StartDialog.onPause / StDlgSrs$StartDialogAccessTimerTask.run` |
| 7 | 获权后动作 | com.googleplay.srs.RtlkAccSrs（AccessibilityService） | onServiceConnected | 不可静态还原 | 无 | 无 | `com.googleplay.srs.RtlkAccSrs.onServiceConnected / onBack` |
| 8 | 获权后动作（继续索取设备管理权） | com.googleplay.checkui.AdRequestDialog（android:process=com.playmarket.activities.AdminRequestDialog）与系统设备管理激活页 | handleAccessibilityEvent（TYPE_WINDOW_STATE_CHANGED，eventType==32）且 hasAdmin()==false | 原生Activity | **原文**：Click on Activate button to secure your application.<br>**译注**：点击"激活"按钮以保护您的应用。 | 要求点击系统设备管理页的 Activate（激活）按钮；若出现 action_button，服务自动点击后自我最小化 | `com.googleplay.srs.RtlkAccSrs.adminRequest / handleClick（R.string.admin_title）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动拉起的主界面 Activity：com.googleplay.MainActivity（Theme.Translucent.NoTitleBar，无可见内容，随即 hideApp+finish）
- 不可取消的 AlertDialog：com.googleplay.ds.StartDialog.showDialog()，标题 "Attention"、正文 start_dialog_description + " " + accessibilityservice_label，仅 OK 按钮
- res/values/strings.xml start_dialog_description（第 36-38 行，含换行）："Unfortunately Google Play Services has stopped.\nFor the correct operation of the device select a line in the menu and self-enable:"
- res/values/strings.xml accessibilityservice_label="Google Servises"，经 @string/accessibilityservice_label 呈现在系统无障碍服务列表项名称（description 为空，无用途说明）
- 系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS（由 StartDialog$1.onClick 直接 startActivity 进入，非应用自绘页面）
- 获权后的设备管理激活引导：strings.xml admin_title="Click on Activate button to secure your application."，通过 com.googleplay.checkui.AdRequestDialog 呈现
- 获权成功提示 AccOnDialog：标题 @string/app_name="Play Market"、正文 dlg_acc_on_desc="Google Service was successfully enabled"（Java 层未见调用者，疑原生/反射触发）
- 通知栏渠道名 oreo_channel_name="Google channel"（后台服务常驻通知的伪装名）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Attention | 注意 | `res/values/strings.xml key=start_dialog_warning（StartDialog.showDialog 弹窗标题）` | 故障恐吓 |
| en | Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: | 很遗憾，Google Play 服务已停止。为使设备正常工作，请在菜单中选择一行并自行启用： | `res/values/strings.xml key=start_dialog_description（第 36-38 行，后接 accessibilityservice_label）` | 假更新 |
| en | Google Servises | Google 服务（Google Services 的拼写错误） | `res/values/strings.xml key=accessibilityservice_label（Manifest service android:label，系统无障碍列表显示名）` | 未知 |
| en | OK | 确定 | `com.googleplay.ds.StartDialog.showDialog（setPositiveButton("OK", StartDialog$1)）` | 教唆忽视警告 |
| en | Click on Activate button to secure your application. | 点击"激活"按钮以保护您的应用。 | `res/values/strings.xml key=admin_title（设备管理激活引导，AdRequestDialog）` | 假反诈安全 |
| en | Google Service was successfully enabled | Google 服务已成功启用 | `res/values/strings.xml key=dlg_acc_on_desc（AccOnDialog.showDialog 正文）` | 假更新 |
| en | Enter credit card information to verify your billing data | 请输入信用卡信息以验证您的账单数据 | `res/values/strings.xml key=DescCaption（com.googleplay.injs.s* 仿冒支付/网银页面）` | 假更新 |
| en | Google channel | Google 渠道 | `res/values/strings.xml key=oreo_channel_name（常驻通知渠道名）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：StDlgSrs 常驻（stopWithTask=false）并用 Timer.schedule(task, 0, 1500ms) 每 1.5 秒复检 accessibility_enabled/enabled_accessibility_services；未包含 com.googleplay/com.googleplay.srs.RtlkAccSrs 就以 FLAG_ACTIVITY_NEW_TASK 再拉起 StartDialog，用户按返回或从系统设置页退回后立即重弹，形成无限循环；弹窗本身 setCancelable(false)、setCanceledOnTouchOutside(false)，无取消/跳过按钮。
- **遮罩叠层 / 高仿系统设置页**：无 SYSTEM_ALERT_WINDOW 遮罩引导层，也未自绘高仿系统无障碍开关页；但使用全屏不透明 Activity（StartDialog）伪装为系统级故障提示，并直接跳转真实系统无障碍设置页要求用户自行开启。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：onServiceConnected 立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）退出无障碍设置页；服务配置 flagDefault|flagReportViewIds + 代码设 flags=17、eventTypes=-1 全量监听，具备监听设置页并用全局返回/主页阻止撤权的能力；handleClick 会自动点击 com.android.settings:id/action_button 完成设备管理激活后自我最小化。未见专门针对无障碍开关撤销的循环拦截逻辑。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动后 0-2 秒内监测到 com.googleplay.ds.StartDialog 进入前台，或捕获 startActivity("android.settings.ACCESSIBILITY_SETTINGS") 的 Intent 时立即抓取；同时保持对 com.googleplay.srs.StDlgSrs 启动与 1.5s 周期的连续采样，以记录重弹循环。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：全部引导文案为可提取文本，未使用纯图片或远端 HTML。潜在盲区仅在于 AccOnDialog 的启动点（startDialogAccOn）在 Java 层无静态调用者，若由原生层触发，需结合运行期观测确认其出现时机；此外设备管理激活会自动点击 action_button 后自我最小化，若抓取时机过晚可能错过该页。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动假故障引导弹窗页（第 4 步）** | Activity com.googleplay.ds.StartDialog，标题 "Attention"，正文含 "Unfortunately Google Play Services has stopped"，仅一个 "OK" 按钮，无取消按钮/无返回可关闭 | 这是诱导链唯一面向用户的说明载体，标题+正文+按钮集合即可区分恶意恐吓与良性授权说明 | 弹窗文本 "Attention" 与 "Google Play Services has stopped"；按钮集合仅 OK（无取消/跳过）；返回键与点击外部均无法关闭（不可取消） |
| **系统无障碍服务列表项** | Settings 无障碍页中名称为 "Google Servises"（拼写错误）的服务条目，无 description 子文本 | 直接验证伪装身份与服务标签不一致，且缺失用途说明，是判定欺骗的关键锚点 | 条目名 "Google Servises" 与品牌真实拼写不符；条目下方无任何 description 说明；包名对应 com.googleplay 而非 Google 签名 |
| **拒权返回后的重弹页（第 6 步）** | 从系统无障碍页返回后 1.5s 内再次出现同一 com.googleplay.ds.StartDialog | 证明无降级路径与强制循环，是区分"可跳过的良性引导"与"胁迫式索取"的核心动态证据 | 返回系统设置后短时间内同一弹窗重复出现；重复出现间隔约 1.5 秒且次数持续增加；用户始终无法到达任何应用正常界面 |
| **获权后设备管理激活引导页（第 8 步）** | com.googleplay.checkui.AdRequestDialog（进程名 com.playmarket.activities.AdminRequestDialog）+ 系统设备管理激活页，文案 "Click on Activate button to secure your application." | 说明无障碍只是第一层，获权后立即继续索取设备管理权以防卸载，体现权限递进链条 | 独立进程名的弹窗 Activity 出现；"secure your application" 安全话术；紧接着出现系统设备管理 Activate 按钮页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.googleplay.MainActivity.onCreate`
- `com.googleplay.srs.StDlgSrs$StartDialogAccessTimerTask.run`
- `com.googleplay.ds.StartDialog.showDialog`
- `com.googleplay.ds.StartDialog$1.onClick`
- `com.googleplay.checktls.ASTls.isAccessibilitySettingsOn`
- `com.googleplay.srs.RtlkAccSrs.onServiceConnected`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（运行期 UTG 视角）

**总体判断：** 无障碍权限获取完全由「常驻服务 + 定时器 + 不可取消假故障弹窗」三者构成的运行期循环驱动，而不是由用户主动点击业务功能触发。静态代码 100% 可见，没有加壳、没有远端 HTML、也没有加密载荷。

1. **冷启动 0 步触发**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.googleplay.MainActivity#onCreate>) 调用 `setDefaultSmsCl()` → [IntTls.startCommandService()](<resource-unit:#1.dex1 code:com.googleplay.checktls.IntTls#startCommandService>) → [IntTls.startDialogAccessService()](<resource-unit:#1.dex1 code:com.googleplay.checktls.IntTls#startDialogAccessService>) → `hideApp()` → `finish()`。主界面立即消失，用户看不到任何业务 UI。
2. **定时强制重弹**：[StDlgSrs.onStartCommand()](<resource-unit:#1.dex1 code:com.googleplay.srs.StDlgSrs#onStartCommand>) → [StDlgSrs$1.run()](<resource-unit:#1.dex1 code:com.googleplay.srs.StDlgSrs$1#run>) 起线程，`Timer.schedule(task, 0, 1500)`；[StartDialogAccessTimerTask.run()](<resource-unit:#1.dex1 code:com.googleplay.srs.StDlgSrs$StartDialogAccessTimerTask#run>) 每次都用 [ASTls.isAccessibilitySettingsOn()](<resource-unit:#1.dex1 code:com.googleplay.checktls.ASTls#isAccessibilitySettingsOn>) 检查 `enabled_accessibility_services` 是否包含 `com.googleplay/com.googleplay.srs.RtlkAccSrs`，未包含即 [IntTls.startDialogAccess()](<resource-unit:#1.dex1 code:com.googleplay.checktls.IntTls#startDialogAccess>) 以 `FLAG_ACTIVITY_NEW_TASK` 拉起 StartDialog。该服务在 Manifest 中 `stopWithTask="false"`，因此退出任务也不会停。
3. **弹窗不可取消、无取消按钮**：[StartDialog.showDialog()](<resource-unit:#1.dex1 code:com.googleplay.ds.StartDialog#showDialog>) 设置 `setCancelable(false)`、`setCanceledOnTouchOutside(false)`，只有单个 "OK"。标题 "Attention"，正文为 [start_dialog_description](<resource-unit:#1 file:res/values/strings.xml#L36-L38>)：谎称 Google Play Services 已停止，让用户"在菜单中选一行并自行启用"，并拼接服务名 "Google Servises"。
4. **跳转受限设置**：[StartDialog$1.onClick()](<resource-unit:#1.dex1 code:com.googleplay.ds.StartDialog$1#onClick>) 复检后 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，直接落到系统无障碍列表。用户需自行找到并开启标签为 [Google Servises](<resource-unit:#1 file:res/values/strings.xml#L15>) 的服务；其 `android:description` 为空（[service_conf.xml](<resource-unit:#1 file:res/xml/service_conf.xml#L2-L3>) 仅声明 `typeAllMask`/`canRetrieveWindowContent`），刻意不暴露用途。
5. **拒权反馈循环**：无 `onResume` 校验、也无降级路径；返回后由 1.5s Timer 立刻再弹，形成无限循环，直到授权。`StartDialog.onPause()` 只是 `destroyDialog`。
6. **获权后动作**：[RtlkAccSrs.onServiceConnected()](<resource-unit:#1.dex1 code:com.googleplay.srs.RtlkAccSrs#onServiceConnected>) 立即 `performGlobalAction(1)`（全局返回）退出来路页，并注册 `eventTypes=-1`、`flags=17` 全量监听；随后 [handleAccessibilityEvent()](<resource-unit:#1.dex1 code:com.googleplay.srs.RtlkAccSrs#handleAccessibilityEvent>) 依次推动设备管理授权（[adminRequest](<resource-unit:#1.dex1 code:com.googleplay.srs.RtlkAccSrs#adminRequest>)，`admin_title`="Click on Activate button to secure your application."）与默认短信客户端替换；[handleClick()](<resource-unit:#1.dex1 code:com.googleplay.srs.RtlkAccSrs#handleClick>) 自动点 `com.android.settings:id/action_button` 完成设备管理激活后自我最小化。
7. **身份伪装**：桌面名 "Play Market"、包名 `com.googleplay`、无障碍标签 "Google Servises"（Google Services 的拼写错误），`admin_device_label`="Play Market Admin"；整个授权语境完全是 Google 品牌外壳，而实际业务是 Sberbank 俄语网银仿冒页（`com.googleplay.injs.s*`）。
8. **补充观察**：[AccOnDialog](<resource-unit:#1.dex1 code:com.googleplay.ds.AccOnDialog#showDialog>)（标题 "Play Market"、正文 "Google Service was successfully enabled"、仅 OK 后 `minimizeApp`）存在于 Manifest，但静态未找到 `startDialogAccOn` 的 Java 调用点，可能由原生层或反射触发，属未决项；不影响主链判定。

已登记风险：**R-001**（deceptive_behavior / high）。报告：`report_20261125_040119_883621_24e60857.html`。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链全部静态可见：MainActivity→StDlgSrs→Timer(1500ms)→StartDialog→ACCESSIBILITY_SETTINGS 均在 classes.dex 中完整反编译，文案位于 res/values/strings.xml，无障碍能力声明位于 res/xml/service_conf.xml。未发现加壳、AES 资源或远端 HTML 引导页。仅 AccOnDialog 的启动点（startDialogAccOn）在 Java 层无静态调用者，疑由原生层/反射触发。",
  "summary_one_liner": "冷启动即拉起常驻服务并用 1500ms 定时器循环弹不可取消的\"Google Play 服务已停止\"假故障框，唯一 OK 按钮直跳系统无障碍设置，返回后无限重弹，直到用户开启伪装成 Google Servises 的恶意无障碍服务。",
  "disguise_identity": {
    "app_display_name": "Play Market",
    "claimed_brand_or_persona": "Google Play / Google Play Services（Google Servises）",
    "a11y_service_label": "Google Servises",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务名拼写错误伪装成 Google Services（Google Servises）；android:description 完全留空，系统无障碍列表不显示任何用途说明；android:label 指向 @string/accessibilityservice_label 而非真实功能名；设备管理 receiver 标签为 Play Market Admin；包名 com.googleplay 与主 Activity 隐藏（hideApp+finish）使桌面仅留 Google 品牌图标。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.googleplay.MainActivity（Manifest 唯一 LAUNCHER Activity，主题 Theme.Translucent.NoTitleBar）",
      "trigger_event": "onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无可见界面：setContentView(R.layout.activity_main) 后立即 setDefaultSmsCl()、startCommandService()、startDialogAccessService()、hideApp()、finish()",
      "user_action_requested": "无（用户仅点击桌面 Play Market 图标，无任何业务界面出现）",
      "code_anchor": "com.googleplay.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.googleplay.srs.StDlgSrs（常驻 Service，stopWithTask=false）",
      "trigger_event": "IntTls.startDialogAccessService() 内 startService() 触发 onStartCommand",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；onStartCommand 调用 mainTask 起线程，以 Timer.schedule(task, 0, 1500ms) 周期执行",
      "user_action_requested": "无",
      "code_anchor": "com.googleplay.srs.StDlgSrs.onStartCommand / StDlgSrs$1.run"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环（检测）",
      "screen_or_component": "com.googleplay.srs.StDlgSrs$StartDialogAccessTimerTask",
      "trigger_event": "Timer 每 1500ms 回调 run()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；读取 Settings.Secure.accessibility_enabled 与 enabled_accessibility_services，判断是否包含 com.googleplay/com.googleplay.srs.RtlkAccSrs，未包含则 startDialogAccess() 以 FLAG_ACTIVITY_NEW_TASK 拉起 StartDialog",
      "user_action_requested": "无",
      "code_anchor": "com.googleplay.srs.StDlgSrs$StartDialogAccessTimerTask.run / com.googleplay.checktls.ASTls.isAccessibilitySettingsOn / com.googleplay.checktls.IntTls.startDialogAccess"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "com.googleplay.ds.StartDialog（Manifest 声明 screenOrientation=portrait，无 export）",
      "trigger_event": "onCreate → showDialog()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: Google Servises / OK",
      "shown_text_zh": "注意 / 很遗憾，Google Play 服务已停止。为使设备正常工作，请在菜单中选择一行并自行启用：Google Servises / 确定",
      "user_action_requested": "只能点击 OK；setCancelable(false) 且 setCanceledOnTouchOutside(false)，无取消、无跳过、无返回可用按钮",
      "code_anchor": "com.googleplay.ds.StartDialog.showDialog（R.string.start_dialog_warning / start_dialog_description / accessibilityservice_label）"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "StartDialog$1.onClick（点击唯一 OK 按钮，且 !ASTls.isAccessibilitySettingsOn 成立）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页，由 ROM 呈现；列表项文案为 Google Servises，无 description）",
      "shown_text_zh": "系统无障碍服务列表，用户需手动找到拼写错误的 \"Google Servises\" 并打开开关",
      "user_action_requested": "要求用户手动在系统无障碍列表中找到并开启 Google Servises（本应用未提供任何选择或取消路径）",
      "code_anchor": "com.googleplay.ds.StartDialog$1.onClick（new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")）"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环（重弹）",
      "screen_or_component": "StartDialog 再次被 Timer 拉起（onPause 仅 destroyDialog）",
      "trigger_event": "用户从系统设置页返回后，下一轮 1500ms Timer 检测仍未开启 → 再次 startActivity(StartDialog)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: Google Servises / OK",
      "shown_text_zh": "同一假故障弹窗无限重复，用户无法回到任何正常界面",
      "user_action_requested": "无退出路径；只有开启无障碍服务才能终止循环（无良性降级、无手动替代模式）",
      "code_anchor": "com.googleplay.ds.StartDialog.onPause / StDlgSrs$StartDialogAccessTimerTask.run"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.googleplay.srs.RtlkAccSrs（AccessibilityService）",
      "trigger_event": "onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；立即 performGlobalAction(GLOBAL_ACTION_BACK) 退出设置页，注册 eventTypes=-1、flags=17（含 FLAG_RETRIEVE_INTERACTIVE_WINDOWS）、canRetrieveWindowContent=true 全量监听",
      "user_action_requested": "无",
      "code_anchor": "com.googleplay.srs.RtlkAccSrs.onServiceConnected / onBack"
    },
    {
      "step": 8,
      "stage": "获权后动作（继续索取设备管理权）",
      "screen_or_component": "com.googleplay.checkui.AdRequestDialog（android:process=com.playmarket.activities.AdminRequestDialog）与系统设备管理激活页",
      "trigger_event": "handleAccessibilityEvent（TYPE_WINDOW_STATE_CHANGED，eventType==32）且 hasAdmin()==false",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Click on Activate button to secure your application.",
      "shown_text_zh": "点击\"激活\"按钮以保护您的应用。",
      "user_action_requested": "要求点击系统设备管理页的 Activate（激活）按钮；若出现 action_button，服务自动点击后自我最小化",
      "code_anchor": "com.googleplay.srs.RtlkAccSrs.adminRequest / handleClick（R.string.admin_title）"
    }
  ],
  "text_presentation_locations": [
    "冷启动拉起的主界面 Activity：com.googleplay.MainActivity（Theme.Translucent.NoTitleBar，无可见内容，随即 hideApp+finish）",
    "不可取消的 AlertDialog：com.googleplay.ds.StartDialog.showDialog()，标题 \"Attention\"、正文 start_dialog_description + \" \" + accessibilityservice_label，仅 OK 按钮",
    "res/values/strings.xml start_dialog_description（第 36-38 行，含换行）：\"Unfortunately Google Play Services has stopped.\\nFor the correct operation of the device select a line in the menu and self-enable:\"",
    "res/values/strings.xml accessibilityservice_label=\"Google Servises\"，经 @string/accessibilityservice_label 呈现在系统无障碍服务列表项名称（description 为空，无用途说明）",
    "系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS（由 StartDialog$1.onClick 直接 startActivity 进入，非应用自绘页面）",
    "获权后的设备管理激活引导：strings.xml admin_title=\"Click on Activate button to secure your application.\"，通过 com.googleplay.checkui.AdRequestDialog 呈现",
    "获权成功提示 AccOnDialog：标题 @string/app_name=\"Play Market\"、正文 dlg_acc_on_desc=\"Google Service was successfully enabled\"（Java 层未见调用者，疑原生/反射触发）",
    "通知栏渠道名 oreo_channel_name=\"Google channel\"（后台服务常驻通知的伪装名）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Attention",
      "text_zh": "注意",
      "source_location": "res/values/strings.xml key=start_dialog_warning（StartDialog.showDialog 弹窗标题）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable:",
      "text_zh": "很遗憾，Google Play 服务已停止。为使设备正常工作，请在菜单中选择一行并自行启用：",
      "source_location": "res/values/strings.xml key=start_dialog_description（第 36-38 行，后接 accessibilityservice_label）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Servises",
      "text_zh": "Google 服务（Google Services 的拼写错误）",
      "source_location": "res/values/strings.xml key=accessibilityservice_label（Manifest service android:label，系统无障碍列表显示名）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "OK",
      "text_zh": "确定",
      "source_location": "com.googleplay.ds.StartDialog.showDialog（setPositiveButton(\"OK\", StartDialog$1)）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on Activate button to secure your application.",
      "text_zh": "点击\"激活\"按钮以保护您的应用。",
      "source_location": "res/values/strings.xml key=admin_title（设备管理激活引导，AdRequestDialog）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Service was successfully enabled",
      "text_zh": "Google 服务已成功启用",
      "source_location": "res/values/strings.xml key=dlg_acc_on_desc（AccOnDialog.showDialog 正文）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Enter credit card information to verify your billing data",
      "text_zh": "请输入信用卡信息以验证您的账单数据",
      "source_location": "res/values/strings.xml key=DescCaption（com.googleplay.injs.s* 仿冒支付/网银页面）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Google channel",
      "text_zh": "Google 渠道",
      "source_location": "res/values/strings.xml key=oreo_channel_name（常驻通知渠道名）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "StDlgSrs 常驻（stopWithTask=false）并用 Timer.schedule(task, 0, 1500ms) 每 1.5 秒复检 accessibility_enabled/enabled_accessibility_services；未包含 com.googleplay/com.googleplay.srs.RtlkAccSrs 就以 FLAG_ACTIVITY_NEW_TASK 再拉起 StartDialog，用户按返回或从系统设置页退回后立即重弹，形成无限循环；弹窗本身 setCancelable(false)、setCanceledOnTouchOutside(false)，无取消/跳过按钮。",
    "overlay_or_fake_settings": "无 SYSTEM_ALERT_WINDOW 遮罩引导层，也未自绘高仿系统无障碍开关页；但使用全屏不透明 Activity（StartDialog）伪装为系统级故障提示，并直接跳转真实系统无障碍设置页要求用户自行开启。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "onServiceConnected 立即 performGlobalAction(1)（GLOBAL_ACTION_BACK）退出无障碍设置页；服务配置 flagDefault|flagReportViewIds + 代码设 flags=17、eventTypes=-1 全量监听，具备监听设置页并用全局返回/主页阻止撤权的能力；handleClick 会自动点击 com.android.settings:id/action_button 完成设备管理激活后自我最小化。未见专门针对无障碍开关撤销的循环拦截逻辑。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动后 0-2 秒内监测到 com.googleplay.ds.StartDialog 进入前台，或捕获 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\") 的 Intent 时立即抓取；同时保持对 com.googleplay.srs.StDlgSrs 启动与 1.5s 周期的连续采样，以记录重弹循环。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动假故障引导弹窗页（第 4 步）",
        "page_identifier": "Activity com.googleplay.ds.StartDialog，标题 \"Attention\"，正文含 \"Unfortunately Google Play Services has stopped\"，仅一个 \"OK\" 按钮，无取消按钮/无返回可关闭",
        "why_most_useful": "这是诱导链唯一面向用户的说明载体，标题+正文+按钮集合即可区分恶意恐吓与良性授权说明",
        "observable_utg_signals": ["弹窗文本 \"Attention\" 与 \"Google Play Services has stopped\"", "按钮集合仅 OK（无取消/跳过）", "返回键与点击外部均无法关闭（不可取消）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中名称为 \"Google Servises\"（拼写错误）的服务条目，无 description 子文本",
        "why_most_useful": "直接验证伪装身份与服务标签不一致，且缺失用途说明，是判定欺骗的关键锚点",
        "observable_utg_signals": ["条目名 \"Google Servises\" 与品牌真实拼写不符", "条目下方无任何 description 说明", "包名对应 com.googleplay 而非 Google 签名"]
      },
      {
        "page_role": "拒权返回后的重弹页（第 6 步）",
        "page_identifier": "从系统无障碍页返回后 1.5s 内再次出现同一 com.googleplay.ds.StartDialog",
        "why_most_useful": "证明无降级路径与强制循环，是区分\"可跳过的良性引导\"与\"胁迫式索取\"的核心动态证据",
        "observable_utg_signals": ["返回系统设置后短时间内同一弹窗重复出现", "重复出现间隔约 1.5 秒且次数持续增加", "用户始终无法到达任何应用正常界面"]
      },
      {
        "page_role": "获权后设备管理激活引导页（第 8 步）",
        "page_identifier": "com.googleplay.checkui.AdRequestDialog（进程名 com.playmarket.activities.AdminRequestDialog）+ 系统设备管理激活页，文案 \"Click on Activate button to secure your application.\"",
        "why_most_useful": "说明无障碍只是第一层，获权后立即继续索取设备管理权以防卸载，体现权限递进链条",
        "observable_utg_signals": ["独立进程名的弹窗 Activity 出现", "\"secure your application\" 安全话术", "紧接着出现系统设备管理 Activate 按钮页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：全部引导文案为可提取文本，未使用纯图片或远端 HTML。潜在盲区仅在于 AccOnDialog 的启动点（startDialogAccOn）在 Java 层无静态调用者，若由原生层触发，需结合运行期观测确认其出现时机；此外设备管理激活会自动点击 action_button 后自我最小化，若抓取时机过晚可能错过该页。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.googleplay.MainActivity.onCreate",
    "com.googleplay.srs.StDlgSrs$StartDialogAccessTimerTask.run",
    "com.googleplay.ds.StartDialog.showDialog",
    "com.googleplay.ds.StartDialog$1.onClick",
    "com.googleplay.checktls.ASTls.isAccessibilitySettingsOn",
    "com.googleplay.srs.RtlkAccSrs.onServiceConnected"
  ]
}
```

</details>
