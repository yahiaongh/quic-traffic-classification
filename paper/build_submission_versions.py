#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "paper" / "QUIC_Traffic_Classification_Pass5_Final.tex"
OUT = ROOT / "pdfs"
OUT.mkdir(exist_ok=True)
source = SRC.read_text(encoding="utf-8")
title = re.search(r"\\title\{([\s\S]*?)\}\s*\\author", source).group(1).strip()

abstract = (
    "Encrypted QUIC traffic limits payload-based identification, while temporal change and class imbalance complicate application classification. "
    "We evaluate a 50-class closed-set task on the medium CESNET-QUICEXT-25 variant using a chronological protocol: 27,727,267 flows from "
    "June 2024--March 2025 for training, disjoint April 2025 partitions for development and stacking, and all 2,359,061 known-class flows "
    "from May 2025 for testing. The 101-feature representation combines the first 30 packet timing/direction/size triples with 11 auxiliary "
    "flow statistics; some auxiliary variables are full-flow summaries, so this is not strict first-30-packet online classification. "
    "Under the shared protocol, LightGBM with an April-trained logistic stacker achieves 0.8789 accuracy and 0.7534 macro-F1, compared "
    "with 0.8427 and 0.6966 for XGBoost one-vs-rest. A paired bootstrap over 31 test-day blocks estimates a 0.0568 macro-F1 advantage "
    "(95\\% interval 0.0531--0.0607). XGBoost is 4.97 times faster in the measured model-only benchmark. Neural results remain an external, "
    "non-inferential reference because its checkpoint and per-flow predictions are unavailable."
)
keywords = "QUIC; encrypted traffic classification; temporal generalization; CESNET-QUICEXT-25; LightGBM; XGBoost; one-vs-rest; probability stacking; calibration; day-block bootstrap"

doc = source.split(r"\begin{document}", 1)[1].rsplit(r"\end{document}", 1)[0]
doc = re.sub(r"^\s*\\maketitle\s*", "", doc, count=1)
doc = re.sub(r"\\begin\{abstract\}[\s\S]*?\\end\{abstract\}", "", doc, count=1)
doc = re.sub(r"\\noindent\\textbf\{Keywords:\}[\s\S]*?(?=\\section\{Introduction\})", "", doc, count=1)
doc = re.sub(r"\\bibliographystyle\{plain\}[\s\S]*?\\end\{thebibliography\}\s*$", "", doc, count=1)
doc = doc.strip()

# Convert the fifty-class longtable to a full-width float for two-column classes.
lm = re.search(r"\\begin\{longtable\}\{lrrrr\}([\s\S]*?)\\end\{longtable\}", doc)
if lm:
    inner = lm.group(1)
    cm = re.search(r"\\caption\{([\s\S]*?)\}\\label\{([^}]+)\}\\\\", inner)
    if not cm:
        raise RuntimeError("Could not parse the per-class longtable caption.")
    cap, lab = cm.group(1), cm.group(2)
    inner = inner[:cm.start()] + inner[cm.end():]
    inner = re.sub(r"\\endfirsthead\s*|\\endhead\s*", "", inner)
    replacement = (
        r"\begin{table*}[t]" + "\n" + r"\centering" + "\n" +
        r"\caption{" + cap + "}" + r"\label{" + lab + "}" + "\n" +
        r"\small" + "\n" + r"\begin{tabular}{lrrrr}" + inner +
        r"\end{tabular}" + "\n" + r"\end{table*}"
    )
    doc = doc[:lm.start()] + replacement + doc[lm.end():]

# Set each TikZ diagram as a two-column float and retain vector artwork.
def widen_figure(m):
    block = m.group(0)
    block = block.replace(r"\begin{figure}[ht]", r"\begin{figure*}[t]")
    block = block.replace(r"\end{figure}", r"\end{figure*}")
    block = block.replace(r"0.98\linewidth", r"0.98\textwidth")
    return block
doc = re.sub(r"\\begin\{figure\}\[ht\][\s\S]*?\\end\{figure\}", widen_figure, doc)
doc = doc.replace(r"\begin{table}[ht]", r"\begin{table}[t]")
doc = doc.replace(r"\begin{figure}[ht]", r"\begin{figure}[t]")

