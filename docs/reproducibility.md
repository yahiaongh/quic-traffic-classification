# Reproducibility and execution notes

## Before execution

1. Use the public Kaggle notebooks as the intended environment reference.
2. Attach the exact dataset and metadata Kaggle inputs referenced by each notebook. Input paths are currently author/workspace-specific and are not automatically rewritten by this repository.
3. Review the notebook's first configuration cells and compare them with the reference values in `configs/experiment_config.yaml`.
4. Record the Kaggle notebook version, input dataset versions, package versions, accelerator, and output artifact hashes for any new run.
5. Keep `DRY_RUN=False` only for a full experiment. Diagnostic/dry-run outputs must not be substituted for the paper's reported metrics.

## Pass dependencies

- Pass 1 reads the source dataset and writes preprocessing statistics/metadata under `/kaggle/working`.
- Pass 2 reads source data plus metadata and creates TFRecord data. It includes cleanup commands scoped to `/kaggle/working`; review these before execution.
- Pass 3 consumes the TFRecord dataset and refers to a separate checkpoint/parameter dataset for HPO configuration. The notebook is not self-contained unless those inputs are attached.
- Pass 4 is a separate tree-baseline experiment with its own configuration and result directory.
- Pass 5 reads the source HDF5 data directly, uses the April development period and May 2025 test period, and writes its results to a Kaggle working directory. It does not require Pass 2 TFRecords as its direct input.

Do not assume all five notebooks must be run sequentially. Use the specific dependency path documented above.

## Reproduction status and result provenance

The Pass 5 result tables were extracted from the supplied `pass5_fair_full_run_complete.zip`. The artifact audit verified that saved tree predictions aligned with the test labels and that recomputed aggregate metrics matched the stored metric JSONs. This audit did not independently rerun model training.

The reported neural metrics are transcribed from the earlier Pass 3 report and are descriptive only. The Pass 5 artifact archive did not include the neural checkpoint or per-flow neural predictions/probabilities required for independent recalculation.

## Remaining work before claiming full reproducibility

- Freeze and document exact input dataset versions and access instructions.
- Add a dependency lock/environment export for each pass after verifying a clean run.
- Restore or regenerate neural checkpoints and per-flow predictions if neural/tree inferential comparisons are needed.
- Run the higher-iteration tree sensitivity experiment.
- Test a prefix-only feature ablation if making early/online classification claims.
- Evaluate at least one additional future month if the dataset and compute budget allow.
