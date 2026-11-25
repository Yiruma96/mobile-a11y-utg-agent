# MB_069__a8ecd43776｜Cerberus —                

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：127.4s

## 1. 一句话核心结论

- **核心申请方式**：空白名伪装 + 二阶段加密 DEX 加载器：静态仅暴露土耳其语诱导性无障碍服务标签『Lütfen izin Veriniz』且无 description、无包名白名单的全屏读取无障碍服务，真正的申请引导流程藏在 assets 加密载荷中运行期解密注入。
- **静态可见性说明**：一阶段 classes.dex 仅为加载器：Application.attachBaseContext 经 HNgFdCpWk.roughsubway 反射读取 assets/UBFpLdj.json 加密块、解密落地后由 PMrBlAwLpWbGsPjQlDhOjOzOmLdRyHaQxIeJkGfNsOcGh.chefuncover 反射改写 ClassLoader 注入二阶段 DEX。无障碍服务类 com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto 及其全部引导 UI/跳转逻辑均不在静态 DEX 内（strings 与 search 全部 no_matches）；APK 无 strings.xml、无 layout、无本地 HTML，故引导弹窗文案与 ACCESSIBILITY_SETTINGS 跳转点无法静态还原。
- **命中的行为模式标签**：`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_RESTRICTED_SETTINGS_COACHING`（Android 13+受限设置分步解锁教学(应用信息→右上角菜单)）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a8ecd437766e7960bf5002c553dc047f50db750818bee1a3f0ffdff1633f0d1b` |
| 包名 / 年份 | `com.safe.census` / 2024 |
| 家族 / 品类 | **Cerberus**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | — |
| 引导页宣称品牌/身份 | com.safe.census（名义为『census 人口普查』类工具，实际为 Cerberus 系银行木马） |
| 系统无障碍列表服务名 | Lütfen izin Veriniz |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：桌面 android:label 为 15 个空格；多个 Activity（fyygvslonj、dpugiw、lvawixefqmeze、hkmetfanmljay）label 为空串且 theme=NoDisplay/excludeFromRecents；类名与成员名全量随机化（RUnIiIeYsTrTmDeJoKxMkFpEbWxUd 等）；无障碍配置 iwxj.xml 刻意不写 android:description；二进制载荷伪装为 assets/UBFpLdj.json；一阶段代码内插入大量无效算术与控制流混淆 |
| 无障碍服务类名 | `com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW, WRITE_SETTINGS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.safe.census.RUnIiIeYsTrTmDeJoKxMkFpEbWxUd（Application.attachBaseContext） | 进程启动即 attachBaseContext 回调 | 不可静态还原 | 无 | 无需用户操作，静默完成二阶段 DEX 解密与 ClassLoader 注入 | `com.safe.census.RUnIiIeYsTrTmDeJoKxMkFpEbWxUd.attachBaseContext` |
| 2 | 获权后动作（服务声明侧） | com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto（AccessibilityService，配置 res/xml/iwxj.xml） | 用户在系统设置中手动启用该服务后系统绑定 | 系统无障碍页 | **原文**：Lütfen izin Veriniz<br>**译注**：请授予许可 | 在系统无障碍列表中找到并开启该服务；系统详情页无任何用途说明（无 android:description） | `AndroidManifest.xml:119-124 service ijedaqwrajkyto / res/xml/iwxj.xml` |
| 3 | 引导说明页 | 二阶段 DEX 内引导 Activity/Dialog/WebView（类名未知） | 不可静态还原（位于 assets/UBFpLdj.json 加密载荷解密后的 DEX） | 不可静态还原 | 无 | 不可静态还原 | `assets/UBFpLdj.json（加密载荷，66 KB，高熵）` |
| 4 | 跳无障碍设置 | Settings.ACTION_ACCESSIBILITY_SETTINGS 跳转（二阶段内） | 不可静态还原 | 不可静态还原 | 无 | 不可静态还原 | `不可静态还原` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表项：服务标签『Lütfen izin Veriniz』（AndroidManifest.xml service android:label）
- 系统无障碍服务详情页：android:description 缺失，res/xml/iwxj.xml 仅有 eventTypes/flags/canRetrieveWindowContent，无任何说明文字
- 桌面启动器：应用名称为 15 个空格（application android:label），无可见名称
- 应用内部引导弹窗/WebView/遮罩：不可静态还原（位于 assets/UBFpLdj.json 解密后的二阶段 DEX；APK 内无 strings.xml、无 layout、无本地 HTML）

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Lütfen izin Veriniz | 请授予许可 | `AndroidManifest.xml service com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto android:label` | 受限设置分步教学 |
| none | — | 15 个空格（无可见名称） | `AndroidManifest.xml application android:label` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原（引导与重跳逻辑位于加密二阶段 DEX，静态 DEX 内无 ACCESSIBILITY_SETTINGS 调用点）
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；但清单已申请 SYSTEM_ALERT_WINDOW，具备叠层引导/遮罩能力
- **Android 13+ 受限设置（Restricted Settings）应对**：不可静态还原（targetSdkVersion=30，未触及 Android 13 受限设置机制；二阶段逻辑不可见）
- **获权后即时行为与防撤权机制**：不可静态还原；但同包已声明 BIND_DEVICE_ADMIN 设备管理器接收器（csebcib.wasktbfdhiqkhqa，meta-data @xml/kxjblzewzbmdealq）并监听 DEVICE_ADMIN_DISABLED，具备典型反卸载/反撤权配套能力
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动后监测任何 Activity 启动即为起点（二阶段 DEX 在 attachBaseContext 注入，首个前台 Activity 即引导页）；最佳钩子为监测 Intent 目标包含 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间，以及首个非 com.google.android.gms.common.api.GoogleApiActivity 的应用 Activity 出现时立即抓取 UTG。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：主要盲区：全部引导文案、跳转逻辑与拒权循环位于 assets/UBFpLdj.json 加密载荷解密后的二阶段 DEX，静态完全不可见；桌面图标名称为 15 个空格，按名称检索会漏检；无障碍服务无 description，系统设置页无摘要文本。注：静态加壳本身不阻挡运行期 UTG，只要设备在线即可在首 Activity 出现时抓到真实引导话术。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动后首个应用 Activity（二阶段引导页/弹窗宿主）** | 包名 com.safe.census，非 GoogleApiActivity，theme 常为 Theme.Translucent.NoTitleBar 或无标题全屏；界面元素含开关/授权按钮 | 引导文案与跳转按钮全部来自加密二阶段 DEX，静态零证据，UTG 是唯一可取得逐字诱导话术的途径 | 界面文本节点（诱导话术原文）；按钮文案与可点击性（是否存在取消/跳过）；页面是否为 WebView（含 webview 节点类名） |
| **跳转前说明页 / 设置页后压栈遮罩页** | 应用窗口之上的 SYSTEM_ALERT_WINDOW 悬浮层（TYPE_APPLICATION_OVERLAY）或半透明 Activity | 判定是否存在遮罩叠层指引、高仿系统无障碍开关页等关键诱导手段 | 叠加在 Settings 之上的独立窗口；箭头/手指图标等指引图形节点；伪装为系统控件的文本（如『无障碍』『辅助功能』标题） |
| **系统无障碍服务列表项** | Settings$AccessibilitySettings，条目文本 Lütfen izin Veriniz，无 summary 描述行 | 确认服务标签诱导话术与 description 缺失导致用户无知情说明 | 列表项 title=Lütfen izin Veriniz；该条目无 description 子行；服务开关状态（判断拒权后是否被重跳） |
| **拒权返回后的反馈循环页** | 从系统设置返回后 0.5~3 秒内再次出现的应用 Activity 或悬浮层 | 识别无取消按钮的死循环重跳与拒权惩罚式反馈 | 同一引导页短时间内重复出现次数；返回键是否被拦截；是否出现倒计时/威胁性文案 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.safe.census.RUnIiIeYsTrTmDeJoKxMkFpEbWxUd.attachBaseContext`
- `com.safe.census.HNgFdCpWk.roughsubway`
- `com.safe.census.PMrBlAwLpWbGsPjQlDhOjOzOmLdRyHaQxIeJkGfNsOcGh.chefuncover`
- `AndroidManifest.xml:119-124 service com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto`
- `res/xml/iwxj.xml`
- `assets/UBFpLdj.json`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，已收敛）

**静态可见性：`packed_or_encrypted`（两阶段加载器 / 二阶段 DEX 全程加密）**

以下为核实到的事实链：

1. **一阶段仅为空壳加载器**。`AndroidManifest.xml` 声明 Application 为 [RUnIiIeYsTrTmDeJoKxMkFpEbWxUd](<resource-unit:#1.dex1 code:com.safe.census.RUnIiIeYsTrTmDeJoKxMkFpEbWxUd>)，其 `attachBaseContext()` 依次执行：`anciententire()`/`sniffdeliver()` 取 `getDir(...)` 私有目录 → `fortuneshare()` 取绝对路径 → `lectureprovide()` → [HNgFdCpWk.processrelief()](<resource-unit:#1.dex1 code:com.safe.census.HNgFdCpWk#processrelief>)。

2. **二阶段载荷来自 assets 内加密文件并解密落地后反射注入**。[HNgFdCpWk.roughsubway()](<resource-unit:#1.dex1 code:com.safe.census.HNgFdCpWk#roughsubway>) 通过 `AssetManager.class.newInstance()` + 反射调用隐藏方法从 assets 读出加密块，写出临时文件后由 `insidestart(crystaldevice(bArr2), ...)` 解密并写回；随后 [PMrBlAwLpWbGsPjQlDhOjOzOmLdRyHaQxIeJkGfNsOcGh.chefuncover()](<resource-unit:#1.dex1 code:com.safe.census.PMrBlAwLpWbGsPjQlDhOjOzOmLdRyHaQxIeJkGfNsOcGh#chefuncover>) 用 `Class.forName` + `Field.set` 反射改写 `LoadedApk` 的 `ClassLoader` 相关字段，把二阶段 DEX 挂入应用类加载器。assets 中 `UBFpLdj.json`（66 KB 高熵随机字节）即为加密载荷本体。

3. **无障碍服务类完全不在静态 DEX 中**。清单声明 [com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto](<resource-unit:#1 manifest:components>)，`permission=BIND_ACCESSIBILITY_SERVICE`、`label="Lütfen izin Veriniz"`、配置为 [res/xml/iwxj.xml](<resource-unit:#1 file:res/xml/iwxj.xml>)。但 `strings classes.dex` 仅含 `com/safe/...` 包，`search_function_definitions`/`search_function_callsites` 对 `AccessibilityService`、`ijedaqwrajkyto`、`ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`performGlobalAction` 全部 `no_matches`——说明这些组件与全部引导逻辑均位于加密二阶段。