availability = r"""\section*{Data and Code Availability}

The manuscript source, experimental notebooks, model configurations, result tables, evaluation manifests, audit information, and reproducibility documentation are publicly available at:
\url{https://github.com/yahiaongh/quic-traffic-classification}

The repository does not redistribute the CESNET-QUICEXT-25 dataset. That dataset is distributed separately by its original providers (DOI: \url{https://doi.org/10.5281/zenodo.17249078}) and remains subject to their access and use conditions. The current repository snapshot does not contain a restorable checkpoint or per-flow predictions for the external neural reference; its reported neural results are therefore retained only as descriptive results, as explained in the paper.
"""
blind_availability = r"""\section*{Data and Code Availability}

The manuscript source, experimental notebooks, model configurations, result tables, evaluation manifests, audit information, and reproducibility documentation are maintained in a public project repository. The direct repository URL is withheld from this double-blind review copy to avoid exposing author identity; it should be restored in the camera-ready version. The CESNET-QUICEXT-25 dataset is distributed separately by its original providers (DOI: \url{https://doi.org/10.5281/zenodo.17249078}) and is not redistributed in the project repository. The current repository snapshot does not contain a restorable checkpoint or per-flow predictions for the external neural reference; its reported results are descriptive only.
"""
doc_ifip = re.sub(r"\\section\*\{Data and Code Availability\}[\s\S]*$", blind_availability, doc)
doc_tnsm = re.sub(r"\\section\*\{Data and Code Availability\}[\s\S]*$", availability, doc)

bib = r"""@misc{cesnet-quicext25,
  author = {Jan Luxemburk and Karel Hynek and Jonas M\"ucke},
  title = {CESNET-QUICEXT-25: A Year-Long QUIC Traffic Dataset with EXTended Attributes},
  year = {2025}, publisher = {Zenodo}, doi = {10.5281/zenodo.17249078},
  url = {https://doi.org/10.5281/zenodo.17249078}
}
@article{waitingforquic,
  author = {Jonas M\"ucke and Michal Nawrocki and Robert Hiesgen and Paul Sattler and Julian Zirngibl and Georg Carle and Jan Luxemburk and Thomas C. Schmidt and Matthias W\"ahlisch},
  title = {Waiting for QUIC: Passive Measurements to Understand QUIC Deployments},
  journal = {Proceedings of the ACM on Networking}, volume = {3}, number = {CoNEXT4},
  pages = {Article 41}, year = {2025}, doi = {10.1145/3768988}
}
@misc{cesnet-datazoo,
  author = {{CESNET}}, title = {cesnet-datazoo: A Python Library for CESNET Traffic Datasets},
  url = {https://github.com/CESNET/cesnet-datazoo}, year = {2025}
}
@misc{cesnet-models,
  author = {{CESNET}}, title = {cesnet-models: Reference Transforms and Models for CESNET Traffic Datasets},
  url = {https://github.com/CESNET/cesnet-models}, year = {2025}
}
@article{rezaei2019,
  author = {Saeed Rezaei and Xiali Liu},
  title = {Deep Learning for Encrypted Traffic Classification: An Overview},
  journal = {IEEE Communications Magazine}, volume = {57}, number = {5},
  pages = {76--81}, year = {2019}, doi = {10.1109/MCOM.2019.1800819}
}
@article{sharma2025survey,
  author = {Amit Sharma and Ali H. Lashkari},
  title = {A Survey on Encrypted Network Traffic: A Comprehensive Survey of Identification/Classification Techniques, Challenges, and Future Directions},
  journal = {Computer Networks}, volume = {257}, pages = {110984}, year = {2025},
  doi = {10.1016/j.comnet.2024.110984}
}
@misc{visquic2024,
  author = {B. Gahtan and R. J. Shahla and A. M. Bronstein and R. Cohen},
  title = {Exploring QUIC Dynamics: A Large-Scale Dataset for Encrypted Traffic Analysis},
  year = {2024}, eprint = {2410.03728}, archivePrefix = {arXiv}
}
@article{quicensemble2023,
  author = {S. Almuhammadi and A. Alnajim and M. Ayub},
  title = {QUIC Network Traffic Classification Using Ensemble Machine Learning Techniques},
  journal = {Applied Sciences}, volume = {13}, number = {8}, pages = {4725},
  year = {2023}, doi = {10.3390/app13084725}
}
@inproceedings{lightgbm,
  author = {Guolin Ke and Qi Meng and Thomas Finley and Taifeng Wang and Wei Chen and Weidong Ma and Qiwei Ye and Tie-Yan Liu},
  title = {LightGBM: A Highly Efficient Gradient Boosting Decision Tree},
  booktitle = {Advances in Neural Information Processing Systems}, year = {2017}
}
@inproceedings{xgboost,
  author = {Tianqi Chen and Carlos Guestrin},
  title = {XGBoost: A Scalable Tree Boosting System},
  booktitle = {Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining},
  pages = {785--794}, year = {2016}
}
@inproceedings{hu2018senet,
  author = {Jie Hu and Li Shen and Gang Sun},
  title = {Squeeze-and-Excitation Networks},
  booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
  year = {2018}
}
@article{bai2018tcn,
  author = {Shaojie Bai and J. Zico Kolter and Vladlen Koltun},
  title = {An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling},
  journal = {arXiv preprint arXiv:1803.01271}, year = {2018}
}
@inproceedings{vaswani2017attention,
  author = {Ashish Vaswani and Noam Shazeer and Niki Parmar and Jakob Uszkoreit and Llion Jones and A. N. Gomez and Lukasz Kaiser and Illia Polosukhin},
  title = {Attention Is All You Need},
  booktitle = {Advances in Neural Information Processing Systems}, year = {2017}
}
"""

