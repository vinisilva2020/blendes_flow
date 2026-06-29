from django.test import TestCase

from apps.blendes_flow.exceptions.blaves import (
    BlaveNotFoundError,
    BlaveOrganizationInactiveError,
    BlaveOrganizationNotFoundError,
)
from apps.blendes_flow.exceptions.boundaries import (
    BoundaryAlreadyExistsError,
    BoundaryHasChildrenError,
    BoundaryInvalidParentError,
    BoundaryMovementNotAllowedError,
)
from apps.blendes_flow.exceptions.schapters import (
    SchapterAlreadyExistsError,
    SchapterMovementNotAllowedError,
    SchapterRoleTypeConflictError,
)
from apps.blendes_flow.exceptions.facet_descriptions import (
    FacetDescriptionAlreadyExistsError,
    FacetDescriptionMovementNotAllowedError,
)
from apps.blendes_flow.exceptions.kref_pratices import (
    KrefPraticeMovementNotAllowedError,
)
from apps.blendes_flow.exceptions.mixpoints import (
    MixpointMovementNotAllowedError,
)
from apps.blendes_flow.exceptions.risks import (
    RiskFacetNotAllowedError,
    RiskMovementNotAllowedError,
)
from apps.blendes_flow.models import (
    ActorType,
    Blave,
    BlaveMovements,
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
from apps.blendes_flow.services import (
    create_blave_service,
    create_boundary_service,
    create_facet_descriptions_service,
    create_kref_pratices_service,
    create_mixpoints_service,
    create_risks_service,
    create_schapter_service,
    delete_blave_service,
    delete_boundary_service,
    delete_facet_description_service,
    delete_kref_pratice_service,
    delete_mixpoint_service,
    delete_risk_service,
    delete_schapter_service,
    get_blave_service,
    get_facet_description_service,
    get_kref_pratice_service,
    get_mixpoint_service,
    get_risk_service,
    list_blaves_service,
    list_boundaries_service,
    list_facet_descriptions_service,
    list_global_boundary_names_service,
    list_global_schapter_names_service,
    list_kref_pratices_service,
    list_mixpoints_service,
    list_risks_service,
    list_schapters_service,
    update_blave_service,
    update_boundary_service,
    update_facet_description_service,
    update_kref_pratice_service,
    update_mixpoint_service,
    update_risk_service,
    update_schapter_service,
)
from tests.authentication.factories import create_user
from tests.blendes_flow.factories import (
    create_blave,
    create_boundary,
    create_facet_description,
    create_concrete_action,
    create_kref_pratice,
    create_mixpoint,
    create_risk,
    create_role,
    create_schapter,
)
from tests.organizations.factories import create_organization


class CreateBlaveServiceTests(TestCase):
    def test_creates_blave_with_all_movements(self):
        user = create_user(username="create-blave-owner")
        organization = create_organization(created_by=user)

        blave = create_blave_service(
            user=user,
            organization_id=organization.id,
            title="Map billing workflow",
        )

        self.assertEqual(blave.organization, organization)
        self.assertEqual(blave.created_by_user, user)
        self.assertEqual(blave.title, "Map billing workflow")
        self.assertEqual(blave.movement_statuses.count(), len(Movement.values))
        self.assertEqual(
            blave.movement_statuses.get(movement=Movement.BOUNDGROUND).status,
            MovementStatus.ACTIVE,
        )
        self.assertEqual(
            blave.movement_statuses.exclude(
                movement=Movement.BOUNDGROUND,
            ).filter(status=MovementStatus.LOCKED).count(),
            len(Movement.values) - 1,
        )

    def test_raises_when_user_does_not_own_organization(self):
        user = create_user(username="create-blave-outsider")
        organization = create_organization()

        with self.assertRaises(BlaveOrganizationNotFoundError):
            create_blave_service(
                user=user,
                organization_id=organization.id,
                title="Hidden workflow",
            )

    def test_raises_when_organization_is_inactive(self):
        user = create_user(username="create-blave-inactive")
        organization = create_organization(created_by=user, is_active=False)

        with self.assertRaises(BlaveOrganizationInactiveError):
            create_blave_service(
                user=user,
                organization_id=organization.id,
                title="Inactive workflow",
            )


class ListBlavesServiceTests(TestCase):
    def test_lists_only_blaves_from_owned_organization(self):
        user = create_user(username="list-blaves-owner")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        other_blave = create_blave()

        result = list(list_blaves_service(user=user, organization_id=organization.id))

        self.assertEqual(result, [blave])
        self.assertNotIn(other_blave, result)


class GetBlaveServiceTests(TestCase):
    def test_returns_owned_blave(self):
        user = create_user(username="get-blave-owner")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)

        result = get_blave_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
        )

        self.assertEqual(result, blave)

    def test_raises_when_organization_belongs_to_other_user(self):
        user = create_user(username="get-blave-outsider")
        blave = create_blave()

        with self.assertRaises(BlaveNotFoundError):
            get_blave_service(
                user=user,
                organization_id=blave.organization_id,
                blave_id=blave.id,
            )


