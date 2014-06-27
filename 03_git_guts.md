# Les entrailles de Git

<!-- .slide: class="page-title" -->



## Stockage des objets Git

Comment sont stockés nos objets ?
```shell
$ tree .git/objects/
.git/objects/
├── 0d
│   └── 5a735b5fd6ec5366e94f5380e15c3f88d03935
├── 55
│   └── f82bcf8364111553db85ffd35f3047dcbb237f
├── 8b
│   └── 137891791fe96927ad78e64b0aad7bded08bdc
├── cd
│   └── 0875583aabe89ee197ea133980a9085d08e497
├── d2
│   └── 85c028104fbb7f6660124ec3d6d6ce71931a19
├── ee
│   └── aed96b54b42657303b5d3eb7f6bf1b72fab94a
├── f3
│   └── e305e8e299c36370302a7b695d457c2aa14a7a
└── f8
    └── 25c6ac4780ce6b1ba465167167bfaffe8a6e93

8 directories, 8 files
```



## Contenu des fichiers objets

De simples fichiers donc !
```shell
$ cat .git/objects/cd/0875583aabe89ee197ea133980a9085d08e497
xR04f�H���W(�/�IQ�IA�K��OR04f�H���W(�/�IQ�IA�
```

Pas si simples que ça...

Pour gagner de la place, les contenus sont compressés avec zlib.

zlibu.py :
```python
#!/usr/bin/env python
import sys, zlib
sys.stdout.write(zlib.decompress(sys.stdin.read()))
```

zlibc.py :
```python
#!/usr/bin/env python
import sys, zlib
sys.stdout.write(zlib.compress(sys.stdin.read()))
```



## Décompression

Regardons la version décompréssée :
```shell
$ cat .git/objects/cd/0875583aabe89ee197ea133980a9085d08e497\
 | zlibu.py | cat -v
blob 13^@Hello world!
$ cat .git/objects/f8/25c6ac4780ce6b1ba465167167bfaffe8a6e93\
 | zlibu.py | cat -v
blob 7^@Zenika
```

Donc un blob est stocké sous la forme :
```
blob SPACE <size> NULL <content>
```



## Contenu d'un fichier de tree

Et pour les tree ?
```shell
$ cat .git/objects/55/f82bcf8364111553db85ffd35f3047dcbb237f\
 | zlibu.py | cat -v
tree 79^@100644 HelloWorld.txt^@M-M^HuX:M-+M-hM-^^M-
aM-^WM-j^S9M-^@M-)^H]^HM-dM-^W100644 empty.txt^@M-^K
^SxM-^Qy^_M-ii'M--xM-fK
M--{M-^M-PM-^KM-\
```

Gné ??!!

```shell
$ cat .git/objects/55/f82bcf8364111553db85ffd35f3047dcbb237f\
 | zlibu.py | xxd -p
74726565203739003130303634342048656c6c6f576f726c642e74787400
_cd0875583aabe89ee197ea133980a9085d08e497_31303036343420656d70
74792e74787400_8b137891791fe96927ad78e64b0aad7bded08bdc_

```

Ah mais c'est la version binaire des SHA1 !



## Forme de stockage d'un tree

Pour l'autre tree :
```shell
$ cat .git/objects/0d/5a735b5fd6ec5366e94f5380e15c3f88d03935\
 | zlibu.py | cat -v
tree 71^@100644 Zenika.txt^@M-x%M-FM-,GM-^@M-
Nk^[M-$e^VqgM-?M-/M-~M-^JnM-^S40000 folder^@UM-
x+M-OM-^Cd^Q^USM-[M-^EM-^?M-S_0GM-\M-;#^?
```

Donc un tree est stocké sous la forme :
```
tree SPACE <size> NULL (<mode> SPACE <name> <binary_sha1>)+
```



## Contenu d'un fichier de commit

Voyons pour les commits.
```shell
$ cat .git/objects/ee/aed96b54b42657303b5d3eb7f6bf1b72fab94a\
 | zlibu.py | cat -v
commit 207^@tree 0d5a735b5fd6ec5366e94f5380e15c3f88d03935
author Alexandre Garnier <alexandre.garnier@zenika.com> 1394530133 +0100
committer Alexandre Garnier <alexandre.garnier@zenika.com> 1394530133 +0100

1st commit

$ cat .git/objects/f3/e305e8e299c36370302a7b695d457c2aa14a7a\
 | zlibu.py | cat -v
commit 255^@tree d285c028104fbb7f6660124ec3d6d6ce71931a19
parent eeaed96b54b42657303b5d3eb7f6bf1b72fab94a
author Alexandre Garnier <alexandre.garnier@zenika.com> 1395859028 +0100
committer Alexandre Garnier <alexandre.garnier@zenika.com> 1395859028 +0100

2nd commit
```

Ah ben ici les SHA1 restent en hexa...



## Forme de stockage d'un commit

Donc un commit est stocké sous la forme :
```shell
commit SPACE <size> NULL tree SPACE <sha1> LF
(parent SPACE <sha1> LF)*
author SPACE <author> SPACE <timestamp> LF
commiter SPACE <committer> SPACE <timestamp> LF
LF
<message>
```



## À nous

