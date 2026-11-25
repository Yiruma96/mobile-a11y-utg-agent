# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T14:44:26
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.parcellize.unmatrimonial`（静态标签：`malicious` / `GodFather` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.parcellize.unmatrimonial` / `Tatarian` | `-` | 3 | 82 / 否 | `click` → [3] Button text="OK" id=button (click) center=(539,1941 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 299 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 299 / 否 | `click` → [1] ImageButton desc="Back" (click) center=(77,160) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.parcellize.unmatrimonial` / `Tatarian` | `-` | 3 | 82 / 否 | `click` → [3] Button text="OK" id=button (click) center=(539,1941 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.parcellize.unmatrimonial` / `Okawville` | `-` | 3 | 67 / 否 | `click` → [3] Button text="YÜKLE" id=button1 (click) center=(884, | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.packageinstaller` / `PackageInstallerActivity` | `-` | 3 | 53 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.parcellize.unmatrimonial` / `Okawville` | `-` | 3 | 67 / 否 | `click` → [3] Button text="YÜKLE" id=button1 (click) center=(884, | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.packageinstaller` / `PackageInstallerActivity` | `-` | 3 | 53 / 否 | `click` → [3] Button text="Install" id=button1 (click) center=(88 | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.parcellize.unmatrimonial/Tatarian`)**: `Müzik İndir` | `Uygulamanın tüm özelliklerini kullanmak için izin verme` | `OK`
- **Step 2 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `Müzik İndir` | `1.0` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 3 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `Müzik İndir` | `1.0` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 4 (`com.parcellize.unmatrimonial/Tatarian`)**: `Müzik İndir` | `Uygulamanın tüm özelliklerini kullanmak için izin verme` | `OK`
- **Step 5 (`com.parcellize.unmatrimonial/Okawville`)**: `Bilgi` | `Uygulamamızı kullanabilmek için eklentiyi yüklemelisini` | `YÜKLE`
- **Step 6 (`com.google.android.packageinstaller/PackageInstallerActivity`)**: `Do you want to install this application?` | `Cancel` | `Install`
- **Step 7 (`com.parcellize.unmatrimonial/Okawville`)**: `Bilgi` | `Uygulamamızı kullanabilmek için eklentiyi yüklemelisini` | `YÜKLE`
- **Step 8 (`com.google.android.packageinstaller/PackageInstallerActivity`)**: `Do you want to install this application?` | `Cancel` | `Install`

## 中文逐页引导链路解读

> **全链路总结**：该GodFather样本以土耳其语“音乐下载”为伪装，先诱导授权并开启未知来源安装权限，再反复以“必须安装插件”弹窗拉起系统安装器，最终点Install安装内嵌载荷；未见拒绝路径测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 Müzik İndir -> “下载音乐”（Step1/4 Tatarian首屏应用名，伪装下载器）
- 土耳其语 Uygulamanın tüm özelliklerini kullanmak için izin vermeniz gerekiyor. -> “使用全部功能需授予权限”（Step1/4授权提示）
- 土耳其语 Bilgi -> “信息/提示”（Step5/7 Okawville弹窗标题）
- 土耳其语 Uygulamamızı kullanabilmek için eklentiyi yüklemelisiniz. -> “要使用应用必须安装插件”（Step5/7弹窗）
- 土耳其语 YÜKLE -> “安装”（Step5/7按钮，诱导安装插件）
- 英语 Allow from this source -> “允许来自此来源”（Step2系统设置，用于放行未知来源安装）
- 英语 Do you want to install this application? -> “是否安装此应用？”（Step6/8系统安装确认）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: Tatarian** | “下载音乐”首屏弹出土耳其语授权提示，称需授权才能用全部功能；本步点OK进入未知来源设置，无通知遮罩。 | `step_01_action.png` |
| 2 | **Step 2: Settings$ManageAppExternal** | 系统“安装未知应用”页显示Müzik İndir 1.0及英文风险警告；本步打开允许来源开关，为装载荷铺路，无通知遮罩。 | `step_02_action.png` |
| 3 | **Step 3: Settings$ManageAppExternal** | 同一未知来源设置页，允许来源开关已开启；本步点Back返回应用继续流程，无通知遮罩。 | `step_03_action.png` |
| 4 | **Step 4: Tatarian** | 回到“下载音乐”首屏，仍弹土耳其语授权提示并需点OK；本步再次点OK推进后续插件安装诱导，无通知遮罩。 | `step_04_action.png` |
| 5 | **Step 5: Okawville** | 进入Okawville“信息”弹窗，土耳其语称必须安装插件才能用应用；本步点“安装”按钮拉起系统安装器，无通知遮罩。 | `step_05_action.png` |
| 6 | **Step 6: PackageInstallerActivity** | 系统安装确认页，英文询问是否安装此应用，有取消/安装；本步静态跳转回Tatarian，未实际确认安装。 | `step_06_screen.png` |
| 7 | **Step 7: Okawville** | 再次回到Okawville“信息”插件弹窗，仍称必须安装插件；本步再点“安装”重启安装会话，无通知遮罩。 | `step_07_action.png` |
| 8 | **Step 8: PackageInstallerActivity** | 系统安装确认页再现，英文询问是否安装，有取消/安装；本步点击Install确认安装内嵌载荷，无通知遮罩。 | `step_08_action.png` |
