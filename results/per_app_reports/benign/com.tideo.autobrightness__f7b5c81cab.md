# BN_020__f7b5c81cab｜显示调节、截屏与分屏效率 — Tideo Auto Brightness

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：214.9s

## 1. 一句话核心结论

- **核心申请方式**：无障碍权限仅在 Live Debug 页的“Global flash”卡片中作为可选调试浮层功能按需提供，用户点按钮跳系统无障碍设置自行开启，说明文本坦白限定为“只绘制消息浮层、从不读取屏幕内容”，无强制、无伪装、无拒绝循环。
- **静态可见性说明**：全部相关逻辑静态可见：Manifest 服务声明、res/xml/aab_accessibility_service.xml 能力配置、res/values/strings.xml 引导文案、Compose 代码中的设置页跳转与授权状态只读检查均在 DEX 明文中；无加壳、无 AES 密文载荷、无远端 HTML 引导页，assets 下仅 dexopt 产物。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `f7b5c81caba4a06ec5ddcc6af247a2b8df6cae67d4902bf44019fa2011996cbb` |
| 包名 / 年份 | `com.tideo.autobrightness` / 2025-2026 |
| 家族 / 品类 | **显示调节、截屏与分屏效率**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.tideo.autobrightness_33.apk |
| 桌面显示名 | Tideo Auto Brightness |
| 引导页宣称品牌/身份 | Tideo Auto Brightness（F-Droid 开源自动亮度替代方案，真实身份） |
| 系统无障碍列表服务名 | Auto Brightness global flashes |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务 label 与包名、应用名语义一致，未使用空白/换行挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool；Manifest 中无 activity-alias，无障碍服务 exported=false 且由系统 BIND_ACCESSIBILITY_SERVICE 保护。 |
| 无障碍服务类名 | `com.tideo.autobrightness.app.runtime.AabToastAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Shows Auto Brightness debug flash messages system-wide (over other apps). This optional service only draws the message overlays — it never reads screen content. Enable it only if you want the diagnostic flashes visible while using other apps. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tideo.autobrightness.app.MainActivity（Compose NavGraph）→ OnboardingScreen「Setup & Permissions」 | LAUNCHER 启动 MainActivity.onCreate | 原生Activity | **原文**：Setup & Permissions / 2. Modify system settings (required) / Grants brightness control. Without this the service runs but cannot change brightness. / Skip for now<br>**译注**：设置与权限：第 2 步“修改系统设置（必需）”——授予亮度控制能力，否则服务可运行但无法改变亮度；底部有“暂时跳过”。 | 逐步授予通知、修改系统设置、位置、使用情况访问等权限；可点“Skip for now”跳过，全程不涉及无障碍权限 | `com.tideo.autobrightness.app.ui.onboarding.OnboardingScreenKt（strings.xml: onboarding_title / onboarding_step2_body / onboarding_skip）` |
| 2 | 引导说明页 | OnboardingScreen 内 RestrictedSettingsCard 卡片 | 进入 Onboarding 页面即渲染 | 原生Activity | **原文**：Heads up: restricted settings — Installed outside the Play Store, Android may block the "Modify system settings" toggle below (and "Usage access", for per-app rules) — it looks greyed out or shows "Restricted setting". Tap it anyway; that usually shows the unlock prompt. If not, open App info → ⋮ menu → "Allow restricted settings", then return here.<br>**译注**：提示：受限设置——非 Play 商店安装时，下方“修改系统设置”开关（以及按应用规则用的“使用情况访问”）可能被 Android 灰化或显示“受限设置”。可以照常点它，通常会弹出解锁提示；若仍不行，进入应用信息 → ⋮ 菜单 →“允许受限设置”，再回到这里。 | 对 WRITE_SETTINGS / 使用情况访问 尝试解锁受限设置（非无障碍权限）；卡片不阻断，用户可跳过 | `OnboardingScreenKt$RestrictedSettingsCard$1（strings.xml: onboarding_restricted_title / onboarding_restricted_body）` |
| 3 | 业务功能触发 | Live Debug 页 GlobalFlashCard（title_global_flash = Global flash (system-wide)） | 用户在调试页看到该卡片，卡片渲染时调用 LiveDebugViewModel.isGlobalToastServiceEnabled() 读取 Settings.Secure.enabled_accessibility_services 判断状态 | 原生Activity | **原文**：Global flash (system-wide) / Show debug/context flashes over other apps via an optional Accessibility overlay. It only draws the messages — it never reads screen content. / Status: Off (foreground only)<br>**译注**：全局闪烁提示（全系统）：通过可选的无障碍浮层在其他应用之上显示调试/场景提示。它只绘制消息——从不读取屏幕内容。状态：关闭（仅前台）。 | 阅读说明后决定是否开启；不开启仅失去跨应用浮层提示，应用功能不受影响 | `com.tideo.autobrightness.app.ui.screens.LiveDebugScreenKt$GlobalFlashCard$1（strings.xml: livedebug_flash_desc / livedebug_flash_off / title_global_flash）` |
| 4 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（无障碍服务列表） | 点击卡片按钮（未授权时文案 livedebug_flash_enable_settings = Enable in Accessibility settings，已授权时为 livedebug_flash_open_settings = Open Accessibility settings） | 系统无障碍页 | **原文**：Enable in Accessibility settings / Open Accessibility settings<br>**译注**：“在无障碍设置中启用” / “打开无障碍设置” | 用户在系统无障碍列表中自行找到 “Auto Brightness global flashes” 并开启；跳转由 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS").addFlags(FLAG_ACTIVITY_NEW_TASK)) 完成，无任何自动点击 | `com.tideo.autobrightness.app.ui.screens.LiveDebugScreenKt#LiveDebugScreen$lambda$12$lambda$11` |
| 5 | 拒权反馈循环 | 返回 Live Debug 页，GlobalFlashCard 状态仍显示 Off (foreground only) | 用户返回应用，或 Lifecycle RESUMED 触发状态刷新 | 原生Activity | **原文**：Off (foreground only)<br>**译注**：关闭（仅前台）：表示未授权，提示仅在本应用前台显示 | 无强制动作，可随时再次点击进入设置；应用安全降级为前台提示，不重复弹窗 | `com.tideo.autobrightness.app.state.LiveDebugViewModel#isGlobalToastServiceEnabled` |
| 6 | 获权后动作 | com.tideo.autobrightness.app.runtime.AabToastAccessibilityService（无障碍浮层服务） | 系统绑定服务回调 onServiceConnected() | 悬浮窗Overlay | **原文**：High Brightness Mode activated / Adaptive Brightness off — Tideo is back in control / Manual override — auto brightness paused<br>**译注**：高亮模式已激活 / 自适应亮度关闭——Tideo 重新接管 / 手动覆盖——自动亮度已暂停 | 无。浮层为底部居中小标签（TYPE_ACCESSIBILITY_OVERLAY，gravity=BOTTOM，y=80dp），2.5 秒自动消失，点击立即消失；onAccessibilityEvent() 空实现，不读取屏幕内容，无自授权、无阻止撤权行为 | `com.tideo.autobrightness.app.runtime.AabToastAccessibilityService#onServiceConnected / #showOverlay / #onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务 label「Auto Brightness global flashes」+ android:description（res/values/strings.xml 的 global_toasts_a11y_description，经 res/xml/aab_accessibility_service.xml 引用）
- Live Debug 页（Compose 原生界面）GlobalFlashCard：livedebug_flash_desc 说明段 + livedebug_flash_status 状态 + 按钮 livedebug_flash_enable_settings / livedebug_flash_open_settings
- Onboarding「Setup & Permissions」页（Compose 原生界面）：onboarding_step1~3 与 onboarding_usage_* 权限分步说明，含 onboarding_skip「Skip for now」
- Onboarding 页 RestrictedSettingsCard 卡片：onboarding_restricted_title / onboarding_restricted_body（针对 WRITE_SETTINGS 与使用情况访问，不涉及无障碍）
- 无障碍浮层本体（TYPE_ACCESSIBILITY_OVERLAY 的 TextView）：flash_* 系列运行时状态文本，如 flash_hbm_on、flash_manual_override
- 未出现：WebView / 本地或远端 HTML 引导页、全屏遮罩指引、高仿系统无障碍开关页、通知栏拉权引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Shows Auto Brightness debug flash messages system-wide (over other apps). This optional service only draws the message overlays — it never reads screen content. Enable it only if you want the diagnostic flashes visible while using other apps. | 在整个系统范围内（其他应用之上）显示自动亮度的调试闪烁提示。这个可选服务只绘制消息浮层——它从不读取屏幕内容。仅当你希望在使用其他应用时看到诊断闪烁提示才启用它。 | `res/values/strings.xml key=global_toasts_a11y_description（由 res/xml/aab_accessibility_service.xml 的 android:description 引用）` | 良性透明说明 |
| en | Show debug/context flashes over other apps via an optional Accessibility overlay. It only draws the messages — it never reads screen content. | 通过可选的无障碍浮层在其他应用之上显示调试/场景提示。它只绘制消息——从不读取屏幕内容。 | `res/values/strings.xml key=livedebug_flash_desc（LiveDebugScreenKt$GlobalFlashCard$1 渲染）` | 良性透明说明 |
| en | Enable in Accessibility settings | 在无障碍设置中启用 | `res/values/strings.xml key=livedebug_flash_enable_settings（LiveDebugScreenKt$GlobalFlashCard$1$2 按钮文案）` | 良性透明说明 |
| en | Open Accessibility settings | 打开无障碍设置 | `res/values/strings.xml key=livedebug_flash_open_settings（已授权状态下的按钮文案）` | 良性透明说明 |
| en | Global flash (system-wide) | 全局闪烁提示（全系统） | `res/values/strings.xml key=title_global_flash` | 良性透明说明 |
| en | Installed outside the Play Store, Android may block the "Modify system settings" toggle below (and "Usage access", for per-app rules) — it looks greyed out or shows "Restricted setting". Tap it anyway; that usually shows the unlock prompt. If not, open App info → ⋮ menu → "Allow restricted settings", then return here. | 由于不是从 Play 商店安装，Android 可能屏蔽下方的“修改系统设置”开关（以及按应用规则用的“使用情况访问”）——它看起来是灰的或显示“受限设置”。可以照常点它，通常会弹出解锁提示；若仍不行，打开应用信息 → ⋮ 菜单 →“允许受限设置”，然后回到这里。 | `res/values/strings.xml key=onboarding_restricted_body（OnboardingScreenKt$RestrictedSettingsCard$1 渲染；对象为 WRITE_SETTINGS / 使用情况访问，非无障碍）` | 受限设置分步教学 |
| en | Skip for now | 暂时跳过 | `res/values/strings.xml key=onboarding_skip（Onboarding 页）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性安全降级：不开启无障碍时，GlobalFlashCard 状态保持 Off (foreground only)，浮层提示仅在本应用前台显示；返回或拒绝授权后无 onResume 重跳、无定时器拉起、无弹窗催促，用户可随时再次点击进入设置
- **遮罩叠层 / 高仿系统设置页**：无。仅有授权后由无障碍服务自身绘制的底部小标签（TYPE_ACCESSIBILITY_OVERLAY，2.5 秒自动消失、可点击关闭），不是叠在系统设置页上的引导遮罩，也不是高仿系统开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：存在但对象不同：Onboarding 页 onboarding_restricted_body 教用户对「修改系统设置（WRITE_SETTINGS）」与「使用情况访问」在应用信息 → ⋮ → Allow restricted settings 解锁；无障碍权限本身未做任何受限设置绕过教学，也未涉及 Session 安装器
- **获权后即时行为与防撤权机制**：无。onServiceConnected() 仅获取 WindowManager 并向 AabFlash 注册展示器；未调用 performGlobalAction(GLOBAL_ACTION_BACK/HOME)、未监听设置页、未自行改写 enabled_accessibility_services
- **良性降级 / 替代方案**：有：无障碍完全可选，不开启时提示降级为前台内显示；亮度控制主链路走 WRITE_SETTINGS / ADB / Shizuku 通道，与无障碍服务无关

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（唯一入口在 Live Debug 页 GlobalFlashCard 按钮），以及冷启动进入 MainActivity 后 Onboarding「Setup & Permissions」页渲染时
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。该应用静态加壳初判为 False，assets 仅含 dexopt 产物、native 仅 androidx.graphics.path 与 datastore shared counter 两个标准库，运行期无远端下发或二次解密；唯一需注意的判别点是 onboarding_restricted_body 的受限设置教学，其对象是 WRITE_SETTINGS/使用情况访问而非无障碍，不应误判为无障碍受限设置绕过。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页（Onboarding Setup & Permissions）** | MainActivity / com.tideo.autobrightness.app.ui.onboarding.OnboardingScreenKt，含“Setup & Permissions”标题与第 1–5 步权限卡片 | 用于判断是否存在冷启动即推销无障碍、是否强制不可跳过；本应用此页完全不提无障碍，可据此排除 TRIG_COLD_START_BLOCK | 是否出现“Skip for now”可跳过按钮；权限步骤是否包含无障碍服务项；是否出现“Allow restricted settings”教学卡片及其对象权限 |
| **跳转前说明页（Live Debug → Global flash 卡片）** | Live Debug 页，含“Global flash (system-wide)”标题与“Show debug/context flashes over other apps via an optional Accessibility overlay”说明 | 这是唯一的无障碍引导入口，可直接判定触发时机为按需、文案是否坦白限定能力范围 | 是否含“never reads screen content”类隐私/能力承诺；按钮文案是 Enable/Open Accessibility settings 还是伪造的“立即修复/开启优化”；状态行是否显示 Off (foreground only) |
| **系统无障碍服务列表项** | 系统设置 → 无障碍 → 已下载/已安装的服务，条目名“Auto Brightness global flashes”，副标题为 global_toasts_a11y_description 全文 | 核对系统侧展示名与描述是否与包名/应用名一致，是否存在同形字或夸大诱导描述 | 服务名是否为“Auto Brightness global flashes”而非冒充系统组件；描述是否明示 optional 与 never reads screen content；是否出现空白/换行将风险提示挤出可视区域 |
| **获权后浮层展示页** | 其他应用前台时的底部小标签（TYPE_ACCESSIBILITY_OVERLAY，gravity=BOTTOM，约 80dp 上移） | 验证浮层内容仅为本地 flash_* 状态文案、是否覆盖关键 UI 或诱导点击 | 浮层文本是否为本地状态字符串（如 High Brightness Mode activated）；浮层是否约 2.5 秒自动消失、点击即关闭；浮层是否遮挡其他应用的敏感控件或含诱导按钮 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.tideo.autobrightness.app.ui.screens.LiveDebugScreenKt#LiveDebugScreen$lambda$12$lambda$11`
- `com.tideo.autobrightness.app.ui.screens.LiveDebugScreenKt$GlobalFlashCard$1$2#invoke`
- `com.tideo.autobrightness.app.state.LiveDebugViewModel#isGlobalToastServiceEnabled`
- `com.tideo.autobrightness.app.runtime.AabToastAccessibilityService#onServiceConnected`
- `com.tideo.autobrightness.app.runtime.AabToastAccessibilityService#showOverlay`
- `res/xml/aab_accessibility_service.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**结论：未发现无障碍权限诱导或恶意利用。** 该应用的无障碍服务属于用户主动按需开启的可选调试浮层功能，全程静态可见，没有伪装、没有强制、没有拒绝后循环重跳。

**关键事实（逐项核验）**

1. **声明面透明**：`AndroidManifest.xml` 中服务声明 `android:label="Auto Brightness global flashes"`，`android:exported="false"`，受 `BIND_ACCESSIBILITY_SERVICE` 保护；配置 [aab_accessibility_service.xml](<resource-unit:#1 file:res/xml/aab_accessibility_service.xml>) 明确 `canRetrieveWindowContent="false"`、仅监听 `typeWindowStateChanged`、`feedbackGeneric`，`description` 直指 [strings.xml 第 353 行](<resource-unit:#1 file:res/values/strings.xml#L353>) 的坦白说明。

2. **唯一跳转点**：全包仅 1 处 `android.settings.ACCESSIBILITY_SETTINGS` 跳转，位于 [LiveDebugScreen$lambda$12$lambda$11()](<resource-unit:#1.dex1 code:com.tideo.autobrightness.app.ui.screens.LiveDebugScreenKt#LiveDebugScreen$lambda$12$lambda$11>)，由 Live Debug 页 “Global flash (system-wide)” 卡片的按钮触发（`livedebug_flash_enable_settings` / `livedebug_flash_open_settings`）。未发现 `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转，未发现 WebView、HTML 引导页、全屏遮罩或高仿系统设置页。

