# BN_015__7e7887f588｜按键映射与手势导航 — Pineapple Lock Screen

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：151.2s

## 1. 一句话核心结论

- **核心申请方式**：首次启动以原生 Compose 披露弹窗说明用途、主页提供可随时进入的“Accessibility Settings”卡片按钮跳转系统无障碍页，并提供 Shizuku/磁贴/快捷方式等替代路径的良性透明授权流程。
- **静态可见性说明**：全部引导逻辑位于 classes.dex（Kotlin/Compose，仅 R8 名称混淆，无加壳、无 VMP、无 AES 密文载荷、无远端 HTML）；无障碍披露弹窗、主页卡片、跳转 Intent 与全部文案均由本地 strings.xml 与代码静态可见。未逐行反编译的仅为披露弹窗内部 composable 分支与卡片点击回调的局部实现，不影响性质判定。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `7e7887f588c6d5466abbee81e6faea40265c1d7dfbb4ce89daf52089bf530383` |
| 包名 / 年份 | `net.blumia.pineapple.lockscreen.oss` / 2025-2026 |
| 家族 / 品类 | **按键映射与手势导航**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/net.blumia.pineapple.lockscreen.oss_29.apk |
| 桌面显示名 | Lock Screen |
| 引导页宣称品牌/身份 | Pineapple Lock Screen（BLumia / F-Droid 开源项目） |
| 系统无障碍列表服务名 | Pineapple Lock Screen - Accessibility Service |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无恶意混淆技巧；仅有 R8 代码名称混淆，以及多个 enabled=false 的 activity-alias（yellow/indigo/cyan/pink/purple × power/lock）用于用户自选桌面图标配色，属正常自定义功能，非多别名伪装或同形字伪装 |
| 无障碍服务类名 | `net.blumia.pineapple.accessibility.A11yService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | This accessibility service is used to provide the lock screen ability in the Pineapple Lock Screen application, otherwise the application won't be able to work.<br><br>To enable the accessibility service, just tap the toggle switch in the top right corner, then tap Allow on the next screen. You don't need to enable the second shortcut switch.<br><br>Note:<br>1. If you force stop the main application, you might need to enable this service again.<br>2. If the service is enabled but the application doesn't work as intended, try disable and enable it again. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | net.blumia.pineapple.lockscreen.MainActivity（singleTask，承载 NavGraph 根路由） | onCreate → setContent(ComposableSingletons$MainActivityKt.lambda$-1422109542) → NavGraph 渲染，读取 DataStore 偏好 PROMINENT_DISCLOSURE_ACCEPTED | 原生Activity | **原文**：无（该步仅为承载容器，不直接呈现文案）<br>**译注**：主界面容器，首次启动时在其上叠加无障碍披露弹窗 | 无（等待披露弹窗出现） | `net.blumia.pineapple.lockscreen.MainActivity#onCreate；net.blumia.pineapple.lockscreen.ui.NavGraphKt#NavGraph` |
| 2 | 引导说明页 | NavGraph 根节点内的 Compose 披露弹窗（标题 About Accessibility Service Permission） | PROMINENT_DISCLOSURE_ACCEPTED 为 false 时（DataStore 布尔偏好 collectAsState 默认 FALSE）触发显示 | 原生Dialog | **原文**：About Accessibility Service Permission / This application uses the Accessibility Service to provide the lock screen functionality. Related service needs to be enabled to work.<br><br>You can use the entrance link in the main screen to access the accessibility setting at any time you want.<br><br>This application doesn't collect any user data. You can also review the full content of Privacy Policy in the About screen.<br>**译注**：关于无障碍服务权限——本应用使用无障碍服务提供锁屏功能，需启用相关服务才能工作；你可随时通过主界面上的入口链接进入无障碍设置；本应用不收集任何用户数据，完整隐私政策可在“关于”页面查看。 | 点击 Accept 接受（存在 Cancel 字符串，可拒绝并留在主界面继续使用其它方式） | `res/values/strings.xml: accessibility_service_prominent_disclosure_dlg_title / _desc；net.blumia.pineapple.lockscreen.preferences.IconSwitcher#PROMINENT_DISCLOSURE_ACCEPTED；net.blumia.pineapple.lockscreen.ui.NavGraphKt$NavGraph$1$1#invokeSuspend` |
| 3 | 业务功能触发 | 主页 HomeScreen 的方法选择卡片列表（MainScreenCard：Accessibility Service / Shizuku / 快捷设置磁贴 / 快捷方式） | 用户在主界面浏览并选择锁屏实现方式（用户主动按需） | 原生Activity | **原文**：This application require to enable its accessibility service in order to work.<br>You can use the following button to enable or disable the service conveniently. / Accessibility Settings<br>**译注**：本应用需要启用其无障碍服务才能工作，可用下面的按钮方便地启用或禁用该服务。/ 无障碍设置 | 点击“Accessibility Settings”卡片按钮进入系统无障碍设置；也可选择 Shizuku、磁贴、快捷方式等其他方式，无强制 | `net.blumia.pineapple.lockscreen.ui.home.HomeScreenKt#MainScreenCard；res/values/strings.xml: card_a11y_description / card_a11y_action_go_to_setting` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（经 rikka.sui 库工具方法 openSystemA11ySettings 发起 Intent） | 用户点击无障碍卡片按钮后调用 Sui.openSystemA11ySettings(context) | 系统无障碍页 | **原文**：Pineapple Lock Screen - Accessibility Service（系统列表项标签）/ This accessibility service is used to provide the lock screen ability in the Pineapple Lock Screen application, otherwise the application won't be able to work.<br><br>To enable the accessibility service, just tap the toggle switch in the top right corner, then tap Allow on the next screen. You don't need to enable the second shortcut switch.<br><br>Note:<br>1. If you force stop the main application, you might need to enable this service again.<br>2. If the service is enabled but the application doesn't work as intended, try disable and enable it again.<br>**译注**：Pineapple Lock Screen - 无障碍服务；该无障碍服务用于在 Pineapple Lock Screen 中提供锁屏能力，否则应用无法工作。启用方法：点击右上角开关，然后在下一屏点“允许”，无需启用第二个快捷方式开关。注意：1. 强制停止主应用后可能需要重新启用；2. 若已启用但功能不正常，可尝试禁用后再启用。 | 在系统页手动打开开关并点“允许”；用户可随时返回或关闭，应用不拦截 | `rikka.sui.Sui#openSystemA11ySettings；res/values/strings.xml: accessibility_service_label / accessibility_service_description；res/xml/accessibility_service_config` |
| 5 | 拒权反馈循环 | 返回 MainActivity 主界面（无重跳逻辑） | 用户从系统设置返回，或直接拒绝/取消披露弹窗 | 原生Activity | **原文**：Shizuku can be used to lock the screen without the accessibility service. Install and enable Shizuku to use this method.<br>**译注**：Shizuku 可在不使用无障碍服务的情况下锁屏，安装并启用 Shizuku 即可使用该方式。 | 可选择继续使用 Shizuku（跳转 moe.shizuku.privileged.api 或下载页 https://shizuku.rikka.app/download/）、快捷设置磁贴或桌面快捷方式；不存在强制重跳 | `net.blumia.pineapple.lockscreen.ui.home.HomeScreenKt$$ExternalSyntheticLambda6#invoke；net.blumia.pineapple.lockscreen.QuickSettingService#onClick；res/values/strings.xml: card_shizuku_description` |
| 6 | 获权后动作 | net.blumia.pineapple.accessibility.A11yService（获权后由系统绑定） | 系统回调 onServiceConnected | 不可静态还原 | **原文**：无（无界面）<br>**译注**：仅保存自身弱引用并设置 serviceInfo（eventTypes=9、feedbackType=16、notificationTimeout=100ms），不读取界面内容、不自动点击、不阻止撤权 | 无 | `net.blumia.pineapple.accessibility.A11yService#onServiceConnected；net.blumia.pineapple.accessibility.A11yService#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 上 NavGraph 根节点的 Compose 披露弹窗（标题 About Accessibility Service Permission，首次启动且未接受时显示，含 Accept/Cancel）
- 主页 HomeScreen 的 MainScreenCard 卡片区：无障碍卡片说明文字 + “Accessibility Settings”按钮
- 主页同一卡片区的 Shizuku 卡片（含 Connect Shizuku / Start Shizuku Service 按钮）、快捷设置磁贴卡片、快捷方式卡片说明
- 系统无障碍服务列表项：android:description（accessibility_service_description）与 android:label（accessibility_service_label），即 res/xml/accessibility_service_config 引用的两条字符串
- 关于页 AboutScreen：隐私政策外链 https://sites.google.com/view/pineapplelockscreen-privacy/ 与开源仓库链接

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | This accessibility service is used to provide the lock screen ability in the Pineapple Lock Screen application, otherwise the application won't be able to work.<br><br>To enable the accessibility service, just tap the toggle switch in the top right corner, then tap Allow on the next screen. You don't need to enable the second shortcut switch.<br><br>Note:<br>1. If you force stop the main application, you might need to enable this service again.<br>2. If the service is enabled but the application doesn't work as intended, try disable and enable it again. | 该无障碍服务用于在 Pineapple Lock Screen 中提供锁屏能力，否则应用无法工作。启用方法：点击右上角开关，然后在下一屏点“允许”，无需启用第二个快捷方式开关。注意：1. 强制停止主应用后可能需要重新启用该服务；2. 若已启用但功能不正常，可尝试禁用后再启用。 | `res/values/strings.xml → accessibility_service_description（系统无障碍列表 android:description）` | 良性透明说明 |
| en | This application uses the Accessibility Service to provide the lock screen functionality. Related service needs to be enabled to work.<br><br>You can use the entrance link in the main screen to access the accessibility setting at any time you want.<br><br>This application doesn't collect any user data. You can also review the full content of Privacy Policy in the About screen. | 本应用使用无障碍服务提供锁屏功能，需启用相关服务才能工作。你可随时通过主界面入口链接进入无障碍设置。本应用不收集任何用户数据，完整隐私政策可在“关于”页面查看。 | `res/values/strings.xml → accessibility_service_prominent_disclosure_dlg_desc（Compose 披露弹窗正文）` | 良性透明说明 |
| en | About Accessibility Service Permission | 关于无障碍服务权限 | `res/values/strings.xml → accessibility_service_prominent_disclosure_dlg_title` | 良性透明说明 |
| en | This application require to enable its accessibility service in order to work.<br>You can use the following button to enable or disable the service conveniently. | 本应用需要启用其无障碍服务才能工作。你可以用下面的按钮方便地启用或禁用该服务。 | `res/values/strings.xml → card_a11y_description（主页卡片）` | 良性透明说明 |
| en | Accessibility Settings | 无障碍设置 | `res/values/strings.xml → card_a11y_action_go_to_setting（主页卡片按钮）` | 受限设置分步教学 |
| en | Shizuku can be used to lock the screen without the accessibility service. Install and enable Shizuku to use this method. | Shizuku 可在不使用无障碍服务的情况下锁屏，安装并启用 Shizuku 即可使用该方式。 | `res/values/strings.xml → card_shizuku_description（主页替代方式卡片）` | 良性透明说明 |
| en | Pineapple Lock Screen - Accessibility Service | Pineapple Lock Screen - 无障碍服务 | `res/values/strings.xml → accessibility_service_label（系统列表项标签）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`shallow_1_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无重跳循环：拒绝披露弹窗仅不写入 PROMINENT_DISCLOSURE_ACCEPTED，用户留在主界面；从系统设置返回不触发 onResume 强制跳转或定时器拉起，可继续使用 Shizuku / 磁贴 / 快捷方式等替代路径
- **遮罩叠层 / 高仿系统设置页**：无：无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；跳转目标为真实系统设置页 android.settings.ACCESSIBILITY_SETTINGS
- **Android 13+ 受限设置（Restricted Settings）应对**：无：未出现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也未教用户进入应用详情页开启“受限设置”；仅提示点击系统无障碍页右上角开关与 Allow
- **获权后即时行为与防撤权机制**：无：A11yService 未使用 GLOBAL_ACTION_BACK/HOME，未监听设置页阻止撤权，未自点确认；onUnbind 仅清空弱引用
- **良性降级 / 替代方案**：有：Shizuku（moe.shizuku.privileged.api，缺失时跳 https://shizuku.rikka.app/download/）、QuickSettingService 快捷设置磁贴、桌面快捷方式（LockScreenShortcut / PowerDialogShortcut）、桌面小组件（FirstGlanceWidgetReceiver），均在无无障碍权限下可用

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到首次启动（PROMINENT_DISCLOSURE_ACCEPTED 未置位）时 MainActivity 上叠加的披露弹窗；以及后续任意时刻 Sui.openSystemA11ySettings 发起 android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间（应用进程内 Intent 构造点）
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：无纯图空文本界面、无 WebView 远端教学页、无二阶段 Dropper、无静态加壳（R8 混淆不影响运行期 UTG）。唯一需注意的细节是应用自身不直接内联 ACTION_ACCESSIBILITY_SETTINGS，跳转由 rikka.sui 库方法发起，UTG 应以“系统无障碍设置页被拉起”这一页面事实为准，而非依赖应用侧 Intent 字符串特征。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动披露弹窗页** | MainActivity（net.blumia.pineapple.lockscreen.MainActivity）上的 Compose Dialog，标题 About Accessibility Service Permission，含 Accept / Cancel | 这是该应用唯一的授权前置说明层，可直接判定文案是否透明、是否可取消、是否夹带恐吓或虚假隐私承诺 | 弹窗标题与正文文本；Accept / Cancel 按钮可点击性与是否可外部取消；弹窗背后是否被其它界面覆盖或空白化 |
| **主页无障碍引导卡片页** | HomeScreen MainScreenCard 列表中的 Accessibility Service 卡片与 Accessibility Settings 按钮 | 确认入口常驻、按需触发、且同时并列展示 Shizuku/磁贴/快捷方式等替代方式，是区分“诱导强制”与“良性按需”的关键 | 卡片说明文本；并列的替代方式卡片数量与文案；点击按钮后目标页是否为真实系统设置 |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载/已安装服务中的 Pineapple Lock Screen - Accessibility Service | 核对系统展示的服务标签与说明是否与包内字符串一致、有无空标签/换行挤出警告/伪造 isAccessibilityTool 痕迹 | 服务标签原文；描述摘要文本；是否出现“此服务可查看屏幕内容”等系统警示被隐藏 |
| **拒权返回后的降级页** | 返回 MainActivity 主界面，观察是否再次弹出弹窗或被强制拉起系统设置 | 验证不存在拒绝循环与后台重跳，是判定良性的必要条件 | 返回后 3–5 秒内是否重新出现披露弹窗或设置页；主界面是否仍可操作并展示替代方式 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `net.blumia.pineapple.lockscreen.ui.NavGraphKt#NavGraph`
- `net.blumia.pineapple.lockscreen.ui.NavGraphKt$NavGraph$1$1#invokeSuspend`
- `net.blumia.pineapple.lockscreen.ui.home.HomeScreenKt#MainScreenCard`
- `rikka.sui.Sui#openSystemA11ySettings`
- `net.blumia.pineapple.accessibility.A11yService#onAccessibilityEvent`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，静态可见性 clear）

