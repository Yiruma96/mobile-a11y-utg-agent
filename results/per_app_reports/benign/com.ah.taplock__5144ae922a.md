# BN_066__5144ae922a｜锁屏与悬浮组件辅助 — TapLock

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：274.4s

## 1. 一句话核心结论

- **核心申请方式**：TapLock 通过首次启动的可跳过原生引导页（Welcome→Enable Accessibility→Add Widget→Done）说明用途并一键跳转系统无障碍设置，拒权后最多重试 3 次即停，无遮罩、无假设置页、无受限设置教唆，属透明良性申请。
- **静态可见性说明**：全部关键逻辑静态可见：无障碍服务类、跳转 Intent、拒权重试计数、引导页文案均在 classes.dex 与 res/ 中明文可读；无加壳、无加密载荷、无远端 HTML/WebView。仅 MainActivity 的 Compose UI 以资源 ID 绑定文案，未逐条还原到 Composable 点击回调。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5144ae922af78bfa8b80721723c9abc72125c837d4dc4fe94c669b82f655d2e9` |
| 包名 / 年份 | `com.ah.taplock` / 2025-2026 |
| 家族 / 品类 | **锁屏与悬浮组件辅助**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.ah.taplock_23.apk |
| 桌面显示名 | TapLock |
| 引导页宣称品牌/身份 | TapLock（F-Droid 开源项目 modelorona/TapLock，源码链接 https://github.com/modelorona/TapLock） |
| 系统无障碍列表服务名 | TapLock（服务未单独设 android:label，系统无障碍列表沿用应用名 TapLock，描述为 accessibility_service_description） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。未发现空白/换行挤出警告、同形字、多 activity-alias 伪装；android:isAccessibilityTool="true" 为官方 API 标准自声明，与其真实锁屏辅助用途一致。 |
| 无障碍服务类名 | `com.ah.taplock.TapLockAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |
| 系统设置项说明 (`android:description`) | The TapLock accessibility service is necessary to be able to power off the screen. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.ah.taplock.MainActivity（Compose 引导页，内容集 mo1.d / uk） | onCreate；仅当未完成引导（has_completed_onboarding=false）时进入引导流程 | 原生Activity | **原文**：Welcome to TapLock / "Lock your screen instantly with a double-tap. Let's get you set up in a few quick steps."<br>**译注**：欢迎使用 TapLock / 双击即可立即锁屏，我们分几步快速完成设置。 | 点击 Next 继续；界面同时提供 Skip（跳过）按钮，可完全跳过引导 | `com.ah.taplock.MainActivity.onCreate；res/values/strings.xml onboarding_welcome_title/onboarding_welcome_body/onboarding_next/onboarding_skip` |
| 2 | 引导说明页 | MainActivity 内引导页第二页（无障碍说明卡） | 用户点击 Next 进入该页 | 原生Activity | **原文**：Enable Accessibility / TapLock needs the accessibility service to detect double-taps and lock your screen. No other data is collected.<br>**译注**：开启无障碍 / TapLock 需要无障碍服务来识别双击并锁定屏幕，不会收集其他任何数据。 | 点击 Open Settings 前往系统无障碍设置；另有 Skip / Not now 可放弃，应用保留设置页可后续再开 | `res/values/strings.xml onboarding_accessibility_title/onboarding_accessibility_body/onboarding_open_settings/onboarding_skip/not_now` |
| 3 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | 用户点击 Open Settings → 协程体 g7.a() 判定状态未开启（ur0.g()==1）→ startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))；fg0.a() case 2 为等价跳转路径 | 系统无障碍页 | **原文**：无（应用不自绘该页面，直接交由系统无障碍列表呈现）<br>**译注**：无自绘内容，进入系统无障碍服务列表由用户手动选择 TapLock | 在系统列表中点击 TapLock 并确认开启（系统原生警告页由 Android 自身展示，应用未做任何遮挡或伪造） | `g7.a；fg0.a；com.ah.taplock.TapLockTileService.onClick` |
| 4 | 拒权反馈循环 | MainActivity 引导页（保持原页，无强制弹窗） | onAccessibilityServicesStateChanged / onChange 回调 → fg0.a() 重新读取状态；g7.a() 中 ur0.g()<3 时 h(g()+1) 递增重试计数 | 原生Activity | **原文**：Accessibility permission required / Enable accessibility service to use these features<br>**译注**：需要无障碍权限 / 开启无障碍服务以使用这些功能 | 可再次点击前往设置，或直接返回/跳过；重试上限 3 次后不再自动跳转，并写入 has_seen_info 结束本次引导 | `fg0.a（case 2/3 分支，ih0.onAccessibilityServicesStateChanged 调用）；g7.a（ur0.g/ur0.h 计数）` |
| 5 | 获权后动作 | 引导后续页 Add the Widget → You're All Set | 无障碍已开启后继续引导；应用引导添加桌面小组件 | 原生Activity | **原文**：Add the Widget / Go to your home screen, long-press on empty space, and add the TapLock widget. Double-tap it to lock! ｜ "You're All Set!" / TapLock is ready to use. You can customise settings any time from this screen.<br>**译注**：添加小组件 / 回到桌面长按空白处添加 TapLock 小组件，双击即可锁屏！｜一切就绪！/ TapLock 已可使用，随时可在本页调整设置。 | 按提示手动添加桌面小组件并点击 Done；无自动勾选、无自点击确认、无撤权阻断 | `res/values/strings.xml onboarding_widget_title/onboarding_widget_body/onboarding_done_title/onboarding_done_body/onboarding_done` |
| 6 | 业务功能触发 | com.ah.taplock.TapLockTileService（快捷设置磁贴）/ 应用内开关 | 用户点击 QS 磁贴或开启悬浮按钮等依赖无障碍的功能时，检测到服务未启用 | 通知栏 | **原文**：Accessibility Service / Enable accessibility service to use these features<br>**译注**：无障碍服务 / 开启无障碍服务以使用这些功能 | 跳转系统无障碍设置自行开启；用户可取消，不开启则仅该功能不可用 | `com.ah.taplock.TapLockTileService.onClick；res/values/strings.xml accessibility_service/accessibility_required_hint` |
| 7 | 拒权反馈循环 | MainActivity 内 Advanced Protection 提示卡 | 通过 QUERY_ADVANCED_PROTECTION_MODE 权限检测到设备开启 Android Advanced Protection（会拦截所有第三方无障碍服务） | 原生Activity | **原文**：Advanced Protection is on / "This device has Android's Advanced Protection turned on, which blocks all third-party accessibility services. TapLock relies on an accessibility service to lock the screen, so it can't work while Advanced Protection is enabled. To use TapLock, turn off Advanced Protection in Settings > Security & privacy." / Open Security settings<br>**译注**：已开启高级保护 / 本机开启了 Android 高级保护，它会拦截所有第三方无障碍服务。TapLock 依赖无障碍服务锁屏，因此在高级保护开启时无法工作。若要使用 TapLock，请在 设置 > 安全与隐私 中关闭高级保护。/ 打开安全设置 | 可选：点击 Open Security settings 自行决定是否关闭高级保护；应用仅做事实性说明，无恐吓措辞、无强制跳转 | `res/values/strings.xml advanced_protection_title/advanced_protection_description/advanced_protection_open_settings；manifest 权限 QUERY_ADVANCED_PROTECTION_MODE` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 原生 Compose 引导页（Welcome / Enable Accessibility / Add the Widget / You're All Set），带 Skip 与 Next 按钮
- 系统无障碍服务列表条目描述：res/xml/accessibility_service_config.xml → @string/accessibility_service_description
- 应用内设置页状态提示：accessibility_permission_required / accessibility_required_hint
- 应用内 Advanced Protection 提示卡：advanced_protection_title / advanced_protection_description + Open Security settings 按钮
- 应用内电池优化提示卡：battery_optimization_description / battery_status_restricting（仅针对小组件后台可靠性，非无障碍）
- 首页 About 区免责与开源声明：home_screen_disclaimer + github_url
- 快捷设置磁贴点击时的 Toast/跳转提示：accessibility_service / accessibility_required_hint

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | TapLock needs accessibility services to detect double taps and lock the screen. TapLock does not collect any other data or interaction that you have with your device. | TapLock 需要无障碍服务来识别双击并锁定屏幕。TapLock 不会收集你与设备之间的任何其他数据或交互。 | `res/values/strings.xml accessibility_permission_description` | 隐私承诺 |
| en | The TapLock accessibility service is necessary to be able to power off the screen. | TapLock 无障碍服务是关闭屏幕所必需的。 | `res/values/strings.xml accessibility_service_description（系统无障碍列表条目描述）` | 良性透明说明 |
| en | TapLock needs the accessibility service to detect double-taps and lock your screen. No other data is collected. | TapLock 需要无障碍服务来识别双击并锁定屏幕，不会收集其他数据。 | `res/values/strings.xml onboarding_accessibility_body` | 良性透明说明 |
| en | Enable Accessibility | 开启无障碍 | `res/values/strings.xml onboarding_accessibility_title` | 良性透明说明 |
| en | Skip | 跳过 | `res/values/strings.xml onboarding_skip` | 良性透明说明 |
| en | Accessibility permission required | 需要无障碍权限 | `res/values/strings.xml accessibility_permission_required` | 良性透明说明 |
| en | This device has Android's Advanced Protection turned on, which blocks all third-party accessibility services. TapLock relies on an accessibility service to lock the screen, so it can't work while Advanced Protection is enabled. To use TapLock, turn off Advanced Protection in Settings > Security & privacy. | 本机已开启 Android 高级保护，它会拦截所有第三方无障碍服务。TapLock 依赖无障碍服务锁屏，因此在高级保护开启期间无法工作。若要使用 TapLock，请在 设置 > 安全与隐私 中关闭高级保护。 | `res/values/strings.xml advanced_protection_description` | 良性透明说明 |
| en | If the widget stops working after a while, try disabling battery optimization for this app. This allows the accessibility service to run more reliably in the background. | 如果小组件过一段时间失效，请尝试为本应用关闭电池优化，这能让无障碍服务在后台更稳定运行。 | `res/values/strings.xml battery_optimization_description` | 良性透明说明 |
| en | This app collects no personal information and does not access your data. For transparency, the source code is available via the link below: | 本应用不收集任何个人信息，也不访问你的数据。为透明起见，源代码可通过下方链接获取： | `res/values/strings.xml home_screen_disclaimer（配 github_url=https://github.com/modelorona/TapLock）` | 隐私承诺 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：拒权或从系统设置返回后由 onAccessibilityServicesStateChanged/onChange 回读状态，仅在状态仍为未开启时经 ur0 计数重试，重试上限 3 次（ur0.g()<3 才 h(+1)），达到上限写入 has_seen_info 后停止；无 Timer 周期拉起、无 onResume 强制重跳、无阻塞页面。
- **遮罩叠层 / 高仿系统设置页**：无。代码无悬浮窗/遮罩引导层（overlay 线索为空），跳转直接使用系统 android.settings.ACCESSIBILITY_SETTINGS，不自绘高仿无障碍开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全 DEX 未出现 ACTION_APPLICATION_DETAILS_SETTINGS，不存在教用户进应用详情页开启受限设置的路径；唯一与系统保护相关的提示是 Advanced Protection 的事实性说明，且用户可忽略。
- **获权后即时行为与防撤权机制**：无。获权后无自点击确认、无自授权；performGlobalAction 仅用于 GLOBAL_ACTION_LOCK_SCREEN(8) 执行锁屏，不监听设置页做 BACK/HOME 撤权阻断。
- **良性降级 / 替代方案**：有。引导全程可 Skip/Not now 放弃并留在设置页后续再开；未获权时仅依赖无障碍的功能（双击锁屏、悬浮按钮、边缘/角落点击区）不可用，其余设置页、快捷磁贴、桌面小组件配置与说明仍可使用；跳转失败有 fallback Intent（IGNORE_BATTERY_OPTIMIZATION_SETTINGS）。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：首次启动（未完成引导）进入 MainActivity 时即拉起 UTG，完整录制 Welcome→Enable Accessibility→跳系统无障碍页→返回→拒权重试计数→Add Widget→Done 全过程；并另设监测点在出现 Intent android.settings.ACCESSIBILITY_SETTINGS 跳转时截图，用于确认跳转后应用未叠加任何自绘遮罩。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。该应用文本全部为原生 Compose 文本与 strings 资源，无图片诱导、无 WebView 远端页面、无加壳或二阶段载荷；唯一需注意点：MainActivity 的 Compose 文案通过资源 ID 绑定，纯静态文本搜索需按 strings key 而非字面量定位。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（无障碍说明卡）** | MainActivity 内标题 Enable Accessibility、正文以 TapLock needs the accessibility service 开头，含 Open Settings 与 Skip 两个按钮 | 这是该应用唯一向用户索取无障碍权限的界面，能直接判断是否可跳过、文案是否与实际用途一致、是否存在恐吓或伪造系统口吻 | 存在 Skip / Not now 可点击节点；标题与正文为原生文本而非图片；按钮文本 Open Settings 未仿冒系统用语；无倒计时/无不可取消遮罩层 |
| **系统无障碍服务列表项** | Settings 无障碍列表中的 TapLock 条目，描述为 The TapLock accessibility service is necessary to be able to power off the screen. | 核对系统侧展示的服务名与描述是否与应用声明一致，确认无同形字、无空白挤出警告、无伪造 isAccessibilityTool 隐藏风险说明 | 服务名与桌面名一致为 TapLock；描述文本与 strings 一致；未出现被截断/空白占位的警告文案 |
| **跳转前页面与返回后页面** | 跳转前后均为同一 MainActivity 引导页，无新增全屏悬浮窗或系统风格自绘开关 | 区分是否存在设置页压栈遮罩、虚假开关页或 onResume 死循环重跳这类典型诱导手法 | 返回后前台包名仍为 com.ah.taplock 且页面结构未变；重试跳转次数不超过 3 次；无覆盖在系统设置之上的自绘窗口 |
| **Advanced Protection 提示卡** | 标题 Advanced Protection is on，含 Open Security settings 按钮 | 确认该提示是事实性说明还是借安全警告施压，以及是否存在分步教唆关闭系统保护的动线 | 提示为静态卡片非模态强制弹窗；无下一步/确认式分步教学按钮序列；文案明确说明原因与影响 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.ah.taplock.MainActivity.onCreate`
- `g7.a（跳转 ACCESSIBILITY_SETTINGS + ur0 重试计数上限 3）`
- `fg0.a（onAccessibilityServicesStateChanged 回读状态与 case 2 跳转分支）`
- `com.ah.taplock.TapLockAccessibilityService.onAccessibilityEvent / u()（仅 GLOBAL_ACTION_LOCK_SCREEN）`
- `res/xml/accessibility_service_config.xml`
- `res/values/strings.xml（onboarding_accessibility_* / accessibility_service_description / advanced_protection_*）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（代码级定向核验）

