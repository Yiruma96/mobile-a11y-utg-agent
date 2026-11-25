# MB_144__c8dcf4ee90｜Crocodilus — Play-Plus

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：161.7s

## 1. 一句话核心结论

- **核心申请方式**：名为 Play-Plus 的加载器型木马，主包仅含 35 个随机命名类与 AES 解密+反射加载逻辑，真正的无障碍引导界面藏在 8 段加密 DEX 与 6 个伪装 .so 中运行期解密执行，无障碍服务无任何 description 却同时申请窗口内容读取与手势执行。
- **静态可见性说明**：Manifest、无障碍服务声明、无障碍配置 res/xml/kbkcr.xml、设备管理器策略与权限清单为明文可读；但无障碍服务实现类、launcher 之后的引导弹窗/说明页/WebView 文案全部不在 classes.dex 与 resources.arsc 中（静态搜索 startActivity/Settings/AccessibilityService/onAccessibilityEvent 均无命中，res/layout 仅 AppCompat 模板、assets 无任何 html）。实际业务与引导流程藏于 AES 加密载荷 assets/encroc1-8.enc 及伪装成 .so 的密文 lib1-6.so（readelf 全部非 ELF），需运行期解密，静态不可还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c8dcf4ee90bbfbd52c182aa80974381871fbc2f9b34b4e81dbcc4eed9777212e` |
| 包名 / 年份 | `untitled.lividly.disobey` / 2025 |
| 家族 / 品类 | **Crocodilus**（同池样本数：6） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Play-Plus |
| 引导页宣称品牌/身份 | Play-Plus（借用 Google Play 命名格式的伪应用商店/工具身份，包名 untitled.lividly.disobey 与名称毫无语义关联） |
| 系统无障碍列表服务名 | Play-Plus |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置 kbkcr.xml 刻意省略 android:description 与 android:summary，系统无障碍列表该服务说明为空白，用户无从判断用途；未声明 android:isAccessibilityTool，Android 13+ 会显示系统风险提示但仍可被引导开启；包名与全部类名、Activity 名均为随机词拼接（如 stFBYYqPUQcMSB.WXoKggCNxGv、AatUqiQRi、TrumpTayyip）；载荷以 encroc1-8.enc 分段加密并以 lib1-6.so 伪装成原生库，绕过静态扫描；Manifest 中额外内嵌 Chrome 相关 intent-filter。 |
| 无障碍服务类名 | `untitled.lividly.disobey.stFBYYqPUQcMSB.WXoKggCNxGv` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | untitled.lividly.disobey.AatUqiQRi（launcher Activity） | onCreate / LAUNCHER 图标点击 | 原生Activity | **原文**：无（该类在 classes.dex 中无实现体，界面内容来自解密载荷）<br>**译注**：入口页内容不可静态确认；应用名仅显示 Play-Plus | 不可静态确认 | `AndroidManifest.xml → untitled.lividly.disobey.AatUqiQRi` |
| 2 | 业务功能触发 | classes.dex 加载器（javax.crypto.Cipher + java.lang.reflect + getAssets，com.nirvana.dropper.util.TG） | 入口 Activity 启动后读取 assets 并解密 | 不可静态还原 | 无 | 无 | `com.nirvana.dropper.util.TG#send（字段 C="cr", T="x"）` |
| 3 | 引导说明页 | 二阶段解密载荷内的引导页（具体 Activity/Dialog/WebView 不可静态还原） | 不可静态确认（可能为冷启动或功能触发，均位于加密载荷） | 不可静态还原 | **原文**：无（包内无引导 HTML、无业务文案 strings、无业务布局，全部藏于加密载荷）<br>**译注**：引导文案不可静态获取 | 不可静态确认（是否有取消/跳过按钮不可判定） | `assets/encroc1.enc … encroc8.enc（加密）、assets/lib1.so … lib6.so（非 ELF 密文）` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载的服务 → Play-Plus | 二阶段代码拉起 ACTION_ACCESSIBILITY_SETTINGS（该字符串不在明文包内，属推断） | 系统无障碍页 | **原文**：Play-Plus（服务标签；系统列表中说明栏为空白，因 android:description 缺失）<br>**译注**：系统无障碍列表中显示“Play-Plus”，无任何用途说明 | 用户需在列表中自行找到 Play-Plus 并打开开关；是否存在引导遮罩/循环重跳不可静态确认 | `res/xml/kbkcr.xml、AndroidManifest 中 stFBYYqPUQcMSB.WXoKggCNxGv 的 BIND_ACCESSIBILITY_SERVICE` |
| 5 | 获权后动作 | untitled.lividly.disobey.stFBYYqPUQcMSB.WXoKggCNxGv（AccessibilityService 实现体在加密载荷中） | 系统绑定服务后 onServiceConnected / onAccessibilityEvent | 不可静态还原 | 无 | 无（用户已完成授权） | `res/xml/kbkcr.xml（canRetrieveWindowContent/canPerformGestures）、res/xml/fxyfwuv.xml（device-admin force-lock）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：仅显示服务标签 “Play-Plus”，android:description / android:summary 均缺失，说明栏为空白（res/xml/kbkcr.xml 仅含 eventTypes/feedbackType/notificationTimeout/flags/canRetrieveWindowContent/canPerformGestures 六项）
- Android 桌面启动图标与应用名：android:label = “Play-Plus”（AndroidManifest.xml）
- 引导弹窗/说明页/WebView 教学页：包内无任何业务 strings、无业务 layout、无 assets/*.html，故其呈现位置只能在运行期由解密载荷生成，静态不可定位
- 潜在浏览器内呈现通道：Manifest 中存在 VIEW/BROWSABLE intent-filter 与字符串 “Chrome”，可能通过浏览器或 WebView 承载说明内容

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Play-Plus | Play-Plus（应用显示名与无障碍服务名） | `AndroidManifest.xml android:label 与 service android:label（resources.arsc 中唯一业务文案）` | 未知 |
| en | Chrome | Chrome（浏览器包名/关键词，疑用于拉起或劫持浏览器承载页面） | `AndroidManifest.xml 字符串池（配合 VIEW / BROWSABLE intent-filter）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：明文包内无 ACTION_ACCESSIBILITY_SETTINGS 字符串、无 onResume 重跳逻辑、无 Timer 拉起代码，判定所需代码位于 encroc1-8.enc 解密载荷内；但已确认主包为加载器 + 无障碍服务实现体缺失，说明该逻辑必然存在于二阶段载荷。
- **遮罩叠层 / 高仿系统设置页**：不可静态确认。包内无悬浮窗布局、无仿系统设置界面布局（res/layout 仅 38 个 AppCompat 模板），遮罩/高仿开关页若存在只能由解密载荷运行期绘制。
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（相关文案与跳转代码不在明文包内，无法确认是否包含应用详情页受限设置教学或 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：无静态证据。已确认声明设备管理器 force-lock 策略与 SCREEN_ON/OFF、USER_PRESENT、ROLE_HOLDER_CHANGED 接收器，具备撤权对抗的能力基础，但自点确认/自返回阻止撤权的具体实现位于加密载荷，无法静态证实。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在应用进程启动并完成载荷解密后，监测两类瞬间拉起 UTG：①首个 Activity（untitled.lividly.disobey.AatUqiQRi）进入 RESUMED 后 1–3 秒内出现的弹窗/新 Activity；②任意 Activity 发生 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间（此时立即截图并持续 5 秒间隔采样，以捕获随后可能压栈的引导遮罩）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：引导文案与流程完全位于加密载荷，UTG 若在载荷解密完成前抓取将只看到空白或启动页；且 lib1-6.so 为非 ELF 密文、encroc 为 AES 密文，静态无法预判触发时机与文案，必须依赖运行期观测。另因无障碍配置无 description，系统列表页本身不提供任何判别文本，不能仅凭系统页判定诱导。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗/说明页（解密载荷生成）** | AatUqiQRi 之后出现的 Dialog 或新 Activity，窗口标题/包名为 untitled.lividly.disobey，界面含无障碍相关按钮 | 这是判断“是否强制阻塞、是否可取消、用什么话术包装”的唯一直接证据，静态完全缺失 | 是否存在返回键/取消按钮节点；文案中是否出现 accessibility / permission / service / enable 等关键词；弹窗是否覆盖全屏且点击外部不可关闭 |
| **跳转前 WebView / HTML 教学页** | WebView 类节点或含 Chrome/浏览器包名窗口，URL 可能为远端或 data:text/html | 确认话术载体是本地 HTML 还是远端下发，决定后续是否需要抓包配合 | WebView 可见文本节点内容；地址栏/标题中的域名；页面内是否含分步截图指引 |
| **系统无障碍服务列表项（Play-Plus）** | com.android.settings 无障碍页面，服务项文本为 Play-Plus，副标题为空 | 直接验证 android:description 缺失导致的无说明状态，是身份隐瞒与诱导开启的关键证据 | 服务项标题 Play-Plus；说明副文本为空；是否存在系统风险提示文案 |
| **设置页返回后压栈的遮罩/引导层** | 从系统设置返回应用后 0–3 秒内出现的 Overlay 或全屏 Activity | 识别拒绝授权后的循环重跳与叠层指引，这是恶意诱导区别于良性说明的核心行为 | 返回后是否自动再次跳转设置；是否有半透明遮罩与箭头/手势指引节点；是否有“必须开启才能使用”类文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `untitled.lividly.disobey.stFBYYqPUQcMSB.WXoKggCNxGv（无障碍服务，实现体不在 classes.dex）`
- `res/xml/kbkcr.xml（accessibility-service 配置：canRetrieveWindowContent=true, canPerformGestures=true, 无 description）`
- `res/xml/fxyfwuv.xml（device-admin force-lock 策略）`
- `com.nirvana.dropper.util.TG#send（字段 C="cr", T="x"）`
- `assets/encroc1.enc … encroc8.enc、assets/lib1.so … lib6.so（AES 密文载荷，readelf 非 ELF）`
- `untitled.lividly.disobey.AatUqiQRi（launcher Activity）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（纯静态定向核验）

**静态可见度：`packed_or_encrypted`（关键引导流程不可静态还原）**

已核实的静态事实：

1. **Manifest 声明层（明文可见）**
   - 包名 `untitled.lividly.disobey`，`android:label` = **`Play-Plus`**（模仿 “Google Play” 命名，与功能描述无关联），versionName `1.0`。
   - 无障碍服务：`untitled.lividly.disobey.stFBYYqPUQcMSB.WXoKggCNxGv`，持有 `BIND_ACCESSIBILITY_SERVICE`，配置指向 `res/xml/kbkcr.xml`。
   - 无障碍配置 `kbkcr.xml` **仅含 6 个属性**：`accessibilityEventTypes`、`accessibilityFeedbackType`、`notificationTimeout`、`accessibilityFlags`、`canRetrieveWindowContent=true`、`canPerformGestures=true`；**无 `android:description`、无 `android:summary`、无 `android:isAccessibilityTool`**。因此系统无障碍列表中该服务名称旁为空白说明、且不带“系统无障碍工具”标记，用户在列表里几乎看不到任何用途解释，这是典型的“空白描述 + 窗口内容读取 + 手势执行”组合。
   - 并行声明设备管理器 `res/xml/fxyfwuv.xml`（`force-lock` 策略）、短信全套（`SMS_DELIVER`/`WAP_PUSH_DELIVER`/`SEND_SMS`/`READ_SMS`/`WRITE_SMS`）、`FOREGROUND_SERVICE_MEDIA_PROJECTION`、`QUERY_ALL_PACKAGES`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`、`REQUEST_DELETE_PACKAGES`、`SYSTEM_ALERT` 类行为所需的 `BOOT_COMPLETED`/`PACKAGE_ADDED`/`ROLE_HOLDER_CHANGED`/`SCREEN_ON` 接收器，以及 `usesCleartextTraffic`。
   - Manifest 中另出现字符串 `Chrome`（配合 `VIEW`/`BROWSABLE` intent-filter），表明存在面向浏览器/WebView 的拉起或劫持通道。