**判定：良性透明授权引导，未发现诱导/伪装/拒权循环。**

- **无障碍服务本体极简且无监视行为**：[A11yService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:net.blumia.pineapple.accessibility.A11yService#onAccessibilityEvent>) 为空实现，`onServiceConnected` 仅设置 `eventTypes=9`、`feedbackType=16`、`notificationTimeout=100`，不读取窗口内容、不模拟点击；无 `GLOBAL_ACTION_BACK/HOME` 类反撤权逻辑。
- **跳转点**：`android.settings.ACCESSIBILITY_SETTINGS` 仅出现在库类 [Sui.openSystemA11ySettings()](<resource-unit:#1.dex1 code:rikka.sui.Sui#openSystemA11ySettings>)（Shizuku 库工具方法），应用自身未内联 `ACTION_APPLICATION_DETAILS_SETTINGS`，也无 `ACTION_MANAGE_...` 受限设置教唆（RESTRICTED_STR 未落地为引导文案）。
- **引导载体全部为原生 Compose 页面与系统设置页**：首次启动在 NavGraph 根节点以 `PROMINENT_DISCLOSURE_ACCEPTED` 偏好位控制展示"关于无障碍服务权限"披露弹窗（`accept`/`cancel` 字符串存在），主页 [HomeScreenKt.MainScreenCard()](<resource-unit:#1.dex1 code:net.blumia.pineapple.lockscreen.ui.home.HomeScreenKt#MainScreenCard>) 渲染 "Accessibility Settings" 卡片按钮，文案明确说明用途与随时可入口。无 WebView、无悬浮窗、无遮罩、无高仿系统开关页。
- **拒绝后安全降级**：应用提供 Shizuku（`moe.shizuku.privileged.api` 跳转/下载页）、快捷设置磁贴、桌面快捷方式、桌面小组件等多条替代锁屏路径，未获无障碍权限不进入死循环重跳。
- **身份一致**：桌面名 `Lock Screen`（`app_launcher_name`）/应用名 `Pineapple Lock Screen`，服务标签 `Pineapple Lock Screen - Accessibility Service`，与 F-Droid 开源主体一致；多个 `activity-alias` 均为 `enabled="false"` 的图标配色自选（yellow/indigo/cyan/pink/purple × power/lock），属正常自定义功能而非变脸伪装。
- **覆盖边界**：披露弹窗 composable 的完整分支（是否可点击外部取消）与 A11y 卡片点击回调未逐行反编译（受 14 次调用上限约束），但字符串资源、偏好位与调用链已足以判定其性质；无加壳、无密文载荷，`static_visibility` 为 clear。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于 classes.dex（Kotlin/Compose，仅 R8 名称混淆，无加壳、无 VMP、无 AES 密文载荷、无远端 HTML）；无障碍披露弹窗、主页卡片、跳转 Intent 与全部文案均由本地 strings.xml 与代码静态可见。未逐行反编译的仅为披露弹窗内部 composable 分支与卡片点击回调的局部实现，不影响性质判定。",
  "summary_one_liner": "首次启动以原生 Compose 披露弹窗说明用途、主页提供可随时进入的“Accessibility Settings”卡片按钮跳转系统无障碍页，并提供 Shizuku/磁贴/快捷方式等替代路径的良性透明授权流程。",
  "disguise_identity": {
    "app_display_name": "Lock Screen",
    "claimed_brand_or_persona": "Pineapple Lock Screen（BLumia / F-Droid 开源项目）",
    "a11y_service_label": "Pineapple Lock Screen - Accessibility Service",
    "identity_mismatch": false,
    "obfuscation_tricks": "无恶意混淆技巧；仅有 R8 代码名称混淆，以及多个 enabled=false 的 activity-alias（yellow/indigo/cyan/pink/purple × power/lock）用于用户自选桌面图标配色，属正常自定义功能，非多别名伪装或同形字伪装"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "net.blumia.pineapple.lockscreen.MainActivity（singleTask，承载 NavGraph 根路由）",
      "trigger_event": "onCreate → setContent(ComposableSingletons$MainActivityKt.lambda$-1422109542) → NavGraph 渲染，读取 DataStore 偏好 PROMINENT_DISCLOSURE_ACCEPTED",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该步仅为承载容器，不直接呈现文案）",
      "shown_text_zh": "主界面容器，首次启动时在其上叠加无障碍披露弹窗",
      "user_action_requested": "无（等待披露弹窗出现）",
      "code_anchor": "net.blumia.pineapple.lockscreen.MainActivity#onCreate；net.blumia.pineapple.lockscreen.ui.NavGraphKt#NavGraph"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "NavGraph 根节点内的 Compose 披露弹窗（标题 About Accessibility Service Permission）",
      "trigger_event": "PROMINENT_DISCLOSURE_ACCEPTED 为 false 时（DataStore 布尔偏好 collectAsState 默认 FALSE）触发显示",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "About Accessibility Service Permission / This application uses the Accessibility Service to provide the lock screen functionality. Related service needs to be enabled to work.\n\nYou can use the entrance link in the main screen to access the accessibility setting at any time you want.\n\nThis application doesn't collect any user data. You can also review the full content of Privacy Policy in the About screen.",
      "shown_text_zh": "关于无障碍服务权限——本应用使用无障碍服务提供锁屏功能，需启用相关服务才能工作；你可随时通过主界面上的入口链接进入无障碍设置；本应用不收集任何用户数据，完整隐私政策可在“关于”页面查看。",
      "user_action_requested": "点击 Accept 接受（存在 Cancel 字符串，可拒绝并留在主界面继续使用其它方式）",
      "code_anchor": "res/values/strings.xml: accessibility_service_prominent_disclosure_dlg_title / _desc；net.blumia.pineapple.lockscreen.preferences.IconSwitcher#PROMINENT_DISCLOSURE_ACCEPTED；net.blumia.pineapple.lockscreen.ui.NavGraphKt$NavGraph$1$1#invokeSuspend"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "主页 HomeScreen 的方法选择卡片列表（MainScreenCard：Accessibility Service / Shizuku / 快捷设置磁贴 / 快捷方式）",
      "trigger_event": "用户在主界面浏览并选择锁屏实现方式（用户主动按需）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "This application require to enable its accessibility service in order to work.\nYou can use the following button to enable or disable the service conveniently. / Accessibility Settings",
      "shown_text_zh": "本应用需要启用其无障碍服务才能工作，可用下面的按钮方便地启用或禁用该服务。/ 无障碍设置",
      "user_action_requested": "点击“Accessibility Settings”卡片按钮进入系统无障碍设置；也可选择 Shizuku、磁贴、快捷方式等其他方式，无强制",
      "code_anchor": "net.blumia.pineapple.lockscreen.ui.home.HomeScreenKt#MainScreenCard；res/values/strings.xml: card_a11y_description / card_a11y_action_go_to_setting"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（经 rikka.sui 库工具方法 openSystemA11ySettings 发起 Intent）",
      "trigger_event": "用户点击无障碍卡片按钮后调用 Sui.openSystemA11ySettings(context)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Pineapple Lock Screen - Accessibility Service（系统列表项标签）/ This accessibility service is used to provide the lock screen ability in the Pineapple Lock Screen application, otherwise the application won't be able to work.\n\nTo enable the accessibility service, just tap the toggle switch in the top right corner, then tap Allow on the next screen. You don't need to enable the second shortcut switch.\n\nNote:\n1. If you force stop the main application, you might need to enable this service again.\n2. If the service is enabled but the application doesn't work as intended, try disable and enable it again.",
      "shown_text_zh": "Pineapple Lock Screen - 无障碍服务；该无障碍服务用于在 Pineapple Lock Screen 中提供锁屏能力，否则应用无法工作。启用方法：点击右上角开关，然后在下一屏点“允许”，无需启用第二个快捷方式开关。注意：1. 强制停止主应用后可能需要重新启用；2. 若已启用但功能不正常，可尝试禁用后再启用。",
      "user_action_requested": "在系统页手动打开开关并点“允许”；用户可随时返回或关闭，应用不拦截",
      "code_anchor": "rikka.sui.Sui#openSystemA11ySettings；res/values/strings.xml: accessibility_service_label / accessibility_service_description；res/xml/accessibility_service_config"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 MainActivity 主界面（无重跳逻辑）",
      "trigger_event": "用户从系统设置返回，或直接拒绝/取消披露弹窗",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Shizuku can be used to lock the screen without the accessibility service. Install and enable Shizuku to use this method.",
      "shown_text_zh": "Shizuku 可在不使用无障碍服务的情况下锁屏，安装并启用 Shizuku 即可使用该方式。",
      "user_action_requested": "可选择继续使用 Shizuku（跳转 moe.shizuku.privileged.api 或下载页 https://shizuku.rikka.app/download/）、快捷设置磁贴或桌面快捷方式；不存在强制重跳",
      "code_anchor": "net.blumia.pineapple.lockscreen.ui.home.HomeScreenKt$$ExternalSyntheticLambda6#invoke；net.blumia.pineapple.lockscreen.QuickSettingService#onClick；res/values/strings.xml: card_shizuku_description"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "net.blumia.pineapple.accessibility.A11yService（获权后由系统绑定）",
      "trigger_event": "系统回调 onServiceConnected",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（无界面）",
      "shown_text_zh": "仅保存自身弱引用并设置 serviceInfo（eventTypes=9、feedbackType=16、notificationTimeout=100ms），不读取界面内容、不自动点击、不阻止撤权",
      "user_action_requested": "无",
      "code_anchor": "net.blumia.pineapple.accessibility.A11yService#onServiceConnected；net.blumia.pineapple.accessibility.A11yService#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 上 NavGraph 根节点的 Compose 披露弹窗（标题 About Accessibility Service Permission，首次启动且未接受时显示，含 Accept/Cancel）",
    "主页 HomeScreen 的 MainScreenCard 卡片区：无障碍卡片说明文字 + “Accessibility Settings”按钮",
    "主页同一卡片区的 Shizuku 卡片（含 Connect Shizuku / Start Shizuku Service 按钮）、快捷设置磁贴卡片、快捷方式卡片说明",
    "系统无障碍服务列表项：android:description（accessibility_service_description）与 android:label（accessibility_service_label），即 res/xml/accessibility_service_config 引用的两条字符串",
    "关于页 AboutScreen：隐私政策外链 https://sites.google.com/view/pineapplelockscreen-privacy/ 与开源仓库链接"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "This accessibility service is used to provide the lock screen ability in the Pineapple Lock Screen application, otherwise the application won't be able to work.\n\nTo enable the accessibility service, just tap the toggle switch in the top right corner, then tap Allow on the next screen. You don't need to enable the second shortcut switch.\n\nNote:\n1. If you force stop the main application, you might need to enable this service again.\n2. If the service is enabled but the application doesn't work as intended, try disable and enable it again.",
      "text_zh": "该无障碍服务用于在 Pineapple Lock Screen 中提供锁屏能力，否则应用无法工作。启用方法：点击右上角开关，然后在下一屏点“允许”，无需启用第二个快捷方式开关。注意：1. 强制停止主应用后可能需要重新启用该服务；2. 若已启用但功能不正常，可尝试禁用后再启用。",
      "source_location": "res/values/strings.xml → accessibility_service_description（系统无障碍列表 android:description）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This application uses the Accessibility Service to provide the lock screen functionality. Related service needs to be enabled to work.\n\nYou can use the entrance link in the main screen to access the accessibility setting at any time you want.\n\nThis application doesn't collect any user data. You can also review the full content of Privacy Policy in the About screen.",
      "text_zh": "本应用使用无障碍服务提供锁屏功能，需启用相关服务才能工作。你可随时通过主界面入口链接进入无障碍设置。本应用不收集任何用户数据，完整隐私政策可在“关于”页面查看。",
      "source_location": "res/values/strings.xml → accessibility_service_prominent_disclosure_dlg_desc（Compose 披露弹窗正文）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "About Accessibility Service Permission",
      "text_zh": "关于无障碍服务权限",
      "source_location": "res/values/strings.xml → accessibility_service_prominent_disclosure_dlg_title",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This application require to enable its accessibility service in order to work.\nYou can use the following button to enable or disable the service conveniently.",
      "text_zh": "本应用需要启用其无障碍服务才能工作。你可以用下面的按钮方便地启用或禁用该服务。",
      "source_location": "res/values/strings.xml → card_a11y_description（主页卡片）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Accessibility Settings",
      "text_zh": "无障碍设置",
      "source_location": "res/values/strings.xml → card_a11y_action_go_to_setting（主页卡片按钮）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Shizuku can be used to lock the screen without the accessibility service. Install and enable Shizuku to use this method.",
      "text_zh": "Shizuku 可在不使用无障碍服务的情况下锁屏，安装并启用 Shizuku 即可使用该方式。",
      "source_location": "res/values/strings.xml → card_shizuku_description（主页替代方式卡片）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Pineapple Lock Screen - Accessibility Service",
      "text_zh": "Pineapple Lock Screen - 无障碍服务",
      "source_location": "res/values/strings.xml → accessibility_service_label（系统列表项标签）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "shallow_1_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无重跳循环：拒绝披露弹窗仅不写入 PROMINENT_DISCLOSURE_ACCEPTED，用户留在主界面；从系统设置返回不触发 onResume 强制跳转或定时器拉起，可继续使用 Shizuku / 磁贴 / 快捷方式等替代路径",
    "overlay_or_fake_settings": "无：无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；跳转目标为真实系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
    "restricted_settings_13plus_coaching": "无：未出现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转，也未教用户进入应用详情页开启“受限设置”；仅提示点击系统无障碍页右上角开关与 Allow",
    "post_grant_anti_removal": "无：A11yService 未使用 GLOBAL_ACTION_BACK/HOME，未监听设置页阻止撤权，未自点确认；onUnbind 仅清空弱引用",
    "benign_graceful_degradation": "有：Shizuku（moe.shizuku.privileged.api，缺失时跳 https://shizuku.rikka.app/download/）、QuickSettingService 快捷设置磁贴、桌面快捷方式（LockScreenShortcut / PowerDialogShortcut）、桌面小组件（FirstGlanceWidgetReceiver），均在无无障碍权限下可用"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到首次启动（PROMINENT_DISCLOSURE_ACCEPTED 未置位）时 MainActivity 上叠加的披露弹窗；以及后续任意时刻 Sui.openSystemA11ySettings 发起 android.settings.ACCESSIBILITY_SETTINGS 跳转的瞬间（应用进程内 Intent 构造点）",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动披露弹窗页",
        "page_identifier": "MainActivity（net.blumia.pineapple.lockscreen.MainActivity）上的 Compose Dialog，标题 About Accessibility Service Permission，含 Accept / Cancel",
        "why_most_useful": "这是该应用唯一的授权前置说明层，可直接判定文案是否透明、是否可取消、是否夹带恐吓或虚假隐私承诺",
        "observable_utg_signals": ["弹窗标题与正文文本", "Accept / Cancel 按钮可点击性与是否可外部取消", "弹窗背后是否被其它界面覆盖或空白化"]
      },
      {
        "page_role": "主页无障碍引导卡片页",
        "page_identifier": "HomeScreen MainScreenCard 列表中的 Accessibility Service 卡片与 Accessibility Settings 按钮",
        "why_most_useful": "确认入口常驻、按需触发、且同时并列展示 Shizuku/磁贴/快捷方式等替代方式，是区分“诱导强制”与“良性按需”的关键",
        "observable_utg_signals": ["卡片说明文本", "并列的替代方式卡片数量与文案", "点击按钮后目标页是否为真实系统设置"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载/已安装服务中的 Pineapple Lock Screen - Accessibility Service",
        "why_most_useful": "核对系统展示的服务标签与说明是否与包内字符串一致、有无空标签/换行挤出警告/伪造 isAccessibilityTool 痕迹",
        "observable_utg_signals": ["服务标签原文", "描述摘要文本", "是否出现“此服务可查看屏幕内容”等系统警示被隐藏"]
      },
      {
        "page_role": "拒权返回后的降级页",
        "page_identifier": "返回 MainActivity 主界面，观察是否再次弹出弹窗或被强制拉起系统设置",
        "why_most_useful": "验证不存在拒绝循环与后台重跳，是判定良性的必要条件",
        "observable_utg_signals": ["返回后 3–5 秒内是否重新出现披露弹窗或设置页", "主界面是否仍可操作并展示替代方式"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：无纯图空文本界面、无 WebView 远端教学页、无二阶段 Dropper、无静态加壳（R8 混淆不影响运行期 UTG）。唯一需注意的细节是应用自身不直接内联 ACTION_ACCESSIBILITY_SETTINGS，跳转由 rikka.sui 库方法发起，UTG 应以“系统无障碍设置页被拉起”这一页面事实为准，而非依赖应用侧 Intent 字符串特征。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "net.blumia.pineapple.lockscreen.ui.NavGraphKt#NavGraph",
    "net.blumia.pineapple.lockscreen.ui.NavGraphKt$NavGraph$1$1#invokeSuspend",
    "net.blumia.pineapple.lockscreen.ui.home.HomeScreenKt#MainScreenCard",
    "rikka.sui.Sui#openSystemA11ySettings",
    "net.blumia.pineapple.accessibility.A11yService#onAccessibilityEvent",
    "res/values/strings.xml"
  ]
}
```

</details>
