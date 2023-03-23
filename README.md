# pydra-deface

Pydra workflow for defacing structural brain images.

## Using the CLI 

```commandline
pipx install pydra-deface
```

```commandline
pydra-deface -t template.nii.gz -m mask.nii.gz input.nii.gz defaced.nii.gz
```

## Using the Pydra task

```commandline
pip install pydra_deface
```

```python
from pydra_deface.tasks import deface

task = deface(
    input_image="input.nii.gz",
    output_image="defaced.nii.gz",
    template_image="template.nii.gz",
    template_mask="mask.nii.gz",
)

task()
```
