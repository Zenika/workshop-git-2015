# La plomberie de Git

<!-- .slide: class="page-title" -->



## Les objets Git

Le principe de Git est simplement de stocker les contenus et de les identifier par leur hash SHA1.

Les contenus stockables sont répartis en 3 types :

- Blob
- Tree
- Commit



## Blob

C'est la représentation du contenu d'un fichier et uniquement le contenu.

TODO: representation graphique d'un blob

Pour créer un blob :
```shell
$ echo 'Hello world!' | git hash-object --stdin -w
cd0875583aabe89ee197ea133980a9085d08e497
```

Pour lire le contenu d'un blob :
```shell
$ git cat-file -p cd0875583aabe89ee197ea133980a9085d08e497
Hello world!
```

Ajoutons encore quelques blobs :
```shell
$ echo '' | git hash-object --stdin -w
8b137891791fe96927ad78e64b0aad7bded08bdc
$ echo 'Zenika' | git hash-object --stdin -w
f825c6ac4780ce6b1ba465167167bfaffe8a6e93
```



## Tree

C'est la représentation d'un dossier.

Liste les fichiers et le blob de leur contenu.

TODO: representation graphique d'un tree

Pour créer un tree, il faut passer par l'index :
```shell
$ git update-index --add --cacheinfo \
100644 cd0875583aabe89ee197ea133980a9085d08e497 HelloWorld.txt
$ git update-index --add --cacheinfo \
100644 8b137891791fe96927ad78e64b0aad7bded08bdc empty.txt
$ git write-tree
55f82bcf8364111553db85ffd35f3047dcbb237f
```

Pour vérifier le contenu d'un tree :
```shell
$ git cat-file -p 55f82bcf8364111553db85ffd35f3047dcbb237f
100644 blob cd0875583aabe89ee197ea133980a9085d08e497	HelloWorld.txt
100644 blob 8b137891791fe96927ad78e64b0aad7bded08bdc	empty.txt
```



## Tree inception

Créons une vraie arborescence :
```shell
$ git read-tree --prefix=folder 55f82bcf8364111553db85ffd35f3047dcbb237f
$ git update-index --add --cacheinfo \
100644 f825c6ac4780ce6b1ba465167167bfaffe8a6e93 Zenika.txt
$ git update-index --remove HelloWorld.txt
$ git update-index --remove empty.txt
$ git write-tree
0d5a735b5fd6ec5366e94f5380e15c3f88d03935
```
```shell
$ git cat-file -p 0d5a735b5fd6ec5366e94f5380e15c3f88d03935
100644 blob f825c6ac4780ce6b1ba465167167bfaffe8a6e93	Zenika.txt
040000 tree 55f82bcf8364111553db85ffd35f3047dcbb237f	folder

$ git cat-file -p 55f82bcf8364111553db85ffd35f3047dcbb237f
100644 blob cd0875583aabe89ee197ea133980a9085d08e497	HelloWorld.txt
100644 blob 8b137891791fe96927ad78e64b0aad7bded08bdc	empty.txt
```





