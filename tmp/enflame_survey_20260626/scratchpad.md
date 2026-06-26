# Enflame survey scratchpad 20260626

## Route
DSA (not GPGPU). Chips: 邃思 DTU/GCU. Software: TopsRider 驭算.

## Generations
- Gen1: T10/T11 train, i10 infer (2019-2020)
- Gen2: 2.0 T20/T21 train, 2.5 i20 infer (2021)
- Gen3: 320 S60 infer MCM GDDR6 (2024)
- Gen4: 400 L600 train+infer FP8 (2025)
- Gen5/6: IPO 2027/2029

## Key corrections
- Moark ef_gpu wrongly says S60 = 2021 / 邃思2.0 → use Gen3 320 2024
- GCU-CARA (Gen2) vs GCU-CARE (Gen3 S60 docs)

## Deliverables
- Report: contexts/survey_sessions/enflame_gcu_survey_20260626.md
- Diagrams: enflame_gcu_{hw_generations,chip_architecture,software_stack}.{excalidraw,png}
