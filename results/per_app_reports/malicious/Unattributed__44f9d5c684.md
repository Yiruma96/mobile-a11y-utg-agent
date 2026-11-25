# MB_163__44f9d5c684｜Unattributed — D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：164.1s

## 1. 一句话核心结论

- **核心申请方式**：该样本不含任何无障碍服务，也无弹窗/遮罩/教学页诱导，冷启动即路由到通用壳模板的「安装调试」工具面板，其中仅有一个需用户主动点击的按钮直接跳转 android.settings.ACCESSIBILITY_SETTINGS，真实载荷藏于加密的 assets/f80at32d.zip 二阶段。
- **静态可见性说明**：外壳（com.shell.template）全部 Java/Kotlin 代码、Manifest、strings 资源完整静态可见；不可见部分为 assets/f80at32d.zip（文件头 53 56 4c 54，非 ZIP 魔数，自定义加密的二阶段母包载荷）、母包配置下发值（b0VarZ/b2.a），以及 UpgradeActivity 通过 loadUrl 呈现的 upgrade-template/index.html 模板内容（由加密载荷 g2.e 提供）。包内不存在无障碍服务类，因此无障碍相关行为在外壳层已完整可见，无遗漏。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `44f9d5c684fb6f34465cd7593709a37cadb57aaf41430b0d043fa593e4faacab` |
| 包名 / 年份 | `video.lotus19.ridenovel31` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v |
| 引导页宣称品牌/身份 | Dixmax Tv（伪装为视频/影视应用，包名 video.lotus19.ridenovel31 亦暗示视频类，但应用内无任何播放业务实现） |
| 系统无障碍列表服务名 | 无（Manifest 未声明任何 AccessibilityService，系统无障碍列表中不会出现本应用条目） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：app_name 字符串内嵌 U+200B/U+200C/U+200D/U+2060 等零宽字符，渲染为 Dixmax Tv 以规避按名称的检索与比对；application 类与主题为通用壳模板 com.shell.template.app.ShellApplication / Theme.ShellTemplate，与包名命名空间不符；包名 video.lotus19.ridenovel31 下堆料数百个随机命名 Activity/Service 与近百个随机自定义 permission 作为噪音；DEX 类名整体混淆为 i/a/d0/f3 等单双字符包；无 activity-alias 伪装、无伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_INSTALL_PACKAGES` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.shell.template.app.LaunchRouterActivity（android:exported=true、noHistory、taskAffinity=""、Theme.ShellTemplate.Launch） | onCreate → 协程 v.j(this.x, 0, new d2.d(this, null, 1), 3) 启动路由任务 | 原生Activity | **原文**：无（setContentView(2131427357) 后立即异步路由，无任何可见文案）<br>**译注**：无可见界面，纯路由中转页 | 无（用户无任何交互机会，页面随即 finishAndRemoveTask） | `com.shell.template.app.LaunchRouterActivity.onCreate / d2.d.d case 1` |
| 2 | 业务功能触发 | 路由分支：无母包配置 → DebugInstallActivity；有母包配置 → UpgradeActivity | d2.d#d case 1 判定 (b0VarZ?.c?.d == a2.a.e) 与 s1.e.p 包名校验 | 原生Activity | 无 | 无 | `d2.d#d（case 1: launchRouterActivity.startActivity(new Intent(..., DebugInstallActivity.class)) / UpgradeActivity.class）` |
| 3 | 引导说明页 | com.shell.template.feature.debug.DebugInstallActivity「安装调试」面板（layout 2131427356） | onCreate 绑定 4 个 MaterialButton（k(1)/k(2)/k(3)/k(4)），onResume 调用 this.z.c() 与 x() 刷新权限/选中状态 | 原生Activity | **原文**：安装调试 / 选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。/ 选择 APK / 安装所选 APK / 选择 Activity 启动 / 在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。/ 打开无障碍设置 / 尚未选择 APK，点下方按钮开始<br>**译注**：中性“调试工具”面板：选 APK、安装、跨包启动任意 Activity、跳系统无障碍设置 | 需用户主动点击「打开无障碍设置」等按钮；面板可通过 Toolbar 返回键（k(0) → finish()）随时退出，无强制 | `com.shell.template.feature.debug.DebugInstallActivity.onCreate / res/values/strings.xml（debug_install_* 系列）` |
| 4 | 跳受限设置 | com.shell.template.platform.installer.UnknownSourcesPermissionActivity（透明主题）+ PackageInstaller 安装流程 | 点击「安装所选 APK」→ c2.k#onClick case 2 → z1.h.e(new p0(...)) 提交安装；无权限时提示 debug_install_permission_required | 原生Activity | **原文**：请允许此应用安装未知来源应用 / 正在提交安装… / 安装成功 / 安装失败，请重试<br>**译注**：引导用户在系统设置中授予未知来源安装权限，随后提交 APK 安装 | 用户点击安装按钮，并在系统弹窗中确认安装；有明确取消路径（返回键、系统弹窗拒绝） | `c2.k#onClick case 2 / com.shell.template.platform.installer.UnknownSourcesPermissionActivity#c / AndroidManifest REQUEST_INSTALL_PACKAGES` |
| 5 | 跳无障碍设置 | 系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS | 点击「打开无障碍设置」按钮 → c2.k#onClick case 4 → startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：打开无障碍设置 / 无法打开无障碍设置<br>**译注**：一键跳转系统无障碍服务列表页；跳转失败时 Toast 提示 | 仅跳转，不指定任何服务、不弹二次说明；用户在系统页内需自行寻找服务（而本应用并未注册无障碍服务），可自由返回 | `c2.k#onClick case 4 / DebugInstallActivity.onCreate（findViewById(2131230735).setOnClickListener(new k(4, this))）` |
| 6 | 获权后动作 | DebugInstallActivity.onResume（this.z.c(); x()） | 从系统设置页返回后 onResume 重新刷新安装/无障碍权限状态并重绘按钮态 | 原生Activity | **原文**：无新增引导文案（仅状态刷新）<br>**译注**：返回后仅刷新状态，不重跳、不施压、无循环 | 无 | `com.shell.template.feature.debug.DebugInstallActivity.onResume` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- DebugInstallActivity 原生 Activity 面板（layout 2131427356）：标题「安装调试」、副标题「选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。」、提示「在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。」、按钮「选择 APK / 安装所选 APK / 选择 Activity 启动 / 打开无障碍设置」
- Activity 选择器 MaterialAlertDialog（layout 2131427375）：标题「选择 Activity」、副标题「%1$s · 共 %2$d 个，其中 %3$d 个可启动」、提示「可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。」、按钮「启动 / 复制 / 关闭」
- Toast 提示：debug_install_permission_required「请允许此应用安装未知来源应用」、debug_install_accessibility_open_failed「无法打开无障碍设置」、debug_install_launch_failed「启动失败：应用未安装、组件不存在或需要额外权限」、debug_install_activity_not_exported「该 Activity 未导出，母包无法跨包启动」
- 桌面图标下名称：strings.xml app_name「D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v」（含零宽字符）
- 系统无障碍列表：无本应用条目（未声明 AccessibilityService，android:description 不存在）
- UpgradeActivity 本地 WebView（https://appassets.shelltemplate.internal/upgrade-template/index.html）：模板来自加密载荷，静态不可见，运行期为升级/更新引导页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| zh | 选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。 | 选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。 | `res/values/strings.xml → debug_install_subtitle（DebugInstallActivity 副标题）` | 清理工具伪装 |
| zh | 在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。 | 在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。 | `res/values/strings.xml → debug_install_hint` | 受限设置分步教学 |
| zh | 请允许此应用安装未知来源应用 | 请允许此应用安装未知来源应用。 | `res/values/strings.xml → debug_install_permission_required` | 受限设置分步教学 |
| zh | 打开无障碍设置 | 打开无障碍设置。 | `res/values/strings.xml → debug_install_accessibility_settings（按钮文案，点击后 startActivity("android.settings.ACCESSIBILITY_SETTINGS")）` | 良性透明说明 |
| zh | 可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。 | 可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。 | `res/values/strings.xml → debug_install_activity_picker_hint（Activity 选择器对话框）` | 未知 |
| zh | 启动失败：应用未安装、组件不存在或需要额外权限 | 启动失败：应用未安装、组件不存在或需要额外权限。 | `res/values/strings.xml → debug_install_activity_launch_failed` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。从系统无障碍设置返回后仅执行 DebugInstallActivity.onResume 中的 this.z.c() 与 x() 做状态刷新，不重跳、无定时器、无 onResume 死循环；Toolbar 返回键可直接 finish() 退出整个面板。
- **遮罩叠层 / 高仿系统设置页**：无。包内无 SYSTEM_ALERT_WINDOW 权限、无 TYPE_ACCESSIBILITY_OVERLAY、无 WindowManager 悬浮窗代码，也未伪造高仿系统无障碍开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现 ACTION_APPLICATION_DETAILS_SETTINGS、ACTION_MANAGE_UNKNOWN_APP_SOURCES 调用，也无“点右上角菜单允许受限设置”类教学；未知来源安装仅通过 UnknownSourcesPermissionActivity（透明主题）以 startActivityForResult 引导系统弹窗，属常规流程。
- **获权后即时行为与防撤权机制**：无。未声明无障碍服务，故不存在自点确认、自授权、GLOBAL_ACTION_BACK/HOME 阻止撤权等行为。
- **良性降级 / 替代方案**：无（非良性应用，也无降级路径设计；面板本身即最终功能界面）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到前台 Activity 切换为 com.shell.template.feature.debug.DebugInstallActivity 时立即拉起（该界面即冷启动后 0 交互直达的最终前台页）；其次可挂 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间，用于确认跳转是否伴随叠层或遮罩。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区在二阶段：assets/f80at32d.zip 为自定义加密容器（文件头 53 56 4c 54 02 0c，非 ZIP 魔数，8.33 MB），母包运行资源与 UpgradeActivity 的 HTML 模板均需运行期由壳层解密后才会呈现；因此若真实无障碍诱导页藏于母包内，纯静态与冷启动 UTG 首轮均无法捕获，需在设备上先令其完成母包配置下发/解密后再抓 UpgradeActivity 的 WebView。此外外壳本身无加壳（APKiD 仅识别 dexlib 2.x），代码静态完全可见，故本样本“无无障碍诱导”的结论在壳层范围内是确定的。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动直达的投放面板页** | com.shell.template.feature.debug.DebugInstallActivity，标题「安装调试」，含「选择 APK / 安装所选 APK / 选择 Activity 启动 / 打开无障碍设置」四个按钮 | 该页是应用冷启动后第一个（也是唯一）前台界面，直接暴露其非视频业务的真实用途；页面按钮组合（安装 + 跨包启动 + 跳无障碍）是壳模板投放器的强特征，且无任何诱导文案可佐证“未实施无障碍诱导”。 | 标题节点文本「安装调试」与副标题「…或跳转系统无障碍设置」；四个 MaterialButton 的可点击节点及文案「打开无障碍设置」；前台 Activity 类名 com.shell.template.feature.debug.DebugInstallActivity（与包名 video.lotus19.ridenovel31 不符） |
| **跳转后的系统无障碍服务列表页** | android.settings.ACCESSIBILITY_SETTINGS（系统 Settings 无障碍页） | 用于确认跳转后是否存在叠层遮罩、悬浮引导窗或高仿开关页，以及列表中是否出现本应用条目（预期不出现，因未注册无障碍服务），从而判定无障碍跳转仅为预留通道。 | 页面栈顶部是否为系统 Settings 包（com.android.settings），有无第三方悬浮窗覆盖；无障碍服务列表中是否出现 video.lotus19.ridenovel31 相关条目；返回后落回 DebugInstallActivity 而非新的引导页 |
| **有母包配置时的升级/更新引导页** | com.shell.template.feature.upgrade.UpgradeActivity 内 WebView，URL https://appassets.shelltemplate.internal/upgrade-template/index.html | 该页模板由加密载荷 g2.e 提供，静态完全不可见；若运行期能取得母包配置，此页可能承载真正的伪造更新/无障碍诱导文案，是唯一需要运行期补证的分支。 | WebView 内渲染文本（是否出现“立即更新/安装新版本/开启权限”类诱导）；WebView 加载的 asset 域名 appassets.shelltemplate.internal 与页面标题；页面是否注入 window.__SHELL_RUNTIME__ 及 data-theme 属性 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.shell.template.app.LaunchRouterActivity.onCreate`
- `d2.d#d`
- `com.shell.template.feature.debug.DebugInstallActivity.onCreate`
- `c2.k#onClick`
- `com.shell.template.platform.installer.UnknownSourcesPermissionActivity#c`
- `res/values/strings.xml（debug_install_* 系列）/ assets/f80at32d.zip`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**结论：本次审计未发现“无障碍权限诱导”页面流转链。** 该应用根本不包含无障碍服务，也不存在任何引导弹窗、遮罩、WebView 教学页或拒绝授权后的循环重跳；与无障碍有关的唯一入口，是“安装调试”面板上的一个普通按钮，点击后跳转到系统无障碍设置页。

