# Country Context — 14 Education Systems

**Owner:** Interpretation & Limitations Lead
**Purpose:** give meaning to the RQ4 clusters and to country differences in RQ1–RQ3. When countries group together, this table is where we look for the reason.
**Status:** Section A is computed from our data. Section B combines institutional knowledge with fields still to verify; anything marked *(verify)* must be checked against the sources listed at the bottom before it goes into the report.

---

## A. What our data says (weighted with `W_FSTUWT`, mean of 10 PVs)

| CNT | System | Students | Schools | Maths mean | Mean ESCS | % private (any) | Mean PROATCE | Mean CLSIZE | Mean EDUSHORT | SD of school ESCS |
|---|---|---|---|---|---|---|---|---|---|---|
| EST | Estonia | 6,392 | 196 | 510 | 0.15 | 5 | 0.77 | 22.5 | −0.13 | 0.44 |
| NLD | Netherlands | 5,046 | 154 | 493 | 0.26 | 45 | 0.86 | 24.4 | −0.56 | 0.45 |
| BEL | Belgium | 8,286 | 285 | 489 | 0.09 | 84 † | 0.92 † | 19.9 | −0.21 | 0.54 |
| POL | Poland | 6,011 | 240 | 489 | −0.10 | 7 | 0.88 | 28.3 | −0.37 | 0.54 |
| AUT | Austria | 6,151 | 302 | 487 | 0.07 | 0 ‡ | 0.86 | 22.2 | −0.48 | 0.57 |
| CZE | Czechia | 8,460 | 430 | 487 | −0.10 | 9 | 0.88 | 24.1 | −0.14 | 0.58 |
| FIN | Finland | 10,239 | 241 | 484 | 0.26 | 5 | 0.88 | 19.8 | −0.57 | 0.31 |
| SWE | Sweden | 6,072 | 262 | 482 | 0.33 | 20 | 0.83 | 24.0 | −0.63 | 0.39 |
| DEU | Germany | 6,116 | 257 | 475 | −0.13 | 3 | 0.88 | 24.3 | −0.07 | 0.59 |
| FRA | France | 6,770 | 282 | 474 | 0.00 | 21 | 0.83 | 29.4 | −0.39 | 0.65 |
| ESP | Spain | 30,800 | 966 | 473 | −0.03 | 30 | 0.90 | 25.8 | −0.29 | 0.48 |
| PRT | Portugal | 6,793 | 224 | 472 | −0.22 | 15 | 0.80 | 24.6 | 0.24 | 0.57 |
| ITA | Italy | 10,552 | 344 | 471 | −0.10 | 4 | 0.74 | 23.9 | −0.21 | 0.55 |
| QUR | Ukrainian regions | 3,876 | 164 | 441 | −0.35 | 2 | 0.69 | 24.7 | 0.91 | 0.51 |

† Belgium: `PROATCE` 48% imputed, `SCHLTYPE` 60% imputed. ‡ Austria: `SCHLTYPE` 100% imputed → the 0% is an artefact, not a fact.

**How to read "SD of school ESCS":** how different schools are in the social background of their students. High values (France 0.65, Germany 0.59, Czechia 0.58, Austria 0.57) mean advantaged and disadvantaged students are **sorted into different schools**. Low values (Finland 0.31, Sweden 0.39) mean schools are socially mixed. This is the variable most likely to explain why some countries show strong school-level "effects": in sorted systems, school resources travel together with student intake.

**Patterns worth noting already:**
- The Nordic and Baltic systems (FIN, SWE, EST) have the lowest social sorting between schools.
- The early-tracking systems (DEU, AUT, CZE) plus France have the highest.
- Ukrainian regions stand out on every resource indicator: highest equipment shortage (0.91), lowest teacher certification (0.69) and lowest scores. If kept, QUR will likely form a cluster of one.
- Class size is largest in France (29) and Poland (28), smallest in Finland and Belgium (20). Note that Poland scores well despite large classes.

Code to reproduce Section A is in `notebooks/` *(add the notebook name once committed)*.

---

## B. Institutional features (to complete and verify)

| CNT | Age of first tracking *(verify)* | Type of system | Private-school model | COVID: school closure length 2020–21 *(fill from Vol II)* | OECD data-quality flag 2022 *(verify)* | Notes |
|---|---|---|---|---|---|---|
| AUT | 10 | Early tracking | Mostly public | | | Our SCHLTYPE unusable |
| BEL | 12 | Tracking (community-specific: Flemish, French, German) | Large **government-funded** private (mainly Catholic) sector | | | Three separate systems pooled as one |
| CZE | 11 | Early tracking (selective gymnázia) | Mostly public | | | |
| DEU | 10 (most Länder) | Early tracking, federal (16 Länder) | Mostly public | | | ESCS 13% missing |
| EST | 16 | Comprehensive | Mostly public | | | Highest scores in our sample |
| ESP | 16 | Comprehensive, regionally governed | Large *concertada* (government-funded private) sector | | | Oversampled by region → 25% of rows |
| FIN | 16 | Comprehensive | Almost all public | | | |
| FRA | 15 | Comprehensive *collège*, then tracks | Large *privé sous contrat* (government-funded) sector | | | Highest social sorting |
| ITA | 14 | Tracks from upper secondary (licei, tecnici, professionali) | Mostly public | | | Strong North–South gap |
| NLD | 12 | Early tracking (VMBO / HAVO / VWO) | Majority of schools are government-funded private, but legally equal to public | | **Likely flagged** — low response rates *(verify)* | |
| POL | 15 | Comprehensive (8-year primary since 2017 reform) | Mostly public | | | |
| PRT | 15 | Comprehensive | Government-dependent private segment | | | |
| QUR | 15 | Comprehensive | Mostly public | | Only 18 regions; tested during the war | Not an EU system |
| SWE | 16 | Comprehensive | Large share of tax-funded independent schools (*friskolor*) | Lower secondary largely stayed open (Vol II names Sweden among limited-closure systems) | | |

### How to fill the remaining columns

1. **Age of first tracking** → Eurydice, *The structure of European education systems* (interactive diagrams). Look for the age at which students first enter different school types. Cross-check with OECD *Education at a Glance*, indicator on "age at first selection".
2. **COVID closures** → *PISA 2022 Results, Volume II*, chapter "Learning during and from disruption" and its tables on the duration of school closures reported by students and principals.
3. **Data-quality flags** → *PISA 2022 Results, Volume I*, Reader's Guide and Annexes A2 and A4. Countries that did not meet one or more sampling standards are marked with an asterisk (\*) in every table.
4. **Private-school model** → describe in words; the numbers in Section A come from our own data.

---

## C. Why this table matters for interpretation

- **RQ1/RQ2:** in early-tracking systems, a school's resources are tied to which track it serves. A "school effect" there may be a **track effect**.
- **RQ3:** if the Random Forest gives high importance to `CNT` or `SCH_ESCS`, the institutional features above are the likely explanation.
- **RQ4:** our expectation before clustering is three groups: (1) comprehensive, socially mixed (FIN, SWE, EST, possibly POL); (2) early-tracking, socially sorted (DEU, AUT, CZE, NLD, BEL); (3) Southern European with mid-level sorting and large government-funded private sectors (ESP, ITA, PRT, FRA); plus QUR as an outlier. If the clusters do **not** look like this, that is itself a finding worth explaining.