Créons notre blob :
```shell
$ BLOB=`echo -n 'Hello world!\n'` && echo -ne $BLOB
Hello world!

$ GIT_OBJECT=`echo -n "blob \`echo -ne $BLOB\
 | wc --bytes\`\x00$BLOB"` && echo -ne $CONTENT
blob 13Hello world!

$ SHA1=`echo -ne $GIT_OBJECT | sha1sum | awk '{ print $1 }'`\
 && echo $SHA1
cd0875583aabe89ee197ea133980a9085d08e497
```

On est sur la bonne voie.

```shell
$ mkdir -p .git/objects/${SHA1:0:2}

$ echo -ne $GIT_OBJECT\
 | zlibc.py > .git/objects/${SHA1:0:2}/${SHA1:2}

$ git cat-file -p $SHA1
Hello world!
```



## Les autres blobs

Continuons :
```shell
$ BLOB=`echo -n '\n'`
$ GIT_OBJECT=`echo -n "blob \`echo -ne $BLOB\
 | wc --bytes\`\x00$BLOB"`
$ SHA1=`echo -ne $GIT_OBJECT | sha1sum | awk '{ print $1 }'`
$ mkdir -p .git/objects/${SHA1:0:2}
$ echo -ne $GIT_OBJECT\
 | zlibc.py > .git/objects/${SHA1:0:2}/${SHA1:2}
$ git cat-file -p $SHA1

```

```shell
$ BLOB=`echo -n 'Zenika\n'`
$ GIT_OBJECT=`echo -n "blob \`echo -ne $BLOB\
 | wc --bytes\`\x00$BLOB"`
$ SHA1=`echo -ne $GIT_OBJECT | sha1sum | awk '{ print $1 }'`
$ mkdir -p .git/objects/${SHA1:0:2}
$ echo -ne $GIT_OBJECT\
 | zlibc.py > .git/objects/${SHA1:0:2}/${SHA1:2}
$ git cat-file -p $SHA1
Zenika
```



## Les tree

Passons au tree :
```shell
$ echo -ne "100644 HelloWorld.txt\x00`echo 'cd0875583aabe89ee197ea133980a9085d08e497'\
 | xxd -r -p`100644 empty.txt\x00`echo '8b137891791fe96927ad78e64b0aad7bded08bdc'\
 | xxd -r -p`" > tree

$ (echo -ne "tree `cat tree\
 | wc --bytes`\x00"; cat tree) > git_object

$ SHA1=`sha1sum git_object | awk '{ print $1 }'`

$ mkdir -p .git/objects/${SHA1:0:2}

$ cat git_object\
 | zlibc.py > .git/objects/${SHA1:0:2}/${SHA1:2}

$ git ls-tree -r $SHA1
100644 blob cd0875583aabe89ee197ea133980a9085d08e497	HelloWorld.txt
100644 blob 8b137891791fe96927ad78e64b0aad7bded08bdc	empty.txt
```



## Encore des trees

Le tree racine maintenant :
```shell
$ echo -ne "100644 Zenika.txt\x00`echo 'f825c6ac4780ce6b1ba465167167bfaffe8a6e93'\
 | xxd -r -p`40000 folder\x00`echo '55f82bcf8364111553db85ffd35f3047dcbb237f'\
 | xxd -r -p`" > tree

$ (echo -ne "tree `cat tree\
 | wc --bytes`\x00"; cat tree) > git_object

$ SHA1=`sha1sum git_object | awk '{ print $1 }'`

$ mkdir -p .git/objects/${SHA1:0:2}

$ cat git_object\
 | zlibc.py > .git/objects/${SHA1:0:2}/${SHA1:2}

$ git ls-tree -r $SHA1
100644 blob f825c6ac4780ce6b1ba465167167bfaffe8a6e93	Zenika.txt
100644 blob cd0875583aabe89ee197ea133980a9085d08e497	folder/HelloWorld.txt
100644 blob 8b137891791fe96927ad78e64b0aad7bded08bdc	folder/empty.txt

```



## Le commit

Et maintenant le commit :
```shell
$ echo 'tree 0d5a735b5fd6ec5366e94f5380e15c3f88d03935
author Alexandre Garnier <alexandre.garnier@zenika.com> 1394530133 +0100
committer Alexandre Garnier <alexandre.garnier@zenika.com> 1394530133 +0100

1st commit' > commit

$ (echo -ne "commit `cat commit\
 | wc --bytes`\x00"; cat commit) > git_object

$ SHA1=`sha1sum git_object | awk '{ print $1 }'`

$ mkdir -p .git/objects/${SHA1:0:2}

$ cat git_object\
 | zlibc.py > .git/objects/${SHA1:0:2}/${SHA1:2}

$ git cat-file -p $SHA1
tree 0d5a735b5fd6ec5366e94f5380e15c3f88d03935
author Alexandre Garnier <alexandre.garnier@zenika.com> 1394530133 +0100
committer Alexandre Garnier <alexandre.garnier@zenika.com> 1394530133 +0100

1st commit
```



## La référence master

Il ne reste plus qu'à positionner 'master' sur notre commit :
```shell
$ echo $SHA1 > .git/refs/heads/master
$ git show --no-patch master
commit eeaed96b54b42657303b5d3eb7f6bf1b72fab94a
Author: Alexandre Garnier <alexandre.garnier@zenika.com>
Date:   Tue Mar 11 10:28:53 2014 +0100

    1st commit
```
