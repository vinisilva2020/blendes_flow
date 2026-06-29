from rest_framework import status
from rest_framework.test import APITestCase

from apps.blendes_flow.models import (
    ActorType,
    Blave,
    Boundary,
    ConcreteAction,
    FacetDescription,
    FacetType,
    KrefPratice,
    Mixpoint,
    Movement,
    MovementStatus,
    Risk,
    Role,
    Schapter,
)
from tests.authentication.factories import create_user, issue_access_token_for_user
from tests.blendes_flow.factories import (
    create_blave,
    create_boundary,
    create_concrete_action,
    create_facet_description,
    create_kref_pratice,
    create_mixpoint,
    create_risk,
    create_role,
    create_schapter,
)
from tests.organizations.factories import create_organization


def blave_list_url(organization_id):
    return f"/api/v1/organizations/{organization_id}/blaves/"


def blave_detail_url(*args):
    blave_id = args[-1]
    return f"/api/v1/blaves/{blave_id}/"


def boundary_list_url(*args):
    blave_id = args[-1]
    return f"/api/v1/blaves/{blave_id}/boundaries/"


def boundary_detail_url(*args):
    boundary_id = args[-1]
    return f"/api/v1/boundaries/{boundary_id}/"


def boundary_global_url():
    return "/api/v1/boundaries/"


def schapter_list_url(*args):
    boundary_id = args[-1]
    return f"/api/v1/boundaries/{boundary_id}/schapters/"


def schapter_detail_url(*args):
    schapter_id = args[-1]
    return f"/api/v1/schapters/{schapter_id}/"


def schapter_global_url():
    return "/api/v1/schapters/"


def facet_description_list_url(*args):
    schapter_id = args[-1]
    return f"/api/v1/schapters/{schapter_id}/facet-descriptions/"


def facet_description_detail_url(*args):
    facet_description_id = args[-1]
    return f"/api/v1/facet-descriptions/{facet_description_id}/"


def risk_list_url(*args):
    facet_description_id = args[-1]
    return f"/api/v1/facet-descriptions/{facet_description_id}/risks/"


def risk_detail_url(*args):
    risk_id = args[-1]
    return f"/api/v1/risks/{risk_id}/"


def kref_pratice_list_url(*args):
    risk_id = args[-1]
    return f"/api/v1/risks/{risk_id}/kref-pratices/"


def kref_pratice_detail_url(*args):
    kref_pratice_id = args[-1]
    return f"/api/v1/kref-pratices/{kref_pratice_id}/"


def mixpoint_list_url(*args):
    concrete_action_id = args[-1]
    return f"/api/v1/concrete-actions/{concrete_action_id}/mixpoints/"


def mixpoint_detail_url(*args):
    mixpoint_id = args[-1]
    return f"/api/v1/mixpoints/{mixpoint_id}/"


def build_all_facet_payload():
    return [
        {
            "facet": facet,
            "generate_risk": True,
            "value": f"{facet} description",
            "observation": "",
        }
        for facet in FacetType.values
    ]


def build_risk_payload():
    return [
        {
            "formated_text": "Risk when invoice data is incomplete",
            "strategic_impact": "Revenue forecast becomes unreliable",
            "operational_impact": "Billing team reworks invoices",
            "tactical_impact": "Invoice approval is delayed",
        },
        {
            "formated_text": "Risk when approval ownership is unclear",
            "strategic_impact": "Customer experience deteriorates",
            "operational_impact": "Tickets are reopened",
            "tactical_impact": "Analysts wait for escalation",
        },
    ]


def build_kref_pratice_payload():
    return [
        {
            "pratice": "Review approval policy",
            "references": "ISO 31000",
        },
        {
            "pratice": "Add invoice quality gate",
            "references": "Internal billing playbook",
        },
    ]


def build_mixpoint_payload():
    return [
        {"description": "Marketing confirms the handoff"},
        {"description": "Sales checks proposal quality"},
    ]