class UpdateBlaveServiceTests(TestCase):
    def test_updates_only_title(self):
        user = create_user(username="update-blave-owner")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            title="Before",
        )

        result = update_blave_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            title="After",
        )

        blave.refresh_from_db()
        self.assertEqual(result, blave)
        self.assertEqual(blave.title, "After")

    def test_other_user_cannot_update(self):
        user = create_user(username="update-blave-outsider")
        blave = create_blave()

        with self.assertRaises(BlaveNotFoundError):
            update_blave_service(
                user=user,
                organization_id=blave.organization_id,
                blave_id=blave.id,
                title="Forbidden",
            )


class DeleteBlaveServiceTests(TestCase):
    def test_owner_can_delete_blave(self):
        user = create_user(username="delete-blave-owner")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        blave_id = blave.id

        delete_blave_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
        )

        self.assertFalse(Blave.objects.filter(id=blave_id).exists())
        self.assertFalse(BlaveMovements.objects.filter(blave_id=blave_id).exists())


class BoundaryServiceTests(TestCase):
    def test_creates_boundary_with_existing_outer_boundary(self):
        user = create_user(username="boundary-existing-outer")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        outer = create_boundary(blave=blave, name="Company")

        boundary = create_boundary_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            outer_boundary_id=outer.id,
            name="Billing",
            description="Billing context",
        )

        self.assertEqual(boundary.blave, blave)
        self.assertEqual(boundary.outer_boundary, outer)
        self.assertEqual(boundary.name, "Billing")
        self.assertEqual(boundary.description, "Billing context")

    def test_creates_outer_boundary_by_name_in_same_request(self):
        user = create_user(username="boundary-create-outer-name")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)

        boundary = create_boundary_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            outer_boundary_name="Company",
            name="Billing",
        )

        outer = Boundary.objects.get(blave=blave, name="Company")
        self.assertEqual(boundary.outer_boundary, outer)
        self.assertEqual(Boundary.objects.filter(blave=blave).count(), 2)

    def test_blocks_management_outside_boundground(self):
        user = create_user(username="boundary-wrong-movement")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )

        with self.assertRaises(BoundaryMovementNotAllowedError):
            create_boundary_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                name="Billing",
            )

    def test_blocks_duplicate_name_in_blave(self):
        user = create_user(username="boundary-duplicate")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        create_boundary(blave=blave, name="Billing")

        with self.assertRaises(BoundaryAlreadyExistsError):
            create_boundary_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                name="Billing",
            )

    def test_blocks_cycle_when_updating_parent(self):
        user = create_user(username="boundary-cycle")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        parent = create_boundary(blave=blave, name="Parent")
        child = create_boundary(blave=blave, outer_boundary=parent, name="Child")

        with self.assertRaises(BoundaryInvalidParentError):
            update_boundary_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=parent.id,
                outer_boundary_id=child.id,
            )

    def test_blocks_delete_when_boundary_has_children(self):
        user = create_user(username="boundary-delete-with-child")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        parent = create_boundary(blave=blave, name="Parent")
        create_boundary(blave=blave, outer_boundary=parent, name="Child")

        with self.assertRaises(BoundaryHasChildrenError):
            delete_boundary_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=parent.id,
            )

    def test_lists_boundaries_inside_owned_blave(self):
        user = create_user(username="boundary-list-owner")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        create_boundary()

        result = list(
            list_boundaries_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
            )
        )

        self.assertEqual(result, [boundary])

    def test_lists_global_boundary_names_distinct(self):
        blave = create_blave()
        create_boundary(blave=blave, name="Billing")
        create_boundary(blave=create_blave(), name="Billing")
        create_boundary(name="Support")

        result = list(list_global_boundary_names_service())

        self.assertEqual(result, [{"name": "Billing"}, {"name": "Support"}])


