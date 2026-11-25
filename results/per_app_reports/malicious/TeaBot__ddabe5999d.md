# MB_117__ddabe5999d｜TeaBot — QR Code Scanner: Add-on Recognizer

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：219.5s

## 1. 一句话核心结论

- **核心申请方式**：QR 扫描器外壳应用以 MultidexPacker 存根 + 加密二阶段载荷隐藏全部真实代码，Manifest 预置无标签、无说明、全事件掩码且可手势操作的无障碍服务，并捆绑短信读写、全应用枚举、悬浮窗与忽略电池优化权限，属 TeaBot 家族典型的无障碍+SMS+悬浮窗获权结构。
- **静态可见性说明**：可见 classes.dex 为 MultidexPacker 存根（APKiD 判定 packer: MultidexPacker，含 anti_vm），仅含反射式 Application 替换与单字节 XOR 字符串解密逻辑；Manifest 声明的 com.rmowa.wpamz.* 全部类（无障碍服务、注入 Activity、短信 Receiver）在可见 DEX 中出现 0 次，真实业务与全部权限引导代码位于 assets/giwj8II/gGpi8gfof1.hUf（zlib 包裹的高熵密文，inflate 后 286154 字节无 dex/PK 魔数，二次 inflate 与 XOR 穷举均失败，判定为 AES 类加密二阶段载荷）。因此 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转点、引导弹窗、悬浮遮罩与拒权循环逻辑均不可静态还原，仅 Manifest、无障碍 XML 配置、权限集与存根脱壳逻辑可见。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `ddabe5999dbc9ffbc8b804a7ea6bb61415bc88e346b2d2c0d53bfff9dcc88d32` |
| 包名 / 年份 | `com.rmowa.wpamz` / 2022 |
| 家族 / 品类 | **TeaBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | QR Code Scanner: Add-on Recognizer |
| 引导页宣称品牌/身份 | 二维码扫描/识别工具（QR Code Scanner: Add-on Recognizer），并复用 Google Play services 标准提示资源营造正规工具观感 |
| 系统无障碍列表服务名 | 服务未声明 android:label，系统无障碍列表将回退显示应用名 “QR Code Scanner: Add-on Recognizer”（对应类 com.rmowa.wpamz.UIDNwaidobaWIODb） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：三套互不相关命名并存：预筛包名 com.rmowa.wpamz、Manifest 实际 package="in.makaek.lichi"、Provider authority="com.buenosmama.qrcode.provider"；无障碍服务与多个 Activity 显式 android:label=""（空标签）以在列表中隐藏名称；无障碍 XML 无 description，规避系统对服务用途的展示；Application 类 com.caffe.cociss.k 在运行期把 ApplicationInfo.className 改写为 android.app.Application 并通过 ActivityThread 反射回填 mInitialApplication，隐藏真实入口类名；常量采用单字节 XOR 加密（a(int) 解密 android.app.ActivityThread / currentActivityThread 等）；包内无 lib/ 与第二 dex，真实类由加密资产提供；未见 isAccessibilityTool 伪造与同形字，因真实代码在密文中不可核验。 |
| 无障碍服务类名 | `com.rmowa.wpamz.UIDNwaidobaWIODb` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.caffe.cociss.k（Application，Manifest android:name 指定） | 进程创建时 attachBaseContext/onCreate | 不可静态还原 | 无 | 无 | `com.caffe.cociss.k#attachBaseContext / com.caffe.cociss.k#onCreate` |
| 2 | 冷启动入口 | com.caffe.cociss.k.a()（反射脱壳存根） | Application 初始化时反射调用 ActivityThread 相关方法 | 不可静态还原 | **原文**：无（XOR 解密出的常量：android.app.ActivityThread / currentActivityThread / mInitialApplication）<br>**译注**：无界面，仅反射替换 Application 与隐藏真实类名 | 无 | `com.caffe.cociss.k#a() / com.caffe.cociss.k#a(int)` |
| 3 | 业务功能触发 | com.rmowa.wpamz.WNiudwabNUDIba（LAUNCHER Activity，实际类体不在可见 DEX） | 用户点击桌面图标 | 不可静态还原 | **原文**：无（真实布局与文案位于加密二阶段载荷）<br>**译注**：桌面显示 “QR Code Scanner: Add-on Recognizer”，进入后实际界面不可静态还原 | 不可静态还原 | `AndroidManifest.xml: activity com.rmowa.wpamz.WNiudwabNUDIba（MAIN/LAUNCHER）` |
| 4 | 引导说明页 | 疑似引导 Activity：com.rmowa.wpamz.util.nidwoanAIOWDbwaiuBa / com.rmowa.wpamz.nawIODnaiowdna / com.rmowa.wpamz.util.AUInawiOBFA / com.rmowa.wpamz.util.uaiwdBuaiwbdaD / com.rmowa.wpamz.util.InioawndOIADNwaiond（均 Theme.NoTitleBar、label=""） | 不可静态还原（推测由启动页或功能开关触发） | 不可静态还原 | **原文**：无（包内未见引导类 HTML/文案资源；assets 下无引导 html）<br>**译注**：不可静态还原；这些无标题、空标签 Activity 在 Manifest 中已预留为跳转/注入承载页 | 不可静态还原 | `AndroidManifest.xml: com.rmowa.wpamz.util.nawIODnaiowdna / com.rmowa.wpamz.util.AUInawiOBFA 等` |
| 5 | 跳无障碍设置 | 系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS | 不可静态还原（可见 DEX 中不存在该 action 字符串，跳转调用位于加密载荷） | 系统无障碍页 | **原文**：无（包内可见部分无该 action 常量）<br>**译注**：不可静态还原；最终落点为系统无障碍服务列表，其中服务项因无 label/description 仅显示应用名 | 不可静态还原 | `可见 DEX 中 ACCESSIBILITY_SETTINGS 出现 0 次；对应调用应在 assets/giwj8II/gGpi8gfof1.hUf 解密后的 com.rmowa.wpamz.* 中` |
| 6 | 拒权反馈循环 | 不可静态还原（疑似无标题 Activity + SYSTEM_ALERT_WINDOW 悬浮窗配合） | 不可静态还原（可能为 onResume / 定时器 / USER_PRESENT 广播） | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest.xml: receiver com.rmowa.wpamz.receiver.eifbiaFBAUIFB（BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED）` |
| 7 | 获权后动作 | 无障碍服务 com.rmowa.wpamz.UIDNwaidobaWIODb（配置 res/xml/asclllservizio.xml） | 用户在系统设置中开启该服务 | 系统无障碍页 | **原文**：无（XML 仅含属性：typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRetrieveInteractiveWindows）<br>**译注**：服务说明为空；开启后可读取全部窗口内容并执行手势，能力远超二维码识别所需 | 在系统无障碍列表中点开该无说明服务并授权 | `res/xml/asclllservizio.xml / AndroidManifest.xml: service com.rmowa.wpamz.UIDNwaidobaWIODb` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面图标名称：AndroidManifest application android:label="QR Code Scanner: Add-on Recognizer"（res 资源引用 @mipmap/ic_launcher）
- 系统无障碍服务列表项名称：服务未声明 android:label，回退显示应用名；无 android:description，服务用途说明栏为空
- 多个承载页面（com.rmowa.wpamz.inject.uibwduIABuIaw、com.rmowa.wpamz.util.nidwoanAIOWDbwaiuBa、com.rmowa.wpamz.nawIODnaiowdna、com.rmowa.wpamz.util.AUInawiOBFA、com.rmowa.wpamz.util.uaiwdBuaiwbdaD、com.rmowa.wpamz.opnoPAWNDioaNDW）显式 android:label="" 且 Theme.NoTitleBar，标题栏不呈现任何文字
- res/values/strings.xml 中 common_google_play_services_* 系列（Enable/Install/Update Google Play services 等）为 GMS 库标准资源，非应用自写诱导文案，不应视为引导页面
- 真实引导弹窗/悬浮遮罩/WebView 教学页文字：位于 assets/giwj8II/gGpi8gfof1.hUf 加密载荷内，静态不可见；assets 目录下未发现引导用 html 文件

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | QR Code Scanner: Add-on Recognizer | 二维码扫描器：附加识别器 | `AndroidManifest.xml application@android:label` | 清理工具伪装 |
| en | %1$s won't work unless you enable Google Play services. | %1$s 需要启用 Google Play 服务才能正常工作。 | `res/values/strings.xml : common_google_play_services_enable_text（GMS 库标准资源）` | 良性透明说明 |
| en | %1$s won't run without Google Play services, which are missing from your device. | %1$s 无法运行，因为您的设备缺少 Google Play 服务。 | `res/values/strings.xml : common_google_play_services_install_text（GMS 库标准资源）` | 良性透明说明 |
| en | %1$s won't run unless you update Google Play services. | %1$s 需要更新 Google Play 服务才能运行。 | `res/values/strings.xml : common_google_play_services_update_text（GMS 库标准资源）` | 良性透明说明 |
| en | （空字符串） | 无障碍服务标签与用途说明均为空 | `AndroidManifest.xml service@android:label 缺失；res/xml/asclllservizio.xml 无 android:description` | 未知 |
| en | （不可静态还原） | 真实引导文案位于加密二阶段载荷，无法逐字引用 | `assets/giwj8II/gGpi8gfof1.hUf（加密）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：可见 DEX 中不含任何无障碍/应用详情设置 action 常量，重跳与定时拉起逻辑在加密载荷内；Manifest 层面已具备 USER_PRESENT、BOOT_COMPLETED、QUICKBOOT_POWERON、PACKAGE_ADDED 广播接收器（priority 988）与 SYSTEM_ALERT_WINDOW、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 权限，具备后台重新拉起与常驻条件，但具体循环实现无法静态确认。
- **遮罩叠层 / 高仿系统设置页**：不可静态还原：已声明 SYSTEM_ALERT_WINDOW 悬浮窗权限，具备叠放引导遮罩/高仿开关页的能力，但未见实现代码与伪造布局资源；预筛 overlay=[] 亦未命中。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=28，未达 Android 13 受限设置门槛；包内亦无 APPLICATION_DETAILS_SETTINGS 相关字符串）
- **获权后即时行为与防撤权机制**：不可静态还原：无障碍配置含 canPerformGestures 与 flagRetrieveInteractiveWindows，理论上可用于全局手势自点确认或干扰撤权，但无 performGlobalAction 调用点可见（可见 DEX 中出现 0 次），实现位于加密载荷内。
- **良性降级 / 替代方案**：无（无降级证据：无障碍服务无说明、无替代手动模式，且同时捆绑短信读写与全应用枚举权限，不具备良性透明说明特征）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以冷启动为起点：在 ActivityThread 反射替换完成后、首个 com.rmowa.wpamz.WNiudwabNUDIba 或任一空标签 Activity（util.nidwoanAIOWDbwaiuBa / nawIODnaiowdna / util.AUInawiOBFA / util.uaiwdBuaiwbdaD / inject.uibwduIABuIaw）压栈的瞬间抓取；同时 Hook Context.startActivity 中 intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的调用，在跳转前 800ms 与返回后 onResume 各抓一帧。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：真实代码全部位于 assets/giwj8II/gGpi8gfof1.hUf 的加密二阶段载荷，静态无法还原跳转点与文案，因此 UTG 必须以运行期为唯一取证途径；此外服务与多个 Activity 的 android:label="" 与无障碍 description 缺失，会使系统列表与页面标题呈现空白，纯文本抓取可能得到空串，需依赖组件名与窗口层级判定；GMS 库标准 common_google_play_services_* 字符串存在被误判为诱导文案的风险，需排除。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/首屏承载页（空标签、无标题 Activity）** | Activity 名 com.rmowa.wpamz.WNiudwabNUDIba 或 util.nidwoanAIOWDbwaiuBa / nawIODnaiowdna / util.AUInawiOBFA，界面无标题栏、无 actionBar 文字 | 这是加密载荷解密后第一个可控界面，是判定“功能触发即弹引导”还是“伪装成二维码扫描器”的分水岭 | 页面文本全部为 QR 扫描相关 vs 直接出现无障碍授权话术；是否存在不可取消（无返回/无跳过按钮）的弹窗；是否出现“启用服务/授权/辅助功能”等关键词 |
| **跳转前引导弹窗或教学页** | Dialog 或 WebView，文案含 accessibility / service / enable / 辅助功能 等关键词 | 直接决定诱导话术类型（假更新、故障恐吓、清理伪装或教唆忽视警告）与载体（原生/本地 HTML/远端 URL） | 弹窗按钮集合（是否有取消/稍后）；WebView URL 域名（本地 file:// 还是远端）；文案是否要求忽略系统安全警告 |
| **系统无障碍服务列表项** | Settings → Accessibility 中条目名称为 “QR Code Scanner: Add-on Recognizer”，说明栏为空 | 确认服务在系统列表中的实际展示名与空说明，是身份伪装与警告缺位的直接证据 | 条目名称是否与应用名一致（无独立服务名）；服务描述是否为空；是否存在空白/换行挤出的条目 |
| **系统设置返回后的遮罩/悬浮引导页** | SYSTEM_ALERT_WINDOW 悬浮窗或重新压栈的无标题 Activity | 判定是否存在拒绝即重跳的死循环或叠层指引（UTG 可直接看到设置页上叠加的另一层窗口） | 返回设置页后是否 1-3 秒内再次跳转 ACCESSIBILITY_SETTINGS；是否存在半透明遮罩与手指引导动画；悬浮窗是否覆盖系统开关位置 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.caffe.cociss.k#a()`
- `com.caffe.cociss.k#a(int)`
- `com.caffe.cociss.k#onCreate`
- `res/xml/asclllservizio.xml`
- `AndroidManifest.xml: service com.rmowa.wpamz.UIDNwaidobaWIODb`
- `assets/giwj8II/gGpi8gfof1.hUf`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

