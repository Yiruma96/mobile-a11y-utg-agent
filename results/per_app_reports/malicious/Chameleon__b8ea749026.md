# MB_018__b8ea749026｜Chameleon — Employee CRM

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：144.9s

## 1. 一句话核心结论

- **核心申请方式**：外层 com.stub 不含无障碍代码，而是用本地 HTML 伪造企业 CRM 登录页 + 12 秒假加载 + '请重装应用' 假故障，诱导点击 Reinstall 后经 PackageInstaller 静默安装内嵌的 com.wrap.jump（含无障碍服务与 9 个品牌伪装别名），由二阶段自行完成无障碍授权请求。
- **静态可见性说明**：外层 com.stub 完全静态可见：Manifest、assets/iluqsryxvf.html 全文、JS 桥与 PackageInstaller 调用均已还原，无加壳无加密。不可见部分为二阶段 com.wrap.jump（assets/xecvbzvspk.apk）：类名重度混淆（OYa733fe2bfd.OYa18fb8cc9d...），res/xml/accessibility.xml 与 layout_accessibility_restriction.xml 经 apktool 错位命名未能还原，无障碍引导页的具体逐字文案与 ACTION_ACCESSIBILITY_SETTINGS 跳转调用点未闭环；外层 WebView 另有远端地址 https://crmlogin.info 未取回。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_WEBVIEW_LOCAL_HTML`（本地离线HTML/WebView引导页）、`LURE_SYSTEM_ERROR_OR_OPTIMIZE`（假运行故障/性能崩溃/必需启用胁迫）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b8ea74902684dcced62a5ca2c1d6932659decfefcbdb2615bfe5899e05eb1451` |
| 包名 / 年份 | `com.stub` / 2024 |
| 家族 / 品类 | **Chameleon**（同池样本数：3） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Employee CRM |
| 引导页宣称品牌/身份 | 企业 CRM 员工登录门户（Employee CRM / 远端域 crmlogin.info） |
| 系统无障碍列表服务名 | 外层无无障碍服务；二阶段服务类为 OYa733fe2bfd.OYa18fb8cc9d.OY616fa84021.OY2540ff909d，其 android:label 与 accessibilityservice meta-data 属性在反编译中错位未能取出 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 桌面名 Employee CRM 与真实行为（APK 投递器）不符；2) 二阶段以 9 个 activity-alias 复用同一 targetActivity OYa733fe2bfd.OYa18fb8cc9d.OYabb1d7fa0d.OYd16cb90138，分别标注 Gmail、Facebook、Youtube、Google Play、Telegram、Contacts、Discord、Photos、Chrome 及 @string/app_name；3) 二阶段类名整体混淆为 OYa733fe2bfd.OYa18fb8cc9d 系列；4) 二阶段 Manifest 属性名被注入伪命名空间（compileSdkVersion/@null/APKTOOL_MISSING_0）干扰静态解析；5) 内嵌 APK 以随机串文件名 xecvbzvspk.apk 存放于 assets |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_INSTALL_PACKAGES` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.stub.webview.MainActivity（全屏 WebView，theme Theme.Webview，requestWindowFeature(1) + FLAG_FULLSCREEN） | LAUNCHER 启动 → onCreate() 创建 WebView 并调用 e() | 本地HTML WebView | **原文**：Hey,<br>Login Now<br>**译注**：嗨，立即登录 | 无提示、无授权说明，直接进入伪造的登录页 | `com.stub.webview.MainActivity.onCreate / com.stub.webview.MainActivity.e` |
| 2 | 业务功能触发 | WebView 内 form（input placeholder="Employee ID"，submit value="Next"，附 Forgot password? 链接） | 用户输入员工号并点击 Next（form submit 事件，e.preventDefault()） | 本地HTML WebView | **原文**：Employee ID \| Next \| Forgot password?<br>**译注**：员工工号 ｜ 下一步 ｜ 忘记密码？ | 输入任意非空工号后点击 Next；输入为空时仅把边框标红并 return，仍留在本页 | `assets/iluqsryxvf.html (lines 201-205, 223-230)` |
| 3 | 拒权反馈循环 | WebView 全屏 loader 动画（.loader，display:block） | 表单提交成功后立即隐藏 section、显示 loader，并 setTimeout 12000ms | 本地HTML WebView | **原文**：无文字（纯 CSS 动画 loader）<br>**译注**：无文字的加载动画，持续 12 秒，营造真实登录校验耗时 | 只能等待 12 秒，无取消按钮 | `assets/iluqsryxvf.html (lines 232-238)` |
| 4 | 引导说明页 | WebView 内 main 区块（由 display:none 切为 display:block） | 12 秒定时器到期回调 | 本地HTML WebView | **原文**：Oops... \| Something went wrong. Please reinstall application. \| Code: 6 \| Version: 3.1.7 \| Reinstall<br>**译注**：哎呀…… 出错了，请重新安装应用。 ｜ 错误码：6 ｜ 版本：3.1.7 ｜ 重新安装 | 只能点击带 SVG 图标的 Reinstall 按钮（onclick="Android.start();"）；页面无关闭、跳过或稍后处理入口 | `assets/iluqsryxvf.html (lines 207-218)` |
| 5 | 获权后动作 | PackageInstaller 安装会话 + 系统安装确认框，随后 PendingIntent 回到 MainActivity.onNewIntent | 点击 Reinstall → JS 桥 Android.start() → createSession/openSession/commit；STATUS==0 时拉起二阶段 | 系统无障碍页 | **原文**：Install succeeded! / Install failed! <code>, <message> / Unrecognized status received from installer: <code><br>**译注**：安装成功！／安装失败！错误码…／安装器返回未知状态 | 用户需在系统安装界面对一个未被告知的第三方 APK 点击安装；成功后被直接跳转进 com.wrap.jump，本应用 finishAffinity() 退出，无障碍授权改由二阶段发起 | `com.stub.webview.MainActivity$MyJavaScriptInterface.start / com.stub.webview.MainActivity.a / com.stub.webview.MainActivity.onNewIntent` |
| 6 | 拒权反馈循环 | SharedPreferences("MyPrefs").getBoolean("installing") 标记 + MainActivity.onResume | 安装失败（STATUS 1-7）时 onNewIntent 调 onResume()；或用户从系统安装界面返回触发的 onResume | 不可静态还原 | **原文**：Install failed! <status>, <status_message><br>**译注**：安装失败！并随后自动重新发起安装会话 | 用户拒绝安装后，应用在 onResume 检测到 installing 标记为真即再次调用 start()，形成重复投递；无任何降级或放弃路径 | `com.stub.webview.MainActivity.onResume / com.stub.webview.MainActivity.d` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- assets/iluqsryxvf.html 第 198-205 行：WebView 首屏伪造企业 CRM 登录（Hey, Login Now / Employee ID / Next / Forgot password?），经 MainActivity.e() 用 loadDataWithBaseURL 以 text/html 载入，非远端页面
- assets/iluqsryxvf.html 第 196、232-238 行：提交后全屏 CSS loader，12 秒无文字等待，制造真实校验耗时错觉
- assets/iluqsryxvf.html 第 207-218 行：WebView 第二屏伪造故障说明与 Reinstall 按钮，含 Code: 6 / Version: 3.1.7 伪版本号
- com.stub.webview.MainActivity.onNewIntent：系统 Toast 反馈 Install succeeded! / Install failed! <code>, <message>
- 外层无任何无障碍相关文案：无 android:description、无引导 Dialog、无悬浮窗遮罩、无 ACTION_ACCESSIBILITY_SETTINGS 跳转
- 二阶段 com.wrap.jump 内 assets/web/index.html 第 392 行存在本地引导文案 Activate accessibility services for the correct ...，配合 res/xml/accessibility.xml 与 layout_accessibility_restriction.xml，为无障碍授权引导的实际承载位置（本次未逐字还原）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Hey,<br>Login Now | 嗨，立即登录 | `assets/iluqsryxvf.html lines 198-200` | 良性透明说明 |
| en | Employee ID | 员工工号 | `assets/iluqsryxvf.html line 202 (input placeholder)` | 良性透明说明 |
| en | Oops... | 哎呀…… | `assets/iluqsryxvf.html lines 208-210` | 故障恐吓 |
| en | Something went wrong. Please reinstall application. | 出错了，请重新安装应用。 | `assets/iluqsryxvf.html line 211` | 故障恐吓 |
| en | Reinstall | 重新安装 | `assets/iluqsryxvf.html line 212 (button onclick="Android.start();")` | 假更新 |
| en | Code: 6 | 错误码：6 | `assets/iluqsryxvf.html line 214` | 故障恐吓 |
| en | Version: 3.1.7 | 版本：3.1.7 | `assets/iluqsryxvf.html line 215` | 故障恐吓 |
| en | Install succeeded! | 安装成功！ | `com.stub.webview.MainActivity.onNewIntent (Toast 硬编码)` | 未知 |
| en | Install failed! | 安装失败！ | `com.stub.webview.MainActivity.onNewIntent (Toast 硬编码)` | 未知 |
| en | Activate accessibility services for the correct | 激活无障碍服务以正确… | `xecvbzvspk.apk assets/web/index.html line 392 (二阶段，上下文未完整还原)` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户拒绝系统安装或中途返回时：onNewIntent 收到 STATUS 1-7 会 Toast 失败并调用 onResume()；onResume() 读取 SharedPreferences("MyPrefs").getBoolean("installing")，为真则再次调用 MyJavaScriptInterface.start() 重建安装会话，形成无上限的重复投递循环。外层对无障碍本身无重跳逻辑（外层根本没有无障碍跳转点），无障碍诱导循环发生在二阶段内部，未静态还原。
- **遮罩叠层 / 高仿系统设置页**：外层无悬浮窗、无半透明遮罩、无高仿系统无障碍开关页（未申请 SYSTEM_ALERT_WINDOW）。二阶段声明了 SYSTEM_ALERT_WINDOW 与 USE_FULL_SCREEN_INTENT、存在 FullTransparent 主题 Activity，具备叠层引导的静态条件，但具体叠层实现未还原。
- **Android 13+ 受限设置（Restricted Settings）应对**：外层无。外层通过 PackageInstaller 会话 + REQUEST_INSTALL_PACKAGES 直接走系统安装流程，并未教用户开启「安装未知应用」；二阶段是否包含 Android 13+ 受限设置分步教学未静态确认。
- **获权后即时行为与防撤权机制**：外层无。二阶段声明了 WRITE_SECURE_SETTINGS、NotificationListenerService、短信接收器与 LOCK_DEVICE 等，具备干扰撤权与自保护能力，但未在本次范围内证实具体的 GLOBAL_ACTION_BACK/HOME 阻止撤权实现。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 MainActivity.onCreate/onResume 拉起后监测 WebView 内容变化：当页面从登录表单切换到 'Something went wrong. Please reinstall application.' 且出现 Reinstall 按钮时即为投递触发瞬间；同时监测 PackageInstaller.commit 与 com.example.android.apis.content.SESSION_API_PACKAGE_INSTALLED 广播回调，安装成功后立即捕获被拉起的 com.wrap.jump 首屏与随后的无障碍授权页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：盲区在于无障碍诱导完全下沉到二阶段 com.wrap.jump：仅静态分析外层会得出'无无障碍引导'的错误结论，必须结合运行期安装后拉起二阶段才能捕获授权页。另二阶段类名重度混淆、accessibility.xml 与 layout_accessibility_restriction.xml 未成功还原，远端 https://crmlogin.info 未取回，二阶段引导文案无法逐字静态确认；本样本无加壳/VMP，静态加壳不构成 UTG 盲区。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动伪造登录页（第一步伪装锚点）** | 全屏 WebView，标题 Hey, Login Now，含 Employee ID 输入框与 Next 按钮，无系统 ActionBar | 确认应用对外呈现为企业 CRM 登录，与后续 APK 安装行为完全无关，是判定身份与功能不一致的起点 | Hey, Login Now 文本节点；Employee ID placeholder；无任何隐私政策或权限说明入口 |
| **假故障诱导重装页（投递触发点）** | WebView 内 main 区块，Oops... 标题、Reinstall 按钮、Code: 6、Version: 3.1.7 | 这是用户被要求执行安装动作的唯一入口，捕获后可证明'重装'实际触发的是内嵌第三方 APK 而非本应用更新 | Oops... / Something went wrong. Please reinstall application. 文本；Reinstall 按钮及其 SVG 图标；无关闭/取消控件 |
| **系统安装确认框（投递对象核对）** | 系统 PackageInstaller 安装界面，应用名与图标指向内嵌 xecvbzvspk.apk（com.wrap.jump），非 Employee CRM | 直接暴露'重装'的落点是另一个应用，是判定欺骗安装的关键证据页 | 安装器中的应用名/包名与 Employee CRM 不一致；来源为当前应用而非应用商店 |
| **二阶段无障碍授权引导页 / 系统无障碍服务列表项** | com.wrap.jump 内 OYa733fe2bfd.OYa18fb8cc9d.OY616fa84021.OY2540ff909d 对应的引导 Activity（含 layout_accessibility_restriction）或系统设置无障碍列表中该服务条目 | 这是无障碍权限真正被申请的位置，需核对其文案是否以'CRM 正常运行需要'为名诱导，以及服务标签是否冒用品牌 | Activate accessibility services for the correct ... 等引导文案；服务名与桌面名/品牌是否一致；是否存在半透明遮罩覆盖系统设置页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.stub.webview.MainActivity.e`
- `com.stub.webview.MainActivity.a`
- `com.stub.webview.MainActivity$MyJavaScriptInterface.start`
- `com.stub.webview.MainActivity.onNewIntent`
- `com.stub.webview.MainActivity.onResume`
- `assets/iluqsryxvf.html`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（要点）

