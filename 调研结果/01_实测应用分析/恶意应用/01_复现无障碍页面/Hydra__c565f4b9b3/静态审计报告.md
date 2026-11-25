# MB_055__c565f4b9b3｜Hydra — Chrome

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：129.3s

## 1. 一句话核心结论

- **核心申请方式**：以“Chrome”为名的 DexProtector 加密加载型木马，真实逻辑藏于加密 DEX，仅能从 Manifest 确认其挂载无任何说明文字的无障碍服务、全屏悬浮窗、通知监听、设备管理器与 SOCKS5/录屏组件，并在运行期通过引导文案把用户推向无障碍授权。
- **静态可见性说明**：APK 由 DexProtector 加固：ProxyApplication 在 attachBaseContext 中调用 DexProtect.install，将 dp/a.a（987KB）经 DexCrypto.exfr 的 nDnv/FxIjsF keystream 异或后再 Inflate 解密为真实 DEX 并动态加载，全部字符串常量再经 DexCrypto.ab（XOR key 'qtfreet'）还原。明文 classes.dex 仅含壳与反射装载代码，无障碍引导文案、ACTION_ACCESSIBILITY_SETTINGS 跳转点、悬浮遮罩叠层逻辑均位于加密载荷内，本次未解密，故运行期 UTG 页面流转无法静态还原；Manifest 组件、无障碍配置 XML 与外壳常量可完整静态确认。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_FAKE_SETTINGS_SCREEN`（高仿系统无障碍设置列表/假开关页）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_DISMISS_SYSTEM_WARNING`（显式教唆忽略/接受系统隐私与安全警告）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `c565f4b9b3c6bb095c6ce62ab02c5cc8a84502231f4facdddb6f3d7af2321b5e` |
| 包名 / 年份 | `com.grand.thinpad` / 2024 |
| 家族 / 品类 | **Hydra**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Chrome |
| 引导页宣称品牌/身份 | Google Chrome 浏览器 / “Portal”服务 / “Security update”安全更新 |
| 系统无障碍列表服务名 | 无（InjAccessibilityService 配置 res/Qs.xml 未声明 android:label，系统列表中以包名/类名占位显示，且无 android:description） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 应用标签直接冒用 Chrome；2) MainActivity 与 MainActivity2 各自挂同名 activity-alias（MainActivity2 的 alias enabled=false、带独立 label/icon），可运行期切换名称图标；3) LockerActivity 使用 label='Settings'、系统设置主题且带 CATEGORY_HOME，伪装系统设置/桌面；4) 无障碍服务配置刻意省略 label 与 description，不向用户暴露用途；5) 全部字符串以十六进制+XOR('qtfreet') 编码存放，DEX 本体为加密载荷，dexpro-build.properties 带 'Modded by 👽🅐︎🅝︎🅘︎🅚︎555' 构建者标记。 |
| 无障碍服务类名 | `com.grand.snail.bot.components.injects.system.InjAccessibilityService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | xyz.magicph.dexpro.ProxyApplication（无 Launcher 界面的壳 Application）→ 动态加载的真实 Application | 进程创建时 attachBaseContext → DexProtect.install → loadDex；随后 onCreate 反射 bindRealApplication 替换真实 Application | 不可静态还原 | 无 | 无（自动执行） | `xyz.magicph.dexpro.ProxyApplication.attachBaseContext / onCreate；android.support.dexpro.utils.DexProtect.install；dp/a.a（加密载荷）` |
| 2 | 引导说明页 | com.grand.snail.bot.PermissionsActivity（Manifest 声明，excludeFromRecents，无 LAUNCHER filter）及/或 MainActivity 内引导弹窗 | 真实逻辑在解密 DEX 中，触发条件（冷启动即弹 / 功能触发）不可静态还原 | 不可静态还原 | **原文**：In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below: / Please enable Portal service under Accessibility settings<br>**译注**：为了让 %s 的最新版本正常工作，你需要开启无障碍权限，请按以下步骤操作： / 请在“无障碍”设置中启用 Portal 服务 | 按分步指引前往系统无障碍设置（是否存在取消/跳过按钮不可静态确认） | `com.grand.snail.bot.PermissionsActivity（Manifest）；文案位于加密载荷 dp/a.a（预筛提取，明文 DEX 中不存在）` |
| 3 | 跳受限设置 | 系统“电池优化/安装未知应用/应用详情”页（对应权限 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、REQUEST_INSTALL_PACKAGES、WRITE_SETTINGS） | 不可静态还原（跳转 Intent 在加密 DEX 内） | 不可静态还原 | **原文**：Enable control over your battery usage. Press 'Activate' button in the next window / To install Security update you must disable 'Scan device' option!<br>**译注**：启用对电池使用的控制，在下一个窗口点击“激活”按钮 / 要安装安全更新，你必须关闭“扫描设备”选项！ | 在系统弹窗中点击“激活”/关闭系统安全扫描（教唆关闭安全防护） | `Manifest 权限声明（REQUEST_IGNORE_BATTERY_OPTIMIZATIONS / REQUEST_INSTALL_PACKAGES）；跳转点位于 dp/a.a` |
| 4 | 跳无障碍设置 | 系统设置 → 无障碍 → 已安装服务（com.grand.thinpad 下的 InjAccessibilityService，无 label/无 description） | 不可静态还原（预期为 ACTION_ACCESSIBILITY_SETTINGS 跳转，代码在加密 DEX） | 系统无障碍页 | **原文**：Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Check in 'Downloaded Services' list: %s<br>**译注**：第1步 打开“设置” / 第2步 打开“无障碍” / 第3步 打开“已安装的服务” / 在“已下载的服务”列表中查找：%s | 手动进入无障碍列表并打开开关（服务本身无说明文字，用户无法判断用途） | `com.grand.snail.bot.components.injects.system.InjAccessibilityService；res/Qs.xml（accessibility-service 配置）` |
| 5 | 遮罩叠层指引 | com.grand.snail.bot.components.injects.system.FullscreenOverlayService（配合 SYSTEM_ALERT_WINDOW） | 不可静态还原（何时起窗、是否盖在系统设置页上由加密 DEX 决定） | 悬浮窗Overlay | **原文**：Go to settings / Google - do not disable this app<br>**译注**：前往设置 / Google —— 请勿停用此应用 | 按悬浮指引继续操作，并忽略/不要停用该应用（含冒充 Google 的告警） | `com.grand.snail.bot.components.injects.system.FullscreenOverlayService（Manifest）；文案在 dp/a.a` |
| 6 | 拒权反馈循环 | 不可静态还原（预期为 onResume/定时器重新拉起引导） | 不可静态还原 | 不可静态还原 | 无 | 不可静态确认（是否强制不返回无法判定） | `不可静态还原（逻辑位于加密载荷 dp/a.a）` |
| 7 | 获权后动作 | InjAccessibilityService（canRetrieveWindowContent + canPerformGestures + canRequestFilterKeyEvents）；LockerActivity（CATEGORY_HOME 伪装桌面/Settings）；HelperAdmin$MyHomeReceiver（设备管理器）；NLService（通知监听）；Socks5ProxyService；ScreencastService（MediaProjection） | 无障碍服务 onServiceConnected 后按远程指令执行（指令通道在加密 DEX，不可静态还原） | 不可静态还原 | 无 | 无 | `com.grand.snail.bot.components.injects.system.InjAccessibilityService；com.grand.snail.bot.components.locker.LockerActivity；com.grand.snail.bot.HelperAdmin$MyHomeReceiver；com.grand.snail.bot.components.socks5.Socks5ProxyService` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 加密 DEX 载荷 dp/a.a（由 ProxyApplication.attachBaseContext → DexProtect.install → DexCrypto.decrypt 在运行期解密并动态加载），预筛文案（Portal service / Step 1-3 / Security update / battery usage / do not disable this app）全部只存在于此，明文 classes.dex 与 resources.arsc 中均检索不到
- Manifest 应用标签 android:label="Chrome"（桌面图标与系统应用列表显示名，冒充 Chrome）
- Manifest 通知监听服务 android:label="Chrome"（com.grand.snail.bot.components.commands.NLService）
- Manifest LockerActivity：android:label="Settings"、theme=@android:01030007（系统设置样式）、含 CATEGORY_HOME，用于伪装系统设置/桌面页
- 无障碍服务配置 res/Qs.xml（accessibility-service）：无 android:label、无 android:description，系统“已安装服务”列表中该项对用户零说明
- com.grand.snail.bot.PermissionsActivity（Manifest 声明、excludeFromRecents、无 launcher filter）：预期承载权限引导说明页，具体 UI 由加密载荷决定
- FullscreenOverlayService + SYSTEM_ALERT_WINDOW：预期在设置页之上叠放引导/告警悬浮窗，文案在加密载荷内

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below: | 为了让 %s 的最新版本正常工作，你需要开启无障碍权限。请按以下步骤操作： | `加密载荷 dp/a.a（预筛提取；明文 classes.dex 中不存在）` | 假更新 |
| en | Please enable Portal service under Accessibility settings | 请在“无障碍”设置中启用 Portal 服务 | `加密载荷 dp/a.a（预筛提取）` | 假更新 |
| en | Step 1 - Go to “Settings”<br>Step 2 - Open “Accessibility”<br>Step 3 - Open “Installed Services” | 第1步 打开“设置”；第2步 打开“无障碍”；第3步 打开“已安装的服务” | `加密载荷 dp/a.a（预筛提取）` | 受限设置分步教学 |
| en | Check in 'Downloaded Services' list: %s | 在“已下载的服务”列表中查找：%s | `加密载荷 dp/a.a（预筛提取）` | 受限设置分步教学 |
| en | Google - do not disable this app | Google —— 请勿停用此应用 | `加密载荷 dp/a.a（预筛提取）` | 教唆忽视警告 |
| en | To install Security update you must disable 'Scan device' option! | 要安装安全更新，你必须关闭“扫描设备”选项！ | `加密载荷 dp/a.a（预筛提取）` | 教唆忽视警告 |
| en | Enable control over your battery usage. Press 'Activate' button in the next window | 启用对电池使用的控制。在下一个窗口点击“激活”按钮 | `加密载荷 dp/a.a（预筛提取）` | 故障恐吓 |
| en | Go to settings | 前往设置 | `加密载荷 dp/a.a（预筛提取）` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导与重跳逻辑位于 DexProtector 加密载荷 dp/a.a，明文 DEX 仅见壳的 attachBaseContext/install 与 PermissionsActivity 声明，无法确认是否 onResume 死循环重跳或定时器拉起
- **遮罩叠层 / 高仿系统设置页**：Manifest 确证具备叠层能力：FullscreenOverlayService + SYSTEM_ALERT_WINDOW；另有 LockerActivity（label=Settings、系统设置主题、CATEGORY_HOME）可充当高仿设置/桌面页，但具体是否覆盖在无障碍设置页之上、叠层时机由加密载荷决定，静态不可见
- **Android 13+ 受限设置（Restricted Settings）应对**：存在教唆关闭系统防护的文案（“To install Security update you must disable 'Scan device' option!”）与电池优化激活引导（REQUEST_IGNORE_BATTERY_OPTIMIZATIONS）；未发现针对 Android 13+ 受限设置右上角菜单的明确分步文案（该部分可能在加密载荷内）
- **获权后即时行为与防撤权机制**：不可静态确认：具备实现手段（无障碍 canPerformGestures/canRequestFilterKeyEvents、设备管理器 HelperAdmin$MyHomeReceiver、LockerActivity 劫持 HOME），但自点确认/阻止撤权的具体代码在加密载荷内
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以进程启动为起点（包名 com.grand.thinpad，Application=xyz.magicph.dexpro.ProxyApplication），在解密载荷装载完成后立即开始 UTG 采样；最佳抓取瞬间为首次出现 PermissionsActivity 或任何跳转 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 的时刻，以及无障碍服务开启返回后的 1–2 秒（可能叠层或重跳）。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区在静态侧：真实引导逻辑与跳转代码位于 DexProtector 加密载荷 dp/a.a，静态不可还原，必须依赖运行期 UTG；另需注意应用具备 activity-alias 改名换图标（MainActivity2 alias enabled=false）与 label=Settings 的 LockerActivity 伪装能力，UTG 应按 package 而非按界面标题匹配，避免被“Settings/Chrome”标题误导。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/首次权限引导页** | com.grand.snail.bot.PermissionsActivity 或 MainActivity 上弹出的引导对话框，含“Portal service”“latest version of %s”等文案 | 这是唯一能把“正常 Chrome 界面”与“诱导无障碍”连接起来的第一现场，可直接证明文案与按钮形态（是否可取消） | 界面文案含 accessibility / Portal service / Step 1-3；按钮仅为“前往设置/下一步”，无取消或跳过；页面所属 Activity 为 com.grand.snail.bot.PermissionsActivity 而非浏览器界面 |
| **跳转无障碍设置后的系统无障碍列表项** | 设置→无障碍→已安装服务中 com.grand.thinpad 条目（InjAccessibilityService，无说明文字） | 验证服务在系统列表中是否真的空白无 description/label，以及是否有悬浮遮罩盖在其上 | 服务条目文本仅为应用名/类名，无用途说明；无障碍开关节点与 package=com.grand.thinpad 的关联；条目上方是否存在非系统窗口层（悬浮窗） |
| **设置页上方的悬浮引导/告警遮罩** | FullscreenOverlayService 创建的悬浮窗，含“Go to settings”“Google - do not disable this app”文案 | 确认是否采用叠层遮罩与品牌冒充施压，是区分“分步教学”与“强制诱导”的关键 | TYPE_APPLICATION_OVERLAY 窗口归属 com.grand.thinpad；遮罩文案与系统设置页同时可见；遮罩无关闭按钮 |
| **授权后返回/撤权尝试时的反应页** | 从无障碍设置返回后立刻出现的页面（可能为 LockerActivity 伪装 Settings 页或再次弹出的引导页） | 判断是否存在拒权循环与反撤权行为 | 返回后短时间内同一引导页重复出现（时间戳间隔）；HOME 意图被 com.grand.snail.bot.components.locker.LockerActivity 接管；无障碍开关被自动切回开启 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `xyz.magicph.dexpro.ProxyApplication.attachBaseContext / bindRealApplication（反射替换真实 Application，加载加密 DEX）`
- `android.support.dexpro.utils.DexProtect.install（dp/a.a → DexCrypto.decrypt → loadDex）`
- `android.support.dexpro.utils.DexCrypto.exfr / nDnv / ab（载荷与字符串解密算法）`
- `com.grand.snail.bot.components.injects.system.InjAccessibilityService（meta-data @7F090002 → res/Qs.xml，无 label/description）`
- `com.grand.snail.bot.components.injects.system.FullscreenOverlayService（SYSTEM_ALERT_WINDOW 叠层能力）`
- `com.grand.snail.bot.components.locker.LockerActivity（label=Settings、CATEGORY_HOME 伪装）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**静态可见性受限：真实逻辑整体位于加密载荷内，UTG 页面流转无法静态还原。**

