# MB_142__b9ddc7c5f9｜Crocodilus — Magicstyle

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：100.9s

## 1. 一句话核心结论

- **核心申请方式**：仅 33 个类的极简 dropper 外壳，冷启动即用 AES 解密 assets/encroc*.enc 二阶段载荷，无障碍服务 Magicstyle Service 的申请引导页与文案全部藏于该加密载荷，明文层无任何 ACTION_ACCESSIBILITY_SETTINGS 跳转与提示文本。
- **静态可见性说明**：AndroidManifest 声明完整可见（显示名 Magicstyle、无障碍服务 baggage.stream.gonad.tdbuiNelea.xappKOWtA、标签 Magicstyle Service、BIND_ACCESSIBILITY_SERVICE、Application=mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs）；但 classes.dex 仅 33 个随机名外壳类，不含任何 baggage.stream.gonad.* 类，无障碍服务实现、引导 Activity、说明文案全部位于 assets/encroc1-3.enc 的 AES 二阶段加密载荷中。已还原密文布局（key@32-48、iv@48-64、len@64-72、密文@72）与 Cipher 变换名还原逻辑，但密文长度非 16 字节对齐，本地复现解密失败，二阶段 DEX 未能落地；assets/encroc1.dex、encroc2.dex 为伪造/诱饵文件。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `b9ddc7c5f9adbf012494ab258acd80ab35311b52e3b28f2a78a1d8dad75ab259` |
| 包名 / 年份 | `baggage.stream.gonad` / 2025 |
| 家族 / 品类 | **Crocodilus**（同池样本数：6） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Magicstyle |
| 引导页宣称品牌/身份 | Magicstyle（无明确真实品牌对应，疑为随机伪装的风格/美化类应用身份） |
| 系统无障碍列表服务名 | Magicstyle Service |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 baggage.stream.gonad 与显示名 Magicstyle 无语义关联；Manifest 注册十余个随机词组的 activity/activity-alias（如 baggage.stream.gonad.bLKJUcuMiLMbuN.EgRjNorhkhvLN、baggage.stream.gonad.HoyoVHrILE.HyGChkfdoIVnT、baggage.stream.gonad.TrumpTayyip），存在多别名伪装迹象；明文 DEX 类名全部为随机英文词组拼接（kitematter.casingmuck.Hunterrefurnish、mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs）；无障碍服务类 tdbuiNelea.xappKOWtA 大小写混排无意义；Cipher 变换字符串以 XOR 常量数组混淆；引导页具体伪装手法因载荷未还原无法确认。 |
| 无障碍服务类名 | `baggage.stream.gonad.tdbuiNelea.xappKOWtA` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, CAMERA, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | Application 类 mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs（Manifest application 节点） | attachBaseContext() / onCreate() 被系统回调 | 不可静态还原 | **原文**：🔧 Uygulama bağlamı başlatılıyor / 🚀 Uygulama başlatıldı<br>**译注**：🔧 应用上下文初始化中 / 🚀 应用已启动（仅为内部调试日志，非用户界面文案） | 无（进程级自动执行，无需用户交互） | `mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs.attachBaseContext / onCreate` |
| 2 | 冷启动入口 | Edgingraging.cheesyimmovable → Hunterrefurnish.backstabretool → partyflaring.womanlessatypical.Refiningrepacking.bobblecommerce（二阶段 DEX 加载器） | Application.onCreate 中 footereject 调用链自动执行 | 不可静态还原 | **原文**：✅ Şifre çözme başarılı<br>**译注**：✅ 解密成功（内部日志） | 无 | `kitematter.casingmuck.Edgingraging.cheesyimmovable → kitematter.casingmuck.Hunterrefurnish.backstabretool` |
| 3 | 引导说明页 | assets/encroc1.enc / encroc2.enc / encroc3.enc 解密后得到的二阶段 DEX 内 Activity（类名未知） | 二阶段载荷加载完成后由载荷内部逻辑决定（不可静态还原） | 不可静态还原 | **原文**：无（明文层无任何用户可见文案；载荷未还原）<br>**译注**：无法获取 | 无法静态判定（是否提供取消/跳过按钮未知） | `#1 file:assets/encroc1.enc` |
| 4 | 跳无障碍设置 | 预期为 android.settings.ACCESSIBILITY_SETTINGS 系统页（跳转代码位于加密载荷内） | 不可静态还原；明文 classes.dex 全文检索 accessibility / ACCESSIBILITY / Settings 均无命中 | 系统无障碍页 | 无 | 无法静态判定（预期为开启 Magicstyle Service 开关） | `#1 manifest:components（服务声明 baggage.stream.gonad.tdbuiNelea.xappKOWtA）` |
| 5 | 获权后动作 | 无障碍服务实现类 baggage.stream.gonad.tdbuiNelea.xappKOWtA（实现不在 classes.dex） | 系统绑定无障碍服务后回调（onServiceConnected 等，不可静态还原） | 不可静态还原 | 无 | 无法静态判定 | `#1 manifest:components` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 无任何可静态确认的用户可见引导文字：res/ 下仅有 AppCompat 等标准库资源，classes.dex 全文无 accessibility / Settings / 引导语字符串
- 唯一明文自然语言为 com.nirvana.dropper.util.TG.send 输出的土耳其语调试日志（Logcat 层，非界面）
- Manifest 中唯一面向用户的文本：应用显示名 Magicstyle、无障碍服务标签 Magicstyle Service（后者会呈现在系统无障碍服务列表中）
- 预期存在但不可静态还原的位置：assets/encroc1-3.enc 解密出的二阶段 DEX 内引导 Activity / Dialog / WebView 及其中文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | 🔧 Uygulama bağlamı başlatılıyor | 🔧 应用上下文初始化中 | `com.nirvana.dropper.util.TG.send 调用点（Scrubberearplugs.attachBaseContext，硬编码）` | 未知 |
| tr | 🚀 Uygulama başlatıldı | 🚀 应用已启动 | `Scrubberearplugs.onCreate 硬编码` | 未知 |
| tr | ✅ Şifre çözme başarılı | ✅ 解密成功 | `kitematter.casingmuck.Hunterrefurnish.backstabretool 硬编码` | 未知 |
| en | Magicstyle Service | Magicstyle 服务（系统无障碍服务列表中显示） | `AndroidManifest.xml 无障碍服务 android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态判定：明文层无任何跳转与重试逻辑，相关实现位于 AES 加密的二阶段载荷内，未能还原
- **遮罩叠层 / 高仿系统设置页**：不可静态判定（明文层无悬浮窗/遮罩代码，但 Manifest 申请 SYSTEM_ALERT_WINDOW 之外相关权限未能确认；实际叠层行为藏于载荷）
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据；未在明文 DEX 中发现应用详情页或受限设置教学相关字符串，判定需依赖载荷还原
- **获权后即时行为与防撤权机制**：不可静态判定；Manifest 申请 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、REQUEST_DELETE_PACKAGES、设备管理（BIND_DEVICE_ADMIN、DEVICE_ADMIN_ENABLED/DISABLED 接收器）等权限，具备反卸载/持久化能力，但自点确认或阻止撤权的具体代码未在明文层出现
- **良性降级 / 替代方案**：无（无任何良性降级路径证据）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：以冷启动为起点立即拉起 UTG 采集：应用启动（Application.onCreate 自动解密加载载荷）后极短时间内即可能直弹引导页；同时 Hook Activity 启动与 Intent，一旦观测到 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 跳转即锁定引导链
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在明显盲区：一阶段 classes.dex 仅 33 个类，全部引导逻辑在 AES 加密的 assets/encroc1-3.enc 内，密文长度非 16 字节对齐导致本地复现解密失败，二阶段 DEX 未能落地，因此引导页文案、取消按钮、拒权循环、遮罩与受限设置教学均无法静态确认；此外 assets 内大量 1024 字节 png、mp3、随机 json 属诱饵噪声。运行期 UTG 不受此加密阻碍，仍可直接捕获真实界面。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的首个可见界面（载荷加载完成即刻弹出）** | 启动 Magicstyle 后第一个非系统 Activity；预期为带引导文案的原生 Dialog/Activity 或 WebView 容器 | 明文层无任何引导文案，首个界面是唯一能揭示其伪装叙事（假更新/清理/反诈等）的位置，直接决定引导手法定性 | 界面标题与正文全部文本；是否存在取消/跳过/稍后按钮及其文案；是否可返回键退出；Activity 全限定类名与是否为 activity-alias |
| **跳转无障碍设置前的教学/说明页** | 含「无障碍」「辅助功能」「Accessibility」「Ayarlar」「Erişilebilirlik」等字样的原生页或 WebView | 区分是良性透明说明还是假系统警告/教唆忽视安全提示；同时确认是否为本地 HTML 还是远端下发页面 | 页面 URL（区分 file:// 与 http(s):// 远端）；服务名 Magicstyle Service 是否被显式指引用；是否出现伪造系统 UI 元素（开关图形、设置标题栏）；是否有免责/隐私承诺类话术 |
| **系统无障碍服务列表项** | Settings 无障碍列表中 label 为 Magicstyle Service 的条目 | 确认跳转确实落在无障碍页、服务项真实存在，并可核对 android:description 是否被刻意留空以规避警示 | 服务项显示名与图标；description 是否为空（Manifest 中 android:description 缺失）；是否存在同形字/前后空白伪装 |
| **从设置页返回后的拒权反馈页** | 用户未开启服务直接返回时立即重现的界面 | 判定是否存在 onResume 死循环重跳或定时器反复拉起，这是区分诱导与强制的关键 | 返回后重新出现的界面与间隔时长；同屏是否叠有半透明遮罩；返回键是否被拦截 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs.attachBaseContext`
- `mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs.onCreate`
- `kitematter.casingmuck.Edgingraging.cheesyimmovable`
- `kitematter.casingmuck.Hunterrefurnish.backstabretool`
- `kitematter.casingmuck.Hunterrefurnish.humoroushuntsman`
- `#1 file:assets/encroc1.enc`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

