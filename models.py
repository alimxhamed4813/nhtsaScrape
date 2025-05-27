from pydantic import BaseModel


class NHTSAGetAllMakesResultItem(BaseModel):
  Make_ID: str
  Make_Name: str


class NHTSAGetAllMakesAPIResponse(BaseModel):
  Count: int
  Message: str
  Results: list[NHTSAGetAllMakesResultItem]
  SearchCriteria: str | None


# ---------------------------


class NHTSAGetModelsForMakeYearResultItem(BaseModel):
  Make_ID: int
  Make_Name: str
  Model_ID: int
  Model_Name: str
  VehicleTypeId: int
  VehicleTypeName: str


class NHTSAGetModelsForMakeYearAPIResponse(BaseModel):
  Count: int
  Message: str
  SearchCriteria: str | None
  Results: list[NHTSAGetModelsForMakeYearResultItem]


# ---------------------------


# This model represents the key/value pairs of each data point in the model's variant data structure
class NHTSAGetCanadianVehicleSpecificationsSpecItem(BaseModel):
  Name: str
  Value: str


# This model represents the structure of the specification of a model's variant
class NHTSAGetCanadianVehicleSpecificationsResultsItem(BaseModel):
  Specs: list[NHTSAGetCanadianVehicleSpecificationsSpecItem]


# This model represents the response structure of the NHTSA API for the Canadian vehicle specifications
class NHTSAGetCanadianVehicleSpecificationsAPIResponse(BaseModel):
  Count: int
  Message: str | None
  Results: list[NHTSAGetCanadianVehicleSpecificationsResultsItem]
  SearchCriteria: str | None


# ---------------------------


class VehicleDataModel(BaseModel):
  make: str
  model: str
  variant: str
  year: int
  curb_weight_tons: float | None
