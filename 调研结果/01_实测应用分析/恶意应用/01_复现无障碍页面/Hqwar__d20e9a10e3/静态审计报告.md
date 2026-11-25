# MR_076__d20e9a10e3｜Hqwar — Servis Güncellemesi

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalRadar_2014_2021`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：174.0s

## 1. 一句话核心结论

- **核心申请方式**：以与桌面同名的土耳其语『Servis Güncellemesi』注册无任何 description 的窗口内容读取无障碍服务，真实引导逻辑藏于仿冒 android.support 命名空间的混淆类并经反射装配，配合短信拦截、悬浮窗与用量统计权限形成木马能力面。
- **静态可见性说明**：Manifest、无障碍服务声明与 res/xml/elpkjxdgjac.xml 完全静态可见；但引导页面实现被隐藏：启动 Activity 类 ughndgrsdb.ButGLtznTLN 在 DEX 中不存在，真实实现位于仿冒 android.support.hcnrjn 命名空间的 351 个混淆类，由 Application Ewslytsy.onCreate 经 UiBQKt 反射装配；跳转用 action 字符串无明文（strings 未命中 ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS），无 assets/ 与本地 HTML，提示文案不在 res 资源中（无 strings.xml）；unknown/image/mediumcrop（233KB，非图片魔数）由 firstlist.txt 索引，疑为加密二阶段载荷。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_OVERLAY_STACK_ON_SETTINGS`（跳入系统设置页后短时压栈透明指引/遮罩窗）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `d20e9a10e37a310904d70a1b68cafc1985767d9ec026142e7e5f33ade56dcc03` |
| 包名 / 年份 | `com.wdgrlnjoufx.qdlijknlopte` / 2019 |
| 家族 / 品类 | **Hqwar**（同池样本数：4） |
| 原始来源标识 | https://blog.zimperium.com/how-zimperiums-z9-detected-unknown-mobile-malware-overlooked-by-the-av-industry/ |
| 桌面显示名 | Servis Güncellemesi |
| 引导页宣称品牌/身份 | 伪装为土耳其语『系统服务更新』（Servis Güncellemesi），无真实品牌归属 |
| 系统无障碍列表服务名 | Servis Güncellemesi |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍服务 label 与桌面 label 完全同名同图标，用户在系统无障碍列表无法区分；无障碍配置无 android:description/ android:summary，隐藏能力说明；settingsActivity 残留外部示例模板类 com.example.root.myapplication.MainActivity；无障碍配置的 accessibilityFlags 显式开启 flagReportViewIds + canRetrieveWindowContent；十余个 label 为空、Theme.NoDisplay/Translucent、excludeFromRecents、singleTask 的隐形 Activity 群用于承载遮罩与钓鱼页；真实实现藏在仿冒 android.support.hcnrjn 命名空间的混淆类中并经反射装配；无 assets/、无 strings.xml，文案与 action 字符串不在静态资源内 |
| 无障碍服务类名 | `com.wdgrlnjoufx.qdlijknlopte.gVQCLYjZ` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, PACKAGE_USAGE_STATS, READ_CONTACTS, READ_SMS, RECEIVE_SMS, RECORD_AUDIO, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.ButGLtznTLN（MAIN/LAUNCHER，theme=@android:style/Theme.Translucent.NoTitleBar） | 用户点击桌面图标，Activity onCreate | 不可静态还原 | 无 | 不可静态判定 | `AndroidManifest.xml activity com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.ButGLtznTLN` |
| 2 | 引导说明页 | com.srscyf.tdrlieo.Ewslytsy（Application）+ com.srscyf.tdrlieo.UiBQKt（反射装载器） | Application.onCreate 反射取类并实例化 | 不可静态还原 | 无 | 不可静态判定 | `com.srscyf.tdrlieo.Ewslytsy.onCreate / com.srscyf.tdrlieo.UiBQKt.qUclZlPQ` |
| 3 | 跳无障碍设置 | com.wdgrlnjoufx.qdlijknlopte.gVQCLYjZ（BIND_ACCESSIBILITY_SERVICE）+ @xml/elpkjxdgjac 指向的 settingsActivity com.example.root.myapplication.MainActivity | 疑似由混淆类拼接 Settings.ACTION_ACCESSIBILITY_SETTINGS 拉起（明文常量未静态命中） | 系统无障碍页 | **原文**：无（android:description 缺失，系统页仅显示 label）<br>**译注**：系统无障碍设置列表中出现『Servis Güncellemesi』一项，无任何功能说明文字 | 用户需在系统无障碍列表中手动找到并打开该服务开关 | `res/xml/elpkjxdgjac.xml; AndroidManifest.xml service com.wdgrlnjoufx.qdlijknlopte.gVQCLYjZ` |
| 4 | 遮罩叠层指引 | com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.* 隐形 Activity 群（XmWSEBY/CtxZwVg/GSXocBY/cvPravViblhI/kSNKtOkRtf/shtStdaFBR/XDzkxvk/aznFdR 等） | 静态不可还原（受 SYSTEM_ALERT_WINDOW 与 singleTask+excludeFromRecents 配置支持） | 悬浮窗Overlay | 无 | 不可静态判定（疑为点击开关位置的引导） | `AndroidManifest.xml activities com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.*` |
| 5 | 获权后动作 | gVQCLYjZ 无障碍服务（canRetrieveWindowContent=true, flagReportViewIds）+ rojchd.uWwKarFK（SMS_DELIVER）/ rojchd.VEaEjVUFDYJ（WAP_PUSH_DELIVER） | 服务 onServiceConnected 后接收 typeWindowContentChanged / SMS_DELIVER 广播 | 不可静态还原 | 无 | 无需用户操作 | `res/xml/elpkjxdgjac.xml; AndroidManifest.xml receiver com.wdgrlnjoufx.qdlijknlopte.rojchd.uWwKarFK` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- res/xml/elpkjxdgjac.xml 未提供 android:description 与 android:summary，系统无障碍设置列表中该条目无任何说明文字，仅显示服务名『Servis Güncellemesi』
- AndroidManifest.xml 中无障碍服务 android:label 与 application android:label 同为『Servis Güncellemesi』，桌面图标与无障碍列表条目同名同图标
- 应用无 assets/ 目录、无本地 HTML 文件，引导文案不通过 WebView 本地页面呈现
- res/values 下仅有 attrs.xml / ids.xml / public.xml，无 strings.xml，所有提示文案未在资源表中定义
- 十余个 android:label="" 的 ughndgrsdb.* Activity 为空白标题的承载容器，配合 SYSTEM_ALERT_WINDOW 与 Translucent/NoDisplay 主题具备在系统设置页之上叠放引导层的能力
- res/layout/ 下十余个 189–272 字节的极简布局（ayftqrnhad.xml、bifxwsat.xml、zilntq.xml 等）为单控件容器，无可见说明性文本
- unknown/image/mediumcrop（233KB）由 unknown/image/firstlist.txt（内容 image/mediumcrop）索引，为疑加密载荷而非文本载体

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Servis Güncellemesi | 服务更新 | `AndroidManifest.xml application android:label 与 service com.wdgrlnjoufx.qdlijknlopte.gVQCLYjZ android:label` | 假更新 |
| en | com.example.root.myapplication.MainActivity | 示例工程残留的设置页类名（非本应用业务类） | `res/xml/elpkjxdgjac.xml android:settingsActivity` | 未知 |
| en | image/mediumcrop | 载荷索引清单，指向 unknown/image/mediumcrop | `unknown/image/firstlist.txt` | 未知 |
| en | serudp reuyoitrms / teteaitomch / oseopsawmesf rsi | 无意义填充字符串（用于干扰静态分析） | `com.srscyf.tdrlieo.Ewslytsy.onCreate 硬编码` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`static_hidden`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原：引导与重试逻辑位于反射装配的混淆类 android.support.hcnrjn.* 中，明文 action 常量未命中，无法确认是否在 onResume 检测未授权后循环重跳
- **遮罩叠层 / 高仿系统设置页**：具备强配置条件但未静态证实：Manifest 声明 SYSTEM_ALERT_WINDOW，且存在 8 个以上 label 为空、Theme.NoDisplay/Theme.Translucent.NoTitleBar、excludeFromRecents、launchMode=singleTask 的隐形 Activity，可在系统无障碍页之上叠放引导遮罩或高仿开关页；具体叠层代码未静态还原
- **Android 13+ 受限设置（Restricted Settings）应对**：无静态证据（targetSdkVersion=27，未达 Android 13 受限设置门槛；DEX 未命中 APPLICATION_DETAILS_SETTINGS 明文）
- **获权后即时行为与防撤权机制**：无静态证据：未发现 GLOBAL_ACTION_BACK/HOME 相关明文常量，也无 ACCESSIBILITY_SETTINGS 监听明文，实际是否自点确认或阻止撤权无法静态确认
- **良性降级 / 替代方案**：无（未发现任何降级、手动模式或替代路径；反而声明 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 与 RECEIVE_BOOT_COMPLETED 强化常驻）

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在系统无障碍设置页（Settings$Secure 或 com.android.settings 的 AccessibilitySettings 界面）出现『Servis Güncellemesi』条目时立即拉起 UTG，同时并行监测应用自身是否在设置页之上压入新 Activity/悬浮窗；冷启动后若 3 秒内未出现设置页，则改为监测 SYSTEM_ALERT_WINDOW 窗口添加事件
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：显著盲区：1) 启动 Activity ButGLtznTLN 类在 DEX 中不存在，引导逻辑经 Application 反射装配，静态无法确认引导页面文案与时序；2) 跳转 action 字符串非明文，无法确认是否使用 ACTION_ACCESSIBILITY_SETTINGS 还是直接 ComponentName 跳转；3) unknown/image/mediumcrop（233KB，非图片魔数）疑为加密二阶段载荷，可能承载远端下发的引导页/钓鱼页模板；4) 若引导完全依赖运行期解密或远端 HTML，UTG 需在设置页出现瞬间与首次冷启动后各抓一次才能覆盖。静态加壳不阻挡运行期 UTG 观测。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项** | com.android.settings 无障碍页中文本为『Servis Güncellemesi』的列表项，其 summary/description 为空 | 直接证明应用以与桌面同名的『服务更新』身份混入系统无障碍列表且不提供任何能力说明，是身份伪装与欺骗授权的核心证据 | 列表项文本等于 Servis Güncellemesi；列表项描述/摘要字段为空或缺失；条目图标与桌面 launcher 图标一致 |
| **冷启动引导弹窗页 / 隐形 Activity 页** | ButGLtznTLN 启动后覆盖的 Activity，或 ughndgrsdb.* 中 label 为空、不进最近任务的 Activity | 捕获到真实引导文案与按钮结构，才能区分是否属于不可取消的强制引导，填补静态不可见的空白 | 页面是否仅有单一『开启/继续』按钮而无取消/跳过；是否包含指向无障碍或应用详情的说明文字；是否包含土耳其语假更新或故障恐吓文案 |
| **设置页后压栈遮罩页** | 应用进程在 com.android.settings 之上新增的 TYPE_APPLICATION_OVERLAY/TYPE_SYSTEM_ALERT 窗口或单 task 隐形 Activity | 确认是否在系统设置页之上叠放半透明指引层或伪造无障碍开关页，这是判定欺骗性引导的关键运行期信号 | 无障碍节点树中出现两个包名叠加（settings + com.wdgrlnjoufx.qdlijknlopte）；遮罩层是否绘制箭头/手指指向真实开关位置；遮罩层是否伪造无障碍开关控件 |
| **拒权返回后的反应页** | 从系统设置按返回键回到应用后的界面 | 判定是否构成拒权循环重跳（onResume 死循环或定时器反复拉起设置页） | 返回后 1-3 秒内是否再次自动跳转设置页；返回后是否出现新的不可取消弹窗 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.wdgrlnjoufx.qdlijknlopte.gVQCLYjZ（无障碍服务，label=Servis Güncellemesi，无 description）`
- `res/xml/elpkjxdgjac.xml（canRetrieveWindowContent=true，settingsActivity=com.example.root.myapplication.MainActivity）`
- `com.srscyf.tdrlieo.Ewslytsy.onCreate`
- `com.srscyf.tdrlieo.UiBQKt.qUclZlPQ`
- `com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.ButGLtznTLN（LAUNCHER，DEX 中无同名类）`
- `unknown/image/mediumcrop（经 firstlist.txt 索引的可疑加密载荷）`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验，8 次工具调用后完成分析）

**1. 无障碍服务声明本身“干净得可疑”**
- 服务 [gVQCLYjZ](<resource-unit:#1 manifest:components>) 由 `android:label="Servis Güncellemesi"` 标记，与桌面名称**完全一致**；用户在系统无障碍列表里看到的条目与应用图标无法区分。
- 无障碍配置 [elpkjxdgjac.xml](<resource-unit:#1 file:res/xml/elpkjxdgjac.xml>) 只声明 `typeWindowContentChanged|typeWindowStateChanged`、`flagReportViewIds`、`canRetrieveWindowContent="true"`，**完全没有 `android:description` / `android:summary`**，因此系统设置页不展示任何功能说明，用户只能看到一个名称，无从判断它要读取所有界面内容。
- 同一配置里的 `android:settingsActivity="com.example.root.myapplication.MainActivity"` 是外部示例工程的模板残留，说明这份无障碍配置是从别处复制而来，并非为“服务更新”业务设计。

**2. 引导链路在静态层面被刻意隐藏**
- 启动 Activity `com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.ButGLtznTLN` 在 DEX 中**不存在同名类**（`get_class_structure` 返回 Class not found），Manifest 声明的包名 `com.wdgrlnjoufx.qdlijknlopte` 在 DEX 里也查不到对应类；DEX 只暴露 `com.srscyf.tdrlieo`(25 类) 与 `com.hcnrjn.hcnrjn`(5 类)。
- 真实实现主体藏在**仿冒 `android.support` 命名空间的 `android.support.hcnrjn`** 下（351 类 / 8 子包，类名 `GMuZKjNYMwCk`、`AvXGRY`、`DwLvLRMmfi` 等）。
- [Ewslytsy.onCreate()](<resource-unit:#1.dex1 code:com.srscyf.tdrlieo.Ewslytsy#onCreate>) 通过 [UiBQKt.qUclZlPQ()](<resource-unit:#1.dex1 code:com.srscyf.tdrlieo.UiBQKt#qUclZlPQ>) **反射获取类并实例化**，并用大量假字符串、恒真恒假分支填充，静态上不暴露装配目标。
- `strings` 全量检索**未命中** `ACCESSIBILITY_SETTINGS`、`APPLICATION_DETAILS_SETTINGS`、`accessibilityservice` 明文，说明跳转用 action 字符串由运行时拼接或解密得到，而不是硬编码常量。

**3. 引导界面载体线索**
- Manifest 中十余个 `android:label=""`、`Theme.NoDisplay`/`Theme.Translucent.NoTitleBar`、`excludeFromRecents="true"`、`launchMode="singleTask"` 的 Activity 群（`XmWSEBY`、`CtxZwVg`、`GSXocBY`、`cvPravViblhI`、`kSNKtOkRtf`、`shtStdaFBR`、`XDzkxvk`、`aznFdR`…），配合 `SYSTEM_ALERT_WINDOW`，是典型的遮罩、钓鱼页承载结构。
- 应用无 `assets/`、无任何本地 HTML；`unknown/image/mediumcrop`（233 KB，文件头 `09 C8 01 00…` 非图片魔数）由 `firstlist.txt`（内容 `image/mediumcrop`）索引，形态与**加密二阶段载荷**一致。
- 仅有 `res/layout/*.xml` 十余个极简布局（189–272 字节，多为单控件）与 `res/values/public.xml`，无 `strings.xml`，所有提示文案均不在资源中。

**4. 未决边界**
引导文案的具体原文、跳转时序、是否叠遮罩、是否拒权循环，均落在反射装配的混淆命名空间内，且受载荷加密影响，**纯静态不可还原**。建议按下方 UTG 钩子以动态方式捕获。

---

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "Manifest、无障碍服务声明与 res/xml/elpkjxdgjac.xml 完全静态可见；但引导页面实现被隐藏：启动 Activity 类 ughndgrsdb.ButGLtznTLN 在 DEX 中不存在，真实实现位于仿冒 android.support.hcnrjn 命名空间的 351 个混淆类，由 Application Ewslytsy.onCreate 经 UiBQKt 反射装配；跳转用 action 字符串无明文（strings 未命中 ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS），无 assets/ 与本地 HTML，提示文案不在 res 资源中（无 strings.xml）；unknown/image/mediumcrop（233KB，非图片魔数）由 firstlist.txt 索引，疑为加密二阶段载荷。",
  "summary_one_liner": "以与桌面同名的土耳其语『Servis Güncellemesi』注册无任何 description 的窗口内容读取无障碍服务，真实引导逻辑藏于仿冒 android.support 命名空间的混淆类并经反射装配，配合短信拦截、悬浮窗与用量统计权限形成木马能力面。",
  "disguise_identity": {
    "app_display_name": "Servis Güncellemesi",
    "claimed_brand_or_persona": "伪装为土耳其语『系统服务更新』（Servis Güncellemesi），无真实品牌归属",
    "a11y_service_label": "Servis Güncellemesi",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍服务 label 与桌面 label 完全同名同图标，用户在系统无障碍列表无法区分；无障碍配置无 android:description/ android:summary，隐藏能力说明；settingsActivity 残留外部示例模板类 com.example.root.myapplication.MainActivity；无障碍配置的 accessibilityFlags 显式开启 flagReportViewIds + canRetrieveWindowContent；十余个 label 为空、Theme.NoDisplay/Translucent、excludeFromRecents、singleTask 的隐形 Activity 群用于承载遮罩与钓鱼页；真实实现藏在仿冒 android.support.hcnrjn 命名空间的混淆类中并经反射装配；无 assets/、无 strings.xml，文案与 action 字符串不在静态资源内"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.ButGLtznTLN（MAIN/LAUNCHER，theme=@android:style/Theme.Translucent.NoTitleBar）",
      "trigger_event": "用户点击桌面图标，Activity onCreate",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "类 ButGLtznTLN 在 DEX 中不存在同名定义，启动后实际呈现内容无法静态还原",
      "user_action_requested": "不可静态判定",
      "code_anchor": "AndroidManifest.xml activity com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.ButGLtznTLN"
    },
    {
      "step": 2,
      "stage": "引导说明页",
      "screen_or_component": "com.srscyf.tdrlieo.Ewslytsy（Application）+ com.srscyf.tdrlieo.UiBQKt（反射装载器）",
      "trigger_event": "Application.onCreate 反射取类并实例化",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "onCreate 中仅有 \"serudp reuyoitrms\"、\"teteaitomch\"、\"oseopsawmesf rsi\" 等无意义填充字符串，真实引导入口由反射装配",
      "user_action_requested": "不可静态判定",
      "code_anchor": "com.srscyf.tdrlieo.Ewslytsy.onCreate / com.srscyf.tdrlieo.UiBQKt.qUclZlPQ"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "com.wdgrlnjoufx.qdlijknlopte.gVQCLYjZ（BIND_ACCESSIBILITY_SERVICE）+ @xml/elpkjxdgjac 指向的 settingsActivity com.example.root.myapplication.MainActivity",
      "trigger_event": "疑似由混淆类拼接 Settings.ACTION_ACCESSIBILITY_SETTINGS 拉起（明文常量未静态命中）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（android:description 缺失，系统页仅显示 label）",
      "shown_text_zh": "系统无障碍设置列表中出现『Servis Güncellemesi』一项，无任何功能说明文字",
      "user_action_requested": "用户需在系统无障碍列表中手动找到并打开该服务开关",
      "code_anchor": "res/xml/elpkjxdgjac.xml; AndroidManifest.xml service com.wdgrlnjoufx.qdlijknlopte.gVQCLYjZ"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.* 隐形 Activity 群（XmWSEBY/CtxZwVg/GSXocBY/cvPravViblhI/kSNKtOkRtf/shtStdaFBR/XDzkxvk/aznFdR 等）",
      "trigger_event": "静态不可还原（受 SYSTEM_ALERT_WINDOW 与 singleTask+excludeFromRecents 配置支持）",
      "ui_carrier": "悬浮窗Overlay",
      "shown_text_verbatim": "无",
      "shown_text_zh": "十余个 label 为空、NoDisplay/Translucent、不进最近任务的 Activity 具备在设置页之上叠放引导层或伪造开关页的配置条件，实际文案未静态暴露",
      "user_action_requested": "不可静态判定（疑为点击开关位置的引导）",
      "code_anchor": "AndroidManifest.xml activities com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.*"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "gVQCLYjZ 无障碍服务（canRetrieveWindowContent=true, flagReportViewIds）+ rojchd.uWwKarFK（SMS_DELIVER）/ rojchd.VEaEjVUFDYJ（WAP_PUSH_DELIVER）",
      "trigger_event": "服务 onServiceConnected 后接收 typeWindowContentChanged / SMS_DELIVER 广播",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后读取任意前台窗口内容与节点 ID，同时可接收短信投递广播",
      "user_action_requested": "无需用户操作",
      "code_anchor": "res/xml/elpkjxdgjac.xml; AndroidManifest.xml receiver com.wdgrlnjoufx.qdlijknlopte.rojchd.uWwKarFK"
    }
  ],
  "text_presentation_locations": [
    "res/xml/elpkjxdgjac.xml 未提供 android:description 与 android:summary，系统无障碍设置列表中该条目无任何说明文字，仅显示服务名『Servis Güncellemesi』",
    "AndroidManifest.xml 中无障碍服务 android:label 与 application android:label 同为『Servis Güncellemesi』，桌面图标与无障碍列表条目同名同图标",
    "应用无 assets/ 目录、无本地 HTML 文件，引导文案不通过 WebView 本地页面呈现",
    "res/values 下仅有 attrs.xml / ids.xml / public.xml，无 strings.xml，所有提示文案未在资源表中定义",
    "十余个 android:label=\"\" 的 ughndgrsdb.* Activity 为空白标题的承载容器，配合 SYSTEM_ALERT_WINDOW 与 Translucent/NoDisplay 主题具备在系统设置页之上叠放引导层的能力",
    "res/layout/ 下十余个 189–272 字节的极简布局（ayftqrnhad.xml、bifxwsat.xml、zilntq.xml 等）为单控件容器，无可见说明性文本",
    "unknown/image/mediumcrop（233KB）由 unknown/image/firstlist.txt（内容 image/mediumcrop）索引，为疑加密载荷而非文本载体"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Servis Güncellemesi",
      "text_zh": "服务更新",
      "source_location": "AndroidManifest.xml application android:label 与 service com.wdgrlnjoufx.qdlijknlopte.gVQCLYjZ android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "com.example.root.myapplication.MainActivity",
      "text_zh": "示例工程残留的设置页类名（非本应用业务类）",
      "source_location": "res/xml/elpkjxdgjac.xml android:settingsActivity",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "image/mediumcrop",
      "text_zh": "载荷索引清单，指向 unknown/image/mediumcrop",
      "source_location": "unknown/image/firstlist.txt",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "serudp reuyoitrms / teteaitomch / oseopsawmesf rsi",
      "text_zh": "无意义填充字符串（用于干扰静态分析）",
      "source_location": "com.srscyf.tdrlieo.Ewslytsy.onCreate 硬编码",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "static_hidden",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原：引导与重试逻辑位于反射装配的混淆类 android.support.hcnrjn.* 中，明文 action 常量未命中，无法确认是否在 onResume 检测未授权后循环重跳",
    "overlay_or_fake_settings": "具备强配置条件但未静态证实：Manifest 声明 SYSTEM_ALERT_WINDOW，且存在 8 个以上 label 为空、Theme.NoDisplay/Theme.Translucent.NoTitleBar、excludeFromRecents、launchMode=singleTask 的隐形 Activity，可在系统无障碍页之上叠放引导遮罩或高仿开关页；具体叠层代码未静态还原",
    "restricted_settings_13plus_coaching": "无静态证据（targetSdkVersion=27，未达 Android 13 受限设置门槛；DEX 未命中 APPLICATION_DETAILS_SETTINGS 明文）",
    "post_grant_anti_removal": "无静态证据：未发现 GLOBAL_ACTION_BACK/HOME 相关明文常量，也无 ACCESSIBILITY_SETTINGS 监听明文，实际是否自点确认或阻止撤权无法静态确认",
    "benign_graceful_degradation": "无（未发现任何降级、手动模式或替代路径；反而声明 REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 与 RECEIVE_BOOT_COMPLETED 强化常驻）"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在系统无障碍设置页（Settings$Secure 或 com.android.settings 的 AccessibilitySettings 界面）出现『Servis Güncellemesi』条目时立即拉起 UTG，同时并行监测应用自身是否在设置页之上压入新 Activity/悬浮窗；冷启动后若 3 秒内未出现设置页，则改为监测 SYSTEM_ALERT_WINDOW 窗口添加事件",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页中文本为『Servis Güncellemesi』的列表项，其 summary/description 为空",
        "why_most_useful": "直接证明应用以与桌面同名的『服务更新』身份混入系统无障碍列表且不提供任何能力说明，是身份伪装与欺骗授权的核心证据",
        "observable_utg_signals": [
          "列表项文本等于 Servis Güncellemesi",
          "列表项描述/摘要字段为空或缺失",
          "条目图标与桌面 launcher 图标一致"
        ]
      },
      {
        "page_role": "冷启动引导弹窗页 / 隐形 Activity 页",
        "page_identifier": "ButGLtznTLN 启动后覆盖的 Activity，或 ughndgrsdb.* 中 label 为空、不进最近任务的 Activity",
        "why_most_useful": "捕获到真实引导文案与按钮结构，才能区分是否属于不可取消的强制引导，填补静态不可见的空白",
        "observable_utg_signals": [
          "页面是否仅有单一『开启/继续』按钮而无取消/跳过",
          "是否包含指向无障碍或应用详情的说明文字",
          "是否包含土耳其语假更新或故障恐吓文案"
        ]
      },
      {
        "page_role": "设置页后压栈遮罩页",
        "page_identifier": "应用进程在 com.android.settings 之上新增的 TYPE_APPLICATION_OVERLAY/TYPE_SYSTEM_ALERT 窗口或单 task 隐形 Activity",
        "why_most_useful": "确认是否在系统设置页之上叠放半透明指引层或伪造无障碍开关页，这是判定欺骗性引导的关键运行期信号",
        "observable_utg_signals": [
          "无障碍节点树中出现两个包名叠加（settings + com.wdgrlnjoufx.qdlijknlopte）",
          "遮罩层是否绘制箭头/手指指向真实开关位置",
          "遮罩层是否伪造无障碍开关控件"
        ]
      },
      {
        "page_role": "拒权返回后的反应页",
        "page_identifier": "从系统设置按返回键回到应用后的界面",
        "why_most_useful": "判定是否构成拒权循环重跳（onResume 死循环或定时器反复拉起设置页）",
        "observable_utg_signals": [
          "返回后 1-3 秒内是否再次自动跳转设置页",
          "返回后是否出现新的不可取消弹窗"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "显著盲区：1) 启动 Activity ButGLtznTLN 类在 DEX 中不存在，引导逻辑经 Application 反射装配，静态无法确认引导页面文案与时序；2) 跳转 action 字符串非明文，无法确认是否使用 ACTION_ACCESSIBILITY_SETTINGS 还是直接 ComponentName 跳转；3) unknown/image/mediumcrop（233KB，非图片魔数）疑为加密二阶段载荷，可能承载远端下发的引导页/钓鱼页模板；4) 若引导完全依赖运行期解密或远端 HTML，UTG 需在设置页出现瞬间与首次冷启动后各抓一次才能覆盖。静态加壳不阻挡运行期 UTG 观测。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_OVERLAY_STACK_ON_SETTINGS",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD"
  ],
  "code_anchors": [
    "com.wdgrlnjoufx.qdlijknlopte.gVQCLYjZ（无障碍服务，label=Servis Güncellemesi，无 description）",
    "res/xml/elpkjxdgjac.xml（canRetrieveWindowContent=true，settingsActivity=com.example.root.myapplication.MainActivity）",
    "com.srscyf.tdrlieo.Ewslytsy.onCreate",
    "com.srscyf.tdrlieo.UiBQKt.qUclZlPQ",
    "com.wdgrlnjoufx.qdlijknlopte.ughndgrsdb.ButGLtznTLN（LAUNCHER，DEX 中无同名类）",
    "unknown/image/mediumcrop（经 firstlist.txt 索引的可疑加密载荷）"
  ]
}
```

</details>
