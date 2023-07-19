from pathlib import Path
from unittest import mock

import pytest

from exceptions.virus_found import VirusFoundError
from utils import music_utils
from utils.music_utils import MusicUtils


@mock.patch.object(music_utils.MusicUtils, "scan_file")
def test_scan_file(mock_scan):
    mock_scan.side_effect = VirusFoundError("")
    valid_file_name = f"{Path(__file__).parent.parent}/files/EICAR-clamav-testfile.mp3"
    with pytest.raises(VirusFoundError):
        MusicUtils.scan_file(valid_file_name)
