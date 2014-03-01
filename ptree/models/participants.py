from ptree.db import models
import ptree.constants as constants
from ptree.common import currency
import ptree.sessionlib.models
from ptree.common import add_params_to_url
import ptree.models.subsessions
from ptree.user.models import User


class BaseParticipant(User):
    """
    Base class for all participants.
    """

    index_among_participants_in_match = models.PositiveIntegerField(null = True)
    bonus = models.PositiveIntegerField(null=True)

    session_participant = models.ForeignKey(
        ptree.sessionlib.models.SessionParticipant,
        related_name = '%(app_label)s_%(class)s'
    )

    @property
    def session_user(self):
        return self.session_participant

    def name(self):
        return self.session_participant.__unicode__()

    def __unicode__(self):
        return self.name()

    def start_url(self):
        return add_params_to_url(self.subsession.start_url(), {constants.user_code: self.code})

    def pages_as_urls(self):
        from ptree.views.concrete import WaitUntilAssignedToMatch
        code = self.session_user.code
        if self.treatment:
            # 2/11/2014: start at 1 because i added the wait page (until assigned to match)
            # maybe should clean this up.
            # 2/22/2014: i shouldn't have WaitUntilAssignedToMatch because if they were assigned to a match & treatment,
            # they wouldn't access this in the first place.
            # but this must still work if you look up an element.
            all_views = [WaitUntilAssignedToMatch] + self.treatment.pages()
            return [View.url(index, code) for index, View in enumerate(all_views)]
        return [WaitUntilAssignedToMatch.url(0, code)]

    class Meta:
        abstract = True
        ordering = ['pk']

    def add_to_existing_match(self, match):
        self.index_among_participants_in_match = match.participant_set.count()
        self.match = match
        self.save()

    def add_to_existing_or_new_match(self):
        if not self.match:
            MatchClass = self._meta.get_field('match').rel.to
            match = self.treatment.next_open_match() or ptree.common.create_match(MatchClass, self.treatment)
            self.add_to_existing_match(match)

    def pages_completed(self):
        if not (self.treatment and self.visited):
            return None
        return '{}/{}'.format(self.index_in_pages,
                            len(self.treatment.pages()))