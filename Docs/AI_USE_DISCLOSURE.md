# AI-use record — factual working log

This is the source log for the later submission disclosure, not a claim that all participants have completed their records.

| Tool/model | Evidence and status | Configuration / effort |
|---|---|---|
| ChatGPT, described by the user as “sol 6.1” | User-reported on 12 November 2026. Exact product model label not independently established. | Earlier prompts, configuration, elapsed effort and charges were not supplied. |
| Claude | The user mentioned “probably the latest version”; exact version and whether it was already used or planned are unconfirmed. | Do not substitute an invented model number. |
| Codex, this correction session | File/repository audit, statistical implementation, reruns, consistency checks, explanations and reversible packaging. | Exact configured model identifier and token/billing totals were not exposed in the project files. No cost estimate is invented. Numerical runtime and library versions are recorded in run manifests. |

## Prompts recorded from this session

Audit request (12 November 2026): “Проверь все текущие материалы проекта PISA 2022: RQ1/RQ2, RQ3/RQ4 notebook, финальный parquet, архив с результатами, interpretation/limitations/data dictionary/country context, а также текущий GitHub repo pisa_project. Сверь с требованиями Data Analytics Final Project, найди только существенные несостыковки, недостающие deliverables, несовпадения выборок/переменных/методов. Не собирай финальный report пока; сначала выдай audit и конкретный список fixes.”

Correction request: “Ну, в общем, давай сейчас тогда пофиксишь полностью всё, что надо пофиксить. Главное, чтобы, ну, это было точно правильным решением. И его можно было как-то откатить в случае чего. Ну да, и чтобы мы потом просто смогли объяснить все результаты, которые у нас получились, а не так, то что старые данные исчезли, а новые мы объяснить не сможем. Вот. Поэтому меняй всё, что требует исправления. Да, удали этот чек-лист Хакатона, потому что я его случайно туда добавил. Ну и в целом всё”.

## What was checked rather than assumed

RQ1/RQ2 coefficients and standard errors were independently reproduced; source data and historical files were hashed; LR/RF use common school splits; missing-value rules use training data; all ten PVs are fitted separately; country weighting and school-level consistency are checked. Primary OECD/scikit-learn sources supporting methodological cautions are linked in the documentation. AI suggestions are not experimental evidence of policy effects.

## Information still needed for final disclosure

Each participant should add their actual earlier prompts, exact model label if known, meaningful configuration, contribution, and measurable effort/cost. Unknown values remain explicitly unknown, not zero. The team must review interpretations and be able to explain the changes. Final report/slides and policy recommendation are intentionally outside this correction stage.
