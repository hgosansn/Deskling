export function requiresConfirmation(plan) {
    if (!plan || !Array.isArray(plan.proposed_tools)) {
        return false;
    }

    return plan.proposed_tools.some((tool) => {
        const risk = String(tool?.risk || '').toLowerCase();
        return risk === 'medium' || risk === 'high';
    });
}

export function buildConfirmGrant(plan, traceId) {
    const toolNames = Array.isArray(plan?.proposed_tools)
        ? plan.proposed_tools.map((tool) => tool?.name).filter(Boolean)
        : [];

    return {
        confirm_token: `confirm_${traceId}`,
        tools: toolNames,
        ttl_seconds: 60,
        decision: 'approved'
    };
}
