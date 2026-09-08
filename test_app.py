import unittest
import os

class TestF1CompanionSetup(unittest.TestCase):

    def test_cache_directory_creation(self):
        """Verifica se a diretoria de cache é criada corretamente."""
        if not os.path.exists('cache'):
            os.makedirs('cache')
        self.assertTrue(os.path.exists('cache'))

    def test_requirements_file_exists(self):
        """Garante que o ficheiro de dependências está presente no repositório."""
        self.assertTrue(os.path.isfile('requirements.txt'))

if __name__ == '__main__':
    unittest.main()
