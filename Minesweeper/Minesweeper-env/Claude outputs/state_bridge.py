"""
Funzioni "ponte" tra MinesweeperEnv (minesweeper_env.py) e la tabella Q
a dizionario discussa nella nostra conversazione.

Queste funzioni si occupano SOLO di leggere lo stato dall'ambiente e
costruire le feature/chiavi - la logica di E-SARSA (scelta epsilon-greedy,
calcolo del valore atteso, aggiornamento di Q) la scrivi tu nel tuo main.
"""

def get_hidden_cells(env):
    """
    Restituisce la lista degli action_index ancora nascosti (celle 'U'),
    ricalcolata da zero leggendo env.state - nessuna struttura da tenere
    sincronizzata a mano, corretta per costruzione anche dopo le cascate.
    """
    return [i for i, t in enumerate(env.state) if t['value'] == 'U']


def build_coord_lookup(env):
    """
    Costruisce UNA VOLA SOLA per turno un dizionario coordinata -> valore,
    a partire da env.state. Passalo poi a get_cell_neighbors_values per
    ogni cella candidata, invece di ricostruire una struttura pandas ad
    ogni singola chiamata: qui ogni lookup diventa O(1) invece di O(N).
    """
    return {t['coord']: t['value'] for t in env.state}


def get_cell_neighbors_values(coord_lookup, coord, ncols, nrows):
    """
    Valori delle celle adiacenti a `coord`, letti dal dizionario
    coord_lookup (costruito da env.state, cioe' quello che l'agente vede
    davvero) - MAI da env.grid o env.board, che contengono la soluzione
    completa della partita.
    """
    x, y = coord[0], coord[1]

    neighbors = []
    for col in range(y - 1, y + 2):
        for row in range(x - 1, x + 2):
            if ((x != row or y != col) and
                    (0 <= col < ncols) and
                    (0 <= row < nrows)):
                neighbors.append(coord_lookup[(row, col)])

    return neighbors


def get_features(env, action_index, coord_lookup):
    """
    Feature per la cella nascosta identificata da action_index, calcolate
    a partire da coord_lookup (vedi build_coord_lookup - costruiscilo una
    volta per turno, prima di valutare tutte le celle candidate).
    Ricalcolo delle feature discusse in precedenza: conteggio vicini
    nascosti, vincolo numerico piu' stringente tra i vicini scoperti,
    categoria di posizione (angolo/bordo/interno).

    Nota: qui non c'e' un conteggio "flagged_neighbors", perche' questo
    ambiente non ha un'azione di contrassegno - solo "rivela".
    """
    coord = env.state[action_index]['coord']
    neighbor_values = get_cell_neighbors_values(coord_lookup, coord, env.ncols, env.nrows)

    hidden_count = sum(1 for v in neighbor_values if v == 'U')
    revealed_numbers = [v for v in neighbor_values if v != 'U']
    min_constraint = min(revealed_numbers) if revealed_numbers else -1

    n_neighbors = len(neighbor_values)
    if n_neighbors == 3:
        position = "corner"
    elif n_neighbors == 5:
        position = "edge"
    else:
        position = "interior"

    return {
        "hidden_neighbors": hidden_count,
        "min_constraint": min_constraint,
        "position": position,
    }


def features_to_key(features):
    """Tupla ordinata in modo fisso, usabile come chiave del dizionario Q."""
    return (
        features["hidden_neighbors"],
        features["min_constraint"],
        features["position"],
    )


def detect_actually_revealed(state_before, state_after):
    """
    Confronta lo stato prima e dopo uno step() e restituisce gli
    action_index le cui celle sono passate da 'U' a un valore rivelato.
    Serve soprattutto per il primo click dell'episodio, quando l'ambiente
    puo' silenziosamente rivelare una cella diversa da quella richiesta
    (redirect di sicurezza sulla prima mossa).
    """
    changed = []
    for i, (before, after) in enumerate(zip(state_before, state_after)):
        if before['value'] == 'U' and after['value'] != 'U':
            changed.append(i)
    return changed