class SchapterServiceTests(TestCase):
    def test_creates_schapter_with_nested_roles(self):
        user = create_user(username="schapter-create")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)

        schapter = create_schapter_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            name="Process invoice",
            roles=[
                {"name": "Analyst", "type": ActorType.ROLE},
                {"name": "Finance", "type": ActorType.GROUP},
            ],
        )

        self.assertEqual(schapter.boundary, boundary)
        self.assertEqual(schapter.name, "Process invoice")
        self.assertEqual(
            list(schapter.roles.order_by("name").values_list("name", flat=True)),
            ["Analyst", "Finance"],
        )

    def test_reuses_existing_role_by_name(self):
        user = create_user(username="schapter-existing-role")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        role = create_role(organization=organization, name="Analyst")

        schapter = create_schapter_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            name="Process invoice",
            roles=[{"name": "Analyst", "type": ActorType.ROLE}],
        )

        self.assertEqual(Role.objects.filter(organization=organization).count(), 1)
        self.assertEqual(list(schapter.roles.all()), [role])

    def test_blocks_role_type_conflict(self):
        user = create_user(username="schapter-role-conflict")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        create_role(
            organization=organization,
            name="Analyst",
            type=ActorType.ROLE,
        )

        with self.assertRaises(SchapterRoleTypeConflictError):
            create_schapter_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                name="Process invoice",
                roles=[{"name": "Analyst", "type": ActorType.GROUP}],
            )

    def test_blocks_management_outside_labor(self):
        user = create_user(username="schapter-wrong-movement")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)

        with self.assertRaises(SchapterMovementNotAllowedError):
            create_schapter_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                name="Process invoice",
                roles=[],
            )

    def test_blocks_duplicate_name_in_boundary(self):
        user = create_user(username="schapter-duplicate")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        create_schapter(boundary=boundary, name="Process invoice")

        with self.assertRaises(SchapterAlreadyExistsError):
            create_schapter_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                name="Process invoice",
                roles=[],
            )

    def test_lists_schapters_inside_owned_boundary(self):
        user = create_user(username="schapter-list-owner")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        create_schapter()

        result = list(
            list_schapters_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
            )
        )

        self.assertEqual(result, [schapter])

    def test_updates_schapter_roles(self):
        user = create_user(username="schapter-update")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        old_role = create_role(organization=organization, name="Old")
        schapter = create_schapter(boundary=boundary, roles=[old_role])

        result = update_schapter_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            name="Updated",
            roles=[{"name": "New", "type": ActorType.GROUP}],
        )

        self.assertEqual(result.name, "Updated")
        self.assertEqual(
            list(result.roles.values_list("name", "type")),
            [("New", ActorType.GROUP)],
        )

    def test_deletes_schapter(self):
        user = create_user(username="schapter-delete")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)

        delete_schapter_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
        )

        self.assertFalse(Schapter.objects.filter(id=schapter.id).exists())

    def test_lists_global_schapter_names_distinct(self):
        boundary = create_boundary()
        create_schapter(boundary=boundary, name="Invoice")
        create_schapter(boundary=create_boundary(), name="Invoice")
        create_schapter(name="Refund")

        result = list(list_global_schapter_names_service())

        self.assertEqual(result, [{"name": "Invoice"}, {"name": "Refund"}])


def build_all_facet_payload():
    """Monta payload completo de facetas para os testes."""
    return [
        {
            "facet": facet,
            "generate_risk": True,
            "value": f"{facet} description",
            "observation": "",
        }
        for facet in FacetType.values
    ]


