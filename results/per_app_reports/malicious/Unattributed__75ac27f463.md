# MB_170__75ac27f463｜Unattributed — S.A.C ITAÚ

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：125.6s

## 1. 一句话核心结论

- **核心申请方式**：以伪造 Itaú 银行品牌和“Google Play Protect 已验证”的全屏假系统优化页冷启动锁死用户，强制开启未知来源安装后静默 Session 安装加密内嵌载荷，再由广播接收器拉起载荷并直接跳转系统无障碍设置页，自身随后自禁用清痕。
- **静态可见性说明**：一阶段壳（MainActivity 假优化页、VpnService 授权门闸、受限安装设置教学、LCG-XOR 解密、PackageInstaller Session 静默安装、跳转 ACCESSIBILITY_SETTINGS、自禁用组件）完全静态可见；但真正的无障碍服务实现、无障碍列表项名称与 android:description、获权后的叠层/引导 UI 全部位于 assets/dbliqgnjl.dat 内的加密二阶段 APK 中，需运行期解密落盘后才能静态展开，故整体判定为部分静态不可见。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`LURE_UTILITY_CLEANER_DISGUISE`（合法清理/省电/工具外衣伪装）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `75ac27f46332584b7c8ded625e75c6a019d7d90575f622922596ec0590db92ea` |
| 包名 / 年份 | `com.android.system.qspas10` / 2026 |
| 家族 / 品类 | **Unattributed**（同池样本数：13） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | S.A.C ITAÚ |
| 引导页宣称品牌/身份 | Itaú 银行（巴西），并伪装为系统级优化/安全组件（包名 com.android.system.qspas10、文案自称经 Google Play Protect 验证） |
| 系统无障碍列表服务名 | 本包内不存在无障碍服务，系统无障碍列表中无对应条目；实际列表项由二阶段载荷注册，静态不可见 |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：包名 com.android.system.qspas10 伪造 android.system 系统命名空间；界面文案使用简体葡语并宣称 ✓ Google Play Protect verificado；所有按钮与可选文本控件在构建时即 setVisibility(8) 隐藏，页面无任何取消/退出出口；字符串经 e0.a(Base64+XOR) 常量加密，内嵌 APK 以 assets 随机文件名 dbliqgnjl.dat + LCG-XOR 流加密；安装完成后通过 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 禁用 MainActivity/VpnKillService/RcvJbrzn 并 killProcess 自毁痕迹 |
| 无障碍服务类名 | `二阶段/嵌包或无直接声明` |
| 静态能力位 | `canRetrieveWindowContent=False` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `REQUEST_INSTALL_PACKAGES` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.android.system.qspas10.MainActivity（LAUNCHER，singleTop） | 用户点击桌面图标 → onCreate() → J() 构建界面、K() 起线程 | 原生Activity | **原文**：S.A.C ITAÚ / Aguarde o procedimento... / Otimizando sistema / Para continuar, ative a permissão de instalação de fontes desconhecidas nas configurações. / ✓ Google Play Protect verificado<br>**译注**：S.A.C ITAÚ / 请稍候，正在处理... / 正在优化系统 / 要继续，请在设置中开启从未知来源安装的权限 / ✓ 已通过 Google Play 保护机制验证 | 无任何可点击控件；按钮与辅助文本均 setVisibility(8)，不存在取消/跳过/退出入口，用户只能被推进到系统设置 | `com.android.system.qspas10.MainActivity.J / MainActivity.k` |
| 2 | 跳受限设置 | 系统 VPN 授权对话框（VpnService.prepare，requestCode 9999）与系统“安装未知应用”页面 | onCreate 内直接调用 l()：先 VpnService.prepare(this) 非空则 startActivityForResult(...,9999)；否则检查 canRequestPackageInstalls() | 系统设置页 | **原文**：To continue, enable installation from unknown sources in settings.<br>**译注**：要继续，请在设置中开启从未知来源安装。 | 在系统弹窗中允许 VPN 连接、在系统设置中为 com.android.system.qspas10 开启“安装未知应用” | `com.android.system.qspas10.MainActivity.l` |
| 3 | 拒权反馈循环 | MainActivity（onResume / onActivityResult 回到 l()） | 用户从系统设置页返回或点击拒绝 → onActivityResult 延时 150ms 调 l()；onResume 亦调 l() | 原生Activity | **原文**：Aguarde o procedimento... / Otimizando sistema<br>**译注**：请稍候，正在处理... / 正在优化系统 | 无取消入口；未授权则界面停留在假进度页并被反复带回系统授权页，直到权限被授予 | `com.android.system.qspas10.MainActivity.onResume / onActivityResult` |
| 4 | 获权后动作（载荷解密与静默安装） | MainActivity 内线程 j → L()；界面切换为 Installing... | canRequestPackageInstalls() 为 true 且 VpnService.prepare 返回 null → j.set(true) → new Thread(new j(this)).start() | 原生Activity | **原文**：Installing...<br>**译注**：正在安装... | 无操作；用户无感知地完成 assets/dbliqgnjl.dat 解密与 PackageInstaller Session 静默安装（置位 INSTALL_ALLOW_DOWNGRADE 等标志） | `com.android.system.qspas10.MainActivity.L / MainActivity.j` |
| 5 | 获权后动作（拉起载荷并跳无障碍设置） | RcvJbrzn（PACKAGE_ADDED/MY_PACKAGE_REPLACED 广播接收器）→ 系统无障碍设置页 | Session commit 回调触发 RcvJbrzn.onReceive（STATUS_PACKAGE_INSTALLED）→ e() → 线程 t → d() | 系统无障碍页 | **原文**：无（本包不注入任何无障碍引导文本，直接 startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))）<br>**译注**：无；应用直接打开系统“无障碍”设置列表，由二阶段载荷的列表项与引导界面接手 | 在系统无障碍列表中手动找到并开启二阶段载荷注册的无障碍服务（本包不提供任何说明文字，用户需自行在列表中辨识） | `com.android.system.qspas10.RcvJbrzn.d` |
| 6 | 获权后动作（自毁清痕） | RcvJbrzn.c() 禁用 MainActivity / VpnKillService / RcvJbrzn | d() 循环结束或检测到目标包进程已连续两次存在 → c(context) → Thread.sleep(300) → Process.killProcess(myPid()) | 不可静态还原 | 无 | 无 | `com.android.system.qspas10.RcvJbrzn.c` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- MainActivity.J() 中纯代码构建的全屏 LinearLayout：标题 TextView 硬编码 "S.A.C ITAÚ"、副标题 "Aguarde o procedimento..."（#01875F 仿 Google 绿）、卡片标题 "Otimizando sistema"、底部 "✓ Google Play Protect verificado"
- MainActivity.k() 返回的多语言硬编码字符串，填入卡片正文 TextView this.c（pt/de/es/fr/it 及英文默认），内容为“去设置开启未知来源安装”
- MainActivity.l()/L() 在安装阶段把 this.c 文案替换为 "Installing..."，onCreate 的 RETRY 分支替换为 "Retrying..."（硬编码英文，未走多语言表）
- res/values/strings.xml 中仅有 app_name = S.A.C ITAÚ 及通话通知类字符串，无任何无障碍说明文案；无 assets/*.html、无 WebView 页面、无布局 XML 引导页
- 系统无障碍设置列表中的服务项与 android:description：本包 Manifest 未声明任何 AccessibilityService，故本包不提供该项文字；该文字位于加密的 assets/dbliqgnjl.dat 二阶段 APK 内，静态不可见

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| pt | S.A.C ITAÚ | S.A.C ITAÚ（巴西 Itaú 银行品牌名） | `res/values/strings.xml#L3（app_name）及 MainActivity.J 硬编码` | 未知 |
| pt | Aguarde o procedimento... | 请稍候，正在处理... | `MainActivity.J 硬编码` | 良性透明说明 |
| pt | Otimizando sistema | 正在优化系统 | `MainActivity.J 硬编码` | 清理工具伪装 |
| pt | Para continuar, ative a permissão de instalação de fontes desconhecidas nas configurações. | 要继续，请在设置中开启从未知来源安装的权限。 | `MainActivity.k()（pt 分支，另有 de/es/fr/it/en 分支）` | 受限设置分步教学 |
| en | To continue, enable installation from unknown sources in settings. | 要继续，请在设置中开启从未知来源安装。 | `MainActivity.k() default 分支` | 受限设置分步教学 |
| pt | ✓ Google Play Protect verificado | ✓ 已通过 Google Play 保护机制验证 | `MainActivity.J 硬编码` | 假反诈安全 |
| en | Installing... | 正在安装... | `MainActivity.l() 硬编码` | 假更新 |
| en | Retrying... | 正在重试... | `MainActivity.onCreate RETRY 分支硬编码` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：用户从 VPN 授权页或“安装未知应用”设置页返回时，onActivityResult 延时 150ms、onResume 立即再次调用 l()，重新检查 VpnService.prepare 与 canRequestPackageInstalls；任一未满足即重新 startActivityForResult 拉起系统页，界面停留在不可操作的假进度页，形成无限重跳，直至两项权限全部授予
- **遮罩叠层 / 高仿系统设置页**：本包不叠放悬浮窗、不使用 SYSTEM_ALERT_WINDOW，也不伪造高仿系统无障碍开关页；伪装对象是 MainActivity 自身的全屏原生“系统优化”进度页（含品牌图标、进度条、Google Play Protect 徽标），全部控件不可点击且无取消入口
- **Android 13+ 受限设置（Restricted Settings）应对**：有，但仅指向“未知来源安装”：文案为“Para continuar, ative a permissão de instalação de fontes desconhecidas nas configurações.”，通过 canRequestPackageInstalls() 判定并依赖 REQUEST_INSTALL_PACKAGES 权限拉起系统页；未教用户进应用详情右上角菜单开启“允许受限设置”，改以 PackageInstaller Session（显式置位 i3|6、SDK≥31 时 4194310|i3）绕过部分安装确认环节
- **获权后即时行为与防撤权机制**：本包未实现无障碍服务，故无监听设置页、GLOBAL_ACTION_BACK/HOME 或自点确认等撤权对抗；但存在另一类自毁式反取证：安装完成后 RcvJbrzn.c() 用 setComponentEnabledSetting(..., 2, 1) 禁用 MainActivity、VpnKillService、RcvJbrzn 并 Process.killProcess(myPid())，抹除一阶段痕迹
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：两个最佳拉起时刻：① 冷启动后 MainActivity 首帧渲染完成（出现白色全屏“Otimizando sistema”假进度页）时立即拉起；② 监测到 com.android.system.qspas10 调用 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（该动作由 RcvJbrzn.d 在载荷安装完成后触发），此时无障碍列表即将弹出，最利于捕获列表项与后续叠层
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在两处盲区：① 无障碍服务本体、服务标签、android:description 与获权后的叠层/引导 UI 全部位于 assets/dbliqgnjl.dat 内 LCG-XOR 加密的二阶段 APK，静态不可见，纯静态检测只能看到“跳转 ACCESSIBILITY_SETTINGS”而无任何引导文案；② 一阶段为温和外壳（无悬浮窗、无 WebView、无图片引导、仅原生假进度页），且安装完成后自动禁用全部组件并 killProcess，UTG 事后回溯时桌面图标与组件可能已消失，需在首次冷启动即抓取。另注：本包未加壳（静态加壳为 False），运行期 UTG 不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动伪装的假系统优化页（锁定用户、无取消入口）** | com.android.system.qspas10.MainActivity，全屏白底 LinearLayout，含应用图标、"S.A.C ITAÚ"、"Aguarde o procedimento..."、"Otimizando sistema"、"✓ Google Play Protect verificado"、水平进度条 | 这是应用对用户呈现的全部“理由”，其不可取消性与品牌冒充决定了诱导性质，且是本包唯一可见 UI，可直接与二阶段载荷做责任切分 | text="S.A.C ITAÚ" 与 package=com.android.system.qspas10 的身份不一致；text="✓ Google Play Protect verificado" 的伪造安全背书；页面无可点击按钮/无取消控件（clickable 节点为空）；无 WebView、无 ImageView 大图（图标除外），可确认非图诱导 |
| **跳转前受限设置教学页（未知来源安装）** | 同一 MainActivity 内卡片正文切换为 "Para continuar, ative a permissão de instalação de fontes desconhecidas nas configurações."，或 "Installing..." | 区分“良性需要权限”与“为静默安装铺路”的关键：文案要求开启未知来源，随后立即进入 Installing 状态，暴露 dropper 意图 | text 含 "origens desconhecidas" / "unknown sources"；文案随系统语言变化（pt/en/de/es/fr/it）；文案变化后短时间内出现 "Installing..." |
| **系统“安装未知应用”设置页（跳受限设置）** | Settings 的 com.android.system.qspas10 安装未知应用开关页（由 canRequestPackageInstalls 判定后拉起） | 证明应用主动把用户导向 13+ 受限安装权限，是安装器绕过的必要前置；同时可观察用户返回后是否被立即重跳（拒权循环证据） | 页面归属 Settings 且含目标包名；返回 MainActivity 后 150ms 内再次跳转同一设置页（onResume/onActivityResult 重跳） |
| **系统无障碍服务列表项（二阶段载荷注册的服务）** | Settings → 无障碍 → 已下载的服务列表中新增条目（由二阶段 APK 声明，静态不可知），及可能出现的叠层引导窗 | 本包只负责打开该页，真正的服务名/description/叠层引导在此暴露，是判定“如何一步步引导开启无障碍”的关键落点，也是静态分析的最大缺口 | 无障碍列表新增条目的 text 与 summary（服务标签、description）；列表页上层是否叠加悬浮窗/半透明遮罩（window 层数、非 Settings 包名的可见窗口）；从设置页返回后是否被再次拉起（RcvJbrzn.d 循环 4 次 + 800/1200/1800ms 间隔） |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.android.system.qspas10.MainActivity.J`
- `com.android.system.qspas10.MainActivity.k`
- `com.android.system.qspas10.MainActivity.l`
- `com.android.system.qspas10.MainActivity.L`
- `com.android.system.qspas10.RcvJbrzn.d`
- `com.android.system.qspas10.RcvJbrzn.c`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论要点

**核心发现：本包是一个只负责投递的壳（Dropper），自身不包含无障碍服务，也不展示无障碍引导界面。**

1. **入口与伪装**：Manifest 只有一个 LAUNCHER Activity [MainActivity](<resource-unit:#1.dex1 code:com.android.system.qspas10.MainActivity#onCreate>)。启动时，[J()](<resource-unit:#1.dex1 code:com.android.system.qspas10.MainActivity#J>) 用纯代码构建全屏白色“系统优化”页面：银行品牌 `S.A.C ITAÚ`、`Aguarde o procedimento...`、`Otimizando sistema`、`✓ Google Play Protect verificado`。所有按钮和文本控件都在创建时被 `setVisibility(8)` 隐藏，**界面没有任何取消、跳过或退出控件**。包名 `com.android.system.qspas10` 伪造系统命名空间。
2. **冷启动强制推进**：[l()](<resource-unit:#1.dex1 code:com.android.system.qspas10.MainActivity#l>) 在 onCreate 中直接调用，依次检查 `VpnService.prepare()`（requestCode 9999）与 `canRequestPackageInstalls()`。不满足时，界面停在假进度页，并显示由 [k()](<resource-unit:#1.dex1 code:com.android.system.qspas10.MainActivity#k>) 按语言返回的“去设置开启未知来源安装”文案（pt/de/es/fr/it/en）。[onResume()](<resource-unit:#1.dex1 code:com.android.system.qspas10.MainActivity#onResume>) 与 [onActivityResult()](<resource-unit:#1.dex1 code:com.android.system.qspas10.MainActivity#onActivityResult>) 在用户从系统页返回后 150 ms 内再次调用 `l()`，**形成用户拒绝后立即重跳的循环**，且无降级路径。
3. **二阶段载荷（加密内嵌）**：[L()](<resource-unit:#1.dex1 code:com.android.system.qspas10.MainActivity#L>) 用 LCG-XOR 流（`j=(j*1664525+1013904223)&0xFFFFFFFF`，取 `(j>>24)&0xFF`）解密 [assets/dbliqgnjl.dat](<resource-unit:#1 file:assets/dbliqgnjl.dat>)，得到内嵌 APK，再反射调用 `PackageInstaller.createSession/openSession/commit`，显式置位 `i3|6` / SDK≥31 时 `4194310|i3`（INSTALL_ALLOW_DOWNGRADE 等）执行 Session 静默安装。`PendingIntent` 回调指向 `RcvJbrzn`；失败时每 3–5 秒无限重试。
4. **无障碍设置页的跳转点**：[RcvJbrzn.d()](<resource-unit:#1.dex1 code:com.android.system.qspas10.RcvJbrzn#d>) 在载荷安装后循环最多 4 次拉起目标包（`getLaunchIntentForPackage`，回退到 `<pkg>.A1`），随后无条件调用 `startActivity(new Intent("android.settings.ACCESSIBILITY_SETTINGS"))`（`NEW_TASK|CLEAR_TASK`），并调用 [c()](<resource-unit:#1.dex1 code:com.android.system.qspas10.RcvJbrzn#c>) 用 `setComponentEnabledSetting(..., 2, 1)` 禁用 MainActivity / VpnKillService / RcvJbrzn 后执行 `killProcess`，**抹掉一阶段的可见痕迹**。
5. **无障碍引导归属**：Manifest 无 `BIND_ACCESSIBILITY_SERVICE` 服务、无 `accessibility-service` 元数据、无 `android:description`；DEX 中无 `AccessibilityService` 子类（`accessibility` 命中全部是 androidx `a0` 的 `AccessibilityManager` 事件工具）。因此**无障碍列表项、说明文字、叠层指引均在二阶段载荷内，静态不可见**；本包的作用只是把用户直接推送到系统无障碍设置页。
6. **其他**：`j()` 通过 `setHiddenApiExemptions(["L"])` 绕过隐藏 API 限制；`VpnKillService` 声明为 VPN 服务并有 `killInstantly` 反射调用。

已登记风险 R-001（high / fraud_phishing）。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "一阶段壳（MainActivity 假优化页、VpnService 授权门闸、受限安装设置教学、LCG-XOR 解密、PackageInstaller Session 静默安装、跳转 ACCESSIBILITY_SETTINGS、自禁用组件）完全静态可见；但真正的无障碍服务实现、无障碍列表项名称与 android:description、获权后的叠层/引导 UI 全部位于 assets/dbliqgnjl.dat 内的加密二阶段 APK 中，需运行期解密落盘后才能静态展开，故整体判定为部分静态不可见。",
  "summary_one_liner": "以伪造 Itaú 银行品牌和“Google Play Protect 已验证”的全屏假系统优化页冷启动锁死用户，强制开启未知来源安装后静默 Session 安装加密内嵌载荷，再由广播接收器拉起载荷并直接跳转系统无障碍设置页，自身随后自禁用清痕。",
  "disguise_identity": {
    "app_display_name": "S.A.C ITAÚ",
    "claimed_brand_or_persona": "Itaú 银行（巴西），并伪装为系统级优化/安全组件（包名 com.android.system.qspas10、文案自称经 Google Play Protect 验证）",
    "a11y_service_label": "本包内不存在无障碍服务，系统无障碍列表中无对应条目；实际列表项由二阶段载荷注册，静态不可见",
    "identity_mismatch": true,
    "obfuscation_tricks": "包名 com.android.system.qspas10 伪造 android.system 系统命名空间；界面文案使用简体葡语并宣称 ✓ Google Play Protect verificado；所有按钮与可选文本控件在构建时即 setVisibility(8) 隐藏，页面无任何取消/退出出口；字符串经 e0.a(Base64+XOR) 常量加密，内嵌 APK 以 assets 随机文件名 dbliqgnjl.dat + LCG-XOR 流加密；安装完成后通过 setComponentEnabledSetting(COMPONENT_ENABLED_STATE_DISABLED) 禁用 MainActivity/VpnKillService/RcvJbrzn 并 killProcess 自毁痕迹"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.android.system.qspas10.MainActivity（LAUNCHER，singleTop）",
      "trigger_event": "用户点击桌面图标 → onCreate() → J() 构建界面、K() 起线程",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "S.A.C ITAÚ / Aguarde o procedimento... / Otimizando sistema / Para continuar, ative a permissão de instalação de fontes desconhecidas nas configurações. / ✓ Google Play Protect verificado",
      "shown_text_zh": "S.A.C ITAÚ / 请稍候，正在处理... / 正在优化系统 / 要继续，请在设置中开启从未知来源安装的权限 / ✓ 已通过 Google Play 保护机制验证",
      "user_action_requested": "无任何可点击控件；按钮与辅助文本均 setVisibility(8)，不存在取消/跳过/退出入口，用户只能被推进到系统设置",
      "code_anchor": "com.android.system.qspas10.MainActivity.J / MainActivity.k"
    },
    {
      "step": 2,
      "stage": "跳受限设置",
      "screen_or_component": "系统 VPN 授权对话框（VpnService.prepare，requestCode 9999）与系统“安装未知应用”页面",
      "trigger_event": "onCreate 内直接调用 l()：先 VpnService.prepare(this) 非空则 startActivityForResult(...,9999)；否则检查 canRequestPackageInstalls()",
      "ui_carrier": "系统设置页",
      "shown_text_verbatim": "To continue, enable installation from unknown sources in settings.",
      "shown_text_zh": "要继续，请在设置中开启从未知来源安装。",
      "user_action_requested": "在系统弹窗中允许 VPN 连接、在系统设置中为 com.android.system.qspas10 开启“安装未知应用”",
      "code_anchor": "com.android.system.qspas10.MainActivity.l"
    },
    {
      "step": 3,
      "stage": "拒权反馈循环",
      "screen_or_component": "MainActivity（onResume / onActivityResult 回到 l()）",
      "trigger_event": "用户从系统设置页返回或点击拒绝 → onActivityResult 延时 150ms 调 l()；onResume 亦调 l()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Aguarde o procedimento... / Otimizando sistema",
      "shown_text_zh": "请稍候，正在处理... / 正在优化系统",
      "user_action_requested": "无取消入口；未授权则界面停留在假进度页并被反复带回系统授权页，直到权限被授予",
      "code_anchor": "com.android.system.qspas10.MainActivity.onResume / onActivityResult"
    },
    {
      "step": 4,
      "stage": "获权后动作（载荷解密与静默安装）",
      "screen_or_component": "MainActivity 内线程 j → L()；界面切换为 Installing...",
      "trigger_event": "canRequestPackageInstalls() 为 true 且 VpnService.prepare 返回 null → j.set(true) → new Thread(new j(this)).start()",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Installing...",
      "shown_text_zh": "正在安装...",
      "user_action_requested": "无操作；用户无感知地完成 assets/dbliqgnjl.dat 解密与 PackageInstaller Session 静默安装（置位 INSTALL_ALLOW_DOWNGRADE 等标志）",
      "code_anchor": "com.android.system.qspas10.MainActivity.L / MainActivity.j"
    },
    {
      "step": 5,
      "stage": "获权后动作（拉起载荷并跳无障碍设置）",
      "screen_or_component": "RcvJbrzn（PACKAGE_ADDED/MY_PACKAGE_REPLACED 广播接收器）→ 系统无障碍设置页",
      "trigger_event": "Session commit 回调触发 RcvJbrzn.onReceive（STATUS_PACKAGE_INSTALLED）→ e() → 线程 t → d()",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（本包不注入任何无障碍引导文本，直接 startActivity(new Intent(\"android.settings.ACCESSIBILITY_SETTINGS\"))）",
      "shown_text_zh": "无；应用直接打开系统“无障碍”设置列表，由二阶段载荷的列表项与引导界面接手",
      "user_action_requested": "在系统无障碍列表中手动找到并开启二阶段载荷注册的无障碍服务（本包不提供任何说明文字，用户需自行在列表中辨识）",
      "code_anchor": "com.android.system.qspas10.RcvJbrzn.d"
    },
    {
      "step": 6,
      "stage": "获权后动作（自毁清痕）",
      "screen_or_component": "RcvJbrzn.c() 禁用 MainActivity / VpnKillService / RcvJbrzn",
      "trigger_event": "d() 循环结束或检测到目标包进程已连续两次存在 → c(context) → Thread.sleep(300) → Process.killProcess(myPid())",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无；一阶段应用组件被禁用并结束进程，桌面图标失效，用户难以回溯是谁打开了无障碍设置页",
      "user_action_requested": "无",
      "code_anchor": "com.android.system.qspas10.RcvJbrzn.c"
    }
  ],
  "text_presentation_locations": [
    "MainActivity.J() 中纯代码构建的全屏 LinearLayout：标题 TextView 硬编码 \"S.A.C ITAÚ\"、副标题 \"Aguarde o procedimento...\"（#01875F 仿 Google 绿）、卡片标题 \"Otimizando sistema\"、底部 \"✓ Google Play Protect verificado\"",
    "MainActivity.k() 返回的多语言硬编码字符串，填入卡片正文 TextView this.c（pt/de/es/fr/it 及英文默认），内容为“去设置开启未知来源安装”",
    "MainActivity.l()/L() 在安装阶段把 this.c 文案替换为 \"Installing...\"，onCreate 的 RETRY 分支替换为 \"Retrying...\"（硬编码英文，未走多语言表）",
    "res/values/strings.xml 中仅有 app_name = S.A.C ITAÚ 及通话通知类字符串，无任何无障碍说明文案；无 assets/*.html、无 WebView 页面、无布局 XML 引导页",
    "系统无障碍设置列表中的服务项与 android:description：本包 Manifest 未声明任何 AccessibilityService，故本包不提供该项文字；该文字位于加密的 assets/dbliqgnjl.dat 二阶段 APK 内，静态不可见"
  ],
  "verbatim_texts": [
    {
      "lang": "pt",
      "text_verbatim": "S.A.C ITAÚ",
      "text_zh": "S.A.C ITAÚ（巴西 Itaú 银行品牌名）",
      "source_location": "res/values/strings.xml#L3（app_name）及 MainActivity.J 硬编码",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "pt",
      "text_verbatim": "Aguarde o procedimento...",
      "text_zh": "请稍候，正在处理...",
      "source_location": "MainActivity.J 硬编码",
      "rhetorical_frame": "良性透明说明"
    },
    {
      "lang": "pt",
      "text_verbatim": "Otimizando sistema",
      "text_zh": "正在优化系统",
      "source_location": "MainActivity.J 硬编码",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "pt",
      "text_verbatim": "Para continuar, ative a permissão de instalação de fontes desconhecidas nas configurações.",
      "text_zh": "要继续，请在设置中开启从未知来源安装的权限。",
      "source_location": "MainActivity.k()（pt 分支，另有 de/es/fr/it/en 分支）",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "To continue, enable installation from unknown sources in settings.",
      "text_zh": "要继续，请在设置中开启从未知来源安装。",
      "source_location": "MainActivity.k() default 分支",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "pt",
      "text_verbatim": "✓ Google Play Protect verificado",
      "text_zh": "✓ 已通过 Google Play 保护机制验证",
      "source_location": "MainActivity.J 硬编码",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Installing...",
      "text_zh": "正在安装...",
      "source_location": "MainActivity.l() 硬编码",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Retrying...",
      "text_zh": "正在重试...",
      "source_location": "MainActivity.onCreate RETRY 分支硬编码",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "用户从 VPN 授权页或“安装未知应用”设置页返回时，onActivityResult 延时 150ms、onResume 立即再次调用 l()，重新检查 VpnService.prepare 与 canRequestPackageInstalls；任一未满足即重新 startActivityForResult 拉起系统页，界面停留在不可操作的假进度页，形成无限重跳，直至两项权限全部授予",
    "overlay_or_fake_settings": "本包不叠放悬浮窗、不使用 SYSTEM_ALERT_WINDOW，也不伪造高仿系统无障碍开关页；伪装对象是 MainActivity 自身的全屏原生“系统优化”进度页（含品牌图标、进度条、Google Play Protect 徽标），全部控件不可点击且无取消入口",
    "restricted_settings_13plus_coaching": "有，但仅指向“未知来源安装”：文案为“Para continuar, ative a permissão de instalação de fontes desconhecidas nas configurações.”，通过 canRequestPackageInstalls() 判定并依赖 REQUEST_INSTALL_PACKAGES 权限拉起系统页；未教用户进应用详情右上角菜单开启“允许受限设置”，改以 PackageInstaller Session（显式置位 i3|6、SDK≥31 时 4194310|i3）绕过部分安装确认环节",
    "post_grant_anti_removal": "本包未实现无障碍服务，故无监听设置页、GLOBAL_ACTION_BACK/HOME 或自点确认等撤权对抗；但存在另一类自毁式反取证：安装完成后 RcvJbrzn.c() 用 setComponentEnabledSetting(..., 2, 1) 禁用 MainActivity、VpnKillService、RcvJbrzn 并 Process.killProcess(myPid())，抹除一阶段痕迹",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "两个最佳拉起时刻：① 冷启动后 MainActivity 首帧渲染完成（出现白色全屏“Otimizando sistema”假进度页）时立即拉起；② 监测到 com.android.system.qspas10 调用 startActivity(android.settings.ACCESSIBILITY_SETTINGS) 的瞬间（该动作由 RcvJbrzn.d 在载荷安装完成后触发），此时无障碍列表即将弹出，最利于捕获列表项与后续叠层",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动伪装的假系统优化页（锁定用户、无取消入口）",
        "page_identifier": "com.android.system.qspas10.MainActivity，全屏白底 LinearLayout，含应用图标、\"S.A.C ITAÚ\"、\"Aguarde o procedimento...\"、\"Otimizando sistema\"、\"✓ Google Play Protect verificado\"、水平进度条",
        "why_most_useful": "这是应用对用户呈现的全部“理由”，其不可取消性与品牌冒充决定了诱导性质，且是本包唯一可见 UI，可直接与二阶段载荷做责任切分",
        "observable_utg_signals": ["text=\"S.A.C ITAÚ\" 与 package=com.android.system.qspas10 的身份不一致", "text=\"✓ Google Play Protect verificado\" 的伪造安全背书", "页面无可点击按钮/无取消控件（clickable 节点为空）", "无 WebView、无 ImageView 大图（图标除外），可确认非图诱导"]
      },
      {
        "page_role": "跳转前受限设置教学页（未知来源安装）",
        "page_identifier": "同一 MainActivity 内卡片正文切换为 \"Para continuar, ative a permissão de instalação de fontes desconhecidas nas configurações.\"，或 \"Installing...\"",
        "why_most_useful": "区分“良性需要权限”与“为静默安装铺路”的关键：文案要求开启未知来源，随后立即进入 Installing 状态，暴露 dropper 意图",
        "observable_utg_signals": ["text 含 \"origens desconhecidas\" / \"unknown sources\"", "文案随系统语言变化（pt/en/de/es/fr/it）", "文案变化后短时间内出现 \"Installing...\""]
      },
      {
        "page_role": "系统“安装未知应用”设置页（跳受限设置）",
        "page_identifier": "Settings 的 com.android.system.qspas10 安装未知应用开关页（由 canRequestPackageInstalls 判定后拉起）",
        "why_most_useful": "证明应用主动把用户导向 13+ 受限安装权限，是安装器绕过的必要前置；同时可观察用户返回后是否被立即重跳（拒权循环证据）",
        "observable_utg_signals": ["页面归属 Settings 且含目标包名", "返回 MainActivity 后 150ms 内再次跳转同一设置页（onResume/onActivityResult 重跳）"]
      },
      {
        "page_role": "系统无障碍服务列表项（二阶段载荷注册的服务）",
        "page_identifier": "Settings → 无障碍 → 已下载的服务列表中新增条目（由二阶段 APK 声明，静态不可知），及可能出现的叠层引导窗",
        "why_most_useful": "本包只负责打开该页，真正的服务名/description/叠层引导在此暴露，是判定“如何一步步引导开启无障碍”的关键落点，也是静态分析的最大缺口",
        "observable_utg_signals": ["无障碍列表新增条目的 text 与 summary（服务标签、description）", "列表页上层是否叠加悬浮窗/半透明遮罩（window 层数、非 Settings 包名的可见窗口）", "从设置页返回后是否被再次拉起（RcvJbrzn.d 循环 4 次 + 800/1200/1800ms 间隔）"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在两处盲区：① 无障碍服务本体、服务标签、android:description 与获权后的叠层/引导 UI 全部位于 assets/dbliqgnjl.dat 内 LCG-XOR 加密的二阶段 APK，静态不可见，纯静态检测只能看到“跳转 ACCESSIBILITY_SETTINGS”而无任何引导文案；② 一阶段为温和外壳（无悬浮窗、无 WebView、无图片引导、仅原生假进度页），且安装完成后自动禁用全部组件并 killProcess，UTG 事后回溯时桌面图标与组件可能已消失，需在首次冷启动即抓取。另注：本包未加壳（静态加壳为 False），运行期 UTG 不受影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "LURE_UTILITY_CLEANER_DISGUISE",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.android.system.qspas10.MainActivity.J",
    "com.android.system.qspas10.MainActivity.k",
    "com.android.system.qspas10.MainActivity.l",
    "com.android.system.qspas10.MainActivity.L",
    "com.android.system.qspas10.RcvJbrzn.d",
    "com.android.system.qspas10.RcvJbrzn.c"
  ]
}
```

</details>