**已证实的代码事实**

- **包内没有任何无障碍服务**：Manifest 中没有声明 `BIND_ACCESSIBILITY_SERVICE` 服务，代码中没有 `AccessibilityService` 子类，也没有 `TYPE_ACCESSIBILITY_OVERLAY`、`SYSTEM_ALERT_WINDOW`、`performGlobalAction` 等调用。预筛给出的无障碍服务类为空，与静态事实一致。
- **冷启动不显示业务界面**：[LaunchRouterActivity.onCreate()](<resource-unit:#1.dex1 code:com.shell.template.app.LaunchRouterActivity#onCreate>) 是唯一的 LAUNCHER 入口，它只调用 `setContentView` 后立即启动协程路由，不呈现任何视频或业务内容。
- **路由直达投放面板**：[d2.d#d](<resource-unit:#1.dex1 code:d2.d#d>) 的 case 1 中，如果没有母包配置，就直接 `startActivity(DebugInstallActivity)` 并调用 `finishAndRemoveTask()`；如果有配置，则转向 `UpgradeActivity`，用 `loadUrl("https://appassets.shelltemplate.internal/upgrade-template/index.html")` 加载升级页。
- **无障碍跳转来自面板按钮**：[c2.k#onClick](<resource-unit:#1.dex1 code:c2.k#onClick>) 的 case 4 执行 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`，失败时 Toast 提示“无法打开无障碍设置”。它由 [DebugInstallActivity.onCreate()](<resource-unit:#1.dex1 code:com.shell.template.feature.debug.DebugInstallActivity#onCreate>) 的 `findViewById(2131230735).setOnClickListener(new k(4, this))` 绑定，需要用户主动点击。
- **投放能力**：同一点击处理器还实现了选取本地 APK、提交安装（配合 `REQUEST_INSTALL_PACKAGES`）、弹出 Activity 选择器并跨包启动任意组件。
- **二阶段载荷加密**：`assets/f80at32d.zip`（8.33 MB）的文件头为 `53 56 4c 54 02 0c`，不是 ZIP 魔数，说明母包资源采用自定义加密格式，静态不可读。

**关键判断**

- 这个样本的恶意性在于**壳模板投放器骨架**：以零宽字符拼接的显示名 `D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v`（渲染为 “Dixmax Tv”）伪装成视频应用，实际主体为 `com.shell.template`，前台第一个界面是“安装调试”工具面板。这一点已登记为 R-001。
- 就本轮问题而言：**不存在分步教学、故障恐吓、不可取消弹窗或遮罩叠层等诱导形态**。无障碍设置跳转只是工具面板里的一个功能入口，文案为“选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置”。因此，行为标签应归为工具面板直达，而非诱导链。
- **静态可见性为 partial**：外壳与面板代码完整可见，但 `assets/f80at32d.zip` 的加密内容、母包配置下发值、远端或本地升级页 HTML 均不可静态还原；真正的无障碍滥用（如果存在）位于二阶段载荷内，属于本次覆盖边界。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "外壳（com.shell.template）全部 Java/Kotlin 代码、Manifest、strings 资源完整静态可见；不可见部分为 assets/f80at32d.zip（文件头 53 56 4c 54，非 ZIP 魔数，自定义加密的二阶段母包载荷）、母包配置下发值（b0VarZ/b2.a），以及 UpgradeActivity 通过 loadUrl 呈现的 upgrade-template/index.html 模板内容（由加密载荷 g2.e 提供）。包内不存在无障碍服务类，因此无障碍相关行为在外壳层已完整可见，无遗漏。",
  "summary_one_liner": "该样本不含任何无障碍服务，也无弹窗/遮罩/教学页诱导，冷启动即路由到通用壳模板的「安装调试」工具面板，其中仅有一个需用户主动点击的按钮直接跳转 android.settings.ACCESSIBILITY_SETTINGS，真实载荷藏于加密的 assets/f80at32d.zip 二阶段。",
  "disguise_identity": {
    "app_display_name": "D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v",
    "claimed_brand_or_persona": "Dixmax Tv（伪装为视频/影视应用，包名 video.lotus19.ridenovel31 亦暗示视频类，但应用内无任何播放业务实现）",
    "a11y_service_label": "无（Manifest 未声明任何 AccessibilityService，系统无障碍列表中不会出现本应用条目）",
    "identity_mismatch": true,
    "obfuscation_tricks": "app_name 字符串内嵌 U+200B/U+200C/U+200D/U+2060 等零宽字符，渲染为 Dixmax Tv 以规避按名称的检索与比对；application 类与主题为通用壳模板 com.shell.template.app.ShellApplication / Theme.ShellTemplate，与包名命名空间不符；包名 video.lotus19.ridenovel31 下堆料数百个随机命名 Activity/Service 与近百个随机自定义 permission 作为噪音；DEX 类名整体混淆为 i/a/d0/f3 等单双字符包；无 activity-alias 伪装、无伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.shell.template.app.LaunchRouterActivity（android:exported=true、noHistory、taskAffinity=\"\"、Theme.ShellTemplate.Launch）",
      "trigger_event": "onCreate → 协程 v.j(this.x, 0, new d2.d(this, null, 1), 3) 启动路由任务",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（setContentView(2131427357) 后立即异步路由，无任何可见文案）",
      "shown_text_zh": "无可见界面，纯路由中转页",
      "user_action_requested": "无（用户无任何交互机会，页面随即 finishAndRemoveTask）",
      "code_anchor": "com.shell.template.app.LaunchRouterActivity.onCreate / d2.d.d case 1"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "路由分支：无母包配置 → DebugInstallActivity；有母包配置 → UpgradeActivity",
      "trigger_event": "d2.d#d case 1 判定 (b0VarZ?.c?.d == a2.a.e) 与 s1.e.p 包名校验",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "冷启动无业务界面，直接分流至投放/升级流程",
      "user_action_requested": "无",
      "code_anchor": "d2.d#d（case 1: launchRouterActivity.startActivity(new Intent(..., DebugInstallActivity.class)) / UpgradeActivity.class）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.shell.template.feature.debug.DebugInstallActivity「安装调试」面板（layout 2131427356）",
      "trigger_event": "onCreate 绑定 4 个 MaterialButton（k(1)/k(2)/k(3)/k(4)），onResume 调用 this.z.c() 与 x() 刷新权限/选中状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "安装调试 / 选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。/ 选择 APK / 安装所选 APK / 选择 Activity 启动 / 在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。/ 打开无障碍设置 / 尚未选择 APK，点下方按钮开始",
      "shown_text_zh": "中性“调试工具”面板：选 APK、安装、跨包启动任意 Activity、跳系统无障碍设置",
      "user_action_requested": "需用户主动点击「打开无障碍设置」等按钮；面板可通过 Toolbar 返回键（k(0) → finish()）随时退出，无强制",
      "code_anchor": "com.shell.template.feature.debug.DebugInstallActivity.onCreate / res/values/strings.xml（debug_install_* 系列）"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "com.shell.template.platform.installer.UnknownSourcesPermissionActivity（透明主题）+ PackageInstaller 安装流程",
      "trigger_event": "点击「安装所选 APK」→ c2.k#onClick case 2 → z1.h.e(new p0(...)) 提交安装；无权限时提示 debug_install_permission_required",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "请允许此应用安装未知来源应用 / 正在提交安装… / 安装成功 / 安装失败，请重试",
      "shown_text_zh": "引导用户在系统设置中授予未知来源安装权限，随后提交 APK 安装",
      "user_action_requested": "用户点击安装按钮，并在系统弹窗中确认安装；有明确取消路径（返回键、系统弹窗拒绝）",
      "code_anchor": "c2.k#onClick case 2 / com.shell.template.platform.installer.UnknownSourcesPermissionActivity#c / AndroidManifest REQUEST_INSTALL_PACKAGES"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "点击「打开无障碍设置」按钮 → c2.k#onClick case 4 → startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "打开无障碍设置 / 无法打开无障碍设置",
      "shown_text_zh": "一键跳转系统无障碍服务列表页；跳转失败时 Toast 提示",
      "user_action_requested": "仅跳转，不指定任何服务、不弹二次说明；用户在系统页内需自行寻找服务（而本应用并未注册无障碍服务），可自由返回",
      "code_anchor": "c2.k#onClick case 4 / DebugInstallActivity.onCreate（findViewById(2131230735).setOnClickListener(new k(4, this))）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "DebugInstallActivity.onResume（this.z.c(); x()）",
      "trigger_event": "从系统设置页返回后 onResume 重新刷新安装/无障碍权限状态并重绘按钮态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无新增引导文案（仅状态刷新）",
      "shown_text_zh": "返回后仅刷新状态，不重跳、不施压、无循环",
      "user_action_requested": "无",
      "code_anchor": "com.shell.template.feature.debug.DebugInstallActivity.onResume"
    }
  ],
  "text_presentation_locations": [
    "DebugInstallActivity 原生 Activity 面板（layout 2131427356）：标题「安装调试」、副标题「选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。」、提示「在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。」、按钮「选择 APK / 安装所选 APK / 选择 Activity 启动 / 打开无障碍设置」",
    "Activity 选择器 MaterialAlertDialog（layout 2131427375）：标题「选择 Activity」、副标题「%1$s · 共 %2$d 个，其中 %3$d 个可启动」、提示「可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。」、按钮「启动 / 复制 / 关闭」",
    "Toast 提示：debug_install_permission_required「请允许此应用安装未知来源应用」、debug_install_accessibility_open_failed「无法打开无障碍设置」、debug_install_launch_failed「启动失败：应用未安装、组件不存在或需要额外权限」、debug_install_activity_not_exported「该 Activity 未导出，母包无法跨包启动」",
    "桌面图标下名称：strings.xml app_name「D​i⁠‌‍x​m⁠⁠a‍⁠x ‌T‍‌⁠v」（含零宽字符）",
    "系统无障碍列表：无本应用条目（未声明 AccessibilityService，android:description 不存在）",
    "UpgradeActivity 本地 WebView（https://appassets.shelltemplate.internal/upgrade-template/index.html）：模板来自加密载荷，静态不可见，运行期为升级/更新引导页"
  ],
  "verbatim_texts": [
    {
      "lang": "zh",
      "text_verbatim": "选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。",
      "text_zh": "选择本地 APK，解析包信息后可直接安装、启动 Activity，或跳转系统无障碍设置。",
      "source_location": "res/values/strings.xml → debug_install_subtitle（DebugInstallActivity 副标题）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "zh",
      "text_verbatim": "在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。",
      "text_zh": "在 Activity 列表中可一键启动或复制组件名。安装权限需在系统设置中授予本应用。",
      "source_location": "res/values/strings.xml → debug_install_hint",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "请允许此应用安装未知来源应用",
      "text_zh": "请允许此应用安装未知来源应用。",
      "source_location": "res/values/strings.xml → debug_install_permission_required",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "打开无障碍设置",
      "text_zh": "打开无障碍设置。",
      "source_location": "res/values/strings.xml → debug_install_accessibility_settings（按钮文案，点击后 startActivity(\"android.settings.ACCESSIBILITY_SETTINGS\")）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。",
      "text_zh": "可启动项排在前面。点「启动」直接打开；点「复制」复制完整组件名。",
      "source_location": "res/values/strings.xml → debug_install_activity_picker_hint（Activity 选择器对话框）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "启动失败：应用未安装、组件不存在或需要额外权限",
      "text_zh": "启动失败：应用未安装、组件不存在或需要额外权限。",
      "source_location": "res/values/strings.xml → debug_install_activity_launch_failed",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。从系统无障碍设置返回后仅执行 DebugInstallActivity.onResume 中的 this.z.c() 与 x() 做状态刷新，不重跳、无定时器、无 onResume 死循环；Toolbar 返回键可直接 finish() 退出整个面板。",
    "overlay_or_fake_settings": "无。包内无 SYSTEM_ALERT_WINDOW 权限、无 TYPE_ACCESSIBILITY_OVERLAY、无 WindowManager 悬浮窗代码，也未伪造高仿系统无障碍开关页。",
    "restricted_settings_13plus_coaching": "无。未出现 ACTION_APPLICATION_DETAILS_SETTINGS、ACTION_MANAGE_UNKNOWN_APP_SOURCES 调用，也无“点右上角菜单允许受限设置”类教学；未知来源安装仅通过 UnknownSourcesPermissionActivity（透明主题）以 startActivityForResult 引导系统弹窗，属常规流程。",
    "post_grant_anti_removal": "无。未声明无障碍服务，故不存在自点确认、自授权、GLOBAL_ACTION_BACK/HOME 阻止撤权等行为。",
    "benign_graceful_degradation": "无（非良性应用，也无降级路径设计；面板本身即最终功能界面）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到前台 Activity 切换为 com.shell.template.feature.debug.DebugInstallActivity 时立即拉起（该界面即冷启动后 0 交互直达的最终前台页）；其次可挂 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间，用于确认跳转是否伴随叠层或遮罩。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动直达的投放面板页",
        "page_identifier": "com.shell.template.feature.debug.DebugInstallActivity，标题「安装调试」，含「选择 APK / 安装所选 APK / 选择 Activity 启动 / 打开无障碍设置」四个按钮",
        "why_most_useful": "该页是应用冷启动后第一个（也是唯一）前台界面，直接暴露其非视频业务的真实用途；页面按钮组合（安装 + 跨包启动 + 跳无障碍）是壳模板投放器的强特征，且无任何诱导文案可佐证“未实施无障碍诱导”。",
        "observable_utg_signals": [
          "标题节点文本「安装调试」与副标题「…或跳转系统无障碍设置」",
          "四个 MaterialButton 的可点击节点及文案「打开无障碍设置」",
          "前台 Activity 类名 com.shell.template.feature.debug.DebugInstallActivity（与包名 video.lotus19.ridenovel31 不符）"
        ]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表页",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS（系统 Settings 无障碍页）",
        "why_most_useful": "用于确认跳转后是否存在叠层遮罩、悬浮引导窗或高仿开关页，以及列表中是否出现本应用条目（预期不出现，因未注册无障碍服务），从而判定无障碍跳转仅为预留通道。",
        "observable_utg_signals": [
          "页面栈顶部是否为系统 Settings 包（com.android.settings），有无第三方悬浮窗覆盖",
          "无障碍服务列表中是否出现 video.lotus19.ridenovel31 相关条目",
          "返回后落回 DebugInstallActivity 而非新的引导页"
        ]
      },
      {
        "page_role": "有母包配置时的升级/更新引导页",
        "page_identifier": "com.shell.template.feature.upgrade.UpgradeActivity 内 WebView，URL https://appassets.shelltemplate.internal/upgrade-template/index.html",
        "why_most_useful": "该页模板由加密载荷 g2.e 提供，静态完全不可见；若运行期能取得母包配置，此页可能承载真正的伪造更新/无障碍诱导文案，是唯一需要运行期补证的分支。",
        "observable_utg_signals": [
          "WebView 内渲染文本（是否出现“立即更新/安装新版本/开启权限”类诱导）",
          "WebView 加载的 asset 域名 appassets.shelltemplate.internal 与页面标题",
          "页面是否注入 window.__SHELL_RUNTIME__ 及 data-theme 属性"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区在二阶段：assets/f80at32d.zip 为自定义加密容器（文件头 53 56 4c 54 02 0c，非 ZIP 魔数，8.33 MB），母包运行资源与 UpgradeActivity 的 HTML 模板均需运行期由壳层解密后才会呈现；因此若真实无障碍诱导页藏于母包内，纯静态与冷启动 UTG 首轮均无法捕获，需在设备上先令其完成母包配置下发/解密后再抓 UpgradeActivity 的 WebView。此外外壳本身无加壳（APKiD 仅识别 dexlib 2.x），代码静态完全可见，故本样本“无无障碍诱导”的结论在壳层范围内是确定的。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION"
  ],
  "code_anchors": [
    "com.shell.template.app.LaunchRouterActivity.onCreate",
    "d2.d#d",
    "com.shell.template.feature.debug.DebugInstallActivity.onCreate",
    "c2.k#onClick",
    "com.shell.template.platform.installer.UnknownSourcesPermissionActivity#c",
    "res/values/strings.xml（debug_install_* 系列）/ assets/f80at32d.zip"
  ]
}
```

</details>
