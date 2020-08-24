import random
import string

from slugify import slugify
from django.db import models
from django.utils.crypto import get_random_string


def generate_random_slug():
    return get_random_string(8, "0123456789")  # 8 characters, only digits.


def create_unique_slug(value, model, object_pk, max_length=45):
    """Create a unique slug from value.

    Args:
        value (str): Value to slugify.
        model: Model to check against for uniqueness.
        object_pk: Object PK of the one we are creating the slug for.
        max_length (int): Maximal length of the slug before appending the
            number to provide uniqueness.

    Returns:
        str: Unique slug.
    """
    # Always exclude the existing object this is important because when we set
    # slug=None, while this values is not yet saved to the database, it will
    # come up as a collision with the saved database value of the same object.
    queryset = model.objects.exclude(pk=object_pk)

    # First create a slug
    slug_words = slugify(value).split("-")
    slug = slug_words[0]
    for word in slug_words[1:]:
        new_slug = f"{slug}-{word}"
        if len(new_slug) <= max_length:
            slug = new_slug
        else:
            break

    # Now check for uniqueness
    slug_count = queryset.filter(slug=slug).count()
    if slug_count == 0:
        return slug
    else:
        for i in range(slug_count, 10000):
            new_slug = f"{slug}-{i}"
            if queryset.filter(slug=new_slug).count() == 0:
                return new_slug

        # This should never happen but let's be prepared
        word = "".join(random.choice(string.ascii_lowercase) for _ in range(4))
        return f"{slug}-{word}"


class SlugMixinBase(models.Model):
    """Base class for unique and non unique slugs."""

    SLUG_FIELD = "name"

    def _slug_value(self):
        """Return a string value from which the slug will be created."""
        return getattr(self, self.SLUG_FIELD, str(self))

    @classmethod
    def get_by_slug(cls, slug: str, **kwargs):
        """Get an object by it's slug.

        Args:
             slug (str): Search slug

        Returns:
            Queried object.

        Raises:
            ObjectNotFound: If the object is not found.
        """
        return cls.objects.get(slug=slug, **kwargs)

    @classmethod
    def get_by_slug_field(cls, value: str, **kwargs):
        return cls.get_by_slug(slug=slugify(value), **kwargs)

    class Meta:
        app_label = "tea_django"
        abstract = True


class UniqueSlugMixin(SlugMixinBase):
    """Mixin for models with unique slug field.

    Fields:
        slug: Slug field.
    """

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        # FIXME: Do this only when the slug field changes.
        self.slug = create_unique_slug(
            value=self._slug_value(), model=self.__class__, object_pk=self.pk,
        )
        super().save(*args, **kwargs)

    class Meta:
        app_label = "tea_django"
        abstract = True


class NonUniqueSlugMixin(SlugMixinBase):
    """Mixin for models with non-unique slug field.

    Fields:
        slug: Slug field.
    """

    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self._slug_value())
        super().save(*args, **kwargs)

    class Meta:
        app_label = "tea_django"
        abstract = True