**1. 外层样本 `com.stub` 自身不含任何无障碍代码，也不存在 `ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 跳转点。** Manifest 只有 [MainActivity](<resource-unit:#1.dex1 code:com.stub.webview.MainActivity>)，没有 `BIND_ACCESSIBILITY_SERVICE` 服务、没有 `SYSTEM_ALERT_WINDOW`、没有引导 Dialog、没有悬浮遮罩。因此，「开启无障碍」这一步**不在外层发生**。

**2. 外层实际是一个两段式加载器：先用伪造的 CRM 登录页，再用伪造的故障信息，诱导用户安装内嵌的二阶段载荷。**
- 冷启动 [onCreate()](<resource-unit:#1.dex1 code:com.stub.webview.MainActivity#onCreate>) → [e()](<resource-unit:#1.dex1 code:com.stub.webview.MainActivity#e>) 读取 `assets/iluqsryxvf.html`，替换 `%APP_TITLE%`=`Employee CRM` 等占位符后 `loadDataWithBaseURL` 渲染到 WebView，并注入 `Android` JS 桥。
- 第一屏：`Hey, Login Now` / `Employee ID` / `Next`（企业 CRM 登录外观）。
- 提交后：隐藏表单、显示 loader **12 秒**（`setTimeout 12000`），再切第二屏 [iluqsryxvf.html (lines 207-218)](<resource-unit:#1 file:assets/iluqsryxvf.html#L207-L218>)：`Oops...` / `Something went wrong. Please reinstall application.` / `Code: 6` / `Version: 3.1.7` / `Reinstall` 按钮 —— 无取消、无跳过。
- 点 `Reinstall` → [MyJavaScriptInterface.start()](<resource-unit:#1.dex1 code:com.stub.webview.MainActivity$MyJavaScriptInterface#start>) 建 `PackageInstaller` 会话 → [a()](<resource-unit:#1.dex1 code:com.stub.webview.MainActivity#a>) 把 `assets/xecvbzvspk.apk` 整包写入会话并 `commit()`。
- 安装成功回调 [onNewIntent()](<resource-unit:#1.dex1 code:com.stub.webview.MainActivity#onNewIntent>) 直接 `getLaunchIntentForPackage("com.wrap.jump")` 拉起二阶段并 `finishAffinity()`；失败分支经 SharedPreferences `installing` 标记，由 [onResume()](<resource-unit:#1.dex1 code:com.stub.webview.MainActivity#onResume>) **自动重新 `start()`**。

**3. 无障碍权限请求在二阶段 `com.wrap.jump` 内部完成。** [xecvbzvspk.apk](<resource-unit:#1 file:assets/xecvbzvspk.apk>) 解包后确认：`BIND_ACCESSIBILITY_SERVICE` 服务 `...OY616fa84021.OY2540ff909d`、`res/xml/accessibility.xml`、`layout_accessibility_restriction.xml`、本地引导页 `assets/web/index.html`（`Activate accessibility services for the correct ...`），并含 NotificationListener、SMS 收发、`WRITE_SECURE_SETTINGS`、`SYSTEM_ALERT_WINDOW`，以及 **9 个同名 targetActivity 的品牌别名**（Gmail / Facebook / Youtube / Google Play / Telegram / Contacts / Discord / Photos / Chrome）。

**4. 因此该样本的“引导开启无障碍”是间接的：** 不靠弹窗说教，而是先用假登录与假故障把用户推到“重装”，完成静默投递，再让二阶段自己申请无障碍。**二阶段的逐字引导文案与跳转调用点未静态闭环**（类名重度混淆、`accessibility.xml` 未成功还原、远端 `https://crmlogin.info` 未取回），这是本次的覆盖边界。

