# QUIC Traffic Classification

Research code for experiments on encrypted QUIC application traffic classification under temporal shift. The repository organizes the five notebook passes, selected Pass 5 result tables, a reproducibility audit, and the current manuscript source/PDF.

> **Reproducibility status:** the repository is a research artifact, not a one-click, clean-room reproduction package yet. The notebooks reference Kaggle datasets and artifacts by `/kaggle/input/...` paths. Access to the relevant CESNET QUICEXT-25 data and the author-published Kaggle input datasets is required. The Pass 3 neural result is a descriptive external reference: the saved neural checkpoint and per-flow test predictions/probabilities were not present in the Pass 5 artifact archive, so that result was not independently recomputed in the Pass 5 audit.

## Research workflow

| Pass | Role | Notebook |
|---|---|---|
| 1 | Streaming preprocessing statistics and metadata | [`notebooks/pass-1.ipynb`](notebooks/pass-1.ipynb) |
| 2 | TFRecord dataset construction | [`notebooks/pass-2.ipynb`](notebooks/pass-2.ipynb) |
| 3 | Neural model selection, training, stacking, and evaluation | [`notebooks/pass-3.ipynb`](notebooks/pass-3.ipynb) |
| 4 | Separate/alternative tree-baseline experiment and feature-schema checks | [`notebooks/pass-4.ipynb`](notebooks/pass-4.ipynb) |
| 5 | Budgeted LightGBM and XGBoost-OvR baselines, calibration/stacking, May 2025 evaluation, and paired day-block bootstrap | [`notebooks/pass-5.ipynb`](notebooks/pass-5.ipynb) |

The passes should not be assumed to be a fully automated linear pipeline. Pass 4 is an alternative experiment, and Pass 5 reads the source HDF5 dataset directly rather than consuming the Pass 2 TFRecords. Inspect each notebook's configuration and input requirements before running it.

## Reported Pass 5 results

The full May 2025 known-class test population contains 2,359,061 flows across 31 calendar-day blocks. Training data span June 2024–March 2025; April 2025 is used for development/calibration partitions; May 2025 is the future-month test period.

| Model | Accuracy | Macro-F1 | Weighted-F1 | ECE-10 | Reported throughput |
|---|---:|---:|---:|---:|---:|
| LightGBM + April logistic-regression stacker | 0.878906 | 0.753390 | 0.877394 | 0.015418 | 1,254.68 flows/s |
| XGBoost one-vs-rest + April logistic-regression stacker | 0.842685 | 0.696595 | 0.839968 | 0.014053 | 6,235.50 flows/s |

Throughput excludes preprocessing and HDF5 I/O. Calibration error is expected calibration error with 10 bins, as computed by the experiment. See [`results/`](results/) for the detailed result tables and JSON manifests, and [`docs/pass5-artifact-audit.md`](docs/pass5-artifact-audit.md) for the audit scope and limitations.

The Pass 5 paired daily-block bootstrap compares the two tree models over the 31 May day blocks (1,000 replicates). The LightGBM-minus-XGBoost-OvR macro-F1 difference is 0.056795, with a 95% interval of [0.053128, 0.060737]. This is within-May daily-block uncertainty; it is not an estimate of month-to-month or cross-network uncertainty.

The earlier neural reference reports accuracy 0.932417 and macro-F1 0.838613 in Pass 3. These values are **descriptive only** and are not a controlled inferential comparison against Pass 5 tree results because the required neural predictions/checkpoint were not available in the Pass 5 archive for independent recomputation.

## Kaggle notebooks

The public Kaggle notebooks are complementary executable views of the workflow:

- [Pass 1](https://www.kaggle.com/code/yahiaa1/pass-1)
- [Pass 2](https://www.kaggle.com/code/yahiaa1/pass-2)
- [Pass 3](https://www.kaggle.com/code/yahiaa1/pass-3)
- [Pass 4](https://www.kaggle.com/code/yahiaa1/pass-4)
- [Pass 5](https://www.kaggle.com/code/yahiaa1/pass-5)

The GitHub copy is the version-controlled research artifact. When a manuscript is submitted, tag the exact repository revision used for the reported results and cite that version.

## Environment and execution

The intended environment is Kaggle, with GPU T4 x2 for the main neural and Pass 5 runs. The notebooks print or record some environment/package versions; use those recorded versions for exact reproduction. No universal `requirements.txt` is supplied because the notebook passes use different stacks and Kaggle's preinstalled CUDA/TensorFlow/PyTorch-related packages can be sensitive to version changes. See [`docs/reproducibility.md`](docs/reproducibility.md).

At minimum, make the required Kaggle input datasets available and verify that the configured paths exist before running. **Do not run Pass 2 before reviewing its cleanup cells:** it contains commands that remove intermediate files under `/kaggle/working` as part of its workflow. These are scoped to the Kaggle working directory but should still be reviewed.

## Data, privacy, and licensing

This repository does not redistribute the CESNET dataset. Obtain it through the dataset provider and comply with its access terms. The MIT license in this repository applies only to original repository code and documentation, not third-party datasets or artifacts. Before publishing, confirm that each Kaggle input dataset and all included results can be redistributed publicly.

## Limitations to keep in view

- The main tree test is one future month (May 2025); it does not establish multi-month or cross-network generalization.
- LightGBM reached the configured iteration cap, and most XGBoost OvR models reached or approached theirs. Higher-iteration sensitivity analysis remains a pre-submission gate.
- The 101-feature representation includes auxiliary statistics that may summarize the full flow. It should not be described as a strict first-30-packet online classifier without a prefix-only ablation.
- Tree inference throughput excludes preprocessing and HDF5 I/O.
- Neural-reference metrics lack independently verifiable per-flow predictions in the Pass 5 artifact bundle.

## Citation

Citation metadata is in [`CITATION.cff`](CITATION.cff). A DOI and paper citation can be added after the repository is released and the manuscript is finalized.

## Repository layout

```text
.
├── CITATION.cff
├── LICENSE
├── README.md
├── configs/
│   └── experiment_config.yaml
├── docs/
│   ├── pass5-artifact-audit.md
│   └── reproducibility.md
├── notebooks/
│   ├── pass-1.ipynb
│   ├── pass-2.ipynb
│   ├── pass-3.ipynb
│   ├── pass-4.ipynb
│   └── pass-5.ipynb
├── paper/
│   ├── QUIC_Traffic_Classification_Pass5_Final.tex
│   ├── QUIC_Traffic_Classification_Pass5_Final.pdf
│   ├── Pass5_Artifact_Audit.md
│   └── README.md
└── results/
```
