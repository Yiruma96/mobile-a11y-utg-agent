# MB_052__c0e391e254｜Hydra — Commerzbank Sicherheitsupdate

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：113.5s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 Commerzbank 银行安全更新，冷启动即以全屏不可返回的四步教学弹窗把用户推向系统无障碍设置，开启一个无标签无描述的 InjAccessibilityService，取消即重拉、未开启则每 2 分钟闹钟与通知栏持续催促。
- **静态可见性说明**：无障碍诱导链路完整静态可见：入口 Activity、引导 Dialog、布局与 strings 文案、ACCESSIBILITY_SETTINGS 跳转、onCancel 重拉逻辑、AlarmManager 2 分钟周期催促均为明文代码与资源，无加壳/加密；仅获权后 InjAccessibilityService 的远控指令分发未在本轮展开。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c0e391e254b74359896d287069883652a4b8bfd9ce2fd20a3cd7b441e1cbd600` |
| 包名 / 年份 | `com.grand.snail` / 2023 |
| 家族 / 品类 | **Hydra**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Commerzbank Sicherheitsupdate |
| 引导页宣称品牌/身份 | Commerzbank（德国商业银行）安全更新补丁 |
| 系统无障碍列表服务名 | （空）无障碍服务未声明 android:label，配置文件无 android:description，系统列表中显示为空白项 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务无 label 无 description 呈空白项；第二个 launcher activity-alias 的 label 为 alternative_app_name="Settings"、图标 ic_settings_main，伪装成系统设置；设备管理员 receiver 的 label/description 为 "Google - do not disable this app" 冒充 Google；所有引导 Activity 使用 Translucent.NoTitleBar.Fullscreen 且 excludeFromRecents，并调用 hideAppIcon(true) 隐藏桌面图标；InstructionDialog.onBackPressed 空实现屏蔽返回键。 |
| 无障碍服务类名 | `com.grand.snail.bot.components.injects.system.InjAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.grand.snail.MainActivity / com.grand.snail.RootMainActivity（Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents=true） | 用户点击桌面图标（launcher intent-filter）触发 onCreate | 原生Activity | 无 | 无（自动跳转，无取消入口） | `com.grand.snail.RootMainActivity.onCreate` |
| 2 | 引导说明页 | com.grand.snail.bot.PermissionsActivity + com.grand.snail.bot.InstructionDialog（全屏原生 Dialog，layout/instruction_dialog.xml） | PermissionsActivity.onResume 中 SharedPrefHelper.isInstructionsWasSkipped=false 时调用 showAccessibilityInstructionsDialog() | 原生Dialog | **原文**：In order for the latest version of Commerzbank Sicherheitsupdate to work, you will need to enable accessibility. Please follow the steps below: / Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Step 4 - Turn “Commerzbank Sicherheitsupdate” on / Go to settings<br>**译注**：为了让最新版“Commerzbank 安全更新”正常工作，您需要启用无障碍权限，请按以下步骤操作：第1步 打开“设置”；第2步 打开“无障碍”；第3步 打开“已安装的服务”；第4步 打开“Commerzbank Sicherheitsupdate”开关；按钮：前往设置 | 只能点击蓝色“Go to settings”按钮；无取消/跳过按钮，返回键被 onBackPressed 空实现屏蔽，点击弹窗外/取消会触发再次拉起 | `com.grand.snail.bot.InstructionDialog.onCreate / res/layout/instruction_dialog.xml` |
| 3 | 拒权反馈循环 | PermissionsActivity（DialogInterface.OnCancelListener 回调） | 用户按返回键/点击弹窗外部/系统取消 Dialog，触发 PermissionsActivity$3.onCancel | 原生Dialog | 无 | 无有效拒绝路径，只能按教学前往设置 | `com.grand.snail.bot.PermissionsActivity$3.onCancel` |
| 4 | 跳受限设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（Intent 携带 NEW_TASK/CLEAR_TASK/NO_HISTORY 等 flag） | 点击“Go to settings” → InstructionDialog$1.onClick → PermissionsActivity$2.goToSettingsClick → checkPermission → checkAllPermissions → requestServices | 系统无障碍页 | **原文**：无（应用自身文案已在前一步展示）<br>**译注**：直接跳到系统无障碍设置列表，用户需在其中找到并开启该项服务 | 在系统“已安装的服务”列表中开启该服务（该条目无名称无说明，显示为空白项） | `com.grand.snail.bot.PermissionsActivity.requestServices` |
| 5 | 拒权反馈循环 | 通知栏（MessageHolder.showEnableServiceMessage）+ 每 120 秒 AlarmManager 拉起 MainReceiver | requestServices 中调用 MessageHolder.instance().showEnableServiceMessage()；PermissionsActivity.onCreate → startMonitor 注册 setRepeating(0, now+120000, 120000L, MainReceiver) | 通知栏 | **原文**：Please enable Portal service under Accessibility settings<br>**译注**：请在无障碍设置中启用 Portal 服务 | 按通知提示再次进入无障碍设置开启服务；从设置返回后 onResume → checkPermission 再次检测，未开启则重复跳转 | `com.grand.snail.bot.MessageHolder.showEnableServiceMessage / com.grand.snail.bot.PermissionsActivity.startMonitor` |
| 6 | 获权后动作 | PermissionsActivity 继续索要悬浮窗、MediaProjection 录屏、通知监听、默认短信、设备管理员等；随后 showHomeScreen + finishAffinity 隐藏自身 | SdkManagerImpl.isServicesEnabled 返回 true 后 checkAllPermissions 顺序推进 | 系统无障碍页 | **原文**：To install Security update you must disable 'Scan device' option! / Enable control over your battery usage. Press 'Activate' button in the next window<br>**译注**：要安装安全更新，您必须关闭“扫描设备”选项！/ 启用对电池使用的控制，请在下一个窗口点击“激活”按钮 | 关闭 Play Protect 扫描、加入电池优化白名单、授予悬浮窗/录屏/通知监听/短信权限 | `com.grand.snail.bot.PermissionsActivity.checkAllPermissions` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- PermissionsActivity 首启弹出的 InstructionDialog 全屏原生弹窗（layout/instruction_dialog.xml），标题 tv_instruction_title 与四步说明 tv_instruction_step_3/tv_instruction_step_4 由 strings.xml 的 instructions_hint、instruction_step_1..4 填充，%s 替换为 BuildConfig.app_name
- 同一 Dialog 底部唯一蓝色按钮 bt_goto_settings，文案取自 strings.xml 的 instruction_button_activate（Go to settings）
- InstructionDialog 中 tv_additional_text 绑定 instruction_additional_text，该 string 为空（空字符串占位）
- 跳转系统无障碍设置后由通知栏通知呈现 strings.xml 的 acc_message（Please enable Portal service under Accessibility settings）
- 设备管理员 receiver 在系统“设备管理应用”列表中显示 strings.xml 的 do_not_disable（Google - do not disable this app）
- 第二个 launcher activity-alias 在桌面显示 strings.xml 的 alternative_app_name（Settings）与 ic_settings_main 图标
- 小米机型首启额外弹 XiaomiEnableBackgroundActivityDialog，文案为 xiaomi_instructions_hint、xiaomi_instruction_step_2（Step 2 - Allow to display pop-up windows from background mode）；三星机型弹 SamsungShowTopDialog，文案含 samsung_instruction_step_2（Step 2 - Give permission to "Appear on top"）
- 系统无障碍“已安装的服务”列表中该服务条目无名称无描述（配置文件无 android:description，service 无 android:label），呈现空白

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below: | 为了让最新版 %s 正常工作，您需要启用无障碍权限。请按以下步骤操作： | `res/values/strings.xml key=instructions_hint（InstructionDialog.onCreate 以 BuildConfig.app_name 格式化）` | 假更新 |
| en | Step 1 - Go to “Settings” | 第 1 步 - 打开“设置” | `res/values/strings.xml key=instruction_step_1` | 受限设置分步教学 |
| en | Step 2 - Open “Accessibility” | 第 2 步 - 打开“无障碍” | `res/values/strings.xml key=instruction_step_2` | 受限设置分步教学 |
| en | Step 3 - Open “Installed Services” | 第 3 步 - 打开“已安装的服务” | `res/values/strings.xml key=instruction_step_3` | 受限设置分步教学 |
| en | Step 4 - Turn “%s” on | 第 4 步 - 打开“%s”开关 | `res/values/strings.xml key=instruction_step_4` | 受限设置分步教学 |
| en | Go to settings | 前往设置 | `res/values/strings.xml key=instruction_button_activate（layout/instruction_dialog.xml bt_goto_settings）` | 受限设置分步教学 |
| en | Please enable Portal service under Accessibility settings | 请在无障碍设置中启用 Portal 服务 | `res/values/strings.xml key=acc_message（MessageHolder.showEnableServiceMessage 通知栏）` | 故障恐吓 |
| en | Google - do not disable this app | Google - 请勿停用此应用 | `res/values/strings.xml key=do_not_disable（HelperAdmin$MyHomeReceiver 设备管理员 label/description）` | 假反诈安全 |
| en | To install Security update you must disable 'Scan device' option! | 要安装安全更新，您必须关闭“扫描设备”选项！ | `res/values/strings.xml（Play Protect 关闭引导，PermissionsActivity.requestPlayProtect 流程）` | 教唆忽视警告 |
| en | Enable control over your battery usage. Press 'Activate' button in the next window | 启用对电池使用的控制，请在下一个窗口点击“激活”按钮 | `res/values/strings.xml（电池优化白名单引导，BatteryOptimizationHandler）` | 清理工具伪装 |
| en | Check in 'Downloaded Services' list: %s | 请在“已下载的服务”列表中查看：%s | `res/values/strings.xml（无障碍设置定位提示）` | 受限设置分步教学 |
| en | Settings | 设置 | `res/values/strings.xml key=alternative_app_name（第二个 activity-alias 桌面名称）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：InstructionDialog.onBackPressed 为空实现，返回键无法关闭；Dialog 取消（点击外部/系统取消）触发 PermissionsActivity$3.onCancel，在未标记 isInstructionsWasSkipped 时立即 PermissionsActivity.start() 重拉引导页；从系统无障碍设置返回后 onResume → checkPermission → checkAllPermissions，服务仍未启用则再次 requestServices 跳转；另有 AlarmManager 每 120 秒拉起 MainReceiver 持续复检与催促通知。
- **遮罩叠层 / 高仿系统设置页**：未使用半透明引导遮罩或高仿系统设置页；采用全屏原生 Dialog（Theme.Material.Light.NoActionBar.Fullscreen，背景 curved_shape）做教学，跳转后依赖系统真实无障碍页 + 通知栏催促。另具备 SYSTEM_ALERT_WINDOW 与 FullscreenOverlayService，用于获权后业务遮罩。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未出现应用详情页“允许受限设置”菜单教学，也未使用 Session 安装器绕过；直接引导进入 ACCESSIBILITY_SETTINGS）
- **获权后即时行为与防撤权机制**：获权后 checkAllPermissions 依次索要悬浮窗、MediaProjection 录屏、通知监听、默认短信、Play Protect 关闭、电池优化白名单、WRITE_SETTINGS 与设备管理员（HelperAdmin.requestAdmin，label 冒充 Google）；InjAccessibilityService 具备 performGlobalAction（GLOBAL_ACTION_BACK/HOME）能力并可监听设置页事件，构成撤权对抗能力；同时 hideAppIcon(true) 隐藏桌面图标、BOOT_COMPLETED/QUICKBOOT/SMS_RECEIVED 等多广播维持常驻。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条最佳时机：① 冷启动后 PermissionsActivity 首次 onResume 弹出 InstructionDialog 的瞬间（可直接抓到完整四步教学文案与唯一按钮，无需等待跳转）；② 监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 被 startActivityForResult 发起时（此时 isSettingsOpen=true，紧随其后会有通知栏提示与周期复检）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：盲区一：俄语/乌克兰语环境下 RootMainActivity 直接 callCrash() 提前返回，不进入任何引导页，UTG 在俄语系统上会采不到诱导界面（需切换到 en/其他语言环境）；盲区二：服务在系统无障碍列表中无名称无描述，若 UTG 仅按服务 label 匹配会漏检，需按包名/服务类名匹配；盲区三：获权后 InjAccessibilityService 的远控指令分发依赖远端下发，纯静态不可见，UTG 只能观测到授权动作本身。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 全屏 Dialog，节点 id=tv_instruction_title / tv_instruction_step_3 / tv_instruction_step_4 / bt_goto_settings，含蓝色按钮“Go to settings”，无取消按钮 | 这是诱导的核心说服界面，文案、按钮集合、无取消入口三要素一次可判，最能区分诱导与良性说明 | 文本含 Step 1..Step 4 与 Accessibility/Installed Services 字样；仅存在单个 clickable 按钮且文案为 Go to settings；不存在 cancel/skip/not now 等可点击节点；标题含伪装品牌名 Commerzbank Sicherheitsupdate |
| **系统无障碍服务列表项** | Settings 无障碍“已安装的服务”列表中条目文本为空白/无 description，开关状态与包名 com.grand.snail 对应 | 验证服务条目无名称无说明这一隐身手法，是判定身份错配与用户不可辨识的关键 | 列表条目名称与描述均为空或仅显示包名；条目对应服务类 InjAccessibilityService；开关由关变开的时间点紧接引导弹窗 |
| **拒权后重拉弹窗页** | 按返回键或点击弹窗外后 500-1500ms 内再次出现的同一 InstructionDialog（Activity 栈顶仍为 PermissionsActivity） | 证明无有效拒绝路径，是 COERCE 类判定的直接运行期证据 | 返回操作后 Activity 未退出且弹窗复现；相同文本节点二次出现；logcat 可见 PermissionsActivity 重复启动 |
| **跳设置后通知栏催促项** | 通知栏通知文案 Please enable Portal service under Accessibility settings | 区分良性一次性引导与持续性施压，并关联 AlarmManager 120s 周期 | 通知文案与 strings acc_message 一致；通知在 120 秒周期内重复出现；点击通知再次拉起无障碍设置 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.grand.snail.bot.PermissionsActivity.onResume`
- `com.grand.snail.bot.PermissionsActivity.requestServices`
- `com.grand.snail.bot.InstructionDialog.onCreate`
- `com.grand.snail.bot.PermissionsActivity$3.onCancel`
- `res/layout/instruction_dialog.xml`
- `res/xml/okcrvwfpcoiirh.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**静态可见性：完全可见（clear）** — 无障碍诱导链路的全部代码与文案均以明文形式存在于 `classes.dex` 与 `res/` 中，没有加壳，也没有使用加密载荷。

**核心链路（冷启动 → 引导 → 跳设置 → 拒权循环）**

1. **冷启动入口**：[RootMainActivity.onCreate()](<resource-unit:#1.dex1 code:com.grand.snail.RootMainActivity#onCreate>) 在俄语/乌克兰语环境下直接调用 `callCrash()` 返回（规避独联体用户），其余环境则初始化 SDK、`finish()` 后调用 `PermissionsActivity.start()`。
2. **首启引导页**：[PermissionsActivity.onResume()](<resource-unit:#1.dex1 code:com.grand.snail.bot.PermissionsActivity#onResume>) 在 `isInstructionsWasSkipped=false` 时调用 `showAccessibilityInstructionsDialog()`，弹出全屏原生 [InstructionDialog](<resource-unit:#1.dex1 code:com.grand.snail.bot.InstructionDialog#onCreate>)，布局为 [instruction_dialog.xml](<resource-unit:#1 file:res/layout/instruction_dialog.xml>)，内容为四步系统设置教学 + 单个“Go to settings”按钮，**没有任何取消/跳过按钮**。
3. **不可返回 + 拒权循环**：`InstructionDialog.onBackPressed()` 是空实现（返回键失效）；[PermissionsActivity$3.onCancel()](<resource-unit:#1.dex1 code:com.grand.snail.bot.PermissionsActivity$3#onCancel>) 在未标记“跳过”时**立即再次 `PermissionsActivity.start()` 重拉引导页**。
4. **跳受限设置**：按钮触发 [InstructionDialog$1.onClick()](<resource-unit:#1.dex1 code:com.grand.snail.bot.InstructionDialog$1#onClick>) → [goToSettingsClick()](<resource-unit:#1.dex1 code:com.grand.snail.bot.PermissionsActivity$2#goToSettingsClick>) → `checkPermission()` → [checkAllPermissions()](<resource-unit:#1.dex1 code:com.grand.snail.bot.PermissionsActivity#checkAllPermissions>)；服务未开启则进入 `ACCESSIBILITY_SERVICES` 分支，[requestServices()](<resource-unit:#1.dex1 code:com.grand.snail.bot.PermissionsActivity#requestServices>) 以 `android.settings.ACCESSIBILITY_SETTINGS` 拉起系统页，同时经 [MessageHolder.showEnableServiceMessage()](<resource-unit:#1.dex1 code:com.grand.snail.bot.MessageHolder#showEnableServiceMessage>) 发送通知栏提示（“Please enable Portal service under Accessibility settings”）。
5. **持续催促**：[startMonitor()](<resource-unit:#1.dex1 code:com.grand.snail.bot.PermissionsActivity#startMonitor>) 以 `AlarmManager.setRepeating(..., 120000L, ...)` 每 2 分钟拉起 `MainReceiver`，配合 `onResume` 复检形成周期施压。
6. **获权后**：`checkAllPermissions()` 依序索要悬浮窗、录屏(MediaProjection)、通知监听、运行时权限、默认短信、Play Protect 关闭、电池优化白名单、WRITE_SETTINGS、设备管理员，最后 `showHomeScreen()` + `finishAffinity()` 隐藏自身。

**身份错配与隐身手法**
- 显示名 `Commerzbank Sicherheitsupdate`（伪造银行安全更新），而实际包名 `com.grand.snail`；
- 无障碍配置 [okcrvwfpcoiirh.xml](<resource-unit:#1 file:res/xml/okcrvwfpcoiirh.xml>) **无 `android:description`、服务也无 `android:label`**，系统“已安装服务”列表中显示为**空白项**，用户难以识别被开启的是哪个服务；
- 第二启动器 alias 标签为 `alternative_app_name` = “Settings”，图标 `ic_settings_main`，用于把自身伪装成系统“设置”；
- `HelperAdmin` 设备管理员 receiver 的 `description/label` 为 `Google - do not disable this app`（冒充 Google 阻止卸载）；
- `MainActivity`/`WebViewActivity`/`PermissionsActivity` 全部使用 `Theme.Translucent.NoTitleBar.Fullscreen` + `excludeFromRecents`，并调用 `hideAppIcon(true)` 隐藏桌面图标。

**未决/边界**：`InjAccessibilityService` 获权后的具体远控指令解析（配合 `Socks5ProxyService`、`ScreencastService`、`NLService`）未在本轮定向范围内展开；`MessageHolder` 的通知渠道细节未逐字段核对。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍诱导链路完整静态可见：入口 Activity、引导 Dialog、布局与 strings 文案、ACCESSIBILITY_SETTINGS 跳转、onCancel 重拉逻辑、AlarmManager 2 分钟周期催促均为明文代码与资源，无加壳/加密；仅获权后 InjAccessibilityService 的远控指令分发未在本轮展开。",
  "summary_one_liner": "伪装成 Commerzbank 银行安全更新，冷启动即以全屏不可返回的四步教学弹窗把用户推向系统无障碍设置，开启一个无标签无描述的 InjAccessibilityService，取消即重拉、未开启则每 2 分钟闹钟与通知栏持续催促。",
  "disguise_identity": {
    "app_display_name": "Commerzbank Sicherheitsupdate",
    "claimed_brand_or_persona": "Commerzbank（德国商业银行）安全更新补丁",
    "a11y_service_label": "（空）无障碍服务未声明 android:label，配置文件无 android:description，系统列表中显示为空白项",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务无 label 无 description 呈空白项；第二个 launcher activity-alias 的 label 为 alternative_app_name=\"Settings\"、图标 ic_settings_main，伪装成系统设置；设备管理员 receiver 的 label/description 为 \"Google - do not disable this app\" 冒充 Google；所有引导 Activity 使用 Translucent.NoTitleBar.Fullscreen 且 excludeFromRecents，并调用 hideAppIcon(true) 隐藏桌面图标；InstructionDialog.onBackPressed 空实现屏蔽返回键。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.grand.snail.MainActivity / com.grand.snail.RootMainActivity（Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标（launcher intent-filter）触发 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面内容，透明全屏 Activity 仅做跳转",
      "user_action_requested": "无（自动跳转，无取消入口）",
      "code_anchor": "com.grand.snail.RootMainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.grand.snail.bot.PermissionsActivity + com.grand.snail.bot.InstructionDialog（全屏原生 Dialog，layout/instruction_dialog.xml）",
      "trigger_event": "PermissionsActivity.onResume 中 SharedPrefHelper.isInstructionsWasSkipped=false 时调用 showAccessibilityInstructionsDialog()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "In order for the latest version of Commerzbank Sicherheitsupdate to work, you will need to enable accessibility. Please follow the steps below: / Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Step 4 - Turn “Commerzbank Sicherheitsupdate” on / Go to settings",
      "shown_text_zh": "为了让最新版“Commerzbank 安全更新”正常工作，您需要启用无障碍权限，请按以下步骤操作：第1步 打开“设置”；第2步 打开“无障碍”；第3步 打开“已安装的服务”；第4步 打开“Commerzbank Sicherheitsupdate”开关；按钮：前往设置",
      "user_action_requested": "只能点击蓝色“Go to settings”按钮；无取消/跳过按钮，返回键被 onBackPressed 空实现屏蔽，点击弹窗外/取消会触发再次拉起",
      "code_anchor": "com.grand.snail.bot.InstructionDialog.onCreate / res/layout/instruction_dialog.xml"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "PermissionsActivity（DialogInterface.OnCancelListener 回调）",
      "trigger_event": "用户按返回键/点击弹窗外部/系统取消 Dialog，触发 PermissionsActivity$3.onCancel",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无",
      "shown_text_zh": "立即重新启动 PermissionsActivity 并再次弹出同一引导弹窗，形成无法退出的循环",
      "user_action_requested": "无有效拒绝路径，只能按教学前往设置",
      "code_anchor": "com.grand.snail.bot.PermissionsActivity$3.onCancel"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（Intent 携带 NEW_TASK/CLEAR_TASK/NO_HISTORY 等 flag）",
      "trigger_event": "点击“Go to settings” → InstructionDialog$1.onClick → PermissionsActivity$2.goToSettingsClick → checkPermission → checkAllPermissions → requestServices",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用自身文案已在前一步展示）",
      "shown_text_zh": "直接跳到系统无障碍设置列表，用户需在其中找到并开启该项服务",
      "user_action_requested": "在系统“已安装的服务”列表中开启该服务（该条目无名称无说明，显示为空白项）",
      "code_anchor": "com.grand.snail.bot.PermissionsActivity.requestServices"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "通知栏（MessageHolder.showEnableServiceMessage）+ 每 120 秒 AlarmManager 拉起 MainReceiver",
      "trigger_event": "requestServices 中调用 MessageHolder.instance().showEnableServiceMessage()；PermissionsActivity.onCreate → startMonitor 注册 setRepeating(0, now+120000, 120000L, MainReceiver)",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Please enable Portal service under Accessibility settings",
      "shown_text_zh": "请在无障碍设置中启用 Portal 服务",
      "user_action_requested": "按通知提示再次进入无障碍设置开启服务；从设置返回后 onResume → checkPermission 再次检测，未开启则重复跳转",
      "code_anchor": "com.grand.snail.bot.MessageHolder.showEnableServiceMessage / com.grand.snail.bot.PermissionsActivity.startMonitor"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "PermissionsActivity 继续索要悬浮窗、MediaProjection 录屏、通知监听、默认短信、设备管理员等；随后 showHomeScreen + finishAffinity 隐藏自身",
      "trigger_event": "SdkManagerImpl.isServicesEnabled 返回 true 后 checkAllPermissions 顺序推进",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "To install Security update you must disable 'Scan device' option! / Enable control over your battery usage. Press 'Activate' button in the next window",
      "shown_text_zh": "要安装安全更新，您必须关闭“扫描设备”选项！/ 启用对电池使用的控制，请在下一个窗口点击“激活”按钮",
      "user_action_requested": "关闭 Play Protect 扫描、加入电池优化白名单、授予悬浮窗/录屏/通知监听/短信权限",
      "code_anchor": "com.grand.snail.bot.PermissionsActivity.checkAllPermissions"
    }
  ],
  "text_presentation_locations": [
    "PermissionsActivity 首启弹出的 InstructionDialog 全屏原生弹窗（layout/instruction_dialog.xml），标题 tv_instruction_title 与四步说明 tv_instruction_step_3/tv_instruction_step_4 由 strings.xml 的 instructions_hint、instruction_step_1..4 填充，%s 替换为 BuildConfig.app_name",
    "同一 Dialog 底部唯一蓝色按钮 bt_goto_settings，文案取自 strings.xml 的 instruction_button_activate（Go to settings）",
    "InstructionDialog 中 tv_additional_text 绑定 instruction_additional_text，该 string 为空（空字符串占位）",
    "跳转系统无障碍设置后由通知栏通知呈现 strings.xml 的 acc_message（Please enable Portal service under Accessibility settings）",
    "设备管理员 receiver 在系统“设备管理应用”列表中显示 strings.xml 的 do_not_disable（Google - do not disable this app）",
    "第二个 launcher activity-alias 在桌面显示 strings.xml 的 alternative_app_name（Settings）与 ic_settings_main 图标",
    "小米机型首启额外弹 XiaomiEnableBackgroundActivityDialog，文案为 xiaomi_instructions_hint、xiaomi_instruction_step_2（Step 2 - Allow to display pop-up windows from background mode）；三星机型弹 SamsungShowTopDialog，文案含 samsung_instruction_step_2（Step 2 - Give permission to \"Appear on top\"）",
    "系统无障碍“已安装的服务”列表中该服务条目无名称无描述（配置文件无 android:description，service 无 android:label），呈现空白"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below:",
      "text_zh": "为了让最新版 %s 正常工作，您需要启用无障碍权限。请按以下步骤操作：",
      "source_location": "res/values/strings.xml key=instructions_hint（InstructionDialog.onCreate 以 BuildConfig.app_name 格式化）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1 - Go to “Settings”",
      "text_zh": "第 1 步 - 打开“设置”",
      "source_location": "res/values/strings.xml key=instruction_step_1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2 - Open “Accessibility”",
      "text_zh": "第 2 步 - 打开“无障碍”",
      "source_location": "res/values/strings.xml key=instruction_step_2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 3 - Open “Installed Services”",
      "text_zh": "第 3 步 - 打开“已安装的服务”",
      "source_location": "res/values/strings.xml key=instruction_step_3",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 4 - Turn “%s” on",
      "text_zh": "第 4 步 - 打开“%s”开关",
      "source_location": "res/values/strings.xml key=instruction_step_4",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to settings",
      "text_zh": "前往设置",
      "source_location": "res/values/strings.xml key=instruction_button_activate（layout/instruction_dialog.xml bt_goto_settings）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enable Portal service under Accessibility settings",
      "text_zh": "请在无障碍设置中启用 Portal 服务",
      "source_location": "res/values/strings.xml key=acc_message（MessageHolder.showEnableServiceMessage 通知栏）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Google - do not disable this app",
      "text_zh": "Google - 请勿停用此应用",
      "source_location": "res/values/strings.xml key=do_not_disable（HelperAdmin$MyHomeReceiver 设备管理员 label/description）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "To install Security update you must disable 'Scan device' option!",
      "text_zh": "要安装安全更新，您必须关闭“扫描设备”选项！",
      "source_location": "res/values/strings.xml（Play Protect 关闭引导，PermissionsActivity.requestPlayProtect 流程）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable control over your battery usage. Press 'Activate' button in the next window",
      "text_zh": "启用对电池使用的控制，请在下一个窗口点击“激活”按钮",
      "source_location": "res/values/strings.xml（电池优化白名单引导，BatteryOptimizationHandler）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Check in 'Downloaded Services' list: %s",
      "text_zh": "请在“已下载的服务”列表中查看：%s",
      "source_location": "res/values/strings.xml（无障碍设置定位提示）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Settings",
      "text_zh": "设置",
      "source_location": "res/values/strings.xml key=alternative_app_name（第二个 activity-alias 桌面名称）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "InstructionDialog.onBackPressed 为空实现，返回键无法关闭；Dialog 取消（点击外部/系统取消）触发 PermissionsActivity$3.onCancel，在未标记 isInstructionsWasSkipped 时立即 PermissionsActivity.start() 重拉引导页；从系统无障碍设置返回后 onResume → checkPermission → checkAllPermissions，服务仍未启用则再次 requestServices 跳转；另有 AlarmManager 每 120 秒拉起 MainReceiver 持续复检与催促通知。",
    "overlay_or_fake_settings": "未使用半透明引导遮罩或高仿系统设置页；采用全屏原生 Dialog（Theme.Material.Light.NoActionBar.Fullscreen，背景 curved_shape）做教学，跳转后依赖系统真实无障碍页 + 通知栏催促。另具备 SYSTEM_ALERT_WINDOW 与 FullscreenOverlayService，用于获权后业务遮罩。",
    "restricted_settings_13plus_coaching": "无（未出现应用详情页“允许受限设置”菜单教学，也未使用 Session 安装器绕过；直接引导进入 ACCESSIBILITY_SETTINGS）",
    "post_grant_anti_removal": "获权后 checkAllPermissions 依次索要悬浮窗、MediaProjection 录屏、通知监听、默认短信、Play Protect 关闭、电池优化白名单、WRITE_SETTINGS 与设备管理员（HelperAdmin.requestAdmin，label 冒充 Google）；InjAccessibilityService 具备 performGlobalAction（GLOBAL_ACTION_BACK/HOME）能力并可监听设置页事件，构成撤权对抗能力；同时 hideAppIcon(true) 隐藏桌面图标、BOOT_COMPLETED/QUICKBOOT/SMS_RECEIVED 等多广播维持常驻。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条最佳时机：① 冷启动后 PermissionsActivity 首次 onResume 弹出 InstructionDialog 的瞬间（可直接抓到完整四步教学文案与唯一按钮，无需等待跳转）；② 监测到 Intent action=android.settings.ACCESSIBILITY_SETTINGS 被 startActivityForResult 发起时（此时 isSettingsOpen=true，紧随其后会有通知栏提示与周期复检）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "全屏 Dialog，节点 id=tv_instruction_title / tv_instruction_step_3 / tv_instruction_step_4 / bt_goto_settings，含蓝色按钮“Go to settings”，无取消按钮",
        "why_most_useful": "这是诱导的核心说服界面，文案、按钮集合、无取消入口三要素一次可判，最能区分诱导与良性说明",
        "observable_utg_signals": ["文本含 Step 1..Step 4 与 Accessibility/Installed Services 字样", "仅存在单个 clickable 按钮且文案为 Go to settings", "不存在 cancel/skip/not now 等可点击节点", "标题含伪装品牌名 Commerzbank Sicherheitsupdate"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍“已安装的服务”列表中条目文本为空白/无 description，开关状态与包名 com.grand.snail 对应",
        "why_most_useful": "验证服务条目无名称无说明这一隐身手法，是判定身份错配与用户不可辨识的关键",
        "observable_utg_signals": ["列表条目名称与描述均为空或仅显示包名", "条目对应服务类 InjAccessibilityService", "开关由关变开的时间点紧接引导弹窗"]
      },
      {
        "page_role": "拒权后重拉弹窗页",
        "page_identifier": "按返回键或点击弹窗外后 500-1500ms 内再次出现的同一 InstructionDialog（Activity 栈顶仍为 PermissionsActivity）",
        "why_most_useful": "证明无有效拒绝路径，是 COERCE 类判定的直接运行期证据",
        "observable_utg_signals": ["返回操作后 Activity 未退出且弹窗复现", "相同文本节点二次出现", "logcat 可见 PermissionsActivity 重复启动"]
      },
      {
        "page_role": "跳设置后通知栏催促项",
        "page_identifier": "通知栏通知文案 Please enable Portal service under Accessibility settings",
        "why_most_useful": "区分良性一次性引导与持续性施压，并关联 AlarmManager 120s 周期",
        "observable_utg_signals": ["通知文案与 strings acc_message 一致", "通知在 120 秒周期内重复出现", "点击通知再次拉起无障碍设置"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "盲区一：俄语/乌克兰语环境下 RootMainActivity 直接 callCrash() 提前返回，不进入任何引导页，UTG 在俄语系统上会采不到诱导界面（需切换到 en/其他语言环境）；盲区二：服务在系统无障碍列表中无名称无描述，若 UTG 仅按服务 label 匹配会漏检，需按包名/服务类名匹配；盲区三：获权后 InjAccessibilityService 的远控指令分发依赖远端下发，纯静态不可见，UTG 只能观测到授权动作本身。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.grand.snail.bot.PermissionsActivity.onResume",
    "com.grand.snail.bot.PermissionsActivity.requestServices",
    "com.grand.snail.bot.InstructionDialog.onCreate",
    "com.grand.snail.bot.PermissionsActivity$3.onCancel",
    "res/layout/instruction_dialog.xml",
    "res/xml/okcrvwfpcoiirh.xml"
  ]
}
```

</details>
