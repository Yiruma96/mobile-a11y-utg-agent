# MB_162__a1416a250b｜Unattributed — T​⁠i‍‍k​T⁠‍​o⁠⁠⁠k​1‌⁠⁠8⁠​​+

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：137.9s

## 1. 一句话核心结论

- **核心申请方式**：该样本并无无障碍服务，也无可证实的无障碍诱导流程；其本质是伪装成 TikTok 的通用 APK 调试安装器/跨包启动器，仅在工具页提供一个用户主动点击的『打开无障碍设置』按钮，真实风险是身份伪装、未知来源安装能力与运行期解密的 SVLT Vault 载荷。
- **静态可见性说明**：Manifest、DEX、strings/layout 资源均完整静态可见，可确证无无障碍服务与无诱导弹窗链；但 assets/wel3txgv.zip 是 magic=SVLT 的 7.8MB 自定义加密 Vault 容器（非 ZIP），其内 upgrade-template/index.html 等模板与后续载荷需运行期解密（d2.d#d → g2.e.B(path)）才能还原，本次未获得其明文内容。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a1416a250bf7219f95961f484421dda844b5013b5561c4a40591489dcfcdd384` |
| 包名 / 年份 | `store.pandaac.task9d` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | TikTok18+（字符串中嵌入零宽字符：T​⁠i‍‍k​T⁠‍​o⁠⁠⁠k​1‌⁠⁠8⁠​​+） |
| 引导页宣称品牌/身份 | TikTok（短视频客户端） |
| 系统无障碍列表服务名 | 无（应用未声明任何 AccessibilityService，系统无障碍列表中不会出现本应用条目） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) app_name 逐字插入 U+200B/U+200C/U+200D/U+2060 等零宽字符，规避显示名精确匹配与人工核对；2) 约 50 个 activity-alias 使用 ShortcutAlias/QuickActionAlias/WidgetConfigAlias/SettingsAlias 等良性命名，真实指向 DebugInstallActivity、UnknownSourcesPermissionActivity 及各业务 Activity，隐藏真实入口；3) 声明约 60 个形如 permission.content.checkout.v8 的伪造自有权限，膨胀 Manifest 干扰静态研判；4) queries 声明与显示名同源的子包 net.tiktitoks18gh.iceforge；5) 载荷以自定义 SVLT 加密容器 assets/wel3txgv.zip 存放；6) 无伪造 isAccessibilityTool，也无无障碍服务描述。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_INSTALL_PACKAGES` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.shell.template.app.LaunchRouterActivity（MANIFEST 中 LAUNCHER 入口） | onCreate → v.j(this.x,0,new d2.d(this,null,1),3) 启动协程 | 原生Activity | **原文**：无（LaunchRouterActivity 仅 setContentView(2131427357)，无文案；若路由目标非安装分支则立即跳转并 finishAndRemoveTask）<br>**译注**：无引导文案，冷启动不弹任何对话框 | 无，用户无需任何操作 | `com.shell.template.app.LaunchRouterActivity.onCreate；d2.d#d case 1` |
| 2 | 业务功能触发 | com.shell.template.feature.debug.DebugInstallActivity（工具页） | 路由分发后 startActivity(DebugInstallActivity)；或经 activity-alias store.pandaac.task9d.service.recommend.ScannerAlias2024 进入 | 原生Activity | 选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。 | 用户可点『选择 APK』『安装所选 APK』『选择 Activity 启动』，以及工具区的『打开无障碍设置』；页面为普通工具界面，可自由返回，无强制或取消限制 | `DebugInstallActivity.onCreate；res/values/strings.xml debug_install_subtitle` |
| 3 | 跳受限设置 | com.shell.template.platform.installer.UnknownSourcesPermissionActivity → 系统『安装未知应用』页 | 点击『安装所选 APK』后 z1.h.b() 判定无安装权限 → 该 Activity onCreate 调 c() 发 startActivityForResult(new Intent("android.settings.MANAGE_UNKNOWN_APP_SOURCES"), 6101) | 系统无障碍页（此处为系统未知来源安装设置页） | **原文**：请允许此应用安装未知来源应用 / 无法打开未知来源安装权限页面<br>**译注**：请允许此应用安装未知来源应用；异常时记录日志『无法打开未知来源安装权限页面』并返回失败结果 | 用户在系统页为本应用打开『允许安装未知应用』开关；失败或返回时 Activity setResult(1) 并 finish，不重复拉起 | `com.shell.template.platform.installer.UnknownSourcesPermissionActivity#c；c2.k#onClick case 1/2` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS | 用户在工具页点击无障碍按钮（id 2131230735）→ c2.k#onClick case 4 → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：打开无障碍设置 / 无法打开无障碍设置<br>**译注**：按钮文字为『打开无障碍设置』；跳转异常时 Toast『无法打开无障碍设置』 | 纯跳转，无任何引导说明；由于本应用未注册无障碍服务，系统列表中不存在本应用条目，用户无可开启目标，跳转属空操作。无自动返回、无 onResume 重跳、无遮罩 | `c2.k#onClick case 4；res/values/strings.xml debug_install_accessibility_settings / debug_install_accessibility_open_failed` |
| 5 | 获权后动作 | 无（不存在无障碍获权分支） | 无（DebugInstallActivity.onResume 仅调用 this.z.c() 与 x() 刷新 UI 状态） | 不可静态还原 | 无 | 无 | `DebugInstallActivity#onResume` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- DebugInstallActivity 原生布局（setContentView 2131427356）内 TextView 副标题：『选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。』（strings.xml debug_install_subtitle）
- DebugInstallActivity 工具区 MaterialButton（id 2131230735）按钮文字：『打开无障碍设置』（strings.xml debug_install_accessibility_settings）
- DebugInstallActivity 状态横幅 TextView（id 2131230852 statusText）：『请允许此应用安装未知来源应用』『APK 已就绪，可安装或启动 Activity』等状态提示（strings.xml debug_install_permission_required / debug_install_ready）
- DebugInstallActivity 底部提示：『在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。』（strings.xml debug_install_hint）
- Activity 选择弹窗（e1.l MaterialAlertDialog，layout 2131427375）：标题为『%1$s · 共 %2$d 个，其中 %3$d 个可启动』，提示『可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。』
- Toast 提示（DebugInstallActivity.v(String)）：『无法打开无障碍设置』『启动失败：应用未安装、组件不存在或需要额外权限』『该 Activity 未导出，母包无法跨包启动』
- 系统设置页（外部，非应用渲染）：android.settings.MANAGE_UNKNOWN_APP_SOURCES（本应用安装未知应用权限）与 android.settings.ACCESSIBILITY_SETTINGS
- assets/wel3txgv.zip（SVLT 加密 Vault）内 upgrade-template/index.html 经 WebView 以 https://appassets.shelltemplate.internal/ 加载，模板明文当前不可静态读取

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| zh | 选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。 | 选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。 | `res/values/strings.xml: debug_install_subtitle` | 良性透明说明 |
| zh | 打开无障碍设置 | 打开无障碍设置 | `res/values/strings.xml: debug_install_accessibility_settings（按钮 id 2131230735，c2.k#onClick case 4）` | 良性透明说明 |
| zh | 无法打开无障碍设置 | 无法打开无障碍设置 | `res/values/strings.xml: debug_install_accessibility_open_failed（DebugInstallActivity.v）` | 良性透明说明 |
| zh | 请允许此应用安装未知来源应用 | 请允许此应用安装未知来源应用 | `res/values/strings.xml: debug_install_permission_required` | 受限设置分步教学 |
| zh | 在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。 | 在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。 | `res/values/strings.xml: debug_install_hint` | 受限设置分步教学 |
| zh | 可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。 | 可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。 | `res/values/strings.xml: debug_install_activity_picker_hint` | 未知 |
| zh | 启动失败：应用未安装、组件不存在或需要额外权限 | 启动失败：应用未安装、组件不存在或需要额外权限 | `res/values/strings.xml: debug_install_activity_launch_failed` | 未知 |
| zh | 该 Activity 未导出，母包无法跨包启动 | 该 Activity 未导出，母包无法跨包启动 | `res/values/strings.xml: debug_install_activity_not_exported` | 未知 |
| en | T​⁠i‍‍k​T⁠‍​o⁠⁠⁠k​1‌⁠⁠8⁠​​+ | TikTok18+（字间夹入大量零宽不可见字符） | `res/values/strings.xml: app_name` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无拒绝循环。无障碍跳转由用户主动点按钮触发，跳转后无 onResume 检测重跳、无定时器拉起；DebugInstallActivity.onResume 仅执行 this.z.c() 与 UI 状态刷新。未知来源安装页返回后仅 setResult(1)+finish 一次，不重复拉起。
- **遮罩叠层 / 高仿系统设置页**：无。全包无悬浮窗/叠层/仿系统页实现，无 SYSTEM_ALERT_WINDOW 权限声明，无 WindowManager.addView 引导遮罩；跳转即为真实系统设置页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，无『右上角菜单 → 允许受限设置』教学，无 Session Installer（PackageInstaller.Session）绕过实现。
- **获权后即时行为与防撤权机制**：无。应用未注册无障碍服务，不存在监听设置页、performGlobalAction(GLOBAL_ACTION_BACK/HOME) 阻止撤权的实现。
- **良性降级 / 替代方案**：无（不适用）。应用无无障碍依赖功能，按钮跳转为纯附加工具项，跳转失败仅 Toast『无法打开无障碍设置』，不影响主流程。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本不具备诱导式无障碍触发，纯 UTG 侧最有效的挂载点是：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 且发起方为 DebugInstallActivity（按钮点击 c2.k#onClick case 4）；以及监测到 android.settings.MANAGE_UNKNOWN_APP_SOURCES 跳转（UnknownSourcesPermissionActivity.c）。冷启动阶段无 UTG 捕获价值（无弹窗、无叠层）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两类盲区：1) assets/wel3txgv.zip 为 magic=SVLT 的 7.8MB 自定义加密 Vault，其 upgrade-template/index.html 等模板明文需运行期解密后才注入 WebView（https://appassets.shelltemplate.internal/），本次静态未还原，该 WebView 页面的实际文案与后续载荷投放不可静态判定；2) 样本为『调试安装器 + 跨包启动器』形态的一阶段 Dropper，可解析并跨包拉起任意外部 APK 内 Activity（含 queries 声明的 net.tiktitoks18gh.iceforge），真实恶意行为可能完全位于其安装/拉起的二阶段包中，本包运行期 UTG 只能看到外壳工具页。另注：本样本无静态加壳，但静态可见性仍不完整，原因是 Vault 加密而非加壳。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动路由页（确认是否存在诱导弹窗）** | com.shell.template.app.LaunchRouterActivity 首个可见帧，随后立即切换为 DebugInstallActivity 工具页 | 排除『冷启动即弹不可取消引导』的常见诱导模式；此处无弹窗即可直接否定 TRIG_COLD_START_BLOCK | 冷启动 0 秒内是否存在 Dialog 或悬浮窗节点；是否存在 800ms 级延时压栈的第二页面；界面可见文本是否仅为工具类按钮 |
| **调试安装器工具页（无障碍按钮所在页）** | DebugInstallActivity，含『选择 APK』『安装所选 APK』『选择 Activity 启动』『打开无障碍设置』四个按钮 | 这是唯一无障碍跳转入口，可确认其是否被包装成不可取消弹窗、是否伴随恐吓/安全文案，从而区分『工具按钮』与『诱导』 | 无障碍按钮是否为独立工具项而非全屏弹窗主按钮；页面是否存在关闭/返回入口；副标题文案是否含假更新、故障恐吓或假反诈措辞 |
| **系统无障碍服务列表项（验证应用是否出现在列表中）** | android.settings.ACCESSIBILITY_SETTINGS 列表中检索 store.pandaac.task9d | 决定性反证：应用未声明 AccessibilityService，列表中应无本应用条目，可当场否定『诱导开启无障碍』命题 | 列表中不存在 store.pandaac.task9d 或 TikTok18+ 条目；无本应用对应的 service 名称与 description 文本 |
| **系统未知来源安装授权页（真实受限设置引导）** | android.settings.MANAGE_UNKNOWN_APP_SOURCES?package:store.pandaac.task9d | 确认样本真正索取的敏感能力是安装未知应用而非无障碍，是二阶段载荷落地的前置条件 | 系统页顶部包名是否为 store.pandaac.task9d；返回后是否立即触发 APK 安装或 WebView 远程加载 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `c2.k#onClick（case 4：startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))）`
- `com.shell.template.feature.debug.DebugInstallActivity#onCreate（工具页布局 2131427356，无障碍按钮 id 2131230735）`
- `com.shell.template.platform.installer.UnknownSourcesPermissionActivity#c（android.settings.MANAGE_UNKNOWN_APP_SOURCES）`
- `com.shell.template.app.LaunchRouterActivity#onCreate + d2.d#d（路由分发至 DebugInstallActivity / Vault 读取 upgrade-template/index.html）`
- `res/values/strings.xml（app_name 零宽字符伪装；debug_install_accessibility_settings 等文案）`
- `assets/wel3txgv.zip（magic SVLT 自定义加密 Vault，7,826,380 字节）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**核心判断：本样本不存在无障碍权限诱导链。** 全包（含 Manifest、DEX、资源）中：

- **无任何 AccessibilityService**：没有 `BIND_ACCESSIBILITY_SERVICE` 服务、没有 `accessibilityservice` 元数据 XML、没有 `android:description`，代码中也没有 `isAccessibilityTool`。所谓“无障碍类/标签/描述”全部为空，这与预筛结果一致。
- **仅一处无障碍跳转，且是工具按钮**：`android.settings.ACCESSIBILITY_SETTINGS` 只出现在 [c2.k.onClick()](<resource-unit:#1.dex1 code:c2.k#onClick>) 的 `case 4`，绑定 [DebugInstallActivity](<resource-unit:#1.dex1 code:com.shell.template.feature.debug.DebugInstallActivity#onCreate>) 布局里的一个普通 MaterialButton（id `2131230735`），点击即 `startActivity`，失败时仅 Toast「无法打开无障碍设置」。无弹窗包裹、无 onResume 重跳、无遮罩叠层、无拒权循环。
- **真实主体是“调试安装器 + 跨包启动器”**：选择本地 APK → 申请未知来源安装（[UnknownSourcesPermissionActivity.c()](<resource-unit:#1.dex1 code:com.shell.template.platform.installer.UnknownSourcesPermissionActivity#c>) 跳 `MANAGE_UNKNOWN_APP_SOURCES`）→ 解析包内 Activity 列表后跨包 `startActivity`。字符串 `debug_install_subtitle` 明示「…或跳转系统无障碍设置」，属于透明工具说明。
- **身份伪装成立**：[app_name](<resource-unit:#1 file:res/values/strings.xml#L24>) 为 `TikTok18+`，字符间插入大量零宽/不可见字符（ZWSP/ZWJ/WORD JOINER），对抗字符串匹配与人工核对；Manifest `<queries>` 还声明了同名子包 `net.tiktitoks18gh.iceforge`。
- **加密 Vault 载荷（静态不可见）**：`assets/wel3txgv.zip` 并非 ZIP，magic 为 `53 56 4C 54`（"SVLT"）、7.8MB 自定义容器；[d2.d#d](<resource-unit:#1.dex1 code:d2.d#d>) 通过 `g2.e` 从 Vault 读取 `upgrade-template/index.html` 注入 CSP 后经 WebView 加载 `https://appassets.shelltemplate.internal/upgrade-template/index.html`。其明文载荷本次未还原。
- **启动路径**：`LaunchRouterActivity.onCreate` → `d2.d#d` 协程，若路由目标非安装分支则 `startActivity(DebugInstallActivity)` 并 `finishAndRemoveTask()`。冷启动不会弹任何诱导弹窗。
- **大量 activity-alias 伪装**：Manifest 中约 50 个 `ShortcutAlias*` / `QuickActionAlias*` / `SettingsAlias*` 等良性命名别名指向真实业务与安装器 Activity，其中 `store.pandaac.task9d.service.recommend.ScannerAlias2024` → `DebugInstallActivity`、`store.pandaac.task9d.biz.growth.MemberPortalAlias762` → `UnknownSourcesPermissionActivity`。

