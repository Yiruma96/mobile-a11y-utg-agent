# MB_057__cd3ff09b50｜Hydra — Commerzbank Security

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：106.0s

## 1. 一句话核心结论

- **核心申请方式**：以“Commerzbank Security/Portal service”名义，用中文式分步教学文案（Step1-4 + Go to settings）把用户导流到系统无障碍列表手动开启无描述、可读取窗口内容与手势注入的无障碍服务，并配合悬浮窗叠层与“Settings”别名做伪装。
- **静态可见性说明**：Manifest 声明、无障碍配置 XML 与全部引导文案（strings.xml）静态完整可见；但承载引导弹窗、跳转 ACCESSIBILITY_SETTINGS、拒权循环与遮罩叠加的实现类 com.grand.snail.*（MainActivity/PermissionsActivity/InjAccessibilityService/FullscreenOverlayService）在 classes.dex 中完全缺失，仅有 com.camp.make 混淆壳类，assets/na.czl 为非 DEX 非 ELF 的加密/私有格式载荷，二阶段代码需运行期解密或远端下发才能观察。
- **命中的行为模式标签**：`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `cd3ff09b5070985a0797738743b1c62233918666b888dc4867cec9aa82cc5505` |
| 包名 / 年份 | `com.camp.make` / 2023 |
| 家族 / 品类 | **Hydra**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Commerzbank Security |
| 引导页宣称品牌/身份 | Commerzbank Security（德国商业银行安全组件）+ 无障碍服务自称 Portal service，另有 GoogleReader / Google 防禁用 / 系统 Settings 多重人格 |
| 系统无障碍列表服务名 | 无独立 android:label，回落为应用名 Commerzbank Security（android:description 为空，系统列表无任何说明文字） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：多 activity-alias：MainActivity2 别名 label=@string/alternative_app_name("Settings")、icon=@drawable/ic_settings_main 且 enabled=false 可远程启用伪装系统设置；application label 硬编码为 Commerzbank Security 而资源 app_name=GoogleReader；无障碍服务无 description、无 settingsActivity，规避系统风险提示；宿主包名 com.camp.make 与代码命名空间 com.grand.snail 不一致，类名全随机字符串混淆；device-admin 描述 "Google - do not disable this app" 冒充 Google 组件；LockerActivity 注册 HOME 类别且 label=Settings 可顶替桌面 |
| 无障碍服务类名 | `com.grand.snail.bot.components.injects.system.InjAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.grand.snail.MainActivity（LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents=true，另有同名 activity-alias 双入口） | onCreate（图标点击，含 HOME 键返回后再次进入） | 不可静态还原 | 无 | 无（无任何界面元素，无法取消） | `AndroidManifest.xml: com.grand.snail.MainActivity / activity-alias` |
| 2 | 引导说明页 | com.grand.snail.bot.PermissionsActivity（Translucent.NoTitleBar.Fullscreen，excludeFromRecents=true，无 launcher 入口，由载荷内部拉起） | 载荷判定无障碍未开启后 startActivity（具体触发方法不可静态还原） | 原生Dialog | **原文**：In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below: / Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Step 4 - Turn “%s” on / Go to settings<br>**译注**：为了让最新版 %s 正常工作，你需要开启无障碍。请按以下步骤操作：第1步 打开“设置”／第2步 打开“无障碍”／第3步 打开“已安装的服务”／第4步 打开“%s”；按钮：前往设置 | 只能点击“Go to settings”，文案中未提供取消/跳过/稍后按钮 | `res/values/strings.xml: instructions_hint / instruction_step_1..4 / instruction_button_activate；承载类 com.grand.snail.bot.PermissionsActivity（代码缺失）` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（由 PermissionsActivity 点击后跳转；classes.dex 中无该 action 常量，属缺失载荷内调用） | 点击“Go to settings”按钮 | 系统无障碍页 | **原文**：Please enable Portal service under Accessibility settings / Check in 'Downloaded Services' list: %s<br>**译注**：请在无障碍设置中开启 Portal 服务／在“已下载的服务”列表中查看：%s | 在系统“已安装/已下载的服务”列表中找到该服务并手动开启开关 | `res/values/strings.xml: acc_message / check_in_services_message；InjAccessibilityService 声明（AndroidManifest.xml）` |
| 4 | 遮罩叠层指引 | com.grand.snail.bot.components.injects.system.FullscreenOverlayService（SYSTEM_ALERT_WINDOW）+ 厂商特化步骤提示 | 跳转设置后由悬浮窗服务覆盖屏幕引导（触发条件不可静态还原） | 悬浮窗Overlay | **原文**：Step 2 - Allow to display pop-up windows from background mode / Allow pop-up windows for the correct application work: / Step 2 - Give permission to "Appear on top" / Enable control over your battery usage. Press 'Activate' button in the next window<br>**译注**：第2步 允许后台弹出界面／允许弹窗以便应用正常工作／第2步 授予“显示在其他应用上层”权限／开启电池使用控制，在下一窗口点击“激活” | 继续在系统页面授予悬浮窗、后台弹窗、忽略电池优化等权限 | `res/values/strings.xml: xiaomi_instruction_step_2 / xiaomi_instructions_hint / samsung_instruction_step_2 / enable_control_battery_usage；AndroidManifest.xml: FullscreenOverlayService` |
| 5 | 拒权反馈循环 | 不可静态还原（com.grand.snail.* 实现缺失，无 onResume/定时器代码可读） | 用户按返回或未开启开关回到应用 | 不可静态还原 | **原文**：Attention! Without permission app may not work properly / Error<br>**译注**：注意！没有该权限应用可能无法正常工作／错误 | 不可静态确认是否有取消或循环重跳 | `res/values/strings.xml: permissions_dialog_title / permissions_dialog_message / dialogErrorTitle` |
| 6 | 获权后动作 | InjAccessibilityService（injects.system，canRetrieveWindowContent + canPerformGestures + 按键过滤）+ LockerActivity（HOME 类别，label=Settings）+ NLService（通知监听） | onServiceConnected（无障碍开关打开后由系统绑定） | 不可静态还原 | 无 | 无 | `res/xml/uzafwzhqblmhdr.xml；AndroidManifest.xml: InjAccessibilityService / LockerActivity / NLService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- PermissionsActivity（全屏透明 Dialog 页面，由载荷内部拉起，无 launcher 入口）中的分步教学：instructions_hint + instruction_step_1..4 + 唯一按钮 instruction_button_activate("Go to settings")
- 引导页/提示中的单句指令：acc_message（Please enable Portal service under Accessibility settings）、check_in_services_message（Check in 'Downloaded Services' list: %s）
- 厂商特化提示：xiaomi_instructions_hint / xiaomi_instruction_step_2 / samsung_instruction_step_2（引导授予后台弹窗与“显示在顶层”）
- 系统无障碍服务列表条目：InjAccessibilityService 无 android:description，列表中仅显示应用名 Commerzbank Security，无任何用途说明
- 跳转设置后的悬浮窗引导：FullscreenOverlayService（SYSTEM_ALERT_WINDOW）叠层覆盖系统设置页（能力已声明，触发代码不可静态还原）
- 权限缺失提示：permissions_dialog_title/message（Attention! ... may not work properly）
- 教唆关闭系统防护的提示：enablePlayProtect_message + services_playProtect / services_playScanningDisableBtn（turn off）
- 设备管理器说明与标签：do_not_disable = "Google - do not disable this app"（receiver label/description）
- 伪装系统设置的桌面入口：activity-alias(MainActivity2) label="Settings"、icon=ic_settings_main

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below: | 为了让最新版 %s 正常工作，你需要开启无障碍权限。请按以下步骤操作： | `res/values/strings.xml: instructions_hint` | 假更新 |
| en | Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Step 4 - Turn “%s” on / Go to settings | 第1步 打开“设置”／第2步 打开“无障碍”／第3步 打开“已安装的服务”／第4步 打开“%s”／按钮：前往设置 | `res/values/strings.xml: instruction_step_1..4 / instruction_button_activate` | 受限设置分步教学 |
| en | Please enable Portal service under Accessibility settings | 请在无障碍设置中开启 Portal 服务 | `res/values/strings.xml: acc_message` | 假更新 |
| en | Check in 'Downloaded Services' list: %s | 请在“已下载的服务”列表中查看：%s | `res/values/strings.xml: check_in_services_message` | 受限设置分步教学 |
| en | To install Security update you must disable 'Scan device' option! | 要安装安全更新，你必须关闭“扫描设备”选项！ | `res/values/strings.xml: enablePlayProtect_message` | 教唆忽视警告 |
| en | Google - do not disable this app | Google——请勿禁用此应用 | `res/values/strings.xml: do_not_disable（device admin receiver label/description）` | 假反诈安全 |
| en | Attention! Without permission app may not work properly | 注意！没有该权限，应用可能无法正常工作 | `res/values/strings.xml: permissions_dialog_message` | 故障恐吓 |
| en | Enable control over your battery usage. Press 'Activate' button in the next window | 开启电池使用控制，请在下一窗口点击“激活”按钮 | `res/values/strings.xml: enable_control_battery_usage` | 受限设置分步教学 |
| en | Allow pop-up windows for the correct application work: | 请允许弹出窗口，以保证应用正常工作： | `res/values/strings.xml: xiaomi_instructions_hint` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：拒权后的 onResume 重跳/定时器逻辑位于 com.grand.snail.* 实现中，而该类未出现在 classes.dex，仅能确认存在“权限缺失”恐吓弹窗文案（Attention! ... may not work properly）与错误提示；无良性降级文案。
- **遮罩叠层 / 高仿系统设置页**：声明 FullscreenOverlayService（SYSTEM_ALERT_WINDOW）具备叠层能力，并有“允许后台弹窗/显示在顶层”的前置引导文案；另有 label="Settings"、icon=ic_settings_main 的 activity-alias 与 HOME 类别 LockerActivity，可伪装系统设置/桌面，但具体叠层与伪造页面的绘制代码不可静态还原。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（仅教学进入“设置→无障碍→已安装的服务”，未见进入应用详情右上角菜单允许受限设置的文案或 ACTION_APPLICATION_DETAILS_SETTINGS 调用点）
- **获权后即时行为与防撤权机制**：不可静态还原：未见 GLOBAL_ACTION_BACK/HOME 阻止撤权代码（载荷缺失）；但已声明 device-admin receiver（标签 Google - do not disable this app）与 LockerActivity(HOME)、PeriodicJobReceiver（BOOT_COMPLETED/SCREEN_ON/USER_PRESENT 等）具备持续驻留与防移除能力基础
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到前台 Activity 切换到 com.grand.snail.bot.PermissionsActivity，或系统设置包 com.android.settings 的无障碍/已安装服务页被拉起（伴随本应用 overlay 窗口出现）时立即抓取全屏
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：一阶段壳（com.camp.make 混淆类）+ 二阶段载荷缺失。classes.dex 中不存在 com.grand.snail.* 任何实现类，android.settings.ACCESSIBILITY_SETTINGS 无静态调用点，assets/na.czl（头部 00 01 01 00）为私有/加密格式、assets/nd 为 ELF，故跳转与循环的具体代码无法静态定位；纯图/空文本遮罩与远端 HTML 下发的引导页需依赖运行期 UTG 才能取证。另存在 label="Settings" 别名与 LockerActivity(HOME) 的伪装入口，若远程切换启用，桌面图标与名称会与本次静态快照不一致。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/引导说明弹窗页** | com.grand.snail.bot.PermissionsActivity，透明全屏，含 instructions_hint 与单一“Go to settings”按钮 | 这是唯一静态可证实的“教学入口”，可判定是否存在取消/跳过按钮、是否为假更新话术、是否不可取消 | 控件文本包含 Step 1 - Go to “Settings”；仅存在一个可点击按钮 Go to settings；无取消/跳过/稍后节点；Activity 名 PermissionsActivity 且窗口透明全屏 |
| **系统无障碍服务列表项** | com.android.settings 的 Installed/Downloaded services 列表中的 Commerzbank Security 条目 | 直接验证服务无 description、以银行名展示、被引导用户点开的开关位置，是诱导链条的关键落点 | 条目文本 Commerzbank Security 且无副标题说明；与 acc_message 中 Portal service 措辞不一致；页面处于 com.android.settings 包 |
| **跳设置后压栈遮罩/引导层** | FullscreenOverlayService 创建的系统级窗口（TYPE_APPLICATION_OVERLAY）覆盖在设置页之上 | 判定是否用悬浮窗在设置页上叠加指引或伪造开关，是区分善意教学与遮罩诱导的核心 | 窗口层级包含应用包名 com.camp.make 的 overlay；遮罩文本含 Step 4 - Turn “%s” on；设置页控件被遮挡或出现高亮圈选 |
| **拒权返回后的反馈页** | 返回应用后再次出现的 PermissionsActivity 或 Attention! 弹窗 | 验证是否存在拒权死循环重跳与恐吓话术，判定强制性与骚扰强度 | 返回后 X 秒内重复出现同一 Activity；出现 Attention! Without permission app may not work properly；开关未开启时无任何可用功能界面 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `res/values/strings.xml#L3-L22（acc_message / check_in_services_message / instruction_step_1..4 / instructions_hint / instruction_button_activate）`
- `res/xml/uzafwzhqblmhdr.xml（无障碍配置：canRetrieveWindowContent / canPerformGestures / flagRequestFilterKeyEvents，android:description 为空）`
- `AndroidManifest.xml: service com.grand.snail.bot.components.injects.system.InjAccessibilityService`
- `AndroidManifest.xml: activity com.grand.snail.bot.PermissionsActivity / service com.grand.snail.bot.components.injects.system.FullscreenOverlayService`
- `AndroidManifest.xml: activity-alias com.grand.snail.MainActivity2（label=@string/alternative_app_name=Settings, icon=@drawable/ic_settings_main, enabled=false）`
- `com.grand.snail.bot.components.injects.system.InjAccessibilityService（类实现未包含于 classes.dex，二阶段载荷缺失）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，纯运行期 UTG 视角）

**静态可见性：部分可见（引导文案与声明齐全，执行代码不在 classes.dex）**

- 已确认的引导体系：`res/values/strings.xml` 提供完整的分步教学文案（Step 1–4、`Go to settings`、`Please enable Portal service under Accessibility settings`、`Check in 'Downloaded Services' list`），以及小米、三星的厂商特化步骤（允许后台弹窗、允许“Appear on top”）；对应 `[strings.xml (L3-L22)](<resource-unit:#1 file:res/values/strings.xml#L3-L22>)`。
- 无障碍声明：`[InjAccessibilityService](<resource-unit:#1 manifest:components>)` 绑定 `BIND_ACCESSIBILITY_SERVICE`，其配置 `[uzafwzhqblmhdr.xml](<resource-unit:#1 file:res/xml/uzafwzhqblmhdr.xml>)` 开启 `canRetrieveWindowContent`、`canPerformGestures`、`canRequestFilterKeyEvents`、`flagRequestFilterKeyEvents`、`typeWindowContentChanged`，但 `android:description` 与 `android:settingsActivity` 均为空，系统无障碍列表**不会显示任何风险说明**，条目名回落为应用名 `Commerzbank Security`。
- 关键缺口：`com.grand.snail.*`（MainActivity / PermissionsActivity / InjAccessibilityService / FullscreenOverlayService 的实际实现）在 `classes.dex` 中**不存在**；`list_codebase` 仅含 `com.camp.*` 混淆类与三方 SDK，`search_function_definitions` 对 `snail`/`Portal`/`Accessibility` 全部无命中，`android.settings.ACCESSIBILITY_SETTINGS` 亦无调用点。即“谁弹窗、谁跳设置、谁循环”的代码属于未落地的二阶段载荷（`assets/na.czl` 头部 `00 01 01 00`，非 DEX/非 ELF；`assets/nd` 为 ELF），无法静态还原其具体 UTG 流转。
- 身份伪装已可静态确认：应用 label 硬编码 `Commerzbank Security`，资源 `app_name=GoogleReader`；`MainActivity2` 的 activity-alias 标签为 `Settings`、图标 `ic_settings_main`（默认 `enabled=false`，可远程开启）——用“系统设置”外观做第二入口；device-admin 描述 `Google - do not disable this app`；字符串包含 `To install Security update you must disable 'Scan device' option!` 及 `turn off / Scan device for / protection?` 等**教唆关闭 Play Protect** 的话术。
- 拒绝授权后的循环、是否压栈遮罩、是否伪造 `isAccessibilityTool`：静态不可判定（逻辑在缺失载荷内），仅能确认 `FullscreenOverlayService` 与 `SYSTEM_ALERT_WINDOW` 具备叠层能力。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest 声明、无障碍配置 XML 与全部引导文案（strings.xml）静态完整可见；但承载引导弹窗、跳转 ACCESSIBILITY_SETTINGS、拒权循环与遮罩叠加的实现类 com.grand.snail.*（MainActivity/PermissionsActivity/InjAccessibilityService/FullscreenOverlayService）在 classes.dex 中完全缺失，仅有 com.camp.make 混淆壳类，assets/na.czl 为非 DEX 非 ELF 的加密/私有格式载荷，二阶段代码需运行期解密或远端下发才能观察。",
  "summary_one_liner": "以“Commerzbank Security/Portal service”名义，用中文式分步教学文案（Step1-4 + Go to settings）把用户导流到系统无障碍列表手动开启无描述、可读取窗口内容与手势注入的无障碍服务，并配合悬浮窗叠层与“Settings”别名做伪装。",
  "disguise_identity": {
    "app_display_name": "Commerzbank Security",
    "claimed_brand_or_persona": "Commerzbank Security（德国商业银行安全组件）+ 无障碍服务自称 Portal service，另有 GoogleReader / Google 防禁用 / 系统 Settings 多重人格",
    "a11y_service_label": "无独立 android:label，回落为应用名 Commerzbank Security（android:description 为空，系统列表无任何说明文字）",
    "identity_mismatch": true,
    "obfuscation_tricks": "多 activity-alias：MainActivity2 别名 label=@string/alternative_app_name(\"Settings\")、icon=@drawable/ic_settings_main 且 enabled=false 可远程启用伪装系统设置；application label 硬编码为 Commerzbank Security 而资源 app_name=GoogleReader；无障碍服务无 description、无 settingsActivity，规避系统风险提示；宿主包名 com.camp.make 与代码命名空间 com.grand.snail 不一致，类名全随机字符串混淆；device-admin 描述 \"Google - do not disable this app\" 冒充 Google 组件；LockerActivity 注册 HOME 类别且 label=Settings 可顶替桌面"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.grand.snail.MainActivity（LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents=true，另有同名 activity-alias 双入口）",
      "trigger_event": "onCreate（图标点击，含 HOME 键返回后再次进入）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "全屏透明无标题栏，无可见界面，仅作为载荷启动点",
      "user_action_requested": "无（无任何界面元素，无法取消）",
      "code_anchor": "AndroidManifest.xml: com.grand.snail.MainActivity / activity-alias"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.grand.snail.bot.PermissionsActivity（Translucent.NoTitleBar.Fullscreen，excludeFromRecents=true，无 launcher 入口，由载荷内部拉起）",
      "trigger_event": "载荷判定无障碍未开启后 startActivity（具体触发方法不可静态还原）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below: / Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Step 4 - Turn “%s” on / Go to settings",
      "shown_text_zh": "为了让最新版 %s 正常工作，你需要开启无障碍。请按以下步骤操作：第1步 打开“设置”／第2步 打开“无障碍”／第3步 打开“已安装的服务”／第4步 打开“%s”；按钮：前往设置",
      "user_action_requested": "只能点击“Go to settings”，文案中未提供取消/跳过/稍后按钮",
      "code_anchor": "res/values/strings.xml: instructions_hint / instruction_step_1..4 / instruction_button_activate；承载类 com.grand.snail.bot.PermissionsActivity（代码缺失）"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（由 PermissionsActivity 点击后跳转；classes.dex 中无该 action 常量，属缺失载荷内调用）",
      "trigger_event": "点击“Go to settings”按钮",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Please enable Portal service under Accessibility settings / Check in 'Downloaded Services' list: %s",
      "shown_text_zh": "请在无障碍设置中开启 Portal 服务／在“已下载的服务”列表中查看：%s",
      "user_action_requested": "在系统“已安装/已下载的服务”列表中找到该服务并手动开启开关",
      "code_anchor": "res/values/strings.xml: acc_message / check_in_services_message；InjAccessibilityService 声明（AndroidManifest.xml）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.grand.snail.bot.components.injects.system.FullscreenOverlayService（SYSTEM_ALERT_WINDOW）+ 厂商特化步骤提示",
      "trigger_event": "跳转设置后由悬浮窗服务覆盖屏幕引导（触发条件不可静态还原）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Step 2 - Allow to display pop-up windows from background mode / Allow pop-up windows for the correct application work: / Step 2 - Give permission to \"Appear on top\" / Enable control over your battery usage. Press 'Activate' button in the next window",
      "shown_text_zh": "第2步 允许后台弹出界面／允许弹窗以便应用正常工作／第2步 授予“显示在其他应用上层”权限／开启电池使用控制，在下一窗口点击“激活”",
      "user_action_requested": "继续在系统页面授予悬浮窗、后台弹窗、忽略电池优化等权限",
      "code_anchor": "res/values/strings.xml: xiaomi_instruction_step_2 / xiaomi_instructions_hint / samsung_instruction_step_2 / enable_control_battery_usage；AndroidManifest.xml: FullscreenOverlayService"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "不可静态还原（com.grand.snail.* 实现缺失，无 onResume/定时器代码可读）",
      "trigger_event": "用户按返回或未开启开关回到应用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Attention! Without permission app may not work properly / Error",
      "shown_text_zh": "注意！没有该权限应用可能无法正常工作／错误",
      "user_action_requested": "不可静态确认是否有取消或循环重跳",
      "code_anchor": "res/values/strings.xml: permissions_dialog_title / permissions_dialog_message / dialogErrorTitle"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "InjAccessibilityService（injects.system，canRetrieveWindowContent + canPerformGestures + 按键过滤）+ LockerActivity（HOME 类别，label=Settings）+ NLService（通知监听）",
      "trigger_event": "onServiceConnected（无障碍开关打开后由系统绑定）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "读取窗口内容、注入手势与按键，配合通知监听与桌面顶替能力；具体注入目标（银行/短信/支付界面）代码不在包内可读 DEX 中",
      "user_action_requested": "无",
      "code_anchor": "res/xml/uzafwzhqblmhdr.xml；AndroidManifest.xml: InjAccessibilityService / LockerActivity / NLService"
    }
  ],
  "text_presentation_locations": [
    "PermissionsActivity（全屏透明 Dialog 页面，由载荷内部拉起，无 launcher 入口）中的分步教学：instructions_hint + instruction_step_1..4 + 唯一按钮 instruction_button_activate(\"Go to settings\")",
    "引导页/提示中的单句指令：acc_message（Please enable Portal service under Accessibility settings）、check_in_services_message（Check in 'Downloaded Services' list: %s）",
    "厂商特化提示：xiaomi_instructions_hint / xiaomi_instruction_step_2 / samsung_instruction_step_2（引导授予后台弹窗与“显示在顶层”）",
    "系统无障碍服务列表条目：InjAccessibilityService 无 android:description，列表中仅显示应用名 Commerzbank Security，无任何用途说明",
    "跳转设置后的悬浮窗引导：FullscreenOverlayService（SYSTEM_ALERT_WINDOW）叠层覆盖系统设置页（能力已声明，触发代码不可静态还原）",
    "权限缺失提示：permissions_dialog_title/message（Attention! ... may not work properly）",
    "教唆关闭系统防护的提示：enablePlayProtect_message + services_playProtect / services_playScanningDisableBtn（turn off）",
    "设备管理器说明与标签：do_not_disable = \"Google - do not disable this app\"（receiver label/description）",
    "伪装系统设置的桌面入口：activity-alias(MainActivity2) label=\"Settings\"、icon=ic_settings_main"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below:",
      "text_zh": "为了让最新版 %s 正常工作，你需要开启无障碍权限。请按以下步骤操作：",
      "source_location": "res/values/strings.xml: instructions_hint",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Step 4 - Turn “%s” on / Go to settings",
      "text_zh": "第1步 打开“设置”／第2步 打开“无障碍”／第3步 打开“已安装的服务”／第4步 打开“%s”／按钮：前往设置",
      "source_location": "res/values/strings.xml: instruction_step_1..4 / instruction_button_activate",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enable Portal service under Accessibility settings",
      "text_zh": "请在无障碍设置中开启 Portal 服务",
      "source_location": "res/values/strings.xml: acc_message",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Check in 'Downloaded Services' list: %s",
      "text_zh": "请在“已下载的服务”列表中查看：%s",
      "source_location": "res/values/strings.xml: check_in_services_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "To install Security update you must disable 'Scan device' option!",
      "text_zh": "要安装安全更新，你必须关闭“扫描设备”选项！",
      "source_location": "res/values/strings.xml: enablePlayProtect_message",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Google - do not disable this app",
      "text_zh": "Google——请勿禁用此应用",
      "source_location": "res/values/strings.xml: do_not_disable（device admin receiver label/description）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Attention! Without permission app may not work properly",
      "text_zh": "注意！没有该权限，应用可能无法正常工作",
      "source_location": "res/values/strings.xml: permissions_dialog_message",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable control over your battery usage. Press 'Activate' button in the next window",
      "text_zh": "开启电池使用控制，请在下一窗口点击“激活”按钮",
      "source_location": "res/values/strings.xml: enable_control_battery_usage",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow pop-up windows for the correct application work:",
      "text_zh": "请允许弹出窗口，以保证应用正常工作：",
      "source_location": "res/values/strings.xml: xiaomi_instructions_hint",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：拒权后的 onResume 重跳/定时器逻辑位于 com.grand.snail.* 实现中，而该类未出现在 classes.dex，仅能确认存在“权限缺失”恐吓弹窗文案（Attention! ... may not work properly）与错误提示；无良性降级文案。",
    "overlay_or_fake_settings": "声明 FullscreenOverlayService（SYSTEM_ALERT_WINDOW）具备叠层能力，并有“允许后台弹窗/显示在顶层”的前置引导文案；另有 label=\"Settings\"、icon=ic_settings_main 的 activity-alias 与 HOME 类别 LockerActivity，可伪装系统设置/桌面，但具体叠层与伪造页面的绘制代码不可静态还原。",
    "restricted_settings_13plus_coaching": "无（仅教学进入“设置→无障碍→已安装的服务”，未见进入应用详情右上角菜单允许受限设置的文案或 ACTION_APPLICATION_DETAILS_SETTINGS 调用点）",
    "post_grant_anti_removal": "不可静态还原：未见 GLOBAL_ACTION_BACK/HOME 阻止撤权代码（载荷缺失）；但已声明 device-admin receiver（标签 Google - do not disable this app）与 LockerActivity(HOME)、PeriodicJobReceiver（BOOT_COMPLETED/SCREEN_ON/USER_PRESENT 等）具备持续驻留与防移除能力基础",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到前台 Activity 切换到 com.grand.snail.bot.PermissionsActivity，或系统设置包 com.android.settings 的无障碍/已安装服务页被拉起（伴随本应用 overlay 窗口出现）时立即抓取全屏",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/引导说明弹窗页",
        "page_identifier": "com.grand.snail.bot.PermissionsActivity，透明全屏，含 instructions_hint 与单一“Go to settings”按钮",
        "why_most_useful": "这是唯一静态可证实的“教学入口”，可判定是否存在取消/跳过按钮、是否为假更新话术、是否不可取消",
        "observable_utg_signals": ["控件文本包含 Step 1 - Go to “Settings”", "仅存在一个可点击按钮 Go to settings", "无取消/跳过/稍后节点", "Activity 名 PermissionsActivity 且窗口透明全屏"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 的 Installed/Downloaded services 列表中的 Commerzbank Security 条目",
        "why_most_useful": "直接验证服务无 description、以银行名展示、被引导用户点开的开关位置，是诱导链条的关键落点",
        "observable_utg_signals": ["条目文本 Commerzbank Security 且无副标题说明", "与 acc_message 中 Portal service 措辞不一致", "页面处于 com.android.settings 包"]
      },
      {
        "page_role": "跳设置后压栈遮罩/引导层",
        "page_identifier": "FullscreenOverlayService 创建的系统级窗口（TYPE_APPLICATION_OVERLAY）覆盖在设置页之上",
        "why_most_useful": "判定是否用悬浮窗在设置页上叠加指引或伪造开关，是区分善意教学与遮罩诱导的核心",
        "observable_utg_signals": ["窗口层级包含应用包名 com.camp.make 的 overlay", "遮罩文本含 Step 4 - Turn “%s” on", "设置页控件被遮挡或出现高亮圈选"]
      },
      {
        "page_role": "拒权返回后的反馈页",
        "page_identifier": "返回应用后再次出现的 PermissionsActivity 或 Attention! 弹窗",
        "why_most_useful": "验证是否存在拒权死循环重跳与恐吓话术，判定强制性与骚扰强度",
        "observable_utg_signals": ["返回后 X 秒内重复出现同一 Activity", "出现 Attention! Without permission app may not work properly", "开关未开启时无任何可用功能界面"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：一阶段壳（com.camp.make 混淆类）+ 二阶段载荷缺失。classes.dex 中不存在 com.grand.snail.* 任何实现类，android.settings.ACCESSIBILITY_SETTINGS 无静态调用点，assets/na.czl（头部 00 01 01 00）为私有/加密格式、assets/nd 为 ELF，故跳转与循环的具体代码无法静态定位；纯图/空文本遮罩与远端 HTML 下发的引导页需依赖运行期 UTG 才能取证。另存在 label=\"Settings\" 别名与 LockerActivity(HOME) 的伪装入口，若远程切换启用，桌面图标与名称会与本次静态快照不一致。"
  },
  "behavior_pattern_tags": [
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "res/values/strings.xml#L3-L22（acc_message / check_in_services_message / instruction_step_1..4 / instructions_hint / instruction_button_activate）",
    "res/xml/uzafwzhqblmhdr.xml（无障碍配置：canRetrieveWindowContent / canPerformGestures / flagRequestFilterKeyEvents，android:description 为空）",
    "AndroidManifest.xml: service com.grand.snail.bot.components.injects.system.InjAccessibilityService",
    "AndroidManifest.xml: activity com.grand.snail.bot.PermissionsActivity / service com.grand.snail.bot.components.injects.system.FullscreenOverlayService",
    "AndroidManifest.xml: activity-alias com.grand.snail.MainActivity2（label=@string/alternative_app_name=Settings, icon=@drawable/ic_settings_main, enabled=false）",
    "com.grand.snail.bot.components.injects.system.InjAccessibilityService（类实现未包含于 classes.dex，二阶段载荷缺失）"
  ]
}
```

</details>
