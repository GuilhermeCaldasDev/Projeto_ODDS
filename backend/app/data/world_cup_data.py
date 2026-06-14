from typing import List, Dict, Any

TEAMS: List[Dict[str, Any]] = [
    # ── GROUP A: Mexico, South Africa, South Korea, Czechia ──────────────────
    {
        "name": "Mexico", "flag": "🇲🇽", "group": "A", "confederation": "CONCACAF",
        "ranking": 11, "attack_rating": 75, "defense_rating": 72,
        "form": ["W", "D", "W", "L", "W"], "goals_scored_avg": 1.9, "goals_conceded_avg": 1.0,
        "key_players": ["Hirving Lozano", "Raúl Jiménez", "Edson Álvarez"],
        "recent_results": [
            {"opponent": "USA", "result": "L", "score": "0-2"},
            {"opponent": "Jamaica", "result": "W", "score": "3-0"},
            {"opponent": "Canada", "result": "D", "score": "1-1"},
            {"opponent": "Costa Rica", "result": "W", "score": "2-1"},
            {"opponent": "Honduras", "result": "W", "score": "2-0"},
        ],
    },
    {
        "name": "South Africa", "flag": "🇿🇦", "group": "A", "confederation": "CAF",
        "ranking": 57, "attack_rating": 52, "defense_rating": 55,
        "form": ["D", "W", "L", "D", "W"], "goals_scored_avg": 1.1, "goals_conceded_avg": 1.4,
        "key_players": ["Percy Tau", "Bongani Zungu", "Ronwen Williams"],
        "recent_results": [
            {"opponent": "Nigeria", "result": "D", "score": "1-1"},
            {"opponent": "Zimbabwe", "result": "W", "score": "2-0"},
            {"opponent": "Morocco", "result": "L", "score": "0-2"},
            {"opponent": "Lesotho", "result": "D", "score": "0-0"},
            {"opponent": "Botswana", "result": "W", "score": "3-1"},
        ],
    },
    {
        "name": "South Korea", "flag": "🇰🇷", "group": "A", "confederation": "AFC",
        "ranking": 23, "attack_rating": 68, "defense_rating": 66,
        "form": ["W", "W", "D", "W", "L"], "goals_scored_avg": 1.7, "goals_conceded_avg": 1.0,
        "key_players": ["Son Heung-min", "Kim Min-jae", "Lee Kang-in"],
        "recent_results": [
            {"opponent": "Iran", "result": "W", "score": "2-0"},
            {"opponent": "Saudi Arabia", "result": "W", "score": "1-0"},
            {"opponent": "Australia", "result": "D", "score": "2-2"},
            {"opponent": "China", "result": "W", "score": "3-0"},
            {"opponent": "Japan", "result": "L", "score": "0-1"},
        ],
    },
    {
        "name": "Czechia", "flag": "🇨🇿", "group": "A", "confederation": "UEFA",
        "ranking": 40, "attack_rating": 60, "defense_rating": 62,
        "form": ["D", "W", "L", "W", "D"], "goals_scored_avg": 1.3, "goals_conceded_avg": 1.1,
        "key_players": ["Patrik Schick", "Tomáš Souček", "Vladimír Coufal"],
        "recent_results": [
            {"opponent": "Poland", "result": "D", "score": "1-1"},
            {"opponent": "Albania", "result": "W", "score": "2-0"},
            {"opponent": "Ukraine", "result": "L", "score": "0-1"},
            {"opponent": "Moldova", "result": "W", "score": "3-0"},
            {"opponent": "Faroe Islands", "result": "D", "score": "1-1"},
        ],
    },
    # ── GROUP B: Canada, Bosnia, Qatar, Switzerland ──────────────────────────
    {
        "name": "Canada", "flag": "🇨🇦", "group": "B", "confederation": "CONCACAF",
        "ranking": 47, "attack_rating": 65, "defense_rating": 63,
        "form": ["W", "D", "L", "W", "W"], "goals_scored_avg": 1.6, "goals_conceded_avg": 1.2,
        "key_players": ["Alphonso Davies", "Jonathan David", "Cyle Larin"],
        "recent_results": [
            {"opponent": "USA", "result": "L", "score": "1-2"},
            {"opponent": "Mexico", "result": "D", "score": "1-1"},
            {"opponent": "Honduras", "result": "W", "score": "2-0"},
            {"opponent": "El Salvador", "result": "W", "score": "3-0"},
            {"opponent": "Jamaica", "result": "W", "score": "4-0"},
        ],
    },
    {
        "name": "Bosnia and Herzegovina", "flag": "🇧🇦", "group": "B", "confederation": "UEFA",
        "ranking": 66, "attack_rating": 58, "defense_rating": 55,
        "form": ["W", "D", "L", "W", "D"], "goals_scored_avg": 1.3, "goals_conceded_avg": 1.3,
        "key_players": ["Edin Džeko", "Miralem Pjanić", "Sead Kolašinac"],
        "recent_results": [
            {"opponent": "Iceland", "result": "W", "score": "2-0"},
            {"opponent": "Finland", "result": "D", "score": "1-1"},
            {"opponent": "Slovakia", "result": "L", "score": "0-1"},
            {"opponent": "Romania", "result": "W", "score": "2-1"},
            {"opponent": "Liechtenstein", "result": "D", "score": "0-0"},
        ],
    },
    {
        "name": "Qatar", "flag": "🇶🇦", "group": "B", "confederation": "AFC",
        "ranking": 37, "attack_rating": 52, "defense_rating": 48,
        "form": ["L", "D", "L", "W", "L"], "goals_scored_avg": 1.1, "goals_conceded_avg": 1.8,
        "key_players": ["Akram Afif", "Hassan Al-Haydos", "Almoez Ali"],
        "recent_results": [
            {"opponent": "UAE", "result": "L", "score": "1-2"},
            {"opponent": "Iraq", "result": "D", "score": "1-1"},
            {"opponent": "Iran", "result": "L", "score": "0-2"},
            {"opponent": "Bahrain", "result": "W", "score": "3-0"},
            {"opponent": "Kuwait", "result": "L", "score": "0-1"},
        ],
    },
    {
        "name": "Switzerland", "flag": "🇨🇭", "group": "B", "confederation": "UEFA",
        "ranking": 19, "attack_rating": 72, "defense_rating": 74,
        "form": ["W", "W", "D", "W", "D"], "goals_scored_avg": 1.8, "goals_conceded_avg": 0.9,
        "key_players": ["Granit Xhaka", "Xherdan Shaqiri", "Yann Sommer"],
        "recent_results": [
            {"opponent": "Czech Republic", "result": "W", "score": "2-0"},
            {"opponent": "Romania", "result": "W", "score": "2-0"},
            {"opponent": "Kosovo", "result": "D", "score": "1-1"},
            {"opponent": "Belarus", "result": "W", "score": "3-0"},
            {"opponent": "Lithuania", "result": "D", "score": "1-1"},
        ],
    },
    # ── GROUP C: Brazil, Haiti, Morocco, Scotland ────────────────────────────
    {
        "name": "Brazil", "flag": "🇧🇷", "group": "C", "confederation": "CONMEBOL",
        "ranking": 3, "attack_rating": 90, "defense_rating": 84,
        "form": ["W", "W", "D", "W", "W"], "goals_scored_avg": 2.7, "goals_conceded_avg": 0.6,
        "key_players": ["Vinicius Jr.", "Rodrygo", "Casemiro"],
        "recent_results": [
            {"opponent": "Argentina", "result": "L", "score": "0-1"},
            {"opponent": "Peru", "result": "W", "score": "4-0"},
            {"opponent": "Colombia", "result": "W", "score": "2-0"},
            {"opponent": "Venezuela", "result": "W", "score": "3-1"},
            {"opponent": "Bolivia", "result": "D", "score": "1-1"},
        ],
    },
    {
        "name": "Haiti", "flag": "🇭🇹", "group": "C", "confederation": "CONCACAF",
        "ranking": 83, "attack_rating": 42, "defense_rating": 40,
        "form": ["L", "D", "L", "L", "W"], "goals_scored_avg": 0.7, "goals_conceded_avg": 2.0,
        "key_players": ["Duckens Nazon", "Frantz Bertin", "Wecly Florestal"],
        "recent_results": [
            {"opponent": "Jamaica", "result": "L", "score": "0-2"},
            {"opponent": "Cuba", "result": "D", "score": "1-1"},
            {"opponent": "Panama", "result": "L", "score": "0-3"},
            {"opponent": "Guyana", "result": "L", "score": "0-1"},
            {"opponent": "Suriname", "result": "W", "score": "2-0"},
        ],
    },
    {
        "name": "Morocco", "flag": "🇲🇦", "group": "C", "confederation": "CAF",
        "ranking": 14, "attack_rating": 72, "defense_rating": 76,
        "form": ["W", "D", "W", "W", "D"], "goals_scored_avg": 1.6, "goals_conceded_avg": 0.7,
        "key_players": ["Hakim Ziyech", "Youssef En-Nesyri", "Achraf Hakimi"],
        "recent_results": [
            {"opponent": "Senegal", "result": "D", "score": "1-1"},
            {"opponent": "Guinea", "result": "W", "score": "2-0"},
            {"opponent": "Nigeria", "result": "D", "score": "0-0"},
            {"opponent": "Congo", "result": "W", "score": "3-0"},
            {"opponent": "Tanzania", "result": "W", "score": "2-0"},
        ],
    },
    {
        "name": "Scotland", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "group": "C", "confederation": "UEFA",
        "ranking": 39, "attack_rating": 60, "defense_rating": 62,
        "form": ["D", "W", "L", "D", "W"], "goals_scored_avg": 1.3, "goals_conceded_avg": 1.2,
        "key_players": ["Andy Robertson", "Callum McGregor", "Lyndon Dykes"],
        "recent_results": [
            {"opponent": "Croatia", "result": "D", "score": "1-1"},
            {"opponent": "Armenia", "result": "W", "score": "4-1"},
            {"opponent": "Latvia", "result": "D", "score": "0-0"},
            {"opponent": "Turkey", "result": "L", "score": "0-1"},
            {"opponent": "Kosovo", "result": "W", "score": "2-1"},
        ],
    },
    # ── GROUP D: United States, Paraguay, Australia, Türkiye ─────────────────
    {
        "name": "United States", "flag": "🇺🇸", "group": "D", "confederation": "CONCACAF",
        "ranking": 16, "attack_rating": 72, "defense_rating": 70,
        "form": ["W", "D", "W", "W", "D"], "goals_scored_avg": 1.7, "goals_conceded_avg": 1.0,
        "key_players": ["Christian Pulisic", "Weston McKennie", "Tyler Adams"],
        "recent_results": [
            {"opponent": "Mexico", "result": "W", "score": "2-0"},
            {"opponent": "Germany", "result": "D", "score": "1-1"},
            {"opponent": "Jamaica", "result": "W", "score": "4-0"},
            {"opponent": "Canada", "result": "W", "score": "2-1"},
            {"opponent": "Panama", "result": "D", "score": "0-0"},
        ],
    },
    {
        "name": "Paraguay", "flag": "🇵🇾", "group": "D", "confederation": "CONMEBOL",
        "ranking": 54, "attack_rating": 58, "defense_rating": 60,
        "form": ["D", "W", "L", "D", "W"], "goals_scored_avg": 1.2, "goals_conceded_avg": 1.1,
        "key_players": ["Miguel Almirón", "Julio Enciso", "Gustavo Gómez"],
        "recent_results": [
            {"opponent": "Uruguay", "result": "D", "score": "0-0"},
            {"opponent": "Bolivia", "result": "W", "score": "2-0"},
            {"opponent": "Brazil", "result": "L", "score": "0-4"},
            {"opponent": "Chile", "result": "D", "score": "1-1"},
            {"opponent": "Venezuela", "result": "W", "score": "2-0"},
        ],
    },
    {
        "name": "Australia", "flag": "🇦🇺", "group": "D", "confederation": "AFC",
        "ranking": 25, "attack_rating": 63, "defense_rating": 60,
        "form": ["W", "D", "W", "L", "W"], "goals_scored_avg": 1.5, "goals_conceded_avg": 1.2,
        "key_players": ["Mat Ryan", "Aaron Mooy", "Martin Boyle"],
        "recent_results": [
            {"opponent": "New Zealand", "result": "W", "score": "2-0"},
            {"opponent": "Japan", "result": "D", "score": "1-1"},
            {"opponent": "China", "result": "W", "score": "3-0"},
            {"opponent": "South Korea", "result": "L", "score": "1-2"},
            {"opponent": "Indonesia", "result": "W", "score": "4-0"},
        ],
    },
    {
        "name": "Türkiye", "flag": "🇹🇷", "group": "D", "confederation": "UEFA",
        "ranking": 28, "attack_rating": 65, "defense_rating": 63,
        "form": ["W", "W", "D", "L", "W"], "goals_scored_avg": 1.6, "goals_conceded_avg": 1.1,
        "key_players": ["Hakan Çalhanoğlu", "Arda Güler", "Merih Demiral"],
        "recent_results": [
            {"opponent": "Czech Republic", "result": "W", "score": "2-1"},
            {"opponent": "Hungary", "result": "W", "score": "1-0"},
            {"opponent": "Netherlands", "result": "D", "score": "2-2"},
            {"opponent": "Germany", "result": "L", "score": "1-3"},
            {"opponent": "Wales", "result": "W", "score": "1-0"},
        ],
    },
    # ── GROUP E: Germany, Curaçao, Ivory Coast, Ecuador ─────────────────────
    {
        "name": "Germany", "flag": "🇩🇪", "group": "E", "confederation": "UEFA",
        "ranking": 10, "attack_rating": 82, "defense_rating": 78,
        "form": ["W", "D", "W", "W", "W"], "goals_scored_avg": 2.2, "goals_conceded_avg": 0.9,
        "key_players": ["Manuel Neuer", "Thomas Müller", "Kai Havertz"],
        "recent_results": [
            {"opponent": "England", "result": "D", "score": "1-1"},
            {"opponent": "Italy", "result": "W", "score": "3-1"},
            {"opponent": "Netherlands", "result": "D", "score": "2-2"},
            {"opponent": "Hungary", "result": "W", "score": "3-0"},
            {"opponent": "Estonia", "result": "W", "score": "4-0"},
        ],
    },
    {
        "name": "Curaçao", "flag": "🇨🇼", "group": "E", "confederation": "CONCACAF",
        "ranking": 85, "attack_rating": 45, "defense_rating": 43,
        "form": ["D", "L", "W", "L", "L"], "goals_scored_avg": 0.9, "goals_conceded_avg": 1.8,
        "key_players": ["Cuco Martina", "Juriën Timber", "Leandro Bacuna"],
        "recent_results": [
            {"opponent": "Panama", "result": "D", "score": "1-1"},
            {"opponent": "Trinidad", "result": "L", "score": "0-1"},
            {"opponent": "Jamaica", "result": "W", "score": "2-0"},
            {"opponent": "Costa Rica", "result": "L", "score": "0-2"},
            {"opponent": "Honduras", "result": "L", "score": "0-1"},
        ],
    },
    {
        "name": "Ivory Coast", "flag": "🇨🇮", "group": "E", "confederation": "CAF",
        "ranking": 45, "attack_rating": 65, "defense_rating": 60,
        "form": ["W", "D", "W", "L", "W"], "goals_scored_avg": 1.5, "goals_conceded_avg": 1.1,
        "key_players": ["Sébastien Haller", "Franck Kessié", "Nicolas Pépé"],
        "recent_results": [
            {"opponent": "Cameroon", "result": "W", "score": "1-0"},
            {"opponent": "Ghana", "result": "D", "score": "0-0"},
            {"opponent": "Nigeria", "result": "W", "score": "2-1"},
            {"opponent": "Senegal", "result": "L", "score": "0-1"},
            {"opponent": "Guinea", "result": "W", "score": "3-0"},
        ],
    },
    {
        "name": "Ecuador", "flag": "🇪🇨", "group": "E", "confederation": "CONMEBOL",
        "ranking": 44, "attack_rating": 62, "defense_rating": 60,
        "form": ["W", "D", "W", "L", "W"], "goals_scored_avg": 1.5, "goals_conceded_avg": 1.2,
        "key_players": ["Enner Valencia", "Moisés Caicedo", "Gonzalo Plata"],
        "recent_results": [
            {"opponent": "Bolivia", "result": "W", "score": "2-1"},
            {"opponent": "Venezuela", "result": "W", "score": "3-1"},
            {"opponent": "Chile", "result": "D", "score": "1-1"},
            {"opponent": "Colombia", "result": "W", "score": "1-0"},
            {"opponent": "Argentina", "result": "L", "score": "0-1"},
        ],
    },
    # ── GROUP F: Netherlands, Japan, Sweden, Tunisia ─────────────────────────
    {
        "name": "Netherlands", "flag": "🇳🇱", "group": "F", "confederation": "UEFA",
        "ranking": 7, "attack_rating": 82, "defense_rating": 80,
        "form": ["W", "W", "D", "W", "W"], "goals_scored_avg": 2.2, "goals_conceded_avg": 0.9,
        "key_players": ["Virgil van Dijk", "Memphis Depay", "Frenkie de Jong"],
        "recent_results": [
            {"opponent": "Belgium", "result": "W", "score": "2-1"},
            {"opponent": "France", "result": "W", "score": "2-1"},
            {"opponent": "Germany", "result": "D", "score": "2-2"},
            {"opponent": "Turkey", "result": "W", "score": "4-2"},
            {"opponent": "Austria", "result": "W", "score": "3-0"},
        ],
    },
    {
        "name": "Japan", "flag": "🇯🇵", "group": "F", "confederation": "AFC",
        "ranking": 17, "attack_rating": 71, "defense_rating": 68,
        "form": ["W", "W", "D", "W", "W"], "goals_scored_avg": 2.0, "goals_conceded_avg": 0.9,
        "key_players": ["Takumi Minamino", "Daichi Kamada", "Wataru Endō"],
        "recent_results": [
            {"opponent": "Australia", "result": "D", "score": "1-1"},
            {"opponent": "Saudi Arabia", "result": "W", "score": "2-0"},
            {"opponent": "China", "result": "W", "score": "3-0"},
            {"opponent": "Vietnam", "result": "W", "score": "3-0"},
            {"opponent": "Iran", "result": "L", "score": "1-2"},
        ],
    },
    {
        "name": "Sweden", "flag": "🇸🇪", "group": "F", "confederation": "UEFA",
        "ranking": 25, "attack_rating": 68, "defense_rating": 65,
        "form": ["W", "D", "W", "W", "D"], "goals_scored_avg": 1.7, "goals_conceded_avg": 1.0,
        "key_players": ["Alexander Isak", "Dejan Kulusevski", "Victor Nilsson Lindelöf"],
        "recent_results": [
            {"opponent": "Finland", "result": "W", "score": "2-0"},
            {"opponent": "Norway", "result": "D", "score": "1-1"},
            {"opponent": "Estonia", "result": "W", "score": "3-0"},
            {"opponent": "Kosovo", "result": "W", "score": "2-1"},
            {"opponent": "Slovakia", "result": "D", "score": "0-0"},
        ],
    },
    {
        "name": "Tunisia", "flag": "🇹🇳", "group": "F", "confederation": "CAF",
        "ranking": 34, "attack_rating": 60, "defense_rating": 62,
        "form": ["W", "D", "W", "D", "L"], "goals_scored_avg": 1.3, "goals_conceded_avg": 1.0,
        "key_players": ["Wahbi Khazri", "Youssef Msakni", "Dylan Bronn"],
        "recent_results": [
            {"opponent": "Libya", "result": "W", "score": "2-0"},
            {"opponent": "Equatorial Guinea", "result": "D", "score": "1-1"},
            {"opponent": "Comoros", "result": "W", "score": "3-0"},
            {"opponent": "Mali", "result": "D", "score": "0-0"},
            {"opponent": "Nigeria", "result": "L", "score": "1-2"},
        ],
    },
    # ── GROUP G: Belgium, Egypt, Iran, New Zealand ───────────────────────────
    {
        "name": "Belgium", "flag": "🇧🇪", "group": "G", "confederation": "UEFA",
        "ranking": 4, "attack_rating": 85, "defense_rating": 80,
        "form": ["W", "W", "D", "W", "W"], "goals_scored_avg": 2.2, "goals_conceded_avg": 0.9,
        "key_players": ["Kevin De Bruyne", "Romelu Lukaku", "Thibaut Courtois"],
        "recent_results": [
            {"opponent": "Netherlands", "result": "L", "score": "1-2"},
            {"opponent": "Wales", "result": "D", "score": "1-1"},
            {"opponent": "Czech Republic", "result": "W", "score": "3-2"},
            {"opponent": "Estonia", "result": "W", "score": "3-0"},
            {"opponent": "Poland", "result": "W", "score": "2-1"},
        ],
    },
    {
        "name": "Egypt", "flag": "🇪🇬", "group": "G", "confederation": "CAF",
        "ranking": 35, "attack_rating": 62, "defense_rating": 65,
        "form": ["W", "D", "W", "D", "L"], "goals_scored_avg": 1.3, "goals_conceded_avg": 1.0,
        "key_players": ["Mohamed Salah", "Ahmed El Shenawy", "Trezeguet"],
        "recent_results": [
            {"opponent": "Ghana", "result": "W", "score": "2-0"},
            {"opponent": "Sudan", "result": "D", "score": "1-1"},
            {"opponent": "Ethiopia", "result": "W", "score": "3-0"},
            {"opponent": "Cape Verde", "result": "D", "score": "0-0"},
            {"opponent": "Senegal", "result": "L", "score": "0-1"},
        ],
    },
    {
        "name": "Iran", "flag": "🇮🇷", "group": "G", "confederation": "AFC",
        "ranking": 22, "attack_rating": 62, "defense_rating": 65,
        "form": ["W", "D", "W", "L", "W"], "goals_scored_avg": 1.4, "goals_conceded_avg": 1.1,
        "key_players": ["Sardar Azmoun", "Mehdi Taremi", "Alireza Jahanbakhsh"],
        "recent_results": [
            {"opponent": "Syria", "result": "W", "score": "2-0"},
            {"opponent": "Hong Kong", "result": "D", "score": "1-1"},
            {"opponent": "UAE", "result": "W", "score": "3-1"},
            {"opponent": "South Korea", "result": "L", "score": "0-2"},
            {"opponent": "Japan", "result": "W", "score": "2-1"},
        ],
    },
    {
        "name": "New Zealand", "flag": "🇳🇿", "group": "G", "confederation": "OFC",
        "ranking": 94, "attack_rating": 40, "defense_rating": 45,
        "form": ["D", "L", "W", "L", "L"], "goals_scored_avg": 0.8, "goals_conceded_avg": 1.8,
        "key_players": ["Chris Wood", "Clayton Lewis", "Winston Reid"],
        "recent_results": [
            {"opponent": "Australia", "result": "L", "score": "0-2"},
            {"opponent": "Fiji", "result": "D", "score": "1-1"},
            {"opponent": "Papua New Guinea", "result": "W", "score": "3-0"},
            {"opponent": "Solomon Islands", "result": "L", "score": "0-1"},
            {"opponent": "Vanuatu", "result": "L", "score": "0-1"},
        ],
    },
    # ── GROUP H: Spain, Saudi Arabia, Uruguay, Cape Verde ────────────────────
    {
        "name": "Spain", "flag": "🇪🇸", "group": "H", "confederation": "UEFA",
        "ranking": 8, "attack_rating": 85, "defense_rating": 84,
        "form": ["W", "W", "W", "D", "W"], "goals_scored_avg": 2.4, "goals_conceded_avg": 0.7,
        "key_players": ["Pedri", "Álvaro Morata", "Rodri"],
        "recent_results": [
            {"opponent": "England", "result": "L", "score": "1-2"},
            {"opponent": "Albania", "result": "W", "score": "3-0"},
            {"opponent": "Norway", "result": "W", "score": "3-0"},
            {"opponent": "Scotland", "result": "W", "score": "2-0"},
            {"opponent": "Cyprus", "result": "D", "score": "1-1"},
        ],
    },
    {
        "name": "Saudi Arabia", "flag": "🇸🇦", "group": "H", "confederation": "AFC",
        "ranking": 56, "attack_rating": 54, "defense_rating": 55,
        "form": ["D", "W", "L", "L", "W"], "goals_scored_avg": 1.2, "goals_conceded_avg": 1.5,
        "key_players": ["Salem Al-Dawsari", "Mohammed Al-Owais", "Saleh Al-Shehri"],
        "recent_results": [
            {"opponent": "Thailand", "result": "D", "score": "1-1"},
            {"opponent": "Kuwait", "result": "W", "score": "2-0"},
            {"opponent": "Japan", "result": "L", "score": "0-2"},
            {"opponent": "South Korea", "result": "L", "score": "0-1"},
            {"opponent": "Oman", "result": "W", "score": "3-0"},
        ],
    },
    {
        "name": "Uruguay", "flag": "🇺🇾", "group": "H", "confederation": "CONMEBOL",
        "ranking": 16, "attack_rating": 73, "defense_rating": 72,
        "form": ["W", "W", "D", "W", "L"], "goals_scored_avg": 1.8, "goals_conceded_avg": 0.9,
        "key_players": ["Luis Suárez", "Federico Valverde", "Darwin Núñez"],
        "recent_results": [
            {"opponent": "Argentina", "result": "L", "score": "1-3"},
            {"opponent": "Bolivia", "result": "W", "score": "3-0"},
            {"opponent": "Peru", "result": "W", "score": "2-1"},
            {"opponent": "Venezuela", "result": "D", "score": "1-1"},
            {"opponent": "Ecuador", "result": "W", "score": "2-0"},
        ],
    },
    {
        "name": "Cape Verde", "flag": "🇨🇻", "group": "H", "confederation": "CAF",
        "ranking": 72, "attack_rating": 50, "defense_rating": 52,
        "form": ["W", "D", "L", "W", "D"], "goals_scored_avg": 1.0, "goals_conceded_avg": 1.2,
        "key_players": ["Ryan Mendes", "Garry Rodrigues", "Steven Fortes"],
        "recent_results": [
            {"opponent": "Mauritania", "result": "W", "score": "2-0"},
            {"opponent": "Egypt", "result": "D", "score": "0-0"},
            {"opponent": "Senegal", "result": "L", "score": "0-2"},
            {"opponent": "Sudan", "result": "W", "score": "1-0"},
            {"opponent": "Niger", "result": "D", "score": "1-1"},
        ],
    },
    # ── GROUP I: France, Senegal, Norway, Iraq ───────────────────────────────
    {
        "name": "France", "flag": "🇫🇷", "group": "I", "confederation": "UEFA",
        "ranking": 2, "attack_rating": 92, "defense_rating": 88,
        "form": ["W", "W", "W", "W", "W"], "goals_scored_avg": 2.6, "goals_conceded_avg": 0.7,
        "key_players": ["Kylian Mbappé", "Antoine Griezmann", "Aurélien Tchouaméni"],
        "recent_results": [
            {"opponent": "Netherlands", "result": "L", "score": "1-2"},
            {"opponent": "Austria", "result": "W", "score": "2-0"},
            {"opponent": "Denmark", "result": "W", "score": "3-1"},
            {"opponent": "Portugal", "result": "W", "score": "2-1"},
            {"opponent": "Italy", "result": "W", "score": "3-0"},
        ],
    },
    {
        "name": "Senegal", "flag": "🇸🇳", "group": "I", "confederation": "CAF",
        "ranking": 20, "attack_rating": 72, "defense_rating": 70,
        "form": ["W", "W", "W", "D", "W"], "goals_scored_avg": 1.8, "goals_conceded_avg": 0.9,
        "key_players": ["Sadio Mané", "Kalidou Koulibaly", "Idrissa Gueye"],
        "recent_results": [
            {"opponent": "Sudan", "result": "W", "score": "3-0"},
            {"opponent": "Togo", "result": "W", "score": "2-0"},
            {"opponent": "Rwanda", "result": "W", "score": "4-0"},
            {"opponent": "Morocco", "result": "D", "score": "1-1"},
            {"opponent": "Egypt", "result": "W", "score": "1-0"},
        ],
    },
    {
        "name": "Norway", "flag": "🇳🇴", "group": "I", "confederation": "UEFA",
        "ranking": 35, "attack_rating": 68, "defense_rating": 62,
        "form": ["W", "W", "D", "W", "L"], "goals_scored_avg": 1.8, "goals_conceded_avg": 1.1,
        "key_players": ["Erling Haaland", "Martin Ødegaard", "Alexander Sørloth"],
        "recent_results": [
            {"opponent": "Finland", "result": "W", "score": "3-1"},
            {"opponent": "Moldova", "result": "W", "score": "4-0"},
            {"opponent": "Sweden", "result": "D", "score": "1-1"},
            {"opponent": "Denmark", "result": "W", "score": "2-0"},
            {"opponent": "Spain", "result": "L", "score": "0-3"},
        ],
    },
    {
        "name": "Iraq", "flag": "🇮🇶", "group": "I", "confederation": "AFC",
        "ranking": 55, "attack_rating": 52, "defense_rating": 55,
        "form": ["W", "D", "D", "L", "W"], "goals_scored_avg": 1.1, "goals_conceded_avg": 1.3,
        "key_players": ["Mohanad Ali", "Amjed Attwan", "Ahmed Ibrahim"],
        "recent_results": [
            {"opponent": "UAE", "result": "W", "score": "2-1"},
            {"opponent": "Kuwait", "result": "D", "score": "1-1"},
            {"opponent": "Qatar", "result": "D", "score": "1-1"},
            {"opponent": "Iran", "result": "L", "score": "0-1"},
            {"opponent": "Syria", "result": "W", "score": "2-0"},
        ],
    },
    # ── GROUP J: Argentina, Algeria, Austria, Jordan ─────────────────────────
    {
        "name": "Argentina", "flag": "🇦🇷", "group": "J", "confederation": "CONMEBOL",
        "ranking": 1, "attack_rating": 93, "defense_rating": 87,
        "form": ["W", "W", "W", "W", "D"], "goals_scored_avg": 2.8, "goals_conceded_avg": 0.6,
        "key_players": ["Lionel Messi", "Julián Álvarez", "Rodrigo De Paul"],
        "recent_results": [
            {"opponent": "Brazil", "result": "W", "score": "1-0"},
            {"opponent": "Uruguay", "result": "W", "score": "3-1"},
            {"opponent": "Colombia", "result": "W", "score": "2-0"},
            {"opponent": "Ecuador", "result": "W", "score": "1-0"},
            {"opponent": "Paraguay", "result": "D", "score": "0-0"},
        ],
    },
    {
        "name": "Algeria", "flag": "🇩🇿", "group": "J", "confederation": "CAF",
        "ranking": 32, "attack_rating": 65, "defense_rating": 65,
        "form": ["W", "D", "W", "W", "D"], "goals_scored_avg": 1.5, "goals_conceded_avg": 1.0,
        "key_players": ["Riyad Mahrez", "Islam Slimani", "Sofiane Feghouli"],
        "recent_results": [
            {"opponent": "Burkina Faso", "result": "W", "score": "2-0"},
            {"opponent": "Niger", "result": "D", "score": "0-0"},
            {"opponent": "Uganda", "result": "W", "score": "3-1"},
            {"opponent": "Guinea", "result": "W", "score": "2-1"},
            {"opponent": "Cameroon", "result": "D", "score": "1-1"},
        ],
    },
    {
        "name": "Austria", "flag": "🇦🇹", "group": "J", "confederation": "UEFA",
        "ranking": 24, "attack_rating": 68, "defense_rating": 65,
        "form": ["W", "D", "W", "W", "D"], "goals_scored_avg": 1.7, "goals_conceded_avg": 1.0,
        "key_players": ["David Alaba", "Marcel Sabitzer", "Christoph Baumgartner"],
        "recent_results": [
            {"opponent": "Finland", "result": "W", "score": "2-0"},
            {"opponent": "Sweden", "result": "D", "score": "1-1"},
            {"opponent": "Estonia", "result": "W", "score": "3-0"},
            {"opponent": "Serbia", "result": "W", "score": "2-0"},
            {"opponent": "Netherlands", "result": "L", "score": "0-3"},
        ],
    },
    {
        "name": "Jordan", "flag": "🇯🇴", "group": "J", "confederation": "AFC",
        "ranking": 68, "attack_rating": 50, "defense_rating": 52,
        "form": ["W", "D", "L", "D", "W"], "goals_scored_avg": 1.0, "goals_conceded_avg": 1.4,
        "key_players": ["Musa Al-Taamari", "Ahmad Hayel", "Yazan Al-Naimat"],
        "recent_results": [
            {"opponent": "Kuwait", "result": "W", "score": "2-1"},
            {"opponent": "UAE", "result": "D", "score": "0-0"},
            {"opponent": "Bahrain", "result": "L", "score": "0-1"},
            {"opponent": "Qatar", "result": "D", "score": "1-1"},
            {"opponent": "Iraq", "result": "W", "score": "2-0"},
        ],
    },
    # ── GROUP K: Portugal, Colombia, DR Congo, Uzbekistan ────────────────────
    {
        "name": "Portugal", "flag": "🇵🇹", "group": "K", "confederation": "UEFA",
        "ranking": 6, "attack_rating": 87, "defense_rating": 80,
        "form": ["W", "W", "W", "W", "W"], "goals_scored_avg": 2.5, "goals_conceded_avg": 0.7,
        "key_players": ["Cristiano Ronaldo", "Bruno Fernandes", "Bernardo Silva"],
        "recent_results": [
            {"opponent": "Serbia", "result": "W", "score": "3-1"},
            {"opponent": "Luxembourg", "result": "W", "score": "4-0"},
            {"opponent": "Ireland", "result": "W", "score": "2-1"},
            {"opponent": "Slovakia", "result": "W", "score": "3-0"},
            {"opponent": "Bosnia", "result": "W", "score": "2-0"},
        ],
    },
    {
        "name": "Colombia", "flag": "🇨🇴", "group": "K", "confederation": "CONMEBOL",
        "ranking": 11, "attack_rating": 80, "defense_rating": 76,
        "form": ["W", "W", "W", "D", "W"], "goals_scored_avg": 2.0, "goals_conceded_avg": 0.9,
        "key_players": ["James Rodríguez", "Luis Díaz", "Radamel Falcao"],
        "recent_results": [
            {"opponent": "Brazil", "result": "L", "score": "0-2"},
            {"opponent": "Paraguay", "result": "W", "score": "2-0"},
            {"opponent": "Ecuador", "result": "W", "score": "1-0"},
            {"opponent": "Venezuela", "result": "W", "score": "3-0"},
            {"opponent": "Bolivia", "result": "D", "score": "0-0"},
        ],
    },
    {
        "name": "DR Congo", "flag": "🇨🇩", "group": "K", "confederation": "CAF",
        "ranking": 53, "attack_rating": 56, "defense_rating": 54,
        "form": ["W", "D", "L", "W", "D"], "goals_scored_avg": 1.2, "goals_conceded_avg": 1.3,
        "key_players": ["Cédric Bakambu", "Jonathan Bolingi", "Chancel Mbemba"],
        "recent_results": [
            {"opponent": "Ivory Coast", "result": "W", "score": "1-0"},
            {"opponent": "Zambia", "result": "D", "score": "1-1"},
            {"opponent": "Egypt", "result": "L", "score": "0-2"},
            {"opponent": "Angola", "result": "W", "score": "2-0"},
            {"opponent": "Tanzania", "result": "D", "score": "0-0"},
        ],
    },
    {
        "name": "Uzbekistan", "flag": "🇺🇿", "group": "K", "confederation": "AFC",
        "ranking": 74, "attack_rating": 52, "defense_rating": 50,
        "form": ["W", "D", "L", "D", "W"], "goals_scored_avg": 1.2, "goals_conceded_avg": 1.3,
        "key_players": ["Eldor Shomurodov", "Jasur Yaxshiboyev", "Jamshid Iskanderov"],
        "recent_results": [
            {"opponent": "Tajikistan", "result": "W", "score": "3-0"},
            {"opponent": "Iran", "result": "D", "score": "1-1"},
            {"opponent": "South Korea", "result": "L", "score": "0-3"},
            {"opponent": "Syria", "result": "D", "score": "0-0"},
            {"opponent": "Afghanistan", "result": "W", "score": "4-0"},
        ],
    },
    # ── GROUP L: England, Croatia, Ghana, Panama ─────────────────────────────
    {
        "name": "England", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "group": "L", "confederation": "UEFA",
        "ranking": 5, "attack_rating": 84, "defense_rating": 79,
        "form": ["W", "W", "W", "D", "W"], "goals_scored_avg": 2.1, "goals_conceded_avg": 0.8,
        "key_players": ["Harry Kane", "Jude Bellingham", "Bukayo Saka"],
        "recent_results": [
            {"opponent": "Italy", "result": "W", "score": "3-1"},
            {"opponent": "Ukraine", "result": "W", "score": "2-0"},
            {"opponent": "Brazil", "result": "W", "score": "1-0"},
            {"opponent": "Germany", "result": "D", "score": "1-1"},
            {"opponent": "Spain", "result": "W", "score": "2-1"},
        ],
    },
    {
        "name": "Croatia", "flag": "🇭🇷", "group": "L", "confederation": "UEFA",
        "ranking": 9, "attack_rating": 76, "defense_rating": 74,
        "form": ["W", "D", "W", "D", "W"], "goals_scored_avg": 1.8, "goals_conceded_avg": 0.9,
        "key_players": ["Luka Modrić", "Ivan Perišić", "Dominik Livaković"],
        "recent_results": [
            {"opponent": "Denmark", "result": "D", "score": "0-0"},
            {"opponent": "France", "result": "L", "score": "1-2"},
            {"opponent": "Austria", "result": "W", "score": "2-1"},
            {"opponent": "Slovakia", "result": "D", "score": "1-1"},
            {"opponent": "Armenia", "result": "W", "score": "2-0"},
        ],
    },
    {
        "name": "Ghana", "flag": "🇬🇭", "group": "L", "confederation": "CAF",
        "ranking": 61, "attack_rating": 58, "defense_rating": 55,
        "form": ["L", "W", "D", "L", "W"], "goals_scored_avg": 1.3, "goals_conceded_avg": 1.5,
        "key_players": ["Jordan Ayew", "André Ayew", "Thomas Partey"],
        "recent_results": [
            {"opponent": "Morocco", "result": "L", "score": "0-1"},
            {"opponent": "Cape Verde", "result": "W", "score": "2-1"},
            {"opponent": "Algeria", "result": "D", "score": "1-1"},
            {"opponent": "Egypt", "result": "L", "score": "0-2"},
            {"opponent": "Zimbabwe", "result": "W", "score": "2-0"},
        ],
    },
    {
        "name": "Panama", "flag": "🇵🇦", "group": "L", "confederation": "CONCACAF",
        "ranking": 71, "attack_rating": 48, "defense_rating": 50,
        "form": ["W", "D", "L", "D", "W"], "goals_scored_avg": 1.0, "goals_conceded_avg": 1.3,
        "key_players": ["Ismael Díaz", "Édgar Bárcenas", "Rolando Blackburn"],
        "recent_results": [
            {"opponent": "El Salvador", "result": "W", "score": "2-0"},
            {"opponent": "Costa Rica", "result": "D", "score": "0-0"},
            {"opponent": "Jamaica", "result": "L", "score": "0-1"},
            {"opponent": "Honduras", "result": "D", "score": "1-1"},
            {"opponent": "Cuba", "result": "W", "score": "3-0"},
        ],
    },
]

