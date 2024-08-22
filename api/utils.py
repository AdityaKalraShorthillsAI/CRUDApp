import re

class Utils:
    @staticmethod
    def slugify(title):
        slug = title.lower()
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        slug = slug.strip('-')
        max_length = 255
        return slug[:max_length]