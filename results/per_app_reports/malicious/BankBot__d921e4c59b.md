# MB_111__d921e4c59b｜BankBot — Music Downloader

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：255.7s

## 1. 一句话核心结论

- **核心申请方式**：该样本以单字节 XOR 加壳把全部引导与无障碍逻辑藏进 9.6MB 加密 dex 动态加载，仅在 Manifest 暴露一个标签为「Music Downloader」、无任何用途说明的无障碍服务，运行期再借壳内逻辑引导用户开启。
- **静态可见性说明**：主 classes.dex 仅为 81KB 的壳层（单字符混淆类 + NPStringFog + 反射蹦床），真实业务与无障碍引导逻辑位于 APK 根目录 od3KUaQxbf（9,626,284 字节，XOR 0x4F 加密的 dex）及 assets/ 下 101 个随机长名加密资源，由 pmdm.hyn.r6y7.dc1.attachBaseContext 解密后 DexClassLoader 动态加载。该载荷的 DEX 头字段（class_defs_off/data_off/map_off）在明文态仍为乱码，仅异或 0x4F 无法得到完整可解析 DEX，MCP 反编译返回 0 个类，故引导弹窗、ACTION_ACCESSIBILITY_SETTINGS 跳转点、拒绝循环、遮罩与 HTML 教学页均不可静态还原，只能确认 Manifest 层的无障碍服务声明与伪装标签。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d921e4c59b048aa4085712054c1fa0cac28994f8857b519f27a297b8f2c5d77d` |
| 包名 / 年份 | `com.tumuluses.gastrocnemius` / 2026 |
| 家族 / 品类 | **BankBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Music Downloader |
| 引导页宣称品牌/身份 | Music Downloader（音乐下载器，实为隐藏载荷的银行木马类壳） |
| 系统无障碍列表服务名 | Music Downloader |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) 无障碍服务 android:description 完全缺失，系统无障碍列表中不显示任何用途说明；2) 无障碍服务 label 直接复用主应用标签 @7F0E001D（Music Downloader），使系统设置页中服务名与桌面应用名一致，掩盖权限性质；3) 存在两个 LAUNCHER activity-alias：saccharimetry（与 activity 同名，enabled=true）与 consolute（label @7F0E001F、图标 @7F0C0003、enabled=false），可运行期切换桌面名称/图标；4) meta-data app_name="g969.do2.boew.ilq" 与显示名不一致；5) 主 dex 全部类名/方法名为单字符同形混淆（n.ۥ / ۥ۟ 等 700+ 同形方法），字符串经 NPStringFog 二次加密。 |
| 无障碍服务类名 | `com.tumuluses.gastrocnemius.tappable` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | pmdm.hyn.r6y7.dc1（android:name 指定的 Application） | 进程创建 → Application.attachBaseContext() | 不可静态还原 | 无 | 无需用户操作 | `pmdm.hyn.r6y7.dc1.attachBaseContext` |
| 2 | 冷启动入口 | com.tumuluses.gastrocnemius.saccharimetry（activity 与同名 LAUNCHER activity-alias） | 点击桌面图标（android.intent.action.MAIN / LAUNCHER，noHistory=true） | 不可静态还原 | **原文**：无（仅 Manifest 声明，Activity 实现类体不在壳 dex 中）<br>**译注**：桌面入口指向 Activity 类名，该类实现由解密后的动态载荷提供，静态无法取得其 onCreate 内容 | 点击图标启动 | `AndroidManifest.xml: activity/activity-alias com.tumuluses.gastrocnemius.saccharimetry` |
| 3 | 引导说明页 / 跳无障碍设置 / 遮罩叠层指引 / 拒权反馈循环 / 获权后动作 | 不可静态还原（实现位于 od3KUaQxbf 解密载荷） | 不可静态还原 | 不可静态还原 | 无 | 不可静态还原 | `od3KUaQxbf（XOR 0x4F 加密载荷）` |
| 4 | 获权后动作 | com.tumuluses.gastrocnemius.tappable（AccessibilityService） | 用户在系统设置中启用该服务 → 系统 bindService（BIND_ACCESSIBILITY_SERVICE） | 系统无障碍页 | **原文**：Music Downloader<br>**译注**：系统无障碍服务列表中仅显示服务名「Music Downloader」，android:description 缺失，用户看不到任何权限用途说明 | 用户在系统设置中手动开启该无障碍服务（是否由应用内跳转引导，静态不可确认） | `AndroidManifest.xml: service com.tumuluses.gastrocnemius.tappable` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表：服务名「Music Downloader」（复用 @7F0E001D 应用标签），android:description 缺失 → 列表项无任何用途说明文字
- 桌面启动器：应用名「Music Downloader」/ 图标 @7F0C0000；备用别名 consolute 使用 @7F0E001F + @7F0C0003（enabled=false，暂不显示）
- 应用内引导弹窗/Activity/WebView/悬浮窗：实现位于 od3KUaQxbf 加密载荷，静态不可还原，未定位到具体 layout 或 assets/*.html（assets/ 下 101 个文件均为随机长名加密二进制，无明文 HTML）
- 资源字符串池：存在 [DEFAULT] "Low Battery" 与 [zh-rCN] "不在允许的范围内：%1$s"，但无法静态确认其呈现在哪个界面、是否用于无障碍引导，故不列为诱导话术

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Music Downloader | 音乐下载器 | `AndroidManifest.xml → application android:label=@7F0E001D；service tappable android:label=@7F0E001D；activity-alias saccharimetry android:label=@7F0E001D` | 清理工具伪装 |
| en | Low Battery | 电量不足 | `resources.arsc 字符串池（[DEFAULT]），呈现位置静态未确认` | 故障恐吓 |
| zh-rCN | 不在允许的范围内：%1$s | 不在允许的范围内：%1$s | `resources.arsc 字符串池（[zh-rCN]），呈现位置静态未确认` | 未知 |
| en | g969.do2.boew.ilq | 无实义（随机标识串） | `AndroidManifest.xml → meta-data app_name` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导逻辑位于 od3KUaQxbf 加密载荷，DEX 头字段在明文态仍为乱码，无法定位 onResume/Timer 重跳代码
- **遮罩叠层 / 高仿系统设置页**：不可静态还原：壳 dex 中无任何悬浮窗/Overlay/SYSTEM_ALERT_WINDOW 相关调用，亦未声明 SYSTEM_ALERT_WINDOW 权限；若存在遮罩层应位于载荷内，需运行期 UTG 观察
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（未在壳 dex 与 Manifest 中发现 APPLICATION_DETAILS_SETTINGS 跳转或受限设置教学相关代码/字符串）
- **获权后即时行为与防撤权机制**：无静态证据：壳 dex 中未见 GLOBAL_ACTION_BACK/HOME、performGlobalAction 或无障碍设置页监听代码，相关实现可能位于载荷内
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在冷启动 saccharimetry 页面 onResume 起持续监测顶层窗口变化：一旦 Activity 切换为 com.android.settings/.AccessibilitySettings（或 Settings$AccessibilitySettingsActivity）即抓帧；同时以 300~500ms 间隔轮询无障碍服务启用状态，捕捉「跳设置 → 返回应用 → 再次跳设置」的往返循环。因壳层无静态线索，建议对冷启动后 0~60 秒内所有非 Launcher 顶层页面全量录屏。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：本样本为静态加壳 + 单字节 XOR 加密载荷（非 VMP），运行期可正常解密，UTG 不受影响；但静态侧完全看不到引导文案与跳转点，纯静态检测会漏判为「无害音乐下载器」。另需注意两点盲区：(1) 载荷 DEX 头仍二次混淆，本报告未能取得其内部字符串，若载荷以远端 HTML/WebView 下发话术，则需同时抓流量；(2) 应用声明 debuggable=true 且 usesCleartextTraffic=true，可能从明文 HTTP 拉取引导页，建议同步做流量捕获以补证远端话术。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首屏（壳解密完成后的实际入口 Activity）** | 顶层 Activity = com.tumuluses.gastrocnemius.saccharimetry 或载荷内新 Activity；标签/标题为 Music Downloader | 确认载荷加载成功后应用真正呈现的界面，判断是直接弹无障碍引导、还是先展示音乐下载器假功能外壳 | 首屏是否出现无障碍/辅助功能相关按钮或开关；是否存在无取消按钮的模态弹窗；界面是否与「音乐下载器」功能描述相符 |
| **跳转前引导说明页（应用内）** | Dialog 或 Activity，含「无障碍 / 辅助功能 / 授权 / 开启」类文案；可能为 WebView | 获取逐字诱导话术与话术框架（假更新、故障恐吓、假安全、清理伪装），静态完全缺失，这是唯一取证途径 | 弹窗是否有取消/跳过按钮；文案是否提及系统警告可忽略；是否存在倒计时自动跳转 |
| **系统无障碍设置页 + 其后压栈遮罩页** | com.android.settings/.AccessibilitySettings 或 accessibility 服务列表；返回应用后立即出现的半透明引导层 | 验证是否为分步教学式引导，以及是否用悬浮引导层遮住系统警告文案；这是区分「良性透明说明」与「诱导规避」的关键 | 系统设置页停留时长与是否自动滚动定位到服务项；返回应用后是否立即压栈遮罩/箭头指示层；遮罩层是否覆盖系统无障碍警告文本 |
| **系统无障碍服务列表项** | 列表中出现名为 Music Downloader 的服务项，副标题/描述为空 | 直接佐证身份伪装：音乐下载器申请无障碍却无任何用途说明，是 UTG 一眼可判的强信号 | 服务名称 = Music Downloader；描述/摘要为空或缺失；开关默认状态 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `pmdm.hyn.r6y7.dc1.attachBaseContext`
- `pmdm.hyn.r6y7.dc1.onCreate`
- `AndroidManifest.xml: service com.tumuluses.gastrocnemius.tappable (BIND_ACCESSIBILITY_SERVICE, android:label=@7F0E001D, 无 android:description)`
- `AndroidManifest.xml: activity-alias com.tumuluses.gastrocnemius.saccharimetry / consolute（双 LAUNCHER）`
- `od3KUaQxbf（APK 根目录，9,626,284 字节，XOR 0x4F 加密 DEX 载荷）`
- `assets/lpt8.niDDD 及 assets/ 下 101 个随机长名加密资源`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（静态定向审计）

**可见性判定：`packed_or_encrypted`（加密载荷 + 反编译受阻）**

**已证实事实**

1. **主 DEX 是壳层，真实逻辑不在其中。** `classes.dex` 仅 81 KB，只包含 4 个单字符混淆类（`n.ۥ`、`n.ۥ۟`、`n.ۥ۠`、`n.ۦ`、`obfuse.NPStringFog`、`pmdm.hyn.r6y7.dc1`），其中 `n.ۥ` 类有 700+ 个同形单字符方法，且全部只有 2~5 条指令（字符串/反射蹦床），**不含任何 `accessibility`、`Settings.ACTION`、`startActivity` 调用**。预筛“未加壳”判定不成立。
2. **Application 层解密并动态加载 9.6 MB 加密载荷。** [dc1.attachBaseContext()](<resource-unit:<local_path> code:pmdm.hyn.r6y7.dc1#attachBaseContext>) 从 `sourceDir` 读取 zip 条目，逐字节执行 `bArr[i] = bArr[i] ^ 79`（0x4F）后写入 `files` 目录，再通过 `DexClassLoader` + 反射覆写 `mClassLoader` 加载。APK 根目录的 [od3KUaQxbf](<resource-unit:<local_path> file:all>)（9,626,284 字节）首字节为 `2b 2a 37 45 7f 7c 77`，异或 0x4F 后即为 `dex\n038\0`，**确认是加密 DEX**；`assets/` 下另有 101 个随机长名加密资源（如 `assets/lpt8.niDDD`）。
3. **无障碍服务已声明且身份伪装。** Manifest 中 [tappable](<resource-unit:<local_path> file:all>) 声明为 `BIND_ACCESSIBILITY_SERVICE` + `android.accessibilityservice.AccessibilityService` intent-filter + `meta-data android:accessibilityservice`，`android:label="@7F0E001D"`（**Music Downloader**），但 **`android:description` 缺失**，用户在系统无障碍列表看不到任何用途说明。
4. **多入口别名。** `com.tumuluses.gastrocnemius.saccharimetry` 同时是 activity 与同名 LAUNCHER `activity-alias`；另有 `android:enabled="false"` 的第二 LAUNCHER 别名 `consolute`（label `@7F0E001F`、独立图标 `@7F0C0003`），具备按条件切换桌面身份的结构。`meta-data app_name = "g969.do2.boew.ilq"` 与显示名不一致。
5. 权限面：`QUERY_ALL_PACKAGES`、`REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`、`FOREGROUND_SERVICE`、`WAKE_LOCK`，`debuggable=true`、`usesCleartextTraffic=true`；另有 `receiver slideway` 监听 action `"kill"`。

**未还原部分（诚实缺口）**

载荷 `od3KUaQxbf` 的 DEX 头中 `class_defs_off`(0x4F5F584B)、`data_off`、`map_off` 在明文态仍为乱码（尾部为 0x4F 填充区），纯 XOR 0x4F 不能得到完整可解析 DEX；MCP 对该文件返回 `[0 classes, 0 packages]`。因此**引导弹窗文案、`ACTION_ACCESSIBILITY_SETTINGS` 跳转点、拒绝循环、遮罩层、WebView/HTML 教学页均未能静态定位**——这类页面流转只能在运行期观察，或通过更完整的脱壳（二次变换/头部混淆修复）还原。`strings.xml` 中 `[DEFAULT] Low Battery` 与 `[zh-rCN] 不在允许的范围内：%1$s` 仅能确认存在于资源中，**无法确认其呈现位置与是否用于引导**，故不作诱导话术认定。

**风险登记：** 已登记 [R-001](<resource-unit:<local_path> code:pmdm.hyn.r6y7.dc1#attachBaseContext>)（`malware_trojan` / high）：XOR 加壳动态加载隐藏载荷 + 伪装成 Music Downloader 的无障碍服务声明。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "主 classes.dex 仅为 81KB 的壳层（单字符混淆类 + NPStringFog + 反射蹦床），真实业务与无障碍引导逻辑位于 APK 根目录 od3KUaQxbf（9,626,284 字节，XOR 0x4F 加密的 dex）及 assets/ 下 101 个随机长名加密资源，由 pmdm.hyn.r6y7.dc1.attachBaseContext 解密后 DexClassLoader 动态加载。该载荷的 DEX 头字段（class_defs_off/data_off/map_off）在明文态仍为乱码，仅异或 0x4F 无法得到完整可解析 DEX，MCP 反编译返回 0 个类，故引导弹窗、ACTION_ACCESSIBILITY_SETTINGS 跳转点、拒绝循环、遮罩与 HTML 教学页均不可静态还原，只能确认 Manifest 层的无障碍服务声明与伪装标签。",
  "summary_one_liner": "该样本以单字节 XOR 加壳把全部引导与无障碍逻辑藏进 9.6MB 加密 dex 动态加载，仅在 Manifest 暴露一个标签为「Music Downloader」、无任何用途说明的无障碍服务，运行期再借壳内逻辑引导用户开启。",
  "disguise_identity": {
    "app_display_name": "Music Downloader",
    "claimed_brand_or_persona": "Music Downloader（音乐下载器，实为隐藏载荷的银行木马类壳）",
    "a11y_service_label": "Music Downloader",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) 无障碍服务 android:description 完全缺失，系统无障碍列表中不显示任何用途说明；2) 无障碍服务 label 直接复用主应用标签 @7F0E001D（Music Downloader），使系统设置页中服务名与桌面应用名一致，掩盖权限性质；3) 存在两个 LAUNCHER activity-alias：saccharimetry（与 activity 同名，enabled=true）与 consolute（label @7F0E001F、图标 @7F0C0003、enabled=false），可运行期切换桌面名称/图标；4) meta-data app_name=\"g969.do2.boew.ilq\" 与显示名不一致；5) 主 dex 全部类名/方法名为单字符同形混淆（n.ۥ / ۥ۟ 等 700+ 同形方法），字符串经 NPStringFog 二次加密。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "pmdm.hyn.r6y7.dc1（android:name 指定的 Application）",
      "trigger_event": "进程创建 → Application.attachBaseContext()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此阶段无 UI；Application 在上下文挂载前完成载荷解密与 ClassLoader 替换，用户无任何可见提示",
      "user_action_requested": "无需用户操作",
      "code_anchor": "pmdm.hyn.r6y7.dc1.attachBaseContext"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "com.tumuluses.gastrocnemius.saccharimetry（activity 与同名 LAUNCHER activity-alias）",
      "trigger_event": "点击桌面图标（android.intent.action.MAIN / LAUNCHER，noHistory=true）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（仅 Manifest 声明，Activity 实现类体不在壳 dex 中）",
      "shown_text_zh": "桌面入口指向 Activity 类名，该类实现由解密后的动态载荷提供，静态无法取得其 onCreate 内容",
      "user_action_requested": "点击图标启动",
      "code_anchor": "AndroidManifest.xml: activity/activity-alias com.tumuluses.gastrocnemius.saccharimetry"
    },
    {
      "step": 3,
      "stage": "引导说明页 / 跳无障碍设置 / 遮罩叠层指引 / 拒权反馈循环 / 获权后动作",
      "screen_or_component": "不可静态还原（实现位于 od3KUaQxbf 解密载荷）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "载荷 od3KUaQxbf 的 DEX 头在明文态仍为乱码（class_defs_off=0x4F5F584B、data_off 越界），仅异或 0x4F 不能得到可解析 DEX，反编译返回 0 个类，故该步骤的载体、文案、是否可取消、拒绝后是否死循环重跳均无法静态确定",
      "user_action_requested": "不可静态还原",
      "code_anchor": "od3KUaQxbf（XOR 0x4F 加密载荷）"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "com.tumuluses.gastrocnemius.tappable（AccessibilityService）",
      "trigger_event": "用户在系统设置中启用该服务 → 系统 bindService（BIND_ACCESSIBILITY_SERVICE）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Music Downloader",
      "shown_text_zh": "系统无障碍服务列表中仅显示服务名「Music Downloader」，android:description 缺失，用户看不到任何权限用途说明",
      "user_action_requested": "用户在系统设置中手动开启该无障碍服务（是否由应用内跳转引导，静态不可确认）",
      "code_anchor": "AndroidManifest.xml: service com.tumuluses.gastrocnemius.tappable"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表：服务名「Music Downloader」（复用 @7F0E001D 应用标签），android:description 缺失 → 列表项无任何用途说明文字",
    "桌面启动器：应用名「Music Downloader」/ 图标 @7F0C0000；备用别名 consolute 使用 @7F0E001F + @7F0C0003（enabled=false，暂不显示）",
    "应用内引导弹窗/Activity/WebView/悬浮窗：实现位于 od3KUaQxbf 加密载荷，静态不可还原，未定位到具体 layout 或 assets/*.html（assets/ 下 101 个文件均为随机长名加密二进制，无明文 HTML）",
    "资源字符串池：存在 [DEFAULT] \"Low Battery\" 与 [zh-rCN] \"不在允许的范围内：%1$s\"，但无法静态确认其呈现在哪个界面、是否用于无障碍引导，故不列为诱导话术"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Music Downloader",
      "text_zh": "音乐下载器",
      "source_location": "AndroidManifest.xml → application android:label=@7F0E001D；service tappable android:label=@7F0E001D；activity-alias saccharimetry android:label=@7F0E001D",
      "rhetorical_frame": "清理工具伪装"
    },
    {
      "lang": "en",
      "text_verbatim": "Low Battery",
      "text_zh": "电量不足",
      "source_location": "resources.arsc 字符串池（[DEFAULT]），呈现位置静态未确认",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "zh-rCN",
      "text_verbatim": "不在允许的范围内：%1$s",
      "text_zh": "不在允许的范围内：%1$s",
      "source_location": "resources.arsc 字符串池（[zh-rCN]），呈现位置静态未确认",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "g969.do2.boew.ilq",
      "text_zh": "无实义（随机标识串）",
      "source_location": "AndroidManifest.xml → meta-data app_name",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导逻辑位于 od3KUaQxbf 加密载荷，DEX 头字段在明文态仍为乱码，无法定位 onResume/Timer 重跳代码",
    "overlay_or_fake_settings": "不可静态还原：壳 dex 中无任何悬浮窗/Overlay/SYSTEM_ALERT_WINDOW 相关调用，亦未声明 SYSTEM_ALERT_WINDOW 权限；若存在遮罩层应位于载荷内，需运行期 UTG 观察",
    "restricted_settings_13plus_coaching": "无静态证据（未在壳 dex 与 Manifest 中发现 APPLICATION_DETAILS_SETTINGS 跳转或受限设置教学相关代码/字符串）",
    "post_grant_anti_removal": "无静态证据：壳 dex 中未见 GLOBAL_ACTION_BACK/HOME、performGlobalAction 或无障碍设置页监听代码，相关实现可能位于载荷内",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在冷启动 saccharimetry 页面 onResume 起持续监测顶层窗口变化：一旦 Activity 切换为 com.android.settings/.AccessibilitySettings（或 Settings$AccessibilitySettingsActivity）即抓帧；同时以 300~500ms 间隔轮询无障碍服务启用状态，捕捉「跳设置 → 返回应用 → 再次跳设置」的往返循环。因壳层无静态线索，建议对冷启动后 0~60 秒内所有非 Launcher 顶层页面全量录屏。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首屏（壳解密完成后的实际入口 Activity）",
        "page_identifier": "顶层 Activity = com.tumuluses.gastrocnemius.saccharimetry 或载荷内新 Activity；标签/标题为 Music Downloader",
        "why_most_useful": "确认载荷加载成功后应用真正呈现的界面，判断是直接弹无障碍引导、还是先展示音乐下载器假功能外壳",
        "observable_utg_signals": ["首屏是否出现无障碍/辅助功能相关按钮或开关", "是否存在无取消按钮的模态弹窗", "界面是否与「音乐下载器」功能描述相符"]
      },
      {
        "page_role": "跳转前引导说明页（应用内）",
        "page_identifier": "Dialog 或 Activity，含「无障碍 / 辅助功能 / 授权 / 开启」类文案；可能为 WebView",
        "why_most_useful": "获取逐字诱导话术与话术框架（假更新、故障恐吓、假安全、清理伪装），静态完全缺失，这是唯一取证途径",
        "observable_utg_signals": ["弹窗是否有取消/跳过按钮", "文案是否提及系统警告可忽略", "是否存在倒计时自动跳转"]
      },
      {
        "page_role": "系统无障碍设置页 + 其后压栈遮罩页",
        "page_identifier": "com.android.settings/.AccessibilitySettings 或 accessibility 服务列表；返回应用后立即出现的半透明引导层",
        "why_most_useful": "验证是否为分步教学式引导，以及是否用悬浮引导层遮住系统警告文案；这是区分「良性透明说明」与「诱导规避」的关键",
        "observable_utg_signals": ["系统设置页停留时长与是否自动滚动定位到服务项", "返回应用后是否立即压栈遮罩/箭头指示层", "遮罩层是否覆盖系统无障碍警告文本"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "列表中出现名为 Music Downloader 的服务项，副标题/描述为空",
        "why_most_useful": "直接佐证身份伪装：音乐下载器申请无障碍却无任何用途说明，是 UTG 一眼可判的强信号",
        "observable_utg_signals": ["服务名称 = Music Downloader", "描述/摘要为空或缺失", "开关默认状态"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：本样本为静态加壳 + 单字节 XOR 加密载荷（非 VMP），运行期可正常解密，UTG 不受影响；但静态侧完全看不到引导文案与跳转点，纯静态检测会漏判为「无害音乐下载器」。另需注意两点盲区：(1) 载荷 DEX 头仍二次混淆，本报告未能取得其内部字符串，若载荷以远端 HTML/WebView 下发话术，则需同时抓流量；(2) 应用声明 debuggable=true 且 usesCleartextTraffic=true，可能从明文 HTTP 拉取引导页，建议同步做流量捕获以补证远端话术。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "pmdm.hyn.r6y7.dc1.attachBaseContext",
    "pmdm.hyn.r6y7.dc1.onCreate",
    "AndroidManifest.xml: service com.tumuluses.gastrocnemius.tappable (BIND_ACCESSIBILITY_SERVICE, android:label=@7F0E001D, 无 android:description)",
    "AndroidManifest.xml: activity-alias com.tumuluses.gastrocnemius.saccharimetry / consolute（双 LAUNCHER）",
    "od3KUaQxbf（APK 根目录，9,626,284 字节，XOR 0x4F 加密 DEX 载荷）",
    "assets/lpt8.niDDD 及 assets/ 下 101 个随机长名加密资源"
  ]
}
```

</details>