**结论：未发现诱导/欺诈式无障碍权限申请。** 该应用走的是透明、可跳过、可降级的标准开源引导流程，文字与实际功能一致，没有遮罩叠层、没有假系统页、没有拒权死循环、没有受限设置分步教唆，也没有多 alias/同形字伪装。

**关键事实：**

1. **无障碍服务自身声明与用途一致**：[TapLockAccessibilityService](<resource-unit:#1 manifest:components>) 声明 `android:isAccessibilityTool="true"`、`permission="BIND_ACCESSIBILITY_SERVICE"`、`exported=false`；[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 仅申请 `typeWindowContentChanged|typeWindowStateChanged|typeWindowsChanged`、`canRetrieveWindowContent`、`canPerformGestures`，事件集合与"识别双击 → 锁屏"目标吻合。系统无障碍列表条目文案取自 `accessibility_service_description`："The TapLock accessibility service is necessary to be able to power off the screen."

2. **唯一实际行为是锁屏**：[TapLockAccessibilityService.u()](<resource-unit:#1.dex1 code:com.ah.taplock.TapLockAccessibilityService#u>) 中只有 `performGlobalAction(8)`（GLOBAL_ACTION_LOCK_SCREEN）+ 计数落盘；[onAccessibilityEvent](<resource-unit:#1.dex1 code:com.ah.taplock.TapLockAccessibilityService#onAccessibilityEvent>) 仅按 `com.android.systemui` 与前台包名过滤，用于排除应用与双击判定，无内容抓取/上报。这是"PERFORM_GLOBAL_ACTION"被预筛标记为 anti_removal 的正常用途，不是撤权对抗。

3. **跳转点只有一处语义**：全 DEX 中 `ACCESSIBILITY_SETTINGS` 仅 3 处调用——[TapLockTileService.onClick](<resource-unit:#1.dex1 code:com.ah.taplock.TapLockTileService#onClick>)、[fg0.a()](<resource-unit:#1.dex1 code:fg0#a>)、[g7.a()](<resource-unit:#1.dex1 code:g7#a>)；**未发现 `ACTION_APPLICATION_DETAILS_SETTINGS`**，即不存在"去应用详情页开启受限设置"的教唆路径。电池优化跳转指向 `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`/`IGNORE_BATTERY_OPTIMIZATION_SETTINGS`，且失败有 fallback。

4. **拒权后是有上限的重试，非死循环**：`g7.a()` 在状态为 1（未开启）时拉起无障碍设置，随后 `ur0.g()/h()` 计数，`<3` 才递增重试；达到阈值即停并写入 `has_seen_info`。没有 Timer 持续拉起、没有 onResume 强制重跳。

5. **文案位置全部是原生 Compose UI + strings 资源**：引导页 `onboarding_welcome_*` / `onboarding_accessibility_*` / `onboarding_widget_*` / `onboarding_done_*`，并存在 `onboarding_skip`（"Skip"）与 `not_now`，属显式可跳过。无 WebView、无 assets HTML、无悬浮窗引导遮罩（overlay 线索为空与代码一致）。

6. **唯一"教用户关安全保护"的文案是 Advanced Protection**（Android 16 新特性会拦截第三方无障碍）：`advanced_protection_title/description` 说明原因并给 "Open Security settings"，属事实性说明而非故障恐吓；同时有 `home_screen_disclaimer` 隐私承诺与 GitHub 源码链接（modelorona/TapLock），身份透明。

**覆盖边界**：MainActivity 主体为 Compose（`mo1.d`）组合式 UI，字符串资源引用经资源 ID 解析，未逐条反编译到每个 Composable 的点击绑定；但跳转、状态判断、拒权计数三处关键逻辑均已静态读到，足以判定流程性质。未登记风险（无成立的恶意命题）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部关键逻辑静态可见：无障碍服务类、跳转 Intent、拒权重试计数、引导页文案均在 classes.dex 与 res/ 中明文可读；无加壳、无加密载荷、无远端 HTML/WebView。仅 MainActivity 的 Compose UI 以资源 ID 绑定文案，未逐条还原到 Composable 点击回调。",
  "summary_one_liner": "TapLock 通过首次启动的可跳过原生引导页（Welcome→Enable Accessibility→Add Widget→Done）说明用途并一键跳转系统无障碍设置，拒权后最多重试 3 次即停，无遮罩、无假设置页、无受限设置教唆，属透明良性申请。",
  "disguise_identity": {
    "app_display_name": "TapLock",
    "claimed_brand_or_persona": "TapLock（F-Droid 开源项目 modelorona/TapLock，源码链接 https://github.com/modelorona/TapLock）",
    "a11y_service_label": "TapLock（服务未单独设 android:label，系统无障碍列表沿用应用名 TapLock，描述为 accessibility_service_description）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。未发现空白/换行挤出警告、同形字、多 activity-alias 伪装；android:isAccessibilityTool=\"true\" 为官方 API 标准自声明，与其真实锁屏辅助用途一致。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.ah.taplock.MainActivity（Compose 引导页，内容集 mo1.d / uk）",
      "trigger_event": "onCreate；仅当未完成引导（has_completed_onboarding=false）时进入引导流程",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Welcome to TapLock / \"Lock your screen instantly with a double-tap. Let's get you set up in a few quick steps.\"",
      "shown_text_zh": "欢迎使用 TapLock / 双击即可立即锁屏，我们分几步快速完成设置。",
      "user_action_requested": "点击 Next 继续；界面同时提供 Skip（跳过）按钮，可完全跳过引导",
      "code_anchor": "com.ah.taplock.MainActivity.onCreate；res/values/strings.xml onboarding_welcome_title/onboarding_welcome_body/onboarding_next/onboarding_skip"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 内引导页第二页（无障碍说明卡）",
      "trigger_event": "用户点击 Next 进入该页",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Enable Accessibility / TapLock needs the accessibility service to detect double-taps and lock your screen. No other data is collected.",
      "shown_text_zh": "开启无障碍 / TapLock 需要无障碍服务来识别双击并锁定屏幕，不会收集其他任何数据。",
      "user_action_requested": "点击 Open Settings 前往系统无障碍设置；另有 Skip / Not now 可放弃，应用保留设置页可后续再开",
      "code_anchor": "res/values/strings.xml onboarding_accessibility_title/onboarding_accessibility_body/onboarding_open_settings/onboarding_skip/not_now"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "用户点击 Open Settings → 协程体 g7.a() 判定状态未开启（ur0.g()==1）→ startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))；fg0.a() case 2 为等价跳转路径",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用不自绘该页面，直接交由系统无障碍列表呈现）",
      "shown_text_zh": "无自绘内容，进入系统无障碍服务列表由用户手动选择 TapLock",
      "user_action_requested": "在系统列表中点击 TapLock 并确认开启（系统原生警告页由 Android 自身展示，应用未做任何遮挡或伪造）",
      "code_anchor": "g7.a；fg0.a；com.ah.taplock.TapLockTileService.onClick"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 引导页（保持原页，无强制弹窗）",
      "trigger_event": "onAccessibilityServicesStateChanged / onChange 回调 → fg0.a() 重新读取状态；g7.a() 中 ur0.g()<3 时 h(g()+1) 递增重试计数",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility permission required / Enable accessibility service to use these features",
      "shown_text_zh": "需要无障碍权限 / 开启无障碍服务以使用这些功能",
      "user_action_requested": "可再次点击前往设置，或直接返回/跳过；重试上限 3 次后不再自动跳转，并写入 has_seen_info 结束本次引导",
      "code_anchor": "fg0.a（case 2/3 分支，ih0.onAccessibilityServicesStateChanged 调用）；g7.a（ur0.g/ur0.h 计数）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "引导后续页 Add the Widget → You're All Set",
      "trigger_event": "无障碍已开启后继续引导；应用引导添加桌面小组件",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Add the Widget / Go to your home screen, long-press on empty space, and add the TapLock widget. Double-tap it to lock! ｜ \"You're All Set!\" / TapLock is ready to use. You can customise settings any time from this screen.",
      "shown_text_zh": "添加小组件 / 回到桌面长按空白处添加 TapLock 小组件，双击即可锁屏！｜一切就绪！/ TapLock 已可使用，随时可在本页调整设置。",
      "user_action_requested": "按提示手动添加桌面小组件并点击 Done；无自动勾选、无自点击确认、无撤权阻断",
      "code_anchor": "res/values/strings.xml onboarding_widget_title/onboarding_widget_body/onboarding_done_title/onboarding_done_body/onboarding_done"
    },
    {
      "step": 6,
      "stage": "业务功能触发",
      "screen_or_component": "com.ah.taplock.TapLockTileService（快捷设置磁贴）/ 应用内开关",
      "trigger_event": "用户点击 QS 磁贴或开启悬浮按钮等依赖无障碍的功能时，检测到服务未启用",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Accessibility Service / Enable accessibility service to use these features",
      "shown_text_zh": "无障碍服务 / 开启无障碍服务以使用这些功能",
      "user_action_requested": "跳转系统无障碍设置自行开启；用户可取消，不开启则仅该功能不可用",
      "code_anchor": "com.ah.taplock.TapLockTileService.onClick；res/values/strings.xml accessibility_service/accessibility_required_hint"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity 内 Advanced Protection 提示卡",
      "trigger_event": "通过 QUERY_ADVANCED_PROTECTION_MODE 权限检测到设备开启 Android Advanced Protection（会拦截所有第三方无障碍服务）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Advanced Protection is on / \"This device has Android's Advanced Protection turned on, which blocks all third-party accessibility services. TapLock relies on an accessibility service to lock the screen, so it can't work while Advanced Protection is enabled. To use TapLock, turn off Advanced Protection in Settings > Security & privacy.\" / Open Security settings",
      "shown_text_zh": "已开启高级保护 / 本机开启了 Android 高级保护，它会拦截所有第三方无障碍服务。TapLock 依赖无障碍服务锁屏，因此在高级保护开启时无法工作。若要使用 TapLock，请在 设置 > 安全与隐私 中关闭高级保护。/ 打开安全设置",
      "user_action_requested": "可选：点击 Open Security settings 自行决定是否关闭高级保护；应用仅做事实性说明，无恐吓措辞、无强制跳转",
      "code_anchor": "res/values/strings.xml advanced_protection_title/advanced_protection_description/advanced_protection_open_settings；manifest 权限 QUERY_ADVANCED_PROTECTION_MODE"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 原生 Compose 引导页（Welcome / Enable Accessibility / Add the Widget / You're All Set），带 Skip 与 Next 按钮",
    "系统无障碍服务列表条目描述：res/xml/accessibility_service_config.xml → @string/accessibility_service_description",
    "应用内设置页状态提示：accessibility_permission_required / accessibility_required_hint",
    "应用内 Advanced Protection 提示卡：advanced_protection_title / advanced_protection_description + Open Security settings 按钮",
    "应用内电池优化提示卡：battery_optimization_description / battery_status_restricting（仅针对小组件后台可靠性，非无障碍）",
    "首页 About 区免责与开源声明：home_screen_disclaimer + github_url",
    "快捷设置磁贴点击时的 Toast/跳转提示：accessibility_service / accessibility_required_hint"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "TapLock needs accessibility services to detect double taps and lock the screen. TapLock does not collect any other data or interaction that you have with your device.",
      "text_zh": "TapLock 需要无障碍服务来识别双击并锁定屏幕。TapLock 不会收集你与设备之间的任何其他数据或交互。",
      "source_location": "res/values/strings.xml accessibility_permission_description",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "The TapLock accessibility service is necessary to be able to power off the screen.",
      "text_zh": "TapLock 无障碍服务是关闭屏幕所必需的。",
      "source_location": "res/values/strings.xml accessibility_service_description（系统无障碍列表条目描述）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "TapLock needs the accessibility service to detect double-taps and lock your screen. No other data is collected.",
      "text_zh": "TapLock 需要无障碍服务来识别双击并锁定屏幕，不会收集其他数据。",
      "source_location": "res/values/strings.xml onboarding_accessibility_body",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility",
      "text_zh": "开启无障碍",
      "source_location": "res/values/strings.xml onboarding_accessibility_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Skip",
      "text_zh": "跳过",
      "source_location": "res/values/strings.xml onboarding_skip",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility permission required",
      "text_zh": "需要无障碍权限",
      "source_location": "res/values/strings.xml accessibility_permission_required",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This device has Android's Advanced Protection turned on, which blocks all third-party accessibility services. TapLock relies on an accessibility service to lock the screen, so it can't work while Advanced Protection is enabled. To use TapLock, turn off Advanced Protection in Settings > Security & privacy.",
      "text_zh": "本机已开启 Android 高级保护，它会拦截所有第三方无障碍服务。TapLock 依赖无障碍服务锁屏，因此在高级保护开启期间无法工作。若要使用 TapLock，请在 设置 > 安全与隐私 中关闭高级保护。",
      "source_location": "res/values/strings.xml advanced_protection_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "If the widget stops working after a while, try disabling battery optimization for this app. This allows the accessibility service to run more reliably in the background.",
      "text_zh": "如果小组件过一段时间失效，请尝试为本应用关闭电池优化，这能让无障碍服务在后台更稳定运行。",
      "source_location": "res/values/strings.xml battery_optimization_description",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This app collects no personal information and does not access your data. For transparency, the source code is available via the link below:",
      "text_zh": "本应用不收集任何个人信息，也不访问你的数据。为透明起见，源代码可通过下方链接获取：",
      "source_location": "res/values/strings.xml home_screen_disclaimer（配 github_url=https://github.com/modelorona/TapLock）",
      "rhetorical_frame": "隐私承诺"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "拒权或从系统设置返回后由 onAccessibilityServicesStateChanged/onChange 回读状态，仅在状态仍为未开启时经 ur0 计数重试，重试上限 3 次（ur0.g()<3 才 h(+1)），达到上限写入 has_seen_info 后停止；无 Timer 周期拉起、无 onResume 强制重跳、无阻塞页面。",
    "overlay_or_fake_settings": "无。代码无悬浮窗/遮罩引导层（overlay 线索为空），跳转直接使用系统 android.settings.ACCESSIBILITY_SETTINGS，不自绘高仿无障碍开关页。",
    "restricted_settings_13plus_coaching": "无。全 DEX 未出现 ACTION_APPLICATION_DETAILS_SETTINGS，不存在教用户进应用详情页开启受限设置的路径；唯一与系统保护相关的提示是 Advanced Protection 的事实性说明，且用户可忽略。",
    "post_grant_anti_removal": "无。获权后无自点击确认、无自授权；performGlobalAction 仅用于 GLOBAL_ACTION_LOCK_SCREEN(8) 执行锁屏，不监听设置页做 BACK/HOME 撤权阻断。",
    "benign_graceful_degradation": "有。引导全程可 Skip/Not now 放弃并留在设置页后续再开；未获权时仅依赖无障碍的功能（双击锁屏、悬浮按钮、边缘/角落点击区）不可用，其余设置页、快捷磁贴、桌面小组件配置与说明仍可使用；跳转失败有 fallback Intent（IGNORE_BATTERY_OPTIMIZATION_SETTINGS）。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "首次启动（未完成引导）进入 MainActivity 时即拉起 UTG，完整录制 Welcome→Enable Accessibility→跳系统无障碍页→返回→拒权重试计数→Add Widget→Done 全过程；并另设监测点在出现 Intent android.settings.ACCESSIBILITY_SETTINGS 跳转时截图，用于确认跳转后应用未叠加任何自绘遮罩。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（无障碍说明卡）",
        "page_identifier": "MainActivity 内标题 Enable Accessibility、正文以 TapLock needs the accessibility service 开头，含 Open Settings 与 Skip 两个按钮",
        "why_most_useful": "这是该应用唯一向用户索取无障碍权限的界面，能直接判断是否可跳过、文案是否与实际用途一致、是否存在恐吓或伪造系统口吻",
        "observable_utg_signals": ["存在 Skip / Not now 可点击节点", "标题与正文为原生文本而非图片", "按钮文本 Open Settings 未仿冒系统用语", "无倒计时/无不可取消遮罩层"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中的 TapLock 条目，描述为 The TapLock accessibility service is necessary to be able to power off the screen.",
        "why_most_useful": "核对系统侧展示的服务名与描述是否与应用声明一致，确认无同形字、无空白挤出警告、无伪造 isAccessibilityTool 隐藏风险说明",
        "observable_utg_signals": ["服务名与桌面名一致为 TapLock", "描述文本与 strings 一致", "未出现被截断/空白占位的警告文案"]
      },
      {
        "page_role": "跳转前页面与返回后页面",
        "page_identifier": "跳转前后均为同一 MainActivity 引导页，无新增全屏悬浮窗或系统风格自绘开关",
        "why_most_useful": "区分是否存在设置页压栈遮罩、虚假开关页或 onResume 死循环重跳这类典型诱导手法",
        "observable_utg_signals": ["返回后前台包名仍为 com.ah.taplock 且页面结构未变", "重试跳转次数不超过 3 次", "无覆盖在系统设置之上的自绘窗口"]
      },
      {
        "page_role": "Advanced Protection 提示卡",
        "page_identifier": "标题 Advanced Protection is on，含 Open Security settings 按钮",
        "why_most_useful": "确认该提示是事实性说明还是借安全警告施压，以及是否存在分步教唆关闭系统保护的动线",
        "observable_utg_signals": ["提示为静态卡片非模态强制弹窗", "无下一步/确认式分步教学按钮序列", "文案明确说明原因与影响"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。该应用文本全部为原生 Compose 文本与 strings 资源，无图片诱导、无 WebView 远端页面、无加壳或二阶段载荷；唯一需注意点：MainActivity 的 Compose 文案通过资源 ID 绑定，纯静态文本搜索需按 strings key 而非字面量定位。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.ah.taplock.MainActivity.onCreate",
    "g7.a（跳转 ACCESSIBILITY_SETTINGS + ur0 重试计数上限 3）",
    "fg0.a（onAccessibilityServicesStateChanged 回读状态与 case 2 跳转分支）",
    "com.ah.taplock.TapLockAccessibilityService.onAccessibilityEvent / u()（仅 GLOBAL_ACTION_LOCK_SCREEN）",
    "res/xml/accessibility_service_config.xml",
    "res/values/strings.xml（onboarding_accessibility_* / accessibility_service_description / advanced_protection_*）"
  ]
}
```

</details>
