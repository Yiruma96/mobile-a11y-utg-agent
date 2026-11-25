# BN_036__7afde83f96｜极简桌面与双击锁屏 — TV Launcher

> **类型**：开源良性无障碍应用  ｜  **来源池**：`Benign_OSS_2024_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：187.0s

## 1. 一句话核心结论

- **核心申请方式**：仅在用户于『About & Settings』弹窗内手动打开 Override TV Default Launcher 开关时，先 Toast 说明再跳系统无障碍设置页，说明文案透明、可取消、无拒权循环与遮罩。
- **静态可见性说明**：DEX 与全部资源静态可见：classes.dex 中 com.tvlauncher 仅 6 个类，无障碍服务、引导弹窗、跳转 Intent 与全部文案（strings.xml / dialog_about.xml / accessibility_service_config.xml）均可直接还原；无加壳、无 VMP、无 AES 密文、无远端 HTML、无 WebView、无动态加载。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`BENIGN_TRANSPARENT_RATIONALE`（透明诚实说明具体用途与动作边界）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）、`BENIGN_HONEST_IDENTITY_AND_SCOPE`（桌面名/说明页/系统服务名三方如实一致）、`BENIGN_ALTERNATIVE_MODE_OFFERED`（提供免无障碍替代方案(ADB/Root/手动/仅观看)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `7afde83f96ccf30d1bc69ca06692d385800d2d9a14dd5f7d85fb4ad4f3c5c210` |
| 包名 / 年份 | `com.tvlauncher` / 2025-2026 |
| 家族 / 品类 | **极简桌面与双击锁屏**（同池样本数：1） |
| 原始来源标识 | https://f-droid.org/repo/com.tvlauncher_10602.apk |
| 桌面显示名 | TV Launcher |
| 引导页宣称品牌/身份 | TV Launcher（F-Droid 开源项目 wiiguy/lightweight_androidtv_launcher，GPL v3.0，界面显示 vX.Y (FOSS)） |
| 系统无障碍列表服务名 | TV Launcher（服务未单独设置 android:label，继承 application android:label=@string/app_name） |
| 三方身份是否错配/伪装 | **否（如实一致）** ｜ 混淆手法：无。服务描述为直白的真实用途说明；无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.tvlauncher.TvHomeOverrideService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES` |
| 系统设置项说明 (`android:description`) | Allows TV Launcher to detect the Home button on TV remotes and return to this launcher. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.tvlauncher.MainActivity（HOME / LAUNCHER / LEANBACK_LAUNCHER，launchMode=singleTop，landscape） | onCreate → setContentView(R.layout.activity_main) → setupClickListeners()；onResume → loadAppSlots()、applyWallpaper()、更新检查 | 原生Activity | **原文**：无（冷启动不出现任何无障碍引导文案）<br>**译注**：无 | 无强制动作，正常浏览桌面应用图标 | `com.tvlauncher.MainActivity.onCreate / com.tvlauncher.MainActivity.onResume` |
| 2 | 引导说明页 | MainActivity 原生 AlertDialog（自定义视图 res/layout/dialog_about.xml，标题 @string/about_title，关闭按钮 @string/about_close） | 用户点击桌面 aboutButton → setupClickListeners$lambda$2 → showAboutDialog() | 原生Dialog | **原文**：Settings & About \| Override TV Default Launcher \| Intercepts TV Home key on devices that lock the default launcher \| Kill Stock Launcher Background RAM \| Frees 100MB+ RAM by stopping heavy OEM TV home screens \| Close<br>**译注**：设置与关于｜覆盖电视默认桌面｜在锁定默认桌面的设备上拦截电视 Home 键｜结束后台预装桌面以释放内存｜通过停止繁重的 OEM 电视桌面释放 100MB+ 内存｜关闭 | 可选：点击开关卡片或拨动 SwitchCompat；存在 Close 取消按钮，可直接退出不做任何授权 | `com.tvlauncher.MainActivity.showAboutDialog + res/layout/dialog_about.xml + res/values/strings.xml(about_title/about_close/override_default_launcher/override_default_launcher_desc)` |
| 3 | 跳受限设置 | Toast + 系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS（失败降级 android.settings.SETTINGS） | 用户手动打开 Override TV Default Launcher 开关 → SwitchCompat.OnCheckedChangeListener = showAboutDialog$lambda$21（先写 SharedPreferences launcher_settings/home_override_enabled，再判断服务是否已启用） | 原生Dialog | **原文**：Please enable TV Launcher under Accessibility Services to intercept the Home key.<br>**译注**：请在『无障碍服务』中启用 TV Launcher，以便拦截 Home 键。 | 要求用户点击 Toast 后自动跳转到的系统无障碍列表，手动找到并开启 TV Launcher 服务；用户可拒绝、可直接返回 | `com.tvlauncher.MainActivity.showAboutDialog$lambda$21 → com.tvlauncher.MainActivity.openAccessibilitySettings` |
| 4 | 跳无障碍设置 | 系统『无障碍』服务列表项：TV Launcher，描述取 @string/accessibility_service_description | openAccessibilitySettings() 先置 TvHomeOverrideService.c = now+5000ms（静默期），再顺序 startActivity：ACCESSIBILITY_SETTINGS、ACCESSIBILITY_SETTINGS(NEW_TASK)、SETTINGS | 系统无障碍页 | **原文**：Allows TV Launcher to detect the Home button on TV remotes and return to this launcher.<br>**译注**：允许 TV Launcher 检测电视遥控器上的 Home 键，并返回到本桌面。 | 用户在系统页面内自行决定是否开启该服务（系统页自带取消/返回） | `res/xml/accessibility_service_config.xml + res/values/strings.xml(accessibility_service_description) + com.tvlauncher.MainActivity.openAccessibilitySettings` |
| 5 | 拒权反馈循环 | MainActivity.onResume（返回应用后） | 从系统设置返回触发 onResume | 原生Activity | 无 | 无；用户可长期保持未开启状态，桌面功能照常可用（仅 Home 键拦截失效） | `com.tvlauncher.MainActivity.onResume` |
| 6 | 获权后动作 | com.tvlauncher.TvHomeOverrideService（BIND_ACCESSIBILITY_SERVICE，flagRequestFilterKeyEvents=true，typeWindowStateChanged） | onKeyEvent(KEYCODE_HOME, ACTION_DOWN) → a() 以 NEW_TASK\|CLEAR_TOP\|SINGLE_TOP 启动 MainActivity；onAccessibilityEvent(TYPE_WINDOW_STATE_CHANGED) 检测到其它桌面出现 setting/preference/dialog 类窗口后 postDelayed(30ms) 拉回本桌面 | 原生Activity | 无 | 无 | `com.tvlauncher.TvHomeOverrideService.onKeyEvent / onAccessibilityEvent / onServiceConnected` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity 的 AlertDialog（showAboutDialog，自定义视图 res/layout/dialog_about.xml）内的 SwitchCompat 标题与 12sp 说明 TextView：Override TV Default Launcher / Intercepts TV Home key on devices that lock the default launcher
- 同一弹窗内开关切换后的 Toast：@string/enable_accessibility_prompt（Please enable TV Launcher under Accessibility Services to intercept the Home key.）
- 系统『无障碍』列表服务条目描述：@string/accessibility_service_description（Allows TV Launcher to detect the Home button on TV remotes and return to this launcher.）
- 弹窗底部按钮：@string/about_close（Close）与对话框标题 @string/about_title（Settings & About）
- 关于区文案 @string/about_message：TV Launcher / Version %1$s / Free and open source. / License: GNU GPL v3.0.
- 无 WebView / 本地 HTML / 远端 HTML / 悬浮窗 Overlay / 半透明引导遮罩 / 仿系统设置页，全部引导文字均承载于原生 Dialog、Toast 与系统无障碍描述

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Allows TV Launcher to detect the Home button on TV remotes and return to this launcher. | 允许 TV Launcher 检测电视遥控器上的 Home 键，并返回到本桌面。 | `res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml android:description 引用）` | 良性透明说明 |
| en | Please enable TV Launcher under Accessibility Services to intercept the Home key. | 请在『无障碍服务』中启用 TV Launcher，以便拦截 Home 键。 | `res/values/strings.xml key=enable_accessibility_prompt（Toast，由 showAboutDialog$lambda$21 触发）` | 受限设置分步教学 |
| en | Override TV Default Launcher | 覆盖电视默认桌面 | `res/values/strings.xml key=override_default_launcher（dialog_about.xml homeOverrideSwitch）` | 良性透明说明 |
| en | Intercepts TV Home key on devices that lock the default launcher | 在锁定默认桌面的设备上拦截电视 Home 键 | `res/values/strings.xml key=override_default_launcher_desc（dialog_about.xml 说明 TextView）` | 良性透明说明 |
| en | This stops background processes of pre-installed TV launchers to free RAM. Launchers you installed yourself are never touched. You can turn it off anytime in About. | 此操作会停止预装电视桌面的后台进程以释放内存。你自己安装的桌面永远不会被影响。你可以随时在『关于』中关闭它。 | `res/values/strings.xml key=suppress_stock_ram_confirm（内存清理确认对话框正文）` | 良性透明说明 |
| en | TV Launcher<br>Version %1$s<br><br>Free and open source.<br>License: GNU GPL v3.0.<br><br>%2$s | TV Launcher<br>版本 %1$s<br><br>自由且开源。<br>许可证：GNU GPL v3.0。<br><br>%2$s | `res/values/strings.xml key=about_message` | 良性透明说明 |
| en | Close | 关闭 | `res/values/strings.xml key=about_close（对话框取消/关闭按钮）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无循环。拒绝或在系统无障碍页返回后，MainActivity.onResume 仅执行 loadAppSlots()/applyWallpaper()/更新检查，不重跳设置页、不重复弹窗；仅当用户下次打开『About & Settings』并再次拨动开关时才会重新出现 Toast + 跳转。openAccessibilitySettings 另外设置了 5 秒静默期（TvHomeOverrideService.c = now+5000），避免跳转过程中被服务自身打断。
- **遮罩叠层 / 高仿系统设置页**：无。不使用 TYPE_APPLICATION_OVERLAY 或任何悬浮窗权限，不叠加半透明引导遮罩，不绘制高仿系统无障碍开关页；跳转目标为系统真实 ACCESSIBILITY_SETTINGS（失败时降级 SETTINGS/TV_SETTINGS/DEVICE_INFO_SETTINGS）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。全包未见引导用户进入应用详情页右上角菜单开启『允许受限设置』，也无 Session 安装器绕过；相关字符串 update_permission_needed（Allow installs from this app in Settings.）仅指向自身 GitHub 自更新所需的『安装未知应用』授权，与无障碍无关。
- **获权后即时行为与防撤权机制**：无。服务未使用 performGlobalAction、未自动点击确认、未监听无障碍设置页阻止撤权；仅拦截 KEYCODE_HOME 拉起本桌面，以及在其他已安装桌面出现 setting/preference/dialog 窗口时 30ms 后把本桌面拉回前台（其声明用途即 Home 键覆盖）。
- **良性降级 / 替代方案**：有。无障碍开关默认为关闭且完全可选，未开启时桌面应用列表、搜索、壁纸、图标排序等功能正常，仅 Home 键拦截失效；内存清理（Kill Stock Launcher Background RAM）与自更新为独立可选项，各自有确认对话框与 Cancel 按钮。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动不弹引导，最佳时点为『监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS』的瞬间（由 MainActivity.showAboutDialog$lambda$21 触发），或等价地监测『MainActivity 上弹出含 SwitchCompat 的 AlertDialog 且随后 800ms 内出现设置页跳转』；亦可在系统无障碍列表项出现 'TV Launcher' 时抓取描述文本。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：全部引导文本均为原生 TextView/Toast/系统描述，可直接 UTG 文本提取。唯一注意点为跳转前存在一次 5 秒静默期与服务侧 30ms 拉回逻辑，UTG 采集时需容忍设置页被短暂切回桌面（这是其声明的 Home 覆盖功能，非规避检测）。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前引导弹窗页（About & Settings 对话框）** | com.tvlauncher.MainActivity 上的 Dialog 窗口，标题 'Settings & About'，含 'Override TV Default Launcher' 开关与 'Intercepts TV Home key on devices that lock the default launcher' 说明、'Close' 按钮 | 该页是唯一决定是否发起无障碍申请的入口，可判定引导是否为用户按需触发、是否提供取消路径、文案与用途是否一致 | 弹窗是否含可点击 Cancel/Close 关闭按钮；开关文案与描述文本是否与无障碍真实用途一致；弹窗出现前是否存在冷启动自动弹出（本应用应无）；同一弹窗是否还并列内存清理/自更新等无关项 |
| **系统无障碍服务列表项** | 系统 Settings 无障碍页，条目名 'TV Launcher'，summary 为 'Allows TV Launcher to detect the Home button on TV remotes and return to this launcher.' | 核对系统侧呈现给用户的服务名与描述是否与代码/资源一致，是否存在标签与描述不符或空白标签掩盖 | 条目 label 是否为 'TV Launcher'；描述是否为上述逐字文本而非空白/换行占位；是否存在同一应用多个无障碍条目（应为 1 个） |
| **返回应用后的拒权反馈页** | 从系统设置返回后的 MainActivity 桌面（无新增 Dialog/Overlay） | 区分良性降级与拒权死循环/遮罩压栈，是诱导类恶意行为的关键判别点 | 是否在 1-3 秒内再次跳转 ACCESSIBILITY_SETTINGS；是否出现新的全屏遮罩或悬浮窗；是否展示催促/恐吓文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.tvlauncher.MainActivity.showAboutDialog$lambda$21`
- `com.tvlauncher.MainActivity.openAccessibilitySettings`
- `com.tvlauncher.MainActivity.showAboutDialog`
- `com.tvlauncher.TvHomeOverrideService.onKeyEvent`
- `com.tvlauncher.TvHomeOverrideService.onAccessibilityEvent`
- `res/xml/accessibility_service_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验完成）

**可见性**：DEX 完全静态可见，无加壳、无密文载荷、无远端 HTML、无 WebView（`classes.dex` 仅 6 个 `com.tvlauncher` 类，全部可读）。

**引导链路（纯运行期页面流转）**
1. 冷启动 [MainActivity](<resource-unit:#1.dex1 code:com.tvlauncher.MainActivity>)（HOME/LEANBACK 入口）**不弹任何无障碍引导**；`onResume` 只做 `loadAppSlots()`、壁纸应用与更新检查。
2. 用户在桌面点击"About & Settings"（`aboutButton`）→ `setupClickListeners$lambda$2` → `showAboutDialog()`，弹出原生 `AlertDialog`（自定义视图 [res/layout/dialog_about.xml](<resource-unit:#1 file:res/layout/dialog_about.xml>)），内含开关 `Override TV Default Launcher` + 说明 "Intercepts TV Home key on devices that lock the default launcher"。
3. 点击卡片 `lambda$20` 切换开关；`SwitchCompat.OnCheckedChangeListener` = `showAboutDialog$lambda$21`：写入 `launcher_settings/home_override_enabled`，若开启且服务未启用 → `Toast(enable_accessibility_prompt)` 后调用 [openAccessibilitySettings()](<resource-unit:#1.dex1 code:com.tvlauncher.MainActivity#openAccessibilitySettings>)。
4. `openAccessibilitySettings()` 先写 `TvHomeOverrideService.c = now + 5000ms`（自身静默期），再按顺序尝试 `android.settings.ACCESSIBILITY_SETTINGS`（两次，带/不带 `FLAG_ACTIVITY_NEW_TASK`）→ 失败降级 `android.settings.SETTINGS`。
5. 系统无障碍列表展示 `android:label` 继承的 "TV Launcher" 与 [accessibility_service_config.xml](<resource-unit:#1 file:res/xml/accessibility_service_config.xml>) 的 `android:description`（透明说明：仅用于识别遥控器 Home 键）。
6. 返回应用后 `onResume` **不重跳、不死循环、不叠遮罩、不伪造系统页**；开关状态下次打开对话框时重算。

**获权后行为**：[TvHomeOverrideService](<resource-unit:#1.dex1 code:com.tvlauncher.TvHomeOverrideService>) 仅做两件事——`onKeyEvent` 拦截 `KEYCODE_HOME` 拉起自身；`onAccessibilityEvent`（TYPE_WINDOW_STATE_CHANGED）在**其它已安装桌面**出现 setting/preference/dialog 类窗口时 30ms 后把本桌面拉回前台。集合 b 只收非自身、非 OEM 预装桌面；不使用 `performGlobalAction`，不自动点击、不自授权、不阻止撤权。

**预筛线索解释**：`JUMP_A11Y_SETTINGS` 即上述开关引导；`WATCH_SETTINGS/WATCH_PKG_INSTALLER` 是 `TvHomeOverrideService.<clinit>` 里 `com.android.settings / com.android.tv.settings / com.google.android.tv.settings / com.amazon.tv.settings / com.android.packageinstaller / com.android.permissioncontroller …` 的窗口监听白名单，非撤权对抗；`RESTRICTED_STR` 来自 AndroidX 的 "The android:onClick attribute cannot be used within a restricted context"，无 13+ 受限设置教学。

**结论**：属用户按需（feature on demand）触发、可取消、文案与用途一致的良性透明引导，未发现诱导或强制行为，未登记风险。

```json
{
  "static_visibility": "clear",
  "visibility_note": "DEX 与全部资源静态可见：classes.dex 中 com.tvlauncher 仅 6 个类，无障碍服务、引导弹窗、跳转 Intent 与全部文案（strings.xml / dialog_about.xml / accessibility_service_config.xml）均可直接还原；无加壳、无 VMP、无 AES 密文、无远端 HTML、无 WebView、无动态加载。",
  "summary_one_liner": "仅在用户于『About & Settings』弹窗内手动打开 Override TV Default Launcher 开关时，先 Toast 说明再跳系统无障碍设置页，说明文案透明、可取消、无拒权循环与遮罩。",
  "disguise_identity": {
    "app_display_name": "TV Launcher",
    "claimed_brand_or_persona": "TV Launcher（F-Droid 开源项目 wiiguy/lightweight_androidtv_launcher，GPL v3.0，界面显示 vX.Y (FOSS)）",
    "a11y_service_label": "TV Launcher（服务未单独设置 android:label，继承 application android:label=@string/app_name）",
    "identity_mismatch": false,
    "obfuscation_tricks": "无。服务描述为直白的真实用途说明；无空白/换行挤出警告、无同形字、无多 activity-alias、未伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.tvlauncher.MainActivity（HOME / LAUNCHER / LEANBACK_LAUNCHER，launchMode=singleTop，landscape）",
      "trigger_event": "onCreate → setContentView(R.layout.activity_main) → setupClickListeners()；onResume → loadAppSlots()、applyWallpaper()、更新检查",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（冷启动不出现任何无障碍引导文案）",
      "shown_text_zh": "无",
      "user_action_requested": "无强制动作，正常浏览桌面应用图标",
      "code_anchor": "com.tvlauncher.MainActivity.onCreate / com.tvlauncher.MainActivity.onResume"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "MainActivity 原生 AlertDialog（自定义视图 res/layout/dialog_about.xml，标题 @string/about_title，关闭按钮 @string/about_close）",
      "trigger_event": "用户点击桌面 aboutButton → setupClickListeners$lambda$2 → showAboutDialog()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Settings & About | Override TV Default Launcher | Intercepts TV Home key on devices that lock the default launcher | Kill Stock Launcher Background RAM | Frees 100MB+ RAM by stopping heavy OEM TV home screens | Close",
      "shown_text_zh": "设置与关于｜覆盖电视默认桌面｜在锁定默认桌面的设备上拦截电视 Home 键｜结束后台预装桌面以释放内存｜通过停止繁重的 OEM 电视桌面释放 100MB+ 内存｜关闭",
      "user_action_requested": "可选：点击开关卡片或拨动 SwitchCompat；存在 Close 取消按钮，可直接退出不做任何授权",
      "code_anchor": "com.tvlauncher.MainActivity.showAboutDialog + res/layout/dialog_about.xml + res/values/strings.xml(about_title/about_close/override_default_launcher/override_default_launcher_desc)"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "Toast + 系统无障碍设置页 android.settings.ACCESSIBILITY_SETTINGS（失败降级 android.settings.SETTINGS）",
      "trigger_event": "用户手动打开 Override TV Default Launcher 开关 → SwitchCompat.OnCheckedChangeListener = showAboutDialog$lambda$21（先写 SharedPreferences launcher_settings/home_override_enabled，再判断服务是否已启用）",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Please enable TV Launcher under Accessibility Services to intercept the Home key.",
      "shown_text_zh": "请在『无障碍服务』中启用 TV Launcher，以便拦截 Home 键。",
      "user_action_requested": "要求用户点击 Toast 后自动跳转到的系统无障碍列表，手动找到并开启 TV Launcher 服务；用户可拒绝、可直接返回",
      "code_anchor": "com.tvlauncher.MainActivity.showAboutDialog$lambda$21 → com.tvlauncher.MainActivity.openAccessibilitySettings"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统『无障碍』服务列表项：TV Launcher，描述取 @string/accessibility_service_description",
      "trigger_event": "openAccessibilitySettings() 先置 TvHomeOverrideService.c = now+5000ms（静默期），再顺序 startActivity：ACCESSIBILITY_SETTINGS、ACCESSIBILITY_SETTINGS(NEW_TASK)、SETTINGS",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Allows TV Launcher to detect the Home button on TV remotes and return to this launcher.",
      "shown_text_zh": "允许 TV Launcher 检测电视遥控器上的 Home 键，并返回到本桌面。",
      "user_action_requested": "用户在系统页面内自行决定是否开启该服务（系统页自带取消/返回）",
      "code_anchor": "res/xml/accessibility_service_config.xml + res/values/strings.xml(accessibility_service_description) + com.tvlauncher.MainActivity.openAccessibilitySettings"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity.onResume（返回应用后）",
      "trigger_event": "从系统设置返回触发 onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（不重跳设置页、不重复弹窗、不显示催促文案）",
      "user_action_requested": "无；用户可长期保持未开启状态，桌面功能照常可用（仅 Home 键拦截失效）",
      "code_anchor": "com.tvlauncher.MainActivity.onResume"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.tvlauncher.TvHomeOverrideService（BIND_ACCESSIBILITY_SERVICE，flagRequestFilterKeyEvents=true，typeWindowStateChanged）",
      "trigger_event": "onKeyEvent(KEYCODE_HOME, ACTION_DOWN) → a() 以 NEW_TASK|CLEAR_TOP|SINGLE_TOP 启动 MainActivity；onAccessibilityEvent(TYPE_WINDOW_STATE_CHANGED) 检测到其它桌面出现 setting/preference/dialog 类窗口后 postDelayed(30ms) 拉回本桌面",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（无自点击、无自授权、不阻止用户在设置页撤权、无 performGlobalAction 模拟返回/Home）",
      "user_action_requested": "无",
      "code_anchor": "com.tvlauncher.TvHomeOverrideService.onKeyEvent / onAccessibilityEvent / onServiceConnected"
    }
  ],
  "text_presentation_locations": [
    "MainActivity 的 AlertDialog（showAboutDialog，自定义视图 res/layout/dialog_about.xml）内的 SwitchCompat 标题与 12sp 说明 TextView：Override TV Default Launcher / Intercepts TV Home key on devices that lock the default launcher",
    "同一弹窗内开关切换后的 Toast：@string/enable_accessibility_prompt（Please enable TV Launcher under Accessibility Services to intercept the Home key.）",
    "系统『无障碍』列表服务条目描述：@string/accessibility_service_description（Allows TV Launcher to detect the Home button on TV remotes and return to this launcher.）",
    "弹窗底部按钮：@string/about_close（Close）与对话框标题 @string/about_title（Settings & About）",
    "关于区文案 @string/about_message：TV Launcher / Version %1$s / Free and open source. / License: GNU GPL v3.0.",
    "无 WebView / 本地 HTML / 远端 HTML / 悬浮窗 Overlay / 半透明引导遮罩 / 仿系统设置页，全部引导文字均承载于原生 Dialog、Toast 与系统无障碍描述"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Allows TV Launcher to detect the Home button on TV remotes and return to this launcher.",
      "text_zh": "允许 TV Launcher 检测电视遥控器上的 Home 键，并返回到本桌面。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibility_service_config.xml android:description 引用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enable TV Launcher under Accessibility Services to intercept the Home key.",
      "text_zh": "请在『无障碍服务』中启用 TV Launcher，以便拦截 Home 键。",
      "source_location": "res/values/strings.xml key=enable_accessibility_prompt（Toast，由 showAboutDialog$lambda$21 触发）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Override TV Default Launcher",
      "text_zh": "覆盖电视默认桌面",
      "source_location": "res/values/strings.xml key=override_default_launcher（dialog_about.xml homeOverrideSwitch）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Intercepts TV Home key on devices that lock the default launcher",
      "text_zh": "在锁定默认桌面的设备上拦截电视 Home 键",
      "source_location": "res/values/strings.xml key=override_default_launcher_desc（dialog_about.xml 说明 TextView）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "This stops background processes of pre-installed TV launchers to free RAM. Launchers you installed yourself are never touched. You can turn it off anytime in About.",
      "text_zh": "此操作会停止预装电视桌面的后台进程以释放内存。你自己安装的桌面永远不会被影响。你可以随时在『关于』中关闭它。",
      "source_location": "res/values/strings.xml key=suppress_stock_ram_confirm（内存清理确认对话框正文）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "TV Launcher\nVersion %1$s\n\nFree and open source.\nLicense: GNU GPL v3.0.\n\n%2$s",
      "text_zh": "TV Launcher\n版本 %1$s\n\n自由且开源。\n许可证：GNU GPL v3.0。\n\n%2$s",
      "source_location": "res/values/strings.xml key=about_message",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Close",
      "text_zh": "关闭",
      "source_location": "res/values/strings.xml key=about_close（对话框取消/关闭按钮）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无循环。拒绝或在系统无障碍页返回后，MainActivity.onResume 仅执行 loadAppSlots()/applyWallpaper()/更新检查，不重跳设置页、不重复弹窗；仅当用户下次打开『About & Settings』并再次拨动开关时才会重新出现 Toast + 跳转。openAccessibilitySettings 另外设置了 5 秒静默期（TvHomeOverrideService.c = now+5000），避免跳转过程中被服务自身打断。",
    "overlay_or_fake_settings": "无。不使用 TYPE_APPLICATION_OVERLAY 或任何悬浮窗权限，不叠加半透明引导遮罩，不绘制高仿系统无障碍开关页；跳转目标为系统真实 ACCESSIBILITY_SETTINGS（失败时降级 SETTINGS/TV_SETTINGS/DEVICE_INFO_SETTINGS）。",
    "restricted_settings_13plus_coaching": "无。全包未见引导用户进入应用详情页右上角菜单开启『允许受限设置』，也无 Session 安装器绕过；相关字符串 update_permission_needed（Allow installs from this app in Settings.）仅指向自身 GitHub 自更新所需的『安装未知应用』授权，与无障碍无关。",
    "post_grant_anti_removal": "无。服务未使用 performGlobalAction、未自动点击确认、未监听无障碍设置页阻止撤权；仅拦截 KEYCODE_HOME 拉起本桌面，以及在其他已安装桌面出现 setting/preference/dialog 窗口时 30ms 后把本桌面拉回前台（其声明用途即 Home 键覆盖）。",
    "benign_graceful_degradation": "有。无障碍开关默认为关闭且完全可选，未开启时桌面应用列表、搜索、壁纸、图标排序等功能正常，仅 Home 键拦截失效；内存清理（Kill Stock Launcher Background RAM）与自更新为独立可选项，各自有确认对话框与 Cancel 按钮。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动不弹引导，最佳时点为『监测到 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS』的瞬间（由 MainActivity.showAboutDialog$lambda$21 触发），或等价地监测『MainActivity 上弹出含 SwitchCompat 的 AlertDialog 且随后 800ms 内出现设置页跳转』；亦可在系统无障碍列表项出现 'TV Launcher' 时抓取描述文本。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前引导弹窗页（About & Settings 对话框）",
        "page_identifier": "com.tvlauncher.MainActivity 上的 Dialog 窗口，标题 'Settings & About'，含 'Override TV Default Launcher' 开关与 'Intercepts TV Home key on devices that lock the default launcher' 说明、'Close' 按钮",
        "why_most_useful": "该页是唯一决定是否发起无障碍申请的入口，可判定引导是否为用户按需触发、是否提供取消路径、文案与用途是否一致",
        "observable_utg_signals": ["弹窗是否含可点击 Cancel/Close 关闭按钮", "开关文案与描述文本是否与无障碍真实用途一致", "弹窗出现前是否存在冷启动自动弹出（本应用应无）", "同一弹窗是否还并列内存清理/自更新等无关项"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页，条目名 'TV Launcher'，summary 为 'Allows TV Launcher to detect the Home button on TV remotes and return to this launcher.'",
        "why_most_useful": "核对系统侧呈现给用户的服务名与描述是否与代码/资源一致，是否存在标签与描述不符或空白标签掩盖",
        "observable_utg_signals": ["条目 label 是否为 'TV Launcher'", "描述是否为上述逐字文本而非空白/换行占位", "是否存在同一应用多个无障碍条目（应为 1 个）"]
      },
      {
        "page_role": "返回应用后的拒权反馈页",
        "page_identifier": "从系统设置返回后的 MainActivity 桌面（无新增 Dialog/Overlay）",
        "why_most_useful": "区分良性降级与拒权死循环/遮罩压栈，是诱导类恶意行为的关键判别点",
        "observable_utg_signals": ["是否在 1-3 秒内再次跳转 ACCESSIBILITY_SETTINGS", "是否出现新的全屏遮罩或悬浮窗", "是否展示催促/恐吓文案"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：全部引导文本均为原生 TextView/Toast/系统描述，可直接 UTG 文本提取。唯一注意点为跳转前存在一次 5 秒静默期与服务侧 30ms 拉回逻辑，UTG 采集时需容忍设置页被短暂切回桌面（这是其声明的 Home 覆盖功能，非规避检测）。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "BENIGN_TRANSPARENT_RATIONALE",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION",
    "BENIGN_HONEST_IDENTITY_AND_SCOPE",
    "BENIGN_ALTERNATIVE_MODE_OFFERED"
  ],
  "code_anchors": [
    "com.tvlauncher.MainActivity.showAboutDialog$lambda$21",
    "com.tvlauncher.MainActivity.openAccessibilitySettings",
    "com.tvlauncher.MainActivity.showAboutDialog",
    "com.tvlauncher.TvHomeOverrideService.onKeyEvent",
    "com.tvlauncher.TvHomeOverrideService.onAccessibilityEvent",
    "res/xml/accessibility_service_config.xml"
  ]
}
```

</details>
