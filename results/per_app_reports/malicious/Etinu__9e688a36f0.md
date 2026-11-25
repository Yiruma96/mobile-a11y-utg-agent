# MR_029__9e688a36f0｜Etinu — Picture Editor

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：156.1s

## 1. 一句话核心结论

- **核心申请方式**：以 AES 加密的 assets/settings.bin 作为二阶段 DEX 运行期解密加载，无障碍引导（含屏蔽返回键的透明 Activity 与通知监听回传）全部由远端 CloudFront 可更新的隐藏载荷驱动，静态层不暴露任何无障碍服务或设置页跳转点。
- **静态可见性说明**：Manifest、入口 Activity、通知监听服务、透明引导 Activity 与加载骨架完全静态可见；但无障碍引导的实际判定、页面流转、文案与跳转 Intent 全部位于 assets/settings.bin（539248 字节加密载荷，密钥绑定包名 h.W0），运行期解密落盘为 loader.dex 后经反射 DexClassLoader 加载；且全包字符串用 AES/CBC/PKCS5 硬编码密钥 QjwTgBdrbrWTELsO 加密，真实类名/URL/方法名均为密文，故引导流程本体不可静态还原。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `9e688a36f02dd1b1a9ae4a5c94c1335b14d1b0b1c8901ec8c986b4390e95e760` |
| 包名 / 年份 | `com.ce1ab3.app.photo.editor` / 2021 |
| 家族 / 品类 | **Etinu**（同池样本数：4） |
| 原始来源标识 | https://www.mcafee.com/blogs/other-blogs/mcafee-labs/clever-billing-fraud-applications-on-google-play-etinu/ |
| 桌面显示名 | Picture Editor |
| 引导页宣称品牌/身份 | Picture Editor（图片编辑器，包名 com.ce1ab3.app.photo.editor） |
| 系统无障碍列表服务名 | 无（Manifest 未声明任何 BIND_ACCESSIBILITY_SERVICE 服务；若二阶段动态注册则名称不可静态确定） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：①全部业务类名混淆为 p0a1f9a79.pb05c7c01.p1e8c0249.pXXXXXXX 形式；②敏感字符串与类名用 AES/CBC/PKCS5Padding + 硬编码密钥 QjwTgBdrbrWTELsO 加密后 Base64 存放，仅运行期 pc6b2688e.m250ed32b 解密；③服务/Activity 塞入大量随机名 meta-data（如 NYsFYKBdcWGocGRX=zyKtIQbCDtDufXZP）作干扰；④引导 Activity pffdfd40f 使用 Translucent.NoTitleBar + singleInstance + excludeFromRecents 隐藏窗口外观与最近任务记录，并重写 onBackPressed 为空实现屏蔽返回键；⑤真实逻辑藏于 assets/settings.bin 加密载荷，规避 Manifest/静态扫描；⑥反分析：检测 goldfish/vbox、ranchu/generic/vbox、Genymotion、Android SDK built for x86 等模拟器特征并读取 enabled_accessibility_services / accessibility_enabled 状态。 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.ce1ab3.app.editor.photo.android.activities.SplashActivity（MAIN/LAUNCHER，portrait） | onCreate（用户点击图标冷启动） | 原生Activity | **原文**：无（SplashActivity 仅作启动壳，未含引导文案）<br>**译注**：启动闪屏，无可见引导内容 | 无 | `com.ce1ab3.app.editor.photo.android.activities.SplashActivity#onCreate` |
| 2 | 获权后动作 | p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a（静态单例，字段 d） | pffdfd40f.onCreate / pb01661d3.onNotificationPosted 调用 p718dd98a.mf638b3b7(Object[]) | 不可静态还原 | 无 | 无（后台静默执行） | `p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#m63cbeb3a / #mf638b3b7` |
| 3 | 获权后动作 | assets/settings.bin → 私有目录 loader.dex → dalvik.system.DexClassLoader | m63cbeb3a 读取 context.getAssets().open(解密出的 "settings.bin")，经 h.W0(byteArray, packageName.getBytes()) 解密后 c.a(File, InputStream, false, null) 写盘，反射 new DexClassLoader(strR, filesDir, null, classLoader) | 不可静态还原 | **原文**：无（二阶段 DEX 内部逻辑加密，不可静态读取）<br>**译注**：解密释放 539KB 二阶段 DEX 并动态加载，其后行为不可静态还原 | 无 | `p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#m63cbeb3a；assets/settings.bin` |
| 4 | 引导说明页 | p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f（Activity，theme=Theme.AppCompat.Translucent.NoTitleBar，singleInstance，excludeFromRecents，finishOnTaskLaunch=false） | 二阶段载荷经反射按 pffdfd40f.class.getName() 拉起；onCreate 转发给 p718dd98a.mf638b3b7 并由二阶段填充界面；onBackPressed 为空实现 | 原生Activity | **原文**：不可静态获取（文案在 settings.bin 内，运行期注入）<br>**译注**：透明/半透明原生页面，文案由加密二阶段载荷运行期渲染，静态不可见 | 不可静态确定；已确认返回键被屏蔽（onBackPressed 空实现），无法通过返回键取消 | `p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f#onCreate / #onBackPressed` |
| 5 | 跳无障碍设置 | 预期为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 系统页（静态全包搜索无该字符串，判定由二阶段载荷运行期拼接/解密生成） | 不可静态确定（由 settings.bin 解密后的类执行 startActivity） | 系统无障碍页 | **原文**：无（包内 dex1 中不存在 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 字面量）<br>**译注**：跳转动作本身不可静态确认，仅有承载骨架可证 | 不可静态确定 | `p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#mf638b3b7（反射 Method.invoke，目标类名密文）` |
| 6 | 获权后动作 | p0a1f9a79.pb05c7c01.p1e8c0249.pb01661d3（NotificationListenerService） | onNotificationPosted(StatusBarNotification) 每条通知到达即触发 | 通知栏 | **原文**：无（服务不产生界面）<br>**译注**：静默读取全部通知（含验证码/推送）并反射回传二阶段 | 无（无需用户操作，常驻窃取） | `p0a1f9a79.pb05c7c01.p1e8c0249.pb01661d3#onNotificationPosted` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f：Translucent.NoTitleBar 原生透明 Activity，作为运行期引导/弹窗容器（文案由 settings.bin 解密载荷注入，静态不可读）
- assets/settings.bin（539248 字节加密二阶段载荷）：承载全部引导文案与页面逻辑，运行期解密为 loader.dex 后由 DexClassLoader 加载
- p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#m63cbeb3a：以 AES 硬编码密钥 QjwTgBdrbrWTELsO 解密的类名/方法名/URL 密文，运行期才还原为字符串（如 http://d3481mqckui2d7.cloudfront.net）
- 系统无障碍列表 android:description：不存在（Manifest 未声明任何 AccessibilityService）
- 本地 HTML / assets WebView 教学页：未发现（assets 下仅 audience_network.dex、cache.bin、cid、filters/、fonts/、settings.bin、tt_mime_type.pro）
- 通知栏：pb01661d3 仅作为读取方，不主动展示引导通知

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | http://d3481mqckui2d7.cloudfront.net | http://d3481mqckui2d7.cloudfront.net（远端控制/载荷更新地址） | `classes.dex 密文经 pc6b2688e.m250ed32b 解密（AES key=QjwTgBdrbrWTELsO）` | 未知 |
| en | context.assets.open("settings.bin") | 从应用 assets 打开 settings.bin（加密二阶段载荷） | `classes.dex 解密字符串` | 未知 |
| en | com.unite.loader.utils.LoaderExternalClass | 二阶段载荷加载入口类 com.unite.loader.utils.LoaderExternalClass | `classes.dex 解密字符串（p718dd98a#mf638b3b7 反射 getMethod("init", String.class) 后 invoke）` | 未知 |
| en | dalvik.system.DexClassLoader | Dalvik 动态类加载器（用于加载释放后的 loader.dex） | `classes.dex 解密字符串（p718dd98a#m63cbeb3a 反射 getConstructor）` | 未知 |
| en | goldfish,vbox / ranchu,generic,vbox / Genymotion / Android SDK built for x86 | 模拟器特征串：goldfish、vbox、ranchu、generic、Genymotion、Android SDK built for x86 | `d.c.a.e.b0#<init>（运行环境探测，供二阶段判定是否规避分析环境）` | 未知 |
| en | enabled_accessibility_services / accessibility_enabled / touch_exploration_enabled | 已启用的无障碍服务列表 / 无障碍总开关 / 触摸探索开关（Settings.Secure 读取） | `d.c.a.e.b0#<init>（判定无障碍授权状态的代码路径）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态确定。已确证的前置条件：承载引导的 pffdfd40f 为 singleInstance + finishOnTaskLaunch=false + excludeFromRecents，且 onBackPressed() 方法体为空（返回键无效），用户无法以返回键退出该引导页；是否在 onResume 检测未授权后重跳 ACCESSIBILITY_SETTINGS 由 settings.bin 内二阶段代码决定，静态不可见。
- **遮罩叠层 / 高仿系统设置页**：未确证。已确证 pffdfd40f 采用 Theme.AppCompat.Translucent.NoTitleBar 的半透明窗口载体，具备叠放遮罩/引导页能力；但未见高仿系统无障碍开关页的布局或文案资源（引导文案全部在加密载荷内）。
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（全包 dex1 中不存在 restricted_settings、install_packages、ACTION_APPLICATION_DETAILS_SETTINGS 字面量；预筛 SESSION_INSTALLER 命中属载荷加密层，无法静态核实具体教学步骤）。
- **获权后即时行为与防撤权机制**：不可静态确定。pb01661d3 可读取全部通知，pffdfd40f 屏蔽返回键，但未见 GLOBAL_ACTION_BACK/HOME 或无障碍事件拦截的静态实现；anti_removal 预筛为空。
- **良性降级 / 替代方案**：无。应用为图片编辑器外壳，但无任何“仅编辑模式/手动替代路径”的降级代码证据，真实功能由加密载荷运行期决定。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在 SplashActivity 冷启动后立即挂 UTG，重点监听两类瞬间：①p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f 透明 Activity 首次出现在顶层（这是二阶段载荷已解密加载并开始引导的信号）；②任何向 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的 startActivity。另可同步监测通知栏，因 pb01661d3 会转发通知，可能触发二次引导。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：①引导文案与页面流转 100% 位于 assets/settings.bin 加密载荷内，静态完全不可见；②敏感字符串 AES 加密，静态字符串检索会漏检 ACTION_ACCESSIBILITY_SETTINGS 等关键字；③二阶段可经 http://d3481mqckui2d7.cloudfront.net 远端更新，同一包体在不同时间/地域可能呈现不同话术；④存在模拟器与无障碍授权状态探测，UTG 采集若在模拟器上进行可能被判定环境而根本不展示引导；⑤Manifest 无任何无障碍服务声明，若二阶段未动态注册，则无障碍页捕获可能为空——此时应转向通知监听（pb01661d3）与透明 Activity 的证据链。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **二阶段载荷首启引导页（屏蔽返回键的透明原生页）** | 顶层 Activity 为 p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f，Theme.AppCompat.Translucent.NoTitleBar，singleInstance，不在最近任务中出现 | 这是整个无障碍引导链唯一静态可定位的 UI 承载点，捕获其 UTG 树即可获得加密载荷运行期渲染的全部原文，是突破静态不可见的唯一途径 | pffdfd40f 的节点文本/按钮文案（二阶段运行期注入，静态无）；是否存在取消/跳过按钮及其 clickable 属性；点击返回键后页面是否消失（验证 onBackPressed 空实现的实际效果）；窗口是否半透明叠压在下层应用/设置页之上 |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中的服务条目，label 由二阶段动态注册决定 | 确认恶意服务是否以动态方式出现、其展示名是否伪装成系统/品牌组件，以及用户被要求开启的到底是哪一个开关 | 服务条目的显示名（是否伪装系统/品牌）；android:description 说明文案；开关初始状态与是否被自动勾选；跳转发生时是否同时存在 pffdfd40f 遮罩 |
| **跳转前说明/授权理由页** | pffdfd40f 或其内部 Fragment/Dialog，含引导文案与“去开启”按钮 | 区分该应用采用哪种话术框架（假更新/故障恐吓/清理伪装/隐私承诺），这是判定恶意广告之外是否构成变脸与诱骗的核心证据 | 话术关键词原文（update/error/clean/protect/allow）；按钮是否唯一且不可取消；是否有倒计时或反复弹出 |
| **远端 WebView 教学页（若存在）** | 由 http://d3481mqckui2d7.cloudfront.net 下发，可能以 WebViewActivity 形式出现 | 若引导文案改为远端 HTML 下发，静态与本地资源均无法捕获，只能运行期抓取，可直接证明云控可切换话术 | WebView 加载 URL 与页面文本；页面内是否含分步截图/教唆忽略系统警告的文案；与 cloudfront 域名的网络请求时序 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#m63cbeb3a`
- `p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#mf638b3b7`
- `p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f#onCreate`
- `p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f#onBackPressed`
- `p0a1f9a79.pb05c7c01.p1e8c0249.pb01661d3#onNotificationPosted`
- `pc6b2688e#m250ed32b`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点