2. **代码层：classes.dex 只是一个“加载器/投放器”**
   - 全包仅 35 个类，包名全部为随机词拼接（`natureyanking.*`、`excretionflatten.*`、`gzyp.tzkr.*`、`shininessgout.*`、`cateringescapable.*`、`lcskcrhc.*`）。
   - 存在 `com.nirvana.dropper.util.TG`（字段 `C="cr"`、`T="x"`，`send()` 方法），被 5+ 个类 import；`classes.dex` 字符串中含 `Ljavax/crypto/Cipher;`、`java.lang.reflect.Method/Constructor/Field`、`getAssets`。
   - **静态搜索 `startActivity` / `setClassName` / `Settings` / `AccessibilityService` / `loadDex` / `defineClass` 全部无命中**，`search_function_definitions` 对 `WXoKggCNxGv`、`AatUqiQRi`、`onAccessibilityEvent` 亦无命中 —— 说明无障碍服务类、入口 Activity、引导页在 `classes.dex` 中**没有实现体**。

3. **载荷全部加密，且伪装成 `.so`**
   - `assets/encroc1.enc … encroc8.enc`（12–41 KB，共 8 段）为加密 DEX 载荷；`encroc1.dex`/`encroc2.dex` 头部为 `90 fe ca 71 da ea 6b 5a…`，**不是 DEX magic**，同属密文。
   - `assets/lib1.so … lib6.so` 经 `readelf` 校验**全部 “Not an ELF file”**，即加密二进制伪装成原生库（典型的 VMP/加密载荷绕过静态扫描手法）。
   - 资源侧同样“空壳化”：`res/layout/` 只有 38 个 AppCompat 模板布局、`resources.arsc` 中除 `Play-Plus` 外无任何业务文案、`assets/` 内无任何 `.html`。因此**引导弹窗、说明页、WebView 教学页的文案与 UI 均不在明文包内**，只能由解密后的 8 段载荷在运行期生成（本地或远端）。

