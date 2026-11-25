# MR_026__7c2edd8277｜Hqwar — Google Play Service

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：160.4s

## 1. 一句话核心结论

- **核心申请方式**：以「Google Play Service」桌面名和「Google Play Protect」无障碍服务名伪造官方身份，无障碍配置 description 留空、settingsActivity 为无关示例路径，真实引导与无障碍执行体整体移入 AES 类加密载荷 include/monthly.b32，运行期才解密加载。
- **静态可见性说明**：Manifest 声明、无障碍 XML 配置、权限集与 Application 入口完整可见；但 IFBInWN 无障碍服务类本体、全部引导 UI 与跳转逻辑均不在 classes.dex（全文检索 AccessibilityService/DexClassLoader/getAssets/ACCESSIBILITY 设置 action 零命中），包内 16 个 layout 全为空壳根节点、无 strings.xml、无 assets/HTML。真实行为藏于 unknown/include/monthly.b32（188346 字节高熵密文，长度前缀 188342），由 Application.onCreate 经 last.b16 指针加载；单字节 XOR 256 键、两把 41 字节混淆串 XOR、AES-128/256 ECB/CBC、裸 zlib 试解均未得到 dex/PK/gzip 头，解密算法静态不可还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `7c2edd827709df4a5fef45c0b6556f0ade1ebfb120869e20ada7e707509a2df6` |
| 包名 / 年份 | `com.fqaqkdwn.uhkshvhv` / 2019 |
| 家族 / 品类 | **Hqwar**（同池样本数：4） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | Google Play Service |
| 引导页宣称品牌/身份 | Google Play Service / Google Play Protect（Google 官方 GMS 品牌） |
| 系统无障碍列表服务名 | Google Play Protect |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 android:description 完全缺失（系统列表中服务说明为空白行，用户无从核实用途）；settingsActivity 指向本包不存在的 com.example.root.myapplication.MainActivity；多个 ghahsb.* Activity 使用 android:label="" 配 69 字节空白 PNG 图标 zgcqisxuzp 并 excludeFromRecents，呈无名称条目；类名/方法名/字符串全量随机化混淆（32 个同名 kBSUFVbtSvlb 重载），资源与 assets 目录名混淆为 kgmowdr/hvqgsnotkdyt/monthly.b32；未使用伪造 isAccessibilityTool（该样本 targetSdk 28，早于该属性引入）。 |
| 无障碍服务类名 | `com.fqaqkdwn.uhkshvhv.IFBInWN` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.ianigyp.nranmg.RUptMi（android:name 指定的 Application，先于一切 Activity 执行） | 进程启动 Application.onCreate 回调 | 不可静态还原 | 无 | 无 | `com.ianigyp.nranmg.RUptMi.onCreate` |
| 2 | 冷启动入口 | 加密载荷 include/monthly.b32（经 include/last.b16 路径指针定位） | RUptMi.onCreate 内 kBSUFVbtSvlb / tDrycEXjvZ 方法链读取并处理载荷 | 不可静态还原 | 无 | 无 | `unknown/include/monthly.b32、unknown/include/last.b16、com.ianigyp.nranmg.tDrycEXjvZ.kBSUFVbtSvlb` |
| 3 | 跳无障碍设置 | 系统设置 > 无障碍 > 已安装服务列表项「Google Play Protect」（com.fqaqkdwn.uhkshvhv.IFBInWN） | 用户在系统无障碍列表点选该服务并开启开关（服务由系统绑定，manifest 已声明 BIND_ACCESSIBILITY_SERVICE + AccessibilityService intent-filter） | 系统无障碍页 | **原文**：Google Play Protect<br>**译注**：无障碍服务名显示为 Google Play Protect；服务说明（description）为空行 | 打开服务开关（该页由系统渲染，非应用自绘） | `#1 manifest:components（service com.fqaqkdwn.uhkshvhv.IFBInWN）、res/xml/hpgdxqwezny.xml` |
| 4 | 获权后动作 | IFBInWN 无障碍服务（onAccessibilityEvent：typeWindowContentChanged \| typeWindowStateChanged，canRetrieveWindowContent=true，flagIncludeNotImportantViews + flagReportViewIds） | 系统在无障碍事件（窗口内容/状态变化）时回调服务 | 不可静态还原 | 无 | 无 | `res/xml/hpgdxqwezny.xml（服务实现类 com.fqaqkdwn.uhkshvhv.IFBInWN 未出现在 classes.dex）` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项名称：Manifest 中 service com.fqaqkdwn.uhkshvhv.IFBInWN 的 android:label="Google Play Protect"（AndroidManifest.xml）
- 系统无障碍服务说明行：完全缺失 —— res/xml/hpgdxqwezny.xml 未声明 android:description，系统列表中该服务说明为空白
- 桌面/任务列表名称：application android:label="Google Play Service"；多个 ghahsb.* Activity 为 android:label="" 配空白 PNG 图标 zgcqisxuzp，呈无名称条目
- 应用内引导文案（弹窗/Activity/WebView/悬浮窗）：包内不存在任何承载位置 —— res/layout 全部 16 个文件均为无子节点空壳容器，无 res/values/strings.xml，无 assets 目录与 HTML 资源，故引导文本必然由运行期解密载荷动态生成，静态不可见

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Google Play Service | Google Play 服务（伪装 Google 官方 GMS 名称） | `AndroidManifest.xml <application android:label>` | 假反诈安全 |
| en | Google Play Protect | Google Play 保护机制（伪装 Google 官方安全组件名称） | `AndroidManifest.xml <service android:name="com.fqaqkdwn.uhkshvhv.IFBInWN" android:label>` | 假反诈安全 |
| en | com.example.root.myapplication.MainActivity | 示例工程残留路径（指向本包不存在的 Activity，用于填充 settingsActivity 字段） | `res/xml/hpgdxqwezny.xml android:settingsActivity` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原。可见 DEX 内不存在 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转点与任何 onResume/Timer 重跳逻辑，拒绝后的反馈循环需运行期观测
- **遮罩叠层 / 高仿系统设置页**：不可静态还原。已声明 SYSTEM_ALERT_WINDOW 权限且无障碍配置含 flagIncludeNotImportantViews，具备叠放遮罩能力，但遮罩绘制代码不在可见 DEX
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=28，且可见 DEX 无 APPLICATION_DETAILS_SETTINGS 跳转与受限设置引导代码）
- **获权后即时行为与防撤权机制**：不可静态还原。未发现 GLOBAL_ACTION_BACK/HOME 或自点确认相关代码（服务实现类不在可见 DEX），无法排除载荷内实现
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以「进程启动后任意 Activity 前台化」为拉起时机（该应用引导逻辑由 Application.onCreate 解密载荷后动态生成，无固定静态入口）；若观测到跳转 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS，应在跳转瞬间拉起并保留 800ms–3s 压栈帧。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：核心行为体（无障碍服务实现、全部引导 UI、跳转逻辑）静态不可见，全部位于加密载荷 include/monthly.b32，需运行期解密后由 UTG 捕获；此外应用存在多个 label="" 空白图标 Activity，UTG 页面上可能无任何可读文本，需依赖类名与窗口属性判别；启动早期 Application 阶段无界面，纯静态与首屏 UTG 均无法覆盖该阶段的载荷解密与预埋动作。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动/载荷解密后首个前台页面** | 包名 com.fqaqkdwn.uhkshvhv 下首个 Resume 的 Activity；注意可能出现 label="" 且无标题栏的 ghahsb.* 页面 | 应用内无任何静态引导资源，首屏是否直接弹出无障碍引导决定了属于「冷启动 0 步阻断」还是「功能触发」型 | 首个 Activity 类名与是否 Theme.Translucent.NoTitleBar；页面是否含按钮文案（如 Enable/Activate/Continue）；是否存在无法关闭的遮罩或返回键无效 |
| **跳转前引导/教学页** | 承载说明文字的原生 Dialog、Activity 或 WebView（若为 WebView，记录其 URL：本地 assets 或远端 http(s)） | 逐字文案与载体类型是区分假反诈安全、假更新、清理工具伪装等话术框架的直接证据 | Dialog 是否 setCancelable(false)/无取消按钮；WebView 加载 URL 与是否远端下发；页面文案是否出现 Google Play Protect 等品牌词 |
| **系统无障碍设置页与压栈遮罩** | Settings$AccessibilitySettings（列表项文本 Google Play Protect）以及其上叠加的悬浮窗 | 验证是否引导用户精确点选伪装服务，以及是否用 SYSTEM_ALERT_WINDOW 覆盖系统页做「点这里」指引 | 无障碍列表项名称与说明是否为空；是否有 TYPE_APPLICATION_OVERLAY 窗口覆盖在设置页上；返回后是否立即重新跳转 |
| **获权后动作页** | 开启开关后返回应用的界面或跳转的下一 Activity（可能为空白 label Activity） | 判断获权后是否立刻转入短信/通知读取、覆盖攻击或静默保活 | 获权后是否弹出新权限请求（短信/悬浮窗）；是否出现空白页面随后自退；是否触发其他设置页跳转 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `#1 manifest:components（service com.fqaqkdwn.uhkshvhv.IFBInWN android:label="Google Play Protect"）`
- `res/xml/hpgdxqwezny.xml（canRetrieveWindowContent=true，无 android:description，settingsActivity=com.example.root.myapplication.MainActivity）`
- `com.ianigyp.nranmg.RUptMi.onCreate`
- `unknown/include/last.b16（指向 include/monthly.b32）`
- `unknown/include/monthly.b32（188346 字节加密二阶段载荷）`
- `res/drawable/zgcqisxuzp.png（69 字节空白图标，用于 label="" 的 ghahsb.* Activity）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论

**结论：静态分析无法还原“逐步引导开启无障碍权限”的运行期流程，因为真实的无障碍服务实现和引导界面都被移出了可见 DEX，位于加密载荷中；只能确认 Manifest 层级的伪装外壳。**

**1. 无障碍声明的关键矛盾（可静态确认）**
- 服务 [com.fqaqkdwn.uhkshvhv.IFBInWN](<resource-unit:#1 manifest:components>) 声明 `android:label="Google Play Protect"`，而应用桌面名称为 `Google Play Service`，二者都借用 Google 官方品牌，但包名与 GMS 无任何归属关系。
- 无障碍配置 [res/xml/hpgdxqwezny.xml](<resource-unit:#1 file:res/xml/hpgdxqwezny.xml>) 只有 2 行有效属性：`canRetrieveWindowContent="true"`、`typeWindowContentChanged|typeWindowStateChanged`、`flagIncludeNotImportantViews`、`flagReportViewIds`，**完全没有 `android:description`**，这与预筛给出的 description 为空一致，因此系统无障碍列表中的服务说明行是空白的。
- 同一配置的 `android:settingsActivity="com.example.root.myapplication.MainActivity"` 是一个与本包无关的示例工程残留路径，在本包组件表中不存在，这说明配置由模板拼接，并且没有配置真实引导入口。

**2. 可见 DEX 内不存在引导逻辑**
- 在 `classes.dex` 中全文检索 `AccessibilityService`、`android.settings.ACCESSIBILITY`、`BIND_ACCESSIBILITY`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`DexClassLoader`、`getAssets`，**全部没有命中**；`IFBInWN` 类本体也不在可见 DEX（`list_codebase` 仅 41 个类，全部为 `com.ianigyp.nranmg` / `com.mrbtolwomd`）。
- 全部 16 个 layout 都是空壳容器（仅根节点，无子视图、无文本），`res/values` 下只有 `attrs/ids/public`，**没有 strings.xml，没有 assets/HTML**。也就是说，包内不存在任何可承载引导文案的原生布局或本地 WebView 页面。

**3. 真正的行为在加密二阶段载荷中**
- [com.ianigyp.nranmg.RUptMi#onCreate](<resource-unit:#1.dex1 code:com.ianigyp.nranmg.RUptMi#onCreate>) 是 `android:name` 指定的 Application，启动即执行混淆方法链（32 个 `kBSUFVbtSvlb` 重载）。
- 载荷入口 [unknown/include/last.b16](<resource-unit:#1 file:unknown/include/last.b16>) 仅有 19 字节，明文内容就是 `include/monthly.b32` 的路径指针；[unknown/include/monthly.b32](<resource-unit:#1 file:unknown/include/monthly.b32>) 为 188,346 字节（前 4 字节为 188,342 的长度前缀），高熵，尾部无块对齐特征。
- 对 `monthly.b32` 尝试单字节 XOR（256 键）、`kgmowdr`/`hvqgsnotkdyt` 两个 41 字节混淆串 XOR（8 种偏移）、AES-128/256 ECB/CBC（多组密钥候选）以及裸 zlib，**均未得到 `dex\n`/`PK`/gzip/zlib 头**。解密算法不可静态还原。

**4. 同族特征**
- 声明 `SYSTEM_ALERT_WINDOW`、`RECEIVE_SMS`/`WRITE_SMS` + `SMS_DELIVER` 接收器、`READ_CONTACTS`、`RECORD_AUDIO`、`PACKAGE_USAGE_STATS`、`CALL_PHONE`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`，与 Hqwar 家族的短信拦截 + 无障碍覆盖攻击组合一致。
- 多个 `ghahsb.*` Activity 使用 `android:label=""` 与 69 字节空白图 [res/drawable/zgcqisxuzp.png](<resource-unit:#1 file:res/drawable/zgcqisxuzp.png>)，并且设置了 `excludeFromRecents="true"`，任务列表与弹窗中呈现为无名称条目。

**5. 覆盖边界**
- 引导文案的逐字原文、弹窗/遮罩载体、拒绝后的重跳机制、获权后自保动作，**在本包可静态触及的范围内均无证据**；它们只能通过运行期 UTG 在载荷解密加载后捕获。因此 `static_visibility` 标注为 `packed_or_encrypted`。

已登记风险 R-001（autonomous_audit / high / deceptive_behavior）：伪装 Google Play 品牌的无障碍服务与加密二阶段载荷。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest 声明、无障碍 XML 配置、权限集与 Application 入口完整可见；但 IFBInWN 无障碍服务类本体、全部引导 UI 与跳转逻辑均不在 classes.dex（全文检索 AccessibilityService/DexClassLoader/getAssets/ACCESSIBILITY 设置 action 零命中），包内 16 个 layout 全为空壳根节点、无 strings.xml、无 assets/HTML。真实行为藏于 unknown/include/monthly.b32（188346 字节高熵密文，长度前缀 188342），由 Application.onCreate 经 last.b16 指针加载；单字节 XOR 256 键、两把 41 字节混淆串 XOR、AES-128/256 ECB/CBC、裸 zlib 试解均未得到 dex/PK/gzip 头，解密算法静态不可还原。",
  "summary_one_liner": "以「Google Play Service」桌面名和「Google Play Protect」无障碍服务名伪造官方身份，无障碍配置 description 留空、settingsActivity 为无关示例路径，真实引导与无障碍执行体整体移入 AES 类加密载荷 include/monthly.b32，运行期才解密加载。",
  "disguise_identity": {
    "app_display_name": "Google Play Service",
    "claimed_brand_or_persona": "Google Play Service / Google Play Protect（Google 官方 GMS 品牌）",
    "a11y_service_label": "Google Play Protect",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 android:description 完全缺失（系统列表中服务说明为空白行，用户无从核实用途）；settingsActivity 指向本包不存在的 com.example.root.myapplication.MainActivity；多个 ghahsb.* Activity 使用 android:label=\"\" 配 69 字节空白 PNG 图标 zgcqisxuzp 并 excludeFromRecents，呈无名称条目；类名/方法名/字符串全量随机化混淆（32 个同名 kBSUFVbtSvlb 重载），资源与 assets 目录名混淆为 kgmowdr/hvqgsnotkdyt/monthly.b32；未使用伪造 isAccessibilityTool（该样本 targetSdk 28，早于该属性引入）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.ianigyp.nranmg.RUptMi（android:name 指定的 Application，先于一切 Activity 执行）",
      "trigger_event": "进程启动 Application.onCreate 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该阶段无任何界面，仅执行混淆初始化方法链",
      "user_action_requested": "无",
      "code_anchor": "com.ianigyp.nranmg.RUptMi.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "加密载荷 include/monthly.b32（经 include/last.b16 路径指针定位）",
      "trigger_event": "RUptMi.onCreate 内 kBSUFVbtSvlb / tDrycEXjvZ 方法链读取并处理载荷",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "载荷解密后的类实现（含无障碍服务与引导 UI）不可静态还原，其界面形态无法确认",
      "user_action_requested": "无",
      "code_anchor": "unknown/include/monthly.b32、unknown/include/last.b16、com.ianigyp.nranmg.tDrycEXjvZ.kBSUFVbtSvlb"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 > 无障碍 > 已安装服务列表项「Google Play Protect」（com.fqaqkdwn.uhkshvhv.IFBInWN）",
      "trigger_event": "用户在系统无障碍列表点选该服务并开启开关（服务由系统绑定，manifest 已声明 BIND_ACCESSIBILITY_SERVICE + AccessibilityService intent-filter）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Google Play Protect",
      "shown_text_zh": "无障碍服务名显示为 Google Play Protect；服务说明（description）为空行",
      "user_action_requested": "打开服务开关（该页由系统渲染，非应用自绘）",
      "code_anchor": "#1 manifest:components（service com.fqaqkdwn.uhkshvhv.IFBInWN）、res/xml/hpgdxqwezny.xml"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "IFBInWN 无障碍服务（onAccessibilityEvent：typeWindowContentChanged | typeWindowStateChanged，canRetrieveWindowContent=true，flagIncludeNotImportantViews + flagReportViewIds）",
      "trigger_event": "系统在无障碍事件（窗口内容/状态变化）时回调服务",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务实现不在可见 DEX，获权后的读取窗口内容、模拟点击与覆盖行为无法静态确认",
      "user_action_requested": "无",
      "code_anchor": "res/xml/hpgdxqwezny.xml（服务实现类 com.fqaqkdwn.uhkshvhv.IFBInWN 未出现在 classes.dex）"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项名称：Manifest 中 service com.fqaqkdwn.uhkshvhv.IFBInWN 的 android:label=\"Google Play Protect\"（AndroidManifest.xml）",
    "系统无障碍服务说明行：完全缺失 —— res/xml/hpgdxqwezny.xml 未声明 android:description，系统列表中该服务说明为空白",
    "桌面/任务列表名称：application android:label=\"Google Play Service\"；多个 ghahsb.* Activity 为 android:label=\"\" 配空白 PNG 图标 zgcqisxuzp，呈无名称条目",
    "应用内引导文案（弹窗/Activity/WebView/悬浮窗）：包内不存在任何承载位置 —— res/layout 全部 16 个文件均为无子节点空壳容器，无 res/values/strings.xml，无 assets 目录与 HTML 资源，故引导文本必然由运行期解密载荷动态生成，静态不可见"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Google Play Service",
      "text_zh": "Google Play 服务（伪装 Google 官方 GMS 名称）",
      "source_location": "AndroidManifest.xml <application android:label>",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Google Play Protect",
      "text_zh": "Google Play 保护机制（伪装 Google 官方安全组件名称）",
      "source_location": "AndroidManifest.xml <service android:name=\"com.fqaqkdwn.uhkshvhv.IFBInWN\" android:label>",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "com.example.root.myapplication.MainActivity",
      "text_zh": "示例工程残留路径（指向本包不存在的 Activity，用于填充 settingsActivity 字段）",
      "source_location": "res/xml/hpgdxqwezny.xml android:settingsActivity",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原。可见 DEX 内不存在 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS 跳转点与任何 onResume/Timer 重跳逻辑，拒绝后的反馈循环需运行期观测",
    "overlay_or_fake_settings": "不可静态还原。已声明 SYSTEM_ALERT_WINDOW 权限且无障碍配置含 flagIncludeNotImportantViews，具备叠放遮罩能力，但遮罩绘制代码不在可见 DEX",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=28，且可见 DEX 无 APPLICATION_DETAILS_SETTINGS 跳转与受限设置引导代码）",
    "post_grant_anti_removal": "不可静态还原。未发现 GLOBAL_ACTION_BACK/HOME 或自点确认相关代码（服务实现类不在可见 DEX），无法排除载荷内实现",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以「进程启动后任意 Activity 前台化」为拉起时机（该应用引导逻辑由 Application.onCreate 解密载荷后动态生成，无固定静态入口）；若观测到跳转 android.settings.ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS，应在跳转瞬间拉起并保留 800ms–3s 压栈帧。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动/载荷解密后首个前台页面",
        "page_identifier": "包名 com.fqaqkdwn.uhkshvhv 下首个 Resume 的 Activity；注意可能出现 label=\"\" 且无标题栏的 ghahsb.* 页面",
        "why_most_useful": "应用内无任何静态引导资源，首屏是否直接弹出无障碍引导决定了属于「冷启动 0 步阻断」还是「功能触发」型",
        "observable_utg_signals": ["首个 Activity 类名与是否 Theme.Translucent.NoTitleBar", "页面是否含按钮文案（如 Enable/Activate/Continue）", "是否存在无法关闭的遮罩或返回键无效"]
      },
      {
        "page_role": "跳转前引导/教学页",
        "page_identifier": "承载说明文字的原生 Dialog、Activity 或 WebView（若为 WebView，记录其 URL：本地 assets 或远端 http(s)）",
        "why_most_useful": "逐字文案与载体类型是区分假反诈安全、假更新、清理工具伪装等话术框架的直接证据",
        "observable_utg_signals": ["Dialog 是否 setCancelable(false)/无取消按钮", "WebView 加载 URL 与是否远端下发", "页面文案是否出现 Google Play Protect 等品牌词"]
      },
      {
        "page_role": "系统无障碍设置页与压栈遮罩",
        "page_identifier": "Settings$AccessibilitySettings（列表项文本 Google Play Protect）以及其上叠加的悬浮窗",
        "why_most_useful": "验证是否引导用户精确点选伪装服务，以及是否用 SYSTEM_ALERT_WINDOW 覆盖系统页做「点这里」指引",
        "observable_utg_signals": ["无障碍列表项名称与说明是否为空", "是否有 TYPE_APPLICATION_OVERLAY 窗口覆盖在设置页上", "返回后是否立即重新跳转"]
      },
      {
        "page_role": "获权后动作页",
        "page_identifier": "开启开关后返回应用的界面或跳转的下一 Activity（可能为空白 label Activity）",
        "why_most_useful": "判断获权后是否立刻转入短信/通知读取、覆盖攻击或静默保活",
        "observable_utg_signals": ["获权后是否弹出新权限请求（短信/悬浮窗）", "是否出现空白页面随后自退", "是否触发其他设置页跳转"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：核心行为体（无障碍服务实现、全部引导 UI、跳转逻辑）静态不可见，全部位于加密载荷 include/monthly.b32，需运行期解密后由 UTG 捕获；此外应用存在多个 label=\"\" 空白图标 Activity，UTG 页面上可能无任何可读文本，需依赖类名与窗口属性判别；启动早期 Application 阶段无界面，纯静态与首屏 UTG 均无法覆盖该阶段的载荷解密与预埋动作。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "#1 manifest:components（service com.fqaqkdwn.uhkshvhv.IFBInWN android:label=\"Google Play Protect\"）",
    "res/xml/hpgdxqwezny.xml（canRetrieveWindowContent=true，无 android:description，settingsActivity=com.example.root.myapplication.MainActivity）",
    "com.ianigyp.nranmg.RUptMi.onCreate",
    "unknown/include/last.b16（指向 include/monthly.b32）",
    "unknown/include/monthly.b32（188346 字节加密二阶段载荷）",
    "res/drawable/zgcqisxuzp.png（69 字节空白图标，用于 label=\"\" 的 ghahsb.* Activity）"
  ]
}
```

</details>
