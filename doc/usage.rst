=====
Usage
=====

`pkglts` is intended to be used every time you want to create a package and maintain it throughout time
despite changes in the different services you use to test and distribute your package.

It has been though so you just have to regenerate your package everytime one of the tools you use changes
its interface (e.g. change some option in the yaml config file associated with the tool).

The sequence is always the same:

 * initialize your package in an empty directory
 * add options that represent the tools you intend to use
 * change settings for these options in the pkg_cfg file
 * regenerate your package

Then you can happily write some code to actually create functionalities in your package knowing you won't have
to care about continuous integration, testing or deployment :)

If you find yourself always using the same options with the same parameters everytime you create a new package
you can consider writing your very own plugin to smoothen your life. Then creating a new package will be as simple
as typing::

    $ pmg init my_plugin_name
    $ pmg rg
