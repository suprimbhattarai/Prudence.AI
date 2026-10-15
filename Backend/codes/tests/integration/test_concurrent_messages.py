import getpass
import json
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from urllib.request import Request, urlopen

BASE_URL = "http://127.0.0.1:8000"
CONCURRENT_REQUESTS = 10


def request_api(
    method: str,
    path: str,
    token: str,
    payload: dict | None = None,
):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None

    request = Request(
        url=f"{BASE_URL}{path}",
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    with urlopen(request, timeout=30) as response:
        if response.status == 204:
            return None

        return json.loads(response.read().decode("utf-8"))


def main():
    token = getpass.getpass("Customer access token: ").strip()

    conversation = request_api(
        "POST",
        "/conversations",
        token,
    )

    conversation_id = conversation["id"]

    messages = [f"Concurrent test message {i}" for i in range(CONCURRENT_REQUESTS)]

    barrier = Barrier(CONCURRENT_REQUESTS)

    def send_message(content: str):
        barrier.wait()

        return request_api(
            "POST",
            f"/conversations/{conversation_id}/messages",
            token,
            {"content": content},
        )

    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        results = list(executor.map(send_message, messages))

    assert len(results) == CONCURRENT_REQUESTS

    saved_messages = request_api(
        "GET",
        f"/conversations/{conversation_id}/messages?limit=100",
        token,
    )

    assert len(saved_messages) == CONCURRENT_REQUESTS
    assert {m["content"] for m in saved_messages} == set(messages)

    conversations = request_api(
        "GET",
        "/conversations",
        token,
    )

    saved_conversation = next(
        item for item in conversations if item["id"] == conversation_id
    )

    # The first request to acquire the lock determines
    # the fallback title.
    assert saved_conversation["title"] in messages

    # Sending one more message must not replace the title.
    initial_title = saved_conversation["title"]
    previous_activity = saved_conversation["updated_at"]

    request_api(
        "POST",
        f"/conversations/{conversation_id}/messages",
        token,
        {"content": "A later message"},
    )

    conversations = request_api(
        "GET",
        "/conversations",
        token,
    )

    updated_conversation = next(
        item for item in conversations if item["id"] == conversation_id
    )

    assert updated_conversation["title"] == initial_title
    assert updated_conversation["updated_at"] > previous_activity

    print("All concurrency checks passed.")
    print(f"Conversation ID: {conversation_id}")


if __name__ == "__main__":
    main()
