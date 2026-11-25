# MR_100__ccc5736b1e｜Monokle — Ultra GPS Logger

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：178.6s

## 1. 一句话核心结论

- **核心申请方式**：该应用把真实功能藏在 XOR 二阶段 DEX 中，以标签为 AndroidSecurity 的伪装系统安全服务在开机/解锁广播后先用 root shell 命令静默写入 enabled_accessibility_services 自授权，失败才直接跳系统无障碍设置页，全程没有任何面向用户的引导界面或说明弹窗。
- **静态可见性说明**：外层 DEX 为壳加载器，真实载荷 assets/data.d 以 assets/data.e 的 512 字节循环 XOR 加密，但密钥与算法均硬编码于 LoaderApp.bDDiagonalsB(File) 中，已完整静态解密为 payload_stage2.dex（dex\n035），无障碍服务、自授权命令、设置页跳转逻辑全部可反编译确认；无 VMP、无远端下发 HTML、无二次网络解密。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ccc5736b1eb71a7783bc9fc62a5d16fabda33a306e9a842403ba24c3aac679cd` |
| 包名 / 年份 | `com.flashlight.ultra.gps.logger` / 2019 |
| 家族 / 品类 | **Monokle**（同池样本数：25） |
| 原始来源标识 | https://www.lookout.com/documents/threat-reports/lookout-discovers-monokle-threat-report.pdf |
| 桌面显示名 | Ultra GPS Logger |
| 引导页宣称品牌/身份 | 伪装为 Android 系统安全更新组件（服务名 AndroidSecurity / AndroidNotificationSecure，命名空间 com.system.security_update，含 com.smartagents.system_service.BackgroundService 动作） |
| 系统无障碍列表服务名 | AndroidSecurity |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：android:description 完全缺失，系统无障碍列表中只显示名称 AndroidSecurity 而无任何功能说明；无障碍配置使用 typeAllMask + flagIncludeNotImportantViews + canRetrieveWindowContent 最大权限但描述留空；包内混入 com.system.security_update / com.smartagents 两套仿系统命名空间；无障碍相关接收器 AccessibilityReceiver 使用伪 action "just.a.filter" 且可被 setComponentEnabledSetting 动态禁用；核心载荷以 assets/data.d + data.e 循环 XOR 二阶段释放，逃避静态特征匹配。 |
| 无障碍服务类名 | `com.system.security_update.accessibility.services.AccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PACKAGE_USAGE_STATS, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.flashlight.ultra.gps.logger.MyApplication_（继承 com.system.security_update.LoaderApp） | Application.onCreate()，任意组件启动即触发，无需用户交互 | 不可静态还原（无 UI，纯后台解密加载） | 无 | 无，用户完全不可见 | `com.system.security_update.LoaderApp.onCreate / LoaderApp.bDDiagonalsB(java.io.File)` |
| 2 | 业务功能触发 | com.system.security_update.receivers.StartBroadcastReceiver（BOOT_COMPLETED / QUICKBOOT_POWERON / MY_BOOT_COMPLETED / USER_PRESENT，priority=2147483647） | 开机完成或屏幕解锁 USER_PRESENT 广播 | 不可静态还原（广播接收器，无界面） | 无 | 无 | `com.system.security_update.receivers.StartBroadcastReceiver.onReceive → BackgroundService.ULAbstinence_theoryje` |
| 3 | 获权后动作（静默自授权，先于任何用户可见步骤） | com.system.security_update.BackgroundService.onCreate → ULCabEmpty_string.ULEquiprobableaL() | 服务创建时执行；先 ULMedicationtK() 轮询等待 root 检测通过（最多 30×200ms） | 不可静态还原（shell 命令执行，无界面） | **原文**：Try to enable accessibility<br>**译注**：日志输出“尝试启用无障碍”，随后执行 settings put secure enabled_accessibility_services 等命令 | 无，用户无需也无法确认；同时批量 appops 授予短信、通话、通讯录、录音、相机、悬浮窗、WRITE_SETTINGS 等权限 | `com.system.security_update.ULCabEmpty_string.ULEquiprobableaL` |
| 4 | 跳无障碍设置 | android.settings.ACCESSIBILITY_SETTINGS（系统无障碍设置页） | BackgroundService$1.run → ULCongregateZf() → ULProduct_portabilitywB(context)，条件为 AccessibilityService.ULCatalogingVE() 判定未启用 | 系统无障碍页 | **原文**：无（跳转前无任何应用内提示文案）<br>**译注**：直接打开系统无障碍设置页，用户看到列表中名为 AndroidSecurity 的服务项，无说明文字 | 用户在系统页中手动勾选名为 AndroidSecurity 的服务（应用本身不提供任何操作提示或替代路径） | `com.system.security_update.ULCabEmpty_string.ULProduct_portabilitywB` |
| 5 | 获权后动作 | com.system.security_update.accessibility.services.AccessibilityService | 系统绑定服务回调 onServiceConnected() | 不可静态还原（后台服务） | **原文**：***** onServiceConnected<br>**译注**：启动事件消费线程，将 AccessibilityEvent 与 getRootInActiveWindow() 成对放入队列，供后续控件读取与模拟操作 | 无 | `com.system.security_update.accessibility.services.AccessibilityService.onServiceConnected / onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍设置页服务列表项：仅由 Manifest 的 android:label="AndroidSecurity" 提供名称，android:description 未配置，无任何说明文字
- 应用内：无。载荷中不存在 AlertDialog、WebView、Toast 或自定义引导 Activity 的无障碍引导文案（payload_stage2.dex 全文检索 AlertDialog / WebView / 无障碍 / 辅助功能 均无引导类命中）
- 日志字符串（用户不可见）："Try to enable accessibility"、"Can't check root"，位于 com.system.security_update.ULCabEmpty_string 与 ULAscenderoc.log
- Manifest 通知监听服务 label："AndroidNotificationSecure"，同样仅出现在系统通知使用权列表中
- res/raw/hlp_bluetooth.html、hlp_provider.html、hlp_layout.html 为 GPS 功能帮助页，不含无障碍引导内容，与本链路无关

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | AndroidSecurity | 安卓安全（伪装为系统安全组件名） | `AndroidManifest.xml service android:label（com.system.security_update.accessibility.services.AccessibilityService）` | 假反诈安全 |
| en | AndroidNotificationSecure | 安卓通知安全（伪装为系统通知安全组件） | `AndroidManifest.xml service android:label（com.system.security_update.data.NotificationListener）` | 假反诈安全 |
| en | Try to enable accessibility | 尝试启用无障碍 | `payload_stage2.dex 硬编码字符串，com.system.security_update.ULCabEmpty_string.ULEquiprobableaL` | 未知 |
| en | settings put secure enabled_accessibility_services %accessibility:com.flashlight.ultra.gps.logger/com.system.security_update.accessibility.services.AccessibilityService | 通过 shell 直接写入系统安全设置，将本应用无障碍服务加入已启用列表（%accessibility: 前缀为系统 Shell 的辅助功能调用语法） | `payload_stage2.dex 硬编码字符串，com.system.security_update.ULCabEmpty_string.ULEquiprobableaL` | 未知 |
| en | Can't check root | 无法检测 root | `payload_stage2.dex 硬编码字符串，com.system.security_update.ULCabEmpty_string.ULMedicationtK` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无应用内循环重跳。拒绝或返回后，下一次 BOOT_COMPLETED / USER_PRESENT 广播会再次拉起 BackgroundService，ULCongregateZf() 中 ULProduct_portabilitywB() 每次检查 AccessibilityService.ULCatalogingVE() 未启用即再次 startActivity(ACCESSIBILITY_SETTINGS)，形成跨会话反复拉起而非前台死循环
- **遮罩叠层 / 高仿系统设置页**：无。未发现 TYPE_SYSTEM_ALERT 悬浮遮罩、高仿无障碍开关页或叠层指引；SYSTEM_ALERT_WINDOW 权限仅通过 appops set android:system_alert_window allow 静默获取，供其他用途
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无显式反卸载/阻止撤权逻辑（未发现 GLOBAL_ACTION_BACK/HOME 拦截或监听设置页自点确认）；但通过 shell 命令静默写入 enabled_accessibility_services 与 enabled_notification_listeners，用户无从察觉该授权来源
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 Activity 跳转 intent action = android.settings.ACCESSIBILITY_SETTINGS（由本应用进程发起，且跳转前栈内无任何应用内说明页）的瞬间拉起 UTG；或在收到 BOOT_COMPLETED/USER_PRESENT 后 BackgroundService 启动的 3-5 秒窗口内拉起，捕获其对系统设置页的直接跳转
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：一是静默自授权路径依赖 root/shell 能力，在无 root 的常规 UTG 设备上该路径不触发，只会看到直接跳系统设置，容易误判为普通跳转；二是真实功能藏在 XOR 二阶段 DEX（assets/data.d），静态扫描外壳 DEX 与资源时几乎看不到无障碍相关代码，必须解密后才能观察到。此外应用自身无任何引导文案，若 UTG 仅按“引导页文本特征”匹配会完全漏检，应以“后台发起 ACCESSIBILITY_SETTINGS 跳转 + 服务标签伪装系统品牌 + 描述为空”作为组合判据。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转瞬间的源栈快照（判定是否存在引导前置页）** | 启动 ACCESSIBILITY_SETTINGS 前一帧的 topActivity：预期为 GPS 主界面或后台无界面状态，而非任何说明/教学页 | 该样本的核心特征是零引导直接跳设置，捕获源栈即可与“有良性说明页再跳转”的正常应用区分开 | 跳转前栈顶是否为应用自身 Activity；是否存在任何应用内 Dialog/WebView 承载无障碍说明；跳转是否由后台 Service 线程发起（无用户点击事件） |
| **系统无障碍服务列表项** | 设置 > 无障碍 > 已安装服务，条目文本为 AndroidSecurity，下方无描述文字 | 服务名伪装成系统安全组件且描述为空，是最强的身份欺骗信号 | 条目文本 AndroidSecurity；描述区为空；条目所属应用为 Ultra GPS Logger（名称与标签错位） |
| **获权后的桌面/前台状态** | 返回桌面后是否存在后台常驻通知或悬浮窗，以及无障碍服务是否已被置为启用 | 验证自授权是否成功，以及获权后是否立即进入界面读取状态 | 设置中 enabled_accessibility_services 已包含本应用服务；通知使用权列表出现 AndroidNotificationSecure；无用户操作记录下服务即被启用 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.system.security_update.LoaderApp.bDDiagonalsB(java.io.File)`
- `com.system.security_update.BackgroundService.onCreate`
- `com.system.security_update.ULCabEmpty_string.ULEquiprobableaL`
- `com.system.security_update.ULCabEmpty_string.ULProduct_portabilitywB`
- `com.system.security_update.accessibility.services.AccessibilityService.onServiceConnected`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**核心发现：该应用并不存在“面向用户的无障碍引导流程”，引导环节被后台静默自授权与直接跳转系统设置页取代。**

