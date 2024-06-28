import mesop as me

_BACKGROUND_COLOR = "#fafafa"
_FONT_COLOR = "#555"
_NOTE_ROW_FONT_COLOR = "#777"
_NOTE_ROW_FONT_SIZE = "14px"
_SELECTED_ROW_BACKGROUND_COLOR = "#dee3eb"
_DEFAULT_BORDER_STYLE = me.BorderSide(width=1, style="solid", color="#bbb")


def style_container(show_preview: bool = True) -> me.Style:
    return me.Style(
        background=_BACKGROUND_COLOR,
        color=_FONT_COLOR,
        display="grid",
        grid_template_columns="2fr 4fr 4fr" if show_preview else "2fr 8fr",
        height="100vh",
    )


def style_note_row(selected: bool = False) -> me.Style:
    return me.Style(
        color=_NOTE_ROW_FONT_COLOR,
        font_size=_NOTE_ROW_FONT_SIZE,
        background=_SELECTED_ROW_BACKGROUND_COLOR if selected else "none",
        padding=me.Padding.all(10),
        border=me.Border(bottom=_DEFAULT_BORDER_STYLE),
        height="100px",
        overflow_x="hidden",
        overflow_y="hidden",
    )


NOTES_NAV = me.Style(overflow_y="scroll", padding=me.Padding.all(15))


TOOLBAR = me.Style(
    padding=me.Padding.all(5),
    border=me.Border(bottom=_DEFAULT_BORDER_STYLE),
)


EDITOR = me.Style(
    overflow_y="hidden",
    padding=me.Padding(left=20, right=15, top=20, bottom=0),
    border=me.Border(
        left=_DEFAULT_BORDER_STYLE,
        right=_DEFAULT_BORDER_STYLE,
    ),
)


PREVIEW = me.Style(
    overflow_y="scroll", padding=me.Padding.symmetric(vertical=0, horizontal=20)
)


TEXTAREA = me.Style(
    color=_FONT_COLOR,
    background=_BACKGROUND_COLOR,
    outline="none",  # Hides focus border
    border=me.Border.all(me.BorderSide(style="none")),
    width="100%",
    height="100%",
)

TITLE_CONTAINER = me.Style(
    box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
    border_radius="8px",
    padding=me.Padding.all(16),
    margin=me.Padding.all(16),
    width="100%",
)

TITLE_INPUT = me.Style(
    color=_BACKGROUND_COLOR,
    font_size="20px",
    font_weight="bold",
    border=me.Border.all(me.BorderSide(style="none")),
    outline="none",
    width="100%",
    padding=me.Padding.all(8),
    border_radius="4px",
)

PROMPT_INPUT = me.Style(
    color=_NOTE_ROW_FONT_COLOR,
    font_size=_NOTE_ROW_FONT_SIZE,
    padding=me.Padding.all(20),
    height="300px",
    overflow_x="hidden",
    overflow_y="hidden",
    width="100%",
)
