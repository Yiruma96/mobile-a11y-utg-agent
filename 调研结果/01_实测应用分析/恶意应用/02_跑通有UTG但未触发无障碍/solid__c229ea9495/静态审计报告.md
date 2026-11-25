# MR_175__c229ea9495｜solid — Deep Cleaner

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：105.8s

## 1. 一句话核心结论

- **核心申请方式**：以“省电优化/深度清理”为名，在电池省电流程中弹出原生双按钮弹窗引导开启名为 BatteryOptimizeService 的无障碍服务，跳转系统无障碍列表后 1 秒压栈自定义提示页并循环重跳，获权后转为对系统应用详情页叠放悬浮窗并用无障碍批量点击强制停止第三方应用。
- **静态可见性说明**：应用未加壳（apkid 初判 False，DEX/布局/字符串均可反编译）。无障碍引导链路的 Activity/Dialog/布局/文案资源全部静态可见；唯一运行期变量是 cmaccessdia 遮罩页正文由 Intent extra "content" 注入，无法静态确定其逐字文本。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c229ea94958340fdbe928c8424a0fa365e3228a35701ab3dd4f81b69f3e0296b` |
| 包名 / 年份 | `com.antivirus.deep.cleaner` / 2018 |
| 家族 / 品类 | **solid**（同池样本数：60） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/18/a/apps-disguised-security-tools-bombard-users-ads-track-users-location.html |
| 桌面显示名 | Deep Cleaner |
| 引导页宣称品牌/身份 | Deep Cleaner（自称深度清理/省电优化工具，宣称可阻止应用自启、提升电池续航与性能 50% 以上，并保证隐私与个人数据完全安全） |
| 系统无障碍列表服务名 | Deep Cleaner（服务类名 com.anti.security.service.BatteryOptimizeService） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务类名伪装为 BatteryOptimizeService（电池优化）而实际用于设置页自动化点击；无障碍说明中夹带换行与“可忽略隐私警告”措辞；类名与资源键大量混淆（cmaccessdia、cmbatsavsel、cmoption）；同名引导组件分散为 Activity + Dialog + 悬浮窗三套载体；未发现伪造 isAccessibilityTool 或 activity-alias 多重伪装 |
| 无障碍服务类名 | `com.anti.security.service.BatteryOptimizeService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability.Deep Cleaner only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>        You can have the privacy warning ignored. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | cn.sc.sec.act.cmbatsavsel（电池省电结果/选择页，布局 activity_battery_select_layout） | 用户点击 tv_optimize 进入省电优化，或 onCreate 收到 Intent extra operate=true | 原生Activity | **原文**：draining_fast / running_apps / optimize<br>**译注**：展示耗电速度与运行应用数量，并提供“优化”按钮 | 点击“优化/一键省电”继续 | `cn.sc.sec.act.cmbatsavsel#onCreate` |
| 2 | 引导说明页 | cn.sc.sec.v.cmaccess（Dialog，布局 res/layout/dialog_battery_accessibility_layout.xml） | cmbatsavsel.trySuperSave() 检测 BatteryOptimizeService.a()==false（无障碍未开启）后 show() | 原生Dialog | **原文**：Deep Cleaner use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%. / Not now / Enable<br>**译注**：“Deep Cleaner 使用无障碍功能帮你停止不必要的应用，可提升电池续航与手机性能 50% 以上”，提供“暂不”与“开启”两个按钮 | 点击“Enable”开启无障碍；存在“Not now”取消按钮 | `cn.sc.sec.v.cmaccess#onCreate；res/layout/dialog_battery_accessibility_layout.xml；@string/battery_permission_desc` |
| 3 | 跳无障碍设置 | 系统页 android.settings.ACCESSIBILITY_SETTINGS | cmaccess$2.onClick → BatteryAccessibilityDialog.OnDialogBtnClickListener.onEnable → cmbatsavsel.onEnable | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：跳转系统“无障碍”设置页，用户需在列表中找到 Deep Cleaner 并手动开启 | 在系统列表中手动找到并开启 Deep Cleaner 服务（系统页含返回/关闭） | `ns.mt#a(Activity,int)；cn.sc.sec.act.cmbatsavsel#onEnable` |
| 4 | 遮罩叠层指引 | cn.sc.sec.act.cmaccessdia（Activity，布局 accessibility_toast_view） | onEnable 中 mHandler.postDelayed(cmbatsavsel$8, 1000L) → showAccessibilityToast() | 悬浮窗Overlay | **原文**：（正文由 Intent extra "content" 运行期注入，静态不可确定）<br>**译注**：跳转设置页 1 秒后在设置页之上压栈一个提示 TextView，指引用户在系统列表中开启服务 | 按提示在系统页中完成开启；同时 mHandler.post(checkAcessiblity) 持续检测授权状态 | `cn.sc.sec.act.cmaccessdia#onCreate；cn.sc.sec.act.cmbatsavsel#showAccessibilityToast` |
| 5 | 获权后动作 | cn.sc.sec.mgr.cmoption 叠放的 layout_battery_clean 悬浮窗 + 系统 android.settings.APPLICATION_DETAILS_SETTINGS 页面 | 无障碍开启后 cmoption.j()/a(int,Activity) 循环，每 3 秒（sendEmptyMessageDelayed 3000L）拉起下一个应用的详情页 | 悬浮窗Overlay | **原文**：tv_appindex / tv_total("/"+总数) / tv_cancel<br>**译注**：全屏悬浮窗显示正在强制停止的应用图标与“已处理/总数”进度，隐藏系统 UI 覆盖在应用详情页之上 | 无需用户操作，由无障碍服务自动定位 com.android.settings 的 force_stop 文本并 performAction(16) 点击 | `cn.sc.sec.mgr.cmoption#a(Activity,String)；cn.sc.sec.mgr.cmoption#j；ns.mt#a(AccessibilityNodeInfo,String[])` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目说明：res/xml/top_accessbility.xml 引用 @string/boost_tag_acc_kill_service_description（res/values/strings.xml 第 159 行）
- 电池省电流程内的原生 AlertDialog 式弹窗：res/layout/dialog_battery_accessibility_layout.xml（标题 enable_dr_security、正文 battery_permission_desc、按钮 not_now / enable2）
- 跳转系统无障碍页 1 秒后压栈的 Activity：res/layout/accessibility_toast_view.xml（正文由 Intent extra "content" 注入）
- 获权后在系统应用详情页之上叠放的全屏悬浮窗：res/layout/layout_battery_clean.xml（tv_appindex、tv_total、iv_cancel，配合 setSystemUiVisibility(5895) 隐藏状态栏）
- 悬浮窗/覆盖权限前置引导：cmoverlay 弹窗（cmbatsavsel.enableOverlayDIalog），点击后跳 android.settings.action.MANAGE_OVERLAY_PERMISSION
- 本地 HTML 资源 assets/privacy.html、assets/terms.html 仅为静态隐私政策/条款页面（Google Docs 导出样式），不承担无障碍引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability.Deep Cleaner only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>        You can have the privacy warning ignored. | 无障碍功能可阻止不想要的应用重新启动，还能延长电池寿命并提升其耐用性。Deep Cleaner 仅用于优化设备功能，我们保证您的隐私与个人数据完全安全。您可以让隐私警告被忽略。 | `res/values/strings.xml:159 (boost_tag_acc_kill_service_description，被 res/xml/top_accessbility.xml 引用为 android:description)` | 教唆忽视警告 |
| en | Deep Cleaner use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%. | Deep Cleaner 使用无障碍功能帮你停止不必要的应用，可将电池续航与手机性能提升 50% 以上。 | `res/values/strings.xml:153 (battery_permission_desc)，呈现在 res/layout/dialog_battery_accessibility_layout.xml 弹窗正文` | 清理工具伪装 |
| en | Not now | 暂不 | `res/layout/dialog_battery_accessibility_layout.xml @string/not_now（tv_cancel）` | 未知 |
| en | Enable | 开启 | `res/layout/dialog_battery_accessibility_layout.xml @string/enable2（tv_enable）` | 未知 |
| en | %1$s won't work unless you enable Google Play services. / Enable Google Play services | 除非启用 Google Play 服务，否则 %1$s 无法工作。/ 启用 Google Play 服务 | `GMS 依赖字符串（预筛字符串清单，来自内置 Google Play services 资源）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：弹窗提供 Not now 可取消，但无障碍是省电流程的硬性前置：trySuperSave() 每次检查 BatteryOptimizeService.a() 为 false 即重新 show() 弹窗；点击 Enable 后除跳系统无障碍页外，还会在 1000ms 后压栈 cmaccessdia 提示页并 post(checkAcessiblity) 持续检测，未授权则反复回到设置页/提示页，形成拒权重跳循环。
- **遮罩叠层 / 高仿系统设置页**：不使用高仿系统无障碍开关页；但会在系统无障碍页之上压栈自定义 cmaccessdia 提示 Activity，并在获权后的应用详情页之上叠放全屏半透明悬浮窗（layout_battery_clean，隐藏系统 UI）用于自动强停进度指引。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：有：无障碍服务启用后由 ns.mt 定位 com.android.settings 的 force_stop 文本并 performAction(16) 自动点击强停第三方应用；同时 Manifest 注册 PACKAGE_ADDED/PACKAGE_REPLACED/PACKAGE_REMOVED 广播（cn.sc.sec.rev.cmnewinstall）及 SCREEN_ON/USER_PRESENT/CLOSE_SYSTEM_DIALOGS 接收器（cn.sc.sec.rev.cmscreen）用于安装/卸载与屏幕状态监控，属抗移除/保活侧行为；未发现用 GLOBAL_ACTION_BACK/HOME 阻止用户撤权的显式代码。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 startActivity/startActivityForResult 的 action 为 android.settings.ACCESSIBILITY_SETTINGS（ns.mt.a）瞬间开始连续截屏，覆盖 0–3 秒窗口；同时以 cmbatsavsel 页面 tv_optimize 点击为起点，捕获前置 Dialog。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：一是 cmaccessdia 提示正文由 Intent extra "content" 运行期注入，纯静态无法获知逐字文案，需 UTG 截屏补证；二是引导弹窗的取消路径可能因版本/渠道配置而隐藏，且服务被命名/描述为 BatteryOptimizeService，若仅靠包名与文案关键字判定，容易漏检其为设置页自动化服务。应用本身未加壳，静态加壳不构成 UTG 阻挡。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/业务触发引导弹窗页** | cmaccess Dialog（320dip 白底卡片，图标 icon_clean_permission + 标题 + 双按钮 Not now/Enable） | 这是唯一向用户直接陈述“需要无障碍”并取得点击同意的界面，可判定是否以省电/清理名义索取高敏权限 | 弹窗文本包含 accessibility 与 battery/performance 混合话术；存在 Enable 主按钮且点击后立即跳系统无障碍页；同屏出现省电/清理类界面元素 |
| **跳转前系统无障碍服务列表项** | 系统 Settings 无障碍页中标签为 Deep Cleaner 的条目（类名 BatteryOptimizeService） | 核对系统展示的服务名与描述，确认身份伪装与说明文案 | 服务条目文本 Deep Cleaner；描述含 privacy 保证与“可忽略隐私警告”；条目位于“已下载的服务/未启用”分组 |
| **设置页后 1 秒压栈遮罩页** | cmaccessdia Activity（accessibility_toast_view，单个 TextView，内容由 Intent content 注入） | 证明应用在用户离开自身界面后仍持续指引，且文案运行期注入、静态不可见，是纯 UTG 才能取证的关键页 | 系统无障碍页上方出现应用自身 Activity 覆盖；覆盖层文本指向开启无障碍步骤；返回键后再次出现同一覆盖层 |
| **获权后应用详情页 + 悬浮窗自动强停页** | com.android.settings 应用详情页（InstalledAppDetailsTop）上方叠放 layout_battery_clean（应用图标 + 已处理/总数 + 取消） | 直接证明无障碍被用于自动化点击系统强停按钮，而非宣称的省电优化，且隐藏系统 UI 规避用户干预 | 状态栏/导航栏消失（setSystemUiVisibility 5895）；每约 3 秒自动切换应用详情页；无需用户触摸即出现“强制停止”确认对话框 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `cn.sc.sec.act.cmbatsavsel#onCreate`
- `cn.sc.sec.act.cmbatsavsel#trySuperSave`
- `cn.sc.sec.act.cmbatsavsel#onEnable`
- `cn.sc.sec.v.cmaccess#onCreate`
- `ns.mt#a(Activity,int)`
- `cn.sc.sec.act.cmaccessdia#onCreate`
- `cn.sc.sec.mgr.cmoption#j`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，静态可读）

