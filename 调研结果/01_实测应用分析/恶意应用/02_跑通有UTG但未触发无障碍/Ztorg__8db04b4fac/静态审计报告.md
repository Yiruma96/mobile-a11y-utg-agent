# MR_145__8db04b4fac｜Ztorg — LocationServices

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：111.9s

## 1. 一句话核心结论

- **核心申请方式**：以 LocationServices 为桌面名、Daemon Service/Daemon 为无障碍标签的 Ztorg 类样本，主包零引导界面，无障碍事件全量外派给运行时下载并 XOR 解密后 DexClassLoader 加载的二阶段载荷，引导用户开启无障碍的页面流转完全藏在该加密载荷内。
- **静态可见性说明**：主包（classes.dex）仅为壳与加载器：全包搜索 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS / android.settings / ACTION_ 均零命中，无引导 Dialog、无 WebView、无 HTML 资源，唯一 Activity 为 Theme.NoDisplay 且 onCreate 后 finish。真正的引导 UI、设置页跳转与拒权循环位于运行时经 DexClassLoader 加载的二阶段 DEX（由外部存储拷贝 + 首尾5字节校验 + 10字节密钥异或 + 去30字节头尾解密，并可能进一步远端下发），类名/方法名常量亦由 a.a.c.e.a(byte[]) 运行期解密，静态不可读。
- **命中的行为模式标签**：`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `8db04b4fac4cd4368a85dfad85e16e9acadc301700532302687dc273f028bdbd` |
| 包名 / 年份 | `com.android.musitk.in` / 2017 |
| 家族 / 品类 | **Ztorg**（同池样本数：5） |
| 原始来源标识 | https://securelist.com/ztorg-money-for-infecting-your-smartphone/78325/ |
| 桌面显示名 | LocationServices |
| 引导页宣称品牌/身份 | 无真实品牌可对应：桌面名伪装为系统级定位/位置服务（LocationServices），无障碍服务则伪装为系统守护进程 Daemon Service |
| 系统无障碍列表服务名 | Daemon Service（android:description = Daemon） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务标签与说明使用无意义且非本应用身份的通用词 Daemon Service / Daemon，脱离桌面名 LocationServices，使系统无障碍列表项无法与所装应用对应；应用层无 android:description 说明真实用途；同时声明 BIND_DEVICE_ADMIN 的 MDAReceiver 复用同一 acc_title/acc_desc 文案，形成设备管理器与无障碍双重伪装；全部类名与方法名常量以字节数组经 a.a.c.e.a() 运行期解密，规避静态字符串检索 |
| 无障碍服务类名 | `com.android.musitk.in.sr.BAService` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CAMERA, PACKAGE_USAGE_STATS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |
| 系统设置项说明 (`android:description`) | Daemon |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.android.musitk.in.Main（@android:style/Theme.NoDisplay, noHistory=true） | LAUNCHER intent-filter 的 MAIN 入口；onCreate() 内 d.c(this)==0 时直接 finish() | 原生Activity（无界面，Theme.NoDisplay） | 无 | 无任何用户交互，启动后由代码以 ACTION_MAIN + CATEGORY_HOME 直接返回桌面 | `com.android.musitk.in.Main#onCreate` |
| 2 | 冷启动入口 | a.a.a.g 壳入口 + com.android.musitk.in.sr.CService | Main.onCreate() 中 startService(CService) 与 a.a.a.g.a(this)，随后 a.a.a.g.e() 触发二阶段 DEX 装载 | 不可静态还原（二阶段加密载荷） | 无 | 无（后台静默） | `a.a.a.g#e / a.a.a.a#c` |
| 3 | 跳无障碍设置 | 预期为二阶段 DEX 内的引导 Activity/Dialog 及其跳转（主包不存在该类代码） | 二阶段载荷内逻辑触发；主包仅提供 AccessibilityService 转发与 30 分钟节流拉起 Main 的入口 | 不可静态还原（二阶段加密载荷） | **原文**：无（主包内无任何引导文案字符串，res/values/strings.xml 仅有 acc_title=Daemon Service、acc_desc=Daemon）<br>**译注**：主包内不存在引导文字；真实文案藏于加密载荷 | 无法静态确定 | `com.android.musitk.in.sr.BAService#onAccessibilityEvent` |
| 4 | 系统无障碍页 | 系统设置 → 无障碍 → 已下载的服务，条目名 Daemon Service / 说明 Daemon | 用户被引导进入系统无障碍列表（跳转代码位于二阶段载荷，不可静态还原） | 系统无障碍页 | **原文**：Daemon Service / Daemon<br>**译注**：“守护服务” / “守护”——无意义的通用名，未说明真实功能 | 用户被要求在该列表中开启该服务开关（是否可取消不可静态确定） | `res/values/strings.xml#L3-L4 + res/xml/mms_config.xml#L2 + AndroidManifest.xml service com.android.musitk.in.sr.BAService` |
| 5 | 获权后动作 | com.android.musitk.in.sr.BAService.onAccessibilityEvent → a.a.a.g.a(service,event) 反射转发 | 任意无障碍事件回调；内部先 a.a.a.g.a().a() 探测载荷，未就绪则 b(this) 触发装载，再 g.a(this).a(service,event) 外派 | 不可静态还原（二阶段加密载荷） | 无 | 无 | `com.android.musitk.in.sr.BAService#onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/values/strings.xml 的 acc_title="Daemon Service"：作为无障碍服务在系统无障碍列表中的条目标题显示（AndroidManifest.xml 中 service com.android.musitk.in.sr.BAService 的 android:label）
- res/values/strings.xml 的 acc_desc="Daemon"：经 res/xml/mms_config.xml 的 android:description 显示为系统无障碍列表条目下方的说明文字
- 同一对 acc_title/acc_desc 同时被设备管理器 receiver com.android.musitk.in.re.MDAReceiver 的 android:label/android:description 复用，显示在激活设备管理器的系统弹窗中
- 主包内不存在其他呈现位置：无 layout、无 assets HTML、无引导 Dialog、无悬浮窗；全部引导/说明文字位于运行时解密加载的二阶段 DEX（可能进一步远端下发）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Daemon Service | 守护服务 | `res/values/strings.xml key acc_title（AndroidManifest.xml 无障碍服务 android:label 与 MDAReceiver android:label）` | 未知 |
| en | Daemon | 守护进程 | `res/values/strings.xml key acc_desc（res/xml/mms_config.xml 无障碍服务 android:description 与 MDAReceiver android:description）` | 未知 |
| en | LocationServices | 定位服务 | `AndroidManifest.xml application android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无法静态确定：主包无任何设置页跳转与 onResume 重跳逻辑；仅确认 BAService.onAccessibilityEvent 中存在 Math.abs(now-last)>1800000 的 30 分钟节流拉起 Main 的保活分支，拒权后的重跳/循环逻辑位于二阶段加密载荷
- **遮罩叠层 / 高仿系统设置页**：无法静态确定：已声明 SYSTEM_ALERT_WINDOW / SYSTEM_OVERLAY_WINDOW 权限，具备叠放悬浮窗能力，但主包内无任何 Overlay 创建代码或伪造设置页布局，实际实现位于二阶段载荷
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据：主包内无 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、无 Session 安装器相关代码；targetSdkVersion=25 低于 30，设计上不涉及 13+ 受限设置分步教学
- **获权后即时行为与防撤权机制**：主包未实现阻止撤权逻辑；但已声明 BIND_DEVICE_ADMIN（MDAReceiver，device_admin 配置）与 DISABLE_KEYGUARD、INSTALL_PACKAGES/DELETE_PACKAGES、ACCESS_SUPERUSER，并含 4 个 :daemonServiceN 进程守护组件与 libdaemon_api20/21.so 守护库，具备卸载与撤权对抗能力，具体触发位于二阶段载荷
- **良性降级 / 替代方案**：无（未见任何良性降级路径，未获无障碍权限时仅静默返回桌面）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：主包自身不弹引导，故 UTG 应在两类瞬间拉起：①冷启动 com.android.musitk.in.Main 后立即（该 Activity 为 Theme.NoDisplay 且随即 finish 并回桌面，其后由二阶段载荷接管界面）；②监测到任意 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS，或系统无障碍列表中出现 "Daemon Service" 条目时立即抓取前后栈。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：主包静态零引导界面，全部引导文案/按钮/遮罩逻辑位于运行时下载并 XOR 解密的二阶段 DEX（可能进一步远端下发 HTML），纯静态无法给出页面与原文；另 Main 为 Theme.NoDisplay 且秒退，冷启动瞬间可能无任何可截获页面，需在返回桌面后延时监控新 Activity 与悬浮窗。主包未见纯图空文本诱饵与一阶段 APK 嵌入（assets 中仅有 ELF 守护库）。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项** | Settings → Accessibility → Downloaded services 列表中出现 title="Daemon Service"、summary="Daemon" 的条目 | 这是唯一静态可证实的对外呈现文本，可直接对照 strings.xml 证明伪装标签与桌面名 LocationServices 的身份错配 | 条目文本 Daemon Service / Daemon；同列表内其他服务名对比（该名称不属任何已装应用身份）；开关默认关闭状态 |
| **跳转前引导页（二阶段载荷弹出）** | Main 结束回桌面后 0.5–3 秒内新出现的 Activity / Dialog / WebView，非本应用 launcher 图标触发 | 捕获主包不可静态还原的引导文案与按钮结构，判断是否存在取消/跳过与恐吓框架 | 页面文案与按钮文本；是否含“开启/授权/去设置”主按钮且无取消；Activity 组件名是否属 com.android.musitk.in 或由 DexClassLoader 加载的类；是否存在 WebView（本地或远端 URL） |
| **设置页压栈遮罩/拒权返回后页面** | 从系统无障碍页返回后立即出现的悬浮窗（TYPE_SYSTEM_ALERT）或高仿开关页 | 区分“良性一次性引导”与“拒权循环 + 遮罩诱导”，是本样本最关键的恶意判定点 | 返回后是否再次跳转 ACCESSIBILITY_SETTINGS（时间戳间隔）；是否存在覆盖系统设置的悬浮窗节点；是否出现伪造的系统无障碍开关 UI；是否出现无障碍自动点击（GLOBAL_ACTION_BACK/HOME） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.android.musitk.in.Main#onCreate`
- `com.android.musitk.in.sr.BAService#onAccessibilityEvent`
- `a.a.a.g#e`
- `a.a.a.a#c`
- `a.a.a.c#a`
- `res/values/strings.xml#L3-L4`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验：无障碍引导 UTG 页面流转）

