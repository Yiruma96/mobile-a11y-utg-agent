# MR_173__1f5e3e5465｜EventBot — Flash Player

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：98.0s

## 1. 一句话核心结论

- **核心申请方式**：桌面伪装成 Flash Player，启动即静默起服务并 RC4 解密加载 eventBot 二阶段 DEX，由该载荷在全屏 Activity 内用本地 HTML+截图做“选择 Flash Player 并打开”的分步无障碍开启教学，并以 System updating 假更新动画掩护，无障碍服务开启后才启动核心远控逻辑。
- **静态可见性说明**：Manifest、无障碍服务配置、全部引导文案/HTML/截图资源（strings.xml 的 hint_text、hint_button、banner_text，assets/1.jpg、2.jpg、es1/es2、it1/it2）以及载荷装载器 tblvifn 均可完整静态读取；但真正驱动引导页呈现、跳转 ACTION_ACCESSIBILITY_SETTINGS、拒权后重跳与悬浮遮罩的核心逻辑位于 assets/fonts/default.ttf —— 该文件为 RC4 加密的第二阶段 DEX（密钥硬编码 7e89013d...affd63），经 DexClassLoader 加载为 com.lib/com.libInterface，本次未解密还原，故该部分静态不可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `1f5e3e5465c6d10ea80960a908dd75c123a295a4a49edf593f458a6253a3b773` |
| 包名 / 年份 | `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d` / 2020 |
| 家族 / 品类 | **EventBot**（同池样本数：124） |
| 原始来源标识 | https://www.cybereason.com/blog/eventbot-a-new-mobile-banking-trojan-is-born |
| 桌面显示名 | Flash Player |
| 引导页宣称品牌/身份 | Adobe Flash Player（Android 平台上已不存在该产品，纯属伪造品牌身份） |
| 系统无障碍列表服务名 | Flash Player |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用名、无障碍服务 label、引导文案三者统一冒用 Flash Player 品牌；无障碍配置 description 以“不开启就无法正常使用”为由施加功能恐吓；另用 banner_text 的 System updating, please wait... 旋转加载页充当假更新掩护；类名/服务名全为随机小写字母串（erhesr、tblvifn、tvpeqghuln、vkiiukmqt），核心逻辑藏于 RC4 加密 DEX，未发现空白挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool 的静态证据。 |
| 无障碍服务类名 | `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.erhesr` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | You must enable Flash Player in order to get full functionality of the application. Flash Player will not work correctly. |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.vkiiukmqt（LAUNCHER Activity，无自定义 UI 主题） | 用户点击桌面图标 Flash Player，onCreate 回调 | 原生Activity | **原文**：无（onCreate 中 startService(new Intent(this, tblvifn.class)) 后立即 finish()，界面不呈现任何内容）<br>**译注**：无可见界面：启动瞬间闪退式关闭，同时静默拉起后台服务 | 无需操作，用户仅感知为“点开即关”或直接进入下一步 | `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.vkiiukmqt#onCreate` |
| 2 | 冷启动入口 | com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn（Service）+ DexClassLoader 装载 assets/fonts/default.ttf | vkiiukmqt 调用 startService → tblvifn.onCreate 触发 a(this, 1, true) | 不可静态还原 | **原文**：无界面文本；载荷构造参数硬编码为 "eventBot"、"0.4.0.1"、"erhesr"、"flash401"<br>**译注**：无界面：服务在后台把 RC4 加密的 default.ttf 解密为 dex/MD5(MANUFACTURER+MODEL).jar，反射构造 com.libInterface 实例，取得后续所有 UI 与跳转的控制权 | 无 | `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a(Context,int,boolean) / com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a(File,String)` |
| 3 | 引导说明页 | com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln（FullScreen、NoActionBar Activity）+ 由 com.lib 加载的本地 HTML WebView 与截图 | tvpeqghuln.onCreate 中 d.doActivity(this, this, 2131296284, 2131165311, getIntent().getIntExtra("mode",0)) | 本地HTML WebView | **原文**：Select Flash Player in Settings（配图 1.jpg） / 2. Turn on it（配图 2.jpg）；按钮文案 Open Flash Player<br>**译注**：“在设置中选择 Flash Player”（附截图 1）、“2. 打开它”（附截图 2），配一个 Open Flash Player 按钮；多语言版本另备 es1/es2.jpg、it1/it2.jpg 截图 | 按图文分步教学：进入系统设置 → 找到 Flash Player → 打开开关；页面提供 Open Flash Player 按钮作为下一步入口（是否可取消由加密载荷控制） | `res/values/strings.xml: hint_text / hint_button；com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln#onCreate` |
| 4 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（由 com.libInterface 内部构造 Intent 拉起） | 用户点击 Open Flash Player 按钮 / com.lib 定时或生命周期回调触发跳转 | 系统无障碍页 | **原文**：无（系统页；应用侧仅以 Flash Player 作为列表项名称，描述为 You must enable Flash Player in order to get full functionality of the application. Flash Player will not work correctly.）<br>**译注**：系统无障碍服务列表中出现 “Flash Player”，其说明文字为“你必须启用 Flash Player 才能获得应用的完整功能。Flash Player 将无法正常工作。” | 在系统设置中手动把 Flash Player 的开关拨到开启 | `res/xml/accessibility_config.xml（android:description=@string/accessibility_config_text）；跳转 Intent 位于加密载荷 com.lib 内（classes.dex 无 ACTION_ACCESSIBILITY_SETTINGS 调用点）` |
| 5 | 遮罩叠层指引 / 拒权反馈循环 | tvpeqghuln 再次被 doActivity/doOnBackPressed 拉起 + banner_text 全屏 HTML（旋转 spinner） | 用户从设置页返回或点击返回键，Activity onBackPressed/onCreate 交由 com.libInterface 处理 | 本地HTML WebView | **原文**：System updating, please wait...<br>**译注**：“系统正在更新，请稍候……” 旋转加载动画，用于在等待/重试期间占满屏幕 | 只能等待（页面无实际进度，等待逻辑由加密载荷决定，可能反复回到步骤 3 的引导页） | `res/values/strings.xml: banner_text；com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln#onBackPressed` |
| 6 | 获权后动作 | com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.erhesr（AccessibilityService） | 系统绑定服务后 onServiceConnected 回调再次调用 tblvifn.a(...) 装载同一加密载荷 | 不可静态还原 | **原文**：无界面文本<br>**译注**：无障碍能力就绪后二阶段载荷被再次加载，事件监听（typeAllMask、flagRetrieveInteractiveWindows、flagRequestFilterKeyEvents、canRetrieveWindowContent）与后续短信读取、悬浮窗、安装包投放等行为进入可执行状态 | 无 | `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.erhesr#onServiceConnected / res/xml/accessibility_config.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：名称 = Flash Player（android:label=@string/app_name），说明 = You must enable Flash Player in order to get full functionality of the application. Flash Player will not work correctly.（@string/accessibility_config_text，经 res/xml/accessibility_config.xml 的 android:description 引用）
- tvpeqghuln 全屏 Activity 内由 com.lib 加载的本地 HTML WebView：分步教学文案 Select Flash Player in Settings / 2. Turn on it，配 assets/1.jpg、assets/2.jpg 截图（多语言时替换为 es1/es2.jpg、it1/it2.jpg）
- 同一 WebView 或原生按钮区的操作入口：hint_button = Open Flash Player
- 等待/掩护阶段全屏 HTML：banner_text 内 System updating, please wait... 旋转 spinner
- 桌面启动图标与系统任务栏标签：Flash Player（@string/app_name）
- （静态不可见）跳转 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 前的中间提示、拒权后重复引导文案，均由 RC4 加密的 com.lib 载荷动态构造，不在 res/values/strings.xml 中

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | You must enable Flash Player in order to get full functionality of the application. Flash Player will not work correctly. | 你必须启用 Flash Player 才能获得应用的完整功能。Flash Player 将无法正常工作。 | `res/values/strings.xml: accessibility_config_text（被 res/xml/accessibility_config.xml 的 android:description 引用）` | 故障恐吓 |
| en | Select Flash Player in Settings | 在设置中选择 Flash Player | `res/values/strings.xml: hint_text（HTML 片段，配图 1.jpg）` | 受限设置分步教学 |
| en | 2. Turn on it | 2. 把它打开 | `res/values/strings.xml: hint_text（HTML 片段，配图 2.jpg）` | 受限设置分步教学 |
| en | Open Flash Player | 打开 Flash Player | `res/values/strings.xml: hint_button` | 假更新 |
| en | System updating, please wait... | 系统正在更新，请稍候…… | `res/values/strings.xml: banner_text（内嵌 CSS 旋转 spinner 的 HTML）` | 假更新 |
| en | Flash Player | Flash Player（Adobe 已停服的播放器品牌） | `res/values/strings.xml: app_name（同时作为 android:label 与无障碍服务 label）` | 未知 |
| en | %1$s won't work unless you enable Google Play services. | 除非你启用 Google Play 服务，否则 %1$s 无法工作。 | `res/values/strings.xml: common_google_play_services_enable_text（Google Play services 官方库文案，非本应用自撰）` | 良性透明说明 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无法静态确认：tvpeqghuln 的 onCreate/onBackPressed/onDestroy 全部代理给 RC4 加密载荷的 com.libInterface.doActivity/doOnBackPressed，classes.dex 内不存在无障碍检测或重跳代码；从 banner_text 的 System updating 全屏等待页与 tvpeqghuln 可被反复拉起（mode 参数来自 Intent extra）推断存在返回后重新引导的循环，但具体间隔与次数需动态验证。
- **遮罩叠层 / 高仿系统设置页**：未发现高仿系统无障碍开关页的静态资源（res/layout 与 res/drawable 中无仿设置界面），但应用持有 SYSTEM_ALERT_WINDOW 且引导页为 FullScreen 无 ActionBar 主题、另有全屏 banner_text 假更新页，具备在系统设置页之上叠放遮罩的能力；是否实际叠放由加密载荷决定，静态不可见。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=21，未针对 Android 13 受限设置做教学；未见引导进入应用详情页右上角菜单允许受限设置，也未见 Session 安装器绕过代码）
- **获权后即时行为与防撤权机制**：无法静态确认（获权后 erhesr.onServiceConnected 会重新装载加密载荷，事件配置含 flagRetrieveInteractiveWindows 与 flagRequestFilterKeyEvents，具备监听设置页并模拟返回/回桌面的能力，但阻止撤权的具体实现位于 com.lib 内）
- **良性降级 / 替代方案**：无（未提供手动模式、仅观看模式或 ADB 替代路径；description 明确宣称不开启即无法正常工作）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：监测到当前前台为 com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln（FullScreen 无 ActionBar，通常在点击图标后 1 秒内出现）即开始抓取；同时在检测到 packageName 等于本包且 settingsIntent=android.settings.ACCESSIBILITY_SETTINGS 的系统设置页被拉起时抓第二张；随后用户返回应用瞬间再抓一次以观察是否重跳或叠遮罩。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区不是纯图空文本：引导文案为真实文本，可由 UTG 直接提取。真正的盲区是控制流——跳转 ACTION_ACCESSIBILITY_SETTINGS 的 Intent 构造、拒权重跳间隔、悬浮遮罩叠放全部位于 RC4 加密的第二阶段 DEX（assets/fonts/default.ttf → com.lib），静态不可见，只能靠运行期 UTG 观测；此外首屏 Activity 无任何 UI（启动即 finish），若只按“首屏文本”采样可能漏采，需以 tvpeqghuln 出现或无障碍设置页被拉起作为触发锚点。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的分步教学页（引导说明页）** | Activity=com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln，内容含文本 Select Flash Player in Settings、2. Turn on it、按钮 Open Flash Player 及两张截图 | 这是应用自身绘制的唯一诱导界面，直接证明其为“教用户去系统里开启 Flash Player 无障碍”的分步教学，而非真实播放器功能页 | 文本 Select Flash Player in Settings；文本 2. Turn on it；按钮 Open Flash Player；WebView 节点及其加载的本地 HTML/img（1.jpg、2.jpg）；Activity 为 FullScreen 无 ActionBar，无真实播放器控件 |
| **系统无障碍服务列表项** | Settings.ACTION_ACCESSIBILITY_SETTINGS 页面中 label=Flash Player 的条目及其描述文本 | 证明诱导终点确实是开启无障碍，且服务名与服务描述完全冒用 Flash Player 品牌并施加功能恐吓 | 无障碍列表项文本 Flash Player；描述 You must enable Flash Player in order to get full functionality of the application.；该条目开关的 checked 状态变化 |
| **返回后的假更新等待页/重复引导页** | tvpeqghuln 再次位于前台，内容为 System updating, please wait... 旋转 spinner，或回到教学页 | 区分“良性一次性引导”与“拒权后死循环强制”，是判定胁迫性的关键观测点 | 文本 System updating, please wait...；页面无任何进度或取消控件；从设置页返回后 tvpeqghuln 被重新拉起的次数与时间间隔；是否存在悬浮窗图层覆盖系统设置页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.vkiiukmqt#onCreate`
- `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a(Context,int,boolean)`
- `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a(File,String)`
- `com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln#onCreate`
- `res/values/strings.xml#hint_text`
- `res/xml/accessibility_config.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（定向核验，纯运行期 UTG 视角）

- **桌面图标叫 `Flash Player`，但启动 Activity 完全不显示界面**：[vkiiukmqt.onCreate()](<resource-unit:#1.dex1 code:com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.vkiiukmqt#onCreate>) 只执行 `startService(tblvifn)` 后立刻 `finish()`。因此“点图标→引导页”这一步不是由主 Activity 自身完成的。
- **引导界面全部由第二阶段（加密载荷）绘制**：[tblvifn.a(Context,int,boolean)](<resource-unit:#1.dex1 code:com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a>) 用 `DexClassLoader` 加载 `assets/fonts/default.ttf`（RC4 密钥硬编码在 [tblvifn.a(File,String)](<resource-unit:#1.dex1 code:com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a>)），得到 `com.lib`，并以 `"eventBot" / "0.4.0.1"`、无障碍服务名 `"erhesr"`、宿主 Activity `tvpeqghuln`、两个布局资源 id 与 `"flash401"` 构造 `com.libInterface`。
- **Activity 生命周期被完整代理**：[tvpeqghuln.onCreate()](<resource-unit:#1.dex1 code:com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln#onCreate>)（FullScreen 无 ActionBar 主题）把 `doActivity/doOnBackPressed/doOnDestroy` 全部交给解密后的 `com.libInterface` 执行。因此引导弹窗、WebView 与悬浮层的显示时机由加密载荷控制，`classes.dex` 内**没有任何** `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 字面量或调用点。
- **静态可见的引导素材确实存在且是“分步教学 + 假更新”组合**：`hint_text` 是一段本地 HTML（步骤 1 `Select Flash Player in Settings` + `1.jpg` 截图，步骤 2 `Turn on it` + `2.jpg` 截图），`hint_button` = `Open Flash Player`，`banner_text` 是带旋转 spinner 的 `System updating, please wait...` 全屏 HTML；`assets/` 内并存 `es1/es2.jpg`、`it1/it2.jpg` 多语言截图，说明按语言下发不同引导图。
- **身份与权限面**：无障碍服务 `erhesr` 的 `android:label="@string/app_name"`（= `Flash Player`），description 以“不开启就无法正常使用”恐吓；配置为 `typeAllMask` + `flagRetrieveInteractiveWindows` + `flagRequestFilterKeyEvents` + `canRetrieveWindowContent`，属读屏+读窗+截键的全量监视能力。同包还带 `READ_SMS/RECEIVE_SMS`、`SYSTEM_ALERT_WINDOW`、`REQUEST_INSTALL_PACKAGES`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`。
- **获权后动作**：`erhesr.onServiceConnected` 同样调用 `tblvifn.a(...)`，即核心控制逻辑只在无障碍授权后才启动。
- **覆盖边界**：跳转系统设置的 Intent 构造、拒绝后重跳逻辑、悬浮遮罩叠放均位于 RC4 加密的 `com.lib` 载荷内，本次未解包该 DEX，因此这部分为**静态不可见**（非远端 HTML，而是本地加密二阶段 DEX）。受调用预算约束，本轮未向风险台账写入记录。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍服务配置、全部引导文案/HTML/截图资源（strings.xml 的 hint_text、hint_button、banner_text，assets/1.jpg、2.jpg、es1/es2、it1/it2）以及载荷装载器 tblvifn 均可完整静态读取；但真正驱动引导页呈现、跳转 ACTION_ACCESSIBILITY_SETTINGS、拒权后重跳与悬浮遮罩的核心逻辑位于 assets/fonts/default.ttf —— 该文件为 RC4 加密的第二阶段 DEX（密钥硬编码 7e89013d...affd63），经 DexClassLoader 加载为 com.lib/com.libInterface，本次未解密还原，故该部分静态不可见。",
  "summary_one_liner": "桌面伪装成 Flash Player，启动即静默起服务并 RC4 解密加载 eventBot 二阶段 DEX，由该载荷在全屏 Activity 内用本地 HTML+截图做“选择 Flash Player 并打开”的分步无障碍开启教学，并以 System updating 假更新动画掩护，无障碍服务开启后才启动核心远控逻辑。",
  "disguise_identity": {
    "app_display_name": "Flash Player",
    "claimed_brand_or_persona": "Adobe Flash Player（Android 平台上已不存在该产品，纯属伪造品牌身份）",
    "a11y_service_label": "Flash Player",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用名、无障碍服务 label、引导文案三者统一冒用 Flash Player 品牌；无障碍配置 description 以“不开启就无法正常使用”为由施加功能恐吓；另用 banner_text 的 System updating, please wait... 旋转加载页充当假更新掩护；类名/服务名全为随机小写字母串（erhesr、tblvifn、tvpeqghuln、vkiiukmqt），核心逻辑藏于 RC4 加密 DEX，未发现空白挤出、同形字、多 activity-alias 或伪造 isAccessibilityTool 的静态证据。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.vkiiukmqt（LAUNCHER Activity，无自定义 UI 主题）",
      "trigger_event": "用户点击桌面图标 Flash Player，onCreate 回调",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（onCreate 中 startService(new Intent(this, tblvifn.class)) 后立即 finish()，界面不呈现任何内容）",
      "shown_text_zh": "无可见界面：启动瞬间闪退式关闭，同时静默拉起后台服务",
      "user_action_requested": "无需操作，用户仅感知为“点开即关”或直接进入下一步",
      "code_anchor": "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.vkiiukmqt#onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn（Service）+ DexClassLoader 装载 assets/fonts/default.ttf",
      "trigger_event": "vkiiukmqt 调用 startService → tblvifn.onCreate 触发 a(this, 1, true)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无界面文本；载荷构造参数硬编码为 \"eventBot\"、\"0.4.0.1\"、\"erhesr\"、\"flash401\"",
      "shown_text_zh": "无界面：服务在后台把 RC4 加密的 default.ttf 解密为 dex/MD5(MANUFACTURER+MODEL).jar，反射构造 com.libInterface 实例，取得后续所有 UI 与跳转的控制权",
      "user_action_requested": "无",
      "code_anchor": "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a(Context,int,boolean) / com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a(File,String)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln（FullScreen、NoActionBar Activity）+ 由 com.lib 加载的本地 HTML WebView 与截图",
      "trigger_event": "tvpeqghuln.onCreate 中 d.doActivity(this, this, 2131296284, 2131165311, getIntent().getIntExtra(\"mode\",0))",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Select Flash Player in Settings（配图 1.jpg） / 2. Turn on it（配图 2.jpg）；按钮文案 Open Flash Player",
      "shown_text_zh": "“在设置中选择 Flash Player”（附截图 1）、“2. 打开它”（附截图 2），配一个 Open Flash Player 按钮；多语言版本另备 es1/es2.jpg、it1/it2.jpg 截图",
      "user_action_requested": "按图文分步教学：进入系统设置 → 找到 Flash Player → 打开开关；页面提供 Open Flash Player 按钮作为下一步入口（是否可取消由加密载荷控制）",
      "code_anchor": "res/values/strings.xml: hint_text / hint_button；com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln#onCreate"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS（由 com.libInterface 内部构造 Intent 拉起）",
      "trigger_event": "用户点击 Open Flash Player 按钮 / com.lib 定时或生命周期回调触发跳转",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（系统页；应用侧仅以 Flash Player 作为列表项名称，描述为 You must enable Flash Player in order to get full functionality of the application. Flash Player will not work correctly.）",
      "shown_text_zh": "系统无障碍服务列表中出现 “Flash Player”，其说明文字为“你必须启用 Flash Player 才能获得应用的完整功能。Flash Player 将无法正常工作。”",
      "user_action_requested": "在系统设置中手动把 Flash Player 的开关拨到开启",
      "code_anchor": "res/xml/accessibility_config.xml（android:description=@string/accessibility_config_text）；跳转 Intent 位于加密载荷 com.lib 内（classes.dex 无 ACTION_ACCESSIBILITY_SETTINGS 调用点）"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引 / 拒权反馈循环",
      "screen_or_component": "tvpeqghuln 再次被 doActivity/doOnBackPressed 拉起 + banner_text 全屏 HTML（旋转 spinner）",
      "trigger_event": "用户从设置页返回或点击返回键，Activity onBackPressed/onCreate 交由 com.libInterface 处理",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "System updating, please wait...",
      "shown_text_zh": "“系统正在更新，请稍候……” 旋转加载动画，用于在等待/重试期间占满屏幕",
      "user_action_requested": "只能等待（页面无实际进度，等待逻辑由加密载荷决定，可能反复回到步骤 3 的引导页）",
      "code_anchor": "res/values/strings.xml: banner_text；com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln#onBackPressed"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.erhesr（AccessibilityService）",
      "trigger_event": "系统绑定服务后 onServiceConnected 回调再次调用 tblvifn.a(...) 装载同一加密载荷",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无界面文本",
      "shown_text_zh": "无障碍能力就绪后二阶段载荷被再次加载，事件监听（typeAllMask、flagRetrieveInteractiveWindows、flagRequestFilterKeyEvents、canRetrieveWindowContent）与后续短信读取、悬浮窗、安装包投放等行为进入可执行状态",
      "user_action_requested": "无",
      "code_anchor": "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.erhesr#onServiceConnected / res/xml/accessibility_config.xml"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：名称 = Flash Player（android:label=@string/app_name），说明 = You must enable Flash Player in order to get full functionality of the application. Flash Player will not work correctly.（@string/accessibility_config_text，经 res/xml/accessibility_config.xml 的 android:description 引用）",
    "tvpeqghuln 全屏 Activity 内由 com.lib 加载的本地 HTML WebView：分步教学文案 Select Flash Player in Settings / 2. Turn on it，配 assets/1.jpg、assets/2.jpg 截图（多语言时替换为 es1/es2.jpg、it1/it2.jpg）",
    "同一 WebView 或原生按钮区的操作入口：hint_button = Open Flash Player",
    "等待/掩护阶段全屏 HTML：banner_text 内 System updating, please wait... 旋转 spinner",
    "桌面启动图标与系统任务栏标签：Flash Player（@string/app_name）",
    "（静态不可见）跳转 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS_SETTINGS 前的中间提示、拒权后重复引导文案，均由 RC4 加密的 com.lib 载荷动态构造，不在 res/values/strings.xml 中"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "You must enable Flash Player in order to get full functionality of the application. Flash Player will not work correctly.",
      "text_zh": "你必须启用 Flash Player 才能获得应用的完整功能。Flash Player 将无法正常工作。",
      "source_location": "res/values/strings.xml: accessibility_config_text（被 res/xml/accessibility_config.xml 的 android:description 引用）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Select Flash Player in Settings",
      "text_zh": "在设置中选择 Flash Player",
      "source_location": "res/values/strings.xml: hint_text（HTML 片段，配图 1.jpg）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "2. Turn on it",
      "text_zh": "2. 把它打开",
      "source_location": "res/values/strings.xml: hint_text（HTML 片段，配图 2.jpg）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Open Flash Player",
      "text_zh": "打开 Flash Player",
      "source_location": "res/values/strings.xml: hint_button",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "System updating, please wait...",
      "text_zh": "系统正在更新，请稍候……",
      "source_location": "res/values/strings.xml: banner_text（内嵌 CSS 旋转 spinner 的 HTML）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Flash Player",
      "text_zh": "Flash Player（Adobe 已停服的播放器品牌）",
      "source_location": "res/values/strings.xml: app_name（同时作为 android:label 与无障碍服务 label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "除非你启用 Google Play 服务，否则 %1$s 无法工作。",
      "source_location": "res/values/strings.xml: common_google_play_services_enable_text（Google Play services 官方库文案，非本应用自撰）",
      "rhetorical_frame": "良性透明说明"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无法静态确认：tvpeqghuln 的 onCreate/onBackPressed/onDestroy 全部代理给 RC4 加密载荷的 com.libInterface.doActivity/doOnBackPressed，classes.dex 内不存在无障碍检测或重跳代码；从 banner_text 的 System updating 全屏等待页与 tvpeqghuln 可被反复拉起（mode 参数来自 Intent extra）推断存在返回后重新引导的循环，但具体间隔与次数需动态验证。",
    "overlay_or_fake_settings": "未发现高仿系统无障碍开关页的静态资源（res/layout 与 res/drawable 中无仿设置界面），但应用持有 SYSTEM_ALERT_WINDOW 且引导页为 FullScreen 无 ActionBar 主题、另有全屏 banner_text 假更新页，具备在系统设置页之上叠放遮罩的能力；是否实际叠放由加密载荷决定，静态不可见。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=21，未针对 Android 13 受限设置做教学；未见引导进入应用详情页右上角菜单允许受限设置，也未见 Session 安装器绕过代码）",
    "post_grant_anti_removal": "无法静态确认（获权后 erhesr.onServiceConnected 会重新装载加密载荷，事件配置含 flagRetrieveInteractiveWindows 与 flagRequestFilterKeyEvents，具备监听设置页并模拟返回/回桌面的能力，但阻止撤权的具体实现位于 com.lib 内）",
    "benign_graceful_degradation": "无（未提供手动模式、仅观看模式或 ADB 替代路径；description 明确宣称不开启即无法正常工作）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "监测到当前前台为 com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln（FullScreen 无 ActionBar，通常在点击图标后 1 秒内出现）即开始抓取；同时在检测到 packageName 等于本包且 settingsIntent=android.settings.ACCESSIBILITY_SETTINGS 的系统设置页被拉起时抓第二张；随后用户返回应用瞬间再抓一次以观察是否重跳或叠遮罩。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的分步教学页（引导说明页）",
        "page_identifier": "Activity=com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln，内容含文本 Select Flash Player in Settings、2. Turn on it、按钮 Open Flash Player 及两张截图",
        "why_most_useful": "这是应用自身绘制的唯一诱导界面，直接证明其为“教用户去系统里开启 Flash Player 无障碍”的分步教学，而非真实播放器功能页",
        "observable_utg_signals": ["文本 Select Flash Player in Settings", "文本 2. Turn on it", "按钮 Open Flash Player", "WebView 节点及其加载的本地 HTML/img（1.jpg、2.jpg）", "Activity 为 FullScreen 无 ActionBar，无真实播放器控件"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings.ACTION_ACCESSIBILITY_SETTINGS 页面中 label=Flash Player 的条目及其描述文本",
        "why_most_useful": "证明诱导终点确实是开启无障碍，且服务名与服务描述完全冒用 Flash Player 品牌并施加功能恐吓",
        "observable_utg_signals": ["无障碍列表项文本 Flash Player", "描述 You must enable Flash Player in order to get full functionality of the application.", "该条目开关的 checked 状态变化"]
      },
      {
        "page_role": "返回后的假更新等待页/重复引导页",
        "page_identifier": "tvpeqghuln 再次位于前台，内容为 System updating, please wait... 旋转 spinner，或回到教学页",
        "why_most_useful": "区分“良性一次性引导”与“拒权后死循环强制”，是判定胁迫性的关键观测点",
        "observable_utg_signals": ["文本 System updating, please wait...", "页面无任何进度或取消控件", "从设置页返回后 tvpeqghuln 被重新拉起的次数与时间间隔", "是否存在悬浮窗图层覆盖系统设置页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区不是纯图空文本：引导文案为真实文本，可由 UTG 直接提取。真正的盲区是控制流——跳转 ACTION_ACCESSIBILITY_SETTINGS 的 Intent 构造、拒权重跳间隔、悬浮遮罩叠放全部位于 RC4 加密的第二阶段 DEX（assets/fonts/default.ttf → com.lib），静态不可见，只能靠运行期 UTG 观测；此外首屏 Activity 无任何 UI（启动即 finish），若只按“首屏文本”采样可能漏采，需以 tvpeqghuln 出现或无障碍设置页被拉起作为触发锚点。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED"
  ],
  "code_anchors": [
    "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.vkiiukmqt#onCreate",
    "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a(Context,int,boolean)",
    "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tblvifn#a(File,String)",
    "com.bf4eba1fcde137.dc20a2a5.bcc9909d03e33ddf0b3d.tvpeqghuln#onCreate",
    "res/values/strings.xml#hint_text",
    "res/xml/accessibility_config.xml"
  ]
}
```

</details>
