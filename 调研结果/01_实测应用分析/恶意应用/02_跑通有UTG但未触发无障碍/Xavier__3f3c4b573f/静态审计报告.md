# MR_160__3f3c4b573f｜Xavier — Battery Saver

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：141.7s

## 1. 一句话核心结论

- **核心申请方式**：省电工具在用户点击 Power Boost 时跳转系统无障碍设置，并在 170ms 后向系统设置页之上叠一张全屏半透明“两步开启教程”遮罩窗，引导用户为监听 com.android.settings 的无障碍服务授权。
- **静态可见性说明**：引导链全部在 classes.dex 中静态可见：ForceActivity#powerBoost/i/j/k、li#a/b、PowerBoostService#onServiceConnected 与 res/xml/power_optimize_config.xml、res/layout/view_window_setting.xml、strings.xml 均未加密，未发现加壳或远端下发 HTML；引导文字全为本地资源。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3f3c4b573f77390cbd852f2b86450979d7d23fcfea43f8836e1b8b194abc5f6d` |
| 包名 / 年份 | `com.coramobile.powerbattery.batterysaver` / 2017 |
| 家族 / 品类 | **Xavier**（同池样本数：41） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/f/analyzing-xavier-information-stealing-ad-library-android.html |
| 桌面显示名 | Battery Saver |
| 引导页宣称品牌/身份 | Battery Saver（省电/后台清理工具，宣称“杀后台应用省电”） |
| 系统无障碍列表服务名 | Battery Saver（服务未声明 android:label，系统列表回退显示应用名），说明文字为 power_description 全文 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无空白挤出/同形字/多 alias/伪造 isAccessibilityTool；隐瞒点在能力范围：无障碍配置限定 packageNames=com.android.settings 且 canRetrieveWindowContent=true（实际用于读取设置界面），对外仅描述为“杀后台省电”，未披露该监听范围。 |
| 无障碍服务类名 | `com.coramobile.powerbattery.batterysaver.force.PowerBoostService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.android.settings |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.coramobile.powerbattery.batterysaver.force.ForceActivity（Power Boost 页，含后台应用列表、复选框与 power_boost_button） | 用户点击 power_boost_button → OnClick powerBoost(View)；页面亦可由 PowerBoostService#onServiceConnected、ni#onClick、ci#onAnimationEnd 拉起 | 原生Activity | **原文**：Power Boost（工具栏 power_boost_toolbar_title1/2）；power_boost_write_system_settings_dialog_message: "In Android 6.0 or above, you must permit %1$s to access system modification so that you can use this function."<br>**译注**：“Power Boost”功能页；Android 6.0 以上需授予修改系统设置权限才能使用该功能 | 点击底部 Power Boost 按钮开始清理/加速（有返回箭头可退出，非强制） | `com.coramobile.powerbattery.batterysaver.force.ForceActivity#powerBoost / onCreate / f` |
| 2 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表） | powerBoost → i()：li.a(context) 读取 Settings.Secure enabled_accessibility_services 判定未授权，则 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS")) | 系统无障碍页 | **原文**：无（应用侧不绘制，交由系统页显示）<br>**译注**：系统无障碍设置列表，用户需在其中找到 Battery Saver 并打开开关 | 在系统列表中手动开启 Battery Saver 的无障碍开关 | `com.coramobile.powerbattery.batterysaver.force.ForceActivity#i + li#a(Context)` |
| 3 | 遮罩叠层指引 | 全屏悬浮遮罩窗（LayoutInflater.inflate(0x7f04008e)=res/layout/view_window_setting.xml，经 getWindowManager().addView 叠加于系统无障碍页之上） | i() 中 new Handler().postDelayed(new gv(this), 170L) → gv#run → ForceActivity#j()，WindowManager.LayoutParams type=2032/2002、flags\|=8、width/height=-1、background=@color/mask_bg | 悬浮窗Overlay | **原文**：Tips / Follow below 2 steps to enable Force Stop feature: / Step 1. Scroll to find “Battery Saver” / Battery Saver / Off / Step 2. Tap “Battery Saver”and turn the switch on / Battery Saver / On / Got it<br>**译注**：“提示”——按以下两步开启强制停止功能：第 1 步，滚动找到“Battery Saver”（当前显示 关）；第 2 步，点按“Battery Saver”并打开开关（打开后显示 开）；按钮“知道了” | 照图文在系统页滚动查找并打开 Battery Saver 开关；可点 “Got it” 关闭遮罩（也可等自动消失） | `com.coramobile.powerbattery.batterysaver.force.ForceActivity#j + gv#run + res/layout/view_window_setting.xml + strings window_title/window_info/window_step1/window_step2/window_get` |
| 4 | 拒权反馈循环 | 遮罩自动消退后回到 ForceActivity（仍在 Power Boost 页） | this.e.postDelayed(new gw(this), ToolTipPopup.DEFAULT_POPUP_DISPLAY_TIME) 定时 removeView；或 gx#onClick（Got it）立即 removeView | 原生Activity | 无 | 无强制动作；用户可放弃，或再次点击 Power Boost 按钮重新进入引导 | `gw#run / gx#onClick / ForceActivity#j` |
| 5 | 跳受限设置 | 系统设置 android.settings.action.MANAGE_WRITE_SETTINGS（修改系统设置授权页） | i() 中无障碍已开启但 li.b(context)=Settings.System.canWrite 为 false 时：k() 先叠同一全屏遮罩（this.f，gz#onClick/gy#run 关闭），随后 startActivity(li.a()) | 悬浮窗Overlay | **原文**：2. Tap and Click switch to permit Write System Settings.（power_optimize_write_settings_overlay_line2）<br>**译注**：第 2 步：点按开关以允许写入系统设置 | 在系统页打开“允许修改系统设置”开关 | `com.coramobile.powerbattery.batterysaver.force.ForceActivity#i / #k + li#a()` |
| 6 | 获权后动作 | PowerBoostService（无障碍服务）onServiceConnected → 再次拉起 ForceActivity | 系统绑定无障碍服务后 onServiceConnected 内 new Intent(this, ForceActivity.class) 启动界面；回到 ForceActivity 后 powerBoost 再次点击时 i() 返回 true，执行 hl.a().a(c.b()) 并进入 ForceCleanActivity | 原生Activity | **原文**：power_description: "Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access."<br>**译注**：“Battery Saver 会关闭后台运行的应用以进一步省电。要启用此功能，请允许 Battery Saver 使用无障碍服务，打开开关以授予访问权限。” | 无需额外操作，获权后直接执行批量杀进程（ForceCleanActivity 展示清理结果） | `com.coramobile.powerbattery.batterysaver.force.PowerBoostService#onServiceConnected + res/xml/power_optimize_config.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项说明文字：android:description=@string/power_description（res/xml/power_optimize_config.xml 引用），服务未设 android:label，列表名回退为应用名 Battery Saver
- 系统设置页之上的全屏半透明遮罩窗：res/layout/view_window_setting.xml（Tips / 两步图文 / Got it），由 ForceActivity#j 通过 WindowManager.addView 叠加
- ForceActivity 页面内：power_dialog_message / power_optimize_accessibility_overlay_line1-2 等字符串资源已随包存在，作为跳转前后的提示文案储备（部分由 %1$s 填充应用名）
- ForceActivity 工具栏标题 power_boost_toolbar_title1/2（"Power" / " Boost"）与 checkbox 说明
- 应用内 policy.html / license.html WebView：仅承载隐私政策与开源许可，与无障碍引导无关

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access. | Battery Saver 会关闭后台运行的应用以进一步省电。要启用此功能，请允许 Battery Saver 使用无障碍服务，打开开关以授予访问权限。 | `res/values/strings.xml: power_description（供 res/xml/power_optimize_config.xml 的 android:description 使用）` | 良性透明说明 |
| en | Tips | 提示 | `res/values/strings.xml: window_title（view_window_setting.xml tv_title）` | 受限设置分步教学 |
| en | Follow below 2 steps to enable Force Stop feature: | 按以下两步开启“强制停止”功能： | `res/values/strings.xml: window_info（view_window_setting.xml tv_info）` | 受限设置分步教学 |
| en | Step 1. Scroll to find “Battery Saver” | 第 1 步：滚动查找“Battery Saver” | `res/values/strings.xml: window_step1（view_window_setting.xml tv_step_1）` | 受限设置分步教学 |
| en | Step 2. Tap “Battery Saver”and turn the switch on | 第 2 步：点按“Battery Saver”并打开开关 | `res/values/strings.xml: window_step2（view_window_setting.xml tv_step_2）` | 受限设置分步教学 |
| en | Got it | 知道了 | `res/values/strings.xml: window_get（view_window_setting.xml tv_get，gx#onClick 关闭遮罩）` | 受限设置分步教学 |
| en | To enable Power Boost, please permit %1$s to use Accessibility Service | 要启用 Power Boost，请允许 %1$s 使用无障碍服务 | `res/values/strings.xml: power_dialog_message` | 受限设置分步教学 |
| en | 1. Scroll and Find %1$s | 1. 滚动并找到 %1$s | `res/values/strings.xml: power_optimize_accessibility_overlay_line1` | 受限设置分步教学 |
| en | 2. Tap and Click switch to permit Accessibility setting. | 2. 点按开关以允许无障碍设置。 | `res/values/strings.xml: power_optimize_accessibility_overlay_line2` | 受限设置分步教学 |
| en | 2. Tap and Click switch to permit Write System Settings. | 2. 点按开关以允许写入系统设置。 | `res/values/strings.xml: power_optimize_write_settings_overlay_line2` | 受限设置分步教学 |
| en | In Android 6.0 or above, you must permit %1$s to access system modification so that you can use this function. | 在 Android 6.0 及以上，你必须允许 %1$s 修改系统，才能使用该功能。 | `res/values/strings.xml: power_boost_write_system_settings_dialog_message` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：无死循环：遮罩由 postDelayed(gw, DEFAULT_POPUP_DISPLAY_TIME) 自动 removeView，或点 Got it 立即关闭；用户返回 ForceActivity 后不自动重跳，需再次点击 Power Boost 才会重走 i() 引导；onResume 仅触发 ht 异步任务刷新进程列表，不含跳转
- **遮罩叠层 / 高仿系统设置页**：有全屏半透明遮罩（type 2002/2032，flags|=8 不可聚焦，width/height=-1，背景 @color/mask_bg），叠加在真实系统无障碍设置页与 MANAGE_WRITE_SETTINGS 页之上，内容是自绘两步教程卡片，非高仿系统开关页
- **Android 13+ 受限设置（Restricted Settings）应对**：无；targetSdkVersion=20，未涉及 Android 13 应用详情“允许受限设置”教学，也未发现 SESSION_INSTALLER 绕过代码
- **获权后即时行为与防撤权机制**：未见自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但无障碍配置限定 packageNames=com.android.settings 且 canRetrieveWindowContent=true、typeWindowStateChanged，服务具备读取设置界面的监听能力（能力可疑，未验证具体拦截行为）
- **良性降级 / 替代方案**：有弱降级：用户可以关闭遮罩后继续留在 Power Boost 页并退出，功能不可用但不阻断其他页面；不存在手动模式或 ADB 替代说明

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 后延迟约 170–500ms 再抓取（遮罩 170ms 才压栈），或监测到 ForceActivity 上点击 power_boost_button 的瞬间开始连续截图
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：遮罩为 WindowManager 添加的 2002/2032 悬浮窗且 flags|=8 不可聚焦，部分 UTG 实现可能不将其纳入当前 Activity 层级而漏采，需以全屏截图 + 悬浮窗节点双通道采集；应用未加壳，静态引导链完整可见，无远端 HTML 或一阶段 Dropper 造成的盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍设置页后压栈的全屏引导遮罩页** | 系统 Settings 无障碍列表之上出现全屏半透明遮罩 + 白底卡片，标题 Tips、含“Step 1/Step 2”“Got it” | 这是应用唯一实际呈现引导文案的载体，可证明其在真实设置页之上叠加自绘教程、并指出具体目标项名 | 节点文本 Tips / Follow below 2 steps to enable Force Stop feature:；节点文本 Step 1. Scroll to find “Battery Saver” 与 Step 2. Tap “Battery Saver”and turn the switch on；节点文本 Got it 可点击控件；遮罩层与底层系统无障碍列表同屏共存 |
| **系统无障碍服务列表项** | Settings → Accessibility 中名为 Battery Saver 的服务项及其说明文字 | 核对系统侧展示的服务名与 description 是否与包内文案一致，判断是否存在身份/范围隐瞒 | 服务项名称 Battery Saver；说明文本以 Battery Saver kills background running apps 开头；开关状态 Off/On 变化 |
| **触发引导的 Power Boost 业务页** | ForceActivity：工具栏“Power Boost”、后台应用列表、power_boost_button | 确定引导的触发时机为按需点击而非冷启动强制，并记录点击前后的界面差异 | power_boost_button 可点击文本；进程列表项与复选框 cb_app_selected；点击后界面是否立即消失并跳系统设置 |
| **WRITE_SETTINGS 授权页与同款遮罩** | Settings → 修改系统设置（MANAGE_WRITE_SETTINGS）页面 + 同一遮罩布局 | 证明存在无障碍→写系统设置的第二段受限权限教学 | 系统页标题含“修改系统设置”；遮罩文本 2. Tap and Click switch to permit Write System Settings. |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.coramobile.powerbattery.batterysaver.force.ForceActivity#powerBoost`
- `com.coramobile.powerbattery.batterysaver.force.ForceActivity#i`
- `com.coramobile.powerbattery.batterysaver.force.ForceActivity#j`
- `com.coramobile.powerbattery.batterysaver.force.PowerBoostService#onServiceConnected`
- `res/xml/power_optimize_config.xml`
- `res/layout/view_window_setting.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**入口与触发**：无障碍引导只在**用户点击 Power Boost 按钮**时触发（按需触发），并不在冷启动时强制弹出。ForceActivity 可由 `PowerBoostService#onServiceConnected`（服务刚被授权后）、广告位 `ni#onClick`、动画结束回调 `ci#onAnimationEnd` 拉起。

