from dataclasses import dataclass, field

import mesop as me
import openai

from src import style
from src.settings import Settings

settings = Settings()


@dataclass(kw_only=True)
class Note:
    content: str = ""
    title: str = ""


@me.stateclass
class State:
    notes: list[Note] = field(
        default_factory=lambda: [Note(content=settings.default_content)]
    )
    selected_note_index: int = 0
    selected_note_content: str = settings.default_content
    selected_note_title: str = ""
    show_preview: bool = True
    additional_prompt: str = ""
    show_prompt: bool = False
    clear_prompt_count: int = 0


@me.page(
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io"]
    ),
    title="Markdown Editor",
)
def page():
    state = me.state(State)
    with me.box(style=style.TITLE_CONTAINER):
        me.input(
            label="タイトル",
            value=state.selected_note_title,
            on_input=on_title_input,
            style=style.TITLE_INPUT,
        )

    with me.box(style=style.style_container(state.show_preview)):
        # Note list column
        with me.box(style=style.NOTES_NAV):
            # Toolbar
            with me.box(style=style.TOOLBAR):
                with me.content_button(on_click=on_click_new):
                    with me.tooltip(message="New note"):
                        me.icon(icon="add_notes")
                with me.content_button(on_click=on_click_hide):
                    with me.tooltip(
                        message="Hide preview" if state.show_preview else "Show preview"
                    ):
                        me.icon(icon="hide_image")
                with me.content_button(on_click=on_click_delete):
                    with me.tooltip(message="Delete note"):
                        me.icon(icon="delete")
                with me.content_button(on_click=on_click_prompt):
                    with me.tooltip(message="Show prompt"):
                        me.icon(icon="chat")

            # Note list and prompt container
            if state.show_prompt:
                with me.box():
                    me.textarea(
                        label="プロンプト",
                        key=f"prompt-{state.clear_prompt_count}",
                        on_input=on_prompt_input,
                        style=style.PROMPT_INPUT,
                    )
                    me.button(label="Submit", type="flat", on_click=on_click_submit)
                    me.button(label="Clear", on_click=on_click_clear)
            else:
                for index, note in enumerate(state.notes):
                    with me.box(
                        key=f"note-{index}",
                        on_click=on_click_note,
                        style=style.style_note_row(index == state.selected_note_index),
                    ):
                        me.text(note.title)

        # Markdown Editor Column
        with me.box(style=style.EDITOR):
            me.native_textarea(
                value=state.selected_note_content,
                style=style.TEXTAREA,
                on_input=on_text_input,
            )

        # Markdown Preview Column
        if state.show_preview:
            with me.box(style=style.PREVIEW):
                if state.selected_note_index < len(state.notes):
                    me.markdown(state.notes[state.selected_note_index].content)


# EVENT HANDLERS


def on_title_input(e: me.InputEvent):
    state = me.state(State)
    state.notes[state.selected_note_index].title = e.value


def on_prompt_input(e: me.InputEvent):
    state = me.state(State)
    state.additional_prompt = e.value


def on_click_prompt(e: me.ClickEvent):
    state = me.state(State)
    print(f"{state.show_prompt=}")
    state.show_prompt = bool(not state.show_prompt)
    print(f"{state.show_prompt=}")


def on_click_new(e: me.ClickEvent):
    state = me.state(State)
    state.show_prompt = False
    # Need to update the initial value of the editor text area so we can
    # trigger a diff to reset the editor to empty. Need to yield this change.
    # for this to work.
    if state.notes:
        state.selected_note_content = state.notes[state.selected_note_index].content
        state.selected_note_title = state.notes[state.selected_note_index].title
        print(f"click new title{state.selected_note_title}")
        print(f"click new content{state.selected_note_content}")
        yield
    # Reset the initial value of the editor text area to empty since the new note
    # has no content.
    state.selected_note_content = settings.default_content
    state.selected_note_title = ""
    state.notes.append(Note(content=settings.default_content))
    state.selected_note_index = len(state.notes) - 1
    yield


def on_click_hide(e: me.ClickEvent):
    """Hides/Shows preview Markdown pane."""
    state = me.state(State)
    state.show_preview = bool(not state.show_preview)


def on_click_note(e: me.ClickEvent):
    """Selects a note from the note list."""
    state = me.state(State)
    note_id = int(e.key.replace("note-", ""))
    note = state.notes[note_id]
    print(note)
    state.selected_note_index = note_id
    state.selected_note_title = note.title
    state.selected_note_content = note.content


def on_text_input(e: me.InputEvent):
    """Captures text in editor."""
    state = me.state(State)
    state.notes[state.selected_note_index].content = e.value


def on_click_submit(e: me.ClickEvent):
    state = me.state(State)
    openai.api_key = settings.open_api_key
    prompt = settings.base_prompt.format(
        note_title=state.notes[state.selected_note_index].title,
        default_content=settings.default_content if state.selected_note_content else "",
        note_content=state.selected_note_content,
        additional_prompt=state.additional_prompt,
    )

    print(f"{prompt=}")

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": settings.role_prompt,
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        # max_tokens=
    )
    data = response.choices[0].message.content
    # data = "hoge"
    state.selected_note_content = data
    on_text_input(me.InputEvent(key="response", value=data))
    # print(state.selected_note_content)
    # state.selected_note_content = state.selected_note_content


def on_click_clear(e: me.ClickEvent):
    """Click event for clearing prompt text."""
    state = me.state(State)
    state.clear_prompt_count += 1
    print(f"{state.additional_prompt=}")
    state.additional_prompt = ""


def on_click_delete(e: me.ClickEvent):
    """Click event for deleting a note."""
    state = me.state(State)
    state.show_prompt = False
    if state.notes:
        state.selected_note_content = state.notes[state.selected_note_index - 1].content
        state.selected_note_title = state.notes[state.selected_note_index - 1].title
    del state.notes[state.selected_note_index]
    if state.notes:
        state.selected_note_index -= 1
    else:
        state.selected_note_content = ""
        state.selected_note_title = ""
