# MR_178__2366a679bf｜TOASTAMIGO — Smart AppLocker

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：138.7s

## 1. 一句话核心结论

- **核心申请方式**：以明文 JSON 任务表驱动、按 ROM/版本分流跳转系统无障碍设置页，用全屏半透明遮罩加录屏 GIF 与 Get It 按钮教学，随后由无障碍服务自动勾选并点确定，同时对关闭/卸载警告自动点取消阻止撤权。
- **静态可见性说明**：DEX 主体被 360 加固（com.stub.StubApp 入口 + assets/libjiagu.so、libjiagu_a64/x64/x86/ls.so），com.goami.applocker.* 与 com.luna.powersaver.gp、com.wuli.go.KaService 的实际执行代码不可静态还原；assets/slogan.gpt 为 4.1MB ZIP 容器未解包。但无障碍引导与自动化流程以明文 JSON（assets/conf/set1.conf，76KB 未加密）、无障碍配置 XML、遮罩布局与 GIF 资源形式完整可见，运行期页面流转可据此还原；配置解释器（读取 set1.conf 并执行 action 的代码）位于加密 DEX，未静态确认。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `2366a679bfb69522f37cfe92507e1b028e10b84d4e784568b14211941b5236d5` |
| 包名 / 年份 | `com.agomi.applocker` / 2017 |
| 家族 / 品类 | **TOASTAMIGO**（同池样本数：44） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/k/toast-overlay-weaponized-install-android-malware-single-attack-chain.html |
| 桌面显示名 | Smart AppLocker |
| 引导页宣称品牌/身份 | 通用「Smart AppLocker」应用锁工具（自称仅用于锁定应用），引导文案另称「App Locker」 |
| 系统无障碍列表服务名 | Smart AppLocker（服务未声明 android:label，系统列表回退为应用名 app_name） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未设 android:label，系统列表显示 Smart AppLocker，而 strings 引导文案让用户去找「App Locker」，名称不吻合；包名 com.agomi.applocker 与代码命名空间 com.goami.applocker 字母互换（agomi/goami）；LAUNCHER 入口为壳的 com.stub.stub01.Stub01 而非真实首屏 ApplicationListActivity；服务描述仅称 lock apps easily，隐藏自动点击与安装器代点能力 |
| 无障碍服务类名 | `com.goami.applocker.AppLocker.MyAccessibilityServiceTmp` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.miui.home,com.umiplus.screenlock,com.android.vending,com.android.settings,com.android.packageinstaller,com.google.android.packageinstaller,com.sec.android.app.launcher,com.bbk.launcher2,com.oppo.launcher |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | The service for the purpose of Android 4.0.3 and above to lock apps easily. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.stub.stub01.Stub01（LAUNCHER）→ com.goami.applocker.AppLocker.ApplicationListActivity（真实首屏，singleInstance、excludeFromRecents） | 点击桌面图标，MAIN/LAUNCHER intent 进入壳 Activity 后跳转真实首页 | 原生Activity | **原文**：Smart AppLocker<br>**译注**：应用名「Smart AppLocker」（桌面与标题栏） | 无（正常进入应用列表首页，可选勾选要锁定的应用） | `com.goami.applocker.AppLocker.ApplicationListActivity / @string/app_name` |
| 2 | 业务功能触发 | ApplicationListActivity 首页锁定开关 / 设置项 setting_item_service_enable | 用户打开应用锁开关或选择任一待锁定应用时，检测无障碍服务未启用 | 原生Activity | **原文**：Applocker Server / Service is Running<br>**译注**：「Applocker 服务」/「服务正在运行」——以服务开关形式表达无障碍授权需求 | 点击开关开启保护（触发后续无障碍引导） | `res/values/strings.xml setting_item_service_enable / service_running` |
| 3 | 引导说明页 | 全屏半透明遮罩层（res/layout/hint_set_accessibility.xml，GifImageView + btn_get） | 配置任务 open_accessibility 执行，或检测到无障碍未开启时叠加遮罩 | 悬浮窗Overlay | **原文**：Get It（@string/str_get_it）；背景为 pic_accessibility_guide.gif 操作录屏；系统无障碍列表项说明：The service for the purpose of Android 4.0.3 and above to lock apps easily.<br>**译注**：「知道了/开始」按钮；配合 GIF 演示如何进入系统设置勾选；服务说明称「用于 Android 4.0.3 及以上轻松锁定应用的服务」 | 点击 Get It 进入系统无障碍设置页（无取消/跳过按钮，遮罩 #aa000000 全屏覆盖） | `res/layout/hint_set_accessibility.xml / res/drawable-xxhdpi-v4/pic_accessibility_guide.gif / @string/str_get_it` |
| 4 | 跳无障碍设置 | 系统设置 · 无障碍服务列表（Settings.ACTION_ACCESSIBILITY_SETTINGS） | set1.conf 任务「打开辅助7.0」（id accessibility_7，intent_time 1500ms）或「打开Tes2辅助」（id accessibility）中的 open_accessibility 动作 | 系统无障碍页 | **原文**：This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Find Setting->AccessibilityService->App Locker and Open it.<br>**译注**：「本机版本高于 Android 4.0.3，请前往 设置->无障碍服务->App Locker 并开启它。」（提示语指向的 App Locker 与列表实际显示的 Smart AppLocker 不一致） | 按提示在列表中找到条目并进入服务详情页开启（点击动作随后由程序自动完成） | `res/values/strings.xml alp_42447968_cmd_android_m_above / alp_42447968_cmd_android_m_above_toast；assets/conf/set1.conf 任务 accessibility_7` |
| 5 | 遮罩叠层指引 | 无障碍服务详情页之上叠放的 hint_set_accessibility 遮罩（跳转后 intent_time 1500ms 拉起） | 进入设置页后按 intent_time=1500ms 定时触发遮罩与自动点击序列 | 悬浮窗Overlay | **原文**：Get It；pic_accessibility_guide.gif（逐帧演示点击「Smart AppLocker」条目与开关位置）<br>**译注**：「Get It」按钮 + GIF 动画指示应点击的条目与开关坐标 | 照 GIF 指示点击服务条目与开关（遮罩全屏覆盖，无关闭入口） | `assets/conf/set1.conf action: check_package_as_check_close_7.0 / res/layout/hint_set_accessibility.xml` |
| 6 | 获权后动作 | MyAccessibilityServiceTmp 自动执行 click_package_as_check → click_enter_must；随后任务表转入 usage_access / notify / unknown_source 等分支 | 无障碍服务连接成功后，配置解释器依 rom 字段继续执行后续任务 | 系统无障碍页 | **原文**：click_package_as_check / click_enter_must / check_package_as_check_close_7.0（配置动作标识，非界面文案）；界面层为系统无障碍详情页的开关与「确定」弹窗<br>**译注**：由服务自身在无障碍详情页勾选服务并点击系统「确定」按钮完成授权，无需用户手动点击 | 无（授权动作由程序代劳）；用户仅在弹窗出现时被要求忽略或确认 | `assets/conf/set1.conf 任务 accessibility_7 action 列表 / #1 manifest:components 服务 MyAccessibilityServiceTmp` |
| 7 | 拒权反馈循环 | com.android.settings 的 android.app.AlertDialog（关闭无障碍警告）与 com.android.packageinstaller 的 android.app.AlertDialog（卸载确认） | 用户在设置页尝试关闭无障碍或卸载时，后台任务 as_dialog / setting_dialog 被触发（background=true） | 系统无障碍页 | **原文**：check_dialog_title_is_want → check_dialog_content_is_want → click_cancel_enter（配置动作标识）；界面为系统「关闭此无障碍服务？」类警告弹窗<br>**译注**：识别系统警告弹窗标题与内容后自动点击「取消」，使关闭无障碍/卸载操作无法完成 | 用户被要求确认关闭或卸载，但确认路径被自动点击「取消」阻断；配置中无跳过或降级选项 | `assets/conf/set1.conf 任务 bgAsprotectDialog（as_dialog）/ bgSettingUninstallDialog（setting_dialog）/ 桌面防卸载` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml · accessibility_service_description —— 系统无障碍列表/详情页显示的服务说明：「The service for the purpose of Android 4.0.3 and above to lock apps easily.」
- res/xml/phone_accessibility.xml —— android:description 引用上述字符串，声明 typeAllMask + canRetrieveWindowContent + canRequestFilterKeyEvents
- res/layout/hint_set_accessibility.xml —— #aa000000 全屏半透明遮罩内的 GifImageView（pic_accessibility_guide.gif）与 Get It 按钮，跳设置页后压栈叠放
- res/drawable-xxhdpi-v4/pic_accessibility_guide.gif —— 298KB 逐帧操作录屏，以图像方式演示在系统设置中勾选服务，无文字
- res/values/strings.xml · alp_42447968_cmd_android_m_above / alp_42447968_cmd_android_m_above_toast —— 提示用户「Go Setting->AccessibilityService->App Locker and Open it」，指向的名称与列表显示名 Smart AppLocker 不一致
- res/values/strings.xml · setting_item_service_enable（Applocker Server）/ service_running（Service is Running）—— 首页以「服务开关/服务运行中」形式表达无障碍授权
- assets/conf/set1.conf · task_name「打开Tes2辅助」「打开辅助7.0」「辅助防止关掉对话框」「设置防止卸载对话框」「桌面防卸载」—— 任务名称本身构成流程说明，驱动跳转与自动点击时序
- Manifest 服务 MyAccessibilityServiceTmp 未声明 android:label —— 系统列表条目名称回退为 @string/app_name「Smart AppLocker」

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | The service for the purpose of Android 4.0.3 and above to lock apps easily. | 本服务用于在 Android 4.0.3 及以上系统中轻松锁定应用。 | `res/values/strings.xml key=accessibility_service_description（被 res/xml/phone_accessibility.xml 的 android:description 引用）` | 隐私承诺 |
| en | This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. | 本机版本高于 Android 4.0.3，请前往 设置->无障碍服务->App Locker 并开启它。 | `res/values/strings.xml key=alp_42447968_cmd_android_m_above` | 受限设置分步教学 |
| en | Find Setting->AccessibilityService->App Locker and Open it. | 找到 设置->无障碍服务->App Locker 并开启它。 | `res/values/strings.xml key=alp_42447968_cmd_android_m_above_toast` | 受限设置分步教学 |
| en | Get It | 知道了 / 开始（遮罩层唯一按钮，无取消） | `res/values/strings.xml key=str_get_it，用于 res/layout/hint_set_accessibility.xml 的 btn_get` | 受限设置分步教学 |
| en | Applocker Server | Applocker 服务（首页以服务开关形式暗示需开启无障碍） | `res/values/strings.xml key=setting_item_service_enable` | 清理工具伪装 |
| en | Service is Running | 服务正在运行 | `res/values/strings.xml key=service_running` | 良性透明说明 |
| zh | 打开辅助7.0 / 辅助防止关掉对话框 / 设置防止卸载对话框 / 桌面防卸载 / 打开未知来源 / 6.0自动安装 / 停止360security | 开启辅助（无障碍）7.0 / 自动取消无障碍关闭警告 / 自动取消卸载确认 / 桌面防卸载 / 开启未知来源 / 6.0 自动安装 / 终止 360 安全软件 | `assets/conf/set1.conf 任务表 task_name 字段（明文 JSON，未加密）` | 教唆忽视警告 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：拒绝或返回后不降级：配置任务表以 intent_time=1500ms 定时重新拉起 open_accessibility，并在 com.android.settings 后台持续执行 as_dialog（bgAsprotectDialog）识别「关闭无障碍」警告弹窗标题与内容后 click_cancel_enter 自动点「取消」，使关闭动作无法完成；另有 7.0辅助防止关掉 分支覆盖 Android 7.0，桌面防卸载 与 设置防止卸载对话框 覆盖 com.android.packageinstaller 卸载确认
- **遮罩叠层 / 高仿系统设置页**：是。res/layout/hint_set_accessibility.xml 为 #aa000000 全屏半透明遮罩，叠放在系统无障碍设置页之上，内含 pic_accessibility_guide.gif 录屏与 Get It 按钮；非高仿系统开关页，而是覆盖式引导遮罩 + GIF 坐标指示
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion 24、minSdkVersion 19，样本面向 Android 4.4–7.x，配置中无 Android 13 受限设置或 Session 安装器教学分支）
- **获权后即时行为与防撤权机制**：有。获权后由无障碍服务自身执行 click_package_as_check 与 click_enter_must 代点系统「确定」；并长期在 com.android.settings 前台/后台监测 AlertDialog，自动点击「取消」阻止撤权；同时对 com.android.packageinstaller 卸载确认弹窗自动点取消，并配置 桌面防卸载、识别取消的对话框、识别警告的对话框 等任务阻断卸载路径
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到拉起 Settings.ACTION_ACCESSIBILITY_SETTINGS（或应用内点击「Applocker Server」开关）后，在 800–1500ms 窗口内立即抓屏——此即配置 intent_time=1500 触发的遮罩层与自动勾选序列重叠时刻；同时在用户尝试关闭无障碍/卸载时抓取系统 AlertDialog 上方的自动点击行为
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：主要盲区：pic_accessibility_guide.gif 内的操作指示为纯图像无文本，UTG 只能取到 Get It 文本与图像区域，需截图/OCR 或图像差分留证；assets/conf/set1.conf 的任务解释器位于 360 加固 DEX，静态无法确认配置读取点与触发时机，须以运行期观测为准。静态加壳不阻挡运行期 UTG，遮罩层与系统设置页仍可正常抓取。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转后叠放的遮罩引导页（最关键）** | 系统无障碍详情页之上出现 #aa000000 全屏半透明层，含 GIF 动画与 Get It 文字按钮；窗口层级可见 pl.droidsonroids.gif.GifImageView 或应用 overlay 窗口 | 这是唯一能把「引导」与「自动勾选」两阶段区分开的画面，可直接证明遮罩式教学而非用户自行操作 | 半透明遮罩上的 Get It 文本节点；GIF 图像区域（无文本，需图像差分或截图留证）；系统无障碍页与遮罩同时存在（双窗口层级） |
| **系统无障碍服务列表项** | 条目名为 Smart AppLocker，进入详情后描述为 The service for the purpose of Android 4.0.3 and above to lock apps easily. | 核对引导文案所称 App Locker 与列表实际显示名不一致的身份混淆证据，并记录服务声明的宽泛能力 | 列表条目文本 Smart AppLocker；详情页描述文本 accessibility_service_description；开关状态的自动翻转（用户未操作却变为开启） |
| **拒权/撤权对抗页** | com.android.settings 或 com.android.packageinstaller 的 android.app.AlertDialog 上方，弹窗在无用户输入情况下自动消失（点到「取消」） | 证明存在自动点取消的撤权阻断，而非良性安全降级 | AlertDialog 出现后短时间内自动消失且开关保持开启；弹窗出现时无障碍服务处于运行状态；同屏出现应用 overlay 窗口 |
| **首页服务开关诱导页** | com.goami.applocker.AppLocker.ApplicationListActivity 中的 Applocker Server 开关项与 Service is Running 状态文本 | 确认触发时点为功能开关点击（user_feature_on_demand），而非冷启动直弹 | Applocker Server 文本节点；Service is Running 状态文本；点击开关后紧接 Settings 页拉起 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `#1 manifest:components（service com.goami.applocker.AppLocker.MyAccessibilityServiceTmp，无 android:label）`
- `res/xml/phone_accessibility.xml（typeAllMask + canRetrieveWindowContent + canRequestFilterKeyEvents + @string/accessibility_service_description）`
- `res/layout/hint_set_accessibility.xml（#aa000000 全屏遮罩 + GifImageView + @string/str_get_it）`
- `res/values/strings.xml（accessibility_service_description / alp_42447968_cmd_android_m_above / alp_42447968_cmd_android_m_above_toast / str_get_it）`
- `assets/conf/set1.conf（task accessibility_7：open_accessibility → check_package_as_check_close_7.0 → click_package_as_check → click_enter_must；task bgAsprotectDialog：click_cancel_enter）`
- `res/drawable-xxhdpi-v4/pic_accessibility_guide.gif（298KB 操作录屏指引）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论

已完成定向核验（12 次工具调用）。核心判断：该应用的“引导开启无障碍”**不是常规的弹窗劝说，而是配置驱动的自动化流程**——明文 JSON 任务表指定跳转与点击脚本，遮罩 GIF 负责教学，勾选动作由无障碍服务自己完成，并对用户的撤权/卸载警告自动点“取消”。

- **身份不一致**：桌面名 `Smart AppLocker`，包名 `com.agomi.applocker`，代码命名空间 `com.goami.applocker`（字母互换）；无障碍服务无 `android:label`，系统列表显示 “Smart AppLocker”，但引导文案要求用户找 “App Locker”（[alp_42447968_cmd_android_m_above](<resource-unit:#1 file:res/values/strings.xml#L22>)）。
- **声明过宽**：[phone_accessibility.xml](<resource-unit:#1 file:res/xml/phone_accessibility.xml>) 为 `typeAllMask` + `canRetrieveWindowContent` + `canRequestFilterKeyEvents`，而 [服务描述](<resource-unit:#1 file:res/values/strings.xml#L21>) 只说“lock apps easily”。
- **引导链**：[set1.conf](<resource-unit:#1 file:assets/conf/set1.conf>) 中 `打开辅助7.0`（`task_type: accessibility`，`intent_time: 1500`）动作序列 `open_accessibility → check_package_as_check_close_7.0 → click_package_as_check → click_enter_must`，按 ROM 分流（normal/6.0+/7.0+/meizu/samsung/oppo/vivo）。
- **载体**：[hint_set_accessibility.xml](<resource-unit:#1 file:res/layout/hint_set_accessibility.xml>) 为 `#aa000000` 全屏半透明遮罩 + [pic_accessibility_guide.gif](<resource-unit:#1 file:res/drawable-xxhdpi-v4/pic_accessibility_guide.gif>)（298KB 录屏）+ `Get It` 按钮，跳设置后压栈。
- **拒权不降级**：`辅助防止关掉对话框`（`as_dialog`，监听 `com.android.settings` 的 `android.app.AlertDialog`，`click_cancel_enter`）、`设置防止卸载对话框`、`桌面防卸载`——自动点取消阻止撤权。
- **能力外溢**：同表含 `打开未知来源`、`6.0/4.4自动安装`、`停止360security/lbe/cclear`、`gp打星星`、`搜集用户google信息`。
- **可见性边界**：DEX 为 360 加固（`com.stub.StubApp` + `assets/libjiagu*.so`），`com.luna.powersaver.gp` / `com.wuli.go.KaService` 执行体与 `assets/slogan.gpt`（ZIP）不可静态还原；配置解释器实现未静态确认，判定依据为明文配置与资源。

