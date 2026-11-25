# MR_121__b015c99ad5｜Ghimob — Instale - Adobe reader

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：172.8s

## 1. 一句话核心结论

- **核心申请方式**：应用伪装成 'Instale - Adobe reader'，冷启动即在 onResume 中检测无障碍未开启并无任何说明页地直接 startActivityForResult 跳转系统无障碍设置，用户返回未授权就由 onActivityResult(333→20) 重跳，并辅以常驻通知与 30 分钟定时器形成无取消路径的强制授权循环。
- **静态可见性说明**：Manifest、无障碍配置、跳转与循环控制流全部静态可见；界面/系统参数文案并非明文，而是以自定义算法加密存放于 resources.arsc（Base64 + 双字母编码 + 动态 key，由 x.b.u/D 解密），本轮已用脚本完整还原为可读葡语/系统标识串，故不属于动态或远端隐藏。未发现 WebView 远端 HTML、二次载荷或加壳（apkid 仅报 r8 编译与反调试/反虚拟机特征）。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b015c99ad510c766d7fed64aa18f1ff9a7321f062e9c6d2912144168897d166b` |
| 包名 / 年份 | `com.sysdroidxx.addons` / 2020 |
| 家族 / 品类 | **Ghimob**（同池样本数：4） |
| 原始来源标识 | https://securelist.com/ghimob-tetrade-threat-mobile-devices/99228/ |
| 桌面显示名 | Instale - Adobe reader |
| 引导页宣称品牌/身份 | Adobe Reader（PDF 阅读器）；应用内不含任何 PDF/阅读器实现，实际为巴西银行定向凭据窃取木马（Ghimob 家族） |
| 系统无障碍列表服务名 | 系统无障碍列表中以应用标签 'Instale - Adobe reader' 呈现（服务无独立 android:label，res/xml/serg.xml 的 description 值为空，无任何用途说明） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置 description 留空以在系统列表中抹去用途说明；android:label 指向 @7F0B0098 伪装成 Adobe reader；所有字符串资源以自定义 Base64+双字母编码加密，运行时按 x.b.D(context, index) 逐条解密，静态直接读 arsc 只能看到密文；类名与包名强混淆（mok / a3k / x.b / yff / r0st）；集成 Debug.isDebuggerConnected、可调试标志与 Build.* 模拟器指纹检测（mok.l()），命中即 killProcess 退出；使用 com.intelsyss/plugins 这类与包名无关的组件串作为跳转目标 |
| 无障碍服务类名 | `com.sysdroidxx.addons.a3k` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |
| 系统设置项说明 (`android:description`) | Instale - Adobe reader |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.sysdroidxx.addons.mok（MAIN/LAUNCHER Activity） | onCreate()：先执行 mok.l() 模拟器/调试器检测，命中即 finish+killProcess；通过后 setContentView(2131296283)，将两个按钮 setVisibility(8)，注册 1800000ms 周期 Timer(mok$a) | 原生Activity | **原文**：Instale - Adobe reader<br>**译注**：界面仅显示应用标题“安装 - Adobe 阅读器”，无任何说明文字与可操作业务控件（按钮被置为不可见） | 无需操作，界面无可用功能；无跳过/取消按钮 | `com.sysdroidxx.addons.mok.onCreate` |
| 2 | 冷启动入口 | com.sysdroidxx.addons.mok.onResume + 通知栏常驻通知 | onResume()：mok.o() 读取 Settings.Secure 的 accessibility_enabled 与 ENABLED_ACCESSIBILITY_SERVICES，未包含 com.sysdroidxx.addons/com.sysdroidxx.addons.a3k 时调用 x.b.I() 构造指向 mok 的 PendingIntent 通知（渠道 id 由 D(27)+111100 生成） | 通知栏 | **原文**：无（通知标题/内容取自加密串 b.D(this,26)/D(this,28)，解密表内为葡语运维文案，本轮未确认其确切索引对应文本）<br>**译注**：常驻通知用于把用户反复拉回主 Activity，本身不承载说明文字 | 点击通知即回到 mok，再次触发跳转；通知无取消入口 | `com.sysdroidxx.addons.mok.onResume / x.b.I` |
| 3 | 跳无障碍设置 | 系统无障碍设置页（component 目标：com.android.settings.Settings$AccessibilityInstalledServiceActivity；兜底 action：android.settings.ACCESSIBILITY_SETTINGS） | onResume() 中 new Intent(b.D(this,20)).setAction(b.D(this,12)).setComponent(new ComponentName(b.D(this,13), b.D(this,14))) 后 startActivityForResult(intent, 333)；异常时回退为仅 setAction(b.D(this,21)) 的 Intent | 系统无障碍页 | **原文**：Instale - Adobe reader（系统列表项名称；description 为空）<br>**译注**：用户被直接带入系统无障碍服务列表，看到唯一可选项名称为伪装身份，且没有任何功能说明 | 要求用户点开该项并把开关拨到开启；页面无应用侧取消/跳过按钮，只能靠系统返回键退出 | `com.sysdroidxx.addons.mok.onResume / x.b.D` |
| 4 | 拒权反馈循环 | mok.onActivityResult(333, resultCode, intent) → 再次拉起同一系统设置页 | 用户在设置页返回/未开启（resultCode != RESULT_OK）时，新建 Intent setFlags(32768=FLAG_ACTIVITY_NEW_TASK) + setAction(b.D(this,21))，startActivityForResult(..., 20)；mok 未 finish，回到前台即再次走 onResume 重跳 | 系统无障碍页 | 无 | 只能反复返回或最终开启开关，应用不提供任何“稍后再说/跳过”路径 | `com.sysdroidxx.addons.mok.onActivityResult` |
| 5 | 获权后动作 | com.sysdroidxx.addons.a3k（无障碍服务 onServiceConnected） | mok.o() 返回 true → 隐藏视图并 finish()；系统绑定 a3k 后 onServiceConnected() 设置 eventTypes=-1、flags=119 监听全部事件，并调用 performGlobalAction 返回主屏 | 悬浮窗Overlay | **原文**：Cliente: / Modo Seguro / Restaurar dados / Redefina seu telefone / Fazer backup dos dados / Link Conexao;<br>**译注**：“客户：”/“安全模式”/“恢复数据”/“重置您的手机”/“备份数据”/“连接链接”等葡语遮罩与操作提示，用于在目标银行应用上覆盖伪造界面并读取窗口内容 | 诱使受害者在被覆盖的银行/密码界面上继续输入（此阶段已非权限引导） | `com.sysdroidxx.addons.a3k.onServiceConnected / com.sysdroidxx.addons.a3k.g` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 桌面图标与系统无障碍列表项名称：android:label=@7F0B0098 → 'Instale - Adobe reader'（Manifest 声明）
- 系统无障碍服务详情/列表说明：res/xml/serg.xml 的 android:description 值为空，列表内不呈现任何用途说明文字
- 应用主界面 com.sysdroidxx.addons.mok：仅 setContentView(2131296283) 的标题级界面，两个按钮 setVisibility(8) 隐藏，无说明文案、无 WebView、无引导弹窗
- 通知栏常驻通知（x.b.I）：文案取自加密串 b.D(context,26)/D(context,28)，用途为拉回 mok 而非说明
- 系统无障碍设置页：由应用跳转后由系统呈现，应用侧无叠加引导遮罩
- 获权后 a3k 悬浮窗（WindowManager FrameLayout，经 x.b.u 解密的葡语文本）：Cliente: / Modo Seguro / Restaurar dados 等，属于窃取阶段而非引导阶段
- 加密资源载体：全部界面/系统参数文本存放于 resources.arsc 的 string 池，经 x.b.u（Base64→双字母编码→减 seed 与 key）解密，明文不在包内直接可读

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Instale - Adobe reader | 安装 - Adobe 阅读器 | `resources.arsc string @7F0B0098（Manifest android:label / application 显示名，明文未加密）` | 清理工具伪装 |
| none | （空字符串） | 无障碍服务描述为空，系统列表中不显示任何用途说明 | `res/xml/serg.xml android:description（加密态资源，解析后为空值）` | 教唆忽视警告 |
| pt | Cliente: | 客户： | `resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）` | 未知 |
| pt | Modo Seguro | 安全模式 | `resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）` | 假反诈安全 |
| pt | Restaurar dados | 恢复数据 | `resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）` | 未知 |
| pt | Redefina seu telefone | 重置您的手机 | `resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）` | 故障恐吓 |
| pt | Fazer backup dos dados | 备份数据 | `resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）` | 未知 |
| pt | Link Conexao; | 连接链接; | `resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）` | 未知 |
| en | com.android.settings.Settings$AccessibilityInstalledServiceActivity | 系统无障碍“已安装的服务”设置页组件名（作为跳转 component 使用的解密串） | `resources.arsc 加密 string，经 x.b.u 解密` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：mok 在未授权时从不 finish()：onResume 每次回到前台都重新 startActivityForResult(intent, 333) 跳系统无障碍设置；用户在设置页返回（resultCode != RESULT_OK）时 onActivityResult 立即以 FLAG_ACTIVITY_NEW_TASK + action b.D(21) 再次 startActivityForResult(..., 20) 重跳；此外 onCreate 注册 1800000ms 周期 Timer(mok$a) 定时再拉起，onResume 每次调用 x.b.I() 保持指向 mok 的常驻通知供点击拉活，三重叠加构成无取消路径的拒权循环。
- **遮罩叠层 / 高仿系统设置页**：本轮静态未见应用侧半透明引导遮罩或高仿系统无障碍开关页；引导完全依赖跳转真实系统设置页，仅靠 android:label 伪装与空 description 隐去用途。悬浮窗（SYSTEM_ALERT_WINDOW）能力在获权后由 a3k.g() 用于覆盖目标银行应用，而非用于权限引导。
- **Android 13+ 受限设置（Restricted Settings）应对**：无。targetSdkVersion=27，无需“受限设置”教学；未见应用详情页→右上角菜单→允许受限设置的分步文案，也未见 Session 安装器绕过。解密串中仅出现系统无障碍设置组件名与 com.intelsyss/plugins/... 组件串。
- **获权后即时行为与防撤权机制**：获权后 a3k.onServiceConnected() 以 performGlobalAction(GLOBAL_ACTION_HOME/BACK) 立即离开系统设置页（DEX 线索 anti_removal=PERFORM_GLOBAL_ACTION 与之对应）；本轮未在已读分支中发现监听设置页、自动点确认或持续阻止撤权的显式逻辑（a3k 其余分支未逐条展开）。
- **良性降级 / 替代方案**：无。未授权时既无手动模式、无仅观看模式、也无任何功能降级说明，界面唯一出路是开启无障碍或退出应用。

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：纯 UTG 检测应在两处拉起：①冷启动后监测 com.sysdroidxx.addons.mok 的 startActivityForResult(intent, 333)（intent action=android.settings.ACCESSIBILITY_SETTINGS 或 component=com.android.settings.Settings$AccessibilityInstalledServiceActivity）瞬间；②用户从系统设置页返回时监测 onActivityResult(333, resultCode!=RESULT_OK) 触发的第二次 startActivityForResult(..., 20)，以确认拒权重跳。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无显著盲区：引导阶段不含图片或纯图空文本，全部判别信号为 Activity 跳转序列 + 系统设置页文本 + 空 description。唯一需注意的是所有界面/参数文案以自定义 Base64+双字母编码加密存放于 resources.arsc，纯静态 grep 明文会一无所获（本轮已用解密脚本还原）；另有反模拟器/反调试检测（mok.l() 命中即 killProcess），在模拟器或可调试环境下可能看不到任何界面，UTG 检测应优先使用真机。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首个界面（mok 主 Activity）** | 包名 com.sysdroidxx.addons，Activity com.sysdroidxx.addons.mok，标题 'Instale - Adobe reader'，页面无可见按钮（两按钮 GONE） | 确认引导是 0 步直跳：没有任何业务功能与说明页，直接暴露伪装的空壳主界面 | 当前 Activity 为 com.sysdroidxx.addons.mok；页面可见控件数为 0（按钮 visibility=gone）；界面文本仅 'Instale - Adobe reader' |
| **系统无障碍服务列表项** | Settings 无障碍页（Settings$AccessibilityInstalledServiceActivity 或 ACCESSIBILITY_SETTINGS），列表项文本 'Instale - Adobe reader' 且无副标题/说明 | 是判定“服务说明为空 + 名称伪装”的关键：恶意样本借此让用户在无用途说明下开启高权限服务 | 列表项文本 = 'Instale - Adobe reader'；该项无 description 副文本；页面由 com.sysdroidxx.addons 跳转进入（前一个 Activity 为 mok） |
| **拒权返回后的重跳页（与系统无障碍页同构，但出现次数 ≥2）** | 同一系统无障碍页在短时间内被重复拉起，且中间无用户主动点击、无应用内中间页 | 直接量化“返回即重跳”的强制循环强度，是最强的诱导证据 | 同一 AccessibilitySettings 页在 <5s 内第二次出现；两次跳转之间 mok 未 finish（仍在任务栈）；存在指向 mok 的常驻通知 |
| **获权后覆盖在目标应用上的悬浮窗** | a3k 服务运行中，WindowManager 覆盖的 FrameLayout，含 'Cliente:' / 'Modo Seguro' 等葡语文本 | 验证授权目的：无障碍能力被用于覆盖与读取银行类窗口内容，而非无障碍辅助 | 无障碍服务 com.sysdroidxx.addons.a3k 处于 enabled 状态；前台出现非本应用包名的覆盖层节点；覆盖层文本为葡语银行操作引导 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.sysdroidxx.addons.mok.onResume`
- `com.sysdroidxx.addons.mok.onActivityResult`
- `com.sysdroidxx.addons.mok.o`
- `com.sysdroidxx.addons.mok.l`
- `x.b.D`
- `res/xml/serg.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（UTG 运行期视角）

**核心判断：这是一个不展示任何说明或教学页、冷启动即强制跳转系统无障碍设置的“零文案引导”样本**（葡语 Ghimob 变种，实际面向巴西银行凭据）。全部逻辑静态可见；资源中字符串经自定义加密（Base64 + 双字母编码 + 动态 key），本次已用脚本还原。

1. **入口**：[mok.onCreate()](<resource-unit:#1.dex1 code:com.sysdroidxx.addons.mok#onCreate>) 是唯一的 LAUNCHER Activity。它先运行 [mok.l()](<resource-unit:#1.dex1 code:com.sysdroidxx.addons.mok#l>) 进行模拟器、调试器和可调试包检测，命中后直接结束进程；随后调用 `setContentView`，把两个按钮隐藏为 `GONE`，并注册 30 分钟周期的 `Timer`（`mok$a`）。界面不提供任何业务功能。
2. **判定与跳转**：[mok.onResume()](<resource-unit:#1.dex1 code:com.sysdroidxx.addons.mok#onResume>) 调用 [mok.o()](<resource-unit:#1.dex1 code:com.sysdroidxx.addons.mok#o>) 读取 `Settings.Secure` 中的 `accessibility_enabled`（解密串 `bddfttjcjmjuz\`fobcmfe`）与 `ENABLED_ACCESSIBILITY_SERVICES`，比对 `com.sysdroidxx.addons/com.sysdroidxx.addons.a3k`。若未授权，先通过 [x.b.I()](<resource-unit:#1.dex1 code:x.b#I>) 发送常驻通知（`PendingIntent` 指回 `mok`），再调用 `startActivityForResult(intent, 333)`；该 intent 的 action 和 component 全部由 [x.b.D()](<resource-unit:#1.dex1 code:x.b#D>) 在运行时解密取得。
3. **跳转目标**：解密串表中包含 `com.android.settings.Settings$AccessibilityInstalledServiceActivity` 与 `com.intelsyss/plugins/com.intelsyss/plugins/a3y`，它们被用作 component 目标。catch 分支回退为仅设置 action 的 Intent（即系统无障碍设置），没有其它业务页。这意味着引导就是“直接把用户推进系统设置”。
4. **拒绝后的循环**：[mok.onActivityResult()](<resource-unit:#1.dex1 code:com.sysdroidxx.addons.mok#onActivityResult>) 在 `requestCode==333` 且结果非 `RESULT_OK` 时，会新建带 `FLAG_ACTIVITY_NEW_TASK` 的 Intent，再次调用 `startActivityForResult(..., 20)`。由于 `mok` 在未授权时从不 `finish()`，`onResume` 每次回到前台都会重跳；再叠加 30 分钟 `Timer` 与通知栏拉活，用户没有取消或跳过路径。
5. **唯一“文案”载体**：`android:label="Instale - Adobe reader"`（`@7F0B0098`），而无障碍配置 [res/xml/serg.xml](<resource-unit:#1 file:res/xml/serg.xml>) 只声明 `canRetrieveWindowContent` / `canPerformGestures`，`description` 值为空。因此系统无障碍列表中该服务没有任何用途说明，只剩一个伪装成 PDF 阅读器的名称。应用内没有 WebView、没有说明弹窗、没有引导图。葡语原文（`Cliente:`、`Modo Seguro`、`Restaurar dados`、`Redefina seu telefone`、`Fazer backup dos dados`、`Link Conexao;`）属于获权后 a3k 侧悬浮窗和窃取界面的文案，不是引导文案。
6. **获权后**：`o()` 返回真后隐藏视图并调用 `finish()`；`a3k.onServiceConnected()` 监听全部事件，并通过 `performGlobalAction` 离开设置页，后续绘制悬浮窗窃取。

**风险记录**：该命题与既有 [R-001](<resource-unit:#1 manifest:components>)（source_mode=`autonomous_audit`）实质同一命题，本轮不重复登记；本轮补充的是文案层证据（描述为空、资源加密可静态解密）与 `onActivityResult` 精确的 requestCode 20/333 循环结构。

**覆盖边界**：`a3k` 内部各 `g()`/`r()` 分支（含是否监听设置页阻止撤权）未逐条展开；未启动动态分析（静态证据已闭合）。

```json
{
  "static_visibility": "clear",
  "visibility_note": "Manifest、无障碍配置、跳转与循环控制流全部静态可见；界面/系统参数文案并非明文，而是以自定义算法加密存放于 resources.arsc（Base64 + 双字母编码 + 动态 key，由 x.b.u/D 解密），本轮已用脚本完整还原为可读葡语/系统标识串，故不属于动态或远端隐藏。未发现 WebView 远端 HTML、二次载荷或加壳（apkid 仅报 r8 编译与反调试/反虚拟机特征）。",
  "summary_one_liner": "应用伪装成 'Instale - Adobe reader'，冷启动即在 onResume 中检测无障碍未开启并无任何说明页地直接 startActivityForResult 跳转系统无障碍设置，用户返回未授权就由 onActivityResult(333→20) 重跳，并辅以常驻通知与 30 分钟定时器形成无取消路径的强制授权循环。",
  "disguise_identity": {
    "app_display_name": "Instale - Adobe reader",
    "claimed_brand_or_persona": "Adobe Reader（PDF 阅读器）；应用内不含任何 PDF/阅读器实现，实际为巴西银行定向凭据窃取木马（Ghimob 家族）",
    "a11y_service_label": "系统无障碍列表中以应用标签 'Instale - Adobe reader' 呈现（服务无独立 android:label，res/xml/serg.xml 的 description 值为空，无任何用途说明）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置 description 留空以在系统列表中抹去用途说明；android:label 指向 @7F0B0098 伪装成 Adobe reader；所有字符串资源以自定义 Base64+双字母编码加密，运行时按 x.b.D(context, index) 逐条解密，静态直接读 arsc 只能看到密文；类名与包名强混淆（mok / a3k / x.b / yff / r0st）；集成 Debug.isDebuggerConnected、可调试标志与 Build.* 模拟器指纹检测（mok.l()），命中即 killProcess 退出；使用 com.intelsyss/plugins 这类与包名无关的组件串作为跳转目标"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.sysdroidxx.addons.mok（MAIN/LAUNCHER Activity）",
      "trigger_event": "onCreate()：先执行 mok.l() 模拟器/调试器检测，命中即 finish+killProcess；通过后 setContentView(2131296283)，将两个按钮 setVisibility(8)，注册 1800000ms 周期 Timer(mok$a)",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Instale - Adobe reader",
      "shown_text_zh": "界面仅显示应用标题“安装 - Adobe 阅读器”，无任何说明文字与可操作业务控件（按钮被置为不可见）",
      "user_action_requested": "无需操作，界面无可用功能；无跳过/取消按钮",
      "code_anchor": "com.sysdroidxx.addons.mok.onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.sysdroidxx.addons.mok.onResume + 通知栏常驻通知",
      "trigger_event": "onResume()：mok.o() 读取 Settings.Secure 的 accessibility_enabled 与 ENABLED_ACCESSIBILITY_SERVICES，未包含 com.sysdroidxx.addons/com.sysdroidxx.addons.a3k 时调用 x.b.I() 构造指向 mok 的 PendingIntent 通知（渠道 id 由 D(27)+111100 生成）",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "无（通知标题/内容取自加密串 b.D(this,26)/D(this,28)，解密表内为葡语运维文案，本轮未确认其确切索引对应文本）",
      "shown_text_zh": "常驻通知用于把用户反复拉回主 Activity，本身不承载说明文字",
      "user_action_requested": "点击通知即回到 mok，再次触发跳转；通知无取消入口",
      "code_anchor": "com.sysdroidxx.addons.mok.onResume / x.b.I"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统无障碍设置页（component 目标：com.android.settings.Settings$AccessibilityInstalledServiceActivity；兜底 action：android.settings.ACCESSIBILITY_SETTINGS）",
      "trigger_event": "onResume() 中 new Intent(b.D(this,20)).setAction(b.D(this,12)).setComponent(new ComponentName(b.D(this,13), b.D(this,14))) 后 startActivityForResult(intent, 333)；异常时回退为仅 setAction(b.D(this,21)) 的 Intent",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Instale - Adobe reader（系统列表项名称；description 为空）",
      "shown_text_zh": "用户被直接带入系统无障碍服务列表，看到唯一可选项名称为伪装身份，且没有任何功能说明",
      "user_action_requested": "要求用户点开该项并把开关拨到开启；页面无应用侧取消/跳过按钮，只能靠系统返回键退出",
      "code_anchor": "com.sysdroidxx.addons.mok.onResume / x.b.D"
    },
    {
      "step": 4,
      "stage": "拒权反馈循环",
      "screen_or_component": "mok.onActivityResult(333, resultCode, intent) → 再次拉起同一系统设置页",
      "trigger_event": "用户在设置页返回/未开启（resultCode != RESULT_OK）时，新建 Intent setFlags(32768=FLAG_ACTIVITY_NEW_TASK) + setAction(b.D(this,21))，startActivityForResult(..., 20)；mok 未 finish，回到前台即再次走 onResume 重跳",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "拒绝授权后立即被重新推回无障碍设置页，形成返回即重跳的死循环；另有 30 分钟周期 Timer 与通知点击再次拉活",
      "user_action_requested": "只能反复返回或最终开启开关，应用不提供任何“稍后再说/跳过”路径",
      "code_anchor": "com.sysdroidxx.addons.mok.onActivityResult"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.sysdroidxx.addons.a3k（无障碍服务 onServiceConnected）",
      "trigger_event": "mok.o() 返回 true → 隐藏视图并 finish()；系统绑定 a3k 后 onServiceConnected() 设置 eventTypes=-1、flags=119 监听全部事件，并调用 performGlobalAction 返回主屏",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "Cliente: / Modo Seguro / Restaurar dados / Redefina seu telefone / Fazer backup dos dados / Link Conexao;",
      "shown_text_zh": "“客户：”/“安全模式”/“恢复数据”/“重置您的手机”/“备份数据”/“连接链接”等葡语遮罩与操作提示，用于在目标银行应用上覆盖伪造界面并读取窗口内容",
      "user_action_requested": "诱使受害者在被覆盖的银行/密码界面上继续输入（此阶段已非权限引导）",
      "code_anchor": "com.sysdroidxx.addons.a3k.onServiceConnected / com.sysdroidxx.addons.a3k.g"
    }
  ],
  "text_presentation_locations": [
    "桌面图标与系统无障碍列表项名称：android:label=@7F0B0098 → 'Instale - Adobe reader'（Manifest 声明）",
    "系统无障碍服务详情/列表说明：res/xml/serg.xml 的 android:description 值为空，列表内不呈现任何用途说明文字",
    "应用主界面 com.sysdroidxx.addons.mok：仅 setContentView(2131296283) 的标题级界面，两个按钮 setVisibility(8) 隐藏，无说明文案、无 WebView、无引导弹窗",
    "通知栏常驻通知（x.b.I）：文案取自加密串 b.D(context,26)/D(context,28)，用途为拉回 mok 而非说明",
    "系统无障碍设置页：由应用跳转后由系统呈现，应用侧无叠加引导遮罩",
    "获权后 a3k 悬浮窗（WindowManager FrameLayout，经 x.b.u 解密的葡语文本）：Cliente: / Modo Seguro / Restaurar dados 等，属于窃取阶段而非引导阶段",
    "加密资源载体：全部界面/系统参数文本存放于 resources.arsc 的 string 池，经 x.b.u（Base64→双字母编码→减 seed 与 key）解密，明文不在包内直接可读"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Instale - Adobe reader",
      "text_zh": "安装 - Adobe 阅读器",
      "source_location": "resources.arsc string @7F0B0098（Manifest android:label / application 显示名，明文未加密）",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "none",
      "text_verbatim": "（空字符串）",
      "text_zh": "无障碍服务描述为空，系统列表中不显示任何用途说明",
      "source_location": "res/xml/serg.xml android:description（加密态资源，解析后为空值）",
      "rhetorical_frame": "教唆忽视警告"
    },
    {
      "lang": "pt",
      "text_verbatim": "Cliente:",
      "text_zh": "客户：",
      "source_location": "resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "Modo Seguro",
      "text_zh": "安全模式",
      "source_location": "resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "pt",
      "text_verbatim": "Restaurar dados",
      "text_zh": "恢复数据",
      "source_location": "resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "Redefina seu telefone",
      "text_zh": "重置您的手机",
      "source_location": "resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "pt",
      "text_verbatim": "Fazer backup dos dados",
      "text_zh": "备份数据",
      "source_location": "resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "Link Conexao;",
      "text_zh": "连接链接;",
      "source_location": "resources.arsc 加密 string，经 x.b.u 解密（a3k 悬浮窗文本）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "com.android.settings.Settings$AccessibilityInstalledServiceActivity",
      "text_zh": "系统无障碍“已安装的服务”设置页组件名（作为跳转 component 使用的解密串）",
      "source_location": "resources.arsc 加密 string，经 x.b.u 解密",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "mok 在未授权时从不 finish()：onResume 每次回到前台都重新 startActivityForResult(intent, 333) 跳系统无障碍设置；用户在设置页返回（resultCode != RESULT_OK）时 onActivityResult 立即以 FLAG_ACTIVITY_NEW_TASK + action b.D(21) 再次 startActivityForResult(..., 20) 重跳；此外 onCreate 注册 1800000ms 周期 Timer(mok$a) 定时再拉起，onResume 每次调用 x.b.I() 保持指向 mok 的常驻通知供点击拉活，三重叠加构成无取消路径的拒权循环。",
    "overlay_or_fake_settings": "本轮静态未见应用侧半透明引导遮罩或高仿系统无障碍开关页；引导完全依赖跳转真实系统设置页，仅靠 android:label 伪装与空 description 隐去用途。悬浮窗（SYSTEM_ALERT_WINDOW）能力在获权后由 a3k.g() 用于覆盖目标银行应用，而非用于权限引导。",
    "restricted_settings_13plus_coaching": "无。targetSdkVersion=27，无需“受限设置”教学；未见应用详情页→右上角菜单→允许受限设置的分步文案，也未见 Session 安装器绕过。解密串中仅出现系统无障碍设置组件名与 com.intelsyss/plugins/... 组件串。",
    "post_grant_anti_removal": "获权后 a3k.onServiceConnected() 以 performGlobalAction(GLOBAL_ACTION_HOME/BACK) 立即离开系统设置页（DEX 线索 anti_removal=PERFORM_GLOBAL_ACTION 与之对应）；本轮未在已读分支中发现监听设置页、自动点确认或持续阻止撤权的显式逻辑（a3k 其余分支未逐条展开）。",
    "benign_graceful_degradation": "无。未授权时既无手动模式、无仅观看模式、也无任何功能降级说明，界面唯一出路是开启无障碍或退出应用。"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "纯 UTG 检测应在两处拉起：①冷启动后监测 com.sysdroidxx.addons.mok 的 startActivityForResult(intent, 333)（intent action=android.settings.ACCESSIBILITY_SETTINGS 或 component=com.android.settings.Settings$AccessibilityInstalledServiceActivity）瞬间；②用户从系统设置页返回时监测 onActivityResult(333, resultCode!=RESULT_OK) 触发的第二次 startActivityForResult(..., 20)，以确认拒权重跳。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首个界面（mok 主 Activity）",
        "page_identifier": "包名 com.sysdroidxx.addons，Activity com.sysdroidxx.addons.mok，标题 'Instale - Adobe reader'，页面无可见按钮（两按钮 GONE）",
        "why_most_useful": "确认引导是 0 步直跳：没有任何业务功能与说明页，直接暴露伪装的空壳主界面",
        "observable_utg_signals": ["当前 Activity 为 com.sysdroidxx.addons.mok", "页面可见控件数为 0（按钮 visibility=gone）", "界面文本仅 'Instale - Adobe reader'"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍页（Settings$AccessibilityInstalledServiceActivity 或 ACCESSIBILITY_SETTINGS），列表项文本 'Instale - Adobe reader' 且无副标题/说明",
        "why_most_useful": "是判定“服务说明为空 + 名称伪装”的关键：恶意样本借此让用户在无用途说明下开启高权限服务",
        "observable_utg_signals": ["列表项文本 = 'Instale - Adobe reader'", "该项无 description 副文本", "页面由 com.sysdroidxx.addons 跳转进入（前一个 Activity 为 mok）"]
      },
      {
        "page_role": "拒权返回后的重跳页（与系统无障碍页同构，但出现次数 ≥2）",
        "page_identifier": "同一系统无障碍页在短时间内被重复拉起，且中间无用户主动点击、无应用内中间页",
        "why_most_useful": "直接量化“返回即重跳”的强制循环强度，是最强的诱导证据",
        "observable_utg_signals": ["同一 AccessibilitySettings 页在 <5s 内第二次出现", "两次跳转之间 mok 未 finish（仍在任务栈）", "存在指向 mok 的常驻通知"]
      },
      {
        "page_role": "获权后覆盖在目标应用上的悬浮窗",
        "page_identifier": "a3k 服务运行中，WindowManager 覆盖的 FrameLayout，含 'Cliente:' / 'Modo Seguro' 等葡语文本",
        "why_most_useful": "验证授权目的：无障碍能力被用于覆盖与读取银行类窗口内容，而非无障碍辅助",
        "observable_utg_signals": ["无障碍服务 com.sysdroidxx.addons.a3k 处于 enabled 状态", "前台出现非本应用包名的覆盖层节点", "覆盖层文本为葡语银行操作引导"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无显著盲区：引导阶段不含图片或纯图空文本，全部判别信号为 Activity 跳转序列 + 系统设置页文本 + 空 description。唯一需注意的是所有界面/参数文案以自定义 Base64+双字母编码加密存放于 resources.arsc，纯静态 grep 明文会一无所获（本轮已用解密脚本还原）；另有反模拟器/反调试检测（mok.l() 命中即 killProcess），在模拟器或可调试环境下可能看不到任何界面，UTG 检测应优先使用真机。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.sysdroidxx.addons.mok.onResume",
    "com.sysdroidxx.addons.mok.onActivityResult",
    "com.sysdroidxx.addons.mok.o",
    "com.sysdroidxx.addons.mok.l",
    "x.b.D",
    "res/xml/serg.xml"
  ]
}
```

</details>
