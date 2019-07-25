from plone.app.standardtiles import PloneMessageFactory as _
from plone.app.uuid.utils import uuidToObject
from plone.app.vocabularies.catalog import CatalogSource as CatalogSourceBase
from plone.memoize.view import memoize
from plone.supermodel import model
from plone.tiles import Tile
from plone.uuid.interfaces import IUUID
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary


class CatalogSource(CatalogSourceBase):
    """ExistingContentTile specific catalog source to allow targeted widget
    """


class IPresentationTile(model.Schema):

    content_uid = schema.Choice(
        title=_(u"Select an existing content"),
        required=True,
        source=CatalogSource(portal_type=['presentation', 'training_class']),
    )


class PresentationTile(Tile):
    """Existing content tile
    """

    @property
    @memoize
    def content_context(self):
        uuid = self.data.get('content_uid')
        item = uuidToObject(uuid)
        if item is not None:
            return item
        return None

    @property
    def length(self):
        return self.data.get('talk_length')

    @property
    @memoize
    def speaker(self):
        content = self.content_context
        speaker_uids = getattr(content, 'speaker', None)
        if speaker_uids:
            speakers = [uuidToObject(u) for u in speaker_uids]
            return ', '.join(s.title for s in speakers if s)