已登记风险 **R-001**（high / privacy_spyware）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "DEX 主体被 360 加固（com.stub.StubApp 入口 + assets/libjiagu.so、libjiagu_a64/x64/x86/ls.so），com.goami.applocker.* 与 com.luna.powersaver.gp、com.wuli.go.KaService 的实际执行代码不可静态还原；assets/slogan.gpt 为 4.1MB ZIP 容器未解包。但无障碍引导与自动化流程以明文 JSON（assets/conf/set1.conf，76KB 未加密）、无障碍配置 XML、遮罩布局与 GIF 资源形式完整可见，运行期页面流转可据此还原；配置解释器（读取 set1.conf 并执行 action 的代码）位于加密 DEX，未静态确认。",
  "summary_one_liner": "以明文 JSON 任务表驱动、按 ROM/版本分流跳转系统无障碍设置页，用全屏半透明遮罩加录屏 GIF 与 Get It 按钮教学，随后由无障碍服务自动勾选并点确定，同时对关闭/卸载警告自动点取消阻止撤权。",
  "disguise_identity": {
    "app_display_name": "Smart AppLocker",
    "claimed_brand_or_persona": "通用「Smart AppLocker」应用锁工具（自称仅用于锁定应用），引导文案另称「App Locker」",
    "a11y_service_label": "Smart AppLocker（服务未声明 android:label，系统列表回退为应用名 app_name）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未设 android:label，系统列表显示 Smart AppLocker，而 strings 引导文案让用户去找「App Locker」，名称不吻合；包名 com.agomi.applocker 与代码命名空间 com.goami.applocker 字母互换（agomi/goami）；LAUNCHER 入口为壳的 com.stub.stub01.Stub01 而非真实首屏 ApplicationListActivity；服务描述仅称 lock apps easily，隐藏自动点击与安装器代点能力"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.stub.stub01.Stub01（LAUNCHER）→ com.goami.applocker.AppLocker.ApplicationListActivity（真实首屏，singleInstance、excludeFromRecents）",
      "trigger_event": "点击桌面图标，MAIN/LAUNCHER intent 进入壳 Activity 后跳转真实首页",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Smart AppLocker",
      "shown_text_zh": "应用名「Smart AppLocker」（桌面与标题栏）",
      "user_action_requested": "无（正常进入应用列表首页，可选勾选要锁定的应用）",
      "code_anchor": "com.goami.applocker.AppLocker.ApplicationListActivity / @string/app_name"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "ApplicationListActivity 首页锁定开关 / 设置项 setting_item_service_enable",
      "trigger_event": "用户打开应用锁开关或选择任一待锁定应用时，检测无障碍服务未启用",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Applocker Server / Service is Running",
      "shown_text_zh": "「Applocker 服务」/「服务正在运行」——以服务开关形式表达无障碍授权需求",
      "user_action_requested": "点击开关开启保护（触发后续无障碍引导）",
      "code_anchor": "res/values/strings.xml setting_item_service_enable / service_running"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "全屏半透明遮罩层（res/layout/hint_set_accessibility.xml，GifImageView + btn_get）",
      "trigger_event": "配置任务 open_accessibility 执行，或检测到无障碍未开启时叠加遮罩",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Get It（@string/str_get_it）；背景为 pic_accessibility_guide.gif 操作录屏；系统无障碍列表项说明：The service for the purpose of Android 4.0.3 and above to lock apps easily.",
      "shown_text_zh": "「知道了/开始」按钮；配合 GIF 演示如何进入系统设置勾选；服务说明称「用于 Android 4.0.3 及以上轻松锁定应用的服务」",
      "user_action_requested": "点击 Get It 进入系统无障碍设置页（无取消/跳过按钮，遮罩 #aa000000 全屏覆盖）",
      "code_anchor": "res/layout/hint_set_accessibility.xml / res/drawable-xxhdpi-v4/pic_accessibility_guide.gif / @string/str_get_it"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 · 无障碍服务列表（Settings.ACTION_ACCESSIBILITY_SETTINGS）",
      "trigger_event": "set1.conf 任务「打开辅助7.0」（id accessibility_7，intent_time 1500ms）或「打开Tes2辅助」（id accessibility）中的 open_accessibility 动作",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it. / Find Setting->AccessibilityService->App Locker and Open it.",
      "shown_text_zh": "「本机版本高于 Android 4.0.3，请前往 设置->无障碍服务->App Locker 并开启它。」（提示语指向的 App Locker 与列表实际显示的 Smart AppLocker 不一致）",
      "user_action_requested": "按提示在列表中找到条目并进入服务详情页开启（点击动作随后由程序自动完成）",
      "code_anchor": "res/values/strings.xml alp_42447968_cmd_android_m_above / alp_42447968_cmd_android_m_above_toast；assets/conf/set1.conf 任务 accessibility_7"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "无障碍服务详情页之上叠放的 hint_set_accessibility 遮罩（跳转后 intent_time 1500ms 拉起）",
      "trigger_event": "进入设置页后按 intent_time=1500ms 定时触发遮罩与自动点击序列",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Get It；pic_accessibility_guide.gif（逐帧演示点击「Smart AppLocker」条目与开关位置）",
      "shown_text_zh": "「Get It」按钮 + GIF 动画指示应点击的条目与开关坐标",
      "user_action_requested": "照 GIF 指示点击服务条目与开关（遮罩全屏覆盖，无关闭入口）",
      "code_anchor": "assets/conf/set1.conf action: check_package_as_check_close_7.0 / res/layout/hint_set_accessibility.xml"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "MyAccessibilityServiceTmp 自动执行 click_package_as_check → click_enter_must；随后任务表转入 usage_access / notify / unknown_source 等分支",
      "trigger_event": "无障碍服务连接成功后，配置解释器依 rom 字段继续执行后续任务",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "click_package_as_check / click_enter_must / check_package_as_check_close_7.0（配置动作标识，非界面文案）；界面层为系统无障碍详情页的开关与「确定」弹窗",
      "shown_text_zh": "由服务自身在无障碍详情页勾选服务并点击系统「确定」按钮完成授权，无需用户手动点击",
      "user_action_requested": "无（授权动作由程序代劳）；用户仅在弹窗出现时被要求忽略或确认",
      "code_anchor": "assets/conf/set1.conf 任务 accessibility_7 action 列表 / #1 manifest:components 服务 MyAccessibilityServiceTmp"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.android.settings 的 android.app.AlertDialog（关闭无障碍警告）与 com.android.packageinstaller 的 android.app.AlertDialog（卸载确认）",
      "trigger_event": "用户在设置页尝试关闭无障碍或卸载时，后台任务 as_dialog / setting_dialog 被触发（background=true）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "check_dialog_title_is_want → check_dialog_content_is_want → click_cancel_enter（配置动作标识）；界面为系统「关闭此无障碍服务？」类警告弹窗",
      "shown_text_zh": "识别系统警告弹窗标题与内容后自动点击「取消」，使关闭无障碍/卸载操作无法完成",
      "user_action_requested": "用户被要求确认关闭或卸载，但确认路径被自动点击「取消」阻断；配置中无跳过或降级选项",
      "code_anchor": "assets/conf/set1.conf 任务 bgAsprotectDialog（as_dialog）/ bgSettingUninstallDialog（setting_dialog）/ 桌面防卸载"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml · accessibility_service_description —— 系统无障碍列表/详情页显示的服务说明：「The service for the purpose of Android 4.0.3 and above to lock apps easily.」",
    "res/xml/phone_accessibility.xml —— android:description 引用上述字符串，声明 typeAllMask + canRetrieveWindowContent + canRequestFilterKeyEvents",
    "res/layout/hint_set_accessibility.xml —— #aa000000 全屏半透明遮罩内的 GifImageView（pic_accessibility_guide.gif）与 Get It 按钮，跳设置页后压栈叠放",
    "res/drawable-xxhdpi-v4/pic_accessibility_guide.gif —— 298KB 逐帧操作录屏，以图像方式演示在系统设置中勾选服务，无文字",
    "res/values/strings.xml · alp_42447968_cmd_android_m_above / alp_42447968_cmd_android_m_above_toast —— 提示用户「Go Setting->AccessibilityService->App Locker and Open it」，指向的名称与列表显示名 Smart AppLocker 不一致",
    "res/values/strings.xml · setting_item_service_enable（Applocker Server）/ service_running（Service is Running）—— 首页以「服务开关/服务运行中」形式表达无障碍授权",
    "assets/conf/set1.conf · task_name「打开Tes2辅助」「打开辅助7.0」「辅助防止关掉对话框」「设置防止卸载对话框」「桌面防卸载」—— 任务名称本身构成流程说明，驱动跳转与自动点击时序",
    "Manifest 服务 MyAccessibilityServiceTmp 未声明 android:label —— 系统列表条目名称回退为 @string/app_name「Smart AppLocker」"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "The service for the purpose of Android 4.0.3 and above to lock apps easily.",
      "text_zh": "本服务用于在 Android 4.0.3 及以上系统中轻松锁定应用。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（被 res/xml/phone_accessibility.xml 的 android:description 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "This device version is above Android 4.0.3 .Please Go Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "本机版本高于 Android 4.0.3，请前往 设置->无障碍服务->App Locker 并开启它。",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_android_m_above",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Find Setting->AccessibilityService->App Locker and Open it.",
      "text_zh": "找到 设置->无障碍服务->App Locker 并开启它。",
      "source_location": "res/values/strings.xml key=alp_42447968_cmd_android_m_above_toast",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Get It",
      "text_zh": "知道了 / 开始（遮罩层唯一按钮，无取消）",
      "source_location": "res/values/strings.xml key=str_get_it，用于 res/layout/hint_set_accessibility.xml 的 btn_get",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Applocker Server",
      "text_zh": "Applocker 服务（首页以服务开关形式暗示需开启无障碍）",
      "source_location": "res/values/strings.xml key=setting_item_service_enable",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Service is Running",
      "text_zh": "服务正在运行",
      "source_location": "res/values/strings.xml key=service_running",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "打开辅助7.0 / 辅助防止关掉对话框 / 设置防止卸载对话框 / 桌面防卸载 / 打开未知来源 / 6.0自动安装 / 停止360security",
      "text_zh": "开启辅助（无障碍）7.0 / 自动取消无障碍关闭警告 / 自动取消卸载确认 / 桌面防卸载 / 开启未知来源 / 6.0 自动安装 / 终止 360 安全软件",
      "source_location": "assets/conf/set1.conf 任务表 task_name 字段（明文 JSON，未加密）",
      "rhetorical_frame": "教唆忽视警告"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "拒绝或返回后不降级：配置任务表以 intent_time=1500ms 定时重新拉起 open_accessibility，并在 com.android.settings 后台持续执行 as_dialog（bgAsprotectDialog）识别「关闭无障碍」警告弹窗标题与内容后 click_cancel_enter 自动点「取消」，使关闭动作无法完成；另有 7.0辅助防止关掉 分支覆盖 Android 7.0，桌面防卸载 与 设置防止卸载对话框 覆盖 com.android.packageinstaller 卸载确认",
    "overlay_or_fake_settings": "是。res/layout/hint_set_accessibility.xml 为 #aa000000 全屏半透明遮罩，叠放在系统无障碍设置页之上，内含 pic_accessibility_guide.gif 录屏与 Get It 按钮；非高仿系统开关页，而是覆盖式引导遮罩 + GIF 坐标指示",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion 24、minSdkVersion 19，样本面向 Android 4.4–7.x，配置中无 Android 13 受限设置或 Session 安装器教学分支）",
    "post_grant_anti_removal": "有。获权后由无障碍服务自身执行 click_package_as_check 与 click_enter_must 代点系统「确定」；并长期在 com.android.settings 前台/后台监测 AlertDialog，自动点击「取消」阻止撤权；同时对 com.android.packageinstaller 卸载确认弹窗自动点取消，并配置 桌面防卸载、识别取消的对话框、识别警告的对话框 等任务阻断卸载路径",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到拉起 Settings.ACTION_ACCESSIBILITY_SETTINGS（或应用内点击「Applocker Server」开关）后，在 800–1500ms 窗口内立即抓屏——此即配置 intent_time=1500 触发的遮罩层与自动勾选序列重叠时刻；同时在用户尝试关闭无障碍/卸载时抓取系统 AlertDialog 上方的自动点击行为",
    "key_pages_to_capture": [
      {
        "page_role": "跳转后叠放的遮罩引导页（最关键）",
        "page_identifier": "系统无障碍详情页之上出现 #aa000000 全屏半透明层，含 GIF 动画与 Get It 文字按钮；窗口层级可见 pl.droidsonroids.gif.GifImageView 或应用 overlay 窗口",
        "why_most_useful": "这是唯一能把「引导」与「自动勾选」两阶段区分开的画面，可直接证明遮罩式教学而非用户自行操作",
        "observable_utg_signals": ["半透明遮罩上的 Get It 文本节点", "GIF 图像区域（无文本，需图像差分或截图留证）", "系统无障碍页与遮罩同时存在（双窗口层级）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "条目名为 Smart AppLocker，进入详情后描述为 The service for the purpose of Android 4.0.3 and above to lock apps easily.",
        "why_most_useful": "核对引导文案所称 App Locker 与列表实际显示名不一致的身份混淆证据，并记录服务声明的宽泛能力",
        "observable_utg_signals": ["列表条目文本 Smart AppLocker", "详情页描述文本 accessibility_service_description", "开关状态的自动翻转（用户未操作却变为开启）"]
      },
      {
        "page_role": "拒权/撤权对抗页",
        "page_identifier": "com.android.settings 或 com.android.packageinstaller 的 android.app.AlertDialog 上方，弹窗在无用户输入情况下自动消失（点到「取消」）",
        "why_most_useful": "证明存在自动点取消的撤权阻断，而非良性安全降级",
        "observable_utg_signals": ["AlertDialog 出现后短时间内自动消失且开关保持开启", "弹窗出现时无障碍服务处于运行状态", "同屏出现应用 overlay 窗口"]
      },
      {
        "page_role": "首页服务开关诱导页",
        "page_identifier": "com.goami.applocker.AppLocker.ApplicationListActivity 中的 Applocker Server 开关项与 Service is Running 状态文本",
        "why_most_useful": "确认触发时点为功能开关点击（user_feature_on_demand），而非冷启动直弹",
        "observable_utg_signals": ["Applocker Server 文本节点", "Service is Running 状态文本", "点击开关后紧接 Settings 页拉起"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "主要盲区：pic_accessibility_guide.gif 内的操作指示为纯图像无文本，UTG 只能取到 Get It 文本与图像区域，需截图/OCR 或图像差分留证；assets/conf/set1.conf 的任务解释器位于 360 加固 DEX，静态无法确认配置读取点与触发时机，须以运行期观测为准。静态加壳不阻挡运行期 UTG，遮罩层与系统设置页仍可正常抓取。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "#1 manifest:components（service com.goami.applocker.AppLocker.MyAccessibilityServiceTmp，无 android:label）",
    "res/xml/phone_accessibility.xml（typeAllMask + canRetrieveWindowContent + canRequestFilterKeyEvents + @string/accessibility_service_description）",
    "res/layout/hint_set_accessibility.xml（#aa000000 全屏遮罩 + GifImageView + @string/str_get_it）",
    "res/values/strings.xml（accessibility_service_description / alp_42447968_cmd_android_m_above / alp_42447968_cmd_android_m_above_toast / str_get_it）",
    "assets/conf/set1.conf（task accessibility_7：open_accessibility → check_package_as_check_close_7.0 → click_package_as_check → click_enter_must；task bgAsprotectDialog：click_cancel_enter）",
    "res/drawable-xxhdpi-v4/pic_accessibility_guide.gif（298KB 操作录屏指引）"
  ]
}
```

</details>
