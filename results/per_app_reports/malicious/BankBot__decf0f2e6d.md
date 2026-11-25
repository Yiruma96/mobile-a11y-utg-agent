# MB_109__decf0f2e6d｜BankBot — M​ü​z​i​k

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：181.7s

## 1. 一句话核心结论

- **核心申请方式**：以零宽空格名『Müzik』伪装音乐应用，冷启动强制申请通知权限后跳自绘说明页（土耳其语+GIF），点击卡片用 Samsung 私有无障碍深链直接高亮本应用服务项，拒绝即 Toast 并结束进程，全程无取消/跳过。
- **静态可见性说明**：无障碍引导链的代码、跳转 Intent、解密文案全部静态可见且已还原（Blowfish/ECB 硬编码密钥 30aa7531ea + 双层 Base64）；未见加壳/VMP/动态加载 DEX。仅两处为远端内容：引导页操作图示 GIF 来自 https://s11.gifyu.com/images/SW9m9.gif，以及获权后 MOV 中 WebView 加载的远端面板 rx/f.php?f=<id>&p=<device>|tr，其页面内容本地无法静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `decf0f2e6d42f5da6ef5f77954115e5cbbb8d68edab7151cf34d28a6d49cb9f8` |
| 包名 / 年份 | `com.starryheaded.defrauds` / 2026 |
| 家族 / 品类 | **BankBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Müzik（字符间插入 U+200B 零宽空格） |
| 引导页宣称品牌/身份 | 音乐播放/下载应用『Müzik』，另备『Play Store』『Google』『Youtube』别名身份 |
| 系统无障碍列表服务名 | Müzik（同样含 U+200B，与桌面名一致，复用 @string/app_name） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 桌面名与服务标签在 ü/z/i/k 之间插入 U+200B 零宽空格，系统无障碍警告处显示为不可见字符串；2) 三个 activity-alias（Google 启用/指向 skijoring、Youtube 默认禁用/指向 wellthoughtout、标签 Play Store、独立图标 launc/launcr）实现多身份换皮，获权后由无障碍服务动态 setComponentEnabledSetting 切换；3) 全部诱导文案与 Intent action 经 Blowfish/ECB 加密，避免静态字符串检索；4) 无障碍服务未声明 android:description，系统权限说明页无任何用途解释。 |
| 无障碍服务类名 | `com.starryheaded.defrauds.outdancing` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.starryheaded.defrauds.skijoring（经 activity-alias com.starryheaded.defrauds.Google 启动，布局 R.layout.Lyubertsy） | onCreate 加载启动布局；onResume 检测 Build.VERSION.SDK_INT >= 33 且 shouldShowRequestPermissionRationale("112") 为 false | 原生Activity | **原文**：无（仅空白启动布局，随后弹出系统通知权限对话框）<br>**译注**：启动瞬间无自绘文案，直接弹出系统 POST_NOTIFICATIONS 权限请求框 | 在系统弹框中点击『允许』；无自绘取消/跳过入口 | `com.starryheaded.defrauds.skijoring.onResume / skijoring.Annora` |
| 2 | 拒权反馈循环 | Toast + Activity.finish()（skijoring 被销毁） | onRequestPermissionsResult(requestCode=112) 中 grantResults[0] != 0 | 原生Dialog | **原文**：Gerekli izni vermeden uygulamayı kullanamazsınız.<br>**译注**：不授予必要权限，您将无法使用本应用。 | 无任何按钮；Toast 后立即 finish() 退出应用，必须重开并重新授权 | `com.starryheaded.defrauds.skijoring.onRequestPermissionsResult` |
| 3 | 引导说明页 | com.starryheaded.defrauds.craniate（布局 R.layout.partycolored，正文 TextView + 副标题 TextView + CardView 授权卡片 + Glide GIF） | skijoring.signifiable() 完成配置写入与 pegtop 前台服务启动后 startActivity(craniate)；craniate.onResume 中 setText 与 asGif().load(...) | 原生Activity | **原文**：Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / İzin Ver / (GIF: https://s11.gifyu.com/images/SW9m9.gif)<br>**译注**：为使音乐下载功能生效，请授予上方所示的权限。／『授予权限』按钮／配图 GIF 演示操作步骤 | 点击 CardView（『İzin Ver』）进入下一步；页面无『跳过』『稍后』『取消』按钮 | `com.starryheaded.defrauds.craniate.onResume` |
| 4 | 跳无障碍设置 | Intent(com.samsung.accessibility.installed_service)，失败回退 Settings.ACTION_ACCESSIBILITY_SETTINGS；携带 :settings:show_fragment_args 与 :settings:fragment_args_key | craniate$1.onClick 中 intent.resolveActivity() 判定；!pegtop.stactes() 为真时 Toast 后 startActivity(FLAG_ACTIVITY_NEW_TASK)，随后 finish() | 系统无障碍页 | **原文**：Müzik indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)<br>**译注**：为使音乐下载功能生效，请授予无障碍（erişebilirlik）权限。(Müzik) | 在系统无障碍页中把『Müzik』服务开关拨至开启（因 fragment_args_key 已预选，页面直接高亮该项） | `com.starryheaded.defrauds.craniate$1.onClick` |
| 5 | 获权后动作 | com.starryheaded.defrauds.outdancing（AccessibilityService）+ pegtop（前台服务） | onAccessibilityEvent 检出配置项 fss 含 true 分支 | 不可静态还原 | **原文**：无（静默执行：setComponentEnabledSetting 启用 .Youtube、禁用 .Google，performGlobalAction(2) 回桌面，Handler 延迟 2000ms 继续后续任务）<br>**译注**：无界面文案；自动切换 activity-alias 伪装身份并退回桌面，隐藏自身后开始读取窗口内容/自动点击 | 无需用户操作，界面被自动夺回桌面 | `com.starryheaded.defrauds.outdancing.onAccessibilityEvent` |
| 6 | 拒权反馈循环 | craniate 页 + Toast（无自动重跳，需再次点击卡片） | 用户从系统无障碍页直接返回而未开启服务，再次点击 craniate 的授权卡片 | 原生Activity | **原文**：Müzik indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)<br>**译注**：再次提示必须授予无障碍权限，否则无法使用音乐下载功能 | 重复点击卡片重试；或按返回键退出（应用核心功能始终不可用） | `com.starryheaded.defrauds.craniate$1.onClick / pegtop.stactes` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动：skijoring 仅空白布局 R.layout.Lyubertsy，文案完全由系统 POST_NOTIFICATIONS 权限弹框承担（无自绘说明）
- 拒权：skijoring.onRequestPermissionsResult 中的系统 Toast『Gerekli izni vermeden uygulamayı kullanamazsınız.』
- 说明页：craniate（R.layout.partycolored）正文 TextView 显示『Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz.』，副标题 TextView 显示『İzin Ver』，ImageView 经 Glide 加载远端 GIF 作为分步图示
- 跳转前：craniate$1.onClick 中 Toast『Müzik indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)』，setGravity 居中显示
- 系统无障碍列表：服务项名称取自 android:label=@string/app_name（含 U+200B 的『Müzik』），android:description 缺失，因此系统权限详情页无任何用途说明文字
- 系统无障碍页内定位：通过 :settings:fragment_args_key 预选条目，跳转后该服务项被高亮/滚动到可见区域（非应用自绘界面）
- 远端面板：获权后 MOV 内 WebView 加载 rx/f.php?f=<id>&p=<device>|tr，页面文案由服务端下发，本地不可静态还原

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. | 为使音乐下载功能生效，请授予上方所示的权限。 | `craniate.onResume 中 unsided.n("Jcw0kdWfO1oVXArrzApMnZMnX9GGRE4wrejZM8ikxQF0KkK1v2C6R+3es0s/9T/I06iA0VxQ4LILx/joObBIcKI7EyFmVWnbXvrUa8sVXkmoBzgQBr5YbZxcUmZTXgthsTDIQxqiwGRKrwrKz+WtuV1Sj+3n496H")` | 故障恐吓 |
| tr | Müzik indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik) | 为使音乐下载功能生效，请授予无障碍（erişebilirlik）权限。(Müzik) | `craniate$1.onClick 中 unsided.n("Jcw0kdWfO1oVXArrzApMnZMnX9GGRE4wrejZM8ikxQF0KkK1v2C6R+3es0s/9T/I06iA0VxQ4LILx/joObBIcHLZqE/4ez92mRIaqsNI+/lP7pRhyEl2ZSvVrf8F2WUe5dOFr9UZC4iopJGQcwlPog==") + unsided.n("bOOfyEHvTGiy/N1DR+wEzw==")` | 故障恐吓 |
| tr | Gerekli izni vermeden uygulamayı kullanamazsınız. | 不授予必要权限，您将无法使用本应用。 | `skijoring.onRequestPermissionsResult / skijoring.onResume 中 unsided.n("CLMm8PyXq4CcwD+5aTgJk9mJ+Pjemn6cRSvMHuxkYEuWVMQsngFMDd2EIODhMocCKizhUBiI81P/NhO0sbOrzLM/gHvb5M4E")` | 故障恐吓 |
| tr | Lütfen daha sonra deneyiniz. | 请稍后再试。 | `skijoring.onResume / skijoring.signifiable 中 unsided.n("7KtG32z/8wvJorFZNNJNAGK/Vabg3CrvH8E/ludtYvhH5mHgQ5EThw==")` | 未知 |
| tr | İzin Ver | 授予权限（授权按钮文字） | `craniate.onResume 中 hornpout.setText(... unsided.n("xLtbGhaYGioPjT500NIxvQ=="))` | 受限设置分步教学 |
| tr | Tamam | 确定 | `skijoring.signifiable 中 unsided.n("u5d1Baxd1qM=") 写入配置项 SqmxGUkFusI=` | 未知 |
| en | Play Store | Play 商店（伪装的应用商店身份标签） | `res/values/strings.xml 中 <string name="appname">P​l​a​y S​t​o​r​e</string>（含 U+200B）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：通知权限被拒 → Toast『不授予必要权限，您将无法使用本应用』并立即 finish() 销毁当前 Activity，用户须重启应用再授权；从无障碍设置返回但未开启服务时不会自动重跳，仅再次点击说明页授权卡片时以 Toast 提示必须授予无障碍权限（且应用核心功能始终不可用），未见 onResume 定时死循环或 Timer 定时拉起
- **遮罩叠层 / 高仿系统设置页**：无悬浮窗遮罩、无高仿系统无障碍开关页；引导依靠原生 Activity 说明页 + 系统设置深链定位（:settings:fragment_args_key 预选高亮本应用服务项），并配远端 GIF 演示操作步骤
- **Android 13+ 受限设置（Restricted Settings）应对**：无；未出现引导进入应用详情页右上角菜单开启『受限设置』的文案，也未使用 Session 安装器绕过，仅针对 Android 13+ 做 POST_NOTIFICATIONS 前置申请
- **获权后即时行为与防撤权机制**：获权后由无障碍服务执行 setComponentEnabledSetting 启用 .Youtube 别名、禁用 .Google 别名完成换皮，并 performGlobalAction(2)（GLOBAL_ACTION_HOME）立即退出系统设置页；未见自点确认、自授权或监听设置页用 GLOBAL_ACTION_BACK 阻止撤权的逻辑
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 Activity 切换至 com.starryheaded.defrauds.craniate 的瞬间拉起 UTG（这是唯一承载自绘引导文案与授权卡片的页面）；其次在捕获到 Intent action 为 com.samsung.accessibility.installed_service 或 android.settings.ACCESSIBILITY_SETTINGS 时立即截取系统无障碍页，以确认 fragment_args_key 是否把本应用服务项预选高亮。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：引导说明页的关键配图为远端 GIF（s11.gifyu.com/images/SW9m9.gif），其画面内容纯图无文本，须 OCR/视觉模型识别；此外获权后远端面板 rx/f.php 由服务端渲染，文案与表单结构本地不可静态还原；应用未加壳，静态加壳不构成 UTG 盲区。另需注意显示名与服务标签含 U+200B 零宽空格，按纯文本精确匹配『Müzik』会漏判，应以归一化（去零宽字符）后比较。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | com.starryheaded.defrauds.craniate，布局 partycolored：正文长句『Müzik indirme işleminin aktif olabilmesi için…』+ 副标题『İzin Ver』+ CardView + GIF ImageView | 唯一以自绘文字把『无障碍授权』包装成『音乐下载必需条件』的页面，是判断虚假陈述与不可跳过引导的核心界面证据 | 页面根节点为 craniate 的 window 且无返回/关闭控件；TextView 文本包含 'Müzik indirme işleminin aktif olabilmesi' 与 'İzin Ver'；ImageView 节点存在但无文本（远端 GIF，需结合图像判断）；全页仅 CardView 可点击，无跳过/取消节点 |
| **设置页后压栈的系统无障碍服务列表项** | 系统 Settings 无障碍页，目标条目文本『Müzik』（实际含 U+200B 零宽字符） | 验证深链是否直接定位并高亮本应用服务项，以及系统侧展示的服务名与警告文案是否与桌面名不一致 | package 为 com.android.settings 的 window，条目 text 以 'Müzik' 开头但字节长度异常（含零宽字符）；该条目处于选中/滚动到可见位置（fragment_args_key 生效）；条目 summary/description 为空（android:description 缺失） |
| **拒权反馈页（Toast）** | craniate 内居中 Toast 或 skijoring 退出前 Toast | 确认拒绝授权后应用以不可用为要挟并销毁自身，量化强制程度 | Toast 文本 'Gerekli izni vermeden uygulamayı kullanamazsınız.' 或 '…erişebilirlik iznini veriniz. (Müzik)'；随后窗口从 craniate/skijoring 变为桌面 |
| **获权后自动返回桌面与别名切换** | Launcher 桌面（performGlobalAction(2) 后）及变更后的 launcher 图标/名称 | 证明获权后服务立即介入并静默切换 activity-alias 身份，是变脸行为的运行期证据 | 无障碍开关开启后约 2 秒内前台窗口变为 Launcher；桌面出现标签为 'Play Store' / 'Youtube' 的入口（Google 别名被禁用、Youtube 被启用） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.starryheaded.defrauds.skijoring.onResume`
- `com.starryheaded.defrauds.skijoring.signifiable`
- `com.starryheaded.defrauds.craniate.onResume`
- `com.starryheaded.defrauds.craniate$1.onClick`
- `com.starryheaded.defrauds.outdancing.onAccessibilityEvent`
- `res/xml/preferences.xml + res/values/strings.xml(app_name/appname)`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验已完成，未加壳，字符串已完全还原）

