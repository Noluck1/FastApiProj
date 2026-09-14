# template-vue

Vue 3 + Vite template with repository-local shared UI built on the official `shadcn-vue` workflow.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## UI Stack

- Base UI source: `shadcn-vue`
- Registry workflow: `components.json` + registry `@shadcn`
- App import entry point: `@/shared/ui`
- Shared class helper: `@/shared/lib/utils`
- Toast layer: `vue-sonner` through `@/shared/ui/sonner`
- Form validation: `shadcn-vue` Form + `vee-validate` + `@vee-validate/zod` + `zod`
- Starter primitives included: `Button`, `Input`, `Textarea`, `Card`, `Label`, `Toaster`, `Form`

## MCP shadcn

- This template is intended to be used with MCP shadcn for browsing and adding components from registries.
- Project-local VS Code config lives in [`.vscode/mcp.json`](./.vscode/mcp.json).
- For Codex, configure the shadcn MCP server in `~/.codex/config.toml`:

```toml
[mcp_servers.shadcn]
command = "npx"
args = ["shadcn-vue@latest", "mcp"]
```

## Registry Workflow

1. Use MCP shadcn to search or browse the `@shadcn` registry.
2. Add required components through the registry workflow instead of inventing primitives.
3. Keep app-facing imports routed through `@/shared/ui`.
4. Use canonical shared exports such as `Button`, `Input`, `Toaster`, and `toast`.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/) and [shadcn-vue docs](https://www.shadcn-vue.com/docs).

## Project Setup

```sh
npm install
```

## Deployment Templates

The template includes deployment-ready examples based on GitLab CI, Docker, and Kubernetes:

- [`.gitlab-ci.yml`](./.gitlab-ci.yml) runs checks, builds the app, builds and pushes a Docker image on `main`, then applies Kubernetes manifests.
- [`app.Dockerfile`](./app.Dockerfile) builds the Vite app and serves the compiled `dist` folder on port `80`.
- [`k8s/deployment.yaml`](./k8s/deployment.yaml), [`k8s/svc.yaml`](./k8s/svc.yaml), and [`k8s/ingress-route.yaml`](./k8s/ingress-route.yaml) are applied through `envsubst`.

Configure these CI/CD variables before enabling production deploy:

| Variable                                            | Purpose                                                                      |
| --------------------------------------------------- | ---------------------------------------------------------------------------- |
| `CI_REGISTRY_GITLAB` / `CI_REGISTRY`                | Docker registry host.                                                        |
| `CI_REGISTRY_USER_GITLAB` / `CI_REGISTRY_USER`      | Docker registry user.                                                        |
| `CI_REGISTRY_TOKEN_GITLAB` / `CI_REGISTRY_PASSWORD` | Docker registry token or password.                                           |
| `K8S_SERVER`                                        | Kubernetes API server URL.                                                   |
| `K8S_TOKEN`                                         | Base64-encoded Kubernetes service account token.                             |
| `K8S_NAMESPACE`                                     | Target Kubernetes namespace.                                                 |
| `CI_K8S_REGISTRY_SECRET_NAME`                       | Image pull secret name in the target namespace.                              |
| `K8S_HOST`                                          | Public host for the Traefik `IngressRoute`.                                  |
| `K8S_BASE_PATH`                                     | Public route prefix without trailing slash, for example `/my-app`.           |
| `VITE_BASE_PATH`                                    | Optional Vite asset base path. When provided, it must match `K8S_BASE_PATH`. |
| `VITE_API_BASE_URL`                                 | Optional API base URL exposed to frontend code.                              |
| `NPM_TOKEN`, `NPM_REGISTRY`, `NPM_SCOPE`            | Optional private npm registry settings; provide all three together.          |

Optional deploy defaults can be overridden with `APP_IMAGE_TAG`, `K8S_APP_NAME`, `K8S_REPLICAS`, `K8S_SERVICE_PORT`, and `K8S_CONTAINER_PORT`. `K8S_APP_NAME` must be a Kubernetes DNS label up to 50 characters so suffixes like `-svc` and `-strip-prefix` stay valid.

### Add shadcn Components

```sh
npm shadcn-vue add @shadcn/button @shadcn/input @shadcn/textarea @shadcn/card @shadcn/sonner @shadcn/form
```

### Form Validation Pattern

- Shared form primitives come from `@/shared/ui`.
- Page-level schema and `useForm()` logic stay in `pages/<Page>/model`.
- Use `FormField`, `FormItem`, `FormLabel`, `FormControl`, `FormDescription`, and `FormMessage`.

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
