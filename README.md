# Evaluating the Robustness of rStar

This repository contains the code and resources for the project **"Evaluating the Robustness of rStar: A Novel Framework for Enhanced Reasoning in Small Language Models"**, conducted as part of the 02456 Deep Learning course at DTU Compute, Fall 2024.

### Authors:

-   Jone Steinhoff (s243867)
-   Lukas Rasocha (s233498)
-   Panagiota Emmanouilidi (s223531)
-   Petr B. Nylander (s240466)
-   Robert Spralja (s243658)

### Supervised by:

Prof. Ole Winther
DTU Compute, Technical University of Denmark

## Overview

This project focuses on evaluating the robustness of the rStar framework, a reasoning system for small language models (SLMs). The evaluation uses variations of the GSM8K dataset, highlighting the framework’s strengths and limitations in handling diverse input modifications.

For more information please refer to our report.

## Reproduce

Prerequisites

-   Python 3.10 or later
-   CUDA-enabled GPU (e.g., NVIDIA Tesla A100)
-   Libraries listed in `requirements.txt`

1. Clone the repository:

```
git clone https://github.com/lukyrasocha/rStar.git
cd rStar
```

2. Install dependencies:

```
pip install -r requirements.txt
```

Run and inspect the `main.ipynb` notebook to see how results can be reproduced.