1. **真实功能完全不在外壳 DEX 里**：`MyApplication_` 继承 `com.system.security_update.LoaderApp`；`onCreate()` 立即调用 [LoaderApp.bDDiagonalsB(Context)](<resource-unit:#1.dex1 code:com.system.security_update.LoaderApp#bDDiagonalsB(android.content.Context)>)，该方法的 File 重载用 `assets/data.e`（512 字节）作为循环密钥对 [assets/data.d](<resource-unit:#1 file:assets/data.d>)（2,588,572 字节）做 XOR，写出后再用 `DexClassLoader.findClass("com.system.security_update.App").getMethod("init", Context.class).invoke(...)` 反射执行。解出物头部为 `dex\n035`，**已静态还原为可反编译 DEX**（`payload_stage2.dex`）。
2. **身份伪装**：Manifest 中无障碍服务 label 为 `AndroidSecurity`，通知监听服务为 `AndroidNotificationSecure`，命名空间 `com.system.security_update` 全套模仿系统安全更新组件；桌面名仍是 `Ultra GPS Logger`，两者形成明显错位。
3. **能力极宽**：[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 声明 `typeAllMask`、`flagIncludeNotImportantViews`、`flagReportViewIds`、`canRetrieveWindowContent=true`，即读取全部界面内容。
4. **纯运行期路径（无任何引导 UI）**：`StartBroadcastReceiver`（BOOT_COMPLETED / USER_PRESENT，priority=2147483647）→ `BackgroundService.onCreate()` → `ULEquiprobableaL()` 先用 `settings put secure enabled_accessibility_services ...`、`accessibility_enabled 1`、`enabled_notification_listeners`、`appops ...` 等 shell 命令**静默自授权**；若判定未启用，则由 `ULProduct_portabilitywB()` 直接 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`——没有说明页、没有弹窗、没有取消按钮、没有 WebView 教学，也没有悬浮遮罩。
5. **获权后**：`onServiceConnected()` 起消费线程，`onAccessibilityEvent()` 把事件与 `getRootInActiveWindow()` 成对入队，为后续控件读取/模拟点击供料。
6. **预筛 HTML 无关**：`res/raw/hlp_bluetooth.html`、`hlp_provider.html`、`hlp_layout.html` 均为 GPS 工具自身的功能帮助页，不含无障碍引导内容；`strings` 中的 Google Play services 文案亦为 GMS 标准资源。
7. **对 UTG 的含义**：由于不存在应用内引导页，纯 UTG 应把“跳转 `ACCESSIBILITY_SETTINGS` 前是否出现过任何说明界面”本身作为判据——该样本为**零引导直接跳设置**，且服务名伪装为系统组件。

已登记风险 R-001（high / malware_trojan）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "外层 DEX 为壳加载器，真实载荷 assets/data.d 以 assets/data.e 的 512 字节循环 XOR 加密，但密钥与算法均硬编码于 LoaderApp.bDDiagonalsB(File) 中，已完整静态解密为 payload_stage2.dex（dex\\n035），无障碍服务、自授权命令、设置页跳转逻辑全部可反编译确认；无 VMP、无远端下发 HTML、无二次网络解密。",
  "summary_one_liner": "该应用把真实功能藏在 XOR 二阶段 DEX 中，以标签为 AndroidSecurity 的伪装系统安全服务在开机/解锁广播后先用 root shell 命令静默写入 enabled_accessibility_services 自授权，失败才直接跳系统无障碍设置页，全程没有任何面向用户的引导界面或说明弹窗。",
  "disguise_identity": {
    "app_display_name": "Ultra GPS Logger",
    "claimed_brand_or_persona": "伪装为 Android 系统安全更新组件（服务名 AndroidSecurity / AndroidNotificationSecure，命名空间 com.system.security_update，含 com.smartagents.system_service.BackgroundService 动作）",
    "a11y_service_label": "AndroidSecurity",
    "identity_mismatch": true,
    "obfuscation_tricks": "android:description 完全缺失，系统无障碍列表中只显示名称 AndroidSecurity 而无任何功能说明；无障碍配置使用 typeAllMask + flagIncludeNotImportantViews + canRetrieveWindowContent 最大权限但描述留空；包内混入 com.system.security_update / com.smartagents 两套仿系统命名空间；无障碍相关接收器 AccessibilityReceiver 使用伪 action \"just.a.filter\" 且可被 setComponentEnabledSetting 动态禁用；核心载荷以 assets/data.d + data.e 循环 XOR 二阶段释放，逃避静态特征匹配。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.flashlight.ultra.gps.logger.MyApplication_（继承 com.system.security_update.LoaderApp）",
      "trigger_event": "Application.onCreate()，任意组件启动即触发，无需用户交互",
      "ui_carrier": "不可静态还原（无 UI，纯后台解密加载）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面呈现，静默完成 assets/data.d 的 XOR 解密与 DexClassLoader 加载",
      "user_action_requested": "无，用户完全不可见",
      "code_anchor": "com.system.security_update.LoaderApp.onCreate / LoaderApp.bDDiagonalsB(java.io.File)"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.system.security_update.receivers.StartBroadcastReceiver（BOOT_COMPLETED / QUICKBOOT_POWERON / MY_BOOT_COMPLETED / USER_PRESENT，priority=2147483647）",
      "trigger_event": "开机完成或屏幕解锁 USER_PRESENT 广播",
      "ui_carrier": "不可静态还原（广播接收器，无界面）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，后台拉起 BackgroundService",
      "user_action_requested": "无",
      "code_anchor": "com.system.security_update.receivers.StartBroadcastReceiver.onReceive → BackgroundService.ULAbstinence_theoryje"
    },
    {
      "step": 3,
      "stage": "获权后动作（静默自授权，先于任何用户可见步骤）",
      "screen_or_component": "com.system.security_update.BackgroundService.onCreate → ULCabEmpty_string.ULEquiprobableaL()",
      "trigger_event": "服务创建时执行；先 ULMedicationtK() 轮询等待 root 检测通过（最多 30×200ms）",
      "ui_carrier": "不可静态还原（shell 命令执行，无界面）",
      "shown_text_verbatim": "Try to enable accessibility",
      "shown_text_zh": "日志输出“尝试启用无障碍”，随后执行 settings put secure enabled_accessibility_services 等命令",
      "user_action_requested": "无，用户无需也无法确认；同时批量 appops 授予短信、通话、通讯录、录音、相机、悬浮窗、WRITE_SETTINGS 等权限",
      "code_anchor": "com.system.security_update.ULCabEmpty_string.ULEquiprobableaL"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS（系统无障碍设置页）",
      "trigger_event": "BackgroundService$1.run → ULCongregateZf() → ULProduct_portabilitywB(context)，条件为 AccessibilityService.ULCatalogingVE() 判定未启用",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（跳转前无任何应用内提示文案）",
      "shown_text_zh": "直接打开系统无障碍设置页，用户看到列表中名为 AndroidSecurity 的服务项，无说明文字",
      "user_action_requested": "用户在系统页中手动勾选名为 AndroidSecurity 的服务（应用本身不提供任何操作提示或替代路径）",
      "code_anchor": "com.system.security_update.ULCabEmpty_string.ULProduct_portabilitywB"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.system.security_update.accessibility.services.AccessibilityService",
      "trigger_event": "系统绑定服务回调 onServiceConnected()",
      "ui_carrier": "不可静态还原（后台服务）",
      "shown_text_verbatim": "***** onServiceConnected",
      "shown_text_zh": "启动事件消费线程，将 AccessibilityEvent 与 getRootInActiveWindow() 成对放入队列，供后续控件读取与模拟操作",
      "user_action_requested": "无",
      "code_anchor": "com.system.security_update.accessibility.services.AccessibilityService.onServiceConnected / onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍设置页服务列表项：仅由 Manifest 的 android:label=\"AndroidSecurity\" 提供名称，android:description 未配置，无任何说明文字",
    "应用内：无。载荷中不存在 AlertDialog、WebView、Toast 或自定义引导 Activity 的无障碍引导文案（payload_stage2.dex 全文检索 AlertDialog / WebView / 无障碍 / 辅助功能 均无引导类命中）",
    "日志字符串（用户不可见）：\"Try to enable accessibility\"、\"Can't check root\"，位于 com.system.security_update.ULCabEmpty_string 与 ULAscenderoc.log",
    "Manifest 通知监听服务 label：\"AndroidNotificationSecure\"，同样仅出现在系统通知使用权列表中",
    "res/raw/hlp_bluetooth.html、hlp_provider.html、hlp_layout.html 为 GPS 功能帮助页，不含无障碍引导内容，与本链路无关"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "AndroidSecurity",
      "text_zh": "安卓安全（伪装为系统安全组件名）",
      "source_location": "AndroidManifest.xml service android:label（com.system.security_update.accessibility.services.AccessibilityService）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "AndroidNotificationSecure",
      "text_zh": "安卓通知安全（伪装为系统通知安全组件）",
      "source_location": "AndroidManifest.xml service android:label（com.system.security_update.data.NotificationListener）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Try to enable accessibility",
      "text_zh": "尝试启用无障碍",
      "source_location": "payload_stage2.dex 硬编码字符串，com.system.security_update.ULCabEmpty_string.ULEquiprobableaL",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "settings put secure enabled_accessibility_services %accessibility:com.flashlight.ultra.gps.logger/com.system.security_update.accessibility.services.AccessibilityService",
      "text_zh": "通过 shell 直接写入系统安全设置，将本应用无障碍服务加入已启用列表（%accessibility: 前缀为系统 Shell 的辅助功能调用语法）",
      "source_location": "payload_stage2.dex 硬编码字符串，com.system.security_update.ULCabEmpty_string.ULEquiprobableaL",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Can't check root",
      "text_zh": "无法检测 root",
      "source_location": "payload_stage2.dex 硬编码字符串，com.system.security_update.ULCabEmpty_string.ULMedicationtK",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无应用内循环重跳。拒绝或返回后，下一次 BOOT_COMPLETED / USER_PRESENT 广播会再次拉起 BackgroundService，ULCongregateZf() 中 ULProduct_portabilitywB() 每次检查 AccessibilityService.ULCatalogingVE() 未启用即再次 startActivity(ACCESSIBILITY_SETTINGS)，形成跨会话反复拉起而非前台死循环",
    "overlay_or_fake_settings": "无。未发现 TYPE_SYSTEM_ALERT 悬浮遮罩、高仿无障碍开关页或叠层指引；SYSTEM_ALERT_WINDOW 权限仅通过 appops set android:system_alert_window allow 静默获取，供其他用途",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无显式反卸载/阻止撤权逻辑（未发现 GLOBAL_ACTION_BACK/HOME 拦截或监听设置页自点确认）；但通过 shell 命令静默写入 enabled_accessibility_services 与 enabled_notification_listeners，用户无从察觉该授权来源",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 Activity 跳转 intent action = android.settings.ACCESSIBILITY_SETTINGS（由本应用进程发起，且跳转前栈内无任何应用内说明页）的瞬间拉起 UTG；或在收到 BOOT_COMPLETED/USER_PRESENT 后 BackgroundService 启动的 3-5 秒窗口内拉起，捕获其对系统设置页的直接跳转",
    "key_pages_to_capture": [
      {
        "page_role": "跳转瞬间的源栈快照（判定是否存在引导前置页）",
        "page_identifier": "启动 ACCESSIBILITY_SETTINGS 前一帧的 topActivity：预期为 GPS 主界面或后台无界面状态，而非任何说明/教学页",
        "why_most_useful": "该样本的核心特征是零引导直接跳设置，捕获源栈即可与“有良性说明页再跳转”的正常应用区分开",
        "observable_utg_signals": ["跳转前栈顶是否为应用自身 Activity", "是否存在任何应用内 Dialog/WebView 承载无障碍说明", "跳转是否由后台 Service 线程发起（无用户点击事件）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 > 无障碍 > 已安装服务，条目文本为 AndroidSecurity，下方无描述文字",
        "why_most_useful": "服务名伪装成系统安全组件且描述为空，是最强的身份欺骗信号",
        "observable_utg_signals": ["条目文本 AndroidSecurity", "描述区为空", "条目所属应用为 Ultra GPS Logger（名称与标签错位）"]
      },
      {
        "page_role": "获权后的桌面/前台状态",
        "page_identifier": "返回桌面后是否存在后台常驻通知或悬浮窗，以及无障碍服务是否已被置为启用",
        "why_most_useful": "验证自授权是否成功，以及获权后是否立即进入界面读取状态",
        "observable_utg_signals": ["设置中 enabled_accessibility_services 已包含本应用服务", "通知使用权列表出现 AndroidNotificationSecure", "无用户操作记录下服务即被启用"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：一是静默自授权路径依赖 root/shell 能力，在无 root 的常规 UTG 设备上该路径不触发，只会看到直接跳系统设置，容易误判为普通跳转；二是真实功能藏在 XOR 二阶段 DEX（assets/data.d），静态扫描外壳 DEX 与资源时几乎看不到无障碍相关代码，必须解密后才能观察到。此外应用自身无任何引导文案，若 UTG 仅按“引导页文本特征”匹配会完全漏检，应以“后台发起 ACCESSIBILITY_SETTINGS 跳转 + 服务标签伪装系统品牌 + 描述为空”作为组合判据。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.system.security_update.LoaderApp.bDDiagonalsB(java.io.File)",
    "com.system.security_update.BackgroundService.onCreate",
    "com.system.security_update.ULCabEmpty_string.ULEquiprobableaL",
    "com.system.security_update.ULCabEmpty_string.ULProduct_portabilitywB",
    "com.system.security_update.accessibility.services.AccessibilityService.onServiceConnected",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