- **Manifest 声明与实现严重脱节**：二进制 Manifest 中确认 `label = Magicstyle`、无障碍服务标签 `Magicstyle Service`、服务类 `baggage.stream.gonad.tdbuiNelea.xappKOWtA`、`BIND_ACCESSIBILITY_SERVICE`、`Application` 为 `mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs`，并注册了十余个 `baggage.stream.gonad.*` 的 activity / activity-alias 类名。
- **classes.dex 只是外壳**：仅 33 个类，包名全部为随机词组（`kitematter.*`、`nwpg.lzaf.*`、`partyflaring.*`、`mlbpdnmi.*`），**不存在任何 `baggage.stream.gonad.*` 类**。无障碍服务实现类、引导 Activity、说明页全部缺席 → 明文 DEX 不含 UTG 引导逻辑。
- **冷启动即触发载荷解密**：[Scrubberearplugs.attachBaseContext()](<resource-unit:#1.dex1 code:mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs#attachBaseContext>) → `ensnaredandy`，[onCreate()](<resource-unit:#1.dex1 code:mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs#onCreate>) → `footereject`，最终进入 [Edgingraging.cheesyimmovable()](<resource-unit:#1.dex1 code:kitematter.casingmuck.Edgingraging#cheesyimmovable>) → [Hunterrefurnish.backstabretool()](<resource-unit:#1.dex1 code:kitematter.casingmuck.Hunterrefurnish#backstabretool>)，对 `assets/encroc1-3.enc` 做 AES 解密后交给 `Refiningrepacking.bobblecommerce` 加载。
- **解密算法已还原，但载荷未能解出**：密文布局为 `[0,32)` 头部、`key=[32,48)`、`iv=[48,64)`、`expected_len=long@[64,72)`、密文 `[72,EOF)`；Cipher 变换名由 [humoroushuntsman()](<resource-unit:#1.dex1 code:kitematter.casingmuck.Hunterrefurnish#humoroushuntsman>) 用 XOR 常量还原，解密后还需 `length == expected_len` 校验（[bubblingmoonwalk()](<resource-unit:#1.dex1 code:kitematter.casingmuck.Hunterrefurnish#bubblingmoonwalk>)）。本地按该布局复现 AES-CBC/ECB 均因**密文长度非 16 字节对齐**失败，说明读取 `assets` 前还有一层变换（base64/分段）未捕获 → 二阶段 DEX 未能静态落地。
- `assets/encroc1.dex`（1024 字节）、`encroc2.dex`（14336 字节）文件头均非 `dex\n` 魔数，属诱饵；`.png` 多为 1024 字节填充、`.mp3` 与 `.json` 为噪声诱饵。
- **可见文案为零**：明文层唯一自然语言是 [TG.send()](<resource-unit:#1.dex1 code:com.nirvana.dropper.util.TG#send>) 的土耳其语调试日志（`Uygulama bağlamı başlatılıyor` 等），无任何用户可见弹窗/HTML/strings 引导文本，说明引导页与文案全部在加密载荷内。
- **结论**：符合项目既有 R-001（`source_mode = autonomous_audit`，high，`review_evasion_mutation`）——无障碍诱导交互不可静态还原，`static_visibility = packed_or_encrypted`；本轮未新增或修订风险记录。

## 可确认与不可确认的边界

| 项 | 状态 |
|---|---|
| 无障碍服务声明存在、标签 `Magicstyle Service` | 已确认（Manifest 字符串） |
| 服务实现类 `xappKOWtA` 在 classes.dex 中 | **不存在** |
| 冷启动自动解密 + 加载二阶段载荷 | 已确认（调用链完整） |
| 二阶段载荷内容（含引导页/弹窗/文案） | 未还原（AES 布局已知，数据前置变换未解） |
| `ACTION_ACCESSIBILITY_SETTINGS` 跳转点 | 明文 DEX 中无任何 `Settings`/`accessibility` 字符串命中 |
| 取消按钮、拒权循环、遮罩、受限设置教学 | 无法静态判定，属未决问题 |

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "AndroidManifest 声明完整可见（显示名 Magicstyle、无障碍服务 baggage.stream.gonad.tdbuiNelea.xappKOWtA、标签 Magicstyle Service、BIND_ACCESSIBILITY_SERVICE、Application=mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs）；但 classes.dex 仅 33 个随机名外壳类，不含任何 baggage.stream.gonad.* 类，无障碍服务实现、引导 Activity、说明文案全部位于 assets/encroc1-3.enc 的 AES 二阶段加密载荷中。已还原密文布局（key@32-48、iv@48-64、len@64-72、密文@72）与 Cipher 变换名还原逻辑，但密文长度非 16 字节对齐，本地复现解密失败，二阶段 DEX 未能落地；assets/encroc1.dex、encroc2.dex 为伪造/诱饵文件。",
  "summary_one_liner": "仅 33 个类的极简 dropper 外壳，冷启动即用 AES 解密 assets/encroc*.enc 二阶段载荷，无障碍服务 Magicstyle Service 的申请引导页与文案全部藏于该加密载荷，明文层无任何 ACTION_ACCESSIBILITY_SETTINGS 跳转与提示文本。",
  "disguise_identity": {
    "app_display_name": "Magicstyle",
    "claimed_brand_or_persona": "Magicstyle（无明确真实品牌对应，疑为随机伪装的风格/美化类应用身份）",
    "a11y_service_label": "Magicstyle Service",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 baggage.stream.gonad 与显示名 Magicstyle 无语义关联；Manifest 注册十余个随机词组的 activity/activity-alias（如 baggage.stream.gonad.bLKJUcuMiLMbuN.EgRjNorhkhvLN、baggage.stream.gonad.HoyoVHrILE.HyGChkfdoIVnT、baggage.stream.gonad.TrumpTayyip），存在多别名伪装迹象；明文 DEX 类名全部为随机英文词组拼接（kitematter.casingmuck.Hunterrefurnish、mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs）；无障碍服务类 tdbuiNelea.xappKOWtA 大小写混排无意义；Cipher 变换字符串以 XOR 常量数组混淆；引导页具体伪装手法因载荷未还原无法确认。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "Application 类 mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs（Manifest application 节点）",
      "trigger_event": "attachBaseContext() / onCreate() 被系统回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "🔧 Uygulama bağlamı başlatılıyor / 🚀 Uygulama başlatıldı",
      "shown_text_zh": "🔧 应用上下文初始化中 / 🚀 应用已启动（仅为内部调试日志，非用户界面文案）",
      "user_action_requested": "无（进程级自动执行，无需用户交互）",
      "code_anchor": "mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs.attachBaseContext / onCreate"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "Edgingraging.cheesyimmovable → Hunterrefurnish.backstabretool → partyflaring.womanlessatypical.Refiningrepacking.bobblecommerce（二阶段 DEX 加载器）",
      "trigger_event": "Application.onCreate 中 footereject 调用链自动执行",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "✅ Şifre çözme başarılı",
      "shown_text_zh": "✅ 解密成功（内部日志）",
      "user_action_requested": "无",
      "code_anchor": "kitematter.casingmuck.Edgingraging.cheesyimmovable → kitematter.casingmuck.Hunterrefurnish.backstabretool"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "assets/encroc1.enc / encroc2.enc / encroc3.enc 解密后得到的二阶段 DEX 内 Activity（类名未知）",
      "trigger_event": "二阶段载荷加载完成后由载荷内部逻辑决定（不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（明文层无任何用户可见文案；载荷未还原）",
      "shown_text_zh": "无法获取",
      "user_action_requested": "无法静态判定（是否提供取消/跳过按钮未知）",
      "code_anchor": "#1 file:assets/encroc1.enc"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "预期为 android.settings.ACCESSIBILITY_SETTINGS 系统页（跳转代码位于加密载荷内）",
      "trigger_event": "不可静态还原；明文 classes.dex 全文检索 accessibility / ACCESSIBILITY / Settings 均无命中",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无",
      "shown_text_zh": "系统无障碍设置列表中将出现 Magicstyle Service",
      "user_action_requested": "无法静态判定（预期为开启 Magicstyle Service 开关）",
      "code_anchor": "#1 manifest:components（服务声明 baggage.stream.gonad.tdbuiNelea.xappKOWtA）"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务实现类 baggage.stream.gonad.tdbuiNelea.xappKOWtA（实现不在 classes.dex）",
      "trigger_event": "系统绑定无障碍服务后回调（onServiceConnected 等，不可静态还原）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无法获取",
      "user_action_requested": "无法静态判定",
      "code_anchor": "#1 manifest:components"
    }
  ],
  "text_presentation_locations": [
    "无任何可静态确认的用户可见引导文字：res/ 下仅有 AppCompat 等标准库资源，classes.dex 全文无 accessibility / Settings / 引导语字符串",
    "唯一明文自然语言为 com.nirvana.dropper.util.TG.send 输出的土耳其语调试日志（Logcat 层，非界面）",
    "Manifest 中唯一面向用户的文本：应用显示名 Magicstyle、无障碍服务标签 Magicstyle Service（后者会呈现在系统无障碍服务列表中）",
    "预期存在但不可静态还原的位置：assets/encroc1-3.enc 解密出的二阶段 DEX 内引导 Activity / Dialog / WebView 及其中文案"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "🔧 Uygulama bağlamı başlatılıyor",
      "text_zh": "🔧 应用上下文初始化中",
      "source_location": "com.nirvana.dropper.util.TG.send 调用点（Scrubberearplugs.attachBaseContext，硬编码）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "🚀 Uygulama başlatıldı",
      "text_zh": "🚀 应用已启动",
      "source_location": "Scrubberearplugs.onCreate 硬编码",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "tr",
      "text_verbatim": "✅ Şifre çözme başarılı",
      "text_zh": "✅ 解密成功",
      "source_location": "kitematter.casingmuck.Hunterrefurnish.backstabretool 硬编码",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "Magicstyle Service",
      "text_zh": "Magicstyle 服务（系统无障碍服务列表中显示）",
      "source_location": "AndroidManifest.xml 无障碍服务 android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态判定：明文层无任何跳转与重试逻辑，相关实现位于 AES 加密的二阶段载荷内，未能还原",
    "overlay_or_fake_settings": "不可静态判定（明文层无悬浮窗/遮罩代码，但 Manifest 申请 SYSTEM_ALERT_WINDOW 之外相关权限未能确认；实际叠层行为藏于载荷）",
    "restricted_settings_13plus_coaching": "无静态证据；未在明文 DEX 中发现应用详情页或受限设置教学相关字符串，判定需依赖载荷还原",
    "post_grant_anti_removal": "不可静态判定；Manifest 申请 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS、REQUEST_DELETE_PACKAGES、设备管理（BIND_DEVICE_ADMIN、DEVICE_ADMIN_ENABLED/DISABLED 接收器）等权限，具备反卸载/持久化能力，但自点确认或阻止撤权的具体代码未在明文层出现",
    "benign_graceful_degradation": "无（无任何良性降级路径证据）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "以冷启动为起点立即拉起 UTG 采集：应用启动（Application.onCreate 自动解密加载载荷）后极短时间内即可能直弹引导页；同时 Hook Activity 启动与 Intent，一旦观测到 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 跳转即锁定引导链",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的首个可见界面（载荷加载完成即刻弹出）",
        "page_identifier": "启动 Magicstyle 后第一个非系统 Activity；预期为带引导文案的原生 Dialog/Activity 或 WebView 容器",
        "why_most_useful": "明文层无任何引导文案，首个界面是唯一能揭示其伪装叙事（假更新/清理/反诈等）的位置，直接决定引导手法定性",
        "observable_utg_signals": ["界面标题与正文全部文本", "是否存在取消/跳过/稍后按钮及其文案", "是否可返回键退出", "Activity 全限定类名与是否为 activity-alias"]
      },
      {
        "page_role": "跳转无障碍设置前的教学/说明页",
        "page_identifier": "含「无障碍」「辅助功能」「Accessibility」「Ayarlar」「Erişilebilirlik」等字样的原生页或 WebView",
        "why_most_useful": "区分是良性透明说明还是假系统警告/教唆忽视安全提示；同时确认是否为本地 HTML 还是远端下发页面",
        "observable_utg_signals": ["页面 URL（区分 file:// 与 http(s):// 远端）", "服务名 Magicstyle Service 是否被显式指引用", "是否出现伪造系统 UI 元素（开关图形、设置标题栏）", "是否有免责/隐私承诺类话术"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中 label 为 Magicstyle Service 的条目",
        "why_most_useful": "确认跳转确实落在无障碍页、服务项真实存在，并可核对 android:description 是否被刻意留空以规避警示",
        "observable_utg_signals": ["服务项显示名与图标", "description 是否为空（Manifest 中 android:description 缺失）", "是否存在同形字/前后空白伪装"]
      },
      {
        "page_role": "从设置页返回后的拒权反馈页",
        "page_identifier": "用户未开启服务直接返回时立即重现的界面",
        "why_most_useful": "判定是否存在 onResume 死循环重跳或定时器反复拉起，这是区分诱导与强制的关键",
        "observable_utg_signals": ["返回后重新出现的界面与间隔时长", "同屏是否叠有半透明遮罩", "返回键是否被拦截"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在明显盲区：一阶段 classes.dex 仅 33 个类，全部引导逻辑在 AES 加密的 assets/encroc1-3.enc 内，密文长度非 16 字节对齐导致本地复现解密失败，二阶段 DEX 未能落地，因此引导页文案、取消按钮、拒权循环、遮罩与受限设置教学均无法静态确认；此外 assets 内大量 1024 字节 png、mp3、随机 json 属诱饵噪声。运行期 UTG 不受此加密阻碍，仍可直接捕获真实界面。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs.attachBaseContext",
    "mlbpdnmi.synthesisvelvet.tampercertainly.Scrubberearplugs.onCreate",
    "kitematter.casingmuck.Edgingraging.cheesyimmovable",
    "kitematter.casingmuck.Hunterrefurnish.backstabretool",
    "kitematter.casingmuck.Hunterrefurnish.humoroushuntsman",
    "#1 file:assets/encroc1.enc"
  ]
}
```

</details>
