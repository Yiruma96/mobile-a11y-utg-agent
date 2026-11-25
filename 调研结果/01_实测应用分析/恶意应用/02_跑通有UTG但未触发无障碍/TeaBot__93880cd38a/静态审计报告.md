# MB_116__93880cd38a｜TeaBot — PDF Text Recognition: Add-On

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：160.1s

## 1. 一句话核心结论

- **核心申请方式**：应用以 PDF 文字识别工具为外壳，无障碍服务与引导页面整体藏入加密二阶段载荷，由 attachBaseContext 反射壳解密加载后才向用户展示开启引导，静态无任何用途说明。
- **静态可见性说明**：Manifest 与壳调用链静态完整可见，但无障碍服务实现类、Launcher Activity、全部引导页面（弹窗/WebView/悬浮窗）及其文案均不在 classes.dex；检索 in.makaek / UIDNwaidobaWIODb / KAopneaoniAoiasM 均为 no_matches，ACCESSIBILITY_SETTINGS 在应用自身代码零命中。真实代码位于 assets/oHkaUfo/U6fdggioU1.pyp（zlib 解压后仍为高熵密文）与高熵 assets/analytics，由 attachBaseContext 阶段反射式壳解密加载，静态无法取得引导文案与页面流转。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `93880cd38abffa10e753c17ae7c14f0833356cba601bd1a3d3998859f47c900f` |
| 包名 / 年份 | `com.obckaliva.ebnxvikzi` / 2022 |
| 家族 / 品类 | **TeaBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | PDF Text Recognition: Add-On |
| 引导页宣称品牌/身份 | 伪装为 PDF 文字识别类工具应用（Add-On 插件）；实际代码位于 com.car.parking.master.puzzle.truck.games 游戏命名空间，与声称功能无关 |
| 系统无障碍列表服务名 | 无（asclllservizio.xml 未设置 android:description 与 android:summary，系统无障碍列表中服务项无用途说明） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：全部 Activity 的 android:label 置为空字符串以在界面/最近任务中隐去名称；无障碍服务刻意不声明 android:description（挤出系统警告与用途说明）；Application 实现类放在与业务无关的 com.car.parking.master.puzzle.truck.games 包下并以 a/b/c 单字母类名混淆；服务与 Activity 类名随机化（UIDNwaidobaWIODb、KAopneaoniAoiasM）；真实逻辑封装在 assets/oHkaUfo/U6fdggioU1.pyp 加密载荷内并在 attachBaseContext 反射注入 |
| 无障碍服务类名 | `in.makaek.galbak.UIDNwaidobaWIODb` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.car.parking.master.puzzle.truck.games.a（伪装的 Application 类） | 进程创建时 attachBaseContext 回调 | 不可静态还原 | 无 | 无（用户无感知） | `com.car.parking.master.puzzle.truck.games.a.attachBaseContext` |
| 2 | 冷启动入口 | b.a(Context) / b.a(Context,File,File,String,String) / c.a(Context,String,boolean) | attachBaseContext 内调用 b.a(this) | 不可静态还原 | 无 | 无 | `com.car.parking.master.puzzle.truck.games.b.a(Context, File, File, String, String)` |
| 3 | 引导说明页 | in.makaek.galbak.KAopneaoniAoiasM（LAUNCHER Activity，实现类不在 DEX） | 用户点击桌面图标（label 为空，显示名仅取自 application 的 PDF Text Recognition: Add-On） | 不可静态还原 | 无 | 不可静态确认 | `#1 manifest:components` |
| 4 | 跳无障碍设置 | 预期为 android.settings.ACCESSIBILITY_SETTINGS（跳转代码不在 DEX） | 不可静态还原 | 系统无障碍页 | **原文**：无（服务项因未配置 android:description 而无用途说明）<br>**译注**：系统无障碍列表中的服务条目无描述，仅显示随机化服务名 | 用户在系统列表中手动打开该服务开关 | `res/xml/asclllservizio.xml` |
| 5 | 遮罩叠层指引 | 预期由 in.makaek.galbak.inject.uibwduIABuIaw（singleTask、excludeFromRecents、Theme.NoTitleBar）或悬浮窗承载 | 不可静态还原 | 悬浮窗Overlay | 无 | 不可静态确认 | `in.makaek.galbak.inject.uibwduIABuIaw` |
| 6 | 获权后动作 | in.makaek.galbak.UIDNwaidobaWIODb（无障碍服务本体，实现类不在 DEX） | 系统在用户启用后实例化服务并回调 onServiceConnected/onAccessibilityEvent | 不可静态还原 | 无 | 无 | `res/xml/asclllservizio.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/xml/asclllservizio.xml：系统无障碍列表中的服务条目（未声明 android:description/summary，故无用途说明文字）
- AndroidManifest.xml：application android:label="PDF Text Recognition: Add-On"（桌面图标名称）；所有 Activity 的 android:label 为空串
- in.makaek.galbak.KAopneaoniAoiasM（LAUNCHER Activity）：首屏引导内容，实现类不在 classes.dex，位于加密载荷 U6fdggioU1.pyp
- in.makaek.galbak.inject.uibwduIABuIaw（singleTask + excludeFromRecents + Theme.NoTitleBar）：疑似设置页跳转后的覆盖/引导层，内容不可静态还原
- assets/oHkaUfo/U6fdggioU1.pyp 与 assets/analytics：加密载荷，可能包含远端 HTML 或文案资源，静态不可读
- assets/tcaptcha_webview.html：仅腾讯验证码回调 iframe 骨架，无引导文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | PDF Text Recognition: Add-On | PDF 文字识别：附加组件 | `AndroidManifest.xml application android:label` | 清理工具伪装 |
| en | Enable Google Play services / %1$s won't work unless you enable Google Play services. | 启用 Google Play 服务 / 若不启用 Google Play 服务，%1$s 将无法工作。 | `res/values/strings.xml（common_google_play_services_*，属 Google Play Services 库自带字符串，非应用自写引导文案）` | 未知 |
| en | ms.singaporepaya.com | （C2 域名，非界面文案） | `assets/centauri_oversea_singapore/centauri_oversea_cp.cfg` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：判断无障碍是否已启用、拒绝或返回后的重跳逻辑均位于加密载荷 U6fdggioU1.pyp 内，首层 DEX 无 AccessibilityManager/AccessibilityServiceInfo 相关校验代码；仅可确认壳在 attachBaseContext 阶段无条件解密加载，任何界面出现前已完成载荷注入
- **遮罩叠层 / 高仿系统设置页**：存在覆盖层载体但内容不可静态还原：Manifest 中 in.makaek.galbak.inject.uibwduIABuIaw 具备 singleTask、excludeFromRecents、Theme.NoTitleBar 组合，符合设置页之上叠放全屏覆盖/引导层特征；未发现可静态确认的高仿系统无障碍开关页布局资源（res 下无相关 layout）
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（targetSdkVersion=28，低于 13；APPLICATION_DETAILS_SETTINGS 跳转在应用自身代码零命中，相关教学逻辑可能位于加密载荷内）
- **获权后即时行为与防撤权机制**：无静态证据：首层 DEX 中无 GLOBAL_ACTION_BACK/GLOBAL_ACTION_HOME 调用点，撤权阻止逻辑若存在亦在加密载荷内
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：进程启动即拉起 UTG 监测：以 com.obckaliva.ebnxvikzi 进程首个 Activity onResume 为锚点（壳在 attachBaseContext 已解密完成，后续任何界面均属载荷真实引导）；同时在系统侧监测无障碍列表出现 in.makaek.galbak.UIDNwaidobaWIODb 条目、以及任何指向 android.settings.ACCESSIBILITY_SETTINGS 的页面跳转作为第二触发点
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：引导页面与全部文案位于加密载荷 U6fdggioU1.pyp（zlib 解压后仍为高熵密文），静态无法提供任何可对照的预期文案，UTG 只能在运行期首次呈现时抓取；若载荷在非目标环境（模拟器/无 SIM/无目标金融应用）下不展示引导，UTG 可能只捕获到空壳页。静态加壳本身不阻挡运行期 UTG，需以真实设备+正常网络（C2 ms.singaporepaya.com）运行。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首个界面（载荷解密后的真实引导页）** | 包 com.obckaliva.ebnxvikzi 下 Activity in.makaek.galbak.KAopneaoniAoiasM，label 为空、Theme 默认 | 此页是唯一能取得应用自写引导文案的时机，全部文案在加密载荷内，静态完全不可见 | 页面文本节点全量（含中文/英文引导语）；按钮文案与是否存在取消/跳过控件；是否出现 PDF/工具类图标与品牌名 |
| **系统无障碍服务列表项** | 设置 > 无障碍 > 已下载/已安装服务列表，条目名含 UIDNwaidobaWIODb 随机串且无副标题描述 | 验证应用刻意省略 android:description 以隐去用途说明，是无身份说明型无障碍申请的确定性证据 | 服务条目文本（仅随机名，无描述）；条目是否被高亮/被引导圈选；列表滚动位置是否被自动定位到该条目 |
| **跳转设置后压栈的覆盖/引导层** | in.makaek.galbak.inject.uibwduIABuIaw（excludeFromRecents、Theme.NoTitleBar、singleTask） | 该 Activity 的 Manifest 属性高度符合'设置页之上叠放遮罩引导'模式，是区分诱导与良性说明的关键页 | 是否存在半透明遮罩与手指/箭头指示；是否覆盖系统开关位置；是否有'必须开启否则无法使用'类文案；返回键是否被吞掉或重跳 |
| **获权后首个自动化动作页** | 无障碍服务启用瞬间的系统事件与随后跳转的页面 | 确认获权后是否立即执行短信读取、包名扫描或覆盖目标金融应用 | 获权后 1-3 秒内页面跳转目标；是否出现通知栏常驻项；是否弹出电池优化忽略请求 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.car.parking.master.puzzle.truck.games.a.attachBaseContext`
- `com.car.parking.master.puzzle.truck.games.b.a(Context, File, File, String, String)`
- `com.car.parking.master.puzzle.truck.games.c.a(Context, String, boolean)`
- `res/xml/asclllservizio.xml`
- `assets/oHkaUfo/U6fdggioU1.pyp`
- `AndroidManifest.xml（service in.makaek.galbak.UIDNwaidobaWIODb / activity in.makaek.galbak.inject.uibwduIABuIaw）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（12 次工具调用内完成）

**核心事实：无障碍引导流程完全不在首层 DEX，被移入加密二阶段载荷。**

1. **Manifest 声明了高权限无障碍服务，但该服务无任何身份说明**
   - 服务 `in.makaek.galbak.UIDNwaidobaWIODb`，`BIND_ACCESSIBILITY_SERVICE`、`exported=false`；
   - 配置 [res/xml/asclllservizio.xml](<resource-unit:#1 file:res/xml/asclllservizio.xml>) 为 `typeAllMask` + `flagRetrieveInteractiveWindows` + `canRetrieveWindowContent=true` + `canPerformGestures=true`，**且无 `android:description` / `android:summary`** —— 系统无障碍列表中将不显示任何用途说明。
2. **该服务类在 DEX 中不存在**：检索 `UIDNwaidobaWIODb`、`KAopneaoniAoiasM`、`in.makaek` 全部 `no_matches`；`ACCESSIBILITY_SETTINGS` / `APPLICATION_DETAILS_SETTINGS` 在应用自身代码中零命中（仅命中系统自带 `com.miui.*`）。Launcher Activity 与全部引导页实现同样缺失。
3. **壳入口清晰可还原**：[a.attachBaseContext()](<resource-unit:#1.dex1 code:com.car.parking.master.puzzle.truck.games.a#attachBaseContext>) → [b.a(Context)](<resource-unit:#1.dex1 code:com.car.parking.master.puzzle.truck.games.b#void a(android.content.Context)>) → [b.a(Context,File,File,String,String)](<resource-unit:#1.dex1 code:com.car.parking.master.puzzle.truck.games.b#void a(android.content.Context, java.io.File, java.io.File, java.lang.String, java.lang.String)>)（`ZipFile`/`ZipEntry` 解包）→ [c.a(Context,String,boolean)](<resource-unit:#1.dex1 code:com.car.parking.master.puzzle.truck.games.c#java.util.List<? extends java.io.File> a(android.content.Context, java.lang.String, boolean)>) 解密落盘 → 反射替换 `ActivityThread.mInstrumentation`、`mBoundApplication`、`ApplicationInfo.className`。
4. **载荷资产**：[assets/oHkaUfo/U6fdggioU1.pyp](<resource-unit:#1 file:assets/oHkaUfo/U6fdggioU1.pyp>)（266 KB，`78 9C` zlib 头，解压后仍为高熵密文、无可读字符串）；`assets/analytics` 同为高熵密文；[centauri_oversea_cp.cfg](<resource-unit:#1 file:assets/centauri_oversea_singapore/centauri_oversea_cp.cfg>) 给出 C2 `ms.singaporepaya.com` / `119.28.109.70`。
5. **身份伪装**：桌面名 `PDF Text Recognition: Add-On`，而 Application 类位于 `com.car.parking.master.puzzle.truck.games`（停车/拼图小游戏命名空间），**所有 Activity 的 `android:label` 均为空串**；权限组合 `READ_SMS/RECEIVE_SMS/SEND_SMS` + `priority=999` 的 `SMS_DELIVER` 接收器 + `QUERY_ALL_PACKAGES` + `SYSTEM_ALERT_WINDOW`，符合 TeaBot 家族"无障碍覆盖 + 短信验证码窃取"特征。
6. **未决/覆盖边界**：`U6fdggioU1.pyp` 解压后仍加密，未能算法级还原，因此引导弹窗文案、Activity 序列、拒权循环、悬浮遮罩均**无法静态逐字取证**，只能靠运行期 UTG 获取。

已登记风险 **R-001**（high / malware_trojan）：无障碍服务实现与引导流程隐藏于加密二阶段载荷。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest 与壳调用链静态完整可见，但无障碍服务实现类、Launcher Activity、全部引导页面（弹窗/WebView/悬浮窗）及其文案均不在 classes.dex；检索 in.makaek / UIDNwaidobaWIODb / KAopneaoniAoiasM 均为 no_matches，ACCESSIBILITY_SETTINGS 在应用自身代码零命中。真实代码位于 assets/oHkaUfo/U6fdggioU1.pyp（zlib 解压后仍为高熵密文）与高熵 assets/analytics，由 attachBaseContext 阶段反射式壳解密加载，静态无法取得引导文案与页面流转。",
  "summary_one_liner": "应用以 PDF 文字识别工具为外壳，无障碍服务与引导页面整体藏入加密二阶段载荷，由 attachBaseContext 反射壳解密加载后才向用户展示开启引导，静态无任何用途说明。",
  "disguise_identity": {
    "app_display_name": "PDF Text Recognition: Add-On",
    "claimed_brand_or_persona": "伪装为 PDF 文字识别类工具应用（Add-On 插件）；实际代码位于 com.car.parking.master.puzzle.truck.games 游戏命名空间，与声称功能无关",
    "a11y_service_label": "无（asclllservizio.xml 未设置 android:description 与 android:summary，系统无障碍列表中服务项无用途说明）",
    "identity_mismatch": true,
    "obfuscation_tricks": "全部 Activity 的 android:label 置为空字符串以在界面/最近任务中隐去名称；无障碍服务刻意不声明 android:description（挤出系统警告与用途说明）；Application 实现类放在与业务无关的 com.car.parking.master.puzzle.truck.games 包下并以 a/b/c 单字母类名混淆；服务与 Activity 类名随机化（UIDNwaidobaWIODb、KAopneaoniAoiasM）；真实逻辑封装在 assets/oHkaUfo/U6fdggioU1.pyp 加密载荷内并在 attachBaseContext 反射注入"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.car.parking.master.puzzle.truck.games.a（伪装的 Application 类）",
      "trigger_event": "进程创建时 attachBaseContext 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此阶段无界面，仅执行解密与加载",
      "user_action_requested": "无（用户无感知）",
      "code_anchor": "com.car.parking.master.puzzle.truck.games.a.attachBaseContext"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "b.a(Context) / b.a(Context,File,File,String,String) / c.a(Context,String,boolean)",
      "trigger_event": "attachBaseContext 内调用 b.a(this)",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "使用 ZipFile/ZipEntry 从 APK 解出加密条目并解密落盘，再以反射替换 ActivityThread.mInstrumentation、mBoundApplication 与 ApplicationInfo.className，装载真实 Application",
      "user_action_requested": "无",
      "code_anchor": "com.car.parking.master.puzzle.truck.games.b.a(Context, File, File, String, String)"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "in.makaek.galbak.KAopneaoniAoiasM（LAUNCHER Activity，实现类不在 DEX）",
      "trigger_event": "用户点击桌面图标（label 为空，显示名仅取自 application 的 PDF Text Recognition: Add-On）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "首个界面内容完全位于加密载荷内，静态不可取得",
      "user_action_requested": "不可静态确认",
      "code_anchor": "#1 manifest:components"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "预期为 android.settings.ACCESSIBILITY_SETTINGS（跳转代码不在 DEX）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（服务项因未配置 android:description 而无用途说明）",
      "shown_text_zh": "系统无障碍列表中的服务条目无描述，仅显示随机化服务名",
      "user_action_requested": "用户在系统列表中手动打开该服务开关",
      "code_anchor": "res/xml/asclllservizio.xml"
    },
    {
      "step": 5,
      "stage": "遮罩叠层指引",
      "screen_or_component": "预期由 in.makaek.galbak.inject.uibwduIABuIaw（singleTask、excludeFromRecents、Theme.NoTitleBar）或悬浮窗承载",
      "trigger_event": "不可静态还原",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 具备无标题全屏、排除最近任务、单实例等覆盖/引导特征，具体遮罩内容与文案在加密载荷内",
      "user_action_requested": "不可静态确认",
      "code_anchor": "in.makaek.galbak.inject.uibwduIABuIaw"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "in.makaek.galbak.UIDNwaidobaWIODb（无障碍服务本体，实现类不在 DEX）",
      "trigger_event": "系统在用户启用后实例化服务并回调 onServiceConnected/onAccessibilityEvent",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "服务配置为全事件监听、可读取窗口内容、可执行手势，具备界面覆盖与自动化点击能力",
      "user_action_requested": "无",
      "code_anchor": "res/xml/asclllservizio.xml"
    }
  ],
  "text_presentation_locations": [
    "res/xml/asclllservizio.xml：系统无障碍列表中的服务条目（未声明 android:description/summary，故无用途说明文字）",
    "AndroidManifest.xml：application android:label=\"PDF Text Recognition: Add-On\"（桌面图标名称）；所有 Activity 的 android:label 为空串",
    "in.makaek.galbak.KAopneaoniAoiasM（LAUNCHER Activity）：首屏引导内容，实现类不在 classes.dex，位于加密载荷 U6fdggioU1.pyp",
    "in.makaek.galbak.inject.uibwduIABuIaw（singleTask + excludeFromRecents + Theme.NoTitleBar）：疑似设置页跳转后的覆盖/引导层，内容不可静态还原",
    "assets/oHkaUfo/U6fdggioU1.pyp 与 assets/analytics：加密载荷，可能包含远端 HTML 或文案资源，静态不可读",
    "assets/tcaptcha_webview.html：仅腾讯验证码回调 iframe 骨架，无引导文案"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "PDF Text Recognition: Add-On",
      "text_zh": "PDF 文字识别：附加组件",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Enable Google Play services / %1$s won't work unless you enable Google Play services.",
      "text_zh": "启用 Google Play 服务 / 若不启用 Google Play 服务，%1$s 将无法工作。",
      "source_location": "res/values/strings.xml（common_google_play_services_*，属 Google Play Services 库自带字符串，非应用自写引导文案）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "ms.singaporepaya.com",
      "text_zh": "（C2 域名，非界面文案）",
      "source_location": "assets/centauri_oversea_singapore/centauri_oversea_cp.cfg",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：判断无障碍是否已启用、拒绝或返回后的重跳逻辑均位于加密载荷 U6fdggioU1.pyp 内，首层 DEX 无 AccessibilityManager/AccessibilityServiceInfo 相关校验代码；仅可确认壳在 attachBaseContext 阶段无条件解密加载，任何界面出现前已完成载荷注入",
    "overlay_or_fake_settings": "存在覆盖层载体但内容不可静态还原：Manifest 中 in.makaek.galbak.inject.uibwduIABuIaw 具备 singleTask、excludeFromRecents、Theme.NoTitleBar 组合，符合设置页之上叠放全屏覆盖/引导层特征；未发现可静态确认的高仿系统无障碍开关页布局资源（res 下无相关 layout）",
    "restricted_settings_13plus_coaching": "无静态证据（targetSdkVersion=28，低于 13；APPLICATION_DETAILS_SETTINGS 跳转在应用自身代码零命中，相关教学逻辑可能位于加密载荷内）",
    "post_grant_anti_removal": "无静态证据：首层 DEX 中无 GLOBAL_ACTION_BACK/GLOBAL_ACTION_HOME 调用点，撤权阻止逻辑若存在亦在加密载荷内",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "进程启动即拉起 UTG 监测：以 com.obckaliva.ebnxvikzi 进程首个 Activity onResume 为锚点（壳在 attachBaseContext 已解密完成，后续任何界面均属载荷真实引导）；同时在系统侧监测无障碍列表出现 in.makaek.galbak.UIDNwaidobaWIODb 条目、以及任何指向 android.settings.ACCESSIBILITY_SETTINGS 的页面跳转作为第二触发点",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首个界面（载荷解密后的真实引导页）",
        "page_identifier": "包 com.obckaliva.ebnxvikzi 下 Activity in.makaek.galbak.KAopneaoniAoiasM，label 为空、Theme 默认",
        "why_most_useful": "此页是唯一能取得应用自写引导文案的时机，全部文案在加密载荷内，静态完全不可见",
        "observable_utg_signals": ["页面文本节点全量（含中文/英文引导语）", "按钮文案与是否存在取消/跳过控件", "是否出现 PDF/工具类图标与品牌名"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "设置 > 无障碍 > 已下载/已安装服务列表，条目名含 UIDNwaidobaWIODb 随机串且无副标题描述",
        "why_most_useful": "验证应用刻意省略 android:description 以隐去用途说明，是无身份说明型无障碍申请的确定性证据",
        "observable_utg_signals": ["服务条目文本（仅随机名，无描述）", "条目是否被高亮/被引导圈选", "列表滚动位置是否被自动定位到该条目"]
      },
      {
        "page_role": "跳转设置后压栈的覆盖/引导层",
        "page_identifier": "in.makaek.galbak.inject.uibwduIABuIaw（excludeFromRecents、Theme.NoTitleBar、singleTask）",
        "why_most_useful": "该 Activity 的 Manifest 属性高度符合'设置页之上叠放遮罩引导'模式，是区分诱导与良性说明的关键页",
        "observable_utg_signals": ["是否存在半透明遮罩与手指/箭头指示", "是否覆盖系统开关位置", "是否有'必须开启否则无法使用'类文案", "返回键是否被吞掉或重跳"]
      },
      {
        "page_role": "获权后首个自动化动作页",
        "page_identifier": "无障碍服务启用瞬间的系统事件与随后跳转的页面",
        "why_most_useful": "确认获权后是否立即执行短信读取、包名扫描或覆盖目标金融应用",
        "observable_utg_signals": ["获权后 1-3 秒内页面跳转目标", "是否出现通知栏常驻项", "是否弹出电池优化忽略请求"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：引导页面与全部文案位于加密载荷 U6fdggioU1.pyp（zlib 解压后仍为高熵密文），静态无法提供任何可对照的预期文案，UTG 只能在运行期首次呈现时抓取；若载荷在非目标环境（模拟器/无 SIM/无目标金融应用）下不展示引导，UTG 可能只捕获到空壳页。静态加壳本身不阻挡运行期 UTG，需以真实设备+正常网络（C2 ms.singaporepaya.com）运行。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "com.car.parking.master.puzzle.truck.games.a.attachBaseContext",
    "com.car.parking.master.puzzle.truck.games.b.a(Context, File, File, String, String)",
    "com.car.parking.master.puzzle.truck.games.c.a(Context, String, boolean)",
    "res/xml/asclllservizio.xml",
    "assets/oHkaUfo/U6fdggioU1.pyp",
    "AndroidManifest.xml（service in.makaek.galbak.UIDNwaidobaWIODb / activity in.makaek.galbak.inject.uibwduIABuIaw）"
  ]
}
```

</details>
