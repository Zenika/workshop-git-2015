# Git log

<!-- .slide: class="page-title" -->



## Une brève histoire de Git

La génèse de Git :
```shell
$ git log --reverse --pretty=format:'%h %cd %an %n %s%n'

3e557c5 2005-04-05 00:00:00 +0000 BitMover
 BitMover arrête la version gratuite de BitKeeper

86b037e 2005-04-05 12:00:00 +0000 Linus Torvalds
 Linus Torvald démarre le développement de Git

a13dfb9 2005-04-07 22:13:13 +0000 Linus Torvalds
 Initial revision of "git", the information manager from hell

c6aac97 2005-04-16 22:20:36 +0000 Linus Torvalds
 Le noyau Linux est versionné sous Git
```



## 3e557c537ec302f0b6e4dd7d6fe73d677dd3267c

3e557c5 :
```git-log
$ git show 3e557c5
commit 3e557c537ec302f0b6e4dd7d6fe73d677dd3267c
Author: BitMover <bitkeeper@bitkeeper.com>
Date:   Tue Apr 5 00:00:00 2005 +0000

    BitMover arrête la version gratuite de BitKeeper
    
    http://www.bitkeeper.com/press/2005-04-05.html
    Fin de la version gratuite pour les projets open-source.
    Le noyau Linux doit trouver un autre outil de versionning...

diff --git a/bitkeeper b/bitkeeper
new file mode 100644
index 0000000..e69de29
```



## 86b037e9b2cb3a7283674a85e5f60407926e42a4

86b037e :
```git-log
$ git show 86b037e
commit 86b037e9b2cb3a7283674a85e5f60407926e42a4
Author: Linus Torvalds <torvalds@kernel.org>
Date:   Tue Apr 5 12:00:00 2005 +0000

    Linus Torvald démarre le développement de Git
    
    Ne trouvant pas d'alternative lui convenant,
    il démarre un nouvel outil pour versionner le noyau Linux.

diff --git a/bitkeeper b/bitkeeper
deleted file mode 100644
index e69de29..0000000
diff --git a/git b/git
new file mode 100644
index 0000000..e69de29
```



## a13dfb93446c7fa270371d47fba944bb132b72ba

a13dfb9 :
```git-log
$ git show a13dfb9
commit a13dfb93446c7fa270371d47fba944bb132b72ba
Author: Linus Torvalds <torvalds@kernel.org>
Date:   Fri Apr 7 22:13:13 2005 +0000

    Initial revision of "git", the information manager from hell
    
    https://git.kernel.org/cgit/git/git.git/commit/?id=e83c5163316f89bfbde7d9ab23ca2e25604af290
    Git est versionné sous Git après seulement 3 jours.

diff --git a/git b/git
index e69de29..3b62dc1 100644
--- a/git
+++ b/git
@@ -0,0 +1 @@
+Start
```



## c6aac977ad0ae2ee9be16cd222676f82bbfa81d5

c6aac97 :
```git-log
$ git show c6aac97
commit c6aac977ad0ae2ee9be16cd222676f82bbfa81d5
Author: Linus Torvalds <torvalds@kernel.org>
Date:   Sun Apr 16 22:20:36 2005 +0000

    Le noyau Linux est versionné sous Git
    
    https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=1da177e4c3f41524e886b7f1b8a0c1fc7321cac2
    Pour la 2.6.12-rc2 Linus passe le code du noyau sous Git.

diff --git a/kernel b/kernel
new file mode 100644
index 0000000..e69de29
```
