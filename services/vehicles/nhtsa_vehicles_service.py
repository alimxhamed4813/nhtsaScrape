import asyncio
import time

import httpx
import requests
from services.http.http_service import http_get
from models import (
    NHTSAGetAllMakesAPIResponse,
    NHTSAGetCanadianVehicleSpecificationsResultsItem,
    NHTSAGetModelsForMakeYearAPIResponse,
    NHTSAGetCanadianVehicleSpecificationsAPIResponse,
)


class NHTSAVehiclesService:
    def __init__(self):
        self.api_base_url = "https://vpic.nhtsa.dot.gov/api"
        pass

    @staticmethod
    def get_all_makes() -> list:
        url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json"
        try:
            response = requests.get(url)
            time.sleep(0.2)
            data = response.json()
            return [make["Make_Name"] for make in data.get("Results", [])]
        except Exception as e:
            print(f"[!] Failed to get makes: {e}")
            return []

    async def get_models(
            self, client: httpx.AsyncClient, year: int, make: str, vehicle_type: str
    ) -> list[str]:
        try:
            models = []

            api_response_data = await http_get(
                client,
                f"{self.api_base_url}/vehicles/GetModelsForMakeYear/make/{make}/modelyear/{year}/vehicletype/{vehicle_type}?format=json",
            )

            data = NHTSAGetModelsForMakeYearAPIResponse(**api_response_data)
            if data.Results is None:
                return []

            result_items = data.Results
            models = [item.Model_Name for item in result_items]

            return models
        except Exception as e:
            print(
                f"[!] Error: [get_models] - Failed to fetch models for {make}, {year}, {vehicle_type}: {e}"
            )
            return []

    async def get_weights_and_trims_of_model_variants(
            self, client: httpx.AsyncClient, year: int, make: str, model: str
    ) -> list[tuple[float | None, str]]:
        variants_specs_results: list[
            NHTSAGetCanadianVehicleSpecificationsResultsItem
        ] = await self.get_model_variants_specs(client, year, make, model)

        if not variants_specs_results:
            print(
                f"[!] Error: [get_weights_and_trims_of_model_variants] - No vehicle specifications found for {year}, {make}, {model}."
            )
            return []

        variants_list: list[tuple[float | None, str]] = []

        # Each item holds info about a specific variant of the model
        for item in variants_specs_results:
            variant: str = ""
            weight_in_tons: float | None = None

            if item.Specs[1].Name.lower() == "model":
                # Check if model is already in the variant value
                model_check = model.lower().strip()
                variant_value = item.Specs[1].Value.strip()

                if model_check and model_check in variant_value.lower():
                    # Extract just the additional variant information by removing the model name
                    # We can use case-insensitive replace and then strip whitespace
                    variant_parts = variant_value.lower().replace(model_check, "", 1).strip()

                    if variant_parts:
                        # Convert back to uppercase to follow original casing
                        variant = variant_parts.upper()
                    else:
                        # If nothing remains after removing the model, use the full value
                        variant = variant_value
                else:
                    # If model name is not in the variant value, use the whole value
                    variant = variant_value

            curbweight_key, curb_weight_value = item.Specs[7].Name, item.Specs[7].Value
            if curbweight_key.lower() == "cw" and curb_weight_value:
                try:
                    weight_in_tons = round(float(item.Specs[7].Value) * 0.001102, 1)
                except ValueError:
                    print(
                        f"[!] Error: [get_weights_and_trims_of_model_variants] - "
                        f"Invalid weight value: {curb_weight_value if curb_weight_value else 'No value exists'}."
                    )

            variants_list.append((weight_in_tons, variant))

        return variants_list

    async def get_model_variants_specs(
            self, client: httpx.AsyncClient, year: int, make: str, model: str
    ) -> list[NHTSAGetCanadianVehicleSpecificationsResultsItem]:
        try:
            await asyncio.sleep(0.25)

            api_response_data = await http_get(
                client,
                f"{self.api_base_url}/vehicles/GetCanadianVehicleSpecifications?year={year}&make={make}&model={model}&format=json",
            )

            data = NHTSAGetCanadianVehicleSpecificationsAPIResponse(**api_response_data)
            if data.Results is None:
                return []

            return data.Results
        except Exception as e:
            print(f"[!] Error: [get_model_variants_specs] - {e}")
            return []


if __name__ == "__main__":
    api_base_url = "https://vpic.nhtsa.dot.gov/api"
    url = f"{api_base_url}/vehicles/DecodeVin/INPCXPTX3PD814892*BA?format=json&modelyear=2023"
    response = requests.get(url)
    print(response.json())

