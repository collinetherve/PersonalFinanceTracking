# GEMINI.md

# 1. Présentation du projet

Cette application est une application full-stack de **suivi des dépenses personnelles**.

L'application est composée de :

* **Frontend** : React
* **UI / Styling** : Tailwind CSS + shadcn/ui
* **Backend** : Django
* **API** : Django REST Framework
* **Base de données** : à définir selon l'environnement, SQLite pour le développement initial et PostgreSQL recommandé en production.

L'objectif est de construire une application :

* simple à utiliser ;
* rapide ;
* minimaliste ;
* professionnelle ;
* responsive ;
* maintenable ;
* facilement extensible.

---

# 2. Principes généraux

Lors de toute modification du projet, respecter les principes suivants :

1. Privilégier la simplicité.
2. Ne pas ajouter de dépendance inutile.
3. Ne pas dupliquer du code lorsqu'une abstraction simple est pertinente.
4. Ne pas créer d'architecture complexe prématurément.
5. Préserver les fonctionnalités existantes lors des modifications.
6. Écrire du code lisible avant de chercher à optimiser.
7. Garder une séparation claire entre frontend et backend.
8. Les données provenant de l'utilisateur doivent toujours être validées côté backend.
9. Ne jamais faire confiance aux données envoyées par le frontend.
10. Ne jamais stocker de mots de passe en clair.

---

# 3. Structure générale du projet

Le projet doit conserver une séparation claire entre frontend et backend.

Structure recommandée :

```text
project/
├── backend/
│   ├── manage.py
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── apps/
│   │   ├── users/
│   │   └── expenses/
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── lib/
│   │
│   ├── public/
│   └── package.json
│
└── GEMINI.md
```

Cette structure peut être adaptée si le projet existant impose une autre organisation.

---

# 4. Frontend

## 4.1 Technologies

Le frontend utilise :

* React
* Tailwind CSS
* shadcn/ui

Les composants shadcn/ui doivent être privilégiés lorsqu'un composant équivalent existe.

Ne pas réinventer inutilement des composants déjà disponibles dans shadcn/ui.

---

## 4.2 Direction artistique

L'interface doit avoir une esthétique :

* minimaliste ;
* épurée ;
* professionnelle ;
* moderne ;
* sobre ;
* cohérente.

Éviter :

* les interfaces surchargées ;
* les couleurs trop nombreuses ;
* les gradients décoratifs inutiles ;
* les animations excessives ;
* les ombres trop fortes ;
* les bordures omniprésentes ;
* les éléments visuellement inutiles.

L'interface doit donner une impression de **clarté et de contrôle**, adaptée à une application de gestion financière.

---

## 4.3 Couleurs

Utiliser principalement les variables de thème de Tailwind/shadcn :

* `background`
* `foreground`
* `primary`
* `secondary`
* `muted`
* `accent`
* `destructive`
* `border`

Éviter d'introduire des couleurs arbitraires directement dans les composants lorsqu'une variable du thème existe.

Exemple à privilégier :

```tsx
<Button variant="default">
  Ajouter une dépense
</Button>
```

plutôt que :

```tsx
<button className="bg-blue-600 text-white">
  Ajouter une dépense
</button>
```

---

## 4.4 Composants

Les composants React doivent respecter le principe de responsabilité unique.

Privilégier :

```text
components/
├── ui/
├── expenses/
├── dashboard/
└── navigation/
```

Un composant ne doit pas devenir excessivement volumineux.

Si un composant dépasse une taille raisonnable ou contient plusieurs responsabilités distinctes, envisager de le découper.

---

## 4.5 Responsive design

L'application doit être responsive par défaut.

Les interfaces doivent fonctionner correctement sur :

* mobile ;
* tablette ;
* ordinateur.

Toujours concevoir l'interface en **mobile-first** lorsque cela est pertinent.

---

## 4.6 Gestion des états

Éviter les états React inutiles.

Avant d'utiliser `useState`, vérifier si la donnée peut être :

