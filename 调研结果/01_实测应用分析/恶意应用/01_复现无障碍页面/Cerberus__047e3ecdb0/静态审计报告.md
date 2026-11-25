# MB_068__047e3ecdb0｜Cerberus — Android Güncelleme

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`packed_or_encrypted`  ｜  **APKAudit 耗时**：146.1s

## 1. 一句话核心结论

- **核心申请方式**：以“Android Güncelleme（Android 更新）”假更新身份冷启动即注入加密二阶段 DEX，无障碍服务无描述且不限包名、可读取全系统窗口内容，具体引导 UI 全部藏于二阶段载荷。
- **静态可见性说明**：classes.dex 中不含 com.ujirteg.* 任何类（全文检索 ujirteg/kuofsogpbnjo 均 0 命中），无障碍服务、Launcher Activity、全部引导页均在运行期二阶段 DEX 中；Application.attachBaseContext 通过反射构造 DexClassLoader 并把 ActivityThread.mPackage.mClassLoader 字段替换为该 loader 完成注入，载荷实体为包内加密/二进制资产 assets/kmbiI.json 与 assets/sin_enc_lut。仅 Manifest 声明、无障碍 xml 配置、设备管理器策略与注入链可静态确认；引导弹窗/HTML/跳转文案不可静态还原。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`CARRIER_OVERLAY_MASK_OR_GUIDE`（悬浮窗/透明遮罩引导层）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`DROPPER_STAGE1_INSTALL_OR_EMBEDDED`（一阶段Dropper/Session安装器或嵌包二阶段投递）、`STATIC_PACKED_OR_ENCRYPTED_PAYLOAD`（强加壳/VMP/AES密文或远端载荷致静态遮蔽）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `047e3ecdb04d695b7e8a3c2789c29ec57da19f58bdcdb1d97fa926205ce718eb` |
| 包名 / 年份 | `com.cable.liar` / 2025 |
| 家族 / 品类 | **Cerberus**（同池样本数：15） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | Android Güncelleme |
| 引导页宣称品牌/身份 | 冒充 Android 系统更新（Turkish “Android Güncelleme”），并同时声明 android.app.role.SMS 冒充短信默认应用 |
| 系统无障碍列表服务名 | Android Güncelleme |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：无障碍配置 res/xml/uuujc.xml 无 android:description（系统无障碍列表无任何用途说明）；多个 Activity 使用 android:label="" 空显示名 + 118 字节透明图标 @drawable/sqbafpkv + Theme.NoDisplay + excludeFromRecents 实现不可见跳转；类名/字符串全量混淆并用 XOR 混淆字符串（curtaincage/sampletarget/catspice 解出 android.app.ActivityThread、mPackage、mClassLoader）；包名 com.cable.liar 与类包 com.ujirteg.qlowvkvdwx 完全错位；无障碍服务不受 packageNames 限制，监听全系统窗口内容。 |
| 无障碍服务类名 | `com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=False` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, READ_SMS, RECEIVE_SMS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, REQUEST_INSTALL_PACKAGES, SEND_SMS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | com.cable.liar.FHtJbMxKbHtAhBmMqZzEbFgErDcRo（Application.attachBaseContext） | 进程启动时 attachBaseContext 回调（早于任何 Activity 的 onCreate） | 不可静态还原 | 无 | 无 | `com.cable.liar.FHtJbMxKbHtAhBmMqZzEbFgErDcRo.attachBaseContext → celeryplace → DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.winterstove` |
| 2 | 冷启动入口 | Launcher Activity com.ujirteg.qlowvkvdwx.pcc（MAIN/LAUNCHER + android.app.role.SMS） | 用户点击桌面图标（图标/名称来自 android:label="Android Güncelleme"） | 不可静态还原 | 无 | 不可静态还原（推测要求用户继续操作以进入引导页） | `AndroidManifest.xml: activity com.ujirteg.qlowvkvdwx.pcc` |
| 3 | 引导说明页 | 不可静态还原（疑似二阶段 DEX 内 Dialog/WebView/隐藏 Activity，如 com.ujirteg.qlowvkvdwx.vjziz.dsxujce / tuixszjun / ucjrgbvsnflef） | 不可静态还原 | 不可静态还原 | 无 | 不可静态还原 | `AndroidManifest.xml: activity com.ujirteg.qlowvkvdwx.vjziz.*（label=""、Theme.NoDisplay、excludeFromRecents）` |
| 4 | 跳无障碍设置 | 系统设置 ACTION_ACCESSIBILITY_SETTINGS → 无障碍服务列表项 “Android Güncelleme” | 不可静态还原（classes.dex 中检索 ACCESSIBILITY_SETTINGS 0 命中，跳转代码在二阶段） | 系统无障碍页 | **原文**：Android Güncelleme<br>**译注**：系统无障碍服务列表中显示的服务名（无描述、无用途说明） | 在系统无障碍列表中手动开启该服务（无取消/跳过按钮的静态证据） | `AndroidManifest.xml: service com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo（android:label="Android Güncelleme"）；res/xml/uuujc.xml` |
| 5 | 获权后动作 | 无障碍服务 com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo（typeWindowContentChanged\|typeWindowStateChanged, canRetrieveWindowContent=true, flagReportViewIds） | 系统下发窗口内容/状态变更事件 | 不可静态还原 | 无 | 无 | `res/xml/uuujc.xml；AndroidManifest.xml: kuofsogpbnjo 服务声明` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 系统无障碍服务列表：服务项名称 “Android Güncelleme”（AndroidManifest.xml 中 service android:label），且 res/xml/uuujc.xml 未配置 android:description，列表项无任何用途说明文字
- 桌面启动器：应用名 “Android Güncelleme”（application android:label）与图标 @mipmap/ic_launcher
- 设备管理器/广播接收器标签：receiver android:label="Android Güncelleme"（com.ujirteg.qlowvkvdwx.jzkbfu.ecoiaazxjradrd）
- 不可见 Activity 项：com.ujirteg.qlowvkvdwx.vjziz.dsxujce / tuixszjun / ucjrgbvsnflef 与 com.ujirteg.qlowvkvdwx.jzkbfu.gxk 使用 android:label=""（空显示名），不呈现任何文字
- 包内引导文案载体：无本地 HTML/strings 引导文案，assets/ 全为广告 SDK 与订阅/Lottie 资源；引导文本推测位于加密载荷 assets/kmbiI.json（非文本二进制）解出的二阶段 DEX 内，静态不可读

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Android Güncelleme | Android 更新 | `AndroidManifest.xml: application@android:label 与 service com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo@android:label、receiver ecoiaazxjradrd@android:label` | 假更新 |
| en | android.app.ActivityThread | （反射目标类名，非用户可见文案） | `com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.curtaincage（XOR 解密 {93,104,94,...} ^ {60,6,58}）` | 未知 |
| en | mPackage | （反射字段名，非用户可见文案） | `com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.sampletarget（XOR 解密 {60,82,48,...} ^ {81,2}）` | 未知 |
| en | mClassLoader | （反射字段名，非用户可见文案） | `com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.catspice（XOR 解密 {102,76,13,...} ^ {11,15,97}）` | 未知 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：不可静态还原（跳转与 onResume 重跳逻辑位于加密二阶段 DEX；classes.dex 中检索 ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS 均 0 命中）
- **遮罩叠层 / 高仿系统设置页**：不可静态还原；但已确认持有 SYSTEM_ALERT_WINDOW 与无障碍 flagReportViewIds+canRetrieveWindowContent，具备叠放覆盖层的技术条件，需运行期截图确认
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdkVersion=30，未发现受限设置教学代码；实际是否含于二阶段载荷不可静态确认）
- **获权后即时行为与防撤权机制**：不可静态还原；已确认配套 force-lock/wipe-data 设备管理器（res/xml/lno.xml）与 DISABLE_KEYGUARD、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 权限，具备抗卸载/抗撤权条件，未见自点确认代码
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动点击桌面图标 “Android Güncelleme” 后立即开始 UTG 采样（attachBaseContext 已完成注入，首帧即为二阶段 UI）；同时在检测到栈顶出现 com.ujirteg.qlowvkvdwx.vjziz.* 或 com.ujirteg.qlowvkvdwx.jzkbfu.gxk 等 label=""+Theme.NoDisplay 的 Activity 时立即抓帧；并在系统设置包 com.android.settings 进入前台时抓取无障碍列表项。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：存在显著盲区：引导 UI 全部位于运行期解密并注入的二阶段 DEX（类加载器劫持式 DexClassLoader + ActivityThread.mPackage.mClassLoader 字段替换），包内无任何本地 HTML/strings 引导文案，静态只能确认 Manifest 声明与注入链；静态“未加壳”预筛为假阴性。若二阶段界面采用纯图/视频载体（包内已含 questionary_v3_welcome_video.mp4 等素材），需开启 OCR/录屏辅助。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动首帧页（二阶段 DEX 接管后的第一个界面）** | Activity 名 com.ujirteg.qlowvkvdwx.pcc 或随后栈顶的 com.ujirteg.qlowvkvdwx.vjziz.*；包名 com.cable.liar | 静态完全不可见，此帧决定是否存在引导说明页/弹窗，以及文案与伪装身份是否与 “Android 更新” 一致 | 全部可见文本节点（标题/正文/按钮）；是否存在关闭/取消/跳过按钮；是否为假系统更新进度或故障提示样式 |
| **跳转前引导页（含无障碍说明/教学）** | 包名仍为 com.cable.liar 且页面内容出现“无障碍/辅助功能/Erişilebilirlik/Accessibility”字样 | 直接证明诱导话术性质（假更新/假安全/分步教学）与是否可取消 | 引导文案逐字文本；是否含分步编号或箭头指示；是否提示“忽略系统警告” |
| **系统无障碍服务列表项** | com.android.settings 无障碍页面中文本 “Android Güncelleme” 的列表项 | 确认系统侧展示的服务名与缺失描述，是身份冒充的直接证据 | 服务项显示名；描述文本为空；开关初始状态与随后是否被开启 |
| **跳转返回后的遮罩/重跳页** | 设置页后 500–1500ms 内栈顶变为 com.cable.liar 的悬浮窗或 Theme.NoDisplay Activity | 判定拒绝/返回后的循环重跳与遮罩叠层指引（静态被壳遮蔽，只能运行期取证） | 是否出现半透明遮罩/手指指引图；是否再次拉起系统设置；返回键是否被吞掉 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.cable.liar.FHtJbMxKbHtAhBmMqZzEbFgErDcRo.attachBaseContext`
- `com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.winterstove`
- `com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.cautionbrick`
- `com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.shrimpdivorce`
- `res/xml/uuujc.xml`
- `AndroidManifest.xml: service com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo / activity com.ujirteg.qlowvkvdwx.pcc`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**核心判定：无障碍引导流程本身不在静态 DEX 中，而是被藏进运行期解密的二阶段载荷，因此静态不可见。**

1. **Manifest 层可确认的“无障碍诱导面”**
   - 应用显示名与无障碍服务标签均为 `Android Güncelleme`（土耳其语“Android 更新”），冒充系统更新；`targetSdkVersion=30`、`minSdkVersion=15`。
   - 无障碍服务 [com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo](<resource-unit:#1 manifest:components>) 声明 `BIND_ACCESSIBILITY_SERVICE`，其配置 [res/xml/uuujc.xml](<resource-unit:#1 file:res/xml/uuujc.xml>) **只有** `typeWindowContentChanged|typeWindowStateChanged`、`canRetrieveWindowContent=true`、`flagReportViewIds`，**无 `android:description`、无 `packageNames` 白名单** → 可读取全系统任意应用窗口内容（典型银行木马黑屏覆盖/凭证窃取的配置形态），但无任何面向用户的说明文案。
   - 启动入口 [com.ujirteg.qlowvkvdwx.pcc](<resource-unit:#1 manifest:components>) 同时挂 `LAUNCHER` 与 `android.app.role.SMS`（冒充短信默认应用）；另有多个 `android:label=""`、`icon=@drawable/sqbafpkv`（118 字节透明小图）、`excludeFromRecents`、`Theme.NoDisplay` 的不可见 Activity（`dsxujce`、`tuixszjun`(singleTask)、`ucjrgbvsnflef`、`gzk`、`yxh`），用于无界面跳转与页面抢占。
   - 配套：`force-lock`/`wipe-data` 设备管理器、`SYSTEM_ALERT_WINDOW`、`REQUEST_INSTALL_PACKAGES`、`READ_SMS/SEND_SMS`、`QUERY_ALL_PACKAGES`。

2. **关键发现：`com.ujirteg.*` 全部类在 `classes.dex` 中不存在**
   - 对 `classes.dex` 全文检索 `ujirteg` / `kuofsogpbnjo` 均 0 命中；包列表仅有 `com.cable.liar`、`com.intentsoftware.addapptr`(广告 SDK)、`com.cable.*` 等。**即无障碍服务、Launcher Activity、全部引导页均位于外部二阶段 DEX**。

3. **二阶段载荷的加载链已完整还原（可静态证实）**
   - [FHtJbMxKbHtAhBmMqZzEbFgErDcRo#attachBaseContext](<resource-unit:#1.dex1 code:com.cable.liar.FHtJbMxKbHtAhBmMqZzEbFgErDcRo#attachBaseContext>) → `callindustry/getDir` + `surfacehover/getDir`（dex 输出目录与文件名来自解密字符串）→ [lazysurge](<resource-unit:#1.dex1 code:com.cable.liar.FHtJbMxKbHtAhBmMqZzEbFgErDcRo#lazysurge>) → [celeryplace](<resource-unit:#1.dex1 code:com.cable.liar.FHtJbMxKbHtAhBmMqZzEbFgErDcRo#celeryplace>) → [DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx#winterstove](<resource-unit:#1.dex1 code:com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx#winterstove>)。
   - `winterstove` 用混淆字符串解密函数（`curtaincage`/`sampletarget`/`catspice`，均为 `bArr[i]^key[i%n]`）解出反射目标，我手工还原为：`android.app.ActivityThread`、`mPackage`、`mClassLoader`；随后 [cautionbrick](<resource-unit:#1.dex1 code:com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx#cautionbrick>) 反射构造 `DexClassLoader`，[shrimpdivorce](<resource-unit:#1.dex1 code:com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx#shrimpdivorce>) 以 `Field.set` 把该 loader 写回 `ActivityThread.mPackage.mClassLoader` → **全局类加载器劫持式 DEX 注入**，属强隐蔽的壳/二阶段加载（`apkid` 初判“未加壳”不成立）。
   - 加密载荷实体在包内可见但不可静态解析：[assets/kmbiI.json](<resource-unit:#1 file:assets/kmbiI.json>)（非文本二进制，66KB）与 [assets/sin_enc_lut](<resource-unit:#1 file:assets/sin_enc_lut>)（89KB 加密体）。

4. **因此对“如何一步步引导开启无障碍”的结论**：静态只能确证**冷启动即接管**（`Application.attachBaseContext` 阶段完成注入，早于任何 Activity）+ **无障碍服务以“Android Güncelleme”名义出现在系统无障碍列表** + **存在大量空白标签隐藏 Activity 承接跳转**；而具体的引导弹窗、`ACTION_ACCESSIBILITY_SETTINGS` 跳转、拒绝后重跳循环、遮罩叠层、13+ 受限设置教学等运行期 UI 编排，**全部位于加密二阶段 DEX，本次静态不可还原**。这也意味着预筛线索中 `anti_removal=[] / overlay=[]` 的“空”是壳导致的假阴性。

**建议的纯 UTG 抓取点（基于静态可确认的入口）**：冷启动 launcher `com.ujirteg.qlowvkvdwx.pcc` 首帧后 0–2s；系统无障碍服务列表项文本 `Android Güncelleme`；以及任何 `label=""`+`Theme.NoDisplay` 的 Activity 出现在栈顶的瞬间。

> 说明：本轮受调用预算约束未写入风险台账，以下为可直接落账的命题——「加密二阶段 DEX 注入 + 无障碍服务全窗口监听 + 假更新身份」应作为 `malware_trojan`/high 记录；引导流程文本需动态复现补齐。

```json
{
  "static_visibility": "packed_or_encrypted",
  "visibility_note": "classes.dex 中不含 com.ujirteg.* 任何类（全文检索 ujirteg/kuofsogpbnjo 均 0 命中），无障碍服务、Launcher Activity、全部引导页均在运行期二阶段 DEX 中；Application.attachBaseContext 通过反射构造 DexClassLoader 并把 ActivityThread.mPackage.mClassLoader 字段替换为该 loader 完成注入，载荷实体为包内加密/二进制资产 assets/kmbiI.json 与 assets/sin_enc_lut。仅 Manifest 声明、无障碍 xml 配置、设备管理器策略与注入链可静态确认；引导弹窗/HTML/跳转文案不可静态还原。",
  "summary_one_liner": "以“Android Güncelleme（Android 更新）”假更新身份冷启动即注入加密二阶段 DEX，无障碍服务无描述且不限包名、可读取全系统窗口内容，具体引导 UI 全部藏于二阶段载荷。",
  "disguise_identity": {
    "app_display_name": "Android Güncelleme",
    "claimed_brand_or_persona": "冒充 Android 系统更新（Turkish “Android Güncelleme”），并同时声明 android.app.role.SMS 冒充短信默认应用",
    "a11y_service_label": "Android Güncelleme",
    "identity_mismatch": true,
    "obfuscation_tricks": "无障碍配置 res/xml/uuujc.xml 无 android:description（系统无障碍列表无任何用途说明）；多个 Activity 使用 android:label=\"\" 空显示名 + 118 字节透明图标 @drawable/sqbafpkv + Theme.NoDisplay + excludeFromRecents 实现不可见跳转；类名/字符串全量混淆并用 XOR 混淆字符串（curtaincage/sampletarget/catspice 解出 android.app.ActivityThread、mPackage、mClassLoader）；包名 com.cable.liar 与类包 com.ujirteg.qlowvkvdwx 完全错位；无障碍服务不受 packageNames 限制，监听全系统窗口内容。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "com.cable.liar.FHtJbMxKbHtAhBmMqZzEbFgErDcRo（Application.attachBaseContext）",
      "trigger_event": "进程启动时 attachBaseContext 回调（早于任何 Activity 的 onCreate）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "此阶段无界面，完成字符串解密、dex 输出目录创建与类加载器注入",
      "user_action_requested": "无",
      "code_anchor": "com.cable.liar.FHtJbMxKbHtAhBmMqZzEbFgErDcRo.attachBaseContext → celeryplace → DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.winterstove"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "Launcher Activity com.ujirteg.qlowvkvdwx.pcc（MAIN/LAUNCHER + android.app.role.SMS）",
      "trigger_event": "用户点击桌面图标（图标/名称来自 android:label=\"Android Güncelleme\"）",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "该 Activity 类体不在 classes.dex 中，界面内容由二阶段 DEX 提供，静态不可还原",
      "user_action_requested": "不可静态还原（推测要求用户继续操作以进入引导页）",
      "code_anchor": "AndroidManifest.xml: activity com.ujirteg.qlowvkvdwx.pcc"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "不可静态还原（疑似二阶段 DEX 内 Dialog/WebView/隐藏 Activity，如 com.ujirteg.qlowvkvdwx.vjziz.dsxujce / tuixszjun / ucjrgbvsnflef）",
      "trigger_event": "不可静态还原",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "无静态证据，需运行期 UTG 抓取",
      "user_action_requested": "不可静态还原",
      "code_anchor": "AndroidManifest.xml: activity com.ujirteg.qlowvkvdwx.vjziz.*（label=\"\"、Theme.NoDisplay、excludeFromRecents）"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置 ACTION_ACCESSIBILITY_SETTINGS → 无障碍服务列表项 “Android Güncelleme”",
      "trigger_event": "不可静态还原（classes.dex 中检索 ACCESSIBILITY_SETTINGS 0 命中，跳转代码在二阶段）",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Android Güncelleme",
      "shown_text_zh": "系统无障碍服务列表中显示的服务名（无描述、无用途说明）",
      "user_action_requested": "在系统无障碍列表中手动开启该服务（无取消/跳过按钮的静态证据）",
      "code_anchor": "AndroidManifest.xml: service com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo（android:label=\"Android Güncelleme\"）；res/xml/uuujc.xml"
    },
    {
      "step": 5,
      "stage": "获权后动作",
      "screen_or_component": "无障碍服务 com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo（typeWindowContentChanged|typeWindowStateChanged, canRetrieveWindowContent=true, flagReportViewIds）",
      "trigger_event": "系统下发窗口内容/状态变更事件",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "获权后读取全系统任意应用窗口内容（无 packageNames 限制），配合 SYSTEM_ALERT_WINDOW 可实施覆盖页/凭证窃取",
      "user_action_requested": "无",
      "code_anchor": "res/xml/uuujc.xml；AndroidManifest.xml: kuofsogpbnjo 服务声明"
    }
  ],
  "text_presentation_locations": [
    "系统无障碍服务列表：服务项名称 “Android Güncelleme”（AndroidManifest.xml 中 service android:label），且 res/xml/uuujc.xml 未配置 android:description，列表项无任何用途说明文字",
    "桌面启动器：应用名 “Android Güncelleme”（application android:label）与图标 @mipmap/ic_launcher",
    "设备管理器/广播接收器标签：receiver android:label=\"Android Güncelleme\"（com.ujirteg.qlowvkvdwx.jzkbfu.ecoiaazxjradrd）",
    "不可见 Activity 项：com.ujirteg.qlowvkvdwx.vjziz.dsxujce / tuixszjun / ucjrgbvsnflef 与 com.ujirteg.qlowvkvdwx.jzkbfu.gxk 使用 android:label=\"\"（空显示名），不呈现任何文字",
    "包内引导文案载体：无本地 HTML/strings 引导文案，assets/ 全为广告 SDK 与订阅/Lottie 资源；引导文本推测位于加密载荷 assets/kmbiI.json（非文本二进制）解出的二阶段 DEX 内，静态不可读"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Android Güncelleme",
      "text_zh": "Android 更新",
      "source_location": "AndroidManifest.xml: application@android:label 与 service com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo@android:label、receiver ecoiaazxjradrd@android:label",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "android.app.ActivityThread",
      "text_zh": "（反射目标类名，非用户可见文案）",
      "source_location": "com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.curtaincage（XOR 解密 {93,104,94,...} ^ {60,6,58}）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "mPackage",
      "text_zh": "（反射字段名，非用户可见文案）",
      "source_location": "com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.sampletarget（XOR 解密 {60,82,48,...} ^ {81,2}）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "mClassLoader",
      "text_zh": "（反射字段名，非用户可见文案）",
      "source_location": "com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.catspice（XOR 解密 {102,76,13,...} ^ {11,15,97}）",
      "rhetorical_frame": "未知"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "不可静态还原（跳转与 onResume 重跳逻辑位于加密二阶段 DEX；classes.dex 中检索 ACCESSIBILITY_SETTINGS/APPLICATION_DETAILS_SETTINGS 均 0 命中）",
    "overlay_or_fake_settings": "不可静态还原；但已确认持有 SYSTEM_ALERT_WINDOW 与无障碍 flagReportViewIds+canRetrieveWindowContent，具备叠放覆盖层的技术条件，需运行期截图确认",
    "restricted_settings_13plus_coaching": "无（targetSdkVersion=30，未发现受限设置教学代码；实际是否含于二阶段载荷不可静态确认）",
    "post_grant_anti_removal": "不可静态还原；已确认配套 force-lock/wipe-data 设备管理器（res/xml/lno.xml）与 DISABLE_KEYGUARD、REQUEST_IGNORE_BATTERY_OPTIMIZATIONS 权限，具备抗卸载/抗撤权条件，未见自点确认代码",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动点击桌面图标 “Android Güncelleme” 后立即开始 UTG 采样（attachBaseContext 已完成注入，首帧即为二阶段 UI）；同时在检测到栈顶出现 com.ujirteg.qlowvkvdwx.vjziz.* 或 com.ujirteg.qlowvkvdwx.jzkbfu.gxk 等 label=\"\"+Theme.NoDisplay 的 Activity 时立即抓帧；并在系统设置包 com.android.settings 进入前台时抓取无障碍列表项。",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动首帧页（二阶段 DEX 接管后的第一个界面）",
        "page_identifier": "Activity 名 com.ujirteg.qlowvkvdwx.pcc 或随后栈顶的 com.ujirteg.qlowvkvdwx.vjziz.*；包名 com.cable.liar",
        "why_most_useful": "静态完全不可见，此帧决定是否存在引导说明页/弹窗，以及文案与伪装身份是否与 “Android 更新” 一致",
        "observable_utg_signals": ["全部可见文本节点（标题/正文/按钮）", "是否存在关闭/取消/跳过按钮", "是否为假系统更新进度或故障提示样式"]
      },
      {
        "page_role": "跳转前引导页（含无障碍说明/教学）",
        "page_identifier": "包名仍为 com.cable.liar 且页面内容出现“无障碍/辅助功能/Erişilebilirlik/Accessibility”字样",
        "why_most_useful": "直接证明诱导话术性质（假更新/假安全/分步教学）与是否可取消",
        "observable_utg_signals": ["引导文案逐字文本", "是否含分步编号或箭头指示", "是否提示“忽略系统警告”"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "com.android.settings 无障碍页面中文本 “Android Güncelleme” 的列表项",
        "why_most_useful": "确认系统侧展示的服务名与缺失描述，是身份冒充的直接证据",
        "observable_utg_signals": ["服务项显示名", "描述文本为空", "开关初始状态与随后是否被开启"]
      },
      {
        "page_role": "跳转返回后的遮罩/重跳页",
        "page_identifier": "设置页后 500–1500ms 内栈顶变为 com.cable.liar 的悬浮窗或 Theme.NoDisplay Activity",
        "why_most_useful": "判定拒绝/返回后的循环重跳与遮罩叠层指引（静态被壳遮蔽，只能运行期取证）",
        "observable_utg_signals": ["是否出现半透明遮罩/手指指引图", "是否再次拉起系统设置", "返回键是否被吞掉"]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "存在显著盲区：引导 UI 全部位于运行期解密并注入的二阶段 DEX（类加载器劫持式 DexClassLoader + ActivityThread.mPackage.mClassLoader 字段替换），包内无任何本地 HTML/strings 引导文案，静态只能确认 Manifest 声明与注入链；静态“未加壳”预筛为假阴性。若二阶段界面采用纯图/视频载体（包内已含 questionary_v3_welcome_video.mp4 等素材），需开启 OCR/录屏辅助。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "CARRIER_OVERLAY_MASK_OR_GUIDE",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "DROPPER_STAGE1_INSTALL_OR_EMBEDDED",
    "STATIC_PACKED_OR_ENCRYPTED_PAYLOAD",
    "COERCE_NO_SKIP_NON_CANCELABLE"
  ],
  "code_anchors": [
    "com.cable.liar.FHtJbMxKbHtAhBmMqZzEbFgErDcRo.attachBaseContext",
    "com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.winterstove",
    "com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.cautionbrick",
    "com.cable.liar.DFeYjTbEoYnTtGiFiKeUqPpYqEkBnPaDcPyHdIxOkHfWgCaPx.shrimpdivorce",
    "res/xml/uuujc.xml",
    "AndroidManifest.xml: service com.ujirteg.qlowvkvdwx.bxqppotueb.kuofsogpbnjo / activity com.ujirteg.qlowvkvdwx.pcc"
  ]
}
```

</details>
