# MR_143__d9bc87ab45｜Brata — Privacy Titan

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：119.6s

## 1. 一句话核心结论

- **核心申请方式**：以“Privacy Titan/隐私工具”为外壳、无障碍服务伪装成葡语“更新服务”，冷启动弹说明页诱导点击后启动 35 秒定时器：检测到未授权即跳系统无障碍页并在其上压入 5 秒自动消失的自有引导页，循环往复直至授权，授权后反射隐藏桌面图标。
- **静态可见性说明**：跳转与循环控制逻辑（Timer 35s、Settings.Secure 检测、MainActivity.a() 动态拼 Intent、JodampActivity 压栈/5s 自动关闭）在 DEX 中完整静态可见；但全部界面文案来自 assets/arakeem、assets/cfirraw 两个加密二进制（经 f.a(int) 索引解密），目标包名列表来自远端 URL（f.a(4530) 解密后 Base64+XOR 0x08），跳转 action/ComponentName 亦为整数数组运行期解密，故文案与远端配置未静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`LURE_PRIVACY_GUARANTEE_CLAIM`（主动抛出「绝不收集隐私/安全可靠」承诺）、`BENIGN_EXPLICIT_CANCEL_DEGRADATION`（提供显式取消/跳过且拒权后安全降级不循环）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d9bc87ab45b0c786aa09f964a8101f6df7ea76895e2e8438c13935a356d9116b` |
| 包名 / 年份 | `com.privacytitan.android` / 2021 |
| 家族 / 品类 | **Brata**（同池样本数：8） |
| 原始来源标识 | https://www.mcafee.com/blogs/other-blogs/mcafee-labs/brata-keeps-sneaking-into-google-play-now-targeting-usa-and-spain/?hilite=%27Android%27%2C%27Malware%27 |
| 桌面显示名 | Privacy Titan |
| 引导页宣称品牌/身份 | Privacy Titan（隐私保护/安全工具外壳），系统无障碍列表中伪装为“更新服务”（Serviço de Atualização） |
| 系统无障碍列表服务名 | Serviço de Atualização |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签与桌面名/功能宣称完全不一致（更新服务 vs 隐私工具）；service_iletes_cfg.xml 未声明 android:description，系统无障碍列表中不展示任何能力说明，掩盖 canRetrieveWindowContent 与 canPerformGestures 权限；服务 intent-filter priority=999 抢占；类名/字符串全量混淆（IletesSvc、JodampActivity、f.a(int) 整数数组解密）；获权后经反射 setComponentEnabledSetting 禁用启动组件隐藏图标；MainActivity 存在包名/签名校验（b.a().matches(f.a(1484))）与魔数开关（o.a("synolo")==1149306941）。 |
| 无障碍服务类名 | `com.privacytitan.IletesSvc` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `无` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.privacytitan.MainActivity（LAUNCHER，layout 2131361820） | onCreate 中 b.a().matches(f.a(1484)) 且 o.a("synolo")==1149306941 成立后设置按钮监听，并启动 MainActivity$c 线程拉取远端配置 | 原生Activity | **原文**：不可静态还原（TextView 2131165282 文本由 f.a(8378) 从加密 assets 解密）<br>**译注**：冷启动说明页，正文加密不可读；界面含一个取消按钮与一个继续按钮 | 点击继续（2131165311，MainActivity$b）或点击取消/关闭（2131165276，MainActivity$a → finish()），存在取消路径 | `com.privacytitan.MainActivity#onCreate / 布局资源 2131361820` |
| 2 | 业务功能触发 | MainActivity 继续按钮 → MainActivity$b.onClick | 用户点击继续按钮；写入 SharedPreferences("rathefa", true) 并 new Timer().schedule(MainActivity$d, 0L, 35000L) | 原生Activity | 无 | 仅需一次点击“继续”即视为同意，后续无需再交互 | `com.privacytitan.MainActivity$b#onClick` |
| 3 | 跳受限设置 | 系统无障碍设置页（或按 Build.MANUFACTURER 解密的厂商自定义设置 Activity） | MainActivity$d.run 每 35s 读取 Settings.Secure.enabled_accessibility_services，若本包组件未在列表中则 startActivity(MainActivity.a(ctx))，flags 0x10818000 | 系统无障碍页 | **原文**：不可静态还原（action 字符串与厂商 ComponentName 均为整数数组解密）<br>**译注**：直接跳到系统无障碍设置界面，用户需自行找到“更新服务”并打开开关 | 在系统列表中开启“Serviço de Atualização”开关；页面本身由系统提供，无应用内取消按钮 | `com.privacytitan.MainActivity$d#run → com.privacytitan.MainActivity#a` |
| 4 | 遮罩叠层指引 | com.privacytitan.JodampActivity（theme @7F0D00BC，taskAffinity 为空，layout 2131361821） | 上一步 startActivity 后 Thread.sleep(1000) 再 startActivity(JodampActivity)，叠在系统设置页之上 | 原生Activity | **原文**：Serviço de Atualização<br>**译注**：“更新服务”——页面标题/正文均取自加密 assets 与 strings 资源 2131492896，仅服务名可读；内容为分步操作指引 | 整块 FrameLayout（2131165245）可点击关闭；且 onResume postDelayed(5000) 后自动 finish()，用户仅约 5 秒阅读窗口 | `com.privacytitan.JodampActivity#onCreate / #onResume / JodampActivity$a#onClick / JodampActivity$b#run` |
| 5 | 拒权反馈循环 | MainActivity$d（Timer 35000ms 周期任务） | 用户返回或未开启开关 → z=false → 下一个 35s tick 再次 startActivity(设置页) 并再次压入 JodampActivity | 系统无障碍页 + 自有引导页叠加 | **原文**：无（复用第 3、4 步页面）<br>**译注**：每 35 秒重复“跳设置页 + 压引导页”，直到检测到本包组件出现在 enabled_accessibility_services 中 | 无退出机制：Timer 不因取消或返回而停止，只能通过开启无障碍结束循环 | `com.privacytitan.MainActivity$d#run` |
| 6 | 获权后动作 | com.privacytitan.IletesSvc（无障碍服务）→ IletesSvc$a 线程 → MainActivity.b(Context) | onServiceConnected 中读取 SharedPreferences("rathefa")==true 后起线程；反射调用 getComponentEnabledSetting 判断为 0 时 setComponentEnabledSetting(component, 2, 1) | 不可静态还原（无界面；后台反射禁用组件） | 无 | 无用户交互，全程后台完成 | `com.privacytitan.IletesSvc#onServiceConnected / com.privacytitan.MainActivity#b` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity（layout 2131361820）冷启动说明页：正文 TextView 2131165282 文本来自 f.a(8378)，从 assets/arakeem 或 cfirraw 解密读取，加密不可直读
- MainActivity 两个按钮：2131165276（取消，MainActivity$a → finish）、2131165311（继续，MainActivity$b → 启动 35s Timer）
- JodampActivity（layout 2131361821）叠在系统无障碍设置页之上的引导页：TextView 2131165272（f.a(9310) 格式化 + getString(2131492896)）、2131165285（f.a(8608)）、2131165314（2131492896）、2131165293（f.a(3387)），全部来自加密 assets 与 resources.arsc
- 系统无障碍服务列表项：service android:label=@7F0C0020 即 strings service_name="Serviço de Atualização"；service_iletes_cfg.xml 未提供 android:description，故列表内无能力说明文字
- 桌面启动器图标名称：application android:label=@7F0C001B = "Privacy Titan"
- 远端配置：MainActivity$c 从 f.a(4530) 解密出的 URL 下载文本，Base64 解码后再逐字符 XOR 0x08 得到 JSON 包名数组，用于判定本机是否已安装目标应用（无 UI 呈现）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | Serviço de Atualização | 更新服务 | `res/values/strings.xml key=service_name（resources.arsc 7F0C0020），被 IletesSvc android:label 与 JodampActivity TextView 2131165314 复用` | 假更新 |
| en | Privacy Titan | 隐私泰坦（隐私保护工具） | `resources.arsc application label 7F0C001B` | 隐私承诺 |
| pt | 不可静态还原（f.a(8378)，来源 assets/arakeem 或 assets/cfirraw 加密载荷） | MainActivity 冷启动说明正文，疑为“更新/安全提示”类话术（载体与调用点已确认，内容加密） | `com.privacytitan.MainActivity#onCreate 中 f.a(8378)；加密 assets 未还原` | 未知 |
| pt | 不可静态还原（f.a(9310)、f.a(8608)、f.a(3387) 与 string 2131492896） | JodampActivity 分步引导正文，围绕“更新服务”名义指导用户开启无障碍（内容加密） | `com.privacytitan.JodampActivity#onCreate；加密 assets 未还原` | 受限设置分步教学 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`True`
- **拒权或返回后的反馈回路**：一旦点击“继续”，Timer 以 0 延迟、35000ms 周期永久运行；每轮读取 Settings.Secure.enabled_accessibility_services，若本包组件不在列表中则立即 startActivity(无障碍设置页)，1 秒后再压入 JodampActivity 引导页（5 秒后自动 finish）。用户返回或拒绝不会取消 Timer，35 秒后再次重跳，形成无终止拒权循环；取消按钮仅 finish 当前 Activity，不影响已启动的 Timer。
- **遮罩叠层 / 高仿系统设置页**：不是仿冒设置页，而是真实拉起系统/厂商无障碍设置页，然后在 1 秒后把自有 JodampActivity（非悬浮窗、非透明，theme @7F0D00BC 的普通 Activity）压在其上充当指引遮罩，且该页 5 秒自动关闭，令用户反复看到“更新服务”开启指引。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion 29，未见引导进入应用详情开启“受限设置”或 Session 安装器绕过的代码；仅厂商自定义设置 ComponentName 兜底）
- **获权后即时行为与防撤权机制**：获权后 IletesSvc.onServiceConnected 起线程反射调用 PackageManager.setComponentEnabledSetting(MainActivity, COMPONENT_ENABLED_STATE_DISABLED(2), DONT_KILL_APP(1))，隐藏桌面启动图标防止用户卸载；未见监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码（onAccessibilityEvent 交由 a.a(4151,event)，本轮未展开）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两种时机：① 冷启动 MainActivity 出现“取消/继续”双按钮说明页时即拉起 UTG 并逐页截图；② Hook ActivityThread/Instrumentation 或监控 startActivity 调用，捕获 flags=0x10818000 且目标为系统无障碍设置页的跳转，以及随后 1000ms 内的 JodampActivity 启动，在设置页出现后 800–1200ms 抓取被压栈的引导页。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：界面全部文案位于 assets/arakeem、assets/cfirraw 两个加密二进制中，运行期才解密渲染，静态无法逐字比对话术；跳转 action 与厂商 ComponentName 亦为整数数组解密，需运行时 Hook 才能确认最终目标 Intent。此外 MainActivity 存在包名/签名校验与魔数开关（o.a("synolo")==1149306941），在非目标环境可能不进入引导链，UTG 需保证包名与签名一致；若冷启动 2 秒内出现的远端配置拉取失败，部分 UI 分支（MainActivity$c$b/$c$c）可能表现不同。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导弹窗/说明页** | com.privacytitan.MainActivity，双按钮布局（继续=2131165311，取消=2131165276），正文为加密 assets 解密文本 | 这是用户唯一可拒绝的节点，可直接区分“一次性透明说明”与“恶意诱导入口”，并记录拒绝后的行为分支 | 页面文本与无障碍/更新/权限是否相关；是否存在明确的取消/跳过按钮及按钮文案；点击取消后是否立即再次弹窗或起 Timer |
| **跳转前/跳转时的系统无障碍服务列表项** | 系统设置 → 无障碍 → 已安装服务中 label 为“Serviço de Atualização”的条目，无 description 副标题 | 该条目即最终要被打开的服务，其标签与桌面名（Privacy Titan）完全不符，是身份伪装最直接的可视证据 | 服务显示名 Serviço de Atualização；条目下方是否有能力说明（预期为空）；列表排序靠前（priority=999） |
| **设置页后压栈的自有引导遮罩页** | com.privacytitan.JodampActivity，整页可点、约 5 秒自动消失，内容含“更新服务/更新”类字样 | 证明应用在系统设置页之上主动叠层教学，且限时自动消失，是“遮罩叠层指引 + 拒权循环”的关键运行期证据 | 页面出现在系统无障碍设置之后约 1 秒；页面停留约 5 秒后自动返回设置页；再次返回桌面/退出后 35 秒内自动重跳设置页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.privacytitan.MainActivity#onCreate`
- `com.privacytitan.MainActivity$b#onClick`
- `com.privacytitan.MainActivity$d#run`
- `com.privacytitan.MainActivity#a`
- `com.privacytitan.JodampActivity#onCreate`
- `com.privacytitan.IletesSvc#onServiceConnected`
- `res/xml/service_iletes_cfg.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**静态可见性：代码主干清晰，但全部引导文案位于加密 assets 中，远端配置也未解析。**

**1. 引导链（已在代码中证实）**
- [MainActivity.onCreate()](<resource-unit:#1.dex1 code:com.privacytitan.MainActivity#onCreate>) 冷启动即 `setContentView`，正文由 `f.a(8378)` 从 assets 解密读取；随后在 `o.a("synolo")==1149306941` 与 `b.a().matches(f.a(1484))`（包签名/包名校验）同时成立时，为两个按钮挂监听：`2131165276 → MainActivity$a`（`finish()`，即取消）、`2131165311 → MainActivity$b`（同意继续）。同页另起线程 `MainActivity$c` 拉取远端 URL（`f.a(4530)`）→ Base64+XOR 0x08 → JSON 包名列表，判断本机是否已装目标 App（Brata 式目标识别）。
- 用户点“继续”后，[MainActivity$b.onClick()](<resource-unit:#1.dex1 code:com.privacytitan.MainActivity$b#onClick>) 写入 `SharedPreferences("rathefa")=true`，并启动 **35 秒周期** 的 `Timer`。
- [MainActivity$d.run()](<resource-unit:#1.dex1 code:com.privacytitan.MainActivity$d#run>) 每轮读取 `Settings.Secure.enabled_accessibility_services`（键名经整数数组解混淆）判断自身组件是否已启用；未启用则 `startActivity(MainActivity.a(ctx))` 跳设置页，`sleep(1000)` 后再 `startActivity(JodampActivity)` —— **在系统设置页之上压入自有引导 Activity**。
- [MainActivity.a()](<resource-unit:#1.dex1 code:com.privacytitan.MainActivity#a>) 动态拼装跳转：按 `Build.MANUFACTURER` 命中则用解密出的 `ComponentName`（厂商自定义无障碍/权限页）并 `queryIntentActivities` 探测可用性，否则退回解密出的 action 字符串构造 Intent，flags `0x10818000`（NEW_TASK）。**DEX 中无明文的 `ACTION_ACCESSIBILITY_SETTINGS`/`APPLICATION_DETAILS_SETTINGS`**，全部为运行期解密。
- [JodampActivity.onCreate()](<resource-unit:#1.dex1 code:com.privacytitan.JodampActivity#onCreate>) 为纯文本教学页（4 个 TextView 全部来自加密 assets + `getString(2131492896)`），整块 FrameLayout 可点关闭；[onResume()](<resource-unit:#1.dex1 code:com.privacytitan.JodampActivity#onResume>) 中 `postDelayed(5000)` 自动 `finish()` —— **5 秒自动消失的“看完就走”遮罩页**，正好叠在被拉起的设置页上。
- 拒绝/返回后无降级：Timer 不取消，35 秒后重新跳设置页并再次压栈引导页，形成拒权循环。

**2. 身份伪装**
- 桌面名 `Privacy Titan`（隐私承诺型外壳），而无障碍服务标签为 [Serviço de Atualização](<resource-unit:#1 file:res/xml/service_iletes_cfg.xml>)（葡语“更新服务”），且 a11y 配置**无 `android:description`**，系统列表只剩一行“更新服务”，用户无从得知其读屏/手势能力（配置声明 `canRetrieveWindowContent`、`canPerformGestures`）。
- 获权后 [IletesSvc.onServiceConnected()](<resource-unit:#1.dex1 code:com.privacytitan.IletesSvc#onServiceConnected>) 校验 `rathefa` 后起线程，经反射调用 `setComponentEnabledSetting(..., 2, 1)` 将 MainActivity 组件禁用（`MainActivity.b()`），**授予无障碍后隐藏启动图标**，防卸载/防复查。

**3. 证据边界**
- `assets/arakeem`、`assets/cfirraw` 为加密二进制（2.8KB 级），`f.a(int)` 索引解密读取；本次未还原，故 MainActivity / JodampActivity 的**具体引导原文无法逐字引用**，仅能确认载体与结构。
- `onAccessibilityEvent → a.a(4151, event)` 的后续滥用逻辑（读屏、点击注入）不在本轮 UTG 专题范围内，未展开。

---

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "跳转与循环控制逻辑（Timer 35s、Settings.Secure 检测、MainActivity.a() 动态拼 Intent、JodampActivity 压栈/5s 自动关闭）在 DEX 中完整静态可见；但全部界面文案来自 assets/arakeem、assets/cfirraw 两个加密二进制（经 f.a(int) 索引解密），目标包名列表来自远端 URL（f.a(4530) 解密后 Base64+XOR 0x08），跳转 action/ComponentName 亦为整数数组运行期解密，故文案与远端配置未静态还原。",
  "summary_one_liner": "以“Privacy Titan/隐私工具”为外壳、无障碍服务伪装成葡语“更新服务”，冷启动弹说明页诱导点击后启动 35 秒定时器：检测到未授权即跳系统无障碍页并在其上压入 5 秒自动消失的自有引导页，循环往复直至授权，授权后反射隐藏桌面图标。",
  "disguise_identity": {
    "app_display_name": "Privacy Titan",
    "claimed_brand_or_persona": "Privacy Titan（隐私保护/安全工具外壳），系统无障碍列表中伪装为“更新服务”（Serviço de Atualização）",
    "a11y_service_label": "Serviço de Atualização",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签与桌面名/功能宣称完全不一致（更新服务 vs 隐私工具）；service_iletes_cfg.xml 未声明 android:description，系统无障碍列表中不展示任何能力说明，掩盖 canRetrieveWindowContent 与 canPerformGestures 权限；服务 intent-filter priority=999 抢占；类名/字符串全量混淆（IletesSvc、JodampActivity、f.a(int) 整数数组解密）；获权后经反射 setComponentEnabledSetting 禁用启动组件隐藏图标；MainActivity 存在包名/签名校验（b.a().matches(f.a(1484))）与魔数开关（o.a(\"synolo\")==1149306941）。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.privacytitan.MainActivity（LAUNCHER，layout 2131361820）",
      "trigger_event": "onCreate 中 b.a().matches(f.a(1484)) 且 o.a(\"synolo\")==1149306941 成立后设置按钮监听，并启动 MainActivity$c 线程拉取远端配置",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "不可静态还原（TextView 2131165282 文本由 f.a(8378) 从加密 assets 解密）",
      "shown_text_zh": "冷启动说明页，正文加密不可读；界面含一个取消按钮与一个继续按钮",
      "user_action_requested": "点击继续（2131165311，MainActivity$b）或点击取消/关闭（2131165276，MainActivity$a → finish()），存在取消路径",
      "code_anchor": "com.privacytitan.MainActivity#onCreate / 布局资源 2131361820"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "MainActivity 继续按钮 → MainActivity$b.onClick",
      "trigger_event": "用户点击继续按钮；写入 SharedPreferences(\"rathefa\", true) 并 new Timer().schedule(MainActivity$d, 0L, 35000L)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无",
      "shown_text_zh": "点击后页面无新文案，转入后台 35 秒周期轮询",
      "user_action_requested": "仅需一次点击“继续”即视为同意，后续无需再交互",
      "code_anchor": "com.privacytitan.MainActivity$b#onClick"
    },
    {
      "step": 3,
      "stage": "跳受限设置",
      "screen_or_component": "系统无障碍设置页（或按 Build.MANUFACTURER 解密的厂商自定义设置 Activity）",
      "trigger_event": "MainActivity$d.run 每 35s 读取 Settings.Secure.enabled_accessibility_services，若本包组件未在列表中则 startActivity(MainActivity.a(ctx))，flags 0x10818000",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "不可静态还原（action 字符串与厂商 ComponentName 均为整数数组解密）",
      "shown_text_zh": "直接跳到系统无障碍设置界面，用户需自行找到“更新服务”并打开开关",
      "user_action_requested": "在系统列表中开启“Serviço de Atualização”开关；页面本身由系统提供，无应用内取消按钮",
      "code_anchor": "com.privacytitan.MainActivity$d#run → com.privacytitan.MainActivity#a"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.privacytitan.JodampActivity（theme @7F0D00BC，taskAffinity 为空，layout 2131361821）",
      "trigger_event": "上一步 startActivity 后 Thread.sleep(1000) 再 startActivity(JodampActivity)，叠在系统设置页之上",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Serviço de Atualização",
      "shown_text_zh": "“更新服务”——页面标题/正文均取自加密 assets 与 strings 资源 2131492896，仅服务名可读；内容为分步操作指引",
      "user_action_requested": "整块 FrameLayout（2131165245）可点击关闭；且 onResume postDelayed(5000) 后自动 finish()，用户仅约 5 秒阅读窗口",
      "code_anchor": "com.privacytitan.JodampActivity#onCreate / #onResume / JodampActivity$a#onClick / JodampActivity$b#run"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity$d（Timer 35000ms 周期任务）",
      "trigger_event": "用户返回或未开启开关 → z=false → 下一个 35s tick 再次 startActivity(设置页) 并再次压入 JodampActivity",
      "ui_carrier": "系统无障碍页 + 自有引导页叠加",
      "shown_text_verbatim": "无（复用第 3、4 步页面）",
      "shown_text_zh": "每 35 秒重复“跳设置页 + 压引导页”，直到检测到本包组件出现在 enabled_accessibility_services 中",
      "user_action_requested": "无退出机制：Timer 不因取消或返回而停止，只能通过开启无障碍结束循环",
      "code_anchor": "com.privacytitan.MainActivity$d#run"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "com.privacytitan.IletesSvc（无障碍服务）→ IletesSvc$a 线程 → MainActivity.b(Context)",
      "trigger_event": "onServiceConnected 中读取 SharedPreferences(\"rathefa\")==true 后起线程；反射调用 getComponentEnabledSetting 判断为 0 时 setComponentEnabledSetting(component, 2, 1)",
      "ui_carrier": "不可静态还原（无界面；后台反射禁用组件）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "授予无障碍后静默隐藏桌面启动图标，应用从桌面消失以防用户卸载/复查；此后 onAccessibilityEvent 交由 a.a(4151, event) 处理读屏与手势",
      "user_action_requested": "无用户交互，全程后台完成",
      "code_anchor": "com.privacytitan.IletesSvc#onServiceConnected / com.privacytitan.MainActivity#b"
    }
  ],
  "text_presentation_locations": [
    "MainActivity（layout 2131361820）冷启动说明页：正文 TextView 2131165282 文本来自 f.a(8378)，从 assets/arakeem 或 cfirraw 解密读取，加密不可直读",
    "MainActivity 两个按钮：2131165276（取消，MainActivity$a → finish）、2131165311（继续，MainActivity$b → 启动 35s Timer）",
    "JodampActivity（layout 2131361821）叠在系统无障碍设置页之上的引导页：TextView 2131165272（f.a(9310) 格式化 + getString(2131492896)）、2131165285（f.a(8608)）、2131165314（2131492896）、2131165293（f.a(3387)），全部来自加密 assets 与 resources.arsc",
    "系统无障碍服务列表项：service android:label=@7F0C0020 即 strings service_name=\"Serviço de Atualização\"；service_iletes_cfg.xml 未提供 android:description，故列表内无能力说明文字",
    "桌面启动器图标名称：application android:label=@7F0C001B = \"Privacy Titan\"",
    "远端配置：MainActivity$c 从 f.a(4530) 解密出的 URL 下载文本，Base64 解码后再逐字符 XOR 0x08 得到 JSON 包名数组，用于判定本机是否已安装目标应用（无 UI 呈现）"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "Serviço de Atualização",
      "text_zh": "更新服务",
      "source_location": "res/values/strings.xml key=service_name（resources.arsc 7F0C0020），被 IletesSvc android:label 与 JodampActivity TextView 2131165314 复用",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Privacy Titan",
      "text_zh": "隐私泰坦（隐私保护工具）",
      "source_location": "resources.arsc application label 7F0C001B",
      "rhetorical_frame": "隐私承诺"
    },
    {
      "lang": "pt",
      "text_verbatim": "不可静态还原（f.a(8378)，来源 assets/arakeem 或 assets/cfirraw 加密载荷）",
      "text_zh": "MainActivity 冷启动说明正文，疑为“更新/安全提示”类话术（载体与调用点已确认，内容加密）",
      "source_location": "com.privacytitan.MainActivity#onCreate 中 f.a(8378)；加密 assets 未还原",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "不可静态还原（f.a(9310)、f.a(8608)、f.a(3387) 与 string 2131492896）",
      "text_zh": "JodampActivity 分步引导正文，围绕“更新服务”名义指导用户开启无障碍（内容加密）",
      "source_location": "com.privacytitan.JodampActivity#onCreate；加密 assets 未还原",
      "rhetorical_frame": "受限设置分步教学"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": true,
    "refusal_loop_mechanism": "一旦点击“继续”，Timer 以 0 延迟、35000ms 周期永久运行；每轮读取 Settings.Secure.enabled_accessibility_services，若本包组件不在列表中则立即 startActivity(无障碍设置页)，1 秒后再压入 JodampActivity 引导页（5 秒后自动 finish）。用户返回或拒绝不会取消 Timer，35 秒后再次重跳，形成无终止拒权循环；取消按钮仅 finish 当前 Activity，不影响已启动的 Timer。",
    "overlay_or_fake_settings": "不是仿冒设置页，而是真实拉起系统/厂商无障碍设置页，然后在 1 秒后把自有 JodampActivity（非悬浮窗、非透明，theme @7F0D00BC 的普通 Activity）压在其上充当指引遮罩，且该页 5 秒自动关闭，令用户反复看到“更新服务”开启指引。",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion 29，未见引导进入应用详情开启“受限设置”或 Session 安装器绕过的代码；仅厂商自定义设置 ComponentName 兜底）",
    "post_grant_anti_removal": "获权后 IletesSvc.onServiceConnected 起线程反射调用 PackageManager.setComponentEnabledSetting(MainActivity, COMPONENT_ENABLED_STATE_DISABLED(2), DONT_KILL_APP(1))，隐藏桌面启动图标防止用户卸载；未见监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码（onAccessibilityEvent 交由 a.a(4151,event)，本轮未展开）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两种时机：① 冷启动 MainActivity 出现“取消/继续”双按钮说明页时即拉起 UTG 并逐页截图；② Hook ActivityThread/Instrumentation 或监控 startActivity 调用，捕获 flags=0x10818000 且目标为系统无障碍设置页的跳转，以及随后 1000ms 内的 JodampActivity 启动，在设置页出现后 800–1200ms 抓取被压栈的引导页。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导弹窗/说明页",
        "page_identifier": "com.privacytitan.MainActivity，双按钮布局（继续=2131165311，取消=2131165276），正文为加密 assets 解密文本",
        "why_most_useful": "这是用户唯一可拒绝的节点，可直接区分“一次性透明说明”与“恶意诱导入口”，并记录拒绝后的行为分支",
        "observable_utg_signals": ["页面文本与无障碍/更新/权限是否相关", "是否存在明确的取消/跳过按钮及按钮文案", "点击取消后是否立即再次弹窗或起 Timer"]
      },
      {
        "page_role": "跳转前/跳转时的系统无障碍服务列表项",
        "page_identifier": "系统设置 → 无障碍 → 已安装服务中 label 为“Serviço de Atualização”的条目，无 description 副标题",
        "why_most_useful": "该条目即最终要被打开的服务，其标签与桌面名（Privacy Titan）完全不符，是身份伪装最直接的可视证据",
        "observable_utg_signals": ["服务显示名 Serviço de Atualização", "条目下方是否有能力说明（预期为空）", "列表排序靠前（priority=999）"]
      },
      {
        "page_role": "设置页后压栈的自有引导遮罩页",
        "page_identifier": "com.privacytitan.JodampActivity，整页可点、约 5 秒自动消失，内容含“更新服务/更新”类字样",
        "why_most_useful": "证明应用在系统设置页之上主动叠层教学，且限时自动消失，是“遮罩叠层指引 + 拒权循环”的关键运行期证据",
        "observable_utg_signals": ["页面出现在系统无障碍设置之后约 1 秒", "页面停留约 5 秒后自动返回设置页", "再次返回桌面/退出后 35 秒内自动重跳设置页"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：界面全部文案位于 assets/arakeem、assets/cfirraw 两个加密二进制中，运行期才解密渲染，静态无法逐字比对话术；跳转 action 与厂商 ComponentName 亦为整数数组解密，需运行时 Hook 才能确认最终目标 Intent。此外 MainActivity 存在包名/签名校验与魔数开关（o.a(\"synolo\")==1149306941），在非目标环境可能不进入引导链，UTG 需保证包名与签名一致；若冷启动 2 秒内出现的远端配置拉取失败，部分 UI 分支（MainActivity$c$b/$c$c）可能表现不同。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "LURE_PRIVACY_GUARANTEE_CLAIM",
    "BENIGN_EXPLICIT_CANCEL_DEGRADATION"
  ],
  "code_anchors": [
    "com.privacytitan.MainActivity#onCreate",
    "com.privacytitan.MainActivity$b#onClick",
    "com.privacytitan.MainActivity$d#run",
    "com.privacytitan.MainActivity#a",
    "com.privacytitan.JodampActivity#onCreate",
    "com.privacytitan.IletesSvc#onServiceConnected",
    "res/xml/service_iletes_cfg.xml"
  ]
}
```

**说明**：本轮为定向 UTG 视角核验，聚焦引导链与跳转机制；`IletesSvc.onAccessibilityEvent → a.a(4151, event)` 的读屏/点击注入滥用逻辑与远端配置内容（`f.a(4530)`）未展开，且因效率约束未写入项目风险台账，如需可按上述锚点续查。

</details>
