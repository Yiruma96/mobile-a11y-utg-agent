# MB_099__3d4f63fc88｜GodFather — MYT Müzik

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`clear`  ｜  **APKAudit 耗时**：144.7s

## 1. 一句话核心结论

- **核心申请方式**：冷启动即在语言/环境过滤后直接 startActivity 跳转系统无障碍设置，并用 fragment_args_key 把列表预定位到伪装成 com.viber.voip.InputService 的服务项，以'保护/更新生效'名义要求用户开启点击注入型无障碍。
- **静态可见性说明**：无壳无VMP；全部界面文案由 com.stringmanager.Change 以 AES/ECB(PBKDF2WithHmacSHA1(a,a,8,256)) 加密为 hex 常量，已离线静态还原433条明文，引导逻辑与跳转目标完全可读。残留缺口：承载引导弹窗的具体 Activity 未逐一反编译、远端C2下发HTML/配置未取回。
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_SYSTEM_A11Y_DESCRIPTION`（系统无障碍列表服务说明(android:description)）、`LURE_FAKE_UPDATE_OR_INSTALL`（假系统/应用更新或插件安装胁迫）、`LURE_FAKE_SECURITY_ANTIFRAUD`（假安全防护/杀毒扫描/反诈保护恐吓）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_SYSTEM_OR_BRAND_IMPERSONATION`（冒充系统组件/Google/大厂或银行品牌身份）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `3d4f63fc88ec8a4dfc9a5c3fee1a59ded40bbb2f4f04ed937c135b144e8a166d` |
| 包名 / 年份 | `com.snaperfect.inframe1` / 2024 |
| 家族 / 品类 | **GodFather**（同池样本数：11） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | @string/app_name（activity-alias com.snaperfect.inframe1.Android） |
| 引导页宣称品牌/身份 | Viber（无障碍服务包名与类名伪装为 com.viber.voip.InputService） |
| 系统无障碍列表服务名 | @string/app_name（与桌面名一致，冒充 Viber 显示名） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：多activity-alias伪装：Android(label=app_name) 与 Youtube(label=app_names, icon=ic_youtube, enabled=false) 双入口；无障碍服务使用第三方品牌包名 com.viber.voip 冒充；服务配置 android:description 为空不解释用途；全部字符串AES加密常量；类名语义化随机化混淆（monogenesymethanating、pancreatopathyregauge）；未发现同形字或伪造isAccessibilityTool。 |
| 无障碍服务类名 | `com.viber.voip.InputService` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `CALL_PHONE, QUERY_ALL_PACKAGES, READ_CONTACTS, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, SYSTEM_ALERT_WINDOW` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | activity-alias com.snaperfect.inframe1.Android → com.snaperfect.inframe1.monogenesymethanating | 用户点击桌面图标（ACTION_MAIN/LAUNCHER）触发 onCreate | 原生Activity | **原文**：无（本步无界面文案，直接执行判定）<br>**译注**：无可见界面，静默判定 | 仅点击图标启动，无取消/跳过入口 | `com.snaperfect.inframe1.monogenesymethanating#onCreate` |
| 2 | 业务功能触发 | monogenesymethanating.onCreate 内条件判定 c638ee9c(context) / c49756ec() / 语言白名单 becc1b | onCreate 同步执行：语言不在白名单则 finish()；c49756ec() 为真直接 return；c638ee9c 判定无障碍未开启 | 不可静态还原 | 无 | 无（静默过滤，用户无感知） | `com.snaperfect.inframe1.monogenesymethanating#onCreate` |
| 3 | 跳无障碍设置 | 品牌定向 Intent：MIUI com.android.settings.accessibility.MiuiAccessibilitySettingsActivity / 三星 com.samsung.accessibility.installed_service / 回退 android.settings.ACCESSIBILITY_SETTINGS | onCreate 中 ce10b6ac() 返回 5 或 4 时按机型构造 Intent，resolveActivity 为空则回退通用 Action，随后 startActivity | 系统无障碍页 | **原文**：android.settings.ACCESSIBILITY_SETTINGS / :settings:fragment_args_key / :settings:show_fragment_args<br>**译注**：直接打开系统「无障碍」设置页（按小米/三星定制页优先） | 要求用户在系统页中自行开启服务；无应用侧取消按钮 | `com.snaperfect.inframe1.monogenesymethanating#onCreate` |
| 4 | 遮罩叠层指引 | Intent extra 预定位：fragment_args_key = 包名 + "/" + com.viber.voip.InputService.class.getName() | startActivity 前 putExtra 写入 fragment_args_key 与 show_fragment_args Bundle | 系统无障碍页 | **原文**：com.snaperfect.inframe1/com.viber.voip.InputService<br>**译注**：系统无障碍列表自动滚动并高亮到伪装为 Viber 的服务项，减少用户辨识成本 | 用户只需在已定位的服务项上点开启开关 | `com.snaperfect.inframe1.monogenesymethanating#onCreate` |
| 5 | 拒权反馈循环 | 下次冷启动重新执行 c638ee9c 判定并再次 startActivity(ACCESSIBILITY_SETTINGS) | 用户从设置页返回或直接杀进程后再次点图标启动 | 系统无障碍页 | **原文**：无（无任何拒绝说明或降级提示）<br>**译注**：未授权即每次启动重复跳转系统设置，无降级路径 | 无跳过选项，只能授权或退出应用 | `com.snaperfect.inframe1.monogenesymethanating#onCreate` |
| 6 | 获权后动作 | startActivity(com.snaperfect.inframe1.Activitys.calamaroidblennometritis, START=false) + startForegroundService(faithkeepingmistfall / linenshyperlogicality) | onCreate 内无条件执行（与是否授权并行） | 原生Activity + 前台服务 | **原文**：START<br>**译注**：拉起主业务页并常驻前台服务，无障碍开启后即具备点击注入能力（click/input/back/home/recents/scroll） | 无 | `com.snaperfect.inframe1.monogenesymethanating#onCreate` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- 冷启动跳转由 monogenesymethanating.onCreate 静默执行，无应用侧引导弹窗——说明文字主要落在系统无障碍设置页上
- 系统无障碍服务列表项标签：@string/app_name（伪装 Viber），android:description 为空，未向用户解释用途
- Intent extra :settings:fragment_args_key / :settings:show_fragment_args 将系统列表预定位到 com.snaperfect.inframe1/com.viber.voip.InputService
- 多语言提示串（[en]Enable accessibility for protection to take effect 等）为已解密字符串常量，供后续引导/悬浮提示界面复用
- 土耳其语条目 [tr]Mp3 indirebilmek için Erişebilirlik iznini veriniz. 与保护/更新语境不符，属模板复用

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| en | Enable accessibility for protection to take effect | 开启无障碍，保护功能才会生效 | `com.stringmanager.Change.decipher 解密的硬编码 hex 常量（多语言串 [en]...[tr]）` | 假反诈安全 |
| en | Please activate for updates to be active | 请激活，以便更新功能生效 | `com.stringmanager.Change.decipher 解密的硬编码 hex 常量（多语言串 [en]...[tr]）` | 假更新 |
| en | Allow | 允许 | `解密字符串 '[en]Allow::[es]Permitir::[ca]PERMET::[de]Zulassen::[fr]Autoriser::[it]Consenti::[ko]허용::[pl]Zezwól::[ja]許可::[tr]İZİN VER::'` | 受限设置分步教学 |
| en | Settings | 设置 | `解密字符串 '[en]Settings::[es]Ajustes::[ca]Configuració::[de]Einstellungen::[fr]Paramètres::[it]Impostazioni::[ko]설정::[pl]Ustawienia::[ja]設定::[tr]Ayarlar::'` | 受限设置分步教学 |
| tr | Mp3 indirebilmek için Erişebilirlik iznini veriniz. | 请授予无障碍权限以下载 Mp3。 | `同两条多语言串的 [tr] 分节（与 en/de/fr 语境冲突）` | 未知 |
| en | to remove | 卸载 | `解密字符串 '[en]to remove::[es]eliminar::[it]disinstallare questa::[pl]Odinstalować tę::[tr]Durmaya zorla::'` | 清理工具伪装 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：未授权时每次冷启动都重新执行 c638ee9c 判定并再次 startActivity 跳系统无障碍设置；无任何拒绝说明或降级提示。已确认的是冷启动重跳，未见 onResume/Timer 定时死循环的静态证据。
- **遮罩叠层 / 高仿系统设置页**：未发现伪造系统无障碍开关页或半透明引导遮罩；但申请 SYSTEM_ALERT_WINDOW 且持久化 SizeX/SizeY（70% 屏宽/高），具备悬浮窗叠层能力。
- **Android 13+ 受限设置（Restricted Settings）应对**：无（targetSdk 31，未发现应用详情右上角受限设置分步教学，也未发现 Session 安装器绕过）
- **获权后即时行为与防撤权机制**：未发现获权后自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但解密串中存在 protect_allow、uninstall1、uninstall2、uninstall_huawei、uninstall1_pixel11 等反卸载相关键名，本次未展开核实。
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：冷启动 activity-alias com.snaperfect.inframe1.Android 后、monogenesymethanating.onCreate 执行 startActivity 跳 android.settings.ACCESSIBILITY_SETTINGS（或 MIUI/三星定制页）的瞬间拉起 UTG；亦可监控无障碍服务 com.viber.voip.InputService 被系统绑定的瞬间。
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`False`
- **纯 UTG 方案盲区/边界提示**：应用无壳，字符串 AES 加密但静态可还原，不构成 UTG 盲区；主要盲区是承载引导文案的具体弹窗 Activity 需动态触发才可见（受语言白名单 becc1b、c49756ec 环境门控影响，非白名单语种/环境会静默 finish，UTG 可能看不到任何界面）；远端 C2 下发的后续话术未取回。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **系统无障碍服务列表项（跳转落地页）** | com.android.settings 无障碍页，列表自动滚动/高亮至 'com.snaperfect.inframe1/com.viber.voip.InputService' | 直接证明应用把用户导航到伪装成 Viber 的服务开关，是诱导最关键的落点 | 列表项标签与桌面应用名一致、无用途说明；fragment_args_key 导致的自动定位/高亮行为；当前前台包名为 com.android.settings 而启动来源为 com.snaperfect.inframe1 |
| **冷启动首个应用界面** | monogenesymethanating 承载页或 calamaroidblennometritis 业务页 | 确认是否存在应用侧引导弹窗、是否有可关闭/跳过按钮 | 是否有 Cancel/Skip 控件；从设置页返回后是否立刻再次跳转；界面文案是否与'保护/更新'话术一致 |
| **跳转前后品牌/身份呈现** | 桌面图标标签、近期任务卡、无障碍服务项标签三者对比 | 暴露 Viber 冒充与多 activity-alias 身份不一致 | 无障碍服务项显示名与真实 Viber 应用是否并存；是否存在第二个 Youtube 别名入口 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.snaperfect.inframe1.monogenesymethanating#onCreate`
- `com.stringmanager.Change#decipher`
- `com.stringmanager.Change#isOk`
- `AndroidManifest.xml service com.viber.voip.InputService (meta-data @xml/serviceconfig)`
- `AndroidManifest.xml activity-alias com.snaperfect.inframe1.Android / com.snaperfect.inframe1.Youtube`
- `com.snaperfect.inframe1.Littrowblastogenic$ListViewListener#onMessage`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（GodFather 家族，`com.snaperfect.inframe1`）

