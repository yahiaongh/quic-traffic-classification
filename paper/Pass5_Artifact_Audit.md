# Pass 5 artifact audit — manuscript update

## Integrity checks completed

- Loaded the complete experiment ZIP (106 archive entries) and verified that both saved prediction vectors align with the 2,359,061 test labels.
- Recomputed accuracy, macro-precision, macro-recall, macro-F1, and weighted-F1 directly from the saved prediction arrays and labels. The recomputed values match the saved metric JSON files to numerical precision.
- Verified that the daily confusion-matrix arrays contain 31 day blocks and that `may_test_day_ids.npy` spans IDs 0–30.
- Verified that `pass5_per_class_comparison.csv` contains all 50 classes and provides current per-class metrics for both tree models plus descriptive neural-reference F1 values.
- Used the Pass 3 notebook source to document the selected neural Model A (SE-residual 1D CNN), Model C (lightweight Transformer), and logistic-regression stacking rule.

## Recomputed May 2025 tree metrics

| Model | Accuracy | Macro precision | Macro recall | Macro-F1 | Weighted-F1 | Matches stored JSON |
|---|---:|---:|---:|---:|---:|---|
| LightGBM | 0.8789060563 | 0.8144017003 | 0.7274527535 | 0.7533901744 | 0.8773937975 | True |
| XGBoost-OvR | 0.8426848649 | 0.7716202296 | 0.6642489722 | 0.6965948073 | 0.8399677018 | True |


## Statistical comparison

The paired day-block bootstrap uses 31 May calendar-day blocks and 1,000 replicates. LightGBM minus XGBoost-OvR macro-F1 is 0.056795, with a 95% interval [0.053128, 0.060737]. This interval is interpreted as within-May daily-block uncertainty, not as month-to-month or cross-network uncertainty.

## Neural-reference status

The supplied Pass 3 notebook's printed aggregate report matches the external neural summary at the reported precision (accuracy 0.9324; macro-F1 0.8386; weighted-F1 0.9320; ECE 0.0096), and the notebook contains the Model A/Model C builder code and the April selection procedure. However, the Pass 5 manifest still marks this row as an external point estimate and warns that provenance must be reconciled. The archive does not include the saved neural checkpoint or per-flow neural probabilities/predictions. The manuscript therefore documents the architecture and scores but does not report neural bootstrap intervals or make inferential claims against the tree baselines.

## Remaining pre-submission gates

1. Release the exact Pass 3 neural checkpoint, saved predictions/probabilities, class mapping, and inference configuration—or retrain/restore it under a frozen manifest—and independently regenerate its May metrics.
2. Extend tree training beyond the configured iteration caps in a validation-only sensitivity experiment: LightGBM reached 260 rounds and most XGBoost binary models reached/approached the 209-round cap.
3. Add at least one additional future-month evaluation if the dataset permits; May alone cannot establish long-term temporal robustness.
4. Evaluate a strict prefix-only feature set that removes full-flow auxiliary statistics before claiming early/online classification.
5. Publish code, environment lock/versions, and artifact hashes with a DOI or public repository URL.
6. Reformat to the chosen venue's official template and enforce its page/reference limits after the target venue is selected.

This audit confirms internal consistency between the supplied tree predictions, labels, and saved tree metric JSONs; it does not constitute an independent rerun of model training.
