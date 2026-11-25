# MR_156__b6ce31d96f｜solid — Powerful Security

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：138.3s

## 1. 一句话核心结论

- **核心申请方式**：以省电清理为名，在权限聚合页点击后直接跳系统无障碍设置、1 秒后在其上压栈原生说明页并轮询授权状态，描述文案明确教用户忽略系统隐私警告，获权后通过无障碍自动点按系统应用详情页的强制停止按钮。
- **静态可见性说明**：无障碍申请全链路（跳转、延时压栈说明页、轮询回调、获权后自动点击）均以明文 DEX 与 res/xml、strings.xml 静态可见，未见加壳、AES 载荷或远端 HTML 下发引导页；assets/privacy.html 与 terms.html 仅为本地隐私/条款页，不参与权限引导。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b6ce31d96ffd135ddc9e4819af09d5decc14af8e464fa93ee33e82623293d89a` |
| 包名 / 年份 | `com.antivirus.powerful.security` / 2018 |
| 家族 / 品类 | **solid**（同池样本数：60） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/18/a/apps-disguised-security-tools-bombard-users-ads-track-users-location.html |
| 桌面显示名 | Powerful Security |
| 引导页宣称品牌/身份 | Powerful Security（省电与系统优化、隐私保护工具） |
| 系统无障碍列表服务名 | Powerful Security（服务 android:label="@string/app_name"，类名为 com.anti.security.service.BatteryOptimizeService） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无同形字/多 activity-alias/空白挤出；但存在语义错配：无障碍服务命名与声明用途为 BatteryOptimize（省电），实际能力为 canRetrieveWindowContent + flagReportViewIds 的窗口读取与自动点击，并在 description 中明确教用户忽略系统隐私警告 |
| 无障碍服务类名 | `com.anti.security.service.BatteryOptimizeService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Powerful Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>        You can have the privacy warning ignored. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | an.sc.clean.act.smstapge（SplashTheme 启动页）→ an.sc.clean.act.smmain | LAUNCHER 点击图标，onCreate 后延时跳主页 | 原生Activity | **原文**：无（仅启动图）<br>**译注**：无实质文案，直接进入主页 | 无，被动进入 | `an.sc.clean.act.smstapge.onCreate / AndroidManifest activity smstapge` |
| 2 | 引导说明页 | com.anti.security.activity.GrantPermissonsActivity（layout activity_grant_permission，权限清单列表） | 主页/省电页跳转进入，onCreate→initData/updateData 渲染权限条目 | 原生Activity | **原文**：Access Permission / Grant the necessary permission to prevent others from uninstalling your apps. / CONTINUE / CANCEL<br>**译注**：「访问权限」/「授予必要权限以防止他人卸载你的应用」/「继续」/「取消」 | 在列表中点击无障碍条目（资源 id 2130837588）以继续，工具栏返回可退出 | `com.anti.security.activity.GrantPermissonsActivity.onCreate + strings.xml dialog_access_title/dialog_access_content` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | GrantPermissonsActivity$4.onClick 中 BatteryOptimizeService.a() 返回未开启时触发 | 系统无障碍页 | **原文**：无（系统页）<br>**译注**：跳转至系统「无障碍」服务列表，要求用户找到并开启 Powerful Security | 在系统无障碍列表中手动找到 Powerful Security 并打开开关 | `ns.ne#a(android.app.Activity, int) → startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` |
| 4 | 遮罩叠层指引 | an.sc.clean.act.smaccessdia（原生 Activity，layout accessibility_toast_view，AppTheme.NoActionBar） | 跳转后 Handler.postDelayed(1000ms) → GrantPermissonsActivity$4$1.run → showAccessibilityToast() | 原生Activity | **原文**：Please find and enalbe Powerful Security for system optimization and phone security.<br>**译注**：请找到并启用 Powerful Security，以实现系统优化与手机安全（原文含拼写错误 enalbe） | 按提示在下方系统列表中开启开关；该页无取消/跳过按钮，仅展示文案 | `com.anti.security.activity.GrantPermissonsActivity#showAccessibilityToast + an.sc.clean.act.smaccessdia.onCreate + strings.xml accessibility_desc` |
| 5 | 业务功能触发 | an.sc.clean.act.smbatsavsel（Battery Saver 页）弹出自定义对话框 an.sc.clean.v.smaccess（style upgrade_dialog_style） | 进入省电页 onCreate 弹出，点击对话框「开启」按钮 an.sc.clean.v.smaccess$2.onClick → onEnable() | 原生Dialog | **原文**：Enable %s to clean battery-consuming apps / To prevent apps from restarting and save battery power, please find and enable Powerful Security.<br>**译注**：「启用 %s 以清理耗电应用」/「为防止应用重启并省电，请找到并启用 Powerful Security」 | 点击开启，随后再次跳转系统无障碍设置并在 1 秒后压栈说明页 | `an.sc.clean.act.smbatsavsel#onEnable + an.sc.clean.v.smaccess$2#onClick + strings.xml dialog_tips / accessibility_toast_text` |
| 6 | 拒权反馈循环 | GrantPermissonsActivity 重新拉起（jumpBackFrombackgroundSetting） | GrantPermissonsActivity$2.run / $3.run 回调触发 | 原生Activity | 无 | 再次点击继续授权，形成反复引导 | `com.anti.security.activity.GrantPermissonsActivity#jumpBackFrombackgroundSetting` |
| 7 | 获权后动作 | ns.ne（TopAccessibilityService，即 com.anti.security.service.BatteryOptimizeService）onAccessibilityEvent | typeWindowStateChanged 事件，包名为 com.android.settings 且类名为 InstalledAppDetailsTop / InstalledAppDetailsActivity | 不可静态还原（后台自动点击，无界面） | **原文**：Force stop / 结束运行 / 强行停止 / 确定 / ok（自动匹配并点击）<br>**译注**：自动定位并点击「强制停止」「确定」按钮 | 无用户操作，服务自行 performAction(16) 点击 | `ns.ne#onAccessibilityEvent + ns.ne#a(java.util.List) + res/xml/top_accessbility.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项描述（android:description=@string/boost_tag_acc_kill_service_description，见 res/xml/top_accessbility.xml）
- 系统无障碍列表中的服务名（android:label=@string/app_name → Powerful Security）
- GrantPermissonsActivity 权限聚合页列表条目及 AlertDialog（strings.xml dialog_access_title / dialog_access_content / dialog_access_ok / dialog_access_cancel）
- 跳转系统无障碍设置 1 秒后压栈的原生 Activity an.sc.clean.act.smaccessdia（layout accessibility_toast_view），文案来自 strings.xml accessibility_desc
- Battery Saver 页自定义对话框 an.sc.clean.v.smaccess（strings.xml dialog_tips、accessibility_toast_text、battery_permission_desc）
- 系统设置返回后的授权页刷新与重新拉起（无独立文案，仅勾选状态变化）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Powerful Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.<br>        You can have the privacy warning ignored. | 无障碍功能可阻止不需要的应用重新打开，也能延长电池寿命与耐用度。Powerful Security 仅用于优化设备功能，我们保证你的隐私和个人数据完全安全。你可以忽略隐私警告。 | `res/values/strings.xml key=boost_tag_acc_kill_service_description（被 res/xml/top_accessbility.xml 引用）` | 教唆忽视警告 |
| en | Please find and enalbe Powerful Security for system optimization and phone security. | 请找到并启用 Powerful Security，以实现系统优化与手机安全。 | `res/values/strings.xml key=accessibility_desc，由 GrantPermissonsActivity.showAccessibilityToast 注入 smaccessdia 页面` | 清理工具伪装 |
| en | To prevent apps from restarting and save battery power, please find and enable Powerful Security. | 为防止应用重启并节省电量，请找到并启用 Powerful Security。 | `res/values/strings.xml key=accessibility_toast_text` | 系统错误或优化恐吓 |
| en | Powerful Security use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%. | Powerful Security 使用无障碍功能帮你停止不必要的应用，可提升电池续航与手机性能 50% 以上。 | `res/values/strings.xml key=battery_permission_desc` | 系统错误或优化恐吓 |
| en | Grant the necessary permission to prevent others from uninstalling your apps. | 授予必要权限，以防止他人卸载你的应用。 | `res/values/strings.xml key=dialog_access_content` | 假反诈安全 |
| en | Enable %s to clean battery-consuming apps | 启用 %s 以清理耗电应用。 | `res/values/strings.xml key=dialog_tips` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：从系统设置返回后 jumpBackFrombackgroundSetting() 以 FLAG_ACTIVITY_NEW_TASK(0x100000) 重新 startActivity 授权页并刷新勾选状态；同时跳转时 post(checkAcessiblity) 与 postDelayed(1000ms) 持续检测授权状态并再次压栈说明页，未授权条目保持未勾选直至用户开启
- **遮罩叠层 / 高仿系统设置页**：使用带 NoActionBar 主题的原生 Activity（smaccessdia）在系统无障碍列表上压栈充当引导层，非半透明悬浮窗、非高仿系统开关页；另在权限页申请 MANAGE_OVERLAY_PERMISSION 悬浮窗权限
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：onAccessibilityEvent 监听 com.android.settings 的 InstalledAppDetailsTop 页面，按多语言文案（Force stop/结束运行/强行停止/确定/ok）与 viewId（com.android.settings:id/force_stop_button、android:id/button1）自动 performAction(16) 点击，实现用户查看应用详情时自动强制停止/确认，阻止用户手动停用或卸载
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivityForResult（ns.ne.a）或 GrantPermissonsActivity 点击无障碍条目后 1000ms 内新出现的 Activity（smaccessdia），两者任一时机拉起 UTG
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案均为纯文本，无图片诱导；盲区在于获权后的自动点击行为发生在系统设置页，需 UTG 与无障碍事件/点击注入日志联动才能观测；应用未加壳，运行期无动态解密载荷，故不存在静态不可见的一阶段 Dropper。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前的权限聚合引导页** | com.anti.security.activity.GrantPermissonsActivity，列表中含 Accessibility 条目 + CONTINUE/CANCEL 文案 | 确认诱导起点与文案框架（防卸载恐吓），并记录是否提供取消/跳过 | 文本节点 'Access Permission' / 'Grant the necessary permission to prevent others from uninstalling your apps.'；可点击条目 'Accessibility' 与 CONTINUE 按钮；无 skip/稍后 控件 |
| **设置页后 1000ms 压栈的说明页** | an.sc.clean.act.smaccessdia，layout accessibility_toast_view，纯文本无按钮 | 证明该页在系统无障碍页之上叠加且无取消入口，是诱导关键证据 | 顶层 Activity 为 smaccessdia 而非系统 Settings；文本 'Please find and enalbe Powerful Security for system optimization and phone security.'；页面无可交互按钮 |
| **系统无障碍服务列表项** | 系统设置 Accessibility 列表中 label=Powerful Security 的开关项 | 核对系统展示名与描述是否与诱导文案一致、描述是否含忽略隐私警告的教唆 | 服务项标题 'Powerful Security'；描述含 'You can have the privacy warning ignored.'；开关初始状态为关闭 |
| **获权后自动点击的目标页** | 系统设置 InstalledAppDetailsTop（应用详情页） | 验证反卸载行为：服务自动点击「强制停止」「确定」 | 详情页出现后 100ms 内按钮被自动点击；无用户触摸事件却发生点击；强制停止确认弹窗自动消失 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `ns.ne#a(android.app.Activity, int)`
- `com.anti.security.activity.GrantPermissonsActivity#showAccessibilityToast`
- `com.anti.security.activity.GrantPermissonsActivity$4#onClick`
- `an.sc.clean.act.smbatsavsel#onEnable`
- `an.sc.clean.act.smaccessdia#onCreate`
- `ns.ne#onAccessibilityEvent`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**样本性质：`com.antivirus.powerful.security`（Powerful Security）是清理、省电类应用外壳，它使用无障碍服务进行自动化点击。核心逻辑全部位于 DEX，未加壳，静态可见性良好。**

