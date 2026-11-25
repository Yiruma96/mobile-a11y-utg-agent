# MR_080__441ad01dc1｜hiddad — Powerful Security

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：189.3s

## 1. 一句话核心结论

- **核心申请方式**：以电池优化/防应用重开话术包装无障碍权限，在电池优化页与权限汇总页弹「Access Permission」原生弹窗，点 CONTINUE 直跳系统无障碍设置并在 1 秒后压栈遮罩页引导开启，获权后自动点击系统设置页控件。
- **静态可见性说明**：应用未加壳，无障碍服务声明、跳转 Intent 常量、弹窗/遮罩文案均在 DEX 与 res 中明文可见；assets/privacy.html 与 terms.html 为第三方站点导出的静态页面，未参与无障碍引导链路。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `441ad01dc16241705b6a1dcd527f0947d782843764431bc0284ccd3544fdd3b2` |
| 包名 / 年份 | `com.antivirus.powerful.security` / 2018 |
| 家族 / 品类 | **hiddad**（同池样本数：4） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/18/a/apps-disguised-security-tools-bombard-users-ads-track-users-location.html |
| 桌面显示名 | Powerful Security |
| 引导页宣称品牌/身份 | Powerful Security（自称设备优化/安全防护工具） |
| 系统无障碍列表服务名 | Powerful Security |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务类名伪装为 BatteryOptimizeService（电池优化），无障碍配置描述写入「延长电池寿命、隐私绝对安全、可忽略隐私警告」；文案存在拼写错误 enalbe 以规避关键词匹配；未使用多 activity-alias 或伪造 isAccessibilityTool |
| 无障碍服务类名 | `com.antivirus.powerful.security.svc.BatteryOptimizeService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Powerful Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>        You can have the privacy warning ignored. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.antivirus.powerful.security.act.BatterySaverSelectActivity（电池/待机优化结果页） | onCreate 携带 operate=true 或用户点击优化按钮进入 h()，判定 BatteryOptimizeService.a() 为 false | 原生Dialog | **原文**：Access Permission / Grant the necessary permission to prevent others from uninstalling your apps. / CANCEL / CONTINUE<br>**译注**：「访问权限」/「授予必要权限以防止他人卸载您的应用」/「取消」「继续」 | 点击 CONTINUE 继续；提供 CANCEL 取消按钮 | `BatterySaverSelectActivity.h → com.anti.security.view.BatteryAccessibilityDialog.onCreate；strings: dialog_access_title/dialog_access_content/dialog_access_ok/dialog_access_cancel` |
| 2 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | BatteryAccessibilityDialog 的 CONTINUE 回调 onEnable() | 系统无障碍页 | **原文**：Please find and enable Powerful Security for proper working of advanced protection.<br>**译注**：请找到并开启 Powerful Security，以让高级防护正常工作。 | 在系统无障碍列表中找到并手动开启 Powerful Security 开关 | `BatterySaverSelectActivity.onEnable → ns.afa.a(Activity,int) → startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1588)；strings: usage_setting_guide_content` |
| 3 | 遮罩叠层指引 | com.antivirus.powerful.security.act.AccessibilityDialogActivity（压栈于系统设置页之上） | 跳转后 Handler.postDelayed(1000ms) 执行 BatterySaverSelectActivity$8.run → d() | 原生Activity | **原文**：To prevent apps from restarting and save battery power, please find and enable Powerful Security.<br>**译注**：为防止应用自动重启并节省电量，请找到并开启 Powerful Security。 | 阅读文案后关闭该页，回到系统设置页手动开启；无跳过/放弃开关 | `BatterySaverSelectActivity.d；AccessibilityDialogActivity.onCreate（读取 Intent extra 覆盖 TextView）；strings: accessibility_toast_text` |
| 4 | 引导说明页（权限汇总） | com.antivirus.powerful.security.act.GrantPermissonsActivity 权限清单（RecyclerView 三项：无障碍/通知/悬浮窗） | onCreate/onResume 调用 h() 刷新 mChecked，点击首项（mResId=2130837588） | 原生Activity | **原文**：Accessibility / System optimization and phone security / GRANT<br>**译注**：「无障碍」/「系统优化与手机安全」/「授予」 | 点击首项「Accessibility」行进入授权 | `GrantPermissonsActivity.d / h / $4.onClick；strings: acessibility/acessibility_content/grant` |
| 5 | 跳无障碍设置（复用链路） | 系统设置 ACCESSIBILITY_SETTINGS + AccessibilityDialogActivity 二次压栈 | GrantPermissonsActivity$4.onClick → afa.a(this.a, 1588)，随后 postDelayed 1000ms 执行 $4$1.run → g() | 系统无障碍页 | **原文**：Please find and enable Powerful Security for system optimization and phone security.<br>**译注**：请找到并开启 Powerful Security，用于系统优化与手机安全。 | 在系统设置中开启服务；无跳过路径 | `GrantPermissonsActivity$4.onClick / $4$1.run / g()；strings: accessibility_desc` |
| 6 | 获权后动作 | ns.afa / BatteryOptimizeService 无障碍服务监听 com.android.settings 页面 | onAccessibilityEvent(typeWindowStateChanged) 且包名为 com.android.settings | 不可静态还原 | 无 | 无（用户无感知） | `ns.afa.onAccessibilityEvent / ns.afa.a(AccessibilityNodeInfo,String[]) / ns.afa.b；BatteryOptimizeService.a(AccessibilityEvent)` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- BatterySaverSelectActivity：原生 Dialog（dialog_battery_accessibility_layout）显示 Access Permission 标题与防卸载说明，按钮 CANCEL/CONTINUE
- 系统无障碍列表项：android:description 来自 res/xml/top_accessbility.xml → @string/boost_tag_acc_kill_service_description（省电+隐私承诺长文案）
- 系统无障碍页之上压栈的 AccessibilityDialogActivity（activity_grant_permission 之外独立布局 2130968604）显示 accessibility_toast_text 或 Intent 传入的 accessibility_desc
- GrantPermissonsActivity 权限清单首行：Accessibility / System optimization and phone security（strings acessibility、acessibility_content），右上按钮 GRANT
- org.nt.notifylib.view.PermissionToastView + WindowManager.addView 全屏半透明遮罩（accessibility_toast_view.xml，@color/translucent_dark 背景 + hand 手势图 + GOT IT 按钮），在 MessageLockActivity 等页面复用
- assets/privacy.html、assets/terms.html：应用内条款/隐私声明页（Google Sites 导出静态页），非无障碍引导载体

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Access Permission | 访问权限 | `strings.xml dialog_access_title` | 受限设置分步教学 |
| en | Grant the necessary permission to prevent others from uninstalling your apps. | 授予必要权限以防止他人卸载您的应用。 | `strings.xml dialog_access_content` | 故障恐吓 |
| en | To prevent apps from restarting and save battery power, please find and enable Powerful Security. | 为防止应用自动重启并节省电量，请找到并开启 Powerful Security。 | `strings.xml accessibility_toast_text` | 清理工具伪装 |
| en | Please find and enable Powerful Security for system optimization and phone security. | 请找到并开启 Powerful Security，用于系统优化与手机安全。 | `strings.xml accessibility_desc` | 假反诈安全 |
| en | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Powerful Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe. You can have the privacy warning ignored. | 无障碍可阻止不需要的应用重新打开，也能延长电池寿命与耐用性。Powerful Security 仅用于优化设备功能，我们保证您的隐私与个人数据完全安全。您可以让隐私警告被忽略。 | `strings.xml boost_tag_acc_kill_service_description（top_accessbility.xml android:description）` | 教唆忽视警告 |
| en | Please find and enable Powerful Security for proper working of advanced protection. | 请找到并开启 Powerful Security，以让高级防护正常工作。 | `strings.xml usage_setting_guide_content` | 受限设置分步教学 |
| en | Accessibility | 无障碍 | `strings.xml acessibility（GrantPermissonsActivity 列表首项标题）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：未发现死循环强跳：BatterySaverSelectActivity.onResume 会 removeCallbacksAndMessages 清除延迟任务，仅当用户再次点击优化入口或权限清单项时才重新弹窗并跳转；但每次跳转后固定 1 秒压栈 AccessibilityDialogActivity 遮罩，返回后仍留在系统设置页需再次操作，形成反复引导。
- **遮罩叠层 / 高仿系统设置页**：非高仿系统页，但存在两类叠层：1) 跳转系统无障碍设置后 1 秒压栈 AccessibilityDialogActivity 全屏引导页；2) org.nt.notifylib.view.PermissionToastView 通过 WindowManager.addView 叠加半透明深色遮罩（maskLayout/translucent_dark）+ 手势动画 + GOT IT 按钮。
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：有：ns.afa.onAccessibilityEvent 与 BatteryOptimizeService 在 com.android.settings 页面（含 InstalledAppDetailsTop）按文案与 ViewId 查找控件并 performAction(16) 自动点击，含通过 createPackageContext("com.android.settings") 取 force_stop 字符串点击「强行停止」，可用于自动化确认与阻止用户操作；Manifest 同时声明 NewInstallAppReceiver 监听 PACKAGE_ADDED/REMOVED 与 StartFastChargeSettingReceiver。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：Hook 监测 startActivityForResult 中 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 的调用（ns.afa.a），在跳转瞬间截图系统无障碍列表；随后 800~1200ms 内再次抓取，捕捉压栈的 AccessibilityDialogActivity 遮罩页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：遮罩页含 hand 手势图与 mipmap 图标，但均有配套文本可提取，无需 OCR；获权后的自动点击行为发生在系统设置页内部，UTG 需在 com.android.settings 页面上监测非用户来源的控件点击才能捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前原生弹窗页** | BatteryAccessibilityDialog：标题 Access Permission、正文 Grant the necessary permission...、按钮 CANCEL/CONTINUE | 证明存在明确的诱导弹窗与用户点击确认路径，是「引导申请」的起点证据 | 文本 Access Permission；文本 Grant the necessary permission to prevent others from uninstalling your apps.；按钮 CONTINUE/CANCEL 同屏 |
| **系统无障碍服务列表项** | 设置 > 无障碍列表中的 Powerful Security 条目及其描述文本 | 核对服务标签与 android:description 话术是否与实际权限能力不符（省电/隐私承诺 vs 读取窗口内容+自动点击） | 条目名 Powerful Security；描述含 prolong the lifespan of battery / privacy and personal data is total safe；开关状态 off |
| **设置页后 1000ms 压栈遮罩页** | AccessibilityDialogActivity 全屏页，文案 To prevent apps from restarting and save battery power... | 直接证明在系统设置页之上叠层引导，区分于仅跳转设置的良性应用 | 当前前台为 com.antivirus.powerful.security 而底层为 com.android.settings；文案 accessibility_toast_text；无跳过按钮 |
| **权限汇总引导页** | GrantPermissonsActivity：列表首行 Accessibility / System optimization and phone security / GRANT | 证明无障碍与通知、悬浮窗权限被批量打包引导，属系统性提权流程 | 首行文本 Accessibility；副文本 System optimization and phone security；按钮 GRANT |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.antivirus.powerful.security.act.BatterySaverSelectActivity.h / onEnable / d`
- `ns.afa.a(android.app.Activity,int) → startActivityForResult("android.settings.ACCESSIBILITY_SETTINGS", 1588)`
- `com.antivirus.powerful.security.act.AccessibilityDialogActivity.onCreate`
- `com.antivirus.powerful.security.act.GrantPermissonsActivity$4.onClick / g()`
- `ns.afa.onAccessibilityEvent`
- `res/xml/top_accessbility.xml 与 res/values/strings.xml（boost_tag_acc_kill_service_description / accessibility_toast_text / dialog_access_*）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**静态可见性**：完整可静态还原（无加壳，跳转与文案均为明文常量），无需动态脱壳。

