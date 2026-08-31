import os
import random
import json
import textwrap

os.makedirs(r"c:\Users\sriji\OneDrive\Documents\kaaam\ScoutBench\scripts", exist_ok=True)
outfile = r"c:\Users\sriji\OneDrive\Documents\kaaam\ScoutBench\scripts\real_la_liga.py"

teams = {
    "Barcelona": [
        ("Marc-Andre ter Stegen", "GK", 32), ("Inaki Pena", "GK", 25),
        ("Ronald Araujo", "CB", 25), ("Andreas Christensen", "CB", 28), ("Pau Cubarsi", "CB", 17), ("Inigo Martinez", "CB", 33), ("Eric Garcia", "CB", 23),
        ("Alejandro Balde", "FB", 20), ("Jules Kounde", "FB", 25), ("Hector Fort", "FB", 18), ("Gerard Martin", "FB", 22),
        ("Pedri", "CM", 21), ("Gavi", "CM", 20), ("Frenkie de Jong", "CM", 27), ("Dani Olmo", "CM", 26), ("Fermin Lopez", "CM", 21), ("Marc Casado", "CM", 20), ("Marc Bernal", "CM", 17),
        ("Lamine Yamal", "W", 17), ("Raphinha", "W", 27), ("Ferran Torres", "W", 24), ("Ansu Fati", "W", 21),
        ("Robert Lewandowski", "ST", 36), ("Pau Victor", "ST", 22)
    ],
    "Real Madrid": [
        ("Thibaut Courtois", "GK", 32), ("Andriy Lunin", "GK", 25),
        ("Antonio Rudiger", "CB", 31), ("Eder Militao", "CB", 26), ("David Alaba", "CB", 32), ("Jesus Vallejo", "CB", 27),
        ("Dani Carvajal", "FB", 32), ("Ferland Mendy", "FB", 29), ("Fran Garcia", "FB", 25), ("Lucas Vazquez", "FB", 33),
        ("Jude Bellingham", "CM", 21), ("Federico Valverde", "CM", 26), ("Aurelien Tchouameni", "CM", 24), ("Eduardo Camavinga", "CM", 21), ("Luka Modric", "CM", 39), ("Dani Ceballos", "CM", 28), ("Arda Guler", "CM", 19),
        ("Vinicius Junior", "W", 24), ("Rodrygo", "W", 23), ("Brahim Diaz", "W", 25),
        ("Kylian Mbappe", "ST", 25), ("Endrick", "ST", 18)
    ],
    "Atletico Madrid": [
        ("Jan Oblak", "GK", 31), ("Juan Musso", "GK", 30),
        ("Jose Maria Gimenez", "CB", 29), ("Robin Le Normand", "CB", 27), ("Axel Witsel", "CB", 35), ("Cesar Azpilicueta", "CB", 35), ("Clement Lenglet", "CB", 29),
        ("Marcos Llorente", "FB", 29), ("Nahuel Molina", "FB", 26), ("Samuel Lino", "FB", 24), ("Rodrigo Riquelme", "FB", 24), ("Javi Galan", "FB", 29),
        ("Koke", "CM", 32), ("Rodrigo De Paul", "CM", 30), ("Conor Gallagher", "CM", 24), ("Pablo Barrios", "CM", 21), ("Thomas Lemar", "CM", 28),
        ("Antoine Griezmann", "W", 33), ("Angel Correa", "W", 29),
        ("Julian Alvarez", "ST", 24), ("Alexander Sorloth", "ST", 28), ("Giuliano Simeone", "ST", 21)
    ],
    "Girona": [
        ("Paulo Gazzaniga", "GK", 32), ("Pau Lopez", "GK", 29),
        ("David Lopez", "CB", 34), ("Daley Blind", "CB", 34), ("Alejandro Frances", "CB", 22), ("Ladislav Krejci", "CB", 25), ("Juanpe", "CB", 33),
        ("Arnau Martinez", "FB", 21), ("Miguel Gutierrez", "FB", 23), ("Francés", "FB", 22),
        ("Yangel Herrera", "CM", 26), ("Ivan Martin", "CM", 25), ("Oriol Romeu", "CM", 32), ("Donny van de Beek", "CM", 27), ("Jhon Solis", "CM", 19),
        ("Viktor Tsygankov", "W", 26), ("Bryan Gil", "W", 23), ("Portu", "W", 32), ("Arnaut Danjuma", "W", 27),
        ("Cristhian Stuani", "ST", 37), ("Abel Ruiz", "ST", 24), ("Bojan Miovski", "ST", 25)
    ],
    "Athletic Club": [
        ("Unai Simon", "GK", 27), ("Julen Agirrezabala", "GK", 23),
        ("Dani Vivian", "CB", 25), ("Aitor Paredes", "CB", 24), ("Yeray Alvarez", "CB", 29), ("Unai Nunez", "CB", 27),
        ("Oscar De Marcos", "FB", 35), ("Yuri Berchiche", "FB", 34), ("Inigo Lekue", "FB", 31), ("Andoni Gorosabel", "FB", 28),
        ("Oihan Sancet", "CM", 24), ("Inigo Ruiz de Galarreta", "CM", 31), ("Mikel Vesga", "CM", 31), ("Benat Prados", "CM", 23), ("Ander Herrera", "CM", 35), ("Mikel Jauregizar", "CM", 20),
        ("Nico Williams", "W", 22), ("Inaki Williams", "W", 30), ("Alex Berenguer", "W", 29), ("Alvaro Djalo", "W", 24),
        ("Gorka Guruzeta", "ST", 28), ("Javier Marton", "ST", 25)
    ],
    "Real Sociedad": [
        ("Alex Remiro", "GK", 29), ("Unai Marrero", "GK", 22),
        ("Igor Zubeldia", "CB", 27), ("Jon Pacheco", "CB", 23), ("Aritz Elustondo", "CB", 30), ("Nayef Aguerd", "CB", 28),
        ("Hamari Traore", "FB", 32), ("Javi Lopez", "FB", 22), ("Alvaro Odriozola", "FB", 28), ("Aihen Munoz", "FB", 27),
        ("Martin Zubimendi", "CM", 25), ("Brais Mendez", "CM", 27), ("Benat Turrientes", "CM", 22), ("Luka Sucic", "CM", 21), ("Arsen Zakharyan", "CM", 21), ("Urko Gonzalez", "CM", 23),
        ("Takefusa Kubo", "W", 23), ("Mikel Oyarzabal", "W", 27), ("Ander Barrenetxea", "W", 22), ("Sheraldo Becker", "W", 29),
        ("Umar Sadiq", "ST", 27), ("Orri Oskarsson", "ST", 20)
    ],
    "Real Betis": [
        ("Rui Silva", "GK", 30), ("Adrian", "GK", 37),
        ("Diego Llorente", "CB", 31), ("Marc Bartra", "CB", 33), ("Natan", "CB", 23), ("Nobel Mendy", "CB", 20),
        ("Hector Bellerin", "FB", 29), ("Romain Perraud", "FB", 26), ("Youssouf Sabaly", "FB", 31), ("Ricardo Rodriguez", "FB", 32),
        ("William Carvalho", "CM", 32), ("Marc Roca", "CM", 27), ("Johnny Cardoso", "CM", 22), ("Sergi Altimira", "CM", 23), ("Isco", "CM", 32), ("Giovani Lo Celso", "CM", 28), ("Pablo Fornals", "CM", 28),
        ("Ez Abde", "W", 22), ("Juanmi", "W", 31), ("Assane Diao", "W", 19),
        ("Cedric Bakambu", "ST", 33), ("Vitor Roque", "ST", 19), ("Ezequiel Avila", "ST", 30)
    ],
    "Villarreal": [
        ("Diego Conde", "GK", 26), ("Luiz Junior", "GK", 23),
        ("Raul Albiol", "CB", 38), ("Eric Bailly", "CB", 30), ("Willy Kambwala", "CB", 20), ("Logan Costa", "CB", 23),
        ("Juan Foyth", "FB", 26), ("Kiko Femenia", "FB", 33), ("Alfonso Pedraza", "FB", 28), ("Sergi Cardona", "FB", 25), ("Juan Bernat", "FB", 31),
        ("Dani Parejo", "CM", 35), ("Santi Comesana", "CM", 27), ("Pape Gueye", "CM", 25), ("Ramon Terrats", "CM", 23), ("Alex Baena", "CM", 23), ("Denis Suarez", "CM", 30),
        ("Yeremy Pino", "W", 21), ("Ilias Akhomach", "W", 20), ("Nicolas Pepe", "W", 29),
        ("Gerard Moreno", "ST", 32), ("Ayoze Perez", "ST", 31), ("Thierno Barry", "ST", 21)
    ],
    "Valencia": [
        ("Giorgi Mamardashvili", "GK", 23), ("Stole Dimitrievski", "GK", 30),
        ("Cristhian Mosquera", "CB", 20), ("Mouctar Diakhaby", "CB", 27), ("Cesar Tarrega", "CB", 22), ("Yarek Gasiorowski", "CB", 19),
        ("Thierry Correia", "FB", 25), ("Jose Gaya", "FB", 29), ("Dimitri Foulquier", "FB", 31), ("Jesus Vazquez", "FB", 21),
        ("Pepelu", "CM", 26), ("Javi Guerra", "CM", 21), ("Hugo Guillamon", "CM", 24), ("Enzo Barrenechea", "CM", 23), ("Andre Almeida", "CM", 24),
        ("Diego Lopez", "W", 22), ("Fran Perez", "W", 21), ("Sergi Canos", "W", 27), ("Luis Rioja", "W", 30),
        ("Hugo Duro", "ST", 24), ("Rafa Mir", "ST", 27), ("Dani Gomez", "ST", 26)
    ],
    "Sevilla": [
        ("Orjan Nyland", "GK", 33), ("Alvaro Fernandez", "GK", 26),
        ("Loic Bade", "CB", 24), ("Marcao", "CB", 28), ("Tanguy Nianzou", "CB", 22), ("Kike Salas", "CB", 22),
        ("Jesus Navas", "FB", 38), ("Jose Angel Carmona", "FB", 22), ("Adria Pedrosa", "FB", 26), ("Valentin Barco", "FB", 20),
        ("Nemanja Gudelj", "CM", 32), ("Djibril Sow", "CM", 27), ("Albert Sambi Lokonga", "CM", 24), ("Lucien Agoume", "CM", 22), ("Saul Niguez", "CM", 29), ("Juanlu Sanchez", "CM", 21),
        ("Dodi Lukebakio", "W", 26), ("Chidera Ejuke", "W", 26), ("Suso", "W", 30), ("Peque", "W", 21),
        ("Isaac Romero", "ST", 24), ("Kelechi Iheanacho", "ST", 27)
    ],
    "Osasuna": [
        ("Sergio Herrera", "GK", 31), ("Aitor Fernandez", "GK", 33),
        ("Alejandro Catena", "CB", 29), ("Jorge Herrando", "CB", 23), ("Enzo Boyomo", "CB", 22), ("Unai Garcia", "CB", 31),
        ("Jesus Areso", "FB", 25), ("Ruben Pena", "FB", 33), ("Juan Cruz", "FB", 32), ("Abel Bretones", "FB", 24),
        ("Jon Moncayola", "CM", 26), ("Lucas Torro", "CM", 30), ("Pablo Ibanez", "CM", 25), ("Iker Munoz", "CM", 21), ("Aimar Oroz", "CM", 22), ("Moi Gomez", "CM", 30),
        ("Ruben Garcia", "W", 31), ("Bryan Zaragoza", "W", 23), ("Jose Arnaiz", "W", 29), ("Iker Benito", "W", 22),
        ("Ante Budimir", "ST", 33), ("Raul Garcia", "ST", 23)
    ],
    "Getafe": [
        ("David Soria", "GK", 31), ("Jiri Letacek", "GK", 25),
        ("Djene", "CB", 32), ("Omar Alderete", "CB", 27), ("Domingos Duarte", "CB", 29), ("Nabil Aberdin", "CB", 22),
        ("Juan Iglesias", "FB", 26), ("Diego Rico", "FB", 31), ("Alex Sola", "FB", 25),
        ("Luis Milla", "CM", 29), ("Mauro Arambarri", "CM", 28), ("Carles Alena", "CM", 26), ("Uche", "CM", 21), ("Yellu Santiago", "CM", 20),
        ("Carles Perez", "W", 26), ("Peter Federico", "W", 22),
        ("Borja Mayoral", "ST", 27), ("Bertug Yildirim", "ST", 22), ("Alvaro Rodriguez", "ST", 20)
    ],
    "Celta Vigo": [
        ("Vicente Guaita", "GK", 37), ("Ivan Villar", "GK", 27),
        ("Carl Starfelt", "CB", 29), ("Joseph Aidoo", "CB", 28), ("Jailson", "CB", 28), ("Carlos Dominguez", "CB", 23),
        ("Oscar Mingueza", "FB", 25), ("Hugo Alvarez", "FB", 21), ("Javier Manquillo", "FB", 30), ("Marcos Alonso", "FB", 33),
        ("Fran Beltran", "CM", 25), ("Hugo Sotelo", "CM", 20), ("Damian Rodriguez", "CM", 21), ("Ilaix Moriba", "CM", 21), ("Williot Swedberg", "CM", 20),
        ("Iago Aspas", "W", 37), ("Jonathan Bamba", "W", 28), ("Franco Cervi", "W", 30), ("Alfon Gonzalez", "W", 25),
        ("Borja Iglesias", "ST", 31), ("Tasos Douvikas", "ST", 25), ("Pablo Duran", "ST", 23)
    ],
    "Rayo Vallecano": [
        ("Stole Dimitrievski", "GK", 30), ("Dani Cardenas", "GK", 27),
        ("Florian Lejeune", "CB", 33), ("Abdul Mumin", "CB", 26), ("Aridane Hernandez", "CB", 35), ("Pelayo Fernandez", "CB", 21),
        ("Ivan Balliu", "FB", 32), ("Alfonso Espino", "FB", 32), ("Pep Chavarria", "FB", 26), ("Andrei Ratiu", "FB", 26),
        ("Oscar Valentin", "CM", 30), ("Unai Lopez", "CM", 28), ("Pathe Ciss", "CM", 30), ("Gerard Gumbau", "CM", 29), ("Isi Palazon", "CM", 29), ("James Rodriguez", "CM", 33),
        ("Alvaro Garcia", "W", 31), ("Jorge de Frutos", "W", 27), ("Adri Embarba", "W", 32),
        ("Sergio Camello", "ST", 23), ("Raul de Tomas", "ST", 29), ("Randy Nteka", "ST", 26)
    ],
    "Mallorca": [
        ("Predrag Rajkovic", "GK", 28), ("Dominik Greif", "GK", 27), ("Leo Roman", "GK", 24),
        ("Antonio Raillo", "CB", 32), ("Martin Valjent", "CB", 28), ("Jose Copete", "CB", 24), ("Siebe Van der Heyden", "CB", 26),
        ("Pablo Maffeo", "FB", 27), ("Toni Lato", "FB", 26), ("Mateu Morey", "FB", 24), ("Johan Mojica", "FB", 31),
        ("Samu Costa", "CM", 23), ("Sergi Darder", "CM", 30), ("Dani Rodriguez", "CM", 36), ("Manu Morlanes", "CM", 25), ("Omar Mascarell", "CM", 31), ("Antonio Sanchez", "CM", 27),
        ("Takuma Asano", "W", 29), ("Javi Llabres", "W", 22), ("Valery Fernandez", "W", 24), ("Chiquinho", "W", 24),
        ("Vedat Muriqi", "ST", 30), ("Cyle Larin", "ST", 29), ("Abdon Prats", "ST", 31)
    ],
    "Las Palmas": [
        ("Jasper Cillessen", "GK", 35), ("Dinko Horkas", "GK", 25),
        ("Mika Marmol", "CB", 23), ("Scott McKenna", "CB", 27), ("Alex Suarez", "CB", 31), ("Juanma Herzog", "CB", 20),
        ("Alex Munoz", "FB", 29), ("Marvin Park", "FB", 24), ("Daley Sinkgraven", "FB", 29), ("Viti Rozada", "FB", 26),
        ("Kirian Rodriguez", "CM", 28), ("Javi Munoz", "CM", 29), ("Enzo Loiodice", "CM", 23), ("Jose Campana", "CM", 31), ("Fabio Gonzalez", "CM", 27), ("Dario Essugo", "CM", 19),
        ("Sandro Ramirez", "W", 29), ("Adnan Januzaj", "W", 29), ("Benito Ramirez", "W", 29), ("Pejino", "W", 28),
        ("Oli McBurnie", "ST", 28), ("Jaime Mata", "ST", 35), ("Marc Cardona", "ST", 29), ("Fabio Silva", "ST", 22)
    ],
    "Alaves": [
        ("Antonio Sivera", "GK", 28), ("Jesus Owono", "GK", 23),
        ("Abdel Abqar", "CB", 25), ("Aleksandar Sedlar", "CB", 32), ("Santiago Mourino", "CB", 22), ("Facundo Garces", "CB", 24),
        ("Nahuel Tenaglia", "FB", 28), ("Manu Sanchez", "FB", 24), ("Hugo Novoa", "FB", 21), ("Moussa Diarra", "FB", 23),
        ("Ander Guevara", "CM", 27), ("Jon Guridi", "CM", 29), ("Antonio Blanco", "CM", 24), ("Carlos Protesoni", "CM", 23), ("Joan Jordan", "CM", 30),
        ("Carlos Vicente", "W", 25), ("Tomas Conechny", "W", 26), ("Luka Romero", "W", 19), ("Abde Rebbach", "W", 26),
        ("Kike Garcia", "ST", 34), ("Toni Martinez", "ST", 27), ("Asier Villalibre", "ST", 26)
    ],
    "Espanyol": [
        ("Joan Garcia", "GK", 23), ("Fernando Pacheco", "GK", 32),
        ("Leandro Cabrera", "CB", 33), ("Fernando Calero", "CB", 28), ("Marash Kumbulla", "CB", 24), ("Sergi Gomez", "CB", 32),
        ("Omar El Hilali", "FB", 21), ("Brian Olivan", "FB", 30), ("Carlos Romero", "FB", 22), ("Alvaro Tejero", "FB", 28),
        ("Pol Lozano", "CM", 24), ("Alex Kral", "CM", 26), ("Jose Gragera", "CM", 24), ("Alvaro Aguado", "CM", 28), ("Edu Exposito", "CM", 28),
        ("Javi Puado", "W", 26), ("Irvin Cardona", "W", 27), ("Salvi Sanchez", "W", 33), ("Jofre Carreras", "W", 23),
        ("Alejo Veliz", "ST", 20), ("Walid Cheddira", "ST", 26), ("Pere Milla", "ST", 31)
    ],
    "Leganes": [
        ("Marko Dmitrovic", "GK", 32), ("Juan Soriano", "GK", 27),
        ("Sergio Gonzalez", "CB", 32), ("Matija Nastasic", "CB", 31), ("Jorge Saenz", "CB", 27), ("Jackson Porozo", "CB", 24),
        ("Valentin Rosier", "FB", 28), ("Enric Franquesa", "FB", 27), ("Javi Hernandez", "FB", 26), ("Adria Altimira", "FB", 23),
        ("Darko Brasanac", "CM", 32), ("Yvan Neyou", "CM", 27), ("Seydouba Cisse", "CM", 23), ("Renato Tapia", "CM", 29), ("Roberto Lopez", "CM", 24),
        ("Juan Cruz", "W", 24), ("Oscar Rodriguez", "W", 26), ("Munir El Haddadi", "W", 28), ("Dani Raba", "W", 28),
        ("Miguel de la Fuente", "ST", 25), ("Sebastien Haller", "ST", 30), ("Diego Garcia", "ST", 24)
    ],
    "Real Valladolid": [
        ("Karl Hein", "GK", 22), ("Andre Ferreira", "GK", 28),
        ("Javi Sanchez", "CB", 27), ("Eray Comert", "CB", 26), ("David Torres", "CB", 21), ("Cenk Ozkacar", "CB", 23),
        ("Luis Perez", "FB", 29), ("Lucas Rosa", "FB", 24), ("Raul Chasco", "FB", 20),
        ("Kike Perez", "CM", 27), ("Victor Meseguer", "CM", 25), ("Stanko Juric", "CM", 28), ("Selim Amallah", "CM", 27), ("Mario Martin", "CM", 20), ("Cesar de la Hoz", "CM", 32),
        ("Raul Moro", "W", 21), ("Amath Ndiaye", "W", 28), ("Ivan Sanchez", "W", 31), ("Darwin Machis", "W", 31),
        ("Mamadou Sylla", "ST", 30), ("Juanmi Latasa", "ST", 23), ("Marcos Andre", "ST", 27)
    ]
}

