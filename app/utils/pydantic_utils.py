from typing import Annotated, Union

from pydantic import BaseModel, Field, create_model


def make_fields_optional(model_cls: type[BaseModel],new_model_name:str) -> type[BaseModel]:
    new_fields = {}

    for f_name, f_info in model_cls.model_fields.items():
        f_dct = f_info.asdict()
        new_fields[f_name] = (
            Annotated[(Union[f_dct['annotation'], None], *f_dct['metadata'], Field(**f_dct['attributes']))],
            None,
        )

    return create_model(
        new_model_name,
        __base__=model_cls,  
        **new_fields,
    )