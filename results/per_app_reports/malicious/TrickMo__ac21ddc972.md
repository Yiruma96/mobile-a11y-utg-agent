# MB_014__ac21ddc972｜TrickMo — TikTok18

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：185.2s

## 1. 一句话核心结论

- **核心申请方式**：以 TikTok18 为壳，用本地明文 HTML 伪装 Google 服务过旧并分步教用户进设置开启'Downloaded Services'中的服务，真实无障碍服务与跳转逻辑藏在 DexClassLoader 加载的加密载荷内
- **静态可见性说明**：诱导页面模板 assets/hint.html 为明文完整可见（含假更新话术与 step_1/2/3 无障碍开启教学）；但无障碍服务实现类、ACTION_ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS 跳转点、拒权循环与遮罩引导时序均不在明文 DEX（可见 DEX 无任何 AccessibilityService/BIND_ACCESSIBILITY_SERVICE 字符串），实际逻辑位于经 DexClassLoader 加载的 AES 密文载荷 oinymxI.json、v1-configuration.jsa、v1-strings.jsa 与加密 zip 条目 deper.apk 中，静态不可还原
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ac21ddc972b50c66a9876f1a470f0a29f4df58c1557b8fa0ba649fc0b255dd37` |
| 包名 / 年份 | `nvyfee.dcvxvm.zsakxl` / 2025 |
| 家族 / 品类 | **TrickMo**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | TikTok18 |
| 引导页宣称品牌/身份 | TikTok18 / Google（Google Play 服务、Google 账号登录页） |
| 系统无障碍列表服务名 | 不可静态还原（预筛无障碍服务标签为空，标签由加密载荷在运行期注册，模板中以 app_title 即 TikTok18 代入 step_3 'Activate services for the TikTok18'） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 nvyfee.dcvxvm.zsakxl 与品牌完全无关；核心类置于 com.hospital.two 伪命名空间并用 Emosquitosample/Nalreadyprivate 等无意义标识符；页面模板通过 %LANG%/%IS_XIAOMI%/%IS_SAMSUNG% 占位符在运行期按设备品牌替换系统菜单名（Downloaded Services / Downloaded apps / Installed apps）以匹配各厂商设置界面；关键代码以 DexClassLoader 反射方式从密文资产加载，规避明文静态检测 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_INSTALL_PACKAGES` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | 承载 assets/hint.html 的 WebView 容器 Activity（明文 DEX 中无对应无障碍相关 Activity，具体宿主类不可静态还原） | 冷启动加载本地 HTML 模板，脚本 setTimeout 1500ms 后由 #step_0 切至 #step_1 | 本地HTML WebView | **原文**：Welcome to TikTok18 / Continue with Google / Already have an account? Log in / By continuing with an account located in IT, you agree to our Terms of Service and acknowledge you have read our Privacy Policy and Cookies Policy.<br>**译注**：欢迎使用 TikTok18；使用 Google 继续；已有账号？登录；以位于 IT 的账号继续即表示同意服务条款、隐私政策与 Cookie 政策 | 点击'使用 Google 继续'或'登录'推进；无跳过/取消按钮 | `assets/hint.html（app_title='TikTok18'，$(document).ready 中 setTimeout 切换 #step_0→#step_1）` |
| 2 | 引导说明页 | #step_1 页面内的假更新对话框（HTML 覆盖层） | 点击 #step_1 .btnmy 或 .log_in 后 #step_1 隐藏、#p2 显示；同时弹出 dialog_text 假更新弹窗 | 本地HTML WebView | **原文**：You are using an outdated version of Google services.<br><br>- New version 24.01.03 (183004-871692384)<br><br>Update google services for the correct Google Chrome work. / Accept & continue / Update<br>**译注**：你正在使用过时的 Google 服务版本。新版本 24.01.03 (183004-871692384)。请更新 Google 服务以保证 Chrome 正常工作。按钮：接受并继续 / 更新 | 仅可点击'接受并继续'/'更新'，无取消或稍后按钮 | `assets/hint.html（dialog_text / dialog_btn / btn1 变量与 #step_1 .btnmy 点击绑定）` |
| 3 | 跳受限设置 | 系统'安装未知应用/允许来自此来源'页面（配合 REQUEST_INSTALL_PACKAGES 与假更新包下载安装） | 点击'更新'后由加密载荷内的代码发起安装/跳转（明文 DEX 未见该跳转，不可静态还原） | 系统设置页 | **原文**：To continue using TikTok18 you will need to update Google services / Update TikTok18 ? / Update size: 5.2MB / Install activity<br>**译注**：要继续使用 TikTok18 需要更新 Google 服务；是否更新 TikTok18？更新大小 5.2MB；安装界面 | 确认更新并安装 APK；未见取消路径说明 | `预筛字符串（Install activity / Update app / Update size: 5.2MB，位于加密载荷或二进制资源）；权限 REQUEST_INSTALL_PACKAGES` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务（小米：已下载应用；三星：已安装应用）列表页 | 跳转 ACTION_ACCESSIBILITY_SETTINGS 的代码位于加密载荷，明文 DEX 无此字符串，触发点不可静态还原 | 不可静态还原 | **原文**：Step 1. - Go to Settings / Step 2. - Open "Downloaded Services" menu / Step 2. - Open "Downloaded apps" menu / Step 2. - Open "Installed apps" menu<br>**译注**：第 1 步：进入设置；第 2 步：打开'已下载的服务'（小米为'已下载应用'、三星为'已安装应用'）菜单 | 按指引逐级进入系统无障碍服务列表；无跳过选项 | `assets/hint.html（step_1 / step_2 / step_2_xiaomi / step_2_samsung 变量）` |
| 5 | 遮罩叠层指引 | 系统无障碍服务列表项（服务名以 TikTok18 呈现） | 用户在列表中找到并点开该服务条目（触发代码在加密载荷内） | 系统无障碍页 | **原文**：Step 3. - Activate services for the <a>TikTok18</a><br>**译注**：第 3 步：为 TikTok18 启用服务 | 在系统无障碍列表中为 TikTok18 服务打开开关并确认授权 | `assets/hint.html（step_3 = "Step 3. - Activate services for the <a>" + app_title + "</a>"）` |
| 6 | 获权后动作 | 无障碍服务本体（实现类在加密载荷中，名称不可静态还原） | 服务被系统绑定后 onServiceConnected 等回调（不可静态还原） | 不可静态还原 | 无 | 无（自动执行读屏/模拟点击等能力） | `不可静态还原（位于 oinymxI.json / deper.apk 解密后的 DEX）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets/hint.html：本地 WebView 页面，先呈现 Google 账号登录仿冒页（Continue with Google / Already have an account? Log in）
- assets/hint.html #step_1 覆盖层：假 Google 服务过旧更新弹窗（dialog_text + dialog_btn），无取消按钮
- assets/hint.html #p2 / step 区块：三步无障碍开启图文教学（Go to Settings → Downloaded Services → Activate services for TikTok18）
- assets/hint.html 顶部红色提示条（red_top 变量）：'You are using an outdated version of Google Play services...'
- 预筛字符串（加密载荷/二进制资源中）：'To continue using TikTok18 you will need to update Google services'、'Update TikTok18 ?'、'Update size: 5.2MB'、'Update app'、'Update time!'、'Install activity'
- 系统无障碍列表项：android:description 静态缺失，服务名与说明由加密载荷在运行期注册，预期显示为 TikTok18

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | You are using an outdated version of Google services.<br><br>- New version 24.01.03 (183004-871692384)<br><br>Update google services for the correct Google Chrome work. | 你正在使用过时的 Google 服务版本。新版本 24.01.03 (183004-871692384)。请更新 Google 服务以保证 Google Chrome 正常运行。 | `assets/hint.html（dialog_text 变量，默认 en 分支）` | 假更新 |
| en | Step 1. - Go to Settings | 第 1 步：进入设置 | `assets/hint.html（step_1 变量）` | 受限设置分步教学 |
| en | Step 2. - Open "Downloaded Services" menu | 第 2 步：打开“已下载的服务”菜单（小米为“已下载应用”，三星为“已安装应用”） | `assets/hint.html（step_2 / step_2_xiaomi / step_2_samsung 变量）` | 受限设置分步教学 |
| en | Step 3. - Activate services for the <a>TikTok18</a> | 第 3 步：为 TikTok18 启用服务 | `assets/hint.html（step_3 变量，app_title='TikTok18'）` | 受限设置分步教学 |
| en | Accept & continue | 接受并继续 | `assets/hint.html（btn1 变量）` | 假更新 |
| en | To continue using TikTok18 you will need to update Google services | 要继续使用 TikTok18，你需要更新 Google 服务 | `预筛字符串（加密载荷/资源，DEFAULT）` | 假更新 |
| en | Update TikTok18 ? / Update size: 5.2MB / Update app / Install activity | 是否更新 TikTok18？/ 更新大小：5.2MB / 更新应用 / 安装界面 | `预筛字符串（加密载荷/资源，DEFAULT）` | 假更新 |
| en | Continue with Google / Already have an account? Log in | 使用 Google 继续 / 已有账号？登录 | `assets/hint.html（登录仿冒页正文）` | 假更新 |
| es/fr/other | Estás utilizando una versión desactualizada de los servicios de Google Play. Actualiza los servicios de Google Play para que TikTok18 funcione correctamente. | 你正在使用过时的 Google Play 服务版本。请更新 Google Play 服务以便 TikTok18 正常运行。 | `assets/hint.html（red_top 变量，es 分支；同一模板另有 fr 等多语言分支）` | 假更新 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：模板侧仅见 setTimeout 1500ms 自动推进与 #step_1 点击后切页，返回系统设置后的重跳/循环逻辑位于加密载荷 oinymxI.json（DexClassLoader 加载），明文 DEX 无相关代码
- **遮罩叠层 / 高仿系统设置页**：本地 HTML 内使用多层覆盖 div（#step_0/#step_1/#p2/#black_lay/#wait_div）模拟遮罩与加载层；是否在系统无障碍页上方压全屏悬浮窗不可静态还原
- **Android 13+ 受限设置（Restricted Settings）应对**：未见针对 Android 13+ 受限设置的'应用详情右上角菜单允许受限设置'或 Session 安装器绕过文案；仅见针对厂商无障碍菜单名称（Downloaded Services / Downloaded apps / Installed apps）的分步教学，且配合 REQUEST_INSTALL_PACKAGES 走假更新安装路径
- **获权后即时行为与防撤权机制**：不可静态还原（明文 DEX 无 GLOBAL_ACTION_BACK/HOME 或 AccessibilityNodeInfo 自点确认代码，相关能力应在加密载荷内）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 WebView 加载本地 assets/hint.html（file:// 或 asset:// 路径含 hint.html）或监测到 Intent 目标为 Settings.ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 时立即拉起 UTG 快照；冷启动 1.5 秒后页面自动切换为假更新弹窗，建议冷启动即开始连续抓帧
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在盲区：无障碍服务实现与全部设置跳转、拒权循环、遮罩时序均封装在 AES 密文资产（oinymxI.json / v1-configuration.jsa / v1-strings.jsa）及加密 zip 条目 deper.apk 中，由 DexClassLoader 反射加载，纯静态 UTG 无法覆盖跳转瞬间的组件名；此外第一阶段为 Dropper 形态（假更新引导安装 APK），真正持权载体可能是被安装的二阶段包。静态加壳不阻挡运行期 UTG，建议以运行期抓帧 + Intent 监测为主

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页** | WebView 内 'Continue with Google' + 'You are using an outdated version of Google services' 弹窗与 'Accept & continue' 按钮 | 证明应用以假 Google 服务更新话术作为无障碍引导的入口话术，且无取消按钮，是区分诱导与非良性说明的第一现场 | 弹窗文本 'outdated version of Google services'；按钮仅 'Accept & continue'/'Update'，无 Cancel/Skip 节点；WebView 控件类型与 file:///android_asset/hint.html 来源 |
| **跳转前 WebView 教学页** | 含 'Step 1. - Go to Settings' / 'Step 2. - Open "Downloaded Services" menu' / 'Step 3. - Activate services for the TikTok18' 的三步图文页 | 直接暴露应用在教用户为自身启用无障碍服务，且菜单名随设备品牌动态替换，属无障碍诱导的决定性文本证据 | 'Activate services for the TikTok18' 文本；步骤编号 Step 1/2/3 与厂商化菜单名；页面中 app_title 与实际服务名一致性 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务/已安装的应用 下显示为 TikTok18 的条目及其描述文本 | 确认服务标签与真实功能声明不符（无静态 android:description，运行期注入），验证身份冒用 | 服务名 'TikTok18'；description 文本为空或与更新/系统服务相关的伪描述；所属应用包名 nvyfee.dcvxvm.zsakxl 与品牌不符 |
| **设置页后压栈遮罩页** | 跳转系统设置后 800ms 内出现的悬浮窗/全屏覆盖层 | 识别是否以 TYPE_APPLICATION_OVERLAY 遮罩把用户点击引向服务开关，是强制引导的关键判别信号 | 同进程 overlay 窗口层级；覆盖层文本与 HTML 步骤文本一致；覆盖层上箭头/高亮指向系统开关 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `assets/hint.html（app_title='TikTok18'、dialog_text 假更新、step_1/step_2/step_3 无障碍开启教学、setTimeout 1500 自动推进）`
- `com.hospital.two.Emosquitosample#textweird（反射构造 DexClassLoader 加载外部 DEX）`
- `com.hospital.two.Nalreadyprivate#Ywhenodor（常量 "oinymxI.json" 指认密文载荷）`
- `assets/oinymxI.json（587KB 高熵密文载荷，AES/加密资源）`
- `assets/deper.apk（8.4MB，内部 classes.dex 与 AndroidManifest.xml 条目加密需口令）`
- `assets/v1-configuration.jsa / assets/v1-strings.jsa（加密配置与文案资源）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**可见部分（明文，完整）**
- 诱导内容预置在 [assets/hint.html](<resource-unit:#1 file:assets/hint.html>)（217KB 本地 HTML），内含完整仿 Google 账号/Play 服务更新页面：`app_title='TikTok18'`、`app_title2='Google'`，并自带"Google 服务版本过旧需更新（新版本 24.01.03）"弹窗文案与"更新"按钮。
- 同一模板内含无障碍开启分步教学：`step_1="Step 1. - Go to Settings"`、`step_2="Step 2. - Open \"Downloaded Services\" menu"`（按 `%IS_XIAOMI%`→Downloaded apps、`%IS_SAMSUNG%`→Installed apps 分支替换）、`step_3="Step 3. - Activate services for the <a>TikTok18</a>"`，并含 `btn1="Accept & continue"`；页面以 `setTimeout(...,1500)` 从 `step_0` 自动切到 `step_1`，`#step_1 .btnmy` 点击后切到 `#p2`，属脚本驱动的多步页面流转。
- 页面初始为 Google 登录仿冒页（"Continue with Google"、"Already have an account? Log in"），用于包装"更新/登录"外壳。

