# MB_054__d300e348a2｜Hydra — BAWAG PSK Security

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：143.9s

## 1. 一句话核心结论

- **核心申请方式**：伪装 BAWAG PSK 银行安全组件的注入式木马，用带空 label/description 的无障碍服务配合'Step1进设置→Step2打开Downloaded Services→Step3启用服务'分步教学与半透明全屏 PermissionsActivity，把用户一步步教到系统无障碍列表手动开启远程控制权限。
- **静态可见性说明**：AndroidManifest、res/values/strings.xml、res/xml/severnoneyuggpoldd.xml 完整可读，引导文案与分步教学资源全部静态可见；但清单声明的 com.ombththz.ufqsuqx.* 全部组件（含 InjAccessibilityService、PermissionsActivity、LockerActivity、Screen）在 classes.dex 中不存在，仅存 com.honey.miletes.k（Application，含混淆方法 a()）与 com.injected.StubClass，payload 由运行期注入/解密生成，故无障碍引导的具体 Intent 跳转、弹窗与悬浮遮罩实现不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d300e348a236c6fc23bceae84fdbd6deecf8f41565c032c0d062733fcb066a6e` |
| 包名 / 年份 | `com.ombththz.ufqsuqx` / 2026 |
| 家族 / 品类 | **Hydra**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | BAWAG PSK Security |
| 引导页宣称品牌/身份 | BAWAG PSK（奥地利银行）安全组件 + Google 系统组件双重伪装；resources 内 app_name 另为 GoogleReader，设备管理器名为 'Google - do not disable this app' |
| 系统无障碍列表服务名 | 无独立 label：res/xml/severnoneyuggpoldd.xml 未声明 android:label 与 android:description，系统中显示为应用名 'BAWAG PSK Security' 的空白服务项（settingsActivity 为空串） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍配置完全无 android:label/android:description，用户无法从系统列表判断服务用途；2) 三层包名/名称错位：manifest package=com.sdktools.android、代码包 com.ombththz.ufqsuqx、app_name=GoogleReader、显示名=BAWAG PSK Security；3) 设备管理器伪装 Google 并以 'do not disable this app' 阻止关闭；4) 用 'Protected System component. Can't be viewed' 阻止用户查看应用详情；5) PermissionsActivity 使用 Theme.Translucent.NoTitleBar.Fullscreen 且 excludeFromRecents 做无标题全屏遮罩；6) LockerActivity 注册为 HOME 类别且 enabled=false，可动态切换劫持桌面 |
| 无障碍服务类名 | `com.ombththz.ufqsuqx.bot.components.injects.system.InjAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.ombththz.ufqsuqx.MainActivity（Theme.Translucent.NoTitleBar.Fullscreen, excludeFromRecents, portrait）；由 com.honey.miletes.k(Application).onCreate/a() 先注入 payload 类 | 启动器点击图标 → Application.onCreate → 注入后拉起 MainActivity | 不可静态还原 | 无 | 无（被动进入） | `com.honey.miletes.k#onCreate / com.honey.miletes.k#a / com.ombththz.ufqsuqx.MainActivity（仅清单可见）` |
| 2 | 引导说明页 | com.ombththz.ufqsuqx.bot.PermissionsActivity（Theme.Translucent.NoTitleBar.Fullscreen, excludeFromRecents, portrait） | 权限未授予时的引导入口（具体触发回调不可静态还原，推测 onCreate/onResume 或 MainActivity 内判断后启动） | 不可静态还原 | **原文**：Activate accessibility services for the correct application work:<br>Step 1. - Go to Settings<br>Step 2. - Open "Downloaded Services" menu<br>Step 3. - Activate services for the %s<br>Enjoy your new opportunities<br>**译注**：为了让应用正常工作，请激活无障碍服务：第1步 进入设置；第2步 打开“已下载的服务”菜单；第3步 为 %s 启用服务；然后享受新的能力。 | 按步骤自行进入系统设置并启用无障碍；按钮文案仅为 'Go to settings'（strings instruction_button_activate），是否提供取消/跳过不可静态确认 | `res/values/strings.xml#instruction_step_1..4 / instructions_hint / instruction_button_activate；com.ombththz.ufqsuqx.bot.PermissionsActivity` |
| 3 | 跳无障碍设置 | 系统无障碍设置页（预期 android.settings.ACCESSIBILITY_SETTINGS，或经 ACTION_APPLICATION_DETAILS_SETTINGS 中转）；Intent 拼装代码不可静态还原 | 点击 'Go to settings' 按钮 | 系统无障碍页 | **原文**：Go to settings<br>**译注**：前往设置（按钮） | 点击后跳转系统设置，并要求用户手动进入“已下载的服务/已下载的应用”列表 | `res/values/strings.xml#instruction_button_activate；DEX 内无 ACTION_ACCESSIBILITY_SETTINGS 字符串（payload 注入后生成）` |
| 4 | 遮罩叠层指引 | 系统无障碍服务列表项：显示名 'BAWAG PSK Security'，无 description、无 settingsActivity，notificationTimeout=1、canRetrieveWindowContent=true、flagRequestFilterKeyEvents | 用户到达无障碍列表后，应用可能以 SYSTEM_ALERT_WINDOW 悬浮窗叠加指引（权限已申请，实现不可静态还原） | 不可静态还原 | **原文**：Check in 'Downloaded Services' list: %s<br>To install Security update you must disable 'Scan device' option!<br>**译注**：请到“已下载的服务”列表中勾选：%s；要安装安全更新，你必须关闭“扫描设备”选项！ | 在列表中勾选该银行/Google 名称的服务；同时被要求关闭 Play Protect 的“扫描设备” | `res/values/strings.xml#enableAccessibilityServices_message / enablePlayProtect_message；res/xml/severnoneyuggpoldd.xml` |
| 5 | 拒权反馈循环 | 返回应用后的再次引导（PermissionsActivity / 悬浮窗，实现不可静态还原） | 从设置页返回（推测 onResume 或定时器复查无障碍状态） | 不可静态还原 | **原文**：Attention! Without permission app may not work properly<br>**译注**：注意！没有该权限应用可能无法正常工作 | 继续开启权限；是否提供取消/降级不可静态确认（恶意样本通常无） | `res/values/strings.xml#permissions_dialog_title / permissions_dialog_message` |
| 6 | 获权后动作 | com.ombththz.ufqsuqx.bot.components.injects.system.InjAccessibilityService（注入框架执行体） | 用户在系统中勾选服务后，系统绑定 BIND_ACCESSIBILITY_SERVICE 回调 onServiceConnected | 不可静态还原 | 无 | 无（权限移交完成） | `com.ombththz.ufqsuqx.bot.components.injects.system.InjAccessibilityService（清单可见，类体不在 DEX）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml 的 instruction_step_1~4 / instructions_hint / instruction_button_activate：分步教学文案（对应 PermissionsActivity 引导页，代码体不可静态还原）
- res/values/strings.xml 的 enableAccessibilityServices_message（'Check in \'Downloaded Services\' list: %s'）：指向系统无障碍列表的定位提示
- res/values/strings.xml 的 permissions_dialog_title/message（'Attention!' / 'Without permission app may not work properly'）：权限恐吓弹窗文案
- res/values/strings.xml 的 enablePlayProtect_message / services_playProtect* 系列：伪造 Play Protect 界面要求关闭“扫描设备”
- res/values/strings.xml 的 dialogAppSettingsErrorText（'Protected System component. Can't be viewed'）：阻止用户查看应用详情
- res/values/strings.xml 的 admin_app_name / admin_explainMessage：设备管理器授权页显示 'Google - do not disable this app'
- res/values/strings.xml 的 xiaomi_instruction_step_1/2 与 samsung_instruction_step_2：按厂商定制的“允许后台弹窗/显示在其他应用上层”引导文案
- AndroidManifest：无障碍服务未声明 android:label/description（res/xml/severnoneyuggpoldd.xml 中亦无），系统无障碍列表中该服务项无任何功能说明
- AndroidManifest：com.ombththz.ufqsuqx.bot.PermissionsActivity 以 Translucent.NoTitleBar.Fullscreen + excludeFromRecents 承载全屏遮罩式引导
- AndroidManifest：LockerActivity 注册 CATEGORY_HOME 且 enabled=false、label='Settings'，可在获权后被启用为高仿桌面/设置界面

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Activate accessibility services for the correct application work: | 为了让应用正常工作，请激活无障碍服务： | `res/values/strings.xml → instructions_hint` | 教唆忽视警告 |
| en | Step 1. - Go to Settings | 第 1 步 - 进入设置 | `res/values/strings.xml → instruction_step_1` | 受限设置分步教学 |
| en | Step 2. - Open "Downloaded Services" menu | 第 2 步 - 打开“已下载的服务”菜单 | `res/values/strings.xml → instruction_step_2` | 受限设置分步教学 |
| en | Step 3. - Activate services for the %s | 第 3 步 - 为 %s 启用服务 | `res/values/strings.xml → instruction_step_3` | 受限设置分步教学 |
| en | Enjoy your new opportunities | 享受你的新能力吧 | `res/values/strings.xml → instruction_step_4` | 受限设置分步教学 |
| en | Check in 'Downloaded Services' list: %s | 请到“已下载的服务”列表中勾选：%s | `res/values/strings.xml → enableAccessibilityServices_message` | 教唆忽视警告 |
| en | Go to settings | 前往设置 | `res/values/strings.xml → instruction_button_activate` | 受限设置分步教学 |
| en | Attention! Without permission app may not work properly | 注意！没有该权限应用可能无法正常工作 | `res/values/strings.xml → permissions_dialog_message` | 故障恐吓 |
| en | Google - do not disable this app | Google - 请勿禁用此应用 | `res/values/strings.xml → admin_app_name（设备管理器 label/description）` | 假反诈安全 |
| en | Enable control over your battery usage. Press 'Activate' button in the next window | 启用对电池使用的控制。请在下一个窗口点击“激活”按钮 | `res/values/strings.xml → admin_explainMessage` | 假更新 |
| en | To install Security update you must disable 'Scan device' option! | 要安装安全更新，你必须关闭“扫描设备”选项！ | `res/values/strings.xml → enablePlayProtect_message` | 假更新 |
| en | Protected System component. Can't be viewed | 受保护的系统组件，无法查看 | `res/values/strings.xml → dialogAppSettingsErrorText` | 假反诈安全 |
| en | Allow pop-up windows for the correct application work: | 为了让应用正常工作，请允许弹出窗口： | `res/values/strings.xml → xiaomi_instructions_hint` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：静态不可完整还原：仅见 'Attention! Without permission app may not work properly' 的权限弹窗文案；是否 onResume 复查无障碍状态后无限重跳、或定时器周期拉起，需运行期 UTG 观测（工具预算内未取证）
- **遮罩叠层 / 高仿系统设置页**：配置层面存在条件：已申请 SYSTEM_ALERT_WINDOW，且 PermissionsActivity 使用 Translucent.NoTitleBar.Fullscreen + excludeFromRecents 全屏遮罩；另有 LockerActivity（CATEGORY_HOME、label='Settings'、enabled=false）可被动态启用为高仿设置/桌面界面。是否在系统无障碍页上压半透明引导层不可静态确认
- **Android 13+ 受限设置（Restricted Settings）应对**：未见 'Allow restricted settings' 菜单教学文案；实际使用的是更原始的绕行话术：'Check in \'Downloaded Services\' list: %s'（教用户到无障碍“已下载的服务”里手动勾选）与 'To install Security update you must disable \'Scan device\' option!'（教用户关闭 Play Protect 扫描以放行安装）
- **获权后即时行为与防撤权机制**：存在反移除设计但实现不可静态还原：设备管理器 label/description 为 'Google - do not disable this app'（阻止关闭/卸载），文案 'Protected System component. Can\'t be viewed' 阻止查看应用详情；是否在无障碍设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权不可静态确认
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后应用把 PermissionsActivity（Translucent.NoTitleBar.Fullscreen）压栈的瞬间即开始录屏；并以窗口焦点/Intent 监测作为触发钩子——一旦出现 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 跳转，以及无障碍状态变为 enabled 后立刻续录，可覆盖引导页→设置页→返回重引导的完整闭环。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区在实现层而非呈现层：payload 类（InjAccessibilityService/PermissionsActivity/Screen/LockerActivity）不在 classes.dex，引导页的 Intent 拼装、拒权重跳逻辑、悬浮遮罩绘制均需运行期注入后才能观测，静态只能确认文案与组件声明；此外 LockerActivity 可被动态启用为高仿 HOME/设置界面，若其渲染为纯图或复用系统样式，纯文本 UTG 可能识别不足；未发现强 VMP/一阶段纯图空文本外壳。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页** | com.ombththz.ufqsuqx.bot.PermissionsActivity：无标题全屏、半透明、不出现在最近任务；页面含 'Step 1./Step 2./Step 3.' 分步文本与唯一 'Go to settings' 按钮 | 这是分步教学文案的实际呈现载体，能直接证明应用以文本教学方式把用户导向无障碍列表，并判断有无取消/跳过与是否可返回 | 界面文本 'Step 2. - Open "Downloaded Services" menu'；仅一个 'Go to settings' 按钮、无取消/关闭控件；无标题栏、背景透出下层（Translucent） |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务 中的 'BAWAG PSK Security' 条目，无描述文字、无设置入口 | 直接验证服务 label/description 为空的欺骗效果：用户在列表中无法获知该服务用途，仅凭银行名被诱导勾选 | 条目名称与 app 显示名一致且下方无任何说明文字；该条目无 '设置' 齿轮/无 description；开关状态由关到开的时间点 |
| **设置页后叠层/返回重引导页** | 从设置返回后再次出现的 PermissionsActivity 或悬浮窗（SYSTEM_ALERT_WINDOW 图层，可能在无障碍页之上） | 区分'温和一次引导'与'拒权死循环强制'，并识别是否在系统页上压半透明遮罩指引点击位置（典型的遮挡式诱导） | 设置页返回后 <1s 内再次出现引导页；无障碍页上出现应用悬浮窗节点；同一引导文本重复出现次数 |
| **Play Protect / 设备管理器配套欺骗页** | 含 'Scan device'/'turn off' 的伪 Play Protect 界面，以及设备管理器激活页 'Google - do not disable this app' | 说明该无障碍诱导不是孤立行为，而是与关闭安全扫描、获取设备管理器防卸载组成同一权限获取链，可用于定级 | 文本 'To install Security update you must disable \'Scan device\' option!'；设备管理器激活页标题为 'Google - do not disable this app' |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `res/values/strings.xml#instruction_step_1 / instruction_step_2 / instruction_step_3 / instructions_hint / instruction_button_activate`
- `res/values/strings.xml#enableAccessibilityServices_message / enablePlayProtect_message / permissions_dialog_message`
- `res/xml/severnoneyuggpoldd.xml（无 android:label / android:description，canRetrieveWindowContent=true，flagRequestFilterKeyEvents）`
- `com.ombththz.ufqsuqx.bot.PermissionsActivity（清单：Theme.Translucent.NoTitleBar.Fullscreen + excludeFromRecents）`
- `com.ombththz.ufqsuqx.bot.components.injects.system.InjAccessibilityService（清单声明，类体不在 classes.dex）`
- `com.honey.miletes.k#onCreate / com.honey.miletes.k#a（payload 注入装载入口）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论（效率约束内收口）

**静态可见性：payload 主体不在 DEX 内**。`classes.dex` 中**完全不存在** `com.ombththz.ufqsuqx.*` 任何类（`search_function_definitions` 对 `InjAccessibilityService`/`PermissionsActivity`/`ombththz` 全部 no_matches），仅存在 `com.honey.miletes.k`（Application，含 304 指令与 3768 指令两个混淆 `a()` 方法）与 `com.injected.StubClass`，说明清单里声明的全部恶意组件由运行期注入/解密生成；DEX 剩余 8241 个类几乎全是 tencent/huawei/alibaba/bykv 等三方 SDK。因此**无障碍引导的 UI 代码本身静态不可见**，但**引导文案与流程设计在资源与 Manifest 中完整可证**。

**已确证的诱导链路（资源+清单层）**
- 身份三层不一致：桌面名 `BAWAG PSK Security`（伪装奥地利 BAWAG PSK 银行安全组件）、`strings.xml` 内 `app_name=GoogleReader`、Manifest `package="com.sdktools.android"`、真实代码包 `com.ombththz.ufqsuqx`。
- 无障碍服务 [InjAccessibilityService](<resource-unit:#1 manifest:components>) 引用的配置 [res/xml/severnoneyuggpoldd.xml](<resource-unit:#1 file:res/xml/severnoneyuggpoldd.xml>) **无 `android:label`、无 `android:description`、`settingsActivity=""`**，`canRetrieveWindowContent=true`、`flagRequestFilterKeyEvents`、`notificationTimeout=1` —— 即系统无障碍列表里用户看不到任何功能说明，只看到一个银行/Google 名称的空服务项。
- 分步教学文案全套落地于 [res/values/strings.xml](<resource-unit:#1 file:res/values/strings.xml#L9-L18>)：`Step 1. - Go to Settings` → `Step 2. - Open "Downloaded Services" menu` → `Step 3. - Activate services for the %s` → `Enjoy your new opportunities`，按钮 `Go to settings`，提示 `Activate accessibility services for the correct application work:`；并用 `Check in 'Downloaded Services' list: %s` 把"下载的服务"这一 Android 无障碍列表的真实入口名直接教给用户。这是**教用户绕开"这个服务是干什么的"这一认知环节**的典型话术。
- 辅助欺骗链同源：设备管理器名为 `Google - do not disable this app`、说明为"启用电池使用控制，在下一窗口按 Activate"（[strings.xml#L3-L4](<resource-unit:#1 file:res/values/strings.xml#L3-L4>)），以及 `To install Security update you must disable 'Scan device' option!`、`Protected System component. Can't be viewed`（诱导关闭 Play Protect / 隐藏应用详情）；配套 `PermissionsActivity`（`Theme.Translucent.NoTitleBar.Fullscreen` + `excludeFromRecents`，用于全屏遮罩式引导）与 `LockerActivity`（注册为 HOME，`enabled=false`，可劫持桌面）。

