"""
Many of the sessions at the conference are recorded and the videos
are then posted to YouTube.  The A/V team makes a spreadsheet available
from their workflow that includes columns with the URL for the presentation,
here, in sympsion, and the URL for the video on YouTube.

This module contains the function(s) used by the update_video_urls management
command to update the ``video_url`` attribute of the *Presentation* model
instances with this information.

The input is a CSV file wherein columns 4 and 5 contain the pycon and youtube
URLs, respectively.  The last part of the path in the pycon URL is the pk of
*Presentation* instance.  If this is non-empty (i.e., a positive integer),
the ``video_url`` attribute of the instance can be updated with the corresponding
youtube URL.
"""
import logging
log = logging.getLogger(__file__)

import csv
from symposion.schedule.models import Presentation

class VideoURLUpdater(object):
    '''
    Handles digestion of A/V CSV file that includes columns for
    symposion (i.e. pycon) Presentation and youtube video URLs
    and updating of the Presentation model ``video_url`` property.
    These are expected to be in columns 4 and 5 of the spreadsheet,
    but this can be overridden with the ``pr_col`` and ``yt_col``
    arguments.

    Note that the ``__len__`` special method returns possibly different
    results, depending on whether or not ``empty_only`` is ``True`` or
    not.  If it is, then only updates to empty or blank ``video_url``
    fields will be performed.  Existing, non-empty fields will be left
    unalterned.
    '''

    def __init__(self, csv_file, pr_col=4, yt_col=5, pkndx=2):

        # The presentation url will be of the form:
        #   .../presentation/nnn/
        # The nnn is a positive integer that is the pk
        # for thie Presentation instance. The ``split``
        # string method, using '/' as the delimiter will
        # return the path elements and the pk will be the
        # ``pkndx``-to-last of these.  (DO NOT CHANGE THIS
        # UNLESS YOU REALLY KNOW WHAT YOU'RE DOING, OK?)
        self._rows = dict([[r[pr_col].split('/')[-pkndx], r[yt_col]] \
            for r in csv.reader(open(csv_file)) \
                if r[pr_col] not in (None, '')])

        self._len = len(self._rows)

    def update(self, empty_only=False):
        '''
        Update the database.

        If ``empty_only`` is ``True`` then only update those instances
        where ``video_url`` is blank.  Otherwise, this effectively
        clears any existing Youtube video URL from the corresponding
        presentation's ``video_url`` property.
        '''
        actual = 0
        for ppk, yt_url in self._rows.items():
            try:
                prez = Presentation.objects.filter(pk=ppk).exclude(cancelled=True)

                if empty_only:
                    prez = prez.filter(video_url__exact='')
                    actual += prez.count()
                prez.update(video_url=yt_url)

            except Exception as e:
                log.error(e)
                return False

        if empty_only:
            self._len = actual

        return True

    def __len__(self):
        return self._len

    def __getitem__(self, key):
        return self._rows.get(str(key) if isinstance(key, int) else key, None)
