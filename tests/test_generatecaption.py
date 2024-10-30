import unittest
import sys
from PIL import Image
from src.generatecaption import generate_caption_image
from src import config


class TestGenerateCaption(unittest.TestCase):
    show = config.show_test_result_images
    def test_generate_caption_image_hu(self):
        rawtext = "Árvíztűrő tükörfúrógép"
        result = generate_caption_image(rawtext)
        self.assertIsInstance(result, Image.Image)

        if self.show:
            result.show()

    def test_generate_caption_image_emoji(self):
        rawtext = ":3 <3 :+1: :skull: 🦊 🐱"
        result = generate_caption_image(rawtext)
        self.assertIsInstance(result, Image.Image)

        if self.show:
            result.show()

    def test_generate_caption_image_long(self):
        rawtext = "faliure after " * 32
        result = generate_caption_image(rawtext)
        self.assertIsInstance(result, Image.Image)

        if self.show:
            result.show()

    def test_generate_caption_image_emote(self):
        rawtext = "<:floraSmug:1112288234488201307> " * 40
        result = generate_caption_image(rawtext)
        self.assertIsInstance(result, Image.Image)

        if self.show:
            result.show()

    def test_generate_caption_image_longword(self):
        rawtext = "test_generate_caption_image_longword_" + "A" * 100 
        result = generate_caption_image(rawtext)
        self.assertIsInstance(result, Image.Image)

        if self.show:
            result.show()

if __name__ == "__main__":
    unittest.main()
