# MB_110__a0610f08c7｜BankBot — M​ü​z​i​k

> **类型**：在野恶意无障碍样本  ｜  **来源池**：`MalwareBazaar_2022_2026`  ｜  **静态可见性**：`partial_dynamic_or_remote`  ｜  **APKAudit 耗时**：167.6s

## 1. 一句话核心结论

- **核心申请方式**：伪装成音乐应用 Müzik 的 BankBot 样本，冷启动即以原生引导页（拦截返回键、GIF 演示、仅一个“允许”按钮）把用户送入 ACCESSIBILITY_SETTINGS 并定位到自身无障碍服务项，拒权则提示后直接退出、下次启动重复，获权后拉起前台服务与远端钓鱼 WebView。
- **静态可见性说明**：DEX 未加壳，全部引导文案经本地 Blowfish(key=aa87e0aa39)+Base64 双层编码，已静态还原；远端仅涉 GIF 教学图 https://s11.gifyu.com/images/SW9m9.gif 与获权后 WebView 页面 http://<prefs.min>/rx/f.php?f=&p=&tr=（页面内容不在包内，未还原）
- **命中的行为模式标签**：`TRIG_COLD_START_BLOCK`（冷启动0步强阻断直弹授权）、`CARRIER_NATIVE_DIALOG_OR_ACTIVITY`（原生弹窗(Dialog)或原生引导页(Activity)）、`CARRIER_GIF_OR_IMAGE_GUIDE`（纯图片/GIF动画分步操作指引）、`CARRIER_WEBVIEW_REMOTE_URL`（远端下发HTML/WebView动态引导页）、`COERCE_NO_SKIP_NON_CANCELABLE`（不可取消弹窗/无跳过出口/单一正向按钮）、`COERCE_REFUSAL_LOOP_RELAUNCH`（拒权或返回后死循环重拉无障碍设置页）、`ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH`（空白符/大量换行挤出警告/零宽或同形字隐身）、`ID_MULTI_ALIAS_CAMOUFLAGE`（多activity-alias动态切换图标与伪装身份）

## 2. 应用标识、静态能力与身份署名核验

