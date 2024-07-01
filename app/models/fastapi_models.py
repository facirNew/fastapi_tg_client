from pydantic import BaseModel


class PhoneNumberModel(BaseModel):
    phone: str


class MessageModel(BaseModel):
    message_text: str | None = None
    from_phone: str
    username: str
