from django.test import TestCase


class TestHomeViews(TestCase):

    def test_index_page_response(self):
        page = self.client.get("/", content_type="html/text", follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "bestsellers.html")
