"""Principal agent behavior extracted from INSIDER.

Shared tools are supplied by the existing ecc-workflow-api-server backend:
run with its directory on PYTHONPATH. This is a focused source extract,
not a separate runnable application or a new experimental implementation.
"""

"""Design-time optimization, necessary-condition diagnostics and held-out assessment.

The holdout never changes the selected plan. All performance inputs are explicit
model assumptions; this module neither deploys nor certifies a provider SLA.
"""
from copy import deepcopy
from app.api.multiagent.feasibility_bounds import check
from app.api.multiagent.planner import fingerprint
from app.api.multiagent.robust_search import optimize
from app.api.multiagent.simulation import evaluate, _number
from app.api.multiagent.statistics import ratio_interval
from app.api.multiagent.risk_evidence import run_violation_evidence, binomial_upper
from app.api.multiagent.model_contract import validate_profile
from app.api.multiagent.placement_text import recontextualize
from app.api.multiagent.validation import InputError, validate_plan


def _seeds(values, name):
    values = tuple(values)
    if not values or any(type(v) is not int for v in values) or len(set(values)) != len(values):
        raise InputError(f'{name} must contain unique integer seeds.')
    return values


def propose(space, search_profiles, validation_profiles, *, search_seeds,
            validation_seeds, rates=(1, 3), method='beam', budget=80,
            optimizer_seed=1, tolerance=.01, duration=120, warmup=20, drain=120,
            evidence_alpha=.05):
    binomial_upper(0, 1, evidence_alpha)
    search_seeds = _seeds(search_seeds, 'search_seeds')
    validation_seeds = _seeds(validation_seeds, 'validation_seeds')
    if set(search_seeds) & set(validation_seeds):
        raise InputError('Search and validation seeds must be disjoint; validation cannot select the plan.')
    rates = tuple(rates)
    if not search_profiles or not validation_profiles or not rates:
        raise InputError('Explicit non-empty search/validation profiles and arrival rates are required.')
    for rate in rates:
        _number(rate, 'arrival rate', strict=True)
    if len(set(rates)) != len(rates):
        raise InputError('Arrival rates must be unique.')
    _number(tolerance, 'tolerance')
    if tolerance > 1:
        raise InputError('Tolerance must be between zero and one.')
    binomial_upper(0, len(validation_seeds), evidence_alpha/(len(validation_profiles)*len(rates)))
    # Snapshot caller-owned assumptions and diagnose validation conditions before
    # choosing a plan. Diagnostics do not alter rates, capacities or the objective.
    search_profiles, validation_profiles = deepcopy(search_profiles), deepcopy(validation_profiles)
    contracts={split:{label:validate_profile(space, profile) for label,profile in profiles.items()}
               for split,profiles in [('search',search_profiles),('validation',validation_profiles)]}
    diagnostics = [{'profile': label, 'rate': rate, **check(space, profile, rate, tolerance)}
                   for label, profile in validation_profiles.items() for rate in rates]
    selected = optimize(space, search_profiles, method=method, budget=budget,
                        seed=optimizer_seed, rates=rates, seeds=search_seeds,
                        tolerance=tolerance, duration=duration, warmup=warmup, drain=drain)
    plan = selected['plan']
    validation = validate_plan(plan, space.workflow, space.candidates)
    if not validation['valid']:
        raise InputError('Optimizer returned a catalog-invalid plan.')
    plan,text_provenance=recontextualize(space.initial,plan,method)
    selected['plan']=plan
    cells = []
    for label, profile in validation_profiles.items():
        evaluated = evaluate(space.workflow, plan, profile, rates, validation_seeds,
                             duration=duration, warmup=warmup, drain=drain)
        for rate in rates:
            runs = [r for r in evaluated['runs'] if r['rate'] == rate]
            for run in runs:
                run.pop('latencies_seconds', None)
            miss = ratio_interval(runs)
            cells.append({'profile': label, 'rate': rate, 'miss': miss,
                          'replication_violation_evidence': run_violation_evidence(
                              runs, tolerance, alpha=evidence_alpha,
                              family_size=len(validation_profiles)*len(rates)),
                          'unfinished': ratio_interval(runs, 'unfinished_cohort'),
                          'observed_tolerance_met': miss['estimate'] <= tolerance,
                          'replications': runs})
    observed_pass = all(cell['observed_tolerance_met'] for cell in cells)
    necessary_violations = any(d['necessary_condition_violations'] for d in diagnostics)
    unknowns = list(space.unknowns)
    if selected.get('stop_reason')=='candidate_scan_limit':
        unknowns.append('Candidate scanning stopped before the configuration budget; unexplored admissible placements may remain.')
    for row in plan['result']:
        for candidate in space.candidates[str(row['abstractservice_id'])]:
            if (candidate['provider'], candidate['service_id']) == (row['provider'], row['service_id']) and candidate.get('implementation_required'):
                unknowns.append(f"Node {row['abstractservice_id']}: application/model artifacts, hardware and configuration remain to be validated.")
    unknowns.extend(a for a in plan.get('assumptions', []) if isinstance(a, str))
    return {
        'plan': plan, 'catalog_validation': validation, 'optimization': selected,
        'diagnostics': diagnostics, 'held_out_assessment': cells, 'model_contracts': contracts,
        'assessment': 'model_necessary_condition_violated' if necessary_violations else
                      'observed_tolerance_met' if observed_pass else 'observed_tolerance_exceeded',
        'observed_tolerance_met': observed_pass,
        'unknowns': list(dict.fromkeys(unknowns)), 'placement_text_provenance':text_provenance,
        'metadata': {'search_seeds': list(search_seeds), 'validation_seeds': list(validation_seeds),
                     'search_profiles_sha256': fingerprint(search_profiles),
                     'validation_profiles_sha256': fingerprint(validation_profiles),
                     'workflow_sha256': fingerprint(space.workflow), 'plan_sha256': fingerprint(plan),
                     'tolerance': tolerance, 'rates': list(rates),
                     'selection': 'Search data only; no reselection from holdout or analytical diagnostics.',
                     'scope': 'Synthetic model assessment, no deployment or real SLA certification. Necessary steady-state bounds and finite cohorts have different meanings. Bootstrap zero-event intervals do not prove zero risk; absence of a necessary violation does not prove feasibility.'}}


