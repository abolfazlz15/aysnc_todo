from enum import Enum

class TaskFieldEnum(Enum):
    """
    Enum for task fields.
    """
    ID = "id"
    TITLE = "title"
    CONTENT = "content"
    STATUS = "status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"