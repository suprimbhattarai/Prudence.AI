import { httpClient } from "../../../services/api/httpClient";

import type { Organization } from "../types/organization.types";

export async function getAvailableOrganizations(): Promise<Organization[]> {
    return httpClient<Organization[]>(
        "/api/v1/organizations/available"
    );
}