"""Bounded file/request interface to the complete design-time assessment path."""
from copy import deepcopy
from app.api.multiagent.planner import fingerprint
from app.api.multiagent.robust_search import PlacementSpace
from app.api.multiagent.simulation import _number
from app.api.multiagent.validation import InputError

DEFAULTS={'method':'beam','budget':80,'optimizer_seed':1,'tolerance':.01,
          'rates':[1,3],'duration':120,'warmup':20,'drain':120,'evidence_alpha':.05}
CONFIG_KEYS=set(DEFAULTS)|{'search_seeds','validation_seeds'}


def assess(request,catalog,provider='catalog'):
    required={'workflow','initial_plan','search_profiles','validation_profiles','config'}
    if not isinstance(request,dict) or not required <= request.keys() or request.keys()-required:
        raise InputError('Request requires exactly workflow, initial_plan, search_profiles, validation_profiles and config.')
    config=request['config']
    if not isinstance(config,dict) or config.keys()-CONFIG_KEYS:
        raise InputError('Unknown or invalid assessment configuration.')
    config=deepcopy({**DEFAULTS,**config})
    for name,limit in [('search_seeds',4),('validation_seeds',20),('rates',4)]:
        values=config.get(name)
        if not isinstance(values,list) or not 1<=len(values)<=limit:
            raise InputError(f'{name} must be a non-empty list with at most {limit} entries.')
    if type(config['budget']) is not int or not 1<=config['budget']<=80:
        raise InputError('Assessment request budget must be an integer from 1 to 80.')
    if config['method'] not in ('beam','de','random','local'):
        raise InputError('Unsupported assessment optimizer.')
    if type(config['optimizer_seed']) is not int:
        raise InputError('optimizer_seed must be an integer.')
    for field in ('duration','warmup','drain'):
        _number(config[field],field,strict=field=='duration')
    if config['warmup']>=config['duration']:
        raise InputError('warmup must be below the arrival duration.')
    for split in ('search_profiles','validation_profiles'):
        profiles=request[split]
        if not isinstance(profiles,dict) or not 1<=len(profiles)<=5:
            raise InputError(f'{split} requires one to five explicit profiles.')
        for label,profile in profiles.items():
            if not isinstance(label,str) or not label or not isinstance(profile,dict):
                raise InputError('Profiles require non-empty string labels and object values.')
            if not {'target_id','deadline_seconds','distribution','layers','links','tasks'}<=profile.keys():
                raise InputError('Incomplete explicit quantitative profile.')
            _number(profile['deadline_seconds'],'deadline_seconds',strict=True)
            if config['drain']<profile['deadline_seconds']:
                raise InputError('Drain must cover every profile deadline before search starts.')
    first=next(iter(request['search_profiles'].values()))
    space=PlacementSpace(request['workflow'],request['initial_plan'],catalog,first,provider=provider)
    report=propose(space,request['search_profiles'],request['validation_profiles'],**config)
    report['request_metadata']={'request_sha256':fingerprint(request),'catalog_sha256':fingerprint(catalog),
                                'initial_plan_sha256':fingerprint(request['initial_plan']),
                                'resolved_config':config,'provider_fallback':provider,
                                'scope':'Bounded design-time assessment from a supplied initial plan. No LLM request, deployment, or real SLA certification.'}
    return report


class QuantitativeAssessmentAgent:
    """Q searches a bounded space and evaluates the frozen plan on held-out seeds.

    Optimization and simulation remain shared deterministic tools. This facade
    uses the existing design-time assessment implementation, not an LLM call.
    """

    @staticmethod
    def assess(request, catalog, provider="catalog"):
        return assess(request, catalog, provider)
