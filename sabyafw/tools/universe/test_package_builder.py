import pytest
from .package_builder import UniversePackageBuilder
from .package import Package


def test_non_existent_input_dir_raises_exception():
    with pytest.raises(Exception) as e:
        UniversePackageBuilder(None, None, '__SHOULD_NOT_EXIST__', '.', [])

    assert "Provided package path is not a directory: __SHOULD_NOT_EXIST__" in str(
        e.value)


def test_empty_input_dir_raises_exception():
    with pytest.raises(Exception) as e:
        UniversePackageBuilder(None, None, 'resources/empty', '.', [])

    assert "Provided package path does not contain the expected package files: resources/empty" in str(
        e.value)


def test_sabyafw_service_(mocker):

    package_json = {
        'name': 'sabyafw',
        'version': '1.2.3',
        'releaseVersion': 0
    }
    package = Package("sabyafw", "stub-universe")
    package_manager = mocker.Mock()

    package_manager.get_latest = mocker.MagicMock(return_value=Package.from_json(package_json))

    upb = UniversePackageBuilder(package, package_manager, 'resources/sabyafw', ',', [])

    sabyafw_mapping = upb._get_sabyafw_mapping_for_content("")
    assert 'upgrades-from' in sabyafw_mapping
    assert sabyafw_mapping['upgrades-from'] == "1.2.3"
