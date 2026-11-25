# MR_065__9a81e55efe｜HiddenAd — Helicopter Shoot

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：120.8s

## 1. 一句话核心结论

- **核心申请方式**：该样本不申请、不引导、不跳转无障碍权限，所谓无障碍线索全部来自 androidx id 与 Facebook/GMS 的 Play 服务提示文案；其真实恶意面是隐藏广告与无图标前台常驻，而非无障碍滥用。
- **静态可见性说明**：无障碍相关面完全静态可见且为空：Manifest 无任何 BIND_ACCESSIBILITY_SERVICE 服务与 accessibility 配置 XML，DEX 无 ACCESSIBILITY_SETTINGS/SYSTEM_ALERT_WINDOW/overlay 类型窗口/perfomGlobalAction 调用，也无自研 AccessibilityService 子类。未还原部分仅为 Unity libil2cpp.so/libmain.so 的原生侧逻辑与 assets/vpaid_html_template.html（IAB VPAID 广告模板），二者不含无障碍引导文案。

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9a81e55efefea878c7fb540c07bf7b778a7bca0f5ea8dbfa49444bf40d8bd020` |
| 包名 / 年份 | `com.helicopter.shoot.city.explore.peace` / 2020 |
| 家族 / 品类 | **HiddenAd**（同池样本数：12） |
| 原始来源标识 | https://gbhackers.com/21-malicious-apps/ |
| 桌面显示名 | Helicopter Shoot |
| 引导页宣称品牌/身份 | Helicopter Shoot（Unity 直升机射击小游戏，包名 com.helicopter.shoot.city.explore.peace，UMENG_CHANNEL=Google） |
| 系统无障碍列表服务名 | 无（不存在无障碍服务，系统无障碍列表中不会出现本应用条目） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无无障碍相关伪装；但存在代码层混淆：字符串统一经 com.helicopt.p.ALLATORIxDEMOxanyValidIdentifierName（逐字符 XOR 0x31/0x5F）解密后作为资源名/scheme 使用，类名被压成 a/b/ga/q/u/z 等短名（Allatori 风格），桌面入口用 Theme.Translucent 的空壳 Activity 隐藏真实跳转。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.helicopt.b（Theme.Translucent 空壳 Activity，LAUNCHER + MAIN，taskAffinity=.start） | 用户点击桌面图标 → onCreate | 原生Activity | 无 | 无（无需任何操作，无可取消项） | `com.helicopt.b.onCreate` |
| 2 | 冷启动入口 | com.unity3d.player.UnityPlayerActivity（游戏主界面，sensorPortrait，hardwareAccelerated=false） | com.helicopt.b.onCreate 中 startActivity(Intent.setClass(UnityPlayerActivity).addFlags(0x10000000)) 后 finish() | 原生Activity | **原文**：无（游戏渲染画面，文案来自 Unity 资源）<br>**译注**：直接进入直升机射击游戏主界面 | 无权限相关请求；不出现任何无障碍引导弹窗 | `com.helicopt.b.onCreate` |
| 3 | 获权后动作 | 无（不存在获权环节） | 无 | 不可静态还原 | 无 | 无 | `com.helicopt.ShootApplication.onCreate（仅初始化 AudienceNetwork/MobileAds/AppLovin 广告 SDK，无权限引导）` |
| 4 | 业务功能触发 | com.helicopt.ga（exported，Theme.NoTitleBar.Fullscreen，接受 detail/overlay/link 三种 scheme） | 外部或内部 Intent(ACTION_VIEW) 携 detail\|overlay\|link scheme → onCreate 取 Uri scheme 后经 EventBus sticky 事件渲染 | 原生Activity | **原文**：textView.setText(this.g.getAdvertiserName()); textView3.setText(this.g.getAdBodyText()); button.setText(this.g.getAdCallToAction());<br>**译注**：全屏展示 Facebook NativeAd 的广告主名称、广告正文与行动号召按钮（内容由广告下发，非无障碍引导） | 点击广告区（registerViewForInteraction），有 close(View) 关闭按钮 → finish() | `com.helicopt.ga.onCreate / com.helicopt.ga.ALLATORIxDEMOxanyValidIdentifierName` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 不存在无障碍引导文字：无 AlertDialog/引导 Activity/引导 WebView/悬浮引导窗承载任何开启无障碍的说明
- res/values/strings.xml 中被预筛命中的文案实为三方 SDK 提示：com_facebook_internet_permission_error_message『WebView login requires INTERNET permission』、common_google_play_services_enable_text『%1$s won't work unless you enable Google Play services.』，指向网络权限与 Play 服务，而非无障碍
- res/values/ids.xml 的 accessibility_custom_action_* / accessibility_action_clickable_span 仅为 androidx 标准 View id 声明，不产生任何界面文字
- com.helicopt.ga 的广告文案（getAdvertiserName/getAdBodyText/getAdCallToAction）来自 Facebook 广告响应，呈现在全屏原生布局，与权限申请无关
- assets/vpaid_html_template.html 为 IAB VPAID 播放模板（.play-button-hack 为 30×30 透明点击区，z-index 99999999），属广告测量，无权限说明文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | WebView login requires INTERNET permission | WebView 登录需要 INTERNET 权限 | `res/values/strings.xml:37 (com_facebook_internet_permission_error_message)` | 良性透明说明 |
| en | %1$s won't work unless you enable Google Play services. | 除非启用 Google Play 服务，否则 %1$s 无法运行。 | `res/values/strings.xml:59 (common_google_play_services_enable_text)` | 故障恐吓 |
| en | Enable Google Play services | 启用 Google Play 服务 | `res/values/strings.xml:60 (common_google_play_services_enable_title)` | 故障恐吓 |
| en | Get Google Play services | 获取 Google Play 服务 | `res/values/strings.xml (common_google_play_services_install_button) / com.google.android.gms.common.internal.zzg#zzg 触发 APPLICATION_DETAILS_SETTINGS` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不存在（无无障碍跳转，故无拒权返回重跳、无 onResume 死循环、无 Timer 定时拉起）
- **遮罩叠层 / 高仿系统设置页**：无。虽有 com.helicopt.ga 的 overlay scheme 与 Theme.Translucent 入口，但前者是广告展示 Activity、后者是无 UI 跳板，均不叠加引导遮罩或伪造系统无障碍开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。代码中唯一 APPLICATION_DETAILS_SETTINGS 跳转在 GMS 的 zzg 内，属 Play 服务安装引导；无『应用详情→右上角菜单→允许受限设置』教学，无 Session Installer 绕过
- **获权后即时行为与防撤权机制**：无。不存在无障碍服务，故无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权
- **良性降级 / 替代方案**：无（本应用根本不涉及无障碍能力，无需降级路径）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：本样本不产生任何无障碍跳转，纯 UTG 无障碍检测链对其为空。若仍需运行期取证，应在冷启动瞬间（点击图标后 300ms 内）拉起，捕获 com.helicopt.b→UnityPlayerActivity 的静默跳转；并在 Intent(ACTION_VIEW, scheme=overlay|detail|link) 直达 com.helicopt.ga 时捕获全屏广告页与随后出现的无图标前台通知（startForeground id=1001）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：本样本对无障碍判别存在根本性盲区：不存在无障碍服务与设置跳转，任何基于『跳 ACCESSIBILITY_SETTINGS / 无障碍列表条目 / 设置页遮罩』的 UTG 规则都不会命中，属真阴性而非规避。另 Unity 原生层（libil2cpp.so/libmain.so）与远端广告 HTML 未逐函数还原，若后续需排除原生侧无障碍调用，应在 C++ 层补证。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **全屏广告展示页（可疑收益点，非权限引导）** | com.helicopt.ga，Theme.NoTitleBar.Fullscreen，包名 com.helicopter.shoot.city.explore.peace，界面为 NativeAdLayout（含 AdOptionsView/MediaView/CTA 按钮） | 该样本的恶意面在于以隐藏入口承载广告变现与常驻驻留，捕获此页可确认广告是否与用户操作无关地被触发，从而区分『隐藏广告』与良性游戏内广告 | 无应用自身标题栏/关闭入口的 Fullscreen 广告布局；AdChoices 图标（AdOptionsView）与 getSponsoredTranslation 赞助标注；无任何无障碍权限说明文本 |
| **冷启动透明空壳跳板** | com.helicopt.b（Theme.Translucent，taskAffinity=.start），几乎不可见 | 证明桌面入口被刻意抽离，真实 Activity 不直接暴露，是判断『入口伪装/隐蔽拉起』的关键信号 | 点击图标后无对应可见 Activity 名称的界面；Activity 栈瞬间切换至 UnityPlayerActivity；无权限弹窗/无引导说明 |
| **系统通知栏常驻项（隐蔽驻留佐证）** | 通知 id=1001，channelId=包名，SDK<29 时 smallIcon=Icon.createWithContentUri("")（空白图标） | 验证前台服务被用于无图标常驻、隐藏『正在运行』提示，属隐蔽驻留手法 | 通知栏出现无图标/空白图标的常驻通知；通知渠道名由 XOR 解密资源取得、无描述文案；无点击跳转的可见说明 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.helicopt.b.onCreate`
- `com.helicopt.ga.onCreate`
- `com.helicopt.ga.ALLATORIxDEMOxanyValidIdentifierName`
- `com.helicopt.z.ALLATORIxDEMOxanyValidIdentifierName(android.app.Service)`
- `com.helicopt.q.onStartJob`
- `com.helicopt.p.ALLATORIxDEMOxanyValidIdentifierName(java.lang.String)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（定向核验无障碍引导链）

