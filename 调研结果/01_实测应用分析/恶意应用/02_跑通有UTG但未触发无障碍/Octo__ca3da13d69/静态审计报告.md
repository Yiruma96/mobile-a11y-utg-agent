# MB_102__ca3da13d69｜Octo — Google Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：164.6s

## 1. 一句话核心结论

- **核心申请方式**：以「Google Chrome」为显示名与无障碍服务名的土耳其语样本，通过 native 壳解密一阶段 DEX 后以全窗口读取型无障碍服务接管设备，引导开启无障碍的具体页面流转被封装在加密载荷内、静态不可见。
- **静态可见性说明**：Manifest、无障碍配置 res/xml/vhlso.xml、strings.xml 与全部字符串资源静态完整可见；真实业务代码与无障碍引导 UI（弹窗/WebView/悬浮遮罩/跳转逻辑）位于 res/raw/tqampnkfskbkj（458908 字节、熵 8.000、无 dex/PK 明文头）中，由 libTCqnfQ.so 的 JNI 方法 UqLPQhk 解密后经 DexClassLoader 反射注入，密钥派生在 native 内部，AES-ECB/CBC 与 RC4 对可见字符串密钥均未命中，纯静态无法还原逐字引导文案与页面流转代码。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ca3da13d69ce07ed9b31314f2404f9c6a2235067406b545d7b00517258cee9d6` |
| 包名 / 年份 | `com.atlotzowj` / 2024 |
| 家族 / 品类 | **Octo**（同池样本数：9） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Google Chrome |
| 引导页宣称品牌/身份 | Google Chrome（Google 官方浏览器品牌，包名 com.atlotzowj 与品牌无任何关联，属完全冒用） |
| 系统无障碍列表服务名 | Google Chrome |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：全部真实类名被混淆为单字母/双字符（com.atlotzowj.p039n、p054s、p013g 等）；无障碍说明使用土耳其语且存在拼写错误「Servisileri」（正确为 Servisleri），降低可信度却仍复用品牌名；com.atlotzowj.p013g 的 android:label 置为空字符串以隐藏标题；多数 Activity 使用 Theme.AppCompat.Transparent.NoActionBar 透明主题并 excludeFromRecents 以不留最近任务痕迹；启动器 Activity 为混淆名而非品牌相关类名。 |
| 无障碍服务类名 | `com.atlotzowj.p039n` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Erişebilirlik Servisileri Etkinleştirme / Erişebilirlik Servisileri Etkinleştirme |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.atlotzowj.QdEXrt（Application）→ com.atlotzowj.p054s（LAUNCHER Activity，载荷内类） | 进程启动时 Application.attachBaseContext(Context) 被系统回调 | 不可静态还原 | **原文**：无（该阶段无 UI）<br>**译注**：该阶段无界面，仅执行解密与类加载 | 无需用户操作，用户点击桌面「Google Chrome」图标即触发 | `com.atlotzowj.QdEXrt.attachBaseContext / com.atlotzowj.QdEXrt.UqLPQhk（native）` |
| 2 | 冷启动入口 | lib/arm64-v8a/libTCqnfQ.so（JNI UqLPQhk）→ res/raw/tqampnkfskbkj → DexClassLoader | attachBaseContext 内调用 native UqLPQhk(Context)，读取 raw 资源解密后反射注入 ClassLoader | 不可静态还原 | **原文**：无（native 层解密，无 UI）<br>**译注**：native 层解密载荷并替换 ClassLoader，此过程对用户不可见 | 无 | `libTCqnfQ.so: Java_com_atlotzowj_QdEXrt_UqLPQhk / res/raw/tqampnkfskbkj` |
| 3 | 引导说明页 | 载荷内混淆 Activity（com.atlotzowj.p013g 透明全屏 / p044r 全屏 / p065d Theme.Dialog 之一，具体归属不可静态确认） | 载荷内 Activity onCreate/onResume（加密 DEX 内，不可静态还原） | 不可静态还原 | **原文**：不可静态还原（明文 DEX 与 res/values/strings.xml 中无引导文案，仅存在 Google Chrome / Erişebilirlik Servisileri Etkinleştirme）<br>**译注**：无法取得逐字文案；资源层仅见品牌名与土耳其语无障碍说明 | 不可静态还原；Manifest 未见该 Activity 声明跳过/取消入口 | `AndroidManifest.xml: activity com.atlotzowj.p013g / com.atlotzowj.p065d（Theme.Dialog）` |
| 4 | 跳无障碍设置 | 系统设置 android.settings.ACCESSIBILITY_SETTINGS（由载荷内代码 Intent 拉起） | 载荷内代码构造 Settings.ACTION_ACCESSIBILITY_SETTINGS Intent（字符串在加密 DEX 内） | 系统无障碍页 | **原文**：系统页显示服务项：Google Chrome（android:label=@string/a），说明：Erişebilirlik Servisileri Etkinleştirme<br>**译注**：系统无障碍列表中显示名为「Google Chrome」、说明为土耳其语「启用无障碍服务」的服务项，与真实 Google 浏览器高度混淆 | 要求用户进入系统无障碍设置并开启「Google Chrome」服务开关 | `res/values/strings.xml#L3-L4 / res/xml/vhlso.xml#L2 / AndroidManifest.xml service com.atlotzowj.p039n` |
| 5 | 拒权反馈循环 | 载荷内 Activity/Service 与透明 Activity（com.atlotzowj.p030w、p068e 均 noHistory=true，p078h singleTask） | 从设置页返回后载荷 Activity onResume / 广播接收器（p088s 监听 SCREEN_ON、USER_PRESENT、BOOT_COMPLETED）重新拉起 | 不可静态还原 | **原文**：不可静态还原<br>**译注**：无法静态确认是否存在重跳死循环或定时拉起；但 Manifest 中多个 noHistory 透明 Activity 与高优先级（999）启动/亮屏/解锁广播接收器构成可反复拉起的前置条件 | 不可静态还原 | `AndroidManifest.xml: receiver com.atlotzowj.p088s（priority 999）/ activity com.atlotzowj.p030w` |
| 6 | 获权后动作 | com.atlotzowj.p039n（AccessibilityService，typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows） | 系统绑定服务后 onServiceConnected，接收 typeAllMask 全部无障碍事件 | 不可静态还原 | **原文**：无（后台运行，无界面）<br>**译注**：获权后进入后台，无任何界面提示；配合 READ_SMS/SEND_SMS/CALL_PHONE/QUERY_ALL_PACKAGES 与设备管理器（res/xml/kufobow）执行短信、拨号、应用枚举等操作 | 无（获权后不再需要用户交互） | `AndroidManifest.xml: service com.atlotzowj.p039n / res/xml/vhlso.xml#L2` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面/应用列表图标名称：@string/a = 「Google Chrome」（AndroidManifest.xml application android:label）
- 系统无障碍服务列表项名称：@string/a = 「Google Chrome」（service com.atlotzowj.p039n android:label）
- 系统无障碍服务列表项说明文字：@string/jDrnan = 「Erişebilirlik Servisileri Etkinleştirme」（res/xml/vhlso.xml 与 res/xml-v22/vhlso.xml 的 android:description）
- 透明全屏 Activity com.atlotzowj.p013g（Theme.NoTitleBar.Fullscreen、android:label="" 空标签）——疑似承载引导内容但实现类在加密载荷内
- Theme.Dialog 型 Activity com.atlotzowj.p065d 与 transparent NoActionBar 的 com.atlotzowj.p030w / p068e——疑似引导弹窗载体，文案不可静态还原
- 加密载荷 res/raw/tqampnkfskbkj 内的一阶段 DEX——全部实际引导文案（弹窗正文、按钮文字、WebView HTML/远端页面）应在此，静态不可读

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Chrome | 谷歌浏览器（Chrome） | `res/values/strings.xml key=a（application android:label 与无障碍 service android:label 均引用）` | 未知 |
| tr | Erişebilirlik Servisileri Etkinleştirme | 启用无障碍服务（原文 Servisileri 为拼写错误，正确应为 Servisleri） | `res/values/strings.xml key=jDrnan（res/xml/vhlso.xml android:description）` | 受限设置分步教学 |
| numeric | 151896084210 | 纯数字串，疑似硬编码标识/配置项（用途需载荷解密后确认） | `res/values/strings.xml key=sbrumrobfefvwjry` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态确认。Manifest 具备反复拉起条件：receiver com.atlotzowj.p088s 以 priority 999 监听 BOOT_COMPLETED、QUICKBOOT_POWERON、USER_PRESENT、SCREEN_ON、PACKAGE_ADDED/REMOVED；activity com.atlotzowj.p078h 为 singleTask；com.atlotzowj.p030w、p068e 为 noHistory 透明 Activity，可由上述事件在用户返回设置页后重新压栈。
- **遮罩叠层 / 高仿系统设置页**：静态可见层未见 SYSTEM_ALERT_WINDOW 权限声明，故无悬浮窗遮罩；但存在 Theme.AppCompat.Transparent.NoActionBar 的透明 Activity（p030w、p068e）与 Theme.NoTitleBar.Fullscreen 的全屏 Activity（p013g、p044r），具备“伪设置页/全屏引导层”载体条件，具体实现不可静态还原。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=30，未声明任何 Android 13 受限设置相关引导；ACTION_APPLICATION_DETAILS_SETTINGS 字符串在可见 DEX 中无命中，相关实现若存在则在加密载荷内）
- **获权后即时行为与防撤权机制**：不可静态确认。已确认存在设备管理器接收器 com.atlotzowj.p045j（BIND_DEVICE_ADMIN，meta-data res/xml/kufobow）与 USES_POLICY_FORCE_LOCK 权限，具备阻碍卸载/锁屏对抗能力；是否在获权后监听设置页并 GLOBAL_ACTION_BACK 阻止撤权，需载荷解密确认。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在进程启动后立即挂 Application.attachBaseContext 之后的钩子，同时监控 startActivity 的目标 Intent：一旦出现 android.settings.ACCESSIBILITY_SETTINGS（或 android.settings.APPLICATION_DETAILS_SETTINGS）立即在跳转前 300ms 与跳转后 500ms 各抓一帧；另一路在 com.atlotzowj.p013g / p065d / p030w 任一 Activity onResume 时抓帧（这些是载荷 UI 的实际载体）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在明显盲区：一阶段 DEX 由 libTCqnfQ.so 在 attachBaseContext 阶段从 res/raw/tqampnkfskbkj 解密并以 DexClassLoader 反射加载，密钥派生在 native 内完成（熵 8.000，AES/RC4 用可见字符串密钥均未命中），因此引导文案、跳转 Intent 字符串、按钮逻辑在静态层完全不可见；若引导页由远端下发（usesCleartextTraffic=true 且具备 INTERNET），文案还会随云端变化，静态与单次 UTG 均可能漏检。需在运行期以 attachBaseContext 后钩子 + startActivity 监控为主，静态结论仅覆盖 Manifest/资源层的身份伪装与无障碍能力声明。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗页（载荷解密后的首个 UI）** | 透明/全屏 Activity com.atlotzowj.p013g（无标题栏、label 为空）或 Theme.Dialog 型 com.atlotzowj.p065d，画面常为居中小弹窗 + 单一确认按钮 | 这是用户第一次被告知“为什么需要无障碍”的位置，逐字文案与按钮数量直接决定是良性说明还是恐吓/假更新诱导 | 弹窗标题与正文全文；是否存在取消/跳过按钮（按钮数量与文字）；是否出现品牌 Logo、更新进度条、错误/风险提示等诱导元素 |
| **跳转前说明页/教学页（若有）** | com.atlotzowj.p044r 或 com.atlotzowj.p068e 全屏 Activity，可能内嵌 WebView | 若为 WebView，可判定文案来自本地 assets 还是远端 URL（远端则属云端可变引导，规避性强），并取得完整 HTML 逐字文本 | WebView 加载的 URL 或本地 file:// 路径；页面内的分步序号/箭头指示图；是否出现土耳其语与英文混排 |
| **系统无障碍服务列表项** | 设置 → 无障碍 → 已下载的服务，条目名称「Google Chrome」，副标题「Erişebilirlik Servisileri Etkinleştirme」 | 这是伪造身份与真实包名 com.atlotzowj 冲突最直观的位置，也是用户最终授权点，可作为身份冒用的截图证据 | 条目显示名与副标题原文；开关状态（未开启/已开启）；同页面是否存在其他同名「Google Chrome」条目 |
| **设置页返回后的叠层/重跳页** | 从无障碍设置按返回后 500～1500ms 内新出现的 Activity（预期为 p030w/p068e 透明页或再次弹出 p013g） | 用于判定拒权后是否存在死循环重跳或半透明遮罩压迫，是区分“引导”与“强迫”的关键帧 | 返回后是否立即重现同一弹窗（时间间隔）；是否存在半透明黑底遮罩覆盖系统设置；是否出现“必须开启才能使用”类强制话术 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.atlotzowj.QdEXrt.attachBaseContext`
- `com.atlotzowj.QdEXrt.UqLPQhk（native，libTCqnfQ.so: Java_com_atlotzowj_QdEXrt_UqLPQhk）`
- `res/raw/tqampnkfskbkj（加密一阶段 DEX 载荷，458908 字节，熵 8.000）`
- `res/xml/vhlso.xml（accessibility-service: typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows）`
- `res/values/strings.xml#L3-L4（a=Google Chrome，jDrnan=Erişebilirlik Servisileri Etkinleştirme）`
- `AndroidManifest.xml: service com.atlotzowj.p039n / activity com.atlotzowj.p013g / receiver com.atlotzowj.p088s`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，已达工具预算上限）

