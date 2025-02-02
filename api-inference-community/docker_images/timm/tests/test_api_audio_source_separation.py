import os
from unittest import TestCase, skipIf

from app.main import ALLOWED_TASKS
from app.validation import ffmpeg_read
from starlette.testclient import TestClient
from tests.test_api import TESTABLE_MODELS


@skipIf(
    "audio-source-separation" not in ALLOWED_TASKS,
    "audio-source-separation not implemented",
)
class AudioSourceSeparationTestCase(TestCase):
    def setUp(self):
        model_id = TESTABLE_MODELS["audio-source-separation"]
        self.old_model_id = os.getenv("MODEL_ID")
        self.old_task = os.getenv("TASK")
        os.environ["MODEL_ID"] = model_id
        os.environ["TASK"] = "audio-source-separation"
        from app.main import app

        self.app = app

    def tearDown(self):
        os.environ["MODEL_ID"] = self.old_model_id
        os.environ["TASK"] = self.old_task

    def read(self, filename: str) -> bytes:
        dirname = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dirname, "samples", filename)
        with open(filename, "rb") as f:
            bpayload = f.read()
        return bpayload

    def test_simple(self):
        bpayload = self.read("sample1.flac")

        with TestClient(self.app) as client:
            response = client.post("/", data=bpayload)

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(response.header["content-type"], "audio/wav")
        audio = ffmpeg_read(response.content)
        self.assertEqual(audio.shape, (10,))

    def test_malformed_audio(self):
        bpayload = self.read("malformed.flac")

        with TestClient(self.app) as client:
            response = client.post("/", data=bpayload)

        self.assertEqual(
            response.status_code,
            400,
        )
        self.assertEqual(response.content, b'{"error":"Malformed soundfile"}')

    def test_dual_channel_audiofile(self):
        bpayload = self.read("sample1_dual.ogg")

        with TestClient(self.app) as client:
            response = client.post("/", data=bpayload)

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(response.header["content-type"], "audio/wav")
        audio = ffmpeg_read(response.content)
        self.assertEqual(audio.shape, (10,))

    def test_webm_audiofile(self):
        bpayload = self.read("sample1.webm")

        with TestClient(self.app) as client:
            response = client.post("/", data=bpayload)

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(response.header["content-type"], "audio/wav")
        audio = ffmpeg_read(response.content)
        self.assertEqual(audio.shape, (10,))
