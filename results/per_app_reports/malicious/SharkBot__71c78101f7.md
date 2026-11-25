# MB_006__71c78101f7｜SharkBot — Alfa Antivirus, Cleaner

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：230.3s

## 1. 一句话核心结论

- **核心申请方式**：以清理杀毒加速为诱饵，按云端加密配置在每次回前台弹原生引导弹窗，点确认即跳系统无障碍设置并压入引导页，未开启则返回后循环重弹，服务名与桌面名一致且描述教用户忽略系统警告。
- **静态可见性说明**：引导全链路（云控门控判定、原生引导弹窗、ACTION_ACCESSIBILITY_SETTINGS 跳转、压栈引导页、系统无障碍列表文案）均完整静态可见；仅远端下发的 SESSION 开关值（atsFull/status）被硬编码密钥 AES 加密存储，具体取值需运行期确认，但不影响流程判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `71c78101f7792fe879a082e323fed89c5e4a43132d01d3f79ed02afd8db45497` |
| 包名 / 年份 | `com.pagnotto28.sellsourcecode.alpha` / 2022 |
| 家族 / 品类 | **SharkBot**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Alfa Antivirus, Cleaner |
| 引导页宣称品牌/身份 | Alfa Antivirus, Cleaner（描述文案中另自称 Super Cleaner / Clean master） |
| 系统无障碍列表服务名 | Alfa Antivirus, Cleaner |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍描述中连续空行 " \n \n" 分隔并把关键警告语放在末尾；多处故意错拼（Accessiblility / warinings / orther / tollowing）弱化识别；描述内自称 Super Cleaner 与 Clean master，与桌面名 Alfa Antivirus, Cleaner 不一致；代码整体混淆为 d.j.a.a.* 短名；会话配置以硬编码密钥 AES 加密存储。 |
| 无障碍服务类名 | `com.pagnotto28.sellsourcecode.alpha.service.ForceStopAccessibility` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Tap on top right use to Accessiblility service. <br> <br>This will allow Super Cleaner to: <br> <br>- Deep clean hidden junk <br>- Hibernate draining apps <br> <br>You will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.pagnotto28.sellsourcecode.alpha.screen.main.MainActivity（SplashActivity 之后的主界面） | onResume() → Y() | 原生Activity | **原文**：无（此步仅读取本地/云端配置）<br>**译注**：无界面呈现，仅解密 SESSION 配置并调度 7 秒后复核 | 无 | `MainActivity.onResume → d.j.a.a.j.s.Y（AES 密钥 IIBCgKCntNatAu9qo1QgM8FH7）` |
| 2 | 业务功能触发 | d.j.a.a.j.s#c0 门控方法 | Y() 内 checkResult 判定；或用户点击首页/工具页功能入口（MainActivity$a.onClick → f0） | 不可静态还原（开关值来自远端 AES 加密 JSON） | 无 | 无 | `d.j.a.a.j.s#c0` |
| 3 | 引导说明页 | com.pagnotto28.sellsourcecode.alpha.dialog.DialogAskPermission（layout 2131558481） | c0() 判定未授权 → f0() → DialogAskPermission.N0("android.settings.ACCESSIBILITY_SETTINGS", ...) | 原生Dialog | **原文**：Grant permission to use accessibility service<br>**译注**：授予使用无障碍服务的权限 | 点击确认按钮（Grant Permission）或取消；对话框 setCancelable(true)、setCanceledOnTouchOutside(true)，可跳过 | `DialogAskPermission#O0（string 2131951653 = accessibility_setting_permission）/ #k0 / #click` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | DialogAskPermission#click 回调 → d.j.a.a.j.m#a | 系统无障碍页 | **原文**：无（由系统渲染）<br>**译注**：跳转至系统无障碍服务列表 | 在系统列表中手动找到并开启服务开关 | `d.j.a.a.j.m#a：startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` |
| 5 | 遮罩叠层指引 | com.pagnotto28.sellsourcecode.alpha.screen.guildPermission.GuildPermissionActivity（紧接 startActivity 压栈） | d.j.a.a.j.m#a 同方法内 GuildPermissionActivity.i0(ctx, "android.settings.ACCESSIBILITY_SETTINGS") → onCreate | 原生Activity | **原文**：Find Alfa Antivirus, Cleaner and grant accessibility permission<br>**译注**：找到「Alfa Antivirus, Cleaner」并授予无障碍权限 | 按页面指示在系统列表中找到同名条目并开启；页面含返回/关闭按钮（findViewById 2131362082、2131362159 点击关闭） | `GuildPermissionActivity#onCreate（getString(2131951809=find_and_grant, app_name, 2131951651=accessibility_permission)）` |
| 6 | 跳无障碍设置 | 系统无障碍列表中的 ForceStopAccessibility 条目 | 用户到达系统无障碍服务列表 | 系统无障碍页 | **原文**：Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.<br>**译注**：点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾；休眠耗电应用。启用无障碍服务时你需要接受 Android 系统的警告。Clean master 不会将这些用于此处列出的以外的任何其他目的。 | 忽略系统弹出的无障碍高危警告并确认开启 | `res/xml/accessibility_service_config.xml + res/values/strings.xml#accessibility_service_description；Manifest service android:label=@string/app_name` |
| 7 | 拒权反馈循环 | MainActivity.onResume → Y() → c0() → f0()（再次 DialogAskPermission） | 用户从系统设置按返回键回到应用（onResume） | 原生Dialog | **原文**：Grant permission to use accessibility service<br>**译注**：再次弹出同一授权弹窗（无冷却、无「不再提示」选项） | 再次要求授权；可再次取消，但每次回前台都会重弹 | `d.j.a.a.j.s#Y → #c0 → #f0` |
| 8 | 获权后动作 | 系统设置 android.settings.MANAGE_UNKNOWN_APP_SOURCES（应用自身包名） | Y() 中 V(false) 为真且 ForceStopAccessibility 已启用 → r=2 → canRequestPackageInstalls() 为假 | 系统无障碍页（后续为系统安装来源页） | **原文**：无（h0("waitSource"); S("atsSource")）<br>**译注**：获权后转入未知来源安装授权，为后续投放安装包做准备 | 允许本应用安装未知应用 | `d.j.a.a.j.s#Y（Intent android.settings.MANAGE_UNKNOWN_APP_SOURCES）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 原生 Dialog（DialogAskPermission，layout 2131558481，dimAmount 0.7）正文：Grant permission to use accessibility service（string accessibility_setting_permission）
- 原生 Activity（GuildPermissionActivity，layout 2131558441）正文：Find Alfa Antivirus, Cleaner and grant accessibility permission（string find_and_grant 格式化 app_name + accessibility_permission）
- 系统无障碍服务列表条目名：@string/app_name = Alfa Antivirus, Cleaner（与桌面图标名完全一致）
- 系统无障碍服务条目描述：@string/accessibility_service_description（含 Super Cleaner / Clean master 话术与「接受系统警告」提示）
- 系统无障碍条目摘要键：string accessibility_permission = accessibility permission
- 清理/加速类功能页话术：string content_permission_1 = Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Grant permission to use accessibility service | 授予使用无障碍服务的权限 | `res/values/strings.xml key=accessibility_setting_permission（DialogAskPermission#O0 引用 2131951653）` | 受限设置分步教学 |
| en | Find %s and grant %s | 找到 %s 并授予 %s（实际渲染为 Find Alfa Antivirus, Cleaner and grant accessibility permission） | `res/values/strings.xml key=find_and_grant（GuildPermissionActivity#onCreate 引用 2131951809）` | 受限设置分步教学 |
| en | Tap on top right use to Accessiblility service. \n \nThis will allow Super Cleaner to: \n \n- Deep clean hidden junk \n- Hibernate draining apps \n \nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here. | 点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾；休眠耗电应用。启用无障碍服务时你需要接受 Android 系统的警告。Clean master 不会将其用于此处所列以外的任何其他目的。 | `res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）` | 教唆忽视警告 |
| en | Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50% | 请授予无障碍权限以关闭以下自启动应用，加速效果可提升 50%。 | `res/values/strings.xml key=content_permission_1` | 清理工具伪装 |
| en | accessibility permission | 无障碍权限 | `res/values/strings.xml key=accessibility_permission` | 良性透明说明 |
| en | Enable now | 立即启用 | `res/values/strings.xml key=Notificationbarcleanup_RightNow` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：用户取消弹窗或从系统设置按返回后，MainActivity.onResume 再次执行 Y() → c0()，只要远端 atsFull 仍在且 ForceStopAccessibility 未启用即再次调用 f0() 弹出同一引导弹窗；无冷却计时、无「不再提示」开关，形成每次回前台必弹的循环。
- **遮罩叠层 / 高仿系统设置页**：无全屏悬浮窗或高仿系统无障碍开关页；采用原生 Dialog（dimAmount 0.7 半透明背景）+ 在 startActivity(ACCESSIBILITY_SETTINGS) 同一方法内压栈 GuildPermissionActivity 引导页的方式，让引导页覆盖在系统设置页之上。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（未使用 ACTION_APPLICATION_DETAILS_SETTINGS，无 Android 13 受限设置分步教学，targetSdk=30）
- **获权后即时行为与防撤权机制**：有间接对抗：Y() 在检测到无障碍已启用后立即推进 r=2 并跳转 MANAGE_UNKNOWN_APP_SOURCES 申请安装未知应用权限（前置投放环节）；无障碍服务运行于 :BackgroundService 独立进程并配合 LockRestarterBroadcastReceiver 等常驻机制，但未见监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接代码。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动进入 MainActivity 后首次 onResume 完成 SESSION 解密并触发 f0() 的瞬间；以及 DialogAskPermission 确认按钮回调 d.j.a.a.j.m#a 执行 startActivity(ACCESSIBILITY_SETTINGS) 后 300–800ms（引导页压栈完成、系统设置页被覆盖）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导文案全部为可提取文本，无图片诱饵；但两点需注意：一是是否弹窗由远端下发并经 AES 加密存储的 SESSION（atsFull/status）决定，离线或未取到配置时可能不触发，静态无法确定线上触发率；二是紧随其后的 MANAGE_UNKNOWN_APP_SOURCES 与安装动作属于下一阶段投放，本 UTG 观测仅覆盖无障碍索取阶段。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | com.pagnotto28.sellsourcecode.alpha.dialog.DialogAskPermission，半透明遮罩（dimAmount 0.7），标题含应用名、正文含 Grant permission 与 Grant Permission 按钮 | 证明索要无障碍由应用主动发起、文案为纯功能收益诱导而非系统原生提示 | 对话框包名归属为 com.pagnotto28.sellsourcecode.alpha；正文文本 Grant permission to use accessibility service；按钮文案 Grant Permission 与取消按钮并存 |
| **设置页后压栈遮罩页（引导教学页）** | com.pagnotto28.sellsourcecode.alpha.screen.guildPermission.GuildPermissionActivity，叠于系统设置之上 | 区分「仅跳系统设置」与「跳转后强制叠加指引」，是诱导链完整性的关键判据 | Activity 归属为应用包名而非 com.android.settings；文本 Find Alfa Antivirus, Cleaner and grant accessibility permission；页面出现于系统设置页启动之后 |
| **系统无障碍服务列表项** | com.android.settings 无障碍列表中的 Alfa Antivirus, Cleaner 条目 | 核验服务标签与桌面名一致（身份不可区分）及描述中教用户接受系统警告 | 条目名 Alfa Antivirus, Cleaner；描述文本含 accept Android system warinings；开关状态由关变为开的时间点 |
| **拒权返回后的重弹页** | 从系统设置返回 MainActivity 后再次出现的 DialogAskPermission | 证明存在无冷却的循环索要，构成强制施压 | 同一对话框在返回后 1–2 秒内重复出现；连续出现次数；无「不再提示」选项 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.pagnotto28.sellsourcecode.alpha.screen.main.MainActivity#onResume`
- `d.j.a.a.j.s#Y`
- `d.j.a.a.j.s#c0`
- `com.pagnotto28.sellsourcecode.alpha.dialog.DialogAskPermission#O0`
- `d.j.a.a.j.m#a`
- `com.pagnotto28.sellsourcecode.alpha.screen.guildPermission.GuildPermissionActivity#onCreate`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

