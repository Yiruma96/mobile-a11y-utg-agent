# 静态引导动态 GUI-Owl Agent 运行与鸿蒙 UTG 捕获报告

- **运行时间**：2026-11-25T15:46:17
- **平台与设备**：`android` / `emulator-5556`（断网隔离：`True`）
- **驱动模型与模式**：`deepseek-v4.1-flash`（模式：`hybrid`）
- **目标应用**：`com.akbjmrnec.wiuvhfydb`（静态标签：`malicious` / `TeaBot` / 静态可见性：`packed_or_encrypted`）
- **最终状态**：`success`（共执行 1 步，UTG 唯一节点 `1` 个，有向边 `0` 条）
- **拒权回退探针结论（Golden Page ④）**：`not_tested`

## 1. 触发钩子与黄金 UTG 页面捕获汇总

- 本次探索未触发 `HOOK_A11Y_SETTINGS` / `HOOK_APP_DETAILS`。

## 3. 逐步骤 Entry → Hook 完整动态 UTG 轨迹（含 Android XML + 鸿蒙 JSON）

| 步号 | 当前包 / Activity | 触发钩子 | 元素数 | 文本密度 / 需OCR | Agent 动作 | 双格式 Layout |
|---:|---|---|---:|---|---|---|
| 1 | `com.akbjmrnec.wiuvhfydb` / `InioawndOIADNwaiond` | `-` | 2 | 23 / 是 | `terminate` → App flow triggered the Accessibility prompt and opened  | `step_01_layout.xml` + `step_01_layout_harmony.json` |

## 4. 各步骤原始界面文本摘录

- **Step 1 (`com.akbjmrnec.wiuvhfydb/InioawndOIADNwaiond`)**: `QR Code Scanner: Add-On`

## 中文逐页引导链路解读

> **全链路总结**：该应用以“QR Code Scanner: Add-On”伪装为扫码插件入口，随后触发无障碍权限提示并跳转系统无障碍设置页；探针在该步终止，未观察到通知横幅或遮罩。

![全流程中文标注连环画](./utg_storyboard.png)

**捕获到的诱导/说明话术（中译）**：
- 英文 -> “二维码扫描器：附加组件”（Step 1 页面，伪装为扫码插件入口）

| 帧序 | 页面阶段 | 中文界面与交互说明 | 截图 |
|---:|---|---|---|
| 1 | **Step 1: InioawndOIADNwaiond** | Step 1 为伪装成“QR Code Scanner: Add-On”的扫码插件入口页；操作触发无障碍权限提示并跳转系统无障碍设置，本步终止，无通知横幅/遮罩。 | `step_01_action.png` |