| 维度 | 实测详情 |
| --- | --- |
| 样本 SHA-256 | `a0610f08c783ff5486a66022fedf483e1ac81dfe48935680b5d9d29b309338c5` |
| 包名 / 年份 | `com.quadrigeminate.hydrocatalysis` / 2026 |
| 家族 / 品类 | **BankBot**（同池样本数：8） |
| 原始来源标识 | MalwareBazaar_2022_2026 |
| 桌面显示名 | M​ü​z​i​k（含 U+200B 零宽空格） |
| 引导页宣称品牌/身份 | Müzik 音乐播放器；引导文案中自称/宣称“Tözir 下载功能”；备用启动别名伪装为 Play Store |
| 系统无障碍列表服务名 | M​ü​z​i​k（@string/app_name，含零宽空格，无 android:description） |
| 三方身份是否错配/伪装 | **是（存在伪装/错配）** ｜ 混淆手法：1) app_name/appname 中插入 U+200B 零宽空格规避字符串比对（M\u200bü\u200bz\u200bi\u200bk、P\u200bl\u200ba\u200by S\u200bt\u200bo\u200br\u200be）；2) 多 activity-alias 伪装：Google→hypochondriasis（启用，LAUNCHER），Youtube（label=Play Store、icon=launcr、enabled=false）→mohel；3) 全部敏感字符串 Blowfish ECB 加密 + 二次 Base64（pleuralgic.n / touzling.homoeoplasy）；4) 无障碍服务未配置 android:description，系统列表无任何用途说明；5) 未使用伪造 isAccessibilityTool |
| 无障碍服务类名 | `com.quadrigeminate.hydrocatalysis.panomphaic` |
| 静态能力位 | `canRetrieveWindowContent=True` · `canPerformGestures=True` · `isAccessibilityTool=False` · 监听范围：全局通配（未限定 packageNames） |
| 共现高危权限 | `QUERY_ALL_PACKAGES, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |

## 3. 一步步引导用户申请/开启无障碍流程（Pre-Grant UTG 全链路）

| 步骤 | 阶段 | 页面 / 组件 | 触发事件 | UI 载体 | 界面呈现原文与译文 | 要求用户执行的动作 | 代码/资源锚点 |
| :---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 冷启动入口 | activity-alias com.quadrigeminate.hydrocatalysis.Google → com.quadrigeminate.hydrocatalysis.hypochondriasis（桌面图标 Müzik） | 用户点击桌面图标；hypochondriasis.onCreate → onResume | 原生Activity | **原文**：无（onCreate 仅 setContentView(R.layout.partycolored)，无引导文案）<br>**译注**：冷启动空白/普通界面，无说明 | 无交互；若 SharedPreferences app/accs 含 "true" 则弹提示并 finish，否则进入权限/引导流程 | `com.quadrigeminate.hydrocatalysis.hypochondriasis#onCreate / #onResume` |
| 2 | 冷启动入口 | Android 13+ 通知权限系统弹窗（requestCode 112） | hypochondriasis.onResume 中 SDK_INT>=33 且 shouldShowRequestPermissionRationale 为假时调用 oratoric() | 原生Dialog | **原文**：无（系统弹窗文案，权限 android.permission.POST_NOTIFICATIONS）<br>**译注**：系统通知权限申请，为后续常驻前台服务/通知做铺垫 | 允许/拒绝均可；无论结果都会继续进入 Readstown() 引导流程 | `com.quadrigeminate.hydrocatalysis.hypochondriasis#oratoric / #onRequestPermissionsResult` |
| 3 | 引导说明页 | com.quadrigeminate.hydrocatalysis.directorial（AppCompatActivity，布局 R.layout.synonymes） | Readstown() 中 accs 不含 "true" 时 startActivity(new Intent(ctx, directorial.class))；directorial.onResume 渲染 | 原生Activity | **原文**：Tözir indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / 按钮：İzin Ver / 演示图：https://s11.gifyu.com/images/SW9m9.gif<br>**译注**：“为使 Tözir 下载功能生效，请授予上方所示的权限。”按钮为“允许”，上方播放一张 GIF 操作演示图 | 只能点击“İzin Ver”卡片（R.id.numerators）；无取消/跳过按钮，返回键被拦截无法退出 | `com.quadrigeminate.hydrocatalysis.directorial#onResume / #onKeyDown` |
| 4 | 跳无障碍设置 | 系统设置：com.samsung.accessibility.installed_service，回退 android.settings.ACCESSIBILITY_SETTINGS（附 :settings:show_fragment_args=包名/com.quadrigeminate.hydrocatalysis.panomphaic） | 用户点击“İzin Ver” → directorial$1.onClick；先 resolveActivity 探测三星无障碍页，失败则回退标准无障碍设置 | 系统无障碍页 | **原文**：Tözir indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)<br>**译注**：跳转瞬间居中 Toast：“为使 Tözir 下载功能生效，请授予无障碍权限。(Müzik)”；随后 directorial.finish()，用户面对系统无障碍列表中无说明的“Müzik”服务项 | 在系统无障碍列表中找到 Müzik 并打开开关（无应用侧确认步骤） | `com.quadrigeminate.hydrocatalysis.directorial$1#onClick` |
| 5 | 拒权反馈循环 | Toast + 应用退出；下次冷启动重复步骤 1-4 | 用户在系统设置返回未开启服务；或通知权限对话框点拒绝（onRequestPermissionsResult requestCode 112 分支） | 通知栏 | **原文**：Gerekli izni vermeden uygulamayı kullanamazsınız.<br>**译注**：“未授予必要权限，你无法使用本应用。”随后 finish() 关闭应用；重新打开仍回到同一引导页，形成重复索取 | 无降级路径，只能再次进入引导页并去开权限 | `com.quadrigeminate.hydrocatalysis.hypochondriasis#onRequestPermissionsResult / #Readstown` |
| 6 | 获权后动作 | triennially 前台服务 + unjewelled Activity（内建 WebView） | 无障碍服务开启后 SharedPreferences app/accs 被置为 "true"，hypochondriasis.onResume 检测到后 finish()；triennially 前台服务启动，fiscality 等定时任务运行；unjewelled.onStart 加载远端页面 | 远端WebView | **原文**：wv.loadUrl(<prefs.min> + "rx/f.php?f=" + str + "&p=" + <prefs.ky> + "&tr=")（页面内容由远端下发，本地不可见）<br>**译注**：加载远端钓鱼/叠加页面（BankBot 典型 rx/f.php 注入页），内容动态下发 | 无（后台自动化） | `com.quadrigeminate.hydrocatalysis.unjewelled#onStart / com.quadrigeminate.hydrocatalysis.triennially#Untuscan` |

## 4. 引导文字呈现位置与逐字原文摘录

