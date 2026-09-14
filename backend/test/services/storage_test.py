"""Tests for the mock storage layer."""

from services.storage import StorageService
from models.user import User
import pytest


@pytest.fixture(autouse=True)
def storage_service():
    """This PyTest fixture is injected into each test parameter of the same name below.

    It constructs a new, empty StorageService object."""
    storage_service = StorageService()
    storage_service.reset()
    return storage_service


def test_get_registrations_empty(storage_service: StorageService):
    assert len(storage_service.get_registrations()) == 0


def test_create_registration_valid(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    users = storage_service.get_registrations()
    assert len(users) == 1
    assert users[0].pid == pid


def test_create_registration_invalid_pid(storage_service: StorageService):
    pid = 71045308
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    with pytest.raises(Exception):
        storage_service.create_registration(user)


def test_create_registration_missing_first_name(storage_service: StorageService):
    pid = 71045308
    user = User(pid=pid, first_name="", last_name="Jordan")
    with pytest.raises(Exception):
        storage_service.create_registration(user)


def test_create_registration_missing_last_name(storage_service: StorageService):
    pid = 71045308
    user = User(pid=pid, first_name="Kris", last_name="")
    with pytest.raises(Exception):
        storage_service.create_registration(user)


def test_create_registration_duplicate(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    with pytest.raises(Exception):
        storage_service.create_registration(user)


def test_get_user_by_pid_does_not_exist(storage_service: StorageService):
    assert storage_service.get_user_by_pid(710453084) is None


def test_get_user_by_pid_does_exist(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    assert storage_service.get_user_by_pid(710453084) is user


def test_create_checkin_unknown_pid(storage_service: StorageService):
    with pytest.raises(Exception):
        storage_service.create_checkin(710453084)


def test_create_checkin_produces_checkin(storage_service: StorageService):
    pid = 710453084
    user = User(pid=pid, first_name="Kris", last_name="Jordan")
    storage_service.create_registration(user)
    storage_service.create_checkin(pid)
    checkins = storage_service.get_checkins()
    assert len(checkins) == 1
    assert checkins[0].user == user


def test_delete_registration_use_case(storage_service: StorageService):
    pid_1 = 730525001
    user_1 = User(pid=pid_1, first_name="Tyler", last_name="Smith")

    pid_2 = 710453084
    user_2 = User(pid=pid_2, first_name="Kris", last_name="Jordan")

    storage_service.create_registration(user_1)
    storage_service.create_registration(user_2)
    storage_service.delete_user(pid_1)

    registrations = storage_service.get_registrations()

    assert len(registrations) == 1 
    assert user_1 not in registrations


def test_2_delete_registration_use_case(storage_service: StorageService):
    pid_1 = 730525001
    user_1 = User(pid=pid_1, first_name="Tyler", last_name="Smith")

    pid_2 = 710453084
    user_2 = User(pid=pid_2, first_name="Kris", last_name="Jordan")

    pid_3 = 111111111
    user_3 = User(pid=pid_3, first_name="Kevin", last_name="Guskiewicz")

    storage_service.create_registration(user_1)
    storage_service.create_registration(user_2)
    storage_service.create_registration(user_3)

    storage_service.create_checkin(pid_1)
    storage_service.create_checkin(pid_3)
    storage_service.create_checkin(pid_1)
    storage_service.create_checkin(pid_2)
    storage_service.create_checkin(pid_2)
    storage_service.create_checkin(pid_2)
    storage_service.create_checkin(pid_1)
    storage_service.create_checkin(pid_3)
    storage_service.create_checkin(pid_2)
    
    storage_service.delete_user(pid_1)

    registrations = storage_service.get_registrations()
    assert len(registrations) == 2

    checkins = storage_service.get_checkins()

    for checkin in checkins:
        assert checkin.user.pid != pid_1

    assert len(checkins) == 6


def test_delete_registration_not_registered(storage_service: StorageService):
    pid_1 = 730525001
    user_1 = User(pid=pid_1, first_name="Tyler", last_name="Smith")

    pid_2 = 710453084
    user_2 = User(pid=pid_2, first_name="Kris", last_name="Jordan")

    storage_service.create_registration(user_1)
    storage_service.create_registration(user_2)

    pid_3 = 123456789

    with pytest.raises(Exception):
        storage_service.delete_user(pid_3)

    registrations = storage_service.get_registrations()
    assert len(registrations) == 2 


def test_delete_registration_invalid_pid(storage_service: StorageService):
    pid_1 = 999999999999
    user_1 = User(pid=pid_1, first_name="Tyler", last_name="Smith")

    pid_2 = 710453084
    user_2 = User(pid=pid_2, first_name="Kris", last_name="Jordan")

    with pytest.raises(Exception):
        storage_service.create_registration(user_1)

    storage_service.create_registration(user_2)

    with pytest.raises(Exception):
        storage_service.delete_user(pid_1)

    registrations = storage_service.get_registrations()
    assert len(registrations) == 1


def test_2_delete_registration_invalid_pid(storage_service: StorageService):
    pid_1 = 730525001
    user_1 = User(pid=pid_1, first_name="Tyler", last_name="Smith")

    pid_2 = 710453084
    user_2 = User(pid=pid_2, first_name="Kris", last_name="Jordan")

    pid_3 = 1010101
    user_3 = User(pid=pid_3, first_name="Dummy", last_name="User")
    
    storage_service.create_registration(user_1)
    storage_service.create_registration(user_2)

    with pytest.raises(Exception):
        StorageService.delete_user(user_3)

    registrations = storage_service.get_registrations()
    assert len(registrations) == 2