4. **引导文案与 UI 载体不可静态还原**。APK 内 `res/values*` 不存在（无 `strings.xml`），仅 5 个 xml（`attrs/ids/public/iwxj/kxjblzewzbmdealq`），无 layout、无本地 HTML；`Lütfen izin Veriniz` 仅出现在 Manifest 属性中，DEX 内亦无对应字符串（经资源混淆与加密双隔离）。故"如何一步步引导"的弹窗/WebView/遮罩实现无法从一阶段静态还原。

5. **可确证的诱导性设计缺陷（不依赖二阶段）**：
   - 桌面名 `android:label` 为 **15 个空格**（`"               "`），全应用多个 Activity 的 `label=""`，属典型空白名隐藏（`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`）。
   - 无障碍服务标签为土耳其语 **"Lütfen izin Veriniz"（"请授予许可"）**——服务名本身即诱导性话术，非功能描述。
   - [iwxj.xml](<resource-unit:#1 file:res/xml/iwxj.xml>) **缺少 `android:description`**：系统无障碍详情页不显示任何用途说明，用户无法获知该服务将读取屏幕内容。
   - 配置 `canRetrieveWindowContent="true"`、`flagIncludeNotImportantViews|flagReportViewIds`，且**未设 `android:packageNames` 白名单**——获得授权后可读取任意应用（含银行、短信）窗口内容，与"census 人口普查"名义严重不符。
   - 同包并存 `BIND_DEVICE_ADMIN` 设备管理器接收器、`SEND_SMS/READ_SMS/RECEIVE_SMS`、`SYSTEM_ALERT_WINDOW`、`REQUEST_INSTALL_PACKAGES` 与 `<category android:name="android.app.role.SMS"/>`（伪装默认短信角色），构成典型银行木马能力面。

**覆盖边界**：第 4 点所列"引导页面流转"（弹窗文案、跳 `ACTION_ACCESSIBILITY_SETTINGS` 的触发点、遮罩叠层、拒权重跳循环）全部位于 AES/自定义加密的二阶段 DEX（`UBFpLdj.json` 解密所得）内，静态不可见；动态解密需运行设备与脱壳环境，本次未展开。以下 JSON 中相关字段按不可静态还原标注，凡未取得逐字原文者一律填"无"。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "一阶段 classes.dex 仅为加载器：Application.attachBaseContext 经 HNgFdCpWk.roughsubway 反射读取 assets/UBFpLdj.json 加密块、解密落地后由 PMrBlAwLpWbGsPjQlDhOjOzOmLdRyHaQxIeJkGfNsOcGh.chefuncover 反射改写 ClassLoader 注入二阶段 DEX。无障碍服务类 com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto 及其全部引导 UI/跳转逻辑均不在静态 DEX 内（strings 与 search 全部 no_matches）；APK 无 strings.xml、无 layout、无本地 HTML，故引导弹窗文案与 ACCESSIBILITY_SETTINGS 跳转点无法静态还原。",
  "summary_one_liner": "空白名伪装 + 二阶段加密 DEX 加载器：静态仅暴露土耳其语诱导性无障碍服务标签『Lütfen izin Veriniz』且无 description、无包名白名单的全屏读取无障碍服务，真正的申请引导流程藏在 assets 加密载荷中运行期解密注入。",
  "disguise_identity": {
    "app_display_name": "               ",
    "claimed_brand_or_persona": "com.safe.census（名义为『census 人口普查』类工具，实际为 Cerberus 系银行木马）",
    "a11y_service_label": "Lütfen izin Veriniz",
    "identity_mismatch": true,
    "obfuscation_tricks": "桌面 android:label 为 15 个空格；多个 Activity（fyygvslonj、dpugiw、lvawixefqmeze、hkmetfanmljay）label 为空串且 theme=NoDisplay/excludeFromRecents；类名与成员名全量随机化（RUnIiIeYsTrTmDeJoKxMkFpEbWxUd 等）；无障碍配置 iwxj.xml 刻意不写 android:description；二进制载荷伪装为 assets/UBFpLdj.json；一阶段代码内插入大量无效算术与控制流混淆"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.safe.census.RUnIiIeYsTrTmDeJoKxMkFpEbWxUd（Application.attachBaseContext）",
      "trigger_event": "进程启动即 attachBaseContext 回调",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无（此阶段无任何 UI，仅执行解密注入）",
      "user_action_requested": "无需用户操作，静默完成二阶段 DEX 解密与 ClassLoader 注入",
      "code_anchor": "com.safe.census.RUnIiIeYsTrTmDeJoKxMkFpEbWxUd.attachBaseContext"
    },
    {
      "step": 2,
      "stage": "获权后动作（服务声明侧）",
      "screen_or_component": "com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto（AccessibilityService，配置 res/xml/iwxj.xml）",
      "trigger_event": "用户在系统设置中手动启用该服务后系统绑定",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Lütfen izin Veriniz",
      "shown_text_zh": "请授予许可",
      "user_action_requested": "在系统无障碍列表中找到并开启该服务；系统详情页无任何用途说明（无 android:description）",
      "code_anchor": "AndroidManifest.xml:119-124 service ijedaqwrajkyto / res/xml/iwxj.xml"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "二阶段 DEX 内引导 Activity/Dialog/WebView（类名未知）",
      "trigger_event": "不可静态还原（位于 assets/UBFpLdj.json 加密载荷解密后的 DEX）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "不可静态还原；静态 DEX 无任何引导文案字符串",
      "user_action_requested": "不可静态还原",
      "code_anchor": "assets/UBFpLdj.json（加密载荷，66 KB，高熵）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "Settings.ACTION_ACCESSIBILITY_SETTINGS 跳转（二阶段内）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "静态 DEX 中 ACCESSIBILITY_SETTINGS 与 APPLICATION_DETAILS_SETTINGS 均 no_matches",
      "user_action_requested": "不可静态还原",
      "code_anchor": "不可静态还原"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表项：服务标签『Lütfen izin Veriniz』（AndroidManifest.xml service android:label）",
    "系统无障碍服务详情页：android:description 缺失，res/xml/iwxj.xml 仅有 eventTypes/flags/canRetrieveWindowContent，无任何说明文字",
    "桌面启动器：应用名称为 15 个空格（application android:label），无可见名称",
    "应用内部引导弹窗/WebView/遮罩：不可静态还原（位于 assets/UBFpLdj.json 解密后的二阶段 DEX；APK 内无 strings.xml、无 layout、无本地 HTML）"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Lütfen izin Veriniz",
      "text_zh": "请授予许可",
      "source_location": "AndroidManifest.xml service com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto android:label",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "none",
      "text_verbatim": "               ",
      "text_zh": "15 个空格（无可见名称）",
      "source_location": "AndroidManifest.xml application android:label",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原（引导与重跳逻辑位于加密二阶段 DEX，静态 DEX 内无 ACCESSIBILITY_SETTINGS 调用点）",
    "overlay_or_fake_settings": "不可静态还原；但清单已申请 SYSTEM_ALERT_WINDOW，具备叠层引导/遮罩能力",
    "restricted_settings_13plus_coaching": "不可静态还原（targetSdkVersion=30，未触及 Android 13 受限设置机制；二阶段逻辑不可见）",
    "post_grant_anti_removal": "不可静态还原；但同包已声明 BIND_DEVICE_ADMIN 设备管理器接收器（csebcib.wasktbfdhiqkhqa，meta-data @xml/kxjblzewzbmdealq）并监听 DEVICE_ADMIN_DISABLED，具备典型反卸载/反撤权配套能力",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动后监测任何 Activity 启动即为起点（二阶段 DEX 在 attachBaseContext 注入，首个前台 Activity 即引导页）；最佳钩子为监测 Intent 目标包含 ACTION_ACCESSIBILITY_SETTINGS 或 ACTION_APPLICATION_DETAILS_SETTINGS 的瞬间，以及首个非 com.google.android.gms.common.api.GoogleApiActivity 的应用 Activity 出现时立即抓取 UTG。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动后首个应用 Activity（二阶段引导页/弹窗宿主）",
        "page_identifier": "包名 com.safe.census，非 GoogleApiActivity，theme 常为 Theme.Translucent.NoTitleBar 或无标题全屏；界面元素含开关/授权按钮",
        "why_most_useful": "引导文案与跳转按钮全部来自加密二阶段 DEX，静态零证据，UTG 是唯一可取得逐字诱导话术的途径",
        "observable_utg_signals": ["界面文本节点（诱导话术原文）", "按钮文案与可点击性（是否存在取消/跳过）", "页面是否为 WebView（含 webview 节点类名）"]
      },
      {
        "page_role": "跳转前说明页 / 设置页后压栈遮罩页",
        "page_identifier": "应用窗口之上的 SYSTEM_ALERT_WINDOW 悬浮层（TYPE_APPLICATION_OVERLAY）或半透明 Activity",
        "why_most_useful": "判定是否存在遮罩叠层指引、高仿系统无障碍开关页等关键诱导手段",
        "observable_utg_signals": ["叠加在 Settings 之上的独立窗口", "箭头/手指图标等指引图形节点", "伪装为系统控件的文本（如『无障碍』『辅助功能』标题）"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings$AccessibilitySettings，条目文本 Lütfen izin Veriniz，无 summary 描述行",
        "why_most_useful": "确认服务标签诱导话术与 description 缺失导致用户无知情说明",
        "observable_utg_signals": ["列表项 title=Lütfen izin Veriniz", "该条目无 description 子行", "服务开关状态（判断拒权后是否被重跳）"]
      },
      {
        "page_role": "拒权返回后的反馈循环页",
        "page_identifier": "从系统设置返回后 0.5~3 秒内再次出现的应用 Activity 或悬浮层",
        "why_most_useful": "识别无取消按钮的死循环重跳与拒权惩罚式反馈",
        "observable_utg_signals": ["同一引导页短时间内重复出现次数", "返回键是否被拦截", "是否出现倒计时/威胁性文案"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "主要盲区：全部引导文案、跳转逻辑与拒权循环位于 assets/UBFpLdj.json 加密载荷解密后的二阶段 DEX，静态完全不可见；桌面图标名称为 15 个空格，按名称检索会漏检；无障碍服务无 description，系统设置页无摘要文本。注：静态加壳本身不阻挡运行期 UTG，只要设备在线即可在首 Activity 出现时抓到真实引导话术。"
  },
  "behavior_pattern_tags": [
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_RESTRICTED_SETTINGS_COACHING",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "TRIG_COLD_START_BLOCK",
    "CARRIER_OVERLAY_MASK_OR_GUIDE"
  ],
  "code_anchors": [
    "com.safe.census.RUnIiIeYsTrTmDeJoKxMkFpEbWxUd.attachBaseContext",
    "com.safe.census.HNgFdCpWk.roughsubway",
    "com.safe.census.PMrBlAwLpWbGsPjQlDhOjOzOmLdRyHaQxIeJkGfNsOcGh.chefuncover",
    "AndroidManifest.xml:119-124 service com.vgvvqankgtozrwm.hjhpxppobbyze.ozjexsg.ijedaqwrajkyto",
    "res/xml/iwxj.xml",
    "assets/UBFpLdj.json"
  ]
}
```

</details>