**核心判断：无障碍引导流程无法通过静态分析还原，被藏进加密二阶段载荷；但引导流程的“投递骨架”完整可见。**

1. **Manifest 里没有任何无障碍服务声明**：全包无 `BIND_ACCESSIBILITY_SERVICE`、无 `android.accessibilityservice.AccessibilityService` 子类，与预筛 `无障碍服务类=[]` 一致。所以 UTG 视角下，此包**当前阶段**不会在系统无障碍列表中产生条目。
2. **真实的恶意逻辑位于 `assets/settings.bin`（539,248 字节，无标准文件头）**。`p718dd98a.m63cbeb3a()` 把它解密（`h.W0(byteArray, packageName.getBytes())`，密钥绑定包名）后写入应用私有目录的 `loader.dex`，再用反射构造 `dalvik.system.DexClassLoader` 加载，反射调用 `init(...)`，参数含 `pffdfd40f.class.getName()` 等。**无障碍引导、受限设置教学、页面流转文案全部在这层之内。**
3. **字符串使用 AES/CBC/PKCS5 + 硬编码密钥 `QjwTgBdrbrWTELsO`（IV 同密钥）加密**（`pc6b2688e.m250ed32b`），全包真实 URL、类名、方法名均为密文。解密后得到远端控制地址 `http://d3481mqckui2d7.cloudfront.net`、`com.unite.loader.utils.LoaderExternalClass`、`loader.dex`、`settings.bin`、`onNotificationPosted`、`onCreate`、`dalvik.system.DexClassLoader` 等——**二阶段载荷完全由 CloudFront 远端可更新**。
4. **可见的诱导弹窗承载组件**：[pffdfd40f](<resource-unit:#1.dex1 code:p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f>) 是 `singleInstance` + `Translucent.NoTitleBar` + `excludeFromRecents` + `finishOnTaskLaunch=false` 的透明 Activity，`onBackPressed()` **方法体为空**（屏蔽返回键，无法取消）；它由二阶段载荷通过反射按类名启动，参数含 `Boolean.FALSE, Boolean.FALSE, 0`。
5. **通知监听是第二条常驻通道**：[pb01661d3](<resource-unit:#1.dex1 code:p0a1f9a79.pb05c7c01.p1e8c0249.pb01661d3>) 继承 `NotificationListenerService`，`onNotificationPosted` 把整条 `StatusBarNotification` 反射转发进二阶段（`mf638b3b7`）。这是 Etinu 家族典型的“读通知取验证码/劫持”入口，也可作为引导触发源。
6. **反分析特征**：`d.c.a.e.b0`（AppsFlyer SDK，非恶意）采集 `enabled_accessibility_services`、`accessibility_enabled`、`touch_exploration_enabled` 及模拟器特征（`goldfish,vbox` / `ranchu,generic,vbox` / `Genymotion` / `Android SDK built for x86`）——二阶段可据此判断“无障碍是否已开启”以及“是否为分析环境”，这是云控/环境开关的典型前置。
7. **工具预算边界**：受 8–14 次调用硬约束，本轮的结论已收敛，因此**未向项目风险清单写入记录**（写入需要额外的证据图注册调用）；如需登记“加密二阶段载荷 + 隐藏投递”风险，请在下一轮指示。

**UTG 采集建议**：不要等冷启动——应在 `SplashActivity` 之后立刻挂 UTG 监测，捕获 **`pffdfd40f` 透明 Activity 出现**、以及任何向 `android.settings.ACCESSIBILITY_SETTINGS` / `APPLICATION_DETAILS_SETTINGS` 的跳转；这两个信号只会在 `settings.bin` 解密并加载 `loader.dex` 之后出现，静态无法预判其文案。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、入口 Activity、通知监听服务、透明引导 Activity 与加载骨架完全静态可见；但无障碍引导的实际判定、页面流转、文案与跳转 Intent 全部位于 assets/settings.bin（539248 字节加密载荷，密钥绑定包名 h.W0），运行期解密落盘为 loader.dex 后经反射 DexClassLoader 加载；且全包字符串用 AES/CBC/PKCS5 硬编码密钥 QjwTgBdrbrWTELsO 加密，真实类名/URL/方法名均为密文，故引导流程本体不可静态还原。",
  "summary_one_liner": "以 AES 加密的 assets/settings.bin 作为二阶段 DEX 运行期解密加载，无障碍引导（含屏蔽返回键的透明 Activity 与通知监听回传）全部由远端 CloudFront 可更新的隐藏载荷驱动，静态层不暴露任何无障碍服务或设置页跳转点。",
  "disguise_identity": {
    "app_display_name": "Picture Editor",
    "claimed_brand_or_persona": "Picture Editor（图片编辑器，包名 com.ce1ab3.app.photo.editor）",
    "a11y_service_label": "无（Manifest 未声明任何 BIND_ACCESSIBILITY_SERVICE 服务；若二阶段动态注册则名称不可静态确定）",
    "identity_mismatch": true,
    "obfuscation_tricks": "①全部业务类名混淆为 p0a1f9a79.pb05c7c01.p1e8c0249.pXXXXXXX 形式；②敏感字符串与类名用 AES/CBC/PKCS5Padding + 硬编码密钥 QjwTgBdrbrWTELsO 加密后 Base64 存放，仅运行期 pc6b2688e.m250ed32b 解密；③服务/Activity 塞入大量随机名 meta-data（如 NYsFYKBdcWGocGRX=zyKtIQbCDtDufXZP）作干扰；④引导 Activity pffdfd40f 使用 Translucent.NoTitleBar + singleInstance + excludeFromRecents 隐藏窗口外观与最近任务记录，并重写 onBackPressed 为空实现屏蔽返回键；⑤真实逻辑藏于 assets/settings.bin 加密载荷，规避 Manifest/静态扫描；⑥反分析：检测 goldfish/vbox、ranchu/generic/vbox、Genymotion、Android SDK built for x86 等模拟器特征并读取 enabled_accessibility_services / accessibility_enabled 状态。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.ce1ab3.app.editor.photo.android.activities.SplashActivity（MAIN/LAUNCHER，portrait）",
      "trigger_event": "onCreate（用户点击图标冷启动）",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（SplashActivity 仅作启动壳，未含引导文案）",
      "shown_text_zh": "启动闪屏，无可见引导内容",
      "user_action_requested": "无",
      "code_anchor": "com.ce1ab3.app.editor.photo.android.activities.SplashActivity#onCreate"
    },
    {
      "step": 2,
      "stage": "获权后动作",
      "screen_or_component": "p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a（静态单例，字段 d）",
      "trigger_event": "pffdfd40f.onCreate / pb01661d3.onNotificationPosted 调用 p718dd98a.mf638b3b7(Object[])",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "解密并释放二阶段载荷，无界面",
      "user_action_requested": "无（后台静默执行）",
      "code_anchor": "p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#m63cbeb3a / #mf638b3b7"
    },
    {
      "step": 3,
      "stage": "获权后动作",
      "screen_or_component": "assets/settings.bin → 私有目录 loader.dex → dalvik.system.DexClassLoader",
      "trigger_event": "m63cbeb3a 读取 context.getAssets().open(解密出的 \"settings.bin\")，经 h.W0(byteArray, packageName.getBytes()) 解密后 c.a(File, InputStream, false, null) 写盘，反射 new DexClassLoader(strR, filesDir, null, classLoader)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（二阶段 DEX 内部逻辑加密，不可静态读取）",
      "shown_text_zh": "解密释放 539KB 二阶段 DEX 并动态加载，其后行为不可静态还原",
      "user_action_requested": "无",
      "code_anchor": "p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#m63cbeb3a；assets/settings.bin"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f（Activity，theme=Theme.AppCompat.Translucent.NoTitleBar，singleInstance，excludeFromRecents，finishOnTaskLaunch=false）",
      "trigger_event": "二阶段载荷经反射按 pffdfd40f.class.getName() 拉起；onCreate 转发给 p718dd98a.mf638b3b7 并由二阶段填充界面；onBackPressed 为空实现",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "不可静态获取（文案在 settings.bin 内，运行期注入）",
      "shown_text_zh": "透明/半透明原生页面，文案由加密二阶段载荷运行期渲染，静态不可见",
      "user_action_requested": "不可静态确定；已确认返回键被屏蔽（onBackPressed 空实现），无法通过返回键取消",
      "code_anchor": "p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f#onCreate / #onBackPressed"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "预期为 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 系统页（静态全包搜索无该字符串，判定由二阶段载荷运行期拼接/解密生成）",
      "trigger_event": "不可静态确定（由 settings.bin 解密后的类执行 startActivity）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（包内 dex1 中不存在 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 字面量）",
      "shown_text_zh": "跳转动作本身不可静态确认，仅有承载骨架可证",
      "user_action_requested": "不可静态确定",
      "code_anchor": "p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#mf638b3b7（反射 Method.invoke，目标类名密文）"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "p0a1f9a79.pb05c7c01.p1e8c0249.pb01661d3（NotificationListenerService）",
      "trigger_event": "onNotificationPosted(StatusBarNotification) 每条通知到达即触发",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "无（服务不产生界面）",
      "shown_text_zh": "静默读取全部通知（含验证码/推送）并反射回传二阶段",
      "user_action_requested": "无（无需用户操作，常驻窃取）",
      "code_anchor": "p0a1f9a79.pb05c7c01.p1e8c0249.pb01661d3#onNotificationPosted"
    }
  ],
  "text_presentation_locations": [
    "p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f：Translucent.NoTitleBar 原生透明 Activity，作为运行期引导/弹窗容器（文案由 settings.bin 解密载荷注入，静态不可读）",
    "assets/settings.bin（539248 字节加密二阶段载荷）：承载全部引导文案与页面逻辑，运行期解密为 loader.dex 后由 DexClassLoader 加载",
    "p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#m63cbeb3a：以 AES 硬编码密钥 QjwTgBdrbrWTELsO 解密的类名/方法名/URL 密文，运行期才还原为字符串（如 http://d3481mqckui2d7.cloudfront.net）",
    "系统无障碍列表 android:description：不存在（Manifest 未声明任何 AccessibilityService）",
    "本地 HTML / assets WebView 教学页：未发现（assets 下仅 audience_network.dex、cache.bin、cid、filters/、fonts/、settings.bin、tt_mime_type.pro）",
    "通知栏：pb01661d3 仅作为读取方，不主动展示引导通知"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "http://d3481mqckui2d7.cloudfront.net",
      "text_zh": "http://d3481mqckui2d7.cloudfront.net（远端控制/载荷更新地址）",
      "source_location": "classes.dex 密文经 pc6b2688e.m250ed32b 解密（AES key=QjwTgBdrbrWTELsO）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "context.assets.open(\"settings.bin\")",
      "text_zh": "从应用 assets 打开 settings.bin（加密二阶段载荷）",
      "source_location": "classes.dex 解密字符串",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "com.unite.loader.utils.LoaderExternalClass",
      "text_zh": "二阶段载荷加载入口类 com.unite.loader.utils.LoaderExternalClass",
      "source_location": "classes.dex 解密字符串（p718dd98a#mf638b3b7 反射 getMethod(\"init\", String.class) 后 invoke）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "dalvik.system.DexClassLoader",
      "text_zh": "Dalvik 动态类加载器（用于加载释放后的 loader.dex）",
      "source_location": "classes.dex 解密字符串（p718dd98a#m63cbeb3a 反射 getConstructor）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "goldfish,vbox / ranchu,generic,vbox / Genymotion / Android SDK built for x86",
      "text_zh": "模拟器特征串：goldfish、vbox、ranchu、generic、Genymotion、Android SDK built for x86",
      "source_location": "d.c.a.e.b0#<init>（运行环境探测，供二阶段判定是否规避分析环境）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "enabled_accessibility_services / accessibility_enabled / touch_exploration_enabled",
      "text_zh": "已启用的无障碍服务列表 / 无障碍总开关 / 触摸探索开关（Settings.Secure 读取）",
      "source_location": "d.c.a.e.b0#<init>（判定无障碍授权状态的代码路径）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态确定。已确证的前置条件：承载引导的 pffdfd40f 为 singleInstance + finishOnTaskLaunch=false + excludeFromRecents，且 onBackPressed() 方法体为空（返回键无效），用户无法以返回键退出该引导页；是否在 onResume 检测未授权后重跳 ACCESSIBILITY_SETTINGS 由 settings.bin 内二阶段代码决定，静态不可见。",
    "overlay_or_fake_settings": "未确证。已确证 pffdfd40f 采用 Theme.AppCompat.Translucent.NoTitleBar 的半透明窗口载体，具备叠放遮罩/引导页能力；但未见高仿系统无障碍开关页的布局或文案资源（引导文案全部在加密载荷内）。",
    "restricted_settings_13plus_coaching": "无静态证据（全包 dex1 中不存在 restricted_settings、install_packages、ACTION_APPLICATION_DETAILS_SETTINGS 字面量；预筛 SESSION_INSTALLER 命中属载荷加密层，无法静态核实具体教学步骤）。",
    "post_grant_anti_removal": "不可静态确定。pb01661d3 可读取全部通知，pffdfd40f 屏蔽返回键，但未见 GLOBAL_ACTION_BACK/HOME 或无障碍事件拦截的静态实现；anti_removal 预筛为空。",
    "benign_graceful_degradation": "无。应用为图片编辑器外壳，但无任何“仅编辑模式/手动替代路径”的降级代码证据，真实功能由加密载荷运行期决定。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在 SplashActivity 冷启动后立即挂 UTG，重点监听两类瞬间：①p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f 透明 Activity 首次出现在顶层（这是二阶段载荷已解密加载并开始引导的信号）；②任何向 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的 startActivity。另可同步监测通知栏，因 pb01661d3 会转发通知，可能触发二次引导。",
    "key_pages_to_capture": [
      {
        "page_role": "二阶段载荷首启引导页（屏蔽返回键的透明原生页）",
        "page_identifier": "顶层 Activity 为 p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f，Theme.AppCompat.Translucent.NoTitleBar，singleInstance，不在最近任务中出现",
        "why_most_useful": "这是整个无障碍引导链唯一静态可定位的 UI 承载点，捕获其 UTG 树即可获得加密载荷运行期渲染的全部原文，是突破静态不可见的唯一途径",
        "observable_utg_signals": ["pffdfd40f 的节点文本/按钮文案（二阶段运行期注入，静态无）", "是否存在取消/跳过按钮及其 clickable 属性", "点击返回键后页面是否消失（验证 onBackPressed 空实现的实际效果）", "窗口是否半透明叠压在下层应用/设置页之上"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中的服务条目，label 由二阶段动态注册决定",
        "why_most_useful": "确认恶意服务是否以动态方式出现、其展示名是否伪装成系统/品牌组件，以及用户被要求开启的到底是哪一个开关",
        "observable_utg_signals": ["服务条目的显示名（是否伪装系统/品牌）", "android:description 说明文案", "开关初始状态与是否被自动勾选", "跳转发生时是否同时存在 pffdfd40f 遮罩"]
      },
      {
        "page_role": "跳转前说明/授权理由页",
        "page_identifier": "pffdfd40f 或其内部 Fragment/Dialog，含引导文案与“去开启”按钮",
        "why_most_useful": "区分该应用采用哪种话术框架（假更新/故障恐吓/清理伪装/隐私承诺），这是判定恶意广告之外是否构成变脸与诱骗的核心证据",
        "observable_utg_signals": ["话术关键词原文（update/error/clean/protect/allow）", "按钮是否唯一且不可取消", "是否有倒计时或反复弹出"]
      },
      {
        "page_role": "远端 WebView 教学页（若存在）",
        "page_identifier": "由 http://d3481mqckui2d7.cloudfront.net 下发，可能以 WebViewActivity 形式出现",
        "why_most_useful": "若引导文案改为远端 HTML 下发，静态与本地资源均无法捕获，只能运行期抓取，可直接证明云控可切换话术",
        "observable_utg_signals": ["WebView 加载 URL 与页面文本", "页面内是否含分步截图/教唆忽略系统警告的文案", "与 cloudfront 域名的网络请求时序"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：①引导文案与页面流转 100% 位于 assets/settings.bin 加密载荷内，静态完全不可见；②敏感字符串 AES 加密，静态字符串检索会漏检 ACTION_ACCESSIBILITY_SETTINGS 等关键字；③二阶段可经 http://d3481mqckui2d7.cloudfront.net 远端更新，同一包体在不同时间/地域可能呈现不同话术；④存在模拟器与无障碍授权状态探测，UTG 采集若在模拟器上进行可能被判定环境而根本不展示引导；⑤Manifest 无任何无障碍服务声明，若二阶段未动态注册，则无障碍页捕获可能为空——此时应转向通知监听（pb01661d3）与透明 Activity 的证据链。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "COERCE_NO_SKIP_NON_CANCELABLE"
  ],
  "code_anchors": [
    "p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#m63cbeb3a",
    "p0a1f9a79.pb05c7c01.p1e8c0249.p718dd98a#mf638b3b7",
    "p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f#onCreate",
    "p0a1f9a79.pb05c7c01.p1e8c0249.pffdfd40f#onBackPressed",
    "p0a1f9a79.pb05c7c01.p1e8c0249.pb01661d3#onNotificationPosted",
    "pc6b2688e#m250ed32b"
  ]
}
```

</details>
