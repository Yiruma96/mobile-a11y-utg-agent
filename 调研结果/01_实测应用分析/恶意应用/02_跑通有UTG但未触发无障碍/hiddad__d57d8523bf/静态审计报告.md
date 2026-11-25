# MR_119__d57d8523bf｜hiddad — Guardian Antivirus

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：130.9s

## 1. 一句话核心结论

- **核心申请方式**：以'省电优化/防自启/性能提升50%'话术在权限引导页加全屏遮罩手势动画教程中诱导用户手动开启名为 Guardian Antivirus 的无障碍服务，开启后在系统设置页自动点击'强行停止/确定'阻止卸载。
- **静态可见性说明**：无障碍引导链路全部静态可见：Java 代码（GrantPermissonsActivity / ns.afc / PermissionToastView）+ res/layout/accessibility_toast_view.xml + res/values/strings.xml。assets/privacy.html 与 assets/terms.html 仅为内嵌隐私政策/条款页，与无障碍引导无关，无远端 HTML 下发、无加密二阶段载荷。未运行验证的是拒绝后的具体重跳时序细节。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d57d8523bf53736937a2935635ef6677bcf7c20fca9b1403cc032dfce87ed1c7` |
| 包名 / 年份 | `com.antivirus.guardian.cleaner.security` / 2018 |
| 家族 / 品类 | **hiddad**（同池样本数：4） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/18/a/apps-disguised-security-tools-bombard-users-ads-track-users-location.html |
| 桌面显示名 | Guardian Antivirus |
| 引导页宣称品牌/身份 | Guardian Antivirus（伪装为系统级电池优化/反病毒清理工具） |
| 系统无障碍列表服务名 | Guardian Antivirus |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务类名为 BatteryOptimizeService（暗示仅做电池优化），实际能力是读取并操作 com.android.settings 界面；android:description 主动教唆'You can have the privacy warning ignored'（可忽略隐私警告）；strings.xml 中同时存在拼写变体 acessibility/accessibility 与 accessibility_desc/accessibility_toast_text 多套诱导文案，未使用空白挤出、同形字或多 activity-alias 伪装。 |
| 无障碍服务类名 | `com.antivirus.guardian.cleaner.security.svc.BatteryOptimizeService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Guardian Antivirus only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>        You can have the privacy warning ignored. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity | onCreate（写入埋点 grant_page_show 后调用 h() 逐项检查权限状态） | 原生Activity | **原文**：grant_page_show（埋点键名，界面文案取自 layout 2130968617 与 res 字符串）<br>**译注**：权限集中引导列表页，列出悬浮窗、通知使用权、无障碍三项授权状态 | 逐项点击未开启的权限条目（含页面左上返回箭头） | `com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity#onCreate` |
| 2 | 拒权反馈循环 | GrantPermissonsActivity 列表项状态刷新 | onResume / onActivityResult → h() | 原生Activity | **原文**：appEntity$NavHeadData.mChecked = BatteryOptimizeService.a();<br>**译注**：从系统设置返回后立即重读 enabled_accessibility_services，未开启项保持未勾选并继续呈现引导 | 继续点击未开启项，或点返回箭头离开（页面保留离开路径） | `com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity#h` |
| 3 | 引导说明页 | com.antivirus.guardian.cleaner.security.v.PermissionToastView（全屏遮罩视图） | onFinishInflate 装配 RecyclerView 循环动画、smoothScrollToPosition 与 hand 手势图 | 悬浮窗Overlay | **原文**：To prevent apps from restarting and save battery power, please find and enable Guardian Antivirus.<br>**译注**：为防止应用重新启动并节省电池电量，请找到并启用 Guardian Antivirus。 | 按遮罩中的手指动画与滚动演示，照做去系统设置里找到该服务并打开开关；底部按钮 usage_setting_guide_btn 用于确认/继续 | `res/layout/accessibility_toast_view.xml + com.antivirus.guardian.cleaner.security.v.PermissionToastView#onFinishInflate` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | GrantPermissonsActivity$4.onClick 判定 mResId==2130837588 且 !BatteryOptimizeService.a() 后调用 ns.afc.a(Activity,int) | 系统无障碍页 | **原文**：activity.startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), i2);<br>**译注**：以 startActivityForResult 直接拉起系统无障碍设置页，并置静态标志 k=true 供服务 onCreate 消费 | 在系统无障碍列表中找到 Guardian Antivirus 并手动打开开关 | `ns.afc#a(android.app.Activity, int)` |
| 5 | 系统无障碍页 | 系统无障碍服务列表项 Guardian Antivirus | 用户点击服务开关 | 系统无障碍页 | **原文**：Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Guardian Antivirus only in use of optimizing device functionality, we assure you your privacy and personal data is total safe. You can have the privacy warning ignored.<br>**译注**：无障碍功能可阻止不需要的应用重新打开，也能延长电池寿命与耐用度。Guardian Antivirus 仅用于优化设备功能，我们保证您的隐私和个人数据完全安全。您可以让隐私警告被忽略。 | 确认系统弹出的隐私警告并允许（描述文案主动引导忽略该警告） | `res/values/strings.xml#boost_tag_acc_kill_service_description（Manifest android:description）` |
| 6 | 获权后动作 | ns.afc（AccessibilityService，源文件 TopAccessibilityService.java） | 系统回调 onCreate（k==true 则清标志并走 a(-1001)）与 onAccessibilityEvent(TYPE_WINDOW_STATE_CHANGED) | 不可静态还原（无 UI，后台静默） | **原文**：findAccessibilityNodeInfosByText: force_stop_button / button1 / "Force stop" / "强行停止" / "强制停止" / "确定" 多语言数组；performAction(16)<br>**译注**：仅监听 com.android.settings 界面，用文本匹配定位'强行停止'与'确定'按钮并自动点击，实现对停止/卸载确认的代替操作 | 无（用户不知情，操作被服务代替执行） | `ns.afc#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- GrantPermissonsActivity 权限引导列表页（原生 Activity，逐项显示已/未开启状态）
- PermissionToastView 全屏半透明遮罩（res/layout/accessibility_toast_view.xml），内含 ic_launcher 图标 + accessibility_toast_text 文案 + RecyclerView 循环动画 + hand 手势图 + usage_setting_guide_btn 按钮
- 系统无障碍服务列表项 android:description（strings.xml boost_tag_acc_kill_service_description，含'可忽略隐私警告'）
- strings.xml accessibility_desc：Please find and enalbe Guardian Antivirus for system optimization and phone security.（注意原文拼写错误 enalbe）
- strings.xml battery_permission_desc：Guardian Antivirus use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%.
- strings.xml accessibility_toast_text：To prevent apps from restarting and save battery power, please find and enable Guardian Antivirus.
- assets/privacy.html / assets/terms.html：内嵌隐私政策与条款 WebView 页，与无障碍引导无直接文案关联

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | To prevent apps from restarting and save battery power, please find and enable Guardian Antivirus. | 为防止应用重新启动并节省电池电量，请找到并启用 Guardian Antivirus。 | `res/values/strings.xml key=accessibility_toast_text（呈现于 accessibility_toast_view.xml 的 tv_content）` | 清理工具伪装 |
| en | Please find and enalbe Guardian Antivirus for system optimization and phone security. | 请找到并启用 Guardian Antivirus，以进行系统优化和手机安全保护。 | `res/values/strings.xml key=accessibility_desc` | 假反诈安全 |
| en | Guardian Antivirus use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%. | Guardian Antivirus 使用无障碍功能帮您停止不必要的应用，可改善电池续航并将手机性能提升 50% 以上。 | `res/values/strings.xml key=battery_permission_desc` | 故障恐吓 |
| en | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Guardian Antivirus only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>        You can have the privacy warning ignored. | 无障碍功能可阻止不需要的应用重新打开，也能延长电池寿命与耐用度。Guardian Antivirus 仅用于优化设备功能，我们保证您的隐私和个人数据完全安全。您可以让隐私警告被忽略。 | `res/values/strings.xml key=boost_tag_acc_kill_service_description（Manifest 无障碍服务 android:description）` | 教唆忽视警告 |
| en | Guardian Antivirus | Guardian Antivirus（系统无障碍列表与桌面显示名一致） | `AndroidManifest.xml 无障碍服务 android:label / @string/app_name` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：在系统设置页返回后，GrantPermissonsActivity.onResume / onActivityResult 会再次执行 h()，重读 enabled_accessibility_services；若仍未开启，该项继续显示未勾选并保留点击引导（复检式循环，未发现 Handler/Timer 定时强制重跳或直接再次 startActivity）。同时 ns.afc.onCreate 在检测到标志 k 后会清除 k，避免重复计数。
- **遮罩叠层 / 高仿系统设置页**：有叠层引导：PermissionToastView 全屏半透明遮罩（background=@color/translucent_dark），内嵌应用图标、诱导文案、RecyclerView 循环播放操作动画与 hand 手势图，用于在真实系统设置之上演示'手指该点哪里'；不是高仿系统无障碍开关页（无伪造 Switch/开关控件）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：有：ns.afc#onAccessibilityEvent 仅针对 com.android.settings，用 findAccessibilityNodeInfosByText 匹配 force_stop_button、android:id/button1、'Force stop'/'强行停止'/'强制停止' 及 50 余种语言的'确定'数组，performAction(16) 自动点击，代替用户确认停止/卸载；并通过 createPackageContext("com.android.settings") 读取系统 force_stop 字符串做语言适配。未见 GLOBAL_ACTION_BACK/HOME 主动阻止撤权。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条最佳拉起点：①监测到应用发起 Intent(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（由 ns.afc#a(Activity,int) 触发，跳转前一刻），用于抓取跳转前的遮罩教程页；②冷启动进入 GrantPermissonsActivity 且列表存在未勾选无障碍项时，用于抓取权限引导列表页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无静态加壳、无远端 HTML 下发，引导文案全部为可提取文本；唯一盲区是 ns.afc 获权后的自动点击行为无 UI 呈现（纯无障碍事件驱动），需通过窗口状态变化而非页面文本判定；另 GrantPermissonsActivity 的三项权限列表顺序与具体 item 布局未逐条读取 layout，UTG 抓取时以实际渲染为准。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **权限引导列表页** | GrantPermissonsActivity，列表含 mResId 2130837588（无障碍）项，标题栏为 @style/AppTheme.NoActionBar | 直接证明应用在正常运行路径中以列表形式逐项索权，并显示'未开启'状态，是最直观的索权入口证据 | 列表项文案与勾选状态；页面是否存在返回箭头（是否可跳过）；无障碍项是否与悬浮窗、通知使用权并列 |
| **跳转前遮罩手势教学页** | PermissionToastView 全屏遮罩，含 ic_launcher、accessibility_toast_text 文案、RecyclerView 动画区、hand 手势图、usage_setting_guide_btn 按钮 | 证明存在'照着手指点'的分步教学，是诱导开启无障碍的直接视觉证据；同时可判断是否覆盖在系统设置之上 | 遮罩文案原文；是否存在 hand 手势图与循环动画；遮罩按钮文案（usage_setting_guide_btn）；遮罩是否可取消/有无关闭按钮 |
| **系统无障碍服务列表项** | 设置→无障碍→已下载的服务中 'Guardian Antivirus' 条目，描述文案以 'Accessibility can prevent unwanted applications from reopening' 开头 | 核对服务在系统层面的展示名与描述话术，判断身份错配与'教唆忽略隐私警告' | 服务显示名；description 全文；开关当前状态 |
| **获权后系统设置页自动点击现场** | com.android.settings 的 InstalledAppDetailsTop / 强行停止确认对话框 | 验证无障碍服务实际接管系统界面并自动点击'强行停止/确定'，是反卸载机制的关键运行证据 | 强行停止确认对话框是否在无用户触摸下自动消失；点击后焦点/窗口变化；是否存在模拟点击的 AccessibilityEvent |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity#h`
- `com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity$4#onClick`
- `ns.afc#a(android.app.Activity, int)`
- `ns.afc#onAccessibilityEvent`
- `com.antivirus.guardian.cleaner.security.v.PermissionToastView#onFinishInflate`
- `res/layout/accessibility_toast_view.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**可见性判断：** `clear`。该样本没有加壳，也没有 VMP。无障碍引导链路完全由 Java 代码、`res/layout` 和 `res/values/strings.xml` 静态呈现，没有远端 HTML 下发，也没有加密载荷参与引导；`assets/privacy.html`、`assets/terms.html` 只是内嵌的隐私政策页面，与无障碍引导无关。

**引导链路（逐步）：**
1. **业务触发页** [GrantPermissonsActivity](<resource-unit:#1.dex1 code:com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity>) 是权限集中引导页。它在 `onCreate` 中写入埋点 `grant_page_show`，并以列表形式列出悬浮窗、通知使用权、无障碍三项。
2. **逐项复检** [GrantPermissonsActivity#h()](<resource-unit:#1.dex1 code:com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity#h>) 通过 `BatteryOptimizeService.a()`（读取 `Settings.Secure` 的 `enabled_accessibility_services`）判断服务是否已开启；`onCreate`、`onResume`、`onActivityResult` 都会调用它，因此从系统设置返回后会立即重算。
3. **点击引导** [GrantPermissonsActivity$4#onClick](<resource-unit:#1.dex1 code:com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity$4#onClick>) 在未开启时直接发起跳转。
4. **跳受限设置** [ns.afc#a(Activity,int)](<resource-unit:#1.dex1 code:ns.afc#a(android.app.Activity, int)>) 会调用 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), i2)`，并置静态标志 `k=true`。
5. **系统无障碍列表** 显示服务名 `Guardian Antivirus`，`android:description` 用“优化设备、隐私完全安全、可忽略隐私警告”的话术。
6. **开启后回执** [ns.afc#onCreate](<resource-unit:#1.dex1 code:ns.afc#onCreate>) 检测到 `k` 后清标志，并执行 `a(-1001)`，表示“首次开启”分支。
7. **全屏遮罩手势教程** [accessibility_toast_view.xml](<resource-unit:#1 file:res/layout/accessibility_toast_view.xml>) 承载 `PermissionToastView`：半透明全屏遮罩、应用图标、说明文案、`RecyclerView` 循环动画和 `hand` 手势图，用于“照着手指点”的分步教学；按钮文案为 `usage_setting_guide_btn`（“知道了/去开启”）。
8. **获权后动作** [ns.afc#onAccessibilityEvent](<resource-unit:#1.dex1 code:ns.afc#onAccessibilityEvent>) 只监听 `com.android.settings` 的 `TYPE_WINDOW_STATE_CHANGED`，用 `findAccessibilityNodeInfosByText` 匹配 `force_stop_button`、`button1`、`Force stop`、`强行停止`、`强制停止` 及 50 余种语言的“确定”数组，然后 `performAction(16)` 自动点击；它还通过 `createPackageContext("com.android.settings")` 取系统 `force_stop` 字符串，以适配不同语言的系统。这样做的实际效果是：在应用详情页替用户点掉“强行停止/确认”，阻止停止与卸载。

**关键伪装点：** 无障碍服务类名叫 `BatteryOptimizeService`（电池优化），`android:description` 与 `boost_tag_acc_kill_service_description` 声称“延长电池寿命、提升性能 50%、隐私完全安全，可忽略隐私警告”，而实际能力是读取系统设置界面并自动点击。这里存在明显的“能力声明≠实际能力”错配，并且话术还主动教唆用户忽略隐私警告。

**边界说明：** 未动态运行验证“拒绝后是否定时死循环重跳”（静态只见到 `onResume` 复检与 `Handler.removeCallbacksAndMessages`，属复检式而非计时器强制重跳）；`PermissionToastView` 的具体调用方中，`MessageLockActivity` 已确认，`GrantPermissonsActivity` 侧通过同资源 id 关联，未逐条读全 `$2/$5` 的 `run()` 时序。这些不影响引导链路判定。

已登记风险 R-001（high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链路全部静态可见：Java 代码（GrantPermissonsActivity / ns.afc / PermissionToastView）+ res/layout/accessibility_toast_view.xml + res/values/strings.xml。assets/privacy.html 与 assets/terms.html 仅为内嵌隐私政策/条款页，与无障碍引导无关，无远端 HTML 下发、无加密二阶段载荷。未运行验证的是拒绝后的具体重跳时序细节。",
  "summary_one_liner": "以'省电优化/防自启/性能提升50%'话术在权限引导页加全屏遮罩手势动画教程中诱导用户手动开启名为 Guardian Antivirus 的无障碍服务，开启后在系统设置页自动点击'强行停止/确定'阻止卸载。",
  "disguise_identity": {
    "app_display_name": "Guardian Antivirus",
    "claimed_brand_or_persona": "Guardian Antivirus（伪装为系统级电池优化/反病毒清理工具）",
    "a11y_service_label": "Guardian Antivirus",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务类名为 BatteryOptimizeService（暗示仅做电池优化），实际能力是读取并操作 com.android.settings 界面；android:description 主动教唆'You can have the privacy warning ignored'（可忽略隐私警告）；strings.xml 中同时存在拼写变体 acessibility/accessibility 与 accessibility_desc/accessibility_toast_text 多套诱导文案，未使用空白挤出、同形字或多 activity-alias 伪装。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity",
      "trigger_event": "onCreate（写入埋点 grant_page_show 后调用 h() 逐项检查权限状态）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "grant_page_show（埋点键名，界面文案取自 layout 2130968617 与 res 字符串）",
      "shown_text_zh": "权限集中引导列表页，列出悬浮窗、通知使用权、无障碍三项授权状态",
      "user_action_requested": "逐项点击未开启的权限条目（含页面左上返回箭头）",
      "code_anchor": "com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "拒权反馈循环",
      "screen_or_component": "GrantPermissonsActivity 列表项状态刷新",
      "trigger_event": "onResume / onActivityResult → h()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "appEntity$NavHeadData.mChecked = BatteryOptimizeService.a();",
      "shown_text_zh": "从系统设置返回后立即重读 enabled_accessibility_services，未开启项保持未勾选并继续呈现引导",
      "user_action_requested": "继续点击未开启项，或点返回箭头离开（页面保留离开路径）",
      "code_anchor": "com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity#h"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.antivirus.guardian.cleaner.security.v.PermissionToastView（全屏遮罩视图）",
      "trigger_event": "onFinishInflate 装配 RecyclerView 循环动画、smoothScrollToPosition 与 hand 手势图",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "To prevent apps from restarting and save battery power, please find and enable Guardian Antivirus.",
      "shown_text_zh": "为防止应用重新启动并节省电池电量，请找到并启用 Guardian Antivirus。",
      "user_action_requested": "按遮罩中的手指动画与滚动演示，照做去系统设置里找到该服务并打开开关；底部按钮 usage_setting_guide_btn 用于确认/继续",
      "code_anchor": "res/layout/accessibility_toast_view.xml + com.antivirus.guardian.cleaner.security.v.PermissionToastView#onFinishInflate"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "GrantPermissonsActivity$4.onClick 判定 mResId==2130837588 且 !BatteryOptimizeService.a() 后调用 ns.afc.a(Activity,int)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "activity.startActivityForResult(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), i2);",
      "shown_text_zh": "以 startActivityForResult 直接拉起系统无障碍设置页，并置静态标志 k=true 供服务 onCreate 消费",
      "user_action_requested": "在系统无障碍列表中找到 Guardian Antivirus 并手动打开开关",
      "code_anchor": "ns.afc#a(android.app.Activity, int)"
    },
    {
      "step": 5,
      "stage": "系统无障碍页",
      "screen_or_component": "系统无障碍服务列表项 Guardian Antivirus",
      "trigger_event": "用户点击服务开关",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Guardian Antivirus only in use of optimizing device functionality, we assure you your privacy and personal data is total safe. You can have the privacy warning ignored.",
      "shown_text_zh": "无障碍功能可阻止不需要的应用重新打开，也能延长电池寿命与耐用度。Guardian Antivirus 仅用于优化设备功能，我们保证您的隐私和个人数据完全安全。您可以让隐私警告被忽略。",
      "user_action_requested": "确认系统弹出的隐私警告并允许（描述文案主动引导忽略该警告）",
      "code_anchor": "res/values/strings.xml#boost_tag_acc_kill_service_description（Manifest android:description）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "ns.afc（AccessibilityService，源文件 TopAccessibilityService.java）",
      "trigger_event": "系统回调 onCreate（k==true 则清标志并走 a(-1001)）与 onAccessibilityEvent(TYPE_WINDOW_STATE_CHANGED)",
      "ui_carrier": "不可静态还原（无 UI，后台静默）",
      "shown_text_verbatim": "findAccessibilityNodeInfosByText: force_stop_button / button1 / \"Force stop\" / \"强行停止\" / \"强制停止\" / \"确定\" 多语言数组；performAction(16)",
      "shown_text_zh": "仅监听 com.android.settings 界面，用文本匹配定位'强行停止'与'确定'按钮并自动点击，实现对停止/卸载确认的代替操作",
      "user_action_requested": "无（用户不知情，操作被服务代替执行）",
      "code_anchor": "ns.afc#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "GrantPermissonsActivity 权限引导列表页（原生 Activity，逐项显示已/未开启状态）",
    "PermissionToastView 全屏半透明遮罩（res/layout/accessibility_toast_view.xml），内含 ic_launcher 图标 + accessibility_toast_text 文案 + RecyclerView 循环动画 + hand 手势图 + usage_setting_guide_btn 按钮",
    "系统无障碍服务列表项 android:description（strings.xml boost_tag_acc_kill_service_description，含'可忽略隐私警告'）",
    "strings.xml accessibility_desc：Please find and enalbe Guardian Antivirus for system optimization and phone security.（注意原文拼写错误 enalbe）",
    "strings.xml battery_permission_desc：Guardian Antivirus use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%.",
    "strings.xml accessibility_toast_text：To prevent apps from restarting and save battery power, please find and enable Guardian Antivirus.",
    "assets/privacy.html / assets/terms.html：内嵌隐私政策与条款 WebView 页，与无障碍引导无直接文案关联"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "To prevent apps from restarting and save battery power, please find and enable Guardian Antivirus.",
      "text_zh": "为防止应用重新启动并节省电池电量，请找到并启用 Guardian Antivirus。",
      "source_location": "res/values/strings.xml key=accessibility_toast_text（呈现于 accessibility_toast_view.xml 的 tv_content）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Please find and enalbe Guardian Antivirus for system optimization and phone security.",
      "text_zh": "请找到并启用 Guardian Antivirus，以进行系统优化和手机安全保护。",
      "source_location": "res/values/strings.xml key=accessibility_desc",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Guardian Antivirus use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%.",
      "text_zh": "Guardian Antivirus 使用无障碍功能帮您停止不必要的应用，可改善电池续航并将手机性能提升 50% 以上。",
      "source_location": "res/values/strings.xml key=battery_permission_desc",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Guardian Antivirus only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.\n        You can have the privacy warning ignored.",
      "text_zh": "无障碍功能可阻止不需要的应用重新打开，也能延长电池寿命与耐用度。Guardian Antivirus 仅用于优化设备功能，我们保证您的隐私和个人数据完全安全。您可以让隐私警告被忽略。",
      "source_location": "res/values/strings.xml key=boost_tag_acc_kill_service_description（Manifest 无障碍服务 android:description）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Guardian Antivirus",
      "text_zh": "Guardian Antivirus（系统无障碍列表与桌面显示名一致）",
      "source_location": "AndroidManifest.xml 无障碍服务 android:label / @string/app_name",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "在系统设置页返回后，GrantPermissonsActivity.onResume / onActivityResult 会再次执行 h()，重读 enabled_accessibility_services；若仍未开启，该项继续显示未勾选并保留点击引导（复检式循环，未发现 Handler/Timer 定时强制重跳或直接再次 startActivity）。同时 ns.afc.onCreate 在检测到标志 k 后会清除 k，避免重复计数。",
    "overlay_or_fake_settings": "有叠层引导：PermissionToastView 全屏半透明遮罩（background=@color/translucent_dark），内嵌应用图标、诱导文案、RecyclerView 循环播放操作动画与 hand 手势图，用于在真实系统设置之上演示'手指该点哪里'；不是高仿系统无障碍开关页（无伪造 Switch/开关控件）。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "有：ns.afc#onAccessibilityEvent 仅针对 com.android.settings，用 findAccessibilityNodeInfosByText 匹配 force_stop_button、android:id/button1、'Force stop'/'强行停止'/'强制停止' 及 50 余种语言的'确定'数组，performAction(16) 自动点击，代替用户确认停止/卸载；并通过 createPackageContext(\"com.android.settings\") 读取系统 force_stop 字符串做语言适配。未见 GLOBAL_ACTION_BACK/HOME 主动阻止撤权。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条最佳拉起点：①监测到应用发起 Intent(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（由 ns.afc#a(Activity,int) 触发，跳转前一刻），用于抓取跳转前的遮罩教程页；②冷启动进入 GrantPermissonsActivity 且列表存在未勾选无障碍项时，用于抓取权限引导列表页。",
    "key_pages_to_capture": [
      {
        "page_role": "权限引导列表页",
        "page_identifier": "GrantPermissonsActivity，列表含 mResId 2130837588（无障碍）项，标题栏为 @style/AppTheme.NoActionBar",
        "why_most_useful": "直接证明应用在正常运行路径中以列表形式逐项索权，并显示'未开启'状态，是最直观的索权入口证据",
        "observable_utg_signals": ["列表项文案与勾选状态", "页面是否存在返回箭头（是否可跳过）", "无障碍项是否与悬浮窗、通知使用权并列"]
      },
      {
        "page_role": "跳转前遮罩手势教学页",
        "page_identifier": "PermissionToastView 全屏遮罩，含 ic_launcher、accessibility_toast_text 文案、RecyclerView 动画区、hand 手势图、usage_setting_guide_btn 按钮",
        "why_most_useful": "证明存在'照着手指点'的分步教学，是诱导开启无障碍的直接视觉证据；同时可判断是否覆盖在系统设置之上",
        "observable_utg_signals": ["遮罩文案原文", "是否存在 hand 手势图与循环动画", "遮罩按钮文案（usage_setting_guide_btn）", "遮罩是否可取消/有无关闭按钮"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置→无障碍→已下载的服务中 'Guardian Antivirus' 条目，描述文案以 'Accessibility can prevent unwanted applications from reopening' 开头",
        "why_most_useful": "核对服务在系统层面的展示名与描述话术，判断身份错配与'教唆忽略隐私警告'",
        "observable_utg_signals": ["服务显示名", "description 全文", "开关当前状态"]
      },
      {
        "page_role": "获权后系统设置页自动点击现场",
        "page_identifier": "com.android.settings 的 InstalledAppDetailsTop / 强行停止确认对话框",
        "why_most_useful": "验证无障碍服务实际接管系统界面并自动点击'强行停止/确定'，是反卸载机制的关键运行证据",
        "observable_utg_signals": ["强行停止确认对话框是否在无用户触摸下自动消失", "点击后焦点/窗口变化", "是否存在模拟点击的 AccessibilityEvent"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无静态加壳、无远端 HTML 下发，引导文案全部为可提取文本；唯一盲区是 ns.afc 获权后的自动点击行为无 UI 呈现（纯无障碍事件驱动），需通过窗口状态变化而非页面文本判定；另 GrantPermissonsActivity 的三项权限列表顺序与具体 item 布局未逐条读取 layout，UTG 抓取时以实际渲染为准。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_SECURITY_ANTIFRADE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity#h",
    "com.antivirus.guardian.cleaner.security.act.GrantPermissonsActivity$4#onClick",
    "ns.afc#a(android.app.Activity, int)",
    "ns.afc#onAccessibilityEvent",
    "com.antivirus.guardian.cleaner.security.v.PermissionToastView#onFinishInflate",
    "res/layout/accessibility_toast_view.xml"
  ]
}
```

</details>
