import pydra


def brain_mask_extraction(**kwargs) -> pydra.Workflow:
    from pydra.tasks import fsl

    workflow = pydra.Workflow(input_spec=["input_image"], **kwargs)

    workflow.add(
        fsl.BET(
            name="bet",
            input_image=workflow.lzin.input_image,
            save_brain_mask=True,
        )
    )

    workflow.set_output(
        {"brain_mask": workflow.bet.lzout.brain_mask}
    )

    return workflow


def bias_field_correction(**kwargs) -> pydra.Workflow:
    from pydra.tasks import fsl

    workflow = pydra.Workflow(input_spec=["input_image"], **kwargs)

    workflow.add(
        fsl.FAST(
            name="fast",
            input_image=workflow.lzin.input_image,
            save_bias_corrected_image=True,
            no_partial_volume_estimation=True,
        )
    )

    workflow.set_output(
        {"bias_corrected_image": workflow.fast.lzout.bias_corrected_image}
    )

    return workflow


def deface(with_bias_field_correction: bool = False, **kwargs) -> pydra.Workflow:
    from pydra.tasks import fsl
    from pydra.tasks.fsl import fslmaths

    workflow = pydra.Workflow(
        input_spec=[
            "input_image",
            "output_image",
            "template_image",
            "template_mask",
            "output_mask",
        ],
        **kwargs,
    )

    workflow.add(
        fsl.FSLReorient2Std(
            name="fslreorient2std",
            input_image=workflow.lzin.input_image,
        )
    )

    if with_bias_field_correction:
        workflow.add(
            bias_field_correction(
                name="bias_field_correction",
                input_image=workflow.fslreorient2std.lzout.output_image,
                verbose=True,
            )
        )

    reference_image = (
        workflow.bias_field_correction.lzout.bias_corrected_image
        if with_bias_field_correction
        else workflow.fslreorient2std.lzout.output_image
    )

    workflow.add(
        fsl.FLIRT(
            name="flirt_template_image",
            input_image=workflow.lzin.template_image,
            reference_image=reference_image,
            cost_function="mutualinfo",
            verbose=True,
        )
    )

    workflow.add(
        fsl.FLIRT(
            name="flirt_template_mask",
            input_image=workflow.lzin.template_mask,
            reference_image=reference_image,
            input_matrix=workflow.flirt_template_image.lzout.output_matrix,
            apply_transformation=True,
            verbose=True,
        )
    )

    workflow.add(
        fslmaths.Mul(
            name="apply_mask",
            input_image=reference_image,
            other_image=workflow.flirt_template_mask.lzout.output_image,
            output_image=workflow.lzin.output_image,
        )
    )

    workflow.set_output({
        "output_image": workflow.apply_mask.lzout.output_image,
        "output_mask": workflow.flirt_template_mask.lzout.output_image,
    })

    return workflow
