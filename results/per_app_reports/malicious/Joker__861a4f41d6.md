# MR_116__861a4f41d6｜Joker — Smart Computer Style Launcher

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：129.9s

## 1. 一句话核心结论

- **核心申请方式**：以全屏半透明遮罩 + 不可点击假开关 + 指向手势手机构成高仿系统开关引导层，配合系统无障碍列表中以 iTouch 名义作出的“绝不收集个人信息”承诺，推动用户自行前往系统页开启高频监听通知的 MyAccService，真实跳转与获权后动作被爱加密壳隐藏。
- **静态可见性说明**：Manifest、无障碍服务配置、strings 文案、引导层 layout 均完整静态可见；但无障碍跳转逻辑（ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS）与 MyAccService 真实行为被爱加密壳（assets/ijiami.ajm + ijm_lib/libexec.so + Application=s.h.e.l.l.S）剥离，WelcomeGuildActivity.onCreate、MyAccService.onServiceConnected/onAccessibilityEvent/onInterrupt 反编译方法体为空，全包搜索 ACCESSIBILITY_SETTINGS 零命中，故引导页触发时机、拒绝后重跳循环、获权后防撤权动作不可静态还原。assets 下无任何本地或远端 HTML/JS 教学页。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `861a4f41d6680f6021aa24d36d4be36961f134550a748b25bd75ca5db7d2f5e8` |
| 包名 / 年份 | `com.windowspl.launcherwith` / 2021 |
| 家族 / 品类 | **Joker**（同池样本数：4） |
| 原始来源标识 | https://therecord.media/android-malware-found-on-huaweis-official-app-store/ |
| 桌面显示名 | Smart Computer Style Launcher |
| 引导页宣称品牌/身份 | Windows 风格电脑桌面（Smart Computer Style Launcher）；无障碍描述中另行自称 iTouch |
| 系统无障碍列表服务名 | Smart Computer Style Launcher（服务 android:label 引用 @string/app_name；列表描述为 accessibility_service_description） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍描述自称 iTouch 与显示名 Smart Computer Style Launcher 不一致；描述含拼写错误“ike”（应为 like），呈模板复用痕迹；引导层用 android:checked="true" 且 clickable="false" 的 Switch 伪装成“已开启”状态；另声明第二个 HOME 入口 FakeLauncherActivity（clearTaskOnLaunch、excludeFromRecents）但 enabled="false"，当前不可用；未发现伪造 isAccessibilityTool 声明（targetSdk=29，早于该字段）。 |
| 无障碍服务类名 | `com.windowspl.launcherwith.MyAccService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Enable Accessibility Service to perform global actions ike going back, opening notifications taking screen shot. Please be assured that iTouch will not collect any personal information |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.windowspl.launcherwith.SplashScreen（MAIN/LAUNCHER 入口，Theme.AppCompat.Light.NoActionBar） | onCreate（壳化后仅剩壳回调桩 SplashScreen$d.handleMessage / $e.run） | 原生Activity | **原文**：无（activity_splash.xml 仅承载启动视觉，未见引导文案）<br>**译注**：启动页，无文字引导 | 无，自动过渡 | `com.windowspl.launcherwith.SplashScreen.onCreate / res/layout/activity_splash.xml` |
| 2 | 引导说明页 | com.windowspl.launcherwith.WelcomeGuildActivity（@style/NoTitleTranslucentTheme）叠加 layout_guide 遮罩层 | WelcomeGuildActivity.onCreate / a()（方法体被壳剥离，调用时机不可静态确认） | 悬浮窗Overlay | **原文**：For better user experience, please allow the notification permission of app<br>**译注**：为了更好的使用体验，请允许本应用的通知权限。 | 按右侧 pointing_hand 手指指引去开启开关；右上角 ic_close 可关闭遮罩，但文案未说明开关不可直接点击（Switch 为 clickable=false） | `res/layout/activity_welcome_guide.xml:2-15 / strings.xml:147 (find_and_grant) / WelcomeGuildActivity$a.onClick / WelcomeGuildActivity$b.onClick` |
| 3 | 跳受限设置 | 预期为系统无障碍/通知权限设置页；实际 Intent 目标不可静态还原 | 不可静态还原（全包 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 搜索零命中，逻辑在壳内） | 不可静态还原 | 无 | 不可静态还原 | `不可静态还原（壳：assets/ijiami.ajm、assets/ijm_lib/arm64-v8a/libexec.so）` |
| 4 | 跳无障碍设置 | 系统「设置 → 无障碍 → 已下载的服务」列表项：Smart Computer Style Launcher / com.windowspl.launcherwith.MyAccService | 用户在系统列表中点选该服务；配置由 @xml/accessibilityservice 提供 | 系统无障碍页 | **原文**：Enable Accessibility Service to perform global actions ike going back, opening notifications taking screen shot. Please be assured that iTouch will not collect any personal information<br>**译注**：启用无障碍服务以执行返回、打开通知、截屏等全局操作。请放心，iTouch 不会收集任何个人信息。 | 在系统无障碍页手动打开该服务开关；系统原生页含返回/取消能力 | `res/xml/accessibilityservice.xml:2 / strings.xml:30 (accessibility_service_description)` |
| 5 | 获权后动作 | com.windowspl.launcherwith.MyAccService（typeNotificationStateChanged，notificationTimeout=100） | onServiceConnected / onAccessibilityEvent（方法体被壳剥离） | 不可静态还原 | 无 | 不可静态还原 | `com.windowspl.launcherwith.MyAccService.onServiceConnected / onAccessibilityEvent / res/xml/accessibilityservice.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/layout/activity_welcome_guide.xml 全屏半透明遮罩（background=#66000000）顶部蓝色标题条：ic_warning 图标 + strings.xml:147 find_and_grant 文案（WelcomeGuildActivity 承载）
- res/layout/activity_welcome_guide.xml 白色横条：应用图标 + @string/app_name（Smart Computer Style Launcher）+ 伪装为已开启的 Switch（checked=true, clickable=false）+ pointing_hand 指向手势图标
- 系统无障碍服务列表项描述：res/xml/accessibilityservice.xml 的 android:description → strings.xml:30 accessibility_service_description（含 iTouch 隐私承诺）
- 未发现：本地 HTML/JS 教学页（assets 下无 html/js）、远端 WebView 引导页、跳转设置后的二次压栈遮罩（均无静态证据）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable Accessibility Service to perform global actions ike going back, opening notifications taking screen shot. Please be assured that iTouch will not collect any personal information | 启用无障碍服务以执行返回、打开通知、截屏等全局操作。请放心，iTouch 不会收集任何个人信息。 | `res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibilityservice.xml 引用为 android:description）` | 隐私承诺 |
| en | For better user experience, please allow the notification permission of app | 为了更好的使用体验，请允许本应用的通知权限。 | `res/values/strings.xml key=find_and_grant（activity_welcome_guide.xml 的 @id/tv_content）` | 受限设置分步教学 |
| en | Smart Computer Style Launcher | 智能电脑风格桌面 | `res/values/strings.xml key=app_name / app_name_prime（同时用作 application、activity 与无障碍 service 的 android:label）` | 良性透明说明 |
| en | By Date Installed | 按安装日期排序 | `res/values/strings.xml（桌面应用抽屉排序选项）` | 良性透明说明 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 需要启用 Google Play 服务后才能正常工作。 | `res/values/strings.xml key=common_google_play_services_enable_text（Google Play services 标准库资源，非应用自写）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：不可静态还原：WelcomeGuildActivity 与 MyAccService 方法体被爱加密壳剥离，未见 onResume/Timer 重跳代码；遮罩层右上角存在 ic_close，静态结构上允许关闭
- **遮罩叠层 / 高仿系统设置页**：是：activity_welcome_guide.xml 为全屏半透明遮罩（#66000000），内含 checked=true 且 clickable=false 的假开关与 pointing_hand 指向手势，构成高仿系统开关的视觉引导；未见跳转设置后二次压栈遮罩的静态证据
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=29，低于 Android 13 受限设置机制；strings 与代码中未见“应用详情 → 右上角菜单 → 允许受限设置”或 Session 安装器相关文案）
- **获权后即时行为与防撤权机制**：不可静态还原：MyAccService.onServiceConnected 为空方法体，预筛线索中的 PERFORM_GLOBAL_ACTION / WATCH_SETTINGS 位于壳内 DEX，无法静态确认是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动 SplashScreen 之后、WelcomeGuildActivity 首次 onResume 拉起 layout_guide 遮罩的瞬间截图（此时半透明遮罩 + 假开关 + 指向手势同屏）；同时监听 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的跳转，跳转落地后立即再截一帧
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：无障碍跳转与获权后行为全部位于爱加密壳内（assets/ijiami.ajm + ijm_lib/libexec.so），静态无法还原；但静态加壳不阻挡运行期 UTG 观测，遮罩页与系统无障碍列表页仍可正常抓取。另需注意引导层文案实际指向“通知权限”，与无障碍服务并非同一授权项，UTG 判定时应以实际跳转目标为准而非仅凭文案。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导遮罩页** | WelcomeGuildActivity（NoTitleTranslucentTheme）上覆盖 layout_guide：底部蓝色条含 ic_warning + 文案，白色条含应用名与 checked 状态的 Switch + pointing_hand | 该页是应用自绘的授权引导载体，其假开关与指向手势是区分“透明说明”与“视觉诱导”的决定性画面 | 半透明遮罩上层叠不可点击的 Switch 控件（控件可点击性为 false）；同一屏内出现指向手势图标与开关控件的相对位置关系；遮罩文案是否只提“通知权限”而未提无障碍服务 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务 → Smart Computer Style Launcher / MyAccService | 核对系统实际展示的服务名与描述文案，确认 iTouch 身份不一致与隐私承诺原文是否原样呈现 | 服务条目显示的 label 与 description 原文；description 中是否出现 iTouch 及“不会收集任何个人信息”承诺 |
| **跳转落地后的系统页（若存在）** | android.settings.ACCESSIBILITY_SETTINGS 或应用详情页 | 验证是否存在设置页之上的二次压栈遮罩或自动滚动定位，用于区分“仅引导”与“遮罩指引式强推” | 系统设置页之上是否叠加应用自绘 View；页面是否被自动滚动/高亮到特定服务项 |
| **关闭遮罩或返回后的反馈页** | 点 ic_close 或从系统设置返回后的 WelcomeGuildActivity / MainActivity | 判断是否存在拒绝循环重跳（对应不可静态还原的 onResume 逻辑） | 返回后是否在数秒内再次弹出同一遮罩；是否反复跳转系统设置页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.windowspl.launcherwith.WelcomeGuildActivity.onCreate`
- `com.windowspl.launcherwith.WelcomeGuildActivity$a.onClick`
- `com.windowspl.launcherwith.MyAccService.onAccessibilityEvent`
- `res/xml/accessibilityservice.xml`
- `res/layout/activity_welcome_guide.xml`
- `res/values/strings.xml（accessibility_service_description / find_and_grant）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**1. 无障碍服务的静态可见部分（已核实）**
- `AndroidManifest.xml` 注册了 `com.windowspl.launcherwith.MyAccService`（`BIND_ACCESSIBILITY_SERVICE`），meta-data 指向 [res/xml/accessibilityservice.xml](<resource-unit:#1 file:res/xml/accessibilityservice.xml>)：`accessibilityEventTypes="typeNotificationStateChanged"`、`notificationTimeout="100"`、`feedbackAllMask`——即**以 100ms 高频监听通知栏变化**，而非"返回/截屏"这类全局动作。
- 系统无障碍列表展示的 `android:description` 为 [strings.xml#L30](<resource-unit:#1 file:res/values/strings.xml#L30>)：承诺"只用于返回、打开通知、截屏"，并声明"iTouch 不会收集任何个人信息"。文案中自称 **iTouch**，与桌面显示名 [Smart Computer Style Launcher](<resource-unit:#1 file:res/values/strings.xml#L46>) 不一致，且存在拼写错误 `ike`（漏 `l`），说明该描述由其他产品复用或刻意模糊主体。

**2. 引导层形态（已核实，为遮罩式假开关页）**
[activity_welcome_guide.xml#L2-L15](<resource-unit:#1 file:res/layout/activity_welcome_guide.xml#L2-L15>) 是**全屏半透明遮罩**（`background="#66000000"`、`fill_parent`）：
- 顶部蓝色标题条 + `ic_warning` 警告图标 + 文案 [strings.xml#L147](<resource-unit:#1 file:res/values/strings.xml#L147>) `For better user experience, please allow the notification permission of app`（"为更好体验，请允许应用的**通知权限**"）；
- 中部为应用图标 + 应用名 + 一个 `android:checked="true"` 且 `clickable="false"` 的**不可点击假开关**，旁边叠加 `pointing_hand` 手指图标指向该开关；
- 右上角有 `ic_close`，即该遮罩层本身**可关闭**。

这是典型的"高仿系统开关 + 指向手势 + 遮罩压栈"引导范式：用户看到的"开关"只是图片级视觉，真实操作需自行去系统设置页完成。

**3. 不可静态还原的部分（壳化）**
- 包为**爱加密**加固：`assets/ijiami.ajm`（`indl01` 头）、`assets/ijm_lib/{arm64-v8a,armeabi,x86,x86_64}/libexec.so`、`Application = s.h.e.l.l.S`、`appComponentFactory = s.h.e.l.l.A`。
- 反编译 `WelcomeGuildActivity.onCreate/a`、`MyAccService.onServiceConnected/onAccessibilityEvent/onInterrupt` **方法体全为空**（壳剥离），`SplashScreen` 只剩壳的回调桩。
- 全包 `search_function_callsites` 对 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`isAccessibilityServiceEnabled` **零命中**——`ACTION_ACCESSIBILITY_SETTINGS` 跳转点、拒绝后 `onResume` 死循环重跳、获权后 `GLOBAL_ACTION_BACK` 防撤权等**运行期 UTG 跳转逻辑均不可静态还原**。
- `assets/` 下无任何 HTML/JS，跳转不依赖本地或远端 WebView 教学页；`FakeLauncherActivity`（第二个 HOME 入口）虽声明但 `enabled="false"`，运行期不可用，不能作为变脸证据。

**4. 判定**
已确认的是"无障碍服务声明 + 通知高频监听配置 + 隐私承诺式描述 + 遮罩假开关引导层"这一组合；"引导层文字指向的是通知权限而非无障碍"，且无障碍跳转代码被壳隐藏，因此**不能**断言存在强制跳转、不可取消弹窗或拒绝循环。已按此证据边界登记 R-001（medium / malware_trojan）。

---

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍服务配置、strings 文案、引导层 layout 均完整静态可见；但无障碍跳转逻辑（ACTION_ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS）与 MyAccService 真实行为被爱加密壳（assets/ijiami.ajm + ijm_lib/libexec.so + Application=s.h.e.l.l.S）剥离，WelcomeGuildActivity.onCreate、MyAccService.onServiceConnected/onAccessibilityEvent/onInterrupt 反编译方法体为空，全包搜索 ACCESSIBILITY_SETTINGS 零命中，故引导页触发时机、拒绝后重跳循环、获权后防撤权动作不可静态还原。assets 下无任何本地或远端 HTML/JS 教学页。",
  "summary_one_liner": "以全屏半透明遮罩 + 不可点击假开关 + 指向手势手机构成高仿系统开关引导层，配合系统无障碍列表中以 iTouch 名义作出的“绝不收集个人信息”承诺，推动用户自行前往系统页开启高频监听通知的 MyAccService，真实跳转与获权后动作被爱加密壳隐藏。",
  "disguise_identity": {
    "app_display_name": "Smart Computer Style Launcher",
    "claimed_brand_or_persona": "Windows 风格电脑桌面（Smart Computer Style Launcher）；无障碍描述中另行自称 iTouch",
    "a11y_service_label": "Smart Computer Style Launcher（服务 android:label 引用 @string/app_name；列表描述为 accessibility_service_description）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍描述自称 iTouch 与显示名 Smart Computer Style Launcher 不一致；描述含拼写错误“ike”（应为 like），呈模板复用痕迹；引导层用 android:checked=\"true\" 且 clickable=\"false\" 的 Switch 伪装成“已开启”状态；另声明第二个 HOME 入口 FakeLauncherActivity（clearTaskOnLaunch、excludeFromRecents）但 enabled=\"false\"，当前不可用；未发现伪造 isAccessibilityTool 声明（targetSdk=29，早于该字段）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.windowspl.launcherwith.SplashScreen（MAIN/LAUNCHER 入口，Theme.AppCompat.Light.NoActionBar）",
      "trigger_event": "onCreate（壳化后仅剩壳回调桩 SplashScreen$d.handleMessage / $e.run）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（activity_splash.xml 仅承载启动视觉，未见引导文案）",
      "shown_text_zh": "启动页，无文字引导",
      "user_action_requested": "无，自动过渡",
      "code_anchor": "com.windowspl.launcherwith.SplashScreen.onCreate / res/layout/activity_splash.xml"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.windowspl.launcherwith.WelcomeGuildActivity（@style/NoTitleTranslucentTheme）叠加 layout_guide 遮罩层",
      "trigger_event": "WelcomeGuildActivity.onCreate / a()（方法体被壳剥离，调用时机不可静态确认）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "For better user experience, please allow the notification permission of app",
      "shown_text_zh": "为了更好的使用体验，请允许本应用的通知权限。",
      "user_action_requested": "按右侧 pointing_hand 手指指引去开启开关；右上角 ic_close 可关闭遮罩，但文案未说明开关不可直接点击（Switch 为 clickable=false）",
      "code_anchor": "res/layout/activity_welcome_guide.xml:2-15 / strings.xml:147 (find_and_grant) / WelcomeGuildActivity$a.onClick / WelcomeGuildActivity$b.onClick"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "预期为系统无障碍/通知权限设置页；实际 Intent 目标不可静态还原",
      "trigger_event": "不可静态还原（全包 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 搜索零命中，逻辑在壳内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无",
      "user_action_requested": "不可静态还原",
      "code_anchor": "不可静态还原（壳：assets/ijiami.ajm、assets/ijm_lib/arm64-v8a/libexec.so）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统「设置 → 无障碍 → 已下载的服务」列表项：Smart Computer Style Launcher / com.windowspl.launcherwith.MyAccService",
      "trigger_event": "用户在系统列表中点选该服务；配置由 @xml/accessibilityservice 提供",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Enable Accessibility Service to perform global actions ike going back, opening notifications taking screen shot. Please be assured that iTouch will not collect any personal information",
      "shown_text_zh": "启用无障碍服务以执行返回、打开通知、截屏等全局操作。请放心，iTouch 不会收集任何个人信息。",
      "user_action_requested": "在系统无障碍页手动打开该服务开关；系统原生页含返回/取消能力",
      "code_anchor": "res/xml/accessibilityservice.xml:2 / strings.xml:30 (accessibility_service_description)"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.windowspl.launcherwith.MyAccService（typeNotificationStateChanged，notificationTimeout=100）",
      "trigger_event": "onServiceConnected / onAccessibilityEvent（方法体被壳剥离）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无",
      "user_action_requested": "不可静态还原",
      "code_anchor": "com.windowspl.launcherwith.MyAccService.onServiceConnected / onAccessibilityEvent / res/xml/accessibilityservice.xml"
    }
  ],
  "text_presentation_locations": [
    "res/layout/activity_welcome_guide.xml 全屏半透明遮罩（background=#66000000）顶部蓝色标题条：ic_warning 图标 + strings.xml:147 find_and_grant 文案（WelcomeGuildActivity 承载）",
    "res/layout/activity_welcome_guide.xml 白色横条：应用图标 + @string/app_name（Smart Computer Style Launcher）+ 伪装为已开启的 Switch（checked=true, clickable=false）+ pointing_hand 指向手势图标",
    "系统无障碍服务列表项描述：res/xml/accessibilityservice.xml 的 android:description → strings.xml:30 accessibility_service_description（含 iTouch 隐私承诺）",
    "未发现：本地 HTML/JS 教学页（assets 下无 html/js）、远端 WebView 引导页、跳转设置后的二次压栈遮罩（均无静态证据）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable Accessibility Service to perform global actions ike going back, opening notifications taking screen shot. Please be assured that iTouch will not collect any personal information",
      "text_zh": "启用无障碍服务以执行返回、打开通知、截屏等全局操作。请放心，iTouch 不会收集任何个人信息。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（被 res/xml/accessibilityservice.xml 引用为 android:description）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "For better user experience, please allow the notification permission of app",
      "text_zh": "为了更好的使用体验，请允许本应用的通知权限。",
      "source_location": "res/values/strings.xml key=find_and_grant（activity_welcome_guide.xml 的 @id/tv_content）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Smart Computer Style Launcher",
      "text_zh": "智能电脑风格桌面",
      "source_location": "res/values/strings.xml key=app_name / app_name_prime（同时用作 application、activity 与无障碍 service 的 android:label）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "By Date Installed",
      "text_zh": "按安装日期排序",
      "source_location": "res/values/strings.xml（桌面应用抽屉排序选项）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 需要启用 Google Play 服务后才能正常工作。",
      "source_location": "res/values/strings.xml key=common_google_play_services_enable_text（Google Play services 标准库资源，非应用自写）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "不可静态还原：WelcomeGuildActivity 与 MyAccService 方法体被爱加密壳剥离，未见 onResume/Timer 重跳代码；遮罩层右上角存在 ic_close，静态结构上允许关闭",
    "overlay_or_fake_settings": "是：activity_welcome_guide.xml 为全屏半透明遮罩（#66000000），内含 checked=true 且 clickable=false 的假开关与 pointing_hand 指向手势，构成高仿系统开关的视觉引导；未见跳转设置后二次压栈遮罩的静态证据",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=29，低于 Android 13 受限设置机制；strings 与代码中未见“应用详情 → 右上角菜单 → 允许受限设置”或 Session 安装器相关文案）",
    "post_grant_anti_removal": "不可静态还原：MyAccService.onServiceConnected 为空方法体，预筛线索中的 PERFORM_GLOBAL_ACTION / WATCH_SETTINGS 位于壳内 DEX，无法静态确认是否用 GLOBAL_ACTION_BACK/HOME 阻止撤权",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动 SplashScreen 之后、WelcomeGuildActivity 首次 onResume 拉起 layout_guide 遮罩的瞬间截图（此时半透明遮罩 + 假开关 + 指向手势同屏）；同时监听 Intent 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的跳转，跳转落地后立即再截一帧",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导遮罩页",
        "page_identifier": "WelcomeGuildActivity（NoTitleTranslucentTheme）上覆盖 layout_guide：底部蓝色条含 ic_warning + 文案，白色条含应用名与 checked 状态的 Switch + pointing_hand",
        "why_most_useful": "该页是应用自绘的授权引导载体，其假开关与指向手势是区分“透明说明”与“视觉诱导”的决定性画面",
        "observable_utg_signals": ["半透明遮罩上层叠不可点击的 Switch 控件（控件可点击性为 false）", "同一屏内出现指向手势图标与开关控件的相对位置关系", "遮罩文案是否只提“通知权限”而未提无障碍服务"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务 → Smart Computer Style Launcher / MyAccService",
        "why_most_useful": "核对系统实际展示的服务名与描述文案，确认 iTouch 身份不一致与隐私承诺原文是否原样呈现",
        "observable_utg_signals": ["服务条目显示的 label 与 description 原文", "description 中是否出现 iTouch 及“不会收集任何个人信息”承诺"]
      },
      {
        "page_role": "跳转落地后的系统页（若存在）",
        "page_identifier": "android.settings.ACCESSIBILITY_SETTINGS 或应用详情页",
        "why_most_useful": "验证是否存在设置页之上的二次压栈遮罩或自动滚动定位，用于区分“仅引导”与“遮罩指引式强推”",
        "observable_utg_signals": ["系统设置页之上是否叠加应用自绘 View", "页面是否被自动滚动/高亮到特定服务项"]
      },
      {
        "page_role": "关闭遮罩或返回后的反馈页",
        "page_identifier": "点 ic_close 或从系统设置返回后的 WelcomeGuildActivity / MainActivity",
        "why_most_useful": "判断是否存在拒绝循环重跳（对应不可静态还原的 onResume 逻辑）",
        "observable_utg_signals": ["返回后是否在数秒内再次弹出同一遮罩", "是否反复跳转系统设置页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：无障碍跳转与获权后行为全部位于爱加密壳内（assets/ijiami.ajm + ijm_lib/libexec.so），静态无法还原；但静态加壳不阻挡运行期 UTG 观测，遮罩页与系统无障碍列表页仍可正常抓取。另需注意引导层文案实际指向“通知权限”，与无障碍服务并非同一授权项，UTG 判定时应以实际跳转目标为准而非仅凭文案。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.windowspl.launcherwith.WelcomeGuildActivity.onCreate",
    "com.windowspl.launcherwith.WelcomeGuildActivity$a.onClick",
    "com.windowspl.launcherwith.MyAccService.onAccessibilityEvent",
    "res/xml/accessibilityservice.xml",
    "res/layout/activity_welcome_guide.xml",
    "res/values/strings.xml（accessibility_service_description / find_and_grant）"
  ]
}
```

</details>
