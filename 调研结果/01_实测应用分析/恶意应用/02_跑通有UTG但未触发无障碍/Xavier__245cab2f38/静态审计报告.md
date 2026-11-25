# MR_131__245cab2f38｜Xavier — Master Cleanner

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：109.0s

## 1. 一句话核心结论

- **核心申请方式**：清理工具在进程管理页点击后先跳系统无障碍列表、再立刻压上 90% 黑底半透明图示遮罩，用两张步骤图教学开启 Master Cleanner 无障碍服务，并以'不收集任何信息''80% 用户已开启'话术降低戒心，多个业务页会反复拉起同一引导。
- **静态可见性说明**：无障碍引导链路（ProcessManagerActivity 点击 -> ACCESSIBILITY_SETTINGS 跳转 -> AccessTipActivity 半透明遮罩 -> activity_access_tip.xml 图示）全部为明文 DEX 与资源，无加壳、无 AES 密文、无远端 HTML。仅图示内容以 PNG（access_guide_step_01/02、access_arrow、pop_notice_read、usage_access）承载，文本不可静态读取；获权后 MyAccessibilityService 内 GLOBAL_ACTION 反撤权细节本轮未逐行核验。
- **命中的行为模式标签**：`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `245cab2f38c539c9daec89c9d00394b8699da18641af872b8f9cbe57a48a9e18` |
| 包名 / 年份 | `com.appativesh.masterclean` / 2017 |
| 家族 / 品类 | **Xavier**（同池样本数：41） |
| 原始来源标识 | https://www.trendmicro.com/en_us/research/17/f/analyzing-xavier-information-stealing-ad-library-android.html |
| 桌面显示名 | Master Cleanner |
| 引导页宣称品牌/身份 | Master Cleanner（手机清理/进程管理工具，声称'帮你停止不必要的应用且不收集任何信息'） |
| 系统无障碍列表服务名 | Master Cleanner |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：品牌名拼写异常（Cleanner 而非 Cleaner）；无障碍用途声明窄化（只说'停止不必要的应用/不收集信息'），而服务实际声明 canRetrieveWindowContent=true、监听 typeWindowStateChanged，并在类内持有 WindowManager + MyDesktopLayout 悬浮窗与 BroadcastReceiver；AccessTipActivity 使用 Theme.Translucent.NoTitleBar + #bb000000 全屏遮罩叠在系统设置页之上，使系统无障碍界面处于半遮挡状态；未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。 |
| 无障碍服务类名 | `com.appativesh.masterclean.process.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Master Cleanner uses accessibility features to help you stop unnecessary app(s). We do not collect any information |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.appativesh.masterclean.PIPCleanerMainActivity（LAUNCHER，label=@string/my_app_name） | onCreate / LAUNCHER 图标点击 | 原生Activity | **原文**：Master Cleanner<br>**译注**：桌面与启动页显示的应用名：Master Cleanner | 正常进入清理工具主界面 | `com.appativesh.masterclean.PIPCleanerMainActivity（AndroidManifest.xml application/activity 声明）` |
| 2 | 业务功能触发 | com.appativesh.masterclean.process.ProcessManagerActivity（Theme.Translucent.NoTitleBar） | 用户进入进程/后台应用管理功能，点击 id=2131165606 的按钮触发 onClick | 原生Activity | **原文**：无（按钮文案取自布局资源，未逐字核验）<br>**译注**：进程管理页中的一键加速/清理按钮 | 点击清理按钮（无取消按钮，点击即进入引导） | `com.appativesh.masterclean.process.ProcessManagerActivity#onClick` |
| 3 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | onClick 中 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))，随后紧接 k(); g(); AccessTipActivity.a(this, "accessibilityServiceAccess") | 系统无障碍页 | **原文**：Master Cleanner uses accessibility features to help you stop unnecessary app(s). We do not collect any information<br>**译注**：系统无障碍服务列表中 Master Cleanner 条目的说明：使用无障碍功能帮你停止不必要的应用，我们不收集任何信息 | 在系统列表中查找并开启 Master Cleanner 服务（用户须自行点击开关） | `com.appativesh.masterclean.process.ProcessManagerActivity#onClick / res/xml/phone_accessibility.xml（android:description=@string/accessibility_service_description）` |
| 4 | 遮罩叠层指引 | com.appativesh.masterclean.AccessTipActivity（Theme.Translucent.NoTitleBar，背景 #bb000000 全屏半透明） | AccessTipActivity.a(Context,"accessibilityServiceAccess") -> onCreate 读取 operationType，命中 accessibilityServiceAccess 后调用 d() 将 rl_accessibilityService_layout 置为可见 | 悬浮窗Overlay | **原文**：Please enter  Master Cleanner  off / Master Cleanner Turn the feature on<br>**译注**：遮罩上分两步的图示教学：第一步「进入 [Master Cleanner]（当前状态 off）」并配 access_guide_step_01 截图与箭头；第二步「把该功能打开」配 access_guide_step_02 截图，指示用户在系统页里打开开关 | 按图示在下方系统无障碍页点击 Master Cleanner 开关；点击遮罩任意位置或按钮即 finish() 关闭遮罩（无'跳过/取消'文案，但可单击穿透式关闭） | `com.appativesh.masterclean.AccessTipActivity#onCreate / #d / res/layout/activity_access_tip.xml（@id/rl_accessibilityService_layout）` |
| 5 | 拒权反馈循环 | AccessTipActivity（由 applock.activity.c/e/g/u/w#run、floatingwindow.aa#run、fragment.af#run 等入口再次调用 AccessTipActivity.a） | 各业务页 Runnable#run 中再次执行 AccessTipActivity.a(context, operationType) | 悬浮窗Overlay | **原文**：无新增文案（复用同一遮罩布局）<br>**译注**：未开启无障碍时，用户后续使用其它功能会被再次弹出同一引导遮罩 | 再次按图示去开启无障碍；遮罩本身仍可单击关闭（未发现 onResume 强制重跳或定时器死循环） | `com.appativesh.masterclean.AccessTipActivity#a / com.appativesh.masterclean.applock.activity.c#run / com.appativesh.masterclean.fragment.af#run` |
| 6 | 跳受限设置（同类并行引导） | AccessTipActivity 的 open_window_layout（小米 MIUI 悬浮窗引导）、usage_Access_layout（使用情况访问）、boot_start_layout（自启动） | AccessTipActivity.a(ctx,"openWindowAccess"/"openUsageAccess"/"bootStartAccess") -> onCreate 调 e()/c()/b() 显示对应布局 | 悬浮窗Overlay | **原文**：xiaomi_open_window_title / xiaomi_open_window_content / xiaomi_open_window_explain / usage_access_last_step_tip / confirm<br>**译注**：以截图（pop_notice_read、usage_access）教学在 MIUI 中开启'显示悬浮窗'、'使用情况访问'与自启动权限，配'确认'按钮 | 按截图在系统/厂商设置中逐项允许悬浮窗、使用情况访问、自启动 | `res/layout/activity_access_tip.xml（@id/open_window_layout、@id/usage_Access_layout、@id/boot_start_layout） / com.appativesh.masterclean.AccessTipActivity#e / #c / #b` |
| 7 | 获权后动作 | com.appativesh.masterclean.process.MyAccessibilityService（onServiceConnected / onStart / onAccessibilityEvent，持有 WindowManager + MyDesktopLayout） | 系统绑定服务后 onServiceConnected/onStart；之后窗口状态变化（typeWindowStateChanged）触发 onAccessibilityEvent | 悬浮窗Overlay | **原文**：无（本步界面由运行时悬浮窗动态构建）<br>**译注**：获权后在窗口切换时叠加自定义悬浮视图并执行进程清理/拦截动作 | 无需用户操作（后台自动执行） | `com.appativesh.masterclean.process.MyAccessibilityService#onStart / #onAccessibilityEvent（字段 WindowManager g、MyDesktopLayout e、Handler o、BroadcastReceiver p）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/xml/phone_accessibility.xml 的 android:description -> 系统无障碍服务列表条目下方的说明文字（@string/accessibility_service_description）
- AccessTipActivity 全屏半透明遮罩（#bb000000）内的 rl_accessibilityService_layout：'Please enter'+@string/my_app_name+'off'、@string/my_app_name+'Turn the feature on'，并叠放 access_guide_step_01/access_guide_step_02 图示与 access_arrow 箭头
- 同一遮罩布局 open_window_layout：xiaomi_open_window_title/content/explain + pop_notice_read 截图 + 'confirm' 按钮
- 同一遮罩布局 usage_Access_layout：usage_access 截图 + usage_access_last_step_tip
- 同一遮罩布局 boot_start_layout：自启动引导文案（复用 confirm）
- res/values/strings.xml 中 dialog_dis_01：'Master Cleanner uses accessibility features to help you stop unnecessary app(s). More than 80% of users enable this feature.'（弹窗类话术资源，具体弹出位置本轮未逐处核验）
- assets/help/help_english_v1_0_7.html 与 assets/help/help_v1_0_7.html：本地 HTML 帮助页（标题为 AppLocker/AppLocker常见问题），未承载无障碍引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Master Cleanner uses accessibility features to help you stop unnecessary app(s). We do not collect any information | Master Cleanner 使用无障碍功能来帮你停止不必要的应用。我们不收集任何信息。 | `res/values/strings.xml key=accessibility_service_description（经 res/xml/phone_accessibility.xml 的 android:description 呈现于系统无障碍列表）` | 隐私承诺 |
| en | Master Cleanner uses accessibility features to help you stop unnecessary app(s). More than 80% of users enable this feature. | Master Cleanner 使用无障碍功能来帮你停止不必要的应用。超过 80% 的用户都开启了此功能。 | `res/values/strings.xml key=dialog_dis_01` | 清理工具伪装 |
| en | Please enter | 请进入（配应用名与 'off' 状态，指示在系统列表中找到该应用） | `res/values/strings.xml key=access_tip_step_01（用于 res/layout/activity_access_tip.xml 遮罩第一步）` | 受限设置分步教学 |
| en | off | 关闭（显示当前服务处于关闭状态，制造待办压力） | `res/values/strings.xml key=access_off` | 受限设置分步教学 |
| en | Turn the feature on | 把该功能打开（第二步图示，指示点击系统开关） | `res/values/strings.xml key=access_tip_step_02` | 受限设置分步教学 |
| zh | AppLocker常见问题 | AppLocker 常见问题（本地帮助页标题，功能定位为应用锁） | `assets/help/help_v1_0_7.html` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`user_feature_on_demand`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：AccessTipActivity 自身无 onResume 重跳、无定时器（onTouchEvent/按钮 onClick 均只 finish()）；但 applock.activity.c/e/g/u/w、floatingwindow.aa、fragment.af 共 8 处 Runnable#run 会再次调用 AccessTipActivity.a(ctx, operationType)，因此用户每次使用相关功能都会被重新压上同一引导遮罩，形成按需重复施压。
- **遮罩叠层 / 高仿系统设置页**：叠放 90% 黑底（#bb000000）全屏半透明 Activity（Theme.Translucent.NoTitleBar）覆盖在系统 ACCESSIBILITY_SETTINGS 页之上，用两张真实系统截图（access_guide_step_01/02）+ 箭头做分步指引；不是高仿系统开关页，而是真实系统页 + 遮罩指引。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现跳 ACTION_APPLICATION_DETAILS_SETTINGS 或 'Allow restricted settings' 菜单教学，也未发现 Session 安装器绕过（targetSdkVersion=22，运行于旧策略环境）。
- **获权后即时行为与防撤权机制**：本轮未逐行核验。依据类结构，MyAccessibilityService 持有 WindowManager、MyDesktopLayout、Handler 与 BroadcastReceiver，并实现 onAccessibilityEvent/onStart；预筛线索显示存在 PERFORM_GLOBAL_ACTION、WATCH_SETTINGS、WATCH_PKG_INSTALLER 等行为标记，指向获权后监听设置页并可能用全局返回/主页阻止撤权，具体实现待验证。
- **良性降级 / 替代方案**：无。除遮罩可单击关闭外，未见手动模式、仅观看模式或明确的功能降级路径说明。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 ProcessManagerActivity#onClick（id=2131165606）触发瞬间拉起 UTG，并持续跟踪随后 2~3 秒的窗口栈：应先后看到 android.settings.ACCESSIBILITY_SETTINGS 与 com.appativesh.masterclean/.AccessTipActivity 两个窗口叠加；另可在 Activity 启动参数 operationType=accessibilityServiceAccess 上直接命中。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：遮罩内的关键引导几乎全部为 PNG 截图（access_guide_step_01/02、access_arrow、pop_notice_read、usage_access），UTG 文本节点极少，纯文本检测易漏；需配合截图 + OCR 或图像相似度。另获权后的反撤权行为发生在系统设置页上下文，UTG 需持续监测窗口栈变化与 GLOBAL_ACTION 回退事件才能捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **设置页后压栈遮罩页（核心诱导界面）** | com.appativesh.masterclean/.AccessTipActivity，主题 Translucent、背景 #bb000000，含 access_guide_step_01/02 两张截图与 access_arrow | 此页同时证明'跳系统设置'与'叠加图文教学'两个动作在同一时序内发生，是判定诱导开启无障碍的决定性画面 | 窗口栈中 AccessTipActivity 位于 ACCESSIBILITY_SETTINGS 之上；遮罩半透明，可见下层系统无障碍列表；遮罩内仅极短文字（Please enter / off / Turn the feature on），主要信息在图片中 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载/已安装的服务，条目名 Master Cleanner，说明为'...We do not collect any information' | 核对身份与声明：显示名与服务名一致但用途声明窄化，且条目名拼写为 Cleanner | 服务条目文本 Master Cleanner；说明文字含 'We do not collect any information' 隐私承诺；开关初始为 off |
| **同类受限权限引导页（悬浮窗/使用情况/自启动）** | AccessTipActivity 的 open_window_layout / usage_Access_layout / boot_start_layout 分支 | 显示该应用把 SYSTEM_ALERT_WINDOW、PACKAGE_USAGE_STATS、自启动也用同一套截图教学串起来，属系统性权限堆叠 | 含 pop_notice_read、usage_access 截图与 confirm 按钮；标题为 MIUI 悬浮窗相关文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.appativesh.masterclean.process.ProcessManagerActivity#onClick`
- `com.appativesh.masterclean.AccessTipActivity#onCreate`
- `com.appativesh.masterclean.AccessTipActivity#a`
- `res/layout/activity_access_tip.xml`
- `res/xml/phone_accessibility.xml`
- `res/values/strings.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

已完成定向核验（无障碍服务声明、跳转点、引导层布局/图片、字符串与多入口调用）。以下为结论。

## 分析结论要点

- **权限申请路径为纯原生 Activity + 半透明遮罩，无 WebView、无远端页面**：入口在进程管理页 `ProcessManagerActivity` 的按钮点击里，先 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))` 跳到系统无障碍列表，随后立刻用 `AccessTipActivity.a(this,"accessibilityServiceAccess")` 压上一个**90% 黑底（`#bb000000`）的全屏半透明 Activity**，叠在系统设置页之上做两步图示指引。
- **引导载体是图片，不是文字**：`activity_access_tip.xml` 中 `rl_accessibilityService_layout` 用 `access_guide_step_01`/`access_guide_step_02`/`access_arrow` 三张图 + 极短文字「Please enter / Master Cleanner / off」「Turn the feature on」组合，构成"进列表 → 找到 Master Cleanner → 打开开关"的分步教学；同一布局还用 `open_window_layout`（小米 MIUI 悬浮窗引导 `pop_notice_read`）、`usage_Access_layout`（`usage_access` 图）、`boot_start_layout` 承载另外三项受限权限的同类教学。
- **遮罩可被一次点击关掉（无死循环证据）**：`AccessTipActivity.onTouchEvent` 与两个按钮 `onClick` 都只调 `finish()`；未在 `AccessTipActivity` 中发现 `onResume` 重跳。但 `applock.activity.c/e/g/u/w`、`floatingwindow.aa`、`fragment.af` 等 8 处 `run()` 都调用 `AccessTipActivity.a(...)`，说明多个业务页会**在功能使用时反复拉起同一引导层**（属按需重复施压，非证实定时死循环）。
- **身份与权限声明不匹配**：系统无障碍列表显示名与桌面名同为 `Master Cleanner`（"Cleaner" 拼错），`android:description` 仅称"帮你停止不必要的应用、不收集任何信息"，而服务实际声明 `canRetrieveWindowContent="true"` + `typeWindowStateChanged`，类内持有 `WindowManager`、`MyDesktopLayout` 悬浮窗、`Handler`、`BroadcastReceiver` 并实现 `onAccessibilityEvent/onStart`——说明文字远小于实际能力（隐私承诺 + 用途窄化）。
- **话术辅助**：`strings.xml` 另有 `dialog_dis_01`"More than 80% of users enable this feature."（从众施压）。
- **可见性**：本链路（跳转、遮罩、布局、图片、字符串）全部静态可见，未见加壳/密文/远端 HTML；唯一"不可静态读取"的是图片内的图示文案，需 OCR/截图。
- 说明：受本轮 14 次调用上限约束，未继续逐行核验 `MyAccessibilityService` 获权后的 `GLOBAL_ACTION` 反撤权逻辑，也未写入风险台账（该部分依据预筛线索与类结构，标注为判断而非证实）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导链路（ProcessManagerActivity 点击 -> ACCESSIBILITY_SETTINGS 跳转 -> AccessTipActivity 半透明遮罩 -> activity_access_tip.xml 图示）全部为明文 DEX 与资源，无加壳、无 AES 密文、无远端 HTML。仅图示内容以 PNG（access_guide_step_01/02、access_arrow、pop_notice_read、usage_access）承载，文本不可静态读取；获权后 MyAccessibilityService 内 GLOBAL_ACTION 反撤权细节本轮未逐行核验。",
  "summary_one_liner": "清理工具在进程管理页点击后先跳系统无障碍列表、再立刻压上 90% 黑底半透明图示遮罩，用两张步骤图教学开启 Master Cleanner 无障碍服务，并以'不收集任何信息''80% 用户已开启'话术降低戒心，多个业务页会反复拉起同一引导。",
  "disguise_identity": {
    "app_display_name": "Master Cleanner",
    "claimed_brand_or_persona": "Master Cleanner（手机清理/进程管理工具，声称'帮你停止不必要的应用且不收集任何信息'）",
    "a11y_service_label": "Master Cleanner",
    "identity_mismatch": true,
    "obfuscation_tricks": "品牌名拼写异常（Cleanner 而非 Cleaner）；无障碍用途声明窄化（只说'停止不必要的应用/不收集信息'），而服务实际声明 canRetrieveWindowContent=true、监听 typeWindowStateChanged，并在类内持有 WindowManager + MyDesktopLayout 悬浮窗与 BroadcastReceiver；AccessTipActivity 使用 Theme.Translucent.NoTitleBar + #bb000000 全屏遮罩叠在系统设置页之上，使系统无障碍界面处于半遮挡状态；未发现空白/换行挤出警告、同形字、多 activity-alias 或伪造 isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.appativesh.masterclean.PIPCleanerMainActivity（LAUNCHER，label=@string/my_app_name）",
      "trigger_event": "onCreate / LAUNCHER 图标点击",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Master Cleanner",
      "shown_text_zh": "桌面与启动页显示的应用名：Master Cleanner",
      "user_action_requested": "正常进入清理工具主界面",
      "code_anchor": "com.appativesh.masterclean.PIPCleanerMainActivity（AndroidManifest.xml application/activity 声明）"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "com.appativesh.masterclean.process.ProcessManagerActivity（Theme.Translucent.NoTitleBar）",
      "trigger_event": "用户进入进程/后台应用管理功能，点击 id=2131165606 的按钮触发 onClick",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（按钮文案取自布局资源，未逐字核验）",
      "shown_text_zh": "进程管理页中的一键加速/清理按钮",
      "user_action_requested": "点击清理按钮（无取消按钮，点击即进入引导）",
      "code_anchor": "com.appativesh.masterclean.process.ProcessManagerActivity#onClick"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "onClick 中 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))，随后紧接 k(); g(); AccessTipActivity.a(this, \"accessibilityServiceAccess\")",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Master Cleanner uses accessibility features to help you stop unnecessary app(s). We do not collect any information",
      "shown_text_zh": "系统无障碍服务列表中 Master Cleanner 条目的说明：使用无障碍功能帮你停止不必要的应用，我们不收集任何信息",
      "user_action_requested": "在系统列表中查找并开启 Master Cleanner 服务（用户须自行点击开关）",
      "code_anchor": "com.appativesh.masterclean.process.ProcessManagerActivity#onClick / res/xml/phone_accessibility.xml（android:description=@string/accessibility_service_description）"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.appativesh.masterclean.AccessTipActivity（Theme.Translucent.NoTitleBar，背景 #bb000000 全屏半透明）",
      "trigger_event": "AccessTipActivity.a(Context,\"accessibilityServiceAccess\") -> onCreate 读取 operationType，命中 accessibilityServiceAccess 后调用 d() 将 rl_accessibilityService_layout 置为可见",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Please enter  Master Cleanner  off / Master Cleanner Turn the feature on",
      "shown_text_zh": "遮罩上分两步的图示教学：第一步「进入 [Master Cleanner]（当前状态 off）」并配 access_guide_step_01 截图与箭头；第二步「把该功能打开」配 access_guide_step_02 截图，指示用户在系统页里打开开关",
      "user_action_requested": "按图示在下方系统无障碍页点击 Master Cleanner 开关；点击遮罩任意位置或按钮即 finish() 关闭遮罩（无'跳过/取消'文案，但可单击穿透式关闭）",
      "code_anchor": "com.appativesh.masterclean.AccessTipActivity#onCreate / #d / res/layout/activity_access_tip.xml（@id/rl_accessibilityService_layout）"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "AccessTipActivity（由 applock.activity.c/e/g/u/w#run、floatingwindow.aa#run、fragment.af#run 等入口再次调用 AccessTipActivity.a）",
      "trigger_event": "各业务页 Runnable#run 中再次执行 AccessTipActivity.a(context, operationType)",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无新增文案（复用同一遮罩布局）",
      "shown_text_zh": "未开启无障碍时，用户后续使用其它功能会被再次弹出同一引导遮罩",
      "user_action_requested": "再次按图示去开启无障碍；遮罩本身仍可单击关闭（未发现 onResume 强制重跳或定时器死循环）",
      "code_anchor": "com.appativesh.masterclean.AccessTipActivity#a / com.appativesh.masterclean.applock.activity.c#run / com.appativesh.masterclean.fragment.af#run"
    },
    {
      "step": 6,
      "stage": "跳受限设置（同类并行引导）",
      "screen_or_component": "AccessTipActivity 的 open_window_layout（小米 MIUI 悬浮窗引导）、usage_Access_layout（使用情况访问）、boot_start_layout（自启动）",
      "trigger_event": "AccessTipActivity.a(ctx,\"openWindowAccess\"/\"openUsageAccess\"/\"bootStartAccess\") -> onCreate 调 e()/c()/b() 显示对应布局",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "xiaomi_open_window_title / xiaomi_open_window_content / xiaomi_open_window_explain / usage_access_last_step_tip / confirm",
      "shown_text_zh": "以截图（pop_notice_read、usage_access）教学在 MIUI 中开启'显示悬浮窗'、'使用情况访问'与自启动权限，配'确认'按钮",
      "user_action_requested": "按截图在系统/厂商设置中逐项允许悬浮窗、使用情况访问、自启动",
      "code_anchor": "res/layout/activity_access_tip.xml（@id/open_window_layout、@id/usage_Access_layout、@id/boot_start_layout） / com.appativesh.masterclean.AccessTipActivity#e / #c / #b"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "com.appativesh.masterclean.process.MyAccessibilityService（onServiceConnected / onStart / onAccessibilityEvent，持有 WindowManager + MyDesktopLayout）",
      "trigger_event": "系统绑定服务后 onServiceConnected/onStart；之后窗口状态变化（typeWindowStateChanged）触发 onAccessibilityEvent",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（本步界面由运行时悬浮窗动态构建）",
      "shown_text_zh": "获权后在窗口切换时叠加自定义悬浮视图并执行进程清理/拦截动作",
      "user_action_requested": "无需用户操作（后台自动执行）",
      "code_anchor": "com.appativesh.masterclean.process.MyAccessibilityService#onStart / #onAccessibilityEvent（字段 WindowManager g、MyDesktopLayout e、Handler o、BroadcastReceiver p）"
    }
  ],
  "text_presentation_locations": [
    "res/xml/phone_accessibility.xml 的 android:description -> 系统无障碍服务列表条目下方的说明文字（@string/accessibility_service_description）",
    "AccessTipActivity 全屏半透明遮罩（#bb000000）内的 rl_accessibilityService_layout：'Please enter'+@string/my_app_name+'off'、@string/my_app_name+'Turn the feature on'，并叠放 access_guide_step_01/access_guide_step_02 图示与 access_arrow 箭头",
    "同一遮罩布局 open_window_layout：xiaomi_open_window_title/content/explain + pop_notice_read 截图 + 'confirm' 按钮",
    "同一遮罩布局 usage_Access_layout：usage_access 截图 + usage_access_last_step_tip",
    "同一遮罩布局 boot_start_layout：自启动引导文案（复用 confirm）",
    "res/values/strings.xml 中 dialog_dis_01：'Master Cleanner uses accessibility features to help you stop unnecessary app(s). More than 80% of users enable this feature.'（弹窗类话术资源，具体弹出位置本轮未逐处核验）",
    "assets/help/help_english_v1_0_7.html 与 assets/help/help_v1_0_7.html：本地 HTML 帮助页（标题为 AppLocker/AppLocker常见问题），未承载无障碍引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Master Cleanner uses accessibility features to help you stop unnecessary app(s). We do not collect any information",
      "text_zh": "Master Cleanner 使用无障碍功能来帮你停止不必要的应用。我们不收集任何信息。",
      "source_location": "res/values/strings.xml key=accessibility_service_description（经 res/xml/phone_accessibility.xml 的 android:description 呈现于系统无障碍列表）",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "en",
      "text_verbatim": "Master Cleanner uses accessibility features to help you stop unnecessary app(s). More than 80% of users enable this feature.",
      "text_zh": "Master Cleanner 使用无障碍功能来帮你停止不必要的应用。超过 80% 的用户都开启了此功能。",
      "source_location": "res/values/strings.xml key=dialog_dis_01",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enter",
      "text_zh": "请进入（配应用名与 'off' 状态，指示在系统列表中找到该应用）",
      "source_location": "res/values/strings.xml key=access_tip_step_01（用于 res/layout/activity_access_tip.xml 遮罩第一步）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "off",
      "text_zh": "关闭（显示当前服务处于关闭状态，制造待办压力）",
      "source_location": "res/values/strings.xml key=access_off",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Turn the feature on",
      "text_zh": "把该功能打开（第二步图示，指示点击系统开关）",
      "source_location": "res/values/strings.xml key=access_tip_step_02",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "zh",
      "text_verbatim": "AppLocker常见问题",
      "text_zh": "AppLocker 常见问题（本地帮助页标题，功能定位为应用锁）",
      "source_location": "assets/help/help_v1_0_7.html",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "user_feature_on_demand",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "AccessTipActivity 自身无 onResume 重跳、无定时器（onTouchEvent/按钮 onClick 均只 finish()）；但 applock.activity.c/e/g/u/w、floatingwindow.aa、fragment.af 共 8 处 Runnable#run 会再次调用 AccessTipActivity.a(ctx, operationType)，因此用户每次使用相关功能都会被重新压上同一引导遮罩，形成按需重复施压。",
    "overlay_or_fake_settings": "叠放 90% 黑底（#bb000000）全屏半透明 Activity（Theme.Translucent.NoTitleBar）覆盖在系统 ACCESSIBILITY_SETTINGS 页之上，用两张真实系统截图（access_guide_step_01/02）+ 箭头做分步指引；不是高仿系统开关页，而是真实系统页 + 遮罩指引。",
    "restricted_settings_13plus_coaching": "无。未发现跳 ACTION_APPLICATION_DETAILS_SETTINGS 或 'Allow restricted settings' 菜单教学，也未发现 Session 安装器绕过（targetSdkVersion=22，运行于旧策略环境）。",
    "post_grant_anti_removal": "本轮未逐行核验。依据类结构，MyAccessibilityService 持有 WindowManager、MyDesktopLayout、Handler 与 BroadcastReceiver，并实现 onAccessibilityEvent/onStart；预筛线索显示存在 PERFORM_GLOBAL_ACTION、WATCH_SETTINGS、WATCH_PKG_INSTALLER 等行为标记，指向获权后监听设置页并可能用全局返回/主页阻止撤权，具体实现待验证。",
    "benign_graceful_degradation": "无。除遮罩可单击关闭外，未见手动模式、仅观看模式或明确的功能降级路径说明。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 ProcessManagerActivity#onClick（id=2131165606）触发瞬间拉起 UTG，并持续跟踪随后 2~3 秒的窗口栈：应先后看到 android.settings.ACCESSIBILITY_SETTINGS 与 com.appativesh.masterclean/.AccessTipActivity 两个窗口叠加；另可在 Activity 启动参数 operationType=accessibilityServiceAccess 上直接命中。",
    "key_pages_to_capture": [
      {
        "page_role": "设置页后压栈遮罩页（核心诱导界面）",
        "page_identifier": "com.appativesh.masterclean/.AccessTipActivity，主题 Translucent、背景 #bb000000，含 access_guide_step_01/02 两张截图与 access_arrow",
        "why_most_useful": "此页同时证明'跳系统设置'与'叠加图文教学'两个动作在同一时序内发生，是判定诱导开启无障碍的决定性画面",
        "observable_utg_signals": [
          "窗口栈中 AccessTipActivity 位于 ACCESSIBILITY_SETTINGS 之上",
          "遮罩半透明，可见下层系统无障碍列表",
          "遮罩内仅极短文字（Please enter / off / Turn the feature on），主要信息在图片中"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载/已安装的服务，条目名 Master Cleanner，说明为'...We do not collect any information'",
        "why_most_useful": "核对身份与声明：显示名与服务名一致但用途声明窄化，且条目名拼写为 Cleanner",
        "observable_utg_signals": [
          "服务条目文本 Master Cleanner",
          "说明文字含 'We do not collect any information' 隐私承诺",
          "开关初始为 off"
        ]
      },
      {
        "page_role": "同类受限权限引导页（悬浮窗/使用情况/自启动）",
        "page_identifier": "AccessTipActivity 的 open_window_layout / usage_Access_layout / boot_start_layout 分支",
        "why_most_useful": "显示该应用把 SYSTEM_ALERT_WINDOW、PACKAGE_USAGE_STATS、自启动也用同一套截图教学串起来，属系统性权限堆叠",
        "observable_utg_signals": [
          "含 pop_notice_read、usage_access 截图与 confirm 按钮",
          "标题为 MIUI 悬浮窗相关文案"
        ]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "遮罩内的关键引导几乎全部为 PNG 截图（access_guide_step_01/02、access_arrow、pop_notice_read、usage_access），UTG 文本节点极少，纯文本检测易漏；需配合截图 + OCR 或图像相似度。另获权后的反撤权行为发生在系统设置页上下文，UTG 需持续监测窗口栈变化与 GLOBAL_ACTION 回退事件才能捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.appativesh.masterclean.process.ProcessManagerActivity#onClick",
    "com.appativesh.masterclean.AccessTipActivity#onCreate",
    "com.appativesh.masterclean.AccessTipActivity#a",
    "res/layout/activity_access_tip.xml",
    "res/xml/phone_accessibility.xml",
    "res/values/strings.xml"
  ]
}
```

</details>
