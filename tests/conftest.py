from pathlib import Path

import pytest

from cik_mapper import CIKMapper


@pytest.fixture(scope="session")
def mapper() -> CIKMapper:
    return CIKMapper()


@pytest.fixture(scope="session")
def auto_generated_mappings_path() -> Path:
    return Path("auto_generated_mappings")
