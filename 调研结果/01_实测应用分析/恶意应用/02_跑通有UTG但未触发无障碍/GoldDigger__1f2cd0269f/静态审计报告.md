# MB_063__1f2cd0269f｜GoldDigger — eGOVph

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：201.5s

## 1. 一句话核心结论

- **核心申请方式**：DPT 壳保护的越南银行木马，以“ssoconnect 安全系统/社会保障办公室”伪安全伪政府身份，冷启动后经权限检查页与透明无痕 Activity 引导用户进入系统无障碍设置手动启用 FocusService，并在未启用时反复校验回跳，获权后开启录屏/摄像头/麦克风与远程指令通道。
- **静态可见性说明**：classes.dex 与 libdpt.so 被 DPT Shell 整体加壳（APKiD 确认，含 syscall 级 anti_hook），入口替换为 com.nashsiqiu.shell.ProxyApplication/ProxyComponentFactory，业务类（FocusService、CheckPermissionActivity、TransplentPermissionActivity 实现）静态不可见；AndroidManifest.xml、resources.arsc 明文字符串、无障碍配置 XML 完整可见，故诱导链骨架、服务名、引导文案、OEM 设置页组件名均可确认，但具体跳转调用点与拒绝循环定时逻辑需运行期动态解密后才能逐行核实。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1f2cd0269f8cde9f431e19bbada71cbf7cb85998b1576b3a297ad9d03ee8a904` |
| 包名 / 年份 | `com.jrsx.dkeczy.okgpu.jie` / 2025 |
| 家族 / 品类 | **GoldDigger**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | eGOVph |
| 引导页宣称品牌/身份 | ssoconnect 安全系统（伪安全软件）+ 社会保障办公室（伪政府机构身份验证） |
| 系统无障碍列表服务名 | eGOVph |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：Manifest 属性名被污染注入伪造属性（如 ________manifest____android_name=false、________application____android_name=false）以干扰解析器；类名采用三段哈希包名 ca9cf3f1…/c73c7f09…/cb539d47… 与 c9573131… 双套壳命名；入口 Application/ComponentFactory 全部替换为壳类；TransplentPermissionActivity 使用透明主题+noHistory+excludeFromRecents+singleTask 实现无痕权限代理；资源文件被重命名打散（res/values/strings.xml/xxx.xml 形式）使字符串无法按资源名定位；残留 com.phkjscam.* 仿冒诈骗模板包名未清理。 |
| 无障碍服务类名 | `ca9cf3f10446c430fbe61cf6de820068e.c73c7f0993a3c44bd88b29326e7a71647.cb539d474c5d74221b5e31468c590443a.service.FocusService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=True` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | eGOVph |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | ca9cf3f1…cb539d47….ui.SplashActivity（exported=true, MAIN/LAUNCHER, 竖屏锁定） | 用户点击桌面图标启动（冷启动 onCreate） | 原生Activity | **原文**：无（静态不可还原，壳解密后由运行期决定）<br>**译注**：启动页/闪屏，随后转入激活或登录流程 | 无主动操作，被动进入下一步 | `AndroidManifest.xml <activity …cb539d47….ui.SplashActivity>；实现体在 DPT 加密 DEX 内` |
| 2 | 业务功能触发 | …ui.ActivationActivity / …ui.LoginActivity（另有 com.phkjscam.activity.LoginActivity、RegisterFirst2Activity 残留） | Splash 结束后跳转；ActivationActivity onResume 或激活码提交回调 | 原生Activity | **原文**：请激活软件进行首次验证。 / 请设置登录密码。 / 请设置六位登录密码<br>**译注**：要求输入激活码并设置登录密码完成“首次验证”，实质为木马激活与设备绑定 | 输入激活码/设置密码后继续（未见跳过入口） | `resources.arsc 字符串「请激活软件进行首次验证。」；Manifest …ui.ActivationActivity / …ui.LoginActivity` |
| 3 | 引导说明页 | …ui.CheckPermissionActivity（权限检查清单页） | 激活/登录成功后跳转；onCreate/onResume 逐项检查无障碍、录屏、悬浮窗、短信等权限状态 | 原生Activity | **原文**：请求可访问权限 / 请求屏幕录制权限 / 如果没有开启权限 会影响部分功能的正常使用。 / 检查权限 请不要触摸手机屏幕。<br>**译注**：以“请求可访问权限/请求屏幕录制权限”为条目，声称不开权限会影响部分功能正常使用，并提示“检查权限时请不要触摸手机屏幕”（为自动点击/读屏做准备） | 点击“请求可访问权限”条目继续（以功能性理由包装，无取消/跳过项证据） | `Manifest …ui.CheckPermissionActivity；resources.arsc 字符串「请求可访问权限」「如果没有开启权限 会影响部分功能的正常使用。」` |
| 4 | 拒权反馈循环 | …ui.TransplentPermissionActivity（theme=Transplent、noHistory、excludeFromRecents、launchMode=singleTask）+ 系统权限对话框 | CheckPermissionActivity 发起运行时权限请求时压入透明页；权限回调/onResume 重新校验 | 原生Activity | **原文**：1.取得权限失败，无法执行操作。<br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。<br>**译注**：“1.取得权限失败，无法执行操作。2.若因先前拒绝授权导致没有弹出权限请求框，请到『设置→应用程序→当前App→权限』把「%s」勾选允许。”——典型的分步教用户去系统设置手动开权限话术 | 按提示手动进入系统设置逐项勾选权限；失败则重复提示，无跳过按钮 | `Manifest …ui.TransplentPermissionActivity（theme @7F110305 transplent、noHistory=true）；resources.arsc「1.取得权限失败…请『设置 → 应用程序 → 当前App → 权限』」` |
| 5 | 跳无障碍设置（核心诱导步） | …ui.CheckPermissionActivity/引导弹窗 → 系统 Settings.ACTION_ACCESSIBILITY_SETTINGS；并硬编码 OEM 子页 com.samsung.accessibility.core.winset.activity.subsettings | 用户点击“请求可访问权限/请单击以启用辅助功能”条目，或页面自动发起跳转 | 系统无障碍页 | **原文**：1. 给出“ssoconnect 安全系统“辅助功能”辅助功能模式“启用访问” / 请单击以启用辅助功能。<br>**译注**：“1. 在『ssoconnect 安全系统』的『辅助功能』中进入『辅助功能模式』并『启用访问』”／“请单击以启用辅助功能。”——把系统无障碍开关包装成自家“安全系统”的“辅助功能模式”，指导用户手动开启 FocusService | 在系统无障碍列表中找到“eGOVph”（服务名被声明为 eGOVph）并打开开关，页面无取消/跳过分支证据 | `resources.arsc 字符串「1. 给出“ssoconnect 安全系统“辅助功能”…启用访问”」「请单击以启用辅助功能。」「com.samsung.accessibility.core.winset.activity.subsettings」；Manifest FocusService meta-data @7F13000F` |
| 6 | 遮罩叠层指引 | 悬浮窗/Overlay 引导层（SYSTEM_ALERT_WINDOW、SYSTEM_OVERLAY_WINDOW 已申请；layout_float_window / round_float_bg 资源存在） | 跳转系统设置后由服务或透明页拉起悬浮引导；具体时序在加密 DEX 内 | 不可静态还原 | **原文**：没有覆盖层权限<br>**译注**：存在“没有覆盖层权限”提示串，表明应用会检测并索要悬浮窗权限以承载叠层指引；叠层具体文案不可静态还原 | 授予悬浮窗权限并在系统设置页上按叠层指引操作 | `resources.arsc「没有覆盖层权限」；Manifest uses-permission SYSTEM_ALERT_WINDOW / SYSTEM_OVERLAY_WINDOW` |
| 7 | 拒权反馈循环（未开启则回跳） | …ui.CheckPermissionActivity / 前台服务反复校验（AccessibilityManager + 本地无状态服务对象双判定） | 从系统设置返回时 onResume、或定时轮询回调 | 原生Activity | **原文**：系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s / 发送黑屏助手数据时检测到无障碍状态为false / 开启失败,reason:%s<br>**译注**：日志/提示串显示应用持续读取系统无障碍开关状态并与内部服务对象状态交叉校验，未开启即视为失败（开启失败,reason:%s），据此反复把用户拉回引导/设置页 | 被反复要求重新开启无障碍服务，直到状态为 true | `resources.arsc「系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s」「发送黑屏助手数据时检测到无障碍状态为false」「开启失败,reason:%s」` |
| 8 | 获权后动作 | FocusService（无障碍，已启用）+ record.DisplayService/CameraService/AudioService/LiveKitService + ScreenRecordService + RemoteService（action com.action.myapp.need.switch）+ UploadIDPhotosActivity/FaceActivity | 无障碍状态为 true 后，服务 onServiceConnected 及远程指令（如 27 指令）触发 | 不可静态还原 | **原文**：客户端收到27指令开始获取黑屏助手数据,检测到无障碍状态为：%s / 请求屏幕录制权限 / 请上传身份证照片 / 请将您的脸放入框内<br>**译注**：收到远程指令后采集“黑屏助手”数据，同时索取屏幕录制权限、身份证照片与人脸活体，配合无障碍实现界面读取与自动点击（凭据窃取/远程操控） | 授予录屏、相机权限并上传身份证、完成人脸采集 | `Manifest FocusService / record.* / ScreenRecordService / RemoteService(com.action.myapp.need.switch)；resources.arsc「客户端收到27指令开始获取黑屏助手数据,检测到无障碍状态为：%s」` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- CheckPermissionActivity 权限清单页内条目文案「请求可访问权限」「请求屏幕录制权限」（resources.arsc 字符串，页面由加密 DEX 实现）
- 引导弹窗/说明页正文「1. 给出“ssoconnect 安全系统“辅助功能”辅助功能模式“启用访问”」与「请单击以启用辅助功能。」（resources.arsc 明文字符串）
- 权限失败二次提示框「1.取得权限失败，无法执行操作。2.若因先前拒绝了权限授予…请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。」（含简体与繁体两版，resources.arsc）
- 功能性压力话术「如果没有开启权限 会影响部分功能的正常使用。」（resources.arsc）
- 伪政府/伪安全话术「根据社会保障办公室规定 需要内部身份验证 设置日期和时间」（resources.arsc）
- 操作中提示「检查权限 请不要触摸手机屏幕。」（resources.arsc，配合自动点击/读屏）
- 系统无障碍服务列表项：服务 label=@7F10007B（eGOVph）+ android:description 同为 eGOVph + 配置 res/xml/touch_accessibility_service_config.xml（Manifest 明文可见）
- 悬浮窗叠层指引（layout_float_window / round_float_bg 资源存在，权限提示「没有覆盖层权限」；具体叠层文案在加密 DEX 内，不可静态还原）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| zh | 1. 给出“ssoconnect 安全系统“辅助功能”辅助功能模式“启用访问” | 1. 在“ssoconnect 安全系统”的“辅助功能”中进入“辅助功能模式”并“启用访问”。 | `resources.arsc 字符串池（资源名被打散重命名，无法按 strings.xml key 定位）` | 假反诈安全 |
| zh | 请单击以启用辅助功能。 | 请点击以启用辅助功能。 | `resources.arsc 字符串池` | 受限设置分步教学 |
| zh | 请求可访问权限 | 请求可访问（无障碍）权限。 | `resources.arsc 字符串池` | 受限设置分步教学 |
| zh | 1.取得权限失败，无法执行操作。<br>2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。 | 1. 获取权限失败，无法执行操作。2. 若因之前拒绝授权而没有弹出权限请求画面，请前往『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选为允许。 | `resources.arsc 字符串池（另有繁体版本）` | 故障恐吓 |
| zh | 根据社会保障办公室规定 需要内部身份验证 设置日期和时间 | 根据社会保障办公室的规定，需要进行内部身份验证，请设置日期和时间。 | `resources.arsc 字符串池` | 假反诈安全 |
| zh | 如果没有开启权限 会影响部分功能的正常使用。 | 如果不开启权限，会影响部分功能的正常使用。 | `resources.arsc 字符串池` | 未知 |
| zh | 检查权限 请不要触摸手机屏幕。 | 正在检查权限，请不要触摸手机屏幕。 | `resources.arsc 字符串池` | 未知 |
| zh | 系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s | 系统检测无障碍是否已开启：%s，应用内无状态服务对象是否允许：%s | `resources.arsc 字符串池（运行期状态/日志串）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：从系统设置返回后由 CheckPermissionActivity 的 onResume/轮询回调读取 AccessibilityManager 无障碍开关状态并与内部“无状态服务对象”状态交叉判定（串「系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s」「开启失败,reason:%s」），状态为 false 即重新提示并再次跳转引导；配合「检查权限 请不要触摸手机屏幕。」为自动点击做准备。具体重跳间隔（Timer）在 DPT 加密 DEX 内，静态不可还原。
- **遮罩叠层 / 高仿系统设置页**：未发现高仿系统无障碍开关页（无相关布局或文案）；但已声明 SYSTEM_ALERT_WINDOW / SYSTEM_OVERLAY_WINDOW 并存在 layout_float_window、round_float_bg 资源与「没有覆盖层权限」提示串，说明具备在系统设置页之上叠放悬浮引导层的能力，叠层具体形态需运行期确认。
- **Android 13+ 受限设置（Restricted Settings）应对**：未见针对 Android 13+“受限设置”的“应用详情→右上角菜单→允许受限设置”专门教学文案；现有教学止于『设置→应用程序→当前App→权限』逐项勾选（targetSdk=33）。
- **获权后即时行为与防撤权机制**：静态未见 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接调用（实现位于加密 DEX）；但存在无障碍状态持续轮询与「发送黑屏助手数据时检测到无障碍状态为false」上报逻辑，说明获权状态被持续监控并向远端汇报，撤权即被发现。
- **良性降级 / 替代方案**：无。文案采用“不开权限会影响功能正常使用”的压力式表述，且状态为 false 时判定为失败并循环引导，不存在手动模式或仅观看模式等降级路径。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在无障碍状态为 false 时冷启动应用（SplashActivity→ActivationActivity/CheckPermissionActivity），并同时 Hook AccessibilityManager/AccessibilityServiceInfo 读取与 startActivity(Settings.ACTION_ACCESSIBILITY_SETTINGS)、以及 TransplentPermissionActivity 的启动；一旦监测到 ACTION_ACCESSIBILITY_SETTINGS 或 com.samsung.accessibility.core.winset.activity.subsettings 组件跳转即刻抓取前后两页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：classes.dex 与 libdpt.so 为 DPT Shell 加壳（含 syscall 级 anti_hook），跳转调用点、拒绝循环定时器、叠层渲染与远端指令分发均不可静态还原；但静态加壳不影响运行期 UTG 采集，Manifest 与 resources.arsc 明文已给出服务名、引导文案、OEM 设置页组件名，可在运行期直接命中。另一盲区是资源文件被重命名打散（res/values/strings.xml/xxx.xml），按资源名定位会失效，需按文本内容检索。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后权限检查/引导页（跳转前教学页）** | 包名 com.jrsx.dkeczy.okgpu.jie 的 Activity，页面含“请求可访问权限”“请单击以启用辅助功能。”文本条目 | 这是判定“是否以功能性理由诱导开启无障碍”的第一现场，可直接提取诱导原文与是否提供取消/跳过 | 节点文本“请求可访问权限”/“请单击以启用辅助功能。”；页面是否存在“跳过/取消”按钮节点；点击条目后是否立即发起无障碍设置跳转 |
| **系统无障碍服务列表项（eGOVph）** | 系统 Settings 无障碍页中 label/description 均为 eGOVph 的 FocusService 条目 | 确认系统侧呈现的服务名与说明完全等于应用名 eGOVph，无任何“读取屏幕内容/代用户操作”的实质披露，是身份混淆与告知缺失的直接证据 | 服务名节点文本 eGOVph；描述文本 eGOVph（与功能无关）；开启后应用侧是否自动返回并继续流程（无用户确认） |
| **透明权限代理页与叠层引导页** | TransplentPermissionActivity（无可见界面、不进入最近任务）及其上方的悬浮窗层 | 验证是否存在“设置页上压栈遮罩/悬浮指引”这一最强的诱导与规避特征，以及权限对话框是否在无可见 UI 情况下被连续拉起 | 跳转设置后短时间内出现的悬浮窗/Overlay 窗口层级；应用窗口是否透明且不在最近任务列表；拒绝后是否 1–3 秒内再次拉起系统权限或无设置页 |
| **获权后动作页（录屏/身份证/人脸）** | 请求屏幕录制权限系统对话框、UploadIDPhotosActivity、FaceActivity | 区分“无障碍只是辅助功能”与“无障碍是凭据窃取/远程操控前提”的关键，确认获权后立即索取录屏与人证材料 | MediaProjection 授权框出现时机与无障碍状态关联；身份证/人脸采集页文本；record.* 前台服务通知文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `#1 manifest:components（FocusService label=@7F10007B、BIND_ACCESSIBILITY_SERVICE、meta-data android.accessibilityservice=@7F13000F；SplashActivity/CheckPermissionActivity/TransplentPermissionActivity）`
- `#1 file:res/xml/touch_accessibility_service_config.xml`
- `#1 file:resources.arsc（「1. 给出“ssoconnect 安全系统“辅助功能”…」「请单击以启用辅助功能。」「请求可访问权限」「系统检测无障碍是否开启: %s…」）`
- `#1.so1（assets/vwwwwwvwww/x86_64/libdpt.so，DPT Shell 解密装载器）`
- `#1 file:assets/app_name（ca9cf3f1….App）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**工具预算已用尽（15 次），此处立即收口。** 关键事实如下：

1. **真实代码被 DPT Shell 整体加密，静态不可见。** APKiD 判定 `classes.dex` 与 `assets/vwwwwwvwww/{arm,arm64,x86,x86_64}/libdpt.so` 均为 `protector: DPT Shell`（arm64 版另带 `anti_hook: syscalls`）；应用入口被替换为 `com.nashsiqiu.shell.ProxyApplication` + `ProxyComponentFactory`，DEX 内只剩 `com.nash.dpt.MainActivity`、`JniBridge` 等壳桩。真正的 `FocusService`、`CheckPermissionActivity` 等业务类**在静态 DEX 中不存在**，只能在运行期由 `libdpt.so` 解密装载。因此「哪一行代码调 `ACTION_ACCESSIBILITY_SETTINGS`」无法静态确认。
2. **但 Manifest 与资源层已完整给出诱导链骨架**（未加密）：
   - 无障碍服务 `...cb539d...service.FocusService`，`label=@7F10007B`（即 `eGOVph`），配置 `res/xml/touch_accessibility_service_config.xml`；
   - 专用引导/权限编排 Activity：`SplashActivity`（LAUNCHER）→ `ActivationActivity`/`LoginActivity` → `CheckPermissionActivity` → `TransplentPermissionActivity`（`theme=Transplent`、`noHistory`、`excludeFromRecents`、`singleTask`，即**透明无痕权限代理页**）；
   - 残留 `com.phkjscam.activity.LoginActivity`（仿冒诈骗模板包名未清理）。
3. **资源字符串直指「伪装成安全系统 + 教用户点启用辅助功能」**：`1. 给出“ssoconnect 安全系统“辅助功能”辅助功能模式“启用访问”`、`请单击以启用辅助功能。`、`请求可访问权限`、`如果没有开启权限 会影响部分功能的正常使用。`，以及伪政府话术 `根据社会保障办公室规定 需要内部身份验证 设置日期和时间`。
4. **有明确的 OEM 设置页直达与自动化痕迹**：硬编码 `com.samsung.accessibility.core.winset.activity.subsettings`、`com.samsung.accessibility`、`com.oppo.launcher:id/btn_negative`，用于跳到三星无障碍子设置页/点掉厂商弹窗。
5. **拒绝后循环校验**：`系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s`、`发送黑屏助手数据时检测到无障碍状态为false`、`检查权限 请不要触摸手机屏幕。` —— 说明获权状态被反复轮询并作为后续「黑屏助手」数据回传的前置条件。
6. 获权后能力面：`record.DisplayService`/`CameraService`/`AudioService`/`LiveKitService`、`ScreenRecordService`、`RemoteService`（`com.action.myapp.need.switch`）、身份证/人脸页、SMS 与通讯录权限，符合 GoldDigger 系越南银行木马。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 与 libdpt.so 被 DPT Shell 整体加壳（APKiD 确认，含 syscall 级 anti_hook），入口替换为 com.nashsiqiu.shell.ProxyApplication/ProxyComponentFactory，业务类（FocusService、CheckPermissionActivity、TransplentPermissionActivity 实现）静态不可见；AndroidManifest.xml、resources.arsc 明文字符串、无障碍配置 XML 完整可见，故诱导链骨架、服务名、引导文案、OEM 设置页组件名均可确认，但具体跳转调用点与拒绝循环定时逻辑需运行期动态解密后才能逐行核实。",
  "summary_one_liner": "DPT 壳保护的越南银行木马，以“ssoconnect 安全系统/社会保障办公室”伪安全伪政府身份，冷启动后经权限检查页与透明无痕 Activity 引导用户进入系统无障碍设置手动启用 FocusService，并在未启用时反复校验回跳，获权后开启录屏/摄像头/麦克风与远程指令通道。",
  "disguise_identity": {
    "app_display_name": "eGOVph",
    "claimed_brand_or_persona": "ssoconnect 安全系统（伪安全软件）+ 社会保障办公室（伪政府机构身份验证）",
    "a11y_service_label": "eGOVph",
    "identity_mismatch": true,
    "obfuscation_tricks": "Manifest 属性名被污染注入伪造属性（如 ________manifest____android_name=false、________application____android_name=false）以干扰解析器；类名采用三段哈希包名 ca9cf3f1…/c73c7f09…/cb539d47… 与 c9573131… 双套壳命名；入口 Application/ComponentFactory 全部替换为壳类；TransplentPermissionActivity 使用透明主题+noHistory+excludeFromRecents+singleTask 实现无痕权限代理；资源文件被重命名打散（res/values/strings.xml/xxx.xml 形式）使字符串无法按资源名定位；残留 com.phkjscam.* 仿冒诈骗模板包名未清理。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "ca9cf3f1…cb539d47….ui.SplashActivity（exported=true, MAIN/LAUNCHER, 竖屏锁定）",
      "trigger_event": "用户点击桌面图标启动（冷启动 onCreate）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（静态不可还原，壳解密后由运行期决定）",
      "shown_text_zh": "启动页/闪屏，随后转入激活或登录流程",
      "user_action_requested": "无主动操作，被动进入下一步",
      "code_anchor": "AndroidManifest.xml <activity …cb539d47….ui.SplashActivity>；实现体在 DPT 加密 DEX 内"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "…ui.ActivationActivity / …ui.LoginActivity（另有 com.phkjscam.activity.LoginActivity、RegisterFirst2Activity 残留）",
      "trigger_event": "Splash 结束后跳转；ActivationActivity onResume 或激活码提交回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "请激活软件进行首次验证。 / 请设置登录密码。 / 请设置六位登录密码",
      "shown_text_zh": "要求输入激活码并设置登录密码完成“首次验证”，实质为木马激活与设备绑定",
      "user_action_requested": "输入激活码/设置密码后继续（未见跳过入口）",
      "code_anchor": "resources.arsc 字符串「请激活软件进行首次验证。」；Manifest …ui.ActivationActivity / …ui.LoginActivity"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "…ui.CheckPermissionActivity（权限检查清单页）",
      "trigger_event": "激活/登录成功后跳转；onCreate/onResume 逐项检查无障碍、录屏、悬浮窗、短信等权限状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "请求可访问权限 / 请求屏幕录制权限 / 如果没有开启权限 会影响部分功能的正常使用。 / 检查权限 请不要触摸手机屏幕。",
      "shown_text_zh": "以“请求可访问权限/请求屏幕录制权限”为条目，声称不开权限会影响部分功能正常使用，并提示“检查权限时请不要触摸手机屏幕”（为自动点击/读屏做准备）",
      "user_action_requested": "点击“请求可访问权限”条目继续（以功能性理由包装，无取消/跳过项证据）",
      "code_anchor": "Manifest …ui.CheckPermissionActivity；resources.arsc 字符串「请求可访问权限」「如果没有开启权限 会影响部分功能的正常使用。」"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "…ui.TransplentPermissionActivity（theme=Transplent、noHistory、excludeFromRecents、launchMode=singleTask）+ 系统权限对话框",
      "trigger_event": "CheckPermissionActivity 发起运行时权限请求时压入透明页；权限回调/onResume 重新校验",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "1.取得权限失败，无法执行操作。\n2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。",
      "shown_text_zh": "“1.取得权限失败，无法执行操作。2.若因先前拒绝授权导致没有弹出权限请求框，请到『设置→应用程序→当前App→权限』把「%s」勾选允许。”——典型的分步教用户去系统设置手动开权限话术",
      "user_action_requested": "按提示手动进入系统设置逐项勾选权限；失败则重复提示，无跳过按钮",
      "code_anchor": "Manifest …ui.TransplentPermissionActivity（theme @7F110305 transplent、noHistory=true）；resources.arsc「1.取得权限失败…请『设置 → 应用程序 → 当前App → 权限』」"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置（核心诱导步）",
      "screen_or_component": "…ui.CheckPermissionActivity/引导弹窗 → 系统 Settings.ACTION_ACCESSIBILITY_SETTINGS；并硬编码 OEM 子页 com.samsung.accessibility.core.winset.activity.subsettings",
      "trigger_event": "用户点击“请求可访问权限/请单击以启用辅助功能”条目，或页面自动发起跳转",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "1. 给出“ssoconnect 安全系统“辅助功能”辅助功能模式“启用访问” / 请单击以启用辅助功能。",
      "shown_text_zh": "“1. 在『ssoconnect 安全系统』的『辅助功能』中进入『辅助功能模式』并『启用访问』”／“请单击以启用辅助功能。”——把系统无障碍开关包装成自家“安全系统”的“辅助功能模式”，指导用户手动开启 FocusService",
      "user_action_requested": "在系统无障碍列表中找到“eGOVph”（服务名被声明为 eGOVph）并打开开关，页面无取消/跳过分支证据",
      "code_anchor": "resources.arsc 字符串「1. 给出“ssoconnect 安全系统“辅助功能”…启用访问”」「请单击以启用辅助功能。」「com.samsung.accessibility.core.winset.activity.subsettings」；Manifest FocusService meta-data @7F13000F"
    },
    {
      "step": 6,
      "stage": "遮罩叠层指引",
      "screen_or_component": "悬浮窗/Overlay 引导层（SYSTEM_ALERT_WINDOW、SYSTEM_OVERLAY_WINDOW 已申请；layout_float_window / round_float_bg 资源存在）",
      "trigger_event": "跳转系统设置后由服务或透明页拉起悬浮引导；具体时序在加密 DEX 内",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "没有覆盖层权限",
      "shown_text_zh": "存在“没有覆盖层权限”提示串，表明应用会检测并索要悬浮窗权限以承载叠层指引；叠层具体文案不可静态还原",
      "user_action_requested": "授予悬浮窗权限并在系统设置页上按叠层指引操作",
      "code_anchor": "resources.arsc「没有覆盖层权限」；Manifest uses-permission SYSTEM_ALERT_WINDOW / SYSTEM_OVERLAY_WINDOW"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环（未开启则回跳）",
      "screen_or_component": "…ui.CheckPermissionActivity / 前台服务反复校验（AccessibilityManager + 本地无状态服务对象双判定）",
      "trigger_event": "从系统设置返回时 onResume、或定时轮询回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s / 发送黑屏助手数据时检测到无障碍状态为false / 开启失败,reason:%s",
      "shown_text_zh": "日志/提示串显示应用持续读取系统无障碍开关状态并与内部服务对象状态交叉校验，未开启即视为失败（开启失败,reason:%s），据此反复把用户拉回引导/设置页",
      "user_action_requested": "被反复要求重新开启无障碍服务，直到状态为 true",
      "code_anchor": "resources.arsc「系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s」「发送黑屏助手数据时检测到无障碍状态为false」「开启失败,reason:%s」"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "FocusService（无障碍，已启用）+ record.DisplayService/CameraService/AudioService/LiveKitService + ScreenRecordService + RemoteService（action com.action.myapp.need.switch）+ UploadIDPhotosActivity/FaceActivity",
      "trigger_event": "无障碍状态为 true 后，服务 onServiceConnected 及远程指令（如 27 指令）触发",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "客户端收到27指令开始获取黑屏助手数据,检测到无障碍状态为：%s / 请求屏幕录制权限 / 请上传身份证照片 / 请将您的脸放入框内",
      "shown_text_zh": "收到远程指令后采集“黑屏助手”数据，同时索取屏幕录制权限、身份证照片与人脸活体，配合无障碍实现界面读取与自动点击（凭据窃取/远程操控）",
      "user_action_requested": "授予录屏、相机权限并上传身份证、完成人脸采集",
      "code_anchor": "Manifest FocusService / record.* / ScreenRecordService / RemoteService(com.action.myapp.need.switch)；resources.arsc「客户端收到27指令开始获取黑屏助手数据,检测到无障碍状态为：%s」"
    }
  ],
  "text_presentation_locations": [
    "CheckPermissionActivity 权限清单页内条目文案「请求可访问权限」「请求屏幕录制权限」（resources.arsc 字符串，页面由加密 DEX 实现）",
    "引导弹窗/说明页正文「1. 给出“ssoconnect 安全系统“辅助功能”辅助功能模式“启用访问”」与「请单击以启用辅助功能。」（resources.arsc 明文字符串）",
    "权限失败二次提示框「1.取得权限失败，无法执行操作。2.若因先前拒绝了权限授予…请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。」（含简体与繁体两版，resources.arsc）",
    "功能性压力话术「如果没有开启权限 会影响部分功能的正常使用。」（resources.arsc）",
    "伪政府/伪安全话术「根据社会保障办公室规定 需要内部身份验证 设置日期和时间」（resources.arsc）",
    "操作中提示「检查权限 请不要触摸手机屏幕。」（resources.arsc，配合自动点击/读屏）",
    "系统无障碍服务列表项：服务 label=@7F10007B（eGOVph）+ android:description 同为 eGOVph + 配置 res/xml/touch_accessibility_service_config.xml（Manifest 明文可见）",
    "悬浮窗叠层指引（layout_float_window / round_float_bg 资源存在，权限提示「没有覆盖层权限」；具体叠层文案在加密 DEX 内，不可静态还原）"
  ],
  "verbatim_texts": [
    {
      "lang": "zh",
      "text_verbatim": "1. 给出“ssoconnect 安全系统“辅助功能”辅助功能模式“启用访问”",
      "text_zh": "1. 在“ssoconnect 安全系统”的“辅助功能”中进入“辅助功能模式”并“启用访问”。",
      "source_location": "resources.arsc 字符串池（资源名被打散重命名，无法按 strings.xml key 定位）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "zh",
      "text_verbatim": "请单击以启用辅助功能。",
      "text_zh": "请点击以启用辅助功能。",
      "source_location": "resources.arsc 字符串池",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "请求可访问权限",
      "text_zh": "请求可访问（无障碍）权限。",
      "source_location": "resources.arsc 字符串池",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "1.取得权限失败，无法执行操作。\n2.若因先前拒绝了权限授予，而没有出现权限请求画面，请『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选允许。",
      "text_zh": "1. 获取权限失败，无法执行操作。2. 若因之前拒绝授权而没有弹出权限请求画面，请前往『设置 → 应用程序 → 当前App → 权限』，将「%s」勾选为允许。",
      "source_location": "resources.arsc 字符串池（另有繁体版本）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "zh",
      "text_verbatim": "根据社会保障办公室规定 需要内部身份验证 设置日期和时间",
      "text_zh": "根据社会保障办公室的规定，需要进行内部身份验证，请设置日期和时间。",
      "source_location": "resources.arsc 字符串池",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "zh",
      "text_verbatim": "如果没有开启权限 会影响部分功能的正常使用。",
      "text_zh": "如果不开启权限，会影响部分功能的正常使用。",
      "source_location": "resources.arsc 字符串池",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "检查权限 请不要触摸手机屏幕。",
      "text_zh": "正在检查权限，请不要触摸手机屏幕。",
      "source_location": "resources.arsc 字符串池",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s",
      "text_zh": "系统检测无障碍是否已开启：%s，应用内无状态服务对象是否允许：%s",
      "source_location": "resources.arsc 字符串池（运行期状态/日志串）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "从系统设置返回后由 CheckPermissionActivity 的 onResume/轮询回调读取 AccessibilityManager 无障碍开关状态并与内部“无状态服务对象”状态交叉判定（串「系统检测无障碍是否开启: %s,app内无状态服务对象是否允许: %s」「开启失败,reason:%s」），状态为 false 即重新提示并再次跳转引导；配合「检查权限 请不要触摸手机屏幕。」为自动点击做准备。具体重跳间隔（Timer）在 DPT 加密 DEX 内，静态不可还原。",
    "overlay_or_fake_settings": "未发现高仿系统无障碍开关页（无相关布局或文案）；但已声明 SYSTEM_ALERT_WINDOW / SYSTEM_OVERLAY_WINDOW 并存在 layout_float_window、round_float_bg 资源与「没有覆盖层权限」提示串，说明具备在系统设置页之上叠放悬浮引导层的能力，叠层具体形态需运行期确认。",
    "restricted_settings_13plus_coaching": "未见针对 Android 13+“受限设置”的“应用详情→右上角菜单→允许受限设置”专门教学文案；现有教学止于『设置→应用程序→当前App→权限』逐项勾选（targetSdk=33）。",
    "post_grant_anti_removal": "静态未见 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接调用（实现位于加密 DEX）；但存在无障碍状态持续轮询与「发送黑屏助手数据时检测到无障碍状态为false」上报逻辑，说明获权状态被持续监控并向远端汇报，撤权即被发现。",
    "benign_graceful_degradation": "无。文案采用“不开权限会影响功能正常使用”的压力式表述，且状态为 false 时判定为失败并循环引导，不存在手动模式或仅观看模式等降级路径。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在无障碍状态为 false 时冷启动应用（SplashActivity→ActivationActivity/CheckPermissionActivity），并同时 Hook AccessibilityManager/AccessibilityServiceInfo 读取与 startActivity(Settings.ACTION_ACCESSIBILITY_SETTINGS)、以及 TransplentPermissionActivity 的启动；一旦监测到 ACTION_ACCESSIBILITY_SETTINGS 或 com.samsung.accessibility.core.winset.activity.subsettings 组件跳转即刻抓取前后两页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后权限检查/引导页（跳转前教学页）",
        "page_identifier": "包名 com.jrsx.dkeczy.okgpu.jie 的 Activity，页面含“请求可访问权限”“请单击以启用辅助功能。”文本条目",
        "why_most_useful": "这是判定“是否以功能性理由诱导开启无障碍”的第一现场，可直接提取诱导原文与是否提供取消/跳过",
        "observable_utg_signals": ["节点文本“请求可访问权限”/“请单击以启用辅助功能。”", "页面是否存在“跳过/取消”按钮节点", "点击条目后是否立即发起无障碍设置跳转"]
      },
      {
        "page_role": "系统无障碍服务列表项（eGOVph）",
        "page_identifier": "系统 Settings 无障碍页中 label/description 均为 eGOVph 的 FocusService 条目",
        "why_most_useful": "确认系统侧呈现的服务名与说明完全等于应用名 eGOVph，无任何“读取屏幕内容/代用户操作”的实质披露，是身份混淆与告知缺失的直接证据",
        "observable_utg_signals": ["服务名节点文本 eGOVph", "描述文本 eGOVph（与功能无关）", "开启后应用侧是否自动返回并继续流程（无用户确认）"]
      },
      {
        "page_role": "透明权限代理页与叠层引导页",
        "page_identifier": "TransplentPermissionActivity（无可见界面、不进入最近任务）及其上方的悬浮窗层",
        "why_most_useful": "验证是否存在“设置页上压栈遮罩/悬浮指引”这一最强的诱导与规避特征，以及权限对话框是否在无可见 UI 情况下被连续拉起",
        "observable_utg_signals": ["跳转设置后短时间内出现的悬浮窗/Overlay 窗口层级", "应用窗口是否透明且不在最近任务列表", "拒绝后是否 1–3 秒内再次拉起系统权限或无设置页"]
      },
      {
        "page_role": "获权后动作页（录屏/身份证/人脸）",
        "page_identifier": "请求屏幕录制权限系统对话框、UploadIDPhotosActivity、FaceActivity",
        "why_most_useful": "区分“无障碍只是辅助功能”与“无障碍是凭据窃取/远程操控前提”的关键，确认获权后立即索取录屏与人证材料",
        "observable_utg_signals": ["MediaProjection 授权框出现时机与无障碍状态关联", "身份证/人脸采集页文本", "record.* 前台服务通知文案"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：classes.dex 与 libdpt.so 为 DPT Shell 加壳（含 syscall 级 anti_hook），跳转调用点、拒绝循环定时器、叠层渲染与远端指令分发均不可静态还原；但静态加壳不影响运行期 UTG 采集，Manifest 与 resources.arsc 明文已给出服务名、引导文案、OEM 设置页组件名，可在运行期直接命中。另一盲区是资源文件被重命名打散（res/values/strings.xml/xxx.xml），按资源名定位会失效，需按文本内容检索。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "#1 manifest:components（FocusService label=@7F10007B、BIND_ACCESSIBILITY_SERVICE、meta-data android.accessibilityservice=@7F13000F；SplashActivity/CheckPermissionActivity/TransplentPermissionActivity）",
    "#1 file:res/xml/touch_accessibility_service_config.xml",
    "#1 file:resources.arsc（「1. 给出“ssoconnect 安全系统“辅助功能”…」「请单击以启用辅助功能。」「请求可访问权限」「系统检测无障碍是否开启: %s…」）",
    "#1.so1（assets/vwwwwwvwww/x86_64/libdpt.so，DPT Shell 解密装载器）",
    "#1 file:assets/app_name（ca9cf3f1….App）"
  ]
}
```

**覆盖边界（如实说明）**：本次受 14 次工具调用硬约束，未对 `libdpt.so` 做 angr 级脱壳逆向，也未启动动态分析，故未完成风险台账写入（`record_risk`）与正式报告生成；`step_by_step_flow` 中步骤 1、6、8 的时序与叠层形态属基于 Manifest/资源证据的推断，标注为“不可静态还原”。如需闭环，下一步建议：动态运行 + UTG 抓取步骤 5/6 两页，并对 arm64 `libdpt.so` 定位解密后的 DEX 内存镜像以确认 `ACTION_ACCESSIBILITY_SETTINGS` 调用点与重跳定时器。

</details>
