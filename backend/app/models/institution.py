import uuid

from pydantic import BaseModel


class Institution(BaseModel):    

    id : str= ""
    name : str= ""
    location : str= ""
    contact_name : str= ""
    contact_mobile : str= ""
    contact_wechat : str= ""