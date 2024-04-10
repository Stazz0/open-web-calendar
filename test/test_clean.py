"""Test cleaning the HTML input."""
import pytest
from clean_html import clean_html, remove_html
from pprint import pprint


@pytest.mark.parametrize(
    "input,spec,expected_output",
    [
        ("<script>js</script>a", {"clean_html_scripts":True}, "a"),
        ("<malicious>", {"clean_html_remove_unknown_tags":True}, "")
    ]
)
def test_clean_html_from_spec(input, spec, expected_output):
    """Specify how to clean the HTML content."""
    output = clean_html(input, spec=spec).replace("\n", "")
    assert output == expected_output


def test_remove_html():
    """Remove all HTML tags - we do not expect them in the summary."""
    assert remove_html("<asd>aaa</asd>bbb") == "aaabbb"
    assert remove_html("><<<>") == ">"


def test_nice_id_for_event(client, calendar_urls):
    """Make sure that we have nice IDs without HTML in them."""
    response = client.get(f"/calendar.events.json?url={calendar_urls['one-event']}&timezone=Europe/London&from=2019-03-04&to=2019-03-05")
    event = response.json[0]
    pprint(event)
    assert not " " in event["id"]
    assert not ":" in event["id"]
