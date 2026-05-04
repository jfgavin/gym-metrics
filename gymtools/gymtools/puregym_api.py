import requests

AUTH_URL = "https://auth.puregym.com/connect/token"
API_BASE = "https://capi.puregym.com/api/v2"
_HEADERS = {"User-Agent": "PureGym/1523 CFNetwork/1312 Darwin/21.0.0"}


class PureGymClient:
    def __init__(self, email: str, pin: str):
        self.email = email
        self.pin = pin
        self._token: str | None = None

    def authenticate(self) -> None:
        resp = requests.post(
            AUTH_URL,
            data={
                "grant_type": "password",
                "username": self.email,
                "password": self.pin,
                "scope": "pgcapi",
                "client_id": "ro.client",
            },
            headers=_HEADERS,
        )
        resp.raise_for_status()
        self._token = resp.json()["access_token"]

    def _get(self, path: str, **kwargs) -> dict:
        if not self._token:
            self.authenticate()
        headers = {**_HEADERS, "Authorization": f"Bearer {self._token}"}
        resp = requests.get(f"{API_BASE}{path}", headers=headers, **kwargs)
        if resp.status_code == 401:
            self.authenticate()
            headers["Authorization"] = f"Bearer {self._token}"
            resp = requests.get(f"{API_BASE}{path}", headers=headers, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def get_home_gym_id(self) -> int:
        member = self._get("/member")
        return member["HomeGym"]["Id"]

    def get_people_in_gym(self, gym_id: int) -> int:
        data = self._get("/gymSessions/gym", params={"gymId": gym_id})
        return data["TotalPeopleInGym"]
