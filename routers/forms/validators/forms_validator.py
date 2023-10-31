from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class BaseValidator(BaseModel):
    pass


class contract_type(str, Enum):
    new = "new"
    renew = "renew"
    update = "update"


class contract_duration(str, Enum):
    month_3 = "3 month"
    month_6 = "6 month"
    month_9 = "9 month"
    month_12 = "12 month"


class FormsValidator(BaseModel):
    sortType: Optional[contract_type] = Field(
        title="Contract Type",
        alias="contractType",
        description="contract condition",
        dataType="str",
        isRquired=True
    )
    name: Optional[str] = Field(
        title="Name",
        alias="name",
        description="name of user",
        dataType="str",
        isRquired=True
    )
    idNumber: Optional[str] = Field(
        title="id number",
        alias="idNumber",
        description="name of user",
        dataType="str",
        isRquired=True
    )
    address: Optional[str] = Field(
        title="address",
        alias="address",
        description="address of user",
        dataType="str",
        isRquired=True
    )
    phone: Optional[str] = Field(
        title="phone number",
        alias="phoneNumber",
        description="phone number of user",
        dataType="str",
        isRquired=True
    )

    educationDegree: Optional[str] = Field(
        title="highest academic degree",
        alias="educationDegree",
        description="education of user",
        dataType="str",
        isRquired=True
    )
    university: Optional[str] = Field(
        title="university",
        alias="university",
        description="university of user",
        dataType="str",
        isRquired=True
    )
    exprience1: Optional[str] = Field(
        title="exprience",
        alias="exprience",
        description="experience detail of user",
        dataType="str",
        isRquired=True
    )
    exprience1Year: Optional[str] = Field(
        title="exprience year",
        alias="exprienceYear",
        description="experience year detail of user",
        dataType="str",
        isRquired=True
    )
    exprience2: Optional[str] = Field(
        title="exprience",
        alias="exprience",
        description="university of user",
        dataType="str",
        isRquired=False
    )
    exprience2Year: Optional[str] = Field(
        title="exprience year",
        alias="exprienceYear",
        description="experience year detail of user",
        dataType="str",
        isRquired=False
    )
    exprience3: Optional[str] = Field(
        title="exprience",
        alias="exprience",
        description="university of user",
        dataType="str",
        isRquired=False
    )
    exprience3Year: Optional[str] = Field(
        title="exprience year",
        alias="exprienceYear",
        description="experience year detail of user",
        dataType="str",
        isRquired=False
    )
    registration_period: Optional[contract_duration] = Field(
        title="registration period",
        alias="registration_period",
        description="contract duration of user",
        dataType="str",
        isRquired=True
    )
    activities_propose1: Optional[str] = Field(
        title="activities propose",
        alias="activitiesPropose",
        description="activities perpose 1",
        dataType="str",
        isRquired=True
    )
    activities_propose2: Optional[str] = Field(
        title="activities propose",
        alias="activitiesPropose",
        description="activities perpose 1",
        dataType="str",
        isRquired=False
    )
    activities_propose3: Optional[str] = Field(
        title="activities propose",
        alias="activitiesPropose",
        description="activities perpose 1",
        dataType="str",
        isRquired=False
    )
    special_condition1: Optional[str] = Field(
        title="special condition from client",
        alias="specialCondition",
        description="special condition from client",
        dataType="str",
        isRquired=True
    )
    special_condition2: Optional[str] = Field(
        title="special condition from client",
        alias="specialCondition",
        description="special condition from client",
        dataType="str",
        isRquired=True
    )
    special_condition3: Optional[str] = Field(
        title="special condition from client",
        alias="specialCondition",
        description="special condition from client",
        dataType="str",
        isRquired=True
    )
    official_use_aotnrrit: Optional[str] = Field(
        title="second official use item",
        alias="officialUseAotnrrit",
        description="approval of the new registration reequest isprovided that",
        dataType="str",
        isRquired=False
    )
    official_use_tawnaftfr: Optional[str] = Field(
        title="third official use item",
        alias="officialUseTawnaftfr",
        description="the application was not approved for the following reasons",
        dataType="str",
        isRquired=False
    )
    special_sservises: Optional[list] = Field(
        title="special servises",
        alias="specialServises",
        description="pricing for special services",
        dataType="list",
        isRquired=False
    )
