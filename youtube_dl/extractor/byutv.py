from __future__ import unicode_literals

import json
import re

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
)


class BYUtvIE(InfoExtractor):
    _VALID_URL = r'^https?://(?:www\.)?byutv.org/watch/[0-9a-f-]+/(?P<video_id>[^/?#]+)'
    _TEST = {
        'url': 'http://www.byutv.org/watch/44e80f7b-e3ba-43ba-8c51-b1fd96c94a79/granite-flats-talking',
        'info_dict': {
            'id': 'granite-flats-talking',
            'ext': 'mp4',
            'description': 'md5:1a7ae3e153359b7cc355ef3963441e5f',
            'title': 'Talking',
            'thumbnail': 're:^https?://.*promo.*'
        },
        'params': {
            'skip_download': True,
        }
    }

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('video_id')

        webpage = self._download_webpage(url, video_id)
        episode_code = self._search_regex(
            r'(?s)episode:(.*?\}),\s*\n', webpage, 'episode information')
        episode_json = re.sub(
            r'(\n\s+)([a-zA-Z]+):\s+\'(.*?)\'', r'\1"\2": "\3"', episode_code)
        ep = json.loads(episode_json)

        if ep['providerType'] == 'Ooyala':
            return {
                '_type': 'url_transparent',
                'ie_key': 'Ooyala',
                'url': 'ooyala:%s' % ep['providerId'],
                'id': video_id,
                'title': ep['title'],
                'description': ep.get('description'),
                'thumbnail': ep.get('imageThumbnail'),
            }
        else:
            raise ExtractorError('Unsupported provider %s' % ep['provider'])
