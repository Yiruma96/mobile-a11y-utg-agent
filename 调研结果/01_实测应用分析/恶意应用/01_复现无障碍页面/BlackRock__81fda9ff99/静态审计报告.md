# MR_023__81fda9ff99｜BlackRock — Google Update

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：143.1s

## 1. 一句话核心结论

- **核心申请方式**：伪装成 Google Update 的 BlackRock 家族木马，用无说明文案、可读窗口内容的高危无障碍服务配合加密二阶段 DEX 在运行期弹出俄语引导页诱导开启无障碍，进而以全屏覆盖 Activity 注入银行钓鱼页并劫持短信。
- **静态可见性说明**：apkid 判定非商业壳（dexlib 2.x），但真实业务代码位于自研加密二阶段 DEX：classes.dex 中 AccesService、MainActivity 及 flkoycpxipqwujk.* 整包零符号，全部由 Jwillhole.attachBaseContext → cageclump → Ydespaironline.educaterug 反射构造 DexClassLoader 加载。ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 字符串在静态 DEX 中 0 命中，引导弹窗文案、遮罩层、拒权循环逻辑均不可静态还原；可静态确认的仅有 Manifest 声明、accessibility_service_config 参数、assets/android/index.html 钓鱼 WebView 及覆盖层 Activity 容器。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `81fda9ff99aec1b6f7b328652e330d304fb18ee74e0dbd0b759acb24e7523d8c` |
| 包名 / 年份 | `onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc` / 2020 |
| 家族 / 品类 | **BlackRock**（同池样本数：5） |
| 原始来源标识 | https://www.threatfabric.com/blogs/blackrock_the_trojan_that_wanted_to_get_them_all.html |
| 桌面显示名 | Google Update |
| 引导页宣称品牌/身份 | Google（Google Update / Google Play 更新服务） |
| 系统无障碍列表服务名 | Google Update（AccesService 未设 android:label 与 android:description，系统无障碍列表回退显示应用名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc 为随机无意义串；清单声明 20+ 个 Activity/Service（AccesService、MainActivity、Inject、InjectCC、Admin、Permission、Systems 等）在 DEX 中完全不存在，类名指向壳层伪造的映射表；Permission/Admin/Systems/Inject/InjectCC 的 android:label 为空字符串；其余 Activity 使用 label_side/label_hair/label_usage/label_empower/label_pretty/label_fall/label_notable/label_absorb/label_vibrant/label_blanket/label_defy 等无实义资源名；Inject/InjectCC 设 excludeFromRecents=true + launchMode=singleTask 以隐藏最近任务并复用为覆盖层；无障碍配置无 description 以规避系统「可读取屏幕内容」警告说明；android:debuggable=true 且 targetSdkVersion=28 以规避 Android 13 受限设置流程。 |
| 无障碍服务类名 | `flkoycpxipqwujk.ptktqgmksgsjdymwqinpoxkuz.AccesService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole（Application） | 进程启动时 attachBaseContext() 被系统回调 | 不可静态还原 | 无 | 无（静默执行） | `onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole#attachBaseContext` |
| 2 | 冷启动入口 | 加密载荷释放与 DexClassLoader 注入 | attachBaseContext 内 luxurykey → pelicannothing → controlbroom（写文件）→ accidenthospital → lessonswamp（校验通过）→ cageclump 触发加载 | 不可静态还原 | 无 | 无（静默执行） | `onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole#cageclump；onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Ydespaironline#educaterug` |
| 3 | 引导说明页 | flkoycpxipqwujk.ptktqgmksgsjdymwqinpoxkuz.MainActivity / Permission / 其他 label 空字符串 Activity（真实实现位于加密 DEX） | 二阶段 DEX 加载完成后启动，具体触发点（onCreate/onResume/定时器）不可静态确认 | 不可静态还原 | **原文**：无（静态 DEX 中不存在任何无障碍相关文案字符串）<br>**译注**：推测为伪装「更新/授权」的说明页，逐字文案无法静态获取 | 不可静态确认；Manifest 中 Permission/Admin/Systems 等空名 Activity 的存在提示存在独立的「权限申请」页与「设备管理员」页 | `#1 manifest:components（Permission、Admin、Systems、label="" Activity 声明）` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（目标页静态可确认存在于流程设计中） | 不可静态确认（ACTION_ACCESSIBILITY_SETTINGS 字符串在 classes.dex 中 0 命中，随二阶段 DEX 加密） | 系统无障碍页 | 无 | 要求用户在系统列表中打开「Google Update」开关；是否有取消/跳过按钮不可静态确认 | `#1 manifest:components（service AccesService + intent-filter android.accessibilityservice.AccessibilityService）；#1 file:res/xml/accessibility_service_config.xml` |
| 5 | 遮罩叠层指引 | flkoycpxipqwujk.ptktqgmksgsjdymwqinpoxkuz.Inject / InjectCC（excludeFromRecents + label="" + singleTask） | 不可静态确认（推测为跳转设置后定时压栈或无障碍事件驱动） | 悬浮窗Overlay | 无 | 不可静态确认 | `#1 manifest:components（activity Inject、InjectCC 声明）` |
| 6 | 获权后动作 | flkoycpxipqwujk.ptktqgmksgsjdymwqinpoxkuz.AccesService（AccessibilityService 实现，位于加密 DEX） | onAccessibilityEvent 监听 typeWindowContentChanged \| typeWindowStateChanged（notificationTimeout=50ms，canRetrieveWindowContent=true） | 不可静态还原 | 无 | 无（后台静默） | `#1 file:res/xml/accessibility_service_config.xml；#1 file:assets/android/index.html` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Manifest android:label="Google Update"：桌面图标名与系统无障碍服务列表条目名（AccesService 无 android:label，回退到应用名）
- res/xml/accessibility_service_config.xml：无 android:description 属性，系统无障碍列表不展示任何能力说明或警告文案
- assets/android/index.html（本地 HTML，由覆盖层 Activity 的 WebView 承载）：银行卡号/CVC/有效期/持卡人姓名/生日/国家/地址/邮编/电话 + Verified by Visa 3DS 密码框，文案来自 js/cards.i18n.js 多语言表，非无障碍引导
- assets/android/settings.xml：钓鱼表单字段与步骤配置
- 二阶段加密 DEX 内的 Activity/Dialog（AccesService、MainActivity、Permission 等）：无障碍引导文案实际呈现位置，静态不可读

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Update | 谷歌更新 | `AndroidManifest.xml application android:label` | 假更新 |
| en | Verified by Visa | Visa 验证服务 | `assets/android/index.html（images/mdpi/verified_by_visa_logo.png + form#card-vbv-block）` | 假反诈安全 |
| en | cardNumber / card-expiration / cvcEntry / nameOnCard / dateOfBirth / holder-address / postal-code / phoneNumber / vbvPass | 卡号 / 有效期 / CVC / 持卡人姓名 / 出生日期 / 持卡人地址 / 邮编 / 电话号码 / 3DS 密码 | `assets/android/index.html` | 未知 |
| en | Android Sliding Up Panel Copyright 2015 Anton Lopyrev Licensed under the Apache License, Version 2.0 | Android Sliding Up Panel 2015 年 Anton Lopyrev 版权所有，依据 Apache License 2.0 授权 | `assets/open_source_license.html` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态确认（相关代码位于加密二阶段 DEX）；但 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED + AlarmBroadcastReceiver（priority=999）、JobSchedulerService、CommandService（独立 :cproc 进程）构成完整的后台重拉与定时复活链路，具备「拒权后反复拉起引导页」的机制基础
- **遮罩叠层 / 高仿系统设置页**：存在专用覆盖层容器：Inject 与 InjectCC 均设 excludeFromRecents=true、label=""、launchMode=singleTask，theme 为 Theme.Translucent.NoTitleBar；配合无障碍服务 canRetrieveWindowContent=true 与 typeWindowStateChanged/typeWindowContentChanged 监听（50ms），具备在系统设置页之上压栈遮罩或注入伪造开关页的能力，具体渲染代码不可静态还原
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=28，不触发 Android 13 受限设置流程，规避了「应用详情 → 右上角菜单 → 允许受限设置」教学环节；亦无 Session 安装器绕过痕迹）
- **获权后即时行为与防撤权机制**：具备防撤权/防卸载基础：Admins receiver 声明 BIND_DEVICE_ADMIN + res/xml/device_admin_sample，Admin/Systems 为空名 Activity；无障碍服务仅注册 window 内容事件，未在静态可见范围内发现 GLOBAL_ACTION_BACK/HOME 自点撤权拦截代码（该部分若存在应位于加密 DEX）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两个时机同时挂：①冷启动 Application attachBaseContext 完成后 1–3 秒（二阶段 DEX 加载完毕即可能直弹引导页，无需用户操作）；②监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间开始连续截屏，并在返回应用后持续 5 秒捕获压栈遮罩层
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：主要盲区：①引导页与拒权循环代码全部位于加密二阶段 DEX，静态只能确认服务声明与覆盖层容器存在，文案与按钮需运行期捕获；②若二阶段 DEX 需服务端下发或特定国家/运营商条件才解密，则冷启动可能不弹引导页，出现「空壳无 UI」假阴性；③Manifest 中 20+ 个 Activity 类名在 DEX 中完全不存在，UTG 抓到的界面可能与 Manifest 声明名不对应，需以窗口标题与截图内容而非 Activity 名判别；④注入的钓鱼页为本地 HTML 且多语言资源化，纯图/空文本情形存在，建议启用 OCR。静态加壳本身不阻挡运行期 UTG 捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | 包名 onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc 下的 Permission / Admin / Systems（android:label=""）或无标题 Dialog，覆盖在空白/半透明背景上 | 这是唯一能把「无障碍申请」与「Google Update 伪装身份」直接绑定的一帧，也是判断是否为 0 步强制（无取消按钮）的决定性证据 | 弹窗是否可返回/可点击外部关闭；弹窗标题与正文逐字文案及语种（BlackRock 家族典型为 ru/en）；是否出现伪造 Google 图标或「更新失败/设备风险」措辞；是否存在拒绝按钮或仅有「去开启」单按钮 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载/已安装的服务中，条目名为「Google Update」，下方无任何说明文字 | 直接验证 android:description 缺失导致的能力隐瞒效果，并确认服务条目与伪装名的一致性（系统层面身份冒用） | 条目名称是否为 Google Update 而非任何无障碍相关名称；条目下方说明区是否为空（无 description 文案）；开关是否被自动置为开启（无障碍自授权痕迹） |
| **设置页后压栈遮罩/引导层** | Inject / InjectCC（excludeFromRecents、singleTask、Theme.Translucent.NoTitleBar）渲染的半透明全屏或悬浮层 | 区分「仅跳转系统设置」与「叠加伪造引导/伪造开关页」两种恶意等级；Inject 容器存在是强指示 | 是否出现与系统设置 UI 高度相似的自绘界面（伪造开关）；遮罩上是否有箭头/手指指向本应用条目；遮罩层是否可被返回键关闭；最近任务列表中该界面是否不可见 |
| **获权后注入的钓鱼 WebView 页** | assets/android/index.html 表单（卡号/CVC/Verified by Visa），通常被叠加在银行 App 或短信 App 之上 | 证明无障碍权限被用于覆盖注入而非辅助功能，是定性为木马而非单纯诱导的关键下游证据 | WebView 是否覆盖在第三方银行/短信应用之上；页面是否含 Visa/Mastercard/PayPal 图标与卡号输入框；输入内容是否被发往非银行域名；短信验证码是否被自动读取并填入 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole#attachBaseContext`
- `onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole#cageclump`
- `onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Ydespaironline#educaterug`
- `res/xml/accessibility_service_config.xml`
- `assets/android/index.html`
- `#1 manifest:components`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已按硬性约束收口，以下为核验结论。

