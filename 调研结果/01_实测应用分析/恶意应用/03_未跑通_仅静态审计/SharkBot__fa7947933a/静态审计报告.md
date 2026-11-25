# MB_077__fa7947933a｜SharkBot — LiteCleaner M

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：132.7s

## 1. 一句话核心结论

- **核心申请方式**：以清理/加速工具身份，用原生权限弹窗（Grant Now / Grant permission to use accessibility service）+ 自定义 Find…and grant 引导页，在点击瞬间连跳 android.settings.ACCESSIBILITY_SETTINGS 并把自有引导页压在其上，索取本应用根本未声明的无障碍权限。
- **静态可见性说明**：无障碍引导链全部位于 DEX 明文中，未加壳、无加密字符串、无远端 HTML；引导弹窗为原生 Dialog（layout 2131558484），引导页为原生 Activity（layout 2131558442），跳转 action 以明文字符串常量硬编码。仅 GuildPermissionActivity 内两个按钮的 onClick 回调实现未逐一展开，属可见范围内的次要未读点。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `fa7947933a3561b7174f1d94472dcf8633a03749c14342ce65dafe94db361140` |
| 包名 / 年份 | `com.ltdevelopergroups.litecleaner.m` / 2022 |
| 家族 / 品类 | **SharkBot**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | LiteCleaner M |
| 引导页宣称品牌/身份 | Super Cleaner / Clean master（清理加速工具） |
| 系统无障碍列表服务名 | 无——Manifest 未声明任何 BIND_ACCESSIBILITY_SERVICE 服务，系统无障碍列表中没有本应用条目 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍说明文案自称 Super Cleaner/Clean master 而应用名为 LiteCleaner M；该 android:description 字符串未绑定任何服务（悬空文案）；文案内嵌换行与空行排版（Tap on top right use to Accessiblility service. \n \n …）并含 Accessiblility 拼写变形；文案明确要求用户忽略 Android 系统警告；无伪造 isAccessibilityTool、无多 activity-alias 伪装。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | e.j.a.a.i.t（权限编排基类）→ DialogAskPermission 原生对话框 | 功能页调用 t.W()/t.X()/t.Y()/t.c0 等权限门控方法，判定权限未授予后 DialogAskPermission.O0(action, 回调).N0(...) 弹出对话框 | 原生Dialog | **原文**：Grant permission to use accessibility service<br>**译注**：授予使用无障碍服务的权限 | 点击对话框唯一有效按钮（id 2131362608，文案取自布局 2131558484 的按钮控件）确认前往授权；对话框可返回键取消 | `com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission.L0 / P0` |
| 2 | 跳无障碍设置 | android.settings.ACCESSIBILITY_SETTINGS 系统页（startActivityForResult, requestCode 1111） | DialogAskPermission.click(View) → DialogAskPermission$a.a() 回调 → e.o.a.i.b.a() | 系统无障碍页 | **原文**：无（系统设置页，非应用绘制）<br>**译注**：系统「无障碍」设置界面 | 在系统无障碍列表中自行找到并开启本应用服务（实际无服务可开） | `e.o.a.i.b.a / com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission.click` |
| 3 | 遮罩叠层指引 | GuildPermissionActivity（自有引导 Activity，layout 2131558442，随跳转同帧压栈到系统设置页之上） | 同一回调内紧接 startActivityForResult 调用 GuildPermissionActivity.f0(context, "android.settings.ACCESSIBILITY_SETTINGS") | 原生Activity | **原文**：Find LiteCleaner M and grant accessibility permission<br>**译注**：找到 LiteCleaner M 并授予无障碍权限 | 照页面指示在系统页中定位本应用并开启；页面含两个按钮（id 2131362105、2131362183），其一为继续/前往、其一为关闭，具体回调未逐一展开 | `com.ltdevelopergroups.litecleaner.m.screen.guildPermission.GuildPermissionActivity.onCreate / f0` |
| 4 | 引导说明页 | FragmentAdvancedProtection 菜单弹窗（e.o.a.i.h.e + k 对话框）→ 跳 ACCESSIBILITY_SETTINGS | 高级防护菜单项点击（MenuFunction.b 回调 e.o.a.i.h.e.a()）；已授权则直接 I0(new Intent(ACCESSIBILITY_SETTINGS),1111)，未授权先弹对话框 | 原生Dialog | **原文**：Grant Now<br>**译注**：立即授予 | 点击 Grant Now 按钮进入系统无障碍页；对话框可取消 | `e.o.a.i.h.e.a / e.o.a.i.b.a` |
| 5 | 获权后动作 | e.o.a.a.a().c 状态标记（权限回调后置位） | e.o.a.i.b.a() 中 Objects.requireNonNull 后 e.o.a.a.a().c = true，随后 gVar.K0(false,false) 结束对话框流程 | 不可静态还原（后续消费无障碍权限的逻辑：Manifest 中无对应 AccessibilityService，无可执行消费点） | 无 | 无 | `e.o.a.i.b.a / #1 manifest:components` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- DialogAskPermission 原生对话框（layout 2131558484）正文：strings.xml accessibility_setting_permission = "Grant permission to use accessibility service"
- DialogAskPermission 高级防护入口版本标题：strings.xml grant_now = "Grant Now"
- GuildPermissionActivity 引导页（layout 2131558442）TextView：strings.xml find_and_grant = "Find %s and grant %s"，填充后为 "Find LiteCleaner M and grant accessibility permission"
- strings.xml accessibility_service_description（"Tap on top right use to Accessiblility service…Super Cleaner…accept Android system warinings…"）——因无服务声明，实际不会出现在系统无障碍列表，属悬空文案
- strings.xml content_permission_1（"Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%"）——以 50% 加速为诱因的权限话术
- 未发现 WebView 本地/远端 HTML、悬浮窗遮罩或高仿系统无障碍开关页承载引导文字

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Grant permission to use accessibility service | 授予使用无障碍服务的权限 | `res/values/strings.xml accessibility_setting_permission（DialogAskPermission.P0 引用 2131951654）` | 清理工具伪装 |
| en | Find LiteCleaner M and grant accessibility permission | 找到 LiteCleaner M 并授予无障碍权限 | `res/values/strings.xml find_and_grant（GuildPermissionActivity.onCreate 引用 2131951820）` | 受限设置分步教学 |
| en | Grant Now | 立即授予 | `res/values/strings.xml grant_now（e.o.a.i.h.e.a 引用 2131951839）` | 清理工具伪装 |
| en | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. | 点击右上角以使用无障碍服务。这将允许 Super Cleaner 进行：- 深度清理隐藏垃圾 - 休眠耗电应用。开启无障碍服务时你必须接受 Android 系统警告。Clean master 不会将其用于此处列出的之外的任何其他用途。 | `res/values/strings.xml accessibility_service_description` | 教唆忽视警告 |
| en | Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50% | 请授予无障碍权限以关闭以下自启动应用，加速效果可提升 50% | `res/values/strings.xml content_permission_1` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：未发现 onResume 死循环重跳或定时器强制拉起的静态证据；对话框可被返回键/取消按钮关闭，取消后本次功能调用中止（gVar.K0(false,false)），下次触发该功能时权限门控（t.W/X/Y 的权限判定）会再次弹出同一对话框，形成按需重复劝说而非强制循环。
- **遮罩叠层 / 高仿系统设置页**：无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；叠层方式为把自有 GuildPermissionActivity 引导页与系统 ACCESSIBILITY_SETTINGS 同帧压栈，视觉上呈现为「系统页 + 应用指示页」。
- **Android 13+ 受限设置（Restricted Settings）应对**：有——跳转 ACTION_APPLICATION_DETAILS_SETTINGS 的实现存在于 e.j.a.a.b.k$b.onClick（携带 package: 打开应用详情页），配合 REQUEST_INSTALL_PACKAGES 权限，具备引导用户进入应用详情页（Android 13+ 受限设置入口）的能力；但未发现明确的「点右上角菜单允许受限设置」文字教学。
- **获权后即时行为与防撤权机制**：未发现获权后自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权的证据；但存在 WatchmenReceiver/RestarterBroadcastReceiver/AutoRebootReceiver(priority 99999) 等保活组件。
- **良性降级 / 替代方案**：无——包内不存在任何 AccessibilityService 消费该权限，也未提供无障碍不可用时的替代降级路径说明。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivityForResult(Intent("android.settings.ACCESSIBILITY_SETTINGS"),1111) 的瞬间（或 DialogAskPermission 对话框出现时）即拉起 UTG，可完整捕获「弹窗→系统页→压栈引导页」三层流转。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文字全部为可提取文本，无纯图空文本诱导；但存在两点盲区：一是无障碍权限在包内无对应服务消费，获权后的真实用途不可从 Manifest/服务层观察，需动态监测后续行为（如是否出现模拟点击、读屏采集）；二是 assets/vxoid.bin 等资产未展开，可能存在二阶段载荷，但不影响本 UTG 命题。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **权限索取弹窗页（第一触点）** | DialogAskPermission 对话框，正文 "Grant permission to use accessibility service" 或标题 "Grant Now" | 此处可直接判定应用是否以非无障碍功能为名索取无障碍权限，并观察是否存在取消路径 | 对话框标题/正文文本（Grant Now / Grant permission to use accessibility service）；按钮数量与可取消性（是否有取消/关闭控件）；弹窗触发的前置功能页上下文 |
| **跳转后 800ms 压栈引导页** | GuildPermissionActivity（layout 2131558442），文本 "Find LiteCleaner M and grant accessibility permission" | 这是最关键的 UTG 证据：应用在系统无障碍页之上主动叠加指示层，说明其目的是引导用户开启本应用服务 | 指示文案原文（Find…and grant…）；该 Activity 与系统 ACCESSIBILITY_SETTINGS 的压栈关系（是否遮挡系统页）；页内按钮语义（继续/关闭） |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已安装的服务列表 | 用于验证身份错配：应用自身并未声明任何 BIND_ACCESSIBILITY_SERVICE 服务，列表中将找不到 LiteCleaner M 条目，而引导页却指示用户去开启 | 列表中是否存在本应用无障碍服务条目；服务名与显示名是否与引导文案一致 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission.click`
- `com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission.P0`
- `e.o.a.i.b.a`
- `com.ltdevelopergroups.litecleaner.m.screen.guildPermission.GuildPermissionActivity.onCreate`
- `e.j.a.a.i.h.e.a`
- `res/values/strings.xml (accessibility_service_description / accessibility_setting_permission / find_and_grant / grant_now)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯运行期 UTG 视角）

