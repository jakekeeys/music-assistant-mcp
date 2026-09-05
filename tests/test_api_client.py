"""Minimal check for parse_library_uri. Run: python tests/test_api_client.py"""

from music_assistant_mcp.client.api_client import MusicAssistantError, parse_library_uri

assert parse_library_uri("library://track/42") == ("track", "42")
assert parse_library_uri("library://album/abc/def") == ("album", "abc/def")
for bad in ("spotify://track/42", "library://track", "library://", "42"):
    try:
        parse_library_uri(bad)
    except MusicAssistantError:
        pass
    else:
        raise AssertionError(f"should reject {bad!r}")
print("ok")