**核心判断：引导流程在主包中并不存在，完全位于运行时加载的二阶段加密 DEX 内。**

- **无任何设置页跳转**：`ACTION_ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`ACTION_MANAGE_OVERLAY_PERMISSION`、`ACTION_USAGE_ACCESS_SETTINGS`、`ACTION_SETTINGS` 调用点搜索全部无命中；`ACCESSIBILITY_SETTINGS` / `android.settings` / `ACTION_` 全文搜索亦无命中。主 DEX 内不存在任何引导弹窗、WebView、HTML 资源或悬浮窗。
- **唯一 Activity 无界面**：`Main` 使用 `@android:style/Theme.NoDisplay` + `noHistory`，`onCreate` 启动 `CService`、调用壳 `a.a.a.g.a(this)`，然后以 `ACTION_MAIN`+`CATEGORY_HOME` 直接回桌面；`onResume` 末尾无条件 `finish()`。
- **身份伪装**：[AndroidManifest.xml 无障碍服务声明](<resource-unit:#1 manifest:components>) 中服务 label 为 `Daemon Service`、`mms_config.xml` 引用 `acc_desc`=`Daemon`，桌面名却是 `LocationServices`——三者互不相符，系统无障碍列表项被弱化为无意义守护服务名。
- **获权后事件全量外派**：[BAService.onAccessibilityEvent()](<resource-unit:#1.dex1 code:com.android.musitk.in.sr.BAService#onAccessibilityEvent>) 自身不实现任何逻辑，仅探测载荷就绪→触发装载→把 `AccessibilityService` 与事件反射转发给二阶段类；另含 30 分钟节流拉起 `Main` 的保活分支。
- **载荷装载与解密链**：[a.a.a.g.e()](<resource-unit:#1.dex1 code:a.a.a.g#e>) 从外部存储拷贝文件到 `getFilesDir()`，经 [a.a.a.a.c()](<resource-unit:#1.dex1 code:a.a.a.a#c>) 做“首尾 5 字节校验 + 10 字节密钥异或 + 去 30 字节头尾”自定义解密，再 `DexClassLoader` 加载；[a.a.a.c.a()](<resource-unit:#1.dex1 code:a.a.a.c#a>) 含 `com.b.a.a` 网络下载与 4 小时节流。所有类/方法常量由 `a.a.c.e.a(byte[])` 运行期解密，真实设置页 action 与文案无法静态读出。
- **补充**：`assets/armeabi/daemon` 实为 9444 字节 ELF（非 DEX），属进程守护组件。

已登记风险 R-001（`packed_or_encrypted` 边界）：可确认的静态证据到“伪装身份 + 无障碍挂载 + 载荷装载入口”为止；引导步骤、原文文案、取消按钮、拒权重跳、遮罩/伪造设置页等细节无法静态还原。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "主包（classes.dex）仅为壳与加载器：全包搜索 ACTION_ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS / android.settings / ACTION_ 均零命中，无引导 Dialog、无 WebView、无 HTML 资源，唯一 Activity 为 Theme.NoDisplay 且 onCreate 后 finish。真正的引导 UI、设置页跳转与拒权循环位于运行时经 DexClassLoader 加载的二阶段 DEX（由外部存储拷贝 + 首尾5字节校验 + 10字节密钥异或 + 去30字节头尾解密，并可能进一步远端下发），类名/方法名常量亦由 a.a.c.e.a(byte[]) 运行期解密，静态不可读。",
  "summary_one_liner": "以 LocationServices 为桌面名、Daemon Service/Daemon 为无障碍标签的 Ztorg 类样本，主包零引导界面，无障碍事件全量外派给运行时下载并 XOR 解密后 DexClassLoader 加载的二阶段载荷，引导用户开启无障碍的页面流转完全藏在该加密载荷内。",
  "disguise_identity": {
    "app_display_name": "LocationServices",
    "claimed_brand_or_persona": "无真实品牌可对应：桌面名伪装为系统级定位/位置服务（LocationServices），无障碍服务则伪装为系统守护进程 Daemon Service",
    "a11y_service_label": "Daemon Service（android:description = Daemon）",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务标签与说明使用无意义且非本应用身份的通用词 Daemon Service / Daemon，脱离桌面名 LocationServices，使系统无障碍列表项无法与所装应用对应；应用层无 android:description 说明真实用途；同时声明 BIND_DEVICE_ADMIN 的 MDAReceiver 复用同一 acc_title/acc_desc 文案，形成设备管理器与无障碍双重伪装；全部类名与方法名常量以字节数组经 a.a.c.e.a() 运行期解密，规避静态字符串检索"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.android.musitk.in.Main（@android:style/Theme.NoDisplay, noHistory=true）",
      "trigger_event": "LAUNCHER intent-filter 的 MAIN 入口；onCreate() 内 d.c(this)==0 时直接 finish()",
      "ui_carrier": "原生Activity（无界面，Theme.NoDisplay）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无界面呈现；Activity 不绘制任何内容",
      "user_action_requested": "无任何用户交互，启动后由代码以 ACTION_MAIN + CATEGORY_HOME 直接返回桌面",
      "code_anchor": "com.android.musitk.in.Main#onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "a.a.a.g 壳入口 + com.android.musitk.in.sr.CService",
      "trigger_event": "Main.onCreate() 中 startService(CService) 与 a.a.a.g.a(this)，随后 a.a.a.g.e() 触发二阶段 DEX 装载",
      "ui_carrier": "不可静态还原（二阶段加密载荷）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "主包无任何文案；后续行为由解密后的二阶段 DEX 决定",
      "user_action_requested": "无（后台静默）",
      "code_anchor": "a.a.a.g#e / a.a.a.a#c"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "预期为二阶段 DEX 内的引导 Activity/Dialog 及其跳转（主包不存在该类代码）",
      "trigger_event": "二阶段载荷内逻辑触发；主包仅提供 AccessibilityService 转发与 30 分钟节流拉起 Main 的入口",
      "ui_carrier": "不可静态还原（二阶段加密载荷）",
      "shown_text_verbatim": "无（主包内无任何引导文案字符串，res/values/strings.xml 仅有 acc_title=Daemon Service、acc_desc=Daemon）",
      "shown_text_zh": "主包内不存在引导文字；真实文案藏于加密载荷",
      "user_action_requested": "无法静态确定",
      "code_anchor": "com.android.musitk.in.sr.BAService#onAccessibilityEvent"
    },
    {
      "step": 4,
      "stage": "系统无障碍页",
      "screen_or_component": "系统设置 → 无障碍 → 已下载的服务，条目名 Daemon Service / 说明 Daemon",
      "trigger_event": "用户被引导进入系统无障碍列表（跳转代码位于二阶段载荷，不可静态还原）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Daemon Service / Daemon",
      "shown_text_zh": "“守护服务” / “守护”——无意义的通用名，未说明真实功能",
      "user_action_requested": "用户被要求在该列表中开启该服务开关（是否可取消不可静态确定）",
      "code_anchor": "res/values/strings.xml#L3-L4 + res/xml/mms_config.xml#L2 + AndroidManifest.xml service com.android.musitk.in.sr.BAService"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "com.android.musitk.in.sr.BAService.onAccessibilityEvent → a.a.a.g.a(service,event) 反射转发",
      "trigger_event": "任意无障碍事件回调；内部先 a.a.a.g.a().a() 探测载荷，未就绪则 b(this) 触发装载，再 g.a(this).a(service,event) 外派",
      "ui_carrier": "不可静态还原（二阶段加密载荷）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后不在本类中呈现任何界面，全部事件处理外派给加密载荷",
      "user_action_requested": "无",
      "code_anchor": "com.android.musitk.in.sr.BAService#onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "res/values/strings.xml 的 acc_title=\"Daemon Service\"：作为无障碍服务在系统无障碍列表中的条目标题显示（AndroidManifest.xml 中 service com.android.musitk.in.sr.BAService 的 android:label）",
    "res/values/strings.xml 的 acc_desc=\"Daemon\"：经 res/xml/mms_config.xml 的 android:description 显示为系统无障碍列表条目下方的说明文字",
    "同一对 acc_title/acc_desc 同时被设备管理器 receiver com.android.musitk.in.re.MDAReceiver 的 android:label/android:description 复用，显示在激活设备管理器的系统弹窗中",
    "主包内不存在其他呈现位置：无 layout、无 assets HTML、无引导 Dialog、无悬浮窗；全部引导/说明文字位于运行时解密加载的二阶段 DEX（可能进一步远端下发）"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Daemon Service",
      "text_zh": "守护服务",
      "source_location": "res/values/strings.xml key acc_title（AndroidManifest.xml 无障碍服务 android:label 与 MDAReceiver android:label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Daemon",
      "text_zh": "守护进程",
      "source_location": "res/values/strings.xml key acc_desc（res/xml/mms_config.xml 无障碍服务 android:description 与 MDAReceiver android:description）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "LocationServices",
      "text_zh": "定位服务",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无法静态确定：主包无任何设置页跳转与 onResume 重跳逻辑；仅确认 BAService.onAccessibilityEvent 中存在 Math.abs(now-last)>1800000 的 30 分钟节流拉起 Main 的保活分支，拒权后的重跳/循环逻辑位于二阶段加密载荷",
    "overlay_or_fake_settings": "无法静态确定：已声明 SYSTEM_ALERT_WINDOW / SYSTEM_OVERLAY_WINDOW 权限，具备叠放悬浮窗能力，但主包内无任何 Overlay 创建代码或伪造设置页布局，实际实现位于二阶段载荷",
    "restricted_settings_13plus_coaching": "无静态证据：主包内无 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、无 Session 安装器相关代码；targetSdkVersion=25 低于 30，设计上不涉及 13+ 受限设置分步教学",
    "post_grant_anti_removal": "主包未实现阻止撤权逻辑；但已声明 BIND_DEVICE_ADMIN（MDAReceiver，device_admin 配置）与 DISABLE_KEYGUARD、INSTALL_PACKAGES/DELETE_PACKAGES、ACCESS_SUPERUSER，并含 4 个 :daemonServiceN 进程守护组件与 libdaemon_api20/21.so 守护库，具备卸载与撤权对抗能力，具体触发位于二阶段载荷",
    "benign_graceful_degradation": "无（未见任何良性降级路径，未获无障碍权限时仅静默返回桌面）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "主包自身不弹引导，故 UTG 应在两类瞬间拉起：①冷启动 com.android.musitk.in.Main 后立即（该 Activity 为 Theme.NoDisplay 且随即 finish 并回桌面，其后由二阶段载荷接管界面）；②监测到任意 Activity 跳转 android.settings.ACCESSIBILITY_SETTINGS / ACTION_APPLICATION_DETAILS_SETTINGS，或系统无障碍列表中出现 \"Daemon Service\" 条目时立即抓取前后栈。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings → Accessibility → Downloaded services 列表中出现 title=\"Daemon Service\"、summary=\"Daemon\" 的条目",
        "why_most_useful": "这是唯一静态可证实的对外呈现文本，可直接对照 strings.xml 证明伪装标签与桌面名 LocationServices 的身份错配",
        "observable_utg_signals": ["条目文本 Daemon Service / Daemon", "同列表内其他服务名对比（该名称不属任何已装应用身份）", "开关默认关闭状态"]
      },
      {
        "page_role": "跳转前引导页（二阶段载荷弹出）",
        "page_identifier": "Main 结束回桌面后 0.5–3 秒内新出现的 Activity / Dialog / WebView，非本应用 launcher 图标触发",
        "why_most_useful": "捕获主包不可静态还原的引导文案与按钮结构，判断是否存在取消/跳过与恐吓框架",
        "observable_utg_signals": ["页面文案与按钮文本", "是否含“开启/授权/去设置”主按钮且无取消", "Activity 组件名是否属 com.android.musitk.in 或由 DexClassLoader 加载的类", "是否存在 WebView（本地或远端 URL）"]
      },
      {
        "page_role": "设置页压栈遮罩/拒权返回后页面",
        "page_identifier": "从系统无障碍页返回后立即出现的悬浮窗（TYPE_SYSTEM_ALERT）或高仿开关页",
        "why_most_useful": "区分“良性一次性引导”与“拒权循环 + 遮罩诱导”，是本样本最关键的恶意判定点",
        "observable_utg_signals": ["返回后是否再次跳转 ACCESSIBILITY_SETTINGS（时间戳间隔）", "是否存在覆盖系统设置的悬浮窗节点", "是否出现伪造的系统无障碍开关 UI", "是否出现无障碍自动点击（GLOBAL_ACTION_BACK/HOME）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：主包静态零引导界面，全部引导文案/按钮/遮罩逻辑位于运行时下载并 XOR 解密的二阶段 DEX（可能进一步远端下发 HTML），纯静态无法给出页面与原文；另 Main 为 Theme.NoDisplay 且秒退，冷启动瞬间可能无任何可截获页面，需在返回桌面后延时监控新 Activity 与悬浮窗。主包未见纯图空文本诱饵与一阶段 APK 嵌入（assets 中仅有 ELF 守护库）。"
  },
  "behavior_pattern_tags": [
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "TRIG_COLD_START_BLOCK"
  ],
  "code_anchors": [
    "com.android.musitk.in.Main#onCreate",
    "com.android.musitk.in.sr.BAService#onAccessibilityEvent",
    "a.a.a.g#e",
    "a.a.a.a#c",
    "a.a.a.c#a",
    "res/values/strings.xml#L3-L4"
  ]
}
```

</details>
