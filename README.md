# Potato Classifier 🥔

Ever wondered if that odd blob on your plate is a potato… or not? Get your **Instant Verdict**! ⚡  
**Zero Science Degree Required** 🎓 — **No More Spud Doubts** 🤯  

Powered by a NextViT-Small model (fine-tuned on spud images) and exported to ONNX for lightning-fast inference.

Check out the live demo [here](https://projects.byvova.com/potato/).

Created through the combined efforts of [**@aalizelau**](https://github.com/aalizelau) (ML) and [**@vovapyc**](https://github.com/vovapyc) (Engineering).

## Frontend development

Use Node.js 22.23.4 or a newer 22.x release. From `frontend/`, run `nvm use`
(or select the version in `.nvmrc` with your Node manager), `npm ci`, then
`npm run build`. GitHub Pages uses the same pinned version and validates pull
requests without deploying them. The Python API and its Fly.io hosting are
unchanged.