**无障碍申请流程（纯运行期 UTG 视角）**

1. **入口**：Launcher 的 `an.sc.clean.act.smstapge`（SplashTheme）→ `smmain`；权限聚合页 [GrantPermissonsActivity](<resource-unit:#1.dex1 code:com.anti.security.activity.GrantPermissonsActivity#onCreate>) 以列表形式列出「使用情况访问、悬浮窗、无障碍」三项。
2. **触发跳转**：点击无障碍条目（资源 id 2130837588）且 `BatteryOptimizeService.a()` 判定未开启时，[GrantPermissonsActivity$4.onClick](<resource-unit:#1.dex1 code:com.anti.security.activity.GrantPermissonsActivity$4#onClick>) 调用 [ns.ne.a(Activity,int)](<resource-unit:#1.dex1 code:ns.ne#a(android.app.Activity, int)>) 直接执行 `startActivityForResult("android.settings.ACCESSIBILITY_SETTINGS")`，随后 `postDelayed(1000ms)`。
3. **设置页上的说明覆盖层**：1 秒后 [GrantPermissonsActivity.showAccessibilityToast()](<resource-unit:#1.dex1 code:com.anti.security.activity.GrantPermissonsActivity#showAccessibilityToast>) 在系统无障碍列表之上压栈启动 [an.sc.clean.act.smaccessdia](<resource-unit:#1.dex1 code:an.sc.clean.act.smaccessdia#onCreate>)（原生 Activity，layout `accessibility_toast_view`），文案为 `accessibility_desc`：“Please find and enalbe Powerful Security…”，同时 `post(checkAcessiblity)` 轮询授权状态。
4. **第二条入口**：省电页 `an.sc.clean.act.smbatsavsel` 弹出自定义 `an.sc.clean.v.smaccess` 对话框（`upgrade_dialog_style`），点击「开启」后 [onEnable()](<resource-unit:#1.dex1 code:an.sc.clean.act.smbatsavsel#onEnable>) 同样跳设置 + 1 秒后压栈说明页。
5. **拒绝后重新拉起**：`jumpBackFrombackgroundSetting()` 以 `addFlags(0x100000)` 重新启动 GrantPermissonsActivity，并由 `$2.run / $3.run` 驱动，形成「返回即重进授权页」的循环。
6. **获取权限后的动作（反卸载与自动点按）**：[ns.ne.onAccessibilityEvent](<resource-unit:#1.dex1 code:ns.ne#onAccessibilityEvent>) 仅在 `packageName == com.android.settings` 时对 `InstalledAppDetailsTop` 页面按多语言文案（"Force stop"/"结束运行"/"强行停止"/"确定"…）与 id `com.android.settings:id/force_stop_button`、`android:id/button1` 执行 `performAction(16)` 自动点击，即**用户查看应用详情时自动强制停止/确认**。

**关键恶意/诱导特征**
- 无障碍描述内直接**教唆忽视系统隐私警告**：“You can have the privacy warning ignored.”，并以「延长电池寿命、保证隐私绝对安全」作为承诺。
- 服务名为 `BatteryOptimizeService`（省电），实际行为是窗口内容读取 + 自动点击，用途与命名不符；系统列表显示名沿用 `@string/app_name`（Powerful Security），无额外伪装字形/多 alias。
- 未发现 `isAccessibilityTool`、伪造系统无障碍开关页、内嵌 a11y APK、13+ 受限设置教学（targetSdk 24 时代，`settings:APPLICATION_DETAILS_SETTINGS` 仅用于普通应用详情跳转）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍申请全链路（跳转、延时压栈说明页、轮询回调、获权后自动点击）均以明文 DEX 与 res/xml、strings.xml 静态可见，未见加壳、AES 载荷或远端 HTML 下发引导页；assets/privacy.html 与 terms.html 仅为本地隐私/条款页，不参与权限引导。",
  "summary_one_liner": "以省电清理为名，在权限聚合页点击后直接跳系统无障碍设置、1 秒后在其上压栈原生说明页并轮询授权状态，描述文案明确教用户忽略系统隐私警告，获权后通过无障碍自动点按系统应用详情页的强制停止按钮。",
  "disguise_identity": {
    "app_display_name": "Powerful Security",
    "claimed_brand_or_persona": "Powerful Security（省电与系统优化、隐私保护工具）",
    "a11y_service_label": "Powerful Security（服务 android:label=\"@string/app_name\"，类名为 com.anti.security.service.BatteryOptimizeService）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无同形字/多 activity-alias/空白挤出；但存在语义错配：无障碍服务命名与声明用途为 BatteryOptimize（省电），实际能力为 canRetrieveWindowContent + flagReportViewIds 的窗口读取与自动点击，并在 description 中明确教用户忽略系统隐私警告"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "an.sc.clean.act.smstapge（SplashTheme 启动页）→ an.sc.clean.act.smmain",
      "trigger_event": "LAUNCHER 点击图标，onCreate 后延时跳主页",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅启动图）",
      "shown_text_zh": "无实质文案，直接进入主页",
      "user_action_requested": "无，被动进入",
      "code_anchor": "an.sc.clean.act.smstapge.onCreate / AndroidManifest activity smstapge"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.anti.security.activity.GrantPermissonsActivity（layout activity_grant_permission，权限清单列表）",
      "trigger_event": "主页/省电页跳转进入，onCreate→initData/updateData 渲染权限条目",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Access Permission / Grant the necessary permission to prevent others from uninstalling your apps. / CONTINUE / CANCEL",
      "shown_text_zh": "「访问权限」/「授予必要权限以防止他人卸载你的应用」/「继续」/「取消」",
      "user_action_requested": "在列表中点击无障碍条目（资源 id 2130837588）以继续，工具栏返回可退出",
      "code_anchor": "com.anti.security.activity.GrantPermissonsActivity.onCreate + strings.xml dialog_access_title/dialog_access_content"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "GrantPermissonsActivity$4.onClick 中 BatteryOptimizeService.a() 返回未开启时触发",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页）",
      "shown_text_zh": "跳转至系统「无障碍」服务列表，要求用户找到并开启 Powerful Security",
      "user_action_requested": "在系统无障碍列表中手动找到 Powerful Security 并打开开关",
      "code_anchor": "ns.ne#a(android.app.Activity, int) → startActivityForResult(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "an.sc.clean.act.smaccessdia（原生 Activity，layout accessibility_toast_view，AppTheme.NoActionBar）",
      "trigger_event": "跳转后 Handler.postDelayed(1000ms) → GrantPermissonsActivity$4$1.run → showAccessibilityToast()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Please find and enalbe Powerful Security for system optimization and phone security.",
      "shown_text_zh": "请找到并启用 Powerful Security，以实现系统优化与手机安全（原文含拼写错误 enalbe）",
      "user_action_requested": "按提示在下方系统列表中开启开关；该页无取消/跳过按钮，仅展示文案",
      "code_anchor": "com.anti.security.activity.GrantPermissonsActivity#showAccessibilityToast + an.sc.clean.act.smaccessdia.onCreate + strings.xml accessibility_desc"
    },
    {
      "step": 5,
      "stage": "业务功能触发",
      "screen_or_component": "an.sc.clean.act.smbatsavsel（Battery Saver 页）弹出自定义对话框 an.sc.clean.v.smaccess（style upgrade_dialog_style）",
      "trigger_event": "进入省电页 onCreate 弹出，点击对话框「开启」按钮 an.sc.clean.v.smaccess$2.onClick → onEnable()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Enable %s to clean battery-consuming apps / To prevent apps from restarting and save battery power, please find and enable Powerful Security.",
      "shown_text_zh": "「启用 %s 以清理耗电应用」/「为防止应用重启并省电，请找到并启用 Powerful Security」",
      "user_action_requested": "点击开启，随后再次跳转系统无障碍设置并在 1 秒后压栈说明页",
      "code_anchor": "an.sc.clean.act.smbatsavsel#onEnable + an.sc.clean.v.smaccess$2#onClick + strings.xml dialog_tips / accessibility_toast_text"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "GrantPermissonsActivity 重新拉起（jumpBackFrombackgroundSetting）",
      "trigger_event": "GrantPermissonsActivity$2.run / $3.run 回调触发",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "从设置返回后重新打开授权页并刷新勾选状态，未授权条目保持未勾选",
      "user_action_requested": "再次点击继续授权，形成反复引导",
      "code_anchor": "com.anti.security.activity.GrantPermissonsActivity#jumpBackFrombackgroundSetting"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "ns.ne（TopAccessibilityService，即 com.anti.security.service.BatteryOptimizeService）onAccessibilityEvent",
      "trigger_event": "typeWindowStateChanged 事件，包名为 com.android.settings 且类名为 InstalledAppDetailsTop / InstalledAppDetailsActivity",
      "ui_carrier": "不可静态还原（后台自动点击，无界面）",
      "shown_text_verbatim": "Force stop / 结束运行 / 强行停止 / 确定 / ok（自动匹配并点击）",
      "shown_text_zh": "自动定位并点击「强制停止」「确定」按钮",
      "user_action_requested": "无用户操作，服务自行 performAction(16) 点击",
      "code_anchor": "ns.ne#onAccessibilityEvent + ns.ne#a(java.util.List) + res/xml/top_accessbility.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项描述（android:description=@string/boost_tag_acc_kill_service_description，见 res/xml/top_accessbility.xml）",
    "系统无障碍列表中的服务名（android:label=@string/app_name → Powerful Security）",
    "GrantPermissonsActivity 权限聚合页列表条目及 AlertDialog（strings.xml dialog_access_title / dialog_access_content / dialog_access_ok / dialog_access_cancel）",
    "跳转系统无障碍设置 1 秒后压栈的原生 Activity an.sc.clean.act.smaccessdia（layout accessibility_toast_view），文案来自 strings.xml accessibility_desc",
    "Battery Saver 页自定义对话框 an.sc.clean.v.smaccess（strings.xml dialog_tips、accessibility_toast_text、battery_permission_desc）",
    "系统设置返回后的授权页刷新与重新拉起（无独立文案，仅勾选状态变化）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Accessibility can prevent unwanted applications from reopening, also can prolong the lifespan of battery and extend their durability. Powerful Security only in use of optimizing device functionality, we assure you your privacy and personal data is total safe.\n        You can have the privacy warning ignored.",
      "text_zh": "无障碍功能可阻止不需要的应用重新打开，也能延长电池寿命与耐用度。Powerful Security 仅用于优化设备功能，我们保证你的隐私和个人数据完全安全。你可以忽略隐私警告。",
      "source_location": "res/values/strings.xml key=boost_tag_acc_kill_service_description（被 res/xml/top_accessbility.xml 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Please find and enalbe Powerful Security for system optimization and phone security.",
      "text_zh": "请找到并启用 Powerful Security，以实现系统优化与手机安全。",
      "source_location": "res/values/strings.xml key=accessibility_desc，由 GrantPermissonsActivity.showAccessibilityToast 注入 smaccessdia 页面",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "To prevent apps from restarting and save battery power, please find and enable Powerful Security.",
      "text_zh": "为防止应用重启并节省电量，请找到并启用 Powerful Security。",
      "source_location": "res/values/strings.xml key=accessibility_toast_text",
      "rhetorical_frame": "系统错误或优化恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Powerful Security use accessibility features to help you stop unnecessary app(s).Can improve battery life and boost phone performance more than 50%.",
      "text_zh": "Powerful Security 使用无障碍功能帮你停止不必要的应用，可提升电池续航与手机性能 50% 以上。",
      "source_location": "res/values/strings.xml key=battery_permission_desc",
      "rhetorical_frame": "系统错误或优化恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant the necessary permission to prevent others from uninstalling your apps.",
      "text_zh": "授予必要权限，以防止他人卸载你的应用。",
      "source_location": "res/values/strings.xml key=dialog_access_content",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable %s to clean battery-consuming apps",
      "text_zh": "启用 %s 以清理耗电应用。",
      "source_location": "res/values/strings.xml key=dialog_tips",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "从系统设置返回后 jumpBackFrombackgroundSetting() 以 FLAG_ACTIVITY_NEW_TASK(0x100000) 重新 startActivity 授权页并刷新勾选状态；同时跳转时 post(checkAcessiblity) 与 postDelayed(1000ms) 持续检测授权状态并再次压栈说明页，未授权条目保持未勾选直至用户开启",
    "overlay_or_fake_settings": "使用带 NoActionBar 主题的原生 Activity（smaccessdia）在系统无障碍列表上压栈充当引导层，非半透明悬浮窗、非高仿系统开关页；另在权限页申请 MANAGE_OVERLAY_PERMISSION 悬浮窗权限",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "onAccessibilityEvent 监听 com.android.settings 的 InstalledAppDetailsTop 页面，按多语言文案（Force stop/结束运行/强行停止/确定/ok）与 viewId（com.android.settings:id/force_stop_button、android:id/button1）自动 performAction(16) 点击，实现用户查看应用详情时自动强制停止/确认，阻止用户手动停用或卸载",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 的 startActivityForResult（ns.ne.a）或 GrantPermissonsActivity 点击无障碍条目后 1000ms 内新出现的 Activity（smaccessdia），两者任一时机拉起 UTG",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前的权限聚合引导页",
        "page_identifier": "com.anti.security.activity.GrantPermissonsActivity，列表中含 Accessibility 条目 + CONTINUE/CANCEL 文案",
        "why_most_useful": "确认诱导起点与文案框架（防卸载恐吓），并记录是否提供取消/跳过",
        "observable_utg_signals": ["文本节点 'Access Permission' / 'Grant the necessary permission to prevent others from uninstalling your apps.'", "可点击条目 'Accessibility' 与 CONTINUE 按钮", "无 skip/稍后 控件"]
      },
      {
        "page_role": "设置页后 1000ms 压栈的说明页",
        "page_identifier": "an.sc.clean.act.smaccessdia，layout accessibility_toast_view，纯文本无按钮",
        "why_most_useful": "证明该页在系统无障碍页之上叠加且无取消入口，是诱导关键证据",
        "observable_utg_signals": ["顶层 Activity 为 smaccessdia 而非系统 Settings", "文本 'Please find and enalbe Powerful Security for system optimization and phone security.'", "页面无可交互按钮"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 Accessibility 列表中 label=Powerful Security 的开关项",
        "why_most_useful": "核对系统展示名与描述是否与诱导文案一致、描述是否含忽略隐私警告的教唆",
        "observable_utg_signals": ["服务项标题 'Powerful Security'", "描述含 'You can have the privacy warning ignored.'", "开关初始状态为关闭"]
      },
      {
        "page_role": "获权后自动点击的目标页",
        "page_identifier": "系统设置 InstalledAppDetailsTop（应用详情页）",
        "why_most_useful": "验证反卸载行为：服务自动点击「强制停止」「确定」",
        "observable_utg_signals": ["详情页出现后 100ms 内按钮被自动点击", "无用户触摸事件却发生点击", "强制停止确认弹窗自动消失"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案均为纯文本，无图片诱导；盲区在于获权后的自动点击行为发生在系统设置页，需 UTG 与无障碍事件/点击注入日志联动才能观测；应用未加壳，运行期无动态解密载荷，故不存在静态不可见的一阶段 Dropper。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS"
  ],
  "code_anchors": [
    "ns.ne#a(android.app.Activity, int)",
    "com.anti.security.activity.GrantPermissonsActivity#showAccessibilityToast",
    "com.anti.security.activity.GrantPermissonsActivity$4#onClick",
    "an.sc.clean.act.smbatsavsel#onEnable",
    "an.sc.clean.act.smaccessdia#onCreate",
    "ns.ne#onAccessibilityEvent"
  ]
}
```

</details>
