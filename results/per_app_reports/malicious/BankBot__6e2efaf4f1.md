# MR_120__6e2efaf4f1｜BankBot — Jewels Star Classic

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：131.1s

## 1. 一句话核心结论

- **核心申请方式**：游戏外壳在后台延迟 1 分钟后弹出不可取消的"Google Service"原生对话框，仅给 OK 按钮直接把用户甩到系统无障碍设置页，同时用全屏 TYPE_SYSTEM_ALERT 假"Google service update"进度遮罩维持假更新假象，获权后由无障碍服务自动点击开关与确认按钮并连发返回键阻止撤权。
- **静态可见性说明**：全部引导逻辑静态可见。字符串仅做单字节 XOR 混淆（c.H 用 '|'/'}'、n.ALLATORIxDEMO 用 0x09/0x13，按末位交替逐字符异或），已完整还原出 'android.settings.ACCESSIBILITY_SETTINGS'、'For applications to work properly, enable Google Service!'、'Google Service'、'app.apk'、'/Download/app.apk'、'com.w8fjgwopjmv.ngfes.app'、'com.android.settings:id/main_content'、'android:id/button1' 等关键常量；无障碍说明文字位于本地 strings 资源 @string/aa，无需远端/HTML 参与。仅二阶段载荷 assets/app.apk 与外部 settingsActivity 类不在本包内，未展开。
- **命中的行为模式标签**：`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `6e2efaf4f1895d6468e8b628ce20b361635094ee39f2451689b2ef5e36c6e8ea` |
| 包名 / 年份 | `com.mygamejewelsclassic.app` / 2017 |
| 家族 / 品类 | **BankBot**（同池样本数：4） |
| 原始来源标识 | https://www.welivesecurity.com/2017/09/25/banking-trojan-returns-google-play/ |
| 桌面显示名 | Jewels Star Classic |
| 引导页宣称品牌/身份 | Google / Google Service（伪造 Google 服务更新与 Google 服务条款） |
| 系统无障碍列表服务名 | Google Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 直接写 'Google Service'；android:description 用整段真实 Google 服务条款原文充当权限说明，把索取全量无障碍权限包装成同意 Google 条款；权限引导界面用 'Google service update' + 进度条伪装系统更新；设置页目标包名使用伪 Google 风格域 com.w8fjgwopjmv.ngfes.app；所有关键字符串经单字节 XOR 混淆以躲避静态关键字检测；无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool 声明。 |
| 无障碍服务类名 | `com.mygamejewelsclassic.app.MyAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | The Services are provided by Google Inc. (“Google”), located at 1600 Amphitheatre Parkway, Mountain View, CA 94043, United States. <br> <br> By using our Services, you are agreeing to these terms. Please read them carefully. <br> <br> Our Services are very diverse, so sometimes additional terms or product requirements (including age requirements) may apply. Additional terms will be available with the relevant Services, and those additional terms become part of your agreement with us if you use those Services. <br> <br> You must follow any policies made available to you within the Services. <br> <br> Don’t misuse our Services. For example, don’t interfere with our Services or try to access them using a method other than the interface and the instructions that we provide. You may use our Services only as permitted by law, including applicable export and re-export control laws and regulations. We may suspend or stop providing our Services to you if you do not comply with our terms or policies or if we are investigating suspected misconduct. <br> <br> Using our Services does not give you ownership of any intellectual property rights in our Services or the content you access. You may not use content from our Services unless you obtain permission from its owner or are otherwise permitted by law. These terms do not grant you the right to use any branding or logos used in our Services. Don’t remove, obscure, or alter any legal notices displayed in or along with our Services. <br> <br> Our Services display some content that is not Google’s. This content is the sole responsibility of the entity that makes it available. We may review content to determine whether it is illegal or violates our policies, and we may remove or refuse to display content that we reasonably believe violates our policies or the law. But that does not necessarily mean that we review content, so please don’t assume that we do. <br> <br> In connection with your use of the Services, we may send you service announcements, administrative messages, and other information. You may opt out of some of those communications. <br> <br> Some of our Services are available on mobile devices. Do not use such Services in a way that distracts you and prevents you from obeying traffic or safety laws. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.mygamejewelsclassic.app.UnityPlayerActivity（launcher，Unity 游戏画面）+ com.mygamejewelsclassic.app.AlarM → MyIntentService | 用户点击桌面图标启动 Unity 游戏；AlarM 广播接收器 onReceive 启动 MyIntentService，后者 sleep(60s) 后触发引导 | 原生Activity | **原文**：无（游戏画面本身无可疑文案）<br>**译注**：正常消除游戏界面，无任何权限说明 | 无，用户只感知为玩游戏 | `com.mygamejewelsclassic.app.AlarM.onReceive / com.mygamejewelsclassic.app.MyIntentService.onHandleIntent` |
| 2 | 拒权反馈循环 | com.mygamejewelsclassic.app.MyIntentService（IntentService，后台启动 Main2Activity） | onHandleIntent 中 TimeUnit.MINUTES.sleep(1L) 后，检测未安装 com.w8fjgwopjmv.ngfes.app 即 startActivity(Main2Activity)，flags=268468224（NEW_TASK\|NO_ANIMATION） | 原生Activity | 无 | 无（强制弹出） | `com.mygamejewelsclassic.app.MyIntentService.onHandleIntent` |
| 3 | 引导说明页 | com.mygamejewelsclassic.app.Main2Activity（Theme.DeviceDefault.Light.Dialog.NoActionBar，系统对话框样式 Activity）内的 AlertDialog | Main2Activity.onCreate：SDK_INT>=19 且 Telephony.Sms.getDefaultSmsPackage() 不等于本包名时 show() | 原生Dialog | **原文**：Title: Google Service / Message: For applications to work properly, enable Google Service! / Button: OK<br>**译注**：标题"Google 服务"；正文"为使应用正常工作，请启用 Google 服务！"；按钮"确定" | 只能点击 OK（setCancelable(false)，无取消、无跳过、返回键无效） | `com.mygamejewelsclassic.app.Main2Activity.onCreate（strings 经 c.H 解密）` |
| 4 | 跳无障碍设置 | 系统设置页 android.settings.ACCESSIBILITY_SETTINGS | p.onClick(DialogInterface,int) 中 startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1)，随后 Main2Activity.finish() | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS<br>**译注**：系统无障碍服务列表页，其中服务项显示为 "Google Service"，说明为伪造的 Google 服务条款长文 | 要求用户在该列表中找到 "Google Service" 并打开开关（实际由无障碍服务代为点击） | `com.mygamejewelsclassic.app.p.onClick` |
| 5 | 遮罩叠层指引 | MainActivity 与 HUD 服务：WindowManager.addView(res/layout/floatingview.xml, TYPE_SYSTEM_ALERT=2003, alpha=0.75, 全屏) | MainActivity.onCreate → ALLATORIxDEMO() 挂载后 finish()，onStart 睡 3 秒 removeView；HUD.onStartCommand 收到 extra "gus" 时再次挂载（TagLayout 包裹），extra "del" 时移除 | 悬浮窗Overlay | **原文**：Google service update / Wait...<br>**译注**："Google 服务更新中" / "请稍候……"（配 ProgressBar 的假更新进度） | 无操作按钮，仅以半透明全屏浮层遮挡界面，制造系统更新/卡顿假象并压制用户操作 | `res/layout/floatingview.xml（第 4、6 行硬编码文案）/ com.mygamejewelsclassic.app.MainActivity.ALLATORIxDEMO / com.mygamejewelsclassic.app.HUD.ALLATORIxDEMO` |
| 6 | 获权后动作 | com.mygamejewelsclassic.app.MyAccessibilityService（onServiceConnected / onAccessibilityEvent） | 用户开启服务后 onServiceConnected 回调；之后每次无障碍事件（eventTypes=-1，全量）触发 onAccessibilityEvent | 系统无障碍页 | **原文**：com.android.settings:id/main_content / android:id/button1 / com.w8fjgwopjmv.ngfes.app / /Download/app.apk<br>**译注**：定位设置页主内容区与系统确认按钮，自动点击开关、自动确认对话框，并在设置页连按 3 次返回键；同时将内置 app.apk 释放到 /Download/app.apk 并拉起 MyService/MyIntent | 无需用户操作；反而通过 performGlobalAction(1) 连续返回键阻止用户退出设置页或撤销权限 | `com.mygamejewelsclassic.app.MyAccessibilityService.onServiceConnected / onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- Main2Activity 内不可取消 AlertDialog（标题 Google Service，正文 For applications to work properly, enable Google Service!，唯一按钮 OK）——这是唯一显式要求开启无障碍的文案
- 系统无障碍服务列表项：android:label="Google Service" 与 android:description="@string/aa"（整段伪造的 Google 服务条款，含 "Don't misuse our Services"、"You must follow any policies…" 等原文）
- res/layout/floatingview.xml 第 4 行 TextView 硬编码 "Google service update"、第 6 行 "Wait..."（配 ProgressBar），由 MainActivity 与 HUD 以 TYPE_SYSTEM_ALERT 全屏半透明叠放
- AndroidManifest.xml 中 service 声明 android:label="Google Service"，与应用显示名 "Jewels Star Classic" 及游戏图标形成身份错配
- res/xml/accessibility_service_config.xml：settingsActivity 指向 com.moba11y.basicaccessibilityservice.SettingsActivity，accessibilityEventTypes=typeAllMask、canRetrieveWindowContent=true

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | For applications to work properly, enable Google Service! | 为使应用正常工作，请启用 Google 服务！ | `Main2Activity.onCreate 经 c.H 解密（原文 'For applications to work properly, enable Google Service!'）` | 故障恐吓 |
| en | Google Service | Google 服务 | `Main2Activity 对话框标题（n.ALLATORIxDEMO 解密）+ AndroidManifest.xml service android:label` | 假更新 |
| en | Google service update | Google 服务更新 | `res/layout/floatingview.xml 第 4 行 TextView android:text（硬编码）` | 假更新 |
| en | Wait... | 请稍候…… | `res/layout/floatingview.xml 第 6 行 TextView android:text（硬编码）` | 假更新 |
| en | The Services are provided by Google Inc. (“Google”), located at 1600 Amphitheatre Parkway, Mountain View, CA 94043, United States. <br> <br> By using our Services, you are agreeing to these terms. Please read them carefully. <br> <br> Our Services are very diverse, so sometimes additional terms or product requirements (including age requirements) may apply. Additional terms will be available with the relevant Services, and those additional terms become part of your agreement with us if you use those Services. <br> <br> You must follow any policies made available to you within the Services. <br> <br> Don’t misuse our Services. For example, don’t interfere with our Services or try to access them using a method other than the interface and the instructions that we provide. You may use our Services only as permitted by law, including applicable export and re-export control laws and regulations. We may suspend or stop providing our Services to you if you do not comply with our terms or policies or if we are investigating suspected misconduct. | 服务由位于美国加州山景城 1600 Amphitheatre Parkway 的 Google Inc.（“Google”）提供。使用我们的服务即表示您同意这些条款，请仔细阅读。我们的服务非常多样，因此有时会适用附加条款或产品要求（包括年龄要求）。附加条款将随相关服务提供，若您使用这些服务，这些附加条款即成为您与我们协议的一部分。您必须遵守服务中提供的所有政策。请勿滥用我们的服务，例如，不要以我们提供的界面和说明之外的方式干扰或访问我们的服务。您只能在法律允许的范围内使用我们的服务，包括适用的出口和再出口管制法律法规。如果您不遵守我们的条款或政策，或我们正在调查涉嫌不当行为，我们可能会暂停或停止向您提供服务。 | `res/values*/strings.xml 中 key=aa（被 accessibility_service_config.xml 的 android:description 引用）` | 教唆忽视警告 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`background_relaunch`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：引导弹窗 setCancelable(false) 且仅一个 OK 按钮，用户无法取消；点击 OK 后直接跳系统无障碍设置并 finish 自身。若用户未开启，AlarM 广播与 MyIntentService 每轮 sleep(60s) 后再次 startActivity(Main2Activity) 重复弹出；进入设置页后无障碍服务已通过 onAccessibilityEvent 监听 com.android.settings:id/main_content，L==-1 时连发 3 次 performGlobalAction(1)（返回键）把用户压回设置页，并循环遍历节点自动点击开关与 android:id/button1 确认按钮。
- **遮罩叠层 / 高仿系统设置页**：有两层：MainActivity 与 HUD 服务分别以 TYPE_SYSTEM_ALERT(2003)、全屏尺寸、alpha=0.75 叠放 res/layout/floatingview.xml（Google service update + ProgressBar + Wait...），在跳设置前后遮挡真实界面；未发现高仿系统无障碍开关页，开关操作借用真实系统设置页并由无障碍服务代点。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=22，无 Android 13 受限设置分步教学，也无 Session 安装器说明页；相关安装绕过由无障碍服务直接代点系统安装器按钮实现）
- **获权后即时行为与防撤权机制**：有。onAccessibilityEvent 在全量事件下监听设置页主内容区，L==-1 时连续 3 次 performGlobalAction(1) 阻止用户退出设置页；同时自动点击 android:id/button1 与目标项（performAction(16)）完成开启，并在 onServiceConnected 中设置 flags=91、eventTypes=-1 以持续监听。
- **良性降级 / 替代方案**：无。未提供任何替代路径（无手动模式、无仅观看模式、无功能降级），拒权只导致无限重弹。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以 AlarM/MyIntentService 启动为起点，监测 Main2Activity（Theme.DeviceDefault.Light.Dialog.NoActionBar）首次出现在前台时立即截图；或直接 hook startActivity 出现 intent action = android.settings.ACCESSIBILITY_SETTINGS 的瞬间，在跳转前后各抓一帧（跳转前弹窗、跳转后设置页 + 半透明 'Google service update' 浮层）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：静态无壳、字符串可完整 XOR 还原，运行期 UTG 无本质盲区。需注意两点时序盲区：引导弹窗不在冷启动第 0 步出现，而由 MyIntentService 延迟 60 秒后拉起，短时启动观测易漏；'Google service update' 遮罩仅显示约 3 秒即被 removeView 移除，HUD 层需额外触发（extra "gus"）才复现，UTG 采样间隔过长会漏帧。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **引导弹窗页（冷启动后约 60 秒出现）** | Main2Activity 的 AlertDialog：标题 'Google Service'、正文 'For applications to work properly, enable Google Service!'、仅 'OK' 按钮 | 这是整个诱导链唯一显式索权文案，且不可取消、无跳过，是判断胁迫式引导与身份伪装的第一手证据 | 对话框无取消/关闭按钮；标题/正文出现 Google 品牌但应用名为 Jewels Star Classic；点击 OK 后前台立即变为系统无障碍设置页 |
| **系统无障碍服务列表项** | 设置 → 无障碍列表中的 'Google Service' 条目及其展开说明（伪造 Google 服务条款长文） | 证明服务名与说明均冒用 Google 身份，且说明文字与真实功能（读窗口内容、代点）严重不符 | 服务名 'Google Service'；说明文本为 Google 服务条款原文；开关在无用户触摸情况下自行变为开启 |
| **设置页后压栈遮罩页** | 全屏半透明白底浮层，含 'Google service update' 文本 + ProgressBar + 'Wait...' | 证明跳转设置后应用以 SYSTEM_ALERT_WINDOW 叠层伪装系统更新、压制用户操作，是恶意引导而非正常权限说明的关键区别 | 浮层覆盖系统设置界面且无按钮；浮层文本 'Google service update'/'Wait...'；浮层约 3 秒后自动消失（MainActivity onStart removeView） |
| **获权后自动代点/防撤权现场** | 无障碍设置页被连续返回键弹回、开关被自动切换；随后 /Download/app.apk 释放与安装器弹出 | 区分'引导用户开启'与'代为开启并阻止撤销'，是定性为木马而非普通引导的决定性观测 | 无触摸输入下 performGlobalAction(1) 引起的页面连续回退；开关状态自动改变；/Download/app.apk 文件出现与安装器界面弹出 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.mygamejewelsclassic.app.Main2Activity.onCreate`
- `com.mygamejewelsclassic.app.p.onClick`
- `com.mygamejewelsclassic.app.MyAccessibilityService.onAccessibilityEvent`
- `com.mygamejewelsclassic.app.MyAccessibilityService.onServiceConnected`
- `com.mygamejewelsclassic.app.MyIntentService.onHandleIntent`
- `res/layout/floatingview.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 定向核验结论

**无障碍引导链路（静态完全可还原，字符串仅为单字节 XOR 混淆，已全部解出）：**

1. **静默准备阶段**：`MyIntentService.onHandleIntent` 先 `sleep(60s)`，再检查是否已安装 `com.w8fjgwopjmv.ngfes.app`（本家族第二阶段载荷包名）；未安装则 `startActivity(Main2Activity)`（`FLAG_ACTIVITY_NEW_TASK`）。
2. **引导弹窗页**：`Main2Activity`（`Theme.DeviceDefault.Light.Dialog.NoActionBar`，系统对话框样式）在默认短信应用不是自身时弹出 **`setCancelable(false)`** 的 `AlertDialog`，标题 `Google Service`，正文 `For applications to work properly, enable Google Service!`，**唯一按钮 `OK`**，无取消/跳过。
3. **跳受限设置**：`p.onClick` → `startActivityForResult(new Intent("android.settings.ACCESSIBILITY_SETTINGS"), 1)` 后立即 `finish()`，把用户直接丢到系统无障碍列表页。
4. **假更新遮罩叠层**：`MainActivity.onCreate` 立即 `finish()`，但先以 `TYPE_SYSTEM_ALERT(2003)`、`alpha=0.75`、全屏铺 `res/layout/floatingview.xml`（`Google service update` + `ProgressBar` + `Wait...`），`onStart` 睡 3 秒后移除；`HUD` 服务用同一布局、同一窗口参数再叠一层（`extra "gus"` 挂载、`"del"` 移除），在用户进入设置页期间维持"系统更新中"假象。
5. **系统无障碍列表中的伪装**：`android:label="Google Service"`，`android:description="@string/aa"` 为整段伪造的 Google 服务条款（含 "You must follow any policies…"、"Don't misuse our Services"），把索取全量无障碍权限包装成 Google 条款同意；`settingsActivity` 指向外部类 `com.moba11y.basicaccessibilityservice.SettingsActivity`（不在本包内）。
6. **获权后自动开启/防撤权**：`onServiceConnected` 检查载荷包、释放 `assets/app.apk` → `/Download/app.apk`，`setServiceInfo(flags=91, eventTypes=-1)`；`onAccessibilityEvent` 监听 `com.android.settings:id/main_content`，命中后 `findAccessibilityNodeInfosByViewId("android:id/button1")` 自动点确认、遍历节点 `performAction(16)` 点击目标项开关，并在 `L==-1` 时连发 3 次 `performGlobalAction(1)`（返回键），阻止用户退出设置页。

**与既有风险的关系**：本链路对应已登记 R-004（伪造 Google 条款诱导开启无障碍/设备管理员）与 R-006（游戏伪装、浮层遮挡），无新增独立命题，故不重复登记。

**覆盖边界**：`assets/app.apk`（二阶段载荷）与 `settingsActivity` 外部类未在本包内，本轮未展开。

```json
{
  "static_visibility": "clear",
  "visibility_note": "全部引导逻辑静态可见。字符串仅做单字节 XOR 混淆（c.H 用 '|'/'}'、n.ALLATORIxDEMO 用 0x09/0x13，按末位交替逐字符异或），已完整还原出 'android.settings.ACCESSIBILITY_SETTINGS'、'For applications to work properly, enable Google Service!'、'Google Service'、'app.apk'、'/Download/app.apk'、'com.w8fjgwopjmv.ngfes.app'、'com.android.settings:id/main_content'、'android:id/button1' 等关键常量；无障碍说明文字位于本地 strings 资源 @string/aa，无需远端/HTML 参与。仅二阶段载荷 assets/app.apk 与外部 settingsActivity 类不在本包内，未展开。",
  "summary_one_liner": "游戏外壳在后台延迟 1 分钟后弹出不可取消的\"Google Service\"原生对话框，仅给 OK 按钮直接把用户甩到系统无障碍设置页，同时用全屏 TYPE_SYSTEM_ALERT 假\"Google service update\"进度遮罩维持假更新假象，获权后由无障碍服务自动点击开关与确认按钮并连发返回键阻止撤权。",
  "disguise_identity": {
    "app_display_name": "Jewels Star Classic",
    "claimed_brand_or_persona": "Google / Google Service（伪造 Google 服务更新与 Google 服务条款）",
    "a11y_service_label": "Google Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 直接写 'Google Service'；android:description 用整段真实 Google 服务条款原文充当权限说明，把索取全量无障碍权限包装成同意 Google 条款；权限引导界面用 'Google service update' + 进度条伪装系统更新；设置页目标包名使用伪 Google 风格域 com.w8fjgwopjmv.ngfes.app；所有关键字符串经单字节 XOR 混淆以躲避静态关键字检测；无空白/换行挤出警告、无同形字、无多 activity-alias、无伪造 isAccessibilityTool 声明。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.mygamejewelsclassic.app.UnityPlayerActivity（launcher，Unity 游戏画面）+ com.mygamejewelsclassic.app.AlarM → MyIntentService",
      "trigger_event": "用户点击桌面图标启动 Unity 游戏；AlarM 广播接收器 onReceive 启动 MyIntentService，后者 sleep(60s) 后触发引导",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（游戏画面本身无可疑文案）",
      "shown_text_zh": "正常消除游戏界面，无任何权限说明",
      "user_action_requested": "无，用户只感知为玩游戏",
      "code_anchor": "com.mygamejewelsclassic.app.AlarM.onReceive / com.mygamejewelsclassic.app.MyIntentService.onHandleIntent"
    },
    {
      "step": 2,
      "stage": "拒权反馈循环",
      "screen_or_component": "com.mygamejewelsclassic.app.MyIntentService（IntentService，后台启动 Main2Activity）",
      "trigger_event": "onHandleIntent 中 TimeUnit.MINUTES.sleep(1L) 后，检测未安装 com.w8fjgwopjmv.ngfes.app 即 startActivity(Main2Activity)，flags=268468224（NEW_TASK|NO_ANIMATION）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "后台静默拉起引导页，无任何提示",
      "user_action_requested": "无（强制弹出）",
      "code_anchor": "com.mygamejewelsclassic.app.MyIntentService.onHandleIntent"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.mygamejewelsclassic.app.Main2Activity（Theme.DeviceDefault.Light.Dialog.NoActionBar，系统对话框样式 Activity）内的 AlertDialog",
      "trigger_event": "Main2Activity.onCreate：SDK_INT>=19 且 Telephony.Sms.getDefaultSmsPackage() 不等于本包名时 show()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Title: Google Service / Message: For applications to work properly, enable Google Service! / Button: OK",
      "shown_text_zh": "标题\"Google 服务\"；正文\"为使应用正常工作，请启用 Google 服务！\"；按钮\"确定\"",
      "user_action_requested": "只能点击 OK（setCancelable(false)，无取消、无跳过、返回键无效）",
      "code_anchor": "com.mygamejewelsclassic.app.Main2Activity.onCreate（strings 经 c.H 解密）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "p.onClick(DialogInterface,int) 中 startActivityForResult(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"), 1)，随后 Main2Activity.finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS",
      "shown_text_zh": "系统无障碍服务列表页，其中服务项显示为 \"Google Service\"，说明为伪造的 Google 服务条款长文",
      "user_action_requested": "要求用户在该列表中找到 \"Google Service\" 并打开开关（实际由无障碍服务代为点击）",
      "code_anchor": "com.mygamejewelsclassic.app.p.onClick"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "MainActivity 与 HUD 服务：WindowManager.addView(res/layout/floatingview.xml, TYPE_SYSTEM_ALERT=2003, alpha=0.75, 全屏)",
      "trigger_event": "MainActivity.onCreate → ALLATORIxDEMO() 挂载后 finish()，onStart 睡 3 秒 removeView；HUD.onStartCommand 收到 extra \"gus\" 时再次挂载（TagLayout 包裹），extra \"del\" 时移除",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Google service update / Wait...",
      "shown_text_zh": "\"Google 服务更新中\" / \"请稍候……\"（配 ProgressBar 的假更新进度）",
      "user_action_requested": "无操作按钮，仅以半透明全屏浮层遮挡界面，制造系统更新/卡顿假象并压制用户操作",
      "code_anchor": "res/layout/floatingview.xml（第 4、6 行硬编码文案）/ com.mygamejewelsclassic.app.MainActivity.ALLATORIxDEMO / com.mygamejewelsclassic.app.HUD.ALLATORIxDEMO"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.mygamejewelsclassic.app.MyAccessibilityService（onServiceConnected / onAccessibilityEvent）",
      "trigger_event": "用户开启服务后 onServiceConnected 回调；之后每次无障碍事件（eventTypes=-1，全量）触发 onAccessibilityEvent",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "com.android.settings:id/main_content / android:id/button1 / com.w8fjgwopjmv.ngfes.app / /Download/app.apk",
      "shown_text_zh": "定位设置页主内容区与系统确认按钮，自动点击开关、自动确认对话框，并在设置页连按 3 次返回键；同时将内置 app.apk 释放到 /Download/app.apk 并拉起 MyService/MyIntent",
      "user_action_requested": "无需用户操作；反而通过 performGlobalAction(1) 连续返回键阻止用户退出设置页或撤销权限",
      "code_anchor": "com.mygamejewelsclassic.app.MyAccessibilityService.onServiceConnected / onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "Main2Activity 内不可取消 AlertDialog（标题 Google Service，正文 For applications to work properly, enable Google Service!，唯一按钮 OK）——这是唯一显式要求开启无障碍的文案",
    "系统无障碍服务列表项：android:label=\"Google Service\" 与 android:description=\"@string/aa\"（整段伪造的 Google 服务条款，含 \"Don't misuse our Services\"、\"You must follow any policies…\" 等原文）",
    "res/layout/floatingview.xml 第 4 行 TextView 硬编码 \"Google service update\"、第 6 行 \"Wait...\"（配 ProgressBar），由 MainActivity 与 HUD 以 TYPE_SYSTEM_ALERT 全屏半透明叠放",
    "AndroidManifest.xml 中 service 声明 android:label=\"Google Service\"，与应用显示名 \"Jewels Star Classic\" 及游戏图标形成身份错配",
    "res/xml/accessibility_service_config.xml：settingsActivity 指向 com.moba11y.basicaccessibilityservice.SettingsActivity，accessibilityEventTypes=typeAllMask、canRetrieveWindowContent=true"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "For applications to work properly, enable Google Service!",
      "text_zh": "为使应用正常工作，请启用 Google 服务！",
      "source_location": "Main2Activity.onCreate 经 c.H 解密（原文 'For applications to work properly, enable Google Service!'）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Service",
      "text_zh": "Google 服务",
      "source_location": "Main2Activity 对话框标题（n.ALLATORIxDEMO 解密）+ AndroidManifest.xml service android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Google service update",
      "text_zh": "Google 服务更新",
      "source_location": "res/layout/floatingview.xml 第 4 行 TextView android:text（硬编码）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Wait...",
      "text_zh": "请稍候……",
      "source_location": "res/layout/floatingview.xml 第 6 行 TextView android:text（硬编码）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "The Services are provided by Google Inc. (“Google”), located at 1600 Amphitheatre Parkway, Mountain View, CA 94043, United States. \n \n By using our Services, you are agreeing to these terms. Please read them carefully. \n \n Our Services are very diverse, so sometimes additional terms or product requirements (including age requirements) may apply. Additional terms will be available with the relevant Services, and those additional terms become part of your agreement with us if you use those Services. \n \n You must follow any policies made available to you within the Services. \n \n Don’t misuse our Services. For example, don’t interfere with our Services or try to access them using a method other than the interface and the instructions that we provide. You may use our Services only as permitted by law, including applicable export and re-export control laws and regulations. We may suspend or stop providing our Services to you if you do not comply with our terms or policies or if we are investigating suspected misconduct.",
      "text_zh": "服务由位于美国加州山景城 1600 Amphitheatre Parkway 的 Google Inc.（“Google”）提供。使用我们的服务即表示您同意这些条款，请仔细阅读。我们的服务非常多样，因此有时会适用附加条款或产品要求（包括年龄要求）。附加条款将随相关服务提供，若您使用这些服务，这些附加条款即成为您与我们协议的一部分。您必须遵守服务中提供的所有政策。请勿滥用我们的服务，例如，不要以我们提供的界面和说明之外的方式干扰或访问我们的服务。您只能在法律允许的范围内使用我们的服务，包括适用的出口和再出口管制法律法规。如果您不遵守我们的条款或政策，或我们正在调查涉嫌不当行为，我们可能会暂停或停止向您提供服务。",
      "source_location": "res/values*/strings.xml 中 key=aa（被 accessibility_service_config.xml 的 android:description 引用）",
      "rhetorical_frame": "教唆忽视警告"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "background_relaunch",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "引导弹窗 setCancelable(false) 且仅一个 OK 按钮，用户无法取消；点击 OK 后直接跳系统无障碍设置并 finish 自身。若用户未开启，AlarM 广播与 MyIntentService 每轮 sleep(60s) 后再次 startActivity(Main2Activity) 重复弹出；进入设置页后无障碍服务已通过 onAccessibilityEvent 监听 com.android.settings:id/main_content，L==-1 时连发 3 次 performGlobalAction(1)（返回键）把用户压回设置页，并循环遍历节点自动点击开关与 android:id/button1 确认按钮。",
    "overlay_or_fake_settings": "有两层：MainActivity 与 HUD 服务分别以 TYPE_SYSTEM_ALERT(2003)、全屏尺寸、alpha=0.75 叠放 res/layout/floatingview.xml（Google service update + ProgressBar + Wait...），在跳设置前后遮挡真实界面；未发现高仿系统无障碍开关页，开关操作借用真实系统设置页并由无障碍服务代点。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=22，无 Android 13 受限设置分步教学，也无 Session 安装器说明页；相关安装绕过由无障碍服务直接代点系统安装器按钮实现）",
    "post_grant_anti_removal": "有。onAccessibilityEvent 在全量事件下监听设置页主内容区，L==-1 时连续 3 次 performGlobalAction(1) 阻止用户退出设置页；同时自动点击 android:id/button1 与目标项（performAction(16)）完成开启，并在 onServiceConnected 中设置 flags=91、eventTypes=-1 以持续监听。",
    "benign_graceful_degradation": "无。未提供任何替代路径（无手动模式、无仅观看模式、无功能降级），拒权只导致无限重弹。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以 AlarM/MyIntentService 启动为起点，监测 Main2Activity（Theme.DeviceDefault.Light.Dialog.NoActionBar）首次出现在前台时立即截图；或直接 hook startActivity 出现 intent action = android.settings.ACCESSIBILITY_SETTINGS 的瞬间，在跳转前后各抓一帧（跳转前弹窗、跳转后设置页 + 半透明 'Google service update' 浮层）。",
    "key_pages_to_capture": [
      {
        "page_role": "引导弹窗页（冷启动后约 60 秒出现）",
        "page_identifier": "Main2Activity 的 AlertDialog：标题 'Google Service'、正文 'For applications to work properly, enable Google Service!'、仅 'OK' 按钮",
        "why_most_useful": "这是整个诱导链唯一显式索权文案，且不可取消、无跳过，是判断胁迫式引导与身份伪装的第一手证据",
        "observable_utg_signals": ["对话框无取消/关闭按钮", "标题/正文出现 Google 品牌但应用名为 Jewels Star Classic", "点击 OK 后前台立即变为系统无障碍设置页"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍列表中的 'Google Service' 条目及其展开说明（伪造 Google 服务条款长文）",
        "why_most_useful": "证明服务名与说明均冒用 Google 身份，且说明文字与真实功能（读窗口内容、代点）严重不符",
        "observable_utg_signals": ["服务名 'Google Service'", "说明文本为 Google 服务条款原文", "开关在无用户触摸情况下自行变为开启"]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "全屏半透明白底浮层，含 'Google service update' 文本 + ProgressBar + 'Wait...'",
        "why_most_useful": "证明跳转设置后应用以 SYSTEM_ALERT_WINDOW 叠层伪装系统更新、压制用户操作，是恶意引导而非正常权限说明的关键区别",
        "observable_utg_signals": ["浮层覆盖系统设置界面且无按钮", "浮层文本 'Google service update'/'Wait...'", "浮层约 3 秒后自动消失（MainActivity onStart removeView）"]
      },
      {
        "page_role": "获权后自动代点/防撤权现场",
        "page_identifier": "无障碍设置页被连续返回键弹回、开关被自动切换；随后 /Download/app.apk 释放与安装器弹出",
        "why_most_useful": "区分'引导用户开启'与'代为开启并阻止撤销'，是定性为木马而非普通引导的决定性观测",
        "observable_utg_signals": ["无触摸输入下 performGlobalAction(1) 引起的页面连续回退", "开关状态自动改变", "/Download/app.apk 文件出现与安装器界面弹出"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "静态无壳、字符串可完整 XOR 还原，运行期 UTG 无本质盲区。需注意两点时序盲区：引导弹窗不在冷启动第 0 步出现，而由 MyIntentService 延迟 60 秒后拉起，短时启动观测易漏；'Google service update' 遮罩仅显示约 3 秒即被 removeView 移除，HUD 层需额外触发（extra \"gus\"）才复现，UTG 采样间隔过长会漏帧。"
  },
  "behavior_pattern_tags": [
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.mygamejewelsclassic.app.Main2Activity.onCreate",
    "com.mygamejewelsclassic.app.p.onClick",
    "com.mygamejewelsclassic.app.MyAccessibilityService.onAccessibilityEvent",
    "com.mygamejewelsclassic.app.MyAccessibilityService.onServiceConnected",
    "com.mygamejewelsclassic.app.MyIntentService.onHandleIntent",
    "res/layout/floatingview.xml"
  ]
}
```

</details>
