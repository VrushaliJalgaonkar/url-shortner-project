# from django.db import models
# import string
# from django.utils import timezone
# from datetime import timedelta
# # Create your models here.

# BASE62_ALPHABET = string.ascii_letters + string.digits  # "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# # Function to convert an integer ID to Base62

# def encode_base62(num):
#     if num == 0:
#         return BASE62_ALPHABET[0]
#     base62 = []
#     while num:
#         num, rem = divmod(num, 62)
#         base62.append(BASE62_ALPHABET[rem])
#     return ''.join(reversed(base62))

# class ShortenedUrl(models.Model):
#     short_url_code = models.CharField(max_length=10, unique=True, blank=True)
#     long_url = models.URLField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=7))
#     clicks = models.IntegerField(default=0)

#     def save(self, *args, **kwargs):
#         if not self.short_code:
#             self.short_code = encode_base62(self.pk)  # Convert numeric ID to Base62
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.short_code} → {self.long_url}"

