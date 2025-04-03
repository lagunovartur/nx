from typing import Any, Type

from dishka import AsyncContainer, Provider, make_async_container


class IocBuilder:
    def __init__(self, *providers: Provider, context: dict[Any, Any] | None = None):
        self._context = context or {}
        self._providers = {
            self._provider_key(provider): provider for provider in providers
        }
        self._overrides: dict[Type[Provider], Provider] = {}

    def __call__(self) -> AsyncContainer:
        return make_async_container(*self._get_merged(), context=self._context)

    @property
    def context(self) -> dict[Any, Any]:
        return self._context

    def add(self, provider):
        self._providers[self._provider_key(provider)] = provider

    def remove(self, provider):
        self._providers.pop(self._provider_key(provider))
        self._overrides.pop(self._provider_key(provider), None)

    def __iter__(self):
        return iter(self._get_merged())

    def __setitem__(self, item: Type[Provider], value: Provider):
        if not self._providers.get(item):
            raise KeyError(f"Provider {item} not registered")
        self._overrides[item] = value

    def __getitem__(self, item: Type[Provider]) -> Provider:
        provider = self._overrides.get(item) or self._providers.get(item)
        if not provider:
            raise KeyError(f"Provider {item} not registered")
        return provider

    def get_providers(self) -> list[Provider]:
        return list(self._providers.values())

    @staticmethod
    def _provider_key(provider):
        return provider.__class__

    def _get_merged(self):
        return (self._providers | self._overrides).values()
