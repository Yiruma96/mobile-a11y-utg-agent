# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T10:18:28
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.mydocs.documents`（静态标签：`malicious` / `BrasDex` / 静态可见性：`clear`）
- **最终状态**：`max_steps_reached`（共执行 8 步，UTG 唯一节点 `1` 个，有向边 `7` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.mydocs.documents` / `mainActivity` | `-` | 0 | 0 / 否 | `open` | `step_01_layout.xml` + `step_01_layout_harmony.json` |
| 2 | `com.mydocs.documents` / `mainActivity` | `-` | 0 | 0 / 否 | `wait` | `step_02_layout.xml` + `step_02_layout_harmony.json` |
| 3 | `com.mydocs.documents` / `mainActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_03_layout.xml` + `step_03_layout_harmony.json` |
| 4 | `com.mydocs.documents` / `mainActivity` | `-` | 0 | 0 / 否 | `click` → [340, 1220] | `step_04_layout.xml` + `step_04_layout_harmony.json` |
| 5 | `com.mydocs.documents` / `mainActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_05_layout.xml` + `step_05_layout_harmony.json` |
| 6 | `com.mydocs.documents` / `mainActivity` | `-` | 0 | 0 / 否 | `static_activity_jump` | `step_06_layout.xml` + `step_06_layout_harmony.json` |
| 7 | `com.mydocs.documents` / `mainActivity` | `-` | 0 | 0 / 否 | `open` | `step_07_layout.xml` + `step_07_layout_harmony.json` |
| 8 | `com.mydocs.documents` / `mainActivity` | `-` | 0 | 0 / 否 | `wait` | `step_08_layout.xml` + `step_08_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.mydocs.documents/mainActivity`)**: (空文本)
- **Step 2 (`com.mydocs.documents/mainActivity`)**: (空文本)
- **Step 3 (`com.mydocs.documents/mainActivity`)**: (空文本)
- **Step 4 (`com.mydocs.documents/mainActivity`)**: (空文本)
- **Step 5 (`com.mydocs.documents/mainActivity`)**: (空文本)
- **Step 6 (`com.mydocs.documents/mainActivity`)**: (空文本)
- **Step 7 (`com.mydocs.documents/mainActivity`)**: (空文本)
- **Step 8 (`com.mydocs.documents/mainActivity`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：该应用启动后始终未渲染有效界面，屏幕停留在桌面/启动器；轨迹仅通过静态引导跳转尝试进入 .Root.Initializer 与 .Services.serviceMagic 等组件，未触发授权/拒权流程，未见通知、遮罩或诱导话术。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: mainActivity** | 当前为设备桌面/启动器，未见应用窗口；执行打开应用尝试，但目标 mainActivity 未渲染，无通知或遮罩。 | `step_01_action.png` |
| 2 | **Step 2: mainActivity** | 界面仍停留在桌面/启动器，应用窗口未出现；等待后无任何 UI 文本、通知横幅或遮罩，未观察到诱导话术。 | `step_02_action.png` |
| 3 | **Step 3: mainActivity** | 仍为桌面/启动器；通过静态引导回退跳转 .Root.Initializer，页面无可见文本与交互控件，通知/遮罩均为 0。 | `step_03_screen.png` |
| 4 | **Step 4: mainActivity** | 桌面/启动器未渲染应用界面；在坐标[340,1220]点击桌面文档图标尝试拉起，仍无应用窗口、通知或遮罩。 | `step_04_action.png` |
| 5 | **Step 5: mainActivity** | 屏幕仍无应用界面；静态引导回退跳转至 .Services.serviceMagic 服务组件，未见文本、通知或遮罩，也无取消键。 | `step_05_screen.png` |
| 6 | **Step 6: mainActivity** | 仍停留在桌面/启动器；静态引导回退跳转回 .mainActivity，未渲染任何可见内容，无通知、遮罩与诱导话术。 | `step_06_screen.png` |
| 7 | **Step 7: mainActivity** | 可见界面仍为桌面/启动器；再次按包名显式启动应用，目标窗口未出现，未观察到文本、通知或遮罩。 | `step_07_action.png` |
| 8 | **Step 8: mainActivity** | 应用报告前台但屏幕仍显示桌面/启动器；等待后未见 mainActivity 内容，无 UI 文本、通知、遮罩或授权弹窗。 | `step_08_action.png` |
