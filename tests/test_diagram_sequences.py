"""
Tests for diagram_sequences.get_diagram_sequence().

Covers:
  - Known slug returns a non-empty list of step dicts
  - Each step dict has 'src' and 'caption' keys
  - Unknown slug returns None (does not raise)
  - Empty-string slug returns None
  - The hash-map sequence has exactly the expected 5 steps
  - The linked-list sequence has exactly the expected 4 steps with correct captions
  - Step src paths are relative (no leading slash) and end in a known image ext
"""
import pytest

from diagram_sequences import get_diagram_sequence, DIAGRAM_SEQUENCES


class TestKnownSlug:
    def test_hash_map_returns_list(self):
        result = get_diagram_sequence("hash-map")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_hash_map_has_five_steps(self):
        result = get_diagram_sequence("hash-map")
        assert len(result) == 5

    def test_each_step_has_src_and_caption(self):
        result = get_diagram_sequence("hash-map")
        for step in result:
            assert "src" in step, f"Step missing 'src': {step}"
            assert "caption" in step, f"Step missing 'caption': {step}"

    def test_src_paths_are_relative(self):
        result = get_diagram_sequence("hash-map")
        for step in result:
            assert not step["src"].startswith("/"), (
                f"src should be relative (no leading slash): {step['src']}"
            )

    def test_src_paths_have_image_extension(self):
        valid_exts = {".png", ".svg", ".jpg", ".jpeg", ".webp", ".gif"}
        result = get_diagram_sequence("hash-map")
        for step in result:
            src = step["src"].lower()
            assert any(src.endswith(ext) for ext in valid_exts), (
                f"src doesn't look like an image path: {step['src']}"
            )

    def test_captions_are_non_empty_strings(self):
        result = get_diagram_sequence("hash-map")
        for step in result:
            assert isinstance(step["caption"], str)
            assert step["caption"].strip() != ""


class TestLinkedListSequence:
    def test_linked_list_returns_list(self):
        result = get_diagram_sequence("linked-list")
        assert isinstance(result, list)

    def test_linked_list_has_four_steps(self):
        result = get_diagram_sequence("linked-list")
        assert len(result) == 4

    def test_linked_list_captions_in_order(self):
        result = get_diagram_sequence("linked-list")
        expected_captions = [
            "Original list: A → B → C → null.",
            "New node X is created, but not yet connected to the list.",
            "X's pointer is set to point at C — link the new node forward first.",
            "B's pointer is redirected from C to X. Final: A → B → X → C → null.",
        ]
        actual_captions = [step["caption"] for step in result]
        assert actual_captions == expected_captions

    def test_linked_list_srcs_point_to_correct_dir(self):
        result = get_diagram_sequence("linked-list")
        for step in result:
            assert "linked-list" in step["src"], (
                f"Expected src to reference linked-list dir: {step['src']}"
            )


class TestUnknownSlug:
    def test_unknown_slug_returns_none(self):
        assert get_diagram_sequence("nonexistent-lesson") is None

    def test_empty_string_returns_none(self):
        assert get_diagram_sequence("") is None

    def test_does_not_raise_for_any_string(self):
        for slug in ["", "   ", "hash-map-2", "!!!", "a" * 200]:
            try:
                get_diagram_sequence(slug)
            except Exception as exc:
                pytest.fail(f"get_diagram_sequence({slug!r}) raised {type(exc).__name__}: {exc}")


class TestDataIntegrity:
    def test_all_sequences_are_lists(self):
        for slug, seq in DIAGRAM_SEQUENCES.items():
            assert isinstance(seq, list), f"{slug}: expected list, got {type(seq)}"

    def test_all_sequences_non_empty(self):
        for slug, seq in DIAGRAM_SEQUENCES.items():
            assert len(seq) > 0, f"{slug}: sequence is empty"

    def test_step_srcs_are_unique_within_sequence(self):
        for slug, seq in DIAGRAM_SEQUENCES.items():
            srcs = [s["src"] for s in seq]
            assert len(srcs) == len(set(srcs)), (
                f"{slug}: duplicate src paths found: {srcs}"
            )
