import os
import pathlib

import typer

app = typer.Typer()


def version_callback(value: bool):
    from .__about__ import __version__

    if value:
        typer.echo(f"pydra-deface version {__version__}")


@app.command()
def main(
    input_image: pathlib.Path = typer.Argument(
        None,
        help="Input image",
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
    output_image: pathlib.Path = typer.Argument(
        None,
        help="Ouput defaced image",
        file_okay=True,
        writable=True,
        resolve_path=True,
    ),
    template_image: pathlib.Path = typer.Option(
        None,
        "--template-image",
        "-t",
        help="Template image",
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
    template_mask: pathlib.Path = typer.Option(
        None,
        "--template-mask",
        "-m",
        help="Mask associated with template",
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
    output_mask: pathlib.Path = typer.Option(
        None,
        help="Output defacing mask",
        file_okay=True,
        writable=True,
        resolve_path=True,
    ),
    cache_dir: pathlib.Path = typer.Option(
        None,
        help="Cache directory for workflow",
        dir_okay=True,
        writable=True,
        resolve_path=True,
    ),
    version: bool = typer.Option(  # noqa
        None,
        "--version",
        help="Show this program's version",
        callback=version_callback,
    ),
) -> None:
    from . import workflow

    wf = workflow.build(
        with_brain_mask_extraction=template_mask is None,
        name="pydra_deface",
        cache_dir=cache_dir,
    )

    wf.inputs.input_image = input_image
    wf.inputs.output_image = os.fspath(output_image)
    wf.inputs.template_image = template_image

    if template_mask:
        wf.inputs.template_mask = template_mask

    if output_mask:
        wf.inputs.output_mask = os.fspath(output_mask)

    workflow.run(wf)


if __name__ == "__main__":
    app()
