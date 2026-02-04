# test_basic.py
"""Basic tests for CompliFriend bot"""
import pytest
from predictions import (
    MOTIVATION,
    PREDICTIONS,
    get_random_message
)


def test_motivation_list_not_empty():
    """Test that MOTIVATION list is not empty"""
    assert len(MOTIVATION) > 0


def test_predictions_list_not_empty():
    """Test that PREDICTIONS list is not empty"""
    assert len(PREDICTIONS) > 0


def test_get_random_message_returns_string():
    """Test that get_random_message returns a string"""
    result = get_random_message(PREDICTIONS)
    assert isinstance(result, str)


def test_get_random_message_returns_from_list():
    """Test that get_random_message returns item from provided list"""
    test_messages = ["message1", "message2", "message3"]
    result = get_random_message(test_messages)
    assert result in test_messages


def test_combined_list():
    """Test that PREDICTIONS + MOTIVATION can be combined"""
    combined = PREDICTIONS + MOTIVATION
    assert len(combined) == len(PREDICTIONS) + len(MOTIVATION)


def test_all_messages_are_strings():
    """Test that all messages are strings"""
    for msg in PREDICTIONS:
        assert isinstance(msg, str)
    for msg in MOTIVATION:
        assert isinstance(msg, str)
