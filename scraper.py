import json
import asyncio
import time

import httpx

from services.vehicles.nhtsa_vehicles_service import NHTSAVehiclesService
from models import VehicleDataModel
from services.files.file_storage_service import FileStorageService

import re

vehicle_types = [
    "Motorcycle",
    "Passenger Car",
    "Truck",
    "Bus",
    "Trailer",
    "Multipurpose Passenger Vehicle (MPV)",
    "Low Speed Vehicle (LSV)",
    "Incomplete Vehicle",
    "Off Road Vehicle",
]


def is_valid_make(make: str) -> bool:
    # Reject makes starting with "#" or other problematic characters
    return not re.match(r"^[#]", make)


async def execute():
    vehicles_service = NHTSAVehiclesService()
    makes = vehicles_service.get_all_makes()
    years = range(1990, 2021)

    print("Processing...")
    start = time.time()
    for year in years:
        for make in makes:
            if not is_valid_make(make):
                continue
            vehicles: list[VehicleDataModel] = []
            for vehicle_type in vehicle_types:
                async with httpx.AsyncClient() as client:
                    models = await vehicles_service.get_models(client, year, make, vehicle_type)
                    tasks = []

                    for model in models:
                        async def fetch_model_data(model=model):
                            tuples = await vehicles_service.get_weights_and_trims_of_model_variants(
                                client, year, make, model
                            )
                            return [
                                VehicleDataModel(
                                    make=make,
                                    model=model,
                                    year=year,
                                    variant=variant,
                                    curb_weight_tons=weight_in_tons,
                                )
                                for weight_in_tons, variant in tuples
                            ]

                        tasks.append(asyncio.create_task(fetch_model_data()))

                    task_results = await asyncio.gather(*tasks)
                    for result in task_results:
                        if not result:
                            # one of the models had no data
                            continue
                        vehicles.extend(result)

            # ——— WRITE OUT THIS MAKE's FILE ———
            folder = f"./nhtsa-vehicles/{make}"
            file_storage_service = FileStorageService(folder)
            filename = f"{year}.json"
            await file_storage_service.save_json(
                filename,
                json.dumps(vehicles, default=lambda o: o.__dict__, indent=2)
            )

            # vehicles list for this make/year is now written; next make starts fresh

    elapsed = time.time() - start
    print(f"Total execution time: {elapsed:.2f} seconds")
