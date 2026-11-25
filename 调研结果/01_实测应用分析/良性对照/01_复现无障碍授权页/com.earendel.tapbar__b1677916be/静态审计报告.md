# BN_010__b1677916be｜按键映射与手势导航 — Tapbar

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：189.8s

## 1. 一句话核心结论

- **核心申请方式**：Tapbar 通过设置页内的“Setup Tapbar”权限清单按需引导用户点击跳转系统无障碍列表（并高亮定位自身服务条目），配合 Android 13+ 官方“允许受限设置”文字教学，并提供悬浮窗降级与“跳过”选项，全程无强制、无循环重跳。
- **静态可见性说明**：全部引导逻辑位于 DEX 与本地资源中：Compose 原生权限页（strings.xml 的 permissions_title/perm_* 系列）+ ac0.a() 的显式 Intent 跳转；无 WebView、无远端 HTML、无加壳或加密载荷，静态完整可见。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b1677916be25a0c143ff8c8cde44760c1f61a94104281558f046e6d09191aad7` |
| 包名 / 年份 | `com.earendel.tapbar` / 2025-2026 |
| 家族 / 品类 | **按键映射与手势导航**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.earendel.tapbar_13.apk |
| 桌面显示名 | Tapbar |
| 引导页宣称品牌/身份 | Tapbar / Earendel（F-Droid 开源按键映射工具，tagline: 100% Offline • Zero Trackers • Open Source） |
| 系统无障碍列表服务名 | Tapbar |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无 |
| 无障碍服务类名 | `com.earendel.tapbar.TapAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Lets Tapbar place a small tap target on the status bar. It does not read screen content. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.earendel.tapbar.MainActivity（Compose 主界面） | onCreate / onResume | 原生Activity | **原文**：Setup Tapbar<br>**译注**：配置 Tapbar（权限清单页标题，用户主动点入后才展示） | 无强制操作；冷启动不弹授权弹窗，可正常浏览主界面 | `com.earendel.tapbar.MainActivity.onCreate / onResume；res/values/strings.xml permissions_title` |
| 2 | 引导说明页 | Setup Tapbar 权限清单页（Compose，含 Accessibility service / Display over other apps 两项） | 用户在主界面/设置入口点开权限配置 | 原生Activity | **原文**：Accessibility service — Lets the tap zone sit directly on the status bar. It does not read or send any screen text. \| Turn on \| Fallback \| Recommended \| Skip for now<br>**译注**：无障碍服务——让点击区直接位于状态栏上，不读取也不发送任何屏幕文字。｜开启｜替代方案｜推荐｜暂时跳过 | 可选择“Turn on”开启无障碍，或选择“Fallback/跳过”使用悬浮窗替代方案；存在取消/跳过入口 | `res/values/strings.xml perm_accessibility_title / perm_accessibility_desc / perm_allow / perm_fallback / skip_for_now / perm_recommended` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（部分路径带 :settings:fragment_args_key 高亮 TapAccessibilityService 条目） | 点击“Turn on accessibility service”按钮 | 系统无障碍页 | **原文**：Turn on accessibility service<br>**译注**：开启无障碍服务 | 在系统无障碍列表中手动找到 Tapbar 并开启开关；用户可随时返回 | `ac0.a() case 1 / case 6；strings.xml turn_on_accessibility` |
| 4 | 跳受限设置 | 系统设置页 android.settings.APPLICATION_DETAILS_SETTINGS（package:com.earendel.tapbar） | 开关置灰时点击帮助入口，触发 ac0.a() case 2 | 系统无障碍页 | **原文**：If the accessibility switch is greyed out: Open App info, tap the three-dot menu at the top right, choose Allow restricted settings, then try again.<br>**译注**：如果无障碍开关是灰色的：打开应用信息，点右上角三点菜单，选择“允许受限设置”，然后重试。 | 按官方路径进入应用详情页并允许受限设置（Android 13+ 侧载应用的系统要求，非绕过手段） | `res/values/strings.xml restricted_help_title / restricted_help_text；ac0.a() case 2` |
| 5 | 拒权反馈循环 | MainActivity / Setup 页状态刷新 | 从系统设置返回后 onResume | 原生Activity | **原文**：The tap zone sits below the status bar. You can enable accessibility later in Settings.<br>**译注**：点击区位于状态栏下方。你可以稍后在设置中开启无障碍。 | 无强制重跳；用户可继续使用悬浮窗替代模式 | `com.earendel.tapbar.MainActivity.onResume；strings.xml success_desc_overlay / perm_overlay_desc` |
| 6 | 获权后动作 | com.earendel.tapbar.TapAccessibilityService（onServiceConnected） | 系统绑定无障碍服务回调 | 原生Activity | **原文**：The tap zone sits directly on the status bar. / You're all set<br>**译注**：点击区直接位于状态栏上。／已全部设置完成。 | 无额外操作；服务仅注册浮窗控制器并停止 OverlayService，无自点确认或阻止撤权行为 | `com.earendel.tapbar.TapAccessibilityService.onServiceConnected；strings.xml success_desc_a11y / success_title` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 内的 Compose“Setup Tapbar”权限清单页（原生渲染，非 WebView/HTML），条目文字来自 res/values/strings.xml 的 perm_accessibility_title / perm_accessibility_desc / perm_overlay_title / perm_overlay_desc
- 按钮文案 perm_allow（Turn on）、perm_fallback（Fallback）、skip_for_now（Skip for now）同处该 Compose 页面
- 系统无障碍列表条目说明：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_desc（"Lets Tapbar place a small tap target on the status bar. It does not read screen content."）
- 受限设置帮助区块：strings.xml restricted_help_title / restricted_help_text，展示在设置页/权限页内，点击跳 APPLICATION_DETAILS_SETTINGS
- 成功态文案 success_title（You're all set）、success_desc_a11y、success_desc_overlay 展示在权限页完成状态
- 关于页（h70.n 构建的 Compose About 列表）：版本号、Earendel、GitHub、源码与 LICENSE 链接，跳转 github.com/Earendel-lab/Tapbar

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Lets Tapbar place a small tap target on the status bar. It does not read screen content. | 允许 Tapbar 在状态栏上放置一个小型点击目标。它不会读取屏幕内容。 | `res/values/strings.xml key=accessibility_desc（系统无障碍列表说明）` | 良性透明说明 |
| en | Without the accessibility service, Android places the zone below the status bar and the system takes those taps. Turn the service on to place the zone directly on the status bar. | 未开启无障碍服务时，Android 会把点击区放在状态栏下方，系统会接管这些点击。开启服务后即可把点击区直接放在状态栏上。 | `res/values/strings.xml key=accessibility_service_body（含 de/es/fr/hi/ja/ko/ne/pt/ru/tr/zh 多语言版本）` | 良性透明说明 |
| en | Lets the tap zone sit directly on the status bar. It does not read or send any screen text. | 让点击区直接位于状态栏上。它不会读取或发送任何屏幕文字。 | `res/values/strings.xml key=perm_accessibility_desc` | 隐私承诺 |
| en | If the accessibility switch is greyed out: Open App info, tap the three-dot menu at the top right, choose Allow restricted settings, then try again. | 如果无障碍开关是灰色的：打开应用信息，点右上角三点菜单，选择“允许受限设置”，然后重试。 | `res/values/strings.xml key=restricted_help_title / restricted_help_text` | 受限设置分步教学 |
| en | The tap zone sits below the status bar. You can enable accessibility later in Settings. | 点击区位于状态栏下方。你可以稍后在设置中开启无障碍。 | `res/values/strings.xml key=success_desc_overlay` | 良性透明说明 |
| en | Skip for now | 暂时跳过 | `res/values/strings.xml key=skip_for_now` | 良性透明说明 |
| zh | 未开启无障碍服务时，Android 会将触摸区域放在状态栏下方，系统会拦截这些点击。开启服务后即可将触摸区域直接放在状态栏上。 | （同英文原文的中文本地化版本） | `res/values-zh/strings.xml key=accessibility_service_body` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。MainActivity.onResume 仅在语言/配置变化或已获悬浮窗权限时启动 OverlayService，不重跳设置页；用户从系统设置返回后停留在原页并展示实际状态（perm_granted / Fallback 提示），可选择 skip_for_now 继续使用。
- **遮罩叠层 / 高仿系统设置页**：无。无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；跳转目标为标准系统 Settings 页（含 :settings:fragment_args_key 仅为定位高亮自身条目）。
- **Android 13+ 受限设置（Restricted Settings）应对**：有，但为官方允许路径：strings.xml restricted_help_text 指引“App info → 右上三点菜单 → Allow restricted settings”，对应 ac0.a() case 2 跳 APPLICATION_DETAILS_SETTINGS；未使用 Session 安装器或任何绕过手段。
- **获权后即时行为与防撤权机制**：无。onServiceConnected 仅注册浮窗控制器并 stopService(OverlayService)；不监听设置页、不自点确认、不使用 GLOBAL_ACTION_BACK/HOME 阻止撤权（performGlobalAction 仅用于用户配置的 back/home/通知栏等映射动作）。
- **良性降级 / 替代方案**：有完整降级：未开无障碍时使用 SYSTEM_ALERT_WINDOW 悬浮窗把点击区放在状态栏下方（perm_overlay_desc / success_desc_overlay），并提供 perm_fallback 与 skip_for_now 选项，可稍后开启。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS（尤其带 :settings:fragment_args_key 指向 TapAccessibilityService）或 android.settings.APPLICATION_DETAILS_SETTINGS 时拉起 UTG；其次在 MainActivity 显示“Setup Tapbar”权限清单页（permissions_title）时抓取。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。纯静态可见（无加壳、无远端 HTML、无二阶段载荷），运行期 UTG 可完整覆盖；注意无障碍说明与权限页文案均使用系统本地化字符串（含 zh 等 12 种语言），OCR/文本匹配需按语言配置。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **Setup Tapbar 权限清单页（引导说明页）** | 包名 com.earendel.tapbar 的 MainActivity 内 Compose 页，标题文本 Setup Tapbar，含 Accessibility service / Display over other apps 条目与 Turn on / Fallback / Skip for now 按钮 | 可直接读出该应用对无障碍用途的自我陈述与是否提供跳过/降级，是区分透明引导与强制诱导的核心页面 | 标题与条目文案 Setup Tapbar / Accessibility service / Turn on / Fallback / Skip for now；是否存在可点击的取消/跳过控件；是否展示受限设置帮助区块文字 |
| **系统无障碍服务列表项** | Settings → Accessibility → 已安装服务列表中的 Tapbar 条目，摘要文字为 accessibility_desc | 核对系统列表显示的服务名与说明是否与应用宣称一致，验证无身份伪装与空白挤出 | 服务名 Tapbar 与包名 com.earendel.tapbar 对应关系；摘要文本是否为 It does not read screen content；开关状态与是否被置灰（受限设置） |
| **系统应用详情页（受限设置教学落地页）** | Settings → Apps → Tapbar（android.settings.APPLICATION_DETAILS_SETTINGS，package:com.earendel.tapbar） | 确认该应用只把用户带到官方详情页，而非伪造页面或 Session 安装器绕过 | 页面为系统 Settings 组件而非应用自有 Activity；右上角三点菜单中 Allow restricted settings 是否存在；返回后是否自动重跳或循环 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `ac0.a()（case 1 / 6 跳 ACCESSIBILITY_SETTINGS 并携带 :settings:fragment_args_key 定位 TapAccessibilityService；case 2 跳 APPLICATION_DETAILS_SETTINGS）`
- `com.earendel.tapbar.MainActivity.onResume（无重跳循环，仅在 canDrawOverlays 且偏好开启时启动 OverlayService）`
- `com.earendel.tapbar.TapAccessibilityService.onServiceConnected（注册浮窗控制器并 stopService(OverlayService)，无反撤权逻辑）`
- `res/values/strings.xml（perm_accessibility_title/desc、perm_allow、perm_fallback、skip_for_now、restricted_help_title/text、success_desc_overlay、turn_on_accessibility）`
- `res/xml/accessibility_service_config.xml（android:description=@string/accessibility_desc，canPerformGestures=true、flagRetrieveInteractiveWindows）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（Tapbar `com.earendel.tapbar`）

**静态可见性：完全可见（clear）**。该应用未加壳、无动态加载、无远端 HTML、无 WebView；全部引导文案位于 `res/values*/strings.xml`，引导 UI 由 Jetpack Compose 原生代码绘制。

**引导路径（按运行期页面流转）**

1. **冷启动进入 `MainActivity`**（`onCreate` 只做偏好初始化与主题/语言重建，不弹任何授权弹窗；`onResume` 仅在语言或配置变化时 `recreate()`，并在已具备悬浮窗权限且偏好开启时拉起 `OverlayService`）。
2. **用户主动进入“Setup Tapbar”权限页**（Compose 权限清单页，字符串 `permissions_title`=Setup Tapbar，分项 `perm_accessibility_title/desc`、`perm_overlay_title/desc`、`perm_recommended`）。这是**按需触发**而非冷启动强制阻断。
3. **点击“Turn on accessibility service”** → [ac0.a()](<resource-unit:#1.dex1 code:ac0#a>) 分支 `case 1` 用 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 跳系统无障碍列表页；分支 `case 6` 追加 `:settings:fragment_args_key` = `ComponentName(context, TapAccessibilityService.class).flattenToString()`，即**直接高亮定位到 Tapbar 自己的服务条目**（仅定位，非伪造页面）。
4. **受限设置教学**：`restricted_help_title`/`restricted_help_text` 明确给出“App info → 右上三点菜单 → Allow restricted settings”的文字指引，跳转目标为 `case 2` 的 `android.settings.APPLICATION_DETAILS_SETTINGS`（`package:com.earendel.tapbar`）。这是 Android 13+ 侧载应用的**官方允许路径教学**，非绕过手段。
5. **拒绝/返回的反馈**：无 `onResume` 死循环重跳、无定时器反复拉起、无 `GLOBAL_ACTION_BACK/HOME` 反撤权。返回后页面仅按实际状态刷新（`perm_granted` / `perm_fallback`）。
6. **降级路径（良性）**：`perm_overlay_desc` 与 `success_desc_overlay` 明确说明“无障碍服务未启用时，点击区落在状态栏下方”，并提供 `perm_fallback`、`skip_for_now`（跳过）与 `case 0/5` 的 `MANAGE_OVERLAY_PERMISSION` 悬浮窗替代方案；`success_desc_a11y` 为获权成功态。
7. **获权后动作**：[TapAccessibilityService.onServiceConnected()](<resource-unit:#1.dex1 code:com.earendel.tapbar.TapAccessibilityService#onServiceConnected>) 只注册浮窗控制器并 `stopService(OverlayService)`（用无障碍替代悬浮窗），无自点确认、无监听设置页、无 `performGlobalAction` 反撤权（`GLOBAL_ACTION` 仅用于用户配置的返回/主页等按键映射动作）。

**身份一致性**：桌面名 `Tapbar`、无障碍服务标签 `Tapbar`、说明文字 `Lets Tapbar place a small tap target on the status bar. It does not read screen content.` —— 品牌、服务名与功能描述三者一致，无同形字、无空白挤出、无多 `activity-alias`、无伪造 `isAccessibilityTool`。说明文字与代码行为基本吻合（虽 `canRetrieveWindowContent=true` 与 `flagRetrieveInteractiveWindows`，用于读取前台应用包名以显示“当前应用”名称，未见外发；应用声明 `100% Offline • Zero Trackers`）。

**结论**：该应用的无障碍申请流程为**透明的按需引导 + 官方受限设置教学 + 完整降级与跳过选项**，未发现诱导、恐吓、伪造系统页或拒权循环。本轮未登记风险。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于 DEX 与本地资源中：Compose 原生权限页（strings.xml 的 permissions_title/perm_* 系列）+ ac0.a() 的显式 Intent 跳转；无 WebView、无远端 HTML、无加壳或加密载荷，静态完整可见。",
  "summary_one_liner": "Tapbar 通过设置页内的“Setup Tapbar”权限清单按需引导用户点击跳转系统无障碍列表（并高亮定位自身服务条目），配合 Android 13+ 官方“允许受限设置”文字教学，并提供悬浮窗降级与“跳过”选项，全程无强制、无循环重跳。",
  "disguise_identity": {
    "app_display_name": "Tapbar",
    "claimed_brand_or_persona": "Tapbar / Earendel（F-Droid 开源按键映射工具，tagline: 100% Offline • Zero Trackers • Open Source）",
    "a11y_service_label": "Tapbar",
    "identity_mismatch": false,
    "obfuscation_tricks": "无"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.earendel.tapbar.MainActivity（Compose 主界面）",
      "trigger_event": "onCreate / onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Setup Tapbar",
      "shown_text_zh": "配置 Tapbar（权限清单页标题，用户主动点入后才展示）",
      "user_action_requested": "无强制操作；冷启动不弹授权弹窗，可正常浏览主界面",
      "code_anchor": "com.earendel.tapbar.MainActivity.onCreate / onResume；res/values/strings.xml permissions_title"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "Setup Tapbar 权限清单页（Compose，含 Accessibility service / Display over other apps 两项）",
      "trigger_event": "用户在主界面/设置入口点开权限配置",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility service — Lets the tap zone sit directly on the status bar. It does not read or send any screen text. | Turn on | Fallback | Recommended | Skip for now",
      "shown_text_zh": "无障碍服务——让点击区直接位于状态栏上，不读取也不发送任何屏幕文字。｜开启｜替代方案｜推荐｜暂时跳过",
      "user_action_requested": "可选择“Turn on”开启无障碍，或选择“Fallback/跳过”使用悬浮窗替代方案；存在取消/跳过入口",
      "code_anchor": "res/values/strings.xml perm_accessibility_title / perm_accessibility_desc / perm_allow / perm_fallback / skip_for_now / perm_recommended"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（部分路径带 :settings:fragment_args_key 高亮 TapAccessibilityService 条目）",
      "trigger_event": "点击“Turn on accessibility service”按钮",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Turn on accessibility service",
      "shown_text_zh": "开启无障碍服务",
      "user_action_requested": "在系统无障碍列表中手动找到 Tapbar 并开启开关；用户可随时返回",
      "code_anchor": "ac0.a() case 1 / case 6；strings.xml turn_on_accessibility"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置页 android.settings.APPLICATION_DETAILS_SETTINGS（package:com.earendel.tapbar）",
      "trigger_event": "开关置灰时点击帮助入口，触发 ac0.a() case 2",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "If the accessibility switch is greyed out: Open App info, tap the three-dot menu at the top right, choose Allow restricted settings, then try again.",
      "shown_text_zh": "如果无障碍开关是灰色的：打开应用信息，点右上角三点菜单，选择“允许受限设置”，然后重试。",
      "user_action_requested": "按官方路径进入应用详情页并允许受限设置（Android 13+ 侧载应用的系统要求，非绕过手段）",
      "code_anchor": "res/values/strings.xml restricted_help_title / restricted_help_text；ac0.a() case 2"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity / Setup 页状态刷新",
      "trigger_event": "从系统设置返回后 onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "The tap zone sits below the status bar. You can enable accessibility later in Settings.",
      "shown_text_zh": "点击区位于状态栏下方。你可以稍后在设置中开启无障碍。",
      "user_action_requested": "无强制重跳；用户可继续使用悬浮窗替代模式",
      "code_anchor": "com.earendel.tapbar.MainActivity.onResume；strings.xml success_desc_overlay / perm_overlay_desc"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.earendel.tapbar.TapAccessibilityService（onServiceConnected）",
      "trigger_event": "系统绑定无障碍服务回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "The tap zone sits directly on the status bar. / You're all set",
      "shown_text_zh": "点击区直接位于状态栏上。／已全部设置完成。",
      "user_action_requested": "无额外操作；服务仅注册浮窗控制器并停止 OverlayService，无自点确认或阻止撤权行为",
      "code_anchor": "com.earendel.tapbar.TapAccessibilityService.onServiceConnected；strings.xml success_desc_a11y / success_title"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 内的 Compose“Setup Tapbar”权限清单页（原生渲染，非 WebView/HTML），条目文字来自 res/values/strings.xml 的 perm_accessibility_title / perm_accessibility_desc / perm_overlay_title / perm_overlay_desc",
    "按钮文案 perm_allow（Turn on）、perm_fallback（Fallback）、skip_for_now（Skip for now）同处该 Compose 页面",
    "系统无障碍列表条目说明：res/xml/accessibility_service_config.xml 的 android:description=@string/accessibility_desc（\"Lets Tapbar place a small tap target on the status bar. It does not read screen content.\"）",
    "受限设置帮助区块：strings.xml restricted_help_title / restricted_help_text，展示在设置页/权限页内，点击跳 APPLICATION_DETAILS_SETTINGS",
    "成功态文案 success_title（You're all set）、success_desc_a11y、success_desc_overlay 展示在权限页完成状态",
    "关于页（h70.n 构建的 Compose About 列表）：版本号、Earendel、GitHub、源码与 LICENSE 链接，跳转 github.com/Earendel-lab/Tapbar"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Lets Tapbar place a small tap target on the status bar. It does not read screen content.",
      "text_zh": "允许 Tapbar 在状态栏上放置一个小型点击目标。它不会读取屏幕内容。",
      "source_location": "res/values/strings.xml key=accessibility_desc（系统无障碍列表说明）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Without the accessibility service, Android places the zone below the status bar and the system takes those taps. Turn the service on to place the zone directly on the status bar.",
      "text_zh": "未开启无障碍服务时，Android 会把点击区放在状态栏下方，系统会接管这些点击。开启服务后即可把点击区直接放在状态栏上。",
      "source_location": "res/values/strings.xml key=accessibility_service_body（含 de/es/fr/hi/ja/ko/ne/pt/ru/tr/zh 多语言版本）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Lets the tap zone sit directly on the status bar. It does not read or send any screen text.",
      "text_zh": "让点击区直接位于状态栏上。它不会读取或发送任何屏幕文字。",
      "source_location": "res/values/strings.xml key=perm_accessibility_desc",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "If the accessibility switch is greyed out: Open App info, tap the three-dot menu at the top right, choose Allow restricted settings, then try again.",
      "text_zh": "如果无障碍开关是灰色的：打开应用信息，点右上角三点菜单，选择“允许受限设置”，然后重试。",
      "source_location": "res/values/strings.xml key=restricted_help_title / restricted_help_text",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "The tap zone sits below the status bar. You can enable accessibility later in Settings.",
      "text_zh": "点击区位于状态栏下方。你可以稍后在设置中开启无障碍。",
      "source_location": "res/values/strings.xml key=success_desc_overlay",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Skip for now",
      "text_zh": "暂时跳过",
      "source_location": "res/values/strings.xml key=skip_for_now",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "未开启无障碍服务时，Android 会将触摸区域放在状态栏下方，系统会拦截这些点击。开启服务后即可将触摸区域直接放在状态栏上。",
      "text_zh": "（同英文原文的中文本地化版本）",
      "source_location": "res/values-zh/strings.xml key=accessibility_service_body",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。MainActivity.onResume 仅在语言/配置变化或已获悬浮窗权限时启动 OverlayService，不重跳设置页；用户从系统设置返回后停留在原页并展示实际状态（perm_granted / Fallback 提示），可选择 skip_for_now 继续使用。",
    "overlay_or_fake_settings": "无。无半透明引导遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；跳转目标为标准系统 Settings 页（含 :settings:fragment_args_key 仅为定位高亮自身条目）。",
    "restricted_settings_13plus_coaching": "有，但为官方允许路径：strings.xml restricted_help_text 指引“App info → 右上三点菜单 → Allow restricted settings”，对应 ac0.a() case 2 跳 APPLICATION_DETAILS_SETTINGS；未使用 Session 安装器或任何绕过手段。",
    "post_grant_anti_removal": "无。onServiceConnected 仅注册浮窗控制器并 stopService(OverlayService)；不监听设置页、不自点确认、不使用 GLOBAL_ACTION_BACK/HOME 阻止撤权（performGlobalAction 仅用于用户配置的 back/home/通知栏等映射动作）。",
    "benign_graceful_degradation": "有完整降级：未开无障碍时使用 SYSTEM_ALERT_WINDOW 悬浮窗把点击区放在状态栏下方（perm_overlay_desc / success_desc_overlay），并提供 perm_fallback 与 skip_for_now 选项，可稍后开启。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Intent 跳转 android.settings.ACCESSIBILITY_SETTINGS（尤其带 :settings:fragment_args_key 指向 TapAccessibilityService）或 android.settings.APPLICATION_DETAILS_SETTINGS 时拉起 UTG；其次在 MainActivity 显示“Setup Tapbar”权限清单页（permissions_title）时抓取。",
    "key_pages_to_capture": [
      {
        "page_role": "Setup Tapbar 权限清单页（引导说明页）",
        "page_identifier": "包名 com.earendel.tapbar 的 MainActivity 内 Compose 页，标题文本 Setup Tapbar，含 Accessibility service / Display over other apps 条目与 Turn on / Fallback / Skip for now 按钮",
        "why_most_useful": "可直接读出该应用对无障碍用途的自我陈述与是否提供跳过/降级，是区分透明引导与强制诱导的核心页面",
        "observable_utg_signals": ["标题与条目文案 Setup Tapbar / Accessibility service / Turn on / Fallback / Skip for now", "是否存在可点击的取消/跳过控件", "是否展示受限设置帮助区块文字"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility → 已安装服务列表中的 Tapbar 条目，摘要文字为 accessibility_desc",
        "why_most_useful": "核对系统列表显示的服务名与说明是否与应用宣称一致，验证无身份伪装与空白挤出",
        "observable_utg_signals": ["服务名 Tapbar 与包名 com.earendel.tapbar 对应关系", "摘要文本是否为 It does not read screen content", "开关状态与是否被置灰（受限设置）"]
      },
      {
        "page_role": "系统应用详情页（受限设置教学落地页）",
        "page_identifier": "Settings → Apps → Tapbar（android.settings.APPLICATION_DETAILS_SETTINGS，package:com.earendel.tapbar）",
        "why_most_useful": "确认该应用只把用户带到官方详情页，而非伪造页面或 Session 安装器绕过",
        "observable_utg_signals": ["页面为系统 Settings 组件而非应用自有 Activity", "右上角三点菜单中 Allow restricted settings 是否存在", "返回后是否自动重跳或循环"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。纯静态可见（无加壳、无远端 HTML、无二阶段载荷），运行期 UTG 可完整覆盖；注意无障碍说明与权限页文案均使用系统本地化字符串（含 zh 等 12 种语言），OCR/文本匹配需按语言配置。"
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
    "ac0.a()（case 1 / 6 跳 ACCESSIBILITY_SETTINGS 并携带 :settings:fragment_args_key 定位 TapAccessibilityService；case 2 跳 APPLICATION_DETAILS_SETTINGS）",
    "com.earendel.tapbar.MainActivity.onResume（无重跳循环，仅在 canDrawOverlays 且偏好开启时启动 OverlayService）",
    "com.earendel.tapbar.TapAccessibilityService.onServiceConnected（注册浮窗控制器并 stopService(OverlayService)，无反撤权逻辑）",
    "res/values/strings.xml（perm_accessibility_title/desc、perm_allow、perm_fallback、skip_for_now、restricted_help_title/text、success_desc_overlay、turn_on_accessibility）",
    "res/xml/accessibility_service_config.xml（android:description=@string/accessibility_desc，canPerformGestures=true、flagRetrieveInteractiveWindows）"
  ]
}
```

</details>