def generate_stats(pos):
    if pos == "GK":
        return {
            "psxg_net_per90": round(random.uniform(-0.3, 0.3), 2),
            "save_pct": round(random.uniform(60.0, 80.0), 1),
            "pass_completion_pct": round(random.uniform(60.0, 90.0), 1),
            "passes_completed_long_pct": round(random.uniform(30.0, 60.0), 1),
            "def_actions_outside_pen_per90": round(random.uniform(0.5, 2.5), 2),
            "crosses_stopped_pct": round(random.uniform(4.0, 12.0), 1),
            "avg_dist_def_actions": round(random.uniform(10.0, 18.0), 1)
        }
    elif pos == "CB":
        return {
            "pass_completion_pct": round(random.uniform(75.0, 95.0), 1),
            "progressive_passes_per90": round(random.uniform(2.0, 6.0), 2),
            "progressive_passing_distance_per90": round(random.uniform(200.0, 500.0), 1),
            "passes_into_final_third_per90": round(random.uniform(1.0, 5.0), 2),
            "progressive_carries_per90": round(random.uniform(0.5, 2.5), 2),
            "take_on_success_pct": round(random.uniform(40.0, 80.0), 1),
            "padj_tackles_per90": round(random.uniform(1.0, 3.5), 2),
            "padj_interceptions_per90": round(random.uniform(1.0, 3.5), 2),
            "ball_recoveries_per90": round(random.uniform(4.0, 8.0), 2),
            "blocks_per90": round(random.uniform(1.0, 3.0), 2),
            "aerial_win_pct": round(random.uniform(50.0, 75.0), 1),
            "tackle_win_pct": round(random.uniform(55.0, 85.0), 1)
        }
    elif pos == "FB":
        return {
            "xAG_per90": round(random.uniform(0.05, 0.25), 2),
            "sca_per90": round(random.uniform(1.0, 3.5), 2),
            "key_passes_per90": round(random.uniform(0.5, 2.0), 2),
            "passes_into_penalty_area_per90": round(random.uniform(0.5, 2.0), 2),
            "pass_completion_pct": round(random.uniform(70.0, 88.0), 1),
            "progressive_passes_per90": round(random.uniform(3.0, 7.0), 2),
            "progressive_carries_per90": round(random.uniform(1.5, 4.5), 2),
            "passes_into_final_third_per90": round(random.uniform(2.0, 6.0), 2),
            "take_ons_attempted_per90": round(random.uniform(1.0, 4.0), 2),
            "take_on_success_pct": round(random.uniform(40.0, 70.0), 1),
            "padj_tackles_per90": round(random.uniform(1.5, 4.0), 2),
            "padj_interceptions_per90": round(random.uniform(1.0, 3.0), 2),
            "ball_recoveries_per90": round(random.uniform(4.0, 8.0), 2),
            "tackles_att_3rd_per90": round(random.uniform(0.1, 0.8), 2),
            "aerial_win_pct": round(random.uniform(40.0, 65.0), 1)
        }
    elif pos == "CM":
        return {
            "npxG_per90": round(random.uniform(0.05, 0.25), 2),
            "xAG_per90": round(random.uniform(0.05, 0.30), 2),
            "sca_per90": round(random.uniform(1.5, 4.5), 2),
            "key_passes_per90": round(random.uniform(0.5, 2.5), 2),
            "passes_into_penalty_area_per90": round(random.uniform(0.5, 2.5), 2),
            "pass_completion_pct": round(random.uniform(75.0, 92.0), 1),
            "progressive_passes_per90": round(random.uniform(4.0, 9.0), 2),
            "progressive_carries_per90": round(random.uniform(1.5, 4.0), 2),
            "passes_into_final_third_per90": round(random.uniform(3.0, 8.0), 2),
            "take_on_success_pct": round(random.uniform(45.0, 75.0), 1),
            "padj_tackles_per90": round(random.uniform(1.5, 4.5), 2),
            "padj_interceptions_per90": round(random.uniform(1.0, 3.5), 2),
            "ball_recoveries_per90": round(random.uniform(5.0, 9.0), 2),
            "blocks_per90": round(random.uniform(0.8, 2.5), 2),
            "aerial_win_pct": round(random.uniform(40.0, 65.0), 1)
        }
    elif pos == "W":
        return {
            "npxG_per90": round(random.uniform(0.15, 0.45), 2),
            "xAG_per90": round(random.uniform(0.15, 0.40), 2),
            "sca_per90": round(random.uniform(2.5, 5.5), 2),
            "shots_total_per90": round(random.uniform(1.5, 4.0), 2),
            "touches_att_pen_per90": round(random.uniform(3.0, 8.0), 2),
            "take_ons_attempted_per90": round(random.uniform(3.0, 8.0), 2),
            "take_on_success_pct": round(random.uniform(35.0, 65.0), 1),
            "progressive_carries_per90": round(random.uniform(3.0, 7.0), 2),
            "progressive_passes_per90": round(random.uniform(2.0, 6.0), 2),
            "carries_into_penalty_area_per90": round(random.uniform(1.0, 3.5), 2),
            "key_passes_per90": round(random.uniform(1.0, 3.0), 2),
            "padj_tackles_per90": round(random.uniform(0.5, 2.5), 2),
            "padj_interceptions_per90": round(random.uniform(0.2, 1.5), 2),
            "ball_recoveries_per90": round(random.uniform(2.0, 5.0), 2),
            "tackles_att_3rd_per90": round(random.uniform(0.2, 1.2), 2)
        }
    elif pos == "ST":
        return {
            "npxG_per90": round(random.uniform(0.30, 0.75), 2),
            "shots_total_per90": round(random.uniform(2.0, 5.0), 2),
            "shots_on_target_pct": round(random.uniform(35.0, 55.0), 1),
            "touches_att_pen_per90": round(random.uniform(4.0, 9.0), 2),
            "aerial_win_pct": round(random.uniform(30.0, 60.0), 1),
            "xAG_per90": round(random.uniform(0.05, 0.25), 2),
            "sca_per90": round(random.uniform(1.5, 3.5), 2),
            "key_passes_per90": round(random.uniform(0.5, 2.0), 2),
            "pass_completion_pct": round(random.uniform(65.0, 82.0), 1),
            "carries_into_penalty_area_per90": round(random.uniform(0.5, 2.5), 2),
            "tackles_att_3rd_per90": round(random.uniform(0.1, 0.8), 2),
            "ball_recoveries_per90": round(random.uniform(1.0, 3.5), 2),
            "padj_tackles_per90": round(random.uniform(0.3, 1.5), 2)
        }

with open(outfile, 'w', encoding='utf-8') as f:
    f.write("LA_LIGA_REAL_ROSTERS = {\n")
    for team, players in teams.items():
        f.write(f'    "{team}": [\n')
        for player in players:
            name, pos, age = player
            mins = random.randint(500, 3200)
            stats = generate_stats(pos)
            
            stats_str = ", ".join([f"'{k}': {v}" for k, v in stats.items()])
            f.write(f'        ("{name}", "{pos}", {age}, {mins}, {{{stats_str}}}),\n')
        f.write("    ],\n")
    f.write("}\n")

print(f"Generated successfully at {outfile}")
