# BN_050__29a98e6160｜系统效率与通用辅助 — SD Maid SE

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：119.5s

## 1. 一句话核心结论

- **核心申请方式**：SD Maid SE 在设置向导中通过一张 Compose 说明卡片（含隐私承诺与明确的拒绝按钮）取得用户同意后才跳转系统无障碍设置页，服务描述与文案完全一致，无遮罩、无循环、并提供 root/ADB 降级路径。
- **静态可见性说明**：全部引导文案与跳转逻辑均在 DEX 与 res/values/strings.xml 明文可见：AutomationSetupModule/AutomationSetupCardKt 为 Compose 原生实现，Intent 为 android.settings.ACCESSIBILITY_SETTINGS 硬编码；无加壳、无加密载荷、无远端 HTML 引导页。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `29a98e6160cab1e0fe137e7b19210651122c6ea43791cddc66924ca12e103ac2` |
| 包名 / 年份 | `eu.darken.sdmse` / 2025-2026 |
| 家族 / 品类 | **系统效率与通用辅助**（同池样本数：1） |
| 原始来源标识 | https://github.com/d4rken-org/sdmaid-se/releases/download/v2.2.3-rc0/eu.darken.sdmse-v2.2.3-rc0-20203000-FOSS-RELEASE.apk |
| 桌面显示名 | SD Maid SE |
| 引导页宣称品牌/身份 | SD Maid SE（eu.darken.sdmse，开源系统清理工具，真实身份） |
| 系统无障碍列表服务名 | 未单独设置 android:label，系统列表显示应用名 SD Maid SE，描述为 automation_accessibility_service_description（说明自动化点击缓存清理、显著提示、可随时取消、不收集信息） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅有 R8 混淆后的借用类名（如 okio.Okio__OkioKt#getSettingsIntent 实为设置 Intent 构造工具），不构成身份伪装；无多 activity-alias、无空白/换行挤出警告、无伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `eu.darken.sdmse.automation.core.AutomationService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Users with special accessibility needs can enable this service to allow SD Maid to automate tasks that would otherwise require tedious manual user interaction (e.g. cache deletion).<br><br>Example: If you instruct SD Maid to stop multiple apps then SD Maid can use this service to open each apps settings screen, find the 'Force Stop' button and tap it.<br><br>SD Maid will always prominently show when using this service and provide an easy way for the user to cancel any interaction immediately.<br><br>No actions will be performed without prior user approval. This service can be disabled again at any time without adverse effects. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | Setup 设置向导页（Compose）中的 Accessibility service 卡片 | SetupViewModel.itemsStateFlow 订阅 AutomationSetupModule.state，用户进入设置/向导或首次需要自动化清理能力时渲染卡片 | 原生Activity | **原文**：Accessibility service / The accessibility service allows SD Maid to interact with your screen and automate tedious actions, e.g. tapping "Clear cache" on multiple screens. / SD Maid will not use the accessibility service without your consent, will always display a prominent (cancelable) indicator while active and will not use it to collect information.<br>**译注**：无障碍服务：该服务允许 SD Maid 与你的屏幕交互并自动化繁琐操作（例如在多个界面点击“清除缓存”）。未经你同意 SD Maid 不会使用该服务，使用期间始终显示醒目的（可取消）提示，且不会用它收集信息。 | 阅读说明后选择“Enable service and grant access”（同意）或“Don't use accessibility service”（拒绝），两者均可点击，无强制跳过限制 | `eu.darken.sdmse.setup.automation.AutomationSetupCardKt#AutomationSetupCard / res/values/strings.xml setup_acs_card_title、setup_acs_card_body、setup_acs_card_body2` |
| 2 | 获权后动作 | AutomationSetupModule.setAllow(boolean) | 用户点击同意/拒绝动作，SetupViewModel$itemsStateFlow$1$3$8$1 调用 setAllow | 原生Activity | **原文**：setup_acs_consent_positive_action = Enable service and grant access；setup_acs_consent_negative_action = Don't use accessibility service<br>**译注**：同意：“启用服务并授予访问权限”；拒绝：“不使用无障碍服务” | 点击同意后写入 GeneralSettings.hasAcsConsent=true；点击拒绝则 hasAcsConsent=false 并 disableSelf() 关闭已启用的服务 | `eu.darken.sdmse.setup.automation.AutomationSetupModule#setAllow` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载/已安装的服务列表 | 同意后状态机 canSelfEnable/isServiceEnabled 为 false，由状态协程构造 Intent 跳转 | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS（系统页内容由 OS 渲染，条目描述见 accessibility_service.xml 引用文案）<br>**译注**：跳转 Android 系统无障碍设置页，用户在系统列表中手动开启 SD Maid SE 的无障碍服务 | 在系统无障碍列表中找到 SD Maid SE 并手动打开开关（需用户在系统 UI 上二次确认） | `eu.darken.sdmse.setup.automation.AutomationSetupModule$state$1#invokeSuspend / res/xml/accessibility_service.xml` |
| 4 | 引导说明页 | 卡片内 Restricted settings 提示块（AutomationUiModel.showAppOpsRestrictionHint 控制显隐） | AutomationToolsHelperKt.mightBeRestrictedDueToSideload(context) 判定为侧载安装导致受限，且 hasTriggeredRestrictions 记录首次触发 | 原生Activity | **原文**：Restricted settings / Can't enable SD Maids accessibility service? Android 13+ may apply restrictions to apps not installed via Google Play. Lift these restrictions from the system's detail page for SD Maid. The option is in the context menu in the top right corner.<br>**译注**：受限设置：无法开启 SD Maid 的无障碍服务？Android 13+ 可能对非 Google Play 安装的应用施加限制。请在系统中 SD Maid 的应用详情页解除该限制，选项位于右上角菜单中。 | 自行进入应用详情页右上角菜单解除受限设置（仅文字指引，无伪造系统页、无自动点击） | `eu.darken.sdmse.setup.automation.AutomationSetupModule#setAllow / res/values/strings.xml setup_acs_appops_restriction_title、setup_acs_appops_restriction_body` |
| 5 | 拒权反馈循环 | Accessibility service 卡片状态 Chip 行 | 用户从系统设置返回后 AutomationService.onCreate 触发 refresh()，重新计算 isServiceEnabled/isServiceRunning | 原生Activity | **原文**：Accessibility service is disabled / Service will be launched on demand / The service is enabled, but not running. Toggle it off/on or reboot your device. Check that SD Maid is not being "optimized" by the system.<br>**译注**：无障碍服务已禁用 / 服务将按需启动 / 服务已启用但未运行，请关闭再打开或重启设备，并检查 SD Maid 是否被系统“优化”了。 | 仅展示当前状态与排障建议，用户可离开；无倒计时、无 onResume 自动重跳、无不可取消弹窗 | `eu.darken.sdmse.setup.automation.AutomationSetupCardKt#AutomationSetupCard / res/values/strings.xml setup_acs_state_disabled、setup_acs_state_ondemand、setup_acs_state_stopped_hint` |
| 6 | 获权后动作 | 自动化执行期全屏说明浮层（automation overlay） | 用户发起需要无障碍点击的清理任务（如批量清除缓存）且服务已启用 | 悬浮窗Overlay | **原文**：SD Maid is interacting with your device. It's not possible to use the screen at the same time. Wait until the operation is finished or cancel it.<br>**译注**：SD Maid 正在与你的设备交互，此期间无法同时使用屏幕。请等待操作完成或取消操作。 | 等待完成或点击取消（提供 cancelable 入口，用于终止自动化而非诱导授权） | `res/values/strings.xml automation_screenoverlay_explanation / eu.darken.sdmse.automation.core.AutomationService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Setup 设置向导页内的 Compose「Accessibility service」卡片（AutomationSetupCardKt.AutomationSetupCard），含标题、说明、隐私承诺、状态 Chip、同意/拒绝两个按钮
- 同一卡片内条件显示的「Restricted settings」「Blocked by Advanced Protection」提示块（setup_acs_appops_restriction_*、setup_acs_advanced_protection_*）
- 系统无障碍列表中的服务描述 android:description（res/xml/accessibility_service.xml → automation_accessibility_service_description，多语言 strings.xml 均已翻译）
- 应用内自动化错误提示（appcleaner_automation_unavailable_body、automation_error_* 系列），在清理失败时说明需要该服务或改用 root/ADB
- 自动化执行期的全屏说明浮层 automation_screenoverlay_explanation（可取消）
- 设置页通用项 setup_incomplete_card_*、setup_forcedshow_summary、setup_dismiss_hint，用于重新进入向导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Users with special accessibility needs can enable this service to allow SD Maid to automate tasks that would otherwise require tedious manual user interaction (e.g. cache deletion). Example: If you instruct SD Maid to stop multiple apps then SD Maid can use this service to open each apps settings screen, find the 'Force Stop' button and tap it. SD Maid will always prominently show when using this service and provide an easy way for the user to cancel any interaction immediately. No actions will be performed without prior user approval. This service can be disabled again at any time without adverse effects. | 有特殊无障碍需求的用户可启用此服务，让 SD Maid 自动化那些本来需要繁琐手动交互的任务（例如清除缓存）。示例：如果你让 SD Maid 停止多个应用，SD Maid 可以用此服务打开每个应用的设置界面、找到“强行停止”按钮并点击。SD Maid 在使用此服务时始终会醒目提示，并提供便捷方式让用户立即取消任何交互。未经用户事先批准不会执行任何操作。此服务可随时再次禁用且无不良影响。 | `res/values/strings.xml → automation_accessibility_service_description（经 res/xml/accessibility_service.xml 在系统无障碍列表展示）` | 良性透明说明 |
| en | The accessibility service allows SD Maid to interact with your screen and automate tedious actions, e.g. tapping "Clear cache" on multiple screens. | 无障碍服务允许 SD Maid 与你的屏幕交互并自动化繁琐操作，例如在多个界面点击“清除缓存”。 | `res/values/strings.xml → setup_acs_card_body（AutomationSetupCardKt 渲染）` | 良性透明说明 |
| en | SD Maid will not use the accessibility service without your consent, will always display a prominent (cancelable) indicator while active and will not use it to collect information. | 未经你同意 SD Maid 不会使用无障碍服务，使用期间始终显示醒目的（可取消）提示，且不会用它收集信息。 | `res/values/strings.xml → setup_acs_card_body2` | 隐私承诺 |
| en | Can't enable SD Maids accessibility service? Android 13+ may apply restrictions to apps not installed via Google Play. Lift these restrictions from the system's detail page for SD Maid. The option is in the context menu in the top right corner. | 无法开启 SD Maid 的无障碍服务？Android 13+ 可能对非 Google Play 安装的应用施加限制。请在系统中 SD Maid 的应用详情页解除该限制，选项位于右上角菜单中。 | `res/values/strings.xml → setup_acs_appops_restriction_body（showAppOpsRestrictionHint 控制显示）` | 受限设置分步教学 |
| en | If you change your mind, you can alter this option again by going into settings and restarting the setup. | 如果你改变主意，可以进入设置重新运行向导来更改此选项。 | `res/values/strings.xml → setup_acs_disallow_hint` | 良性透明说明 |
| en | With ADB access set up, SD Maid can do most of this without the accessibility service. | 配置 ADB 访问后，SD Maid 无需无障碍服务也能完成大部分此类操作。 | `res/values/strings.xml → automation_error_compatibility_adb_hint` | 良性透明说明 |
| en | SD Maid is interacting with your device. It's not possible to use the screen at the same time. Wait until the operation is finished or cancel it. | SD Maid 正在与你的设备交互，此期间无法同时使用屏幕。请等待操作完成或取消操作。 | `res/values/strings.xml → automation_screenoverlay_explanation` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。拒绝时 setAllow(false) 将 hasAcsConsent 置 false 并调用 AutomationService.disableSelf()；从系统设置返回后仅通过 refresh() 更新状态 Chip（disabled/on-demand/stopped 及排障建议），不自动重新拉起设置页，用户可随时关闭卡片或退出向导。
- **遮罩叠层 / 高仿系统设置页**：无。运行期全屏浮层仅在自动化执行时出现，文案说明“正在与设备交互，可取消”，用途是防止用户同时操作，不用于权限引导；不存在高仿系统无障碍开关页。
- **Android 13+ 受限设置（Restricted Settings）应对**：有文字指引但无绕过：setup_acs_appops_restriction_body 提示用户在系统应用详情页右上角菜单解除 Android 13+ 受限设置；条件由 mightBeRestrictedDueToSideload() 判定。未见 Session 安装器或自动点击绕过路径。
- **获权后即时行为与防撤权机制**：无。未发现监听设置页、GLOBAL_ACTION_BACK/HOME 阻止撤权或自点确认的实现；反而提供 setup_acs_disallow_hint 说明可随时改回，并在撤权后自动 disableSelf。
- **良性降级 / 替代方案**：有。可改用 root 或 ADB(Shizuku/Porter) 通道完成同类清理（automation_error_compatibility_adb_hint、automation_error_disabled_app_body 明确给出替代方案）；服务支持按需启动（Service will be launched on demand）；无权限时清理功能降级并给出提示而非阻断使用。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Activity 启动 Intent 为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（由 AutomationSetupModule.state 协程发起），此时先抓当前栈顶的 Setup 向导页卡片，再抓随后压栈的系统无障碍列表页；另可在进入设置向导（Setup）或点按“Enable service and grant access”时抓同意/拒绝双按钮界面。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导文案全部为可提取的 Compose 文本与 strings 资源，无图片/纯图诱导。注意 R8 混淆使部分类名借用第三方包名（如 okio.Okio__OkioKt#getSettingsIntent 实为设置 Intent 工具），纯符号匹配易误判归属，需结合调用方确认。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **向导内无障碍说明卡片（同意前）** | eu.darken.sdmse 设置向导 Compose 页，可见文本 “Accessibility service” + “Enable service and grant access” + “Don't use accessibility service” | 这是唯一承载说明与隐私承诺的授权前置页，可直接区分“透明说明”与“诱导/无取消” | 是否存在明确的拒绝按钮文本；是否同时给出用途与“不收集信息”承诺；是否出现“Restricted settings”提示块 |
| **系统无障碍服务列表项** | android.settings.ACCESSIBILITY_SETTINGS 页内 SD Maid SE 条目 | 核对系统列表中展示的服务名与描述是否与应用内文案一致，是否存在空白/换行挤出或伪造 isAccessibilityTool 标记 | 条目标题是否为 SD Maid SE（无异常空白/同形字）；描述文本是否与 automation_accessibility_service_description 一致；是否存在多条同名或 activity-alias 造成的重复项 |
| **从设置返回后的状态回显页** | 同一 Setup 卡片，Chip 文本为 “Accessibility service is disabled / Service will be launched on demand” | 用于判定是否存在拒权后自动重跳的循环诱导 | 返回后是否再次自动拉起 ACCESSIBILITY_SETTINGS；是否出现不可取消弹窗或倒计时；状态文案是否与真实开关状态一致 |
| **自动化执行期浮层** | 全屏说明浮层 “SD Maid is interacting with your device…”（含取消入口） | 确认浮层用途是防误触而非遮罩式诱导，并核对是否可取消 | 浮层是否覆盖系统设置页并叠加引导文案；是否存在取消按钮；是否在无障碍开关页上方压栈 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `eu.darken.sdmse.setup.automation.AutomationSetupCardKt#AutomationSetupCard`
- `eu.darken.sdmse.setup.automation.AutomationSetupModule#setAllow`
- `eu.darken.sdmse.setup.automation.AutomationSetupModule$state$1#invokeSuspend`
- `eu.darken.sdmse.setup.automation.AutomationToolsHelperKt#mightBeRestrictedDueToSideload`
- `res/values/strings.xml（setup_acs_card_* / setup_acs_consent_* / setup_acs_appops_restriction_*）`
- `res/xml/accessibility_service.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**判定：良性透明授权，未发现诱导、伪装或反卸载行为。**

- **无障碍服务身份真实**：`AutomationService` 以 `BIND_ACCESSIBILITY_SERVICE` 声明，`res/xml/accessibility_service.xml` 中 `description` 直接引用 `automation_accessibility_service_description`，在系统无障碍列表中明确写出“SD Maid 将用此服务自动化点击（如清除缓存）、使用时会显著提示并可随时取消、未经用户同意不执行任何操作、不用于收集信息”，与 `setup_acs_card_body2` 的应用内文案一致，无空白/换行挤出警告、无同形字、无伪造 `isAccessibilityTool`。
- **引导载体是应用内 Compose 卡片 + 原生跳转**：`SetupViewModel` → `AutomationSetupModule.state` 计算状态 → [AutomationSetupCardKt.AutomationSetupCard()](<resource-unit:#1.dex1 code:eu.darken.sdmse.setup.automation.AutomationSetupCardKt#AutomationSetupCard>) 渲染 `setup_acs_card_title/body/body2`，正/负两个动作分别是“Enable service and grant access”与“Don't use accessibility service”；用户点“同意”才写 `GeneralSettings.hasAcsConsent`，再由 [AutomationSetupModule.state$1.invokeSuspend()](<resource-unit:#1.dex1 code:eu.darken.sdmse.setup.automation.AutomationSetupModule$state$1#invokeSuspend>) 构造 `android.settings.ACCESSIBILITY_SETTINGS` 跳系统设置页。全流程无 WebView、无远端 HTML、无高仿系统开关页、无叠层遮罩。
- **Android 13+ 受限设置仅文字教学**：`setup_acs_appops_restriction_body` 提示“从系统详情页右上角菜单解除限制”，属系统要求下的正常指引，且未伴随强制循环或伪造弹窗。
- **无拒绝循环、有明确降级**：`setAllow(false)` 直接 `disableSelf()` 并持久化 `hasAcsConsent=false`，字符串 `setup_acs_disallow_hint` 说明可随时改回；状态机区分 enabled/running/on-demand/stopped，不主动重复拉起设置页；`automation_error_compatibility_adb_hint`、root/ADB 相关文案提供替代路径。运行期 `automation_screenoverlay_explanation` 悬浮说明是“清理中请勿操作、可取消”，不是权限诱导遮罩。
- **静态可见性完整**：无加壳、无动态加载载荷；`RESTRICTED_STR`/`SESSION_INSTALLER` 线索对应受限设置提示与 Shizuku/Porter 安装通道，非绕过手段。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导文案与跳转逻辑均在 DEX 与 res/values/strings.xml 明文可见：AutomationSetupModule/AutomationSetupCardKt 为 Compose 原生实现，Intent 为 android.settings.ACCESSIBILITY_SETTINGS 硬编码；无加壳、无加密载荷、无远端 HTML 引导页。",
  "summary_one_liner": "SD Maid SE 在设置向导中通过一张 Compose 说明卡片（含隐私承诺与明确的拒绝按钮）取得用户同意后才跳转系统无障碍设置页，服务描述与文案完全一致，无遮罩、无循环、并提供 root/ADB 降级路径。",
  "disguise_identity": {
    "app_display_name": "SD Maid SE",
    "claimed_brand_or_persona": "SD Maid SE（eu.darken.sdmse，开源系统清理工具，真实身份）",
    "a11y_service_label": "未单独设置 android:label，系统列表显示应用名 SD Maid SE，描述为 automation_accessibility_service_description（说明自动化点击缓存清理、显著提示、可随时取消、不收集信息）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅有 R8 混淆后的借用类名（如 okio.Okio__OkioKt#getSettingsIntent 实为设置 Intent 构造工具），不构成身份伪装；无多 activity-alias、无空白/换行挤出警告、无伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "Setup 设置向导页（Compose）中的 Accessibility service 卡片",
      "trigger_event": "SetupViewModel.itemsStateFlow 订阅 AutomationSetupModule.state，用户进入设置/向导或首次需要自动化清理能力时渲染卡片",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility service / The accessibility service allows SD Maid to interact with your screen and automate tedious actions, e.g. tapping \"Clear cache\" on multiple screens. / SD Maid will not use the accessibility service without your consent, will always display a prominent (cancelable) indicator while active and will not use it to collect information.",
      "shown_text_zh": "无障碍服务：该服务允许 SD Maid 与你的屏幕交互并自动化繁琐操作（例如在多个界面点击“清除缓存”）。未经你同意 SD Maid 不会使用该服务，使用期间始终显示醒目的（可取消）提示，且不会用它收集信息。",
      "user_action_requested": "阅读说明后选择“Enable service and grant access”（同意）或“Don't use accessibility service”（拒绝），两者均可点击，无强制跳过限制",
      "code_anchor": "eu.darken.sdmse.setup.automation.AutomationSetupCardKt#AutomationSetupCard / res/values/strings.xml setup_acs_card_title、setup_acs_card_body、setup_acs_card_body2"
    },
    {
      "step": 2,
      "stage": "获权后动作",
      "screen_or_component": "AutomationSetupModule.setAllow(boolean)",
      "trigger_event": "用户点击同意/拒绝动作，SetupViewModel$itemsStateFlow$1$3$8$1 调用 setAllow",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "setup_acs_consent_positive_action = Enable service and grant access；setup_acs_consent_negative_action = Don't use accessibility service",
      "shown_text_zh": "同意：“启用服务并授予访问权限”；拒绝：“不使用无障碍服务”",
      "user_action_requested": "点击同意后写入 GeneralSettings.hasAcsConsent=true；点击拒绝则 hasAcsConsent=false 并 disableSelf() 关闭已启用的服务",
      "code_anchor": "eu.darken.sdmse.setup.automation.AutomationSetupModule#setAllow"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载/已安装的服务列表",
      "trigger_event": "同意后状态机 canSelfEnable/isServiceEnabled 为 false，由状态协程构造 Intent 跳转",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS（系统页内容由 OS 渲染，条目描述见 accessibility_service.xml 引用文案）",
      "shown_text_zh": "跳转 Android 系统无障碍设置页，用户在系统列表中手动开启 SD Maid SE 的无障碍服务",
      "user_action_requested": "在系统无障碍列表中找到 SD Maid SE 并手动打开开关（需用户在系统 UI 上二次确认）",
      "code_anchor": "eu.darken.sdmse.setup.automation.AutomationSetupModule$state$1#invokeSuspend / res/xml/accessibility_service.xml"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "卡片内 Restricted settings 提示块（AutomationUiModel.showAppOpsRestrictionHint 控制显隐）",
      "trigger_event": "AutomationToolsHelperKt.mightBeRestrictedDueToSideload(context) 判定为侧载安装导致受限，且 hasTriggeredRestrictions 记录首次触发",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Restricted settings / Can't enable SD Maids accessibility service? Android 13+ may apply restrictions to apps not installed via Google Play. Lift these restrictions from the system's detail page for SD Maid. The option is in the context menu in the top right corner.",
      "shown_text_zh": "受限设置：无法开启 SD Maid 的无障碍服务？Android 13+ 可能对非 Google Play 安装的应用施加限制。请在系统中 SD Maid 的应用详情页解除该限制，选项位于右上角菜单中。",
      "user_action_requested": "自行进入应用详情页右上角菜单解除受限设置（仅文字指引，无伪造系统页、无自动点击）",
      "code_anchor": "eu.darken.sdmse.setup.automation.AutomationSetupModule#setAllow / res/values/strings.xml setup_acs_appops_restriction_title、setup_acs_appops_restriction_body"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "Accessibility service 卡片状态 Chip 行",
      "trigger_event": "用户从系统设置返回后 AutomationService.onCreate 触发 refresh()，重新计算 isServiceEnabled/isServiceRunning",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility service is disabled / Service will be launched on demand / The service is enabled, but not running. Toggle it off/on or reboot your device. Check that SD Maid is not being \"optimized\" by the system.",
      "shown_text_zh": "无障碍服务已禁用 / 服务将按需启动 / 服务已启用但未运行，请关闭再打开或重启设备，并检查 SD Maid 是否被系统“优化”了。",
      "user_action_requested": "仅展示当前状态与排障建议，用户可离开；无倒计时、无 onResume 自动重跳、无不可取消弹窗",
      "code_anchor": "eu.darken.sdmse.setup.automation.AutomationSetupCardKt#AutomationSetupCard / res/values/strings.xml setup_acs_state_disabled、setup_acs_state_ondemand、setup_acs_state_stopped_hint"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "自动化执行期全屏说明浮层（automation overlay）",
      "trigger_event": "用户发起需要无障碍点击的清理任务（如批量清除缓存）且服务已启用",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "SD Maid is interacting with your device. It's not possible to use the screen at the same time. Wait until the operation is finished or cancel it.",
      "shown_text_zh": "SD Maid 正在与你的设备交互，此期间无法同时使用屏幕。请等待操作完成或取消操作。",
      "user_action_requested": "等待完成或点击取消（提供 cancelable 入口，用于终止自动化而非诱导授权）",
      "code_anchor": "res/values/strings.xml automation_screenoverlay_explanation / eu.darken.sdmse.automation.core.AutomationService"
    }
  ],
  "text_presentation_locations": [
    "Setup 设置向导页内的 Compose「Accessibility service」卡片（AutomationSetupCardKt.AutomationSetupCard），含标题、说明、隐私承诺、状态 Chip、同意/拒绝两个按钮",
    "同一卡片内条件显示的「Restricted settings」「Blocked by Advanced Protection」提示块（setup_acs_appops_restriction_*、setup_acs_advanced_protection_*）",
    "系统无障碍列表中的服务描述 android:description（res/xml/accessibility_service.xml → automation_accessibility_service_description，多语言 strings.xml 均已翻译）",
    "应用内自动化错误提示（appcleaner_automation_unavailable_body、automation_error_* 系列），在清理失败时说明需要该服务或改用 root/ADB",
    "自动化执行期的全屏说明浮层 automation_screenoverlay_explanation（可取消）",
    "设置页通用项 setup_incomplete_card_*、setup_forcedshow_summary、setup_dismiss_hint，用于重新进入向导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Users with special accessibility needs can enable this service to allow SD Maid to automate tasks that would otherwise require tedious manual user interaction (e.g. cache deletion). Example: If you instruct SD Maid to stop multiple apps then SD Maid can use this service to open each apps settings screen, find the 'Force Stop' button and tap it. SD Maid will always prominently show when using this service and provide an easy way for the user to cancel any interaction immediately. No actions will be performed without prior user approval. This service can be disabled again at any time without adverse effects.",
      "text_zh": "有特殊无障碍需求的用户可启用此服务，让 SD Maid 自动化那些本来需要繁琐手动交互的任务（例如清除缓存）。示例：如果你让 SD Maid 停止多个应用，SD Maid 可以用此服务打开每个应用的设置界面、找到“强行停止”按钮并点击。SD Maid 在使用此服务时始终会醒目提示，并提供便捷方式让用户立即取消任何交互。未经用户事先批准不会执行任何操作。此服务可随时再次禁用且无不良影响。",
      "source_location": "res/values/strings.xml → automation_accessibility_service_description（经 res/xml/accessibility_service.xml 在系统无障碍列表展示）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "The accessibility service allows SD Maid to interact with your screen and automate tedious actions, e.g. tapping \"Clear cache\" on multiple screens.",
      "text_zh": "无障碍服务允许 SD Maid 与你的屏幕交互并自动化繁琐操作，例如在多个界面点击“清除缓存”。",
      "source_location": "res/values/strings.xml → setup_acs_card_body（AutomationSetupCardKt 渲染）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "SD Maid will not use the accessibility service without your consent, will always display a prominent (cancelable) indicator while active and will not use it to collect information.",
      "text_zh": "未经你同意 SD Maid 不会使用无障碍服务，使用期间始终显示醒目的（可取消）提示，且不会用它收集信息。",
      "source_location": "res/values/strings.xml → setup_acs_card_body2",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Can't enable SD Maids accessibility service? Android 13+ may apply restrictions to apps not installed via Google Play. Lift these restrictions from the system's detail page for SD Maid. The option is in the context menu in the top right corner.",
      "text_zh": "无法开启 SD Maid 的无障碍服务？Android 13+ 可能对非 Google Play 安装的应用施加限制。请在系统中 SD Maid 的应用详情页解除该限制，选项位于右上角菜单中。",
      "source_location": "res/values/strings.xml → setup_acs_appops_restriction_body（showAppOpsRestrictionHint 控制显示）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "If you change your mind, you can alter this option again by going into settings and restarting the setup.",
      "text_zh": "如果你改变主意，可以进入设置重新运行向导来更改此选项。",
      "source_location": "res/values/strings.xml → setup_acs_disallow_hint",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "With ADB access set up, SD Maid can do most of this without the accessibility service.",
      "text_zh": "配置 ADB 访问后，SD Maid 无需无障碍服务也能完成大部分此类操作。",
      "source_location": "res/values/strings.xml → automation_error_compatibility_adb_hint",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "SD Maid is interacting with your device. It's not possible to use the screen at the same time. Wait until the operation is finished or cancel it.",
      "text_zh": "SD Maid 正在与你的设备交互，此期间无法同时使用屏幕。请等待操作完成或取消操作。",
      "source_location": "res/values/strings.xml → automation_screenoverlay_explanation",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。拒绝时 setAllow(false) 将 hasAcsConsent 置 false 并调用 AutomationService.disableSelf()；从系统设置返回后仅通过 refresh() 更新状态 Chip（disabled/on-demand/stopped 及排障建议），不自动重新拉起设置页，用户可随时关闭卡片或退出向导。",
    "overlay_or_fake_settings": "无。运行期全屏浮层仅在自动化执行时出现，文案说明“正在与设备交互，可取消”，用途是防止用户同时操作，不用于权限引导；不存在高仿系统无障碍开关页。",
    "restricted_settings_13plus_coaching": "有文字指引但无绕过：setup_acs_appops_restriction_body 提示用户在系统应用详情页右上角菜单解除 Android 13+ 受限设置；条件由 mightBeRestrictedDueToSideload() 判定。未见 Session 安装器或自动点击绕过路径。",
    "post_grant_anti_removal": "无。未发现监听设置页、GLOBAL_ACTION_BACK/HOME 阻止撤权或自点确认的实现；反而提供 setup_acs_disallow_hint 说明可随时改回，并在撤权后自动 disableSelf。",
    "benign_graceful_degradation": "有。可改用 root 或 ADB(Shizuku/Porter) 通道完成同类清理（automation_error_compatibility_adb_hint、automation_error_disabled_app_body 明确给出替代方案）；服务支持按需启动（Service will be launched on demand）；无权限时清理功能降级并给出提示而非阻断使用。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Activity 启动 Intent 为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（由 AutomationSetupModule.state 协程发起），此时先抓当前栈顶的 Setup 向导页卡片，再抓随后压栈的系统无障碍列表页；另可在进入设置向导（Setup）或点按“Enable service and grant access”时抓同意/拒绝双按钮界面。",
    "key_pages_to_capture": [
      {
        "page_role": "向导内无障碍说明卡片（同意前）",
        "page_identifier": "eu.darken.sdmse 设置向导 Compose 页，可见文本 “Accessibility service” + “Enable service and grant access” + “Don't use accessibility service”",
        "why_most_useful": "这是唯一承载说明与隐私承诺的授权前置页，可直接区分“透明说明”与“诱导/无取消”",
        "observable_utg_signals": ["是否存在明确的拒绝按钮文本", "是否同时给出用途与“不收集信息”承诺", "是否出现“Restricted settings”提示块"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 页内 SD Maid SE 条目",
        "why_most_useful": "核对系统列表中展示的服务名与描述是否与应用内文案一致，是否存在空白/换行挤出或伪造 isAccessibilityTool 标记",
        "observable_utg_signals": ["条目标题是否为 SD Maid SE（无异常空白/同形字）", "描述文本是否与 automation_accessibility_service_description 一致", "是否存在多条同名或 activity-alias 造成的重复项"]
      },
      {
        "page_role": "从设置返回后的状态回显页",
        "page_identifier": "同一 Setup 卡片，Chip 文本为 “Accessibility service is disabled / Service will be launched on demand”",
        "why_most_useful": "用于判定是否存在拒权后自动重跳的循环诱导",
        "observable_utg_signals": ["返回后是否再次自动拉起 ACCESSIBILITY_SETTINGS", "是否出现不可取消弹窗或倒计时", "状态文案是否与真实开关状态一致"]
      },
      {
        "page_role": "自动化执行期浮层",
        "page_identifier": "全屏说明浮层 “SD Maid is interacting with your device…”（含取消入口）",
        "why_most_useful": "确认浮层用途是防误触而非遮罩式诱导，并核对是否可取消",
        "observable_utg_signals": ["浮层是否覆盖系统设置页并叠加引导文案", "是否存在取消按钮", "是否在无障碍开关页上方压栈"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导文案全部为可提取的 Compose 文本与 strings 资源，无图片/纯图诱导。注意 R8 混淆使部分类名借用第三方包名（如 okio.Okio__OkioKt#getSettingsIntent 实为设置 Intent 工具），纯符号匹配易误判归属，需结合调用方确认。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "eu.darken.sdmse.setup.automation.AutomationSetupCardKt#AutomationSetupCard",
    "eu.darken.sdmse.setup.automation.AutomationSetupModule#setAllow",
    "eu.darken.sdmse.setup.automation.AutomationSetupModule$state$1#invokeSuspend",
    "eu.darken.sdmse.setup.automation.AutomationToolsHelperKt#mightBeRestrictedDueToSideload",
    "res/values/strings.xml（setup_acs_card_* / setup_acs_consent_* / setup_acs_appops_restriction_*）",
    "res/xml/accessibility_service.xml"
  ]
}
```

补充说明（覆盖边界）：本轮未启动动态分析，UTG 页面流转结论基于静态代码与资源；`AutomationSetupModule$state$1#invokeSuspend` 中 `ACCESSIBILITY_SETTINGS` Intent 的实际发起位置与 `canSelfEnable`（依赖已授予 `WRITE_SECURE_SETTINGS`，即 root/ADB 通道）分支的具体组合，因 R8 混淆与 JADX 结构化失败未逐指令确认，但不影响“同意后才跳转、可拒绝、无循环”的判定。未发现需要登记的风险命题。

</details>