**未决边界**：`PermissionsActivity`/`Screen`/`InjAccessibilityService` 的方法体、跳转 Intent 的具体 action 拼装、拒绝后是否 `onResume` 死循环重跳、是否叠悬浮遮罩，均**只能运行期 UTG 观测**，本次未做（无静态载体、工具预算已用尽）。下面 JSON 中凡代码不可见处已如实标注。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "AndroidManifest、res/values/strings.xml、res/xml/severnoneyuggpoldd.xml 完整可读，引导文案与分步教学资源全部静态可见；但清单声明的 com.ombththz.ufqsuqx.* 全部组件（含 InjAccessibilityService、PermissionsActivity、LockerActivity、Screen）在 classes.dex 中不存在，仅存 com.honey.miletes.k（Application，含混淆方法 a()）与 com.injected.StubClass，payload 由运行期注入/解密生成，故无障碍引导的具体 Intent 跳转、弹窗与悬浮遮罩实现不可静态还原。",
  "summary_one_liner": "伪装 BAWAG PSK 银行安全组件的注入式木马，用带空 label/description 的无障碍服务配合'Step1进设置→Step2打开Downloaded Services→Step3启用服务'分步教学与半透明全屏 PermissionsActivity，把用户一步步教到系统无障碍列表手动开启远程控制权限。",
  "disguise_identity": {
    "app_display_name": "BAWAG PSK Security",
    "claimed_brand_or_persona": "BAWAG PSK（奥地利银行）安全组件 + Google 系统组件双重伪装；resources 内 app_name 另为 GoogleReader，设备管理器名为 'Google - do not disable this app'",
    "a11y_service_label": "无独立 label：res/xml/severnoneyuggpoldd.xml 未声明 android:label 与 android:description，系统中显示为应用名 'BAWAG PSK Security' 的空白服务项（settingsActivity 为空串）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍配置完全无 android:label/android:description，用户无法从系统列表判断服务用途；2) 三层包名/名称错位：manifest package=com.sdktools.android、代码包 com.ombththz.ufqsuqx、app_name=GoogleReader、显示名=BAWAG PSK Security；3) 设备管理器伪装 Google 并以 'do not disable this app' 阻止关闭；4) 用 'Protected System component. Can't be viewed' 阻止用户查看应用详情；5) PermissionsActivity 使用 Theme.Translucent.NoTitleBar.Fullscreen 且 excludeFromRecents 做无标题全屏遮罩；6) LockerActivity 注册为 HOME 类别且 enabled=false，可动态切换劫持桌面"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.ombththz.ufqsuqx.MainActivity（Theme.Translucent.NoTitleBar.Fullscreen, excludeFromRecents, portrait）；由 com.honey.miletes.k(Application).onCreate/a() 先注入 payload 类",
      "trigger_event": "启动器点击图标 → Application.onCreate → 注入后拉起 MainActivity",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "入口页面内容不可静态还原（payload 类不在 DEX 内）",
      "user_action_requested": "无（被动进入）",
      "code_anchor": "com.honey.miletes.k#onCreate / com.honey.miletes.k#a / com.ombththz.ufqsuqx.MainActivity（仅清单可见）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.ombththz.ufqsuqx.bot.PermissionsActivity（Theme.Translucent.NoTitleBar.Fullscreen, excludeFromRecents, portrait）",
      "trigger_event": "权限未授予时的引导入口（具体触发回调不可静态还原，推测 onCreate/onResume 或 MainActivity 内判断后启动）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Activate accessibility services for the correct application work:\nStep 1. - Go to Settings\nStep 2. - Open \"Downloaded Services\" menu\nStep 3. - Activate services for the %s\nEnjoy your new opportunities",
      "shown_text_zh": "为了让应用正常工作，请激活无障碍服务：第1步 进入设置；第2步 打开“已下载的服务”菜单；第3步 为 %s 启用服务；然后享受新的能力。",
      "user_action_requested": "按步骤自行进入系统设置并启用无障碍；按钮文案仅为 'Go to settings'（strings instruction_button_activate），是否提供取消/跳过不可静态确认",
      "code_anchor": "res/values/strings.xml#instruction_step_1..4 / instructions_hint / instruction_button_activate；com.ombththz.ufqsuqx.bot.PermissionsActivity"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（预期 android.settings.ACCESSIBILITY_SETTINGS，或经 ACTION_APPLICATION_DETAILS_SETTINGS 中转）；Intent 拼装代码不可静态还原",
      "trigger_event": "点击 'Go to settings' 按钮",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Go to settings",
      "shown_text_zh": "前往设置（按钮）",
      "user_action_requested": "点击后跳转系统设置，并要求用户手动进入“已下载的服务/已下载的应用”列表",
      "code_anchor": "res/values/strings.xml#instruction_button_activate；DEX 内无 ACTION_ACCESSIBILITY_SETTINGS 字符串（payload 注入后生成）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍服务列表项：显示名 'BAWAG PSK Security'，无 description、无 settingsActivity，notificationTimeout=1、canRetrieveWindowContent=true、flagRequestFilterKeyEvents",
      "trigger_event": "用户到达无障碍列表后，应用可能以 SYSTEM_ALERT_WINDOW 悬浮窗叠加指引（权限已申请，实现不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Check in 'Downloaded Services' list: %s\nTo install Security update you must disable 'Scan device' option!",
      "shown_text_zh": "请到“已下载的服务”列表中勾选：%s；要安装安全更新，你必须关闭“扫描设备”选项！",
      "user_action_requested": "在列表中勾选该银行/Google 名称的服务；同时被要求关闭 Play Protect 的“扫描设备”",
      "code_anchor": "res/values/strings.xml#enableAccessibilityServices_message / enablePlayProtect_message；res/xml/severnoneyuggpoldd.xml"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回应用后的再次引导（PermissionsActivity / 悬浮窗，实现不可静态还原）",
      "trigger_event": "从设置页返回（推测 onResume 或定时器复查无障碍状态）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Attention! Without permission app may not work properly",
      "shown_text_zh": "注意！没有该权限应用可能无法正常工作",
      "user_action_requested": "继续开启权限；是否提供取消/降级不可静态确认（恶意样本通常无）",
      "code_anchor": "res/values/strings.xml#permissions_dialog_title / permissions_dialog_message"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.ombththz.ufqsuqx.bot.components.injects.system.InjAccessibilityService（注入框架执行体）",
      "trigger_event": "用户在系统中勾选服务后，系统绑定 BIND_ACCESSIBILITY_SERVICE 回调 onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后进入注入/远控执行阶段，界面表现不可静态还原",
      "user_action_requested": "无（权限移交完成）",
      "code_anchor": "com.ombththz.ufqsuqx.bot.components.injects.system.InjAccessibilityService（清单可见，类体不在 DEX）"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml 的 instruction_step_1~4 / instructions_hint / instruction_button_activate：分步教学文案（对应 PermissionsActivity 引导页，代码体不可静态还原）",
    "res/values/strings.xml 的 enableAccessibilityServices_message（'Check in \\'Downloaded Services\\' list: %s'）：指向系统无障碍列表的定位提示",
    "res/values/strings.xml 的 permissions_dialog_title/message（'Attention!' / 'Without permission app may not work properly'）：权限恐吓弹窗文案",
    "res/values/strings.xml 的 enablePlayProtect_message / services_playProtect* 系列：伪造 Play Protect 界面要求关闭“扫描设备”",
    "res/values/strings.xml 的 dialogAppSettingsErrorText（'Protected System component. Can't be viewed'）：阻止用户查看应用详情",
    "res/values/strings.xml 的 admin_app_name / admin_explainMessage：设备管理器授权页显示 'Google - do not disable this app'",
    "res/values/strings.xml 的 xiaomi_instruction_step_1/2 与 samsung_instruction_step_2：按厂商定制的“允许后台弹窗/显示在其他应用上层”引导文案",
    "AndroidManifest：无障碍服务未声明 android:label/description（res/xml/severnoneyuggpoldd.xml 中亦无），系统无障碍列表中该服务项无任何功能说明",
    "AndroidManifest：com.ombththz.ufqsuqx.bot.PermissionsActivity 以 Translucent.NoTitleBar.Fullscreen + excludeFromRecents 承载全屏遮罩式引导",
    "AndroidManifest：LockerActivity 注册 CATEGORY_HOME 且 enabled=false、label='Settings'，可在获权后被启用为高仿桌面/设置界面"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Activate accessibility services for the correct application work:",
      "text_zh": "为了让应用正常工作，请激活无障碍服务：",
      "source_location": "res/values/strings.xml → instructions_hint",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. - Go to Settings",
      "text_zh": "第 1 步 - 进入设置",
      "source_location": "res/values/strings.xml → instruction_step_1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. - Open \"Downloaded Services\" menu",
      "text_zh": "第 2 步 - 打开“已下载的服务”菜单",
      "source_location": "res/values/strings.xml → instruction_step_2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 3. - Activate services for the %s",
      "text_zh": "第 3 步 - 为 %s 启用服务",
      "source_location": "res/values/strings.xml → instruction_step_3",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Enjoy your new opportunities",
      "text_zh": "享受你的新能力吧",
      "source_location": "res/values/strings.xml → instruction_step_4",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Check in 'Downloaded Services' list: %s",
      "text_zh": "请到“已下载的服务”列表中勾选：%s",
      "source_location": "res/values/strings.xml → enableAccessibilityServices_message",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to settings",
      "text_zh": "前往设置",
      "source_location": "res/values/strings.xml → instruction_button_activate",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Attention! Without permission app may not work properly",
      "text_zh": "注意！没有该权限应用可能无法正常工作",
      "source_location": "res/values/strings.xml → permissions_dialog_message",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Google - do not disable this app",
      "text_zh": "Google - 请勿禁用此应用",
      "source_location": "res/values/strings.xml → admin_app_name（设备管理器 label/description）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable control over your battery usage. Press 'Activate' button in the next window",
      "text_zh": "启用对电池使用的控制。请在下一个窗口点击“激活”按钮",
      "source_location": "res/values/strings.xml → admin_explainMessage",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "To install Security update you must disable 'Scan device' option!",
      "text_zh": "要安装安全更新，你必须关闭“扫描设备”选项！",
      "source_location": "res/values/strings.xml → enablePlayProtect_message",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Protected System component. Can't be viewed",
      "text_zh": "受保护的系统组件，无法查看",
      "source_location": "res/values/strings.xml → dialogAppSettingsErrorText",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow pop-up windows for the correct application work:",
      "text_zh": "为了让应用正常工作，请允许弹出窗口：",
      "source_location": "res/values/strings.xml → xiaomi_instructions_hint",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "静态不可完整还原：仅见 'Attention! Without permission app may not work properly' 的权限弹窗文案；是否 onResume 复查无障碍状态后无限重跳、或定时器周期拉起，需运行期 UTG 观测（工具预算内未取证）",
    "overlay_or_fake_settings": "配置层面存在条件：已申请 SYSTEM_ALERT_WINDOW，且 PermissionsActivity 使用 Translucent.NoTitleBar.Fullscreen + excludeFromRecents 全屏遮罩；另有 LockerActivity（CATEGORY_HOME、label='Settings'、enabled=false）可被动态启用为高仿设置/桌面界面。是否在系统无障碍页上压半透明引导层不可静态确认",
    "restricted_settings_13plus_coaching": "未见 'Allow restricted settings' 菜单教学文案；实际使用的是更原始的绕行话术：'Check in \\'Downloaded Services\\' list: %s'（教用户到无障碍“已下载的服务”里手动勾选）与 'To install Security update you must disable \\'Scan device\\' option!'（教用户关闭 Play Protect 扫描以放行安装）",
    "post_grant_anti_removal": "存在反移除设计但实现不可静态还原：设备管理器 label/description 为 'Google - do not disable this app'（阻止关闭/卸载），文案 'Protected System component. Can\\'t be viewed' 阻止查看应用详情；是否在无障碍设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权不可静态确认",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后应用把 PermissionsActivity（Translucent.NoTitleBar.Fullscreen）压栈的瞬间即开始录屏；并以窗口焦点/Intent 监测作为触发钩子——一旦出现 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 跳转，以及无障碍状态变为 enabled 后立刻续录，可覆盖引导页→设置页→返回重引导的完整闭环。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页",
        "page_identifier": "com.ombththz.ufqsuqx.bot.PermissionsActivity：无标题全屏、半透明、不出现在最近任务；页面含 'Step 1./Step 2./Step 3.' 分步文本与唯一 'Go to settings' 按钮",
        "why_most_useful": "这是分步教学文案的实际呈现载体，能直接证明应用以文本教学方式把用户导向无障碍列表，并判断有无取消/跳过与是否可返回",
        "observable_utg_signals": ["界面文本 'Step 2. - Open \"Downloaded Services\" menu'", "仅一个 'Go to settings' 按钮、无取消/关闭控件", "无标题栏、背景透出下层（Translucent）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务 中的 'BAWAG PSK Security' 条目，无描述文字、无设置入口",
        "why_most_useful": "直接验证服务 label/description 为空的欺骗效果：用户在列表中无法获知该服务用途，仅凭银行名被诱导勾选",
        "observable_utg_signals": ["条目名称与 app 显示名一致且下方无任何说明文字", "该条目无 '设置' 齿轮/无 description", "开关状态由关到开的时间点"]
      },
      {
        "page_role": "设置页后叠层/返回重引导页",
        "page_identifier": "从设置返回后再次出现的 PermissionsActivity 或悬浮窗（SYSTEM_ALERT_WINDOW 图层，可能在无障碍页之上）",
        "why_most_useful": "区分'温和一次引导'与'拒权死循环强制'，并识别是否在系统页上压半透明遮罩指引点击位置（典型的遮挡式诱导）",
        "observable_utg_signals": ["设置页返回后 <1s 内再次出现引导页", "无障碍页上出现应用悬浮窗节点", "同一引导文本重复出现次数"]
      },
      {
        "page_role": "Play Protect / 设备管理器配套欺骗页",
        "page_identifier": "含 'Scan device'/'turn off' 的伪 Play Protect 界面，以及设备管理器激活页 'Google - do not disable this app'",
        "why_most_useful": "说明该无障碍诱导不是孤立行为，而是与关闭安全扫描、获取设备管理器防卸载组成同一权限获取链，可用于定级",
        "observable_utg_signals": ["文本 'To install Security update you must disable \\'Scan device\\' option!'", "设备管理器激活页标题为 'Google - do not disable this app'"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区在实现层而非呈现层：payload 类（InjAccessibilityService/PermissionsActivity/Screen/LockerActivity）不在 classes.dex，引导页的 Intent 拼装、拒权重跳逻辑、悬浮遮罩绘制均需运行期注入后才能观测，静态只能确认文案与组件声明；此外 LockerActivity 可被动态启用为高仿 HOME/设置界面，若其渲染为纯图或复用系统样式，纯文本 UTG 可能识别不足；未发现强 VMP/一阶段纯图空文本外壳。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "res/values/strings.xml#instruction_step_1 / instruction_step_2 / instruction_step_3 / instructions_hint / instruction_button_activate",
    "res/values/strings.xml#enableAccessibilityServices_message / enablePlayProtect_message / permissions_dialog_message",
    "res/xml/severnoneyuggpoldd.xml（无 android:label / android:description，canRetrieveWindowContent=true，flagRequestFilterKeyEvents）",
    "com.ombththz.ufqsuqx.bot.PermissionsActivity（清单：Theme.Translucent.NoTitleBar.Fullscreen + excludeFromRecents）",
    "com.ombththz.ufqsuqx.bot.components.injects.system.InjAccessibilityService（清单声明，类体不在 classes.dex）",
    "com.honey.miletes.k#onCreate / com.honey.miletes.k#a（payload 注入装载入口）"
  ]
}
```

</details>
