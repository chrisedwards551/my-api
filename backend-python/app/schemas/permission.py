from pydantic import BaseModel


class PermissionBase(BaseModel):
    name: str
    description: str | None = None


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class RolePermissionCreate(BaseModel):
    role: str
    permission_id: int


class RolePermissionResponse(BaseModel):
    id: int
    role: str
    permission_id: int

    model_config = {
        "from_attributes": True
    }