* calculée ;
* dérivée d'une autre donnée ;
* gérée directement par un formulaire ;
* récupérée depuis l'API.

Ne pas introduire Redux ou une autre solution de state management globale sans besoin réel.

---

## 4.7 Communication avec l'API

La communication avec le backend doit être centralisée dans des services ou fonctions dédiées.

Exemple :

```text
services/
├── authService.ts
└── expenseService.ts
```

Éviter de multiplier les appels `fetch()` directement dans les composants.

Exemple :

```tsx
const expenses = await expenseService.getExpenses();
```

plutôt que :

```tsx
const response = await fetch("/api/expenses/");
```

dans plusieurs composants différents.

---

# 5. Backend Django

## 5.1 Technologies

Le backend utilise :

* Django
* Django REST Framework

L'API doit être organisée autour de ressources REST.

Exemple :

```text
/api/auth/login/
/api/auth/logout/
/api/expenses/
/api/expenses/<id>/
```

---

# 6. Vues Django REST Framework

## Règle importante

Pour les endpoints API, utiliser **des vues basées sur des fonctions**.

Privilégier :

```python
@api_view(["GET", "POST"])
def expenses(request):
    ...
```

et :

```python
@api_view(["GET", "PUT", "DELETE"])
def expense_detail(request, expense_id):
    ...
```

Ne pas utiliser de `APIView`, `ViewSet` ou classes génériques DRF sauf demande explicite ou nécessité particulière.

---

## 6.1 Récupération des données

Pour les données envoyées par le frontend, utiliser :

```python
request.data.get("field")
```

Exemple :

```python
description = request.data.get("description")
amount = request.data.get("amount")
category = request.data.get("category")
```

Éviter :

```python
request.data["description"]
```

lorsque cela n'est pas nécessaire.

Cela permet notamment de gérer explicitement les champs absents.

---

## 6.2 Validation

Toute donnée reçue du frontend doit être validée côté backend.

Exemple :

```python
amount = request.data.get("amount")

if amount is None:
    return Response(
        {"error": "Le montant est obligatoire."},
        status=400
    )
```

La validation frontend est utile pour l'expérience utilisateur mais **ne remplace jamais la validation backend**.

---

# 7. Modèle des dépenses

Une dépense doit au minimum pouvoir contenir :

```text
Expense
├── id
├── user
├── bank_account
├── amount
├── description
├── category
├── type (income or expense)
├── date
├── created_at
└── updated_at
```

Le champ `user` permet d'associer chaque dépense à son propriétaire.

Le champs `bank_account` doit permettre de savoir d'où provient ou à quel compte appartient la dépense.

Un utilisateur ne doit jamais pouvoir consulter ou modifier les dépenses appartenant à un autre utilisateur.


---

# 8. Authentification

## Version 1

La première version utilise une authentification simple basée sur :

* login ;
* mot de passe.

Les mots de passe doivent être **hachés**, jamais stockés en clair.

Utiliser le système d'authentification natif de Django et ses mécanismes de hashage.

Ne jamais implémenter soi-même un algorithme de chiffrement ou de hashage des mots de passe.

---

## 8.1 Utilisateur

Privilégier le système d'utilisateur Django :

```python
from django.contrib.auth.models import User
```

ou un modèle utilisateur personnalisé uniquement si cela devient nécessaire.

---

## 8.2 Login

Le frontend envoie :

```json
{
  "username": "john",
  "password": "password"
}
```

Le backend vérifie les identifiants avec les mécanismes Django.

Le mot de passe ne doit jamais être :

* retourné par l'API ;
* enregistré dans les logs ;
* stocké en clair ;
* inclus dans une réponse JSON.

---

# 9. Sécurité

La sécurité est une priorité.

Toujours :

* valider les données côté backend ;
* vérifier l'utilisateur authentifié ;
* vérifier les permissions avant toute modification ;
* empêcher l'accès aux données d'un autre utilisateur ;
* utiliser les mécanismes de sécurité Django ;
* protéger les secrets et clés privées ;
* utiliser des variables d'environnement pour les secrets.

