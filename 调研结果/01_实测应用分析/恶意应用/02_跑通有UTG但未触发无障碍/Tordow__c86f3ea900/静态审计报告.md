# MR_042__c86f3ea900｜Tordow — Android Security Update

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：97.9s

## 1. 一句话核心结论

- **核心申请方式**：应用冷启动即禁用自身图标并跳回桌面，仅后台从硬编码 C2 拉取并解密远端 DEX，由空壳无障碍服务反射加载真实模块来完成后续的无障碍权限诱导与操控，本地无任何引导界面。
- **静态可见性说明**：本地 classes.dex 完整可读（29 类），但其中不存在任何 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转点，也没有引导文案、弹窗、HTML 教学页或遮罩代码。无障碍开启引导、页面流转、点击模拟与设置页操控逻辑全部位于 http://5.45.70.34/cryptocomponent.1 下载、经 CryptoUtil 解密为 DEX_API.apk 后用 DexClassLoader 加载的 com.raccoon.Accessibility 远端载荷中，该载荷不随包分发，无法静态获取。可静态确认的只有：空壳无障碍服务、反射转发通道、远端下载地址与 MD5 校验重试、俄语/英语预置 UI 资源。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c86f3ea9002ca83fdf1c8f2c9118c317999ab204d83bbaefc0d959850d49ba50` |
| 包名 / 年份 | `com.example.raccoonapi2` / 2016 |
| 家族 / 品类 | **Tordow**（同池样本数：2） |
| 原始来源标识 | https://securelist.com/the-banker-that-can-steal-anything/76101/ |
| 桌面显示名 | Android Security Update |
| 引导页宣称品牌/身份 | 伪造成 Android 系统安全更新/系统策略监控程序（启动 Activity 自称 Android Policy Monitor） |
| 系统无障碍列表服务名 | 系统无障碍列表按 manifest 服务名展示 com.API2.DummyAccessibility，描述取自 @string/description_that_shows_on_the_accessibility_page，其值仅为占位符 "description" |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍描述为无意义占位符 "description"，在系统列表中呈近乎空白以弱化用户警惕；桌面名(Android Security Update)、Activity 标签(Android Policy Monitor)、真实代码包(com.API2 / com.raccoon.Accessibility)三套身份互不一致；MainActivity 在 onCreate 中禁用自身组件并跳转 CATEGORY_HOME，实现图标消失、无前台入口的隐蔽驻留；核心类通过反射加载，类名与调用关系静态不可见 |
| 无障碍服务类名 | `com.API2.DummyAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | description |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.API2.MainActivity（android:noHistory="true"，LAUNCHER） | 用户点击桌面图标 → onCreate() | 原生Activity | 无 | 无（用户无需操作，页面瞬间消失） | `com.API2.MainActivity.onCreate` |
| 2 | 冷启动入口 | PackageManager.setComponentEnabledSetting(this, COMPONENT_ENABLED_STATE_DISABLED(2), DONT_KILL_APP(1)) + Intent(ACTION_MAIN, CATEGORY_HOME) | onCreate 内顺序执行：先禁用自身组件，再 startActivity 跳转桌面 | 系统桌面（Launcher） | 无 | 无；用户此时已无法通过图标再次进入 | `com.API2.MainActivity.onCreate` |
| 3 | 获权后动作 | com.API2.My2Service → com.API2.API2Service._onStartCommand → Thread(API2Service$ST) → com.API2.Loader.run | MainActivity.onCreate 末尾 startService(My2Service)；后续由 MyReceiver 的 BOOT_COMPLETED / CONNECTIVITY_CHANGE 等广播复启 | 不可静态还原（后台服务） | 无 | 无 | `com.API2.Loader.run / com.API2.Config#server` |
| 4 | 获权后动作 | com.API2.Reflector.loadClass → CryptoUtil.decrypt(cryptocomponent.1 → DEX_API.apk) → dalvik.system.DexClassLoader → Class.forName("com.raccoon.Accessibility") | API2Service$ST.run / API2Receiver$RT.run / DummyAccessibility.onServiceConnected 三处调用 loadClass | 不可静态还原（解密后的远端 DEX） | 无 | 无 | `com.API2.Reflector.loadClass / com.API2.CryptoUtil.decrypt` |
| 5 | 跳无障碍设置 | 远端载荷 com.raccoon.Accessibility（预期由 DummyAccessibility 反射代理执行） | 远端模块逻辑（推测在 onServiceConnected 或首个 onAccessibilityEvent 时触发），本地代码无对应跳转点 | 不可静态还原 | **原文**：无（本地包内无任何无障碍引导文案）<br>**译注**：本地无 ACTION_ACCESSIBILITY_SETTINGS 跳转，无法静态确认引导页形态与文案 | 不可静态确认 | `com.API2.DummyAccessibility.onServiceConnected（反射转发 com.raccoon.Accessibility#onServiceConnected）` |
| 6 | 获权后动作 | com.API2.DummyAccessibility.onAccessibilityEvent → 反射调用 com.raccoon.Accessibility#onAccessibilityEvent | 系统无障碍事件回调（每个窗口/点击事件均被转发） | 不可静态还原 | 无 | 无 | `com.API2.DummyAccessibility.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml 的 description_that_shows_on_the_accessibility_page 值为占位符 "description"，经 res/xml/accessibilityservice.xml 的 android:description 呈现在系统设置→无障碍→服务列表中，作为该服务的唯一官方说明
- res/layout/agreement.xml：标题 TextView 硬编码 "Android Security Update"，正文为整段 GNU GPL 全文，底部 "Accept" 按钮 —— 免责/授权掩护页，本地代码无引用点，仅可由远端模块 inflate
- res/layout/info.xml：俄语来电号码浮层（"Номер телефона звонящего" / "Закрыть"），白色全屏背景，为通话界面覆盖做准备
- assets/page2.xml：俄语占位页 "Это страница 2!"，配 assets/style.css，供 WebView 加载用的本地 HTML 骨架
- res/layout/activity_main.xml：仅一个 @string/hello_world（俄语 "Привет мир!"）TextView，为残留模板页
- 桌面图标名称：Android Security Update；启动 Activity 标签：Android Policy Monitor（Manifest 声明）
- 真正的无障碍开启引导、权限分步教学、遮罩叠层与拒权重跳提示均未出现在包内，位于加密远端 DEX（com.raccoon.Accessibility），运行期才由网络下发

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Android Security Update | 安卓安全更新 | `AndroidManifest.xml android:label / res/layout/agreement.xml textView1` | 假更新 |
| en | Android Policy Monitor | 安卓策略监控器 | `AndroidManifest.xml com.API2.MainActivity android:label` | 假反诈安全 |
| en | description | 描述（无实际含义的占位符，系统无障碍列表中呈现近乎空白说明） | `res/values/strings.xml key=description_that_shows_on_the_accessibility_page → res/xml/accessibilityservice.xml android:description` | 教唆忽视警告 |
| en | Accept | 接受 | `res/layout/agreement.xml button1` | 假更新 |
| en | The GNU General Public License is a free, copyleft license for software and other kinds of works. | GNU 通用公共许可证是一种自由的、保留版权的软件及其他作品许可证。 | `res/layout/agreement.xml textView2（整段 GPL 全文硬编码）` | 未知 |
| ru | Номер телефона звонящего | 来电者电话号码 | `res/layout/info.xml（textViewNumber 浮层标题）` | 未知 |
| ru | Закрыть | 关闭 | `res/layout/info.xml buttonClose` | 未知 |
| ru | Это страница 2! | 这是第 2 页！ | `assets/page2.xml` | 未知 |
| ru | Привет мир! | 你好，世界！ | `res/values/strings.xml key=hello_world → res/layout/activity_main.xml` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：本地包内既无引导页也无重跳逻辑；已确认的循环机制仅存在于载荷获取环节——Loader.run 在 MD5 不匹配时 do-while 无限重下，以及 MyReceiver 注册 BOOT_COMPLETED/CONNECTIVITY_CHANGE 等 9 个广播（priority 1000）用于后台反复拉起。无障碍拒权后的重跳行为取决于远端 com.raccoon.Accessibility 实现。
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；但 Manifest 已申请 SYSTEM_ALERT_WINDOW，且 res/layout/info.xml 提供了可全屏覆盖通话界面的俄语号码浮层模板，具备叠层能力。
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（本地无 ACTION_APPLICATION_DETAILS_SETTINGS 及任何受限设置教学文案；targetSdkVersion=23，若在 Android 13+ 设备运行需远端载荷自行处理，不可静态确认）
- **获权后即时行为与防撤权机制**：本地可见间接反移除机制：MainActivity.onCreate 主动禁用自身 LAUNCHER 组件使图标消失，配合后台服务与高优先级广播常驻；获权后是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权取决于远端模块，不可静态确认
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：包内无引导页，最佳时机为：设备启动或任意网络变化后监测 MyReceiver 被拉起 → My2Service 启动 → 出现对 5.45.70.34 的 HTTP 请求（/cryptocomponent.1 与 .md5）→ DexClassLoader 加载后，监测进程内是否新出现 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的 startActivity 调用；同时在冷启动瞬间抓取 MainActivity（图标消失、跳回桌面）与 DummyAccessibility 被启用前后的系统无障碍列表页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：核心引导流程完全位于 AES 加密、网络下发的远端 DEX（com.raccoon.Accessibility），包内一阶段仅为空壳反射代理，静态无法还原任何引导文案、跳转时机与拒权重跳逻辑；若 C2 5.45.70.34 不可达，Loader 会卡在 MD5 校验的 do-while 死循环，应用将永远不展示引导界面，UTG 只能观测到“图标消失 + 静默联网 + 无障碍服务空描述”这一前置形态。另需注意：无障碍描述为占位符，纯文本抓取时信息量极低，须结合服务名与包名比对判定。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（服务被启用前的原始呈现）** | 设置→无障碍→已下载/已安装服务中名为 com.API2.DummyAccessibility 的条目，描述显示为 "description" | 这是唯一由包内静态资源决定的可见界面，可直接证明身份伪装与描述占位，且不依赖远端载荷是否可下载 | 服务描述文本恰为占位符 description；服务名与桌面名 Android Security Update 完全不对应；无任何功能说明与用途告知 |
| **远端载荷下发后弹出的引导说明页（一阶段下载成功后）** | DexClassLoader 加载完成后新出现的 Activity/Dialog/WebView，内容含俄语或英语的无障碍开启教学 | 本地无引导代码，只有该页能揭示真实诱导文案与是否可取消/跳过 | 首次出现的非 Manifest 声明组件界面；文本中包含 无障碍/специальные возможности/accessibility 关键词；是否存在取消或跳过按钮 |
| **跳转系统设置后的遮罩叠层页** | SYSTEM_ALERT_WINDOW 悬浮窗覆盖在无障碍设置页之上，或 res/layout/info.xml 类浮层 | 判断是否以遮罩指引/伪造开关页方式引导，是区分恶意诱导与正常引导的关键 | 悬浮窗窗口类型为 TYPE_APPLICATION_OVERLAY；遮罩内含指向具体开关位置的箭头或手指提示；遮罩可点击区域与系统开关位置重叠 |
| **预置免责掩护页（可能被远端 inflate 展示）** | 标题 Android Security Update + 整段 GPL 正文 + 单一 Accept 按钮的页面 | 确认恶意方是否用无关法律文本伪装合规告知、且不提供拒绝路径 | 正文为 GPL 全文而非隐私/权限说明；仅有一个 Accept 按钮，无拒绝/退出；标题冒充系统安全更新 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.API2.MainActivity.onCreate`
- `com.API2.DummyAccessibility.onServiceConnected`
- `com.API2.DummyAccessibility.onAccessibilityEvent`
- `com.API2.Reflector.loadClass`
- `com.API2.Loader.run`
- `res/values/strings.xml#L5 (description_that_shows_on_the_accessibility_page)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验）