**1. 身份伪装**
- 桌面名 `Müzik` 在 `ü/z/i/k` 之间插入 U+200B 零宽空格（[strings.xml](#1 file:res/values/strings.xml)），无障碍服务 `label` 复用同一名称，系统无障碍列表显示为“Müzik”；另有 `appname` = `Play Store`。
- Manifest 声明 3 个 `activity-alias`：`Google`（启用，入口 `skijoring`）、`Youtube`（默认禁用，入口 `wellthoughtout`）、`Play Store` 图标集；获权后由服务动态启停这两个别名完成变脸（`setComponentEnabledSetting` 后 `performGlobalAction(2)` 返回桌面）。

**2. 无障碍服务用途空白，但能力最大**
[res/xml/preferences.xml](#1 file:res/xml/preferences.xml) 仅声明 `typeAllMask`、`canRetrieveWindowContent=true`、`canPerformGestures=true`，无 `android:description`，`feedbackGeneric`；这实质上是“读取全部界面文本+模拟点击手势”，而对外给出的理由是“音乐下载需要授权”。

**3. 四步强制引导链（无取消、无跳过、无降级）**
- **冷启动**：[skijoring.onResume()](#1.dex1 code:com.starryheaded.defrauds.skijoring#onResume) 先判断 `accs` 是否受限；Android 13+ 直接 `requestPermissions(POST_NOTIFICATIONS, 112)`，被拒即 Toast「Gerekli izni vermeden uygulamayı kullanamazsınız.」+ `finish()`（[onRequestPermissionsResult](#1.dex1 code:com.starryheaded.defrauds.skijoring#onRequestPermissionsResult)）。
- **说明页**：[signifiable()](#1.dex1 code:com.starryheaded.defrauds.skijoring#signifiable) 写入配置、起前台服务 `pegtop`，跳 [craniate](#1.dex1 code:com.starryheaded.defrauds.craniate#onResume)；布局 `partycolored`，正文“音乐下载功能要生效，请授予上方所示的权限”，按钮“İzin Ver”，并 Glide 加载远端 GIF `https://s11.gifyu.com/images/SW9m9.gif` 作为操作图示。
- **跳系统无障碍页**：[craniate$1.onClick()](#1.dex1 code:com.starryheaded.defrauds.craniate$1#onClick) 优先使用 Samsung 私有 action `com.samsung.accessibility.installed_service`，失败回退 `Settings.ACTION_ACCESSIBILITY_SETTINGS`；两者均塞入 `:settings:show_fragment_args`（`component_name=包名/outdancing`）与 `:settings:fragment_args_key`，使系统页**直接定位并高亮本应用服务项**，再用 `NEW_TASK` 启动；未授权时再 Toast「…erişebilirlik iznini veriniz. (Müzik)」。
- **获权后**：[outdancing.onAccessibilityEvent()](#1.dex1 code:com.starryheaded.defrauds.outdancing#onAccessibilityEvent) 检出 `fss` 标志→启 `Google`、禁 `Youtube` 别名→`GLOBAL_ACTION_HOME` 退出设置页→2s 后执行后续自动化。

**4. 文案加密方式**：所有诱导文案经 [unsided.z()](#1.dex1 code:com.starryheaded.defrauds.unsided#z) 用 Blowfish/ECB、密钥 `30aa7531ea` 加密 + Base64，二次 Base64 后为土耳其语明文；无 VMP/无加壳，`static_visibility` 判定为引导链完全静态可见。

**5. 待说明的边界**：引导页 GIF 与获权后 C2 面板（`MOV` 中 WebView 加载 `…/rx/f.php?f=<id>&p=<设备>&tr`）为远端资源，本地不可静态还原其内容；从无障碍设置返回但未授权时无自动重跳循环（依赖用户再次点击卡片）。

已登记风险 **R-001**（high / deceptive_behavior）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "无障碍引导链的代码、跳转 Intent、解密文案全部静态可见且已还原（Blowfish/ECB 硬编码密钥 30aa7531ea + 双层 Base64）；未见加壳/VMP/动态加载 DEX。仅两处为远端内容：引导页操作图示 GIF 来自 https://s11.gifyu.com/images/SW9m9.gif，以及获权后 MOV 中 WebView 加载的远端面板 rx/f.php?f=<id>&p=<device>|tr，其页面内容本地无法静态还原。",
  "summary_one_liner": "以零宽空格名『Müzik』伪装音乐应用，冷启动强制申请通知权限后跳自绘说明页（土耳其语+GIF），点击卡片用 Samsung 私有无障碍深链直接高亮本应用服务项，拒绝即 Toast 并结束进程，全程无取消/跳过。",
  "disguise_identity": {
    "app_display_name": "Müzik（字符间插入 U+200B 零宽空格）",
    "claimed_brand_or_persona": "音乐播放/下载应用『Müzik』，另备『Play Store』『Google』『Youtube』别名身份",
    "a11y_service_label": "Müzik（同样含 U+200B，与桌面名一致，复用 @string/app_name）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 桌面名与服务标签在 ü/z/i/k 之间插入 U+200B 零宽空格，系统无障碍警告处显示为不可见字符串；2) 三个 activity-alias（Google 启用/指向 skijoring、Youtube 默认禁用/指向 wellthoughtout、标签 Play Store、独立图标 launc/launcr）实现多身份换皮，获权后由无障碍服务动态 setComponentEnabledSetting 切换；3) 全部诱导文案与 Intent action 经 Blowfish/ECB 加密，避免静态字符串检索；4) 无障碍服务未声明 android:description，系统权限说明页无任何用途解释。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.starryheaded.defrauds.skijoring（经 activity-alias com.starryheaded.defrauds.Google 启动，布局 R.layout.Lyubertsy）",
      "trigger_event": "onCreate 加载启动布局；onResume 检测 Build.VERSION.SDK_INT >= 33 且 shouldShowRequestPermissionRationale(\"112\") 为 false",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（仅空白启动布局，随后弹出系统通知权限对话框）",
      "shown_text_zh": "启动瞬间无自绘文案，直接弹出系统 POST_NOTIFICATIONS 权限请求框",
      "user_action_requested": "在系统弹框中点击『允许』；无自绘取消/跳过入口",
      "code_anchor": "com.starryheaded.defrauds.skijoring.onResume / skijoring.Annora"
    },
    {
      "step": 2,
      "stage": "拒权反馈循环",
      "screen_or_component": "Toast + Activity.finish()（skijoring 被销毁）",
      "trigger_event": "onRequestPermissionsResult(requestCode=112) 中 grantResults[0] != 0",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "Gerekli izni vermeden uygulamayı kullanamazsınız.",
      "shown_text_zh": "不授予必要权限，您将无法使用本应用。",
      "user_action_requested": "无任何按钮；Toast 后立即 finish() 退出应用，必须重开并重新授权",
      "code_anchor": "com.starryheaded.defrauds.skijoring.onRequestPermissionsResult"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.starryheaded.defrauds.craniate（布局 R.layout.partycolored，正文 TextView + 副标题 TextView + CardView 授权卡片 + Glide GIF）",
      "trigger_event": "skijoring.signifiable() 完成配置写入与 pegtop 前台服务启动后 startActivity(craniate)；craniate.onResume 中 setText 与 asGif().load(...)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / İzin Ver / (GIF: https://s11.gifyu.com/images/SW9m9.gif)",
      "shown_text_zh": "为使音乐下载功能生效，请授予上方所示的权限。／『授予权限』按钮／配图 GIF 演示操作步骤",
      "user_action_requested": "点击 CardView（『İzin Ver』）进入下一步；页面无『跳过』『稍后』『取消』按钮",
      "code_anchor": "com.starryheaded.defrauds.craniate.onResume"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "Intent(com.samsung.accessibility.installed_service)，失败回退 Settings.ACTION_ACCESSIBILITY_SETTINGS；携带 :settings:show_fragment_args 与 :settings:fragment_args_key",
      "trigger_event": "craniate$1.onClick 中 intent.resolveActivity() 判定；!pegtop.stactes() 为真时 Toast 后 startActivity(FLAG_ACTIVITY_NEW_TASK)，随后 finish()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Müzik indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)",
      "shown_text_zh": "为使音乐下载功能生效，请授予无障碍（erişebilirlik）权限。(Müzik)",
      "user_action_requested": "在系统无障碍页中把『Müzik』服务开关拨至开启（因 fragment_args_key 已预选，页面直接高亮该项）",
      "code_anchor": "com.starryheaded.defrauds.craniate$1.onClick"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.starryheaded.defrauds.outdancing（AccessibilityService）+ pegtop（前台服务）",
      "trigger_event": "onAccessibilityEvent 检出配置项 fss 含 true 分支",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（静默执行：setComponentEnabledSetting 启用 .Youtube、禁用 .Google，performGlobalAction(2) 回桌面，Handler 延迟 2000ms 继续后续任务）",
      "shown_text_zh": "无界面文案；自动切换 activity-alias 伪装身份并退回桌面，隐藏自身后开始读取窗口内容/自动点击",
      "user_action_requested": "无需用户操作，界面被自动夺回桌面",
      "code_anchor": "com.starryheaded.defrauds.outdancing.onAccessibilityEvent"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "craniate 页 + Toast（无自动重跳，需再次点击卡片）",
      "trigger_event": "用户从系统无障碍页直接返回而未开启服务，再次点击 craniate 的授权卡片",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Müzik indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)",
      "shown_text_zh": "再次提示必须授予无障碍权限，否则无法使用音乐下载功能",
      "user_action_requested": "重复点击卡片重试；或按返回键退出（应用核心功能始终不可用）",
      "code_anchor": "com.starryheaded.defrauds.craniate$1.onClick / pegtop.stactes"
    }
  ],
  "text_presentation_locations": [
    "冷启动：skijoring 仅空白布局 R.layout.Lyubertsy，文案完全由系统 POST_NOTIFICATIONS 权限弹框承担（无自绘说明）",
    "拒权：skijoring.onRequestPermissionsResult 中的系统 Toast『Gerekli izni vermeden uygulamayı kullanamazsınız.』",
    "说明页：craniate（R.layout.partycolored）正文 TextView 显示『Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz.』，副标题 TextView 显示『İzin Ver』，ImageView 经 Glide 加载远端 GIF 作为分步图示",
    "跳转前：craniate$1.onClick 中 Toast『Müzik indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)』，setGravity 居中显示",
    "系统无障碍列表：服务项名称取自 android:label=@string/app_name（含 U+200B 的『Müzik』），android:description 缺失，因此系统权限详情页无任何用途说明文字",
    "系统无障碍页内定位：通过 :settings:fragment_args_key 预选条目，跳转后该服务项被高亮/滚动到可见区域（非应用自绘界面）",
    "远端面板：获权后 MOV 内 WebView 加载 rx/f.php?f=<id>&p=<device>|tr，页面文案由服务端下发，本地不可静态还原"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Müzik indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz.",
      "text_zh": "为使音乐下载功能生效，请授予上方所示的权限。",
      "source_location": "craniate.onResume 中 unsided.n(\"Jcw0kdWfO1oVXArrzApMnZMnX9GGRE4wrejZM8ikxQF0KkK1v2C6R+3es0s/9T/I06iA0VxQ4LILx/joObBIcKI7EyFmVWnbXvrUa8sVXkmoBzgQBr5YbZxcUmZTXgthsTDIQxqiwGRKrwrKz+WtuV1Sj+3n496H\")",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "tr",
      "text_verbatim": "Müzik indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)",
      "text_zh": "为使音乐下载功能生效，请授予无障碍（erişebilirlik）权限。(Müzik)",
      "source_location": "craniate$1.onClick 中 unsided.n(\"Jcw0kdWfO1oVXArrzApMnZMnX9GGRE4wrejZM8ikxQF0KkK1v2C6R+3es0s/9T/I06iA0VxQ4LILx/joObBIcHLZqE/4ez92mRIaqsNI+/lP7pRhyEl2ZSvVrf8F2WUe5dOFr9UZC4iopJGQcwlPog==\") + unsided.n(\"bOOfyEHvTGiy/N1DR+wEzw==\")",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "tr",
      "text_verbatim": "Gerekli izni vermeden uygulamayı kullanamazsınız.",
      "text_zh": "不授予必要权限，您将无法使用本应用。",
      "source_location": "skijoring.onRequestPermissionsResult / skijoring.onResume 中 unsided.n(\"CLMm8PyXq4CcwD+5aTgJk9mJ+Pjemn6cRSvMHuxkYEuWVMQsngFMDd2EIODhMocCKizhUBiI81P/NhO0sbOrzLM/gHvb5M4E\")",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "tr",
      "text_verbatim": "Lütfen daha sonra deneyiniz.",
      "text_zh": "请稍后再试。",
      "source_location": "skijoring.onResume / skijoring.signifiable 中 unsided.n(\"7KtG32z/8wvJorFZNNJNAGK/Vabg3CrvH8E/ludtYvhH5mHgQ5EThw==\")",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "İzin Ver",
      "text_zh": "授予权限（授权按钮文字）",
      "source_location": "craniate.onResume 中 hornpout.setText(... unsided.n(\"xLtbGhaYGioPjT500NIxvQ==\"))",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Tamam",
      "text_zh": "确定",
      "source_location": "skijoring.signifiable 中 unsided.n(\"u5d1Baxd1qM=\") 写入配置项 SqmxGUkFusI=",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Play Store",
      "text_zh": "Play 商店（伪装的应用商店身份标签）",
      "source_location": "res/values/strings.xml 中 <string name=\"appname\">P​l​a​y S​t​o​r​e</string>（含 U+200B）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "通知权限被拒 → Toast『不授予必要权限，您将无法使用本应用』并立即 finish() 销毁当前 Activity，用户须重启应用再授权；从无障碍设置返回但未开启服务时不会自动重跳，仅再次点击说明页授权卡片时以 Toast 提示必须授予无障碍权限（且应用核心功能始终不可用），未见 onResume 定时死循环或 Timer 定时拉起",
    "overlay_or_fake_settings": "无悬浮窗遮罩、无高仿系统无障碍开关页；引导依靠原生 Activity 说明页 + 系统设置深链定位（:settings:fragment_args_key 预选高亮本应用服务项），并配远端 GIF 演示操作步骤",
    "restricted_settings_13plus_coaching": "无；未出现引导进入应用详情页右上角菜单开启『受限设置』的文案，也未使用 Session 安装器绕过，仅针对 Android 13+ 做 POST_NOTIFICATIONS 前置申请",
    "post_grant_anti_removal": "获权后由无障碍服务执行 setComponentEnabledSetting 启用 .Youtube 别名、禁用 .Google 别名完成换皮，并 performGlobalAction(2)（GLOBAL_ACTION_HOME）立即退出系统设置页；未见自点确认、自授权或监听设置页用 GLOBAL_ACTION_BACK 阻止撤权的逻辑",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 Activity 切换至 com.starryheaded.defrauds.craniate 的瞬间拉起 UTG（这是唯一承载自绘引导文案与授权卡片的页面）；其次在捕获到 Intent action 为 com.samsung.accessibility.installed_service 或 android.settings.ACCESSIBILITY_SETTINGS 时立即截取系统无障碍页，以确认 fragment_args_key 是否把本应用服务项预选高亮。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "com.starryheaded.defrauds.craniate，布局 partycolored：正文长句『Müzik indirme işleminin aktif olabilmesi için…』+ 副标题『İzin Ver』+ CardView + GIF ImageView",
        "why_most_useful": "唯一以自绘文字把『无障碍授权』包装成『音乐下载必需条件』的页面，是判断虚假陈述与不可跳过引导的核心界面证据",
        "observable_utg_signals": ["页面根节点为 craniate 的 window 且无返回/关闭控件", "TextView 文本包含 'Müzik indirme işleminin aktif olabilmesi' 与 'İzin Ver'", "ImageView 节点存在但无文本（远端 GIF，需结合图像判断）", "全页仅 CardView 可点击，无跳过/取消节点"]
      },
      {
        "page_role": "设置页后压栈的系统无障碍服务列表项",
        "page_identifier": "系统 Settings 无障碍页，目标条目文本『Müzik』（实际含 U+200B 零宽字符）",
        "why_most_useful": "验证深链是否直接定位并高亮本应用服务项，以及系统侧展示的服务名与警告文案是否与桌面名不一致",
        "observable_utg_signals": ["package 为 com.android.settings 的 window，条目 text 以 'Müzik' 开头但字节长度异常（含零宽字符）", "该条目处于选中/滚动到可见位置（fragment_args_key 生效）", "条目 summary/description 为空（android:description 缺失）"]
      },
      {
        "page_role": "拒权反馈页（Toast）",
        "page_identifier": "craniate 内居中 Toast 或 skijoring 退出前 Toast",
        "why_most_useful": "确认拒绝授权后应用以不可用为要挟并销毁自身，量化强制程度",
        "observable_utg_signals": ["Toast 文本 'Gerekli izni vermeden uygulamayı kullanamazsınız.' 或 '…erişebilirlik iznini veriniz. (Müzik)'", "随后窗口从 craniate/skijoring 变为桌面"]
      },
      {
        "page_role": "获权后自动返回桌面与别名切换",
        "page_identifier": "Launcher 桌面（performGlobalAction(2) 后）及变更后的 launcher 图标/名称",
        "why_most_useful": "证明获权后服务立即介入并静默切换 activity-alias 身份，是变脸行为的运行期证据",
        "observable_utg_signals": ["无障碍开关开启后约 2 秒内前台窗口变为 Launcher", "桌面出现标签为 'Play Store' / 'Youtube' 的入口（Google 别名被禁用、Youtube 被启用）"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "引导说明页的关键配图为远端 GIF（s11.gifyu.com/images/SW9m9.gif），其画面内容纯图无文本，须 OCR/视觉模型识别；此外获权后远端面板 rx/f.php 由服务端渲染，文案与表单结构本地不可静态还原；应用未加壳，静态加壳不构成 UTG 盲区。另需注意显示名与服务标签含 U+200B 零宽空格，按纯文本精确匹配『Müzik』会漏判，应以归一化（去零宽字符）后比较。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.starryheaded.defrauds.skijoring.onResume",
    "com.starryheaded.defrauds.skijoring.signifiable",
    "com.starryheaded.defrauds.craniate.onResume",
    "com.starryheaded.defrauds.craniate$1.onClick",
    "com.starryheaded.defrauds.outdancing.onAccessibilityEvent",
    "res/xml/preferences.xml + res/values/strings.xml(app_name/appname)"
  ]
}
```

</details>