**1. 加壳事实（已确证）**
- Application 为 [ProxyApplication](<resource-unit:#1.dex1 code:xyz.magicph.dexpro.ProxyApplication>)，其 `attachBaseContext` 读取 meta-data（`protectKey`/`secData`/`realApp`/`dexes`）后调用 `DexProtect.install`；`onCreate` 用反射把真实 Application 换入（`bindRealApplication`）。
- 解密链为 [DexProtect.install](<resource-unit:#1.dex1 code:android.support.dexpro.utils.DexProtect#install>) → `copyAssets` → [DexCrypto.decrypt](<resource-unit:#1.dex1 code:android.support.dexpro.utils.DexCrypto#decrypt>)（[exfr](<resource-unit:#1.dex1 code:android.support.dexpro.utils.DexCrypto#exfr>) 的 keystream 由 [nDnv](<resource-unit:#1.dex1 code:android.support.dexpro.utils.DexCrypto#nDnv>)/`FxIjsF` 生成，再做 `InflaterOutputStream` 解压），字符串常量统一经 [DexCrypto.ab](<resource-unit:#1.dex1 code:android.support.dexpro.utils.DexCrypto#ab>)（XOR key `qtfreet`）还原。
- 载荷位置：`dp/a.a`（987 KB）经 `install` 中以 `ab("150449")`=`dp/`、`ab("105A07")`=`a.a` 拼出；`assets/classes.dex.dat` 仅 37 字节为占位。[dexpro-build.properties](<resource-unit:#1 file:dexpro-build.properties>) 注明 DexProtector 2024-03-04 构建且被“Modded by 👽🅐︎🅝︎🅘︎🅚︎555”。
- 结果：`classes.dex`（62 KB）内仅含壳代码，预筛的全部引导文案（“Please enable Portal service under Accessibility settings”“Step 1 - Go to Settings”…）在明文 DEX 中**搜索不到**，只存在于加密的 `dp/a.a` 内。

**2. 仍可从 Manifest/资源确证的无障碍诱导相关面**
- 服务：[InjAccessibilityService](<resource-unit:#1 manifest:components>)（`BIND_ACCESSIBILITY_SERVICE`，meta-data `@7F090002`）；其配置 XML（[res/Qs.xml](<resource-unit:#1 file:res/Qs.xml>) 含 `settingsActivity`、`canRetrieveWindowContent`、`canPerformGestures`、`canRequestFilterKeyEvents`）**无 `android:description`、无 label**，与预筛 `服务标签=[]`、`description=[]` 一致——即系统无障碍列表中该项对用户无任何用途说明。
- 配套滥用组件：`FullscreenOverlayService`（+`SYSTEM_ALERT_WINDOW`）、`NLService`（通知监听，label 亦为 `Chrome`）、`Socks5ProxyService`、`ScreencastService`（MediaProjection）、`HelperAdmin$MyHomeReceiver`（设备管理器）。
- 伪装/变脸面：`application@label="Chrome"`；`LockerActivity` 主题为 `@android:01030007`、label `Settings`、带 `CATEGORY_HOME`（伪装桌面/设置页，`enabled=false` 备用）；`MainActivity`/`MainActivity2` 各自挂同名 `activity-alias`（第二个 alias `enabled=false`、独立 label/icon），可运行期切换图标与名称。

**3. 未决/覆盖边界**
- 引导弹窗、`ACTION_ACCESSIBILITY_SETTINGS` 跳转点、悬浮遮罩叠层、拒权循环、获权后 `GLOBAL_ACTION_BACK` 阻止撤权等运行期流转，全部在解密后的真实 DEX 中，本次未解密，故 `step_by_step_flow` 仅能给出组件级（Manifest）步骤并标注不可静态还原。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "APK 由 DexProtector 加固：ProxyApplication 在 attachBaseContext 中调用 DexProtect.install，将 dp/a.a（987KB）经 DexCrypto.exfr 的 nDnv/FxIjsF keystream 异或后再 Inflate 解密为真实 DEX 并动态加载，全部字符串常量再经 DexCrypto.ab（XOR key 'qtfreet'）还原。明文 classes.dex 仅含壳与反射装载代码，无障碍引导文案、ACTION_ACCESSIBILITY_SETTINGS 跳转点、悬浮遮罩叠层逻辑均位于加密载荷内，本次未解密，故运行期 UTG 页面流转无法静态还原；Manifest 组件、无障碍配置 XML 与外壳常量可完整静态确认。",
  "summary_one_liner": "以“Chrome”为名的 DexProtector 加密加载型木马，真实逻辑藏于加密 DEX，仅能从 Manifest 确认其挂载无任何说明文字的无障碍服务、全屏悬浮窗、通知监听、设备管理器与 SOCKS5/录屏组件，并在运行期通过引导文案把用户推向无障碍授权。",
  "disguise_identity": {
    "app_display_name": "Chrome",
    "claimed_brand_or_persona": "Google Chrome 浏览器 / “Portal”服务 / “Security update”安全更新",
    "a11y_service_label": "无（InjAccessibilityService 配置 res/Qs.xml 未声明 android:label，系统列表中以包名/类名占位显示，且无 android:description）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 应用标签直接冒用 Chrome；2) MainActivity 与 MainActivity2 各自挂同名 activity-alias（MainActivity2 的 alias enabled=false、带独立 label/icon），可运行期切换名称图标；3) LockerActivity 使用 label='Settings'、系统设置主题且带 CATEGORY_HOME，伪装系统设置/桌面；4) 无障碍服务配置刻意省略 label 与 description，不向用户暴露用途；5) 全部字符串以十六进制+XOR('qtfreet') 编码存放，DEX 本体为加密载荷，dexpro-build.properties 带 'Modded by 👽🅐︎🅝︎🅘︎🅚︎555' 构建者标记。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "xyz.magicph.dexpro.ProxyApplication（无 Launcher 界面的壳 Application）→ 动态加载的真实 Application",
      "trigger_event": "进程创建时 attachBaseContext → DexProtect.install → loadDex；随后 onCreate 反射 bindRealApplication 替换真实 Application",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "壳层无任何界面；若解密失败仅 Toast 抛出异常信息（Toast.makeText(context, th.getMessage(), 1)）",
      "user_action_requested": "无（自动执行）",
      "code_anchor": "xyz.magicph.dexpro.ProxyApplication.attachBaseContext / onCreate；android.support.dexpro.utils.DexProtect.install；dp/a.a（加密载荷）"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.grand.snail.bot.PermissionsActivity（Manifest 声明，excludeFromRecents，无 LAUNCHER filter）及/或 MainActivity 内引导弹窗",
      "trigger_event": "真实逻辑在解密 DEX 中，触发条件（冷启动即弹 / 功能触发）不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below: / Please enable Portal service under Accessibility settings",
      "shown_text_zh": "为了让 %s 的最新版本正常工作，你需要开启无障碍权限，请按以下步骤操作： / 请在“无障碍”设置中启用 Portal 服务",
      "user_action_requested": "按分步指引前往系统无障碍设置（是否存在取消/跳过按钮不可静态确认）",
      "code_anchor": "com.grand.snail.bot.PermissionsActivity（Manifest）；文案位于加密载荷 dp/a.a（预筛提取，明文 DEX 中不存在）"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统“电池优化/安装未知应用/应用详情”页（对应权限 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、REQUEST_INSTALL_PACKAGES、WRITE_SETTINGS）",
      "trigger_event": "不可静态还原（跳转 Intent 在加密 DEX 内）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "Enable control over your battery usage. Press 'Activate' button in the next window / To install Security update you must disable 'Scan device' option!",
      "shown_text_zh": "启用对电池使用的控制，在下一个窗口点击“激活”按钮 / 要安装安全更新，你必须关闭“扫描设备”选项！",
      "user_action_requested": "在系统弹窗中点击“激活”/关闭系统安全扫描（教唆关闭安全防护）",
      "code_anchor": "Manifest 权限声明（REQUEST_IGNORE_BATTERY_OPTIMIZATIONS / REQUEST_INSTALL_PACKAGES）；跳转点位于 dp/a.a"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已安装服务（com.grand.thinpad 下的 InjAccessibilityService，无 label/无 description）",
      "trigger_event": "不可静态还原（预期为 ACTION_ACCESSIBILITY_SETTINGS 跳转，代码在加密 DEX）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Step 1 - Go to “Settings” / Step 2 - Open “Accessibility” / Step 3 - Open “Installed Services” / Check in 'Downloaded Services' list: %s",
      "shown_text_zh": "第1步 打开“设置” / 第2步 打开“无障碍” / 第3步 打开“已安装的服务” / 在“已下载的服务”列表中查找：%s",
      "user_action_requested": "手动进入无障碍列表并打开开关（服务本身无说明文字，用户无法判断用途）",
      "code_anchor": "com.grand.snail.bot.components.injects.system.InjAccessibilityService；res/Qs.xml（accessibility-service 配置）"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.grand.snail.bot.components.injects.system.FullscreenOverlayService（配合 SYSTEM_ALERT_WINDOW）",
      "trigger_event": "不可静态还原（何时起窗、是否盖在系统设置页上由加密 DEX 决定）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Go to settings / Google - do not disable this app",
      "shown_text_zh": "前往设置 / Google —— 请勿停用此应用",
      "user_action_requested": "按悬浮指引继续操作，并忽略/不要停用该应用（含冒充 Google 的告警）",
      "code_anchor": "com.grand.snail.bot.components.injects.system.FullscreenOverlayService（Manifest）；文案在 dp/a.a"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "不可静态还原（预期为 onResume/定时器重新拉起引导）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无",
      "user_action_requested": "不可静态确认（是否强制不返回无法判定）",
      "code_anchor": "不可静态还原（逻辑位于加密载荷 dp/a.a）"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "InjAccessibilityService（canRetrieveWindowContent + canPerformGestures + canRequestFilterKeyEvents）；LockerActivity（CATEGORY_HOME 伪装桌面/Settings）；HelperAdmin$MyHomeReceiver（设备管理器）；NLService（通知监听）；Socks5ProxyService；ScreencastService（MediaProjection）",
      "trigger_event": "无障碍服务 onServiceConnected 后按远程指令执行（指令通道在加密 DEX，不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（组件能力已在 Manifest 确证：读取窗口内容、执行手势、过滤按键、劫持 HOME、设备管理、通知监听、SOCKS5 代理、录屏）",
      "user_action_requested": "无",
      "code_anchor": "com.grand.snail.bot.components.injects.system.InjAccessibilityService；com.grand.snail.bot.components.locker.LockerActivity；com.grand.snail.bot.HelperAdmin$MyHomeReceiver；com.grand.snail.bot.components.socks5.Socks5ProxyService"
    }
  ],
  "text_presentation_locations": [
    "加密 DEX 载荷 dp/a.a（由 ProxyApplication.attachBaseContext → DexProtect.install → DexCrypto.decrypt 在运行期解密并动态加载），预筛文案（Portal service / Step 1-3 / Security update / battery usage / do not disable this app）全部只存在于此，明文 classes.dex 与 resources.arsc 中均检索不到",
    "Manifest 应用标签 android:label=\"Chrome\"（桌面图标与系统应用列表显示名，冒充 Chrome）",
    "Manifest 通知监听服务 android:label=\"Chrome\"（com.grand.snail.bot.components.commands.NLService）",
    "Manifest LockerActivity：android:label=\"Settings\"、theme=@android:01030007（系统设置样式）、含 CATEGORY_HOME，用于伪装系统设置/桌面页",
    "无障碍服务配置 res/Qs.xml（accessibility-service）：无 android:label、无 android:description，系统“已安装服务”列表中该项对用户零说明",
    "com.grand.snail.bot.PermissionsActivity（Manifest 声明、excludeFromRecents、无 launcher filter）：预期承载权限引导说明页，具体 UI 由加密载荷决定",
    "FullscreenOverlayService + SYSTEM_ALERT_WINDOW：预期在设置页之上叠放引导/告警悬浮窗，文案在加密载荷内"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "In order for the latest version of %s to work, you will need to enable accessibility. Please follow the steps below:",
      "text_zh": "为了让 %s 的最新版本正常工作，你需要开启无障碍权限。请按以下步骤操作：",
      "source_location": "加密载荷 dp/a.a（预筛提取；明文 classes.dex 中不存在）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Please enable Portal service under Accessibility settings",
      "text_zh": "请在“无障碍”设置中启用 Portal 服务",
      "source_location": "加密载荷 dp/a.a（预筛提取）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Step 1 - Go to “Settings”\nStep 2 - Open “Accessibility”\nStep 3 - Open “Installed Services”",
      "text_zh": "第1步 打开“设置”；第2步 打开“无障碍”；第3步 打开“已安装的服务”",
      "source_location": "加密载荷 dp/a.a（预筛提取）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Check in 'Downloaded Services' list: %s",
      "text_zh": "在“已下载的服务”列表中查找：%s",
      "source_location": "加密载荷 dp/a.a（预筛提取）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Google - do not disable this app",
      "text_zh": "Google —— 请勿停用此应用",
      "source_location": "加密载荷 dp/a.a（预筛提取）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "To install Security update you must disable 'Scan device' option!",
      "text_zh": "要安装安全更新，你必须关闭“扫描设备”选项！",
      "source_location": "加密载荷 dp/a.a（预筛提取）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable control over your battery usage. Press 'Activate' button in the next window",
      "text_zh": "启用对电池使用的控制。在下一个窗口点击“激活”按钮",
      "source_location": "加密载荷 dp/a.a（预筛提取）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "en",
      "text_verbatim": "Go to settings",
      "text_zh": "前往设置",
      "source_location": "加密载荷 dp/a.a（预筛提取）",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导与重跳逻辑位于 DexProtector 加密载荷 dp/a.a，明文 DEX 仅见壳的 attachBaseContext/install 与 PermissionsActivity 声明，无法确认是否 onResume 死循环重跳或定时器拉起",
    "overlay_or_fake_settings": "Manifest 确证具备叠层能力：FullscreenOverlayService + SYSTEM_ALERT_WINDOW；另有 LockerActivity（label=Settings、系统设置主题、CATEGORY_HOME）可充当高仿设置/桌面页，但具体是否覆盖在无障碍设置页之上、叠层时机由加密载荷决定，静态不可见",
    "restricted_settings_13plus_coaching": "存在教唆关闭系统防护的文案（“To install Security update you must disable 'Scan device' option!”）与电池优化激活引导（REQUEST_IGNORE_BATTERY_OPTIMIZATIONS）；未发现针对 Android 13+ 受限设置右上角菜单的明确分步文案（该部分可能在加密载荷内）",
    "post_grant_anti_removal": "不可静态确认：具备实现手段（无障碍 canPerformGestures/canRequestFilterKeyEvents、设备管理器 HelperAdmin$MyHomeReceiver、LockerActivity 劫持 HOME），但自点确认/阻止撤权的具体代码在加密载荷内",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以进程启动为起点（包名 com.grand.thinpad，Application=xyz.magicph.dexpro.ProxyApplication），在解密载荷装载完成后立即开始 UTG 采样；最佳抓取瞬间为首次出现 PermissionsActivity 或任何跳转 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 的时刻，以及无障碍服务开启返回后的 1–2 秒（可能叠层或重跳）。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/首次权限引导页",
        "page_identifier": "com.grand.snail.bot.PermissionsActivity 或 MainActivity 上弹出的引导对话框，含“Portal service”“latest version of %s”等文案",
        "why_most_useful": "这是唯一能把“正常 Chrome 界面”与“诱导无障碍”连接起来的第一现场，可直接证明文案与按钮形态（是否可取消）",
        "observable_utg_signals": ["界面文案含 accessibility / Portal service / Step 1-3", "按钮仅为“前往设置/下一步”，无取消或跳过", "页面所属 Activity 为 com.grand.snail.bot.PermissionsActivity 而非浏览器界面"]
      },
      {
        "page_role": "跳转无障碍设置后的系统无障碍列表项",
        "page_identifier": "设置→无障碍→已安装服务中 com.grand.thinpad 条目（InjAccessibilityService，无说明文字）",
        "why_most_useful": "验证服务在系统列表中是否真的空白无 description/label，以及是否有悬浮遮罩盖在其上",
        "observable_utg_signals": ["服务条目文本仅为应用名/类名，无用途说明", "无障碍开关节点与 package=com.grand.thinpad 的关联", "条目上方是否存在非系统窗口层（悬浮窗）"]
      },
      {
        "page_role": "设置页上方的悬浮引导/告警遮罩",
        "page_identifier": "FullscreenOverlayService 创建的悬浮窗，含“Go to settings”“Google - do not disable this app”文案",
        "why_most_useful": "确认是否采用叠层遮罩与品牌冒充施压，是区分“分步教学”与“强制诱导”的关键",
        "observable_utg_signals": ["TYPE_APPLICATION_OVERLAY 窗口归属 com.grand.thinpad", "遮罩文案与系统设置页同时可见", "遮罩无关闭按钮"]
      },
      {
        "page_role": "授权后返回/撤权尝试时的反应页",
        "page_identifier": "从无障碍设置返回后立刻出现的页面（可能为 LockerActivity 伪装 Settings 页或再次弹出的引导页）",
        "why_most_useful": "判断是否存在拒权循环与反撤权行为",
        "observable_utg_signals": ["返回后短时间内同一引导页重复出现（时间戳间隔）", "HOME 意图被 com.grand.snail.bot.components.locker.LockerActivity 接管", "无障碍开关被自动切回开启"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区在静态侧：真实引导逻辑与跳转代码位于 DexProtector 加密载荷 dp/a.a，静态不可还原，必须依赖运行期 UTG；另需注意应用具备 activity-alias 改名换图标（MainActivity2 alias enabled=false）与 label=Settings 的 LockerActivity 伪装能力，UTG 应按 package 而非按界面标题匹配，避免被“Settings/Chrome”标题误导。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_FAKE_SETTINGS_SCREEN",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_DISMISS_SYSTEM_WARNING",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "xyz.magicph.dexpro.ProxyApplication.attachBaseContext / bindRealApplication（反射替换真实 Application，加载加密 DEX）",
    "android.support.dexpro.utils.DexProtect.install（dp/a.a → DexCrypto.decrypt → loadDex）",
    "android.support.dexpro.utils.DexCrypto.exfr / nDnv / ab（载荷与字符串解密算法）",
    "com.grand.snail.bot.components.injects.system.InjAccessibilityService（meta-data @7F090002 → res/Qs.xml，无 label/description）",
    "com.grand.snail.bot.components.injects.system.FullscreenOverlayService（SYSTEM_ALERT_WINDOW 叠层能力）",
    "com.grand.snail.bot.components.locker.LockerActivity（label=Settings、CATEGORY_HOME 伪装）"
  ]
}
```

</details>
