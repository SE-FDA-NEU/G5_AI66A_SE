"""The one shape every error answer has, so the interactive documentation shows it."""

from pydantic import BaseModel


class ErrorOut(BaseModel):
    # The exact sentence of the acceptance criteria, in English.
    detail: str
    # What went wrong, such as "date_in_future". It never changes when the sentence is reworded,
    # so the app picks the message to show, in the chosen language, by this.
    code: str