3. **无强制与无循环**：无障碍入口只在 Live Debug 功能页按需出现，冷启动、Onboarding 流程（[OnboardingScreenKt](<resource-unit:#1.dex1 code:com.tideo.autobrightness.app.ui.onboarding.OnboardingScreenKt#RestrictedSettingsCard>)）均不推销无障碍；授权状态仅通过 [isGlobalToastServiceEnabled()](<resource-unit:#1.dex1 code:com.tideo.autobrightness.app.state.LiveDebugViewModel#isGlobalToastServiceEnabled>) 读取 `Settings.Secure.enabled_accessibility_services` 做只读展示，无 onResume 重跳、无定时器拉起、无 `performGlobalAction` 阻止撤权。

4. **能力边界与声明一致**：[onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.tideo.autobrightness.app.runtime.AabToastAccessibilityService#onAccessibilityEvent>) 方法体为空（不读取任何界面内容）；[showOverlay()](<resource-unit:#1.dex1 code:com.tideo.autobrightness.app.runtime.AabToastAccessibilityService#showOverlay>) 用 `TYPE_ACCESSIBILITY_OVERLAY(2032)` 添加一个底部居中小 TextView，2.5 秒后自动 `removeOverlay`，点击即消失，文本来自本地 `flash_*` 字符串（如 “High Brightness Mode activated”），不含外部下发。

5. **一处需说明的“教唆”文本属另一权限链**：`onboarding_restricted_body`（“Tap it anyway… open App info → ⋮ menu → 'Allow restricted settings'”）针对的是 **WRITE_SETTINGS / 使用情况访问** 这两项受限设置，用于 `targetSdk 36` 侧载场景，措辞同时给出 “Skip for now” 与 ADB/Shizuku 替代通道；与无障碍权限无关，且未教用户绕过 Session 安装器等更强手段。

6. **覆盖边界**：静态可见性完整，无加壳（`apkid` 预筛 False、`assets/` 仅 dexopt 产物、native 仅 androidx.path 与 datastore counter 两个标准库），故不存在 `packed_or_encrypted` 缺口；动态分析未启动（静态证据已闭合）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部相关逻辑静态可见：Manifest 服务声明、res/xml/aab_accessibility_service.xml 能力配置、res/values/strings.xml 引导文案、Compose 代码中的设置页跳转与授权状态只读检查均在 DEX 明文中；无加壳、无 AES 密文载荷、无远端 HTML 引导页，assets 下仅 dexopt 产物。",
  "summary_one_liner": "无障碍权限仅在 Live Debug 页的“Global flash”卡片中作为可选调试浮层功能按需提供，用户点按钮跳系统无障碍设置自行开启，说明文本坦白限定为“只绘制消息浮层、从不读取屏幕内容”，无强制、无伪装、无拒绝循环。",
  "disguise_identity": {
    "app_display_name": "Tideo Auto Brightness",
    "claimed_brand_or_persona": "Tideo Auto Brightness（F-Droid 开源自动亮度替代方案，真实身份）",
    "a11y_service_label": "Auto Brightness global flashes",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务 label 与包名、应用名语义一致，未使用空白/换行挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool；Manifest 中无 activity-alias，无障碍服务 exported=false 且由系统 BIND_ACCESSIBILITY_SERVICE 保护。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tideo.autobrightness.app.MainActivity（Compose NavGraph）→ OnboardingScreen「Setup & Permissions」",
      "trigger_event": "LAUNCHER 启动 MainActivity.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Setup & Permissions / 2. Modify system settings (required) / Grants brightness control. Without this the service runs but cannot change brightness. / Skip for now",
      "shown_text_zh": "设置与权限：第 2 步“修改系统设置（必需）”——授予亮度控制能力，否则服务可运行但无法改变亮度；底部有“暂时跳过”。",
      "user_action_requested": "逐步授予通知、修改系统设置、位置、使用情况访问等权限；可点“Skip for now”跳过，全程不涉及无障碍权限",
      "code_anchor": "com.tideo.autobrightness.app.ui.onboarding.OnboardingScreenKt（strings.xml: onboarding_title / onboarding_step2_body / onboarding_skip）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "OnboardingScreen 内 RestrictedSettingsCard 卡片",
      "trigger_event": "进入 Onboarding 页面即渲染",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Heads up: restricted settings — Installed outside the Play Store, Android may block the \"Modify system settings\" toggle below (and \"Usage access\", for per-app rules) — it looks greyed out or shows \"Restricted setting\". Tap it anyway; that usually shows the unlock prompt. If not, open App info → ⋮ menu → \"Allow restricted settings\", then return here.",
      "shown_text_zh": "提示：受限设置——非 Play 商店安装时，下方“修改系统设置”开关（以及按应用规则用的“使用情况访问”）可能被 Android 灰化或显示“受限设置”。可以照常点它，通常会弹出解锁提示；若仍不行，进入应用信息 → ⋮ 菜单 →“允许受限设置”，再回到这里。",
      "user_action_requested": "对 WRITE_SETTINGS / 使用情况访问 尝试解锁受限设置（非无障碍权限）；卡片不阻断，用户可跳过",
      "code_anchor": "OnboardingScreenKt$RestrictedSettingsCard$1（strings.xml: onboarding_restricted_title / onboarding_restricted_body）"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "Live Debug 页 GlobalFlashCard（title_global_flash = Global flash (system-wide)）",
      "trigger_event": "用户在调试页看到该卡片，卡片渲染时调用 LiveDebugViewModel.isGlobalToastServiceEnabled() 读取 Settings.Secure.enabled_accessibility_services 判断状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Global flash (system-wide) / Show debug/context flashes over other apps via an optional Accessibility overlay. It only draws the messages — it never reads screen content. / Status: Off (foreground only)",
      "shown_text_zh": "全局闪烁提示（全系统）：通过可选的无障碍浮层在其他应用之上显示调试/场景提示。它只绘制消息——从不读取屏幕内容。状态：关闭（仅前台）。",
      "user_action_requested": "阅读说明后决定是否开启；不开启仅失去跨应用浮层提示，应用功能不受影响",
      "code_anchor": "com.tideo.autobrightness.app.ui.screens.LiveDebugScreenKt$GlobalFlashCard$1（strings.xml: livedebug_flash_desc / livedebug_flash_off / title_global_flash）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "点击卡片按钮（未授权时文案 livedebug_flash_enable_settings = Enable in Accessibility settings，已授权时为 livedebug_flash_open_settings = Open Accessibility settings）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable in Accessibility settings / Open Accessibility settings",
      "shown_text_zh": "“在无障碍设置中启用” / “打开无障碍设置”",
      "user_action_requested": "用户在系统无障碍列表中自行找到 “Auto Brightness global flashes” 并开启；跳转由 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\").addFlags(FLAG_ACTIVITY_NEW_TASK)) 完成，无任何自动点击",
      "code_anchor": "com.tideo.autobrightness.app.ui.screens.LiveDebugScreenKt#LiveDebugScreen$lambda$12$lambda$11"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 Live Debug 页，GlobalFlashCard 状态仍显示 Off (foreground only)",
      "trigger_event": "用户返回应用，或 Lifecycle RESUMED 触发状态刷新",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Off (foreground only)",
      "shown_text_zh": "关闭（仅前台）：表示未授权，提示仅在本应用前台显示",
      "user_action_requested": "无强制动作，可随时再次点击进入设置；应用安全降级为前台提示，不重复弹窗",
      "code_anchor": "com.tideo.autobrightness.app.state.LiveDebugViewModel#isGlobalToastServiceEnabled"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.tideo.autobrightness.app.runtime.AabToastAccessibilityService（无障碍浮层服务）",
      "trigger_event": "系统绑定服务回调 onServiceConnected()",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "High Brightness Mode activated / Adaptive Brightness off — Tideo is back in control / Manual override — auto brightness paused",
      "shown_text_zh": "高亮模式已激活 / 自适应亮度关闭——Tideo 重新接管 / 手动覆盖——自动亮度已暂停",
      "user_action_requested": "无。浮层为底部居中小标签（TYPE_ACCESSIBILITY_OVERLAY，gravity=BOTTOM，y=80dp），2.5 秒自动消失，点击立即消失；onAccessibilityEvent() 空实现，不读取屏幕内容，无自授权、无阻止撤权行为",
      "code_anchor": "com.tideo.autobrightness.app.runtime.AabToastAccessibilityService#onServiceConnected / #showOverlay / #onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务 label「Auto Brightness global flashes」+ android:description（res/values/strings.xml 的 global_toasts_a11y_description，经 res/xml/aab_accessibility_service.xml 引用）",
    "Live Debug 页（Compose 原生界面）GlobalFlashCard：livedebug_flash_desc 说明段 + livedebug_flash_status 状态 + 按钮 livedebug_flash_enable_settings / livedebug_flash_open_settings",
    "Onboarding「Setup & Permissions」页（Compose 原生界面）：onboarding_step1~3 与 onboarding_usage_* 权限分步说明，含 onboarding_skip「Skip for now」",
    "Onboarding 页 RestrictedSettingsCard 卡片：onboarding_restricted_title / onboarding_restricted_body（针对 WRITE_SETTINGS 与使用情况访问，不涉及无障碍）",
    "无障碍浮层本体（TYPE_ACCESSIBILITY_OVERLAY 的 TextView）：flash_* 系列运行时状态文本，如 flash_hbm_on、flash_manual_override",
    "未出现：WebView / 本地或远端 HTML 引导页、全屏遮罩指引、高仿系统无障碍开关页、通知栏拉权引导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Shows Auto Brightness debug flash messages system-wide (over other apps). This optional service only draws the message overlays — it never reads screen content. Enable it only if you want the diagnostic flashes visible while using other apps.",
      "text_zh": "在整个系统范围内（其他应用之上）显示自动亮度的调试闪烁提示。这个可选服务只绘制消息浮层——它从不读取屏幕内容。仅当你希望在使用其他应用时看到诊断闪烁提示才启用它。",
      "source_location": "res/values/strings.xml key=global_toasts_a11y_description（由 res/xml/aab_accessibility_service.xml 的 android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Show debug/context flashes over other apps via an optional Accessibility overlay. It only draws the messages — it never reads screen content.",
      "text_zh": "通过可选的无障碍浮层在其他应用之上显示调试/场景提示。它只绘制消息——从不读取屏幕内容。",
      "source_location": "res/values/strings.xml key=livedebug_flash_desc（LiveDebugScreenKt$GlobalFlashCard$1 渲染）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable in Accessibility settings",
      "text_zh": "在无障碍设置中启用",
      "source_location": "res/values/strings.xml key=livedebug_flash_enable_settings（LiveDebugScreenKt$GlobalFlashCard$1$2 按钮文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Accessibility settings",
      "text_zh": "打开无障碍设置",
      "source_location": "res/values/strings.xml key=livedebug_flash_open_settings（已授权状态下的按钮文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Global flash (system-wide)",
      "text_zh": "全局闪烁提示（全系统）",
      "source_location": "res/values/strings.xml key=title_global_flash",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Installed outside the Play Store, Android may block the \"Modify system settings\" toggle below (and \"Usage access\", for per-app rules) — it looks greyed out or shows \"Restricted setting\". Tap it anyway; that usually shows the unlock prompt. If not, open App info → ⋮ menu → \"Allow restricted settings\", then return here.",
      "text_zh": "由于不是从 Play 商店安装，Android 可能屏蔽下方的“修改系统设置”开关（以及按应用规则用的“使用情况访问”）——它看起来是灰的或显示“受限设置”。可以照常点它，通常会弹出解锁提示；若仍不行，打开应用信息 → ⋮ 菜单 →“允许受限设置”，然后回到这里。",
      "source_location": "res/values/strings.xml key=onboarding_restricted_body（OnboardingScreenKt$RestrictedSettingsCard$1 渲染；对象为 WRITE_SETTINGS / 使用情况访问，非无障碍）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Skip for now",
      "text_zh": "暂时跳过",
      "source_location": "res/values/strings.xml key=onboarding_skip（Onboarding 页）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性安全降级：不开启无障碍时，GlobalFlashCard 状态保持 Off (foreground only)，浮层提示仅在本应用前台显示；返回或拒绝授权后无 onResume 重跳、无定时器拉起、无弹窗催促，用户可随时再次点击进入设置",
    "overlay_or_fake_settings": "无。仅有授权后由无障碍服务自身绘制的底部小标签（TYPE_ACCESSIBILITY_OVERLAY，2.5 秒自动消失、可点击关闭），不是叠在系统设置页上的引导遮罩，也不是高仿系统开关页",
    "restricted_settings_13plus_coaching": "存在但对象不同：Onboarding 页 onboarding_restricted_body 教用户对「修改系统设置（WRITE_SETTINGS）」与「使用情况访问」在应用信息 → ⋮ → Allow restricted settings 解锁；无障碍权限本身未做任何受限设置绕过教学，也未涉及 Session 安装器",
    "post_grant_anti_removal": "无。onServiceConnected() 仅获取 WindowManager 并向 AabFlash 注册展示器；未调用 performGlobalAction(GLOBAL_ACTION_BACK/HOME)、未监听设置页、未自行改写 enabled_accessibility_services",
    "benign_graceful_degradation": "有：无障碍完全可选，不开启时提示降级为前台内显示；亮度控制主链路走 WRITE_SETTINGS / ADB / Shizuku 通道，与无障碍服务无关"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 的瞬间（唯一入口在 Live Debug 页 GlobalFlashCard 按钮），以及冷启动进入 MainActivity 后 Onboarding「Setup & Permissions」页渲染时",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页（Onboarding Setup & Permissions）",
        "page_identifier": "MainActivity / com.tideo.autobrightness.app.ui.onboarding.OnboardingScreenKt，含“Setup & Permissions”标题与第 1–5 步权限卡片",
        "why_most_useful": "用于判断是否存在冷启动即推销无障碍、是否强制不可跳过；本应用此页完全不提无障碍，可据此排除 TRIG_COLD_START_BLOCK",
        "observable_utg_signals": ["是否出现“Skip for now”可跳过按钮", "权限步骤是否包含无障碍服务项", "是否出现“Allow restricted settings”教学卡片及其对象权限"]
      },
      {
        "page_role": "跳转前说明页（Live Debug → Global flash 卡片）",
        "page_identifier": "Live Debug 页，含“Global flash (system-wide)”标题与“Show debug/context flashes over other apps via an optional Accessibility overlay”说明",
        "why_most_useful": "这是唯一的无障碍引导入口，可直接判定触发时机为按需、文案是否坦白限定能力范围",
        "observable_utg_signals": ["是否含“never reads screen content”类隐私/能力承诺", "按钮文案是 Enable/Open Accessibility settings 还是伪造的“立即修复/开启优化”", "状态行是否显示 Off (foreground only)"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已下载/已安装的服务，条目名“Auto Brightness global flashes”，副标题为 global_toasts_a11y_description 全文",
        "why_most_useful": "核对系统侧展示名与描述是否与包名/应用名一致，是否存在同形字或夸大诱导描述",
        "observable_utg_signals": ["服务名是否为“Auto Brightness global flashes”而非冒充系统组件", "描述是否明示 optional 与 never reads screen content", "是否出现空白/换行将风险提示挤出可视区域"]
      },
      {
        "page_role": "获权后浮层展示页",
        "page_identifier": "其他应用前台时的底部小标签（TYPE_ACCESSIBILITY_OVERLAY，gravity=BOTTOM，约 80dp 上移）",
        "why_most_useful": "验证浮层内容仅为本地 flash_* 状态文案、是否覆盖关键 UI 或诱导点击",
        "observable_utg_signals": ["浮层文本是否为本地状态字符串（如 High Brightness Mode activated）", "浮层是否约 2.5 秒自动消失、点击即关闭", "浮层是否遮挡其他应用的敏感控件或含诱导按钮"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。该应用静态加壳初判为 False，assets 仅含 dexopt 产物、native 仅 androidx.graphics.path 与 datastore shared counter 两个标准库，运行期无远端下发或二次解密；唯一需注意的判别点是 onboarding_restricted_body 的受限设置教学，其对象是 WRITE_SETTINGS/使用情况访问而非无障碍，不应误判为无障碍受限设置绕过。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.tideo.autobrightness.app.ui.screens.LiveDebugScreenKt#LiveDebugScreen$lambda$12$lambda$11",
    "com.tideo.autobrightness.app.ui.screens.LiveDebugScreenKt$GlobalFlashCard$1$2#invoke",
    "com.tideo.autobrightness.app.state.LiveDebugViewModel#isGlobalToastServiceEnabled",
    "com.tideo.autobrightness.app.runtime.AabToastAccessibilityService#onServiceConnected",
    "com.tideo.autobrightness.app.runtime.AabToastAccessibilityService#showOverlay",
    "res/xml/aab_accessibility_service.xml"
  ]
}
```

</details>