**一句话结论**：该应用（`com.ltdevelopergroups.litecleaner.m`，显示名 LiteCleaner M）**在 Manifest 中根本没有声明任何无障碍服务**，却通过原生 Dialog + 自定义引导 Activity 的双层页面，把用户从"清理/加速"功能页一步步送到系统 `android.settings.ACCESSIBILITY_SETTINGS`，属于典型的纯运行期 UTG 权限索取，而不是无障碍功能自用。

**关键事实链**

1. **引导载体是原生 Dialog，非 WebView/悬浮窗**：权限编排由基类 `e.j.a.a.i.t` 统一负责，权限未满足时弹 [DialogAskPermission.L0()](<resource-unit:#1.dex1 code:com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission#L0>)，`inflate(2131558484)` + ButterKnife 绑定，正文由 [P0()](<resource-unit:#1.dex1 code:com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission#P0>) 按 intent action 字符串分支设置：无障碍分支取 `2131951654` = `accessibility_setting_permission` → *"Grant permission to use accessibility service"*。
2. **点击"确认"即跳系统无障碍页**：[DialogAskPermission.click()](<resource-unit:#1.dex1 code:com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission#click>) 仅对按钮 id `2131362608` 生效，回调 [e.o.a.i.b.a()](<resource-unit:#1.dex1 code:e.o.a.i.b#a>) 执行 `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1111)`，**紧接着**再调 `GuildPermissionActivity.g0(ctx, "android.settings.ACCESSIBILITY_SETTINGS")` 把自有引导页压栈到系统设置页之上。
3. **第二层"手把手找服务"教学页**：[GuildPermissionActivity.onCreate()](<resource-unit:#1.dex1 code:com.ltdevelopergroups.litecleaner.m.screen.guildPermission.GuildPermissionActivity#onCreate>) 用 `getString(2131951820=find_and_grant, app_name, accessibility_permission)` 生成 *"Find %s and grant %s"* → **"Find LiteCleaner M and grant accessibility permission"**，明确指示用户在系统列表里找到本应用并开启；页面有两个按钮监听（`2131362105` / `2131362183`），布局 `2131558442`。
4. **第二条入口（高级防护菜单）**：[e.o.a.i.h.e.a()](<resource-unit:#1.dex1 code:e.o.a.i.h.e#a>) 在 `FragmentAdvancedProtection` 菜单点击时，标题取 `2131951839` = `grant_now` → *"Grant Now"*，同样构造 `ACCESSIBILITY_SETTINGS` 跳转；已授权时直接跳系统页，未授权时先弹对话框。
5. **身份与告知不实**：`accessibility_service_description`（[strings.xml](<resource-unit:#1 file:res/values/strings.xml#L39-L48>)）以 **"Super Cleaner"/"Clean master"** 自称（实际应用名 LiteCleaner M），并明写 *"You will have to accept Android system warinings when enabling Accessibility service"* —— 教唆用户忽略系统警告。该 description 字符串因无服务声明而**不会出现在系统无障碍列表中**，属悬空话术。
6. **能力与权限错配**：Manifest 仅有 `NotificationListener` 与 `ServiceManager`，**无 `BIND_ACCESSIBILITY_SERVICE` 服务、无 a11y 配置 xml**；获取的无障碍权限在包内无对应服务可消费，权限诉求与功能陈述不一致。

**边界**：`GuildPermissionActivity` 两个按钮的具体回调（取消/继续）未逐一反编译确认；未发现 `onResume` 死循环重跳或设置页遮罩叠层的静态证据；`assets/vxoid.bin` 未展开（不影响本命题）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链全部位于 DEX 明文中，未加壳、无加密字符串、无远端 HTML；引导弹窗为原生 Dialog（layout 2131558484），引导页为原生 Activity（layout 2131558442），跳转 action 以明文字符串常量硬编码。仅 GuildPermissionActivity 内两个按钮的 onClick 回调实现未逐一展开，属可见范围内的次要未读点。",
  "summary_one_liner": "以清理/加速工具身份，用原生权限弹窗（Grant Now / Grant permission to use accessibility service）+ 自定义 Find…and grant 引导页，在点击瞬间连跳 android.settings.ACCESSIBILITY_SETTINGS 并把自有引导页压在其上，索取本应用根本未声明的无障碍权限。",
  "disguise_identity": {
    "app_display_name": "LiteCleaner M",
    "claimed_brand_or_persona": "Super Cleaner / Clean master（清理加速工具）",
    "a11y_service_label": "无——Manifest 未声明任何 BIND_ACCESSIBILITY_SERVICE 服务，系统无障碍列表中没有本应用条目",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍说明文案自称 Super Cleaner/Clean master 而应用名为 LiteCleaner M；该 android:description 字符串未绑定任何服务（悬空文案）；文案内嵌换行与空行排版（Tap on top right use to Accessiblility service. \\n \\n …）并含 Accessiblility 拼写变形；文案明确要求用户忽略 Android 系统警告；无伪造 isAccessibilityTool、无多 activity-alias 伪装。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "e.j.a.a.i.t（权限编排基类）→ DialogAskPermission 原生对话框",
      "trigger_event": "功能页调用 t.W()/t.X()/t.Y()/t.c0 等权限门控方法，判定权限未授予后 DialogAskPermission.O0(action, 回调).N0(...) 弹出对话框",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Grant permission to use accessibility service",
      "shown_text_zh": "授予使用无障碍服务的权限",
      "user_action_requested": "点击对话框唯一有效按钮（id 2131362608，文案取自布局 2131558484 的按钮控件）确认前往授权；对话框可返回键取消",
      "code_anchor": "com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission.L0 / P0"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS 系统页（startActivityForResult, requestCode 1111）",
      "trigger_event": "DialogAskPermission.click(View) → DialogAskPermission$a.a() 回调 → e.o.a.i.b.a()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统设置页，非应用绘制）",
      "shown_text_zh": "系统「无障碍」设置界面",
      "user_action_requested": "在系统无障碍列表中自行找到并开启本应用服务（实际无服务可开）",
      "code_anchor": "e.o.a.i.b.a / com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission.click"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "GuildPermissionActivity（自有引导 Activity，layout 2131558442，随跳转同帧压栈到系统设置页之上）",
      "trigger_event": "同一回调内紧接 startActivityForResult 调用 GuildPermissionActivity.f0(context, \"android.settings.ACCESSIBILITY_SETTINGS\")",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Find LiteCleaner M and grant accessibility permission",
      "shown_text_zh": "找到 LiteCleaner M 并授予无障碍权限",
      "user_action_requested": "照页面指示在系统页中定位本应用并开启；页面含两个按钮（id 2131362105、2131362183），其一为继续/前往、其一为关闭，具体回调未逐一展开",
      "code_anchor": "com.ltdevelopergroups.litecleaner.m.screen.guildPermission.GuildPermissionActivity.onCreate / f0"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "FragmentAdvancedProtection 菜单弹窗（e.o.a.i.h.e + k 对话框）→ 跳 ACCESSIBILITY_SETTINGS",
      "trigger_event": "高级防护菜单项点击（MenuFunction.b 回调 e.o.a.i.h.e.a()）；已授权则直接 I0(new Intent(ACCESSIBILITY_SETTINGS),1111)，未授权先弹对话框",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Grant Now",
      "shown_text_zh": "立即授予",
      "user_action_requested": "点击 Grant Now 按钮进入系统无障碍页；对话框可取消",
      "code_anchor": "e.o.a.i.h.e.a / e.o.a.i.b.a"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "e.o.a.a.a().c 状态标记（权限回调后置位）",
      "trigger_event": "e.o.a.i.b.a() 中 Objects.requireNonNull 后 e.o.a.a.a().c = true，随后 gVar.K0(false,false) 结束对话框流程",
      "ui_carrier": "不可静态还原（后续消费无障碍权限的逻辑：Manifest 中无对应 AccessibilityService，无可执行消费点）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面；仅内部状态置位，包内不存在消费该权限的无障碍服务",
      "user_action_requested": "无",
      "code_anchor": "e.o.a.i.b.a / #1 manifest:components"
    }
  ],
  "text_presentation_locations": [
    "DialogAskPermission 原生对话框（layout 2131558484）正文：strings.xml accessibility_setting_permission = \"Grant permission to use accessibility service\"",
    "DialogAskPermission 高级防护入口版本标题：strings.xml grant_now = \"Grant Now\"",
    "GuildPermissionActivity 引导页（layout 2131558442）TextView：strings.xml find_and_grant = \"Find %s and grant %s\"，填充后为 \"Find LiteCleaner M and grant accessibility permission\"",
    "strings.xml accessibility_service_description（\"Tap on top right use to Accessiblility service…Super Cleaner…accept Android system warinings…\"）——因无服务声明，实际不会出现在系统无障碍列表，属悬空文案",
    "strings.xml content_permission_1（\"Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%\"）——以 50% 加速为诱因的权限话术",
    "未发现 WebView 本地/远端 HTML、悬浮窗遮罩或高仿系统无障碍开关页承载引导文字"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Grant permission to use accessibility service",
      "text_zh": "授予使用无障碍服务的权限",
      "source_location": "res/values/strings.xml accessibility_setting_permission（DialogAskPermission.P0 引用 2131951654）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Find LiteCleaner M and grant accessibility permission",
      "text_zh": "找到 LiteCleaner M 并授予无障碍权限",
      "source_location": "res/values/strings.xml find_and_grant（GuildPermissionActivity.onCreate 引用 2131951820）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Grant Now",
      "text_zh": "立即授予",
      "source_location": "res/values/strings.xml grant_now（e.o.a.i.h.e.a 引用 2131951839）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "text_zh": "点击右上角以使用无障碍服务。这将允许 Super Cleaner 进行：- 深度清理隐藏垃圾 - 休眠耗电应用。开启无障碍服务时你必须接受 Android 系统警告。Clean master 不会将其用于此处列出的之外的任何其他用途。",
      "source_location": "res/values/strings.xml accessibility_service_description",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%",
      "text_zh": "请授予无障碍权限以关闭以下自启动应用，加速效果可提升 50%",
      "source_location": "res/values/strings.xml content_permission_1",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "未发现 onResume 死循环重跳或定时器强制拉起的静态证据；对话框可被返回键/取消按钮关闭，取消后本次功能调用中止（gVar.K0(false,false)），下次触发该功能时权限门控（t.W/X/Y 的权限判定）会再次弹出同一对话框，形成按需重复劝说而非强制循环。",
    "overlay_or_fake_settings": "无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；叠层方式为把自有 GuildPermissionActivity 引导页与系统 ACCESSIBILITY_SETTINGS 同帧压栈，视觉上呈现为「系统页 + 应用指示页」。",
    "restricted_settings_13plus_coaching": "有——跳转 ACTION_APPLICATION_DETAILS_SETTINGS 的实现存在于 e.j.a.a.b.k$b.onClick（携带 package: 打开应用详情页），配合 REQUEST_INSTALL_PACKAGES 权限，具备引导用户进入应用详情页（Android 13+ 受限设置入口）的能力；但未发现明确的「点右上角菜单允许受限设置」文字教学。",
    "post_grant_anti_removal": "未发现获权后自点确认、GLOBAL_ACTION_BACK/HOME 阻止撤权的证据；但存在 WatchmenReceiver/RestarterBroadcastReceiver/AutoRebootReceiver(priority 99999) 等保活组件。",
    "benign_graceful_degradation": "无——包内不存在任何 AccessibilityService 消费该权限，也未提供无障碍不可用时的替代降级路径说明。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivityForResult(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"),1111) 的瞬间（或 DialogAskPermission 对话框出现时）即拉起 UTG，可完整捕获「弹窗→系统页→压栈引导页」三层流转。",
    "key_pages_to_capture": [
      {
        "page_role": "权限索取弹窗页（第一触点）",
        "page_identifier": "DialogAskPermission 对话框，正文 \"Grant permission to use accessibility service\" 或标题 \"Grant Now\"",
        "why_most_useful": "此处可直接判定应用是否以非无障碍功能为名索取无障碍权限，并观察是否存在取消路径",
        "observable_utg_signals": ["对话框标题/正文文本（Grant Now / Grant permission to use accessibility service）", "按钮数量与可取消性（是否有取消/关闭控件）", "弹窗触发的前置功能页上下文"]
      },
      {
        "page_role": "跳转后 800ms 压栈引导页",
        "page_identifier": "GuildPermissionActivity（layout 2131558442），文本 \"Find LiteCleaner M and grant accessibility permission\"",
        "why_most_useful": "这是最关键的 UTG 证据：应用在系统无障碍页之上主动叠加指示层，说明其目的是引导用户开启本应用服务",
        "observable_utg_signals": ["指示文案原文（Find…and grant…）", "该 Activity 与系统 ACCESSIBILITY_SETTINGS 的压栈关系（是否遮挡系统页）", "页内按钮语义（继续/关闭）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已安装的服务列表",
        "why_most_useful": "用于验证身份错配：应用自身并未声明任何 BIND_ACCESSIBILITY_SERVICE 服务，列表中将找不到 LiteCleaner M 条目，而引导页却指示用户去开启",
        "observable_utg_signals": ["列表中是否存在本应用无障碍服务条目", "服务名与显示名是否与引导文案一致"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文字全部为可提取文本，无纯图空文本诱导；但存在两点盲区：一是无障碍权限在包内无对应服务消费，获权后的真实用途不可从 Manifest/服务层观察，需动态监测后续行为（如是否出现模拟点击、读屏采集）；二是 assets/vxoid.bin 等资产未展开，可能存在二阶段载荷，但不影响本 UTG 命题。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION"
  ],
  "code_anchors": [
    "com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission.click",
    "com.ltdevelopergroups.litecleaner.m.dialog.DialogAskPermission.P0",
    "e.o.a.i.b.a",
    "com.ltdevelopergroups.litecleaner.m.screen.guildPermission.GuildPermissionActivity.onCreate",
    "e.j.a.a.i.h.e.a",
    "res/values/strings.xml (accessibility_service_description / accessibility_setting_permission / find_and_grant / grant_now)"
  ]
}
```

</details>
