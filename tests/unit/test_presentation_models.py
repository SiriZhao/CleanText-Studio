from cleantext_studio.presentation import AppPresentationState, MessageSeverity, UserMessage


def test_user_messages_keep_locale_outside_business_data() -> None:
    message = UserMessage("status.cleaning.completed", MessageSeverity.SUCCESS, {"count": 4})
    assert message.message_id == "status.cleaning.completed"
    assert message.parameters == {"count": 4}


def test_presentation_state_uses_stable_values() -> None:
    state = AppPresentationState(selected_preset="standard", selected_paragraph_mode="smart_sections")
    assert state.selected_preset == "standard"
    assert state.selected_paragraph_mode == "smart_sections"
