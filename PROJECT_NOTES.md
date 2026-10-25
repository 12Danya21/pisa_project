# Project A — PISA 2022

## Main question
Which school-level investment is most strongly associated
with student performance after accounting for family background?

## Countries
Germany
France
Poland
Estonia
Italy
Spain
Ukraine

## Research Questions

RQ1
Which school factors correlate with student performance:
equipment, class size, teacher qualification?

RQ2
What happens after controlling for ESCS?

RQ3
Do linear regression and Random Forest agree?

RQ4
Do countries cluster into recognizable school-system types?

## Variables

Outcome:
PV1MATH–PV10MATH

School factors:
CLSIZE — class size
EDUSHORT — educational resource shortage
PROATCE — teacher certification/qualification proxy
...

Control:
ESCS

Weight:
W_FSTUWT

## Decisions / Issues

1. Use PISA 2022 only.
2. Preserve all 10 plausible values.
3. Apply survey weights.
4. Need justification of school-factor proxies from codebook.
5. Need to document missing-data treatment.

## Results

RQ1:
Waiting for regression.

RQ2:
Waiting for regression + ESCS.

RQ3:
Waiting for Random Forest.

RQ4:
Waiting for clustering.

## Interpretation

To be completed jointly with Alex.

## Limitations

- Observational data / no causal claim
- Survey weights
- Plausible values
- PISA 2022 response-rate issues
- Missing data
- Variable proxies
