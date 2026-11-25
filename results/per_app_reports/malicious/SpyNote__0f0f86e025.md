# MR_005__0f0f86e025｜SpyNote — Android

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：172.0s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即 finish 自身并静默 startActivity 跳到系统无障碍设置页，全程零文案零弹窗，配合无 label/description 的裸无障碍服务与'Android'同名应用，靠界面消失后的系统设置页冒充系统提示诱导用户勾选开启
- **静态可见性说明**：无障碍跳转链路、开关位读取、服务声明均完整静态可见于单 DEX，无加壳/无加密载荷/无 WebView/无 HTML 资源；唯一不确定项是开关串 abcd06 可被远端 82.137.218.185 下发内容覆盖（saveRES），即跳转是否发生由云控配置决定，但代码路径本身不含隐藏逻辑
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `0f0f86e025dd5ad4426d7324e589a0fa6bcb5eace56c17f7c54c0cfdecff276a` |
| 包名 / 年份 | `yps.eton.application` / 2020 |
| 家族 / 品类 | **SpyNote**（同池样本数：59） |
| 原始来源标识 | https://blog.lookout.com/nation-state-mobile-malware-targets-syrians-with-covid-19-lures |
| 桌面显示名 | Android |
| 引导页宣称品牌/身份 | 冒充 Android 系统自身（应用名、服务标签均为 Android），实际为 SpyNote 家族远控木马，署名 Hamodi |
| 系统无障碍列表服务名 | 无（服务未配置 android:label，系统无障碍列表回退显示应用名 Android，且无 description 说明文字） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 应用名与服务标签均硬编码为 'Android'，与系统同名同形，用户难以辨别；2) 无障碍服务刻意不配 android:description 与 android:label，系统列表呈现无说明裸条目，规避'该服务可读取屏幕全部内容'的警示文本；3) 启动 Activity 在 onCreate 中立即 finish() 并 sleep 1500ms 后跳转，制造'点开就闪退随即弹出系统设置'的错觉；4) 全部类名/方法名/字段名为随机小写串（ysszamqyia1、pkfvgtngbzwgeqjureag 等）并插入大量 charAt 开关分支与死循环垃圾代码做控制流混淆 |
| 无障碍服务类名 | `yps.eton.application.ysszamqyia1` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, PROCESS_OUTGOING_CALLS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | yps.eton.application.ysszamqyia7（LAUNCHER Activity，label=@string/app_name=Android，excludeFromRecents=true） | 用户点击桌面图标 'Android' → Activity.onCreate | 原生Activity | **原文**：无（onCreate 中无 setContentView，第一句即 finish()）<br>**译注**：无任何界面内容，窗口在绘制前就被关闭，用户看到的是桌面→系统设置页的瞬间切换 | 无提示；用户来不及操作，Activity 已自行关闭 | `yps.eton.application.ysszamqyia7.onCreate` |
| 2 | 跳转前延时与自身隐藏 | ysszamqyia7.izezqztvpopulbhmjqvg() / eflobknlcjtaefcmmgjt() | onCreate 中 finish() 之后同步执行；另在 onResume 中重复调用 eflobknlcjtaefcmmgjt() | 不可静态还原（无 UI，纯后台逻辑） | 无 | 无 | `yps.eton.application.ysszamqyia7.izezqztvpopulbhmjqvg` |
| 3 | 业务功能触发（云控开关判定） | ysszamqyia7.onStart → pkfvgtngbzwgeqjureag() → new Thread(ysszamqyia7$1) | onStart 生命周期回调，无条件起线程 | 不可静态还原（无 UI） | **原文**：res/values/strings.xml: <string name="abcd06">10000</string><br>**译注**：读取 abcd06 字符串（'10000'）作为配置位串，charAt(1)=='1' 即启用无障碍跳转，charAt(3)=='1' 启用设备管理器索权，charAt(4)=='1' 触发 MyRoohabfdtidhodlsopviuhd()；该字符串可被远端 82.137.218.185 下发内容覆盖 | 无（服务端可控的静默判定） | `yps.eton.application.ysszamqyia7$1.run（读 R$string.abcd06）` |
| 4 | 跳受限设置（并列支线） | android.app.action.ADD_DEVICE_ADMIN 系统设备管理器激活页 | run() 中 abcd06.charAt(3)=='1' 且 ysszamqyia15.yzjsjlwtxfqjqwqyhxtf() 为 false（尚未激活） | 系统无障碍页（此处为系统设备管理器页） | **原文**：putExtra("android.app.extra.ADD_EXPLANATION", BuildConfig.FLAVOR) —— 解释文案为空串<br>**译注**：向系统设备管理器激活页提交空白的解释说明，页面仅显示系统默认的'激活此设备管理器'警示，无任何业务理由 | 系统页要求点击'激活'；无应用自建取消/跳过入口 | `yps.eton.application.ysszamqyia7$1.run（startActivityForResult(..., 100)）` |
| 5 | 跳无障碍设置（主路径） | android.settings.ACCESSIBILITY_SETTINGS（系统无障碍服务列表页） | run() 中 abcd06.charAt(1)=='1' 且 ysszamqyia0.tzjquxmaybrwoyyijjpd==false（无障碍服务未启用） | 系统无障碍页 | **原文**：Intent().setFlags(268435456).setAction("android.settings.ACCESSIBILITY_SETTINGS") → startActivity；页面由系统渲染，应用侧无任何附加文案<br>**译注**：直接拉起系统无障碍服务列表，列表中出现一条无说明的 'Android' 服务项（因未配 android:description / android:label） | 要求用户在该列表中找到 'Android' 条目并手动开启开关；应用不提供任何解释、确认或取消界面 | `yps.eton.application.ysszamqyia7$1.run；同构副本 yps.eton.application.ysszamqyia19.pkvgtngbzwgeqjureag00` |
| 6 | 拒权反馈循环 | ysszamqyia7.onResume → eflobknlcjtaefcmmgjt() | 用户从系统设置页返回、Activity 再次 onResume | 不可静态还原（无 UI，无重跳） | 无 | 无（不存在引导用户重试的界面） | `yps.eton.application.ysszamqyia7.onResume` |
| 7 | 获权后动作 | yps.eton.application.ysszamqyia1（AccessibilityService） | 用户在系统无障碍列表中启用 'Android' 服务 → 系统绑定服务 → onAccessibilityEvent 持续回调 | 悬浮窗Overlay | **原文**：无（界面内容由 C2 82.137.218.185 实时下发，非本地资源）<br>**译注**：获得全局界面读取与点击注入能力后，配合 READ_SMS/RECEIVE_SMS/READ_CONTACTS/CAMERA/RECORD_AUDIO/SYSTEM_ALERT_WINDOW/WRITE_SETTINGS 形成屏幕录制、短信窃取、按键注入与悬浮窗覆盖的远控通道 | 无（静默后台行为） | `yps.eton.application.ysszamqyia1.onAccessibilityEvent` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 完全没有任何应用自建的引导/说明文字载体：无 AlertDialog、无引导 Activity、无 assets/*.html 或 WebView 页面、无悬浮引导窗、无 GIF/图片教程
- 唯一与'文字'相关的呈现位置是系统无障碍服务列表中的条目名：因 Manifest 中 ysszamqyia1 未配 android:label 与 android:description，系统回退显示应用名 @string/app_name（值 'Android'），说明栏为空
- 桌面启动器图标标签：@string/app_name = 'Android'（与系统名同形）；另外两个 Activity 标签分别为 @string/abcd03（'Android'）与 @string/app_name
- res/values/strings.xml 中 abcd00='82.137.218.185'、abcd04='Hamodi'、abcd06='10000' 等仅作为 C2 地址、署名与控制位串被代码读取，不呈现给用户
- 系统设备管理器激活页：ADD_EXPLANATION 被置为空串（BuildConfig.FLAVOR），故该页也无任何应用提供的解释文本
- 结论：本样本的'引导'不是文案说服，而是通过 finish() 抹掉自身界面后直接落到系统设置页，让系统页面的默认外观充当'提示'

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Android | 安卓（系统名） | `res/values/strings.xml key=app_name（同时用于 application android:label 与 ysszamqyia7/ysszamqyia16/ysszamqyia17 的 android:label）` | 未知 |
| en | Android | 安卓（系统名） | `res/values/strings.xml key=abcd03（用于 ysszamqyia6 Activity 与 ysszamqyia0/ysszamqyia5/ysszamqyia14 三个 service 的 android:label）` | 未知 |
| en | Hamodi | 哈莫迪（人名署名） | `res/values/strings.xml key=abcd04` | 未知 |
| en | 10000 | 10000（非文案，为控制位串：charAt(1) 控制无障碍跳转、charAt(3) 控制设备管理器索权、charAt(4) 控制附加动作） | `res/values/strings.xml key=abcd06，由 ysszamqyia7$1.run 与 ysszamqyia19.pkvgtngbzwgeqjureag00 读取，且可被远端 82.137.218.185 下发覆盖` | 未知 |
| en | 82.137.218.185 | 82.137.218.185（C2 服务器 IP，非文案） | `res/values/strings.xml key=abcd00` | 未知 |
| en | (empty) — putExtra("android.app.extra.ADD_EXPLANATION", BuildConfig.FLAVOR) | 空字符串：设备管理器激活页的解释说明被刻意置空，不向用户说明为何需要该权限 | `yps.eton.application.ysszamqyia7$1.run` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：无死循环重跳：用户从系统设置页返回后 onResume 仅重跑 eflobknlcjtaefcmmgjt() 做状态回写，不再次拉起 ACCESSIBILITY_SETTINGS，也不弹任何提示；因 izezqztvpopulbhmjqvg() 已将启动组件 setComponentEnabledSetting(DISABLED)，用户再点桌面图标通常表现为无响应/闪退，形成'应用坏了'的误导性印象而非明示重试
- **遮罩叠层 / 高仿系统设置页**：无。未发现自绘高仿无障碍开关页，也未发现跳转后叠放半透明引导遮罩或全屏悬浮窗（SYSTEM_ALERT_WINDOW 权限虽已声明，但跳转链路中无 WindowManager.addView 调用；悬浮窗能力用于获权后的远控界面覆盖）
- **Android 13+ 受限设置（Restricted Settings）应对**：无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、未发现'点右上角菜单允许受限设置'的图文教学，也无 Session 安装器绕过逻辑（该样本面向 Android 6.0 时代环境，未实现 13+ 受限设置引导）
- **获权后即时行为与防撤权机制**：未发现获权后自点确认或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；但存在并列的设备管理器保护链——run() 中按 abcd06.charAt(3) 拉起 ADD_DEVICE_ADMIN 并 startActivityForResult(...,100) 尝试激活 DeviceAdmin（ysszamqyia2，android.app.device_admin 资源 @raw/android），与无障碍服务共同构成防卸载/防撤权的双重锁
- **良性降级 / 替代方案**：无。被拒权后无任何替代路径（无手动模式、无 ADB 说明、无仅观看模式），直接静默停留在后台等待 C2 指令

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：最佳拉起时机是监测到 Activity 启动 intent 的 action 为 android.settings.ACCESSIBILITY_SETTINGS（或观测到应用 LAUNCHER Activity 在 onCreate 内 finish 后 1.5 秒内前景切到系统无障碍设置页）。此时立刻截取系统无障碍列表并定位 'Android' 裸条目；同时在跳转前后各抓一帧，用于证明应用自身零界面、零文案
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：无纯图片诱饵、无远端 HTML 话术页；主要盲区是：1) 跳转是否发生受远端下发字符串 abcd06 的 charAt(1) 位控制，若 C2 关闭该位则运行期可能完全不跳无障碍页（需结合 C2 通信侧观测）；2) 获权后行为完全由 C2 82.137.218.185 指令驱动，本地无静态文案可对照；3) 启动组件被 setComponentEnabledSetting(DISABLED) 后桌面入口消失，重复复现需重装或先清除组件禁用状态。样本未加壳，静态逻辑完整可见

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **跳转瞬间的空白窗口期（应用 LAUNCHER Activity 已 finish、系统设置页尚未完全绘制）** | yps.eton.application.ysszamqyia7 生命周期极短（onCreate→finish，无 setContentView），Activity 栈中几乎不可见；表现为点击图标后黑屏/桌面残留 0~1.5 秒 | 这是区分'静默甩到设置页'与'良性说明页再引导'的决定性画面——没有说明页本身就构成诱导要件 | 无任何应用自有 View 层级（根节点直接为系统界面）；无 TextView 文本节点，可判定零文案；应用包名 yps.eton.application 无活动窗口 |
| **系统无障碍服务列表项（诱导落点）** | Settings 的 Accessibility 页面，列表中出现 label='Android'、说明为空的条目 | 直接证明服务名伪装为系统名且无 description 警示文本，是'冒充系统身份 + 隐藏能力说明'的核心证据页 | 条目文本节点内容为 'Android'，无副标题/说明文本节点；条目所属包名 yps.eton.application（可通过点击进入详情确认）；开关控件初始为关闭状态 |
| **并列的设备管理器激活页（配套索权）** | 系统 Device admin 激活页，应用解释说明为空 | 证明除无障碍外还同步索取设备管理器权限以对抗卸载/撤权，可与无障碍跳转形成同一次诱导序列 | 页面解释文本为空或仅系统默认警示；激活按钮对应的组件为 yps.eton.application.ysszamqyia2；包名 yps.eton.application 出现在权限授予提示中 |
| **获权后的悬浮窗/覆盖界面** | TYPE_APPLICATION_OVERLAY 悬浮窗（由 C2 下发内容渲染） | 确认无障碍获权后确实进入恶意用途而非良性辅助功能 | 非应用 Activity 的顶层窗口但带 yps.eton.application 的窗口归属；窗口内容与本地 res 资源不匹配（远端下发） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `yps.eton.application.ysszamqyia7.onCreate（finish() + Thread.sleep(1500L) + 配置解析）`
- `yps.eton.application.ysszamqyia7.onStart → pkfvgtngbzwgeqjureag() → new Thread(ysszamqyia7$1)`
- `yps.eton.application.ysszamqyia7$1.run（charAt(1) → setAction("android.settings.ACCESSIBILITY_SETTINGS") + startActivity；charAt(3) → ADD_DEVICE_ADMIN）`
- `yps.eton.application.ysszamqyia19.pkvgtngbzwgeqjureag00（服务侧同构无障碍跳转副本）`
- `yps.eton.application.ysszamqyia7.izezqztvpopulbhmjqvg（setComponentEnabledSetting(ComponentName(this, ysszamqyia7.class), 2, 1) 自禁用启动组件）`
- `res/values/strings.xml（app_name/abcd03='Android'、abcd04='Hamodi'、abcd06='10000' 控制位串、abcd00='82.137.218.185'）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向核验）

**核心结论：该样本没有任何“引导说明”环节，而是在冷启动瞬间静默地把用户抛到系统无障碍设置列表，全程零文案、零解释、无取消按钮。**

1. **入口即自杀式跳转**：LAUNCHER 组件 [ysszamqyia7](<resource-unit:#1.dex1 code:yps.eton.application.ysszamqyia7>) 的 `onCreate` 第一件事是 `finish()` 关闭自身界面，随后 `Thread.sleep(1500L)` 再串接 `izezqztvpopulbhmjqvg()` / `eflobknlcjtaefcmmgjt()`，**没有 `setContentView`、没有 AlertDialog、没有 WebView**。
2. **跳转链路**：`onStart` → [pkfvgtngbzwgeqjureag()](<resource-unit:#1.dex1 code:yps.eton.application.ysszamqyia7#pkfvgtngbzwgeqjureag>) 起线程 → [ysszamqyia7$1#run()](<resource-unit:#1.dex1 code:yps.eton.application.ysszamqyia7$1#run>) 读取 [strings.xml abcd06](<resource-unit:#1 file:res/values/strings.xml#L48>)（值 `10000`）以 `charAt(1)=='1'` 作开关，成立后 `new Intent().setFlags(0x10000000).setAction("android.settings.ACCESSIBILITY_SETTINGS")` → `startActivity`。
3. **同构逻辑备份**：[ysszamqyia19#pkfvgtngbzwgeqjureag00()](<resource-unit:#1.dex1 code:yps.eton.application.ysszamqyia19#pkfvgtngbzwgeqjureag00>) 完全相同的 `ACCESSIBILITY_SETTINGS` 跳转，由后台服务（`ysszamqyia0$*`）侧复用，说明跳转可由服务端/远程指令再次拉起。
4. **无障碍条目无任何说明**：Manifest 中 [ysszamqyia1](<resource-unit:#1.dex1 code:yps.eton.application.ysszamqyia1>) 仅声明 `BIND_ACCESSIBILITY_SERVICE` + intent-filter，**未配置 `android:description`、未配置 `android:label`、无 accessibility-service 元数据 XML**，系统列表中只呈现一个无说明的裸条目。
5. **身份伪装**：`app_name`=`Android`、`abcd03`=`Android`，桌面名与系统名同形；`abcd04`=`Hamodi` 为样本署名；远端 C2 明文 `abcd00`=`82.137.218.185`。
6. **并列的配套勒索型授权**：同一 `run()` 内还按 `charAt(3)` 拉起 `android.app.action.ADD_DEVICE_ADMIN`（`startActivityForResult(...,100)`，`ADD_EXPLANATION` 直接塞空串 `BuildConfig.FLAVOR`），按 `charAt(4)` 触发 `MyRoohabfdtidhodlsopviuhd()`，构成“无障碍 + 设备管理器”双重锁。
7. **拒权反馈**：`onResume` 只调 `eflobknlcjtaefcmmgjt()`，**不会**在返回后死循环重跳无障碍页——即它是“一次性甩到设置页，不解释、不重试”，被拒后表现为“点开图标闪退”的怪象而非重跳弹窗。

已登记风险：R-001（autonomous_audit / high / malware_trojan）。

**UTG 捕获要点**：最佳触发点是监测到 `android.settings.ACCESSIBILITY_SETTINGS` 被拉起的瞬间——此时前景为系统无障碍列表，而列表项将显示为**空白说明的 `Android` 条目**；该“跳转前后无任何自有界面”的空窗期本身就是最强判别信号。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无障碍跳转链路、开关位读取、服务声明均完整静态可见于单 DEX，无加壳/无加密载荷/无 WebView/无 HTML 资源；唯一不确定项是开关串 abcd06 可被远端 82.137.218.185 下发内容覆盖（saveRES），即跳转是否发生由云控配置决定，但代码路径本身不含隐藏逻辑",
  "summary_one_liner": "冷启动即 finish 自身并静默 startActivity 跳到系统无障碍设置页，全程零文案零弹窗，配合无 label/description 的裸无障碍服务与'Android'同名应用，靠界面消失后的系统设置页冒充系统提示诱导用户勾选开启",
  "disguise_identity": {
    "app_display_name": "Android",
    "claimed_brand_or_persona": "冒充 Android 系统自身（应用名、服务标签均为 Android），实际为 SpyNote 家族远控木马，署名 Hamodi",
    "a11y_service_label": "无（服务未配置 android:label，系统无障碍列表回退显示应用名 Android，且无 description 说明文字）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 应用名与服务标签均硬编码为 'Android'，与系统同名同形，用户难以辨别；2) 无障碍服务刻意不配 android:description 与 android:label，系统列表呈现无说明裸条目，规避'该服务可读取屏幕全部内容'的警示文本；3) 启动 Activity 在 onCreate 中立即 finish() 并 sleep 1500ms 后跳转，制造'点开就闪退随即弹出系统设置'的错觉；4) 全部类名/方法名/字段名为随机小写串（ysszamqyia1、pkfvgtngbzwgeqjureag 等）并插入大量 charAt 开关分支与死循环垃圾代码做控制流混淆"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "yps.eton.application.ysszamqyia7（LAUNCHER Activity，label=@string/app_name=Android，excludeFromRecents=true）",
      "trigger_event": "用户点击桌面图标 'Android' → Activity.onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（onCreate 中无 setContentView，第一句即 finish()）",
      "shown_text_zh": "无任何界面内容，窗口在绘制前就被关闭，用户看到的是桌面→系统设置页的瞬间切换",
      "user_action_requested": "无提示；用户来不及操作，Activity 已自行关闭",
      "code_anchor": "yps.eton.application.ysszamqyia7.onCreate"
    },
    {
      "step": 2,
      "stage": "跳转前延时与自身隐藏",
      "screen_or_component": "ysszamqyia7.izezqztvpopulbhmjqvg() / eflobknlcjtaefcmmgjt()",
      "trigger_event": "onCreate 中 finish() 之后同步执行；另在 onResume 中重复调用 eflobknlcjtaefcmmgjt()",
      "ui_carrier": "不可静态还原（无 UI，纯后台逻辑）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "Thread.sleep(1500L) 后调用配置解析与组件自禁用逻辑；izezqztvpopulbhmjqvg 中通过 PackageManager.setComponentEnabledSetting(ComponentName(this, ysszamqyia7.class), 2, 1) 将启动组件自身设为 DISABLED，抹除桌面入口痕迹",
      "user_action_requested": "无",
      "code_anchor": "yps.eton.application.ysszamqyia7.izezqztvpopulbhmjqvg"
    },
    {
      "step": 3,
      "stage": "业务功能触发（云控开关判定）",
      "screen_or_component": "ysszamqyia7.onStart → pkfvgtngbzwgeqjureag() → new Thread(ysszamqyia7$1)",
      "trigger_event": "onStart 生命周期回调，无条件起线程",
      "ui_carrier": "不可静态还原（无 UI）",
      "shown_text_verbatim": "res/values/strings.xml: <string name=\"abcd06\">10000</string>",
      "shown_text_zh": "读取 abcd06 字符串（'10000'）作为配置位串，charAt(1)=='1' 即启用无障碍跳转，charAt(3)=='1' 启用设备管理器索权，charAt(4)=='1' 触发 MyRoohabfdtidhodlsopviuhd()；该字符串可被远端 82.137.218.185 下发内容覆盖",
      "user_action_requested": "无（服务端可控的静默判定）",
      "code_anchor": "yps.eton.application.ysszamqyia7$1.run（读 R$string.abcd06）"
    },
    {
      "step": 4,
      "stage": "跳受限设置（并列支线）",
      "screen_or_component": "android.app.action.ADD_DEVICE_ADMIN 系统设备管理器激活页",
      "trigger_event": "run() 中 abcd06.charAt(3)=='1' 且 ysszamqyia15.yzjsjlwtxfqjqwqyhxtf() 为 false（尚未激活）",
      "ui_carrier": "系统无障碍页（此处为系统设备管理器页）",
      "shown_text_verbatim": "putExtra(\"android.app.extra.ADD_EXPLANATION\", BuildConfig.FLAVOR) —— 解释文案为空串",
      "shown_text_zh": "向系统设备管理器激活页提交空白的解释说明，页面仅显示系统默认的'激活此设备管理器'警示，无任何业务理由",
      "user_action_requested": "系统页要求点击'激活'；无应用自建取消/跳过入口",
      "code_anchor": "yps.eton.application.ysszamqyia7$1.run（startActivityForResult(..., 100)）"
    },
    {
      "step": 5,
      "stage": "跳无障碍设置（主路径）",
      "screen_or_component": "android.settings.ACCESSIBILITY_SETTINGS（系统无障碍服务列表页）",
      "trigger_event": "run() 中 abcd06.charAt(1)=='1' 且 ysszamqyia0.tzjquxmaybrwoyyijjpd==false（无障碍服务未启用）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Intent().setFlags(268435456).setAction(\"android.settings.ACCESSIBILITY_SETTINGS\") → startActivity；页面由系统渲染，应用侧无任何附加文案",
      "shown_text_zh": "直接拉起系统无障碍服务列表，列表中出现一条无说明的 'Android' 服务项（因未配 android:description / android:label）",
      "user_action_requested": "要求用户在该列表中找到 'Android' 条目并手动开启开关；应用不提供任何解释、确认或取消界面",
      "code_anchor": "yps.eton.application.ysszamqyia7$1.run；同构副本 yps.eton.application.ysszamqyia19.pkvgtngbzwgeqjureag00"
    },
    {
      "step": 6,
      "stage": "拒权反馈循环",
      "screen_or_component": "ysszamqyia7.onResume → eflobknlcjtaefcmmgjt()",
      "trigger_event": "用户从系统设置页返回、Activity 再次 onResume",
      "ui_carrier": "不可静态还原（无 UI，无重跳）",
      "shown_text_verbatim": "无",
      "shown_text_zh": "onResume 仅重跑配置解析与状态回写，不再重复拉起 ACCESSIBILITY_SETTINGS，也不弹任何提示；因启动组件已被 DISABLED，用户再次点桌面图标通常表现为闪退/无响应",
      "user_action_requested": "无（不存在引导用户重试的界面）",
      "code_anchor": "yps.eton.application.ysszamqyia7.onResume"
    },
    {
      "step": 7,
      "stage": "获权后动作",
      "screen_or_component": "yps.eton.application.ysszamqyia1（AccessibilityService）",
      "trigger_event": "用户在系统无障碍列表中启用 'Android' 服务 → 系统绑定服务 → onAccessibilityEvent 持续回调",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无（界面内容由 C2 82.137.218.185 实时下发，非本地资源）",
      "shown_text_zh": "获得全局界面读取与点击注入能力后，配合 READ_SMS/RECEIVE_SMS/READ_CONTACTS/CAMERA/RECORD_AUDIO/SYSTEM_ALERT_WINDOW/WRITE_SETTINGS 形成屏幕录制、短信窃取、按键注入与悬浮窗覆盖的远控通道",
      "user_action_requested": "无（静默后台行为）",
      "code_anchor": "yps.eton.application.ysszamqyia1.onAccessibilityEvent"
    }
  ],
  "text_presentation_locations": [
    "完全没有任何应用自建的引导/说明文字载体：无 AlertDialog、无引导 Activity、无 assets/*.html 或 WebView 页面、无悬浮引导窗、无 GIF/图片教程",
    "唯一与'文字'相关的呈现位置是系统无障碍服务列表中的条目名：因 Manifest 中 ysszamqyia1 未配 android:label 与 android:description，系统回退显示应用名 @string/app_name（值 'Android'），说明栏为空",
    "桌面启动器图标标签：@string/app_name = 'Android'（与系统名同形）；另外两个 Activity 标签分别为 @string/abcd03（'Android'）与 @string/app_name",
    "res/values/strings.xml 中 abcd00='82.137.218.185'、abcd04='Hamodi'、abcd06='10000' 等仅作为 C2 地址、署名与控制位串被代码读取，不呈现给用户",
    "系统设备管理器激活页：ADD_EXPLANATION 被置为空串（BuildConfig.FLAVOR），故该页也无任何应用提供的解释文本",
    "结论：本样本的'引导'不是文案说服，而是通过 finish() 抹掉自身界面后直接落到系统设置页，让系统页面的默认外观充当'提示'"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Android",
      "text_zh": "安卓（系统名）",
      "source_location": "res/values/strings.xml key=app_name（同时用于 application android:label 与 ysszamqyia7/ysszamqyia16/ysszamqyia17 的 android:label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Android",
      "text_zh": "安卓（系统名）",
      "source_location": "res/values/strings.xml key=abcd03（用于 ysszamqyia6 Activity 与 ysszamqyia0/ysszamqyia5/ysszamqyia14 三个 service 的 android:label）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Hamodi",
      "text_zh": "哈莫迪（人名署名）",
      "source_location": "res/values/strings.xml key=abcd04",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "10000",
      "text_zh": "10000（非文案，为控制位串：charAt(1) 控制无障碍跳转、charAt(3) 控制设备管理器索权、charAt(4) 控制附加动作）",
      "source_location": "res/values/strings.xml key=abcd06，由 ysszamqyia7$1.run 与 ysszamqyia19.pkvgtngbzwgeqjureag00 读取，且可被远端 82.137.218.185 下发覆盖",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "82.137.218.185",
      "text_zh": "82.137.218.185（C2 服务器 IP，非文案）",
      "source_location": "res/values/strings.xml key=abcd00",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "(empty) — putExtra(\"android.app.extra.ADD_EXPLANATION\", BuildConfig.FLAVOR)",
      "text_zh": "空字符串：设备管理器激活页的解释说明被刻意置空，不向用户说明为何需要该权限",
      "source_location": "yps.eton.application.ysszamqyia7$1.run",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "无死循环重跳：用户从系统设置页返回后 onResume 仅重跑 eflobknlcjtaefcmmgjt() 做状态回写，不再次拉起 ACCESSIBILITY_SETTINGS，也不弹任何提示；因 izezqztvpopulbhmjqvg() 已将启动组件 setComponentEnabledSetting(DISABLED)，用户再点桌面图标通常表现为无响应/闪退，形成'应用坏了'的误导性印象而非明示重试",
    "overlay_or_fake_settings": "无。未发现自绘高仿无障碍开关页，也未发现跳转后叠放半透明引导遮罩或全屏悬浮窗（SYSTEM_ALERT_WINDOW 权限虽已声明，但跳转链路中无 WindowManager.addView 调用；悬浮窗能力用于获权后的远控界面覆盖）",
    "restricted_settings_13plus_coaching": "无。未发现 ACTION_APPLICATION_DETAILS_SETTINGS 跳转、未发现'点右上角菜单允许受限设置'的图文教学，也无 Session 安装器绕过逻辑（该样本面向 Android 6.0 时代环境，未实现 13+ 受限设置引导）",
    "post_grant_anti_removal": "未发现获权后自点确认或监听设置页用 GLOBAL_ACTION_BACK/HOME 阻止撤权的代码；但存在并列的设备管理器保护链——run() 中按 abcd06.charAt(3) 拉起 ADD_DEVICE_ADMIN 并 startActivityForResult(...,100) 尝试激活 DeviceAdmin（ysszamqyia2，android.app.device_admin 资源 @raw/android），与无障碍服务共同构成防卸载/防撤权的双重锁",
    "benign_graceful_degradation": "无。被拒权后无任何替代路径（无手动模式、无 ADB 说明、无仅观看模式），直接静默停留在后台等待 C2 指令"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "最佳拉起时机是监测到 Activity 启动 intent 的 action 为 android.settings.ACCESSIBILITY_SETTINGS（或观测到应用 LAUNCHER Activity 在 onCreate 内 finish 后 1.5 秒内前景切到系统无障碍设置页）。此时立刻截取系统无障碍列表并定位 'Android' 裸条目；同时在跳转前后各抓一帧，用于证明应用自身零界面、零文案",
    "key_pages_to_capture": [
      {
        "page_role": "跳转瞬间的空白窗口期（应用 LAUNCHER Activity 已 finish、系统设置页尚未完全绘制）",
        "page_identifier": "yps.eton.application.ysszamqyia7 生命周期极短（onCreate→finish，无 setContentView），Activity 栈中几乎不可见；表现为点击图标后黑屏/桌面残留 0~1.5 秒",
        "why_most_useful": "这是区分'静默甩到设置页'与'良性说明页再引导'的决定性画面——没有说明页本身就构成诱导要件",
        "observable_utg_signals": [
          "无任何应用自有 View 层级（根节点直接为系统界面）",
          "无 TextView 文本节点，可判定零文案",
          "应用包名 yps.eton.application 无活动窗口"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项（诱导落点）",
        "page_identifier": "Settings 的 Accessibility 页面，列表中出现 label='Android'、说明为空的条目",
        "why_most_useful": "直接证明服务名伪装为系统名且无 description 警示文本，是'冒充系统身份 + 隐藏能力说明'的核心证据页",
        "observable_utg_signals": [
          "条目文本节点内容为 'Android'，无副标题/说明文本节点",
          "条目所属包名 yps.eton.application（可通过点击进入详情确认）",
          "开关控件初始为关闭状态"
        ]
      },
      {
        "page_role": "并列的设备管理器激活页（配套索权）",
        "page_identifier": "系统 Device admin 激活页，应用解释说明为空",
        "why_most_useful": "证明除无障碍外还同步索取设备管理器权限以对抗卸载/撤权，可与无障碍跳转形成同一次诱导序列",
        "observable_utg_signals": [
          "页面解释文本为空或仅系统默认警示",
          "激活按钮对应的组件为 yps.eton.application.ysszamqyia2",
          "包名 yps.eton.application 出现在权限授予提示中"
        ]
      },
      {
        "page_role": "获权后的悬浮窗/覆盖界面",
        "page_identifier": "TYPE_APPLICATION_OVERLAY 悬浮窗（由 C2 下发内容渲染）",
        "why_most_useful": "确认无障碍获权后确实进入恶意用途而非良性辅助功能",
        "observable_utg_signals": [
          "非应用 Activity 的顶层窗口但带 yps.eton.application 的窗口归属",
          "窗口内容与本地 res 资源不匹配（远端下发）"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "无纯图片诱饵、无远端 HTML 话术页；主要盲区是：1) 跳转是否发生受远端下发字符串 abcd06 的 charAt(1) 位控制，若 C2 关闭该位则运行期可能完全不跳无障碍页（需结合 C2 通信侧观测）；2) 获权后行为完全由 C2 82.137.218.185 指令驱动，本地无静态文案可对照；3) 启动组件被 setComponentEnabledSetting(DISABLED) 后桌面入口消失，重复复现需重装或先清除组件禁用状态。样本未加壳，静态逻辑完整可见"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION"
  ],
  "code_anchors": [
    "yps.eton.application.ysszamqyia7.onCreate（finish() + Thread.sleep(1500L) + 配置解析）",
    "yps.eton.application.ysszamqyia7.onStart → pkfvgtngbzwgeqjureag() → new Thread(ysszamqyia7$1)",
    "yps.eton.application.ysszamqyia7$1.run（charAt(1) → setAction(\"android.settings.ACCESSIBILITY_SETTINGS\") + startActivity；charAt(3) → ADD_DEVICE_ADMIN）",
    "yps.eton.application.ysszamqyia19.pkvgtngbzwgeqjureag00（服务侧同构无障碍跳转副本）",
    "yps.eton.application.ysszamqyia7.izezqztvpopulbhmjqvg（setComponentEnabledSetting(ComponentName(this, ysszamqyia7.class), 2, 1) 自禁用启动组件）",
    "res/values/strings.xml（app_name/abcd03='Android'、abcd04='Hamodi'、abcd06='10000' 控制位串、abcd00='82.137.218.185'）"
  ]
}
```

</details>
