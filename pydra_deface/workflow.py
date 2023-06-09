import os

import pydra


def build(
    with_brain_mask_extraction: bool = True,
    with_bias_field_correction: bool = True,
    **kwargs,
) -> pydra.Workflow:
    from . import tasks

    input_spec = [
        "input_image",
        "output_image",
        "output_mask",
        "template_image",
        "template_mask",
    ]

    workflow = pydra.Workflow(input_spec=input_spec, **kwargs)

    if with_brain_mask_extraction:
        workflow.add(
            tasks.brain_mask_extraction(
                name="brain_mask_extraction",
                input_image=workflow.lzin.template_image,
            )
        )

    template_mask = (
        workflow.brain_mask_extraction.lzout.brain_mask
        if with_brain_mask_extraction
        else workflow.lzin.template_mask
    )

    workflow.add(
        tasks.deface(
            name="deface",
            input_image=workflow.lzin.input_image,
            output_image=workflow.lzin.output_image,
            template_image=workflow.lzin.template_image,
            template_mask=template_mask,
            output_mask=workflow.lzin.output_mask,
            with_bias_field_correction=with_bias_field_correction,
        )
    )

    workflow.set_output({
        "output_image": workflow.deface.lzout.output_image,
        "output_mask": workflow.deface.lzout.output_mask,
    })

    return workflow


def run(workflow: pydra.Workflow) -> pydra.engine.core.Result:
    with pydra.Submitter() as submitter:
        submitter(workflow)

    return workflow.result()
