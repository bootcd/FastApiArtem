from typing import Dict

from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

app = FastAPI(docs_url=None)

hotels = [
    {"id": 1, "title": "Sochi", "name": "Three Stars"},
    {"id": 2, "title": "Дубай", "name": "So hot in July"},
    {"id": 3, "title": "Goa", "name": "Cabin in the Woods"},
]

# Задание №1

FIELDS_LESS_NUMBER_RESPONSE = {"status": "ok",
                               "description": "fields number less than required",
                               "message": "Please, use PATCH method for partial updates!",
                               }

WRONG_KEY_RESPONSE = {"status": "error",
                      "description": "one or more wrong fields were entered",
                      "message": "Please, check entered field(s)!",
                      }

HOTEL_NOT_FOUND_RESPONSE = {"status": "error",
                            "description": "not hotel found",
                            "message": "Please, check hotel_id argument!",
                            }


def find_hotel_by_id(hotel_id):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            return hotel


@app.put("/hotels/{hotel_id}")
def put_hotel(hotel_id: int,
              data: dict = Body(),
              ):
    all_fields_in_data = True
    hotel_for_update = find_hotel_by_id(hotel_id)

    # catch WRONG FIELDS IN BODY
    for k, v in data.items():
        if k not in hotel_for_update:
            return WRONG_KEY_RESPONSE

    # check for PARTIAL DATA
    if len(hotel_for_update) > len(data):
        all_fields_in_data = False

    # Do All works if we FOUND hotel for update
    if hotel_for_update:
        if "title" in data:
            hotel_for_update['title'] = data["title"]
        if "name" in data:
            hotel_for_update['name'] = data["name"]
        if not all_fields_in_data:
            return FIELDS_LESS_NUMBER_RESPONSE
    else:
        return HOTEL_NOT_FOUND_RESPONSE
    return {"status": "OK",
            }


@app.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int,
                data: dict = Body(),
                ):
    hotel_for_update = find_hotel_by_id(hotel_id)

    # Do All works if we FOUND need hotel for update
    if hotel_for_update:
        try:
            for k, v in data.items():
                if k in hotel_for_update:
                    hotel_for_update[k] = v

                # catch WRONG FIELDS IN BODY
                else:
                    raise KeyError(k)
        except KeyError:
            return WRONG_KEY_RESPONSE
    else:
        return HOTEL_NOT_FOUND_RESPONSE
    return {"status": "OK",
            }


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
