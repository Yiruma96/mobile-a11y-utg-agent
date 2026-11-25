# BN_004__3d1b87e523｜专注自律与防沉迷管控 — Nudge

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：160.9s

## 1. 一句话核心结论

- **核心申请方式**：在主界面以原生 Compose 卡片透明说明用途并提供按钮，点击后通过官方 ACTION_ACCESSIBILITY_SETTINGS 跳转系统无障碍列表，Android 13+ 额外提供跳应用详情页开启受限设置的分步说明，全程无弹窗逼迫、无遮罩、无拒权循环。
- **静态可见性说明**：全部引导逻辑位于 classes.dex 的 Compose 代码与 res/values/strings.xml、res/xml/accessibility_service_config.xml 中，无加壳、无加密资产、无远端 HTML 下发的引导页；唯一动态要素是系统无障碍开关状态（Settings.Secure 读取），属正常运行期状态查询。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3d1b87e5238ad6687eb5d90e3a594289fcacd2b29519c1718b6ffb1ee29aa48f` |
| 包名 / 年份 | `com.nitulshah.nudge` / 2025-2026 |
| 家族 / 品类 | **专注自律与防沉迷管控**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.nitulshah.nudge_18.apk |
| 桌面显示名 | Nudge |
| 引导页宣称品牌/身份 | Nudge（F-Droid 开源专注自律应用，真实名称，未冒充任何系统或第三方品牌） |
| 系统无障碍列表服务名 | Nudge Scroll Tracker |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。仅见常规 R8 类名混淆（S1.E/S1.u/S1.U/l2.a 等），未使用空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool；服务 label 与 app_name 语义一致。 |
| 无障碍服务类名 | `com.nitulshah.nudge.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Nudge counts your scrolls to help you track your phone use. It only learns that a scroll happened and in which app. It cannot read text or anything else on your screen. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.nitulshah.nudge.MainActivity（单 Activity + Jetpack Compose 界面） | LAUNCHER 启动 → onCreate()：初始化 FIRST_LAUNCH_DATE、注册午夜重置 Worker、按需申请 POST_NOTIFICATIONS、setContent 挂载 Compose 界面 | 原生Activity | **原文**：无（本步不呈现权限引导文案，仅进入主界面）<br>**译注**：冷启动直接进入 Nudge 主界面，无强制权限弹窗拦截 | 无强制操作；可自由浏览界面 | `com.nitulshah.nudge.MainActivity.onCreate` |
| 2 | 引导说明页 | 主界面内 Compose Card 卡片（S1.E 组合项） | 主界面渲染时组合执行，非弹窗、非独立 Activity | 原生Activity | **原文**：Turn on scroll tracking / Nudge counts scrolls and unlocks with an Android accessibility service. Nothing is tracked, and there's no score, until it's on. / Find Nudge under Downloaded apps (or Installed apps) and switch it on.<br>**译注**：开启滚动追踪 / Nudge 通过 Android 无障碍服务统计滚动与解锁次数。未开启前不追踪任何内容，也没有评分。/ 在「已下载的应用」（或「已安装的应用」）中找到 Nudge 并打开开关。 | 阅读说明后点击卡片内按钮进入下一步；卡片外可正常使用其他功能（无强制、无取消阻断） | `S1.E.d` |
| 3 | 跳受限设置 | 系统「应用信息」页（android.settings.APPLICATION_DETAILS_SETTINGS，package:com.nitulshah.nudge） | 点击卡片内受限设置说明下方按钮 → S1.u.c 分支 case 3，仅 SDK_INT>=33 显示 | 系统无障碍页 | **原文**：Is Nudge greyed out or showing "Restricted setting"? Open App info, tap the ⋮ menu, choose Allow restricted settings, then try again.<br>**译注**：Nudge 显示为灰色或提示「受限设置」？打开应用信息，点右上角 ⋮ 菜单，选择「允许受限设置」，然后重试。 | 进入应用详情页 → 右上角菜单 → 允许受限设置（无恐吓、无假故障包装，为 AOSP 官方路径说明） | `S1.u.c（case 3）+ S1.E.d（SDK>=33 分支）` |
| 4 | 跳无障碍设置 | 系统无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS） | 点击卡片主按钮 → S1.u.c 分支 case 2，以 FLAG_ACTIVITY_NEW_TASK 启动；另一路径 S1.U.c 在 canDrawOverlays 已授权且无障碍未启用时同样跳此页 | 系统无障碍页 | **原文**：Find Nudge under Downloaded apps (or Installed apps) and switch it on.<br>**译注**：在「已下载的应用」（或「已安装的应用」）分类下找到 Nudge，打开其开关。 | 在系统列表中手动找到「Nudge Scroll Tracker」并开启；可返回或放弃，无循环重跳 | `S1.u.c / S1.U.c` |
| 5 | 遮罩叠层指引 | 无。应用未在设置页上方叠加任何悬浮窗、半透明遮罩或高仿开关页 | 不适用 | 不可静态还原 | 无 | 无 | `S1.U.c（仅使用 MANAGE_OVERLAY_PERMISSION 官方跳转，未见 WindowManager 叠层绘制于设置页之上）` |
| 6 | 业务功能触发 | 可选「显示在其他应用上层」开关 → android.settings.action.MANAGE_OVERLAY_PERMISSION | 用户点击可选按钮（S1.u.c default 分支）或点击气泡开关而 canDrawOverlays 为 false（S1.U.c case 1） | 系统无障碍页 | **原文**：Optional: allow Display over other apps to show the floating scroll-count bubble.<br>**译注**：可选：允许「显示在其他应用上层」，以显示悬浮的滚动计数气泡。 | 可选授权悬浮窗权限；明确标注 Optional，拒绝不影响核心计数功能 | `S1.u.c（default 分支）/ S1.U.c（case 1）` |
| 7 | 获权后动作 | MyAccessibilityService（滚动事件计数）+ 悬浮气泡（_isBubbleVisible） | 系统绑定服务后 onAccessibilityEvent 计数；主界面再次进入时 l2.a.x 检测 accessibility_enabled 与 enabled_accessibility_services 判定已授权 | 悬浮窗Overlay | **原文**：You're scrolling fast / Take a breath? Tap to take a break.<br>**译注**：你滚动得太快了 / 需要喘口气吗？点击休息一下。 | 超阈值时点击通知或弹出 InterventionActivity 进入休息干预；无自授权、无阻止撤权行为 | `com.nitulshah.nudge.MyAccessibilityService.checkIntervention / l2.a.x` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 主界面内嵌 Compose Card 卡片（S1.E.d 渲染，非弹窗、非独立 Activity）：标题、用途说明、分类查找指引、受限设置教学、可选悬浮窗说明
- 系统无障碍列表中的服务项说明：res/values/strings.xml 的 accessibility_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用）
- 系统无障碍列表中的服务名称：AndroidManifest.xml 中 service 的 android:label="Nudge Scroll Tracker"
- 跳转至系统无障碍设置页 / 应用详情页 / 悬浮窗权限页后由系统 UI 呈现，应用本身不在其上叠加任何文案
- 超阈值干预通知与 InterventionActivity："You're scrolling fast" / "Take a breath? Tap to take a break."（属功能提醒，非权限引导）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Nudge counts your scrolls to help you track your phone use. It only learns that a scroll happened and in which app. It cannot read text or anything else on your screen. | Nudge 统计你的滚动次数，帮助你了解手机使用情况。它只会知道发生了一次滚动以及发生在哪个应用里，无法读取屏幕上的文字或其他任何内容。 | `res/values/strings.xml: accessibility_description（经 res/xml/accessibility_service_config.xml android:description 引用，显示于系统无障碍列表）` | 隐私承诺 |
| en | Turn on scroll tracking | 开启滚动追踪 | `S1.E.d（硬编码 Compose 文案）` | 良性透明说明 |
| en | Nudge counts scrolls and unlocks with an Android accessibility service. Nothing is tracked, and there's no score, until it's on. | Nudge 通过 Android 无障碍服务统计滚动与解锁次数。在开启之前不会追踪任何内容，也不会生成评分。 | `S1.E.d（硬编码 Compose 文案）` | 良性透明说明 |
| en | Find Nudge under Downloaded apps (or Installed apps) and switch it on. | 在「已下载的应用」（或「已安装的应用」）中找到 Nudge 并打开开关。 | `S1.E.d（硬编码 Compose 文案）` | 受限设置分步教学 |
| en | Is Nudge greyed out or showing "Restricted setting"? Open App info, tap the ⋮ menu, choose Allow restricted settings, then try again. | Nudge 显示为灰色或提示「受限设置」？打开应用信息，点右上角 ⋮ 菜单，选择「允许受限设置」，然后重试。 | `S1.E.d（SDK_INT>=33 分支，硬编码 Compose 文案）` | 受限设置分步教学 |
| en | Optional: allow Display over other apps to show the floating scroll-count bubble. | 可选：允许「显示在其他应用上层」，以显示悬浮的滚动计数气泡。 | `S1.E.d（硬编码 Compose 文案）` | 良性透明说明 |
| en | You're scrolling fast | 你滚动得太快了 | `com.nitulshah.nudge.MyAccessibilityService.checkIntervention（通知标题硬编码）` | 良性透明说明 |
| en | Take a breath? Tap to take a break. | 需要喘口气吗？点击休息一下。 | `com.nitulshah.nudge.MyAccessibilityService.checkIntervention（通知正文硬编码）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无拒权循环。MainActivity.onResume 仅读取 NudgePrefs 的 LAST_SCROLL_DATE 与 DayBoundary.today() 做跨日计数重置，不做无障碍状态重定向；用户从系统设置返回后停留在原主界面卡片，功能降级为无计数、无评分，无 Timer 定时重跳、无 onResume 死循环重跳。
- **遮罩叠层 / 高仿系统设置页**：无。未绘制半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于可选的滚动计数气泡（_isBubbleVisible），且文案明确标注 Optional。跳转均使用官方 ACTION，落点为真实系统页面。
- **Android 13+ 受限设置（Restricted Settings）应对**：有，但为官方路径透明说明：SDK_INT>=33 时卡片显示「Is Nudge greyed out or showing "Restricted setting"? Open App info, tap the ⋮ menu, choose Allow restricted settings, then try again.」并配按钮跳转 android.settings.APPLICATION_DETAILS_SETTINGS（package:com.nitulshah.nudge）。无恐吓、无假故障、无 Session 安装器绕过、无伪造安装包投递。
- **获权后即时行为与防撤权机制**：无。MyAccessibilityService 未实现 GLOBAL_ACTION_BACK/HOME 阻止撤权，未监听设置页自动回跳，未自点确认或自授权。
- **良性降级 / 替代方案**：有。无障碍未开启时应用照常启动，仅不产生滚动计数、健康评分与干预提醒；悬浮气泡为显式 Optional 项；用户可选择只用界面内手动查看，权限获取完全依赖用户在系统页自行开启。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以监测到 Intent action = android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的 startActivity 为触发点拉起 UTG；同时在冷启动后 1~2s 抓取一次主界面，确认引导为内嵌卡片而非强制弹窗。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。引导文案全部为 Compose 文本节点与 strings 资源，可被 UTG 直接提取，无需 OCR；未使用图片/GIF 引导、无远端 HTML、无静态加壳或密文二阶段载荷。唯一需注意的边界：无障碍配置订阅了 typeViewTextChanged，而描述声明不读取文本，若做运行期核验可重点确认服务事件处理是否仅取包名与滚动计数（静态侧未见节点文本读取与上报路径）。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后主界面引导卡片页** | com.nitulshah.nudge.MainActivity + Compose 卡片，可见文本节点 'Turn on scroll tracking' 与 'Nudge counts scrolls and unlocks with an Android accessibility service...' | 确认引导载体是内嵌卡片而非不可取消弹窗/WebView，是区分良性透明引导与诱导弹窗的第一判据 | 是否存在可关闭的 Dialog/全屏遮罩节点；卡片文案是否含隐私划界句 'It cannot read text'；是否存在 WebView 节点或 remote url |
| **受限设置教学分支页（Android 13+）** | 同卡片内 'Is Nudge greyed out or showing "Restricted setting"?' 文本 + 跳应用详情按钮 | 受限设置教学是诱导类高频信号，需确认其文案框架是官方路径说明还是恐吓/伪造更新 | 文案是否出现假更新/故障恐吓/假反诈用语；按钮是否指向 android.settings.APPLICATION_DETAILS_SETTINGS；是否存在悬浮遮罩覆盖系统菜单 |
| **跳转后系统无障碍服务列表项** | Settings 无障碍页中 'Nudge Scroll Tracker' 列表项及其 description 摘要 | 核对服务名与描述是否与真实功能一致，验证无身份冒充与空白/同形字挤出 | 服务 label 是否等于 Nudge Scroll Tracker；description 是否包含透明范围声明；是否存在多个同应用无障碍服务项（多 alias 伪装） |
| **获权后悬浮气泡与干预页** | 悬浮窗滚动计数气泡 + com.nitulshah.nudge.InterventionActivity（excludeFromRecents、Theme.Intervention） | 确认获权后行为限于计数展示与休息提醒，无后台静默操作、无读取屏文本上报 | 气泡是否仅显示数字；干预页是否出现外部跳转/广告/诱导安装；是否有向网络发送节点文本的流量 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `S1.E.d`
- `S1.u.c`
- `S1.U.c`
- `l2.a.x`
- `com.nitulshah.nudge.MainActivity.onResume`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（共 10 轮工具调用），结论如下。

## 分析结论

**性质判断：良性透明引导，未发现诱导/欺诈行为。**

- **无障碍入口唯一且常规**：Manifest 中仅声明 [MyAccessibilityService](<resource-unit:#1 manifest:components>)（`android:label="Nudge Scroll Tracker"`，绑定 `BIND_ACCESSIBILITY_SERVICE`），配置 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 仅订阅 `typeViewScrolled|typeViewTextChanged|typeWindowStateChanged`，`feedbackGeneric`、无 `flagRetrieveInteractiveWindows`、无 `canRetrieveWindowContent`。
- **系统描述逐字透明**：[strings.xml 第14行](<resource-unit:#1 file:res/values/strings.xml#L14>) 明确写“It only learns that a scroll happened and in which app. It cannot read text or anything else on your screen.”，属于主动划界，与 DEX 预筛的 `RESTRICTED_STR` 命中同源（即该说明文本本身）。
- **引导载体为原生 Compose 卡片，非弹窗/WebView/悬浮遮罩**：[S1.E#d](<resource-unit:#1.dex1 code:S1.E#d>) 在主页 `Card` 内渲染标题“Turn on scroll tracking”、说明文字与按钮；无 `AlertDialog`、无 `assets/*.html`、无 `WebView`、无叠层引导遮罩（`SYSTEM_ALERT_WINDOW` 仅用于“可选”滚动气泡，文案写明 Optional）。
- **跳转点全部为官方 Action，无伪造设置页**：[S1.u#c](<resource-unit:#1.dex1 code:S1.u#c>) 按分支分别发起 `android.settings.ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`MANAGE_OVERLAY_PERMISSION`；[S1.U#c](<resource-unit:#1.dex1 code:S1.U#c>) 先判 `canDrawOverlays`，再用 [l2.a#x](<resource-unit:#1.dex1 code:l2.a#x>) 读取 `Settings.Secure.accessibility_enabled` / `enabled_accessibility_services` 判定状态，已启用则只切换气泡。
- **存在 Android 13+ 受限设置分步教学**（[S1.E#d](<resource-unit:#1.dex1 code:S1.E#d>) 内 `SDK_INT>=33` 分支文案：“Is Nudge greyed out or showing "Restricted setting"? Open App info, tap the ⋮ menu, choose Allow restricted settings, then try again.”），但配以跳转应用详情页的显式按钮，属于 AOSP 官方路径的透明说明，无恐吓/假故障框架。
- **无拒权死循环、无获权后防撤权**：[MainActivity.onResume](<resource-unit:#1.dex1 code:com.nitulshah.nudge.MainActivity#onResume>) 仅做跨日计数重置，不重跳设置页；`MyAccessibilityService` 未见 `GLOBAL_ACTION_BACK/HOME` 或自点确认逻辑。拒权后停留在本页，功能降级为无评分/无计数。
- **一处轻微技术偏差**：配置订阅了 `typeViewTextChanged`，与描述中“cannot read text”存在形式上的不完全一致；但代码侧未见任何节点文本读取/上报路径（`MyAccessibilityService` 仅按包名与滚动事件计数，另有 `TelemetryFlushWorker` 本地聚合），不构成隐私违规。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于 classes.dex 的 Compose 代码与 res/values/strings.xml、res/xml/accessibility_service_config.xml 中，无加壳、无加密资产、无远端 HTML 下发的引导页；唯一动态要素是系统无障碍开关状态（Settings.Secure 读取），属正常运行期状态查询。",
  "summary_one_liner": "在主界面以原生 Compose 卡片透明说明用途并提供按钮，点击后通过官方 ACTION_ACCESSIBILITY_SETTINGS 跳转系统无障碍列表，Android 13+ 额外提供跳应用详情页开启受限设置的分步说明，全程无弹窗逼迫、无遮罩、无拒权循环。",
  "disguise_identity": {
    "app_display_name": "Nudge",
    "claimed_brand_or_persona": "Nudge（F-Droid 开源专注自律应用，真实名称，未冒充任何系统或第三方品牌）",
    "a11y_service_label": "Nudge Scroll Tracker",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。仅见常规 R8 类名混淆（S1.E/S1.u/S1.U/l2.a 等），未使用空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool；服务 label 与 app_name 语义一致。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.nitulshah.nudge.MainActivity（单 Activity + Jetpack Compose 界面）",
      "trigger_event": "LAUNCHER 启动 → onCreate()：初始化 FIRST_LAUNCH_DATE、注册午夜重置 Worker、按需申请 POST_NOTIFICATIONS、setContent 挂载 Compose 界面",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（本步不呈现权限引导文案，仅进入主界面）",
      "shown_text_zh": "冷启动直接进入 Nudge 主界面，无强制权限弹窗拦截",
      "user_action_requested": "无强制操作；可自由浏览界面",
      "code_anchor": "com.nitulshah.nudge.MainActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "主界面内 Compose Card 卡片（S1.E 组合项）",
      "trigger_event": "主界面渲染时组合执行，非弹窗、非独立 Activity",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Turn on scroll tracking / Nudge counts scrolls and unlocks with an Android accessibility service. Nothing is tracked, and there's no score, until it's on. / Find Nudge under Downloaded apps (or Installed apps) and switch it on.",
      "shown_text_zh": "开启滚动追踪 / Nudge 通过 Android 无障碍服务统计滚动与解锁次数。未开启前不追踪任何内容，也没有评分。/ 在「已下载的应用」（或「已安装的应用」）中找到 Nudge 并打开开关。",
      "user_action_requested": "阅读说明后点击卡片内按钮进入下一步；卡片外可正常使用其他功能（无强制、无取消阻断）",
      "code_anchor": "S1.E.d"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统「应用信息」页（android.settings.APPLICATION_DETAILS_SETTINGS，package:com.nitulshah.nudge）",
      "trigger_event": "点击卡片内受限设置说明下方按钮 → S1.u.c 分支 case 3，仅 SDK_INT>=33 显示",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Is Nudge greyed out or showing \"Restricted setting\"? Open App info, tap the ⋮ menu, choose Allow restricted settings, then try again.",
      "shown_text_zh": "Nudge 显示为灰色或提示「受限设置」？打开应用信息，点右上角 ⋮ 菜单，选择「允许受限设置」，然后重试。",
      "user_action_requested": "进入应用详情页 → 右上角菜单 → 允许受限设置（无恐吓、无假故障包装，为 AOSP 官方路径说明）",
      "code_anchor": "S1.u.c（case 3）+ S1.E.d（SDK>=33 分支）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍服务列表页（android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "点击卡片主按钮 → S1.u.c 分支 case 2，以 FLAG_ACTIVITY_NEW_TASK 启动；另一路径 S1.U.c 在 canDrawOverlays 已授权且无障碍未启用时同样跳此页",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Find Nudge under Downloaded apps (or Installed apps) and switch it on.",
      "shown_text_zh": "在「已下载的应用」（或「已安装的应用」）分类下找到 Nudge，打开其开关。",
      "user_action_requested": "在系统列表中手动找到「Nudge Scroll Tracker」并开启；可返回或放弃，无循环重跳",
      "code_anchor": "S1.u.c / S1.U.c"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "无。应用未在设置页上方叠加任何悬浮窗、半透明遮罩或高仿开关页",
      "trigger_event": "不适用",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无遮罩叠层指引",
      "user_action_requested": "无",
      "code_anchor": "S1.U.c（仅使用 MANAGE_OVERLAY_PERMISSION 官方跳转，未见 WindowManager 叠层绘制于设置页之上）"
    },
    {
      "step": 6,
      "stage": "业务功能触发",
      "screen_or_component": "可选「显示在其他应用上层」开关 → android.settings.action.MANAGE_OVERLAY_PERMISSION",
      "trigger_event": "用户点击可选按钮（S1.u.c default 分支）或点击气泡开关而 canDrawOverlays 为 false（S1.U.c case 1）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Optional: allow Display over other apps to show the floating scroll-count bubble.",
      "shown_text_zh": "可选：允许「显示在其他应用上层」，以显示悬浮的滚动计数气泡。",
      "user_action_requested": "可选授权悬浮窗权限；明确标注 Optional，拒绝不影响核心计数功能",
      "code_anchor": "S1.u.c（default 分支）/ S1.U.c（case 1）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "MyAccessibilityService（滚动事件计数）+ 悬浮气泡（_isBubbleVisible）",
      "trigger_event": "系统绑定服务后 onAccessibilityEvent 计数；主界面再次进入时 l2.a.x 检测 accessibility_enabled 与 enabled_accessibility_services 判定已授权",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "You're scrolling fast / Take a breath? Tap to take a break.",
      "shown_text_zh": "你滚动得太快了 / 需要喘口气吗？点击休息一下。",
      "user_action_requested": "超阈值时点击通知或弹出 InterventionActivity 进入休息干预；无自授权、无阻止撤权行为",
      "code_anchor": "com.nitulshah.nudge.MyAccessibilityService.checkIntervention / l2.a.x"
    }
  ],
  "text_presentation_locations": [
    "主界面内嵌 Compose Card 卡片（S1.E.d 渲染，非弹窗、非独立 Activity）：标题、用途说明、分类查找指引、受限设置教学、可选悬浮窗说明",
    "系统无障碍列表中的服务项说明：res/values/strings.xml 的 accessibility_description（经 res/xml/accessibility_service_config.xml 的 android:description 引用）",
    "系统无障碍列表中的服务名称：AndroidManifest.xml 中 service 的 android:label=\"Nudge Scroll Tracker\"",
    "跳转至系统无障碍设置页 / 应用详情页 / 悬浮窗权限页后由系统 UI 呈现，应用本身不在其上叠加任何文案",
    "超阈值干预通知与 InterventionActivity：\"You're scrolling fast\" / \"Take a breath? Tap to take a break.\"（属功能提醒，非权限引导）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Nudge counts your scrolls to help you track your phone use. It only learns that a scroll happened and in which app. It cannot read text or anything else on your screen.",
      "text_zh": "Nudge 统计你的滚动次数，帮助你了解手机使用情况。它只会知道发生了一次滚动以及发生在哪个应用里，无法读取屏幕上的文字或其他任何内容。",
      "source_location": "res/values/strings.xml: accessibility_description（经 res/xml/accessibility_service_config.xml android:description 引用，显示于系统无障碍列表）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn on scroll tracking",
      "text_zh": "开启滚动追踪",
      "source_location": "S1.E.d（硬编码 Compose 文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Nudge counts scrolls and unlocks with an Android accessibility service. Nothing is tracked, and there's no score, until it's on.",
      "text_zh": "Nudge 通过 Android 无障碍服务统计滚动与解锁次数。在开启之前不会追踪任何内容，也不会生成评分。",
      "source_location": "S1.E.d（硬编码 Compose 文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Find Nudge under Downloaded apps (or Installed apps) and switch it on.",
      "text_zh": "在「已下载的应用」（或「已安装的应用」）中找到 Nudge 并打开开关。",
      "source_location": "S1.E.d（硬编码 Compose 文案）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Is Nudge greyed out or showing \"Restricted setting\"? Open App info, tap the ⋮ menu, choose Allow restricted settings, then try again.",
      "text_zh": "Nudge 显示为灰色或提示「受限设置」？打开应用信息，点右上角 ⋮ 菜单，选择「允许受限设置」，然后重试。",
      "source_location": "S1.E.d（SDK_INT>=33 分支，硬编码 Compose 文案）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Optional: allow Display over other apps to show the floating scroll-count bubble.",
      "text_zh": "可选：允许「显示在其他应用上层」，以显示悬浮的滚动计数气泡。",
      "source_location": "S1.E.d（硬编码 Compose 文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "You're scrolling fast",
      "text_zh": "你滚动得太快了",
      "source_location": "com.nitulshah.nudge.MyAccessibilityService.checkIntervention（通知标题硬编码）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Take a breath? Tap to take a break.",
      "text_zh": "需要喘口气吗？点击休息一下。",
      "source_location": "com.nitulshah.nudge.MyAccessibilityService.checkIntervention（通知正文硬编码）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无拒权循环。MainActivity.onResume 仅读取 NudgePrefs 的 LAST_SCROLL_DATE 与 DayBoundary.today() 做跨日计数重置，不做无障碍状态重定向；用户从系统设置返回后停留在原主界面卡片，功能降级为无计数、无评分，无 Timer 定时重跳、无 onResume 死循环重跳。",
    "overlay_or_fake_settings": "无。未绘制半透明引导遮罩、全屏悬浮窗或高仿系统无障碍开关页；SYSTEM_ALERT_WINDOW 仅用于可选的滚动计数气泡（_isBubbleVisible），且文案明确标注 Optional。跳转均使用官方 ACTION，落点为真实系统页面。",
    "restricted_settings_13plus_coaching": "有，但为官方路径透明说明：SDK_INT>=33 时卡片显示「Is Nudge greyed out or showing \"Restricted setting\"? Open App info, tap the ⋮ menu, choose Allow restricted settings, then try again.」并配按钮跳转 android.settings.APPLICATION_DETAILS_SETTINGS（package:com.nitulshah.nudge）。无恐吓、无假故障、无 Session 安装器绕过、无伪造安装包投递。",
    "post_grant_anti_removal": "无。MyAccessibilityService 未实现 GLOBAL_ACTION_BACK/HOME 阻止撤权，未监听设置页自动回跳，未自点确认或自授权。",
    "benign_graceful_degradation": "有。无障碍未开启时应用照常启动，仅不产生滚动计数、健康评分与干预提醒；悬浮气泡为显式 Optional 项；用户可选择只用界面内手动查看，权限获取完全依赖用户在系统页自行开启。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以监测到 Intent action = android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的 startActivity 为触发点拉起 UTG；同时在冷启动后 1~2s 抓取一次主界面，确认引导为内嵌卡片而非强制弹窗。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后主界面引导卡片页",
        "page_identifier": "com.nitulshah.nudge.MainActivity + Compose 卡片，可见文本节点 'Turn on scroll tracking' 与 'Nudge counts scrolls and unlocks with an Android accessibility service...'",
        "why_most_useful": "确认引导载体是内嵌卡片而非不可取消弹窗/WebView，是区分良性透明引导与诱导弹窗的第一判据",
        "observable_utg_signals": [
          "是否存在可关闭的 Dialog/全屏遮罩节点",
          "卡片文案是否含隐私划界句 'It cannot read text'",
          "是否存在 WebView 节点或 remote url"
        ]
      },
      {
        "page_role": "受限设置教学分支页（Android 13+）",
        "page_identifier": "同卡片内 'Is Nudge greyed out or showing \"Restricted setting\"?' 文本 + 跳应用详情按钮",
        "why_most_useful": "受限设置教学是诱导类高频信号，需确认其文案框架是官方路径说明还是恐吓/伪造更新",
        "observable_utg_signals": [
          "文案是否出现假更新/故障恐吓/假反诈用语",
          "按钮是否指向 android.settings.APPLICATION_DETAILS_SETTINGS",
          "是否存在悬浮遮罩覆盖系统菜单"
        ]
      },
      {
        "page_role": "跳转后系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页中 'Nudge Scroll Tracker' 列表项及其 description 摘要",
        "why_most_useful": "核对服务名与描述是否与真实功能一致，验证无身份冒充与空白/同形字挤出",
        "observable_utg_signals": [
          "服务 label 是否等于 Nudge Scroll Tracker",
          "description 是否包含透明范围声明",
          "是否存在多个同应用无障碍服务项（多 alias 伪装）"
        ]
      },
      {
        "page_role": "获权后悬浮气泡与干预页",
        "page_identifier": "悬浮窗滚动计数气泡 + com.nitulshah.nudge.InterventionActivity（excludeFromRecents、Theme.Intervention）",
        "why_most_useful": "确认获权后行为限于计数展示与休息提醒，无后台静默操作、无读取屏文本上报",
        "observable_utg_signals": [
          "气泡是否仅显示数字",
          "干预页是否出现外部跳转/广告/诱导安装",
          "是否有向网络发送节点文本的流量"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。引导文案全部为 Compose 文本节点与 strings 资源，可被 UTG 直接提取，无需 OCR；未使用图片/GIF 引导、无远端 HTML、无静态加壳或密文二阶段载荷。唯一需注意的边界：无障碍配置订阅了 typeViewTextChanged，而描述声明不读取文本，若做运行期核验可重点确认服务事件处理是否仅取包名与滚动计数（静态侧未见节点文本读取与上报路径）。"
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
    "S1.E.d",
    "S1.u.c",
    "S1.U.c",
    "l2.a.x",
    "com.nitulshah.nudge.MainActivity.onResume",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
