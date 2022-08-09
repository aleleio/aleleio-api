"""
Connexion - Override Validator to Enforce Defaults

When defaults are set in openapi.yml, they are only used for the documentation, not enforced when empty keywords are
provided for GameIn. This is an override for the validator, example from the docs:
https://github.com/spec-first/connexion/tree/main/examples/swagger2/enforcedefaults

Careful with `OneOf`: https://github.com/spec-first/connexion/issues/351#issuecomment-1124187644
"""

import jsonschema
from connexion.decorators.validation import RequestBodyValidator
from connexion.json_schema import Draft4RequestValidator


def extend_with_set_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        yield from validate_properties(validator, properties, instance, schema)

    return jsonschema.validators.extend(validator_class, {"properties": set_defaults})


EnforcingValidator = extend_with_set_default(Draft4RequestValidator)


class EnforcingRequestBodyValidator(RequestBodyValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, validator=EnforcingValidator, **kwargs)


validator_remap = {"body": EnforcingRequestBodyValidator}
