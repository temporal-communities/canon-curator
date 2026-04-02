import time
import pytest
import requests
import threading

from canon_curator.enrich.clients.http_client import HttpClient


@pytest.fixture
def client():
    client = HttpClient(rate_limit="5/second", client_key="test")
    yield client
    client.close()


def test_session_is_cached(client):
    s1 = client._get_session()
    s2 = client._get_session()
    assert s1 is s2


def test_close_removes_session(client):
    s1 = client._get_session()
    client.close()
    s2 = client._get_session()
    assert s1 is not s2


def test_fetch_page_success(mocker, client):
    mock_response = mocker.Mock()
    mock_get = mocker.patch("requests.Session.get", return_value=mock_response)
    result = client.fetch_page("https://example.com")
    mock_get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    assert result is mock_response


def test_fetch_page_handles_http_error(mocker, client):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mocker.patch("requests.Session.get", return_value=mock_response)
    result = client.fetch_page("https://example.com")
    assert result is None


def test_fetch_page_handles_request_exception(mocker, client):
    mocker.patch("requests.Session.get", side_effect=requests.exceptions.ConnectionError())
    result = client.fetch_page("https://example.com")
    assert result is None


def test_fetch_page_retry_error_returns_none(mocker, client):
    mocker.patch("requests.Session.get", side_effect=requests.exceptions.RetryError())
    result = client.fetch_page("https://example.com")
    assert result is None


def _collect_session(client, session_list):
    session_list.append(client._get_session())
    client.close()


def test_sessions_are_thread_local(client):
    sessions = []

    t1 = threading.Thread(target=_collect_session, args=(client, sessions))
    t2 = threading.Thread(target=_collect_session, args=(client, sessions))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert len(sessions) == 2
    assert sessions[0] is not sessions[1]


def _append_result(client, results_list):
    results_list.append(client.fetch_page("https://example.com"))


def test_concurrent_requests_success(mocker, client):  # test concurrent requests succeed
    mocker.patch.object(client._limiter, "hit", return_value=True)
    mock_response = mocker.Mock()
    mocker.patch("requests.Session.get", return_value=mock_response)

    results = []
    threads = [threading.Thread(target=_append_result, args=(client, results)) for _ in range(2)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == 2
    assert all(result is mock_response for result in results)


def test_fetch_page_waits_when_rate_limited(mocker, client):
    mocker.patch.object(client._limiter, "hit", side_effect=[False, True])
    mock_sleep = mocker.patch("time.sleep")
    mocker.patch("requests.Session.get", return_value=mocker.Mock())
    client.fetch_page("https://example.com")
    mock_sleep.assert_called_once()
    sleep_duration = mock_sleep.call_args[0][0]
    assert 1 > sleep_duration >= 0


def test_context_manager_closes_session_on_exit(mocker):
    client = HttpClient(rate_limit="5/second", client_key="test")
    mock_close = mocker.patch.object(client, "close")
    with client:
        pass
    mock_close.assert_called_once()
