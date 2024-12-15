import argparse
import subprocess
import platform

def traceroute(target, progressive, output_file):
    # Déterminer la commande selon le système d'exploitation
    traceroute_cmd = ["tracert"] if platform.system() == "Windows" else ["traceroute"]
    traceroute_cmd.append(target)
    
    results = []

    try:
        if progressive:
            # Mode progressif avec subprocess.Popen
            process = subprocess.Popen(traceroute_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            with process.stdout:
                for line in iter(process.stdout.readline, ''):
                    print(line.strip())  # Affichage progressif
                    results.append(line.strip())
        else:
            # Mode complet avec subprocess.run
            result = subprocess.run(traceroute_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            results = result.stdout.splitlines()
            print("\n".join(results))  # Affichage complet

        # Enregistrement dans un fichier si demandé
        if output_file:
            with open(output_file, 'w') as file:
                file.write("\n".join(results))
            print(f"Résultats enregistrés dans le fichier : {output_file}")

    except Exception as e:
        print(f"Erreur lors de l'exécution du traceroute : {e}")

def main():
    parser = argparse.ArgumentParser(description="Script de traceroute avec options.")
    parser.add_argument("target", help="URL ou adresse IP cible pour le traceroute.")
    parser.add_argument("-p", "--progressive", action="store_true",
                        help="Affiche les résultats au fur et à mesure.")
    parser.add_argument("-o", "--output-file", type=str,
                        help="Nom du fichier pour enregistrer les résultats.")
    args = parser.parse_args()

    traceroute(args.target, args.progressive, args.output_file)

if __name__ == "__main__":
    main()