class FacetDescriptionServiceTests(TestCase):
    def test_creates_all_facets_for_schapter(self):
        user = create_user(username="facet-create")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)

        result = list(
            create_facet_descriptions_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facets=build_all_facet_payload(),
            )
        )

        self.assertEqual(len(result), len(FacetType.values))
        what = FacetDescription.objects.get(schapter=schapter, facet=FacetType.WHAT)
        self.assertFalse(what.generate_risk)

    def test_blocks_management_outside_echo(self):
        user = create_user(username="facet-wrong-movement")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.LABOR,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)

        with self.assertRaises(FacetDescriptionMovementNotAllowedError):
            create_facet_descriptions_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facets=build_all_facet_payload(),
            )

    def test_blocks_duplicate_facets_in_schapter(self):
        user = create_user(username="facet-duplicate")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        create_facet_description(schapter=schapter, facet=FacetType.WHAT)

        with self.assertRaises(FacetDescriptionAlreadyExistsError):
            create_facet_descriptions_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facets=build_all_facet_payload(),
            )

    def test_lists_facets_inside_owned_schapter(self):
        user = create_user(username="facet-list-owner")
        organization = create_organization(created_by=user)
        blave = create_blave(organization=organization, created_by_user=user)
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(schapter=schapter)
        create_facet_description()

        result = list(
            list_facet_descriptions_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
            )
        )

        self.assertEqual(result, [facet_description])

    def test_updates_facet_description_and_keeps_what_without_risk(self):
        user = create_user(username="facet-update")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(schapter=schapter)

        result = update_facet_description_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            generate_risk=True,
            value="Updated value",
        )

        self.assertEqual(result.value, "Updated value")
        self.assertFalse(result.generate_risk)

    def test_get_and_delete_facet_description(self):
        user = create_user(username="facet-delete")
        organization = create_organization(created_by=user)
        blave = create_blave(
            organization=organization,
            created_by_user=user,
            current_movement=Movement.ECHO,
        )
        boundary = create_boundary(blave=blave)
        schapter = create_schapter(boundary=boundary)
        facet_description = create_facet_description(schapter=schapter)

        result = get_facet_description_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
        )
        self.assertEqual(result, facet_description)

        delete_facet_description_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
        )
        self.assertFalse(
            FacetDescription.objects.filter(id=facet_description.id).exists()
        )


def build_risk_payload():
    """Monta payload de riscos para os testes."""
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


class RiskServiceTests(TestCase):
    def test_creates_risks_for_facet_description(self):
        user = create_user(username="risk-create")
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

        result = list(
            create_risks_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
                risks=build_risk_payload(),
            )
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(
            Risk.objects.filter(facet_description=facet_description).count(),
            2,
        )

    def test_blocks_management_outside_echo(self):
        user = create_user(username="risk-wrong-movement")
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

        with self.assertRaises(RiskMovementNotAllowedError):
            create_risks_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
                risks=build_risk_payload(),
            )

    def test_blocks_what_facet(self):
        user = create_user(username="risk-what")
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

        with self.assertRaises(RiskFacetNotAllowedError):
            create_risks_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
                risks=build_risk_payload(),
            )

    def test_lists_risks_inside_owned_facet_description(self):
        user = create_user(username="risk-list-owner")
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

        result = list(
            list_risks_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
            )
        )

        self.assertEqual(result, [risk])

    def test_updates_gets_and_deletes_risk(self):
        user = create_user(username="risk-update")
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

        result = update_risk_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            risk_id=risk.id,
            formated_text="Updated risk",
        )
        self.assertEqual(result.formated_text, "Updated risk")

        result = get_risk_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            risk_id=risk.id,
        )
        self.assertEqual(result.id, risk.id)

        delete_risk_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            risk_id=risk.id,
        )
        self.assertFalse(Risk.objects.filter(id=risk.id).exists())


def build_kref_pratice_payload():
    """Monta payload de praticas KREF para os testes."""
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


