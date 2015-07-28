from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from model_mommy import mommy

from users.models import MflUser
from facilities.models import Facility, FacilityApproval
from facilities.tests.test_facility_views import load_dump


from common.tests.test_views import default


class TestFacilityFilterApprovedAndPublished(APITestCase):
    def setUp(self):
        self.url = reverse("api:facilities:facilities_list")
        self.view_unpublished_perm = Permission.objects.get(
            codename="view_unpublished_facilities")
        self.view_approved_perm = Permission.objects.get(
            codename="view_unapproved_facilities")
        self.view_classified_perm = Permission.objects.get(
            codename="view_classified_facilities")
        self.public_group = mommy.make(Group, name="public")
        view_fields_perm = Permission.objects.get(
            codename='view_all_facility_fields')
        self.admin_group = mommy.make(Group, name="mfl admins")
        self.admin_group.permissions.add(self.view_unpublished_perm.id)
        self.admin_group.permissions.add(self.view_approved_perm.id)
        self.admin_group.permissions.add(self.view_classified_perm.id)
        self.admin_group.permissions.add(view_fields_perm.id)

        self.admin_user = mommy.make(MflUser, first_name='admin')
        self.public_user = mommy.make(MflUser, first_name='public')

        self.public_user.groups.add(self.public_group)
        self.admin_user.groups.add(self.admin_group)

        self.assertTrue(self.admin_user.has_perm(
            "facilities.view_unpublished_facilities"))
        self.assertTrue(self.admin_user.has_perm(
            "facilities.view_unapproved_facilities"))
        self.assertTrue(self.admin_user.has_perm(
            "facilities.view_classified_facilities"))

        super(TestFacilityFilterApprovedAndPublished, self).setUp()

    def test_public_cant_see_unpublished_facilities(self):
        mommy.make(Facility)
        mommy.make(Facility, rejected=True)
        facility_2 = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility_2)
        self.assertTrue(facility_2.approved)
        facility_2.is_published = True
        facility_2.save()

        # test admin user sees all facilities
        self.client.force_authenticate(self.admin_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(2, admin_response.data.get("count"))
        for obj in admin_response.data.get("results"):
            self.assertFalse(Facility.objects.get(id=obj.get('id')).rejected)

        # test public user sees only published facilties
        self.client.logout()
        self.client.force_authenticate(self.public_user)
        public_response = self.client.get(self.url)
        self.assertEquals(200, public_response.status_code)
        self.assertEquals(1, public_response.data.get("count"))
        for obj in public_response.data.get("results"):
            self.assertTrue(
                Facility.objects.get(id=obj.get('id')).is_published)

    def test_public_cant_see_unapproved_facilities(self):
        mommy.make(Facility)
        facility_2 = mommy.make(Facility, approved=True)
        mommy.make(FacilityApproval, facility=facility_2)
        facility_2.is_published = True
        facility_2.save()

        # test admin user sees all facilities
        self.client.force_authenticate(self.admin_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(2, admin_response.data.get("count"))

        # test public user sees only approved facilties
        self.client.logout()
        self.client.force_authenticate(self.public_user)
        public_response = self.client.get(self.url)
        self.assertEquals(200, public_response.status_code)
        self.assertEquals(1, public_response.data.get("count"))
        for obj in public_response.data.get("results"):
            self.assertTrue(
                Facility.objects.get(id=obj.get('id')).approved)

    def test_public_cant_see_classified_facilities(self):
        mommy.make(Facility, is_classified=True)
        facility_2 = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility_2)
        facility_2.is_published = True
        facility_2.save()

        # test admin user sees all facilities
        self.client.force_authenticate(self.admin_user)
        admin_response = self.client.get(self.url)
        self.assertEquals(200, admin_response.status_code)
        self.assertEquals(2, admin_response.data.get("count"))

        # test public user sees only non classified facilties
        self.client.logout()
        self.client.force_authenticate(self.public_user)
        public_response = self.client.get(self.url)
        self.assertEquals(200, public_response.status_code)
        self.assertEquals(1, public_response.data.get("count"))
        for obj in public_response.data.get("results"):
            self.assertFalse(
                Facility.objects.get(id=obj.get('id')).is_classified)

    def test_public_user_does_not_see_non_public_fields(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        facility.is_published = True
        facility.save()
        self.client.force_authenticate(self.public_user)
        response = self.client.get(self.url)
        all_data = load_dump(response.data['results'], default=default)
        data = all_data[0]
        self.assertIsNone(data.get('has_edits'))
        self.assertIsNone(data.get('is_approved'))
        self.assertIsNone(data.get('latest_update'))
        self.assertIsNone(data.get('deleted'))
        self.assertIsNone(data.get('active'))
        self.assertIsNone(data.get('search'))
        self.assertIsNone(data.get('is_classified'))
        self.assertIsNone(data.get('is_published'))
        self.assertIsNone(data.get('regulated'))
        self.assertIsNone(data.get('approved'))
        self.assertIsNone(data.get('rejected'))
        self.assertIsNone(data.get('created_by'))
        self.assertIsNone(data.get('updated_by'))

    def test_public_user_does_not_see_non_public_fields_on_detail(self):
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        facility.is_published = True
        facility.save()
        self.client.force_authenticate(self.public_user)
        url = self.url + "{}/".format(facility.id)
        response = self.client.get(url)
        data = load_dump(response.data, default=default)
        self.assertIsNone(data.get('has_edits'))
        self.assertIsNone(data.get('is_approved'))
        self.assertIsNone(data.get('latest_update'))
        self.assertIsNone(data.get('deleted'))
        self.assertIsNone(data.get('active'))
        self.assertIsNone(data.get('search'))
        self.assertIsNone(data.get('is_classified'))
        self.assertIsNone(data.get('is_published'))
        self.assertIsNone(data.get('regulated'))
        self.assertIsNone(data.get('approved'))
        self.assertIsNone(data.get('rejected'))
        self.assertIsNone(data.get('created_by'))
        self.assertIsNone(data.get('updated_by'))

    def test_admin_user_sees_all_fields_list_endpoint(self):
        perm = Permission.objects.get(codename="view_all_facility_fields")
        self.admin_group.permissions.add(perm.id)
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        facility.is_published = True
        facility.save()
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(self.url)
        all_data = load_dump(response.data['results'], default=default)
        data = all_data[0]
        self.assertIsNone(data.get('has_edits'))
        self.assertIsNone(data.get('is_approved'))
        self.assertIsNone(data.get('latest_update'))
        self.assertIsNone(data.get('deleted'))
        self.assertIsNone(data.get('active'))
        self.assertIsNone(data.get('search'))
        self.assertIsNone(data.get('is_classified'))
        self.assertIsNone(data.get('is_published'))
        self.assertIsNone(data.get('regulated'))
        self.assertIsNone(data.get('approved'))
        self.assertIsNone(data.get('rejected'))
        self.assertIsNone(data.get('created_by'))
        self.assertIsNone(data.get('updated_by'))

    def test_admin_user_sees_all_fields_on_detail(self):
        perm = Permission.objects.get(codename="view_all_facility_fields")
        self.admin_group.permissions.add(perm.id)
        facility = mommy.make(Facility)
        mommy.make(FacilityApproval, facility=facility)
        self.client.force_authenticate(self.admin_user)
        url = self.url + "{}/".format(facility.id)
        response = self.client.get(url)
        data = load_dump(response.data, default=default)
        self.assertIsNone(data.get('has_edits'))
        self.assertIsNone(data.get('is_approved'))
        self.assertIsNone(data.get('latest_update'))
        self.assertIsNone(data.get('deleted'))
        self.assertIsNone(data.get('active'))
        self.assertIsNone(data.get('search'))
        self.assertIsNone(data.get('is_classified'))
        self.assertIsNone(data.get('is_published'))
        self.assertIsNone(data.get('regulated'))
        self.assertIsNone(data.get('approved'))
        self.assertIsNone(data.get('rejected'))
        self.assertIsNone(data.get('created_by'))
        self.assertIsNone(data.get('updated_by'))
