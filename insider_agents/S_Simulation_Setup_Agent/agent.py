"""Principal agent behavior extracted from INSIDER.

Shared tools are supplied by the existing ecc-workflow-api-server backend:
run with its directory on PYTHONPATH. This is a focused source extract,
not a separate runnable application or a new experimental implementation.
"""

"""Deterministic simulation setup agent with parameter-level evidence accounting.

It schedules controlled scenarios; it does not invent measurements or certify
real deployment. An adapted measurement is evidence about another system.
"""
from copy import deepcopy
import math
from app.api.multiagent.simulation import compile_slice
from app.api.multiagent.validation import InputError


class SimulationSetupAgent:
    """Tools are deterministic: acquire reviewed sources, then audit scenarios.

    Literature discovery and application-semantic approval are not automated.
    The facade deliberately exposes the same evidence checks to a future LLM
    coordinator without allowing that coordinator to silently fill numeric gaps.
    """
    @staticmethod
    def acquire_sources(destination):
        from app.api.multiagent.evidence_acquisition import acquire
        return acquire(destination)

    @staticmethod
    def prepare(*args, **kwargs):
        return prepare_scenarios(*args, **kwargs)

    @staticmethod
    def audit_benchmark_code(source):
        """Static, bounded-scope source-integrity tool; never execute fetched code."""
        from app.api.multiagent.observed_configurations import audit_latency_code
        return audit_latency_code(source)

    @staticmethod
    def select_recorded_configuration(configurations, requirement):
        """Do not extrapolate quarantined points or unsupported metric semantics."""
        from app.api.multiagent.observed_configurations import select_observed
        return select_observed(configurations, requirement)

    @staticmethod
    def assess_local_reference_evidence(card):
        """Admit a matched local component trace; never certify a full workflow.

        The acquisition/training/execution commands have separate frozen
        protocols. Calling this tool cannot approve application semantics or
        extrapolate the measured CPU into a cloud VM.
        """
        from app.api.multiagent.evidence_binding import assess_binding
        return assess_binding(card)


def numeric_parameters(value, prefix=''):
    """Enumerate every numeric input, including zero defaults made explicit."""
    if isinstance(value, dict):
        for key, child in value.items():
            path = f'{prefix}/{key}'
            yield from numeric_parameters(child, path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from numeric_parameters(child, f'{prefix}/{index}')
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        yield prefix, value


def prepare_scenarios(workflow, plan, profile, evidence, sources, updates, *, rates, seeds):
    """Return profiles and a gate for external validity, without any API call.

    Evidence is keyed by JSON-pointer-like parameter paths. Numeric coverage is
    deliberately conservative: all declared profile parameters are inventoried,
    even if outside the selected target slice. Semantic blockers are separate.
    """
    if not rates or any(type(r) not in (int, float) or not math.isfinite(r) or r <= 0 for r in rates):
        raise InputError('Explicit positive arrival rates required.')
    if not seeds or any(type(s) is not int for s in seeds) or len(set(seeds)) != len(seeds):
        raise InputError('Unique integer replication seeds required.')
    if len(set(rates)) != len(rates):
        raise InputError('Duplicate arrival rates.')
    numeric = dict(numeric_parameters(profile))
    if set(evidence) != set(numeric):
        raise InputError('Every numeric profile parameter needs exactly one evidence entry.')
    allowed = {'measured', 'derived', 'adapted', 'assumed'}
    for path, row in evidence.items():
        if row.get('status') not in allowed or row.get('value') != numeric[path]:
            raise InputError(f'Invalid evidence value/status: {path}')
        if row['status'] != 'assumed':
            source = sources.get(row.get('source_id'), {})
            if not source.get('url') or not row.get('locator') or not row.get('transformation'):
                raise InputError(f'Missing source/locator/transformation: {path}')
    scenarios = {'synthetic_control': deepcopy(profile)}
    manifests = {'synthetic_control': deepcopy(evidence)}
    for label, changes in updates.items():
        if label in scenarios or not changes:
            raise InputError('Scenario labels must be unique and changes explicit.')
        current, rows = deepcopy(profile), deepcopy(evidence)
        for path, row in changes.items():
            if path not in numeric or row.get('status') not in ('measured', 'derived', 'adapted'):
                raise InputError(f'Unsupported sourced override: {path}')
            source = sources.get(row.get('source_id'), {})
            value = row.get('value')
            if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                raise InputError('Sourced overrides must be nonnegative finite numbers.')
            if not source.get('url') or not row.get('locator') or not row.get('transformation'):
                raise InputError('Sourced overrides require an auditable transformation.')
            container = current
            parts = path.strip('/').split('/')
            for part in parts[:-1]:
                container = container[part]
            container[parts[-1]] = value
            rows[path] = deepcopy(row)
        current['calibration'] = 'partially_evidence_informed_not_application_calibrated'
        scenarios[label], manifests[label] = current, rows
    included = compile_slice(workflow, plan, profile)[4]
    unresolved = [path for path, row in evidence.items() if row['status'] in ('assumed', 'adapted')]
    # A parameter table cannot establish semantic equivalence or prediction error.
    blockers = ['Application model/version, hardware, batch/request unit and concurrency need matching evidence.',
                'Source synchronization, target endpoint and omitted background contention require application review.',
                'Independent observed end-to-end logs are required to estimate prediction error.',
                'Arrival scenarios and deadline must be justified by workload evidence and application requirements.']
    return {'agent': 'SimulationSetupAgent', 'implementation': 'deterministic evidence and scenario orchestrator',
            'profiles': scenarios, 'parameter_evidence': manifests,
            'rates': list(rates), 'seeds': list(seeds), 'included_nodes': sorted(included),
            'real_execution_prediction_ready': False, 'unresolved_base_parameters': unresolved,
            'external_validity_blockers': blockers,
            'scenario_semantics': 'Measured local-network quantile envelopes are adapted to a hypothetical layer link. Marginal quantiles are not joint trace replay or probability bounds.'}
