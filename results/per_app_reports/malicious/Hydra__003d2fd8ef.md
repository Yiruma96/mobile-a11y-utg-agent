# MB_053__003d2fd8ef｜Hydra — HD Video Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：109.4s

## 1. 一句话核心结论

- **核心申请方式**：以 'HD Video Player' 上架的样本把真实逻辑藏在加密载荷里，仅留下带单一'Go to settings'按钮、无取消选项的四步'下载服务'教学弹窗与仿 Play Protect 恐吓话术，把用户一步步推入系统无障碍列表为 InjAccessibilityService 授权。
- **静态可见性说明**：Manifest、无障碍服务声明、serviceconfig.xml、全部引导字符串与三个引导布局（instruction_dialog / samsung_show_top_dialog / xiaomi_background_activity_dialog）静态完整可见；但 Manifest 声明的 deal.average.off.* 组件类在 classes.dex 中全部缺失，真实业务代码由 Application attachBaseContext 经 assets/xcN.json（2.9MB 高熵密文）解密注入，跳转 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 的调用点、onResume 拒权重跳与获权后动作在 DEX 中检索均为 no_matches，无法静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `003d2fd8ef8fc9d4765e4bbc650ecd20ef339be94606486629c003f683cb5982` |
| 包名 / 年份 | `kind.collect.action` / 2024 |
| 家族 / 品类 | **Hydra**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | HD Video Player |
| 引导页宣称品牌/身份 | Google / Play Protect 安全组件（strings 中 app_name=GoogleReader、设备管理器名 'Google - do not disable this app'、仿 Play Protect 设置页文案） |
| 系统无障碍列表服务名 | 未声明 android:label 与 android:description，系统无障碍列表仅显示类名 InjAccessibilityService（无说明文字） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务故意省略 label/description，使系统列表只剩类名、无功能说明；settingsActivity 置空；启动 Activity 与 PermissionsActivity 均 excludeFromRecents 且使用 Theme.Translucent.NoTitleBar.Fullscreen 透明全屏主题掩盖真实界面；桌面名 'HD Video Player'、字符串 app_name 'GoogleReader'、设备管理器 'Google - do not disable this app' 三套身份并存；普通 Activity 使用 label_creek/label_mom/label_range 等无语义标签；全部类名与包名 deal.average.off.* 为随机字母串混淆。 |
| 无障碍服务类名 | `deal.average.off.bot.components.injects.system.InjAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | deal.average.off.MainActivity（LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents） | 用户点击桌面图标 / BOOT_COMPLETED 后 PeriodicJobReceiver 拉起 | 原生Activity | **原文**：无（透明全屏主题，静态无可见文案）<br>**译注**：透明无标题全屏壳页面，静态资源中不含该页文案 | 无需操作，作为跳板继续拉起权限引导流程 | `AndroidManifest.xml: activity deal.average.off.MainActivity（类体不在 classes.dex，逻辑位于 assets/xcN.json 加密载荷）` |
| 2 | 引导说明页 | 原生引导对话框（layout/instruction_dialog.xml 承载，业务代码不可见） | 冷启动后由注入载荷内的控制逻辑触发（静态不可见） | 原生Dialog | **原文**：Activate accessibility services for the correct application work: / Step 1. - Go to Settings / Step 2. - Open "Downloaded Services" menu / Step 3. - Activate services for the %s / Enjoy your new opportunities / Go to settings<br>**译注**：为让应用正常工作，请激活无障碍服务：第1步 进入设置；第2步 打开“已下载的服务”菜单；第3步 为 %s 激活服务；尽享全新体验；按钮：前往设置 | 只能点击唯一的 'Go to settings' 按钮，布局中无取消/跳过/关闭控件 | `res/layout/instruction_dialog.xml + res/values/strings.xml (instructions_hint, instruction_step_1..4, instruction_button_activate)` |
| 3 | 跳受限设置 | deal.average.off.bot.PermissionsActivity（透明全屏、excludeFromRecents）+ 系统应用详情/特殊权限页 | 引导弹窗按钮点击 → 载荷内 Intent 跳转（ACTION_APPLICATION_DETAILS_SETTINGS / 悬浮窗、电池优化等设置页） | 系统无障碍页 | **原文**：Attention! / Attention! Without permission app may not work properly / Enable control over your battery usage. Press 'Activate' button in the next window / Step 2. - Give permission to "Appear on top" / Step 2. - Allow to display pop-up windows from background mode<br>**译注**：注意！缺少权限应用可能无法正常工作 / 启用对电池使用的控制，请在下一窗口点击“激活” / 第2步 授予“显示在其他应用上层”权限 / 第2步 允许后台弹出界面 | 在系统设置页手动授予悬浮窗/后台弹窗/忽略电池优化权限；无取消说明 | `res/values/strings.xml (permissions_dialog_title, permissions_dialog_message, admin_explainMessage, samsung_instruction_step_2, xiaomi_instruction_step_2) + layout/samsung_show_top_dialog.xml、xiaomi_background_activity_dialog.xml` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务（Downloaded Services）列表，目标项 InjAccessibilityService | 引导按钮触发 ACTION_ACCESSIBILITY_SETTINGS 跳转（调用点位于加密载荷，DEX 内 no_matches） | 系统无障碍页 | **原文**：Check in 'Downloaded Services' list: %s / Step 3. - Activate services for the %s<br>**译注**：请在“已下载的服务”列表中查看：%s / 第3步 为 %s 激活服务 | 在系统无障碍列表中手动打开 InjAccessibilityService 开关；服务本身无 label/description，用户看不到任何功能说明 | `res/values/strings.xml (enableAccessibilityServices_message, instruction_step_3) + AndroidManifest service deal.average.off.bot.components.injects.system.InjAccessibilityService` |
| 5 | 遮罩叠层指引 | 仿系统/仿 Play Protect 页面（services_playProtect* 文案集）与悬浮窗提示 | 设置页停留期间或返回应用时由载荷内控制逻辑展示（静态不可见触发点） | 原生Activity | **原文**：Protected System component. Can't be viewed / Error / To install Security update you must disable 'Scan device' option! / Play Protect / Scan device for / protection? / turn off / Settings / My apps & games / open / Stop / Uninstall / Ok<br>**译注**：受保护的系统组件，无法查看 / 错误 / 要安装安全更新，你必须关闭“扫描设备”选项！/ Play Protect / 扫描设备以…/…保护？/ 关闭 / 设置 / 我的应用与游戏 / 打开 / 停止 / 卸载 / 确定 | 引导用户相信这是受保护的系统组件，并主动关闭 Play Protect 扫描后继续安装 | `res/values/strings.xml (dialogAppSettingsErrorText, dialogErrorTitle, enablePlayProtect_message, services_playProtect*, services_playScanningDisableBtn)` |
| 6 | 拒权反馈循环 | 返回应用后再次弹出引导弹窗 / 重新跳转设置页（载荷内 onResume 或定时器实现，静态不可见） | 用户从系统设置返回或拒绝授权后的生命周期回调 | 不可静态还原 | **原文**：Attention! Without permission app may not work properly<br>**译注**：注意！缺少权限应用可能无法正常工作 | 重复弹窗施压直至用户开启无障碍服务；布局中无跳过入口，具体重跳机制需动态确认 | `res/values/strings.xml (permissions_dialog_message) — 重跳调用点位于 assets/xcN.json 加密载荷，静态 no_matches` |
| 7 | 获权后动作 | InjAccessibilityService（可读窗口内容 + 按键过滤）→ 短信/通话/设备管理器/Socks5 代理/录屏等能力 | 无障碍服务被系统绑定后由载荷内指令通道驱动 | 不可静态还原 | **原文**：Enjoy your new opportunities<br>**译注**：尽享全新体验 | 无（获权后自动执行，含 SMS 收发、拨号、安装包、设备管理器策略等） | `res/xml/serviceconfig.xml + res/xml/policies.xml + AndroidManifest 权限集；实际行为实现位于 assets/xcN.json 加密载荷` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动后的原生引导对话框：res/layout/instruction_dialog.xml（标题 instructions_hint + 四步步骤文字 + 唯一按钮 'Go to settings'）
- 三星机型专用引导对话框：res/layout/samsung_show_top_dialog.xml（改用 samsung_instruction_step_2 'Give permission to "Appear on top"'）
- 小米机型专用引导对话框：res/layout/xiaomi_background_activity_dialog.xml（改用 xiaomi_instruction_step_2 'Allow to display pop-up windows from background mode'）
- 权限施压弹窗：strings permissions_dialog_title='Attention!'、permissions_dialog_message='Without permission app may not work properly'
- 设备管理器激活说明：strings admin_app_name='Google - do not disable this app'、admin_explainMessage='Enable control over your battery usage...'（对应 res/xml/policies.xml 的设备管理策略）
- 仿 Play Protect 页面文案集：strings services_playProtect、services_playProtectCheckApps、services_playProtectDisableText、services_playScanningDisableBtn、servicesButton_ForceStop/Uninstall、services_my_apps
- 错误/受保护组件提示：strings dialogErrorTitle='Error'、dialogAppSettingsErrorText='Protected System component. Can't be viewed'
- 无障碍引导提示：strings enableAccessibilityServices_message='Check in \'Downloaded Services\' list: %s'、instruction_step_1..4、instruction_button_activate='Go to settings'
- 系统无障碍服务列表项：service 未声明 android:label / android:description，仅显示类名 InjAccessibilityService，无任何说明文字（res/xml/serviceconfig.xml 未配置 description）
- assets/wifidirect_guid/{en,ru,in}/wifi-direct-guid-panelless.html：与无障碍无关的打印机连接指引，属重打包宿主应用遗留资源

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Activate accessibility services for the correct application work: | 请为应用的正常工作激活无障碍服务： | `res/values/strings.xml key=instructions_hint；layout/instruction_dialog.xml 标题` | 假故障恐吓 |
| en | Step 1. - Go to Settings | 第 1 步 —— 进入设置 | `res/values/strings.xml key=instruction_step_1` | 受限设置分步教学 |
| en | Step 2. - Open "Downloaded Services" menu | 第 2 步 —— 打开“已下载的服务”菜单 | `res/values/strings.xml key=instruction_step_2` | 受限设置分步教学 |
| en | Step 3. - Activate services for the %s | 第 3 步 —— 为 %s 激活服务 | `res/values/strings.xml key=instruction_step_3` | 受限设置分步教学 |
| en | Enjoy your new opportunities | 尽享你的全新体验 | `res/values/strings.xml key=instruction_step_4` | 良性透明说明 |
| en | Go to settings | 前往设置 | `res/values/strings.xml key=instruction_button_activate；layout/instruction_dialog.xml 按钮 id=bt_goto_settings` | 受限设置分步教学 |
| en | Check in 'Downloaded Services' list: %s | 请在“已下载的服务”列表中查看：%s | `res/values/strings.xml key=enableAccessibilityServices_message` | 受限设置分步教学 |
| en | Attention! | 注意！ | `res/values/strings.xml key=permissions_dialog_title` | 假故障恐吓 |
| en | Attention! Without permission app may not work properly | 注意！没有该权限应用可能无法正常运行 | `res/values/strings.xml key=permissions_dialog_message` | 假故障恐吓 |
| en | Google - do not disable this app | Google —— 请勿停用本应用 | `res/values/strings.xml key=admin_app_name（设备管理器 receiver label/description）` | 假反诈安全 |
| en | Enable control over your battery usage. Press 'Activate' button in the next window | 启用对电池使用的控制。请在下一窗口点击“激活”按钮 | `res/values/strings.xml key=admin_explainMessage` | 清理工具伪装 |
| en | Protected System component. Can't be viewed | 受保护的系统组件，无法查看 | `res/values/strings.xml key=dialogAppSettingsErrorText` | 教唆忽视警告 |
| en | To install Security update you must disable 'Scan device' option! | 要安装安全更新，你必须先关闭“扫描设备”选项！ | `res/values/strings.xml key=enablePlayProtect_message` | 假更新 |
| en | Scan device for | 扫描设备以…（仿 Play Protect 界面片段） | `res/values/strings.xml key=services_playProtectCheckApps` | 假反诈安全 |
| en | protection? | …保护？（仿 Play Protect 关闭确认片段） | `res/values/strings.xml key=services_playProtectDisableText` | 教唆忽视警告 |
| en | turn off | 关闭 | `res/values/strings.xml key=services_playScanningDisableBtn` | 教唆忽视警告 |
| en | Step 2. - Give permission to "Appear on top" | 第 2 步 —— 授予“显示在其他应用上层”权限 | `res/values/strings.xml key=samsung_instruction_step_2（layout/samsung_show_top_dialog.xml）` | 受限设置分步教学 |
| en | Step 2. - Allow to display pop-up windows from background mode | 第 2 步 —— 允许后台模式下弹出窗口 | `res/values/strings.xml key=xiaomi_instruction_step_2（layout/xiaomi_background_activity_dialog.xml）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态不可完整确认：三个引导布局均无取消/跳过控件，仅存在单一 'Go to settings' 按钮；拒权或从系统设置返回后的重跳逻辑（onResume 重跳或定时器拉起）位于 assets/xcN.json 加密载荷内，DEX 中 ACTION_ACCESSIBILITY_SETTINGS 检索 no_matches，需动态分析验证是否为死循环重跳。
- **遮罩叠层 / 高仿系统设置页**：具备仿系统/仿 Play Protect 页面的字符串与按钮物料（services_playProtect、services_playProtectCheckApps、services_playScanningDisableBtn、servicesButton_ForceStop/Uninstall、services_my_apps），并持有 SYSTEM_ALERT_WINDOW 权限；但静态资源中未见对应仿设置页 layout，遮罩/悬浮窗实际呈现需动态确认。
- **Android 13+ 受限设置（Restricted Settings）应对**：有受限设置分步教学：strings 明确指示进入设置 → 打开 'Downloaded Services' 菜单 → 为 %s 激活服务，即教用户绕过 Android 13+ 无障碍受限设置限制；未见应用详情右上角菜单或 Session 安装器的显式文案。
- **获权后即时行为与防撤权机制**：静态可见部分为隐性防清除：设备管理器（policies: force-lock / reset-password / limit-password / encrypted-storage）与 admin_app_name 'Google - do not disable this app'、LockerActivity 注册为 HOME，获权后是否监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权位于加密载荷内，需动态确认。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到应用发起 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 跳转的瞬间拉起 UTG（此时截取跳转前的引导弹窗残留与系统无障碍列表页）；若冷启动后 3 秒内即出现 'Go to settings' 引导弹窗，则直接从冷启动开始全程 UTG 录制。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：真实引导/跳转逻辑位于 assets/xcN.json 加密二阶段载荷，Manifest 声明的 deal.average.off.* 组件类在 classes.dex 中不存在，故 UTG 必须以运行期实际呈现为准，不能依赖静态页面清单；另外 assets 中混入打印机 SDK 与 OpenVPN 等宿主遗留资源，抓取时需避免把 wifidirect_guid HTML 等良性页面误判为诱导页面。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 浅灰白底原生 Dialog，标题 'Activate accessibility services for the correct application work:'，正文为 Step 1/2/3/4 四行带下边框，底部单个蓝色按钮 'Go to settings'，无取消按钮 | 这是本样本唯一的静态可见诱导界面，其四步文案与单按钮结构直接证明'分步教用户开无障碍且不给退出选项' | 标题与四步文案逐字文本；按钮列表仅有 'Go to settings'（无 Cancel/Skip/Close）；Dialog 无关闭图标、点外部不消失 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务，条目名显示 'InjAccessibilityService'，无描述文字，开关为关闭状态 | 服务未声明 label/description，系统列表只剩混淆类名，可与桌面名 'HD Video Player' 形成身份错配的直接对照 | 条目文本为类名 InjAccessibilityService；description 区域为空或仅显示类名；所在分组为 Downloaded Services / 已下载的服务 |
| **跳转前权限施压弹窗页** | 标题 'Attention!'，正文 'Without permission app may not work properly' 或 'Enable control over your battery usage. Press 'Activate' button in the next window' | 用于区分'善意权限说明'与'故障恐吓式施压'，并捕获跳转目标（应用详情/电池优化/悬浮窗）的准确顺序 | 弹窗标题/正文原文；弹窗按钮集合；紧接其后的系统页面标题（应用详情或电池优化） |
| **设置页返回后的压栈遮罩页** | 从系统设置返回后立即出现的重复引导 Dialog 或半透明悬浮窗（含 'Protected System component. Can't be viewed' / 仿 Play Protect 文案） | 确认是否存在拒权死循环重跳以及是否叠放仿系统设置界面，是判定胁迫强度的关键 | 返回应用后 1 秒内是否再次出现同文案 Dialog；是否存在非应用 Activity 的悬浮层；页面标题是否伪装为 Play Protect / Settings |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `kind.collect.action.KAlOfBpWiDePb.attachBaseContext（反射解密加载 assets/xcN.json 的注入入口）`
- `assets/xcN.json（2.9MB 高熵密文二阶段载荷，承载跳转/重跳/获权后逻辑）`
- `res/layout/instruction_dialog.xml（四步无障碍教学弹窗，唯一按钮 bt_goto_settings）`
- `res/values/strings.xml（instructions_hint / instruction_step_1..4 / enableAccessibilityServices_message / services_playProtect* / admin_app_name）`
- `res/xml/serviceconfig.xml（无障碍服务未声明 description，请求 flagReportViewIds|flagRequestFilterKeyEvents、canRetrieveWindowContent、notificationTimeout=1）`
- `AndroidManifest.xml（deal.average.off.bot.components.injects.system.InjAccessibilityService 与 deal.average.off.MainActivity / PermissionsActivity 声明）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论

- **身份与代码分离**：Manifest 声明的启动入口 [MainActivity](<resource-unit:#1 manifest:components>) 与无障碍服务 [InjAccessibilityService](<resource-unit:#1 manifest:components>) 均属 `deal.average.off.*` 包，但该类在 `classes.dex` 中完全不存在（`search_function_definitions` 对 `off.bot`、`MainActivity`、`InjAccessibilityService` 全部 `no_matches`），仅剩空的 `deal.average.off.*` 组件名占位。真实逻辑由 [KAlOfBpWiDePb.attachBaseContext()](<resource-unit:#1.dex1 code:kind.collect.action.KAlOfBpWiDePb#attachBaseContext>) 通过 `cratercritic → reduceexample → receiveeagle → pearlamp` 解密加载 [assets/xcN.json](<resource-unit:#1 file:assets/xcN.json>)（2.9 MB，首字节 `57 8b 47 c9`，高熵、非 zip/dex 魔数）注入。
- **引导物料齐全、触发代码不可见**：[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L3-L33>) 内置了完整四步教学与冒充话术；三个引导布局 [instruction_dialog.xml](<resource-unit:#1 file:res/layout/instruction_dialog.xml#L6-L12>)、`samsung_show_top_dialog.xml`、`xiaomi_background_activity_dialog.xml` 均只有**单一蓝色按钮 `bt_goto_settings`（"Go to settings"），无取消/跳过控件**，并带分步骤灰底分割线排版。但 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 在 DEX 中检索为 `no_matches`——跳转与 `onResume` 拒权重跳逻辑位于加密载荷内，静态不可还原。
- **系统无障碍列表身份被抹除**：[serviceconfig.xml](<resource-unit:#1 file:res/xml/serviceconfig.xml#L2>) 未设 `android:description`，Manifest 中该 service 也未设 `android:label`，故系统列表仅显示类名 `InjAccessibilityService`，与桌面名 "HD Video Player"、`strings.xml` 中 `app_name=GoogleReader`、设备管理器名 "Google - do not disable this app" 三套身份互不相符；同时请求 `flagRequestFilterKeyEvents`+`canRetrieveWindowContent`+`notificationTimeout=1`（可读取窗口内容与过滤按键，属高权限监视配置）。
- **伪装系统页 + 假更新诱导链**：`services_playProtect*`、`enablePlayProtect_message`、`dialogAppSettingsErrorText` 等字符串构成一套"仿 Play Protect 设置页 + 恐吓关闭扫描 + 假安全更新"话术，配合 `REQUEST_INSTALL_PACKAGES`、`SYSTEM_ALERT_WINDOW`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`，指向"先关防护→再开无障碍→再装包"的完整操纵序列。
- **重打包痕迹**：`assets/` 混杂 Epson/打印机 SDK（`wifidirect_guid/*`、`iPrint_PRIVACY_STATEMENT`、`MyPocketSDK.properties`）、OpenVPN 可执行文件与健身 JSON，说明样本在良性宿主应用之上叠加了恶意层，与 "HD Video Player" 功能描述不符。
- **覆盖边界**：包内无 `DexClassLoader` 静态调用点（`Class.newInstance`/反射散布于 `kind.collect.action.*` 混淆类），二阶段加载方式与 UTG 页面流转细节需动态验证；未启动设备。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍服务声明、serviceconfig.xml、全部引导字符串与三个引导布局（instruction_dialog / samsung_show_top_dialog / xiaomi_background_activity_dialog）静态完整可见；但 Manifest 声明的 deal.average.off.* 组件类在 classes.dex 中全部缺失，真实业务代码由 Application attachBaseContext 经 assets/xcN.json（2.9MB 高熵密文）解密注入，跳转 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 的调用点、onResume 拒权重跳与获权后动作在 DEX 中检索均为 no_matches，无法静态还原。",
  "summary_one_liner": "以 'HD Video Player' 上架的样本把真实逻辑藏在加密载荷里，仅留下带单一'Go to settings'按钮、无取消选项的四步'下载服务'教学弹窗与仿 Play Protect 恐吓话术，把用户一步步推入系统无障碍列表为 InjAccessibilityService 授权。",
  "disguise_identity": {
    "app_display_name": "HD Video Player",
    "claimed_brand_or_persona": "Google / Play Protect 安全组件（strings 中 app_name=GoogleReader、设备管理器名 'Google - do not disable this app'、仿 Play Protect 设置页文案）",
    "a11y_service_label": "未声明 android:label 与 android:description，系统无障碍列表仅显示类名 InjAccessibilityService（无说明文字）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务故意省略 label/description，使系统列表只剩类名、无功能说明；settingsActivity 置空；启动 Activity 与 PermissionsActivity 均 excludeFromRecents 且使用 Theme.Translucent.NoTitleBar.Fullscreen 透明全屏主题掩盖真实界面；桌面名 'HD Video Player'、字符串 app_name 'GoogleReader'、设备管理器 'Google - do not disable this app' 三套身份并存；普通 Activity 使用 label_creek/label_mom/label_range 等无语义标签；全部类名与包名 deal.average.off.* 为随机字母串混淆。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "deal.average.off.MainActivity（LAUNCHER，Theme.Translucent.NoTitleBar.Fullscreen，excludeFromRecents）",
      "trigger_event": "用户点击桌面图标 / BOOT_COMPLETED 后 PeriodicJobReceiver 拉起",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（透明全屏主题，静态无可见文案）",
      "shown_text_zh": "透明无标题全屏壳页面，静态资源中不含该页文案",
      "user_action_requested": "无需操作，作为跳板继续拉起权限引导流程",
      "code_anchor": "AndroidManifest.xml: activity deal.average.off.MainActivity（类体不在 classes.dex，逻辑位于 assets/xcN.json 加密载荷）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "原生引导对话框（layout/instruction_dialog.xml 承载，业务代码不可见）",
      "trigger_event": "冷启动后由注入载荷内的控制逻辑触发（静态不可见）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Activate accessibility services for the correct application work: / Step 1. - Go to Settings / Step 2. - Open \"Downloaded Services\" menu / Step 3. - Activate services for the %s / Enjoy your new opportunities / Go to settings",
      "shown_text_zh": "为让应用正常工作，请激活无障碍服务：第1步 进入设置；第2步 打开“已下载的服务”菜单；第3步 为 %s 激活服务；尽享全新体验；按钮：前往设置",
      "user_action_requested": "只能点击唯一的 'Go to settings' 按钮，布局中无取消/跳过/关闭控件",
      "code_anchor": "res/layout/instruction_dialog.xml + res/values/strings.xml (instructions_hint, instruction_step_1..4, instruction_button_activate)"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "deal.average.off.bot.PermissionsActivity（透明全屏、excludeFromRecents）+ 系统应用详情/特殊权限页",
      "trigger_event": "引导弹窗按钮点击 → 载荷内 Intent 跳转（ACTION_APPLICATION_DETAILS_SETTINGS / 悬浮窗、电池优化等设置页）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Attention! / Attention! Without permission app may not work properly / Enable control over your battery usage. Press 'Activate' button in the next window / Step 2. - Give permission to \"Appear on top\" / Step 2. - Allow to display pop-up windows from background mode",
      "shown_text_zh": "注意！缺少权限应用可能无法正常工作 / 启用对电池使用的控制，请在下一窗口点击“激活” / 第2步 授予“显示在其他应用上层”权限 / 第2步 允许后台弹出界面",
      "user_action_requested": "在系统设置页手动授予悬浮窗/后台弹窗/忽略电池优化权限；无取消说明",
      "code_anchor": "res/values/strings.xml (permissions_dialog_title, permissions_dialog_message, admin_explainMessage, samsung_instruction_step_2, xiaomi_instruction_step_2) + layout/samsung_show_top_dialog.xml、xiaomi_background_activity_dialog.xml"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务（Downloaded Services）列表，目标项 InjAccessibilityService",
      "trigger_event": "引导按钮触发 ACTION_ACCESSIBILITY_SETTINGS 跳转（调用点位于加密载荷，DEX 内 no_matches）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Check in 'Downloaded Services' list: %s / Step 3. - Activate services for the %s",
      "shown_text_zh": "请在“已下载的服务”列表中查看：%s / 第3步 为 %s 激活服务",
      "user_action_requested": "在系统无障碍列表中手动打开 InjAccessibilityService 开关；服务本身无 label/description，用户看不到任何功能说明",
      "code_anchor": "res/values/strings.xml (enableAccessibilityServices_message, instruction_step_3) + AndroidManifest service deal.average.off.bot.components.injects.system.InjAccessibilityService"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "仿系统/仿 Play Protect 页面（services_playProtect* 文案集）与悬浮窗提示",
      "trigger_event": "设置页停留期间或返回应用时由载荷内控制逻辑展示（静态不可见触发点）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Protected System component. Can't be viewed / Error / To install Security update you must disable 'Scan device' option! / Play Protect / Scan device for / protection? / turn off / Settings / My apps & games / open / Stop / Uninstall / Ok",
      "shown_text_zh": "受保护的系统组件，无法查看 / 错误 / 要安装安全更新，你必须关闭“扫描设备”选项！/ Play Protect / 扫描设备以…/…保护？/ 关闭 / 设置 / 我的应用与游戏 / 打开 / 停止 / 卸载 / 确定",
      "user_action_requested": "引导用户相信这是受保护的系统组件，并主动关闭 Play Protect 扫描后继续安装",
      "code_anchor": "res/values/strings.xml (dialogAppSettingsErrorText, dialogErrorTitle, enablePlayProtect_message, services_playProtect*, services_playScanningDisableBtn)"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回应用后再次弹出引导弹窗 / 重新跳转设置页（载荷内 onResume 或定时器实现，静态不可见）",
      "trigger_event": "用户从系统设置返回或拒绝授权后的生命周期回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Attention! Without permission app may not work properly",
      "shown_text_zh": "注意！缺少权限应用可能无法正常工作",
      "user_action_requested": "重复弹窗施压直至用户开启无障碍服务；布局中无跳过入口，具体重跳机制需动态确认",
      "code_anchor": "res/values/strings.xml (permissions_dialog_message) — 重跳调用点位于 assets/xcN.json 加密载荷，静态 no_matches"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "InjAccessibilityService（可读窗口内容 + 按键过滤）→ 短信/通话/设备管理器/Socks5 代理/录屏等能力",
      "trigger_event": "无障碍服务被系统绑定后由载荷内指令通道驱动",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Enjoy your new opportunities",
      "shown_text_zh": "尽享全新体验",
      "user_action_requested": "无（获权后自动执行，含 SMS 收发、拨号、安装包、设备管理器策略等）",
      "code_anchor": "res/xml/serviceconfig.xml + res/xml/policies.xml + AndroidManifest 权限集；实际行为实现位于 assets/xcN.json 加密载荷"
    }
  ],
  "text_presentation_locations": [
    "冷启动后的原生引导对话框：res/layout/instruction_dialog.xml（标题 instructions_hint + 四步步骤文字 + 唯一按钮 'Go to settings'）",
    "三星机型专用引导对话框：res/layout/samsung_show_top_dialog.xml（改用 samsung_instruction_step_2 'Give permission to \"Appear on top\"'）",
    "小米机型专用引导对话框：res/layout/xiaomi_background_activity_dialog.xml（改用 xiaomi_instruction_step_2 'Allow to display pop-up windows from background mode'）",
    "权限施压弹窗：strings permissions_dialog_title='Attention!'、permissions_dialog_message='Without permission app may not work properly'",
    "设备管理器激活说明：strings admin_app_name='Google - do not disable this app'、admin_explainMessage='Enable control over your battery usage...'（对应 res/xml/policies.xml 的设备管理策略）",
    "仿 Play Protect 页面文案集：strings services_playProtect、services_playProtectCheckApps、services_playProtectDisableText、services_playScanningDisableBtn、servicesButton_ForceStop/Uninstall、services_my_apps",
    "错误/受保护组件提示：strings dialogErrorTitle='Error'、dialogAppSettingsErrorText='Protected System component. Can't be viewed'",
    "无障碍引导提示：strings enableAccessibilityServices_message='Check in \\'Downloaded Services\\' list: %s'、instruction_step_1..4、instruction_button_activate='Go to settings'",
    "系统无障碍服务列表项：service 未声明 android:label / android:description，仅显示类名 InjAccessibilityService，无任何说明文字（res/xml/serviceconfig.xml 未配置 description）",
    "assets/wifidirect_guid/{en,ru,in}/wifi-direct-guid-panelless.html：与无障碍无关的打印机连接指引，属重打包宿主应用遗留资源"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Activate accessibility services for the correct application work:",
      "text_zh": "请为应用的正常工作激活无障碍服务：",
      "source_location": "res/values/strings.xml key=instructions_hint；layout/instruction_dialog.xml 标题",
      "rhetorical_frame": "假故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. - Go to Settings",
      "text_zh": "第 1 步 —— 进入设置",
      "source_location": "res/values/strings.xml key=instruction_step_1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. - Open \"Downloaded Services\" menu",
      "text_zh": "第 2 步 —— 打开“已下载的服务”菜单",
      "source_location": "res/values/strings.xml key=instruction_step_2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 3. - Activate services for the %s",
      "text_zh": "第 3 步 —— 为 %s 激活服务",
      "source_location": "res/values/strings.xml key=instruction_step_3",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enjoy your new opportunities",
      "text_zh": "尽享你的全新体验",
      "source_location": "res/values/strings.xml key=instruction_step_4",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to settings",
      "text_zh": "前往设置",
      "source_location": "res/values/strings.xml key=instruction_button_activate；layout/instruction_dialog.xml 按钮 id=bt_goto_settings",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Check in 'Downloaded Services' list: %s",
      "text_zh": "请在“已下载的服务”列表中查看：%s",
      "source_location": "res/values/strings.xml key=enableAccessibilityServices_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Attention!",
      "text_zh": "注意！",
      "source_location": "res/values/strings.xml key=permissions_dialog_title",
      "rhetorical_frame": "假故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Attention! Without permission app may not work properly",
      "text_zh": "注意！没有该权限应用可能无法正常运行",
      "source_location": "res/values/strings.xml key=permissions_dialog_message",
      "rhetorical_frame": "假故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Google - do not disable this app",
      "text_zh": "Google —— 请勿停用本应用",
      "source_location": "res/values/strings.xml key=admin_app_name（设备管理器 receiver label/description）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable control over your battery usage. Press 'Activate' button in the next window",
      "text_zh": "启用对电池使用的控制。请在下一窗口点击“激活”按钮",
      "source_location": "res/values/strings.xml key=admin_explainMessage",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Protected System component. Can't be viewed",
      "text_zh": "受保护的系统组件，无法查看",
      "source_location": "res/values/strings.xml key=dialogAppSettingsErrorText",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "To install Security update you must disable 'Scan device' option!",
      "text_zh": "要安装安全更新，你必须先关闭“扫描设备”选项！",
      "source_location": "res/values/strings.xml key=enablePlayProtect_message",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Scan device for",
      "text_zh": "扫描设备以…（仿 Play Protect 界面片段）",
      "source_location": "res/values/strings.xml key=services_playProtectCheckApps",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "protection?",
      "text_zh": "…保护？（仿 Play Protect 关闭确认片段）",
      "source_location": "res/values/strings.xml key=services_playProtectDisableText",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "turn off",
      "text_zh": "关闭",
      "source_location": "res/values/strings.xml key=services_playScanningDisableBtn",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. - Give permission to \"Appear on top\"",
      "text_zh": "第 2 步 —— 授予“显示在其他应用上层”权限",
      "source_location": "res/values/strings.xml key=samsung_instruction_step_2（layout/samsung_show_top_dialog.xml）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. - Allow to display pop-up windows from background mode",
      "text_zh": "第 2 步 —— 允许后台模式下弹出窗口",
      "source_location": "res/values/strings.xml key=xiaomi_instruction_step_2（layout/xiaomi_background_activity_dialog.xml）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态不可完整确认：三个引导布局均无取消/跳过控件，仅存在单一 'Go to settings' 按钮；拒权或从系统设置返回后的重跳逻辑（onResume 重跳或定时器拉起）位于 assets/xcN.json 加密载荷内，DEX 中 ACTION_ACCESSIBILITY_SETTINGS 检索 no_matches，需动态分析验证是否为死循环重跳。",
    "overlay_or_fake_settings": "具备仿系统/仿 Play Protect 页面的字符串与按钮物料（services_playProtect、services_playProtectCheckApps、services_playScanningDisableBtn、servicesButton_ForceStop/Uninstall、services_my_apps），并持有 SYSTEM_ALERT_WINDOW 权限；但静态资源中未见对应仿设置页 layout，遮罩/悬浮窗实际呈现需动态确认。",
    "restricted_settings_13plus_coaching": "有受限设置分步教学：strings 明确指示进入设置 → 打开 'Downloaded Services' 菜单 → 为 %s 激活服务，即教用户绕过 Android 13+ 无障碍受限设置限制；未见应用详情右上角菜单或 Session 安装器的显式文案。",
    "post_grant_anti_removal": "静态可见部分为隐性防清除：设备管理器（policies: force-lock / reset-password / limit-password / encrypted-storage）与 admin_app_name 'Google - do not disable this app'、LockerActivity 注册为 HOME，获权后是否监听设置页并用 GLOBAL_ACTION_BACK/HOME 阻止撤权位于加密载荷内，需动态确认。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到应用发起 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 跳转的瞬间拉起 UTG（此时截取跳转前的引导弹窗残留与系统无障碍列表页）；若冷启动后 3 秒内即出现 'Go to settings' 引导弹窗，则直接从冷启动开始全程 UTG 录制。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "浅灰白底原生 Dialog，标题 'Activate accessibility services for the correct application work:'，正文为 Step 1/2/3/4 四行带下边框，底部单个蓝色按钮 'Go to settings'，无取消按钮",
        "why_most_useful": "这是本样本唯一的静态可见诱导界面，其四步文案与单按钮结构直接证明'分步教用户开无障碍且不给退出选项'",
        "observable_utg_signals": ["标题与四步文案逐字文本", "按钮列表仅有 'Go to settings'（无 Cancel/Skip/Close）", "Dialog 无关闭图标、点外部不消失"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，条目名显示 'InjAccessibilityService'，无描述文字，开关为关闭状态",
        "why_most_useful": "服务未声明 label/description，系统列表只剩混淆类名，可与桌面名 'HD Video Player' 形成身份错配的直接对照",
        "observable_utg_signals": ["条目文本为类名 InjAccessibilityService", "description 区域为空或仅显示类名", "所在分组为 Downloaded Services / 已下载的服务"]
      },
      {
        "page_role": "跳转前权限施压弹窗页",
        "page_identifier": "标题 'Attention!'，正文 'Without permission app may not work properly' 或 'Enable control over your battery usage. Press 'Activate' button in the next window'",
        "why_most_useful": "用于区分'善意权限说明'与'故障恐吓式施压'，并捕获跳转目标（应用详情/电池优化/悬浮窗）的准确顺序",
        "observable_utg_signals": ["弹窗标题/正文原文", "弹窗按钮集合", "紧接其后的系统页面标题（应用详情或电池优化）"]
      },
      {
        "page_role": "设置页返回后的压栈遮罩页",
        "page_identifier": "从系统设置返回后立即出现的重复引导 Dialog 或半透明悬浮窗（含 'Protected System component. Can't be viewed' / 仿 Play Protect 文案）",
        "why_most_useful": "确认是否存在拒权死循环重跳以及是否叠放仿系统设置界面，是判定胁迫强度的关键",
        "observable_utg_signals": ["返回应用后 1 秒内是否再次出现同文案 Dialog", "是否存在非应用 Activity 的悬浮层", "页面标题是否伪装为 Play Protect / Settings"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：真实引导/跳转逻辑位于 assets/xcN.json 加密二阶段载荷，Manifest 声明的 deal.average.off.* 组件类在 classes.dex 中不存在，故 UTG 必须以运行期实际呈现为准，不能依赖静态页面清单；另外 assets 中混入打印机 SDK 与 OpenVPN 等宿主遗留资源，抓取时需避免把 wifidirect_guid HTML 等良性页面误判为诱导页面。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "kind.collect.action.KAlOfBpWiDePb.attachBaseContext（反射解密加载 assets/xcN.json 的注入入口）",
    "assets/xcN.json（2.9MB 高熵密文二阶段载荷，承载跳转/重跳/获权后逻辑）",
    "res/layout/instruction_dialog.xml（四步无障碍教学弹窗，唯一按钮 bt_goto_settings）",
    "res/values/strings.xml（instructions_hint / instruction_step_1..4 / enableAccessibilityServices_message / services_playProtect* / admin_app_name）",
    "res/xml/serviceconfig.xml（无障碍服务未声明 description，请求 flagReportViewIds|flagRequestFilterKeyEvents、canRetrieveWindowContent、notificationTimeout=1）",
    "AndroidManifest.xml（deal.average.off.bot.components.injects.system.InjAccessibilityService 与 deal.average.off.MainActivity / PermissionsActivity 声明）"
  ]
}
```

</details>