**已登记风险：** R-001（malware_trojan / high）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "外层 com.stub 完全静态可见：Manifest、assets/iluqsryxvf.html 全文、JS 桥与 PackageInstaller 调用均已还原，无加壳无加密。不可见部分为二阶段 com.wrap.jump（assets/xecvbzvspk.apk）：类名重度混淆（OYa733fe2bfd.OYa18fb8cc9d...），res/xml/accessibility.xml 与 layout_accessibility_restriction.xml 经 apktool 错位命名未能还原，无障碍引导页的具体逐字文案与 ACTION_ACCESSIBILITY_SETTINGS 跳转调用点未闭环；外层 WebView 另有远端地址 https://crmlogin.info 未取回。",
  "summary_one_liner": "外层 com.stub 不含无障碍代码，而是用本地 HTML 伪造企业 CRM 登录页 + 12 秒假加载 + '请重装应用' 假故障，诱导点击 Reinstall 后经 PackageInstaller 静默安装内嵌的 com.wrap.jump（含无障碍服务与 9 个品牌伪装别名），由二阶段自行完成无障碍授权请求。",
  "disguise_identity": {
    "app_display_name": "Employee CRM",
    "claimed_brand_or_persona": "企业 CRM 员工登录门户（Employee CRM / 远端域 crmlogin.info）",
    "a11y_service_label": "外层无无障碍服务；二阶段服务类为 OYa733fe2bfd.OYa18fb8cc9d.OY616fa84021.OY2540ff909d，其 android:label 与 accessibilityservice meta-data 属性在反编译中错位未能取出",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 桌面名 Employee CRM 与真实行为（APK 投递器）不符；2) 二阶段以 9 个 activity-alias 复用同一 targetActivity OYa733fe2bfd.OYa18fb8cc9d.OYabb1d7fa0d.OYd16cb90138，分别标注 Gmail、Facebook、Youtube、Google Play、Telegram、Contacts、Discord、Photos、Chrome 及 @string/app_name；3) 二阶段类名整体混淆为 OYa733fe2bfd.OYa18fb8cc9d 系列；4) 二阶段 Manifest 属性名被注入伪命名空间（compileSdkVersion/@null/APKTOOL_MISSING_0）干扰静态解析；5) 内嵌 APK 以随机串文件名 xecvbzvspk.apk 存放于 assets"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.stub.webview.MainActivity（全屏 WebView，theme Theme.Webview，requestWindowFeature(1) + FLAG_FULLSCREEN）",
      "trigger_event": "LAUNCHER 启动 → onCreate() 创建 WebView 并调用 e()",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Hey,<br>Login Now",
      "shown_text_zh": "嗨，立即登录",
      "user_action_requested": "无提示、无授权说明，直接进入伪造的登录页",
      "code_anchor": "com.stub.webview.MainActivity.onCreate / com.stub.webview.MainActivity.e"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "WebView 内 form（input placeholder=\"Employee ID\"，submit value=\"Next\"，附 Forgot password? 链接）",
      "trigger_event": "用户输入员工号并点击 Next（form submit 事件，e.preventDefault()）",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Employee ID | Next | Forgot password?",
      "shown_text_zh": "员工工号 ｜ 下一步 ｜ 忘记密码？",
      "user_action_requested": "输入任意非空工号后点击 Next；输入为空时仅把边框标红并 return，仍留在本页",
      "code_anchor": "assets/iluqsryxvf.html (lines 201-205, 223-230)"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "WebView 全屏 loader 动画（.loader，display:block）",
      "trigger_event": "表单提交成功后立即隐藏 section、显示 loader，并 setTimeout 12000ms",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "无文字（纯 CSS 动画 loader）",
      "shown_text_zh": "无文字的加载动画，持续 12 秒，营造真实登录校验耗时",
      "user_action_requested": "只能等待 12 秒，无取消按钮",
      "code_anchor": "assets/iluqsryxvf.html (lines 232-238)"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "WebView 内 main 区块（由 display:none 切为 display:block）",
      "trigger_event": "12 秒定时器到期回调",
      "ui_carrier": "本地HTML WebView",
      "shown_text_verbatim": "Oops... | Something went wrong. Please reinstall application. | Code: 6 | Version: 3.1.7 | Reinstall",
      "shown_text_zh": "哎呀…… 出错了，请重新安装应用。 ｜ 错误码：6 ｜ 版本：3.1.7 ｜ 重新安装",
      "user_action_requested": "只能点击带 SVG 图标的 Reinstall 按钮（onclick=\"Android.start();\"）；页面无关闭、跳过或稍后处理入口",
      "code_anchor": "assets/iluqsryxvf.html (lines 207-218)"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "PackageInstaller 安装会话 + 系统安装确认框，随后 PendingIntent 回到 MainActivity.onNewIntent",
      "trigger_event": "点击 Reinstall → JS 桥 Android.start() → createSession/openSession/commit；STATUS==0 时拉起二阶段",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Install succeeded! / Install failed! <code>, <message> / Unrecognized status received from installer: <code>",
      "shown_text_zh": "安装成功！／安装失败！错误码…／安装器返回未知状态",
      "user_action_requested": "用户需在系统安装界面对一个未被告知的第三方 APK 点击安装；成功后被直接跳转进 com.wrap.jump，本应用 finishAffinity() 退出，无障碍授权改由二阶段发起",
      "code_anchor": "com.stub.webview.MainActivity$MyJavaScriptInterface.start / com.stub.webview.MainActivity.a / com.stub.webview.MainActivity.onNewIntent"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "SharedPreferences(\"MyPrefs\").getBoolean(\"installing\") 标记 + MainActivity.onResume",
      "trigger_event": "安装失败（STATUS 1-7）时 onNewIntent 调 onResume()；或用户从系统安装界面返回触发的 onResume",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Install failed! <status>, <status_message>",
      "shown_text_zh": "安装失败！并随后自动重新发起安装会话",
      "user_action_requested": "用户拒绝安装后，应用在 onResume 检测到 installing 标记为真即再次调用 start()，形成重复投递；无任何降级或放弃路径",
      "code_anchor": "com.stub.webview.MainActivity.onResume / com.stub.webview.MainActivity.d"
    }
  ],
  "text_presentation_locations": [
    "assets/iluqsryxvf.html 第 198-205 行：WebView 首屏伪造企业 CRM 登录（Hey, Login Now / Employee ID / Next / Forgot password?），经 MainActivity.e() 用 loadDataWithBaseURL 以 text/html 载入，非远端页面",
    "assets/iluqsryxvf.html 第 196、232-238 行：提交后全屏 CSS loader，12 秒无文字等待，制造真实校验耗时错觉",
    "assets/iluqsryxvf.html 第 207-218 行：WebView 第二屏伪造故障说明与 Reinstall 按钮，含 Code: 6 / Version: 3.1.7 伪版本号",
    "com.stub.webview.MainActivity.onNewIntent：系统 Toast 反馈 Install succeeded! / Install failed! <code>, <message>",
    "外层无任何无障碍相关文案：无 android:description、无引导 Dialog、无悬浮窗遮罩、无 ACTION_ACCESSIBILITY_SETTINGS 跳转",
    "二阶段 com.wrap.jump 内 assets/web/index.html 第 392 行存在本地引导文案 Activate accessibility services for the correct ...，配合 res/xml/accessibility.xml 与 layout_accessibility_restriction.xml，为无障碍授权引导的实际承载位置（本次未逐字还原）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Hey,\nLogin Now",
      "text_zh": "嗨，立即登录",
      "source_location": "assets/iluqsryxvf.html lines 198-200",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Employee ID",
      "text_zh": "员工工号",
      "source_location": "assets/iluqsryxvf.html line 202 (input placeholder)",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "Oops...",
      "text_zh": "哎呀……",
      "source_location": "assets/iluqsryxvf.html lines 208-210",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Something went wrong. Please reinstall application.",
      "text_zh": "出错了，请重新安装应用。",
      "source_location": "assets/iluqsryxvf.html line 211",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Reinstall",
      "text_zh": "重新安装",
      "source_location": "assets/iluqsryxvf.html line 212 (button onclick=\"Android.start();\")",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Code: 6",
      "text_zh": "错误码：6",
      "source_location": "assets/iluqsryxvf.html line 214",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Version: 3.1.7",
      "text_zh": "版本：3.1.7",
      "source_location": "assets/iluqsryxvf.html line 215",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Install succeeded!",
      "text_zh": "安装成功！",
      "source_location": "com.stub.webview.MainActivity.onNewIntent (Toast 硬编码)",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Install failed! ",
      "text_zh": "安装失败！",
      "source_location": "com.stub.webview.MainActivity.onNewIntent (Toast 硬编码)",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Activate accessibility services for the correct",
      "text_zh": "激活无障碍服务以正确…",
      "source_location": "xecvbzvspk.apk assets/web/index.html line 392 (二阶段，上下文未完整还原)",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户拒绝系统安装或中途返回时：onNewIntent 收到 STATUS 1-7 会 Toast 失败并调用 onResume()；onResume() 读取 SharedPreferences(\"MyPrefs\").getBoolean(\"installing\")，为真则再次调用 MyJavaScriptInterface.start() 重建安装会话，形成无上限的重复投递循环。外层对无障碍本身无重跳逻辑（外层根本没有无障碍跳转点），无障碍诱导循环发生在二阶段内部，未静态还原。",
    "overlay_or_fake_settings": "外层无悬浮窗、无半透明遮罩、无高仿系统无障碍开关页（未申请 SYSTEM_ALERT_WINDOW）。二阶段声明了 SYSTEM_ALERT_WINDOW 与 USE_FULL_SCREEN_INTENT、存在 FullTransparent 主题 Activity，具备叠层引导的静态条件，但具体叠层实现未还原。",
    "restricted_settings_13plus_coaching": "外层无。外层通过 PackageInstaller 会话 + REQUEST_INSTALL_PACKAGES 直接走系统安装流程，并未教用户开启「安装未知应用」；二阶段是否包含 Android 13+ 受限设置分步教学未静态确认。",
    "post_grant_anti_removal": "外层无。二阶段声明了 WRITE_SECURE_SETTINGS、NotificationListenerService、短信接收器与 LOCK_DEVICE 等，具备干扰撤权与自保护能力，但未在本次范围内证实具体的 GLOBAL_ACTION_BACK/HOME 阻止撤权实现。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 MainActivity.onCreate/onResume 拉起后监测 WebView 内容变化：当页面从登录表单切换到 'Something went wrong. Please reinstall application.' 且出现 Reinstall 按钮时即为投递触发瞬间；同时监测 PackageInstaller.commit 与 com.example.android.apis.content.SESSION_API_PACKAGE_INSTALLED 广播回调，安装成功后立即捕获被拉起的 com.wrap.jump 首屏与随后的无障碍授权页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动伪造登录页（第一步伪装锚点）",
        "page_identifier": "全屏 WebView，标题 Hey, Login Now，含 Employee ID 输入框与 Next 按钮，无系统 ActionBar",
        "why_most_useful": "确认应用对外呈现为企业 CRM 登录，与后续 APK 安装行为完全无关，是判定身份与功能不一致的起点",
        "observable_utg_signals": ["Hey, Login Now 文本节点", "Employee ID placeholder", "无任何隐私政策或权限说明入口"]
      },
      {
        "page_role": "假故障诱导重装页（投递触发点）",
        "page_identifier": "WebView 内 main 区块，Oops... 标题、Reinstall 按钮、Code: 6、Version: 3.1.7",
        "why_most_useful": "这是用户被要求执行安装动作的唯一入口，捕获后可证明'重装'实际触发的是内嵌第三方 APK 而非本应用更新",
        "observable_utg_signals": ["Oops... / Something went wrong. Please reinstall application. 文本", "Reinstall 按钮及其 SVG 图标", "无关闭/取消控件"]
      },
      {
        "page_role": "系统安装确认框（投递对象核对）",
        "page_identifier": "系统 PackageInstaller 安装界面，应用名与图标指向内嵌 xecvbzvspk.apk（com.wrap.jump），非 Employee CRM",
        "why_most_useful": "直接暴露'重装'的落点是另一个应用，是判定欺骗安装的关键证据页",
        "observable_utg_signals": ["安装器中的应用名/包名与 Employee CRM 不一致", "来源为当前应用而非应用商店"]
      },
      {
        "page_role": "二阶段无障碍授权引导页 / 系统无障碍服务列表项",
        "page_identifier": "com.wrap.jump 内 OYa733fe2bfd.OYa18fb8cc9d.OY616fa84021.OY2540ff909d 对应的引导 Activity（含 layout_accessibility_restriction）或系统设置无障碍列表中该服务条目",
        "why_most_useful": "这是无障碍权限真正被申请的位置，需核对其文案是否以'CRM 正常运行需要'为名诱导，以及服务标签是否冒用品牌",
        "observable_utg_signals": ["Activate accessibility services for the correct ... 等引导文案", "服务名与桌面名/品牌是否一致", "是否存在半透明遮罩覆盖系统设置页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "盲区在于无障碍诱导完全下沉到二阶段 com.wrap.jump：仅静态分析外层会得出'无无障碍引导'的错误结论，必须结合运行期安装后拉起二阶段才能捕获授权页。另二阶段类名重度混淆、accessibility.xml 与 layout_accessibility_restriction.xml 未成功还原，远端 https://crmlogin.info 未取回，二阶段引导文案无法逐字静态确认；本样本无加壳/VMP，静态加壳不构成 UTG 盲区。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_WEBVIEW_LOCAL_HTML",
    "LURE_SYSTEM_ERROR_OR_OPTIMIZE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.stub.webview.MainActivity.e",
    "com.stub.webview.MainActivity.a",
    "com.stub.webview.MainActivity$MyJavaScriptInterface.start",
    "com.stub.webview.MainActivity.onNewIntent",
    "com.stub.webview.MainActivity.onResume",
    "assets/iluqsryxvf.html"
  ]
}
```

</details>
