import random

random.seed(42)  # Ensure reproducibility of stats across imports

_clubs = {
    "Bayer Leverkusen": [
        ("Lukas Hradecky", "GK", 35), ("Matej Kovar", "GK", 24),
        ("Jonathan Tah", "CB", 28), ("Edmond Tapsoba", "CB", 25), ("Piero Hincapie", "CB", 22), ("Odilon Kossounou", "CB", 23),
        ("Jeremie Frimpong", "FB", 24), ("Alejandro Grimaldo", "FB", 29), ("Arthur", "FB", 21),
        ("Granit Xhaka", "CM", 32), ("Exequiel Palacios", "CM", 26), ("Robert Andrich", "CM", 30), ("Aleix Garcia", "CM", 27),
        ("Florian Wirtz", "W", 21), ("Jonas Hofmann", "W", 32), ("Amine Adli", "W", 24), ("Nathan Tella", "W", 25),
        ("Victor Boniface", "ST", 24), ("Patrik Schick", "ST", 28)
    ],
    "Bayern Munich": [
        ("Manuel Neuer", "GK", 38), ("Sven Ulreich", "GK", 36),
        ("Dayot Upamecano", "CB", 26), ("Kim Min-jae", "CB", 28), ("Eric Dier", "CB", 30), ("Hiroki Ito", "CB", 25),
        ("Alphonso Davies", "FB", 24), ("Raphael Guerreiro", "FB", 31), ("Sacha Boey", "FB", 24), ("Josip Stanisic", "FB", 24),
        ("Joshua Kimmich", "CM", 29), ("Leon Goretzka", "CM", 29), ("Konrad Laimer", "CM", 27), ("Aleksandar Pavlovic", "CM", 20), ("Joao Palhinha", "CM", 29),
        ("Jamal Musiala", "W", 21), ("Leroy Sane", "W", 28), ("Serge Gnabry", "W", 29), ("Kingsley Coman", "W", 28), ("Michael Olise", "W", 23),
        ("Harry Kane", "ST", 31), ("Mathys Tel", "ST", 19), ("Thomas Muller", "W", 35)
    ],
    "VfB Stuttgart": [
        ("Alexander Nübel", "GK", 28), ("Fabian Bredlow", "GK", 29),
        ("Jeff Chabot", "CB", 26), ("Anthony Rouault", "CB", 23), ("Dan-Axel Zagadou", "CB", 25), ("Leonidas Stergiou", "CB", 22),
        ("Maximilian Mittelstädt", "FB", 27), ("Josha Vagnoman", "FB", 24), ("Pascal Stenzel", "FB", 28),
        ("Angelo Stiller", "CM", 23), ("Atakan Karazor", "CM", 28), ("Enzo Millot", "CM", 22), ("Fabian Rieder", "CM", 22),
        ("Chris Führich", "W", 26), ("Jamie Leweling", "W", 23), ("Justin Diehl", "W", 20),
        ("Deniz Undav", "ST", 28), ("Ermedin Demirovic", "ST", 26), ("El Bilal Toure", "ST", 23)
    ],
    "RB Leipzig": [
        ("Peter Gulacsi", "GK", 34), ("Maarten Vandevoordt", "GK", 22),
        ("Willi Orban", "CB", 32), ("Castello Lukeba", "CB", 22), ("Lutsharel Geertruida", "CB", 24), ("El Chadaille Bitshiabu", "CB", 19),
        ("David Raum", "FB", 26), ("Benjamin Henrichs", "FB", 27),
        ("Amadou Haidara", "CM", 26), ("Kevin Kampl", "CM", 34), ("Nicolas Seiwald", "CM", 23), ("Xaver Schlager", "CM", 27), ("Arthur Vermeeren", "CM", 19),
        ("Xavi Simons", "W", 21), ("Christoph Baumgartner", "W", 25), ("Antonio Nusa", "W", 19),
        ("Lois Openda", "ST", 24), ("Benjamin Sesko", "ST", 21), ("Yussuf Poulsen", "ST", 30)
    ],
    "Borussia Dortmund": [
        ("Gregor Kobel", "GK", 27), ("Alexander Meyer", "GK", 33),
        ("Nico Schlotterbeck", "CB", 25), ("Waldemar Anton", "CB", 28), ("Niklas Süle", "CB", 29),
        ("Julian Ryerson", "FB", 27), ("Yan Couto", "FB", 22), ("Ramy Bensebaini", "FB", 29),
        ("Emre Can", "CM", 30), ("Pascal Gross", "CM", 33), ("Marcel Sabitzer", "CM", 30), ("Felix Nmecha", "CM", 24),
        ("Julian Brandt", "W", 28), ("Karim Adeyemi", "W", 23), ("Donyell Malen", "W", 25), ("Jamie Gittens", "W", 20), ("Gio Reyna", "W", 22),
        ("Serhou Guirassy", "ST", 28), ("Maximilian Beier", "ST", 22)
    ],
    "Eintracht Frankfurt": [
        ("Kevin Trapp", "GK", 34), ("Kaua Santos", "GK", 21),
        ("Robin Koch", "CB", 28), ("Tuta", "CB", 25), ("Arthur Theate", "CB", 24), ("Aurele Amenda", "CB", 21),
        ("Rasmus Kristensen", "FB", 27), ("Niels Nkounkou", "FB", 24), ("Timothy Chandler", "FB", 34),
        ("Ellyes Skhiri", "CM", 29), ("Hugo Larsson", "CM", 20), ("Mario Götze", "CM", 32), ("Mahmoud Dahoud", "CM", 28),
        ("Fares Chaibi", "W", 22), ("Ansgar Knauff", "W", 22), ("Eric Junior Dina Ebimbe", "W", 24),
        ("Omar Marmoush", "ST", 25), ("Hugo Ekitike", "ST", 22), ("Igor Matanovic", "ST", 21)
    ],
    "Hoffenheim": [
        ("Oliver Baumann", "GK", 34), ("Luca Philipp", "GK", 24),
        ("Ozan Kabak", "CB", 24), ("Kevin Akpoguma", "CB", 29), ("Stanley Nsoki", "CB", 25), ("Anton Stach", "CB", 26),
        ("Pavel Kaderabek", "FB", 32), ("Alexander Prass", "FB", 23), ("Valentin Gendrey", "FB", 24),
        ("Florian Grillitsch", "CM", 29), ("Grischa Prömel", "CM", 29), ("Dennis Geiger", "CM", 26), ("Tom Bischof", "CM", 19),
        ("Andrej Kramaric", "W", 33), ("Marius Bülter", "W", 31), ("Jacob Bruun Larsen", "W", 26),
        ("Ihlas Bebou", "ST", 30), ("Adam Hlozek", "ST", 22), ("Haris Tabakovic", "ST", 30), ("Max Moerstedt", "ST", 18)
    ],
    "Heidenheim": [
        ("Kevin Müller", "GK", 33), ("Frank Feller", "GK", 21),
        ("Patrick Mainka", "CB", 30), ("Benedikt Gimber", "CB", 27), ("Tim Siersleben", "CB", 24),
        ("Jonas Föhrenbach", "FB", 29), ("Marnon Busch", "FB", 30), ("Omar Traore", "FB", 26),
        ("Lennard Maloney", "CM", 25), ("Jan Schöppner", "CM", 25), ("Norman Theuerkauf", "CM", 37), ("Luka Janes", "CM", 21),
        ("Paul Wanner", "W", 19), ("Leo Scienza", "W", 26), ("Adrian Beck", "W", 27), ("Sirlord Conteh", "W", 28),
        ("Marvin Pieringer", "ST", 25), ("Mikkel Kaufmann", "ST", 23), ("Maximilian Breunig", "ST", 24)
    ],
    "Werder Bremen": [
        ("Michael Zetterer", "GK", 29), ("Mio Backhaus", "GK", 20),
        ("Marco Friedl", "CB", 26), ("Niklas Stark", "CB", 29), ("Milos Veljkovic", "CB", 29), ("Anthony Jung", "CB", 33),
        ("Mitchell Weiser", "FB", 30), ("Felix Agu", "FB", 25), ("Derrick Köhn", "FB", 26),
        ("Senne Lynen", "CM", 25), ("Jens Stage", "CM", 28), ("Romano Schmid", "CM", 25), ("Leonardo Bittencourt", "CM", 31),
        ("Marco Grüll", "W", 26), ("Justin Njinmah", "W", 24), ("Olivier Deman", "W", 24),
        ("Marvin Ducksch", "ST", 30), ("Keke Topp", "ST", 20)
    ],
    "SC Freiburg": [
        ("Noah Atubolu", "GK", 22), ("Florian Müller", "GK", 27),
        ("Matthias Ginter", "CB", 31), ("Philipp Lienhart", "CB", 28), ("Max Rosenfelder", "CB", 21), ("Kenneth Schmidt", "CB", 22),
        ("Christian Günter", "FB", 31), ("Lukas Kübler", "FB", 32), ("Jordy Makengo", "FB", 23),
        ("Maximilian Eggestein", "CM", 28), ("Nicolas Höfler", "CM", 34), ("Patrick Osterhage", "CM", 25), ("Merlin Röhl", "CM", 22),
        ("Vincenzo Grifo", "W", 31), ("Ritsu Doan", "W", 26), ("Noah Weißhaupt", "W", 23), ("Eren Dinkci", "W", 23),
        ("Michael Gregoritsch", "ST", 30), ("Chukwubuike Adamu", "ST", 23), ("Lucas Höler", "ST", 30)
    ],
    "FC Augsburg": [
        ("Finn Dahmen", "GK", 26), ("Nediljko Labrovic", "GK", 25),
        ("Jeffrey Gouweleeuw", "CB", 33), ("Keven Schlotterbeck", "CB", 27), ("Reece Oxford", "CB", 26), ("Maximilian Bauer", "CB", 24),
        ("Dimitrios Giannoulis", "FB", 29), ("Mads Pedersen", "FB", 28), ("Marius Wolf", "FB", 29),
        ("Elvis Rexhbecaj", "CM", 27), ("Arne Maier", "CM", 26), ("Kristijan Jakic", "CM", 27), ("Frank Onyeka", "CM", 27),
        ("Ruben Vargas", "W", 26), ("Fredrik Jensen", "W", 27), ("Alexis Claude-Maurice", "W", 26),
        ("Phillip Tietz", "ST", 27), ("Samuel Essende", "ST", 27), ("Steve Mounie", "ST", 30)
    ],
    "VfL Wolfsburg": [
        ("Kamil Grabara", "GK", 26), ("Pavao Pervan", "GK", 37),
        ("Cedric Zesiger", "CB", 26), ("Sebastiaan Bornauw", "CB", 25), ("Konstantinos Koulierakis", "CB", 21), ("Denis Vavro", "CB", 28),
        ("Joakim Maehle", "FB", 27), ("Ridle Baku", "FB", 26), ("Kilian Fischer", "FB", 24),
        ("Maximilian Arnold", "CM", 30), ("Mattias Svanberg", "CM", 26), ("Lovro Majer", "CM", 27), ("Aster Vranckx", "CM", 22),
        ("Patrick Wimmer", "W", 23), ("Jakub Kaminski", "W", 22), ("Tiago Tomas", "W", 22), ("Salih Özcan", "CM", 27),
        ("Jonas Wind", "ST", 26), ("Mohamed Amoura", "ST", 24), ("Kevin Behrens", "ST", 34)
    ],
    "Borussia Monchengladbach": [
        ("Jonas Omlin", "GK", 31), ("Moritz Nicolas", "GK", 27),
        ("Ko Itakura", "CB", 28), ("Nico Elvedi", "CB", 28), ("Marvin Friedrich", "CB", 29), ("Fabio Chiarodia", "CB", 19),
        ("Luca Netz", "FB", 21), ("Joe Scally", "FB", 22), ("Stefan Lainer", "FB", 32),
        ("Julian Weigl", "CM", 29), ("Rocco Reitz", "CM", 22), ("Philipp Sander", "CM", 26), ("Florian Neuhaus", "CM", 27),
        ("Franck Honorat", "W", 28), ("Robin Hack", "W", 26), ("Nathan Ngoumou", "W", 24), ("Kevin Stöger", "W", 31),
        ("Alassane Plea", "ST", 31), ("Tim Kleindienst", "ST", 29), ("Tomas Cvancara", "ST", 24)
    ],
    "Union Berlin": [
        ("Frederik Rønnow", "GK", 32), ("Alexander Schwolow", "GK", 32),
        ("Kevin Vogt", "CB", 33), ("Danilho Doekhi", "CB", 26), ("Diogo Leite", "CB", 26), ("Leopold Querfeld", "CB", 21),
        ("Christopher Trimmel", "FB", 38), ("Josip Juranovic", "FB", 29), ("Tom Rothe", "FB", 20), ("Jerome Roussillon", "FB", 32),
        ("Rani Khedira", "CM", 31), ("Lucas Tousart", "CM", 27), ("Andras Schäfer", "CM", 25), ("Janik Haberer", "CM", 30),
        ("Benedict Hollerbach", "W", 23), ("Woo-yeong Jeong", "W", 25), ("Tim Skarke", "W", 28),
        ("Kevin Volland", "ST", 32), ("Jordan Siebatcheu", "ST", 28), ("Yorbe Vertessen", "ST", 24)
    ],
    "VfL Bochum": [
        ("Patrick Drewes", "GK", 32), ("Manuel Riemann", "GK", 36),
        ("Ivan Ordets", "CB", 32), ("Erhan Masovic", "CB", 26), ("Tim Oermann", "CB", 21), ("Jakov Medic", "CB", 26),
        ("Maximilian Wittek", "FB", 29), ("Felix Passlack", "FB", 26), ("Cristian Gamboa", "FB", 35),
        ("Anthony Losilla", "CM", 38), ("Matus Bero", "CM", 29), ("Lukas Daschner", "CM", 26), ("Ibrahima Sissoko", "CM", 27),
        ("Philipp Hofmann", "ST", 31), ("Moritz Broschinski", "ST", 24), ("Gerrit Holtmann", "W", 29), ("Koji Miyoshi", "W", 27),
        ("Aliou Balde", "W", 22), ("Dani de Wit", "CM", 26), ("Myron Boadu", "ST", 24)
    ],
    "FC St. Pauli": [
        ("Nikola Vasilj", "GK", 29), ("Sascha Burchert", "GK", 35),
        ("Eric Smith", "CB", 28), ("Karol Mets", "CB", 32), ("Hauke Wahl", "CB", 30), ("David Nemeth", "CB", 23),
        ("Philipp Treu", "FB", 24), ("Manolis Saliakas", "FB", 28), ("Fin Stevens", "FB", 21),
        ("Jackson Irvine", "CM", 31), ("Carlo Boukhalfa", "CM", 25), ("Connor Metcalfe", "CM", 25), ("Robert Wagner", "CM", 21),
        ("Oladapo Afolayan", "W", 27), ("Elias Saad", "W", 25), ("Danel Sinani", "W", 27),
        ("Johannes Eggestein", "ST", 26), ("Morgan Guilavogui", "ST", 26), ("Andreas Albers", "ST", 34)
    ],
    "Holstein Kiel": [
        ("Timon Weiner", "GK", 26), ("Thomas Dähne", "GK", 30),
        ("Patrick Erras", "CB", 30), ("Carl Johansson", "CB", 30), ("Colin Kleine-Bekel", "CB", 22), ("Marco Komenda", "CB", 28),
        ("Timo Becker", "FB", 27), ("Tymoteusz Puchacz", "FB", 26), ("Lasse Rosenboom", "FB", 23),
        ("Magnus Knudsen", "CM", 23), ("Lewis Holtby", "CM", 34), ("Nicolai Remberg", "CM", 24), ("Armin Gigovic", "CM", 22),
        ("Finn Porath", "W", 28), ("Steven Skrzybski", "W", 32), ("Alexander Bernhardsson", "W", 26),
        ("Shuto Machino", "ST", 25), ("Benedikt Pichler", "ST", 27), ("Fiete Arp", "ST", 25)
    ],
    "Mainz 05": [
        ("Robin Zentner", "GK", 30), ("Daniel Batz", "GK", 34),
        ("Stefan Bell", "CB", 33), ("Dominik Kohr", "CB", 31), ("Maxim Leitsch", "CB", 26), ("Moritz Jenz", "CB", 25),
        ("Anthony Caci", "FB", 27), ("Phillipp Mwene", "FB", 31), ("Silvan Widmer", "FB", 32),
        ("Nadiem Amiri", "CM", 28), ("Kaishu Sano", "CM", 24), ("Jae-sung Lee", "CM", 32), ("Hyun-seok Hong", "CM", 25),
        ("Jonathan Burkardt", "ST", 24), ("Armindo Sieb", "ST", 22), ("Nelson Weiper", "ST", 19),
        ("Karim Onisiwo", "ST", 32), ("Paul Nebel", "W", 22), ("Gabriel Vidovic", "W", 21)
    ]
}

