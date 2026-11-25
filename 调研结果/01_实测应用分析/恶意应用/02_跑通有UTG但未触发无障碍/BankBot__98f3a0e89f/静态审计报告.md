# MR_032__98f3a0e89f｜BankBot — Willhaben

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：111.6s

## 1. 一句话核心结论

- **核心申请方式**：以 Willhaben 名义安装，用「Google Play Services 已停止」假故障弹窗（不可取消、返回键失效、无跳过）把唯一 OK 按钮直连 android.settings.ACCESSIBILITY_SETTINGS，配合名为 Google Services 的空描述无障碍服务与后台线程周期性重拉，构成无降级路径的强制诱导。
- **静态可见性说明**：引导弹窗文案、按钮回调、ACTION_ACCESSIBILITY_SETTINGS 跳转、无障碍 service_conf 与 strings 均在 DEX/资源中明文完整可见；未使用加壳、AES 或远端 HTML 教学页。libobladaet-jni.so 仅提供 hasEnabledGp/setEnabledGp/getAddDevicePackageFromJNI 等状态与包名读写，不承载引导 UI 逻辑。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `98f3a0e89f6d73ddc51b090d27c221f91875d027e399e7dd90dac3d39a85154b` |
| 包名 / 年份 | `com.resterent` / 2019 |
| 家族 / 品类 | **BankBot**（同池样本数：4） |
| 原始来源标识 | https://ti.360.net/blog/articles/tracking-austrian-fishing-trojans/ |
| 桌面显示名 | Willhaben |
| 引导页宣称品牌/身份 | Google Play Services / Google Services（虚构系统组件故障与修复提示，服务标签另伪装为 Play Market 设备管理员） |
| 系统无障碍列表服务名 | Google Services |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 完全缺失（settings 页不显示任何用途说明）；服务标签与桌面名不一致，冒用 Google 品牌；AdRequestDialog 通过 android:process="com.googleplay.activities.AdminRequestDialog" 伪造进程名；设备管理员 receiver 标签为 Play Market；类名与字符串名大量缩写混淆（GPSzs、AcsOfDialog、GScclaf 等）。 |
| 无障碍服务类名 | `com.resterent.srs.GPSzs` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_SMS, RECEIVE_SMS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 引导说明页 | com.resterent.ds.StartDialog（Activity，portrait，系统设置返回后由后台线程重拉） | onCreate → ScrTls.scrOn → showDialog()；另由 StDlgSrs.mainTask 起的线程经 IntTls.startDialogAccess 以 FLAG_ACTIVITY_NEW_TASK 重复拉起 | 原生Dialog | **原文**：Attention / Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: Google Services / OK<br>**译注**：注意 / 很遗憾 Google Play 服务已停止。为使设备正常运行，请在菜单中选择一行并自行启用：Google Services / 确定 | 仅有一个 OK 按钮；setCancelable(false)、setCanceledOnTouchOutside(false)，onBackPressed 空实现，无取消、无跳过、返回键无效 | `com.resterent.ds.StartDialog#showDialog / #onBackPressed；res/values/strings.xml: start_dialog_warning、start_dialog_description、accessibilityservice_label` |
| 2 | 跳无障碍设置 | android.settings.ACCESSIBILITY_SETTINGS（系统无障碍服务列表页，列表项显示「Google Services」） | StartDialog$1.onClick(DialogInterface, int) 中 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：Google Services<br>**译注**：系统无障碍服务列表中显示为「Google Services」，无任何 android:description 说明文字 | 要求用户在系统列表中手动找到并打开「Google Services」开关 | `com.resterent.ds.StartDialog$1#onClick；res/xml/service_conf.xml；res/values/strings.xml: accessibilityservice_label` |
| 3 | 拒权反馈循环 | com.resterent.srs.StDlgSrs（后台 Service，intent-filter action com.googleplay.srs.StDlgSrs）→ StDlgSrs$1 线程 → 再次拉起 StartDialog | StDlgSrs.onStartCommand → mainTask → new Thread(StDlgSrs$1).start() → IntTls.startDialogAccess（FLAG_ACTIVITY_NEW_TASK） | 原生Activity | **原文**：Attention / Unfortunately Google Play Services has stopped.<br>**译注**：用户从设置页返回或拒绝授权后，后台线程再次以同一假故障弹窗抢占前台 | 再次被迫点击 OK 回到无障碍设置页；无「拒绝并继续使用」路径 | `com.resterent.srs.StDlgSrs#onStartCommand / #mainTask；com.resterent.tls.IntTls#startDialogAccess` |
| 4 | 获权后动作 | com.resterent.srs.GPSzs（AccessibilityService）→ com.resterent.ui.AdRequestDialog（伪装进程 com.googleplay.activities.AdminRequestDialog）→ com.resterent.ds.AcsOfDialog | GPSzs.onServiceConnected（注册 typeAllMask、feedbackAllMask、flagReportViewIds）→ onAccessibilityEvent → handleAccessibilityEvent：!hasAd() 时 adReq() → IntTls.startOdminRequest() | 原生Dialog | **原文**：Willhaben / Google Service was successfully enabled / OK；设备管理员页文案 Click on Activate button to secure your application.<br>**译注**：「Willhaben / Google 服务已成功启用 / 确定」；随后弹出设备管理员激活页，要求点击「激活」以「保护你的应用」 | 点击 OK（AcsOfDialog$1.onClick → IntTls.minimizeApp 将自身最小化）；设备管理员页要求点击 Activate | `com.resterent.srs.GPSzs#onServiceConnected / #handleAccessibilityEvent / #adReq；com.resterent.ds.AcsOfDialog#showDialog；com.resterent.ds.AcsOfDialog$1#onClick；com.resterent.tls.IntTls#startoAdminAction` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- com.resterent.ds.StartDialog：原生 AlertDialog（BaseActivity 子类），标题 Attention，正文为 start_dialog_description + accessibilityservice_label 拼接，单按钮 OK，不可取消、不可点外部关闭、返回键被 onBackPressed 空实现吞掉
- 系统无障碍设置页服务列表项：由 manifest 中 service android:label="@string/accessibilityservice_label" 显示为「Google Services」；android:description 未声明，页面无任何用途说明
- com.resterent.ds.AcsOfDialog：获权后原生 AlertDialog，标题取 @string/app_name（Willhaben），正文 dlg_acc_on_desc = "Google Service was successfully enabled"
- com.resterent.ui.AdRequestDialog：设备管理员申请前置引导弹窗（独立进程 com.googleplay.activities.AdminRequestDialog），激活说明取 @string/admin_title = "Click on Activate button to secure your application."，系统管理员页标签 @string/admin_device_label = "Play Market"
- 未使用 WebView、本地 HTML 或悬浮窗承载引导文案；全部为原生 Dialog + 系统设置页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: | 很遗憾 Google Play 服务已停止。为使设备正常运行，请在菜单中选择一行并自行启用： | `res/values/strings.xml key=start_dialog_description` | 故障恐吓 |
| en | Attention | 注意 | `res/values/strings.xml key=start_dialog_warning` | 故障恐吓 |
| en | Google Services | Google 服务 | `res/values/strings.xml key=accessibilityservice_label（manifest 中无障碍服务 android:label 引用）` | 假反诈安全 |
| en | Google Service was successfully enabled | Google 服务已成功启用 | `res/values/strings.xml key=dlg_acc_on_desc（AcsOfDialog.showDialog 使用）` | 假更新 |
| en | Click on Activate button to secure your application. | 点击「激活」按钮以保护您的应用。 | `res/values/strings.xml key=admin_title（IntTls.startoAdminAction 的 ADD_EXPLANATION）` | 假反诈安全 |
| en | Play Market | Play 商店 | `res/values/strings.xml key=admin_device_label（设备管理员 receiver android:label）` | 未知 |
| en | Willhaben | Willhaben（奥地利二手交易平台品牌） | `res/values/strings.xml key=app_name（application android:label）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：StartDialog 的 onBackPressed 为空实现、setCancelable(false)，用户无法退出；从系统设置页返回后，StDlgSrs 后台线程（mainTask → StDlgSrs$1 → IntTls.startDialogAccess，FLAG_ACTIVITY_NEW_TASK）再次以同一假故障弹窗抢占前台，直到用户打开无障碍开关为止
- **遮罩叠层 / 高仿系统设置页**：未使用半透明遮罩、全屏悬浮窗或高仿系统无障碍开关页；直接跳转真实系统 ACCESSIBILITY_SETTINGS 页，靠服务标签「Google Services」冒充系统组件骗取点击
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=19，未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转或「点右上角菜单允许受限设置」的分步教学
- **获权后即时行为与防撤权机制**：未发现 GLOBAL_ACTION_BACK/HOME 阻止撤权或监听设置页自动确认；获权后转向设备管理员申请（ADD_DEVICE_ADMIN）与无障碍事件监听（typeAllMask），设备管理员本身构成后续卸载阻力
- **良性降级 / 替代方案**：无。未提供手动模式、ADB 或仅观看等替代路径，弹窗只有唯一 OK 且强制导向设置页

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后监测到 Activity 栈顶变为 com.resterent.ds.StartDialog（或捕获到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity）即立刻拉起 UTG，此时是唯一不可跳过的人工确认节点
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无明显盲区：文案全部为 strings.xml 明文字符串，非图片、非远端 HTML。唯一需注意 StDlgSrs 的实际拉起时机由后台 Service/广播决定，若设备未触发服务启动则可能只看到一次弹窗；另 targetSdk=19 场景下系统不会出现 Android 13 受限设置拦截，UTG 不应以「未出现受限设置教学」作为良性判据。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动假故障引导弹窗页** | com.resterent.ds.StartDialog，标题 Attention，正文含 Unfortunately Google Play Services has stopped，仅一个 OK 按钮 | 此页是恐吓文案、无取消设计、品牌冒用的集中呈现处，UTG 可直接提取完整文本并验证返回键是否失效 | 标题 Attention 与正文含 Google Play Services has stopped；只有一个可点击按钮 OK（无取消/跳过）；按返回键后弹窗仍在（onBackPressed 空实现） |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载服务中的条目「Google Services」，无副标题描述 | 可验证服务标签与已安装应用名 Willhaben 的身份错配，以及 android:description 缺失导致的零说明 | 服务名称为 Google Services；条目无任何描述副文本；返回后弹窗再次出现（重拉循环） |
| **获权后设备管理员申请弹窗** | com.resterent.ui.AdRequestDialog（进程名 com.googleplay.activities.AdminRequestDialog）及随后系统 ADD_DEVICE_ADMIN 页 | 证明无障碍授权只是第一步，紧接着索取设备管理员权限，用于区分单纯无障碍引导与后续提权链 | 弹窗文案 Click on Activate button to secure your application；系统管理员页标签 Play Market；随后出现 Google Service was successfully enabled 收尾提示 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.resterent.ds.StartDialog#showDialog`
- `com.resterent.ds.StartDialog$1#onClick`
- `com.resterent.ds.StartDialog#onBackPressed`
- `com.resterent.srs.StDlgSrs#mainTask`
- `com.resterent.srs.GPSzs#onServiceConnected`
- `res/xml/service_conf.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**静态可见性：完全可见（clear）**。整条引导链路（弹窗文案、按钮回调、跳转 Intent、无障碍配置）都在 DEX 和资源里明文实现，未使用加壳、AES 或远端 HTML 页面；`libobladaet-jni.so` 只承担 `hasEnabledGp`、`setEnabledGp`、`getAddDevicePackageFromJNI` 等状态读写与包名下发，不影响本条判定。

**引导流程（三步强制闭环）**

1. **假故障恐吓弹窗** — [StartDialog.showDialog()](<resource-unit:#1.dex1 code:com.resterent.ds.StartDialog#showDialog>) 以 `Attention` 为标题、把 `start_dialog_description` 与 `accessibilityservice_label` 拼接为正文（"Unfortunately Google Play Services has stopped… Google Services"），只挂一个 `OK` 按钮，并调用 `setCancelable(false)` + `setCanceledOnTouchOutside(false)`；[StartDialog.onBackPressed()](<resource-unit:#1.dex1 code:com.resterent.ds.StartDialog#onBackPressed>) 是空实现，**返回键完全失效**。
2. **唯一出路直达系统设置** — [StartDialog$1.onClick()](<resource-unit:#1.dex1 code:com.resterent.ds.StartDialog$1#onClick>) 里 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，不存在"取消/稍后/跳过"。
3. **后台线程周期性重拉** — [StDlgSrs.onStartCommand()](<resource-unit:#1.dex1 code:com.resterent.srs.StDlgSrs#onStartCommand>) → [StDlgSrs.mainTask()](<resource-unit:#1.dex1 code:com.resterent.srs.StDlgSrs#mainTask>) 起线程，再经 `IntTls.startDialogAccess` 以 `FLAG_ACTIVITY_NEW_TASK` 再次弹出同一弹窗，形成拒权后的重跳循环。
4. **获权后立即推进下一诱导** — [GPSzs.onServiceConnected()](<resource-unit:#1.dex1 code:com.resterent.srs.GPSzs#onServiceConnected>) 注册 `typeAllMask` 全事件监听，[GPSzs.handleAccessibilityEvent()](<resource-unit:#1.dex1 code:com.resterent.srs.GPSzs#handleAccessibilityEvent>) 在无设备管理员时经 `adReq`→`startOdminRequest` 拉起 `AdRequestDialog`（进程名伪装为 `com.googleplay.activities.AdminRequestDialog`）；随后 [AcsOfDialog.showDialog()](<resource-unit:#1.dex1 code:com.resterent.ds.AcsOfDialog#showDialog>) 用"Google Service was successfully enabled"收尾并 `minimizeApp` 隐藏自身。

**身份错配**：桌面名 `Willhaben`（`app_name`），系统无障碍列表里却显示 `Google Services`（`accessibilityservice_label`），而 [service_conf.xml](<resource-unit:#1 file:res/xml/service_conf.xml>) 未声明 `android:description`，设置页不给用户任何用途说明；`canRetrieveWindowContent="true"` + `typeAllMask` 为最高采集能力。

**缺失项**：未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转，也无 Android 13 受限设置分步教学（`targetSdkVersion=19`，机制上不适用）；未见 `GLOBAL_ACTION_BACK/HOME` 阻止撤权——获权后动作转向设备管理员与短信/覆盖层链路，不属于本轮 UTG 页面流转范围。

**边界**：未做真机复现，`StDlgSrs` 的实际启动时机（开机广播、`AlarmManager` 或指令服务）属运行期条件，但代码已具备完整强制引导能力，故判定不受影响。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导弹窗文案、按钮回调、ACTION_ACCESSIBILITY_SETTINGS 跳转、无障碍 service_conf 与 strings 均在 DEX/资源中明文完整可见；未使用加壳、AES 或远端 HTML 教学页。libobladaet-jni.so 仅提供 hasEnabledGp/setEnabledGp/getAddDevicePackageFromJNI 等状态与包名读写，不承载引导 UI 逻辑。",
  "summary_one_liner": "以 Willhaben 名义安装，用「Google Play Services 已停止」假故障弹窗（不可取消、返回键失效、无跳过）把唯一 OK 按钮直连 android.settings.ACCESSIBILITY_SETTINGS，配合名为 Google Services 的空描述无障碍服务与后台线程周期性重拉，构成无降级路径的强制诱导。",
  "disguise_identity": {
    "app_display_name": "Willhaben",
    "claimed_brand_or_persona": "Google Play Services / Google Services（虚构系统组件故障与修复提示，服务标签另伪装为 Play Market 设备管理员）",
    "a11y_service_label": "Google Services",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 完全缺失（settings 页不显示任何用途说明）；服务标签与桌面名不一致，冒用 Google 品牌；AdRequestDialog 通过 android:process=\"com.googleplay.activities.AdminRequestDialog\" 伪造进程名；设备管理员 receiver 标签为 Play Market；类名与字符串名大量缩写混淆（GPSzs、AcsOfDialog、GScclaf 等）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "引导说明页",
      "screen_or_component": "com.resterent.ds.StartDialog（Activity，portrait，系统设置返回后由后台线程重拉）",
      "trigger_event": "onCreate → ScrTls.scrOn → showDialog()；另由 StDlgSrs.mainTask 起的线程经 IntTls.startDialogAccess 以 FLAG_ACTIVITY_NEW_TASK 重复拉起",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Attention / Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable: Google Services / OK",
      "shown_text_zh": "注意 / 很遗憾 Google Play 服务已停止。为使设备正常运行，请在菜单中选择一行并自行启用：Google Services / 确定",
      "user_action_requested": "仅有一个 OK 按钮；setCancelable(false)、setCanceledOnTouchOutside(false)，onBackPressed 空实现，无取消、无跳过、返回键无效",
      "code_anchor": "com.resterent.ds.StartDialog#showDialog / #onBackPressed；res/values/strings.xml: start_dialog_warning、start_dialog_description、accessibilityservice_label"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS（系统无障碍服务列表页，列表项显示「Google Services」）",
      "trigger_event": "StartDialog$1.onClick(DialogInterface, int) 中 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Services",
      "shown_text_zh": "系统无障碍服务列表中显示为「Google Services」，无任何 android:description 说明文字",
      "user_action_requested": "要求用户在系统列表中手动找到并打开「Google Services」开关",
      "code_anchor": "com.resterent.ds.StartDialog$1#onClick；res/xml/service_conf.xml；res/values/strings.xml: accessibilityservice_label"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.resterent.srs.StDlgSrs（后台 Service，intent-filter action com.googleplay.srs.StDlgSrs）→ StDlgSrs$1 线程 → 再次拉起 StartDialog",
      "trigger_event": "StDlgSrs.onStartCommand → mainTask → new Thread(StDlgSrs$1).start() → IntTls.startDialogAccess（FLAG_ACTIVITY_NEW_TASK）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Attention / Unfortunately Google Play Services has stopped.",
      "shown_text_zh": "用户从设置页返回或拒绝授权后，后台线程再次以同一假故障弹窗抢占前台",
      "user_action_requested": "再次被迫点击 OK 回到无障碍设置页；无「拒绝并继续使用」路径",
      "code_anchor": "com.resterent.srs.StDlgSrs#onStartCommand / #mainTask；com.resterent.tls.IntTls#startDialogAccess"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.resterent.srs.GPSzs（AccessibilityService）→ com.resterent.ui.AdRequestDialog（伪装进程 com.googleplay.activities.AdminRequestDialog）→ com.resterent.ds.AcsOfDialog",
      "trigger_event": "GPSzs.onServiceConnected（注册 typeAllMask、feedbackAllMask、flagReportViewIds）→ onAccessibilityEvent → handleAccessibilityEvent：!hasAd() 时 adReq() → IntTls.startOdminRequest()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Willhaben / Google Service was successfully enabled / OK；设备管理员页文案 Click on Activate button to secure your application.",
      "shown_text_zh": "「Willhaben / Google 服务已成功启用 / 确定」；随后弹出设备管理员激活页，要求点击「激活」以「保护你的应用」",
      "user_action_requested": "点击 OK（AcsOfDialog$1.onClick → IntTls.minimizeApp 将自身最小化）；设备管理员页要求点击 Activate",
      "code_anchor": "com.resterent.srs.GPSzs#onServiceConnected / #handleAccessibilityEvent / #adReq；com.resterent.ds.AcsOfDialog#showDialog；com.resterent.ds.AcsOfDialog$1#onClick；com.resterent.tls.IntTls#startoAdminAction"
    }
  ],
  "text_presentation_locations": [
    "com.resterent.ds.StartDialog：原生 AlertDialog（BaseActivity 子类），标题 Attention，正文为 start_dialog_description + accessibilityservice_label 拼接，单按钮 OK，不可取消、不可点外部关闭、返回键被 onBackPressed 空实现吞掉",
    "系统无障碍设置页服务列表项：由 manifest 中 service android:label=\"@string/accessibilityservice_label\" 显示为「Google Services」；android:description 未声明，页面无任何用途说明",
    "com.resterent.ds.AcsOfDialog：获权后原生 AlertDialog，标题取 @string/app_name（Willhaben），正文 dlg_acc_on_desc = \"Google Service was successfully enabled\"",
    "com.resterent.ui.AdRequestDialog：设备管理员申请前置引导弹窗（独立进程 com.googleplay.activities.AdminRequestDialog），激活说明取 @string/admin_title = \"Click on Activate button to secure your application.\"，系统管理员页标签 @string/admin_device_label = \"Play Market\"",
    "未使用 WebView、本地 HTML 或悬浮窗承载引导文案；全部为原生 Dialog + 系统设置页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Unfortunately Google Play Services has stopped. For the correct operation of the device select a line in the menu and self-enable:",
      "text_zh": "很遗憾 Google Play 服务已停止。为使设备正常运行，请在菜单中选择一行并自行启用：",
      "source_location": "res/values/strings.xml key=start_dialog_description",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Attention",
      "text_zh": "注意",
      "source_location": "res/values/strings.xml key=start_dialog_warning",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Services",
      "text_zh": "Google 服务",
      "source_location": "res/values/strings.xml key=accessibilityservice_label（manifest 中无障碍服务 android:label 引用）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Service was successfully enabled",
      "text_zh": "Google 服务已成功启用",
      "source_location": "res/values/strings.xml key=dlg_acc_on_desc（AcsOfDialog.showDialog 使用）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Click on Activate button to secure your application.",
      "text_zh": "点击「激活」按钮以保护您的应用。",
      "source_location": "res/values/strings.xml key=admin_title（IntTls.startoAdminAction 的 ADD_EXPLANATION）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Play Market",
      "text_zh": "Play 商店",
      "source_location": "res/values/strings.xml key=admin_device_label（设备管理员 receiver android:label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Willhaben",
      "text_zh": "Willhaben（奥地利二手交易平台品牌）",
      "source_location": "res/values/strings.xml key=app_name（application android:label）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "StartDialog 的 onBackPressed 为空实现、setCancelable(false)，用户无法退出；从系统设置页返回后，StDlgSrs 后台线程（mainTask → StDlgSrs$1 → IntTls.startDialogAccess，FLAG_ACTIVITY_NEW_TASK）再次以同一假故障弹窗抢占前台，直到用户打开无障碍开关为止",
    "overlay_or_fake_settings": "未使用半透明遮罩、全屏悬浮窗或高仿系统无障碍开关页；直接跳转真实系统 ACCESSIBILITY_SETTINGS 页，靠服务标签「Google Services」冒充系统组件骗取点击",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=19，未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转或「点右上角菜单允许受限设置」的分步教学",
    "post_grant_anti_removal": "未发现 GLOBAL_ACTION_BACK/HOME 阻止撤权或监听设置页自动确认；获权后转向设备管理员申请（ADD_DEVICE_ADMIN）与无障碍事件监听（typeAllMask），设备管理员本身构成后续卸载阻力",
    "benign_graceful_degradation": "无。未提供手动模式、ADB 或仅观看等替代路径，弹窗只有唯一 OK 且强制导向设置页"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后监测到 Activity 栈顶变为 com.resterent.ds.StartDialog（或捕获到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivity）即立刻拉起 UTG，此时是唯一不可跳过的人工确认节点",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动假故障引导弹窗页",
        "page_identifier": "com.resterent.ds.StartDialog，标题 Attention，正文含 Unfortunately Google Play Services has stopped，仅一个 OK 按钮",
        "why_most_useful": "此页是恐吓文案、无取消设计、品牌冒用的集中呈现处，UTG 可直接提取完整文本并验证返回键是否失效",
        "observable_utg_signals": ["标题 Attention 与正文含 Google Play Services has stopped", "只有一个可点击按钮 OK（无取消/跳过）", "按返回键后弹窗仍在（onBackPressed 空实现）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载服务中的条目「Google Services」，无副标题描述",
        "why_most_useful": "可验证服务标签与已安装应用名 Willhaben 的身份错配，以及 android:description 缺失导致的零说明",
        "observable_utg_signals": ["服务名称为 Google Services", "条目无任何描述副文本", "返回后弹窗再次出现（重拉循环）"]
      },
      {
        "page_role": "获权后设备管理员申请弹窗",
        "page_identifier": "com.resterent.ui.AdRequestDialog（进程名 com.googleplay.activities.AdminRequestDialog）及随后系统 ADD_DEVICE_ADMIN 页",
        "why_most_useful": "证明无障碍授权只是第一步，紧接着索取设备管理员权限，用于区分单纯无障碍引导与后续提权链",
        "observable_utg_signals": ["弹窗文案 Click on Activate button to secure your application", "系统管理员页标签 Play Market", "随后出现 Google Service was successfully enabled 收尾提示"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无明显盲区：文案全部为 strings.xml 明文字符串，非图片、非远端 HTML。唯一需注意 StDlgSrs 的实际拉起时机由后台 Service/广播决定，若设备未触发服务启动则可能只看到一次弹窗；另 targetSdk=19 场景下系统不会出现 Android 13 受限设置拦截，UTG 不应以「未出现受限设置教学」作为良性判据。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.resterent.ds.StartDialog#showDialog",
    "com.resterent.ds.StartDialog$1#onClick",
    "com.resterent.ds.StartDialog#onBackPressed",
    "com.resterent.srs.StDlgSrs#mainTask",
    "com.resterent.srs.GPSzs#onServiceConnected",
    "res/xml/service_conf.xml"
  ]
}
```

</details>
