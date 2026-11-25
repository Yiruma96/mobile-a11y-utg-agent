# BN_003__eb54b3ee0b｜专注自律与防沉迷管控 — GrayPause

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：109.6s

## 1. 一句话核心结论

- **核心申请方式**：GrayPause 在主界面以普通按钮 "Turn on app watcher" 按需跳转系统 ACTION_ACCESSIBILITY_SETTINGS，并以 android:description 与界面文案透明说明其仅读取前台应用名、从不读取屏幕内容，无遮罩、无循环强推、无身份伪装，未授权时保留手动灰度与计时器降级路径。
- **静态可见性说明**：全部引导逻辑位于单一 classes.dex 的 MainActivity（纯代码构建视图，无 XML layout、无 WebView、无 assets HTML、无本地加密资源）与 b.c#onClick 跳转分支中，可完整静态还原；无障碍能力受 res/xml/accessibility_config.xml 与 strings.xml 描述约束，均明文可见。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `eb54b3ee0b2aaa3aab14986b78e6b4ac7a149e78e889c6ba10a310ab6af76d09` |
| 包名 / 年份 | `com.lpw.graypause` / 2025-2026 |
| 家族 / 品类 | **专注自律与防沉迷管控**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.lpw.graypause_6.apk |
| 桌面显示名 | GrayPause |
| 引导页宣称品牌/身份 | GrayPause（F-Droid 开源专注自律/灰度防沉迷工具，真实身份） |
| 系统无障碍列表服务名 | GrayPause color apps |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。应用名、服务标签与说明文案一致，无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 isAccessibilityTool；代码存在混淆（类名 b.c、b.a、方法名 a-h）但属常规 R8 压缩，不影响行为可读性。 |
| 无障碍服务类名 | `com.lpw.graypause.AppWatchService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |
| 系统设置项说明 (`android:description`) | Watches which app is in front so grayscale can be switched off while you use the apps you chose in GrayPause (for example your gallery or camera). It reads only the app name, never screen content. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.lpw.graypause.MainActivity（LAUNCHER，singleTop） | onCreate：requestPermissions(POST_NOTIFICATIONS) 后以代码构建 ScrollView+LinearLayout 界面并调用 b()/h() | 原生Activity | **原文**：GrayPause / Grayscale permission missing / Grayscale now / Color apps / Turn on app watcher / Tips: long-press the app icon for quick timers. The "Color break" Quick Settings tile starts a break of the last length you used; tap it again to end the break early.<br>**译注**：应用标题、主界面按钮与提示：长按图标可快速起计时；快捷设置磁贴 "Color break" 按上次时长开始休息，再点一次提前结束。 | 自行浏览主界面，可选点击灰度开关、计时器或下方按钮；无强制操作，无弹窗拦截 | `com.lpw.graypause.MainActivity#onCreate` |
| 2 | 引导说明页 | MainActivity 内联卡片 LinearLayout（MainActivity.i() 生成，带 2dp 描边圆角） | h() 检测 a.c(this)==false（缺 WRITE_SECURE_SETTINGS）时 setVisibility(0) 显示 | 原生Activity | **原文**：Grayscale permission missing<br>GrayPause needs "Write secure settings" to switch grayscale. Android has no switch for it in Settings, but it only has to be granted once.<br><br>Easiest: with the free Shizuku app running, tap the button below.<br>Or, from adb:<br>adb shell pm grant com.lpw.graypause android.permission.WRITE_SECURE_SETTINGS<br>**译注**：缺少灰度权限：GrayPause 需要"写入安全设置"权限来切换灰度，Android 设置里没有对应开关，但只需授权一次。最简单的方式：安装并运行免费的 Shizuku 后点下方按钮；或用 adb 命令授权。 | 可选点击按钮（Get Shizuku / Open Shizuku and start it / Grant with Shizuku）或 "Copy adb command" 复制命令；可完全忽略 | `com.lpw.graypause.MainActivity#onCreate / com.lpw.graypause.MainActivity#h` |
| 3 | 业务功能触发 | MainActivity "Turn on app watcher" 按钮（this.h） | 用户主动点击该按钮 → b.c#onClick case 6 | 原生Activity | **原文**：Turn on app watcher<br>**译注**：开启应用监视器（即无障碍服务） | 点击按钮；按钮旁说明文案告知该服务"只看到哪个应用在前台"，用户可跳过此步继续使用灰度与计时器 | `b.c#onClick (case 6) / com.lpw.graypause.MainActivity#h` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | case 6 分支中 a.c(this)==false 时执行 mainActivity.f(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：直接跳转系统无障碍服务列表页，由用户在系统列表中自行找到 "GrayPause color apps" 并开启，无任何自绘遮罩或仿冒页面 | 在系统无障碍列表中选择 "GrayPause color apps" 并打开开关；可随时返回不开启 | `b.c#onClick (case 6)` |
| 5 | 系统无障碍列表项 | 系统无障碍列表中的 GrayPause color apps 条目说明 | 系统读取 res/xml/accessibility_config.xml 的 android:description | 系统无障碍页 | **原文**：Watches which app is in front so grayscale can be switched off while you use the apps you chose in GrayPause (for example your gallery or camera). It reads only the app name, never screen content.<br>**译注**：监视前台是哪个应用，以便在你使用 GrayPause 中选定的应用（例如相册或相机）时关闭灰度。它只读取应用名，从不读取屏幕内容。 | 用户阅读系统说明后决定是否开启；说明内容与应用实际能力（canRetrieveWindowContent=false）一致 | `res/xml/accessibility_config.xml / res/values/strings.xml#a11y_description` |
| 6 | 拒权反馈循环 | 返回 MainActivity（onResume） | onResume → Handler.post(b.n) → MainActivity.h() 刷新状态；case 6 另 postDelayed 500ms 刷新一次 | 原生Activity | **原文**：Keep chosen apps (gallery, camera…) in color. Needs the GrayPause app watcher, an accessibility service that only sees which app is open.<br>**译注**：让选定应用（相册、相机…）保持彩色。需要 GrayPause 应用监视器——一个只看到当前哪个应用在运行的无障碍服务。 | 不重复跳转、不循环拉起、不弹窗骚扰，仅停留在本页并保留按钮供用户再次选择；无取消按钮需求（无强制弹窗） | `com.lpw.graypause.MainActivity#onResume / b.d#run / com.lpw.graypause.MainActivity#h` |
| 7 | 获权后动作 | AppWatchService（BIND_ACCESSIBILITY_SERVICE） | 系统分发 TYPE_WINDOW_STATE_CHANGED 事件 → onAccessibilityEvent；或已具 WRITE_SECURE_SETTINGS 时 case 6 直接写 Settings.Secure 自启用 | 原生Activity | **原文**：Grayscale switches off while one of these apps is open, and back on when you leave it.<br>**译注**：当这些应用之一处于前台时灰度自动关闭，离开后恢复灰度。 | 无需用户操作；服务仅取 getPackageName()/getClassName() 比对用户已选应用集合，按需 a.l() 切换灰度，onUnbind 时恢复灰度，无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权 | `com.lpw.graypause.AppWatchService#onAccessibilityEvent / com.lpw.graypause.AppWatchService#onUnbind` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 主界面内联卡片（MainActivity.i() 生成的带描边 LinearLayout）："Grayscale permission missing" + WRITE_SECURE_SETTINGS/Shizuku/adb 分步说明与 "Copy adb command" 按钮
- MainActivity 主界面内联卡片："Notifications are off" + "Open notification settings" 按钮（跳 android.settings.APP_NOTIFICATION_SETTINGS）
- MainActivity 主界面 "Color apps" 区块说明文字（h() 动态设置）：未获权时为 "Keep chosen apps (gallery, camera…) in color. Needs the GrayPause app watcher…"，获权后改为 "Grayscale switches off while one of these apps is open…"
- MainActivity 底部 Tips 提示文字（长按图标快捷计时、"Color break" 磁贴说明）
- 系统无障碍服务列表项：res/values/strings.xml 的 a11y_description（经 res/xml/accessibility_config.xml 的 android:description 引用），服务标签 "GrayPause color apps"
- Shizuku 引导分支文案随状态切换："Get Shizuku" / "Open Shizuku and start it" / "Grant with Shizuku"（h() 依据 a.n(this) 返回值动态设置按钮文字）
- 无 WebView、无 assets HTML、无悬浮窗 Overlay、无自绘仿系统设置页

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | GrayPause needs "Write secure settings" to switch grayscale. Android has no switch for it in Settings, but it only has to be granted once.<br><br>Easiest: with the free Shizuku app running, tap the button below.<br>Or, from adb:<br>adb shell pm grant com.lpw.graypause android.permission.WRITE_SECURE_SETTINGS | GrayPause 需要"写入安全设置"权限来切换灰度。Android 设置里没有该开关，但只需授权一次。最简单的办法：运行免费的 Shizuku 应用后点击下面的按钮。或者用 adb 命令授权。 | `com.lpw.graypause.MainActivity#onCreate（硬编码字符串）` | 受限设置分步教学 |
| en | Watches which app is in front so grayscale can be switched off while you use the apps you chose in GrayPause (for example your gallery or camera). It reads only the app name, never screen content. | 监视前台是哪个应用，以便在你使用 GrayPause 中选定的应用（例如相册或相机）时关闭灰度。它只读取应用名，从不读取屏幕内容。 | `res/values/strings.xml key=a11y_description（经 res/xml/accessibility_config.xml 引用）` | 隐私承诺 |
| en | Keep chosen apps (gallery, camera…) in color. Needs the GrayPause app watcher, an accessibility service that only sees which app is open. | 让选定应用（相册、相机…）保持彩色。需要 GrayPause 应用监视器——一个只看到当前哪个应用在运行的无障碍服务。 | `com.lpw.graypause.MainActivity#h（硬编码字符串）` | 良性透明说明 |
| en | Notifications are off<br>Without them you won't see the countdown, or the "Grayscale now" and "+5 min" buttons, during a color break. Timers still work. | 通知已关闭：没有通知，你在彩色休息期间看不到倒计时以及"立即灰度""+5 分钟"按钮。计时器仍然可用。 | `com.lpw.graypause.MainActivity#onCreate（硬编码字符串）` | 良性透明说明 |
| en | Tips: long-press the app icon for quick timers. The "Color break" Quick Settings tile starts a break of the last length you used; tap it again to end the break early. | 提示：长按应用图标可快速起计时。快捷设置磁贴"Color break"会按你上次使用的时长开始一次休息；再次点击可提前结束。 | `com.lpw.graypause.MainActivity#onCreate（硬编码字符串）` | 良性透明说明 |
| en | Grayscale switches off while one of these apps is open, and back on when you leave it. | 当这些应用之一处于前台时灰度自动关闭，离开后恢复灰度。 | `com.lpw.graypause.MainActivity#h（硬编码字符串）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环强推。用户从系统设置页返回后仅触发 onResume → Handler.post(b.n) → MainActivity.h() 做一次状态刷新（case 6 另有 500ms 后 postDelayed 刷新），按钮仍保留供再次选择，无定时器重跳、无死循环、无阻塞返回。
- **遮罩叠层 / 高仿系统设置页**：无。全程无悬浮窗、无半透明引导遮罩、无高仿系统无障碍开关页；跳转即系统原生 android.settings.ACCESSIBILITY_SETTINGS。
- **Android 13+ 受限设置（Restricted Settings）应对**：针对 WRITE_SECURE_SETTINGS（并非 Android 13 受限设置）给出透明分步教学：界面明文说明系统无开关、推荐用 Shizuku 授权或执行 adb shell pm grant com.lpw.graypause android.permission.WRITE_SECURE_SETTINGS，并提供 "Copy adb command" 一键复制（b.c#onClick case 2）；未引导用户进入应用详情"允许受限设置"，也无 Session 安装器绕过。
- **获权后即时行为与防撤权机制**：无。获权后无自点确认弹窗、无自授权；onUnbind 时清空缓存包名并按状态恢复灰度，不存在用 GLOBAL_ACTION_BACK/HOME 阻止用户撤权或监听设置页的行为。（唯一可注意点：已具备 WRITE_SECURE_SETTINGS 时 case 6 会直接向 Settings.Secure 写入 enabled_accessibility_services 与 accessibility_enabled=1 以自启用服务，但该特权本身须由用户先通过 Shizuku/adb 明确授予，且界面已如实说明。）
- **良性降级 / 替代方案**：有。未授予无障碍/未授权 WRITE_SECURE_SETTINGS 时，应用仍可手动开启/关闭灰度、使用自定义计时器（Custom timer 对话框）、通过快捷设置磁贴 "Color break" 起休息；仅 "Color apps" 前台联动功能被禁用并以文字说明原因，且 "Grayscale now" / 计时器按钮仅在获得写安全设置权限后启用。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 且来源为 com.lpw.graypause 时立即快照（对应点击 "Turn on app watcher" 瞬间）；并在返回 MainActivity 后 600ms 再抓一帧，用于确认是良性单次跳转还是循环重跳。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区。唯一需注意：应用存在代码混淆（b.c、b.a 等单字母类名）与 Shizuku 特权通道，纯静态扫描易把 "WRITE_SECURE_SETTINGS 直写 Settings.Secure" 误判为静默提权，实际为界面明示、用户预先经 Shizuku/adb 授权的开源用法；无 WebView/远端 HTML/加壳/一阶段 Dropper。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动主界面（含灰度权限缺失卡片与 Turn on app watcher 按钮）** | com.lpw.graypause.MainActivity，单 Activity 纯代码 LinearLayout，含文本 "Grayscale permission missing"、"Turn on app watcher"、"Grayscale now" | 确认无障碍引导是用户按需点击而非冷启动强制弹窗，并核对权限说明文案是否与实际能力一致 | 无 Dialog / 无 Overlay 窗口节点；按钮文案 Turn on app watcher 存在且可跳过；卡片文本包含 adb shell pm grant 明文命令 |
| **跳转后的系统无障碍服务列表项** | 系统设置 com.android.settings 无障碍列表中的 "GrayPause color apps" 条目及其 description 摘要 | 核验服务标签与系统说明是否与主界面宣称一致，排除伪造 isAccessibilityTool 或仿冒条目 | 条目 label = GrayPause color apps；description 首句 Watches which app is in front…；无第三方/仿冒品牌名 |
| **返回主界面后的状态页** | MainActivity 重新可见，Color apps 区块说明文字随授权状态变化 | 区分良性一次性刷新与拒权循环强推（恶意应用常在此处 800ms 内再次压栈遮罩或重跳设置） | 无新压栈的 Activity/Overlay；无重复 ACCESSIBILITY_SETTINGS 跳转；文案切换为 Keep chosen apps… / Grayscale switches off… |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.lpw.graypause.MainActivity#onCreate`
- `com.lpw.graypause.MainActivity#h`
- `b.c#onClick`
- `com.lpw.graypause.AppWatchService#onAccessibilityEvent`
- `res/xml/accessibility_config.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（GrayPause 无障碍权限申请路径）

**性质判断：良性、透明、按需触发。全流程静态可见（无加壳、无加密载荷、无 WebView、无悬浮窗）。**

**引导链路（纯运行期页面流转）**
1. 冷启动 [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.lpw.graypause.MainActivity#onCreate>) 用纯代码构建 `ScrollView + LinearLayout` 界面，**不自动弹窗、不跳设置**，仅在 `onCreate` 申请 `POST_NOTIFICATIONS`（通知权限，非无障碍）。
2. 主界面出现两个条件卡片：`Grayscale permission missing`（WRITE_SECURE_SETTINGS 缺失时）与 `Notifications are off`（通知关闭时）；两个卡片都带有操作按钮，用户可自行选择是否操作。
3. 无障碍权限的入口是一个普通按钮 `Turn on app watcher`（[b.c#onClick](<resource-unit:#1.dex1 code:b.c#onClick>) case 6）。点击后：若已具备 `WRITE_SECURE_SETTINGS`（Shizuku/adb 授权），则直接向 `enabled_accessibility_services` 写入自身组件名并置 `accessibility_enabled=1`；否则只发出一条 `Intent("android.settings.ACCESSIBILITY_SETTINGS")` 跳系统设置页，无遮罩、无高仿页、无倒计时强推。
4. 从设置页返回后 `onResume → Handler.post → h()` 仅刷新 UI 状态（隐藏按钮、更新文案），**不重复跳转、不循环拉起**；另在 case 6 后 `postDelayed 500ms` 再做一次 UI 刷新。
5. 获权后 [AppWatchService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.lpw.graypause.AppWatchService#onAccessibilityEvent>) 只处理 `TYPE_WINDOW_STATE_CHANGED` 取前台包名，`canRetrieveWindowContent="false"`，不读屏内容；`onUnbind` 恢复灰度，无自保护/防撤权逻辑。

**关键良性证据**
- 无障碍 `android:description` 与界面文案明确自述"只读应用名、从不读屏内容"、WRITE_SECURE_SETTINGS "Android 设置里没有开关，但只需授权一次"，并给出 adb 命令原文，属**受限设置分步教学 + 隐私承诺**的正当披露。
- 身份一致：`app_name=GrayPause`、服务标签 `GrayPause color apps`，无空白/同形字/多 alias/伪造 `isAccessibilityTool`。
- 存在安全降级：未授权时手动灰度开关、计时器、QS 磁贴 `Color break` 仍可用，仅"Color apps"联动功能提示"Needs the GrayPause app watcher"。
- 附带观察（非风险）：`Settings.Secure` 直写自启用依赖用户先行授予 Shizuku/adb 特权，属开源应用常见的高级授权路径，界面已完整说明。

**一处实现缺陷（非安全风险）**：`MainActivity.h()` 中 `enabled_accessibility_services` 检测循环结束恒置 `z = false`，导致 `Turn on app watcher` 按钮获权后仍可能显示，属逻辑 bug，不影响定性。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑位于单一 classes.dex 的 MainActivity（纯代码构建视图，无 XML layout、无 WebView、无 assets HTML、无本地加密资源）与 b.c#onClick 跳转分支中，可完整静态还原；无障碍能力受 res/xml/accessibility_config.xml 与 strings.xml 描述约束，均明文可见。",
  "summary_one_liner": "GrayPause 在主界面以普通按钮 \"Turn on app watcher\" 按需跳转系统 ACTION_ACCESSIBILITY_SETTINGS，并以 android:description 与界面文案透明说明其仅读取前台应用名、从不读取屏幕内容，无遮罩、无循环强推、无身份伪装，未授权时保留手动灰度与计时器降级路径。",
  "disguise_identity": {
    "app_display_name": "GrayPause",
    "claimed_brand_or_persona": "GrayPause（F-Droid 开源专注自律/灰度防沉迷工具，真实身份）",
    "a11y_service_label": "GrayPause color apps",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。应用名、服务标签与说明文案一致，无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 isAccessibilityTool；代码存在混淆（类名 b.c、b.a、方法名 a-h）但属常规 R8 压缩，不影响行为可读性。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.lpw.graypause.MainActivity（LAUNCHER，singleTop）",
      "trigger_event": "onCreate：requestPermissions(POST_NOTIFICATIONS) 后以代码构建 ScrollView+LinearLayout 界面并调用 b()/h()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "GrayPause / Grayscale permission missing / Grayscale now / Color apps / Turn on app watcher / Tips: long-press the app icon for quick timers. The \"Color break\" Quick Settings tile starts a break of the last length you used; tap it again to end the break early.",
      "shown_text_zh": "应用标题、主界面按钮与提示：长按图标可快速起计时；快捷设置磁贴 \"Color break\" 按上次时长开始休息，再点一次提前结束。",
      "user_action_requested": "自行浏览主界面，可选点击灰度开关、计时器或下方按钮；无强制操作，无弹窗拦截",
      "code_anchor": "com.lpw.graypause.MainActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 内联卡片 LinearLayout（MainActivity.i() 生成，带 2dp 描边圆角）",
      "trigger_event": "h() 检测 a.c(this)==false（缺 WRITE_SECURE_SETTINGS）时 setVisibility(0) 显示",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Grayscale permission missing\nGrayPause needs \"Write secure settings\" to switch grayscale. Android has no switch for it in Settings, but it only has to be granted once.\n\nEasiest: with the free Shizuku app running, tap the button below.\nOr, from adb:\nadb shell pm grant com.lpw.graypause android.permission.WRITE_SECURE_SETTINGS",
      "shown_text_zh": "缺少灰度权限：GrayPause 需要\"写入安全设置\"权限来切换灰度，Android 设置里没有对应开关，但只需授权一次。最简单的方式：安装并运行免费的 Shizuku 后点下方按钮；或用 adb 命令授权。",
      "user_action_requested": "可选点击按钮（Get Shizuku / Open Shizuku and start it / Grant with Shizuku）或 \"Copy adb command\" 复制命令；可完全忽略",
      "code_anchor": "com.lpw.graypause.MainActivity#onCreate / com.lpw.graypause.MainActivity#h"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity \"Turn on app watcher\" 按钮（this.h）",
      "trigger_event": "用户主动点击该按钮 → b.c#onClick case 6",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Turn on app watcher",
      "shown_text_zh": "开启应用监视器（即无障碍服务）",
      "user_action_requested": "点击按钮；按钮旁说明文案告知该服务\"只看到哪个应用在前台\"，用户可跳过此步继续使用灰度与计时器",
      "code_anchor": "b.c#onClick (case 6) / com.lpw.graypause.MainActivity#h"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "case 6 分支中 a.c(this)==false 时执行 mainActivity.f(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "直接跳转系统无障碍服务列表页，由用户在系统列表中自行找到 \"GrayPause color apps\" 并开启，无任何自绘遮罩或仿冒页面",
      "user_action_requested": "在系统无障碍列表中选择 \"GrayPause color apps\" 并打开开关；可随时返回不开启",
      "code_anchor": "b.c#onClick (case 6)"
    },
    {
      "step": 5,
      "stage": "系统无障碍列表项",
      "screen_or_component": "系统无障碍列表中的 GrayPause color apps 条目说明",
      "trigger_event": "系统读取 res/xml/accessibility_config.xml 的 android:description",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Watches which app is in front so grayscale can be switched off while you use the apps you chose in GrayPause (for example your gallery or camera). It reads only the app name, never screen content.",
      "shown_text_zh": "监视前台是哪个应用，以便在你使用 GrayPause 中选定的应用（例如相册或相机）时关闭灰度。它只读取应用名，从不读取屏幕内容。",
      "user_action_requested": "用户阅读系统说明后决定是否开启；说明内容与应用实际能力（canRetrieveWindowContent=false）一致",
      "code_anchor": "res/xml/accessibility_config.xml / res/values/strings.xml#a11y_description"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "返回 MainActivity（onResume）",
      "trigger_event": "onResume → Handler.post(b.n) → MainActivity.h() 刷新状态；case 6 另 postDelayed 500ms 刷新一次",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Keep chosen apps (gallery, camera…) in color. Needs the GrayPause app watcher, an accessibility service that only sees which app is open.",
      "shown_text_zh": "让选定应用（相册、相机…）保持彩色。需要 GrayPause 应用监视器——一个只看到当前哪个应用在运行的无障碍服务。",
      "user_action_requested": "不重复跳转、不循环拉起、不弹窗骚扰，仅停留在本页并保留按钮供用户再次选择；无取消按钮需求（无强制弹窗）",
      "code_anchor": "com.lpw.graypause.MainActivity#onResume / b.d#run / com.lpw.graypause.MainActivity#h"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "AppWatchService（BIND_ACCESSIBILITY_SERVICE）",
      "trigger_event": "系统分发 TYPE_WINDOW_STATE_CHANGED 事件 → onAccessibilityEvent；或已具 WRITE_SECURE_SETTINGS 时 case 6 直接写 Settings.Secure 自启用",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Grayscale switches off while one of these apps is open, and back on when you leave it.",
      "shown_text_zh": "当这些应用之一处于前台时灰度自动关闭，离开后恢复灰度。",
      "user_action_requested": "无需用户操作；服务仅取 getPackageName()/getClassName() 比对用户已选应用集合，按需 a.l() 切换灰度，onUnbind 时恢复灰度，无自点确认、无 GLOBAL_ACTION_BACK/HOME 阻止撤权",
      "code_anchor": "com.lpw.graypause.AppWatchService#onAccessibilityEvent / com.lpw.graypause.AppWatchService#onUnbind"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 主界面内联卡片（MainActivity.i() 生成的带描边 LinearLayout）：\"Grayscale permission missing\" + WRITE_SECURE_SETTINGS/Shizuku/adb 分步说明与 \"Copy adb command\" 按钮",
    "MainActivity 主界面内联卡片：\"Notifications are off\" + \"Open notification settings\" 按钮（跳 android.settings.APP_NOTIFICATION_SETTINGS）",
    "MainActivity 主界面 \"Color apps\" 区块说明文字（h() 动态设置）：未获权时为 \"Keep chosen apps (gallery, camera…) in color. Needs the GrayPause app watcher…\"，获权后改为 \"Grayscale switches off while one of these apps is open…\"",
    "MainActivity 底部 Tips 提示文字（长按图标快捷计时、\"Color break\" 磁贴说明）",
    "系统无障碍服务列表项：res/values/strings.xml 的 a11y_description（经 res/xml/accessibility_config.xml 的 android:description 引用），服务标签 \"GrayPause color apps\"",
    "Shizuku 引导分支文案随状态切换：\"Get Shizuku\" / \"Open Shizuku and start it\" / \"Grant with Shizuku\"（h() 依据 a.n(this) 返回值动态设置按钮文字）",
    "无 WebView、无 assets HTML、无悬浮窗 Overlay、无自绘仿系统设置页"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "GrayPause needs \"Write secure settings\" to switch grayscale. Android has no switch for it in Settings, but it only has to be granted once.\n\nEasiest: with the free Shizuku app running, tap the button below.\nOr, from adb:\nadb shell pm grant com.lpw.graypause android.permission.WRITE_SECURE_SETTINGS",
      "text_zh": "GrayPause 需要\"写入安全设置\"权限来切换灰度。Android 设置里没有该开关，但只需授权一次。最简单的办法：运行免费的 Shizuku 应用后点击下面的按钮。或者用 adb 命令授权。",
      "source_location": "com.lpw.graypause.MainActivity#onCreate（硬编码字符串）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Watches which app is in front so grayscale can be switched off while you use the apps you chose in GrayPause (for example your gallery or camera). It reads only the app name, never screen content.",
      "text_zh": "监视前台是哪个应用，以便在你使用 GrayPause 中选定的应用（例如相册或相机）时关闭灰度。它只读取应用名，从不读取屏幕内容。",
      "source_location": "res/values/strings.xml key=a11y_description（经 res/xml/accessibility_config.xml 引用）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Keep chosen apps (gallery, camera…) in color. Needs the GrayPause app watcher, an accessibility service that only sees which app is open.",
      "text_zh": "让选定应用（相册、相机…）保持彩色。需要 GrayPause 应用监视器——一个只看到当前哪个应用在运行的无障碍服务。",
      "source_location": "com.lpw.graypause.MainActivity#h（硬编码字符串）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Notifications are off\nWithout them you won't see the countdown, or the \"Grayscale now\" and \"+5 min\" buttons, during a color break. Timers still work.",
      "text_zh": "通知已关闭：没有通知，你在彩色休息期间看不到倒计时以及\"立即灰度\"\"+5 分钟\"按钮。计时器仍然可用。",
      "source_location": "com.lpw.graypause.MainActivity#onCreate（硬编码字符串）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Tips: long-press the app icon for quick timers. The \"Color break\" Quick Settings tile starts a break of the last length you used; tap it again to end the break early.",
      "text_zh": "提示：长按应用图标可快速起计时。快捷设置磁贴\"Color break\"会按你上次使用的时长开始一次休息；再次点击可提前结束。",
      "source_location": "com.lpw.graypause.MainActivity#onCreate（硬编码字符串）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Grayscale switches off while one of these apps is open, and back on when you leave it.",
      "text_zh": "当这些应用之一处于前台时灰度自动关闭，离开后恢复灰度。",
      "source_location": "com.lpw.graypause.MainActivity#h（硬编码字符串）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环强推。用户从系统设置页返回后仅触发 onResume → Handler.post(b.n) → MainActivity.h() 做一次状态刷新（case 6 另有 500ms 后 postDelayed 刷新），按钮仍保留供再次选择，无定时器重跳、无死循环、无阻塞返回。",
    "overlay_or_fake_settings": "无。全程无悬浮窗、无半透明引导遮罩、无高仿系统无障碍开关页；跳转即系统原生 android.settings.ACCESSIBILITY_SETTINGS。",
    "restricted_settings_13plus_coaching": "针对 WRITE_SECURE_SETTINGS（并非 Android 13 受限设置）给出透明分步教学：界面明文说明系统无开关、推荐用 Shizuku 授权或执行 adb shell pm grant com.lpw.graypause android.permission.WRITE_SECURE_SETTINGS，并提供 \"Copy adb command\" 一键复制（b.c#onClick case 2）；未引导用户进入应用详情\"允许受限设置\"，也无 Session 安装器绕过。",
    "post_grant_anti_removal": "无。获权后无自点确认弹窗、无自授权；onUnbind 时清空缓存包名并按状态恢复灰度，不存在用 GLOBAL_ACTION_BACK/HOME 阻止用户撤权或监听设置页的行为。（唯一可注意点：已具备 WRITE_SECURE_SETTINGS 时 case 6 会直接向 Settings.Secure 写入 enabled_accessibility_services 与 accessibility_enabled=1 以自启用服务，但该特权本身须由用户先通过 Shizuku/adb 明确授予，且界面已如实说明。）",
    "benign_graceful_degradation": "有。未授予无障碍/未授权 WRITE_SECURE_SETTINGS 时，应用仍可手动开启/关闭灰度、使用自定义计时器（Custom timer 对话框）、通过快捷设置磁贴 \"Color break\" 起休息；仅 \"Color apps\" 前台联动功能被禁用并以文字说明原因，且 \"Grayscale now\" / 计时器按钮仅在获得写安全设置权限后启用。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 且来源为 com.lpw.graypause 时立即快照（对应点击 \"Turn on app watcher\" 瞬间）；并在返回 MainActivity 后 600ms 再抓一帧，用于确认是良性单次跳转还是循环重跳。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动主界面（含灰度权限缺失卡片与 Turn on app watcher 按钮）",
        "page_identifier": "com.lpw.graypause.MainActivity，单 Activity 纯代码 LinearLayout，含文本 \"Grayscale permission missing\"、\"Turn on app watcher\"、\"Grayscale now\"",
        "why_most_useful": "确认无障碍引导是用户按需点击而非冷启动强制弹窗，并核对权限说明文案是否与实际能力一致",
        "observable_utg_signals": ["无 Dialog / 无 Overlay 窗口节点", "按钮文案 Turn on app watcher 存在且可跳过", "卡片文本包含 adb shell pm grant 明文命令"]
      },
      {
        "page_role": "跳转后的系统无障碍服务列表项",
        "page_identifier": "系统设置 com.android.settings 无障碍列表中的 \"GrayPause color apps\" 条目及其 description 摘要",
        "why_most_useful": "核验服务标签与系统说明是否与主界面宣称一致，排除伪造 isAccessibilityTool 或仿冒条目",
        "observable_utg_signals": ["条目 label = GrayPause color apps", "description 首句 Watches which app is in front…", "无第三方/仿冒品牌名"]
      },
      {
        "page_role": "返回主界面后的状态页",
        "page_identifier": "MainActivity 重新可见，Color apps 区块说明文字随授权状态变化",
        "why_most_useful": "区分良性一次性刷新与拒权循环强推（恶意应用常在此处 800ms 内再次压栈遮罩或重跳设置）",
        "observable_utg_signals": ["无新压栈的 Activity/Overlay", "无重复 ACCESSIBILITY_SETTINGS 跳转", "文案切换为 Keep chosen apps… / Grayscale switches off…"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区。唯一需注意：应用存在代码混淆（b.c、b.a 等单字母类名）与 Shizuku 特权通道，纯静态扫描易把 \"WRITE_SECURE_SETTINGS 直写 Settings.Secure\" 误判为静默提权，实际为界面明示、用户预先经 Shizuku/adb 授权的开源用法；无 WebView/远端 HTML/加壳/一阶段 Dropper。"
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
    "com.lpw.graypause.MainActivity#onCreate",
    "com.lpw.graypause.MainActivity#h",
    "b.c#onClick",
    "com.lpw.graypause.AppWatchService#onAccessibilityEvent",
    "res/xml/accessibility_config.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