### 4.1 呈现位置清单（Where Text Appears）
- directorial 引导页 R.layout.synonymes 的 TextView（R.id.sorrowbreathing 等）：正文“Tözir indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz.”与按钮“İzin Ver”，运行时由 touzling.homoeoplasy(pleuralgic.n(...)) 解码写入
- directorial 引导页 ImageView(R.id.Phytomonas)：Glide 加载远端 GIF https://s11.gifyu.com/images/SW9m9.gif 作为操作演示图
- 点击“İzin Ver”后跳转系统设置瞬间的屏幕中央 Toast：“Tözir indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)”
- 拒权/返回后的 Toast：“Gerekli izni vermeden uygulamayı kullanamazsınız.”
- 系统无障碍服务列表项：label=@string/app_name（Müzik，零宽空格），android:description 缺失（res/xml/preferences.xml 无 description 属性），系统侧无任何用途说明
- 获权后 unjewelled 的远端 WebView 页面（rx/f.php）——内容由服务器下发，非本地 HTML

### 4.2 逐字原文与话术框架（Verbatim Texts）
| 语种 | 逐字原文 | 中文翻译 | 源码/资源位置 | 话术/修辞框架 |
| :---: | --- | --- | --- | --- |
| tr | Tözir indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. | 为使 Tözir 下载功能生效，请授予上方所示的权限。 | `硬编码密文 QzAFoPyJY/jd4/3V77jOsm0ILwE4...（Blowfish+Base64），解密后由 directorial.onResume 写入 bowfin TextView` | 假更新 |
| tr | İzin Ver | 允许 | `密文 X+DjijdE90aJGyKrBya46g==，directorial.onResume 写入 bulten TextView` | 受限设置分步教学 |
| tr | Tözir indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik) | 为使 Tözir 下载功能生效，请授予无障碍权限。（Müzik） | `密文 QzAFoPyJY/jd4/3V77jOsm0ILwE4...s8m3e6Sh3Ai8...，directorial$1.onClick 中 Toast 显示` | 假更新 |
| tr | Gerekli izni vermeden uygulamayı kullanamazsınız. | 未授予必要权限，你无法使用本应用。 | `密文 Q5B9w06w+F69fIn7XARt+5fEv/beEofP...，hypochondriasis.onRequestPermissionsResult 中 Toast 显示` | 故障恐吓 |
| tr | Tözfeln daha sonra deneyiniz. | 请稍后再试。 | `密文 ckddoEX0WrBSXX3MabJLdY1JjOknMIbwdzq59BerIiCkMICPE5olwg==，hypochondriasis.onResume / Readstown 中 Toast 显示` | 故障恐吓 |

## 5. 让用户完成开启的具体机制与拒权反馈

- **触发时机（Trigger Timing）**：`cold_start_0_step`
- **是否提供取消/跳过出口**：`False`
- **拒权或返回后的反馈回路**：引导页返回键被 onKeyDown(keyCode==4) 直接吞掉；拒权/返回后 Toast“Gerekli izni vermeden uygulamayı kullanamazsınız.”并 finish()，应用下次冷启动仍按 accs!=true 重跳 directorial 引导页，形成重复索取（无定时器强制拉起）
- **遮罩叠层 / 高仿系统设置页**：无半透明遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅用 GIF 演示图 + Toast 指引，并直接把用户送入真实系统设置页且用 :settings:show_fragment_args 预定位到自身服务项
- **Android 13+ 受限设置（Restricted Settings）应对**：无
- **获权后即时行为与防撤权机制**：无
- **良性降级 / 替代方案**：无

## 6. 面向纯 UTG 检测机制的关键捕获页面与判别信号

- **推荐检测拉起时机（Trigger Hook）**：在检测到 startActivity 跳转 android.settings.ACCESSIBILITY_SETTINGS（或 com.samsung.accessibility.installed_service）且 Intent 携带 :settings:show_fragment_args 含本应用无障碍服务类名的瞬间拉起 UTG；或在 directorial（引导页）首次 onResume 后 800ms 抓取
- **是否需对纯图/GIF 引导页触发按需单帧 OCR**：`True`
- **纯 UTG 方案盲区/边界提示**：GIF 教学图与获权后 WebView 页面内容均由远端下发（gifyu.com 图片、rx/f.php），若断网或服务器下线则这两处不可见；另需注意引导文案全部为本地加密字符串，静态文本检索（如搜 ACCESSIBILITY_SETTINGS）会漏检，运行期 UTG 不受影响。

