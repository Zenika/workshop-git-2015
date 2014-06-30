# Modèle de branche

<!-- .slide: class="page-title" -->



## Qu'est-ce qu'une branche ?

Conceptuellement, c'est simplement une branche du graphe acyclique orienté des commits.

<figure>
    <img src="ressources/branches_concept.png" alt="Branches" width="50%"/>
</figure>




## Le but des branches

Les branches sont un moyen de faire des développements parallèles.

Cela permet de ne pas avoir de développements intermédiaire sur la branche principale.

Il est ainsi possible de livrer à tout moment ce qui est terminé.

Ou de décider à tout moment ce que l'on veut livrer.



## Les branches dans Git

Techniquement, c'est un fichier contenant le SHA1 d'un commit.

```shell
$ tree .git/refs/heads/
.git/refs/heads/
├── big-feature
├── little-feature
└── master

0 directories, 3 files

$ cat .git/refs/heads/master
f3e305e8e299c36370302a7b695d457c2aa14a7a
```

La branche courante est celle référencée par le HEAD.
```shell
$ cat .git/HEAD
ref: refs/heads/master
```



## Arborescence de branches

Il est parfaitement possible d'organiser les branches par dossier :
```shell
$ tree .git/refs/heads/
.git/refs/heads/
├── feature
│   ├── feature1
│   └── feature2
├── master
└── release
    ├── 1.0.x
    └── 1.1.x

2 directories, 6 files

$ git branch
  feature/feature1
  feature/feature2
* master
  release/1.0.x
  release/1.1.x
```



## Branches symboliques

Il est possible de créer une branche symbolique, c'est-à-dire une branche qui est une indirection sur une autre branche :
```shell
$ git symbolic-ref refs/heads/release/current\
 refs/heads/release/1.1.x

$ cat .git/refs/heads/release/current
ref: refs/heads/release/1.1.x

$ git branch
  feature/feature1
  feature/feature2
* master
  release/1.0.x
  release/1.1.x
  release/current -> release/1.1.x
```
