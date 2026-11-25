# BN_070__25a7c475de｜隐私指示与安全防护工具 — Privacy Flip

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：119.7s

## 1. 一句话核心结论

- **核心申请方式**：Privacy Flip 在主界面以一张标注「实验性」的锁屏检测卡片配合开关和「Open Accessibility Settings」按钮，由用户主动开启后才跳转系统无障碍设置页，并在返回时用 Secure 设置真实状态显示提示或成功，无强制弹窗、无遮罩、无受限设置教学、无撤权阻止。
- **静态可见性说明**：全部引导与跳转逻辑静态可见：无障碍跳转点、服务配置、事件处理、布局与全部文案均在 classes.dex / res/xml / res/layout / res/values 中直接可读；assets/main.jar 仅含分 dex classes.dex，无远端 HTML、无加密载荷、无加壳（apkid 初判 False）。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `25a7c475de640bf5ceb5c1ef3d0a2c65cbfc049a4fb06125840d9046be62b301` |
| 包名 / 年份 | `io.github.dorumrr.privacyflip` / 2025-2026 |
| 家族 / 品类 | **隐私指示与安全防护工具**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/io.github.dorumrr.privacyflip_38.apk |
| 桌面显示名 | Privacy Flip |
| 引导页宣称品牌/身份 | Privacy Flip（F-Droid 开源隐私开关工具，作者 dorumrr，GitHub 仓库 github.com/dorumrr/privacyFlip） |
| 系统无障碍列表服务名 | Privacy Flip - Lock Screen Detection |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。代码经 R8 名称混淆（如 zf、MainFragment#W）但语义可还原；服务标签、android:description、settingsActivity 均指向真实包名与 MainActivity，无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool 标志（全包未出现 isAccessibilityTool 字符串）。 |
| 无障碍服务类名 | `io.github.dorumrr.privacyflip.accessibility.PrivacyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `PACKAGE_USAGE_STATS, QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |
| 系统设置项说明 (`android:description`) | Lets Privacy Flip notice the lock screen appearing and going away, as an extra signal next to the screen on/off events, and cancel lock actions an unlock made unnecessary. This service does not read screen content or passwords. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | io.github.dorumrr.privacyflip.MainActivity（portrait，Theme.PrivacyFlip）承载 MainFragment 主界面 | LAUNCHER 冷启动 → Activity.onCreate 加载主界面布局（含无障碍卡片） | 原生Activity | **原文**：无自动弹出文案（主界面常态渲染）<br>**译注**：冷启动不弹任何权限引导，直接进入主功能页 | 无强制操作，用户可自由浏览/离开 | `io.github.dorumrr.privacyflip.MainActivity.onCreate；io.github.dorumrr.privacyflip.ui.fragment.MainFragment#D` |
| 2 | 引导说明页 | 主界面内嵌 CardView「Lock Screen Detection (Experimental)」卡片（layout/card_accessibility_service.xml） | 主界面渲染时卡片可见（CardView setVisibility(0)），文案来自 strings 资源 | 原生Activity | **原文**：Lock Screen Detection (Experimental) / Enable Accessibility Service as an extra lock and unlock signal / Enable Lock Screen Detection / Open Accessibility Settings / Notices the lock screen appearing and going away, as an extra signal next to the screen on/off events, and cancels lock actions an unlock made unnecessary. Does not read screen content.<br>**译注**：锁屏检测（实验性）；将无障碍服务作为额外的锁屏/解锁信号；启用锁屏检测；打开无障碍设置；该服务仅感知锁屏出现与消失作为亮灭屏之外的补充信号，并取消已无必要的锁动作，不读取屏幕内容。 | 用户可自行拨动开关或点击按钮，也可完全忽略；卡片无取消阻塞语义 | `res/layout/card_accessibility_service.xml#L7-L17；res/values/strings.xml#L30-L33` |
| 3 | 业务功能触发 | MainFragment 中 accessibilityServiceSwitch（SwitchCompat） | 用户拨动开关 → Bf#onCheckedChanged case 4 → 写入 SharedPreferences "accessibility_service_enabled" 并调用 MainFragment#W() 刷新状态 | 原生Activity | **原文**：Accessibility service preference updated:<br>**译注**：记录用户偏好「是否启用无障碍锁屏检测」，仅本地保存，不上报 | 用户主动开启开关；关闭即彻底停用该功能 | `Bf#onCheckedChanged；io.github.dorumrr.privacyflip.ui.fragment.MainFragment#W` |
| 4 | 拒权反馈循环 | 卡片内 TextView accessibilityServiceStatus + Button openAccessibilitySettingsButton | MainFragment#W() 读取 Settings.Secure.enabled_accessibility_services 判断实际是否开启；偏好已开但系统未开时显示提示并露出按钮 | 原生Activity | **原文**：⚠️ Please enable in Accessibility Settings<br>**译注**：⚠️ 请在无障碍设置中启用（仅静态提示，无死循环重跳、无定时拉起） | 用户可再次点击按钮跳转，或直接放弃；无阻塞 | `io.github.dorumrr.privacyflip.ui.fragment.MainFragment#W` |
| 5 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（系统无障碍服务列表） | 用户点击「Open Accessibility Settings」按钮 → zf#onClick case 10 → startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS") + FLAG_ACTIVITY_NEW_TASK) | 系统无障碍页 | **原文**：Opened Accessibility Settings（日志）；列表项显示 Privacy Flip - Lock Screen Detection / Lets Privacy Flip notice the lock screen appearing and going away, as an extra signal next to the screen on/off events, and cancel lock actions an unlock made unnecessary. This service does not read screen content or passwords.<br>**译注**：跳转到系统无障碍列表，用户看到条目「Privacy Flip - 锁屏检测」，说明为：让 Privacy Flip 感知锁屏出现与消失，作为亮灭屏之外的补充信号，并取消已无必要的锁动作；本服务不读取屏幕内容或密码。 | 由用户手动在系统页打开该服务开关（应用无自动点击/无悬浮遮罩指引） | `zf#onClick（case 10）；res/xml/accessibility_service_config.xml；res/values/strings.xml#L32-L33` |
| 6 | 获权后动作 | PrivacyAccessibilityService（BIND_ACCESSIBILITY_SERVICE，typeWindowStateChanged） | onServiceConnected 置位 c=true；onAccessibilityEvent 仅处理 eventType==32 且类名含 Keyguard/LockScreen，并用 KeyguardManager.isKeyguardLocked() 复核后触发锁/解锁延时逻辑 | 原生Activity | **原文**：✅ Service Active - Lock screen detection enabled<br>**译注**：✅ 服务已激活 - 锁屏检测已启用（回到应用仅刷新状态文案） | 无需进一步操作；用户可随时在系统设置关闭，应用无阻止或自恢复行为 | `io.github.dorumrr.privacyflip.accessibility.PrivacyAccessibilityService#onServiceConnected / #onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 主界面内嵌 CardView（res/layout/card_accessibility_service.xml）：标题「Lock Screen Detection (Experimental)」、副标题 accessibility_service_card_subtitle、开关行「Enable Lock Screen Detection」、按钮「Open Accessibility Settings」、脚注 accessibility_service_card_description
- 卡片状态 TextView accessibilityServiceStatus（运行时由 MainFragment#W() 设置）：⚠️ Please enable in Accessibility Settings / ✅ Service Active - Lock screen detection enabled
- 系统无障碍列表条目：android:label=@string/accessibility_service_label（Privacy Flip - Lock Screen Detection）、android:description=@string/accessibility_service_description（含「不读取屏幕内容或密码」声明），经 res/xml/accessibility_service_config.xml 绑定
- Toast/日志类辅助提示（非权限诱导）：Opened Accessibility Settings、Please allow Privacy Flip to run in background、Unable to open battery settings 等
- 其余说明性 AlertDialog（Airplane Mode (Experimental)、Battery Saver Info、Camera & Microphone Info、ExemptAppsDialog）与无障碍申请无关联
- 未发现 WebView / assets HTML / 悬浮窗 / 高仿系统开关页承载引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Lock Screen Detection (Experimental) | 锁屏检测（实验性） | `res/layout/card_accessibility_service.xml#L7（硬编码）` | 良性透明说明 |
| en | Enable Accessibility Service as an extra lock and unlock signal | 将无障碍服务作为额外的锁屏/解锁信号启用 | `res/values/strings.xml#L31（accessibility_service_card_subtitle）` | 良性透明说明 |
| en | Notices the lock screen appearing and going away, as an extra signal next to the screen on/off events, and cancels lock actions an unlock made unnecessary. Does not read screen content. | 感知锁屏的出现与消失，作为亮灭屏事件之外的补充信号，并取消解锁后已无必要的锁动作。不读取屏幕内容。 | `res/values/strings.xml#L30（accessibility_service_card_description）` | 良性透明说明 |
| en | Lets Privacy Flip notice the lock screen appearing and going away, as an extra signal next to the screen on/off events, and cancel lock actions an unlock made unnecessary. This service does not read screen content or passwords. | 让 Privacy Flip 感知锁屏的出现与消失，作为亮灭屏事件之外的补充信号，并取消解锁后已无必要的锁动作。本服务不读取屏幕内容或密码。 | `res/values/strings.xml#L32（accessibility_service_description，系统无障碍列表展示）` | 隐私承诺 |
| en | Privacy Flip - Lock Screen Detection | Privacy Flip - 锁屏检测 | `res/values/strings.xml#L33（accessibility_service_label）` | 良性透明说明 |
| en | Open Accessibility Settings | 打开无障碍设置 | `res/layout/card_accessibility_service.xml#L16（硬编码）` | 良性透明说明 |
| en | ⚠️ Please enable in Accessibility Settings | ⚠️ 请在无障碍设置中启用 | `MainFragment#W() 硬编码` | 良性透明说明 |
| en | ✅ Service Active - Lock screen detection enabled | ✅ 服务已激活 - 锁屏检测已启用 | `MainFragment#W() 硬编码` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：良性安全降级：MainFragment#W() 在回到界面时仅比对 Settings.Secure.enabled_accessibility_services 与 "<包名>/.accessibility.PrivacyAccessibilityService"，未开启则显示「⚠️ Please enable in Accessibility Settings」并露出按钮，用户可无限期忽略；无 onResume 强制重跳、无定时器轮询拉起、无退出即重弹。
- **遮罩叠层 / 高仿系统设置页**：无。未使用 SYSTEM_ALERT_WINDOW，无悬浮窗、无半透明遮罩、无高仿系统无障碍开关页；跳转后即为真实系统设置页。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包未出现 ACTION_APPLICATION_DETAILS_SETTINGS，也无「右上角菜单允许受限设置」类文案或 Session 安装器绕过；targetSdk 35 下若系统施加受限设置限制，应用不提供绕过指引。
- **获权后即时行为与防撤权机制**：无。服务内无 performGlobalAction(GLOBAL_ACTION_BACK/HOME)、无监听设置页、无自点确认；onAccessibilityEvent 仅处理 eventType 32 的 Keyguard/LockScreen 判定，撤权即自然失效。
- **良性降级 / 替代方案**：有。无障碍属可选增强：偏好默认 false，服务端 onAccessibilityEvent 首先校验 accessibility_service_enabled，关闭时直接忽略事件；应用核心隐私开关功能依赖亮灭屏/锁屏广播与 Shizuku/Dhizuku、快捷磁贴、桌面小部件等替代路径，无障碍仅作为「额外的锁屏/解锁信号」。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在检测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（即用户点击「Open Accessibility Settings」后）拉起 UTG，同时保留点击前的 MainFragment 主界面卡片页面；另可在冷启动后主界面渲染完成即抓取一次基线，用于对比是否存在卡片状态文案变化。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导全为本地文本控件与 strings 资源，无纯图空文本页面、无远端 HTML、无加壳（静态加壳亦不影响运行期 UTG）。唯一弱信号是代码经 R8 混淆（zf、MainFragment#W），但文案与跳转逻辑均可静态还原；若需确认 Shizuku/Dhizuku 分支是否触发额外设置跳转，需在已授权环境下观测，与本命题（无障碍申请）无冲突。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **主界面无障碍引导卡片页（点击前基线）** | MainActivity / MainFragment，含文本「Lock Screen Detection (Experimental)」「Enable Lock Screen Detection」及 SwitchCompat 与「Open Accessibility Settings」按钮 | 这是该应用唯一的无障碍引导载体，可直接判定引导是否为嵌入式可忽略卡片而非强制弹窗/遮罩 | 卡片标题与「(Experimental)」字样；是否存在关闭/取消控件（无则说明本就不阻塞）；按钮文案「Open Accessibility Settings」及其可见性 |
| **跳转前状态提示（拒权反馈）** | 卡片内 accessibilityServiceStatus TextView，文本「⚠️ Please enable in Accessibility Settings」 | 区分「一次提示+按钮」与「死循环重跳」两类诱导，是判定拒权反馈性质的关键页面 | 提示文案原文与颜色；是否伴随遮罩或浮层；返回后是否立即再次自动跳转（可多次返回观测） |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载/已安装服务，条目「Privacy Flip - Lock Screen Detection」及其说明摘要 | 核对系统页展示的服务名与描述是否与应用内宣称一致，验证无身份混淆或功能范围夸大 | 服务条目显示名；描述文本是否包含「不读取屏幕内容或密码」；是否被系统标记为受限设置条目 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `zf#onClick（case 10：startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS") + FLAG_ACTIVITY_NEW_TASK)）`
- `io.github.dorumrr.privacyflip.ui.fragment.MainFragment#W（Settings.Secure.enabled_accessibility_services 状态核对与提示文案）`
- `Bf#onCheckedChanged（case 4：写入 SharedPreferences accessibility_service_enabled）`
- `io.github.dorumrr.privacyflip.accessibility.PrivacyAccessibilityService#onAccessibilityEvent（eventType 32 + Keyguard/LockScreen + KeyguardManager 复核）`
- `res/xml/accessibility_service_config.xml（canRetrieveWindowContent=false、typeWindowStateChanged、settingsActivity=MainActivity）`
- `res/layout/card_accessibility_service.xml#L7-L17 / res/values/strings.xml#L30-L33`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（受限于本轮工具预算，已在核实无障碍跳转链、服务配置、事件处理、布局与字符串后收口）。