| 关键捕获页面角色 | 预期页面/组件标识 | 为何捕获该页面最有用 | 可在 UTG 直接提取的判别信号 |
| --- | --- | --- | --- |
| **冷启动引导说明页** | com.quadrigeminate.hydrocatalysis.directorial，布局 R.layout.synonymes，含 TextView 正文与单个“İzin Ver”卡片，无返回/跳过入口 | 这是唯一的说明性界面，能同时确认伪装话术、GIF 教学图和“无取消按钮”的强制结构 | 节点文本 Tözir indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz.；按钮文本 İzin Ver；节点树中不存在“跳过/取消/Iptal”类可点击文本；ImageView 中 GIF 帧（gifyu.com 远端图） |
| **跳转前 Toast 提示** | Toast 文本“Tözir ... erişebilirlik iznini veriniz. (Müzik)” | 直接给出“应用主动索要无障碍权限”的语义证据，且带伪装应用名 | 含 erişebilirlik（无障碍）关键词；括号内应用名 (Müzik) |
| **系统无障碍服务列表项** | Settings 无障碍列表中的“Müzik”条目（label 含零宽空格，无 summary/description） | 对比系统展示的服务名与桌面应用名，验证零宽字符伪装与无用途说明的弱告知 | 服务项文本含 U+200B；该条目无描述文本（summary 为空）；包名 com.quadrigeminate.hydrocatalysis |
| **拒权返回后的提示与退出** | Toast“Gerekli izni vermeden uygulamayı kullanamazsınız.”后应用界面消失 | 证明无降级路径与重复索取行为（再次冷启动回到引导页） | Toast 文本含 Gerekli izni vermeden；随后当前 Activity finish（界面消失/回到桌面）；再次启动仍出现同一引导页 |

## 7. 代码锚点与 APKAudit 原始完整逆向纪要

- `com.quadrigeminate.hydrocatalysis.hypochondriasis#onResume`
- `com.quadrigeminate.hydrocatalysis.hypochondriasis#Readstown`
- `com.quadrigeminate.hydrocatalysis.directorial#onResume`
- `com.quadrigeminate.hydrocatalysis.directorial$1#onClick`
- `com.quadrigeminate.hydrocatalysis.directorial#onKeyDown`
- `res/xml/preferences.xml`

<details>
<summary>点击展开 APKAudit CLI 原始完整审计输出</summary>

## 分析结论（定向核验）

**整条引导链完全可见，可以静态还原**：应用没有加壳；敏感字符串用本地 Blowfish（key `aa87e0aa39`）+ Base64 双层编码，已经还原；远端只用于 GIF 教学图和获权后的 WebView 页面。

**逐步流程（纯运行期）**

