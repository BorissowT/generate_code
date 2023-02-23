"""Color Palettes Controller.
Controller class implements logic, collection of functions executed when api
route is called.
"""
import log
from base import shared
from color_palettes.color_palette_repository import ColorPaletteRepository

color_palettes_repository = ColorPaletteRepository()


def load_color_palettes():
    """Load color palette data."""
    color_palettes_repository.load_data_to_cache()


load_color_palettes()


def save_color_palettes():
    """Save color palette data."""
    color_palettes_repository.save_elements()


# =============================================================================


def has_color_palette(color_palette_id):
    """Return True if color palette with id exists."""
    return color_palettes_repository.has_element(color_palette_id)


def get_color_palette(color_palette_id):
    """Return color palette specified by id."""
    return color_palettes_repository.get_element(color_palette_id)


def get_color_palettes():
    """Return color palettes."""
    return color_palettes_repository.get_data_from_cache()


# =============================================================================


def handle_get_color_palettes(io_context, **kwargs):
    """Return all color palettes."""
    return shared.json_get_handler(
        color_palettes_repository.get_data_from_cache(),
        io_context
    )


def handle_get_color_palette(io_context, matched_path, **kwargs):
    """Return a specific color palette."""
    return shared.json_get_handler(
        get_color_palette(matched_path['item_id']),
        io_context
    )


def handle_get_color_palette_value(io_context, matched_path, **kwargs):
    """Return value for key of a specific color palette."""
    return shared.json_get_handler(
        getattr(
            get_color_palette(matched_path['item_id']),
            matched_path['field_id']
        ),
        io_context
    )


shared.register_api_routes(
    key='color_palettes',
    list_getter=handle_get_color_palettes,
    item_getter=handle_get_color_palette,
    value_getter=handle_get_color_palette_value
)


# =============================================================================


def maintain_module():
    """Perform repeating maintenance tasks."""
    log.info("saving color_palettes...")
    save_color_palettes()


# =============================================================================


def test_functionality(result, out_progress, out_progress_end):
    """Run tests for this module and return any message."""
    count = 0
    messages = []

    if color_palettes_repository.get_data_from_cache():
        color_palette_id = color_palettes_repository.get_data_from_cache()[0].id

        if not has_color_palette(color_palette_id):
            messages.append('has_color_palette failed')
        count = count + 1
        out_progress(count)

        if not get_color_palette(color_palette_id) is \
               color_palettes_repository.get_data_from_cache()[0]:
            messages.append('get_color_palette failed')
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

    color_palettes_len = len(color_palettes_repository.get_data_from_cache())
    for color_palette in color_palettes_repository.get_data_from_cache():
        test_count, test_messages = color_palette.validate(
            color_palettes_repository.get_data_from_cache())
        count = count + test_count
        messages.extend(test_messages)
        out_progress(count, color_palettes_len)
    out_progress_end()

    result['validity_tests']['messages'] = messages
    result['validity_tests']['test_count'] = count
    return result