class KrefPraticeServiceTests(TestCase):
    def test_creates_kref_pratices_for_risk(self):
        user = create_user(username="kref-create")
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

        result = list(
            create_kref_pratices_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
                risk_id=risk.id,
                kref_pratices=build_kref_pratice_payload(),
            )
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(KrefPratice.objects.filter(risk=risk).count(), 2)

    def test_blocks_management_outside_echo(self):
        user = create_user(username="kref-wrong-movement")
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

        with self.assertRaises(KrefPraticeMovementNotAllowedError):
            create_kref_pratices_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
                risk_id=risk.id,
                kref_pratices=build_kref_pratice_payload(),
            )

    def test_lists_kref_pratices_inside_owned_risk(self):
        user = create_user(username="kref-list-owner")
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

        result = list(
            list_kref_pratices_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
                risk_id=risk.id,
            )
        )

        self.assertEqual(result, [kref_pratice])

    def test_updates_gets_and_deletes_kref_pratice(self):
        user = create_user(username="kref-update")
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

        result = update_kref_pratice_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            risk_id=risk.id,
            kref_pratice_id=kref_pratice.id,
            pratice="Updated practice",
        )
        self.assertEqual(result.pratice, "Updated practice")

        result = get_kref_pratice_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            risk_id=risk.id,
            kref_pratice_id=kref_pratice.id,
        )
        self.assertEqual(result.id, kref_pratice.id)

        delete_kref_pratice_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            risk_id=risk.id,
            kref_pratice_id=kref_pratice.id,
        )
        self.assertFalse(KrefPratice.objects.filter(id=kref_pratice.id).exists())


def build_mixpoint_payload():
    """Monta payload de mixpoints para os testes."""
    return [
        {"description": "Marketing confirms the handoff"},
        {"description": "Sales checks proposal quality"},
    ]


class MixpointServiceTests(TestCase):
    def test_creates_mixpoints_for_concrete_action(self):
        user = create_user(username="mixpoint-create")
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

        result = list(
            create_mixpoints_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
                risk_id=risk.id,
                kref_pratice_id=kref_pratice.id,
                concrete_action_id=concrete_action.id,
                mixpoints=build_mixpoint_payload(),
            )
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(
            Mixpoint.objects.filter(concrete_action=concrete_action).count(),
            2,
        )

    def test_blocks_management_outside_sightline(self):
        user = create_user(username="mixpoint-wrong-movement")
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

        with self.assertRaises(MixpointMovementNotAllowedError):
            create_mixpoints_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
                risk_id=risk.id,
                kref_pratice_id=kref_pratice.id,
                concrete_action_id=concrete_action.id,
                mixpoints=build_mixpoint_payload(),
            )

    def test_lists_mixpoints_inside_owned_concrete_action(self):
        user = create_user(username="mixpoint-list-owner")
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

        result = list(
            list_mixpoints_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
                boundary_id=boundary.id,
                schapter_id=schapter.id,
                facet_description_id=facet_description.id,
                risk_id=risk.id,
                kref_pratice_id=kref_pratice.id,
                concrete_action_id=concrete_action.id,
            )
        )

        self.assertEqual(result, [mixpoint])

    def test_updates_gets_and_deletes_mixpoint(self):
        user = create_user(username="mixpoint-update")
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

        result = update_mixpoint_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            risk_id=risk.id,
            kref_pratice_id=kref_pratice.id,
            concrete_action_id=concrete_action.id,
            mixpoint_id=mixpoint.id,
            description="Updated mixpoint",
        )
        self.assertEqual(result.description, "Updated mixpoint")

        result = get_mixpoint_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            risk_id=risk.id,
            kref_pratice_id=kref_pratice.id,
            concrete_action_id=concrete_action.id,
            mixpoint_id=mixpoint.id,
        )
        self.assertEqual(result.id, mixpoint.id)

        delete_mixpoint_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
            boundary_id=boundary.id,
            schapter_id=schapter.id,
            facet_description_id=facet_description.id,
            risk_id=risk.id,
            kref_pratice_id=kref_pratice.id,
            concrete_action_id=concrete_action.id,
            mixpoint_id=mixpoint.id,
        )
        self.assertFalse(Mixpoint.objects.filter(id=mixpoint.id).exists())
