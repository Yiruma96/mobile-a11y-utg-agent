# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:51:45
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.slhytrowb.wfxaicaiw`（静态标签：`malicious` / `MaliBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `4` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.slhytrowb.wfxaicaiw` / `BrowserAppActivity` | `-` | 5 | 277 / 否 | `system_button` → Back | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `android` / `ResolverActivity` | `-` | 6 | 70 / 否 | `click` → [6] TextView text="Amazon App" id=text1 center=(302,206 | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.slhytrowb.wfxaicaiw` / `PixelLauncher` | `-` | 7 | 45 / 否 | `click` → [1] View desc="Apps list" (click) center=(540,1786) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.slhytrowb.wfxaicaiw` / `PixelLauncher` | `-` | 7 | 45 / 否 | `swipe` → [540, 1900] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.slhytrowb.wfxaicaiw` / `PixelLauncher` | `-` | 21 | 158 / 否 | `click` → [3] TextView text="Amazon App" id=icon (click) center=( | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.slhytrowb.wfxaicaiw` / `BrowserAppActivity` | `-` | 5 | 277 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.slhytrowb.wfxaicaiw` / `BrowserAppActivity` | `-` | 5 | 277 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.slhytrowb.wfxaicaiw` / `BrowserAppActivity` | `-` | 5 | 277 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.slhytrowb.wfxaicaiw/BrowserAppActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at https://socrersutagans.site/?botid=53bde` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 2 (`android/ResolverActivity`)**: `Use Pixel Launcher as Home` | `Just once` | `Always` | `Use a different app` | `Amazon App`
- **Step 3 (`com.slhytrowb.wfxaicaiw/PixelLauncher`)**: `Apps list` | `Gmail` | `Photos` | `Phone` | `Messages` | `Chrome` | `Camera`
- **Step 4 (`com.slhytrowb.wfxaicaiw/PixelLauncher`)**: `Apps list` | `Gmail` | `Photos` | `Phone` | `Messages` | `Chrome` | `Camera`
- **Step 5 (`com.slhytrowb.wfxaicaiw/PixelLauncher`)**: `Apps list` | `Search apps` | `Amazon App` | `Calendar` | `Camera` | `Chrome` | `Clock` | `Contacts` | `Drive` | `Files`
- **Step 6 (`com.slhytrowb.wfxaicaiw/BrowserAppActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at https://socrersutagans.site/?botid=53bde` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 7 (`com.slhytrowb.wfxaicaiw/BrowserAppActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at https://socrersutagans.site/?botid=53bde` | `net::ERR_INTERNET_DISCONNECTED`
- **Step 8 (`com.slhytrowb.wfxaicaiw/BrowserAppActivity`)**: `Webpage not available` | `x+AAAAAElFTkSuQmCC` | `The webpage at https://socrersutagans.site/?botid=53bde` | `net::ERR_INTERNET_DISCONNECTED`

## 中文逐页引导链路解读

> **全链路总结**：应用启动后先由BrowserAppActivity加载带botid、page=accessibility等参数的远程页面，因断网显示WebView错误页；随后经系统主页选择器、内置启动器和多次静态跳转指向AccessibilityRequest、AccessibilityService与StartActivity，呈现MaliBot借无障碍授权话术引导用户开启服务的链路特征，但本次未完成授权/拒权测试。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “网页不可用”：内嵌WebView加载失败的系统提示（步骤1/6/7/8）
- 英文URL参数 -> page=accessibility、botkey=mfe、botid=…：以“无障碍”页面为引导并按机器人标识回传（步骤1/6/7/8）
- 英文 -> “网页在…无法加载，因为 net::ERR_INTERNET_DISCONNECTED”：网络断开错误提示（步骤1/6/7/8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: BrowserAppActivity** | 内嵌WebView报错页：英文提示“网页不可用”，含page=accessibility的远程地址因断网加载失败；按返回键，无通知/遮罩。 | `step_01_action.png` |
| 2 | **Step 2: ResolverActivity** | 系统主页选择器：英文含“仅一次/始终/使用其他应用/Amazon App”；点击Amazon App，未设默认桌面。 | `step_02_action.png` |
| 3 | **Step 3: PixelLauncher** | 应用内置启动器桌面，显示Gmail、相机等图标；点击“应用列表”入口，未见明显响应。 | `step_03_action.png` |
| 4 | **Step 4: PixelLauncher** | 仍为内置启动器桌面，显示应用列表与常用图标；上滑尝试打开应用抽屉寻找Amazon App入口。 | `step_04_action.png` |
| 5 | **Step 5: PixelLauncher** | 应用抽屉展开，英文“搜索应用”，列出Amazon App等图标；点击Amazon App图标尝试重新拉起目标应用。 | `step_05_action.png` |
| 6 | **Step 6: BrowserAppActivity** | 再次显示WebView“网页不可用”断网页；随后静态跳转至AccessibilityRequest，试图进入无障碍授权引导。 | `step_06_screen.png` |
| 7 | **Step 7: BrowserAppActivity** | 仍为WebView“网页不可用”断网页，URL含page=accessibility；静态跳转至AccessibilityService无障碍服务组件。 | `step_07_screen.png` |
| 8 | **Step 8: BrowserAppActivity** | 仍为“网页不可用”断网页；静态跳转至StartActivity，形成远程无障碍话术页到本地启动组件的引导链。 | `step_08_screen.png` |
