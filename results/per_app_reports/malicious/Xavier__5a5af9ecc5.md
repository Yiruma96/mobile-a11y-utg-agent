# MR_099__5a5af9ecc5｜Xavier — Battery Saver

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：144.0s

## 1. 一句话核心结论

- **核心申请方式**：以“省电清理后台”为名，在点击强制停止时跳转系统无障碍设置页并在 170ms 后叠加全屏半透明遮罩分步教学“找到 Battery Saver 打开开关”，而其无障碍服务实际只监听 com.android.settings 窗口并读取窗口内容。
- **静态可见性说明**：无障碍服务的声明、配置、引导跳转、判定逻辑、遮罩布局与全部引导文案均以明文资源与可反编译 DEX 完整可见，未发现加壳、AES 或远端 HTML 承载该引导流程；仅无障碍服务内部具体的节点点击辅助方法（a(source) 等）未逐行展开，不影响引导链判定。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `5a5af9ecc5e6e909387993dd3f095fd19040b99ea4cde582bb831e436d083afc` |
| 包名 / 年份 | `com.coramobile.powerbattery.batterysaver` / 2017 |
| 家族 / 品类 | **Xavier**（同池样本数：41） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/f/analyzing-xavier-information-stealing-ad-library-android.html |
| 桌面显示名 | Battery Saver |
| 引导页宣称品牌/身份 | Battery Saver（电池省电/后台清理工具） |
| 系统无障碍列表服务名 | Battery Saver（服务未单独声明 label，沿用应用名 @string/app_name） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：服务未设置 android:label 而继承应用名以避免出现独立可疑服务名；无障碍说明把高权限能力包装为“清理后台省电”；遮罩标题仅显示 “Tips” 并称之为 Force Stop feature；包内另含 Xavier SDK 组件（xavier.lib.XavierActivity 等，label 置空、excludeFromRecents）与广告 SDK Activity 共用同一图标资源 icon_tnm。 |
| 无障碍服务类名 | `com.coramobile.powerbattery.batterysaver.force.PowerBoostService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：com.android.settings |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 业务功能触发 | com.coramobile.powerbattery.batterysaver.force.ForceActivity | 用户点击结果页“强制停止/优化”按钮，ResultView 点击监听 onClick 以 FLAG_ACTIVITY_NEW_TASK 启动 ForceActivity；另 PowerBoostService.onServiceConnected 在服务已连接时同样拉起该 Activity | 原生Activity | **原文**：Tips<br>**译注**：提示（Toolbar 标题） | 在面板中点击底部 powerBoost 按钮（R.id 2131624243）执行强制停止 | `ml.onClick；PowerBoostService.onServiceConnected；ForceActivity.e (setTitle 2131230897)` |
| 2 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表页） | powerBoost() 调用 i()，kl.a(Context) 读取 Settings.Secure 的 enabled_accessibility_services 判定本服务未启用后 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))，同时 Handler().postDelayed(new fy(this), 170L) | 系统无障碍页 | **原文**：Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access.<br>**译注**：Battery Saver 会杀死后台运行的应用以进一步节省电量。要启用此功能，请允许 Battery Saver 使用无障碍服务。打开开关以允许访问。 | 在系统无障碍列表中找到 Battery Saver 并打开开关（系统页本身提供返回/取消） | `ForceActivity.i；kl.a(Context)；res/xml/power_optimize_config.xml` |
| 3 | 遮罩叠层指引 | WindowManager 全屏浮层（inflate res/layout/view_window_setting.xml） | 跳转后 170ms 由 fy.run 触发 ForceActivity.j()；WRITE_SETTINGS 分支由 k() 叠加同款浮层。LayoutParams type=2032(或2002)、width/height=-1、flags\|=8、gravity=51、format=1 | 悬浮窗Overlay | **原文**：Tips / Follow below 2 steps to enable Force Stop feature: / Step 1. Scroll to find “Battery Saver” / Battery Saver / Off / Step 2. Tap “Battery Saver”and turn the switch on / On / Got it<br>**译注**：提示 / 按以下 2 步启用强制停止功能： / 第 1 步：滚动找到 “Battery Saver” / Battery Saver / 关 / 第 2 步：点击 “Battery Saver”并打开开关 / 开 / 知道了 | 只能按“知道了”（tv_get，id 2131624511）关闭遮罩，或等待 ToolTipPopup.DEFAULT_POPUP_DISPLAY_TIME 定时移除；无跳过/拒绝入口 | `ForceActivity.j / ForceActivity.k；fy.run；res/layout/view_window_setting.xml；res/values/strings.xml#L303-L310` |
| 4 | 拒权反馈循环 | ForceActivity + 遮罩移除回调 | 遮罩 postDelayed(fz, DEFAULT_POPUP_DISPLAY_TIME) 到期 removeView，或 ga.onClick / gc.onClick 点击“知道了” removeView；ForceActivity.onDestroy 再经 d() 延迟 500ms 由 fw.run 兜底 removeView。用户若返回设置页未授权，回到 ForceActivity.onResume → g() → gw AsyncTask 重新扫描进程 | 原生Activity | **原文**：Got it<br>**译注**：知道了 | 关闭遮罩后仍停留于 ForceActivity，再次点击强制停止会重新跳转无障碍设置页（无降级路径） | `fz.run；ga.onClick；gc.onClick；ForceActivity.d；ForceActivity.onResume；gw.doInBackground` |
| 5 | 获权后动作 | ForceActivity → ForceCleanActivity；PowerBoostService.onAccessibilityEvent | kl.a(Context) 返回 true（已启用）且 kl.b(Context) 成立后，powerBoost 调用 go.a().a(list) 并启动 ForceCleanActivity，随后 finish()；服务在 com.android.settings 窗口状态变化时按事件处理节点（非 Dialog 直接处理，Dialog 延迟 1000ms） | 原生Activity | 无 | 无需额外操作，应用自行在设置页执行控件操作 | `ForceActivity.powerBoost；PowerBoostService.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表服务说明：res/xml/power_optimize_config.xml 的 android:description=@string/power_description（res/values/strings.xml#L218 及 de/es/it/ko/pt/ru/th/tr/vi/ms/id 多语言）
- 跳转无障碍设置后 170ms 叠加的全屏半透明遮罩：res/layout/view_window_setting.xml（背景 @color/mask_bg，含 tv_title/tv_info/tv_step_1/tv_content_1/tv_content_switch_1/tv_step_2/tv_content_2/tv_content_switch_2/tv_get）
- 遮罩文案资源：res/values/strings.xml#L303-L310（window_get / window_info / window_on1 / window_on2 / window_step1 / window_step2 / window_text1 / window_title）
- ForceActivity 原生界面：Toolbar 标题（setTitle 2131230897）、进程列表 ListView（hf adapter）、计数 TextView、复选框 mCheckbox 与底部 powerBoost 按钮
- 本地 HTML 页面（非引导载体，仅隐私/许可说明）：assets/policy.html、assets/license.html

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access. | Battery Saver 会杀死后台运行的应用以进一步节省电量。要启用此功能，请允许 Battery Saver 使用无障碍服务。打开开关以允许访问。 | `res/values/strings.xml power_description（经 res/xml/power_optimize_config.xml android:description 引用）` | 清理工具伪装 |
| en | Follow below 2 steps to enable Force Stop feature: | 按以下 2 步启用强制停止功能： | `res/values/strings.xml window_info` | 受限设置分步教学 |
| en | Step 1. Scroll to find “Battery Saver” | 第 1 步：滚动找到 “Battery Saver” | `res/values/strings.xml window_step1` | 受限设置分步教学 |
| en | Step 2. Tap “Battery Saver”and turn the switch on | 第 2 步：点击 “Battery Saver”并打开开关 | `res/values/strings.xml window_step2` | 受限设置分步教学 |
| en | Tips | 提示 | `res/values/strings.xml window_title` | 未知 |
| en | Got it | 知道了 | `res/values/strings.xml window_get` | 未知 |
| en | Battery Saver | Battery Saver | `res/values/strings.xml window_text1 / window_step1、window_step2 中引用` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：遮罩仅在定时到期或点击“知道了”后移除，ForceActivity 不会因未授权而退出或降级；用户从设置页返回后 onResume → g() → gw AsyncTask 重新扫描，再次点击强制停止会重新跳转 ACCESSIBILITY_SETTINGS 并再次叠加遮罩，形成重复拉起。kl.a(Context) 捕获 SettingNotFoundException 时直接返回 true（视为已授权），绕过真实状态判断。
- **遮罩叠层 / 高仿系统设置页**：是：跳转系统无障碍设置页后 170ms 用 WindowManager.addView 叠加全屏（-1×-1）半透明遮罩，type=2032(TYPE_SYSTEM_OVERLAY) 或 2002(TYPE_SYSTEM_ALERT)、flags|=8、gravity=51，覆盖在真实系统设置页之上做两步图文指引（含箭头 boost_arrow 与开关图标 ic_button_on）；非高仿系统开关页，而是覆盖式教学浮层。
- **Android 13+ 受限设置（Restricted Settings）应对**：无：仅引导无障碍服务开关，未见针对 Android 13+ 受限设置的应用详情菜单教学，也未见 SESSION_INSTALLER 绕过路径。
- **获权后即时行为与防撤权机制**：未见以 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；onAccessibilityEvent 仅处理 typeWindowStateChanged（32）事件并做节点操作，未见监听设置页阻止关闭开关的显式逻辑。
- **良性降级 / 替代方案**：无：未授权时不做任何降级（如仅展示可清理进程列表或提供手动模式），仅反复跳转设置页并要求用户开启。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 ForceActivity.powerBoost 触发 i() 的时刻拉起检测：即监测到 startActivity(Intent("android.settings.ACCESSIBILITY_SETTINGS")) 或界面切换为系统无障碍设置页时开始抓取，并在其后约 170ms 再次抓取以捕获叠加上来的遮罩层。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：引导链全部为原生文本与本地布局，纯文本 UTG 可完整提取；但若在无 SYSTEM_ALERT_WINDOW 授权或 kx.a() 判定的机型上，遮罩 addView 可能抛异常被 catch 吞掉（仅 printStackTrace），此时只剩跳转设置页而无可视教学层，需以“跳转 ACCESSIBILITY_SETTINGS + 服务 description”作为兜底判别信号。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转前业务面板页（ForceActivity）** | Toolbar 标题“Tips/优化” + 进程列表 + 底部强制停止按钮 + 复选框 | 确认引导由业务按钮主动触发，而非系统正常权限请求，可定位 powerBoost→i 的调用起点 | 包名 com.coramobile.powerbattery.batterysaver 的 ForceActivity 前台；存在 powerBoost 按钮与 mCheckbox 控件节点；无系统权限对话框 |
| **设置页后约 170ms 压栈遮罩页** | 全屏半透明遮罩 + 白色居中卡片，标题 Tips，两段 Step 文案与箭头/开关图标，右下角 Got it | 这是诱导开启的决定性证据：遮罩叠加在真实系统无障碍页之上，文案逐字教用户开启 Battery Saver 开关 | 窗口层级出现与当前前台 Activity 不同的悬浮窗（SYSTEM_OVERLAY）；文本节点含 “Step 1. Scroll to find “Battery Saver””；文本节点含 “Got it”；背景节点颜色为 mask_bg 半透明 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中名为 Battery Saver 的服务条目及说明文字 | 核对系统侧展示名与 description 是否与省电宣称一致，确认服务实际权限范围 | 服务名 Battery Saver；说明文本含 “kills background running apps”；开关状态由关变开 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.coramobile.powerbattery.batterysaver.force.ForceActivity.i`
- `com.coramobile.powerbattery.batterysaver.force.ForceActivity.j`
- `com.coramobile.powerbattery.batterysaver.force.ForceActivity.k`
- `com.coramobile.powerbattery.batterysaver.force.PowerBoostService.onServiceConnected`
- `res/layout/view_window_setting.xml`
- `res/xml/power_optimize_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（代码级定向核验，共 12 次定向工具调用）

**1. 无障碍服务的实际监听范围与宣称功能不一致**
- [power_optimize_config.xml](<resource-unit:#1 file:res/xml/power_optimize_config.xml>) 将 `packageNames` 硬性限定为 `com.android.settings`，事件类型为 `typeWindowStateChanged`，`notificationTimeout=150`，`canRetrieveWindowContent=true`。这一配置表明，该服务的设计目标是在**系统设置界面内读取窗口内容并定位控件**，并非“杀后台省电”。
- [PowerBoostService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.coramobile.powerbattery.batterysaver.force.PowerBoostService#onAccessibilityEvent>) 对非 Dialog 事件直接处理节点，对 Dialog 事件延迟 1000ms 处理，这是典型的设置页自动化点击结构。

**2. 引导路径完整可静态还原**
- 用户点击业务按钮后，[ml.onClick](<resource-unit:#1.dex1 code:ml#onClick>) 直接以 `FLAG_ACTIVITY_NEW_TASK` 拉起 `ForceActivity`；服务连接回调 [onServiceConnected()](<resource-unit:#1.dex1 code:com.coramobile.powerbattery.batterysaver.force.PowerBoostService#onServiceConnected>) 也会拉起同一个面板。
- 点击“强制停止”后，[powerBoost()](<resource-unit:#1.dex1 code:com.coramobile.powerbattery.batterysaver.force.ForceActivity#powerBoost>) 调用 [i()](<resource-unit:#1.dex1 code:com.coramobile.powerbattery.batterysaver.force.ForceActivity#i>)；后者读取 `Settings.Secure.enabled_accessibility_services`，判断是否包含本服务（[kl.a](<resource-unit:#1.dex1 code:kl#a>)）。未启用时跳 `android.settings.ACCESSIBILITY_SETTINGS`，并 `postDelayed(fy, 170ms)`。
- **170ms 后压栈遮罩**：[fy.run](<resource-unit:#1.dex1 code:fy#run>) → [j()](<resource-unit:#1.dex1 code:com.coramobile.powerbattery.batterysaver.force.ForceActivity#j>)；另一分支 [k()](<resource-unit:#1.dex1 code:com.coramobile.powerbattery.batterysaver.force.ForceActivity#k>) 用于 WRITE_SETTINGS。二者均用 `WindowManager.addView` 叠加全屏视图（`type=2032/2002`、`-1×-1`、`flags|=8`、`gravity=51`），加载 [view_window_setting.xml](<resource-unit:#1 file:res/layout/view_window_setting.xml>)，背景为半透明 `@color/mask_bg`，内容为“Tips / Step 1. Scroll to find “Battery Saver” / Step 2. Tap “Battery Saver”and turn the switch on / Got it”。

**3. 关键交互特征**
- 遮罩覆盖系统设置页，属于**盖在系统无障碍页上的教学浮层**；点击“Got it”或定时器到期后移除，`onDestroy` 还有 500ms 兜底移除。
- 没有取消或跳过按钮，也没有降级路径；用户只能按指引操作，或手动退出。
- 文案仅称“省电需要清理后台”，未披露可获得设置页窗口读取与模拟点击能力。
- 应用内嵌 Xavier SDK（`xavier.lib.*` 的 Activity、Receiver、MessageService 与 `xavier.MEDIA_ID`），显示名为 “Battery Saver”，但无障碍服务实际能力远超省电清理。

**4. 未决与边界**
- 无障碍服务获取权限后，具体会点击哪些设置项（例如自动关闭某些开关）在 `a(source)` 等辅助方法中还需进一步展开；这不影响对“诱导开启”本身的判定。
- 未启动动态分析；UTG 页面特征基于静态资源与布局确定。

已登记风险 **R-001**（`deceptive_behavior` / high）：无障碍权限分步诱导与设置页全屏遮罩叠层。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍服务的声明、配置、引导跳转、判定逻辑、遮罩布局与全部引导文案均以明文资源与可反编译 DEX 完整可见，未发现加壳、AES 或远端 HTML 承载该引导流程；仅无障碍服务内部具体的节点点击辅助方法（a(source) 等）未逐行展开，不影响引导链判定。",
  "summary_one_liner": "以“省电清理后台”为名，在点击强制停止时跳转系统无障碍设置页并在 170ms 后叠加全屏半透明遮罩分步教学“找到 Battery Saver 打开开关”，而其无障碍服务实际只监听 com.android.settings 窗口并读取窗口内容。",
  "disguise_identity": {
    "app_display_name": "Battery Saver",
    "claimed_brand_or_persona": "Battery Saver（电池省电/后台清理工具）",
    "a11y_service_label": "Battery Saver（服务未单独声明 label，沿用应用名 @string/app_name）",
    "identity_mismatch": true,
    "obfuscation_tricks": "服务未设置 android:label 而继承应用名以避免出现独立可疑服务名；无障碍说明把高权限能力包装为“清理后台省电”；遮罩标题仅显示 “Tips” 并称之为 Force Stop feature；包内另含 Xavier SDK 组件（xavier.lib.XavierActivity 等，label 置空、excludeFromRecents）与广告 SDK Activity 共用同一图标资源 icon_tnm。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "业务功能触发",
      "screen_or_component": "com.coramobile.powerbattery.batterysaver.force.ForceActivity",
      "trigger_event": "用户点击结果页“强制停止/优化”按钮，ResultView 点击监听 onClick 以 FLAG_ACTIVITY_NEW_TASK 启动 ForceActivity；另 PowerBoostService.onServiceConnected 在服务已连接时同样拉起该 Activity",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Tips",
      "shown_text_zh": "提示（Toolbar 标题）",
      "user_action_requested": "在面板中点击底部 powerBoost 按钮（R.id 2131624243）执行强制停止",
      "code_anchor": "ml.onClick；PowerBoostService.onServiceConnected；ForceActivity.e (setTitle 2131230897)"
    },
    {
      "step": 2,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（无障碍服务列表页）",
      "trigger_event": "powerBoost() 调用 i()，kl.a(Context) 读取 Settings.Secure 的 enabled_accessibility_services 判定本服务未启用后 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))，同时 Handler().postDelayed(new fy(this), 170L)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access.",
      "shown_text_zh": "Battery Saver 会杀死后台运行的应用以进一步节省电量。要启用此功能，请允许 Battery Saver 使用无障碍服务。打开开关以允许访问。",
      "user_action_requested": "在系统无障碍列表中找到 Battery Saver 并打开开关（系统页本身提供返回/取消）",
      "code_anchor": "ForceActivity.i；kl.a(Context)；res/xml/power_optimize_config.xml"
    },
    {
      "step": 3,
      "stage": "遮罩叠层指引",
      "screen_or_component": "WindowManager 全屏浮层（inflate res/layout/view_window_setting.xml）",
      "trigger_event": "跳转后 170ms 由 fy.run 触发 ForceActivity.j()；WRITE_SETTINGS 分支由 k() 叠加同款浮层。LayoutParams type=2032(或2002)、width/height=-1、flags|=8、gravity=51、format=1",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Tips / Follow below 2 steps to enable Force Stop feature: / Step 1. Scroll to find “Battery Saver” / Battery Saver / Off / Step 2. Tap “Battery Saver”and turn the switch on / On / Got it",
      "shown_text_zh": "提示 / 按以下 2 步启用强制停止功能： / 第 1 步：滚动找到 “Battery Saver” / Battery Saver / 关 / 第 2 步：点击 “Battery Saver”并打开开关 / 开 / 知道了",
      "user_action_requested": "只能按“知道了”（tv_get，id 2131624511）关闭遮罩，或等待 ToolTipPopup.DEFAULT_POPUP_DISPLAY_TIME 定时移除；无跳过/拒绝入口",
      "code_anchor": "ForceActivity.j / ForceActivity.k；fy.run；res/layout/view_window_setting.xml；res/values/strings.xml#L303-L310"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "ForceActivity + 遮罩移除回调",
      "trigger_event": "遮罩 postDelayed(fz, DEFAULT_POPUP_DISPLAY_TIME) 到期 removeView，或 ga.onClick / gc.onClick 点击“知道了” removeView；ForceActivity.onDestroy 再经 d() 延迟 500ms 由 fw.run 兜底 removeView。用户若返回设置页未授权，回到 ForceActivity.onResume → g() → gw AsyncTask 重新扫描进程",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Got it",
      "shown_text_zh": "知道了",
      "user_action_requested": "关闭遮罩后仍停留于 ForceActivity，再次点击强制停止会重新跳转无障碍设置页（无降级路径）",
      "code_anchor": "fz.run；ga.onClick；gc.onClick；ForceActivity.d；ForceActivity.onResume；gw.doInBackground"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "ForceActivity → ForceCleanActivity；PowerBoostService.onAccessibilityEvent",
      "trigger_event": "kl.a(Context) 返回 true（已启用）且 kl.b(Context) 成立后，powerBoost 调用 go.a().a(list) 并启动 ForceCleanActivity，随后 finish()；服务在 com.android.settings 窗口状态变化时按事件处理节点（非 Dialog 直接处理，Dialog 延迟 1000ms）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（进入清理结果页，文案取自其他资源）",
      "user_action_requested": "无需额外操作，应用自行在设置页执行控件操作",
      "code_anchor": "ForceActivity.powerBoost；PowerBoostService.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表服务说明：res/xml/power_optimize_config.xml 的 android:description=@string/power_description（res/values/strings.xml#L218 及 de/es/it/ko/pt/ru/th/tr/vi/ms/id 多语言）",
    "跳转无障碍设置后 170ms 叠加的全屏半透明遮罩：res/layout/view_window_setting.xml（背景 @color/mask_bg，含 tv_title/tv_info/tv_step_1/tv_content_1/tv_content_switch_1/tv_step_2/tv_content_2/tv_content_switch_2/tv_get）",
    "遮罩文案资源：res/values/strings.xml#L303-L310（window_get / window_info / window_on1 / window_on2 / window_step1 / window_step2 / window_text1 / window_title）",
    "ForceActivity 原生界面：Toolbar 标题（setTitle 2131230897）、进程列表 ListView（hf adapter）、计数 TextView、复选框 mCheckbox 与底部 powerBoost 按钮",
    "本地 HTML 页面（非引导载体，仅隐私/许可说明）：assets/policy.html、assets/license.html"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Battery Saver kills background running apps to further save your Battery. To enable this function, please permit Battery Saver to use Accessibility Service. Turn ON the switch to permit access.",
      "text_zh": "Battery Saver 会杀死后台运行的应用以进一步节省电量。要启用此功能，请允许 Battery Saver 使用无障碍服务。打开开关以允许访问。",
      "source_location": "res/values/strings.xml power_description（经 res/xml/power_optimize_config.xml android:description 引用）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Follow below 2 steps to enable Force Stop feature:",
      "text_zh": "按以下 2 步启用强制停止功能：",
      "source_location": "res/values/strings.xml window_info",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. Scroll to find “Battery Saver”",
      "text_zh": "第 1 步：滚动找到 “Battery Saver”",
      "source_location": "res/values/strings.xml window_step1",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. Tap “Battery Saver”and turn the switch on",
      "text_zh": "第 2 步：点击 “Battery Saver”并打开开关",
      "source_location": "res/values/strings.xml window_step2",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Tips",
      "text_zh": "提示",
      "source_location": "res/values/strings.xml window_title",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Got it",
      "text_zh": "知道了",
      "source_location": "res/values/strings.xml window_get",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Battery Saver",
      "text_zh": "Battery Saver",
      "source_location": "res/values/strings.xml window_text1 / window_step1、window_step2 中引用",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "遮罩仅在定时到期或点击“知道了”后移除，ForceActivity 不会因未授权而退出或降级；用户从设置页返回后 onResume → g() → gw AsyncTask 重新扫描，再次点击强制停止会重新跳转 ACCESSIBILITY_SETTINGS 并再次叠加遮罩，形成重复拉起。kl.a(Context) 捕获 SettingNotFoundException 时直接返回 true（视为已授权），绕过真实状态判断。",
    "overlay_or_fake_settings": "是：跳转系统无障碍设置页后 170ms 用 WindowManager.addView 叠加全屏（-1×-1）半透明遮罩，type=2032(TYPE_SYSTEM_OVERLAY) 或 2002(TYPE_SYSTEM_ALERT)、flags|=8、gravity=51，覆盖在真实系统设置页之上做两步图文指引（含箭头 boost_arrow 与开关图标 ic_button_on）；非高仿系统开关页，而是覆盖式教学浮层。",
    "restricted_settings_13plus_coaching": "无：仅引导无障碍服务开关，未见针对 Android 13+ 受限设置的应用详情菜单教学，也未见 SESSION_INSTALLER 绕过路径。",
    "post_grant_anti_removal": "未见以 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；onAccessibilityEvent 仅处理 typeWindowStateChanged（32）事件并做节点操作，未见监听设置页阻止关闭开关的显式逻辑。",
    "benign_graceful_degradation": "无：未授权时不做任何降级（如仅展示可清理进程列表或提供手动模式），仅反复跳转设置页并要求用户开启。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 ForceActivity.powerBoost 触发 i() 的时刻拉起检测：即监测到 startActivity(Intent(\"android.settings.ACCESSIBILITY_SETTINGS\")) 或界面切换为系统无障碍设置页时开始抓取，并在其后约 170ms 再次抓取以捕获叠加上来的遮罩层。",
    "key_pages_to_capture": [
      {
        "page_role": "跳转前业务面板页（ForceActivity）",
        "page_identifier": "Toolbar 标题“Tips/优化” + 进程列表 + 底部强制停止按钮 + 复选框",
        "why_most_useful": "确认引导由业务按钮主动触发，而非系统正常权限请求，可定位 powerBoost→i 的调用起点",
        "observable_utg_signals": ["包名 com.coramobile.powerbattery.batterysaver 的 ForceActivity 前台", "存在 powerBoost 按钮与 mCheckbox 控件节点", "无系统权限对话框"]
      },
      {
        "page_role": "设置页后约 170ms 压栈遮罩页",
        "page_identifier": "全屏半透明遮罩 + 白色居中卡片，标题 Tips，两段 Step 文案与箭头/开关图标，右下角 Got it",
        "why_most_useful": "这是诱导开启的决定性证据：遮罩叠加在真实系统无障碍页之上，文案逐字教用户开启 Battery Saver 开关",
        "observable_utg_signals": ["窗口层级出现与当前前台 Activity 不同的悬浮窗（SYSTEM_OVERLAY）", "文本节点含 “Step 1. Scroll to find “Battery Saver””", "文本节点含 “Got it”", "背景节点颜色为 mask_bg 半透明"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中名为 Battery Saver 的服务条目及说明文字",
        "why_most_useful": "核对系统侧展示名与 description 是否与省电宣称一致，确认服务实际权限范围",
        "observable_utg_signals": ["服务名 Battery Saver", "说明文本含 “kills background running apps”", "开关状态由关变开"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "引导链全部为原生文本与本地布局，纯文本 UTG 可完整提取；但若在无 SYSTEM_ALERT_WINDOW 授权或 kx.a() 判定的机型上，遮罩 addView 可能抛异常被 catch 吞掉（仅 printStackTrace），此时只剩跳转设置页而无可视教学层，需以“跳转 ACCESSIBILITY_SETTINGS + 服务 description”作为兜底判别信号。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.coramobile.powerbattery.batterysaver.force.ForceActivity.i",
    "com.coramobile.powerbattery.batterysaver.force.ForceActivity.j",
    "com.coramobile.powerbattery.batterysaver.force.ForceActivity.k",
    "com.coramobile.powerbattery.batterysaver.force.PowerBoostService.onServiceConnected",
    "res/layout/view_window_setting.xml",
    "res/xml/power_optimize_config.xml"
  ]
}
```

</details>