**可见性**：应用没有使用加壳或 VMP；但所有界面文案都被 `com.stringmanager.Change` 以 AES/ECB 加密成十六进制常量（密钥 `PBKDF2WithHmacSHA1("a","a",8,256)`），我已经在离线环境下完整还原了相关字符串表，因此无障碍诱导逻辑是**静态可见**的。

**逐步流程（纯运行期）**

1. **冷启动入口**：桌面图标由 `activity-alias com.snaperfect.inframe1.Android`（label=`@string/app_name`）指向 `monogenesymethanating`；同时另设 `com.snaperfect.inframe1.Youtube` 别名（label=`@string/app_names`、icon=`@drawable/ic_youtube`、`enabled=false`），用于更换应用身份。
2. **语言/环境过滤**：`onCreate` 先用 `becc1b` 语言白名单过滤，不匹配就直接 `finish()`；`c49756ec()` 提前返回；`c638ee9c(context)` 判定无障碍服务未开启时才继续。因此**每次冷启动**未授权都会重走诱导流程。
3. **跳受限设置（品牌定向）**：`ce10b6ac()` 判断机型品牌；`==5` 走 MIUI 专用 Activity，`==4` 走三星专用 Activity（两个 Activity 名由 base64 常量解码，解码后分别是 `com.android.settings.accessibility.MiuiAccessibilitySettingsActivity` 与 `com.samsung.accessibility.installed_service`），若 `resolveActivity` 为空则回退到 `android.settings.ACCESSIBILITY_SETTINGS`。
4. **预选中伪装服务**：Intent 附带 `:settings:fragment_args_key` = `包名 + "/" + com.viber.voip.InputService`，以及 `:settings:show_fragment_args` Bundle——**把系统无障碍列表直接定位并高亮到伪装成 Viber 的服务项**，用户只需点一个开关。
5. **获权前同时拉起业务页**：无条件 `startActivity(calamaroidblennometritis, START=false)`，并 `startForegroundService(faithkeepingmistfall / linenshyperlogicality)`，即"先跳设置、同时起常驻服务"。
6. **文案框架**：多语言字符串以"开启无障碍才能让**保护**生效""请激活以便**更新**生效"为由（实际是远控/RAT 所需的点击注入能力），按钮文案为 `Allow` / `Settings`。土耳其语条目翻译为"授予无障碍权限以下载 Mp3"，说明模板被复用，可信度低。

