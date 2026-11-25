# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T12:47:53
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.safe.census`（静态标签：`malicious` / `Cerberus` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`success`（共执行 1 步，UTG 唯一节点 `1` 个，有向边 `0` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.safe.census` / `dpugiw` | `-` | 1 | 0 / 是 | `terminate` → App launched into its WebView-guided flow which trigger | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.safe.census/dpugiw`)**: (空文本)

## 中文逐页引导链路解读

> **全链路总结**：应用启动后即通过 WebView 引导跳转至系统无障碍设置，试图诱导用户为恶意服务开启无障碍授权；本次运行未继续后续流程并直接终止，授权/拒权结果未测试。

![全流程中文标注连环画](./utg_storyboard.png)

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: dpugiw** | 该页为 WebView 引导后跳转的系统无障碍设置界面，未抓取到页面文案，意图诱导开启恶意服务；本步已终止。 | `step_01_action.png` |
