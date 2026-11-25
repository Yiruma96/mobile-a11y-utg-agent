# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:20:03
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.duke.centers`（静态标签：`malicious` / `SpyNote` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `5` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.duke.centers/com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.MainActivity` | hooks=`[]` | overlays=`0` | texts=``
- **Back 后 +5.5s**：`com.duke.centers/com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20` | hooks=`[]` | overlays=`0` | texts=`Accessibility Service / .nered / To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App / Enable`
- **Back 后 +10.5s**：`com.duke.centers/com.duke.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20` | hooks=`[]` | overlays=`0` | texts=`Accessibility Service / .nered / To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App / Enable`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.duke.centers` / `isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20` | `-` | 7 | 166 / 否 | `click` → [7] Button text="Enable" id=okbtn (click) center=(540,1 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 32 | 205 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.duke.centers/isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20`)**: `Accessibility Service` | `.nered` | `To unlock premium feature,  Follow these steps 1. Click` | `Enable`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `.nered` | `Off` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY` | `Font size`

## 中文逐页引导链路解读

> **全链路总结**：应用先以伪造“Accessibility Service”页面和虚构“解锁高级功能”步骤诱导点击 Enable，跳转系统无障碍列表并打开 .nered 服务详情；在系统“完全控制设备”警告处拒绝后，应用回退到空白主页并反复重弹同一诱导页，表现出 SpyNote 无障碍授权钓鱼与拒权重生特征。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “To unlock premium feature, Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App” 中文意为“解锁高级功能，请按步骤：1.点击启用按钮 2.进入已安装服务/应用 3.启用高亮应用”（伪造无障碍引导页 step_01、refusal_5.5s、refusal_10.5s）
- 英文 -> “Allow .nered to have full control of your device?” 中文意为“允许 .nered 完全控制你的设备？”，并说明可查看控制屏幕、读取所有内容、覆盖其他应用及代表用户操作（系统警告弹窗 detail_2）
- 英文 -> “Use .nered”“.nered shortcut”“Hold volume keys” 中文意为“使用 .nered”“.nered 快捷方式”“按住音量键”（服务详情页 detail_1）
- 英文 -> 通知标题伪装为“Google Play Services”，正文“Tap to learn more...” 中文意为“点按了解更多”（应用通知横幅，贯穿各页）
- 英文 -> “Your data isn’t backed up”“Add a backup account now” 中文意为“你的数据未备份”“立即添加备份账户”（Google Play Services 通知，贯穿各页）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: isrjhroorjshhuhvaoyxhzihjo** | 伪造无障碍引导页，英文以“解锁高级功能”诱导点 Enable 并到已安装服务启用高亮应用；点击后跳系统设置，通知栏有伪装 Google Play Services 横幅，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 系统无障碍列表，DOWNLOADED APPS 中 .nered 为 Off；采集无障碍 Hook/探针后终止，通知栏有伪装 Google Play Services 横幅，无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳转后 0.8 秒探针，仍停在系统无障碍设置页，UI 文本为空、无遮罩；通知栏继续显示伪装 Google Play Services 横幅与数据未备份提示。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳转后 2.0 秒探针，仍在系统无障碍设置页且无任何 UI 文本与遮罩；通知栏持续显示伪装 Google Play Services 横幅及数据未备份提示。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 打开 .nered 无障碍服务详情页，英文显示“Use .nered”、快捷方式与“按住音量键”等选项；仅检查未授权，通知栏仍有伪装横幅，无遮罩。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统无障碍授权警告框，英文称允许 .nered 完全控制设备，可读屏、覆盖应用并代操作；本步仅检查并准备点 Deny，无遮罩，通知栏仍有伪装横幅。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 在警告框拒绝后回到应用 MainActivity，界面文本为空；随后触发 RELAUNCHED_LURE_DIALOG，通知栏仍有伪装 Google Play Services 横幅，无遮罩。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +5.5s** | 拒权返回 5.5 秒后重弹同一伪造无障碍引导页，英文仍以“解锁高级功能”诱导 Enable；属 RELAUNCHED_LURE_DIALOG，通知栏伪装横幅持续，无遮罩。 | `step_02_refusal_5500ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权返回 10.5 秒后再次重弹伪造引导页，英文步骤与 Enable 按钮不变，持续施压；属 RELAUNCHED_LURE_DIALOG，通知栏伪装横幅仍在，无遮罩。 | `step_02_refusal_10500ms_screen.png` |