**静态可见性判定：`packed_or_encrypted`（一阶段 Native 解密加载壳 + AES/流密码加密 DEX 载荷）**

已确认事实：

1. **外壳结构极简、无真实业务代码**：`classes.dex` 仅 2756 字节，只含 8 个类，其中唯一的逻辑类是 [QdEXrt.attachBaseContext()](<resource-unit:#1.dex1 code:com.atlotzowj.QdEXrt#attachBaseContext>)，它在 `super.attachBaseContext()` 之后立即调用 native 方法 `UqLPQhk(Context)`。真正的 Activity/Service 类（`p054s`、`p039n`、`p013g` 等）**在 DEX 中完全不存在**，说明它们都位于加密载荷中。
2. **Native 壳的解密路径明确**：[libTCqnfQ.so](<resource-unit:#1.so1 byte:0x0>) 导出 `Java_com_atlotzowj_QdEXrt_UqLPQhk`，字符串包含 `dalvik/system/DexClassLoader`、`openRawResource`、`w/tqampnkfskbkj`、`getDeclaredField`、`setAccessible`、`currentActivityThread`、`mPackages`、`getExternalCache`、`ClassLoader`，由此可确认其完整流程为“读取 raw 资源 → native 解密 → 反射注入 ClassLoader → 启动载荷”。混淆类 `hLAxxpoiLeIhH`、`eDBkpkWDoAuN` 提供对称解密函数（`mBIHirESKf`、`KdtmApWCtI`、`PVIuGarvyh` 等）。
3. **加密载荷**：[res/raw/tqampnkfskbkj](<resource-unit:#1 file:res/raw/tqampnkfskbkj>) 共 458908 字节，熵值 8.000，字节分布覆盖全部 256 个值，内部不含 `dex\n`/`PK\x03\x04` 明文魔数，长度也非 16 的整数倍；我用包内可见字符串尝试了 AES-ECB/CBC 和 RC4 两种方式，用 `Z6D7i4oFVdvBsHA1`、`xYWYFEkY8JlrElY6nt`、`151896084210` 作密钥均未解出 DEX 头，因此**密钥派生完全在 native 代码中完成，纯静态条件无法还原**。
4. **无障碍声明与身份伪装（Manifest/资源层，静态完整可见）**：
   - 服务 `com.atlotzowj.p039n` 绑定 `BIND_ACCESSIBILITY_SERVICE`，`android:label="@string/a"` = **`Google Chrome`**；
   - 配置 [res/xml/vhlso.xml](<resource-unit:#1 file:res/xml/vhlso.xml#L1-L3>)：`typeAllMask`、`canRetrieveWindowContent="true"`、`flagRetrieveInteractiveWindows`、`flagReportViewIds`、`flagIncludeNotImportantViews` —— 具备**读取全部窗口内容与交互控件**的最高观测能力，远超“浏览器”所需；
   - `android:description="@string/jDrnan"` = **`Erişebilirlik Servisileri Etkinleştirme`**（土耳其语“启用无障碍服务”，且 `Servisileri` 为拼写错误，正确应为 `Servisleri`）。
   - 应用显示名同为 `Google Chrome`，包名 `com.atlotzowj` 与品牌完全无关；启动 Activity 为混淆名 `com.atlotzowj.p054s`；多数 Activity 使用 `Theme.AppCompat.Transparent.NoActionBar` 透明主题并 `excludeFromRecents="true"`，`p013g` 甚至 `android:label=""`（空标签）——典型隐藏 UI 手法。
5. **运行期引导流程本身不在可见层**：`ACTION_ACCESSIBILITY_SETTINGS` / `ACTION_APPLICATION_DETAILS_SETTINGS` 字符串在明文 DEX 中均无命中，引导弹窗/WebView/悬浮遮罩的实现代码全部位于加密 DEX 内，故第 3～6 步只能标注为“不可静态还原”，仅能依据 Manifest 与权限共现（`WRITE_SETTINGS`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`、`QUERY_ALL_PACKAGES`、`READ_SMS/SEND_SMS/CALL_PHONE`、设备管理器 `kufobow`）判定其必然在获权后执行短信/电话/应用枚举类操作。

**结论**：该样本是 Octo 家族的“Chrome 仿冒 + 无障碍远控”木马。它在 Manifest 层已经完成伪装（Chrome 名称 + 土耳其语无障碍说明 + 全窗口读取能力），引导开启无障碍的 UI 流转（UTG 需捕获的弹窗、遮罩、跳转）被封装在 native 解密的一阶段 DEX 中，静态无法取得逐字文案。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest、无障碍配置 res/xml/vhlso.xml、strings.xml 与全部字符串资源静态完整可见；真实业务代码与无障碍引导 UI（弹窗/WebView/悬浮遮罩/跳转逻辑）位于 res/raw/tqampnkfskbkj（458908 字节、熵 8.000、无 dex/PK 明文头）中，由 libTCqnfQ.so 的 JNI 方法 UqLPQhk 解密后经 DexClassLoader 反射注入，密钥派生在 native 内部，AES-ECB/CBC 与 RC4 对可见字符串密钥均未命中，纯静态无法还原逐字引导文案与页面流转代码。",
  "summary_one_liner": "以「Google Chrome」为显示名与无障碍服务名的土耳其语样本，通过 native 壳解密一阶段 DEX 后以全窗口读取型无障碍服务接管设备，引导开启无障碍的具体页面流转被封装在加密载荷内、静态不可见。",
  "disguise_identity": {
    "app_display_name": "Google Chrome",
    "claimed_brand_or_persona": "Google Chrome（Google 官方浏览器品牌，包名 com.atlotzowj 与品牌无任何关联，属完全冒用）",
    "a11y_service_label": "Google Chrome",
    "identity_mismatch": true,
    "obfuscation_tricks": "全部真实类名被混淆为单字母/双字符（com.atlotzowj.p039n、p054s、p013g 等）；无障碍说明使用土耳其语且存在拼写错误「Servisileri」（正确为 Servisleri），降低可信度却仍复用品牌名；com.atlotzowj.p013g 的 android:label 置为空字符串以隐藏标题；多数 Activity 使用 Theme.AppCompat.Transparent.NoActionBar 透明主题并 excludeFromRecents 以不留最近任务痕迹；启动器 Activity 为混淆名而非品牌相关类名。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.atlotzowj.QdEXrt（Application）→ com.atlotzowj.p054s（LAUNCHER Activity，载荷内类）",
      "trigger_event": "进程启动时 Application.attachBaseContext(Context) 被系统回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（该阶段无 UI）",
      "shown_text_zh": "该阶段无界面，仅执行解密与类加载",
      "user_action_requested": "无需用户操作，用户点击桌面「Google Chrome」图标即触发",
      "code_anchor": "com.atlotzowj.QdEXrt.attachBaseContext / com.atlotzowj.QdEXrt.UqLPQhk（native）"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "lib/arm64-v8a/libTCqnfQ.so（JNI UqLPQhk）→ res/raw/tqampnkfskbkj → DexClassLoader",
      "trigger_event": "attachBaseContext 内调用 native UqLPQhk(Context)，读取 raw 资源解密后反射注入 ClassLoader",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（native 层解密，无 UI）",
      "shown_text_zh": "native 层解密载荷并替换 ClassLoader，此过程对用户不可见",
      "user_action_requested": "无",
      "code_anchor": "libTCqnfQ.so: Java_com_atlotzowj_QdEXrt_UqLPQhk / res/raw/tqampnkfskbkj"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "载荷内混淆 Activity（com.atlotzowj.p013g 透明全屏 / p044r 全屏 / p065d Theme.Dialog 之一，具体归属不可静态确认）",
      "trigger_event": "载荷内 Activity onCreate/onResume（加密 DEX 内，不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "不可静态还原（明文 DEX 与 res/values/strings.xml 中无引导文案，仅存在 Google Chrome / Erişebilirlik Servisileri Etkinleştirme）",
      "shown_text_zh": "无法取得逐字文案；资源层仅见品牌名与土耳其语无障碍说明",
      "user_action_requested": "不可静态还原；Manifest 未见该 Activity 声明跳过/取消入口",
      "code_anchor": "AndroidManifest.xml: activity com.atlotzowj.p013g / com.atlotzowj.p065d（Theme.Dialog）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 android.settings.ACCESSIBILITY_SETTINGS（由载荷内代码 Intent 拉起）",
      "trigger_event": "载荷内代码构造 Settings.ACTION_ACCESSIBILITY_SETTINGS Intent（字符串在加密 DEX 内）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "系统页显示服务项：Google Chrome（android:label=@string/a），说明：Erişebilirlik Servisileri Etkinleştirme",
      "shown_text_zh": "系统无障碍列表中显示名为「Google Chrome」、说明为土耳其语「启用无障碍服务」的服务项，与真实 Google 浏览器高度混淆",
      "user_action_requested": "要求用户进入系统无障碍设置并开启「Google Chrome」服务开关",
      "code_anchor": "res/values/strings.xml#L3-L4 / res/xml/vhlso.xml#L2 / AndroidManifest.xml service com.atlotzowj.p039n"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "载荷内 Activity/Service 与透明 Activity（com.atlotzowj.p030w、p068e 均 noHistory=true，p078h singleTask）",
      "trigger_event": "从设置页返回后载荷 Activity onResume / 广播接收器（p088s 监听 SCREEN_ON、USER_PRESENT、BOOT_COMPLETED）重新拉起",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "不可静态还原",
      "shown_text_zh": "无法静态确认是否存在重跳死循环或定时拉起；但 Manifest 中多个 noHistory 透明 Activity 与高优先级（999）启动/亮屏/解锁广播接收器构成可反复拉起的前置条件",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml: receiver com.atlotzowj.p088s（priority 999）/ activity com.atlotzowj.p030w"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.atlotzowj.p039n（AccessibilityService，typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows）",
      "trigger_event": "系统绑定服务后 onServiceConnected，接收 typeAllMask 全部无障碍事件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（后台运行，无界面）",
      "shown_text_zh": "获权后进入后台，无任何界面提示；配合 READ_SMS/SEND_SMS/CALL_PHONE/QUERY_ALL_PACKAGES 与设备管理器（res/xml/kufobow）执行短信、拨号、应用枚举等操作",
      "user_action_requested": "无（获权后不再需要用户交互）",
      "code_anchor": "AndroidManifest.xml: service com.atlotzowj.p039n / res/xml/vhlso.xml#L2"
    }
  ],
  "text_presentation_locations": [
    "桌面/应用列表图标名称：@string/a = 「Google Chrome」（AndroidManifest.xml application android:label）",
    "系统无障碍服务列表项名称：@string/a = 「Google Chrome」（service com.atlotzowj.p039n android:label）",
    "系统无障碍服务列表项说明文字：@string/jDrnan = 「Erişebilirlik Servisileri Etkinleştirme」（res/xml/vhlso.xml 与 res/xml-v22/vhlso.xml 的 android:description）",
    "透明全屏 Activity com.atlotzowj.p013g（Theme.NoTitleBar.Fullscreen、android:label=\"\" 空标签）——疑似承载引导内容但实现类在加密载荷内",
    "Theme.Dialog 型 Activity com.atlotzowj.p065d 与 transparent NoActionBar 的 com.atlotzowj.p030w / p068e——疑似引导弹窗载体，文案不可静态还原",
    "加密载荷 res/raw/tqampnkfskbkj 内的一阶段 DEX——全部实际引导文案（弹窗正文、按钮文字、WebView HTML/远端页面）应在此，静态不可读"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Chrome",
      "text_zh": "谷歌浏览器（Chrome）",
      "source_location": "res/values/strings.xml key=a（application android:label 与无障碍 service android:label 均引用）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "Erişebilirlik Servisileri Etkinleştirme",
      "text_zh": "启用无障碍服务（原文 Servisileri 为拼写错误，正确应为 Servisleri）",
      "source_location": "res/values/strings.xml key=jDrnan（res/xml/vhlso.xml android:description）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "numeric",
      "text_verbatim": "151896084210",
      "text_zh": "纯数字串，疑似硬编码标识/配置项（用途需载荷解密后确认）",
      "source_location": "res/values/strings.xml key=sbrumrobfefvwjry",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态确认。Manifest 具备反复拉起条件：receiver com.atlotzowj.p088s 以 priority 999 监听 BOOT_COMPLETED、QUICKBOOT_POWERON、USER_PRESENT、SCREEN_ON、PACKAGE_ADDED/REMOVED；activity com.atlotzowj.p078h 为 singleTask；com.atlotzowj.p030w、p068e 为 noHistory 透明 Activity，可由上述事件在用户返回设置页后重新压栈。",
    "overlay_or_fake_settings": "静态可见层未见 SYSTEM_ALERT_WINDOW 权限声明，故无悬浮窗遮罩；但存在 Theme.AppCompat.Transparent.NoActionBar 的透明 Activity（p030w、p068e）与 Theme.NoTitleBar.Fullscreen 的全屏 Activity（p013g、p044r），具备“伪设置页/全屏引导层”载体条件，具体实现不可静态还原。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=30，未声明任何 Android 13 受限设置相关引导；ACTION_APPLICATION_DETAILS_SETTINGS 字符串在可见 DEX 中无命中，相关实现若存在则在加密载荷内）",
    "post_grant_anti_removal": "不可静态确认。已确认存在设备管理器接收器 com.atlotzowj.p045j（BIND_DEVICE_ADMIN，meta-data res/xml/kufobow）与 USES_POLICY_FORCE_LOCK 权限，具备阻碍卸载/锁屏对抗能力；是否在获权后监听设置页并 GLOBAL_ACTION_BACK 阻止撤权，需载荷解密确认。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在进程启动后立即挂 Application.attachBaseContext 之后的钩子，同时监控 startActivity 的目标 Intent：一旦出现 android.settings.ACCESSIBILITY_SETTINGS（或 android.settings.APPLICATION_DETAILS_SETTINGS）立即在跳转前 300ms 与跳转后 500ms 各抓一帧；另一路在 com.atlotzowj.p013g / p065d / p030w 任一 Activity onResume 时抓帧（这些是载荷 UI 的实际载体）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗页（载荷解密后的首个 UI）",
        "page_identifier": "透明/全屏 Activity com.atlotzowj.p013g（无标题栏、label 为空）或 Theme.Dialog 型 com.atlotzowj.p065d，画面常为居中小弹窗 + 单一确认按钮",
        "why_most_useful": "这是用户第一次被告知“为什么需要无障碍”的位置，逐字文案与按钮数量直接决定是良性说明还是恐吓/假更新诱导",
        "observable_utg_signals": ["弹窗标题与正文全文", "是否存在取消/跳过按钮（按钮数量与文字）", "是否出现品牌 Logo、更新进度条、错误/风险提示等诱导元素"]
      },
      {
        "page_role": "跳转前说明页/教学页（若有）",
        "page_identifier": "com.atlotzowj.p044r 或 com.atlotzowj.p068e 全屏 Activity，可能内嵌 WebView",
        "why_most_useful": "若为 WebView，可判定文案来自本地 assets 还是远端 URL（远端则属云端可变引导，规避性强），并取得完整 HTML 逐字文本",
        "observable_utg_signals": ["WebView 加载的 URL 或本地 file:// 路径", "页面内的分步序号/箭头指示图", "是否出现土耳其语与英文混排"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 → 无障碍 → 已下载的服务，条目名称「Google Chrome」，副标题「Erişebilirlik Servisileri Etkinleştirme」",
        "why_most_useful": "这是伪造身份与真实包名 com.atlotzowj 冲突最直观的位置，也是用户最终授权点，可作为身份冒用的截图证据",
        "observable_utg_signals": ["条目显示名与副标题原文", "开关状态（未开启/已开启）", "同页面是否存在其他同名「Google Chrome」条目"]
      },
      {
        "page_role": "设置页返回后的叠层/重跳页",
        "page_identifier": "从无障碍设置按返回后 500～1500ms 内新出现的 Activity（预期为 p030w/p068e 透明页或再次弹出 p013g）",
        "why_most_useful": "用于判定拒权后是否存在死循环重跳或半透明遮罩压迫，是区分“引导”与“强迫”的关键帧",
        "observable_utg_signals": ["返回后是否立即重现同一弹窗（时间间隔）", "是否存在半透明黑底遮罩覆盖系统设置", "是否出现“必须开启才能使用”类强制话术"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在明显盲区：一阶段 DEX 由 libTCqnfQ.so 在 attachBaseContext 阶段从 res/raw/tqampnkfskbkj 解密并以 DexClassLoader 反射加载，密钥派生在 native 内完成（熵 8.000，AES/RC4 用可见字符串密钥均未命中），因此引导文案、跳转 Intent 字符串、按钮逻辑在静态层完全不可见；若引导页由远端下发（usesCleartextTraffic=true 且具备 INTERNET），文案还会随云端变化，静态与单次 UTG 均可能漏检。需在运行期以 attachBaseContext 后钩子 + startActivity 监控为主，静态结论仅覆盖 Manifest/资源层的身份伪装与无障碍能力声明。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY"
  ],
  "code_anchors": [
    "com.atlotzowj.QdEXrt.attachBaseContext",
    "com.atlotzowj.QdEXrt.UqLPQhk（native，libTCqnfQ.so: Java_com_atlotzowj_QdEXrt_UqLPQhk）",
    "res/raw/tqampnkfskbkj（加密一阶段 DEX 载荷，458908 字节，熵 8.000）",
    "res/xml/vhlso.xml（accessibility-service: typeAllMask + canRetrieveWindowContent + flagRetrieveInteractiveWindows）",
    "res/values/strings.xml#L3-L4（a=Google Chrome，jDrnan=Erişebilirlik Servisileri Etkinleştirme）",
    "AndroidManifest.xml: service com.atlotzowj.p039n / activity com.atlotzowj.p013g / receiver com.atlotzowj.p088s"
  ]
}
```

**覆盖边界说明**：本次受 14 次工具预算限制，未能对 `libTCqnfQ.so` 的解密函数（`eDBkpkWDoAuN::mBIHirESKf`、`hLAxxpoiLeIhH::tcWCKfrsReBbn`）做 angr 函数级反编译，因此 `res/raw/tqampnkfskbkj` 的明文（含无障碍引导 UI 代码与远端 C2 配置）仍未取得；步骤 3、5、6 中的逐字文案与循环机制为基于 Manifest 载体能力的推断，已在 JSON 中明确标注“不可静态还原”。未登记风险条目（预算耗尽，结论以本报告为准）。

</details>
