"""Three bounded inference challenges; answers come from independent exact sums.

Each selected adapter must solve the supplied factor tables itself. These tasks
do not import another candidate's answers or establish a whole capability row.
"""
from copy import deepcopy
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
FLY_RECEIPT = WORKSPACE / 'cadence-flagship/experiments/fly-transition-probe/receipt.json'


def factor(scope, rule):
    scope = tuple(scope)
    return {'scope': scope, 'values': {a: F(rule(a)) for a in product((0, 1), repeat=len(scope))}}


def enumerate_joint(factors):
    """Raw-factor oracle, independent of any candidate/message implementation."""
    variables = tuple(sorted(set().union(*(set(f['scope']) for f in factors))))
    indices = [tuple(variables.index(v) for v in f['scope']) for f in factors]
    joint = {}
    for assignment in product((0, 1), repeat=len(variables)):
        weight = F(1)
        for f, positions in zip(factors, indices):
            weight *= f['values'][tuple(assignment[p] for p in positions)]
        joint[assignment] = weight
    mass = sum(joint.values(), F(0))
    if not mass:
        raise ValueError('Zero supported mass in independent oracle')
    return variables, {a: w / mass for a, w in joint.items()}


def marginal(variables, joint, scope):
    positions = tuple(variables.index(v) for v in scope)
    values = {a: F(0) for a in product((0, 1), repeat=len(scope))}
    for assignment, weight in joint.items():
        values[tuple(assignment[p] for p in positions)] += weight
    return values


def checked_beliefs(candidate, factors, edges):
    variables, joint = enumerate_joint(factors)
    result = candidate.solve_factors(deepcopy(factors), list(edges))
    if not isinstance(result, (tuple, list)) or len(result) != len(factors):
        return False
    for actual, supplied in zip(result, factors):
        if (not isinstance(actual, dict) or tuple(actual.get('scope', ())) != supplied['scope']
                or actual.get('values') != marginal(variables, joint, supplied['scope'])):
            return False
        if any(type(value) not in (int, F) for value in actual['values'].values()):
            return False
    return True


def outcome(ok, detail, **metrics):
    return {'status': 'PASS' if ok else 'FAIL', 'detail': detail, 'metrics': metrics}


def holonomy_grouped(factory):
    """Represent frustration exactly after explicitly paying three-variable width."""
    candidate = factory()
    soft = factor(('a', 'b', 'c'), lambda a: (3 if a[0] != a[1] else 1)
                  * (3 if a[1] != a[2] else 1) * (3 if a[2] != a[0] else 1))
    boundary = factor(('a', 'b'), lambda a: 1)
    if not checked_beliefs(candidate, [soft, boundary], [(0, 1)]):
        return outcome(False, 'Candidate failed the grouped soft odd-cycle posterior.')
    variables, joint = enumerate_joint([soft, boundary])
    unequal = sum(w for a, w in joint.items() if a[variables.index('a')] != a[variables.index('b')])
    if unequal != F(9, 14):
        raise AssertionError('Independent odd-cycle fixture changed')
    hard = factor(('a', 'b', 'c'), lambda a: int(a[0] != a[1] and a[1] != a[2] and a[2] != a[0]))
    rejected = False
    try:
        candidate.solve_factors([hard, boundary], [(0, 1)])
    except ValueError:
        rejected = True
    return outcome(rejected,
                   'Soft frustration and hard contradiction in an explicitly grouped8-state problem; '
                   'not arbitrary loopy convergence or particle identification.',
                   exact_unequal_probability=str(unequal), misleading_pairwise_value='3/4',
                   hard_zero_support_rejected=rejected, largest_bag_states=8, candidate_calls=2)