**可见性：** 应用未加壳，无障碍引导链路的全部关键代码、布局和文案资源都能静态还原；唯一在运行期才能确定的，是 `cmaccessdia` 页面正文由 `Intent` 的 `content` 附加参数在运行时传入。

**引导链路（真实调用链，已逐跳核实）：**

1. **业务触发**：[cmbatsavsel.onCreate()](<resource-unit:#1.dex1 code:cn.sc.sec.act.cmbatsavsel#onCreate>) 在电池省电流程中构造 `cmaccess` 弹窗对象；如果进入时带有 `operate=true` 且悬浮窗权限尚未授予，就先弹出 `cmoverlay` 覆盖权限弹窗，否则走 `doSaver()`。在 [trySuperSave()](<resource-unit:#1.dex1 code:cn.sc.sec.act.cmbatsavsel#trySuperSave>) 中，只要 `BatteryOptimizeService.a()` 返回 false（表示无障碍未开启），就调用 `batteryAccessibilityDialog.show()`，这说明无障碍是硬性前置条件，而不是可选功能。
2. **引导弹窗（原生 Dialog，可以取消）**：[cmaccess.onCreate()](<resource-unit:#1.dex2 code:cn.sc.sec.v.cmaccess#onCreate>) 加载 [dialog_battery_accessibility_layout.xml](<resource-unit:#1 file:res/layout/dialog_battery_accessibility_layout.xml>)，包含“Not now / Enable”双按钮（`@string/not_now`、`@string/enable2`），标题为 `@string/enable_dr_security`，正文为 `@string/battery_permission_desc`（“Deep Cleaner use accessibility features to help you stop unnecessary app(s). Can improve battery life and boost phone performance more than 50%.”）。
3. **点击 Enable → 跳系统无障碍列表**：[cmaccess$2.onClick](<resource-unit:#1.dex2 code:cn.sc.sec.v.cmaccess$2#onClick>) → [cmbatsavsel.onEnable()](<resource-unit:#1.dex2 code:cn.sc.sec.act.cmbatsavsel#onEnable>) → [ns.mt.a(Activity,int)](<resource-unit:#1.dex2 code:ns.mt#a>) 执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，并把 `k=true` 记为已引导状态。
4. **1 秒后压栈遮罩提示页**：`postDelayed(1000L)` 触发 [cmbatsavsel$8.run()](<resource-unit:#1.dex2 code:cn.sc.sec.act.cmbatsavsel$8#run>)，调用 [showAccessibilityToast()](<resource-unit:#1.dex2 code:cn.sc.sec.act.cmbatsavsel#showAccessibilityToast>) 启动 [cmaccessdia](<resource-unit:#1.dex1 code:cn.sc.sec.act.cmaccessdia#onCreate>)（布局 [accessibility_toast_view](<resource-unit:#1 file:res/layout/accessibility_toast_view.xml>)，正文取自 Intent `content`），随后执行 `mHandler.post(checkAcessiblity)`，形成“返回后再次拉起设置”的检测与重跳循环。
5. **获权后转为对系统设置页进行无障碍自动操作**：[cn.sc.sec.mgr.cmoption.a(Activity,String)](<resource-unit:#1.dex1 code:cn.sc.sec.mgr.cmoption#a>) 用 `startActivityForResult` 打开 `android.settings.APPLICATION_DETAILS_SETTINGS`（requestCode 1024），同时通过 `WindowManager` 叠放 `layout_battery_clean` 全屏悬浮窗，并隐藏系统 UI（`setSystemUiVisibility(5895)`）；[cmoption.j()](<resource-unit:#1.dex1 code:cn.sc.sec.mgr.cmoption#j>) 在无障碍已开启时以 `sendEmptyMessageDelayed(..., 3000L)` 每 3 秒循环打开下一个应用的详情页；[ns.mt](<resource-unit:#1.dex2 code:ns.mt#a>) 则用 `findAccessibilityNodeInfosByText` 和 `performAction(16)` 定位 `com.android.settings` 的 `force_stop` 文本并点击，实现批量强制停止。

**伪装与矛盾点：** 服务类名 `BatteryOptimizeService`、服务标签 `Deep Cleaner`、`android:description` 都把权限描述成“省电/隐私安全”，配置 [top_accessbility.xml](<resource-unit:#1 file:res/xml/top_accessbility.xml>) 申请了 `typeWindowStateChanged + canRetrieveWindowContent`；但实际行为是自动化点击设置页、批量强停第三方应用，并配合 `PACKAGE_ADDED/REMOVED` 广播与 `cmnewinstall`/`cmpurev` 监听（抗卸载/安装监控），身份与真实用途明显不符。权限说明中还夹带换行与“privacy and personal data is total safe / 可忽略隐私警告”的措辞。

**未决边界：** `cmaccessdia` 的实际提示正文由运行期 Intent 注入，静态无法确定逐字文案；`enable_dr_security`、`enable2`、`not_now` 的值未逐条展开（`battery_permission_desc` 与无障碍 description 已取证）；Android 13+ 受限设置分步教学与 `isAccessibilityTool` 伪造在代码中未发现。

```json
{
  "static_visibility": "clear",
  "visibility_note": "应用未加壳（apkid 初判 False，DEX/布局/字符串均可反编译）。无障碍引导链路的 Activity/Dialog/布局/文案资源全部静态可见；唯一运行期变量是 cmaccessdia 遮罩页正文由 Intent extra \"content\" 注入，无法静态确定其逐字文本。",
  "summary_one_liner": "以“省电优化/深度清理”为名，在电池省电流程中弹出原生双按钮弹窗引导开启名为 BatteryOptimizeService 的无障碍服务，跳转系统无障碍列表后 1 秒压栈自定义提示页并循环重跳，获权后转为对系统应用详情页叠放悬浮窗并用无障碍批量点击强制停止第三方应用。",
  "disguise_identity": {
    "app_display_name": "Deep Cleaner",
    "claimed_brand_or_persona": "Deep Cleaner（自称深度清理/省电优化工具，宣称可阻止应用自启、提升电池续航与性能 50% 以上，并保证隐私与个人数据完全安全）",
    "a11y_service_label": "Deep Cleaner（服务类名 com.anti.security.service.BatteryOptimizeService）",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务类名伪装为 BatteryOptimizeService（电池优化）而实际用于设置页自动化点击；无障碍说明中夹带换行与“可忽略隐私警告”措辞；类名与资源键大量混淆（cmaccessdia、cmbatsavsel、cmoption）；同名引导组件分散为 Activity + Dialog + 悬浮窗三套载体；未发现伪造 isAccessibilityTool 或 activity-alias 多重伪装"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "cn.sc.sec.act.cmbatsavsel（电池省电结果/选择页，布局 activity_battery_select_layout）",
      "trigger_event": "用户点击 tv_optimize 进入省电优化，或 onCreate 收到 Intent extra operate=true",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "draining_fast / running_apps / optimize",
      "shown_text_zh": "展示耗电速度与运行应用数量，并提供“优化”按钮",
      "user_action_requested": "点击“优化/一键省电”继续",
      "code_anchor": "cn.sc.sec.act.cmbatsavsel#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "cn.sc.sec.v.cmaccess（Dialog，布局 res/layout/dialog_battery_accessibility_layout.xml）",
      "trigger_event": "cmbatsavsel.trySuperSave() 检测 BatteryOptimizeService.a()==false（无障碍未开启）后 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Deep Cleaner use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%. / Not now / Enable",
      "shown_text_zh": "“Deep Cleaner 使用无障碍功能帮你停止不必要的应用，可提升电池续航与手机性能 50% 以上”，提供“暂不”与“开启”两个按钮",
      "user_action_requested": "点击“Enable”开启无障碍；存在“Not now”取消按钮",
      "code_anchor": "cn.sc.sec.v.cmaccess#onCreate；res/layout/dialog_battery_accessibility_layout.xml；@string/battery_permission_desc"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "cmaccess$2.onClick → BatteryAccessibilityDialog.OnDialogBtnClickListener.onEnable → cmbatsavsel.onEnable",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "跳转系统“无障碍”设置页，用户需在列表中找到 Deep Cleaner 并手动开启",
      "user_action_requested": "在系统列表中手动找到并开启 Deep Cleaner 服务（系统页含返回/关闭）",
      "code_anchor": "ns.mt#a(Activity,int)；cn.sc.sec.act.cmbatsavsel#onEnable"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "cn.sc.sec.act.cmaccessdia（Activity，布局 accessibility_toast_view）",
      "trigger_event": "onEnable 中 mHandler.postDelayed(cmbatsavsel$8, 1000L) → showAccessibilityToast()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "（正文由 Intent extra \"content\" 运行期注入，静态不可确定）",
      "shown_text_zh": "跳转设置页 1 秒后在设置页之上压栈一个提示 TextView，指引用户在系统列表中开启服务",
      "user_action_requested": "按提示在系统页中完成开启；同时 mHandler.post(checkAcessiblity) 持续检测授权状态",
      "code_anchor": "cn.sc.sec.act.cmaccessdia#onCreate；cn.sc.sec.act.cmbatsavsel#showAccessibilityToast"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "cn.sc.sec.mgr.cmoption 叠放的 layout_battery_clean 悬浮窗 + 系统 android.settings.APPLICATION_DETAILS_SETTINGS 页面",
      "trigger_event": "无障碍开启后 cmoption.j()/a(int,Activity) 循环，每 3 秒（sendEmptyMessageDelayed 3000L）拉起下一个应用的详情页",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "tv_appindex / tv_total(\"/\"+总数) / tv_cancel",
      "shown_text_zh": "全屏悬浮窗显示正在强制停止的应用图标与“已处理/总数”进度，隐藏系统 UI 覆盖在应用详情页之上",
      "user_action_requested": "无需用户操作，由无障碍服务自动定位 com.android.settings 的 force_stop 文本并 performAction(16) 点击",
      "code_anchor": "cn.sc.sec.mgr.cmoption#a(Activity,String)；cn.sc.sec.mgr.cmoption#j；ns.mt#a(AccessibilityNodeInfo,String[])"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目说明：res/xml/top_accessbility.xml 引用 @string/boost_tag_acc_kill_service_description（res/values/strings.xml 第 159 行）",
    "电池省电流程内的原生 AlertDialog 式弹窗：res/layout/dialog_battery_accessibility_layout.xml（标题 enable_dr_security、正文 battery_permission_desc、按钮 not_now / enable2）",
    "跳转系统无障碍页 1 秒后压栈的 Activity：res/layout/accessibility_toast_view.xml（正文由 Intent extra \"content\" 注入）",
    "获权后在系统应用详情页之上叠放的全屏悬浮窗：res/layout/layout_battery_clean.xml（tv_appindex、tv_total、iv_cancel，配合 setSystemUiVisibility(5895) 隐藏状态栏）",
    "悬浮窗/覆盖权限前置引导：cmoverlay 弹窗（cmbatsavsel.enableOverlayDIalog），点击后跳 android.settings.action.MANAGE_OVERLAY_PERMISSION",
    "本地 HTML 资源 assets/privacy.html、assets/terms.html 仅为静态隐私政策/条款页面（Google Docs 导出样式），不承担无障碍引导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability.Deep Cleaner only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.\n        You can have the privacy warning ignored.",
      "text_zh": "无障碍功能可阻止不想要的应用重新启动，还能延长电池寿命并提升其耐用性。Deep Cleaner 仅用于优化设备功能，我们保证您的隐私与个人数据完全安全。您可以让隐私警告被忽略。",
      "source_location": "res/values/strings.xml:159 (boost_tag_acc_kill_service_description，被 res/xml/top_accessbility.xml 引用为 android:description)",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Deep Cleaner use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%.",
      "text_zh": "Deep Cleaner 使用无障碍功能帮你停止不必要的应用，可将电池续航与手机性能提升 50% 以上。",
      "source_location": "res/values/strings.xml:153 (battery_permission_desc)，呈现在 res/layout/dialog_battery_accessibility_layout.xml 弹窗正文",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Not now",
      "text_zh": "暂不",
      "source_location": "res/layout/dialog_battery_accessibility_layout.xml @string/not_now（tv_cancel）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable",
      "text_zh": "开启",
      "source_location": "res/layout/dialog_battery_accessibility_layout.xml @string/enable2（tv_enable）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services. / Enable Google Play services",
      "text_zh": "除非启用 Google Play 服务，否则 %1$s 无法工作。/ 启用 Google Play 服务",
      "source_location": "GMS 依赖字符串（预筛字符串清单，来自内置 Google Play services 资源）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "弹窗提供 Not now 可取消，但无障碍是省电流程的硬性前置：trySuperSave() 每次检查 BatteryOptimizeService.a() 为 false 即重新 show() 弹窗；点击 Enable 后除跳系统无障碍页外，还会在 1000ms 后压栈 cmaccessdia 提示页并 post(checkAcessiblity) 持续检测，未授权则反复回到设置页/提示页，形成拒权重跳循环。",
    "overlay_or_fake_settings": "不使用高仿系统无障碍开关页；但会在系统无障碍页之上压栈自定义 cmaccessdia 提示 Activity，并在获权后的应用详情页之上叠放全屏半透明悬浮窗（layout_battery_clean，隐藏系统 UI）用于自动强停进度指引。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "有：无障碍服务启用后由 ns.mt 定位 com.android.settings 的 force_stop 文本并 performAction(16) 自动点击强停第三方应用；同时 Manifest 注册 PACKAGE_ADDED/PACKAGE_REPLACED/PACKAGE_REMOVED 广播（cn.sc.sec.rev.cmnewinstall）及 SCREEN_ON/USER_PRESENT/CLOSE_SYSTEM_DIALOGS 接收器（cn.sc.sec.rev.cmscreen）用于安装/卸载与屏幕状态监控，属抗移除/保活侧行为；未发现用 GLOBAL_ACTION_BACK/HOME 阻止用户撤权的显式代码。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 startActivity/startActivityForResult 的 action 为 android.settings.ACCESSIBILITY_SETTINGS（ns.mt.a）瞬间开始连续截屏，覆盖 0–3 秒窗口；同时以 cmbatsavsel 页面 tv_optimize 点击为起点，捕获前置 Dialog。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/业务触发引导弹窗页",
        "page_identifier": "cmaccess Dialog（320dip 白底卡片，图标 icon_clean_permission + 标题 + 双按钮 Not now/Enable）",
        "why_most_useful": "这是唯一向用户直接陈述“需要无障碍”并取得点击同意的界面，可判定是否以省电/清理名义索取高敏权限",
        "observable_utg_signals": ["弹窗文本包含 accessibility 与 battery/performance 混合话术", "存在 Enable 主按钮且点击后立即跳系统无障碍页", "同屏出现省电/清理类界面元素"]
      },
      {
        "page_role": "跳转前系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页中标签为 Deep Cleaner 的条目（类名 BatteryOptimizeService）",
        "why_most_useful": "核对系统展示的服务名与描述，确认身份伪装与说明文案",
        "observable_utg_signals": ["服务条目文本 Deep Cleaner", "描述含 privacy 保证与“可忽略隐私警告”", "条目位于“已下载的服务/未启用”分组"]
      },
      {
        "page_role": "设置页后 1 秒压栈遮罩页",
        "page_identifier": "cmaccessdia Activity（accessibility_toast_view，单个 TextView，内容由 Intent content 注入）",
        "why_most_useful": "证明应用在用户离开自身界面后仍持续指引，且文案运行期注入、静态不可见，是纯 UTG 才能取证的关键页",
        "observable_utg_signals": ["系统无障碍页上方出现应用自身 Activity 覆盖", "覆盖层文本指向开启无障碍步骤", "返回键后再次出现同一覆盖层"]
      },
      {
        "page_role": "获权后应用详情页 + 悬浮窗自动强停页",
        "page_identifier": "com.android.settings 应用详情页（InstalledAppDetailsTop）上方叠放 layout_battery_clean（应用图标 + 已处理/总数 + 取消）",
        "why_most_useful": "直接证明无障碍被用于自动化点击系统强停按钮，而非宣称的省电优化，且隐藏系统 UI 规避用户干预",
        "observable_utg_signals": ["状态栏/导航栏消失（setSystemUiVisibility 5895）", "每约 3 秒自动切换应用详情页", "无需用户触摸即出现“强制停止”确认对话框"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：一是 cmaccessdia 提示正文由 Intent extra \"content\" 运行期注入，纯静态无法获知逐字文案，需 UTG 截屏补证；二是引导弹窗的取消路径可能因版本/渠道配置而隐藏，且服务被命名/描述为 BatteryOptimizeService，若仅靠包名与文案关键字判定，容易漏检其为设置页自动化服务。应用本身未加壳，静态加壳不构成 UTG 阻挡。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION"
  ],
  "code_anchors": [
    "cn.sc.sec.act.cmbatsavsel#onCreate",
    "cn.sc.sec.act.cmbatsavsel#trySuperSave",
    "cn.sc.sec.act.cmbatsavsel#onEnable",
    "cn.sc.sec.v.cmaccess#onCreate",
    "ns.mt#a(Activity,int)",
    "cn.sc.sec.act.cmaccessdia#onCreate",
    "cn.sc.sec.mgr.cmoption#j"
  ]
}
```

</details>
