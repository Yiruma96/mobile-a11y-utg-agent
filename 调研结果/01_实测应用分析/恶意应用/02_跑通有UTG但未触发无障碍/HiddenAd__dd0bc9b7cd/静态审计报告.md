# MR_137__dd0bc9b7cd｜HiddenAd — Iron It

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：148.9s

## 1. 一句话核心结论

- **核心申请方式**：该应用完全不申请也不引导无障碍权限：Manifest 无 BIND_ACCESSIBILITY_SERVICE 服务、无 android:description、无 SYSTEM_ALERT_WINDOW，全包无 ACTION_ACCESSIBILITY_SETTINGS 跳转与 AccessibilityService 实现，其真实行为是 Unity 游戏外壳下的隐蔽广告注入。
- **静态可见性说明**：Manifest、5 个主 DEX、res 与 assets/audience_network.dex 均可静态读取；无加壳、无 VMP。仅存在 Allatori 式逐字符 XOR 字符串混淆（com.ironit.o.w / com.ironit.r.v 的 ALLATORIxDEMO），可静态还原。远端广告文案由 ZeusNative 运行时下发，不含无障碍相关内容。

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `dd0bc9b7cde1e5c217f2ef867c37e4e76a505c74da7f2ae8479e4151c76403ef` |
| 包名 / 年份 | `com.iron.clothes.smooth.perfect` / 2020 |
| 家族 / 品类 | **HiddenAd**（同池样本数：12） |
| 原始来源标识 | https://gbhackers.com/21-malicious-apps/ |
| 桌面显示名 | Iron It |
| 引导页宣称品牌/身份 | Iron It（衣物熨烫类 Unity 小游戏，标签 @string/app_name 未改写，无品牌冒用） |
| 系统无障碍列表服务名 | 无（未声明任何无障碍服务，系统无障碍列表中不会出现本应用条目） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：类名与方法名统一为 ALLATORIxDEMO（Allatori 混淆）；字符串以逐字符 XOR 存储（^28/^'?'、^'A'/^'t'）；通过 Class.forName(XOR 解密类名) 反射跳转主 Activity 并带 FLAG_ACTIVITY_NEW_TASK；入口 StartActivity 使用 Theme.Translucent + excludeFromRecents 隐藏启动痕迹。未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.ironit.StartActivity（Theme.Translucent，excludeFromRecents=true） | LAUNCHER 启动 → onCreate → new Handler().postDelayed(new k(this), 2001L) | 原生Activity | 无 | 无需用户操作，无可取消/跳过按钮 | `com.ironit.StartActivity.onCreate / com.ironit.k.run` |
| 2 | 业务功能触发 | 反射目标 Activity（Application.ALLATORIxDEMO() 返回类名，失败回退 MainActivity.class） | 2001ms 定时器到期 → StartActivity.ALLATORIxDEMO() → Intent + FLAG_ACTIVITY_NEW_TASK → startActivity + finish | 原生Activity | 无 | 无 | `com.ironit.StartActivity.ALLATORIxDEMO / com.ironit.Application.ALLATORIxDEMO` |
| 3 | 业务功能触发 | com.ironit.Naguan（singleTask，自绘布局 + ZeusNative 广告视图） | onCreate 解析 Intent extra 选择广告实例 → 填充 getAdvertiserName/getAdBodyText/getAdCallToAction → Random.nextInt(100) 概率命中则 addView(MediaView) → postDelayed(new com.ironit.d(this), 5000) | 原生Activity | **原文**：运行时由 ZeusNative.getAdvertiserName() / getAdBodyText() / getAdCallToAction() 返回，静态无原文<br>**译注**：把远端广告素材（广告主名称、正文、行动号召按钮）渲染成本地原生广告卡片，并在 5 秒后触发后续动作 | 点击广告行动号召按钮（无取消/跳过，属广告展示流程，非权限引导） | `com.ironit.Naguan.onCreate` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无任何无障碍引导文字：不存在 android:description、不存在设置跳转前的说明 Dialog/Activity/WebView/悬浮窗
- com.ironit.StartActivity：Theme.Translucent 透明页，全程零文本
- com.ironit.Naguan：文案全部来自远端广告素材（ZeusNative 的广告主名/正文/CTA），注入自绘 LinearLayout 的 TextView，非本地 strings 资源
- res 中的无障碍相关字符串仅为 androidx 支持库资源（accessibility_action_clickable_span、accessibility_custom_action_* 等），不含面向用户的说明文字
- 已初筛候选字符串（"下载完成，点击安装。"、"%1$s won't work unless you enable Google Play services." 等）分别来自 Pangle/socialbase 下载器与 GMS 可用性提示，均为三方 SDK 资源，不是无障碍引导

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | %1$s won't work unless you enable Google Play services. | 除非启用 Google Play 服务，否则 %1$s 无法运行。 | `三方 SDK（Google Play services common）资源字符串` | 良性透明说明 |
| en | %1$s is having trouble with Google Play services. Please try again. | %1$s 的 Google Play 服务出现问题，请重试。 | `三方 SDK（Google Play services common）资源字符串` | 良性透明说明 |
| zh | 下载完成，点击安装。 | 下载完成，点击安装。 | `三方 SDK（com.ss.android.socialbase 下载器 / Pangle）资源字符串` | 未知 |
| zh | 确认要删除%1$s的下载任务吗？ | 确认要删除 %1$s 的下载任务吗？ | `三方 SDK（com.ss.android.socialbase 下载器）资源字符串` | 未知 |
| en | Enable Google Play services | 启用 Google Play 服务 | `三方 SDK（Google Play services common）资源字符串` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无（不存在无障碍引导，故无拒绝/返回后的重跳逻辑；仅注册了 ActivityLifecycleCallbacks 用于友盟统计 MobclickAgent.onResume/onPause 与启动计数，未做任何设置页返回检测或定时拉起）
- **遮罩叠层 / 高仿系统设置页**：无（未申请 SYSTEM_ALERT_WINDOW，无全屏悬浮窗、无半透明引导遮罩、无高仿系统无障碍开关页；预筛 A11Y_OVERLAY 实为 androidx AccessibilityWindowInfoCompat 常量误报）
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无
- **良性降级 / 替代方案**：无（该应用根本不需要无障碍能力，因此也不存在降级路径；其真实能力集中在隐蔽广告注入）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：不应以 ACCESSIBILITY_SETTINGS / APP_DETAILS 跳转为触发条件（本样本永不发生）。若必须做 UTG 观测，应以冷启动 com.ironit.StartActivity 为锚点，在启动后 1.5–3 秒窗口内抓取实际落地的 Activity 与其自绘布局节点。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两类盲区：一是广告文案完全由远端下发（ZeusNative），静态无原文，纯静态检测可能误判为普通游戏；二是字符串经 XOR + Allatori 混淆、入口经反射 Class.forName 跳转，需还原后才能看清控制流。但静态加壳不阻挡运行期 UTG；本样本无加壳，运行期 UTG 可完整观测。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动透明过渡页** | com.ironit.StartActivity（Theme.Translucent、excludeFromRecents、无任何可交互控件） | 确认应用是否存在隐藏启动页与延时跳转，这是本样本规避检测与投放广告的关键前置环节 | 透明背景且节点树为空或仅 1 个根容器；停留约 2000ms 后自动跳转且该页不出现在最近任务 |
| **隐蔽广告注入页** | com.ironit.Naguan（singleTask，含 ZeusNative 注入的原生广告卡片：广告主名 / 正文 / CTA TextView + MediaView） | 这是应用真实行为的落点，可区分“正常游戏内嵌广告”与“脱离游戏进程的自绘广告注入” | 广告文案与游戏语言/品牌无关且由远端下发；广告节点直接挂在应用自绘 LinearLayout 而非官方 SDK 容器；5 秒后发生二次跳转 |
| **系统无障碍服务列表项（阴性验证）** | Settings → Accessibility → Installed services 列表 | 作为阴性对照，确认列表中不存在本应用条目，可直接否定“诱导开启无障碍”的假设 | 列表中无 Iron It / com.iron.clothes.smooth.perfect 条目；无带服务描述的无障碍开关项 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.ironit.StartActivity.onCreate`
- `com.ironit.StartActivity.ALLATORIxDEMO`
- `com.ironit.Naguan.onCreate`
- `com.ironit.Application.ALLATORIxDEMO`
- `com.ironit.o.w.ALLATORIxDEMO`
- `com.ironit.r.v.ALLATORIxDEMO`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**该样本中不存在无障碍权限申请与引导链**，用户问题预设的“UTG 页面流转”在本应用代码里没有对应实现，逐项核验结果如下：

- **Manifest 无无障碍服务**：`#1` 的 `application` 下没有任何带 `BIND_ACCESSIBILITY_SERVICE` 权限的 `service`，也没有 `android:accessibilityFeedbackType` / `android:description` 声明；与预筛“无障碍服务类 `[]`、`description []`”一致。
- **无无障碍设置跳转**：`classes.dex` 与 `assets/audience_network.dex` 中均搜不到 `ACTION_ACCESSIBILITY_SETTINGS`、`android.settings.ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`（应用自身代码），唯一命中 `android.settings.APPLICATION_DETAILS_SETTINGS` 的是 GMS 内部 `zzg.zzg`（三方 SDK）。
- **无 `AccessibilityService` 实现**：全包 `AccessibilityService` 相关命中仅来自 `androidx.core.accessibilityservice.AccessibilityServiceInfoCompat`（支持库，无服务主体）；`performGlobalAction`、`getRootInActiveWindow`、`dispatchGesture`、`TYPE_ACCESSIBILITY_OVERLAY` 均无应用侧调用。
- **预筛的 `A11Y_OVERLAY` 是误报**：其来源是 `androidx.core.view.accessibility.AccessibilityWindowInfoCompat.TYPE_ACCESSIBILITY_OVERLAY = 4` 这一常量及 `typeToString` 字符串，不是悬浮窗或无障碍叠加实现。Manifest 同样**未申请** `SYSTEM_ALERT_WINDOW`，`Settings.Secure "enabled_accessibility_services"` 仅出现在 AppLovin SDK 的环境探测（`com.applovin.impl.sdk.k#k`），且不涉及拉起设置页。
- **应用实际行为（与本问题无关的另一条链）**：这是 Unity 游戏外壳 + 隐蔽广告注入样本。`StartActivity`（`Theme.Translucent`、`excludeFromRecents`）在 `onCreate` 中 `postDelayed(…, 2001)` 后经 [StartActivity.ALLATORIxDEMO()](<resource-unit:#1.dex1 code:com.ironit.StartActivity#ALLATORIxDEMO>) 反射 `Class.forName(XOR 解密类名)` 跳转主 Activity；[Naguan.onCreate()](<resource-unit:#1.dex1 code:com.ironit.Naguan#onCreate>) 把远端广告内容（`getAdvertiserName` / `getAdBodyText` / `getAdCallToAction`）通过 `com.hera.ads.ZeusNative` 注入自绘布局，并按 `ZeusUtil.getString(key)` 解析的百分比 + `Random.nextInt(100)` 概率决定是否展示广告媒体，再 `postDelayed(…, 5000)` 触发后续动作。字符串由 [com.ironit.o.w.ALLATORIxDEMO()](<resource-unit:#1.dex1 code:com.ironit.o.w#ALLATORIxDEMO>) 与 [com.ironit.r.v.ALLATORIxDEMO()](<resource-unit:#1.dex1 code:com.ironit.r.v#ALLATORIxDEMO>) 的逐字符 XOR（`^28/^'?'`、`^'A'/^'t'`）还原，属静态可逆的 Allatori 式字符串混淆，非加壳或 VMP。
- **覆盖边界**：本轮为定向核验（Manifest + 5 个主 DEX 文本/符号 + `com.ironit` 主链方法），未展开 Unity `libil2cpp.so`/`libyida.so` 全量反编译；`Naguan` 的广告关闭/回调类 `com.ironit.d` 与 `com.hera.ads.ZeusNative` 内部未逐方法展开。就“无障碍引导”这一命题，上述证据已足以判定其不存在。

## 逐字文本（与无障碍无关，仅为已定位界面文本）

- GMS 标准提示（三方 SDK 资源，非本应用自绘）：`%1$s won't work unless you enable Google Play services.` —— 属 Google Play services 可用性提示，不是权限诱导。
- Pangle/字节下载器字符串（三方 SDK）：`下载完成，点击安装。`、`下载完成，点击打开。`、`确认要删除%1$s的下载任务吗？` —— 为 APK 下载安装流程提示，非无障碍引导。
- `Naguan` 页面文案全部来自远端广告素材（`ZeusNative.getAdBodyText()` 等），无静态原文。

## 给 UTG 检测的建议

本样本不应以“无障碍设置页”为触发条件，因为不会命中。若仍需确认，可在 `StartActivity` 冷启动后 2 秒内观测是否跳转至非 Unity 的 `com.ironit` 反射目标 Activity，并抓取 `Naguan` 页面是否为“远端广告文案注入的原生布局”，这才是该样本的真实判别点。

```json
{
  "static_visibility": "clear",
  "visibility_note": "Manifest、5 个主 DEX、res 与 assets/audience_network.dex 均可静态读取；无加壳、无 VMP。仅存在 Allatori 式逐字符 XOR 字符串混淆（com.ironit.o.w / com.ironit.r.v 的 ALLATORIxDEMO），可静态还原。远端广告文案由 ZeusNative 运行时下发，不含无障碍相关内容。",
  "summary_one_liner": "该应用完全不申请也不引导无障碍权限：Manifest 无 BIND_ACCESSIBILITY_SERVICE 服务、无 android:description、无 SYSTEM_ALERT_WINDOW，全包无 ACTION_ACCESSIBILITY_SETTINGS 跳转与 AccessibilityService 实现，其真实行为是 Unity 游戏外壳下的隐蔽广告注入。",
  "disguise_identity": {
    "app_display_name": "Iron It",
    "claimed_brand_or_persona": "Iron It（衣物熨烫类 Unity 小游戏，标签 @string/app_name 未改写，无品牌冒用）",
    "a11y_service_label": "无（未声明任何无障碍服务，系统无障碍列表中不会出现本应用条目）",
    "identity_mismatch": false,
    "obfuscation_tricks": "类名与方法名统一为 ALLATORIxDEMO（Allatori 混淆）；字符串以逐字符 XOR 存储（^28/^'?'、^'A'/^'t'）；通过 Class.forName(XOR 解密类名) 反射跳转主 Activity 并带 FLAG_ACTIVITY_NEW_TASK；入口 StartActivity 使用 Theme.Translucent + excludeFromRecents 隐藏启动痕迹。未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.ironit.StartActivity（Theme.Translucent，excludeFromRecents=true）",
      "trigger_event": "LAUNCHER 启动 → onCreate → new Handler().postDelayed(new k(this), 2001L)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "透明无界面启动页，用户看不到任何内容，也无任何权限说明或按钮",
      "user_action_requested": "无需用户操作，无可取消/跳过按钮",
      "code_anchor": "com.ironit.StartActivity.onCreate / com.ironit.k.run"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "反射目标 Activity（Application.ALLATORIxDEMO() 返回类名，失败回退 MainActivity.class）",
      "trigger_event": "2001ms 定时器到期 → StartActivity.ALLATORIxDEMO() → Intent + FLAG_ACTIVITY_NEW_TASK → startActivity + finish",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "直接跳入业务/广告容器页，全程不出现任何权限申请页或设置跳转",
      "user_action_requested": "无",
      "code_anchor": "com.ironit.StartActivity.ALLATORIxDEMO / com.ironit.Application.ALLATORIxDEMO"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "com.ironit.Naguan（singleTask，自绘布局 + ZeusNative 广告视图）",
      "trigger_event": "onCreate 解析 Intent extra 选择广告实例 → 填充 getAdvertiserName/getAdBodyText/getAdCallToAction → Random.nextInt(100) 概率命中则 addView(MediaView) → postDelayed(new com.ironit.d(this), 5000)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "运行时由 ZeusNative.getAdvertiserName() / getAdBodyText() / getAdCallToAction() 返回，静态无原文",
      "shown_text_zh": "把远端广告素材（广告主名称、正文、行动号召按钮）渲染成本地原生广告卡片，并在 5 秒后触发后续动作",
      "user_action_requested": "点击广告行动号召按钮（无取消/跳过，属广告展示流程，非权限引导）",
      "code_anchor": "com.ironit.Naguan.onCreate"
    }
  ],
  "text_presentation_locations": [
    "无任何无障碍引导文字：不存在 android:description、不存在设置跳转前的说明 Dialog/Activity/WebView/悬浮窗",
    "com.ironit.StartActivity：Theme.Translucent 透明页，全程零文本",
    "com.ironit.Naguan：文案全部来自远端广告素材（ZeusNative 的广告主名/正文/CTA），注入自绘 LinearLayout 的 TextView，非本地 strings 资源",
    "res 中的无障碍相关字符串仅为 androidx 支持库资源（accessibility_action_clickable_span、accessibility_custom_action_* 等），不含面向用户的说明文字",
    "已初筛候选字符串（\"下载完成，点击安装。\"、\"%1$s won't work unless you enable Google Play services.\" 等）分别来自 Pangle/socialbase 下载器与 GMS 可用性提示，均为三方 SDK 资源，不是无障碍引导"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "除非启用 Google Play 服务，否则 %1$s 无法运行。",
      "source_location": "三方 SDK（Google Play services common）资源字符串",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s is having trouble with Google Play services. Please try again.",
      "text_zh": "%1$s 的 Google Play 服务出现问题，请重试。",
      "source_location": "三方 SDK（Google Play services common）资源字符串",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "zh",
      "text_verbatim": "下载完成，点击安装。",
      "text_zh": "下载完成，点击安装。",
      "source_location": "三方 SDK（com.ss.android.socialbase 下载器 / Pangle）资源字符串",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "zh",
      "text_verbatim": "确认要删除%1$s的下载任务吗？",
      "text_zh": "确认要删除 %1$s 的下载任务吗？",
      "source_location": "三方 SDK（com.ss.android.socialbase 下载器）资源字符串",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Google Play services",
      "text_zh": "启用 Google Play 服务",
      "source_location": "三方 SDK（Google Play services common）资源字符串",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无（不存在无障碍引导，故无拒绝/返回后的重跳逻辑；仅注册了 ActivityLifecycleCallbacks 用于友盟统计 MobclickAgent.onResume/onPause 与启动计数，未做任何设置页返回检测或定时拉起）",
    "overlay_or_fake_settings": "无（未申请 SYSTEM_ALERT_WINDOW，无全屏悬浮窗、无半透明引导遮罩、无高仿系统无障碍开关页；预筛 A11Y_OVERLAY 实为 androidx AccessibilityWindowInfoCompat 常量误报）",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无",
    "benign_graceful_degradation": "无（该应用根本不需要无障碍能力，因此也不存在降级路径；其真实能力集中在隐蔽广告注入）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "不应以 ACCESSIBILITY_SETTINGS / APP_DETAILS 跳转为触发条件（本样本永不发生）。若必须做 UTG 观测，应以冷启动 com.ironit.StartActivity 为锚点，在启动后 1.5–3 秒窗口内抓取实际落地的 Activity 与其自绘布局节点。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动透明过渡页",
        "page_identifier": "com.ironit.StartActivity（Theme.Translucent、excludeFromRecents、无任何可交互控件）",
        "why_most_useful": "确认应用是否存在隐藏启动页与延时跳转，这是本样本规避检测与投放广告的关键前置环节",
        "observable_utg_signals": ["透明背景且节点树为空或仅 1 个根容器", "停留约 2000ms 后自动跳转且该页不出现在最近任务"]
      },
      {
        "page_role": "隐蔽广告注入页",
        "page_identifier": "com.ironit.Naguan（singleTask，含 ZeusNative 注入的原生广告卡片：广告主名 / 正文 / CTA TextView + MediaView）",
        "why_most_useful": "这是应用真实行为的落点，可区分“正常游戏内嵌广告”与“脱离游戏进程的自绘广告注入”",
        "observable_utg_signals": ["广告文案与游戏语言/品牌无关且由远端下发", "广告节点直接挂在应用自绘 LinearLayout 而非官方 SDK 容器", "5 秒后发生二次跳转"]
      },
      {
        "page_role": "系统无障碍服务列表项（阴性验证）",
        "page_identifier": "Settings → Accessibility → Installed services 列表",
        "why_most_useful": "作为阴性对照，确认列表中不存在本应用条目，可直接否定“诱导开启无障碍”的假设",
        "observable_utg_signals": ["列表中无 Iron It / com.iron.clothes.smooth.perfect 条目", "无带服务描述的无障碍开关项"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两类盲区：一是广告文案完全由远端下发（ZeusNative），静态无原文，纯静态检测可能误判为普通游戏；二是字符串经 XOR + Allatori 混淆、入口经反射 Class.forName 跳转，需还原后才能看清控制流。但静态加壳不阻挡运行期 UTG；本样本无加壳，运行期 UTG 可完整观测。"
  },
  "behavior_pattern_tags": [],
  "code_anchors": [
    "com.ironit.StartActivity.onCreate",
    "com.ironit.StartActivity.ALLATORIxDEMO",
    "com.ironit.Naguan.onCreate",
    "com.ironit.Application.ALLATORIxDEMO",
    "com.ironit.o.w.ALLATORIxDEMO",
    "com.ironit.r.v.ALLATORIxDEMO"
  ]
}
```

</details>
