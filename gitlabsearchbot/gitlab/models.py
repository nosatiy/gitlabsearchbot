from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional


class GitBlob(BaseModel):
    path: str
    raw: Optional[str] = None
    raw_path: Optional[str] = None

class GitProject(BaseModel):
    path: str = Field(default=None, alias="fullPath")
    project_id: int = Field(default=None, alias="id")
    blobs: Optional[list[GitBlob]] = Field(default=None, alias="repository")
    has_more: Optional[bool] = Field(default=None, alias="repository")
    end_cursor: Optional[str] = Field(default=None, alias="repository")
    
    @field_validator("project_id", mode="before")
    @classmethod
    def get_clean_id(cls, v: str):
        return int(v.split('/')[-1])

    @field_validator("blobs", mode="before")
    @classmethod
    def get_blobs(cls, v: dict):
        try:
            blobs = v["tree"]["blobs"]["nodes"]
        except:
            blobs = None
            return
        return [GitBlob(**blob) for blob in blobs]

    @field_validator("has_more", "end_cursor", mode="before")
    @classmethod
    def get_paginations(cls, v: dict, info: ValidationInfo):
        endpoint = {"has_more": "hasNextPage", "end_cursor": "endCursor"}
        try:
            return v["tree"]["blobs"]["pageInfo"][endpoint.get(info.field_name)]
        except:
            return