## 结论要点

- **触发方式：按需功能开关，非冷启动强制拦截。** 无障碍能力是主界面上一张普通 CardView（`Lock Screen Detection (Experimental)`），内含 `SwitchCompat`（`accessibilityServiceSwitch`）与按钮 `Open Accessibility Settings`；用户打开开关后才把偏好 `accessibility_service_enabled` 写入 SharedPreferences，并刷新状态文案。没有冷启动弹窗、没有不可取消对话框、没有悬浮遮罩。
- **跳转点唯一且透明。** 唯一跳系统设置的位置是 [zf#onClick](<resource-unit:#1.dex1 code:zf#onClick>) 的 `case 10`：`new Intent("android.settings.ACCESSIBILITY_SETTINGS")` + `FLAG_ACTIVITY_NEW_TASK`，并打日志 `Opened Accessibility Settings`。全包未出现 `ACTION_APPLICATION_DETAILS_SETTINGS`，即**不存在 Android 13+「受限设置」分步教学**，也无 Session 安装器绕过。
- **拒权反馈是温和降级，不是循环重跳。** [MainFragment#W()](<resource-unit:#1.dex1 code:io.github.dorumrr.privacyflip.ui.fragment.MainFragment#W>) 通过 `Settings.Secure.enabled_accessibility_services` 判断真实开启状态：未开时显示 `⚠️ Please enable in Accessibility Settings` 并露出「打开设置」按钮；已开显示 `✅ Service Active - Lock screen detection enabled` 并隐藏按钮。回到应用只做一次状态刷新，无 `onResume` 死循环、无定时器重拉。
- **身份与用途诚实一致。** 桌面名 `Privacy Flip`；系统无障碍列表显示 `Privacy Flip - Lock Screen Detection`；[accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 明确 `android:canRetrieveWindowContent="false"`、仅 `typeWindowStateChanged`、`settingsActivity=MainActivity`，说明文字直述「不读取屏幕内容或密码」。
- **服务行为与声明相符。** [PrivacyAccessibilityService#onAccessibilityEvent()](<resource-unit:#1.dex1 code:io.github.dorumrr.privacyflip.accessibility.PrivacyAccessibilityService#onAccessibilityEvent>) 只处理事件类型 32，比对 `Keyguard`/`LockScreen` 类名并用 `KeyguardManager.isKeyguardLocked()` 交叉确认；偏好关闭时直接忽略事件。无 `performGlobalAction`、无手势分发、无自点确认、无阻止撤权逻辑。
- **无 WebView/HTML/远端引导。** 引导文字全部为本地 `res/values/strings.xml` 与 `res/layout/card_accessibility_service.xml`；`assets/` 下只有 `dexopt/` 与 `main.jar`（内含一个 `classes.dex` 分 dex，非远端 HTML 载荷）。
- **判定：** 属透明、可取消、可降级的良性无障碍申请路径，未发现诱导、变脸或恶意能力，故不登记风险。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导与跳转逻辑静态可见：无障碍跳转点、服务配置、事件处理、布局与全部文案均在 classes.dex / res/xml / res/layout / res/values 中直接可读；assets/main.jar 仅含分 dex classes.dex，无远端 HTML、无加密载荷、无加壳（apkid 初判 False）。",
  "summary_one_liner": "Privacy Flip 在主界面以一张标注「实验性」的锁屏检测卡片配合开关和「Open Accessibility Settings」按钮，由用户主动开启后才跳转系统无障碍设置页，并在返回时用 Secure 设置真实状态显示提示或成功，无强制弹窗、无遮罩、无受限设置教学、无撤权阻止。",
  "disguise_identity": {
    "app_display_name": "Privacy Flip",
    "claimed_brand_or_persona": "Privacy Flip（F-Droid 开源隐私开关工具，作者 dorumrr，GitHub 仓库 github.com/dorumrr/privacyFlip）",
    "a11y_service_label": "Privacy Flip - Lock Screen Detection",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。代码经 R8 名称混淆（如 zf、MainFragment#W）但语义可还原；服务标签、android:description、settingsActivity 均指向真实包名与 MainActivity，无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool 标志（全包未出现 isAccessibilityTool 字符串）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "io.github.dorumrr.privacyflip.MainActivity（portrait，Theme.PrivacyFlip）承载 MainFragment 主界面",
      "trigger_event": "LAUNCHER 冷启动 → Activity.onCreate 加载主界面布局（含无障碍卡片）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无自动弹出文案（主界面常态渲染）",
      "shown_text_zh": "冷启动不弹任何权限引导，直接进入主功能页",
      "user_action_requested": "无强制操作，用户可自由浏览/离开",
      "code_anchor": "io.github.dorumrr.privacyflip.MainActivity.onCreate；io.github.dorumrr.privacyflip.ui.fragment.MainFragment#D"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "主界面内嵌 CardView「Lock Screen Detection (Experimental)」卡片（layout/card_accessibility_service.xml）",
      "trigger_event": "主界面渲染时卡片可见（CardView setVisibility(0)），文案来自 strings 资源",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Lock Screen Detection (Experimental) / Enable Accessibility Service as an extra lock and unlock signal / Enable Lock Screen Detection / Open Accessibility Settings / Notices the lock screen appearing and going away, as an extra signal next to the screen on/off events, and cancels lock actions an unlock made unnecessary. Does not read screen content.",
      "shown_text_zh": "锁屏检测（实验性）；将无障碍服务作为额外的锁屏/解锁信号；启用锁屏检测；打开无障碍设置；该服务仅感知锁屏出现与消失作为亮灭屏之外的补充信号，并取消已无必要的锁动作，不读取屏幕内容。",
      "user_action_requested": "用户可自行拨动开关或点击按钮，也可完全忽略；卡片无取消阻塞语义",
      "code_anchor": "res/layout/card_accessibility_service.xml#L7-L17；res/values/strings.xml#L30-L33"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "MainFragment 中 accessibilityServiceSwitch（SwitchCompat）",
      "trigger_event": "用户拨动开关 → Bf#onCheckedChanged case 4 → 写入 SharedPreferences \"accessibility_service_enabled\" 并调用 MainFragment#W() 刷新状态",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Accessibility service preference updated: ",
      "shown_text_zh": "记录用户偏好「是否启用无障碍锁屏检测」，仅本地保存，不上报",
      "user_action_requested": "用户主动开启开关；关闭即彻底停用该功能",
      "code_anchor": "Bf#onCheckedChanged；io.github.dorumrr.privacyflip.ui.fragment.MainFragment#W"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "卡片内 TextView accessibilityServiceStatus + Button openAccessibilitySettingsButton",
      "trigger_event": "MainFragment#W() 读取 Settings.Secure.enabled_accessibility_services 判断实际是否开启；偏好已开但系统未开时显示提示并露出按钮",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "⚠️ Please enable in Accessibility Settings",
      "shown_text_zh": "⚠️ 请在无障碍设置中启用（仅静态提示，无死循环重跳、无定时拉起）",
      "user_action_requested": "用户可再次点击按钮跳转，或直接放弃；无阻塞",
      "code_anchor": "io.github.dorumrr.privacyflip.ui.fragment.MainFragment#W"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（系统无障碍服务列表）",
      "trigger_event": "用户点击「Open Accessibility Settings」按钮 → zf#onClick case 10 → startActivity(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + FLAG_ACTIVITY_NEW_TASK)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Opened Accessibility Settings（日志）；列表项显示 Privacy Flip - Lock Screen Detection / Lets Privacy Flip notice the lock screen appearing and going away, as an extra signal next to the screen on/off events, and cancel lock actions an unlock made unnecessary. This service does not read screen content or passwords.",
      "shown_text_zh": "跳转到系统无障碍列表，用户看到条目「Privacy Flip - 锁屏检测」，说明为：让 Privacy Flip 感知锁屏出现与消失，作为亮灭屏之外的补充信号，并取消已无必要的锁动作；本服务不读取屏幕内容或密码。",
      "user_action_requested": "由用户手动在系统页打开该服务开关（应用无自动点击/无悬浮遮罩指引）",
      "code_anchor": "zf#onClick（case 10）；res/xml/accessibility_service_config.xml；res/values/strings.xml#L32-L33"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "PrivacyAccessibilityService（BIND_ACCESSIBILITY_SERVICE，typeWindowStateChanged）",
      "trigger_event": "onServiceConnected 置位 c=true；onAccessibilityEvent 仅处理 eventType==32 且类名含 Keyguard/LockScreen，并用 KeyguardManager.isKeyguardLocked() 复核后触发锁/解锁延时逻辑",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "✅ Service Active - Lock screen detection enabled",
      "shown_text_zh": "✅ 服务已激活 - 锁屏检测已启用（回到应用仅刷新状态文案）",
      "user_action_requested": "无需进一步操作；用户可随时在系统设置关闭，应用无阻止或自恢复行为",
      "code_anchor": "io.github.dorumrr.privacyflip.accessibility.PrivacyAccessibilityService#onServiceConnected / #onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "主界面内嵌 CardView（res/layout/card_accessibility_service.xml）：标题「Lock Screen Detection (Experimental)」、副标题 accessibility_service_card_subtitle、开关行「Enable Lock Screen Detection」、按钮「Open Accessibility Settings」、脚注 accessibility_service_card_description",
    "卡片状态 TextView accessibilityServiceStatus（运行时由 MainFragment#W() 设置）：⚠️ Please enable in Accessibility Settings / ✅ Service Active - Lock screen detection enabled",
    "系统无障碍列表条目：android:label=@string/accessibility_service_label（Privacy Flip - Lock Screen Detection）、android:description=@string/accessibility_service_description（含「不读取屏幕内容或密码」声明），经 res/xml/accessibility_service_config.xml 绑定",
    "Toast/日志类辅助提示（非权限诱导）：Opened Accessibility Settings、Please allow Privacy Flip to run in background、Unable to open battery settings 等",
    "其余说明性 AlertDialog（Airplane Mode (Experimental)、Battery Saver Info、Camera & Microphone Info、ExemptAppsDialog）与无障碍申请无关联",
    "未发现 WebView / assets HTML / 悬浮窗 / 高仿系统开关页承载引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Lock Screen Detection (Experimental)",
      "text_zh": "锁屏检测（实验性）",
      "source_location": "res/layout/card_accessibility_service.xml#L7（硬编码）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Service as an extra lock and unlock signal",
      "text_zh": "将无障碍服务作为额外的锁屏/解锁信号启用",
      "source_location": "res/values/strings.xml#L31（accessibility_service_card_subtitle）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Notices the lock screen appearing and going away, as an extra signal next to the screen on/off events, and cancels lock actions an unlock made unnecessary. Does not read screen content.",
      "text_zh": "感知锁屏的出现与消失，作为亮灭屏事件之外的补充信号，并取消解锁后已无必要的锁动作。不读取屏幕内容。",
      "source_location": "res/values/strings.xml#L30（accessibility_service_card_description）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Lets Privacy Flip notice the lock screen appearing and going away, as an extra signal next to the screen on/off events, and cancel lock actions an unlock made unnecessary. This service does not read screen content or passwords.",
      "text_zh": "让 Privacy Flip 感知锁屏的出现与消失，作为亮灭屏事件之外的补充信号，并取消解锁后已无必要的锁动作。本服务不读取屏幕内容或密码。",
      "source_location": "res/values/strings.xml#L32（accessibility_service_description，系统无障碍列表展示）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Privacy Flip - Lock Screen Detection",
      "text_zh": "Privacy Flip - 锁屏检测",
      "source_location": "res/values/strings.xml#L33（accessibility_service_label）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Accessibility Settings",
      "text_zh": "打开无障碍设置",
      "source_location": "res/layout/card_accessibility_service.xml#L16（硬编码）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "⚠️ Please enable in Accessibility Settings",
      "text_zh": "⚠️ 请在无障碍设置中启用",
      "source_location": "MainFragment#W() 硬编码",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "✅ Service Active - Lock screen detection enabled",
      "text_zh": "✅ 服务已激活 - 锁屏检测已启用",
      "source_location": "MainFragment#W() 硬编码",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "良性安全降级：MainFragment#W() 在回到界面时仅比对 Settings.Secure.enabled_accessibility_services 与 \"<包名>/.accessibility.PrivacyAccessibilityService\"，未开启则显示「⚠️ Please enable in Accessibility Settings」并露出按钮，用户可无限期忽略；无 onResume 强制重跳、无定时器轮询拉起、无退出即重弹。",
    "overlay_or_fake_settings": "无。未使用 SYSTEM_ALERT_WINDOW，无悬浮窗、无半透明遮罩、无高仿系统无障碍开关页；跳转后即为真实系统设置页。",
    "restricted_settings_13plus_coaching": "无。全包未出现 ACTION_APPLICATION_DETAILS_SETTINGS，也无「右上角菜单允许受限设置」类文案或 Session 安装器绕过；targetSdk 35 下若系统施加受限设置限制，应用不提供绕过指引。",
    "post_grant_anti_removal": "无。服务内无 performGlobalAction(GLOBAL_ACTION_BACK/HOME)、无监听设置页、无自点确认；onAccessibilityEvent 仅处理 eventType 32 的 Keyguard/LockScreen 判定，撤权即自然失效。",
    "benign_graceful_degradation": "有。无障碍属可选增强：偏好默认 false，服务端 onAccessibilityEvent 首先校验 accessibility_service_enabled，关闭时直接忽略事件；应用核心隐私开关功能依赖亮灭屏/锁屏广播与 Shizuku/Dhizuku、快捷磁贴、桌面小部件等替代路径，无障碍仅作为「额外的锁屏/解锁信号」。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在检测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（即用户点击「Open Accessibility Settings」后）拉起 UTG，同时保留点击前的 MainFragment 主界面卡片页面；另可在冷启动后主界面渲染完成即抓取一次基线，用于对比是否存在卡片状态文案变化。",
    "key_pages_to_capture": [
      {
        "page_role": "主界面无障碍引导卡片页（点击前基线）",
        "page_identifier": "MainActivity / MainFragment，含文本「Lock Screen Detection (Experimental)」「Enable Lock Screen Detection」及 SwitchCompat 与「Open Accessibility Settings」按钮",
        "why_most_useful": "这是该应用唯一的无障碍引导载体，可直接判定引导是否为嵌入式可忽略卡片而非强制弹窗/遮罩",
        "observable_utg_signals": [
          "卡片标题与「(Experimental)」字样",
          "是否存在关闭/取消控件（无则说明本就不阻塞）",
          "按钮文案「Open Accessibility Settings」及其可见性"
        ]
      },
      {
        "page_role": "跳转前状态提示（拒权反馈）",
        "page_identifier": "卡片内 accessibilityServiceStatus TextView，文本「⚠️ Please enable in Accessibility Settings」",
        "why_most_useful": "区分「一次提示+按钮」与「死循环重跳」两类诱导，是判定拒权反馈性质的关键页面",
        "observable_utg_signals": [
          "提示文案原文与颜色",
          "是否伴随遮罩或浮层",
          "返回后是否立即再次自动跳转（可多次返回观测）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载/已安装服务，条目「Privacy Flip - Lock Screen Detection」及其说明摘要",
        "why_most_useful": "核对系统页展示的服务名与描述是否与应用内宣称一致，验证无身份混淆或功能范围夸大",
        "observable_utg_signals": [
          "服务条目显示名",
          "描述文本是否包含「不读取屏幕内容或密码」",
          "是否被系统标记为受限设置条目"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导全为本地文本控件与 strings 资源，无纯图空文本页面、无远端 HTML、无加壳（静态加壳亦不影响运行期 UTG）。唯一弱信号是代码经 R8 混淆（zf、MainFragment#W），但文案与跳转逻辑均可静态还原；若需确认 Shizuku/Dhizuku 分支是否触发额外设置跳转，需在已授权环境下观测，与本命题（无障碍申请）无冲突。"
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
    "zf#onClick（case 10：startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\") + FLAG_ACTIVITY_NEW_TASK)）",
    "io.github.dorumrr.privacyflip.ui.fragment.MainFragment#W（Settings.Secure.enabled_accessibility_services 状态核对与提示文案）",
    "Bf#onCheckedChanged（case 4：写入 SharedPreferences accessibility_service_enabled）",
    "io.github.dorumrr.privacyflip.accessibility.PrivacyAccessibilityService#onAccessibilityEvent（eventType 32 + Keyguard/LockScreen + KeyguardManager 复核）",
    "res/xml/accessibility_service_config.xml（canRetrieveWindowContent=false、typeWindowStateChanged、settingsActivity=MainActivity）",
    "res/layout/card_accessibility_service.xml#L7-L17 / res/values/strings.xml#L30-L33"
  ]
}
```

</details>
