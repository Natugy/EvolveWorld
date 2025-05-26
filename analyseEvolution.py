import matplotlib.pyplot as plt
import numpy as np

# Charger les données sauvegardées
data = np.load("history.npy")

generations = data[:, 0]
sizes = data[:, 1]
speeds = data[:, 2]
visions = data[:, 3]
scores = data[:, 4]

# Créer 4 sous-graphes (2 lignes, 2 colonnes)
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Évolution des attributs de Kirby")

# Vue 1 : Size
axs[0, 0].plot(generations, sizes, color='blue')
axs[0, 0].set_title("Taille (Size)")
axs[0, 0].set_xlabel("Génération")
axs[0, 0].set_ylabel("Taille")

# Vue 2 : Speed
axs[0, 1].plot(generations, speeds, color='green')
axs[0, 1].set_title("Vitesse (Speed)")
axs[0, 1].set_xlabel("Génération")
axs[0, 1].set_ylabel("Vitesse")

# Vue 3 : Vision
axs[1, 0].plot(generations, visions, color='orange')
axs[1, 0].set_title("Vision")
axs[1, 0].set_xlabel("Génération")
axs[1, 0].set_ylabel("Vision")

# Vue 4 : Fitness
axs[1, 1].plot(generations, scores, color='red')
axs[1, 1].set_title("Fitness")
axs[1, 1].set_xlabel("Génération")
axs[1, 1].set_ylabel("Score")

# Ajustement des espaces
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Laisse la place pour le titre principal
plt.show()
