"""Routing tests for harvestkit.publish — no network.

Only the collection -> HF repo-id namespace SELECTION is under test here
(the old filename-substring heuristic replaced by an explicit `collection`
argument). Upload/push behaviour is out of scope and never exercised.
"""
from __future__ import annotations

from harvestkit.publish import COLLECTIONS, resolve_repo_id


def test_media_metadata_collection_routes_to_ledata_media_metadata_prefix():
    repo_id = resolve_repo_id("tvmaze_shows", collection="media-metadata")
    assert repo_id == "LeData/media-metadata-tvmaze-shows"


def test_drugs_and_substances_collection_routes_to_ledata_drugs_prefix():
    repo_id = resolve_repo_id("unified_drugs", collection="drugs-and-substances")
    assert repo_id == "LeData/drugs-and-substances-unified-drugs"


def test_default_collection_is_media_metadata():
    assert resolve_repo_id("some_source") == resolve_repo_id(
        "some_source", collection="media-metadata"
    )


def test_org_override_changes_namespace_only():
    repo_id = resolve_repo_id("tvmaze_shows", collection="media-metadata", org="Acme")
    assert repo_id == "Acme/media-metadata-tvmaze-shows"


def test_unknown_collection_rejected():
    import pytest

    with pytest.raises(ValueError):
        resolve_repo_id("x", collection="not-a-real-collection")


def test_known_collections_are_exactly_media_metadata_and_drugs():
    assert set(COLLECTIONS) == {"media-metadata", "drugs-and-substances"}