因此针对本轮“无障碍诱导 UTG 视角”的问题：**静态不可证实任何诱导式引导**，唯一入口是用户主动点击的按钮；样本的真实风险在于身份伪装 + 二阶段加密载荷 + 未知来源安装能力。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、DEX、strings/layout 资源均完整静态可见，可确证无无障碍服务与无诱导弹窗链；但 assets/wel3txgv.zip 是 magic=SVLT 的 7.8MB 自定义加密 Vault 容器（非 ZIP），其内 upgrade-template/index.html 等模板与后续载荷需运行期解密（d2.d#d → g2.e.B(path)）才能还原，本次未获得其明文内容。",
  "summary_one_liner": "该样本并无无障碍服务，也无可证实的无障碍诱导流程；其本质是伪装成 TikTok 的通用 APK 调试安装器/跨包启动器，仅在工具页提供一个用户主动点击的『打开无障碍设置』按钮，真实风险是身份伪装、未知来源安装能力与运行期解密的 SVLT Vault 载荷。",
  "disguise_identity": {
    "app_display_name": "TikTok18+（字符串中嵌入零宽字符：T​⁠i‍‍k​T⁠‍​o⁠⁠⁠k​1‌⁠⁠8⁠​​+）",
    "claimed_brand_or_persona": "TikTok（短视频客户端）",
    "a11y_service_label": "无（应用未声明任何 AccessibilityService，系统无障碍列表中不会出现本应用条目）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) app_name 逐字插入 U+200B/U+200C/U+200D/U+2060 等零宽字符，规避显示名精确匹配与人工核对；2) 约 50 个 activity-alias 使用 ShortcutAlias/QuickActionAlias/WidgetConfigAlias/SettingsAlias 等良性命名，真实指向 DebugInstallActivity、UnknownSourcesPermissionActivity 及各业务 Activity，隐藏真实入口；3) 声明约 60 个形如 permission.content.checkout.v8 的伪造自有权限，膨胀 Manifest 干扰静态研判；4) queries 声明与显示名同源的子包 net.tiktitoks18gh.iceforge；5) 载荷以自定义 SVLT 加密容器 assets/wel3txgv.zip 存放；6) 无伪造 isAccessibilityTool，也无无障碍服务描述。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.shell.template.app.LaunchRouterActivity（MANIFEST 中 LAUNCHER 入口）",
      "trigger_event": "onCreate → v.j(this.x,0,new d2.d(this,null,1),3) 启动协程",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（LaunchRouterActivity 仅 setContentView(2131427357)，无文案；若路由目标非安装分支则立即跳转并 finishAndRemoveTask）",
      "shown_text_zh": "无引导文案，冷启动不弹任何对话框",
      "user_action_requested": "无，用户无需任何操作",
      "code_anchor": "com.shell.template.app.LaunchRouterActivity.onCreate；d2.d#d case 1"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.shell.template.feature.debug.DebugInstallActivity（工具页）",
      "trigger_event": "路由分发后 startActivity(DebugInstallActivity)；或经 activity-alias store.pandaac.task9d.service.recommend.ScannerAlias2024 进入",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。",
      "shown_text_zh": "选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。",
      "user_action_requested": "用户可点『选择 APK』『安装所选 APK』『选择 Activity 启动』，以及工具区的『打开无障碍设置』；页面为普通工具界面，可自由返回，无强制或取消限制",
      "code_anchor": "DebugInstallActivity.onCreate；res/values/strings.xml debug_install_subtitle"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "com.shell.template.platform.installer.UnknownSourcesPermissionActivity → 系统『安装未知应用』页",
      "trigger_event": "点击『安装所选 APK』后 z1.h.b() 判定无安装权限 → 该 Activity onCreate 调 c() 发 startActivityForResult(new Intent(\"android.settings.MANAGE_UNKNOWN_APP_SOURCES\"), 6101)",
      "ui_carrier": "系统无障碍页（此处为系统未知来源安装设置页）",
      "shown_text_verbatim": "请允许此应用安装未知来源应用 / 无法打开未知来源安装权限页面",
      "shown_text_zh": "请允许此应用安装未知来源应用；异常时记录日志『无法打开未知来源安装权限页面』并返回失败结果",
      "user_action_requested": "用户在系统页为本应用打开『允许安装未知应用』开关；失败或返回时 Activity setResult(1) 并 finish，不重复拉起",
      "code_anchor": "com.shell.template.platform.installer.UnknownSourcesPermissionActivity#c；c2.k#onClick case 1/2"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "用户在工具页点击无障碍按钮（id 2131230735）→ c2.k#onClick case 4 → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "打开无障碍设置 / 无法打开无障碍设置",
      "shown_text_zh": "按钮文字为『打开无障碍设置』；跳转异常时 Toast『无法打开无障碍设置』",
      "user_action_requested": "纯跳转，无任何引导说明；由于本应用未注册无障碍服务，系统列表中不存在本应用条目，用户无可开启目标，跳转属空操作。无自动返回、无 onResume 重跳、无遮罩",
      "code_anchor": "c2.k#onClick case 4；res/values/strings.xml debug_install_accessibility_settings / debug_install_accessibility_open_failed"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "无（不存在无障碍获权分支）",
      "trigger_event": "无（DebugInstallActivity.onResume 仅调用 this.z.c() 与 x() 刷新 UI 状态）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无获权后动作；本应用无无障碍服务，无法感知或响应无障碍授权状态",
      "user_action_requested": "无",
      "code_anchor": "DebugInstallActivity#onResume"
    }
  ],
  "text_presentation_locations": [
    "DebugInstallActivity 原生布局（setContentView 2131427356）内 TextView 副标题：『选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。』（strings.xml debug_install_subtitle）",
    "DebugInstallActivity 工具区 MaterialButton（id 2131230735）按钮文字：『打开无障碍设置』（strings.xml debug_install_accessibility_settings）",
    "DebugInstallActivity 状态横幅 TextView（id 2131230852 statusText）：『请允许此应用安装未知来源应用』『APK 已就绪，可安装或启动 Activity』等状态提示（strings.xml debug_install_permission_required / debug_install_ready）",
    "DebugInstallActivity 底部提示：『在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。』（strings.xml debug_install_hint）",
    "Activity 选择弹窗（e1.l MaterialAlertDialog，layout 2131427375）：标题为『%1$s · 共 %2$d 个，其中 %3$d 个可启动』，提示『可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。』",
    "Toast 提示（DebugInstallActivity.v(String)）：『无法打开无障碍设置』『启动失败：应用未安装、组件不存在或需要额外权限』『该 Activity 未导出，母包无法跨包启动』",
    "系统设置页（外部，非应用渲染）：android.settings.MANAGE_UNKNOWN_APP_SOURCES（本应用安装未知应用权限）与 android.settings.ACCESSIBILITY_SETTINGS",
    "assets/wel3txgv.zip（SVLT 加密 Vault）内 upgrade-template/index.html 经 WebView 以 https://appassets.shelltemplate.internal/ 加载，模板明文当前不可静态读取"
  ],
  "verbatim_texts": [
    {
      "lang": "zh",
      "text_verbatim": "选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。",
      "text_zh": "选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。",
      "source_location": "res/values/strings.xml: debug_install_subtitle",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "打开无障碍设置",
      "text_zh": "打开无障碍设置",
      "source_location": "res/values/strings.xml: debug_install_accessibility_settings（按钮 id 2131230735，c2.k#onClick case 4）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "无法打开无障碍设置",
      "text_zh": "无法打开无障碍设置",
      "source_location": "res/values/strings.xml: debug_install_accessibility_open_failed（DebugInstallActivity.v）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "请允许此应用安装未知来源应用",
      "text_zh": "请允许此应用安装未知来源应用",
      "source_location": "res/values/strings.xml: debug_install_permission_required",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。",
      "text_zh": "在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。",
      "source_location": "res/values/strings.xml: debug_install_hint",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。",
      "text_zh": "可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。",
      "source_location": "res/values/strings.xml: debug_install_activity_picker_hint",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "启动失败：应用未安装、组件不存在或需要额外权限",
      "text_zh": "启动失败：应用未安装、组件不存在或需要额外权限",
      "source_location": "res/values/strings.xml: debug_install_activity_launch_failed",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "该 Activity 未导出，母包无法跨包启动",
      "text_zh": "该 Activity 未导出，母包无法跨包启动",
      "source_location": "res/values/strings.xml: debug_install_activity_not_exported",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "T​⁠i‍‍k​T⁠‍​o⁠⁠⁠k​1‌⁠⁠8⁠​​+",
      "text_zh": "TikTok18+（字间夹入大量零宽不可见字符）",
      "source_location": "res/values/strings.xml: app_name",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无拒绝循环。无障碍跳转由用户主动点按钮触发，跳转后无 onResume 检测重跳、无定时器拉起；DebugInstallActivity.onResume 仅执行 this.z.c() 与 UI 状态刷新。未知来源安装页返回后仅 setResult(1)+finish 一次，不重复拉起。",
    "overlay_or_fake_settings": "无。全包无悬浮窗/叠层/仿系统页实现，无 SYSTEM_ALERT_WINDOW 权限声明，无 WindowManager.addView 引导遮罩；跳转即为真实系统设置页。",
    "restricted_settings_13plus_coaching": "无。未出现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，无『右上角菜单 → 允许受限设置』教学，无 Session Installer（PackageInstaller.Session）绕过实现。",
    "post_grant_anti_removal": "无。应用未注册无障碍服务，不存在监听设置页、performGlobalAction(GLOBAL_ACTION_BACK/HOME) 阻止撤权的实现。",
    "benign_graceful_degradation": "无（不适用）。应用无无障碍依赖功能，按钮跳转为纯附加工具项，跳转失败仅 Toast『无法打开无障碍设置』，不影响主流程。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本不具备诱导式无障碍触发，纯 UTG 侧最有效的挂载点是：监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 且发起方为 DebugInstallActivity（按钮点击 c2.k#onClick case 4）；以及监测到 android.settings.MANAGE_UNKNOWN_APP_SOURCES 跳转（UnknownSourcesPermissionActivity.c）。冷启动阶段无 UTG 捕获价值（无弹窗、无叠层）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动路由页（确认是否存在诱导弹窗）",
        "page_identifier": "com.shell.template.app.LaunchRouterActivity 首个可见帧，随后立即切换为 DebugInstallActivity 工具页",
        "why_most_useful": "排除『冷启动即弹不可取消引导』的常见诱导模式；此处无弹窗即可直接否定 TRIG_COLD_START_BLOCK",
        "observable_utg_signals": ["冷启动 0 秒内是否存在 Dialog 或悬浮窗节点", "是否存在 800ms 级延时压栈的第二页面", "界面可见文本是否仅为工具类按钮"]
      },
      {
        "page_role": "调试安装器工具页（无障碍按钮所在页）",
        "page_identifier": "DebugInstallActivity，含『选择 APK』『安装所选 APK』『选择 Activity 启动』『打开无障碍设置』四个按钮",
        "why_most_useful": "这是唯一无障碍跳转入口，可确认其是否被包装成不可取消弹窗、是否伴随恐吓/安全文案，从而区分『工具按钮』与『诱导』",
        "observable_utg_signals": ["无障碍按钮是否为独立工具项而非全屏弹窗主按钮", "页面是否存在关闭/返回入口", "副标题文案是否含假更新、故障恐吓或假反诈措辞"]
      },
      {
        "page_role": "系统无障碍服务列表项（验证应用是否出现在列表中）",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 列表中检索 store.pandaac.task9d",
        "why_most_useful": "决定性反证：应用未声明 AccessibilityService，列表中应无本应用条目，可当场否定『诱导开启无障碍』命题",
        "observable_utg_signals": ["列表中不存在 store.pandaac.task9d 或 TikTok18+ 条目", "无本应用对应的 service 名称与 description 文本"]
      },
      {
        "page_role": "系统未知来源安装授权页（真实受限设置引导）",
        "page_identifier": "android.settings.MANAGE_UNKNOWN_APP_SOURCES?package:store.pandaac.task9d",
        "why_most_useful": "确认样本真正索取的敏感能力是安装未知应用而非无障碍，是二阶段载荷落地的前置条件",
        "observable_utg_signals": ["系统页顶部包名是否为 store.pandaac.task9d", "返回后是否立即触发 APK 安装或 WebView 远程加载"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两类盲区：1) assets/wel3txgv.zip 为 magic=SVLT 的 7.8MB 自定义加密 Vault，其 upgrade-template/index.html 等模板明文需运行期解密后才注入 WebView（https://appassets.shelltemplate.internal/），本次静态未还原，该 WebView 页面的实际文案与后续载荷投放不可静态判定；2) 样本为『调试安装器 + 跨包启动器』形态的一阶段 Dropper，可解析并跨包拉起任意外部 APK 内 Activity（含 queries 声明的 net.tiktitoks18gh.iceforge），真实恶意行为可能完全位于其安装/拉起的二阶段包中，本包运行期 UTG 只能看到外壳工具页。另注：本样本无静态加壳，但静态可见性仍不完整，原因是 Vault 加密而非加壳。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION"
  ],
  "code_anchors": [
    "c2.k#onClick（case 4：startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))）",
    "com.shell.template.feature.debug.DebugInstallActivity#onCreate（工具页布局 2131427356，无障碍按钮 id 2131230735）",
    "com.shell.template.platform.installer.UnknownSourcesPermissionActivity#c（android.settings.MANAGE_UNKNOWN_APP_SOURCES）",
    "com.shell.template.app.LaunchRouterActivity#onCreate + d2.d#d（路由分发至 DebugInstallActivity / Vault 读取 upgrade-template/index.html）",
    "res/values/strings.xml（app_name 零宽字符伪装；debug_install_accessibility_settings 等文案）",
    "assets/wel3txgv.zip（magic SVLT 自定义加密 Vault，7,826,380 字节）"
  ]
}
```

</details>
