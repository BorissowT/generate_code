"""{{ docstrings_name_camelcase_plural }} Controller.
Controller class implements logic, collection of functions executed when api
route is called.
"""
import log
from base import shared
from {{ name }}.{{ name_singular }}_repository import {{ camel_case_singular }}Repository


{{ name }}_repository = {{ camel_case_singular }}Repository()


def load_{{ name }}():
    """Load {{ docstring_name_lower_case_singular }} data."""
    {{ name }}_repository.load_data_to_cache()


load_{{ name }}()


def save_{{ name }}():
    """Save {{ docstring_name_lower_case_singular }} data."""
    {{ name }}_repository.save_elements()


# =============================================================================


def has_{{ name_singular }}({{ name_singular }}_id):
    """Return True if {{ docstring_name_lower_case_singular }} with id exists."""
    return {{ name }}_repository.has_element({{ name_singular }}_id)


def get_{{ name_singular }}({{ name_singular }}_id):
    """Return {{ docstring_name_lower_case_singular }} specified by id."""
    return {{ name }}_repository.get_element({{ name_singular }}_id)


def get_{{ name }}():
    """Return {{ docstrings_name_lower_case_plural }}."""
    return {{ name }}_repository.get_data_from_cache()


# =============================================================================


def handle_get_{{ name }}(io_context, **kwargs):
    """Return all {{ docstrings_name_lower_case_plural }}."""
    return shared.json_get_handler(
        {{ name }}_repository.get_data_from_cache(),
        io_context
    )


def handle_get_{{ name_singular }}(io_context, matched_path, **kwargs):
    """Return a specific {{ docstring_name_lower_case_singular }}."""
    return shared.json_get_handler(
        get_{{ name_singular }}(matched_path['item_id']),
        io_context
    )


def handle_get_{{ name_singular }}_value(io_context, matched_path, **kwargs):
    """Return value for key of a specific {{ docstring_name_lower_case_singular }}."""
    return shared.json_get_handler(
        getattr(
            get_{{ name_singular }}(matched_path['item_id']),
            matched_path['field_id']
        ),
        io_context
    )


shared.register_api_routes(
    key='{{ name }}',
    list_getter=handle_get_{{ name }},
    item_getter=handle_get_{{ name_singular }},
    value_getter=handle_get_{{ name_singular }}_value
)


# =============================================================================


def maintain_module():
    """Perform repeating maintenance tasks."""
    log.info("saving {{ name }}...")
    save_{{ name }}()


# =============================================================================


def test_functionality(result, out_progress, out_progress_end):
    """Run tests for this module and return any message."""
    count = 0
    messages = []

    if {{ name }}_repository.get_data_from_cache():
        {{ name_singular }}_id = {{ name }}_repository.get_data_from_cache()[0].id

        if not has_{{ name_singular }}({{ name_singular }}_id):
            messages.append('has_{{ name_singular }} failed')
        count = count + 1
        out_progress(count)

        if not get_{{ name_singular }}({{ name_singular }}_id) is {{ name }}_repository.get_data_from_cache()[0]:
            messages.append('get_{{ name_singular }} failed')
        count = count + 1
        out_progress(count)

        # TODO: test all functions

    out_progress_end()

    result['functionality_tests']['messages'] = messages
    result['functionality_tests']['test_count'] = count
    return result


def test_validity(result, out_progress, out_progress_end):
    """Run tests for this module and return any message."""
    count = 0
    messages = []

    {{ name }}_len = len({{ name }}_repository.get_data_from_cache())
    for {{ name_singular }} in {{ name }}_repository.get_data_from_cache():
        test_count, test_messages = {{ name_singular }}.validate({{ name }}_repository.get_data_from_cache())
        count = count + test_count
        messages.extend(test_messages)
        out_progress(count, {{ name }}_len)
    out_progress_end()

    result['validity_tests']['messages'] = messages
    result['validity_tests']['test_count'] = count
    return result