1. **冷启动入口**：LAUNCHER 由 `activity-alias ...Google` 指向 [hypochondriasis](<resource-unit:#1.dex1 code:com.quadrigeminate.hydrocatalysis.hypochondriasis>)（显示名 `Müzik`，含零宽空格）。`onCreate` 只调用 `setContentView(R.layout.partycolored)`，`onResume` 先检查 SharedPreferences `app/accs` 是否含 `true`：若已授权，就弹 Toast 并 `finish()`；若未授权，Android 13+ 先申请 `POST_NOTIFICATIONS`（requestCode 112），在 `onRequestPermissionsResult` 里无论允许还是拒绝都会进入 `Readstown()`。
2. **引导说明页**：[directorial.onResume()](<resource-unit:#1.dex1 code:com.quadrigeminate.hydrocatalysis.directorial#onResume>) 加载 `R.layout.synonymes`，正文用 `bowfin.setText()` 写入“Tözir indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz.”，按钮 `bulten` 显示“İzin Ver”（允许）；同时用 Glide 把远端 GIF `https://s11.gifyu.com/images/SW9m9.gif` 加载到 `R.id.Phytomonas`，作为操作演示动画。
3. **无法退出的引导页**：[directorial.onKeyDown()](<resource-unit:#1.dex1 code:com.quadrigeminate.hydrocatalysis.directorial#onKeyDown>) 对 `keyCode == 4`（返回键）直接 `return true` 拦截，页面上没有“跳过/取消”控件，只能点击“İzin Ver”。
4. **跳转到无障碍设置**：[directorial$1.onClick()](<resource-unit:#1.dex1 code:com.quadrigeminate.hydrocatalysis.directorial$1#onClick>) 先尝试 Intent `com.samsung.accessibility.installed_service`，解析失败后回退到 `android.settings.ACCESSIBILITY_SETTINGS`，并写入 `:settings:show_fragment_args` = `包名/com.quadrigeminate.hydrocatalysis.panomphaic`，让系统设置直接定位到本应用的服务项；跳转前再用 Toast 提示“Tözir indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)”，然后 `finish()`。
5. **拒权反馈循环**：如果用户返回但未开启服务，下次启动仍会走同一路径（`accs` 不为 `true` 时，`Readstown()` 仍会 `startActivity(directorial)`）；在权限对话框拒绝时，Toast“Gerekli izni vermeden uygulamayı kullanamazsınız.”随后 `finish()`，直接退出应用。这不属于 Android 13 受限设置（受限设置教学），因为没有走应用详情页右侧菜单。
6. **获权后动作**：`accs=true` 后，`hypochondriasis.onResume` 直接 `finish()`；`triennially` 前台服务常驻；`unjewelled.onStart()` 用 `WebView` 加载远端 `http://<prefs.min>/rx/f.php?f=<str>&p=<ky>&tr=`，并开启 JavaScript，进入后续钓鱼/叠加页面。

**身份伪装**：桌面名 `Müzik`（音乐）与无障碍列表标签同为 `Müzik`（零宽空格，用来绕过文本匹配）；第二个别名 `com.quadrigeminate.hydrocatalysis.Youtube` 的 label 是 `Play Store`（同样含零宽空格）、图标 `mipmap/launcr`、`enabled=false`（多别名伪装）。`res/xml/preferences.xml` 只声明 `typeAllMask`/`canRetrieveWindowContent`/`canPerformGestures`，**没有 `android:description`**，也没有伪造 `isAccessibilityTool`——因此在 Android 13 上，系统列表项不会显示任何说明，用户看不到“该服务可以读取屏幕内容”的解释，这本身就是弱告知。

**未发现**：悬浮窗遮罩、高仿系统开关页、定时器强制重新拉起、获权后自点确认或 `GLOBAL_ACTION_BACK` 阻止撤权。

```json
{
  "static_visibility": "partial_dynamic_or_remote",
  "visibility_note": "DEX 未加壳，全部引导文案经本地 Blowfish(key=aa87e0aa39)+Base64 双层编码，已静态还原；远端仅涉 GIF 教学图 https://s11.gifyu.com/images/SW9m9.gif 与获权后 WebView 页面 http://<prefs.min>/rx/f.php?f=&p=&tr=（页面内容不在包内，未还原）",
  "summary_one_liner": "伪装成音乐应用 Müzik 的 BankBot 样本，冷启动即以原生引导页（拦截返回键、GIF 演示、仅一个“允许”按钮）把用户送入 ACCESSIBILITY_SETTINGS 并定位到自身无障碍服务项，拒权则提示后直接退出、下次启动重复，获权后拉起前台服务与远端钓鱼 WebView。",
  "disguise_identity": {
    "app_display_name": "M​ü​z​i​k（含 U+200B 零宽空格）",
    "claimed_brand_or_persona": "Müzik 音乐播放器；引导文案中自称/宣称“Tözir 下载功能”；备用启动别名伪装为 Play Store",
    "a11y_service_label": "M​ü​z​i​k（@string/app_name，含零宽空格，无 android:description）",
    "identity_mismatch": true,
    "obfuscation_tricks": "1) app_name/appname 中插入 U+200B 零宽空格规避字符串比对（M\\u200bü\\u200bz\\u200bi\\u200bk、P\\u200bl\\u200ba\\u200by S\\u200bt\\u200bo\\u200br\\u200be）；2) 多 activity-alias 伪装：Google→hypochondriasis（启用，LAUNCHER），Youtube（label=Play Store、icon=launcr、enabled=false）→mohel；3) 全部敏感字符串 Blowfish ECB 加密 + 二次 Base64（pleuralgic.n / touzling.homoeoplasy）；4) 无障碍服务未配置 android:description，系统列表无任何用途说明；5) 未使用伪造 isAccessibilityTool"
  },
  "step_by_step_flow": [
    {
      "step": 1,
      "stage": "冷启动入口",
      "screen_or_component": "activity-alias com.quadrigeminate.hydrocatalysis.Google → com.quadrigeminate.hydrocatalysis.hypochondriasis（桌面图标 Müzik）",
      "trigger_event": "用户点击桌面图标；hypochondriasis.onCreate → onResume",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "无（onCreate 仅 setContentView(R.layout.partycolored)，无引导文案）",
      "shown_text_zh": "冷启动空白/普通界面，无说明",
      "user_action_requested": "无交互；若 SharedPreferences app/accs 含 \"true\" 则弹提示并 finish，否则进入权限/引导流程",
      "code_anchor": "com.quadrigeminate.hydrocatalysis.hypochondriasis#onCreate / #onResume"
    },
    {
      "step": 2,
      "stage": "冷启动入口",
      "screen_or_component": "Android 13+ 通知权限系统弹窗（requestCode 112）",
      "trigger_event": "hypochondriasis.onResume 中 SDK_INT>=33 且 shouldShowRequestPermissionRationale 为假时调用 oratoric()",
      "ui_carrier": "原生Dialog",
      "shown_text_verbatim": "无（系统弹窗文案，权限 android.permission.POST_NOTIFICATIONS）",
      "shown_text_zh": "系统通知权限申请，为后续常驻前台服务/通知做铺垫",
      "user_action_requested": "允许/拒绝均可；无论结果都会继续进入 Readstown() 引导流程",
      "code_anchor": "com.quadrigeminate.hydrocatalysis.hypochondriasis#oratoric / #onRequestPermissionsResult"
    },
    {
      "step": 3,
      "stage": "引导说明页",
      "screen_or_component": "com.quadrigeminate.hydrocatalysis.directorial（AppCompatActivity，布局 R.layout.synonymes）",
      "trigger_event": "Readstown() 中 accs 不含 \"true\" 时 startActivity(new Intent(ctx, directorial.class))；directorial.onResume 渲染",
      "ui_carrier": "原生Activity",
      "shown_text_verbatim": "Tözir indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz. / 按钮：İzin Ver / 演示图：https://s11.gifyu.com/images/SW9m9.gif",
      "shown_text_zh": "“为使 Tözir 下载功能生效，请授予上方所示的权限。”按钮为“允许”，上方播放一张 GIF 操作演示图",
      "user_action_requested": "只能点击“İzin Ver”卡片（R.id.numerators）；无取消/跳过按钮，返回键被拦截无法退出",
      "code_anchor": "com.quadrigeminate.hydrocatalysis.directorial#onResume / #onKeyDown"
    },
    {
      "step": 4,
      "stage": "跳无障碍设置",
      "screen_or_component": "系统设置：com.samsung.accessibility.installed_service，回退 android.settings.ACCESSIBILITY_SETTINGS（附 :settings:show_fragment_args=包名/com.quadrigeminate.hydrocatalysis.panomphaic）",
      "trigger_event": "用户点击“İzin Ver” → directorial$1.onClick；先 resolveActivity 探测三星无障碍页，失败则回退标准无障碍设置",
      "ui_carrier": "系统无障碍页",
      "shown_text_verbatim": "Tözir indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)",
      "shown_text_zh": "跳转瞬间居中 Toast：“为使 Tözir 下载功能生效，请授予无障碍权限。(Müzik)”；随后 directorial.finish()，用户面对系统无障碍列表中无说明的“Müzik”服务项",
      "user_action_requested": "在系统无障碍列表中找到 Müzik 并打开开关（无应用侧确认步骤）",
      "code_anchor": "com.quadrigeminate.hydrocatalysis.directorial$1#onClick"
    },
    {
      "step": 5,
      "stage": "拒权反馈循环",
      "screen_or_component": "Toast + 应用退出；下次冷启动重复步骤 1-4",
      "trigger_event": "用户在系统设置返回未开启服务；或通知权限对话框点拒绝（onRequestPermissionsResult requestCode 112 分支）",
      "ui_carrier": "通知栏",
      "shown_text_verbatim": "Gerekli izni vermeden uygulamayı kullanamazsınız.",
      "shown_text_zh": "“未授予必要权限，你无法使用本应用。”随后 finish() 关闭应用；重新打开仍回到同一引导页，形成重复索取",
      "user_action_requested": "无降级路径，只能再次进入引导页并去开权限",
      "code_anchor": "com.quadrigeminate.hydrocatalysis.hypochondriasis#onRequestPermissionsResult / #Readstown"
    },
    {
      "step": 6,
      "stage": "获权后动作",
      "screen_or_component": "triennially 前台服务 + unjewelled Activity（内建 WebView）",
      "trigger_event": "无障碍服务开启后 SharedPreferences app/accs 被置为 \"true\"，hypochondriasis.onResume 检测到后 finish()；triennially 前台服务启动，fiscality 等定时任务运行；unjewelled.onStart 加载远端页面",
      "ui_carrier": "远端WebView",
      "shown_text_verbatim": "wv.loadUrl(<prefs.min> + \"rx/f.php?f=\" + str + \"&p=\" + <prefs.ky> + \"&tr=\")（页面内容由远端下发，本地不可见）",
      "shown_text_zh": "加载远端钓鱼/叠加页面（BankBot 典型 rx/f.php 注入页），内容动态下发",
      "user_action_requested": "无（后台自动化）",
      "code_anchor": "com.quadrigeminate.hydrocatalysis.unjewelled#onStart / com.quadrigeminate.hydrocatalysis.triennially#Untuscan"
    }
  ],
  "text_presentation_locations": [
    "directorial 引导页 R.layout.synonymes 的 TextView（R.id.sorrowbreathing 等）：正文“Tözir indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz.”与按钮“İzin Ver”，运行时由 touzling.homoeoplasy(pleuralgic.n(...)) 解码写入",
    "directorial 引导页 ImageView(R.id.Phytomonas)：Glide 加载远端 GIF https://s11.gifyu.com/images/SW9m9.gif 作为操作演示图",
    "点击“İzin Ver”后跳转系统设置瞬间的屏幕中央 Toast：“Tözir indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)”",
    "拒权/返回后的 Toast：“Gerekli izni vermeden uygulamayı kullanamazsınız.”",
    "系统无障碍服务列表项：label=@string/app_name（Müzik，零宽空格），android:description 缺失（res/xml/preferences.xml 无 description 属性），系统侧无任何用途说明",
    "获权后 unjewelled 的远端 WebView 页面（rx/f.php）——内容由服务器下发，非本地 HTML"
  ],
  "verbatim_texts": [
    {
      "lang": "tr",
      "text_verbatim": "Tözir indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz.",
      "text_zh": "为使 Tözir 下载功能生效，请授予上方所示的权限。",
      "source_location": "硬编码密文 QzAFoPyJY/jd4/3V77jOsm0ILwE4...（Blowfish+Base64），解密后由 directorial.onResume 写入 bowfin TextView",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "İzin Ver",
      "text_zh": "允许",
      "source_location": "密文 X+DjijdE90aJGyKrBya46g==，directorial.onResume 写入 bulten TextView",
      "rhetorical_frame": "受限设置分步教学"
    },
    {
      "lang": "tr",
      "text_verbatim": "Tözir indirme işleminin aktif olabilmesi için erişebilirlik iznini veriniz. (Müzik)",
      "text_zh": "为使 Tözir 下载功能生效，请授予无障碍权限。（Müzik）",
      "source_location": "密文 QzAFoPyJY/jd4/3V77jOsm0ILwE4...s8m3e6Sh3Ai8...，directorial$1.onClick 中 Toast 显示",
      "rhetorical_frame": "假更新"
    },
    {
      "lang": "tr",
      "text_verbatim": "Gerekli izni vermeden uygulamayı kullanamazsınız.",
      "text_zh": "未授予必要权限，你无法使用本应用。",
      "source_location": "密文 Q5B9w06w+F69fIn7XARt+5fEv/beEofP...，hypochondriasis.onRequestPermissionsResult 中 Toast 显示",
      "rhetorical_frame": "故障恐吓"
    },
    {
      "lang": "tr",
      "text_verbatim": "Tözfeln daha sonra deneyiniz.",
      "text_zh": "请稍后再试。",
      "source_location": "密文 ckddoEX0WrBSXX3MabJLdY1JjOknMIbwdzq59BerIiCkMICPE5olwg==，hypochondriasis.onResume / Readstown 中 Toast 显示",
      "rhetorical_frame": "故障恐吓"
    }
  ],
  "how_user_is_guided_to_enable": {
    "trigger_timing": "cold_start_0_step",
    "has_cancel_or_skip": false,
    "refusal_loop_mechanism": "引导页返回键被 onKeyDown(keyCode==4) 直接吞掉；拒权/返回后 Toast“Gerekli izni vermeden uygulamayı kullanamazsınız.”并 finish()，应用下次冷启动仍按 accs!=true 重跳 directorial 引导页，形成重复索取（无定时器强制拉起）",
    "overlay_or_fake_settings": "无半透明遮罩、无全屏悬浮窗、无高仿系统无障碍开关页；仅用 GIF 演示图 + Toast 指引，并直接把用户送入真实系统设置页且用 :settings:show_fragment_args 预定位到自身服务项",
    "restricted_settings_13plus_coaching": "无",
    "post_grant_anti_removal": "无",
    "benign_graceful_degradation": "无"
  },
  "utg_capture_guidance": {
    "best_trigger_hook": "在检测到 startActivity 跳转 android.settings.ACCESSIBILITY_SETTINGS（或 com.samsung.accessibility.installed_service）且 Intent 携带 :settings:show_fragment_args 含本应用无障碍服务类名的瞬间拉起 UTG；或在 directorial（引导页）首次 onResume 后 800ms 抓取",
    "key_pages_to_capture": [
      {
        "page_role": "冷启动引导说明页",
        "page_identifier": "com.quadrigeminate.hydrocatalysis.directorial，布局 R.layout.synonymes，含 TextView 正文与单个“İzin Ver”卡片，无返回/跳过入口",
        "why_most_useful": "这是唯一的说明性界面，能同时确认伪装话术、GIF 教学图和“无取消按钮”的强制结构",
        "observable_utg_signals": ["节点文本 Tözir indirme işleminin aktif olabilmesi için yukarıda gösterilen izni veriniz.", "按钮文本 İzin Ver", "节点树中不存在“跳过/取消/Iptal”类可点击文本", "ImageView 中 GIF 帧（gifyu.com 远端图）"]
      },
      {
        "page_role": "跳转前 Toast 提示",
        "page_identifier": "Toast 文本“Tözir ... erişebilirlik iznini veriniz. (Müzik)”",
        "why_most_useful": "直接给出“应用主动索要无障碍权限”的语义证据，且带伪装应用名",
        "observable_utg_signals": ["含 erişebilirlik（无障碍）关键词", "括号内应用名 (Müzik)"]
      },
      {
        "page_role": "系统无障碍服务列表项",
        "page_identifier": "Settings 无障碍列表中的“Müzik”条目（label 含零宽空格，无 summary/description）",
        "why_most_useful": "对比系统展示的服务名与桌面应用名，验证零宽字符伪装与无用途说明的弱告知",
        "observable_utg_signals": ["服务项文本含 U+200B", "该条目无描述文本（summary 为空）", "包名 com.quadrigeminate.hydrocatalysis"]
      },
      {
        "page_role": "拒权返回后的提示与退出",
        "page_identifier": "Toast“Gerekli izni vermeden uygulamayı kullanamazsınız.”后应用界面消失",
        "why_most_useful": "证明无降级路径与重复索取行为（再次冷启动回到引导页）",
        "observable_utg_signals": ["Toast 文本含 Gerekli izni vermeden", "随后当前 Activity finish（界面消失/回到桌面）", "再次启动仍出现同一引导页"]
      }
    ],
    "needs_ocr_for_image_lure": true,
    "detection_blindspot_note": "GIF 教学图与获权后 WebView 页面内容均由远端下发（gifyu.com 图片、rx/f.php），若断网或服务器下线则这两处不可见；另需注意引导文案全部为本地加密字符串，静态文本检索（如搜 ACCESSIBILITY_SETTINGS）会漏检，运行期 UTG 不受影响。"
  },
  "behavior_pattern_tags": [
    "TRIG_COLD_START_BLOCK",
    "CARRIER_NATIVE_DIALOG_OR_ACTIVITY",
    "CARRIER_GIF_OR_IMAGE_GUIDE",
    "CARRIER_WEBVIEW_REMOTE_URL",
    "COERCE_NO_SKIP_NON_CANCELABLE",
    "COERCE_REFUSAL_LOOP_RELAUNCH",
    "ID_WHITESPACE_NEWLINE_OR_HOMOGLYPH",
    "ID_MULTI_ALIAS_CAMOUFLAGE"
  ],
  "code_anchors": [
    "com.quadrigeminate.hydrocatalysis.hypochondriasis#onResume",
    "com.quadrigeminate.hydrocatalysis.hypochondriasis#Readstown",
    "com.quadrigeminate.hydrocatalysis.directorial#onResume",
    "com.quadrigeminate.hydrocatalysis.directorial$1#onClick",
    "com.quadrigeminate.hydrocatalysis.directorial#onKeyDown",
    "res/xml/preferences.xml"
  ]
}
```

</details>