**可见性判定：核心引导逻辑不在包内，而位于 AES 加密的远端 DEX 中**

- 本地 DEX 仅 29 个类，**不含** `ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS` 字符串；全包也没有任何无障碍引导文案、弹窗或 HTML 教学页，因此运行期“如何引导开启无障碍”的分步流程**无法静态还原**。
- 已确认的分层结构（属于典型 Tordow/Raccoon 式模块化木马）：
  1. [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.API2.MainActivity#onCreate>) 冷启动后**立即调用 `setComponentEnabledSetting(..., 2, 1)` 禁用自身启动组件**，使桌面图标消失；随后跳转 `CATEGORY_HOME`，并启动 `My2Service`。也就是说，它没有任何前置 UI。
  2. `My2Service` → [API2Service._onStartCommand()](<resource-unit:#1.dex1 code:com.API2.API2Service#_onStartCommand>) 启动线程，[Loader.run()](<resource-unit:#1.dex1 code:com.API2.Loader#run>) 从 [Config](<resource-unit:#1.dex1 code:com.API2.Config#server>) 中的 `http://5.45.70.34` 循环下载 `/cryptocomponent.1` 并校验 MD5（失败后重试，形成死循环）。
  3. [Reflector.loadClass()](<resource-unit:#1.dex1 code:com.API2.Reflector#loadClass>) 经 `CryptoUtil.decrypt()` 解密为 `DEX_API.apk`，再通过 `DexClassLoader` 加载 `com.raccoon.Accessibility` 并删除明文。
  4. [DummyAccessibility.onServiceConnected()](<resource-unit:#1.dex1 code:com.API2.DummyAccessibility#onServiceConnected>) 作为**空壳无障碍服务**，用反射把 `onAccessibilityEvent`、`onInterrupt`、`onServiceConnected` 全部转发给远端类。因此，真实的手势操控、页面点击和设置页跳转都在远端载荷内。
- **身份伪装证据（本地可确认）**：桌面名 `Android Security Update`；启动 Activity 标签 `Android Policy Monitor`；无障碍配置描述仅为占位符 [description_that_shows_on_the_accessibility_page](<resource-unit:#1 file:res/values/strings.xml#L5>)，值就是 `description`，在系统无障碍列表中毫无说明力，属于典型的“空白或占位挤出警告”。
- **本地预置 UI 资源全部指向远端的后续行为**：[agreement.xml](<resource-unit:#1 file:res/layout/agreement.xml>) 用 GPL 全文和 `Accept` 按钮做免责掩护，标题却是 `Android Security Update`；[info.xml](<resource-unit:#1 file:res/layout/info.xml>) 是俄语来电号码浮层（`Номер телефона звонящего` / `Закрыть`）；[page2.xml](<resource-unit:#1 file:assets/page2.xml>) 是俄语占位 `Это страница 2!`。这些布局在本地代码中无任何引用点，仅由远端模块通过反射渲染。
- `ActivityTwo` 反编译为空，`DummyActivity` 的 `onCreate`、`onResume` 均为纯反射转发；这进一步说明引导页、遮罩和跳转动作全部由远端下发。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "本地 classes.dex 完整可读（29 类），但其中不存在任何 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转点，也没有引导文案、弹窗、HTML 教学页或遮罩代码。无障碍开启引导、页面流转、点击模拟与设置页操控逻辑全部位于 http://5.45.70.34/cryptocomponent.1 下载、经 CryptoUtil 解密为 DEX_API.apk 后用 DexClassLoader 加载的 com.raccoon.Accessibility 远端载荷中，该载荷不随包分发，无法静态获取。可静态确认的只有：空壳无障碍服务、反射转发通道、远端下载地址与 MD5 校验重试、俄语/英语预置 UI 资源。",
  "summary_one_liner": "应用冷启动即禁用自身图标并跳回桌面，仅后台从硬编码 C2 拉取并解密远端 DEX，由空壳无障碍服务反射加载真实模块来完成后续的无障碍权限诱导与操控，本地无任何引导界面。",
  "disguise_identity": {
    "app_display_name": "Android Security Update",
    "claimed_brand_or_persona": "伪造成 Android 系统安全更新/系统策略监控程序（启动 Activity 自称 Android Policy Monitor）",
    "a11y_service_label": "系统无障碍列表按 manifest 服务名展示 com.API2.DummyAccessibility，描述取自 @string/description_that_shows_on_the_accessibility_page，其值仅为占位符 \"description\"",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍描述为无意义占位符 \"description\"，在系统列表中呈近乎空白以弱化用户警惕；桌面名(Android Security Update)、Activity 标签(Android Policy Monitor)、真实代码包(com.API2 / com.raccoon.Accessibility)三套身份互不一致；MainActivity 在 onCreate 中禁用自身组件并跳转 CATEGORY_HOME，实现图标消失、无前台入口的隐蔽驻留；核心类通过反射加载，类名与调用关系静态不可见"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.API2.MainActivity（android:noHistory=\"true\"，LAUNCHER）",
      "trigger_event": "用户点击桌面图标 → onCreate()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 不加载任何布局，无可见界面",
      "user_action_requested": "无（用户无需操作，页面瞬间消失）",
      "code_anchor": "com.API2.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "PackageManager.setComponentEnabledSetting(this, COMPONENT_ENABLED_STATE_DISABLED(2), DONT_KILL_APP(1)) + Intent(ACTION_MAIN, CATEGORY_HOME)",
      "trigger_event": "onCreate 内顺序执行：先禁用自身组件，再 startActivity 跳转桌面",
      "ui_carrier": "系统桌面（Launcher）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "应用图标从桌面消失，界面回到系统桌面，用户被送回主屏",
      "user_action_requested": "无；用户此时已无法通过图标再次进入",
      "code_anchor": "com.API2.MainActivity.onCreate"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "com.API2.My2Service → com.API2.API2Service._onStartCommand → Thread(API2Service$ST) → com.API2.Loader.run",
      "trigger_event": "MainActivity.onCreate 末尾 startService(My2Service)；后续由 MyReceiver 的 BOOT_COMPLETED / CONNECTIVITY_CHANGE 等广播复启",
      "ui_carrier": "不可静态还原（后台服务）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；后台静默向 http://5.45.70.34 拉取 /cryptocomponent.1 并比对 /cryptocomponent.1.md5，校验不符则无限重下",
      "user_action_requested": "无",
      "code_anchor": "com.API2.Loader.run / com.API2.Config#server"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.API2.Reflector.loadClass → CryptoUtil.decrypt(cryptocomponent.1 → DEX_API.apk) → dalvik.system.DexClassLoader → Class.forName(\"com.raccoon.Accessibility\")",
      "trigger_event": "API2Service$ST.run / API2Receiver$RT.run / DummyAccessibility.onServiceConnected 三处调用 loadClass",
      "ui_carrier": "不可静态还原（解密后的远端 DEX）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "解密加载远端模块后立即删除明文 DEX_API.apk，真实业务类 com.raccoon.Accessibility 就此进入执行路径",
      "user_action_requested": "无",
      "code_anchor": "com.API2.Reflector.loadClass / com.API2.CryptoUtil.decrypt"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "远端载荷 com.raccoon.Accessibility（预期由 DummyAccessibility 反射代理执行）",
      "trigger_event": "远端模块逻辑（推测在 onServiceConnected 或首个 onAccessibilityEvent 时触发），本地代码无对应跳转点",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（本地包内无任何无障碍引导文案）",
      "shown_text_zh": "本地无 ACTION_ACCESSIBILITY_SETTINGS 跳转，无法静态确认引导页形态与文案",
      "user_action_requested": "不可静态确认",
      "code_anchor": "com.API2.DummyAccessibility.onServiceConnected（反射转发 com.raccoon.Accessibility#onServiceConnected）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.API2.DummyAccessibility.onAccessibilityEvent → 反射调用 com.raccoon.Accessibility#onAccessibilityEvent",
      "trigger_event": "系统无障碍事件回调（每个窗口/点击事件均被转发）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后所有无障碍事件被无过滤地转发至远端模块，为其页面操控、短信/通话界面劫持提供通道",
      "user_action_requested": "无",
      "code_anchor": "com.API2.DummyAccessibility.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml 的 description_that_shows_on_the_accessibility_page 值为占位符 \"description\"，经 res/xml/accessibilityservice.xml 的 android:description 呈现在系统设置→无障碍→服务列表中，作为该服务的唯一官方说明",
    "res/layout/agreement.xml：标题 TextView 硬编码 \"Android Security Update\"，正文为整段 GNU GPL 全文，底部 \"Accept\" 按钮 —— 免责/授权掩护页，本地代码无引用点，仅可由远端模块 inflate",
    "res/layout/info.xml：俄语来电号码浮层（\"Номер телефона звонящего\" / \"Закрыть\"），白色全屏背景，为通话界面覆盖做准备",
    "assets/page2.xml：俄语占位页 \"Это страница 2!\"，配 assets/style.css，供 WebView 加载用的本地 HTML 骨架",
    "res/layout/activity_main.xml：仅一个 @string/hello_world（俄语 \"Привет мир!\"）TextView，为残留模板页",
    "桌面图标名称：Android Security Update；启动 Activity 标签：Android Policy Monitor（Manifest 声明）",
    "真正的无障碍开启引导、权限分步教学、遮罩叠层与拒权重跳提示均未出现在包内，位于加密远端 DEX（com.raccoon.Accessibility），运行期才由网络下发"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Android Security Update",
      "text_zh": "安卓安全更新",
      "source_location": "AndroidManifest.xml android:label / res/layout/agreement.xml textView1",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Policy Monitor",
      "text_zh": "安卓策略监控器",
      "source_location": "AndroidManifest.xml com.API2.MainActivity android:label",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "description",
      "text_zh": "描述（无实际含义的占位符，系统无障碍列表中呈现近乎空白说明）",
      "source_location": "res/values/strings.xml key=description_that_shows_on_the_accessibility_page → res/xml/accessibilityservice.xml android:description",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Accept",
      "text_zh": "接受",
      "source_location": "res/layout/agreement.xml button1",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "The GNU General Public License is a free, copyleft license for software and other kinds of works.",
      "text_zh": "GNU 通用公共许可证是一种自由的、保留版权的软件及其他作品许可证。",
      "source_location": "res/layout/agreement.xml textView2（整段 GPL 全文硬编码）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "Номер телефона звонящего",
      "text_zh": "来电者电话号码",
      "source_location": "res/layout/info.xml（textViewNumber 浮层标题）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "Закрыть",
      "text_zh": "关闭",
      "source_location": "res/layout/info.xml buttonClose",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "Это страница 2!",
      "text_zh": "这是第 2 页！",
      "source_location": "assets/page2.xml",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "ru",
      "text_verbatim": "Привет мир!",
      "text_zh": "你好，世界！",
      "source_location": "res/values/strings.xml key=hello_world → res/layout/activity_main.xml",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：本地包内既无引导页也无重跳逻辑；已确认的循环机制仅存在于载荷获取环节——Loader.run 在 MD5 不匹配时 do-while 无限重下，以及 MyReceiver 注册 BOOT_COMPLETED/CONNECTIVITY_CHANGE 等 9 个广播（priority 1000）用于后台反复拉起。无障碍拒权后的重跳行为取决于远端 com.raccoon.Accessibility 实现。",
    "overlay_or_fake_settings": "不可静态还原；但 Manifest 已申请 SYSTEM_ALERT_WINDOW，且 res/layout/info.xml 提供了可全屏覆盖通话界面的俄语号码浮层模板，具备叠层能力。",
    "restricted_settings_13plus_coaching": "无静态证据（本地无 ACTION_APPLICATION_DETAILS_SETTINGS 及任何受限设置教学文案；targetSdkVersion=23，若在 Android 13+ 设备运行需远端载荷自行处理，不可静态确认）",
    "post_grant_anti_removal": "本地可见间接反移除机制：MainActivity.onCreate 主动禁用自身 LAUNCHER 组件使图标消失，配合后台服务与高优先级广播常驻；获权后是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权取决于远端模块，不可静态确认",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "包内无引导页，最佳时机为：设备启动或任意网络变化后监测 MyReceiver 被拉起 → My2Service 启动 → 出现对 5.45.70.34 的 HTTP 请求（/cryptocomponent.1 与 .md5）→ DexClassLoader 加载后，监测进程内是否新出现 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的 startActivity 调用；同时在冷启动瞬间抓取 MainActivity（图标消失、跳回桌面）与 DummyAccessibility 被启用前后的系统无障碍列表页。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（服务被启用前的原始呈现）",
        "page_identifier": "设置→无障碍→已下载/已安装服务中名为 com.API2.DummyAccessibility 的条目，描述显示为 \"description\"",
        "why_most_useful": "这是唯一由包内静态资源决定的可见界面，可直接证明身份伪装与描述占位，且不依赖远端载荷是否可下载",
        "observable_utg_signals": ["服务描述文本恰为占位符 description", "服务名与桌面名 Android Security Update 完全不对应", "无任何功能说明与用途告知"]
      },
      {
        "page_role": "远端载荷下发后弹出的引导说明页（一阶段下载成功后）",
        "page_identifier": "DexClassLoader 加载完成后新出现的 Activity/Dialog/WebView，内容含俄语或英语的无障碍开启教学",
        "why_most_useful": "本地无引导代码，只有该页能揭示真实诱导文案与是否可取消/跳过",
        "observable_utg_signals": ["首次出现的非 Manifest 声明组件界面", "文本中包含 无障碍/специальные возможности/accessibility 关键词", "是否存在取消或跳过按钮"]
      },
      {
        "page_role": "跳转系统设置后的遮罩叠层页",
        "page_identifier": "SYSTEM_ALERT_WINDOW 悬浮窗覆盖在无障碍设置页之上，或 res/layout/info.xml 类浮层",
        "why_most_useful": "判断是否以遮罩指引/伪造开关页方式引导，是区分恶意诱导与正常引导的关键",
        "observable_utg_signals": ["悬浮窗窗口类型为 TYPE_APPLICATION_OVERLAY", "遮罩内含指向具体开关位置的箭头或手指提示", "遮罩可点击区域与系统开关位置重叠"]
      },
      {
        "page_role": "预置免责掩护页（可能被远端 inflate 展示）",
        "page_identifier": "标题 Android Security Update + 整段 GPL 正文 + 单一 Accept 按钮的页面",
        "why_most_useful": "确认恶意方是否用无关法律文本伪装合规告知、且不提供拒绝路径",
        "observable_utg_signals": ["正文为 GPL 全文而非隐私/权限说明", "仅有一个 Accept 按钮，无拒绝/退出", "标题冒充系统安全更新"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：核心引导流程完全位于 AES 加密、网络下发的远端 DEX（com.raccoon.Accessibility），包内一阶段仅为空壳反射代理，静态无法还原任何引导文案、跳转时机与拒权重跳逻辑；若 C2 5.45.70.34 不可达，Loader 会卡在 MD5 校验的 do-while 死循环，应用将永远不展示引导界面，UTG 只能观测到“图标消失 + 静默联网 + 无障碍服务空描述”这一前置形态。另需注意：无障碍描述为占位符，纯文本抓取时信息量极低，须结合服务名与包名比对判定。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.API2.MainActivity.onCreate",
    "com.API2.DummyAccessibility.onServiceConnected",
    "com.API2.DummyAccessibility.onAccessibilityEvent",
    "com.API2.Reflector.loadClass",
    "com.API2.Loader.run",
    "res/values/strings.xml#L5 (description_that_shows_on_the_accessibility_page)"
  ]
}
```

**边界说明**：本次未使用动态分析（未验证在线设备）；`com.raccoon.Accessibility` 的实际引导步骤、文案与拒权重跳机制均以“不可静态还原”标注，未作推断性填充。

</details>
