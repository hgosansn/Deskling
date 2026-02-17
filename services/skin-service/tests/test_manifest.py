import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'services' / 'skin-service'))

from manifest import ManifestError, load_manifest, validate_manifest  # noqa: E402


class ManifestTests(unittest.TestCase):
    def _manifest(self):
        return {
            'id': 'default_skin',
            'name': 'Default Skin',
            'version': '1.0.0',
            'assets': {
                'idle': 'assets/idle.txt',
                'talk': 'assets/talk.txt',
                'emotion': 'assets/emotion.txt'
            }
        }

    def test_validate_manifest_success(self):
        manifest = self._manifest()
        self.assertEqual(validate_manifest(manifest), manifest)

    def test_validate_manifest_missing_keys(self):
        manifest = self._manifest()
        del manifest['id']
        with self.assertRaises(ManifestError) as err:
            validate_manifest(manifest)
        self.assertEqual(err.exception.code, 'ERR_MANIFEST_KEYS')

    def test_load_manifest_from_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'manifest.json'
            path.write_text(json.dumps(self._manifest()), encoding='utf-8')
            loaded = load_manifest(path)
            self.assertEqual(loaded['id'], 'default_skin')


if __name__ == '__main__':
    unittest.main()