**关键事实**
- 无障碍服务类名为 [com.viber.voip.InputService](<resource-unit:#1 manifest:components>)，`android:label=@string/app_name`，冒充 Viber；配套申请 `CALL_PHONE / READ_CONTACTS / READ_PHONE_NUMBERS` 使这一伪装身份自洽。
- 服务能力为 `click(x,y)` / `input(x,y,text)` / `backed/homex/recents/scroll*`（见 [Littrowblastogenic$ListViewListener.onMessage](<resource-unit:#1.dex1 code:com.snaperfect.inframe1.Littrowblastogenic$ListViewListener#onMessage>)），即远控点击注入，与"保护/更新"的说明完全不符。
- 未见"受限设置（Android 13）分步教学"、也未见伪造系统无障碍开关页的证据；未发现 `GLOBAL_ACTION_BACK` 撤权对抗，但存在 `protect_allow`、`uninstall_huawei` 等反卸载字符串（本次未展开）。

**边界**：①具体承载"开启无障碍"弹窗的 Activity 未逐一反编译确认（`anticulariamossinwoven`、`calamaroidblennometritis` 均为候选）；②远端 C2 下发的 HTML/配置未取回；③因工具调用已达 14 次上限，本轮未写入风险台账。

```json
{
  "static_visibility": "clear",
  "visibility_note": "无壳无VMP；全部界面文案由 com.stringmanager.Change 以 AES/ECB(PBKDF2WithHmacSHA1(a,a,8,256)) 加密为 hex 常量，已离线静态还原433条明文，引导逻辑与跳转目标完全可读。残留缺口：承载引导弹窗的具体 Activity 未逐一反编译、远端C2下发HTML/配置未取回。",
  "summary_one_liner": "冷启动即在语言/环境过滤后直接 startActivity 跳转系统无障碍设置，并用 fragment_args_key 把列表预定位到伪装成 com.viber.voip.InputService 的服务项，以'保护/更新生效'名义要求用户开启点击注入型无障碍。",
  "disguise_identity": {
    "app_display_name": "@string/app_name（activity-alias com.snaperfect.inframe1.Android）",
    "claimed_brand_or_persona": "Viber（无障碍服务包名与类名伪装为 com.viber.voip.InputService）",
    "a11y_service_label": "@string/app_name（与桌面名一致，冒充 Viber 显示名）",
    "identity_mismatch": true,
    "obfuscation_tricks": "多activity-alias伪装：Android(label=app_name) 与 Youtube(label=app_names, icon=ic_youtube, enabled=false) 双入口；无障碍服务使用第三方品牌包名 com.viber.voip 冒充；服务配置 android:description 为空不解释用途；全部字符串AES加密常量；类名语义化随机化混淆（monogenesymethanating、pancreatopathyregauge）；未发现同形字或伪造isAccessibilityTool。"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "activity-alias com.snaperfect.inframe1.Android → com.snaperfect.inframe1.monogenesymethanating",
      "trigger_event": "用户点击桌面图标（ACTION_MAIN/LAUNCHER）触发 onCreate",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（本步无界面文案，直接执行判定）",
      "shown_text_zh": "无可见界面，静默判定",
      "user_action_requested": "仅点击图标启动，无取消/跳过入口",
      "code_anchor": "com.snaperfect.inframe1.monogenesymethanating#onCreate"
    },
    {
      "step": 2,
      "stage": "业务功能触发",
      "screen_or_component": "monogenesymethanating.onCreate 内条件判定 c638ee9c(context) / c49756ec() / 语言白名单 becc1b",
      "trigger_event": "onCreate 同步执行：语言不在白名单则 finish()；c49756ec() 为真直接 return；c638ee9c 判定无障碍未开启",
      "ui_carrier": "不可静态还原",
      "shown_text_verbatim": "无",
      "shown_text_zh": "语言/环境门控，不匹配即静默退出，不展示任何说明",
      "user_action_requested": "无（静默过滤，用户无感知）",
      "code_anchor": "com.snaperfect.inframe1.monogenesymethanating#onCreate"
    },
    {
      "step": 3,
      "stage": "跳无障碍设置",
      "screen_or_component": "品牌定向 Intent：MIUI com.android.settings.accessibility.MiuiAccessibilitySettingsActivity / 三星 com.samsung.accessibility.installed_service / 回退 android.settings.ACCESSIBILITY_SETTINGS",
      "trigger_event": "onCreate 中 ce10b6ac() 返回 5 或 4 时按机型构造 Intent，resolveActivity 为空则回退通用 Action，随后 startActivity",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "android.settings.ACCESSIBILITY_SETTINGS / :settings:fragment_args_key / :settings:show_fragment_args",
      "shown_text_zh": "直接打开系统「无障碍」设置页（按小米/三星定制页优先）",
      "user_action_requested": "要求用户在系统页中自行开启服务；无应用侧取消按钮",
      "code_anchor": "com.snaperfect.inframe1.monogenesymethanating#onCreate"
    },
    {
      "step": 4,
      "stage": "遮罩叠层指引",
      "screen_or_component": "Intent extra 预定位：fragment_args_key = 包名 + \"/\" + com.viber.voip.InputService.class.getName()",
      "trigger_event": "startActivity 前 putExtra 写入 fragment_args_key 与 show_fragment_args Bundle",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "com.snaperfect.inframe1/com.viber.voip.InputService",
      "shown_text_zh": "系统无障碍列表自动滚动并高亮到伪装为 Viber 的服务项，减少用户辨识成本",
      "user_action_requested": "用户只需在已定位的服务项上点开启开关",
      "code_anchor": "com.snaperfect.inframe1.monogenesymethanating#onCreate"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "下次冷启动重新执行 c638ee9c 判定并再次 startActivity(ACCESSIBILITY_SETTINGS)",
      "trigger_event": "用户从设置页返回或直接杀进程后再次点图标启动",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "无（无任何拒绝说明或降级提示）",
      "shown_text_zh": "未授权即每次启动重复跳转系统设置，无降级路径",
      "user_action_requested": "无跳过选项，只能授权或退出应用",
      "code_anchor": "com.snaperfect.inframe1.monogenesymethanating#onCreate"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "startActivity(com.snaperfect.inframe1.Activitys.calamaroidblennometritis, START=false) + startForegroundService(faithkeepingmistfall / linenshyperlogicality)",
      "trigger_event": "onCreate 内无条件执行（与是否授权并行）",
      "ui_carrier": "原生Activity + 前台服务",
      "shown_text_verbatim": "START",
      "shown_text_zh": "拉起主业务页并常驻前台服务，无障碍开启后即具备点击注入能力（click/input/back/home/recents/scroll）",
      "user_action_requested": "无",
      "code_anchor": "com.snaperfect.inframe1.monogenesymethanating#onCreate"
    }
  ],
  "text_presentation_locations": [
    "冷启动跳转由 monogenesymethanating.onCreate 静默执行，无应用侧引导弹窗——说明文字主要落在系统无障碍设置页上",
    "系统无障碍服务列表项标签：@string/app_name（伪装 Viber），android:description 为空，未向用户解释用途",
    "Intent extra :settings:fragment_args_key / :settings:show_fragment_args 将系统列表预定位到 com.snaperfect.inframe1/com.viber.voip.InputService",
    "多语言提示串（[en]Enable accessibility for protection to take effect 等）为已解密字符串常量，供后续引导/悬浮提示界面复用",
    "土耳其语条目 [tr]Mp3 indirebilmek için Erişebilirlik iznini veriniz. 与保护/更新语境不符，属模板复用"
  ],
  "verbatim_texts": [
    {
      "lang": "en",
      "text_verbatim": "Enable accessibility for protection to take effect",
      "text_zh": "开启无障碍，保护功能才会生效",
      "source_location": "com.stringmanager.Change.decipher 解密的硬编码 hex 常量（多语言串 [en]...[tr]）",
      "rhetorical_frame": "假反诈安全"
    },
    {
      "lang": "en",
      "text_verbatim": "Please activate for updates to be active",
      "text_zh": "请激活，以便更新功能生效",
      "source_location": "com.stringmanager.Change.decipher 解密的硬编码 hex 常量（多语言串 [en]...[tr]）",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "en",
      "text_verbatim": "Allow",
      "text_zh": "允许",
      "source_location": "解密字符串 '[en]Allow::[es]Permitir::[ca]PERMET::[de]Zulassen::[fr]Autoriser::[it]Consenti::[ko]허용::[pl]Zezwól::[ja]許可::[tr]İZİN VER::'",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "en",
      "text_verbatim": "Settings",
      "text_zh": "设置",
      "source_location": "解密字符串 '[en]Settings::[es]Ajustes::[ca]Configuració::[de]Einstellungen::[fr]Paramètres::[it]Impostazioni::[ko]설정::[pl]Ustawienia::[ja]設定::[tr]Ayarlar::'",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Mp3 indirebilmek için Erişebilirlik iznini veriniz.",
      "text_zh": "请授予无障碍权限以下载 Mp3。",
      "source_location": "同两条多语言串的 [tr] 分节（与 en/de/fr 语境冲突）",
      "rhetorical_frame": "未知"
    },
    {
      "lang": "en",
      "text_verbatim": "to remove",
      "text_zh": "卸载",
      "source_location": "解密字符串 '[en]to remove::[es]eliminar::[it]disinstallare questa::[pl]Odinstalować tę::[tr]Durmaya zorla::'",
      "rhetorical_frame": "清理工具伪装"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "未授权时每次冷启动都重新执行 c638ee9c 判定并再次 startActivity 跳系统无障碍设置；无任何拒绝说明或降级提示。已确认的是冷启动重跳，未见 onResume/Timer 定时死循环的静态证据。",
    "overlay_or_fake_settings": "未发现伪造系统无障碍开关页或半透明引导遮罩；但申请 SYSTEM_ALERT_WINDOW 且持久化 SizeX/SizeY（70% 屏宽/高），具备悬浮窗叠层能力。",
    "restricted_settings_13plus_coaching": "无（targetSdk 31，未发现应用详情右上角受限设置分步教学，也未发现 Session 安装器绕过）",
    "post_grant_anti_removal": "未发现获权后自点确认或 GLOBAL_ACTION_BACK/HOME 阻止撤权；但解密串中存在 protect_allow、uninstall1、uninstall2、uninstall_huawei、uninstall1_pixel11 等反卸载相关键名，本次未展开核实。",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "冷启动 activity-alias com.snaperfect.inframe1.Android 后、monogenesymethanating.onCreate 执行 startActivity 跳 android.settings.ACCESSIBILITY_SETTINGS（或 MIUI/三星定制页）的瞬间拉起 UTG；亦可监控无障碍服务 com.viber.voip.InputService 被系统绑定的瞬间。",
    "key_pages_to_capture": [
      {
        "page_role": "系统无障碍服务列表项（跳转落地页）",
        "page_identifier": "com.android.settings 无障碍页，列表自动滚动/高亮至 'com.snaperfect.inframe1/com.viber.voip.InputService'",
        "why_most_useful": "直接证明应用把用户导航到伪装成 Viber 的服务开关，是诱导最关键的落点",
        "observable_utg_signals": [
          "列表项标签与桌面应用名一致、无用途说明",
          "fragment_args_key 导致的自动定位/高亮行为",
          "当前前台包名为 com.android.settings 而启动来源为 com.snaperfect.inframe1"
        ]
      },
      {
        "page_role": "冷启动首个应用界面",
        "page_identifier": "monogenesymethanating 承载页或 calamaroidblennometritis 业务页",
        "why_most_useful": "确认是否存在应用侧引导弹窗、是否有可关闭/跳过按钮",
        "observable_utg_signals": [
          "是否有 Cancel/Skip 控件",
          "从设置页返回后是否立刻再次跳转",
          "界面文案是否与'保护/更新'话术一致"
        ]
      },
      {
        "page_role": "跳转前后品牌/身份呈现",
        "page_identifier": "桌面图标标签、近期任务卡、无障碍服务项标签三者对比",
        "why_most_useful": "暴露 Viber 冒充与多 activity-alias 身份不一致",
        "observable_utg_signals": [
          "无障碍服务项显示名与真实 Viber 应用是否并存",
          "是否存在第二个 Youtube 别名入口"
        ]
      }
    ],
    "needs_ocr_for_image_lure": false,
    "detection_blindspot_note": "应用无壳，字符串 AES 加密但静态可还原，不构成 UTG 盲区；主要盲区是承载引导文案的具体弹窗 Activity 需动态触发才可见（受语言白名单 becc1b、c49756ec 环境门控影响，非白名单语种/环境会静默 finish，UTG 可能看不到任何界面）；远端 C2 下发的后续话术未取回。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_SYSTEM_A11Y_DESCRIPTION",
    "LURE_FAKE_UPDATE_OR_INSTALL",
    "LURE_FAKE_SECURITY_ANTIFRAUD",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_SYSTEM_OR_BRAND_IMPERSONATION",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.snaperfect.inframe1.monogenesymethanating#onCreate",
    "com.stringmanager.Change#decipher",
    "com.stringmanager.Change#isOk",
    "AndroidManifest.xml service com.viber.voip.InputService (meta-data @xml/serviceconfig)",
    "AndroidManifest.xml activity-alias com.snaperfect.inframe1.Android / com.snaperfect.inframe1.Youtube",
    "com.snaperfect.inframe1.Littrowblastogenic$ListViewListener#onMessage"
  ]
}
```

</details>
