"""Provides a :class:`MutualFundMapper` class for mapping CIKs, tickers, and company names.."""

from .BaseMapper import BaseMapper
from .retrievers import MutualFundRetriever


class MutualFundMapper(BaseMapper):
    """A :class:`MutualFundMapper` object.

    Usage::

        >>> from sec_cik_mapper import MutualFundMapper

        # Create a MutualFundMapper instance
        >>> mutualFundMapper = MutualFundMapper()
    """

    def __init__(self):
        super().__init__()
        mutualFundRetriever = MutualFundRetriever()
        self.mapping_metadata = self._get_mapping_metadata_from_sec(mutualFundRetriever)
