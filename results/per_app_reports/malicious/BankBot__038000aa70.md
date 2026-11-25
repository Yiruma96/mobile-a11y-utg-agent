# MB_112__038000aa70｜BankBot — Sistem Güncelleştirmesi

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：101.0s

## 1. 一句话核心结论

- **核心申请方式**：以“Sistem Güncelleştirmesi（系统更新）”同时伪装应用名与无障碍服务名，真正把用户骗进无障碍设置的代码藏在加密 repack 载荷中，静态仅见同名伪装与零说明文字的 BIND_ACCESSIBILITY_SERVICE 声明。
- **静态可见性说明**：Manifest 声明的所有类在 classes.dex 中均不存在，DEX 为 com.gtdksnlp.lmensid.* 的字节码级混淆误导层（死分支+空格插字乱序字符串），无 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS / DexClassLoader / getAssets / Cipher 任何引用；真实逻辑与引导文案位于 unknown/repack/ 下 48 个无文件头魔数的加密 blob（19B~254KB）及 graphics.rpk/strings.rpk 索引，运行期解密后加载，静态无法还原页面流转与逐字文案。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`TRIG_BACKGROUND_OR_NOTIF_RELAUNCH`（后台服务/定时器/通知栏反复拉起授权页）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `038000aa704b98f988e032d47a151524d4bbf47a63a0129d3f984711d5497e0e` |
| 包名 / 年份 | `com.jiuloisetp.muvhbmbajhun` / 2024 |
| 家族 / 品类 | **BankBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Sistem Güncelleştirmesi |
| 引导页宣称品牌/身份 | Android 系统更新（伪造的“系统更新”组件） |
| 系统无障碍列表服务名 | Sistem Güncelleştirmesi |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：应用 label 与无障碍服务 label 完全同名“系统更新”，制造系统组件错觉；无障碍服务未配置 android:description（系统列表项无任何用途说明）；settingsActivity 指向本应用不存在的模板类 com.example.root.myapplication.MainActivity 以伪造配置完整；十余个 kmomlakuour.* 马甲 Activity 使用 label="" + 自定义图标 afsxrting + excludeFromRecents + singleTask 隐藏于最近任务；其余 Activity 全部随机串 label 掩盖用途；DEX 层采用类名/方法名字节码级混淆与乱序空格插字字符串 |
| 无障碍服务类名 | `com.jiuloisetp.muvhbmbajhun.LaEInNhOgzA` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.jiuloisetp.muvhbmbajhun.kmomlakuour.hPdKACvDL（MAIN/LAUNCHER） | 用户点击桌面“Sistem Güncelleştirmesi”图标启动 | 不可静态还原 | 无 | 点击桌面图标 | `AndroidManifest.xml: activity com.jiuloisetp.muvhbmbajhun.kmomlakuour.hPdKACvDL (MAIN/LAUNCHER)` |
| 2 | 引导说明页 | Application 入口 com.gtdksnlp.lmensid.fTSeSCeN（Manifest android:name） | Application.onCreate 执行，调用 NyMcNYDR.EPzxEa(Application) 与 NyMcNYDR.VzIsqYICcyG() | 不可静态还原 | **原文**：无（仅见填充字符串如 "epetsn csiuhiftg  asrbpamaoc nephosbwo hos beinisoriruntsng aeltim nak"）<br>**译注**：仅见无意义填充串，无真实引导文案 | 无（不可静态确认） | `com.gtdksnlp.lmensid.fTSeSCeN.onCreate` |
| 3 | 跳无障碍设置 | 系统设置 → 无障碍 → 已下载服务列表项“Sistem Güncelleştirmesi”（服务 com.jiuloisetp.muvhbmbajhun.LaEInNhOgzA） | 运行期由加密 repack 载荷解密后发起跳转（静态未见 Intent 构造点） | 系统无障碍页 | **原文**：Sistem Güncelleştirmesi<br>**译注**：系统更新 | 用户需在系统无障碍列表中手动开启该“系统更新”服务；服务无 android:description，用户看不到任何权限用途说明 | `AndroidManifest.xml: service LaEInNhOgzA + res/xml/gyuxrhtyavno.xml` |
| 4 | 获权后动作 | 无障碍服务 LaEInNhOgzA（typeWindowContentChanged\|typeWindowStateChanged, canRetrieveWindowContent=true, flagReportViewIds） | 服务被系统绑定后接收窗口事件 | 不可静态还原 | 无 | 无 | `res/xml/gyuxrhtyavno.xml` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- AndroidManifest.xml 中 application/android:label="Sistem Güncelleştirmesi"：桌面图标下方显示名
- AndroidManifest.xml 中 service com.jiuloisetp.muvhbmbajhun.LaEInNhOgzA 的 android:label="Sistem Güncelleştirmesi"：系统设置→无障碍→已下载服务列表项名称
- res/xml/gyuxrhtyavno.xml：无障碍服务配置，未提供 android:description，故系统列表项无任何用途/隐私说明文字
- 运行期引导弹窗/WebView/悬浮窗文案：不在可读 DEX 与 res 中，位于 unknown/repack/ 加密载荷（AES/自定义加密），静态不可提取
- unknown/repack/* 小文件（19~44B）为纯 ASCII 随机串占位（如 "zfuheoka"、"wosxqzgw"、"repack/graphics.rpk"），非可读文案

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Sistem Güncelleştirmesi | 系统更新 | `AndroidManifest.xml: application@android:label 与 service LaEInNhOgzA@android:label` | 假更新 |
| en | com.example.root.myapplication.MainActivity | 示例模板主界面（本应用并不存在的类） | `res/xml/gyuxrhtyavno.xml android:settingsActivity` | 未知 |
| en | repack/graphics.rpk | 重打包图形资源索引路径（指向加密载荷 graphics.rpk） | `unknown/repack/strings.rpk` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导与拒权重跳逻辑位于 unknown/repack 加密载荷；Manifest 层可见 BOOT_COMPLETED / USER_PRESENT / SCREEN_ON / CONNECTIVITY_CHANGE（receiver ixqsuxinj.BEAfZdraNzrV，priority=999）具备后台反复拉起条件
- **遮罩叠层 / 高仿系统设置页**：Manifest 已声明 SYSTEM_ALERT_WINDOW 悬浮窗权限，配合多个 label="" 的 kmomlakuour.* 透明/单实例 Activity（部分 theme=Theme.NoDisplay / Translucent.NoTitleBar），具备叠层遮罩与高仿页载体，但具体叠加行为在加密载荷中，静态不可确认
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=27，无 Android 13 受限设置分步教学代码可静态确认）
- **获权后即时行为与防撤权机制**：不可静态还原：未见 GLOBAL_ACTION_BACK/HOME 静态引用（该引用亦可能由加密载荷动态反射调用）
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在监测到 Launcher 启动 com.jiuloisetp.muvhbmbajhun.kmomlakuour.hPdKACvDL 后 1~3 秒内即拉起 UTG 抓取当前 Activity；同时 Hook/轮询前台包名切换至 com.android.settings（无障碍或应用详情）时立即抓取压栈页面与悬浮窗层
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：DEX 为不可读误导层，真实引导逻辑与全部文案位于 unknown/repack 的加密二进制载荷，纯静态无法给出引导页流转与逐字原文；另 Manifest 中 label="" 的透明/NoDisplay Activity 与 SYSTEM_ALERT_WINDOW 组合可能以纯图或无文本遮罩呈现，UTG 需配合截图 OCR。静态加密不阻碍运行期 UTG 捕获。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后的首个应用页（伪“系统更新”界面）** | package=com.jiuloisetp.muvhbmbajhun，activity 名形如 kmomlakuour.*，label 为空或随机串 | 判定诱导是否零步直达（cold_start_0_step），并取得真实引导文案与是否有取消按钮 | 页面标题/正文是否出现“Sistem Güncelleştirmesi / Güncelle / Ayarlar / Erişilebilirlik”等字样；是否存在“取消/跳过/Kapat”控件，或仅单一“Tamam/Devam”按钮；是否出现 WebView 容器（含 URL 地址栏） |
| **跳转前的引导说明页/弹窗** | Activity 或 Dialog，文案含无障碍/设置相关词，可能伴随半透明遮罩 | 区分是原生 Dialog、本地 HTML 还是远端 WebView 教学，以及话术框架（假更新/故障恐吓/教唆忽略警告） | 窗口层级是否含悬浮窗（SYSTEM_ALERT_WINDOW）类型节点；文本是否指导用户“找到 系统更新 / 开启服务”；是否含 Gif/图片引导（无文本节点则需 OCR） |
| **系统无障碍服务列表项** | com.android.settings .accessibility/.AccessibilitySettings，条目文本为“Sistem Güncelleştirmesi”且无 summary 描述 | 确认服务在系统列表中确实以“系统更新”名义出现且零用途说明，是身份欺骗的直接证据 | 条目名称文本 = Sistem Güncelleştirmesi；条目 description/summary 为空；切换开关时是否出现应用自绘的遮挡层覆盖系统警告弹窗 |
| **返回/拒绝后的反应页** | 按返回键或关闭开关后的前台页面变化序列 | 判定是否存在拒权循环重跳（COERCE_REFUSAL_LOOP_RELAUNCH）或良性降级 | 是否在 1~3 秒内再次跳回 ACCESSIBILITY_SETTINGS；是否弹出更强恐吓文案（故障/病毒/不更新将停机）；是否出现自绘“开启”假开关页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `AndroidManifest.xml: application@android:label="Sistem Güncelleştirmesi" / service com.jiuloisetp.muvhbmbajhun.LaEInNhOgzA@android:label="Sistem Güncelleştirmesi"`
- `res/xml/gyuxrhtyavno.xml: accessibility-service(canRetrieveWindowContent=true, 无 android:description, settingsActivity=com.example.root.myapplication.MainActivity)`
- `com.gtdksnlp.lmensid.fTSeSCeN.onCreate（占位式加固层，调用 NyMcNYDR.EPzxEa/VzIsqYICcyG，无真实引导逻辑）`
- `unknown/repack/strings.rpk → repack/graphics.rpk（加密二阶段载荷索引）`
- `com.jiuloisetp.muvhbmbajhun.kmomlakuour.hPdKACvDL（MAIN/LAUNCHER 马甲入口，类体不在 DEX 中）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 结论要点（围绕“如何一步步引导开启无障碍权限”）

**静态可见性受限：真正实现跳转引导的代码不在 DEX 中。**

已核实的事实链：

1. **DEX 层只是占位、不可用的代码**：Manifest 声明的全部类（如 `com.jiuloisetp.muvhbmbajhun.LaEInNhOgzA`）在 [classes.dex](<resource-unit:#1.dex1 code:com.gtdksnlp.lmensid.fTSeSCeN#onCreate>) 中**均不存在**；DEX 实际包含 416 个 `com.gtdksnlp.lmensid.*` 类，类名、方法名全为 `EPzxEa`/`UanzMw` 式混淆，字符串为 “epetsn csiuhiftg  asrbpamaoc…” 这类被插入空格的乱序碎片，`onCreate` 中大量 `if (true != this.LZxciwKEI) {}`、`switch(156458)` 死分支——这是典型的字节码级加固/误导层，不含真实业务逻辑。
2. **真实载荷是加密二进制**：`unknown/repack/` 下 48 个无任何文件头魔数（非 ZIP/ELF/DEX/zlib/gzip）的 blob（19B～254KB），配 `strings.rpk`（内容仅一行 `repack/graphics.rpk`）与 `graphics.rpk` 索引结构，ASCII/UTF-16 关键字扫描**零命中**（无 `accessib`/`Ayarlar`/`Güncelle`/`com.android.settings`）→ 内容为密文，需运行期解密。
3. **DEX 内没有任何无障碍跳转锚点**：`ACCESSIBILITY_SETTINGS`、`ACTION_APPLICATION_DETAILS_SETTINGS`、`DexClassLoader`、`getAssets`、`Cipher`、`isAccessibilityTool`、`GLOBAL_ACTION_BACK` 全部 `no_matches`，故“纯运行期 UTG 页面流转”无法从静态代码还原。

**仍可静态确认的伪装与诱导结构（Manifest/资源级）：**

| 维度 | 证据 |
|---|---|
| 桌面名 | `android:label="Sistem Güncelleştirmesi"`（土耳其语“系统更新”） |
| 无障碍服务名 | [LaEInNhOgzA](<resource-unit:#1 manifest:components>) 的 `android:label` 同为 **Sistem Güncelleştirmesi**，即系统无障碍列表里显示为“系统更新” |
| 无障碍配置 | [res/xml/gyuxrhtyavno.xml](<resource-unit:#1 file:res/xml/gyuxrhtyavno.xml#L2>)：`canRetrieveWindowContent="true"`、`typeWindowContentChanged|typeWindowStateChanged`、`flagReportViewIds`；**无 `android:description`**（列表页零说明文字）；`android:settingsActivity="com.example.root.myapplication.MainActivity"` 指向**本应用不存在的模板类**（伪造/残留） |
| 隐式业务页 | 十余个 `kmomlakuour.*` Activity 均 `label=""`、`icon=@drawable/afsxrting`、`excludeFromRecents="true"`、`singleTask`（银行/推送类马甲页） |
| 其余 Activity | 全部随机串 label（`linzsgljpf`、`ocprcepow`…）用于掩盖真实用途 |

**判定：** 该样本属于“系统更新”品牌伪装 + 无障碍服务同名伪装 + 加密二阶段载荷的银行木马，诱导流程（跳设置页、遮罩指引、拒权重跳）完全位于 `unknown/repack` 密文中，静态不可见；UTG 动态检测应针对运行期而非依赖静态字符串。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "Manifest 声明的所有类在 classes.dex 中均不存在，DEX 为 com.gtdksnlp.lmensid.* 的字节码级混淆误导层（死分支+空格插字乱序字符串），无 ACCESSIBILITY_SETTINGS / APPLICATION_DETAILS / DexClassLoader / getAssets / Cipher 任何引用；真实逻辑与引导文案位于 unknown/repack/ 下 48 个无文件头魔数的加密 blob（19B~254KB）及 graphics.rpk/strings.rpk 索引，运行期解密后加载，静态无法还原页面流转与逐字文案。",
  "summary_one_liner": "以“Sistem Güncelleştirmesi（系统更新）”同时伪装应用名与无障碍服务名，真正把用户骗进无障碍设置的代码藏在加密 repack 载荷中，静态仅见同名伪装与零说明文字的 BIND_ACCESSIBILITY_SERVICE 声明。",
  "disguise_identity": {
    "app_display_name": "Sistem Güncelleştirmesi",
    "claimed_brand_or_persona": "Android 系统更新（伪造的“系统更新”组件）",
    "a11y_service_label": "Sistem Güncelleştirmesi",
    "identity_mismatch": true,
    "obfuscation_tricks": "应用 label 与无障碍服务 label 完全同名“系统更新”，制造系统组件错觉；无障碍服务未配置 android:description（系统列表项无任何用途说明）；settingsActivity 指向本应用不存在的模板类 com.example.root.myapplication.MainActivity 以伪造配置完整；十余个 kmomlakuour.* 马甲 Activity 使用 label=\"\" + 自定义图标 afsxrting + excludeFromRecents + singleTask 隐藏于最近任务；其余 Activity 全部随机串 label 掩盖用途；DEX 层采用类名/方法名字节码级混淆与乱序空格插字字符串"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.jiuloisetp.muvhbmbajhun.kmomlakuour.hPdKACvDL（MAIN/LAUNCHER）",
      "trigger_event": "用户点击桌面“Sistem Güncelleştirmesi”图标启动",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "启动器入口存在，但该类在 DEX 中不存在，界面内容不可静态还原",
      "user_action_requested": "点击桌面图标",
      "code_anchor": "AndroidManifest.xml: activity com.jiuloisetp.muvhbmbajhun.kmomlakuour.hPdKACvDL (MAIN/LAUNCHER)"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "Application 入口 com.gtdksnlp.lmensid.fTSeSCeN（Manifest android:name）",
      "trigger_event": "Application.onCreate 执行，调用 NyMcNYDR.EPzxEa(Application) 与 NyMcNYDR.VzIsqYICcyG()",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无（仅见填充字符串如 \"epetsn csiuhiftg  asrbpamaoc nephosbwo hos beinisoriruntsng aeltim nak\"）",
      "shown_text_zh": "仅见无意义填充串，无真实引导文案",
      "user_action_requested": "无（不可静态确认）",
      "code_anchor": "com.gtdksnlp.lmensid.fTSeSCeN.onCreate"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 → 无障碍 → 已下载服务列表项“Sistem Güncelleştirmesi”（服务 com.jiuloisetp.muvhbmbajhun.LaEInNhOgzA）",
      "trigger_event": "运行期由加密 repack 载荷解密后发起跳转（静态未见 Intent 构造点）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Sistem Güncelleştirmesi",
      "shown_text_zh": "系统更新",
      "user_action_requested": "用户需在系统无障碍列表中手动开启该“系统更新”服务；服务无 android:description，用户看不到任何权限用途说明",
      "code_anchor": "AndroidManifest.xml: service LaEInNhOgzA + res/xml/gyuxrhtyavno.xml"
    },
    {
      "step": 4,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 LaEInNhOgzA（typeWindowContentChanged|typeWindowStateChanged, canRetrieveWindowContent=true, flagReportViewIds）",
      "trigger_event": "服务被系统绑定后接收窗口事件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后即可读取全部窗口内容与控件 ID（具备银行界面注入/凭证窃取能力），具体注入页面在加密载荷中",
      "user_action_requested": "无",
      "code_anchor": "res/xml/gyuxrhtyavno.xml"
    }
  ],
  "text_presentation_locations": [
    "AndroidManifest.xml 中 application/android:label=\"Sistem Güncelleştirmesi\"：桌面图标下方显示名",
    "AndroidManifest.xml 中 service com.jiuloisetp.muvhbmbajhun.LaEInNhOgzA 的 android:label=\"Sistem Güncelleştirmesi\"：系统设置→无障碍→已下载服务列表项名称",
    "res/xml/gyuxrhtyavno.xml：无障碍服务配置，未提供 android:description，故系统列表项无任何用途/隐私说明文字",
    "运行期引导弹窗/WebView/悬浮窗文案：不在可读 DEX 与 res 中，位于 unknown/repack/ 加密载荷（AES/自定义加密），静态不可提取",
    "unknown/repack/* 小文件（19~44B）为纯 ASCII 随机串占位（如 \"zfuheoka\"、\"wosxqzgw\"、\"repack/graphics.rpk\"），非可读文案"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Sistem Güncelleştirmesi",
      "text_zh": "系统更新",
      "source_location": "AndroidManifest.xml: application@android:label 与 service LaEInNhOgzA@android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "com.example.root.myapplication.MainActivity",
      "text_zh": "示例模板主界面（本应用并不存在的类）",
      "source_location": "res/xml/gyuxrhtyavno.xml android:settingsActivity",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "repack/graphics.rpk",
      "text_zh": "重打包图形资源索引路径（指向加密载荷 graphics.rpk）",
      "source_location": "unknown/repack/strings.rpk",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导与拒权重跳逻辑位于 unknown/repack 加密载荷；Manifest 层可见 BOOT_COMPLETED / USER_PRESENT / SCREEN_ON / CONNECTIVITY_CHANGE（receiver ixqsuxinj.BEAfZdraNzrV，priority=999）具备后台反复拉起条件",
    "overlay_or_fake_settings": "Manifest 已声明 SYSTEM_ALERT_WINDOW 悬浮窗权限，配合多个 label=\"\" 的 kmomlakuour.* 透明/单实例 Activity（部分 theme=Theme.NoDisplay / Translucent.NoTitleBar），具备叠层遮罩与高仿页载体，但具体叠加行为在加密载荷中，静态不可确认",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=27，无 Android 13 受限设置分步教学代码可静态确认）",
    "post_grant_anti_removal": "不可静态还原：未见 GLOBAL_ACTION_BACK/HOME 静态引用（该引用亦可能由加密载荷动态反射调用）",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在监测到 Launcher 启动 com.jiuloisetp.muvhbmbajhun.kmomlakuour.hPdKACvDL 后 1~3 秒内即拉起 UTG 抓取当前 Activity；同时 Hook/轮询前台包名切换至 com.android.settings（无障碍或应用详情）时立即抓取压栈页面与悬浮窗层",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后的首个应用页（伪“系统更新”界面）",
        "page_identifier": "package=com.jiuloisetp.muvhbmbajhun，activity 名形如 kmomlakuour.*，label 为空或随机串",
        "why_most_useful": "判定诱导是否零步直达（cold_start_0_step），并取得真实引导文案与是否有取消按钮",
        "observable_utg_signals": [
          "页面标题/正文是否出现“Sistem Güncelleştirmesi / Güncelle / Ayarlar / Erişilebilirlik”等字样",
          "是否存在“取消/跳过/Kapat”控件，或仅单一“Tamam/Devam”按钮",
          "是否出现 WebView 容器（含 URL 地址栏）"
        ]
      },
      {
        "page_role": "跳转前的引导说明页/弹窗",
        "page_identifier": "Activity 或 Dialog，文案含无障碍/设置相关词，可能伴随半透明遮罩",
        "why_most_useful": "区分是原生 Dialog、本地 HTML 还是远端 WebView 教学，以及话术框架（假更新/故障恐吓/教唆忽略警告）",
        "observable_utg_signals": [
          "窗口层级是否含悬浮窗（SYSTEM_ALERT_WINDOW）类型节点",
          "文本是否指导用户“找到 系统更新 / 开启服务”",
          "是否含 Gif/图片引导（无文本节点则需 OCR）"
        ]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings .accessibility/.AccessibilitySettings，条目文本为“Sistem Güncelleştirmesi”且无 summary 描述",
        "why_most_useful": "确认服务在系统列表中确实以“系统更新”名义出现且零用途说明，是身份欺骗的直接证据",
        "observable_utg_signals": [
          "条目名称文本 = Sistem Güncelleştirmesi",
          "条目 description/summary 为空",
          "切换开关时是否出现应用自绘的遮挡层覆盖系统警告弹窗"
        ]
      },
      {
        "page_role": "返回/拒绝后的反应页",
        "page_identifier": "按返回键或关闭开关后的前台页面变化序列",
        "why_most_useful": "判定是否存在拒权循环重跳（COERCE_REFUSAL_LOOP_RELAUNCH）或良性降级",
        "observable_utg_signals": [
          "是否在 1~3 秒内再次跳回 ACCESSIBILITY_SETTINGS",
          "是否弹出更强恐吓文案（故障/病毒/不更新将停机）",
          "是否出现自绘“开启”假开关页"
        ]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "存在显著盲区：DEX 为不可读误导层，真实引导逻辑与全部文案位于 unknown/repack 的加密二进制载荷，纯静态无法给出引导页流转与逐字原文；另 Manifest 中 label=\"\" 的透明/NoDisplay Activity 与 SYSTEM_ALERT_WINDOW 组合可能以纯图或无文本遮罩呈现，UTG 需配合截图 OCR。静态加密不阻碍运行期 UTG 捕获。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "TRIG_BACKGROUND_OR_NOTIF_RELAUNCH",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "AndroidManifest.xml: application@android:label=\"Sistem Güncelleştirmesi\" / service com.jiuloisetp.muvhbmbajhun.LaEInNhOgzA@android:label=\"Sistem Güncelleştirmesi\"",
    "res/xml/gyuxrhtyavno.xml: accessibility-service(canRetrieveWindowContent=true, 无 android:description, settingsActivity=com.example.root.myapplication.MainActivity)",
    "com.gtdksnlp.lmensid.fTSeSCeN.onCreate（占位式加固层，调用 NyMcNYDR.EPzxEa/VzIsqYICcyG，无真实引导逻辑）",
    "unknown/repack/strings.rpk → repack/graphics.rpk（加密二阶段载荷索引）",
    "com.jiuloisetp.muvhbmbajhun.kmomlakuour.hPdKACvDL（MAIN/LAUNCHER 马甲入口，类体不在 DEX 中）"
  ]
}
```

> 说明：受本轮 14 次工具调用硬约束，未再展开 `res/values/strings.xml`、`res/layout/*`（15 个）与 repack 载荷解密尝试，亦未登记风险台账；上述缺口不改变“引导逻辑藏于加密载荷、静态不可见”的结论。若需闭环，下一步应优先对 `unknown/repack/graphics.rpk` 做密钥定位与解密，再还原引导页文案。

</details>