def federation_joint_separator(factory):
    """A pair separator must retain parity correlation in both causal directions."""
    candidate = factory()
    scopes = (('a', 'b', 'c'), ('b', 'c', 'd'))
    left = factor(scopes[0], lambda a: 3 if a[0] == a[1] ^ a[2] else 1)
    right = factor(scopes[1], lambda a: 3 if a[2] == a[0] ^ a[1] else 1)
    probabilities = []
    for observed, queried in (('a', 'd'), ('d', 'a')):
        factors = deepcopy([left, right])
        index = 0 if observed == 'a' else 1
        position = factors[index]['scope'].index(observed)
        factors[index]['values'] = {a: w * int(a[position] == 0) for a, w in factors[index]['values'].items()}
        if not checked_beliefs(candidate, factors, [(0, 1)]):
            return outcome(False, 'Candidate lost the joint parity separator or reverse conditioning.')
        variables, joint = enumerate_joint(factors)
        probabilities.append(marginal(variables, joint, (queried,))[(0,)])
        separator = marginal(variables, joint, ('b', 'c'))
        if (separator != {(0, 0): F(3, 8), (0, 1): F(1, 8), (1, 0): F(1, 8), (1, 1): F(3, 8)}):
            raise AssertionError('Parity separator fixture changed')
        # Transport a coordinate relabeling through every occurrence of b.
        for f in factors:
            p = f['scope'].index('b')
            f['values'] = {a[:p] + (1-a[p],) + a[p+1:]: w for a, w in f['values'].items()}
        if not checked_beliefs(candidate, factors, [(0, 1)]):
            return outcome(False, 'Candidate failed consistent gauge relabeling of the joint separator.')
    return outcome(probabilities == [F(5, 8), F(5, 8)],
                   'Joint two-bit boundary, outside conditioning and transported labels; '
                   'no arbitrary federation scalability claim.',
                   forward_probability=str(probabilities[0]), reverse_probability=str(probabilities[1]),
                   independent_singleton_compression='1/2', compression_error='1/8',
                   largest_bag_states=8, candidate_calls=4)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def load_fly_fixture(path=FLY_RECEIPT):
    """Treat pinned row tables as supplied input, never as candidate answers."""
    path = Path(path)
    receipt = json.loads(path.read_text())
    if (receipt.get('schema') != 'cadence-fly-transition/1' or not receipt.get('checks')
            or any(v is not True for v in receipt['checks'].values())
            or receipt['scope']['same_multistep_rate_dynamics'] is not False):
        raise ValueError('Unqualified or misrepresented fly fixture')
    if not receipt.get('source_hashes'):
        raise ValueError('Missing fixture source custody')
    for name, expected in receipt['source_hashes'].items():
        source = (WORKSPACE / name).resolve()
        source.relative_to(WORKSPACE)
        if digest(source) != expected:
            raise ValueError('Changed fly fixture source: ' + name)
    return receipt, digest(path)


def transition_factors(model):
    current = ('s', 'm', 'o', 'i')
    factors = [factor(current, lambda a: F(1, 16))]
    for neuron in range(4):
        rows = [row for row in model['rows'] if row['neuron'] == neuron]
        if not rows or any(row['clipped'] or F(row['mean_error']) != 0 for row in rows):
            raise ValueError('Missing, clipped or non-preserving transition rows')
        parents = tuple(rows[0]['parents'])
        if tuple(sorted(set(parents))) != parents or any(p not in range(4) for p in parents):
            raise ValueError('Invalid transition parent scope')
        values = {}
        for row in rows:
            if tuple(row['parents']) != parents:
                raise ValueError('Inconsistent transition parent scope')
            assignment, probability = tuple(row['current']), F(row['high_probability'])
            if assignment + (0,) in values or not 0 <= probability <= 1:
                raise ValueError('Duplicate or invalid transition row')
            values[assignment + (0,)], values[assignment + (1,)] = 1-probability, probability
        if set(values) != set(product((0, 1), repeat=len(parents)+1)):
            raise ValueError('Incomplete transition table')
        factors.append({'scope': tuple(current[p] for p in parents)+(current[neuron]+'_next',), 'values': values})
    return factors


def fly_transition_fixture(factory):
    candidate = factory()
    receipt, pin = load_fly_fixture()
    chosen = ('rest:intact:pulse=False', 'rest:intact:pulse=True',
              'rest:source_cut:pulse=False', 'rest:inhibitory_cut:pulse=False')
    seen = []
    for name in chosen:
        matches = [model for model in receipt['models'] if model['name'] == name]
        if len(matches) != 1:
            raise ValueError('Missing or duplicate frozen fly condition')
        factors = transition_factors(matches[0])
        if not checked_beliefs(candidate, factors, [(0, i) for i in range(1, 5)]):
            return outcome(False, 'Selected candidate failed independently enumerated fly-derived factors.',
                           failed_condition=name, fixture_sha256=pin)
        seen.append(name)
    return outcome(True,
                   'Same selected candidate solves four supplied fly-derived transition fixtures; '
                   'two-bin stochastic dynamics, not a full fly, original trajectories, motor control or learning.',
                   conditions=seen, fixture_sha256=pin, neurons=4, joint_oracle_states=256,
                   largest_bag_states=32, candidate_calls=4, original_dynamics_preserved=False)


TESTS = {'holonomy_conflict':holonomy_grouped,
         'federation_joint_boundary':federation_joint_separator,
         'fly_directed_transition':fly_transition_fixture}
