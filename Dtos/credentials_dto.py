class CredentialsDto:
    def __init__(self, username: str | None, token: str | None):
        self.username = username
        self.token = token
    
    @staticmethod
    def from_dict(data: dict[str, str]) -> "CredentialsDto":
        return CredentialsDto(
            username=data.get("username"),
            token=data.get("token")
        )
    
    def to_dict(self) -> dict[str, str | None]:
        return {
            "username": self.username,
            "token": self.token
        }