class BlavesAPITests(APITestCase):
    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_requires_authentication(self):
        response = self.client.get(blave_list_url(organization_id=1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_create_blave_sets_user_and_movements(self):
        user = create_user(username="api-blave-create")
        organization = create_organization(created_by=user)
        self.authenticate(user)

        response = self.client.post(
            blave_list_url(organization.id),
            {"title": "Understand onboarding"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blave = Blave.objects.get(id=response.data["id"])
        self.assertEqual(blave.created_by_user, user)
        self.assertEqual(blave.organization, organization)
        self.assertEqual(len(response.data["movements"]), len(Movement.values))
        self.assertEqual(
            blave.movement_statuses.get(movement=Movement.BOUNDGROUND).status,
            MovementStatus.ACTIVE,
        )

    def test_create_blave_returns_not_found_for_other_user_organization(self):
        user = create_user(username="api-blave-create-outsider")
        organization = create_organization()
        self.authenticate(user)

        response = self.client.post(
            blave_list_url(organization.id),
            {"title": "Forbidden"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["error"]["code"],
            "blave_organization_not_found",
        )

    def test_list_returns_blaves_from_owned_organization(self):
        user = create_user(username="api-blave-list")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        create_blave()
        self.authenticate(user)

        response = self.client.get(blave_list_url(organization.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], blave.id)

    def test_retrieve_blave_for_owner(self):
        user = create_user(username="api-blave-detail")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        self.authenticate(user)

        response = self.client.get(blave_detail_url(organization.id, blave.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], blave.id)

    def test_patch_updates_only_title(self):
        user = create_user(username="api-blave-patch")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            title="Before",
        )
        self.authenticate(user)

        response = self.client.patch(
            blave_detail_url(organization.id, blave.id),
            {"title": "After", "status": "COMPLETED"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blave.refresh_from_db()
        self.assertEqual(blave.title, "After")
        self.assertNotEqual(blave.status, "COMPLETED")

    def test_other_user_cannot_patch_blave(self):
        user = create_user(username="api-blave-patch-outsider")
        blave = create_blave()
        self.authenticate(user)

        response = self.client.patch(
            blave_detail_url(blave.organization_id, blave.id),
            {"title": "Forbidden"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete_blave(self):
        user = create_user(username="api-blave-delete")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        self.authenticate(user)

        response = self.client.delete(blave_detail_url(organization.id, blave.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Blave.objects.filter(id=blave.id).exists())


class BoundariesAPITests(APITestCase):
    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_requires_authentication(self):
        response = self.client.get(boundary_list_url(1, 1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_create_boundary_with_outer_name_creates_parent(self):
        user = create_user(username="api-boundary-create")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        self.authenticate(user)

        response = self.client.post(
            boundary_list_url(organization.id, blave.id),
            {
                "outer_boundary_name": "Company",
                "name": "Billing",
                "description": "Billing context",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        boundary = Boundary.objects.get(id=response.data["id"])
        outer = Boundary.objects.get(blave=blave, name="Company")
        self.assertEqual(boundary.outer_boundary, outer)
        self.assertEqual(boundary.name, "Billing")

    def test_create_boundary_blocks_outside_boundground(self):
        user = create_user(username="api-boundary-movement")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        self.authenticate(user)

        response = self.client.post(
            boundary_list_url(organization.id, blave.id),
            {"name": "Billing"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["error"]["code"],
            "boundary_movement_not_allowed",
        )

    def test_list_returns_boundaries_from_owned_blave(self):
        user = create_user(username="api-boundary-list")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        create_boundary()
        self.authenticate(user)

        response = self.client.get(boundary_list_url(organization.id, blave.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], boundary.id)

    def test_patch_blocks_cycle(self):
        user = create_user(username="api-boundary-cycle")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        parent = create_boundary(blave=blave, name="Parent")
        child = create_boundary(blave=blave, outer_boundary=parent, name="Child")
        self.authenticate(user)

        response = self.client.patch(
            boundary_detail_url(organization.id, blave.id, parent.id),
            {"outer_boundary_id": child.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["code"], "boundary_invalid_parent")

    def test_delete_blocks_boundary_with_children(self):
        user = create_user(username="api-boundary-delete-child")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        parent = create_boundary(blave=blave, name="Parent")
        create_boundary(blave=blave, outer_boundary=parent, name="Child")
        self.authenticate(user)

        response = self.client.delete(
            boundary_detail_url(organization.id, blave.id, parent.id),
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"]["code"], "boundary_has_children")

    def test_owner_can_delete_leaf_boundary(self):
        user = create_user(username="api-boundary-delete")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        self.authenticate(user)

        response = self.client.delete(
            boundary_detail_url(organization.id, blave.id, boundary.id),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Boundary.objects.filter(id=boundary.id).exists())

    def test_global_names_are_paginated_and_name_only(self):
        user = create_user(username="api-boundary-global")
        for index in range(12):
            create_boundary(name=f"Boundary {index:02d}")
        self.authenticate(user)

        response = self.client.get(boundary_global_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(list(response.data["results"][0].keys()), ["name"])


class SchaptersAPITests(APITestCase):
    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_requires_authentication(self):
        response = self.client.get(schapter_list_url(1, 1, 1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_create_schapter_with_nested_roles(self):
        user = create_user(username="api-schapter-create")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        self.authenticate(user)

        response = self.client.post(
            schapter_list_url(organization.id, blave.id, boundary.id),
            {
                "name": "Process invoice",
                "roles": [
                    {"name": "Analyst", "type": ActorType.ROLE},
                    {"name": "Finance", "type": ActorType.GROUP},
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        schapter = Schapter.objects.get(id=response.data["id"])
        self.assertEqual(schapter.boundary, boundary)
        self.assertEqual(len(response.data["roles"]), 2)
        self.assertEqual(Role.objects.filter(organization=organization).count(), 2)

    def test_create_schapter_blocks_outside_labor(self):
        user = create_user(username="api-schapter-movement")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        self.authenticate(user)

        response = self.client.post(
            schapter_list_url(organization.id, blave.id, boundary.id),
            {"name": "Process invoice", "roles": []},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["error"]["code"],
            "schapter_movement_not_allowed",
        )

    def test_list_returns_schapters_with_roles_from_owned_boundary(self):
        user = create_user(username="api-schapter-list")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        role = create_role(organization=organization, name="Analyst")
        schapter = create_schapter(boundary=boundary, roles=[role])
        create_schapter()
        self.authenticate(user)

        response = self.client.get(
            schapter_list_url(organization.id, blave.id, boundary.id),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], schapter.id)
        self.assertEqual(response.data[0]["roles"][0]["name"], "Analyst")

    def test_patch_replaces_roles(self):
        user = create_user(username="api-schapter-patch")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        role = create_role(organization=organization, name="Old")
        schapter = create_schapter(boundary=boundary, roles=[role])
        self.authenticate(user)

        response = self.client.patch(
            schapter_detail_url(organization.id, blave.id, boundary.id, schapter.id),
            {
                "name": "Updated",
                "roles": [{"name": "New", "type": ActorType.GROUP}],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated")
        self.assertEqual(response.data["roles"][0]["name"], "New")

    def test_delete_schapter(self):
        user = create_user(username="api-schapter-delete")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        self.authenticate(user)

        response = self.client.delete(
            schapter_detail_url(organization.id, blave.id, boundary.id, schapter.id),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Schapter.objects.filter(id=schapter.id).exists())

    def test_global_names_are_paginated_and_name_only(self):
        user = create_user(username="api-schapter-global")
        for index in range(12):
            create_schapter(name=f"Schapter {index:02d}")
        self.authenticate(user)

        response = self.client.get(schapter_global_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(list(response.data["results"][0].keys()), ["name"])


class FacetDescriptionsAPITests(APITestCase):
    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_requires_authentication(self):
        response = self.client.get(facet_description_list_url(1, 1, 1, 1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_create_all_facets_for_schapter(self):
        user = create_user(username="api-facet-create")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        self.authenticate(user)

        response = self.client.post(
            facet_description_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
            ),
            {"facets": build_all_facet_payload()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), len(FacetType.values))
        what = FacetDescription.objects.get(schapter=schapter, facet=FacetType.WHAT)
        self.assertFalse(what.generate_risk)

    def test_create_blocks_outside_echo(self):
        user = create_user(username="api-facet-movement")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        self.authenticate(user)

        response = self.client.post(
            facet_description_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
            ),
            {"facets": build_all_facet_payload()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["error"]["code"],
            "facet_description_movement_not_allowed",
        )

    def test_create_requires_all_facets_once(self):
        user = create_user(username="api-facet-validation")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        self.authenticate(user)

        response = self.client.post(
            facet_description_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
            ),
            {"facets": build_all_facet_payload()[:-1]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["code"], "validation_error")

    def test_list_returns_facets_from_owned_schapter(self):
        user = create_user(username="api-facet-list")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(schapter=schapter)
        create_facet_description()
        self.authenticate(user)

        response = self.client.get(
            facet_description_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], facet_description.id)

    def test_patch_updates_facet_description(self):
        user = create_user(username="api-facet-patch")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(schapter=schapter)
        self.authenticate(user)

        response = self.client.patch(
            facet_description_detail_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
            ),
            {"value": "Updated value", "generate_risk": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], "Updated value")
        self.assertFalse(response.data["generate_risk"])

    def test_delete_facet_description(self):
        user = create_user(username="api-facet-delete")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(schapter=schapter)
        self.authenticate(user)

        response = self.client.delete(
            facet_description_detail_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            FacetDescription.objects.filter(id=facet_description.id).exists()
        )


class RisksAPITests(APITestCase):
    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_requires_authentication(self):
        response = self.client.get(risk_list_url(1, 1, 1, 1, 1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_create_risks_for_facet_description(self):
        user = create_user(username="api-risk-create")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        self.authenticate(user)

        response = self.client.post(
            risk_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
            ),
            {"risks": build_risk_payload()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            Risk.objects.filter(facet_description=facet_description).count(),
            2,
        )

    def test_create_blocks_outside_echo(self):
        user = create_user(username="api-risk-movement")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        self.authenticate(user)

        response = self.client.post(
            risk_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
            ),
            {"risks": build_risk_payload()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"]["code"], "risk_movement_not_allowed")

    def test_create_blocks_what_facet(self):
        user = create_user(username="api-risk-what")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHAT,
            generate_risk=False,
        )
        self.authenticate(user)

        response = self.client.post(
            risk_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
            ),
            {"risks": build_risk_payload()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"]["code"], "risk_facet_not_allowed")

    def test_list_returns_risks_from_owned_facet_description(self):
        user = create_user(username="api-risk-list")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        create_risk()
        self.authenticate(user)

        response = self.client.get(
            risk_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], risk.id)

    def test_patch_updates_risk(self):
        user = create_user(username="api-risk-patch")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        self.authenticate(user)

        response = self.client.patch(
            risk_detail_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
            ),
            {"formated_text": "Updated risk"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["formated_text"], "Updated risk")

    def test_delete_risk(self):
        user = create_user(username="api-risk-delete")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        self.authenticate(user)

        response = self.client.delete(
            risk_detail_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Risk.objects.filter(id=risk.id).exists())


class KrefPraticesAPITests(APITestCase):
    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_requires_authentication(self):
        response = self.client.get(kref_pratice_list_url(1, 1, 1, 1, 1, 1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_create_kref_pratices_for_risk(self):
        user = create_user(username="api-kref-create")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        self.authenticate(user)

        response = self.client.post(
            kref_pratice_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
            ),
            {"kref_pratices": build_kref_pratice_payload()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(KrefPratice.objects.filter(risk=risk).count(), 2)

    def test_create_blocks_outside_echo(self):
        user = create_user(username="api-kref-movement")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        self.authenticate(user)

        response = self.client.post(
            kref_pratice_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
            ),
            {"kref_pratices": build_kref_pratice_payload()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["error"]["code"],
            "kref_pratice_movement_not_allowed",
        )

    def test_list_returns_kref_pratices_from_owned_risk(self):
        user = create_user(username="api-kref-list")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        kref_pratice = create_kref_pratice(risk=risk)
        create_kref_pratice()
        self.authenticate(user)

        response = self.client.get(
            kref_pratice_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], kref_pratice.id)

    def test_patch_updates_kref_pratice(self):
        user = create_user(username="api-kref-patch")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        kref_pratice = create_kref_pratice(risk=risk)
        self.authenticate(user)

        response = self.client.patch(
            kref_pratice_detail_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
                kref_pratice.id,
            ),
            {"pratice": "Updated practice"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pratice"], "Updated practice")

    def test_delete_kref_pratice(self):
        user = create_user(username="api-kref-delete")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        kref_pratice = create_kref_pratice(risk=risk)
        self.authenticate(user)

        response = self.client.delete(
            kref_pratice_detail_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
                kref_pratice.id,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(KrefPratice.objects.filter(id=kref_pratice.id).exists())


class MixpointsAPITests(APITestCase):
    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_requires_authentication(self):
        response = self.client.get(mixpoint_list_url(1, 1, 1, 1, 1, 1, 1, 1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_create_mixpoints_for_concrete_action(self):
        user = create_user(username="api-mixpoint-create")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.SIGHTLINE,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        kref_pratice = create_kref_pratice(risk=risk)
        concrete_action = create_concrete_action(kref_pratice=kref_pratice)
        self.authenticate(user)

        response = self.client.post(
            mixpoint_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
                kref_pratice.id,
                concrete_action.id,
            ),
            {"mixpoints": build_mixpoint_payload()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            Mixpoint.objects.filter(concrete_action=concrete_action).count(),
            2,
        )

    def test_create_blocks_outside_sightline(self):
        user = create_user(username="api-mixpoint-movement")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        kref_pratice = create_kref_pratice(risk=risk)
        concrete_action = create_concrete_action(kref_pratice=kref_pratice)
        self.authenticate(user)

        response = self.client.post(
            mixpoint_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
                kref_pratice.id,
                concrete_action.id,
            ),
            {"mixpoints": build_mixpoint_payload()},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["error"]["code"],
            "mixpoint_movement_not_allowed",
        )

    def test_list_returns_mixpoints_from_owned_concrete_action(self):
        user = create_user(username="api-mixpoint-list")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        kref_pratice = create_kref_pratice(risk=risk)
        concrete_action = create_concrete_action(kref_pratice=kref_pratice)
        mixpoint = create_mixpoint(concrete_action=concrete_action)
        create_mixpoint()
        self.authenticate(user)

        response = self.client.get(
            mixpoint_list_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
                kref_pratice.id,
                concrete_action.id,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], mixpoint.id)

    def test_patch_updates_mixpoint(self):
        user = create_user(username="api-mixpoint-patch")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.SIGHTLINE,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        kref_pratice = create_kref_pratice(risk=risk)
        concrete_action = create_concrete_action(kref_pratice=kref_pratice)
        mixpoint = create_mixpoint(concrete_action=concrete_action)
        self.authenticate(user)

        response = self.client.patch(
            mixpoint_detail_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
                kref_pratice.id,
                concrete_action.id,
                mixpoint.id,
            ),
            {"description": "Updated mixpoint"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Updated mixpoint")

    def test_delete_mixpoint(self):
        user = create_user(username="api-mixpoint-delete")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.SIGHTLINE,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(
            schapter=schapter,
            facet=FacetType.WHY,
            generate_risk=True,
        )
        risk = create_risk(facet_description=facet_description)
        kref_pratice = create_kref_pratice(risk=risk)
        concrete_action = create_concrete_action(kref_pratice=kref_pratice)
        mixpoint = create_mixpoint(concrete_action=concrete_action)
        self.authenticate(user)

        response = self.client.delete(
            mixpoint_detail_url(
                organization.id,
                blave.id,
                boundary.id,
                schapter.id,
                facet_description.id,
                risk.id,
                kref_pratice.id,
                concrete_action.id,
                mixpoint.id,
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Mixpoint.objects.filter(id=mixpoint.id).exists())
