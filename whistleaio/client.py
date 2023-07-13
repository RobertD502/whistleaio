""" Python client for Whistle API """
from __future__ import annotations

from typing import Any

import asyncio
from aiohttp import ClientResponse, ClientSession
from aiohttp.client_exceptions import ContentTypeError

from whistleaio.const import Endpoint, Header, TIMEOUT

from whistleaio.exceptions import WhistleAuthError, WhistleError

from whistleaio.model import WhistleData, Pet


class WhistleClient:
    """ Whistle Client. """

    def __init__(
            self, email: str, password: str,
            session: ClientSession | None = None,
            timeout: int = TIMEOUT
    ) -> None:
        """
        email: Registered whistle account email
        password: Registered whistle account password
        session: aiohttp.ClientSession or None to create a new session
        """

        self.email: str = email
        self.password: str = password
        self._session = session if session else ClientSession()
        self.token: str | None = None
        self.timeout: int = timeout

    async def get_token(self) -> None:
        """ Get auth token. No header needed. """

        data = {
            "email": self.email,
            "password": self.password
        }

        response = await self._post(endpoint=Endpoint.LOGIN, header={}, data=data)
        self.token = response['auth_token']

    async def get_whistle_data(self) -> WhistleData:
        """Fetch info for all pets and devices associated with
        Whistle account.
        """

        pets_data: dict[str, Pet] = {}
        response = await self.get_pets()

        if response['pets']:
            for pet in response['pets']:
                all_endpoints = await self.fetch_all_endpoints(pet)
                daily_item = await self.get_dailies_daily_items(pet['id'],
                                                                all_endpoints[1]['dailies'][00]['day_number'])

                pets_data[str(pet['id'])] = Pet(
                    id=str(pet['id']),
                    data=pet,
                    device=all_endpoints[0],
                    dailies=all_endpoints[1],
                    events=daily_item,
                    places=all_endpoints[2],
                    stats=all_endpoints[3],
                    health=all_endpoints[4]
                )
        return WhistleData(pets=pets_data)

    async def get_pets(self) -> dict[str, Any]:
        """ Get all pets. """

        if self.token is None:
            await self.get_token()
        header = await self.create_header()
        response = await self._get(endpoint=Endpoint.PETS, header=header)
        return response

    async def get_device_data(self, device_serial: str) -> dict[str, Any]:
        """ Get data for a single device. """

        if self.token is None:
            await self.get_token()
        header = await self.create_header()
        endpoint = f'{Endpoint.DEVICES}/{device_serial}'
        response = await self._get(endpoint=endpoint, header=header)
        return response

    async def get_dailies(self, pet_id: int) -> dict[str, Any]:
        """ Get dailies data for single pet. """

        if self.token is None:
            await self.get_token()
        header = await self.create_header()
        endpoint = f'{Endpoint.PETS}/{pet_id}{Endpoint.DAILIES}'
        response = await self._get(endpoint=endpoint, header=header)
        return response

    async def get_dailies_daily_items(self, pet_id: int, day_number: int) -> dict[str, Any]:
        """Get dailies daily items for single pet. The events reside
        at this endpoint.
        """

        if self.token is None:
            await self.get_token()
        header = await self.create_header()
        endpoint = f'{Endpoint.PETS}/{pet_id}{Endpoint.DAILIES}/{day_number}/daily_items'
        response = await self._get(endpoint=endpoint, header=header)
        return response

    async def get_stats(self, pet_id: int) -> dict[str, Any]:
        """ Get stats for single pet. """

        if self.token is None:
            await self.get_token()
        header = await self.create_header()
        endpoint = f'{Endpoint.PETS}/{pet_id}{Endpoint.STATS}'
        response = await self._get(endpoint=endpoint, header=header)
        return response

    async def get_places(self) -> dict[str, Any]:
        """ Get all places created within Whistle app. """

        if self.token is None:
            await self.get_token()
        header = await self.create_header()
        response = await self._get(endpoint=Endpoint.PLACES, header=header)
        return response

    async def get_health_trends(self, pet_id: int) -> dict[str, Any]:
        """Get all the health trends associated with a pet."""

        if self.token is None:
            await self.get_token()
        header = await self.create_header()
        endpoint = f'{Endpoint.PETS}/{pet_id}{Endpoint.HEALTH}'
        response = await self._get(endpoint=endpoint, header=header)
        return response

    async def fetch_all_endpoints(self, pet: dict[str, Any]) -> list:
        """Parallel request are made to all endpoints needed to
        get data for device, dailies, places, and stats of the Pet Object.
        """

        results = await asyncio.gather(*[
            self.get_device_data(pet['device']['serial_number']),
            self.get_dailies(pet['id']),
            self.get_places(),
            self.get_stats(pet['id']),
            self.get_health_trends(pet['id'])
            ],
        )
        return results

    async def create_header(self) -> dict[str, str]:
        """ Creates header that is used in all calls except token retrieval. """

        header = {
            "Accept": Header.ACCEPT,
            "Accept-Encoding": Header.ACCEPT_ENCODING,
            "Accept-Language": Header.LANGUAGE,
            "Accept-Unit-System": Header.UNIT,
            "Connection": 'keep-alive',
            "Content-Type": Header.CONTENT_TYPE,
            "User-Agent": Header.AGENT,
            "Authorization": f'Bearer {self.token}'
        }
        return header

    async def _post(self, endpoint: str, header: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
        """ Make POST call to Whistle servers. """

        async with self._session.post(
            url=f'{Endpoint.BASE_URL}{endpoint}', headers=header,
                data=data, timeout=self.timeout) as resp:
            return await self._response(resp)

    async def _get(self, endpoint: str, header: dict[str, Any]) -> dict[str, Any]:
        """ Make GET call to Whistle servers. """

        async with self._session.get(
            url=f'{Endpoint.BASE_URL}{endpoint}', headers=header,
                timeout=self.timeout) as resp:
            return await self._response(resp)

    @staticmethod
    async def _response(resp: ClientResponse) -> dict[str, Any] | None:
        """ Check response for any errors & return original response if none """

        try:
            response: dict[str, Any] = await resp.json()
        except ContentTypeError as cte:
            raise WhistleError(f'Whistle servers failed to return data for endpoint {resp.url}')
        if resp.status == 422:
            if response['errors'][0]['message'] == 'Invalid email address or password':
                raise WhistleAuthError('Invalid email address or password')
        else:
            return response