- **引导链条静态完全可见**（无 WebView/HTML、无悬浮窗遮罩），全部由原生 Dialog + 原生 Activity + 系统设置页构成：
  1. `MainActivity.onResume()` 每次回前台调 `Y()`，从 SharedPreferences 取 `SESSION` 并用硬编码密钥 `IIBCgKCntNatAu9qo1QgM8FH7` 解密为 JSON，读 `atsFull` / `status` 开关，并用 `postDelayed(7000ms)` 延迟复核——**是否索要无障碍由云端加密配置决定**。
  2. `c0()` 判定：`atsFull` 存在且 `ForceStopAccessibility` 未启用 → `S("atsFull"); h0("waitA11"); r=1; f0()`。
  3. `f0()` 弹 `DialogAskPermission`，正文 = `accessibility_setting_permission`「Grant permission to use accessibility service」；`dimAmount=0.7f`，`setCancelable(true)`（**有取消/点外部关闭**）。
  4. 点确认 → 回调 `d.j.a.a.j.m#a` **同时** `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 与 `GuildPermissionActivity.i0(...)`，即把引导页压到系统设置页之上。
  5. `GuildPermissionActivity.onCreate` 按 `find_and_grant` 拼出「Find Alfa Antivirus, Cleaner and grant accessibility permission」。
  6. 系统无障碍列表项名 = `@string/app_name`（Alfa Antivirus, Cleaner），`android:description` 主动交代「You will have to accept Android system warinings」——预先教用户忽略系统警告。
  7. 用户返回仍未启用 → `onResume` 再次走 `Y()`/`c0()` **循环重弹**（无冷却、无"不再提示"）。
  8. 获权后 `r=2` → 检查 `canRequestPackageInstalls()` → 跳 `MANAGE_UNKNOWN_APP_SOURCES` 进入安装下一环。
- 同一框架还用于通知使用权（`P()`）与用量访问（`R()`），说明无障碍只是多级高权限链的一环。
- **诱饵与能力不对等**：宣称"深度清理隐藏垃圾 / 休眠耗电应用 / 加速 50%"，实际配置为 `typeAllMask` + `canRetrieveWindowContent=true` + `notificationTimeout=50`，可读取任意前台界面节点。
- 未见全屏高仿系统无障碍页、GIF 引导、`isAccessibilityTool` 伪造、`ACTION_APPLICATION_DETAILS_SETTINGS` 或 Android 13 受限设置分步教学。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导全链路（云控门控判定、原生引导弹窗、ACTION_ACCESSIBILITY_SETTINGS 跳转、压栈引导页、系统无障碍列表文案）均完整静态可见；仅远端下发的 SESSION 开关值（atsFull/status）被硬编码密钥 AES 加密存储，具体取值需运行期确认，但不影响流程判定。",
  "summary_one_liner": "以清理杀毒加速为诱饵，按云端加密配置在每次回前台弹原生引导弹窗，点确认即跳系统无障碍设置并压入引导页，未开启则返回后循环重弹，服务名与桌面名一致且描述教用户忽略系统警告。",
  "disguise_identity": {
    "app_display_name": "Alfa Antivirus, Cleaner",
    "claimed_brand_or_persona": "Alfa Antivirus, Cleaner（描述文案中另自称 Super Cleaner / Clean master）",
    "a11y_service_label": "Alfa Antivirus, Cleaner",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍描述中连续空行 \" \\n \\n\" 分隔并把关键警告语放在末尾；多处故意错拼（Accessiblility / warinings / orther / tollowing）弱化识别；描述内自称 Super Cleaner 与 Clean master，与桌面名 Alfa Antivirus, Cleaner 不一致；代码整体混淆为 d.j.a.a.* 短名；会话配置以硬编码密钥 AES 加密存储。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.pagnotto28.sellsourcecode.alpha.screen.main.MainActivity（SplashActivity 之后的主界面）",
      "trigger_event": "onResume() → Y()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（此步仅读取本地/云端配置）",
      "shown_text_zh": "无界面呈现，仅解密 SESSION 配置并调度 7 秒后复核",
      "user_action_requested": "无",
      "code_anchor": "MainActivity.onResume → d.j.a.a.j.s.Y（AES 密钥 IIBCgKCntNatAu9qo1QgM8FH7）"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "d.j.a.a.j.s#c0 门控方法",
      "trigger_event": "Y() 内 checkResult 判定；或用户点击首页/工具页功能入口（MainActivity$a.onClick → f0）",
      "ui_carrier": "不可静态还原（开关值来自远端 AES 加密 JSON）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "若云端 JSON 含 atsFull 且 ForceStopAccessibility 未启用，则进入无障碍索取分支（h0(\"waitA11\")）",
      "user_action_requested": "无",
      "code_anchor": "d.j.a.a.j.s#c0"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.pagnotto28.sellsourcecode.alpha.dialog.DialogAskPermission（layout 2131558481）",
      "trigger_event": "c0() 判定未授权 → f0() → DialogAskPermission.N0(\"android.settings.ACCESSIBILITY_SETTINGS\", ...)",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Grant permission to use accessibility service",
      "shown_text_zh": "授予使用无障碍服务的权限",
      "user_action_requested": "点击确认按钮（Grant Permission）或取消；对话框 setCancelable(true)、setCanceledOnTouchOutside(true)，可跳过",
      "code_anchor": "DialogAskPermission#O0（string 2131951653 = accessibility_setting_permission）/ #k0 / #click"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "DialogAskPermission#click 回调 → d.j.a.a.j.m#a",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（由系统渲染）",
      "shown_text_zh": "跳转至系统无障碍服务列表",
      "user_action_requested": "在系统列表中手动找到并开启服务开关",
      "code_anchor": "d.j.a.a.j.m#a：startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.pagnotto28.sellsourcecode.alpha.screen.guildPermission.GuildPermissionActivity（紧接 startActivity 压栈）",
      "trigger_event": "d.j.a.a.j.m#a 同方法内 GuildPermissionActivity.i0(ctx, \"android.settings.ACCESSIBILITY_SETTINGS\") → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Find Alfa Antivirus, Cleaner and grant accessibility permission",
      "shown_text_zh": "找到「Alfa Antivirus, Cleaner」并授予无障碍权限",
      "user_action_requested": "按页面指示在系统列表中找到同名条目并开启；页面含返回/关闭按钮（findViewById 2131362082、2131362159 点击关闭）",
      "code_anchor": "GuildPermissionActivity#onCreate（getString(2131951809=find_and_grant, app_name, 2131951651=accessibility_permission)）"
    },
    {
      "step": 6,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍列表中的 ForceStopAccessibility 条目",
      "trigger_event": "用户到达系统无障碍服务列表",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Tap on top right use to Accessiblility service. \\n \\nThis will allow Super Cleaner to: \\n \\n- Deep clean hidden junk \\n- Hibernate draining apps \\n \\nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "shown_text_zh": "点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾；休眠耗电应用。启用无障碍服务时你需要接受 Android 系统的警告。Clean master 不会将这些用于此处列出的以外的任何其他目的。",
      "user_action_requested": "忽略系统弹出的无障碍高危警告并确认开启",
      "code_anchor": "res/xml/accessibility_service_config.xml + res/values/strings.xml#accessibility_service_description；Manifest service android:label=@string/app_name"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onResume → Y() → c0() → f0()（再次 DialogAskPermission）",
      "trigger_event": "用户从系统设置按返回键回到应用（onResume）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Grant permission to use accessibility service",
      "shown_text_zh": "再次弹出同一授权弹窗（无冷却、无「不再提示」选项）",
      "user_action_requested": "再次要求授权；可再次取消，但每次回前台都会重弹",
      "code_anchor": "d.j.a.a.j.s#Y → #c0 → #f0"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "系统设置 android.settings.MANAGE_UNKNOWN_APP_SOURCES（应用自身包名）",
      "trigger_event": "Y() 中 V(false) 为真且 ForceStopAccessibility 已启用 → r=2 → canRequestPackageInstalls() 为假",
      "ui_carrier": "系统无障碍页（后续为系统安装来源页）",
      "shown_text_verbatim": "无（h0(\"waitSource\"); S(\"atsSource\")）",
      "shown_text_zh": "获权后转入未知来源安装授权，为后续投放安装包做准备",
      "user_action_requested": "允许本应用安装未知应用",
      "code_anchor": "d.j.a.a.j.s#Y（Intent android.settings.MANAGE_UNKNOWN_APP_SOURCES）"
    }
  ],
  "text_presentation_locations": [
    "原生 Dialog（DialogAskPermission，layout 2131558481，dimAmount 0.7）正文：Grant permission to use accessibility service（string accessibility_setting_permission）",
    "原生 Activity（GuildPermissionActivity，layout 2131558441）正文：Find Alfa Antivirus, Cleaner and grant accessibility permission（string find_and_grant 格式化 app_name + accessibility_permission）",
    "系统无障碍服务列表条目名：@string/app_name = Alfa Antivirus, Cleaner（与桌面图标名完全一致）",
    "系统无障碍服务条目描述：@string/accessibility_service_description（含 Super Cleaner / Clean master 话术与「接受系统警告」提示）",
    "系统无障碍条目摘要键：string accessibility_permission = accessibility permission",
    "清理/加速类功能页话术：string content_permission_1 = Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Grant permission to use accessibility service",
      "text_zh": "授予使用无障碍服务的权限",
      "source_location": "res/values/strings.xml key=accessibility_setting_permission（DialogAskPermission#O0 引用 2131951653）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Find %s and grant %s",
      "text_zh": "找到 %s 并授予 %s（实际渲染为 Find Alfa Antivirus, Cleaner and grant accessibility permission）",
      "source_location": "res/values/strings.xml key=find_and_grant（GuildPermissionActivity#onCreate 引用 2131951809）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Tap on top right use to Accessiblility service. \\n \\nThis will allow Super Cleaner to: \\n \\n- Deep clean hidden junk \\n- Hibernate draining apps \\n \\nYou will have to accept Android system warinings when enabling Accessibility service. Clean master will not use these for any orther purpose than listed here.",
      "text_zh": "点击右上角以使用无障碍服务。这将允许 Super Cleaner：深度清理隐藏垃圾；休眠耗电应用。启用无障碍服务时你需要接受 Android 系统的警告。Clean master 不会将其用于此处所列以外的任何其他目的。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml 引用）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Please grant Accessibility to close tollowing auto start apps. Acceleration could be increased by 50%",
      "text_zh": "请授予无障碍权限以关闭以下自启动应用，加速效果可提升 50%。",
      "source_location": "res/values/strings.xml key=content_permission_1",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "accessibility permission",
      "text_zh": "无障碍权限",
      "source_location": "res/values/strings.xml key=accessibility_permission",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable now",
      "text_zh": "立即启用",
      "source_location": "res/values/strings.xml key=Notificationbarcleanup_RightNow",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "用户取消弹窗或从系统设置按返回后，MainActivity.onResume 再次执行 Y() → c0()，只要远端 atsFull 仍在且 ForceStopAccessibility 未启用即再次调用 f0() 弹出同一引导弹窗；无冷却计时、无「不再提示」开关，形成每次回前台必弹的循环。",
    "overlay_or_fake_settings": "无全屏悬浮窗或高仿系统无障碍开关页；采用原生 Dialog（dimAmount 0.7 半透明背景）+ 在 startActivity(ACCESSIBILITY_SETTINGS) 同一方法内压栈 GuildPermissionActivity 引导页的方式，让引导页覆盖在系统设置页之上。",
    "restricted_settings_13plus_coaching": "无（未使用 ACTION_APPLICATION_DETAILS_SETTINGS，无 Android 13 受限设置分步教学，targetSdk=30）",
    "post_grant_anti_removal": "有间接对抗：Y() 在检测到无障碍已启用后立即推进 r=2 并跳转 MANAGE_UNKNOWN_APP_SOURCES 申请安装未知应用权限（前置投放环节）；无障碍服务运行于 :BackgroundService 独立进程并配合 LockRestarterBroadcastReceiver 等常驻机制，但未见监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的直接代码。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动进入 MainActivity 后首次 onResume 完成 SESSION 解密并触发 f0() 的瞬间；以及 DialogAskPermission 确认按钮回调 d.j.a.a.j.m#a 执行 startActivity(ACCESSIBILITY_SETTINGS) 后 300–800ms（引导页压栈完成、系统设置页被覆盖）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "com.pagnotto28.sellsourcecode.alpha.dialog.DialogAskPermission，半透明遮罩（dimAmount 0.7），标题含应用名、正文含 Grant permission 与 Grant Permission 按钮",
        "why_most_useful": "证明索要无障碍由应用主动发起、文案为纯功能收益诱导而非系统原生提示",
        "observable_utg_signals": ["对话框包名归属为 com.pagnotto28.sellsourcecode.alpha", "正文文本 Grant permission to use accessibility service", "按钮文案 Grant Permission 与取消按钮并存"]
      },
      {
        "page_role": "设置页后压栈遮罩页（引导教学页）",
        "page_identifier": "com.pagnotto28.sellsourcecode.alpha.screen.guildPermission.GuildPermissionActivity，叠于系统设置之上",
        "why_most_useful": "区分「仅跳系统设置」与「跳转后强制叠加指引」，是诱导链完整性的关键判据",
        "observable_utg_signals": ["Activity 归属为应用包名而非 com.android.settings", "文本 Find Alfa Antivirus, Cleaner and grant accessibility permission", "页面出现于系统设置页启动之后"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍列表中的 Alfa Antivirus, Cleaner 条目",
        "why_most_useful": "核验服务标签与桌面名一致（身份不可区分）及描述中教用户接受系统警告",
        "observable_utg_signals": ["条目名 Alfa Antivirus, Cleaner", "描述文本含 accept Android system warinings", "开关状态由关变为开的时间点"]
      },
      {
        "page_role": "拒权返回后的重弹页",
        "page_identifier": "从系统设置返回 MainActivity 后再次出现的 DialogAskPermission",
        "why_most_useful": "证明存在无冷却的循环索要，构成强制施压",
        "observable_utg_signals": ["同一对话框在返回后 1–2 秒内重复出现", "连续出现次数", "无「不再提示」选项"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导文案全部为可提取文本，无图片诱饵；但两点需注意：一是是否弹窗由远端下发并经 AES 加密存储的 SESSION（atsFull/status）决定，离线或未取到配置时可能不触发，静态无法确定线上触发率；二是紧随其后的 MANAGE_UNKNOWN_APP_SOURCES 与安装动作属于下一阶段投放，本 UTG 观测仅覆盖无障碍索取阶段。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH"
  ],
  "code_anchors": [
    "com.pagnotto28.sellsourcecode.alpha.screen.main.MainActivity#onResume",
    "d.j.a.a.j.s#Y",
    "d.j.a.a.j.s#c0",
    "com.pagnotto28.sellsourcecode.alpha.dialog.DialogAskPermission#O0",
    "d.j.a.a.j.m#a",
    "com.pagnotto28.sellsourcecode.alpha.screen.guildPermission.GuildPermissionActivity#onCreate"
  ]
}
```

</details>