**跳转与遮罩的时序（关键）**：`ForceActivity#powerBoost` → `i()` 先判断是否已授权；未授权则 `startActivity(ACTION_ACCESSIBILITY_SETTINGS)`，随后 `Handler.postDelayed(gv, 170ms)` → `j()` 用 `WindowManager` 叠一张**全屏半透明遮罩窗**（type 2002/2032，`flags|=8` 不可聚焦、宽高 -1、背景 `@color/mask_bg`），内容就是 `view_window_setting.xml` 的两步图文教程。因为它在 170ms 后才压栈，所以会在系统无障碍设置页之上形成“教程遮罩”，这正是 UTG 抓取的最佳时机。

**文字载体**：原生 Activity + 原生全屏 Overlay 遮罩 + 系统无障碍列表 description（`@string/power_description`）。全程**无 WebView、无远端 HTML**，`assets/*.html` 只用于 license/policy 页面。

**拒绝/返回后的行为**：没有循环强制重跳；遮罩在 `ToolTipPopup.DEFAULT_POPUP_DISPLAY_TIME` 后自动 `removeView`，也可点 “Got it” 关闭（`gx#onClick`）。用户返回 ForceActivity 后需再次点按钮才会重试。属于**有跳过、非死循环**的一步式引导。

**权限范围隐瞒点**：无障碍配置 `packageNames="com.android.settings"` + `canRetrieveWindowContent="true"` + `typeWindowStateChanged`，即服务被限定为**监听系统设置界面**（与预筛 anti_removal `WATCH_SETTINGS` 线索一致），而对外文案只说是“杀后台省电”，能力范围被隐去。