def _generate_stats(pos):
    if pos == "GK":
        return {
            "psxg_net_per90": round(random.uniform(-0.3, 0.4), 2),
            "save_pct": round(random.uniform(60.0, 80.0), 1),
            "pass_completion_pct": round(random.uniform(65.0, 85.0), 1),
            "passes_completed_long_pct": round(random.uniform(30.0, 55.0), 1),
            "def_actions_outside_pen_per90": round(random.uniform(0.5, 2.5), 2),
            "crosses_stopped_pct": round(random.uniform(3.0, 12.0), 1),
            "avg_dist_def_actions": round(random.uniform(12.0, 18.0), 1)
        }
    elif pos == "CB":
        return {
            "pass_completion_pct": round(random.uniform(75.0, 92.0), 1),
            "progressive_passes_per90": round(random.uniform(2.0, 6.0), 2),
            "progressive_passing_distance_per90": round(random.uniform(200, 450), 1),
            "passes_into_final_third_per90": round(random.uniform(1.5, 6.0), 2),
            "progressive_carries_per90": round(random.uniform(0.5, 2.0), 2),
            "take_on_success_pct": round(random.uniform(50.0, 80.0), 1),
            "padj_tackles_per90": round(random.uniform(1.0, 3.0), 2),
            "padj_interceptions_per90": round(random.uniform(1.0, 2.5), 2),
            "ball_recoveries_per90": round(random.uniform(4.0, 7.5), 2),
            "blocks_per90": round(random.uniform(1.0, 2.5), 2),
            "aerial_win_pct": round(random.uniform(55.0, 75.0), 1),
            "tackle_win_pct": round(random.uniform(60.0, 80.0), 1)
        }
    elif pos == "FB":
        return {
            "xAG_per90": round(random.uniform(0.05, 0.25), 2),
            "sca_per90": round(random.uniform(1.5, 3.5), 2),
            "key_passes_per90": round(random.uniform(0.8, 2.2), 2),
            "passes_into_penalty_area_per90": round(random.uniform(0.5, 2.5), 2),
            "pass_completion_pct": round(random.uniform(70.0, 88.0), 1),
            "progressive_passes_per90": round(random.uniform(3.0, 7.0), 2),
            "progressive_carries_per90": round(random.uniform(1.5, 4.0), 2),
            "passes_into_final_third_per90": round(random.uniform(2.0, 5.0), 2),
            "take_ons_attempted_per90": round(random.uniform(1.0, 4.0), 2),
            "take_on_success_pct": round(random.uniform(40.0, 70.0), 1),
            "padj_tackles_per90": round(random.uniform(1.5, 3.5), 2),
            "padj_interceptions_per90": round(random.uniform(1.0, 2.5), 2),
            "ball_recoveries_per90": round(random.uniform(4.5, 7.5), 2),
            "tackles_att_3rd_per90": round(random.uniform(0.1, 0.6), 2),
            "aerial_win_pct": round(random.uniform(40.0, 65.0), 1)
        }
    elif pos == "CM":
        return {
            "npxG_per90": round(random.uniform(0.02, 0.15), 2),
            "xAG_per90": round(random.uniform(0.05, 0.25), 2),
            "sca_per90": round(random.uniform(1.5, 4.5), 2),
            "key_passes_per90": round(random.uniform(0.8, 2.5), 2),
            "passes_into_penalty_area_per90": round(random.uniform(0.5, 2.5), 2),
            "pass_completion_pct": round(random.uniform(75.0, 90.0), 1),
            "progressive_passes_per90": round(random.uniform(4.0, 9.0), 2),
            "progressive_carries_per90": round(random.uniform(1.0, 3.5), 2),
            "passes_into_final_third_per90": round(random.uniform(3.0, 7.0), 2),
            "take_on_success_pct": round(random.uniform(45.0, 75.0), 1),
            "padj_tackles_per90": round(random.uniform(1.5, 4.0), 2),
            "padj_interceptions_per90": round(random.uniform(1.0, 2.5), 2),
            "ball_recoveries_per90": round(random.uniform(5.0, 9.0), 2),
            "blocks_per90": round(random.uniform(0.8, 2.0), 2),
            "aerial_win_pct": round(random.uniform(40.0, 65.0), 1)
        }
    elif pos == "W":
        return {
            "npxG_per90": round(random.uniform(0.15, 0.45), 2),
            "xAG_per90": round(random.uniform(0.15, 0.35), 2),
            "sca_per90": round(random.uniform(2.5, 5.5), 2),
            "shots_total_per90": round(random.uniform(1.5, 3.5), 2),
            "touches_att_pen_per90": round(random.uniform(3.0, 7.0), 2),
            "take_ons_attempted_per90": round(random.uniform(3.0, 8.0), 2),
            "take_on_success_pct": round(random.uniform(40.0, 65.0), 1),
            "progressive_carries_per90": round(random.uniform(3.0, 7.0), 2),
            "progressive_passes_per90": round(random.uniform(2.0, 6.0), 2),
            "carries_into_penalty_area_per90": round(random.uniform(1.0, 3.5), 2),
            "key_passes_per90": round(random.uniform(1.0, 2.8), 2),
            "padj_tackles_per90": round(random.uniform(0.5, 2.5), 2),
            "padj_interceptions_per90": round(random.uniform(0.5, 1.5), 2),
            "ball_recoveries_per90": round(random.uniform(3.0, 6.0), 2),
            "tackles_att_3rd_per90": round(random.uniform(0.3, 1.2), 2)
        }
    elif pos == "ST":
        return {
            "npxG_per90": round(random.uniform(0.3, 0.8), 2),
            "shots_total_per90": round(random.uniform(2.5, 4.5), 2),
            "shots_on_target_pct": round(random.uniform(35.0, 55.0), 1),
            "touches_att_pen_per90": round(random.uniform(4.0, 8.0), 2),
            "aerial_win_pct": round(random.uniform(35.0, 60.0), 1),
            "xAG_per90": round(random.uniform(0.05, 0.25), 2),
            "sca_per90": round(random.uniform(1.5, 3.5), 2),
            "key_passes_per90": round(random.uniform(0.5, 2.0), 2),
            "pass_completion_pct": round(random.uniform(60.0, 80.0), 1),
            "carries_into_penalty_area_per90": round(random.uniform(0.5, 2.0), 2),
            "tackles_att_3rd_per90": round(random.uniform(0.2, 0.8), 2),
            "ball_recoveries_per90": round(random.uniform(1.5, 3.5), 2),
            "padj_tackles_per90": round(random.uniform(0.5, 1.5), 2)
        }

BUNDESLIGA_REAL_ROSTERS = {}
for club_name, players in _clubs.items():
    roster = []
    for (name, pos, age) in players:
        mins = random.randint(800, 3200)
        stats = _generate_stats(pos)
        roster.append((name, pos, age, mins, stats))
    BUNDESLIGA_REAL_ROSTERS[club_name] = roster
