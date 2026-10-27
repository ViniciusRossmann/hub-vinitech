# hub-vinitech

My hub site.

## Deploy automático

Commits em `main` publicam a imagem privada no GHCR. O Image Updater registra o
digest em `platform/projects/hub-vinitech.yaml` no repositório privado
[vps-infra](https://github.com/ViniciusRossmann/vps-infra), e o Argo CD Core aplica
o estado no k3s. Não há SSH, kubeconfig ou token de deploy nos Secrets deste projeto.

Variáveis e referências de Secrets são declaradas nesse mesmo YAML. Os valores
ficam nos Actions Secrets deste repositório. A plataforma detecta mudanças e
sincroniza somente as chaves selecionadas, usando OIDC, com rollout automático.
Uma imagem do mesmo SHA já publicada é reutilizada em atualizações de Secrets.

A configuração de produção preserva porta 3000, namespace compartilhado `apps`,
cache temporário do Next.js e os domínios `viniciusnunes.dev.br` e
`www.viniciusnunes.dev.br`. O sucesso do build é separado da saúde do rollout;
consulte a documentação de operação em `vps-infra` para diagnóstico e rollback.
