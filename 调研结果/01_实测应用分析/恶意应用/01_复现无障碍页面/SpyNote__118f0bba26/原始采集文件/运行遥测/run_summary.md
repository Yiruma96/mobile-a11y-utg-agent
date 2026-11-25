# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T16:12:34
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.corporate.finished`（静态标签：`malicious` / `SpyNote` / 静态可见性：`clear`）
- **最终状态**：`hook_captured`（共执行 2 步，UTG 唯一节点 `5` 个，有向边 `6` 条）
- **拒权回退探针结论（Golden Page ④）**：`RELAUNCHED_LURE_DIALOG`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

| 步号 | 触发锚点 | 所在包 / Activity | 跳后遮罩探针（0.8s / 2.0s） | 鸿蒙 Layout JSON |
|---:|---|---|---|---|
| Step 2 | `HOOK_A11Y_SETTINGS` | `com.android.settings/com.android.settings.Settings$AccessibilitySettingsActivity` | 0.8s: 无异源遮罩 / 2.0s: 无异源遮罩 | `step_02_layout_harmony.json` |

## 2. 拒权返回探针结果（按 Back 模拟拒绝开启无障碍）

- **Back 后 +2.0s**：`com.corporate.finished/com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.MainActivity` | hooks=`[]` | overlays=`0` | texts=``
- **Back 后 +5.5s**：`com.corporate.finished/com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20` | hooks=`[]` | overlays=`0` | texts=`Accessibility Service / Blockchain / To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App / Enable`
- **Back 后 +10.5s**：`com.corporate.finished/com.corporate.vhasjbytsejmchjytybqaiucxsovcftvkngegomeqdvgmgvqzg2.isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20` | hooks=`[]` | overlays=`0` | texts=`Accessibility Service / Blockchain / To unlock premium feature,  Follow these steps 1. Click on Enable Button 2. Go to Installed services / Apps 3. Enable Highlighted App / Enable`

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.corporate.finished` / `isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20` | `-` | 7 | 170 / 否 | `click` → [7] Button text="Enable" id=okbtn (click) center=(540,1 | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.android.settings` / `Settings$AccessibilitySettingsActivity` | `HOOK_A11Y_SETTINGS` | 33 | 201 / 否 | `terminate` → Captured Accessibility Settings hook & probes | `step_02_layout.xml` + `step_02_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.corporate.finished/isrjhroorjshhuhvaoyxhzihjosgyxaalfopwxsqtcaxyhmbzs20`)**: `Accessibility Service` | `Blockchain` | `To unlock premium feature,  Follow these steps 1. Click` | `Enable`
- **Step 2 (`com.android.settings/Settings$AccessibilitySettingsActivity`)**: `Back` | `Accessibility` | `Search settings` | `DOWNLOADED APPS` | `Blockchain` | `Off` | `media player` | `SCREEN READERS` | `Text-to-speech output` | `DISPLAY`

## 中文逐页引导链路解读

> **全链路总结**：应用先以“解锁高级功能”为名，在伪造的无障碍开通页诱导点击 Enable，跳转系统无障碍列表并进入 Blockchain 服务详情；用户拒绝完全控制权限后，应用返回主界面并反复重弹同一诱导页。全程伴随伪装成 Google Play 服务的通知横幅，且无覆盖层。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文「Accessibility Service / Blockchain / To unlock premium feature, Follow these steps... / Enable」 -> 中文意译：为解锁高级功能，请点击启用并到已安装服务/应用中启用高亮应用；位于伪无障碍开通页（step_01、refusal_5.5s、refusal_10.5s）。
- 英文「String (Google Play Services) / String (Tap to learn more...)」 -> 中文意译：伪装成 Google Play 服务的通知，提示点击了解更多，用于增强可信度；位于多数页面的通知横幅。
- 英文「Use Blockchain / Blockchain shortcut / Hold volume keys」 -> 中文意译：以使用 Blockchain、音量键快捷键等正常设置项包装恶意无障碍服务；位于服务详情页。
- 英文「Allow Blockchain to have full control of your device? ... Allow / Deny」 -> 中文意译：系统警告是否允许 Blockchain 完全控制设备、读屏并代操作；位于系统授权弹窗。

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: isrjhroorjshhuhvaoyxhzihjo** | 伪无障碍开通页：以“解锁高级功能”为由，列出三步诱导开启 Blockchain 服务；本步点击 Enable，并见伪 Google Play 通知横幅，无遮罩。 | `step_01_action.png` |
| 2 | **Step 2: [无障碍列表页]** | 跳转系统无障碍列表：DOWNLOADED APPS 下 Blockchain 显示 Off；因捕获 HOOK_A11Y_SETTINGS 与探针而自动终止，通知横幅仍在，无遮罩。 | `step_02_screen.png` |
| 3 | **跳后探针 +0.8s** | 跳后 0.8 秒探针：仍停留系统无障碍页，界面无可读文本，仅见伪 Google Play 通知；遮罩数为 0，未出现覆盖层。 | `step_02_probe_800ms_screen.png` |
| 4 | **跳后探针 +2.0s** | 跳后 2.0 秒探针：页面仍无可见文本，系统无障碍列表未变化，伪 Google Play 通知持续存在；遮罩数为 0。 | `step_02_probe_2000ms_screen.png` |
| 5 | **服务详情页** | 服务详情页：显示 Blockchain 的 Use Blockchain 开关及快捷键选项；此为系统设置包装页，本步仅检查详情，通知仍在，遮罩为 0。 | `step_02_service_detail_screen.png` |
| 6 | **系统警告弹窗(点Deny)** | 系统风险弹窗：警告允许 Blockchain 完全控制设备，会读屏并可代操作；提供 Allow/Deny，本步仅检查未授权，遮罩为 0。 | `step_02_system_warning_screen.png` |
| 7 | **拒权返回 +2.0s** | 拒权返回 2 秒：回到 MainActivity，界面无文本；应用随即准备重弹诱导窗，通知仍在，遮罩为 0。 | `step_02_refusal_2000ms_screen.png` |
| 8 | **拒权返回 +5.5s** | 拒权后 5.5 秒：恶意无障碍诱导页重新弹出，重复“解锁高级功能”三步话术与 Enable 按钮；通知仍在，遮罩为 0。 | `step_02_refusal_5500ms_screen.png` |
| 9 | **拒权返回 +10.5s** | 拒权后 10.5 秒：同一诱导页持续重弹，仍以 Blockchain 与 Enable 按钮催促开启无障碍；通知横幅未撤，遮罩为 0。 | `step_02_refusal_10500ms_screen.png` |
