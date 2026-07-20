<!--
provenance:
  file: openpriors/docs/founding-request.md
  role: archived founding request, historical record; authority superseded per constitution
  version: 2026-07-18 (original text 2026-06) (authoritative history: LOG.md and git once committed)
  generator: Claude (Fable 5, claude-fable-5) via claude.ai
  conversation: metaproof-founding-2026-07 — https://claude.ai/chat/65ec034b-6d86-4ccc-b995-70fbb3c22e74
  archived: 2026-07-20
-->

# docs/founding-request.md — the founding request (archived verbatim, 2026-06)

> Archived for provenance. Authority: superseded by CLAUDE.md's Precedence section
> (Amendment 001); retained clauses are listed there. This document is historical record,
> not standing instruction.

帮我在OpenPriors里写一个generic skills workflow，然后选择性能与计算效率最大化且易持续开发、易拓展、易audit的实现工具、数据格式与开发流程，把以下几份文本作为test case，完成下述几步：

1. 把它的tex source和html文件提取出来（if available）
2. 去除source file格式冗余
3. 整理这个文本中起到结构分割作用、多次复现的data class，如章节/定理/公式/文献引用等，
4. 根据以上的数据格式进行合理的nested, hierarchical拆分存储。

- https://arxiv.org/abs/2006.06138
- Repo ´/Imports/decomposer-sample-test-cases´ 下的全部内容

开发要求：

【开发内容上】
- 每一步都用统一且informative的格式储存在repo中，包含完整meta data 与开发 trajectories
- 开始时可以进行case by case的special case设计。最后应aim at提炼出不限定文本的领域、格式、任务类型的通用引导流程
- 设计出来的workflow中每一步必须同时包含论证、构建与独立检验的三个阶段，且全部基于当前任务所对应的fundamental / motivational principles （至于这些principle该怎么从不同的且潜在未知的任务中提取出来，还需要你系统性地思考、设计、实验、论证）
- 每一步在整体和细节的设计理念和实现手段上都先进行尽可能全面的lit-review，吸收学习对比反思，充分了解、利用现有工具，去伪存真，推陈出新。

【开发手段上】
- 整个workflow中需要自然语言理解能力的步骤需要使用Claude Code session内部由Max plan cover的sub-agents，无API call
- 同步记录开发过程，决策，经验
- 将开发与拓展流程本身整理成结构化的工具指南，并重复验证最终决策的效益（性能vs资源），从尽可能多的方面交叉比对，系统论证
- 你可以使用可及范围内的任何一种在20× Max plan基础上Total额外成本<$5的工具，包括但不限于各种embedding，agentic programming framework，formal language package，Github Copilot，Issues/PR features，Actions workflows / automation bots。
- 你拥有完整的auto create/merge OpenPriors repo下任意branch的权限，以及root settings的主动修改权限。请合理规划任务层次、分支、嵌套与迭代关系，合理分配独立开发空间、步调、监督机制，与安全备份、冗余。

---

本任务为下一步终极目标服务：

开发一个形式化表征文本概念、推理链条的package，可以选择基于(object, attribute, relation) 的node/edge拆分结构，或者你推荐的任何一种适合完成此类任务的结构。

---

请尽可能24h不间断地独立推进该任务的所有阶段、所有步骤，主动搜索信息、记录信息、搜集资料、填补未知，在推导出不可调和、不可避免的逻辑矛盾（并充分论证其绝对不可避免性）之前不诉诸用户。