**顺带第二步**：无障碍已开但 WRITE_SETTINGS 未开时，`i()` 走 `k()` 用同一遮罩 + `startActivity(MANAGE_WRITE_SETTINGS)`，形成“无障碍 → 写系统设置”的两段式受限设置教学。

```json
{
  "static_visibility": "clear",
  "visibility_note": "引导链全部在 classes.dex 中静态可见：ForceActivity#powerBoost/i/j/k、li#a/b、PowerBoostService#onServiceConnected 与 res/xml/power_optimize_config.xml、res/layout/view_window_setting.xml、strings.xml 均未加密，未发现加壳或远端下发 HTML；引导文字全为本地资源。",
  "summary_one_liner": "省电工具在用户点击 Power Boost 时跳转系统无障碍设置，并在 170ms 后向系统设置页之上叠一张全屏半透明“两步开启教程”遮罩窗，引导用户为监听 com.android.settings 的无障碍服务授权。",
  "disguise_identity": {
    "app_display_name": "Battery Saver",
    "claimed_brand_or_persona": "Battery Saver（省电/后台清理工具，宣称“杀后台应用省电”）",
    "a11y_service_label": "Battery Saver（服务未声明 android:label，系统列表回退显示应用名），说明文字为 power_description 全文",
    "identity_mismatch": true,
    "obfuscation_tricks": "无空白挤出/同形字/多 alias/伪造 isAccessibilityTool；隐瞒点在能力范围：无障碍配置限定 packageNames=com.android.settings 且 canRetrieveWindowContent=true（实际用于读取设置界面），对外仅描述为“杀后台省电”，未披露该监听范围。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.coramobile.powerbattery.batterysaver.force.ForceActivity（Power Boost 页，含后台应用列表、复选框与 power_boost_button）",
      "trigger_event": "用户点击 power_boost_button → OnClick powerBoost(View)；页面亦可由 PowerBoostService#onServiceConnected、ni#onClick、ci#onAnimationEnd 拉起",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Power Boost（工具栏 power_boost_toolbar_title1/2）；power_boost_write_system_settings_dialog_message: \"In Android 6.0 or above, you must permit %1$s to access system modification so that you can use this function.\"",
      "shown_text_zh": "“Power Boost”功能页；Android 6.0 以上需授予修改系统设置权限才能使用该功能",
      "user_action_requested": "点击底部 Power Boost 按钮开始清理/加速（有返回箭头可退出，非强制）",
      "code_anchor": "com.coramobile.powerbattery.batterysaver.force.ForceActivity#powerBoost / onCreate / f"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表）",
      "trigger_event": "powerBoost → i()：li.a(context) 读取 Settings.Secure enabled_accessibility_services 判定未授权，则 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（应用侧不绘制，交由系统页显示）",
      "shown_text_zh": "系统无障碍设置列表，用户需在其中找到 Battery Saver 并打开开关",
      "user_action_requested": "在系统列表中手动开启 Battery Saver 的无障碍开关",
      "code_anchor": "com.coramobile.powerbattery.batterysaver.force.ForceActivity#i + li#a(Context)"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "全屏悬浮遮罩窗（LayoutInflater.inflate(0x7f04008e)=res/layout/view_window_setting.xml，经 getWindowManager().addView 叠加于系统无障碍页之上）",
      "trigger_event": "i() 中 new Handler().postDelayed(new gv(this), 170L) → gv#run → ForceActivity#j()，WindowManager.LayoutParams type=2032/2002、flags|=8、width/height=-1、background=@color/mask_bg",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Tips / Follow below 2 steps to enable Force Stop feature: / Step 1. Scroll to find “Battery Saver” / Battery Saver / Off / Step 2. Tap “Battery Saver”and turn the switch on / Battery Saver / On / Got it",
      "shown_text_zh": "“提示”——按以下两步开启强制停止功能：第 1 步，滚动找到“Battery Saver”（当前显示 关）；第 2 步，点按“Battery Saver”并打开开关（打开后显示 开）；按钮“知道了”",
      "user_action_requested": "照图文在系统页滚动查找并打开 Battery Saver 开关；可点 “Got it” 关闭遮罩（也可等自动消失）",
      "code_anchor": "com.coramobile.powerbattery.batterysaver.force.ForceActivity#j + gv#run + res/layout/view_window_setting.xml + strings window_title/window_info/window_step1/window_step2/window_get"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "遮罩自动消退后回到 ForceActivity（仍在 Power Boost 页）",
      "trigger_event": "this.e.postDelayed(new gw(this), ToolTipPopup.DEFAULT_POPUP_DISPLAY_TIME) 定时 removeView；或 gx#onClick（Got it）立即 removeView",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "遮罩自动消失或点击“知道了”后，界面停留在 Power Boost 页，不自动重跳",
      "user_action_requested": "无强制动作；用户可放弃，或再次点击 Power Boost 按钮重新进入引导",
      "code_anchor": "gw#run / gx#onClick / ForceActivity#j"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统设置 android.settings.action.MANAGE_WRITE_SETTINGS（修改系统设置授权页）",
      "trigger_event": "i() 中无障碍已开启但 li.b(context)=Settings.System.canWrite 为 false 时：k() 先叠同一全屏遮罩（this.f，gz#onClick/gy#run 关闭），随后 startActivity(li.a())",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "2. Tap and Click switch to permit Write System Settings.（power_optimize_write_settings_overlay_line2）",
      "shown_text_zh": "第 2 步：点按开关以允许写入系统设置",
      "user_action_requested": "在系统页打开“允许修改系统设置”开关",
      "code_anchor": "com.coramobile.powerbattery.batterysaver.force.ForceActivity#i / #k + li#a()"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "PowerBoostService（无障碍服务）onServiceConnected → 再次拉起 ForceActivity",
      "trigger_event": "系统绑定无障碍服务后 onServiceConnected 内 new Intent(this, ForceActivity.class) 启动界面；回到 ForceActivity 后 powerBoost 再次点击时 i() 返回 true，执行 hl.a().a(c.b()) 并进入 ForceCleanActivity",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "power_description: \"Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access.\"",
      "shown_text_zh": "“Battery Saver 会关闭后台运行的应用以进一步省电。要启用此功能，请允许 Battery Saver 使用无障碍服务，打开开关以授予访问权限。”",
      "user_action_requested": "无需额外操作，获权后直接执行批量杀进程（ForceCleanActivity 展示清理结果）",
      "code_anchor": "com.coramobile.powerbattery.batterysaver.force.PowerBoostService#onServiceConnected + res/xml/power_optimize_config.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项说明文字：android:description=@string/power_description（res/xml/power_optimize_config.xml 引用），服务未设 android:label，列表名回退为应用名 Battery Saver",
    "系统设置页之上的全屏半透明遮罩窗：res/layout/view_window_setting.xml（Tips / 两步图文 / Got it），由 ForceActivity#j 通过 WindowManager.addView 叠加",
    "ForceActivity 页面内：power_dialog_message / power_optimize_accessibility_overlay_line1-2 等字符串资源已随包存在，作为跳转前后的提示文案储备（部分由 %1$s 填充应用名）",
    "ForceActivity 工具栏标题 power_boost_toolbar_title1/2（\"Power\" / \" Boost\"）与 checkbox 说明",
    "应用内 policy.html / license.html WebView：仅承载隐私政策与开源许可，与无障碍引导无关"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access.",
      "text_zh": "Battery Saver 会关闭后台运行的应用以进一步省电。要启用此功能，请允许 Battery Saver 使用无障碍服务，打开开关以授予访问权限。",
      "source_location": "res/values/strings.xml: power_description（供 res/xml/power_optimize_config.xml 的 android:description 使用）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Tips",
      "text_zh": "提示",
      "source_location": "res/values/strings.xml: window_title（view_window_setting.xml tv_title）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Follow below 2 steps to enable Force Stop feature:",
      "text_zh": "按以下两步开启“强制停止”功能：",
      "source_location": "res/values/strings.xml: window_info（view_window_setting.xml tv_info）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. Scroll to find “Battery Saver”",
      "text_zh": "第 1 步：滚动查找“Battery Saver”",
      "source_location": "res/values/strings.xml: window_step1（view_window_setting.xml tv_step_1）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. Tap “Battery Saver”and turn the switch on",
      "text_zh": "第 2 步：点按“Battery Saver”并打开开关",
      "source_location": "res/values/strings.xml: window_step2（view_window_setting.xml tv_step_2）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Got it",
      "text_zh": "知道了",
      "source_location": "res/values/strings.xml: window_get（view_window_setting.xml tv_get，gx#onClick 关闭遮罩）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "To enable Power Boost, please permit %1$s to use Accessibility Service",
      "text_zh": "要启用 Power Boost，请允许 %1$s 使用无障碍服务",
      "source_location": "res/values/strings.xml: power_dialog_message",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "1. Scroll and Find %1$s",
      "text_zh": "1. 滚动并找到 %1$s",
      "source_location": "res/values/strings.xml: power_optimize_accessibility_overlay_line1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. Tap and Click switch to permit Accessibility setting.",
      "text_zh": "2. 点按开关以允许无障碍设置。",
      "source_location": "res/values/strings.xml: power_optimize_accessibility_overlay_line2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. Tap and Click switch to permit Write System Settings.",
      "text_zh": "2. 点按开关以允许写入系统设置。",
      "source_location": "res/values/strings.xml: power_optimize_write_settings_overlay_line2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "In Android 6.0 or above, you must permit %1$s to access system modification so that you can use this function.",
      "text_zh": "在 Android 6.0 及以上，你必须允许 %1$s 修改系统，才能使用该功能。",
      "source_location": "res/values/strings.xml: power_boost_write_system_settings_dialog_message",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "无死循环：遮罩由 postDelayed(gw, DEFAULT_POPUP_DISPLAY_TIME) 自动 removeView，或点 Got it 立即关闭；用户返回 ForceActivity 后不自动重跳，需再次点击 Power Boost 才会重走 i() 引导；onResume 仅触发 ht 异步任务刷新进程列表，不含跳转",
    "overlay_or_fake_settings": "有全屏半透明遮罩（type 2002/2032，flags|=8 不可聚焦，width/height=-1，背景 @color/mask_bg），叠加在真实系统无障碍设置页与 MANAGE_WRITE_SETTINGS 页之上，内容是自绘两步教程卡片，非高仿系统开关页",
    "restricted_settings_13plus_coaching": "无；targetSdkVersion=20，未涉及 Android 13 应用详情“允许受限设置”教学，也未发现 SESSION_INSTALLER 绕过代码",
    "post_grant_anti_removal": "未见自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但无障碍配置限定 packageNames=com.android.settings 且 canRetrieveWindowContent=true、typeWindowStateChanged，服务具备读取设置界面的监听能力（能力可疑，未验证具体拦截行为）",
    "benign_graceful_degradation": "有弱降级：用户可以关闭遮罩后继续留在 Power Boost 页并退出，功能不可用但不阻断其他页面；不存在手动模式或 ADB 替代说明"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 后延迟约 170–500ms 再抓取（遮罩 170ms 才压栈），或监测到 ForceActivity 上点击 power_boost_button 的瞬间开始连续截图",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍设置页后压栈的全屏引导遮罩页",
        "page_identifier": "系统 Settings 无障碍列表之上出现全屏半透明遮罩 + 白底卡片，标题 Tips、含“Step 1/Step 2”“Got it”",
        "why_most_useful": "这是应用唯一实际呈现引导文案的载体，可证明其在真实设置页之上叠加自绘教程、并指出具体目标项名",
        "observable_utg_signals": ["节点文本 Tips / Follow below 2 steps to enable Force Stop feature:", "节点文本 Step 1. Scroll to find “Battery Saver” 与 Step 2. Tap “Battery Saver”and turn the switch on", "节点文本 Got it 可点击控件", "遮罩层与底层系统无障碍列表同屏共存"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility 中名为 Battery Saver 的服务项及其说明文字",
        "why_most_useful": "核对系统侧展示的服务名与 description 是否与包内文案一致，判断是否存在身份/范围隐瞒",
        "observable_utg_signals": ["服务项名称 Battery Saver", "说明文本以 Battery Saver kills background running apps 开头", "开关状态 Off/On 变化"]
      },
      {
        "page_role": "触发引导的 Power Boost 业务页",
        "page_identifier": "ForceActivity：工具栏“Power Boost”、后台应用列表、power_boost_button",
        "why_most_useful": "确定引导的触发时机为按需点击而非冷启动强制，并记录点击前后的界面差异",
        "observable_utg_signals": ["power_boost_button 可点击文本", "进程列表项与复选框 cb_app_selected", "点击后界面是否立即消失并跳系统设置"]
      },
      {
        "page_role": "WRITE_SETTINGS 授权页与同款遮罩",
        "page_identifier": "Settings → 修改系统设置（MANAGE_WRITE_SETTINGS）页面 + 同一遮罩布局",
        "why_most_useful": "证明存在无障碍→写系统设置的第二段受限权限教学",
        "observable_utg_signals": ["系统页标题含“修改系统设置”", "遮罩文本 2. Tap and Click switch to permit Write System Settings."]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "遮罩为 WindowManager 添加的 2002/2032 悬浮窗且 flags|=8 不可聚焦，部分 UTG 实现可能不将其纳入当前 Activity 层级而漏采，需以全屏截图 + 悬浮窗节点双通道采集；应用未加壳，静态引导链完整可见，无远端 HTML 或一阶段 Dropper 造成的盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_OVERLAY_STACK_ON_SETTINGS"
  ],
  "code_anchors": [
    "com.coramobile.powerbattery.batterysaver.force.ForceActivity#powerBoost",
    "com.coramobile.powerbattery.batterysaver.force.ForceActivity#i",
    "com.coramobile.powerbattery.batterysaver.force.ForceActivity#j",
    "com.coramobile.powerbattery.batterysaver.force.PowerBoostService#onServiceConnected",
    "res/xml/power_optimize_config.xml",
    "res/layout/view_window_setting.xml"
  ]
}
```

**边界说明**：本次为静态代码级核验，未运行应用；`PowerBoostService#onAccessibilityEvent` 对设置页事件的具体处理（是否用于阻止撤权）、预筛 `SESSION_INSTALLER`/`RESTRICTED_STR` 线索对应的 `xavier.lib` 广告/推广链未展开，故“获权后自保”结论仅标注为能力可疑而非已证实行为。

</details>