Ne jamais :

* mettre une clé secrète dans le frontend ;
* mettre un mot de passe dans Git ;
* retourner un mot de passe dans une réponse API ;
* faire confiance à un `user_id` fourni par le frontend pour déterminer le propriétaire d'une ressource.

Le propriétaire d'une dépense doit être déterminé à partir de l'utilisateur authentifié.

Exemple :

```python
expense = Expense.objects.create(
    user=request.user,
    amount=amount,
    description=description,
)
```

et non :

```python
user_id = request.data.get("user_id")
```

---

# 10. API

Les réponses API doivent être simples, prévisibles et cohérentes.

Exemple de succès :

```json
{
  "id": 1,
  "amount": "42.50",
  "description": "Courses",
  "category": "Alimentation",
  "date": "2026-10-05"
}
```

Exemple d'erreur :

```json
{
  "error": "Le montant est obligatoire."
}
```

Utiliser les codes HTTP appropriés :

* `200` : succès
* `201` : création
* `400` : données invalides
* `401` : non authentifié
* `403` : accès interdit
* `404` : ressource inexistante
* `500` : erreur serveur

---

# 11. Gestion des erreurs

Les erreurs doivent être explicites pour faciliter leur traitement par le frontend.

Éviter les réponses vagues comme :

```json
{
  "error": "Erreur"
}
```

Préférer :

```json
{
  "error": "Impossible de créer la dépense : le montant doit être supérieur à 0."
}
```

Le frontend doit afficher les erreurs de manière compréhensible pour l'utilisateur.

---

# 12. Base de données

Les montants financiers doivent utiliser un type décimal.

Dans Django :

```python
amount = models.DecimalField(
    max_digits=10,
    decimal_places=2
)
```

Ne jamais utiliser `FloatField` pour représenter de l'argent.

Les dates doivent utiliser les fonctionnalités timezone-aware de Django.

Il faut prévoir une table pour les comptes bancaires et une autre pour les utilisateurs.

En plus de cela, il faudra sans doute prévoir une table pour les catégories de dépenses et d'autres tables pour les autres fonctionnalités du site. Ces tables doivent être pensées pour être facilement modifiables et extensibles.

En respectant ces consignes, le projet doit être structuré d'une manière cohérente.

---

# 13. Catégories de dépenses

Les catégories doivent être structurées de manière cohérente.

Exemples :

