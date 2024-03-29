from fastapi import FastAPI, status, HTTPException
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderInsufficientPrivileges

app = FastAPI()
geolocator = Nominatim(user_agent="py-get-location")


@app.get("/", status_code=status.HTTP_200_OK, tags=["default".upper()])
def read_root():
    return "running...!"


@app.get("/full_location", status_code=status.HTTP_200_OK, tags=["get full location".upper()])
def get_full_location(
        latitude: float,
        longitude: float
):
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True, language=True)
        address = location.address
        address_parts = address.split(', ')
        province = address_parts[-2] if len(address_parts) > 1 else None
        if province and province.isnumeric():
            province = address_parts[-3] if len(address_parts) > 1 else None
        return {
            "address": address,
            "address_parts": address_parts,
            "province": province
        }
    except GeocoderInsufficientPrivileges as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Geocoding service error: Insufficient privileges")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
