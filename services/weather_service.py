import requests
import re

class WeatherService:
    """Servicio para consumir la API externa de clima de forma segura."""

    def __init__(self, base_url: str = "https://wttr.in"):
        self.base_url = base_url

    @staticmethod
    def _sanitize(text: str) -> str:
        """Sanea la entrada para evitar caracteres maliciosos."""
        if not text:
            return ""
        return re.sub(r"[<>'\"\\;]", "", text.strip())

    def get_weather(self, city: str) -> dict:
        city_clean = self._sanitize(city)
        if not city_clean:
            return {"status": "error", "message": "Ciudad no válida."}

        url = f"{self.base_url}/{city_clean}?format=j1"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current = data["current_condition"][0]

            return {
                "status": "success",
                "city": city_clean.capitalize(),
                "temp_C": current.get("temp_C"),
                "humidity": current.get("humidity"),
                "desc": current.get("lang_es", [{}])[0].get("value", "N/A")
            }
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Error de conexión: {str(e)}"}
        except (KeyError, ValueError):
            return {"status": "error", "message": "Error al procesar el JSON de la API."}