# ── 72 GROUP STAGE MATCHES ────────────────────────────────────────────────────
MATCHES: List[Dict[str, Any]] = [
    # Group A
    {"id": 1, "home_team": "Mexico", "away_team": "South Africa", "group": "A", "date": "2026-06-11", "time": "15:00", "venue": "Estadio Azteca (Ciudad de México)", "home_score": 2, "away_score": 0},
    {"id": 2, "home_team": "South Korea", "away_team": "Czechia", "group": "A", "date": "2026-06-11", "time": "22:00", "venue": "Estadio Akron (Guadalajara)", "home_score": 2, "away_score": 1},
    {"id": 3, "home_team": "Czechia", "away_team": "South Africa", "group": "A", "date": "2026-06-18", "time": "12:00", "venue": "Mercedes-Benz Stadium (Atlanta)"},
    {"id": 4, "home_team": "Mexico", "away_team": "South Korea", "group": "A", "date": "2026-06-18", "time": "21:00", "venue": "Estadio Akron (Guadalajara)"},
    {"id": 5, "home_team": "South Africa", "away_team": "South Korea", "group": "A", "date": "2026-06-24", "time": "16:00", "venue": "AT&T Stadium (Arlington)"},
    {"id": 6, "home_team": "Czechia", "away_team": "Mexico", "group": "A", "date": "2026-06-24", "time": "16:00", "venue": "Estadio Azteca (Ciudad de México)"},
    # Group B
    {"id": 7, "home_team": "Canada", "away_team": "Bosnia and Herzegovina", "group": "B", "date": "2026-06-12", "time": "15:00", "venue": "BMO Field (Toronto)", "home_score": 1, "away_score": 1},
    {"id": 8, "home_team": "Qatar", "away_team": "Switzerland", "group": "B", "date": "2026-06-13", "time": "15:00", "venue": "Levi's Stadium (Santa Clara)"},
    {"id": 9, "home_team": "Switzerland", "away_team": "Bosnia and Herzegovina", "group": "B", "date": "2026-06-18", "time": "15:00", "venue": "SoFi Stadium (Los Angeles)"},
    {"id": 10, "home_team": "Canada", "away_team": "Qatar", "group": "B", "date": "2026-06-18", "time": "18:00", "venue": "BC Place (Vancouver)"},
    {"id": 11, "home_team": "Bosnia and Herzegovina", "away_team": "Qatar", "group": "B", "date": "2026-06-24", "time": "19:00", "venue": "Gillette Stadium (Boston)"},
    {"id": 12, "home_team": "Canada", "away_team": "Switzerland", "group": "B", "date": "2026-06-24", "time": "19:00", "venue": "BC Place (Vancouver)"},
    # Group C
    {"id": 13, "home_team": "Brazil", "away_team": "Morocco", "group": "C", "date": "2026-06-13", "time": "18:00", "venue": "Hard Rock Stadium (Miami)"},
    {"id": 14, "home_team": "Haiti", "away_team": "Scotland", "group": "C", "date": "2026-06-13", "time": "21:00", "venue": "NRG Stadium (Houston)"},
    {"id": 15, "home_team": "Brazil", "away_team": "Scotland", "group": "C", "date": "2026-06-19", "time": "18:00", "venue": "Lincoln Financial Field (Philadelphia)"},
    {"id": 16, "home_team": "Morocco", "away_team": "Haiti", "group": "C", "date": "2026-06-19", "time": "21:00", "venue": "Gillette Stadium (Boston)"},
    {"id": 17, "home_team": "Brazil", "away_team": "Haiti", "group": "C", "date": "2026-06-25", "time": "19:00", "venue": "Rose Bowl (Los Angeles)"},
    {"id": 18, "home_team": "Morocco", "away_team": "Scotland", "group": "C", "date": "2026-06-25", "time": "19:00", "venue": "Mercedes-Benz Stadium (Atlanta)"},
    # Group D
    {"id": 19, "home_team": "United States", "away_team": "Paraguay", "group": "D", "date": "2026-06-12", "time": "15:00", "venue": "Lumen Field (Seattle)", "home_score": 4, "away_score": 1},
    {"id": 20, "home_team": "Türkiye", "away_team": "Australia", "group": "D", "date": "2026-06-14", "time": "21:00", "venue": "Empower Field (Denver)"},
    {"id": 21, "home_team": "United States", "away_team": "Türkiye", "group": "D", "date": "2026-06-19", "time": "15:00", "venue": "MetLife Stadium (East Rutherford)"},
    {"id": 22, "home_team": "Australia", "away_team": "Paraguay", "group": "D", "date": "2026-06-19", "time": "21:00", "venue": "Levi's Stadium (Santa Clara)"},
    {"id": 23, "home_team": "United States", "away_team": "Australia", "group": "D", "date": "2026-06-25", "time": "19:00", "venue": "SoFi Stadium (Los Angeles)"},
    {"id": 24, "home_team": "Paraguay", "away_team": "Türkiye", "group": "D", "date": "2026-06-25", "time": "19:00", "venue": "Rose Bowl (Los Angeles)"},
    # Group E
    {"id": 25, "home_team": "Germany", "away_team": "Curaçao", "group": "E", "date": "2026-06-14", "time": "13:00", "venue": "NRG Stadium (Houston)"},
    {"id": 26, "home_team": "Ivory Coast", "away_team": "Ecuador", "group": "E", "date": "2026-06-14", "time": "19:00", "venue": "Lincoln Financial Field (Philadelphia)"},
    {"id": 27, "home_team": "Germany", "away_team": "Ivory Coast", "group": "E", "date": "2026-06-20", "time": "16:00", "venue": "BMO Field (Toronto)"},
    {"id": 28, "home_team": "Ecuador", "away_team": "Curaçao", "group": "E", "date": "2026-06-20", "time": "20:00", "venue": "Arrowhead Stadium (Kansas City)"},
    {"id": 29, "home_team": "Ecuador", "away_team": "Germany", "group": "E", "date": "2026-06-25", "time": "16:00", "venue": "MetLife Stadium (East Rutherford)"},
    {"id": 30, "home_team": "Curaçao", "away_team": "Ivory Coast", "group": "E", "date": "2026-06-25", "time": "16:00", "venue": "Lincoln Financial Field (Philadelphia)"},
    # Group F
    {"id": 31, "home_team": "Netherlands", "away_team": "Japan", "group": "F", "date": "2026-06-14", "time": "16:00", "venue": "AT&T Stadium (Arlington)"},
    {"id": 32, "home_team": "Sweden", "away_team": "Tunisia", "group": "F", "date": "2026-06-14", "time": "22:00", "venue": "Estadio Akron (Guadalajara)"},
    {"id": 33, "home_team": "Netherlands", "away_team": "Sweden", "group": "F", "date": "2026-06-20", "time": "13:00", "venue": "NRG Stadium (Houston)"},
    {"id": 34, "home_team": "Tunisia", "away_team": "Japan", "group": "F", "date": "2026-06-20", "time": "22:00", "venue": "Estadio Akron (Guadalajara)"},
    {"id": 35, "home_team": "Japan", "away_team": "Sweden", "group": "F", "date": "2026-06-25", "time": "19:00", "venue": "AT&T Stadium (Arlington)"},
    {"id": 36, "home_team": "Tunisia", "away_team": "Netherlands", "group": "F", "date": "2026-06-25", "time": "19:00", "venue": "Arrowhead Stadium (Kansas City)"},
    # Group G
    {"id": 37, "home_team": "Belgium", "away_team": "Egypt", "group": "G", "date": "2026-06-15", "time": "18:00", "venue": "Lumen Field (Seattle)"},
    {"id": 38, "home_team": "Iran", "away_team": "New Zealand", "group": "G", "date": "2026-06-16", "time": "00:00", "venue": "SoFi Stadium (Los Angeles)"},
    {"id": 39, "home_team": "Belgium", "away_team": "Iran", "group": "G", "date": "2026-06-21", "time": "15:00", "venue": "AT&T Stadium (Arlington)"},
    {"id": 40, "home_team": "Egypt", "away_team": "New Zealand", "group": "G", "date": "2026-06-21", "time": "15:00", "venue": "Empower Field (Denver)"},
    {"id": 41, "home_team": "New Zealand", "away_team": "Belgium", "group": "G", "date": "2026-06-26", "time": "19:00", "venue": "Levi's Stadium (Santa Clara)"},
    {"id": 42, "home_team": "Egypt", "away_team": "Iran", "group": "G", "date": "2026-06-26", "time": "19:00", "venue": "Mercedes-Benz Stadium (Atlanta)"},
    # Group H
    {"id": 43, "home_team": "Spain", "away_team": "Cape Verde", "group": "H", "date": "2026-06-15", "time": "13:00", "venue": "Mercedes-Benz Stadium (Atlanta)"},
    {"id": 44, "home_team": "Saudi Arabia", "away_team": "Uruguay", "group": "H", "date": "2026-06-15", "time": "18:00", "venue": "Hard Rock Stadium (Miami)"},
    {"id": 45, "home_team": "Spain", "away_team": "Saudi Arabia", "group": "H", "date": "2026-06-21", "time": "16:00", "venue": "Hard Rock Stadium (Miami)"},
    {"id": 46, "home_team": "Uruguay", "away_team": "Cape Verde", "group": "H", "date": "2026-06-21", "time": "16:00", "venue": "NRG Stadium (Houston)"},
    {"id": 47, "home_team": "Uruguay", "away_team": "Spain", "group": "H", "date": "2026-06-26", "time": "19:00", "venue": "MetLife Stadium (East Rutherford)"},
    {"id": 48, "home_team": "Cape Verde", "away_team": "Saudi Arabia", "group": "H", "date": "2026-06-26", "time": "19:00", "venue": "Lincoln Financial Field (Philadelphia)"},
    # Group I
    {"id": 49, "home_team": "France", "away_team": "Senegal", "group": "I", "date": "2026-06-16", "time": "15:00", "venue": "MetLife Stadium (East Rutherford)"},
    {"id": 50, "home_team": "Iraq", "away_team": "Norway", "group": "I", "date": "2026-06-16", "time": "18:00", "venue": "Gillette Stadium (Boston)"},
    {"id": 51, "home_team": "France", "away_team": "Norway", "group": "I", "date": "2026-06-22", "time": "15:00", "venue": "Rose Bowl (Los Angeles)"},
    {"id": 52, "home_team": "Senegal", "away_team": "Iraq", "group": "I", "date": "2026-06-22", "time": "15:00", "venue": "Arrowhead Stadium (Kansas City)"},
    {"id": 53, "home_team": "Norway", "away_team": "Senegal", "group": "I", "date": "2026-06-26", "time": "16:00", "venue": "Lumen Field (Seattle)"},
    {"id": 54, "home_team": "Iraq", "away_team": "France", "group": "I", "date": "2026-06-26", "time": "16:00", "venue": "Empower Field (Denver)"},
    # Group J
    {"id": 55, "home_team": "Algeria", "away_team": "Jordan", "group": "J", "date": "2026-06-17", "time": "13:00", "venue": "Levi's Stadium (Santa Clara)"},
    {"id": 56, "home_team": "Argentina", "away_team": "Austria", "group": "J", "date": "2026-06-17", "time": "19:00", "venue": "MetLife Stadium (East Rutherford)"},
    {"id": 57, "home_team": "Argentina", "away_team": "Algeria", "group": "J", "date": "2026-06-22", "time": "18:00", "venue": "SoFi Stadium (Los Angeles)"},
    {"id": 58, "home_team": "Austria", "away_team": "Jordan", "group": "J", "date": "2026-06-22", "time": "18:00", "venue": "Rose Bowl (Los Angeles)"},
    {"id": 59, "home_team": "Jordan", "away_team": "Argentina", "group": "J", "date": "2026-06-27", "time": "19:00", "venue": "AT&T Stadium (Arlington)"},
    {"id": 60, "home_team": "Austria", "away_team": "Algeria", "group": "J", "date": "2026-06-27", "time": "19:00", "venue": "Lumen Field (Seattle)"},
    # Group K
    {"id": 61, "home_team": "Portugal", "away_team": "DR Congo", "group": "K", "date": "2026-06-17", "time": "13:00", "venue": "NRG Stadium (Houston)"},
    {"id": 62, "home_team": "Uzbekistan", "away_team": "Colombia", "group": "K", "date": "2026-06-17", "time": "22:00", "venue": "Estadio Azteca (Ciudad de México)"},
    {"id": 63, "home_team": "Portugal", "away_team": "Uzbekistan", "group": "K", "date": "2026-06-22", "time": "21:00", "venue": "Hard Rock Stadium (Miami)"},
    {"id": 64, "home_team": "DR Congo", "away_team": "Colombia", "group": "K", "date": "2026-06-22", "time": "21:00", "venue": "BMO Field (Toronto)"},
    {"id": 65, "home_team": "Colombia", "away_team": "Portugal", "group": "K", "date": "2026-06-27", "time": "16:00", "venue": "MetLife Stadium (East Rutherford)"},
    {"id": 66, "home_team": "Uzbekistan", "away_team": "DR Congo", "group": "K", "date": "2026-06-27", "time": "16:00", "venue": "BC Place (Vancouver)"},
    # Group L
    {"id": 67, "home_team": "England", "away_team": "Panama", "group": "L", "date": "2026-06-16", "time": "21:00", "venue": "SoFi Stadium (Los Angeles)"},
    {"id": 68, "home_team": "Croatia", "away_team": "Ghana", "group": "L", "date": "2026-06-16", "time": "18:00", "venue": "BC Place (Vancouver)"},
    {"id": 69, "home_team": "England", "away_team": "Croatia", "group": "L", "date": "2026-06-21", "time": "21:00", "venue": "AT&T Stadium (Arlington)"},
    {"id": 70, "home_team": "Panama", "away_team": "Ghana", "group": "L", "date": "2026-06-21", "time": "21:00", "venue": "Empower Field (Denver)"},
    {"id": 71, "home_team": "Ghana", "away_team": "England", "group": "L", "date": "2026-06-26", "time": "21:00", "venue": "Gillette Stadium (Boston)"},
    {"id": 72, "home_team": "Croatia", "away_team": "Panama", "group": "L", "date": "2026-06-26", "time": "21:00", "venue": "Hard Rock Stadium (Miami)"},
]

