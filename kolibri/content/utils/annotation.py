import fnmatch
import os

from django.conf import settings

from ..content_db_router import using_content_database
from ..models import ChannelMetadata, ChannelMetadataCache


def _get_channel_list_from_scanning_contentdb_dir():
    db_list = fnmatch.filter(os.listdir(settings.CONTENT_DATABASE_DIR), '*.sqlite3')
    db_names = [db.split('.sqlite3', 1)[0] for db in db_list]
    return db_names


def sync_channelmetadata():
    """
    Everytime kolibri runs, scan through the settings.CONTENT_DATABASE_DIR folder to collect the names for all ContentDB,
    and use the name to query each ContentDB to get the ChannelMetadata object,
    and use them to update the ChannelMetadata object in the default database to ensure they are insync
    """
    db_names = _get_channel_list_from_scanning_contentdb_dir()
    # delete channelmetadata obejcts in default db that cannot be found in CONTENT_DATABASE_DIR
    ChannelMetadataCache.objects.exclude(id__in=db_names).delete()
    # sync the channelmetadata objects in default db with channelmetadata objects in CONTENT_DATABASE_DIR
    for db_name in db_names:
        with using_content_database(db_name):
            update_values = ChannelMetadata.objects.values()[0]
        ChannelMetadataCache.objects.update_or_create(id=db_name, defaults=update_values)