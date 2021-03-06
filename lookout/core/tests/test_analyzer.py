import io
import unittest

from lookout.core.analyzer import Analyzer, DummyAnalyzerModel, ReferencePointer


class FakeAnalyzer(Analyzer):
    version = 7
    model_type = DummyAnalyzerModel
    name = "fake"
    vendor = "source{d}"


class AnalyzerTests(unittest.TestCase):
    def test_dummy_model(self):
        ptr = ReferencePointer("1", "2", "3")
        model = DummyAnalyzerModel.generate(FakeAnalyzer, ptr)
        self.assertEqual(model.name, FakeAnalyzer.name)
        self.assertEqual(model.version, [FakeAnalyzer.version])
        self.assertEqual(model.ptr, ptr)
        self.assertEqual(model.vendor, "source{d}")
        self.assertEqual(model.description, "Model bound to fake Lookout analyzer.")
        buffer = io.BytesIO()
        model.save(buffer)
        buffer.seek(0)
        model2 = model.load(buffer)
        self.assertEqual(model.ptr, model2.ptr)
        self.assertEqual(model.name, model2.name)
        self.assertEqual(model.description, model2.description)
        self.assertEqual(model.vendor, model2.vendor)


if __name__ == "__main__":
    unittest.main()
