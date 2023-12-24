# nginx-extras-docs

Generation of docs for nginx-extras


## Book generation

Using https://github.com/orzih/mkdocs-with-pdf

```bash
pip install "qrcode[pil]"
```

Add to `plugins`:

```yaml
- with-pdf:
    author: Danila Vershinin
    copyright: GetPageSpeed LLC
    
    cover: true
    back_cover: true
    cover_title: NGINX Extras by GetPageSpeed
```

Generate book: `ENABLE_PDF_EXPORT=1 mkdocs build`