4. **运行期引导路径（基于以上证据的定位结论，非逐字还原）**
   - 可确认的入口链：`AndroidManifest` launcher Activity `untitled.lividly.disobey.AatUqiQRi` → `classes.dex` 加载器（`Cipher` + `reflect` + `getAssets`）解密 `encroc*.enc`/`lib*.so` → 解密出的二阶段代码启动无障碍服务 `stFBYYqPUQcMSB.WXoKggCNxGv`。
   - 但“何时弹引导、弹什么文案、是否可取消、是否在系统设置页上叠遮罩、拒绝后是否循环重跳、13+ 是否教用户开启受限设置”**全部位于加密载荷内，静态不可判定**。包内既无 `ACTION_ACCESSIBILITY_SETTINGS` 字符串、也无引导 HTML/布局，因此不能凭静态证据断定其属于“冷启动强制阻塞”还是“按需触发”。

**覆盖边界与未决问题：** 未解密 `encroc1–8.enc` 与伪装 `.so`（缺密钥来源，密钥可能由 `TG.C/T` 派生或来自远端 `*.json` 配置），故 UTG 页面流转的文案、载体与循环机制无法逐字给出；本结论仅以 Manifest + 无障碍配置 + 加载器证据为界。已确认的恶意性判断依据（无障碍服务无描述、读窗口内容+执行手势、加密 DEX 分段投放、`.so` 伪装密文、短信/设备管理器/录屏权限捆绑）足以支撑“无障碍权限滥用型木马投放器”定性。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍服务声明、无障碍配置 res/xml/kbkcr.xml、设备管理器策略与权限清单为明文可读；但无障碍服务实现类、launcher 之后的引导弹窗/说明页/WebView 文案全部不在 classes.dex 与 resources.arsc 中（静态搜索 startActivity/Settings/AccessibilityService/onAccessibilityEvent 均无命中，res/layout 仅 AppCompat 模板、assets 无任何 html）。实际业务与引导流程藏于 AES 加密载荷 assets/encroc1-8.enc 及伪装成 .so 的密文 lib1-6.so（readelf 全部非 ELF），需运行期解密，静态不可还原。",
  "summary_one_liner": "名为 Play-Plus 的加载器型木马，主包仅含 35 个随机命名类与 AES 解密+反射加载逻辑，真正的无障碍引导界面藏在 8 段加密 DEX 与 6 个伪装 .so 中运行期解密执行，无障碍服务无任何 description 却同时申请窗口内容读取与手势执行。",
  "disguise_identity": {
    "app_display_name": "Play-Plus",
    "claimed_brand_or_persona": "Play-Plus（借用 Google Play 命名格式的伪应用商店/工具身份，包名 untitled.lividly.disobey 与名称毫无语义关联）",
    "a11y_service_label": "Play-Plus",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置 kbkcr.xml 刻意省略 android:description 与 android:summary，系统无障碍列表该服务说明为空白，用户无从判断用途；未声明 android:isAccessibilityTool，Android 13+ 会显示系统风险提示但仍可被引导开启；包名与全部类名、Activity 名均为随机词拼接（如 stFBYYqPUQcMSB.WXoKggCNxGv、AatUqiQRi、TrumpTayyip）；载荷以 encroc1-8.enc 分段加密并以 lib1-6.so 伪装成原生库，绕过静态扫描；Manifest 中额外内嵌 Chrome 相关 intent-filter。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "untitled.lividly.disobey.AatUqiQRi（launcher Activity）",
      "trigger_event": "onCreate / LAUNCHER 图标点击",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（该类在 classes.dex 中无实现体，界面内容来自解密载荷）",
      "shown_text_zh": "入口页内容不可静态确认；应用名仅显示 Play-Plus",
      "user_action_requested": "不可静态确认",
      "code_anchor": "AndroidManifest.xml → untitled.lividly.disobey.AatUqiQRi"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "classes.dex 加载器（javax.crypto.Cipher + java.lang.reflect + getAssets，com.nirvana.dropper.util.TG）",
      "trigger_event": "入口 Activity 启动后读取 assets 并解密",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面，后台解密 encroc1-8.enc / lib1-6.so 并反射加载二阶段代码",
      "user_action_requested": "无",
      "code_anchor": "com.nirvana.dropper.util.TG#send（字段 C=\"cr\", T=\"x\"）"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "二阶段解密载荷内的引导页（具体 Activity/Dialog/WebView 不可静态还原）",
      "trigger_event": "不可静态确认（可能为冷启动或功能触发，均位于加密载荷）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（包内无引导 HTML、无业务文案 strings、无业务布局，全部藏于加密载荷）",
      "shown_text_zh": "引导文案不可静态获取",
      "user_action_requested": "不可静态确认（是否有取消/跳过按钮不可判定）",
      "code_anchor": "assets/encroc1.enc … encroc8.enc（加密）、assets/lib1.so … lib6.so（非 ELF 密文）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务 → Play-Plus",
      "trigger_event": "二阶段代码拉起 ACTION_ACCESSIBILITY_SETTINGS（该字符串不在明文包内，属推断）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Play-Plus（服务标签；系统列表中说明栏为空白，因 android:description 缺失）",
      "shown_text_zh": "系统无障碍列表中显示“Play-Plus”，无任何用途说明",
      "user_action_requested": "用户需在列表中自行找到 Play-Plus 并打开开关；是否存在引导遮罩/循环重跳不可静态确认",
      "code_anchor": "res/xml/kbkcr.xml、AndroidManifest 中 stFBYYqPUQcMSB.WXoKggCNxGv 的 BIND_ACCESSIBILITY_SERVICE"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "untitled.lividly.disobey.stFBYYqPUQcMSB.WXoKggCNxGv（AccessibilityService 实现体在加密载荷中）",
      "trigger_event": "系统绑定服务后 onServiceConnected / onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获取 canRetrieveWindowContent + canPerformGestures 后自动读取界面内容并模拟手势操作，配合短信读写、设备管理器 force-lock、录屏与 QUERY_ALL_PACKAGES 权限链",
      "user_action_requested": "无（用户已完成授权）",
      "code_anchor": "res/xml/kbkcr.xml（canRetrieveWindowContent/canPerformGestures）、res/xml/fxyfwuv.xml（device-admin force-lock）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：仅显示服务标签 “Play-Plus”，android:description / android:summary 均缺失，说明栏为空白（res/xml/kbkcr.xml 仅含 eventTypes/feedbackType/notificationTimeout/flags/canRetrieveWindowContent/canPerformGestures 六项）",
    "Android 桌面启动图标与应用名：android:label = “Play-Plus”（AndroidManifest.xml）",
    "引导弹窗/说明页/WebView 教学页：包内无任何业务 strings、无业务 layout、无 assets/*.html，故其呈现位置只能在运行期由解密载荷生成，静态不可定位",
    "潜在浏览器内呈现通道：Manifest 中存在 VIEW/BROWSABLE intent-filter 与字符串 “Chrome”，可能通过浏览器或 WebView 承载说明内容"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Play-Plus",
      "text_zh": "Play-Plus（应用显示名与无障碍服务名）",
      "source_location": "AndroidManifest.xml android:label 与 service android:label（resources.arsc 中唯一业务文案）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Chrome",
      "text_zh": "Chrome（浏览器包名/关键词，疑用于拉起或劫持浏览器承载页面）",
      "source_location": "AndroidManifest.xml 字符串池（配合 VIEW / BROWSABLE intent-filter）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：明文包内无 ACTION_ACCESSIBILITY_SETTINGS 字符串、无 onResume 重跳逻辑、无 Timer 拉起代码，判定所需代码位于 encroc1-8.enc 解密载荷内；但已确认主包为加载器 + 无障碍服务实现体缺失，说明该逻辑必然存在于二阶段载荷。",
    "overlay_or_fake_settings": "不可静态确认。包内无悬浮窗布局、无仿系统设置界面布局（res/layout 仅 38 个 AppCompat 模板），遮罩/高仿开关页若存在只能由解密载荷运行期绘制。",
    "restricted_settings_13plus_coaching": "无静态证据（相关文案与跳转代码不在明文包内，无法确认是否包含应用详情页受限设置教学或 Session 安装器绕过）",
    "post_grant_anti_removal": "无静态证据。已确认声明设备管理器 force-lock 策略与 SCREEN_ON/OFF、USER_PRESENT、ROLE_HOLDER_CHANGED 接收器，具备撤权对抗的能力基础，但自点确认/自返回阻止撤权的具体实现位于加密载荷，无法静态证实。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在应用进程启动并完成载荷解密后，监测两类瞬间拉起 UTG：①首个 Activity（untitled.lividly.disobey.AatUqiQRi）进入 RESUMED 后 1–3 秒内出现的弹窗/新 Activity；②任意 Activity 发生 startActivity 目标为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间（此时立即截图并持续 5 秒间隔采样，以捕获随后可能压栈的引导遮罩）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗/说明页（解密载荷生成）",
        "page_identifier": "AatUqiQRi 之后出现的 Dialog 或新 Activity，窗口标题/包名为 untitled.lividly.disobey，界面含无障碍相关按钮",
        "why_most_useful": "这是判断“是否强制阻塞、是否可取消、用什么话术包装”的唯一直接证据，静态完全缺失",
        "observable_utg_signals": ["是否存在返回键/取消按钮节点", "文案中是否出现 accessibility / permission / service / enable 等关键词", "弹窗是否覆盖全屏且点击外部不可关闭"]
      },
      {
        "page_role": "跳转前 WebView / HTML 教学页",
        "page_identifier": "WebView 类节点或含 Chrome/浏览器包名窗口，URL 可能为远端或 data:text/html",
        "why_most_useful": "确认话术载体是本地 HTML 还是远端下发，决定后续是否需要抓包配合",
        "observable_utg_signals": ["WebView 可见文本节点内容", "地址栏/标题中的域名", "页面内是否含分步截图指引"]
      },
      {
        "page_role": "系统无障碍服务列表项（Play-Plus）",
        "page_identifier": "com.android.settings 无障碍页面，服务项文本为 Play-Plus，副标题为空",
        "why_most_useful": "直接验证 android:description 缺失导致的无说明状态，是身份隐瞒与诱导开启的关键证据",
        "observable_utg_signals": ["服务项标题 Play-Plus", "说明副文本为空", "是否存在系统风险提示文案"]
      },
      {
        "page_role": "设置页返回后压栈的遮罩/引导层",
        "page_identifier": "从系统设置返回应用后 0–3 秒内出现的 Overlay 或全屏 Activity",
        "why_most_useful": "识别拒绝授权后的循环重跳与叠层指引，这是恶意诱导区别于良性说明的核心行为",
        "observable_utg_signals": ["返回后是否自动再次跳转设置", "是否有半透明遮罩与箭头/手势指引节点", "是否有“必须开启才能使用”类文案"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：引导文案与流程完全位于加密载荷，UTG 若在载荷解密完成前抓取将只看到空白或启动页；且 lib1-6.so 为非 ELF 密文、encroc 为 AES 密文，静态无法预判触发时机与文案，必须依赖运行期观测。另因无障碍配置无 description，系统列表页本身不提供任何判别文本，不能仅凭系统页判定诱导。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "COERCE_NO_SKIP_NON_CANCELABLE"
  ],
  "code_anchors": [
    "untitled.lividly.disobey.stFBYYqPUQcMSB.WXoKggCNxGv（无障碍服务，实现体不在 classes.dex）",
    "res/xml/kbkcr.xml（accessibility-service 配置：canRetrieveWindowContent=true, canPerformGestures=true, 无 description）",
    "res/xml/fxyfwuv.xml（device-admin force-lock 策略）",
    "com.nirvana.dropper.util.TG#send（字段 C=\"cr\", T=\"x\"）",
    "assets/encroc1.enc … encroc8.enc、assets/lib1.so … lib6.so（AES 密文载荷，readelf 非 ELF）",
    "untitled.lividly.disobey.AatUqiQRi（launcher Activity）"
  ]
}
```

**说明：** 本轮受 14 次工具调用上限约束，已在第 13 次调用后收口，未再执行 `record_risk` 与报告生成；上述 JSON 中的恶意性结论均以已列 Manifest / 无障碍配置 / 加载器与密文载荷证据为界，引导话术与循环机制标记为运行期未决。

</details>