**不可见部分（加密载荷）**
- 可见 DEX 中**完全不存在** `AccessibilityService`、`BIND_ACCESSIBILITY_SERVICE`、`ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS` 字符串，也无无障碍服务类声明，与预筛 `无障碍服务类=[]` 一致——无障碍服务实现与设置跳转代码不在明文 DEX。
- 载荷经动态加载：`com.hospital.two.Nalreadyprivate` 以常量 `oinymxI.json` 指认密文资产，[com.hospital.two.Emosquitosample#textweird](<resource-unit:C:/Users/admin/AppData/Local/Temp/trk2/classes.dex code:com.hospital.two.Emosquitosample#textweird>) 通过反射构造 `DexClassLoader` 装载外部 DEX。
- 密文资产：[oinymxI.json](<resource-unit:C:/Users/admin/AppData/Local/Temp/trk2/oinymxI.json>)（587KB 高熵）、`assets/v1-configuration.jsa`、`assets/v1-strings.jsa`、[deper.apk](<resource-unit:#1 file:assets/deper.apk>)（8.4MB，其内部 `classes.dex`/`AndroidManifest.xml` 条目本身加密需口令）。因此**运行期跳转时序、拒权循环、设置页遮罩等 UTG 视角页面流转无法静态还原**。

**判定**
明文模板已构成完整诱导链路的一半（假更新话术 + 分步无障碍开启教学 + 品牌冒用），加密二次载荷承载实际跳转与读屏控制。已登记风险 R-001（malware_trojan / high）。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "诱导页面模板 assets/hint.html 为明文完整可见（含假更新话术与 step_1/2/3 无障碍开启教学）；但无障碍服务实现类、ACTION_ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS 跳转点、拒权循环与遮罩引导时序均不在明文 DEX（可见 DEX 无任何 AccessibilityService/BIND_ACCESSIBILITY_SERVICE 字符串），实际逻辑位于经 DexClassLoader 加载的 AES 密文载荷 oinymxI.json、v1-configuration.jsa、v1-strings.jsa 与加密 zip 条目 deper.apk 中，静态不可还原",
  "summary_one_liner": "以 TikTok18 为壳，用本地明文 HTML 伪装 Google 服务过旧并分步教用户进设置开启'Downloaded Services'中的服务，真实无障碍服务与跳转逻辑藏在 DexClassLoader 加载的加密载荷内",
  "disguise_identity": {
    "app_display_name": "TikTok18",
    "claimed_brand_or_persona": "TikTok18 / Google（Google Play 服务、Google 账号登录页）",
    "a11y_service_label": "不可静态还原（预筛无障碍服务标签为空，标签由加密载荷在运行期注册，模板中以 app_title 即 TikTok18 代入 step_3 'Activate services for the TikTok18'）",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 nvyfee.dcvxvm.zsakxl 与品牌完全无关；核心类置于 com.hospital.two 伪命名空间并用 Emosquitosample/Nalreadyprivate 等无意义标识符；页面模板通过 %LANG%/%IS_XIAOMI%/%IS_SAMSUNG% 占位符在运行期按设备品牌替换系统菜单名（Downloaded Services / Downloaded apps / Installed apps）以匹配各厂商设置界面；关键代码以 DexClassLoader 反射方式从密文资产加载，规避明文静态检测"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "承载 assets/hint.html 的 WebView 容器 Activity（明文 DEX 中无对应无障碍相关 Activity，具体宿主类不可静态还原）",
      "trigger_event": "冷启动加载本地 HTML 模板，脚本 setTimeout 1500ms 后由 #step_0 切至 #step_1",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Welcome to TikTok18 / Continue with Google / Already have an account? Log in / By continuing with an account located in IT, you agree to our Terms of Service and acknowledge you have read our Privacy Policy and Cookies Policy.",
      "shown_text_zh": "欢迎使用 TikTok18；使用 Google 继续；已有账号？登录；以位于 IT 的账号继续即表示同意服务条款、隐私政策与 Cookie 政策",
      "user_action_requested": "点击'使用 Google 继续'或'登录'推进；无跳过/取消按钮",
      "code_anchor": "assets/hint.html（app_title='TikTok18'，$(document).ready 中 setTimeout 切换 #step_0→#step_1）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "#step_1 页面内的假更新对话框（HTML 覆盖层）",
      "trigger_event": "点击 #step_1 .btnmy 或 .log_in 后 #step_1 隐藏、#p2 显示；同时弹出 dialog_text 假更新弹窗",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "You are using an outdated version of Google services.<br><br>- New version 24.01.03 (183004-871692384)<br><br>Update google services for the correct Google Chrome work. / Accept & continue / Update",
      "shown_text_zh": "你正在使用过时的 Google 服务版本。新版本 24.01.03 (183004-871692384)。请更新 Google 服务以保证 Chrome 正常工作。按钮：接受并继续 / 更新",
      "user_action_requested": "仅可点击'接受并继续'/'更新'，无取消或稍后按钮",
      "code_anchor": "assets/hint.html（dialog_text / dialog_btn / btn1 变量与 #step_1 .btnmy 点击绑定）"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统'安装未知应用/允许来自此来源'页面（配合 REQUEST_INSTALL_PACKAGES 与假更新包下载安装）",
      "trigger_event": "点击'更新'后由加密载荷内的代码发起安装/跳转（明文 DEX 未见该跳转，不可静态还原）",
      "ui_carrier": "系统设置页",
      "shown_text_verbatim": "To continue using TikTok18 you will need to update Google services / Update TikTok18 ? / Update size: 5.2MB / Install activity",
      "shown_text_zh": "要继续使用 TikTok18 需要更新 Google 服务；是否更新 TikTok18？更新大小 5.2MB；安装界面",
      "user_action_requested": "确认更新并安装 APK；未见取消路径说明",
      "code_anchor": "预筛字符串（Install activity / Update app / Update size: 5.2MB，位于加密载荷或二进制资源）；权限 REQUEST_INSTALL_PACKAGES"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务（小米：已下载应用；三星：已安装应用）列表页",
      "trigger_event": "跳转 ACTION_ACCESSIBILITY_SETTINGS 的代码位于加密载荷，明文 DEX 无此字符串，触发点不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Step 1. - Go to Settings / Step 2. - Open \"Downloaded Services\" menu / Step 2. - Open \"Downloaded apps\" menu / Step 2. - Open \"Installed apps\" menu",
      "shown_text_zh": "第 1 步：进入设置；第 2 步：打开'已下载的服务'（小米为'已下载应用'、三星为'已安装应用'）菜单",
      "user_action_requested": "按指引逐级进入系统无障碍服务列表；无跳过选项",
      "code_anchor": "assets/hint.html（step_1 / step_2 / step_2_xiaomi / step_2_samsung 变量）"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "系统无障碍服务列表项（服务名以 TikTok18 呈现）",
      "trigger_event": "用户在列表中找到并点开该服务条目（触发代码在加密载荷内）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Step 3. - Activate services for the <a>TikTok18</a>",
      "shown_text_zh": "第 3 步：为 TikTok18 启用服务",
      "user_action_requested": "在系统无障碍列表中为 TikTok18 服务打开开关并确认授权",
      "code_anchor": "assets/hint.html（step_3 = \"Step 3. - Activate services for the <a>\" + app_title + \"</a>\"）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务本体（实现类在加密载荷中，名称不可静态还原）",
      "trigger_event": "服务被系统绑定后 onServiceConnected 等回调（不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（获权后界面表现需动态观测）",
      "user_action_requested": "无（自动执行读屏/模拟点击等能力）",
      "code_anchor": "不可静态还原（位于 oinymxI.json / deper.apk 解密后的 DEX）"
    }
  ],
  "text_presentation_locations": [
    "assets/hint.html：本地 WebView 页面，先呈现 Google 账号登录仿冒页（Continue with Google / Already have an account? Log in）",
    "assets/hint.html #step_1 覆盖层：假 Google 服务过旧更新弹窗（dialog_text + dialog_btn），无取消按钮",
    "assets/hint.html #p2 / step 区块：三步无障碍开启图文教学（Go to Settings → Downloaded Services → Activate services for TikTok18）",
    "assets/hint.html 顶部红色提示条（red_top 变量）：'You are using an outdated version of Google Play services...'",
    "预筛字符串（加密载荷/二进制资源中）：'To continue using TikTok18 you will need to update Google services'、'Update TikTok18 ?'、'Update size: 5.2MB'、'Update app'、'Update time!'、'Install activity'",
    "系统无障碍列表项：android:description 静态缺失，服务名与说明由加密载荷在运行期注册，预期显示为 TikTok18"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "You are using an outdated version of Google services.<br><br>- New version 24.01.03 (183004-871692384)<br><br>Update google services for the correct Google Chrome work.",
      "text_zh": "你正在使用过时的 Google 服务版本。新版本 24.01.03 (183004-871692384)。请更新 Google 服务以保证 Google Chrome 正常运行。",
      "source_location": "assets/hint.html（dialog_text 变量，默认 en 分支）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1. - Go to Settings",
      "text_zh": "第 1 步：进入设置",
      "source_location": "assets/hint.html（step_1 变量）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 2. - Open \"Downloaded Services\" menu",
      "text_zh": "第 2 步：打开“已下载的服务”菜单（小米为“已下载应用”，三星为“已安装应用”）",
      "source_location": "assets/hint.html（step_2 / step_2_xiaomi / step_2_samsung 变量）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 3. - Activate services for the <a>TikTok18</a>",
      "text_zh": "第 3 步：为 TikTok18 启用服务",
      "source_location": "assets/hint.html（step_3 变量，app_title='TikTok18'）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Accept & continue",
      "text_zh": "接受并继续",
      "source_location": "assets/hint.html（btn1 变量）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "To continue using TikTok18 you will need to update Google services",
      "text_zh": "要继续使用 TikTok18，你需要更新 Google 服务",
      "source_location": "预筛字符串（加密载荷/资源，DEFAULT）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Update TikTok18 ? / Update size: 5.2MB / Update app / Install activity",
      "text_zh": "是否更新 TikTok18？/ 更新大小：5.2MB / 更新应用 / 安装界面",
      "source_location": "预筛字符串（加密载荷/资源，DEFAULT）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Continue with Google / Already have an account? Log in",
      "text_zh": "使用 Google 继续 / 已有账号？登录",
      "source_location": "assets/hint.html（登录仿冒页正文）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "es/fr/other",
      "text_verbatim": "Estás utilizando una versión desactualizada de los servicios de Google Play. Actualiza los servicios de Google Play para que TikTok18 funcione correctamente.",
      "text_zh": "你正在使用过时的 Google Play 服务版本。请更新 Google Play 服务以便 TikTok18 正常运行。",
      "source_location": "assets/hint.html（red_top 变量，es 分支；同一模板另有 fr 等多语言分支）",
      "rhetorical_frame": "假更新"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：模板侧仅见 setTimeout 1500ms 自动推进与 #step_1 点击后切页，返回系统设置后的重跳/循环逻辑位于加密载荷 oinymxI.json（DexClassLoader 加载），明文 DEX 无相关代码",
    "overlay_or_fake_settings": "本地 HTML 内使用多层覆盖 div（#step_0/#step_1/#p2/#black_lay/#wait_div）模拟遮罩与加载层；是否在系统无障碍页上方压全屏悬浮窗不可静态还原",
    "restricted_settings_13plus_coaching": "未见针对 Android 13+ 受限设置的'应用详情右上角菜单允许受限设置'或 Session 安装器绕过文案；仅见针对厂商无障碍菜单名称（Downloaded Services / Downloaded apps / Installed apps）的分步教学，且配合 REQUEST_INSTALL_PACKAGES 走假更新安装路径",
    "post_grant_anti_removal": "不可静态还原（明文 DEX 无 GLOBAL_ACTION_BACK/HOME 或 AccessibilityNodeInfo 自点确认代码，相关能力应在加密载荷内）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 WebView 加载本地 assets/hint.html（file:// 或 asset:// 路径含 hint.html）或监测到 Intent 目标为 Settings.ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 时立即拉起 UTG 快照；冷启动 1.5 秒后页面自动切换为假更新弹窗，建议冷启动即开始连续抓帧",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页",
        "page_identifier": "WebView 内 'Continue with Google' + 'You are using an outdated version of Google services' 弹窗与 'Accept & continue' 按钮",
        "why_most_useful": "证明应用以假 Google 服务更新话术作为无障碍引导的入口话术，且无取消按钮，是区分诱导与非良性说明的第一现场",
        "observable_utg_signals": ["弹窗文本 'outdated version of Google services'", "按钮仅 'Accept & continue'/'Update'，无 Cancel/Skip 节点", "WebView 控件类型与 file:///android_asset/hint.html 来源"]
      },
      {
        "page_role": "跳转前 WebView 教学页",
        "page_identifier": "含 'Step 1. - Go to Settings' / 'Step 2. - Open \"Downloaded Services\" menu' / 'Step 3. - Activate services for the TikTok18' 的三步图文页",
        "why_most_useful": "直接暴露应用在教用户为自身启用无障碍服务，且菜单名随设备品牌动态替换，属无障碍诱导的决定性文本证据",
        "observable_utg_signals": ["'Activate services for the TikTok18' 文本", "步骤编号 Step 1/2/3 与厂商化菜单名", "页面中 app_title 与实际服务名一致性"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务/已安装的应用 下显示为 TikTok18 的条目及其描述文本",
        "why_most_useful": "确认服务标签与真实功能声明不符（无静态 android:description，运行期注入），验证身份冒用",
        "observable_utg_signals": ["服务名 'TikTok18'", "description 文本为空或与更新/系统服务相关的伪描述", "所属应用包名 nvyfee.dcvxvm.zsakxl 与品牌不符"]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "跳转系统设置后 800ms 内出现的悬浮窗/全屏覆盖层",
        "why_most_useful": "识别是否以 TYPE_APPLICATION_OVERLAY 遮罩把用户点击引向服务开关，是强制引导的关键判别信号",
        "observable_utg_signals": ["同进程 overlay 窗口层级", "覆盖层文本与 HTML 步骤文本一致", "覆盖层上箭头/高亮指向系统开关"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在盲区：无障碍服务实现与全部设置跳转、拒权循环、遮罩时序均封装在 AES 密文资产（oinymxI.json / v1-configuration.jsa / v1-strings.jsa）及加密 zip 条目 deper.apk 中，由 DexClassLoader 反射加载，纯静态 UTG 无法覆盖跳转瞬间的组件名；此外第一阶段为 Dropper 形态（假更新引导安装 APK），真正持权载体可能是被安装的二阶段包。静态加壳不阻挡运行期 UTG，建议以运行期抓帧 + Intent 监测为主"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "assets/hint.html（app_title='TikTok18'、dialog_text 假更新、step_1/step_2/step_3 无障碍开启教学、setTimeout 1500 自动推进）",
    "com.hospital.two.Emosquitosample#textweird（反射构造 DexClassLoader 加载外部 DEX）",
    "com.hospital.two.Nalreadyprivate#Ywhenodor（常量 \"oinymxI.json\" 指认密文载荷）",
    "assets/oinymxI.json（587KB 高熵密文载荷，AES/加密资源）",
    "assets/deper.apk（8.4MB，内部 classes.dex 与 AndroidManifest.xml 条目加密需口令）",
    "assets/v1-configuration.jsa / assets/v1-strings.jsa（加密配置与文案资源）"
  ]
}
```

</details>
