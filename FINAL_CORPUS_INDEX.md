# 移动端无障碍权限诱骗研究 · 三源统一融合总目录（Master Corpus Index）

本索引将本项目全部 **静态代码逆向（Source B）**、**动态 GUI-Owl 无损 UTG 实测（Source A）**、**国内外公开威胁情报与安全博客实战案例（Source C）**、**本地 418 样本集（git-ignored）** 以及 **鸿蒙端侧轻量级裁剪消融实验** 融合为一套结构清晰、一一对应、可一键增量刷新的完整研究目录。

---

## 一、三源融合总目录地图

```text
无障碍权限诱导攻击/  (同步映射至公开仓库 github_repo_release/)
│
├── FINAL_CORPUS_INDEX.md                           <-- 本统一总入口
│
├── 【核心综合研究文档】
│   ├── 诱导用户开启无障碍行为模式清单.md              <-- 34 条全谱系模式（25 静态 + 9 动态/情报补盲）、6 大诱导原型与首启不暴露补全矩阵
│   ├── 无障碍权限诱骗三源融合话术与手法全景库.md      <-- L0–L4 五级隐蔽度分层 + 1,200+ 条 8 语种三源融合实证话术库
│   ├── 鸿蒙端侧纯UTG轻量级裁剪方案与消融分析.md       <-- 基于无损鸿蒙 JSON 的 P0→P4 消融（625 KB → 2.66 KB / -99.6% / 通知信号 11.8%→100%）
│   ├── Android无障碍权限诱骗样本分析与正邪对照报告.md  <-- 跨十年（2014–2026）1,769 APK 正邪对照总报告
│   ├── 移动端无障碍权限诱骗机理与UTG检测方案研究.pptx  <-- 27 页学术研究汇报 PPT
│   └── fused_a11y_inducement_kb.json               <-- 机器可读三源融合结构化知识库（供分类器/实验直接加载）
│
├── 【Source A · 动态 GUI-Owl 无损 UTG（与 418 报告同名一一对应）】
│   ├── dynamic_utg_418/
│   │   ├── INDEX_418_UTG.md                        <-- 418 份报告 ↔ 样本 ↔ 动态 UTG 一一对应总表
│   │   ├── malicious/<report_stem>/                <-- 每应用含：原图截屏 + 点击标注 + Android XML + 鸿蒙 JSON + 通知遥测 + 中文连环画
│   │   └── benign/<report_stem>/                   <-- 70/70 全部良性对照无损 UTG
│   └── gui_agent/                                  <-- 静态引导动态 GUI-Owl Agent + Android XML→鸿蒙 JSON 转换器 + 中文连环画源码
│
├── 【Source B · 静态 APKAudit 深度代码审计（补齐首启不暴露样本）】
│   └── per_app_reports/
│       ├── INDEX.md                                <-- 418 份「一应用一文件」代码逆向索引
│       ├── REPORT_APK_UTG_MANIFEST.csv             <-- 报告 ↔ 本地 APK ↔ SHA-256 ↔ 动态 UTG 映射总表
│       ├── malicious/<report_stem>.md              <-- 348 份恶意代码逆向报告（覆盖 82/82 全家族）
│       └── benign/<report_stem>.md                 <-- 70 份开源良性对照报告（覆盖 11/11 全品类）
│
├── 【Source C · 公开威胁情报、警方通报与安全博客（18 份一案一档）】
│   └── threat_intel_cases/
│       ├── 国内外公开威胁情报与涉诈实战案例集.md     <-- 18 案例全景研判汇总
│       ├── threat_intel_cases.json                 <-- 结构化情报 JSON（含话术、杀伤链、UTG 信号与鸿蒙映射）
│       └── cases/                                  <-- 一案一档：INTEL_CN_01..06（银联会议/中银会议/RustDesk滥用/深夜数币/假反诈/受限解锁）
│                                                       + INTEL_GL_01..12（SecuriDropper/Chameleon/Vultur/Brokewell/Crocodilus/ToxicPanda/PlayPraetor/Anatsa/GodFather虚拟化/Snowblind/FakeCall/RatOn+SuperCardX/PixPirate）
│
├── 【本地样本库（严格 git-ignored，绝不提交公开仓库）】
│   └── samples/
│       ├── README.md                               <-- 目录说明（唯一提交到仓库的文件）
│       ├── malicious/<report_stem>.apk             <-- 348 个与报告同名的恶意 APK（仅本地）
│       └── benign/<report_stem>.apk                <-- 70 个与报告同名的良性 APK（仅本地）
│
└── 【一键同步与刷新流水线】
    └── scripts/
        ├── sync_418_utg_folders.py                 <-- 将最新动态 UTG 一键同步至 dynamic_utg_418/（1-to-1 同名零额外占盘）
        ├── build_fused_rhetoric_kb.py              <-- 一键重算三源融合话术全景库 + 18 份一案一档情报报告 + JSON 知识库
        └── analyze_utg_pruning.py                  <-- 一键重跑全量无损鸿蒙 JSON 的 P0→P4 裁剪消融实验
```

---

## 二、首启不暴露与生态盲区的「三源互补分工」

1. **为什么需要 Source B（静态审计 418 份）补 Source A（动态 UTG）？**
   - 动态首启中因登录墙（35 例）、老旧 SDK 装不上（33 例）、后台潜伏/闪退（28 例）、深层功能触发（18 例）或离线 C2 阻断（7 例）未触发无障碍页的样本，全部由 Source B 静态代码逆向补齐，并直接回收 **787 条 `[STATIC_HIDDEN]` 隐藏诱导原文**、**74 例受限设置教学分支** 与 **66 例后台定时重拉链路**。
2. **为什么需要 Source C（18 份国内+全球实战情报/博客）补 Source A & B？**
   - 专门补齐海外样本池缺失的 **国内「银联会议 / 中银会议 / 抖音会议 / N+会议 / 国密会议」电话带外社工**、**合法远控软件滥用（RustDesk / 向日葵 / ToDesk）的端侧防误报红线**、**官方商店干净壳多日延迟 + 地理围栏热更（Anatsa）**、**Session 安装器绕受限设置（SecuriDropper / BugDrop / Zombinder）** 以及 **2024–2026 新型对抗（GodFather 虚拟化、Snowblind `seccomp`、FakeCall 拨号劫持、RatOn / NGate / SuperCard X NFC 中继、`TYPE_ACCESSIBILITY_OVERLAY` 透明点击劫持）**。
3. **为什么需要 Source A（动态 UTG 全量无损采集）补 Source B & C？**
   - 专门打穿静态不可见的强加壳/密文载荷（`TeaBot`、`Alien`、`FluBot`），实测抓出静态和纯控件树均会漏掉的 **顶部通知横幅压栈（46/88 恶意）**、**桌面持续 Toast**、**70/70 良性零误报基准**，并为 **鸿蒙 `uitest dumpLayout` JSON 的 P0→P4 轻量化裁剪实验** 提供真实无损语料。