**该应用不存在无障碍权限申请链——这是阴性结论，并非"隐藏得很深"。**

1. **Manifest 中没有任何 AccessibilityService**：没有 `<service ... android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">`，也没有 `res/xml/*_accessibility*.xml` 配置；`read_manifest` 的 `components` 中只出现 `com.helicopt.u`、`com.helicopt.a`（普通 Service）、`com.helicopt.q`（BIND_JOB_SERVICE 的 JobService）三个自有组件。`res/values/ids.xml` 里成批的 `accessibility_custom_action_*` 是 androidx 标准 id，`AccessibilityServiceInfoCompat` 也来自 androidx.core，均非自研无障碍能力。

2. **没有跳转无障碍设置的代码**：`search_text_in_app` 在 `#1.dex1` 中对 `ACCESSIBILITY_SETTINGS`、`SYSTEM_ALERT_WINDOW`、`TYPE_APPLICATION_OVERLAY`、`TYPE_SYSTEM_ALERT`、`performGlobalAction` 全部 **no_matches**；唯一命中的 `APPLICATION_DETAILS_SETTINGS` 位于 GMS 的 `com.google.android.gms.common.internal.zzg#zzg`（第三方 SDK 的 Play 服务引导），与无障碍无关。也没有 `Settings.ACTION_ACCESSIBILITY_SETTINGS` 的字符串或 `AccessibilityService` 自研子类。