**引导链路（运行期 UTG 视角，5 步）**

1. **功能触发**：用户进入电池优化/待机优化流程，落到 [BatterySaverSelectActivity](<resource-unit:#1.dex1 code:com.antivirus.powerful.security.act.BatterySaverSelectActivity#h>)。`h()` 先判定 `BatteryOptimizeService.a()`（读 `Settings.Secure.enabled_accessibility_services`），未开启即弹原生 [BatteryAccessibilityDialog](<resource-unit:#1.dex1 code:com.anti.security.view.BatteryAccessibilityDialog#onCreate>)（`Access Permission` / `Grant the necessary permission to prevent others from uninstalling your apps.` / `CANCEL`·`CONTINUE`）。
2. **跳受限设置**：CONTINUE → [onEnable](<resource-unit:#1.dex1 code:com.antivirus.powerful.security.act.BatterySaverSelectActivity#onEnable>) → [ns.afa#a](<resource-unit:#1.dex1 code:ns.afa#a>) 执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1588)`。
3. **叠层指引**：跳转后 `postDelayed(1000L)` 触发 [BatterySaverSelectActivity$8#run](<resource-unit:#1.dex1 code:com.antivirus.powerful.security.act.BatterySaverSelectActivity$8#run>) → [#d](<resource-unit:#1.dex1 code:com.antivirus.powerful.security.act.BatterySaverSelectActivity#d>)，在系统无障碍页之上压入 [AccessibilityDialogActivity](<resource-unit:#1.dex1 code:com.antivirus.powerful.security.act.AccessibilityDialogActivity#onCreate>)，文案 `To prevent apps from restarting and save battery power, please find and enable Powerful Security.`（`accessibility_toast_text`）。
4. **权限汇总页复用同链路**：[GrantPermissonsActivity#d](<resource-unit:#1.dex1 code:com.antivirus.powerful.security.act.GrantPermissonsActivity#d>) 的列表首项即无障碍（标题 `Accessibility`／副文案 `System optimization and phone security`）；点击由 [GrantPermissonsActivity$4#onClick](<resource-unit:#1.dex1 code:com.antivirus.powerful.security.act.GrantPermissonsActivity$4#onClick>) 同样 `afa.a(...,1588)`，1 秒后 [#g](<resource-unit:#1.dex1 code:com.antivirus.powerful.security.act.GrantPermissonsActivity#g>) 拉起遮罩页，文案换成 `accessibility_desc`：`Please find and enable Powerful Security for system optimization and phone security.`（注意原文 `enalbe` 拼写错误）。
5. **获权后动作**：[ns.afa#onAccessibilityEvent](<resource-unit:#1.dex1 code:ns.afa#onAccessibilityEvent>) 在 `typeWindowStateChanged` 下针对 `com.android.settings` 页面按文案/ViewId 找控件并 `performAction(16)` 自动点击（含取 `com.android.settings:force_stop` 字符串点击「强行停止」），[BatteryOptimizeService](<resource-unit:#1.dex1 code:com.antivirus.powerful.security.svc.BatteryOptimizeService>) 同构逻辑并叠加 `createPackageContext` 取系统资源。

**关键特点**

- 身份与话术不匹配：服务标签/显示名均为 `Powerful Security`，[top_accessbility.xml](<resource-unit:#1 file:res/xml/top_accessbility.xml>) 与 strings 用「省电、防应用重开、隐私绝对安全、可忽略隐私警告」包装，而实际申请 `canRetrieveWindowContent` + `flagReportViewIds`，能力远超说明。
- 跳转前有 `CANCEL`，但跳转后 1 秒压栈引导页形成叠层遮挡，属引导性阻断而非严格死循环。
- 未发现 13+ 受限设置分步教学或 Session 安装器实现于本链路；`AccessibilityDialogActivity` 仅展示文案与关闭，不提供跳过开启的替代路径。
- 存在同家族形态的 `org.nt.notifylib.view.PermissionToastView` + `WindowManager.addView` 全屏半透明遮罩（`accessibility_toast_view.xml`，含 `hand` 手势图与 `GOT IT` 按钮），在 `MessageLockActivity` 等页面复用。

**风险登记**：R-001（medium / deceptive_behavior），证据图 EG-99018CF89AFA。

```json
{
  "static_visibility": "clear",
  "visibility_note": "应用未加壳，无障碍服务声明、跳转 Intent 常量、弹窗/遮罩文案均在 DEX 与 res 中明文可见；assets/privacy.html 与 terms.html 为第三方站点导出的静态页面，未参与无障碍引导链路。",
  "summary_one_liner": "以电池优化/防应用重开话术包装无障碍权限，在电池优化页与权限汇总页弹「Access Permission」原生弹窗，点 CONTINUE 直跳系统无障碍设置并在 1 秒后压栈遮罩页引导开启，获权后自动点击系统设置页控件。",
  "disguise_identity": {
    "app_display_name": "Powerful Security",
    "claimed_brand_or_persona": "Powerful Security（自称设备优化/安全防护工具）",
    "a11y_service_label": "Powerful Security",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务类名伪装为 BatteryOptimizeService（电池优化），无障碍配置描述写入「延长电池寿命、隐私绝对安全、可忽略隐私警告」；文案存在拼写错误 enalbe 以规避关键词匹配；未使用多 activity-alias 或伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.antivirus.powerful.security.act.BatterySaverSelectActivity（电池/待机优化结果页）",
      "trigger_event": "onCreate 携带 operate=true 或用户点击优化按钮进入 h()，判定 BatteryOptimizeService.a() 为 false",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Access Permission / Grant the necessary permission to prevent others from uninstalling your apps. / CANCEL / CONTINUE",
      "shown_text_zh": "「访问权限」/「授予必要权限以防止他人卸载您的应用」/「取消」「继续」",
      "user_action_requested": "点击 CONTINUE 继续；提供 CANCEL 取消按钮",
      "code_anchor": "BatterySaverSelectActivity.h → com.anti.security.view.BatteryAccessibilityDialog.onCreate；strings: dialog_access_title/dialog_access_content/dialog_access_ok/dialog_access_cancel"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "BatteryAccessibilityDialog 的 CONTINUE 回调 onEnable()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please find and enable Powerful Security for proper working of advanced protection.",
      "shown_text_zh": "请找到并开启 Powerful Security，以让高级防护正常工作。",
      "user_action_requested": "在系统无障碍列表中找到并手动开启 Powerful Security 开关",
      "code_anchor": "BatterySaverSelectActivity.onEnable → ns.afa.a(Activity,int) → startActivityForResult(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), 1588)；strings: usage_setting_guide_content"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.antivirus.powerful.security.act.AccessibilityDialogActivity（压栈于系统设置页之上）",
      "trigger_event": "跳转后 Handler.postDelayed(1000ms) 执行 BatterySaverSelectActivity$8.run → d()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "To prevent apps from restarting and save battery power, please find and enable Powerful Security.",
      "shown_text_zh": "为防止应用自动重启并节省电量，请找到并开启 Powerful Security。",
      "user_action_requested": "阅读文案后关闭该页，回到系统设置页手动开启；无跳过/放弃开关",
      "code_anchor": "BatterySaverSelectActivity.d；AccessibilityDialogActivity.onCreate（读取 Intent extra 覆盖 TextView）；strings: accessibility_toast_text"
    },
    {
      "step": 4,
      "stage": "引导说明页（权限汇总）",
      "screen_or_component": "com.antivirus.powerful.security.act.GrantPermissonsActivity 权限清单（RecyclerView 三项：无障碍/通知/悬浮窗）",
      "trigger_event": "onCreate/onResume 调用 h() 刷新 mChecked，点击首项（mResId=2130837588）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility / System optimization and phone security / GRANT",
      "shown_text_zh": "「无障碍」/「系统优化与手机安全」/「授予」",
      "user_action_requested": "点击首项「Accessibility」行进入授权",
      "code_anchor": "GrantPermissonsActivity.d / h / $4.onClick；strings: acessibility/acessibility_content/grant"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置（复用链路）",
      "screen_or_component": "系统设置 ACCESSIBILITY_SETTINGS + AccessibilityDialogActivity 二次压栈",
      "trigger_event": "GrantPermissonsActivity$4.onClick → afa.a(this.a, 1588)，随后 postDelayed 1000ms 执行 $4$1.run → g()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please find and enable Powerful Security for system optimization and phone security.",
      "shown_text_zh": "请找到并开启 Powerful Security，用于系统优化与手机安全。",
      "user_action_requested": "在系统设置中开启服务；无跳过路径",
      "code_anchor": "GrantPermissonsActivity$4.onClick / $4$1.run / g()；strings: accessibility_desc"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "ns.afa / BatteryOptimizeService 无障碍服务监听 com.android.settings 页面",
      "trigger_event": "onAccessibilityEvent(typeWindowStateChanged) 且包名为 com.android.settings",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（后台自动对系统设置页控件执行 performAction(16) 点击，含取 force_stop 字符串）",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "ns.afa.onAccessibilityEvent / ns.afa.a(AccessibilityNodeInfo,String[]) / ns.afa.b；BatteryOptimizeService.a(AccessibilityEvent)"
    }
  ],
  "text_presentation_locations": [
    "BatterySaverSelectActivity：原生 Dialog（dialog_battery_accessibility_layout）显示 Access Permission 标题与防卸载说明，按钮 CANCEL/CONTINUE",
    "系统无障碍列表项：android:description 来自 res/xml/top_accessbility.xml → @string/boost_tag_acc_kill_service_description（省电+隐私承诺长文案）",
    "系统无障碍页之上压栈的 AccessibilityDialogActivity（activity_grant_permission 之外独立布局 2130968604）显示 accessibility_toast_text 或 Intent 传入的 accessibility_desc",
    "GrantPermissonsActivity 权限清单首行：Accessibility / System optimization and phone security（strings acessibility、acessibility_content），右上按钮 GRANT",
    "org.nt.notifylib.view.PermissionToastView + WindowManager.addView 全屏半透明遮罩（accessibility_toast_view.xml，@color/translucent_dark 背景 + hand 手势图 + GOT IT 按钮），在 MessageLockActivity 等页面复用",
    "assets/privacy.html、assets/terms.html：应用内条款/隐私声明页（Google Sites 导出静态页），非无障碍引导载体"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Access Permission",
      "text_zh": "访问权限",
      "source_location": "strings.xml dialog_access_title",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant the necessary permission to prevent others from uninstalling your apps.",
      "text_zh": "授予必要权限以防止他人卸载您的应用。",
      "source_location": "strings.xml dialog_access_content",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "To prevent apps from restarting and save battery power, please find and enable Powerful Security.",
      "text_zh": "为防止应用自动重启并节省电量，请找到并开启 Powerful Security。",
      "source_location": "strings.xml accessibility_toast_text",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Please find and enable Powerful Security for system optimization and phone security.",
      "text_zh": "请找到并开启 Powerful Security，用于系统优化与手机安全。",
      "source_location": "strings.xml accessibility_desc",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Powerful Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe. You can have the privacy warning ignored.",
      "text_zh": "无障碍可阻止不需要的应用重新打开，也能延长电池寿命与耐用性。Powerful Security 仅用于优化设备功能，我们保证您的隐私与个人数据完全安全。您可以让隐私警告被忽略。",
      "source_location": "strings.xml boost_tag_acc_kill_service_description（top_accessbility.xml android:description）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Please find and enable Powerful Security for proper working of advanced protection.",
      "text_zh": "请找到并开启 Powerful Security，以让高级防护正常工作。",
      "source_location": "strings.xml usage_setting_guide_content",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility",
      "text_zh": "无障碍",
      "source_location": "strings.xml acessibility（GrantPermissonsActivity 列表首项标题）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "未发现死循环强跳：BatterySaverSelectActivity.onResume 会 removeCallbacksAndMessages 清除延迟任务，仅当用户再次点击优化入口或权限清单项时才重新弹窗并跳转；但每次跳转后固定 1 秒压栈 AccessibilityDialogActivity 遮罩，返回后仍留在系统设置页需再次操作，形成反复引导。",
    "overlay_or_fake_settings": "非高仿系统页，但存在两类叠层：1) 跳转系统无障碍设置后 1 秒压栈 AccessibilityDialogActivity 全屏引导页；2) org.nt.notifylib.view.PermissionToastView 通过 WindowManager.addView 叠加半透明深色遮罩（maskLayout/translucent_dark）+ 手势动画 + GOT IT 按钮。",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "有：ns.afa.onAccessibilityEvent 与 BatteryOptimizeService 在 com.android.settings 页面（含 InstalledAppDetailsTop）按文案与 ViewId 查找控件并 performAction(16) 自动点击，含通过 createPackageContext(\"com.android.settings\") 取 force_stop 字符串点击「强行停止」，可用于自动化确认与阻止用户操作；Manifest 同时声明 NewInstallAppReceiver 监听 PACKAGE_ADDED/REMOVED 与 StartFastChargeSettingReceiver。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "Hook 监测 startActivityForResult 中 Intent action 为 android.settings.ACCESSIBILITY_SETTINGS 的调用（ns.afa.a），在跳转瞬间截图系统无障碍列表；随后 800~1200ms 内再次抓取，捕捉压栈的 AccessibilityDialogActivity 遮罩页。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前原生弹窗页",
        "page_identifier": "BatteryAccessibilityDialog：标题 Access Permission、正文 Grant the necessary permission...、按钮 CANCEL/CONTINUE",
        "why_most_useful": "证明存在明确的诱导弹窗与用户点击确认路径，是「引导申请」的起点证据",
        "observable_utg_signals": ["文本 Access Permission", "文本 Grant the necessary permission to prevent others from uninstalling your apps.", "按钮 CONTINUE/CANCEL 同屏"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 > 无障碍列表中的 Powerful Security 条目及其描述文本",
        "why_most_useful": "核对服务标签与 android:description 话术是否与实际权限能力不符（省电/隐私承诺 vs 读取窗口内容+自动点击）",
        "observable_utg_signals": ["条目名 Powerful Security", "描述含 prolong the lifespan of battery / privacy and personal data is total safe", "开关状态 off"]
      },
      {
        "page_role": "设置页后 1000ms 压栈遮罩页",
        "page_identifier": "AccessibilityDialogActivity 全屏页，文案 To prevent apps from restarting and save battery power...",
        "why_most_useful": "直接证明在系统设置页之上叠层引导，区分于仅跳转设置的良性应用",
        "observable_utg_signals": ["当前前台为 com.antivirus.powerful.security 而底层为 com.android.settings", "文案 accessibility_toast_text", "无跳过按钮"]
      },
      {
        "page_role": "权限汇总引导页",
        "page_identifier": "GrantPermissonsActivity：列表首行 Accessibility / System optimization and phone security / GRANT",
        "why_most_useful": "证明无障碍与通知、悬浮窗权限被批量打包引导，属系统性提权流程",
        "observable_utg_signals": ["首行文本 Accessibility", "副文本 System optimization and phone security", "按钮 GRANT"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "遮罩页含 hand 手势图与 mipmap 图标，但均有配套文本可提取，无需 OCR；获权后的自动点击行为发生在系统设置页内部，UTG 需在 com.android.settings 页面上监测非用户来源的控件点击才能捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_OVERLAY_STACK_ON_SETTINGS"
  ],
  "code_anchors": [
    "com.antivirus.powerful.security.act.BatterySaverSelectActivity.h / onEnable / d",
    "ns.afa.a(android.app.Activity,int) → startActivityForResult(\"android.settings.ACCESSIBILITY_SETTINGS\", 1588)",
    "com.antivirus.powerful.security.act.AccessibilityDialogActivity.onCreate",
    "com.antivirus.powerful.security.act.GrantPermissonsActivity$4.onClick / g()",
    "ns.afa.onAccessibilityEvent",
    "res/xml/top_accessbility.xml 与 res/values/strings.xml（boost_tag_acc_kill_service_description / accessibility_toast_text / dialog_access_*）"
  ]
}
```

</details>