* Alimentation (courses...)
* Logement (loyer...)
* Transport (essence, ticket...)
* Loisirs (sortie, restaurant...)
* Abonnements (net, téléphone...)
* Santé (médicaments...)
* Shopping (vêtement, accessoire...)
* Factures (charges...)
* Scolarité (frais de scolarité, livres, fournitures...)
* Transferts (vers un autre compte)
* Retrait (d'un compte)
* Divers
* Autres

Le système doit pouvoir être étendu ultérieurement sans nécessiter une refonte majeure.

Les catégories doivent être stockées dans la base de données., une ligne de dépense doit contenir un id de catégorie et pas le nom de la catégorie.

---

# 14. Dashboard

Le dashboard doit permettre à l'utilisateur de comprendre rapidement sa situation financière.

Il peut notamment afficher :

* dépenses du mois ;
* dépenses de la semaine ;
* nombre de dépenses ;
* répartition par catégorie ;
* dernières dépenses ;
* évolution des dépenses.

Le dashboard doit rester visuellement simple.

Éviter de présenter trop de graphiques simultanément.

---

# 15. UX

L'utilisateur doit pouvoir :

1. se connecter ;
2. consulter ses dépenses ;
3. ajouter une dépense :
3. 1. manuellement
3. 2. en important des relevés bancaires (csv), un fichier csv par compte bancaire;
4. modifier une dépense :
4. 1. associer une catégorie
4. 2. associer un compte bancaire
4. 3. modifier la description;
4. 4. associer un type de dépense;
4. 5. découper une dépense en plusieurs dépenses;
4. 6. fusionner plusieurs dépenses en une seule dépense;
5. supprimer une dépense;
6. filtrer ses dépenses;
6. 1. par catégorie
6. 2. par compte bancaire
6. 3. par date, jour, mois, année;
6. 4. par type de dépense
7. consulter des statistiques simples ;
7. 1. dépenses du mois
7. 2. dépenses de la semaine
7. 3. nombre de dépenses
7. 4. répartition par catégorie
7. 5. dernières dépenses
7. 6. évolution des dépenses (par jour, semaine, mois, année)
7. 7. évolution par catégorie (par jour, semaine, mois, année)
7. 8. évolution par compte bancaire (par jour, semaine, mois, année)
7. 9. évolution par type de dépense (par jour, semaine, mois, année)
7. 10. évolution par catégorie, compte bancaire et type de dépense (par jour, semaine, mois, année)
8. se déconnecter.
9. paramétrer le système

Les actions importantes doivent être facilement accessibles.

Les actions sensibles, comme modifier ou supprimer une dépense, doivent demander une confirmation lorsque cela est pertinent.

---

# 16. Conventions de code

## Python

Respecter autant que possible :

* PEP 8 ;
* noms explicites ;
* fonctions courtes ;
* responsabilités clairement séparées.

Exemple :

```python
def create_expense(request):
    amount = request.data.get("amount")
    description = request.data.get("description")

    ...
```

Éviter les noms vagues :

```python
def process_data():
    ...
```

---

## React / TypeScript

Privilégier :

* composants fonctionnels ;
* hooks React ;
* TypeScript ;
* props explicitement typées ;
* noms explicites.

Exemple :

```tsx
interface Expense {
  id: number;
  amount: string;
  description: string;
  category: string;
  date: string;
}
```

---

# 17. Comment modifier le projet

Avant de modifier du code :

1. Comprendre l'architecture existante.
2. Identifier les fichiers concernés.
3. Vérifier les dépendances existantes.
4. Éviter de modifier des fichiers sans rapport avec la tâche.
5. Préserver les conventions déjà présentes dans le projet.

Après une modification :

1. Vérifier les imports.
2. Vérifier les types.
3. Vérifier les routes API.
4. Vérifier les permissions.
5. Vérifier les erreurs potentielles.
6. Exécuter les tests disponibles.
7. Vérifier que les fonctionnalités existantes ne sont pas cassées.

---

# 18. Tests

Les fonctionnalités importantes doivent être testées.

Backend :

* création d'une dépense ;
* modification ;
* suppression ;
* récupération ;
* authentification ;
* permissions ;
* isolation des données entre utilisateurs.

Frontend :

* affichage des dépenses ;
* formulaire d'ajout ;
* validation ;
* gestion des erreurs ;
* authentification ;
* états de chargement.

---

# 19. Principes à respecter par Gemini

Lorsque tu génères ou modifies du code :

* Explique brièvement les changements importants.
* Ne génère pas de code inutile.
* Respecte l'architecture existante.
* Ne crée pas d'abstraction prématurée.
* Ne change pas de technologie sans raison.
* Ne remplace pas Django/DRF par une autre technologie.
* Utilise des vues DRF basées sur des fonctions.
* Utilise `request.data.get()`.
* Utilise les composants shadcn/ui lorsque pertinents.
* Respecte l'esthétique minimaliste et professionnelle.
* Priorise la sécurité des données financières.
* Ne stocke jamais les mots de passe en clair.
* Ne donne jamais accès à un utilisateur aux données d'un autre utilisateur.
* N'ajoute pas de fonctionnalités non demandées sans les signaler.

---

# 20. Priorités du projet

En cas de conflit entre plusieurs choix, respecter cet ordre :

1. **Sécurité**
2. **Correctness / fonctionnement**
3. **Simplicité**
4. **Maintenabilité**
5. **Expérience utilisateur**
6. **Performance**
7. **Esthétique**

L'objectif est de construire progressivement une application fiable, simple et professionnelle plutôt qu'une architecture excessivement complexe dès la première version.