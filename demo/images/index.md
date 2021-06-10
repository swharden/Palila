# Image Formatting

Include images inside `div` blocks with certain classes to control how they display.

## Default

* small images are left-aligned
* large images occupy the full width

```html
![](small.jpg)
```

![](small.jpg)

## Center

* To center an image use bootstrap's `text-center` in a `div`
* Spaces above and below the image line are recommended
* To include markdown inside HTML `div` apply the `markdown="block"` attribute

```html
<div markdown="block" class="text-center">

![](small.jpg)

</div>
```

<div markdown="block" class="text-center">

![](small.jpg)

</div>

## Border and Shadow

```html
<div markdown="block" class="text-center img-border">

![](small.jpg)

</div>
```

<div markdown="block" class="text-center img-border">

![](small.jpg)

</div>

## Sizing

Size of large images can be constrained with the following classes:

* `img-micro`
* `img-small`
* `img-medium`

### Micro

<div markdown="block" class="text-center img-border img-micro">

![](large.jpg)
![](large.jpg)
![](large.jpg)

</div>

### Small

<div markdown="block" class="text-center img-border img-small">

![](large.jpg)
![](large.jpg)

</div>

### Medium

<div markdown="block" class="text-center img-border img-medium">

![](large.jpg)

</div>

### No Restriction

<div markdown="block" class="text-center img-border">

![](large.jpg)

</div>

### Remote Image

<div markdown="block" class="text-center img-border">

![](https://mods.org/wp-content/uploads/2017/02/test-image.png)

</div>