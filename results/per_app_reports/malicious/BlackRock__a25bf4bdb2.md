# MB_033__a25bf4bdb2｜BlackRock — Flash Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：235.6s

## 1. 一句话核心结论

- **核心申请方式**：以「Flash Player」为外壳声明可读取窗口内容的无障碍服务，业务逻辑经 DexGuard 运行期解密，配套内置 Сбербанк 银行协议页与银行卡/CVC 录入 HTML 及透明 Inject 活动、独立进程 CommandService、短信自启接收器。
- **静态可见性说明**：Manifest、无障碍服务配置（res/xml/accessibility_service_config.xml）与 assets 钓鱼 HTML 完整静态可见；但全部 security.sword.* 类体（含 AccesService、Inject、CommandService、各混淆 Activity）被 DexGuard 加密，仅由 Application.attachBaseContext 中的 eaglehint/figureride/onematter/voidnominee 在运行期解密装载，DEX 中不含 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS / AccessibilityService 任何静态引用，故引导弹窗、跳设置点、遮罩与拒权循环不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a25bf4bdb2ed9872456af0057eb21ce31fd03d680d63a9da469519060b4814bc` |
| 包名 / 年份 | `artwork.differ.kitchen` / 2024 |
| 家族 / 品类 | **BlackRock**（同池样本数：1） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Flash Player |
| 引导页宣称品牌/身份 | ПАО Сбербанк（俄罗斯联邦储蓄银行）试点项目/Сбербанк Онлайн 客户端 |
| 系统无障碍列表服务名 | 无（Manifest 中该 service 未设置 android:label，accessibility_service_config 亦无 android:description，系统无障碍列表将显示为默认空标签/包名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：所有 Activity 的 android:label 均为随机小写字母串（如 ayiztuoyfjnqyipjpnn、kybqisbosbulzxuowqghyfqmgkzha），Permission/Admin/Systems/Inject/InjectCC 标签为空字符串；Inject 与 InjectCC 使用 android:icon=@drawable/background、excludeFromRecents、launchMode=singleTask 隐藏任务栈；无障碍项无 description 说明；类名与成员名混淆为随机词（acquirefringe/loungedeputy/eaglehint 等）并插入大量无意义算术以干扰反编译；无伪造 isAccessibilityTool 证据（targetSdk 28，低于该属性引入版本）。 |
| 无障碍服务类名 | `security.sword.AccesService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | security.sword.MainActivity（LAUNCHER + android.app.role.SMS 类别）；进程级 artwork.differ.kitchen.ALdKxTnSqDnMtXhHwBmBkNmRyLsKnChBbGdRxZbWzNpZhEhKf（Application） | 用户点击桌面「Flash Player」图标启动；Application.attachBaseContext() 先执行 DexGuard 解密并装载业务类 | 不可静态还原 | **原文**：无（MainActivity 类体被加密，未取得界面文案）<br>**译注**：不可静态还原；Manifest 层面仅确认透明无标题主题 Theme.Translucent.NoTitleBar | 不可静态还原 | `artwork.differ.kitchen.ALdKxTnSqDnMtXhHwBmBkNmRyLsKnChBbGdRxZbWzNpZhEhKf.attachBaseContext / security.sword.MainActivity` |
| 2 | 引导说明页 | 不可静态还原（预期为 security.sword 包下某个随机名 Activity，如 KQoUsNwPeLuQcNoLqJkNrLzKhBlZhXhDmOcGtCiUnJfRhSsAr、Permission 等） | 不可静态还原 | 不可静态还原 | **原文**：无（无静态可定位的引导文案；res/strings 中未检索到无障碍相关说明文本）<br>**译注**：不可静态还原 | 不可静态还原（无法确认是否存在取消/跳过按钮） | `security.sword.Permission（android:label=""）/ res/xml/accessibility_service_config.xml` |
| 3 | 跳无障碍设置 | 预期为系统「设置 → 无障碍 → 已下载的服务」页面 | 不可静态还原（DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 静态引用，跳转常量由运行期解密代码持有） | 系统无障碍页 | 无 | 不可静态还原；系统页面上用户需手动找到并开启该服务，无 android:description 说明其真实用途 | `#1 manifest:components（service security.sword.AccesService）/ res/xml/accessibility_service_config.xml` |
| 4 | 获权后动作 | security.sword.AccesService（无障碍服务）→ security.sword.Inject / InjectCC（透明 overlay 活动）、security.sword.CommandService（:cproc 独立进程）、assets/android/index.html 银行卡表单、assets/offer.html Сбербанк 协议页 | 无障碍服务被系统启用后 onServiceConnected（实现体加密，不可静态确认）；BOOT_COMPLETED 由 SmsBroadcast / AlarmBroadcastReceiver 重新拉起 | 本地HTML WebView + 悬浮窗Overlay（据 Manifest 组件与 assets 推断，实现体不可静态还原） | **原文**：Соглашение об участии в пилотном проекте Банка … между ПАО Сбербанк … и клиентом ПАО Сбербанк, использующим автоматизированную систему Сбербанк Онлайн<br>**译注**：「关于参与银行试点项目的协议……由 ПАО Сбербанк（俄罗斯联邦储蓄银行）与使用 Сбербанк Онлайн 自动化系统的客户签订」——冒充银行试点协议，配合卡号/CVC/有效期录入表单 | 在仿冒银行页面填写卡号、有效期、CVC、姓名、地址、出生日期（表单字段见 index.html） | `assets/offer.html / assets/android/index.html / security.sword.Inject（excludeFromRecents, @drawable/background）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：security.sword.AccesService 无 android:label、无 android:description（accessibility_service_config.xml 中仅配置事件类型与 canRetrieveWindowContent），用户看不到任何用途说明
- res/strings 与 res/xml 中未检索到任何无障碍引导/教学文案，说明引导文字不在静态资源内，由 DexGuard 解密后的代码或远端下发提供
- assets/offer.html：俄语 Сбербанк 试点项目协议长文（纯本地 HTML，用于伪装银行合规授权）
- assets/android/index.html：本地 HTML 银行卡录入表单（卡号、有效期、CVC、持卡人、地址、生日），含多国卡组织图标与 getCountryCode/getLanguageCode 地域适配脚本
- assets/report/bank_report_for_card_template*.html、bank_statement*.html：银行对账单/流水模板，用于伪造交易与余额界面
- 所有引导弹窗/遮罩/WebView 教学页的具体呈现位置不可静态还原（security.sword.* 类体加密）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Соглашение об участии в пилотном проекте Банка. Данное соглашение заключено между ПАО Сбербанк (далее - Банк) и клиентом ПАО Сбербанк, использующим автоматизированную систему Сбербанк Онлайн - защищенную систему дистанционного обслуживания клиента (далее - Клиент [1]) через мобильное приложение Сбербанк Онлайн | 关于参与银行试点项目的协议。本协议由 ПАО Сбербанк（下称「银行」）与通过 Сбербанк Онлайн 移动应用使用 Сбербанк Онлайн 自动化系统（客户远程服务安全系统）的 ПАО Сбербанк 客户（下称「客户」）签订。 | `assets/offer.html` | 假更新 |
| en | CVC | 「CVC」——卡片安全码输入占位提示（表单同时采集 cardNumber、card-expiration、nameOnCard、firstname、lastname、date-birth） | `assets/android/index.html（input placeholder="CVC" / name="cardNumber" / class="card-expiration"）` | 未知 |
| en | Flash Player | 「Flash Player」——桌面图标显示名，宣称提供多媒体播放能力 | `AndroidManifest.xml application@android:label` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原（AccesService 与引导 Activity 类体被 DexGuard 加密；DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 静态引用，onResume 重跳或定时器拉起逻辑无法确认）
- **遮罩叠层 / 高仿系统设置页**：未取得高仿设置页证据；但 Manifest 存在 security.sword.Inject 与 InjectCC 两个 excludeFromRecents、singleTask、透明背景图标的 Activity，具备在系统设置页之上叠加无痕遮罩的结构条件，实际叠层行为不可静态确认
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=28、minSdkVersion=16，低于 Android 13 受限设置机制适用版本；未发现对应引导文案或 Session 安装器路径）
- **获权后即时行为与防撤权机制**：不可静态还原（未发现 GLOBAL_ACTION_BACK/HOME 静态调用；同包存在设备管理员 Admins 与独立进程 CommandService，具备阻碍撤权的能力条件但无静态证据）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动后首帧即拉起录屏/UTG 抓取，并以「页面标题或包名切换至 com.android.settings 无障碍页」为关键瞬间：一旦检测到前台窗口变为系统设置无障碍列表（或应用详情页），立即连续截图并提取节点树，捕捉跳转前页面与返回后的反应。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区为 DexGuard 加密导致 security.sword.* 类体不可静态还原：引导文案、跳转时序、遮罩与拒权循环全部只能靠运行期 UTG 获取；另需注意资产中的钓鱼页面为本地 HTML（非远端），若攻击者仅按远端下发条件才展示引导，则离线环境可能只看到无害首屏。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏/引导页** | 包名 artwork.differ.kitchen、透明无标题主题、桌面名为 Flash Player 的 Activity；可能伴随加载/更新提示 | 判定引导是冷启动零步强制还是功能触发，并取得 DexGuard 解密后才出现的引导文案原文 | 首屏是否立即出现无障碍/授权相关弹窗或按钮；是否存在取消、跳过、返回按钮；是否出现「更新/故障/安全」类恐吓措辞；界面是否出现银行品牌 Logo 与播放器身份不符 |
| **跳转前教学页（原生或 WebView）** | 包含「设置 → 无障碍」「Настройки → Специальные возможности」等分步指引文字的 Activity/WebView | 该页承载「教用户开启无障碍」的完整话术与步骤编号，是诱导行为的直接证据 | 分步序号与箭头图示；是否点名要求找到空标签服务项；是否出现受限设置/应用详情右上角菜单的引导 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中新增的一项无描述服务（对应 security.sword.AccesService） | 验证系统列表中该服务确实无用途说明，是身份隐瞒与诱导成立的关键观测点 | 列表项名称是否为空或显示包名；是否存在说明副标题；用户是否需滚动到「已下载的服务」才能找到 |
| **设置页返回后反应（拒权反馈/叠层）** | 从系统设置返回后自动弹出的弹窗、遮罩或再次被拉起的引导页 | 判定拒权循环与遮罩叠层是否存在，这是强制性与非自愿授权的核心判别 | 返回后是否在 1~2 秒内自动重跳设置页；是否出现全屏半透明遮罩或悬浮引导窗；是否只有「去开启」单一按钮而无关闭途径 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `artwork.differ.kitchen.ALdKxTnSqDnMtXhHwBmBkNmRyLsKnChBbGdRxZbWzNpZhEhKf.attachBaseContext`
- `security.sword.AccesService（Manifest 声明，类体 DexGuard 加密）`
- `res/xml/accessibility_service_config.xml`
- `assets/offer.html`
- `assets/android/index.html`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验）

**静态可见性：`packed_or_encrypted`（DexGuard 运行时解密）**

- **无障碍声明齐全，但服务实现不可见**：Manifest 声明了 `security.sword.AccesService`（`BIND_ACCESSIBILITY_SERVICE`，exported=false），[无障碍配置](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 启用 `typeWindowContentChanged|typeWindowStateChanged`、`canRetrieveWindowContent="true"`、`notificationTimeout="50"`，即实时读取任意前台窗口内容；但 `classes.dex` 中 **不存在** `security/sword`、`AccesService` 等字符串，`AccesService` 类体被 DexGuard 加密，仅运行期还原。
- **没有任何静态可定位的跳转点**：`search_function_callsites` 在 DEX 中对 `ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`AccessibilityService` 全部 `no_matches`；唯一 `AccessibilityService` 相关代码来自集成的 PDFTron/QuickMobile SDK（`View$AccessibilityDelegate`），与应用自身无关。引导弹窗、遮罩、WebView 教学页、拒权循环均无法静态读取。
- **入口即解密加载**：[ALdKxTnSqDnMtXhHwBmBkNmRyLsKnChBbGdRxZbWzNpZhEhKf.attachBaseContext()](<resource-unit:#1.dex1 code:artwork.differ.kitchen.ALdKxTnSqDnMtXhHwBmBkNmRyLsKnChBbGdRxZbWzNpZhEhKf#attachBaseContext>) 经 `eaglehint→figureride→onematter` 解密后调用 `voidnominee(...)` 装载业务逻辑；`assets/*/libc763d2.so` 仅导出 DexGuard 的 `DebugBlocker/EmulatorDetector/HookDetector/RootDetector`，属加固运行时，非业务载荷。
- **身份与内容严重错位**：桌面名 `Flash Player`，无障碍项 `android:description` 为空（系统列表无任何用途说明），而 `assets/` 内含俄语「ПАО Сбербанк 试点项目参与协议」[offer.html](<resource-unit:#1 file:assets/offer.html>) 与带 Visa/MasterCard/JCB 图标的卡号/有效期/CVC 录入页 [assets/android/index.html](<resource-unit:#1 file:assets/android/index.html>)（含 `getCountryCode()/getLanguageCode()` 目标地域适配）。
- **配套恶意组件**：`Inject`/`InjectCC`（`excludeFromRecents`、透明图标、singleTask）、独立进程 `CommandService`（exported=true）、设备管理员 `Admins`、短信收发与 `BOOT_COMPLETED` 自启；应用主题为 `Theme.Translucent.NoTitleBar`，`debuggable=true`。
- **未决**：诱导页面的实际文案、跳转时序、是否有遮罩叠层与拒权重跳循环，全部依赖运行期解密，本次未做动态验证。

已登记风险：**R-001**（high / malware_trojan）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍服务配置（res/xml/accessibility_service_config.xml）与 assets 钓鱼 HTML 完整静态可见；但全部 security.sword.* 类体（含 AccesService、Inject、CommandService、各混淆 Activity）被 DexGuard 加密，仅由 Application.attachBaseContext 中的 eaglehint/figureride/onematter/voidnominee 在运行期解密装载，DEX 中不含 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS / AccessibilityService 任何静态引用，故引导弹窗、跳设置点、遮罩与拒权循环不可静态还原。",
  "summary_one_liner": "以「Flash Player」为外壳声明可读取窗口内容的无障碍服务，业务逻辑经 DexGuard 运行期解密，配套内置 Сбербанк 银行协议页与银行卡/CVC 录入 HTML 及透明 Inject 活动、独立进程 CommandService、短信自启接收器。",
  "disguise_identity": {
    "app_display_name": "Flash Player",
    "claimed_brand_or_persona": "ПАО Сбербанк（俄罗斯联邦储蓄银行）试点项目/Сбербанк Онлайн 客户端",
    "a11y_service_label": "无（Manifest 中该 service 未设置 android:label，accessibility_service_config 亦无 android:description，系统无障碍列表将显示为默认空标签/包名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "所有 Activity 的 android:label 均为随机小写字母串（如 ayiztuoyfjnqyipjpnn、kybqisbosbulzxuowqghyfqmgkzha），Permission/Admin/Systems/Inject/InjectCC 标签为空字符串；Inject 与 InjectCC 使用 android:icon=@drawable/background、excludeFromRecents、launchMode=singleTask 隐藏任务栈；无障碍项无 description 说明；类名与成员名混淆为随机词（acquirefringe/loungedeputy/eaglehint 等）并插入大量无意义算术以干扰反编译；无伪造 isAccessibilityTool 证据（targetSdk 28，低于该属性引入版本）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "security.sword.MainActivity（LAUNCHER + android.app.role.SMS 类别）；进程级 artwork.differ.kitchen.ALdKxTnSqDnMtXhHwBmBkNmRyLsKnChBbGdRxZbWzNpZhEhKf（Application）",
      "trigger_event": "用户点击桌面「Flash Player」图标启动；Application.attachBaseContext() 先执行 DexGuard 解密并装载业务类",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（MainActivity 类体被加密，未取得界面文案）",
      "shown_text_zh": "不可静态还原；Manifest 层面仅确认透明无标题主题 Theme.Translucent.NoTitleBar",
      "user_action_requested": "不可静态还原",
      "code_anchor": "artwork.differ.kitchen.ALdKxTnSqDnMtXhHwBmBkNmRyLsKnChBbGdRxZbWzNpZhEhKf.attachBaseContext / security.sword.MainActivity"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "不可静态还原（预期为 security.sword 包下某个随机名 Activity，如 KQoUsNwPeLuQcNoLqJkNrLzKhBlZhXhDmOcGtCiUnJfRhSsAr、Permission 等）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（无静态可定位的引导文案；res/strings 中未检索到无障碍相关说明文本）",
      "shown_text_zh": "不可静态还原",
      "user_action_requested": "不可静态还原（无法确认是否存在取消/跳过按钮）",
      "code_anchor": "security.sword.Permission（android:label=\"\"）/ res/xml/accessibility_service_config.xml"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "预期为系统「设置 → 无障碍 → 已下载的服务」页面",
      "trigger_event": "不可静态还原（DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 静态引用，跳转常量由运行期解密代码持有）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍列表中将出现一项无标签、无说明的服务（对应 security.sword.AccesService）",
      "user_action_requested": "不可静态还原；系统页面上用户需手动找到并开启该服务，无 android:description 说明其真实用途",
      "code_anchor": "#1 manifest:components（service security.sword.AccesService）/ res/xml/accessibility_service_config.xml"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "security.sword.AccesService（无障碍服务）→ security.sword.Inject / InjectCC（透明 overlay 活动）、security.sword.CommandService（:cproc 独立进程）、assets/android/index.html 银行卡表单、assets/offer.html Сбербанк 协议页",
      "trigger_event": "无障碍服务被系统启用后 onServiceConnected（实现体加密，不可静态确认）；BOOT_COMPLETED 由 SmsBroadcast / AlarmBroadcastReceiver 重新拉起",
      "ui_carrier": "本地HTML WebView + 悬浮窗Overlay（据 Manifest 组件与 assets 推断，实现体不可静态还原）",
      "shown_text_verbatim": "Соглашение об участии в пилотном проекте Банка … между ПАО Сбербанк … и клиентом ПАО Сбербанк, использующим автоматизированную систему Сбербанк Онлайн",
      "shown_text_zh": "「关于参与银行试点项目的协议……由 ПАО Сбербанк（俄罗斯联邦储蓄银行）与使用 Сбербанк Онлайн 自动化系统的客户签订」——冒充银行试点协议，配合卡号/CVC/有效期录入表单",
      "user_action_requested": "在仿冒银行页面填写卡号、有效期、CVC、姓名、地址、出生日期（表单字段见 index.html）",
      "code_anchor": "assets/offer.html / assets/android/index.html / security.sword.Inject（excludeFromRecents, @drawable/background）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：security.sword.AccesService 无 android:label、无 android:description（accessibility_service_config.xml 中仅配置事件类型与 canRetrieveWindowContent），用户看不到任何用途说明",
    "res/strings 与 res/xml 中未检索到任何无障碍引导/教学文案，说明引导文字不在静态资源内，由 DexGuard 解密后的代码或远端下发提供",
    "assets/offer.html：俄语 Сбербанк 试点项目协议长文（纯本地 HTML，用于伪装银行合规授权）",
    "assets/android/index.html：本地 HTML 银行卡录入表单（卡号、有效期、CVC、持卡人、地址、生日），含多国卡组织图标与 getCountryCode/getLanguageCode 地域适配脚本",
    "assets/report/bank_report_for_card_template*.html、bank_statement*.html：银行对账单/流水模板，用于伪造交易与余额界面",
    "所有引导弹窗/遮罩/WebView 教学页的具体呈现位置不可静态还原（security.sword.* 类体加密）"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Соглашение об участии в пилотном проекте Банка. Данное соглашение заключено между ПАО Сбербанк (далее - Банк) и клиентом ПАО Сбербанк, использующим автоматизированную систему Сбербанк Онлайн - защищенную систему дистанционного обслуживания клиента (далее - Клиент [1]) через мобильное приложение Сбербанк Онлайн",
      "text_zh": "关于参与银行试点项目的协议。本协议由 ПАО Сбербанк（下称「银行」）与通过 Сбербанк Онлайн 移动应用使用 Сбербанк Онлайн 自动化系统（客户远程服务安全系统）的 ПАО Сбербанк 客户（下称「客户」）签订。",
      "source_location": "assets/offer.html",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "CVC",
      "text_zh": "「CVC」——卡片安全码输入占位提示（表单同时采集 cardNumber、card-expiration、nameOnCard、firstname、lastname、date-birth）",
      "source_location": "assets/android/index.html（input placeholder=\"CVC\" / name=\"cardNumber\" / class=\"card-expiration\"）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Flash Player",
      "text_zh": "「Flash Player」——桌面图标显示名，宣称提供多媒体播放能力",
      "source_location": "AndroidManifest.xml application@android:label",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原（AccesService 与引导 Activity 类体被 DexGuard 加密；DEX 中无 ACTION_ACCESSIBILITY_SETTINGS 静态引用，onResume 重跳或定时器拉起逻辑无法确认）",
    "overlay_or_fake_settings": "未取得高仿设置页证据；但 Manifest 存在 security.sword.Inject 与 InjectCC 两个 excludeFromRecents、singleTask、透明背景图标的 Activity，具备在系统设置页之上叠加无痕遮罩的结构条件，实际叠层行为不可静态确认",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=28、minSdkVersion=16，低于 Android 13 受限设置机制适用版本；未发现对应引导文案或 Session 安装器路径）",
    "post_grant_anti_removal": "不可静态还原（未发现 GLOBAL_ACTION_BACK/HOME 静态调用；同包存在设备管理员 Admins 与独立进程 CommandService，具备阻碍撤权的能力条件但无静态证据）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动后首帧即拉起录屏/UTG 抓取，并以「页面标题或包名切换至 com.android.settings 无障碍页」为关键瞬间：一旦检测到前台窗口变为系统设置无障碍列表（或应用详情页），立即连续截图并提取节点树，捕捉跳转前页面与返回后的反应。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏/引导页",
        "page_identifier": "包名 artwork.differ.kitchen、透明无标题主题、桌面名为 Flash Player 的 Activity；可能伴随加载/更新提示",
        "why_most_useful": "判定引导是冷启动零步强制还是功能触发，并取得 DexGuard 解密后才出现的引导文案原文",
        "observable_utg_signals": ["首屏是否立即出现无障碍/授权相关弹窗或按钮", "是否存在取消、跳过、返回按钮", "是否出现「更新/故障/安全」类恐吓措辞", "界面是否出现银行品牌 Logo 与播放器身份不符"]
      },
      {
        "page_role": "跳转前教学页（原生或 WebView）",
        "page_identifier": "包含「设置 → 无障碍」「Настройки → Специальные возможности」等分步指引文字的 Activity/WebView",
        "why_most_useful": "该页承载「教用户开启无障碍」的完整话术与步骤编号，是诱导行为的直接证据",
        "observable_utg_signals": ["分步序号与箭头图示", "是否点名要求找到空标签服务项", "是否出现受限设置/应用详情右上角菜单的引导"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中新增的一项无描述服务（对应 security.sword.AccesService）",
        "why_most_useful": "验证系统列表中该服务确实无用途说明，是身份隐瞒与诱导成立的关键观测点",
        "observable_utg_signals": ["列表项名称是否为空或显示包名", "是否存在说明副标题", "用户是否需滚动到「已下载的服务」才能找到"]
      },
      {
        "page_role": "设置页返回后反应（拒权反馈/叠层）",
        "page_identifier": "从系统设置返回后自动弹出的弹窗、遮罩或再次被拉起的引导页",
        "why_most_useful": "判定拒权循环与遮罩叠层是否存在，这是强制性与非自愿授权的核心判别",
        "observable_utg_signals": ["返回后是否在 1~2 秒内自动重跳设置页", "是否出现全屏半透明遮罩或悬浮引导窗", "是否只有「去开启」单一按钮而无关闭途径"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区为 DexGuard 加密导致 security.sword.* 类体不可静态还原：引导文案、跳转时序、遮罩与拒权循环全部只能靠运行期 UTG 获取；另需注意资产中的钓鱼页面为本地 HTML（非远端），若攻击者仅按远端下发条件才展示引导，则离线环境可能只看到无害首屏。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "LURE_FAKE_UPDATE_OR_INSTALL"
  ],
  "code_anchors": [
    "artwork.differ.kitchen.ALdKxTnSqDnMtXhHwBmBkNmRyLsKnChBbGdRxZbWzNpZhEhKf.attachBaseContext",
    "security.sword.AccesService（Manifest 声明，类体 DexGuard 加密）",
    "res/xml/accessibility_service_config.xml",
    "assets/offer.html",
    "assets/android/index.html"
  ]
}
```

</details>