- **可见 DEX 中没有真实业务代码**：`classes.dex`（7.2 MB，dexlib2 编译）中 `Lcom/rmowa`、`wpamz`、`UIDNwaidobaWIODb` 出现次数均为 **0**，且不含 `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`com/android/settings`、`ignore_battery` 等任何跳转字符串。也就是说，Manifest 声明的无障碍服务、注入 Activity、短信 Receiver 等 `com.rmowa.wpamz.*` 类**不在本 DEX 中**，只能由运行期还原的二阶段载荷提供。
- **可见 DEX 是打包器存根**：`APKiD` 判定 `packer: MultidexPacker`，并检出大量 anti_vm 特征；[com.caffe.cociss.k#a()](<resource-unit:#1.dex1 code:com.caffe.cociss.k#a>) 用 `c.a/c.b` 反射调用配合 `a(int)` 的**单字节 XOR 常量解密**（解出 `android.app.ActivityThread`、`currentActivityThread`、`mInitialApplication` 等），随后把 `ApplicationInfo.className` 强制改为 `android.app.Application`，并回填 `ActivityThread` 中的 Application 引用——典型的“反射式 Application 替换 + 隐藏真实类名”脱壳存根；`onCreate` 仅转调还原后的 Application。
- **加密载荷已定位但未还原**：`assets/giwj8II/gGpi8gfof1.hUf`（286 223 B）为 zlib 包裹的高熵密文（inflate 后 286 154 B，无 `dex\n`/`PK`/gzip 魔数，二次 inflate 失败，XOR 穷举无命中），判断为 AES 类加密的二阶段 DEX/载荷；包内无 `lib/` 原生库，无第二份 dex。静态无法取得密钥 → 二阶段代码不可见。
- **Manifest 层可确认的“获权面”**：无障碍服务 [com.rmowa.wpamz.UIDNwaidobaWIODb](<resource-unit:#1 manifest:components>) 绑定 `BIND_ACCESSIBILITY_SERVICE`，配置 [res/xml/asclllservizio.xml](<resource-unit:#1 file:res/xml/asclllservizio.xml>) 为**最高权限档**（`typeAllMask`、`canRetrieveWindowContent`、`canPerformGestures`、`flagRetrieveInteractiveWindows`），且**无 `android:label`、无 `android:description`**；配合 `READ_SMS/RECEIVE_SMS/SEND_SMS/WRITE_SMS`、`QUERY_ALL_PACKAGES`、`SYSTEM_ALERT_WINDOW`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`、开机/`USER_PRESENT`/`PACKAGE_ADDED` 广播——与 TeaBot 家族的“无障碍 + 短信 + 悬浮窗”组合一致。
- **身份不一致（已确认）**：预筛包名 `com.rmowa.wpamz`，实际 Manifest `package="in.makaek.lichi"`；应用名 `QR Code Scanner: Add-on Recognizer`，代码内 Provider authority 却是 `com.buenosmama.qrcode.provider`——至少三套互不相关的命名。
- **预筛字符串不是诱导文案**：所谓 “Google Play services” 系列均来自 `res/values/strings.xml` 的 `common_google_play_services_*`，属 GMS 库标准资源，**不构成诱导弹窗**，不应作为引导证据。
- **引导流程本身不可静态判定**：跳 `ACTION_ACCESSIBILITY_SETTINGS`/`ACTION_APPLICATION_DETAILS_SETTINGS` 的调用点、引导弹窗/悬浮遮罩/WebView 教学页、拒绝后重跳逻辑全部位于加密载荷内，本次静态不可达。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "可见 classes.dex 为 MultidexPacker 存根（APKiD 判定 packer: MultidexPacker，含 anti_vm），仅含反射式 Application 替换与单字节 XOR 字符串解密逻辑；Manifest 声明的 com.rmowa.wpamz.* 全部类（无障碍服务、注入 Activity、短信 Receiver）在可见 DEX 中出现 0 次，真实业务与全部权限引导代码位于 assets/giwj8II/gGpi8gfof1.hUf（zlib 包裹的高熵密文，inflate 后 286154 字节无 dex/PK 魔数，二次 inflate 与 XOR 穷举均失败，判定为 AES 类加密二阶段载荷）。因此 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转点、引导弹窗、悬浮遮罩与拒权循环逻辑均不可静态还原，仅 Manifest、无障碍 XML 配置、权限集与存根脱壳逻辑可见。",
  "summary_one_liner": "QR 扫描器外壳应用以 MultidexPacker 存根 + 加密二阶段载荷隐藏全部真实代码，Manifest 预置无标签、无说明、全事件掩码且可手势操作的无障碍服务，并捆绑短信读写、全应用枚举、悬浮窗与忽略电池优化权限，属 TeaBot 家族典型的无障碍+SMS+悬浮窗获权结构。",
  "disguise_identity": {
    "app_display_name": "QR Code Scanner: Add-on Recognizer",
    "claimed_brand_or_persona": "二维码扫描/识别工具（QR Code Scanner: Add-on Recognizer），并复用 Google Play services 标准提示资源营造正规工具观感",
    "a11y_service_label": "服务未声明 android:label，系统无障碍列表将回退显示应用名 “QR Code Scanner: Add-on Recognizer”（对应类 com.rmowa.wpamz.UIDNwaidobaWIODb）",
    "identity_mismatch": true,
    "obfuscation_tricks": "三套互不相关命名并存：预筛包名 com.rmowa.wpamz、Manifest 实际 package=\"in.makaek.lichi\"、Provider authority=\"com.buenosmama.qrcode.provider\"；无障碍服务与多个 Activity 显式 android:label=\"\"（空标签）以在列表中隐藏名称；无障碍 XML 无 description，规避系统对服务用途的展示；Application 类 com.caffe.cociss.k 在运行期把 ApplicationInfo.className 改写为 android.app.Application 并通过 ActivityThread 反射回填 mInitialApplication，隐藏真实入口类名；常量采用单字节 XOR 加密（a(int) 解密 android.app.ActivityThread / currentActivityThread 等）；包内无 lib/ 与第二 dex，真实类由加密资产提供；未见 isAccessibilityTool 伪造与同形字，因真实代码在密文中不可核验。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.caffe.cociss.k（Application，Manifest android:name 指定）",
      "trigger_event": "进程创建时 attachBaseContext/onCreate",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面",
      "user_action_requested": "无",
      "code_anchor": "com.caffe.cociss.k#attachBaseContext / com.caffe.cociss.k#onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.caffe.cociss.k.a()（反射脱壳存根）",
      "trigger_event": "Application 初始化时反射调用 ActivityThread 相关方法",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（XOR 解密出的常量：android.app.ActivityThread / currentActivityThread / mInitialApplication）",
      "shown_text_zh": "无界面，仅反射替换 Application 与隐藏真实类名",
      "user_action_requested": "无",
      "code_anchor": "com.caffe.cociss.k#a() / com.caffe.cociss.k#a(int)"
    },
    {
      "step": 3,
      "stage": "业务功能触发",
      "screen_or_component": "com.rmowa.wpamz.WNiudwabNUDIba（LAUNCHER Activity，实际类体不在可见 DEX）",
      "trigger_event": "用户点击桌面图标",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（真实布局与文案位于加密二阶段载荷）",
      "shown_text_zh": "桌面显示 “QR Code Scanner: Add-on Recognizer”，进入后实际界面不可静态还原",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml: activity com.rmowa.wpamz.WNiudwabNUDIba（MAIN/LAUNCHER）"
    },
    {
      "step": 4,
      "stage": "引导说明页",
      "screen_or_component": "疑似引导 Activity：com.rmowa.wpamz.util.nidwoanAIOWDbwaiuBa / com.rmowa.wpamz.nawIODnaiowdna / com.rmowa.wpamz.util.AUInawiOBFA / com.rmowa.wpamz.util.uaiwdBuaiwbdaD / com.rmowa.wpamz.util.InioawndOIADNwaiond（均 Theme.NoTitleBar、label=\"\"）",
      "trigger_event": "不可静态还原（推测由启动页或功能开关触发）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（包内未见引导类 HTML/文案资源；assets 下无引导 html）",
      "shown_text_zh": "不可静态还原；这些无标题、空标签 Activity 在 Manifest 中已预留为跳转/注入承载页",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml: com.rmowa.wpamz.util.nawIODnaiowdna / com.rmowa.wpamz.util.AUInawiOBFA 等"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置页 Settings.ACTION_ACCESSIBILITY_SETTINGS",
      "trigger_event": "不可静态还原（可见 DEX 中不存在该 action 字符串，跳转调用位于加密载荷）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（包内可见部分无该 action 常量）",
      "shown_text_zh": "不可静态还原；最终落点为系统无障碍服务列表，其中服务项因无 label/description 仅显示应用名",
      "user_action_requested": "不可静态还原",
      "code_anchor": "可见 DEX 中 ACCESSIBILITY_SETTINGS 出现 0 次；对应调用应在 assets/giwj8II/gGpi8gfof1.hUf 解密后的 com.rmowa.wpamz.* 中"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "不可静态还原（疑似无标题 Activity + SYSTEM_ALERT_WINDOW 悬浮窗配合）",
      "trigger_event": "不可静态还原（可能为 onResume / 定时器 / USER_PRESENT 广播）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不可静态还原；Manifest 已具备 USER_PRESENT、BOOT_COMPLETED、QUICKBOOT_POWERON 广播与悬浮窗权限，具备返回后重新拉起的条件",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml: receiver com.rmowa.wpamz.receiver.eifbiaFBAUIFB（BOOT_COMPLETED/USER_PRESENT/PACKAGE_ADDED）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 com.rmowa.wpamz.UIDNwaidobaWIODb（配置 res/xml/asclllservizio.xml）",
      "trigger_event": "用户在系统设置中开启该服务",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（XML 仅含属性：typeAllMask、canRetrieveWindowContent、canPerformGestures、flagRetrieveInteractiveWindows）",
      "shown_text_zh": "服务说明为空；开启后可读取全部窗口内容并执行手势，能力远超二维码识别所需",
      "user_action_requested": "在系统无障碍列表中点开该无说明服务并授权",
      "code_anchor": "res/xml/asclllservizio.xml / AndroidManifest.xml: service com.rmowa.wpamz.UIDNwaidobaWIODb"
    }
  ],
  "text_presentation_locations": [
    "桌面图标名称：AndroidManifest application android:label=\"QR Code Scanner: Add-on Recognizer\"（res 资源引用 @mipmap/ic_launcher）",
    "系统无障碍服务列表项名称：服务未声明 android:label，回退显示应用名；无 android:description，服务用途说明栏为空",
    "多个承载页面（com.rmowa.wpamz.inject.uibwduIABuIaw、com.rmowa.wpamz.util.nidwoanAIOWDbwaiuBa、com.rmowa.wpamz.nawIODnaiowdna、com.rmowa.wpamz.util.AUInawiOBFA、com.rmowa.wpamz.util.uaiwdBuaiwbdaD、com.rmowa.wpamz.opnoPAWNDioaNDW）显式 android:label=\"\" 且 Theme.NoTitleBar，标题栏不呈现任何文字",
    "res/values/strings.xml 中 common_google_play_services_* 系列（Enable/Install/Update Google Play services 等）为 GMS 库标准资源，非应用自写诱导文案，不应视为引导页面",
    "真实引导弹窗/悬浮遮罩/WebView 教学页文字：位于 assets/giwj8II/gGpi8gfof1.hUf 加密载荷内，静态不可见；assets 目录下未发现引导用 html 文件"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "QR Code Scanner: Add-on Recognizer",
      "text_zh": "二维码扫描器：附加识别器",
      "source_location": "AndroidManifest.xml application@android:label",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't work unless you enable Google Play services.",
      "text_zh": "%1$s 需要启用 Google Play 服务才能正常工作。",
      "source_location": "res/values/strings.xml : common_google_play_services_enable_text（GMS 库标准资源）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't run without Google Play services, which are missing from your device.",
      "text_zh": "%1$s 无法运行，因为您的设备缺少 Google Play 服务。",
      "source_location": "res/values/strings.xml : common_google_play_services_install_text（GMS 库标准资源）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "%1$s won't run unless you update Google Play services.",
      "text_zh": "%1$s 需要更新 Google Play 服务才能运行。",
      "source_location": "res/values/strings.xml : common_google_play_services_update_text（GMS 库标准资源）",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "en",
      "text_verbatim": "（空字符串）",
      "text_zh": "无障碍服务标签与用途说明均为空",
      "source_location": "AndroidManifest.xml service@android:label 缺失；res/xml/asclllservizio.xml 无 android:description",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "（不可静态还原）",
      "text_zh": "真实引导文案位于加密二阶段载荷，无法逐字引用",
      "source_location": "assets/giwj8II/gGpi8gfof1.hUf（加密）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：可见 DEX 中不含任何无障碍/应用详情设置 action 常量，重跳与定时拉起逻辑在加密载荷内；Manifest 层面已具备 USER_PRESENT、BOOT_COMPLETED、QUICKBOOT_POWERON、PACKAGE_ADDED 广播接收器（priority 988）与 SYSTEM_ALERT_WINDOW、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 权限，具备后台重新拉起与常驻条件，但具体循环实现无法静态确认。",
    "overlay_or_fake_settings": "不可静态还原：已声明 SYSTEM_ALERT_WINDOW 悬浮窗权限，具备叠放引导遮罩/高仿开关页的能力，但未见实现代码与伪造布局资源；预筛 overlay=[] 亦未命中。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=28，未达 Android 13 受限设置门槛；包内亦无 APPLICATION_DETAILS_SETTINGS 相关字符串）",
    "post_grant_anti_removal": "不可静态还原：无障碍配置含 canPerformGestures 与 flagRetrieveInteractiveWindows，理论上可用于全局手势自点确认或干扰撤权，但无 performGlobalAction 调用点可见（可见 DEX 中出现 0 次），实现位于加密载荷内。",
    "benign_graceful_degradation": "无（无降级证据：无障碍服务无说明、无替代手动模式，且同时捆绑短信读写与全应用枚举权限，不具备良性透明说明特征）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以冷启动为起点：在 ActivityThread 反射替换完成后、首个 com.rmowa.wpamz.WNiudwabNUDIba 或任一空标签 Activity（util.nidwoanAIOWDbwaiuBa / nawIODnaiowdna / util.AUInawiOBFA / util.uaiwdBuaiwbdaD / inject.uibwduIABuIaw）压栈的瞬间抓取；同时 Hook Context.startActivity 中 intent action 为 android.settings.ACCESSIBILITY_SETTINGS 或 android.settings.APPLICATION_DETAILS_SETTINGS 的调用，在跳转前 800ms 与返回后 onResume 各抓一帧。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/首屏承载页（空标签、无标题 Activity）",
        "page_identifier": "Activity 名 com.rmowa.wpamz.WNiudwabNUDIba 或 util.nidwoanAIOWDbwaiuBa / nawIODnaiowdna / util.AUInawiOBFA，界面无标题栏、无 actionBar 文字",
        "why_most_useful": "这是加密载荷解密后第一个可控界面，是判定“功能触发即弹引导”还是“伪装成二维码扫描器”的分水岭",
        "observable_utg_signals": ["页面文本全部为 QR 扫描相关 vs 直接出现无障碍授权话术", "是否存在不可取消（无返回/无跳过按钮）的弹窗", "是否出现“启用服务/授权/辅助功能”等关键词"]
      },
      {
        "page_role": "跳转前引导弹窗或教学页",
        "page_identifier": "Dialog 或 WebView，文案含 accessibility / service / enable / 辅助功能 等关键词",
        "why_most_useful": "直接决定诱导话术类型（假更新、故障恐吓、清理伪装或教唆忽视警告）与载体（原生/本地 HTML/远端 URL）",
        "observable_utg_signals": ["弹窗按钮集合（是否有取消/稍后）", "WebView URL 域名（本地 file:// 还是远端）", "文案是否要求忽略系统安全警告"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility 中条目名称为 “QR Code Scanner: Add-on Recognizer”，说明栏为空",
        "why_most_useful": "确认服务在系统列表中的实际展示名与空说明，是身份伪装与警告缺位的直接证据",
        "observable_utg_signals": ["条目名称是否与应用名一致（无独立服务名）", "服务描述是否为空", "是否存在空白/换行挤出的条目"]
      },
      {
        "page_role": "系统设置返回后的遮罩/悬浮引导页",
        "page_identifier": "SYSTEM_ALERT_WINDOW 悬浮窗或重新压栈的无标题 Activity",
        "why_most_useful": "判定是否存在拒绝即重跳的死循环或叠层指引（UTG 可直接看到设置页上叠加的另一层窗口）",
        "observable_utg_signals": ["返回设置页后是否 1-3 秒内再次跳转 ACCESSIBILITY_SETTINGS", "是否存在半透明遮罩与手指引导动画", "悬浮窗是否覆盖系统开关位置"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：真实代码全部位于 assets/giwj8II/gGpi8gfof1.hUf 的加密二阶段载荷，静态无法还原跳转点与文案，因此 UTG 必须以运行期为唯一取证途径；此外服务与多个 Activity 的 android:label=\"\" 与无障碍 description 缺失，会使系统列表与页面标题呈现空白，纯文本抓取可能得到空串，需依赖组件名与窗口层级判定；GMS 库标准 common_google_play_services_* 字符串存在被误判为诱导文案的风险，需排除。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "LURE_UTILITY_CLEANER_DISGUISE"
  ],
  "code_anchors": [
    "com.caffe.cociss.k#a()",
    "com.caffe.cociss.k#a(int)",
    "com.caffe.cociss.k#onCreate",
    "res/xml/asclllservizio.xml",
    "AndroidManifest.xml: service com.rmowa.wpamz.UIDNwaidobaWIODb",
    "assets/giwj8II/gGpi8gfof1.hUf"
  ]
}
```

</details>
