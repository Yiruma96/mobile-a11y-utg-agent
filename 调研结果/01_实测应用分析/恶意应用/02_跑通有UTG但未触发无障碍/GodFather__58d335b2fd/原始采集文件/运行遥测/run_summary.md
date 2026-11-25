# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:27:30
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.sulphatase.wordman`（静态标签：`malicious` / `GodFather` / 静态可见性：`partial_dynamic_or_remote`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.sulphatase.wordman` / `goldcrest` | `-` | 3 | 82 / 否 | `click` → [3] Button text="OK" id=button (click) center=(539,1941 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 299 / 否 | `click` → [9] Switch id=switch_widget (unchecked) center=(972,707 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.android.settings` / `Settings$ManageAppExternalSourcesActivity` | `-` | 10 | 299 / 否 | `system_button` → Back | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.sulphatase.wordman` / `goldcrest` | `-` | 3 | 82 / 否 | `click` → [3] Button text="OK" id=button (click) center=(539,1941 | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.sulphatase.wordman` / `facecentered` | `-` | 3 | 67 / 否 | `click` → [3] Button text="YÜKLE" id=button1 (click) center=(884, | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.google.android.packageinstaller` / `PackageInstallerActivity` | `-` | 3 | 53 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.sulphatase.wordman` / `facecentered` | `-` | 3 | 67 / 否 | `click` → [3] Button text="YÜKLE" id=button1 (click) center=(884, | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.packageinstaller` / `PackageInstallerActivity` | `-` | 3 | 53 / 否 | `click` → [3] Button text="Install" id=button1 (click) center=(88 | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.sulphatase.wordman/goldcrest`)**: `Müzik İndir` | `Uygulamanın tüm özelliklerini kullanmak için izin verme` | `OK`
- **Step 2 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `Müzik İndir` | `1.0` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 3 (`com.android.settings/Settings$ManageAppExternalSourcesActivity`)**: `Back` | `Install unknown apps` | `Search settings` | `Müzik İndir` | `1.0` | `Allow from this source` | `Your phone and personal data are more vulnerable to att`
- **Step 4 (`com.sulphatase.wordman/goldcrest`)**: `Müzik İndir` | `Uygulamanın tüm özelliklerini kullanmak için izin verme` | `OK`
- **Step 5 (`com.sulphatase.wordman/facecentered`)**: `Bilgi` | `Uygulamamızı kullanabilmek için eklentiyi yüklemelisini` | `YÜKLE`
- **Step 6 (`com.google.android.packageinstaller/PackageInstallerActivity`)**: `Do you want to install this application?` | `Cancel` | `Install`
- **Step 7 (`com.sulphatase.wordman/facecentered`)**: `Bilgi` | `Uygulamamızı kullanabilmek için eklentiyi yüklemelisini` | `YÜKLE`
- **Step 8 (`com.google.android.packageinstaller/PackageInstallerActivity`)**: `Do you want to install this application?` | `Cancel` | `Install`

## 中文逐页引导链路解读

> **全链路总结**：该应用以“Müzik İndir（下载音乐）”为名，先诱导用户开启“安装未知应用”，再以“必须安装插件”弹窗反复拉起系统安装器安装二阶段APK；整体为GodFather类社会工程侧载链路，本次未测试拒权结果。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 土耳其语 -> 使用应用全部功能需授予权限（Step 1/4启动页）
- 英语 -> 安装未知来源应用会使手机和个人数据更易受攻击，您需自行承担风险（Step 2/3设置页）
- 土耳其语 -> 要使用我们的应用必须安装插件（Step 5/7提示弹窗）
- 英语 -> 是否安装此应用（Step 6/8系统安装确认页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: goldcrest** | 应用启动页，标题“Müzik İndir（下载音乐）”；土耳其语称需授权才能使用全部功能，仅OK键可点，进入授权引导。 | `step_01_action.png` |
| 2 | **Step 2: Settings$ManageAppExternal** | 系统“安装未知应用”设置页，显示Müzik İndir与英文风险警告；本步点击未勾选的“Allow from this source”开关。 | `step_02_action.png` |
| 3 | **Step 3: Settings$ManageAppExternal** | 同一系统授权页，开关已勾选放行未知来源安装；点击返回键离开设置，返回应用继续诱导。 | `step_03_action.png` |
| 4 | **Step 4: goldcrest** | 返回应用启动页，仍显示“Müzik İndir（下载音乐）”和需授权使用全部功能的土耳其语提示；再次点击OK推进。 | `step_04_action.png` |
| 5 | **Step 5: facecentered** | 应用内“Bilgi（信息）”弹窗，土耳其语称使用应用必须安装插件；仅“YÜKLE（安装）”键，点击拉起二阶段APK安装。 | `step_05_action.png` |
| 6 | **Step 6: PackageInstallerActivity** | 系统安装确认页，英文询问是否安装此应用并提供取消/安装；本步未点击，仅静态跳转回goldcrest入口。 | `step_06_screen.png` |
| 7 | **Step 7: facecentered** | 再次出现“Bilgi（信息）”插件安装弹窗，土耳其语要求安装插件才能使用；点击“YÜKLE（安装）”再次触发安装会话。 | `step_07_action.png` |
| 8 | **Step 8: PackageInstallerActivity** | 系统安装确认页，英文询问是否安装此应用；点击“Install（安装）”确认安装二阶段APK，完成侧载关键一步。 | `step_08_action.png` |
