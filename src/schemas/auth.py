from pydantic import BaseModel, Field, model_validator


class TokenSchema(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str


class AccessTokenInputDataSchema(BaseModel):
    email: str | None = None


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class ChangePasswordIn(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)
    new_password_confirm: str = Field(min_length=8)

    @model_validator(mode='after')
    def validate_passwords(self):
        current_password = self.current_password
        new_password = self.new_password
        new_password_confirm = self.new_password_confirm
        if new_password != new_password_confirm:
            raise ValueError('passwords do not match')
        if current_password == new_password:
            raise ValueError('your new password can not be like your current password')
        return self        