ieee_packages = r"""\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath,amssymb}
\usepackage{multirow}
\usepackage{array}
\usepackage{xurl}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,calc}
\usepackage[hidelinks]{hyperref}
"""
def write_ieee(filename, mode, body, blind=False):
    klass = "conference" if mode == "conference" else "journal"
    author = r"\author{}" if blind else (
        r"\author{Yahia Abdeldjalil Benyahia\thanks{Yahia Abdeldjalil Benyahia is with "
        r"\'Ecole nationale Sup\'erieure d'Informatique (ESI), Algiers, Algeria.}}"
    )
    author_pdf = "" if blind else "Yahia Abdeldjalil Benyahia"
    pre = (
        r"\documentclass[" + klass + r"]{IEEEtran}" + "\n" + ieee_packages +
        "\n\\hypersetup{pdftitle={" + title + "},pdfauthor={" + author_pdf + "}}\n" +
        r"\title{" + title + "}" + "\n" + author + "\n\\begin{document}\n\\maketitle\n" +
        r"\begin{abstract}" + abstract + r"\end{abstract}" + "\n" +
        r"\begin{IEEEkeywords}" + keywords + r"\end{IEEEkeywords}" + "\n"
    )
    end = "\n\\bibliographystyle{IEEEtran}\n\\bibliography{references}\n\\end{document}\n"
    (OUT / filename).write_text(pre + body + end, encoding="utf-8")

write_ieee("ifip-networking-2027.tex", "conference", doc_ifip, blind=True)
write_ieee("ieee-tnsm.tex", "journal", doc_tnsm, blind=False)

