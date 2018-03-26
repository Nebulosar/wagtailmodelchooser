from django.db import models
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.blocks import RichTextBlock
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsearch.queryset import SearchableQuerySetMixin

from wagtailmodelchooser import Chooser, register_model_chooser
from wagtailmodelchooser.blocks import ModelChooserBlock
from wagtailmodelchooser.edit_handlers import ModelChooserPanel


class AuthorQuerySet(SearchableQuerySetMixin, models.QuerySet):
    pass


@register_model_chooser(icon='user')
class Author(models.Model, index.Indexed):
    name = models.CharField(max_length=255)

    search_fields = [
        index.SearchField('name'),
    ]

    objects = AuthorQuerySet.as_manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(Page):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)

    content_panels = Page.content_panels + [
        ModelChooserPanel('author'),
    ]


@register_model_chooser
class BookChooser(Chooser):
    model = Book
    icon = 'form'


class ContentPage(Page):
    body = StreamField([
        ('text', RichTextBlock()),
        ('author', ModelChooserBlock(Author)),
        ('book', ModelChooserBlock(Book)),
    ])

    favourite_book = models.ForeignKey(
        Book, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+')

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        ModelChooserPanel('favourite_book'),
    ]
