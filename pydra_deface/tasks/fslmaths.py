__all__ = ["Mul"]

import os

import attrs
import pydra


@attrs.define(slots=False, kw_only=True)
class MulSpec(pydra.specs.ShellSpec):
    _ALLOWED_DATATYPES = {"char", "short", "int", "float", "double", "input"}

    datatype: str = attrs.field(
        metadata={
            "help_string": "datatype used for internal computation",
            "argstr": "-dt",
            "position": 1,
            "allowed_values": _ALLOWED_DATATYPES,
        }
    )

    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image",
            "mandatory": True,
            "argstr": "",
            "position": 2,
        }
    )

    # Restricted to image multiplication.
    operation: str = attrs.field(
        default="mul",
        metadata={
            "help_string": "operation",
            "argstr": "-{operation}",
            "allowed_values": {"mul"},
        },
    )

    other_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "other image used as operand",
            "argstr": "",
            "requires": {"operation"},
        }
    )

    output_image: str = attrs.field(
        metadata={
            "help_string": "output image",
            "argstr": "",
            "position": -2,
            "output_file_template": "{input_image}_mul",
        }
    )

    output_datatype: str = attrs.field(
        default="float",
        metadata={
            "help_string": "datatype used for output serialization",
            "argstr": "-odt",
            "position": -1,
            "allowed_values": _ALLOWED_DATATYPES,
        },
    )


class Mul(pydra.engine.ShellCommandTask):
    executable = "fslmaths"

    input_spec = pydra.specs.SpecInfo(name="MulInput", bases=(MulSpec,))