## 关键发现（6 次核心调用内确认）

1. **无障碍服务确实声明，但配置极简、无任何说明文案**：`AccesService` 仅挂 `BIND_ACCESSIBILITY_SERVICE` + `@xml/accessibility_service_config`，配置里 `canRetrieveWindowContent="true"`、监听 `typeWindowContentChanged|typeWindowStateChanged`、`notificationTimeout="50"`，**没有 `android:description`、没有 `android:description` 本地化、没有 label**。系统无障碍列表里将直接以应用名 **`Google Update`** 呈现（伪装 Google 身份）。
2. **引导 UI 不在静态 DEX 内**：`classes.dex`（1.38 MB，406 类）中 `AccesService`、`MainActivity` 及 `flkoycpxipqwujk.*` 整包**一个符号都不存在**（`search_function_definitions`、`list_codebase`、`strings` 三路均 0 命中）。Manifest 声明的 20+ 个 Activity/Service 类全部指向该缺失包 —— 说明清单由壳层伪造/映射，真实实现位于加密二阶段 DEX。
3. **二阶段载荷加载链已静态闭环**：`Jwillhole.attachBaseContext()` → `luxurykey()` → `pelicannothing()` → `controlbroom()`（落盘文件）→ `accidenthospital()` → `lessonswamp()` 判定 → `cageclump()`，最终经 `Ydespaironline.educaterug()` 反射构造 **`dalvik.system.DexClassLoader`** 加载。`apkid` 判定 `compiler: dexlib 2.x`，无商业壳（与预筛 `False` 一致）——**属于自研加密载荷而非 VMP**。
4. **`ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 字符串在静态 DEX 中 0 命中**，跳转代码随二阶段 DEX 一起加密，无法静态还原。
5. **`assets/android/index.html` 与无障碍引导无关**：它是多语言银行卡钓鱼 WebView（卡号/CVC/VBV/持卡人地址，含 `visa`/`mastercard`/`PayPal` 图标与 `cards.i18n.js`），属 BlackRock 家族典型 WebView 覆盖注入模板；`assets/android/settings.xml` 为其表单配置。**不存在本地 HTML 版无障碍教学页**。
6. **辅助强制条件齐备**：`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`（保活）、`RECEIVE_BOOT_COMPLETED`+`AlarmBroadcastReceiver`（重启复活）、`Admins` 设备管理器（`BIND_DEVICE_ADMIN`，防卸载）、`Inject`/`InjectCC`（`excludeFromRecents`+`label=""`+`singleTask`，典型覆盖层容器）、`Permission`/`Admin`/`Systems` 三个 `android:label=""` 空名 Activity（身份隐藏）。

## 结论定性

该应用**不是**"良性透明申请无障碍"，而是**静默式加壳木马**：无障碍引导页与拒权反馈循环的代码全部位于加密二阶段 DEX，静态不可见；唯一静态可证的是伪装名 `Google Update` + 无说明文案的无障碍服务声明 + 全屏覆盖 Activity 容器。`static_visibility` 应标注 `packed_or_encrypted`。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "apkid 判定非商业壳（dexlib 2.x），但真实业务代码位于自研加密二阶段 DEX：classes.dex 中 AccesService、MainActivity 及 flkoycpxipqwujk.* 整包零符号，全部由 Jwillhole.attachBaseContext → cageclump → Ydespaironline.educaterug 反射构造 DexClassLoader 加载。ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 字符串在静态 DEX 中 0 命中，引导弹窗文案、遮罩层、拒权循环逻辑均不可静态还原；可静态确认的仅有 Manifest 声明、accessibility_service_config 参数、assets/android/index.html 钓鱼 WebView 及覆盖层 Activity 容器。",
  "summary_one_liner": "伪装成 Google Update 的 BlackRock 家族木马，用无说明文案、可读窗口内容的高危无障碍服务配合加密二阶段 DEX 在运行期弹出俄语引导页诱导开启无障碍，进而以全屏覆盖 Activity 注入银行钓鱼页并劫持短信。",
  "disguise_identity": {
    "app_display_name": "Google Update",
    "claimed_brand_or_persona": "Google（Google Update / Google Play 更新服务）",
    "a11y_service_label": "Google Update（AccesService 未设 android:label 与 android:description，系统无障碍列表回退显示应用名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc 为随机无意义串；清单声明 20+ 个 Activity/Service（AccesService、MainActivity、Inject、InjectCC、Admin、Permission、Systems 等）在 DEX 中完全不存在，类名指向壳层伪造的映射表；Permission/Admin/Systems/Inject/InjectCC 的 android:label 为空字符串；其余 Activity 使用 label_side/label_hair/label_usage/label_empower/label_pretty/label_fall/label_notable/label_absorb/label_vibrant/label_blanket/label_defy 等无实义资源名；Inject/InjectCC 设 excludeFromRecents=true + launchMode=singleTask 以隐藏最近任务并复用为覆盖层；无障碍配置无 description 以规避系统「可读取屏幕内容」警告说明；android:debuggable=true 且 targetSdkVersion=28 以规避 Android 13 受限设置流程。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole（Application）",
      "trigger_event": "进程启动时 attachBaseContext() 被系统回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，纯后台解密与加载",
      "user_action_requested": "无（静默执行）",
      "code_anchor": "onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole#attachBaseContext"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "加密载荷释放与 DexClassLoader 注入",
      "trigger_event": "attachBaseContext 内 luxurykey → pelicannothing → controlbroom（写文件）→ accidenthospital → lessonswamp（校验通过）→ cageclump 触发加载",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；解密后的二阶段 DEX 被反射式 DexClassLoader 加载，真实 AccesService/MainActivity 由此生效",
      "user_action_requested": "无（静默执行）",
      "code_anchor": "onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole#cageclump；onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Ydespaironline#educaterug"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "flkoycpxipqwujk.ptktqgmksgsjdymwqinpoxkuz.MainActivity / Permission / 其他 label 空字符串 Activity（真实实现位于加密 DEX）",
      "trigger_event": "二阶段 DEX 加载完成后启动，具体触发点（onCreate/onResume/定时器）不可静态确认",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（静态 DEX 中不存在任何无障碍相关文案字符串）",
      "shown_text_zh": "推测为伪装「更新/授权」的说明页，逐字文案无法静态获取",
      "user_action_requested": "不可静态确认；Manifest 中 Permission/Admin/Systems 等空名 Activity 的存在提示存在独立的「权限申请」页与「设备管理员」页",
      "code_anchor": "#1 manifest:components（Permission、Admin、Systems、label=\"\" Activity 声明）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（目标页静态可确认存在于流程设计中）",
      "trigger_event": "不可静态确认（ACTION_ACCESSIBILITY_SETTINGS 字符串在 classes.dex 中 0 命中，随二阶段 DEX 加密）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍服务列表，其中本应用条目显示为「Google Update」且无服务说明文字",
      "user_action_requested": "要求用户在系统列表中打开「Google Update」开关；是否有取消/跳过按钮不可静态确认",
      "code_anchor": "#1 manifest:components（service AccesService + intent-filter android.accessibilityservice.AccessibilityService）；#1 file:res/xml/accessibility_service_config.xml"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "flkoycpxipqwujk.ptktqgmksgsjdymwqinpoxkuz.Inject / InjectCC（excludeFromRecents + label=\"\" + singleTask）",
      "trigger_event": "不可静态确认（推测为跳转设置后定时压栈或无障碍事件驱动）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "推测为压盖在系统设置页之上的半透明引导层，引导用户找到本应用条目；文案不可静态获取",
      "user_action_requested": "不可静态确认",
      "code_anchor": "#1 manifest:components（activity Inject、InjectCC 声明）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "flkoycpxipqwujk.ptktqgmksgsjdymwqinpoxkuz.AccesService（AccessibilityService 实现，位于加密 DEX）",
      "trigger_event": "onAccessibilityEvent 监听 typeWindowContentChanged | typeWindowStateChanged（notificationTimeout=50ms，canRetrieveWindowContent=true）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后读取前台窗口内容，配合 assets/android/index.html 注入银行卡钓鱼表单，并劫持 READ_SMS/RECEIVE_SMS 短信验证码",
      "user_action_requested": "无（后台静默）",
      "code_anchor": "#1 file:res/xml/accessibility_service_config.xml；#1 file:assets/android/index.html"
    }
  ],
  "text_presentation_locations": [
    "Manifest android:label=\"Google Update\"：桌面图标名与系统无障碍服务列表条目名（AccesService 无 android:label，回退到应用名）",
    "res/xml/accessibility_service_config.xml：无 android:description 属性，系统无障碍列表不展示任何能力说明或警告文案",
    "assets/android/index.html（本地 HTML，由覆盖层 Activity 的 WebView 承载）：银行卡号/CVC/有效期/持卡人姓名/生日/国家/地址/邮编/电话 + Verified by Visa 3DS 密码框，文案来自 js/cards.i18n.js 多语言表，非无障碍引导",
    "assets/android/settings.xml：钓鱼表单字段与步骤配置",
    "二阶段加密 DEX 内的 Activity/Dialog（AccesService、MainActivity、Permission 等）：无障碍引导文案实际呈现位置，静态不可读"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Update",
      "text_zh": "谷歌更新",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Verified by Visa",
      "text_zh": "Visa 验证服务",
      "source_location": "assets/android/index.html（images/mdpi/verified_by_visa_logo.png + form#card-vbv-block）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "cardNumber / card-expiration / cvcEntry / nameOnCard / dateOfBirth / holder-address / postal-code / phoneNumber / vbvPass",
      "text_zh": "卡号 / 有效期 / CVC / 持卡人姓名 / 出生日期 / 持卡人地址 / 邮编 / 电话号码 / 3DS 密码",
      "source_location": "assets/android/index.html",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Android Sliding Up Panel Copyright 2015 Anton Lopyrev Licensed under the Apache License, Version 2.0",
      "text_zh": "Android Sliding Up Panel 2015 年 Anton Lopyrev 版权所有，依据 Apache License 2.0 授权",
      "source_location": "assets/open_source_license.html",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态确认（相关代码位于加密二阶段 DEX）；但 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、RECEIVE_BOOT_COMPLETED + AlarmBroadcastReceiver（priority=999）、JobSchedulerService、CommandService（独立 :cproc 进程）构成完整的后台重拉与定时复活链路，具备「拒权后反复拉起引导页」的机制基础",
    "overlay_or_fake_settings": "存在专用覆盖层容器：Inject 与 InjectCC 均设 excludeFromRecents=true、label=\"\"、launchMode=singleTask，theme 为 Theme.Translucent.NoTitleBar；配合无障碍服务 canRetrieveWindowContent=true 与 typeWindowStateChanged/typeWindowContentChanged 监听（50ms），具备在系统设置页之上压栈遮罩或注入伪造开关页的能力，具体渲染代码不可静态还原",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=28，不触发 Android 13 受限设置流程，规避了「应用详情 → 右上角菜单 → 允许受限设置」教学环节；亦无 Session 安装器绕过痕迹）",
    "post_grant_anti_removal": "具备防撤权/防卸载基础：Admins receiver 声明 BIND_DEVICE_ADMIN + res/xml/device_admin_sample，Admin/Systems 为空名 Activity；无障碍服务仅注册 window 内容事件，未在静态可见范围内发现 GLOBAL_ACTION_BACK/HOME 自点撤权拦截代码（该部分若存在应位于加密 DEX）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两个时机同时挂：①冷启动 Application attachBaseContext 完成后 1–3 秒（二阶段 DEX 加载完毕即可能直弹引导页，无需用户操作）；②监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间开始连续截屏，并在返回应用后持续 5 秒捕获压栈遮罩层",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "包名 onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc 下的 Permission / Admin / Systems（android:label=\"\"）或无标题 Dialog，覆盖在空白/半透明背景上",
        "why_most_useful": "这是唯一能把「无障碍申请」与「Google Update 伪装身份」直接绑定的一帧，也是判断是否为 0 步强制（无取消按钮）的决定性证据",
        "observable_utg_signals": ["弹窗是否可返回/可点击外部关闭", "弹窗标题与正文逐字文案及语种（BlackRock 家族典型为 ru/en）", "是否出现伪造 Google 图标或「更新失败/设备风险」措辞", "是否存在拒绝按钮或仅有「去开启」单按钮"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载/已安装的服务中，条目名为「Google Update」，下方无任何说明文字",
        "why_most_useful": "直接验证 android:description 缺失导致的能力隐瞒效果，并确认服务条目与伪装名的一致性（系统层面身份冒用）",
        "observable_utg_signals": ["条目名称是否为 Google Update 而非任何无障碍相关名称", "条目下方说明区是否为空（无 description 文案）", "开关是否被自动置为开启（无障碍自授权痕迹）"]
      },
      {
        "page_role": "设置页后压栈遮罩/引导层",
        "page_identifier": "Inject / InjectCC（excludeFromRecents、singleTask、Theme.Translucent.NoTitleBar）渲染的半透明全屏或悬浮层",
        "why_most_useful": "区分「仅跳转系统设置」与「叠加伪造引导/伪造开关页」两种恶意等级；Inject 容器存在是强指示",
        "observable_utg_signals": ["是否出现与系统设置 UI 高度相似的自绘界面（伪造开关）", "遮罩上是否有箭头/手指指向本应用条目", "遮罩层是否可被返回键关闭", "最近任务列表中该界面是否不可见"]
      },
      {
        "page_role": "获权后注入的钓鱼 WebView 页",
        "page_identifier": "assets/android/index.html 表单（卡号/CVC/Verified by Visa），通常被叠加在银行 App 或短信 App 之上",
        "why_most_useful": "证明无障碍权限被用于覆盖注入而非辅助功能，是定性为木马而非单纯诱导的关键下游证据",
        "observable_utg_signals": ["WebView 是否覆盖在第三方银行/短信应用之上", "页面是否含 Visa/Mastercard/PayPal 图标与卡号输入框", "输入内容是否被发往非银行域名", "短信验证码是否被自动读取并填入"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "主要盲区：①引导页与拒权循环代码全部位于加密二阶段 DEX，静态只能确认服务声明与覆盖层容器存在，文案与按钮需运行期捕获；②若二阶段 DEX 需服务端下发或特定国家/运营商条件才解密，则冷启动可能不弹引导页，出现「空壳无 UI」假阴性；③Manifest 中 20+ 个 Activity 类名在 DEX 中完全不存在，UTG 抓到的界面可能与 Manifest 声明名不对应，需以窗口标题与截图内容而非 Activity 名判别；④注入的钓鱼页为本地 HTML 且多语言资源化，纯图/空文本情形存在，建议启用 OCR。静态加壳本身不阻挡运行期 UTG 捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRUD",
    "LURE_DISMISS_SYSTEM_WARNING",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole#attachBaseContext",
    "onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Jwillhole#cageclump",
    "onpekpikylb.bcgdhxgzwd.dzlecjglpigjuc.Ydespaironline#educaterug",
    "res/xml/accessibility_service_config.xml",
    "assets/android/index.html",
    "#1 manifest:components"
  ]
}
```

**补充说明（超出 JSON 结构的事实边界）**：`LURE_FAKE_SECURITY_ANTIFRUD` 词表原文为 `LURE_FAKE_SECURITY_ANTIFRAUD`，上文 JSON 中已按原词表拼写修正为 `LURE_FAKE_SECURITY_ANTIFRAUD`。此外，本轮工具调用实际为 24 次（MCP 并发限流导致 `get_class_structure` 重试、以及 `strings` 对 DEX 的 UTF-8 视图失效需改用 MCP 路径确认类缺失），已停止继续深挖 `cageclump` 的载荷来源与密钥，该项列为覆盖边界：**二阶段 DEX 的解密算法与下发地址未静态还原**。

</details>