acm_body = re.sub(r"\\section\*\{Data and Code Availability\}[\s\S]*$", "", doc).rstrip()
acm_appendix = r"""
\clearpage
\appendix
\section{Ethics}
This study analyzes the pre-existing CESNET-QUICEXT-25 research dataset, which contains flow records collected on the CESNET3 network. The dataset provider states that client IP addresses are not included, destination addresses are transformed into non-reversible identifiers using a secret salt, flow start times are clipped to the hour, and source ports are omitted. The provider describes collection on a legitimate-interest basis rather than on consent, and states that the released data contain flow records rather than payload content apart from QUIC handshake metadata \cite{cesnet-quicext25,waitingforquic}. The present analysis uses the paper's 101 flow-level features and does not attempt re-identification, collect new user traffic, contact individuals, or redistribute raw dataset records. Nevertheless, network-flow metadata can be sensitive even when anonymized. The supplied project materials do not record a separate institutional ethics review, approval number, or waiver for this secondary analysis. The authors must confirm the applicable institutional determination and the dataset provider's access conditions before submission and add the accurate determination here if one exists.

\section{Open Science}
The manuscript source, experimental notebooks, model configurations, result tables, evaluation manifests, artifact audit, and reproducibility documentation are maintained in a public project repository. To preserve double-blind review, the repository URL is withheld from this review copy and should be added to the camera-ready version. The project repository does not redistribute CESNET-QUICEXT-25; the dataset is available separately from its original providers (DOI: \url{https://doi.org/10.5281/zenodo.17249078}) subject to their access and use conditions. The current repository snapshot does not contain a restorable checkpoint or per-flow predictions for the external neural reference. Its descriptive scores are therefore not presented as an independently reproducible comparison. The repository documentation records the environment, data partitions, model configurations, metrics, and known reproducibility limitations.

\section{Generative AI}
During preparation of this submission version, ChatGPT (OpenAI, GPT-6; accessed 30 October 2026) was used to assist with LaTeX conversion into venue-specific formats and to draft the revised abstract and venue-specific disclosure text. It was not used to collect or process the network dataset, train models, run experiments, calculate metrics, or generate the reported numerical results. The authors remain responsible for checking the manuscript, citations, disclosures, and final rendered files and for the accuracy and integrity of the submitted work.
"""
acm_preamble = (
    r"\documentclass[sigconf,review,anonymous,nonacm]{acmart}" + "\n" +
    r"\usepackage{microtype}" + "\n" +
    r"\usepackage{booktabs,multirow,array,xurl}" + "\n" +
    r"\usepackage{tikz}" + "\n" +
    r"\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,calc}" + "\n" +
    r"\settopmatter{printfolios=true,printacmref=false}" + "\n" +
    r"\hypersetup{pdftitle={" + title + r"},pdfauthor={}}" + "\n" +
    r"\title{" + title + "}" + "\n" +
    r"\author{Anonymous Author(s)}" + "\n" +
    r"\begin{document}" + "\n" +
    r"\begin{abstract}" + abstract + r"\end{abstract}" + "\n" +
    r"\maketitle" + "\n" +
    r"\keywords{" + keywords + "}\n"
)
acm_end = "\n\\bibliographystyle{ACM-Reference-Format}\n\\bibliography{references}\n\\end{document}\n"
(OUT / "acm-imc-2027.tex").write_text(acm_preamble + acm_body + acm_appendix + acm_end, encoding="utf-8")
(OUT / "references.bib").write_text(bib, encoding="utf-8")
report = """# Submission build report

The research sections, mathematical expressions, tables, TikZ diagrams, reported values, limitations, and references are retained. Abstracts are condensed for venue length guidance. The fifty-row per-class longtable is converted to a full-width float because longtable is not supported in standard two-column output. Diagrams remain vector artwork and are made full-width for legibility. No experimental results have been recomputed.

## Venue-specific handling
- IFIP Networking 2027: IEEE conference format; author block and PDF author metadata are removed. The direct GitHub URL is withheld from the review copy because it identifies the author; restore it in camera-ready.
- ACM IMC 2027: ACM sigconf, 10-point, letter-size, anonymous review format. Required Ethics, Open Science, and Generative AI appendices are included. A BBL is generated by BibTeX for the references upload.
- IEEE TNSM: IEEE Transactions journal format with author and affiliation retained. Abstract is within the required 75–200 word range. An ORCID was not present in the repository or manuscript materials and must be added before submission.

## Research and availability qualifications
The repository contains source, notebooks, configs, reported results, manifests, audit notes, and reproducibility documentation. It does not redistribute the CESNET-QUICEXT-25 input data or provide a restorable checkpoint/per-flow predictions for the external neural reference. These limitations are stated in the papers.

## Author verification needed before submission
1. Confirm institutional ethics review/waiver requirements for secondary analysis of CESNET-QUICEXT-25 and replace the explanatory note in the IMC Ethics appendix with the exact institutional determination.
2. Add the registered ORCID to the TNSM submission metadata/manuscript.
3. Restore the public repository URL in camera-ready versions of double-blind submissions, not in the review copies.
4. Verify current venue templates and instructions at submission time.
5. Review bibliographic fields and the final proof, particularly the venue-specific citation styles.
"""
(OUT / "submission-compliance-notes.md").write_text(report, encoding="utf-8")

for fn in ("ifip-networking-2027.tex", "acm-imc-2027.tex", "ieee-tnsm.tex"):
    t = (OUT / fn).read_text(encoding="utf-8")
    if t.count(r"\begin{document}") != 1 or t.count(r"\end{document}") != 1:
        raise RuntimeError("Document boundary check failed: " + fn)
    if r"\begin{longtable}" in t or r"\bibliography{references}" not in t:
        raise RuntimeError("Formatting conversion check failed: " + fn)
print("Prepared venue source files in", OUT)
