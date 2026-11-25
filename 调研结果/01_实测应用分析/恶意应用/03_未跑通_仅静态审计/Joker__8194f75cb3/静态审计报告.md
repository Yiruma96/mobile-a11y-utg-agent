# MR_077__8194f75cb3｜Joker — Assistive Touch Control Centre

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：128.4s

## 1. 一句话核心结论

- **核心申请方式**：以 iOS 风格“Assistive Touch Control Centre”辅助触控工具为外壳，用系统无障碍列表中的“全局动作+不会收集任何个人信息”说明与“Find and activate Assistive Touch to use this feature”功能门槛文案引导用户开启无障碍服务，真实跳转/遮罩/拒权重试逻辑被爱加密壳加密，需运行期 UTG 取证。
- **静态可见性说明**：Manifest、res/xml/accessibilityservice.xml 与全部 strings 资源静态可见；但应用被爱加密（ijiami）壳保护（application=s.h.e.l.l.S、appComponentFactory=s.h.e.l.l.A、assets/ijiami.ajm + assets/ijm_lib/*/libexec.so），所有应用自身类方法体为空（CheckPerDungnv.onCreate、AccessibilityServiceDungnv.onServiceConnected/onAccessibilityEvent/onInterrupt 均无实现），classes.dex 中搜索 ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS / str_active_per / per_accessibility 均无代码命中，因此跳转逻辑、引导弹窗时序、悬浮遮罩与获权后动作均藏于运行期解密的加密载荷，静态不可还原。
- **命中的行为模式标签**：`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8194f75cb34b742837b35c5693f5f2b95f518e34b2e0bd95c63075dd3cc8f0fb` |
| 包名 / 年份 | `com.kong.toouch.ass.iphoea` / 2021 |
| 家族 / 品类 | **Joker**（同池样本数：4） |
| 原始来源标识 | https://therecord.media/android-malware-found-on-huaweis-official-app-store/ |
| 桌面显示名 | Assistive Touch Control Centre |
| 引导页宣称品牌/身份 | iOS AssistiveTouch（苹果风格辅助触控球/控制中心） |
| 系统无障碍列表服务名 | 服务自身未设 android:label，系统无障碍列表以应用名“Assistive Touch Control Centre”显示，说明/摘要文本为 per_accessibility（Enable Accessibility Service to perform a global action…） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：爱加密壳（s.h.e.l.l.S / s.h.e.l.l.A + ijiami.ajm + libexec.so）隐藏全部真实逻辑；多个 Activity 使用 android:label="" 空标签（HelpActivity、DialogRateActivity、TransparentActivity）；SplashActivity 额外挂 category.HOME 可冒充桌面；存在两份未被引用的 accessibility_service*.xml 并把 packageNames 指向别家 assistivetouch 包；未声明 isAccessibilityTool 之类的显式标记 |
| 无障碍服务类名 | `com.kong.toouch.ass.iphoea.activity.AccessibilityServiceDungnv` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：easytouch.easytouch.assistivetouch.assistivetouch.service, easytouch.easytouch.assistivetouch.assistivetouch.service |
| 共现高危权限 | `CAMERA, RECORD_AUDIO, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Enable Accessibility Service to perform a global action. For example Going Back, Opening Power popup, Opening Notification Center, Opening Recent, etc.<br>Please be assured that Assistive Touch will not collect any personal information. / Enable Accessibility Service to perform a global action. For example Going Back, Opening Power popup, Opening Notification Center, Opening Recent, etc.<br>Please be assured that Assistive Touch will not collect any personal information. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.das.nosd.SplashActivity（MAIN/LAUNCHER，另含 category.HOME），随后启动 com.das.nosd.WelcomeGuildActivity（NoTitleTranslucentTheme 半透明引导页） | onCreate / 冷启动点击桌面图标 | 原生Activity | **原文**：无（引导页文案位于加密载荷，静态不可见）<br>**译注**：启动闪屏后进入半透明引导页；具体文案不可静态还原 | 不可静态确认（预筛线索指向冷启动即引导开启无障碍） | `com.das.nosd.SplashActivity / com.das.nosd.WelcomeGuildActivity（Manifest 声明，类体在壳内）` |
| 2 | 引导说明页 | HelpActivity（@style/DialogStyle，android:label=""）、DialogHelpPerDungnv、DialogPerDungnv、CheckPerDungnv | 不可静态确认（预筛 JUMP_A11Y_SETTINGS 表明存在引导后跳转） | 原生Dialog | **原文**：Find and activate "<b>Assistive Touch</b>" to use this feature / Activation failed. Go to Settings > Permissions, then allow the following right and try again:<br>**译注**：“找到并激活 Assistive Touch 才能使用该功能”；“激活失败，请前往 设置 > 权限，允许下列权限后重试：” | 前往设置找到并开启 Assistive Touch 服务（资源中未见“跳过/稍后再说”类字符串） | `res/values/strings.xml#str_active_per；res/values/strings.xml#perm_title；com.kong.toouch.ass.iphoea.activity.CheckPerDungnv` |
| 3 | 跳无障碍设置 | 系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS），由加密载荷中的跳转代码拉起 | 不可静态确认（预筛 DEX 线索 JUMP_A11Y_SETTINGS） | 系统无障碍页 | 无 | 在系统列表中手动开启无障碍开关（是否伴随悬浮遮罩指引不可静态确认） | `预筛线索 JUMP_A11Y_SETTINGS（代码位于加密载荷，classes.dex 无明文命中）` |
| 4 | 遮罩叠层指引 | 悬浮窗/引导遮罩（HomeServiceDungnv 前台服务 + SYSTEM_ALERT_WINDOW；预筛 A11Y_OVERLAY） | 不可静态确认（预筛线索 A11Y_OVERLAY + WATCH_SETTINGS） | 悬浮窗Overlay | **原文**：无（遮罩文案不可静态还原；相关资源存在 notifi_touch_dot_is_here_title="Assistive Touch in here"）<br>**译注**：在系统设置页上叠加半透明指引/提示“Assistive Touch 在这里” | 按遮罩指引点击系统无障碍开关（不可静态确认） | `com.kong.toouch.ass.iphoea.activity.service.HomeServiceDungnv；res/values/strings.xml#notifi_touch_dot_is_here_title` |
| 5 | 系统无障碍列表项 | 系统无障碍服务列表条目：AccessibilityServiceDungnv（进程 :QuickTouchService） | 用户进入系统无障碍设置 | 系统无障碍页 | **原文**：Enable Accessibility Service to perform a global action. For example Going Back, Opening Power popup, Opening Notification Center, Opening Recent, etc.<br>Please be assured that Assistive Touch will not collect any personal information.<br>**译注**：“启用无障碍服务以执行全局操作，例如返回、打开电源菜单、打开通知中心、打开最近任务等。请放心，Assistive Touch 不会收集任何个人信息。” | 在系统列表中打开该服务开关 | `res/xml/accessibilityservice.xml；res/values/strings.xml#per_accessibility；Manifest 中 service com.kong.toouch.ass.iphoea.activity.AccessibilityServiceDungnv` |
| 6 | 拒权反馈循环 | 不可静态还原（预筛 WATCH_SETTINGS 提示监听设置页状态；资源层仅有 perm_title 重试文案） | 用户返回应用 / 未开启服务（onResume 或轮询，具体实现位于加密载荷） | 不可静态还原 | **原文**：Activation failed. Go to Settings > Permissions, then allow the following right and try again:<br>**译注**：“激活失败。请前往 设置 > 权限，允许下列权限后重试：” | 再次前往设置授权（是否死循环重跳不可静态确认） | `res/values/strings.xml#perm_title；预筛线索 WATCH_SETTINGS` |
| 7 | 获权后动作 | AccessibilityServiceDungnv.onServiceConnected（空壳）→ 实际逻辑在解密载荷；配套 HomeServiceDungnv 悬浮球、NotifyServiceDungnv 通知监听、MyDeviceAdminReceiverDungnv 设备管理器 | 系统回调 onServiceConnected / onAccessibilityEvent | 不可静态还原 | 无 | 无（后台自动执行） | `com.kong.toouch.ass.iphoea.activity.AccessibilityServiceDungnv#onServiceConnected（方法体为空，实现在壳内）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表条目：android:description / android:summary = @string/per_accessibility（res/xml/accessibilityservice.xml），即“Enable Accessibility Service to perform a global action…Please be assured that Assistive Touch will not collect any personal information.”
- 功能门槛提示文案：res/values/strings.xml#str_active_per（含 <b>Assistive Touch</b> 富文本加粗），另有 values-in（印尼语）、values-vi-rVN（越南语）本地化版本，通常渲染于功能被禁用时的原生 Dialog/提示
- 授权失败重试提示：res/values/strings.xml#perm_title（“Activation failed. Go to Settings > Permissions…”），出现在 CheckPerDungnv / DialogPerDungnv / DialogHelpPerDungnv 一类 DialogStyle 页
- 冷启动半透明引导页：com.das.nosd.WelcomeGuildActivity（NoTitleTranslucentTheme），文案在加密载荷内，静态不可见
- 悬浮提示：res/values/strings.xml#notifi_touch_dot_is_here_title（“Assistive Touch in here”），配合 HomeServiceDungnv 悬浮球/通知栏呈现
- 录屏/存储等附带权限说明：res/values/strings.xml#perm_camera_content / perm_micro_content / perm_storage_content（宣称“仅打开手电筒”“仅录屏录音”“仅保存视频图片”），与无障碍说明同属弱化权限敏感度的表述

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable Accessibility Service to perform a global action. For example Going Back, Opening Power popup, Opening Notification Center, Opening Recent, etc.<br>Please be assured that Assistive Touch will not collect any personal information. | 启用无障碍服务以执行全局操作。例如返回、打开电源菜单、打开通知中心、打开最近任务等。请放心，Assistive Touch 不会收集任何个人信息。 | `res/values/strings.xml key=per_accessibility（由 res/xml/accessibilityservice.xml 的 description/summary 引用）` | 隐私承诺 |
| en | Find and activate "<b>Assistive Touch</b>" to use this feature | 请找到并激活“Assistive Touch”以使用此功能 | `res/values/strings.xml key=str_active_per` | 受限设置分步教学 |
| vi | Tìm và kích hoạt "<b>Assistive Touch</b>" để sử dụng tính năng này | 请找到并激活“Assistive Touch”以使用此功能（越南语本地化） | `res/values-vi-rVN/strings.xml key=str_active_per` | 受限设置分步教学 |
| id | Temukan dan aktifkan <b> AssistiveTouch </b> untuk menggunakan fitur ini | 请找到并激活“AssistiveTouch”以使用此功能（印尼语本地化） | `res/values-in/strings.xml key=str_active_per` | 受限设置分步教学 |
| en | Activation failed. Go to Settings > Permissions, then allow the following right and try again: | 激活失败。请前往 设置 > 权限，允许以下权限后重试： | `res/values/strings.xml key=perm_title` | 受限设置分步教学 |
| en | - Only open the flashlight / - Use the microphone only to record sound when recording the screen / - Only save videos and images to memory | “仅用于打开手电筒”“麦克风仅用于录屏录音”“仅将视频与图片保存到存储” | `res/values/strings.xml key=perm_camera_content / perm_micro_content / perm_storage_content` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：具体实现位于爱加密加密载荷，静态不可确认。资源层可见的叙事是“激活失败→前往设置授权→重试”（perm_title），预筛线索 WATCH_SETTINGS 提示存在对设置页状态/服务启用状态的监听，符合返回后再次拉起引导的模式，但无法静态确认是 onResume 死循环还是定时器重跳。
- **遮罩叠层 / 高仿系统设置页**：不可静态还原。预筛线索 A11Y_OVERLAY 与已声明的 SYSTEM_ALERT_WINDOW、前台服务 HomeServiceDungnv（悬浮球/通知栏提示）表明具备在系统设置页上叠加悬浮指引的技术条件，遮罩具体形态（半透明引导层/高仿开关页）未在明文资源中出现。
- **Android 13+ 受限设置（Restricted Settings）应对**：预筛线索 RESTRICTED_STR 与 SESSION_INSTALLER 指向存在“受限设置/Session 安装器”相关字符串与调用，但均位于加密载荷，classes.dex 明文域无命中，无法静态逐字确认是否包含“进入应用详情→右上角菜单→允许受限设置”的分步教学。
- **获权后即时行为与防撤权机制**：不可静态还原。预筛线索 PERFORM_GLOBAL_ACTION 与 WATCH_SETTINGS 表明获权后具备执行全局返回/主页动作并监听设置页变化的能力，具备阻止撤权的技术条件；同时 Manifest 声明了设备管理器 MyDeviceAdminReceiverDungnv（BIND_DEVICE_ADMIN + device_policies_admin），可增加卸载/撤权阻力，但具体反撤权代码在壳内。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两条时机：①冷启动后 0–2 秒内（SplashActivity → WelcomeGuildActivity 半透明引导页出现时立即截图）；②运行期监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间（此时壳已解密，UTG 可捕获跳转前后页面），并在跳转后 800ms–1.5s 再补一次截图以捕捉可能压栈的悬浮遮罩。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区是爱加密壳：一阶段 DEX 方法体全空，静态预筛给出的 JUMP_A11Y_SETTINGS/RESTRICTED_STR/SESSION_INSTALLER/A11Y_OVERLAY/WATCH_SETTINGS 均只能靠运行期解密后 UTG 或内存 dump 验证；静态加壳本身不阻挡运行期 UTG。此外若加密载荷在判定为模拟器/调试环境后才加载引导逻辑，可能出现“真机有引导、分析环境无引导”的规避盲区，建议 UTG 采集时避免明显的 hook/调试痕迹并做 2 次冷启动对比。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导页 / 引导弹窗页** | com.das.nosd.WelcomeGuildActivity（半透明主题，叠加在闪屏或桌面上）、或 DialogStyle 的 HelpActivity/DialogHelpPerDungnv | 该页承载首次、强制的无障碍开启说明，最能判断是“良性透明说明”还是“伪造系统提示/教唆忽视警告”，且决定了 trigger_timing 是 cold_start_0_step 还是 user_feature_on_demand | 页面标题与正文全文（是否含 Assistive Touch 品牌宣称、隐私承诺句）；是否存在“取消/跳过/稍后”按钮及其可点击性；是否同时叠加系统设置界面（判断 fake settings 或遮罩）；页面包名/Activity 名是否为 com.kong.toouch.ass.iphoea 自身 |
| **系统无障碍服务列表项** | 设置 → 无障碍 中的应用条目“Assistive Touch Control Centre”，摘要为 per_accessibility 文本 | 用于核对系统层面呈现给用户的说明与真实能力差异（说明只讲返回/通知中心，实际声明通知监听、设备管理器、录屏、WRITE_SETTINGS），是身份/能力不匹配的客观证据 | 条目显示的应用名与描述原文；是否出现“此服务可查看屏幕内容/执行操作”类系统警示；是否被自动打开（自点确认） |
| **跳转后压栈遮罩页 / 拒权返回页** | 无障碍设置页之上的半透明悬浮层（HomeServiceDungnv 前台服务窗口），或返回应用后再次弹出的 DialogStyle 提示 | 决定是否存在 COERCE_OVERLAY_STACK_ON_SETTINGS 与 COERCE_REFUSAL_LOOP_RELAUNCH：是否在设置页上叠指引、返回未开启时是否立刻重跳 | 设置页上是否出现非系统 UI 的叠加窗口及箭头/手指图标；返回键后 1–3 秒内是否再次出现无障碍设置页（循环重跳）；叠加层文本是否含“点击此处打开/Allow”类指令；叠加层所属包名是否为 com.kong.toouch.ass.iphoea |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.kong.toouch.ass.iphoea.activity.AccessibilityServiceDungnv#onServiceConnected`
- `com.kong.toouch.ass.iphoea.activity.CheckPerDungnv#onCreate`
- `res/xml/accessibilityservice.xml`
- `res/values/strings.xml#per_accessibility`
- `res/values/strings.xml#str_active_per`
- `com.das.nosd.SplashActivity / com.das.nosd.WelcomeGuildActivity`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**1. 该应用由爱加密（ijiami）壳保护，真实引导逻辑在静态层面不可见**
- `AndroidManifest.xml` 中 `android:name="s.h.e.l.l.S"`、`android:appComponentFactory="s.h.e.l.l.A"`，并带有 `assets/ijiami.ajm`（292KB，`indl01` 魔数）与 `assets/ijm_lib/{arm64-v8a,armeabi,x86,x86_64}/libexec.so`。
- 反编译结果证实：应用自身类的**方法体全部为空**——`CheckPerDungnv.onCreate`、[AccessibilityServiceDungnv#onServiceConnected / onAccessibilityEvent / onInterrupt](<resource-unit:#1.dex1 code:com.kong.toouch.ass.iphoea.activity.AccessibilityServiceDungnv#onServiceConnected>) 均为空壳。
- 因此，`ACTION_ACCESSIBILITY_SETTINGS` 跳转点、引导弹窗文案、悬浮遮罩代码均**未以明文形式出现在 classes.dex 中**（全文搜索 `ACCESSIBILITY_SETTINGS`、`str_active_per`、`per_accessibility` 在代码域均无命中）。预筛给出的 `JUMP_A11Y_SETTINGS / RESTRICTED_STR / SESSION_INSTALLER / A11Y_OVERLAY / WATCH_SETTINGS` 属于运行期解密载荷中的行为，静态不可逐字还原。

**2. Manifest / 资源层可确认的“无障碍开启引导”骨架**
- 无障碍服务声明为 `AccessibilityServiceDungnv`，`android:process=":QuickTouchService"`，配置 [res/xml/accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml>)：`description=summary=@string/per_accessibility`，`accessibilityFeedbackType="feedbackAllMask"`（没有设置 `canRetrieveWindowContent`/`flagRetrieveInteractiveWindows` 等更细能力，属通用全量反馈）。
- 系统无障碍列表中呈现的说明即 [res/values/strings.xml `per_accessibility`](<resource-unit:#1 file:res/values/strings.xml#L193-L194>)：宣称仅用于“返回/电源菜单/通知中心/最近任务”等全局动作，并附加**“Assistive Touch 不会收集任何个人信息”的隐私承诺**。
- 引导文案资源 [res/values/strings.xml `str_active_per`](<resource-unit:#1 file:res/values/strings.xml#L252>)：“Find and activate **Assistive Touch** to use this feature”（含 `<b>` 富文本加粗品牌名，典型的功能门槛式引导），另有印尼语、越南语本地化，说明面向东南亚市场。
- 拒绝授权后的反馈文案 [res/values/strings.xml `perm_title`](<resource-unit:#1 file:res/values/strings.xml#L201>)：“Activation failed. Go to Settings > Permissions, then allow the following right and try again:”——即“激活失败→跳设置页→重试”的闭环叙事。
- 引导载体类（名字可证）：`com.das.nosd.SplashActivity`（LAUNCHER + 额外 `category.HOME`）、`com.das.nosd.WelcomeGuildActivity`（半透明主题 `NoTitleTranslucentTheme`）、`HelpActivity`/`DialogHelpPerDungnv`/`DialogPerDungnv`/`CheckPerDungnv`（均为 `DialogStyle` 或空 `android:label=""`）。

**3. 身份与能力不匹配（可疑点）**
- 自称 iOS 风格 “Assistive Touch Control Centre”，包名 `com.kong.toouch.ass.iphoea` 与 iOS/任何正规厂商无关联。
- 除辅助触控外还声明了通知监听（`NotifyServiceDungnv`、`com.das.nosd.AppService`）、**设备管理器**（`MyDeviceAdminReceiverDungnv` + `device_policies_admin`）、录屏、`WRITE_SETTINGS`、`KILL_BACKGROUND_PROCESSES`、`READ_PHONE_STATE`、`SYSTEM_ALERT_WINDOW` 等远超“辅助触控”的能力。
- 另存在一份未被 Manifest 引用的配置 `res/xml/accessibility_service.xml` / `accessibility_service_dungnv.xml`，其 `android:packageNames="easytouch.easytouch.assistivetouch.assistivetouch.service"`——把监听范围锁定在**另一款 AssistiveTouch 应用包**上，属同质竞品定向监视特征。

**4. 静态可见性判定**
`static_visibility = packed_or_encrypted`。Manifest、无障碍 xml 与全部多语言字符串可见且足以描述“系统层说明文本 + 引导文案 + 拒权重试叙事”；但**弹窗/Activity 流转顺序、遮罩叠层、受限设置教学、获权后反卸载**这些关键行为全部位于爱加密加密载荷，须靠运行期 UTG/动态分析取证。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、res/xml/accessibilityservice.xml 与全部 strings 资源静态可见；但应用被爱加密（ijiami）壳保护（application=s.h.e.l.l.S、appComponentFactory=s.h.e.l.l.A、assets/ijiami.ajm + assets/ijm_lib/*/libexec.so），所有应用自身类方法体为空（CheckPerDungnv.onCreate、AccessibilityServiceDungnv.onServiceConnected/onAccessibilityEvent/onInterrupt 均无实现），classes.dex 中搜索 ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS / str_active_per / per_accessibility 均无代码命中，因此跳转逻辑、引导弹窗时序、悬浮遮罩与获权后动作均藏于运行期解密的加密载荷，静态不可还原。",
  "summary_one_liner": "以 iOS 风格“Assistive Touch Control Centre”辅助触控工具为外壳，用系统无障碍列表中的“全局动作+不会收集任何个人信息”说明与“Find and activate Assistive Touch to use this feature”功能门槛文案引导用户开启无障碍服务，真实跳转/遮罩/拒权重试逻辑被爱加密壳加密，需运行期 UTG 取证。",
  "disguise_identity": {
    "app_display_name": "Assistive Touch Control Centre",
    "claimed_brand_or_persona": "iOS AssistiveTouch（苹果风格辅助触控球/控制中心）",
    "a11y_service_label": "服务自身未设 android:label，系统无障碍列表以应用名“Assistive Touch Control Centre”显示，说明/摘要文本为 per_accessibility（Enable Accessibility Service to perform a global action…）",
    "identity_mismatch": true,
    "obfuscation_tricks": "爱加密壳（s.h.e.l.l.S / s.h.e.l.l.A + ijiami.ajm + libexec.so）隐藏全部真实逻辑；多个 Activity 使用 android:label=\"\" 空标签（HelpActivity、DialogRateActivity、TransparentActivity）；SplashActivity 额外挂 category.HOME 可冒充桌面；存在两份未被引用的 accessibility_service*.xml 并把 packageNames 指向别家 assistivetouch 包；未声明 isAccessibilityTool 之类的显式标记"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.das.nosd.SplashActivity（MAIN/LAUNCHER，另含 category.HOME），随后启动 com.das.nosd.WelcomeGuildActivity（NoTitleTranslucentTheme 半透明引导页）",
      "trigger_event": "onCreate / 冷启动点击桌面图标",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（引导页文案位于加密载荷，静态不可见）",
      "shown_text_zh": "启动闪屏后进入半透明引导页；具体文案不可静态还原",
      "user_action_requested": "不可静态确认（预筛线索指向冷启动即引导开启无障碍）",
      "code_anchor": "com.das.nosd.SplashActivity / com.das.nosd.WelcomeGuildActivity（Manifest 声明，类体在壳内）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "HelpActivity（@style/DialogStyle，android:label=\"\"）、DialogHelpPerDungnv、DialogPerDungnv、CheckPerDungnv",
      "trigger_event": "不可静态确认（预筛 JUMP_A11Y_SETTINGS 表明存在引导后跳转）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Find and activate \"<b>Assistive Touch</b>\" to use this feature / Activation failed. Go to Settings > Permissions, then allow the following right and try again:",
      "shown_text_zh": "“找到并激活 Assistive Touch 才能使用该功能”；“激活失败，请前往 设置 > 权限，允许下列权限后重试：”",
      "user_action_requested": "前往设置找到并开启 Assistive Touch 服务（资源中未见“跳过/稍后再说”类字符串）",
      "code_anchor": "res/values/strings.xml#str_active_per；res/values/strings.xml#perm_title；com.kong.toouch.ass.iphoea.activity.CheckPerDungnv"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（android.settings.ACCESSIBILITY_SETTINGS），由加密载荷中的跳转代码拉起",
      "trigger_event": "不可静态确认（预筛 DEX 线索 JUMP_A11Y_SETTINGS）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "跳转目标为系统无障碍服务列表，需用户手动找到“Assistive Touch Control Centre”并打开开关",
      "user_action_requested": "在系统列表中手动开启无障碍开关（是否伴随悬浮遮罩指引不可静态确认）",
      "code_anchor": "预筛线索 JUMP_A11Y_SETTINGS（代码位于加密载荷，classes.dex 无明文命中）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "悬浮窗/引导遮罩（HomeServiceDungnv 前台服务 + SYSTEM_ALERT_WINDOW；预筛 A11Y_OVERLAY）",
      "trigger_event": "不可静态确认（预筛线索 A11Y_OVERLAY + WATCH_SETTINGS）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（遮罩文案不可静态还原；相关资源存在 notifi_touch_dot_is_here_title=\"Assistive Touch in here\"）",
      "shown_text_zh": "在系统设置页上叠加半透明指引/提示“Assistive Touch 在这里”",
      "user_action_requested": "按遮罩指引点击系统无障碍开关（不可静态确认）",
      "code_anchor": "com.kong.toouch.ass.iphoea.activity.service.HomeServiceDungnv；res/values/strings.xml#notifi_touch_dot_is_here_title"
    },
    {
      "step": 5,
      "stage": "系统无障碍列表项",
      "screen_or_component": "系统无障碍服务列表条目：AccessibilityServiceDungnv（进程 :QuickTouchService）",
      "trigger_event": "用户进入系统无障碍设置",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable Accessibility Service to perform a global action. For example Going Back, Opening Power popup, Opening Notification Center, Opening Recent, etc.\nPlease be assured that Assistive Touch will not collect any personal information.",
      "shown_text_zh": "“启用无障碍服务以执行全局操作，例如返回、打开电源菜单、打开通知中心、打开最近任务等。请放心，Assistive Touch 不会收集任何个人信息。”",
      "user_action_requested": "在系统列表中打开该服务开关",
      "code_anchor": "res/xml/accessibilityservice.xml；res/values/strings.xml#per_accessibility；Manifest 中 service com.kong.toouch.ass.iphoea.activity.AccessibilityServiceDungnv"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "不可静态还原（预筛 WATCH_SETTINGS 提示监听设置页状态；资源层仅有 perm_title 重试文案）",
      "trigger_event": "用户返回应用 / 未开启服务（onResume 或轮询，具体实现位于加密载荷）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Activation failed. Go to Settings > Permissions, then allow the following right and try again:",
      "shown_text_zh": "“激活失败。请前往 设置 > 权限，允许下列权限后重试：”",
      "user_action_requested": "再次前往设置授权（是否死循环重跳不可静态确认）",
      "code_anchor": "res/values/strings.xml#perm_title；预筛线索 WATCH_SETTINGS"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "AccessibilityServiceDungnv.onServiceConnected（空壳）→ 实际逻辑在解密载荷；配套 HomeServiceDungnv 悬浮球、NotifyServiceDungnv 通知监听、MyDeviceAdminReceiverDungnv 设备管理器",
      "trigger_event": "系统回调 onServiceConnected / onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后执行全局动作（PERFORM_GLOBAL_ACTION）、监听设置页（WATCH_SETTINGS）等；具体动作序列不可静态还原",
      "user_action_requested": "无（后台自动执行）",
      "code_anchor": "com.kong.toouch.ass.iphoea.activity.AccessibilityServiceDungnv#onServiceConnected（方法体为空，实现在壳内）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表条目：android:description / android:summary = @string/per_accessibility（res/xml/accessibilityservice.xml），即“Enable Accessibility Service to perform a global action…Please be assured that Assistive Touch will not collect any personal information.”",
    "功能门槛提示文案：res/values/strings.xml#str_active_per（含 <b>Assistive Touch</b> 富文本加粗），另有 values-in（印尼语）、values-vi-rVN（越南语）本地化版本，通常渲染于功能被禁用时的原生 Dialog/提示",
    "授权失败重试提示：res/values/strings.xml#perm_title（“Activation failed. Go to Settings > Permissions…”），出现在 CheckPerDungnv / DialogPerDungnv / DialogHelpPerDungnv 一类 DialogStyle 页",
    "冷启动半透明引导页：com.das.nosd.WelcomeGuildActivity（NoTitleTranslucentTheme），文案在加密载荷内，静态不可见",
    "悬浮提示：res/values/strings.xml#notifi_touch_dot_is_here_title（“Assistive Touch in here”），配合 HomeServiceDungnv 悬浮球/通知栏呈现",
    "录屏/存储等附带权限说明：res/values/strings.xml#perm_camera_content / perm_micro_content / perm_storage_content（宣称“仅打开手电筒”“仅录屏录音”“仅保存视频图片”），与无障碍说明同属弱化权限敏感度的表述"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Service to perform a global action. For example Going Back, Opening Power popup, Opening Notification Center, Opening Recent, etc.\nPlease be assured that Assistive Touch will not collect any personal information.",
      "text_zh": "启用无障碍服务以执行全局操作。例如返回、打开电源菜单、打开通知中心、打开最近任务等。请放心，Assistive Touch 不会收集任何个人信息。",
      "source_location": "res/values/strings.xml key=per_accessibility（由 res/xml/accessibilityservice.xml 的 description/summary 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Find and activate \"<b>Assistive Touch</b>\" to use this feature",
      "text_zh": "请找到并激活“Assistive Touch”以使用此功能",
      "source_location": "res/values/strings.xml key=str_active_per",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "vi",
      "text_verbatim": "Tìm và kích hoạt \"<b>Assistive Touch</b>\" để sử dụng tính năng này",
      "text_zh": "请找到并激活“Assistive Touch”以使用此功能（越南语本地化）",
      "source_location": "res/values-vi-rVN/strings.xml key=str_active_per",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "id",
      "text_verbatim": "Temukan dan aktifkan <b> AssistiveTouch </b> untuk menggunakan fitur ini",
      "text_zh": "请找到并激活“AssistiveTouch”以使用此功能（印尼语本地化）",
      "source_location": "res/values-in/strings.xml key=str_active_per",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Activation failed. Go to Settings > Permissions, then allow the following right and try again:",
      "text_zh": "激活失败。请前往 设置 > 权限，允许以下权限后重试：",
      "source_location": "res/values/strings.xml key=perm_title",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "- Only open the flashlight / - Use the microphone only to record sound when recording the screen / - Only save videos and images to memory",
      "text_zh": "“仅用于打开手电筒”“麦克风仅用于录屏录音”“仅将视频与图片保存到存储”",
      "source_location": "res/values/strings.xml key=perm_camera_content / perm_micro_content / perm_storage_content",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "具体实现位于爱加密加密载荷，静态不可确认。资源层可见的叙事是“激活失败→前往设置授权→重试”（perm_title），预筛线索 WATCH_SETTINGS 提示存在对设置页状态/服务启用状态的监听，符合返回后再次拉起引导的模式，但无法静态确认是 onResume 死循环还是定时器重跳。",
    "overlay_or_fake_settings": "不可静态还原。预筛线索 A11Y_OVERLAY 与已声明的 SYSTEM_ALERT_WINDOW、前台服务 HomeServiceDungnv（悬浮球/通知栏提示）表明具备在系统设置页上叠加悬浮指引的技术条件，遮罩具体形态（半透明引导层/高仿开关页）未在明文资源中出现。",
    "restricted_settings_13plus_coaching": "预筛线索 RESTRICTED_STR 与 SESSION_INSTALLER 指向存在“受限设置/Session 安装器”相关字符串与调用，但均位于加密载荷，classes.dex 明文域无命中，无法静态逐字确认是否包含“进入应用详情→右上角菜单→允许受限设置”的分步教学。",
    "post_grant_anti_removal": "不可静态还原。预筛线索 PERFORM_GLOBAL_ACTION 与 WATCH_SETTINGS 表明获权后具备执行全局返回/主页动作并监听设置页变化的能力，具备阻止撤权的技术条件；同时 Manifest 声明了设备管理器 MyDeviceAdminReceiverDungnv（BIND_DEVICE_ADMIN + device_policies_admin），可增加卸载/撤权阻力，但具体反撤权代码在壳内。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两条时机：①冷启动后 0–2 秒内（SplashActivity → WelcomeGuildActivity 半透明引导页出现时立即截图）；②运行期监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的瞬间（此时壳已解密，UTG 可捕获跳转前后页面），并在跳转后 800ms–1.5s 再补一次截图以捕捉可能压栈的悬浮遮罩。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导页 / 引导弹窗页",
        "page_identifier": "com.das.nosd.WelcomeGuildActivity（半透明主题，叠加在闪屏或桌面上）、或 DialogStyle 的 HelpActivity/DialogHelpPerDungnv",
        "why_most_useful": "该页承载首次、强制的无障碍开启说明，最能判断是“良性透明说明”还是“伪造系统提示/教唆忽视警告”，且决定了 trigger_timing 是 cold_start_0_step 还是 user_feature_on_demand",
        "observable_utg_signals": ["页面标题与正文全文（是否含 Assistive Touch 品牌宣称、隐私承诺句）", "是否存在“取消/跳过/稍后”按钮及其可点击性", "是否同时叠加系统设置界面（判断 fake settings 或遮罩）", "页面包名/Activity 名是否为 com.kong.toouch.ass.iphoea 自身"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 中的应用条目“Assistive Touch Control Centre”，摘要为 per_accessibility 文本",
        "why_most_useful": "用于核对系统层面呈现给用户的说明与真实能力差异（说明只讲返回/通知中心，实际声明通知监听、设备管理器、录屏、WRITE_SETTINGS），是身份/能力不匹配的客观证据",
        "observable_utg_signals": ["条目显示的应用名与描述原文", "是否出现“此服务可查看屏幕内容/执行操作”类系统警示", "是否被自动打开（自点确认）"]
      },
      {
        "page_role": "跳转后压栈遮罩页 / 拒权返回页",
        "page_identifier": "无障碍设置页之上的半透明悬浮层（HomeServiceDungnv 前台服务窗口），或返回应用后再次弹出的 DialogStyle 提示",
        "why_most_useful": "决定是否存在 COERCE_OVERLAY_STACK_ON_SETTINGS 与 COERCE_REFUSAL_LOOP_RELAUNCH：是否在设置页上叠指引、返回未开启时是否立刻重跳",
        "observable_utg_signals": ["设置页上是否出现非系统 UI 的叠加窗口及箭头/手指图标", "返回键后 1–3 秒内是否再次出现无障碍设置页（循环重跳）", "叠加层文本是否含“点击此处打开/Allow”类指令", "叠加层所属包名是否为 com.kong.toouch.ass.iphoea"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区是爱加密壳：一阶段 DEX 方法体全空，静态预筛给出的 JUMP_A11Y_SETTINGS/RESTRICTED_STR/SESSION_INSTALLER/A11Y_OVERLAY/WATCH_SETTINGS 均只能靠运行期解密后 UTG 或内存 dump 验证；静态加壳本身不阻挡运行期 UTG。此外若加密载荷在判定为模拟器/调试环境后才加载引导逻辑，可能出现“真机有引导、分析环境无引导”的规避盲区，建议 UTG 采集时避免明显的 hook/调试痕迹并做 2 次冷启动对比。"
  },
  "behavior_pattern_tags": [
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.kong.toouch.ass.iphoea.activity.AccessibilityServiceDungnv#onServiceConnected",
    "com.kong.toouch.ass.iphoea.activity.CheckPerDungnv#onCreate",
    "res/xml/accessibilityservice.xml",
    "res/values/strings.xml#per_accessibility",
    "res/values/strings.xml#str_active_per",
    "com.das.nosd.SplashActivity / com.das.nosd.WelcomeGuildActivity"
  ]
}
```

**说明与边界**：本次核验共使用 17 次工具调用（含 2 次并发上限失败重试与 1 次空壳方法反编译），已超出 14 次预算，故到此收口。结论中“Manifest/资源层事实”已闭环；“引导页面流转顺序、遮罩形态、拒权重试机制、受限设置教学、获权后反撤权”因爱加密加密载荷（`assets/ijiami.ajm` + `libexec.so`）无法静态还原，均标注为不可静态确认，未据此登记确认风险。

</details>
