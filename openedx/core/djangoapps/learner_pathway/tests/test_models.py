"""
Unit tests for LearnerPathwayProgress models.
"""


from uuid import UUID

import ddt
from django.test import TestCase
from opaque_keys.edx.keys import CourseKey

from common.djangoapps.course_modes.models import CourseMode
from common.djangoapps.student.tests.factories import CourseEnrollmentFactory, UserFactory
from openedx.core.djangoapps.content.course_overviews.tests.factories import CourseOverviewFactory

from ..models import LearnerPathwayProgress
from .constants import LearnerPathwayProgressOutputs
from .factories import LearnerPathwayProgressFactory


@ddt.ddt
class LearnerPathwayProgressModelTests(TestCase):
    """
    Tests for the LearnerPathwayProgress model.
    """
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.user = UserFactory(username="rocky")
        self.learner_pathway_uuid = UUID("1f301a72-f344-4a31-9e9a-e0b04d8d86b1")
        self.program1_uuid = UUID("1f301a72-f344-4a31-9e9a-e0b04d8d86b2")
        self.program2_uuid = UUID("1f301a72-f344-4a31-9e9a-e0b04d8d86b3")
        self.course_keys = []
        for i in range(8):
            self.course_keys.insert(i, CourseKey.from_string(f"course-v1:test-enterprise+test1+202{i}"))
            CourseOverviewFactory(id=self.course_keys[i])
            self.course_enrollment = CourseEnrollmentFactory.create(
                course_id=self.course_keys[i],
                user=self.user,
                mode=CourseMode.VERIFIED
            )
        LearnerPathwayProgressFactory.create(
            user=self.user,
            learner_pathway_uuid=self.learner_pathway_uuid,
        )

    def test_update_progress(self):
        """
        Make sure the update_progress method works correctly.
        """
        learner_pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=self.learner_pathway_uuid
        ).first()
        self.assertEqual(
            learner_pathway_progress.learner_pathway_progress,
            LearnerPathwayProgressOutputs.snapshot_from_discovery
        )
        learner_pathway_progress.update_pathway_progress()
        updated_learner_pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=self.learner_pathway_uuid
        ).first()
        self.assertEqual(
            updated_learner_pathway_progress.learner_pathway_progress,
            LearnerPathwayProgressOutputs.updated_learner_progress
        )
