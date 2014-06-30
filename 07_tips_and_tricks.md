# Trucs et astuces

<!-- .slide: class="page-title" -->



## Checkout de la dernière branche

Vous connaissez le `cd -` ?
```shell
~ $ cd Dev/jenkins/jenkins/
~/Dev/jenkins/jenkins $ cd -
/home/alex
~ $ cd -
/home/alex/Dev/jenkins/jenkins
~/Dev/jenkins/jenkins $ 
```

Et bien vous avez la même chose en Git avec le checkout :
```shell
$ git checkout master
Switched to branch 'master'

$ git checkout branch
Switched to branch 'branch'

$ git checkout -
Switched to branch 'master'
```



## Chercher l'erreur avec bisect

`git bisect` vous permet de faire une dichotomie pour trouver le commit (et donc le code) ayant provoqué un bug.

1. Déterminer le dernier commit sans bug (par exemple la dernière version) = GOOD
2. Écrire un test permettant de vérifier la présence du bug
3. Lancer `git bisect`
```shell
$ git bisect start HEAD GOOD
```
4. Git va effectuer une dichotomie, tester alors chaque commit en lançant le test et indiquer s'il est correct avec `git bisect good` ou mauvais avec `git bisect bad`
5. Trouver le bug dans le commit fautif



## Un diff au mot à mot

Marre d'avoir un diff indiquant un changement sur toute la ligne pour le changement d'un seul caractère ?
```diff
 Marre d'avoir un diff indiquant un changement sur toute la ligne
-pour le changement d'un seul caractere ?
+pour le changement d'un seul caractère ?
```

Utiliser l'option `--word-diff` :
```diff
Marre d'avoir un diff indiquant un changement sur toute la ligne
pour le changement d'un seul [-caractere-]{+caractère+} ?
```



## Diff et espaces

Une *grosse* astuce : toujours terminer vos fichiers par un saut de ligne.
```diff
-Dernière ligne de code.
\ No newline at end of file
+Dernière ligne de code.
+La vraie dernière ligne.
\ No newline at end of file
```
```diff
 Dernière ligne de code.
+La vraie dernière ligne.
```

Vous avez aussi les options `--ignore-space-at-eol`, `--ignore-space-change` et `--ignore-all-space` pour éviter les différences d'espaces.



## Alias

De la même manière que votre shell vous permet de définir des alias, git possède un système d'alias.

```shell
$ git config --global alias.st status
$ git config --global alias.ci commit
$ git config --global alias.co checkout
$ git config --global alias.glog log\
 'log --graph --oneline --decorate --branches --tags --remotes'
$ git config --global alias.git '!git'
```

Un dernier pour la route ?

```shell
$ git config --global alias.lg "log --graph --pretty=format:
 '%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr)
  %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative"
```



## Mettre de côté avec le stash

Git est sympa : il ne vous permet pas de perdre ou mélanger vos modifications locales sur certaines actions (checkout, merge, rebase).
```shell
$ git checkout branch
error: Your local changes to the following
files would be overwritten by checkout:
	Zenika.txt
Please, commit your changes or stash them
before you can switch branches.
Aborting
```

Mais il est encore plus sympa car il met à disposition un système pour sauvegarder les modifications locales avant ces actions : le *stash*.

Un stash est une suite de 2 commits pour sauvegarder les modifications locales :

- un commit pour l'index
- un commit pour l'espace de travail



## Mettre dans le stash

```shell
$ git status -s
M  Zenika.txt
 M folder/empty.txt

$ git stash
Saved working directory and index state WIP on master: 3568a7f 4th commit
HEAD is now at 3568a7f 4th commit

$ git status -s

$ git log --oneline --graph --decorate --all -3
*   33cccc8 (refs/stash) WIP on master: 3568a7f 4th commit
|\  
| * 06adc4e index on master: 3568a7f 4th commit
|/  
* 3568a7f (HEAD, master) 4th commit
```



## Appliquer le stash

```shell
$ git checkout branch
Switched to branch 'branch'

$ git stash list
stash@{0}: WIP on master: 3568a7f 4th commit

$ git stash pop --index
On branch branch
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	modified:   Zenika.txt

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   folder/empty.txt

Dropped refs/stash@{0} (33cccc89e7487595f675ce9ff26a1bf4df232f7c)
```



## Reflog

Git garde un historique de mise à jour des références : le reflog.

```shell
$ git reflog
3568a7f HEAD@{0}: checkout: moving from branch to master
f3e305e HEAD@{1}: checkout: moving from master to branch
3568a7f HEAD@{2}: checkout: moving from branch to master
f3e305e HEAD@{3}: checkout: moving from master to branch
3568a7f HEAD@{4}: commit: 4th commit
6c68d48 HEAD@{5}: commit: fixup! 2nd commit
e8353bb HEAD@{6}: commit: 3rd commit
```



## Références relatives

Il est possible de référencer des objets Git sans connaitre leur SHA1.

- `<ref>^<n>` : le nième parent, permet de choisir l'embrayage en remontant un merge
- `<ref>~<n>` : le nième ancètre, permet de choisir la profondeur de remontée
- `<ref>^{tree}` : le tree d'un commit
- `<ref>^{commit}` : le commit d'un tag



## Ignorer les modifications des fichiers traqués

Si vous avez des fichiers toujours dans votre status mais que vous ne voulez jamais commiter :
```shell
$ git update-index --assume-unchanged README.md
```

Pour lister les fichiers dans cet état :
```shell
$ git ls-files -v | grep '^h'
h README.md
```

Revenir en arrière :
```shell
$ git update-index --no-assume-unchanged README.md
```

Pour simplifier ces commandes :
```ini
[alias]
        forget = update-index --assume-unchanged 
        unforget = update-index --no-assume-unchanged
        forgotten = ! git ls-files -v | grep ^[a-z]
```



## Divers

Un cheat sheet bien sympa : http://ndpsoftware.com/git-cheatsheet.html

Activer la completion shell (dans [`contrib/completion`](https://github.com/git/git/tree/master/contrib/completion))

Utiliser les méthodes de prompt `__git_ps1*` ou un outil tel que [git-prompt](http://volnitsky.com/project/git-prompt/)

Des astuces à partager ?
