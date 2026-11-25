# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T13:35:08
- **平台与设备**：`android` / `emulator-5558`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`nvyfee.dcvxvm.zsakxl`（静态标签：`malicious` / `TrickMo` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `3` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `nvyfee.dcvxvm.zsakxl` / `e` | `-` | 1 | 0 / 是 | `wait` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `nvyfee.dcvxvm.zsakxl` / `e` | `-` | 2 | 1 / 是 | `wait` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `nvyfee.dcvxvm.zsakxl` / `e` | `-` | 2 | 1 / 是 | `click` → [2] Image text="y" center=(540,1156) | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `nvyfee.dcvxvm.zsakxl` / `e` | `-` | 2 | 1 / 是 | `static_activity_jump` | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `nvyfee.dcvxvm.zsakxl` / `e` | `-` | 2 | 1 / 是 | `wait` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `nvyfee.dcvxvm.zsakxl` / `e` | `-` | 2 | 1 / 是 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.google.android.packageinstaller` / `PackageInstallerActivity` | `-` | 4 | 108 / 否 | `static_activity_jump` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.google.android.packageinstaller` / `PackageInstallerActivity` | `-` | 4 | 108 / 否 | `static_activity_jump` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`nvyfee.dcvxvm.zsakxl/e`)**: (空文本)
- **Step 2 (`nvyfee.dcvxvm.zsakxl/e`)**: `y`
- **Step 3 (`nvyfee.dcvxvm.zsakxl/e`)**: `y`
- **Step 4 (`nvyfee.dcvxvm.zsakxl/e`)**: `y`
- **Step 5 (`nvyfee.dcvxvm.zsakxl/e`)**: `y`
- **Step 6 (`nvyfee.dcvxvm.zsakxl/e`)**: `y`
- **Step 7 (`com.google.android.packageinstaller/PackageInstallerActivity`)**: `TikTok18` | `For your security, your phone is not allowed to install` | `Cancel` | `Settings`
- **Step 8 (`com.google.android.packageinstaller/PackageInstallerActivity`)**: `TikTok18` | `For your security, your phone is not allowed to install` | `Cancel` | `Settings`

## 中文逐页引导链路解读

> **全链路总结**：入口为 WebView 版 TikTok 开屏占位页，反复显示“y”并经静态引导跳转至 com.example.tiramisudropper 组件，随后拉起系统安装器尝试安装“TikTok18”但被“禁止未知来源安装”拦截，仅提供取消/设置；全程无应用内遮罩，通知栏持续出现 Google 备份提示。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文通知 -> “你的数据未备份”/“立即添加备份账户”（全程通知栏，非应用内弹窗）
- 英文占位 -> “y”（TikTok 开屏 WebView，Step2-Step6）
- 英文应用名 -> “TikTok18”（系统安装器页，Step7-Step8）
- 英文提示 -> “为你的安全，你的手机不允许从此来源安装未知应用。”（系统安装器页，Step7-Step8）
- 英文按钮 -> “取消”/“设置”（系统安装器页，Step7-Step8）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: e** | WebView 显示 TikTok 开屏占位，暂未见文本，无遮罩；通知提示数据未备份；本步仅等待未点击。 | `step_01_action.png` |
| 2 | **Step 2: e** | 仍为 TikTok 开屏 WebView，仅见占位“y”，无遮罩；通知提示数据未备份；本步继续等待，未点击。 | `step_02_action.png` |
| 3 | **Step 3: e** | TikTok 开屏 WebView 仍见“y”，无遮罩；通知持续提示数据未备份；本步点击图像“y”尝试推进假更新流程。 | `step_03_action.png` |
| 4 | **Step 4: e** | 同一开屏页仅见“y”，无遮罩；通知仍在；本步为静态引导跳转探针，目标为 tiramisudropper.b。 | `step_04_screen.png` |
| 5 | **Step 5: e** | 仍停留 TikTok 开屏 WebView，仅见“y”，无遮罩；通知提示数据未备份；本步等待 WebView 加载，未点击。 | `step_05_action.png` |
| 6 | **Step 6: e** | 仍为开屏 WebView 占位“y”，无遮罩；通知持续；本步静态引导跳转探针指向 tiramisudropper.a。 | `step_06_screen.png` |
| 7 | **Step 7: PackageInstallerActivity** | 系统安装器页显示“TikTok18”，提示禁止从此来源安装未知应用，含取消/设置；无遮罩；本步静态跳转探针，未授权。 | `step_07_screen.png` |
| 8 | **Step 8: PackageInstallerActivity** | 仍为系统安装器拦截页，显示“TikTok18”和禁止未知来源安装提示，含取消/设置；无遮罩；本步静态跳转探针，未安装。 | `step_08_screen.png` |
