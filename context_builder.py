def build_context(partida: dict) -> str:
    version = partida.get("versionJuego", "desconocida")
    jugador = partida.get("nombreJugador", "desconocido")
    inicial = partida.get("pokemonInicial", "desconocido")
    medallas = len(partida.get("medallas", []))
    vidas = partida.get("vidas", 0)

    equipo = partida.get("equipo", [])
    equipo_str = (
        ", ".join(f"{p.get('nombre', '?')} Nv.{p.get('nivel', '?')}" for p in equipo)
        or "Sin equipo"
    )

    muertos = partida.get("muertos", [])
    muertos_str = ", ".join(p.get("nombre", "?") for p in muertos) or "Ninguno"

    combates = partida.get("resultadosCombates", [])
    victorias = sum(1 for c in combates if c.get("victoria"))
    derrotas = len(combates) - victorias

    return (
        f"Partida: Pokémon {version}\n"
        f"Jugador: {jugador} | Inicial: {inicial} | Medallas: {medallas}/8\n"
        f"Vidas restantes: {vidas}\n"
        f"Equipo actual: {equipo_str}\n"
        f"Pokémon caídos: {muertos_str}\n"
        f"Combates: {victorias} victorias, {derrotas} derrotas"
    )