# ── KNOCKOUT BRACKET STRUCTURE ────────────────────────────────────────────────
# Round of 32: top 2 from each group (24 teams) + 8 best 3rd-place teams = 32
# Bracket defined by FIFA with specific group winner vs runner-up pairings
KNOCKOUT_BRACKET = {
    "round_of_32": [
        {"match": 73, "slot1": "1A", "slot2": "2B", "date": "2026-06-28", "venue": "MetLife Stadium (East Rutherford)"},
        {"match": 74, "slot1": "1C", "slot2": "2D", "date": "2026-06-28", "venue": "SoFi Stadium (Los Angeles)"},
        {"match": 75, "slot1": "1B", "slot2": "2A", "date": "2026-06-29", "venue": "BC Place (Vancouver)"},
        {"match": 76, "slot1": "1D", "slot2": "2C", "date": "2026-06-29", "venue": "Rose Bowl (Los Angeles)"},
        {"match": 77, "slot1": "1E", "slot2": "2F", "date": "2026-06-30", "venue": "AT&T Stadium (Arlington)"},
        {"match": 78, "slot1": "1G", "slot2": "2H", "date": "2026-06-30", "venue": "Mercedes-Benz Stadium (Atlanta)"},
        {"match": 79, "slot1": "1F", "slot2": "2E", "date": "2026-07-01", "venue": "Hard Rock Stadium (Miami)"},
        {"match": 80, "slot1": "1H", "slot2": "2G", "date": "2026-07-01", "venue": "Levi's Stadium (Santa Clara)"},
        {"match": 81, "slot1": "1I", "slot2": "2J", "date": "2026-07-02", "venue": "NRG Stadium (Houston)"},
        {"match": 82, "slot1": "1K", "slot2": "2L", "date": "2026-07-02", "venue": "Gillette Stadium (Boston)"},
        {"match": 83, "slot1": "1J", "slot2": "2I", "date": "2026-07-03", "venue": "Lincoln Financial Field (Philadelphia)"},
        {"match": 84, "slot1": "1L", "slot2": "2K", "date": "2026-07-03", "venue": "Arrowhead Stadium (Kansas City)"},
        # 8 slots for best 3rd-place teams (depends on group results)
        {"match": 85, "slot1": "3rd_best_1", "slot2": "TBD_winner", "date": "2026-07-04", "venue": "MetLife Stadium (East Rutherford)", "wildcard": True},
        {"match": 86, "slot1": "3rd_best_2", "slot2": "TBD_winner", "date": "2026-07-04", "venue": "Rose Bowl (Los Angeles)", "wildcard": True},
        {"match": 87, "slot1": "3rd_best_3", "slot2": "TBD_winner", "date": "2026-07-05", "venue": "Hard Rock Stadium (Miami)", "wildcard": True},
        {"match": 88, "slot1": "3rd_best_4", "slot2": "TBD_winner", "date": "2026-07-05", "venue": "Levi's Stadium (Santa Clara)", "wildcard": True},
        {"match": 89, "slot1": "3rd_best_5", "slot2": "TBD_winner", "date": "2026-07-06", "venue": "AT&T Stadium (Arlington)", "wildcard": True},
        {"match": 90, "slot1": "3rd_best_6", "slot2": "TBD_winner", "date": "2026-07-06", "venue": "NRG Stadium (Houston)", "wildcard": True},
        {"match": 91, "slot1": "3rd_best_7", "slot2": "TBD_winner", "date": "2026-07-07", "venue": "BC Place (Vancouver)", "wildcard": True},
        {"match": 92, "slot1": "3rd_best_8", "slot2": "TBD_winner", "date": "2026-07-07", "venue": "Empower Field (Denver)", "wildcard": True},
    ],
    "round_of_16": [
        {"match": 93, "feeds_from": [73, 74], "date": "2026-07-08", "venue": "MetLife Stadium (East Rutherford)"},
        {"match": 94, "feeds_from": [75, 76], "date": "2026-07-08", "venue": "BC Place (Vancouver)"},
        {"match": 95, "feeds_from": [77, 78], "date": "2026-07-09", "venue": "AT&T Stadium (Arlington)"},
        {"match": 96, "feeds_from": [79, 80], "date": "2026-07-09", "venue": "Hard Rock Stadium (Miami)"},
        {"match": 97, "feeds_from": [81, 82], "date": "2026-07-10", "venue": "NRG Stadium (Houston)"},
        {"match": 98, "feeds_from": [83, 84], "date": "2026-07-10", "venue": "Levi's Stadium (Santa Clara)"},
        {"match": 99, "feeds_from": [85, 86], "date": "2026-07-11", "venue": "Rose Bowl (Los Angeles)"},
        {"match": 100, "feeds_from": [87, 88], "date": "2026-07-11", "venue": "Mercedes-Benz Stadium (Atlanta)"},
    ],
    "quarterfinals": [
        {"match": 101, "feeds_from": [93, 94], "date": "2026-07-13", "venue": "MetLife Stadium (East Rutherford)"},
        {"match": 102, "feeds_from": [95, 96], "date": "2026-07-13", "venue": "AT&T Stadium (Arlington)"},
        {"match": 103, "feeds_from": [97, 98], "date": "2026-07-14", "venue": "SoFi Stadium (Los Angeles)"},
        {"match": 104, "feeds_from": [99, 100], "date": "2026-07-14", "venue": "Hard Rock Stadium (Miami)"},
    ],
    "semifinals": [
        {"match": 105, "feeds_from": [101, 102], "date": "2026-07-17", "venue": "MetLife Stadium (East Rutherford)"},
        {"match": 106, "feeds_from": [103, 104], "date": "2026-07-18", "venue": "Rose Bowl (Los Angeles)"},
    ],
    "third_place": {"match": 107, "feeds_from": [105, 106], "date": "2026-07-19", "venue": "AT&T Stadium (Arlington)"},
    "final": {"match": 108, "feeds_from": [105, 106], "date": "2026-07-19", "venue": "MetLife Stadium (East Rutherford)"},
}

GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]


def get_team(name: str) -> Dict[str, Any]:
    for team in TEAMS:
        if team["name"].lower() == name.lower():
            return team
    return None


def get_match(match_id: int) -> Dict[str, Any]:
    for match in MATCHES:
        if match["id"] == match_id:
            return match
    return None


def get_teams_by_group(group: str) -> List[Dict[str, Any]]:
    return [t for t in TEAMS if t["group"] == group.upper()]


def get_matches_by_group(group: str) -> List[Dict[str, Any]]:
    return [m for m in MATCHES if m["group"] == group.upper()]
