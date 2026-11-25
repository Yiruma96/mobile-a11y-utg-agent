# MB_165__1773556f99｜Unattributed — VideoZapisDTP

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：143.6s

## 1. 一句话核心结论

- **核心申请方式**：冷启动强制进入不可返回的原生卡片式分步授权向导，用俄语'保障应用稳定运行'为名把无障碍与短信/VPN/通知使用权并列索要，未授权则 onResume 反复重弹同一卡片，获权后无障碍服务持续把用户从设置/安装器/权限页踢回桌面以阻止撤权卸载。
- **静态可见性说明**：无障碍引导全链路（MainActivity→OnboardingActivity 卡片机→ACCESSIBILITY_DETAILS_SETTINGS/ACCESSIBILITY_SETTINGS 跳转→GuardAccessibilityService 反卸载）均静态可见；界面文案以 XOR 加密字节数组硬编码在 dex 中，跳转 Action 与 extra 已通过 ۟ۤۡۡ.decode 算法解密确认。唯一缺省项是 assets/onboarding_stealer.html 未被打包（运行时探测失败即回退原生卡片），故 WebView 版引导页文本无法静态获得。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_FEATURE_ON_DEMAND`（用户主动进入具体功能/设置后按需触发）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1773556f99489337e6152d3736ab4f0b8df56c47501b8ef10145a4cb7d3baa94` |
| 包名 / 年份 | `com.devstudio.reader` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | VideoZapisDTP |
| 引导页宣称品牌/身份 | 视频录制工具（获权后主界面伪装为 rutube.ru 视频站） |
| 系统无障碍列表服务名 | 无 label（系统列表仅显示应用名 VideoZapisDTP） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务未声明 android:isAccessibilityTool，无 label 仅有俄语 description；settingsActivity 指向不存在的 com.app.shadow.OnboardingActivity；同时声明 HiddenAlias(启用) 与 VisibleAlias(禁用) 两个 LAUNCHER activity-alias 配合 HIDE_ICON 开关做图标隐藏；OnboardingActivity 对全部 AppTask 调 setExcludeFromRecents(true)；所有界面文案 XOR 加密，字符串不以明文出现 |
| 无障碍服务类名 | `com.base.template.services.GuardAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |
| 系统设置项说明 (`android:description`) | Служба специальных возможностей для стабильной работы приложения. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.base.template.MainActivity → com.base.template.OnboardingActivity | LAUNCHER 启动 MainActivity.onCreate；SharedPreferences("setup").getBoolean("done", false)==false 时 startActivity(OnboardingActivity) 并 finish() | 原生Activity | **原文**：无（纯跳转，无可见文案）<br>**译注**：无界面，直接跳转引导页 | 无需操作；无取消/跳过入口 | `com.base.template.MainActivity.onCreate / com.base.template.OnboardingActivity.onCreate` |
| 2 | 引导说明页 | OnboardingActivity 根 FrameLayout（黑色背景 -16777216）+ 全屏 WebView + blocker View + 底部 cardContainer | OnboardingActivity.onCreate：先 getAssets().open("onboarding_stealer.html") 探测；抛异常则走原生卡片分支，创建 cardContainer(FrameLayout, gravity=80, bottomMargin=24dp) | 原生Activity | **原文**：无（外层 WebView 加载 OnboardingConfig.WEBVIEW_URL，默认 https://www.google.com；原生分支为空白底 + 底部卡片）<br>**译注**：黑底页面上盖一层全屏可点击拦截层，底部预留卡片区域 | 无法滑动/返回，必须等卡片出现并点击卡片按钮 | `com.base.template.OnboardingActivity.onCreate` |
| 3 | 引导说明页 | StealerCard 卡片 #1（id=post_notifications）：LinearLayout 圆角卡（cornerRadius 24dp、elevation 16dp）+ 自绘铃铛图标 + 标题/副标题 TextView + 渐变按钮 TextView | buildCards$2.invoke case 5 检查 hasNotifAccess()，未授权则 startActivity(ACTION_NOTIFICATION_LISTENER_SETTINGS) | 原生Activity | **原文**：Для доступа к данному ресурсу<br>**译注**：「要访问此资源」（按钮文案；标题/副标题为 XOR 加密字符串，运行期解密，未逐字还原） | 点击卡片按钮进入通知使用权设置页；无跳过按钮 | `com.base.template.OnboardingActivity.onCreate / OnboardingActivity$buildCards$2#invoke(case 5) / strings r_pbgbybmjjknf(Enable)` |
| 4 | 跳受限设置 | 系统页：默认短信应用选择器 + 短信运行时权限对话框（requestPermissions code 9990/9988/9991） | buildCards$2 case 2/4：isDefaultSms() 为假则 requestPermissions(含 SEND_SMS/READ_SMS/READ_CONTACTS/CALL_PHONE 等) + ACTION_CHANGE_DEFAULT(sms)；为真则直接弹运行时权限 | 系统无障碍页 | **原文**：无（系统原生权限对话框，应用侧无自定义文案）<br>**译注**：系统默认短信应用选择与短信/通讯录/电话权限授权弹窗 | 选择本应用为默认短信应用并允许短信/通讯录/通话权限 | `com.base.template.OnboardingActivity$buildCards$2#invoke(case 2) / OnboardingActivity.withFwdPerms` |
| 5 | 跳受限设置 | 系统页：REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 电池优化白名单；厂商自启动管理页（OemAutoStart.resolve）；VpnService.prepare 授权对话框 | buildCards$2 case 2(autostart：OemAutoStart.resolve 命中则 startActivity 并置 autostartOpened=true)、case 3/4(VpnService.prepare → startActivityForResult 1002) | 系统无障碍页 | 无 | 允许忽略电池优化、开启自启动、同意 VPN 授权 | `com.base.template.OnboardingActivity$buildCards$2#invoke(case 3,4) / OnboardingConfig.PERM_BATTERY_ENABLED` |
| 6 | 跳无障碍设置 | 系统页：android.settings.ACCESSIBILITY_DETAILS_SETTINGS（带 android.intent.extra.COMPONENT_NAME=com.base.template.services.GuardAccessibilityService 的 flattenToString） | buildCards$2 case 8：Headers$Companion.isEnabled() 为假 → new Intent(ACTION_ACCESSIBILITY_DETAILS_SETTINGS).addFlags(FLAG_ACTIVITY_NEW_TASK).putExtra(EXTRA_COMPONENT_NAME, componentName)；捕获异常后回退 Intent(ACTION_ACCESSIBILITY_SETTINGS).addFlags(0x14000000) 并额外塞 :settings:fragment_args_key / :settings:show_fragment_args(Bundle) 等 ROM 专用 extra | 系统无障碍页 | **原文**：Служба специальных возможностей для стабильной работы приложения.<br>**译注**：「用于保障应用稳定运行的特殊能力服务」（该文案作为系统无障碍列表/详情页中的服务说明展示） | 在系统无障碍页找到 VideoZapisDTP 服务并打开开关（无应用内说明页、无取消入口） | `com.base.template.OnboardingActivity$buildCards$2#invoke(case 8) / res/xml/r_pvbqgtrefwgj.xml` |
| 7 | 拒权反馈循环 | OnboardingActivity.onResume → showNextCard() 重绘同一 StealerCard | 从系统设置页返回触发 onResume：checkGranted.invoke() 为假 → 不推进（return）；advanceCard() 后 showNextCard()→skipGranted() 亦不会跳过未授权卡片，4500ms 后 OnboardingActivity$$ExternalSyntheticLambda12 再次 advanceCard；autostart 卡片另在 onResume 中写 SharedPreferences 后 400ms 强制 advanceCard | 原生Activity | **原文**：无（重复展示同一张卡片）<br>**译注**：拒绝授权后回到应用即重新弹出同一张权限卡片，无跳过/放弃路径 | 只能继续点击卡片按钮重新跳设置，或按 Home 退出（返回键已被 onBackPressed 空实现屏蔽） | `com.base.template.OnboardingActivity#onResume / #skipGranted / #showNextCard / #onBackPressed` |
| 8 | 获权后动作 | OnboardingActivity.finalizeSetup() → CommandService(:g 之外主进程) + GuardianService(:g) + StealthVpnService + GuardAccessibilityService 生效 | 所有卡片 checkGranted 通过后 skipGranted 越过末尾 → finalizeSetup：写 SharedPreferences("setup").putBoolean("done", true)、blocker/cardContainer alpha→0 隐藏、safeStartService(CommandService)、CallForwardHelper.schedule()；此后 MainActivity 走 WebView 加载 rutube.ru 伪装视频站 | 原生Activity | **原文**：无（界面淡出，转入伪装视频站）<br>**译注**：引导页淡出，应用转为正常视频界面，后台服务接管 | 无；用户此时已交出无障碍+短信+通话+通知使用权 | `com.base.template.OnboardingActivity#finalizeSetup / com.base.template.MainActivity#onCreate` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍列表/详情页：android:description = "Служба специальных возможностей для стабильной работы приложения."（res/values/strings.xml r_wwvyyvwokopz，经 res/xml/r_pvbqgtrefwgj.xml 引用）
- OnboardingActivity 底部原生卡片：StealerCard.title / StealerCard.subtitle（XOR 加密字符串运行期解密后 setText，位于程序化构建的 LinearLayout 卡片内）
- 卡片按钮 TextView："Для доступа к данному ресурсу"（XOR 加密硬编码，OnboardingActivity.showNextCard 内）
- stealer mode 分支：WebView 加载 file:///android_asset/onboarding_stealer.html，卡片内容经 evaluateJavascript("showCard('" + JSON + "')") 注入（本样本该 HTML 未打包）
- 外层背景 WebView：OnboardingConfig.WEBVIEW_URL，默认 https://www.google.com（仅作背景/掩护，无引导文案）
- 获权后主界面：MainActivity WebView 加载 https://rutube.ru（伪装视频站）
- strings.xml 中 Google Play services 系列文案（%1$s won't work unless you enable Google Play services. 等）为 GMS 依赖库资源，非本应用引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| ru | Служба специальных возможностей для стабильной работы приложения. | 用于保障应用稳定运行的特殊能力服务。 | `res/values/strings.xml key=r_wwvyyvwokopz（被 res/xml/r_pvbqgtrefwgj.xml android:description 引用）` | 假更新 |
| ru | Для доступа к данному ресурсу | 要访问此资源 | `硬编码 XOR 字符串，OnboardingActivity.showNextCard（卡片按钮文案）` | 受限设置分步教学 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 在启用 Google Play 服务之前无法工作。 | `res/values/strings.xml key=r_tlvpriizjfwa（Google Play services 资源库，非应用自身引导文案）` | 良性透明说明 |
| en | Enable Google Play services | 启用 Google Play 服务 | `res/values/strings.xml key=r_ijjuiqjnodel（Google Play services 资源库）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：从系统设置页返回触发 OnboardingActivity.onResume，若当前卡片 checkGranted 为假则直接 return 不推进；advanceCard/showNextCard/skipGranted 只会跳过已授权卡片，未授权卡片被无限重绘（WebView 分支固定 4500ms 定时器推进、autostart 卡片 400ms 强制推进），形成拒权即重弹的闭环；返回键被 onBackPressed() 空实现屏蔽
- **遮罩叠层 / 高仿系统设置页**：不使用半透明遮罩叠在系统设置页上，也不伪造系统开关页；改为在自有 OnboardingActivity 内用全屏可点击 blocker View 阻断交互、底部叠加自绘权限卡片，卡片按钮直接 startActivity 跳真实系统无障碍页
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未出现教用户进入应用详情页允许受限设置的分步教学，也未使用 Session 安装器绕过（ACCESSIBILITY_DETAILS_SETTINGS 在 targetSdk 34 下受限时以 ACCESSIBILITY_SETTINGS + :settings:fragment_args_key 多 extra 兜底重试）
- **获权后即时行为与防撤权机制**：有。GuardAccessibilityService.onAccessibilityEvent 监听 typeWindowStateChanged/typeWindowContentChanged，命中 com.android.settings 及 40+ 厂商设置/安全中心/权限管理/应用管理包名、packageinstaller、uninstall/uninstaller、permissioncontroller 等即调用 blockAndGoHome()：performGlobalAction(GLOBAL_ACTION_HOME) 后在 50/100/180ms 再连发三次（400ms 节流），把用户从设置页/卸载页踢回桌面；对 com.android.vending 额外检查类名含 appdetail/finsky 且节点同时含本应用名与 uninstall 文本时才拦截
- **良性降级 / 替代方案**：无。未提供任何手动模式、仅观看模式或跳过授权的降级路径，未授权即卡死在引导页

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 com.base.template.MainActivity 后立刻出现 com.base.template.OnboardingActivity（首帧即黑底+底部卡片，无需任何用户操作）；或以 Intent action 为 android.settings.ACCESSIBILITY_DETAILS_SETTINGS / android.settings.ACCESSIBILITY_SETTINGS 且 extra COMPONENT_NAME 指向 GuardAccessibilityService 的跳转作为拉起时刻
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：卡片标题/副标题为 XOR 加密字符串，须在运行期（卡片绘制后）用 UTG 读取文本节点才能获得明文话术，纯静态只能拿到按钮文案；assets/onboarding_stealer.html 未打包，WebView 版引导页在本样本中不可达，若样本带该 HTML 则引导话术会整体迁入本地 HTML（UTG 需读取 WebView 无障碍节点）。应用未加壳、无 VMP，不构成运行期观测盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动分步授权卡片页（无障碍卡片所在轮次）** | com.base.template.OnboardingActivity 窗口，底部圆角卡片含图标+两行标题+渐变按钮，全屏无返回箭头 | 这是应用唯一呈现无障碍索取理由的界面，可直接判定是否为无正当业务理由的强制授权向导 | 卡片标题/副标题文本（运行期解密后可见明文，是唯一能拿到真实诱导话术的位置）；卡片按钮文本 'Для доступа к данному ресурсу'；是否存在跳过/关闭按钮（预期无）；无障碍卡片与短信/通知/VPN/电池卡片是否串成同一序列 |
| **跳转前无障碍卡片点击瞬间** | OnboardingActivity 内按钮点击 → 系统 ACCESSIBILITY_DETAILS_SETTINGS 详情页（直接定位到 GuardAccessibilityService） | 确认应用是否用 COMPONENT_NAME 直跳详情页、避免用户在列表中看到其他服务，并核对服务说明文案 | 系统无障碍详情页显示的服务名与说明 'Служба специальных возможностей для стабильной работы приложения.'；系统是否弹出'此服务可查看屏幕内容/敏感数据'警告；跳转是否附带 :settings:fragment_args_key 等 ROM 专用参数 |
| **拒权返回后的重弹循环页** | 从系统设置返回后 400ms 内重现的同一张 OnboardingActivity 卡片 | 区分良性一次性引导与强制循环诱导，是判定 coercion 的关键运行期证据 | 返回后是否仍停留在同一卡片（预期不推进）；onResume 后 400ms 卡片是否重新绘制；连续三次拒绝后是否仍无跳过入口 |
| **获权后反卸载拦截页** | 系统设置→应用详情/卸载确认页、com.android.vending 应用详情页，被 performGlobalAction(HOME) 弹回桌面 | 证明无障碍权限的真实用途是阻碍用户撤权与卸载，而非'保障稳定运行' | 进入设置应用详情页后 <200ms 被强制回到桌面；连续 3 次 HOME 动作（50/100/180ms 间隔）；打开应用商店详情页同样被踢出 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.base.template.OnboardingActivity$buildCards$2#invoke`
- `com.base.template.OnboardingActivity#onResume`
- `com.base.template.OnboardingActivity#onCreate`
- `com.base.template.services.GuardAccessibilityService#onAccessibilityEvent`
- `com.base.template.services.GuardAccessibilityService#blockAndGoHome`
- `res/xml/r_pvbqgtrefwgj.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，已收敛）

**核心判断：这是一个典型的俄语系短信/通话窃取型木马，通过冷启动即触发的分步授权向导（原生卡片式 onboarding）逐项索取高危权限，无障碍只是其中一环；获权后用无障碍服务阻止用户卸载、改权限。**

1. **入口强制**：[MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.base.template.MainActivity#onCreate>) 检查 `setup/done`，未完成则直接 `startActivity(OnboardingActivity)` 并 `finish()`，无主界面可回退；同时对所有 AppTask 调 `setExcludeFromRecents(true)` 隐藏最近任务。
2. **向导载体双形态**：[OnboardingActivity.onCreate()](<resource-unit:#1.dex1 code:com.base.template.OnboardingActivity#onCreate>) 先探测 `assets/onboarding_stealer.html` 是否存在（本样本 assets 目录为空，探测失败），存在则走"stealer mode"——透明 WebView 加载 `file:///android_asset/onboarding_stealer.html` 并注册 `Android.onGrantClicked()/getLocale()` 桥；否则走原生卡片分支（`FrameLayout cardContainer` + 程序化 `StealerCard` 卡片）。所有界面字符串经 [ۧۢ.۟ۤۡۡ.decode()](<resource-unit:#1.dex1 code:ۧۢ.۟ۤۡۡ#decode>) XOR 加密。
3. **不可取消、不可返回**：`onBackPressed()` 为空实现；全屏 `blocker` View 覆盖 WebView 且 `clickable/focusable`，未点击卡片无法交互。
4. **无障碍跳转精确还原**（解密确认）：卡片 case 8 先用 `Headers$Companion.isEnabled()` 检查，未启用则发 `android.settings.ACCESSIBILITY_DETAILS_SETTINGS` + `android.intent.extra.COMPONENT_NAME` = `com.base.template.services.GuardAccessibilityService` 的 `flattenToString()`，失败回退 `android.settings.ACCESSIBILITY_SETTINGS` + `:settings:fragment_args_key`（多套 extra 兜底适配不同 ROM）。
5. **拒绝后循环**：`onResume` 中 `checkGranted` 为真才 400ms 后 `advanceCard()`；未授权则 `showNextCard()` 重新展示同一卡片，永不跳过。
6. **身份伪装**：桌面名 `VideoZapisDTP`（视频录制），获权后主界面加载 `https://rutube.ru` 伪装视频站；无障碍服务无 label，描述为俄语"用于应用稳定运行的特殊能力服务"；`settingsActivity` 指向不存在的 `com.app.shadow.OnboardingActivity`；另有 `HiddenAlias`/`VisibleAlias` 双 activity-alias 与 `HIDE_ICON` 开关。
7. **获权后反卸载**：[GuardAccessibilityService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.base.template.services.GuardAccessibilityService#onAccessibilityEvent>) 监控窗口变化，命中 `packageinstaller/uninstall/uninstaller/permissioncontroller/settings/securitycenter/...` 等 40+ 包名即 [blockAndGoHome()](<resource-unit:#1.dex1 code:com.base.template.services.GuardAccessibilityService#blockAndGoHome>)（`performGlobalAction(HOME)` 三次连发）；对 `com.android.vending` 还会在 `appdetail/finsky` 页面检查节点是否含本应用名+"uninstall"再拦截。
8. **最终目标**：`finalizeSetup()` 写入完成标记、启动 `CommandService`、`CallForwardHelper.schedule()`（呼叫转移），配合已申请的 `READ_SMS/SEND_SMS/CALL_PHONE/CAMERA/READ_CONTACTS` 构成短信拦截+通话转移的窃取闭环。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍引导全链路（MainActivity→OnboardingActivity 卡片机→ACCESSIBILITY_DETAILS_SETTINGS/ACCESSIBILITY_SETTINGS 跳转→GuardAccessibilityService 反卸载）均静态可见；界面文案以 XOR 加密字节数组硬编码在 dex 中，跳转 Action 与 extra 已通过 ۟ۤۡۡ.decode 算法解密确认。唯一缺省项是 assets/onboarding_stealer.html 未被打包（运行时探测失败即回退原生卡片），故 WebView 版引导页文本无法静态获得。",
  "summary_one_liner": "冷启动强制进入不可返回的原生卡片式分步授权向导，用俄语'保障应用稳定运行'为名把无障碍与短信/VPN/通知使用权并列索要，未授权则 onResume 反复重弹同一卡片，获权后无障碍服务持续把用户从设置/安装器/权限页踢回桌面以阻止撤权卸载。",
  "disguise_identity": {
    "app_display_name": "VideoZapisDTP",
    "claimed_brand_or_persona": "视频录制工具（获权后主界面伪装为 rutube.ru 视频站）",
    "a11y_service_label": "无 label（系统列表仅显示应用名 VideoZapisDTP）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务未声明 android:isAccessibilityTool，无 label 仅有俄语 description；settingsActivity 指向不存在的 com.app.shadow.OnboardingActivity；同时声明 HiddenAlias(启用) 与 VisibleAlias(禁用) 两个 LAUNCHER activity-alias 配合 HIDE_ICON 开关做图标隐藏；OnboardingActivity 对全部 AppTask 调 setExcludeFromRecents(true)；所有界面文案 XOR 加密，字符串不以明文出现"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.base.template.MainActivity → com.base.template.OnboardingActivity",
      "trigger_event": "LAUNCHER 启动 MainActivity.onCreate；SharedPreferences(\"setup\").getBoolean(\"done\", false)==false 时 startActivity(OnboardingActivity) 并 finish()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（纯跳转，无可见文案）",
      "shown_text_zh": "无界面，直接跳转引导页",
      "user_action_requested": "无需操作；无取消/跳过入口",
      "code_anchor": "com.base.template.MainActivity.onCreate / com.base.template.OnboardingActivity.onCreate"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "OnboardingActivity 根 FrameLayout（黑色背景 -16777216）+ 全屏 WebView + blocker View + 底部 cardContainer",
      "trigger_event": "OnboardingActivity.onCreate：先 getAssets().open(\"onboarding_stealer.html\") 探测；抛异常则走原生卡片分支，创建 cardContainer(FrameLayout, gravity=80, bottomMargin=24dp)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（外层 WebView 加载 OnboardingConfig.WEBVIEW_URL，默认 https://www.google.com；原生分支为空白底 + 底部卡片）",
      "shown_text_zh": "黑底页面上盖一层全屏可点击拦截层，底部预留卡片区域",
      "user_action_requested": "无法滑动/返回，必须等卡片出现并点击卡片按钮",
      "code_anchor": "com.base.template.OnboardingActivity.onCreate"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "StealerCard 卡片 #1（id=post_notifications）：LinearLayout 圆角卡（cornerRadius 24dp、elevation 16dp）+ 自绘铃铛图标 + 标题/副标题 TextView + 渐变按钮 TextView",
      "trigger_event": "buildCards$2.invoke case 5 检查 hasNotifAccess()，未授权则 startActivity(ACTION_NOTIFICATION_LISTENER_SETTINGS)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Для доступа к данному ресурсу",
      "shown_text_zh": "「要访问此资源」（按钮文案；标题/副标题为 XOR 加密字符串，运行期解密，未逐字还原）",
      "user_action_requested": "点击卡片按钮进入通知使用权设置页；无跳过按钮",
      "code_anchor": "com.base.template.OnboardingActivity.onCreate / OnboardingActivity$buildCards$2#invoke(case 5) / strings r_pbgbybmjjknf(Enable)"
    },
    {
      "step": 4,
      "stage": "跳受限设置",
      "screen_or_component": "系统页：默认短信应用选择器 + 短信运行时权限对话框（requestPermissions code 9990/9988/9991）",
      "trigger_event": "buildCards$2 case 2/4：isDefaultSms() 为假则 requestPermissions(含 SEND_SMS/READ_SMS/READ_CONTACTS/CALL_PHONE 等) + ACTION_CHANGE_DEFAULT(sms)；为真则直接弹运行时权限",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统原生权限对话框，应用侧无自定义文案）",
      "shown_text_zh": "系统默认短信应用选择与短信/通讯录/电话权限授权弹窗",
      "user_action_requested": "选择本应用为默认短信应用并允许短信/通讯录/通话权限",
      "code_anchor": "com.base.template.OnboardingActivity$buildCards$2#invoke(case 2) / OnboardingActivity.withFwdPerms"
    },
    {
      "step": 5,
      "stage": "跳受限设置",
      "screen_or_component": "系统页：REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 电池优化白名单；厂商自启动管理页（OemAutoStart.resolve）；VpnService.prepare 授权对话框",
      "trigger_event": "buildCards$2 case 2(autostart：OemAutoStart.resolve 命中则 startActivity 并置 autostartOpened=true)、case 3/4(VpnService.prepare → startActivityForResult 1002)",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "电池优化忽略、厂商自启动白名单、VPN 连接授权三个系统弹窗/页面",
      "user_action_requested": "允许忽略电池优化、开启自启动、同意 VPN 授权",
      "code_anchor": "com.base.template.OnboardingActivity$buildCards$2#invoke(case 3,4) / OnboardingConfig.PERM_BATTERY_ENABLED"
    },
    {
      "step": 6,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统页：android.settings.ACCESSIBILITY_DETAILS_SETTINGS（带 android.intent.extra.COMPONENT_NAME=com.base.template.services.GuardAccessibilityService 的 flattenToString）",
      "trigger_event": "buildCards$2 case 8：Headers$Companion.isEnabled() 为假 → new Intent(ACTION_ACCESSIBILITY_DETAILS_SETTINGS).addFlags(FLAG_ACTIVITY_NEW_TASK).putExtra(EXTRA_COMPONENT_NAME, componentName)；捕获异常后回退 Intent(ACTION_ACCESSIBILITY_SETTINGS).addFlags(0x14000000) 并额外塞 :settings:fragment_args_key / :settings:show_fragment_args(Bundle) 等 ROM 专用 extra",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Служба специальных возможностей для стабильной работы приложения.",
      "shown_text_zh": "「用于保障应用稳定运行的特殊能力服务」（该文案作为系统无障碍列表/详情页中的服务说明展示）",
      "user_action_requested": "在系统无障碍页找到 VideoZapisDTP 服务并打开开关（无应用内说明页、无取消入口）",
      "code_anchor": "com.base.template.OnboardingActivity$buildCards$2#invoke(case 8) / res/xml/r_pvbqgtrefwgj.xml"
    },
    {
      "step": 7,
      "stage": "拒权反馈循环",
      "screen_or_component": "OnboardingActivity.onResume → showNextCard() 重绘同一 StealerCard",
      "trigger_event": "从系统设置页返回触发 onResume：checkGranted.invoke() 为假 → 不推进（return）；advanceCard() 后 showNextCard()→skipGranted() 亦不会跳过未授权卡片，4500ms 后 OnboardingActivity$$ExternalSyntheticLambda12 再次 advanceCard；autostart 卡片另在 onResume 中写 SharedPreferences 后 400ms 强制 advanceCard",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（重复展示同一张卡片）",
      "shown_text_zh": "拒绝授权后回到应用即重新弹出同一张权限卡片，无跳过/放弃路径",
      "user_action_requested": "只能继续点击卡片按钮重新跳设置，或按 Home 退出（返回键已被 onBackPressed 空实现屏蔽）",
      "code_anchor": "com.base.template.OnboardingActivity#onResume / #skipGranted / #showNextCard / #onBackPressed"
    },
    {
      "step": 8,
      "stage": "获权后动作",
      "screen_or_component": "OnboardingActivity.finalizeSetup() → CommandService(:g 之外主进程) + GuardianService(:g) + StealthVpnService + GuardAccessibilityService 生效",
      "trigger_event": "所有卡片 checkGranted 通过后 skipGranted 越过末尾 → finalizeSetup：写 SharedPreferences(\"setup\").putBoolean(\"done\", true)、blocker/cardContainer alpha→0 隐藏、safeStartService(CommandService)、CallForwardHelper.schedule()；此后 MainActivity 走 WebView 加载 rutube.ru 伪装视频站",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（界面淡出，转入伪装视频站）",
      "shown_text_zh": "引导页淡出，应用转为正常视频界面，后台服务接管",
      "user_action_requested": "无；用户此时已交出无障碍+短信+通话+通知使用权",
      "code_anchor": "com.base.template.OnboardingActivity#finalizeSetup / com.base.template.MainActivity#onCreate"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍列表/详情页：android:description = \"Служба специальных возможностей для стабильной работы приложения.\"（res/values/strings.xml r_wwvyyvwokopz，经 res/xml/r_pvbqgtrefwgj.xml 引用）",
    "OnboardingActivity 底部原生卡片：StealerCard.title / StealerCard.subtitle（XOR 加密字符串运行期解密后 setText，位于程序化构建的 LinearLayout 卡片内）",
    "卡片按钮 TextView：\"Для доступа к данному ресурсу\"（XOR 加密硬编码，OnboardingActivity.showNextCard 内）",
    "stealer mode 分支：WebView 加载 file:///android_asset/onboarding_stealer.html，卡片内容经 evaluateJavascript(\"showCard('\" + JSON + \"')\") 注入（本样本该 HTML 未打包）",
    "外层背景 WebView：OnboardingConfig.WEBVIEW_URL，默认 https://www.google.com（仅作背景/掩护，无引导文案）",
    "获权后主界面：MainActivity WebView 加载 https://rutube.ru（伪装视频站）",
    "strings.xml 中 Google Play services 系列文案（%1$s won't work unless you enable Google Play services. 等）为 GMS 依赖库资源，非本应用引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "ru",
      "text_verbatim": "Служба специальных возможностей для стабильной работы приложения.",
      "text_zh": "用于保障应用稳定运行的特殊能力服务。",
      "source_location": "res/values/strings.xml key=r_wwvyyvwokopz（被 res/xml/r_pvbqgtrefwgj.xml android:description 引用）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "ru",
      "text_verbatim": "Для доступа к данному ресурсу",
      "text_zh": "要访问此资源",
      "source_location": "硬编码 XOR 字符串，OnboardingActivity.showNextCard（卡片按钮文案）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 在启用 Google Play 服务之前无法工作。",
      "source_location": "res/values/strings.xml key=r_tlvpriizjfwa（Google Play services 资源库，非应用自身引导文案）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Google Play services",
      "text_zh": "启用 Google Play 服务",
      "source_location": "res/values/strings.xml key=r_ijjuiqjnodel（Google Play services 资源库）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "从系统设置页返回触发 OnboardingActivity.onResume，若当前卡片 checkGranted 为假则直接 return 不推进；advanceCard/showNextCard/skipGranted 只会跳过已授权卡片，未授权卡片被无限重绘（WebView 分支固定 4500ms 定时器推进、autostart 卡片 400ms 强制推进），形成拒权即重弹的闭环；返回键被 onBackPressed() 空实现屏蔽",
    "overlay_or_fake_settings": "不使用半透明遮罩叠在系统设置页上，也不伪造系统开关页；改为在自有 OnboardingActivity 内用全屏可点击 blocker View 阻断交互、底部叠加自绘权限卡片，卡片按钮直接 startActivity 跳真实系统无障碍页",
    "restricted_settings_13plus_coaching": "无。未出现教用户进入应用详情页允许受限设置的分步教学，也未使用 Session 安装器绕过（ACCESSIBILITY_DETAILS_SETTINGS 在 targetSdk 34 下受限时以 ACCESSIBILITY_SETTINGS + :settings:fragment_args_key 多 extra 兜底重试）",
    "post_grant_anti_removal": "有。GuardAccessibilityService.onAccessibilityEvent 监听 typeWindowStateChanged/typeWindowContentChanged，命中 com.android.settings 及 40+ 厂商设置/安全中心/权限管理/应用管理包名、packageinstaller、uninstall/uninstaller、permissioncontroller 等即调用 blockAndGoHome()：performGlobalAction(GLOBAL_ACTION_HOME) 后在 50/100/180ms 再连发三次（400ms 节流），把用户从设置页/卸载页踢回桌面；对 com.android.vending 额外检查类名含 appdetail/finsky 且节点同时含本应用名与 uninstall 文本时才拦截",
    "benign_graceful_degradation": "无。未提供任何手动模式、仅观看模式或跳过授权的降级路径，未授权即卡死在引导页"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 com.base.template.MainActivity 后立刻出现 com.base.template.OnboardingActivity（首帧即黑底+底部卡片，无需任何用户操作）；或以 Intent action 为 android.settings.ACCESSIBILITY_DETAILS_SETTINGS / android.settings.ACCESSIBILITY_SETTINGS 且 extra COMPONENT_NAME 指向 GuardAccessibilityService 的跳转作为拉起时刻",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动分步授权卡片页（无障碍卡片所在轮次）",
        "page_identifier": "com.base.template.OnboardingActivity 窗口，底部圆角卡片含图标+两行标题+渐变按钮，全屏无返回箭头",
        "why_most_useful": "这是应用唯一呈现无障碍索取理由的界面，可直接判定是否为无正当业务理由的强制授权向导",
        "observable_utg_signals": ["卡片标题/副标题文本（运行期解密后可见明文，是唯一能拿到真实诱导话术的位置）", "卡片按钮文本 'Для доступа к данному ресурсу'", "是否存在跳过/关闭按钮（预期无）", "无障碍卡片与短信/通知/VPN/电池卡片是否串成同一序列"]
      },
      {
        "page_role": "跳转前无障碍卡片点击瞬间",
        "page_identifier": "OnboardingActivity 内按钮点击 → 系统 ACCESSIBILITY_DETAILS_SETTINGS 详情页（直接定位到 GuardAccessibilityService）",
        "why_most_useful": "确认应用是否用 COMPONENT_NAME 直跳详情页、避免用户在列表中看到其他服务，并核对服务说明文案",
        "observable_utg_signals": ["系统无障碍详情页显示的服务名与说明 'Служба специальных возможностей для стабильной работы приложения.'", "系统是否弹出'此服务可查看屏幕内容/敏感数据'警告", "跳转是否附带 :settings:fragment_args_key 等 ROM 专用参数"]
      },
      {
        "page_role": "拒权返回后的重弹循环页",
        "page_identifier": "从系统设置返回后 400ms 内重现的同一张 OnboardingActivity 卡片",
        "why_most_useful": "区分良性一次性引导与强制循环诱导，是判定 coercion 的关键运行期证据",
        "observable_utg_signals": ["返回后是否仍停留在同一卡片（预期不推进）", "onResume 后 400ms 卡片是否重新绘制", "连续三次拒绝后是否仍无跳过入口"]
      },
      {
        "page_role": "获权后反卸载拦截页",
        "page_identifier": "系统设置→应用详情/卸载确认页、com.android.vending 应用详情页，被 performGlobalAction(HOME) 弹回桌面",
        "why_most_useful": "证明无障碍权限的真实用途是阻碍用户撤权与卸载，而非'保障稳定运行'",
        "observable_utg_signals": ["进入设置应用详情页后 <200ms 被强制回到桌面", "连续 3 次 HOME 动作（50/100/180ms 间隔）", "打开应用商店详情页同样被踢出"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "卡片标题/副标题为 XOR 加密字符串，须在运行期（卡片绘制后）用 UTG 读取文本节点才能获得明文话术，纯静态只能拿到按钮文案；assets/onboarding_stealer.html 未打包，WebView 版引导页在本样本中不可达，若样本带该 HTML 则引导话术会整体迁入本地 HTML（UTG 需读取 WebView 无障碍节点）。应用未加壳、无 VMP，不构成运行期观测盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_FEATURE_ON_DEMAND",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "LURE_RESTRICTED_SETTINGS_COACHING"
  ],
  "code_anchors": [
    "com.base.template.OnboardingActivity$buildCards$2#invoke",
    "com.base.template.OnboardingActivity#onResume",
    "com.base.template.OnboardingActivity#onCreate",
    "com.base.template.services.GuardAccessibilityService#onAccessibilityEvent",
    "com.base.template.services.GuardAccessibilityService#blockAndGoHome",
    "res/xml/r_pvbqgtrefwgj.xml"
  ]
}
```

</details>
