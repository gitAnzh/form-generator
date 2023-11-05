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


class PersonalInformation(BaseModel):
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


class EducationInformation(BaseModel):
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


class Experiences(BaseModel):
    exprience1: Optional[str] = Field(
        title="exprience",
        alias="exprience1",
        description="experience detail of user",
        dataType="str",
        isRquired=True
    )
    exprience1Year: Optional[str] = Field(
        title="exprience year",
        alias="exprience1Year",
        description="experience year detail of user",
        dataType="str",
        isRquired=True
    )
    exprience2: Optional[str] = Field(
        title="exprience",
        alias="exprience2",
        description="university of user",
        dataType="str",
        isRquired=False
    )
    exprience2Year: Optional[str] = Field(
        title="exprience year",
        alias="exprience2Year",
        description="experience year detail of user",
        dataType="str",
        isRquired=False,
        default=None
    )
    exprience3: Optional[str] = Field(
        title="exprience",
        alias="exprience3",
        description="university of user",
        dataType="str",
        isRquired=False,
        default=None
    )
    exprience3Year: Optional[str] = Field(
        title="exprience year",
        alias="exprience3Year",
        description="experience year detail of user",
        dataType="str",
        isRquired=False,
        default=None
    )


class RegistrationData(BaseModel):
    registration_period: Optional[contract_duration] = Field(
        title="registration period",
        alias="registration_period",
        description="contract duration of user",
        dataType="str",
        isRquired=True
    )
    activities_propose1: Optional[str] = Field(
        title="activities propose",
        alias="activitiesPropose1",
        description="activities perpose 1",
        dataType="str",
        isRquired=True
    )
    activities_propose2: Optional[str] = Field(
        title="activities propose",
        alias="activitiesPropose2",
        description="activities perpose 1",
        dataType="str",
        isRquired=False,
        default=None
    )
    activities_propose3: Optional[str] = Field(
        title="activities propose",
        alias="activitiesPropose3",
        description="activities perpose 1",
        dataType="str",
        isRquired=False,
        default=None
    )
    special_condition1: Optional[str] = Field(
        title="special condition from client",
        alias="specialCondition1",
        description="special condition from client",
        dataType="str",
        isRquired=True,
        default=None
    )
    special_condition2: Optional[str] = Field(
        title="special condition from client",
        alias="specialCondition2",
        description="special condition from client",
        dataType="str",
        isRquired=True
    )
    special_condition3: Optional[str] = Field(
        title="special condition from client",
        alias="specialCondition3",
        description="special condition from client",
        dataType="str",
        isRquired=True
    )


class OfficialUse(BaseModel):
    official_use_aotnrrit: Optional[str] = Field(
        title="second official use item",
        alias="officialUseAotnrrit",
        description="approval of the new registration reequest isprovided that",
        dataType="str",
        isRquired=False,
        default=None
    )
    official_use_tawnaftfr: Optional[str] = Field(
        title="third official use item",
        alias="officialUseTawnaftfr",
        description="the application was not approved for the following reasons",
        dataType="str",
        isRquired=False,
        default=None
    )


class FormsValidator(BaseModel):
    companyID: Optional[int] = Field(
        title="company id",
        alias="companyID",
        dataType="str",
        isRquired=True,
    )
    PersonalInformation: Optional[PersonalInformation]
    educationalInformation: Optional[EducationInformation]
    experienceInformation: Optional[Experiences]
    RegistrationData: Optional[RegistrationData]
    OfficialUse: Optional[OfficialUse]
    special_servises: Optional[list] = Field(
        title="special servises",
        alias="specialServises",
        description="pricing for special services",
        dataType="dict",
        isRquired=True,
    )