3. **预筛线索 `A11Y_OVERLAY` / `RESTRICTED_STR` / `SESSION_INSTALLER` 属误报**：`restricted` 命中来自 `res/values/strings.xml` 的 Facebook SDK 文案（`WebView login requires INTERNET permission`、`%1$s won't work unless you enable Google Play services.` 等）与 `com.google.android.gms` 的 Play 服务安装提示；`overlay` 命中来自 `com.helicopt.ga` 的 `detail/overlay/link` 三个 scheme，而它展示的是 **Facebook NativeAd 原生广告布局**，并非无障碍叠层。

4. **实际入口与可疑点（与无障碍无关，但与本样本的"隐藏广告"性质一致）**：桌面入口是 `Theme.Translucent` 的 [com.helicopt.b](<resource-unit:#1.dex1 code:com.helicopt.b#onCreate>)，它无 UI 直接 `startActivity(UnityPlayerActivity)` 并 `finish()`；[com.helicopt.ga](<resource-unit:#1.dex1 code:com.helicopt.ga#onCreate>) 是 exported 的 `NoTitleBar.Fullscreen` Activity，按 `detail/overlay/link` scheme 用 `Resources.getIdentifier` + `p.ALLATORIxDEMOxanyValidIdentifierName`（XOR 0x31/0x5F 解密资源名）动态加载广告布局并 `registerViewForInteraction`；[com.helicopt.q#onStartJob](<resource-unit:#1.dex1 code:com.helicopt.q#onStartJob>) 反复拉起 `com.helicopt.u`，其 `onStartCommand` 走 `z.ALLATORIxDEMOxanyValidIdentifierName(Service)`，在 SDK<29 时用 `setSmallIcon(Icon.createWithContentUri(""))` 构造**无图标常驻通知**并 `startForeground(1001, …)`——这是隐蔽驻留/隐藏广告位手法，而不是无障碍诱导。

5. **UTG 视角**：本样本不存在"设置页压栈遮罩""拒权重跳""伪造无障碍开关页"等可捕获页面，纯 UTG 无障碍判别链对本样本为空；若要动态取证，应改为观测 `com.helicopt.ga` 的全屏广告 Activity 与无图标前台通知。

**未决/覆盖边界**：Unity 层（`libil2cpp.so` 与 `libmain.so`）内是否另有原生侧设置页跳转未做逐函数逆向；`assets/vpaid_html_template.html` 仅为 IAB VPAID 播放器模板（含 `.play-button-hack` 30×30 透明可点区），属广告测量用途，未见无障碍文案。上述均不改变"无无障碍申请链"的结论。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍相关面完全静态可见且为空：Manifest 无任何 BIND_ACCESSIBILITY_SERVICE 服务与 accessibility 配置 XML，DEX 无 ACCESSIBILITY_SETTINGS/SYSTEM_ALERT_WINDOW/overlay 类型窗口/perfomGlobalAction 调用，也无自研 AccessibilityService 子类。未还原部分仅为 Unity libil2cpp.so/libmain.so 的原生侧逻辑与 assets/vpaid_html_template.html（IAB VPAID 广告模板），二者不含无障碍引导文案。",
  "summary_one_liner": "该样本不申请、不引导、不跳转无障碍权限，所谓无障碍线索全部来自 androidx id 与 Facebook/GMS 的 Play 服务提示文案；其真实恶意面是隐藏广告与无图标前台常驻，而非无障碍滥用。",
  "disguise_identity": {
    "app_display_name": "Helicopter Shoot",
    "claimed_brand_or_persona": "Helicopter Shoot（Unity 直升机射击小游戏，包名 com.helicopter.shoot.city.explore.peace，UMENG_CHANNEL=Google）",
    "a11y_service_label": "无（不存在无障碍服务，系统无障碍列表中不会出现本应用条目）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无无障碍相关伪装；但存在代码层混淆：字符串统一经 com.helicopt.p.ALLATORIxDEMOxanyValidIdentifierName（逐字符 XOR 0x31/0x5F）解密后作为资源名/scheme 使用，类名被压成 a/b/ga/q/u/z 等短名（Allatori 风格），桌面入口用 Theme.Translucent 的空壳 Activity 隐藏真实跳转。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.helicopt.b（Theme.Translucent 空壳 Activity，LAUNCHER + MAIN，taskAffinity=.start）",
      "trigger_event": "用户点击桌面图标 → onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无任何界面内容，透明空壳页，用户无感知",
      "user_action_requested": "无（无需任何操作，无可取消项）",
      "code_anchor": "com.helicopt.b.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.unity3d.player.UnityPlayerActivity（游戏主界面，sensorPortrait，hardwareAccelerated=false）",
      "trigger_event": "com.helicopt.b.onCreate 中 startActivity(Intent.setClass(UnityPlayerActivity).addFlags(0x10000000)) 后 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（游戏渲染画面，文案来自 Unity 资源）",
      "shown_text_zh": "直接进入直升机射击游戏主界面",
      "user_action_requested": "无权限相关请求；不出现任何无障碍引导弹窗",
      "code_anchor": "com.helicopt.b.onCreate"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "无（不存在获权环节）",
      "trigger_event": "无",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无。应用从不请求无障碍，也不存在获权后的无障碍能力使用",
      "user_action_requested": "无",
      "code_anchor": "com.helicopt.ShootApplication.onCreate（仅初始化 AudienceNetwork/MobileAds/AppLovin 广告 SDK，无权限引导）"
    },
    {
      "step": 4,
      "stage": "业务功能触发",
      "screen_or_component": "com.helicopt.ga（exported，Theme.NoTitleBar.Fullscreen，接受 detail/overlay/link 三种 scheme）",
      "trigger_event": "外部或内部 Intent(ACTION_VIEW) 携 detail|overlay|link scheme → onCreate 取 Uri scheme 后经 EventBus sticky 事件渲染",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "textView.setText(this.g.getAdvertiserName()); textView3.setText(this.g.getAdBodyText()); button.setText(this.g.getAdCallToAction());",
      "shown_text_zh": "全屏展示 Facebook NativeAd 的广告主名称、广告正文与行动号召按钮（内容由广告下发，非无障碍引导）",
      "user_action_requested": "点击广告区（registerViewForInteraction），有 close(View) 关闭按钮 → finish()",
      "code_anchor": "com.helicopt.ga.onCreate / com.helicopt.ga.ALLATORIxDEMOxanyValidIdentifierName"
    }
  ],
  "text_presentation_locations": [
    "不存在无障碍引导文字：无 AlertDialog/引导 Activity/引导 WebView/悬浮引导窗承载任何开启无障碍的说明",
    "res/values/strings.xml 中被预筛命中的文案实为三方 SDK 提示：com_facebook_internet_permission_error_message『WebView login requires INTERNET permission』、common_google_play_services_enable_text『%1$s won't work unless you enable Google Play services.』，指向网络权限与 Play 服务，而非无障碍",
    "res/values/ids.xml 的 accessibility_custom_action_* / accessibility_action_clickable_span 仅为 androidx 标准 View id 声明，不产生任何界面文字",
    "com.helicopt.ga 的广告文案（getAdvertiserName/getAdBodyText/getAdCallToAction）来自 Facebook 广告响应，呈现在全屏原生布局，与权限申请无关",
    "assets/vpaid_html_template.html 为 IAB VPAID 播放模板（.play-button-hack 为 30×30 透明点击区，z-index 99999999），属广告测量，无权限说明文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "WebView login requires INTERNET permission",
      "text_zh": "WebView 登录需要 INTERNET 权限",
      "source_location": "res/values/strings.xml:37 (com_facebook_internet_permission_error_message)",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "除非启用 Google Play 服务，否则 %1$s 无法运行。",
      "source_location": "res/values/strings.xml:59 (common_google_play_services_enable_text)",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Google Play services",
      "text_zh": "启用 Google Play 服务",
      "source_location": "res/values/strings.xml:60 (common_google_play_services_enable_title)",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Get Google Play services",
      "text_zh": "获取 Google Play 服务",
      "source_location": "res/values/strings.xml (common_google_play_services_install_button) / com.google.android.gms.common.internal.zzg#zzg 触发 APPLICATION_DETAILS_SETTINGS",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不存在（无无障碍跳转，故无拒权返回重跳、无 onResume 死循环、无 Timer 定时拉起）",
    "overlay_or_fake_settings": "无。虽有 com.helicopt.ga 的 overlay scheme 与 Theme.Translucent 入口，但前者是广告展示 Activity、后者是无 UI 跳板，均不叠加引导遮罩或伪造系统无障碍开关页",
    "restricted_settings_13plus_coaching": "无。代码中唯一 APPLICATION_DETAILS_SETTINGS 跳转在 GMS 的 zzg 内，属 Play 服务安装引导；无『应用详情→右上角菜单→允许受限设置』教学，无 Session Installer 绕过",
    "post_grant_anti_removal": "无。不存在无障碍服务，故无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权",
    "benign_graceful_degradation": "无（本应用根本不涉及无障碍能力，无需降级路径）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "本样本不产生任何无障碍跳转，纯 UTG 无障碍检测链对其为空。若仍需运行期取证，应在冷启动瞬间（点击图标后 300ms 内）拉起，捕获 com.helicopt.b→UnityPlayerActivity 的静默跳转；并在 Intent(ACTION_VIEW, scheme=overlay|detail|link) 直达 com.helicopt.ga 时捕获全屏广告页与随后出现的无图标前台通知（startForeground id=1001）。",
    "key_pages_to_capture": [
      {
        "page_role": "全屏广告展示页（可疑收益点，非权限引导）",
        "page_identifier": "com.helicopt.ga，Theme.NoTitleBar.Fullscreen，包名 com.helicopter.shoot.city.explore.peace，界面为 NativeAdLayout（含 AdOptionsView/MediaView/CTA 按钮）",
        "why_most_useful": "该样本的恶意面在于以隐藏入口承载广告变现与常驻驻留，捕获此页可确认广告是否与用户操作无关地被触发，从而区分『隐藏广告』与良性游戏内广告",
        "observable_utg_signals": ["无应用自身标题栏/关闭入口的 Fullscreen 广告布局", "AdChoices 图标（AdOptionsView）与 getSponsoredTranslation 赞助标注", "无任何无障碍权限说明文本"]
      },
      {
        "page_role": "冷启动透明空壳跳板",
        "page_identifier": "com.helicopt.b（Theme.Translucent，taskAffinity=.start），几乎不可见",
        "why_most_useful": "证明桌面入口被刻意抽离，真实 Activity 不直接暴露，是判断『入口伪装/隐蔽拉起』的关键信号",
        "observable_utg_signals": ["点击图标后无对应可见 Activity 名称的界面", "Activity 栈瞬间切换至 UnityPlayerActivity", "无权限弹窗/无引导说明"]
      },
      {
        "page_role": "系统通知栏常驻项（隐蔽驻留佐证）",
        "page_identifier": "通知 id=1001，channelId=包名，SDK<29 时 smallIcon=Icon.createWithContentUri(\"\")（空白图标）",
        "why_most_useful": "验证前台服务被用于无图标常驻、隐藏『正在运行』提示，属隐蔽驻留手法",
        "observable_utg_signals": ["通知栏出现无图标/空白图标的常驻通知", "通知渠道名由 XOR 解密资源取得、无描述文案", "无点击跳转的可见说明"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "本样本对无障碍判别存在根本性盲区：不存在无障碍服务与设置跳转，任何基于『跳 ACCESSIBILITY_SETTINGS / 无障碍列表条目 / 设置页遮罩』的 UTG 规则都不会命中，属真阴性而非规避。另 Unity 原生层（libil2cpp.so/libmain.so）与远端广告 HTML 未逐函数还原，若后续需排除原生侧无障碍调用，应在 C++ 层补证。"
  },
  "behavior_pattern_tags": [],
  "code_anchors": [
    "com.helicopt.b.onCreate",
    "com.helicopt.ga.onCreate",
    "com.helicopt.ga.ALLATORIxDEMOxanyValidIdentifierName",
    "com.helicopt.z.ALLATORIxDEMOxanyValidIdentifierName(android.app.Service)",
    "com.helicopt.q.onStartJob",
    "com.helicopt.p.ALLATORIxDEMOxanyValidIdentifierName(java.lang.String)"
  ]
}
```

</details>
